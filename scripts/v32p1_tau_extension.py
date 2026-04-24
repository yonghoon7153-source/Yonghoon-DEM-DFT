#!/usr/bin/env python3
"""v32.1 proposal — add a τ-interaction term to close the thin-film
under-prediction identified by residual_diagnostic.py.

Current v32 (4-term, R²=0.985, std(err)=19.4%, 49/61 within ±20%):
  σ_v32 = v29 × exp( γ1·LIGG_LB + γ2·THIN_X_GEOM + γ3·P50_DR_DEV + γ4·PSD_RATIO )

v32.1 candidates — add one τ-based term to the 4-term base:
  A) + γ5·TAU_DIJ       = (τ_Dij − 1.5)            # direct τ deviation
  B) + γ5·THIN_TAU      = w_thin · (τ − 1.5)       # thin × τ interaction
  C) + γ5·THIN_TAU_LOG  = w_thin · log(τ/1.3)      # thin × log(τ)
     (new — added to build_features via a light extension below)

For each candidate we JOINTLY refit all 5 γ's, report:
  - R², LOOCV, ±20% band count
  - 1mAh mean err% (should drop from +12.5%)
  - 1mAh_80:20 mean err% (should drop from +34.4%)
  - 6mAh mean err% (should rise from -13.9% toward 0)
  - γ values (stability check)

If one candidate clearly wins on multiple axes → that is v32.1. If not,
Methods Limitation note is the better path.

Usage:
  python3 scripts/v32p1_tau_extension.py
"""
from __future__ import annotations
import sys
from pathlib import Path
import numpy as np
import pandas as pd

SCRIPTS = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS))

from v32_exhaustive_refit import (  # noqa: E402
    load_cases, build_features, v29_predict_vec, fit_candidate, r2_log,
)
from generate_comparison_plots import _formx_v29_params  # noqa: E402


V32_BASE = ['LIGG_LB_PCT', 'THIN_X_GEOM', 'P50_DR_DEV', 'PSD_RATIO']
TAU_CANDIDATES = {
    'A_TAU_DIJ':     'TAU_DIJ',     # direct
    'B_THIN_TAU':    'THIN_TAU',    # thin × (τ-1.5)
}


def add_thin_tau_log(features, df):
    """Extend features dict with THIN_TAU_LOG = w_thin · log(τ/1.3)."""
    T = df['thick'].values
    tau = df['tau'].values
    T_c = 30.0
    w_thin = np.exp(-T / T_c)
    tau_ref = 1.3
    features['THIN_TAU_LOG'] = w_thin * np.log(np.maximum(tau / tau_ref, 1e-6))
    return features


def name_tags(df):
    """Derive case-type tags used for sub-group reporting."""
    tags = []
    for _, r in df.iterrows():
        n = (r['name'] or '').lower()
        t = {
            'is_1mAh':  '1mah' in n,
            'is_6mAh':  '6mah' in n,
            'is_8mAh':  '8mah' in n,
            'is_thin':  'thin' in n or r['thick'] < 25,
            'amse_is_80_20': False,  # filled below
        }
        tags.append(t)
    return tags


def err_pct(actual, pred):
    return (actual - pred) / pred * 100.0


def subgroup_mean(errs, mask):
    if mask.sum() == 0:
        return float('nan')
    return float(np.mean(errs[mask]))


def summarise(label, res, df, actual, errs_v32):
    pred = res['pred']
    errs = err_pct(actual, pred)

    n = len(actual)
    w20 = int(np.sum(np.abs(errs) < 20))

    # Sub-groups
    is_1mAh  = df['name'].str.lower().str.contains('1mah').values
    is_6mAh  = df['name'].str.lower().str.contains('6mah').values
    is_8mAh  = df['name'].str.lower().str.contains('8mah').values
    is_80_20_1mAh = is_1mAh & df['name'].str.lower().str.contains('80', regex=False).values

    print(f'\n--- {label} ---')
    print(f'  R²           : {res["r2"]:.4f}')
    print(f'  LOOCV R²     : {res["loocv"]:.4f}')
    print(f'  AIC          : {res["aic"]:.2f}')
    print(f'  |err|<20%    : {w20}/{n}')
    print(f'  std(err%)    : {np.std(errs):.2f}')
    print(f'  mean err%    : {np.mean(errs):+.2f}')
    print(f'  sub-group mean err%:')
    print(f'    1mAh       : {subgroup_mean(errs, is_1mAh):+.2f}  (was {subgroup_mean(errs_v32, is_1mAh):+.2f})')
    print(f'    6mAh       : {subgroup_mean(errs, is_6mAh):+.2f}  (was {subgroup_mean(errs_v32, is_6mAh):+.2f})')
    print(f'    8mAh       : {subgroup_mean(errs, is_8mAh):+.2f}  (was {subgroup_mean(errs_v32, is_8mAh):+.2f})')
    print(f'  γ values:')
    for fname, g in zip(res['features'], res['gammas']):
        print(f'    {fname:15s}: {g:+.3f}')


