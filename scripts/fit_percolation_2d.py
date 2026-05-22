"""
fit_percolation_2d.py — Phase C1.

세미나 피드백 #3 (Percolation threshold 계산) + #6 (조성 파라미터 →
percolation generalize) 직접 대응.

모델 — Kirkpatrick 3D scaling:
  σ_ionic = σ_0 × max(0, φ_SE − φc(λ))^t
  φc(λ)   = φc_inf − A × λ^(−α)

  percolation_pct 대신 σ_ionic을 fit target으로 선택: 대부분 case가
  이미 percolation saturated (97-99.5%) → sigmoid 못 잡음.  σ_ionic은
  0.001-0.7 mS/cm 넓은 dynamic range, Kirkpatrick power-law 직접 fit 가능.

이론값:
  • Bruggeman EMT:    φc = 1/3
  • Kirkpatrick 1973: t ≈ 2.0 (3D)

출력:
  docs/figures/percolation_2d_fit.png   (4-panel paper figure)
  docs/data/percolation_2d_fit.csv      (per-case data + fit residual)
"""
from __future__ import annotations
import csv
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.optimize import differential_evolution

ROOT = Path(__file__).resolve().parent.parent

RHO_AM = 4.8   # NCM811 g/cc
RHO_SE = 2.0   # LPSCl g/cc


def fnum(s):
    try: return float(s)
    except (TypeError, ValueError): return None


def tier_of(case_name: str) -> str:
    for t in ['1mAh', '6mAh', '8mAh']:
        if t in case_name: return t
    if 'particulate' in case_name: return 'particulate'
    if case_name.startswith('input_S_'): return 'S'
    return 'other'


def composition_class(ps_ratio: str) -> str:
    if not ps_ratio or ':' not in str(ps_ratio):
        return 'unknown'
    try:
        a, b = (float(x) for x in str(ps_ratio).split(':')[:2])
    except (ValueError, IndexError):
        return 'unknown'
    if a > 0 and b == 0: return 'mono AM_P'
    if a == 0 and b > 0: return 'mono AM_S'
    if a > 0 and b > 0:  return 'bimodal'
    return 'unknown'


def load_data():
    csv_path = ROOT / 'docs' / 'case_summary.csv'
    rows = list(csv.DictReader(open(csv_path)))
    out = []
    for r in rows:
        name = r.get('meta__name') or r.get('case_id')
        if not name or not name.startswith('input_'):
            continue
        am_se_str = r.get('fm__am_se_ratio') or r.get('ip__am_se_ratio')
        wt_am = None
        if am_se_str and ':' in str(am_se_str):
            try:
                a, b = (float(x) for x in str(am_se_str).split(':')[:2])
                if a + b > 0:
                    wt_am = a / (a + b)
            except (ValueError, IndexError):
                pass
        if wt_am is None or not (0.05 < wt_am < 0.99):
            continue
        V_AM = wt_am / RHO_AM
        V_SE = (1 - wt_am) / RHO_SE
        phi_SE = V_SE / (V_AM + V_SE)

        rse = fnum(r.get('ip__r_SE_um')) or fnum(r.get('ip__r_SE')) or 0
        if rse and rse < 0.01:
            rse = rse * (fnum(r.get('meta__scale')) or 1000)
        rp = fnum(r.get('ip__r_AM_P_um')) or fnum(r.get('ip__r_AM_P')) or 0
        if rp and rp < 0.01: rp = rp * (fnum(r.get('meta__scale')) or 1000)
        rs = fnum(r.get('ip__r_AM_S_um')) or fnum(r.get('ip__r_AM_S')) or 0
        if rs and rs < 0.01: rs = rs * (fnum(r.get('meta__scale')) or 1000)
        if rp > 0 and rs > 0:
            r_AM_eff = (rp + rs) / 2
        elif rp > 0:
            r_AM_eff = rp
        elif rs > 0:
            r_AM_eff = rs
        else:
            continue
        if rse <= 0: continue
        lam_eff = r_AM_eff / rse

        perc = fnum(r.get('fm__percolation_pct'))
        sigma_i = (fnum(r.get('fm__sigma_full_mScm_stage_e_physics'))
                   or fnum(r.get('fm__sigma_full_mScm_physics'))
                   or fnum(r.get('fm__sigma_full_mScm_stage_e'))
                   or fnum(r.get('fm__sigma_full_mScm')))
        if sigma_i is None or sigma_i <= 0:
            continue

        out.append({
            'case_name':       name,
            'tier':            tier_of(name),
            'composition':     composition_class(r.get('meta__ps_ratio', '')),
            'mode':            r.get('meta__mode', ''),
            'wt_AM':           round(wt_am, 4),
            'phi_SE':          round(phi_SE, 4),
            'r_SE_um':         rse,
            'r_AM_eff_um':     r_AM_eff,
            'lam_eff':         round(lam_eff, 3),
            'percolation_pct': round(perc, 2) if perc is not None else None,
            'sigma_ionic_mScm': sigma_i,
        })
    return out


