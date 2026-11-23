#!/usr/bin/env bash
# 定稿夹缺件门禁：缺件非 0 退出
#
# 用法:
#   ./gate_archive.sh --dahao DIR     # 大号：00_封面、01–N 配图、04_发布文案.txt、05_来源说明.txt、06_归档校验.json
#   ./gate_archive.sh --xiaohao DIR   # 小号 YYYY-MM-DD_标题：00_封面、≥1 配图、文案.md、数据.json
#   ./gate_archive.sh --auto DIR      # 按目录名/内容自动判断
#   ./gate_archive.sh --help
#
# 兼容: 若存在较多内页导致文案编号后移（05_发布文案 / 06_来源 / 07_归档），亦视为通过（打印提示）。
set -euo pipefail

usage() { sed -n '2,10p' "$0" | sed 's/^# \?//'; }

mode=""
dir=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help) usage; exit 0 ;;
    --dahao) mode=dahao; dir="${2:-}"; shift 2 || true ;;
    --xiaohao) mode=xiaohao; dir="${2:-}"; shift 2 || true ;;
    --auto) mode=auto; dir="${2:-}"; shift 2 || true ;;
    *) if [[ -z "$dir" ]]; then dir="$1"; shift; else echo "ERROR: 多余参数 $1" >&2; exit 2; fi ;;
  esac
done

if [[ -z "$dir" ]]; then
  echo "ERROR: 缺少目录" >&2
  usage >&2
  exit 2
fi
if [[ ! -d "$dir" ]]; then
  echo "ERROR: 目录不存在: $dir" >&2
  exit 2
fi

# 自动：含 04_发布文案 或 05_发布文案 → 大号；含 文案.md+数据.json → 小号
if [[ "$mode" == "auto" || -z "$mode" ]]; then
  if [[ -f "$dir/文案.md" || -f "$dir/数据.json" ]]; then
    mode=xiaohao
  else
    mode=dahao
  fi
fi

missing=()
warn=()

has_cover() {
  compgen -G "$dir/00_封面*" >/dev/null
}

count_inner() {
  # 01_ 起的配图（png/jpg）
  local n=0
  local f
  for f in "$dir"/0[1-9]_*.png "$dir"/0[1-9]_*.jpg "$dir"/[1-9][0-9]_*.png; do
    [[ -e "$f" ]] || continue
    n=$((n + 1))
  done
  echo "$n"
}

if [[ "$mode" == "dahao" ]]; then
  echo "## 大号定稿门禁: $dir"
  has_cover || missing+=("00_封面(.png/.jpg)")
  inn=$(count_inner)
  if [[ "$inn" -lt 1 ]]; then
    missing+=("01–N 配图(至少1张)")
  fi
  # 标准三件套 or 后移编号
  if [[ -f "$dir/04_发布文案.txt" && -f "$dir/05_来源说明.txt" && -f "$dir/06_归档校验.json" ]]; then
    :
  elif [[ -f "$dir/05_发布文案.txt" && -f "$dir/06_来源说明.txt" && -f "$dir/07_归档校验.json" ]]; then
    warn+=("文案/来源/校验编号为 05/06/07（内页占满 01–04），已兼容通过")
  else
    [[ -f "$dir/04_发布文案.txt" || -f "$dir/05_发布文案.txt" ]] || missing+=("04_发布文案.txt(或05_发布文案.txt)")
    [[ -f "$dir/05_来源说明.txt" || -f "$dir/06_来源说明.txt" ]] || missing+=("05_来源说明.txt(或06_来源说明.txt)")
    [[ -f "$dir/06_归档校验.json" || -f "$dir/07_归档校验.json" ]] || missing+=("06_归档校验.json(或07_归档校验.json)")
  fi
  echo "- 配图张数(含01起): $inn"
elif [[ "$mode" == "xiaohao" ]]; then
  echo "## 小号定稿门禁: $dir"
  base=$(basename "$dir")
  if [[ ! "$base" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}_ ]]; then
    warn+=("目录名建议 YYYY-MM-DD_标题，当前: $base")
  fi
  has_cover || missing+=("00_封面(.png/.jpg)")
  inn=$(count_inner)
  if [[ "$inn" -lt 1 ]]; then
    missing+=("配图(01_*.png 等至少1张)")
  fi
  [[ -f "$dir/文案.md" ]] || missing+=("文案.md")
  [[ -f "$dir/数据.json" ]] || missing+=("数据.json")
  echo "- 配图张数(含01起): $inn"
else
  echo "ERROR: 未知 mode=$mode" >&2
  exit 2
fi

for w in "${warn[@]:-}"; do
  [[ -n "$w" ]] && echo "WARN: $w"
done

if [[ ${#missing[@]} -gt 0 ]]; then
  echo "缺件:"
  for m in "${missing[@]}"; do
    echo "  - $m"
  done
  echo "结论: FAIL (缺 ${#missing[@]} 项)"
  exit 1
fi

echo "结论: PASS"
exit 0
