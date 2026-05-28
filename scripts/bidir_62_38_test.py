#!/usr/bin/env python3
"""Test BIDIRECTIONAL correction for the 0:10 SE-rich r_SE-sweep bias.

The 62:38 corner shows opposite-sign errors with r_SE:
   r_SE = 0.5 µm  →  form OVER-predicts (input_S_2 +32%, particulate_5 +22%)
   r_SE ≥ 1.0 µm  →  form UNDER-predicts (particulate_7 -24%, _10 -37%)

A SINGLE multiplicative correction (P2) catches only the r_SE≥1 side
(P2 is mathematically zero at r_SE=0.5).  This script tests whether
adding a SECOND correction that fires at r_SE=0.5 in the same 0:10
SE-rich gate can catch the over-prediction side too.

The diagnostic candidate: `coverage_AM_S_delta_pct_rough` had +0.86
correlation with the SAT-blend residual in the 62:38 subset (n=15) —
strongest single non-circular signal.  Tested as ungated additive
in nested CV before (FAIL Δ≈0), but the gated-to-0:10 SE-rich version
was never tested.

Tests:
  C1.  P2 alone
  C2.  gated cov_delta alone
  C3.  P2 + gated cov_delta JOINT (joint OLS for both β)
  C4.  P2 + ungated cov_delta JOINT (control)

For each: LOOCV, β values, predicted err% on the 4 corner cases
(S_2 / particulate_5 / particulate_7 / particulate_10), and the
leave-corner-out result for the JOINT model.

Run from the repo root:  python3 scripts/bidir_62_38_test.py
"""
from __future__ import annotations
import sys, json
from pathlib import Path
import numpy as np

SCRIPTS = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS))
import generate_comparison_plots as gcp  # noqa
from nested_cv_sat import (load_corpus, base_log_sat, cblend_fit, cblend_pred,
                           cronau_factor, _meta_name, _EXCLUDED_NAMES,
                           PHICP_F, PHICS_F, DELTA_F, K_PS, P_C, PHI_C0)


PHI_HIGH = 0.30; K_PHI_HIGH = 15.0
PHIC_FIX = 0.195


def _g_high(phi):
    return 1.0/(1.0+np.exp(-K_PHI_HIGH*(phi - PHI_HIGH)))


def _g_010(p):
    return 1.0/(1.0+np.exp(K_PS*(p - P_C)))


def _rse_safe(a):
    rse = a[:, 8]
    med = float(np.nanmedian(rse[np.isfinite(rse)])) if np.isfinite(rse).any() else 0.5
    return np.where(np.isfinite(rse) & (rse > 0), rse, med)


def p2_feat(a):
    """P2: (φ−φc_S)²·(r_SE−0.5)+  — catches r_SE≥1µm under-prediction."""
    pex = np.maximum(a[:, 0] - PHIC_FIX, 0.0)
    rse_hi = np.maximum(_rse_safe(a) - 0.5, 0.0)
    return pex**2 * rse_hi


def cov_delta_raw(a):
    """log(coverage_AM_S_delta_pct_rough / median), already in column 12 as
    `cov_dlt`.  May be 0 or negative depending on Hertz→physics direction."""
    v = a[:, 12]
    med = float(np.nanmedian(v[np.isfinite(v)])) if np.isfinite(v).any() else 0.0
    return np.where(np.isfinite(v), v - med, 0.0)


def cov_delta_gated(a):
    """g_010 · g_high · cov_delta_raw — fires only in 0:10 SE-rich corner.
    Hypothesis: this should be positive when Hertz→physics amplification
    is large (= form under-predicts) and negative when amplification is
    small (= form over-predicts), giving bidirectional correction."""
    return _g_010(a[:, 6]) * _g_high(a[:, 0]) * cov_delta_raw(a)


def _load_names(a):
    """Re-walk corpus to get case names aligned with `a` (matches load_corpus
    iteration order)."""
    names, seen = [], set()
    for base in ('webapp/results', 'webapp/archive'):
        bp = Path(base)
        if not bp.is_dir():
            continue
        for mp in bp.rglob('full_metrics.json'):
            try:
                d = json.load(open(mp))
            except Exception:
                continue
            sig = gcp._stage_e_sigma(d)
            phi = gcp._get(d, 'phi_se'); cn = gcp._get(d, 'se_se_cn')
            cov = gcp._cov_frac(d, physics=True) or gcp._cov_frac(d, physics=False)
            fp = gcp._get(d, 'percolation_pct') / 100.0
            tau = gcp._get(d, 'tortuosity_recommended', gcp._get(d, 'tortuosity_mean', 0))
            if not (sig and sig > 0 and phi > PHI_C0 and cn > 0 and cov and cov > 0
                    and fp > 0 and tau > 0):
                continue
            nm = _meta_name(mp.parent.name, mp.parent)
            if nm in _EXCLUDED_NAMES:
                continue
            key = (round(phi, 4), round(cn, 3), round(float(sig), 5))
            if key in seen:
                continue
            seen.add(key)
            names.append(nm)
    return names


