"""Phase 2a v4 — TMD-reference-style binding curves + matching CSV.

⚠️ DEPRECATED 2026-05-11 — produces image 1 anomaly (Y range -3..+2.5,
modelC included, curves not converging at d=4). Use plot_binding_curves_v7.py
for image-2 paper style. Reasons:
  - line 97 reads MAX-over-registry CSV (binding_UMA_Wad_max_J_m2.csv) but
    title says "mean" (line 154) — misleading
  - max-over-registry exaggerates Y range (extreme values not averaged out)
  - includes modelC which paper figure (image 2) excludes
Kept for legacy reproducibility only.

Reference (WSe2/MoSe2 fig from user): smooth adhesion energy vs distance,
no big circle markers, multiple curves with small line markers, asymptote 0
at large d, deep well in middle. Per-line marker for distinction.

Our deviations from v3:
  - Remove big circle markers at d_min (user will style in Origin)
  - Use small markers per comp (different shapes for line distinction)
  - Cleaner axis range / labels
  - Output matching CSV `binding_curves_paper.csv` for direct Origin import

Output:
  binding_curves_paper.pdf/png    final paper figure (TMD-style, no circles)
  binding_curves_paper.csv        gap_A, adhesion_energy_J_m2 per comp

Usage:
  cd /mnt/c/Users/안용훈/Downloads/paper2_data
  wget -O plot_binding_curves_v4.py 'https://raw.../tools/plot_binding_curves_v4.py'
  python3 plot_binding_curves_v4.py
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

GAP_MIN_PLOT = 1.0
GAP_MAX_PLOT = 4.0
GAP_ASYMPTOTE_MIN = 3.0

# Colors: distinct per comp (avoid red-gradient overlap for comp3/4/5)
COLORS = {
    'comp1':  '#1f77b4',   # Li6 — blue
    'comp2':  '#17becf',   # Li6 — cyan
    'comp3':  '#d62728',   # Li5.4 Cl-rich — red
    'comp4':  '#9467bd',   # Li5.4 balanced — purple
    'comp5':  '#2ca02c',   # Li5.4 Br-rich — green
    'modelC': '#ff7f0e',   # Li5.4 Cl-only — orange
}
LINESTYLES = {
    'comp1':  '-', 'comp2':  '-',
    'comp3':  '-', 'comp4':  '-', 'comp5':  '-',
    'modelC': '--',
}
MARKERS = {
    'comp1':  's',     # square
    'comp2':  'o',     # circle
    'comp3':  '^',     # up-triangle
    'comp4':  'D',     # diamond
    'comp5':  'v',     # down-triangle
    'modelC': 'X',     # cross
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
    # USE MAX-OVER-REGISTRY (not mean): mean is dominated by unfavorable
    # Madelung at random registries, giving inverted ranking vs paper exp.
    # Max-over-registry picks the BEST binding configuration per (gap, comp),
    # matching Method A protocol that gave R=+0.87 with paper exp.
    gaps, max_cols = read_csv_data(CSV_DIR / "binding_UMA_Wad_max_J_m2.csv")
    if gaps is None:
        print("Run extract_phase1_binding_csv.py first.")
        return
    mean_cols = max_cols  # use 'mean_cols' name for downstream compatibility

    mask_asym = gaps >= GAP_ASYMPTOTE_MIN
    asymptotes = {}
    for c in ALL_COMPS:
        if c in mean_cols:
            asymptotes[c] = float(np.nanmean(mean_cols[c][mask_asym]))

    mask_plot = (gaps >= GAP_MIN_PLOT) & (gaps <= GAP_MAX_PLOT)
    gaps_plot = gaps[mask_plot]

    # Compute adhesion energy (TMD convention) per comp
    adh_data = {}
    for c in ALL_COMPS:
        if c in mean_cols:
            wad = mean_cols[c][mask_plot] - asymptotes[c]
            adh_data[c] = -wad  # TMD: negative = binding favorable

    # ── Save CSV ──
    csv_path = OUT_DIR / "binding_curves_paper.csv"
    with open(csv_path, 'w', encoding='utf-8') as f:
        f.write("gap_A," + ",".join(ALL_COMPS) + "\n")
        f.write("# adhesion energy (J/m^2), TMD sign convention: "
                "negative = binding favorable\n")
        f.write("# mean over 36 xy-shift registries, asymptote subtracted "
                "(asymptote = mean of gap >= 3.0 A)\n")
        for i, g in enumerate(gaps_plot):
            row = [f"{g:.3f}"]
            for c in ALL_COMPS:
                v = adh_data.get(c, [None])[i] if c in adh_data else None
                row.append(f"{v:.6f}" if (v is not None and not np.isnan(v)) else "")
            f.write(",".join(row) + "\n")
    print(f"  saved {csv_path}")

    # ── Figure 1: TMD-style adhesion (negative = binding) ──
    fig, ax = plt.subplots(figsize=(8, 5.5))
    for c in ALL_COMPS:
        if c not in adh_data:
            continue
        adh = adh_data[c]
        valid = ~np.isnan(adh)
        ax.plot(gaps_plot[valid], adh[valid],
                color=COLORS[c],
                linestyle=LINESTYLES[c],
                lw=1.8,
                marker=MARKERS[c],
                markersize=5,
                markerfacecolor=COLORS[c],
                markeredgecolor=COLORS[c],
                label=LABELS[c])
    ax.axhline(0, color='k', linewidth=0.5, alpha=0.5)
    ax.set_xlabel('Interface gap, $d$ (Å)', fontsize=12)
    ax.set_ylabel('Adhesion energy (J/m$^2$)', fontsize=12)
    ax.set_title('SE/NCM binding curves (UMA, mean over 36 xy-shifts)',
                 fontsize=12)
    ax.set_xlim(GAP_MIN_PLOT, GAP_MAX_PLOT)
    ax.legend(loc='lower right', fontsize=9, framealpha=0.95)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "binding_curves_paper.pdf", bbox_inches='tight')
    fig.savefig(OUT_DIR / "binding_curves_paper.png", bbox_inches='tight')
    plt.close()
    print(f"  saved binding_curves_paper.pdf/png  (TMD-style)")

    # ── Figure 2: positive Wad (alternative) ──
    fig, ax = plt.subplots(figsize=(8, 5.5))
    for c in ALL_COMPS:
        if c not in adh_data:
            continue
        wad = -adh_data[c]
        valid = ~np.isnan(wad)
        ax.plot(gaps_plot[valid], wad[valid],
                color=COLORS[c],
                linestyle=LINESTYLES[c],
                lw=1.8,
                marker=MARKERS[c],
                markersize=5,
                markerfacecolor=COLORS[c],
                markeredgecolor=COLORS[c],
                label=LABELS[c])
    ax.axhline(0, color='k', linewidth=0.5, alpha=0.5)
    ax.set_xlabel('Interface gap, $d$ (Å)', fontsize=12)
    ax.set_ylabel(r'$W_{ad}$ (J/m$^2$)', fontsize=12)
    ax.set_title('SE/NCM binding curves (positive convention)', fontsize=12)
    ax.set_xlim(GAP_MIN_PLOT, GAP_MAX_PLOT)
    ax.legend(loc='upper right', fontsize=9, framealpha=0.95)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "binding_curves_paper_positive.pdf", bbox_inches='tight')
    fig.savefig(OUT_DIR / "binding_curves_paper_positive.png", bbox_inches='tight')
    plt.close()
    print(f"  saved binding_curves_paper_positive.pdf/png")

    # ── Per-comp summary print ──
    print("\n--- Per-comp (gap 1.0-4.0 A, asymptote-subtracted) ---")
    print(f"{'comp':<8} {'asym(J/m²)':>12} {'depth(J/m²)':>12} {'d_eq(Å)':>10}")
    for c in ALL_COMPS:
        if c not in adh_data:
            continue
        adh = adh_data[c]
        if np.all(np.isnan(adh)):
            continue
        i_min = int(np.nanargmin(adh))
        depth = float(adh[i_min])  # most negative
        d_eq = float(gaps_plot[i_min])
        print(f"  {c:<8} {asymptotes[c]:>+12.3f} {depth:>+12.3f} {d_eq:>10.2f}")

    print(f"\nAll outputs in: {OUT_DIR.resolve()}")


if __name__ == "__main__":
    main()
