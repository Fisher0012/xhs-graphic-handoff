#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""选题候选摘要：从选题库「待选」段生成当日候选，去重对照 notes / 选题库历史。

用法:
  python3 topic_candidates.py              # 默认读最新「每日选题」段，输出 stdout + tmp
  python3 topic_candidates.py --date 2026-11-06
  python3 topic_candidates.py --lib PATH --notes PATH --out PATH --min 3
  python3 topic_candidates.py --help

说明:
  - 只挑状态含「待选」的行；已选/已定稿/已否等跳过。
  - 去重：notes 目录名关键词、选题库中「已选/已定稿/已出稿」历史标题相似度。
  - 不改例程；不把候选数改成 1；供人工挑 ≥3 条。
"""
from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import sys
from pathlib import Path

ROOT = Path("/workspace/xhs")
DEFAULT_LIB = ROOT / "选题库.md"
DEFAULT_NOTES = ROOT / "notes"
DEFAULT_OUT = ROOT / "tmp" / "今日候选.md"

DONE_STATUS = re.compile(r"已选|已定稿|已出稿|已否|放弃|并入|升级为")
WAIT_STATUS = re.compile(r"待选")


def parse_args():
    p = argparse.ArgumentParser(description="从选题库待选段生成当日候选摘要（保留≥3 供 Fisher 挑）")
    p.add_argument("--lib", default=str(DEFAULT_LIB), help="选题库路径")
    p.add_argument("--notes", default=str(DEFAULT_NOTES), help="notes 目录")
    p.add_argument("--out", default=str(DEFAULT_OUT), help="输出 md 路径")
    p.add_argument("--date", default=None, help="指定日期 YYYY-MM-DD；默认取库中最新每日选题段")
    p.add_argument("--min", type=int, default=3, help="最少候选数提醒阈值（默认 3）")
    return p.parse_args()


def section_date(title: str):
    m = re.search(r"(\d{4}-\d{2}-\d{2})", title)
    return m.group(1) if m else None


def split_sections(text: str):
    parts = re.split(r"(?m)^## ", text)
    out = []
    for i, part in enumerate(parts):
        if i == 0:
            continue
        lines = part.splitlines()
        title = lines[0].strip()
        body = "\n".join(lines[1:])
        out.append((title, body))
    return out


def parse_table_rows(body: str):
    rows = []
    for line in body.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if not cells or cells[0] in {"#", "---"} or set(cells[0]) <= {"-"}:
            continue
        if cells[0].startswith("---") or all(re.fullmatch(r":?-+:?", c or "") for c in cells):
            continue
        # 标准每日选题：# | 账号 | 选题 | 分 | 状态 | 时间 | 备注
        if len(cells) >= 5 and (
            cells[1] in ("大号", "小号", "小号·统计", "小号·解读")
            or ("大号" in cells[1] or "小号" in cells[1])
        ):
            rows.append(
                {
                    "id": cells[0],
                    "account": cells[1],
                    "title": cells[2],
                    "score": cells[3] if len(cells) > 3 else "",
                    "status": cells[4] if len(cells) > 4 else "",
                    "when": cells[5] if len(cells) > 5 else "",
                    "note": cells[6] if len(cells) > 6 else "",
                }
            )
        # 排行榜替换表：# | 选题 | 分 | 状态
        elif len(cells) >= 4 and cells[0].isdigit():
            rows.append(
                {
                    "id": cells[0],
                    "account": "大号",
                    "title": cells[1],
                    "score": cells[2],
                    "status": cells[3],
                    "when": "",
                    "note": "",
                }
            )
    return rows


def normalize(s: str) -> str:
    s = re.sub(r"【.*?】", "", s)
    s = re.sub(r"[^\w\u4e00-\u9fff]+", "", s)
    return s.lower()


def bigrams(s: str):
    s = normalize(s)
    if len(s) < 2:
        return {s} if s else set()
    return {s[i : i + 2] for i in range(len(s) - 1)}


def similar(a: str, b: str) -> float:
    A, B = bigrams(a), bigrams(b)
    if not A or not B:
        return 0.0
    return len(A & B) / len(A | B)


def notes_titles(notes_dir: Path):
    names = []
    if not notes_dir.is_dir():
        return names
    for p in notes_dir.iterdir():
        if p.is_dir() and re.match(r"\d{8}", p.name):
            # 去掉日期与账号前缀
            t = re.sub(r"^\d{8}-?(大号-|小号-)?", "", p.name)
            names.append((p.name, t))
    return names


def history_done_titles(sections):
    done = []
    for title, body in sections:
        for r in parse_table_rows(body):
            st = r["status"]
            if DONE_STATUS.search(st) and not WAIT_STATUS.search(st):
                done.append(r["title"])
            elif re.search(r"已选|已定稿|已出稿", st):
                done.append(r["title"])
    return done


def pick_section(sections, date: str | None):
    daily = [
        (t, b)
        for t, b in sections
        if "每日选题" in t or "统计/排行榜选题" in t
    ]
    if date:
        for t, b in reversed(daily):
            if section_date(t) == date:
                return t, b
        return None, None
    # 最新带「每日选题」的段
    for t, b in reversed(daily):
        if "每日选题" in t:
            return t, b
    return (daily[-1] if daily else (None, None))


def main():
    args = parse_args()
    lib = Path(args.lib)
    notes = Path(args.notes)
    out = Path(args.out)
    if not lib.is_file():
        print(f"ERROR: 选题库不存在: {lib}", file=sys.stderr)
        return 2

    text = lib.read_text(encoding="utf-8")
    sections = split_sections(text)
    sec_title, body = pick_section(sections, args.date)
    if not body:
        print(f"ERROR: 未找到日期段 {args.date or '(最新)'}", file=sys.stderr)
        return 2

    note_list = notes_titles(notes)
    hist = history_done_titles(sections)
    today = section_date(sec_title) or args.date or dt.date.today().isoformat()

    candidates = []
    for r in parse_table_rows(body):
        if not WAIT_STATUS.search(r["status"]):
            continue
        flags = []
        for nd, nt in note_list:
            if similar(r["title"], nt) >= 0.45 or (nt and nt in r["title"]) or (nt and r["title"][:8] in nt):
                flags.append(f"notes近似:{nd}")
        for ht in hist:
            if similar(r["title"], ht) >= 0.55:
                flags.append("历史已做近似")
                break
        # 账号归一
        acct = "大号" if "大号" in r["account"] else ("小号" if "小号" in r["account"] else r["account"])
        candidates.append({**r, "account_n": acct, "flags": flags})

    big = [c for c in candidates if c["account_n"] == "大号"]
    small = [c for c in candidates if c["account_n"] == "小号"]

    lines = []
    lines.append(f"# 今日选题候选（{today}）")
    lines.append("")
    lines.append(f"- 来源段：## {sec_title}")
    lines.append(f"- 待选合计：{len(candidates)}（大号 {len(big)} / 小号 {len(small)}）")
    lines.append(f"- 硬规则：每天至少交 **{args.min}** 个候选给 Fisher 挑（不可改成 1 或全自动）")
    lines.append("")
    lines.append("## 大号待选")
    if not big:
        lines.append("（无）")
    for c in big:
        flag = (" ⚠️ " + "; ".join(c["flags"])) if c["flags"] else ""
        lines.append(f"- [{c['id']}] {c['title']}｜分:{c['score']}｜状态:{c['status']}｜建议:{c['when']}{flag}")
    lines.append("")
    lines.append("## 小号待选")
    if not small:
        lines.append("（无）")
    for c in small:
        flag = (" ⚠️ " + "; ".join(c["flags"])) if c["flags"] else ""
        lines.append(f"- [{c['id']}] {c['title']}｜分:{c['score']}｜状态:{c['status']}｜建议:{c['when']}{flag}")
    lines.append("")
    warn = ""
    if len(candidates) < args.min:
        warn = f"⚠️ 待选不足 {args.min} 条，需补选题后再交 Fisher。"
        lines.append(warn)
    else:
        lines.append(f"✅ 待选 ≥{args.min}，可交 Fisher 挑选（建议同时给大号+小号视角，总数仍 ≥{args.min}）。")
    lines.append("")
    lines.append("---")
    lines.append("生成：topic_candidates.py；去重仅标注，不自动删除。")

    md = "\n".join(lines) + "\n"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(md, encoding="utf-8")
    sys.stdout.write(md)
    if warn:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
