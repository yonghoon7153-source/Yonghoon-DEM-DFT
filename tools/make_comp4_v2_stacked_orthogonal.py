"""make_comp4_v2_stacked_orthogonal.py — produce comp4_v2 stacked xyz
in the same format as uploaded comp1/comp2 orthogonal stacked files.

Protocol:
  1. Read comp4_slab_v2_PRESERVED.xyz (= .bak_anomaly via symlink)
  2. Apply xy-mirror to expose face B (clean Li/S termination — avoids
     the Cl-exposed anomaly that motivated v1 swap)
  3. Read ncm_5x5x1_PRESERVED.xyz (NCM slab)
  4. Stack with d = 1.4 Å (comp4_v2 face B well per face-flip data)
  5. Orthogonalize the final stacked cell (a3 → z-only, preserves
     fractional positions)
  6. Save as comp4_v2_R1_origin_d1.4_orthogonal.xyz

Output:
  /data/work/v30u_ensemble/comp4_v2_R1_origin_d1.4_orthogonal.xyz
"""
from pathlib import Path
import numpy as np
from ase.io import read, write

WORK = Path('/data/work/v30u_ensemble')
SE_PATH  = WORK / 'comp4_slab_v2_PRESERVED.xyz'    # symlink → .bak_anomaly
NCM_PATH = WORK / 'ncm_5x5x1_PRESERVED.xyz'
OUT_PATH = WORK / 'comp4_v2_R1_origin_d1.4_orthogonal.xyz'

GAP = 1.4
VACUUM = 30.0
USE_FACE_B = True       # True → flip SE in xy plane (avoid Cl-anomaly)


def flip_xy(se):
    """Mirror in xy plane: z → z_top + z_bottom − z."""
    a = se.copy()
    pos = a.positions.copy()
    pos[:, 2] = pos[:, 2].max() + pos[:, 2].min() - pos[:, 2]
    a.set_positions(pos)
    return a


def stack_interface(se, ncm, gap, shift=(0.0, 0.0)):
    """phase1-faithful stacking (verbatim)."""
    se_a = se.copy(); ncm_a = ncm.copy()
    dx, dy = shift
    shift_cart = dx * ncm_a.cell.array[0] + dy * ncm_a.cell.array[1]
    ncm_a.translate([shift_cart[0], shift_cart[1], 0])
    ncm_a.wrap()
    ncm_a.translate([0, 0, -ncm_a.positions[:, 2].min()])
    se_a.translate([0, 0, ncm_a.positions[:, 2].max() - se_a.positions[:, 2].min() + gap])
    combined = ncm_a + se_a
    new_cell = se.cell.array.copy()
    z_extent = combined.positions[:, 2].max() - combined.positions[:, 2].min()
    new_cell[2] = [0, 0, z_extent + VACUUM]
    combined.set_cell(new_cell, scale_atoms=False)
    combined.set_pbc([True, True, True])
    return combined


def orthogonalize(atoms):
    """Keep fractional positions, set a3 to (0, 0, |a3_z|).
    Same logic as verify_slabs.py orthogonalize()."""
    cell = atoms.cell.array.copy()
    if abs(cell[2, 0]) < 0.01 and abs(cell[2, 1]) < 0.01:
        return atoms.copy()
    frac = atoms.get_scaled_positions()
    new_cell = cell.copy()
    new_cell[2] = [0, 0, cell[2, 2]]
    out = atoms.copy()
    out.set_cell(new_cell, scale_atoms=False)
    out.set_scaled_positions(frac)
    return out


def main():
    se = read(SE_PATH)
    ncm = read(NCM_PATH)
    print(f"SE: {len(se)} atoms, cell:\n{se.cell.array}")
    print(f"NCM: {len(ncm)} atoms, cell:\n{ncm.cell.array}")

    if USE_FACE_B:
        se = flip_xy(se)
        print(f"\nApplied face B flip (xy-mirror)")

    stacked = stack_interface(se, ncm, GAP)
    print(f"\nStacked at gap {GAP} Å: {len(stacked)} atoms")
    print(f"  cell (before ortho):\n{stacked.cell.array}")

    stacked_ortho = orthogonalize(stacked)
    print(f"\nOrthogonalized:")
    print(f"  cell:\n{stacked_ortho.cell.array}")

    # Sanity: composition
    from collections import Counter
    print(f"\nComposition: {dict(Counter(stacked_ortho.get_chemical_symbols()))}")
    print(f"Expected: SE (Li5.4 4fu × 62 = 248) + NCM (5×5×3 atomic layers = 300) = 548 atoms")

    write(OUT_PATH, stacked_ortho)
    print(f"\nSaved: {OUT_PATH}")


if __name__ == "__main__":
    main()
