#!/usr/bin/env python3
"""Physics-mode fit v39 — Tier-1 upgrade sweep on v34 regime base.

After v33–v38 confirmed the data noise floor at R²≈0.97–0.98 (ML
included), v34's regime-aware fit (R²=0.9798 combined) is the
working baseline. This script tries every Tier-1 upgrade in
parallel to see if any squeezes a few more points without overfitting:

  U1  Free-exponent regime fit
      Currently α=1/2, β=3/2, γ=2/5, δ=3 are 'fixed-by-physics' on
      the Hertzian baseline. In physics-mode the data may prefer
      slightly different exponents. Let all four become free
      parameters in each regime → 8 extra params (4 per regime).

  U2  Heteroscedastic weighted fit
      Weight each case by 1/(1 + |log_residual|²) iteratively (IRLS)
      so high-noise outliers stop dragging the fit. R² evaluated
      unweighted at the end so it's a fair comparison.

  U3  Polynomial cov term: cov^γ → cov^γ · (1 + θ·cov)
      Adds curvature in coverage dependence. 1 extra param per regime.

  U4  Per-AM-batch stratification (1mAh / 8mAh / 6mAh / particulate)
      Independent v34 fits per name-prefix. Reports each batch's R²
      and the concat'd combined R². Highlights any batch with
      higher inherent noise.

  U5  U1 + U2 + U3 stacked
      Free exponents + IRLS + polynomial cov. The 'kitchen sink' but
      restricted to physically interpretable upgrades.

Each upgrade evaluated for R², LOOCV, w20. Sorted at end.
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


# ─────────────────────────────────────────────────────────────────────
# U1 — Free-exponent regime fit (subsumes v34 with extra freedom)
# ─────────────────────────────────────────────────────────────────────
def predict_free_regime(df, params, tau_split=TAU_SPLIT):
    """Like v34 predict_regime but α/β/γ/δ/μ all interactable per regime,
    and crucially φ_c can also differ (so 14 free params total instead of 13).
    """
    (b0, alpha, beta, gamma, delta, phi_c, mu,
     b0_t, alpha_t, beta_t, gamma_t, delta_t, mu_t, phi_c_t) = params
    phi  = df['phi'].values
    tau  = df['tau'].values
    cn   = df['cn'].values
    cov  = df['cov_phys'].values
    f_p  = df['f_perc'].values
    is_thick = (tau < tau_split).astype(float)

    excess_a = np.maximum(phi - phi_c, 1e-6)        # ¬thick
    excess_b = np.maximum(phi - (phi_c + phi_c_t), 1e-6)  # thick

    log_pred = (
        b0 + np.log(SIGMA_GRAIN)
        + alpha * np.log(excess_a) + beta * np.log(cn)
        + gamma * np.log(cov) + delta * np.log(f_p)
        + mu * np.log(tau)
    )
    log_pred_thick = (
        (b0 + b0_t) + np.log(SIGMA_GRAIN)
        + (alpha + alpha_t) * np.log(excess_b)
        + (beta + beta_t) * np.log(cn)
        + (gamma + gamma_t) * np.log(cov)
        + (delta + delta_t) * np.log(f_p)
        + (mu + mu_t) * np.log(tau)
    )
    return np.exp(np.where(is_thick == 1, log_pred_thick, log_pred))


def fit_free_regime(df, n_start=18, weights=None):
    bounds = [
        (-5,5), (0.3,5), (0.3,5), (0.0,2.5), (0.5,8), (0.05,0.30), (-2,1),
        (-3,3), (-3,3), (-3,3), (-1.5,1.5), (-3,3), (-2,2), (-0.20,0.20),
    ]
    rng = np.random.default_rng(101)
    best = None
    for s in range(n_start):
        x0 = [rng.uniform(*b) for b in bounds]
        def loss(p):
            pred = predict_free_regime(df, p)
            log_err = np.log(df['sigma'].values + 1e-12) - np.log(pred + 1e-12)
            if weights is not None:
                return float(np.average(log_err ** 2, weights=weights))
            return float(np.mean(log_err ** 2))
        res = minimize(loss, x0, method='Nelder-Mead',
                       options={'maxiter': 5000, 'xatol': 1e-7, 'fatol': 1e-9})
        if best is None or res.fun < best.fun:
            best = res
    return best.x


def loocv_free_regime(df, weights=None):
    n = len(df)
    pred_loo = np.empty(n)
    for i in range(n):
        sub = df.drop(df.index[i]).reset_index(drop=True)
        w_sub = None if weights is None else np.delete(weights, i)
        params = fit_free_regime(sub, n_start=4, weights=w_sub)
        held = df.iloc[[i]]
        pred_loo[i] = predict_free_regime(held, params)[0]
    a = np.log(df['sigma'].values + 1e-12); p = np.log(pred_loo + 1e-12)
    ss_res = np.sum((a - p) ** 2); ss_tot = np.sum((a - a.mean()) ** 2)
    return 1 - ss_res / ss_tot if ss_tot > 0 else 0.0


# ─────────────────────────────────────────────────────────────────────
# U2 — Heteroscedastic IRLS weighted fit
# ─────────────────────────────────────────────────────────────────────
def fit_irls(df, n_iter=4):
    """Iteratively reweighted least squares — downweights large residuals."""
    weights = np.ones(len(df))
    for it in range(n_iter):
        params = fit_free_regime(df, n_start=10, weights=weights)
        pred = predict_free_regime(df, params)
        log_resid = np.log(df['sigma'].values + 1e-12) - np.log(pred + 1e-12)
        # Tukey-style biweight, scale-invariant
        s = max(np.std(log_resid), 1e-3)
        weights = 1.0 / (1.0 + (log_resid / (1.5 * s)) ** 2)
    return params, weights


# ─────────────────────────────────────────────────────────────────────
# U3 — Polynomial cov term (free_regime + cov² interaction)
# ─────────────────────────────────────────────────────────────────────
def predict_poly_cov(df, params, tau_split=TAU_SPLIT):
    """Free regime + θ_cov2 · cov² (per regime)."""
    base_p = params[:14]
    theta_cov2_a = params[14]   # ¬thick cov² coefficient
    theta_cov2_b = params[15]   # thick     cov² coefficient
    pred = predict_free_regime(df, base_p, tau_split)
    cov = df['cov_phys'].values
    is_thick = (df['tau'].values < tau_split).astype(float)
    cov2_term = (1 - is_thick) * theta_cov2_a + is_thick * theta_cov2_b
    return pred * np.exp(cov2_term * cov ** 2)


def fit_poly_cov(df, n_start=14, weights=None):
    bounds = [
        (-5,5), (0.3,5), (0.3,5), (0.0,2.5), (0.5,8), (0.05,0.30), (-2,1),
        (-3,3), (-3,3), (-3,3), (-1.5,1.5), (-3,3), (-2,2), (-0.20,0.20),
        (-2,2), (-2,2),  # θ_cov2_a, θ_cov2_b
    ]
    rng = np.random.default_rng(202)
    best = None
    for s in range(n_start):
        x0 = [rng.uniform(*b) for b in bounds]
        def loss(p):
            pred = predict_poly_cov(df, p)
            log_err = np.log(df['sigma'].values + 1e-12) - np.log(pred + 1e-12)
            if weights is not None:
                return float(np.average(log_err ** 2, weights=weights))
            return float(np.mean(log_err ** 2))
        res = minimize(loss, x0, method='Nelder-Mead',
                       options={'maxiter': 6000, 'xatol': 1e-7, 'fatol': 1e-9})
        if best is None or res.fun < best.fun:
            best = res
    return best.x


# ─────────────────────────────────────────────────────────────────────
# U4 — Per-AM-batch stratification
# ─────────────────────────────────────────────────────────────────────
def per_batch_fit(df):
    """Independent v29 base fit per batch tag (1mAh / 8mAh / 6mAh / particulate)."""
    name = df['name'].astype(str)
    tags = []
    for n in name:
        n_lo = n.lower()
        if '1mah' in n_lo:    tags.append('1mAh')
        elif '8mah' in n_lo:  tags.append('8mAh')
        elif '6mah' in n_lo:  tags.append('6mAh')
        elif 'particulate' in n_lo: tags.append('particulate')
        else:                  tags.append('other')
    df = df.copy(); df['batch'] = tags
    print(f'\nBatch distribution:')
    for t, c in df['batch'].value_counts().items():
        print(f'  {t}: {c}')

    preds, sigmas = [], []
    per_batch = {}
    for batch in df['batch'].unique():
        sub = df[df['batch'] == batch].reset_index(drop=True)
        if len(sub) < 5:
            print(f'  {batch}: too few cases — skipped')
            continue
        params = fit_base(sub, n_start=12)
        pred = predict_base(sub, params)
        r2, w20 = metrics(sub['sigma'].values, pred)
        loocv = loocv_r2(sub, pred)
        print(f'  {batch:14s}: n={len(sub):>3d}  R²={r2:.4f}  '
              f'LOOCV={loocv:.4f}  w20={w20}/{len(sub)}')
        preds.append(pred); sigmas.append(sub['sigma'].values)
        per_batch[batch] = {'n': len(sub), 'r2': r2, 'loocv': loocv,
                            'w20': w20, 'params': list(params)}
    pred_all = np.concatenate(preds); sig_all = np.concatenate(sigmas)
    a = np.log(sig_all + 1e-12); p = np.log(pred_all + 1e-12)
    r2_combo = 1 - np.sum((a-p)**2) / np.sum((a-a.mean())**2)
    err = np.abs(sig_all - pred_all) / np.maximum(sig_all, 1e-12)
    w20_combo = int(np.sum(err <= 0.20))
    return per_batch, r2_combo, w20_combo, len(sig_all)


def main():
    cases = load_cases()
    rows = load_phys_rows(cases)
    df = pd.DataFrame(rows)
    actual = df['sigma'].values
    print(f'Loaded {len(df)} physics-mode cases.')

    results = []

    # Reference: v34 baseline (free exponents disabled = same as v34)
    print('\n' + '=' * 80)
    print('U1 — Free-exponent regime fit (φ_c can also differ)')
    print('=' * 80)
    p1 = fit_free_regime(df, n_start=20)
    pred1 = predict_free_regime(df, p1)
    r2_1, w20_1 = metrics(actual, pred1)
    print(f'  R²={r2_1:.4f}  w20={w20_1}/{len(df)}')
    print('  ¬thick params:',
          '  '.join(f'{n}={v:+.3f}' for n, v in zip(
              ('b0','α','β','γ','δ','φc','μ'), p1[:7])))
    print('  thick deltas:',
          '  '.join(f'{n}={v:+.3f}' for n, v in zip(
              ('Δb0','Δα','Δβ','Δγ','Δδ','Δμ','Δφc'),
              [p1[7], p1[8], p1[9], p1[10], p1[11], p1[12], p1[13]])))
    print('  computing LOOCV (slow) ...')
    loocv1 = loocv_free_regime(df)
    print(f'  LOOCV={loocv1:.4f}')
    results.append({'label': 'U1 free-exponent regime', 'r2': r2_1,
                    'loocv': loocv1, 'w20': w20_1, 'params': list(p1)})

    print('\n' + '=' * 80)
    print('U2 — IRLS heteroscedastic-weighted free-exponent fit')
    print('=' * 80)
    p2, w2 = fit_irls(df, n_iter=4)
    pred2 = predict_free_regime(df, p2)
    r2_2, w20_2 = metrics(actual, pred2)
    print(f'  R² (unweighted)={r2_2:.4f}  w20={w20_2}/{len(df)}')
    n_down = int(np.sum(w2 < 0.5))
    print(f'  cases downweighted (w<0.5): {n_down}/{len(df)}')
    results.append({'label': 'U2 IRLS-weighted free-exp', 'r2': r2_2,
                    'loocv': None, 'w20': w20_2, 'params': list(p2)})

    print('\n' + '=' * 80)
    print('U3 — Free-exponent + polynomial cov² term')
    print('=' * 80)
    p3 = fit_poly_cov(df, n_start=14)
    pred3 = predict_poly_cov(df, p3)
    r2_3, w20_3 = metrics(actual, pred3)
    print(f'  R²={r2_3:.4f}  w20={w20_3}/{len(df)}')
    print(f'  cov² coefs: ¬thick={p3[14]:+.3f}  thick={p3[15]:+.3f}')
    results.append({'label': 'U3 free-exp + cov² term', 'r2': r2_3,
                    'loocv': None, 'w20': w20_3, 'params': list(p3)})

    print('\n' + '=' * 80)
    print('U4 — Per-AM-batch stratification (independent v29 per batch)')
    print('=' * 80)
    per_batch, r2_4, w20_4, n_4 = per_batch_fit(df)
    print(f'  COMBINED across batches: n={n_4}  R²={r2_4:.4f}  w20={w20_4}/{n_4}')
    results.append({'label': 'U4 per-batch stratified', 'r2': r2_4,
                    'loocv': None, 'w20': w20_4, 'per_batch': per_batch,
                    'n': n_4})

    print('\n' + '=' * 80)
    print('U5 — KITCHEN: free-exp + IRLS + cov² (everything Tier-1)')
    print('=' * 80)
    # Run IRLS first, then poly-cov fit on those weights
    p_irls, w_irls = fit_irls(df, n_iter=3)
    p5 = fit_poly_cov(df, n_start=14, weights=w_irls)
    pred5 = predict_poly_cov(df, p5)
    r2_5, w20_5 = metrics(actual, pred5)
    print(f'  R² (unweighted)={r2_5:.4f}  w20={w20_5}/{len(df)}')
    results.append({'label': 'U5 free-exp + IRLS + cov²', 'r2': r2_5,
                    'loocv': None, 'w20': w20_5, 'params': list(p5)})

    # Summary
    print('\n' + '=' * 80)
    print('=== UPGRADE COMPARISON (sorted by R²) ===')
    print('=' * 80)
    print(f'{"upgrade":36s}  {"R²":>8s}  {"LOOCV":>8s}  {"w20":>10s}')
    for r in sorted(results, key=lambda x: -x['r2']):
        loocv_s = f'{r["loocv"]:8.4f}' if r["loocv"] is not None else '   —    '
        n_show = r.get('n', len(df))
        print(f'{r["label"]:36s}  {r["r2"]:8.4f}  {loocv_s}  '
              f'{r["w20"]:>3d}/{n_show}')

    out = Path('docs/figures/physics_regime')
    out.mkdir(parents=True, exist_ok=True)
    with open(out / 'physics_fit_v39_tier1.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print(f'\n→ {out}/physics_fit_v39_tier1.json')

    best = max(results, key=lambda r: r['r2'])
    print(f'\nBest: {best["label"]} → R²={best["r2"]:.4f}')
    if best['r2'] >= 0.99:
        print('  🎯 0.99 REACHED.')
    elif best['r2'] >= 0.985:
        print(f'  Close (gap={0.99 - best["r2"]:+.4f}).')
    else:
        print(f'  Below 0.99 (gap={0.99 - best["r2"]:+.4f}). '
              'Confirms v38 ML diagnosis: 0.98 = noise floor.')


if __name__ == '__main__':
    main()
