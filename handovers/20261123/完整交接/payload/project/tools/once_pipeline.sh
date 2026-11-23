#!/usr/bin/env bash
# once_pipeline.sh — 选定选题后「一次成稿」总编排（最小可运行版）
#
# 用法:
#   ./once_pipeline.sh --note-dir <notes期目录> [--skip-render]
#   ./once_pipeline.sh /workspace/xhs/notes/20261102-大号-产油国 --skip-render
#   ./once_pipeline.sh --help
#
# 流水线顺序:
#   1) 检查目录存在，且有 data.json 或 框架.md
#      （都没有 → 建最小骨架 README/框架占位，exit 非0，说明需先核数据，不编数）
#   2) 若有可渲染 HTML（03-design/p*.html），调用 render_heijin.sh；
#      无 HTML 或 --skip-render → 跳过渲染并记 WARN
#   3) compliance_precheck.py --dir 该目录
#   4) 若存在 final/ 或定稿/archive 结构 → gate_archive.sh --auto；
#      否则对 notes 输出物做宽松检查，并说明定稿门禁在存档阶段跑
#   5) 汇总 PASS/FAIL 写入该目录 pipeline_log.md；任一硬失败 → exit 1
#
# 退出码: 0=PASS；1=FAIL；2=用法/目录错误
set -euo pipefail

TOOLS_DIR="$(cd "$(dirname "$0")" && pwd)"
SKIP_RENDER=0
NOTE_DIR=""

usage() {
  sed -n '2,20p' "$0" | sed 's/^# \?//'
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help) usage; exit 0 ;;
    --note-dir)
      NOTE_DIR="${2:-}"
      if [[ -z "$NOTE_DIR" ]]; then
        echo "ERROR: --note-dir 需要路径" >&2
        exit 2
      fi
      shift 2
      ;;
    --skip-render) SKIP_RENDER=1; shift ;;
    --*)
      echo "ERROR: 未知参数 $1" >&2
      usage >&2
      exit 2
      ;;
    *)
      if [[ -z "$NOTE_DIR" ]]; then
        NOTE_DIR="$1"
        shift
      else
        echo "ERROR: 多余参数 $1" >&2
        exit 2
      fi
      ;;
  esac
done

if [[ -z "$NOTE_DIR" ]]; then
  echo "ERROR: 缺少 --note-dir / 期目录" >&2
  usage >&2
  exit 2
fi

# 规范化为绝对路径（假路径也保留原样便于报错）
if [[ -d "$NOTE_DIR" ]]; then
  NOTE_DIR="$(cd "$NOTE_DIR" && pwd)"
fi

TS="$(date '+%Y-%m-%d %H:%M:%S %Z')"
LOG_LINES=()
HARD_FAIL=0
WARN_N=0

log() {
  local line="$1"
  LOG_LINES+=("$line")
  echo "$line"
}

mark_fail() {
  HARD_FAIL=1
  log "FAIL: $1"
}

mark_warn() {
  WARN_N=$((WARN_N + 1))
  log "WARN: $1"
}

mark_ok() {
  log "OK: $1"
}

write_log() {
  local conclusion="$1"
  local out="$NOTE_DIR/pipeline_log.md"
  # 目录不存在时写到 /tmp，避免 set -e 在假路径上炸
  if [[ ! -d "$NOTE_DIR" ]]; then
    out="/tmp/once_pipeline_fake_$$.md"
  fi
  {
    echo "# once_pipeline 日志"
    echo "- 时间: $TS"
    echo "- 目录: $NOTE_DIR"
    echo "- skip_render: $SKIP_RENDER"
    echo "- 结论: $conclusion"
    echo
    echo "## 步骤"
    for line in "${LOG_LINES[@]}"; do
      echo "- $line"
    done
  } >"$out"
  echo "日志: $out"
}

# ---------- 1) 目录与数据骨架 ----------
if [[ ! -d "$NOTE_DIR" ]]; then
  mark_fail "目录不存在: $NOTE_DIR"
  write_log "FAIL"
  exit 2
fi
mark_ok "目录存在: $NOTE_DIR"

has_data=0
[[ -f "$NOTE_DIR/data.json" || -f "$NOTE_DIR/数据.json" ]] && has_data=1
has_frame=0
[[ -f "$NOTE_DIR/框架.md" ]] && has_frame=1

if [[ $has_data -eq 0 && $has_frame -eq 0 ]]; then
  # 建最小骨架占位，不编数
  mkdir -p "$NOTE_DIR"
  if [[ ! -f "$NOTE_DIR/README.md" ]]; then
    cat >"$NOTE_DIR/README.md" <<'RD'
# notes 期目录骨架（once_pipeline 自动创建）

