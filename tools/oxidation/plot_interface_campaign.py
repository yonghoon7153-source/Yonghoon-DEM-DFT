#!/usr/bin/env python3
"""Interface campaign (3 seeds x 100 ps): controlled b2o3-vs-undoped comparison.
Entity colors match the project MSD/Arrhenius figures: b2o3=red, LPSCl1.6=blue."""
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

RED, BLUE, INK, MUT = "#d1352b", "#1f6fb4", "#222", "#666"

fig, (axA, axB) = plt.subplots(1, 2, figsize=(12.4, 4.8), gridspec_kw={"width_ratios": [1.05, 1]})

# ---- A: PS4-loss% across the three slabs ----
names = ["B$_2$O$_3$-doped\n(2× frame, 128)", "undoped LPSCl1.6\n(same 2× frame, 124)", "undoped 1× thin slab\n(62, only 5 P)"]
vals  = [21.8, 25.6, 48.1]; errs = [9.1, 0.0, 7.8]
x = np.arange(3)
bars = axA.bar(x[:2], vals[:2], 0.52, color=[RED, BLUE], edgecolor="white", lw=1)
axA.bar(x[2:], vals[2:], 0.52, facecolor="white", edgecolor=BLUE, lw=1.4, hatch="///")
axA.errorbar(x, vals, yerr=errs, fmt="none", ecolor=INK, capsize=5, elinewidth=1.3, zorder=5)
for xi, v, e in zip(x, vals, errs):
    axA.text(xi, v + e + 1.5, f"{v:.0f}±{e:.0f}%", ha="center", fontsize=10, color=INK, fontweight="bold")
# controlled-pair bracket
yb = 44
axA.plot([0, 0, 1, 1], [yb, yb+2, yb+2, yb], color=INK, lw=1.1)
axA.text(0.5, yb+3.2, "controlled pair — same surface, dopant isolated\n→ EQUAL within error (ratio 0.85 ± 0.36)",
         ha="center", fontsize=8.6, color=INK)
axA.annotate("same material as blue —\n½-thick slab inflates %\n(interface layer / P-count)\n= the old '6×' artifact",
             xy=(2, 48.1), xytext=(2.02, 62), fontsize=8, color=MUT, ha="center",
             arrowprops=dict(arrowstyle="-", color=MUT, lw=0.8))
axA.set_xticks(x); axA.set_xticklabels(names, fontsize=8.6)
axA.set_ylabel("PS$_4$ breakdown after 100 ps  (P–S loss, %)", fontsize=10.5)
axA.set_ylim(0, 74); axA.grid(axis="y", alpha=0.22, lw=0.6); axA.set_axisbelow(True)
axA.set_title("PS$_4$ framework loss at the Li interface", fontsize=11, fontweight="bold")

# ---- B: controlled ratios, all channels ----
ch = ["PS$_4$ break", "Li$_3$P form\n($\\Delta$P–Li)", "Li$_2$S form\n($\\Delta$S–Li)", "Li ingress"]
r  = [85.2, 102.0, 70.6, 95.5]; re = [35.6, 39.6, 21.7, 58.2]
xb = np.arange(4)
axB.axhline(100, color=INK, lw=1.1, ls="--")
axB.text(3.45, 103, "100% = equal", fontsize=8.5, color=INK, ha="right")
axB.bar(xb, r, 0.5, color=RED, edgecolor="white", lw=1)
axB.errorbar(xb, r, yerr=re, fmt="none", ecolor=INK, capsize=5, elinewidth=1.3, zorder=5)
for xi, v, e in zip(xb, r, re):
    axB.text(xi, v + e + 4, f"{v:.0f}±{e:.0f}", ha="center", fontsize=9.2, color=INK)
axB.set_xticks(xb); axB.set_xticklabels(ch, fontsize=8.8)
axB.set_ylabel("B$_2$O$_3$-doped, % of undoped (same frame)", fontsize=10.5)
axB.set_ylim(0, 175); axB.grid(axis="y", alpha=0.22, lw=0.6); axB.set_axisbelow(True)
axB.set_title("Every decomposition channel: doped ≈ undoped", fontsize=11, fontweight="bold")
axB.text(0.5, 0.955, "B–S = 3.00→3.00 in ALL seeds: BS$_3$ intact — no metallic LiB\n(the equilibrium worst-case is NOT realized dynamically)",
         transform=axB.transAxes, ha="center", va="top", fontsize=8.4, color="#0e7a6d",
         bbox=dict(boxstyle="round,pad=0.4", fc="#f2faf8", ec="#159a8a", lw=0.9))

fig.suptitle("Li-metal interface, 3-seed × 100 ps campaign  —  B$_2$O$_3$ does not worsen (no LiB, BS$_3$ robust); "
             "decomposition ≈ undoped; earlier '6×' was a thin-slab artifact", fontsize=11.3, fontweight="bold", y=1.015)
fig.tight_layout()
OUT = "interface_campaign_controlled.png"
fig.savefig(OUT, dpi=200, bbox_inches="tight"); print("saved", OUT)
