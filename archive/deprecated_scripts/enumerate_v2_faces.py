#!/usr/bin/env python
"""Enumerate 32 face combos for v2 shift 2 face_flip data with OLD recipe.

Recipe:
  Wad_alpha = Wad_well_mean - ALPHA * dW_strain    (ALPHA = 1.0)

Goal:
  Find face combo (A/B per comp) giving:
    - positive R(Wad_alpha, paper Wad)
    - Li5.4 family deeper than Li6 (family_ok)
    - within Li5.4: comp3 > comp4 > comp5 (rank_ok)

Run from /data/work/v30u_ensemble/
"""
import json, numpy as np
from itertools import product
from scipy.stats import spearmanr

COMPS = ['comp1', 'comp2', 'comp3_v2', 'comp4_v2', 'comp5_v2']
EISO  = {'comp1':'comp1','comp2':'comp2','comp3_v2':'comp3','comp4_v2':'comp4','comp5_v2':'comp5'}
PAPER = np.array([194, 180, 316, 298, 249], float)
ALPHA = 1.0

ff = {}
dw = {}
for c in COMPS:
    j = json.load(open(f'face_flip_results/{c}_done.json'))
    ff[c] = j['faces']
    e = json.load(open(f'v30u_1L_correct_results_eiso_fix/{EISO[c]}_done.json'))
    dw[c] = float(e.get('delta_Wad_J_per_m2', e.get('dW_strain', 0.0)))

print("dW(eiso):", {c: f"{dw[c]:+.3f}" for c in COMPS})
print("face_flip Wad_well_mean (A / B):")
for c in COMPS:
    print(f"  {c:10}  A={ff[c]['A']['Wad_well_mean']:+.4f}   B={ff[c]['B']['Wad_well_mean']:+.4f}")

results = []
for faces in product('AB', repeat=5):
    wells = []
    for c, f in zip(COMPS, faces):
        wm = ff[c][f]['Wad_well_mean']
        wa = wm - ALPHA * dw[c]
        wells.append(wa)
    wells = np.array(wells)
    R   = float(np.corrcoef(wells, PAPER)[0, 1])
    rho = float(spearmanr(wells, PAPER).statistic)
    li6_max  = max(wells[0], wells[1])
    li54_min = min(wells[2], wells[3], wells[4])
    family_ok = li54_min < li6_max
    rank_ok   = wells[2] < wells[3] < wells[4]
    results.append((''.join(faces), R, rho, family_ok, rank_ok, wells.tolist()))

results.sort(key=lambda x: -x[1])
print(f"\nTop 10 by R   (combo order = comp1, comp2, comp3_v2, comp4_v2, comp5_v2)")
print(f"{'combo':6}  {'R':>8}  {'rho':>7}  fam  rank   wells")
for r in results[:10]:
    combo, R, rho, fok, rok, w = r
    print(f"{combo}  {R:+8.4f}  {rho:+7.3f}  {fok!s:5} {rok!s:5}  "
          f"[{w[0]:+.2f} {w[1]:+.2f} {w[2]:+.2f} {w[3]:+.2f} {w[4]:+.2f}]")

print("\nCombos satisfying BOTH family_ok AND rank_ok:")
hits = [r for r in results if r[3] and r[4]]
if not hits:
    print("  (none)")
else:
    for combo, R, rho, fok, rok, w in hits:
        print(f"  {combo}  R={R:+.4f}  rho={rho:+.3f}  "
              f"wells=[{w[0]:+.2f} {w[1]:+.2f} {w[2]:+.2f} {w[3]:+.2f} {w[4]:+.2f}]")
