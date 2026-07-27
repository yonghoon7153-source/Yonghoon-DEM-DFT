#!/usr/bin/env python3
"""fig_comp2_conductivity.py — panel-(e) style: sigma(300K) + Ea per system.

comp1 (LPSCl) / comp2 (LPSCl0.5Br0.5) / modelc (LPSCl1.6, vacancy).
Left axis  = Nernst-Einstein sigma(300K) [mS/cm] (Haven=1), INTERNAL-only absolute.
Right axis = Arrhenius Ea [eV] (2-50 ps, 600/800/1000 K).

HONEST framing: the Li VACANCY (modelc) is the robust conductivity lever (~4x,
survives all noise). Br isovalent Cl->Br (comp2, Li6 no-vacancy) shows no clear
boost and its 300 K sigma is UNDETERMINED (Ea 0.275+/-0.033 from 800 K seed
scatter -> sigma300 spans 0.39-4.98 mS/cm). comp2 carries that error bar.
comp1/modelc = deck SINGLE-SEED anchors (slide 5), one trajectory per T with no
seed error bar -- so comp2 (3-seed) vs comp1/modelc is a MIXED-protocol pair.
Method validated: comp1 sigma300 3.4 & modelc 14 mS/cm == deck.

Outputs docs/figures/comp2/comp2_conductivity.png
      + db/properties/comp2_conductivity_origin.csv
"""
import csv
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))
from tools.figures.house_style import INK, MUT, SYS, apply_axes  # noqa: E402

kB = 8.617333e-5
e = 1.602176634e-19
kB_J = 1.380649e-23
Ts = np.array([600., 800., 1000.]); xT = 1.0 / Ts
C2COL = "#c2410c"; SIGCOL = "#0f766e"; EACOL = "#b45309"

NLI = {"comp1": 24 / (1016.62e-24), "comp2": 24 / (1037.55e-24), "modelc": 27 / (1216.44e-24)}

# D per T (cm2/s): comp1/modelc = deck SINGLE-SEED (slide 5 = DB/littable),
# comp2 = gabia 3-seed mean. Reproduces deck: comp1 sig300 3.4, modelc 14 mS/cm.
D = {"comp1": np.array([3.09e-6, 1.03e-5, 2.20e-5]),    # LPSCl, Ea 0.253
     "modelc": np.array([7.90e-6, 2.05e-5, 4.55e-5]),   # LPSCl1.6, Ea 0.224
     "comp2": np.array([2.2681e-06, 7.6248e-06, 2.0316e-05])}
SEEDS2 = np.array([[1.8231e-06, 6.2380e-06, 2.1425e-05],
                   [2.4388e-06, 2.1464e-06, 1.8506e-05],
                   [2.5425e-06, 1.4490e-05, 2.1017e-05]])


def sig300(n, Darr):
    s, b = np.polyfit(xT, np.log(Darr), 1)
    Ea = -s * kB
    D300 = np.exp(b) * np.exp(-Ea / (kB * 300.0))
    return n * e * e * D300 / (kB_J * 300.0) * 1e3, Ea   # mS/cm, eV


order = ["comp1", "comp2", "modelc"]
labels = {"comp1": "comp1\nLPSCl\n(Li6)", "comp2": "comp2\nLPSCl$_{0.5}$Br$_{0.5}$\n(Li6)",
          "modelc": "modelC\nLPSCl1.6\n(vacancy)"}
sig = {}; ea = {}
for s in order:
    sig[s], ea[s] = sig300(NLI[s], D[s])
# comp2 uncertainty from 3-seed Ea spread -> sigma range
ea2_seeds = np.array([-np.polyfit(xT, np.log(SEEDS2[i]), 1)[0] * kB for i in range(3)])
ea2_err = ea2_seeds.std()
_, ea2c = sig300(NLI["comp2"], D["comp2"])
D0_2 = sig["comp2"] / (NLI["comp2"] * e * e / (kB_J * 300.0) * 1e3) * np.exp(ea2c / (kB * 300.0))
sig2_lo = NLI["comp2"] * e * e / (kB_J * 300.0) * D0_2 * np.exp(-(ea2c + ea2_err) / (kB * 300.0)) * 1e3
sig2_hi = NLI["comp2"] * e * e / (kB_J * 300.0) * D0_2 * np.exp(-(ea2c - ea2_err) / (kB * 300.0)) * 1e3

