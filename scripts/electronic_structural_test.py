#!/usr/bin/env python3
"""σ_electronic Stage 21 — STRUCTURAL form test.

User reports persistent shape mismatch despite Stage 21 LOOCV 0.957.
Hypothesis: geometric mix σ_S^(1-p)·σ_P^p is too convex → mid-composition
DIP naturally; β_bi · p(1-p) partial compensation insufficient.

Test 4 STRUCTURAL alternatives:
  B1  ARITHMETIC mix:   σ_S·(1-p) + σ_P·p  (linear, less convex)
  B2  PER-CAPACITY σ_S/σ_P (4 extra params: 1mAh/2mAh/6mAh/8mAh shifts)
  B3  arithmetic + drop bimodal (test if bimodal becomes redundant)
  B4  ARITHMETIC mix + ASYMMETRIC bimodal (best of both)

Reports global LOOCV + per-design-family MAE
(1mAh / 2mAh / 6mAh_real / 8mAh / particulate).

Run on WSL:
    python3 scripts/electronic_structural_test.py 2>&1 | tee /tmp/e_struct.log
"""
from __future__ import annotations
import sys, json
from pathlib import Path
import numpy as np
from numpy.linalg import lstsq

SCRIPTS = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS))


def loo_r2_logsf(X_, y_resid_, log_offset_, logsf_):
    """LOOCV in LOGSF scale (matches production _electronic_fit)."""
    n_ = len(y_resid_)
    if n_ < X_.shape[1] + 2: return float('nan')
    ss_tot = float(np.sum((logsf_ - logsf_.mean())**2))
    if ss_tot <= 0: return 0.0
    sse = 0.0
    for j in range(n_):
        m = np.ones(n_, bool); m[j] = False
        c, *_ = lstsq(X_[m], y_resid_[m], rcond=None)
        # Error in logsf scale = logsf - (X·c + log_offset)
        sse += (logsf_[j] - (X_[j] @ c + log_offset_[j]))**2
    return 1 - sse/ss_tot


