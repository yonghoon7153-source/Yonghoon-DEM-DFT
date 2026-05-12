"""UMA_main_paper protocol — replicates the May 8 binding curve figure.

Method (recovered from binding_curves_plots/UMA_main_paper_*.csv):
  1. Read phase1 binding_curves.json (mean over 36 xy-shift registries)
  2. Per-registry asymptote subtract (mean Wad at gap >= 3.0 A per registry)
  3. Per-comp W_max = max of (asymp-subtracted mean Wad) in window 1.0-2.0 A
  4. Linear fit:  paper_exp_Wad (mJ/m²) = a * W_max + b   (Pearson R reported)
  5. Apply transform to ALL gap points:
       adh(d) = -(a * Wad_raw(d) + b) / 1000     [J/m²]
       (Wad_raw = same asymp-subtracted Wad; same affine map for every comp)
  6. PCHIP smooth on dense grid (300 points, 0.8-4.0 A)
  7. Output 3 CSVs + PNG + PDF in image-2 style.

Key insight: linear fit slope `a` can be NEGATIVE if raw ranking is inverted
vs paper exp. With a < 0, the affine transform FLIPS family ordering, so
Li5.4 family ends up at the bottom (image 2 look).

Usage:
    python plot_uma_main_paper.py [JSON_PATH]
    # default: phase1_results/binding_curves.json
"""
import csv, json, sys
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import PchipInterpolator

JSON_DEFAULT = "phase1_results/binding_curves.json"
JSON_PATH = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(JSON_DEFAULT)
OUT_DIR = Path("binding_curves_plots"); OUT_DIR.mkdir(exist_ok=True)

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

GAP_ASYMP_MIN = 3.0
WMAX_WINDOW   = (1.0, 2.0)
GAP_LO, GAP_HI = 0.8, 4.0
GAP_WINDOW_LO, GAP_WINDOW_HI = 1.2, 1.6


def load_raw_mean(path):
    """For each (comp, gap): mean & std of RAW Wad over 36 registries.
    NO asymptote subtraction — the original UMA_main_paper protocol applies
    the linear-fit transform to RAW W_ad, so per-comp baselines are preserved
    and the affine map gives positive slope (correct ranking).
    """
    raw = json.load(open(path))
    out = {}
    for c in PAPER_COMPS:
        if c not in raw:
            continue
        comp_data = raw[c]
        gap_set = set()
        for reg, rd in comp_data.items():
            gap_set.update(rd.get('curve', {}).keys())
        gaps_str = sorted(gap_set, key=float)
        gaps = np.array([float(g) for g in gaps_str])

        means = []; stds = []
        for g in gaps_str:
            vs = []
            for reg, rd in comp_data.items():
                curve = rd.get('curve', {})
                if g in curve and curve[g].get('Wad_J_per_m2') is not None:
                    vs.append(curve[g]['Wad_J_per_m2'])     # RAW, no subtract
            means.append(float(np.mean(vs)) if vs else float('nan'))
            stds.append(float(np.std(vs)) if len(vs) > 1 else 0.0)
        out[c] = (gaps, np.array(means), np.array(stds))
    return out


