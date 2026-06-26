#!/usr/bin/env python3
"""plot_xps_nd_only.py — ONLY the Nd-related XPS peaks of the Nd-SEI system.
Headline panel = Nd 3d (3d5/2 + derived 3d3/2 + screened satellite note); the
small panels = companion anion peaks (O 1s / P 2p / Cl 2p / S 2p) restricted to
Nd-bearing phases, i.e. the fingerprints that tell you WHICH Nd compound.
Source: db/properties/xps_reference_sei.csv (lit/NIST, C 1s 284.8 ref).
Also writes db/properties/xps_reference_nd_only.csv (filtered) and prints a table.
"""
import csv, io, os
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

OUT = "docs/figures/nd_sei"; os.makedirs(OUT, exist_ok=True)
raw = open("db/properties/xps_reference_sei.csv").read().splitlines()
h = next(i for i, l in enumerate(raw) if l.startswith("product,"))
rows = list(csv.DictReader(io.StringIO("\n".join(raw[h:]))))

# Nd-related = Nd-bearing compounds (product contains 'Nd')
nd_rows = [r for r in rows if "Nd" in r["product"]]
ND_SOSPLIT = 22.5  # Nd 3d3/2 = 3d5/2 + ~22.5 eV

# write filtered CSV
os.makedirs("db/properties", exist_ok=True)
with open("db/properties/xps_reference_nd_only.csv", "w") as f:
    f.write("# Nd-RELATED XPS peaks only (filtered from xps_reference_sei.csv).\n")
    f.write("# Nd-bearing SEI/decomposition phases. C 1s 284.8 eV ref. 2p=2p3/2; Nd 3d3/2 = 3d5/2 + ~22.5 eV.\n")
    f.write("# conf A/B well-established; C = Nd 3d multiplet/satellite-limited, per-ligand shift is an ESTIMATE.\n")
    f.write("product,element,core_level,BE_eV,BE_pm,conf,diagnostic\n")
    for r in nd_rows:
        f.write(f"{r['product']},{r['element']},{r['core_level']},{r['BE_eV']},{r['BE_pm']},{r['conf']},{r['diagnostic']}\n")

# color per Nd phase
phases = sorted({r["product"] for r in nd_rows})
cmap = plt.cm.tab10
PC = {p: cmap(i % 10) for i, p in enumerate(phases)}

fig = plt.figure(figsize=(15, 8.2))
gs = fig.add_gridspec(2, 4, height_ratios=[1.35, 1], hspace=0.42, wspace=0.30)
axNd = fig.add_subplot(gs[0, :])           # headline Nd 3d
axsm = [fig.add_subplot(gs[1, i]) for i in range(4)]

# ---- headline: Nd 3d (5/2 + derived 3/2) ----
nd3d = sorted([r for r in nd_rows if r["element"] == "Nd"], key=lambda r: float(r["BE_eV"]))
for i, r in enumerate(nd3d):
    be = float(r["BE_eV"]); pm = float(r["BE_pm"]); c = PC[r["product"]]
    for x, lab, ms in [(be, "3d$_{5/2}$", 13), (be + ND_SOSPLIT, "3d$_{3/2}$", 10)]:
        axNd.errorbar(x, i, xerr=pm, fmt="o", ms=ms, color=c, ecolor=c, elinewidth=1.4,
                      capsize=3, mfc="white", mec=c, mew=2.0, zorder=4)
        axNd.text(x, i + 0.26, f"{x:.1f}", fontsize=7.5, ha="center", va="bottom", color="0.3")
    axNd.text(975.0, i, r["product"], fontsize=9, ha="right", va="center", color=c, fontweight="bold")
