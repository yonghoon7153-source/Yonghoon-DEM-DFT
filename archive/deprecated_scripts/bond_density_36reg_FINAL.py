#!/usr/bin/env python
"""bond_density_36reg_FINAL.py — bond density averaged over 36 registries.

Replaces single-config bond_density_FINAL_combo.py with proper
36-registry sampling (6 high-symmetry + 30 random seed=42, matching
face_flip protocol).

For each of 15 SE×NCM element pair types, computes mean contact
density (per A^2) averaged over 36 registries at d=1.4 A (well minimum).

No UMA required — geometric counting only.
Runtime ~30 sec on CPU.

Run from /data/work/v30u_ensemble/
"""
import json
from pathlib import Path
import numpy as np
from ase.io import read
from scipy.stats import spearmanr

WORK = Path('/data/work/v30u_ensemble')
OUT_JSON = WORK / 'bond_density_36reg_FINAL.json'
D_WELL = 1.4
VACUUM_TOP = 30.0
RANDOM_SEED = 42

# FINAL combo
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

# 36 registry list (matches face_flip protocol)
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

# All 15 SE x NCM element pair types
SE_ELEMS = ['Li', 'P', 'S', 'Cl', 'Br']
NCM_M = {'Ni', 'Co', 'Mn'}
NCM_TYPES = ['O', 'M', 'Li']

# Ionic-radius-based cutoffs (Å)
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


def stack(se, ncm, d, shift_frac):
    """NCM at bottom, SE on top, with NCM xy-shift."""
    se_a = se.copy(); ncm_a = ncm.copy()
    dx, dy = shift_frac
    shift_cart = dx * ncm_a.cell.array[0] + dy * ncm_a.cell.array[1]
    ncm_a.translate([shift_cart[0], shift_cart[1], 0])
    ncm_a.wrap()
    ncm_a.translate([0, 0, -ncm_a.positions[:, 2].min()])
    ncm_z_max = ncm_a.positions[:, 2].max()
    se_z_min = se_a.positions[:, 2].min()
    se_a.translate([0, 0, ncm_z_max - se_z_min + d])
    combined = ncm_a + se_a
    new_cell = se.cell.array.copy()
    z_extent = combined.positions[:, 2].max() - combined.positions[:, 2].min()
    new_cell[2] = [0, 0, z_extent + VACUUM_TOP]
    combined.set_cell(new_cell, scale_atoms=False)
    combined.set_pbc([True, True, True])
    return combined, len(ncm_a), len(se_a)


def count_pairs(atoms, n_ncm, n_se):
    """Count SE × NCM contact pairs within cutoffs."""
    pos = atoms.positions
    sym = np.array(atoms.symbols)
    cell = atoms.cell.array
    # NCM first half, SE second (since combined = ncm_a + se_a)
    ncm_mask = np.arange(len(atoms)) < n_ncm
    se_mask = ~ncm_mask
    inv = np.linalg.inv(cell[:2, :2].T)

    counts = {}
    for (se_el, ncm_el_token), cut in CUTOFFS.items():
        if ncm_el_token == 'M':
            ncm_elems = NCM_M
        else:
            ncm_elems = {ncm_el_token}
        i_se = np.where(se_mask & (sym == se_el))[0]
        i_ncm = np.where(ncm_mask & np.isin(sym, list(ncm_elems)))[0]
        if len(i_se) == 0 or len(i_ncm) == 0:
            counts[(se_el, ncm_el_token)] = 0
            continue
        c = 0
        for ii in i_se:
            ri = pos[ii]
            for jj in i_ncm:
                r = pos[jj] - ri
                # MIC in xy
                frac = inv @ r[:2]
                frac -= np.round(frac)
                r_xy = cell[:2, :2].T @ frac
                d2 = r_xy[0]**2 + r_xy[1]**2 + r[2]**2
                if d2 < cut**2:
                    c += 1
        counts[(se_el, ncm_el_token)] = c
    return counts


def main():
    import time
    t0 = time.time()
    print("=" * 110)
    print(f"36-reg averaged bond density at d={D_WELL} Å — FINAL combo")
    print(f"  {len(HIGH_SYM)} high-sym + {N_RANDOM} random = {len(ALL_REG)} registries")
    print("=" * 110)

    results = {}
    for comp, info in COMBO.items():
        se = read(info['se'], format='extxyz')
        if info['face'] == 'B':
            se = flip_se_xy(se)
        ncm = read(info['ncm'], format='extxyz')

        # Average count per registry
        sum_counts = {k: 0 for k in CUTOFFS}
        for (reg_name, shift_frac) in ALL_REG:
            stacked, n_ncm, n_se = stack(se, ncm, D_WELL, shift_frac)
            cs = count_pairs(stacked, n_ncm, n_se)
            for k in CUTOFFS:
                sum_counts[k] += cs[k]
        mean_counts = {k: v / len(ALL_REG) for k, v in sum_counts.items()}

        # Area for density normalization
        area = abs(np.cross(np.append(se.cell.array[0, :2], 0),
                            np.append(se.cell.array[1, :2], 0))[2])
        densities = {f'{k[0]}-{k[1]}': v / area for k, v in mean_counts.items()}

        results[comp] = {
            'face': info['face'],
            'family': info['family'],
            'paper': info['paper'],
            'area': float(area),
            'mean_counts': {f'{k[0]}-{k[1]}': v for k, v in mean_counts.items()},
            'densities': densities,
        }
        print(f"  {comp:<10} (face {info['face']}, {info['family']}, paper={info['paper']}): area={area:.2f} Å²  done")

    # Per-pair table + correlations
    print(f"\n--- Mean counts per registry at d={D_WELL} Å (36-reg average) ---")
    print(f"{'pair':>8} | {'comp1':>8} {'comp2':>8} {'comp3':>8} {'comp4':>8} {'comp5':>8} | {'R':>8} {'ρ':>7}")
    print("-" * 90)
    pairs = list(CUTOFFS.keys())
    paper_arr = np.array([results[c]['paper'] for c in COMBO], dtype=float)
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
              f"{R:>+8.4f} {rho:>+7.3f}")

    print(f"\n--- Mean DENSITY (count / Å²) at d={D_WELL} Å (36-reg average) ---")
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
              f"{R:>+8.4f} {rho:>+7.3f}")

    # Sort by |R|
    print(f"\n--- Sorted by |R| (strongest correlation first) ---")
    rs.sort(key=lambda x: -abs(x[1]) if not np.isnan(x[1]) else 0)
    for pk, R, rho, _ in rs[:10]:
        print(f"  {pk}: R={R:+.4f}, ρ={rho:+.3f}")

    # Killer descriptors
    print(f"\n--- |R| > 0.9 ---")
    for pk, R, rho, _ in rs:
        if not np.isnan(R) and abs(R) > 0.9:
            print(f"  {pk}: R={R:+.4f}, ρ={rho:+.3f}")

    # Save
    out = {'D_WELL': D_WELL, 'n_registries': len(ALL_REG),
           'per_comp': results,
           'correlations': [{'pair': pk, 'R': R, 'rho': rho, 'counts_per_reg': c}
                            for pk, R, rho, c in rs]}
    json.dump(out, open(OUT_JSON, 'w'), indent=2)
    print(f"\nSaved: {OUT_JSON}")
    print(f"Runtime: {time.time()-t0:.1f} s")


if __name__ == '__main__':
    main()
