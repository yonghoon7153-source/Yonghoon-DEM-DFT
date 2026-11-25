#!/usr/bin/env python3
"""Top-view render v2 — paper-quality figure for (g) panel.

Targets Cui 2023 ACS Nano Figure 2c style:
- Shaded spheres with white highlight (faux-3D look)
- Auto bond lines between nearest-neighbor surface atoms
- Clean white background, no axes
- Adatom overlay with dark-red edge ring, gradient color (initial pale → final dark)

Usage:
    python3 plot_neb_topview_v2.py \\
        --xyz /path/to/neb_path_final.xyz \\
        --out /path/to/topview.png \\
        --title "Li3N (001)"
"""
import argparse
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle


ELEM_COLOR = {
    "N":  "#3F7BB6",   # paper-blue
    "Li": "#1a1a1a",   # black
    "C":  "#2a2a2a",   # near-black (LiC6 graphite)
}
ELEM_RADIUS_A = {       # display radius in Å (small, like paper)
    "N":  0.32,
    "Li": 0.40,
    "C":  0.30,
}

# Bond cutoffs (Å) — only TRUE nearest neighbors
BOND_CUTOFFS = {
    frozenset(["Li", "N"]):  2.3,   # Li(2)-N nearest = 2.11 Å in Li3N
    frozenset(["Li", "Li"]): 2.3,   # Li(2)-Li(2) nearest = 2.11 Å in basal
    frozenset(["N",  "N"]):  0.0,   # no N-N bonds (would be 3.65 Å, too far)
    frozenset(["C",  "C"]):  1.6,   # graphene C-C = 1.42 Å
    frozenset(["Li", "C"]):  2.5,
}