def kirkpatrick(params, phi, lam):
    """σ_ionic = σ_0 × max(0, φ - φc(λ))^t,
       φc(λ) = φc_inf - A × λ^(-α)
    """
    sigma_0, phi_c_inf, A, alpha, t = params
    phi_c = phi_c_inf - A * np.power(np.clip(lam, 0.1, None), -alpha)
    delta = np.maximum(0, phi - phi_c)
    return sigma_0 * np.power(delta, t)


def fit_surface(data):
    phi   = np.array([d['phi_SE']            for d in data])
    lam   = np.array([d['lam_eff']           for d in data])
    sigma = np.array([d['sigma_ionic_mScm']  for d in data])

    log_sigma = np.log10(np.maximum(sigma, 1e-5))

    def loss(p):
        pred = kirkpatrick(p, phi, lam)
        log_pred = np.log10(np.maximum(pred, 1e-5))
        return float(np.sqrt(np.mean((log_pred - log_sigma) ** 2)))

    bounds = [(1.0, 100.0), (0.05, 0.35), (0.0, 0.20),
              (0.1, 2.0), (1.0, 3.5)]
    res = differential_evolution(loss, bounds, seed=42, maxiter=500,
                                  popsize=40, tol=1e-8, polish=True)
    return res.x, loss(res.x), res


