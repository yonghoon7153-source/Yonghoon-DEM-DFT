#!/usr/bin/env python3
"""Physics-mode fit v53 — Lasso sweep over rich feature library.

The user pushed: "we haven't found something yet, keep digging." Untried
angles after v33-v52:
  • Hertzian-mode network-solver outputs as features for Physics-mode
    target (sigma_full_H, tau_Lap_eff_H, sigma_constr_H, etc.).
    Different mode = potentially independent signal.
  • Cross-mode ratios (Hertzian/Physics deltas as plastic-shift proxies).
  • Polynomial transforms, log/sqrt transforms, interaction products.
  • L1 regularization (Lasso) to AUTOMATICALLY select which combination
    of 30+ candidate features survives without overfit.

Strategy:
  1. Build a rich feature library (~35 features):
      - v29-style: log(phi-phic), log(CN), log(cov), log(f_perc), log(tau)
      - Hertzian-mode: log(sigma_H), log(tau_eff_H), log(sigma_constr_H)
      - Cross-mode ratios: log(sigma_H/sigma_P) if available, etc.
      - Binding shares: b_tabor, b_geom, b_ligg, b_hertzian
      - Composition: p_frac, log(thickness), is_thin
      - Interactions: phi*tau, CN*cov, cov*f_perc, etc.
      - Quadratic: phi^2, tau^2, CN^2

  2. Standardize all features (zero mean, unit variance).

  3. Fit log(sigma_P) target with LassoCV (10-fold CV chooses optimal
     alpha automatically, balancing fit vs regularization).

  4. Report which features survived (non-zero coefficient), with
     coefficient magnitudes and signs. LOOCV computed properly.

  5. Compare against v29 baseline (LOOCV=0.8977).

If LassoCV picks features that v29 doesn't capture, we have a signal.
If it just rediscovers v29 features, v29 confirmed optimal.
"""
from __future__ import annotations
import sys, json, warnings
from pathlib import Path
import numpy as np
import pandas as pd

SCRIPTS = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS))
from physics_fit_v33_binding import load_phys_rows  # noqa: E402
from v32_exhaustive_refit import load_cases  # noqa: E402

WEBAPP = SCRIPTS.parent / 'webapp'
warnings.filterwarnings('ignore')


def _read_full_metrics(cid):
    for base in ('results', 'archive'):
        for p in (WEBAPP / base).rglob(f'{cid}/full_metrics.json'):
            try: return json.load(open(p))
            except: pass
    return None


def enrich_full(rows):
    out = []
    for r in rows:
        m = _read_full_metrics(r['case_id']) or {}
        r2 = dict(r)
        r2['thickness']    = float(m.get('thickness_um', 0) or 0)
        r2['porosity']     = float(m.get('porosity', 0) or 0)
        # Hertzian-mode network outputs
        r2['sigma_H']      = float(m.get('sigma_full_mScm', 0) or 0)
        r2['sigma_bulk_H'] = float(m.get('sigma_bulk_net_mScm', 0) or 0)
        r2['sigma_cf_H']   = float(m.get('sigma_constr_only_mScm') or
                                    m.get('sigma_constr_mScm', 0) or 0)
        r2['constr_pct_H'] = float(m.get('constriction_fraction_pct') or
                                    m.get('constriction_pct', 0) or 0)
        out.append(r2)
    return out


