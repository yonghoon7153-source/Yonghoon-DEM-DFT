#!/usr/bin/env python3
"""
Br content vs mechanical properties — monotonic trend visualization.

Shows how Br substitution affects B0, E, and Wad separately within each family.

Source: kb/papers/final_report_v2.md Sections 3, 4-1, 5-2
"""
import json
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "output"
OUT.mkdir(exist_ok=True)

# Per-composition Br count per f.u. (cubic: 4 fu; rhombo: 5 fu)
DATA = {
    # id:      Br/fu   B0      E      Wad_paper  Wad_100s   family
    "comp1":   (0.0,   26.5,   29.1,  1.277,     1.151,    "Li6"),   # B0 v2 pipeline
    "comp2B":  (0.5,   25.8,   28.6,  1.183,     1.615,    "Li6"),
    "modelc":  (0.0,   21.7,   32.9,  None,      None,     "Li5.4"),
    "comp3":   (0.6,   20.8,   27.3,  2.103,     2.328,    "Li5.4"),
    "comp4":   (0.8,   20.8,   26.4,  1.970,     2.250,    "Li5.4"),
    "comp5":   (1.0,   22.9,   25.8,  1.651,     2.280,    "Li5.4"),
}

FAMILY_COLOR = {"Li6": "#9B5DE5", "Li5.4": "#4FBDFF"}
FAMILY_MARKER = {"Li6": "s", "Li5.4": "o"}


def plot():
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.2))
    for ax, (prop_idx, title, ylabel) in zip(
        axes,
        [(1, "B₀ (DFT EOS)", "B₀ (GPa)"),
         (2, "E (MLIP 600K snap)", "E (GPa)"),
         (3, "Wₐd (paper)", "Wₐd (J/m²)")]
    ):
        for fam in ["Li6", "Li5.4"]:
            xs, ys, labels = [], [], []
            for cid, v in DATA.items():
                br, b0, ee, wp, w100, f = v
                if f != fam:
                    continue
                val = v[prop_idx]
                if val is None:
                    continue
                xs.append(br)
                ys.append(val)
                labels.append(cid)
            if not xs:
                continue
            order = np.argsort(xs)
            xs = np.array(xs)[order]
            ys = np.array(ys)[order]
            labels = [labels[i] for i in order]
            ax.plot(xs, ys, "-", color=FAMILY_COLOR[fam], lw=1.2, alpha=0.6)
            ax.scatter(xs, ys, s=130, color=FAMILY_COLOR[fam],
                       marker=FAMILY_MARKER[fam], edgecolor="#404040", lw=1,
                       label=f"{fam} family", zorder=3)
            for xi, yi, lab in zip(xs, ys, labels):
                ax.annotate(lab, (xi, yi), xytext=(4, 4),
                            textcoords="offset points", fontsize=8)
        ax.set_xlabel("Br content per f.u.", fontsize=11)
        ax.set_ylabel(ylabel, fontsize=11)
        ax.set_title(title, fontsize=11)
        ax.grid(alpha=0.3)
        # legend only on first
    axes[0].legend(frameon=False, fontsize=10, loc="upper right")

    fig.suptitle("Br substitution effects (within each family)", fontsize=12, y=1.02)
    fig.tight_layout()
    out = OUT / "br_content_trend.png"
    fig.savefig(out, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"  ✓ {out.name}")

    with open(OUT / "br_content_summary.json", "w") as f:
        json.dump({k: {"Br_per_fu": v[0], "B0": v[1], "E": v[2],
                       "Wad_paper": v[3], "Wad_100s": v[4], "family": v[5]}
                   for k, v in DATA.items()}, f, indent=2)
    print("  ✓ br_content_summary.json")


if __name__ == "__main__":
    plot()