def simple_atom(ax, x, y, r, color, edge='#000', edge_lw=0.8, zorder=3):
    """Paper-style: solid filled circle with thin black border, no highlight."""
    ax.add_patch(Circle((x, y), r, facecolor=color, edgecolor=edge,
                        linewidth=edge_lw, zorder=zorder))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--xyz", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--adatom_idx", type=int, default=-1)
    ap.add_argument("--top_z_thresh", type=float, default=2.5)
    ap.add_argument("--replicate", type=int, nargs=2, default=[2, 2])
    ap.add_argument("--xy_pad", type=float, default=5.0)
    ap.add_argument("--cmap", default="YlOrBr")
    ap.add_argument("--cmap_range", type=float, nargs=2, default=[0.35, 0.95])
    ap.add_argument("--adatom_radius", type=float, default=0.40)
    ap.add_argument("--adatom_edge_color", default="#8B1A1A")  # dark red
    ap.add_argument("--adatom_show",
                    choices=["all", "endpoints", "three"], default="three",
                    help="all=all 7 images; endpoints=init+final only; "
                         "three=init+TS(image idx auto-detect)+final (paper style)")
    ap.add_argument("--bond_lw", type=float, default=0.8)
    ap.add_argument("--bond_color", default="#444444")
    ap.add_argument("--title", default=None)
    ap.add_argument("--dpi", type=int, default=300)
    ap.add_argument("--figsize", type=float, nargs=2, default=[6.5, 6.0])
    args = ap.parse_args()

    from ase.io import read
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
    syms = np.array(ref.get_chemical_symbols())
    elems_present = sorted(set(syms[show_idx]))
    print(f"Loaded {n_img} images; adatom idx {aidx} ({syms[aidx]})")
    print(f"Top layer: {len(show_idx)} atoms, elements {elems_present}")

    # Adatom positions across images
    ada = np.array([img.positions[aidx] for img in images])

    # Plot window
    xmin = ada[:, 0].min() - args.xy_pad
    xmax = ada[:, 0].max() + args.xy_pad
    ymin = ada[:, 1].min() - args.xy_pad
    ymax = ada[:, 1].max() + args.xy_pad

    # Build replicated atom list inside (extended) window
    nx, ny = args.replicate
    cell = ref.cell.array
    atoms = []  # list of (x, y, sym)
    for ix in range(-nx, nx + 1):
        for iy in range(-ny, ny + 1):
            shift = ix * cell[0] + iy * cell[1]
            for i in show_idx:
                x = pos[i, 0] + shift[0]
                y = pos[i, 1] + shift[1]
                if xmin - 2 < x < xmax + 2 and ymin - 2 < y < ymax + 2:
                    atoms.append((x, y, syms[i]))
    print(f"In-window atoms (with replicas): {len(atoms)}")

    fig, ax = plt.subplots(figsize=tuple(args.figsize))

    # 1. Bonds
    A = np.array([(a[0], a[1]) for a in atoms])
    S = [a[2] for a in atoms]
    if len(A) > 1:
        diff = A[:, None, :] - A[None, :, :]
        D = np.linalg.norm(diff, axis=-1)
        ii, jj = np.where((D > 0.1) & np.triu(np.ones_like(D, dtype=bool), k=1))
        for k in range(len(ii)):
            i, j = ii[k], jj[k]
            pair = frozenset([S[i], S[j]])
            cutoff = BOND_CUTOFFS.get(pair, 0)
            if D[i, j] < cutoff:
                ax.plot([A[i, 0], A[j, 0]], [A[i, 1], A[j, 1]],
                        '-', color=args.bond_color, lw=args.bond_lw,
                        alpha=0.85, zorder=2, solid_capstyle='round')

    # 2. Slab atoms (simple solid circles, paper style)
    for x, y, s in atoms:
        r = ELEM_RADIUS_A.get(s, 0.30)
        c = ELEM_COLOR.get(s, "#666")
        simple_atom(ax, x, y, r, c, zorder=3)

    # 3. Pick which adatom images to show
    if args.adatom_show == "all":
        show_imgs = list(range(n_img))
    elif args.adatom_show == "endpoints":
        show_imgs = [0, n_img - 1]
    else:  # "three" — initial, TS (max-energy guess = middle), final
        show_imgs = [0, n_img // 2, n_img - 1]

    # Path line (always drawn through all images for trajectory)
    ax.plot(ada[:, 0], ada[:, 1], '-', color='#999', lw=1.0,
            alpha=0.50, zorder=6)

    # 4. Adatoms (red-ringed, paper style)
    cmap = plt.get_cmap(args.cmap)
    n_show = len(show_imgs)
    if n_show == 1:
        cvals = np.array([0.5 * sum(args.cmap_range)])
    else:
        cvals = np.linspace(args.cmap_range[0], args.cmap_range[1], n_show)
    cols = cmap(cvals)
    for img_i, c in zip(show_imgs, cols):
        p = ada[img_i]
        ax.add_patch(Circle((p[0], p[1]), args.adatom_radius,
                            facecolor=c, edgecolor=args.adatom_edge_color,
                            linewidth=1.6, zorder=10))

    # Legend (top)
    handles = []
    for s in elems_present:
        handles.append(plt.Line2D([0], [0], marker='o', linestyle='',
                                  markerfacecolor=ELEM_COLOR.get(s, "#666"),
                                  markeredgecolor='#000',
                                  markersize=9, label=s))
    if args.adatom_show == "three":
        for lbl, frac in [("Initial Li", args.cmap_range[0]),
                          ("Diffusing Li", 0.5 * sum(args.cmap_range)),
                          ("Final Li", args.cmap_range[1])]:
            handles.append(plt.Line2D([0], [0], marker='o', linestyle='',
                                      markerfacecolor=cmap(frac),
                                      markeredgecolor=args.adatom_edge_color,
                                      markeredgewidth=1.2,
                                      markersize=11, label=lbl))
    elif args.adatom_show == "endpoints":
        for lbl, frac in [("Initial Li", args.cmap_range[0]),
                          ("Final Li", args.cmap_range[1])]:
            handles.append(plt.Line2D([0], [0], marker='o', linestyle='',
                                      markerfacecolor=cmap(frac),
                                      markeredgecolor=args.adatom_edge_color,
                                      markeredgewidth=1.2,
                                      markersize=11, label=lbl))
    else:  # all
        handles.append(plt.Line2D([0], [0], marker='o', linestyle='',
                                  markerfacecolor=cmap(0.5),
                                  markeredgecolor=args.adatom_edge_color,
                                  markeredgewidth=1.2,
                                  markersize=11, label="Li adatom"))

    leg = ax.legend(handles=handles, loc='upper center',
                    ncol=min(len(handles), 4),
                    fontsize=9, frameon=False,
                    bbox_to_anchor=(0.5, 1.06),
                    handletextpad=0.4, columnspacing=1.2)

    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_aspect('equal')
    ax.axis('off')

    if args.title:
        ax.text(0.5, -0.02, args.title, transform=ax.transAxes,
                ha='center', va='top', fontsize=12, fontstyle='italic')

    out = Path(args.out); out.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(out, dpi=args.dpi, bbox_inches='tight', facecolor='white')
    print(f"\n→ {out}")


if __name__ == "__main__":
    main()
