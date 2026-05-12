"""Plot full ensemble binding curves — mean line + std fill_between.

Reads v30u_full_ensemble_results/summary.json (or samples.json for richer
stats), produces image-2 style figure:
  - 5 paper comps (modelC excluded by default; use --include-modelc)
  - PCHIP smooth mean curves (300 dense points)
  - ±1σ shaded band per comp
  - Gray vertical span 1.2-1.6 Å (equilibrium gap window)
  - Title: R(W_max_mean, paper exp Wad) shown
  - Outputs: PNG + PDF + CSV (gap, comp_mean, comp_std)

Usage:
  python plot_v30u_full_ensemble.py [--summary path.json] [--include-modelc]
  python plot_v30u_full_ensemble.py --linfit       # optional: apply
                                                    # uma_main_paper linear-fit calibration
"""
import csv, json, argparse
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.interpolate import PchipInterpolator

PAPER_EXP = {'comp1': 194, 'comp2': 180, 'comp3': 316, 'comp4': 298, 'comp5': 249}
PAPER_COMPS = ['comp1', 'comp2', 'comp3', 'comp4', 'comp5']

COLORS  = {'comp1': '#1f77b4', 'comp2': '#17becf',
           'comp3': '#d62728', 'comp4': '#9467bd',
           'comp5': '#2ca02c', 'modelC': '#ff7f0e'}
MARKERS = {'comp1': 's', 'comp2': 'o', 'comp3': '^',
           'comp4': 'D', 'comp5': 'v', 'modelC': 'X'}
LABELS  = {
    'comp1': r'comp1: Li$_6$PS$_5$Cl',
    'comp2': r'comp2: Li$_6$PS$_5$Cl$_{0.5}$Br$_{0.5}$',
    'comp3': r'comp3: Li$_{5.4}$PS$_{4.4}$Cl$_{1.0}$Br$_{0.6}$',
    'comp4': r'comp4: Li$_{5.4}$PS$_{4.4}$Cl$_{0.8}$Br$_{0.8}$',
    'comp5': r'comp5: Li$_{5.4}$PS$_{4.4}$Cl$_{0.6}$Br$_{1.0}$',
    'modelC': r'modelC: Li$_{5.4}$PS$_{4.4}$Cl$_{1.6}$',
}

