#!/usr/bin/env python3
"""annot_bvse_arrows.py — overlay color-coded migration arrows on the BVSE
low-channel figure (docs/figures/deck_extracted/bvse_channels.png).

Arrows only (no redraw). Colour meaning:
  blue  (solid)        intra-cage hop          fast local motion inside a cage
  red   (dashed, x)    inter-cage BOTTLENECK   LPSCl: rate-limiting -> Ea
  green (solid, check) inter-cage OPENS        LPSCl1.6: route percolates

Story: the static low-BVSE channel actually SHRINKS (8.75 -> 7.4 %, -15 %),
yet sigma x4. BVSE sees only the intra-cage channel; the win is the inter-cage
bottleneck, which is blocked in LPSCl (red) and opened by anti-site disorder in
LPSCl1.6 (green). Pairs with the percolation barrier F* (0.191 -> 0.078 eV).

  python3 annot_bvse_arrows.py
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.image as mpimg
import matplotlib.patheffects as pe

HALO = [pe.withStroke(linewidth=3.5, foreground="white")]

SRC = "docs/figures/deck_extracted/bvse_channels.png"
OUT = "docs/figures/ionic/bvse_channels_arrows.png"

BLUE, RED, GREEN = "#1f77b4", "#d62728", "#2ca02c"


def arrow(ax, p0, p1, color, dashed=False, lw=3.0):
    # white halo underneath so the arrow pops against the blue point cloud
    ax.annotate("", xy=p1, xytext=p0,
                arrowprops=dict(arrowstyle="-|>", color="white", lw=lw + 3.0,
                                mutation_scale=28, shrinkA=0, shrinkB=0,
                                linestyle="-"))
    ax.annotate("", xy=p1, xytext=p0,
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw,
                                mutation_scale=26, shrinkA=0, shrinkB=0,
                                linestyle="--" if dashed else "-"))


def main():
    im = mpimg.imread(SRC)
    h, w = im.shape[:2]            # (487, 960)
    band = 110                     # white header strip (px) above the image
    fig, ax = plt.subplots(figsize=(w / 125, (h + band) / 125))
    ax.imshow(im)                  # pixel coords, y downward (0=top)
    ax.set_xlim(0, w); ax.set_ylim(h, -band); ax.axis("off")
    ax.set_facecolor("white")

    # ---- panel labels in the top white band ----
    ax.text(240, -78, "LPSCl", color="black", fontsize=12, ha="center",
            fontweight="bold")
    ax.text(720, -78, "LPSCl1.6", color="black", fontsize=12, ha="center",
            fontweight="bold")

    # ---- LEFT panel = LPSCl (comp1), cloud ~ center (240, 215) ----
    arrow(ax, (200, 235), (258, 200), BLUE)                       # intra-cage
    arrow(ax, (150, 150), (330, 150), RED, dashed=True)           # inter-cage blocked
    ax.text(343, 150, "✗", color=RED, fontsize=18, ha="center",
            va="center", fontweight="bold", path_effects=HALO)

    # ---- RIGHT panel = LPSCl1.6 (modelc), cloud ~ center (720, 215) ----
    arrow(ax, (680, 235), (738, 200), BLUE)                       # intra-cage
    arrow(ax, (628, 150), (812, 150), GREEN)                      # inter-cage open
    ax.text(825, 150, "✓", color=GREEN, fontsize=18, ha="center",
            va="center", fontweight="bold", path_effects=HALO)

    # ---- compact legend (centered in the top band) ----
    handles = [
        Line2D([0], [0], color=BLUE, lw=3, label="intra-cage hop (fast, local)"),
        Line2D([0], [0], color=RED, lw=3, ls="--",
               label="inter-cage bottleneck = Ea  (blocked)"),
        Line2D([0], [0], color=GREEN, lw=3,
               label="inter-cage opens (percolates)"),
    ]
    ax.legend(handles=handles, loc="lower center", ncol=3, fontsize=8.5,
              framealpha=0.0, bbox_to_anchor=(0.5, 1.005), borderaxespad=0,
              handlelength=2.4, columnspacing=1.4)

    fig.tight_layout(pad=0.2)
    fig.savefig(OUT, dpi=170, bbox_inches="tight", facecolor="white")
    print(f"-> {OUT}")


if __name__ == "__main__":
    main()
