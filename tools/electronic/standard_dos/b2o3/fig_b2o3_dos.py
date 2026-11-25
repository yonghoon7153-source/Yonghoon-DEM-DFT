#!/usr/bin/env python3
"""b2o3 (B2O3-doped LPSCl1.6, 128-atom champion) — standard-style DOS/PDOS figures.
Data: db/properties/b2o3_{dos,pdos_element,pdos_site}_smooth.csv (sigma 0.05 eV).
Gap 1.9671 eV = VBM/CBM eigenvalues 2.4717/4.4388 from fixed-occ nscf
(b2o3_nscf_gap.out, 25 irr k; confirmed from KISTI backup 2026-07-16).
Site mean-3p values are computed from the csv over the displayed valence
window (-8..0 eV) at plot time — the June 2026 full-range values for
PS4-S/Cl (-5.37/-5.25) were inflated by deep sigma-band weight below -8 eV.
Same figure family as lpsocl/fig_lpsocl_dos.py. Outputs 3 PNGs into cwd.
"""
import csv
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

INK, MUT = "#1f2937", "#6b7280"
# VBM/CBM: fixed-occ nscf eigenvalues, CONFIRMED 2026-07-16 from backup
# b2o3_eos/b2o3_nscf_gap.out ("highest occupied, lowest unoccupied: 2.4717 4.4388")
VBM, CBM = 2.4717, 4.4388
GAP = CBM - VBM  # 1.9671
COL = {"Li": "#0d9488", "P": "#7c3aed", "S": "#c05621", "Cl": "#65a30d",
       "B": "#0284c7", "O": "#be123c"}

from pathlib import Path
DB = str(Path(__file__).resolve().parents[4] / "db" / "properties") + "/"
E, D = [], []
with open(DB + "b2o3_dos_smooth.csv") as f:
    for r in csv.DictReader(f):
        E.append(float(r["E_minus_VBM"])); D.append(float(r["total_DOS"]))

# ── 1) total DOS ──
fig, ax = plt.subplots(figsize=(8.6, 5.4))
fig.subplots_adjust(left=0.09, right=0.97, top=0.92, bottom=0.12)
ax.fill_between(E, D, color="#e5e7eb", alpha=0.8)
ax.plot(E, D, color=INK, lw=1.8)
ax.axvspan(0, GAP, color="#fef9c3", zorder=0)
ax.axvline(0, color="#2563eb", ls="--", lw=1.4)
ax.axvline(GAP, color="#2563eb", ls="--", lw=1.4)
ax.text(GAP/2, 98, f"gap {GAP:.3f} eV", ha="center", fontsize=12, color="#92400e", fontweight="bold")
ax.text(GAP/2, 87, "(VBM/CBM eigenvalues,\nfixed-occ nscf)", ha="center", fontsize=8.5, color="#92400e")
ax.text(GAP/2, 9, "tails inside gap =\nGaussian smoothing\n($\\sigma$ = 0.05 eV) only", ha="center",
        fontsize=7.5, color=MUT, style="italic")
ax.set_xlim(-8, 7); ax.set_ylim(0, 138)
ax.set_xlabel("E $-$ E$_{VBM}$ (eV)", fontsize=12, color=INK)
ax.set_ylabel("DOS (states/eV)", fontsize=12, color=INK)
ax.set_title("B$_2$O$_3$-doped LPSCl$_{1.6}$ — total DOS (PBE, tetrahedra, V$_0$)", fontsize=12.5, color=INK)
for s in ("top", "right"): ax.spines[s].set_visible(False)
ax.tick_params(colors=MUT)
fig.savefig("b2o3_dos_total.png", dpi=300)
plt.close(fig)

# ── 2) element PDOS ──
cols = {el: [] for el in COL}
E2 = []
with open(DB + "b2o3_pdos_element_smooth.csv") as f:
    for r in csv.DictReader(f):
        E2.append(float(r["E_minus_VBM"]))
        for el in COL: cols[el].append(float(r[el]))
fig, ax = plt.subplots(figsize=(8.6, 5.4))
fig.subplots_adjust(left=0.09, right=0.97, top=0.92, bottom=0.12)
ax.axvspan(0, GAP, color="#fef9c3", zorder=0)
ax.axvline(0, color="#2563eb", ls="--", lw=1.2)
ax.axvline(GAP, color="#2563eb", ls="--", lw=1.2)
for el in ("Li", "P", "S", "Cl"):
    ax.plot(E2, cols[el], color=COL[el], lw=1.7)
ax.plot(E2, cols["O"], color=COL["O"], lw=2.6, zorder=5)
ax.plot(E2, cols["B"], color=COL["B"], lw=2.6, zorder=5)
lab = {"S": (-1.55, 88), "Cl": (-3.2, 84), "Li": (6.1, 52), "P": (-4.6, 19)}
for el, (x, y) in lab.items():
    ax.text(x, y, el, color=COL[el], fontsize=12, fontweight="bold", ha="center")
ax.annotate("O 2p buried deep below VBM\n(P–O band) — no O at band edges",
            xy=(-5.4, 7.2), xytext=(-7.8, 42), fontsize=9.5, color=COL["O"],
            arrowprops=dict(arrowstyle="-|>", color=COL["O"], lw=1.2))
