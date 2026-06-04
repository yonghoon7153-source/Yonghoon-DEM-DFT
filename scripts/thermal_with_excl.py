#!/usr/bin/env python3
"""Test: thermal Physics target with σ_e EXCL applied.

After backfill_stage_e_physics.py recovered 9 cases, σ_thermal Physics
target corpus is ~100.  But many added cases are σ_e EXCL family —
known outliers.  Apply σ_e EXCL to thermal corpus to test if cleanup
restores LOOCV.

Compare to baseline 0.81 (76 cases, original Physics Stage E corpus).
"""
import sys, json, glob
from pathlib import Path
from collections import Counter
import numpy as np

sys.path.insert(0, str(Path(__file__).parent))

# σ_e EXCL (from generate_comparison_plots._EXCLUDED_NAMES_EL)
EXCL_NAMES = {
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

from thermal_physics_target import load_corpus, fit_ridge_loocv


def main():
    cases = load_corpus()
    print(f"\nPhysics Stage E corpus: {len(cases)}")
    cases_clean = [c for c in cases if c['_name'] not in EXCL_NAMES]
    excluded_present = [c['_name'] for c in cases if c['_name'] in EXCL_NAMES]
    print(f"After σ_e EXCL: {len(cases_clean)} (excluded {len(excluded_present)} known outliers)")
    if excluded_present:
        print(f"  EXCL cases in Physics corpus: {len(excluded_present)}")
        for nm in excluded_present[:8]:
            print(f"    - {nm}")
        if len(excluded_present) > 8:
            print(f"    ... +{len(excluded_present)-8} more")

    y = np.log(np.array([c['_kappa'] for c in cases_clean]))

    EXCLUDE = ('thermal_sigma', 'sigma_full_mScm',
               'electronic_sigma_full_mScm', '_')
    def is_excluded(k): return any(k.startswith(p) for p in EXCLUDE)
    counts = Counter()
    for c in cases_clean:
        for k in c:
            if not is_excluded(k): counts[k] += 1
    common = [k for k, ct in counts.items() if ct / len(cases_clean) >= 0.90]

    feature_data = []
    for k in common:
        vals = np.array([c.get(k, np.nan) for c in cases_clean])
        if not np.all(np.isfinite(vals)): continue
        if np.min(vals) > 0:
            feature_data.append((f'log({k})', np.log(vals)))
        feature_data.append((k, vals))
    print(f"features: {len(feature_data)}\n")

    print("=" * 90)
    print(f"  Greedy forward selection on EXCL-clean corpus (n={len(cases_clean)})")
    print("=" * 90)
    selected = []
    remaining = list(range(len(feature_data)))
    best = -np.inf; history = []
    for step in range(20):
        best_step = -np.inf; best_idx = None
        for idx in remaining:
            try_idx = selected + [idx]
            X = np.column_stack([feature_data[i][1] for i in try_idx])
            try:
                _, loo, _ = fit_ridge_loocv(X, y, alpha=0.1)
                if loo > best_step:
                    best_step = loo; best_idx = idx
            except: continue
        if best_idx is None: break
        selected.append(best_idx); remaining.remove(best_idx)
        flag = ' ⭐' if best_step >= 0.9 else (' ★' if best_step > 0.5 else '')
        print(f"  Step {step+1:2d}  {feature_data[best_idx][0][:55]:55s}  LOOCV={best_step:.4f}{flag}")
        history.append((step+1, feature_data[best_idx][0], best_step))
        if best_step > best: best = best_step
        if step >= 3 and history[-1][2] - history[-2][2] < 0.001:
            print(f"           plateau, stop")
            break

    print()
    print("=" * 90)
    print(f"  VERDICT")
    print("=" * 90)
    print(f"  Best LOOCV (EXCL-clean): {best:.4f}")
    print(f"  Baseline (n=76, no EXCL):    0.8147")
    print(f"  Diff: {best - 0.8147:+.4f}")
    if best >= 0.9:
        print(f"  ⭐ MEETS 0.9 — EXCL was the key!")
    elif best >= 0.85:
        print(f"  Close to 0.9 but not quite")
    else:
        print(f"  Still ceiling; EXCL helps but doesn't reach threshold")


if __name__ == '__main__':
    main()
