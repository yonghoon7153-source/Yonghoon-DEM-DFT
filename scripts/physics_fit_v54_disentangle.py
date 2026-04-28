#!/usr/bin/env python3
"""Physics-mode fit v54 — disentangle Hertzian vs structural signal.

v53 LassoCV achieved LOOCV=0.996 with sigma_bulk_H (γ=+0.62) and
sigma_H (γ=+0.20) as dominant features. Two questions to settle:

  Q1  Is sigma_bulk_H ALONE sufficient? (single-feature predictor)
      If yes → almost-circular, publication value limited.
      If no → genuine multi-feature signal.

  Q2  Without Hertzian-mode features, what's the structural-only
      LassoCV ceiling? Confirms v29's 0.90 floor under automatic
      feature selection.

Three runs:
  R1  sigma_bulk_H ONLY (1 feature + intercept)
  R2  sigma_bulk_H + sigma_H (2 features + intercept)
  R3  all v29 structural + binding features, NO Hertzian-mode outputs
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
from physics_fit_v53_lasso import enrich_full       # noqa: E402

WEBAPP = SCRIPTS.parent / 'webapp'
warnings.filterwarnings('ignore')


def run_lasso(X, feat_names, y, label):
    from sklearn.linear_model import LassoCV, Lasso
    from sklearn.model_selection import LeaveOneOut

    print(f'\n=== {label} ({X.shape[1]} candidate features) ===', flush=True)
    Xs = (X - X.mean(0)) / (X.std(0) + 1e-9)

    if X.shape[1] == 1:
        # 1-feature linear regression (no L1 needed)
        coef = np.array([np.sum((Xs[:, 0] - Xs[:, 0].mean()) * (y - y.mean())) /
                         np.sum((Xs[:, 0] - Xs[:, 0].mean()) ** 2)])
        intercept = y.mean() - coef[0] * Xs[:, 0].mean()
        alpha = 0.0
        pred = Xs @ coef + intercept
    else:
        lcv = LassoCV(cv=10, max_iter=20000, n_alphas=120,
                      fit_intercept=True, random_state=42)
        lcv.fit(Xs, y)
        coef = lcv.coef_; intercept = lcv.intercept_
        alpha = lcv.alpha_
        pred = Xs @ coef + intercept

    ss_res = np.sum((y - pred) ** 2); ss_tot = np.sum((y - y.mean()) ** 2)
    r2_in = 1 - ss_res / ss_tot
    err = np.abs(np.exp(pred) - np.exp(y)) / np.maximum(np.exp(y), 1e-12)
    w20_in = int(np.sum(err <= 0.20))
    print(f'  in-sample R²={r2_in:.4f}  w20={w20_in}/{len(y)}  alpha={alpha:.5f}',
          flush=True)

    nonzero = [(feat_names[i], float(coef[i])) for i in range(len(coef))
               if abs(coef[i]) > 1e-9]
    nonzero.sort(key=lambda t: -abs(t[1]))
    print(f'  active features ({len(nonzero)}):', flush=True)
    for n, g in nonzero[:10]:
        print(f'    {n:30s}  γ = {g:+.4f}', flush=True)

    # LOOCV
    n = len(y); pred_loo = np.empty(n); loo = LeaveOneOut()
    for i, (tr, te) in enumerate(loo.split(Xs)):
        if X.shape[1] == 1:
            x_tr = Xs[tr, 0]; y_tr = y[tr]
            c = np.sum((x_tr - x_tr.mean()) * (y_tr - y_tr.mean())) / \
                np.sum((x_tr - x_tr.mean()) ** 2)
            it = y_tr.mean() - c * x_tr.mean()
            pred_loo[te] = c * Xs[te, 0] + it
        else:
            m = Lasso(alpha=alpha, max_iter=20000, fit_intercept=True)
            m.fit(Xs[tr], y[tr])
            pred_loo[te] = m.predict(Xs[te])[0]
    ss_res = np.sum((y - pred_loo) ** 2); ss_tot = np.sum((y - y.mean()) ** 2)
    r2_loo = 1 - ss_res / ss_tot
    err_loo = np.abs(np.exp(pred_loo) - np.exp(y)) / np.maximum(np.exp(y), 1e-12)
    w20_loo = int(np.sum(err_loo <= 0.20))
    print(f'  LOOCV R²={r2_loo:.4f}  w20={w20_loo}/{len(y)}', flush=True)

    return {'r2_in': float(r2_in), 'r2_loocv': float(r2_loo),
            'w20_in': w20_in, 'w20_loocv': w20_loo,
            'alpha': float(alpha), 'survivors': nonzero,
            'k_active': len(nonzero), 'k_total': X.shape[1]}


def build_structural_only(df):
    """No Hertzian-mode network outputs."""
    X = pd.DataFrame()
    excess = np.maximum(df['phi'].values - 0.20, 1e-6)
    X['log_excess']    = np.log(excess)
    X['log_CN']        = np.log(np.maximum(df['cn'].values, 1e-3))
    X['log_cov']       = np.log(np.maximum(df['cov_phys'].values, 1e-3))
    X['log_f_perc']    = np.log(np.maximum(df['f_perc'].values, 1e-3))
    X['log_tau']       = np.log(np.maximum(df['tau'].values, 1e-3))
    X['b_tabor']       = df['b_tabor'].values / 100.0
    X['b_geom']        = df['b_geom'].values / 100.0
    X['b_hertzian']    = df['b_hertzian'].values / 100.0
    X['b_liggghts']    = df['b_liggghts'].values / 100.0
    X['p_frac']        = df['p_frac'].values
    X['log_thickness'] = np.log(np.maximum(df['thickness'].values, 1.0))
    X['is_thin']       = (df['thickness'].values < 50).astype(float)
    X['log_gb']        = np.log(np.maximum(df['gb_dens'].values, 1e-6))
    X['porosity']      = df['porosity'].values / 100.0
    # Interactions / quadratics (NO Hertzian features)
    X['log_excess__log_CN']     = X['log_excess'] * X['log_CN']
    X['log_cov__log_f_perc']    = X['log_cov'] * X['log_f_perc']
    X['log_tau__log_CN']        = X['log_tau'] * X['log_CN']
    X['log_tau__b_tabor']       = X['log_tau'] * X['b_tabor']
    X['log_tau__log_thickness'] = X['log_tau'] * X['log_thickness']
    X['p_frac__b_tabor']        = X['p_frac'] * X['b_tabor']
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
    y = np.log(np.maximum(df['sigma'].values, 1e-12))

    # ── R1: sigma_bulk_H ALONE ─────────────────────────────
    sig_bulk_H = np.log(np.maximum(df['sigma_bulk_H'].values, 1e-6))
    X1 = sig_bulk_H.reshape(-1, 1)
    R1 = run_lasso(X1, ['log_sigma_bulk_H'], y, 'R1: sigma_bulk_H ALONE')

    # ── R2: sigma_bulk_H + sigma_H (2 features) ────────────
    sig_H = np.log(np.maximum(df['sigma_H'].values, 1e-6))
    X2 = np.column_stack([sig_bulk_H, sig_H])
    R2 = run_lasso(X2, ['log_sigma_bulk_H', 'log_sigma_H'], y,
                    'R2: sigma_bulk_H + sigma_H')

    # ── R3: structural ONLY (no Hertzian features) ─────────
    X3, names3 = build_structural_only(df)
    R3 = run_lasso(X3, names3, y, 'R3: structural-only (no Hertzian)')

    # ── Summary ────────────────────────────────────────────
    v29_loocv = 0.8977
    print('\n' + '=' * 80, flush=True)
    print('=== SUMMARY ===', flush=True)
    print('=' * 80, flush=True)
    print(f'  v29 baseline:                   LOOCV = {v29_loocv:.4f}', flush=True)
    print(f'  R1 sigma_bulk_H alone:           LOOCV = {R1["r2_loocv"]:.4f}',
          flush=True)
    print(f'  R2 sigma_bulk_H + sigma_H:       LOOCV = {R2["r2_loocv"]:.4f}',
          flush=True)
    print(f'  R3 structural-only (Lasso 25f):  LOOCV = {R3["r2_loocv"]:.4f}',
          flush=True)
    print(f'  v53 hybrid (33 features):        LOOCV = 0.9960 (prior run)',
          flush=True)

    print('\n=== INTERPRETATION ===', flush=True)
    if R1['r2_loocv'] > 0.95:
        print('  R1 alone reaches >0.95 — sigma_bulk_H IS the dominant predictor.',
              flush=True)
        print('  Publication: "physics σ ≈ structural map of Hertzian σ_bulk"',
              flush=True)
    elif R1['r2_loocv'] > 0.85:
        print('  R1 alone solid but not perfect — multi-feature combination needed.',
              flush=True)
    else:
        print('  R1 alone weak — sigma_bulk_H + structural features needed jointly.',
              flush=True)

    if R3['r2_loocv'] >= 0.89 and R3['r2_loocv'] <= 0.92:
        print(f'  R3 structural-only at {R3["r2_loocv"]:.4f} confirms v29 ceiling.',
              flush=True)
    elif R3['r2_loocv'] > 0.92:
        print(f'  R3 structural-only at {R3["r2_loocv"]:.4f} EXCEEDS v29 — '
              'Lasso found better structural combination.', flush=True)
    else:
        print(f'  R3 structural-only at {R3["r2_loocv"]:.4f} below v29 — '
              'L1 regularisation too aggressive.', flush=True)

    out = Path('docs/figures/physics_regime')
    out.mkdir(parents=True, exist_ok=True)
    with open(out / 'physics_fit_v54_disentangle.json', 'w') as f:
        json.dump({'R1_sigma_bulk_H_alone': R1,
                   'R2_two_hertzian_features': R2,
                   'R3_structural_only': R3,
                   'v29_baseline_loocv': v29_loocv}, f, indent=2)
    print(f'\n→ {out}/physics_fit_v54_disentangle.json', flush=True)


if __name__ == '__main__':
    main()
