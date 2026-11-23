#!/usr/bin/env bash
# 总协调派活前拍基线（零额度，只读目标文件）。ADR-EG1，2026-11-10。
# 用法：baseline.sh [--root 项目根目录] [--task 任务ID] <项目> <路径...>
#   路径可以是文件或目录（目录递归；跳过 .git、node_modules、__pycache__、.venv、符号链接）。
#   路径不存在 → 记 ABSENT（表示本次允许新增）。
#   密钥类（/home/box/secrets、/workspace/foundation/keys、.env*、*.pem、*.key、cookie、*_token）不读，只记一行 # skipped。
# 输出：/workspace/ops/eng_gate/baselines/<项目>/<任务ID或时间>_<时间>.sha256，并打印该路径。
# 校验：python3 verify_receipt.py <receipt.json> --baseline <该文件> [--project-root 根目录]
set -eu
ROOT=""; TASK=""
while [ "$#" -gt 0 ]; do
  case "$1" in
    --root) ROOT=${2:?--root 需要目录}; shift 2;;
    --task) TASK=${2:?--task 需要任务ID}; shift 2;;
    --) shift; break;;
    -*) echo "未知选项 $1" >&2; exit 2;;
    *) break;;
  esac
done
[ "$#" -ge 2 ] || { echo "用法：baseline.sh [--root 目录] [--task 任务ID] <项目> <路径...>" >&2; exit 2; }
PROJ=$1; shift
case "$PROJ" in */*|.*|"") echo "项目名非法：$PROJ" >&2; exit 2;; esac
case "$TASK" in */*|.*) echo "任务ID非法：$TASK" >&2; exit 2;; esac
OUTDIR=${BASELINE_DIR:-/workspace/ops/eng_gate/baselines}
exec python3 - "$OUTDIR" "$PROJ" "$ROOT" "$TASK" "$@" <<'PY'
import datetime as dt, hashlib, os, re, sys, tempfile
outdir, proj, root, task, *paths = sys.argv[1:]
DENY_PREFIXES = ("/home/box/secrets", "/workspace/foundation/keys")
DENY_NAMES = re.compile(r"^(\.env(\..*)?|.*\.pem|.*\.key|id_rsa.*|.*cookies?(\.txt|\.json)?|.*_token|tokens?\.(txt|json))$", re.I)
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv"}
def denied(p):
    rp = os.path.realpath(p)
    return any(rp == d or rp.startswith(d + "/") for d in DENY_PREFIXES) or bool(DENY_NAMES.match(os.path.basename(rp)))
def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()
entries, skipped = {}, []
for raw in paths:
    p = os.path.abspath(raw if os.path.isabs(raw) or not root else os.path.join(root, raw))
    if denied(p):
        skipped.append(p); continue
    if os.path.islink(p):
        skipped.append(p + "（符号链接）"); continue
    if os.path.isfile(p):
        entries[p] = sha(p)
    elif os.path.isdir(p):
        for base, dirs, files in os.walk(p, followlinks=False):
            dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS and not denied(os.path.join(base, d)))
            for f in sorted(files):
                fp = os.path.join(base, f)
                if os.path.islink(fp) or denied(fp):
                    skipped.append(fp); continue
                if os.path.isfile(fp):
                    entries[fp] = sha(fp)
    elif not os.path.lexists(p):
        entries[p] = "ABSENT"
    else:
        skipped.append(p + "（非普通文件）")
if not entries:
    sys.exit("基线为空：没有可登记的文件")
if not root:
    root = os.path.commonpath([os.path.dirname(x) if not os.path.isdir(x) else x for x in entries])
root = os.path.abspath(root)
out_of_root = [x for x in entries if not (x == root or x.startswith(root.rstrip("/") + "/"))]
if out_of_root:
    sys.exit(f"有路径不在 --root {root} 之内：{out_of_root[:3]}")
now = dt.datetime.now().astimezone()
d = os.path.join(outdir, proj)
os.makedirs(d, exist_ok=True)
name = f"{task + '_' if task else ''}{now:%Y%m%d-%H%M%S}.sha256"
target = os.path.join(d, name)
if os.path.exists(target):
    sys.exit(f"基线已存在，不覆盖：{target}")
lines = ["# format: eng_gate-baseline-v1", f"# project: {proj}", f"# task: {task or '-'}",
         f"# root: {root}", f"# created_at: {now.isoformat(timespec='seconds')}",
         f"# created_by: {os.environ.get('FROM', '总协调')}", f"# files: {len(entries)}"]
lines += [f"# skipped: {s}" for s in skipped]
lines += [f"{h}  {p}" for p, h in sorted(entries.items())]
fd, tmp = tempfile.mkstemp(prefix=".tmp.", dir=d)
with os.fdopen(fd, "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")
os.chmod(tmp, 0o444)
os.replace(tmp, target)
print(target)
print(f"已登记 {len(entries)} 个文件（ABSENT {sum(v == 'ABSENT' for v in entries.values())} 个），跳过 {len(skipped)} 个", file=sys.stderr)
PY
