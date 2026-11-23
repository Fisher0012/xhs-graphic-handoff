#!/usr/bin/env python3
"""本期 HTML 已按创始人离职已通过模板定稿，本脚本不再生成或覆盖 HTML/PNG。

封面基底：template-02/approved_cover_v8.html
内页1基底：pages/01_内页_v4.html
内页2、3基底：pages/02_内页_v5.html
只替换文字、数据和头像路径；CSS 除头像 url() 外不得改动。
请直接编辑 03-design/p1.html–p4.html，再用 render_heijin.sh 渲染。
"""
from pathlib import Path
import sys
OUT = Path(__file__).resolve().parent
needed = ["p1.html", "p2.html", "p3.html", "p4.html"]
missing = [n for n in needed if not (OUT / n).exists()]
if missing:
    print("MISSING", ", ".join(missing))
    sys.exit(1)
print("noop: keep existing", ", ".join(needed))
sys.exit(0)
