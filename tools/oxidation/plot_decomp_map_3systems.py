#!/usr/bin/env python3
"""plot_decomp_map_3systems.py — grand-potential decomposition map, 3 systems.
Extends tools/oxidation/plot_esw_staircase.py (comp1 + modelc) with the
Nd2O3-doped row. Bar colors = thermodynamic state (blue reduced / green stable /
red oxidized). Breakpoint lines = decomposition onsets; GREEN bold = WIDE-GAP
(electron-blocking) product, black = conductive product. The Nd row carries the
honest dual message: intrinsic stable window is NARROWER (1.52-1.92 = 0.40 V),
but oxidation yields wide-gap passivators NdPO4 (2.45) / NdCl3 (2.62) / Nd(PO3)3
(3.66) that comp1/modelc never form.
Data: db/properties/oxidation_stability.json (comp1, modelc, nd_doped);
nd staircase tools/oxidation/esw_nd_result.txt.
"""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mp
import os

BLK, GRN = "0.0", "#1a7a34"   # conductive label vs wide-gap label
# (V, label, is_widegap).  reduction-limit entry has empty label.
SYS = {
    "LPSCl": dict(red=1.24, ox=2.14, marks=[
        (1.24, "", False), (2.14, "S$^{2-}$→S$_n^{2-}$", False),
        (2.36, "P–S→P$_2$S$_7$", False), (3.06, "→S$^0$", False),
        (3.33, "Cl$^-$→SCl", False)]),
    "LPSCl$_{1.6}$": dict(red=1.24, ox=2.14, marks=[
        (1.24, "", False), (2.14, "S$^{2-}$→S$_n^{2-}$", False),
        (2.36, "P–S→P$_2$S$_7$", False), (3.06, "→S$^0$", False),
        (3.33, "Cl$^-$→SCl", False), (3.39, "→PCl$_5$", False)]),
    "Nd$_2$O$_3$-doped": dict(red=1.52, ox=1.92, marks=[
        (1.52, "", False), (1.92, "Nd–S→Nd$_{10}$S$_{19}$", False),
        (2.36, "→P$_2$S$_7$", False), (2.45, "→NdPO$_4$", True),
        (2.62, "→NdCl$_3$", True), (3.06, "→S$^0$", False),
        (3.39, "→PCl$_5$", False), (3.66, "→Nd(PO$_3$)$_3$", True)]),
}
ROWY = {"LPSCl": 4.0, "LPSCl$_{1.6}$": 2.0, "Nd$_2$O$_3$-doped": 0.0}
XMAX, barh = 3.7, 0.5

fig, ax = plt.subplots(figsize=(12.4, 6.4))
for nm, yy in ROWY.items():
    s = SYS[nm]; red, ox = s["red"], s["ox"]
    ax.barh(yy, red,        left=0,   height=barh, color="#aec7e8", zorder=1)        # reduced
    ax.barh(yy, ox-red,     left=red, height=barh, color="#5cb85c", zorder=1)        # stable
    ax.barh(yy, XMAX-ox,    left=ox,  height=barh, color="#f2a0a0", zorder=1)        # oxidized
    for j, (v, lab, wg) in enumerate(s["marks"]):
        col = GRN if wg else "k"
        ax.plot([v, v], [yy-barh/2, yy+barh/2], color=col, lw=2.0 if wg else 1.0, zorder=3)
        if not lab:
            continue
        off = 0.46 + (j % 2) * 0.66
        ax.plot([v, v], [yy+barh/2, yy+off-0.04], color=(GRN if wg else "0.65"),
                lw=0.7, zorder=2)
        ax.annotate(f"{lab}\n{v:.2f} V", (v, yy+off), fontsize=8.6, ha="center",
                    va="bottom", zorder=4, color=(GRN if wg else BLK),
                    fontweight=("bold" if wg else "normal"))
    ax.text(-0.06, yy, nm, ha="right", va="center", fontsize=13, fontweight="bold")
    ax.text((red+ox)/2, yy, "OCV\n1.72", ha="center", va="center", fontsize=7, color="#1c4a1c")
    # narrower-window callout on the Nd row
    if nm.startswith("Nd"):
        ax.annotate("stable window 0.40 V\n(vs 0.90 V) — narrower",
                    (red, yy-barh/2-0.06), fontsize=7.8, ha="left", va="top",
                    color="#7a3b00", style="italic")

ax.set_xlim(-0.02, XMAX); ax.set_ylim(-0.95, 5.55); ax.set_yticks([])
ax.set_xlabel("V vs Li/Li$^+$", fontsize=12)
ax.set_title(
    "Grand-potential decomposition map (MP hull) — comp1 · modelc · Nd$_2$O$_3$-doped\n"
    "Nd$_2$O$_3$-doping: intrinsic window NARROWER, but oxidation yields "
    "WIDE-GAP passivators (NdPO$_4$, NdCl$_3$; green) vs conductive polysulfides",
    fontsize=11, pad=14)
for sp in ["top", "right", "left"]:
    ax.spines[sp].set_visible(False)
ax.legend(handles=[
    mp.Patch(color="#aec7e8", label="reduced"),
    mp.Patch(color="#5cb85c", label="stable"),
    mp.Patch(color="#f2a0a0", label="oxidized"),
    plt.Line2D([0], [0], color=GRN, lw=2.4, label="wide-gap (e$^-$-blocking) product"),
    plt.Line2D([0], [0], color="k", lw=1.2, label="conductive product"),
], loc="lower right", ncol=3, fontsize=8.4, frameon=False)
ax.text(0.0, -0.92, "HANYANG UNIVERSITY · Battery Materials lab", fontsize=8,
        color="0.45", ha="left", va="bottom")

OUT = os.path.join(os.path.dirname(__file__) or ".", "../../docs/figures/oxidation")
os.makedirs(os.path.abspath(OUT), exist_ok=True)
plt.tight_layout()
for ext in ("png", "pdf"):
    plt.savefig(os.path.join(OUT, f"decomp_map_3systems.{ext}"), dpi=200, bbox_inches="tight")
print("saved decomp_map_3systems.png/.pdf ->", os.path.abspath(OUT))
