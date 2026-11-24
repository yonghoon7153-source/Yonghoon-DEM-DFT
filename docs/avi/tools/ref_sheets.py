#!/usr/bin/env python3
"""Contact sheets for the reference analysis.

  frames mode : grid of frames (every N s) with time labels
  captions mode: stacked caption crops (one per caption segment) with labels

Usage:
  python3 -I ref_sheets.py frames  DIR_WITH_s_XXXX.png --every 3 --out-prefix P
  python3 -I ref_sheets.py captions DIR_WITH_c_XXXX.png --meta capmids.json --out-prefix P
"""
import argparse
import glob
import json
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFont

FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"


def font(sz):
    return ImageFont.truetype(FONT, sz, index=1)  # index 1 = KR in the ttc? fall back below


def safe_font(sz):
    for idx in (1, 0, 2, 3):
        try:
            return ImageFont.truetype(FONT, sz, index=idx)
        except Exception:
            continue
    return ImageFont.load_default()


def frames(a):
    files = sorted(glob.glob(os.path.join(a.dir, "s_*.png")))
    cols, rows = 4, 4
    w, h = Image.open(files[0]).size
    lab = 26
    f = safe_font(20)
    per = cols * rows
    for k in range(0, len(files), per):
        sheet = Image.new("RGB", (cols * w, rows * (h + lab)), (255, 255, 255))
        dr = ImageDraw.Draw(sheet)
        for j, fn in enumerate(files[k:k + per]):
            idx = k + j
            t = idx * a.every  # fps=1/N filter: output i ~ input frame nearest i*N s
            x, y = (j % cols) * w, (j // cols) * (h + lab)
            sheet.paste(Image.open(fn), (x, y + lab))
            dr.text((x + 6, y + 2), f"#{idx:03d}  t~{t:5.1f}s", fill=(200, 0, 0), font=f)
        out = f"{a.out_prefix}_{k // per + 1:02d}.jpg"
        sheet.save(out, quality=80)
        print(out)


def captions(a):
    meta = json.load(open(a.meta))
    files = sorted(glob.glob(os.path.join(a.dir, "c_*.png")))
    assert len(files) == len(meta), (len(files), len(meta))
    f = safe_font(18)
    crops = []
    for fn, m in zip(files, meta):
        im = Image.open(fn).convert("RGB")
        L = np.asarray(im).mean(axis=2)
        dark = L < 120
        cols = np.where(dark.sum(axis=0) > 5)[0]
        if len(cols):
            x0, x1 = max(cols.min() - 4, 0), min(cols.max() + 4, im.width)
        else:
            x0, x1 = 300, 980
        crops.append((im.crop((x0, 0, x1, im.height)), m))
    colw = 760
    rowh = 76 + 4
    per_col = 16
    ncol = 2
    per = per_col * ncol
    for k in range(0, len(crops), per):
        sheet = Image.new("RGB", (ncol * (colw + 150), per_col * rowh), (255, 255, 255))
        dr = ImageDraw.Draw(sheet)
        for j, (c, m) in enumerate(crops[k:k + per]):
            cx = (j // per_col) * (colw + 150)
            cy = (j % per_col) * rowh
            dr.text((cx + 4, cy + 22), f"{k + j:03d} {m['t0']:6.2f}", fill=(200, 0, 0), font=f)
            dr.text((cx + 4, cy + 44), f"{m['dur']:.2f}s", fill=(0, 0, 160), font=f)
            sheet.paste(c.crop((0, 0, min(c.width, colw), c.height)), (cx + 145, cy))
        out = f"{a.out_prefix}_{k // per + 1:02d}.png"
        sheet.save(out)
        print(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["frames", "captions"])
    ap.add_argument("dir")
    ap.add_argument("--every", type=float, default=3.0)
    ap.add_argument("--meta")
    ap.add_argument("--out-prefix", required=True)
    a = ap.parse_args()
    (frames if a.mode == "frames" else captions)(a)


if __name__ == "__main__":
    main()
