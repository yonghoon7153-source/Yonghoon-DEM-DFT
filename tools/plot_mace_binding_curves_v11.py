"""Phase 2a v11 — MACE binding curves post-processing.

Reads phase2a_v30_results/summary.json (MACE Z-scan, 6 comps × 23 gaps × 1 reg)
and produces binding curve plots similar to Phase 1 UMA curves but with MACE.

NOTE: v30 was single-registry (R1_origin only). Curves shown are raw single
registry, not registry-averaged like Phase 1. For paper figure, this is
acknowledged as 'single representative registry' with Phase 1 36-reg as
cross-validation.

Outputs:
  binding_MACE_curves_raw.pdf/png       all 6 comps, raw single-registry
  binding_MACE_curves_renormalized.pdf  asymptote-subtracted (cleaner)
  binding_MACE_curves.csv               gap_A + Wad per comp
"""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

PATH_V30 = Path("phase2a_v30_results/summary.json")
OUT_DIR = Path("binding_curves_plots"); OUT_DIR.mkdir(exist_ok=True)

ALL_COMPS = ['comp1', 'comp2', 'comp3', 'comp4', 'comp5', 'modelC']
PAPER_COMPS = ['comp1', 'comp2', 'comp3', 'comp4', 'comp5']
PAPER_EXP = {'comp1': 194, 'comp2': 180, 'comp3': 316, 'comp4': 298, 'comp5': 249}

LABELS = {
    'comp1':  r'comp1: Li$_6$PS$_5$Cl',
    'comp2':  r'comp2: Li$_6$PS$_5$Cl$_{0.5}$Br$_{0.5}$',
    'comp3':  r'comp3: Li$_{5.4}$PS$_{4.4}$Cl$_{1.0}$Br$_{0.6}$',
    'comp4':  r'comp4: Li$_{5.4}$PS$_{4.4}$Cl$_{0.8}$Br$_{0.8}$',
    'comp5':  r'comp5: Li$_{5.4}$PS$_{4.4}$Cl$_{0.6}$Br$_{1.0}$',
    'modelC': r'modelC: Li$_{5.4}$PS$_{4.4}$Cl$_{1.6}$ (no Br)',
}
COLORS = {
    'comp1':  '#1f77b4', 'comp2':  '#17becf',
    'comp3':  '#d62728', 'comp4':  '#9467bd', 'comp5':  '#2ca02c',
    'modelC': '#ff7f0e',
}
LINESTYLES = {'comp1':'-', 'comp2':'-', 'comp3':'-',
              'comp4':'-', 'comp5':'-', 'modelC':'--'}
MARKERS = {'comp1':'s', 'comp2':'o', 'comp3':'^',
           'comp4':'D', 'comp5':'v', 'modelC':'X'}

plt.rcParams.update({
    'font.size': 11, 'axes.labelsize': 12, 'axes.titlesize': 12,
    'xtick.labelsize': 10, 'ytick.labelsize': 10, 'legend.fontsize': 9,
    'figure.dpi': 150, 'savefig.dpi': 300, 'savefig.bbox': 'tight',
})


