#!/usr/bin/env python3
"""Physics-mode fit v35 — open-minded multi-strategy comparison.

The R²=0.96 → 0.98 progress through v33 (binding) and v34 (regime
split) suggests we're near the form's ceiling but multiple unexplored
feature classes might still push us higher. Rather than commit to a
single direction, try **all reasonable strategies in parallel** and
report side-by-side so the best one wins on its merits.

Strategies tried:

  S0  v34 baseline (regime-aware, no extra features)         — control
  S1  + stress_cv  (DEM von-Mises stress dispersion)
  S2  + am_isolation_risk  (fraction of AM with no SE contact)
  S3  + path_bottleneck    (smallest hop area along percolation path)
  S4  + porosity            (post-compaction void fraction)
  S5  + thickness          (electrode thickness, μm)
  S6  + ALL of S1..S5
  S7  + Quadratic interactions: φ², τ², CN², φ·CN, τ·cov
  S8  + Different τ split:  τ_split = 2.0
  S9  + Different τ split:  τ_split = 2.5
  S10 + Drop top-5 outliers and refit (sanity-check ceiling)
  S11 + Drop top-9 outliers and refit
  S12 + Stress + binding + r_ratio + regime + quadratic (kitchen sink)

Each strategy reports R², LOOCV, w20. Results sorted at the end so the
winner is obvious. JSON dump with full param vectors.
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
    fit_residual_features,
)
from v32_exhaustive_refit import load_cases  # noqa: E402

WEBAPP = SCRIPTS.parent / 'webapp'
SIGMA_GRAIN = 3.0


def _read_full_metrics(cid: str) -> dict | None:
    for base in ('results', 'archive'):
        for p in (WEBAPP / base).rglob(f'{cid}/full_metrics.json'):
            try:
                return json.load(open(p))
            except Exception:
                pass
    return None


def enrich_with_extras(df_rows):
    """Read additional metrics that v33 didn't load."""
    out = []
    for r in df_rows:
        cid = r['case_id']
        m = _read_full_metrics(cid)
        if m is None:
            r2 = dict(r)
        else:
            r2 = dict(r)
            r2['stress_cv']  = float(m.get('stress_cv', 0) or 0)
            isol = m.get('am_isolation_risk') or {}
            if isinstance(isol, dict):
                # Use fraction of vulnerable AM (sum over AM types) as scalar
                vuln = (isol.get('AM_P_vulnerable_pct', 0) or 0) + \
                       (isol.get('AM_S_vulnerable_pct', 0) or 0)
                r2['am_vulnerable'] = float(vuln) / 100.0
            else:
                r2['am_vulnerable'] = 0.0
            r2['path_bottleneck'] = float(m.get('path_hop_area_min_mean', 0) or 0)
            r2['porosity'] = float(m.get('porosity', 0) or 0) / 100.0
            r2['thickness'] = float(m.get('thickness_um', 0) or 0)
        out.append(r2)
    return out


# ─────────────────────────────────────────────────────────────────────
# Regime-aware base prediction (from v34, copied to avoid circular import)
# ─────────────────────────────────────────────────────────────────────
def predict_regime(df, params, tau_split=1.5):
    (b0, alpha, beta, gamma, delta, phi_c, mu,
     b0_t, alpha_t, beta_t, gamma_t, delta_t, mu_t) = params
    phi  = df['phi'].values
    tau  = df['tau'].values
    cn   = df['cn'].values
    cov  = df['cov_phys'].values
    f_p  = df['f_perc'].values
    is_thick = (tau < tau_split).astype(float)
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


def fit_regime(df, tau_split=1.5, n_start=12):
    bounds = [(-5,5),(0.3,3),(0.3,3),(0.0,1.5),(0.5,7),(0.05,0.30),(-2,0.5),
              (-3,3),(-2,2),(-2,2),(-1,1),(-3,3),(-2,2)]
    rng = np.random.default_rng(7)
    best = None
    for s in range(n_start):
        x0 = [rng.uniform(*b) for b in bounds]
        def loss(p): return float(np.mean(
            (np.log(df['sigma'].values+1e-12) -
             np.log(predict_regime(df, p, tau_split)+1e-12))**2))
        res = minimize(loss, x0, method='Nelder-Mead',
                       options={'maxiter': 4000, 'xatol': 1e-7, 'fatol': 1e-9})
        if best is None or res.fun < best.fun:
            best = res
    return best.x


