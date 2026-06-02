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
ELEM_RADIUS_A = {       # display radius in Å (NOT van der Waals)
    "N":  0.45,
    "Li": 0.60,
    "C":  0.50,
}

# Bond cutoffs (Å) — pairs of element types
BOND_CUTOFFS = {
    frozenset(["Li", "N"]):  2.5,
    frozenset(["Li", "Li"]): 2.4,   # only short Li-Li (honeycomb edge if present)
    frozenset(["N",  "N"]):  3.8,   # N-N hex outline (Li3N basal honeycomb dual)
    frozenset(["C",  "C"]):  1.7,
    frozenset(["Li", "C"]):  2.5,
}


def shaded_sphere(ax, x, y, r, color, edge='#222', edge_lw=0.6, zorder=3):
    """Draw a 2D shaded circle (faux-3D sphere)."""
    ax.add_patch(Circle((x, y), r, facecolor=color, edgecolor=edge,
                        linewidth=edge_lw, zorder=zorder))
    # Highlight: white-ish smaller circle offset up-left
    ax.add_patch(Circle((x - r * 0.30, y + r * 0.30), r * 0.38,
                        facecolor=(1, 1, 1, 0.40), edgecolor='none',
                        zorder=zorder + 1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--xyz", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--adatom_idx", type=int, default=-1)
    ap.add_argument("--top_z_thresh", type=float, default=2.5)
    ap.add_argument("--replicate", type=int, nargs=2, default=[3, 3])
    ap.add_argument("--xy_pad", type=float, default=3.5)
    ap.add_argument("--cmap", default="YlOrBr")
    ap.add_argument("--cmap_range", type=float, nargs=2, default=[0.30, 0.95])
    ap.add_argument("--adatom_radius", type=float, default=0.70)
    ap.add_argument("--adatom_edge_color", default="#8B1A1A")  # dark red
    ap.add_argument("--bond_lw", type=float, default=1.5)
    ap.add_argument("--bond_color", default="#222222")
    ap.add_argument("--title", default=None)
    ap.add_argument("--dpi", type=int, default=300)
    ap.add_argument("--figsize", type=float, nargs=2, default=[6.0, 6.0])
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

    # 2. Slab atoms (shaded spheres)
    for x, y, s in atoms:
        r = ELEM_RADIUS_A.get(s, 0.40)
        c = ELEM_COLOR.get(s, "#666")
        shaded_sphere(ax, x, y, r, c, zorder=3)

    # 3. Adatom path: subtle connecting line
    ax.plot(ada[:, 0], ada[:, 1], '-', color='#999', lw=1.0,
            alpha=0.50, zorder=6)

    # 4. Adatoms (red-ringed gradient spheres)
    cmap = plt.get_cmap(args.cmap)
    cols = cmap(np.linspace(args.cmap_range[0], args.cmap_range[1], n_img))
    for p, c in zip(ada, cols):
        ax.add_patch(Circle((p[0], p[1]), args.adatom_radius,
                            facecolor=c, edgecolor=args.adatom_edge_color,
                            linewidth=1.8, zorder=10))
        ax.add_patch(Circle((p[0] - args.adatom_radius * 0.30,
                             p[1] + args.adatom_radius * 0.30),
                            args.adatom_radius * 0.38,
                            facecolor=(1, 1, 1, 0.45), edgecolor='none',
                            zorder=11))

    # Legend (top, no frame, multi-column)
    handles = []
    for s in elems_present:
        handles.append(plt.Line2D([0], [0], marker='o', linestyle='',
                                  markerfacecolor=ELEM_COLOR.get(s, "#666"),
                                  markeredgecolor='#222',
                                  markersize=11, label=s))
    for lbl, frac in [("Initial Li", args.cmap_range[0]),
                      ("Diffusing Li", 0.5 * sum(args.cmap_range)),
                      ("Final Li", args.cmap_range[1])]:
        handles.append(plt.Line2D([0], [0], marker='o', linestyle='',
                                  markerfacecolor=cmap(frac),
                                  markeredgecolor=args.adatom_edge_color,
                                  markeredgewidth=1.5,
                                  markersize=13, label=lbl))
    ax.legend(handles=handles, loc='upper center', ncol=len(handles),
              fontsize=10, frameon=False, bbox_to_anchor=(0.5, 1.02))

    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_aspect('equal')
    ax.axis('off')

    if args.title:
        ax.text(0.5, -0.03, args.title, transform=ax.transAxes,
                ha='center', va='top', fontsize=14, fontstyle='italic')

    out = Path(args.out); out.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(out, dpi=args.dpi, bbox_inches='tight', facecolor='white')
    print(f"\n→ {out}")


if __name__ == "__main__":
    main()
