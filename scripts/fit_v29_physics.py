#!/usr/bin/env python3
"""Fit a separate v29 model on Physics-mode (coverage_phys, σ_phys).

We ran the baseline v29 against Hertzian (coverage, σ). Earlier diagnostic
showed a uniform 0.83× prefactor suffices to transport that fit to
Physics mode, but the scale-only recovery caps at R² ≈ 0.96 (vs 0.988
in the native Hertzian fit). This script does a **full independent fit**
on Physics data — same functional form, all 14 hyperparameters re-
optimised — and reports:

  • Side-by-side param comparison (Hertzian vs Physics)
  • R², LOOCV, w20 band in both modes
  • What shifted, what stayed

The logic mirrors plot_ionic_scaling_fit's Nelder-Mead + OLS inner loop
but runs standalone (no plotting, no webapp coupling).
"""
from __future__ import annotations
import sys, json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.optimize import minimize

SCRIPTS = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS))

from v32_exhaustive_refit import load_cases  # noqa: E402
from generate_comparison_plots import _ps_fraction  # noqa: E402

SIGMA_GRAIN = 3.0
PHI_C = 0.20
# Fixed v5 sigmoid shape (C(τ) asymptote blend)
TAU_C_V5 = 2.1
TAU_K_V5 = 5.0


def load_phys_data(cases):
    """Enrich with Physics-mode coverage + σ from full_metrics.json.
    Drops cases that lack Physics keys."""
    rows = []
    for c in cases:
        cid = c['case_id']
        fm = None
        for base in ('results', 'archive'):
            for p in Path(f'webapp/{base}').rglob(f'{cid}/full_metrics.json'):
                try:
                    fm = json.load(open(p))
                except Exception:
                    pass
                break
            if fm is not None:
                break
        if fm is None:
            continue

        cov_p_keys = [fm.get(k) for k in
                      ('coverage_AM_P_mean_physics',
                       'coverage_AM_S_mean_physics',
                       'coverage_AM_mean_physics')]
        cov_p_vals = [v for v in cov_p_keys if v and v > 0]
        if not cov_p_vals:
            continue
        cov_p = sum(cov_p_vals) / len(cov_p_vals) / 100.0

        cov_h_keys = [fm.get(k) for k in
                      ('coverage_AM_P_mean',
                       'coverage_AM_S_mean',
                       'coverage_AM_mean')]
        cov_h_vals = [v for v in cov_h_keys if v and v > 0]
        cov_h = sum(cov_h_vals) / len(cov_h_vals) / 100.0 if cov_h_vals else None

        sig_p = fm.get('sigma_full_mScm_physics')
        sig_h = fm.get('sigma_full_mScm')
        if sig_p is None or sig_p <= 0 or sig_h is None or sig_h <= 0:
            continue

        r = dict(c)
        r.update(cov_hertz=cov_h, cov_phys=cov_p,
                 sigma_hertz=sig_h, sigma_phys=sig_p)
        rows.append(r)
    return rows


