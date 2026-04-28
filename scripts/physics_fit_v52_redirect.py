#!/usr/bin/env python3
"""Physics-mode fit v52 — redirect collapsed slots to plastic-mode signals.

Hypothesis (per user insight): in physics-mode, several v29 sigmoid
coefficients collapse to zero (K_BL: 5.11→0.11, β_pf→0). Their
elastic-regime semantics no longer apply. Rather than removing those
slots, REDIRECT their input features to plastic-mode-specific signals
that DO carry signal — preserving the 15-parameter budget.

Two redirections (same form, different sigmoid inputs):

  C_blend blend weight:
      w_BL = σ(K_BL · (τ − τ_c_BL))     ← original (elastic regime via τ)
           ↓ replaced with ↓
      w_BL = σ(K_BL · (b_tabor · log τ − τ_c_BL))    ← v52

      Tabor binding share × log τ encodes "plastic regime activated
      under high tortuosity" — captures regime transitions specific
      to plastic film constriction.

  C_corr P:S sigmoid:
      w_pf = σ(k_pf · (p_frac − p_c))     ← original (elastic mode P:S effect)
           ↓ replaced with ↓
      w_pf = σ(k_pf · (b_tabor/(b_geom+ε) − p_c))    ← v52

      Tabor/geom binding ratio encodes plastic-film-vs-spreading
      balance per contact — replaces P:S elastic-mode signature.

All other v29 components UNCHANGED (canonical exponents, v5 asymptotes,
poly3, τ-bump, GB). Total 15 params (same as v29 baseline). Same
sigmoid structure, only INPUT FEATURES are physics-aware.

Comparison vs v29 baseline (LOOCV=0.8977 from v48 F0):
  ΔLOOCV > +0.005 → v52 is the publication form upgrade
  ΔLOOCV ≈ 0      → redirected inputs equivalent, choose simpler
  ΔLOOCV < 0      → original elastic semantics still better
"""
from __future__ import annotations
import sys, json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.optimize import minimize

SCRIPTS = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS))
from physics_fit_v33_binding import load_phys_rows  # noqa: E402
from v32_exhaustive_refit import load_cases  # noqa: E402
from physics_fit_v48_full_v29_betaT import (  # noqa: E402
    enrich, _bounds_v29_full, _sigmoid, metrics_simple,
    SIGMA_GRAIN, ALPHA_FIX, BETA_FIX, GAMMA_FIX, DELTA_FIX, PHI_C_FIX,
)


