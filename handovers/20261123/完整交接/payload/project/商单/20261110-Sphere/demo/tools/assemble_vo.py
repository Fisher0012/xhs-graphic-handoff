#!/usr/bin/env python3
"""Assemble demo/audio/vo.wav from clause mp3s, fitted to the 14.4s demo windows.

Most lines stay at +12% (Yunxi). Shot 20 uses the +35% takes so the two
clauses land on the existing 1.30s subtitle cut in shot20.mp4. Shot 1 gets
a very slight atempo after trim so 2.82s of speech fits in 2.8s.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

import numpy as np
import wave

ROOT = Path("/workspace/xhs/商单/20261110-Sphere/demo")
LINES = ROOT / "audio" / "vo_lines"
OUT = ROOT / "audio" / "vo.wav"
SR = 48000
TOTAL = 14.4

# (file, dest_start_sec, atempo or None)
# dest_start is where the TRIMMED speech (plus 40ms head pad) begins.
PLACES = [
    # shot 1 0.00-2.80 — speech 2.82s → atempo to 2.70s, start 0.05
    ("s1.mp3", 0.05, 2.82 / 2.70),
    # shot 2 2.80-3.90 — speech 0.72s, plenty of room
    ("s2.mp3", 2.85, None),
    # shot 19 3.90-5.10 silent
    # shot 20 5.10-7.90, baked subtitle cut at 5.10+1.30=6.40
    ("s20a_35.mp3", 5.15, None),  # 1.26s speech → ends ~6.41
    ("s20b_35.mp3", 6.52, None),  # after s20a; ends ~7.92
    # shot 21 7.90-11.80
    ("s21a.mp3", 8.05, None),     # 1.04s → ends 9.09
    ("s21b.mp3", 9.30, None),     # 1.74s → ends 11.04
    # shot 22 11.80-14.40
    ("s22a.mp3", 11.85, None),    # 0.70s → ends 12.55
    ("s22b.mp3", 12.88, None),    # 1.46s → ends 14.34
]

HEAD_PAD = 0.04
TAIL_PAD = 0.04
THRESH = 0.01


def decode(path: Path) -> np.ndarray:
    raw = subprocess.check_output([
        "ffmpeg", "-v", "error", "-i", str(path),
        "-ac", "1", "-ar", str(SR), "-f", "f32le", "-",
    ])
    return np.frombuffer(raw, dtype=np.float32)


def trim_speech(x: np.ndarray) -> np.ndarray:
    hop = int(SR * 0.02)
    if len(x) < hop:
        return x
    env = np.array([np.sqrt(np.mean(x[i:i + hop] ** 2)) for i in range(0, len(x) - hop, hop)])
    active = np.where(env > THRESH)[0]
    if len(active) == 0:
        return x[:1]
    t0 = max(0, active[0] * hop - int(HEAD_PAD * SR))
    t1 = min(len(x), (active[-1] + 1) * hop + int(TAIL_PAD * SR))
    return x[t0:t1]


def atempo(x: np.ndarray, tempo: float) -> np.ndarray:
    if abs(tempo - 1.0) < 0.005:
        return x
    proc = subprocess.run(
        ["ffmpeg", "-v", "error", "-f", "f32le", "-ac", "1", "-ar", str(SR), "-i", "-",
         "-filter:a", f"atempo={tempo:.5f}", "-f", "f32le", "-"],
        input=x.astype(np.float32).tobytes(),
        stdout=subprocess.PIPE,
        check=True,
    )
    return np.frombuffer(proc.stdout, dtype=np.float32)


def main() -> None:
    n = int(round(TOTAL * SR))
    mix = np.zeros(n + SR, dtype=np.float32)  # tiny tail cushion
    report = []
    for name, start, tempo in PLACES:
        path = LINES / name
        x = trim_speech(decode(path))
        raw_dur = len(x) / SR
        if tempo is not None:
            x = atempo(x, tempo)
        dur = len(x) / SR
        i0 = int(round(start * SR))
        i1 = i0 + len(x)
        if i1 > len(mix):
            mix = np.pad(mix, (0, i1 - len(mix)))
        mix[i0:i1] += x
        report.append({
            "file": name,
            "start": round(start, 3),
            "end": round(start + dur, 3),
            "dur": round(dur, 3),
            "trim_dur": round(raw_dur, 3),
            "atempo": tempo,
        })
        print(f"  {name:16s}  {start:.3f}–{start+dur:.3f}  ({dur:.3f}s)")

    mix = mix[:n]
    peak = float(np.max(np.abs(mix))) if mix.size else 0.0
    if peak > 0.89:
        mix *= 0.89 / peak
        print(f"peak-normalized {peak:.3f} → 0.89")
    else:
        print(f"peak {peak:.3f}, no attenuate")

    # 16-bit stereo wav
    pcm = np.clip(mix * 32767.0, -32768, 32767).astype(np.int16)
    stereo = np.column_stack([pcm, pcm]).tobytes()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(OUT), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(stereo)
    (ROOT / "audio" / "vo_timeline.json").write_text(json.dumps({
        "sample_rate": SR,
        "duration": TOTAL,
        "places": report,
        "subtitle_cues": [
            {"start": 0.00, "end": 2.80, "shot": 1, "text": "(hook title, no bottom bar)"},
            {"start": 2.80, "end": 3.90, "shot": 2, "text": "是这三道坎"},
            {"start": 5.10, "end": 6.40, "shot": 20, "text": "第三道坎 出镜"},
            {"start": 6.40, "end": 7.90, "shot": 20, "text": "不想露脸 也没空拍"},
            {"start": 7.90, "end": 9.30, "shot": 21, "text": "Sphere的数字分身"},
            {"start": 9.30, "end": 11.80, "shot": 21, "text": "传1张照片 生成形象"},
            {"start": 11.80, "end": 12.88, "shot": 22, "text": "读一段文字"},
            {"start": 12.88, "end": 14.40, "shot": 22, "text": "录15秒 克隆声音"},
        ],
    }, ensure_ascii=False, indent=2))
    print("wrote", OUT, "dur", n / SR)


if __name__ == "__main__":
    main()