def main():
    if not PATH_V30.exists():
        print(f"ERROR: {PATH_V30} not found.")
        print(f"sftp from KISTI:")
        print(f"  /scratch/x3430a02/kgy/manuscript_support/phase2a_v30_results")
        print(f"  or")
        print(f"  /scratch/x3430a02/kgy/manuscript_support/adhesion_v5_v2/phase2a_v30_results")
        return

    d = json.load(open(PATH_V30))

    # Extract curves
    curves = {}
    for c in ALL_COMPS:
        if c not in d or 'wad_curve' not in d[c]:
            print(f"  WARN: {c} not in v30 summary")
            continue
        gaps = [pt['gap'] for pt in d[c]['wad_curve']]
        wads = [pt['Wad'] for pt in d[c]['wad_curve']]
        curves[c] = {'gap': np.array(gaps), 'wad': np.array(wads)}

    # ── Plot 1: raw curves ──
    fig, ax = plt.subplots(figsize=(8.5, 5.5))
    for c in ALL_COMPS:
        if c not in curves:
            continue
        cv = curves[c]
        ax.plot(cv['gap'], cv['wad'], color=COLORS[c],
                linestyle=LINESTYLES[c], lw=1.8,
                marker=MARKERS[c], markersize=4,
                label=LABELS[c])
    ax.axhline(0, color='k', linewidth=0.5, alpha=0.4)
    ax.axvspan(1.2, 1.6, color='gray', alpha=0.10, label='gap_eq region')
    ax.set_xlabel('Interface gap (Å)', fontsize=12)
    ax.set_ylabel(r'MACE $W_{ad}$ (J/m²)', fontsize=12)
    ax.set_title('MACE-MP-0 binding curves (single registry R1_origin, 23 gap points)',
                 fontsize=11)
    ax.set_xlim(0.5, 4.0)
    ax.legend(loc='lower right', fontsize=8.5)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "binding_MACE_curves_raw.pdf", bbox_inches='tight')
    fig.savefig(OUT_DIR / "binding_MACE_curves_raw.png", bbox_inches='tight')
    plt.close()
    print(f"  saved binding_MACE_curves_raw.pdf/png")

    # ── Plot 2: asymptote-subtracted (per-comp) ──
    asyms = {}
    for c in ALL_COMPS:
        if c not in curves:
            continue
        gap_arr = curves[c]['gap']
        mask_far = gap_arr >= 3.0
        if mask_far.any():
            asyms[c] = float(np.mean(curves[c]['wad'][mask_far]))
        else:
            asyms[c] = 0.0

    fig, ax = plt.subplots(figsize=(8.5, 5.5))
    for c in ALL_COMPS:
        if c not in curves:
            continue
        cv = curves[c]
        wad_norm = cv['wad'] - asyms[c]
        ax.plot(cv['gap'], wad_norm, color=COLORS[c],
                linestyle=LINESTYLES[c], lw=1.8,
                marker=MARKERS[c], markersize=4,
                label=f"{LABELS[c]} (asym={asyms[c]:+.2f})")
    ax.axhline(0, color='k', linewidth=0.5, alpha=0.4)
    ax.axvspan(1.2, 1.6, color='gray', alpha=0.10)
    ax.set_xlabel('Interface gap (Å)', fontsize=12)
    ax.set_ylabel(r'$W_{ad}$ above asymptote (J/m²)', fontsize=12)
    ax.set_title('MACE binding curves — asymptote-subtracted', fontsize=11)
    ax.set_xlim(0.5, 4.0)
    ax.legend(loc='upper right', fontsize=7.5)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "binding_MACE_curves_renormalized.pdf", bbox_inches='tight')
    fig.savefig(OUT_DIR / "binding_MACE_curves_renormalized.png", bbox_inches='tight')
    plt.close()
    print(f"  saved binding_MACE_curves_renormalized.pdf/png")

    # ── CSV ──
    # union of gap axes
    all_gaps = sorted(set().union(*[set(c['gap'].tolist()) for c in curves.values()]))
    csv_path = OUT_DIR / "binding_MACE_curves.csv"
    with open(csv_path, 'w', encoding='utf-8') as f:
        f.write("# MACE-MP-0 single-registry (R1_origin) Wad J/m^2 vs gap\n")
        f.write("# 23 gap points 0.5-6.0 A, step 0.25 A\n")
        f.write("gap_A," + ",".join(ALL_COMPS) + "\n")
        for g in all_gaps:
            row = [f"{g:.3f}"]
            for c in ALL_COMPS:
                if c not in curves:
                    row.append("")
                    continue
                idx = np.where(np.abs(curves[c]['gap'] - g) < 1e-6)[0]
                if len(idx) > 0:
                    row.append(f"{curves[c]['wad'][idx[0]]:.6f}")
                else:
                    row.append("")
            f.write(",".join(row) + "\n")
    print(f"  saved {csv_path}")

    # ── Print summary ──
    print(f"\n--- MACE per-comp W_max + d_min (single registry) ---")
    print(f"{'comp':<8} {'W_max':>10} {'d_min(Å)':>10} {'asymptote':>11} {'paper':>7}")
    for c in ALL_COMPS:
        if c not in curves:
            continue
        cv = curves[c]
        i_max = int(np.argmax(cv['wad']))
        wm = float(cv['wad'][i_max])
        dm = float(cv['gap'][i_max])
        pe = PAPER_EXP.get(c, '—')
        print(f"  {c:<8} {wm:>+10.3f} {dm:>10.2f} {asyms[c]:>+11.3f} {str(pe):>7}")


if __name__ == "__main__":
    main()
