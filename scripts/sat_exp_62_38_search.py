#!/usr/bin/env python3
"""Scan exponential / saturation / coupled terms for the D1/D1.5 62:38 corner.

The 62:38 outliers (particulate_7 D1, _10 D1.5; pure 0:10, large SE r_SE≥1µm,
φ_SE≈0.38) are the last failure mode of the SAT-blend × Cronau form.  Every
LINEAR / power-law correction we've tested (am_se_cn, coverage variants,
r_SE/r_AM ratio, sub-µm GB, path_hop_area, stress_cv, cn_eff_area …) has
either FAILED nested CV or generalized only inside the 62:38 subset.

Hypothesis (this script): at extreme SE fraction (φ_SE ≳ 0.30) with LARGE
SE grains, the conductivity is dominated by bulk-like grain conduction —
specific GB area per volume drops, individual grain conductance saturates,
and the response is EXPONENTIAL in (φ × r_SE) rather than a multiplicative
mean-field power.  Tests:

    Saturation-style (toward σ_grain):
      A.  log(1 − exp(−α·(φ−φc))_+)               α ∈ scan
      B.  log(1 + exp(α·(φ−PHI_HIGH)))            soft-plus ramp above φ=0.30
      C.  exp(α·(φ−PHI_HIGH))_+                   rectified exp ramp
    Bulk-grain (SE volume × grain size):
      D.  (φ−φc)_+ × r_SE                         linear coupling
      E.  (φ−φc)_+² × r_SE                        quadratic coupling
      F.  exp(γ·φ·r_SE) − 1                       γ scan; pure exp
      G.  log(φ·r_SE)                             log-coupled
    GB / surface area (1/r_SE-like):
      H.  −φ/r_SE                                 specific GB area, inverse
      I.  −log(φ/r_SE)                            log-inverse
    High-CN saturation:
      J.  exp(CN/CN0) − 1                         CN0 scan
    Tortuosity:
      K.  exp(−ατ)                                α scan
    Pinpoint (D1/D1.5 corner gate):
      L.  g_high × g_010 × log(1 + α·(φ−PHI_HIGH)·r_SE)   α scan

Each candidate is fit as a single OLS coefficient β added to (SAT × Cronau);
LOOCV β is unbiased (no inner selection) and we also report:
    • RMSE on the 62:38 SUBSET (p<0.05, φ>0.30, r_SE≥1.0)    — DID we catch it?
    • global LOOCV Δ                                          — at what cost?

Run from the repo root:  python3 scripts/sat_exp_62_38_search.py
"""
from __future__ import annotations
import sys
from pathlib import Path
import numpy as np

SCRIPTS = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS))
from nested_cv_sat import (load_corpus, base_log_sat, loocv_r2, loocv_with_feat,
                           cblend_fit, cblend_pred, cronau_factor,
                           PHICP_F, PHICS_F, DELTA_F, K_PS, P_C)


PHI_HIGH = 0.30
PHIC_FIX = 0.195  # composition-neutral threshold (0:10 limit)


def _g_high(phi, k=15.0):
    return 1.0/(1.0+np.exp(-k*(phi - PHI_HIGH)))


def _g_010(p):
    return 1.0/(1.0+np.exp(K_PS*(p - P_C)))


def _pex(a):
    return np.maximum(a[:, 0] - PHIC_FIX, 0.0)


