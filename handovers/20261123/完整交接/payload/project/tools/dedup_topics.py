#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""简单选题去重：标题 bigram 相似度 + notes 已做过标记。

用法:
  python3 dedup_topics.py "标题A" "标题B"
  python3 dedup_topics.py --check "候选标题" --notes /workspace/xhs/notes
  python3 dedup_topics.py --help
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


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


def parse_args():
    p = argparse.ArgumentParser(description="选题标题相似度 / 已做过标记")
    p.add_argument("titles", nargs="*", help="两两比较的标题")
    p.add_argument("--check", help="对单条标题对照 notes 目录名")
    p.add_argument("--notes", default="/workspace/xhs/notes")
    p.add_argument("--threshold", type=float, default=0.45)
    return p.parse_args()


def main():
    args = parse_args()
    if args.check:
        notes = Path(args.notes)
        hits = []
        if notes.is_dir():
            for p in notes.iterdir():
                if not p.is_dir():
                    continue
                t = re.sub(r"^\d{8}-?(大号-|小号-)?", "", p.name)
                sc = similar(args.check, t)
                if sc >= args.threshold or (t and t in args.check):
                    hits.append((sc, p.name))
        hits.sort(reverse=True)
        print(f"## 去重检查: {args.check}")
        if not hits:
            print("结论: 未见明显重复")
            return 0
        print("可能重复:")
        for sc, name in hits[:10]:
            print(f"  - {sc:.2f}  {name}")
        return 1

    if len(args.titles) < 2:
        print("ERROR: 需要至少两个标题，或使用 --check", file=sys.stderr)
        return 2
    print("## 标题两两相似度")
    for i in range(len(args.titles)):
        for j in range(i + 1, len(args.titles)):
            sc = similar(args.titles[i], args.titles[j])
            mark = "重复?" if sc >= args.threshold else "ok"
            print(f"[{mark}] {sc:.2f} | {args.titles[i][:40]} || {args.titles[j][:40]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
