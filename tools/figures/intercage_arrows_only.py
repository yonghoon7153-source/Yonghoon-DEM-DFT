#!/usr/bin/env python3
"""intercage_arrows_only.py — Li-density inter-cage figure with ARROWS ONLY.

Takes the Li-density heatmap (docs/figures/elf_licl/Li_density_core_spread_
comp1_modelc.png) and overlays ONLY blue/green/red migration arrows — no text
boxes, no extra markers. The baked-in site dots (orange = free S2- cage centre,
green = Cl inter-cage gateway) and the panel titles stay (they are part of the
base PNG; removing them needs the raw density, which lives on gabia).

Colour meaning (told in chat, not on the figure):
  blue  (solid)        intra-cage hop      fast local motion inside a cage core
  red   (dashed)       inter-cage gap      LPSCl: dark gap, blocked -> high Ea
  green (solid, chain) inter-cage bridge   LPSCl1.6: connected -> percolates

  python3 intercage_arrows_only.py
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

SRC = "docs/figures/elf_licl/Li_density_core_spread_comp1_modelc.png"
OUT = "docs/figures/elf_licl/intercage_arrows_only.png"
BLUE, RED, GREEN = "#1f77b4", "#d62728", "#2ca02c"


def main():
    im = mpimg.imread(SRC)[110:, :, :]      # crop the verbose top title
    H, W = im.shape[:2]
    fig = plt.figure(figsize=(W / 190, H / 190))
    ax = fig.add_axes([0, 0, 1, 1]); ax.imshow(im); ax.axis("off")

    def fx(v): return v * W
    def fy(v): return v * H

    def arrow(p0, p1, color, dashed=False, lw=4.0):
        for c, w, z in ((("white"), lw + 3.5, 4), (color, lw, 5)):
            ax.annotate("", xy=(fx(p1[0]), fy(p1[1])),
                        xytext=(fx(p0[0]), fy(p0[1])), zorder=z,
                        arrowprops=dict(arrowstyle="-|>", color=c, lw=w,
                                        mutation_scale=30, shrinkA=0, shrinkB=0,
                                        linestyle="--" if (dashed and c != "white")
                                        else "-"))

    # ---- LEFT = comp1 (LPSCl): blue intra-cage + red blocked inter-cage ----
    arrow((0.15, 0.47), (0.23, 0.38), BLUE)                  # intra-cage (in a core)
    arrow((0.21, 0.585), (0.40, 0.585), RED, dashed=True)    # inter-cage gap (blocked)

    # ---- RIGHT = modelc (LPSCl1.6): blue intra-cage + green open inter-cage ----
    arrow((0.62, 0.45), (0.70, 0.36), BLUE)                  # intra-cage
    arrow((0.61, 0.57), (0.735, 0.48), GREEN)                # inter-cage bridge 1
    arrow((0.735, 0.48), (0.86, 0.42), GREEN)               # inter-cage bridge 2 (chain)

    fig.savefig(OUT, dpi=150, bbox_inches="tight")
    print(f"-> {OUT}  ({W}x{H})")


if __name__ == "__main__":
    main()
