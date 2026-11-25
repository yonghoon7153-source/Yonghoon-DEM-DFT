#!/usr/bin/env python
"""generate_stacked_deq_orthogonal.py — d_eq stacked xyz with orthogonal cell.

For each of the 5 FINAL combo comps:
  1. Read SE slab, apply face flip if needed
  2. Stack with NCM at the comp's d_eq (Morse fit minimum)
  3. Convert to orthogonal supercell (a1, a2 perpendicular in xy plane,
     a3 along z) — typically 1×2 hex supercell for argyrodite
  4. Save as <comp>_stacked_deq_orthogonal.xyz

Output: stacked_FINAL_combo_orthogonal/<comp>_stacked_deq_orthogonal.xyz

Run from /data/work/v30u_ensemble/
"""
import numpy as np
from pathlib import Path
from ase.io import read, write
from ase import Atoms

WORK = Path('/data/work/v30u_ensemble')
OUT = WORK / 'stacked_FINAL_combo_orthogonal'
OUT.mkdir(exist_ok=True)
VACUUM_TOP = 30.0

# FINAL combo with d_eq
COMBO = {
    'comp1':    {'se': 'comp1_slab_v2.xyz',                'face': 'A',
                 'ncm': 'ncm_7x7x1_PRESERVED.xyz', 'd_eq': 1.17},
    'comp2':    {'se': 'comp2_slab_v2.xyz',                'face': 'A',
                 'ncm': 'ncm_7x7x1_PRESERVED.xyz', 'd_eq': 1.11},
    'comp3_v2': {'se': 'comp3_slab_v2_preShift.xyz',       'face': 'B',
                 'ncm': 'ncm_5x5x1_PRESERVED.xyz', 'd_eq': 1.44},
    'comp4_v2': {'se': 'comp4_v2_slab_shift2.xyz',         'face': 'B',
                 'ncm': 'ncm_5x5x1_PRESERVED.xyz', 'd_eq': 1.39},
    'comp5_v2': {'se': 'comp5_v2_slab_shift2.xyz',         'face': 'A',
                 'ncm': 'ncm_5x5x1_PRESERVED.xyz', 'd_eq': 1.19},
}


def flip_se_xy(se):
    a = se.copy()
    pos = a.positions.copy()
    pos[:, 2] = pos[:, 2].max() + pos[:, 2].min() - pos[:, 2]
    a.set_positions(pos)
    return a


def stack_interface(se, ncm, gap):
    """NCM at bottom (z=0), SE on top, parallel interface at gap."""
    se_a = se.copy()
    ncm_a = ncm.copy()
    ncm_a.wrap()
    ncm_a.translate([0, 0, -ncm_a.positions[:, 2].min()])
    ncm_z_max = ncm_a.positions[:, 2].max()
    se_z_min = se_a.positions[:, 2].min()
    se_a.translate([0, 0, ncm_z_max - se_z_min + gap])
    combined = ncm_a + se_a
    new_cell = se.cell.array.copy()
    z_extent = combined.positions[:, 2].max() - combined.positions[:, 2].min()
    new_cell[2] = [0, 0, z_extent + VACUUM_TOP]
    combined.set_cell(new_cell, scale_atoms=False)
    combined.set_pbc([True, True, True])
    return combined


def orthogonalize(atoms):
    """Convert hex cell to orthogonal supercell (1×2 expansion).

    For hex 120° cell:
      a1 = (a, 0, 0)
      a2 = (-a/2, a√3/2, 0)
    The orthogonal supercell is:
      a1' = a1 = (a, 0, 0)
      a2' = 2·a2 + a1 = (0, a√3, 0)  ← orthogonal!
      a3' = a3 (already along z if z_PBC)

    Returns 1×2-expanded orthogonal version.
    """
    cell = atoms.cell.array
    a1 = cell[0]
    a2 = cell[1]
    a3 = cell[2]

    # Check if already orthogonal in xy (a1·a2 ≈ 0)
    if abs(a1[0] * a2[0] + a1[1] * a2[1]) < 1e-6:
        # already orthogonal
        return atoms.copy()

    # Build 1×2 supercell along a2 direction
    from ase.build import make_supercell
    P = np.array([[1, 0, 0], [1, 2, 0], [0, 0, 1]])
    # The (1, 2) part: new a2 = a1 + 2*a2 (zero out a1 x-component)
    # Let's verify: new_a2 = 1*a1 + 2*a2 = (a, 0, 0) + 2*(-a/2, a√3/2, 0) = (0, a√3, 0) ✓
    supercell = make_supercell(atoms, P)

    # Verify orthogonality
    new_cell = supercell.cell.array
    dot12 = new_cell[0, 0] * new_cell[1, 0] + new_cell[0, 1] * new_cell[1, 1]
    if abs(dot12) > 1e-4:
        print(f"  WARN: supercell still non-orthogonal (a1·a2_xy = {dot12:.4f})")

    return supercell


def main():
    print(f"{'comp':<12} {'face':<5} {'d_eq (Å)':>10} {'N_orig':>7} {'N_ortho':>8}   output")
    print("-" * 100)
    for comp, info in COMBO.items():
        se = read(info['se'], format='extxyz')
        if info['face'] == 'B':
            se = flip_se_xy(se)
        ncm = read(info['ncm'], format='extxyz')

        stacked = stack_interface(se, ncm, info['d_eq'])
        n_orig = len(stacked)

        ortho = orthogonalize(stacked)
        n_ortho = len(ortho)

        out_path = OUT / f'{comp}_stacked_deq{info["d_eq"]:.2f}_orthogonal.xyz'
        write(out_path, ortho, format='extxyz')
        print(f"{comp:<12} {info['face']:<5} {info['d_eq']:>10.2f} {n_orig:>7} {n_ortho:>8}   {out_path.name}")

    print(f"\nSaved {len(COMBO)} orthogonal d_eq stacked xyz files to {OUT}/")


if __name__ == '__main__':
    main()
