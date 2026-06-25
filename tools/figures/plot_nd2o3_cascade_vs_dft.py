#!/usr/bin/env python3
"""plot_nd2o3_cascade_vs_dft.py — honest consistency check: the v23 UMA cascade
Nd2O3 champion (LPSCl canonical, Nd2O3 unit, x=0.25, 50-atom, 3 replicates) vs our
DEDICATED Nd-doping track (modelc Li5.4 base, Nd->Li x=0.20 + O0.3, 120-atom,
DFT-relaxed geometry; UMA-omat EOS + MP grand-potential ESW).

NOT the same setup (base / x / cell / mechanism differ) -> this is a consistency
check, not an identical-cell reproduction. What we CAN compare:
  * EOS bulk modulus B0  (both UMA)            -> agree ~19-20 GPa
  * grand-potential ESW  (both MP GGA_GGA+U)   -> identical 1.92/1.52/0.40 (Nd+O chemistry)
  * absolute Young's E   (cascade UMA only)     -> UMA runs ~2x stiff vs exp/DFT (directional only)
DFT EOS (KISTI 3_dft_eos_v7) still PENDING -> the B0 match is UMA-vs-UMA, not yet UMA-vs-DFT.
Sources: db/properties/cascade_v23_champions.csv ; db/properties/{eos,oxidation_stability,elastic}.json
"""
import csv, os
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
OUT = "docs/figures/cascade"; os.makedirs(OUT, exist_ok=True)

# ---- cascade Nd2O3 (3 replicates, UMA-s-1p1, x=0.25) ----
B0c, Ec, Bhc, Ghc, nuc = [], [], [], [], []
for r in csv.DictReader(open("db/properties/cascade_v23_champions.csv")):
    if r["dopant"].split("+")[0] == "Nd2O3":
        B0c.append(float(r["eos_B0_GPa"])); Ec.append(float(r["elastic_E_young_GPa"]))
        Bhc.append(float(r["elastic_B_hill_GPa"])); Ghc.append(float(r["elastic_G_hill_GPa"]))
        nuc.append(float(r["elastic_poisson_nu"]))
B0c, Ec, Bhc, Ghc, nuc = map(np.array, (B0c, Ec, Bhc, Ghc, nuc))

# ---- dedicated DFT-track values (from db/properties/*.json) ----
DED = dict(
    eos_B0_uma=18.9, eos_B0_uma_std=1.4,      # modelc_nd_doped_mlip, 72 physical members
    eos_B0_undoped_dft=21.7,                   # modelc DFT EOS (v1)
    esw_ox=1.92, esw_red=1.52, esw_win=0.40,   # nd_doped grand-potential
    E_exp_undoped=20.3, E_exp_nd=20.7,         # experiment pellet E (FINAL capstone)
    E_dft_relaxed_lo=22.06, E_dft_relaxed_hi=27.66,  # comp1/modelc DFT relaxed-ion E_VRH (undoped)
)
# cascade ESW for Nd2O3 (from oxidation_stability_cascade.csv)
ESWc = dict(ox=1.92, red=1.518, win=0.402)

fig, axs = plt.subplots(1, 3, figsize=(17, 6.2))

# ===== (A) EOS bulk modulus B0 — the closest apples-to-apples =====
ax = axs[0]
ax.scatter(np.full(len(B0c), 0) + np.linspace(-.08, .08, len(B0c)), B0c, c="#5c6bc0",
           s=70, edgecolor="white", zorder=4, label="cascade replicates (x=0.25)")
ax.errorbar(0, B0c.mean(), yerr=B0c.std(), fmt="o", color="#1a237e", ms=11, capsize=6,
            elinewidth=2, zorder=5, label=f"cascade mean {B0c.mean():.1f}±{B0c.std():.1f}")
ax.errorbar(1, DED["eos_B0_uma"], yerr=DED["eos_B0_uma_std"], fmt="s", color="#00897b", ms=12,
            capsize=6, elinewidth=2, zorder=5, label=f"dedicated UMA {DED['eos_B0_uma']}±{DED['eos_B0_uma_std']}")
ax.axhline(DED["eos_B0_undoped_dft"], ls="--", color="0.45", lw=1.4)
ax.text(1.45, DED["eos_B0_undoped_dft"] + .15, f"undoped modelc DFT-EOS {DED['eos_B0_undoped_dft']}",
        fontsize=8, color="0.35", ha="center")
ax.set_xticks([0, 1]); ax.set_xticklabels(["UMA cascade\n(LPSCl, x0.25)", "dedicated\n(modelc, x0.20)"])
ax.set_ylabel("EOS bulk modulus B0 (GPa)"); ax.set_xlim(-.5, 2.0); ax.set_ylim(12, 28)
ax.set_title("(A) Bulk modulus B0 — STRONG agreement\n19.9 vs 18.9 GPa (both UMA; DFT-EOS pending)", fontsize=10)
ax.legend(fontsize=7.5, loc="lower right"); ax.grid(axis="y", alpha=.3)

