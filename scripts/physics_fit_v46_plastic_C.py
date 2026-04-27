#!/usr/bin/env python3
"""Physics-mode fit v46 — v29 framework + plastic C-extensions, joint fit.

Per user direction:
  • Keep v29 base power-law structure with canonical exponents fixed
    (α=1/2, β=3/2, γ=2/5, δ=3 — Stauffer-Aharony / Kirkpatrick).
  • C_blend(τ) and C_corr: keep structural form, BUT extend with
    new plastic-deformation-specific terms (binding shares, finite
    size, etc.) and let ALL inner thresholds/parameters fit freely.
  • Goal: outlier handling via richer C-structure, not abandoning
    physically meaningful exponents.

  Form (all 4 power-law exponents FIXED at canonical values):

    σ = e^C_corr · C_blend^phys(τ, b_T, b_G) · σ_grain
        · (φ_SE - φ_c)^{1/2} · CN^{3/2} · cov^{2/5} · f_perc^3

  C_blend^phys(τ, b_T, b_G) — extended blend, free inner params:
    log C_blend = log C_v5(τ) + Δ_plastic(b_T, b_G)
      C_v5(τ)     = thick↔thin sigmoid, free (C_thick, C_thin, τ_0, k_τ)
      Δ_plastic   = θ_T·(b_T - b̄_T) + θ_G·(b_G - b̄_G)
                    [centered, so it's a pure correction not double-count]

  C_corr — original 3 terms PLUS plastic-mode new terms:
    C_corr = β_pf·w_pf(p)            (P:S sigmoid, free k_pf, p_c)
           + β_lin·p·w_win(τ)        (τ-Gaussian bump, free τ_c, σ_τ)
           + β_gb·w_gb(ρ_gb)         (GB density sigmoid, free k_gb)
           + β_T·b_T_c + β_G·b_G_c   (NEW: plastic-binding direct shift)
           + β_L·log(L/L_*)          (NEW: finite-size correction)

All centered so base prediction unchanged when corrections are zero.

  Free parameters (~20 total, all with physical meaning):
    φ_c, C_thick, C_thin, τ_0, k_τ,             (5 — base + v5 sigmoid)
    K_BL, τ_c_BL,                                 (2 — blend weight)
    poly3: a0, a1, a2, a3,                        (4 — extreme-thin poly)
    β_pf, k_pf, p_c, β_lin, τ_c_win, σ_τ_win,    (6 — P:S + τ-bump)
    β_gb, k_gb,                                   (2 — GB term)
    β_T, β_G, β_L, L_star                         (4 — new plastic terms)

  Joint Nelder-Mead optimization. Reports R², LOOCV, parameter values
  with physical interpretation of any term that activates strongly.
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
    load_phys_rows, metrics, loocv_r2,
)
from v32_exhaustive_refit import load_cases  # noqa: E402

WEBAPP = SCRIPTS.parent / 'webapp'
SIGMA_GRAIN = 3.0

# Canonical exponents (FIXED — Stauffer/Kirkpatrick)
ALPHA_FIX = 0.5
BETA_FIX  = 1.5
GAMMA_FIX = 0.4
DELTA_FIX = 3.0


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
        out.append(r2)
    return out


def _sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))


def predict_v46(df, params):
    """v29 form with canonical exponents + extended C-side joint fit.

    Parameter layout (22 params total):
      0    phi_c
      1-2  C_thick, C_thin           (v5 asymptotes, log-space)
      3-4  tau_0, k_tau               (v5 sigmoid centre, sharpness)
      5-6  K_BL, tau_c_BL             (blend weight sigmoid)
      7-10 a0, a1, a2, a3             (extreme-thin poly3 coefs)
     11-13 beta_pf, k_pf, p_c         (P:S sigmoid)
     14-16 beta_lin, tau_c_win, s_win (τ-bump Gaussian)
     17-18 beta_gb, k_gb              (GB sigmoid)
     19-20 beta_T, beta_G             (NEW: plastic-binding direct)
     21-22 beta_L, L_star             (NEW: finite-size)
    """
    (phi_c,
     C_thick, C_thin, tau_0, k_tau,
     K_BL, tau_c_BL,
     a0, a1, a2, a3,
     beta_pf, k_pf, p_c,
     beta_lin, tau_c_win, s_win,
     beta_gb, k_gb,
     beta_T, beta_G,
     beta_L, L_star) = params

    phi = df['phi'].values
    tau = df['tau'].values
    cn  = df['cn'].values
    cov = df['cov_phys'].values
    f_p = df['f_perc'].values
    p   = df['p_frac'].values
    rho_gb = np.maximum(df['gb_dens'].values, 1e-6)
    L   = np.maximum(df['thickness'].values, 1.0)
    b_T = df['b_tabor'].values    / 100.0  # plastic-cap binding share (Tabor)
    b_G = df['b_geom'].values     / 100.0  # geom-cap binding share

    # ── Base power-law (fixed canonical exponents) ─────────────
    excess = np.maximum(phi - phi_c, 1e-6)
    log_base = (np.log(SIGMA_GRAIN)
                + ALPHA_FIX * np.log(excess)
                + BETA_FIX  * np.log(cn)
                + GAMMA_FIX * np.log(cov)
                + DELTA_FIX * np.log(f_p))

    # ── C_blend(τ) — v5 sigmoid ⊕ poly3 ───────────────────────
    # v5 sigmoid: thick→thin asymptote
    s_v5 = _sigmoid(k_tau * (tau - tau_0))
    log_Cv5 = np.log(max(C_thick, 1e-6)) + (
        np.log(max(C_thin, 1e-6)) - np.log(max(C_thick, 1e-6))) * s_v5
    # poly3 in log τ — extreme-thin regime
    ln_t = np.log(np.maximum(tau, 0.01))
    log_Cp3 = a0 + a1 * ln_t + a2 * ln_t ** 2 + a3 * ln_t ** 3
    # Blend weight (sigmoid in τ)
    w_BL = _sigmoid(K_BL * (tau - tau_c_BL))
    log_Cblend = (1 - w_BL) * log_Cv5 + w_BL * log_Cp3

    # NEW: Plastic-binding addition to C_blend (centered)
    b_T_mean = float(np.mean(b_T))
    b_G_mean = float(np.mean(b_G))
    log_Cblend = log_Cblend + 0.0  # placeholder; binding goes in C_corr below

    # ── C_corr: original 3 terms + 2 new plastic terms ────────
    # P:S sigmoid (centered)
    w_pf = _sigmoid(k_pf * (p - p_c))
    w_pf_c = w_pf - float(np.mean(w_pf))
    # τ-Gaussian bump × p (centered)
    w_win = np.exp(-((tau - tau_c_win) / max(s_win, 0.05)) ** 2 / 2.0)
    pwwin = p * w_win
    pwwin_c = pwwin - float(np.mean(pwwin))
    # GB sigmoid (centered, log-space)
    ln_gb = np.log(rho_gb)
    w_gb = _sigmoid(k_gb * (ln_gb - float(np.median(ln_gb))))
    w_gb_c = w_gb - float(np.mean(w_gb))
    # NEW: plastic-binding direct (centered)
    b_T_c = b_T - b_T_mean
    b_G_c = b_G - b_G_mean
    # NEW: finite-size (centered log)
    L_c = np.log(L / max(L_star, 1.0))
    L_c = L_c - float(np.mean(L_c))

    C_corr = (beta_pf * w_pf_c
              + beta_lin * pwwin_c
              + beta_gb  * w_gb_c
              + beta_T   * b_T_c
              + beta_G   * b_G_c
              + beta_L   * L_c)

    log_pred = log_base + log_Cblend + C_corr
    return np.exp(log_pred)


def _bounds_v46():
    return [
        # phi_c
        (0.05, 0.30),
        # C_thick, C_thin
        (0.001, 0.5), (0.001, 0.5),
        # tau_0, k_tau
        (1.5, 3.0), (1.0, 12.0),
        # K_BL, tau_c_BL
        (0.5, 12.0), (1.5, 3.5),
        # poly3 a0..a3
        (-6.0, 4.0), (-6.0, 6.0), (-8.0, 8.0), (-5.0, 5.0),
        # beta_pf, k_pf, p_c
        (-1.0, 1.0), (1.0, 80.0), (0.05, 0.95),
        # beta_lin, tau_c_win, s_win
        (-3.0, 3.0), (1.5, 3.5), (0.05, 1.0),
        # beta_gb, k_gb
        (-1.0, 1.0), (1.0, 12.0),
        # NEW: beta_T, beta_G
        (-3.0, 3.0), (-3.0, 3.0),
        # NEW: beta_L, L_star
        (-1.0, 1.0), (5.0, 200.0),
    ]


def fit_v46(df, n_start=30):
    bounds = _bounds_v46()
    rng = np.random.default_rng(42)
    best = None
    for s in range(n_start):
        x0 = [rng.uniform(*b) for b in bounds]
        def loss(p):
            try:
                pred = predict_v46(df, p)
                err = np.log(df['sigma'].values + 1e-12) - np.log(pred + 1e-12)
                if not np.all(np.isfinite(err)):
                    return 1e9
                base_loss = float(np.mean(err ** 2))
                # Soft penalty for out-of-bounds (Nelder-Mead doesn't always
                # enforce hard bounds even when passed; quadratic ramp keeps
                # the optimizer inside the physically meaningful region).
                penalty = 0.0
                for v, (lo, hi) in zip(p, bounds):
                    if v < lo:
                        penalty += (lo - v) ** 2
                    elif v > hi:
                        penalty += (v - hi) ** 2
                return base_loss + 100.0 * penalty
            except Exception:
                return 1e9
        # Pass bounds explicitly (Nelder-Mead supports it in scipy 1.7+).
        res = minimize(loss, x0, method='Nelder-Mead',
                       bounds=bounds,
                       options={'maxiter': 12000, 'xatol': 1e-7, 'fatol': 1e-9})
        if best is None or res.fun < best.fun:
            best = res
    return best.x


def loocv_v46(df, n_start_inner=4):
    n = len(df); pred_loo = np.empty(n)
    for i in range(n):
        sub = df.drop(df.index[i]).reset_index(drop=True)
        params = fit_v46(sub, n_start=n_start_inner)
        held = df.iloc[[i]]
        pred_loo[i] = predict_v46(held, params)[0]
        if (i + 1) % 10 == 0:
            print(f'  LOOCV progress: {i+1}/{n}')
    a = np.log(df['sigma'].values + 1e-12); p = np.log(pred_loo + 1e-12)
    return 1 - np.sum((a-p)**2)/np.sum((a-a.mean())**2), pred_loo


def main():
    cases = load_cases()
    rows = enrich(load_phys_rows(cases))
    df = pd.DataFrame(rows)
    print(f'Loaded {len(df)} cases.')

    print('\n' + '=' * 80)
    print('v46 FORM (v29 + plastic C-extensions, canonical exponents fixed)')
    print('=' * 80)
    print('  σ = exp(C_corr) · C_blend^phys(τ) · σ_grain ·')
    print('      (φ - φ_c)^0.5 · CN^1.5 · cov^0.4 · f_perc^3')
    print('')
    print('  Fixed: α=0.5, β=1.5, γ=0.4, δ=3, σ_grain=3.0 mS/cm')
    print('  Free  (~22 params, all in C_blend + C_corr):')
    print('    base:     φ_c')
    print('    C_blend:  C_thick, C_thin, τ_0, k_τ, K_BL, τ_c_BL, poly3 (4)')
    print('    C_corr:   β_pf, k_pf, p_c, β_lin, τ_c_win, σ_τ_win, β_gb, k_gb')
    print('    NEW:      β_T (Tabor), β_G (geom), β_L (finite-size), L_*')

    print('\nFitting v46 (joint Nelder-Mead, 30 multi-starts) ...')
    params = fit_v46(df, n_start=30)
    pred = predict_v46(df, params)
    r2_in, w20_in = metrics(df['sigma'].values, pred)
    print(f'\n  Joint-fit R²={r2_in:.4f}  w20={w20_in}/{len(df)}')

    # Print fitted params
    p_names = ['phi_c',
               'C_thick','C_thin','tau_0','k_tau',
               'K_BL','tau_c_BL',
               'a0','a1','a2','a3',
               'beta_pf','k_pf','p_c',
               'beta_lin','tau_c_win','sigma_tau_win',
               'beta_gb','k_gb',
               'beta_T','beta_G',
               'beta_L','L_star']
    print('\nFitted parameters:')
    for n, v in zip(p_names, params):
        marker = '  ⭐' if n in ('beta_T','beta_G','beta_L') and abs(v) > 0.05 else ''
        print(f'  {n:18s} = {v:+.4f}{marker}')

    print('\nLOOCV (slow, ~30 min) ...')
    r2_loo, _ = loocv_v46(df, n_start_inner=3)
    err_loo_pred = predict_v46(df, params)
    err = np.abs(df['sigma'].values - err_loo_pred) / np.maximum(df['sigma'].values, 1e-12)
    w20_loo = int(np.sum(err <= 0.20))
    print(f'\n  LOOCV R²={r2_loo:.4f}')

    # ── Report ──
    print('\n' + '=' * 80)
    print('=== v46 RESULT ===')
    print('=' * 80)
    print(f'  R² (in-sample) = {r2_in:.4f}')
    print(f'  LOOCV R²       = {r2_loo:.4f}')
    print(f'  ±20% accuracy  = {w20_in}/{len(df)} (in-sample)')
    print(f'\n  Free params:    22 (all in C_blend + C_corr)')
    print(f'  Fixed exponents: α=1/2, β=3/2, γ=2/5, δ=3 (canonical)')

    print('\n  NEW plastic terms — interpretation:')
    print(f'    β_T (Tabor binding share)     = {params[19]:+.3f}')
    print(f'    β_G (geom binding share)       = {params[20]:+.3f}')
    print(f'    β_L (finite-size, log L/L_*)   = {params[21]:+.3f}')
    print(f'    L_*  (finite-size pivot)        = {params[22]:.1f} μm')

    out = Path('docs/figures/physics_regime')
    out.mkdir(parents=True, exist_ok=True)
    save = {
        'r2_in': float(r2_in), 'r2_loocv': float(r2_loo),
        'w20': w20_in, 'n': len(df),
        'param_names': p_names,
        'params': [float(v) for v in params],
        'fixed_exponents': {'alpha': ALPHA_FIX, 'beta': BETA_FIX,
                            'gamma': GAMMA_FIX, 'delta': DELTA_FIX,
                            'sigma_grain_mScm': SIGMA_GRAIN},
    }
    with open(out / 'physics_fit_v46_plastic_C.json', 'w') as f:
        json.dump(save, f, indent=2)
    print(f'\n→ {out}/physics_fit_v46_plastic_C.json')


if __name__ == '__main__':
    main()
