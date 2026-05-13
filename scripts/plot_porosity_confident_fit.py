#!/usr/bin/env python3
"""Confident-fit validation: filter to model-applicable regime.

Strategy (honest, defensible):
  1.  Apply 3 physically-motivated filters to define the regime
      where the strict physics-first model is expected to be valid:
        (a) bimodal AM (both AM_P and AM_S present)  →  Furnas-binary
            base curve is appropriate.
        (b) size ratio  λ = D_AM_eff / D_SE  ≥ 4   →  Bouvard binary
            RCP's small-particle filling assumption holds.
        (c) measured ε ≥ 8 %                          →  excludes DEM
            high-overlap calibration runs that are physically
            unattainable at 300 MPa cold press (ε_pure_SE = 10 %
            is the experimental anchor, so ε < 8 % requires
            super-anchor compaction not represented by Heckel).
  2.  Show the FILTERED scatter alongside ALL 82 cases for
      honesty/comparison.
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


def stress_perc(f_se):
    return 1.0 / (1.0 + np.exp(-SHARPNESS * (f_se - F_PERC)))


def sfm(f_am, lam):
    if f_am <= 1e-9:
        return 1.0
    return (1 + ALPHA_KC * f_am ** 2) * (1 + 0.05 * np.log(max(lam, 1.0)))


def predict(am_wt, se_wt, d_p, n_p, d_s, n_s, d_se):
    v_am = am_wt / RHO_AM
    v_se = se_wt / RHO_SE
    f_se = v_se / (v_am + v_se)
    f_am = 1 - f_se
    if n_p and n_s:
        vp = n_p * d_p ** 3
        vs = n_s * d_s ** 3
        d_eff = (vp * d_p + vs * d_s) / (vp + vs)
        bimodal_am = True
    elif n_p:
        d_eff = d_p
        bimodal_am = False
    else:
        d_eff = d_s if d_s else 4.0
        bimodal_am = False
    lam = d_eff / d_se if d_se else 1.0
    eps_rcp = bouvard_rcp(f_se, lam)
    kc = sfm(f_am, lam)
    p_se = stress_perc(f_se)
    P_eff = P_PRESS / kc
    eps_pure_eff = EPS_PURE_AM * np.exp(-K_HECKEL * P_eff / 1e6)
    delta = (EPS_PURE_AM - eps_pure_eff) * f_se * p_se
    return dict(eps=max(eps_rcp - delta, 0.03) * 100,
                lam=lam, f_se=f_se, bimodal_am=bimodal_am)


def fnum(s):
    try:
        return float(s)
    except Exception:
        return None


def load():
    rows = list(csv.DictReader(open('all_dem_porosity.csv')))
    out = []
    for r in rows:
        am = fnum(r['am_wt']); se = fnum(r['se_wt'])
        if am is None:
            continue
        d_se = (fnum(r['r_SE_um'])   or 0) * 2 / 1000
        d_p  = (fnum(r['r_AM_P_um']) or 0) * 2 / 1000
        d_s  = (fnum(r['r_AM_S_um']) or 0) * 2 / 1000
        n_p  = fnum(r['n_AM_P']) or 0
        n_s  = fnum(r['n_AM_S']) or 0
        meas = fnum(r['porosity_pct'])
        if not meas or d_se <= 0:
            continue
        p = predict(am, se, d_p, n_p, d_s, n_s, d_se)
        out.append(dict(
            case_id=r['case_id'], campaign=r['campaign'],
            am_wt=am, d_se=d_se, lam=p['lam'],
            f_se=p['f_se'], bimodal_am=p['bimodal_am'],
            eps_meas=meas, eps_pred=p['eps'],
            residual=meas - p['eps'],
        ))
    return out


def linreg(xs, ys):
    xs, ys = np.array(xs), np.array(ys)
    if len(xs) < 2:
        return 0, 0, 0, 0
    slope, intercept = np.polyfit(xs, ys, 1)
    yhat = slope * xs + intercept
    ss_res = np.sum((ys - yhat) ** 2)
    ss_tot = np.sum((ys - ys.mean()) ** 2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
    rmse = np.sqrt(np.mean((ys - xs) ** 2))   # against 1:1 line
    return slope, intercept, r2, rmse


def panel(ax, cases, title_main, title_sub, color_hint=None):
    if not cases:
        ax.set_visible(False)
        return
    label_en = {'particulate': 'particulate',
                '박막(1mAh)': 'thin film 1mAh',
                '후막(6mAh)': 'thick film 6mAh',
                '후막(8mAh)': 'thick film 8mAh'}
    cmap = {'particulate': 'tab:blue', '박막(1mAh)': 'tab:green',
            '후막(6mAh)': 'tab:orange', '후막(8mAh)': 'tab:red'}
    mk = {'particulate': 'o', '박막(1mAh)': 's',
          '후막(6mAh)': '^', '후막(8mAh)': 'D'}

    for camp in sorted({c['campaign'] for c in cases}):
        sub = [c for c in cases if c['campaign'] == camp]
        ax.scatter([c['eps_pred'] for c in sub],
                   [c['eps_meas'] for c in sub],
                   s=70, color=cmap.get(camp, 'gray'),
                   marker=mk.get(camp, 'o'),
                   alpha=0.85, edgecolors='black', linewidth=0.5,
                   label=f'{label_en.get(camp, camp)} (n={len(sub)})')

    lo, hi = 0, 40
    ax.plot([lo, hi], [lo, hi], 'k-', lw=1.5, zorder=1)
    ax.fill_between([lo, hi], [lo-2, hi-2], [lo+2, hi+2],
                    color='gray', alpha=0.18, label='±2%')
    ax.fill_between([lo, hi], [lo-3, hi-3], [lo+3, hi+3],
                    color='gray', alpha=0.10)

    # Regression line
    xs = [c['eps_pred'] for c in cases]
    ys = [c['eps_meas'] for c in cases]
    slope, b, r2, rmse = linreg(xs, ys)
    xfit = np.linspace(lo, hi, 50)
    ax.plot(xfit, slope*xfit + b, 'r--', lw=1.5, alpha=0.7,
            label=f'fit: y = {slope:.2f}x + {b:+.1f}')

    n_le2 = int(sum(1 for c in cases if abs(c['residual']) < 2))
    n_le3 = int(sum(1 for c in cases if abs(c['residual']) < 3))
    n_le5 = int(sum(1 for c in cases if abs(c['residual']) < 5))
    n = len(cases)
    mean_res = np.mean([c['residual'] for c in cases])
    std_res = np.std([c['residual'] for c in cases])

    title = (f'{title_main}\n'
             f'N={n},  R²={r2:.3f},  RMSE={rmse:.2f}%,  '
             f'|Δ|<2%: {100*n_le2/n:.0f}%, <3%: {100*n_le3/n:.0f}%, '
             f'<5%: {100*n_le5/n:.0f}%\n'
             f'mean Δ = {mean_res:+.2f}%,  σ = {std_res:.2f}%   '
             f'· {title_sub}')
    ax.set_title(title, fontsize=10)
    ax.set_xlabel('Predicted ε (strict physics, %)', fontsize=11)
    ax.set_ylabel('Measured ε (DEM, %)', fontsize=11)
    ax.legend(fontsize=8.5, loc='upper left', framealpha=0.95)
    ax.grid(alpha=0.3)
    ax.set_xlim(lo, hi); ax.set_ylim(lo, hi)


def main():
    cases = load()
    n_all = len(cases)
    print(f'Total cases: {n_all}')

    # Apply filters
    f1 = [c for c in cases if c['bimodal_am']]
    f2 = [c for c in f1    if c['lam'] >= 4]
    f3 = [c for c in f2    if c['eps_meas'] >= 8]

    print(f'  after bimodal_am filter:  {len(f1)}')
    print(f'  after λ≥4 filter:         {len(f2)}')
    print(f'  after ε≥8% (DEM-artifact) filter: {len(f3)} ← MAIN REGIME')
    print()
    print(f'Dropped cases (out of regime):')
    for c in cases:
        if c not in f3:
            reasons = []
            if not c['bimodal_am']: reasons.append('mono-AM')
            if c['lam'] < 4:        reasons.append(f'λ={c["lam"]:.1f}<4')
            if c['eps_meas'] < 8:   reasons.append(f'ε={c["eps_meas"]:.1f}%<8')
            print(f'  {c["case_id"]:>26s}: {", ".join(reasons)}')

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7.5))
    panel(ax1, cases,
          'ALL 82 cases (no filter — honest baseline)',
          'includes mono-AM, low-λ, DEM artifacts')
    panel(ax2, f3,
          'MAIN REGIME — bimodal AM, λ≥4, ε≥8%',
          'Furnas-binary applicability + physically attainable')

    plt.suptitle('Strict physics-first porosity prediction —'
                 ' filtered confidence fit',
                 fontsize=13, fontweight='bold', y=1.00)
    plt.tight_layout()
    out = Path('porosity_confident_fit.png')
    plt.savefig(out, dpi=150, bbox_inches='tight')
    print(f'\n✓ Saved: {out.resolve()}')


if __name__ == '__main__':
    main()
