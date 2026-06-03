#!/usr/bin/env python3
"""σ_e Stage 22 — comprehensive ablation screen.

Tests removing each LIVE-fit term (β) one-by-one + key group combinations.
For each: refit on n_fit cases, compute LOOCV and family MAE.

Verdict thresholds:
  ΔLOOCV > -0.005  → UNNEEDED (safe to drop)
  -0.010 < ΔLOOCV ≤ -0.005 → marginal (case-by-case decision)
  ΔLOOCV ≤ -0.010 → NEEDED (keep in form)

Form column layout (from _electronic_form_arrays):
   0: (1-p)  → log σ_S      LOCKED
   1: p      → log σ_P      LOCKED
   2: β_T    log(T/d_AM)    geometry
   3: β_v    v_AM           vulnerability
   4: p_τ    1              C(τ) constant
   5: q_τ    log τ          C(τ) linear
   6: r_τ    (log τ)²       C(τ) quadratic
   7: β_AC   φ·log CN       network saturation
   8: β_φth  g_thin·log φ   thin-film φ
   9: β_covth g_thin·log cov thin-film cov
  10: β_bi   p(1-p)·log φ   bimodal coupling
  11: β_Fe   log f_intact   fracture Holm
  12: β_fpth g_thin·log f_p thin-film percolation
  13: β_logrSE log r_SE     SE size effect

Run:  python3 scripts/electronic_ablation_full.py
"""
from __future__ import annotations
import sys, json
from pathlib import Path
import numpy as np
from numpy.linalg import lstsq

SCRIPTS = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS))

# Term groups for ablation
TESTS = [
    # (label, cols_to_drop, category)
    ("β_T  (T/d Pouillet)",           [2],           "🔵 geometry"),
    ("β_v  (AM vulnerability)",       [3],           "🟡 correction"),
    ("C(τ) full logpoly2",            [4, 5, 6],     "🟡 tortuosity"),
    ("β_AC (φ·log CN saturation)",    [7],           "🟡 correction"),
    ("β_φth (thin·log φ)",            [8],           "🟡 thin-film"),
    ("β_covth (thin·log cov)",        [9],           "🟡 thin-film"),
    ("β_bi (bimodal p(1-p)·log φ)",   [10],          "🟡 coupling"),
    ("β_Fe (fracture log f_intact)",  [11],          "🟡 fracture"),
    ("β_fpth (thin·log f_p)",         [12],          "🟡 thin-film"),
    ("β_logrSE (r_SE size)",          [13],          "🔵 geometry"),
    # Group ablations
    ("ALL 3 thin-film (φth+covth+fpth)", [8, 9, 12], "🟡 group"),
    ("WEAK BLOCK (β_v+β_AC+β_fpth+β_logrSE)", [3, 7, 12, 13], "🟡 group"),
    # MINIMAL FORM test (drop all 9 SAFE candidates → keep only β_T + C(τ) + β_bi)
    ("MINIMAL FORM (drop 9 SAFE → keep β_T+C(τ)+β_bi)",
     [3, 7, 8, 9, 11, 12, 13],     "⭐ minimal"),
]


