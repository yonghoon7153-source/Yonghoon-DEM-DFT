#!/usr/bin/env python3
"""σ_thermal corpus audit — find outliers that should be EXCL.

σ_e has _EXCLUDED_NAMES_EL with 21 cases (broken sim, marginal-perc,
sibling-tails).  σ_thermal currently has NO EXCL list.

Diagnose:
  1. Cases with κ > 50 mScm (already filtered as solver pathology)
  2. Cases with κ < 0.05 mScm (broken / no percolation)
  3. Cases where κ_stage_e_physics undefined but Hertz defined (mode bug)
  4. Cases with extreme residuals after best form fit
  5. Cross-reference with σ_e EXCL list to see overlap
"""
from __future__ import annotations
import sys, json, glob
from pathlib import Path
import numpy as np

# σ_e EXCL list for cross-reference
EXCLUDED_NAMES_EL = {
    'input_1mAh_6_S1', 'input_8mAh_1', 'input_6mAh_real_10',
    'input_S_2', 'input_particulate_5', 'input_8mAh_3',
    'input_8mAh_2', 'input_1mAh_5_AMP_S2', 'input_2mAh_real_15',
    'input_8mAh_real_13', 'input_8mAh_real_12',
    'input_1mAh_5_AMP_S3', 'input_2mAh_real_10', 'input_2mAh_real_20',
    'input_1mAh_100_6', 'input_1mAh_100_8', 'input_1mAh_100_11',
    'input_8mAh_real_5',
    'input_1mAh_8_AMP_S2', 'input_1mAh_8_AMP_S5',
    'input_1mAh_5_AMP_S1', 'input_1mAh_5_AMP_S4', 'input_1mAh_5_AMP_S5',
}


def main():
    cases = []
    for f in sorted(glob.glob('webapp/archive/**/full_metrics.json', recursive=True)):
        nm = Path(f).parent.name
        if not nm.startswith('input_'): continue
        try: d = json.load(open(f))
        except: continue
        cases.append({
            'name': nm,
            'k_hertz_raw':  d.get('thermal_sigma_full_mScm') or 0,
            'k_hertz_se':   d.get('thermal_sigma_full_mScm_stage_e') or 0,
            'k_phys_raw':   d.get('thermal_sigma_full_mScm_physics') or 0,
            'k_phys_se':    d.get('thermal_sigma_full_mScm_stage_e_physics') or 0,
        })
    print(f"\n  Total cases on disk: {len(cases)}\n")

    # ─── 1. Pathology: κ > 50 or < 0.05 ───
    print("=" * 95)
    print("  1. κ value outliers (each target)")
    print("=" * 95)
    for key, lbl in [('k_hertz_raw',  'Hertz raw'),
                      ('k_hertz_se',   'Hertz Stage E'),
                      ('k_phys_raw',   'Physics raw'),
                      ('k_phys_se',    'Physics Stage E')]:
        too_high = [(c['name'], c[key]) for c in cases if c[key] > 50]
        too_low  = [(c['name'], c[key]) for c in cases if 0 < c[key] < 0.05]
        missing  = [(c['name'])         for c in cases if not c[key] or c[key] <= 0]
        print(f"\n  {lbl}:")
        print(f"    HIGH (>50):    {len(too_high)} cases")
        for nm, k in sorted(too_high, key=lambda t: -t[1])[:5]:
            print(f"      {nm:35s}  κ={k:.2f}")
        print(f"    LOW (<0.05):   {len(too_low)} cases")
        for nm, k in too_low[:5]:
            print(f"      {nm:35s}  κ={k:.4f}")
        print(f"    MISSING/0:     {len(missing)} cases")
        if missing[:5]:
            print(f"      {', '.join(missing[:5])}{' ...' if len(missing) > 5 else ''}")

    # ─── 2. Mode mismatches (Hertz exists but Physics doesn't) ───
    print()
    print("=" * 95)
    print("  2. Cases where Physics Stage E missing but Hertz Stage E present")
    print("=" * 95)
    hertz_but_no_phys = [c['name'] for c in cases
                         if c['k_hertz_se'] > 0 and not (c['k_phys_se'] and c['k_phys_se'] > 0)]
    print(f"  {len(hertz_but_no_phys)} cases:")
    for nm in hertz_but_no_phys[:15]:
        print(f"    {nm}")
    if len(hertz_but_no_phys) > 15:
        print(f"    ... +{len(hertz_but_no_phys)-15} more")

    # ─── 3. Cross-ref with σ_e EXCL list ───
    print()
    print("=" * 95)
    print("  3. σ_e EXCL list — do those have problematic thermal too?")
    print("=" * 95)
    print(f"  {'Case':35s} {'Hertz raw':>10s} {'Hertz Stage E':>13s} {'Phys raw':>10s} {'Phys Stage E':>13s}")
    by_name = {c['name']: c for c in cases}
    for nm in sorted(EXCLUDED_NAMES_EL):
        c = by_name.get(nm)
        if c is None:
            print(f"  {nm:35s}  (not on disk)")
            continue
        flag = ''
        if c['k_hertz_se'] > 50 or c['k_hertz_se'] <= 0: flag = ' ⚠'
        if c['k_phys_se'] and (c['k_phys_se'] > 50 or c['k_phys_se'] <= 0): flag = ' ⚠'
        print(f"  {nm:35s}  {c['k_hertz_raw']:>10.2f} {c['k_hertz_se']:>13.2f} "
              f"{c['k_phys_raw']:>10.2f} {c['k_phys_se']:>13.2f}{flag}")

    # ─── 4. Recommendation ───
    print()
    print("=" * 95)
    print("  4. Recommendation: σ_thermal EXCL list candidates")
    print("=" * 95)
    candidates = []
    for c in cases:
        target = c['k_phys_se'] or c['k_hertz_se'] or 0
        if target <= 0:
            candidates.append((c['name'], 'no σ_th'))
        elif target > 50:
            candidates.append((c['name'], f'σ_th={target:.0f} extreme'))
        elif target < 0.05:
            candidates.append((c['name'], f'σ_th={target:.3f} low'))
    print(f"  ({len(candidates)} potential EXCL candidates)\n")
    for nm, reason in candidates[:25]:
        in_el = ' [also σ_e EXCL]' if nm in EXCLUDED_NAMES_EL else ''
        print(f"    {nm:35s}  {reason}{in_el}")
    if len(candidates) > 25:
        print(f"    ... +{len(candidates)-25} more")


if __name__ == '__main__':
    main()
