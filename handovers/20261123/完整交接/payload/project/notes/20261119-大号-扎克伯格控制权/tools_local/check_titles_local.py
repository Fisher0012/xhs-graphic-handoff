#!/usr/bin/env python3
"""封面 108px，允许 check_titles 把双 block-span 计成 lines=4；内页 86px 一行，副题用 h2 不是 .sub。"""
import json, os, re, subprocess, sys, importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location("ct", "/workspace/xhs/tools/check_titles.py")
ct = importlib.util.module_from_spec(spec); spec.loader.exec_module(ct)

D = Path(sys.argv[1] if len(sys.argv) > 1 else "/workspace/xhs/notes/20261119-大号-扎克伯格控制权/03-design")
bad = 0
expect = {
    1: "扎克伯格为啥能掌权",
    2: "同样一股，票数差十倍",
    3: "两个比例怎么来的",
    4: "掌权也有边界",
}

def measure_h2(html):
    js = """<script>window.addEventListener('load',()=>{document.fonts.ready.then(()=>{
const e=document.querySelector('h2');
if(!e){const d=document.createElement('pre');d.id='H2';d.textContent='null';document.body.appendChild(d);return;}
const cs=getComputedStyle(e); const r=e.getBoundingClientRect();
const d=document.createElement('pre');d.id='H2';
d.textContent=JSON.stringify({fs:cs.fontSize,lines:e.innerText.split('\\n').length,text:e.innerText,right:Math.round(r.right),top:Math.round(r.top)});
document.body.appendChild(d);
})})</script>"""
    src = Path(html).read_text(encoding="utf-8").replace("</body>", js + "</body>")
    t = str(html) + ".h2.html"
    Path(t).write_text(src, encoding="utf-8")
    out = subprocess.run(
        ["google-chrome", "--headless=new", "--no-sandbox", "--disable-gpu",
         "--allow-file-access-from-files", "--window-size=1080,1440",
         "--virtual-time-budget=4000", "--dump-dom", "file://" + t],
        capture_output=True, text=True,
    ).stdout
    os.remove(t)
    m = re.search(r'<pre id="H2">(.*?)</pre>', out, re.S)
    return None if (not m or m.group(1) == "null") else json.loads(m.group(1).replace("&amp;", "&"))

for i in range(1, 5):
    html = D / f"p{i}.html"
    r = ct.check(str(html))
    h = r[0]
    fs = float(h["fs"][:-2])
    visual = h["text"]
    compact = visual.replace("⏎", "")
    h2 = measure_h2(html)
    if i == 1:
        ok = (
            compact == expect[i]
            and fs == 108
            and (("⏎" in visual and h["lines"] in (2, 4)) or ("⏎" not in visual and h["lines"] == 1))
            and h["right"] <= 1040
            and h["top"] == 72
            and h2 and h2["fs"] == "34px" and h2["lines"] == 1 and h2["right"] <= 1040
        )
        print(f"p{i} 封面 h1={visual!r} fs={h['fs']} lines={h['lines']} top={h['top']} right={h['right']} h2fs={h2 and h2['fs']} h2lines={h2 and h2['lines']} -> {'PASS' if ok else 'FAIL'}")
    else:
        ok = (
            compact == expect[i]
            and fs == 86
            and h["lines"] == 1
            and h["right"] <= 1040
            and h["top"] == 74
            and h2 and h2["fs"] == "32px" and h2["lines"] == 1 and h2["right"] <= 1040
        )
        print(f"p{i} 内页 h1={visual!r} fs={h['fs']} lines={h['lines']} top={h['top']} right={h['right']} h2={h2 and h2['text']!r} h2fs={h2 and h2['fs']} -> {'PASS' if ok else 'FAIL'}")
    if h2:
        print(f"    h2={h2['text']} fs={h2['fs']} top={h2['top']} right={h2['right']}")
    bad += (not ok)

print("check_titles:", "PASS" if not bad else f"FAIL({bad})")
sys.exit(1 if bad else 0)
