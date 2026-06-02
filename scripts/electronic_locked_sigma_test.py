#!/usr/bin/env python3
"""σ_electronic Stage 22 — lock σ_AM = 50 (Trevisanello literature reference)
and test if form STRUCTURE still matches data shape.

User insight (2026-06-02): σ_ionic uses single fixed σ_grain=3 (Cronau)
and shape matches perfectly.  σ_e fits σ_S=9.13, σ_P=4.14 LIVE — 2 free
endpoint parameters that can absorb structural form errors.  This test:

  1. LOCK σ_AM = 50 mS/cm (Trevisanello NCM811 single-crystal literature)
  2. APPLY Trevisanello NCM(r) grain-size correction:
       NCM(r) = 1 / (1 + (r/2)^1.5)
       NCM_mix = (1-p)·NCM_S + p·NCM_P  (linear, not geometric)
  3. REFIT only the multiplicative correction terms (β_T, β_v, β_AC, etc.)
  4. Compare per-panel shape MAE vs Stage 21 (live-fit σ_S/σ_P)

If Stage 22 (locked σ_AM=50) shape MATCHES BETTER than Stage 21 →
  user's hypothesis confirmed: live-fit σ_S/σ_P was masking form error.
  Adopt as Stage 22 final.

If Stage 22 shape MATCHES WORSE → live-fit σ_S/σ_P encodes real physics
  (e.g., S-end vs P-end have different effective single-crystal conductivities).
  Stage 21 is structurally correct, shape mismatches are intrinsic limit.

Run on WSL:
    python3 scripts/electronic_locked_sigma_test.py 2>&1 | tee /tmp/e_lock.log
"""
from __future__ import annotations
import sys, json
from pathlib import Path
import numpy as np
from numpy.linalg import lstsq

SCRIPTS = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS))


