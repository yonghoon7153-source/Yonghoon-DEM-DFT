"""Phase 2a v7 — image-2 style canonical binding-curve figure.

Supersedes v4 (max-over-registry, modelC-included → image 1 anomaly with
Y range -3..+2.5 and curves not converging at d=4).

This script reproduces the original "UMA binding curves (R = +0.925)" figure:
  - Read phase1_results/binding_curves.json (preferred) or
    binding_curves_csv/binding_UMA_Wad_mean_J_m2.csv as fallback
  - 5 paper comps only (no modelC)
  - MEAN over 36 xy-shift registries per (gap, comp)
  - Asymptote = mean of Wad at gap >= 3.0 Å, subtracted per comp
  - E_adh = -(Wad - asymp)  (negative = binding favorable)
  - Cubic spline smoothing (250 dense points), markers at data points
  - Gray axvspan 1.2-1.6 Å (typical equilibrium gap window)
  - Pearson R(well_depth, paper_exp) shown in title
  - Auto-fit Y range with 10% padding (typically ~[-0.35, 0.20])

Usage:
    python3 tools/plot_binding_curves_v7.py
    # outputs: binding_curves_plots/figure_v7_image2_style.{png,pdf,csv}

Inputs (priority):
  1) phase1_results/binding_curves.json
  2) binding_curves_csv/binding_UMA_Wad_mean_J_m2.csv
"""
import csv
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import CubicSpline

JSON_PATH = Path("phase1_results/binding_curves.json")
CSV_DIR   = Path("binding_curves_csv")
OUT_DIR   = Path("binding_curves_plots"); OUT_DIR.mkdir(exist_ok=True)

PAPER_EXP   = {'comp1': 194, 'comp2': 180, 'comp3': 316, 'comp4': 298, 'comp5': 249}
PAPER_COMPS = ['comp1', 'comp2', 'comp3', 'comp4', 'comp5']

COLORS  = {'comp1': '#1f77b4', 'comp2': '#17becf',
           'comp3': '#d62728', 'comp4': '#9467bd', 'comp5': '#2ca02c'}
MARKERS = {'comp1': 's', 'comp2': 'o', 'comp3': '^', 'comp4': 'D', 'comp5': 'v'}
LABELS  = {
    'comp1': r'comp1: Li$_6$PS$_5$Cl',
    'comp2': r'comp2: Li$_6$PS$_5$Cl$_{0.5}$Br$_{0.5}$',
    'comp3': r'comp3: Li$_{5.4}$PS$_{4.4}$Cl$_{1.0}$Br$_{0.6}$',
    'comp4': r'comp4: Li$_{5.4}$PS$_{4.4}$Cl$_{0.8}$Br$_{0.8}$',
    'comp5': r'comp5: Li$_{5.4}$PS$_{4.4}$Cl$_{0.6}$Br$_{1.0}$',
}

GAP_LO, GAP_HI       = 0.8, 4.0
GAP_ASYMPTOTE_MIN    = 3.0
GAP_WINDOW_LO, GAP_WINDOW_HI = 1.2, 1.6


def load_from_json(path):
    """Compute mean Wad over 36 registries from raw JSON."""
    raw = json.load(open(path))
    out = {}
    for c in PAPER_COMPS:
        if c not in raw:
            continue
        regs = raw[c]
        gaps_str = list(regs['R1_origin']['curve'].keys())
        gaps = np.array([float(g) for g in gaps_str])
        wads = []
        for g in gaps_str:
            vals = [regs[r]['curve'][g]['Wad_J_per_m2'] for r in regs]
            wads.append(float(np.mean(vals)))
        out[c] = (gaps, np.array(wads))
    return out


def load_from_csv(path):
    """Fallback: pre-computed mean Wad CSV."""
    rows = list(csv.reader(open(path)))
    header = rows[0]
    data = [r for r in rows[1:] if r and not r[0].startswith('#')]
    gaps = np.array([float(r[0]) for r in data])
    out = {}
    for j, name in enumerate(header[1:], 1):
        if name in PAPER_COMPS:
            vals = np.array([float(r[j]) if r[j] else np.nan for r in data])
            out[name] = (gaps, vals)
    return out


