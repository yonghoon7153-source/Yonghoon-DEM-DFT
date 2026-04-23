#!/usr/bin/env python3
"""Dump EVERY P:S=7:3 case with v32 residual, unfiltered by name/amse.

The earlier 1mAh_80:20 tracker missed most of the outliers the plot
shows because load_cases() applies phi>0.20 filter AND the 'name'-
based regex 'thin|1mah' may miss cases whose meta-name differs.

This script:
  1. Loads cases via v32_exhaustive_refit.load_cases  (matches plot dataset)
  2. Joint OLS refit v32 γ  (matches plot γ)
  3. Lists every case where ps_ratio == '7:3', sorted by |err%|
  4. Flags thin-film candidates (thick < 25 μm)
  5. Computes mean err% for (thin ∧ 7:3) vs (thick ∧ 7:3)
"""
from __future__ import annotations
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import json

SCRIPTS = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS))

from v32_exhaustive_refit import (  # noqa: E402
    load_cases, build_features, v29_predict_vec, fit_candidate,
)
from generate_comparison_plots import _formx_v29_params  # noqa: E402

V32 = ['LIGG_LB_PCT', 'THIN_X_GEOM', 'P50_DR_DEV', 'PSD_RATIO']


def find_amse(cid):
    """Fetch am_se_ratio directly from archive full_metrics.json."""
    for p in Path('webapp/archive').rglob(f'{cid}/full_metrics.json'):
        try:
            return json.load(open(p)).get('am_se_ratio', '')
        except Exception:
            pass
    return ''


def find_ps(cid):
    for p in Path('webapp/archive').rglob(f'{cid}/meta.json'):
        try:
            return json.load(open(p)).get('ps_ratio', '')
        except Exception:
            pass
    for p in Path('webapp/archive').rglob(f'{cid}/full_metrics.json'):
        try:
            return json.load(open(p)).get('ps_ratio', '')
        except Exception:
            pass
    return ''


def main():
    rows = load_cases()
    df = pd.DataFrame(rows).reset_index(drop=True)
    n = len(df)

    # Enrich with ps_ratio + am_se_ratio
    ps_list, amse_list = [], []
    for _, r in df.iterrows():
        ps_list.append(find_ps(r['case_id']))
        amse_list.append(find_amse(r['case_id']))
    df['ps_ratio'] = ps_list
    df['am_se_ratio'] = amse_list

    # Fit v32
    params = _formx_v29_params()
    base = v29_predict_vec(df, params)
    feats = build_features(df)
    res = fit_candidate(df, V32, feats, base)
    df['sigma_v32'] = res['pred']
    df['err_pct'] = (df['sigma_actual'] - df['sigma_v32']) / df['sigma_v32'] * 100

    print(f'Loaded {n} cases. v32 R²={res["r2"]:.4f}  LOOCV={res["loocv"]:.4f}')
    print(f'γ: ' + ', '.join(f'{f}={g:+.3f}' for f, g in zip(V32, res['gammas'])))

    # ── All 7:3 cases ───────────────────────────────────────────
    is_73 = df['ps_ratio'] == '7:3'
    sub = df[is_73].copy().sort_values('err_pct', ascending=False)
    print(f'\n=== ALL ps_ratio==7:3  ({len(sub)} cases) ===')
    cols = ['case_id', 'name', 'thick', 'am_se_ratio', 'phi', 'cn', 'tau',
            'cov', 'sigma_actual', 'sigma_v32', 'err_pct']
    with pd.option_context('display.width', 200, 'display.max_rows', None,
                           'display.float_format', lambda x: f'{x:7.3f}' if abs(x) < 1000 else f'{x:8.1f}'):
        print(sub[cols].to_string(index=False))

    # ── Sub-split by thickness ───────────────────────────────────
    thin = sub[sub['thick'] < 25]
    thick = sub[sub['thick'] >= 25]
    print(f'\n=== 7:3 split ===')
    if len(thin):
        e = thin['err_pct'].values
        print(f'  THIN  (thick<25, n={len(thin):2d}): mean={e.mean():+6.2f}  '
              f'median={np.median(e):+6.2f}  std={e.std():5.2f}  '
              f'range=[{e.min():+5.1f}, {e.max():+5.1f}]')
    if len(thick):
        e = thick['err_pct'].values
        print(f'  THICK (thick≥25, n={len(thick):2d}): mean={e.mean():+6.2f}  '
              f'median={np.median(e):+6.2f}  std={e.std():5.2f}  '
              f'range=[{e.min():+5.1f}, {e.max():+5.1f}]')

    # ── Thin+80:20+7:3 spotlight ─────────────────────────────────
    spot = sub[(sub['thick'] < 25) & (sub['am_se_ratio'] == '80:20')]
    print(f'\n=== THIN (<25 μm) ∧ 80:20 ∧ 7:3  ({len(spot)} cases) ===')
    if len(spot):
        with pd.option_context('display.width', 200,
                               'display.float_format', lambda x: f'{x:7.3f}'):
            print(spot[cols].to_string(index=False))
        e = spot['err_pct'].values
        all_err = df['err_pct'].values
        z = (e.mean() - all_err.mean()) / (all_err.std() + 1e-9) * np.sqrt(len(spot))
        print(f'\n  cluster mean err = {e.mean():+.2f}%   (global {all_err.mean():+.2f}%)')
        print(f'  z-score vs global = {z:+.2f}σ')


if __name__ == '__main__':
    main()
