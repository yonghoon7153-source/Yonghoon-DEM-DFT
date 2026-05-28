#!/usr/bin/env python3
"""Holistic screening — can the production σ_ionic form be simplified?

The current form has 7 multiplicative factors:
  σ = σ_grain · Cronau(r_SE) · (φ_eff)^½ · CN² · cov^½ · f_p³ · C_blend(τ)
plus the φ_eff disorder rounding (δ·g_phys) and the dual-branch C_blend(τ).
Exponents (½, 2, ½, 3) were locked one-at-a-time; this script asks four
holistic questions:

  Q1. JOINT EXPONENT OPTIMUM.  When all four exponents move TOGETHER, does
      the optimum sit at (2.0, 0.5, 0.5, 3.0)?  Interactions could pull it
      elsewhere (e.g. tightening CN compensated by loosening f_p).
  Q2. PERCOLATION TERM MERGE.  (φ_eff)^½ · f_p³  →  (φ_eff · f_p^k)^α
      one merged percolation factor?
  Q3. NETWORK TERM MERGE.  CN² · cov^½  →  (CN · √cov)^α  or  (CN · cov)^α
      one merged network factor?
  Q4. C_blend SIMPLIFICATION.  Current dual-branch has 6 fit params.  Try
      τ^(-α) (1 param), ε/τ² (Bruggeman, 0 params), low-order log poly,
      etc.  Simpler form with equivalent LOOCV → prefer the simpler one.
  Q5. δ-saturation NECESSARY?  Test δ=0 — does removing the rounding lose
      anything?

For each candidate report (LOOCV, ΔAIC vs production, # free params).
Rule of thumb: SIMPLER form with |ΔLOOCV| < noise SE is the prefer.

Run from the repo root:  python3 scripts/screen_form_simplifications.py
"""
from __future__ import annotations
import sys
from pathlib import Path
import numpy as np

SCRIPTS = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS))
from nested_cv_sat import (load_corpus, base_log_sat, base_no_phi, loocv_r2,
                           cblend_fit, cblend_pred, cronau_factor,
                           PHICP_F, PHICS_F, DELTA_F, K_PS, P_C, SG)


def _g010(p):
    return 1.0/(1.0+np.exp(K_PS*(p - 0.5)))


def base_log_general(a, e_phi=0.5, e_cn=2.0, e_cov=0.5, e_fp=3.0,
                     phicP=PHICP_F, phicS=PHICS_F, delta=DELTA_F):
    """General SAT-blend base with all four exponents variable."""
    phi, cn, cov, fp, p = a[:, 0], a[:, 1], a[:, 2], a[:, 3], a[:, 6]
    g = _g010(p)
    phic = (1.0 - g)*phicP + g*phicS
    pex = phi - phic
    phi_eff = np.sqrt(pex**2 + (delta*g)**2 + 1e-12)
    return (np.log(SG) + e_phi*np.log(phi_eff) + e_cn*np.log(cn)
            + e_cov*np.log(cov) + e_fp*np.log(fp))


def _loocv_const_blend(base, logsf, taus, n_params_fit):
    """LOOCV with C_blend refit (6 fit params) — returns R² and (n_fit, sse)."""
    n = len(taus); ss = float(np.sum((logsf - logsf.mean())**2))
    sse = 0.0
    for i in range(n):
        m = np.ones(n, bool); m[i] = False
        b = cblend_fit(base[m], logsf[m], taus[m])
        pi = cblend_pred(base[i:i+1], taus[i:i+1], b)[0]
        sse += (logsf[i] - pi)**2
    return 1 - sse/ss, sse, n_params_fit


