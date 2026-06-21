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
# Tuned to the real c-axis projections of the AIMD Li-density cubes.
ARROWS_L = [                                   # comp1 (LPSCl): bright core (0.19,0.47)
    (0.15, 0.44, 0.22, 0.51, BLUE, False),     # intra-cage (inside the bright core)
    (0.25, 0.47, 0.43, 0.48, RED, True),       # inter-cage -> dark gap (0.44,0.48): blocked
]
ARROWS_R = [                                   # modelc (LPSCl1.6): bright corridor at left
    (0.02, 0.60, 0.085, 0.70, BLUE, False),    # intra-cage (in the bright core)
    (0.10, 0.62, 0.14, 0.40, GREEN, False),    # inter-cage corridor 1 (no dark wall)
    (0.14, 0.40, 0.42, 0.24, GREEN, False),    # inter-cage corridor 2 (chain -> percolates)
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


def draw_arrow(ax, x0, y0, x1, y1, color, dashed, lw=4, scale=26):
    for col, w, z in (("white", lw + 3, 4), (color, lw, 5)):  # white halo then colour
        ax.annotate("", xy=(x1, y1), xytext=(x0, y0), zorder=z,
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=w,
                                    mutation_scale=scale, shrinkA=0, shrinkB=0,
                                    linestyle="--" if (dashed and col != "white")
                                    else "-"))


def find_cores(P, thr, min_dist):
    """Fractional (x=a, y=b) positions of every bright cage core (local maxima)."""
    from scipy.ndimage import maximum_filter, label, center_of_mass
    peaks = (P == maximum_filter(P, size=min_dist, mode="wrap")) & (P >= thr * P.max())
    lab, n = label(peaks)
    if n == 0:
        return []
    na, nb = P.shape
    return [(c[0] / na, c[1] / nb) for c in center_of_mass(P, lab, range(1, n + 1))]


def panel(ax, spec, arrows, gamma, show_cl, all_intra, core_thr, core_dist):
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
    if all_intra:                  # one short blue intra-cage arrow per cage core
        for (x, y) in find_cores(P, core_thr, core_dist):
            draw_arrow(ax, x - 0.022, y - 0.028, x + 0.022, y + 0.028,
                       BLUE, False, lw=2.6, scale=16)
        arrows = [a for a in arrows if a[4] != BLUE]        # drop the single manual blue
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
    ap.add_argument("--all-intra", action="store_true",
                    help="blue intra-cage arrow at EVERY cage core")
    ap.add_argument("--core-thr", type=float, default=0.45,
                    help="core = local max above this fraction of peak")
    ap.add_argument("--core-dist", type=int, default=7,
                    help="min core separation (voxels)")
    ap.add_argument("--out", default="intercage_clean.png")
    a = ap.parse_args()
    fig, axes = plt.subplots(1, 2, figsize=(13, 6.2))
    for ax, spec, arrows in ((axes[0], a.left, ARROWS_L),
                             (axes[1], a.right, ARROWS_R)):
        im = panel(ax, spec, [] if a.no_arrows else arrows, a.gamma, a.cl,
                   a.all_intra, a.core_thr, a.core_dist)
        fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04,
                     label=f"Li density (norm, gamma={a.gamma})")
    fig.tight_layout(); fig.savefig(a.out, dpi=150)
    print("->", a.out)


if __name__ == "__main__":
    main()
