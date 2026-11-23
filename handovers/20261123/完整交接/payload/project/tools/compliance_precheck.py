#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""合规初筛：对文案/框架文本扫禁区关键词，输出通过/问题列表。

用法:
  python3 compliance_precheck.py FILE [FILE ...]
  python3 compliance_precheck.py --dir NOTES_DIR
  python3 compliance_precheck.py --text "保证收益稳赚"
  python3 compliance_precheck.py --help

注意:
  - 仅初筛，不做最终合规替代；送审前仍须跑 skill-1792678316447 / 审查官。
  - 命中任一条 → 退出码 1；全过 → 0；用法错 → 2。
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# (规则 id, 说明, 正则)
RULES = [
    ("保证收益", "承诺/暗示保证收益", re.compile(r"保证收益|保本保息|稳赚不赔|必赚|稳稳赚钱")),
    ("稳赚", "稳赚类话术", re.compile(r"稳赚|躺赚|轻松发财|一夜暴富")),
    ("荐股", "荐股/跟买暗示", re.compile(r"荐股|推荐买入|建议买入|赶紧买|抄底买|跟我买|必涨")),
    ("产品代码荐买", "具体产品代码+荐买", re.compile(r"(?:股票代码|基金代码)?[（(]?\d{6}[)）]?.{0,12}(?:买入|建仓|加仓|推荐)|买[入进]\s*\d{6}")),
    ("承诺收益数字", "承诺具体收益率", re.compile(r"(?:保证|承诺|稳获|坐享).{0,8}\d+(?:\.\d+)?\s*%")),
    ("投资建议口吻", "构成投资建议口吻（初筛）", re.compile(r"本(?:文|条)?(?:构成|属于)投资建议|当作(?:买卖|投资)依据")),
]


def parse_args():
    p = argparse.ArgumentParser(description="财经图文合规初筛（禁区关键词）")
    p.add_argument("files", nargs="*", help="待检文本文件")
    p.add_argument("--dir", help="notes 期目录：扫描其中 *.md/*.txt/文案*")
    p.add_argument("--text", help="直接检查一段字符串")
    return p.parse_args()


def collect_from_dir(d: Path):
    files = []
    if not d.is_dir():
        raise FileNotFoundError(str(d))
    patterns = ["*.md", "*.txt", "文案.md", "04_发布文案.txt", "05_发布文案.txt"]
    seen = set()
    for pat in ("**/*.md", "**/*.txt"):
        for f in d.glob(pat):
            if f.is_file() and f.resolve() not in seen:
                # 跳过巨大二进制误匹配
                if f.suffix.lower() in {".md", ".txt"}:
                    seen.add(f.resolve())
                    files.append(f)
    return files


def scan_text(label: str, text: str):
    hits = []
    for rid, desc, rx in RULES:
        for m in rx.finditer(text):
            start = max(0, m.start() - 12)
            end = min(len(text), m.end() + 12)
            snippet = text[start:end].replace("\n", " ")
            hits.append({"file": label, "rule": rid, "desc": desc, "match": m.group(0), "snippet": snippet})
    return hits


def main():
    args = parse_args()
    targets = []  # (label, text)

    if args.text is not None:
        targets.append(("<--text>", args.text))
    if args.dir:
        d = Path(args.dir)
        try:
            for f in collect_from_dir(d):
                targets.append((str(f), f.read_text(encoding="utf-8", errors="replace")))
        except FileNotFoundError:
            print(f"ERROR: 目录不存在: {d}", file=sys.stderr)
            return 2
    for fp in args.files:
        p = Path(fp)
        if not p.is_file():
            print(f"ERROR: 文件不存在: {p}", file=sys.stderr)
            return 2
        targets.append((str(p), p.read_text(encoding="utf-8", errors="replace")))

    if not targets:
        print("ERROR: 请提供 FILE / --dir / --text", file=sys.stderr)
        return 2

    all_hits = []
    for label, text in targets:
        all_hits.extend(scan_text(label, text))

    print("## 合规初筛结果")
    print(f"- 检查对象数: {len(targets)}")
    print(f"- 命中数: {len(all_hits)}")
    if not all_hits:
        print("- 结论: PASS（初筛通过；仍须最终合规/审查官）")
        return 0
    print("- 结论: FAIL（仅初筛，请人工复核后改稿）")
    print("")
    for i, h in enumerate(all_hits, 1):
        print(f"{i}. [{h['rule']}] {h['desc']}")
        print(f"   文件: {h['file']}")
        print(f"   命中: {h['match']}")
        print(f"   上下文: …{h['snippet']}…")
    return 1


if __name__ == "__main__":
    sys.exit(main())
