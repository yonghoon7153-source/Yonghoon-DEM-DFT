"""Phase 2a v7 — paper-publishable energy descriptor figure (no curves).

User decision: 'curve말고 다른 값 쓰자' — skip curves entirely, use Method A
W_max as single value per comp. Bar chart + scatter, matching paper exp Wad
reference figure style.

Method A protocol (matches db, R=+0.87 with paper exp):
  1. For each (comp, registry): find max Wad across all gaps
  2. Mean over 36 registries → W_max
  3. Std over 36 registries → W_max_std

Outputs:
  energy_descriptor_bar.pdf/png       2-panel bar: paper exp vs Method A W_max
  energy_descriptor_scatter.pdf/png   W_max vs paper exp scatter (R=+0.87)
  energy_descriptor_summary.csv       paper-citation table
"""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

OUT_DIR = Path("binding_curves_plots"); OUT_DIR.mkdir(exist_ok=True)
PATH_BIND = Path("phase1_results/binding_curves.json")
ALL_COMPS = ['comp1', 'comp2', 'comp3', 'comp4', 'comp5', 'modelC']
PAPER_COMPS = ['comp1', 'comp2', 'comp3', 'comp4', 'comp5']
PAPER_EXP = {'comp1': 194, 'comp2': 180, 'comp3': 316, 'comp4': 298, 'comp5': 249}
LABELS_SHORT = {
    'comp1':  'LPSC$_{1.0}$',
    'comp2':  'LPSC$_{0.5}$B$_{0.5}$',
    'comp3':  'LPSC$_{1.0}$B$_{0.6}$',
    'comp4':  'LPSC$_{0.8}$B$_{0.8}$',
    'comp5':  'LPSC$_{0.6}$B$_{1.0}$',
    'modelC': 'LPSC$_{1.6}$',
}
COLORS = {
    'comp1':  '#1f77b4',  'comp2':  '#17becf',
    'comp3':  '#d62728',  'comp4':  '#9467bd', 'comp5':  '#2ca02c',
    'modelC': '#ff7f0e',
}

plt.rcParams.update({
    'font.size': 11, 'axes.labelsize': 12, 'axes.titlesize': 12,
    'xtick.labelsize': 10, 'ytick.labelsize': 10, 'legend.fontsize': 9,
    'figure.dpi': 150, 'savefig.dpi': 300, 'savefig.bbox': 'tight',
})


def method_a_per_comp(d, comp):
    """For each registry: find max Wad across gap. Return list of (W_max, d_min)."""
    if comp not in d:
        return [], []
    comp_data = d[comp]
    wmax_list, dmin_list = [], []
    for reg, reg_data in comp_data.items():
        curve = reg_data.get('curve', {})
        best_w, best_g = -np.inf, None
        for g, v in curve.items():
            w = v.get('Wad_J_per_m2')
            if w is None:
                continue
            if w > best_w:
                best_w = w
                best_g = float(g)
        if best_g is not None:
            wmax_list.append(best_w)
            dmin_list.append(best_g)
    return wmax_list, dmin_list


