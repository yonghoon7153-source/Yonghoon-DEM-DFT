#!/usr/bin/env python3
"""Physics-mode fit v43 — REAL τ_Lap_eff feature (non-circular).

v42 used tortuosity_median as a stand-in for τ_Lap_eff and got γ that
was meaningless (numerator = denominator after dedup). The real
τ_Lap_eff was never stored to full_metrics.json — webapp/app.py
computes it dynamically from:

    τ_Lap_eff = √(φ_SE × σ_grain / σ_full)        σ_grain = 3.0 mS/cm

This script reads σ_full_mScm (Hertzian) from each case's metrics and
constructs τ_Lap_eff_H from scratch. Crucially, we use the
**Hertzian-mode** τ_Lap_eff as a feature for predicting **Physics-mode**
σ_full — which is non-circular because target and feature come from
different network solver runs.

Concept tested:

  log σ_physics = log σ_v34_base + γ_1 · log τ_Lap_eff_H
                                + γ_2 · log(τ_Lap_eff_H / τ_Dij)

The second feature (τ_eff/τ_geom ratio) is the 'constriction
amplification' — physically meaningful: how much extra resistance the
contact constriction adds beyond pure geometric tortuosity.

If γ_1 or γ_2 has |γ| > 0.1 and LOOCV improves materially, this is
genuine new physics that v34 couldn't capture. Otherwise the 0.98
ceiling is confirmed once more.
"""
from __future__ import annotations
import sys, json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.optimize import minimize

SCRIPTS = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS))
from physics_fit_v33_binding import (  # noqa: E402
    load_phys_rows, fit_base, predict_base, metrics, loocv_r2,
)
from v32_exhaustive_refit import load_cases  # noqa: E402

WEBAPP = SCRIPTS.parent / 'webapp'
SIGMA_GRAIN = 3.0
TAU_SPLIT = 1.5


def _read_full_metrics(cid):
    for base in ('results', 'archive'):
        for p in (WEBAPP / base).rglob(f'{cid}/full_metrics.json'):
            try: return json.load(open(p))
            except: pass
    return None


def predict_v34(df, params, tau_split=TAU_SPLIT):
    (b0, alpha, beta, gamma, delta, phi_c, mu,
     b0_t, alpha_t, beta_t, gamma_t, delta_t, mu_t) = params
    phi  = df['phi'].values; tau = df['tau'].values; cn = df['cn'].values
    cov  = df['cov_phys'].values; f_p = df['f_perc'].values
    is_thick = (tau < tau_split).astype(float)
    excess = np.maximum(phi - phi_c, 1e-6)
    log_pred = (b0 + np.log(SIGMA_GRAIN)
        + alpha*np.log(excess) + beta*np.log(cn) + gamma*np.log(cov)
        + delta*np.log(f_p) + mu*np.log(tau)
        + is_thick*(b0_t + alpha_t*np.log(excess) + beta_t*np.log(cn)
                     + gamma_t*np.log(cov) + delta_t*np.log(f_p)
                     + mu_t*np.log(tau)))
    return np.exp(log_pred)


def fit_v34(df, n_start=12):
    bounds = [(-5,5),(0.3,3),(0.3,3),(0.0,1.5),(0.5,7),(0.05,0.30),(-2,0.5),
              (-3,3),(-2,2),(-2,2),(-1,1),(-3,3),(-2,2)]
    rng = np.random.default_rng(7)
    best = None
    for s in range(n_start):
        x0 = [rng.uniform(*b) for b in bounds]
        def loss(p):
            pred = predict_v34(df, p)
            err = np.log(df['sigma'].values + 1e-12) - np.log(pred + 1e-12)
            return float(np.mean(err**2))
        res = minimize(loss, x0, method='Nelder-Mead',
                       options={'maxiter': 4000, 'xatol': 1e-7, 'fatol': 1e-9})
        if best is None or res.fun < best.fun:
            best = res
    return best.x


