#!/usr/bin/env python3
"""Validate strict physics-first porosity model against ALL DEM cases.

Reads all_dem_porosity.csv (82 cases across 4 campaigns), computes the
strict physics prediction PER CASE (using each case's actual particle
diameters, not hard-coded defaults), then plots:

  Left panel : measured vs predicted scatter (1:1 line, ±2% bands)
  Right panel: residual histogram + per-campaign summary

NOTE on CSV units: r_*_um columns in the collector output are 1000x the
physical µm (collector multiplies by 1e6 then divides by scale=1000,
which is OK for input_params 'm' values but full_metrics stores them
already in physical units). We divide by 1000 here for true µm.
"""
import csv
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sys

sys.path.insert(0, str(Path(__file__).parent))
from predict_porosity_strict_physics import (
    RHO_AM, RHO_SE, EPS_PURE_AM, K_HECKEL, P_PRESS,
    ALPHA_KC, F_PERC, SHARPNESS, bouvard_rcp,
)


def stress_percolation(f_se):
    return 1.0 / (1.0 + np.exp(-SHARPNESS * (f_se - F_PERC)))


def sfm_constraint(f_am, lam_eff):
    if f_am <= 1e-9:
        return 1.0
    kc = 1.0 + ALPHA_KC * f_am ** 2
    kc *= 1.0 + 0.05 * np.log(max(lam_eff, 1.0))
    return kc


def predict_case(am_wt, se_wt, d_am_p, n_p, d_am_s, n_s, d_se):
    """Predict porosity from case-specific particle data."""
    # Volume fractions from mass fractions (am_wt + se_wt = 100)
    v_am = am_wt / RHO_AM
    v_se = se_wt / RHO_SE
    f_am_tot = v_am / (v_am + v_se)
    f_se     = v_se / (v_am + v_se)

    # Within AM, partition P/S by VOLUME from particle counts × r³
    if n_p and n_s:
        vol_p = n_p * (d_am_p / 2.0) ** 3
        vol_s = n_s * (d_am_s / 2.0) ** 3
        frac_p_in_am = vol_p / (vol_p + vol_s)
    elif n_p:
        frac_p_in_am = 1.0
    elif n_s:
        frac_p_in_am = 0.0
    else:
        frac_p_in_am = 0.0

    f_p = f_am_tot * frac_p_in_am
    f_s = f_am_tot * (1.0 - frac_p_in_am)

    # Effective AM diameter
    if d_am_p and d_am_s and n_p and n_s:
        d_eff_am = frac_p_in_am * d_am_p + (1 - frac_p_in_am) * d_am_s
    elif d_am_p and n_p:
        d_eff_am = d_am_p
    elif d_am_s and n_s:
        d_eff_am = d_am_s
    else:
        d_eff_am = 4.0  # fallback
    lam_eff = d_eff_am / d_se

    eps_rcp = bouvard_rcp(f_se, lam_eff)
    kc      = sfm_constraint(f_am_tot, lam_eff)
    p_se    = stress_percolation(f_se)

    P_eff = P_PRESS / kc
    eps_pure_at_Peff = EPS_PURE_AM * np.exp(-K_HECKEL * P_eff / 1e6)
    delta_max = EPS_PURE_AM - eps_pure_at_Peff
    delta = delta_max * f_se * p_se
    eps_pred = max(eps_rcp - delta, 0.03)

    return dict(f_se=f_se, lam_eff=lam_eff, d_eff_am=d_eff_am,
                eps_rcp=eps_rcp, eps_pred=eps_pred,
                kc=kc, p_se=p_se)


def fnum(s):
    try:
        return float(s)
    except (ValueError, TypeError):
        return None


