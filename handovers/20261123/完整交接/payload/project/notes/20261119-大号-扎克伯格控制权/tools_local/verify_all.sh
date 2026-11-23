#!/bin/bash
set -euo pipefail
P=/workspace/xhs/notes/20261119-大号-扎克伯格控制权
python3 "$P/tools_local/verify_numbers.py" | tee "$P/tools_local/verify_numbers_result.txt"
python3 "$P/tools_local/check_titles_local.py" | tee "$P/tools_local/check_titles_result.txt"
python3 "$P/tools_local/measure_space_local.py" "$P"/03-design/p{1,2,3,4}.png | tee "$P/tools_local/measure_space_result.txt"
python3 /workspace/xhs/tools/compliance_precheck.py --dir "$P" | tee "$P/tools_local/compliance_precheck_result.txt"
bash /workspace/xhs/tools/gate_archive.sh --auto "$P/final" | tee "$P/tools_local/gate_archive_result.txt"
python3 - << 'PY'
from pathlib import Path
import hashlib, sys
P=Path("/workspace/xhs/notes/20261119-大号-扎克伯格控制权")
pairs=[("p1.png","00_封面.png"),("p2.png","01_同样一股票数能差十倍.png"),("p3.png","02_这两个百分比是怎么来的.png"),("p4.png","03_掌权也有边界.png")]
bad=0
for a,b in pairs:
    ha=hashlib.sha256((P/"03-design"/a).read_bytes()).hexdigest()
    hb=hashlib.sha256((P/"final"/b).read_bytes()).hexdigest()
    ok=ha==hb
    print(f"{a} <-> {b}: {'MATCH' if ok else 'DIFF'} {hb}")
    bad += (not ok)
sys.exit(1 if bad else 0)
PY
