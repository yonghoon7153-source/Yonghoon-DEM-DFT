"""Build comp4 v2 hybrid slab — bulk from v2 anneal champion, surface Cl→Br
swap to restore v1-like surface chemistry.

Rationale:
  comp4 v2 anneal champion has Cl migrated to surface (4/16 Cl at z=+0.3 Å,
  bottom surface). This makes rigid binding curves anomalous (Cl-O repulsion
  dominates). But experimentally synthesized Argyrodite has surface frozen
  during quench, more like v1 (Cl in bulk, Br at surface).

  We preserve v2 bulk structure (cell, Li ordering, P-S framework, halogen
  total count) but swap surface Cl with bulk Br. Result represents a
  thermodynamically valid bulk-relaxed state with kinetically-frozen
  experimental-like surface.

What's preserved:
  - Cell parameters (a, b, c, angles)
  - All P-S framework positions (PS4 tetrahedra intact)
  - All Li positions (anneal-optimized ordering, no 1.78 Å Li-Li like v1)
  - Total Cl/Br stoichiometry

What's swapped:
  - 4 Cl at z ≈ 0.3 Å (surface) ↔ 4 Br at z ≈ 11.7 Å (bulk middle)
  - Result: surface has 8 Br + 0 Cl (v1-like), bulk has more Cl

Usage:
    python make_comp4_v2_surface_hybrid.py comp4_slab_v2_PRESERVED.xyz \
        comp4_slab_v2_HYBRID.xyz [--surface_z_max 3.0] [--bulk_z_min 8.0]
"""
import sys
from pathlib import Path
import numpy as np
from ase.io import read, write
import argparse


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('input_xyz', help='comp4 v2 slab xyz')
    p.add_argument('output_xyz', help='output hybrid xyz')
    p.add_argument('--surface_z_max', type=float, default=3.0,
                   help='atoms with z <= this are "surface bottom" (default 3.0 A)')
    p.add_argument('--bulk_z_min', type=float, default=8.0,
                   help='Br candidates for swap with z >= this (default 8.0 A)')
    p.add_argument('--bulk_z_max', type=float, default=20.0,
                   help='also Br z <= this (default 20.0 A; avoid top surface)')
    args = p.parse_args()

    atoms = read(args.input_xyz)
    sym = list(atoms.get_chemical_symbols())
    z = atoms.positions[:, 2]
    print(f"Loaded {len(atoms)} atoms from {args.input_xyz}")
    print(f"z range: [{z.min():.3f}, {z.max():.3f}] (Δz = {z.max()-z.min():.3f} Å)")

    # Find surface Cl: z <= surface_z_max
    surf_cl = [i for i, s in enumerate(sym) if s == 'Cl' and z[i] <= args.surface_z_max]
    # Find bulk Br: surface_z_max < z and bulk_z_min <= z <= bulk_z_max
    bulk_br = [i for i, s in enumerate(sym)
               if s == 'Br' and args.bulk_z_min <= z[i] <= args.bulk_z_max]

    print(f"\nSurface Cl candidates (z <= {args.surface_z_max}): {len(surf_cl)}")
    for i in surf_cl:
        print(f"  Cl{i:3d}: z={z[i]:+.3f}")
    print(f"\nBulk Br candidates ({args.bulk_z_min} <= z <= {args.bulk_z_max}): {len(bulk_br)}")
    for i in bulk_br:
        print(f"  Br{i:3d}: z={z[i]:+.3f}")

    if len(surf_cl) == 0:
        print("\nNo surface Cl to swap — already v1-like surface. Exiting.")
        return
    if len(surf_cl) > len(bulk_br):
        print(f"\nWARNING: more surface Cl ({len(surf_cl)}) than bulk Br ({len(bulk_br)}). "
              f"Will only swap {len(bulk_br)}.")
    n_swap = min(len(surf_cl), len(bulk_br))

    # Pair them: closest-in-x,y matching to minimize Madelung disturbance
    pos = atoms.positions
    used_br = set()
    pairs = []
    for ci in surf_cl[:n_swap]:
        # find nearest unused bulk Br by xy distance
        best_bi, best_d = None, float('inf')
        for bi in bulk_br:
            if bi in used_br:
                continue
            dxy = np.hypot(pos[ci,0] - pos[bi,0], pos[ci,1] - pos[bi,1])
            if dxy < best_d:
                best_d = dxy; best_bi = bi
        if best_bi is not None:
            pairs.append((ci, best_bi, best_d))
            used_br.add(best_bi)

    print(f"\nSwap pairs (Cl ↔ Br):")
    for ci, bi, dxy in pairs:
        print(f"  Cl{ci:3d}(z={z[ci]:+.2f}) ↔ Br{bi:3d}(z={z[bi]:+.2f}), xy_dist={dxy:.2f} Å")

    # Apply swap by changing species (positions stay)
    new_sym = sym.copy()
    for ci, bi, _ in pairs:
        new_sym[ci] = 'Br'
        new_sym[bi] = 'Cl'

    # Verify total composition preserved
    from collections import Counter
    print(f"\nComposition before swap:", Counter(sym))
    print(f"Composition after swap: ", Counter(new_sym))

    new_atoms = atoms.copy()
    new_atoms.set_chemical_symbols(new_sym)
    write(args.output_xyz, new_atoms)
    print(f"\nWrote {args.output_xyz}")
    print(f"\nNext step: replace comp4 slab in v30u Z-scan with this hybrid:")
    print(f"  COMPS['comp4'] = {{'se': '{args.output_xyz}', ...}}")


if __name__ == '__main__':
    main()
