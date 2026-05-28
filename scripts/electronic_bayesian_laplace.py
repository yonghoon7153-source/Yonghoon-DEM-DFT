#!/usr/bin/env python3
"""Bayesian Laplace posterior for σ_electronic Stage 4 form.

Mirrors scripts/bayesian_laplace.py for σ_ionic, with the electronic
form's 8 coefficients instead of 5.

Stage 4 σ_electronic form (post phantom + fallback + top-5 outlier filter):
   log σ_e = log σ_AM + a·log φ_AM + d·log f_p_e
             + β_P·p_amp + β_r·log r̄_AM + β_T·log(T/d_AM)
             + p + q·ln τ + r·(ln τ)²

PHYSICS PRIORS (informative, weakly regularizing):
   a (φ_AM)   ~ N(2.5, 1.0²)     intermediate Bruggeman-ish (literature 1.5-3.5)
   d (f_p_e)  ~ N(2.0, 1.0²)     between σ_ionic 3 and Bruggeman 1
   β_P        ~ N(-0.5, 0.3²)    AM_P (single-crystal NCM) σ ≈ AM_S × 0.5
                                  per Stage 3 data fit (-0.6 to -0.2)
   β_r        ~ N(-0.5, 0.3²)    Trevisanello-like size effect:
                                  larger AM → lower σ (size-dep GB density)
   β_T        ~ N(-0.4, 0.2²)    thin-electrode geometric penalty
   a, b, c    ~ N(0, 1²)         logpoly2 weak priors

For approximately Gaussian posteriors (which OLS + Gaussian priors give),
Laplace matches MCMC within a few percent.  Closed form — no PyMC needed.

PER-CASE PREDICTION INTERVAL: same approach as σ_ionic Bayesian script.

Run on WSL:
    python3 scripts/electronic_bayesian_laplace.py
"""
from __future__ import annotations
import sys, json
from pathlib import Path
import numpy as np

SCRIPTS = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS))

from electronic_nested_cv import load_corpus_e, SIGMA_AM


# Prior means + stds for the 8 coefficients
# Order: [a (φ_AM), d (f_p_e), β_P, β_r, β_T, p, q, r]
PRIOR_MEAN = np.array([2.5, 2.0, -0.5, -0.5, -0.4, 0.0, 0.0, 0.0])
PRIOR_STD  = np.array([1.0, 1.0,  0.3,  0.3,  0.2, 1.0, 1.0, 1.0])
PRIOR_LABELS = ['a (φ_AM)', 'd (f_p_e)', 'β_P (p_amp)',
                'β_r (log r̄_AM)', 'β_T (log T/d_AM)',
                'p (const)', 'q (ln τ)', 'r (ln²τ)']


def build_design_matrix(a_array):
    """X for Stage 4 form, returns (X, y_target) where
       y_target = log σ_DEM − log σ_AM."""
    phi_am = a_array[:, 0]; fp = a_array[:, 3]; tau = a_array[:, 4]
    p_amp = a_array[:, 6]
    r_AM_S = a_array[:, 8]; r_AM_P = a_array[:, 9]; T_um = a_array[:, 10]
    r_eff = np.where(np.isfinite(r_AM_S), r_AM_S, 2.5)
    r_eff_P = np.where(np.isfinite(r_AM_P), r_AM_P, 5.5)
    r_eff = (1.0 - p_amp)*r_eff + p_amp*r_eff_P
    T_safe = np.where(np.isfinite(T_um) & (T_um > 0), T_um, 100.0)
    d_AM = 2.0 * r_eff
    log_r = np.log(np.maximum(r_eff, 0.5))
    log_Td = np.log(np.maximum(T_safe / d_AM, 0.1))
    lt = np.log(tau)
    X = np.column_stack([
        np.log(phi_am),  # a
        np.log(fp),       # d
        p_amp,            # β_P
        log_r,            # β_r
        log_Td,           # β_T
        np.ones(len(tau)),# p
        lt,               # q
        lt**2,            # r
    ])
    return X


def map_and_laplace(X, y, prior_mean, prior_std, sigma_residual):
    """Closed-form Laplace = exact posterior for Gaussian-Gaussian."""
    n, k = X.shape
    Lambda_prior = np.diag(1.0 / prior_std**2)
    P_post = X.T @ X / sigma_residual**2 + Lambda_prior
    Sigma_post = np.linalg.inv(P_post)
    rhs = X.T @ y / sigma_residual**2 + Lambda_prior @ prior_mean
    b_MAP = Sigma_post @ rhs
    return b_MAP, Sigma_post


def sample_posterior(b_MAP, Sigma_post, n_samples=2000, seed=42):
    rng = np.random.default_rng(seed)
    return rng.multivariate_normal(b_MAP, Sigma_post, size=n_samples)