def main():
    import matplotlib; matplotlib.use('Agg')
    import generate_comparison_plots as gcp

    # ───── Walk corpus ─────
    data_list, names = [], []
    seen = set()
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
                except Exception: pass
            if nm == cid and not nm.startswith('input_'): continue
            if nm in seen: continue
            seen.add(nm)
            try: d = json.load(open(mp))
            except Exception: continue
            data_list.append(d); names.append(nm)

    arr = gcp._electronic_form_arrays(data_list, names)
    if arr is None: print("[ABORT] corpus too small"); return
    fit_mask = ~arr['excluded']
    fit = gcp._electronic_fit(arr, fit_mask=fit_mask)
    n = arr['n']; nfit = fit['n_fit']; nms = arr['names']
    sig_act = arr['sig_act']; logsf = arr['logsf']
    log_off = arr['log_offset']
    p_a = arr['p_amp']

    print("=" * 110)
    print(f" Stage 21 BASELINE  n={n}  n_fit={nfit}  LOOCV={fit['loocv']:.4f}  R²={fit['r2']:.4f}")
    print("=" * 110)
    print(f"  σ_S={float(np.exp(fit['coef'][0])):.3f}  σ_P={float(np.exp(fit['coef'][1])):.3f}")
    sig_pred_base = np.exp(fit['pred_log'])
    err_base = (sig_pred_base - sig_act) / sig_act * 100

    # Family masks
    def fam_mask(test): return np.array([test(nm) for nm in nms])
    families = [
        ('1mAh',         fam_mask(lambda nm: '1mAh' in nm and '_real' not in nm)),
        ('2mAh_real',    fam_mask(lambda nm: '2mAh' in nm)),
        ('6mAh_real',    fam_mask(lambda nm: '6mAh' in nm)),
        ('8mAh (all)',   fam_mask(lambda nm: '8mAh' in nm)),
        ('particulate',  fam_mask(lambda nm: 'particulate' in nm or '_S_' in nm)),
    ]

    def per_fam_mae(err_arr):
        out = {}
        for label, m in families:
            mf = m & fit_mask
            if mf.sum() == 0: out[label] = (0, float('nan')); continue
            out[label] = (int(mf.sum()), float(np.mean(np.abs(err_arr[mf]))))
        return out

    base_mae = per_fam_mae(err_base)
    print(f"  Baseline per-family MAE:")
    for lab, m in families:
        n_, m_ = base_mae[lab]
        print(f"    {lab:15s}  n={n_:>3d}  MAE={m_:>5.1f}%")
    print()

    # Build Stage 21 X but with structural changes
    X_base = arr['X']  # 14 cols
    y_resid = arr['y_resid']

    # For B1/B4: arithmetic mix.  Replace cols 0,1 (linear-in-log σ) with
    # a NEW design where we fit σ_S and σ_P that go into ARITHMETIC mix.
    # In log-space: log(σ_S·(1-p) + σ_P·p) is nonlinear in σ_S, σ_P.
    # We use 2-step: (a) hold mix function explicit, (b) iterate.
    # Simpler: parametrize by (σ_S, σ_P) and grid-search for best pair,
    # then OLS the rest.
    def fit_arith(X_full, y_full_logsf, log_off_full, p_a_full,
                  drop_bimodal=False, asymm_bimodal=False, n_iter=12):
        """Fit form with ARITHMETIC σ_S·(1-p) + σ_P·p mix.

        Iteratively: (1) guess σ_S, σ_P, (2) compute log(arith_mix) which
        replaces cols 0,1, (3) OLS the remaining coefs, (4) re-estimate
        σ_S, σ_P by grid + 1D fit, repeat.
        """
        # Stage 21 X cols 0=(1-p), 1=p; new model: log(σ_S·(1-p)+σ_P·p)
        # We MUST treat σ_S, σ_P as nonlinear parameters.
        # Inner OLS: fit cols 2-13 (or modified) with the arith_mix offset.

        # Determine which cols to keep
        keep_cols = list(range(2, X_full.shape[1]))  # drop 0,1
        if drop_bimodal and 10 in keep_cols:
            keep_cols.remove(10)
        X_inner = X_full[:, keep_cols]
        if asymm_bimodal:
            # add p² log φ, (1-p)² log φ
            log_phi = np.log(np.maximum(arr['phi'], 0.01))
            X_inner = np.column_stack([X_inner, p_a_full**2 * log_phi,
                                       (1-p_a_full)**2 * log_phi])

        # Initial σ_S, σ_P from Stage 21 baseline
        sS_cur = float(np.exp(fit['coef'][0])); sP_cur = float(np.exp(fit['coef'][1]))

        for it in range(n_iter):
            arith = sS_cur * (1 - p_a_full) + sP_cur * p_a_full
            log_arith = np.log(np.maximum(arith, 1e-6))
            # New target = logsf - log_arith - log_offset_residual_of_other_cols
            # Effective y for OLS = logsf - log_arith - (only_phi4_NCM_holm part of log_offset)
            # Actually log_offset = log_ncm + log_holm + log_phi4 (all independent of σ_S/σ_P)
            # So new y for OLS on X_inner = logsf - log_offset - log_arith
            y_inner = y_full_logsf - log_off_full - log_arith
            # OLS
            c_inner, *_ = lstsq(X_inner, y_inner, rcond=None)
            # Compute residuals to find σ_S, σ_P update
            pred_inner = X_inner @ c_inner   # this is the "exp factor product"
            # Total prediction: log(arith_mix) + log_offset + X_inner·c
            # = logsf_pred
            # Residual w.r.t. arith mix: logsf - pred - log_offset - X_inner·c = log_arith - true_log_mix
            # We want σ_S, σ_P such that arith mix matches data after factoring out the rest
            # The "factored-out" part: implied_log_mix = logsf - log_offset - X_inner·c
            implied_log_mix = y_full_logsf - log_off_full - pred_inner
            implied_mix = np.exp(implied_log_mix)
            # Now find σ_S, σ_P that best fit arith mix = implied_mix
            # OLS: arith = σ_S·(1-p) + σ_P·p
            A = np.column_stack([1 - p_a_full, p_a_full])
            coef_mix, *_ = lstsq(A, implied_mix, rcond=None)
            sS_new = max(float(coef_mix[0]), 0.1)
            sP_new = max(float(coef_mix[1]), 0.1)
            if abs(sS_new - sS_cur) < 0.01 and abs(sP_new - sP_cur) < 0.01:
                sS_cur, sP_cur = sS_new, sP_new
                break
            sS_cur, sP_cur = sS_new, sP_new

        # Final predictions
        arith = sS_cur * (1 - p_a_full) + sP_cur * p_a_full
        log_arith = np.log(np.maximum(arith, 1e-6))
        y_inner = y_full_logsf - log_off_full - log_arith
        c_inner, *_ = lstsq(X_inner[fit_mask], y_inner[fit_mask], rcond=None)
        pred_logsf = log_arith + log_off_full + X_inner @ c_inner

        # LOOCV in logsf scale
        ss_tot = float(np.sum((y_full_logsf[fit_mask] - y_full_logsf[fit_mask].mean())**2))
        sse_loo = 0.0
        X_in_f = X_inner[fit_mask]
        y_in_f = y_inner[fit_mask]
        logsf_f = y_full_logsf[fit_mask]
        log_off_f = log_off_full[fit_mask]
        log_arith_f = log_arith[fit_mask]
        for j in range(len(y_in_f)):
            m = np.ones(len(y_in_f), bool); m[j] = False
            c_loo, *_ = lstsq(X_in_f[m], y_in_f[m], rcond=None)
            pred_j = log_arith_f[j] + log_off_f[j] + X_in_f[j] @ c_loo
            sse_loo += (logsf_f[j] - pred_j)**2
        loocv = 1 - sse_loo / ss_tot if ss_tot > 0 else 0.0
        return sS_cur, sP_cur, c_inner, np.exp(pred_logsf), loocv

    # B1: arithmetic mix
    print("=" * 110)
    print(" B1: ARITHMETIC mix (σ_S·(1-p) + σ_P·p)")
    print("=" * 110)
    sS, sP, c_in, pred_b1, loo_b1 = fit_arith(X_base, logsf, log_off, p_a)
    err_b1 = (pred_b1 - sig_act) / sig_act * 100
    print(f"  σ_S={sS:.2f}  σ_P={sP:.2f}  LOOCV={loo_b1:.4f}  ΔLOOCV={loo_b1-fit['loocv']:+.4f}")
    mae_b1 = per_fam_mae(err_b1)
    for lab, m in families:
        n_, m_ = mae_b1[lab]
        if n_ == 0: continue
        d = m_ - base_mae[lab][1]
        print(f"    {lab:15s}  MAE={m_:>5.1f}% (Δ{d:+.1f})")
    print()

    # B3: arithmetic + drop bimodal
    print("=" * 110)
    print(" B3: ARITHMETIC mix + DROP bimodal β_bi")
    print("=" * 110)
    sS, sP, c_in, pred_b3, loo_b3 = fit_arith(X_base, logsf, log_off, p_a, drop_bimodal=True)
    err_b3 = (pred_b3 - sig_act) / sig_act * 100
    print(f"  σ_S={sS:.2f}  σ_P={sP:.2f}  LOOCV={loo_b3:.4f}  ΔLOOCV={loo_b3-fit['loocv']:+.4f}")
    mae_b3 = per_fam_mae(err_b3)
    for lab, m in families:
        n_, m_ = mae_b3[lab]
        if n_ == 0: continue
        d = m_ - base_mae[lab][1]
        print(f"    {lab:15s}  MAE={m_:>5.1f}% (Δ{d:+.1f})")
    print()

    # B4: arithmetic + asymmetric bimodal
    print("=" * 110)
    print(" B4: ARITHMETIC mix + ASYMMETRIC bimodal (p²·logφ + (1-p)²·logφ replace β_bi)")
    print("=" * 110)
    sS, sP, c_in, pred_b4, loo_b4 = fit_arith(X_base, logsf, log_off, p_a,
                                              drop_bimodal=True, asymm_bimodal=True)
    err_b4 = (pred_b4 - sig_act) / sig_act * 100
    print(f"  σ_S={sS:.2f}  σ_P={sP:.2f}  LOOCV={loo_b4:.4f}  ΔLOOCV={loo_b4-fit['loocv']:+.4f}")
    mae_b4 = per_fam_mae(err_b4)
    for lab, m in families:
        n_, m_ = mae_b4[lab]
        if n_ == 0: continue
        d = m_ - base_mae[lab][1]
        print(f"    {lab:15s}  MAE={m_:>5.1f}% (Δ{d:+.1f})")
    print()

    # B2: PER-CAPACITY σ_S/σ_P (one-hot capacity offsets to σ_S)
    print("=" * 110)
    print(" B2: PER-CAPACITY σ_S shift (geometric mix kept; add 1mAh/2mAh/8mAh dummy)")
    print("=" * 110)
    is_1mAh = np.array([('1mAh' in nm and '_real' not in nm) for nm in nms]).astype(float)
    is_2mAh = np.array([('2mAh' in nm) for nm in nms]).astype(float)
    is_8mAh = np.array([('8mAh' in nm) for nm in nms]).astype(float)
    X_b2 = np.column_stack([X_base, (1-p_a)*is_1mAh, (1-p_a)*is_2mAh, (1-p_a)*is_8mAh])
    Xf_b2 = X_b2[fit_mask]; yf_b2 = y_resid[fit_mask]
    c_b2, *_ = lstsq(Xf_b2, yf_b2, rcond=None)
    pred_b2 = np.exp(X_b2 @ c_b2 + log_off)
    err_b2 = (pred_b2 - sig_act) / sig_act * 100
    # LOOCV in logsf scale
    logsf_f = logsf[fit_mask]; ss_t = float(np.sum((logsf_f - logsf_f.mean())**2))
    sse_l = 0.0
    log_off_f = log_off[fit_mask]
    for j in range(len(yf_b2)):
        m = np.ones(len(yf_b2), bool); m[j] = False
        c_l, *_ = lstsq(Xf_b2[m], yf_b2[m], rcond=None)
        sse_l += (logsf_f[j] - (Xf_b2[j] @ c_l + log_off_f[j]))**2
    loo_b2 = 1 - sse_l/ss_t if ss_t > 0 else 0
    print(f"  LOOCV={loo_b2:.4f}  ΔLOOCV={loo_b2-fit['loocv']:+.4f}")
    print(f"  capacity shifts: 1mAh={float(c_b2[-3]):+.3f}  2mAh={float(c_b2[-2]):+.3f}  8mAh={float(c_b2[-1]):+.3f}")
    mae_b2 = per_fam_mae(err_b2)
    for lab, m in families:
        n_, m_ = mae_b2[lab]
        if n_ == 0: continue
        d = m_ - base_mae[lab][1]
        print(f"    {lab:15s}  MAE={m_:>5.1f}% (Δ{d:+.1f})")
    print()

    print("=" * 110)
    print(" VERDICT")
    print("=" * 110)
    results = [
        ('Stage 21 (baseline)', fit['loocv'], base_mae),
        ('B1 arithmetic mix', loo_b1, mae_b1),
        ('B2 per-capacity shift', loo_b2, mae_b2),
        ('B3 arith + drop bimodal', loo_b3, mae_b3),
        ('B4 arith + asymm bimodal', loo_b4, mae_b4),
    ]
    print(f"  {'option':30s}  {'LOOCV':>7s}  {'1mAh':>6s}  {'2mAh':>6s}  {'6mAh':>6s}  {'8mAh':>6s}  {'partic':>6s}")
    for label, lo, m in results:
        m1 = m['1mAh'][1]; m2 = m['2mAh_real'][1]; m6 = m['6mAh_real'][1]
        m8 = m['8mAh (all)'][1]; mp = m['particulate'][1]
        print(f"  {label:30s}  {lo:>7.4f}  {m1:>5.1f}%  {m2:>5.1f}%  {m6:>5.1f}%  {m8:>5.1f}%  {mp:>5.1f}%")
    print()
    print("  If any option REDUCES family MAE by ≥3 pp AND LOOCV ≥ baseline-0.005")
    print("  → propose as Stage 22 structural rewrite.")
    print("  If not → Stage 21 is at structural ceiling, only multi-seed data path.")


if __name__ == '__main__':
    main()
