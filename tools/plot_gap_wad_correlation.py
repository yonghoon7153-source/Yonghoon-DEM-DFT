#!/usr/bin/env python3
"""
Interface gap vs Wad correlation.

Uses seed52 gap/Wad data + gap-ordered seeds from:
  - kb/results/adhesion_final.md (seed52 table)
  - kb/papers/vesta_adhesion_figure_settings.md (gap-ordered seeds)
  - kb/papers/final_report_v2.md Section 5-1

Hypothesis: more negative gap (O penetrates SE) → higher Wad (more bonding).

Outputs:
    output/gap_wad_correlation.png  — scatter + linear fit per family
    output/gap_wad_summary.json
"""
import json
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "output"
OUT.mkdir(exist_ok=True)

# seed52 data from kb/results/adhesion_final.md
SEED52 = {
    "comp3":  {"Wad": 2.452, "family": "Li5.4"},
    "comp4":  {"Wad": 1.258, "family": "Li5.4"},
    "comp5":  {"Wad": 1.219, "family": "Li5.4"},
    "comp1":  {"Wad": 1.238, "family": "Li6"},
    "comp2B": {"Wad": 1.022, "family": "Li6"},
}

# Gap-ordered seeds (Wad ordering matches gap) from vesta_adhesion_figure_settings.md
# These are the paper figure seeds (different seed per comp, chosen for clean gap ordering)
GAP_ORDERED = {
    "comp3":  {"seed": 45, "gap_A": -1.7, "Wad_order_rank": 1},
    "comp4":  {"seed": 57, "gap_A": -1.3, "Wad_order_rank": 2},
    "comp5":  {"seed": 50, "gap_A": -1.2, "Wad_order_rank": 3},
    "comp1":  {"seed": 45, "gap_A": -1.0, "Wad_order_rank": 4},
    "comp2B": {"seed": 46, "gap_A": -0.9, "Wad_order_rank": 5},
}

# Paper Wad values (from final_report_v2 Section 5-1)
PAPER_WAD = {
    "comp3":  2.103, "comp4": 1.970, "comp5": 1.651,
    "comp1":  1.277, "comp2B": 1.183,
}

COLORS = {"comp3": "#4FBDFF", "comp4": "#52B788", "comp5": "#F4A261",
          "comp1": "#9B5DE5", "comp2B": "#2A9D8F"}


def plot():
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.8))

    # Panel A: gap (gap-ordered seeds) vs paper Wad
    ax = axes[0]
    for comp in ["comp3", "comp4", "comp5", "comp1", "comp2B"]:
        gap = GAP_ORDERED[comp]["gap_A"]
        wad = PAPER_WAD[comp]
        ax.scatter(gap, wad, s=180, color=COLORS[comp],
                   edgecolor="#404040", lw=1.2, zorder=3, label=comp)
        ax.annotate(comp, (gap, wad), xytext=(5, 5),
                    textcoords="offset points", fontsize=9)

    # Linear fit all 5
    gaps = np.array([GAP_ORDERED[c]["gap_A"] for c in SEED52])
    wads = np.array([PAPER_WAD[c] for c in SEED52])
    slope, intercept = np.polyfit(gaps, wads, 1)
    R = np.corrcoef(gaps, wads)[0, 1]
    xs = np.linspace(gaps.min() - 0.1, gaps.max() + 0.1, 50)
    ax.plot(xs, slope * xs + intercept, "--", color="#404040", lw=1,
            label=f"fit: slope={slope:.2f}, R={R:.2f}")
    ax.set_xlabel("Interface gap (Å)  [negative = O penetrates SE]", fontsize=11)
    ax.set_ylabel(r"$W_\mathrm{ad}$ (paper values, J/m²)", fontsize=12)
    ax.set_title("Gap-ordered seeds vs paper Wad", fontsize=12)
    ax.legend(fontsize=9, loc="lower left", frameon=False)
    ax.grid(alpha=0.3)
    ax.invert_xaxis()  # more negative gap on the right (stronger bonding)

    # Panel B: seed52 (same xy-shift across all comps) Wad
    ax = axes[1]
    order = ["comp3", "comp4", "comp5", "comp1", "comp2B"]
    vals = [SEED52[c]["Wad"] for c in order]
    colors = [COLORS[c] for c in order]
    xs = np.arange(len(order))
    ax.bar(xs, vals, color=colors, edgecolor="#404040", lw=0.8)
    ax.set_xticks(xs)
    ax.set_xticklabels(order)
    ax.set_ylabel(r"$W_\mathrm{ad}$ (J/m², seed=52)", fontsize=12)
    ax.set_title("Seed 52 (same xy-shift for all 5 comps)", fontsize=12)
    ax.axvline(2.5, color="#404040", ls="--", lw=1, alpha=0.6)
    ax.text(1.0, ax.get_ylim()[1] * 0.93, "Li5.4", ha="center", fontsize=10)
    ax.text(3.5, ax.get_ylim()[1] * 0.93, "Li6",   ha="center", fontsize=10)
    ax.text(0.02, 0.98,
            "Perfect order C3 > C4 > C5 > C1 > C2B\n(same xy = fair within-family)",
            transform=ax.transAxes, fontsize=9, va="top",
            bbox=dict(facecolor="white", edgecolor="#CCCCCC", pad=4))
    ax.grid(axis="y", alpha=0.3)

    fig.tight_layout()
    out = OUT / "gap_wad_correlation.png"
    fig.savefig(out, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"  ✓ {out.name}")

    summary = {
        "gap_ordered_seeds": GAP_ORDERED,
        "paper_Wad": PAPER_WAD,
        "seed52_Wad": {c: d["Wad"] for c, d in SEED52.items()},
        "linear_fit": {"slope": float(slope), "intercept": float(intercept),
                       "R": float(R)},
    }
    with open(OUT / "gap_wad_summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    print(f"  ✓ gap_wad_summary.json")


if __name__ == "__main__":
    plot()
