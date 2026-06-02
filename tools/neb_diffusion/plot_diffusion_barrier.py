#!/usr/bin/env python3
"""Diffusion barrier bar chart for paper Figure (h).

Mirrors Cui 2023 ACS Nano Figure 2e style: ordered descending bars of Li
adatom diffusion barrier on SEI / interphase materials.

Data sources:
  - Cui 2023 (literature): Li2O 0.319, Li2CO3 0.232, LiF 0.169, LiOH 0.141,
    Li3N 0.133 eV (DFT, surface adsorbate diffusion)
  - This work (DFT): Li3N (001), LiC6 (0001) — UMA-NEB path geometry,
    DFT SCF energies, effective barrier = TS - bridge

Usage:
    # Default: all literature + Li3N(ours), LiC6 from JSON if available
    python3 plot_diffusion_barrier.py \\
        --li3n_ours_eV 0.0486 \\
        --lic6_ours_eV 0.241 \\
        --out output/barrier_bar.png

    # Or feed full DFT results JSON
    python3 plot_diffusion_barrier.py \\
        --dft_json /data/.../li3n_dft_neb_results.json \\
        --dft_json2 /data/.../lic6_dft_neb_results.json \\
        --out output/barrier_bar.png
"""
import argparse
import json
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt


# Cui 2023 ACS Nano Figure 2e values (DFT, eV)
LIT_DATA = {
    "Li$_2$O":      0.319,
    "Li$_2$CO$_3$": 0.232,
    "LiF":          0.169,
    "LiOH":         0.141,
    "Li$_3$N (Cui)":      0.133,
}

# Pastel palette (Cui Fig 2e style)
LIT_COLORS = {
    "Li$_2$O":         "#F4A6A6",   # pink
    "Li$_2$CO$_3$":    "#F4C28D",   # peach
    "LiF":             "#F2DC9B",   # yellow-tan
    "LiOH":            "#A9D4A2",   # green
    "Li$_3$N (Cui)":   "#9FB7DC",   # blue
}
OURS_COLOR_LI3N = "#3B5BA0"   # deep blue (highlight: our Li3N)
OURS_COLOR_LIC6 = "#5A5A5A"   # dark gray (LiC6 baseline, "anode-free worst case")


def _parse_eff_barrier_from_dft_json(path):
    """Effective barrier from a 7-image DFT SCF JSON written by run_dft_neb.sh.

    Effective barrier (bridge → on-site TS → bridge):
        TS_energy_rel - bridge_energy_rel
    where:
        TS = max(rel_energies_eV)
        bridge = min(rel_energies_eV)   (intermediate basin if it exists)
    If no intermediate basin (all rel > endpoints), fall back to barrier_eV.
    """
    with open(path) as f:
        d = json.load(f)
    rel = d["rel_energies_eV"]
    tot = max(rel)
    mn = min(rel)
    if mn < -1e-3:  # has a sub-endpoint basin (bridge minimum)
        return tot - mn
    return d.get("barrier_eV", tot)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--li3n_ours_eV", type=float, default=None,
                    help="our Li3N effective barrier (eV); overrides --dft_json_li3n")
    ap.add_argument("--lic6_ours_eV", type=float, default=None,
                    help="our LiC6 barrier (eV); overrides --dft_json_lic6")
    ap.add_argument("--dft_json_li3n", default=None,
                    help="dft_neb_results.json for Li3N")
    ap.add_argument("--dft_json_lic6", default=None,
                    help="dft_neb_results.json for LiC6")
    ap.add_argument("--out", required=True)
    ap.add_argument("--include_literature", action="store_true", default=True,
                    help="include Cui 2023 literature SEI bars (default true)")
    ap.add_argument("--no_literature", dest="include_literature",
                    action="store_false")
    ap.add_argument("--figsize", type=float, nargs=2, default=[7.0, 4.5])
    ap.add_argument("--dpi", type=int, default=300)
    ap.add_argument("--title", default=None)
    args = ap.parse_args()

    li3n_ours = args.li3n_ours_eV
    if li3n_ours is None and args.dft_json_li3n:
        li3n_ours = _parse_eff_barrier_from_dft_json(args.dft_json_li3n)
        print(f"Li3N (ours) effective barrier from JSON: {li3n_ours:.4f} eV")

    lic6_ours = args.lic6_ours_eV
    if lic6_ours is None and args.dft_json_lic6:
        lic6_ours = _parse_eff_barrier_from_dft_json(args.dft_json_lic6)
        print(f"LiC6 (ours) barrier from JSON: {lic6_ours:.4f} eV")

    # Assemble bar data
    bars = []  # list of (label, value, color, edgecolor, linewidth)
    if args.include_literature:
        for lbl, v in LIT_DATA.items():
            bars.append((lbl, v, LIT_COLORS[lbl], "#222", 0.8))
    if lic6_ours is not None:
        bars.append(("LiC$_6$\n(this work)", lic6_ours,
                     OURS_COLOR_LIC6, "#000", 1.5))
    if li3n_ours is not None:
        bars.append(("Li$_3$N\n(this work)", li3n_ours,
                     OURS_COLOR_LI3N, "#000", 1.5))

    if not bars:
        raise SystemExit("No data — provide at least one of --li3n_ours_eV / "
                         "--lic6_ours_eV / --dft_json_* or enable literature.")

    # Sort descending by value (Cui 2023 Fig 2e style)
    bars.sort(key=lambda b: -b[1])

    labels = [b[0] for b in bars]
    values = [b[1] for b in bars]
    colors = [b[2] for b in bars]
    edges  = [b[3] for b in bars]
    lws    = [b[4] for b in bars]

    fig, ax = plt.subplots(figsize=tuple(args.figsize))
    x = np.arange(len(bars))
    rects = ax.bar(x, values, color=colors, edgecolor=edges, linewidth=lws,
                   width=0.72, zorder=3)

    # Value labels above bars
    for r, v in zip(rects, values):
        ax.text(r.get_x() + r.get_width() / 2, v + 0.008,
                f"{v:.3f}", ha='center', va='bottom',
                fontsize=9, color='#333', zorder=4)

    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=10)
    ax.set_ylabel("Diffusion Barrier (eV)", fontsize=12)
    ax.set_ylim(0, max(values) * 1.18)
    ax.grid(axis='y', linestyle='--', alpha=0.4, zorder=0)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    if args.title:
        ax.set_title(args.title, fontsize=12)

    out = Path(args.out); out.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(out, dpi=args.dpi, bbox_inches='tight', facecolor='white')
    print(f"\n→ {out}")

    # Also dump compact summary JSON next to the png
    summary_path = out.with_suffix(".json")
    with open(summary_path, 'w') as f:
        json.dump({
            "bars": [{"label": lbl.replace("$", "").replace("_", ""),
                       "barrier_eV": v}
                     for lbl, v, *_ in bars],
            "source": {
                "literature": "Cui et al., ACS Nano 2023, 17, 3168",
                "this_work": "UMA-oc20 NEB geometry + QE PBE+USPP DFT SCF",
            },
        }, f, indent=2)
    print(f"→ {summary_path}")


if __name__ == "__main__":
    main()