def stack_residual(df, base_pred, feature_names):
    """OLS γ on log residual for given features (drop NaN rows)."""
    sub = df[feature_names].notna().all(axis=1)
    if sub.sum() < len(df):
        # Use full set + impute (fill NaN with column mean)
        df = df.copy()
        for f in feature_names:
            df[f] = df[f].fillna(df[f].mean() if df[f].notna().any() else 0.0)
    valid = [f for f in feature_names if df[f].std() > 1e-9]
    if not valid:
        return [], base_pred, valid
    X = np.column_stack([df[f].values for f in valid])
    resid = np.log(df['sigma'].values+1e-12) - np.log(base_pred+1e-12)
    coef, *_ = np.linalg.lstsq(X, resid, rcond=None)
    pred = base_pred * np.exp(X @ coef)
    return coef, pred, valid


def evaluate(df, base_params, feature_names, label, tau_split=1.5):
    base_pred = predict_regime(df, base_params, tau_split)
    coef, pred, valid = stack_residual(df, base_pred, feature_names)
    r2, w20 = metrics(df['sigma'].values, pred)
    loocv = loocv_r2(df, base_pred, valid, coef)
    return {'label': label, 'r2': r2, 'loocv': loocv, 'w20': w20,
            'n': len(df), 'features': valid, 'gamma': list(coef)}


def add_quadratic(df):
    df = df.copy()
    df['phi_sq'] = df['phi'].values ** 2
    df['tau_sq'] = df['tau'].values ** 2
    df['cn_sq']  = df['cn'].values ** 2
    df['phi_cn'] = df['phi'].values * df['cn'].values
    df['tau_cov']= df['tau'].values * df['cov_phys'].values
    return df


def drop_outliers(df, base_params, k, tau_split=1.5):
    base_pred = predict_regime(df, base_params, tau_split)
    log_resid = np.log(df['sigma'].values+1e-12) - np.log(base_pred+1e-12)
    keep = np.argsort(np.abs(log_resid))[:len(df) - k]
    return df.iloc[keep].reset_index(drop=True)


