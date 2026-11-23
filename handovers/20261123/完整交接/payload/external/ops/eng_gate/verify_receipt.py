#!/usr/bin/env python3
"""零额度回执校验器（v0.2，2026-11-10 14:35 起全项目执行，ADR-EG1）。

用法：
  python3 verify_receipt.py <receipt.json> [--project-root 项目根目录] [--baseline 基线清单]
                            [--no-run-tests] [--json] [--now ISO时间]

v0.2 新增（任意项目目录）：
  --project-root DIR  回执里的相对路径按 DIR 解析；targets 和 protected 必须落在 DIR 之内（C15）。
                      不给时若基线头部写了 root 则用它。
  --baseline FILE     总协调派活前用 baseline.sh 生成的基线（C14）：
                      - modify/delete 目标必须在基线里，且 before_sha256 必须等于基线值（Builder 不能自填）；
                      - add 目标在基线里必须是 ABSENT（派活时不存在）；
                      - 基线里不是目标的文件一律当未授权文件，哈希必须不变。

原则：回执里的自报值只当"线索"，能重算的一律由本脚本自己重算：
  - 重算每个 target 的 SHA-256，与 after_sha256 比对；文件为空直接 FAIL；
  - diff 文件必须存在、非空、是统一 diff 格式；
  - 对 modify 类 target，在临时目录里用 `patch -R` 反向应用 diff，计时，
    重算回滚结果哈希必须等于 before_sha256（G3 独立复算，不碰原文件）；
  - .py 目标用 ast + py_compile 编译到临时目录（不在源码旁写 __pycache__）；
  - executed_at 必须带时区、不得在未来（容差 120 秒）；
  - 测试数量守恒 total == passed + failed，failed == 0，exit_code == 0；
  - 回执给了测试命令（argv 列表）就默认重跑，退出码必须为 0 且与自报一致，带超时；
  - 给了 manifest_path 就逐行重算；给了 git_repo 就只读查 `git status --porcelain`；
  - protected 列表里的未授权文件哈希必须不变。
输出每项 PASS/FAIL/WARN 和原因；任一 FAIL → 退出码 1，否则 0。
本脚本只读：不写、不删、不改任何回执里提到的文件；不读密钥目录。
"""
import argparse, ast, datetime as dt, hashlib, json, os, py_compile, re, shutil
import subprocess, sys, tempfile, time

HEX64 = re.compile(r"^[0-9a-f]{64}$")
FUTURE_SKEW_S = 120
DENY_PREFIXES = ("/home/box/secrets", "/workspace/foundation/keys")
DENY_NAMES = re.compile(r"^(\.env(\..*)?|.*\.pem|.*\.key|id_rsa.*|.*cookies?(\.txt|\.json)?|.*_token|tokens?\.(txt|json))$", re.I)
TIER_ROLLBACK_LIMIT_S = {"T0": 0.1, "T1": 60.0}   # T2~T4 只要求有回滚方案/批准记录；C=内容类
MAX_TEST_TIMEOUT_S = 900


class Report:
    def __init__(self):
        self.items = []

    def add(self, status, code, msg):
        self.items.append({"status": status, "check": code, "detail": msg})

    def ok(self, c, m): self.add("PASS", c, m)
    def fail(self, c, m): self.add("FAIL", c, m)
    def warn(self, c, m): self.add("WARN", c, m)

    @property
    def verdict(self):
        return "FAIL" if any(i["status"] == "FAIL" for i in self.items) else "PASS"


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def denied(path):
    rp = os.path.realpath(path)
    if any(rp == p or rp.startswith(p + "/") for p in DENY_PREFIXES):
        return True
    return bool(DENY_NAMES.match(os.path.basename(rp)))


def inside(path, root):
    rp, rr = os.path.realpath(path), os.path.realpath(root)
    return rp == rr or rp.startswith(rr.rstrip("/") + "/")


def load_baseline(path):
    """读 baseline.sh 生成的基线：返回 (头部 dict, {绝对路径: sha256 或 'ABSENT'}, 错误)。"""
    head, entries = {}, {}
    try:
        lines = open(path, encoding="utf-8").read().splitlines()
    except OSError as e:
        return head, entries, f"基线读不了：{e}"
    for ln in lines:
        if not ln.strip():
            continue
        if ln.startswith("#"):
            m = re.match(r"^#\s*([a-z_]+):\s*(.*)$", ln)
            if m:
                head[m.group(1)] = m.group(2).strip()
            continue
        m = re.match(r"^([0-9a-f]{64}|ABSENT)  (/.+)$", ln)
        if not m:
            return head, entries, f"基线格式错：{ln[:80]}"
        entries[m.group(2)] = m.group(1)
    if head.get("format") != "eng_gate-baseline-v1":
        return head, entries, "基线头部缺 '# format: eng_gate-baseline-v1'，不是 baseline.sh 生成的"
    if not entries:
        return head, entries, "基线为空"
    return head, entries, None