def _loocv_joint(base, logsf, taus, feats):
    """LOOCV with C_blend + k extra β coefficients (joint OLS).  `feats` is
    a list of (name, vec) tuples.  Returns (R², mean_betas dict)."""
    n = len(taus); ss = float(np.sum((logsf-logsf.mean())**2)); sse = 0.0
    lt = np.log(taus)
    X_cb = np.column_stack([np.ones(n), lt, lt**2])
    # Joint design: [C_blend basis | each feature centered]
    sf_mat = np.column_stack([sf for _, sf in feats])
    sf_means = sf_mat.mean(axis=0)
    X_full = np.column_stack([X_cb, sf_mat - sf_means])
    betas_acc = []
    for i in range(n):
        mk = np.ones(n, bool); mk[i] = False
        coef, *_ = np.linalg.lstsq(X_full[mk], logsf[mk] - base[mk], rcond=None)
        pi = base[i] + X_full[i] @ coef
        sse += (logsf[i] - pi)**2
        betas_acc.append(coef[3:])  # the feature β's (skip C_blend's 3)
    betas_acc = np.array(betas_acc)
    mean_b = {feats[j][0]: float(np.mean(betas_acc[:, j])) for j in range(len(feats))}
    # Also return single-shot β for per-case prediction
    coef_ss, *_ = np.linalg.lstsq(X_full, logsf - base, rcond=None)
    pred_ss = base + X_full @ coef_ss
    return 1 - sse/ss, mean_b, coef_ss, pred_ss


