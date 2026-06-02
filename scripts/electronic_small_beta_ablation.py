#!/usr/bin/env python3
"""σ_e Stage 22 — small-β term ablation test.

User question: β_T (Pouillet thickness) and β_rSE (SE size direct) are
labeled "약함 (small)" — do we actually need them?

Tests:
  1. BASELINE (Stage 22 full)
  2. − (T/d)^β_T term removed
  3. − r_SE^β_rSE term removed
  4. − both removed

For each: refit on n_fit cases, compute LOOCV and family MAE.
Verdict: term is necessary if removal degrades LOOCV by >0.005
(production threshold for "term contributes signal").

Run on WSL:
    python3 scripts/electronic_small_beta_ablation.py
"""
from __future__ import annotations
import sys, json
from pathlib import Path
import numpy as np
from numpy.linalg import lstsq

SCRIPTS = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS))


def loo_r2_logsf(X_, log_offset_, logsf_, lock_endpoints=True,
                 sS_log=None, sP_log=None):
    n_ = len(logsf_)
    if n_ < X_.shape[1] + 2: return float('nan')
    ss_tot = float(np.sum((logsf_ - logsf_.mean())**2))
    if ss_tot <= 0: return 0.0
    y_resid = logsf_ - log_offset_
    sse = 0.0
    for j in range(n_):
        m = np.ones(n_, bool); m[j] = False
        if lock_endpoints and sS_log is not None:
            y_adj = y_resid[m] - X_[m, 0]*sS_log - X_[m, 1]*sP_log
            # Find cols to fit (exclude 0,1)
            c_other, *_ = lstsq(X_[m][:, 2:], y_adj, rcond=None)
            c = np.concatenate([[sS_log, sP_log], c_other])
        else:
            c, *_ = lstsq(X_[m], y_resid[m], rcond=None)
        sse += (logsf_[j] - (X_[j] @ c + log_offset_[j]))**2
    return 1 - sse/ss_tot


