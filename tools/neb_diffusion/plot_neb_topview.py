#!/usr/bin/env python3
"""Top-view render of Li adatom NEB path for paper figure (g).

Reads a multi-frame xyz (one frame per NEB image, written by ASE NEB),
identifies the adatom (by convention: last atom — added by run_neb_uma.py),
and renders a top-down (xy) view with:
  - Slab atoms in the topmost layer(s): N (blue) and Li (black/gray)
  - Adatom positions at all NEB images, colored initial (pale) → final (dark),
    matching Cui 2023 ACS Nano Figure 2c style (Initial / Diffusing / Final Li)

Designed for Li3N (001) path A, but works for any NEB xyz where the adatom
is appended last to a hexagonal slab.

Usage:
    python3 plot_neb_topview.py \\
        --xyz /data/.../neb_path_final.xyz \\
        --out /data/.../topview_li3n.png \\
        --top_z_thresh 2.5 --replicate 2 2
"""
import argparse
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt


ELEM_COLOR = {
    "N":  "#3a6ea5",   # blue
    "Li": "#1a1a1a",   # near-black (slab Li)
    "C":  "#1a1a1a",   # carbon (for LiC6 reuse)
}
ELEM_SIZE = {
    "N":  140,
    "Li": 90,
    "C":  90,
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--xyz", required=True, help="neb_path_final.xyz (multi-frame)")
    ap.add_argument("--out", required=True, help="output png")
    ap.add_argument("--adatom_idx", type=int, default=-1,
                    help="adatom atom index (default: last)")
    ap.add_argument("--top_z_thresh", type=float, default=2.5,
                    help="show slab atoms within this Å of slab z_max")
    ap.add_argument("--replicate", type=int, nargs=2, default=[2, 2],
                    help="replicate slab atoms in (±x, ±y) for context")
    ap.add_argument("--cmap", default="YlOrBr",
                    help="matplotlib cmap for adatom gradient (pale→dark)")
    ap.add_argument("--cmap_range", type=float, nargs=2, default=[0.30, 0.95])
    ap.add_argument("--xy_pad", type=float, default=3.5,
                    help="±padding around adatom path (Å)")
    ap.add_argument("--title", default=None)
    ap.add_argument("--dpi", type=int, default=300)
    args = ap.parse_args()

    from ase.io import read
    images = read(args.xyz, index=":")
    n_img = len(images)
    print(f"Loaded {n_img} images from {args.xyz}")

    ref = images[0]
    n_atoms = len(ref)
    aidx = args.adatom_idx if args.adatom_idx >= 0 else n_atoms + args.adatom_idx
    print(f"Adatom index: {aidx} ({ref.symbols[aidx]})")

    # Slab mask = all except adatom
    slab_mask = np.ones(n_atoms, dtype=bool)
    slab_mask[aidx] = False

    pos = ref.positions
    z = pos[:, 2]
    z_slab_max = z[slab_mask].max()
    show_mask = slab_mask & (z > z_slab_max - args.top_z_thresh)
    symbols = np.array(ref.get_chemical_symbols())
    print(f"Top-layer atoms shown: {show_mask.sum()} "
          f"({dict(zip(*np.unique(symbols[show_mask], return_counts=True)))})")

    # Adatom positions across NEB images
    ada = np.array([img.positions[aidx] for img in images])
    print(f"Adatom path: x=[{ada[:,0].min():.2f},{ada[:,0].max():.2f}], "
          f"y=[{ada[:,1].min():.2f},{ada[:,1].max():.2f}], "
          f"z=[{ada[:,2].min():.2f},{ada[:,2].max():.2f}]")

    fig, ax = plt.subplots(figsize=(6.5, 6.0))

    # Replicate slab atoms across neighboring cells for visual context
    nx, ny = args.replicate
    cell = ref.cell.array
    elems_present = sorted(set(symbols[show_mask]))

    # Plot slab atoms (replicas + central) — order: smaller markers on top
    for ix in range(-nx, nx + 1):
        for iy in range(-ny, ny + 1):
            shift = ix * cell[0] + iy * cell[1]
            for elem in elems_present:
                m = show_mask & (symbols == elem)
                if not m.any():
                    continue
                xy = pos[m, :2] + shift[:2]
                ax.scatter(
                    xy[:, 0], xy[:, 1],
                    s=ELEM_SIZE.get(elem, 90),
                    c=ELEM_COLOR.get(elem, "#888"),
                    edgecolors='k', linewidths=0.5,
                    zorder=3 if elem == "N" else 2,
                    label=elem if (ix == 0 and iy == 0) else None,
                )

    # Adatom path: faint connecting line
    ax.plot(ada[:, 0], ada[:, 1], '-', color='#888', lw=1.0, alpha=0.5, zorder=5)

    # Adatom positions colored by image index
    cmap = plt.get_cmap(args.cmap)
    colors_adatom = cmap(np.linspace(args.cmap_range[0], args.cmap_range[1], n_img))

    for i, (p, c) in enumerate(zip(ada, colors_adatom)):
        label = None
        if i == 0:
            label = "Initial Li"
        elif i == n_img - 1:
            label = "Final Li"
        elif i == n_img // 2:
            label = "Diffusing Li"
        ax.scatter(p[0], p[1], s=240, c=[c],
                   edgecolors='k', linewidths=1.2, zorder=10, label=label)

    # View window: snug around adatom path
    xmin, xmax = ada[:, 0].min() - args.xy_pad, ada[:, 0].max() + args.xy_pad
    ymin, ymax = ada[:, 1].min() - args.xy_pad, ada[:, 1].max() + args.xy_pad
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_aspect('equal')
    ax.set_xlabel('x (Å)')
    ax.set_ylabel('y (Å)')
    if args.title:
        ax.set_title(args.title)
    ax.legend(loc='upper right', fontsize=9, framealpha=0.92)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(out, dpi=args.dpi, bbox_inches='tight')
    print(f"\n→ {out}")


if __name__ == "__main__":
    main()
