#!/usr/bin/env python3
"""Render shots 21 and 22 of the Sphere 14.4s style demo.

Layout and motion follow plan/script_v3.md shots 21–22 and
refs2/laomai_breakdown.md §7 (可复制的制作规范):

  - 9:16 1080×1920 chalkboard, same badge/subtitle style as render_shots.py
  - UI is upscaled with Lanczos from the 1920×1200 source and occupies
    most of the well between the module label and the subtitle
  - When a red box appears, the camera punches in (0.3s ease-in-out) so
    the boxed element plus its neighbourhood fill ~90% of the frame width
    at 1.6–2.2× (or tighter for small labels, to keep glyphs ≥ ~40px)
  - #E0000E 4px rounded red boxes sit on the target with even padding
  - 0.35s radial zoom-blur entry into shot 21
  - 0.4s 3D page-flip from the image dialog to the language dialog
  - hard cut to the reading dialog; the「香港」passage is Gaussian-blurred
  - 0.8s close-up of the「录制15秒即可完成克隆」card with a red circle
    centred on the real glyph box of「15秒」
"""
from __future__ import annotations

import math
import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, str(Path(__file__).resolve().parent))
import render_shots as rs

ROOT = rs.ROOT
STILLS = ROOT / "grabs" / "r4_stills"
CLIPS = rs.CLIPS
GRABS = rs.GRABS
W, H, FPS = rs.W, rs.H, rs.FPS
COL_RED = rs.COL_RED  # #E0000E

# Content well: between the module label (~y=200) and the subtitle (~y=1600)
WELL_TOP = 250
WELL_BOTTOM = 1480
WELL_H = WELL_BOTTOM - WELL_TOP
WELL_CX = W / 2.0
WELL_CY = (WELL_TOP + WELL_BOTTOM) / 2.0

SHOT21_DUR = 3.9
SHOT22_DUR = 2.6
ZOOM_DUR = 0.35
FLIP_DUR = 0.40
BOX_POP = 0.14
PUNCH_DUR = 0.30  # ease-in-out punch-in when a box appears / moves

S21_CUT = 1.40
S22_CUT = 1.08
S22_HARD_CUT = 1.10
S22_INSERT_AT = 1.80

# Source boxes on the 1920×1200 recording (tight, no pad)
AVATAR_DIALOG = (510, 367, 900, 512)
LANG_DIALOG = (560, 358, 800, 530)
READ_DIALOG = (560, 358, 800, 530)
BOX_UPLOADS = (528, 431, 427, 320)       # both 手机上传 / 从电脑上传 cards
BOX_REQ_CHIP = (561, 776, 157, 14)       # ink of 半身正面照，脸部清晰 + icon
BOX_MANDARIN = (580, 424, 373, 445)      # left 普通话 card
BOX_RECORD_BTN = (594, 774, 732, 46)     # full 开始录制 button
BOX_RECORD_LABEL = (920, 789, 80, 16)    # icon + 「开始录制」glyphs
PASSAGE = (575, 518, 770, 130)

# Overview: 创建声音 card. Subtitle and 「15秒」 measured in the card crop
# that starts at (270, 630).
VOICE_CARD = (270, 630, 410, 145)
# Content focus: title + plus icon + 「录制15秒即可完成克隆」
VOICE_FOCUS = (270 + 8, 630, 222, 145)   # x 278–500
# 「15秒」 in the 410-wide card crop (origin 270, 630): (115, 95, 26, 13)
SEC15_IN_CARD = (115, 95, 26, 13)
SUBTITLE_IN_CARD = (89, 95, 129, 13)     # 录制15秒即可完成克隆
SEC15_ABS = (270 + 115, 630 + 95, 26, 13)

# Even padding around a red box, in *frame* pixels
BOX_PAD_FRAME = 12
BOX_STROKE = 4
BOX_RADIUS = 12

# Dark fill when the camera runs off the screenshot
BACKDROP = (45, 45, 50)