def main():
    # Load
    rows = load_cases()
    df = pd.DataFrame(rows)
    n = len(df)
    actual = df['sigma_actual'].values
    print(f'Loaded {n} cases')

    # Base v29 prediction + feature bank (extended with THIN_TAU_LOG)
    params = _formx_v29_params()
    base_pred = v29_predict_vec(df, params)
    features = build_features(df)
    features = add_thin_tau_log(features, df)

    # ── Reference: v32 (4-term) ───────────────────────────────────
    res_v32 = fit_candidate(df, V32_BASE, features, base_pred)
    errs_v32 = err_pct(actual, res_v32['pred'])
    print(f'\n=== BASELINE v32 (4-term) ===')
    summarise('v32 (4-term)', res_v32, df, actual, errs_v32)

    # ── v32.1 candidates: 4-term + 1 τ term (joint refit) ─────────
    print('\n' + '=' * 60)
    print('=== v32.1 CANDIDATES (5-term, joint refit) ===')
    print('=' * 60)

    candidates_ranked = []
    for label, tau_feat in {
        'A_TAU_DIJ':     'TAU_DIJ',
        'B_THIN_TAU':    'THIN_TAU',
        'C_THIN_TAU_LOG': 'THIN_TAU_LOG',
    }.items():
        res = fit_candidate(df, V32_BASE + [tau_feat], features, base_pred)
        candidates_ranked.append((label, tau_feat, res))
        summarise(f'v32.1 [{label}]', res, df, actual, errs_v32)

    # ── Ranking ────────────────────────────────────────────────────
    print('\n' + '=' * 60)
    print('=== RANKING ===')
    print(f'{"candidate":20s}  {"R²":>7s}  {"LOOCV":>7s}  {"AIC":>8s}  {"w20":>4s}  {"std%":>6s}')
    print(f'{"v32 (baseline)":20s}  {res_v32["r2"]:7.4f}  {res_v32["loocv"]:7.4f}  '
          f'{res_v32["aic"]:8.2f}  {res_v32["w20"]:>4d}  {np.std(errs_v32):6.2f}')
    for label, feat, res in candidates_ranked:
        errs = err_pct(actual, res['pred'])
        print(f'{label:20s}  {res["r2"]:7.4f}  {res["loocv"]:7.4f}  '
              f'{res["aic"]:8.2f}  {res["w20"]:>4d}  {np.std(errs):6.2f}')

    # ── Verdict ────────────────────────────────────────────────────
    best = max(candidates_ranked, key=lambda x: x[2]['loocv'])
    label, feat, res = best
    dR2 = res['r2'] - res_v32['r2']
    dLOOCV = res['loocv'] - res_v32['loocv']
    dAIC = res['aic'] - res_v32['aic']  # negative = better
    dw20 = res['w20'] - res_v32['w20']

    print('\n=== VERDICT ===')
    print(f'  Best τ extension: {label}  (+{feat})')
    print(f'    ΔR²     = {dR2:+.4f}')
    print(f'    ΔLOOCV  = {dLOOCV:+.4f}  ({"↑ improved" if dLOOCV>0 else "↓ WORSE"})')
    print(f'    ΔAIC    = {dAIC:+.2f}     ({"↓ improved" if dAIC<0 else "↑ WORSE"})')
    print(f'    Δw20    = {dw20:+d}')

    # Decision thresholds
    if dLOOCV > 0.003 and dAIC < 0 and dw20 >= 2:
        print(f'\n  → ADOPT v32.1 with +{feat}. Material improvement on robust metrics.')
    elif dLOOCV > 0 and dAIC < 0:
        print(f'\n  → MARGINAL improvement. Consider reporting as sensitivity-only '
              f'(not a new primary form).')
    else:
        print(f'\n  → DO NOT ADOPT. Extension does not improve LOOCV meaningfully. '
              f'Recommend Methods Limitation note instead.')


if __name__ == '__main__':
    main()
