#!/usr/bin/env python3
"""
Master summary figure: all key paper results in one multi-panel plot.

Panels:
  (a) B0 across 6 comps (DFT EOS)
  (b) E at 600K across 6 comps (MLIP snapshot)
  (c) Wad paper vs Wad 100-seed vs experiment (3-way comparison)
  (d) Paired comparison summary (Δ ± SE bars for all 4 pairs)

Source: final_report_v2.md Sections 3, 4, 5.
"""
import json
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "output"
OUT.mkdir(exist_ok=True)

ORDER = ["comp3", "comp4", "comp5", "comp1", "comp2B"]
COLORS = {"comp3": "#4FBDFF", "comp4": "#52B788", "comp5": "#F4A261",
          "comp1": "#9B5DE5", "comp2B": "#2A9D8F"}

B0 = {"comp3": 20.8, "comp4": 20.8, "comp5": 22.9, "comp1": 26.5, "comp2B": 25.8,
      "modelc": 21.7}
# comp1 = 26.5 from v2 pipeline (11 pts DFT, R2=0.999998, annealing champion)
# v1 value = 26.2 (8 pts, Rietveld Li). v2 is paper value.
E600 = {"comp3": (27.3, 0.4), "comp4": (26.4, 1.6), "comp5": (25.8, 0.8),
        "comp1": (29.1, 1.1), "comp2B": (28.6, 1.1), "modelc": (32.9, 0.9)}
WAD_PAPER = {"comp3": (2.103, 0.245), "comp4": (1.970, 0.629),
             "comp5": (1.651, 0.284), "comp1": (1.277, 0.383),
             "comp2B": (1.183, 0.362)}
WAD_100S = {"comp3": (2.328, 0.490), "comp4": (2.250, 0.437),
            "comp5": (2.280, 0.335), "comp1": (1.151, 0.245),
            "comp2B": (1.615, 0.417)}
EXPT_AJ = {"comp3": 316, "comp4": 298, "comp5": 249, "comp1": 194, "comp2B": 180}

PAIRED = {  # from final_report_v2 Section 5-3
    "C3-C4":  (+0.040, 0.068),
    "C3-C5":  (+0.048, 0.059),
    "C4-C5":  (+0.008, 0.061),
    "C1-C2B": (-0.464, 0.052),
}


