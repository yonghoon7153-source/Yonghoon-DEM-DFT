#!/usr/bin/env python3
"""Physics-mode fit v34 — regime-aware to break R²=0.96 ceiling.

Diagnostic from physics_fit_v33_binding.py revealed:
  • Combined fit:        R²=0.962 (n=76)
  • thick    (τ<1.5):    R²=0.976 (n=45)
  • moderate (1.5≤τ<2.5): R²=0.987 (n=26)  ← almost 0.99 alone
  • thin/extreme:        only 5 cases total (insufficient)

The combined fit is dragged down because the form's exponents differ
between thick and not-thick regimes. v29's smooth C_blend(τ) collapsed
in physics-mode fitting (K_BL → 0). This script tries hard regime
splits with two strategies:

  Strategy A — Independent per-regime fits
      Two completely separate v29 power-laws, one for τ<1.5 and one
      for τ≥1.5. Reports each fit's R²/LOOCV individually.

  Strategy B — Joint fit with regime interactions
      Single combined form, but with a binary indicator I_thick and
      interaction terms I_thick·CN, I_thick·cov, I_thick·τ, etc.
      One unified function but lets exponents differ across regimes.
      Total params ≈ 12 (vs 7 in single regime).

  Strategy C — Strategy B + binding share + r_SE/r_AM corrections
      Adds the v33 corrections inside the regime-aware base.

Goal: combined R² ≥ 0.99 and LOOCV ≥ 0.98 with one form that the
publication can quote as the unified scaling law.
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

SIGMA_GRAIN = 3.0
TAU_SPLIT = 1.5  # boundary between thick and not-thick


# ─────────────────────────────────────────────────────────────────────
# Strategy A — Independent per-regime fits
# ─────────────────────────────────────────────────────────────────────
def strategy_A(df):
    print('\n' + '=' * 75)
    print('STRATEGY A — Independent per-regime fits')
    print('=' * 75)
    print(f'  τ split @ τ = {TAU_SPLIT}')

    sub_thick = df[df['tau'] <  TAU_SPLIT].reset_index(drop=True)
    sub_thin  = df[df['tau'] >= TAU_SPLIT].reset_index(drop=True)
    print(f'  thick  (τ<{TAU_SPLIT}): n={len(sub_thick)}')
    print(f'  ¬thick (τ≥{TAU_SPLIT}): n={len(sub_thin)}')

    p_thick = fit_base(sub_thick, n_start=10)
    pred_thick = predict_base(sub_thick, p_thick)
    r2_t, w20_t = metrics(sub_thick['sigma'].values, pred_thick)
    loocv_t = loocv_r2(sub_thick, pred_thick)
    print(f'\n  thick :  R²={r2_t:.4f}  LOOCV={loocv_t:.4f}  '
          f'w20={w20_t}/{len(sub_thick)}')
    print('    base:', '  '.join(f'{n}={v:+.3f}' for n, v in zip(
        ('α','β','γ','δ','φc','μ','b0'), p_thick)))

    p_thin = fit_base(sub_thin, n_start=10)
    pred_thin = predict_base(sub_thin, p_thin)
    r2_n, w20_n = metrics(sub_thin['sigma'].values, pred_thin)
    loocv_n = loocv_r2(sub_thin, pred_thin)
    print(f'\n  ¬thick:  R²={r2_n:.4f}  LOOCV={loocv_n:.4f}  '
          f'w20={w20_n}/{len(sub_thin)}')
    print('    base:', '  '.join(f'{n}={v:+.3f}' for n, v in zip(
        ('α','β','γ','δ','φc','μ','b0'), p_thin)))

    # Combined R² across both subsets
    pred_all = np.concatenate([pred_thick, pred_thin])
    actual_all = np.concatenate([sub_thick['sigma'].values, sub_thin['sigma'].values])
    a = np.log(actual_all + 1e-12); p = np.log(pred_all + 1e-12)
    ss_res = np.sum((a - p) ** 2); ss_tot = np.sum((a - a.mean()) ** 2)
    r2_combo = 1 - ss_res / ss_tot if ss_tot > 0 else 0.0
    err = np.abs(actual_all - pred_all) / np.maximum(actual_all, 1e-12)
    w20_combo = int(np.sum(err <= 0.20))
    print(f'\n  ⇒ COMBINED across both subsets: R²={r2_combo:.4f}  '
          f'w20={w20_combo}/{len(df)}')
    return {
        'thick': {'r2': r2_t, 'loocv': loocv_t, 'w20': w20_t,
                  'n': len(sub_thick), 'params': list(p_thick)},
        'thin':  {'r2': r2_n, 'loocv': loocv_n, 'w20': w20_n,
                  'n': len(sub_thin),  'params': list(p_thin)},
        'combined': {'r2': r2_combo, 'w20': w20_combo, 'n': len(df)},
    }


# ─────────────────────────────────────────────────────────────────────
# Strategy B — Joint fit with regime interactions
# ─────────────────────────────────────────────────────────────────────
def predict_regime(df, params):
    """Joint form with thick-regime interactions:
         log σ = b0 + α·log(φ-φc) + β·log CN + γ·log cov
                 + δ·log f_p + μ·log τ
                 + I_thick·(α'·log(φ-φc) + β'·log CN
                             + γ'·log cov + δ'·log f_p + μ'·log τ + b0')
    """
    (b0, alpha, beta, gamma, delta, phi_c, mu,
     b0_t, alpha_t, beta_t, gamma_t, delta_t, mu_t) = params

    phi  = df['phi'].values
    tau  = df['tau'].values
    cn   = df['cn'].values
    cov  = df['cov_phys'].values
    f_p  = df['f_perc'].values
    is_thick = (tau < TAU_SPLIT).astype(float)
    excess = np.maximum(phi - phi_c, 1e-6)

    log_pred = (
        b0 + np.log(SIGMA_GRAIN)
        + alpha * np.log(excess) + beta * np.log(cn)
        + gamma * np.log(cov) + delta * np.log(f_p)
        + mu * np.log(tau)
        + is_thick * (b0_t
                      + alpha_t * np.log(excess) + beta_t * np.log(cn)
                      + gamma_t * np.log(cov) + delta_t * np.log(f_p)
                      + mu_t * np.log(tau))
    )
    return np.exp(log_pred)


def loss_regime(params, df):
    pred = predict_regime(df, params)
    a = np.log(df['sigma'].values + 1e-12); p = np.log(pred + 1e-12)
    return float(np.mean((a - p) ** 2))


def fit_regime(df, n_start=12):
    bounds = [
        (-5.0, 5.0),  # b0
        ( 0.3, 3.0),  # alpha
        ( 0.3, 3.0),  # beta
        ( 0.0, 1.5),  # gamma
        ( 0.5, 7.0),  # delta
        ( 0.05, 0.30),# phi_c
        (-2.0, 0.5),  # mu
        (-3.0, 3.0),  # b0_t
        (-2.0, 2.0),  # alpha_t
        (-2.0, 2.0),  # beta_t
        (-1.0, 1.0),  # gamma_t
        (-3.0, 3.0),  # delta_t
        (-2.0, 2.0),  # mu_t
    ]
    rng = np.random.default_rng(7)
    best = None
    for s in range(n_start):
        x0 = [rng.uniform(*b) for b in bounds]
        res = minimize(loss_regime, x0, args=(df,), method='Nelder-Mead',
                       options={'maxiter': 5000, 'xatol': 1e-7, 'fatol': 1e-9})
        if best is None or res.fun < best.fun:
            best = res
    return best.x


def loocv_regime(df):
    """Leave-one-out on the joint regime fit (refit per fold)."""
    n = len(df)
    pred_loo = np.empty(n)
    for i in range(n):
        sub = df.drop(df.index[i]).reset_index(drop=True)
        p = fit_regime(sub, n_start=4)
        # Predict on the held-out row
        held = df.iloc[[i]]
        pred_loo[i] = predict_regime(held, p)[0]
    a = np.log(df['sigma'].values + 1e-12); p = np.log(pred_loo + 1e-12)
    ss_res = np.sum((a - p) ** 2); ss_tot = np.sum((a - a.mean()) ** 2)
    return 1 - ss_res / ss_tot if ss_tot > 0 else 0.0, pred_loo


def strategy_B(df, do_loocv=True):
    print('\n' + '=' * 75)
    print('STRATEGY B — Joint fit with regime interactions')
    print('=' * 75)
    params = fit_regime(df, n_start=15)
    pred = predict_regime(df, params)
    r2, w20 = metrics(df['sigma'].values, pred)
    print(f'\n  R²={r2:.4f}  w20={w20}/{len(df)}')
    print('  base (¬thick):',
          '  '.join(f'{n}={v:+.3f}' for n, v in zip(
              ('b0','α','β','γ','δ','φc','μ'), params[:7])))
    print('  Δ(thick − ¬thick):',
          '  '.join(f'{n}={v:+.3f}' for n, v in zip(
              ('Δb0','Δα','Δβ','Δγ','Δδ','Δμ'), params[7:])))

    loocv = None
    if do_loocv:
        print('  computing LOOCV (this is the slow step) …')
        loocv, _ = loocv_regime(df)
        print(f'  LOOCV={loocv:.4f}')

    return {'r2': r2, 'loocv': loocv, 'w20': w20, 'n': len(df),
            'params': list(params)}


# ─────────────────────────────────────────────────────────────────────
# Strategy C — Strategy B + binding/r_ratio residual corrections
# ─────────────────────────────────────────────────────────────────────
def strategy_C(df, base_params):
    """Take the regime-aware base prediction and stack a residual
    correction with binding shares + r_SE/r_AM.
    """
    print('\n' + '=' * 75)
    print('STRATEGY C — regime fit + binding/r_ratio residual')
    print('=' * 75)

    base_pred = predict_regime(df, base_params)
    actual = df['sigma'].values

    # Restrict to rows with usable r_ratio for full feature set
    df_x = df.copy()
    def _ratio(r):
        rs = r['r_SE']
        ra = r['r_AM_S'] or r['r_AM_P']
        if rs and ra and ra > 0:
            return rs / ra
        return np.nan
    df_x['r_ratio'] = df_x.apply(_ratio, axis=1)

    feature_full = ['b_liggghts', 'b_tabor', 'b_geom', 'r_ratio']
    df_full = df_x[df_x['r_ratio'].notna()].reset_index(drop=True)
    base_pred_full = predict_regime(df_full, base_params)

    # OLS on the log residual
    X = np.column_stack([df_full[f].values for f in feature_full])
    resid = np.log(df_full['sigma'].values + 1e-12) - np.log(base_pred_full + 1e-12)
    coef, *_ = np.linalg.lstsq(X, resid, rcond=None)
    pred_full = base_pred_full * np.exp(X @ coef)
    r2_full, w20_full = metrics(df_full['sigma'].values, pred_full)

    print(f'\n  full feature set (r_ratio req.): n={len(df_full)}')
    print(f'    R²={r2_full:.4f}  w20={w20_full}/{len(df_full)}')
    print('    γ:')
    for f, g in zip(feature_full, coef):
        print(f'      {f:14s} = {g:+.4f}')

    # Subset with no r_ratio: use binding-only correction
    feature_bind = ['b_liggghts', 'b_tabor', 'b_geom']
    Xb = np.column_stack([df[f].values for f in feature_bind])
    resid_all = np.log(actual + 1e-12) - np.log(base_pred + 1e-12)
    coef_b, *_ = np.linalg.lstsq(Xb, resid_all, rcond=None)
    pred_b = base_pred * np.exp(Xb @ coef_b)
    r2_b, w20_b = metrics(actual, pred_b)
    print(f'\n  binding-only (no r_ratio req.): n={len(df)}')
    print(f'    R²={r2_b:.4f}  w20={w20_b}/{len(df)}')
    print('    γ:')
    for f, g in zip(feature_bind, coef_b):
        print(f'      {f:14s} = {g:+.4f}')

    return {
        'full':    {'r2': r2_full, 'w20': w20_full, 'n': len(df_full),
                    'features': feature_full, 'gamma': list(coef)},
        'binding': {'r2': r2_b, 'w20': w20_b, 'n': len(df),
                    'features': feature_bind, 'gamma': list(coef_b)},
    }


def main():
    cases = load_cases()
    rows = load_phys_rows(cases)
    df = pd.DataFrame(rows)
    print(f'Loaded {len(df)} physics-mode cases.')

    A = strategy_A(df)
    B = strategy_B(df, do_loocv=True)
    C = strategy_C(df, B['params']) if B else None

    print('\n' + '=' * 75)
    print('=== FINAL SUMMARY ===')
    print('=' * 75)
    print(f'{"strategy":40s}  {"R²":>8s}  {"LOOCV":>8s}  {"w20":>10s}')
    print(f'{"A.thick    (τ<1.5, indep.)":40s}  '
          f'{A["thick"]["r2"]:8.4f}  {A["thick"]["loocv"]:8.4f}  '
          f'{A["thick"]["w20"]:>3d}/{A["thick"]["n"]}')
    print(f'{"A.¬thick   (τ≥1.5, indep.)":40s}  '
          f'{A["thin"]["r2"]:8.4f}  {A["thin"]["loocv"]:8.4f}  '
          f'{A["thin"]["w20"]:>3d}/{A["thin"]["n"]}')
    print(f'{"A.combined (concat preds)":40s}  '
          f'{A["combined"]["r2"]:8.4f}  '
          f'{"  —   ":>8s}  '
          f'{A["combined"]["w20"]:>3d}/{A["combined"]["n"]}')
    loocv_b_str = f'{B["loocv"]:8.4f}' if B["loocv"] is not None else '   —    '
    print(f'{"B. joint regime-aware":40s}  '
          f'{B["r2"]:8.4f}  {loocv_b_str}  '
          f'{B["w20"]:>3d}/{B["n"]}')
    if C:
        print(f'{"C. regime + bind/r_ratio (full)":40s}  '
              f'{C["full"]["r2"]:8.4f}  {"  —   ":>8s}  '
              f'{C["full"]["w20"]:>3d}/{C["full"]["n"]}')
        print(f'{"C. regime + bind only":40s}  '
              f'{C["binding"]["r2"]:8.4f}  {"  —   ":>8s}  '
              f'{C["binding"]["w20"]:>3d}/{C["binding"]["n"]}')

    out = Path('docs/figures/physics_regime')
    out.mkdir(parents=True, exist_ok=True)
    with open(out / 'physics_fit_v34_regime.json', 'w') as f:
        json.dump({'A': A, 'B': B, 'C': C}, f, indent=2, default=str)
    print(f'\n→ {out}/physics_fit_v34_regime.json')


if __name__ == '__main__':
    main()
