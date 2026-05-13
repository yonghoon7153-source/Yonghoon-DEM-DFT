"""make_comp12_stacked_orthogonal.py — produce comp1, comp2 stacked xyz files.

Same protocol as uploaded comp1/comp2 orthogonal stacked files:
  • face A (no flip — Cl on bottom for Li6 family is the natural state)
  • d = 1.2 Å gap (well distance for Li6 family per paper)
  • orthogonal cell (Li6 cubic SE is already orthogonal)

Outputs:
  comp1_R1_origin_d1.2_orthogonal.xyz
  comp2_R1_origin_d1.2_orthogonal.xyz
"""
from pathlib import Path
import numpy as np
from ase.io import read, write

WORK = Path('/data/work/v30u_ensemble')
GAP = 1.2
VACUUM = 30.0

CONFIGS = {
    'comp1': {'se': 'comp1_slab_v2.xyz',  'ncm': 'ncm_7x7x1_PRESERVED.xyz'},
    'comp2': {'se': 'comp2_slab_v2.xyz',  'ncm': 'ncm_7x7x1_PRESERVED.xyz'},
}


def stack_interface(se, ncm, gap, shift=(0.0, 0.0)):
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
    for comp, info in CONFIGS.items():
        se = read(WORK / info['se'])
        ncm = read(WORK / info['ncm'])
        print(f"\n=== {comp} ===")
        print(f"  SE: {len(se)} atoms")
        print(f"  NCM: {len(ncm)} atoms")
        stacked = stack_interface(se, ncm, GAP)
        stacked_ortho = orthogonalize(stacked)
        out_path = WORK / f"{comp}_R1_origin_d{GAP}_orthogonal.xyz"
        write(out_path, stacked_ortho)
        print(f"  Total: {len(stacked_ortho)} atoms")
        print(f"  Saved: {out_path}")


if __name__ == "__main__":
    main()