# ─────────────────────────────────────────────────────────────────────
# v52 predictor — same 15 params, but blend-weight and P:S sigmoid
# inputs redirected to plastic-mode-specific features.
# ─────────────────────────────────────────────────────────────────────
def predict_v52(df, params):
    """v29 form structure preserved. Two sigmoid inputs redirected:
       - blend weight uses (b_tabor · log τ) instead of τ
       - 'P:S' sigmoid uses (b_tabor/(b_geom+ε)) instead of p_frac

    Layout (15 params, IDENTICAL to v48 v29_full):
       0-1   C_thick, C_thin
       2-3   K_BL, blend_centre
       4-7   poly3 a0-a3
       8-10  k_pf, plastic_ratio_centre, beta_pf
      11-13  beta_lin, tau_c_win, s_win
      14    beta_gb
    Note: parameter SLOTS are unchanged; only the meanings of
    'blend_centre' and 'plastic_ratio_centre' differ from v29's
    'tau_c_BL' and 'p_c' (different units, different bounds).
    """
    (C_thick, C_thin, K_BL, blend_centre,
     a0, a1, a2, a3,
     k_pf, plastic_ratio_centre, beta_pf,
     beta_lin, tau_c_win, s_win,
     beta_gb) = params

    K_GB_FIX = 4.0

    phi = df['phi'].values
    tau = df['tau'].values
    cn  = df['cn'].values
    cov = df['cov_phys'].values
    f_p = df['f_perc'].values
    rho_gb = np.maximum(df['gb_dens'].values, 1e-6)
    b_T = df['b_tabor'].values / 100.0
    b_G = df['b_geom'].values  / 100.0

    # ── Base (canonical exponents fixed) ─────────────────────
    excess = np.maximum(phi - PHI_C_FIX, 1e-6)
    log_base = (np.log(SIGMA_GRAIN)
                + ALPHA_FIX * np.log(excess)
                + BETA_FIX  * np.log(cn)
                + GAMMA_FIX * np.log(cov)
                + DELTA_FIX * np.log(f_p))

    # ── C_blend: v5 sigmoid in τ ⊕ poly3 ─────────────────────
    s_v5 = _sigmoid(5.0 * (tau - 2.1))
    log_Cv5 = (np.log(max(C_thick, 1e-6))
               + (np.log(max(C_thin, 1e-6)) - np.log(max(C_thick, 1e-6))) * s_v5)
    ln_t = np.log(np.maximum(tau, 0.01))
    log_Cp3 = a0 + a1 * ln_t + a2 * ln_t ** 2 + a3 * ln_t ** 3

    # *** REDIRECTED: blend weight input is now b_tabor · log τ ***
    # Captures "plastic regime activated under high tortuosity".
    blend_input = b_T * ln_t
    w_BL = _sigmoid(K_BL * (blend_input - blend_centre))
    log_Cblend = (1 - w_BL) * log_Cv5 + w_BL * log_Cp3

    # ── C_corr: 3 terms ──────────────────────────────────────
    # *** REDIRECTED: P:S sigmoid input is now b_tabor/(b_geom+ε) ***
    # Captures Tabor-vs-geom binding balance (plastic-film severity).
    eps = 0.05  # avoid divide-by-zero when geom share ≈ 0
    plastic_ratio = b_T / (b_G + eps)
    w_pf = _sigmoid(k_pf * (plastic_ratio - plastic_ratio_centre))
    w_pf_c = w_pf - float(np.mean(w_pf))

    # τ-bump (unchanged from v29)
    w_win = np.exp(-((tau - tau_c_win) / max(s_win, 0.05)) ** 2 / 2.0)
    pwwin = w_win  # NOTE: original v29 multiplied p_frac × w_win;
                    # since p_frac slot redirected, just use w_win directly.
    pwwin_c = pwwin - float(np.mean(pwwin))

    # GB (unchanged from v29)
    ln_gb = np.log(rho_gb)
    w_gb = _sigmoid(K_GB_FIX * (ln_gb - float(np.median(ln_gb))))
    w_gb_c = w_gb - float(np.mean(w_gb))

    C_corr = beta_pf * w_pf_c + beta_lin * pwwin_c + beta_gb * w_gb_c

    return np.exp(log_base + log_Cblend + C_corr)


def _bounds_v52():
    """Same 15-slot structure but bounds adjusted for redirected inputs.
       blend_centre: b_tabor·log τ ranges roughly [0, 2] for our data
       plastic_ratio_centre: b_tabor/(b_geom+0.05) ranges roughly [0, 30]
    """
    return [
        (0.001, 0.5), (0.001, 0.5),         # C_thick, C_thin
        (0.5, 12.0), (-1.0, 3.0),             # K_BL, blend_centre (b_T·log τ)
        (-6.0, 4.0), (-6.0, 6.0), (-8.0, 8.0), (-5.0, 5.0),  # poly3
        (0.05, 5.0),                          # k_pf (smaller because input range larger)
        (0.0, 30.0),                          # plastic_ratio_centre
        (-1.0, 1.0),                          # beta_pf
        (-3.0, 3.0), (1.5, 3.5), (0.05, 1.0), # τ-bump
        (-1.0, 1.0),                          # beta_gb
    ]


def fit_v52(df, n_start=25):
    bounds = _bounds_v52()
    rng = np.random.default_rng(52)
    best = None
    for s in range(n_start):
        x0 = [rng.uniform(*b) for b in bounds]
        def loss(p):
            try:
                pred = predict_v52(df, p)
                err = np.log(df['sigma'].values + 1e-12) - np.log(pred + 1e-12)
                if not np.all(np.isfinite(err)): return 1e9
                base_loss = float(np.mean(err ** 2))
                penalty = sum((max(0, lo - v) + max(0, v - hi)) ** 2
                              for v, (lo, hi) in zip(p, bounds))
                return base_loss + 100.0 * penalty
            except Exception:
                return 1e9
        res = minimize(loss, x0, method='Nelder-Mead', bounds=bounds,
                       options={'maxiter': 8000, 'xatol': 1e-7, 'fatol': 1e-9})
        if best is None or res.fun < best.fun:
            best = res
    return best.x


