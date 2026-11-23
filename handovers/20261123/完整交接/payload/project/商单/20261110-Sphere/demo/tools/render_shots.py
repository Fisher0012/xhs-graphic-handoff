#!/usr/bin/env python3
"""Render Sphere 商单 14.4s style-demo graphic shots (1, 2, 19, 20).

1080x1920, 30fps, no audio. Look is matched to refs2/laomai_frames
and the production specs in refs2/laomai_breakdown.md + plan/script_v3.md §3 / §7.
"""
from __future__ import annotations

import argparse
import math
import os
import shutil
import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

# ---------------------------------------------------------------------------
# Paths & constants
# ---------------------------------------------------------------------------
ROOT = Path("/workspace/xhs/商单/20261110-Sphere/demo")
ASSETS = ROOT / "assets"
CLIPS = ROOT / "clips"
GRABS = ROOT / "grabs"
FRAMES = ROOT / "frames"
HTML = ROOT / "html"
REFS = Path("/workspace/xhs/商单/20261110-Sphere/refs2/laomai_frames")

W, H, FPS = 1080, 1920, 30
FONT_PATH = "/home/box/.fonts/NotoSansSC-Black.otf"

# Colours (spec + measured)
COL_HOOK_BG = (10, 10, 10)          # #0A0A0A
COL_GRID = (34, 34, 34)             # #222222
GRID_STEP = 40
COL_RED = (224, 0, 14)              # #E0000E
COL_WHITE = (255, 255, 255)
COL_CHALK = (254, 254, 254)         # #FEFEFE
COL_STROKE = (0, 0, 0)

# Hook title: spec 150 / 165 cannot fit 8-char line 2 on 1080px.
# Preserve the 150:165 ratio and scale so line 2 has ~44px side margins.
LINE1_SIZE = 114
LINE2_SIZE = 125
LINE1_TEXT = "金融人做IP"
LINE2_TEXT = "卡住你的不是剪辑"
# Title block visual centre on the hook (slightly above frame centre).
TITLE_CX, TITLE_CY = W // 2, 860
# Shot 2: shrink to 60%, move up.
SHOT2_SCALE = 0.60
SHOT2_CY = 500
SHOT2_SHRINK_DUR = 0.35

# Subtitles (script 3.1 — the one intentional 9:16 change vs the reference)
SUB_SIZE = 80
SUB_STROKE = 9
SUB_BOTTOM_Y = 1600          # text lower edge
SUB_TRACKING_EM = 0.02
SUB_FADE = 0.10
SUB_RISE = 6

# Badge / chapter tag
BADGE_TEXT = "合作内容 · 工具演示，不构成投资建议"
BADGE_SIZE = 30
BADGE_ALPHA = 0.55
BADGE_Y = 200
TAG_TEXT = "③ 出镜"
TAG_SIZE = 44
TAG_ALPHA = 0.70
TAG_Y = 200

CHAPTER_TEXT = "3 出镜"
CHAPTER_SIZE = 200
CHAPTER_CY = 1290
CHAPTER_WRITE = 0.25

BOX_LABELS = ("选题", "合规", "出镜")
BOX_POP_START = 0.20
BOX_POP_GAP = 0.15
BOX_POP_DUR = 0.22

SHOT_DUR = {1: 2.8, 2: 1.1, 19: 1.2, 20: 2.8}

# Shot 20 subtitle split (two clauses over 2.8s)
SHOT20_CUT = 1.30


# ---------------------------------------------------------------------------
# Easing
# ---------------------------------------------------------------------------
def clamp(x, a=0.0, b=1.0):
    return a if x < a else b if x > b else x


def ease_out_cubic(t: float) -> float:
    t = clamp(t)
    return 1.0 - (1.0 - t) ** 3


def ease_in_out(t: float) -> float:
    t = clamp(t)
    return 3 * t * t - 2 * t * t * t


def ease_css(t: float) -> float:
    """Approximate cubic-bezier(0.25, 0.10, 0.25, 1.00)."""
    t = clamp(t)
    # Close to ease / ease-out-ish
    return 1.0 - (1.0 - t) ** 2.6


# ---------------------------------------------------------------------------
# Font helpers
# ---------------------------------------------------------------------------
_font_cache: dict[tuple[int, str], ImageFont.FreeTypeFont] = {}


def font(size: int, path: str = FONT_PATH) -> ImageFont.FreeTypeFont:
    key = (size, path)
    if key not in _font_cache:
        _font_cache[key] = ImageFont.truetype(path, size)
    return _font_cache[key]


def text_ink_size(text: str, size: int, tracking_em: float = 0.0):
    """Return (width, height, per-char layout list of (ch, x, w))."""
    f = font(size)
    dummy = Image.new("L", (4, 4), 0)
    d = ImageDraw.Draw(dummy)
    sp = size * tracking_em
    layout = []
    x = 0.0
    max_h = 0
    min_top = 0
    # Use a generous temp image to get ink
    tmp = Image.new("L", (max(8, int(size * len(text) * 2) + 20), int(size * 3)), 0)
    td = ImageDraw.Draw(tmp)
    ox, oy = 10, int(size)
    cx = ox
    for i, ch in enumerate(text):
        td.text((cx, oy), ch, font=f, fill=255)
        w = d.textlength(ch, font=f)
        layout.append((ch, cx - ox, w))
        cx += w + (sp if i < len(text) - 1 else 0)
    ink = tmp.getbbox()
    if not ink:
        return 1, 1, layout, 0
    # ink relative to (ox, oy) origin of first baseline
    width = ink[2] - ink[0]
    height = ink[3] - ink[1]
    # x offset of ink left from start origin, y offset of ink top from oy
    x0 = ink[0] - ox
    y0 = ink[1] - oy
    return width, height, layout, (x0, y0, ox, oy, tmp, ink)


def render_text_mask(text: str, size: int, tracking_em: float = 0.0, scale: int = 2) -> tuple[Image.Image, tuple]:
    """Render white text on transparent, return (L mask cropped to ink, (x0,y0) ink offsets from baseline)."""
    f = font(size * scale)
    sp = size * scale * tracking_em
    # rough canvas
    canvas_w = int(size * scale * (len(text) + 2) + abs(sp) * len(text) + 40)
    canvas_h = int(size * scale * 3)
    img = Image.new("L", (canvas_w, canvas_h), 0)
    d = ImageDraw.Draw(img)
    ox, oy = 20, int(size * scale)
    x = float(ox)
    dummy = ImageDraw.Draw(Image.new("L", (4, 4)))
    for i, ch in enumerate(text):
        d.text((x, oy), ch, font=f, fill=255)
        x += dummy.textlength(ch, font=f) + (sp if i < len(text) - 1 else 0)
    ink = img.getbbox()
    if not ink:
        return Image.new("L", (1, 1), 0), (0, 0)
    cropped = img.crop(ink)
    x0 = ink[0] - ox
    y0 = ink[1] - oy  # typically negative
    return cropped, (x0, y0)


# ---------------------------------------------------------------------------
# Asset builders
# ---------------------------------------------------------------------------
def _inpaint_letters(bgr: np.ndarray) -> np.ndarray:
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    mask = (gray > 170).astype(np.uint8) * 255
    # Restrict to the title band, keep a generous pad
    mask[:560, :] = 0
    mask[880:, :] = 0
    mask = cv2.dilate(mask, np.ones((21, 21), np.uint8), iterations=1)
    # Also knock out any residual bright chalk flecks in the band? keep texture flecks.
    return cv2.inpaint(bgr, mask, 5, cv2.INPAINT_TELEA)



