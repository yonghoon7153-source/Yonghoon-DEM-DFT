#!/usr/bin/env python3
"""plot_xps_reference_sei.py — where the Nd-SEI XPS peaks appear. One panel per
core-level region (P 2p / S 2p / Cl 2p / O 1s / Nd 3d / Li 1s); each SEI product
plotted at its literature BE (xerr = reported spread), colored by interface role,
open marker = low-confidence (Nd 3d multiplet). Diagnostic shifts annotated.
Source: db/properties/xps_reference_sei.csv (lit/NIST, C 1s 284.8 ref).
This is the EXPERIMENTAL ANCHOR for the ORCA dSCF core-hole calc.
"""
import csv, io, os
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
OUT = "docs/figures/nd_sei"; os.makedirs(OUT, exist_ok=True)

raw = open("db/properties/xps_reference_sei.csv").read().splitlines()
h = next(i for i, l in enumerate(raw) if l.startswith("product,"))
rows = list(csv.DictReader(io.StringIO("\n".join(raw[h:]))))

def cat(role):
    r = role.lower()
    if "leak" in r or "avoid" in r: return "leak/avoid"
    if "marker" in r: return "ox-marker"
    if "host" in r: return "host backbone"
    if "anode" in r and "cathode" in r: return "anode+cathode SEI"
    if "anode" in r: return "anode SEI"
    return "cathode passivation"
COL = {"anode SEI": "#1e88e5", "anode+cathode SEI": "#26a69a", "cathode passivation": "#e65100",
       "host backbone": "#6d4c41", "leak/avoid": "#b71c1c", "ox-marker": "#8e24aa"}

# panels: (element, core_level, x-range, title, optional diagnostic annotation)
PANELS = [
    ("P", "2p3/2", (126, 136), "P 2p$_{3/2}$ — thiophosphate→phosphate = O-doping signature"),
    ("S", "2p3/2", (158, 170), "S 2p$_{3/2}$ — sulfide vs oxidized-S (sulfate) marker"),
    ("Cl", "2p3/2", (197, 201), "Cl 2p$_{3/2}$ — LiCl vs Nd-chloride"),
    ("O", "1s", (527, 533), "O 1s — oxide / RE-oxide / phosphate ladder"),
    ("Nd", "3d5/2", (979, 985), "Nd 3d$_{5/2}$ — Nd$^{3+}$ ~982 (+satellite); open=multiplet-limited"),
    ("Li", "1s", (52, 58), "Li 1s — low resolution, overlapping (support only)"),
]
fig, axs = plt.subplots(3, 2, figsize=(15, 12)); axs = axs.ravel()
for ax, (el, cl, xlim, title) in zip(axs, PANELS):
    sub = [r for r in rows if r["element"] == el and r["core_level"] == cl]
    sub.sort(key=lambda r: float(r["BE_eV"]))
    for i, r in enumerate(sub):
        be = float(r["BE_eV"]); pm = float(r["BE_pm"]); c = COL[cat(r["role_side"])]
        filled = r["conf"] in ("A", "B")
        ax.errorbar(be, i, xerr=pm, fmt="o", ms=11, color=c, ecolor=c, elinewidth=1.4, capsize=3,
                    mfc=(c if filled else "white"), mec=c, mew=1.8, zorder=4)
        ax.text(be, i + 0.28, r["product"].replace("_", " "), fontsize=7.2, ha="center", va="bottom")
        ax.text(be, i - 0.30, f"{be:.1f} ({r['conf']})", fontsize=6.6, ha="center", va="top", color="0.35")
    ax.set_xlim(*xlim); ax.set_ylim(-0.8, len(sub) - 0.2 + 0.6)
    ax.set_yticks([]); ax.set_xlabel("binding energy (eV)"); ax.set_title(title, fontsize=9.5)
    ax.grid(axis="x", alpha=.3)
    # diagnostic annotations
    if el == "P":
        ax.annotate("", xy=(133.3, 0.5), xytext=(131.7, 0.5),
                    arrowprops=dict(arrowstyle="->", color="#e65100", lw=2))
        ax.text(132.5, 0.62, "+1.6 eV\nO-doping", fontsize=7.5, ha="center", color="#e65100", fontweight="bold")
    if el == "Nd":
        ax.axvspan(982, 987, color="#e65100", alpha=.08); ax.text(984.5, len(sub)-1, "satellite\nregion", fontsize=7, ha="center", color="#e65100")

handles = [Line2D([0],[0], marker="o", ls="", mfc=COL[k], mec=COL[k], ms=9, label=k) for k in COL]
handles += [Line2D([0],[0], marker="o", ls="", mfc="white", mec="0.3", mew=1.8, ms=9, label="open = low conf (C)")]
fig.legend(handles=handles, loc="lower center", ncol=4, fontsize=8.5, bbox_to_anchor=(0.5, -0.02))
plt.suptitle("Nd₂O₃-doped LPSCl — SEI/decomposition XPS reference positions (lit anchors for ORCA ΔSCF)\n"
             "charge-ref C 1s 284.8 eV · 2p = 2p₃/₂ component · conf A/B/C", fontsize=12.5, y=1.0)
plt.tight_layout(rect=[0, 0.03, 1, 1])
plt.savefig(f"{OUT}/xps_reference_sei.png", dpi=150, bbox_inches="tight")
plt.savefig(f"{OUT}/xps_reference_sei.pdf", bbox_inches="tight")
print(f"saved {OUT}/xps_reference_sei.png")
# console: the diagnostic ladders
print("\n=== O 1s ladder (oxide -> phosphate) ===")
for r in sorted([r for r in rows if r["element"]=="O"], key=lambda r: float(r["BE_eV"])):
    print(f"  {float(r['BE_eV']):6.1f}  {r['product']:28s} ({r['conf']})")
print("=== P 2p (phosphide / thiophosphate / phosphate) ===")
for r in sorted([r for r in rows if r["element"]=="P"], key=lambda r: float(r["BE_eV"])):
    print(f"  {float(r['BE_eV']):6.1f}  {r['product']:28s} ({r['conf']})")
