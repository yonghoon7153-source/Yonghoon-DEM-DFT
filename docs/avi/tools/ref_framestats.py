#!/usr/bin/env python3
"""Per-frame statistics of a reference video (measure, don't guess).

Decodes the video once through ffmpeg (rawvideo pipe, small gray frames) and
stores, per frame:
  * mean absolute difference vs the previous frame in three bands
    (content = top 80 %, caption band, whole frame)
  * a tiny 96x54 thumbnail for later net-change comparisons
Outputs an .npz next to --out.

Usage: python3 -I ref_framestats.py VIDEO --out stats.npz [--w 320 --h 180]
"""
import argparse
import subprocess
import sys

import numpy as np


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--out", required=True)
    ap.add_argument("--w", type=int, default=320)
    ap.add_argument("--h", type=int, default=180)
    ap.add_argument("--threads", type=int, default=2)
    a = ap.parse_args()
    W, H = a.w, a.h
    cmd = ["nice", "-n", "15", "ffmpeg", "-v", "error", "-threads", str(a.threads),
           "-i", a.video, "-vf", f"scale={W}:{H}:flags=area,format=gray",
           "-f", "rawvideo", "-pix_fmt", "gray", "-"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=W * H * 64)
    fs = W * H
    prev = None
    d_content, d_caption, d_all, mean_l = [], [], [], []
    thumbs = []
    cy0, cy1 = int(0.84 * H), int(0.97 * H)   # caption band (measured ~0.86-0.94 H)
    ky1 = int(0.80 * H)                        # content band
    n = 0
    while True:
        buf = p.stdout.read(fs)
        if len(buf) < fs:
            break
        f = np.frombuffer(buf, np.uint8).reshape(H, W).astype(np.int16)
        if prev is None:
            d_content.append(0.0); d_caption.append(0.0); d_all.append(0.0)
        else:
            ad = np.abs(f - prev)
            d_content.append(float(ad[:ky1].mean()))
            d_caption.append(float(ad[cy0:cy1].mean()))
            d_all.append(float(ad.mean()))
        mean_l.append(float(f.mean()))
        t = f.reshape(54, H // 54, 96, W // 96).mean(axis=(1, 3)) if (H % 54 == 0 and W % 96 == 0) else None
        if t is None:
            # generic block mean
            ys = np.linspace(0, H, 55).astype(int); xs = np.linspace(0, W, 97).astype(int)
            t = np.add.reduceat(np.add.reduceat(f.astype(np.int32), ys[:-1], axis=0), xs[:-1], axis=1)
            t = t / (np.diff(ys)[:, None] * np.diff(xs)[None, :])
        thumbs.append(t.astype(np.uint8))
        prev = f
        n += 1
    p.wait()
    np.savez_compressed(a.out, d_content=np.array(d_content, np.float32),
                        d_caption=np.array(d_caption, np.float32),
                        d_all=np.array(d_all, np.float32),
                        mean_l=np.array(mean_l, np.float32),
                        thumbs=np.stack(thumbs), W=W, H=H)
    print(f"frames={n} saved {a.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
