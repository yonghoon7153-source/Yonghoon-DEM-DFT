#!/usr/bin/env python3
"""Build a Li3N (001) slab for Li adatom NEB.

Crystal: Li3N, P6/mmm (No. 191), Wang 1981
  a = 3.65 Å, c = 3.87 Å
  N  at (0, 0, 0)
  Li(1) (axial) at (0, 0, 1/2)
  Li(2) (in-plane) at (1/3, 2/3, 0) and (2/3, 1/3, 0)

(001) facet = c-axis ⊥ surface. Two termination choices per unit cell along c:
  - z=0 layer: N + Li(2) honeycomb (paper Figure 2a shows this layer)
  - z=c/2 layer: Li(1) only (sparse)

Paper diffuses Li adatom across the N-rich (001) layer; we expose that as the
top surface.

Usage:
    python3 build_li3n_slab.py \\
        --repeat 3 3 --n_layers 4 --vacuum 15 \\
        --out_init <out>/li3n_001_init.xyz
"""
import argparse
from pathlib import Path
import numpy as np


def build_li3n_bulk():
    """Wang 1981 Li3N hexagonal unit cell."""
    from ase import Atoms
    a, c = 3.65, 3.87
    cell = [[a, 0, 0], [-a/2, a*np.sqrt(3)/2, 0], [0, 0, c]]
    frac = np.array([
        [0,   0,   0],     # N
        [0,   0,   0.5],   # Li(1) axial
        [1/3, 2/3, 0],     # Li(2)a in-plane
        [2/3, 1/3, 0],     # Li(2)b in-plane
    ])
    symbols = ['N', 'Li', 'Li', 'Li']
    positions = frac @ np.array(cell)
    return Atoms(symbols=symbols, positions=positions, cell=cell, pbc=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repeat", type=int, nargs=2, default=[3, 3],
                    help="in-plane repeat (default 3 3 → 36-atom surface layer)")
    ap.add_argument("--n_layers", type=int, default=4,
                    help="number of unit cells along c (each = 2 atomic planes)")
    ap.add_argument("--vacuum", type=float, default=15.0)
    ap.add_argument("--out_init", required=True,
                    help="output xyz path for the bare slab (no adatom)")
    args = ap.parse_args()

    out = Path(args.out_init); out.parent.mkdir(parents=True, exist_ok=True)

    bulk = build_li3n_bulk()
    print(f"Bulk Li3N: {len(bulk)} atoms, "
          f"a={bulk.cell.cellpar()[0]:.3f}, c={bulk.cell.cellpar()[2]:.3f} Å, "
          f"V={bulk.get_volume():.2f} Å³")

    nx, ny = args.repeat
    nz = args.n_layers
    slab = bulk.repeat((nx, ny, nz))
    print(f"After repeat ({nx},{ny},{nz}): {len(slab)} atoms")
    n_li = (slab.symbols == 'Li').sum()
    n_n = (slab.symbols == 'N').sum()
    print(f"  Composition: Li={n_li}, N={n_n}, ratio Li/N = {n_li/n_n:.2f} (expect 3.00)")

    # Move slab so z_min = 0, expand cell c to add vacuum on top
    z = slab.positions[:, 2]
    slab.positions[:, 2] -= z.min()
    z_max = slab.positions[:, 2].max()
    new_cell = slab.cell.array.copy()
    new_cell[2] = [0, 0, z_max + args.vacuum]
    slab.set_cell(new_cell, scale_atoms=False)
    slab.set_pbc(True)
    print(f"  Slab z = [0, {z_max:.2f}] Å, cell c = {new_cell[2,2]:.2f} (vacuum {args.vacuum})")
    print(f"  Lateral cell: a={np.linalg.norm(slab.cell[0]):.2f}, "
          f"b={np.linalg.norm(slab.cell[1]):.2f}, γ=120°")

    from ase.io import write
    write(out, slab, format="extxyz")
    print(f"\n→ {out}")

    # Save also the surface site information for adatom placement
    z_top = slab.positions[:, 2].max()
    top_n_mask = (slab.symbols == 'N') & (np.abs(slab.positions[:, 2] - z_top) < 0.1)
    top_n_idx = np.where(top_n_mask)[0]
    if len(top_n_idx) == 0:
        # Top layer might be Li(1) — find topmost N within 2 Å
        top_n_mask = (slab.symbols == 'N') & (slab.positions[:, 2] > z_top - 2.0)
        top_n_idx = np.where(top_n_mask)[0]
    print(f"\nTop-layer N atoms (adatom anchor candidates): {len(top_n_idx)}")
    if len(top_n_idx) >= 2:
        # Pick two nearest N's for NEB initial/final
        n_pos = slab.positions[top_n_idx]
        dists = np.linalg.norm(n_pos - n_pos[0], axis=1)
        ord = np.argsort(dists)
        if len(ord) > 1:
            i0, i1 = top_n_idx[ord[0]], top_n_idx[ord[1]]
            d = np.linalg.norm(slab.positions[i1] - slab.positions[i0])
            print(f"  N pair: idx {i0} ↔ {i1}, distance {d:.3f} Å (expect ~{3.65:.2f} = a₀)")
            print(f"  Place Li adatom ~1.0-1.5 Å above each for NEB init/final")
    # Also report what the topmost z atoms are (Li or N)
    top_atoms = slab.positions[:, 2] > z_top - 0.05
    top_symbols = list(slab.symbols[top_atoms])
    from collections import Counter
    print(f"  Topmost atomic layer composition: {dict(Counter(top_symbols))}")


if __name__ == "__main__":
    main()
