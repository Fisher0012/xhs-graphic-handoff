"""QC for v3: every frame → luminance stats; every 0.25s → sheets + content-area metric."""
import sys, subprocess, numpy as np, json
from PIL import Image, ImageDraw, ImageFont
src = sys.argv[1]; outdir = sys.argv[2]
import os; os.makedirs(outdir, exist_ok=True)
W, H = 1080, 1920
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)
n = fr.shape[0]
lum = []; white = []; content = []
B = 40
for i in range(n):
    f = fr[i].astype(np.float32) / 255
    y = f @ np.array([0.2126, 0.7152, 0.0722], np.float32)
    lum.append(float(y.mean())); white.append(float((y > 0.92).mean()))
    if i % 3 == 0 or True:
        blk = y[:H // B * B, :W // B * B].reshape(H // B, B, W // B, B)
        m = blk.mean((1, 3)); sd = blk.std((1, 3))
        dead = (m < 0.14) & (sd < 0.03)          # flat, near-black block = dead area
        content.append(float(1 - dead.mean()))
lum = np.array(lum); white = np.array(white); content = np.array(content)
flash = []
for i in range(n):
    a = lum[max(0, i - 3):i]; b = lum[i + 1:i + 4]
    if len(a) and len(b) and lum[i] - max(a.max(), b.max()) > 0.06: flash.append(i)
    if len(a) and len(b) and min(a.min(), b.min()) - lum[i] > 0.06: flash.append(i)
jumps = [(i, round(float(lum[i] - lum[i - 1]), 3)) for i in range(1, n) if abs(lum[i] - lum[i - 1]) > 0.08]
res = dict(frames=n, min_content=round(float(content.min()), 3), min_content_t=round(int(content.argmin()) / 30, 3),
           content_below_70=[round(i / 30, 3) for i in np.where(content < 0.70)[0]],
           max_white_frac=round(float(white.max()), 3), max_white_t=round(int(white.argmax()) / 30, 3),
           transient_flash_frames=[round(i / 30, 3) for i in flash], lum_jumps=[(round(i / 30, 3), d) for i, d in jumps])
print(json.dumps(res, ensure_ascii=False, indent=1))
# 0.25s sheets (exact frames round(t*30)), 6 per row at 360x640
ts = [round(k * 0.25, 2) for k in range(int(14.4 / 0.25) + 1) if round(k * 0.25 * 30) < n]
f = ImageFont.truetype("/home/box/.fonts/NotoSansSC-Black.otf", 26)
per = 12
for s in range(0, len(ts), per):
    part = ts[s:s + per]
    sh = Image.new("RGB", (6 * 360, 2 * 640), "black")
    for j, t in enumerate(part):
        im = Image.fromarray(fr[min(n - 1, round(t * 30))]).resize((360, 640), Image.LANCZOS)
        d = ImageDraw.Draw(im); d.rectangle((0, 0, 150, 34), fill=(0, 0, 0)); d.text((6, 2), f"{t:.2f}s c{content[min(n-1, round(t*30))]:.2f}", font=f, fill=(255, 220, 0))
        sh.paste(im, ((j % 6) * 360, (j // 6) * 640))
    sh.save(f"{outdir}/sheet_{s // per:02d}.jpg", quality=88)
