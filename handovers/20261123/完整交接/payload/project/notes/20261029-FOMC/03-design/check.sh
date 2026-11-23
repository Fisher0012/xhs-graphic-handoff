#!/bin/bash
cd "$(dirname "$0")"
for p in ${@:-p1 p2 p3 p4}; do sed 's#</body>#<script src="check.js"></script></body>#' $p.html > _chk_$p.html; echo "== $p"
google-chrome --headless=new --no-sandbox --disable-gpu --allow-file-access-from-files --window-size=1080,1440 --virtual-time-budget=4000 --dump-dom file://$PWD/_chk_$p.html 2>/dev/null | python3 -c "import sys,re,html;m=re.search(r'<pre id=\"RES\">(.*?)</pre>',sys.stdin.read(),re.S);print(html.unescape(m.group(1)) if m else 'NO RESULT')"
rm -f _chk_$p.html; done
