#!/usr/bin/env python3
"""Section 7 design-rule heatmap from the 10-case sweep CSV.

Generates Figure (section7_design_rules.png) summarizing how
each transport metric depends on (P:S ratio, r_SE).  Three
subpanels — σ_ionic, σ_e, τ_Laplace_eff — laid out as a
P:S × r_SE grid colored by metric value, plus an overlaid
porosity number on each cell.

Source: docs/db/section7_10case_sweep.csv  (10 real_1..real_10 cases).
"""
import csv
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def fnum(s):
    try: return float(s)
    except: return None


def load_section7():
    rows = list(csv.DictReader(open('docs/db/section7_10case_sweep.csv')))
    out = []
    for r in rows:
        out.append(dict(
            case_id=r['case_id'],
            P_S=r['P_S_ratio'],
            r_SE=fnum(r['r_SE_um']),
            poro=fnum(r['porosity_pct']),
            sigma_i=fnum(r['sigma_ionic_mScm']),
            sigma_e=fnum(r['sigma_e_mScm']),
            sigma_th=fnum(r['sigma_th_mScm']),
            perc=fnum(r['percolation_pct']),
            AM_perc=fnum(r['AM_percolation_pct']),
            severe=fnum(r['total_severe_pct']),
            tau=fnum(r['tau_Lap_eff']),
        ))
    return out


def build_grid(rows, value_key):
    """Build a (P:S × r_SE) grid for plotting."""
    P_S_order = ['0:10', '3:7', '5:5', '7:3', '10:0']
    r_SE_vals = sorted({r['r_SE'] for r in rows})  # [0.5, 1.5]
    Z = np.full((len(P_S_order), len(r_SE_vals)), np.nan)
    for r in rows:
        if r['P_S'] in P_S_order and r['r_SE'] in r_SE_vals:
            i = P_S_order.index(r['P_S'])
            j = r_SE_vals.index(r['r_SE'])
            v = r[value_key]
            if v is not None:
                Z[i, j] = v
    return Z, P_S_order, r_SE_vals


def panel(ax, rows, value_key, title, cbar_label, cmap='viridis',
          fmt='{:.3f}', overlay_key='poro', overlay_fmt='ε={:.1f}%'):
    Z, P_S, r_SE = build_grid(rows, value_key)
    Zo, _, _ = build_grid(rows, overlay_key)

    im = ax.imshow(Z, cmap=cmap, aspect='auto', origin='lower')
    for i in range(Z.shape[0]):
        for j in range(Z.shape[1]):
            if not np.isnan(Z[i, j]):
                val_txt = fmt.format(Z[i, j])
                ov_txt = overlay_fmt.format(Zo[i, j]) if not np.isnan(Zo[i, j]) else ''
                txt = val_txt if not ov_txt else f'{val_txt}\n{ov_txt}'
                # Pick contrasting text color
                vmin, vmax = np.nanmin(Z), np.nanmax(Z)
                norm = (Z[i, j] - vmin) / (vmax - vmin) if vmax > vmin else 0.5
                color = 'white' if norm < 0.5 else 'black'
                ax.text(j, i, txt, ha='center', va='center',
                        color=color, fontsize=9, fontweight='bold')

    ax.set_xticks(range(len(r_SE)))
    ax.set_xticklabels([f'{v:.1f} µm' for v in r_SE], fontsize=10)
    ax.set_yticks(range(len(P_S)))
    ax.set_yticklabels(P_S, fontsize=10)
    ax.set_xlabel('SE radius r_SE', fontsize=11)
    ax.set_ylabel('AM_P : AM_S ratio (P:S)', fontsize=11)
    ax.set_title(title, fontsize=11, fontweight='bold')
    plt.colorbar(im, ax=ax, label=cbar_label, shrink=0.85)


def main():
    rows = load_section7()
    print(f'Section 7 rows: {len(rows)}')
    for r in rows:
        print(f"  {r['case_id']:>8s}: P:S={r['P_S']}  r_SE={r['r_SE']}µm  "
              f"ε={r['poro']}%  σ_i={r['sigma_i']}  σ_e={r['sigma_e']}  "
              f"τ={r['tau']}")

    fig, axes = plt.subplots(2, 2, figsize=(13, 11))

    panel(axes[0, 0], rows, 'sigma_i',
          'σ_ionic — full network solver (mS/cm)',
          'σ_ionic (mS/cm)', cmap='Blues')
    panel(axes[0, 1], rows, 'sigma_e',
          'σ_electronic — fracture-aware (mS/cm)',
          'σ_e (mS/cm)', cmap='Oranges', fmt='{:.2f}')
    panel(axes[1, 0], rows, 'tau',
          'τ_Laplace,eff — COMSOL/EIS input',
          'τ_eff', cmap='RdPu', fmt='{:.2f}')
    panel(axes[1, 1], rows, 'severe',
          'Severe damage fraction (%)',
          'severe %', cmap='Reds', fmt='{:.1f}%')

    plt.suptitle('Section 7 — design-rule sweep (10 cases, P:S × r_SE)\n'
                 'cell labels show metric value + porosity ε',
                 fontsize=13, fontweight='bold', y=1.00)
    plt.tight_layout()
    out = Path('docs/figures/section7_design_rules.png')
    out.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out, dpi=150, bbox_inches='tight')
    print(f'\n✓ Saved: {out.resolve()}')


if __name__ == '__main__':
    main()