def _loocv_simpler_blend(base, logsf, taus, blend_kind):
    """LOOCV with a SIMPLER C_blend replacement. Returns R², sse, n_fit_params."""
    n = len(taus); ss = float(np.sum((logsf - logsf.mean())**2)); sse = 0.0
    for i in range(n):
        m = np.ones(n, bool); m[i] = False
        t = taus[m]; y = logsf[m] - base[m]
        if blend_kind == 'const':
            c = float(np.mean(y)); pi = base[i] + c
            n_fit = 1
        elif blend_kind == 'pow_tau':       # σ ∝ τ^-α  →  log τ slope
            X = np.column_stack([np.ones(len(t)), np.log(t)])
            β = np.linalg.lstsq(X, y, rcond=None)[0]
            pi = base[i] + β[0] + β[1]*np.log(taus[i])
            n_fit = 2
        elif blend_kind == 'inv_tau2':      # σ ∝ 1/τ²  (Bruggeman, 0 free)
            # but allow one intercept to match scale → 1 free param
            X = np.column_stack([np.ones(len(t)), -2.0*np.log(t)])
            β = np.linalg.lstsq(X, y, rcond=None)[0]
            pi = base[i] + β[0] - 2.0*np.log(taus[i])  # fix slope = -2
            n_fit = 1
        elif blend_kind == 'logpoly2':      # a + b·ln τ + c·(ln τ)²
            lt = np.log(t)
            X = np.column_stack([np.ones(len(t)), lt, lt**2])
            β = np.linalg.lstsq(X, y, rcond=None)[0]
            lt_i = np.log(taus[i])
            pi = base[i] + β[0] + β[1]*lt_i + β[2]*lt_i**2
            n_fit = 3
        elif blend_kind == 'logpoly3':      # a + b·ln τ + c·(ln τ)² + d·(ln τ)³
            lt = np.log(t)
            X = np.column_stack([np.ones(len(t)), lt, lt**2, lt**3])
            β = np.linalg.lstsq(X, y, rcond=None)[0]
            lt_i = np.log(taus[i])
            pi = base[i] + β[0] + β[1]*lt_i + β[2]*lt_i**2 + β[3]*lt_i**3
            n_fit = 4
        else:
            raise ValueError(blend_kind)
        sse += (logsf[i] - pi)**2
    return 1 - sse/ss, sse, n_fit


def _aic_bic(sse, n, k):
    """Gaussian AIC/BIC with k = # free params."""
    return n*np.log(sse/n) + 2*k, n*np.log(sse/n) + np.log(n)*k


