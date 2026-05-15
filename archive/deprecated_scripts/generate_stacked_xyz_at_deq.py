#!/usr/bin/env python
"""generate_stacked_xyz_at_deq.py — write stacked SE+NCM xyz for each comp.

Generates TWO stacked configurations per comp:
  1. At each comp's individual d_eq (Morse fit minimum)
  2. At common d = 1.4 Å (mean well region, fair cross-comp comparison)

Uses FINAL combo slabs + face from R=+0.989 figure.
Output: stacked_FINAL_combo/<comp>_stacked_d<gap>.xyz

Run from /data/work/v30u_ensemble/
"""
import numpy as np
from pathlib import Path
from ase.io import read, write

WORK = Path('/data/work/v30u_ensemble')
OUT = WORK / 'stacked_FINAL_combo'
OUT.mkdir(exist_ok=True)
VACUUM_TOP = 30.0

# FINAL combo with d_eq from Morse fit
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

# Common gap for fair cross-comp comparison
COMMON_GAPS = [1.2, 1.4, 1.6]


def flip_se_xy(se):
    a = se.copy()
    pos = a.positions.copy()
    pos[:, 2] = pos[:, 2].max() + pos[:, 2].min() - pos[:, 2]
    a.set_positions(pos)
    return a


def stack_interface(se, ncm, gap):
    """NCM at bottom (z=0), SE on top — matches working li_migration stack."""
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


def main():
    print(f"{'comp':<12} {'face':<5} {'gap (Å)':>9} {'label':<10} {'n_atoms':>8}   output file")
    print("-" * 100)
    for comp, info in COMBO.items():
        se_base = read(info['se'], format='extxyz')
        if info['face'] == 'B':
            se_base = flip_se_xy(se_base)
        ncm = read(info['ncm'], format='extxyz')

        # (1) at this comp's d_eq
        stacked = stack_interface(se_base, ncm, info['d_eq'])
        out_path = OUT / f'{comp}_stacked_deq{info["d_eq"]:.2f}.xyz'
        write(out_path, stacked, format='extxyz')
        print(f"{comp:<12} {info['face']:<5} {info['d_eq']:>9.2f}  deq        {len(stacked):>6}   {out_path.name}")

        # (2) at common gaps (1.2, 1.4, 1.6 Å)
        for g in COMMON_GAPS:
            stacked = stack_interface(se_base, ncm, g)
            out_path = OUT / f'{comp}_stacked_d{g:.1f}.xyz'
            write(out_path, stacked, format='extxyz')
            print(f"{comp:<12} {info['face']:<5} {g:>9.2f}  common     {len(stacked):>6}   {out_path.name}")

    print(f"\nSaved {len(COMBO) * (1 + len(COMMON_GAPS))} stacked xyz files to {OUT}/")
    print(f"  - {len(COMBO)} at each comp's individual d_eq")
    print(f"  - {len(COMBO) * len(COMMON_GAPS)} at common gaps {COMMON_GAPS}")


if __name__ == '__main__':
    main()
