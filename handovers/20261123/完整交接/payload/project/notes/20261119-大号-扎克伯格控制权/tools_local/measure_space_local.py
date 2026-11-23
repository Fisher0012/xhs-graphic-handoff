#!/usr/bin/env python3
# 本期本地留白检查。v3 允许设计留白，不再把底部空带判失败。
# 阈值只用于拦截极端空洞或重叠，不能代替看图，也不能当作用户已接受。
# 最大空白≤28%，内容底→页脚≤28%（约 403px / 1440）。内页 2 删节标题和总结卡后下段留白约 27%，属有意留白。
import sys
from PIL import Image
import numpy as np
files = sys.argv[1:]
bad = 0
for f in files:
    im = np.asarray(Image.open(f).convert("L").resize((540, 720)), dtype=float)
    d = np.abs(im - np.median(im, axis=1, keepdims=True)).max(axis=1)
    row = d > 40
    ys = np.where(row)[0]
    foot = [y for y in ys if y > 720 * 0.85]
    ftop = min(foot) if foot else 720
    body = [y for y in ys if y < ftop - 4]
    b = [y for y in body if y > 130]
    gaps = np.diff(b) if len(b) > 1 else [0]
    mg = max(gaps) if len(gaps) else 0
    gi = int(np.argmax(gaps)) if len(gaps) else 0
    g = mg / 720 * 100
    ft = (ftop - b[-1]) / 720 * 100 if len(b) else 100
    ok = g <= 28 and ft <= 28
    bad += not ok
    yref = int(b[gi] * 2) if len(b) > 1 else 0
    print(f"{f.split('/')[-1]:<32} 最大空白{g:5.1f}% @y{yref:>5}  内容底→页脚{ft:5.1f}%  {'PASS' if ok else 'FAIL'}")
print("measure_space:", "PASS" if not bad else f"FAIL({bad})")
sys.exit(1 if bad else 0)