# ===== (B) grand-potential ESW window — identical =====
ax = axs[1]
ax.barh(1, ESWc["ox"] - ESWc["red"], left=ESWc["red"], color="#5c6bc0", edgecolor="k", height=.5, zorder=3)
ax.barh(0, DED["esw_ox"] - DED["esw_red"], left=DED["esw_red"], color="#00897b", edgecolor="k", height=.5, zorder=3)
for yv, ox, red in [(1, ESWc["ox"], ESWc["red"]), (0, DED["esw_ox"], DED["esw_red"])]:
    ax.text(red - .02, yv, f"{red:.2f}", va="center", ha="right", fontsize=8)
    ax.text(ox + .02, yv, f"{ox:.2f}", va="center", ha="left", fontsize=8)
ax.set_yticks([0, 1]); ax.set_yticklabels(["dedicated DFT-comp\n(grand-potential)", "UMA cascade\n(grand-potential)"])
ax.set_xlabel("V vs Li/Li$^+$  (bar = stable window red→ox)"); ax.set_xlim(1.3, 2.1)
ax.set_title("(B) ESW window — IDENTICAL\nox 1.92 / red 1.52 / width 0.40 (Nd+O → Li₃PO₄+Nd-sulfide chemistry)", fontsize=10)
ax.grid(axis="x", alpha=.3)

# ===== (C) absolute Young's E — UMA runs stiff (honest caveat) =====
ax = axs[2]
ax.scatter(np.full(len(Ec), 0) + np.linspace(-.08, .08, len(Ec)), Ec, c="#5c6bc0", s=70,
           edgecolor="white", zorder=4)
ax.errorbar(0, Ec.mean(), yerr=Ec.std(), fmt="o", color="#1a237e", ms=11, capsize=6, elinewidth=2, zorder=5)
ax.axhspan(DED["E_dft_relaxed_lo"], DED["E_dft_relaxed_hi"], xmin=.30, xmax=.62, color="#ffb74d", alpha=.5, zorder=1)
ax.text(1, (DED["E_dft_relaxed_lo"]+DED["E_dft_relaxed_hi"])/2, "DFT relaxed-ion\n(undoped) 22–28", fontsize=8, ha="center", va="center")
ax.scatter([2, 2], [DED["E_exp_undoped"], DED["E_exp_nd"]], c="#c62828", s=80, marker="D", zorder=4)
ax.text(2, DED["E_exp_nd"] + 1.5, "experiment\n20.3→20.7\n(Nd: ~unchanged)", fontsize=8, ha="center", color="#c62828")
ax.set_xticks([0, 1, 2]); ax.set_xticklabels(["UMA cascade\nE_young", "DFT\nrelaxed-ion", "experiment\n(pellet)"])
ax.set_ylabel("Young's modulus E (GPa)"); ax.set_xlim(-.5, 2.6); ax.set_ylim(15, 55)
ax.text(0, Ec.mean() + 2.5, f"{Ec.mean():.0f}±{Ec.std():.0f}\n(UMA ~2× stiff)", fontsize=8.5, ha="center", color="#1a237e", fontweight="bold")
ax.set_title("(C) Absolute E_young — DIRECTIONAL ONLY\nUMA cascade runs ~2× stiff vs exp/DFT (documented)", fontsize=10)
ax.grid(axis="y", alpha=.3)

plt.suptitle("Nd₂O₃ doping — UMA v23 cascade  vs  dedicated DFT-track  (consistency check; NOT identical cell/x/base)",
             fontsize=13, y=1.02)
plt.tight_layout()
plt.savefig(f"{OUT}/nd2o3_cascade_vs_dft.png", dpi=150, bbox_inches="tight")
plt.savefig(f"{OUT}/nd2o3_cascade_vs_dft.pdf", bbox_inches="tight")
print(f"saved {OUT}/nd2o3_cascade_vs_dft.png")
print(f"\ncascade Nd2O3 (n={len(B0c)}): B0={B0c.mean():.1f}±{B0c.std():.1f}  E={Ec.mean():.1f}±{Ec.std():.1f}  "
      f"B_hill={Bhc.mean():.1f}±{Bhc.std():.1f}  G_hill={Ghc.mean():.1f}±{Ghc.std():.1f}  nu={nuc.mean():.3f}±{nuc.std():.3f}")
print(f"dedicated: EOS-B0(UMA)={DED['eos_B0_uma']}±{DED['eos_B0_uma_std']}  ESW ox/red/win={DED['esw_ox']}/{DED['esw_red']}/{DED['esw_win']}  "
      f"exp-E {DED['E_exp_undoped']}->{DED['E_exp_nd']}")
print(f"cascade ESW: ox/red/win = {ESWc['ox']}/{ESWc['red']}/{ESWc['win']}")