def ease_in_out(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return 3 * t * t - 2 * t * t * t


def bezier_ease(t: float, x1=0.2, y1=0.7, x2=0.2, y2=1.0) -> float:
    """Used only for the 3D flip / zoom-blur (reference easing)."""
    t = max(0.0, min(1.0, t))
    u = t
    for _ in range(8):
        mt = 1.0 - u
        x = 3 * mt * mt * u * x1 + 3 * mt * u * u * x2 + u ** 3
        dx = 3 * mt * mt * x1 + 6 * mt * u * (x2 - x1) + 3 * u * u * (1.0 - x2)
        if abs(dx) < 1e-6:
            break
        u = max(0.0, min(1.0, u - (x - t) / dx))
    mt = 1.0 - u
    return 3 * mt * mt * u * y1 + 3 * mt * u * u * y2 + u ** 3


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def lerp_cam(a, b, t):
    t = ease_in_out(t)
    return (lerp(a[0], b[0], t), lerp(a[1], b[1], t), lerp(a[2], b[2], t))


def camera_for_box(box, min_glyph_src: float, fill: float = 0.90,
                   neigh: float = 0.18, min_pad_src: float = 40.0,
                   max_scale: float | None = None,
                   min_scale: float = 1.6) -> tuple[float, float, float]:
    """Return (scale, cx, cy) so box+neighbourhood fills `fill` of frame width.

    Scale is source→frame. Clamped so the padded box still fits in the
    frame, and boosted if the boxed label would render under ~40px.
    """
    x, y, w, h = box
    pad_x = max(min_pad_src, w * neigh)
    pad_y = max(min_pad_src * 0.6, h * neigh)
    ew = w + 2 * pad_x
    scale = (W * fill) / max(1.0, ew)
    if min_glyph_src > 0 and min_glyph_src * scale < 40.0:
        scale = 40.0 / min_glyph_src
    # the red box (element + frame pad) must fit
    fit = (W - 2 * BOX_PAD_FRAME - 8) / max(1.0, w)
    scale = min(scale, fit)
    if max_scale is not None:
        scale = min(scale, max_scale)
    # keep within the requested 1.6–2.2×-of-dialog-fit band when the
    # box is large enough; allow tighter zooms for small labels.
    # dialog-fit scale is ~1080/900 = 1.20, so 1.6–2.2× that is 1.92–2.64.
    scale = max(scale, min_scale)
    return scale, x + w / 2.0, y + h / 2.0


def camera_for_dialog(dialog, scale: float) -> tuple[float, float, float]:
    x, y, w, h = dialog
    return scale, x + w / 2.0, y + h / 2.0


# Precomputed cameras (scale, cx, cy)
# Uploads: two large cards — max scale that still fits the box ≈ 2.45
CAM_UPLOADS = camera_for_box(BOX_UPLOADS, min_glyph_src=15.0, fill=0.90,
                             neigh=0.10, min_pad_src=24.0, min_scale=2.15)
# Wide establishing view: a little looser than the punch, still large
CAM_AV_WIDE = (max(1.85, CAM_UPLOADS[0] * 0.78),
               (BOX_UPLOADS[0] + BOX_UPLOADS[2] / 2.0) + 40.0,  # peek at the photos
               BOX_UPLOADS[1] + BOX_UPLOADS[3] / 2.0)
CAM_REQ = camera_for_box(BOX_REQ_CHIP, min_glyph_src=14.0, fill=0.90,
                         neigh=0.35, min_pad_src=55.0, min_scale=3.2)
# Nudge right so the dialog's left edge (and the dark page beyond it)
# doesn't leave a empty slab; keep the chip near centre.
_req = list(CAM_REQ)
_req[1] = BOX_REQ_CHIP[0] + BOX_REQ_CHIP[2] / 2.0 + 18.0
CAM_REQ = tuple(_req)
CAM_MANDARIN = camera_for_box(BOX_MANDARIN, min_glyph_src=15.0, fill=0.90,
                             neigh=0.10, min_pad_src=24.0, min_scale=2.2)
# Flip / pre-punch: already large, full 普通话 card on screen, sliver of 粤语
CAM_LANG_WIDE = (
    2.20,
    BOX_MANDARIN[0] + BOX_MANDARIN[2] / 2.0 + 28.0,
    BOX_MANDARIN[1] + BOX_MANDARIN[3] / 2.0,
)
CAM_AV_FLIP = camera_for_dialog(AVATAR_DIALOG, 2.05)
# Punch in tight on「开始录制」so the blue button dominates; sit it
# slightly above the well centre with the instruction line below,
# cropping most of the empty / blurred passage above.
CAM_RECORD = (
    3.90,
    BOX_RECORD_LABEL[0] + BOX_RECORD_LABEL[2] / 2.0,
    BOX_RECORD_LABEL[1] + BOX_RECORD_LABEL[3] / 2.0 + 12.0,
)
CAM_READ_WIDE = (
    2.30,
    BOX_RECORD_BTN[0] + BOX_RECORD_BTN[2] / 2.0,
    BOX_RECORD_BTN[1] + BOX_RECORD_BTN[3] / 2.0 - 20.0,
)


def src_to_frame(box, cam):
    scale, cx, cy = cam
    x, y, w, h = box
    return (
        WELL_CX + (x - cx) * scale,
        WELL_CY + (y - cy) * scale,
        w * scale,
        h * scale,
    )


def padded_frame_box(src_box, cam, pad=BOX_PAD_FRAME):
    x, y, w, h = src_to_frame(src_box, cam)
    return (x - pad, y - pad, w + 2 * pad, h + 2 * pad)


def compose_camera(src_bgr: np.ndarray, cam, board: Image.Image) -> Image.Image:
    """Lanczos-upsample a camera window from the 1920×1200 source into the well."""
    scale, cx, cy = cam
    src_w = W / scale
    src_h = WELL_H / scale
    x0 = cx - src_w / 2.0
    y0 = cy - src_h / 2.0
    M = np.array([[scale, 0.0, -x0 * scale],
                  [0.0, scale, -y0 * scale]], dtype=np.float64)
    patch = cv2.warpAffine(
        src_bgr, M, (W, WELL_H),
        flags=cv2.INTER_LANCZOS4,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=BACKDROP,
    )
    patch_rgb = cv2.cvtColor(patch, cv2.COLOR_BGR2RGB)
    frame = board.copy()
    frame.paste(Image.fromarray(patch_rgb), (0, WELL_TOP))
    return frame


def draw_red_box(frame: Image.Image, box, progress=1.0, width=BOX_STROKE, radius=BOX_RADIUS):
    if progress <= 0:
        return
    x, y, w, h = box
    cx, cy = x + w / 2.0, y + h / 2.0
    sc = 0.92 + 0.08 * min(1.0, progress)
    w2, h2 = w * sc, h * sc
    x2, y2 = cx - w2 / 2.0, cy - h2 / 2.0
    layer = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    # keep the rect inside a small safety margin so a 4px stroke isn't clipped
    d.rounded_rectangle((x2, y2, x2 + w2, y2 + h2), radius=radius,
                        outline=(*COL_RED, 255), width=width)
    if frame.mode != "RGBA":
        tmp = frame.convert("RGBA")
        tmp.alpha_composite(layer)
        frame.paste(tmp.convert(frame.mode))
        return
    frame.alpha_composite(layer)


def draw_red_circle(frame: Image.Image, cx, cy, r, progress=1.0, width=BOX_STROKE):
    if progress <= 0:
        return
    sc = 0.92 + 0.08 * min(1.0, progress)
    r2 = r * sc
    layer = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    ImageDraw.Draw(layer).ellipse(
        (cx - r2, cy - r2, cx + r2, cy + r2),
        outline=(*COL_RED, 255), width=width,
    )
    if frame.mode != "RGBA":
        tmp = frame.convert("RGBA")
        tmp.alpha_composite(layer)
        frame.paste(tmp.convert(frame.mode))
        return
    frame.alpha_composite(layer)


def lerp_box(a, b, t):
    t = max(0.0, min(1.0, t))
    return tuple(a[i] + (b[i] - a[i]) * t for i in range(4))


def draw_module_label(base: Image.Image, text: str, size: int = 40):
    f = rs.font(size)
    dummy = ImageDraw.Draw(Image.new("L", (4, 4)))
    tw = dummy.textlength(text, font=f)
    layer = Image.new("RGBA", (int(tw) + 8, size + 20), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.text((4, 2), text, font=f, fill=(255, 255, 255, int(255 * rs.TAG_ALPHA)))
    ink = layer.getbbox() or (0, 0, layer.width, layer.height)
    dest_x = 48
    dest_y = rs.TAG_Y - (ink[1] + ink[3]) // 2
    base.paste(layer, (dest_x, dest_y), layer)


def finish_chrome(frame: Image.Image, label: str, subtitle: str, fade: float = 1.0) -> Image.Image:
    if frame.mode != "RGBA":
        frame = frame.convert("RGBA")
    rs.draw_badge(frame)
    draw_module_label(frame, label)
    if subtitle:
        rs.draw_subtitle(frame, subtitle, fade=fade, rise=0 if fade >= 1 else 6 * (1 - fade))
    return frame


def zoom_blur_bgr(img: np.ndarray, strength: float, samples: int = 14) -> np.ndarray:
    if strength <= 0.05:
        return img
    h, w = img.shape[:2]
    max_scale = 1.0 + 0.012 * strength
    acc = np.zeros_like(img, dtype=np.float32)
    for i in range(samples):
        t = i / (samples - 1)
        sc = 1.0 + (max_scale - 1.0) * t
        nw, nh = int(round(w * sc)), int(round(h * sc))
        resized = cv2.resize(img, (nw, nh), interpolation=cv2.INTER_LINEAR)
        x0 = (nw - w) // 2
        y0 = (nh - h) // 2
        acc += resized[y0:y0 + h, x0:x0 + w].astype(np.float32)
    return np.clip(acc / samples, 0, 255).astype(np.uint8)


def scale_about_center(img: np.ndarray, scale: float) -> np.ndarray:
    h, w = img.shape[:2]
    nw, nh = int(round(w * scale)), int(round(h * scale))
    resized = cv2.resize(img, (nw, nh), interpolation=cv2.INTER_LINEAR)
    if scale >= 1.0:
        x0 = (nw - w) // 2
        y0 = (nh - h) // 2
        return resized[y0:y0 + h, x0:x0 + w]
    canvas = np.zeros_like(img)
    x0 = (w - nw) // 2
    y0 = (h - nh) // 2
    canvas[y0:y0 + nh, x0:x0 + nw] = resized
    return canvas


def apply_zoom_blur(frame: Image.Image, t: float) -> Image.Image:
    if t >= ZOOM_DUR:
        return frame
    p = bezier_ease(t / ZOOM_DUR)
    strength = 20 * (1.0 - p)
    scale = 1.15 - 0.15 * p
    arr = cv2.cvtColor(np.array(frame.convert("RGB")), cv2.COLOR_RGB2BGR)
    arr = zoom_blur_bgr(arr, strength)
    arr = scale_about_center(arr, scale)
    return Image.fromarray(cv2.cvtColor(arr, cv2.COLOR_BGR2RGB))


def rotate_y_corners(w, h, angle_deg, perspective=1400.0):
    a = math.radians(angle_deg)
    cx, cy = w / 2.0, h / 2.0
    dst = []
    for x, y in ((0, 0), (w, 0), (w, h), (0, h)):
        x0 = x - cx
        z = x0 * math.sin(a)
        x1 = x0 * math.cos(a)
        denom = perspective + z
        if abs(denom) < 1:
            denom = 1 if denom >= 0 else -1
        sc = perspective / denom
        dst.append([cx + x1 * sc, cy + (y - cy) * sc])
    return np.array(dst, np.float32)


def warp_page(img_rgba: np.ndarray, angle_deg: float, perspective=1400.0) -> np.ndarray:
    h, w = img_rgba.shape[:2]
    src = np.array([[0, 0], [w, 0], [w, h], [0, h]], np.float32)
    dst = rotate_y_corners(w, h, angle_deg, perspective)
    M = cv2.getPerspectiveTransform(src, dst)
    return cv2.warpPerspective(
        img_rgba, M, (w, h), flags=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0),
    )


def blur_passage(im: Image.Image, box, radius: int = 20) -> Image.Image:
    out = im.copy()
    x, y, w, h = box
    region = out.crop((x, y, x + w, y + h)).filter(ImageFilter.GaussianBlur(radius=radius))
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, w - 1, h - 1), radius=16, fill=255)
    out.paste(region, (x, y), mask)
    return out


