"""Phase 2a v5 — correctly-normalized binding curves.

KEY FIX: per-registry asymptote subtraction.

v3/v4 used comp-level mean asymptote, which made comp1 (Li6, big Madelung
artifact) appear to have deepest well — opposite of paper exp ranking.

Correct method (matches Method A protocol):
  1. For each (comp, registry):
     - asymptote(reg) = mean Wad over gap >= 3.0 A
     - well_curve(reg, gap) = Wad(reg, gap) - asymptote(reg)
       → each registry's curve is normalized to 0 at large gap
  2. Mean over 36 registries: <well_curve>(gap)
  3. Plot mean curve per comp

This isolates BINDING WELL from cell-rescaling Madelung artifact.
W_max (mean over reg of per-reg max) reproduces Method A db (R=+0.87 with
paper exp).

Usage:
  cd /mnt/c/Users/안용훈/Downloads/paper2_data
  wget -O plot_binding_curves_v5.py 'https://raw.../tools/plot_binding_curves_v5.py'
  python3 plot_binding_curves_v5.py
"""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import statistics

OUT_DIR = Path("binding_curves_plots"); OUT_DIR.mkdir(exist_ok=True)
PATH_BIND = Path("phase1_results/binding_curves.json")

ALL_COMPS = ['comp1', 'comp2', 'comp3', 'comp4', 'comp5', 'modelC']
GAP_MIN_PLOT = 0.8
GAP_MAX_PLOT = 4.0
GAP_ASYMPTOTE_MIN = 3.0

