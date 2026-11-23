#!/usr/bin/env python3
"""Sphere 14.4s style demo v3 — single-timeline renderer (1080x1920 @30fps).

Implements plan/visual_spec_v1.md: unified dark stage, browser frame, E/M camera,
loupe detail card, focus mask, draw-on red stroke, styled cursor, frosted cover.
Usage: render_v2.py OUT.mp4 [--frames t1,t2,...  --png-dir DIR]
"""
from __future__ import annotations
import math, subprocess, sys, functools, argparse
from pathlib import Path
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).parent))
import sources as S  # noqa

ROOT = Path("/workspace/xhs/商单/20261110-Sphere/demo")
W, H, FPS, DUR = 1080, 1920, 30, 14.4
FONT_BLACK = "/home/box/.fonts/NotoSansSC-Black.otf"
FONT_REG = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
FONT_BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
if not Path(FONT_BOLD).exists():
    FONT_BOLD = FONT_BLACK
RED = (224, 0, 14)
WHITE = (255, 255, 255)

# --------------------------------------------------------------------------- easing
def bezier(p1x, p1y, p2x, p2y):
    def f(t):
        if t <= 0: return 0.0
        if t >= 1: return 1.0
        lo, hi = 0.0, 1.0
        for _ in range(40):
            s = (lo + hi) / 2
            x = 3*(1-s)**2*s*p1x + 3*(1-s)*s*s*p2x + s**3
            if x < t: lo = s
            else: hi = s
        s = (lo + hi) / 2
        return 3*(1-s)**2*s*p1y + 3*(1-s)*s*s*p2y + s**3
    return f
CAM = bezier(.65, 0, .35, 1)
EIN = bezier(.05, .7, .1, 1)
EOUT = bezier(.3, 0, .8, .15)
DRAW = bezier(.4, 0, .2, 1)
CUR = bezier(.45, 0, .2, 1)
WHIP = bezier(.7, 0, .3, 1)
def P(t, t0, d, ease=lambda x: x):
    if d <= 0: return 1.0 if t >= t0 else 0.0
    return ease(min(1.0, max(0.0, (t - t0) / d)))
def lerp(a, b, k): return a + (b - a) * k
def lerp_rect(a, b, k): return tuple(lerp(x, y, k) for x, y in zip(a, b))

# --------------------------------------------------------------------------- image helpers (float RGB 0..1, RGBA layers)
def to_f(img): return np.asarray(img, dtype=np.float32) / 255.0
def over(dst, src, x, y, alpha=1.0):
    """Composite RGBA float layer src onto RGB float dst at integer (x,y)."""
    if alpha <= 0.001: return
    x, y = int(round(x)), int(round(y))
    h, w = src.shape[:2]
    x0, y0, x1, y1 = max(0, x), max(0, y), min(dst.shape[1], x + w), min(dst.shape[0], y + h)
    if x0 >= x1 or y0 >= y1: return
    s = src[y0 - y:y1 - y, x0 - x:x1 - x]
    a = s[..., 3:4] * alpha
    d = dst[y0:y1, x0:x1]
    if dst.shape[2] == 4:
        d[..., :3] = d[..., :3] * (1 - a) + s[..., :3] * a
        d[..., 3:4] = a + d[..., 3:4] * (1 - a)
    else:
        d[:] = d * (1 - a) + s[..., :3] * a

def over_sub(dst, src, x, y, alpha=1.0):
    """Sub-pixel placement (for smooth slow motion)."""
    fx, fy = x - math.floor(x), y - math.floor(y)
    if abs(fx) < 1e-3 and abs(fy) < 1e-3:
        return over(dst, src, x, y, alpha)
    M = np.float32([[1, 0, fx], [0, 1, fy]])
    h, w = src.shape[:2]
    s2 = cv2.warpAffine(src, M, (w + 1, h + 1), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
    over(dst, s2, math.floor(x), math.floor(y), alpha)

def scale_layer(src, k):
    if abs(k - 1) < 1e-3: return src
    h, w = src.shape[:2]
    return cv2.resize(src, (max(1, int(w * k)), max(1, int(h * k))), interpolation=cv2.INTER_AREA if k < 1 else cv2.INTER_CUBIC)

def rrect_mask(w, h, r, ss=4):
    m = Image.new("L", (w * ss, h * ss), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, w * ss - 1, h * ss - 1), r * ss, fill=255)
    return to_f(m.resize((w, h), Image.LANCZOS))

@functools.lru_cache(maxsize=None)
def font(path, size): return ImageFont.truetype(path, size)

@functools.lru_cache(maxsize=512)
def text_layer(text, size, color=WHITE, path=FONT_BLACK, stroke=0, stroke_color=(0, 0, 0), tracking=0.0, shadow=0):
    f = font(path, size)
    pad = stroke + 4 + shadow * 3
    # measure with tracking
    widths = [f.getbbox(ch)[2] if ch != " " else size * 0.3 for ch in text]
    asc, desc = f.getmetrics()
    tw = int(sum(widths) + tracking * size * (len(text) - 1)) + 2 * pad
    th = asc + desc + 2 * pad
    img = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    x = pad
    for ch, cw in zip(text, widths):
        d.text((x, pad), ch, font=f, fill=color + (255,), stroke_width=stroke, stroke_fill=stroke_color + (255,))
        x += cw + tracking * size
    arr = to_f(img)
    if shadow:
        a = arr[..., 3]
        sh = cv2.GaussianBlur(a, (0, 0), shadow)
        base = np.zeros_like(arr); base[..., 3] = sh * 0.6
        base = np.roll(base, shadow, axis=0)
        aa = arr[..., 3:4]
        out = base.copy(); out[..., :3] = arr[..., :3]
        out[..., 3:4] = aa + base[..., 3:4] * (1 - aa)
        arr = out
    return arr

def ink_box(layer):
    a = layer[..., 3] > 0.05
    ys, xs = np.where(a)
    return xs.min(), ys.min(), xs.max() + 1, ys.max() + 1

def text_at(dst, text, size, cx=None, x=None, top=None, cy=None, color=WHITE, path=FONT_BLACK, alpha=1.0, stroke=0, anchor_right=None, shadow=0, tracking=0.0):
    L = text_layer(text, size, color, path, stroke, (0, 0, 0), tracking, shadow)
    bx0, by0, bx1, by1 = ink_box(L)
    w = bx1 - bx0; h = by1 - by0
    if cx is not None: px = cx - w / 2 - bx0
    elif anchor_right is not None: px = anchor_right - w - bx0
    else: px = x - bx0
    if cy is not None: py = cy - h / 2 - by0
    else: py = top - by0
    over_sub(dst, L, px, py, alpha)
    return (px + bx0, py + by0, px + bx1, py + by1)