def build_feature_library(df):
    """Return (X dataframe, names list). All features in log/normalised
    space where appropriate so Lasso can find linear combinations.
    """
    X = pd.DataFrame()

    # ── v29-style power-law arguments (log space) ────────────
    excess = np.maximum(df['phi'].values - 0.20, 1e-6)
    X['log_excess']    = np.log(excess)
    X['log_CN']        = np.log(np.maximum(df['cn'].values, 1e-3))
    X['log_cov']       = np.log(np.maximum(df['cov_phys'].values, 1e-3))
    X['log_f_perc']    = np.log(np.maximum(df['f_perc'].values, 1e-3))
    X['log_tau']       = np.log(np.maximum(df['tau'].values, 1e-3))

    # ── Hertzian-mode outputs (NEW — different network mode) ─
    X['log_sigma_H']      = np.log(np.maximum(df['sigma_H'].values, 1e-6))
    X['log_sigma_bulk_H'] = np.log(np.maximum(df['sigma_bulk_H'].values, 1e-6))
    X['log_sigma_cf_H']   = np.log(np.maximum(df['sigma_cf_H'].values, 1e-6))
    # Hertzian τ_Lap_eff = sqrt(phi · 3 / sigma_H)
    sig_H = np.maximum(df['sigma_H'].values, 1e-6)
    tau_eff_H = np.sqrt(np.maximum(df['phi'].values * 3.0 / sig_H, 1e-6))
    X['log_tau_eff_H'] = np.log(tau_eff_H)
    # Constriction-bulk ratio in Hertzian
    sig_bulk = np.maximum(df['sigma_bulk_H'].values, 1e-6)
    X['log_constr_share_H'] = np.log(sig_H / sig_bulk + 1e-9)

    # ── Binding shares (per-contact) ─────────────────────────
    X['b_tabor']    = df['b_tabor'].values / 100.0
    X['b_geom']     = df['b_geom'].values / 100.0
    X['b_hertzian'] = df['b_hertzian'].values / 100.0
    X['b_liggghts'] = df['b_liggghts'].values / 100.0

    # ── Composition / structural ─────────────────────────────
    X['p_frac']        = df['p_frac'].values
    X['log_thickness'] = np.log(np.maximum(df['thickness'].values, 1.0))
    X['is_thin']       = (df['thickness'].values < 50).astype(float)
    X['log_gb']        = np.log(np.maximum(df['gb_dens'].values, 1e-6))
    X['porosity']      = df['porosity'].values / 100.0

    # ── Interactions (pairwise log products) ─────────────────
    X['log_excess__log_CN']   = X['log_excess'] * X['log_CN']
    X['log_cov__log_f_perc']  = X['log_cov'] * X['log_f_perc']
    X['log_tau__log_CN']      = X['log_tau'] * X['log_CN']
    X['log_tau__b_tabor']     = X['log_tau'] * X['b_tabor']
    X['log_tau__log_thickness'] = X['log_tau'] * X['log_thickness']
    X['p_frac__b_tabor']      = X['p_frac'] * X['b_tabor']

    # ── Quadratic (centered) ─────────────────────────────────
    X['log_excess_sq']  = X['log_excess'] ** 2
    X['log_tau_sq']     = X['log_tau'] ** 2
    X['log_CN_sq']      = X['log_CN'] ** 2
    X['b_tabor_sq']     = X['b_tabor'] ** 2

    return X.fillna(0).values, list(X.columns)