def resolve_paths(rc, root):
    """把回执里的相对路径按项目根目录解析成绝对路径（只改内存里的副本）。"""
    if not root:
        return
    fix = lambda p: os.path.normpath(os.path.join(root, p)) if isinstance(p, str) and p and not os.path.isabs(p) else p
    for t in rc.get("targets") or []:
        if isinstance(t, dict):
            for k in ("path", "diff_path"):
                if k in t:
                    t[k] = fix(t[k])
    for p in rc.get("protected") or []:
        if isinstance(p, dict) and "path" in p:
            p["path"] = fix(p["path"])
    g = rc.get("gates") if isinstance(rc.get("gates"), dict) else {}
    g2, g3 = g.get("gate2_invariants_and_tests"), g.get("gate3_simulated_rollback")
    if isinstance(g2, dict) and g2.get("cwd"):
        g2["cwd"] = fix(g2["cwd"])
    if isinstance(g3, dict) and g3.get("rollback_plan"):
        g3["rollback_plan"] = fix(g3["rollback_plan"])
    ev = rc.get("gate4_evidence")
    if isinstance(ev, dict):
        for k in ("manifest_path", "git_repo", "asset_register"):
            if ev.get(k):
                ev[k] = fix(ev[k])


def check_root(r, rc, root):
    if not root:
        return
    if not os.path.isdir(root):
        r.fail("C15", f"项目根目录不存在：{root}"); return
    out = [t.get("path") for t in rc["targets"] if isinstance(t, dict) and isinstance(t.get("path"), str)
           and not inside(t["path"], root)]
    out += [p.get("path") for p in rc.get("protected", []) if isinstance(p, dict)
            and isinstance(p.get("path"), str) and not inside(p["path"], root)]
    if out:
        r.fail("C15", f"以下路径不在项目根目录 {root} 之内（越界改动）：{out[:5]}")
    else:
        r.ok("C15", f"targets/protected 全部位于项目根目录 {root} 之内")


def check_baseline(r, rc, head, entries, root):
    if root and head.get("root") and os.path.realpath(head["root"]) != os.path.realpath(root):
        r.fail("C14", f"基线 root={head['root']} 与 --project-root={root} 不一致")
    tpaths = set()
    for i, t in enumerate(rc["targets"]):
        if not isinstance(t, dict) or not isinstance(t.get("path"), str):
            continue
        p, ch = t["path"], t.get("change", "modify")
        tpaths.add(p)
        b = entries.get(p)
        if ch == "add":
            if b is None:
                r.warn("C14", f"target[{i}] 新增文件不在基线里（派活时没登记要新增的路径）：{p}")
            elif b != "ABSENT":
                r.fail("C14", f"target[{i}] 声称新增，但派活时该文件已存在：{p}")
            else:
                r.ok("C14", f"target[{i}] 新增文件在基线里登记为 ABSENT")
            continue
        if b is None:
            r.fail("C14", f"target[{i}] 不在总协调的基线里（未授权改动或没拍基线）：{p}")
        elif b == "ABSENT":
            r.fail("C14", f"target[{i}] 基线里该文件不存在，change 应为 add：{p}")
        elif t.get("before_sha256") != b:
            r.fail("C14", f"target[{i}] before_sha256 与总协调基线 {b[:12]}… 不一致（Builder 不能自填 before）：{p}")
        else:
            r.ok("C14", f"target[{i}] before_sha256 与总协调基线一致")
    changed = []
    n = 0
    for p, b in entries.items():
        if p in tpaths:
            continue
        n += 1
        if b == "ABSENT":
            if os.path.lexists(p):
                changed.append(f"{p}（基线不存在，现在多出来了）")
        elif denied(p) or not os.path.isfile(p) or sha256_file(p) != b:
            changed.append(p)
    if changed:
        r.fail("C14", f"基线中非目标文件 {n} 个，变化或缺失 {len(changed)} 个：{changed[:5]}")
    else:
        r.ok("C14", f"基线中非目标文件 {n} 个哈希全部不变")


