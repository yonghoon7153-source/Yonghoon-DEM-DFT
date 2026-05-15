#!/usr/bin/env python
"""bond_density_FINAL_combo.py — bond density for THE final combo (R=+0.9888).

Same FINAL combo as plot_killer_v2_R0988_final.py:
  comp1     : comp1_slab_v2.xyz                              face A   (Li+S+Cl)
  comp2     : comp2_slab_v2.xyz                              face A   (Li+S+Cl)
  comp3_v2  : comp3_slab_v2_PRESERVED.HIDE  (preShift)       face B   (Li+Cl)
  comp4_v2  : comp4_v2_slab_shift2.xyz                       face B   (Li+Cl)
  comp5_v2  : comp5_v2_slab_shift2.xyz                       face A   (Li+S+Cl)

For each comp, stack SE/NCM at d=1.4 Å, count contacts within ionic-radius
cutoffs. Report 14 pair densities and R, ρ vs paper Wad.

Run from /data/work/v30u_ensemble/
"""
import json
from pathlib import Path
import numpy as np
from ase.io import read
from scipy.stats import spearmanr

WORK = Path('/data/work/v30u_ensemble')

# FINAL combo — 5 comps with explicit slab + face
COMBO = {
    'comp1':    {'se': 'comp1_slab_v2.xyz',                'face': 'A',
                 'ncm': 'ncm_7x7x1_PRESERVED.xyz', 'paper': 194, 'family': 'Li6'},
    'comp2':    {'se': 'comp2_slab_v2.xyz',                'face': 'A',
                 'ncm': 'ncm_7x7x1_PRESERVED.xyz', 'paper': 180, 'family': 'Li6'},
    'comp3_v2': {'se': 'comp3_slab_v2_PRESERVED.HIDE',     'face': 'B',
                 'ncm': 'ncm_5x5x1_PRESERVED.xyz', 'paper': 316, 'family': 'Li5.4'},
    'comp4_v2': {'se': 'comp4_v2_slab_shift2.xyz',         'face': 'B',
                 'ncm': 'ncm_5x5x1_PRESERVED.xyz', 'paper': 298, 'family': 'Li5.4'},
    'comp5_v2': {'se': 'comp5_v2_slab_shift2.xyz',         'face': 'A',
                 'ncm': 'ncm_5x5x1_PRESERVED.xyz', 'paper': 249, 'family': 'Li5.4'},
}
D_WELL = 1.4
VACUUM_TOP = 30.0

NCM_M = {'Ni', 'Co', 'Mn'}

# Pair cutoffs (Å) — ionic-radii based
CUTOFFS = {
    ('Li', 'O'):  2.8, ('Li', 'M'): 3.0, ('Li', 'Li'): 3.0,
    ('S',  'O'):  3.0, ('S',  'M'): 3.0, ('S',  'Li'): 3.0,
    ('Cl', 'O'):  3.2, ('Cl', 'M'): 3.3, ('Cl', 'Li'): 3.2,
    ('Br', 'O'):  3.4, ('Br', 'M'): 3.5, ('Br', 'Li'): 3.4,
    ('P',  'O'):  3.5, ('P',  'M'): 3.5,
}


def flip_se_xy(se):
    """Mirror SE slab in z (face A ↔ face B)."""
    a = se.copy()
    pos = a.positions.copy()
    pos[:, 2] = pos[:, 2].max() + pos[:, 2].min() - pos[:, 2]
    a.set_positions(pos)
    return a


def stack(se, ncm, d):
    se_a = se.copy(); ncm_a = ncm.copy()
    se_a.set_pbc([True, True, False])
    ncm_a.set_pbc([True, True, False])
    se_max = se_a.positions[:, 2].max()
    ncm_min = ncm_a.positions[:, 2].min()
    shift_z = se_max + d - ncm_min
    ncm_a.translate([0, 0, shift_z])
    combined = se_a + ncm_a
    cell = se_a.cell.array.copy()
    cell[2, 2] = combined.positions[:, 2].max() + VACUUM_TOP
    combined.set_cell(cell)
    return combined, len(se_a), len(ncm_a)


def count_pairs(atoms, n_se):
    """Count SE × NCM contact pairs within cutoffs."""
    pos = atoms.positions
    sym = np.array(atoms.symbols)
    cell = atoms.cell.array
    # PBC-aware xy distance
    a, b = cell[0, :2], cell[1, :2]

    se_mask = np.arange(len(atoms)) < n_se
    ncm_mask = ~se_mask

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
            for jj in i_ncm:
                r = pos[jj] - pos[ii]
                # MIC in xy
                inv = np.linalg.inv(cell[:2, :2].T)
                frac = inv @ r[:2]
                frac -= np.round(frac)
                r_xy = cell[:2, :2].T @ frac
                d2 = r_xy[0]**2 + r_xy[1]**2 + r[2]**2
                if d2 < cut**2:
                    c += 1
        counts[(se_el, ncm_el_token)] = c
    return counts


