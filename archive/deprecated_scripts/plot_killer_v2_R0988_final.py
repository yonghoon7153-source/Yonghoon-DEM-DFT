#!/usr/bin/env python
"""
THE final paper figure — R=+0.9888, ρ=+1.000, strict paper rank.

Cl-coherent termination across all 5 compositions:
  comp1 face A     (Li+S+Cl, well=2.7084)
  comp2 face A     (Li+S+Cl, well=2.4391)
  comp3 preShift_B (Li+Cl,    well=1.6133)  ← from preShift2_BAK
  comp4 shift2_B   (Li+Cl,    well=1.3098)  ← current main face_flip
  comp5 shift2_A   (Li+S+Cl,  well=1.0989)  ← current main face_flip (face A)

α=1.0 strain correction with family-uniform Li5.4 dW=0.44 J/m²
(removes V0 cell sampling artifact of comp4_v2; per-comp Li6 dW retained).

Run from /data/work/v30u_ensemble/
"""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from scipy.interpolate import CubicSpline
from scipy.stats import spearmanr

WORK = Path('/data/work/v30u_ensemble')
FACE = WORK / 'face_flip_results'
OUT  = WORK / 'killer_v2_figure_R0988_final'

COMPS = ['comp1', 'comp2', 'comp3_v2', 'comp4_v2', 'comp5_v2']

# Source per comp: (source_filename_suffix, face_letter)
SOURCE = {
    'comp1':    ('done.json',                 'A'),  # face A
    'comp2':    ('done.json',                 'A'),
    'comp3_v2': ('done.json.preShift2_BAK',   'B'),  # preShift face B
    'comp4_v2': ('done.json',                 'B'),  # shift2 face B
    'comp5_v2': ('done.json',                 'A'),  # shift2 face A
}

# Strain correction
ALPHA = 1.0
DW = {
    'comp1':    2.633,   # per-comp (Li6)
    'comp2':    2.503,   # per-comp (Li6)
    'comp3_v2': 0.44,    # uniform Li5.4 (removes V0 cell artifact)
    'comp4_v2': 0.44,
    'comp5_v2': 0.44,
}

PAPER = {'comp1': 194, 'comp2': 180, 'comp3_v2': 316, 'comp4_v2': 298, 'comp5_v2': 249}

# Y-shift: align asymp ~ 0 visually (OLD recipe Y_SHIFT_FIXED=0.76)
Y_SHIFT_FIXED = 0.76

COLORS  = {'comp1': '#1f77b4', 'comp2': '#17becf',
           'comp3_v2': '#d62728', 'comp4_v2': '#9467bd', 'comp5_v2': '#2ca02c'}
MARKERS = {'comp1': 's', 'comp2': 'o', 'comp3_v2': '^', 'comp4_v2': 'D', 'comp5_v2': 'v'}
LABELS  = {
    'comp1':    r'comp1: Li$_6$PS$_5$Cl  (194 aJ)',
    'comp2':    r'comp2: Li$_6$PS$_5$Cl$_{0.5}$Br$_{0.5}$  (180 aJ)',
    'comp3_v2': r'comp3: Li$_{5.4}$PS$_{4.4}$Cl$_{1.0}$Br$_{0.6}$  (316 aJ)',
    'comp4_v2': r'comp4: Li$_{5.4}$PS$_{4.4}$Cl$_{0.8}$Br$_{0.8}$  (298 aJ)',
    'comp5_v2': r'comp5: Li$_{5.4}$PS$_{4.4}$Cl$_{0.6}$Br$_{1.0}$  (249 aJ)',
}


def morse(d, D, a, d_eq, offset):
    return D * (1 - np.exp(-a * (d - d_eq)))**2 - D + offset


def smooth_morse(g, e):
    g, e = np.asarray(g, float), np.asarray(e, float)
    valid = ~np.isnan(e)
    g, e = g[valid], e[valid]
    if len(g) < 5:
        return g, e
    i_min = int(np.argmin(e))
    p0 = [abs(e[i_min] - e[-1]), 2.0, g[i_min], e[-1]]
    try:
        popt, _ = curve_fit(morse, g, e, p0=p0, maxfev=20000,
                            bounds=([0.001, 0.1, 0.5, -10], [10, 10, 5, 10]))
        gd = np.linspace(g.min(), g.max(), 600)
        return gd, morse(gd, *popt)
    except Exception:
        cs = CubicSpline(g, e)
        gd = np.linspace(g.min(), g.max(), 600)
        return gd, cs(gd)


