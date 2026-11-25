#!/usr/bin/env python3
"""fig_comp2_halide_lengths.py — Li-halide bond-length distributions.

Panel-(iv) style: Li-Cl length histogram, LPSCl (comp1) vs LPSCl0.5Br0.5 (comp2),
PLUS comp2 Li-Br (the size story: Br larger -> longer, softer bond).

Measured directly from the DFT-relaxed structures with PBC minimum-image:
  comp1 = db/structures/comp1_V0_k444.xyz  (Li6PS5Cl)
  comp2 = db/structures/comp2_V0_v3_relaxed.xyz  (Li6PS5Cl0.5Br0.5, v3 champion)
Cutoffs match comp2.json v3 bond_lengths (Li-Cl 3.2 / Li-Br 3.4 A).
Cross-check comp2: Li-Cl 2.597+/-0.223 (n=10), Li-Br 2.752+/-0.164 (n=12).
Outputs docs/figures/comp2/comp2_halide_lengths.png
      + db/properties/comp2_halide_lengths_origin.csv
"""
import csv
import re
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))
from tools.figures.house_style import INK, MUT, ELEM, SYS, apply_axes  # noqa: E402

BR = "#a16207"


def read_xyz(path):
    """Extended-XYZ -> (lattice 3x3 or None, list[(elem, xyz)])."""
    lines = Path(path).read_text().splitlines()
    nat = int(lines[0].split()[0])
    m = re.search(r'Lattice="([^"]+)"', lines[1])
    A = np.array([float(x) for x in m.group(1).split()]).reshape(3, 3) if m else None
    atoms = []
    for ln in lines[2:2 + nat]:
        t = ln.split()
        atoms.append((re.sub(r"\d", "", t[0]), np.array([float(t[1]), float(t[2]), float(t[3])])))
    return A, atoms


def pair_lengths(path, a_elem, b_elem, cutoff):
    """All a-b distances <= cutoff under PBC minimum-image."""
    A, atoms = read_xyz(path)
    ai = [p for e, p in atoms if e == a_elem]
    bi = [p for e, p in atoms if e == b_elem]
    inv = np.linalg.inv(A) if A is not None else None
    out = []
    for pa in ai:
        for pb in bi:
            d = pb - pa
            if inv is not None:
                f = d @ inv
                f -= np.round(f)
                d = f @ A
            r = np.linalg.norm(d)
            if 0.1 < r <= cutoff:
                out.append(r)
    return np.array(out)


C1 = REPO / "db/structures/comp1_V0_k444.xyz"
C2 = REPO / "db/structures/comp2_V0_v3_relaxed.xyz"

dist = {
    "comp1 Li-Cl": pair_lengths(C1, "Li", "Cl", 3.2),
    "comp2 Li-Cl": pair_lengths(C2, "Li", "Cl", 3.2),
    "comp2 Li-Br": pair_lengths(C2, "Li", "Br", 3.4),
}
print("=== measured (cross-check comp2.json v3: Li-Cl 2.597+/-0.223 n10, Li-Br 2.752+/-0.164 n12) ===")
for k, v in dist.items():
    print(f"  {k}: n={len(v)}  mean={v.mean():.3f}  std={v.std():.3f} A")

STY = {
    "comp1 Li-Cl": dict(color=SYS["comp1"], hatch=None),
    "comp2 Li-Cl": dict(color=ELEM["Cl"], hatch=None),
    "comp2 Li-Br": dict(color=BR, hatch=None),
}
bins = np.arange(2.2, 3.25, 0.075)
fig, ax = plt.subplots(figsize=(6.8, 4.8), constrained_layout=True)
# comp1 Li-Cl = reference outline (has 2x the Cl bonds; step avoids fill-dominance)
v = dist["comp1 Li-Cl"]
ax.hist(v, bins=bins, histtype="step", color=SYS["comp1"], lw=2.0,
        label=f"comp1 Li-Cl (LPSCl)  ({v.mean():.2f}$\\pm${v.std():.2f} A, n={len(v)})")
ax.axvline(v.mean(), color=SYS["comp1"], ls=":", lw=1.6)
# comp2 Li-Cl / Li-Br = filled (the same-cell size story)
for k in ["comp2 Li-Cl", "comp2 Li-Br"]:
    v = dist[k]
    ax.hist(v, bins=bins, color=STY[k]["color"], alpha=0.55, edgecolor=STY[k]["color"],
            lw=1.4, label=f"{k}  ({v.mean():.2f}$\\pm${v.std():.2f} A, n={len(v)})")
    ax.axvline(v.mean(), color=STY[k]["color"], ls="--", lw=1.8)

apply_axes(ax, xlabel="Li-halide bond length (A)", ylabel="Counts (bonds in cell)",
           title="Li-halide lengths — Br is larger -> longer, softer bond")
ax.legend(loc="upper right", fontsize=8.5, frameon=False)
# size-effect annotation between Li-Cl and Li-Br means
mcl, mbr = dist["comp2 Li-Cl"].mean(), dist["comp2 Li-Br"].mean()
ax.annotate("", xy=(mbr, ax.get_ylim()[1] * 0.62), xytext=(mcl, ax.get_ylim()[1] * 0.62),
            arrowprops=dict(arrowstyle="->", color=INK, lw=1.3))
ax.text((mcl + mbr) / 2, ax.get_ylim()[1] * 0.64, f"+{mbr - mcl:.2f} A",
        ha="center", va="bottom", fontsize=9, color=INK, fontweight="bold")
fig.text(0.5, -0.03,
         "DFT-relaxed cells (comp1 k444 / comp2 v3 champion), PBC min-image, cutoff Li-Cl 3.2 / Li-Br 3.4 A.  "
         "Larger Li-Br length = lower ion-packing density = softer lattice + weaker Li-Br ICOHP (-1.934 < -2.111).",
         ha="center", fontsize=7.4, color=MUT)

OUTD = REPO / "docs/figures/comp2"; OUTD.mkdir(parents=True, exist_ok=True)
png = OUTD / "comp2_halide_lengths.png"
fig.savefig(png, dpi=300, bbox_inches="tight")
print("->", png)

# Origin CSV: raw bond lengths (padded) + summary
csvp = REPO / "db/properties/comp2_halide_lengths_origin.csv"
keys = ["comp1 Li-Cl", "comp2 Li-Cl", "comp2 Li-Br"]
nmax = max(len(dist[k]) for k in keys)
with open(csvp, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow([k.replace(" ", "_") + "_A" for k in keys])
    for i in range(nmax):
        w.writerow([f"{dist[k][i]:.4f}" if i < len(dist[k]) else "" for k in keys])
    w.writerow([])
    w.writerow(["# summary: " + "; ".join(
        f"{k} mean {dist[k].mean():.3f} std {dist[k].std():.3f} n {len(dist[k])}" for k in keys)])
print("->", csvp)
