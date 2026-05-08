"""Plot UMA binding energy curves from extracted CSVs.

Reads binding_curves_csv/binding_UMA_Wad_*.csv and produces:
  binding_curves_main.pdf/png   (mean + std error band, paper figure)
  binding_curves_max.pdf/png    (max-over-registry, best W_max curves)
  binding_curves_R1.pdf/png     (single registry R1_origin, raw)
  binding_curves_4panel.pdf/png (master 4-panel: mean, max, R1, summary scatter)

Usage:
  cd /mnt/c/Users/안용훈/Downloads/paper2_data
  python3 plot_binding_curves.py

Style: 6 composition colors by family (Li6=blue tones, Li5.4=red tones,
modelC=orange). Equilibrium gap region (0.6-1.6 A) shaded.
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

# Family-based colors (paper-style)
COLORS = {
    'comp1':  '#1f77b4',   # Li6 family — blue
    'comp2':  '#5b9bd5',   # Li6 family — light blue
    'comp3':  '#c0392b',   # Li5.4 family — dark red
    'comp4':  '#e74c3c',   # Li5.4 family — red
    'comp5':  '#f1948a',   # Li5.4 family — light red
    'modelC': '#f39c12',   # Li5.4 + Cl-only — orange
}
LINESTYLES = {
    'comp1':  '-',
    'comp2':  '-',
    'comp3':  '-',
    'comp4':  '-',
    'comp5':  '-',
    'modelC': '--',  # Cl-only control: dashed
}
LABELS = {
    'comp1':  r'comp1: Li$_6$PS$_5$Cl',
    'comp2':  r'comp2: Li$_6$PS$_5$Cl$_{0.5}$Br$_{0.5}$',
    'comp3':  r'comp3: Li$_{5.4}$PS$_{4.4}$Cl$_{1.0}$Br$_{0.6}$',
    'comp4':  r'comp4: Li$_{5.4}$PS$_{4.4}$Cl$_{0.8}$Br$_{0.8}$',
    'comp5':  r'comp5: Li$_{5.4}$PS$_{4.4}$Cl$_{0.6}$Br$_{1.0}$',
    'modelC': r'modelC: Li$_{5.4}$PS$_{4.4}$Cl$_{1.6}$ (no Br)',
}
PAPER_EXP = {'comp1': 194, 'comp2': 180, 'comp3': 316, 'comp4': 298, 'comp5': 249}

# Matplotlib paper style
plt.rcParams.update({
    'font.size': 10,
    'axes.labelsize': 11,
    'axes.titlesize': 11,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 8,
    'figure.dpi': 150,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
})


def read_csv(path):
    """Read CSV → {gap_arr, comp1_arr, ...}."""
    if not path.exists():
        print(f"  MISSING: {path}")
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


def fig_mean_with_std():
    """Mean Wad ± std curves per comp."""
    gaps, mean_cols = read_csv(CSV_DIR / "binding_UMA_Wad_mean_J_m2.csv")
    _, std_cols = read_csv(CSV_DIR / "binding_UMA_Wad_std_J_m2.csv")
    if gaps is None:
        return

    fig, ax = plt.subplots(figsize=(8, 5))
    for c in ALL_COMPS:
        if c not in mean_cols:
            continue
        m = mean_cols[c]
        s = std_cols[c] if std_cols and c in std_cols else np.zeros_like(m)
        valid = ~np.isnan(m)
        ax.plot(gaps[valid], m[valid],
                color=COLORS[c], linestyle=LINESTYLES[c], lw=1.8,
                label=LABELS[c])
        ax.fill_between(gaps[valid], m[valid] - s[valid], m[valid] + s[valid],
                         color=COLORS[c], alpha=0.18, linewidth=0)

    # Equilibrium gap region
    ax.axvspan(0.6, 1.6, color='gray', alpha=0.10, zorder=0,
               label='gap_eq region')
    ax.axhline(0, color='k', linewidth=0.5, alpha=0.4)
    ax.set_xlabel('Interface gap (Å)')
    ax.set_ylabel(r'W$_{ad}$ (J/m$^2$, mean over 36 registries)')
    ax.set_title('UMA binding energy curves — mean ± std (n=36 xy-shifts)')
    ax.set_xlim(0.5, 4.0)
    ax.legend(loc='lower right', fontsize=7.5)
    ax.grid(True, alpha=0.3)
    fig.savefig(OUT_DIR / "binding_curves_main.pdf", bbox_inches='tight')
    fig.savefig(OUT_DIR / "binding_curves_main.png", bbox_inches='tight')
    plt.close()
    print(f"  saved binding_curves_main.pdf/png")


def fig_max():
    """Max over registries per gap (best W_max curve)."""
    gaps, max_cols = read_csv(CSV_DIR / "binding_UMA_Wad_max_J_m2.csv")
    if gaps is None:
        return

    fig, ax = plt.subplots(figsize=(8, 5))
    for c in ALL_COMPS:
        if c not in max_cols:
            continue
        m = max_cols[c]
        valid = ~np.isnan(m)
        ax.plot(gaps[valid], m[valid],
                color=COLORS[c], linestyle=LINESTYLES[c], lw=1.8,
                marker='o', markersize=3,
                label=LABELS[c])
        # Mark d_min (max position)
        i_max = int(np.nanargmax(m))
        ax.scatter([gaps[i_max]], [m[i_max]],
                   color=COLORS[c], s=120, zorder=10,
                   edgecolor='k', linewidth=1.0)
        ax.annotate(f"{m[i_max]:+.2f}",
                    (gaps[i_max], m[i_max]),
                    xytext=(8, 8), textcoords='offset points',
                    fontsize=8, color=COLORS[c], fontweight='bold')

    ax.axvspan(0.6, 1.6, color='gray', alpha=0.10, zorder=0)
    ax.axhline(0, color='k', linewidth=0.5, alpha=0.4)
    ax.set_xlabel('Interface gap (Å)')
    ax.set_ylabel(r'W$_{ad}$ max-over-registry (J/m$^2$)')
    ax.set_title('UMA binding curves — max over 36 registries (best xy-shift per gap)')
    ax.set_xlim(0.5, 4.0)
    ax.legend(loc='upper right', fontsize=7.5)
    ax.grid(True, alpha=0.3)
    fig.savefig(OUT_DIR / "binding_curves_max.pdf", bbox_inches='tight')
    fig.savefig(OUT_DIR / "binding_curves_max.png", bbox_inches='tight')
    plt.close()
    print(f"  saved binding_curves_max.pdf/png")


def fig_R1origin():
    """Single registry R1_origin curves (raw, no averaging)."""
    gaps, r1_cols = read_csv(CSV_DIR / "binding_UMA_Wad_R1origin_J_m2.csv")
    if gaps is None:
        return

    fig, ax = plt.subplots(figsize=(8, 5))
    for c in ALL_COMPS:
        if c not in r1_cols:
            continue
        m = r1_cols[c]
        valid = ~np.isnan(m)
        ax.plot(gaps[valid], m[valid],
                color=COLORS[c], linestyle=LINESTYLES[c], lw=1.8,
                marker='s', markersize=3,
                label=LABELS[c])

    ax.axvspan(0.6, 1.6, color='gray', alpha=0.10, zorder=0)
    ax.axhline(0, color='k', linewidth=0.5, alpha=0.4)
    ax.set_xlabel('Interface gap (Å)')
    ax.set_ylabel(r'W$_{ad}$ at R1_origin (J/m$^2$)')
    ax.set_title('UMA binding curves — single registry (R1_origin, raw)')
    ax.set_xlim(0.5, 4.0)
    ax.legend(loc='lower right', fontsize=7.5)
    ax.grid(True, alpha=0.3)
    fig.savefig(OUT_DIR / "binding_curves_R1.pdf", bbox_inches='tight')
    fig.savefig(OUT_DIR / "binding_curves_R1.png", bbox_inches='tight')
    plt.close()
    print(f"  saved binding_curves_R1.pdf/png")


def fig_4panel():
    """Master 4-panel summary figure."""
    gaps, mean_cols = read_csv(CSV_DIR / "binding_UMA_Wad_mean_J_m2.csv")
    _, std_cols = read_csv(CSV_DIR / "binding_UMA_Wad_std_J_m2.csv")
    _, max_cols = read_csv(CSV_DIR / "binding_UMA_Wad_max_J_m2.csv")
    _, r1_cols = read_csv(CSV_DIR / "binding_UMA_Wad_R1origin_J_m2.csv")
    if gaps is None:
        return

    fig, axes = plt.subplots(2, 2, figsize=(13, 9))

    # (a) Mean ± std
    ax = axes[0, 0]
    for c in ALL_COMPS:
        if c not in mean_cols: continue
        m = mean_cols[c]; s = std_cols.get(c, np.zeros_like(m)) if std_cols else np.zeros_like(m)
        valid = ~np.isnan(m)
        ax.plot(gaps[valid], m[valid], color=COLORS[c],
                linestyle=LINESTYLES[c], lw=1.6, label=c)
        ax.fill_between(gaps[valid], m[valid]-s[valid], m[valid]+s[valid],
                         color=COLORS[c], alpha=0.18, linewidth=0)
    ax.axvspan(0.6, 1.6, color='gray', alpha=0.10, zorder=0)
    ax.axhline(0, color='k', linewidth=0.5, alpha=0.4)
    ax.set_xlabel('gap (Å)'); ax.set_ylabel(r'W$_{ad}$ mean±std (J/m$^2$)')
    ax.set_title('(a) Mean over 36 registries')
    ax.set_xlim(0.5, 4.0); ax.legend(fontsize=7.5, loc='lower right')
    ax.grid(True, alpha=0.3)

    # (b) Max-over-registry
    ax = axes[0, 1]
    for c in ALL_COMPS:
        if c not in max_cols: continue
        m = max_cols[c]; valid = ~np.isnan(m)
        ax.plot(gaps[valid], m[valid], color=COLORS[c],
                linestyle=LINESTYLES[c], lw=1.6, marker='o', markersize=3, label=c)
    ax.axvspan(0.6, 1.6, color='gray', alpha=0.10, zorder=0)
    ax.axhline(0, color='k', linewidth=0.5, alpha=0.4)
    ax.set_xlabel('gap (Å)'); ax.set_ylabel(r'W$_{ad}$ max-over-reg (J/m$^2$)')
    ax.set_title('(b) Max over 36 registries (best W$_{max}$)')
    ax.set_xlim(0.5, 4.0); ax.legend(fontsize=7.5, loc='upper right')
    ax.grid(True, alpha=0.3)

    # (c) R1_origin
    ax = axes[1, 0]
    for c in ALL_COMPS:
        if c not in r1_cols: continue
        m = r1_cols[c]; valid = ~np.isnan(m)
        ax.plot(gaps[valid], m[valid], color=COLORS[c],
                linestyle=LINESTYLES[c], lw=1.6, marker='s', markersize=3, label=c)
    ax.axvspan(0.6, 1.6, color='gray', alpha=0.10, zorder=0)
    ax.axhline(0, color='k', linewidth=0.5, alpha=0.4)
    ax.set_xlabel('gap (Å)'); ax.set_ylabel(r'W$_{ad}$ R1_origin (J/m$^2$)')
    ax.set_title('(c) Single registry (raw)')
    ax.set_xlim(0.5, 4.0); ax.legend(fontsize=7.5, loc='lower right')
    ax.grid(True, alpha=0.3)

    # (d) W_max scatter vs paper exp
    ax = axes[1, 1]
    if max_cols:
        wmax = {}
        d_min = {}
        for c in ALL_COMPS:
            if c not in max_cols: continue
            m = max_cols[c]
            i_max = int(np.nanargmax(m))
            wmax[c] = float(m[i_max])
            d_min[c] = float(gaps[i_max])
        x = [wmax[c] for c in PAPER_EXP if c in wmax]
        y = [PAPER_EXP[c] for c in PAPER_EXP if c in wmax]
        if x and y:
            for c in PAPER_EXP:
                if c not in wmax: continue
                ax.scatter(wmax[c], PAPER_EXP[c], color=COLORS[c], s=130,
                           edgecolor='k', linewidth=1.0, zorder=10)
                ax.annotate(c, (wmax[c], PAPER_EXP[c]), xytext=(8, 6),
                            textcoords='offset points', fontsize=9)
            if 'modelC' in wmax:
                ax.scatter(wmax['modelC'], 0, color=COLORS['modelC'], s=130,
                           marker='^', edgecolor='k', linewidth=1.0)
                ax.annotate('modelC', (wmax['modelC'], 0), xytext=(8, -14),
                            textcoords='offset points', fontsize=9)
            R = float(np.corrcoef(x, y)[0, 1])
            coef = np.polyfit(x, y, 1)
            xfit = np.linspace(min(x)-0.5, max(wmax.values())+0.5, 50)
            ax.plot(xfit, np.polyval(coef, xfit), 'k--', lw=1, alpha=0.5,
                    label=f'R = {R:+.3f}')
    ax.set_xlabel(r'UMA W$_{max}$ (J/m$^2$, max over reg/gap)')
    ax.set_ylabel(r'Paper exp W$_{ad}$ (mJ/m$^2$)')
    ax.set_title('(d) W$_{max}$ vs paper exp')
    ax.legend(fontsize=8, loc='upper left')
    ax.grid(True, alpha=0.3)

    fig.suptitle('UMA Phase 1 binding curves — paper #2 supplementary figure',
                 fontsize=12, y=1.01)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "binding_curves_4panel.pdf", bbox_inches='tight')
    fig.savefig(OUT_DIR / "binding_curves_4panel.png", bbox_inches='tight')
    plt.close()
    print(f"  saved binding_curves_4panel.pdf/png")


def main():
    print("=" * 60)
    print("Plotting UMA binding curves")
    print("=" * 60)
    fig_mean_with_std()
    fig_max()
    fig_R1origin()
    fig_4panel()
    print(f"\nAll plots in: {OUT_DIR.resolve()}")


if __name__ == "__main__":
    main()