def loocv_v52(df, n_start_inner=4):
    n = len(df); pred_loo = np.empty(n)
    for i in range(n):
        sub = df.drop(df.index[i]).reset_index(drop=True)
        params = fit_v52(sub, n_start=n_start_inner)
        held = df.iloc[[i]]
        pred_loo[i] = predict_v52(held, params)[0]
        if (i + 1) % 10 == 0:
            print(f'    progress: {i+1}/{n}', flush=True)
    a = np.log(df['sigma'].values + 1e-12); p = np.log(pred_loo + 1e-12)
    return 1 - np.sum((a-p)**2) / np.sum((a-a.mean())**2)


def main():
    cases = load_cases()
    rows = enrich(load_phys_rows(cases))
    df = pd.DataFrame(rows)
    print(f'Loaded {len(df)} cases.', flush=True)

    print('\n' + '=' * 80, flush=True)
    print('v52 — collapsed slots redirected to plastic-mode features', flush=True)
    print('=' * 80, flush=True)
    print('  Same 15-param structure as v29; two sigmoid inputs redirected:', flush=True)
    print('    blend weight:  τ              → b_tabor · log(τ)', flush=True)
    print('    P:S sigmoid:   p_frac         → b_tabor / (b_geom + 0.05)', flush=True)

    print('\nFitting v52 (joint Nelder-Mead, 25 starts) ...', flush=True)
    params = fit_v52(df, n_start=25)
    pred = predict_v52(df, params)
    r2_in, w20_in = metrics_simple(df['sigma'].values, pred)
    print(f'\n  In-sample R²={r2_in:.4f}  w20={w20_in}/{len(df)}', flush=True)

    p_names = ['C_thick','C_thin','K_BL','blend_centre',
               'a0','a1','a2','a3',
               'k_pf','plastic_ratio_centre','beta_pf',
               'beta_lin','tau_c_win','sigma_tau_win','beta_gb']
    print('\nFitted parameters:', flush=True)
    for n, v in zip(p_names, params):
        print(f'  {n:24s} = {v:+.4f}', flush=True)

    print('\nLOOCV (76 folds × 4 inner starts) ...', flush=True)
    loocv = loocv_v52(df, n_start_inner=4)
    print(f'\n  LOOCV R²={loocv:.4f}', flush=True)

    # Verdict
    v29_loocv = 0.8977   # v48 F0 baseline
    delta = loocv - v29_loocv
    print('\n' + '=' * 80, flush=True)
    print('=== VERDICT ===', flush=True)
    print('=' * 80, flush=True)
    print(f'  v29 baseline (v48 F0):     LOOCV = {v29_loocv:.4f}', flush=True)
    print(f'  v52 (redirected slots):    LOOCV = {loocv:.4f}', flush=True)
    print(f'  ΔLOOCV = {delta:+.4f}', flush=True)
    if delta > 0.005:
        print('\n  🎯 v52 IS A REAL UPGRADE — collapsed slots redirected '
              'successfully to plastic-mode features.', flush=True)
        print('     Same 15-param budget, better generalisation.', flush=True)
    elif delta > -0.002:
        print('\n  ≈ Tied. Original v29 inputs and redirected inputs '
              'equivalent — choose v29 for narrative continuity.', flush=True)
    else:
        print(f'\n  ❌ Redirected inputs degrade LOOCV by {-delta:.3f}. '
              'Original elastic-mode semantics still help in physics.', flush=True)

    out = Path('docs/figures/physics_regime')
    out.mkdir(parents=True, exist_ok=True)
    save = {
        'r2_in': float(r2_in), 'r2_loocv': float(loocv),
        'w20': w20_in, 'n': len(df),
        'param_names': p_names,
        'params': [float(v) for v in params],
        'delta_loocv_vs_v29': float(delta),
    }
    with open(out / 'physics_fit_v52_redirect.json', 'w') as f:
        json.dump(save, f, indent=2)
    print(f'\n→ {out}/physics_fit_v52_redirect.json', flush=True)


if __name__ == '__main__':
    main()