def dialog_layer(src_rgb: Image.Image, dialog, scale: float) -> Image.Image:
    """Transparent 1080×1920 layer with the dialog placed in the well at `scale`."""
    x, y, w, h = dialog
    pad = 28
    x0, y0 = max(0, x - pad), max(0, y - pad)
    x1, y1 = min(src_rgb.width, x + w + pad), min(src_rgb.height, y + h + pad)
    crop = src_rgb.crop((x0, y0, x1, y1))
    nw, nh = int(round((x1 - x0) * scale)), int(round((y1 - y0) * scale))
    scaled = crop.resize((nw, nh), Image.Resampling.LANCZOS).convert("RGBA")
    # centre of the dialog maps to the well centre
    dcx = ((x + w / 2.0) - x0) * scale
    dcy = ((y + h / 2.0) - y0) * scale
    px = int(round(WELL_CX - dcx))
    py = int(round(WELL_CY - dcy))
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    layer.paste(scaled, (px, py), scaled)
    return layer


def find_sec15_bbox(frame: Image.Image, expected) -> tuple[float, float, float, float]:
    """Pixel-analyse the composed frame for the true 「15秒」 glyph box.

    `expected` is a rough (x, y, w, h) in frame pixels used to locate the
    search window. Returns the tight ink bounding box.
    """
    ex, ey, ew, eh = expected
    # generous search window around the predicted box
    x0 = max(0, int(ex) - 30)
    y0 = max(0, int(ey) - 20)
    x1 = min(frame.width, int(ex + ew) + 30)
    y1 = min(frame.height, int(ey + eh) + 20)
    rgb = np.array(frame.convert("RGB"))
    roi = rgb[y0:y1, x0:x1]
    if roi.size == 0:
        return expected
    gray = cv2.cvtColor(roi, cv2.COLOR_RGB2GRAY)
    # The subtitle is mid-gray on a near-white card. Use a threshold that
    # keeps the glyphs but drops the card and the darker title above.
    # Try a few thresholds and pick the one whose bbox is closest in
    # aspect to "three compact characters" (~2.0–2.4 width/height).
    best = None
    for th in (200, 210, 220, 230, 185):
        ink = gray < th
        # drop very small speckles
        ink = cv2.morphologyEx(ink.astype(np.uint8) * 255, cv2.MORPH_OPEN,
                               np.ones((2, 2), np.uint8))
        ys, xs = np.where(ink > 0)
        if len(xs) < 20:
            continue
        # keep only the densest horizontal band (the subtitle row)
        # by taking the y-range with the most ink
        row = ink.sum(axis=1)
        # find the longest / strongest run
        ys_band = np.where(row > row.max() * 0.25)[0]
        if len(ys_band) == 0:
            continue
        by0, by1 = int(ys_band[0]), int(ys_band[-1])
        band = ink[by0:by1 + 1]
        col = band.sum(axis=0)
        # The line is "录制15秒即可完成克隆". We want the run group for 15秒:
        # typically the 3rd–5th character clusters. Use the expected
        # centre as a prior.
        exp_cx = (ex + ew / 2.0) - x0
        # connected column runs
        runs = []
        inn = False
        for i, v in enumerate(col):
            if v > 0 and not inn:
                s = i
                inn = True
            elif v == 0 and inn:
                runs.append((s, i - 1))
                inn = False
        if inn:
            runs.append((s, len(col) - 1))
        if not runs:
            continue
        # pick a group of 3 consecutive runs whose midpoint is closest to exp_cx
        # (1, 5, 秒). If we can't, fall back to ink near the expected box.
        def run_cx(a, b):
            return 0.5 * (a + b)

        if len(runs) >= 3:
            best_g, best_d = None, 1e9
            for i in range(len(runs) - 2):
                a0, a1 = runs[i]
                _, c1 = runs[i + 2]
                gcx = 0.5 * (a0 + c1)
                d = abs(gcx - exp_cx)
                # prefer groups whose width is in a plausible range
                width = c1 - a0 + 1
                if width < ew * 0.4 or width > ew * 2.2:
                    continue
                if d < best_d:
                    best_d, best_g = d, (a0, by0, c1 - a0 + 1, by1 - by0 + 1)
            if best_g is not None:
                gx, gy, gw, gh = best_g
                cand = (x0 + gx, y0 + gy, gw, gh)
                if best is None or abs((cand[0] + cand[2] / 2) - (ex + ew / 2)) < abs((best[0] + best[2] / 2) - (ex + ew / 2)):
                    best = cand
                continue
        # fallback: tight ink of the expected region only
        lx0 = max(0, int(ex - x0) - 4)
        ly0 = max(0, int(ey - y0) - 4)
        lx1 = min(ink.shape[1], int(ex + ew - x0) + 4)
        ly1 = min(ink.shape[0], int(ey + eh - y0) + 4)
        sub = ink[ly0:ly1, lx0:lx1]
        sy, sx = np.where(sub > 0)
        if len(sx) >= 10:
            cand = (x0 + lx0 + int(sx.min()), y0 + ly0 + int(sy.min()),
                    int(sx.max() - sx.min() + 1), int(sy.max() - sy.min() + 1))
            best = cand if best is None else best
    return best if best is not None else expected


