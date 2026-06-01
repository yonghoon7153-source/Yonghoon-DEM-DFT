#!/usr/bin/env python3
"""σ_electronic Stage 21 — 1mAh panel shape mismatch focused fix.

User feedback (2026-06-01): "0.97 인거 치고 너무 안맞는데" + "일단 개형이랑
맞아야지" → LOOCV 우선보다 shape match 가 우선.

Visible shape misses in 1mAh per-config plot:
  • 1mAh_75:25 (3:7, 5:5, 7:3): data 7.2, 7.2, 5.4 (flat then drop)
                                 form 7.3, 5.6, 5.6 (DIP at 5:5)
  • 1mAh_80:20 (0:10, 3:7, 5:5, 7:3): data 8.3, 8.0, 8.2, 6.2 (mostly flat then drop)
                                       form 8.5, 9.8, 7.7, 6.7 (PEAK at 3:7)
  • 1mAh_100_80:20 (4× 10:0): data 4.3, 6.6, 5.5, 5.3 (spread)
                              form ~4.4 flat (form treats them identical)
  • 1mAh_85:15 panel: PI band 일부 missing (numerical issue?)

This script:
  1. Print Stage 21 LOOCV/R² + coefs (sanity check)
  2. For EACH 1mAh case: dump σ_act, σ_form, and PER-FACTOR contribution
     (σ_mix, φ⁴, NCM_mix, √A, (T/d)^βT, r_SE^β, exp terms, bimodal, fracture, C(τ))
     → see WHICH factor causes the shape mismatch
  3. Check PI band lo/hi for ALL 1mAh cases — identify missing-band cases
  4. Test 4 SHAPE-targeted form modifications:
       M1  arithmetic mix     σ_S·(1-p) + σ_P·p instead of σ_S^(1-p)·σ_P^p
       M2  + asymm bimodal    β_p2·p²·logφ + β_1mp2·(1-p)²·logφ (2 new terms)
       M3  + p·log r_AM_eff   composition × particle size coupling
       M4  drop bimodal       remove β_bi · p(1-p) · logφ (test redundancy)
  5. PER-PANEL MAE comparison (1mAh_75:25, 1mAh_80:20, 1mAh_85:15)
     for BASELINE + each M1-M4

Run on WSL:
    python3 scripts/electronic_1mAh_shape_fix.py 2>&1 | tee /tmp/e_1mah.log
"""
from __future__ import annotations
import sys, json
from pathlib import Path
import numpy as np
from numpy.linalg import lstsq

SCRIPTS = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS))


