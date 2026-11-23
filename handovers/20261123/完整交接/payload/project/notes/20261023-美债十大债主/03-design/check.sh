#!/bin/bash
# 自动检查：文字是否越出版心(64px)/画布、元素重叠、横向溢出；打印进度条占比与封面标题宽度占比
cd "$(dirname "$0")"
for p in ${@:-p1 p2 p3 p4}; do sed 's#</body>#<script src="check.js"></script></body>#' $p.html > _chk_$p.html; echo "== $p"
google-chrome --headless=new --no-sandbox --disable-gpu --allow-file-access-from-files --window-size=1080,1440 --virtual-time-budget=4000 --dump-dom file://$PWD/_chk_$p.html 2>/dev/null | python3 -c "import sys,re;m=re.search(r'<pre id=\"RES\">(.*?)</pre>',sys.stdin.read(),re.S);print((m.group(1) if m else 'NO RESULT') or '（无问题）')"
rm -f _chk_$p.html; done