def fit_v29(df, cov_key, sig_key, label=''):
    """Nelder-Mead fit of v29 on (cov_key, sig_key). Returns fitted params."""
    # Extract arrays
    n = len(df)
    phi = df['phi'].values
    cn = df['cn'].values
    tau = df['tau'].values
    cov = df[cov_key].values
    fp = df['f_perc'].values
    gb = np.array([max(g, 1e-6) for g in df['gb_dens'].values])
    pf = df['p_frac'].values
    sigma_actual = df[sig_key].values

    phi_ex = np.maximum(phi - PHI_C, 1e-4)
    log_sf = np.log(sigma_actual)
    log_tau = np.log(np.maximum(tau, 1e-6))
    # Base v12 Kirkpatrick-inspired term (without C(τ))
    log_rhs_base = (np.log(SIGMA_GRAIN) + 0.5*np.log(phi_ex) + 1.5*np.log(cn)
                    + 0.4*np.log(np.maximum(cov, 1e-6)) + 3.0*np.log(np.maximum(fp, 0.01)))
    w_v5 = 1.0 / (1.0 + np.exp(-TAU_K_V5 * (tau - TAU_C_V5)))
    ss_tot = np.sum((log_sf - np.mean(log_sf))**2)

    def fit_at(k_bl, tc_bl, k_pf, pc_pf, tcw, stw):
        w_pf = 1.0 / (1.0 + np.exp(-k_pf * (pf - pc_pf)))
        w_win = np.exp(-0.5 * ((tau - tcw) / max(stw, 0.05))**2)
        w_bl = 1.0 / (1.0 + np.exp(-k_bl * (tau - tc_bl)))
        X_v5 = np.column_stack([np.ones(n), w_v5])
        X_p3 = np.column_stack([np.ones(n), log_tau, log_tau**2, log_tau**3])
        b_v5 = np.linalg.lstsq(X_v5, log_sf - log_rhs_base, rcond=None)[0]
        b_p3 = np.linalg.lstsq(X_p3, log_sf - log_rhs_base, rcond=None)[0]
        pv = X_v5 @ b_v5
        pp = X_p3 @ b_p3
        pred_pre = (1 - w_bl) * pv + w_bl * pp + log_rhs_base

        # residual correction: 3-term (β_pf, β_lin, β_gb)
        pf_c = w_pf - w_pf.mean()
        lin_c = (pf * w_win) - (pf * w_win).mean()
        gb_log = np.log(gb)
        gc_gb = float(np.median(gb_log))
        w_gb = 1.0 / (1.0 + np.exp(-4.0 * (gb_log - gc_gb)))
        gb_c = w_gb - w_gb.mean()
        X_corr = np.column_stack([pf_c, lin_c, gb_c])
        resid = log_sf - pred_pre
        bc = np.linalg.lstsq(X_corr, resid, rcond=None)[0]
        pred = pred_pre + X_corr @ bc
        r2 = 1 - np.sum((log_sf - pred)**2) / ss_tot
        sse_loo = 0.0
        for i in range(n):
            mk = np.ones(n, bool); mk[i] = False
            bv_ = np.linalg.lstsq(X_v5[mk], (log_sf - log_rhs_base)[mk], rcond=None)[0]
            bp_ = np.linalg.lstsq(X_p3[mk], (log_sf - log_rhs_base)[mk], rcond=None)[0]
            p_pre_i = (1 - w_bl[i]) * (X_v5[i] @ bv_) + w_bl[i] * (X_p3[i] @ bp_) + log_rhs_base[i]
            pf_c_mk = w_pf[mk] - w_pf[mk].mean()
            lin_mk = (pf[mk] * w_win[mk]); lin_c_mk = lin_mk - lin_mk.mean()
            gb_c_mk = w_gb[mk] - w_gb[mk].mean()
            Xc_mk = np.column_stack([pf_c_mk, lin_c_mk, gb_c_mk])
            bc_mk = np.linalg.lstsq(Xc_mk, (log_sf - pred_pre)[mk], rcond=None)[0]
            pred_i = p_pre_i + bc_mk[0]*(w_pf[i] - w_pf[mk].mean()) \
                    + bc_mk[1]*(pf[i]*w_win[i] - lin_mk.mean()) \
                    + bc_mk[2]*(w_gb[i] - w_gb[mk].mean())
            sse_loo += (log_sf[i] - pred_i)**2
        loocv = 1 - sse_loo / ss_tot
        s_pred = np.exp(pred)
        w20 = int(np.sum(np.abs(s_pred - sigma_actual) / sigma_actual < 0.20))
        return r2, loocv, w20, b_v5, b_p3, w_bl, bc

    def neg_loocv(x):
        k_, tc_, kp_, pc_, tcw_, stw_ = x
        if k_ <= 0.1 or k_ > 20 or tc_ < 1.2 or tc_ > 3.0: return 1e6
        if kp_ <= 0.05 or kp_ > 50 or pc_ < 0.1 or pc_ > 0.9: return 1e6
        if tcw_ < 1.2 or tcw_ > 3.0 or stw_ < 0.10 or stw_ > 1.0: return 1e6
        return -fit_at(k_, tc_, kp_, pc_, tcw_, stw_)[1]

    res = minimize(neg_loocv, x0=[5.0, 2.0, 10.0, 0.5, 2.0, 0.3],
                   method='Nelder-Mead',
                   options={'xatol': 1e-3, 'fatol': 1e-5, 'maxiter': 600, 'adaptive': True})
    bk, btc, bkp, bpc, btcw, bstw = res.x
    r2, loocv, w20, b_v5, b_p3, _, bc = fit_at(bk, btc, bkp, bpc, btcw, bstw)
    C_thick = float(np.exp(b_v5[0]))
    C_thin = float(np.exp(b_v5[0] + b_v5[1]))

    print(f'\n── {label} fit ──')
    print(f'  n={n}')
    print(f'  R²      = {r2:.4f}')
    print(f'  LOOCV   = {loocv:.4f}')
    print(f'  |err|<20% = {w20}/{n}')
    print(f'  v5 sigmoid: C_thick={C_thick:.4f}  C_thin={C_thin:.4f}  Ct/Cn={C_thick/C_thin:.2f}')
    print(f'  blend     : K_BL={bk:.2f}  TC_BL={btc:.2f}')
    print(f'  P:S sigm  : K_PF={bkp:.2f}  PC_PF={bpc:.2f}  β_pf={bc[0]:+.3f}')
    print(f'  lin term  : TAU_C_WIN={btcw:.2f}  SIG_TW={bstw:.3f}  β_lin={bc[1]:+.3f}')
    print(f'  gb term   : β_gb={bc[2]:+.3f}')
    print(f'  poly3     : [{b_p3[0]:+.3f}, {b_p3[1]:+.3f}, {b_p3[2]:+.3f}, {b_p3[3]:+.3f}]')

    return dict(label=label, n=n, r2=r2, loocv=loocv, w20=w20,
                C_thick=C_thick, C_thin=C_thin,
                K_BL=bk, TC_BL=btc, K_PF=bkp, PC_PF=bpc,
                TAU_C_WIN=btcw, SIGMA_TAU_WIN=bstw,
                beta_pf=bc[0], beta_lin=bc[1], beta_gb=bc[2],
                poly3=tuple(float(x) for x in b_p3))


