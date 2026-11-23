# 复制自 /workspace/xhs/tools/measure_space.py，仅把 glob 改为参数指定的本期 PNG（不改共享原文件）；阈值：最大空白≤8%，内容底→页脚≤6%
import sys, glob
from PIL import Image
import numpy as np
files = sys.argv[1:]
bad = 0
for f in files:
    im=np.asarray(Image.open(f).convert('L').resize((540,720)),dtype=float)
    d=np.abs(im-np.median(im,axis=1,keepdims=True)).max(axis=1)
    row=d>40
    ys=np.where(row)[0]
    foot=[y for y in ys if y>720*0.85]; ftop=min(foot) if foot else 720
    body=[y for y in ys if y<ftop-4]
    b=[y for y in body if y>130]
    gaps=np.diff(b) if len(b)>1 else [0]
    mg=max(gaps); gi=int(np.argmax(gaps))
    g=mg/720*100; ft=(ftop-b[-1])/720*100; ok = g<=8 and ft<=6; bad += not ok
    print(f"{f.split('/')[-1]:<26} 最大空白{g:5.1f}% @y{b[gi]*2:>5}  内容底→页脚{ft:5.1f}%  {'PASS' if ok else 'FAIL'}")
print('measure_space:', 'PASS' if not bad else f'FAIL({bad})'); sys.exit(1 if bad else 0)