def pill(text, size, fg, bg, padx=22, pady=12, path=FONT_BLACK):
    L = text_layer(text, size, fg, path)
    bx0, by0, bx1, by1 = ink_box(L)
    w, h = bx1 - bx0 + 2 * padx, by1 - by0 + 2 * pady
    out = np.zeros((h, w, 4), np.float32)
    m = rrect_mask(w, h, h // 2)
    out[..., :3] = np.array(bg, np.float32) / 255; out[..., 3] = m
    t = L[by0:by1, bx0:bx1]
    sub = out[pady:pady + t.shape[0], padx:padx + t.shape[1]]
    a = t[..., 3:4]
    sub[..., :3] = sub[..., :3] * (1 - a) + t[..., :3] * a
    return out
pill = functools.lru_cache(maxsize=64)(pill)

def add_shadow_layer(layer, blur=24, dy=16, op=0.5):
    a = layer[..., 3]
    pad = blur * 3
    h, w = a.shape
    big = np.zeros((h + 2 * pad, w + 2 * pad), np.float32)
    big[pad + dy:pad + dy + h, pad:pad + w] = a
    big = cv2.GaussianBlur(big, (0, 0), blur) * op
    out = np.zeros((h + 2 * pad, w + 2 * pad, 4), np.float32); out[..., 3] = big
    return out, pad

# --------------------------------------------------------------------------- backgrounds
def make_stage():
    base = np.zeros((H, W, 3), np.float32) + np.array([0x14, 0x14, 0x18], np.float32) / 255
    chalk = to_f(Image.open(ROOT / "assets/chalkboard_1080x1920.png").convert("RGB"))
    base = base * 0.88 + chalk * 0.12
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.sqrt((xx - 540) ** 2 + (yy - 840) ** 2) / 900
    glow = np.clip(1 - d, 0, 1) ** 1.6
    base += glow[..., None] * (np.array([0x2C, 0x2B, 0x36], np.float32) / 255 - 0x14 / 255) * 1.1
    vd = np.sqrt(((xx - 540) / 540) ** 2 + ((yy - 960) / 960) ** 2)
    vig = 1 - 0.25 * np.clip((vd - 0.7) / 0.7, 0, 1)
    return np.clip(base * vig[..., None], 0, 1)
STAGE = make_stage()
BOARD = to_f(Image.open(ROOT / "assets/chalkboard_1080x1920.png").convert("RGB"))
def make_grid_stage():
    g = BOARD * 0.92 + STAGE * 0.08
    col = np.array([0x2A, 0x2A, 0x30], np.float32) / 255
    for x in range(0, W, 40): g[:, x] = g[:, x] * 0.4 + col * 0.6
    for y in range(0, H, 40): g[y, :] = g[y, :] * 0.4 + col * 0.6
    return g
GRID = make_grid_stage()

# chalk grain mask
rng = np.random.default_rng(7)
_noise = cv2.GaussianBlur(rng.random((H, W)).astype(np.float32), (0, 0), 1.1)
_noise = (_noise - _noise.min()) / (_noise.max() - _noise.min())
def chalkify(layer, strength=0.55, ox=0, oy=0):
    h, w = layer.shape[:2]
    n = _noise[oy:oy + h, ox:ox + w]
    if n.shape != (h, w):
        n = cv2.resize(_noise, (w, h))
    k = np.clip(1 - strength + (n - 0.35) * 2.2 * strength, 0.25, 1)
    out = layer.copy(); out[..., 3] *= k
    return out

# --------------------------------------------------------------------------- subtitles
SUBS = [(2.80, 3.90, "是这三道坎"), (5.10, 6.40, "第三道坎 出镜"), (6.40, 7.90, "不想露脸 也没空拍"),
        (7.90, 9.30, "Sphere的数字分身"), (9.30, 11.80, "传1张照片 生成形象"),
        (11.80, 12.88, "读一段文字"), (12.88, 14.40, "录15秒 克隆声音")]
def draw_subs(fr, t):
    for t0, t1, s in SUBS:
        if t0 <= t < t1:
            k = P(t, t0, 0.10)
            L = text_layer(s, 80, WHITE, FONT_BLACK, 9, (0, 0, 0), 0.02)
            bx0, by0, bx1, by1 = ink_box(L)
            over_sub(fr, L, 540 - (bx1 - bx0) / 2 - bx0, 1600 - (by1 - by0) - by0 + 6 * (1 - k), k)

def draw_header(fr, t, tag=None):
    text_at(fr, "合作内容 · 工具演示，不构成投资建议", 28, anchor_right=1020, top=146, color=WHITE, path=FONT_BOLD, alpha=0.72)
    if tag:
        text_at(fr, tag, 40, x=60, top=140, alpha=0.9)

# --------------------------------------------------------------------------- shot 1–2 hook
def chalk_box_layer(w, h, label, size, stroke=5, alpha_text=1.0):
    ss = 2
    img = Image.new("RGBA", (w * ss, h * ss), (0, 0, 0, 0))
    ImageDraw.Draw(img).rounded_rectangle((stroke * ss, stroke * ss, (w - stroke) * ss, (h - stroke) * ss), 16 * ss, outline=(250, 250, 250, 255), width=stroke * ss)
    lay = to_f(img.resize((w, h), Image.LANCZOS))
    T = text_layer(label, size, WHITE)
    bx0, by0, bx1, by1 = ink_box(T)
    t = T[by0:by1, bx0:bx1]
    ox, oy = (w - t.shape[1]) // 2, (h - t.shape[0]) // 2
    sub = lay[oy:oy + t.shape[0], ox:ox + t.shape[1]]
    a = t[..., 3:4]
    sub[..., :3] = sub[..., :3] * (1 - a) + t[..., :3] * a
    sub[..., 3:4] = sub[..., 3:4] + a * (1 - sub[..., 3:4])
    return chalkify(lay, 0.45)
chalk_box_layer = functools.lru_cache(maxsize=16)(chalk_box_layer)

def hook_title_layer():
    """3-line title block, metallic white, rendered once."""
    lines = [("金融人做IP", 150), ("卡住你的", 200), ("不是剪辑", 200)]
    gap = 46
    Ls = []
    for s, z in lines:
        L = text_layer(s, z, WHITE)
        bx0, by0, bx1, by1 = ink_box(L)
        Ls.append(L[by0:by1, bx0:bx1])
    w = max(l.shape[1] for l in Ls) + 40
    h = sum(l.shape[0] for l in Ls) + gap * 2 + 40
    out = np.zeros((h, w, 4), np.float32)
    y = 20; boxes = []
    for l in Ls:
        x = (w - l.shape[1]) // 2
        g = np.linspace(1.0, 0.88, l.shape[0], dtype=np.float32)[:, None, None]
        ll = l.copy(); ll[..., :3] = ll[..., :3] * g
        out[y:y + l.shape[0], x:x + l.shape[1]] = ll
        boxes.append((x, y, x + l.shape[1], y + l.shape[0])); y += l.shape[0] + gap
    return out, boxes
HOOK, HOOK_BOXES = hook_title_layer()
HOOK_CY = 880
STRIKE_T = 2.44   # vo.wav: 「剪」 affricate burst starts 2.44–2.45s (spectral check)

def glitch(layer, amt, seed):
    """RGB split + horizontal slice jitter. amt 0..1."""
    if amt <= 0.001: return layer
    r = np.random.default_rng(seed)
    h, w = layer.shape[:2]
    pad = 80
    big = np.zeros((h, w + 2 * pad, 4), np.float32); big[:, pad:pad + w] = layer
    out = big.copy()
    # slices
    n = r.integers(5, 10)
    for _ in range(n):
        y0 = r.integers(0, h - 10); hh = r.integers(8, max(9, h // 6))
        dx = int(r.uniform(-60, 60) * amt)
        out[y0:y0 + hh] = np.roll(big[y0:y0 + hh], dx, axis=1)
    sh = int(round(12 * amt + 2))
    res = out.copy()
    res[..., 0] = np.roll(out[..., 0] * out[..., 3], -sh, axis=1)
    res[..., 2] = np.roll(out[..., 2] * out[..., 3], sh, axis=1)
    res[..., 1] = out[..., 1] * out[..., 3]
    a = np.maximum.reduce([np.roll(out[..., 3], -sh, 1), out[..., 3], np.roll(out[..., 3], sh, 1)])
    res[..., 3] = a
    res[..., :3] = np.where(a[..., None] > 1e-4, res[..., :3] / np.maximum(a[..., None], 1e-4), 0)
    return res

def glitch_blocks(fr, t, seed):
    r = np.random.default_rng(seed)
    for _ in range(int(r.integers(4, 9))):
        y = int(r.integers(600, 1250)); hh = int(r.integers(6, 30))
        x = int(r.integers(-100, 900)); ww = int(r.integers(120, 700))
        col = [(1, .1, .25), (.1, .9, 1), (1, 1, 1), (.2, .3, 1)][int(r.integers(0, 4))]
        x0, x1 = max(0, x), min(W, x + ww)
        if x1 > x0:
            fr[y:y + hh, x0:x1] = fr[y:y + hh, x0:x1] * 0.3 + np.array(col, np.float32) * 0.7

def red_strike(fr, x0, y, x1, k, th=16):
    if k <= 0: return
    xe = x0 + (x1 - x0) * k
    lay = np.zeros((th * 3, int(x1 - x0) + th * 3, 4), np.float32)
    cv2.line(lay, (th, th + th // 2), (int(xe - x0) + th, th + th // 4), (RED[0] / 255, RED[1] / 255, RED[2] / 255, 1), th, cv2.LINE_AA)
    over(fr, chalkify(lay, 0.35), x0 - th, y - th - th // 2)

def shot_hook(t):
    fr = GRID.copy()
    hw, hh = HOOK.shape[1], HOOK.shape[0]
    if t < 2.8:
        if t < 0.12:
            glitch_blocks(fr, t, int(t * 1000) + 3)
        else:
            amt = 1 - P(t, 0.12, 0.42, EIN)
            k = 1.0 + 0.03 * P(t, 0.5, 2.3)            # drift
            L = scale_layer(HOOK, k)
            g = glitch(L, amt, int(t * 30) * 13 + 1) if amt > 0.02 else L
            flick = 1.0 if amt < 0.3 else (0.55 + 0.45 * ((int(t * 60) % 3) != 0))
            over_sub(fr, g, 540 - g.shape[1] / 2, HOOK_CY - L.shape[0] / 2, flick)
            if amt > 0.25: glitch_blocks(fr, t, int(t * 1000) + 5)
            # red strike through 剪辑 (last two chars of line 3) at 2.05
            ks = P(t, STRIKE_T, 0.26, DRAW)
            if ks > 0:
                bx0, by0, bx1, by1 = HOOK_BOXES[2]
                ox = 540 - L.shape[1] / 2; oy = HOOK_CY - L.shape[0] / 2
                x_mid = ox + (bx0 + (bx1 - bx0) * 0.5) * k; x_end = ox + bx1 * k
                ymid = oy + (by0 + by1) / 2 * k
                red_strike(fr, x_mid - 6, ymid, x_end + 10, ks)
        draw_header(fr, t)
    else:
        lt = t - 2.8
        k = lerp(1.03, 0.52, P(lt, 0, 0.35, CAM))
        cy = lerp(HOOK_CY, 560, P(lt, 0, 0.35, CAM))
        L = scale_layer(HOOK, k)
        over_sub(fr, L, 540 - L.shape[1] / 2, cy - L.shape[0] / 2)
        bx0, by0, bx1, by1 = HOOK_BOXES[2]
        ox = 540 - L.shape[1] / 2; oy = cy - L.shape[0] / 2
        red_strike(fr, ox + (bx0 + (bx1 - bx0) * 0.5) * k - 4, oy + (by0 + by1) / 2 * k, ox + bx1 * k + 6, 1.0, th=max(6, int(16 * k)))
        labels = ["选题", "合规", "出镜"]
        for i, lab in enumerate(labels):
            p = P(lt, 0.15 + i * 0.15, 0.35, EIN)
            if p <= 0: continue
            B = chalk_box_layer(280, 140, lab, 76)
            Bs = scale_layer(B, 0.92 + 0.08 * p)
            cx = 80 + 140 + i * 320
            over_sub(fr, Bs, cx - Bs.shape[1] / 2, 1060 - Bs.shape[0] / 2, p)
            text_at(fr, str(i + 1), 40, cx=cx, cy=950, color=RED, alpha=p)
        draw_header(fr, t)
    draw_subs(fr, t)
    return fr

# --------------------------------------------------------------------------- shot 19 chapter
def solid_chalk_text(text, size):
    """Solid heavy sans, light chalk grain (no gaps)."""
    L = text_layer(text, size, (250, 250, 250))
    bx0, by0, bx1, by1 = ink_box(L)
    L = L[by0:by1, bx0:bx1].copy()
    h, w = L.shape[:2]
    n = _noise[300:300 + h, 100:100 + w]
    L[..., :3] *= (0.90 + 0.10 * n)[..., None]          # grain in colour only, alpha stays solid
    return L
CH3 = solid_chalk_text("3 出镜", 270)

def chalk_ellipse(w, h, k, color=RED, th=14):
    """Continuous brush ellipse (>=12px), tapered start, colour grain only."""
    pad = 40
    lay = np.zeros((h + 2 * pad, w + 2 * pad, 4), np.float32)
    if k > 0:
        a0 = -100; a1 = a0 + 372 * k
        n = max(2, int(120 * k))
        pts = []
        for i in range(n + 1):
            a = math.radians(a0 + (a1 - a0) * i / n)
            r = 1 + 0.025 * math.sin(a * 3)
            x = w / 2 * r * math.cos(a); y = h / 2 * r * math.sin(a)
            rot = math.radians(-4)
            pts.append(((w + 2 * pad) / 2 + x * math.cos(rot) - y * math.sin(rot), (h + 2 * pad) / 2 + x * math.sin(rot) + y * math.cos(rot)))
        col = tuple(c / 255 for c in color) + (1,)
        for i in range(n):
            f = i / n
            tw = th * (0.75 + 0.25 * min(1, f * 6))
            cv2.line(lay, (int(pts[i][0] * 4) , int(pts[i][1] * 4)), (int(pts[i + 1][0] * 4), int(pts[i + 1][1] * 4)), col, int(tw), cv2.LINE_AA, shift=2)
        nn = _noise[:lay.shape[0], :lay.shape[1]]
        lay[..., :3] *= (0.88 + 0.12 * nn)[..., None]
    return lay

def shot19(t):
    lt = t - 3.9
    fr = BOARD.copy()
    for i, lab in enumerate(["选题", "合规", "出镜"]):
        B = chalk_box_layer(220, 100, lab, 52)
        cx = 120 + 110 + i * 300 - 30
        over(fr, B, cx - 110, 520 - 50, 0.35 if i < 2 else 1.0)
    over(fr, chalk_ellipse(300, 170, P(lt, 0.30, 0.32, DRAW)), (120 + 110 + 600 - 30) - 150 - 40, 520 - 85 - 40)
    k = P(lt, 0.0, 0.12, EIN)
    s = lerp(1.10, 1.0, P(lt, 0.0, 0.22, EIN)) + 0.015 * P(lt, 0.25, 0.95)
    Ls = scale_layer(CH3, s)
    over_sub(fr, Ls, 540 - Ls.shape[1] / 2, 1290 - Ls.shape[0] / 2, k)
    draw_header(fr, t)
    return fr

# --------------------------------------------------------------------------- shot 20 pain card
def icon_tile(kind):
    ss = 2; s = 420 * ss
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    d.rounded_rectangle((8, 8, s - 8, s - 8), 40 * ss, outline=(250, 250, 250, 110), width=4 * ss)
    lw = 12 * ss; c = (250, 250, 250, 255)
    if kind == "camera":
        d.rounded_rectangle((95 * ss, 140 * ss, 285 * ss, 290 * ss), 22 * ss, outline=c, width=lw)
        d.polygon([(285 * ss, 190 * ss), (345 * ss, 155 * ss), (345 * ss, 275 * ss), (285 * ss, 240 * ss)], outline=c, width=lw)
        d.ellipse((150 * ss, 175 * ss, 230 * ss, 255 * ss), outline=c, width=lw)
        d.rounded_rectangle((120 * ss, 110 * ss, 180 * ss, 140 * ss), 8 * ss, outline=c, width=lw - 4)
    else:
        d.ellipse((90 * ss, 90 * ss, 330 * ss, 330 * ss), outline=c, width=lw)
        d.line([(210 * ss, 210 * ss), (210 * ss, 135 * ss)], fill=c, width=lw)
        d.line([(210 * ss, 210 * ss), (265 * ss, 240 * ss)], fill=c, width=lw)
        d.ellipse((198 * ss, 198 * ss, 222 * ss, 222 * ss), fill=c)
        for a in range(0, 360, 30):
            r0, r1 = 100 * ss, 112 * ss
            x, y = 210 * ss + math.cos(math.radians(a)), 210 * ss
            d.line([(210 * ss + r0 * math.cos(math.radians(a)), 210 * ss + r0 * math.sin(math.radians(a))),
                    (210 * ss + r1 * math.cos(math.radians(a)), 210 * ss + r1 * math.sin(math.radians(a)))], fill=c, width=5 * ss)
    return chalkify(to_f(img.resize((420, 420), Image.LANCZOS)), 0.5, 50 if kind == "camera" else 500, 400)
TILES = {k: icon_tile(k) for k in ("camera", "clock")}

def red_slash_layer(k):
    lay = np.zeros((420, 420, 4), np.float32)
    if k > 0:
        x0, y0, x1, y1 = 60, 60, 360, 360
        cv2.line(lay, (x0, y0), (int(x0 + (x1 - x0) * k), int(y0 + (y1 - y0) * k)), (RED[0] / 255, RED[1] / 255, RED[2] / 255, 1), 16, cv2.LINE_AA)
    return chalkify(lay, 0.3, 200, 900)

def shot20_content(t):
    lt = t - 5.1
    fr = BOARD * 0.92 + STAGE * 0.08
    fr = fr.copy()
    p = 1.0
    text_at(fr, "第三道坎 · 出镜", 72, x=60, top=360, alpha=p)
    content = np.zeros((H, W, 4), np.float32)
    for i, (kind, cx, lab, ts) in enumerate([("camera", 300, "露脸出镜", 6.52), ("clock", 780, "拍摄时间", 7.30)]):
        pp = 1.0
        T = TILES[kind] * 1.0
        ks = P(t, ts, 0.22, DRAW)
        T = T.copy()
        if ks > 0:
            T[..., :3] *= (1 - 0.5 * min(1, ks * 1.5))
            S2 = red_slash_layer(ks)
            a = S2[..., 3:4]
            T[..., :3] = T[..., :3] * (1 - a) + S2[..., :3] * a
            T[..., 3:4] = np.maximum(T[..., 3:4], a)
        Ts = scale_layer(T, 0.92 + 0.08 * pp)
        over_sub(fr, Ts, cx - Ts.shape[1] / 2, 900 - Ts.shape[0] / 2, pp)
        pl = 1.0
        text_at(fr, lab, 56, cx=cx, top=1150, alpha=pl * (0.55 if ks > 0.5 else 1.0))
    return fr

def zoom_blur(img, amt, cx=540, cy=900, n=8):
    """img RGB float; amt 0..1 → up to ~6% radial smear."""
    if amt <= 0.01: return img
    acc = np.zeros_like(img)
    for i in range(n):
        s = 1 + 0.07 * amt * i / (n - 1)
        M = np.float32([[s, 0, cx - s * cx], [0, s, cy - s * cy]])
        acc += cv2.warpAffine(img, M, (img.shape[1], img.shape[0]), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    return acc / n

def shot20(t, overlays=True):
    lt = t - 5.1
    fr = shot20_content(t)
    s = 1.0 + 0.03 * P(lt, 0, 2.5)
    if s != 1:
        M = np.float32([[s, 0, 540 - s * 540], [0, s, 900 - s * 900]])
        fr = cv2.warpAffine(fr, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    zo = P(t, 7.60, 0.30, bezier(.5, 0, .9, .4))
    if zo > 0:
        s2 = 1 + 0.25 * zo
        M = np.float32([[s2, 0, 540 - s2 * 540], [0, s2, 900 - s2 * 900]])
        fr = cv2.warpAffine(fr, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        fr = zoom_blur(fr, zo)
        fr = fr * (1 - 0.35 * zo) + BOARD * 0.35 * zo
    if overlays:
        draw_header(fr, t, "③ 出镜")
        draw_subs(fr, t)
    return fr

# --------------------------------------------------------------------------- UI sources
def load_src(path, paints=(), darken=(), covers=(), cover_scale=1.0):
    im = cv2.cvtColor(cv2.imread(str(path), cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB).astype(np.float32) / 255
    for (x0, y0, x1, y1), col in paints:
        if col == "sample":
            im[y0:y1, x0:x1] = im[(y0 + y1) // 2, min(im.shape[1] - 1, x1 + 12)]
        else:
            im[y0:y1, x0:x1] = np.array(col, np.float32) / 255
    for x0, y0, x1, y1 in darken:
        im[y0:y1, x0:x1] *= 0.72
    for x0, y0, x1, y1 in covers:
        frost(im, (x0, y0, x1, y1), cover_scale)
    return im

def frost(im, rect, sc=1.0):
    x0, y0, x1, y1 = rect
    reg = im[y0:y1, x0:x1]
    b = cv2.GaussianBlur(reg, (0, 0), 24 * sc)
    b = cv2.GaussianBlur(b, (0, 0), 24 * sc)
    b = b * 0.45 + 0.55 * np.array([0.965, 0.965, 0.975], np.float32)
    # rounded frosted panel
    h, w = reg.shape[:2]
    m = rrect_mask(w, h, int(10 * sc))[..., None]
    reg[:] = reg * (1 - m) + b * m
    # static pale skeleton bars + label
    for i, (fy, fw) in enumerate([(0.17, 0.86), (0.31, 0.93), (0.45, 0.58)]):
        by = int(h * fy); bh = int(10 * sc)
        reg[by:by + bh, int(28 * sc):int(28 * sc + (w - 56 * sc) * fw)] = reg[by:by + bh, int(28 * sc):int(28 * sc + (w - 56 * sc) * fw)] * 0.6 + 0.4 * np.array([0.84, 0.85, 0.88], np.float32)
    L = text_layer("朗读示例文本 · 约 15 秒", int(26 * sc), (110, 112, 122), FONT_BOLD)
    bx0, by0, bx1, by1 = ink_box(L)
    t = L[by0:by1, bx0:bx1]
    ox, oy = (w - t.shape[1]) // 2, int(h * 0.70)
    sub = reg[oy:oy + t.shape[0], ox:ox + t.shape[1]]
    a = t[..., 3:4]; sub[:] = sub * (1 - a) + t[..., :3] * a

SRC = {k: load_src(p, S.PAINT.get(k, [])) for k, p in S.LO.items()}
SRC.update({
    "overview": load_src(S.LO["overview"], S.PAINT.get("overview", [])),
    "avatar": load_src(S.LO["avatar"], S.PAINT.get("avatar", []), darken=[S.AV_PHOTOS]),
    "reading": load_src(S.LO["reading"], S.PAINT.get("reading", []), covers=[S.RD_TEXT_COVER]),
})
HISRC = {k: load_src(p, covers=S.HI_COVERS.get(k, []), cover_scale=S.HI_SCALE) for k, p in S.HI.items()}
def _swap_panel():
    hi = HISRC["avatar_hi"]; lo = SRC["avatar"]           # lo already darkened on AV_PHOTOS
    hx0, hy0, hx1, hy1 = 970, 316, 1600, 790
    lx0, ly0, lx1, ly1 = S.AV_PHOTOS
    hi[hy0:hy1, hx0:hx1] = cv2.resize(lo[ly0:ly1, lx0:lx1], (hx1 - hx0, hy1 - hy0), interpolation=cv2.INTER_CUBIC)
_swap_panel()

# --------------------------------------------------------------------------- overlays (from v2)
def rrect_path(x0, y0, x1, y1, r, n=240):
    pts = []
    segs = [((x0 + r, y0), (x1 - r, y0)), ("arc", x1 - r, y0 + r, -90, 0), ((x1, y0 + r), (x1, y1 - r)), ("arc", x1 - r, y1 - r, 0, 90),
            ((x1 - r, y1), (x0 + r, y1)), ("arc", x0 + r, y1 - r, 90, 180), ((x0, y1 - r), (x0, y0 + r)), ("arc", x0 + r, y0 + r, 180, 270)]
    for sg in segs:
        if sg[0] == "arc":
            _, cx, cy, a0, a1 = sg
            for i in range(12):
                a = math.radians(a0 + (a1 - a0) * i / 11); pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        else:
            (ax, ay), (bx, by) = sg
            for i in range(20): pts.append((ax + (bx - ax) * i / 19, ay + (by - ay) * i / 19))
    return np.array(pts, np.float32)

def red_stroke(fr, rect, k):
    """Draw-on rounded red stroke around rect (output coords) with glow+shadow."""
    if k <= 0.02: return
    x0, y0, x1, y1 = rect
    x0 -= 8; y0 -= 8; x1 += 8; y1 += 8
    pad = 30
    bw, bh = int(x1 - x0) + 2 * pad, int(y1 - y0) + 2 * pad
    pts = rrect_path(pad, pad, pad + (x1 - x0), pad + (y1 - y0), 12)
    d = np.r_[0, np.cumsum(np.hypot(*np.diff(pts, axis=0).T))]
    n = max(2, int(np.searchsorted(d, d[-1] * min(1, k)) + 1))
    sub = (pts[:n] * 4).astype(np.int32)
    lay = np.zeros((bh * 4, bw * 4, 4), np.float32)
    rc = (RED[0] / 255, RED[1] / 255, RED[2] / 255)
    # shadow
    sh = np.zeros((bh * 4, bw * 4), np.float32)
    cv2.polylines(sh, [sub + np.array([0, 16])], k >= 1, 1.0, 3 * 4, cv2.LINE_AA)
    sh = cv2.resize(sh, (bw, bh), interpolation=cv2.INTER_AREA); sh = cv2.GaussianBlur(sh, (0, 0), 5) * 0.35
    glow = np.zeros((bh * 4, bw * 4), np.float32)
    cv2.polylines(glow, [sub], k >= 1, 1.0, 13 * 4, cv2.LINE_AA)
    glow = cv2.resize(glow, (bw, bh), interpolation=cv2.INTER_AREA) * 0.18
    main = np.zeros((bh * 4, bw * 4), np.float32)
    cv2.polylines(main, [sub], k >= 1, 1.0, 3 * 4, cv2.LINE_AA)
    main = cv2.resize(main, (bw, bh), interpolation=cv2.INTER_AREA)
    L = np.zeros((bh, bw, 4), np.float32); L[..., 3] = sh
    over(fr, L, x0 - pad, y0 - pad)
    L = np.zeros((bh, bw, 4), np.float32); L[..., :3] = rc; L[..., 3] = np.clip(glow, 0, 1)
    over(fr, L, x0 - pad, y0 - pad)
    L[..., 3] = np.clip(main, 0, 1)
    over(fr, L, x0 - pad, y0 - pad)

def make_cursor():
    ss = 8
    pts = [(0, 0), (0, 40), (9.5, 31), (15.5, 45), (21, 42.5), (15, 29), (28, 29)]
    sc = 56 / 45
    img = Image.new("RGBA", (int(40 * sc * ss), int(60 * sc * ss)), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    P2 = [((x * sc + 4) * ss, (y * sc + 4) * ss) for x, y in pts]
    d.polygon(P2, fill=(20, 20, 24, 255))
    # inset white
    cxp = sum(p[0] for p in P2) / len(P2); cyp = sum(p[1] for p in P2) / len(P2)
    inner = [(cxp + (x - cxp) * 0.80, cyp + (y - cyp) * 0.84) for x, y in P2]
    d.line(P2 + [P2[0]], fill=(20, 20, 24, 255), width=int(3 * ss), joint="curve")
    d.polygon(inner, fill=(255, 255, 255, 255))
    arr = to_f(img.resize((img.width // ss, img.height // ss), Image.LANCZOS))
    sh, pad = add_shadow_layer(arr, 5, 6, 0.45)
    out = sh.copy()
    over_a = out[pad:pad + arr.shape[0], pad:pad + arr.shape[1]]
    a = arr[..., 3:4]
    over_a[..., :3] = over_a[..., :3] * (1 - a) + arr[..., :3] * a
    over_a[..., 3:4] = a + over_a[..., 3:4] * (1 - a)
    return out, pad + 4
CURSOR, CUR_OFF = make_cursor()

def draw_cursor(fr, x, y, alpha=1.0, press=0.0):
    if alpha <= 0: return
    C = scale_layer(CURSOR, 1 - 0.1 * press) if press > 0 else CURSOR
    k = 1 - 0.1 * press
    over_sub(fr, C, x - CUR_OFF * k, y - CUR_OFF * k, alpha)

def ripple(fr, x, y, k):
    if k <= 0 or k >= 1: return
    r = 4 + 41 * EIN(k)
    lay = np.zeros((120, 120, 4), np.float32)
    cv2.circle(lay, (60, 60), int(r), (1, 1, 1, 1), 3, cv2.LINE_AA)
    over(fr, lay, x - 60, y - 60, 0.7 * (1 - k))

def arc_point(p0, p1, k, bend=0.10):
    mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    cx, cy = mx - dy * bend, my + dx * bend
    return ((1 - k) ** 2 * p0[0] + 2 * (1 - k) * k * cx + k * k * p1[0], (1 - k) ** 2 * p0[1] + 2 * (1 - k) * k * cy + k * k * p1[1])

def leader(fr, p_from, p_to, k, alpha=0.85, dot=True, th=2.5, dashed=False):
    if k <= 0: return
    x0, y0 = p_from; x1, y1 = p_to
    xe, ye = x0 + (x1 - x0) * k, y0 + (y1 - y0) * k
    bx0, by0 = int(min(x0, x1)) - 12, int(min(y0, y1)) - 12
    bw, bh = int(abs(x1 - x0)) + 26, int(abs(y1 - y0)) + 26
    lay = np.zeros((bh * 2, bw * 2, 4), np.float32)
    cv2.line(lay, (int((x0 - bx0) * 2), int((y0 - by0) * 2)), (int((xe - bx0) * 2), int((ye - by0) * 2)), (1, 1, 1, 1), int(th * 2), cv2.LINE_AA)
    if dot and k >= 1:
        cv2.circle(lay, (int((x1 - bx0) * 2), int((y1 - by0) * 2)), 10, (1, 1, 1, 1), -1, cv2.LINE_AA)
    lay = cv2.resize(lay, (bw, bh), interpolation=cv2.INTER_AREA)
    over(fr, lay, bx0, by0, alpha)

def dashed_rect(fr, r, alpha):
    if alpha <= 0: return
    x0, y0, x1, y1 = [int(v) for v in r]
    lay = np.zeros((y1 - y0 + 6, x1 - x0 + 6, 4), np.float32)
    pts = rrect_path(3, 3, x1 - x0 + 3, y1 - y0 + 3, 8, 400)
    d = np.r_[0, np.cumsum(np.hypot(*np.diff(pts, axis=0).T))]
    for i in range(len(pts) - 1):
        if int(d[i] // 9) % 2 == 0:
            cv2.line(lay, tuple(pts[i].astype(int)), tuple(pts[i + 1].astype(int)), (1, 1, 1, 1), 2, cv2.LINE_AA)
    over(fr, lay, x0 - 3, y0 - 3, alpha)


# =========================================================================== v3 UI section (7.9–14.4)
# Portrait composition: full-bleed blurred Sphere workbench + 1020px browser window + cards in the free bands.
WIN_X, WIN_Y, TB = 30, 410, 40
VP_W = 1020
EX0, EY0, EX1, EY1 = 80, 0, 1080, 1012            # E crop: sidebar dropped, page title + both modules kept
E_S = VP_W / (EX1 - EX0)                          # 1.02
VP_H = int(round((EY1 - EY0) * E_S))              # 1032
WIN_H = TB + VP_H
VP_X, VP_Y = WIN_X, WIN_Y + TB
E_CAM = ((EX0 + EX1) / 2, (EY0 + EY1) / 2, E_S)
M_AV = (960.0, 735.0, 1.111)                      # avatar modal ≈1000px wide, sits at y≈532–1101
M_RD = (960.0, 742.0, 1.20)                       # reading modal 960px wide, y≈478–1112
# 175% avatar ↔ 100% avatar mapping (measured on the upload column)
HXK, HYK = 1.512, 1.508
def lo2hi_cam(c): return (315 + (c[0] - 531) * HXK, 315 + (c[1] - 411) * HYK, c[2] / HXK)
PUSH_HI = (627.0, 557.0, VP_W / 670)              # hi view x 292–962, y 218–896 (no cut text)
PUSH_LO = (531 + (PUSH_HI[0] - 315) / HXK, 411 + (PUSH_HI[1] - 315) / HYK, PUSH_HI[2] * HXK)
SCAN_BTN_HI = (775, 400, 903, 453)
REQ_ITEMS_HI = [(348, 812, 609, 869), (669, 812, 930, 869), (990, 812, 1271, 869), (1332, 812, 1572, 869)]
REC_BTN_HI = (412, 827, 1508, 894)

def make_chrome():
    ss = 3
    img = Image.new("RGBA", (VP_W * ss, WIN_H * ss), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, VP_W * ss - 1, WIN_H * ss - 1), 22 * ss, fill=(0x23, 0x23, 0x29, 255))
    for i in range(3):
        cx = (24 + i * 19) * ss; cy = 20 * ss
        d.ellipse((cx - 5 * ss, cy - 5 * ss, cx + 5 * ss, cy + 5 * ss), fill=(0x4A, 0x4A, 0x52, 255))
    d.rounded_rectangle((88 * ss, 7 * ss, 340 * ss, 40 * ss + 10 * ss), 9 * ss, fill=(0x30, 0x30, 0x37, 255))
    img = img.resize((VP_W, WIN_H), Image.LANCZOS)
    arr = to_f(img)
    ov = SRC["overview"]; lx0, ly0, lx1, ly1 = S.LOGO
    logo = cv2.resize(ov[ly0:ly1, lx0:lx1], (18, 18), interpolation=cv2.INTER_AREA)
    lg = np.zeros((18, 18, 4), np.float32); lg[..., :3] = 0.92; lg[..., 3] = np.clip((1 - logo.mean(axis=2)) * 1.8, 0, 1)
    over(arr, lg, 102, 12)
    text_at(arr, "AI分身 - Sphere", 19, x=128, cy=21, color=(235, 235, 240), path=FONT_BOLD)
    return arr
CHROME = make_chrome()
WIN_MASK = rrect_mask(VP_W, WIN_H, 22)
WIN_SHADOW1, SH1P = add_shadow_layer(np.dstack([np.zeros((WIN_H, VP_W, 3), np.float32), WIN_MASK]), 40, 34, 0.6)
WIN_SHADOW2, SH2P = add_shadow_layer(np.dstack([np.zeros((WIN_H, VP_W, 3), np.float32), WIN_MASK]), 10, 8, 0.35)

# ---- full-bleed backdrop: Sphere workbench, cover-fit, gaussian 10px + 40% black (+ soft scrims for the text bands)
def make_backdrop():
    ov = SRC["overview"].copy()
    ov[1168:1200, 0:220] = ov[1160, 110]             # paint the bottom-left URL tooltip out of the backdrop source
    k = H / ov.shape[0]                              # 1.6
    big = cv2.resize(ov, (int(ov.shape[1] * k), H), interpolation=cv2.INTER_AREA)
    x0 = 40
    bg = big[:, x0:x0 + W].copy()
    bg = cv2.GaussianBlur(bg, (0, 0), 10) * 0.60
    yy = np.arange(H, dtype=np.float32)
    scrim = 1 - 0.30 * np.clip((430 - yy) / 430, 0, 1) - 0.28 * np.clip((yy - 1480) / 440, 0, 1)
    return np.clip(bg * scrim[:, None, None], 0, 1).astype(np.float32)
BACKDROP = make_backdrop()

def cam_matrix(cam):
    cx, cy, s = cam
    return np.float32([[s, 0, VP_W / 2 - s * cx], [0, s, VP_H / 2 - s * cy]])

def render_vp(src, cam):
    cx, cy, s = cam
    img = src
    if s < 0.95:
        img = cv2.GaussianBlur(src, (0, 0), 0.42 * math.sqrt(1 / (s * s) - 1))
    return cv2.warpAffine(img, cam_matrix(cam), (VP_W, VP_H), flags=cv2.INTER_CUBIC if s > 1.02 else cv2.INTER_LINEAR,
                          borderMode=cv2.BORDER_REPLICATE)

def s2o(cam, x, y):
    cx, cy, s = cam
    return VP_X + VP_W / 2 + (x - cx) * s, VP_Y + VP_H / 2 + (y - cy) * s
def rect_s2o(cam, r):
    a = s2o(cam, r[0], r[1]); b = s2o(cam, r[2], r[3]); return (a[0], a[1], b[0], b[1])
def cam_lerp(a, b, k):
    return (lerp(a[0], b[0], k), lerp(a[1], b[1], k), a[2] * (b[2] / a[2]) ** k)

def focus_mask(vp, hole_vp, k, radius=14):
    if k <= 0: return vp
    x0, y0, x1, y1 = hole_vp
    ex = 12 * (1 + 0.24 * (1 - k))
    x0 -= ex; y0 -= ex; x1 += ex; y1 += ex
    ss = 2
    m = Image.new("L", (VP_W * ss, VP_H * ss), 0)
    ImageDraw.Draw(m).rounded_rectangle((x0 * ss, y0 * ss, x1 * ss, y1 * ss), radius * ss, fill=255)
    hole = to_f(m.resize((VP_W, VP_H), Image.LANCZOS))[..., None]
    blur = cv2.GaussianBlur(vp, (0, 0), 2.0)
    dim = blur * (1 - 0.45) + np.array([10, 10, 14], np.float32) / 255 * 0.45
    outside = vp * (1 - k) + dim * k
    v = vp * hole + outside * (1 - hole)
    lay = Image.new("L", (VP_W * ss, VP_H * ss), 0)
    ImageDraw.Draw(lay).rounded_rectangle((x0 * ss, y0 * ss, x1 * ss, y1 * ss), radius * ss, outline=255, width=2 * ss)
    line = to_f(lay.resize((VP_W, VP_H), Image.LANCZOS))[..., None] * 0.9 * k
    return v * (1 - line) + line

LOUPE_W = 960
def card_frame(content, radius=20):
    h, w = content.shape[:2]
    card = np.zeros((h, w, 4), np.float32); card[..., :3] = content
    m = rrect_mask(w, h, radius); card[..., 3] = m
    m2 = np.zeros_like(m); m2[2:-2, 2:-2] = rrect_mask(w - 4, h - 4, radius - 2)
    b = np.clip(m - m2, 0, 1)[..., None] * 0.16
    card[..., :3] = card[..., :3] * (1 - b) + b * 0.6
    return card

def hi_crop(key, rect, out_w, feather=(False, False)):
    x0, y0, x1, y1 = rect
    s = out_w / (x1 - x0); oh = int(round((y1 - y0) * s))
    M = np.float32([[s, 0, -s * x0], [0, s, -s * y0]])
    c = np.clip(cv2.warpAffine(HISRC[key], M, (out_w, oh), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE), 0, 1)
    if feather[0] or feather[1]:
        fa = np.ones(out_w, np.float32)
        if feather[0]: fa *= np.clip(np.arange(out_w) / 80, 0, 1)
        if feather[1]: fa *= np.clip((out_w - 1 - np.arange(out_w)) / 80, 0, 1)
        bgc = np.median(c.reshape(-1, 3), axis=0)
        c = c * fa[None, :, None] + bgc * (1 - fa[None, :, None])
    return c, s

# ---- detail cards (built once)
def build_req_card():
    """照片要求: the 4 chips of the 175% requirement bar re-flowed into a 2×2 grid (text ≈36px)."""
    cw, gap, pad = 438, 20, 22
    cells = []
    for r in REQ_ITEMS_HI:
        c, s = hi_crop("avatar_hi", r, cw)
        cells.append(c)
    ch = max(c.shape[0] for c in cells)
    bgc = np.median(cells[0].reshape(-1, 3), axis=0)
    h = pad * 2 + ch * 2 + gap
    content = np.zeros((h, LOUPE_W, 3), np.float32) + 1.0
    for i, c in enumerate(cells):
        x = pad + (i % 2) * (cw + gap + (LOUPE_W - 2 * pad - 2 * cw - gap)); y = pad + (i // 2) * (ch + gap)
        cell = np.zeros((ch, cw, 4), np.float32); cell[..., :3] = bgc; cell[..., 3] = rrect_mask(cw, ch, 14)
        cell[:c.shape[0], :, :3] = c
        over(content, cell, x, y)
    return card_frame(content)
REQ_CARD = build_req_card()
def build_rec_card():
    x0, y0, x1, y1 = REC_BTN_HI
    rect = (680, 806, 1232, 962)
    c, s = hi_crop("reading_hi", rect, LOUPE_W, (True, True))
    return card_frame(c), rect, s
REC_CARD, REC_RECT, REC_S = build_rec_card()
REC_RED_HI = (890, 840, 1032, 884)

def place_card(dst, card, y, k, label=None, src_rect_out=None, dx=0.0):
    """Card centred horizontally at top y; rises 30px + fades with k; dashed source box + connectors."""
    if k <= 0: return None
    h, w = card.shape[:2]
    x = (W - w) / 2 + dx; yy = y + 30 * (1 - k)
    sh, pad = add_shadow_layer_cached(id(card), card)
    sc = 0.96 + 0.04 * k
    cs = scale_layer(card, sc); shs = scale_layer(sh, sc)
    cx, cy = x + w / 2, yy + h / 2
    if src_rect_out is not None:
        dashed_rect(dst, src_rect_out, 0.9 * k)
        lk = min(1, k * 1.2)
        leader(dst, (src_rect_out[0], src_rect_out[3]), (x + 20, yy), lk, alpha=0.45 * k, dot=False, th=1.5)
        leader(dst, (src_rect_out[2], src_rect_out[3]), (x + w - 20, yy), lk, alpha=0.45 * k, dot=False, th=1.5)
    over_sub(dst, shs, cx - shs.shape[1] / 2, cy - shs.shape[0] / 2, k)
    over_sub(dst, cs, cx - cs.shape[1] / 2, cy - cs.shape[0] / 2, k)
    if label:
        pl = pill(label, 30, (255, 255, 255), RED, 18, 9)
        over_sub(dst, pl, x + 20, yy - pl.shape[0] / 2, k)
    return (x, yy, x + w, yy + h)
_SHC = {}
def add_shadow_layer_cached(key, card):
    if key not in _SHC: _SHC[key] = add_shadow_layer(card, 28, 22, 0.55)
    return _SHC[key]

def red_stroke_layer_safe(dst, rect, k):
    red_stroke(dst, rect, k)

# ---- top text band (module title + steps): y 205–380
TITLE_CY, STEPS_CY = 262, 350
def module_title(fr, idx, name, alpha=1.0, dy=0.0, clip=(205, 318)):
    tmp = fr.copy()
    pl = pill(f"模块{'①②'[idx]}", 34, (255, 255, 255), RED, 18, 10)
    over_sub(tmp, pl, 60, TITLE_CY - pl.shape[0] / 2 + dy, alpha)
    text_at(tmp, name, 68, x=60 + pl.shape[1] + 20, cy=TITLE_CY + dy, alpha=alpha)
    c0, c1 = clip; fr[c0:c1] = tmp[c0:c1]

def steps(fr, a, b, lit, alpha=1.0):
    if alpha <= 0: return
    x = 60
    for i, s in enumerate([a, "→", b]):
        op = 1.0 if ((i == 0 and lit == 0) or (i == 2 and lit == 1)) else (0.5 if i == 1 else 0.42)
        bb = text_at(fr, s, 42, x=x, cy=STEPS_CY, alpha=alpha * op, path=FONT_BLACK if op == 1 else FONT_BOLD)
        x = bb[2] + 20

def window_onto(dst, vp, alpha=1.0, dx=0.0):
    win = CHROME.copy()
    win[TB:, :, :3] = vp; win[TB:, :, 3] = 1
    win[..., 3] *= WIN_MASK
    over(dst, WIN_SHADOW1, WIN_X - SH1P + dx, WIN_Y - SH1P, alpha)
    over(dst, WIN_SHADOW2, WIN_X - SH2P + dx, WIN_Y - SH2P, alpha)
    over(dst, win, WIN_X + dx, WIN_Y, alpha)

def hole_of(cam, r):
    a = rect_s2o(cam, r); return (a[0] - VP_X, a[1] - VP_Y, a[2] - VP_X, a[3] - VP_Y)

def badge(dst, cam, card, label, t, t_in, t_out):
    if not (t_in <= t < t_out + 0.2): return
    kd = P(t, t_in, 0.28, DRAW)
    k = kd * (1 - P(t, t_out, 0.15, EOUT))
    if k <= 0: return
    r = rect_s2o(cam, card)
    py = (r[1] + r[3]) / 2
    pl = pill(label, 34, (255, 255, 255), RED, 20, 11)
    px = r[2] + 64
    leader(dst, (px, py), (r[2] - 6, py), kd, alpha=0.95 * k)
    pk = P(t, t_in + 0.12, 0.25, EIN) * (1 - P(t, t_out, 0.15, EOUT))
    over_sub(dst, pl, px + 10 * (1 - pk), py - pl.shape[0] / 2, pk)

CARD1_C = ((S.CARD1[0] + S.CARD1[2]) / 2, (S.CARD1[1] + S.CARD1[3]) / 2)
CARD2_C = ((S.CARD2[0] + S.CARD2[2]) / 2, (S.CARD2[1] + S.CARD2[3]) / 2)

# ---------------------------------------------------------------- scenes (drawn onto an RGBA layer so the push can move them)
def scene_E1(t, L):
    cam = (E_CAM[0], E_CAM[1], E_CAM[2] * (1 + 0.010 * P(t, 7.9, 1.4)))
    vp = render_vp(SRC["overview"], cam)
    hv = P(t, 9.02, 0.08)
    if hv > 0: vp = vp * (1 - hv) + render_vp(SRC["card1_hover"], cam) * hv
    window_onto(L, vp)
    badge(L, cam, S.CARD1, "① 创建数字分身", t, 8.30, 9.30)
    badge(L, cam, S.CARD2, "② 创建我的声音", t, 8.42, 9.30)
    if 8.55 <= t:
        p0 = (VP_X + VP_W - 80, VP_Y + VP_H - 60)
        p1 = s2o(cam, *CARD1_C)
        x, y = arc_point(p0, p1, P(t, 8.55, 0.55, CUR))
        press = 1 - abs(P(t, 9.22, 0.12) * 2 - 1) if 9.22 <= t < 9.34 else 0
        ripple(L, x, y, P(t, 9.26, 0.30))
        draw_cursor(L, x, y, P(t, 8.55, 0.15), press)

def scene_AV(t, L):
    # camera: E → whole modal → push into upload column (175% source) → back to whole modal
    base = (E_CAM[0], E_CAM[1], E_CAM[2] * 1.010)
    if t < 10.05:
        cam = cam_lerp(base, M_AV, P(t, 9.30, 0.40, CAM)); hik = 0.0
    elif t < 10.85:
        k = P(t, 10.05, 0.42, CAM); cam = cam_lerp(M_AV, PUSH_LO, k); hik = P(t, 10.27, 0.16)
    else:
        k = P(t, 10.85, 0.36, CAM); cam = cam_lerp(PUSH_LO, M_AV, k); hik = 1 - P(t, 10.85, 0.12)
        if t > 11.21: cam = (cam[0], cam[1], cam[2] * (1 + 0.012 * P(t, 11.21, 0.6)))
    mix = P(t, 9.64, 0.24, SMOOTH)      # modal opens once the camera has arrived (never half outside the window)
    vp = render_vp(SRC["avatar"], cam)
    if mix < 1: vp = render_vp(SRC["overview"], cam) * (1 - mix) + vp * mix
    camh = lo2hi_cam(cam)
    if hik > 0: vp = vp * (1 - hik) + render_vp(HISRC["avatar_hi"], camh) * hik
    # focus on 你的照片 → 视频效果 while the step "生成形象" is lit
    if t >= 11.02:
        vp = focus_mask(vp, hole_of(cam, S.AV_PHOTOS), P(t, 11.02, 0.40, SMOOTH))
    window_onto(L, vp)
    # red stroke on 扫码上传 (in the pushed 175% view)
    if 10.45 <= t < 11.0:
        rk = P(t, 10.48, 0.32, DRAW) * (1 - P(t, 10.85, 0.12, EOUT))
        red_stroke(L, rect_s2o(camh, SCAN_BTN_HI), rk)
    # 照片要求 card under the modal
    if t >= 11.0:
        place_card(L, REQ_CARD, 1128, P(t, 11.02, 0.32, EIN), "照片要求", rect_s2o(cam, S.AV_REQ_BAR))

def scene_E2(t, L):
    cam = E_CAM
    vp = render_vp(SRC["overview"], cam)
    hv = P(t, 12.08, 0.08)
    if hv > 0: vp = vp * (1 - hv) + render_vp(SRC["card2_hover"], cam) * hv
    if t >= 11.85:
        vp = focus_mask(vp, hole_of(cam, S.CARD2), P(t, 11.85, 0.40, SMOOTH))
    window_onto(L, vp)
    badge(L, cam, S.CARD2, "② 创建我的声音", t, 11.80, 99)
    if 11.85 <= t:
        p0 = (VP_X + VP_W * 0.66, VP_Y + VP_H * 0.92)
        p1 = s2o(cam, *CARD2_C)
        x, y = arc_point(p0, p1, P(t, 11.85, 0.36, CUR), -0.12)
        press = 1 - abs(P(t, 12.17, 0.12) * 2 - 1) if 12.17 <= t < 12.29 else 0
        ripple(L, x, y, P(t, 12.21, 0.30))
        draw_cursor(L, x, y, P(t, 11.85, 0.12), press)

def scene_RD(t, L):
    k = P(t, 12.30, 0.28, CAM)
    cam = cam_lerp(E_CAM, M_RD, k)
    if t > 13.80: cam = (cam[0], cam[1], cam[2] * (1 + 0.012 * P(t, 13.80, 0.6)))
    mix = P(t, 12.54, 0.24, SMOOTH)
    vp = render_vp(SRC["reading"], cam)
    if mix < 1:   # continue from the focused card-2 state of scene_E2 (no bright flash)
        base_old = render_vp(SRC["card2_hover"], cam)
        old = focus_mask(base_old, hole_of(cam, S.CARD2), 1.0)
        dim = cv2.GaussianBlur(base_old, (0, 0), 2.0) * 0.55 + np.array([10, 10, 14], np.float32) / 255 * 0.45
        q = P(t, 12.30, 0.22, SMOOTH)        # the clicked card hands over to the dimmed page, then the modal fades in
        old = old * (1 - q) + dim * q
        vp = old * (1 - mix) + vp * mix
    if t >= 12.76:
        vp = focus_mask(vp, hole_of(cam, S.RD_COLUMN), P(t, 12.76, 0.36, SMOOTH))
        x0, y0, x1, y1 = S.RD_TEXT_COVER
        h = y1 - y0; w = x1 - x0
        for i, (fy, fw) in enumerate([(0.17, 0.86), (0.31, 0.93), (0.45, 0.58)]):
            kb = P(t, 12.78 + i * 0.10, 0.14)
            if kb <= 0: continue
            bx0 = x0 + 28; bx1 = bx0 + (w - 56) * fw * kb; by = y0 + int(h * fy)
            a = rect_s2o(cam, (bx0, by, bx1, by + 10))
            xa, ya, xb, yb = [int(round(v)) for v in (a[0] - VP_X, a[1] - VP_Y, a[2] - VP_X, a[3] - VP_Y)]
            if xb > xa: vp[ya:yb, xa:xb] = vp[ya:yb, xa:xb] * 0.35 + 0.65 * np.array([0.55, 0.62, 0.95], np.float32)
    window_onto(L, vp)
    if t >= 12.88:
        kin = P(t, 12.88, 0.32, EIN)
        lab = "开始录制" if t < 13.75 else "录满 15 秒 · 完成克隆"
        box = place_card(L, REC_CARD, 1140, kin, lab, rect_s2o(cam, S.DETAILS["rec_btn"]["lo_rect"]))
        if box is not None:
            x0, y0, x1, y1 = REC_RECT
            r = REC_RED_HI
            red_stroke(L, (box[0] + (r[0] - x0) * REC_S, box[1] + (r[1] - y0) * REC_S, box[0] + (r[2] - x0) * REC_S, box[1] + (r[3] - y0) * REC_S), P(t, 13.25, 0.32, DRAW))
    if t >= 12.95:
        p1 = s2o(cam, *S.REC_CURSOR)
        p0 = (p1[0] + 160, p1[1] + 90)
        x, y = arc_point(p0, p1, P(t, 12.95, 0.45, CUR))
        press = 1 - abs(P(t, 13.40, 0.12) * 2 - 1) if 13.40 <= t < 13.52 else 0
        ripple(L, x, y, P(t, 13.44, 0.30))
        draw_cursor(L, x, y, P(t, 12.95, 0.15) * (1 - P(t, 13.95, 0.2)), press)

PUSH_T0, PUSH_D = 11.45, 0.40
SMOOTH = bezier(0.4, 0, 0.2, 1)
PUSH = bezier(0.4, 0, 0.2, 1)

def shot_ui(t, overlays=True):
    ent = P(t, 7.90, 0.35, EIN)
    fr = BACKDROP * lerp(0.45, 1.0, ent)
    L = np.zeros((H, W, 4), np.float32)
    if t < 9.30:
        scene_E1(t, L)
    elif t < PUSH_T0:
        scene_AV(t, L)
    elif t < PUSH_T0 + PUSH_D:
        k = PUSH(P(t, PUSH_T0, PUSH_D))
        A = np.zeros_like(L); B = np.zeros_like(L)
        scene_AV(PUSH_T0, A); scene_E2(t, B)
        over(L, A, -W * k, 0); over(L, B, W * (1 - k), 0)
    elif t < 12.30:
        scene_E2(t, L)
    else:
        scene_RD(t, L)
    if ent < 1:
        cnv = fr.copy(); over(cnv, L, 0, 0)
        s = lerp(1.12, 1.0, ent)
        cx, cy = WIN_X + VP_W / 2, WIN_Y + WIN_H / 2
        M = np.float32([[s, 0, cx - s * cx], [0, s, cy - s * cy]])
        cnv = cv2.warpAffine(cnv, M, (W, H), borderMode=cv2.BORDER_REPLICATE)
        tilt = 6 * (1 - ent)
        if tilt > 0.1:
            dy = math.sin(math.radians(tilt)) * 60
            src_q = np.float32([[0, 0], [W, 0], [W, H], [0, H]]); q = np.float32([[dy, 0], [W - dy, 0], [W, H], [0, H]])
            cnv = cv2.warpPerspective(cnv, cv2.getPerspectiveTransform(src_q, q), (W, H), borderMode=cv2.BORDER_REPLICATE)
        fr = zoom_blur(cnv, 1 - ent, cx, cy)
    else:
        over(fr, L, 0, 0)

    # ---- top band: what this page is → module ① → module ②
    if t < 9.30:
        a = P(t, 8.0, 0.30, EIN) * (1 - P(t, 9.16, 0.14, EOUT))
        text_at(fr, "Sphere · 数字分身工作台", 64, x=60, cy=TITLE_CY + 14 * (1 - a), alpha=a)
        text_at(fr, "形象和声音，两大模块都在这一页", 40, x=60, cy=STEPS_CY + 14 * (1 - a), alpha=a * 0.85, path=FONT_BOLD)
    elif t < 11.80:
        p = P(t, 9.30, 0.25, EIN)
        module_title(fr, 0, "创建数字分身", alpha=p, dy=40 * (1 - p))
    else:
        p = P(t, 11.80, 0.25, EIN)
        module_title(fr, 0, "创建数字分身", alpha=1 - p, dy=-40 * p)
        module_title(fr, 1, "创建我的声音", alpha=p, dy=40 * (1 - p))
    if 9.38 <= t < 11.80:
        a = P(t, 9.38, 0.25, EIN) * (1 - P(t, 11.62, 0.15, EOUT))
        steps(fr, "① 上传 1 张照片", "② 生成形象", 0 if t < 10.85 else 1, a)
    if t >= 11.90:
        steps(fr, "① 读一段文字", "② 录 15 秒", 0 if t < 12.88 else 1, P(t, 11.90, 0.25, EIN))
    # ---- 15 秒 counter: counts 0→15 in 13.30–13.75, then holds on 「15秒」 to the end (0.65s)
    if t >= 13.30:
        k = P(t, 13.30, 0.45, EIN)
        n = 15 if t >= 13.75 else min(14, int(15 * k))
        a = P(t, 13.30, 0.12)
        pop = 1 + 0.10 * (1 - P(t, 13.75, 0.18, EIN)) if t >= 13.75 else 1.0
        bb = text_at(fr, "秒", 64, anchor_right=1020, cy=TITLE_CY + 12, alpha=a)
        text_at(fr, str(n), int(116 * pop), anchor_right=bb[0] - 10, cy=TITLE_CY, color=RED, alpha=a)
    if overlays:
        draw_header(fr, t, "③ 出镜")
        draw_subs(fr, t)
    return fr

# --------------------------------------------------------------------------- timeline
def frame(t):
    if t < 3.9: fr = shot_hook(t)
    elif t < 5.1: fr = shot19(t)
    elif t < 7.9: fr = shot20(t)
    else:
        x = P(t, 7.90, 0.36, SMOOTH)          # dissolve out of the zoom-through (no hard dark→white cut)
        if x < 1:
            fr = shot20(7.8999, False) * (1 - x) + shot_ui(t, False) * x
            draw_header(fr, t, "③ 出镜"); draw_subs(fr, t)
        else:
            fr = shot_ui(t)
    return np.clip(fr, 0, 1)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--frames", default="")
    ap.add_argument("--png-dir", default="")
    a = ap.parse_args()
    if a.frames:
        d = Path(a.png_dir); d.mkdir(parents=True, exist_ok=True)
        for s in a.frames.split(","):
            t = float(s)
            Image.fromarray((frame(t) * 255 + 0.5).astype(np.uint8)).save(d / f"t{t:05.2f}.png")
        return
    n = int(round(DUR * FPS))
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "15", "-preset", "medium", a.out], stdin=subprocess.PIPE)
    for i in range(n):
        p.stdin.write((frame(i / FPS) * 255 + 0.5).astype(np.uint8).tobytes())
        if i % 60 == 0: print(f"frame {i}/{n}", flush=True)
    p.stdin.close(); p.wait()

if __name__ == "__main__":
    main()