def main():
    results = []
    print("=" * 110)
    print("Bond density at d=1.4 Å — FINAL combo (R=+0.9888 figure)")
    print("=" * 110)

    for comp, info in COMBO.items():
        se = read(info['se'], format='extxyz')
        ncm = read(info['ncm'], format='extxyz')
        if info['face'] == 'B':
            se = flip_se_xy(se)
        stacked, n_se, n_ncm = stack(se, ncm, D_WELL)
        area = np.abs(np.cross(stacked.cell.array[0, :2], stacked.cell.array[1, :2]))
        counts = count_pairs(stacked, n_se)

        densities = {f'{k[0]}-{k[1]}': v / area for k, v in counts.items()}
        rec = {
            'comp': comp, 'face': info['face'], 'family': info['family'],
            'paper': info['paper'], 'area': float(area),
            'n_se': n_se, 'n_ncm': n_ncm,
            'counts': {f'{k[0]}-{k[1]}': v for k, v in counts.items()},
            'densities': densities,
        }
        results.append(rec)

        print(f"\n--- {comp} (face {info['face']}, {info['family']}, paper={info['paper']}) ---")
        print(f"  area = {area:.2f} Å², n_se={n_se}, n_ncm={n_ncm}")
        for k, v in densities.items():
            c = counts[tuple(k.split('-'))]
            print(f"  {k:>6}  count={c:>3}  density={v:.5f}/Å²")

    # Compute R, ρ for each pair density vs paper
    print("\n" + "=" * 110)
    print("Correlation with paper Wad (5 comps)")
    print("=" * 110)
    print(f"{'pair':>8}  {'R':>8}  {'ρ':>8}  {'comp1':>9}  {'comp2':>9}  {'comp3':>9}  {'comp4':>9}  {'comp5':>9}")
    print("-" * 110)
    pairs_list = list(CUTOFFS.keys())
    rs = []
    paper_arr = np.array([info['paper'] for info in COMBO.values()], dtype=float)
    for p in pairs_list:
        pk = f'{p[0]}-{p[1]}'
        d_arr = np.array([r['densities'][pk] for r in results])
        R = float(np.corrcoef(d_arr, paper_arr)[0, 1]) if d_arr.std() > 0 else float('nan')
        rho = float(spearmanr(d_arr, paper_arr).statistic) if d_arr.std() > 0 else float('nan')
        rs.append((pk, R, rho, d_arr.tolist()))
        print(f"{pk:>8}  {R:+8.4f}  {rho:+8.3f}  "
              f"{d_arr[0]:.5f}  {d_arr[1]:.5f}  {d_arr[2]:.5f}  {d_arr[3]:.5f}  {d_arr[4]:.5f}")

    # Killer descriptor candidates (|R| > 0.9)
    print("\n--- Killer descriptors (|R| > 0.9) ---")
    for pk, R, rho, _ in sorted(rs, key=lambda x: -abs(x[1])):
        if abs(R) > 0.9:
            print(f"  {pk}: R={R:+.4f}, ρ={rho:+.3f}")

    # ANION-O sum descriptor (S-O + Cl-O + Br-O) — paper's hypothesis
    print("\n--- ANION-O sum descriptor (S-O + Cl-O + Br-O) ---")
    anion_o = np.array([
        r['densities']['S-O'] + r['densities']['Cl-O'] + r['densities']['Br-O']
        for r in results
    ])
    R_ao = float(np.corrcoef(anion_o, paper_arr)[0, 1])
    rho_ao = float(spearmanr(anion_o, paper_arr).statistic)
    print(f"  ANION-O  R={R_ao:+.4f}, ρ={rho_ao:+.3f}")
    print(f"  values:  comp1={anion_o[0]:.5f}, comp2={anion_o[1]:.5f}, "
          f"comp3={anion_o[2]:.5f}, comp4={anion_o[3]:.5f}, comp5={anion_o[4]:.5f}")

    # Save full results
    out = {'combo': str(COMBO), 'D_WELL': D_WELL,
           'pairs': [{'pair': pk, 'R': R, 'rho': rho, 'densities': d}
                     for pk, R, rho, d in rs],
           'anion_o': {'R': R_ao, 'rho': rho_ao, 'values': anion_o.tolist()},
           'per_comp': results}
    json.dump(out, open(WORK / 'bond_density_FINAL_combo.json', 'w'), indent=2, default=str)
    print(f"\nSaved: {WORK}/bond_density_FINAL_combo.json")


if __name__ == "__main__":
    main()
