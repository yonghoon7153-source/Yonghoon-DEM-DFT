#!/usr/bin/env python3
"""Compare 1mAh_5_AMP_S* vs 1mAh_8_AMP_S* at full precision to detect
accidental duplicate uploads (same sim data under wrong name)."""
import json, glob
from pathlib import Path

# Compare these pairs
PAIRS = [(f'input_1mAh_5_AMP_S{i}', f'input_1mAh_8_AMP_S{i}') for i in range(1, 6)]

# Keys that should be IDENTICAL if same data, DIFFERENT if separate sims
KEYS = [
    'phi_am', 'phi_se', 'porosity', 'porosity_spheresum', 'porosity_union',
    'thickness_um', 'plate_z', 'percolation_pct',
    'am_am_cn', 'am_am_n_contacts', 'am_am_mean_area',
    'electronic_sigma_full_mScm', 'electronic_sigma_full_mScm_stage_e',
    'electronic_sigma_full_mScm_physics',
    'sigma_full_mScm', 'sigma_full_mScm_stage_e',
    'tortuosity_electronic_recommended',
    'coverage_AM_P_mean', 'coverage_AM_S_mean',
    'se_se_cn', 'am_se_cn_mean',
]

def find_case(name):
    for p in Path('webapp/archive').rglob(name):
        if p.is_dir() and (p / 'full_metrics.json').exists():
            return p
    return None

for a_name, b_name in PAIRS:
    pa = find_case(a_name); pb = find_case(b_name)
    if pa is None or pb is None:
        print(f"\n── {a_name} vs {b_name} — MISSING ({a_name if pa is None else b_name})")
        continue
    da = json.load(open(pa / 'full_metrics.json'))
    db = json.load(open(pb / 'full_metrics.json'))
    print(f"\n── {a_name}  vs  {b_name}")
    print(f"   ({pa})")
    print(f"   ({pb})")
    n_same, n_diff = 0, 0
    for k in KEYS:
        va, vb = da.get(k), db.get(k)
        if va is None and vb is None: continue
        same = (va == vb)
        if same: n_same += 1
        else: n_diff += 1
        flag = '=' if same else '≠'
        print(f"   {flag} {k:42s}  {str(va)[:18]:>18s}  vs  {str(vb)[:18]:18s}")
    verdict = 'IDENTICAL — likely same sim uploaded twice' if n_diff == 0 else \
              f'DISTINCT ({n_diff} differing keys)'
    print(f"   → {verdict}")

# Check input_params.json too — these would differ if true distinct sims
print("\n\n── input_params.json comparison (random seed should differ for distinct sims):")
for a_name, b_name in PAIRS:
    pa = find_case(a_name); pb = find_case(b_name)
    if pa is None or pb is None: continue
    try:
        ipa = json.load(open(pa / 'input_params.json'))
        ipb = json.load(open(pb / 'input_params.json'))
    except: continue
    seed_a = ipa.get('seed') or ipa.get('random_seed') or ipa.get('variables', {}).get('seed', '?')
    seed_b = ipb.get('seed') or ipb.get('random_seed') or ipb.get('variables', {}).get('seed', '?')
    ame_a = ipa.get('am_se_ratio') or ipa.get('mass_fractions', {}).get('am_se_ratio')
    ame_b = ipb.get('am_se_ratio') or ipb.get('mass_fractions', {}).get('am_se_ratio')
    print(f"   {a_name:25s}  seed={seed_a}  am:se={ame_a}")
    print(f"   {b_name:25s}  seed={seed_b}  am:se={ame_b}")