GAP_LO, GAP_HI = 0.8, 4.0
GAP_WINDOW_LO, GAP_WINDOW_HI = 1.2, 1.6


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--summary', default='v30u_full_ensemble_results/summary.json')
    p.add_argument('--include-modelc', action='store_true')
    p.add_argument('--linfit', action='store_true',
                   help='apply uma_main_paper linear-fit calibration to mean')
    p.add_argument('--ylim', nargs=2, type=float, default=None,
                   help='manual Y range, e.g. --ylim -50 50')
    args = p.parse_args()

    summary = json.load(open(args.summary))
    comps = list(PAPER_COMPS)
    if args.include_modelc and 'modelC' in summary:
        comps.append('modelC')

    OUT_DIR = Path(args.summary).parent
    OUT_DIR.mkdir(exist_ok=True)

    # Linear-fit calibration (paper_Wad = a × W_max_mean + b)
    a_fit, b_fit, R = None, None, None
    have = [c for c in PAPER_COMPS if c in summary]
    if len(have) >= 3:
        x = np.array([summary[c]['W_max_mean'] for c in have])
        y = np.array([PAPER_EXP[c] for c in have])
        a_fit, b_fit = np.polyfit(x, y, 1)
        R = float(np.corrcoef(x, y)[0, 1])

    def transform(W):
        if not args.linfit or a_fit is None:
            return -W      # convention: negative = binding (just sign flip)
        return -(a_fit * W + b_fit) / 1000.0   # paper_Wad scale → J/m²

    plt.rcParams.update({
        'font.size': 13, 'axes.labelsize': 15, 'axes.titlesize': 16,
        'xtick.labelsize': 12, 'ytick.labelsize': 12, 'legend.fontsize': 11,
        'figure.dpi': 150, 'savefig.dpi': 300, 'savefig.bbox': 'tight',
    })

    fig, ax = plt.subplots(figsize=(12, 7.5))

    for c in comps:
        if c not in summary:
            continue
        d = summary[c]
        gaps = np.array(d['gaps'])
        mean = np.array(d['Wad_mean'])
        std  = np.array(d['Wad_std'])

        # Mask in plot range
        m = (gaps >= GAP_LO) & (gaps <= GAP_HI)
        gz = gaps[m]; mz = mean[m]; sz = std[m]

        # Adhesion convention
        adh_mean = transform(mz)
        adh_upper = transform(mz - sz)  # less binding (more positive Wad → more negative adh)
        adh_lower = transform(mz + sz)  # more binding

        # PCHIP smooth
        g_dense = np.linspace(gz.min(), gz.max(), 300)
        adh_smooth = PchipInterpolator(gz, adh_mean)(g_dense)
        upper_smooth = PchipInterpolator(gz, adh_upper)(g_dense)
        lower_smooth = PchipInterpolator(gz, adh_lower)(g_dense)

        ax.fill_between(g_dense, lower_smooth, upper_smooth,
                        color=COLORS[c], alpha=0.15, zorder=2)
        ax.plot(g_dense, adh_smooth, '-', color=COLORS[c], lw=3.0, alpha=0.95, zorder=5)
        ax.plot(gz, adh_mean, MARKERS[c], color=COLORS[c],
                ms=9, mec='k', mew=0.5, label=LABELS[c], zorder=10)

    ax.axvspan(GAP_WINDOW_LO, GAP_WINDOW_HI, alpha=0.13, color='gray', zorder=1)
    ax.axhline(0, color='k', lw=0.7, alpha=0.7, zorder=2)
    ax.set_xlabel(r'Interface gap, $d$ (Å)')
    ax.set_ylabel(r'Adhesion energy (J m$^{-2}$)')

    n_samp = summary[have[0]]['n_samples'] if have else 0
    title = f'UMA binding curves — ensemble (n={n_samp} per gap, mean ± 1σ)'
    if args.linfit and R is not None:
        title += f'  [linear-fit cal: R={R:+.3f}]'
    ax.set_title(title)
    ax.set_xlim(GAP_LO, GAP_HI)
    if args.ylim:
        ax.set_ylim(*args.ylim)
    ax.grid(True, alpha=0.25)
    ax.legend(loc='lower right' if args.linfit else 'best', framealpha=0.95)

    fig.tight_layout()
    suffix = "_linfit" if args.linfit else ""
    png = OUT_DIR / f"v30u_full_ensemble_curves{suffix}.png"
    pdf = OUT_DIR / f"v30u_full_ensemble_curves{suffix}.pdf"
    csv_path = OUT_DIR / f"v30u_full_ensemble_curves{suffix}.csv"
    fig.savefig(png); fig.savefig(pdf); plt.close()

    # CSV: gap, per-comp mean ± std
    with open(csv_path, 'w', newline='') as f:
        w = csv.writer(f)
        f.write(f"# UMA full ensemble binding curves — {n_samp} configs per (comp,gap)\n")
        f.write(f"# 5 z-shifts × 36 xy-shifts (6×6 grid), gap 0.5-6.0 Å step 0.25\n")
        if args.linfit and R is not None:
            f.write(f"# linear-fit: paper_Wad = {a_fit:.4f}*W_max_mean + {b_fit:.4f}, R={R:+.4f}\n")
            f.write(f"# adh = -(a*W + b)/1000, J/m²\n")
        else:
            f.write(f"# adh = -W_mean (raw, no calibration), J/m²\n")
        header = ['gap_A']
        for c in comps:
            header.extend([f'{c}_mean', f'{c}_std'])
        w.writerow(header)
        if comps:
            gaps = summary[comps[0]]['gaps']
            for i, g in enumerate(gaps):
                if not (GAP_LO <= g <= GAP_HI):
                    continue
                row = [f"{g:.3f}"]
                for c in comps:
                    if c in summary:
                        m = summary[c]['Wad_mean'][i]
                        s = summary[c]['Wad_std'][i]
                        m_t = transform(np.array([m]))[0]
                        row.append(f"{m_t:.6f}"); row.append(f"{s:.6f}")
                    else:
                        row.append(""); row.append("")
                w.writerow(row)

    print(f"saved {png}\nsaved {pdf}\nsaved {csv_path}\n")
    print(f"{'comp':<8} {'W_max_mean':>12} {'W_max_std':>10} {'d':>6} {'paper':>6}")
    for c in comps:
        if c not in summary: continue
        s = summary[c]
        print(f"{c:<8} {s['W_max_mean']:>+12.3f} {s['W_max_std']:>10.3f} "
              f"{s['d_at_W_max']:>6.2f} {PAPER_EXP.get(c,'—'):>6}")
    if R is not None:
        print(f"\nR(W_max_mean vs paper) = {R:+.4f}")


if __name__ == "__main__":
    main()
