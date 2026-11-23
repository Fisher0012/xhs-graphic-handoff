#!/bin/bash
# 实测每张内页 内容底部→风险提示页脚 的像素间距（DOM），要求 ≥40
cd /workspace/xhs/notes
for d in 20261031-*/03-design; do for i in 3 4 5 6; do
g=$(google-chrome --headless=new --no-sandbox --user-data-dir=/tmp/fg_profile --disable-gpu --allow-file-access-from-files --window-size=1080,1440 --virtual-time-budget=3000 --dump-dom file://$PWD/$d/p$i.html 2>/dev/null | grep -o 'data-gap="[-0-9]*"' | head -1)
echo "${d%%/*} 0$((i-2)) $g"; done; done
rm -rf /tmp/fg_profile