def _make_features(a, alpha_grid=None):
    """Return a dict {label: feat_vector} of all candidates (scanned ones
    expand into a small family at multiple α values)."""
    phi, cn, p, rse, tau = a[:, 0], a[:, 1], a[:, 6], a[:, 8], a[:, 4]
    rse_safe = np.where(np.isfinite(rse) & (rse > 0), rse, np.nanmedian(rse[np.isfinite(rse)]))
    pex = _pex(a)
    gh = _g_high(phi)
    g0 = _g_010(p)

    feats = {}
    # A. saturation toward σ_grain
    for alpha in (3.0, 6.0, 10.0, 15.0, 25.0):
        v = 1.0 - np.exp(-alpha * pex)
        v = np.log(np.maximum(v, 1e-9))
        feats[f"A_log(1-exp(-{alpha:.0f}·(φ-φc)))"] = v
    # B. soft-plus above φ=0.30
    for alpha in (5.0, 10.0, 20.0):
        v = np.log1p(np.exp(np.clip(alpha*(phi - PHI_HIGH), -50, 50)))
        feats[f"B_softplus({alpha:.0f}·(φ-0.30))"] = v
    # C. rectified exp ramp above PHI_HIGH
    for alpha in (5.0, 10.0, 20.0):
        v = np.where(phi > PHI_HIGH, np.exp(alpha*(phi - PHI_HIGH)) - 1.0, 0.0)
        feats[f"C_rect_exp({alpha:.0f}·(φ-0.30))"] = v
    # D-E. coupled bulk-grain
    feats["D_(φ-φc)·r_SE"]     = pex * rse_safe
    feats["E_(φ-φc)²·r_SE"]    = pex**2 * rse_safe
    feats["E2_(φ-φc)·r_SE²"]   = pex * rse_safe**2
    # F. exp(γ·φ·r_SE) − 1
    for gamma in (0.5, 1.0, 2.0, 3.0):
        feats[f"F_exp({gamma:.1f}·φ·r_SE)-1"] = np.exp(gamma*phi*rse_safe) - 1.0
    # G. log(φ·r_SE)
    feats["G_log(φ·r_SE)"] = np.log(np.maximum(phi*rse_safe, 1e-9))
    # H. specific GB area, inverse
    feats["H_-φ/r_SE"] = -phi/np.maximum(rse_safe, 1e-3)
    feats["H2_-log(φ/r_SE)"] = -np.log(np.maximum(phi/np.maximum(rse_safe, 1e-3), 1e-9))
    # I. raw r_SE (control — already tested but as power)
    feats["I_log(r_SE)"] = np.log(np.maximum(rse_safe, 1e-3))
    feats["I2_r_SE"]     = rse_safe
    # J. high-CN saturation
    for cn0 in (3.0, 5.0, 8.0):
        feats[f"J_exp(CN/{cn0:.0f})-1"] = np.exp(cn/cn0) - 1.0
    # K. tortuosity exp
    for alpha in (1.0, 2.0, 4.0):
        feats[f"K_exp(-{alpha:.0f}·τ)"] = np.exp(-alpha*tau)
    # L. D1/D1.5 corner pinpoint with coupling
    for alpha in (1.0, 3.0, 6.0):
        feats[f"L_g_hi·g_010·log(1+{alpha:.0f}·(φ-0.30)·r_SE)"] = (
            gh * g0 * np.log1p(np.maximum(alpha*(phi - PHI_HIGH)*rse_safe, 0.0))
        )
    # M. g_high gated on plain features (control — same gate other terms used)
    feats["M_g_hi·(φ-φc)·r_SE"] = gh * pex * rse_safe
    feats["M2_g_hi·g_010·(φ-φc)·r_SE"] = gh * g0 * pex * rse_safe
    # N. surface vs bulk: φ_SE × r_SE - reference power
    feats["N_(φ-φc)^0.5·log(r_SE)"] = np.sqrt(pex + 1e-9) * np.log(np.maximum(rse_safe, 1e-3))

    # ── INTEGRATED candidates (modify an existing term instead of bolt-on) ──
    # Same DoF (one β), but the form has physical meaning rather than additive.
    # Goal: a "meaningful" σ_ionic equation, not σ × exp(β·blob).
    p_arr = a[:, 6]
    g010 = 1.0/(1.0+np.exp(10.0*(p_arr - 0.5)))
    phic_blend = (1.0 - g010)*0.200 + g010*0.195
    pex_blend = phi - phic_blend
    phi_eff_blend = np.sqrt(pex_blend**2 + (0.040*g010)**2 + 1e-12)
    log_phi_eff = np.log(phi_eff_blend)
    # O.  φ_eff exponent depends on grain size: (φ_eff)^(0.5 + κ·r_SE)
    #     → log term = κ · r_SE · log(φ_eff)   [INTEGRATED into (φ_eff)^0.5]
    feats["O_r_SE·log(φ_eff)  [φ_eff exponent ~ r_SE]"] = rse_safe * log_phi_eff
    feats["O2_(r_SE-0.5)·log(φ_eff)  [centered at Cronau ref]"] = (rse_safe - 0.5) * log_phi_eff
    # P.  Cronau extended to high-r_SE × high-φ (bulk-grain saturation)
    #     → log term = γ · (φ−φc) · (r_SE − 0.5)_+ when r_SE > 0.5µm AND φ > φc
    rse_hi = np.maximum(rse_safe - 0.5, 0.0)
    feats["P_(φ-φc)·(r_SE-0.5)+  [Cronau high-r_SE arm]"] = pex_blend.clip(min=0) * rse_hi
    feats["P2_(φ-φc)²·(r_SE-0.5)+ [Cronau, quadratic-φ]"] = pex_blend.clip(min=0)**2 * rse_hi
    # Q.  CN exponent depends on grain size: CN^(2 + κ·r_SE)
    #     → log term = κ · r_SE · log(CN)   [INTEGRATED into CN²]
    feats["Q_r_SE·log(CN)  [CN exponent ~ r_SE]"] = rse_safe * np.log(np.maximum(cn, 1e-6))
    feats["Q2_(r_SE-0.5)·log(CN)  [centered]"] = (rse_safe - 0.5) * np.log(np.maximum(cn, 1e-6))
    # R.  cov exponent depends on grain size (long-shot)
    #     → log term = κ · r_SE · log(cov)   [INTEGRATED into cov^0.5]
    cov_arr = a[:, 2]
    feats["R_r_SE·log(cov)  [cov exponent ~ r_SE]"] = rse_safe * np.log(np.maximum(cov_arr, 1e-9))

    return feats


