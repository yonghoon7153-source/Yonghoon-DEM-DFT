#!/usr/bin/env python
"""Enumerate all 32 face combos for v1 face_flip data with OLD recipe.

Recipe:
  Wad_alpha = Wad_well_mean - ALPHA * dW_strain    (ALPHA = 1.0)

For each combo check:
  - R(Wad_alpha, paper)
  - ρ(Wad_alpha, paper)
  - family_ok: Li5.4 min Wad+α < Li6 max Wad+α   (Li6 ends up deeper)
  - rank_ok_345: comp3 < comp4 < comp5  (Wad+α; smaller = deeper)
                 ↳ paper rank with deeper=lower-Wad+α
  - rank_ok_strict: full paper rank (comp2>comp1>comp5>comp4>comp3 in Wad+α
                                     i.e. comp2 has largest, comp3 smallest)

dW source:
  - tries v30u_1L_correct_results_eiso_fix/{comp}_done.json
  - falls back to per-comp stub if not present
  - for v1 (not v2): uses uniform DW=0.44 for Li5.4, larger for Li6
    (can override with --uniform-dw)

Run from /data/work/v30u_ensemble/
"""
import json, sys, os
from itertools import product
from pathlib import Path
import numpy as np
from scipy.stats import spearmanr

WORK = Path('/data/work/v30u_ensemble')
FACE = WORK / 'face_flip_results'
EISO = WORK / 'v30u_1L_correct_results_eiso_fix'

COMPS = ['comp1', 'comp2', 'comp3_v1', 'comp4_v1', 'comp5_v1']
PAPER = np.array([194, 180, 316, 298, 249], float)
ALPHA = 1.0

# dW fallback (v1 stub from OLD figure era — uniform Li5.4 0.44; Li6 from current eiso)
DW_STUB = {
    'comp1': 2.633,
    'comp2': 2.503,
    'comp3_v1': 0.44,
    'comp4_v1': 0.44,
    'comp5_v1': 0.44,
}
EISO_KEY = {'comp1':'comp1','comp2':'comp2','comp3_v1':'comp3','comp4_v1':'comp4','comp5_v1':'comp5'}

def get_dw(c):
    p = EISO / f'{EISO_KEY[c]}_done.json'
    if p.exists():
        return float(json.load(open(p))['delta_Wad_J_per_m2'])
    return DW_STUB[c]

# Load all data
ff = {}
dw = {}
for c in COMPS:
    p = FACE / f'{c}_done.json'
    if not p.exists():
        print(f"MISSING {p} — abort"); sys.exit(1)
    ff[c] = json.load(open(p))['faces']
    dw[c] = get_dw(c)

print("Wad_well_mean (A / B):")
for c in COMPS:
    print(f"  {c:10}  A={ff[c]['A']['Wad_well_mean']:+.4f}   B={ff[c]['B']['Wad_well_mean']:+.4f}   dW={dw[c]:+.3f}")
print(f"\nPaper Wad (aJ): {dict(zip(COMPS, PAPER))}\n")

results = []
for faces in product('AB', repeat=5):
    wells = []
    for c, f in zip(COMPS, faces):
        wm = ff[c][f]['Wad_well_mean']
        wa = wm - ALPHA * dw[c]
        wells.append(wa)
    wells = np.array(wells)

    R = float(np.corrcoef(wells, PAPER)[0, 1])
    rho = float(spearmanr(wells, PAPER).statistic)

    # Conventions:
    # - Wad+α: larger = stronger binding in this recipe (Wad is positive at well)
    # - But OLD figure shows binding as NEGATIVE (E_adh = -Wad), so visual:
    #   smaller Wad+α = shallower in figure
    #   larger Wad+α = deeper in figure
    # Paper: comp3 strongest (316). So we want comp3 to have LARGEST Wad+α.

    li6_max  = max(wells[0], wells[1])    # max of comp1,comp2
    li54_min = min(wells[2], wells[3], wells[4])  # min of comp3/4/5
    li54_max = max(wells[2], wells[3], wells[4])

    # family_ok: Li5.4 family has LARGER Wad+α than Li6 (deeper in figure)
    family_ok = li54_min > li6_max

    # rank_ok_345: within Li5.4: comp3 > comp4 > comp5  (Wad+α; larger = deeper)
    rank_ok_345 = wells[2] > wells[3] > wells[4]

    # rank_ok_strict: full paper rank (Wad+α descending: comp3 > comp4 > comp5 > comp1 > comp2)
    rank_strict = (wells[2] > wells[3] > wells[4] > wells[0] > wells[1])

    results.append((''.join(faces), R, rho, family_ok, rank_ok_345, rank_strict, wells.tolist()))

# Sort by R descending
results.sort(key=lambda x: -x[1])
print(f"{'combo':6}  {'R':>8}  {'rho':>7}  fam  3>4>5 strict  wells (1,2,3v1,4v1,5v1)")
print("-"*110)
for r in results:
    combo, R, rho, fok, rok345, rok_str, w = r
    print(f"{combo}  {R:+8.4f}  {rho:+7.3f}  {fok!s:5} {rok345!s:5} {rok_str!s:5}  "
          f"[{w[0]:+.2f} {w[1]:+.2f} {w[2]:+.2f} {w[3]:+.2f} {w[4]:+.2f}]")

print("\n=== family_ok (Li5.4 deeper than Li6) ===")
n_fam = sum(1 for r in results if r[3])
print(f"  {n_fam}/32 combos")

print("\n=== rank_ok_345 (comp3>comp4>comp5 within Li5.4) ===")
hits_345 = [r for r in results if r[4]]
print(f"  {len(hits_345)}/32 combos")
for r in hits_345:
    combo,R,rho,fok,rok345,rok_str,w = r
    print(f"  {combo}  R={R:+.4f}  rho={rho:+.3f}  fam={fok}  strict={rok_str}  wells={[round(x,2) for x in w]}")

print("\n=== rank_strict (full paper rank) ===")
hits_str = [r for r in results if r[5]]
print(f"  {len(hits_str)}/32 combos")
for r in hits_str:
    combo,R,rho,fok,rok345,rok_str,w = r
    print(f"  {combo}  R={R:+.4f}  rho={rho:+.3f}  fam={fok}  wells={[round(x,2) for x in w]}")
