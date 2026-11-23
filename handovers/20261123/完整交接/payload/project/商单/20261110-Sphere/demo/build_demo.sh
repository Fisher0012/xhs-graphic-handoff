#!/usr/bin/env bash
# Assemble the 14.4s Sphere style demo.
#
# Graphic shots 1, 2, 19, 20 come from tools/render_shots.py (baked-in subs).
# Shots 21 and 22 come from tools/render_shots_21_22.py (R4 stills, red boxes,
# zoom-blur, 3D flip, 15s-card insert, baked-in subs).
# Audio: demo/audio/vo.wav + Mixkit BGM/SFX (see audio/LICENSE.txt).
#
# Usage:
#   ./build_demo.sh
#   ./build_demo.sh --rebuild-ui     # also re-render shots 21/22
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
CLIPS="$ROOT/clips"
AUDIO="$ROOT/audio"
GRABS="$ROOT/grabs"
TOOLS="$ROOT/tools"
OUT="$ROOT/sphere_style_demo.mp4"
CONTACT="$ROOT/demo_contact.jpg"
TMP="$ROOT/.build_tmp"
W=1080
H=1920
FPS=30

REBUILD_UI=0
for arg in "$@"; do
  case "$arg" in
    --rebuild-ui) REBUILD_UI=1 ;;
  esac
done

log() { printf '==> %s\n' "$*"; }
need() { command -v "$1" >/dev/null || { echo "missing $1" >&2; exit 1; }; }
need ffmpeg
need ffprobe
need python3

mkdir -p "$CLIPS" "$TMP" "$GRABS"

# ---------------------------------------------------------------------------
# 1. Graphic clips
# ---------------------------------------------------------------------------
missing=0
for s in 1 2 19 20; do
  [[ -f "$CLIPS/shot${s}.mp4" ]] || missing=1
done
if [[ $missing -eq 1 ]]; then
  log "graphic clips missing — running tools/render_shots.py"
  python3 "$TOOLS/render_shots.py" --shots 1,2,19,20
fi

# ---------------------------------------------------------------------------
# 2. Shots 21 / 22
# ---------------------------------------------------------------------------
if [[ $REBUILD_UI -eq 1 || ! -f "$CLIPS/shot21.mp4" || ! -f "$CLIPS/shot22.mp4" ]]; then
  log "rendering shots 21 and 22 from R4 stills"
  python3 "$TOOLS/render_shots_21_22.py"
else
  log "using existing clips/shot21.mp4 and clips/shot22.mp4"
fi

# ---------------------------------------------------------------------------
# 3. Concat (re-encode so timebase / SAR mismatches can't bite us)
# ---------------------------------------------------------------------------
CONCAT="$TMP/concat.txt"
{
  echo "file '$CLIPS/shot1.mp4'"
  echo "file '$CLIPS/shot2.mp4'"
  echo "file '$CLIPS/shot19.mp4'"
  echo "file '$CLIPS/shot20.mp4'"
  echo "file '$CLIPS/shot21.mp4'"
  echo "file '$CLIPS/shot22.mp4'"
} > "$CONCAT"

log "concatenating 6 clips"
ffmpeg -y -f concat -safe 0 -i "$CONCAT" \
  -c:v libx264 -pix_fmt yuv420p -crf 17 -preset medium -an \
  "$TMP/pictured.mp4"

# Subtitles for 21–22 are baked into those clips (same draw_subtitle style
# as shots 2 and 20). subtitle_21_22.ass is kept as a timing reference only.

# ---------------------------------------------------------------------------
# 4. Audio mix
#    BGM alone  → target about -18 LUFS, fade last 0.4s
#    BGM + VO   → VO around -14 LUFS, BGM 12–18 LU under it (≈ -30 LUFS)
#    SFX        → glitch at 0.00; whoosh at 3.90 (chapter), 7.90 (zoom),
#                 11.80 (page-flip). Whoosh file has ~0.32s of leading pad.
# ---------------------------------------------------------------------------
DUR=$(ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "$TMP/pictured.mp4")
log "picture duration ${DUR}s"

# Re-assemble vo.wav if the clause takes exist but vo.wav does not
if [[ ! -f "$AUDIO/vo.wav" && -f "$AUDIO/vo_lines/s1.mp3" ]]; then
  log "assembling audio/vo.wav from clause takes"
  python3 "$TOOLS/assemble_vo.py"
fi

have_bgm=0; have_vo=0; have_glitch=0; have_whoosh=0
bgm_file=""; glitch_file=""; whoosh_file=""
for ext in mp3 wav ogg; do
  [[ -f "$AUDIO/bgm.$ext" ]] && bgm_file="$AUDIO/bgm.$ext" && have_bgm=1 && break
done
[[ -f "$AUDIO/vo.wav" ]] && have_vo=1
for ext in mp3 wav; do
  [[ -f "$AUDIO/sfx_glitch.$ext" ]] && glitch_file="$AUDIO/sfx_glitch.$ext" && have_glitch=1 && break
done
for ext in mp3 wav; do
  [[ -f "$AUDIO/sfx_whoosh.$ext" ]] && whoosh_file="$AUDIO/sfx_whoosh.$ext" && have_whoosh=1 && break
done

inputs=(-i "$TMP/pictured.mp4")
idx=1
filter=""
amix_n=0
amix_list=""

add_audio() {
  inputs+=(-i "$1")
  if [[ -n "$filter" ]]; then
    filter="${filter};$2"
  else
    filter="$2"
  fi
}