def parse_ts(s):
    if not isinstance(s, str):
        return None, "不是字符串"
    try:
        t = dt.datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError as e:
        return None, f"不是 ISO 8601：{e}"
    if t.tzinfo is None or t.utcoffset() is None:
        return None, "没有时区（必须带 +08:00 之类的偏移）"
    return t, None


def check_structure(r, rc):
    need = {"task_id": str, "executed_at": str, "executor": str, "verifier": str,
            "targets": list, "gates": dict, "overall_verdict": str}
    good = True
    for k, typ in need.items():
        if k not in rc:
            r.fail("C02", f"缺字段 {k}"); good = False
        elif not isinstance(rc[k], typ):
            r.fail("C02", f"字段 {k} 类型应为 {typ.__name__}"); good = False
    if good and not rc["targets"]:
        r.fail("C02", "targets 为空：没有任何可核对的改动"); good = False
    if good and rc["executor"].strip() and rc["executor"] == rc["verifier"]:
        r.fail("C02", "executor 与 verifier 相同：自己验自己不算独立验证"); good = False
    for g in ("gate1_syntax_and_py_compile", "gate2_invariants_and_tests",
              "gate3_simulated_rollback", "gate4_manifest_hash_check"):
        if good and g not in rc["gates"]:
            r.fail("C02", f"gates 缺 {g}"); good = False
    if good:
        r.ok("C02", "必填字段与类型齐全")
    if "environment" not in rc:
        r.warn("C02", "缺 environment（协议要求回执含环境信息，模板未列；建议补 host/python/tz）")
    return good


def check_time(r, rc, now):
    t, err = parse_ts(rc.get("executed_at"))
    if err:
        r.fail("C03", f"executed_at {err}"); return
    if (t - now).total_seconds() > FUTURE_SKEW_S:
        r.fail("C03", f"executed_at={rc['executed_at']} 在未来（比校验时刻晚 {int((t-now).total_seconds())} 秒）")
    else:
        r.ok("C03", f"executed_at 带时区且不在未来（{rc['executed_at']}）")


def looks_like_unified_diff(text):
    return ("--- " in text and "+++ " in text and "@@" in text)


def rehearse_rollback(target_path, diff_path, before_sha):
    """在临时目录复制 after 文件，patch -R 反向应用 diff，返回 (ok, 耗时秒, 说明)。不碰原文件。"""
    if shutil.which("patch") is None:
        return False, None, "本机没有 patch 命令，无法独立复算回滚"
    with tempfile.TemporaryDirectory(prefix="vr_rb_") as td:
        work = os.path.join(td, "work")
        shutil.copy2(target_path, work)
        out = os.path.join(td, "restored")
        t0 = time.perf_counter()
        p = subprocess.run(["patch", "-R", "-s", "-f", "-o", out, work, diff_path],
                           capture_output=True, text=True, timeout=30)
        el = time.perf_counter() - t0
        if p.returncode != 0 or not os.path.exists(out):
            return False, el, f"patch -R 失败 rc={p.returncode} {p.stdout.strip()[:200]} {p.stderr.strip()[:200]}"
        got = sha256_file(out)
        if got != before_sha:
            return False, el, f"反向应用后哈希 {got[:12]}… ≠ before_sha256 {before_sha[:12]}…"
        return True, el, "反向应用后哈希与 before_sha256 逐字节一致"


def check_python(r, idx, path):
    try:
        src = open(path, "rb").read()
        tree = ast.parse(src, filename=path)
    except SyntaxError as e:
        r.fail("C06", f"target[{idx}] ast 解析失败：{e}"); return
    with tempfile.TemporaryDirectory(prefix="vr_pyc_") as td:
        try:
            py_compile.compile(path, cfile=os.path.join(td, "x.pyc"), doraise=True)
        except py_compile.PyCompileError as e:
            r.fail("C06", f"target[{idx}] py_compile 失败：{e.msg[:300]}"); return
    # 静态查顶层 import 能否找到（不执行模块代码；相对导入跳过）
    mods = set()
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            mods.update(a.name.split(".")[0] for a in n.names)
        elif isinstance(n, ast.ImportFrom) and n.level == 0 and n.module:
            mods.add(n.module.split(".")[0])
    if mods:
        code = ("import importlib.util,sys,json;m=json.loads(sys.argv[1]);"
                "print(json.dumps([x for x in m if importlib.util.find_spec(x) is None]))")
        p = subprocess.run([sys.executable, "-I", "-c", code, json.dumps(sorted(mods))],
                           capture_output=True, text=True, timeout=30,
                           cwd=os.path.dirname(path),
                           env={"PYTHONPATH": os.path.dirname(path), "PATH": os.environ.get("PATH", "")})
        try:
            missing = json.loads(p.stdout.strip() or "[]")
        except ValueError:
            missing = ["<查询失败>"]
        if missing:
            r.fail("C06", f"target[{idx}] 找不到的导入：{missing}"); return
    r.ok("C06", f"target[{idx}] ast + py_compile 通过，顶层导入 {len(mods)} 个均可找到")