def main():
    import matplotlib; matplotlib.use('Agg')
    import generate_comparison_plots as gcp

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
    if arr is None: print("[ABORT]"); return
    fit_mask = ~arr['excluded']
    logsf = arr['logsf']
    sS_log = np.log(gcp._SIGMA_S_LOCKED)
    sP_log = np.log(gcp._SIGMA_P_LOCKED)

    # Columns layout (Stage 22):
    #  0: (1-p) coef → log σ_S (LOCKED)
    #  1: p coef → log σ_P (LOCKED)
    #  2: β_T  (log T/d)        ← test removal
    #  3: β_v
    #  4: p_τ
    #  5: q_τ
    #  6: r_τ
    #  7: β_AC
    #  8: β_φth
    #  9: β_covth
    # 10: β_bi
    # 11: β_Fe
    # 12: β_fpth
    # 13: β_logrSE             ← test removal

    X_full = arr['X']
    log_off = arr['log_offset']
    log_off_f = log_off[fit_mask]
    logsf_f = logsf[fit_mask]
    Xf = X_full[fit_mask]

    # ───── Baseline (Stage 22 full) ─────
    fit = gcp._electronic_fit(arr, fit_mask=fit_mask)
    base_loo = fit['loocv']; base_r2 = fit['r2']
    sig_act = arr['sig_act']
    pred_base = np.exp(fit['pred_log'])
    err_base = (pred_base - sig_act) / sig_act * 100

    print("=" * 95)
    print(f" Stage 22 small-β ablation  (n_fit={fit['n_fit']})")
    print("=" * 95)
    print(f"  BASELINE (full form, 12 live OLS):")
    print(f"    LOOCV = {base_loo:.4f}   R² = {base_r2:.4f}")
    print(f"    β_T   = {fit['coef'][2]:+.4f}  (T/d_AM)^β_T")
    print(f"    β_rSE = {fit['coef'][13]:+.4f}  r_SE^β_rSE")
    print()

    # ───── Remove single term ─────
    def fit_drop(cols_to_drop, label):
        """Fit with specified col indices dropped (lock 0,1 always)."""
        keep_cols = [j for j in range(X_full.shape[1]) if j not in cols_to_drop]
        X_drop = X_full[:, keep_cols]
        Xf_drop = X_drop[fit_mask]
        # Locked endpoints: cols 0,1 of original → still cols 0,1 in keep_cols
        # (since we only drop non-endpoint cols)
        y_resid_f = arr['y_resid'][fit_mask]
        # Locked fit
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
        # R²
        pred_log = Xf_drop @ coef_drop + log_off_f
        sse_fit = float(np.sum((logsf_f - pred_log)**2))
        r2 = 1 - sse_fit/ss_tot if ss_tot > 0 else 0
        # Per-case err
        pred_full = X_drop @ coef_drop + log_off
        err = (np.exp(pred_full) - sig_act) / sig_act * 100
        return loo_drop, r2, coef_drop, err

    tests = [
        ("(A) DROP (T/d)^β_T only", [2]),
        ("(B) DROP r_SE^β_rSE only", [13]),
        ("(C) DROP BOTH small-β", [2, 13]),
    ]

    print("─" * 95)
    print(f"  {'Test':32s} {'LOOCV':>8s}  {'ΔLOOCV':>9s}  {'R²':>7s}  {'med|err|':>9s}  Verdict")
    print(f"  {'BASELINE (full)':32s} {base_loo:>8.4f}  {'(ref)':>9s}  {base_r2:>7.4f}  "
          f"{float(np.median(np.abs(err_base[fit_mask]))):>8.1f}%   —")

    for label, drops in tests:
        loo, r2, coef, err = fit_drop(drops, label)
        dloo = loo - base_loo
        med = float(np.median(np.abs(err[fit_mask])))
        if dloo > -0.005:
            verdict = "★ UNNEEDED — drop"
        elif dloo > -0.010:
            verdict = "◆ marginal — borderline"
        else:
            verdict = "✗ NEEDED — keep"
        print(f"  {label:32s} {loo:>8.4f}  {dloo:>+8.4f}  {r2:>7.4f}  {med:>8.1f}%   {verdict}")
    print()

    # ───── Per-family MAE breakdown ─────
    print("─" * 95)
    print(" Per-family MAE comparison")
    print("─" * 95)
    def fam_mask(test): return np.array([test(nm) for nm in arr['names']])
    families = [
        ('1mAh',        fam_mask(lambda nm: '1mAh' in nm and '_real' not in nm)),
        ('2mAh_real',   fam_mask(lambda nm: '2mAh' in nm)),
        ('6mAh_real',   fam_mask(lambda nm: '6mAh' in nm)),
        ('8mAh',        fam_mask(lambda nm: '8mAh' in nm)),
        ('particulate', fam_mask(lambda nm: 'particulate' in nm or nm[:8] == 'input_S_')),
    ]

    err_versions = [('BASE', err_base)]
    for label, drops in tests:
        _, _, _, err = fit_drop(drops, label)
        err_versions.append((label.split()[0], err))

    print(f"  {'family':12s}  {'n':>3s}  " + "  ".join(f"{l:>10s}" for l, _ in err_versions))
    for fam_label, m in families:
        mf = m & fit_mask
        if mf.sum() == 0: continue
        row = f"  {fam_label:12s}  {int(mf.sum()):>3d}  "
        row += "  ".join(f"{float(np.mean(np.abs(e[mf]))):>9.1f}%" for _, e in err_versions)
        print(row)
    print()

    # ───── Verdict ─────
    print("=" * 95)
    print(" VERDICT")
    print("=" * 95)
    print(f"  Threshold: ΔLOOCV > -0.005 → UNNEEDED")
    print(f"  Threshold: -0.010 < ΔLOOCV ≤ -0.005 → marginal")
    print(f"  Threshold: ΔLOOCV ≤ -0.010 → NEEDED, keep in form")


if __name__ == '__main__':
    main()
