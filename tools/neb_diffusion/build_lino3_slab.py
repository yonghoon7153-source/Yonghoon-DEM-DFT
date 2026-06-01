#!/usr/bin/env python3
"""Build a LiNO3 (001) slab for Li adatom NEB.

Lithium nitrate, calcite-like rhombohedral structure (R-3c, No. 167).
Hexagonal setting: a = 4.692 Å, c = 15.21 Å
Wyckoff sites (Z = 6):
  Li (6b): (0, 0, 0)         — Li layers
  N  (6a): (0, 0, 1/4)        — N at center of NO3 trigonal planar
  O  (18e): (x, 0, 1/4), x ≈ 0.245   — 3 O around each N (in-plane triangle)

Note: Layers along c stack as Li / NO3 / Li / NO3 / ... at z=0, 1/4, 1/2, 3/4.
(001) cleavage typically between Li and NO3 layers.

Usage:
    python3 build_lino3_slab.py \\
        --repeat 2 2 --n_unitcells_c 2 --vacuum 15 \\
        --out_init <out>/lino3_001_init.xyz
"""
import argparse
from pathlib import Path
import numpy as np


def build_lino3_bulk():
    """LiNO3 R-3c hexagonal setting, 30 atoms (6 Li + 6 N + 18 O)."""
    from ase import Atoms
    a, c = 4.692, 15.21
    cell = np.array([[a, 0, 0], [-a/2, a*np.sqrt(3)/2, 0], [0, 0, c]])

    # R-3c symmetry operations applied to asymmetric unit
    # Asymmetric atoms (in hex setting):
    # Li at (0, 0, 0)
    # N at (0, 0, 1/4)
    # O at (x, 0, 1/4) with x = 0.245
    # Plus rhombohedral centering: (0,0,0), (2/3,1/3,1/3), (1/3,2/3,2/3)
    x_O = 0.245

    # Generate equivalent positions for R-3c
    centerings = [(0, 0, 0), (2/3, 1/3, 1/3), (1/3, 2/3, 2/3)]

    # Li at (0,0,0) + R-3c equivalents (inversion through c-glide)
    li_frac = []
    for cnt in centerings:
        li_frac.append([cnt[0], cnt[1], cnt[2]])
        # Inversion: (-x, -y, -z) → relative to (0, 0, 1/2) center
        li_frac.append([(-cnt[0]) % 1, (-cnt[1]) % 1, (1/2 - cnt[2]) % 1])
    # 6 Li ✓

    # N at (0,0,1/4) + R-3c equivalents
    n_frac = []
    for cnt in centerings:
        n_frac.append([cnt[0], cnt[1], (1/4 + cnt[2]) % 1])
        n_frac.append([(-cnt[0]) % 1, (-cnt[1]) % 1, (1/4 - cnt[2]) % 1])
    # 6 N ✓

    # O at (x,0,1/4) and 2-fold/3-fold rotations
    # In R-3c, O positions are 18e: (x, 0, 1/4), (-y, x-y, 1/4), (-x+y, -x, 1/4)
    # Plus equivalents from centerings + inversion
    o_frac = []
    for cnt in centerings:
        # Triangle of 3 O around the N (3-fold rotation)
        o_frac.append([(x_O + cnt[0]) % 1, cnt[1], (1/4 + cnt[2]) % 1])
        o_frac.append([(-x_O/2 + cnt[0]) % 1, (x_O*np.sqrt(3)/2 + cnt[1]) % 1, (1/4 + cnt[2]) % 1])
        o_frac.append([(-x_O/2 + cnt[0]) % 1, (-x_O*np.sqrt(3)/2 + cnt[1]) % 1, (1/4 + cnt[2]) % 1])
        # Inversion partners
        o_frac.append([(-x_O - cnt[0]) % 1, (-cnt[1]) % 1, (1/4 - cnt[2]) % 1])
        o_frac.append([(x_O/2 - cnt[0]) % 1, (-x_O*np.sqrt(3)/2 - cnt[1]) % 1, (1/4 - cnt[2]) % 1])
        o_frac.append([(x_O/2 - cnt[0]) % 1, (x_O*np.sqrt(3)/2 - cnt[1]) % 1, (1/4 - cnt[2]) % 1])
    # 18 O ✓

    all_frac = np.array(li_frac + n_frac + o_frac)
    symbols = ['Li']*6 + ['N']*6 + ['O']*18
    positions = all_frac @ cell
    return Atoms(symbols=symbols, positions=positions, cell=cell, pbc=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repeat", type=int, nargs=2, default=[2, 2])
    ap.add_argument("--n_unitcells_c", type=int, default=2,
                    help="repeat along c (each unit cell = 4 atomic layers)")
    ap.add_argument("--vacuum", type=float, default=15.0)
    ap.add_argument("--out_init", required=True)
    args = ap.parse_args()

    out = Path(args.out_init); out.parent.mkdir(parents=True, exist_ok=True)

    bulk = build_lino3_bulk()
    print(f"Bulk LiNO3 hex: {len(bulk)} atoms "
          f"(Li={(bulk.symbols=='Li').sum()}, N={(bulk.symbols=='N').sum()}, "
          f"O={(bulk.symbols=='O').sum()})")
    a0 = np.linalg.norm(bulk.cell[0])
    c0 = bulk.cell.array[2, 2]
    print(f"  a={a0:.3f}, c={c0:.3f}, V={bulk.get_volume():.2f} Å³")

    nx, ny = args.repeat
    nz = args.n_unitcells_c
    slab = bulk.repeat((nx, ny, nz))
    print(f"After repeat ({nx},{ny},{nz}): {len(slab)} atoms")

    # Shift z_min to 0, add vacuum above
    z = slab.positions[:, 2]
    slab.positions[:, 2] -= z.min()
    z_max = slab.positions[:, 2].max()
    new_cell = slab.cell.array.copy()
    new_cell[2] = [0, 0, z_max + args.vacuum]
    slab.set_cell(new_cell, scale_atoms=False)
    slab.set_pbc(True)

    print(f"  Slab z = [0, {z_max:.2f}] Å, cell c = {new_cell[2,2]:.2f}")
    print(f"  Surface: a={np.linalg.norm(slab.cell[0]):.2f}, "
          f"b={np.linalg.norm(slab.cell[1]):.2f}, γ=120°")

    # Identify topmost atom layer (likely Li or O depending on cleavage)
    z = slab.positions[:, 2]
    z_max = z.max()
    top = z > z_max - 0.3
    from collections import Counter
    print(f"  Topmost layer: {dict(Counter(slab.symbols[top]))}")

    # Find adjacent topmost Li for NEB endpoints
    top_li_mask = (slab.symbols == 'Li') & (z > z_max - 2.0)
    top_li_idx = np.where(top_li_mask)[0]
    if len(top_li_idx) < 2:
        # If no Li in top region, fall back to highest Li
        li_idx = np.where(slab.symbols == 'Li')[0]
        order = li_idx[np.argsort(-z[li_idx])][:2]
        top_li_idx = order

    if len(top_li_idx) >= 2:
        p = slab.positions[top_li_idx]
        d = np.linalg.norm(p - p[0], axis=1)
        d[0] = 9e9  # exclude self
        nearest_j = np.argmin(d)
        i0 = top_li_idx[0]; i1 = top_li_idx[nearest_j]
        dist = np.linalg.norm(slab.positions[i1] - slab.positions[i0])
        print(f"\n  Nearest top Li pair: idx {i0} ↔ {i1}, distance {dist:.3f} Å")
        # Place adatom 1.5 Å above each Li (Li adatom on Li-terminated surface,
        # or replace these Li with adatom probes)
        # For NEB: place adatom above midway between two top Li sites
        z_target = z_max + 1.5
        print(f"  Adatom initial: ({slab.positions[i0,0]:.3f}, "
              f"{slab.positions[i0,1]:.3f}, {z_target:.3f})")
        print(f"  Adatom final:   ({slab.positions[i1,0]:.3f}, "
              f"{slab.positions[i1,1]:.3f}, {z_target:.3f})")

    from ase.io import write
    write(out, slab, format="extxyz")
    print(f"\n→ {out}")


if __name__ == "__main__":
    main()
