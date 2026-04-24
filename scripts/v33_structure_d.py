#!/usr/bin/env python3
"""
v33 Structure D — fresh scaling-law form with DIVISION corrections.

Motivation: v32's multiplicative exp(correction) form over-corrects
well-fit cases (input_1mAh_1: v29 err 7% → v32 err 22%). Structural
limitation of the correction form, not parameter values. Dispose of
v29's sigmoid-blend inheritance entirely; rebuild from Kirkpatrick-
scaling core + four physics-motivated Θ factors.

Proposed form (σ in mS/cm):
    σ  =  A · σ_grain · (φ − φc)^α · CN^β · cov^γ · f_p^δ
          ────────────────────────────────────────────────
          (1 + λ_thin · w_thin)  ·  (1 + λ_PSD · CV_r)
          × exp(κ · max(p50_δR − 0.20, 0))

where
    w_thin   = exp(−T / T_char)           (thin-regime indicator)
    CV_r     = std(r_AM) / mean(r_AM)      (bimodal dispersity)
    p50_δR   = median δ/R*                 (from physics_regime_histogram)

Free parameters (11 total):
    {A, α, β, γ, δ, φc, λ_thin, T_char, λ_PSD, κ, (σ_grain fixed=3.0)}

Joint Nelder-Mead minimises − LOOCV in log-σ space.

Usage:
    python3 scripts/v33_structure_d.py
    python3 scripts/v33_structure_d.py --verbose
"""
from __future__ import annotations
import os, json, sys, argparse
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.optimize import minimize

SCRIPTS_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS_DIR))
# reuse loader from v32
from v32_exhaustive_refit import load_cases  # noqa: E402

WEBAPP = Path(__file__).parent.parent / 'webapp'
OUT = Path('docs/figures/physics_regime')
OUT.mkdir(parents=True, exist_ok=True)

SIGMA_GRAIN = 3.0  # mS/cm, LPSCl


# ─────────────────────────────────────────────────────────────
# Structure D prediction
# ─────────────────────────────────────────────────────────────
def predict_v33(df, params):
    """
    params tuple: (A, alpha, beta, gamma, delta, phi_c,
                   lam_thin, T_char, lam_PSD, kappa)
    """
    A, alpha, beta, gamma, delta, phi_c, lam_thin, T_char, lam_PSD, kappa = params

    phi_ex = np.maximum(df['phi'].values - phi_c, 1e-4)
    cn = np.maximum(df['cn'].values, 1e-4)
    cov = np.maximum(df['cov'].values, 1e-4)
    fp = np.maximum(df['f_perc'].values, 1e-4)
    T = np.maximum(df['thick'].values, 1.0)
    p50_dr = df['p50_dr'].values

    # r_AM dispersity CV (already computed in loader as a field? compute here if not)
    r_p = df['r_AM_P'].fillna(np.nan).values
    r_s = df['r_AM_S'].fillna(np.nan).values
    cv_r = np.zeros(len(df))
    for i, (p, s) in enumerate(zip(r_p, r_s)):
        if p and s and not np.isnan(p) and not np.isnan(s):
            m = (p + s) / 2
            cv_r[i] = abs(p - s) / (2 * m) if m > 0 else 0.0

    # Kirkpatrick core
    core = A * SIGMA_GRAIN * phi_ex**alpha * cn**beta * cov**gamma * fp**delta

    # Division corrections
    w_thin = np.exp(-T / T_char)
    denom_thin = 1.0 + lam_thin * w_thin
    denom_PSD = 1.0 + lam_PSD * cv_r

    # Plastic correction (rectified exp)
    plastic_excess = np.maximum(p50_dr - 0.20, 0.0)
    plastic_factor = np.exp(kappa * plastic_excess)

    sigma = core / denom_thin / denom_PSD * plastic_factor
    return np.maximum(sigma, 1e-8)


def r2_log(actual, predicted):
    la, lp = np.log(actual), np.log(predicted)
    return 1 - np.sum((la - lp) ** 2) / np.sum((la - np.mean(la)) ** 2)


def loocv_log(df, params_fn, optimizer_fn, x0):
    actual = df['sigma_actual'].values
    la = np.log(actual)
    ss_tot = np.sum((la - np.mean(la)) ** 2)
    n = len(df)
    sse = 0.0
    for i in range(n):
        mask = np.ones(n, bool); mask[i] = False
        df_fold = df.iloc[mask].reset_index(drop=True)
        res = optimizer_fn(df_fold, x0)
        pred_i = params_fn(df.iloc[[i]].reset_index(drop=True), res.x)[0]
        sse += (la[i] - np.log(max(pred_i, 1e-8))) ** 2
    return 1 - sse / ss_tot


# ─────────────────────────────────────────────────────────────
# Fit machinery
# ─────────────────────────────────────────────────────────────
def neg_r2_loss(params, df):
    """Negative R² in log space — scipy minimises."""
    try:
        pred = predict_v33(df, params)
    except Exception:
        return 1e6
    if not np.all(np.isfinite(pred)):
        return 1e6
    return -r2_log(df['sigma_actual'].values, pred)