def build_chalkboard(out_w: int = 1200, out_h: int = 2100, seed: int = 7) -> Image.Image:
    """Synthesize a vertical chalkboard from the reference chapter-card textures.

    Low-frequency colour is a heavily blurred collage (kills tile seams);
    high-frequency chalk grain is overlap-blended from the real boards.
    """
    names = [
        "04_00-02.50_ch1_caveman.jpg",
        "15_00-27.17_ch2_taste.jpg",
        "23_00-48.93_ch3_playwright.jpg",
        "32_01-19.40_ch4_gsap.jpg",
        "38_01-39.03_ch5_hypit.jpg",
    ]
    clean_rgb = []
    for n in names:
        pth = REFS / n
        bgr = cv2.imread(str(pth))
        if bgr is None:
            raise FileNotFoundError(pth)
        rgb = cv2.cvtColor(_inpaint_letters(bgr), cv2.COLOR_BGR2RGB)
        clean_rgb.append(rgb)

    # Clean letter-free strips
    strips = []
    for rgb in clean_rgb:
        strips.append(rgb[:600])
        strips.append(rgb[860:])
    atlas = np.concatenate(strips, axis=0)
    ah, aw, _ = atlas.shape
    rng = np.random.RandomState(seed)

    # --- low frequency: smooth noise field (no strip-collage, so no banding) ---
    target = np.array([50.0, 50.0, 55.0], dtype=np.float32)
    # two octaves of very soft noise, heavily upsampled
    def soft_noise(scale, sigma, amp):
        hh, ww = max(8, out_h // scale), max(8, out_w // scale)
        n = rng.normal(0, 1, (hh, ww, 3)).astype(np.float32)
        n = cv2.resize(n, (out_w, out_h), interpolation=cv2.INTER_CUBIC)
        n = cv2.GaussianBlur(n, (0, 0), sigma)
        return n * amp
    base = np.zeros((out_h, out_w, 3), np.float32) + target
    base = base + soft_noise(16, 48, 10.0) + soft_noise(8, 22, 6.0)
    base = np.clip(base, 0, 255)

    # very soft large-scale wipes (low frequency only)
    for _ in range(8):
        cx = rng.randint(0, out_w)
        cy = rng.randint(0, out_h)
        rad = rng.randint(220, 520)
        strength = rng.uniform(5, 12) * (1 if rng.rand() < 0.5 else -1)
        y0, y1 = max(0, cy - rad), min(out_h, cy + rad)
        x0, x1 = max(0, cx - rad), min(out_w, cx + rad)
        yy, xx = np.ogrid[y0:y1, x0:x1]
        dist = np.sqrt((yy - cy) ** 2 + (xx - cx) ** 2)
        ang = np.arctan2(yy - cy, xx - cx)
        band = np.exp(-0.5 * ((dist - rad * rng.uniform(0.2, 0.65)) / (rad * 0.35)) ** 2)
        band *= 0.6 + 0.4 * np.cos(ang * rng.randint(1, 3) + rng.uniform(0, 6))
        # blur the band itself so no hard rings
        band_img = cv2.GaussianBlur(band.astype(np.float32), (0, 0), rad * 0.08)
        base[y0:y1, x0:x1] = np.clip(base[y0:y1, x0:x1] + strength * band_img[..., None], 0, 255)

    # --- high frequency grain from letter-free bands only, tiled with overlap
    # (using the inpainted letter band leaves ghost glyphs after resize)
    def grain_of(region):
        src = region.astype(np.float32)
        blur = cv2.GaussianBlur(src, (0, 0), 16)
        g = src - blur
        g = g.mean(axis=2)  # luminance, HxW
        return g

    # collect clean 1920-wide strips (top 600 + bottom ~220 of each card)
    strips = []
    for rgb in clean_rgb:
        strips.append(grain_of(rgb[:600]))
        if rgb.shape[0] > 860:
            strips.append(grain_of(rgb[860:]))

    # resize each strip to output width, then overlap-blend vertically
    acc = np.zeros((out_h, out_w), np.float32)
    wgt = np.zeros((out_h, out_w), np.float32)
    y = -30
    overlap = 120
    for i, st in enumerate(strips * 3):  # enough to cover 2100
        sh = int(round(st.shape[0] * (out_w / st.shape[1])))
        piece = cv2.resize(st, (out_w, sh), interpolation=cv2.INTER_AREA)
        if i % 2:
            piece = piece[:, ::-1]
        if i % 3 == 2:
            piece = piece[::-1]
        # 1-D vertical hann-like ramps on the overlap
        ramp = np.ones(sh, np.float32)
        ov = min(overlap, sh // 3)
        if ov > 1:
            ramp[:ov] = np.linspace(0, 1, ov)
            ramp[-ov:] = np.linspace(1, 0, ov)
        y0 = max(0, y)
        y1 = min(out_h, y + sh)
        if y1 > y0:
            py0 = y0 - y
            py1 = py0 + (y1 - y0)
            acc[y0:y1] += piece[py0:py1] * ramp[py0:py1, None]
            wgt[y0:y1] += ramp[py0:py1, None]
        y += sh - overlap
        if y >= out_h:
            break
    grain = (acc / np.maximum(wgt, 1e-6))[..., None]
    tex = np.clip(base + grain * 1.35, 0, 255)

        # fine dust / flecks
    dust = rng.normal(0, 1.8, tex.shape)
    fleck = rng.rand(out_h, out_w) > 0.9968
    tex = np.clip(tex + dust + fleck[..., None] * 16, 0, 255)

    # mild vignette
    ys = np.linspace(-1, 1, out_h)[:, None]
    xs = np.linspace(-1, 1, out_w)[None, :]
    r = np.sqrt((xs * 0.85) ** 2 + (ys * 0.9) ** 2)
    vig = 1.0 - 0.18 * np.clip((r - 0.55) / 0.7, 0, 1) ** 1.4
    tex = np.clip(tex * vig[..., None], 0, 255)
    return Image.fromarray(tex.astype(np.uint8), "RGB")


def build_grid(w: int = W, h: int = H, step: int = GRID_STEP) -> Image.Image:
    arr = np.zeros((h, w, 3), np.uint8)
    arr[:] = COL_HOOK_BG
    # 1px grid lines. Draw on integer step coordinates.
    arr[0:h:step, :] = COL_GRID
    arr[:, 0:w:step] = COL_GRID
    return Image.fromarray(arr, "RGB")


def _metallic_gradient(h: int, w: int) -> np.ndarray:
    """Vertical metal sheen: #FFFFFF → #E8E8E8 → ~#C8C8C8, plus a soft top flare."""
    grad = np.zeros((h, w, 3), np.float32)
    for y in range(h):
        t = y / max(h - 1, 1)
        if t < 0.42:
            u = t / 0.42
            c = 255 - u * 23  # 255 → 232 (#E8E8E8)
        else:
            u = (t - 0.42) / 0.58
            c = 232 - u * 30  # 232 → 202 (measured bottom of ref glyphs)
        grad[y, :] = c
    # soft horizontal highlight in the upper third
    flare = np.clip(1.0 - np.abs(np.linspace(-0.3, 1.4, h)) * 1.1, 0, 1)[:, None, None]
    grad = np.clip(grad + flare * 8, 0, 255)
    return grad


def render_metallic_line(text: str, size: int, tracking_em: float = 0.02) -> Image.Image:
    """Transparent RGBA glyph line with metal gradient fill and soft drop shadow."""
    mask, _ = render_text_mask(text, size, tracking_em=tracking_em, scale=2)
    mh, mw = mask.size[1], mask.size[0]
    grad = _metallic_gradient(mh, mw)
    alpha = np.array(mask, np.float32) / 255.0
    rgb = grad * alpha[..., None]
    # slight unsharp so edges read like the reference
    rgba = np.dstack([rgb, alpha * 255]).astype(np.uint8)
    glyph = Image.fromarray(rgba, "RGBA")
    # down to target size (we rendered at 2x)
    tw, th = mw // 2, mh // 2
    glyph = glyph.resize((tw, th), Image.Resampling.LANCZOS)

    # soft drop shadow
    pad = 24
    canvas = Image.new("RGBA", (tw + pad * 2, th + pad * 2), (0, 0, 0, 0))
    shadow = glyph.split()[-1]
    sh = Image.new("RGBA", glyph.size, (0, 0, 0, 0))
    sh_arr = np.zeros((th, tw, 4), np.uint8)
    sh_arr[..., 3] = np.array(shadow) * 0  # fill below
    # build shadow from alpha
    sh_img = Image.new("RGBA", glyph.size, (0, 0, 0, 0))
    sh_img.putalpha(shadow)
    # colour it black
    black = Image.new("RGBA", glyph.size, (0, 0, 0, 255))
    sh_img = Image.composite(black, Image.new("RGBA", glyph.size, (0, 0, 0, 0)), shadow)
    sh_img = sh_img.filter(ImageFilter.GaussianBlur(5))
    # reduce alpha
    r, g, b, a = sh_img.split()
    a = a.point(lambda v: int(v * 0.55))
    sh_img = Image.merge("RGBA", (r, g, b, a))
    canvas.paste(sh_img, (pad, pad + 4), sh_img)
    canvas.paste(glyph, (pad, pad), glyph)
    # crop back to a tight box plus a little padding for the shadow
    bbox = canvas.getbbox()
    if bbox:
        canvas = canvas.crop(bbox)
    return canvas


def _nibble_mask(mask: np.ndarray, rng: np.random.RandomState, amount: float = 0.012) -> np.ndarray:
    """Eat irregular bites out of a binary (0-255) mask to mimic worn stencil edges."""
    m = mask.copy()
    h, w = m.shape
    # noise threshold around the edge
    edges = cv2.Canny(m, 40, 120)
    edges = cv2.dilate(edges, np.ones((3, 3), np.uint8))
    noise = rng.rand(h, w)
    # randomly erode edge pixels
    eat = (edges > 0) & (noise < 0.35)
    m[eat] = 0
    # a few larger chips
    n_chips = int(max(8, amount * h * w / 40))
    ys, xs = np.where(edges > 0)
    if len(ys):
        for _ in range(n_chips):
            i = rng.randint(0, len(ys))
            cy, cx = int(ys[i]), int(xs[i])
            rad = rng.randint(1, 5)
            cv2.circle(m, (cx, cy), rad, 0, -1)
    # occasional interior pinholes (stencil wear)
    ys2, xs2 = np.where(m > 200)
    if len(ys2):
        for _ in range(max(3, len(ys2) // 18000)):
            i = rng.randint(0, len(ys2))
            cv2.circle(m, (int(xs2[i]), int(ys2[i])), rng.randint(1, 3), 0, -1)
    return m


def _stencil_bridges(mask: np.ndarray, rng: np.random.RandomState) -> np.ndarray:
    """Cut a few thin bridges through enclosed counters — classic stencil look."""
    m = mask.copy()
    # find holes via inverted contours
    inv = np.where(m > 128, 0, 255).astype(np.uint8)
    # don't treat the outside as a hole: flood-fill corners
    ff = inv.copy()
    h, w = ff.shape
    for seed in ((0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)):
        if ff[seed[1], seed[0]] == 255:
            cv2.floodFill(ff, None, seed, 0)
    # remaining white = counters
    cnts, _ = cv2.findContours(ff, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in cnts:
        area = cv2.contourArea(c)
        if area < 80 or area > (h * w * 0.25):
            continue
        M = cv2.moments(c)
        if M["m00"] == 0:
            continue
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        # cut a short horizontal or vertical gap from the hole outward
        if rng.rand() < 0.7:
            # horizontal cut through this hole to the nearest outside on one side
            direction = 1 if rng.rand() < 0.5 else -1
            y = cy + rng.randint(-2, 3)
            y = clamp(y, 1, h - 2)
            x = cx
            thick = rng.randint(2, 5)
            steps = 0
            while 0 < x < w - 1 and steps < w:
                m[int(y) - thick // 2 : int(y) + thick // 2 + 1, int(x)] = 0
                if mask[int(y), int(x)] < 128 and steps > 6:
                    # reached the outside after leaving the stroke
                    # only break once we've gone through the ring
                    # (if still in the hole at the start, keep going)
                    # detect: we were in the ring (mask high) and now low again after a high run
                    pass
                x += direction
                steps += 1
                # stop shortly after exiting the black ring back to empty
                if steps > 8 and m[int(clamp(y, 0, h - 1)), int(clamp(x, 0, w - 1))] == 0 and mask[int(y), int(clamp(x - direction, 0, w - 1))] < 128:
                    # messy; just limit length
                    if steps > 18:
                        break
            # cap length
    return m


def render_chalk_stencil(text: str, size: int, tracking_em: float = 0.04, mild: bool = False) -> Image.Image:
    """Worn stencil / chalk letters in #FEFEFE, slightly beveled, with a contact shadow."""
    rng = np.random.RandomState(11 + sum(map(ord, text)))
    mask, _ = render_text_mask(text, size, tracking_em=tracking_em, scale=2)
    m = np.array(mask)
    # slight blur then re-threshold to round corners a touch (less 'digital')
    m = cv2.GaussianBlur(m, (3, 3), 0)
    m = np.where(m > 80, 255, 0).astype(np.uint8)
    if not mild:
        m = _stencil_bridges(m, rng)
        m = _nibble_mask(m, rng, amount=0.014)
    else:
        m = _nibble_mask(m, rng, amount=0.004)
    # chalk grain: modulate alpha and value
    h, w = m.shape
    grain = rng.normal(0, 14, (h, w))
    alpha = np.clip(m.astype(np.float32) + grain * (m > 40), 0, 255)
    # fill colour with mild variation, slight top highlight
    yy = np.linspace(0, 1, h)[:, None]
    val = 254 - yy * 8 + rng.normal(0, 2.2, (h, w))  # top a bit brighter
    val = np.clip(val, 236, 255)
    rgb = np.dstack([val, val, val + 0.4])  # barely cool-white, close to measured 253,254,255
    rgb = np.clip(rgb, 0, 255)
    rgba = np.dstack([rgb, alpha]).astype(np.uint8)
    glyph = Image.fromarray(rgba, "RGBA")
    tw, th = w // 2, h // 2
    glyph = glyph.resize((tw, th), Image.Resampling.LANCZOS)

    pad = 28
    canvas = Image.new("RGBA", (tw + pad * 2, th + pad * 2), (0, 0, 0, 0))
    # contact shadow (soft, downward) — letters sitting on the board
    shadow = glyph.split()[-1]
    sh = Image.new("RGBA", glyph.size, (0, 0, 0, 255))
    sh.putalpha(shadow)
    sh = sh.filter(ImageFilter.GaussianBlur(3))
    r, g, b, a = sh.split()
    a = a.point(lambda v: int(v * 0.45))
    sh = Image.merge("RGBA", (r, g, b, a))
    canvas.paste(sh, (pad, pad + 3), sh)
    canvas.paste(glyph, (pad, pad), glyph)
    bbox = canvas.getbbox()
    if bbox:
        canvas = canvas.crop(bbox)
    return canvas


# ---- chalk-stroke drawing (icons, boxes, red strikes) --------------------
def _brush_stamp(radius: int, hardness: float, rng: np.random.RandomState) -> np.ndarray:
    d = radius * 2 + 1
    yy, xx = np.ogrid[-radius : radius + 1, -radius : radius + 1]
    dist = np.sqrt(xx * xx + yy * yy) / max(radius, 1)
    alpha = np.clip(1.0 - dist, 0, 1)
    # harder core
    alpha = np.clip((alpha - (1 - hardness)) / max(hardness, 1e-4), 0, 1)
    # grain
    alpha = np.clip(alpha * (0.75 + 0.25 * rng.rand(d, d)), 0, 1)
    # punch a few holes so it looks like chalk, not ink
    punch = rng.rand(d, d) > 0.93
    alpha = alpha * (~punch)
    return alpha.astype(np.float32)


def stamp(rgba: np.ndarray, x: float, y: float, brush: np.ndarray, color, strength: float = 1.0):
    h, w = rgba.shape[:2]
    bh, bw = brush.shape
    x0 = int(round(x)) - bw // 2
    y0 = int(round(y)) - bh // 2
    x1, y1 = x0 + bw, y0 + bh
    sx0 = max(0, -x0)
    sy0 = max(0, -y0)
    sx1 = bw - max(0, x1 - w)
    sy1 = bh - max(0, y1 - h)
    dx0, dy0 = max(0, x0), max(0, y0)
    dx1, dy1 = min(w, x1), min(h, y1)
    if dx1 <= dx0 or dy1 <= dy0:
        return
    b = brush[sy0:sy1, sx0:sx1] * strength
    dest = rgba[dy0:dy1, dx0:dx1].astype(np.float32)
    a = np.clip(b, 0, 1)[..., None]
    col = np.array(color, np.float32).reshape(1, 1, 3)
    out_rgb = dest[..., :3] * (1 - a) + col * a
    out_a = dest[..., 3:4] + (255 - dest[..., 3:4]) * a
    dest[..., :3] = out_rgb
    dest[..., 3:4] = out_a
    rgba[dy0:dy1, dx0:dx1] = np.clip(dest, 0, 255).astype(np.uint8)


def chalk_polyline(rgba, pts, width, color, rng, roughness=0.45, strength=0.9):
    """Stroke a polyline with a chalky brush."""
    if len(pts) < 2:
        return
    # densify
    dense = []
    for i in range(len(pts) - 1):
        x0, y0 = pts[i]
        x1, y1 = pts[i + 1]
        dist = math.hypot(x1 - x0, y1 - y0)
        n = max(1, int(dist / max(1.0, width * 0.35)))
        for k in range(n):
            t = k / n
            dense.append((x0 + (x1 - x0) * t, y0 + (y1 - y0) * t))
    dense.append(tuple(pts[-1]))
    radius = max(1, int(round(width / 2)))
    for i, (x, y) in enumerate(dense):
        # local radius jitter
        r = max(1, int(round(radius * (0.75 + 0.5 * rng.rand()))))
        # occasional skip for broken chalk
        if rng.rand() < 0.03 * roughness:
            continue
        # positional jitter
        jx = rng.normal(0, roughness * 0.6)
        jy = rng.normal(0, roughness * 0.6)
        brush = _brush_stamp(r, hardness=0.55 + rng.rand() * 0.3, rng=rng)
        st = strength * (0.75 + 0.25 * rng.rand())
        stamp(rgba, x + jx, y + jy, brush, color, st)


def rounded_rect_path(x, y, w, h, r, n_arc=8):
    r = min(r, w / 2, h / 2)
    pts = []
    # start mid-top, go clockwise
    def arc(cx, cy, a0, a1):
        for i in range(n_arc + 1):
            a = a0 + (a1 - a0) * (i / n_arc)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))

    arc(x + w - r, y + r, -math.pi / 2, 0)
    arc(x + w - r, y + h - r, 0, math.pi / 2)
    arc(x + r, y + h - r, math.pi / 2, math.pi)
    arc(x + r, y + r, math.pi, 3 * math.pi / 2)
    pts.append(pts[0])
    return pts


def render_chalk_box_frame(w: int, h: int, radius: int = 22, stroke: int = 5) -> Image.Image:
    rng = np.random.RandomState(21)
    rgba = np.zeros((h + 20, w + 20, 4), np.uint8)
    pts = rounded_rect_path(10, 10, w, h, radius)
    chalk_polyline(rgba, pts, stroke, COL_CHALK, rng, roughness=0.5, strength=0.95)
    # a second slightly offset pass for chalk build-up
    pts2 = [(p[0] + rng.uniform(-0.6, 0.6), p[1] + rng.uniform(-0.6, 0.6)) for p in pts]
    chalk_polyline(rgba, pts2, max(2, stroke - 2), (245, 245, 245), rng, roughness=0.7, strength=0.45)
    return Image.fromarray(rgba, "RGBA")


def render_camera_icon(size: int = 400) -> Image.Image:
    rng = np.random.RandomState(3)
    s = size
    rgba = np.zeros((s, s, 4), np.uint8)
    w = 13.0
    col = COL_CHALK
    # body
    bx, by, bw, bh = s * 0.16, s * 0.34, s * 0.50, s * 0.40
    chalk_polyline(rgba, rounded_rect_path(bx, by, bw, bh, 16), w, col, rng)
    # lens (two circles) on the right of the body
    cx, cy, r = s * 0.78, s * 0.54, s * 0.20
    n = 56
    circle = [(cx + r * math.cos(2 * math.pi * i / n), cy + r * math.sin(2 * math.pi * i / n)) for i in range(n + 1)]
    chalk_polyline(rgba, circle, w, col, rng)
    r2 = r * 0.55
    circle2 = [(cx + r2 * math.cos(2 * math.pi * i / n), cy + r2 * math.sin(2 * math.pi * i / n)) for i in range(n + 1)]
    chalk_polyline(rgba, circle2, w * 0.8, col, rng)
    # viewfinder bump on top of body
    vx, vy, vw, vh = s * 0.28, s * 0.22, s * 0.22, s * 0.14
    chalk_polyline(rgba, rounded_rect_path(vx, vy, vw, vh, 6), w * 0.85, col, rng)
    # a small record button
    rx, ry, rr = s * 0.22, s * 0.42, s * 0.035
    circ3 = [(rx + rr * math.cos(2 * math.pi * i / 20), ry + rr * math.sin(2 * math.pi * i / 20)) for i in range(21)]
    chalk_polyline(rgba, circ3, 4, col, rng)
    # short handle / grip line under body
    chalk_polyline(rgba, [(s * 0.22, s * 0.76), (s * 0.22, s * 0.86), (s * 0.48, s * 0.86)], w * 0.8, col, rng)
    img = Image.fromarray(rgba, "RGBA")
    # crop tight with padding
    bbox = img.getbbox()
    if bbox:
        pad = 12
        img = img.crop((max(0, bbox[0] - pad), max(0, bbox[1] - pad), min(s, bbox[2] + pad), min(s, bbox[3] + pad)))
    return img


def render_clock_icon(size: int = 400) -> Image.Image:
    rng = np.random.RandomState(5)
    s = size
    rgba = np.zeros((s, s, 4), np.uint8)
    w = 13.0
    col = COL_CHALK
    cx = cy = s * 0.50
    r = s * 0.36
    n = 64
    circle = [(cx + r * math.cos(2 * math.pi * i / n), cy + r * math.sin(2 * math.pi * i / n)) for i in range(n + 1)]
    chalk_polyline(rgba, circle, w, col, rng)
    # 12 ticks
    for i in range(12):
        a = -math.pi / 2 + i * math.pi / 6
        inner = r * (0.78 if i % 3 == 0 else 0.86)
        outer = r * 0.96
        p0 = (cx + inner * math.cos(a), cy + inner * math.sin(a))
        p1 = (cx + outer * math.cos(a), cy + outer * math.sin(a))
        chalk_polyline(rgba, [p0, p1], 5 if i % 3 == 0 else 3.5, col, rng, roughness=0.35)
    # hour hand (pointing ~10) and minute hand (~2)
    def hand(angle, length, width):
        p0 = (cx - 0.08 * length * math.cos(angle), cy - 0.08 * length * math.sin(angle))
        p1 = (cx + length * math.cos(angle), cy + length * math.sin(angle))
        chalk_polyline(rgba, [p0, p1], width, col, rng, roughness=0.3)

    hand(-math.pi / 2 - math.pi / 3, r * 0.45, 6.5)  # 10 o'clock
    hand(-math.pi / 2 + math.pi / 3, r * 0.66, 5.0)  # 2 o'clock
    # centre cap
    rr = 6
    cap = [(cx + rr * math.cos(2 * math.pi * i / 16), cy + rr * math.sin(2 * math.pi * i / 16)) for i in range(17)]
    chalk_polyline(rgba, cap, 5, col, rng, strength=1.0)
    img = Image.fromarray(rgba, "RGBA")
    bbox = img.getbbox()
    if bbox:
        pad = 12
        img = img.crop((max(0, bbox[0] - pad), max(0, bbox[1] - pad), min(s, bbox[2] + pad), min(s, bbox[3] + pad)))
    return img


def render_red_strike(w: int, h: int, progress: float, seed: int = 9) -> Image.Image:
    """A slightly irregular diagonal chalk slash, drawn by `progress` 0..1."""
    rng = np.random.RandomState(seed)
    rgba = np.zeros((h, w, 4), np.uint8)
    # from upper-left to lower-right, inset
    p0 = (w * 0.08, h * 0.10)
    p1 = (w * 0.92, h * 0.90)
    # add a slight bow
    mid = ((p0[0] + p1[0]) / 2 + rng.uniform(-w * 0.04, w * 0.04),
           (p0[1] + p1[1]) / 2 + rng.uniform(-h * 0.04, h * 0.04))
    # densify quadratic bezier up to progress
    n = 48
    pts = []
    end = max(2, int(n * clamp(progress)))
    for i in range(end + 1):
        t = i / n
        x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * mid[0] + t ** 2 * p1[0]
        y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * mid[1] + t ** 2 * p1[1]
        pts.append((x, y))
    chalk_polyline(rgba, pts, 14, COL_RED, rng, roughness=0.25, strength=1.0)
    chalk_polyline(rgba, pts, 10, COL_RED, rng, roughness=0.15, strength=1.0)
    # solid core so the red stays #E0000E on the dark board
    chalk_polyline(rgba, pts, 7, COL_RED, rng, roughness=0.08, strength=1.0)
    return Image.fromarray(rgba, "RGBA")


def paste_center(base: Image.Image, overlay: Image.Image, cx: int, cy: int, scale: float = 1.0, opacity: float = 1.0):
    if overlay.mode != "RGBA":
        overlay = overlay.convert("RGBA")
    if scale != 1.0:
        nw = max(1, int(overlay.width * scale))
        nh = max(1, int(overlay.height * scale))
        overlay = overlay.resize((nw, nh), Image.Resampling.LANCZOS)
    if opacity < 1.0:
        r, g, b, a = overlay.split()
        a = a.point(lambda v, o=opacity: int(v * o))
        overlay = Image.merge("RGBA", (r, g, b, a))
    x = int(round(cx - overlay.width / 2))
    y = int(round(cy - overlay.height / 2))
    base.paste(overlay, (x, y), overlay)
    return (x, y, overlay.width, overlay.height)


def make_assets(force: bool = False) -> dict[str, Path]:
    ASSETS.mkdir(parents=True, exist_ok=True)
    paths = {
        "chalkboard": ASSETS / "chalkboard.png",
        "grid": ASSETS / "grid.png",
        "title_l1": ASSETS / "title_l1.png",
        "title_l2": ASSETS / "title_l2.png",
        "chapter": ASSETS / "chapter_3_chujing.png",
        "box_frame": ASSETS / "box_frame.png",
        "icon_camera": ASSETS / "icon_camera.png",
        "icon_clock": ASSETS / "icon_clock.png",
        "box_选题": ASSETS / "box_label_选题.png",
        "box_合规": ASSETS / "box_label_合规.png",
        "box_出镜": ASSETS / "box_label_出镜.png",
    }
    if force or not paths["chalkboard"].exists():
        print("building chalkboard texture…")
        board = build_chalkboard(1200, 2100)
        board.save(paths["chalkboard"], "PNG")
        # also a tight 1080x1920 crop (centre)
        x0 = (board.width - W) // 2
        y0 = (board.height - H) // 2
        board.crop((x0, y0, x0 + W, y0 + H)).save(ASSETS / "chalkboard_1080x1920.png", "PNG")
    if force or not paths["grid"].exists():
        print("building grid…")
        build_grid().save(paths["grid"], "PNG")
    if force or not paths["title_l1"].exists():
        print("building metallic titles…")
        render_metallic_line(LINE1_TEXT, LINE1_SIZE, 0.02).save(paths["title_l1"], "PNG")
        render_metallic_line(LINE2_TEXT, LINE2_SIZE, 0.00).save(paths["title_l2"], "PNG")
        # 0 tracking on line 2 to help it fit; line 1 can keep 0.02em
    if force or not paths["chapter"].exists():
        print("building chapter stencil…")
        render_chalk_stencil(CHAPTER_TEXT, CHAPTER_SIZE, tracking_em=0.06).save(paths["chapter"], "PNG")
    if force or not paths["box_frame"].exists():
        print("building chalk boxes / icons…")
        render_chalk_box_frame(300, 200, radius=22, stroke=8).save(paths["box_frame"], "PNG")
        for lab in BOX_LABELS:
            render_chalk_stencil(lab, 78, tracking_em=0.04, mild=True).save(ASSETS / f"box_label_{lab}.png", "PNG")
        render_camera_icon(420).save(paths["icon_camera"], "PNG")
        render_clock_icon(420).save(paths["icon_clock"], "PNG")
    return paths


# ---------------------------------------------------------------------------
# Subtitle + badge
# ---------------------------------------------------------------------------
def draw_subtitle(base: Image.Image, text: str, fade: float = 1.0, rise: float = 0.0):
    """White Heavy 80px, 9px black stroke, bottom edge at y=1600, fade 0..1, rise in px."""
    if fade <= 0 or not text:
        return
    f = font(SUB_SIZE)
    # measure with tracking
    sp = SUB_SIZE * SUB_TRACKING_EM
    dummy = ImageDraw.Draw(Image.new("L", (4, 4)))
    widths = [dummy.textlength(ch, font=f) for ch in text]
    total = sum(widths) + sp * max(0, len(text) - 1)
    # ink height ~80
    pad = SUB_STROKE + 8
    tw, th = int(math.ceil(total)) + pad * 2, SUB_SIZE + pad * 2 + 20
    layer = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    # baseline: we want the visual lower edge of the glyphs (not including stroke
    # hanging below) at a known y. We'll render then place by ink box.
    x = float(pad)
    y_base = pad + 4
    # stroke then fill (paint-order: stroke fill)
    offsets = []
    for i in range(32):
        a = 2 * math.pi * i / 32
        offsets.append((round(SUB_STROKE * math.cos(a)), round(SUB_STROKE * math.sin(a))))
    # unique integer offsets plus axis-aligned for a tight disc
    for dx in range(-SUB_STROKE, SUB_STROKE + 1):
        for dy in range(-SUB_STROKE, SUB_STROKE + 1):
            if dx * dx + dy * dy <= SUB_STROKE * SUB_STROKE + 1:
                offsets.append((dx, dy))
    offsets = list(set(offsets))
    # draw each char
    def draw_chars(fill, shift=(0, 0)):
        cx = x + shift[0]
        for i, ch in enumerate(text):
            d.text((cx, y_base + shift[1]), ch, font=f, fill=fill)
            cx += widths[i] + (sp if i < len(text) - 1 else 0)

    draw_chars((0, 0, 0, 255))  # we'll stamp stroke by drawing black at offsets
    # redo properly
    layer = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for off in offsets:
        draw_chars((0, 0, 0, 255), off)
    draw_chars((255, 255, 255, 255), (0, 0))

    if fade < 1.0:
        r, g, b, a = layer.split()
        a = a.point(lambda v, o=fade: int(v * o))
        layer = Image.merge("RGBA", (r, g, b, a))
    ink = layer.getbbox()
    if not ink:
        return
    # Place so the FILL's lower edge (approx ink bottom minus stroke) sits at SUB_BOTTOM_Y
    # ink includes the 9px stroke, so visual fill bottom ≈ ink[3] - SUB_STROKE
    fill_bottom_local = ink[3] - SUB_STROKE
    dest_y = SUB_BOTTOM_Y - fill_bottom_local - int(round(rise))
    dest_x = (W - tw) // 2
    base.paste(layer, (dest_x, dest_y), layer)


def draw_badge(base: Image.Image):
    f = font(BADGE_SIZE)
    # right-aligned, vertical centre at y=200
    dummy = ImageDraw.Draw(Image.new("L", (4, 4)))
    tw = dummy.textlength(BADGE_TEXT, font=f)
    # ink height ~33 at 30px
    layer = Image.new("RGBA", (int(tw) + 8, BADGE_SIZE + 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.text((4, 2), BADGE_TEXT, font=f, fill=(255, 255, 255, int(255 * BADGE_ALPHA)))
    ink = layer.getbbox() or (0, 0, layer.width, layer.height)
    # vertical centre of ink at BADGE_Y, right margin 48
    dest_x = W - 48 - ink[2]
    dest_y = BADGE_Y - (ink[1] + ink[3]) // 2
    base.paste(layer, (dest_x, dest_y), layer)


def draw_chapter_tag(base: Image.Image):
    f = font(TAG_SIZE)
    dummy = ImageDraw.Draw(Image.new("L", (4, 4)))
    tw = dummy.textlength(TAG_TEXT, font=f)
    layer = Image.new("RGBA", (int(tw) + 8, TAG_SIZE + 20), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.text((4, 2), TAG_TEXT, font=f, fill=(255, 255, 255, int(255 * TAG_ALPHA)))
    ink = layer.getbbox() or (0, 0, layer.width, layer.height)
    dest_x = 48
    dest_y = TAG_Y - (ink[1] + ink[3]) // 2
    base.paste(layer, (dest_x, dest_y), layer)


# ---------------------------------------------------------------------------
# Shot drawing
# ---------------------------------------------------------------------------
class Assets:
    def __init__(self, paths: dict[str, Path]):
        self.grid = Image.open(paths["grid"]).convert("RGB")
        self.board_big = Image.open(paths["chalkboard"]).convert("RGB")
        self.board = Image.open(ASSETS / "chalkboard_1080x1920.png").convert("RGB")
        self.l1 = Image.open(paths["title_l1"]).convert("RGBA")
        self.l2 = Image.open(paths["title_l2"]).convert("RGBA")
        self.chapter = Image.open(paths["chapter"]).convert("RGBA")
        self.box_frame = Image.open(paths["box_frame"]).convert("RGBA")
        self.box_labels = {lab: Image.open(ASSETS / f"box_label_{lab}.png").convert("RGBA") for lab in BOX_LABELS}
        self.cam = Image.open(paths["icon_camera"]).convert("RGBA")
        self.clock = Image.open(paths["icon_clock"]).convert("RGBA")
        # Precompute title group metrics (the two lines as a stack)
        # gap between ink boxes
        self.gap = 72
        self.group_h = self.l1.height + self.gap + self.l2.height
        # Each metallic PNG includes shadow padding; visual centres ≈ image centres.


def title_positions(cy: float, scale: float, A: Assets):
    """Return (l1_cx, l1_cy, l2_cx, l2_cy, scale) for a stack centred at (TITLE_CX, cy)."""
    gh = A.group_h * scale
    top = cy - gh / 2
    l1_cy = top + A.l1.height * scale / 2
    l2_cy = top + A.l1.height * scale + A.gap * scale + A.l2.height * scale / 2
    return TITLE_CX, l1_cy, TITLE_CX, l2_cy, scale


def paste_title(base, A: Assets, cy: float, scale: float = 1.0, opacity: float = 1.0):
    l1x, l1y, l2x, l2y, s = title_positions(cy, scale, A)
    paste_center(base, A.l1, int(l1x), int(l1y), s, opacity)
    paste_center(base, A.l2, int(l2x), int(l2y), s, opacity)
    return l1x, l1y, l2x, l2y, s



def _slice_layer(title_rgba: Image.Image, y0, y1, xoff, rgb_shift, canvas_w, canvas_h, dest_x, dest_y):
    """Copy a horizontal band of the title, with true additive RGB split, onto a canvas-sized layer."""
    y0i, y1i = max(0, int(y0)), min(title_rgba.height, int(y1))
    if y1i <= y0i:
        return Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    band = np.array(title_rgba.crop((0, y0i, title_rgba.width, y1i)), np.float32)
    bh, bw = band.shape[:2]
    layer = np.zeros((canvas_h, canvas_w, 4), np.float32)
    shift = int(round(rgb_shift)) if rgb_shift else 0
    dx = int(round(dest_x + xoff))
    dy = int(round(dest_y + y0i))

    def blit_channel(src, ch, x_shift, only_ch=True):
        x = dx + x_shift
        y = dy
        # src is bh x bw x 4
        sx0, sy0 = 0, 0
        dx0, dy0 = x, y
        dx1, dy1 = x + bw, y + bh
        # clip to canvas
        if dx0 < 0:
            sx0 = -dx0
            dx0 = 0
        if dy0 < 0:
            sy0 = -dy0
            dy0 = 0
        if dx1 > canvas_w:
            dx1 = canvas_w
        if dy1 > canvas_h:
            dy1 = canvas_h
        if dx1 <= dx0 or dy1 <= dy0:
            return
        sx1 = sx0 + (dx1 - dx0)
        sy1 = sy0 + (dy1 - dy0)
        sl = src[sy0:sy1, sx0:sx1]
        dest = layer[dy0:dy1, dx0:dx1]
        a = sl[..., 3:4] / 255.0
        if only_ch:
            dest[..., ch:ch+1] = dest[..., ch:ch+1] * (1 - a) + sl[..., ch:ch+1] * a
            dest[..., 3:4] = np.maximum(dest[..., 3:4], sl[..., 3:4])
        else:
            dest[..., :3] = dest[..., :3] * (1 - a) + sl[..., :3] * a
            dest[..., 3:4] = dest[..., 3:4] + (255 - dest[..., 3:4]) * a

    if shift and abs(shift) >= 1:
        # R left, G unshifted, B right — overlap stays near-white, fringes are red / cyan
        blit_channel(band, 0, -shift, True)
        blit_channel(band, 1, 0, True)
        blit_channel(band, 2, shift, True)
    else:
        blit_channel(band, 0, 0, False)

    return Image.fromarray(np.clip(layer, 0, 255).astype(np.uint8), "RGBA")


def compose_title_image(A: Assets) -> tuple[Image.Image, int, int]:
    """Single RGBA image of the two-line title stack (used for glitch slices)."""
    pad = 40
    w = max(A.l1.width, A.l2.width) + pad * 2
    h = A.group_h + pad * 2
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    paste_center(img, A.l1, w // 2, pad + A.l1.height // 2)
    paste_center(img, A.l2, w // 2, pad + A.l1.height + A.gap + A.l2.height // 2)
    return img, w, h


def apply_glitch(bg: Image.Image, A: Assets, t: float) -> Image.Image:
    """Hook glitch. Deterministic. t is time in shot 1."""
    out = bg.copy()
    title, tw, th = compose_title_image(A)
    dest_x = TITLE_CX - tw // 2
    dest_y = int(TITLE_CY - th / 2)

    rng = np.random.RandomState(20261110)

    # Pre-defined slices (y, h, rest_xoff, bar_color or None, fly_from)
    # y is in title-image space
    slices = []
    y = 0
    while y < th:
        hgt = int(rng.randint(10, 38))
        if y + hgt > th:
            hgt = th - y
        if hgt <= 0:
            break
        rest = int(rng.choice([-86, -54, -28, 0, 0, 24, 48, 78, 110]))
        kind = rng.choice(["title", "title", "title", "bar", "bar"])
        _colors = [(224, 0, 14), (0, 220, 200), (255, 255, 255), (224, 0, 14), (0, 200, 180)]
        color = _colors[int(rng.randint(0, len(_colors)))]
        fly = rng.choice([-1, 1]) * rng.randint(420, 820)
        slices.append((y, hgt, rest, kind, color, fly))
        y += hgt + int(rng.randint(0, 10))

    # Additional free-floating colour bars (not title-aligned)
    bars = []
    for _ in range(7):
        by = int(TITLE_CY + rng.randint(-280, 280))
        bh = int(rng.randint(8, 28))
        bw = int(rng.randint(90, 420))
        bx = TITLE_CX + int(rng.randint(-360, 200))
        _colors2 = [(224, 0, 14), (0, 220, 200), (255, 255, 255), (200, 40, 50)]
        color = _colors2[int(rng.randint(0, len(_colors2)))]
        fly = rng.choice([-1, 1]) * rng.randint(500, 900)
        bars.append((bx, by, bw, bh, color, fly))

    def motion_blur_bar(color, w, h, smear):
        img = Image.new("RGBA", (max(1, w + abs(smear)), h), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        # smear: draw several copies with falling alpha
        steps = max(1, abs(smear) // 6)
        for i in range(steps):
            a = int(220 * (1 - i / steps) ** 1.4)
            x = i * 6 if smear > 0 else img.width - w - i * 6
            d.rectangle([x, 0, x + w, h], fill=(*color, a))
        return img

    if t < 0.20:
        # Only flying RGB blocks, title not yet formed
        p = ease_out_cubic(t / 0.20)
        # slices as colour bars / title fragments flying into rest position
        for (y, hgt, rest, kind, color, fly) in slices:
            xoff = fly * (1 - p) + rest * 0.35
            # motion smear proportional to leftover distance
            smear = int((1 - p) * 80)
            if kind == "bar" or t < 0.10:
                bar = motion_blur_bar(color, int(tw * rng.uniform(0.25, 0.8)), hgt, smear if fly < 0 else -smear)
                # RGB fringe
                bx = dest_x + int(xoff)
                by = dest_y + y
                out.paste(bar, (bx, by), bar)
            else:
                # fragmentary title slice, heavy rgb split
                layer = _slice_layer(title, y, y + hgt, xoff, rgb_shift=6 + (1 - p) * 4,
                                     canvas_w=W, canvas_h=H, dest_x=dest_x, dest_y=dest_y)
                # fade in
                r, g, b, a = layer.split()
                a = a.point(lambda v, pp=p: int(v * (0.35 + 0.65 * pp)))
                layer = Image.merge("RGBA", (r, g, b, a))
                out = Image.alpha_composite(out.convert("RGBA"), layer).convert("RGB")
        for (bx, by, bw, bh, color, fly) in bars:
            xoff = fly * (1 - p)
            smear = int((1 - p) * 90)
            bar = motion_blur_bar(color, bw, bh, smear if fly < 0 else -smear)
            out.paste(bar, (int(bx + xoff), by), bar)
        return out

    if t < 0.50:
        p = ease_in_out((t - 0.20) / 0.30)  # 0 at 0.20, 1 at 0.50
        rgb_shift = 8 * (1 - p)
        # base title with RGB split
        if p > 0.05:
            base_title = _slice_layer(title, 0, th, 0, rgb_shift=rgb_shift,
                                      canvas_w=W, canvas_h=H, dest_x=dest_x, dest_y=dest_y)
            r, g, b, a = base_title.split()
            a = a.point(lambda v, pp=p: int(v * min(1.0, 0.4 + pp)))
            base_title = Image.merge("RGBA", (r, g, b, a))
            out = Image.alpha_composite(out.convert("RGBA"), base_title).convert("RGB")
        # displaced slices decaying to 0
        for i, (y, hgt, rest, kind, color, fly) in enumerate(slices):
            xoff = rest * (1 - p) ** 1.2
            if abs(xoff) < 1 and kind != "bar":
                continue
            if kind == "bar":
                fade = (1 - p) ** 1.5
                if fade < 0.05:
                    continue
                bar = motion_blur_bar(color, int(tw * 0.45), hgt, int((1 - p) * 30))
                r, g, b, a = bar.split()
                a = a.point(lambda v, f=fade: int(v * f))
                bar = Image.merge("RGBA", (r, g, b, a))
                out.paste(bar, (dest_x + int(xoff), dest_y + y), bar)
            else:
                layer = _slice_layer(title, y, y + hgt, xoff, rgb_shift=rgb_shift + 4 * (1 - p),
                                     canvas_w=W, canvas_h=H, dest_x=dest_x, dest_y=dest_y)
                out = Image.alpha_composite(out.convert("RGBA"), layer).convert("RGB")
        # residual free bars fade out quickly
        for (bx, by, bw, bh, color, fly) in bars:
            fade = max(0, 1 - p * 1.6)
            if fade <= 0:
                continue
            bar = motion_blur_bar(color, bw, bh, int(fade * 20))
            r, g, b, a = bar.split()
            a = a.point(lambda v, f=fade: int(v * f * 0.8))
            bar = Image.merge("RGBA", (r, g, b, a))
            out.paste(bar, (int(bx), by), bar)
        return out

    # Hold: clean metallic title
    paste_title(out, A, TITLE_CY, 1.0, 1.0)
    return out


def crop_board(A: Assets, zoom: float = 1.0, anchor_up: float = 0.02) -> Image.Image:
    """Ken Burns crop from the oversized chalkboard. zoom=1 is a 1080x1920 window."""
    big = A.board_big
    # window size in source pixels
    win_w = W / zoom
    win_h = H / zoom
    cx = big.width / 2
    cy = big.height / 2 - anchor_up * big.height
    x0 = cx - win_w / 2
    y0 = cy - win_h / 2
    # resample
    src = big.crop((int(x0), int(y0), int(x0 + win_w), int(y0 + win_h)))
    return src.resize((W, H), Image.Resampling.LANCZOS)


def draw_shot1(A: Assets, t: float) -> Image.Image:
    bg = A.grid.copy()
    frame = apply_glitch(bg, A, t)
    if frame.mode != "RGBA":
        frame = frame.convert("RGBA")
    # badge always-on (script: 全片常驻). On the hook it stays very quiet at 55%.
    draw_badge(frame)
    return frame.convert("RGB")


def draw_shot2(A: Assets, t: float) -> Image.Image:
    frame = A.grid.copy().convert("RGBA")
    # title shrink + rise
    p = ease_in_out(t / SHOT2_SHRINK_DUR)
    scale = 1.0 + (SHOT2_SCALE - 1.0) * p
    cy = TITLE_CY + (SHOT2_CY - TITLE_CY) * p
    paste_title(frame, A, cy, scale, 1.0)

    # three chalk boxes
    box_w, box_h = 300, 200
    gap = 28
    total = 3 * box_w + 2 * gap
    left = (W - total) // 2
    box_cy = 980
    for i, lab in enumerate(BOX_LABELS):
        t0 = BOX_POP_START + i * BOX_POP_GAP
        q = ease_out_cubic((t - t0) / BOX_POP_DUR)
        if q <= 0:
            continue
        sc = 0.92 + 0.08 * q
        op = q
        cx = left + i * (box_w + gap) + box_w // 2
        # frame
        paste_center(frame, A.box_frame, cx, box_cy, sc, op)
        # label
        paste_center(frame, A.box_labels[lab], cx, box_cy, sc, op)

    # subtitle
    fade = clamp(t / SUB_FADE)
    rise = SUB_RISE * (1 - fade)
    draw_subtitle(frame, "是这三道坎", fade, rise)
    draw_badge(frame)
    return frame.convert("RGB")


def draw_shot19(A: Assets, t: float) -> Image.Image:
    frame = crop_board(A, zoom=1.0).convert("RGBA")
    ch = A.chapter
    # left-to-right write-on over 250ms with a soft leading edge
    if t <= 0:
        # still empty
        draw_badge(frame)
        return frame.convert("RGB")
    p = clamp(t / CHAPTER_WRITE)
    if p < 1.0:
        # mask the chapter glyph
        w, h = ch.size
        mask = Image.new("L", (w, h), 0)
        md = ImageDraw.Draw(mask)
        # feathered leading edge ~48px
        reveal_w = int(w * p)
        feather = 48
        md.rectangle([0, 0, max(0, reveal_w - feather), h], fill=255)
        if reveal_w > 0:
            for x in range(max(0, reveal_w - feather), min(w, reveal_w + 1)):
                a = int(255 * (1 - (x - (reveal_w - feather)) / max(feather, 1)))
                a = max(0, min(255, a))
                md.line([(x, 0), (x, h)], fill=a)
        # apply additional mask to chapter alpha
        r, g, b, a = ch.split()
        a = ImageChops_multiply(a, mask)
        glyph = Image.merge("RGBA", (r, g, b, a))
    else:
        glyph = ch
    paste_center(frame, glyph, TITLE_CX, CHAPTER_CY, 1.0, 1.0)
    draw_badge(frame)
    return frame.convert("RGB")


def ImageChops_multiply(a: Image.Image, b: Image.Image) -> Image.Image:
    from PIL import ImageChops
    return ImageChops.multiply(a, b)


def draw_shot20(A: Assets, t: float) -> Image.Image:
    # Ken Burns 0 → 4% over the full 2.8s, in-out, anchor slightly up
    z = 1.0 + 0.04 * ease_in_out(t / SHOT_DUR[20])
    frame = crop_board(A, zoom=z, anchor_up=0.02).convert("RGBA")

    # icon positions in the main visual area
    cam_cx, cam_cy = 340, 900
    clk_cx, clk_cy = 740, 900
    icon_scale = 1.05
    paste_center(frame, A.cam, cam_cx, cam_cy, icon_scale, 1.0)
    paste_center(frame, A.clock, clk_cx, clk_cy, icon_scale, 1.0)

    # red strikes timed to subtitle cuts, 200ms draw-on
    def strike_progress(t0):
        return clamp((t - t0) / 0.20)

    # first strike (camera) just after first subtitle appears
    p1 = strike_progress(0.15)
    if p1 > 0:
        # size the strike to cover the icon
        sw, sh = int(A.cam.width * icon_scale * 1.15), int(A.cam.height * icon_scale * 1.15)
        strike = render_red_strike(sw, sh, p1, seed=11)
        paste_center(frame, strike, cam_cx, cam_cy, 1.0, 1.0)
    p2 = strike_progress(SHOT20_CUT + 0.08)
    if p2 > 0:
        sw, sh = int(A.clock.width * icon_scale * 1.15), int(A.clock.height * icon_scale * 1.15)
        strike = render_red_strike(sw, sh, p2, seed=17)
        paste_center(frame, strike, clk_cx, clk_cy, 1.0, 1.0)

    # subtitles
    if t < SHOT20_CUT:
        fade = clamp(t / SUB_FADE)
        rise = SUB_RISE * (1 - fade)
        draw_subtitle(frame, "第三道坎 出镜", fade, rise)
    else:
        fade = clamp((t - SHOT20_CUT) / SUB_FADE)
        rise = SUB_RISE * (1 - fade)
        draw_subtitle(frame, "不想露脸 也没空拍", fade, rise)

    draw_chapter_tag(frame)
    draw_badge(frame)
    return frame.convert("RGB")


DRAW = {1: draw_shot1, 2: draw_shot2, 19: draw_shot19, 20: draw_shot20}

# Representative grab times (after animations have settled / mid-hold)
GRAB_T = {1: 1.25, 2: 0.95, 19: 0.80, 20: 2.10}


def n_frames(dur: float) -> int:
    # Include the last tick so 2.8s at 30fps is frames 0..83 (84 frames = 2.8s)
    return int(round(dur * FPS))


def render_shot(shot: int, A: Assets, keep_frames: bool = False) -> Path:
    dur = SHOT_DUR[shot]
    nf = n_frames(dur)
    out_dir = FRAMES / f"shot{shot}"
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    drawer = DRAW[shot]
    print(f"rendering shot {shot}: {nf} frames ({dur}s)…")
    for i in range(nf):
        t = i / FPS
        frame = drawer(A, t)
        if frame.size != (W, H):
            frame = frame.resize((W, H), Image.Resampling.LANCZOS)
        frame.save(out_dir / f"f{i:04d}.png", "PNG", optimize=False)
        if i % 15 == 0 or i == nf - 1:
            print(f"  shot{shot}  {i+1}/{nf}")
    CLIPS.mkdir(parents=True, exist_ok=True)
    mp4 = CLIPS / f"shot{shot}.mp4"
    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", str(out_dir / "f%04d.png"),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-crf", "17",
        "-preset", "medium",
        "-movflags", "+faststart",
        "-an",
        str(mp4),
    ]
    print("encoding", mp4)
    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # frame grab
    GRABS.mkdir(parents=True, exist_ok=True)
    gi = min(nf - 1, int(round(GRAB_T[shot] * FPS)))
    grab = Image.open(out_dir / f"f{gi:04d}.png")
    grab.save(GRABS / f"shot{shot}.png", "PNG")
    # also grab a mid-glitch / mid-write frame for review
    extras = []
    if shot == 1:
        extras = [("shot1_glitch_00f", 3), ("shot1_glitch_0.25s", 8)]
    elif shot == 2:
        extras = [("shot2_mid_pop", 12)]
    elif shot == 19:
        extras = [("shot19_writeon", 5)]
    elif shot == 20:
        extras = [("shot20_first_strike", 12), ("shot20_first_sub", 20)]
    for name, idx in extras:
        idx = min(nf - 1, idx)
        Image.open(out_dir / f"f{idx:04d}.png").save(GRABS / f"{name}.png", "PNG")
    if not keep_frames:
        shutil.rmtree(out_dir)
    return mp4


def render_preview(A: Assets, times: dict[int, list[float]]):
    """Quick stills for iteration, no full clip encode."""
    GRABS.mkdir(parents=True, exist_ok=True)
    for shot, ts in times.items():
        drawer = DRAW[shot]
        for t in ts:
            frame = drawer(A, t)
            p = GRABS / f"preview_shot{shot}_{t:.2f}s.png"
            frame.save(p, "PNG")
            print("wrote", p)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force-assets", action="store_true")
    ap.add_argument("--preview", action="store_true", help="only write a few stills")
    ap.add_argument("--shots", default="1,2,19,20")
    ap.add_argument("--keep-frames", action="store_true")
    args = ap.parse_args()
    paths = make_assets(force=args.force_assets)
    A = Assets(paths)
    if args.preview:
        render_preview(A, {
            1: [0.00, 0.10, 0.20, 0.35, 0.55, 1.25],
            2: [0.00, 0.20, 0.40, 0.70, 1.00],
            19: [0.00, 0.08, 0.18, 0.40, 0.90],
            20: [0.00, 0.30, 1.20, 1.50, 2.40],
        })
        return
    shots = [int(s) for s in args.shots.split(",") if s.strip()]
    for s in shots:
        render_shot(s, A, keep_frames=args.keep_frames)
    print("done.")


if __name__ == "__main__":
    main()
