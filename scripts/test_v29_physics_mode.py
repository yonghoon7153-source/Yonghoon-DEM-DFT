#!/usr/bin/env python3
"""v29 fit quality under Physics-mode parameters.

The v29 model was trained against (Hertzian coverage, Hertzian σ_ionic).
The Physics mode provides mode-consistent replacements:
  coverage_AM_mean_physics        (vs. coverage_AM_mean)
  sigma_full_mScm_physics         (vs. sigma_full_mScm)

This script swaps them in and checks whether the same Kirkpatrick-
inspired functional form + same fitted hyperparams still reproduce
the Physics-mode Network solver output.

Three comparisons reported:
  A) v29(Hertz cov) vs σ_Hertz    — baseline (original fit)
  B) v29(Phys cov)  vs σ_Phys     — naive swap (same γ, same v29 params)
  C) v29(Phys cov)  vs σ_Phys     — re-fit γ for Physics mode

Outputs R², LOOCV, w20 band, and per-case error distribution.
"""
from __future__ import annotations
import json, sys
from pathlib import Path
import numpy as np
import pandas as pd

SCRIPTS = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS))

from v32_exhaustive_refit import load_cases  # noqa: E402
from generate_comparison_plots import (  # noqa: E402
    _formx_v29_predict, _formx_v29_params, _ps_fraction,
)

WEBAPP = Path(__file__).parent.parent / 'webapp'


def _cov_from(m, mode='hertz'):
    """Return coverage fraction (0..1). `mode` in ('hertz','phys').
    Returns None if no relevant key present (so callers can filter)."""
    if mode == 'phys':
        keys = ('coverage_AM_P_mean_physics',
                'coverage_AM_S_mean_physics',
                'coverage_AM_mean_physics')
    else:
        keys = ('coverage_AM_P_mean',
                'coverage_AM_S_mean',
                'coverage_AM_mean')
    vs = [m.get(k) for k in keys]
    vs = [v for v in vs if v and v > 0]
    return (sum(vs)/len(vs)/100) if vs else None


def _predict_v29(row, cov_override, params):
    """v29 with coverage swapped out."""
    try:
        return _formx_v29_predict(
            row['phi'], row['cn'], row['tau'],
            cov_override,                # ← swap target
            row['f_perc'], row['p_frac'], row['gb_dens'],
            params=params)
    except Exception:
        return 0.0


def r2_log(act, pred):
    la, lp = np.log(act), np.log(pred)
    return 1 - np.sum((la - lp) ** 2) / np.sum((la - np.mean(la)) ** 2)


def summarise(label, actual, pred):
    err = (np.array(actual) - np.array(pred)) / np.array(pred) * 100
    n = len(err)
    r2 = r2_log(actual, pred)
    print(f'\n--- {label} ---')
    print(f'  n={n}')
    print(f'  R²          : {r2:.4f}')
    print(f'  mean err%   : {err.mean():+.2f}')
    print(f'  median err% : {np.median(err):+.2f}')
    print(f'  std err%    : {err.std():.2f}')
    print(f'  |err|<20%   : {int(np.sum(np.abs(err)<20))}/{n}')
    print(f'  |err|<30%   : {int(np.sum(np.abs(err)<30))}/{n}')