本目录尚无 `data.json` / `数据.json` / `框架.md`。
**禁止编造数据。** 请先核官方来源，写入 data.json 与 框架.md 后再跑 once_pipeline。
RD
  fi
  if [[ ! -f "$NOTE_DIR/框架.md" ]]; then
    cat >"$NOTE_DIR/框架.md" <<'FR'
# 框架（占位）

- 状态：待核数据
- 说明：once_pipeline 检测到无数据/框架，已建占位。请先完成选题核数与框架，再重新跑流水线。
- **不编数、不荐产品、不承诺收益。**
FR
  fi
  mark_fail "无 data.json/数据.json/框架.md；已建 README+框架占位，需先核数据后再跑（不编数）"
  write_log "FAIL"
  exit 1
fi
[[ $has_data -eq 1 ]] && mark_ok "发现数据文件 (data.json/数据.json)"
[[ $has_frame -eq 1 ]] && mark_ok "发现 框架.md"
[[ $has_data -eq 0 ]] && mark_warn "尚无 data.json/数据.json（仅有框架，定稿前须补齐数据）"
[[ $has_frame -eq 0 ]] && mark_warn "尚无 框架.md（仅有数据）"

# ---------- 2) 渲染 ----------
DESIGN="$NOTE_DIR/03-design"
html_count=0
if [[ -d "$DESIGN" ]]; then
  shopt -s nullglob
  htmls=("$DESIGN"/p*.html)
  shopt -u nullglob
  html_count=${#htmls[@]}
fi

if [[ $SKIP_RENDER -eq 1 ]]; then
  mark_warn "跳过渲染 (--skip-render)"
elif [[ $html_count -eq 0 ]]; then
  mark_warn "无 03-design/p*.html，跳过渲染（需先有 HTML 模板才能出图）"
else
  log "RENDER: 调用 render_heijin.sh ($html_count 页)"
  set +e
  bash "$TOOLS_DIR/render_heijin.sh" "$NOTE_DIR"
  render_rc=$?
  set -e
  if [[ $render_rc -eq 0 ]]; then
    mark_ok "render_heijin.sh 完成"
  else
    mark_fail "render_heijin.sh 失败 (exit $render_rc)"
  fi
fi

# ---------- 3) 合规初筛 ----------
log "COMPLIANCE: compliance_precheck.py --dir $NOTE_DIR"
set +e
python3 "$TOOLS_DIR/compliance_precheck.py" --dir "$NOTE_DIR"
comp_rc=$?
set -e
if [[ $comp_rc -eq 0 ]]; then
  mark_ok "合规初筛 PASS"
elif [[ $comp_rc -eq 2 ]]; then
  mark_fail "合规初筛用法/目录错误 (exit 2)"
else
  mark_fail "合规初筛 FAIL (exit $comp_rc) — 踩红线须停手确认"
fi

# ---------- 4) 定稿门禁 / 宽松检查 ----------
GATE_TARGET=""
if [[ -d "$NOTE_DIR/final" ]]; then
  GATE_TARGET="$NOTE_DIR/final"
elif [[ -d "$NOTE_DIR/定稿" ]]; then
  GATE_TARGET="$NOTE_DIR/定稿"
elif compgen -G "$NOTE_DIR/00_封面*" >/dev/null 2>&1; then
  GATE_TARGET="$NOTE_DIR"
fi

if [[ -n "$GATE_TARGET" ]]; then
  log "GATE: gate_archive.sh --auto $GATE_TARGET"
  set +e
  bash "$TOOLS_DIR/gate_archive.sh" --auto "$GATE_TARGET"
  gate_rc=$?
  set -e
  if [[ $gate_rc -eq 0 ]]; then
    mark_ok "定稿门禁 PASS ($GATE_TARGET)"
  else
    mark_fail "定稿门禁 FAIL ($GATE_TARGET, exit $gate_rc)"
  fi
else
  # notes 阶段宽松检查：有数据或框架即可，提醒存档阶段再跑门禁
  loose_ok=1
  [[ $has_data -eq 1 || $has_frame -eq 1 ]] || loose_ok=0
  if [[ $loose_ok -eq 1 ]]; then
    mark_ok "notes 阶段宽松检查通过（有数据/框架）"
    mark_warn "无 final/定稿/00_封面* 结构；定稿门禁 gate_archive.sh 在存档阶段再跑"
  else
    mark_fail "notes 宽松检查失败"
  fi
fi

# ---------- 5) 汇总 ----------
if [[ $HARD_FAIL -eq 0 ]]; then
  mark_ok "流水线汇总 PASS (warn=$WARN_N)"
  write_log "PASS"
  exit 0
else
  log "流水线汇总 FAIL (warn=$WARN_N)"
  write_log "FAIL"
  exit 1
fi
