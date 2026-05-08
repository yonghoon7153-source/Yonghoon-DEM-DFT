"""Phase 2a v6 — RAW binding curves (no asymptote subtraction).

Honest treatment: do not normalize asymptote. Different per-comp baselines
reflect cell-rescaling Madelung artifact, but RANKING in absolute Wad space
matches paper exp (Method A R=+0.87). For SI figure with caveat.

Output:
  binding_curves_v6_raw.pdf/png   raw max-over-reg Wad, no normalization
  binding_curves_v6_zoom.pdf/png  zoomed to well region (gap 0.8-2.0)
  binding_curves_v6_raw.csv       gap_A + raw Wad per comp
"""
import csv
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

CSV_DIR = Path("binding_curves_csv")
OUT_DIR = Path("binding_curves_plots"); OUT_DIR.mkdir(exist_ok=True)
ALL_COMPS = ['comp1', 'comp2', 'comp3', 'comp4', 'comp5', 'modelC']
PAPER_EXP = {'comp1': 194, 'comp2': 180, 'comp3': 316, 'comp4': 298, 'comp5': 249}

COLORS = {
    'comp1':  '#1f77b4',  'comp2':  '#17becf',
    'comp3':  '#d62728',  'comp4':  '#9467bd', 'comp5':  '#2ca02c',
    'modelC': '#ff7f0e',
}
LINESTYLES = {'comp1':'-', 'comp2':'-', 'comp3':'-', 'comp4':'-', 'comp5':'-', 'modelC':'--'}
MARKERS = {'comp1':'s', 'comp2':'o', 'comp3':'^', 'comp4':'D', 'comp5':'v', 'modelC':'X'}
LABELS = {
    'comp1':  r'comp1: Li$_6$PS$_5$Cl',
    'comp2':  r'comp2: Li$_6$PS$_5$Cl$_{0.5}$Br$_{0.5}$',
    'comp3':  r'comp3: Li$_{5.4}$PS$_{4.4}$Cl$_{1.0}$Br$_{0.6}$',
    'comp4':  r'comp4: Li$_{5.4}$PS$_{4.4}$Cl$_{0.8}$Br$_{0.8}$',
    'comp5':  r'comp5: Li$_{5.4}$PS$_{4.4}$Cl$_{0.6}$Br$_{1.0}$',
    'modelC': r'modelC: Li$_{5.4}$PS$_{4.4}$Cl$_{1.6}$ (no Br)',
}

plt.rcParams.update({
    'font.size': 11, 'axes.labelsize': 12, 'axes.titlesize': 12,
    'xtick.labelsize': 10, 'ytick.labelsize': 10, 'legend.fontsize': 9,
    'figure.dpi': 150, 'savefig.dpi': 300, 'savefig.bbox': 'tight',
})


def read_csv_data(path):
    if not path.exists():
        return None, None
    rows = list(csv.reader(open(path)))
    header = rows[0]
    data = rows[1:]
    gaps = np.array([float(r[0]) for r in data])
    cols = {}
    for i, name in enumerate(header[1:], 1):
        try:
            cols[name] = np.array([float(r[i]) if r[i] else np.nan for r in data])
        except Exception:
            cols[name] = np.array([np.nan] * len(data))
    return gaps, cols


def plot(gaps, cols, gap_min, gap_max, ylabel, title, suffix, mark_max=True):
    fig, ax = plt.subplots(figsize=(8, 5.5))
    mask = (gaps >= gap_min) & (gaps <= gap_max)
    g = gaps[mask]
    for c in ALL_COMPS:
        if c not in cols:
            continue
        y = cols[c][mask]
        valid = ~np.isnan(y)
        ax.plot(g[valid], y[valid], color=COLORS[c],
                linestyle=LINESTYLES[c], lw=1.8,
                marker=MARKERS[c], markersize=5,
                markerfacecolor=COLORS[c], markeredgecolor=COLORS[c],
                label=LABELS[c])
        if mark_max and valid.any():
            i_max = int(np.nanargmax(y))
            ax.scatter([g[i_max]], [y[i_max]],
                       color=COLORS[c], s=120, zorder=10,
                       edgecolor='k', linewidth=1.0)
            ax.annotate(f"{y[i_max]:+.2f}",
                        (g[i_max], y[i_max]),
                        xytext=(8, 8), textcoords='offset points',
                        fontsize=8, color=COLORS[c], fontweight='bold')
    ax.axhline(0, color='k', linewidth=0.5, alpha=0.5)
    ax.set_xlabel('Interface gap, $d$ (Å)', fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.set_title(title, fontsize=11)
    ax.set_xlim(gap_min, gap_max)
    ax.legend(loc='best', fontsize=9, framealpha=0.95)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUT_DIR / f"binding_curves_v6_{suffix}.pdf", bbox_inches='tight')
    fig.savefig(OUT_DIR / f"binding_curves_v6_{suffix}.png", bbox_inches='tight')
    plt.close()
    print(f"  saved binding_curves_v6_{suffix}.pdf/png")


def main():
    gaps, max_cols = read_csv_data(CSV_DIR / "binding_UMA_Wad_max_J_m2.csv")
    if gaps is None:
        print("Run extract_phase1_binding_csv.py first.")
        return

    # Save CSV (raw, no transformation)
    csv_path = OUT_DIR / "binding_curves_v6_raw.csv"
    with open(csv_path, 'w', encoding='utf-8') as f:
        f.write("# RAW max-over-36-reg Wad (J/m^2). NO asymptote subtraction.\n")
        f.write("# Different per-comp asymptotes reflect cell-rescaling Madelung\n")
        f.write("# artifact. Ranking at peak still correlates with paper exp Wad\n")
        f.write("# (Method A R=+0.87).\n")
        f.write("gap_A," + ",".join(ALL_COMPS) + "\n")
        for i, g in enumerate(gaps):
            row = [f"{g:.3f}"]
            for c in ALL_COMPS:
                v = max_cols.get(c, [np.nan]*len(gaps))[i]
                row.append(f"{v:.6f}" if not np.isnan(v) else "")
            f.write(",".join(row) + "\n")
    print(f"  saved {csv_path}")

    # Full range plot
    plot(gaps, max_cols, 0.6, 4.0,
         r'$W_{ad}$ max-over-registry (J/m$^2$)',
         'Raw binding curves (max over 36 xy-shifts, no normalization)',
         'raw', mark_max=True)

    # Zoomed to well region
    plot(gaps, max_cols, 0.8, 2.5,
         r'$W_{ad}$ max-over-registry (J/m$^2$)',
         'Binding well region — paper #2 SI figure',
         'zoom', mark_max=True)

    # Print summary
    print("\n--- Per-comp max W_ad and d_min (no normalization) ---")
    print(f"{'comp':<8} {'paper exp':>10} {'W_max':>10} {'d_min(Å)':>10}")
    for c in ALL_COMPS:
        if c not in max_cols:
            continue
        m = max_cols[c]
        valid = ~np.isnan(m)
        if not valid.any():
            continue
        i_max = int(np.nanargmax(m))
        wm = float(m[i_max])
        dm = float(gaps[i_max])
        pe = PAPER_EXP.get(c, '—')
        print(f"  {c:<8} {str(pe):>10} {wm:>+10.3f} {dm:>10.2f}")

    print(f"\nAll outputs in: {OUT_DIR.resolve()}")


if __name__ == "__main__":
    main()