def main():
    cases = load_cases()
    rows = load_phys_rows(cases)
    rows = enrich_with_extras(rows)
    df = pd.DataFrame(rows)
    print(f'Loaded {len(df)} physics-mode cases (regime-aware base + extras).')

    # Survey extra-feature availability
    print('\nExtra feature populations:')
    for f in ('stress_cv','am_vulnerable','path_bottleneck','porosity','thickness'):
        nz = (df[f] > 0).sum() if f in df.columns else 0
        print(f'  {f:20s} : {nz}/{len(df)} non-zero')

    # Fit regime base (τ_split=1.5)
    print('\nFitting regime-aware base (τ_split=1.5) ...')
    base_params = fit_regime(df, tau_split=1.5)
    base_pred = predict_regime(df, base_params, 1.5)
    r2_base, w20_base = metrics(df['sigma'].values, base_pred)
    print(f'  S0 baseline: R²={r2_base:.4f}  w20={w20_base}/{len(df)}')

    results = []
    results.append({'label': 'S0  v34 regime baseline', 'r2': r2_base,
                    'loocv': loocv_r2(df, base_pred), 'w20': w20_base,
                    'n': len(df), 'features': [], 'gamma': []})

    # Single-feature additions
    for f, lbl in [
        ('stress_cv',       'S1  + stress_cv'),
        ('am_vulnerable',   'S2  + am_vulnerable'),
        ('path_bottleneck', 'S3  + path_bottleneck'),
        ('porosity',        'S4  + porosity'),
        ('thickness',       'S5  + thickness'),
    ]:
        results.append(evaluate(df, base_params, [f], lbl))

    # All 5 stacked
    results.append(evaluate(df, base_params,
        ['stress_cv','am_vulnerable','path_bottleneck','porosity','thickness'],
        'S6  + ALL extras (S1-S5)'))

    # Quadratic interactions
    df_q = add_quadratic(df)
    base_pred_q = predict_regime(df_q, base_params, 1.5)
    coef_q, pred_q, val_q = stack_residual(df_q, base_pred_q,
        ['phi_sq','tau_sq','cn_sq','phi_cn','tau_cov'])
    r2_q, w20_q = metrics(df_q['sigma'].values, pred_q)
    results.append({'label': 'S7  + quadratic interactions',
                    'r2': r2_q, 'loocv': loocv_r2(df_q, base_pred_q, val_q, coef_q),
                    'w20': w20_q, 'n': len(df_q),
                    'features': val_q, 'gamma': list(coef_q)})

    # Different τ splits
    for ts, lbl in [(2.0, 'S8  τ_split=2.0'), (2.5, 'S9  τ_split=2.5')]:
        params_ts = fit_regime(df, tau_split=ts)
        pred_ts = predict_regime(df, params_ts, ts)
        r2_ts, w20_ts = metrics(df['sigma'].values, pred_ts)
        results.append({'label': lbl, 'r2': r2_ts,
                        'loocv': loocv_r2(df, pred_ts), 'w20': w20_ts,
                        'n': len(df), 'features': [], 'gamma': []})

    # Outlier drop sanity checks
    for k_drop, lbl in [(5, 'S10 drop top-5 outliers'),
                        (9, 'S11 drop top-9 outliers')]:
        df_d = drop_outliers(df, base_params, k_drop, 1.5)
        params_d = fit_regime(df_d, tau_split=1.5)
        pred_d = predict_regime(df_d, params_d, 1.5)
        r2_d, w20_d = metrics(df_d['sigma'].values, pred_d)
        results.append({'label': lbl, 'r2': r2_d,
                        'loocv': loocv_r2(df_d, pred_d), 'w20': w20_d,
                        'n': len(df_d), 'features': [], 'gamma': []})

    # Kitchen sink
    df_full = add_quadratic(df)
    feats_full = ['stress_cv','am_vulnerable','path_bottleneck','porosity',
                  'thickness','phi_sq','tau_sq','cn_sq','phi_cn','tau_cov',
                  'b_liggghts','b_tabor','b_geom']
    results.append(evaluate(df_full, base_params, feats_full,
                            'S12 KITCHEN SINK (everything)'))

    # Sort by R² and pretty-print
    print('\n' + '=' * 80)
    print('=== ALL STRATEGIES SORTED BY R² ===')
    print('=' * 80)
    print(f'{"strategy":42s}  {"R²":>8s}  {"LOOCV":>8s}  {"w20":>10s}  {"#γ":>3s}')
    for r in sorted(results, key=lambda x: -x['r2']):
        loocv_s = f'{r["loocv"]:8.4f}' if r["loocv"] is not None else '   —    '
        print(f'{r["label"]:42s}  {r["r2"]:8.4f}  {loocv_s}  '
              f'{r["w20"]:>3d}/{r["n"]}     '
              f'{len(r.get("features",[])):>3d}')

    # Save
    out = Path('docs/figures/physics_regime')
    out.mkdir(parents=True, exist_ok=True)
    with open(out / 'physics_fit_v35_multi.json', 'w') as f:
        json.dump({'all': results,
                   'best_by_r2': max(results, key=lambda x: x['r2']),
                   'best_by_loocv': max(results,
                       key=lambda x: x['loocv'] if x['loocv'] is not None else -1),
                   }, f, indent=2, default=str)
    print(f'\n→ {out}/physics_fit_v35_multi.json')

    # Print best honestly (loocv aware)
    best_r2 = max(results, key=lambda x: x['r2'])
    best_loocv = max(results,
                     key=lambda x: x['loocv'] if x['loocv'] is not None else -1)
    print(f'\nBest by R²:    {best_r2["label"]:35s} R²={best_r2["r2"]:.4f}  '
          f'LOOCV={(best_r2["loocv"] if best_r2["loocv"] is not None else 0):.4f}')
    print(f'Best by LOOCV: {best_loocv["label"]:35s} R²={best_loocv["r2"]:.4f}  '
          f'LOOCV={best_loocv["loocv"]:.4f}')


if __name__ == '__main__':
    main()
