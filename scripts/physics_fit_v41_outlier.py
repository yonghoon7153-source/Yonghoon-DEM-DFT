#!/usr/bin/env python3
"""Physics-mode fit v41 — all outlier-correction concepts in parallel.

After v40 confirmed the v29-form noise floor at R²≈0.98, this script
fans out across every outlier-handling concept proposed and reports
each one head-to-head:

  Physics-informed corrections (multiplicative on v34 base):
    E1  finite-size:    σ × (1 - C/L_electrode)
    E2  τ ratio:        σ × (τ_Lap / τ_Dij)^θ
    E3  plate boundary: σ × (n_bottom_SE / n_perc_SE)^θ
    E4  P:S 5:5 bump:   σ × exp(-θ · exp(-((p-0.5)/σ_p)²))
    E5  E1+E2 combined  (top recommendation)
    E6  E1+E2+E3+E4 all physics

  Robust statistics (no form change, weighting only):
    A1  Tukey biweight IRLS  (already partially done in v39)
    A2  Mixture-model soft-outlier (EM-style two-Gaussian noise)

  Diagnostic:
    D2  Print raw values of top-9 residual cases to inspect

Each fit starts from the v34 regime base. Reports R², LOOCV (where
practical), and the 'gap to 0.99' so we can pick the winner.
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


def enrich(rows):
    out = []
    for r in rows:
        m = _read_full_metrics(r['case_id']) or {}
        r2 = dict(r)
        r2['thickness']    = float(m.get('thickness_um', 0) or 0)
        r2['tau_lap_eff']  = float(m.get('tortuosity_lap_eff') or
                                    m.get('tau_lap_eff', 0) or 0)
        r2['tau_dij']      = float(m.get('tau_dij') or
                                    m.get('tortuosity_mean', 0) or 0)
        r2['n_perc_se']    = float(m.get('percolation_pct', 0) or 0) / 100.0
        r2['top_reach']    = float(m.get('top_reachable_pct', 0) or 0) / 100.0
        r2['gb_density']   = float(m.get('gb_density_mean', 0) or 0)
        r2['constr_pct']   = float(m.get('constriction_fraction_pct') or
                                    m.get('constriction_pct', 0) or 0)
        out.append(r2)
    return out


# ─────────────────────────────────────────────────────────────────────
# v34 regime base (replicated)
# ─────────────────────────────────────────────────────────────────────
def predict_v34(df, params, tau_split=TAU_SPLIT):
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
        + is_thick * (b0_t + alpha_t * np.log(excess) + beta_t * np.log(cn)
                      + gamma_t * np.log(cov) + delta_t * np.log(f_p)
                      + mu_t * np.log(tau))
    )
    return np.exp(log_pred)


def fit_v34(df, n_start=12, weights=None):
    bounds = [(-5,5),(0.3,3),(0.3,3),(0.0,1.5),(0.5,7),(0.05,0.30),(-2,0.5),
              (-3,3),(-2,2),(-2,2),(-1,1),(-3,3),(-2,2)]
    rng = np.random.default_rng(7)
    best = None
    for s in range(n_start):
        x0 = [rng.uniform(*b) for b in bounds]
        def loss(p):
            pred = predict_v34(df, p)
            err = np.log(df['sigma'].values + 1e-12) - np.log(pred + 1e-12)
            if weights is not None:
                return float(np.average(err**2, weights=weights))
            return float(np.mean(err**2))
        res = minimize(loss, x0, method='Nelder-Mead',
                       options={'maxiter': 4000, 'xatol': 1e-7, 'fatol': 1e-9})
        if best is None or res.fun < best.fun:
            best = res
    return best.x


# ─────────────────────────────────────────────────────────────────────
# Generic feature stacker — log σ = log v34 + Σ θ_i · feature_i
# ─────────────────────────────────────────────────────────────────────
def fit_with_features(df, base_params, feature_cols):
    base_pred = predict_v34(df, base_params)
    if not feature_cols:
        return [], base_pred
    X = np.column_stack([df[f].values for f in feature_cols])
    resid = np.log(df['sigma'].values + 1e-12) - np.log(base_pred + 1e-12)
    coef, *_ = np.linalg.lstsq(X, resid, rcond=None)
    return coef, base_pred * np.exp(X @ coef)


def loocv_features(df, feature_cols):
    """Proper LOOCV — refit base each fold + residual γ."""
    n = len(df)
    pred_loo = np.empty(n)
    for i in range(n):
        sub = df.drop(df.index[i]).reset_index(drop=True)
        bp = fit_v34(sub, n_start=4)
        bp_pred = predict_v34(sub, bp)
        if feature_cols:
            X = np.column_stack([sub[f].values for f in feature_cols])
            resid = np.log(sub['sigma'].values + 1e-12) - np.log(bp_pred + 1e-12)
            coef, *_ = np.linalg.lstsq(X, resid, rcond=None)
            held = df.iloc[[i]]
            xh = np.array([held[f].values[0] for f in feature_cols])
            pred_loo[i] = predict_v34(held, bp)[0] * np.exp(xh @ coef)
        else:
            held = df.iloc[[i]]
            pred_loo[i] = predict_v34(held, bp)[0]
    actual = df['sigma'].values
    a = np.log(actual + 1e-12); p = np.log(pred_loo + 1e-12)
    ss_res = np.sum((a - p) ** 2); ss_tot = np.sum((a - a.mean()) ** 2)
    return 1 - ss_res / ss_tot if ss_tot > 0 else 0.0


def compute_features(df):
    """Compute all the physics-informed features."""
    df = df.copy()
    th = df['thickness'].values
    # B1: finite-size — log term encourages 1/L decay at small thickness
    df['log_thickness'] = np.log(np.maximum(th, 1.0))
    df['inv_thickness'] = 1.0 / np.maximum(th, 1.0)
    # B2: tau ratio (only when tau_lap_eff exists)
    tau_lap = df['tau_lap_eff'].values
    tau_d = df['tau_dij'].values
    valid = (tau_lap > 0) & (tau_d > 0)
    df['log_tau_ratio'] = np.where(valid, np.log(tau_lap / tau_d), 0.0)
    # B3: plate boundary — top_reach / percolation_pct
    n_perc = df['n_perc_se'].values
    top_r  = df['top_reach'].values
    df['plate_boundary'] = np.where(n_perc > 0, top_r / n_perc, 1.0)
    df['log_plate_boundary'] = np.log(np.maximum(df['plate_boundary'].values, 1e-3))
    # B4: P:S 5:5 Gaussian bump
    p = df['p_frac'].values
    df['p5050_bump'] = np.exp(-((p - 0.5) ** 2) / (2 * 0.05 ** 2))
    return df


# ─────────────────────────────────────────────────────────────────────
# A1 — Tukey biweight IRLS (more aggressive than v39)
# ─────────────────────────────────────────────────────────────────────
def fit_irls_tukey(df, n_iter=6, c_tukey=4.685):
    weights = np.ones(len(df))
    for _ in range(n_iter):
        params = fit_v34(df, n_start=8, weights=weights)
        pred = predict_v34(df, params)
        log_resid = np.log(df['sigma'].values + 1e-12) - np.log(pred + 1e-12)
        s = max(np.median(np.abs(log_resid)) / 0.6745, 1e-3)  # MAD scale
        u = log_resid / (c_tukey * s)
        weights = np.where(np.abs(u) < 1, (1 - u**2) ** 2, 0.0)
        weights = np.clip(weights, 1e-3, 1.0)
    return params, weights


# ─────────────────────────────────────────────────────────────────────
# A2 — Two-Gaussian mixture model on log residuals (EM)
# ─────────────────────────────────────────────────────────────────────
def fit_mixture(df, n_em=20):
    """Fit v34 + EM to identify outliers as wider Gaussian.

    Likelihood: log_resid_i ~ p · N(0, σ_tight²) + (1-p) · N(0, σ_wide²)
    Outliers get assigned to the wide Gaussian; in-distribution to tight.
    R² is computed using only tight-component residuals (the outliers are
    explained by the noise model itself, not the form).
    """
    p_in = 0.85
    s_tight = 0.05
    s_wide = 0.5
    weights = np.ones(len(df))
    params = fit_v34(df, n_start=8, weights=weights)
    for _ in range(n_em):
        params = fit_v34(df, n_start=4, weights=weights)
        pred = predict_v34(df, params)
        log_resid = np.log(df['sigma'].values + 1e-12) - np.log(pred + 1e-12)
        # E-step: posterior P(in | data)
        px = (p_in * np.exp(-log_resid**2 / (2 * s_tight**2)) /
              (np.sqrt(2*np.pi) * s_tight))
        qx = ((1-p_in) * np.exp(-log_resid**2 / (2 * s_wide**2)) /
              (np.sqrt(2*np.pi) * s_wide))
        gamma = px / (px + qx + 1e-30)
        # M-step
        p_in = float(np.mean(gamma))
        s_tight = float(np.sqrt(np.sum(gamma * log_resid**2) / max(np.sum(gamma), 1e-9)))
        s_wide  = float(np.sqrt(np.sum((1-gamma) * log_resid**2) / max(np.sum(1-gamma), 1e-9)))
        weights = gamma  # next round: use posterior as weight
    return params, gamma, p_in, s_tight, s_wide


def main():
    cases = load_cases()
    rows = enrich(load_phys_rows(cases))
    df = pd.DataFrame(rows)
    df = compute_features(df)
    print(f'Loaded {len(df)} cases.')
    print(f'Feature population:')
    for c in ('thickness','tau_lap_eff','tau_dij','top_reach','n_perc_se',
              'gb_density','constr_pct'):
        nz = (df[c] > 0).sum()
        print(f'  {c:18s}: {nz}/{len(df)} non-zero')

    # Baseline v34
    print('\nFitting v34 base ...')
    base_params = fit_v34(df, n_start=15)
    base_pred = predict_v34(df, base_params)
    r2_base, w20_base = metrics(df['sigma'].values, base_pred)
    print(f'  v34 base: R²={r2_base:.4f}  w20={w20_base}/{len(df)}')

    results = []
    results.append({'concept': 'v34 baseline', 'r2': r2_base, 'loocv': None,
                    'w20': w20_base})

    # ─────────────────────────────────────────────────────────
    # B1, B2, B3, B4 individually
    # ─────────────────────────────────────────────────────────
    feature_blocks = {
        'E1 finite-size':       ['log_thickness', 'inv_thickness'],
        'E2 τ ratio':            ['log_tau_ratio'],
        'E3 plate boundary':    ['log_plate_boundary'],
        'E4 P:S 5:5 bump':       ['p5050_bump'],
        'E5 E1+E2':              ['log_thickness','inv_thickness','log_tau_ratio'],
        'E6 ALL physics (E1-4)': ['log_thickness','inv_thickness','log_tau_ratio',
                                  'log_plate_boundary','p5050_bump'],
    }
    print('\n' + '=' * 80)
    print('=== Physics-informed corrections (v34 + features) ===')
    print('=' * 80)
    for label, feats in feature_blocks.items():
        coef, pred = fit_with_features(df, base_params, feats)
        r2, w20 = metrics(df['sigma'].values, pred)
        # LOOCV only for top 3 fastest configs
        do_loocv = label in ('E1 finite-size','E2 τ ratio','E5 E1+E2','E6 ALL physics (E1-4)')
        loocv = loocv_features(df, feats) if do_loocv else None
        loocv_s = f'{loocv:.4f}' if loocv is not None else '   —    '
        gamma_str = ', '.join(f'{f}={c:+.3f}' for f, c in zip(feats, coef))
        print(f'  {label:24s}  R²={r2:.4f}  LOOCV={loocv_s}  w20={w20:>3d}/{len(df)}')
        if coef.size:
            print(f'    γ: {gamma_str}')
        results.append({'concept': label, 'r2': r2, 'loocv': loocv,
                        'w20': w20, 'features': feats, 'gamma': list(coef)})

    # ─────────────────────────────────────────────────────────
    # A1 — Tukey IRLS
    # ─────────────────────────────────────────────────────────
    print('\n' + '=' * 80)
    print('=== A1 — Tukey biweight IRLS ===')
    print('=' * 80)
    p_irls, w_irls = fit_irls_tukey(df, n_iter=6)
    pred_irls = predict_v34(df, p_irls)
    r2_irls, w20_irls = metrics(df['sigma'].values, pred_irls)
    n_down = int(np.sum(w_irls < 0.5))
    print(f'  R²={r2_irls:.4f}  w20={w20_irls}/{len(df)}  '
          f'(downweighted: {n_down}/{len(df)})')
    results.append({'concept': 'A1 Tukey IRLS', 'r2': r2_irls, 'loocv': None,
                    'w20': w20_irls})

    # ─────────────────────────────────────────────────────────
    # A2 — Mixture model EM
    # ─────────────────────────────────────────────────────────
    print('\n' + '=' * 80)
    print('=== A2 — Two-Gaussian mixture (EM, soft-outlier) ===')
    print('=' * 80)
    p_mix, gamma_mix, p_in, s_tight, s_wide = fit_mixture(df, n_em=20)
    pred_mix = predict_v34(df, p_mix)
    r2_mix, w20_mix = metrics(df['sigma'].values, pred_mix)
    # Tight-only R²: re-evaluate using only cases assigned to tight component
    tight_mask = gamma_mix > 0.5
    if tight_mask.sum() > 5:
        a = np.log(df['sigma'].values[tight_mask] + 1e-12)
        p = np.log(pred_mix[tight_mask] + 1e-12)
        ss_res = np.sum((a - p) ** 2); ss_tot = np.sum((a - a.mean()) ** 2)
        r2_tight = 1 - ss_res / ss_tot
    else:
        r2_tight = float('nan')
    n_outlier = int((gamma_mix < 0.5).sum())
    print(f'  Full R²={r2_mix:.4f}  Tight-only R²={r2_tight:.4f}')
    print(f'  Posterior outliers (γ<0.5): {n_outlier}/{len(df)}')
    print(f'  σ_tight={s_tight:.3f}  σ_wide={s_wide:.3f}  p_in={p_in:.3f}')
    results.append({'concept': 'A2 Mixture model (full)', 'r2': r2_mix,
                    'loocv': None, 'w20': w20_mix,
                    'tight_r2': r2_tight, 'n_outlier': n_outlier})

    # ─────────────────────────────────────────────────────────
    # D2 — print top-9 residual cases for diagnostic
    # ─────────────────────────────────────────────────────────
    print('\n' + '=' * 80)
    print('=== D2 — Top-9 residual cases (diagnostic) ===')
    print('=' * 80)
    log_resid = np.log(df['sigma'].values + 1e-12) - np.log(base_pred + 1e-12)
    top_idx = np.argsort(-np.abs(log_resid))[:9]
    print(f'{"name":34s}  {"σ_act":>8s}  {"σ_pred":>8s}  {"resid":>7s}  '
          f'{"L_um":>6s}  {"τ_d":>5s}  {"τ_eff":>5s}  {"top%":>5s}  {"p":>4s}')
    for i in top_idx:
        row = df.iloc[i]
        tau_lap_str = f'{row["tau_lap_eff"]:5.2f}' if row['tau_lap_eff'] > 0 else '  —  '
        print(f'{str(row["name"])[:34]:34s}  '
              f'{row["sigma"]:8.4f}  {base_pred[i]:8.4f}  '
              f'{log_resid[i]:+7.3f}  '
              f'{row["thickness"]:6.1f}  {row["tau_dij"]:5.2f}  '
              f'{tau_lap_str}  '
              f'{row["top_reach"]*100:5.1f}  {row["p_frac"]:4.2f}')

    # ─────────────────────────────────────────────────────────
    # SUMMARY
    # ─────────────────────────────────────────────────────────
    print('\n' + '=' * 80)
    print('=== ALL OUTLIER-CORRECTION CONCEPTS — sorted by R² ===')
    print('=' * 80)
    print(f'{"concept":32s}  {"R²":>8s}  {"LOOCV":>8s}  {"w20":>10s}  {"#γ":>3s}')
    for r in sorted(results, key=lambda x: -x['r2']):
        loocv_s = f'{r["loocv"]:8.4f}' if r["loocv"] is not None else '   —    '
        n_g = len(r.get('features', []))
        print(f'{r["concept"]:32s}  {r["r2"]:8.4f}  {loocv_s}  '
              f'{r["w20"]:>3d}/{len(df)}     {n_g:>3d}')

    out = Path('docs/figures/physics_regime')
    out.mkdir(parents=True, exist_ok=True)
    with open(out / 'physics_fit_v41_outlier.json', 'w') as f:
        json.dump({'results': results,
                   'base_R2': r2_base, 'base_LOOCV': None}, f, indent=2, default=str)
    print(f'\n→ {out}/physics_fit_v41_outlier.json')

    best_r2 = max(results, key=lambda x: x['r2'])
    best_loocv = max(results,
                     key=lambda x: x['loocv'] if x['loocv'] is not None else -1)
    print(f'\nBest by R²:    {best_r2["concept"]:30s} R²={best_r2["r2"]:.4f}')
    if best_loocv["loocv"] is not None:
        print(f'Best by LOOCV: {best_loocv["concept"]:30s} '
              f'LOOCV={best_loocv["loocv"]:.4f}')


if __name__ == '__main__':
    main()
