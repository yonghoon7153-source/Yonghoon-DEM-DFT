#!/usr/bin/env python3
"""plot_esw_llzo_vs_lpscl.py — ESW comparison figure: garnet LLZO vs argyrodite LPSCl.

Data (grand-potential get_element_profile, MP GGA_GGA+U hull, same method/hull):
  • LLZO  Li7La3Zr2O12 : gabia 2026-06-23 (tools/oxidation/esw_llzo_result.txt)
  • LPSCl Li6PS5Cl     : our_dft_baseline.md §ESW (LiS4-excluded, Gil-González set)

Story: both oxidation onsets are ANION oxidation; O 2p sits deeper than S 3p, so
LLZO's onset (2.88 V, O2-→peroxide) is +0.63 V above LPSCl's (2.256 V, S2-→S0).
LLZO's bigger win is on the REDUCTION side (0.04 V, Zr4+/La3+ resist reduction).

No MP API needed — pure plotting from the numbers above.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

# ---- data ---------------------------------------------------------------
XMAX = 4.1
TEAL = "#1f7a8c"   # LLZO
GOLD = "#e08a1e"   # LPSCl
GREEN = "#bfe3b8"  # stable window
REDUC = "#d6e6f5"  # reduced zone
OXID = "#f6d4d4"   # oxidized zone

mats = {
    "LLZO":  dict(y=1.0, color=TEAL, red=0.04, ocv=0.05, ox=2.88,
                  formula=r"LLZO  (Li$_7$La$_3$Zr$_2$O$_{12}$)",
                  ox_rxn=r"O$^{2-}\!\rightarrow$Li$_2$O$_2$ (peroxide)",
                  red_rxn=r"Zr$^{4+}\!\rightarrow$Zr$_x$O",
                  steps=[(2.88, r"Li$_2$O$_2$"+"\n(peroxide)"),
                         (3.22, r"LiO$_8$"+"\n(superoxide)"),
                         (3.84, r"O$_2\!\uparrow$"+"\n(gas)")]),
    "LPSCl": dict(y=0.0, color=GOLD, red=1.242, ocv=1.717, ox=2.256,
                  formula=r"LPSCl  (Li$_6$PS$_5$Cl)",
                  ox_rxn=r"S$^{2-}\!\rightarrow$S$^0$",
                  red_rxn=r"P$^{5+}$/S$^{2-}$ reduced",
                  steps=[(2.256, r"S$^0$"),
                         (2.385, r"P$_2$S$_7$+S"),
                         (3.326, r"SCl")]),
}

fig, (ax1, ax2) = plt.subplots(
    2, 1, figsize=(9.2, 6.6), sharex=True,
    gridspec_kw=dict(height_ratios=[2.0, 1.25], hspace=0.12))

# ===== panel (a): ESW window bars =======================================
H = 0.42
for name, m in mats.items():
    y = m["y"]
    ax1.barh(y, m["red"] - 0.0, left=0.0, height=H, color=REDUC, zorder=2)
    ax1.barh(y, m["ox"] - m["red"], left=m["red"], height=H, color=GREEN,
             edgecolor=m["color"], lw=2.2, zorder=3)
    ax1.barh(y, XMAX - m["ox"], left=m["ox"], height=H, color=OXID, zorder=2)
    # limit labels
    ax1.text(m["red"], y + H/2 + 0.06, f"{m['red']:.2f} V", ha="center",
             va="bottom", fontsize=9, color="#3a6ea5", fontweight="bold")
    ax1.text(m["ox"], y + H/2 + 0.06, f"{m['ox']:.2f} V", ha="center",
             va="bottom", fontsize=9, color="#b03030", fontweight="bold")
    ax1.text(m["ox"] + 0.07, y, m["ox_rxn"], ha="left", va="center",
             fontsize=8.5, color="#7a2020")
    # window width inside the green bar
    ax1.text((m["red"] + m["ox"]) / 2, y, f"ESW {m['ox']-m['red']:.2f} V",
             ha="center", va="center", fontsize=9, fontweight="bold",
             color="#2e6b2e")
    ax1.text(-0.08, y, m["formula"], ha="right", va="center", fontsize=10,
             fontweight="bold", color=m["color"])

# +0.63 V oxidation-onset gap (anion effect)
for xo, c in [(mats["LPSCl"]["ox"], GOLD), (mats["LLZO"]["ox"], TEAL)]:
    ax1.plot([xo, xo], [-0.55, 1.78], ls=":", lw=1.3, color=c, zorder=1)
arr = FancyArrowPatch((mats["LPSCl"]["ox"], 1.62), (mats["LLZO"]["ox"], 1.62),
                      arrowstyle="<->", mutation_scale=13, lw=1.6, color="k")
ax1.add_patch(arr)
ax1.text((mats["LPSCl"]["ox"] + mats["LLZO"]["ox"]) / 2, 1.74,
         r"$\Delta$ = +0.63 V  (O$^{2-}$ harder to oxidize than S$^{2-}$)",
         ha="center", va="bottom", fontsize=9.5, fontweight="bold")

# context lines: Li metal & a typical oxide cathode
ax1.axvline(0.0, color="0.4", lw=1, ls="--")
ax1.text(0.0, -0.62, "Li metal\n(0 V)", ha="center", va="top", fontsize=8,
         color="0.35")
ax1.axvline(3.8, color="0.6", lw=1, ls="--")
ax1.text(3.8, -0.62, "oxide cathode\n(~3.8 V)", ha="center", va="top",
         fontsize=8, color="0.45")

# zone legend text
ax1.text(0.5, 1.93, "reduced", color="#3a6ea5", fontsize=8.5, ha="center")
ax1.text(1.55, 1.93, "stable window", color="#2e6b2e", fontsize=8.5, ha="center")
ax1.text(3.45, 1.93, "oxidized", color="#b03030", fontsize=8.5, ha="center")

ax1.set_ylim(-0.85, 2.15)
ax1.set_yticks([])
ax1.set_title("Electrochemical stability window (grand-potential, MP GGA/GGA+U) — "
              "garnet LLZO vs argyrodite LPSCl", fontsize=11, fontweight="bold")

# ===== panel (b): stepwise anion-oxidation ladder ========================
for name, m in mats.items():
    y = m["y"]
    ax2.plot([m["ox"], XMAX], [y, y], color=m["color"], lw=1.4, zorder=2)
    for j, (v, lab) in enumerate(m["steps"]):
        ax2.plot(v, y, "o", color=m["color"], ms=8, zorder=3)
        above = (j % 2 == 0)
        ax2.text(v, y + (0.17 if above else -0.34), lab, ha="center",
                 va="bottom" if above else "top", fontsize=8, color=m["color"])
    ax2.text(-0.08, y, name, ha="right", va="center", fontsize=10,
             fontweight="bold", color=m["color"])
ax2.set_ylim(-0.7, 1.7)
ax2.set_yticks([])
ax2.set_xlim(0, XMAX)
ax2.set_xlabel(r"Voltage vs Li/Li$^+$  (V)", fontsize=11)
ax2.set_title("Stepwise anion oxidation (decomposition breakpoints)",
              fontsize=10, fontweight="bold", loc="left")
ax2.text(0.02, 1.45,
         "S$^{2-}$ oxidizes early (2.26 V); O$^{2-}$ climbs a higher ladder: "
         "peroxide → superoxide → O$_2$",
         fontsize=8.5, color="0.3", transform=ax2.get_yaxis_transform()
         if False else ax2.transData)

for ax in (ax1, ax2):
    ax.set_xlim(0, XMAX)
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)

fig.text(0.985, 0.01,
         "grand-potential get_element_profile (Mo/Ong/Ceder); LLZO gabia 2026-06-23, "
         "LPSCl comp1 LiS4-excluded",
         ha="right", va="bottom", fontsize=6.5, color="0.5")

import os
out = os.path.join(os.path.dirname(__file__) or ".",
                   "../../litdb/figures/esw_llzo_vs_lpscl")
os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
fig.tight_layout(rect=(0.02, 0.02, 1, 1))
fig.savefig(out + ".png", dpi=300, bbox_inches="tight")
fig.savefig(out + ".pdf", bbox_inches="tight")
print("saved:", os.path.abspath(out) + ".png / .pdf")
