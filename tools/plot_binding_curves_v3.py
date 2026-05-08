"""Clean paper-ready binding curve plot (v3).

Lessons from v1/v2:
  - gap < 1.0 Å is atomic overlap region (repulsive wall, not binding well)
  - max-over-registry picks outlier values → noisy
  - Need: mean over registries, gap >= 1.0 Å only, asymptote-subtracted

Output:
  binding_curves_paper.pdf/png   ← THE final paper figure
  TMD-style sign convention (negative adhesion energy = binding favorable)
  comp colors by family + dashed for modelC

Usage:
  cd /mnt/c/Users/안용훈/Downloads/paper2_data
  python3 plot_binding_curves_v3.py
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

# Skip atomic-overlap gaps. Real binding well starts ~1.0 A.
GAP_MIN_PLOT = 1.0
GAP_MAX_PLOT = 4.0
GAP_ASYMPTOTE_MIN = 3.0  # gaps >= 3.0 used for asymptote estimate

COLORS = {
    'comp1':  '#1f77b4',  'comp2':  '#5b9bd5',
    'comp3':  '#c0392b',  'comp4':  '#e74c3c', 'comp5':  '#f1948a',
    'modelC': '#f39c12',
}
LINESTYLES = {
    'comp1':  '-', 'comp2':  '-',
    'comp3':  '-', 'comp4':  '-', 'comp5':  '-',
    'modelC': '--',
}
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


def main():
    # USE MEAN OVER REGISTRIES (smoother than max)
    gaps, mean_cols = read_csv_data(CSV_DIR / "binding_UMA_Wad_mean_J_m2.csv")
    if gaps is None:
        print("Run extract_phase1_binding_csv.py first.")
        return

    # Asymptote per comp (Wad at gap >= 3.0 A)
    mask_asym = gaps >= GAP_ASYMPTOTE_MIN
    asymptotes = {}
    for c in ALL_COMPS:
        if c not in mean_cols:
            continue
        asymptotes[c] = float(np.nanmean(mean_cols[c][mask_asym]))

    # Trim to plot range (gap >= 1.0)
    mask_plot = (gaps >= GAP_MIN_PLOT) & (gaps <= GAP_MAX_PLOT)
    gaps_plot = gaps[mask_plot]

    # ── Figure: TMD-style adhesion energy (clean paper version) ──
    fig, ax = plt.subplots(figsize=(8, 5.5))
    for c in ALL_COMPS:
        if c not in mean_cols:
            continue
        # Adhesion energy = -(Wad - asymptote)
        wad = mean_cols[c][mask_plot] - asymptotes[c]
        adh = -wad  # TMD convention: negative = binding favorable
        valid = ~np.isnan(adh)
        ax.plot(gaps_plot[valid], adh[valid],
                color=COLORS[c], linestyle=LINESTYLES[c], lw=2.0,
                marker='o', markersize=4,
                label=LABELS[c])
        # Mark minimum (deepest well = most binding favorable)
        if valid.any():
            i_min = int(np.nanargmin(adh))
            ax.scatter([gaps_plot[i_min]], [adh[i_min]],
                       color=COLORS[c], s=140, zorder=10,
                       edgecolor='k', linewidth=1.2)

    # gap_eq band
    ax.axvspan(1.2, 1.6, color='gray', alpha=0.10, zorder=0,
               label=r'g$_{eq}$ region (1.2-1.6 Å)')
    ax.axhline(0, color='k', linewidth=0.5, alpha=0.5)
    ax.set_xlabel('Interface gap, $d$ (Å)', fontsize=12)
    ax.set_ylabel('Adhesion energy (J/m$^2$)', fontsize=12)
    ax.set_title('UMA SE/NCM binding curves\n'
                 '(mean over 36 xy-shifts, asymptote-subtracted, TMD sign convention)',
                 fontsize=11)
    ax.set_xlim(GAP_MIN_PLOT, GAP_MAX_PLOT)
    ax.legend(loc='lower right', fontsize=9, framealpha=0.95)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "binding_curves_paper.pdf", bbox_inches='tight')
    fig.savefig(OUT_DIR / "binding_curves_paper.png", bbox_inches='tight')
    plt.close()
    print(f"  saved binding_curves_paper.pdf/png")

    # ── Same data, alternative sign (positive Wad) ──
    fig, ax = plt.subplots(figsize=(8, 5.5))
    for c in ALL_COMPS:
        if c not in mean_cols:
            continue
        wad = mean_cols[c][mask_plot] - asymptotes[c]
        valid = ~np.isnan(wad)
        ax.plot(gaps_plot[valid], wad[valid],
                color=COLORS[c], linestyle=LINESTYLES[c], lw=2.0,
                marker='o', markersize=4,
                label=LABELS[c])
        if valid.any():
            i_max = int(np.nanargmax(wad))
            ax.scatter([gaps_plot[i_max]], [wad[i_max]],
                       color=COLORS[c], s=140, zorder=10,
                       edgecolor='k', linewidth=1.2)

    ax.axvspan(1.2, 1.6, color='gray', alpha=0.10, zorder=0,
               label=r'g$_{eq}$ region (1.2-1.6 Å)')
    ax.axhline(0, color='k', linewidth=0.5, alpha=0.5)
    ax.set_xlabel('Interface gap, $d$ (Å)', fontsize=12)
    ax.set_ylabel(r'$W_{ad}$ (J/m$^2$, asymptote-subtracted)', fontsize=12)
    ax.set_title('UMA SE/NCM binding curves\n'
                 '(positive = binding favorable, mean over 36 xy-shifts)',
                 fontsize=11)
    ax.set_xlim(GAP_MIN_PLOT, GAP_MAX_PLOT)
    ax.legend(loc='upper right', fontsize=9, framealpha=0.95)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "binding_curves_paper_positive.pdf", bbox_inches='tight')
    fig.savefig(OUT_DIR / "binding_curves_paper_positive.png", bbox_inches='tight')
    plt.close()
    print(f"  saved binding_curves_paper_positive.pdf/png")

    # ── Print per-comp summary ──
    print("\n--- Per-comp (gap 1.0-4.0 Å, asymptote-subtracted) ---")
    print(f"{'comp':<8} {'asym(J/m²)':>12} {'depth (J/m²)':>14} {'d_eq (Å)':>10}")
    for c in ALL_COMPS:
        if c not in mean_cols:
            continue
        wad = mean_cols[c][mask_plot] - asymptotes[c]
        if np.all(np.isnan(wad)):
            continue
        i_max = int(np.nanargmax(wad))
        depth = float(wad[i_max])
        d_eq = float(gaps_plot[i_max])
        print(f"  {c:<8} {asymptotes[c]:>+12.3f} {depth:>+14.3f} {d_eq:>10.2f}")

    print(f"\nAll plots in: {OUT_DIR.resolve()}")


if __name__ == "__main__":
    main()
