#!/usr/bin/env python3
"""Physics-mode fit v44 — final clean form selection.

After 11 fitting iterations (v33-v43) confirmed R²=0.98 ceiling, we
need to pick the ONE form to publish. The criterion: among forms
that preserve as many canonical v29 exponents as possible, which
gives the highest LOOCV R²?

Forms tested in order of increasing complexity:

  F1  — pure canonical, 1 free param (C only)
        σ = C · σ_grain · (φ-0.20)^0.5 · CN^1.5 · cov^0.4 · f_p^3 · τ^-2

  F2  — canonical + φ_c free, 2 params (C, φ_c)
        σ = C · σ_grain · (φ-φ_c)^0.5 · CN^1.5 · cov^0.4 · f_p^3 · τ^-2

  F3  — canonical + τ exponent free, 2 params (C, μ)
        σ = C · σ_grain · (φ-0.20)^0.5 · CN^1.5 · cov^0.4 · f_p^3 · τ^μ

  F4  — canonical + (φ_c, μ) free, 3 params
        σ = C · σ_grain · (φ-φ_c)^0.5 · CN^1.5 · cov^0.4 · f_p^3 · τ^μ

  F5  — all exponents free, 7 params (full v29)
        σ = C · σ_grain · (φ-φ_c)^α · CN^β · cov^γ · f_p^δ · τ^μ

  F6  — F5 + regime split (v34) — 14 params

Each form fitted via Nelder-Mead multi-start. Reports R²/LOOCV/w20
plus parameter values. Final summary picks the **simplest form whose
LOOCV is within 0.005 of the best** — Occam's-razor publication rule.
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


# ─────────────────────────────────────────────────────────────────────
# Form predictors
# ─────────────────────────────────────────────────────────────────────
def predict_form(df, params, form):
    """Generic v29-family predictor.
    params layout per form:
      F1: [logC]
      F2: [logC, phi_c]
      F3: [logC, mu]
      F4: [logC, phi_c, mu]
      F5: [logC, phi_c, alpha, beta, gamma, delta, mu]
      F6: F5 params + 7 thick-regime deltas
    """
    phi = df['phi'].values
    cn  = df['cn'].values
    cov = df['cov_phys'].values
    f_p = df['f_perc'].values
    tau = df['tau'].values

    if form == 'F1':
        logC, = params
        phi_c, alpha, beta, gamma, delta, mu = 0.20, 0.5, 1.5, 0.4, 3.0, -2.0
    elif form == 'F2':
        logC, phi_c = params
        alpha, beta, gamma, delta, mu = 0.5, 1.5, 0.4, 3.0, -2.0
    elif form == 'F3':
        logC, mu = params
        phi_c, alpha, beta, gamma, delta = 0.20, 0.5, 1.5, 0.4, 3.0
    elif form == 'F4':
        logC, phi_c, mu = params
        alpha, beta, gamma, delta = 0.5, 1.5, 0.4, 3.0
    elif form == 'F5':
        logC, phi_c, alpha, beta, gamma, delta, mu = params
    elif form == 'F6':
        # First 7 = ¬thick base, next 7 = thick deltas
        logC, phi_c, alpha, beta, gamma, delta, mu = params[:7]
        is_thick = (tau < 1.5).astype(float)
        excess = np.maximum(phi - phi_c, 1e-6)
        log_pred_n = (logC + np.log(SIGMA_GRAIN)
                      + alpha*np.log(excess) + beta*np.log(cn)
                      + gamma*np.log(cov) + delta*np.log(f_p) + mu*np.log(tau))
        # Thick deltas
        d_logC, d_phi_c, d_alpha, d_beta, d_gamma, d_delta, d_mu = params[7:]
        excess_t = np.maximum(phi - (phi_c + d_phi_c), 1e-6)
        log_pred_t = ((logC + d_logC) + np.log(SIGMA_GRAIN)
                      + (alpha + d_alpha)*np.log(excess_t)
                      + (beta + d_beta)*np.log(cn)
                      + (gamma + d_gamma)*np.log(cov)
                      + (delta + d_delta)*np.log(f_p)
                      + (mu + d_mu)*np.log(tau))
        return np.exp(np.where(is_thick == 1, log_pred_t, log_pred_n))
    else:
        raise ValueError(f'Unknown form: {form}')

    excess = np.maximum(phi - phi_c, 1e-6)
    log_pred = (logC + np.log(SIGMA_GRAIN)
                + alpha*np.log(excess) + beta*np.log(cn)
                + gamma*np.log(cov) + delta*np.log(f_p) + mu*np.log(tau))
    return np.exp(log_pred)


def fit_form(df, form, n_start=15):
    bounds_map = {
        'F1': [(-5, 5)],
        'F2': [(-5, 5), (0.05, 0.30)],
        'F3': [(-5, 5), (-3.0, 0.5)],
        'F4': [(-5, 5), (0.05, 0.30), (-3.0, 0.5)],
        'F5': [(-5,5),(0.05,0.30),(0.1,5),(0.1,5),(0.0,2),(0.5,7),(-3,0.5)],
        'F6': [(-5,5),(0.05,0.30),(0.1,5),(0.1,5),(0.0,2),(0.5,7),(-3,0.5),
               (-3,3),(-0.20,0.20),(-3,3),(-3,3),(-1,1),(-3,3),(-2,2)],
    }
    bounds = bounds_map[form]
    rng = np.random.default_rng(42)
    best = None
    for s in range(n_start):
        x0 = [rng.uniform(*b) for b in bounds]
        def loss(p):
            pred = predict_form(df, p, form)
            err = np.log(df['sigma'].values + 1e-12) - np.log(pred + 1e-12)
            return float(np.mean(err ** 2))
        res = minimize(loss, x0, method='Nelder-Mead',
                       options={'maxiter': 5000, 'xatol': 1e-7, 'fatol': 1e-9})
        if best is None or res.fun < best.fun:
            best = res
    return best.x


def loocv_form(df, form, n_start_inner=4):
    n = len(df)
    pred_loo = np.empty(n)
    for i in range(n):
        sub = df.drop(df.index[i]).reset_index(drop=True)
        params = fit_form(sub, form, n_start=n_start_inner)
        held = df.iloc[[i]]
        pred_loo[i] = predict_form(held, params, form)[0]
    a = np.log(df['sigma'].values + 1e-12); p = np.log(pred_loo + 1e-12)
    return 1 - np.sum((a-p)**2) / np.sum((a-a.mean())**2)


def main():
    cases = load_cases()
    rows = load_phys_rows(cases)
    df = pd.DataFrame(rows)
    print(f'Loaded {len(df)} physics-mode cases.')

    forms = ['F1','F2','F3','F4','F5','F6']
    descriptions = {
        'F1': 'Pure canonical, 1 free (C)',
        'F2': 'Canonical + free φ_c, 2 free (C, φ_c)',
        'F3': 'Canonical + free μ, 2 free (C, μ)',
        'F4': 'Canonical + free φ_c, μ, 3 free',
        'F5': 'All exponents free, 7 free',
        'F6': 'F5 + regime split, 14 free (= v34)',
    }
    n_params = {'F1':1,'F2':2,'F3':2,'F4':3,'F5':7,'F6':14}

    results = []
    for form in forms:
        print('\n' + '=' * 80)
        print(f'{form} — {descriptions[form]}')
        print('=' * 80)
        params = fit_form(df, form, n_start=20 if form == 'F6' else 15)
        pred = predict_form(df, params, form)
        r2, w20 = metrics(df['sigma'].values, pred)

        # Show fitted params
        if form == 'F1':
            logC = params[0]
            print(f'  C = exp({logC:+.3f}) = {np.exp(logC):.4f}')
        elif form == 'F2':
            logC, phi_c = params
            print(f'  C = {np.exp(logC):.4f},  φ_c = {phi_c:.3f}')
        elif form == 'F3':
            logC, mu = params
            print(f'  C = {np.exp(logC):.4f},  μ = {mu:+.3f}')
        elif form == 'F4':
            logC, phi_c, mu = params
            print(f'  C = {np.exp(logC):.4f},  φ_c = {phi_c:.3f},  μ = {mu:+.3f}')
        elif form == 'F5':
            logC, phi_c, alpha, beta, gamma, delta, mu = params
            print(f'  C={np.exp(logC):.4f}  φ_c={phi_c:.3f}')
            print(f'  α={alpha:+.3f}  β={beta:+.3f}  γ={gamma:+.3f}  '
                  f'δ={delta:+.3f}  μ={mu:+.3f}')
        elif form == 'F6':
            print(f'  ¬thick: C={np.exp(params[0]):.4f}  φ_c={params[1]:.3f}  '
                  f'α={params[2]:+.3f}  β={params[3]:+.3f}  γ={params[4]:+.3f}  '
                  f'δ={params[5]:+.3f}  μ={params[6]:+.3f}')
            print(f'  Δ thick:  ΔC={params[7]:+.3f} Δφ_c={params[8]:+.3f} '
                  f'Δα={params[9]:+.3f} Δβ={params[10]:+.3f} Δγ={params[11]:+.3f} '
                  f'Δδ={params[12]:+.3f} Δμ={params[13]:+.3f}')

        # Proper LOOCV
        print('  Computing LOOCV ...')
        loocv = loocv_form(df, form,
                           n_start_inner=2 if form == 'F6' else 3)
        print(f'  R²={r2:.4f}  LOOCV={loocv:.4f}  w20={w20}/{len(df)}')

        # Compute AIC-style penalty for parsimony comparison
        n = len(df); k = n_params[form]
        rss = np.sum((np.log(df['sigma'].values+1e-12) - np.log(pred+1e-12))**2)
        aic = n * np.log(rss / n) + 2 * k
        results.append({'form': form, 'desc': descriptions[form], 'k': k,
                        'r2': r2, 'loocv': loocv, 'w20': w20, 'aic': aic,
                        'params': list(params)})

    # ─────────────────────────────────────────────────────────
    # Summary — sorted by LOOCV (best practical metric)
    # ─────────────────────────────────────────────────────────
    print('\n' + '=' * 80)
    print('=== FINAL CLEAN-FORM COMPARISON (sorted by LOOCV) ===')
    print('=' * 80)
    print(f'{"form":4s}  {"k":>3s}  {"R²":>8s}  {"LOOCV":>8s}  {"w20":>10s}  {"AIC":>8s}  description')
    for r in sorted(results, key=lambda x: -x['loocv']):
        print(f'  {r["form"]:3s}  {r["k"]:>3d}  {r["r2"]:8.4f}  {r["loocv"]:8.4f}  '
              f'{r["w20"]:>3d}/{len(df)}     {r["aic"]:8.2f}  {r["desc"]}')

    # Occam's razor: pick simplest form within 0.005 LOOCV of the best
    best_loocv = max(r['loocv'] for r in results)
    occam = [r for r in results if r['loocv'] >= best_loocv - 0.005]
    occam.sort(key=lambda r: r['k'])
    occam_pick = occam[0]
    abs_best = max(results, key=lambda r: r['loocv'])

    print('\n' + '=' * 80)
    print('=== RECOMMENDATION ===')
    print('=' * 80)
    print(f'Absolute best LOOCV: {abs_best["form"]} '
          f'(LOOCV={abs_best["loocv"]:.4f}, k={abs_best["k"]})')
    print(f'Simplest within 0.005 of best (Occam): {occam_pick["form"]} '
          f'(LOOCV={occam_pick["loocv"]:.4f}, k={occam_pick["k"]})')
    print(f'\nPublication recommendation: **{occam_pick["form"]}**')
    print(f'  {occam_pick["desc"]}')
    print(f'  R²={occam_pick["r2"]:.4f}, LOOCV={occam_pick["loocv"]:.4f}, '
          f'w20={occam_pick["w20"]}/{len(df)}')

    out = Path('docs/figures/physics_regime')
    out.mkdir(parents=True, exist_ok=True)
    with open(out / 'physics_fit_v44_final.json', 'w') as f:
        json.dump({'results': results, 'occam_pick': occam_pick['form'],
                   'absolute_best': abs_best['form']},
                  f, indent=2, default=str)
    print(f'\n→ {out}/physics_fit_v44_final.json')


if __name__ == '__main__':
    main()
