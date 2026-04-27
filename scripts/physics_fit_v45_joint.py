#!/usr/bin/env python3
"""Physics-mode fit v45 — escape the v34-residual trap.

v33–v44 all tested outlier corrections as RESIDUAL TERMS stacked on
top of v34's regime base. The base absorbs all signal first, leaving
nothing for residuals — every single γ collapsed to ≈0. This script
breaks the pattern by:

  1) JOINT optimization. Base exponents + correction coefficients
     fitted together via Nelder-Mead, not sequentially. The optimizer
     can redistribute weight from base to correction terms.

  2) CORE-TERM corrections, not residuals. Finite-size, constriction
     amplification, P:S 5050, and binding shares enter the form as
     multiplicative factors, integrated with the power-law structure.

  3) New architectures designed from scratch for physics-mode:

        ARCH-A  v29 + finite-size (CORE)
                σ = C·σg·(φ-φc)^α·CN^β·cov^γ·f_p^δ·τ^μ · (L/L₀)^η

        ARCH-B  v29 + plastic-blend C_blend_phys
                C_blend_phys = exp(θ_T·b_tabor + θ_G·b_geom)
                replaces the elastic C_blend(τ) which collapses.

        ARCH-C  v29 + finite-size + plastic-blend + 5050 bump
                full physics-aware joint form.

        ARCH-D  Bruggeman-extended (rebuilt from 1st principles)
                σ = σg·φ^n · g_finite(L) · g_constr(b_T, b_G) · g_5050(p)

        ARCH-E  Two-mode mixture (NOT outlier-mixture; physics modes)
                Combine elastic + plastic predictions weighted by
                tabor-share / hertzian-share. Each mode has own
                parameters.

  4) Each arch evaluated with proper LOOCV (refit per fold).

If any architecture LOOCV ≥ 0.99, we have it. If they all plateau at
0.97-0.98, it's truly the data noise floor and we move on with that
honest verdict.
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


def _read_full_metrics(cid):
    for base in ('results', 'archive'):
        for p in (WEBAPP / base).rglob(f'{cid}/full_metrics.json'):
            try: return json.load(open(p))
            except: pass
    return None


def enrich(rows):
    out = []
    for r in rows:
        m = _read_full_metrics(r['case_id']) or {}
        r2 = dict(r)
        r2['thickness'] = float(m.get('thickness_um', 0) or 0)
        r2['sigma_full_h'] = float(m.get('sigma_full_mScm', 0) or 0)
        out.append(r2)
    return out


# ─────────────────────────────────────────────────────────────────────
# ARCH-A — v29 power-law + finite-size as CORE term, joint fit
# ─────────────────────────────────────────────────────────────────────
def predict_A(df, params):
    """σ = C·σg · (φ-φc)^α · CN^β · cov^γ · f_p^δ · τ^μ · (L/L0)^η"""
    logC, phi_c, alpha, beta, gamma, delta, mu, eta, L0 = params
    phi = df['phi'].values; cn = df['cn'].values; cov = df['cov_phys'].values
    f_p = df['f_perc'].values; tau = df['tau'].values
    L = np.maximum(df['thickness'].values, 1.0)
    excess = np.maximum(phi - phi_c, 1e-6)
    log_pred = (logC + np.log(SIGMA_GRAIN)
                + alpha*np.log(excess) + beta*np.log(cn) + gamma*np.log(cov)
                + delta*np.log(f_p) + mu*np.log(tau)
                + eta*np.log(L/max(L0, 1.0)))
    return np.exp(log_pred)


def bounds_A(): return [(-5,5),(0.05,0.30),(0.1,5),(0.1,5),(0.0,2),(0.5,7),
                         (-3,0.5),(-1.5,1.5),(5,200)]


# ─────────────────────────────────────────────────────────────────────
# ARCH-B — v29 + plastic-blend (replaces elastic C_blend)
# ─────────────────────────────────────────────────────────────────────
def predict_B(df, params):
    """σ = C·σg · (φ-φc)^α · CN^β · cov^γ · f_p^δ · τ^μ · C_blend_phys
    where C_blend_phys = exp(θ_T · b_tabor/100 + θ_G · b_geom/100)
    (replaces elastic C_blend(τ) which collapses in physics-mode).
    """
    logC, phi_c, alpha, beta, gamma, delta, mu, theta_T, theta_G = params
    phi = df['phi'].values; cn = df['cn'].values; cov = df['cov_phys'].values
    f_p = df['f_perc'].values; tau = df['tau'].values
    b_T = df['b_tabor'].values / 100.0
    b_G = df['b_geom'].values  / 100.0
    excess = np.maximum(phi - phi_c, 1e-6)
    log_pred = (logC + np.log(SIGMA_GRAIN)
                + alpha*np.log(excess) + beta*np.log(cn) + gamma*np.log(cov)
                + delta*np.log(f_p) + mu*np.log(tau)
                + theta_T * b_T + theta_G * b_G)
    return np.exp(log_pred)


def bounds_B(): return [(-5,5),(0.05,0.30),(0.1,5),(0.1,5),(0.0,2),(0.5,7),
                         (-3,0.5),(-3,3),(-3,3)]


# ─────────────────────────────────────────────────────────────────────
# ARCH-C — full joint physics: finite-size + plastic-blend + 5050 bump
# ─────────────────────────────────────────────────────────────────────
def predict_C(df, params):
    """σ = (ARCH-A finite-size) · plastic-blend · 5050-bump"""
    logC, phi_c, alpha, beta, gamma, delta, mu, eta, L0, \
        theta_T, theta_G, theta_5050, sigma_p = params
    phi = df['phi'].values; cn = df['cn'].values; cov = df['cov_phys'].values
    f_p = df['f_perc'].values; tau = df['tau'].values
    L = np.maximum(df['thickness'].values, 1.0)
    p = df['p_frac'].values
    b_T = df['b_tabor'].values / 100.0
    b_G = df['b_geom'].values / 100.0
    excess = np.maximum(phi - phi_c, 1e-6)
    bump_5050 = np.exp(-((p - 0.5) / max(sigma_p, 0.01)) ** 2)
    log_pred = (logC + np.log(SIGMA_GRAIN)
                + alpha*np.log(excess) + beta*np.log(cn) + gamma*np.log(cov)
                + delta*np.log(f_p) + mu*np.log(tau)
                + eta*np.log(L/max(L0, 1.0))
                + theta_T*b_T + theta_G*b_G
                + theta_5050 * bump_5050)
    return np.exp(log_pred)


def bounds_C(): return [(-5,5),(0.05,0.30),(0.1,5),(0.1,5),(0.0,2),(0.5,7),
                         (-3,0.5),(-1.5,1.5),(5,200),(-3,3),(-3,3),
                         (-2,2),(0.02,0.30)]


# ─────────────────────────────────────────────────────────────────────
# ARCH-D — Bruggeman-extended from 1st principles
# ─────────────────────────────────────────────────────────────────────
def predict_D(df, params):
    """σ = σg·φ^n · g_finite(L) · g_constr(b_T, b_G) · g_5050(p)"""
    n_brug, eta, L0, theta_T, theta_G, theta_5050, sigma_p, logC = params
    phi = df['phi'].values
    L = np.maximum(df['thickness'].values, 1.0)
    p = df['p_frac'].values
    b_T = df['b_tabor'].values / 100.0
    b_G = df['b_geom'].values / 100.0
    bump_5050 = np.exp(-((p - 0.5) / max(sigma_p, 0.01)) ** 2)
    log_pred = (logC + np.log(SIGMA_GRAIN)
                + n_brug*np.log(np.maximum(phi, 1e-3))
                + eta*np.log(L/max(L0, 1.0))
                + theta_T*b_T + theta_G*b_G
                + theta_5050 * bump_5050)
    return np.exp(log_pred)


def bounds_D(): return [(0.5,5),(-1.5,1.5),(5,200),(-3,3),(-3,3),
                         (-2,2),(0.02,0.30),(-5,5)]


# ─────────────────────────────────────────────────────────────────────
# ARCH-E — Two-mode mixture (elastic + plastic), composition-weighted
# ─────────────────────────────────────────────────────────────────────
def predict_E(df, params):
    """σ = w_E · σ_elastic + w_P · σ_plastic
       w_P = b_tabor + b_geom + b_volume   (plastic share)
       w_E = b_hertzian + b_liggghts       (elastic share)
       Each mode has own (logC, alpha, beta, gamma, delta, mu).
    """
    p_E = params[:6]   # logC_E, α_E, β_E, γ_E, δ_E, μ_E
    p_P = params[6:12] # logC_P, α_P, β_P, γ_P, δ_P, μ_P
    phi_c = params[12]
    phi = df['phi'].values; cn = df['cn'].values; cov = df['cov_phys'].values
    f_p = df['f_perc'].values; tau = df['tau'].values
    excess = np.maximum(phi - phi_c, 1e-6)

    def _mode(p):
        logC, a, b, g, d, m = p
        return np.exp(logC + np.log(SIGMA_GRAIN)
                      + a*np.log(excess) + b*np.log(cn) + g*np.log(cov)
                      + d*np.log(f_p) + m*np.log(tau))

    sigma_E = _mode(p_E)
    sigma_P = _mode(p_P)
    # Composition weights from binding distribution
    w_P = (df['b_tabor'].values + df['b_geom'].values +
           df['b_volume'].values) / 100.0
    w_E = (df['b_hertzian'].values + df['b_liggghts'].values) / 100.0
    # Renormalise (sum should be ≈1 anyway)
    total = w_E + w_P + 1e-9
    w_P /= total; w_E /= total
    return w_E * sigma_E + w_P * sigma_P


def bounds_E(): return [(-5,5),(0.1,5),(0.1,5),(0.0,2),(0.5,7),(-3,0.5),
                         (-5,5),(0.1,5),(0.1,5),(0.0,2),(0.5,7),(-3,0.5),
                         (0.05,0.30)]


# ─────────────────────────────────────────────────────────────────────
# Generic fit + LOOCV
# ─────────────────────────────────────────────────────────────────────
def _loss(params, df, predictor):
    pred = predictor(df, params)
    err = np.log(df['sigma'].values + 1e-12) - np.log(pred + 1e-12)
    return float(np.mean(err ** 2))


def fit_arch(df, predictor, bounds, n_start=20):
    rng = np.random.default_rng(101)
    best = None
    for s in range(n_start):
        x0 = [rng.uniform(*b) for b in bounds]
        res = minimize(_loss, x0, args=(df, predictor), method='Nelder-Mead',
                       options={'maxiter': 8000, 'xatol': 1e-7, 'fatol': 1e-9})
        if best is None or res.fun < best.fun:
            best = res
    return best.x


def loocv_arch(df, predictor, bounds, n_start_inner=4):
    n = len(df); pred_loo = np.empty(n)
    for i in range(n):
        sub = df.drop(df.index[i]).reset_index(drop=True)
        params = fit_arch(sub, predictor, bounds, n_start=n_start_inner)
        held = df.iloc[[i]]
        pred_loo[i] = predictor(held, params)[0]
    a = np.log(df['sigma'].values + 1e-12); p = np.log(pred_loo + 1e-12)
    return 1 - np.sum((a-p)**2) / np.sum((a-a.mean())**2)


def main():
    cases = load_cases()
    rows = enrich(load_phys_rows(cases))
    df = pd.DataFrame(rows)
    print(f'Loaded {len(df)} cases.')

    archs = [
        ('A v29 + finite-size CORE', predict_A, bounds_A(), 9),
        ('B v29 + plastic-blend',    predict_B, bounds_B(), 9),
        ('C v29 + ALL physics CORE', predict_C, bounds_C(), 13),
        ('D Bruggeman-extended',     predict_D, bounds_D(), 8),
        ('E Two-mode mixture',       predict_E, bounds_E(), 13),
    ]

    results = []
    for label, predictor, bds, k in archs:
        print('\n' + '=' * 80)
        print(f'ARCH-{label}  (k={k} free params)')
        print('=' * 80)
        params = fit_arch(df, predictor, bds, n_start=30)
        pred = predictor(df, params)
        r2, w20 = metrics(df['sigma'].values, pred)
        print(f'  Joint-fit R²={r2:.4f}  w20={w20}/{len(df)}')
        # Print params (truncated)
        print('  params:', '  '.join(f'{v:+.3f}' for v in params))
        # LOOCV
        print('  LOOCV computing ...')
        loocv = loocv_arch(df, predictor, bds, n_start_inner=3)
        print(f'  LOOCV R²={loocv:.4f}')
        results.append({'arch': label, 'k': k, 'r2': r2, 'loocv': loocv,
                        'w20': w20, 'params': list(params)})

    # Summary
    print('\n' + '=' * 80)
    print('=== ALL JOINT-OPT ARCHITECTURES sorted by LOOCV ===')
    print('=' * 80)
    print(f'{"arch":34s}  {"k":>3s}  {"R²":>8s}  {"LOOCV":>8s}  {"w20":>10s}')
    for r in sorted(results, key=lambda x: -x['loocv']):
        print(f'  {r["arch"]:32s}  {r["k"]:>3d}  {r["r2"]:8.4f}  '
              f'{r["loocv"]:8.4f}  {r["w20"]:>3d}/{len(df)}')

    best = max(results, key=lambda r: r['loocv'])
    print(f'\nBest architecture: {best["arch"]} (LOOCV={best["loocv"]:.4f})')

    if best['loocv'] >= 0.99:
        print('\n  🎯 0.99 REACHED via joint-opt architecture!')
        print('  This breaks the v34 ceiling — corrections work as CORE terms.')
    elif best['loocv'] >= 0.985:
        print(f'\n  Close: gap to 0.99 = {0.99-best["loocv"]:+.4f}')
    else:
        print(f'\n  Joint-opt also caps at LOOCV={best["loocv"]:.4f}.')
        print('  This is decisive: 0.97-0.98 IS the dataset noise floor.')

    out = Path('docs/figures/physics_regime')
    out.mkdir(parents=True, exist_ok=True)
    with open(out / 'physics_fit_v45_joint.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print(f'\n→ {out}/physics_fit_v45_joint.json')


if __name__ == '__main__':
    main()
