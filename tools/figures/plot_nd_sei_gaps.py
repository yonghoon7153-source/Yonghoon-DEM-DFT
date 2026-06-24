#!/usr/bin/env python3
"""plot_nd_sei_gaps.py — SEI/decomposition product band gaps (Materials Project)
for the Nd2O3-doped LPSCl1.6 story, framed around the O EFFECT:
O makes wide-gap insulating passivators (Li3PO4, Li2O) vs the conductive
leak products (Li3P, Li2S, polysulfide) that form without O.
Data: db/properties electronic / sei_product_gaps.py (MP). Nd-containing gaps
are MP lower bounds (4f). No MP API needed here (numbers hard-coded from run).
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

# (label, gap_eV, contains_O, nd_lower_bound)
DATA = [
    ("LiCl",     6.65, False, False),
    ("Li$_3$PO$_4$", 5.73, True,  False),
    ("NdPO$_4$", 5.55, True,  True),
    ("Li$_2$O",  5.24, True,  False),
    ("NdOCl",    4.77, True,  True),
    ("NdCl$_3$", 4.30, False, True),
    ("LiNdO$_2$",4.21, True,  True),
    ("Li$_2$S",  3.90, False, False),
    ("Nd$_2$O$_3$",3.81,True, True),
    ("Nd$_2$S$_3$",1.79,False,True),
    ("Li$_3$P",  0.70, False, False),
    ("NdS",      0.00, False, True),
]
DATA.sort(key=lambda r: r[1])  # ascending -> conductive at bottom

labels = [d[0] for d in DATA]
gaps   = [d[1] for d in DATA]

def color(g):
    if g >= 4.0:  return "#3a9e54"   # insulator -> passivation (green)
    if g >= 2.0:  return "#e0a13a"   # marginal (amber)
    return "#c0392b"                 # conductive leak (red)

cols = [color(g) for g in gaps]

fig, ax = plt.subplots(figsize=(8.6, 5.4))
y = range(len(labels))
bars = ax.barh(list(y), gaps, color=cols, edgecolor="black", lw=0.6, zorder=3)

# O-derived -> blue outline + (O) tag
for i, d in enumerate(DATA):
    if d[2]:
        bars[i].set_edgecolor("#1f4fb0"); bars[i].set_linewidth(2.2)
    lb = "" if not d[3] else "  *"     # Nd lower-bound marker
    ax.text(d[1] + 0.08, i, f"{d[1]:.2f}{lb}", va="center", ha="left",
            fontsize=8.5, fontweight="bold" if d[2] else "normal")

ax.set_yticks(list(y)); ax.set_yticklabels(labels, fontsize=10)
ax.set_xlabel("band gap (eV, Materials Project)", fontsize=11)
ax.set_xlim(0, 7.6)
ax.axvline(2.0, ls="--", lw=1, color="0.4")
ax.text(2.0, len(labels)-0.3, "  conductive-leak threshold (~2 eV)",
        color="0.35", fontsize=8, va="top")
ax.set_title("SEI / decomposition-product band gaps — the O effect\n"
             "O makes wide-gap passivators (Li$_3$PO$_4$ 5.73, Li$_2$O 5.24); "
             "without O → conductive leak (Li$_3$P, Li$_2$S)",
             fontsize=10.5, fontweight="bold")

legend = [
    Patch(fc="#3a9e54", ec="black", label="insulator ≥4 eV → passivation"),
    Patch(fc="#e0a13a", ec="black", label="marginal 2–4 eV"),
    Patch(fc="#c0392b", ec="black", label="conductive <2 eV → e⁻ leak"),
    Patch(fc="white",  ec="#1f4fb0", lw=2.2, label="O-derived phase"),
]
ax.legend(handles=legend, loc="lower right", fontsize=8.5, framealpha=0.95)
ax.text(0.99, 0.02, "* Nd-containing = MP lower bound (4f)",
        transform=ax.transAxes, ha="right", va="bottom", fontsize=7, color="0.5")
for sp in ("top", "right"): ax.spines[sp].set_visible(False)

import os
out = os.path.join(os.path.dirname(__file__) or ".", "../../docs/figures/nd_sei/sei_product_gaps_O")
os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
fig.tight_layout()
fig.savefig(out + ".png", dpi=300, bbox_inches="tight")
fig.savefig(out + ".pdf", bbox_inches="tight")
print("saved:", os.path.abspath(out) + ".png / .pdf")
