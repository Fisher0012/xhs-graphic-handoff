#!/bin/bash
set -euo pipefail
P=/workspace/xhs/notes/20261119-大号-台积电大客户
python3 "$P/tools_local/verify_numbers.py" | tee "$P/tools_local/verify_numbers_result.txt"
python3 "$P/tools_local/check_titles_local.py" | tee "$P/tools_local/check_titles_result.txt"
python3 "$P/tools_local/measure_space_local.py" "$P"/03-design/p{1,2,3,4}.png | tee "$P/tools_local/measure_space_result.txt"
python3 /workspace/xhs/tools/compliance_precheck.py --dir "$P" | tee "$P/tools_local/compliance_precheck_result.txt"
bash /workspace/xhs/tools/gate_archive.sh --auto "$P/final" | tee "$P/tools_local/gate_archive_result.txt"
python3 - << 'PY'
from pathlib import Path
import hashlib, sys
P=Path("/workspace/xhs/notes/20261119-大号-台积电大客户")
pairs=[("p1.png","00_封面.png"),("p2.png","01_三年里大客户在换位置.png"),("p3.png","02_收入主要靠哪类平台.png"),("p4.png","03_读年报别踩这些坑.png")]
bad=0
for a,b in pairs:
    ha=hashlib.sha256((P/"03-design"/a).read_bytes()).hexdigest()
    hb=hashlib.sha256((P/"final"/b).read_bytes()).hexdigest()
    ok=ha==hb
    print(f"{a} <-> {b}: {'MATCH' if ok else 'DIFF'} {hb}")
    bad += (not ok)
sys.exit(1 if bad else 0)
PY