def check_targets(r, rc):
    tier = rc.get("risk_tier", "T0")
    for i, t in enumerate(rc["targets"]):
        if not isinstance(t, dict):
            r.fail("C04", f"target[{i}] 不是对象"); continue
        path, after, before = t.get("path"), t.get("after_sha256"), t.get("before_sha256")
        change = t.get("change", "modify")
        if not isinstance(path, str) or not os.path.isabs(path):
            r.fail("C04", f"target[{i}] path 必须是绝对路径"); continue
        if denied(path):
            r.fail("C04", f"target[{i}] 位于密钥目录，拒绝读取"); continue
        if change not in ("modify", "add", "delete"):
            r.fail("C04", f"target[{i}] change={change!r} 不认识"); continue
        if change != "add" and not (isinstance(before, str) and HEX64.match(before)):
            r.fail("C04", f"target[{i}] before_sha256 不是 64 位小写十六进制"); continue
        if change == "delete":
            if os.path.exists(path):
                r.fail("C04", f"target[{i}] 声称已删除但文件仍存在")
            else:
                r.ok("C04", f"target[{i}] 已删除，文件确实不存在")
            continue
        if not (isinstance(after, str) and HEX64.match(after)):
            r.fail("C04", f"target[{i}] after_sha256 不是 64 位小写十六进制"); continue
        if not os.path.isfile(path):
            r.fail("C04", f"target[{i}] 文件不存在：{path}"); continue
        size = os.path.getsize(path)
        if size == 0:
            r.fail("C04", f"target[{i}] 文件为空（0 字节），空产物不算交付：{path}"); continue
        got = sha256_file(path)
        if got != after:
            r.fail("C04", f"target[{i}] 重算哈希 {got[:12]}… ≠ 自报 after_sha256 {after[:12]}…（被改过或自报不实）")
            continue
        if change == "modify" and before == after:
            r.fail("C04", f"target[{i}] before 与 after 哈希相同：声称修改但没有改动")
            continue
        r.ok("C04", f"target[{i}] 重算 SHA-256 与自报一致（{size} 字节）")

        dp = t.get("diff_path")
        diff_ok = False
        if (not isinstance(dp, str) or not dp) and tier == "C" and change == "add":
            r.ok("C05", f"target[{i}] 内容类新增成品，不要求文本 diff（产物门由 gate2.command 重跑）")
        elif not isinstance(dp, str) or not dp:
            r.fail("C05", f"target[{i}] 没给 diff_path")
        elif denied(dp):
            r.fail("C05", f"target[{i}] diff 位于密钥目录，拒绝读取")
        elif not os.path.isfile(dp):
            r.fail("C05", f"target[{i}] diff 文件不存在：{dp}")
        elif os.path.getsize(dp) == 0:
            r.fail("C05", f"target[{i}] diff 文件为空：{dp}")
        else:
            txt = open(dp, encoding="utf-8", errors="replace").read()
            if not looks_like_unified_diff(txt):
                r.fail("C05", f"target[{i}] diff 不是统一 diff 格式（缺 ---/+++/@@）")
            else:
                r.ok("C05", f"target[{i}] diff 存在且为统一 diff 格式"); diff_ok = True

        if path.endswith(".py"):
            check_python(r, i, path)

        if change == "modify" and diff_ok:
            ok, el, why = rehearse_rollback(path, dp, before)
            limit = TIER_ROLLBACK_LIMIT_S.get(tier)
            if not ok:
                r.fail("C09", f"target[{i}] 独立回滚复算失败：{why}")
            elif tier == "T0" and el >= TIER_ROLLBACK_LIMIT_S["T0"]:
                r.fail("C09", f"target[{i}] 回滚复算耗时 {el:.4f}s ≥ {limit}s（T0 要求 <0.1s）")
            else:
                r.ok("C09", f"target[{i}] 临时目录反向应用 diff 复算回滚：{why}，耗时 {el:.4f}s")