def main():
    if not PATH_BIND.exists():
        print(f"ERROR: {PATH_BIND} not found.")
        return
    d = json.load(open(PATH_BIND))

    summary = {}
    print("Method A reproduction (mean over 36 reg of per-reg max W_ad):")
    print(f"{'comp':<8} {'paper exp':>10} {'W_max':>10} {'std':>7} {'d_min(Å)':>10} {'std':>6}")
    for c in ALL_COMPS:
        wmaxes, dmins = method_a_per_comp(d, c)
        if not wmaxes:
            continue
        wm = float(np.mean(wmaxes))
        ws = float(np.std(wmaxes))
        dm = float(np.mean(dmins))
        ds = float(np.std(dmins))
        summary[c] = (wm, ws, dm, ds)
        pe = PAPER_EXP.get(c, '—')
        print(f"  {c:<8} {str(pe):>10} {wm:>+10.3f} {ws:>7.3f} {dm:>10.3f} {ds:>6.3f}")

    csv_path = OUT_DIR / "energy_descriptor_summary.csv"
    with open(csv_path, 'w', encoding='utf-8') as f:
        f.write("comp,formula_short,paper_exp_Wad_mJ_m2,W_max_J_m2,W_max_std,d_min_A,d_min_std\n")
        for c in ALL_COMPS:
            if c not in summary:
                continue
            wm, ws, dm, ds = summary[c]
            pe = PAPER_EXP.get(c, '')
            f.write(f"{c},{LABELS_SHORT[c]},{pe},{wm:.4f},{ws:.4f},{dm:.3f},{ds:.3f}\n")
    print(f"\n  saved {csv_path}")

    # Bar chart 2-panel: paper exp + Method A W_max
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    comps_plot = [c for c in PAPER_COMPS if c in summary]
    x = np.arange(len(comps_plot))

    ax = axes[0]
    y_exp = [PAPER_EXP[c] for c in comps_plot]
    cols = [COLORS[c] for c in comps_plot]
    ax.bar(x, y_exp, color=cols, alpha=0.7, edgecolor='k', linewidth=0.8)
    for xi, yi in zip(x, y_exp):
        ax.text(xi, yi + 5, f'{yi}', ha='center', va='bottom', fontsize=10)
    ax.set_xticks(x)
    ax.set_xticklabels([LABELS_SHORT[c] for c in comps_plot], rotation=30, ha='right', fontsize=9)
    ax.set_ylabel(r'Experimental $W_{ad}$ (mJ/m$^2$)', fontsize=12)
    ax.set_title('(a) Paper experimental Wad', fontsize=11)
    ax.set_ylim(0, max(y_exp)*1.2)
    ax.grid(axis='y', alpha=0.3)

    ax = axes[1]
    y_calc = [summary[c][0] for c in comps_plot]
    e_calc = [summary[c][1] for c in comps_plot]
    ax.bar(x, y_calc, yerr=e_calc, color=cols, alpha=0.7, edgecolor='k',
           linewidth=0.8, capsize=5)
    for xi, yi, ei in zip(x, y_calc, e_calc):
        ax.text(xi, yi + ei + 0.05, f'{yi:.2f}', ha='center', va='bottom', fontsize=10)
    ax.set_xticks(x)
    ax.set_xticklabels([LABELS_SHORT[c] for c in comps_plot], rotation=30, ha='right', fontsize=9)
    ax.set_ylabel(r'Method A $W_{max}$ (J/m$^2$)', fontsize=12)
    ax.set_title('(b) Calculated W_max (UMA, mean ± std over 36 reg)', fontsize=11)
    ax.set_ylim(0, max(y_calc) + max(e_calc) + 0.5)
    ax.grid(axis='y', alpha=0.3)

    fig.suptitle('Adhesion energy descriptor — Method A reproduces paper exp ranking',
                 fontsize=11, y=1.00)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "energy_descriptor_bar.pdf", bbox_inches='tight')
    fig.savefig(OUT_DIR / "energy_descriptor_bar.png", bbox_inches='tight')
    plt.close()
    print(f"  saved energy_descriptor_bar.pdf/png")

    # Scatter W_max vs paper exp
    fig, ax = plt.subplots(figsize=(6, 5))
    x_calc = [summary[c][0] for c in comps_plot]
    y_exp = [PAPER_EXP[c] for c in comps_plot]
    R = float(np.corrcoef(x_calc, y_exp)[0, 1])
    for c in comps_plot:
        ax.errorbar(summary[c][0], PAPER_EXP[c], xerr=summary[c][1],
                    fmt='o', color=COLORS[c], markersize=12,
                    markeredgecolor='k', markeredgewidth=1, capsize=4,
                    ecolor=COLORS[c], elinewidth=1, alpha=0.85)
        ax.annotate(LABELS_SHORT[c], (summary[c][0], PAPER_EXP[c]),
                    xytext=(10, 5), textcoords='offset points', fontsize=9)
    coef = np.polyfit(x_calc, y_exp, 1)
    xfit = np.linspace(min(x_calc) - 0.1, max(x_calc) + 0.5, 50)
    ax.plot(xfit, np.polyval(coef, xfit), 'k--', lw=1, alpha=0.5,
            label=f'Linear fit (R = {R:+.3f})')
    if 'modelC' in summary:
        mc_w = summary['modelC'][0]
        mc_pred = float(np.polyval(coef, mc_w))
        ax.scatter([mc_w], [mc_pred], color=COLORS['modelC'], s=140, marker='^',
                   edgecolor='k', linewidth=1, zorder=5,
                   label=f'modelC pred: {mc_pred:.0f}')
        ax.annotate(f'modelC\npred={mc_pred:.0f}', (mc_w, mc_pred),
                    xytext=(10, -10), textcoords='offset points', fontsize=8)
    ax.set_xlabel(r'Method A $W_{max}$ (J/m$^2$)', fontsize=12)
    ax.set_ylabel(r'Paper exp $W_{ad}$ (mJ/m$^2$)', fontsize=12)
    ax.set_title('Energy descriptor vs experimental adhesion', fontsize=11)
    ax.legend(loc='lower right', fontsize=9)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "energy_descriptor_scatter.pdf", bbox_inches='tight')
    fig.savefig(OUT_DIR / "energy_descriptor_scatter.png", bbox_inches='tight')
    plt.close()
    print(f"  saved energy_descriptor_scatter.pdf/png  (R = {R:+.3f})")

    print(f"\nAll outputs in: {OUT_DIR.resolve()}")


if __name__ == "__main__":
    main()