def _subset_62_38(a):
    """SE-rich 0:10 (D1/D1.5-type): p<0.05 (pure AM_S), φ>PHI_HIGH, r_SE≥1.0µm."""
    p, phi, rse = a[:, 6], a[:, 0], a[:, 8]
    return np.where((p < 0.05) & (phi > PHI_HIGH) & np.isfinite(rse) & (rse >= 1.0))[0]


def _subset_se_rich(a):
    """SE-rich 0:10 (any r_SE; D1/D1.5 cluster including their D0.25/D0.5 siblings)."""
    p, phi = a[:, 6], a[:, 0]
    return np.where((p < 0.05) & (phi > PHI_HIGH))[0]


def _rmse_on(idx, logsf, pred):
    if len(idx) == 0:
        return float('nan')
    return float(np.sqrt(np.mean((logsf[idx] - pred[idx])**2)))


def _pred_with_feat(base, logsf, taus, sfeat):
    """Single-shot fit (no LOO) of C_blend + β·sfeat → predicted log σ on
    every case.  Used to quantify the 62:38 RMSE *change* from the term."""
    b = cblend_fit(base, logsf, taus)
    resid = logsf - cblend_pred(base, taus, b)
    sm = sfeat.mean(); sc = sfeat - sm
    d = float(np.dot(sc, sc))
    beta = float(np.dot(sc, resid)/d) if d > 1e-12 else 0.0
    return cblend_pred(base, taus, b) + beta*(sfeat - sm), beta


