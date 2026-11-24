#!/usr/bin/env python3
"""Filmstrip of a short time window (to see how an animation moves).

Usage: python3 -I ref_filmstrip.py VIDEO --t0 S --t1 S --step FRAMES --out out.jpg
       [--crop x,y,w,h] (in source pixels) [--cols 6] [--scale 0.5]
"""
import argparse
import os
import subprocess
import tempfile

from PIL import Image, ImageDraw, ImageFont

FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--t0", type=float, required=True)
    ap.add_argument("--t1", type=float, required=True)
    ap.add_argument("--step", type=int, default=2)
    ap.add_argument("--fps", type=float, default=30.0)
    ap.add_argument("--crop", default=None)
    ap.add_argument("--cols", type=int, default=6)
    ap.add_argument("--scale", type=float, default=0.5)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    tmp = tempfile.mkdtemp(prefix="strip_", dir=os.path.dirname(os.path.abspath(a.out)))
    vf = []
    if a.crop:
        x, y, w, h = a.crop.split(",")
        vf.append(f"crop={w}:{h}:{x}:{y}")
    vf.append(f"select='not(mod(n\\,{a.step}))'")
    cmd = ["nice", "-n", "15", "ffmpeg", "-v", "error", "-threads", "2", "-ss", f"{a.t0:.3f}", "-i", a.video,
           "-t", f"{a.t1 - a.t0:.3f}", "-vf", ",".join(vf), "-vsync", "vfr", "-y", os.path.join(tmp, "f_%04d.png")]
    subprocess.run(cmd, check=True)
    files = sorted(os.listdir(tmp))
    ims = [Image.open(os.path.join(tmp, f)).convert("RGB") for f in files]
    if not ims:
        raise SystemExit("no frames")
    w, h = ims[0].size
    w2, h2 = int(w * a.scale), int(h * a.scale)
    cols = a.cols
    rows = (len(ims) + cols - 1) // cols
    lab = 22
    sheet = Image.new("RGB", (cols * w2, rows * (h2 + lab)), (255, 255, 255))
    dr = ImageDraw.Draw(sheet)
    try:
        f = ImageFont.truetype(FONT, 16)
    except Exception:
        f = ImageFont.load_default()
    for i, im in enumerate(ims):
        x, y = (i % cols) * w2, (i // cols) * (h2 + lab)
        sheet.paste(im.resize((w2, h2), Image.LANCZOS), (x, y + lab))
        t = a.t0 + i * a.step / a.fps
        dr.text((x + 4, y + 2), f"{t:.3f}s", fill=(200, 0, 0), font=f)
    sheet.save(a.out, quality=85)
    for fn in files:
        os.remove(os.path.join(tmp, fn))
    os.rmdir(tmp)
    print(a.out, len(ims), "frames")


if __name__ == "__main__":
    main()