if [[ $have_bgm -eq 1 ]]; then
  log "BGM: $bgm_file (in-point 8.0s)"
  local_I="-18"
  if [[ $have_vo -eq 1 ]]; then
    local_I="-30"
    log "VO present — BGM target ${local_I} LUFS (~16 LU under a -14 LUFS voice)"
  else
    log "no VO — BGM target ${local_I} LUFS"
  fi
  fade_st=$(python3 -c "print(max(0, float('$DUR')-0.4))")
  # 8.0s in-point on Stylz, where the groove is already going.
  add_audio "$bgm_file" "[${idx}:a]atrim=8,asetpts=PTS-STARTPTS,aloop=loop=-1:size=2e9,atrim=0:${DUR},asetpts=PTS-STARTPTS,loudnorm=I=${local_I}:TP=-1.5:LRA=11,afade=t=out:st=${fade_st}:d=0.4[abgm]"
  idx=$((idx + 1))
  amix_list="${amix_list}[abgm]"
  amix_n=$((amix_n + 1))
else
  log "no BGM file in audio/"
fi

if [[ $have_vo -eq 1 ]]; then
  log "VO: $AUDIO/vo.wav"
  add_audio "$AUDIO/vo.wav" "[${idx}:a]atrim=0:${DUR},asetpts=PTS-STARTPTS,loudnorm=I=-14:TP=-1.5:LRA=11[avo]"
  idx=$((idx + 1))
  amix_list="${amix_list}[avo]"
  amix_n=$((amix_n + 1))
else
  log "no audio/vo.wav"
fi

if [[ $have_glitch -eq 1 ]]; then
  log "SFX glitch at 0.00 from $glitch_file"
  add_audio "$glitch_file" "[${idx}:a]atrim=0:0.8,asetpts=PTS-STARTPTS,volume=0.7,afade=t=out:st=0.55:d=0.2[aglt]"
  idx=$((idx + 1))
  amix_list="${amix_list}[aglt]"
  amix_n=$((amix_n + 1))
fi

if [[ $have_whoosh -eq 1 ]]; then
  log "SFX whoosh at 3.90 / 7.90 / 11.80 from $whoosh_file"
  # audible peak of Mixkit 1490 sits at 0.40–0.75s; trim the leading pad
  add_audio "$whoosh_file" "[${idx}:a]atrim=0.32:0.90,asetpts=PTS-STARTPTS,volume=0.6,asplit=3[w1][w2][w3];[w1]adelay=3900|3900[awh1];[w2]adelay=7900|7900[awh2];[w3]adelay=11800|11800[awh3]"
  idx=$((idx + 1))
  amix_list="${amix_list}[awh1][awh2][awh3]"
  amix_n=$((amix_n + 3))
fi

if [[ $amix_n -eq 0 ]]; then
  log "no audio sources — writing a silent demo"
  ffmpeg -y -i "$TMP/pictured.mp4" -c:v copy -an "$OUT"
else
  if [[ $amix_n -eq 1 ]]; then
    filter="${filter};${amix_list}anull[a]"
  else
    filter="${filter};${amix_list}amix=inputs=${amix_n}:normalize=0:dropout_transition=0,alimiter=limit=0.95[a]"
  fi
  log "mixing audio ($amix_n track(s))"
  ffmpeg -y "${inputs[@]}" -filter_complex "$filter" -map 0:v -map "[a]" \
    -c:v libx264 -pix_fmt yuv420p -crf 17 -preset medium \
    -c:a aac -b:a 192k -shortest -movflags +faststart \
    "$OUT"
fi

# ---------------------------------------------------------------------------
# 5. Contact sheet
# ---------------------------------------------------------------------------
log "contact sheet → $CONTACT"
python3 - "$TMP/pictured.mp4" "$OUT" "$CONTACT" "$GRABS/assembly" << 'PY'
import sys, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

picture, final, out, grab_dir = sys.argv[1:]
grab_dir = Path(grab_dir)
grab_dir.mkdir(parents=True, exist_ok=True)
# Prefer the mixed final if it exists and has video; else the picture track
src = final if Path(final).exists() else picture
times = [0.10, 1.25, 3.50, 4.50, 6.00, 7.20, 8.00, 8.50, 9.50, 10.50, 11.90, 12.20, 12.50, 13.20, 13.70, 14.20]
thumbs = []
for t in times:
    p = grab_dir / f"t{t:.2f}.png"
    subprocess.run([
        "ffmpeg", "-y", "-ss", f"{t:.2f}", "-i", src, "-frames:v", "1", str(p)
    ], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    thumbs.append((t, Image.open(p).convert("RGB")))

cols = 4
tw, th = 270, 480  # 1080x1920 / 4
rows = (len(thumbs) + cols - 1) // cols
pad, label_h = 8, 28
sheet = Image.new("RGB", (cols * (tw + pad) + pad, rows * (th + pad + label_h) + pad), (20, 20, 22))
try:
    font = ImageFont.truetype("/home/box/.fonts/NotoSansSC-Black.otf", 18)
except Exception:
    font = ImageFont.load_default()
d = ImageDraw.Draw(sheet)
for i, (t, im) in enumerate(thumbs):
    r, c = divmod(i, cols)
    x = pad + c * (tw + pad)
    y = pad + r * (th + pad + label_h)
    sheet.paste(im.resize((tw, th), Image.Resampling.LANCZOS), (x, y))
    d.text((x + 4, y + th + 4), f"{t:.2f}s", font=font, fill=(255, 220, 80))
sheet.save(out, "JPEG", quality=90)
print("wrote", out, sheet.size)
PY

rm -rf "$TMP"
log "wrote $OUT"
ffprobe -hide_banner -show_entries format=duration,size -of default "$OUT" || true