def check_gate2(r, rc, run_tests):
    g = rc["gates"].get("gate2_invariants_and_tests")
    if not isinstance(g, dict):
        r.fail("C07", "gate2 不是对象"); return
    try:
        tot, ps, fl, ec = (int(g["total_tests"]), int(g["passed"]), int(g["failed"]), int(g["exit_code"]))
    except (KeyError, TypeError, ValueError) as e:
        r.fail("C07", f"gate2 计数字段缺失或非整数：{e}"); return
    probs = []
    if tot < 1: probs.append("total_tests < 1（没有测试）")
    if tot != ps + fl: probs.append(f"数量不守恒：total {tot} ≠ passed {ps} + failed {fl}")
    if fl != 0: probs.append(f"failed={fl}")
    if ec != 0: probs.append(f"exit_code={ec}")
    if probs:
        r.fail("C07", "；".join(probs))
    else:
        r.ok("C07", f"自报 {ps}/{tot} 通过、failed 0、exit 0，数量守恒")
    cmd = g.get("command")
    if not run_tests:
        r.warn("C08", "按 --no-run-tests 跳过重跑：测试结果仍是自报，未独立复核"); return
    if cmd is None:
        r.fail("C08", "回执没给测试命令 gate2.command（argv 列表），总协调无法重跑；自报结果不采信"); return
    if not (isinstance(cmd, list) and cmd and all(isinstance(x, str) for x in cmd)):
        r.fail("C08", "gate2.command 必须是非空字符串列表（不走 shell）"); return
    cwd = g.get("cwd") or None
    if cwd and (not os.path.isdir(cwd) or denied(cwd)):
        r.fail("C08", f"gate2.cwd 不存在或不允许：{cwd}"); return
    to = min(int(g.get("timeout_s", 300)), MAX_TEST_TIMEOUT_S)
    t0 = time.perf_counter()
    try:
        p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=to)
    except subprocess.TimeoutExpired:
        r.fail("C08", f"重跑测试超时（>{to}s），按失败处理"); return
    except OSError as e:
        r.fail("C08", f"重跑测试无法启动：{e}"); return
    el = time.perf_counter() - t0
    tail = (p.stdout + p.stderr).strip().splitlines()[-3:]
    if "Traceback (most recent call last)" in (p.stdout + p.stderr) and p.returncode == 0:
        r.fail("C08", "重跑退出码 0 但输出含未捕获 Traceback（负面清单第 2 条）"); return
    if p.returncode != 0 or p.returncode != ec:
        r.fail("C08", f"重跑退出码 {p.returncode}（自报 {ec}），耗时 {el:.2f}s；尾部输出：{tail}")
    else:
        r.ok("C08", f"重跑退出码 0 与自报一致，耗时 {el:.2f}s")


def check_gate3(r, rc):
    g = rc["gates"].get("gate3_simulated_rollback")
    tier = rc.get("risk_tier", "T0")
    if tier not in ("T0", "T1", "T2", "T3", "T4", "C"):
        r.fail("C10", f"risk_tier={tier!r} 不认识（T0~T4，内容类为 C）"); return
    if not isinstance(g, dict):
        r.fail("C10", "gate3 不是对象"); return
    if tier == "C":
        # 内容类：制作阶段可回滚=删掉新增成品；发布另按 T4 单独交回执
        if g.get("restore_by_delete") is True or (isinstance(g.get("rollback_plan"), str) and os.path.isfile(g["rollback_plan"])):
            r.ok("C10", "内容类回滚方式已声明（删除新增成品或附回滚方案）；发布须另按 T4 交回执")
        else:
            r.fail("C10", "内容类必须 restore_by_delete=true 或附存在的 rollback_plan 文件")
        return
    if tier == "T4":
        if g.get("not_rollbackable") is True and g.get("approval_ref"):
            r.ok("C10", f"T4 不可回滚类，已附批准记录 {g['approval_ref']}")
        else:
            r.fail("C10", "T4（对外发布/不可回滚）必须 not_rollbackable=true 且附 approval_ref")
        return
    probs = []
    if g.get("rollback_executed") is not True: probs.append("rollback_executed 不是 true")
    if g.get("restored_sha256_match") is not True: probs.append("restored_sha256_match 不是 true")
    lat = g.get("rollback_latency_seconds")
    if not isinstance(lat, (int, float)) or isinstance(lat, bool) or lat < 0:
        probs.append("rollback_latency_seconds 缺失或不是非负数")
    else:
        lim = TIER_ROLLBACK_LIMIT_S.get(tier)
        if lim is not None and lat >= lim:
            probs.append(f"自报回滚耗时 {lat}s ≥ {tier} 上限 {lim}s")
    if tier in ("T2", "T3"):
        rp = g.get("rollback_plan")
        if not (isinstance(rp, str) and os.path.isfile(rp)):
            probs.append(f"{tier} 必须附 rollback_plan（存在的文件路径）")
    if probs:
        r.fail("C10", "；".join(probs))
    else:
        r.ok("C10", f"{tier} 回滚自报项齐全（自报耗时 {lat}s；T0 的 modify 文件另由 C09 独立复算）")