def loo_r2_logsf(X_, log_offset_, logsf_):
    n_ = len(logsf_)
    if n_ < X_.shape[1] + 2: return float('nan')
    ss_tot = float(np.sum((logsf_ - logsf_.mean())**2))
    if ss_tot <= 0: return 0.0
    y_resid = logsf_ - log_offset_
    sse = 0.0
    for j in range(n_):
        m = np.ones(n_, bool); m[j] = False
        c, *_ = lstsq(X_[m], y_resid[m], rcond=None)
        sse += (logsf_[j] - (X_[j] @ c + log_offset_[j]))**2
    return 1 - sse/ss_tot


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
    if arr is None: print("[ABORT]"); return
    fit_mask = ~arr['excluded']
    sig_act = arr['sig_act']; logsf = arr['logsf']
    n = arr['n']; nfit = int(fit_mask.sum()); nms = arr['names']
    p_a = arr['p_amp']; phi_a = arr['phi']
    ras = arr['r_AM_S']; rap = arr['r_AM_P']

    # Stage 21 baseline (live-fit σ_S/σ_P)
    fit21 = gcp._electronic_fit(arr, fit_mask=fit_mask)
    err21 = (np.exp(fit21['pred_log']) - sig_act) / sig_act * 100
    coef21 = fit21['coef']
    sS21 = float(np.exp(coef21[0])); sP21 = float(np.exp(coef21[1]))

    print("=" * 110)
    print(f" Stage 21 BASELINE (live-fit σ_S/σ_P)")
    print(f"   n={n} n_fit={nfit}  LOOCV={fit21['loocv']:.4f}  R²={fit21['r2']:.4f}")
    print(f"   σ_S={sS21:.2f}  σ_P={sP21:.2f}  ratio={sS21/sP21:.2f}×")
    print("=" * 110)
    print()

    # ───── Stage 22 candidates ─────
    # Common: σ_AM × NCM_mix (Trevisanello), linear mix
    SIGMA_AM_REF = 50.0  # NCM811 single-crystal (Trevisanello 2021)
    NCM_BETA = 1.5       # Trevisanello grain-boundary exponent
    GRAIN_REF = 2.0      # µm grain-size reference

    ncm_S = 1.0 / (1.0 + (np.maximum(ras, 0.05) / GRAIN_REF)**NCM_BETA)
    ncm_P = 1.0 / (1.0 + (np.maximum(rap, 0.05) / GRAIN_REF)**NCM_BETA)

    log_mix_geom = (1 - p_a)*np.log(SIGMA_AM_REF*ncm_S) + p_a*np.log(SIGMA_AM_REF*ncm_P)
    log_mix_lin = np.log(SIGMA_AM_REF * ((1-p_a)*ncm_S + p_a*ncm_P))

    # Existing form's other factors (cols 2-13 of arr['X']) — these stay,
    # but cols 0,1 (linear-in-log σ_S/σ_P parametrization) are REPLACED by
    # the fixed log_mix.
    X_keep = arr['X'][:, 2:]   # 12 cols (β_T through β_logrSE)
    log_holm_phi4_ncm = arr['log_offset']  # contains log_ncm + log_holm + log_phi4
    # WARN: log_offset already has log_ncm built in.  But that NCM uses
    # arr['r_AM_S']/r_AM_P with Trevisanello β=1.5 — same as our redefinition.
    # So log_offset's NCM = log_ncm_mix_geom.  We need to REMOVE that and
    # replace with our literature-anchored σ_AM × NCM_mix.
    log_ncm_existing = arr['log_ncm_mix']  # (1-p)·log NCM_S + p·log NCM_P (geometric)
    log_holm = np.log(np.maximum(arr['am_area'], 1e-12))*0.5
    log_phi4 = 4.0 * np.log(np.maximum(phi_a, 0.01))

    # For S22A (geometric mix with σ_AM=50):
    #   log σ = log_mix_geom + log_phi4 + log_holm + X_keep @ β_other + extras
    # offset_S22A = log_mix_geom + log_phi4 + log_holm
    offset_S22A = log_mix_geom + log_phi4 + log_holm
    y_resid_S22A = logsf - offset_S22A

    # For S22B (linear mix):
    offset_S22B = log_mix_lin + log_phi4 + log_holm
    y_resid_S22B = logsf - offset_S22B

    # Family masks (case-name heuristic)
    def fam(test): return np.array([test(nm) for nm in nms])
    families = [
        ('1mAh', fam(lambda nm: '1mAh' in nm and '_real' not in nm)),
        ('2mAh_real', fam(lambda nm: '2mAh' in nm)),
        ('6mAh_real', fam(lambda nm: '6mAh' in nm)),
        ('8mAh', fam(lambda nm: '8mAh' in nm)),
        ('particulate', fam(lambda nm: 'particulate' in nm or 'input_S_' in nm[:8])),
    ]

    def per_fam_mae(err_arr):
        out = {}
        for label, m in families:
            mf = m & fit_mask
            out[label] = (int(mf.sum()), float(np.mean(np.abs(err_arr[mf]))) if mf.sum() else float('nan'))
        return out

    base_mae = per_fam_mae(err21)
    print(f"  Stage 21 per-family MAE:")
    for lab, _ in families:
        n_, m_ = base_mae[lab]
        print(f"    {lab:15s}  n={n_:>3d}  MAE={m_:>5.1f}%")
    print()

    # Test S22A (geometric mix, σ_AM=50 locked)
    print("=" * 110)
    print(" S22A: σ_AM=50 LOCKED + GEOMETRIC mix · Trevisanello NCM(r)")
    print("=" * 110)
    Xf_22A = X_keep[fit_mask]
    yf_22A = y_resid_S22A[fit_mask]
    c_22A, *_ = lstsq(Xf_22A, yf_22A, rcond=None)
    pred_22A_log = X_keep @ c_22A + offset_S22A
    err_22A = (np.exp(pred_22A_log) - sig_act) / sig_act * 100
    loo_22A = loo_r2_logsf(X_keep[fit_mask], offset_S22A[fit_mask], logsf[fit_mask])
    print(f"   LOOCV={loo_22A:.4f}  ΔLOOCV={loo_22A-fit21['loocv']:+.4f}")
    print(f"   coefs: β_T={c_22A[0]:+.3f}  β_v={c_22A[1]:+.3f}  "
          f"β_AC={c_22A[5]:+.3f}  β_φth={c_22A[6]:+.3f}  β_bi={c_22A[8]:+.3f}")
    mae_22A = per_fam_mae(err_22A)
    print(f"   per-family MAE:")
    for lab, _ in families:
        n_, m_ = mae_22A[lab]
        d = m_ - base_mae[lab][1] if not np.isnan(m_) else 0
        flag = ""
        if d < -1: flag = "  ◆ improves"
        elif d > +1: flag = "  ✗ worsens"
        print(f"    {lab:15s}  MAE={m_:>5.1f}% (Δ{d:+.1f}){flag}")
    print()

    # Test S22B (linear mix)
    print("=" * 110)
    print(" S22B: σ_AM=50 LOCKED + LINEAR mix")
    print("=" * 110)
    Xf_22B = X_keep[fit_mask]
    yf_22B = y_resid_S22B[fit_mask]
    c_22B, *_ = lstsq(Xf_22B, yf_22B, rcond=None)
    pred_22B_log = X_keep @ c_22B + offset_S22B
    err_22B = (np.exp(pred_22B_log) - sig_act) / sig_act * 100
    loo_22B = loo_r2_logsf(X_keep[fit_mask], offset_S22B[fit_mask], logsf[fit_mask])
    print(f"   LOOCV={loo_22B:.4f}  ΔLOOCV={loo_22B-fit21['loocv']:+.4f}")
    print(f"   coefs: β_T={c_22B[0]:+.3f}  β_v={c_22B[1]:+.3f}  "
          f"β_AC={c_22B[5]:+.3f}  β_φth={c_22B[6]:+.3f}  β_bi={c_22B[8]:+.3f}")
    mae_22B = per_fam_mae(err_22B)
    print(f"   per-family MAE:")
    for lab, _ in families:
        n_, m_ = mae_22B[lab]
        d = m_ - base_mae[lab][1] if not np.isnan(m_) else 0
        flag = ""
        if d < -1: flag = "  ◆ improves"
        elif d > +1: flag = "  ✗ worsens"
        print(f"    {lab:15s}  MAE={m_:>5.1f}% (Δ{d:+.1f}){flag}")
    print()

    # Focused 1mAh per-case before/after comparison
    print("=" * 110)
    print(" 1mAh per-case shape comparison (BASELINE vs S22A vs S22B)")
    print("=" * 110)
    print(f"  {'name':35s}  {'σ_act':>6s}  {'S21':>6s}  {'err':>6s}  "
          f"{'S22A':>6s}  {'err':>6s}  {'S22B':>6s}  {'err':>6s}")
    pred_22A = np.exp(pred_22A_log)
    pred_22B = np.exp(pred_22B_log)
    pred_21 = np.exp(fit21['pred_log'])
    for i in range(n):
        if '1mAh' not in nms[i] or '_real' in nms[i]: continue
        if arr['excluded'][i]: continue
        e21 = err21[i]; e22A = err_22A[i]; e22B = err_22B[i]
        print(f"  {nms[i][:35]:35s}  {sig_act[i]:>6.2f}  "
              f"{pred_21[i]:>6.2f}  {e21:>+5.1f}%  "
              f"{pred_22A[i]:>6.2f}  {e22A:>+5.1f}%  "
              f"{pred_22B[i]:>6.2f}  {e22B:>+5.1f}%")
    print()

    # ───── Verdict ─────
    print("=" * 110)
    print(" VERDICT")
    print("=" * 110)
    print(f"  Baseline Stage 21       LOOCV={fit21['loocv']:.4f}  1mAh_MAE={base_mae['1mAh'][1]:.1f}%")
    print(f"  S22A geometric+lock50   LOOCV={loo_22A:.4f}  1mAh_MAE={mae_22A['1mAh'][1]:.1f}%")
    print(f"  S22B linear+lock50      LOOCV={loo_22B:.4f}  1mAh_MAE={mae_22B['1mAh'][1]:.1f}%")
    print()
    if min(loo_22A, loo_22B) > fit21['loocv'] - 0.01:
        print("  ★ Locked-σ_AM version stays within LOOCV tolerance.")
        if min(mae_22A['1mAh'][1], mae_22B['1mAh'][1]) < base_mae['1mAh'][1] - 1:
            print("  ★ Shape match (1mAh MAE) IMPROVES → adopt as Stage 22.")
        else:
            print("  Shape match equivalent. σ_S/σ_P live-fit was overfitting noise,")
            print("  but locking doesn't structurally improve shape either.")
    else:
        print("  σ_AM=50 locking degrades LOOCV significantly → live-fit σ_S/σ_P")
        print("  was encoding real physics (S-end vs P-end have different effective σ).")
        print("  Stage 21 structurally correct.  Shape misses are intrinsic data variance.")


if __name__ == '__main__':
    main()