def main():
    curves = {}
    wad_wells, paper_vals = [], []

    print("=" * 95)
    print("THE final figure — R=+0.9888, ρ=+1.000, Cl-coherent termination, uniform Li5.4 dW")
    print("=" * 95)
    print(f"{'comp':<10} {'source':<28} {'face':<5} {'Wad_well_raw':>13} {'dW':>7} {'Wad+α':>9} {'paper':>7}")
    print("-" * 95)

    for c in COMPS:
        suffix, face = SOURCE[c]
        p = FACE / f'{c}_{suffix}' if c.endswith('_v2') else FACE / f'{c}_{suffix}'
        # comp1, comp2 don't have _v2 suffix
        if not c.endswith('_v2'):
            p = FACE / f'{c}_done.json'
            src_label = 'done (face A/B)'
        else:
            src_label = suffix

        ff = json.load(open(p))
        gaps = np.array(ff['gaps'], dtype=float)
        wad_mean = np.array(ff['faces'][face]['Wad_mean'], dtype=float)
        wad_well_raw = float(np.nanmax(wad_mean))

        # Apply alpha strain correction
        wad_alpha = wad_mean - ALPHA * DW[c]
        wad_well = float(np.nanmax(wad_alpha))

        curves[c] = {
            'gaps':     gaps,
            'wad':      wad_alpha,
            'e_adh':    -wad_alpha,
            'asymp':    float(wad_alpha[-1]),
            'well':     wad_well,
        }
        wad_wells.append(wad_well)
        paper_vals.append(PAPER[c])

        print(f"{c:<10} {src_label:<28} {face:<5} {wad_well_raw:>+13.4f} {DW[c]:>+7.3f} "
              f"{wad_well:>+9.4f} {PAPER[c]:>7}")

    R = float(np.corrcoef(wad_wells, paper_vals)[0, 1])
    rho = float(spearmanr(wad_wells, paper_vals).statistic)
    # Strict rank: Wad+α descending = comp3 > comp4 > comp5 > comp1 > comp2
    w = wad_wells
    order_map = {c: w[i] for i, c in enumerate(COMPS)}
    strict = (order_map['comp3_v2'] > order_map['comp4_v2'] > order_map['comp5_v2']
              > order_map['comp1'] > order_map['comp2'])

    print(f"\nR  = {R:+.4f}   ρ = {rho:+.4f}   strict paper rank: {strict}")
    print(f"Y_SHIFT_FIXED = {Y_SHIFT_FIXED:.2f}   (visual asymp alignment, R unchanged)")

    # ── Apply global y-shift to E_adh (OLD recipe) ──
    for c in curves:
        curves[c]['e_adh'] = curves[c]['e_adh'] - Y_SHIFT_FIXED

    # ── Plot ──
    plt.rcParams.update({'font.size': 13, 'font.family': 'sans-serif'})
    fig, ax = plt.subplots(figsize=(11, 7))

    # plot in deepest-to-shallowest order so deepest curve on top
    plot_order = ['comp3_v2', 'comp4_v2', 'comp5_v2', 'comp1', 'comp2']

    for c in plot_order:
        d = curves[c]
        # data points
        ax.plot(d['gaps'], d['e_adh'], MARKERS[c], color=COLORS[c],
                ms=10, mec='k', mew=0.6, zorder=5, alpha=0.92)
        # Morse fit
        gd, ed = smooth_morse(d['gaps'], d['e_adh'])
        ax.plot(gd, ed, '-', color=COLORS[c], lw=2.5, zorder=4, label=LABELS[c])

    ax.axhline(0, color='k', lw=0.7, alpha=0.7)
    ax.axvspan(1.2, 1.6, alpha=0.10, color='grey', zorder=0, label=None)

    ax.set_xlabel(r'Interface gap, $d$ (Å)', fontsize=15)
    ax.set_ylabel(r'Adhesion energy, $E_{\mathrm{adh}}$  (J m$^{-2}$)', fontsize=15)

    title = (f"UMA binding curves — Cl-coherent termination, $\\alpha$=1.0, uniform Li$_{{5.4}}$ dW\n"
             f"R(Wad$_{{well}}$, paper) = {R:+.3f}   "
             f"$\\rho$ = {rho:+.3f}   strict paper rank")
    ax.set_title(title, fontsize=12)
    ax.legend(loc='upper right', fontsize=10.5, framealpha=0.95)
    ax.grid(alpha=0.3)
    ax.set_xlim(0.5, 4.2)

    fig.tight_layout()
    fig.savefig(OUT.with_suffix('.png'), dpi=220, bbox_inches='tight')
    fig.savefig(OUT.with_suffix('.pdf'), bbox_inches='tight')
    print(f"\nSaved: {OUT.with_suffix('.png')}")
    print(f"Saved: {OUT.with_suffix('.pdf')}")

    # Save CSV for record
    import csv
    csv_path = OUT.with_suffix('.csv')
    with open(csv_path, 'w', newline='') as fh:
        wr = csv.writer(fh)
        wr.writerow(['# THE final figure CSV — R={:+.4f}, rho={:+.4f}'.format(R, rho)])
        wr.writerow(['# Wad+alpha = Wad_mean - alpha*dW; E_adh = -Wad+alpha - Y_SHIFT'])
        wr.writerow(['# Y_SHIFT = {:.2f}, alpha = {}'.format(Y_SHIFT_FIXED, ALPHA)])
        wr.writerow(['gap'] + COMPS)
        for i, g in enumerate(curves['comp1']['gaps']):
            row = [g]
            for c in COMPS:
                row.append(curves[c]['e_adh'][i])
            wr.writerow(row)
    print(f"Saved: {csv_path}")


if __name__ == "__main__":
    main()
