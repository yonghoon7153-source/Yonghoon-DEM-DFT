#!/usr/bin/env python3
"""plot_arrhenius.py — Li+ diffusion Arrhenius (AIMD-MLIP): LPSCl vs LPSCl1.6.
Data = db/properties/li_transport.json (UMA-s-1p1 omat MD, 600/800/1000 K) /
docs/figures/slide09_arrhenius/arrhenius_fit_origin.csv. ln D = ln D0 - Ea/(kB T).
Writes figure (ln D vs 1000/T, points + fit, Ea labels) + a clean CSV.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

KB = 8.617333e-5  # eV/K
T = np.array([600.0, 800.0, 1000.0])
x = 1000.0 / T
# ln D (cm^2/s) measured points (arrhenius_fit_origin.csv; comp1 = 4fu natural)
SYS = {
    "LPSCl (comp1)":      dict(lnD=np.array([-12.6873, -11.4834, -10.7245]),
                               Ea=0.253, lnD0=-7.7951, c="#3a6ea5", m="o"),
    "LPSCl1.6 (modelc)":  dict(lnD=np.array([-11.7486, -10.7951,  -9.9978]),
                               Ea=0.224, lnD0=-7.4634, c="#c0392b", m="s"),
}

fig, ax = plt.subplots(figsize=(7.6, 5.6))
xf = np.linspace(0.95, 1.72, 100)
for lab, s in SYS.items():
    ax.plot(x, s["lnD"], s["m"], color=s["c"], ms=9, mec="white", mew=0.8, zorder=4,
            label=f"{lab}: E$_a$={s['Ea']:.3f} eV")
    ax.plot(xf, s["lnD0"] - s["Ea"] / (1000 * KB) * xf, "--", color=s["c"], lw=1.6, zorder=3)

# D(600K) annotation
for lab, s in SYS.items():
    D600 = np.exp(s["lnD"][0])
    ax.annotate(f"D(600K)={D600:.2e}", xy=(x[0], s["lnD"][0]),
                xytext=(x[0] - 0.02, s["lnD"][0] + (0.45 if "1.6" in lab else -0.55)),
                fontsize=8, color=s["c"], ha="right" if "1.6" in lab else "left")

ax.annotate("", xy=(1.55, -11.6), xytext=(1.55, -12.5),
            arrowprops=dict(arrowstyle="->", color="#2e6b2e", lw=1.8))
ax.text(1.585, -12.05, "Cl-rich:\nlower E$_a$\nhigher D", color="#2e6b2e",
        fontsize=8.5, fontweight="bold", va="center")

ax.set_xlabel(r"1000 / T  (K$^{-1}$)", fontsize=12)
ax.set_ylabel(r"ln $D_{Li}$  (cm$^2$/s)", fontsize=12)
ax.set_xlim(0.95, 1.74)
ax.set_title("Li$^+$ diffusion Arrhenius (AIMD–MLIP) — LPSCl vs LPSCl1.6",
             fontsize=11.5, fontweight="bold")
ax.legend(loc="upper right", fontsize=10, framealpha=0.95)
ax.grid(alpha=0.25)
# top T axis
axT = ax.twiny(); axT.set_xlim(ax.get_xlim())
ticks = [1000/t for t in (1000, 800, 700, 600)]
axT.set_xticks(ticks); axT.set_xticklabels(["1000", "800", "700", "600 K"])
axT.set_xlabel("T (K)", fontsize=10)
for sp in ("top",): ax.spines[sp].set_visible(False)

import os, csv
OUT = os.path.join(os.path.dirname(__file__) or ".", "../../docs/figures/slide09_arrhenius")
os.makedirs(os.path.abspath(OUT), exist_ok=True)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "arrhenius_comp1_modelc.png"), dpi=300, bbox_inches="tight")
fig.savefig(os.path.join(OUT, "arrhenius_comp1_modelc.pdf"), bbox_inches="tight")

# clean CSV
with open(os.path.join(OUT, "arrhenius_data_clean.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["# AIMD-MLIP (UMA-s-1p1 omat) Li diffusion. lnD=lnD0-Ea/(kB*T)."])
    w.writerow(["# LPSCl(comp1 4fu): Ea=0.253 eV, D0=4.11e-4 | LPSCl1.6(modelc): Ea=0.224 eV, D0=5.75e-4"])
    w.writerow(["T_K", "1000overT", "D_LPSCl_cm2s", "D_LPSCl1.6_cm2s", "lnD_LPSCl", "lnD_LPSCl1.6"])
    for i in range(3):
        w.writerow([int(T[i]), f"{x[i]:.4f}",
                    f"{np.exp(SYS['LPSCl (comp1)']['lnD'][i]):.3e}",
                    f"{np.exp(SYS['LPSCl1.6 (modelc)']['lnD'][i]):.3e}",
                    f"{SYS['LPSCl (comp1)']['lnD'][i]:.4f}",
                    f"{SYS['LPSCl1.6 (modelc)']['lnD'][i]:.4f}"])
print("saved arrhenius_comp1_modelc.png/.pdf + arrhenius_data_clean.csv")
