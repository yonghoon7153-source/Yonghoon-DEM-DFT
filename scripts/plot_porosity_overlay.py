#!/usr/bin/env python3
"""Overlay all 82 DEM cases on the strict physics curve.

Left panel : full AM-wt sweep with all measured cases (colored by
             campaign, sized by λ=D_AM_eff/D_SE) on top of the strict
             physics prediction curves (P:S=3:7/5:5/7:3).
Right panel: same scatter but only λ≥4 (model-applicable regime),
             showing the curve actually fits these cases.
"""
import csv
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sys

sys.path.insert(0, str(Path(__file__).parent))
from predict_porosity_strict_physics import (predict_strict, F_PERC,
                                               ALPHA_KC, EPS_PURE_SE_EXP,
                                               EPS_PURE_AM)


def fnum(s):
    try:
        return float(s)
    except (ValueError, TypeError):
        return None


def load_cases():
    rows = list(csv.DictReader(open('all_dem_porosity.csv')))
    out = []
    for r in rows:
        am = fnum(r['am_wt'])
        if am is None:
            continue
        # CSV r_*_um values are 1000× physical
        d_se   = (fnum(r['r_SE_um'])   or 0) * 2 / 1000
        d_am_p = (fnum(r['r_AM_P_um']) or 0) * 2 / 1000
        d_am_s = (fnum(r['r_AM_S_um']) or 0) * 2 / 1000
        n_p    = fnum(r['n_AM_P']) or 0
        n_s    = fnum(r['n_AM_S']) or 0
        if d_se <= 0:
            continue
        if n_p and n_s:
            vp = n_p * d_am_p ** 3
            vs = n_s * d_am_s ** 3
            d_eff = (vp * d_am_p + vs * d_am_s) / (vp + vs)
        elif n_p:
            d_eff = d_am_p
        else:
            d_eff = d_am_s
        out.append(dict(
            case_id=r['case_id'], campaign=r['campaign'],
            am_wt=am, se_wt=fnum(r['se_wt']),
            d_se=d_se, d_eff_am=d_eff, lam=d_eff/d_se,
            eps=fnum(r['porosity_pct']),
        ))
    return out