def fit_v33(df, x0, bounds):
    # Nelder-Mead ignores bounds, but we enforce them via penalty
    def loss(params):
        for i, (val, (lo, hi)) in enumerate(zip(params, bounds)):
            if val < lo or val > hi:
                return 1e6
        return neg_r2_loss(params, df)
    res = minimize(loss, x0=x0, method='Nelder-Mead',
                   options={'xatol': 1e-4, 'fatol': 1e-6,
                            'maxiter': 4000, 'adaptive': True})
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--verbose', action='store_true')
    args = ap.parse_args()

    rows = load_cases()
    df = pd.DataFrame(rows)
    print(f"Loaded {len(df)} cases\n")

    # Initial guess + bounds
    # (A, α, β, γ, δ, φc, λ_thin, T_char, λ_PSD, κ)
    x0 = [0.20, 0.5, 1.5, 0.4, 3.0, 0.20, 0.50, 30.0, 0.30, 2.0]
    bounds = [
        (0.01, 5.0),     # A
        (0.1, 2.0),      # α (phi exponent)
        (0.1, 3.5),      # β (CN exponent)
        (-0.5, 2.0),     # γ (cov exponent)
        (0.1, 5.0),      # δ (f_p exponent)
        (0.05, 0.30),    # φc
        (-2.0, 5.0),     # λ_thin (division strength)
        (5.0, 200.0),    # T_char (thickness scale)
        (-1.0, 3.0),     # λ_PSD
        (-5.0, 5.0),     # κ (plastic excess)
    ]
    param_names = ['A', 'α', 'β', 'γ', 'δ', 'φc', 'λ_thin', 'T_char', 'λ_PSD', 'κ']

    print("=== v33 Structure D: joint Nelder-Mead fit (R² loss) ===")
    res = fit_v33(df, x0, bounds)
    best = res.x
    pred = predict_v33(df, best)
    r2 = r2_log(df['sigma_actual'].values, pred)
    err = np.abs(pred - df['sigma_actual'].values) / df['sigma_actual'].values
    w20 = int(np.sum(err < 0.20))

    print(f"\nFitted parameters:")
    for n, v in zip(param_names, best):
        print(f"  {n:8s}  = {v:.4f}")
    print(f"\nFit stats:")
    print(f"  R² (log)   = {r2:.4f}")
    print(f"  ±20% band  = {w20}/{len(df)}")
    print(f"  |err| median = {np.median(err)*100:.1f}%")
    print(f"  |err| mean   = {np.mean(err)*100:.1f}%")

    # LOOCV (expensive — 60 refits)
    print(f"\nComputing LOOCV (60 refits)...")
    la = np.log(df['sigma_actual'].values)
    ss_tot = np.sum((la - np.mean(la)) ** 2)
    sse_loo = 0.0
    for i in range(len(df)):
        mask = np.ones(len(df), bool); mask[i] = False
        df_fold = df.iloc[mask].reset_index(drop=True)
        res_f = fit_v33(df_fold, best, bounds)
        pred_i = predict_v33(df.iloc[[i]].reset_index(drop=True), res_f.x)[0]
        sse_loo += (la[i] - np.log(max(pred_i, 1e-8))) ** 2
        if args.verbose and (i + 1) % 10 == 0:
            print(f"  LOOCV fold {i+1}/{len(df)} done")
    loocv = 1 - sse_loo / ss_tot
    print(f"\n  LOOCV (log) = {loocv:.4f}")

    # Per-case output
    df['sigma_pred_v33'] = pred
    df['err_pct'] = 100 * (pred - df['sigma_actual']) / df['sigma_actual']
    df['abs_err_pct'] = df['err_pct'].abs()
    out_csv = OUT / 'v33_best_per_case.csv'
    df.sort_values('abs_err_pct', ascending=False).to_csv(out_csv, index=False)
    print(f"\n→ {out_csv}")

    # Top-10 outliers
    print(f"\n=== Top-10 residual outliers ===")
    for _, r in df.nlargest(10, 'abs_err_pct').iterrows():
        print(f"  {r['name']:30s}  σ_act={r['sigma_actual']:.4f}  "
              f"σ_pred={r['sigma_pred_v33']:.4f}  err={r['err_pct']:+.1f}%")

    # Save fitted params
    fit_json = OUT / 'v33_fitted_params.json'
    fit_json.write_text(json.dumps({
        'params': dict(zip(param_names, [float(v) for v in best])),
        'r2_log': float(r2),
        'loocv_log': float(loocv),
        'band_20pct': f"{w20}/{len(df)}",
        'median_err_pct': float(np.median(err) * 100),
    }, indent=2))
    print(f"→ {fit_json}")


if __name__ == '__main__':
    main()
