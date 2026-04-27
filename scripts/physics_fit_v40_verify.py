#!/usr/bin/env python3
"""Physics-mode fit v40 — verify per-batch R²=0.998 + unified-form attempt.

v39 U4 (per-batch stratification) reported astonishing R²=0.9984 for
both 6mAh and 8mAh batches with the v29 base form alone. Two questions:

  1. Is 0.998 real or an overfit artefact? n=12-17 with 7 params is
     close to the parameter:data ratio that can fake high R². The
     loocv_r2() helper used in v39 doesn't refit the base per fold —
     it returns plain R² when no residual features are stacked.
     Need PROPER LOOCV that refits the base each fold.

  2. If 0.998 is real, can we build a UNIFIED form (one fit on all
     76 cases) that hits ≥0.99 by adding the right batch-distinguishing
     feature? Candidates: thickness, RVE box size, p_frac diversity.

This script does both:

  Stage A — Proper LOOCV per batch
      For each of 1mAh / 6mAh / 8mAh / particulate: refit fit_base
      on (n-1) cases, predict held-out, compute LOOCV R² across the
      whole batch. If LOOCV stays at 0.99+, the per-batch fit is
      genuinely tight; if it drops to 0.95, we were fooled.

  Stage B — Unified form with batch-distinguishing features
      Tries adding to a SINGLE v34-style fit:
        F1: + thickness (linear in log)
        F2: + thickness² and 1/thickness
        F3: + log(thickness) interaction with τ
        F4: + log(thickness) × cov interaction
        F5: + binary is_thick_electrode (thickness ≥ 50μm)
      Reports each variant's R²/LOOCV. If any reach ≥0.99 with
      proper LOOCV, that's the unified publication form.
"""
from __future__ import annotations
import sys, json
from pathlib import Path
import numpy as np
import pandas as pd

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
        m = _read_full_metrics(r['case_id'])
        r2 = dict(r)
        r2['thickness'] = float((m or {}).get('thickness_um', 0) or 0)
        out.append(r2)
    return out


def true_loocv_per_batch(df_sub, label):
    """Refit fit_base on (n-1) per fold — gold-standard LOOCV."""
    n = len(df_sub)
    pred_loo = np.empty(n)
    for i in range(n):
        sub = df_sub.drop(df_sub.index[i]).reset_index(drop=True)
        params = fit_base(sub, n_start=8)
        held = df_sub.iloc[[i]]
        pred_loo[i] = predict_base(held, params)[0]
    actual = df_sub['sigma'].values
    a = np.log(actual + 1e-12); p = np.log(pred_loo + 1e-12)
    ss_res = np.sum((a - p) ** 2); ss_tot = np.sum((a - a.mean()) ** 2)
    r2_loo = 1 - ss_res / ss_tot if ss_tot > 0 else 0.0
    err = np.abs(actual - pred_loo) / np.maximum(actual, 1e-12)
    w20 = int(np.sum(err <= 0.20))
    # In-sample for comparison
    p_full = fit_base(df_sub, n_start=15)
    pred_full = predict_base(df_sub, p_full)
    r2_in, w20_in = metrics(actual, pred_full)
    print(f'  {label:14s}: n={n:>3d}   in-samp R²={r2_in:.4f} '
          f' (w20={w20_in}/{n})   true LOOCV R²={r2_loo:.4f} (w20={w20}/{n})')
    return {'label': label, 'n': n, 'r2_in': r2_in, 'r2_loo': r2_loo,
            'w20_in': w20_in, 'w20_loo': w20}


def _predict_v34_regime(df, params, tau_split=1.5):
    """v34 regime base (replicated locally to avoid import chain)."""
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


