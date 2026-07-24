#!/usr/bin/env python3
"""fig_comp2_icohp.py — comp2 (Li6PS5Cl0.5Br0.5) LOBSTER bond analysis.

Same-structure Cl-vs-Br comparison (no comp1 needed): Br weakens the Li-halide
bond. Two panels tell the dual-descriptor story:
  A) -ICOHP  = bond STRENGTH  -> P-S strong covalent framework, Li-X weak ionic,
                                 Li-Br (-1.934) < Li-Cl (-2.111) = Br softens.
  B)  ICOBI  = bond ORDER      -> P-S ~0.93 (covalent single bond), Li-X 0.28-0.38
                                 (ionic). Li-Br ~ Li-Cl ICOBI -> the weakening is
                                 IONIC (bond elongation), NOT a covalency change.

Source: db/compositions/comp2.json :: icohp_lobster_v3 (LOBSTER 5.1.1, all-PAW
nscf, comp2_V0_v3_relaxed champion, charge spilling 1.37%).
Outputs docs/figures/comp2/comp2_icohp.png + db/properties/comp2_icohp_origin.csv
"""
import csv
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))
from tools.figures.house_style import INK, MUT, ELEM, apply_axes  # noqa: E402

BR = "#a16207"  # amber-700 for Br (distinct from Cl lime / O crimson)
BONDCOL = {"P-S": ELEM["P"], "Li-S": ELEM["S"], "Li-Cl": ELEM["Cl"], "Li-Br": BR}

d = json.loads((REPO / "db/compositions/comp2.json").read_text())
ic = d["icohp_lobster_v3"]
order = ["P-S", "Li-S", "Li-Cl", "Li-Br"]
icohp = [ic["mean_ICOHP_eV"][b] for b in order]      # negative (bonding)
icobi = [ic["mean_ICOBI"][b] for b in order]
nb = [ic["n_bonds"][b] for b in order]
cut = [ic["distance_cutoff_A"][b] for b in order]
neg_icohp = [-v for v in icohp]                        # -ICOHP = strength (positive)
cols = [BONDCOL[b] for b in order]

fig, (axA, axB) = plt.subplots(1, 2, figsize=(9.4, 4.5), constrained_layout=True)
x = np.arange(len(order))

# ---- Panel A: -ICOHP (bond strength) ----
barsA = axA.bar(x, neg_icohp, color=cols, width=0.66, zorder=3)
for xi, v, n in zip(x, neg_icohp, nb):
    axA.text(xi, v + 0.12, f"{v:.2f}", ha="center", va="bottom",
             fontsize=10, color=INK, fontweight="bold")
    axA.text(xi, 0.14, f"n={n}", ha="center", va="bottom", fontsize=8, color="white",
             fontweight="bold", zorder=4)
apply_axes(axA, xlabel=None, ylabel="$-$ICOHP per bond (eV)",
           title="Bond strength")
axA.set_xticks(x); axA.set_xticklabels(order, fontsize=10.5, color=INK)
axA.set_ylim(0, max(neg_icohp) * 1.18)

# Li-Cl vs Li-Br delta callout (the money comparison)
i_cl, i_br = order.index("Li-Cl"), order.index("Li-Br")
ytop = max(neg_icohp[i_cl], neg_icohp[i_br]) + 0.62
axA.annotate("", xy=(i_br, ytop), xytext=(i_cl, ytop),
             arrowprops=dict(arrowstyle="<->", color=INK, lw=1.3))
dlt = neg_icohp[i_cl] - neg_icohp[i_br]
axA.text((i_cl + i_br) / 2, ytop + 0.06,
         f"Br weaker\n$\\Delta$ {dlt:.3f} eV", ha="center", va="bottom",
         fontsize=8.6, color=INK, fontweight="bold")

# ---- Panel B: ICOBI (bond order / covalency) ----
axB.bar(x, icobi, color=cols, width=0.66, zorder=3)
for xi, v in zip(x, icobi):
    axB.text(xi, v + 0.015, f"{v:.3f}", ha="center", va="bottom",
             fontsize=10, color=INK, fontweight="bold")
axB.axhline(1.0, color=MUT, ls=":", lw=1.2, zorder=1)
axB.text(len(order) - 0.5, 1.01, "single bond", ha="right", va="bottom",
         fontsize=7.8, color=MUT, style="italic")
apply_axes(axB, xlabel=None, ylabel="ICOBI per bond (bond order)",
           title="Bond order  (covalent vs ionic)")
axB.set_xticks(x); axB.set_xticklabels(order, fontsize=10.5, color=INK)
axB.set_ylim(0, 1.1)
axB.text(0, 0.90, "covalent", ha="center", fontsize=8, color=ELEM["P"], style="italic")
axB.text(2.5, 0.44, "ionic (Li-halide)", ha="center", fontsize=8, color=MUT, style="italic")

fig.suptitle("comp2  Li$_6$PS$_5$Cl$_{0.5}$Br$_{0.5}$  —  LOBSTER: Br softens the ionic Li-halide bond",
             fontsize=11.5, color=INK, y=1.06)
fig.text(0.5, -0.04,
         "Same-structure Cl-vs-Br (v3 champion, charge spilling 1.37%).  "
         "P-S: strong covalent framework (ICOBI~0.93, robust to Br).  "
         "Li-Br ICOBI (0.280) ~ Li-Cl (0.288) -> weakening is IONIC (bond elongation), not covalency.",
         ha="center", fontsize=7.6, color=MUT)

OUTD = REPO / "docs/figures/comp2"; OUTD.mkdir(parents=True, exist_ok=True)
png = OUTD / "comp2_icohp.png"
fig.savefig(png, dpi=300, bbox_inches="tight")
print("->", png)

# ---- Origin-ready CSV ----
csvp = REPO / "db/properties/comp2_icohp_origin.csv"
with open(csvp, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["bond", "n_bonds", "ICOHP_eV_mean", "neg_ICOHP_eV_strength",
                "ICOBI_mean_bondorder", "distance_cutoff_A", "character"])
    charmap = {"P-S": "covalent framework", "Li-S": "ionic", "Li-Cl": "ionic",
               "Li-Br": "ionic (weakest)"}
    for b, ih, ni, ib, ct in zip(order, icohp, nb, icobi, cut):
        w.writerow([b, ni, f"{ih:.3f}", f"{-ih:.3f}", f"{ib:.3f}", ct, charmap[b]])
print("->", csvp)
print(f"Li-Cl {neg_icohp[i_cl]:.3f} vs Li-Br {neg_icohp[i_br]:.3f} eV  (Br weaker by {dlt:.3f} eV)")