def make_figure(data, params, rmse_log):
    sigma_0, phi_c_inf, A, alpha, t = params
    phi   = np.array([d['phi_SE']           for d in data])
    lam   = np.array([d['lam_eff']          for d in data])
    sigma = np.array([d['sigma_ionic_mScm'] for d in data])
    pred  = kirkpatrick(params, phi, lam)

    composition_colors = {'mono AM_P': '#dc2626', 'bimodal': '#10b981',
                           'mono AM_S': '#2563eb', 'unknown': '#888'}
    comp_arr = [d['composition'] for d in data]

    fig = plt.figure(figsize=(15, 11))
    gs = fig.add_gridspec(2, 2, hspace=0.35, wspace=0.30)

    # Panel 1: σ vs φ (semi-log)
    ax = fig.add_subplot(gs[0, 0])
    for cls in ['mono AM_P', 'bimodal', 'mono AM_S']:
        idx = [i for i, c in enumerate(comp_arr) if c == cls]
        if idx:
            ax.scatter(phi[idx], sigma[idx], color=composition_colors[cls],
                        s=45, alpha=0.7, label=f'{cls} (n={len(idx)})',
                        edgecolor='black', linewidth=0.5)
    lam_med = float(np.median(lam))
    phi_grid = np.linspace(0.05, 0.55, 300)
    ax.plot(phi_grid, kirkpatrick(params, phi_grid, np.full_like(phi_grid, lam_med)),
            'k-', linewidth=2, label=f'fit @ λ={lam_med:.1f}')
    ax.axvline(1/3, linestyle='--', color='gray', linewidth=1)
    ax.text(1/3 + 0.005, 0.001, 'Bruggeman φc=1/3', rotation=90,
            ha='left', va='bottom', fontsize=9, color='gray')
    phi_c_med = phi_c_inf - A * lam_med ** (-alpha)
    ax.axvline(phi_c_med, linestyle=':', color='red', linewidth=1.5)
    ax.text(phi_c_med + 0.005, 0.001, f'fit φc(λ_med)={phi_c_med:.3f}',
            rotation=90, ha='left', va='bottom', fontsize=9, color='red')
    ax.set_xlabel('φ_SE  (volume fraction of solid electrolyte)', fontsize=11)
    ax.set_ylabel('σ_ionic  (mS/cm)', fontsize=11)
    ax.set_yscale('log')
    ax.set_title('Kirkpatrick fit @ median λ_eff', fontsize=11)
    ax.legend(loc='lower right', fontsize=9)
    ax.set_xlim(0, 0.65); ax.set_ylim(0.0005, 2)
    ax.grid(alpha=0.3, which='both')

    # Panel 2: log-log scaling collapse
    ax = fig.add_subplot(gs[0, 1])
    phi_c_each = phi_c_inf - A * np.power(lam, -alpha)
    delta_phi = phi - phi_c_each
    valid = delta_phi > 0
    for cls in ['mono AM_P', 'bimodal', 'mono AM_S']:
        idx = [i for i, c in enumerate(comp_arr) if c == cls and valid[i]]
        if idx:
            ax.scatter(delta_phi[idx], sigma[idx],
                        color=composition_colors[cls],
                        s=45, alpha=0.7, label=f'{cls}',
                        edgecolor='black', linewidth=0.5)
    x_grid = np.logspace(-2.5, 0, 200)
    ax.plot(x_grid, sigma_0 * x_grid ** t, 'k-', linewidth=2,
             label=f'σ₀×(φ−φc)^t,  t={t:.2f}')
    ax.plot(x_grid, sigma_0 * x_grid ** 2, 'k--', linewidth=1, alpha=0.5,
             label='theory t=2 (Kirkpatrick 1973)')
    ax.set_xlabel('φ_SE − φc(λ_eff)', fontsize=11)
    ax.set_ylabel('σ_ionic  (mS/cm)', fontsize=11)
    ax.set_xscale('log'); ax.set_yscale('log')
    ax.set_title(f'Power-law collapse — exponent t = {t:.2f}', fontsize=11)
    ax.legend(loc='lower right', fontsize=9)
    ax.grid(alpha=0.3, which='both')

    # Panel 3: 2D contour
    ax = fig.add_subplot(gs[1, 0])
    phi_g, lam_g = np.meshgrid(np.linspace(0.05, 0.55, 100),
                                 np.logspace(np.log10(1.5), np.log10(20), 80))
    sigma_g = kirkpatrick(params, phi_g, lam_g)
    log_g = np.log10(np.maximum(sigma_g, 1e-5))
    cs = ax.contourf(phi_g, lam_g, log_g, levels=20, cmap='viridis')
    lam_curve = np.logspace(np.log10(1.5), np.log10(20), 100)
    phi_c_curve = phi_c_inf - A * np.power(lam_curve, -alpha)
    ax.plot(phi_c_curve, lam_curve, 'r-', linewidth=2.5,
             label=f'φc(λ) = {phi_c_inf:.3f} − {A:.4f}·λ^(−{alpha:.2f})')
    ax.scatter(phi, lam, c=np.log10(np.maximum(sigma, 1e-5)),
                cmap='viridis', s=70,
                edgecolor='black', linewidth=0.8)
    plt.colorbar(cs, ax=ax, label='log₁₀(σ_ionic / mS·cm⁻¹)',
                  fraction=0.046, pad=0.04)
    ax.set_yscale('log')
    ax.set_xlabel('φ_SE', fontsize=11)
    ax.set_ylabel('λ_eff', fontsize=11)
    ax.set_title('2D σ_ionic surface + φc(λ) threshold', fontsize=10)
    ax.legend(loc='upper left', fontsize=9)
    ax.grid(alpha=0.3, which='both')

    # Panel 4: parity
    ax = fig.add_subplot(gs[1, 1])
    for cls in ['mono AM_P', 'bimodal', 'mono AM_S']:
        idx = [i for i, c in enumerate(comp_arr) if c == cls]
        if idx:
            ax.scatter(sigma[idx], pred[idx], color=composition_colors[cls],
                        s=45, alpha=0.7, label=f'{cls}',
                        edgecolor='black', linewidth=0.5)
    lo, hi = 1e-4, 2
    ax.plot([lo, hi], [lo, hi], 'k--', linewidth=1, alpha=0.5)
    ax.set_xlabel('measured σ_ionic (mS/cm)', fontsize=11)
    ax.set_ylabel('predicted σ_ionic (mS/cm)', fontsize=11)
    ax.set_xscale('log'); ax.set_yscale('log')
    log_p = np.log10(np.maximum(pred, 1e-5))
    log_m = np.log10(np.maximum(sigma, 1e-5))
    R2 = 1 - np.sum((log_p - log_m)**2) / np.sum((log_m - log_m.mean())**2)
    ax.set_title(f'Parity (log-log) — R²(log) = {R2:.3f}, '
                  f'RMSE(log) = {rmse_log:.3f}', fontsize=11)
    ax.legend(loc='lower right', fontsize=9)
    ax.set_xlim(lo, hi); ax.set_ylim(lo, hi)
    ax.grid(alpha=0.3, which='both')

    fig.suptitle('SE percolation 2D scaling law — '
                  'σ_ionic = σ₀·(φ_SE − φc(λ))^t   [Phase C1]',
                  fontsize=13, fontweight='bold', y=0.995)

    out_png = ROOT / 'docs' / 'figures' / 'percolation_2d_fit.png'
    out_png.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_png, dpi=130, bbox_inches='tight')
    plt.close(fig)
    return out_png, R2


