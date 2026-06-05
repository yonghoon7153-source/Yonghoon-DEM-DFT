#!/usr/bin/env python3
"""누끼: white background -> transparent PNG (for VESTA/figure exports).

Two modes:
  (default)    flood-fill from border: removes ONLY background-connected white;
               interior white gaps stay white, atom highlights preserved.
  --interior   connected-component area filter (needs scipy): removes ALL large
               white regions (outer bg + interior gaps between atoms) but KEEPS
               small white spots (specular highlights) so atoms get no holes.

Usage:
  python3 cutout_bg.py input.png [output.png] [--interior] [--thresh 30]
          [--white 250] [--min-area 2000] [--feather 1]

  --thresh    flood-fill color tolerance (default mode). 20-40 ok.
  --white     channel >= this counts as white. 248-252.
  --min-area  (--interior) white blobs >= this area are removed; smaller kept.
              raise if atom holes remain; lower if interior gaps not removed.
  --feather   px of edge softening on the alpha (0 = hard edge).

Deps: pillow.  --interior also needs numpy + scipy.
"""
import argparse
from PIL import Image, ImageDraw, ImageFilter


def interior_cutout(img, white, min_area, feather):
    import numpy as np
    from scipy import ndimage
    arr = np.array(img)
    wmask = (arr[:, :, 0] >= white) & (arr[:, :, 1] >= white) & (arr[:, :, 2] >= white)
    lbl, n = ndimage.label(wmask)
    sizes = ndimage.sum(np.ones_like(lbl), lbl, range(1, n + 1))
    big = [i + 1 for i, s in enumerate(sizes) if s >= min_area]
    remove = np.isin(lbl, big)
    alpha = np.where(remove, 0, 255).astype("uint8")
    if feather:
        alpha = np.array(Image.fromarray(alpha, "L").filter(ImageFilter.GaussianBlur(feather)))
    arr[:, :, 3] = alpha
    print(f"  [interior] removed {len(big)} large white blobs of {n} total")
    return Image.fromarray(arr)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("inp")
    ap.add_argument("out", nargs="?")
    ap.add_argument("--thresh", type=int, default=30)
    ap.add_argument("--white", type=int, default=250)
    ap.add_argument("--min-area", type=int, default=2000, dest="min_area")
    ap.add_argument("--interior", action="store_true",
                    help="also remove interior white gaps (CC area filter; needs scipy)")
    ap.add_argument("--feather", type=int, default=1)
    a = ap.parse_args()
    out = a.out or a.inp.rsplit(".", 1)[0] + ("_cc.png" if a.interior else "_cutout.png")

    img = Image.open(a.inp).convert("RGBA")
    w, h = img.size

    if a.interior:
        interior_cutout(img, a.white, a.min_area, a.feather).save(out)
        print(f"누끼(interior) 완료: {out}")
        return
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