def predict_with_thick(df, params, mode='linear'):
    """Unified form: v34 regime base + thickness feature variants."""
    base = params[:13]
    extra = params[13:]
    base_pred = _predict_v34_regime(df, base, tau_split=1.5)
    th = df['thickness'].values
    if mode == 'linear':
        return base_pred * (np.maximum(th, 1.0) ** extra[0])
    elif mode == 'quad':
        ln_th = np.log(np.maximum(th, 1.0))
        return base_pred * np.exp(extra[0] * ln_th + extra[1] * ln_th ** 2)
    elif mode == 'inverse':
        return base_pred * (np.maximum(th, 1.0) ** extra[0]) * \
               np.exp(extra[1] / np.maximum(th, 1.0))
    elif mode == 'th_x_tau':
        ln_th = np.log(np.maximum(th, 1.0))
        ln_t = np.log(df['tau'].values)
        return base_pred * np.exp(extra[0] * ln_th + extra[1] * ln_th * ln_t)
    elif mode == 'th_x_cov':
        ln_th = np.log(np.maximum(th, 1.0))
        ln_c = np.log(df['cov_phys'].values)
        return base_pred * np.exp(extra[0] * ln_th + extra[1] * ln_th * ln_c)
    elif mode == 'binary':
        I = (th >= 50).astype(float)
        return base_pred * np.exp(extra[0] * I)
    return base_pred


def fit_with_thick(df, mode, n_start=12):
    from scipy.optimize import minimize
    n_extra = {'linear':1, 'quad':2, 'inverse':2, 'th_x_tau':2,
               'th_x_cov':2, 'binary':1}[mode]
    base_bounds = [(-5,5),(0.3,3),(0.3,3),(0.0,1.5),(0.5,7),(0.05,0.30),(-2,0.5),
                    (-3,3),(-2,2),(-2,2),(-1,1),(-3,3),(-2,2)]
    extra_bounds = [(-1.5, 1.5)] * n_extra
    bounds = base_bounds + extra_bounds
    rng = np.random.default_rng(42)
    best = None
    for s in range(n_start):
        x0 = [rng.uniform(*b) for b in bounds]
        def loss(p):
            pred = predict_with_thick(df, p, mode)
            err = np.log(df['sigma'].values + 1e-12) - np.log(pred + 1e-12)
            return float(np.mean(err ** 2))
        res = minimize(loss, x0, method='Nelder-Mead',
                       options={'maxiter': 5000, 'xatol': 1e-7, 'fatol': 1e-9})
        if best is None or res.fun < best.fun:
            best = res
    return best.x


def loocv_with_thick(df, mode):
    """Proper LOOCV for unified-with-thickness fits."""
    n = len(df)
    pred_loo = np.empty(n)
    for i in range(n):
        sub = df.drop(df.index[i]).reset_index(drop=True)
        params = fit_with_thick(sub, mode, n_start=4)
        held = df.iloc[[i]]
        pred_loo[i] = predict_with_thick(held, params, mode)[0]
    actual = df['sigma'].values
    a = np.log(actual + 1e-12); p = np.log(pred_loo + 1e-12)
    ss_res = np.sum((a - p) ** 2); ss_tot = np.sum((a - a.mean()) ** 2)
    return 1 - ss_res / ss_tot if ss_tot > 0 else 0.0