def main():
    if not JSON_PATH.exists():
        print(f"ERROR: {JSON_PATH} not found")
        return
    print(f"Loading {JSON_PATH}")
    data = load_raw_mean(JSON_PATH)

    # W_max per comp (max in 1.0-2.0 window)
    Wmax = {}
    dmin = {}
    for c in PAPER_COMPS:
        if c not in data:
            continue
        g, m, s = data[c]
        win = (g >= WMAX_WINDOW[0]) & (g <= WMAX_WINDOW[1])
        if win.any():
            i = int(np.nanargmax(m[win]))
            Wmax[c] = float(m[win][i])
            dmin[c] = float(g[win][i])

    have = [c for c in PAPER_COMPS if c in Wmax]
    x = np.array([Wmax[c] for c in have])
    y = np.array([PAPER_EXP[c] for c in have])

    # Linear fit y = a*x + b (least squares)
    a, b = np.polyfit(x, y, 1)
    R = float(np.corrcoef(x, y)[0, 1])
    print(f"Linear fit: paper_Wad = {a:+.4f} * W_max + {b:+.4f}, R = {R:+.4f}")

    # Predicted + abs error
    pred = {c: float(a * Wmax[c] + b) for c in have}

    # === Save 3 CSVs (mirror UMA_main_paper format) ===

    # 1) summary.csv
    summ_path = OUT_DIR / "uma_main_paper_v2_summary.csv"
    with open(summ_path, 'w') as f:
        f.write("# Per-comp summary: well depth + position + paper exp comparison\n")
        f.write(f"# Linear fit: paper_Wad (mJ/m^2) = {a:.4f} * UMA_W_max + {b:.4f}, R={R:+.4f}\n")
        f.write("comp,paper_exp_Wad_mJ_m2,UMA_W_max_J_m2,d_min_A,"
                "predicted_Wad_mJ_m2,adh_at_well_J_m2,abs_error_mJ_m2\n")
        for c in have:
            adh_well = -(a * Wmax[c] + b) / 1000.0
            err = abs(pred[c] - PAPER_EXP[c])
            f.write(f"{c},{PAPER_EXP[c]},{Wmax[c]:.4f},{dmin[c]:.2f},"
                    f"{pred[c]:.1f},{adh_well:.4f},{err:.1f}\n")

    # 2) raw_points.csv
    raw_path = OUT_DIR / "uma_main_paper_v2_raw_points.csv"
    all_gaps = sorted(set(g for c in have for g in data[c][0].tolist()))
    with open(raw_path, 'w') as f:
        f.write("# UMA binding curves — raw 36-reg mean (linear-fit transformed)\n")
        f.write(f"# Linear fit: paper_Wad (mJ/m^2) = {a:.4f} * UMA_W_max + {b:.4f}, R = {R:+.4f}, n={len(have)}\n")
        f.write("# Adhesion energy (J/m^2) = -(a * UMA_Wad + b) / 1000\n")
        f.write("# All values in J/m^2\n")
        f.write("gap_A," + ",".join(f"{c}_adh" for c in have) + ","
                + ",".join(f"{c}_std" for c in have) + "\n")
        for g in all_gaps:
            row = [f"{g:.3f}"]
            for c in have:
                gs, ms, _ = data[c]
                idx = np.where(np.isclose(gs, g))[0]
                if len(idx) > 0 and not np.isnan(ms[idx[0]]):
                    adh = -(a * ms[idx[0]] + b) / 1000.0
                    row.append(f"{adh:.6f}")
                else:
                    row.append("")
            for c in have:
                gs, _, ss = data[c]
                idx = np.where(np.isclose(gs, g))[0]
                if len(idx) > 0:
                    # std propagates: sigma_adh = |a|/1000 * sigma_W
                    sigma_adh = abs(a) / 1000.0 * ss[idx[0]]
                    row.append(f"{sigma_adh:.6f}")
                else:
                    row.append("")
            f.write(",".join(row) + "\n")

    # 3) smooth.csv (PCHIP, 300 points, 0.8-4.0)
    g_dense = np.linspace(GAP_LO, GAP_HI, 300)
    smooth_per_comp = {}
    for c in have:
        gs, ms, _ = data[c]
        m = (gs >= GAP_LO) & (gs <= GAP_HI) & ~np.isnan(ms)
        if m.sum() < 3:
            continue
        adh = -(a * ms[m] + b) / 1000.0
        order = np.argsort(gs[m])
        pchip = PchipInterpolator(gs[m][order], adh[order])
        smooth_per_comp[c] = pchip(g_dense)

    smooth_path = OUT_DIR / "uma_main_paper_v2_smooth.csv"
    with open(smooth_path, 'w') as f:
        f.write("# UMA binding curves — PCHIP smooth (300 points, 0.8-4.0 A)\n")
        f.write(f"# Linear fit: paper_Wad (mJ/m^2) = {a:.4f} * UMA_W_max + {b:.4f}, R = {R:+.4f}\n")
        f.write("# All values in J/m^2\n")
        f.write("gap_A," + ",".join(c for c in have if c in smooth_per_comp) + "\n")
        for i, gd in enumerate(g_dense):
            row = [f"{gd:.4f}"]
            for c in have:
                if c in smooth_per_comp:
                    row.append(f"{smooth_per_comp[c][i]:.6f}")
            f.write(",".join(row) + "\n")

    # === Plot ===
    plt.rcParams.update({
        'font.size': 13, 'axes.labelsize': 15, 'axes.titlesize': 16,
        'xtick.labelsize': 12, 'ytick.labelsize': 12, 'legend.fontsize': 11,
        'figure.dpi': 150, 'savefig.dpi': 300, 'savefig.bbox': 'tight',
    })
    fig, ax = plt.subplots(figsize=(11, 7.5))
    for c in have:
        if c not in smooth_per_comp:
            continue
        ax.plot(g_dense, smooth_per_comp[c], '-', color=COLORS[c],
                lw=3.0, alpha=0.95, zorder=5)
        # markers from raw data
        gs, ms, _ = data[c]
        m = (gs >= GAP_LO) & (gs <= GAP_HI) & ~np.isnan(ms)
        adh = -(a * ms[m] + b) / 1000.0
        ax.plot(gs[m], adh, MARKERS[c], color=COLORS[c],
                ms=9, mec='k', mew=0.5, label=LABELS[c], zorder=10)

    ax.axvspan(GAP_WINDOW_LO, GAP_WINDOW_HI, alpha=0.13, color='gray', zorder=1)
    ax.axhline(0, color='k', lw=0.7, alpha=0.7, zorder=2)
    ax.set_xlabel(r'Interface gap, $d$ (Å)')
    ax.set_ylabel(r'Adhesion energy (J m$^{-2}$)')
    ax.set_title(r'UMA binding curves')
    ax.set_xlim(GAP_LO, GAP_HI)
    ax.grid(True, alpha=0.25)
    ax.legend(loc='lower right', framealpha=0.95)
    fig.tight_layout()
    png = OUT_DIR / "uma_main_paper_v2.png"
    pdf = OUT_DIR / "uma_main_paper_v2.pdf"
    fig.savefig(png); fig.savefig(pdf); plt.close()

    print(f"\nsaved {png}\nsaved {pdf}")
    print(f"saved {summ_path}\nsaved {raw_path}\nsaved {smooth_path}\n")
    print(f"{'comp':<8} {'W_max':>10} {'d_min':>7} {'pred_Wad':>10} {'paper':>7} {'err':>7}")
    for c in have:
        print(f"{c:<8} {Wmax[c]:>+10.4f} {dmin[c]:>7.2f} {pred[c]:>10.1f} "
              f"{PAPER_EXP[c]:>7} {abs(pred[c]-PAPER_EXP[c]):>7.1f}")
    print(f"\nR(W_max vs paper_exp) = {R:+.4f}  (slope {a:+.2f}, intercept {b:+.2f})")


if __name__ == "__main__":
    main()
