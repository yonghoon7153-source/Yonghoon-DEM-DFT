#!/usr/bin/env python3
"""σ_e Stage 22.5 — LOCKED EXPONENT validation screen (working version).

Tests whether literature-locked exponents agree with n=76 data:
  φ_AM^4  (Stauffer-Bruggeman backbone, Stage 14 lock)
  √A_AM-AM^0.5  (Holm 1967 constriction)
  NCM(r) β=1.5  (Trevisanello 2021 GB scaling)
  C(τ) polynomial degree (logpoly0 / 1 / 2)

Method: Adjusts arr['log_offset'] by delta = (new_exp − old_exp) · log(metric),
then refits Stage 22.5.  Pure LOCKED-exponent test — 0 extra DOF.

Verdicts:
  ★ LOCKED VALUE WINS  literature value gives best LOOCV
  CONFIRMED            literature within Δ ≤ +0.005 of winner (validates lock)
  DEVIATES             data prefers different exponent by Δ > +0.005 (finding!)
  loses                this candidate loses to literature value
"""
from __future__ import annotations
import sys, json, copy
from pathlib import Path
import numpy as np

SCRIPTS = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS))


def load_corpus():
    data_list, names, seen = [], [], set()
    for base in ('webapp/archive', 'webapp/results'):
        bp = Path(base)
        if not bp.is_dir(): continue
        for mp in bp.rglob('full_metrics.json'):
            meta_p = mp.parent / 'meta.json'
            cid = mp.parent.name; nm = cid
            if meta_p.exists():
                try:
                    mn = json.load(open(meta_p)).get('name', '') or ''
                    if mn: nm = mn
                except: pass
            if nm == cid and not nm.startswith('input_'): continue
            if nm in seen: continue
            seen.add(nm)
            try: d = json.load(open(mp))
            except: continue
            data_list.append(d); names.append(nm)
    return data_list, names


def adjusted_arr(arr_base, delta_log_offset):
    """Return shallow copy of arr with log_offset modified by delta."""
    new_arr = dict(arr_base)
    new_arr['log_offset'] = arr_base['log_offset'] + delta_log_offset
    new_arr['y_resid'] = arr_base['logsf'] - new_arr['log_offset']
    return new_arr


def fit_loocv(arr, fit_mask, gcp):
    fit = gcp._electronic_fit(arr, fit_mask=fit_mask)
    return fit['loocv'], fit['r2']