def check_gate4(r, rc):
    g = rc["gates"].get("gate4_manifest_hash_check")
    extra = rc.get("gate4_evidence", {}) if isinstance(rc.get("gate4_evidence"), dict) else {}
    mp, repo, reg = extra.get("manifest_path"), extra.get("git_repo"), extra.get("asset_register")
    if g in ("N/A", "NOT_APPLICABLE"):
        if extra.get("na_reason"):
            r.warn("C11", f"G4 标为不适用：{extra['na_reason']}")
        else:
            r.fail("C11", "G4 标为不适用但没写 gate4_evidence.na_reason")
        return
    if not mp and not repo and not reg:
        r.fail("C11", f"自报 gate4={g!r}，但没给 gate4_evidence.manifest_path / git_repo / asset_register，无法复核")
        return
    if mp:
        if not os.path.isfile(mp):
            r.fail("C11", f"清单不存在：{mp}")
        else:
            base, bad, n = os.path.dirname(mp), [], 0
            for line in open(mp, encoding="utf-8"):
                line = line.rstrip("\n")
                if not line.strip():
                    continue
                m = re.match(r"^([0-9a-f]{64}) [ *](.+)$", line)
                if not m:
                    bad.append(f"格式错：{line[:60]}"); continue
                n += 1
                fp = m.group(2) if os.path.isabs(m.group(2)) else os.path.join(base, m.group(2))
                if denied(fp) or not os.path.isfile(fp) or sha256_file(fp) != m.group(1):
                    bad.append(m.group(2))
            if n == 0:
                r.fail("C11", "清单为空")
            elif bad:
                r.fail("C11", f"清单 {n} 项中不匹配 {len(bad)} 项：{bad[:5]}")
            else:
                r.ok("C11", f"清单 {n} 项全部重算匹配")
    if repo:
        p = subprocess.run(["git", "--no-optional-locks", "-C", repo, "status", "--porcelain"],
                           capture_output=True, text=True, timeout=60)
        if p.returncode != 0:
            r.fail("C11", f"git status 失败：{p.stderr.strip()[:200]}")
        elif p.stdout.strip():
            r.fail("C11", f"git 工作区不干净：{len(p.stdout.splitlines())} 项")
        else:
            r.ok("C11", "git 工作区干净")
    if reg:
        try:
            data = json.load(open(reg, encoding="utf-8"))
            assets = data.get("assets", data) if isinstance(data, dict) else data
            idx = {a.get("path"): a for a in assets if isinstance(a, dict)}
            miss = [t["path"] for t in rc["targets"] if isinstance(t, dict)
                    and t.get("change", "modify") != "delete"
                    and (t.get("path") not in idx or idx[t["path"]].get("sha256") != t.get("after_sha256"))]
            if miss:
                r.fail("C11", f"资产登记缺失或哈希不符：{miss}")
            else:
                r.ok("C11", "所有 target 已在资产登记且哈希一致")
        except (OSError, ValueError, AttributeError) as e:
            r.fail("C11", f"资产登记读不了：{e}")


def check_protected(r, rc):
    prot = rc.get("protected", [])
    if not prot:
        r.warn("C12", "没给 protected（未授权文件不变）清单，G1 的'未授权文件哈希不变'无法核")
        return
    bad = []
    for p in prot:
        fp, sh = p.get("path"), p.get("sha256")
        if not fp or denied(fp) or not os.path.isfile(fp) or sha256_file(fp) != sh:
            bad.append(fp)
    if bad:
        r.fail("C12", f"未授权文件哈希变化或缺失：{bad}")
    else:
        r.ok("C12", f"{len(prot)} 个未授权文件哈希不变")


