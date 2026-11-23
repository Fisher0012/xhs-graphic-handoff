#!/usr/bin/env bash
# Build the 14.4s Sphere style demo v3 (does not touch v1/v2).
#   picture: v3/render_v3.py   audio: audio/vo.wav (Yunxi, unchanged) + Mixkit BGM/SFX (see audio/LICENSE.txt)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
TMP="$ROOT/.build_v3"; mkdir -p "$TMP"
OUT="$ROOT/sphere_style_demo_v3.mp4"
AUDIO="$ROOT/audio"
[ "${SKIP_RENDER:-0}" = 1 ] || python3 "$ROOT/v3/render_v3.py" "$TMP/picture.mp4"
DUR=14.4
ffmpeg -v error -y -i "$TMP/picture.mp4" \
  -i "$AUDIO/bgm.mp3" -i "$AUDIO/vo.wav" -i "$AUDIO/sfx_glitch.mp3" -i "$AUDIO/sfx_whoosh.mp3" \
  -i "$AUDIO/sfx_click.mp3" -i "$AUDIO/sfx_tick.mp3" \
  -filter_complex "\
[1:a]atrim=8,asetpts=PTS-STARTPTS,atrim=0:${DUR},asetpts=PTS-STARTPTS,loudnorm=I=-30:TP=-1.5:LRA=11,afade=t=out:st=14.0:d=0.4[abgm];\
[2:a]atrim=0:${DUR},asetpts=PTS-STARTPTS,loudnorm=I=-14:TP=-1.5:LRA=11[avo];\
[3:a]atrim=0:0.8,asetpts=PTS-STARTPTS,volume=0.7,afade=t=out:st=0.55:d=0.2[aglt];\
[4:a]atrim=0.32:0.90,asetpts=PTS-STARTPTS,volume=0.6,asplit=3[w1][w2][w3];\
[w1]adelay=3900|3900[awh1];[w2]adelay=7620|7620[awh2];[w3]volume=0.45,adelay=11450|11450[awh3];\
[5:a]volume=0.55,asplit=3[c1][c2][c3];\
[c1]adelay=9240|9240[ac1];[c2]adelay=12190|12190[ac2];[c3]adelay=13420|13420[ac3];\
[6:a]volume=0.8,adelay=13650|13650[atk];\
[abgm][avo][aglt][awh1][awh2][awh3][ac1][ac2][ac3][atk]amix=inputs=10:normalize=0:dropout_transition=0,alimiter=limit=0.95[a]" \
  -map 0:v -map "[a]" -c:v libx264 -pix_fmt yuv420p -crf 16 -preset medium -r 30 \
  -c:a aac -b:a 192k -t ${DUR} -movflags +faststart "$OUT"
python3 - "$OUT" "$ROOT/v3_contact.jpg" <<'PY'
import sys, subprocess, tempfile, glob
from PIL import Image, ImageDraw, ImageFont
src, out = sys.argv[1:]
d = tempfile.mkdtemp()
subprocess.run(["ffmpeg","-v","error","-y","-i",src,"-vf","select=not(mod(n\\,15)),scale=270:480","-vsync","0",f"{d}/f_%03d.png"],check=True)
fs = sorted(glob.glob(f"{d}/f_*.png")); cols = 8; rows = (len(fs)+cols-1)//cols
f = ImageFont.truetype("/home/box/.fonts/NotoSansSC-Black.otf", 22)
sh = Image.new("RGB",(cols*270, rows*480),"black")
for i,p in enumerate(fs):
    im = Image.open(p); dr = ImageDraw.Draw(im)
    dr.rectangle((0,0,84,30),fill=(0,0,0)); dr.text((6,2),f"{i*0.5:.1f}s",font=f,fill=(255,220,0))
    sh.paste(im,((i%cols)*270,(i//cols)*480))
sh.save(out, quality=90); print(out, len(fs), "tiles")
PY
echo "done → $OUT"
