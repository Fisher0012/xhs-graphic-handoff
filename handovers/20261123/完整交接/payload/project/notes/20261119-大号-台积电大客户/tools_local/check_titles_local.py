#!/usr/bin/env python3
"""电影感标题检查（不改共享 check_titles.py）。封面一行且约 108px、不溢出；内页一行且 64px。"""
import sys, importlib.util
spec = importlib.util.spec_from_file_location('ct', '/workspace/xhs/tools/check_titles.py')
ct = importlib.util.module_from_spec(spec); spec.loader.exec_module(ct)
D = sys.argv[1] if len(sys.argv) > 1 else '/workspace/xhs/notes/20261119-大号-台积电大客户/03-design'
bad = 0
expect = {1: '台积电有多靠大客户', 2: '三年里大客户在换位置', 3: '收入主要靠哪类平台', 4: '读年报别踩这些坑'}
for i in range(1, 5):
    h, s = ct.check(f'{D}/p{i}.html')
    fs = float(h['fs'][:-2])
    if i == 1:
        ok = h['lines'] == 1 and fs == 108 and h['right'] <= 1040 and h['text'] == expect[i]
        print(f"p{i} 封面 h1={h['text']} fs={h['fs']} lines={h['lines']} right={h['right']} -> {'PASS' if ok else 'FAIL'}")
    else:
        ok = h['lines'] == 1 and fs == 64 and h['right'] <= 1024 and h['text'] == expect[i] and s and s['lines'] == 1
        print(f"p{i} 内页 h1={h['text']} fs={h['fs']} lines={h['lines']} right={h['right']} sub_lines={s and s['lines']} -> {'PASS' if ok else 'FAIL'}")
    if s:
        print(f"    sub={s['text']} fs={s['fs']} color={s['color']}")
    bad += (not ok)
print('check_titles:', 'PASS' if not bad else f'FAIL({bad})'); sys.exit(1 if bad else 0)