def main():
    import matplotlib; matplotlib.use('Agg')
    import generate_comparison_plots as gcp

    # Walk corpus
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

    arr = gcp._electronic_form_arrays(data_list, names)
    if arr is None: print("[ABORT] _electronic_form_arrays returned None"); return

    fit_mask = ~arr['excluded']
    n_fit = int(fit_mask.sum())
    logsf = arr['logsf']
    sS_log = np.log(gcp._SIGMA_S_LOCKED)
    sP_log = np.log(gcp._SIGMA_P_LOCKED)
    X_full = arr['X']
    log_off = arr['log_offset']
    log_off_f = log_off[fit_mask]
    logsf_f = logsf[fit_mask]
    Xf = X_full[fit_mask]
    y_resid_f = arr['y_resid'][fit_mask]

    # ───── Baseline (Stage 22 full) ─────
    fit = gcp._electronic_fit(arr, fit_mask=fit_mask)
    base_loo = fit['loocv']; base_r2 = fit['r2']
    sig_act = arr['sig_act']
    pred_base = np.exp(fit['pred_log'])
    err_base = (pred_base - sig_act) / sig_act * 100
    med_base = float(np.median(np.abs(err_base[fit_mask])))

    print("=" * 105)
    print(f"  σ_e Stage 22 — FULL ABLATION SCREEN  (corpus n={arr['n']}, fit n_fit={n_fit})")
    print("=" * 105)
    print(f"  BASELINE (Stage 22 full form, 12 LIVE OLS):")
    print(f"    LOOCV = {base_loo:.4f}    R² = {base_r2:.4f}    median |err| = {med_base:.1f}%")
    print(f"    σ_S = {gcp._SIGMA_S_LOCKED:.1f} LOCKED,  σ_P = {gcp._SIGMA_P_LOCKED:.1f} LOCKED")
    print(f"    n/k ratio (full form) = {n_fit}/12 = {n_fit/12:.1f}:1")
    print()

    # ───── Per-test ablation ─────
    def fit_drop(cols_to_drop):
        """Drop specified cols (always lock 0,1) → refit, return (loo, r2, med_err)."""
        keep_cols = [j for j in range(X_full.shape[1]) if j not in cols_to_drop]
        Xf_drop = X_full[fit_mask][:, keep_cols]
        # locked-endpoints fit (cols 0,1 still present in keep_cols since drops are 2+)
        y_adj = y_resid_f - Xf_drop[:, 0]*sS_log - Xf_drop[:, 1]*sP_log
        c_other, *_ = lstsq(Xf_drop[:, 2:], y_adj, rcond=None)
        coef_drop = np.concatenate([[sS_log, sP_log], c_other])
        # LOOCV
        ss_tot = float(np.sum((logsf_f - logsf_f.mean())**2))
        sse = 0.0
        for j in range(len(logsf_f)):
            m = np.ones(len(logsf_f), bool); m[j] = False
            y_adj_loo = y_resid_f[m] - Xf_drop[m, 0]*sS_log - Xf_drop[m, 1]*sP_log
            c_other_loo, *_ = lstsq(Xf_drop[m][:, 2:], y_adj_loo, rcond=None)
            c_loo = np.concatenate([[sS_log, sP_log], c_other_loo])
            sse += (logsf_f[j] - (Xf_drop[j] @ c_loo + log_off_f[j]))**2
        loo_drop = 1 - sse/ss_tot if ss_tot > 0 else 0
        # R² (in-sample fit)
        pred_log = Xf_drop @ coef_drop + log_off_f
        sse_fit = float(np.sum((logsf_f - pred_log)**2))
        r2 = 1 - sse_fit/ss_tot if ss_tot > 0 else 0
        # median err
        pred_full = X_full[:, keep_cols] @ coef_drop + log_off
        err = (np.exp(pred_full) - sig_act) / sig_act * 100
        med = float(np.median(np.abs(err[fit_mask])))
        return loo_drop, r2, med

    # ───── Run all tests ─────
    print("─" * 105)
    print(f"  {'Test':45s} {'cat':>14s}   {'LOOCV':>7s}  {'ΔLOOCV':>9s}  {'R²':>6s}  {'med|e|':>7s}  Verdict")
    print(f"  {'BASELINE':45s} {'(full)':>14s}   {base_loo:>7.4f}  {'(ref)':>9s}  {base_r2:>6.4f}  {med_base:>6.1f}%   —")
    print("─" * 105)

    results = []
    for label, drops, cat in TESTS:
        loo, r2, med = fit_drop(drops)
        dloo = loo - base_loo
        if dloo > -0.005:
            verdict = "★ DROP — safe"
        elif dloo > -0.010:
            verdict = "◆ marginal"
        else:
            verdict = "✗ KEEP — needed"
        results.append((label, cat, loo, dloo, r2, med, verdict))
        print(f"  {label:45s} {cat:>14s}   {loo:>7.4f}  {dloo:>+8.4f}  {r2:>6.4f}  {med:>6.1f}%   {verdict}")
    print()

    # ───── Summary ─────
    print("=" * 105)
    print("  SUMMARY")
    print("=" * 105)
    safe_drops  = [r for r in results if r[3] > -0.005]
    marginals   = [r for r in results if -0.010 < r[3] <= -0.005]
    needed      = [r for r in results if r[3] <= -0.010]
    print(f"  ★ SAFE to DROP        ({len(safe_drops):>2d}): {', '.join(r[0].split('(')[0].strip() for r in safe_drops) or '— none —'}")
    print(f"  ◆ MARGINAL (caution)  ({len(marginals):>2d}): {', '.join(r[0].split('(')[0].strip() for r in marginals) or '— none —'}")
    print(f"  ✗ NEEDED — keep        ({len(needed):>2d}): {', '.join(r[0].split('(')[0].strip() for r in needed) or '— none —'}")
    print()
    if safe_drops:
        n_save = sum(len(t[1]) for t in TESTS for r in safe_drops if r[0] == t[0])
        n_new = 12 - n_save
        if n_new > 0:
            print(f"  Potential simplification: drop {n_save} params → {n_new}-param form, n/k = {n_fit}/{n_new} = {n_fit/n_new:.1f}:1")
    print()
    print(f"  THRESHOLDS: ΔLOOCV > -0.005 → UNNEEDED  |  -0.010 < ΔLOOCV ≤ -0.005 → marginal  |  ΔLOOCV ≤ -0.010 → NEEDED")


if __name__ == '__main__':
    main()
