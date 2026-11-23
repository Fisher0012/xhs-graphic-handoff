#!/usr/bin/env bash
set -euo pipefail
D="$(cd "$(dirname "$0")/.." && pwd)"
python3 "$D/tools_local/check_titles_local.py" "$D/03-design"
python3 "$D/tools_local/measure_space_local.py" "$D"/03-design/p{1,2,3,4,5}.png
python3 "$D/tools_local/check_layout.py"
python3 /workspace/xhs/tools/compliance_precheck.py --dir "$D"
bash /workspace/xhs/tools/gate_archive.sh --auto "$D/final"
python3 "$D/tools_local/verify_content.py"