def main():
    cases = load_cases()
    rows = enrich(load_phys_rows(cases))
    df = pd.DataFrame(rows)
    name = df['name'].astype(str)
    df['batch'] = ['1mAh' if '1mah' in n.lower()
                   else '8mAh' if '8mah' in n.lower()
                   else '6mAh' if '6mah' in n.lower()
                   else 'particulate' if 'particulate' in n.lower()
                   else 'other' for n in name]
    print(f'Loaded {len(df)} cases.')
    print('Batch distribution:')
    for t, c in df['batch'].value_counts().items():
        thick_med = df[df['batch'] == t]['thickness'].median()
        print(f'  {t:14s}: n={c:>3d}   median thickness={thick_med:.1f}μm')

    # ─────────────────────────────────────────────────────────
    # STAGE A — proper LOOCV per batch
    # ─────────────────────────────────────────────────────────
    print('\n' + '=' * 80)
    print('STAGE A — proper LOOCV per batch (refit base each fold)')
    print('=' * 80)
    print('  This is the gold-standard test for v39 U4\'s 0.998 numbers.')
    print('  in-sample vs LOOCV gap > 0.02 = overfit, < 0.01 = real fit.\n')
    stage_A = []
    for batch in ['1mAh', '6mAh', '8mAh', 'particulate']:
        sub = df[df['batch'] == batch].reset_index(drop=True)
        if len(sub) < 5:
            print(f'  {batch}: n={len(sub)} (too few)')
            continue
        stage_A.append(true_loocv_per_batch(sub, batch))

    # ─────────────────────────────────────────────────────────
    # STAGE B — unified form with thickness feature
    # ─────────────────────────────────────────────────────────
    print('\n' + '=' * 80)
    print('STAGE B — unified v34 + thickness feature (single fit on all 76)')
    print('=' * 80)
    stage_B = []
    for mode in ['linear','quad','inverse','th_x_tau','th_x_cov','binary']:
        params = fit_with_thick(df, mode, n_start=12)
        pred = predict_with_thick(df, params, mode)
        r2, w20 = metrics(df['sigma'].values, pred)
        print(f'  thickness: {mode:12s}  R²={r2:.4f}  w20={w20}/{len(df)}')
        stage_B.append({'mode': mode, 'r2': r2, 'w20': w20,
                        'params': list(params)})

    # LOOCV for the top-2 best by R²
    stage_B.sort(key=lambda x: -x['r2'])
    print('\n  Computing proper LOOCV for top-2 best (slow) ...')
    for r in stage_B[:2]:
        loocv = loocv_with_thick(df, r['mode'])
        r['loocv'] = loocv
        print(f'  thickness: {r["mode"]:12s}  R²={r["r2"]:.4f}  LOOCV={loocv:.4f}')

    # ─────────────────────────────────────────────────────────
    # SUMMARY
    # ─────────────────────────────────────────────────────────
    print('\n' + '=' * 80)
    print('=== STAGE A: per-batch true LOOCV ===')
    print('=' * 80)
    print(f'{"batch":14s}  {"in-samp R²":>11s}  {"true LOOCV R²":>14s}  {"gap":>6s}')
    for r in stage_A:
        gap = r['r2_in'] - r['r2_loo']
        print(f'{r["label"]:14s}  {r["r2_in"]:11.4f}  {r["r2_loo"]:14.4f}  '
              f'{gap:+6.4f}')

    print('\n' + '=' * 80)
    print('=== STAGE B: unified-with-thickness ===')
    print('=' * 80)
    print(f'{"mode":14s}  {"R²":>8s}  {"LOOCV":>8s}  {"w20":>10s}')
    for r in stage_B:
        loocv_s = f'{r["loocv"]:8.4f}' if 'loocv' in r else '   —    '
        print(f'{r["mode"]:14s}  {r["r2"]:8.4f}  {loocv_s}  '
              f'{r["w20"]:>3d}/{len(df)}')

    # Verdict
    best_B = stage_B[0]
    best_loocv_A = max(stage_A, key=lambda r: r['r2_loo'])
    print('\n' + '=' * 80)
    print('=== VERDICT ===')
    print('=' * 80)
    print(f'  Per-batch best (true LOOCV): {best_loocv_A["label"]} '
          f'R²_loo={best_loocv_A["r2_loo"]:.4f}  '
          f'(gap to in-samp: {best_loocv_A["r2_in"] - best_loocv_A["r2_loo"]:+.4f})')
    if best_loocv_A['r2_in'] - best_loocv_A['r2_loo'] > 0.02:
        print(f'   ⚠ Per-batch in-samp ≥0.998 was OVERFIT '
              f'(gap {best_loocv_A["r2_in"] - best_loocv_A["r2_loo"]:.3f}). '
              'Real fit ≈ 0.99 or lower.')
    elif best_loocv_A['r2_loo'] >= 0.99:
        print('   ✓ Per-batch fit IS genuinely tight at 0.99+ — publishable.')
    else:
        print(f'   Per-batch real fit at {best_loocv_A["r2_loo"]:.4f}.')

    loocv_str = f', LOOCV={best_B["loocv"]:.4f}' if 'loocv' in best_B else ''
    print(f'  Best unified+thickness: {best_B["mode"]} '
          f'R²={best_B["r2"]:.4f}{loocv_str}')
    if 'loocv' in best_B and best_B['loocv'] >= 0.99:
        print('   🎯 0.99 reached on UNIFIED form — publication-ready single law.')
    else:
        print('   Unified form below 0.99; per-batch publication likely cleaner.')

    out = Path('docs/figures/physics_regime')
    out.mkdir(parents=True, exist_ok=True)
    with open(out / 'physics_fit_v40_verify.json', 'w') as f:
        json.dump({'stage_A': stage_A, 'stage_B': stage_B},
                  f, indent=2, default=str)
    print(f'\n→ {out}/physics_fit_v40_verify.json')


if __name__ == '__main__':
    main()