def main():
    rows = load_cases()
    df = pd.DataFrame(rows)
    df_ph = pd.DataFrame(load_phys_data(rows))
    if len(df_ph) == 0:
        print('No cases with Physics mode data. Run coverage_physics_vs_hertzian.py --all first.')
        return

    print(f'Loaded {len(df)} base cases, {len(df_ph)} with Physics data.')

    # Run both fits
    print('\n' + '=' * 70)
    print('Fit 1: Hertzian (cov_hertz, sigma_hertz)')
    print('=' * 70)
    fit_h = fit_v29(df_ph, 'cov_hertz', 'sigma_hertz', 'Hertzian')

    print('\n' + '=' * 70)
    print('Fit 2: Physics (cov_phys, sigma_phys)')
    print('=' * 70)
    fit_p = fit_v29(df_ph, 'cov_phys', 'sigma_phys', 'Physics')

    # Side-by-side comparison
    print('\n' + '=' * 70)
    print('SIDE-BY-SIDE PARAMETER COMPARISON')
    print('=' * 70)
    print(f'{"param":20s} {"Hertzian":>12s} {"Physics":>12s} {"ΔPhys/Hz":>12s}')
    for k in ['n', 'r2', 'loocv', 'w20',
              'C_thick', 'C_thin', 'K_BL', 'TC_BL',
              'K_PF', 'PC_PF', 'beta_pf', 'beta_lin', 'beta_gb',
              'TAU_C_WIN', 'SIGMA_TAU_WIN']:
        h = fit_h[k]; p = fit_p[k]
        if isinstance(h, (int, float)) and h != 0:
            ratio = p / h if abs(h) > 1e-9 else float('nan')
            print(f'{k:20s} {h:>12.4f} {p:>12.4f} {ratio:>12.3f}×')
        else:
            print(f'{k:20s} {h:>12} {p:>12}')
    # poly3 separately
    print(f'poly3(Hertz)  : [{", ".join(f"{x:+.3f}" for x in fit_h["poly3"])}]')
    print(f'poly3(Phys)   : [{", ".join(f"{x:+.3f}" for x in fit_p["poly3"])}]')

    # Save
    out = {'hertz': fit_h, 'phys': fit_p}
    with open('docs/figures/physics_regime/v29_physics_fit.json', 'w') as f:
        json.dump(out, f, indent=2, default=lambda x: list(x) if hasattr(x, '__iter__') else x)
    print(f"\n→ saved docs/figures/physics_regime/v29_physics_fit.json")


if __name__ == '__main__':
    main()
