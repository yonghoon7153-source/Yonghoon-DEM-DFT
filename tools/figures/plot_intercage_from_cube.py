#!/usr/bin/env python3
"""plot_intercage_from_cube.py — clean inter-cage Li-density figure FROM the cube
(gabia). Fixes the "weird dots" by regenerating the c-axis projection straight
from the raw Li-density cube; framework markers (if shown) are projected from
the cube's OWN atom coordinates, so they land correctly. Dots are OFF by
default. Overlays blue/green/red migration arrows.

  python3 plot_intercage_from_cube.py \
    --left  comp1_Cl1.0_T600_Li.cube:"comp1 (LPSCl)" \
    --right modelc_Cl1.6_T600_Li.cube:"modelc (LPSCl1.6)" \
    --gamma 0.45 --out intercage_clean.png      # add --cl for correct Cl dots

Edit ARROWS_L / ARROWS_R below (fractional panel coords, y up) to nudge the
arrows onto the actual bright cores / dark gaps. numpy + matplotlib only.

Arrow colour meaning:
  blue  (solid)  intra-cage hop (fast local)
  red   (dashed) inter-cage gap blocked (comp1) -> high Ea
  green (solid)  inter-cage bridge, percolates (modelc)
"""
import numpy as np, argparse
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

BLUE, RED, GREEN = "#1f77b4", "#d62728", "#2ca02c"

# (x0, y0, x1, y1, color, dashed) in fractional panel coords (y up). EDIT ME.
ARROWS_L = [                                   # comp1 (LPSCl)
    (0.18, 0.55, 0.30, 0.63, BLUE, False),     # intra-cage (in a bright core)
    (0.24, 0.40, 0.56, 0.40, RED, True),       # inter-cage gap, blocked
]
ARROWS_R = [                                   # modelc (LPSCl1.6)
    (0.18, 0.62, 0.30, 0.69, BLUE, False),     # intra-cage
    (0.20, 0.45, 0.50, 0.50, GREEN, False),    # inter-cage bridge 1
    (0.50, 0.50, 0.80, 0.56, GREEN, False),    # inter-cage bridge 2 (chain)
]


def read_cube(path):
    L = open(path).read().splitlines()
    na = int(L[2].split()[0])
    n = [int(L[3 + i].split()[0]) for i in range(3)]
    vox = np.array([[float(x) for x in L[3 + i].split()[1:4]] for i in range(3)])
    cell = np.array([vox[i] * n[i] for i in range(3)])   # lattice vectors (Bohr)
    Z, R = [], []
    for i in range(na):
        t = L[6 + i].split()
        Z.append(int(t[0])); R.append([float(t[2]), float(t[3]), float(t[4])])
    vals = []
    for ln in L[6 + na:]:
        s = ln.split()
        if s:
            vals += [float(x) for x in s]
    rho = np.array(vals, float).reshape(n[0], n[1], n[2])
    return rho, cell, np.array(Z), np.array(R, float).reshape(-1, 3)


def draw_arrow(ax, x0, y0, x1, y1, color, dashed):
    for col, w, z in (("white", 7, 4), (color, 4, 5)):     # white halo then colour
        ax.annotate("", xy=(x1, y1), xytext=(x0, y0), zorder=z,
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=w,
                                    mutation_scale=26, shrinkA=0, shrinkB=0,
                                    linestyle="--" if (dashed and col != "white")
                                    else "-"))


def panel(ax, spec, arrows, gamma, show_cl):
    cube, _, title = spec.partition(":"); title = title or cube
    rho, cell, Z, R = read_cube(cube)
    P = rho.sum(axis=2)                                     # c-axis projection
    P = P / P.max()
    im = ax.imshow(P.T, origin="lower", extent=[0, 1, 0, 1], aspect="equal",
                   cmap="inferno", norm=mcolors.PowerNorm(gamma, 0, 1))
    ax.set_title(title, fontsize=14)
    ax.set_xticks([]); ax.set_yticks([])
    if show_cl and len(R):
        frac = (R @ np.linalg.inv(cell)) % 1.0
        cl = Z == 17
        if cl.any():
            ax.scatter(frac[cl, 0], frac[cl, 1], s=90, c=GREEN,
                       edgecolors="white", linewidths=1.5, zorder=6,
                       label="Cl (inter-cage)")
            ax.legend(loc="upper left", fontsize=9, framealpha=0.85)
    for (x0, y0, x1, y1, c, dash) in arrows:
        draw_arrow(ax, x0, y0, x1, y1, c, dash)
    return im


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--left", required=True, help='cube:title')
    ap.add_argument("--right", required=True, help='cube:title')
    ap.add_argument("--gamma", type=float, default=0.45)
    ap.add_argument("--cl", action="store_true", help="show correct Cl dots")
    ap.add_argument("--no-arrows", action="store_true")
    ap.add_argument("--out", default="intercage_clean.png")
    a = ap.parse_args()
    fig, axes = plt.subplots(1, 2, figsize=(13, 6.2))
    for ax, spec, arrows in ((axes[0], a.left, ARROWS_L),
                             (axes[1], a.right, ARROWS_R)):
        im = panel(ax, spec, [] if a.no_arrows else arrows, a.gamma, a.cl)
        fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04,
                     label=f"Li density (norm, gamma={a.gamma})")
    fig.tight_layout(); fig.savefig(a.out, dpi=150)
    print("->", a.out)


if __name__ == "__main__":
    main()
