#!/usr/bin/env python3
"""
Coating figure-of-merit scatter plot.

Ideal cathode coating: LOW E (compliance) + HIGH Wad (adhesion).
Top-left corner of (E, Wad) plane = best coating candidate.

Figure of merit: FoM = Wad / E  (higher = better coating)

Outputs:
    output/coating_fom.png  — scatter + FoM contours + highlighted optimum
    output/coating_fom.json
"""
import json
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "output"
OUT.mkdir(exist_ok=True)

# Composition data (from final_report_v2.md)
#   key: (E, E_std, Wad, Wad_std, family, has_Wad)
DATA = {
    "comp1":   (29.1, 1.1, 1.277, 0.383, "Li6",   True),
    "comp2B":  (28.6, 1.1, 1.183, 0.362, "Li6",   True),
    "comp3":   (27.3, 0.4, 2.103, 0.245, "Li5.4", True),
    "comp4":   (26.4, 1.6, 1.970, 0.629, "Li5.4", True),
    "comp5":   (25.8, 0.8, 1.651, 0.284, "Li5.4", True),
    "modelc":  (32.9, 0.9, None,  None,  "Li5.4", False),  # Wad not measured
}

FAMILY_COLOR = {"Li6": "#9B5DE5", "Li5.4": "#4FBDFF"}
FAMILY_MARKER = {"Li6": "s", "Li5.4": "o"}


def plot():
    fig, ax = plt.subplots(figsize=(9, 7))

    # ── FoM contour (Wad / E = constant) ─────────────────────────────
    Es = np.linspace(23, 35, 200)
    Ws = np.linspace(0.8, 2.5, 200)
    EE, WW = np.meshgrid(Es, Ws)
    FoM = WW / EE   # J/m² per GPa (normalized ratio)

    # Contour lines at fixed FoM (higher = better)
    levels = [0.03, 0.05, 0.07, 0.09]
    CS = ax.contour(EE, WW, FoM, levels=levels, colors="#AAAAAA",
                    linewidths=0.9, linestyles="--", alpha=0.8)
    ax.clabel(CS, inline=True, fontsize=8, fmt="FoM=%.2f")

    # Shade "coating-favorable zone" (low E, high Wad)
    ax.fill_betweenx(Ws, 23, 27, where=Ws > 1.8, alpha=0.08, color="#2A9D8F",
                     label="Coating-favorable zone\n(E<27, Wad>1.8)")

    # ── Plot compositions ────────────────────────────────────────────
    for name, (E, Es_, W, Ws_, fam, hasW) in DATA.items():
        if not hasW:
            # show E on a side axis (as vertical line and label)
            ax.axvline(E, color=FAMILY_COLOR[fam], lw=0.8, ls=":", alpha=0.6)
            ax.annotate(f"{name} (E={E}, no Wad)", (E, 0.85),
                        fontsize=9, color=FAMILY_COLOR[fam],
                        rotation=90, va="bottom", ha="right")
            continue
        ax.errorbar(E, W, xerr=Es_, yerr=Ws_, fmt=FAMILY_MARKER[fam],
                    markersize=14, color=FAMILY_COLOR[fam],
                    markeredgecolor="#404040", markeredgewidth=1.2,
                    ecolor="#666666", capsize=3, elinewidth=1, zorder=3)
        # FoM text
        fom = W / E
        ax.annotate(f"{name}\nFoM={fom:.3f}",
                    (E, W), xytext=(8, 8),
                    textcoords="offset points", fontsize=10,
                    bbox=dict(facecolor="white", edgecolor="#CCCCCC",
                              alpha=0.85, pad=3))

    # Champion star on comp4 (balance winner)
    Ec, Wc = DATA["comp4"][0], DATA["comp4"][2]
    ax.scatter(Ec, Wc, marker="*", s=600, color="#F4A261",
               edgecolor="#404040", lw=1.5, zorder=4,
               label="★ Balance champion (comp4)")

    # Ideal direction arrow
    ax.annotate("", xy=(24, 2.3), xytext=(31, 1.0),
                arrowprops=dict(arrowstyle="->", color="#2A9D8F", lw=2))
    ax.text(24.5, 2.35, "Ideal direction\n(soft + sticky)",
            fontsize=11, color="#2A9D8F", fontweight="bold",
            ha="left", va="bottom")

    # ── Legends / labels ─────────────────────────────────────────────
    # family legend
    handles = [
        plt.Line2D([0], [0], marker="s", linestyle="", markersize=11,
                   color=FAMILY_COLOR["Li6"], markeredgecolor="#404040",
                   label="Li6 family"),
        plt.Line2D([0], [0], marker="o", linestyle="", markersize=11,
                   color=FAMILY_COLOR["Li5.4"], markeredgecolor="#404040",
                   label="Li5.4 family"),
        plt.Line2D([0], [0], marker="*", linestyle="", markersize=15,
                   color="#F4A261", markeredgecolor="#404040",
                   label="Balance champion"),
    ]
    ax.legend(handles=handles, frameon=False, fontsize=11, loc="upper right")

    ax.set_xlabel("Young's modulus E (GPa)  —  lower = better compliance",
                  fontsize=12)
    ax.set_ylabel(r"Work of adhesion $W_\mathrm{ad}$ (J/m²)  —  higher = better adhesion",
                  fontsize=12)
    ax.set_title("Cathode coating figure-of-merit (FoM = Wad / E)",
                 fontsize=13)
    ax.set_xlim(23, 35)
    ax.set_ylim(0.8, 2.5)
    ax.grid(alpha=0.3)

    fig.tight_layout()
    out = OUT / "coating_fom.png"
    fig.savefig(out, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"  ✓ {out.name}")

    # Summary
    summary = {}
    for name, (E, _, W, _, fam, hasW) in DATA.items():
        entry = {"E": E, "family": fam}
        if hasW:
            entry["Wad"] = W
            entry["FoM"] = W / E
        summary[name] = entry
    # ranking
    ranked = sorted(
        [(k, v["FoM"]) for k, v in summary.items() if "FoM" in v],
        key=lambda x: -x[1])
    summary["_ranking_by_FoM"] = [(k, round(v, 4)) for k, v in ranked]
    summary["_coating_interpretation"] = {
        "rule": "Lower E (compliance) + Higher Wad (adhesion) = better coating",
        "highest_FoM": ranked[0][0],
        "balance_champion": "comp4",
        "balance_reason": "middle of Li5.4 trend, stable basin, E-Wad compromise"
    }
    with open(OUT / "coating_fom.json", "w") as f:
        json.dump(summary, f, indent=2)
    print(f"  ✓ coating_fom.json")
    print("\nFoM ranking (Wad/E, higher = better):")
    for k, v in ranked:
        print(f"  {k}: {v:.4f}")


if __name__ == "__main__":
    plot()
