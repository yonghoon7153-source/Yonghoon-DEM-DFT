#!/usr/bin/env python3
"""누끼: flood-fill white background -> transparent PNG (for VESTA/figure exports).

Removes ONLY the background-connected white region (flood-filled from the image
border), so interior white/grey atoms are preserved and there is no white halo.

Usage:
  python3 cutout_bg.py input.png [output.png] [--thresh 30] [--white 250] [--feather 1]

  --thresh   color distance tolerance for flood fill (anti-aliased edges). 20-40 ok.
  --white    a border pixel is treated as background only if all channels >= this.
  --feather  px of edge softening on the alpha (0 = hard edge).

Deps: pillow (PIL).  numpy optional (used for feather).
"""
import argparse
from PIL import Image, ImageDraw, ImageFilter


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("inp")
    ap.add_argument("out", nargs="?")
    ap.add_argument("--thresh", type=int, default=30)
    ap.add_argument("--white", type=int, default=250)
    ap.add_argument("--feather", type=int, default=1)
    a = ap.parse_args()
    out = a.out or a.inp.rsplit(".", 1)[0] + "_cutout.png"

    img = Image.open(a.inp).convert("RGBA")
    w, h = img.size
    rgb = img.convert("RGB")
    SENT = (255, 0, 255)  # magenta sentinel — flood-fill background to this

    # seed from many border points so a non-uniform border still gets filled
    seeds = []
    for x in range(0, w, max(1, w // 40)):
        seeds += [(x, 0), (x, h - 1)]
    for y in range(0, h, max(1, h // 40)):
        seeds += [(0, y), (w - 1, y)]
    px = rgb.load()
    for s in seeds:
        r, g, b = px[s]
        if r >= a.white and g >= a.white and b >= a.white:   # only seed on white border
            ImageDraw.floodfill(rgb, s, SENT, thresh=a.thresh)

    # build alpha: transparent where sentinel
    src = rgb.load()
    alpha = Image.new("L", (w, h), 255)
    ap_ = alpha.load()
    n = 0
    for y in range(h):
        for x in range(w):
            if src[x, y] == SENT:
                ap_[x, y] = 0
                n += 1
    if a.feather > 0:
        alpha = alpha.filter(ImageFilter.GaussianBlur(a.feather))

    img.putalpha(alpha)
    img.save(out)
    print(f"누끼 완료: {out}  ({n} bg px -> transparent, {100*n/(w*h):.0f}% of image)")


if __name__ == "__main__":
    main()
