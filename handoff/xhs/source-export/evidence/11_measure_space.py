# 量内页内容区：最大连续空白（占画布高%）、内容底到页脚距离
import sys,glob
from PIL import Image
import numpy as np
for f in sorted(glob.glob('2026103*/03-design/final/0[1-4]_*.png')):
    im=np.asarray(Image.open(f).convert('L').resize((540,720)),dtype=float)
    # 背景是渐变暗色：用行内与行中位数差的最大值判断有无内容
    d=np.abs(im-np.median(im,axis=1,keepdims=True)).max(axis=1)
    row=d>40
    # 页脚：最后有内容的一段（底部 15% 内）
    ys=np.where(row)[0]
    foot=[y for y in ys if y>720*0.85]; ftop=min(foot) if foot else 720
    body=[y for y in ys if y<ftop-4]
    # 内容区从标题下开始 (y>140 ≈ 1440坐标280)
    b=[y for y in body if y>130]
    gaps=np.diff(b) if len(b)>1 else [0]
    mg=max(gaps); gi=int(np.argmax(gaps))
    print(f"{f.split('/')[0][9:]:<12}{f.split('/')[-1]:<22} 最大空白{mg/720*100:5.1f}% @y{b[gi]*2:>5}  内容底→页脚{(ftop-b[-1])/720*100:5.1f}%")