def encode_frames(frames, out: Path):
    out.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo", "-pix_fmt", "rgb24",
        "-s", f"{W}x{H}", "-r", str(FPS),
        "-i", "-",
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-crf", "17", "-preset", "medium",
        "-movflags", "+faststart", "-an",
        str(out),
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    assert proc.stdin is not None
    try:
        for im in frames:
            if im.size != (W, H):
                im = im.resize((W, H), Image.Resampling.LANCZOS)
            proc.stdin.write(np.array(im.convert("RGB")).tobytes())
    finally:
        proc.stdin.close()
    err = proc.stderr.read()
    ret = proc.wait()
    if ret != 0:
        sys.stderr.write(err.decode("utf-8", "replace")[-2000:])
        raise RuntimeError(f"ffmpeg failed for {out}")
    print("wrote", out)


def load_sources():
    board = Image.open(rs.ASSETS / "chalkboard_1080x1920.png").convert("RGBA")
    avatar = Image.open(STILLS / "avatar_dialog.png").convert("RGB")
    lang = Image.open(STILLS / "language_dialog.png").convert("RGB")
    read = blur_passage(Image.open(STILLS / "reading_dialog.png").convert("RGB"), PASSAGE, radius=22)
    overview = Image.open(STILLS / "overview.png").convert("RGB")
    return {
        "board": board,
        "avatar": avatar,
        "lang": lang,
        "read": read,
        "overview": overview,
        "avatar_bgr": cv2.cvtColor(np.array(avatar), cv2.COLOR_RGB2BGR),
        "lang_bgr": cv2.cvtColor(np.array(lang), cv2.COLOR_RGB2BGR),
        "read_bgr": cv2.cvtColor(np.array(read), cv2.COLOR_RGB2BGR),
        "overview_bgr": cv2.cvtColor(np.array(overview), cv2.COLOR_RGB2BGR),
    }


