#!/bin/bash
set -euo pipefail
P=/workspace/xhs/notes/20261113-大号-汽车出口榜
bash /workspace/xhs/tools/once_pipeline.sh --note-dir "$P"
python3 "$P/tools_local/check_titles_local.py"
python3 "$P/tools_local/measure_space_local.py" "$P"/03-design/p*.png
python3 "$P/tools_local/check_layout_local.py"
python3 "$P/tools_local/verify_artifacts.py"
