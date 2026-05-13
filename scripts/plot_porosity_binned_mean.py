#!/usr/bin/env python3
"""Honest binned-mean validation plot.

The case-by-case strict-physics prediction has narrow range (17-22%)
while measured DEM porosity spans 10-25% within the main regime, so
the R² is poor in a scatter plot — predictions can't resolve case-
to-case variation.  But the MEAN per composition bin is well captured
(mean Δ < 2% across regime), which is what a mean-field model is
expected to do.

This plot:
  - bins cases by AM wt% (5% width)
  - shows mean ± σ of measured ε per bin (error bars)
  - overlays the strict-physics prediction curve (default 12+4+1)
  - separately for each campaign with bimodal AM in main regime

If the prediction line lies within ±1σ of every binned mean →
"the model captures the central trend within experimental scatter."
This is the defensible, physics-consistent confidence claim.
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
    ALPHA_KC, F_PERC, SHARPNESS, bouvard_rcp, predict_strict,
    EPS_PURE_SE_EXP,
)


def stress_perc(f_se):
    return 1.0 / (1.0 + np.exp(-SHARPNESS * (f_se - F_PERC)))


def sfm(f_am, lam):
    if f_am <= 1e-9:
        return 1.0
    return (1 + ALPHA_KC * f_am ** 2) * (1 + 0.05 * np.log(max(lam, 1.0)))


def predict_full(am_wt, se_wt, d_p, n_p, d_s, n_s, d_se):
    v_am = am_wt / RHO_AM
    v_se = se_wt / RHO_SE
    f_se = v_se / (v_am + v_se)
    f_am = 1 - f_se
    if n_p and n_s:
        vp = n_p * d_p ** 3
        vs = n_s * d_s ** 3
        d_eff = (vp * d_p + vs * d_s) / (vp + vs)
        bimodal = True
    elif n_p:
        d_eff = d_p
        bimodal = False
    else:
        d_eff = d_s if d_s else 4.0
        bimodal = False
    lam = d_eff / d_se if d_se else 1.0
    eps_rcp = bouvard_rcp(f_se, lam)
    kc = sfm(f_am, lam)
    p_se = stress_perc(f_se)
    P_eff = P_PRESS / kc
    eps_pure_eff = EPS_PURE_AM * np.exp(-K_HECKEL * P_eff / 1e6)
    delta = (EPS_PURE_AM - eps_pure_eff) * f_se * p_se
    return dict(eps=max(eps_rcp - delta, 0.03) * 100,
                lam=lam, bimodal=bimodal, f_se=f_se)


def fnum(s):
    try:    return float(s)
    except: return None


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
        p = predict_full(am, se, d_p, n_p, d_s, n_s, d_se)
        out.append(dict(
            case_id=r['case_id'], campaign=r['campaign'],
            am_wt=am, lam=p['lam'], bimodal=p['bimodal'],
            f_se=p['f_se'], eps_meas=meas, eps_pred=p['eps'],
        ))
    return out


def main():
    cases = load()
    # Main regime
    main_regime = [c for c in cases
                   if c['bimodal'] and c['lam'] >= 4 and c['eps_meas'] >= 8]
    print(f'Main regime: {len(main_regime)} cases')

    # Predict curve (default trimodal 12+4+1) for P:S = 7:3, 5:5, 3:7
    am_arr = np.linspace(60, 95, 100)
    curves = {}
    for ps in [(7, 3), (5, 5), (3, 7)]:
        ys = [predict_strict((am, 100-am), ps)['eps_pred'] * 100
              for am in am_arr]
        curves[ps] = ys

    # ── Bin by AM wt% (5% wide bins, centered) ────────────────────
    bin_edges = np.arange(60, 100, 5)
    bin_centers = bin_edges[:-1] + 2.5

    fig, axes = plt.subplots(1, 2, figsize=(16, 7))

    # ── PANEL 1: per-AM-bin mean ± σ vs strict physics curve ─────
    ax = axes[0]
    for ps, color in [((7, 3), 'crimson'),
                       ((5, 5), 'tab:green'),
                       ((3, 7), 'tab:blue')]:
        ax.plot(am_arr, curves[ps], '-', color=color, lw=2.5,
                label=f'strict physics  P:S={ps[0]}:{ps[1]}')

    # Anchors
    ax.scatter([0, 100], [EPS_PURE_SE_EXP*100, EPS_PURE_AM*100],
               s=200, marker='s', color='darkgreen',
               edgecolors='black', linewidth=1.5, zorder=12,
               label='anchors')

    # Compute bin mean ± std using main-regime cases
    bin_data = []
    for lo, hi in zip(bin_edges[:-1], bin_edges[1:]):
        bin_cases = [c for c in main_regime if lo <= c['am_wt'] < hi]
        if len(bin_cases) >= 2:
            eps_arr = np.array([c['eps_meas'] for c in bin_cases])
            pred_arr = np.array([c['eps_pred'] for c in bin_cases])
            bin_data.append((lo + 2.5, eps_arr, pred_arr, len(bin_cases)))

    for center, eps_arr, pred_arr, n in bin_data:
        ax.errorbar(center, eps_arr.mean(), yerr=eps_arr.std(),
                    fmt='o', color='black', markersize=11,
                    capsize=8, elinewidth=2.5, capthick=2,
                    markerfacecolor='gold', markeredgewidth=1.5,
                    zorder=15)
        # show n inside
        ax.annotate(f'n={n}', xy=(center, eps_arr.mean()),
                     xytext=(center+1.2, eps_arr.mean()),
                     fontsize=8.5, zorder=16)

    # Translucent individual cases
    for c in main_regime:
        ax.scatter(c['am_wt'], c['eps_meas'], s=18, color='gray',
                   alpha=0.4, zorder=5)

    ax.set_xlabel('AM weight fraction (%)', fontsize=12)
    ax.set_ylabel('Porosity ε (%)', fontsize=12)
    n_main = len(main_regime)
    ax.set_title(f'Binned mean ± σ vs strict physics curve\n'
                 f'(main regime: bimodal AM, λ≥4, ε≥8%;  N={n_main})',
                 fontsize=11)
    ax.legend(fontsize=9, loc='upper right')
    ax.grid(alpha=0.3)
    ax.set_xlim(55, 100)
    ax.set_ylim(8, 32)

    # ── PANEL 2: residual per case  (measured − predicted) ───────
    ax = axes[1]
    cmap = {'particulate': 'tab:blue', '박막(1mAh)': 'tab:green',
            '후막(6mAh)': 'tab:orange', '후막(8mAh)': 'tab:red'}
    label_en = {'particulate': 'particulate',
                '박막(1mAh)': 'thin film 1mAh',
                '후막(6mAh)': 'thick film 6mAh',
                '후막(8mAh)': 'thick film 8mAh'}
    mk = {'particulate': 'o', '박막(1mAh)': 's',
          '후막(6mAh)': '^', '후막(8mAh)': 'D'}

    for camp in sorted({c['campaign'] for c in main_regime}):
        sub = [c for c in main_regime if c['campaign'] == camp]
        ax.scatter([c['am_wt'] for c in sub],
                   [c['eps_meas'] - c['eps_pred'] for c in sub],
                   s=70, color=cmap.get(camp, 'gray'),
                   marker=mk.get(camp, 'o'),
                   alpha=0.85, edgecolors='black', linewidth=0.5,
                   label=f'{label_en.get(camp, camp)} (n={len(sub)})')

    ax.axhline(0, color='k', lw=1.5, zorder=1)
    ax.axhspan(-2, 2, color='gray', alpha=0.18, label='±2%')
    ax.axhspan(-3, 3, color='gray', alpha=0.10)

    res = np.array([c['eps_meas'] - c['eps_pred'] for c in main_regime])
    ax.axhline(res.mean(), color='crimson', lw=2, ls='--',
               label=f'mean = {res.mean():+.2f}%')

    n_le2 = int(np.sum(np.abs(res) < 2))
    n_le3 = int(np.sum(np.abs(res) < 3))
    n_le5 = int(np.sum(np.abs(res) < 5))
    n = len(main_regime)

    ax.set_xlabel('AM weight fraction (%)', fontsize=12)
    ax.set_ylabel('Residual: measured − predicted (%)', fontsize=12)
    ax.set_title(f'Residual vs composition  (N={n}, main regime)\n'
                 f'mean Δ={res.mean():+.2f}%, σ={res.std():.2f}%,  '
                 f'|Δ|<2%: {100*n_le2/n:.0f}%, '
                 f'<3%: {100*n_le3/n:.0f}%, '
                 f'<5%: {100*n_le5/n:.0f}%',
                 fontsize=11)
    ax.legend(fontsize=9, loc='upper right')
    ax.grid(alpha=0.3)
    ax.set_xlim(55, 100)
    ax.set_ylim(-12, 12)

    plt.suptitle('Strict physics-first model — binned-mean validation',
                 fontsize=13, fontweight='bold', y=1.00)
    plt.tight_layout()
    out = Path('porosity_binned_mean.png')
    plt.savefig(out, dpi=150, bbox_inches='tight')
    print(f'✓ Saved: {out.resolve()}')


if __name__ == '__main__':
    main()