def main():
    a = load_corpus()
    n = len(a)
    if n < 20:
        print(f"[ABORT] only {n} cases."); return
    logsf = np.log(a[:, 5]); taus = a[:, 4]
    ss = np.sum((logsf-logsf.mean())**2)
    cf = cronau_factor(a[:, 8])

    # Production reference (full C_blend, 6 params)
    base_prod = base_log_general(a) + np.log(cf)
    lo_prod, sse_prod, k_prod = _loocv_const_blend(base_prod, logsf, taus, 6)
    aic_prod, bic_prod = _aic_bic(sse_prod, n, k_prod)
    se = np.sqrt(np.var((logsf-logsf.mean())**2)/n) / ss

    print("=" * 90)
    print(f"Holistic form-simplification screen   n={n}   noise SE = {se:.4f}")
    print("=" * 90)
    print(f"PRODUCTION REFERENCE: σ_grain·Cronau·(φ_eff)^.5·CN²·cov^.5·f_p³·C_blend(τ)")
    print(f"  LOOCV = {lo_prod:.4f}   SSE = {sse_prod:.4f}   k_fit = {k_prod}")
    print(f"  AIC = {aic_prod:+.2f}    BIC = {bic_prod:+.2f}")

    # Q1. JOINT EXPONENT scan over (e_phi, e_cn, e_cov, e_fp)
    print("\n" + "=" * 90)
    print("Q1. JOINT exponent screen — production (0.5, 2.0, 0.5, 3.0) vs neighbours")
    print("=" * 90)
    grid = [
        ('production',            (0.5, 2.0, 0.5, 3.0)),
        ('φ_eff exp 0.4',         (0.4, 2.0, 0.5, 3.0)),
        ('φ_eff exp 0.6',         (0.6, 2.0, 0.5, 3.0)),
        ('CN exp 1.8',            (0.5, 1.8, 0.5, 3.0)),
        ('CN exp 2.2',            (0.5, 2.2, 0.5, 3.0)),
        ('cov exp 0.4',           (0.5, 2.0, 0.4, 3.0)),
        ('cov exp 0.6',           (0.5, 2.0, 0.6, 3.0)),
        ('f_p exp 2.0',           (0.5, 2.0, 0.5, 2.0)),
        ('f_p exp 2.5',           (0.5, 2.0, 0.5, 2.5)),
        ('f_p exp 3.5',           (0.5, 2.0, 0.5, 3.5)),
        ('f_p exp 4.0',           (0.5, 2.0, 0.5, 4.0)),
        ('tight all (.4,1.8,.4,2.5)', (0.4, 1.8, 0.4, 2.5)),
        ('loose all (.6,2.2,.6,3.5)', (0.6, 2.2, 0.6, 3.5)),
    ]
    print(f"   {'variant':40s} {'LOOCV':>7s} {'Δ vs prod':>10s} {'AIC':>8s}")
    for tag, (ep, ec, ec2, ef) in grid:
        b = base_log_general(a, e_phi=ep, e_cn=ec, e_cov=ec2, e_fp=ef) + np.log(cf)
        lo, sse, k = _loocv_const_blend(b, logsf, taus, 6)
        aic, _ = _aic_bic(sse, n, k)
        d = lo - lo_prod
        flag = "  ★" if d > se else ("  ⚠" if d < -se else "")
        print(f"   {tag:40s} {lo:7.4f} {d:+10.4f} {aic:+8.2f}{flag}")

    # Q2. PERCOLATION TERM MERGE
    print("\n" + "=" * 90)
    print("Q2. PERCOLATION merge:  (φ_eff)^.5·f_p³  →  one factor?")
    print("=" * 90)
    phi_arr, p_arr = a[:, 0], a[:, 6]
    g = _g010(p_arr)
    phic_e = (1-g)*PHICP_F + g*PHICS_F
    phi_eff = np.sqrt((phi_arr-phic_e)**2 + (DELTA_F*g)**2 + 1e-12)
    fp = a[:, 3]
    other = (np.log(SG) + 2.0*np.log(a[:, 1]) + 0.5*np.log(a[:, 2]))   # CN², cov^.5
    cn_term = 2.0*np.log(a[:, 1]); cov_term = 0.5*np.log(a[:, 2])
    bg = np.log(SG) + cn_term + cov_term + np.log(cf)
    cands_perc = [
        ('prod  (φ_eff)^.5·f_p³',        bg + 0.5*np.log(phi_eff) + 3.0*np.log(fp), 6),
        ('(φ_eff·f_p)^1',                bg + 1.0*np.log(phi_eff*fp), 6),
        ('(φ_eff·f_p)^1.5',              bg + 1.5*np.log(phi_eff*fp), 6),
        ('(φ_eff·f_p²)^1',               bg + np.log(phi_eff*fp**2), 6),
        ('(φ_eff·f_p²)^1.5',             bg + 1.5*np.log(phi_eff*fp**2), 6),
        ('(φ_eff)^.5·f_p²',              bg + 0.5*np.log(phi_eff) + 2.0*np.log(fp), 6),
        ('(φ_eff)^.7·f_p^2.5',           bg + 0.7*np.log(phi_eff) + 2.5*np.log(fp), 6),
    ]
    print(f"   {'variant':40s} {'LOOCV':>7s} {'Δ vs prod':>10s} {'AIC':>8s}")
    for tag, b, k in cands_perc:
        lo, sse, _ = _loocv_const_blend(b, logsf, taus, k)
        aic, _ = _aic_bic(sse, n, k)
        d = lo - lo_prod
        flag = "  ★" if d > se else ("  ⚠" if d < -se else "")
        print(f"   {tag:40s} {lo:7.4f} {d:+10.4f} {aic:+8.2f}{flag}")

    # Q3. NETWORK TERM MERGE
    print("\n" + "=" * 90)
    print("Q3. NETWORK merge:  CN²·cov^.5  →  one factor?")
    print("=" * 90)
    perc_term = 0.5*np.log(phi_eff) + 3.0*np.log(fp)
    bg2 = np.log(SG) + perc_term + np.log(cf)
    cn = a[:, 1]; cov = a[:, 2]
    cands_net = [
        ('prod  CN²·cov^.5',             bg2 + 2.0*np.log(cn) + 0.5*np.log(cov), 6),
        ('(CN·√cov)²',                   bg2 + 2.0*np.log(cn*np.sqrt(cov)), 6),
        ('(CN·cov)^1.5',                 bg2 + 1.5*np.log(cn*cov), 6),
        ('(CN²·cov)^1',                  bg2 + np.log(cn**2 * cov), 6),
        ('CN^1.8·cov^.6',                bg2 + 1.8*np.log(cn) + 0.6*np.log(cov), 6),
        ('CN^2.2·cov^.4',                bg2 + 2.2*np.log(cn) + 0.4*np.log(cov), 6),
        ('CN^2·cov^1   (cov linear)',    bg2 + 2.0*np.log(cn) + 1.0*np.log(cov), 6),
        ('CN²  only   (drop cov)',       bg2 + 2.0*np.log(cn), 6),
        ('cov^.5 only (drop CN)',        bg2 + 0.5*np.log(cov), 6),
    ]
    print(f"   {'variant':40s} {'LOOCV':>7s} {'Δ vs prod':>10s} {'AIC':>8s}")
    for tag, b, k in cands_net:
        lo, sse, _ = _loocv_const_blend(b, logsf, taus, k)
        aic, _ = _aic_bic(sse, n, k)
        d = lo - lo_prod
        flag = "  ★" if d > se else ("  ⚠" if d < -se else "")
        print(f"   {tag:40s} {lo:7.4f} {d:+10.4f} {aic:+8.2f}{flag}")

    # Q4. C_blend SIMPLIFICATION
    print("\n" + "=" * 90)
    print("Q4. C_blend(τ) simplification — fewer params, same LOOCV?")
    print("=" * 90)
    base_full = base_log_general(a) + np.log(cf)
    cands_blend = [
        ('prod  dual-branch (6 params)',   'full',     6),
        ('constant only      (1 param)',   'const',    1),
        ('τ^-α               (2 params)',  'pow_tau',  2),
        ('Bruggeman 1/τ²    (1 param)',    'inv_tau2', 1),
        ('logpoly2 a+b·lτ+c·lτ² (3)',      'logpoly2', 3),
        ('logpoly3 cubic     (4 params)',  'logpoly3', 4),
    ]
    print(f"   {'variant':40s} {'LOOCV':>7s} {'Δ vs prod':>10s} {'AIC':>8s} {'BIC':>8s}")
    for tag, kind, _ in cands_blend:
        if kind == 'full':
            lo, sse, k = _loocv_const_blend(base_full, logsf, taus, 6)
        else:
            lo, sse, k = _loocv_simpler_blend(base_full, logsf, taus, kind)
        aic, bic = _aic_bic(sse, n, k)
        d = lo - lo_prod
        flag = "  ★" if d > se else ("  ⚠" if d < -se else "")
        print(f"   {tag:40s} {lo:7.4f} {d:+10.4f} {aic:+8.2f} {bic:+8.2f}{flag}")

    # Q5. δ-saturation removal
    print("\n" + "=" * 90)
    print("Q5. δ-saturation removal — does φ_eff still need rounding?")
    print("=" * 90)
    cands_delta = [
        ('prod  δ=0.040',  0.040),
        ('δ=0.020',        0.020),
        ('δ=0.000 (sharp)', 0.000),
        ('δ=0.060',        0.060),
        ('δ=0.080',        0.080),
    ]
    print(f"   {'variant':40s} {'LOOCV':>7s} {'Δ vs prod':>10s} {'AIC':>8s}")
    for tag, dl in cands_delta:
        b = base_log_general(a, delta=dl) + np.log(cf)
        lo, sse, k = _loocv_const_blend(b, logsf, taus, 6)
        aic, _ = _aic_bic(sse, n, k)
        d = lo - lo_prod
        flag = "  ★" if d > se else ("  ⚠" if d < -se else "")
        print(f"   {tag:40s} {lo:7.4f} {d:+10.4f} {aic:+8.2f}{flag}")

    print("\n" + "=" * 90)
    print("DECISION RULE for adoption of a simpler form:")
    print(f"  • LOOCV within ±{se:.4f} (noise SE) of prod  AND  AIC better → ADOPT")
    print(f"  • LOOCV equal or better, AIC slightly worse           → CONSIDER")
    print(f"  • LOOCV worse by > SE                                  → REJECT")


if __name__ == "__main__":
    main()
