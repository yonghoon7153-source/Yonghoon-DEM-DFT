#!/usr/bin/env python3
"""plot_icohp_bars.py — ICOHP bar chart + CSV for Nd2O3-doped LPSCl1.6.
Values = 4.0 A cutoff (PAW kjpaw_psl 1.0.0, LOBSTER 5.1.1), the comparison-valid
set from db/properties/nd_icohp.json (comparison_vs_modelc_comp1_PAW_4.0A +
bonds_4.0A_cutoff_for_comparison). Story: host backbone unchanged by Nd2O3
(±4%), the only new strong bond is P-O (O actor), Nd-X are weak ionic (spectator).
Writes: docs/figures/icohp/icohp_nd_summary.csv + icohp_nd_bars.png/.pdf
"""
import csv, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# host bonds: (label, comp1, modelc, nd, pct, d_A, N_nd, character)
HOST = [
    ("P–S",  -5.944, -6.00,  -5.976, "+0.4%", 2.064, 37,  "covalent backbone"),
    ("Li–S", -1.592, -1.717, -1.647, "+4.1%", 2.52,  199, "ionic"),
    ("Li–Cl",-1.855, -2.103, -2.132, "−1.4%", 2.52,  79,  "ionic"),
    ("S–S",  -0.107, -0.110, -0.101, "~0",    None,  117, "non-bonding"),
]
# nd-only bonds: (label, nd, d_A, N, character, group)
NDONLY = [
    ("P–O",  -8.43,  1.571, 3, "strong polar covalent", "O effect"),
    ("Nd–O", -0.42,  2.545, 2, "weak ionic",            "Nd ionic"),
    ("Nd–S", -0.436, 2.898, 8, "weak ionic",            "Nd ionic"),
    ("Nd–Cl",-0.571, 2.772, 2, "weak ionic",            "Nd ionic"),
]

HERE = os.path.dirname(__file__) or "."
OUT = os.path.join(HERE, "../../docs/figures/icohp")
os.makedirs(os.path.abspath(OUT), exist_ok=True)

# ---- CSV ----
csv_path = os.path.join(OUT, "icohp_nd_summary.csv")
with open(csv_path, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["# ICOHP (eV/bond, total=spin1+spin2), 4.0 A cutoff PAW kjpaw LOBSTER5.1.1; from nd_icohp.json"])
    w.writerow(["bond", "comp1_eV", "modelc_eV", "nd_eV", "nd_vs_modelc_pct",
                "d_A", "N_nd", "character", "role"])
    for lab, c1, mc, nd, pct, d, N, ch in HOST:
        w.writerow([lab, c1, mc, nd, pct, d if d else "", N, ch, "host (unchanged)"])
    for lab, nd, d, N, ch, grp in NDONLY:
        w.writerow([lab, "", "", nd, "nd-only", d, N, ch, grp])
print("saved:", os.path.abspath(csv_path))

# ---- figure ----
fig, ax = plt.subplots(figsize=(9.4, 5.4))
W = 0.26
xh = list(range(len(HOST)))
c_comp1, c_modelc, c_nd = "#b9b9b9", "#4a7fb5", "#c0392b"
for i, (lab, c1, mc, nd, pct, d, N, ch) in enumerate(HOST):
    ax.bar(i - W, abs(c1), W, color=c_comp1, edgecolor="k", lw=0.5, zorder=3,
           label="comp1 (LPSCl)" if i == 0 else None)
    ax.bar(i,      abs(mc), W, color=c_modelc, edgecolor="k", lw=0.5, zorder=3,
           label="modelc (LPSCl1.6)" if i == 0 else None)
    ax.bar(i + W, abs(nd), W, color=c_nd, edgecolor="k", lw=0.5, zorder=3,
           label="nd (Nd₂O₃-doped)" if i == 0 else None)
    ax.text(i + W, abs(nd) + 0.12, pct, ha="center", va="bottom", fontsize=8,
            color="#2e6b2e", fontweight="bold")

# gap then nd-only single bars
x0 = len(HOST) + 0.6
xn = []
for j, (lab, nd, d, N, ch, grp) in enumerate(NDONLY):
    x = x0 + j
    xn.append(x)
    col = "#e0a13a" if grp == "O effect" else "#7d5ba6"
    ax.bar(x, abs(nd), W * 2.2, color=col, edgecolor="k", lw=0.6, zorder=3)
    ax.text(x, abs(nd) + 0.12, f"{abs(nd):.2f}", ha="center", va="bottom", fontsize=8.5,
            fontweight="bold")

ax.annotate("O effect\nP–O +41% vs P–S", xy=(x0 - 0.32, 8.43), xytext=(3.35, 7.1),
            ha="center", va="center", fontsize=8.2, color="#9a6a14", fontweight="bold",
            arrowprops=dict(arrowstyle="->", color="#9a6a14"))
ax.annotate("Nd–X weak ionic\n(spectator)", xy=(x0 + 2, 0.6), xytext=(x0 + 1.5, 2.6),
            fontsize=8.5, color="#5a3f7a", ha="center",
            arrowprops=dict(arrowstyle="->", color="#5a3f7a"))

ax.set_xticks(xh + xn)
ax.set_xticklabels([h[0] for h in HOST] + [n[0] for n in NDONLY], fontsize=10)
ax.axvline(len(HOST) - 0.2, ls=":", color="0.6", lw=1)
ax.text(1.5, 7.15, "host backbone — ±4% (Nd₂O₃ leaves it intact)",
        ha="center", va="center", fontsize=9, color="0.35")
ax.set_ylabel("|ICOHP|  (eV / bond)", fontsize=11)
ax.set_ylim(0, 9.6)
ax.set_title("ICOHP bond strengths — Nd₂O₃-doped LPSCl1.6 (4.0 Å, LOBSTER)\n"
             "host unchanged · O actor (P–O −8.43) · Nd ionic spectator",
             fontsize=10.5, fontweight="bold")
ax.legend(loc="upper left", fontsize=8.5, ncol=1, framealpha=0.95)
for sp in ("top", "right"): ax.spines[sp].set_visible(False)

fig.tight_layout()
fig.savefig(os.path.join(OUT, "icohp_nd_bars.png"), dpi=300, bbox_inches="tight")
fig.savefig(os.path.join(OUT, "icohp_nd_bars.pdf"), bbox_inches="tight")
print("saved:", os.path.abspath(os.path.join(OUT, "icohp_nd_bars.png")))