def save_csv(data, params):
    out_csv = ROOT / 'docs' / 'data' / 'percolation_2d_fit.csv'
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    sigma_0, phi_c_inf, A, alpha, t = params
    rows = []
    for d in data:
        phi_c = phi_c_inf - A * (d['lam_eff'] ** (-alpha))
        pred = float(kirkpatrick(params, np.array([d['phi_SE']]),
                                   np.array([d['lam_eff']]))[0])
        rows.append({**d,
                      'phi_c_at_this_lam': round(phi_c, 4),
                      'phi_minus_phi_c':   round(d['phi_SE'] - phi_c, 4),
                      'predicted_sigma_mScm': round(pred, 5),
                      'residual_log':      round(np.log10(max(d['sigma_ionic_mScm'], 1e-5))
                                                   - np.log10(max(pred, 1e-5)), 3)})
    keys = list(rows[0].keys())
    with open(out_csv, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader(); w.writerows(rows)
    return out_csv


def main():
    print('Loading data from docs/case_summary.csv ...')
    data = load_data()
    print(f'  {len(data)} cases with valid (wt_AM, λ_eff, σ_ionic)')

    print('\nKirkpatrick scaling fit (log-space global) ...')
    params, rmse_log, res = fit_surface(data)
    sigma_0, phi_c_inf, A, alpha, t = params

    print('\n' + '─' * 65)
    print('Fit results — σ_ionic = σ₀ × (φ_SE − φc(λ))^t')
    print('             φc(λ) = φc_inf − A × λ^(−α)')
    print('─' * 65)
    print(f'  σ_0     = {sigma_0:.3f} mS/cm   (asymptotic max)')
    print(f'  φc_inf  = {phi_c_inf:.4f}        (vs Bruggeman 1/3 ≈ 0.333)')
    print(f'  A       = {A:.5f}')
    print(f'  α       = {alpha:.3f}')
    print(f'  t       = {t:.3f}        (Kirkpatrick 1973 theory: 2.0)')
    print(f'  RMSE(log₁₀σ) = {rmse_log:.3f}')

    print(f'\n  φc at various λ_eff:')
    for lam_val in [2, 4, 6, 10, 15]:
        phi_c = phi_c_inf - A * lam_val ** (-alpha)
        print(f'    λ={lam_val:>3}: φc = {phi_c:.4f}')

    fig_path, r2 = make_figure(data, params, rmse_log)
    csv_path = save_csv(data, params)
    print(f'\n  R²(log) = {r2:.3f}')
    print(f'  Figure → {fig_path}')
    print(f'  CSV    → {csv_path}')


if __name__ == '__main__':
    main()
