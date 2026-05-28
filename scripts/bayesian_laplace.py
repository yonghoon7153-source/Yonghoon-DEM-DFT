#!/usr/bin/env python3
"""Bayesian inference (Laplace approximation) for the T1 production form's
5 coefficients (a, b, c, β_P2, β_F), with physics-motivated priors.

WHY THIS, NOT PyMC?
-------------------
The cloud container doesn't have PyMC/Stan.  Laplace approximation is a
standard alternative that:
  1. finds the MAP estimate (= OLS posterior mode for Gaussian likelihood)
  2. computes the Hessian of the negative log-posterior at the MAP
  3. inverts the Hessian to get the posterior covariance matrix
  4. samples from MVN(MAP, Σ) → approximate posterior samples

For roughly Gaussian posteriors (which OLS+normal-prior gives), Laplace
matches full MCMC to within a few %.

PHYSICS PRIORS (informative, weakly regularizing)
-------------------------------------------------
  a, b, c       — C_blend logpoly2 coefficients.  Weak N(0, 1²) prior since
                  these are data-driven τ-corrections with no physics anchor.
  β_P2          — Cronau super-µm arm strength.  Prior N(3.5, 1.5²) — empirically
                  fit was +3.45, and the physical mechanism (Cronau extension
                  beyond 0.5µm plateau) bounds this loosely.
  β_F           — fracture-aware Holm partial-conduction exponent.  Prior
                  N(0.19, 0.05²) — literature partial-Holm ratio ≈ 60% retained
                  conduction at broken contacts → log-exponent ≈ 0.19.

PER-CASE PREDICTION INTERVAL
----------------------------
For each case i, sample b from posterior → predict σ_i → percentiles give
the prediction interval, naturally widening for cases the form is uncertain
about (extrapolation, near-threshold, sparse-design).

DIAGNOSTIC OUTPUT
-----------------
  • MAP vs OLS coefficient comparison (priors pull MAP slightly)
  • posterior std per coefficient
  • per-outlier ±90% interval — answers "is this outlier really outside the
    model's stated uncertainty?"

Run on WSL:
    python3 scripts/bayesian_laplace.py
"""
from __future__ import annotations
import sys, json
from pathlib import Path
import numpy as np

SCRIPTS = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS))

from nested_cv_sat import (load_corpus, base_log_sat, cronau_factor,
                           cblend_fit, cblend_pred, _g_phys_smooth,
                           _meta_name, _EXCLUDED_NAMES, PHIC_PROD,
                           PHICP_F, PHICS_F, DELTA_F, PHI_C0)
import generate_comparison_plots as gcp


PRIOR_MEAN  = np.array([0.0, 0.0, 0.0, 3.5, 0.19])  # a, b, c, β_P2, β_F
PRIOR_STD   = np.array([1.0, 1.0, 1.0, 1.5, 0.05])  # weak / weak / weak / moderate / tight


def p2_feat(a, g):
    phi = a[:, 0]; r = a[:, 8]
    pex = np.maximum(phi - PHIC_PROD, 0.0)
    rs = np.where(np.isfinite(r) & (r > 0), r, 0.5)
    return g * pex**2 * np.maximum(rs - 0.5, 0.0)


def build_design_matrix(base, taus, extras):
    """X such that pred_log = base + X @ b, b length = 3 + len(extras)."""
    lt = np.log(taus)
    cols = [np.ones(len(taus)), lt, lt**2]
    for e in extras:
        cols.append(np.asarray(e))
    return np.column_stack(cols)


def map_and_laplace(base, logsf, X, prior_mean, prior_std, sigma_residual):
    """MAP + Laplace covariance for Gaussian likelihood + Gaussian prior.
    The posterior is exactly MVN for this case → Laplace is exact.

    Returns (b_MAP, Sigma_posterior, marginal_log_likelihood).
    """
    y = logsf - base
    n, k = X.shape
    Lambda_prior = np.diag(1.0 / prior_std**2)        # precision
    # Posterior precision: X^T X / σ² + Λ_prior
    P_post = X.T @ X / sigma_residual**2 + Lambda_prior
    # Posterior mean: P_post^-1 (X^T y / σ² + Λ_prior μ_prior)
    Sigma_post = np.linalg.inv(P_post)
    rhs = X.T @ y / sigma_residual**2 + Lambda_prior @ prior_mean
    b_MAP = Sigma_post @ rhs
    return b_MAP, Sigma_post


def sample_posterior(b_MAP, Sigma_post, n_samples=2000, seed=42):
    rng = np.random.default_rng(seed)
    return rng.multivariate_normal(b_MAP, Sigma_post, size=n_samples)


def case_names(n_target):
    names = []
    seen = set()
    for base in ('webapp/results', 'webapp/archive'):
        bp = Path(base)
        if not bp.is_dir():
            continue
        for mp in bp.rglob('full_metrics.json'):
            try: d = json.load(open(mp))
            except Exception: continue
            sig = gcp._stage_e_sigma(d)
            phi = gcp._get(d, 'phi_se'); cn = gcp._get(d, 'se_se_cn')
            cov = gcp._cov_frac(d, physics=False) or gcp._cov_frac(d, physics=True)
            fp = gcp._get(d, 'percolation_pct') / 100.0
            tau = gcp._get(d, 'tortuosity_recommended', gcp._get(d, 'tortuosity_mean', 0))
            if not (sig and sig > 0 and phi > PHI_C0 and cn > 0 and cov and cov > 0
                    and fp > 0 and tau > 0):
                continue
            nm = _meta_name(mp.parent.name, mp.parent)
            if nm in _EXCLUDED_NAMES: continue
            key = (round(phi, 4), round(cn, 3), round(float(sig), 5))
            if key in seen: continue
            seen.add(key); names.append(nm)
            if len(names) == n_target: break
    return names