def main():
    a = load_corpus()
    n = len(a)
    if n < 20:
        print(f"[ABORT] only {n} cases (need WSL corpus)."); return
    names = _load_names(a)
    logsf = np.log(a[:, 5]); taus = a[:, 4]
    cf = cronau_factor(a[:, 8])
    base = base_log_sat(a, PHICP_F, PHICS_F, DELTA_F) + np.log(cf)

    # Reference LOOCV (no extra term)
    bv = cblend_fit(base, logsf, taus)
    pred_ref = cblend_pred(base, taus, bv)
    sse_ref = float(np.sum((logsf - pred_ref)**2))
    ss = float(np.sum((logsf-logsf.mean())**2))
    lo_ref = 1 - sse_ref/ss
    se_loocv = np.sqrt(np.var((logsf-logsf.mean())**2)/n) / ss

    # Identify the 4 named target cases
    target_names = ['input_S_2', 'input_particulate_5', 'input_particulate_7', 'input_particulate_10']
    idx_targets = {nm: names.index(nm) if nm in names else None for nm in target_names}
    idx_corner = np.where((a[:, 6] < 0.05) & (a[:, 0] > PHI_HIGH) &
                          np.isfinite(a[:, 8]) & (a[:, 8] >= 1.0))[0]

    print("=" * 80)
    print(f"BIDIRECTIONAL 0:10 SE-rich corner test  (n={n}, base LOOCV = {lo_ref:.4f})")
    print(f"  noise SE on LOOCV = {se_loocv:.4f}")
    print("=" * 80)
    print(f"\nBase (no extra term) — error on the 4 target cases:")
    print(f"  {'name':28s} {'r_SE':>5s} {'σ_act':>7s} {'σ_pred':>7s} {'err%':>7s}")
    for nm in target_names:
        i = idx_targets[nm]
        if i is None:
            print(f"  {nm:28s}  (not in corpus)"); continue
        sa = float(np.exp(logsf[i])); sp = float(np.exp(pred_ref[i]))
        err = (sp-sa)/sa*100
        print(f"  {nm:28s} {a[i,8]:5.2f} {sa:7.3f} {sp:7.3f} {err:+7.1f}")

    # Run all 4 candidate models
    candidates = [
        ('C1: P2 alone',                     [('P2', p2_feat(a))]),
        ('C2: cov_delta gated alone',        [('cov_g', cov_delta_gated(a))]),
        ('C3: P2 + cov_delta GATED JOINT',   [('P2', p2_feat(a)),
                                              ('cov_g', cov_delta_gated(a))]),
        ('C4: P2 + cov_delta UNGATED JOINT', [('P2', p2_feat(a)),
                                              ('cov_u', cov_delta_raw(a))]),
    ]
    for tag, feats in candidates:
        print("\n" + "=" * 80)
        print(f"{tag}")
        print("=" * 80)
        try:
            lo, mean_b, coef_ss, pred_x = _loocv_joint(base, logsf, taus, feats)
        except Exception as e:
            print(f"  [ERROR] {e}"); continue
        d = lo - lo_ref
        flag = "★" if d > se_loocv else (" " if abs(d) < se_loocv else "⚠")
        print(f"  LOOCV = {lo:.4f}   Δ vs base = {d:+.4f}   {flag}")
        for k, v in mean_b.items():
            print(f"  β_{k:8s} = {v:+.4f}  (LOO mean)")
        # Per-case error on the 4 targets
        print(f"  per-target error (single-shot fit):")
        print(f"    {'name':28s} {'σ_pred':>7s} {'err%':>7s} (Δ from base)")
        for nm in target_names:
            i = idx_targets[nm]
            if i is None: continue
            sa = float(np.exp(logsf[i]))
            sp_base = float(np.exp(pred_ref[i]))
            sp_x = float(np.exp(pred_x[i]))
            err_base = (sp_base-sa)/sa*100
            err_x = (sp_x-sa)/sa*100
            print(f"    {nm:28s} {sp_x:7.3f} {err_x:+7.1f} ({err_x-err_base:+.1f} from base {err_base:+.1f})")
        # Corner subset RMSE
        rmse_corner_base = float(np.sqrt(np.mean((logsf[idx_corner] - pred_ref[idx_corner])**2)))
        rmse_corner_x = float(np.sqrt(np.mean((logsf[idx_corner] - pred_x[idx_corner])**2)))
        print(f"  62:38 corner (n={len(idx_corner)}) RMSE: {rmse_corner_base:.3f} → {rmse_corner_x:.3f}   "
              f"(Δ {rmse_corner_x - rmse_corner_base:+.3f})")
        # Leave-corner-out check for joint model
        idx_bulk = np.array([j for j in range(n) if j not in set(idx_corner)])
        try:
            lo_bulk, mean_b_bulk, coef_bulk, pred_bulk_full = _loocv_joint(
                base[idx_bulk], logsf[idx_bulk], taus[idx_bulk],
                [(k, sf[idx_bulk]) for k, sf in feats])
            # Use bulk coefs to predict the corner
            # Build a full-corpus design with bulk-mean centering
            sf_mat = np.column_stack([sf for _, sf in feats])
            sf_means_bulk = np.array([sf[idx_bulk].mean() for _, sf in feats])
            lt = np.log(taus)
            X_cb = np.column_stack([np.ones(n), lt, lt**2])
            X_full_corp = np.column_stack([X_cb, sf_mat - sf_means_bulk])
            pred_bulk_at_corner = base[idx_corner] + X_full_corp[idx_corner] @ coef_bulk
            rmse_corner_bulk = float(np.sqrt(np.mean((logsf[idx_corner] - pred_bulk_at_corner)**2)))
            print(f"  Leave-corner-out: bulk-only fit β = " +
                  ", ".join(f"{k}:{v:+.3f}" for k, v in mean_b_bulk.items()))
            print(f"    corner RMSE with bulk β = {rmse_corner_bulk:.3f}   "
                  f"(vs no-β = {rmse_corner_base:.3f}, Δ = {rmse_corner_bulk - rmse_corner_base:+.3f})")
            sign_match = all(np.sign(mean_b[k]) == np.sign(mean_b_bulk[k]) for k in mean_b)
            improved = rmse_corner_bulk < rmse_corner_base - 0.05
            v6 = ("PASS — bulk β consistent in sign AND improves corner"
                  if (sign_match and improved) else
                  ("WEAK — sign-consistent but small corner improvement" if sign_match else
                   "FAIL — sign-inconsistent (corner overfit)"))
            print(f"    VERDICT: {v6}")
        except Exception as e:
            print(f"  [leave-corner-out skipped: {e}]")

    print("\n" + "=" * 80)
    print("Interpretation:")
    print("  • C3 (P2 + cov_delta GATED JOINT) is the bidirectional candidate.")
    print("    If it catches BOTH r_SE=0.5 (S_2, particulate_5) AND r_SE≥1.0")
    print("    (particulate_7, _10) with sign-consistent bulk β → adopt as form")
    print("    augmentation.  Otherwise document the bidirectional limit.")
    print("  • If C2 alone catches input_S_2 but P2 alone catches particulate_10,")
    print("    they really ARE two separate corrections — C3 should beat both.")


if __name__ == "__main__":
    main()