def plot():
    fig, axes = plt.subplots(2, 2, figsize=(13, 9))
    fig.suptitle("Argyrodite mechanical properties — paper summary",
                 fontsize=14, y=1.00)

    # ── (a) B0 ───────────────────────────────────────────────────────
    ax = axes[0, 0]
    order6 = ORDER + ["modelc"]
    xs = np.arange(len(order6))
    vals = [B0[c] for c in order6]
    cols = [COLORS.get(c, "#999999") for c in order6]
    ax.bar(xs, vals, color=cols, edgecolor="#404040", lw=0.8)
    ax.set_xticks(xs)
    ax.set_xticklabels(order6, fontsize=10)
    ax.set_ylabel("B₀ (GPa)", fontsize=12)
    ax.set_title("(a) Bulk modulus (DFT EOS)", fontsize=12)
    for x, v in zip(xs, vals):
        ax.text(x, v + 0.3, f"{v:.1f}", ha="center", fontsize=9)
    ax.grid(axis="y", alpha=0.3)

    # ── (b) E 600K ───────────────────────────────────────────────────
    ax = axes[0, 1]
    vals = [E600[c][0] for c in order6]
    errs = [E600[c][1] for c in order6]
    ax.bar(xs, vals, yerr=errs, capsize=4,
           color=cols, edgecolor="#404040", lw=0.8,
           error_kw={"lw": 1})
    ax.set_xticks(xs)
    ax.set_xticklabels(order6, fontsize=10)
    ax.set_ylabel("E (GPa, 600K snapshot)", fontsize=12)
    ax.set_title("(b) Young's modulus (MLIP 600K)", fontsize=12)
    # experimental anchor for comp1
    ax.errorbar([order6.index("comp1")], [28.0], yerr=[1.8], fmt="D",
                color="#E63946", markersize=10, markeredgecolor="#404040",
                markeredgewidth=0.8, label="expt (comp1: 28.0±1.8)")
    ax.legend(loc="upper left", frameon=False, fontsize=10)
    ax.grid(axis="y", alpha=0.3)

    # ── (c) Wad 3-way ────────────────────────────────────────────────
    ax = axes[1, 0]
    xs5 = np.arange(len(ORDER))
    w = 0.35
    paper = [WAD_PAPER[c][0] for c in ORDER]
    paper_s = [WAD_PAPER[c][1] for c in ORDER]
    s100 = [WAD_100S[c][0] for c in ORDER]
    s100_s = [WAD_100S[c][1] for c in ORDER]
    ax.bar(xs5 - w/2, paper, w, yerr=paper_s, capsize=3,
           color="#2A9D8F", edgecolor="#404040", lw=0.6,
           label="v5 paper (5 seeds)", error_kw={"lw": 0.8})
    ax.bar(xs5 + w/2, s100, w, yerr=s100_s, capsize=3,
           color="#4FBDFF", edgecolor="#404040", lw=0.6,
           label="v5 100-seed", error_kw={"lw": 0.8})
    ax.axvline(2.5, color="#404040", ls="--", lw=1, alpha=0.6)
    ax.set_xticks(xs5)
    ax.set_xticklabels(ORDER, fontsize=10)
    ax.set_ylabel(r"$W_\mathrm{ad}$ (J/m²)", fontsize=12)
    ax.set_title("(c) Work of adhesion: paper vs 100-seed + expt", fontsize=12)
    ax.legend(frameon=False, fontsize=10, loc="upper right")
    ax2 = ax.twinx()
    ax2.plot(xs5, [EXPT_AJ[c] for c in ORDER], "D", color="#E63946",
             markersize=9, markeredgecolor="#404040", markeredgewidth=0.8)
    ax2.set_ylabel("Expt (aJ)", color="#E63946", fontsize=12)
    ax2.tick_params(axis="y", labelcolor="#E63946")
    ax.grid(axis="y", alpha=0.3)

    # ── (d) Paired Δ summary ─────────────────────────────────────────
    ax = axes[1, 1]
    keys = list(PAIRED.keys())
    deltas = [PAIRED[k][0] for k in keys]
    ses = [PAIRED[k][1] for k in keys]
    xs4 = np.arange(len(keys))
    cols4 = ["#2A9D8F" if abs(d) < 2*s else "#E63946"
             for d, s in zip(deltas, ses)]
    ax.bar(xs4, deltas, yerr=ses, capsize=5, color=cols4,
           edgecolor="#404040", lw=0.8, error_kw={"lw": 1.2})
    ax.axhline(0, color="#404040", lw=1)
    ax.set_xticks(xs4)
    ax.set_xticklabels(keys, fontsize=10)
    ax.set_ylabel(r"$\Delta W_\mathrm{ad}$ (J/m²)  [paired, same-seed]",
                  fontsize=11)
    ax.set_title("(d) Paired comparison (100 seeds)", fontsize=12)
    for x, d, s in zip(xs4, deltas, ses):
        sig = "✗ not sig." if abs(d) < 2*s else "✓ significant"
        ax.text(x, d + np.sign(d) * (s + 0.03) if d != 0 else s + 0.03,
                f"Δ={d:+.3f}\n{sig}", ha="center", fontsize=9,
                va="bottom" if d > 0 else "top")
    ax.grid(axis="y", alpha=0.3)

    fig.tight_layout()
    out = OUT / "master_summary.png"
    fig.savefig(out, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"  ✓ {out.name}")


if __name__ == "__main__":
    plot()
