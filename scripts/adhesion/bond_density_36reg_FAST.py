#!/usr/bin/env python
"""bond_density_36reg_FAST.py — 36-reg averaged bond density, vectorized.

Same as bond_density_36reg_FINAL.py but with numpy broadcasting instead of
double Python loops. 100x speedup (~10 sec instead of ~10 min).

Run from /data/work/v30u_ensemble/
"""
import json, time
from pathlib import Path
import numpy as np
from ase.io import read
from scipy.stats import spearmanr

WORK = Path('/data/work/v30u_ensemble')
OUT_JSON = WORK / 'bond_density_36reg_FAST.json'
D_WELL = 1.4
VACUUM_TOP = 30.0
RANDOM_SEED = 42

COMBO = {
    'comp1':    {'se': 'comp1_slab_v2.xyz',                'face': 'A',
                 'ncm': 'ncm_7x7x1_PRESERVED.xyz', 'paper': 194, 'family': 'Li6'},
    'comp2':    {'se': 'comp2_slab_v2.xyz',                'face': 'A',
                 'ncm': 'ncm_7x7x1_PRESERVED.xyz', 'paper': 180, 'family': 'Li6'},
    'comp3_v2': {'se': 'comp3_slab_v2_preShift.xyz',       'face': 'B',
                 'ncm': 'ncm_5x5x1_PRESERVED.xyz', 'paper': 316, 'family': 'Li5.4'},
    'comp4_v2': {'se': 'comp4_v2_slab_shift2.xyz',         'face': 'B',
                 'ncm': 'ncm_5x5x1_PRESERVED.xyz', 'paper': 298, 'family': 'Li5.4'},
    'comp5_v2': {'se': 'comp5_v2_slab_shift2.xyz',         'face': 'A',
                 'ncm': 'ncm_5x5x1_PRESERVED.xyz', 'paper': 249, 'family': 'Li5.4'},
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

NCM_M = {'Ni', 'Co', 'Mn'}

CUTOFFS = {
    ('Li', 'O'):  2.8, ('Li', 'M'): 3.0, ('Li', 'Li'): 3.0,
    ('P',  'O'):  3.5, ('P',  'M'): 3.5, ('P',  'Li'): 3.3,
    ('S',  'O'):  3.0, ('S',  'M'): 3.0, ('S',  'Li'): 3.0,
    ('Cl', 'O'):  3.2, ('Cl', 'M'): 3.3, ('Cl', 'Li'): 3.2,
    ('Br', 'O'):  3.4, ('Br', 'M'): 3.5, ('Br', 'Li'): 3.4,
}


def flip_se_xy(se):
    a = se.copy()
    pos = a.positions.copy()
    pos[:, 2] = pos[:, 2].max() + pos[:, 2].min() - pos[:, 2]
    a.set_positions(pos)
    return a


def count_pairs_vectorized(se_positions, se_symbols, ncm_positions, ncm_symbols, cell_xy):
    """Vectorized pair counting with MIC.

    cell_xy: 2x2 lattice vectors (a1[:2], a2[:2]).
    Returns dict {(se_el, ncm_el_token): count}.
    """
    inv_cell = np.linalg.inv(cell_xy.T)  # for fractional coords

    counts = {}
    for (se_el, ncm_el_token), cut in CUTOFFS.items():
        if ncm_el_token == 'M':
            ncm_mask = np.isin(ncm_symbols, list(NCM_M))
        else:
            ncm_mask = (ncm_symbols == ncm_el_token)
        se_mask = (se_symbols == se_el)

        if not se_mask.any() or not ncm_mask.any():
            counts[(se_el, ncm_el_token)] = 0
            continue

        se_p = se_positions[se_mask]    # (n_se_el, 3)
        ncm_p = ncm_positions[ncm_mask] # (n_ncm_el, 3)

        # Pairwise differences (n_se, n_ncm, 3)
        diff = se_p[:, None, :] - ncm_p[None, :, :]
        diff_xy = diff[:, :, :2]  # (n_se, n_ncm, 2)
        diff_z = diff[:, :, 2]     # (n_se, n_ncm)

        # MIC in xy
        frac = diff_xy @ inv_cell.T  # (n_se, n_ncm, 2)
        frac = frac - np.round(frac)
        diff_xy_mic = frac @ cell_xy.T  # (n_se, n_ncm, 2)

        # Distance squared
        d2 = diff_xy_mic[:, :, 0]**2 + diff_xy_mic[:, :, 1]**2 + diff_z**2

        # Count contacts within cutoff
        counts[(se_el, ncm_el_token)] = int(np.sum(d2 < cut**2))

    return counts


def main():
    t0 = time.time()
    print("=" * 110)
    print(f"36-reg averaged bond density at d={D_WELL} Å — FINAL combo  (VECTORIZED)")
    print(f"  {len(HIGH_SYM)} high-sym + {N_RANDOM} random = {len(ALL_REG)} registries")
    print("=" * 110, flush=True)

    results = {}
    for comp, info in COMBO.items():
        t_comp = time.time()
        se = read(info['se'], format='extxyz')
        if info['face'] == 'B':
            se = flip_se_xy(se)
        ncm = read(info['ncm'], format='extxyz')

        # Pre-compute SE positions (fixed across registries)
        se_pos_orig = se.positions.copy()
        se_sym = np.array(se.symbols)
        se_z_min = se_pos_orig[:, 2].min()

        # Pre-compute NCM positions (will translate per registry)
        ncm_pos_orig = ncm.positions.copy()
        ncm_sym = np.array(ncm.symbols)
        ncm_pos_orig[:, 2] -= ncm_pos_orig[:, 2].min()  # bottom at z=0
        ncm_z_max = ncm_pos_orig[:, 2].max()

        # SE will be translated so its bottom is at z = ncm_z_max + d
        se_z_shift = ncm_z_max + D_WELL - se_z_min
        se_pos = se_pos_orig.copy()
        se_pos[:, 2] += se_z_shift

        cell_xy = se.cell.array[:2, :2]

        # Loop over registries, vectorized inner
        sum_counts = {k: 0 for k in CUTOFFS}
        for (reg_name, shift_frac) in ALL_REG:
            dx, dy = shift_frac
            shift_cart = dx * ncm.cell.array[0] + dy * ncm.cell.array[1]
            ncm_pos = ncm_pos_orig.copy()
            ncm_pos[:, :2] += shift_cart[:2]
            cs = count_pairs_vectorized(se_pos, se_sym, ncm_pos, ncm_sym, cell_xy)
            for k in CUTOFFS:
                sum_counts[k] += cs[k]
        mean_counts = {k: v / len(ALL_REG) for k, v in sum_counts.items()}

        area = abs(np.cross(np.append(se.cell.array[0, :2], 0),
                            np.append(se.cell.array[1, :2], 0))[2])
        densities = {f'{k[0]}-{k[1]}': v / area for k, v in mean_counts.items()}

        results[comp] = {
            'face': info['face'], 'family': info['family'],
            'paper': info['paper'], 'area': float(area),
            'mean_counts': {f'{k[0]}-{k[1]}': v for k, v in mean_counts.items()},
            'densities': densities,
        }
        print(f"  {comp:<10} (face {info['face']}, {info['family']}, paper={info['paper']}): "
              f"area={area:.2f} Å²  ({time.time()-t_comp:.1f}s)", flush=True)

    # Tables and correlations
    paper_arr = np.array([results[c]['paper'] for c in COMBO], dtype=float)

    print(f"\n--- Mean counts per registry at d={D_WELL} Å (36-reg average) ---")
    print(f"{'pair':>8} | {'comp1':>8} {'comp2':>8} {'comp3':>8} {'comp4':>8} {'comp5':>8} | {'R':>8} {'ρ':>7}")
    print("-" * 90)
    pairs = list(CUTOFFS.keys())
    rs = []
    for p in pairs:
        pk = f'{p[0]}-{p[1]}'
        vals = np.array([results[c]['mean_counts'][pk] for c in COMBO])
        if vals.std() > 0:
            R = float(np.corrcoef(vals, paper_arr)[0, 1])
            rho = float(spearmanr(vals, paper_arr).statistic)
        else:
            R, rho = float('nan'), float('nan')
        rs.append((pk, R, rho, vals.tolist()))
        print(f"{pk:>8} | {vals[0]:>8.3f} {vals[1]:>8.3f} {vals[2]:>8.3f} {vals[3]:>8.3f} {vals[4]:>8.3f} | "
              f"{R:>+8.4f} {rho:>+7.3f}", flush=True)

    print(f"\n--- Mean DENSITY (count / Å²) ---")
    print(f"{'pair':>8} | {'comp1':>9} {'comp2':>9} {'comp3':>9} {'comp4':>9} {'comp5':>9} | {'R':>8} {'ρ':>7}")
    print("-" * 95)
    for p in pairs:
        pk = f'{p[0]}-{p[1]}'
        vals = np.array([results[c]['densities'][pk] for c in COMBO])
        if vals.std() > 0:
            R = float(np.corrcoef(vals, paper_arr)[0, 1])
            rho = float(spearmanr(vals, paper_arr).statistic)
        else:
            R, rho = float('nan'), float('nan')
        print(f"{pk:>8} | {vals[0]:>9.5f} {vals[1]:>9.5f} {vals[2]:>9.5f} {vals[3]:>9.5f} {vals[4]:>9.5f} | "
              f"{R:>+8.4f} {rho:>+7.3f}", flush=True)

    print(f"\n--- Sorted by |R| ---")
    rs.sort(key=lambda x: -abs(x[1]) if not np.isnan(x[1]) else 0)
    for pk, R, rho, _ in rs:
        flag = '🎯' if not np.isnan(R) and abs(R) > 0.9 else ''
        print(f"  {pk:>8}: R={R:+.4f}, ρ={rho:+.3f}  {flag}")

    out = {'D_WELL': D_WELL, 'n_registries': len(ALL_REG),
           'per_comp': results,
           'correlations': [{'pair': pk, 'R': R, 'rho': rho, 'counts_per_reg': c}
                            for pk, R, rho, c in rs]}
    json.dump(out, open(OUT_JSON, 'w'), indent=2)
    print(f"\nSaved: {OUT_JSON}")
    print(f"Total runtime: {time.time()-t0:.1f} s")


if __name__ == '__main__':
    main()
