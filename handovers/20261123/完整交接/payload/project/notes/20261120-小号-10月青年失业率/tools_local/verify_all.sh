#!/usr/bin/env bash
# 本篇产物门+合规门（不改共享脚本）。失败非 0。
set -euo pipefail
NOTE="$(cd "$(dirname "$0")/.." && pwd)"
DESIGN="$NOTE/03-design"
FINAL="$NOTE/final"
fail=0

echo "== dimensions =="
python3 - << PY || fail=1
from pathlib import Path
from PIL import Image
final=Path("$FINAL")
need={
 "00_封面.png":(2160,2880),
 "01_近4个月怎么走.png":(2160,2880),
 "02_这个口径在统计什么.png":(2160,2880),
}
for name,size in need.items():
    p=final/name
    if not p.is_file():
        print("MISSING", p); raise SystemExit(1)
    im=Image.open(p)
    print(p.name, im.size, p.stat().st_size)
    if im.size!=size:
        print("BAD SIZE", p, im.size); raise SystemExit(1)
print("dimensions PASS")
PY

echo "== numbers in HTML =="
python3 - << PY || fail=1
from pathlib import Path
d=Path("$DESIGN")
t=(d/"p1.html").read_text()+(d/"p2.html").read_text()+(d/"p3.html").read_text()
need=["17.2","7.3","3.9","17.9","18.9","18.0","5.1","0.8个百分点","0.1个百分点","不含在校生"]
miss=[s for s in need if s not in t]
if miss:
    print("MISSING", miss); raise SystemExit(1)
# 百分点 vs 百分比混用粗查：走势页副题必须强调百分点
if "不是百分比涨跌" not in (d/"p2.html").read_text():
    print("P2 missing 百分点说明"); raise SystemExit(1)
print("numbers PASS")
PY

echo "== check.sh =="
out=$(bash "$DESIGN/check.sh")
echo "$out"
if echo "$out" | grep -E 'OVERLAP|MARGIN|SCROLL|ORPHAN|PUNCT-START' >/dev/null; then
  echo "check.sh FAIL"
  fail=1
else
  echo "check.sh PASS"
fi

echo "== compliance_precheck =="
set +e
python3 /workspace/xhs/tools/compliance_precheck.py --dir "$NOTE"
c=$?
set -e
if [[ $c -ne 0 ]]; then echo "compliance FAIL"; fail=1; else echo "compliance PASS"; fi

echo "== gate_archive =="
set +e
bash /workspace/xhs/tools/gate_archive.sh --auto "$FINAL"
g=$?
set -e
if [[ $g -ne 0 ]]; then echo "gate_archive FAIL"; fail=1; else echo "gate_archive PASS"; fi

if [[ $fail -ne 0 ]]; then echo "VERIFY FAIL"; exit 1; fi
echo "VERIFY PASS"
exit 0
