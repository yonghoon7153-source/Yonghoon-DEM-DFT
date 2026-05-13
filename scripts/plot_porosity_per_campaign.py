#!/usr/bin/env python3
"""Per-campaign validation of the strict physics-first porosity model.

4-panel layout (one per campaign).  For every case in the campaign
we plot a vertical "dumbbell":
    ● measured ε   (filled circle, colored by P:S ratio)
    × predicted ε  (case-specific lam_eff using the case's actual
                    D_AM_P, D_AM_S, D_SE) at the same AM wt%
    │ thin line connecting the two — length = residual

This reveals (a) where the model captures the trend within a campaign,
and (b) what families of cases the model misses systematically.
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
    elif n_p:
        d_eff = d_p
    else:
        d_eff = d_s if d_s else 4.0
    lam = d_eff / d_se if d_se else 1.0
    eps_rcp = bouvard_rcp(f_se, lam)
    kc = sfm(f_am, lam)
    p_se = stress_perc(f_se)
    P_eff = P_PRESS / kc
    eps_pure_eff = EPS_PURE_AM * np.exp(-K_HECKEL * P_eff / 1e6)
    delta = (EPS_PURE_AM - eps_pure_eff) * f_se * p_se
    return max(eps_rcp - delta, 0.03) * 100, lam


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
        if am is None or se is None:
            continue
        d_se = (fnum(r['r_SE_um'])   or 0) * 2 / 1000
        d_p  = (fnum(r['r_AM_P_um']) or 0) * 2 / 1000
        d_s  = (fnum(r['r_AM_S_um']) or 0) * 2 / 1000
        n_p  = fnum(r['n_AM_P']) or 0
        n_s  = fnum(r['n_AM_S']) or 0
        meas = fnum(r['porosity_pct'])
        if not meas or d_se <= 0:
            continue
        eps_pred, lam = predict(am, se, d_p, n_p, d_s, n_s, d_se)
        p_v = fnum(r['p_vol']) or 0
        s_v = fnum(r['s_vol']) or 0
        if p_v + s_v <= 0:
            ps_str = '0:10'
            ps_key = '0:10'
        else:
            ps_str = f"{int(p_v)}:{int(s_v)}"
            ps_key = ps_str
        out.append(dict(
            case_id=r['case_id'], campaign=r['campaign'],
            am=am, se=se, d_se=d_se, d_p=d_p, d_s=d_s,
            n_p=n_p, n_s=n_s, lam=lam, ps=ps_key,
            eps_meas=meas, eps_pred=eps_pred,
            res=meas - eps_pred,
        ))
    return out


def plot_one(ax, cases, title):
    """One campaign panel."""
    # color by P:S
    ps_color = {
        '10:0': 'tab:red',
        '7:3':  'tab:orange',
        '5:5':  'tab:green',
        '3:7':  'tab:cyan',
        '0:10': 'tab:purple',
    }
    # Sort cases by AM wt for cleaner rendering
    cases = sorted(cases, key=lambda c: (c['am'], c['ps']))

    # Plot dumbbells
    for c in cases:
        x = c['am']
        col = ps_color.get(c['ps'], 'gray')
        ax.plot([x, x], [c['eps_meas'], c['eps_pred']],
                color=col, lw=0.8, alpha=0.5, zorder=2)
        ax.scatter(x, c['eps_meas'], s=55, color=col, marker='o',
                   edgecolors='black', linewidth=0.5,
                   alpha=0.9, zorder=5)
        ax.scatter(x, c['eps_pred'], s=55, color=col, marker='x',
                   alpha=0.9, linewidth=1.5, zorder=4)

    # Stats
    res = np.array([c['res'] for c in cases])
    n_le2 = int(np.sum(np.abs(res) < 2))
    n_le3 = int(np.sum(np.abs(res) < 3))
    n_le5 = int(np.sum(np.abs(res) < 5))

    # Legend by P:S
    seen = set()
    handles = []
    for c in cases:
        if c['ps'] in seen:
            continue
        seen.add(c['ps'])
        col = ps_color.get(c['ps'], 'gray')
        handles.append(plt.scatter([], [], s=55, color=col, marker='o',
                                    edgecolors='black', linewidth=0.5,
                                    label=f'P:S={c["ps"]}'))
    # measured/predicted legend
    handles.append(plt.scatter([], [], s=55, color='gray', marker='o',
                                edgecolors='black', linewidth=0.5,
                                label='measured (●)'))
    handles.append(plt.scatter([], [], s=55, color='gray', marker='x',
                                linewidth=1.5, label='predicted (×)'))
    ax.legend(handles=handles, fontsize=8, loc='upper left',
              framealpha=0.95, ncol=2)

    ax.set_xlabel('AM weight fraction (%)', fontsize=11)
    ax.set_ylabel('Porosity ε (%)', fontsize=11)
    n = len(cases)
    ax.set_title(f'{title}   (N={n})\n'
                 f'mean Δ={res.mean():+.2f}%, σ={res.std():.2f}%,  '
                 f'|Δ|<2: {n_le2}, <3: {n_le3}, <5: {n_le5}',
                 fontsize=10)
    ax.grid(alpha=0.3)
    ax.set_xlim(-2, 102)
    ax.set_ylim(0, 40)


def main():
    cases = load()
    print(f'Loaded {len(cases)} cases')

    by_camp = {}
    for c in cases:
        by_camp.setdefault(c['campaign'], []).append(c)

    label_en = {'particulate': 'particulate  (monomodal AM, D=6 or 8 µm)',
                '박막(1mAh)':  'thin film 1mAh  (bimodal AM, D=5+10 µm)',
                '후막(6mAh)':  'thick film 6mAh  (bimodal AM, D=4+12 µm)',
                '후막(8mAh)':  'thick film 8mAh  (bimodal AM, D=5+10 µm)'}
    order = ['particulate', '박막(1mAh)', '후막(6mAh)', '후막(8mAh)']

    fig, axes = plt.subplots(2, 2, figsize=(15, 11))
    for i, camp in enumerate(order):
        ax = axes[i // 2, i % 2]
        if camp not in by_camp:
            ax.set_visible(False)
            continue
        plot_one(ax, by_camp[camp], label_en[camp])

    plt.suptitle('Per-campaign validation: strict physics-first '
                 '(case-specific λ_eff used per point)',
                 fontsize=13, fontweight='bold', y=1.00)
    plt.tight_layout()
    out = Path('porosity_per_campaign.png')
    plt.savefig(out, dpi=150, bbox_inches='tight')
    print(f'✓ Saved: {out.resolve()}')

    # Per-campaign summary
    print('\nPer-campaign residual summary (measured − predicted, %):')
    print(f'{"campaign":>20s} {"N":>4s} {"mean":>7s} {"σ":>6s} '
          f'{"|Δ|<2":>6s} {"|Δ|<3":>6s} {"|Δ|<5":>6s}')
    for camp in order:
        if camp not in by_camp:
            continue
        res = np.array([c['res'] for c in by_camp[camp]])
        print(f'{camp:>20s} {len(res):4d} '
              f'{res.mean():+7.2f} {res.std():6.2f} '
              f'{int(np.sum(np.abs(res)<2)):6d} '
              f'{int(np.sum(np.abs(res)<3)):6d} '
              f'{int(np.sum(np.abs(res)<5)):6d}')


if __name__ == '__main__':
    main()