axNd.axvspan(976.0, 978.5, color="0.85", alpha=0.5, zorder=0)
axNd.text(977.2, len(nd3d) - 0.4, "screened\nsatellite ~977", fontsize=7.5, ha="center", va="top", color="0.45")
axNd.axvline(982.5, ls=":", color="#e65100", lw=1.3)
axNd.set_xlim(972, 1010); axNd.set_ylim(-0.7, len(nd3d) - 0.3)
axNd.set_yticks([]); axNd.set_xlabel("binding energy (eV)")
axNd.set_title("Nd 3d  —  the direct Nd fingerprint:  Nd$^{3+}$ 3d$_{5/2}$ ≈ 982.5 eV (+ satellite ~977),  "
               "3d$_{3/2}$ ≈ 1005 eV.  open marker = conf C (multiplet/satellite-limited)", fontsize=10)
axNd.grid(axis="x", alpha=0.3)

# ---- companion anion fingerprints (Nd compounds only) ----
SMALL = [("O", "1s", (527.5, 532.5), "O 1s"),
         ("P", "2p3/2", (131, 135), "P 2p$_{3/2}$"),
         ("Cl", "2p3/2", (197.5, 200.5), "Cl 2p$_{3/2}$"),
         ("S", "2p3/2", (159, 163), "S 2p$_{3/2}$")]
for ax, (el, cl, xlim, title) in zip(axsm, SMALL):
    sub = sorted([r for r in nd_rows if r["element"] == el and r["core_level"] == cl],
                 key=lambda r: float(r["BE_eV"]))
    for i, r in enumerate(sub):
        be = float(r["BE_eV"]); pm = float(r["BE_pm"]); c = PC[r["product"]]
        filled = r["conf"] in ("A", "B")
        ax.errorbar(be, i, xerr=pm, fmt="o", ms=10, color=c, ecolor=c, elinewidth=1.3, capsize=3,
                    mfc=(c if filled else "white"), mec=c, mew=1.8, zorder=4)
        ax.text(be, i + 0.30, r["product"].replace("Nd", "Nd "), fontsize=7, ha="center", va="bottom", color=c)
        ax.text(be, i - 0.32, f"{be:.1f}", fontsize=6.8, ha="center", va="top", color="0.35")
    ax.set_xlim(*xlim); ax.set_ylim(-0.9, max(len(sub) - 0.2, 0.8) + 0.5)
    ax.set_yticks([]); ax.set_xlabel("BE (eV)"); ax.set_title(title, fontsize=9.5)
    ax.grid(axis="x", alpha=0.3)

handles = [Line2D([0], [0], marker="o", ls="", mfc=PC[p], mec=PC[p], ms=9, label=p) for p in phases]
handles += [Line2D([0], [0], marker="o", ls="", mfc="white", mec="0.3", mew=1.8, ms=9, label="open = conf C (estimate)")]
fig.legend(handles=handles, loc="lower center", ncol=5, fontsize=8.5, bbox_to_anchor=(0.5, -0.03))
fig.suptitle("Nd-related XPS peak positions — Nd-bearing SEI/decomposition phases (literature anchors)\n"
             "C 1s 284.8 eV ref · Nd 3d lineshape is multiplet/satellite-complex (orientation, not citation)",
             fontsize=12.5, y=0.99)
fig.savefig(f"{OUT}/xps_nd_only.png", dpi=150, bbox_inches="tight")
fig.savefig(f"{OUT}/xps_nd_only.pdf", bbox_inches="tight")
print(f"saved {OUT}/xps_nd_only.png  ({len(nd_rows)} Nd-related peaks, {len(phases)} phases)")

# ---- console table ----
print("\n=== Nd-RELATED XPS PEAKS (where they appear) ===")
print(f"{'phase':10s} {'element/level':14s} {'BE (eV)':>10s}  conf  diagnostic")
for r in sorted(nd_rows, key=lambda r: (r["product"], float(r["BE_eV"]))):
    print(f"{r['product']:10s} {r['element']+' '+r['core_level']:14s} "
          f"{float(r['BE_eV']):8.1f}±{float(r['BE_pm']):.1f}  {r['conf']:>3s}   {r['diagnostic'][:46]}")
print("\nNd 3d3/2 component = listed 3d5/2 + ~22.5 eV (e.g. Nd2O3: 982.5 -> 1005.0)")
