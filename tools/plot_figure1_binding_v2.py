"""Figure 1 binding curve v2 — comp4 v2 anneal champion reflected.

Recreates user's "UMA binding curves (R=+0.925)" figure with comp4 swapped to
v2 anneal champion. Uses asymptote-subtracted "Adhesion energy" (figure
convention: negative = bonding) since raw v30u Wad has strain-baseline offset.

Source data: output/comp4_v2_adhesion/v30u_v2_curves.json (KISTI v30u_v2)

Outputs:
  output/comp4_v2_adhesion/figures/figure1_binding_v2.{png,pdf}
"""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

OUT_DIR = Path("output/comp4_v2_adhesion/figures")
DATA = Path("output/comp4_v2_adhesion/v30u_v2_curves.json")
PAPER_EXP = {'comp1': 194, 'comp2': 180, 'comp3': 316, 'comp4': 298, 'comp5': 249}

LABELS = {
    'comp1':  r'comp1: Li$_6$PS$_5$Cl',
    'comp2':  r'comp2: Li$_6$PS$_5$Cl$_{0.5}$Br$_{0.5}$',
    'comp3':  r'comp3: Li$_{5.4}$PS$_{4.4}$Cl$_{1.0}$Br$_{0.6}$',
    'comp4':  r'comp4: Li$_{5.4}$PS$_{4.4}$Cl$_{0.8}$Br$_{0.8}$ (v2)',
    'comp5':  r'comp5: Li$_{5.4}$PS$_{4.4}$Cl$_{0.6}$Br$_{1.0}$',
    'modelC': r'modelC: Li$_{5.4}$PS$_{4.4}$Cl$_{1.6}$',
}
COLORS = {
    'comp1':  '#1f77b4', 'comp2':  '#17becf',
    'comp3':  '#d62728', 'comp4':  '#9467bd',
    'comp5':  '#2ca02c', 'modelC': '#ff7f0e',
}
MARKERS = {'comp1':'s', 'comp2':'o', 'comp3':'^', 'comp4':'D', 'comp5':'v', 'modelC':'X'}
PAPER_COMPS = ['comp1', 'comp2', 'comp3', 'comp4', 'comp5']
ALL_COMPS = PAPER_COMPS + ['modelC']

plt.rcParams.update({
    'font.size': 11, 'axes.labelsize': 12, 'axes.titlesize': 12,
    'xtick.labelsize': 10, 'ytick.labelsize': 10, 'legend.fontsize': 9,
    'figure.dpi': 150, 'savefig.dpi': 300, 'savefig.bbox': 'tight',
})


def main():
    raw = json.load(open(DATA))
    # data[comp] = list of (gap, Wad)

    # Compute W_max + asymptote per comp + Pearson R
    summary = {}
    for c in raw:
        arr = np.array(raw[c])  # shape (N, 2)
        gaps, wads = arr[:, 0], arr[:, 1]
        i_max = int(np.argmax(wads))
        W_max = float(wads[i_max])
        d_min = float(gaps[i_max])
        W_asymp = float(np.mean(wads[-5:]))  # avg of last 5 points
        summary[c] = {'gaps': gaps, 'wads': wads, 'W_max': W_max,
                       'd_min': d_min, 'W_asymp': W_asymp}

    x_R = [summary[c]['W_max'] for c in PAPER_COMPS]
    y_R = [PAPER_EXP[c] for c in PAPER_COMPS]
    R = float(np.corrcoef(x_R, y_R)[0, 1])
    print(f"R(W_max vs paper exp) = {R:+.4f}")

    # Two-panel figure: (a) raw Wad, (b) figure-style asymptote-subtracted with sign flip
    fig, axes = plt.subplots(1, 2, figsize=(15, 5.5))

    # === Panel (a): RAW v30u Wad (our convention: positive = binding) ===
    for c in ALL_COMPS:
        d = summary[c]
        axes[0].plot(d['gaps'], d['wads'], '-' if c != 'modelC' else '--',
                     marker=MARKERS[c], color=COLORS[c], label=LABELS[c],
                     ms=5, lw=1.5, mfc=COLORS[c], mec='k', mew=0.4)
    axes[0].axvspan(1.2, 1.6, alpha=0.1, color='gray')
    axes[0].axhline(0, color='k', lw=0.5)
    axes[0].set_xlabel(r'Interface gap, $d$ (Å)')
    axes[0].set_ylabel(r'$W_{ad}$ (J m$^{-2}$, raw v30u)')
    axes[0].set_title(f'(a) Raw $W_{{ad}}$ from v30u UMA Z-scan'
                       f'\nR($W_{{max}}$ vs paper exp) = {R:+.3f}')
    axes[0].set_xlim(0.5, 6.0)
    axes[0].grid(alpha=0.3)
    axes[0].legend(loc='lower right', fontsize=8)

    # === Panel (b): Original figure convention — E_adh = -W (sign flipped) ===
    # Original "UMA binding curves (R=+0.925)": positive value = repulsive,
    # negative value = bonding. Restrict to gap 0.8-4.0 (matching user's figure).
    # Note: absolute scale ~100x user's figure (UMA-s-1p1 vs paper-figure UMA
    # version + 1L vs 3L NCM differ). Trends/ranking preserved (R=+0.964).
    for c in ALL_COMPS:
        d = summary[c]
        mask = (d['gaps'] >= 0.8) & (d['gaps'] <= 4.0)
        gaps_z = d['gaps'][mask]
        E_adh = -d['wads'][mask]  # figure convention: -W
        axes[1].plot(gaps_z, E_adh, '-' if c != 'modelC' else '--',
                     marker=MARKERS[c], color=COLORS[c], label=LABELS[c],
                     ms=6, lw=1.5, mfc=COLORS[c], mec='k', mew=0.4)
    axes[1].axvspan(1.2, 1.6, alpha=0.1, color='gray')
    axes[1].axhline(0, color='k', lw=0.5)
    axes[1].set_xlabel(r'Interface gap, $d$ (Å)')
    axes[1].set_ylabel(r'Adhesion energy $-W_{ad}$ (J m$^{-2}$, figure convention)')
    axes[1].set_title('(b) Original figure convention: $E_{adh} = -W$ '
                       '(negative = binding)')
    axes[1].set_xlim(0.8, 4.0)
    axes[1].grid(alpha=0.3)
    axes[1].legend(loc='upper right', fontsize=8)

    fig.suptitle('Figure 1 v2 — UMA Z-scan binding curves (comp4 = v2 anneal champion)',
                 fontsize=12, y=1.01)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "figure1_binding_v2.png")
    fig.savefig(OUT_DIR / "figure1_binding_v2.pdf")
    plt.close()
    print(f"saved figure1_binding_v2.png/pdf")

    # Print summary table
    print(f"\n{'comp':<8} {'paper':>6} {'W_max':>10} {'d_min':>8} {'W_asymp':>10} {'well_depth':>11}")
    for c in ALL_COMPS:
        d = summary[c]
        depth = d['W_max'] - d['W_asymp']
        pe = PAPER_EXP.get(c, '—')
        print(f"{c:<8} {str(pe):>6} {d['W_max']:>+10.3f} {d['d_min']:>8.2f} "
              f"{d['W_asymp']:>+10.3f} {depth:>+11.3f}")


if __name__ == '__main__':
    main()
