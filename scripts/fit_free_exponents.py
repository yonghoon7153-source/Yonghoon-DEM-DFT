#!/usr/bin/env python3
"""Free-exponent fit: Hertzian vs Physics.

The main v29 model HARDCODES the exponents α=0.5, β=1.5, γ=0.4, δ=3.
They are claimed Kirkpatrick-inspired but differ substantially from
3D percolation theory (α ≈ 2 for continuum conductivity, Kirkpatrick
EMA β = 1 linear). The hypothesis: **Physics-mode data might recover
more theory-consistent exponents** because the Tabor+caps contact
areas reflect real material behaviour, whereas Hertzian areas are a
DEM-specific overestimate that biases the fit.

Fit a SIMPLE power-law form:

  log σ = log(σ_grain) + α·log(φ - φc) + β·log(CN)
        + γ·log(cov) + δ·log(f_p) + μ·log(τ)
        + b0

All six (α, β, γ, δ, φc, μ) + intercept b0 are FREE.
No C(τ) blend, no P:S sigmoid, no gb correction — just the core
power law. This isolates the question: what exponents does the data
prefer, once contact-area convention is fixed?

Runs both Hertzian and Physics targets, reports side-by-side.
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
        # Physics coverage
        ph_keys = [fm.get(k) for k in
                   ('coverage_AM_P_mean_physics',
                    'coverage_AM_S_mean_physics',
                    'coverage_AM_mean_physics')]
        ph_vals = [v for v in ph_keys if v and v > 0]
        if not ph_vals: continue
        cov_p = sum(ph_vals)/len(ph_vals)/100.0
        # Hertzian coverage
        hz_keys = [fm.get(k) for k in
                   ('coverage_AM_P_mean','coverage_AM_S_mean','coverage_AM_mean')]
        hz_vals = [v for v in hz_keys if v and v > 0]
        if not hz_vals: continue
        cov_h = sum(hz_vals)/len(hz_vals)/100.0
        sig_p = fm.get('sigma_full_mScm_physics')
        sig_h = fm.get('sigma_full_mScm')
        if not (sig_p and sig_p > 0 and sig_h and sig_h > 0): continue
        r = dict(c)
        r.update(cov_hertz=cov_h, cov_phys=cov_p,
                 sigma_hertz=sig_h, sigma_phys=sig_p)
        rows.append(r)
    return rows


def fit_free_exponents(df, cov_key, sig_key, label=''):
    """Fit σ = σ_grain·(φ-φc)^α·CN^β·cov^γ·f_p^δ·τ^μ (μ usually negative).
    Six free parameters: α, β, γ, δ, φc, μ. Plus b0 intercept for σ_grain scale.
    """
    phi = df['phi'].values
    cn = df['cn'].values
    tau = df['tau'].values
    cov = df[cov_key].values
    fp = df['f_perc'].values
    sig = df[sig_key].values
    n = len(df)
    log_sig = np.log(sig)

    def _predict(params):
        alpha, beta, gamma_, delta, phi_c, mu, b0 = params
        phi_ex = np.maximum(phi - phi_c, 1e-5)
        lg = (b0
              + alpha * np.log(phi_ex)
              + beta  * np.log(np.maximum(cn, 1e-6))
              + gamma_* np.log(np.maximum(cov, 1e-6))
              + delta * np.log(np.maximum(fp, 1e-3))
              + mu    * np.log(np.maximum(tau, 1e-6)))
        return lg

    def neg_r2(params):
        alpha, beta, gamma_, delta, phi_c, mu, b0 = params
        if not (0.1 < alpha < 3.5):   return 1e6
        if not (0.1 < beta  < 4.0):   return 1e6
        if not (0.0 <= gamma_ < 2.5): return 1e6
        if not (0.5 < delta < 6.0):   return 1e6
        if not (0.05 < phi_c < 0.35): return 1e6
        if not (-3.5 < mu < 0.5):     return 1e6
        lg = _predict(params)
        if not np.all(np.isfinite(lg)): return 1e6
        sse = np.sum((log_sig - lg)**2)
        sst = np.sum((log_sig - log_sig.mean())**2)
        return sse / sst

    # Starting point = Kirkpatrick-ish
    x0 = [0.5, 1.5, 0.4, 3.0, 0.20, -1.0, np.log(SIGMA_GRAIN)]
    best = None
    # Multi-start to avoid local mins
    starts = [x0,
              [2.0, 1.0, 0.4, 2.0, 0.20, -1.5, np.log(SIGMA_GRAIN)],  # theory-ish
              [1.0, 2.0, 1.0, 3.0, 0.15, -0.5, np.log(SIGMA_GRAIN)],
              [0.8, 1.0, 0.2, 2.5, 0.25, -2.0, np.log(SIGMA_GRAIN)]]
    for s in starts:
        res = minimize(neg_r2, x0=s, method='Nelder-Mead',
                       options={'xatol': 1e-4, 'fatol': 1e-6,
                                'maxiter': 4000, 'adaptive': True})
        if best is None or res.fun < best.fun:
            best = res

    alpha, beta, gamma_, delta, phi_c, mu, b0 = best.x
    lg = _predict(best.x)
    r2 = 1 - np.sum((log_sig - lg)**2) / np.sum((log_sig - log_sig.mean())**2)

    # LOOCV
    sse_loo = 0.0
    sst_loo = np.sum((log_sig - log_sig.mean())**2)
    for i in range(n):
        mk = np.ones(n, bool); mk[i] = False
        phi_m, cn_m, tau_m, cov_m, fp_m, sig_m = (
            phi[mk], cn[mk], tau[mk], cov[mk], fp[mk], sig[mk])
        log_sig_m = np.log(sig_m)
        def _neg_r2_loo(params):
            a, b, g, d, pc, m_, b0_ = params
            if not (0.1<a<3.5 and 0.1<b<4.0 and 0.0<=g<2.5 and
                    0.5<d<6.0 and 0.05<pc<0.35 and -3.5<m_<0.5):
                return 1e6
            phi_ex = np.maximum(phi_m - pc, 1e-5)
            lg_ = (b0_ + a*np.log(phi_ex) + b*np.log(np.maximum(cn_m,1e-6))
                   + g*np.log(np.maximum(cov_m,1e-6))
                   + d*np.log(np.maximum(fp_m,1e-3))
                   + m_*np.log(np.maximum(tau_m,1e-6)))
            if not np.all(np.isfinite(lg_)): return 1e6
            sse_ = np.sum((log_sig_m - lg_)**2)
            sst_ = np.sum((log_sig_m - log_sig_m.mean())**2)
            return sse_ / max(sst_, 1e-12)
        res_i = minimize(_neg_r2_loo, x0=best.x, method='Nelder-Mead',
                         options={'xatol':1e-3,'fatol':1e-5,'maxiter':1500,'adaptive':True})
        ai, bi, gi, di, pci, mi, b0i = res_i.x
        phi_ex_i = max(phi[i] - pci, 1e-5)
        lg_i = (b0i + ai*np.log(phi_ex_i) + bi*np.log(max(cn[i],1e-6))
                + gi*np.log(max(cov[i],1e-6)) + di*np.log(max(fp[i],1e-3))
                + mi*np.log(max(tau[i],1e-6)))
        sse_loo += (log_sig[i] - lg_i)**2
    loocv = 1 - sse_loo / sst_loo

    print(f'\n── {label} — Free-exponent fit ──')
    print(f'  n = {n}')
    print(f'  R²      = {r2:.4f}')
    print(f'  LOOCV   = {loocv:.4f}')
    print(f'  Fitted exponents (best of {len(starts)} starts):')
    print(f'    α (φ-φc)   = {alpha:+.3f}     [3D perc. theory ≈ 2.0]')
    print(f'    β (CN)     = {beta:+.3f}     [Kirkpatrick EMA = 1.0]')
    print(f'    γ (cov)    = {gamma_:+.3f}     [no theory]')
    print(f'    δ (f_p)    = {delta:+.3f}     [3D perc. ~ 2-3]')
    print(f'    μ (τ)      = {mu:+.3f}     [tortuosity penalty]')
    print(f'    φ_c        = {phi_c:+.4f}    [3D sphere packing ≈ 0.22]')
    print(f'    b0         = {b0:+.3f}     (ln σ_grain_effective = {b0:.3f} → {np.exp(b0):.2f} mS/cm)')
    return dict(label=label, n=n, r2=float(r2), loocv=float(loocv),
                alpha=float(alpha), beta=float(beta), gamma=float(gamma_),
                delta=float(delta), mu=float(mu), phi_c=float(phi_c),
                b0=float(b0), sigma_grain_eff=float(np.exp(b0)))


def main():
    rows = load_cases()
    data = load_phys_rows(rows)
    df = pd.DataFrame(data)
    if len(df) == 0:
        print('No dual-mode cases. Run coverage_physics_vs_hertzian.py --all first.')
        return
    print(f'Loaded {len(df)} dual-mode cases.')

    print('\n' + '=' * 70)
    fh = fit_free_exponents(df, 'cov_hertz', 'sigma_hertz', 'Hertzian')
    print('\n' + '=' * 70)
    fp = fit_free_exponents(df, 'cov_phys',  'sigma_phys',  'Physics')

    # Side-by-side
    print('\n' + '=' * 70)
    print('=== SIDE-BY-SIDE EXPONENT COMPARISON ===')
    print(f'{"exponent":12s}  {"Hertzian":>10s}  {"Physics":>10s}  {"Δ":>10s}  {"theory":>15s}')
    for k, th in [('alpha', '3D perc. ≈ 2.0'),
                  ('beta',  'EMA = 1.0'),
                  ('gamma', '—'),
                  ('delta', '3D perc. ~ 2-3'),
                  ('mu',    'τ penalty'),
                  ('phi_c', '≈ 0.20-0.22'),
                  ('sigma_grain_eff', 'literature 3.0')]:
        h, p = fh[k], fp[k]
        d = p - h
        print(f'{k:12s}  {h:10.3f}  {p:10.3f}  {d:+10.3f}  {th:>15s}')

    print(f'\nR² / LOOCV:')
    print(f'  Hertzian: R²={fh["r2"]:.4f}  LOOCV={fh["loocv"]:.4f}')
    print(f'  Physics:  R²={fp["r2"]:.4f}  LOOCV={fp["loocv"]:.4f}')

    # Save
    out_dir = Path('docs/figures/physics_regime')
    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_dir / 'free_exponent_fit.json', 'w') as f:
        json.dump({'hertzian': fh, 'physics': fp}, f, indent=2)
    print(f'\n→ {out_dir}/free_exponent_fit.json')


if __name__ == '__main__':
    main()
