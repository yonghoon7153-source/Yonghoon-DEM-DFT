#!/usr/bin/env python3
"""Build a LiC6 (0001) slab for Li adatom NEB.

LiC6 is stage-1 graphite intercalation compound (GIC). Structure:
  - Graphite layers (AA stacking, not AB like graphite)
  - Li atoms intercalated between every layer at hexagonal hollow sites
  - In-plane Li-Li distance = a_Lc6 = sqrt(3) × a_graphene = 4.26 Å
  - Out-of-plane: graphene → Li → graphene → Li → ... spacing 3.706 Å

Per LiC6 in-plane unit cell:
  - C: 6 atoms forming honeycomb (graphene-like)
  - Li: 1 atom per layer, at hexagonal hollow position

Surface (0001) = basal plane (graphene-terminated, no Li on top).
Li adatom sits on hollow site above topmost graphene.

Usage:
    python3 build_lic6_slab.py \\
        --n_graphene_layers 4 --repeat 2 2 --vacuum 15 \\
        --out_init <out>/lic6_0001_init.xyz
"""
import argparse
from pathlib import Path
import numpy as np


def build_lic6_bulk():
    """Stage-1 LiC6 with hexagonal in-plane superstructure (√3 × √3 R30°).

    Returns one unit cell with:
      - 2 graphene layers (C12)
      - 2 Li (one between layers, one above top — periodic)
    Total: 14 atoms.

    Lattice:
      a = 4.26 Å (= √3 × 2.46 Å graphene a)
      c = 7.40 Å (Li-C-Li-C-Li... unit, two layer spacings)
    """
    from ase import Atoms
    a = 4.26
    c = 7.40
    # Hexagonal cell, γ=120°
    cell = [[a, 0, 0], [-a/2, a*np.sqrt(3)/2, 0], [0, 0, c]]

    # Graphene layer at z=0: 6 C atoms in honeycomb
    # In √3×√3 R30° cell, 6 C atoms occupy honeycomb positions
    # 그래핀 √3×√3: 6C per cell at honeycomb positions (rotated 30°)
    # Honeycomb sub-lattice A and B:
    cf_a = 1.0/3.0  # offset for sublattice A
    cf_b = 2.0/3.0
    # Standard √3×√3 6C honeycomb:
    c_frac = np.array([
        [0.0,      0.0,      0],
        [1.0/3.0,  0.0,      0],
        [0.0,      1.0/3.0,  0],
        [2.0/3.0,  1.0/3.0,  0],
        [1.0/3.0,  2.0/3.0,  0],
        [2.0/3.0,  2.0/3.0,  0],
    ])
    # Same graphene at z = c/2 (next layer)
    c_frac_2 = c_frac.copy(); c_frac_2[:, 2] = 0.5
    # Li layer between: at hollow position
    # In √3×√3 graphene, Li sits at center of one hexagon
    li_frac = np.array([
        [1.0/3.0, 1.0/3.0, 0.25],  # between layer 0 and 1
        [2.0/3.0, 2.0/3.0, 0.75],  # between layer 1 and 0 (periodic)
    ])
    all_frac = np.vstack([c_frac, c_frac_2, li_frac])
    symbols = ['C']*6 + ['C']*6 + ['Li']*2
    cell_arr = np.array(cell)
    positions = all_frac @ cell_arr
    return Atoms(symbols=symbols, positions=positions, cell=cell, pbc=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n_graphene_layers", type=int, default=4,
                    help="number of graphene layers (default 4 → 4 C + 3 Li layers)")
    ap.add_argument("--repeat", type=int, nargs=2, default=[2, 2],
                    help="in-plane repeat (default 2 2 → 8.52 Å lateral)")
    ap.add_argument("--vacuum", type=float, default=15.0)
    ap.add_argument("--out_init", required=True)
    args = ap.parse_args()

    out = Path(args.out_init); out.parent.mkdir(parents=True, exist_ok=True)

    bulk = build_lic6_bulk()
    print(f"Bulk LiC6 unit cell: {len(bulk)} atoms "
          f"(C={(bulk.symbols=='C').sum()}, Li={(bulk.symbols=='Li').sum()})")
    a0 = np.linalg.norm(bulk.cell[0])
    c0 = bulk.cell.array[2,2]
    print(f"  a={a0:.3f}, c={c0:.3f} Å, V={bulk.get_volume():.2f} Å³")
    # Stoichiometry check: 12 C, 2 Li → LiC6 ✓
    li_c_ratio = (bulk.symbols=='Li').sum() / (bulk.symbols=='C').sum()
    print(f"  Li/C = {li_c_ratio:.4f}  (expect 1/6 = 0.1667)")

    # Repeat the unit cell. n_graphene_layers controls c-direction repeats:
    # each unit cell has 2 graphene layers, so n_unitcells = n_graphene_layers // 2.
    nx, ny = args.repeat
    nz = max(1, args.n_graphene_layers // 2)
    slab = bulk.repeat((nx, ny, nz))
    print(f"After repeat ({nx},{ny},{nz}): {len(slab)} atoms")

    # Top of slab is currently a Li layer (z=c-step from top graphene).
    # We want graphene-terminated. Trim topmost Li atoms.
    z = slab.positions[:, 2]
    z_max = z.max()
    top_li_mask = (z > z_max - 0.5) & (np.array(slab.symbols) == 'Li')
    print(f"Removing {top_li_mask.sum()} topmost Li atoms (graphene termination)")
    del slab[top_li_mask]

    # Shift so z_min=0, add vacuum
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
    print(f"  Final composition: C={(slab.symbols=='C').sum()}, Li={(slab.symbols=='Li').sum()}")

    # Identify topmost graphene's hexagonal hollow positions for adatom placement
    z = slab.positions[:, 2]
    top_c_mask = (z > z_max - 0.3) & (np.array(slab.symbols) == 'C')
    top_c_idx = np.where(top_c_mask)[0]
    print(f"\nTop-layer C atoms: {len(top_c_idx)}")

    # Adjacent hollow sites in graphene: centroid of 3 nearest C atoms
    # For graphene basal, two types of hollow:
    #   - hex hollow (center of hexagon, 6 C neighbors, ~ 2.46 / √3 × √3 = 2.46/ a stuff)
    #   - bridge midpoint between 2 C
    #   - on-top of 1 C
    # Adatom typically prefers hex hollow → hex hollow hop ~ 0.3-0.5 eV barrier on graphite
    # The hex hollow site = center of an unrepeated graphene hexagon
    # In our √3×√3 cell, those hollows align with Li(intercalated) positions (1/3, 1/3) and (2/3, 2/3)
    a_surf = np.linalg.norm(slab.cell[0])
    a_vec = slab.cell.array[0]; b_vec = slab.cell.array[1]
    # Hex hollow positions (in the topmost graphene layer):
    hollow_1_frac = np.array([1.0/3.0, 1.0/3.0])
    hollow_2_frac = np.array([2.0/3.0, 2.0/3.0])
    hollow_1 = hollow_1_frac[0]*a_vec + hollow_1_frac[1]*b_vec
    hollow_2 = hollow_2_frac[0]*a_vec + hollow_2_frac[1]*b_vec
    hollow_1[2] = z_max + 1.7  # 1.7 Å above top graphene (typical Li adsorption distance)
    hollow_2[2] = z_max + 1.7
    print(f"\nAdatom hollow site candidates (1.7 Å above top graphene):")
    print(f"  hollow 1 (1/3, 1/3): ({hollow_1[0]:.3f}, {hollow_1[1]:.3f}, {hollow_1[2]:.3f})")
    print(f"  hollow 2 (2/3, 2/3): ({hollow_2[0]:.3f}, {hollow_2[1]:.3f}, {hollow_2[2]:.3f})")
    print(f"  distance: {np.linalg.norm(hollow_2 - hollow_1):.3f} Å")
    print(f"\n  Adatom initial: ({hollow_1[0]:.3f}, {hollow_1[1]:.3f}, {hollow_1[2]:.3f})")
    print(f"  Adatom final:   ({hollow_2[0]:.3f}, {hollow_2[1]:.3f}, {hollow_2[2]:.3f})")

    from ase.io import write
    write(out, slab, format="extxyz")
    print(f"\n→ {out}")


if __name__ == "__main__":
    main()