def main():
    if JSON_PATH.exists():
        print(f"Loading {JSON_PATH}")
        wad_data = load_from_json(JSON_PATH)
    else:
        csv_path = CSV_DIR / "binding_UMA_Wad_mean_J_m2.csv"
        if not csv_path.exists():
            print(f"ERROR: neither {JSON_PATH} nor {csv_path} found.")
            return
        print(f"Loading {csv_path}")
        wad_data = load_from_csv(csv_path)

    missing = [c for c in PAPER_COMPS if c not in wad_data]
    if missing:
        print(f"WARNING: missing comps {missing} in input — skipping them.")

    summary = {}
    for c in PAPER_COMPS:
        if c not in wad_data:
            continue
        gaps, wads = wad_data[c]
        asym_mask = gaps >= GAP_ASYMPTOTE_MIN
        W_asymp = float(np.nanmean(wads[asym_mask])) if asym_mask.any() else 0.0
        E_adh = -(wads - W_asymp)
        binding_mask = (gaps >= 1.0) & (gaps <= 2.5)
        if binding_mask.any():
            i = int(np.nanargmin(E_adh[binding_mask]))
            E_well = float(E_adh[binding_mask][i])
            d_min  = float(gaps[binding_mask][i])
        else:
            E_well = float('nan'); d_min = float('nan')
        summary[c] = {'gaps': gaps, 'wads': wads, 'asymp': W_asymp,
                      'E_adh': E_adh, 'E_well': E_well, 'd_min': d_min}

    have = [c for c in PAPER_COMPS if c in summary
            and not np.isnan(summary[c]['E_well'])]
    if len(have) >= 3:
        x = [-summary[c]['E_well'] for c in have]
        y = [PAPER_EXP[c] for c in have]
        R = float(np.corrcoef(x, y)[0, 1])
    else:
        R = float('nan')

    plt.rcParams.update({
        'font.size': 13, 'axes.labelsize': 15, 'axes.titlesize': 16,
        'xtick.labelsize': 12, 'ytick.labelsize': 12, 'legend.fontsize': 11,
        'figure.dpi': 150, 'savefig.dpi': 300, 'savefig.bbox': 'tight',
    })
    fig, ax = plt.subplots(figsize=(11, 7.5))
    gap_dense = np.linspace(GAP_LO, GAP_HI, 250)

    for c in PAPER_COMPS:
        if c not in summary:
            continue
        d = summary[c]
        m = (d['gaps'] >= GAP_LO) & (d['gaps'] <= GAP_HI)
        gz = d['gaps'][m]; Ez = d['E_adh'][m]
        order = np.argsort(gz)
        gz = gz[order]; Ez = Ez[order]
        cs = CubicSpline(gz, Ez)
        ax.plot(gap_dense, cs(gap_dense), '-', color=COLORS[c],
                lw=3.0, alpha=0.95, zorder=5)
        ax.plot(gz, Ez, MARKERS[c], color=COLORS[c],
                ms=9, mec='k', mew=0.5, label=LABELS[c], zorder=10)

    ax.axvspan(GAP_WINDOW_LO, GAP_WINDOW_HI, alpha=0.15, color='gray', zorder=1)
    ax.axhline(0, color='k', lw=0.7, alpha=0.7, zorder=2)
    ax.set_xlabel(r'Interface gap, $d$ (Å)')
    ax.set_ylabel(r'Adhesion energy (J m$^{-2}$)')
    ax.set_title(f'UMA binding curves (R = {R:+.3f})')
    ax.set_xlim(GAP_LO, GAP_HI)

    all_E = np.concatenate([summary[c]['E_adh'][
        (summary[c]['gaps'] >= GAP_LO) & (summary[c]['gaps'] <= GAP_HI)]
        for c in summary])
    y_lo, y_hi = float(np.nanmin(all_E)), float(np.nanmax(all_E))
    pad = 0.10 * (y_hi - y_lo)
    ax.set_ylim(y_lo - pad, y_hi + pad)
    ax.grid(True, alpha=0.25)
    ax.legend(loc='lower right', framealpha=0.95)

    fig.tight_layout()
    png = OUT_DIR / "figure_v7_image2_style.png"
    pdf = OUT_DIR / "figure_v7_image2_style.pdf"
    fig.savefig(png); fig.savefig(pdf); plt.close()

    csv_out = OUT_DIR / "figure_v7_image2_style.csv"
    comps_out = [c for c in PAPER_COMPS if c in summary]
    if comps_out:
        all_gaps = sorted(set(g for c in comps_out for g in summary[c]['gaps'].tolist()))
        with open(csv_out, 'w', encoding='utf-8') as f:
            f.write("# E_adh = -(Wad - asymp), J/m^2; mean over 36 xy-shifts; "
                    "asymp = mean Wad at gap >= 3.0 A; per-comp asymptote-subtracted\n")
            f.write("gap_A," + ",".join(comps_out) + "\n")
            for g in all_gaps:
                row = [f"{g:.3f}"]
                for c in comps_out:
                    arr_g = summary[c]['gaps']; arr_E = summary[c]['E_adh']
                    idx = np.where(np.isclose(arr_g, g))[0]
                    row.append(f"{float(arr_E[idx[0]]):.6f}" if len(idx) else "")
                f.write(",".join(row) + "\n")

    print(f"\nsaved {png}")
    print(f"saved {pdf}")
    print(f"saved {csv_out}")
    print(f"R(well depth vs paper) = {R:+.4f}\n")
    print(f"{'comp':<8} {'asymp':>+10} {'E_well':>+10} {'d_min':>7} {'paper_exp':>10}")
    for c in PAPER_COMPS:
        if c not in summary:
            continue
        d = summary[c]
        print(f"{c:<8} {d['asymp']:>+10.4f} {d['E_well']:>+10.4f} {d['d_min']:>7.2f} "
              f"{PAPER_EXP[c]:>10}")


if __name__ == "__main__":
    main()
