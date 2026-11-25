#!/usr/bin/env python
"""bond_density_LiO_cutoff_sweep.py — Li-O cutoff sensitivity analysis.

Sweeps Li-O cutoff from 2.4 to 3.6 Å (default 2.8 Å). For each cutoff,
recomputes 36-reg averaged Li-O density and R/ρ correlation with paper Wad.

Other pair cutoffs unchanged. Shows whether Li-O conclusion is robust
to cutoff choice.

Output: bond_density_LiO_cutoff_sweep.json + table.
"""
import json, time
from pathlib import Path
import numpy as np
from ase.io import read
from scipy.stats import spearmanr

WORK = Path('/data/work/v30u_ensemble')
D_WELL = 1.4
VACUUM_TOP = 30.0
RANDOM_SEED = 42

# Li-O cutoff values to sweep
LIO_CUTOFFS = [2.4, 2.6, 2.8, 3.0, 3.2, 3.4, 3.6]
DEFAULT_LIO = 2.8  # ionic radii Li(0.76) + O(1.40) + buffer = 2.7 Å

COMBO = {
    'comp1':    {'se': 'comp1_slab_v2.xyz',                'face': 'A',
                 'ncm': 'ncm_7x7x1_PRESERVED.xyz', 'paper': 194},
    'comp2':    {'se': 'comp2_slab_v2.xyz',                'face': 'A',
                 'ncm': 'ncm_7x7x1_PRESERVED.xyz', 'paper': 180},
    'comp3_v2': {'se': 'comp3_slab_v2_preShift.xyz',       'face': 'B',
                 'ncm': 'ncm_5x5x1_PRESERVED.xyz', 'paper': 316},
    'comp4_v2': {'se': 'comp4_v2_slab_shift2.xyz',         'face': 'B',
                 'ncm': 'ncm_5x5x1_PRESERVED.xyz', 'paper': 298},
    'comp5_v2': {'se': 'comp5_v2_slab_shift2.xyz',         'face': 'A',
                 'ncm': 'ncm_5x5x1_PRESERVED.xyz', 'paper': 249},
}

HIGH_SYM = [
    ('R1_origin',   (0.0, 0.0)),
    ('R2_half_x',   (0.5, 0.0)),
    ('R3_half_y',   (0.0, 0.5)),
    ('R4_diagonal', (0.5, 0.5)),
    ('R5_hex1',     (1/3, 2/3)),
    ('R6_hex2',     (2/3, 1/3)),
]
N_RANDOM = 30
rng = np.random.default_rng(RANDOM_SEED)
RANDOM_REG = [(f"rand_{i+1:03d}", (float(rng.uniform(0, 1)), float(rng.uniform(0, 1))))
              for i in range(N_RANDOM)]
ALL_REG = HIGH_SYM + RANDOM_REG


def flip_se_xy(se):
    a = se.copy()
    pos = a.positions.copy()
    pos[:, 2] = pos[:, 2].max() + pos[:, 2].min() - pos[:, 2]
    a.set_positions(pos)
    return a


def count_LiO_vectorized(se_pos, se_sym, ncm_pos, ncm_sym, cell_xy, cutoff):
    inv_cell = np.linalg.inv(cell_xy.T)
    se_mask = (se_sym == 'Li')
    ncm_mask = (ncm_sym == 'O')
    if not se_mask.any() or not ncm_mask.any():
        return 0
    se_p = se_pos[se_mask]
    ncm_p = ncm_pos[ncm_mask]
    diff = se_p[:, None, :] - ncm_p[None, :, :]
    diff_xy = diff[:, :, :2]
    diff_z = diff[:, :, 2]
    frac = diff_xy @ inv_cell.T
    frac = frac - np.round(frac)
    diff_xy_mic = frac @ cell_xy.T
    d2 = diff_xy_mic[:, :, 0]**2 + diff_xy_mic[:, :, 1]**2 + diff_z**2
    return int(np.sum(d2 < cutoff**2))


