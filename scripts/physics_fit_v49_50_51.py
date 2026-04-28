#!/usr/bin/env python3
"""Physics-mode fit v49+50+51 — three remaining-to-try variants.

After v48 confirmed v29's LOOCV=0.90 as the proper baseline (vs v34's
unphysical-exponent 0.96), three families remained worth checking:

  v49 — v29 + regime-aware C_blend asymptotes (17p)
        Canonical exponents fixed; only (C_thick, C_thin) split per
        τ-regime. +2 params over v29. Tests whether the regime
        signal v34 captured can be recovered without breaking
        canonical exponents.

  v50 — 3-way regime split with canonical exponents (3 × ?p)
        cluster (1mAh ∩ p:s=5:5) / thick non-cluster / thin non-cluster
        Each fitted with v29 form (canonical exp fixed), independent
        C_blend and C_corr coefficients per regime. Reports per-regime
        LOOCV and concat'd combined LOOCV.

  v51 — v29 + b_tabor × τ interaction (16p)
        v33 found b_tabor share = 0 by itself on residuals; v48 found
        b_tabor × constant = degraded LOOCV. But b_tabor × τ might
        capture a regime-dependent plastic effect that escaped both.

Each variant's verdict by ΔLOOCV vs v48 F0 baseline (0.8977).
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
    enrich, predict_v29_full, _bounds_v29_full, _sigmoid,
    metrics_simple, SIGMA_GRAIN, ALPHA_FIX, BETA_FIX, GAMMA_FIX,
    DELTA_FIX, PHI_C_FIX,
)

WEBAPP = SCRIPTS.parent / 'webapp'
TAU_SPLIT = 1.5


# ─────────────────────────────────────────────────────────────────────
# v49 — v29 + regime-aware C_blend asymptotes
# ─────────────────────────────────────────────────────────────────────
def predict_v49(df, params):
    """v29 with (C_thick, C_thin) split per τ-regime.

    Layout (17 params): same as v29 but with two extra:
       0-1   C_thick_n, C_thin_n            (¬thick regime asymptotes)
       2-3   K_BL, tau_c_BL
       4-7   poly3 (a0..a3)
       8-10  beta_pf, k_pf, p_c
      11-13  beta_lin, tau_c_win, s_win
      14    beta_gb
      15-16 C_thick_t, C_thin_t              (thick regime asymptotes — NEW)
    """
    (C_thick_n, C_thin_n, K_BL, tau_c_BL,
     a0, a1, a2, a3,
     beta_pf, k_pf, p_c,
     beta_lin, tau_c_win, s_win,
     beta_gb,
     C_thick_t, C_thin_t) = params

    K_GB_FIX = 4.0
    phi = df['phi'].values; tau = df['tau'].values; cn = df['cn'].values
    cov = df['cov_phys'].values; f_p = df['f_perc'].values
    p   = df['p_frac'].values
    rho_gb = np.maximum(df['gb_dens'].values, 1e-6)
    is_thick = (tau < TAU_SPLIT).astype(float)

    excess = np.maximum(phi - PHI_C_FIX, 1e-6)
    log_base = (np.log(SIGMA_GRAIN)
                + ALPHA_FIX * np.log(excess) + BETA_FIX * np.log(cn)
                + GAMMA_FIX * np.log(cov) + DELTA_FIX * np.log(f_p))

    s_v5 = _sigmoid(5.0 * (tau - 2.1))
    # Regime-specific v5 asymptotes
    log_Cv5_n = (np.log(max(C_thick_n, 1e-6))
                 + (np.log(max(C_thin_n, 1e-6)) - np.log(max(C_thick_n, 1e-6))) * s_v5)
    log_Cv5_t = (np.log(max(C_thick_t, 1e-6))
                 + (np.log(max(C_thin_t, 1e-6)) - np.log(max(C_thick_t, 1e-6))) * s_v5)
    log_Cv5 = (1 - is_thick) * log_Cv5_n + is_thick * log_Cv5_t

    ln_t = np.log(np.maximum(tau, 0.01))
    log_Cp3 = a0 + a1 * ln_t + a2 * ln_t ** 2 + a3 * ln_t ** 3
    w_BL = _sigmoid(K_BL * (tau - tau_c_BL))
    log_Cblend = (1 - w_BL) * log_Cv5 + w_BL * log_Cp3

    w_pf = _sigmoid(k_pf * (p - p_c)); w_pf_c = w_pf - float(np.mean(w_pf))
    w_win = np.exp(-((tau - tau_c_win) / max(s_win, 0.05)) ** 2 / 2.0)
    pwwin = p * w_win; pwwin_c = pwwin - float(np.mean(pwwin))
    ln_gb = np.log(rho_gb)
    w_gb = _sigmoid(K_GB_FIX * (ln_gb - float(np.median(ln_gb))))
    w_gb_c = w_gb - float(np.mean(w_gb))
    C_corr = beta_pf * w_pf_c + beta_lin * pwwin_c + beta_gb * w_gb_c
    return np.exp(log_base + log_Cblend + C_corr)


def _bounds_v49():
    return _bounds_v29_full() + [(0.001, 0.5), (0.001, 0.5)]


def fit_v49(df, n_start=25):
    bounds = _bounds_v49()
    rng = np.random.default_rng(49)
    best = None
    for s in range(n_start):
        x0 = [rng.uniform(*b) for b in bounds]
        def loss(p):
            try:
                pred = predict_v49(df, p)
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


# ─────────────────────────────────────────────────────────────────────
# v50 — 3-way regime split, canonical exponents fixed per regime
# ─────────────────────────────────────────────────────────────────────
def fit_v50_regime(df_sub, label, n_start=15):
    """Fit v29 form (canonical exp fixed) on one subset."""
    if len(df_sub) < 5:
        print(f'  {label}: n={len(df_sub)} (too few)')
        return None
    bounds = _bounds_v29_full()
    rng = np.random.default_rng(50)
    best = None
    for s in range(n_start):
        x0 = [rng.uniform(*b) for b in bounds]
        def loss(p):
            try:
                pred = predict_v29_full(df_sub, p)
                err = np.log(df_sub['sigma'].values + 1e-12) - np.log(pred + 1e-12)
                if not np.all(np.isfinite(err)): return 1e9
                base_loss = float(np.mean(err ** 2))
                penalty = sum((max(0, lo - v) + max(0, v - hi)) ** 2
                              for v, (lo, hi) in zip(p, bounds))
                return base_loss + 100.0 * penalty
            except Exception:
                return 1e9
        res = minimize(loss, x0, method='Nelder-Mead', bounds=bounds,
                       options={'maxiter': 6000, 'xatol': 1e-7, 'fatol': 1e-9})
        if best is None or res.fun < best.fun:
            best = res
    return best.x


# ─────────────────────────────────────────────────────────────────────
# v51 — v29 + b_tabor × τ interaction
# ─────────────────────────────────────────────────────────────────────
def predict_v51(df, params):
    """v29 + β_T_tau · b_tabor · log(τ)"""
    base_params = params[:15]
    beta_T_tau = params[15]
    base_pred = predict_v29_full(df, base_params)
    b_T = df['b_tabor'].values / 100.0
    tau = df['tau'].values
    feat = b_T * np.log(np.maximum(tau, 0.01))
    feat_c = feat - float(np.mean(feat))
    return base_pred * np.exp(beta_T_tau * feat_c)


def fit_v51(df, n_start=25):
    bounds = _bounds_v29_full() + [(-3.0, 3.0)]
    rng = np.random.default_rng(51)
    best = None
    for s in range(n_start):
        x0 = [rng.uniform(*b) for b in bounds]
        def loss(p):
            try:
                pred = predict_v51(df, p)
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


# ─────────────────────────────────────────────────────────────────────
# Generic LOOCV
# ─────────────────────────────────────────────────────────────────────
def loocv_generic(df, fit_fn, predict_fn, n_start_inner=4):
    n = len(df); pred_loo = np.empty(n)
    for i in range(n):
        sub = df.drop(df.index[i]).reset_index(drop=True)
        params = fit_fn(sub, n_start=n_start_inner)
        held = df.iloc[[i]]
        pred_loo[i] = predict_fn(held, params)[0]
        if (i + 1) % 10 == 0:
            print(f'    progress: {i+1}/{n}', flush=True)
    a = np.log(df['sigma'].values + 1e-12); p = np.log(pred_loo + 1e-12)
    return 1 - np.sum((a-p)**2) / np.sum((a-a.mean())**2)


def main():
    cases = load_cases()
    rows = enrich(load_phys_rows(cases))
    df = pd.DataFrame(rows)
    print(f'Loaded {len(df)} cases.', flush=True)

    results = {}

    # ─── v49 ────────────────────────────────────────────────
    print('\n' + '=' * 80, flush=True)
    print('v49 — v29 + regime-aware C_blend asymptotes (17p)', flush=True)
    print('=' * 80, flush=True)
    p49 = fit_v49(df, n_start=25)
    pred49 = predict_v49(df, p49)
    r2_49, w20_49 = metrics_simple(df['sigma'].values, pred49)
    print(f'  Joint-fit R²={r2_49:.4f}  w20={w20_49}/{len(df)}', flush=True)
    print(f'  ¬thick: C_thick={p49[0]:.4f}  C_thin={p49[1]:.4f}', flush=True)
    print(f'  thick:  C_thick={p49[15]:.4f}  C_thin={p49[16]:.4f}', flush=True)
    print('  LOOCV (v49) ...', flush=True)
    loocv_49 = loocv_generic(df, fit_v49, predict_v49, n_start_inner=4)
    print(f'  LOOCV R²={loocv_49:.4f}', flush=True)
    results['v49'] = {'r2': r2_49, 'loocv': loocv_49, 'w20': w20_49,
                      'k': 17, 'params': list(p49)}

    # ─── v50 ────────────────────────────────────────────────
    print('\n' + '=' * 80, flush=True)
    print('v50 — 3-way regime split (canonical exp fixed per regime)', flush=True)
    print('=' * 80, flush=True)
    name = df['name'].astype(str)
    is_1mAh = name.str.contains('1mAh', case=False, na=False).values
    p5050 = (np.abs(df['p_frac'].values - 0.5) < 0.05)
    is_cluster = is_1mAh & p5050
    sub_cluster = df[is_cluster].reset_index(drop=True)
    sub_thick   = df[(~is_cluster) & (df['tau'] <  1.5)].reset_index(drop=True)
    sub_thin    = df[(~is_cluster) & (df['tau'] >= 1.5)].reset_index(drop=True)
    print(f'  cluster (1mAh∩5050): n={len(sub_cluster)}', flush=True)
    print(f'  thick non-cluster:   n={len(sub_thick)}', flush=True)
    print(f'  thin non-cluster:    n={len(sub_thin)}', flush=True)

    p_cluster = fit_v50_regime(sub_cluster, 'cluster', n_start=15)
    p_thick   = fit_v50_regime(sub_thick,   'thick',   n_start=15)
    p_thin    = fit_v50_regime(sub_thin,    'thin',    n_start=15)

    preds_concat = []
    sigmas_concat = []
    per_regime = {}
    for name_r, sub, params in [('cluster', sub_cluster, p_cluster),
                                  ('thick', sub_thick, p_thick),
                                  ('thin', sub_thin, p_thin)]:
        if params is None: continue
        pr = predict_v29_full(sub, params)
        r2, w20 = metrics_simple(sub['sigma'].values, pr)
        per_regime[name_r] = {'n': len(sub), 'r2': r2, 'w20': w20,
                               'params': list(params)}
        print(f'  {name_r:8s}: in-sample R²={r2:.4f}  w20={w20}/{len(sub)}',
              flush=True)
        preds_concat.append(pr); sigmas_concat.append(sub['sigma'].values)

    pred_all = np.concatenate(preds_concat); sig_all = np.concatenate(sigmas_concat)
    a = np.log(sig_all+1e-12); p = np.log(pred_all+1e-12)
    r2_combo = 1 - np.sum((a-p)**2)/np.sum((a-a.mean())**2)
    err = np.abs(sig_all - pred_all) / np.maximum(sig_all, 1e-12)
    w20_combo = int(np.sum(err <= 0.20))
    print(f'  combined: R²={r2_combo:.4f}  w20={w20_combo}/{len(sig_all)}', flush=True)
    results['v50'] = {'per_regime': per_regime, 'r2_combo': r2_combo,
                       'w20_combo': w20_combo, 'n_total': len(sig_all),
                       'k_total': sum(15 for v in per_regime.values())}

    # ─── v51 ────────────────────────────────────────────────
    print('\n' + '=' * 80, flush=True)
    print('v51 — v29 + b_tabor × log(τ) interaction (16p)', flush=True)
    print('=' * 80, flush=True)
    p51 = fit_v51(df, n_start=25)
    pred51 = predict_v51(df, p51)
    r2_51, w20_51 = metrics_simple(df['sigma'].values, pred51)
    print(f'  Joint-fit R²={r2_51:.4f}  w20={w20_51}/{len(df)}', flush=True)
    print(f'  β_T_tau = {p51[15]:+.4f}', flush=True)
    print('  LOOCV (v51) ...', flush=True)
    loocv_51 = loocv_generic(df, fit_v51, predict_v51, n_start_inner=4)
    print(f'  LOOCV R²={loocv_51:.4f}', flush=True)
    results['v51'] = {'r2': r2_51, 'loocv': loocv_51, 'w20': w20_51,
                      'k': 16, 'params': list(p51)}

    # ─── Summary ────────────────────────────────────────────
    print('\n' + '=' * 80, flush=True)
    print('=== v49 / v50 / v51 vs v48 baseline ===', flush=True)
    print('=' * 80, flush=True)
    v29_loocv = 0.8977   # v48 F0
    print(f'  v29 baseline (v48 F0):                LOOCV = {v29_loocv:.4f}', flush=True)
    print(f'  v49 (regime-aware C_blend):           LOOCV = {results["v49"]["loocv"]:.4f}  '
          f'(Δ = {results["v49"]["loocv"] - v29_loocv:+.4f})', flush=True)
    print(f'  v50 (3-way concat in-sample):         R²    = {results["v50"]["r2_combo"]:.4f}  '
          f'(no LOOCV — n too few per regime)', flush=True)
    print(f'  v51 (b_tabor × log(τ) interaction):   LOOCV = {results["v51"]["loocv"]:.4f}  '
          f'(Δ = {results["v51"]["loocv"] - v29_loocv:+.4f})', flush=True)

    out = Path('docs/figures/physics_regime')
    out.mkdir(parents=True, exist_ok=True)
    with open(out / 'physics_fit_v49_50_51.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print(f'\n→ {out}/physics_fit_v49_50_51.json', flush=True)


if __name__ == '__main__':
    main()