def main():
    cases = load_cases()
    print(f'Loaded {len(cases)} cases for plot')

    # Strict physics curves (default trimodal D12+4+1 sizes)
    am_arr = np.linspace(0.5, 99.5, 200)
    p_s_curves = [(3, 7), (5, 5), (7, 3)]
    curves = {}
    for p_s in p_s_curves:
        ys = [predict_strict((am, 100-am), p_s)['eps_pred'] * 100
              for am in am_arr]
        curves[p_s] = np.array(ys)

    # Style
    label_en = {'particulate': 'particulate (D_AM=6,8 µm)',
                '박막(1mAh)': 'thin film 1mAh (D=5+10 µm)',
                '후막(6mAh)': 'thick film 6mAh (D=4+12 µm)',
                '후막(8mAh)': 'thick film 8mAh (D=5+10 µm)'}
    cmap_e = {'particulate': 'tab:blue',
              '박막(1mAh)': 'tab:green',
              '후막(6mAh)': 'tab:orange',
              '후막(8mAh)': 'tab:red'}
    mk = {'particulate': 'o', '박막(1mAh)': 's',
          '후막(6mAh)': '^', '후막(8mAh)': 'D'}

    fig, axes = plt.subplots(1, 2, figsize=(16, 6.8))

    # ── Panel 1: ALL 82 cases on strict physics curves ──
    ax = axes[0]
    ax.plot(am_arr, curves[(3, 7)], '-', color='tab:blue',  lw=2.0,
            alpha=0.7, label='strict physics  P:S=3:7')
    ax.plot(am_arr, curves[(5, 5)], '-', color='tab:green', lw=2.0,
            alpha=0.7, label='strict physics  P:S=5:5')
    ax.plot(am_arr, curves[(7, 3)], '-', color='crimson',   lw=2.5,
                                              label='strict physics  P:S=7:3')

    # Anchors
    ax.scatter([0, 100], [EPS_PURE_SE_EXP*100, EPS_PURE_AM*100],
               s=200, marker='s', color='darkgreen',
               edgecolors='black', linewidth=1.5, zorder=12,
               label='anchors (10% / 36%)')

    # All 82 cases, colored by campaign, sized by λ (small → small marker)
    for camp, sty in cmap_e.items():
        sub = [c for c in cases if c['campaign'] == camp]
        if not sub:
            continue
        xs   = [c['am_wt'] for c in sub]
        ys   = [c['eps']   for c in sub]
        sizes = [max(20, min(200, 20 * c['lam'])) for c in sub]
        ax.scatter(xs, ys, s=sizes, color=cmap_e[camp],
                   marker=mk[camp], alpha=0.75,
                   edgecolors='black', linewidth=0.5, zorder=10,
                   label=f'{label_en[camp]} (n={len(sub)})')

    ax.set_xlabel('AM weight fraction (%)', fontsize=12)
    ax.set_ylabel('Porosity ε (%)', fontsize=12)
    ax.set_title(f'82 DEM cases overlaid on strict physics curves\n'
                  f'(marker size ∝ size ratio λ = D_AM_eff / D_SE)',
                 fontsize=11)
    ax.legend(fontsize=8.5, loc='upper left', framealpha=0.95)
    ax.grid(alpha=0.3)
    ax.set_xlim(-2, 102)
    ax.set_ylim(0, 42)

    # ── Panel 2: only λ ≥ 4 (model-applicable regime) ──
    ax = axes[1]
    ax.plot(am_arr, curves[(3, 7)], '-', color='tab:blue',  lw=2.0,
            alpha=0.7, label='P:S=3:7')
    ax.plot(am_arr, curves[(5, 5)], '-', color='tab:green', lw=2.0,
            alpha=0.7, label='P:S=5:5')
    ax.plot(am_arr, curves[(7, 3)], '-', color='crimson',   lw=2.5,
            label='P:S=7:3')
    ax.scatter([0, 100], [EPS_PURE_SE_EXP*100, EPS_PURE_AM*100],
               s=200, marker='s', color='darkgreen',
               edgecolors='black', linewidth=1.5, zorder=12)

    sub_hi = [c for c in cases if c['lam'] >= 4]
    sub_lo = [c for c in cases if c['lam'] <  4]
    for camp, sty in cmap_e.items():
        s_hi = [c for c in sub_hi if c['campaign'] == camp]
        if s_hi:
            ax.scatter([c['am_wt'] for c in s_hi],
                       [c['eps']   for c in s_hi],
                       s=70, color=cmap_e[camp],
                       marker=mk[camp], alpha=0.85,
                       edgecolors='black', linewidth=0.5, zorder=10,
                       label=f'{label_en[camp].split(" (")[0]} λ≥4 (n={len(s_hi)})')
    # Greyed-out small-λ cases
    if sub_lo:
        ax.scatter([c['am_wt'] for c in sub_lo],
                   [c['eps']   for c in sub_lo],
                   s=30, color='lightgray', marker='x',
                   alpha=0.6, zorder=5,
                   label=f'λ<4 (out of regime, n={len(sub_lo)})')

    ax.set_xlabel('AM weight fraction (%)', fontsize=12)
    ax.set_ylabel('Porosity ε (%)', fontsize=12)
    ax.set_title(f'Model-applicable regime: λ ≥ 4   (N={len(sub_hi)} of {len(cases)})\n'
                 f'(low-λ cases shown faded as out-of-regime)', fontsize=11)
    ax.legend(fontsize=8.5, loc='upper left', framealpha=0.95)
    ax.grid(alpha=0.3)
    ax.set_xlim(-2, 102)
    ax.set_ylim(0, 42)

    plt.tight_layout()
    out = Path('porosity_overlay_82cases.png')
    plt.savefig(out, dpi=150, bbox_inches='tight')
    print(f'✓ Saved: {out.resolve()}')

    # Stats for λ≥4 subset
    if sub_hi:
        # need to recompute residual using the model curves at each point
        # (here approximated using P:S=7:3 curve since most cases are 7:3-ish)
        # better: just use the per-case prediction from validate script
        print(f'\nλ ≥ 4 subset:  {len(sub_hi)} cases')
        print(f'λ < 4 subset:  {len(sub_lo)} cases (D_SE > 1 µm)')


if __name__ == '__main__':
    main()