def loo_r2(X_, y_):
    n_ = len(y_)
    if n_ < X_.shape[1] + 2: return float('nan')
    ss = float(np.sum((y_ - y_.mean())**2))
    if ss <= 0: return 0.0
    sse = 0.0
    for j in range(n_):
        m = np.ones(n_, bool); m[j] = False
        c, *_ = lstsq(X_[m], y_[m], rcond=None)
        sse += (y_[j] - X_[j] @ c)**2
    return 1 - sse/ss


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
    coef = fit['coef']
    sig_act = arr['sig_act']; sig_pred = np.exp(fit['pred_log'])
    err_pct = (sig_pred - sig_act) / sig_act * 100.0
    resid_log = arr['logsf'] - fit['pred_log']
    n = arr['n']; nfit = fit['n_fit']; nms = arr['names']

    print("=" * 110)
    print(f" Stage 21 BASELINE  n={n}  n_fit={nfit}  R²={fit['r2']:.4f}  LOOCV={fit['loocv']:.4f}")
    print("=" * 110)
    print(f"  σ_S={float(np.exp(coef[0])):.3f}  σ_P={float(np.exp(coef[1])):.3f}  ratio={float(np.exp(coef[0])/np.exp(coef[1])):.2f}×")
    for i, lbl in enumerate(['β_T', 'β_v', 'p_τ', 'q_τ', 'r_τ', 'β_AC',
                              'β_φth', 'β_covth', 'β_bi', 'β_Fe',
                              'β_fpth', 'β_logrSE']):
        print(f"  coef[{i+2}] {lbl:10s} = {coef[i+2]:+.4f}")
    print()

    # ───── 1mAh cases per-factor decomposition ─────
    print("=" * 110)
    print(" 1mAh family per-factor decomposition (find which factor drives shape mismatch)")
    print("=" * 110)
    mask_1mah = np.array(['1mAh' in nm for nm in nms])
    idxs_1mah = np.where(mask_1mah)[0]
    print(f"  Found {len(idxs_1mah)} 1mAh cases\n")

    # Pre-compute per-factor terms (matching _electronic_form_arrays layout)
    p_a = arr['p_amp']; phi_a = arr['phi']; r_eff_a = arr['r_eff']
    T_a = arr['T']; ras = arr['r_AM_S']; rap = arr['r_AM_P']
    sS = float(np.exp(coef[0])); sP = float(np.exp(coef[1]))

    # σ_mix (geometric)
    log_mix = (1 - p_a) * coef[0] + p_a * coef[1]
    sigma_mix = np.exp(log_mix)
    # φ⁴
    log_phi4 = 4.0 * np.log(np.maximum(phi_a, 0.01))
    # NCM_S^(1-p) NCM_P^p
    ncm_S = 1.0 / (1.0 + (np.maximum(ras, 0.05)/2.0)**1.5)
    ncm_P = 1.0 / (1.0 + (np.maximum(rap, 0.05)/2.0)**1.5)
    log_ncm = (1-p_a)*np.log(np.maximum(ncm_S, 1e-6)) + p_a*np.log(np.maximum(ncm_P, 1e-6))
    # √A (already in log_offset)
    log_holm = arr['log_offset'] - log_ncm - log_phi4
    # exp terms (β_T·log(T/d), β_v·v, β_AC·φlogCN, g_thin·..., β_bi·..., β_Fe·..., β_logrSE·...)
    log_Td = arr['X'][:, 2] * coef[2]
    log_v = arr['X'][:, 3] * coef[3]
    log_Ct = arr['X'][:, 4]*coef[4] + arr['X'][:, 5]*coef[5] + arr['X'][:, 6]*coef[6]
    log_AC = arr['X'][:, 7] * coef[7]
    log_phith = arr['X'][:, 8] * coef[8]
    log_covth = arr['X'][:, 9] * coef[9]
    log_bi = arr['X'][:, 10] * coef[10]
    log_Fe = arr['X'][:, 11] * coef[11]
    log_fpth = arr['X'][:, 12] * coef[12]
    log_logrSE = arr['X'][:, 13] * coef[13]

    print(f"  {'name':28s}  {'σ_act':>6s}  {'σ_form':>6s}  {'err%':>6s}  "
          f"{'σ_mix':>6s}  {'φ⁴':>5s}  {'NCM':>5s}  {'√A':>5s}  "
          f"{'T/d':>6s}  {'r_SE':>6s}  {'AC':>6s}  {'φth':>6s}  {'bi':>6s}  {'C(τ)':>6s}")
    for i in idxs_1mah:
        nm = nms[i]
        if 'AMP' in nm or 'AMS' in nm or '_S' in nm[-3:]: continue  # skip variants for compactness
        ex = "EX" if arr['excluded'][i] else ""
        # Factor contributions (multiplicative, shown as exp of log component)
        fphi4 = float(np.exp(log_phi4[i]))
        fncm = float(np.exp(log_ncm[i]))
        fholm = float(np.exp(log_holm[i]))
        fTd = float(np.exp(log_Td[i]))
        frSE = float(np.exp(log_logrSE[i]))
        fAC = float(np.exp(log_AC[i]))
        fphith = float(np.exp(log_phith[i] + log_covth[i] + log_fpth[i]))
        fbi = float(np.exp(log_bi[i]))
        fCt = float(np.exp(log_Ct[i]))
        print(f"  {nm[:28]:28s}  {sig_act[i]:>6.2f}  {sig_pred[i]:>6.2f}  "
              f"{err_pct[i]:>+5.1f}%  {sigma_mix[i]:>6.2f}  {fphi4:>5.3f}  "
              f"{fncm:>5.3f}  {fholm:>5.2f}  {fTd:>6.3f}  {frSE:>6.3f}  "
              f"{fAC:>6.3f}  {fphith:>6.3f}  {fbi:>6.3f}  {fCt:>6.3f}  {ex}")
    print()

    # ───── PI band check for all 1mAh cases ─────
    print("=" * 110)
    print(" 1mAh PI band check (find missing-band cases)")
    print("=" * 110)
    band = gcp._electronic_pred_band(arr, ci=0.68)
    if band is None:
        print("  Bootstrap unavailable")
    else:
        pred_med, pred_lo, pred_hi = band
        for i in idxs_1mah:
            nm = nms[i]
            if 'AMP' in nm or 'AMS' in nm or '_S' in nm[-3:]: continue
            lo, hi = pred_lo[i], pred_hi[i]
            ok = "✓" if (np.isfinite(lo) and np.isfinite(hi) and (hi-lo) > 0.01) else "✗ MISSING/TINY"
            ratio_hi = hi / sig_pred[i] if sig_pred[i] > 0 else 0
            ratio_lo = lo / sig_pred[i] if sig_pred[i] > 0 else 0
            print(f"  {nm[:35]:35s}  pred={sig_pred[i]:>6.2f}  lo={lo:>6.2f}  hi={hi:>6.2f}  "
                  f"band_ratio=[{ratio_lo:.2f}, {ratio_hi:.2f}]  {ok}")
    print()

    # ───── Per-panel grouping (heuristic by case name patterns) ─────
    def panel_mask(test):
        return np.array([test(nm) for nm in nms])

    panels = [
        ('1mAh_75:25', panel_mask(lambda nm: '1mAh' in nm and ('_2'==nm[-2:] or '_3'==nm[-2:] or '_4'==nm[-2:]))),
        ('1mAh_80:20', panel_mask(lambda nm: '1mAh' in nm and (nm.endswith('_5') or nm.endswith('_6') or nm.endswith('_7') or nm.endswith('_8') or nm.endswith('_9')))),
        ('1mAh_85:15', panel_mask(lambda nm: '1mAh' in nm and ('_5'==nm[-2:] or '_6'==nm[-2:]))),
        ('1mAh_100',   panel_mask(lambda nm: '1mAh_100' in nm)),
    ]

    # ───── Test form modifications ─────
    print("=" * 110)
    print(" Test 4 form modifications (refit, report per-panel MAE)")
    print("=" * 110)
    X = arr['X']; y_full = arr['logsf']; log_off = arr['log_offset']

    # BASELINE: existing Stage 21 form
    Xf = X[fit_mask]; yf = arr['y_resid'][fit_mask]
    c_base, *_ = lstsq(Xf, yf, rcond=None)
    pred_base = X @ c_base + log_off
    err_base = (np.exp(pred_base) - sig_act) / sig_act * 100.0

    # M1: ARITHMETIC mix replaces geometric (σ_S(1-p) + σ_P·p)
    # To test: replace columns 0,1 (which are (1-p), p with log σ in log space)
    # with a single column = log(σ_S·(1-p) + σ_P·p) — but this is nonlinear.
    # Approximation: fit β_a · (1-p) + β_b · p as is (no change in algebra,
    # but interpret as linear-in-log).  Actually for true arithmetic we'd
    # need iterative fit.  SKIP for clarity; do M2-M4.

    # Build candidates as added columns
    log_phi = np.log(np.maximum(phi_a, 0.01))
    log_reff = np.log(np.maximum(r_eff_a, 0.1))
    cands = {
        'M2  + asymm bimodal (p²·logφ + (1-p)²·logφ)':
            np.column_stack([p_a**2 * log_phi, (1-p_a)**2 * log_phi]),
        'M3  + p · log r_AM_eff (comp × size coupling)':
            np.column_stack([p_a * log_reff]),
        'M4  DROP bimodal β_bi (set col[10]=0, no refit of others)':
            None,   # special handling
        'M5  asymm bimodal ONLY (replace β_bi with p²,( 1-p)²)':
            None,   # special: remove col[10] and add 2
        'M6  + (φ-0.45)² (curvature term)':
            np.column_stack([(phi_a - 0.45)**2]),
    }

    print(f"  {'modification':50s}  {'LOOCV':>7s}  {'ΔLOOCV':>7s}  "
          f"{'1mAh_75:25':>10s}  {'1mAh_80:20':>10s}  {'1mAh_85:15':>10s}  {'1mAh_100':>9s}")

    def per_panel_mae(err_arr):
        out = {}
        for label, mask_p in panels:
            m = mask_p & fit_mask
            if m.sum() == 0: out[label] = float('nan'); continue
            out[label] = float(np.mean(np.abs(err_arr[m])))
        return out

    base_mae = per_panel_mae(err_base)
    print(f"  {'BASELINE Stage 21':50s}  {fit['loocv']:>7.4f}  {'-':>7s}  "
          f"{base_mae['1mAh_75:25']:>9.1f}%  {base_mae['1mAh_80:20']:>9.1f}%  "
          f"{base_mae['1mAh_85:15']:>9.1f}%  {base_mae['1mAh_100']:>8.1f}%")

    for label, new_cols in cands.items():
        if 'M4' in label:
            # Drop bimodal: zero out col[10] in pred (refit other coefs without that col)
            keep_cols = [j for j in range(X.shape[1]) if j != 10]
            X_mod = X[:, keep_cols]
            Xf_mod = X_mod[fit_mask]
            c, *_ = lstsq(Xf_mod, arr['y_resid'][fit_mask], rcond=None)
            pred = X_mod @ c + log_off
        elif 'M5' in label:
            # Replace col[10] with 2 new cols (p², (1-p)²) × log φ
            keep_cols = [j for j in range(X.shape[1]) if j != 10]
            X_mod = np.column_stack([X[:, keep_cols], p_a**2 * log_phi, (1-p_a)**2 * log_phi])
            Xf_mod = X_mod[fit_mask]
            c, *_ = lstsq(Xf_mod, arr['y_resid'][fit_mask], rcond=None)
            pred = X_mod @ c + log_off
        else:
            X_mod = np.column_stack([X, new_cols])
            Xf_mod = X_mod[fit_mask]
            c, *_ = lstsq(Xf_mod, arr['y_resid'][fit_mask], rcond=None)
            pred = X_mod @ c + log_off
        err_mod = (np.exp(pred) - sig_act) / sig_act * 100.0
        loo = loo_r2(Xf_mod, arr['y_resid'][fit_mask])
        d_loo = loo - fit['loocv']
        m_mae = per_panel_mae(err_mod)
        # Compute Δ from baseline per panel
        d75 = m_mae['1mAh_75:25'] - base_mae['1mAh_75:25']
        d80 = m_mae['1mAh_80:20'] - base_mae['1mAh_80:20']
        d85 = m_mae['1mAh_85:15'] - base_mae['1mAh_85:15']
        d100 = m_mae['1mAh_100'] - base_mae['1mAh_100']
        flag = ""
        if d_loo > 0 and (d75 < -2 or d80 < -2 or d100 < -2): flag = "  ★ shape-fix"
        elif d_loo > 0: flag = "  ◆ improves"
        elif d_loo < -0.005: flag = "  ✗ degrades"
        print(f"  {label:50s}  {loo:>7.4f}  {d_loo:>+7.4f}  "
              f"{m_mae['1mAh_75:25']:>5.1f}%(Δ{d75:+.1f})  "
              f"{m_mae['1mAh_80:20']:>5.1f}%(Δ{d80:+.1f})  "
              f"{m_mae['1mAh_85:15']:>5.1f}%(Δ{d85:+.1f})  "
              f"{m_mae['1mAh_100']:>5.1f}%(Δ{d100:+.1f}){flag}")
    print()

    # ───── Verdict ─────
    print("=" * 110)
    print(" VERDICT")
    print("=" * 110)
    print("  Look for modification that REDUCES at least one panel MAE by >2 pp")
    print("  AND doesn't degrade LOOCV by more than 0.005.")
    print("  If found → propose as Stage 22.  If not → 1mAh shape is intrinsic")
    print("  to data variance at this design diversity (different seeds, slight")
    print("  microstructure variations at same nominal design).")


if __name__ == '__main__':
    main()