def main():
    print("=" * 78)
    print(" BAYESIAN LAPLACE — T1 form coefficients with physics priors")
    print("=" * 78)
    a = load_corpus()
    n = len(a)
    if n < 8 or a.ndim < 2:
        print("[ABORT] corpus too small."); return
    logsf = np.log(a[:, 5]); taus = a[:, 4]
    g = _g_phys_smooth(a); fi = a[:, 19] if a.shape[1] >= 20 else np.zeros(n)
    base = base_log_sat(a, PHICP_F, PHICS_F, DELTA_F) + np.log(cronau_factor(a[:, 8]))
    extras = [p2_feat(a, g), fi]

    # OLS baseline
    b_ols = cblend_fit(base, logsf, taus, extras=extras)
    pred_ols = cblend_pred(base, taus, b_ols, extras=extras)
    resid_ols = logsf - pred_ols
    sigma_res = float(np.sqrt(np.sum(resid_ols**2) / (n - 5)))
    print(f"  Corpus n = {n}, k = 5 (a,b,c,β_P2,β_F)")
    print(f"  OLS residual SE (log-space) = {sigma_res:.4f}")
    print()

    # Laplace MAP
    X = build_design_matrix(base, taus, extras)
    b_map, S_post = map_and_laplace(base, logsf, X, PRIOR_MEAN, PRIOR_STD, sigma_res)
    se_post = np.sqrt(np.diag(S_post))

    print("─" * 78)
    print(" Coefficient comparison: OLS vs MAP (Laplace)")
    print("─" * 78)
    names_coef = ['a (logpoly2 const)', 'b (log τ)', 'c (log² τ)', 'β_P2', 'β_F']
    print(f"  {'coef':24s}  {'OLS':>9s}  {'MAP':>9s}  {'post SE':>9s}  "
          f"{'prior μ':>9s}  {'prior σ':>9s}  shrinkage")
    for i, nm in enumerate(names_coef):
        shrink = (b_ols[i] - b_map[i]) / max(abs(b_ols[i]), 1e-6) * 100
        print(f"  {nm:24s}  {b_ols[i]:+9.3f}  {b_map[i]:+9.3f}  {se_post[i]:9.4f}  "
              f"{PRIOR_MEAN[i]:+9.3f}  {PRIOR_STD[i]:9.3f}  {shrink:+6.1f}%")
    print()

    # Posterior samples
    samples = sample_posterior(b_map, S_post, n_samples=2000)
    # Predictive distribution per case
    pred_logs = (X[np.newaxis, :, :] * samples[:, np.newaxis, :]).sum(axis=2) + base
    pred_med = np.median(pred_logs, axis=0)
    pred_lo90 = np.quantile(pred_logs, 0.05, axis=0)
    pred_hi90 = np.quantile(pred_logs, 0.95, axis=0)
    # Add aleatoric noise to PI
    pi_lo = pred_lo90 - 1.645 * sigma_res
    pi_hi = pred_hi90 + 1.645 * sigma_res

    # Per-outlier honest interval check
    err_pct = (np.exp(pred_med) - np.exp(logsf)) / np.exp(logsf) * 100
    in_pi = (logsf >= pi_lo) & (logsf <= pi_hi)
    cov_pct = 100 * in_pi.mean()
    print(f"  Empirical 90% PI coverage: {cov_pct:.1f}%  (target 90%)")
    if cov_pct < 85:
        print(f"    → PI is too tight; residuals are under-estimated.")
    elif cov_pct > 95:
        print(f"    → PI is too wide; over-regularized or residual SE too large.")
    else:
        print(f"    → PI is well-calibrated.")
    print()

    print("─" * 78)
    print(" Per-outlier honest interval check (|err|>15% on σ_DEM)")
    print("─" * 78)
    names = case_names(n)
    print(f"  {'case':32s}  {'σ_DEM':>7s}  {'σ_form':>8s}  "
          f"{'lo90%':>7s}  {'hi90%':>7s}  {'err%':>6s}  {'verdict':s}")
    out_idx = np.where(np.abs(err_pct) > 15)[0]
    n_in_pi, n_out_pi = 0, 0
    for i in sorted(out_idx, key=lambda j: -abs(err_pct[j])):
        nm = names[i] if i < len(names) else f"(idx{i})"
        s_dem = float(a[i, 5])
        s_form = float(np.exp(pred_med[i]))
        lo = float(np.exp(pi_lo[i])); hi = float(np.exp(pi_hi[i]))
        in_p = (s_dem >= lo and s_dem <= hi)
        if in_p:
            verdict = "INSIDE PI — model uncertainty already captures this"
            n_in_pi += 1
        else:
            verdict = "OUTSIDE PI — genuine model failure"
            n_out_pi += 1
        print(f"  {nm[:32]:32s}  {s_dem:7.4f}  {s_form:8.4f}  "
              f"{lo:7.4f}  {hi:7.4f}  {err_pct[i]:+6.1f}  {verdict}")
    print()
    print(f"  Summary of |err|>15% outliers: {n_in_pi} inside PI, {n_out_pi} outside PI")
    if n_in_pi > 0:
        print(f"    → {n_in_pi} 'outliers' are ALREADY within model's stated 90% uncertainty.")
        print(f"      These shouldn't be called outliers in the dashboard — they're cases")
        print(f"      where the form correctly says 'I'm not sure'.")
    if n_out_pi > 0:
        print(f"    → {n_out_pi} are GENUINE form failures (outside even the honest PI).")


if __name__ == '__main__':
    main()