def shot21_cam_and_box(t: float):
    """Camera and source box for shot 21 at time t."""
    # 0–0.35: arrive on a wide-but-already-large view
    # 0.35–0.65: punch in to the upload cards
    # 1.40–1.70: punch/pan to the requirement chip
    if t < ZOOM_DUR:
        return CAM_AV_WIDE, BOX_UPLOADS, 0.0
    if t < ZOOM_DUR + PUNCH_DUR:
        p = (t - ZOOM_DUR) / PUNCH_DUR
        cam = lerp_cam(CAM_AV_WIDE, CAM_UPLOADS, p)
        pop = min(1.0, (t - ZOOM_DUR) / BOX_POP)
        return cam, BOX_UPLOADS, pop
    if t < S21_CUT:
        return CAM_UPLOADS, BOX_UPLOADS, 1.0
    if t < S21_CUT + PUNCH_DUR:
        p = (t - S21_CUT) / PUNCH_DUR
        cam = lerp_cam(CAM_UPLOADS, CAM_REQ, p)
        # morph the box with the same ease
        box = lerp_box(BOX_UPLOADS, BOX_REQ_CHIP, ease_in_out(p))
        return cam, box, 1.0
    return CAM_REQ, BOX_REQ_CHIP, 1.0


def render_shot21(S) -> list[Image.Image]:
    print("cameras shot21:")
    for name, cam, box, gsrc in (
        ("wide", CAM_AV_WIDE, BOX_UPLOADS, 15),
        ("uploads", CAM_UPLOADS, BOX_UPLOADS, 15),
        ("req", CAM_REQ, BOX_REQ_CHIP, 14),
    ):
        print(f"  {name:8s}  scale={cam[0]:.2f}  glyph≈{gsrc*cam[0]:.1f}px  "
              f"box_w={box[2]*cam[0]:.0f}px")
    nf = int(round(SHOT21_DUR * FPS))
    frames = []
    for i in range(nf):
        t = i / FPS
        if t < S21_CUT:
            sub, fade = "Sphere的数字分身", min(1.0, t / 0.10) if t < 0.10 else 1.0
        else:
            sub, fade = "传1张照片 生成形象", min(1.0, (t - S21_CUT) / 0.10)
        cam, box, pop = shot21_cam_and_box(t)
        fr = compose_camera(S["avatar_bgr"], cam, S["board"])
        if pop > 0:
            draw_red_box(fr, padded_frame_box(box, cam), progress=pop)
        fr = finish_chrome(fr, "模块① 创建数字分身", sub, fade=fade)
        fr = apply_zoom_blur(fr, t)
        frames.append(fr.convert("RGB"))
        if i % 15 == 0 or i == nf - 1:
            print(f"  shot21  {i+1}/{nf}")
    return frames


