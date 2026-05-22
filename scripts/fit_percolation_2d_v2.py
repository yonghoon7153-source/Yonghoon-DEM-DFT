"""
fit_percolation_2d_v2.py — Phase C1 (v2, comprehensive comparison).

v1 (baseline) 한계:
  • Global fit이 λ_eff 효과를 못 잡음 (A=0).
  • mono AM_S / mono AM_P 모두 fit residual 큼.
  • catastrophic failure (σ_ionic < 0.003 mS/cm) outlier가 fit 왜곡.

v2 전략 (B2 + B3 + B4 + B1 통합):
  • B2: σ_ionic < 0.003 mS/cm outlier 제거 — failed percolation 별도 처리.
  • B3: composition class별 (mono_AMP / bimodal / mono_AMS) 분리 fit.
  • B4: 단순 Bruggeman σ = σ_grain × φ^n baseline 같이 비교.
  • B1: φc(λ) multiplicative form 시도: φc(λ) = φc_inf × (1 − B/λ).

출력:
  docs/figures/percolation_2d_fit_v2.png   (4-panel comparison)
  docs/data/percolation_2d_fit_v2.csv      (per-case + 3 model predictions)
  콘솔: 4가지 모델 (global, class별, Bruggeman, multi-lambda) 비교 표.
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
RHO_AM, RHO_SE = 4.8, 2.0
OUTLIER_SIGMA_THRESHOLD = 0.003   # mS/cm — below this = failed percolation


def fnum(s):
    try: return float(s)
    except (TypeError, ValueError): return None


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

        sigma_i = (fnum(r.get('fm__sigma_full_mScm_stage_e_physics'))
                   or fnum(r.get('fm__sigma_full_mScm_physics'))
                   or fnum(r.get('fm__sigma_full_mScm_stage_e'))
                   or fnum(r.get('fm__sigma_full_mScm')))
        if sigma_i is None or sigma_i <= 0:
            continue
        out.append({
            'case_name':       name,
            'composition':     composition_class(r.get('meta__ps_ratio', '')),
            'wt_AM':           round(wt_am, 4),
            'phi_SE':          round(phi_SE, 4),
            'lam_eff':         round(lam_eff, 3),
            'sigma_ionic_mScm': sigma_i,
            'is_outlier':      sigma_i < OUTLIER_SIGMA_THRESHOLD,
        })
    return out


# ── Model 1: Kirkpatrick with additive λ ───────────────────────────────
def kirkpatrick_add(params, phi, lam):
    sigma_0, phi_c_inf, A, alpha, t = params
    phi_c = phi_c_inf - A * np.power(np.clip(lam, 0.1, None), -alpha)
    delta = np.maximum(0, phi - phi_c)
    return sigma_0 * np.power(delta, t)

# ── Model 2: Kirkpatrick with multiplicative λ (B1) ─────────────────────
def kirkpatrick_mul(params, phi, lam):
    sigma_0, phi_c_inf, B, t = params
    # φc(λ) = φc_inf × (1 − B/λ), bounded > 0
    phi_c = phi_c_inf * np.maximum(0.05, 1.0 - B / np.clip(lam, 0.1, None))
    delta = np.maximum(0, phi - phi_c)
    return sigma_0 * np.power(delta, t)

# ── Model 3: Pure Bruggeman σ = σ_grain × φ^n ──────────────────────────
def bruggeman(params, phi):
    sigma_grain, n = params
    return sigma_grain * np.power(phi, n)


def fit_model(data, model_fn, bounds, params_form='lambda', use_outlier=False):
    """Generic differential-evolution fit in log10(σ) space."""
    data_use = data if use_outlier else [d for d in data if not d['is_outlier']]
    phi   = np.array([d['phi_SE']           for d in data_use])
    lam   = np.array([d['lam_eff']          for d in data_use])
    sigma = np.array([d['sigma_ionic_mScm'] for d in data_use])

    log_sigma = np.log10(np.maximum(sigma, 1e-5))

    def loss(p):
        pred = (model_fn(p, phi, lam) if params_form == 'lambda'
                else model_fn(p, phi))
        log_pred = np.log10(np.maximum(pred, 1e-5))
        return float(np.sqrt(np.mean((log_pred - log_sigma) ** 2)))

    res = differential_evolution(loss, bounds, seed=42, maxiter=500,
                                  popsize=40, tol=1e-8, polish=True)
    pred = (model_fn(res.x, phi, lam) if params_form == 'lambda'
            else model_fn(res.x, phi))
    log_pred = np.log10(np.maximum(pred, 1e-5))
    log_m = np.log10(np.maximum(sigma, 1e-5))
    R2 = 1 - np.sum((log_pred - log_m)**2) / np.sum((log_m - log_m.mean())**2)
    return {'params': res.x, 'rmse_log': loss(res.x), 'R2_log': R2,
            'n_used': len(data_use)}


def main():
    print('Loading data …')
    data = load_data()
    n = len(data)
    n_out = sum(1 for d in data if d['is_outlier'])
    print(f'  Loaded {n} cases  ({n_out} outliers below σ < {OUTLIER_SIGMA_THRESHOLD} mS/cm)')

    # By class
    classes = ['mono AM_P', 'bimodal', 'mono AM_S']
    by_class = {c: [d for d in data if d['composition'] == c] for c in classes}
    by_class_clean = {c: [d for d in by_class[c] if not d['is_outlier']]
                       for c in classes}

    print()
    print('─' * 70)
    print('Per-class case count:')
    for c in classes:
        print(f'  {c:<12s}  n={len(by_class[c]):>3}  '
              f'(clean: {len(by_class_clean[c])})')

    # ── Fit 1: Global (no outliers), additive λ ────────────────────────
    print('\nFit 1: Global Kirkpatrick (additive λ, no outliers) ...')
    fit_global = fit_model(data, kirkpatrick_add,
                            bounds=[(1.0, 100.0), (0.05, 0.35), (0.0, 0.20),
                                    (0.1, 2.0), (1.0, 3.5)],
                            params_form='lambda', use_outlier=False)
    s0, phic, A, alpha, t = fit_global['params']
    print(f'   σ₀={s0:.2f}, φc_inf={phic:.4f}, A={A:.4f}, α={alpha:.2f}, '
          f't={t:.2f}, R²(log)={fit_global["R2_log"]:.3f}, '
          f'RMSE={fit_global["rmse_log"]:.3f}')

    # ── Fit 2: Multiplicative λ form ───────────────────────────────────
    print('\nFit 2: Kirkpatrick multiplicative λ (B1) ...')
    fit_mul = fit_model(data, kirkpatrick_mul,
                         bounds=[(1.0, 100.0), (0.05, 0.40), (0.0, 5.0),
                                 (1.0, 3.5)],
                         params_form='lambda', use_outlier=False)
    s0, phic, B, t = fit_mul['params']
    print(f'   σ₀={s0:.2f}, φc_inf={phic:.4f}, B={B:.3f}, t={t:.2f}, '
          f'R²(log)={fit_mul["R2_log"]:.3f}, RMSE={fit_mul["rmse_log"]:.3f}')

    # ── Fit 3: Bruggeman σ = σ_grain × φ^n (B4 baseline) ──────────────
    print('\nFit 3: Bruggeman σ = σ_grain × φ^n (no threshold) ...')
    fit_brug = fit_model(data, bruggeman,
                          bounds=[(0.5, 100.0), (0.5, 5.0)],
                          params_form='no_lambda', use_outlier=False)
    sg, n_b = fit_brug['params']
    print(f'   σ_grain={sg:.2f}, n={n_b:.2f}, '
          f'R²(log)={fit_brug["R2_log"]:.3f}, RMSE={fit_brug["rmse_log"]:.3f}')

    # ── Fit 4: Per-class Kirkpatrick (additive, only need t + σ_0 + φc) ─
    print('\nFit 4: Per-class Kirkpatrick (φc not λ-dependent within class) ...')
    fit_class = {}
    for c in classes:
        d_c = by_class_clean[c]
        if len(d_c) < 4:
            print(f'   {c}: n={len(d_c)} too few, skip')
            continue
        # Inside class, lam variation can still be present — keep λ but
        # use simpler model: 4 params (σ_0, φc_inf, A, t) with α=1 fixed
        bounds = [(1.0, 100.0), (0.05, 0.40), (0.0, 0.25), (1.0, 3.5)]
        def model_class(p, phi, lam):
            sigma_0, phi_c_inf, A, t = p
            phi_c = phi_c_inf - A / np.clip(lam, 0.1, None)
            delta = np.maximum(0, phi - phi_c)
            return sigma_0 * np.power(delta, t)
        fit_class[c] = fit_model(d_c, model_class, bounds,
                                  params_form='lambda', use_outlier=False)
        s0, phic, A, t = fit_class[c]['params']
        print(f'   {c:<12s} σ₀={s0:.2f}, φc_inf={phic:.3f}, A={A:.4f}, '
              f't={t:.2f}, R²={fit_class[c]["R2_log"]:.3f}, '
              f'n={fit_class[c]["n_used"]}')

    # ── Summary table ─────────────────────────────────────────────────
    print()
    print('─' * 70)
    print('MODEL COMPARISON (log-space R²)')
    print('─' * 70)
    print(f'  {"Model":<35s} {"n":>4} {"R²(log)":>9} {"RMSE":>7}')
    print(f'  {"Kirkpatrick add. λ (Fit 1)":<35s} {fit_global["n_used"]:>4} '
          f'{fit_global["R2_log"]:>9.3f} {fit_global["rmse_log"]:>7.3f}')
    print(f'  {"Kirkpatrick mul. λ (Fit 2 — B1)":<35s} {fit_mul["n_used"]:>4} '
          f'{fit_mul["R2_log"]:>9.3f} {fit_mul["rmse_log"]:>7.3f}')
    print(f'  {"Bruggeman σ = σ_grain × φ^n (B4)":<35s} {fit_brug["n_used"]:>4} '
          f'{fit_brug["R2_log"]:>9.3f} {fit_brug["rmse_log"]:>7.3f}')
    for c in classes:
        if c in fit_class:
            fc = fit_class[c]
            print(f'  Per-class: {c:<24s} {fc["n_used"]:>4} '
                  f'{fc["R2_log"]:>9.3f} {fc["rmse_log"]:>7.3f}')

    # ── Build figure ───────────────────────────────────────────────────
    composition_colors = {'mono AM_P': '#dc2626', 'bimodal': '#10b981',
                           'mono AM_S': '#2563eb'}

    fig = plt.figure(figsize=(15, 12))
    gs = fig.add_gridspec(2, 2, hspace=0.35, wspace=0.30)

    # Panel A: 3 separate class fits overlaid
    ax = fig.add_subplot(gs[0, 0])
    for d in data:
        col = composition_colors.get(d['composition'], '#888')
        marker = 'x' if d['is_outlier'] else 'o'
        ax.scatter(d['phi_SE'], d['sigma_ionic_mScm'],
                    color=col, alpha=0.7, s=45 if not d['is_outlier'] else 80,
                    marker=marker, edgecolor='black', linewidth=0.5,
                    label=None)
    # Plot class-specific fit curves
    for c, fc in fit_class.items():
        s0, phic, A, t = fc['params']
        lam_med = np.median([d['lam_eff'] for d in by_class_clean[c]])
        phi_g = np.linspace(0.05, 0.55, 200)
        phi_c_eff = phic - A / max(lam_med, 0.1)
        delta = np.maximum(0, phi_g - phi_c_eff)
        sigma_g = s0 * np.power(delta, t)
        col = composition_colors[c]
        ax.plot(phi_g, sigma_g, '-', color=col, linewidth=2.5,
                 label=f'{c}: φc={phi_c_eff:.3f}, t={t:.2f} (n={fc["n_used"]})')
    ax.axvline(1/3, linestyle=':', color='gray', linewidth=1, alpha=0.6)
    ax.text(1/3+0.005, 5e-4, 'Bruggeman φc=1/3', rotation=90,
            ha='left', va='bottom', fontsize=8, color='gray')
    ax.set_xlabel('φ_SE', fontsize=11)
    ax.set_ylabel('σ_ionic  (mS/cm)', fontsize=11)
    ax.set_yscale('log')
    ax.set_title('Per-class Kirkpatrick fits — distinct φc, t per composition',
                  fontsize=11)
    ax.legend(loc='lower right', fontsize=8.5)
    ax.set_xlim(0, 0.65); ax.set_ylim(2e-4, 2)
    ax.grid(alpha=0.3, which='both')

    # Panel B: Comparison of 4 models on parity plot
    ax = fig.add_subplot(gs[0, 1])
    phi_arr   = np.array([d['phi_SE']           for d in data])
    lam_arr   = np.array([d['lam_eff']          for d in data])
    sigma_arr = np.array([d['sigma_ionic_mScm'] for d in data])
    outlier_mask = np.array([d['is_outlier'] for d in data])

    pred_global = kirkpatrick_add(fit_global['params'], phi_arr, lam_arr)
    pred_mul    = kirkpatrick_mul(fit_mul['params'], phi_arr, lam_arr)
    pred_brug   = bruggeman(fit_brug['params'], phi_arr)

    # Per-class prediction
    pred_class = np.zeros_like(sigma_arr)
    for i, d in enumerate(data):
        c = d['composition']
        if c in fit_class:
            s0, phic, A, t = fit_class[c]['params']
            phi_c_eff = phic - A / max(d['lam_eff'], 0.1)
            delta = max(0, d['phi_SE'] - phi_c_eff)
            pred_class[i] = s0 * (delta ** t)
        else:
            pred_class[i] = np.nan

    ax.scatter(sigma_arr[~outlier_mask], pred_global[~outlier_mask],
                s=35, c='#6b7280', alpha=0.5, marker='o',
                label=f'Global add (R²={fit_global["R2_log"]:.2f})')
    ax.scatter(sigma_arr[~outlier_mask], pred_mul[~outlier_mask],
                s=35, c='#9333ea', alpha=0.5, marker='^',
                label=f'Global mul (R²={fit_mul["R2_log"]:.2f})')
    ax.scatter(sigma_arr[~outlier_mask], pred_brug[~outlier_mask],
                s=35, c='#0891b2', alpha=0.5, marker='s',
                label=f'Bruggeman (R²={fit_brug["R2_log"]:.2f})')
    finite = ~np.isnan(pred_class) & ~outlier_mask
    R2_class_all = 1 - np.sum((np.log10(np.maximum(pred_class[finite], 1e-5))
                                 - np.log10(np.maximum(sigma_arr[finite], 1e-5)))**2) \
                    / np.sum((np.log10(np.maximum(sigma_arr[finite], 1e-5))
                                - np.log10(np.maximum(sigma_arr[finite], 1e-5)).mean())**2)
    ax.scatter(sigma_arr[finite], pred_class[finite],
                s=45, c='#dc2626', alpha=0.8, marker='*',
                label=f'Per-class (R²={R2_class_all:.2f})')
    ax.scatter(sigma_arr[outlier_mask], pred_global[outlier_mask],
                s=80, marker='x', c='red', label='outlier (σ<0.003)')
    lo, hi = 1e-4, 1
    ax.plot([lo, hi], [lo, hi], 'k--', linewidth=1, alpha=0.5)
    ax.set_xscale('log'); ax.set_yscale('log')
    ax.set_xlabel('measured σ_ionic (mS/cm)', fontsize=11)
    ax.set_ylabel('predicted σ_ionic (mS/cm)', fontsize=11)
    ax.set_title('4-way model comparison — parity plot', fontsize=11)
    ax.legend(loc='upper left', fontsize=8.5)
    ax.set_xlim(lo, hi); ax.set_ylim(lo, hi)
    ax.grid(alpha=0.3, which='both')

    # Panel C: R² + threshold (φc) bar chart
    ax = fig.add_subplot(gs[1, 0])
    names = ['Global\nadd. λ', 'Global\nmul. λ', 'Bruggeman\n(no φc)']
    R2_list = [fit_global['R2_log'], fit_mul['R2_log'], fit_brug['R2_log']]
    colors = ['#6b7280', '#9333ea', '#0891b2']
    bars1 = ax.bar(np.arange(len(names)), R2_list, color=colors, width=0.5,
                    label='Global models')
    # per-class
    x_offset = len(names)
    for i, c in enumerate(classes):
        if c in fit_class:
            ax.bar(x_offset + i, fit_class[c]['R2_log'],
                    color=composition_colors[c], width=0.5)
    names_all = names + [c.replace(' ', '\n') for c in classes if c in fit_class]
    ax.set_xticks(np.arange(len(names_all)))
    ax.set_xticklabels(names_all, fontsize=9)
    ax.set_ylabel('R² (log₁₀ σ)', fontsize=11)
    ax.set_title('Model comparison — log-space R²', fontsize=11)
    ax.set_ylim(0, 1)
    ax.grid(axis='y', alpha=0.3)
    for i, v in enumerate(R2_list):
        ax.text(i, v + 0.02, f'{v:.2f}', ha='center', va='bottom', fontsize=9)
    for i, c in enumerate(classes):
        if c in fit_class:
            ax.text(x_offset + i, fit_class[c]['R2_log'] + 0.02,
                    f'{fit_class[c]["R2_log"]:.2f}',
                    ha='center', va='bottom', fontsize=9)

    # Panel D: φc threshold comparison
    ax = fig.add_subplot(gs[1, 1])
    threshold_data = []
    s0_g, phic_g, A_g, alpha_g, t_g = fit_global['params']
    threshold_data.append(('Global add.', phic_g, t_g, '#6b7280'))
    s0_m, phic_m, B_m, t_m = fit_mul['params']
    threshold_data.append(('Global mul.', phic_m, t_m, '#9333ea'))
    threshold_data.append(('Bruggeman', 0.0, fit_brug['params'][1], '#0891b2'))
    for c in classes:
        if c in fit_class:
            s0_c, phic_c, A_c, t_c = fit_class[c]['params']
            threshold_data.append((c, phic_c, t_c, composition_colors[c]))

    # bar chart: φc on left axis, t on right
    x = np.arange(len(threshold_data))
    phicv = [d[1] for d in threshold_data]
    tv = [d[2] for d in threshold_data]
    cols = [d[3] for d in threshold_data]
    labels = [d[0] for d in threshold_data]

    bars = ax.bar(x - 0.2, phicv, width=0.35, color=cols, alpha=0.85,
                   label='φc_inf')
    ax.axhline(1/3, linestyle='--', color='gray', linewidth=1, alpha=0.6)
    ax.text(len(threshold_data)-0.5, 1/3+0.005, 'Bruggeman 1/3',
             ha='right', va='bottom', fontsize=8, color='gray')
    ax.set_xticks(x)
    ax.set_xticklabels([l.replace(' ', '\n') for l in labels], fontsize=8)
    ax.set_ylabel('φc_inf', fontsize=11)
    ax.set_title('Threshold φc + scaling exponent t per model', fontsize=11)
    ax.set_ylim(0, 0.45)
    ax2 = ax.twinx()
    ax2.bar(x + 0.2, tv, width=0.35, color=cols, alpha=0.45, hatch='//')
    ax2.set_ylabel('exponent t', fontsize=11)
    ax2.axhline(2.0, linestyle=':', color='black', linewidth=1, alpha=0.6)
    ax2.text(len(threshold_data)-0.5, 2.05, 'Kirkpatrick t=2',
              ha='right', va='bottom', fontsize=8)
    ax2.set_ylim(0, 3.5)
    for i, (p, tt) in enumerate(zip(phicv, tv)):
        ax.text(i - 0.2, p + 0.005, f'{p:.2f}', ha='center', va='bottom',
                fontsize=8)
        ax2.text(i + 0.2, tt + 0.05, f'{tt:.2f}', ha='center', va='bottom',
                  fontsize=8)
    ax.grid(axis='y', alpha=0.3)

    fig.suptitle('SE percolation 2D scaling — v2 multi-model comparison '
                  '(outliers removed, per-class fits)   [Phase C1 v2]',
                  fontsize=12, fontweight='bold', y=0.995)

    out_png = ROOT / 'docs' / 'figures' / 'percolation_2d_fit_v2.png'
    out_png.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_png, dpi=130, bbox_inches='tight')
    plt.close(fig)
    print(f'\nFigure → {out_png}')

    # ── CSV: per-case + predictions ──────────────────────────────────
    out_csv = ROOT / 'docs' / 'data' / 'percolation_2d_fit_v2.csv'
    rows = []
    for i, d in enumerate(data):
        rows.append({
            **d,
            'pred_global_add':  round(float(pred_global[i]), 5),
            'pred_global_mul':  round(float(pred_mul[i]), 5),
            'pred_bruggeman':   round(float(pred_brug[i]), 5),
            'pred_class':       round(float(pred_class[i]), 5) if not np.isnan(pred_class[i]) else None,
        })
    keys = list(rows[0].keys())
    with open(out_csv, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader(); w.writerows(rows)
    print(f'CSV    → {out_csv}')


if __name__ == '__main__':
    main()
