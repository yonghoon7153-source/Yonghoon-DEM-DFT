#!/usr/bin/env python3
"""ICOHP comparison: comp1 (LPSCl) vs modelc (LPSCl1.6) [vs nd when available].

Source of truth: db/properties/bonds.json -> icohp_LOBSTER_ext_basis_eV_per_bond
(LOBSTER 5.1.1, PAW kjpaw_psl 1.0.0, ecutwfc 70 Ry, extended basis, spilling <1.5%).
comp1 k=4x4x4, modelc k=6x6x3 (ICOHP is k-robust, <0.006 eV shift).

Produces:
  docs/figures/icohp/icohp_compare.csv   (long format, all bond types + site splits)
  docs/figures/icohp/icohp_compare.png   (2-panel: avg per bond type | per-site splits)

ICOHP convention: more negative = stronger bond. We plot -ICOHP (magnitude),
so taller bar = stronger.  nd_pair01 (Nd2O3-doped) ICOHP to be appended after
the V100 LOBSTER run (P-O / Nd-O / P-S / Li-Cl / Li-S).
"""
import csv
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = Path("docs/figures/icohp")
OUT.mkdir(parents=True, exist_ok=True)

# --- ICOHP averages per bond type (eV/bond), from bonds.json ---
# (icohp_eV, n_bonds)
MAIN = {
    "P-S":   {"comp1": (-5.944, 16),  "modelc": (-6.000, 20)},
    "Li-Cl": {"comp1": (-1.855, 24),  "modelc": (-2.103, 42)},
    "Li-S":  {"comp1": (-1.592, 120), "modelc": (-1.717, 113)},
    "S-S":   {"comp1": (-0.107, 56),  "modelc": (-0.110, 58)},
}
# nd to be filled from V100 LOBSTER: P-S, P-O, Nd-O, Li-Cl, Li-S, S-S
ND = {}  # e.g. {"P-S": (-x, n), "P-O": (...), "Nd-O": (...), ...}

# --- per-site splits (the anti-site / free-S anchors) ---
SPLIT = {
    "Li-Cl(4a)":      {"comp1": (-1.855, 24), "modelc": (-2.026, 38)},
    "Li-Cl(4d,anti)": {"comp1": (None,  0),   "modelc": (-2.836, 4)},
    "Li-S(PS4)":      {"comp1": (-1.348, 96), "modelc": (-1.622, 101)},
    "Li-S(4d,freeS)": {"comp1": (-2.566, 24), "modelc": (-2.516, 12)},
}

SYS_COL = {"comp1": "#3F7BB6", "modelc": "#C44536", "nd": "#2CA089"}
SYS_LAB = {"comp1": "comp1 (LPSCl)", "modelc": "modelc (LPSCl$_{1.6}$)",
           "nd": "Nd$_2$O$_3$-doped"}

# ---------- CSV ----------
rows = []
for grp, d in {**MAIN, **SPLIT}.items():
    kind = "avg_bond_type" if grp in MAIN else "site_split"
    for sysname in ("comp1", "modelc", "nd"):
        src = ND if sysname == "nd" else d
        if sysname not in src:
            continue
        icohp, n = src[sysname]
        if icohp is None:
            continue
        rows.append({"bond": grp, "kind": kind, "system": sysname,
                     "ICOHP_eV": icohp, "n_bonds": n})
with open(OUT / "icohp_compare.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["bond", "kind", "system", "ICOHP_eV", "n_bonds"])
    w.writeheader()
    w.writerows(rows)

# also a wide summary with %delta (comp1->modelc)
with open(OUT / "icohp_summary_wide.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["bond", "comp1_ICOHP_eV", "comp1_n", "modelc_ICOHP_eV", "modelc_n",
                "delta_pct_comp1_to_modelc", "nd_ICOHP_eV"])
    for grp, d in {**MAIN, **SPLIT}.items():
        c = d.get("comp1", (None, 0)); m = d.get("modelc", (None, 0))
        nd = ND.get(grp, (None, 0))
        dpct = ""
        if c[0] and m[0]:
            dpct = f"{100*(m[0]-c[0])/abs(c[0]):+.1f}"
        w.writerow([grp, c[0], c[1], m[0], m[1], dpct, nd[0]])

# ---------- plot ----------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.2),
                               gridspec_kw={"width_ratios": [1, 1]})

def grouped_bars(ax, groups, data_dict, systems, title):
    x = np.arange(len(groups))
    w = 0.8 / len(systems)
    for i, sysname in enumerate(systems):
        vals, ns = [], []
        for g in groups:
            src = ND if sysname == "nd" else data_dict[g]
            v = src.get(sysname, (None, 0)) if sysname == "nd" else data_dict[g].get(sysname, (None, 0))
            vals.append(-v[0] if v[0] is not None else 0.0)  # -ICOHP magnitude
            ns.append(v[1])
        bars = ax.bar(x + (i - (len(systems)-1)/2) * w, vals, w,
                      label=SYS_LAB[sysname], color=SYS_COL[sysname], alpha=0.9,
                      edgecolor="white", lw=0.6)
        for b, v, n in zip(bars, vals, ns):
            if v > 0:
                ax.text(b.get_x() + b.get_width()/2, v + 0.08, f"{v:.2f}",
                        ha="center", va="bottom", fontsize=7.5)
    ax.set_xticks(x); ax.set_xticklabels(groups, fontsize=9)
    ax.set_ylabel(r"$-$ICOHP (eV/bond)   [stronger $\rightarrow$]", fontsize=10)
    ax.set_title(title, fontsize=11)
    ax.legend(fontsize=8.5, framealpha=0.95)
    ax.grid(axis="y", alpha=0.25)

grouped_bars(ax1, list(MAIN), MAIN, ["comp1", "modelc"],
             "Average ICOHP per bond type")
# delta annotations on panel 1
for j, g in enumerate(MAIN):
    c, m = MAIN[g]["comp1"][0], MAIN[g]["modelc"][0]
    dp = 100*(m-c)/abs(c)
    ax1.text(j, max(-c, -m) + 0.55, f"{dp:+.1f}%", ha="center",
             fontsize=8, color="#444", fontweight="bold")
ax1.set_ylim(0, 7.2)

grouped_bars(ax2, list(SPLIT), SPLIT, ["comp1", "modelc"],
             "Per-site splits (4a / 4d anti-site / free-S$^{2-}$)")
ax2.set_ylim(0, 3.4)

fig.suptitle("Argyrodite ICOHP (LOBSTER ext-basis) — bond strength comparison "
             "(nd: V100 LOBSTER pending)", fontsize=12, y=1.02)
plt.tight_layout()
plt.savefig(OUT / "icohp_compare.png", dpi=200, facecolor="white", bbox_inches="tight")
print("-> docs/figures/icohp/icohp_compare.png")
print("-> docs/figures/icohp/icohp_compare.csv")
print("-> docs/figures/icohp/icohp_summary_wide.csv")