def render_shot22(S) -> list[Image.Image]:
    print("cameras shot22:")
    for name, cam, box, gsrc in (
        ("flip", CAM_LANG_WIDE, BOX_MANDARIN, 15),
        ("mandarin", CAM_MANDARIN, BOX_MANDARIN, 15),
        ("record", CAM_RECORD, BOX_RECORD_LABEL, 16),
    ):
        print(f"  {name:8s}  scale={cam[0]:.2f}  glyph≈{gsrc*cam[0]:.1f}px  "
              f"box_w={box[2]*cam[0]:.0f}px")
    nf = int(round(SHOT22_DUR * FPS))

    # Flip layers: well contents at the same cameras used just after the
    # flip, so the last flip frame matches the first punched frame's start.
    def well_rgba(src_bgr, cam):
        fr = compose_camera(src_bgr, cam, S["board"])
        arr = np.array(fr.convert("RGBA"))
        arr[:WELL_TOP, :, 3] = 0
        arr[WELL_BOTTOM:, :, 3] = 0
        return arr

    av_rgba = well_rgba(S["avatar_bgr"], CAM_AV_FLIP)
    lang_rgba = well_rgba(S["lang_bgr"], CAM_LANG_WIDE)
    box_mandarin_flip = padded_frame_box(BOX_MANDARIN, CAM_LANG_WIDE)

    # Pre-compose the 15s insert card, then measure the real 「15秒」glyphs
    # so the circle is centred on the characters, not a guessed offset.
    # Scale so the plus-icon +「录制15秒即可完成克隆」fill the width,
    # with the card title just in frame on the left.
    insert_cam_scale = 5.00
    focus_x = 382.0
    focus_y = VOICE_CARD[1] + 78
    CAM_INSERT = (insert_cam_scale, focus_x, focus_y)
    insert_base = compose_camera(S["overview_bgr"], CAM_INSERT, S["board"])
    predicted = src_to_frame(SEC15_ABS, CAM_INSERT)
    sec_box = find_sec15_bbox(insert_base, predicted)
    sx, sy, sw, sh = sec_box
    sec_cx, sec_cy = sx + sw / 2.0, sy + sh / 2.0
    # diameter clearly larger than the glyph box, even padding
    sec_r = 0.5 * math.hypot(sw, sh) + 16
    print(f"  insert   scale={insert_cam_scale:.2f}  "
          f"15秒 predicted=({predicted[0]:.1f},{predicted[1]:.1f},{predicted[2]:.1f},{predicted[3]:.1f})  "
          f"measured=({sx:.1f},{sy:.1f},{sw:.1f},{sh:.1f})  r={sec_r:.1f}")

    frames = []
    for i in range(nf):
        t = i / FPS
        if t < S22_CUT:
            sub, fade = "读一段文字", min(1.0, t / 0.10) if t < 0.10 else 1.0
        else:
            sub, fade = "录15秒 克隆声音", min(1.0, (t - S22_CUT) / 0.10)

        if t < FLIP_DUR:
            p = bezier_ease(t / FLIP_DUR)
            canvas = S["board"].copy()
            if p < 0.5:
                ang = 180 * p
                warped = warp_page(av_rgba, ang)
            else:
                ang = -180 * (1.0 - p)
                warped = warp_page(lang_rgba, ang)
            canvas.alpha_composite(Image.fromarray(warped, "RGBA"))
            pop = 0.0
            if p >= 0.5:
                pop = min(1.0, (p - 0.5) / 0.5)
                draw_red_box(canvas, box_mandarin_flip, progress=pop)
            fr = finish_chrome(canvas, "模块② 创建我的声音", sub, fade=fade)
        elif t < S22_HARD_CUT:
            # punch in from the flip's wide view to the 普通话 card
            local = t - FLIP_DUR
            # hold a moment if the punch already finished (hard cut is at 1.10,
            # flip ends 0.40, punch needs 0.30 → 0.10s hold)
            p = min(1.0, local / PUNCH_DUR)
            cam = lerp_cam(CAM_LANG_WIDE, CAM_MANDARIN, p)
            fr = compose_camera(S["lang_bgr"], cam, S["board"])
            draw_red_box(fr, padded_frame_box(BOX_MANDARIN, cam), progress=1.0)
            fr = finish_chrome(fr, "模块② 创建我的声音", sub, fade=fade)
        elif t < S22_INSERT_AT:
            local = t - S22_HARD_CUT
            p = min(1.0, local / PUNCH_DUR)
            # start from a wide-ish reading dialog, punch to the 开始录制 label
            cam = lerp_cam(CAM_READ_WIDE, CAM_RECORD, p)
            fr = compose_camera(S["read_bgr"], cam, S["board"])
            pop = min(1.0, local / BOX_POP)
            draw_red_box(fr, padded_frame_box(BOX_RECORD_LABEL, cam), progress=pop)
            fr = finish_chrome(fr, "模块② 创建我的声音", sub, fade=fade)
        else:
            local = t - S22_INSERT_AT
            pop = min(1.0, local / BOX_POP)
            # slight 0.92→1.00 pop of the already-large insert
            sc = 0.92 + 0.08 * pop
            if sc < 0.999:
                # scale the precomposed insert about the well centre
                arr = cv2.cvtColor(np.array(insert_base.convert("RGB")), cv2.COLOR_RGB2BGR)
                arr = scale_about_center(arr, sc)
                fr = Image.fromarray(cv2.cvtColor(arr, cv2.COLOR_BGR2RGB)).convert("RGBA")
                # circle tracks the same centre scale about the frame centre
                cx2 = W / 2 + (sec_cx - W / 2) * sc
                cy2 = H / 2 + (sec_cy - H / 2) * sc
                # the insert is only in the well, which is not the frame
                # centre. scale_about_center uses the image centre (960).
                # The well centre is WELL_CY. Recompute:
                # scale_about_center zooms about (W/2, H/2) = (540, 960).
                # That's slightly off the well centre (540, 865). Use well centre.
                # We'll redo the pop about the well centre for correctness.
                fr = S["board"].copy()
                # zoom insert_base's well about WELL_CX, WELL_CY
                well = np.array(insert_base.convert("RGB"))[WELL_TOP:WELL_BOTTOM, :, :]
                well_bgr = cv2.cvtColor(well, cv2.COLOR_RGB2BGR)
                hh, ww = well_bgr.shape[:2]
                nw, nh = int(round(ww * sc)), int(round(hh * sc))
                resized = cv2.resize(well_bgr, (nw, nh), interpolation=cv2.INTER_LINEAR)
                # place so well centre stays put
                # original centre in well coords: (W/2, WELL_H/2)
                # new centre should land at the same frame point
                cx_w, cy_w = ww / 2.0, hh / 2.0
                x0 = int(round(cx_w * sc - cx_w))
                y0 = int(round(cy_w * sc - cy_w))
                # cropped / padded back to ww x hh
                canvas = np.zeros_like(well_bgr)
                # dest in canvas, src in resized
                dx0, dy0 = max(0, -x0), max(0, -y0)
                sx0, sy0 = max(0, x0), max(0, y0)
                dw = min(ww - dx0, nw - sx0)
                dh = min(hh - dy0, nh - sy0)
                if dw > 0 and dh > 0:
                    canvas[dy0:dy0 + dh, dx0:dx0 + dw] = resized[sy0:sy0 + dh, sx0:sx0 + dw]
                fr.paste(Image.fromarray(cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB)), (0, WELL_TOP))
                # 15秒 centre relative to well, after scale about well centre
                relx = sec_cx - WELL_CX
                rely = sec_cy - WELL_CY
                cx2 = WELL_CX + relx * sc
                cy2 = WELL_CY + rely * sc
                r2 = sec_r * sc
            else:
                fr = insert_base.copy()
                cx2, cy2, r2 = sec_cx, sec_cy, sec_r
            draw_red_circle(fr, cx2, cy2, r2, progress=pop)
            fr = finish_chrome(fr, "模块② 创建我的声音", sub, fade=fade)

        frames.append(fr.convert("RGB"))
        if i % 15 == 0 or i == nf - 1:
            print(f"  shot22  {i+1}/{nf}")
    return frames


