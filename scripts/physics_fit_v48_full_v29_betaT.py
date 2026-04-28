#!/usr/bin/env python3
"""Physics-mode fit v48 — FULL v29 + β_T (Tabor binding share).

v47 found that adding b_tabor as a single feature to a SIMPLIFIED v29
(15 param) baseline gave +0.049 LOOCV improvement. But that v47
baseline (LOOCV=0.847) was lower than the full original v29
(fit_v29_physics.py: LOOCV=0.941) because it omitted the β_gb and
k_gb terms.

This script tests the same β_T addition against the FULL v29 form
(all 15 original params including β_gb, k_gb, τ_c_win) — fair
comparison. If the +β_T term still helps, we have the real
publication form.

Two variants tested:

  F0  Full v29 PHYSICS (15 params)             — control, target LOOCV ≈ 0.94
        Same form/parameters as fit_v29_physics.py
  F1  Full v29 + β_T · b_tabor (16 params)     — proposed extension

If F1 LOOCV > F0 LOOCV by > 0.005, **v48 is the new publication form**.
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
ALPHA_FIX = 0.5; BETA_FIX = 1.5; GAMMA_FIX = 0.4; DELTA_FIX = 3.0
PHI_C_FIX = 0.20


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


def predict_v29_full(df, params, beta_T=0.0):
    """FULL v29 physics-mode form (all 15 original params).

    Layout:
       0-1   C_thick, C_thin               (v5 sigmoid asymptotes)
       2-3   K_BL, tau_c_BL                 (blend weight)
       4-7   a0, a1, a2, a3                 (poly3 in log τ)
       8-10  beta_pf, k_pf, p_c             (P:S sigmoid)
      11-13  beta_lin, tau_c_win, s_win     (τ-bump Gaussian)
      14    beta_gb                         (GB sigmoid amplitude)
                                            (k_gb fixed = 4.0 per docs)

    Optional: beta_T multiplies b_tabor (centered) — added on top.
    """
    (C_thick, C_thin, K_BL, tau_c_BL,
     a0, a1, a2, a3,
     beta_pf, k_pf, p_c,
     beta_lin, tau_c_win, s_win,
     beta_gb) = params

    K_GB_FIX = 4.0   # docs: fixed per v29

    phi = df['phi'].values
    tau = df['tau'].values
    cn  = df['cn'].values
    cov = df['cov_phys'].values
    f_p = df['f_perc'].values
    p   = df['p_frac'].values
    rho_gb = np.maximum(df['gb_dens'].values, 1e-6)

    excess = np.maximum(phi - PHI_C_FIX, 1e-6)
    log_base = (np.log(SIGMA_GRAIN)
                + ALPHA_FIX * np.log(excess)
                + BETA_FIX  * np.log(cn)
                + GAMMA_FIX * np.log(cov)
                + DELTA_FIX * np.log(f_p))

    # C_blend(τ) — v5 sigmoid (tau_0=2.1, k_tau=5.0 fixed) ⊕ poly3
    s_v5 = _sigmoid(5.0 * (tau - 2.1))
    log_Cv5 = (np.log(max(C_thick, 1e-6))
               + (np.log(max(C_thin, 1e-6)) - np.log(max(C_thick, 1e-6))) * s_v5)
    ln_t = np.log(np.maximum(tau, 0.01))
    log_Cp3 = a0 + a1 * ln_t + a2 * ln_t ** 2 + a3 * ln_t ** 3
    w_BL = _sigmoid(K_BL * (tau - tau_c_BL))
    log_Cblend = (1 - w_BL) * log_Cv5 + w_BL * log_Cp3

    # C_corr — 3 terms (P:S sigmoid + τ-bump × p + GB log-sigmoid)
    w_pf = _sigmoid(k_pf * (p - p_c))
    w_pf_c = w_pf - float(np.mean(w_pf))
    w_win = np.exp(-((tau - tau_c_win) / max(s_win, 0.05)) ** 2 / 2.0)
    pwwin = p * w_win
    pwwin_c = pwwin - float(np.mean(pwwin))
    ln_gb = np.log(rho_gb)
    w_gb = _sigmoid(K_GB_FIX * (ln_gb - float(np.median(ln_gb))))
    w_gb_c = w_gb - float(np.mean(w_gb))
    C_corr = beta_pf * w_pf_c + beta_lin * pwwin_c + beta_gb * w_gb_c

    # Optional: Tabor-binding correction
    if beta_T != 0.0:
        b_T = df['b_tabor'].values / 100.0
        b_T_c = b_T - float(np.mean(b_T))
        C_corr = C_corr + beta_T * b_T_c

    return np.exp(log_base + log_Cblend + C_corr)


def _bounds_v29_full():
    return [
        (0.001, 0.5), (0.001, 0.5),     # C_thick, C_thin
        (0.5, 12.0), (1.5, 3.5),         # K_BL, tau_c_BL
        (-6.0, 4.0), (-6.0, 6.0), (-8.0, 8.0), (-5.0, 5.0),  # poly3
        (-1.0, 1.0), (1.0, 80.0), (0.05, 0.95),  # P:S sigm
        (-3.0, 3.0), (1.5, 3.5), (0.05, 1.0),    # τ-bump
        (-1.0, 1.0),                              # beta_gb
    ]


def fit_F(df, with_beta_T, n_start=25):
    bounds = _bounds_v29_full()
    if with_beta_T:
        bounds = bounds + [(-3.0, 3.0)]

    rng = np.random.default_rng(42)
    best = None
    for s in range(n_start):
        x0 = [rng.uniform(*b) for b in bounds]
        def loss(p):
            try:
                if with_beta_T:
                    pred = predict_v29_full(df, p[:-1], beta_T=p[-1])
                else:
                    pred = predict_v29_full(df, p)
                err = np.log(df['sigma'].values + 1e-12) - np.log(pred + 1e-12)
                if not np.all(np.isfinite(err)):
                    return 1e9
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


def metrics_simple(actual, pred):
    a = np.log(actual + 1e-12); p = np.log(pred + 1e-12)
    ss_res = np.sum((a - p) ** 2); ss_tot = np.sum((a - a.mean()) ** 2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0.0
    err = np.abs(actual - pred) / np.maximum(actual, 1e-12)
    w20 = int(np.sum(err <= 0.20))
    return r2, w20


def loocv_F(df, with_beta_T):
    n = len(df); pred_loo = np.empty(n)
    for i in range(n):
        sub = df.drop(df.index[i]).reset_index(drop=True)
        # Inner LOOCV uses n_start=4 to keep total runtime tractable
        # (76 folds × 25 starts would take ~6 hours per variant).
        params = fit_F(sub, with_beta_T, n_start=4)
        held = df.iloc[[i]]
        if with_beta_T:
            pred_loo[i] = predict_v29_full(held, params[:-1], beta_T=params[-1])[0]
        else:
            pred_loo[i] = predict_v29_full(held, params)[0]
        if (i + 1) % 10 == 0:
            print(f'    progress: {i+1}/{n}', flush=True)
    a = np.log(df['sigma'].values + 1e-12); p = np.log(pred_loo + 1e-12)
    ss_res = np.sum((a-p)**2); ss_tot = np.sum((a - a.mean())**2)
    return 1 - ss_res / ss_tot if ss_tot > 0 else 0.0


def main():
    cases = load_cases()
    rows = enrich(load_phys_rows(cases))
    df = pd.DataFrame(rows)
    print(f'Loaded {len(df)} cases.')

    print('\n' + '=' * 80)
    print('F0 — Full v29 physics (15 params, control)')
    print('=' * 80)
    p0 = fit_F(df, with_beta_T=False)
    pred0 = predict_v29_full(df, p0)
    r2_0, w20_0 = metrics_simple(df['sigma'].values, pred0)
    print(f'  Joint-fit R²={r2_0:.4f}  w20={w20_0}/{len(df)}')
    print(f'  LOOCV (F0) ...')
    loocv_0 = loocv_F(df, with_beta_T=False)
    print(f'  LOOCV R²={loocv_0:.4f}')

    print('\n' + '=' * 80)
    print('F1 — Full v29 + β_T · b_tabor (16 params, proposed)')
    print('=' * 80)
    p1 = fit_F(df, with_beta_T=True)
    pred1 = predict_v29_full(df, p1[:-1], beta_T=p1[-1])
    r2_1, w20_1 = metrics_simple(df['sigma'].values, pred1)
    print(f'  Joint-fit R²={r2_1:.4f}  w20={w20_1}/{len(df)}')
    print(f'  β_T = {p1[-1]:+.4f}')
    print(f'  LOOCV (F1) ...')
    loocv_1 = loocv_F(df, with_beta_T=True)
    print(f'  LOOCV R²={loocv_1:.4f}')

    # Verdict
    print('\n' + '=' * 80)
    print('=== VERDICT ===')
    print('=' * 80)
    print(f'{"variant":40s}  {"k":>3s}  {"R²":>8s}  {"LOOCV":>8s}')
    print(f'{"F0 Full v29 physics (control)":40s}  {15:>3d}  {r2_0:8.4f}  {loocv_0:8.4f}')
    print(f'{"F1 Full v29 + β_T·b_tabor":40s}  {16:>3d}  {r2_1:8.4f}  {loocv_1:8.4f}')
    delta = loocv_1 - loocv_0
    print(f'\nΔLOOCV (F1 vs F0) = {delta:+.4f}')
    if delta > 0.005:
        print('  ⭐⭐ Real signal — v29 + β_T is the new publication form.')
        print(f'      σ = exp({p1[-1]:.3f} · b_tabor_centered) · σ_v29')
    elif delta > -0.002:
        print('  ≈ Tied. v29 still publication form; +β_T marginal.')
    else:
        print('  ❌ Adding β_T degrades LOOCV; v29 final.')

    out = Path('docs/figures/physics_regime')
    out.mkdir(parents=True, exist_ok=True)
    save = {
        'F0': {'r2': r2_0, 'loocv': loocv_0, 'w20': w20_0,
               'k': 15, 'params': list(p0)},
        'F1': {'r2': r2_1, 'loocv': loocv_1, 'w20': w20_1,
               'k': 16, 'params': list(p1), 'beta_T': float(p1[-1])},
        'delta_loocv': float(delta),
    }
    with open(out / 'physics_fit_v48_full_v29_betaT.json', 'w') as f:
        json.dump(save, f, indent=2)
    print(f'\n→ {out}/physics_fit_v48_full_v29_betaT.json')


if __name__ == '__main__':
    main()
