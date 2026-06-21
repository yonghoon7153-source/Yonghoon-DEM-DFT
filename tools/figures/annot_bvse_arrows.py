#!/usr/bin/env python3
"""annot_bvse_arrows.py — overlay ONLY blue/green/red migration arrows on the
BVSE low-channel figure (docs/figures/deck_extracted/bvse_channels.png).

Arrows only: no legend, no labels, no S/Cl markers, no x/check marks (the
speaker explains the colours verbally). The baked-in "low-BVSE channel: X %"
captions stay. White halos so the arrows read against the blue point cloud.

Colour scheme (explained verbally):
  blue  (solid)  intra-cage hop (fast local)        - both panels
  red   (dashed) inter-cage bottleneck = Ea         - LPSCl (left), blocked
  green (solid)  inter-cage opens / percolates       - LPSCl1.6 (right)

  python3 annot_bvse_arrows.py
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

SRC = "docs/figures/deck_extracted/bvse_channels.png"
OUT = "docs/figures/ionic/bvse_channels_arrows.png"
BLUE, RED, GREEN = "#1f77b4", "#d62728", "#2ca02c"


def arrow(ax, p0, p1, color, dashed=False, lw=3.2):
    for col, w in (("white", lw + 3.5), (color, lw)):       # white halo, then colour
        ax.annotate("", xy=p1, xytext=p0,
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=w,
                                    mutation_scale=28, shrinkA=0, shrinkB=0,
                                    linestyle="--" if (dashed and col != "white")
                                    else "-"))


def main():
    im = mpimg.imread(SRC)
    h, w = im.shape[:2]                                      # (487, 960)
    fig, ax = plt.subplots(figsize=(w / 130, h / 130))
    ax.imshow(im)
    ax.set_xlim(0, w); ax.set_ylim(h, 0); ax.axis("off")

    # ---- LEFT = LPSCl (comp1): blue intra-cage + red blocked inter-cage ----
    arrow(ax, (200, 235), (258, 200), BLUE)                 # intra-cage
    arrow(ax, (150, 165), (330, 165), RED, dashed=True)     # inter-cage blocked

    # ---- RIGHT = LPSCl1.6 (modelc): blue intra-cage + green open inter-cage ----
    arrow(ax, (680, 235), (738, 200), BLUE)                 # intra-cage
    arrow(ax, (628, 165), (812, 165), GREEN)                # inter-cage opens

    fig.tight_layout(pad=0.1)
    fig.savefig(OUT, dpi=170, bbox_inches="tight", facecolor="white")
    print(f"-> {OUT}")


if __name__ == "__main__":
    main()
