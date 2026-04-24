#!/usr/bin/env python3
"""Physics-mode final fit — multi-stage, free exponents, leverage-aware.

Previous attempts failed: 14-param fit hit boundary solutions, LOOCV
plunged to 0.24 indicating 1-2 leverage cases dominate. This script:

  Stage 1:  σ = σ_grain·(φ-φc)^α·CN^β·cov^γ·f_p^δ·τ^μ     [7 params]
  Stage 2:  + C(τ) simple:   × exp(c_t·(τ-τ_ref))          [+2 params]
  Stage 3:  + residual 3:    × exp(β_pf·w_pf + β_gb·w_gb)  [+5 params]

At each stage:
  • Multi-start Nelder-Mead (10 starts) with wide bounds
  • Report R², LOOCV, parameter values
  • Leverage analysis: drop each case, see which case moves LOOCV most
  • Decide stage with best R²/LOOCV trade-off

Goal: find the **highest-LOOCV Physics fit** achievable with any form.
If Physics data fundamentally resists fitting, quantify the limit.
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

SIGMA_GRAIN = 3.0


def load_phys_rows(cases):
    rows = []
    for c in cases:
        cid = c['case_id']; fm = None
        for base in ('results', 'archive'):
            for p in Path(f'webapp/{base}').rglob(f'{cid}/full_metrics.json'):
                try: fm = json.load(open(p))
                except Exception: pass
                break
            if fm is not None: break
        if fm is None: continue
        ph = [fm.get(k) for k in
              ('coverage_AM_P_mean_physics','coverage_AM_S_mean_physics','coverage_AM_mean_physics')]
        ph_v = [v for v in ph if v and v > 0]
        if not ph_v: continue
        cov_p = sum(ph_v)/len(ph_v)/100.0
        sig_p = fm.get('sigma_full_mScm_physics')
        if not (sig_p and sig_p > 0): continue
        r = dict(c); r.update(cov_phys=cov_p, sigma_phys=sig_p)
        rows.append(r)
    return rows


def _predict_stage(params, arr, stage):
    """Unified predictor. `params` structure depends on stage."""
    phi, cn, tau, cov, fp, pfr, gb = arr
    phi_ex = np.maximum(phi - params['phi_c'], 1e-5)
    lg = (params['b0']
          + params['alpha'] * np.log(phi_ex)
          + params['beta']  * np.log(np.maximum(cn, 1e-6))
          + params['gamma'] * np.log(np.maximum(cov, 1e-6))
          + params['delta'] * np.log(np.maximum(fp, 1e-3))
          + params['mu']    * np.log(np.maximum(tau, 1e-6)))
    if stage >= 2:
        lg = lg + params['c_t'] * (tau - params['tau_ref'])
    if stage >= 3:
        w_pf = 1.0 / (1.0 + np.exp(-params['k_pf'] * (pfr - params['pc_pf'])))
        gb_log = np.log(np.maximum(gb, 1e-9))
        w_gb = 1.0 / (1.0 + np.exp(-4.0 * (gb_log - params['gb_center'])))
        lg = lg + params['beta_pf'] * (w_pf - 0.5) \
                + params['beta_gb'] * (w_gb - 0.5)
    return lg


def _unpack(x, stage):
    p = dict(alpha=x[0], beta=x[1], gamma=x[2], delta=x[3],
             phi_c=x[4], mu=x[5], b0=x[6])
    i = 7
    if stage >= 2:
        p['c_t'] = x[i]; p['tau_ref'] = x[i+1]; i += 2
    if stage >= 3:
        p['k_pf']=x[i]; p['pc_pf']=x[i+1]; p['beta_pf']=x[i+2]
        p['gb_center']=x[i+3]; p['beta_gb']=x[i+4]; i += 5
    return p


def _bounds_ok(x, stage):
    a,b,g,d,pc,mu,b0 = x[:7]
    if not (0.1 < a < 4.0): return False
    if not (0.1 < b < 4.0): return False
    if not (-0.5 < g < 3.0): return False
    if not (0.3 < d < 7.0): return False
    if not (0.05 < pc < 0.35): return False
    if not (-4.0 < mu < 1.0): return False
    if not (-4.0 < b0 < 4.0): return False
    if stage >= 2:
        if not (-2.0 < x[7] < 2.0): return False  # c_t
        if not (0.5 < x[8] < 4.0): return False   # tau_ref
    if stage >= 3:
        if not (0.1 < x[9] < 30): return False    # k_pf
        if not (0.0 < x[10] < 1.0): return False  # pc_pf
        if not (-3 < x[11] < 3): return False     # beta_pf
        if not (-10 < x[12] < 0): return False    # gb_center
        if not (-2 < x[13] < 2): return False     # beta_gb
    return True


def fit_stage(df, cov_key, sig_key, stage, label=''):
    arr = (df['phi'].values, df['cn'].values, df['tau'].values,
           df[cov_key].values, df['f_perc'].values, df['p_frac'].values,
           np.maximum(df['gb_dens'].values, 1e-9))
    log_sig = np.log(df[sig_key].values)
    sst = np.sum((log_sig - log_sig.mean())**2)
    n = len(df)

    def neg_r2(x):
        if not _bounds_ok(x, stage): return 1e6
        p = _unpack(x, stage)
        try: lg = _predict_stage(p, arr, stage)
        except Exception: return 1e6
        if not np.all(np.isfinite(lg)): return 1e6
        return np.sum((log_sig - lg)**2) / sst

    # Multi-start
    starts_base = [
        [0.5, 1.5, 0.4, 3.0, 0.20, -1.0, np.log(SIGMA_GRAIN)],  # v29 like
        [2.0, 1.0, 0.4, 2.5, 0.20, -1.5, np.log(SIGMA_GRAIN)],  # theory
        [1.0, 0.8, 0.2, 4.0, 0.18, -0.5, np.log(SIGMA_GRAIN)],  # Hertzian fit result
        [1.1, 0.77, 0.24, 4.9, 0.174, -0.37, -0.35],            # prev Physics fit
        [0.7, 1.2, 0.5, 3.5, 0.22, -0.8, 0.5],                  # random mix
        [1.5, 0.5, 0.1, 2.0, 0.15, -2.0, -1.0],
    ]
    # Extra params for stages 2, 3
    stage2_extra = [0.0, 2.0]               # c_t=0 (C(τ) off initially), tau_ref=2
    stage3_extra = [10.0, 0.5, 0.0, -5.0, 0.0]  # k_pf, pc_pf, beta_pf, gb_center, beta_gb
    if stage >= 2: starts_base = [s + stage2_extra for s in starts_base]
    if stage >= 3: starts_base = [s + stage3_extra for s in starts_base]

    best = None
    for s in starts_base:
        try:
            res = minimize(neg_r2, x0=s, method='Nelder-Mead',
                           options={'xatol':1e-4,'fatol':1e-6,'maxiter':6000,'adaptive':True})
            if best is None or res.fun < best.fun:
                best = res
        except Exception: pass
    p = _unpack(best.x, stage)
    lg = _predict_stage(p, arr, stage)
    r2 = 1 - np.sum((log_sig - lg)**2) / sst

    # LOOCV (fast: refit using best.x as init for each fold)
    sse_loo = 0.0
    for i in range(n):
        mk = np.ones(n, bool); mk[i] = False
        arr_m = tuple(a[mk] for a in arr)
        log_m = log_sig[mk]
        sst_m = np.sum((log_m - log_m.mean())**2)
        def nr2_m(x):
            if not _bounds_ok(x, stage): return 1e6
            pp = _unpack(x, stage)
            try: lg_ = _predict_stage(pp, arr_m, stage)
            except Exception: return 1e6
            if not np.all(np.isfinite(lg_)): return 1e6
            return np.sum((log_m - lg_)**2) / sst_m
        res_i = minimize(nr2_m, x0=best.x, method='Nelder-Mead',
                         options={'xatol':1e-3,'fatol':1e-5,'maxiter':2000,'adaptive':True})
        p_i = _unpack(res_i.x, stage)
        arr_i = tuple(np.array([a[i]]) for a in arr)
        lg_i = _predict_stage(p_i, arr_i, stage)[0]
        sse_loo += (log_sig[i] - lg_i)**2
    loocv = 1 - sse_loo / sst
    w20 = int(np.sum(np.abs(np.exp(lg) - df[sig_key].values) / df[sig_key].values < 0.20))

    print(f'\n── Stage {stage} — {label} ──')
    print(f'  n={n}   R²={r2:.4f}   LOOCV={loocv:.4f}   w20={w20}/{n}')
    print(f'  params:')
    for k, v in p.items():
        print(f'    {k:12s} = {v:+.4f}')
    return dict(stage=stage, label=label, n=n, r2=float(r2), loocv=float(loocv),
                w20=w20, params={k: float(v) for k,v in p.items()})


def leverage_scan(df, cov_key, sig_key, stage=1):
    """Drop each case and see which has largest effect on R²/LOOCV."""
    arr_full = (df['phi'].values, df['cn'].values, df['tau'].values,
                df[cov_key].values, df['f_perc'].values, df['p_frac'].values,
                np.maximum(df['gb_dens'].values, 1e-9))
    log_sig = np.log(df[sig_key].values)
    base = fit_stage(df, cov_key, sig_key, stage, f'BASELINE stage {stage}')
    # Drop-one analysis: how much does R² change?
    impacts = []
    for i in range(len(df)):
        sub = df.drop(df.index[i]).reset_index(drop=True)
        r2 = fit_stage(sub, cov_key, sig_key, stage, f'drop-{df.iloc[i]["name"][:20]}')['r2']
        impacts.append((df.iloc[i]['name'], r2 - base['r2'], r2))
    impacts.sort(key=lambda x: -abs(x[1]))
    print(f'\n=== Leverage scan (top-10 most influential cases) ===')
    print(f'{"case":40s}  {"R² w/o case":>12s}  {"ΔR² vs full":>12s}')
    for nm, d, r2 in impacts[:10]:
        print(f'{nm[:40]:40s}  {r2:12.4f}  {d:+12.4f}')


def main():
    rows = load_cases()
    data = load_phys_rows(rows)
    df = pd.DataFrame(data)
    if len(df) == 0:
        print('No Physics data.'); return
    print(f'Loaded {len(df)} Physics-mode cases.')

    print('\n' + '=' * 75)
    print('STAGE PROGRESSION — find best R²/LOOCV trade-off')
    print('=' * 75)
    s1 = fit_stage(df, 'cov_phys', 'sigma_phys', 1, 'Physics pure power-law')
    s2 = fit_stage(df, 'cov_phys', 'sigma_phys', 2, 'Physics + simple C(τ)')
    s3 = fit_stage(df, 'cov_phys', 'sigma_phys', 3, 'Physics + residual 2-term')

    print('\n' + '=' * 75)
    print('=== STAGE SUMMARY ===')
    print(f'{"stage":30s}  {"R²":>8s}  {"LOOCV":>8s}  {"w20":>6s}')
    for s in [s1, s2, s3]:
        print(f'{s["label"][:30]:30s}  {s["r2"]:8.4f}  {s["loocv"]:8.4f}  '
              f'{s["w20"]:>3d}/{s["n"]}')

    out = {'stage1': s1, 'stage2': s2, 'stage3': s3}
    out_dir = Path('docs/figures/physics_regime')
    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_dir / 'physics_fit_final.json', 'w') as f:
        json.dump(out, f, indent=2)
    print(f'\n→ {out_dir}/physics_fit_final.json')


if __name__ == '__main__':
    main()
