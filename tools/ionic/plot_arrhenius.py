#!/usr/bin/env python3
"""plot_arrhenius.py — Li+ diffusion Arrhenius (AIMD-MLIP): LPSCl1.6 (modelc) vs
Nd2O3-doped. Data = db/properties/li_transport.json (UMA-s-1p1 omat MD,
600/800/1000 K). ln D = ln D0 - Ea/(kB T). The doping comparison: Nd+O lowers
D to ~0.62x modelc (sigma 0.52x) while Ea is essentially UNCHANGED -> a
prefactor/pathway slowdown, not a barrier effect. comp1 (LPSCl) shown light as
reference (slowest). Writes figure + clean CSV. CAVEAT (json): UMA Nd-4f
transferability unverified -> cite RATIO + Ea direction, not absolute sigma.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

KB = 8.617333e-5  # eV/K
T = np.array([600.0, 800.0, 1000.0])
x = 1000.0 / T
# ln D (cm^2/s) measured points — li_transport.json
SYS = {
    "LPSCl1.6 (modelc)":  dict(D=np.array([7.90e-6, 2.05e-5, 4.55e-5]),
                               Ea=0.2235, D0=5.8e-4,  c="#c0392b", m="s", z=4),
    "Nd$_2$O$_3$-doped":  dict(D=np.array([4.905e-6, 1.268e-5, 2.909e-5]),
                               Ea=0.2267, D0=3.778e-4, c="#1f9e9e", m="o", z=4),
}
REF = dict(D=np.array([3.09e-6, 1.03e-5, 2.20e-5]), Ea=0.2532, D0=4.11e-4,
           c="0.6", m="^", lab="LPSCl (comp1, ref)")   # slowest, light

fig, ax = plt.subplots(figsize=(7.8, 5.7))
xf = np.linspace(0.95, 1.72, 100)
# reference (comp1) light
ax.plot(x, np.log(REF["D"]), REF["m"], color=REF["c"], ms=7, mec="white", mew=0.6, zorder=3)
ax.plot(xf, np.log(REF["D0"]) - REF["Ea"]/(1000*KB)*xf, ":", color=REF["c"], lw=1.3,
        zorder=2, label=f"{REF['lab']}: E$_a$={REF['Ea']:.3f}")
for lab, s in SYS.items():
    ax.plot(x, np.log(s["D"]), s["m"], color=s["c"], ms=9, mec="white", mew=0.8, zorder=s["z"],
            label=f"{lab}: E$_a$={s['Ea']:.3f} eV")
    ax.plot(xf, np.log(s["D0"]) - s["Ea"]/(1000*KB)*xf, "--", color=s["c"], lw=1.7, zorder=3)

# doping arrow (nd below modelc at 600K)
ax.annotate("", xy=(1.6667, np.log(SYS["Nd$_2$O$_3$-doped"]["D"][0])),
            xytext=(1.6667, np.log(SYS["LPSCl1.6 (modelc)"]["D"][0])),
            arrowprops=dict(arrowstyle="->", color="#7d5ba6", lw=2))
ax.text(1.62, -12.0, "Nd+O:\nD 0.62×, σ 0.52×\nE$_a$ ~unchanged\n(prefactor/pathway)",
        color="#5a3f7a", fontsize=8.5, fontweight="bold", va="center", ha="right")

ax.set_xlabel(r"1000 / T  (K$^{-1}$)", fontsize=12)
ax.set_ylabel(r"ln $D_{Li}$  (cm$^2$/s)", fontsize=12)
ax.set_xlim(0.95, 1.74)
ax.set_title("Li$^+$ diffusion Arrhenius (AIMD–MLIP) — LPSCl1.6 vs Nd$_2$O$_3$-doped",
             fontsize=11.5, fontweight="bold")
ax.legend(loc="upper right", fontsize=9.5, framealpha=0.95)
ax.grid(alpha=0.25)
axT = ax.twiny(); axT.set_xlim(ax.get_xlim())
axT.set_xticks([1000/t for t in (1000, 800, 700, 600)])
axT.set_xticklabels(["1000", "800", "700", "600 K"]); axT.set_xlabel("T (K)", fontsize=10)
ax.spines["top"].set_visible(False)

import os, csv
OUT = os.path.join(os.path.dirname(__file__) or ".", "../../docs/figures/slide09_arrhenius")
os.makedirs(os.path.abspath(OUT), exist_ok=True)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "arrhenius_nd_vs_modelc.png"), dpi=300, bbox_inches="tight")
fig.savefig(os.path.join(OUT, "arrhenius_nd_vs_modelc.pdf"), bbox_inches="tight")

with open(os.path.join(OUT, "arrhenius_nd_vs_modelc.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["# AIMD-MLIP (UMA-s-1p1 omat) Li diffusion, nd vs modelc. lnD=lnD0-Ea/(kB*T)."])
    w.writerow(["# modelc(LPSCl1.6): Ea=0.2235 eV D0=5.80e-4 sigma300~14mS/cm | "
                "nd(Nd2O3-doped): Ea=0.2267 D0=3.78e-4 sigma300~7.3mS/cm | "
                "ratio nd/modelc: D 0.62, sigma300 0.52 | comp1(LPSCl ref): Ea=0.2532"])
    w.writerow(["# CAVEAT: UMA Nd-4f transferability unverified -> cite RATIO + Ea, not absolute sigma"])
    w.writerow(["T_K", "1000overT", "D_modelc_cm2s", "D_nd_cm2s", "D_comp1_cm2s",
                "lnD_modelc", "lnD_nd", "lnD_comp1"])
    for i in range(3):
        dm, dn, dc = SYS["LPSCl1.6 (modelc)"]["D"][i], SYS["Nd$_2$O$_3$-doped"]["D"][i], REF["D"][i]
        w.writerow([int(T[i]), f"{x[i]:.4f}", f"{dm:.3e}", f"{dn:.3e}", f"{dc:.3e}",
                    f"{np.log(dm):.4f}", f"{np.log(dn):.4f}", f"{np.log(dc):.4f}"])
print("saved arrhenius_nd_vs_modelc.png/.pdf + .csv")