ax.text(-7.85, 56, "B 2p sparse & buried\n(2 B atoms, BS$_3$ units)",
        fontsize=9.5, color=COL["B"], ha="left")
ax.text(-3.95, 5.0, "B", color=COL["B"], fontsize=11, fontweight="bold", ha="center")
ax.text(GAP/2, 74, f"gap {GAP:.3f} eV", ha="center", fontsize=10.5, color="#92400e", fontweight="bold")
ax.set_xlim(-8, 7); ax.set_ylim(0, 100)
ax.set_xlabel("E $-$ E$_{VBM}$ (eV)", fontsize=12, color=INK)
ax.set_ylabel("PDOS (states/eV)", fontsize=12, color=INK)
ax.set_title("B$_2$O$_3$-doped LPSCl$_{1.6}$ — element-resolved PDOS (PBE, V$_0$)", fontsize=12.5, color=INK)
ax.legend(handles=[plt.Line2D([], [], color=COL[e], lw=2.2, label=e) for e in ("Li","P","S","Cl","B","O")],
          loc="upper right", frameon=False, fontsize=10)
for s in ("top", "right"): ax.spines[s].set_visible(False)
ax.tick_params(colors=MUT)
fig.savefig("b2o3_pdos_elements.png", dpi=300)
plt.close(fig)

# ── 3) site-projected per-atom PDOS (free-S vs B-S vs PS4-S) ──
SITES = ["free_S", "B_S", "PS4_S", "Cl", "O"]
SCOL = {"free_S": "#c05621", "B_S": "#0284c7", "PS4_S": "#7c3aed", "Cl": "#65a30d", "O": "#be123c"}
SLS = {"B_S": "-", "PS4_S": "-", "Cl": "--", "O": ":"}
CNT = {"free_S": 6, "B_S": 6, "PS4_S": 29, "Cl": 16, "O": 3}
LBL = {"free_S": "free S$^{2-}$", "B_S": "B–S (BS$_3$)", "PS4_S": "PS$_4$–S", "Cl": "Cl", "O": "O (on P)"}
sc = {s: [] for s in SITES}
E3 = []
with open(DB + "b2o3_pdos_site_smooth.csv") as f:
    for r in csv.DictReader(f):
        E3.append(float(r["E_minus_VBM"]))
        for s in SITES: sc[s].append(float(r[s]))
# mean 3p per site computed FROM the plotted data (occupied part of the csv
# window, E<=0) so legend numbers always match what is displayed
MEAN3P = {}
for s in SITES:
    num = den = 0.0
    for e, y in zip(E3, sc[s]):
        if e <= 0.0 and y > 0: num += e * y; den += y
    MEAN3P[s] = num / den
fig, ax = plt.subplots(figsize=(8.6, 5.4))
fig.subplots_adjust(left=0.09, right=0.97, top=0.92, bottom=0.12)
ax.axvspan(0, GAP, color="#fef9c3", zorder=0)
ax.axvline(0, color="#2563eb", ls="--", lw=1.2)
ax.axvline(GAP, color="#2563eb", ls="--", lw=1.2)
ax.fill_between(E3, sc["free_S"], color=SCOL["free_S"], alpha=0.35, zorder=4)
ax.plot(E3, sc["free_S"], color=SCOL["free_S"], lw=2.4, zorder=5)
for s in ("B_S", "PS4_S", "Cl", "O"):
    ax.plot(E3, sc[s], color=SCOL[s], ls=SLS[s], lw=1.9)
for s in SITES:
    ax.axvline(MEAN3P[s], color=SCOL[s], ls=":", lw=1.0, alpha=0.55)
ax.annotate("free S$^{2-}$ shallowest\n($\\langle$3p$\\rangle$ $%.2f$ eV)\n$\\rightarrow$ most oxidation-prone" % MEAN3P["free_S"],
            xy=(-0.62, 4.70), xytext=(0.35, 4.55), fontsize=9.5, color=SCOL["free_S"],
            arrowprops=dict(arrowstyle="-|>", color=SCOL["free_S"], lw=1.2))
ax.text(-6.95, 3.45, "$\\langle$3p$\\rangle$ = PDOS-weighted mean,\n$-$8..0 eV (displayed valence window)",
        fontsize=7.5, color=MUT, style="italic")
ax.legend(handles=[plt.Line2D([], [], color=SCOL[s], ls=SLS.get(s, "-"), lw=2.2,
                              label=f"{LBL[s]} $\\times${CNT[s]}  ($\\langle$3p$\\rangle$ ${MEAN3P[s]:+.2f}$)")
                   for s in SITES],
          loc="upper left", frameon=False, fontsize=8.6)
ax.set_xlim(-7, 4); ax.set_ylim(0, 6.0)
ax.set_xlabel("E $-$ E$_{VBM}$ (eV)", fontsize=12, color=INK)
ax.set_ylabel("per-atom PDOS (states/eV)", fontsize=12, color=INK)
ax.set_title("B$_2$O$_3$-doped LPSCl$_{1.6}$ — site-projected anion PDOS (per atom, V$_0$)",
             fontsize=12.5, color=INK)
for s in ("top", "right"): ax.spines[s].set_visible(False)
ax.tick_params(colors=MUT)
fig.savefig("b2o3_pdos_sites.png", dpi=300)
print("saved 3 figures")