def main():
    csv_path = Path('all_dem_porosity.csv')
    rows = list(csv.DictReader(csv_path.open()))
    print(f'Loaded {len(rows)} cases')

    results = []
    for r in rows:
        am_wt = fnum(r['am_wt']); se_wt = fnum(r['se_wt'])
        if am_wt is None or se_wt is None:
            continue
        # Divide by 1000 → physical µm (collector output is 1000× too large)
        d_am_p = (fnum(r['r_AM_P_um']) or 0) * 2 / 1000
        d_am_s = (fnum(r['r_AM_S_um']) or 0) * 2 / 1000
        d_se   = (fnum(r['r_SE_um'])   or 0) * 2 / 1000
        n_p    = fnum(r['n_AM_P']) or 0
        n_s    = fnum(r['n_AM_S']) or 0
        meas   = fnum(r['porosity_pct'])
        if not meas or d_se <= 0:
            continue
        pred = predict_case(am_wt, se_wt, d_am_p, n_p,
                            d_am_s, n_s, d_se)
        results.append({
            **r, 'd_eff_am': pred['d_eff_am'], 'd_se': d_se,
            'lam_eff': pred['lam_eff'], 'f_se': pred['f_se'],
            'eps_meas': meas, 'eps_pred': pred['eps_pred'] * 100,
            'residual': meas - pred['eps_pred'] * 100,
        })
    print(f'Predicted {len(results)} cases')

    # ── Print summary table ──
    print()
    hdr = f'{"case_id":>26s} {"campaign":>14s} {"AM:SE":>7s} {"P:S":>6s} ' \
          f'{"f_se":>6s} {"λ":>5s} {"meas":>7s} {"pred":>7s} {"Δ":>7s}'
    print(hdr)
    print('─' * len(hdr))
    for r in results:
        ps = f"{int(fnum(r['p_vol']))}:{int(fnum(r['s_vol']))}" \
            if r['p_vol'] else '0:10'
        print(f"{r['case_id']:>26s} {r['campaign']:>14s} "
              f"{int(fnum(r['am_wt']))}:{int(fnum(r['se_wt'])):<2d}     "
              f"{ps:>6s} {r['f_se']*100:5.1f}% {r['lam_eff']:5.1f} "
              f"{r['eps_meas']:6.2f}% {r['eps_pred']:6.2f}% "
              f"{r['residual']:+6.2f}%")

    # Stats
    residuals = np.array([r['residual'] for r in results])
    print()
    print(f'Residual (measured − predicted) statistics:')
    print(f'  mean   = {residuals.mean():+.2f}%')
    print(f'  std    = {residuals.std():.2f}%')
    print(f'  median = {np.median(residuals):+.2f}%')
    print(f'  |Δ|<2% : {(np.abs(residuals)<2).sum()}/{len(residuals)} '
          f'({100*(np.abs(residuals)<2).mean():.0f}%)')
    print(f'  |Δ|<3% : {(np.abs(residuals)<3).sum()}/{len(residuals)} '
          f'({100*(np.abs(residuals)<3).mean():.0f}%)')
    print(f'  |Δ|<5% : {(np.abs(residuals)<5).sum()}/{len(residuals)} '
          f'({100*(np.abs(residuals)<5).mean():.0f}%)')

    # ── Plot ──
    fig, axes = plt.subplots(1, 2, figsize=(15, 6.5))

    # Panel 1: measured vs predicted scatter
    ax = axes[0]
    campaigns = sorted({r['campaign'] for r in results})
    label_en = {'particulate': 'particulate',
                '박막(1mAh)': 'thin film (1 mAh)',
                '후막(6mAh)': 'thick film (6 mAh)',
                '후막(8mAh)': 'thick film (8 mAh)'}
    cmap = {'particulate': 'tab:blue',
            '박막(1mAh)': 'tab:green',
            '후막(6mAh)': 'tab:orange',
            '후막(8mAh)': 'tab:red'}
    markers = {'particulate': 'o', '박막(1mAh)': 's',
               '후막(6mAh)': '^', '후막(8mAh)': 'D'}

    for camp in campaigns:
        sub = [r for r in results if r['campaign'] == camp]
        xs = [r['eps_pred'] for r in sub]
        ys = [r['eps_meas'] for r in sub]
        ax.scatter(xs, ys, s=60, color=cmap.get(camp, 'gray'),
                   marker=markers.get(camp, 'o'),
                   alpha=0.75, edgecolors='black', linewidth=0.5,
                   label=f'{label_en.get(camp, camp)}  (n={len(sub)})')

    # 1:1 line and ±2/3% bands
    lo, hi = 0, 40
    ax.plot([lo, hi], [lo, hi], 'k-', lw=1.5, label='1:1', zorder=1)
    ax.fill_between([lo, hi], [lo-2, hi-2], [lo+2, hi+2],
                    color='gray', alpha=0.15, label='±2%')
    ax.fill_between([lo, hi], [lo-3, hi-3], [lo+3, hi+3],
                    color='gray', alpha=0.10)

    ax.set_xlabel('Predicted ε (strict physics, %)', fontsize=12)
    ax.set_ylabel('Measured ε (DEM, %)', fontsize=12)
    ax.set_title(f'Strict physics-first vs DEM, N={len(results)} cases\n'
                 f'|Δ|<2% in {100*(np.abs(residuals)<2).mean():.0f}%, '
                 f'|Δ|<3% in {100*(np.abs(residuals)<3).mean():.0f}%', fontsize=11)
    ax.set_xlim(lo, hi); ax.set_ylim(lo, hi)
    ax.legend(fontsize=9, loc='upper left')
    ax.grid(alpha=0.3)

    # Panel 2: residual histogram
    ax = axes[1]
    ax.hist(residuals, bins=20, color='steelblue',
            edgecolor='black', alpha=0.75)
    ax.axvline(0, color='k', lw=1.5)
    ax.axvline(residuals.mean(), color='crimson', lw=2,
               label=f'mean = {residuals.mean():+.2f}%')
    ax.axvline(residuals.mean()-residuals.std(), color='crimson',
               lw=1, ls='--')
    ax.axvline(residuals.mean()+residuals.std(), color='crimson',
               lw=1, ls='--', label=f'±σ = {residuals.std():.2f}%')
    ax.set_xlabel('Residual: measured − predicted (%)', fontsize=12)
    ax.set_ylabel('Count', fontsize=12)
    ax.set_title('Residual distribution (all 82 DEM cases)\n'
                 f'σ = {residuals.std():.2f}%; positive = DEM higher than physics',
                 fontsize=11)
    ax.legend(fontsize=10)
    ax.grid(alpha=0.3)

    plt.tight_layout()
    out = Path('validation_all_cases.png')
    plt.savefig(out, dpi=150, bbox_inches='tight')
    print(f'\n✓ Saved: {out.resolve()}')

    # Also dump per-case predictions to CSV
    out_csv = Path('validation_all_cases.csv')
    with out_csv.open('w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['case_id', 'campaign', 'am_wt', 'se_wt',
                    'd_eff_am_um', 'd_se_um', 'lam_eff', 'f_se',
                    'eps_meas', 'eps_pred', 'residual'])
        for r in results:
            w.writerow([r['case_id'], r['campaign'],
                        r['am_wt'], r['se_wt'],
                        f"{r['d_eff_am']:.2f}", f"{r['d_se']:.2f}",
                        f"{r['lam_eff']:.2f}", f"{r['f_se']:.3f}",
                        f"{r['eps_meas']:.2f}",
                        f"{r['eps_pred']:.2f}",
                        f"{r['residual']:+.2f}"])
    print(f'✓ Saved: {out_csv.resolve()}')


if __name__ == '__main__':
    main()