def main():
    t0 = time.time()
    print("=" * 100)
    print("Li-O cutoff sensitivity — 36-reg averaged density")
    print(f"Cutoff sweep: {LIO_CUTOFFS} (default = {DEFAULT_LIO} Å)")
    print("=" * 100)

    # Pre-load all comps' positions
    comp_data = {}
    for comp, info in COMBO.items():
        se = read(info['se'], format='extxyz')
        if info['face'] == 'B':
            se = flip_se_xy(se)
        ncm = read(info['ncm'], format='extxyz')
        se_pos_orig = se.positions.copy()
        se_sym = np.array(se.symbols)
        se_z_min = se_pos_orig[:, 2].min()
        ncm_pos_orig = ncm.positions.copy()
        ncm_sym = np.array(ncm.symbols)
        ncm_pos_orig[:, 2] -= ncm_pos_orig[:, 2].min()
        ncm_z_max = ncm_pos_orig[:, 2].max()
        se_z_shift = ncm_z_max + D_WELL - se_z_min
        se_pos = se_pos_orig.copy()
        se_pos[:, 2] += se_z_shift
        cell_xy = se.cell.array[:2, :2]
        area = abs(np.cross(np.append(se.cell.array[0, :2], 0),
                            np.append(se.cell.array[1, :2], 0))[2])
        comp_data[comp] = {
            'se_pos': se_pos, 'se_sym': se_sym, 'ncm_pos_orig': ncm_pos_orig,
            'ncm_sym': ncm_sym, 'cell_xy': cell_xy, 'area': area,
            'cell_a1a2': ncm.cell.array[:2].copy(),
        }

    paper_arr = np.array([COMBO[c]['paper'] for c in COMBO], dtype=float)

    print(f"\n{'cutoff (Å)':>12} | {'comp1':>9} {'comp2':>9} {'comp3':>9} {'comp4':>9} {'comp5':>9} | {'R':>8} {'ρ':>7}")
    print("-" * 95)

    results = {}
    for cut in LIO_CUTOFFS:
        densities = []
        for comp in COMBO:
            d = comp_data[comp]
            total_count = 0
            for (reg_name, shift_frac) in ALL_REG:
                dx, dy = shift_frac
                shift_cart = dx * d['cell_a1a2'][0] + dy * d['cell_a1a2'][1]
                ncm_pos = d['ncm_pos_orig'].copy()
                ncm_pos[:, :2] += shift_cart[:2]
                total_count += count_LiO_vectorized(
                    d['se_pos'], d['se_sym'], ncm_pos, d['ncm_sym'],
                    d['cell_xy'], cut)
            mean_count = total_count / len(ALL_REG)
            densities.append(mean_count / d['area'])
        densities = np.array(densities)
        if densities.std() > 0:
            R = float(np.corrcoef(densities, paper_arr)[0, 1])
            rho = float(spearmanr(densities, paper_arr).statistic)
        else:
            R, rho = float('nan'), float('nan')
        default_flag = ' ← default' if abs(cut - DEFAULT_LIO) < 0.01 else ''
        print(f"  {cut:>10.2f} | {densities[0]:>9.5f} {densities[1]:>9.5f} {densities[2]:>9.5f} "
              f"{densities[3]:>9.5f} {densities[4]:>9.5f} | {R:>+8.4f} {rho:>+7.3f}{default_flag}", flush=True)
        results[f'{cut:.2f}'] = {'densities': densities.tolist(), 'R': R, 'rho': rho}

    print(f"\n--- Robustness summary ---")
    Rs = [results[f'{c:.2f}']['R'] for c in LIO_CUTOFFS]
    print(f"  R range: [{min(Rs):+.4f}, {max(Rs):+.4f}]")
    print(f"  All R positive (Li-O attractive)? {all(r > 0 for r in Rs)}")
    print(f"  All ρ ≥ +0.5? {all(results[f'{c:.2f}']['rho'] >= 0.5 for c in LIO_CUTOFFS)}")

    json.dump(results, open(WORK / 'bond_density_LiO_cutoff_sweep.json', 'w'), indent=2)
    print(f"\nSaved: bond_density_LiO_cutoff_sweep.json")
    print(f"Runtime: {time.time()-t0:.1f} s")


if __name__ == '__main__':
    main()