x = np.arange(len(order))
fig, axL = plt.subplots(figsize=(6.8, 5.0), constrained_layout=True)
axR = axL.twinx()

# sigma bars (left)
bars = axL.bar(x - 0.18, [sig[s] for s in order], width=0.34, color=SIGCOL, alpha=0.8,
               label="$\\sigma$(300K) NE", zorder=3)
# comp2 sigma error bar (asymmetric)
axL.errorbar(x[1] - 0.18, sig["comp2"], yerr=[[sig["comp2"] - sig2_lo], [sig2_hi - sig["comp2"]]],
             fmt="none", ecolor=INK, elinewidth=1.6, capsize=5, zorder=5)
for xi, s in zip(x, order):
    axL.text(xi - 0.18, sig[s] + 0.35, f"{sig[s]:.1f}", ha="center", va="bottom",
             fontsize=9.5, color=SIGCOL, fontweight="bold")

# Ea markers (right)
axR.plot(x + 0.18, [ea[s] for s in order], "s-", color=EACOL, ms=11, lw=1.6, zorder=4,
         label="E$_a$")
axR.errorbar(x[1] + 0.18, ea["comp2"], yerr=ea2_err, fmt="none", ecolor=EACOL,
             elinewidth=1.6, capsize=5, zorder=5)
for xi, s in zip(x, order):
    off = ea2_err + 0.006 if s == "comp2" else 0.006
    axR.text(xi + 0.18, ea[s] + off, f"{ea[s]:.3f}", ha="center", va="bottom",
             fontsize=9, color=EACOL, fontweight="bold")

axL.set_xticks(x); axL.set_xticklabels([labels[s] for s in order], fontsize=9.5, color=INK)
axL.set_ylabel("$\\sigma$(300 K)  (mS/cm)  —  NE, INTERNAL", fontsize=11, color=SIGCOL)
axR.set_ylabel("Activation energy  E$_a$  (eV)", fontsize=11, color=EACOL)
axL.tick_params(axis="y", colors=SIGCOL); axR.tick_params(axis="y", colors=EACOL)
for sp in ("top",):
    axL.spines[sp].set_visible(False); axR.spines[sp].set_visible(False)
axL.set_ylim(0, max(sig.values()) * 1.25)
axR.set_ylim(0.20, 0.34)
axL.set_title("Conductivity lever: vacancy (modelC), not isovalent Br", fontsize=12, color=INK)
axL.legend(loc="upper left", fontsize=9, frameon=False)
axR.legend(loc="upper center", fontsize=9, frameon=False)
fig.text(0.5, -0.06,
         "NE Haven=1, 2-50 ps, 600/800/1000 K.  comp1/modelC = deck single-seed anchors.  modelC vacancy "
         "$\\sigma$300 ~4x comp1 (robust lever).\ncomp2 (isovalent Cl->Br, 3-seed) central 0.41x comp1 but "
         "error bar spans 0.12-1.5x = INCONCLUSIVE (comp2 800 K seed scatter).  absolute $\\sigma$ INTERNAL "
         "(validated: comp1 3.4 & modelC 14 == deck).  Experimental Br gain needs anion-disorder sampling.",
         ha="center", fontsize=7.1, color=MUT)

OUTD = REPO / "docs/figures/comp2"; OUTD.mkdir(parents=True, exist_ok=True)
png = OUTD / "comp2_conductivity.png"
fig.savefig(png, dpi=300, bbox_inches="tight")
print("->", png)

csvp = REPO / "db/properties/comp2_conductivity_origin.csv"
with open(csvp, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["system", "sigma300K_mS_cm_NE_INTERNAL", "sigma_err_lo", "sigma_err_hi",
                "Ea_eV", "Ea_err_eV", "n_Li_cm3", "note"])
    for s in order:
        lo = f"{sig2_lo:.3f}" if s == "comp2" else ""
        hi = f"{sig2_hi:.3f}" if s == "comp2" else ""
        eerr = f"{ea2_err:.3f}" if s == "comp2" else ""
        note = "3-seed" if s == "comp2" else "single-seed"
        w.writerow([s, f"{sig[s]:.3f}", lo, hi, f"{ea[s]:.3f}", eerr, f"{NLI[s]:.3e}", note])
print("->", csvp)
print(f"sigma300 (mS/cm): comp1 {sig['comp1']:.2f} | comp2 {sig['comp2']:.2f} "
      f"[{sig2_lo:.2f}-{sig2_hi:.2f}] | modelc {sig['modelc']:.2f}")
