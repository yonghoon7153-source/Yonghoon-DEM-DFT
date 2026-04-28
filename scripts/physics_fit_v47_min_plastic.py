#!/usr/bin/env python3
"""Physics-mode fit v47 — minimum-parameter plastic extension.

v46 (22 params) overfit catastrophically (LOOCV=−2.67) but revealed
a real signal: β_T = −0.77, β_G = +0.61 — opposite signs on
Tabor-binding vs geom-binding shares. This suggests a single contrast
feature can capture the new physics with minimal parameter cost:

    Δ_GT ≡ (b_G - b_T) / 100         (geom-share minus Tabor-share)

Physical reading:
    Δ_GT > 0  →  geom-cap dominant binding (large contact area, σ↑)
    Δ_GT < 0  →  Tabor-cap dominant binding (constriction-limited, σ↓)
    Δ_GT = 0  →  balanced

Variants tested (all have v29 base preserved exactly — 15 params):

  V0  v29 ORIGINAL (control, 15 params)            — already R²=0.95, LOOCV=0.94

  V1  v29 + (1 param) Δ_GT contrast term           — 16 params total
        σ = σ_v29 · exp(β_GT · Δ_GT)

  V2  v29 + (2 params) Δ_GT + thin indicator       — 17 params total
        σ = σ_v29 · exp(β_GT · Δ_GT + β_thin · I[L<100])
        with L_thresh = 100 μm (from v46's L_* ≈ 98.7)

  V3  v29 + (1 param) absolute Tabor share         — 16 params
        σ = σ_v29 · exp(β_T · b_T)
        sanity check: does Tabor share alone (no geom contrast) help?

  V4  v29 + (1 param) absolute geom share          — 16 params
        σ = σ_v29 · exp(β_G · b_G)

If V1 LOOCV > V0 (0.94) the contrast is genuine signal worth adding.
If V1/V2 LOOCV ≈ V0, v29 is the publication final and these signals
are real but redundant with v29's existing structure.
If V1/V2 LOOCV < V0, even +1 param overfits (76 cases too few).

Sample-to-param ratios:
  v29 (V0):   76/15 = 5.1   ← safe
  V1, V3, V4: 76/16 = 4.8   ← still in safe range
  V2:         76/17 = 4.5   ← borderline
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

WEBAPP = SCRIPTS.parent / 'webapp'
SIGMA_GRAIN = 3.0

# Canonical exponents (FIXED — Stauffer/Kirkpatrick/Bruggeman)
ALPHA_FIX = 0.5
BETA_FIX  = 1.5
GAMMA_FIX = 0.4
DELTA_FIX = 3.0
PHI_C_FIX = 0.20  # data-native percolation threshold


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
    x = np.clip(x, -50, 50)
    return 1.0 / (1.0 + np.exp(-x))


def predict_v29_phys(df, params):
    """v29 physics-mode form. 15 free params (all in C_blend + C_corr).
    Canonical exponents fixed. Same structure as v29 FINAL Hertzian.

    Layout:
       0-1   C_thick, C_thin
       2-3   tau_0, k_tau                (v5 sigmoid centre, sharpness)
       4-5   K_BL, tau_c_BL              (blend weight sigmoid)
       6-9   a0, a1, a2, a3              (poly3 in log τ)
      10-12  beta_pf, k_pf, p_c          (P:S sigmoid)
      13-14  beta_lin, sigma_tau_win     (τ-bump Gaussian, fix tau_c=2.0)
    NOTE: tau_c_win, beta_gb, k_gb consolidated to keep parameter count at 15.
    """
    (C_thick, C_thin, tau_0, k_tau, K_BL, tau_c_BL,
     a0, a1, a2, a3,
     beta_pf, k_pf, p_c,
     beta_lin, s_win) = params

    phi = df['phi'].values
    tau = df['tau'].values
    cn  = df['cn'].values
    cov = df['cov_phys'].values
    f_p = df['f_perc'].values
    p   = df['p_frac'].values

    excess = np.maximum(phi - PHI_C_FIX, 1e-6)
    log_base = (np.log(SIGMA_GRAIN)
                + ALPHA_FIX * np.log(excess)
                + BETA_FIX  * np.log(cn)
                + GAMMA_FIX * np.log(cov)
                + DELTA_FIX * np.log(f_p))

    # C_blend(τ) — v5 sigmoid + poly3 blend
    s_v5 = _sigmoid(k_tau * (tau - tau_0))
    log_Cv5 = (np.log(max(C_thick, 1e-6))
               + (np.log(max(C_thin, 1e-6)) - np.log(max(C_thick, 1e-6))) * s_v5)
    ln_t = np.log(np.maximum(tau, 0.01))
    log_Cp3 = a0 + a1 * ln_t + a2 * ln_t ** 2 + a3 * ln_t ** 3
    w_BL = _sigmoid(K_BL * (tau - tau_c_BL))
    log_Cblend = (1 - w_BL) * log_Cv5 + w_BL * log_Cp3

    # C_corr — P:S sigmoid + τ-bump (centered)
    w_pf = _sigmoid(k_pf * (p - p_c))
    w_pf_c = w_pf - float(np.mean(w_pf))
    w_win = np.exp(-((tau - 2.0) / max(s_win, 0.05)) ** 2 / 2.0)
    pwwin = p * w_win
    pwwin_c = pwwin - float(np.mean(pwwin))
    C_corr = beta_pf * w_pf_c + beta_lin * pwwin_c

    return np.exp(log_base + log_Cblend + C_corr)


def predict_v47(df, params, variant):
    """v29 + small plastic addition. params = v29 base (15) + extras.

    Variant extras:
      V1: [beta_GT]                    σ *= exp(beta_GT · Δ_GT)
      V2: [beta_GT, beta_thin]         σ *= exp(beta_GT · Δ_GT + beta_thin · I[L<100])
      V3: [beta_T_only]                σ *= exp(beta_T · b_T)
      V4: [beta_G_only]                σ *= exp(beta_G · b_G)
    """
    base_params = params[:15]
    extras = params[15:]
    base_pred = predict_v29_phys(df, base_params)

    b_T = df['b_tabor'].values / 100.0
    b_G = df['b_geom'].values  / 100.0
    delta_GT = b_G - b_T

    if variant == 'V1':
        beta_GT = extras[0]
        return base_pred * np.exp(beta_GT * delta_GT)
    elif variant == 'V2':
        beta_GT, beta_thin = extras
        L = df['thickness'].values
        I_thin = (L < 100).astype(float)
        I_thin_c = I_thin - float(np.mean(I_thin))
        return base_pred * np.exp(beta_GT * delta_GT + beta_thin * I_thin_c)
    elif variant == 'V3':
        beta_T_only = extras[0]
        return base_pred * np.exp(beta_T_only * b_T)
    elif variant == 'V4':
        beta_G_only = extras[0]
        return base_pred * np.exp(beta_G_only * b_G)
    else:  # V0
        return base_pred


def _bounds_v29():
    return [
        (0.001, 0.5), (0.001, 0.5),     # C_thick, C_thin
        (1.5, 3.0), (1.0, 12.0),         # tau_0, k_tau
        (0.5, 12.0), (1.5, 3.5),         # K_BL, tau_c_BL
        (-6.0, 4.0), (-6.0, 6.0), (-8.0, 8.0), (-5.0, 5.0),  # poly3
        (-1.0, 1.0), (1.0, 80.0), (0.05, 0.95),  # P:S sigm
        (-3.0, 3.0), (0.05, 1.0),         # τ-bump
    ]


def fit_variant(df, variant, n_start=25):
    bounds = _bounds_v29()
    if variant == 'V1' or variant == 'V3' or variant == 'V4':
        bounds = bounds + [(-3.0, 3.0)]
    elif variant == 'V2':
        bounds = bounds + [(-3.0, 3.0), (-2.0, 2.0)]

    rng = np.random.default_rng(123)
    best = None
    for s in range(n_start):
        x0 = [rng.uniform(*b) for b in bounds]
        def loss(p):
            try:
                pred = predict_v47(df, p, variant)
                err = np.log(df['sigma'].values + 1e-12) - np.log(pred + 1e-12)
                if not np.all(np.isfinite(err)):
                    return 1e9
                base_loss = float(np.mean(err ** 2))
                # Soft-penalty for OOB
                penalty = 0.0
                for v, (lo, hi) in zip(p, bounds):
                    if v < lo:
                        penalty += (lo - v) ** 2
                    elif v > hi:
                        penalty += (v - hi) ** 2
                return base_loss + 100.0 * penalty
            except Exception:
                return 1e9
        res = minimize(loss, x0, method='Nelder-Mead',
                       bounds=bounds,
                       options={'maxiter': 8000, 'xatol': 1e-7, 'fatol': 1e-9})
        if best is None or res.fun < best.fun:
            best = res
    return best.x


def metrics_simple(actual, pred):
    a = np.log(actual + 1e-12); p = np.log(pred + 1e-12)
    ss_res = np.sum((a - p) ** 2); ss_tot = np.sum((a - a.mean()) ** 2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0.0
    err = np.abs(actual - pred) / np.maximum(actual, 1e-12)
    w20 = int(np.sum(err <= 0.20))
    return r2, w20


def loocv_variant(df, variant, n_start_inner=3):
    n = len(df); pred_loo = np.empty(n)
    for i in range(n):
        sub = df.drop(df.index[i]).reset_index(drop=True)
        params = fit_variant(sub, variant, n_start=n_start_inner)
        held = df.iloc[[i]]
        pred_loo[i] = predict_v47(held, params, variant)[0]
        if (i + 1) % 10 == 0:
            print(f'    progress: {i+1}/{n}')
    a = np.log(df['sigma'].values + 1e-12); p = np.log(pred_loo + 1e-12)
    ss_res = np.sum((a-p)**2); ss_tot = np.sum((a - a.mean())**2)
    return 1 - ss_res / ss_tot if ss_tot > 0 else 0.0


def main():
    cases = load_cases()
    rows = enrich(load_phys_rows(cases))
    df = pd.DataFrame(rows)
    print(f'Loaded {len(df)} cases.')

    variants = [
        ('V0', 'v29 ORIGINAL (15p)',                15),
        ('V1', 'v29 + Δ_GT contrast (16p)',          16),
        ('V2', 'v29 + Δ_GT + thin indicator (17p)',   17),
        ('V3', 'v29 + b_T only (16p)',                16),
        ('V4', 'v29 + b_G only (16p)',                16),
    ]
    results = []
    for var, label, k in variants:
        print('\n' + '=' * 80)
        print(f'{var} — {label}')
        print('=' * 80)
        params = fit_variant(df, var, n_start=25)
        pred = predict_v47(df, params, var)
        r2, w20 = metrics_simple(df['sigma'].values, pred)
        print(f'  Joint-fit R²={r2:.4f}  w20={w20}/{len(df)}')
        if var != 'V0':
            extras = params[15:]
            print(f'  Extra params: {", ".join(f"{e:+.4f}" for e in extras)}')
        # LOOCV
        print(f'  LOOCV ({var}) ...')
        loocv = loocv_variant(df, var, n_start_inner=3)
        print(f'  LOOCV R²={loocv:.4f}')
        results.append({'variant': var, 'label': label, 'k': k,
                        'r2': r2, 'loocv': loocv, 'w20': w20,
                        'params': list(params)})

    # Summary
    print('\n' + '=' * 80)
    print('=== v47 RESULTS — sorted by LOOCV ===')
    print('=' * 80)
    print(f'{"var":4s}  {"k":>3s}  {"R²":>8s}  {"LOOCV":>8s}  {"w20":>10s}  description')
    for r in sorted(results, key=lambda x: -x['loocv']):
        print(f'  {r["variant"]:3s}  {r["k"]:>3d}  '
              f'{r["r2"]:8.4f}  {r["loocv"]:8.4f}  '
              f'{r["w20"]:>3d}/{len(df)}    {r["label"]}')

    v0 = next(r for r in results if r['variant'] == 'V0')
    best_loocv = max(results, key=lambda r: r['loocv'])
    print(f'\nv29 baseline (V0): LOOCV={v0["loocv"]:.4f}')
    print(f'Best LOOCV:        {best_loocv["variant"]} (LOOCV={best_loocv["loocv"]:.4f})')
    delta = best_loocv['loocv'] - v0['loocv']
    if delta > 0.005:
        print(f'  ⭐ Improvement: ΔLOOCV = +{delta:.4f}  → real new signal')
    elif delta > 0:
        print(f'  Marginal: ΔLOOCV = +{delta:.4f}  (within noise)')
    else:
        print(f'  No improvement: ΔLOOCV = {delta:+.4f}')
        print('  → v29 framework already captures all generalisable signal')

    out = Path('docs/figures/physics_regime')
    out.mkdir(parents=True, exist_ok=True)
    with open(out / 'physics_fit_v47_min_plastic.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print(f'\n→ {out}/physics_fit_v47_min_plastic.json')


if __name__ == '__main__':
    main()