def main():
    cases = load_cases()
    rows = enrich_full(load_phys_rows(cases))
    df = pd.DataFrame(rows)
    print(f'Loaded {len(df)} cases.', flush=True)

    X, feat_names = build_feature_library(df)
    y = np.log(np.maximum(df['sigma'].values, 1e-12))   # target: log σ_P
    n, k = X.shape
    print(f'Feature library: {k} candidates', flush=True)

    # ── Standardise (zero mean, unit variance) ──────────────
    X_mean = X.mean(axis=0)
    X_std = X.std(axis=0) + 1e-9
    Xs = (X - X_mean) / X_std

    from sklearn.linear_model import LassoCV, Lasso
    from sklearn.model_selection import KFold, LeaveOneOut

    # ── 10-fold LassoCV: choose alpha automatically ─────────
    print('\nLassoCV (10-fold) selecting optimal alpha ...', flush=True)
    lcv = LassoCV(cv=10, max_iter=20000, n_alphas=120,
                  fit_intercept=True, random_state=42)
    lcv.fit(Xs, y)
    alpha_best = lcv.alpha_
    print(f'  best alpha = {alpha_best:.5f}', flush=True)

    # ── In-sample R² with chosen alpha ──────────────────────
    coef = lcv.coef_
    intercept = lcv.intercept_
    pred = Xs @ coef + intercept
    ss_res = np.sum((y - pred) ** 2); ss_tot = np.sum((y - y.mean()) ** 2)
    r2_in = 1 - ss_res / ss_tot
    err = np.abs(np.exp(pred) - np.exp(y)) / np.maximum(np.exp(y), 1e-12)
    w20 = int(np.sum(err <= 0.20))
    print(f'\n  in-sample R² = {r2_in:.4f}  w20 = {w20}/{n}', flush=True)

    # ── Print survivors ─────────────────────────────────────
    nonzero_idx = np.where(np.abs(coef) > 1e-9)[0]
    print(f'\n  {len(nonzero_idx)}/{k} features survived L1:', flush=True)
    for i in sorted(nonzero_idx, key=lambda j: -abs(coef[j])):
        marker = '⭐' if 'log_sigma_H' in feat_names[i] or 'log_tau_eff_H' in feat_names[i] else ''
        print(f'    {feat_names[i]:30s}  γ = {coef[i]:+.4f}  {marker}', flush=True)

    # ── Strict LOOCV (refit Lasso each fold with same alpha) ─
    print('\nProper LOOCV (refit Lasso per fold) ...', flush=True)
    loo = LeaveOneOut()
    pred_loo = np.empty(n)
    for i, (tr, te) in enumerate(loo.split(Xs)):
        m = Lasso(alpha=alpha_best, max_iter=20000, fit_intercept=True)
        m.fit(Xs[tr], y[tr])
        pred_loo[te] = m.predict(Xs[te])[0]
        if (i + 1) % 10 == 0:
            print(f'  progress: {i+1}/{n}', flush=True)
    ss_res = np.sum((y - pred_loo) ** 2); ss_tot = np.sum((y - y.mean()) ** 2)
    r2_loo = 1 - ss_res / ss_tot
    err_loo = np.abs(np.exp(pred_loo) - np.exp(y)) / np.maximum(np.exp(y), 1e-12)
    w20_loo = int(np.sum(err_loo <= 0.20))
    print(f'\n  LOOCV R² = {r2_loo:.4f}  w20 = {w20_loo}/{n}', flush=True)

    # ── Verdict ────────────────────────────────────────────
    v29_loocv = 0.8977
    delta = r2_loo - v29_loocv
    print('\n' + '=' * 80, flush=True)
    print('=== VERDICT ===', flush=True)
    print('=' * 80, flush=True)
    print(f'  v29 baseline (15 params, hand-designed):  LOOCV = {v29_loocv:.4f}',
          flush=True)
    print(f'  v53 LassoCV ({len(nonzero_idx)} active feats):    LOOCV = {r2_loo:.4f}',
          flush=True)
    print(f'  ΔLOOCV = {delta:+.4f}', flush=True)
    if delta > 0.01:
        print('\n  🎯 LASSO FOUND NEW SIGNAL — investigate which features survived '
              'and whether they suggest a refined publication form.', flush=True)
    elif delta > 0:
        print('\n  Marginal improvement. Survivors confirm v29 covers '
              'most signal; small residual signal in some Hertzian-mode '
              'cross feature.', flush=True)
    else:
        print('\n  v29 still best. Even with L1 over 30+ features, no '
              'combination beats v29\'s hand-designed structure.', flush=True)

    # Save
    out = Path('docs/figures/physics_regime')
    out.mkdir(parents=True, exist_ok=True)
    save = {
        'alpha_best': float(alpha_best),
        'r2_in': float(r2_in), 'r2_loocv': float(r2_loo),
        'w20_in': w20_in, 'w20_loocv': w20_loo, 'n': n,
        'features_total': k,
        'features_active': len(nonzero_idx),
        'survivors': [{'name': feat_names[i],
                       'coef': float(coef[i])}
                      for i in sorted(nonzero_idx,
                                      key=lambda j: -abs(coef[j]))],
        'delta_loocv_vs_v29': float(delta),
    }
    with open(out / 'physics_fit_v53_lasso.json', 'w') as f:
        json.dump(save, f, indent=2)
    print(f'\n→ {out}/physics_fit_v53_lasso.json', flush=True)


if __name__ == '__main__':
    main()