def main():
    a = load_corpus()
    n = len(a)
    if n < 20:
        print(f"[ABORT] only {n} cases (need WSL corpus)."); return
    logsf = np.log(a[:, 5]); taus = a[:, 4]
    ss = np.sum((logsf-logsf.mean())**2)
    se = np.sqrt(np.var((logsf - logsf.mean())**2) / n) / ss   # rough LOOCV noise SE

    # SAT × Cronau base (production)
    base = base_log_sat(a, PHICP_F, PHICS_F, DELTA_F) + np.log(cronau_factor(a[:, 8]))
    lo_ref = loocv_r2(base, logsf, taus)
    pred_ref, _ = _pred_with_feat(base, logsf, taus, np.zeros(n))  # β=0, just C_blend
    # actually compute ref pred via cblend_pred directly to avoid degenerate β path
    b = cblend_fit(base, logsf, taus)
    pred_ref = cblend_pred(base, taus, b)

    idx_corner = _subset_62_38(a)
    idx_serich = _subset_se_rich(a)
    rmse_corner_ref = _rmse_on(idx_corner, logsf, pred_ref)
    rmse_serich_ref = _rmse_on(idx_serich, logsf, pred_ref)
    rmse_global_ref = _rmse_on(np.arange(n), logsf, pred_ref)

    print("=" * 78)
    print(f"62:38 exp/sat/coupled term search — base = SAT × Cronau  (n={n})")
    print("=" * 78)
    print(f"  base LOOCV                    : {lo_ref:.4f}")
    print(f"  base RMSE (global)            : {rmse_global_ref:.3f}")
    print(f"  base RMSE (SE-rich 0:10)      : {rmse_serich_ref:.3f}   "
          f"[n={len(idx_serich)}]")
    print(f"  base RMSE (62:38 corner, r_SE≥1µm): {rmse_corner_ref:.3f}   "
          f"[n={len(idx_corner)}]")
    print(f"  rough LOOCV noise SE          : {se:.4f}")
    print("=" * 78)
    print("Candidates (β = OLS, LOOCV unbiased; '↓rmse' = improvement on subset):")
    print(f"  {'tag':52s} {'LOOCV':>7s} {'Δ':>7s} {'β':>7s} {'↓rmse_62':>10s} {'↓rmse_SE':>10s}")
    print("-" * 110)

    feats = _make_features(a)
    rows = []
    for tag, sf in feats.items():
        if not np.all(np.isfinite(sf)):
            print(f"  [skip {tag}: non-finite values]"); continue
        if np.std(sf) < 1e-12:
            print(f"  [skip {tag}: constant feature]"); continue
        lo, beta = loocv_with_feat(base, logsf, taus, sf)
        # single-shot pred to measure subset RMSE change
        pred, beta_ss = _pred_with_feat(base, logsf, taus, sf)
        d_rmse_corner = rmse_corner_ref - _rmse_on(idx_corner, logsf, pred)
        d_rmse_serich = rmse_serich_ref - _rmse_on(idx_serich, logsf, pred)
        delta = lo - lo_ref
        rows.append((tag, lo, delta, beta, d_rmse_corner, d_rmse_serich))

    rows.sort(key=lambda r: -r[2])  # by global LOOCV Δ
    for tag, lo, delta, beta, drc, drs in rows:
        flag = " ★" if delta > se and drc > 0 else (" ⚠" if delta > 0 and drc < 0 else "")
        print(f"  {tag:52s} {lo:7.4f} {delta:+7.4f} {beta:+7.3f} "
              f"{drc:+10.3f} {drs:+10.3f}{flag}")
    print("-" * 110)
    print("  ★ = global LOOCV Δ > noise SE AND 62:38 corner RMSE improved")
    print("  ⚠ = global gain but 62:38 RMSE got worse (= it learned elsewhere)")
    print("\nNotes:")
    print(" - β is the LOOCV-mean coefficient (unbiased — no inner selection).")
    print(" - 62:38 corner subset = p<0.05 AND φ>0.30 AND r_SE≥1.0µm "
          f"(n={len(idx_corner)}). This is the D1/D1.5 target.")
    print(" - SE-rich subset = p<0.05 AND φ>0.30 (any r_SE), wider context "
          f"(n={len(idx_serich)}).")
    print(" - Any '★' candidate is a real lead; pipe it into nested_cv_sat_feat "
          "for the full nested verdict.")


if __name__ == "__main__":
    main()