def save_grabs(frames, shot: int, times: list[float]):
    GRABS.mkdir(parents=True, exist_ok=True)
    nf = len(frames)
    for t in times:
        idx = min(nf - 1, max(0, int(round(t * FPS))))
        p = GRABS / f"shot{shot}_{t:.2f}s.png"
        frames[idx].save(p, "PNG")
        print("  grab", p.name)
    frames[nf // 2].save(GRABS / f"shot{shot}.png", "PNG")


def main():
    if not (STILLS / "avatar_dialog.png").exists():
        raise SystemExit(f"missing stills in {STILLS}")
    print("loading sources…")
    S = load_sources()
    print("rendering shot 21…")
    f21 = render_shot21(S)
    print("rendering shot 22…")
    f22 = render_shot22(S)
    CLIPS.mkdir(parents=True, exist_ok=True)
    encode_frames(f21, CLIPS / "shot21.mp4")
    encode_frames(f22, CLIPS / "shot22.mp4")
    save_grabs(f21, 21, [0.00, 0.12, 0.35, 0.50, 0.80, 1.50, 1.80, 2.40, 3.50])
    save_grabs(f22, 22, [0.00, 0.20, 0.40, 0.70, 1.00, 1.15, 1.40, 1.85, 2.10, 2.50])
    print("done.")


if __name__ == "__main__":
    main()