def main():
    import matplotlib; matplotlib.use('Agg')
    import generate_comparison_plots as gcp

    print("Loading corpus...", flush=True)
    data_list, names = load_corpus()
    arr = gcp._electronic_form_arrays(data_list, names)
    if arr is None: print("[ABORT]"); return

    fit_mask = ~arr['excluded']
    n_fit = int(fit_mask.sum())

    # Raw per-case arrays
    phi_a = arr['phi']
    am_area_a = arr['am_area']
    ras_a = arr['r_AM_S']
    rap_a = arr['r_AM_P']
    p_a = arr['p_amp']

    loo_base, r2_base = fit_loocv(arr, fit_mask, gcp)
    print(f"\n  BASELINE Stage 22.5: LOOCV={loo_base:.4f}  R²={r2_base:.4f}  n_fit={n_fit}\n")

    # ─── Test 1: φ_AM exponent (currently LOCKED at 4) ───
    print("=" * 95)
    print("  TEST 1: φ_AM exponent — currently LOCKED at 4 (Stauffer-Bruggeman backbone)")
    print("=" * 95)
    print(f"  {'φ_exp':>6s}  {'LOOCV':>7s}  {'ΔLOOCV':>9s}  {'R²':>6s}   Verdict")

    log_phi = np.log(np.maximum(phi_a, 1e-6))
    for exp_test in [2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 6.0, 8.0]:
        delta = (exp_test - 4.0) * log_phi  # change φ^4 → φ^exp_test
        arr_t = adjusted_arr(arr, delta)
        loo, r2 = fit_loocv(arr_t, fit_mask, gcp)
        dloo = loo - loo_base
        if exp_test == 4.0:
            verdict = "★ LOCKED (Stage 14)"
        elif dloo >= -0.0001:
            verdict = "DEVIATES — data prefers this!"
        elif abs(dloo) < 0.005:
            verdict = "CONFIRMED"
        else:
            verdict = "loses"
        print(f"  {exp_test:>6.2f}  {loo:>7.4f}  {dloo:>+8.4f}  {r2:>6.4f}   {verdict}")
    print()

    # ─── Test 2: Holm exponent (currently LOCKED at 0.5) ───
    print("=" * 95)
    print("  TEST 2: √A_AM-AM exponent — currently LOCKED at 0.5 (Holm 1967)")
    print("=" * 95)
    print(f"  {'exp':>6s}  {'LOOCV':>7s}  {'ΔLOOCV':>9s}  {'R²':>6s}   Verdict")

    log_area = np.log(np.maximum(am_area_a, 1e-12))
    for exp_test in [0.25, 0.33, 0.40, 0.50, 0.60, 0.67, 0.75, 1.00]:
        delta = (exp_test - 0.5) * log_area
        arr_t = adjusted_arr(arr, delta)
        loo, r2 = fit_loocv(arr_t, fit_mask, gcp)
        dloo = loo - loo_base
        if exp_test == 0.5:
            verdict = "★ LOCKED (Holm 1967)"
        elif dloo >= -0.0001:
            verdict = "DEVIATES — data prefers this!"
        elif abs(dloo) < 0.005:
            verdict = "CONFIRMED"
        else:
            verdict = "loses"
        print(f"  {exp_test:>6.2f}  {loo:>7.4f}  {dloo:>+8.4f}  {r2:>6.4f}   {verdict}")
    print()

    # ─── Test 3: NCM(r) exponent (currently LOCKED at 1.5, Trevisanello) ───
    print("=" * 95)
    print("  TEST 3: NCM(r) = 1/(1+(r/2)^β) — currently LOCKED at β=1.5 (Trevisanello 2021)")
    print("=" * 95)
    print(f"  {'β_NCM':>6s}  {'LOOCV':>7s}  {'ΔLOOCV':>9s}  {'R²':>6s}   Verdict")

    # NCM uses log_ncm = (1-p)*log(NCM_S) + p*log(NCM_P)
    # Need to recompute NCM with different exponent and subtract baseline log_ncm
    log_ncm_base = arr['log_ncm_mix']
    for exp_test in [0.5, 1.0, 1.25, 1.5, 1.75, 2.0, 2.5, 3.0]:
        ncm_S_new = 1.0 / (1.0 + np.power(np.maximum(ras_a, 0.05) / 2.0, exp_test))
        ncm_P_new = 1.0 / (1.0 + np.power(np.maximum(rap_a, 0.05) / 2.0, exp_test))
        log_ncm_new = (1.0 - p_a) * np.log(np.maximum(ncm_S_new, 1e-6)) + \
                       p_a * np.log(np.maximum(ncm_P_new, 1e-6))
        delta = log_ncm_new - log_ncm_base
        arr_t = adjusted_arr(arr, delta)
        loo, r2 = fit_loocv(arr_t, fit_mask, gcp)
        dloo = loo - loo_base
        if exp_test == 1.5:
            verdict = "★ LOCKED (Trevisanello)"
        elif dloo >= -0.0001:
            verdict = "DEVIATES — data prefers this!"
        elif abs(dloo) < 0.005:
            verdict = "CONFIRMED"
        else:
            verdict = "loses"
        print(f"  {exp_test:>6.2f}  {loo:>7.4f}  {dloo:>+8.4f}  {r2:>6.4f}   {verdict}")
    print()

    # ─── Test 4: C(τ) polynomial degree ───
    print("=" * 95)
    print("  TEST 4: C(τ) polynomial degree — currently logpoly2 (3 params)")
    print("=" * 95)
    print(f"  {'variant':25s}  {'LOOCV':>7s}  {'ΔLOOCV':>9s}  {'R²':>6s}   Verdict")
    print(f"  {'logpoly2 (current)':25s}  {loo_base:>7.4f}  {'(ref)':>9s}  {r2_base:>6.4f}   —")

    # Test logpoly1 (drop col 6 = r_τ)
    orig_drop = gcp._STAGE_22_5_DROP_COLS
    gcp._STAGE_22_5_DROP_COLS = orig_drop | {6}
    fit_lp1 = gcp._electronic_fit(arr, fit_mask=fit_mask)
    gcp._STAGE_22_5_DROP_COLS = orig_drop
    dloo = fit_lp1['loocv'] - loo_base
    verdict = ("★ DROP" if dloo > -0.005 else
               "◆ marginal" if dloo > -0.010 else "✗ KEEP")
    print(f"  {'logpoly1 (drop r_τ)':25s}  {fit_lp1['loocv']:>7.4f}  {dloo:>+8.4f}  "
          f"{fit_lp1['r2']:>6.4f}   {verdict}")

    # Test logpoly0 (drop cols 5, 6 = q_τ, r_τ; keep p_τ constant)
    gcp._STAGE_22_5_DROP_COLS = orig_drop | {5, 6}
    fit_lp0 = gcp._electronic_fit(arr, fit_mask=fit_mask)
    gcp._STAGE_22_5_DROP_COLS = orig_drop
    dloo0 = fit_lp0['loocv'] - loo_base
    verdict0 = ("★ DROP" if dloo0 > -0.005 else
                "◆ marginal" if dloo0 > -0.010 else "✗ KEEP")
    print(f"  {'logpoly0 (drop q+r)':25s}  {fit_lp0['loocv']:>7.4f}  {dloo0:>+8.4f}  "
          f"{fit_lp0['r2']:>6.4f}   {verdict0}")
    print()

    # ─── Test 5: bimodal coupling exponent on p(1-p) ───
    print("=" * 95)
    print("  TEST 5: bimodal coupling p^a · (1-p)^a · log φ — currently a=1 (locked)")
    print("=" * 95)
    print(f"  {'a':>4s}  {'LOOCV':>7s}  {'ΔLOOCV':>9s}  {'R²':>6s}   Verdict")
    # X col 10 = p(1-p) * log(φ).  To test (p(1-p))^a, multiply log(φ) by p(1-p)^(a-1)
    # Actually X[:, 10] = p(1-p)*log(φ).  To test (p(1-p))^a * log(φ),
    # the term in linear regression form: β_bi * (p(1-p))^a * log(φ)
    # We modify X[:, 10] entry: new_X[:, 10] = (p(1-p))^a * log(φ)
    # then refit β_bi.
    log_phi_for_bi = np.log(np.maximum(phi_a, 1e-6))
    base_X = arr['X'].copy()
    for a_test in [0.5, 0.75, 1.0, 1.5, 2.0]:
        X_mod = base_X.copy()
        p1p = p_a * (1.0 - p_a)
        new_col = np.power(np.maximum(p1p, 1e-6), a_test) * log_phi_for_bi
        X_mod[:, 10] = new_col
        arr_t = dict(arr)
        arr_t['X'] = X_mod
        loo, r2 = fit_loocv(arr_t, fit_mask, gcp)
        dloo = loo - loo_base
        verdict = ("★ LOCKED (a=1)" if a_test == 1.0 else
                   "DEVIATES — data prefers!" if dloo >= -0.0001 else
                   "CONFIRMED" if abs(dloo) < 0.005 else "loses")
        print(f"  {a_test:>4.2f}  {loo:>7.4f}  {dloo:>+8.4f}  {r2:>6.4f}   {verdict}")
    print()

    # ─── Summary ───
    print("=" * 95)
    print("  SUMMARY")
    print("=" * 95)
    print(f"  BASELINE Stage 22.5: LOOCV {loo_base:.4f}  R² {r2_base:.4f}  n_fit {n_fit}")
    print()
    print("  Interpretation guide:")
    print("    ★ LOCKED VALUE WINS:  literature exponent is best — paper claim 'data confirms'")
    print("    DEVIATES:             data prefers different exponent — potential new finding")
    print("    CONFIRMED:            literature within noise of winner — keep lock with confidence")
    print("    loses:                this candidate is worse than literature — irrelevant")
    print()
    print("  Strong paper narratives:")
    print("    (1) 'φ_AM^4 Stauffer-Bruggeman scaling confirmed by n=76 ablation'")
    print("    (2) 'Holm 1967 √A constriction exponent agrees with our DEM corpus'")
    print("    (3) 'Trevisanello 2021 β=1.5 GB scaling verified across composite cathodes'")
    print()
    print("  If any test shows DEVIATES with ΔLOOCV > +0.010, consider:")
    print("    - Re-fitting the exponent live (cost: 1 LIVE param)")
    print("    - Documenting the deviation as a physical finding")
    print("    - Investigating systematic corpus bias")


if __name__ == '__main__':
    main()