def main():
    cases = load_cases()
    rows = []
    for r in load_phys_rows(cases):
        m = _read_full_metrics(r['case_id']) or {}
        sig_full_h = m.get('sigma_full_mScm')         # Hertzian σ (input data)
        sig_full_p = m.get('sigma_full_mScm_physics')  # Physics σ (target)
        phi_se     = m.get('phi_se') or r['phi']
        tau_dij    = m.get('tortuosity_mean') or r['tau']
        if (not sig_full_h) or (not sig_full_p) or sig_full_h <= 0 or sig_full_p <= 0:
            continue
        # Compute τ_Lap_eff for each mode using webapp/app.py:443 formula
        tau_lap_eff_h = np.sqrt(phi_se * SIGMA_GRAIN / sig_full_h)
        tau_lap_eff_p = np.sqrt(phi_se * SIGMA_GRAIN / sig_full_p)
        r2 = dict(r)
        r2['tau_lap_eff_h']  = float(tau_lap_eff_h)
        r2['tau_lap_eff_p']  = float(tau_lap_eff_p)  # for diagnostic only — circular if used
        r2['tau_dij_clean']  = float(tau_dij)
        r2['log_tau_lap_h']  = float(np.log(tau_lap_eff_h))
        r2['log_tau_ratio_h']= float(np.log(tau_lap_eff_h / tau_dij)
                                     if (tau_lap_eff_h > 0 and tau_dij > 0) else 0.0)
        r2['sigma_full_h']   = float(sig_full_h)
        rows.append(r2)
    df = pd.DataFrame(rows)
    print(f'Loaded {len(df)} cases with both Hertzian and Physics σ.')
    print(f'\nτ_Lap_eff sanity (computed, not stored):')
    print(f'  Hertzian: min={df["tau_lap_eff_h"].min():.2f}  max={df["tau_lap_eff_h"].max():.2f}  '
          f'median={df["tau_lap_eff_h"].median():.2f}')
    print(f'  Physics : min={df["tau_lap_eff_p"].min():.2f}  max={df["tau_lap_eff_p"].max():.2f}  '
          f'median={df["tau_lap_eff_p"].median():.2f}')
    print(f'  τ_Dij    : min={df["tau_dij_clean"].min():.2f}  max={df["tau_dij_clean"].max():.2f}  '
          f'median={df["tau_dij_clean"].median():.2f}')
    print(f'\nτ_Lap_eff_H / τ_Dij ratio (constriction amplification):')
    ratio_h = df['tau_lap_eff_h'].values / df['tau_dij_clean'].values
    print(f'  min={ratio_h.min():.2f}  max={ratio_h.max():.2f}  median={np.median(ratio_h):.2f}')

    # Baseline v34
    print('\nFitting v34 base ...')
    base_params = fit_v34(df, n_start=15)
    base_pred = predict_v34(df, base_params)
    r2_base, w20_base = metrics(df['sigma'].values, base_pred)
    print(f'  v34 base: R²={r2_base:.4f}  w20={w20_base}/{len(df)}')

    # ─────────────────────────────────────────────────────────
    # Three feature variants tested
    # ─────────────────────────────────────────────────────────
    variants = {
        'V1 + log τ_Lap_eff_H':           ['log_tau_lap_h'],
        'V2 + log(τ_Lap_eff_H / τ_Dij)':  ['log_tau_ratio_h'],
        'V3 both V1 + V2':                ['log_tau_lap_h', 'log_tau_ratio_h'],
    }

    print('\n' + '=' * 80)
    print('=== Real τ_Lap_eff (Hertzian-derived) feature tests ===')
    print('=' * 80)
    results = []
    for label, feats in variants.items():
        X = np.column_stack([df[f].values for f in feats])
        log_resid = np.log(df['sigma'].values + 1e-12) - np.log(base_pred + 1e-12)
        coef = np.linalg.lstsq(X, log_resid, rcond=None)[0]
        pred = base_pred * np.exp(X @ coef)
        r2, w20 = metrics(df['sigma'].values, pred)
        # Proper LOOCV — refit base + γ each fold
        n = len(df); pred_loo = np.empty(n)
        for i in range(n):
            sub_i = df.drop(df.index[i]).reset_index(drop=True)
            bp_i = fit_v34(sub_i, n_start=4)
            bp_p_i = predict_v34(sub_i, bp_i)
            X_i = np.column_stack([sub_i[f].values for f in feats])
            r_i = np.log(sub_i['sigma'].values + 1e-12) - np.log(bp_p_i + 1e-12)
            c_i = np.linalg.lstsq(X_i, r_i, rcond=None)[0]
            held = df.iloc[[i]]
            xh = np.array([held[f].values[0] for f in feats])
            pred_loo[i] = predict_v34(held, bp_i)[0] * np.exp(xh @ c_i)
        a = np.log(df['sigma'].values + 1e-12); p = np.log(pred_loo + 1e-12)
        loocv = 1 - np.sum((a-p)**2)/np.sum((a-a.mean())**2)
        coef_str = ', '.join(f'{f}={c:+.3f}' for f, c in zip(feats, coef))
        print(f'\n  {label}')
        print(f'    R²={r2:.4f}  LOOCV={loocv:.4f}  w20={w20}/{len(df)}')
        print(f'    γ: {coef_str}')
        results.append({'label': label, 'r2': r2, 'loocv': loocv, 'w20': w20,
                        'features': feats, 'gamma': list(coef)})

    # ─────────────────────────────────────────────────────────
    # Sanity check — what if we use the CIRCULAR Physics τ_Lap_eff?
    # This MUST give R²≈1.0 because target = derived(target). If not,
    # something's broken in the formula match.
    # ─────────────────────────────────────────────────────────
    print('\n' + '=' * 80)
    print('=== Sanity check — Physics τ_Lap_eff as feature (CIRCULAR) ===')
    print('=' * 80)
    print('  Expected: R² → 1.0 (because feature is just transformed target).')
    log_tau_p = np.log(df['tau_lap_eff_p'].values)
    X = log_tau_p.reshape(-1, 1)
    log_resid = np.log(df['sigma'].values + 1e-12) - np.log(base_pred + 1e-12)
    coef = np.linalg.lstsq(X, log_resid, rcond=None)[0]
    pred_circular = base_pred * np.exp(X.flatten() * coef[0])
    r2_circ, w20_circ = metrics(df['sigma'].values, pred_circular)
    print(f'  R²={r2_circ:.4f}  γ={coef[0]:+.3f}')
    if r2_circ > 0.999:
        print('  ✓ Circularity confirmed — formula matches webapp.')
    else:
        print('  ⚠ Circular feature didn\'t hit R²=1; investigate formula match.')

    # ─────────────────────────────────────────────────────────
    # Verdict
    # ─────────────────────────────────────────────────────────
    print('\n' + '=' * 80)
    print('=== VERDICT ===')
    print('=' * 80)
    print(f'  v34 baseline:  R²={r2_base:.4f}  LOOCV=(see prior runs)')
    print(f'{"variant":40s}  {"R²":>8s}  {"LOOCV":>8s}  {"|Δ LOOCV|":>10s}')
    for r in results:
        delta = r['loocv'] - r2_base   # treat baseline R² as approx LOOCV ref
        print(f'  {r["label"]:38s}  {r["r2"]:8.4f}  {r["loocv"]:8.4f}  {delta:+10.4f}')

    best = max(results, key=lambda r: r['loocv'])
    if best['loocv'] >= 0.99:
        print(f'\n  🎯 Real τ_Lap_eff feature breaks 0.99 with proper LOOCV.')
    elif best['loocv'] >= 0.985:
        print(f'\n  Close: best LOOCV={best["loocv"]:.4f}, gap to 0.99 = {0.99-best["loocv"]:+.4f}')
    elif best['loocv'] > r2_base + 0.005:
        print(f'\n  Real τ_Lap_eff helps (+{best["loocv"] - r2_base:.4f}) but not to 0.99.')
    else:
        print(f'\n  Real τ_Lap_eff does NOT add signal beyond v34 base.')
        print('  v34 already captures everything τ_Lap_eff would contribute.')

    out = Path('docs/figures/physics_regime')
    out.mkdir(parents=True, exist_ok=True)
    with open(out / 'physics_fit_v43_real_tau.json', 'w') as f:
        json.dump({'results': results, 'r2_base': r2_base,
                   'sanity_circular_r2': r2_circ}, f, indent=2, default=str)
    print(f'\n→ {out}/physics_fit_v43_real_tau.json')


if __name__ == '__main__':
    main()
