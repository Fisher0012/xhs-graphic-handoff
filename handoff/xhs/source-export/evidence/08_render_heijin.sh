#!/usr/bin/env bash
# 黑金 HTML 一键渲染：对指定 notes 期目录内 03-design/*.html → PNG（复用 headless Chrome）
#
# 用法:
#   ./render_heijin.sh /workspace/xhs/notes/20261031-世界500强营收前十
#   ./render_heijin.sh NOTES_DIR [p1 p2 ...]     # 只渲指定页
#   ./render_heijin.sh --help
#
# 行为:
#   - 目录不存在 / 无 03-design / 无 html → 清晰报错，非 0 退出
#   - 默认渲染 03-design 下全部 p*.html；可选传页名
#   - 参数与既有 render.sh 一致：1080x1440 @2x
set -euo pipefail

usage() {
  sed -n '2,12p' "$0" | sed 's/^# \?//'
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

if [[ $# -lt 1 ]]; then
  echo "ERROR: 缺少 notes 期目录参数" >&2
  usage >&2
  exit 2
fi

NOTES_DIR="$1"
shift || true

if [[ ! -d "$NOTES_DIR" ]]; then
  echo "ERROR: 目录不存在: $NOTES_DIR" >&2
  exit 2
fi

DESIGN="$NOTES_DIR/03-design"
if [[ ! -d "$DESIGN" ]]; then
  # 兼容：若直接指向 03-design
  if [[ "$(basename "$NOTES_DIR")" == "03-design" ]]; then
    DESIGN="$NOTES_DIR"
  else
    echo "ERROR: 未找到 03-design: $DESIGN" >&2
    exit 2
  fi
fi

if ! command -v google-chrome >/dev/null 2>&1; then
  echo "ERROR: 未找到 google-chrome" >&2
  exit 2
fi

shopt -s nullglob
if [[ $# -gt 0 ]]; then
  pages=("$@")
else
  pages=()
  for f in "$DESIGN"/p*.html; do
    pages+=("$(basename "$f" .html)")
  done
fi

if [[ ${#pages[@]} -eq 0 ]]; then
  echo "ERROR: $DESIGN 下无 p*.html 可渲染" >&2
  exit 2
fi

ok=0
fail=0
for h in "${pages[@]}"; do
  html="$DESIGN/$h.html"
  png="$DESIGN/$h.png"
  if [[ ! -f "$html" ]]; then
    echo "ERROR: 缺 HTML: $html" >&2
    fail=$((fail + 1))
    continue
  fi
  if google-chrome --headless=new --no-sandbox --disable-gpu \
      --allow-file-access-from-files --hide-scrollbars \
      --force-device-scale-factor=2 --window-size=1080,1440 \
      --virtual-time-budget=3000 \
      --screenshot="$png" "file://$html" >/tmp/render_heijin_chrome.log 2>&1; then
    if [[ -f "$png" ]]; then
      echo "OK  $h -> $png ($(stat -c%s "$png") bytes)"
      ok=$((ok + 1))
    else
      echo "FAIL $h: chrome 退出但未生成 png" >&2
      fail=$((fail + 1))
    fi
  else
    echo "FAIL $h: chrome 渲染失败（见 /tmp/render_heijin_chrome.log）" >&2
    fail=$((fail + 1))
  fi
done

echo "合计: ok=$ok fail=$fail design=$DESIGN"
if [[ $fail -gt 0 || $ok -eq 0 ]]; then
  exit 1
fi
exit 0
