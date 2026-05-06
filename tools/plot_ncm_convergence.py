#!/usr/bin/env python3
"""
NCM thickness convergence plot — Choi Fig S1 analog.

Justifies 1L NCM intentional choice by showing cross-family behavior
of Wad at 1L vs 5L thickness.

Outputs:
  - ncm_convergence.png  — bar plot: 1L vs 5L for each comp, grouped by family

Usage:
    python tools/plot_ncm_convergence.py
"""
import json
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "output"
OUT.mkdir(exist_ok=True)

# Data from kb/results/adhesion_100seeds_analysis.md (1L 100-seed, 5L 20-seed)
DATA = {
    "comp3":  {"1L_mean": 2.328, "1L_std": 0.490, "5L_mean": 2.826, "5L_std": 0.604, "family": "Li5.4"},
    "comp4":  {"1L_mean": 2.250, "1L_std": 0.437, "5L_mean": 2.383, "5L_std": 0.805, "family": "Li5.4"},
    "comp5":  {"1L_mean": 2.280, "1L_std": 0.335, "5L_mean": 2.061, "5L_std": 0.824, "family": "Li5.4"},
    "comp1":  {"1L_mean": 1.151, "1L_std": 0.245, "5L_mean": 2.674, "5L_std": 0.882, "family": "Li6"},
    "comp2B": {"1L_mean": 1.615, "1L_std": 0.417, "5L_mean": 2.718, "5L_std": 1.121, "family": "Li6"},
}
ORDER = ["comp3", "comp4", "comp5", "comp1", "comp2B"]
COLORS_1L = "#2A9D8F"
COLORS_5L = "#E63946"


def plot():
    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    x = np.arange(len(ORDER))
    w = 0.38

    m1 = np.array([DATA[c]["1L_mean"] for c in ORDER])
    s1 = np.array([DATA[c]["1L_std"] for c in ORDER])
    m5 = np.array([DATA[c]["5L_mean"] for c in ORDER])
    s5 = np.array([DATA[c]["5L_std"] for c in ORDER])

    ax.bar(x - w/2, m1, w, yerr=s1, capsize=4,
           color=COLORS_1L, label="1L NCM (n=100)",
           edgecolor="#404040", lw=0.8, error_kw={"lw": 1})
    ax.bar(x + w/2, m5, w, yerr=s5, capsize=4,
           color=COLORS_5L, label="5L NCM (n≈20)",
           edgecolor="#404040", lw=0.8, error_kw={"lw": 1})

    # Family divider between Li5.4 and Li6 (index 3 = boundary)
    ax.axvline(2.5, color="#404040", ls="--", lw=1.2, alpha=0.6)
    ax.text(1.0, ax.get_ylim()[1] * 0.92 if ax.get_ylim()[1] > 0 else 3.5,
            "Li5.4 family", ha="center", fontsize=11, color="#404040")
    ax.text(3.5, ax.get_ylim()[1] * 0.92 if ax.get_ylim()[1] > 0 else 3.5,
            "Li6 family", ha="center", fontsize=11, color="#404040")

    ax.set_xticks(x)
    ax.set_xticklabels(ORDER, fontsize=11)
    ax.set_ylabel(r"$W_\mathrm{ad}$ (J/m²)", fontsize=13)
    ax.set_title("NCM thickness effect (1L vs 5L) — Choi Fig S1 analog",
                 fontsize=12)
    ax.legend(frameon=False, fontsize=11, loc="upper right")
    ax.grid(axis="y", alpha=0.3)

    # Annotate key finding
    ax.text(0.02, 0.98,
            "1L: cross-family correct (Li5.4 > Li6) — matches experiment\n"
            "5L: cross-family reversed — SE density mismatch dominates",
            transform=ax.transAxes, fontsize=9, va="top",
            bbox=dict(facecolor="white", edgecolor="#CCCCCC", pad=5))

    fig.tight_layout()
    outpath = OUT / "ncm_convergence.png"
    fig.savefig(outpath, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"  ✓ {outpath.name}")

    with open(OUT / "ncm_convergence_summary.json", "w") as f:
        json.dump(DATA, f, indent=2)
    print(f"  ✓ ncm_convergence_summary.json")


if __name__ == "__main__":
    plot()