def main():
    print("=" * 78)
    print(" BAYESIAN LAPLACE — σ_electronic Stage 4 form with physics priors")
    print("=" * 78)
    a, names = load_corpus_e()
    n = len(a)
    if n < 8:
        print("[ABORT] corpus too small."); return
    logsf = np.log(a[:, 5])
    print(f"  Corpus n = {n}, k = 8 (Stage 4 form)")

    # OLS baseline (no prior — for reference)
    X = build_design_matrix(a)
    y = logsf - np.log(SIGMA_AM)
    b_ols, *_ = np.linalg.lstsq(X, y, rcond=None)
    pred_ols = X @ b_ols
    resid = y - pred_ols
    sigma_res = float(np.sqrt(np.sum(resid**2) / (n - 8)))
    print(f"  OLS residual SE (log-space) = {sigma_res:.4f}")
    print()

    # Laplace MAP
    b_map, S_post = map_and_laplace(X, y, PRIOR_MEAN, PRIOR_STD, sigma_res)
    se_post = np.sqrt(np.diag(S_post))

    print("─" * 78)
    print(" Coefficient comparison: OLS vs MAP (Laplace)")
    print("─" * 78)
    print(f"  {'coef':22s}  {'OLS':>9s}  {'MAP':>9s}  {'post SE':>9s}  "
          f"{'prior μ':>9s}  {'prior σ':>9s}  shrinkage")
    for i, nm in enumerate(PRIOR_LABELS):
        shrink = (b_ols[i] - b_map[i]) / max(abs(b_ols[i]), 1e-6) * 100
        print(f"  {nm:22s}  {b_ols[i]:+9.3f}  {b_map[i]:+9.3f}  {se_post[i]:9.4f}  "
              f"{PRIOR_MEAN[i]:+9.3f}  {PRIOR_STD[i]:9.3f}  {shrink:+6.1f}%")
    print()

    # Posterior samples → per-case predictive distribution
    samples = sample_posterior(b_map, S_post, n_samples=2000)
    base = np.log(SIGMA_AM)
    pred_logs = (X[np.newaxis, :, :] * samples[:, np.newaxis, :]).sum(axis=2) + base
    pred_med = np.median(pred_logs, axis=0)
    pred_lo90 = np.quantile(pred_logs, 0.05, axis=0)
    pred_hi90 = np.quantile(pred_logs, 0.95, axis=0)
    pi_lo = pred_lo90 - 1.645 * sigma_res
    pi_hi = pred_hi90 + 1.645 * sigma_res

    err_pct = (np.exp(pred_med) - np.exp(logsf)) / np.exp(logsf) * 100
    in_pi = (logsf >= pi_lo) & (logsf <= pi_hi)
    cov_pct = 100 * in_pi.mean()
    print(f"  Empirical 90% PI coverage: {cov_pct:.1f}%  (target 90%)")
    if cov_pct < 85:
        print(f"    → PI too tight; residuals under-estimated.")
    elif cov_pct > 95:
        print(f"    → PI too wide; over-regularized.")
    else:
        print(f"    → PI is well-calibrated.")
    print()

    print("─" * 78)
    print(" Per-outlier honest interval check (|err|>20% on σ_DEM)")
    print("─" * 78)
    print(f"  {'case':32s}  {'σ_DEM':>7s}  {'σ_form':>7s}  "
          f"{'lo90%':>7s}  {'hi90%':>7s}  {'err%':>6s}  verdict")
    out_idx = np.where(np.abs(err_pct) > 20)[0]
    n_in, n_out = 0, 0
    for i in sorted(out_idx, key=lambda j: -abs(err_pct[j])):
        nm = names[i] if i < len(names) else f"(idx{i})"
        s_dem = float(a[i, 5])
        s_form = float(np.exp(pred_med[i]))
        lo = float(np.exp(pi_lo[i])); hi = float(np.exp(pi_hi[i]))
        in_p = (s_dem >= lo and s_dem <= hi)
        verdict = "INSIDE PI" if in_p else "OUTSIDE PI"
        if in_p: n_in += 1
        else: n_out += 1
        print(f"  {nm[:32]:32s}  {s_dem:7.4f}  {s_form:7.4f}  "
              f"{lo:7.4f}  {hi:7.4f}  {err_pct[i]:+6.1f}  {verdict}")
    print()
    print(f"  |err|>20% outliers: {n_in} INSIDE PI, {n_out} OUTSIDE PI")
    if n_in > 0:
        print(f"    → {n_in} 'outliers' are within model's stated 90% PI.")
        print(f"      Form correctly says 'I'm uncertain here'.")
    if n_out > 0:
        print(f"    → {n_out} are GENUINE model failures (outside even the honest PI).")
        print(f"      These need new data or upstream solver fix.")


if __name__ == '__main__':
    main()