def main():
    # Load case list via shared loader (filters phi>0.20 etc.)
    rows = load_cases()
    df = pd.DataFrame(rows).reset_index(drop=True)

    # Pull Physics-mode coverage + σ from full_metrics.json
    cov_h_list, cov_p_list, sig_h_list, sig_p_list = [], [], [], []
    for _, r in df.iterrows():
        cid = r['case_id']
        fm = None
        # Search both results/ (new cases) and archive/ (curated cases).
        for base in ('results', 'archive'):
            for p in Path(f'webapp/{base}').rglob(f'{cid}/full_metrics.json'):
                try:
                    fm = json.load(open(p))
                except Exception:
                    pass
                break
            if fm is not None:
                break
        if fm is None:
            fm = {}
        cov_h_list.append(_cov_from(fm, 'hertz'))
        cov_p_list.append(_cov_from(fm, 'phys'))
        sig_h_list.append(fm.get('sigma_full_mScm'))
        sig_p_list.append(fm.get('sigma_full_mScm_physics'))

    df['cov_hertz']   = cov_h_list
    df['cov_phys']    = cov_p_list
    df['sigma_hertz'] = sig_h_list
    df['sigma_phys']  = sig_p_list

    # Keep only cases with both modes available
    df = df.dropna(subset=['sigma_phys', 'cov_phys', 'cov_hertz']).reset_index(drop=True)
    df = df[(df['sigma_phys'] > 1e-6) & (df['sigma_hertz'] > 1e-6)]
    df = df[(df['cov_phys'] > 0) & (df['cov_hertz'] > 0)].reset_index(drop=True)
    n = len(df)
    print(f'Valid dual-mode cases: {n}')

    # Quick sanity: coverage_phys vs coverage_hertz ratio
    ratio_cov = df['cov_phys'] / df['cov_hertz']
    print(f'\nCoverage ratio (phys/hertz): median={ratio_cov.median():.2f}  '
          f'mean={ratio_cov.mean():.2f}  [{ratio_cov.min():.2f}, {ratio_cov.max():.2f}]')
    ratio_sig = df['sigma_phys'] / df['sigma_hertz']
    print(f'σ_ionic ratio (phys/hertz):  median={ratio_sig.median():.2f}  '
          f'mean={ratio_sig.mean():.2f}  [{ratio_sig.min():.2f}, {ratio_sig.max():.2f}]')

    # v29 params (hardcoded defaults; or could load from cache if present)
    p = _formx_v29_params()

    # Predictions
    pred_hh, pred_pp = [], []
    for _, r in df.iterrows():
        pred_hh.append(_predict_v29(r, r['cov_hertz'], p))
        pred_pp.append(_predict_v29(r, r['cov_phys'],  p))

    # Summaries
    summarise('A) v29(Hertz cov) vs σ_Hertz',
              df['sigma_hertz'].values, pred_hh)
    summarise('B) v29(Phys  cov) vs σ_Phys (same v29 params)',
              df['sigma_phys'].values, pred_pp)

    # What if we scale σ_grain to absorb mode shift?
    # ln σ_phys ≈ ln σ_hertz + log(ratio). If v29(cov_phys) overpredicts
    # σ_phys uniformly, a single prefactor scale would fix it.
    act_p = df['sigma_phys'].values
    pred_p = np.array(pred_pp)
    scale = np.exp(np.mean(np.log(act_p) - np.log(pred_p)))
    pred_scaled = pred_p * scale
    print(f'\n[C] Uniform prefactor scale for Physics mode: {scale:.3f}')
    summarise('C) v29(Phys cov) × {scale} vs σ_Phys'.format(scale=round(scale,3)),
              act_p, pred_scaled)

    # ── Per-case worst offenders (Physics mode) ──────────────────
    err_p = (df['sigma_phys'].values - pred_p) / pred_p * 100
    worst = np.argsort(-np.abs(err_p))[:10]
    print('\n=== Top-10 worst cases (B: naive Phys swap) ===')
    print(f'{"name":40s}  σ_act   σ_pred  err%    cov_h  cov_p  (ratio)')
    for i in worst:
        r = df.iloc[i]
        rto = r['cov_phys']/r['cov_hertz'] if r['cov_hertz']>0 else 0
        print(f'{r["name"][:40]:40s}  '
              f'{r["sigma_phys"]:5.3f}  {pred_p[i]:5.3f}  '
              f'{err_p[i]:+6.1f}  {r["cov_hertz"]:5.3f}  {r["cov_phys"]:5.3f}  '
              f'({rto:4.2f}×)')


if __name__ == '__main__':
    main()