def check_claims(r, rc):
    g1 = rc["gates"].get("gate1_syntax_and_py_compile")
    has_py = any(isinstance(t, dict) and str(t.get("path", "")).endswith(".py") for t in rc["targets"])
    if g1 == "N/A" and not has_py:
        r.ok("C13", "无 .py 目标，gate1 自报 N/A 合理（哈希类检查仍由 C04/C05 完成）")
    elif g1 != "PASS":
        r.fail("C13", f"自报 gate1={g1!r}，不是 PASS")
    if rc.get("overall_verdict") not in ("APPROVE_READY_FOR_DEPLOY", "PASS"):
        r.warn("C13", f"自报 overall_verdict={rc.get('overall_verdict')!r}（仅参考，结论以重算为准）")


def verify(path, run_tests=True, now=None, project_root=None, baseline=None):
    r = Report()
    now = now or dt.datetime.now(dt.timezone.utc)
    meta = {"receipt": path}
    head, entries = {}, {}
    if not denied(path) and os.path.isfile(path):
        meta["receipt_sha256"] = sha256_file(path)
    if baseline:
        head, entries, err = load_baseline(baseline)
        if err:
            r.fail("C14", err); return r, meta
        meta["baseline"] = baseline
        meta["baseline_sha256"] = sha256_file(baseline)
        project_root = project_root or head.get("root") or None
    if project_root:
        project_root = os.path.abspath(project_root)
        meta["project_root"] = project_root
    if denied(path) or not os.path.isfile(path):
        r.fail("C01", f"回执文件不存在或不允许读取：{path}"); return r, meta
    meta["receipt_sha256"] = sha256_file(path)
    try:
        rc = json.load(open(path, encoding="utf-8"))
    except (ValueError, UnicodeDecodeError) as e:
        r.fail("C01", f"回执不是合法 JSON：{e}"); return r, meta
    if not isinstance(rc, dict):
        r.fail("C01", "回执顶层不是对象"); return r, meta
    r.ok("C01", "回执是合法 JSON 对象")
    meta["task_id"] = rc.get("task_id")
    resolve_paths(rc, project_root)
    if not check_structure(r, rc):
        return r, meta
    check_root(r, rc, project_root)
    if baseline:
        check_baseline(r, rc, head, entries, project_root)
    elif project_root:
        r.warn("C14", "给了项目根目录但没给 --baseline：before_sha256 仍是 Builder 自报，未对总协调基线")
    check_time(r, rc, now)
    check_targets(r, rc)
    check_gate2(r, rc, run_tests)
    check_gate3(r, rc)
    check_gate4(r, rc)
    check_protected(r, rc)
    check_claims(r, rc)
    return r, meta


def main():
    ap = argparse.ArgumentParser(description="零额度回执校验（只读）")
    ap.add_argument("receipt")
    ap.add_argument("--no-run-tests", action="store_true", help="不重跑测试命令（结果标 WARN：仅自报）")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    ap.add_argument("--now", help="覆盖'当前时间'（ISO，带时区），仅测试用")
    ap.add_argument("--project-root", help="项目根目录：相对路径按它解析，targets/protected 不得越界")
    ap.add_argument("--baseline", help="总协调派活前用 baseline.sh 生成的基线清单")
    a = ap.parse_args()
    now = None
    if a.now:
        now, err = parse_ts(a.now)
        if err:
            print(f"--now {err}", file=sys.stderr); sys.exit(1)
    r, meta = verify(a.receipt, run_tests=not a.no_run_tests, now=now,
                     project_root=a.project_root, baseline=a.baseline)
    checked = dt.datetime.now().astimezone().isoformat(timespec="seconds")
    if a.json:
        print(json.dumps({"verdict": r.verdict, "checked_at": checked, **meta, "items": r.items},
                         ensure_ascii=False, indent=2))
    else:
        for i in r.items:
            print(f"[{i['status']}] {i['check']} {i['detail']}")
        print(f"回执 sha256={meta.get('receipt_sha256', '-')} 校验时刻 {checked}")
        print(f"VERDICT: {r.verdict}")
    sys.exit(0 if r.verdict == "PASS" else 1)


if __name__ == "__main__":
    main()
