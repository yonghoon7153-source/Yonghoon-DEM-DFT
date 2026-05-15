#!/usr/bin/env python
"""alpha_sensitivity_FINAL.py — α strain-correction robustness for FINAL combo.

Tests whether the paper rank (comp3>4>5>1>2) holds across α ∈ [0.0, 1.5]
with the FINAL Cl-coherent slab/face combo + uniform Li5.4 dW=0.44.

Output: alpha_sensitivity_FINAL.json + console table.
"""
import json
from pathlib import Path
import numpy as np
from scipy.stats import spearmanr

# FINAL combo Wad_well_mean (raw, no α applied)
WELLS_RAW = {
    'comp1':    2.7084,
    'comp2':    2.4391,
    'comp3_v2': 1.6133,
    'comp4_v2': 1.3098,
    'comp5_v2': 1.0989,
}

# dW values
DW_UNIFORM = {'comp1': 2.633, 'comp2': 2.503,
              'comp3_v2': 0.44, 'comp4_v2': 0.44, 'comp5_v2': 0.44}
DW_PERCOMP = {'comp1': 2.633, 'comp2': 2.503,
              'comp3_v2': 0.873, 'comp4_v2': 3.640, 'comp5_v2': 0.314}

PAPER = {'comp1': 194, 'comp2': 180, 'comp3_v2': 316, 'comp4_v2': 298, 'comp5_v2': 249}
COMPS = ['comp1', 'comp2', 'comp3_v2', 'comp4_v2', 'comp5_v2']


def evaluate(alpha, dw_dict):
    wells = np.array([WELLS_RAW[c] - alpha * dw_dict[c] for c in COMPS])
    papers = np.array([PAPER[c] for c in COMPS])
    R = float(np.corrcoef(wells, papers)[0, 1])
    rho = float(spearmanr(wells, papers).statistic)
    strict = bool(wells[2] > wells[3] > wells[4] > wells[0] > wells[1])
    family_ok = bool(min(wells[2:5]) > max(wells[0:2]))
    return wells, R, rho, strict, family_ok


def main():
    alphas = np.arange(0.0, 1.51, 0.1)
    print("=" * 110)
    print("α sensitivity — uniform Li5.4 dW=0.44 (this work)  vs  per-comp dW (eiso fix)")
    print("=" * 110)
    print(f"{'α':>5} | {'R(uniform)':>11} {'ρ':>7} {'strict':>7} {'family':>7} || "
          f"{'R(per-comp)':>12} {'ρ':>7} {'strict':>7} {'family':>7}")
    print("-" * 110)
    results_U = []; results_P = []
    for a in alphas:
        wU, RU, rhoU, strU, famU = evaluate(a, DW_UNIFORM)
        wP, RP, rhoP, strP, famP = evaluate(a, DW_PERCOMP)
        results_U.append({'alpha': float(a), 'R': RU, 'rho': rhoU,
                          'strict': strU, 'family_ok': famU, 'wells': wU.tolist()})
        results_P.append({'alpha': float(a), 'R': RP, 'rho': rhoP,
                          'strict': strP, 'family_ok': famP, 'wells': wP.tolist()})
        print(f"{a:5.2f} | {RU:+11.4f} {rhoU:+7.3f}   {str(strU):>5}   {str(famU):>5} || "
              f"{RP:+12.4f} {rhoP:+7.3f}   {str(strP):>5}   {str(famP):>5}")

    sU = [r['alpha'] for r in results_U if r['strict']]
    sP = [r['alpha'] for r in results_P if r['strict']]
    fU = [r['alpha'] for r in results_U if r['family_ok']]
    fP = [r['alpha'] for r in results_P if r['family_ok']]

    print("\n--- strict paper rank holds for α ∈ ... ---")
    print(f"  Uniform Li5.4 dW=0.44:  [{min(sU):.2f}, {max(sU):.2f}]   ({len(sU)}/{len(alphas)})" if sU else "  Uniform: NEVER")
    print(f"  Per-comp dW (eiso):     [{min(sP):.2f}, {max(sP):.2f}]   ({len(sP)}/{len(alphas)})" if sP else "  Per-comp: NEVER (comp4 dW=3.64 outlier)")

    print("\n--- family_ok (Li5.4 > Li6) holds for α ∈ ... ---")
    print(f"  Uniform:  [{min(fU):.2f}, {max(fU):.2f}]   ({len(fU)}/{len(alphas)})" if fU else "  Uniform: NEVER")
    print(f"  Per-comp: [{min(fP):.2f}, {max(fP):.2f}]   ({len(fP)}/{len(alphas)})" if fP else "  Per-comp: NEVER")

    # R at α=1.0
    a1_U = next(r for r in results_U if abs(r['alpha'] - 1.0) < 1e-6)
    a1_P = next(r for r in results_P if abs(r['alpha'] - 1.0) < 1e-6)
    print(f"\n--- At α=1.0 (default) ---")
    print(f"  Uniform:  R={a1_U['R']:+.4f}, ρ={a1_U['rho']:+.3f}, strict={a1_U['strict']}")
    print(f"  Per-comp: R={a1_P['R']:+.4f}, ρ={a1_P['rho']:+.3f}, strict={a1_P['strict']}")

    out = {'alphas': alphas.tolist(), 'uniform': results_U, 'per_comp': results_P}
    json.dump(out, open('alpha_sensitivity_FINAL.json', 'w'), indent=2)
    print(f"\nSaved: alpha_sensitivity_FINAL.json")


if __name__ == '__main__':
    main()