COLORS = {
    'comp1':  '#1f77b4',  'comp2':  '#17becf',
    'comp3':  '#d62728',  'comp4':  '#9467bd', 'comp5':  '#2ca02c',
    'modelC': '#ff7f0e',
}
LINESTYLES = {
    'comp1':  '-', 'comp2':  '-',
    'comp3':  '-', 'comp4':  '-', 'comp5':  '-',
    'modelC': '--',
}
MARKERS = {
    'comp1':  's', 'comp2':  'o',
    'comp3':  '^', 'comp4':  'D', 'comp5':  'v',
    'modelC': 'X',
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


def per_registry_normalized(d, comp):
    """Returns dict: gap_str -> list of normalized Wad over registries.

    For each registry:
      asymptote(reg) = mean Wad at gap >= 3.0
      normalized(reg, gap) = Wad(reg, gap) - asymptote(reg)
    """
    if comp not in d:
        return {}, {}
    comp_data = d[comp]
    # First pass: collect all gap_str across all registries
    gap_set = set()
    for reg, reg_data in comp_data.items():
        gap_set.update(reg_data.get('curve', {}).keys())
    gaps = sorted(gap_set, key=float)

    # Per-registry asymptote
    per_reg_asym = {}
    for reg, reg_data in comp_data.items():
        curve = reg_data.get('curve', {})
        asym_vals = []
        for gap_str in gaps:
            if gap_str in curve and float(gap_str) >= GAP_ASYMPTOTE_MIN:
                w = curve[gap_str].get('Wad_J_per_m2')
                if w is not None:
                    asym_vals.append(w)
        per_reg_asym[reg] = np.mean(asym_vals) if asym_vals else 0.0

    # Per-gap collection of normalized values
    norm_per_gap = {gap_str: [] for gap_str in gaps}
    for reg, reg_data in comp_data.items():
        curve = reg_data.get('curve', {})
        asym = per_reg_asym[reg]
        for gap_str in gaps:
            if gap_str in curve:
                w = curve[gap_str].get('Wad_J_per_m2')
                if w is not None:
                    norm_per_gap[gap_str].append(w - asym)
    return gaps, norm_per_gap


def per_registry_wmax(d, comp):
    """For each registry, find max Wad over gap (well peak above asymptote)."""
    if comp not in d:
        return [], []
    comp_data = d[comp]
    wmax_list = []
    dmin_list = []
    for reg, reg_data in comp_data.items():
        curve = reg_data.get('curve', {})
        # Per-reg asymptote
        asym_vals = [v.get('Wad_J_per_m2') for g, v in curve.items()
                     if float(g) >= GAP_ASYMPTOTE_MIN and v.get('Wad_J_per_m2') is not None]
        if not asym_vals:
            continue
        asym = np.mean(asym_vals)
        # Per-reg max Wad and gap
        best_w = -np.inf
        best_g = None
        for g, v in curve.items():
            w = v.get('Wad_J_per_m2')
            if w is None:
                continue
            w_norm = w - asym
            if w_norm > best_w:
                best_w = w_norm
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

    # Per-comp processing
    print("Per-comp Method-A-style W_max (mean over per-reg max above asymptote):")
    print(f"{'comp':<8} {'W_max(J/m²)':>14} {'std':>8} {'d_min(Å)':>10} {'std':>6}")
    method_a_repro = {}
    for c in ALL_COMPS:
        wmaxes, dmins = per_registry_wmax(d, c)
        if not wmaxes:
            continue
        wm = float(np.mean(wmaxes))
        ws = float(np.std(wmaxes))
        dm = float(np.mean(dmins))
        ds = float(np.std(dmins))
        method_a_repro[c] = {'W_max': wm, 'W_max_std': ws,
                              'd_min': dm, 'd_min_std': ds}
        print(f"  {c:<8} {wm:>+14.4f} {ws:>8.3f} {dm:>10.3f} {ds:>6.3f}")

    # Per-gap mean curves
    curves = {}  # comp -> (gaps, mean, std)
    for c in ALL_COMPS:
        gaps_str, norm_per_gap = per_registry_normalized(d, c)
        if not gaps_str:
            continue
        gaps = np.array([float(g) for g in gaps_str])
        means = np.array([np.mean(norm_per_gap[g]) if norm_per_gap[g] else np.nan
                          for g in gaps_str])
        stds = np.array([np.std(norm_per_gap[g]) if len(norm_per_gap[g]) > 1 else 0.0
                         for g in gaps_str])
        curves[c] = (gaps, means, stds)

    # Save CSV
    csv_path = OUT_DIR / "binding_curves_v5_paper.csv"
    # Find common gap axis
    all_gaps = sorted(set().union(*[set(c[0].tolist()) for c in curves.values()]))
    with open(csv_path, 'w', encoding='utf-8') as f:
        f.write("# Per-registry asymptote-subtracted Wad, mean over 36 registries\n")
        f.write("# Wad > 0 = binding favorable above asymptote\n")
        f.write("# adh = -Wad (TMD convention: negative = binding favorable)\n")
        f.write("gap_A," + ",".join(f"{c}_Wad" for c in ALL_COMPS) +
                "," + ",".join(f"{c}_adh" for c in ALL_COMPS) + "\n")
        for g in all_gaps:
            row = [f"{g:.3f}"]
            wads = []
            for c in ALL_COMPS:
                if c not in curves:
                    row.append("")
                    wads.append(None)
                    continue
                gaps_arr = curves[c][0]
                means_arr = curves[c][1]
                idx = np.where(np.abs(gaps_arr - g) < 1e-6)[0]
                if len(idx) > 0 and not np.isnan(means_arr[idx[0]]):
                    val = means_arr[idx[0]]
                    row.append(f"{val:.6f}")
                    wads.append(val)
                else:
                    row.append("")
                    wads.append(None)
            for w in wads:
                row.append(f"{-w:.6f}" if w is not None else "")
            f.write(",".join(row) + "\n")
    print(f"\n  saved {csv_path}")

    # ── Figure (TMD style: adhesion energy, negative = binding) ──
    fig, ax = plt.subplots(figsize=(8, 5.5))
    for c in ALL_COMPS:
        if c not in curves:
            continue
        gaps_arr, means, stds = curves[c]
        mask = (gaps_arr >= GAP_MIN_PLOT) & (gaps_arr <= GAP_MAX_PLOT)
        adh = -means[mask]
        valid = ~np.isnan(adh)
        ax.plot(gaps_arr[mask][valid], adh[valid],
                color=COLORS[c], linestyle=LINESTYLES[c], lw=1.8,
                marker=MARKERS[c], markersize=5,
                markerfacecolor=COLORS[c], markeredgecolor=COLORS[c],
                label=LABELS[c])
    ax.axhline(0, color='k', linewidth=0.5, alpha=0.5)
    ax.set_xlabel('Interface gap, $d$ (Å)', fontsize=12)
    ax.set_ylabel('Adhesion energy (J/m$^2$)', fontsize=12)
    ax.set_title('SE/NCM binding curves (UMA Phase 1, per-registry normalized)',
                 fontsize=11)
    ax.set_xlim(GAP_MIN_PLOT, GAP_MAX_PLOT)
    ax.legend(loc='lower right', fontsize=9, framealpha=0.95)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "binding_curves_v5_paper.pdf", bbox_inches='tight')
    fig.savefig(OUT_DIR / "binding_curves_v5_paper.png", bbox_inches='tight')
    plt.close()
    print(f"  saved binding_curves_v5_paper.pdf/png")

    # ── Figure (positive Wad alternative) ──
    fig, ax = plt.subplots(figsize=(8, 5.5))
    for c in ALL_COMPS:
        if c not in curves:
            continue
        gaps_arr, means, stds = curves[c]
        mask = (gaps_arr >= GAP_MIN_PLOT) & (gaps_arr <= GAP_MAX_PLOT)
        wad = means[mask]
        valid = ~np.isnan(wad)
        ax.plot(gaps_arr[mask][valid], wad[valid],
                color=COLORS[c], linestyle=LINESTYLES[c], lw=1.8,
                marker=MARKERS[c], markersize=5,
                markerfacecolor=COLORS[c], markeredgecolor=COLORS[c],
                label=LABELS[c])
    ax.axhline(0, color='k', linewidth=0.5, alpha=0.5)
    ax.set_xlabel('Interface gap, $d$ (Å)', fontsize=12)
    ax.set_ylabel(r'$W_{ad}$ above asymptote (J/m$^2$)', fontsize=12)
    ax.set_title('SE/NCM binding curves — positive convention', fontsize=11)
    ax.set_xlim(GAP_MIN_PLOT, GAP_MAX_PLOT)
    ax.legend(loc='upper right', fontsize=9, framealpha=0.95)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "binding_curves_v5_paper_positive.pdf", bbox_inches='tight')
    fig.savefig(OUT_DIR / "binding_curves_v5_paper_positive.png", bbox_inches='tight')
    plt.close()
    print(f"  saved binding_curves_v5_paper_positive.pdf/png")


if __name__ == "__main__":
    main()
