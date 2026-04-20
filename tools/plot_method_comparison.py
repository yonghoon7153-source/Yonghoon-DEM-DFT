#!/usr/bin/env python3
"""
Method comparison plot — Choi Table S2 analog.

Compares 4 adhesion methods side-by-side:
  - v5 paper (5 selected seeds, 1L NCM)
  - v5 100-seed (1L NCM)
  - v8 bulk anneal (new method)
  - 5L unified (FixAtoms)

Source: kb/papers/final_report_v2.md Sections 5-1, 5-2, 5-4, 5-5

Outputs:
  - method_comparison.png  — 4-method bar chart, 5 compositions
  - method_comparison.json — structured data
"""
import json
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "output"
OUT.mkdir(exist_ok=True)

ORDER = ["comp3", "comp4", "comp5", "comp1", "comp2B"]
FAMILIES = {"comp3": "Li5.4", "comp4": "Li5.4", "comp5": "Li5.4",
            "comp1": "Li6",   "comp2B": "Li6"}

# Values from final_report_v2.md
METHODS = {
    "v5 paper (5 seeds)": {
        "comp3":  (2.103, 0.245),
        "comp4":  (1.970, 0.629),
        "comp5":  (1.651, 0.284),
        "comp1":  (1.277, 0.383),
        "comp2B": (1.183, 0.362),
    },
    "v5 100-seed": {
        "comp3":  (2.328, 0.490),
        "comp4":  (2.250, 0.437),
        "comp5":  (2.280, 0.335),
        "comp1":  (1.151, 0.245),
        "comp2B": (1.615, 0.417),
    },
    "v8 bulk anneal": {
        "comp3":  (1.020, 0.335),
        "comp4":  (0.927, 0.301),
        "comp5":  (1.086, 0.739),
        "comp1":  (0.758, 0.148),
        "comp2B": (1.091, 0.420),
    },
    "5L unified (20 seeds)": {
        "comp3":  (2.826, 0.604),
        "comp4":  (2.383, 0.805),
        "comp5":  (2.061, 0.824),
        "comp1":  (2.674, 0.882),
        "comp2B": (2.718, 1.121),
    },
}

# Experimental target (aJ -> relative ratio on right axis)
EXPT_AJ = {"comp3": 316, "comp4": 298, "comp5": 249, "comp1": 194, "comp2B": 180}

METHOD_COLORS = ["#2A9D8F", "#4FBDFF", "#F4A261", "#9B5DE5"]


def plot():
    fig, ax = plt.subplots(figsize=(10, 5.2))
    x = np.arange(len(ORDER))
    n_methods = len(METHODS)
    w = 0.80 / n_methods

    for i, (name, vals) in enumerate(METHODS.items()):
        means = np.array([vals[c][0] for c in ORDER])
        stds  = np.array([vals[c][1] for c in ORDER])
        ax.bar(x + (i - (n_methods - 1)/2) * w, means, w,
               yerr=stds, capsize=3,
               color=METHOD_COLORS[i], label=name,
               edgecolor="#404040", lw=0.6,
               error_kw={"lw": 0.8})

    ax.axvline(2.5, color="#404040", ls="--", lw=1.2, alpha=0.6)
    ylim = ax.get_ylim()[1]
    ax.text(1.0, ylim * 0.95, "Li5.4 family", ha="center", fontsize=11, color="#404040")
    ax.text(3.5, ylim * 0.95, "Li6 family", ha="center", fontsize=11, color="#404040")

    ax.set_xticks(x)
    ax.set_xticklabels(ORDER, fontsize=11)
    ax.set_ylabel(r"$W_\mathrm{ad}$ (J/m²)", fontsize=13)
    ax.set_title("Adhesion method comparison (Choi Table S2 analog)", fontsize=12)
    ax.legend(frameon=False, fontsize=10, ncol=2, loc="upper right")
    ax.grid(axis="y", alpha=0.3)

    # Right axis: experimental aJ values as reference diamonds
    ax2 = ax.twinx()
    expt = [EXPT_AJ[c] for c in ORDER]
    ax2.plot(x, expt, "D", color="#E63946", markersize=9,
             markeredgecolor="#404040", markeredgewidth=0.8,
             label="Expt (aJ, r=10 nm)")
    ax2.set_ylabel("Expt adhesion (aJ)", fontsize=13, color="#E63946")
    ax2.tick_params(axis="y", labelcolor="#E63946")
    ax2.legend(loc="lower right", fontsize=10, frameon=False)

    fig.tight_layout()
    outpath = OUT / "method_comparison.png"
    fig.savefig(outpath, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"  ✓ {outpath.name}")

    summary = {m: {c: {"mean": v[0], "std": v[1]} for c, v in vals.items()}
               for m, vals in METHODS.items()}
    summary["expt_aJ"] = EXPT_AJ
    summary["notes"] = {
        "v5_paper": "R=0.9999 with expt, selected 5 seeds per family",
        "v5_100seed": "Full 100-seed statistics, no selection",
        "v8_bulk_anneal": "SE annealed in bulk PBC then stacked; cross-family preserved",
        "5L_unified": "NCM 7x7x5 + FixAtoms bottom 3L; cross-family FAILS"
    }
    with open(OUT / "method_comparison.json", "w") as f:
        json.dump(summary, f, indent=2)
    print(f"  ✓ method_comparison.json")


if __name__ == "__main__":
    plot()
