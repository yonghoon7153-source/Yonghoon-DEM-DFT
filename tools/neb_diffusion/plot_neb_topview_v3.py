#!/usr/bin/env python3
"""NEB top-view render v3 — ASE plot_atoms shaded spheres + clean bonds.

Uses ase.visualize.plot.plot_atoms() for the slab atom rendering, which
provides VESTA-like shaded spheres (much closer to paper figure quality
than raw matplotlib scatter or hand-drawn highlights).

Bonds (nearest-neighbor pairs in the visible top layer + replicas) are
drawn manually as gray lines underneath the atoms.

Adatom positions are overlaid as solid circles with a dark-red edge ring,
matching Cui 2023 ACS Nano Fig 2c style (Initial/Diffusing/Final).

Usage:
    python3 plot_neb_topview_v3.py \\
        --xyz /path/to/neb_path_final.xyz \\
        --out /path/to/topview.png \\
        --title 'Li$_3$N (001)'

Notes on element sizing (radii in Å, jmol-style sphere radius for display):
    Li  0.70   N  0.55   C  0.50
"""
import argparse
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle


ELEM_COLOR = {
    "N":  "#3F7BB6",  # paper-blue
    "Li": "#1a1a1a",  # black
    "C":  "#222222",  # near-black graphite
}
# Display radii in Å for plot_atoms (jmol-like)
ELEM_RADII_DISPLAY = {
    "N":  0.55,
    "Li": 0.70,
    "C":  0.50,
}
# Bond cutoffs (Å) — ONLY true nearest neighbors
BOND_CUTOFFS = {
    frozenset(["Li", "N"]):  2.4,
    frozenset(["Li", "Li"]): 2.4,
    frozenset(["N",  "N"]):  0.0,
    frozenset(["C",  "C"]):  1.6,
    frozenset(["Li", "C"]):  2.6,
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--xyz", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--adatom_idx", type=int, default=-1)
    ap.add_argument("--top_z_thresh", type=float, default=2.5)
    ap.add_argument("--replicate", type=int, nargs=2, default=[2, 2])
    ap.add_argument("--xy_pad", type=float, default=4.5)
    ap.add_argument("--cmap", default="YlOrBr")
    ap.add_argument("--cmap_range", type=float, nargs=2, default=[0.35, 0.95])
    ap.add_argument("--adatom_radius", type=float, default=0.55)
    ap.add_argument("--adatom_edge_color", default="#8B1A1A")
    ap.add_argument("--adatom_edge_lw", type=float, default=2.0)
    ap.add_argument("--adatom_show", choices=["all", "three"], default="three")
    ap.add_argument("--bond_lw", type=float, default=1.0)
    ap.add_argument("--bond_color", default="#555555")
    ap.add_argument("--title", default=None)
    ap.add_argument("--dpi", type=int, default=300)
    ap.add_argument("--figsize", type=float, nargs=2, default=[6.5, 6.2])
    ap.add_argument("--atom_scale", type=float, default=1.0,
                    help="multiply display radii by this factor")
    args = ap.parse_args()

    from ase.io import read
    from ase.visualize.plot import plot_atoms
    from ase import Atoms

    images = read(args.xyz, index=":")
    n_img = len(images)
    ref = images[0]
    n = len(ref)
    aidx = args.adatom_idx if args.adatom_idx >= 0 else n + args.adatom_idx
    slab_mask = np.ones(n, dtype=bool); slab_mask[aidx] = False

    pos = ref.positions
    z = pos[:, 2]
    z_top = z[slab_mask].max()
    show_idx = np.where(slab_mask & (z > z_top - args.top_z_thresh))[0]
    syms_arr = np.array(ref.get_chemical_symbols())
    elems_present = sorted(set(syms_arr[show_idx]))
    print(f"Loaded {n_img} images; adatom idx {aidx} ({syms_arr[aidx]})")
    print(f"Top layer: {len(show_idx)} atoms, {elems_present}")

    # Adatom positions
    ada = np.array([img.positions[aidx] for img in images])

    # Plot window
    xmin = ada[:, 0].min() - args.xy_pad
    xmax = ada[:, 0].max() + args.xy_pad
    ymin = ada[:, 1].min() - args.xy_pad
    ymax = ada[:, 1].max() + args.xy_pad

    # Build replicated Atoms object of top layer
    nx, ny = args.replicate
    cell = ref.cell.array
    positions_all = []
    symbols_all = []
    for ix in range(-nx, nx + 1):
        for iy in range(-ny, ny + 1):
            shift = ix * cell[0] + iy * cell[1]
            for i in show_idx:
                x = pos[i, 0] + shift[0]
                y = pos[i, 1] + shift[1]
                if xmin - 2 < x < xmax + 2 and ymin - 2 < y < ymax + 2:
                    positions_all.append([x, y, pos[i, 2]])
                    symbols_all.append(syms_arr[i])
    print(f"In-window atoms (with replicas): {len(positions_all)}")

    top_atoms = Atoms(symbols=symbols_all, positions=np.array(positions_all))

    fig, ax = plt.subplots(figsize=tuple(args.figsize))

    # 1. Bonds (drawn first, below atoms)
    A = np.array(positions_all)[:, :2]
    S = symbols_all
    if len(A) > 1:
        D = np.linalg.norm(A[:, None, :] - A[None, :, :], axis=-1)
        ii, jj = np.where((D > 0.1) & np.triu(np.ones_like(D, dtype=bool), k=1))
        for k in range(len(ii)):
            i, j = ii[k], jj[k]
            cutoff = BOND_CUTOFFS.get(frozenset([S[i], S[j]]), 0)
            if D[i, j] < cutoff:
                ax.plot([A[i, 0], A[j, 0]], [A[i, 1], A[j, 1]],
                        '-', color=args.bond_color, lw=args.bond_lw,
                        alpha=0.85, zorder=2, solid_capstyle='round')

    # 2. Slab atoms via ASE plot_atoms (shaded spheres)
    custom_colors = [ELEM_COLOR.get(s, "#666") for s in symbols_all]
    custom_radii = [ELEM_RADII_DISPLAY.get(s, 0.5) * args.atom_scale
                    for s in symbols_all]
    plot_atoms(top_atoms, ax=ax, rotation='0x,0y,0z',
               colors=custom_colors, radii=custom_radii,
               show_unit_cell=0)

    # 3. Adatom trajectory
    ax.plot(ada[:, 0], ada[:, 1], '-', color='#888', lw=1.2,
            alpha=0.5, zorder=5)

    # 4. Adatoms (paper style: solid color + dark-red edge ring)
    if args.adatom_show == "three":
        show_imgs = [0, n_img // 2, n_img - 1]
    else:
        show_imgs = list(range(n_img))

    cmap = plt.get_cmap(args.cmap)
    n_show = len(show_imgs)
    cvals = np.linspace(args.cmap_range[0], args.cmap_range[1], n_show)
    cols = cmap(cvals)
    for img_i, c in zip(show_imgs, cols):
        p = ada[img_i]
        ax.add_patch(Circle((p[0], p[1]), args.adatom_radius,
                            facecolor=c, edgecolor=args.adatom_edge_color,
                            linewidth=args.adatom_edge_lw, zorder=10))

    # Legend (top, multi-column, frameless)
    handles = []
    for s in elems_present:
        handles.append(plt.Line2D([0], [0], marker='o', linestyle='',
                                  markerfacecolor=ELEM_COLOR.get(s, "#666"),
                                  markeredgecolor='#000', markeredgewidth=0.6,
                                  markersize=10, label=s))
    if args.adatom_show == "three":
        lbls = ["Initial Li", "Diffusing Li", "Final Li"]
        for lbl, frac in zip(lbls, cvals):
            handles.append(plt.Line2D([0], [0], marker='o', linestyle='',
                                      markerfacecolor=cmap(frac),
                                      markeredgecolor=args.adatom_edge_color,
                                      markeredgewidth=1.5,
                                      markersize=11, label=lbl))
    else:
        handles.append(plt.Line2D([0], [0], marker='o', linestyle='',
                                  markerfacecolor=cmap(0.5),
                                  markeredgecolor=args.adatom_edge_color,
                                  markeredgewidth=1.5,
                                  markersize=11, label="Li adatom"))

    ax.legend(handles=handles, loc='upper center',
              ncol=min(len(handles), 5),
              fontsize=9, frameon=False,
              bbox_to_anchor=(0.5, 1.06),
              handletextpad=0.4, columnspacing=1.0)

    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_aspect('equal')
    ax.axis('off')

    if args.title:
        ax.text(0.5, -0.03, args.title, transform=ax.transAxes,
                ha='center', va='top', fontsize=12)

    out = Path(args.out); out.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(out, dpi=args.dpi, bbox_inches='tight', facecolor='white')
    print(f"\n→ {out}")


if __name__ == "__main__":
    main()
