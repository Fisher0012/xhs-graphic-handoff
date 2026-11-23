#!/bin/bash
# 用法: ./render.sh [p1 p2 ...]  默认渲染全部；1080x1440 CSS @2x => 2160x2880；同时生成宽400缩略图
cd "$(dirname "$0")"
pages=${@:-p1 p2 p3 p4}
for h in $pages; do
google-chrome --headless=new --no-sandbox --disable-gpu --allow-file-access-from-files --hide-scrollbars --force-device-scale-factor=2 --window-size=1080,1440 --virtual-time-budget=3000 --screenshot=$PWD/$h.png file://$PWD/$h.html 2>/dev/null
done
python3 -c "
from PIL import Image;import sys
for f in sys.argv[1:]:
  im=Image.open(f+'.png');print(f,im.size);im.resize((400,533),Image.LANCZOS).save('thumb_'+f+'.png')
" $pages
