#!/usr/bin/env python3
"""fig_lpsocl_arrhenius.py — LPSOCl Li diffusion Arrhenius vs modelc/b2o3 family.

2026-07-18. UMA-s-1p1(omat), 2-50 ps MSD window, 3-pt Arrhenius (600/800/1000 K).
LPSOCl: 600 K reseeded x4 (ladder+s2/s3/s4, 200 ps each) -> Ea error bar; 800/1000 K
single-seed. Anchors modelc/b2o3 same window (db/properties/b2o3_vs_modelc_md.json).
Outputs docs/figures/lpsocl/lpsocl_arrhenius.png + db/properties/lpsocl_arrhenius_origin.csv
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
T = np.array([600., 800., 1000.])
invT = 1000.0 / T  # 1000/T axis

# --- LPSOCl (this work): 4 seeds (ladder=s1 + reseeds s2/s3/s4) x 3 T, 2026-07-18 ---
SEEDS = np.array([
    [3.887e-6, 2.085e-5, 5.525e-5],   # s1 (ladder)
    [6.405e-6, 2.789e-5, 6.962e-5],   # s2
    [5.820e-6, 1.896e-5, 4.428e-5],   # s3
    [8.970e-6, 2.895e-5, 5.922e-5],   # s4
])
Dl = SEEDS.mean(0)                      # per-T mean
Dsem = SEEDS.std(0, ddof=1) / np.sqrt(len(SEEDS))
Dlo, Dhi = SEEDS.min(0), SEEDS.max(0)
# SEM-weighted Arrhenius fit (all 4 seeds inform each T mean)
lnErr = Dsem / Dl
w = 1 / lnErr ** 2
xv = 1 / T
Dm = np.linalg.solve(
    np.array([[w.sum(), (w * xv).sum()], [(w * xv).sum(), (w * xv * xv).sum()]]),
    np.array([(w * np.log(Dl)).sum(), (w * xv * np.log(Dl)).sum()]))
b_lp, s_lp = Dm[0], Dm[1]
Ea_lp = -s_lp * kB
Ea_err = np.sqrt(w.sum() / (w.sum() * (w * xv * xv).sum() - (w * xv).sum() ** 2)) * kB

# --- anchors ---
Dmod = np.array([7.901e-6, 2.054e-5, 4.554e-5]); Ea_mod = 0.2235
Db = np.array([9.174e-6, 3.009e-5, 5.067e-5]); Ea_b = 0.2234

fig, ax = plt.subplots(figsize=(6.6, 5.4), constrained_layout=True)
xfit = np.linspace(0.95, 1.72, 50)

def line(D3, T3=T):
    s, b = np.polyfit(1 / T3, np.log(D3), 1)
    return np.exp(b) * np.exp(s * (xfit / 1000.0 * 1000.0) / 1000.0 * 0 + s * (xfit / 1.0) * 0), s, b

# plot anchors as faint lines+points
for D3, Ea, c, lab in [(Dmod, Ea_mod, SYS["modelc"], f"modelC (undoped), Ea {Ea_mod:.3f}"),
                       (Db, Ea_b, SYS["b2o3"], f"+B2O3, Ea {Ea_b:.3f}")]:
    s, b = np.polyfit(1 / T, np.log(D3), 1)
    ax.plot(xfit, np.exp(b + s * (xfit / 1000.0) ** -1 * 0 + s * (1000.0 / xfit) / 1000.0 * 0), alpha=0)  # noop
    yy = np.exp(b + s * (xfit))  # xfit already = 1000/T -> need 1/T = xfit/1000
    ax.plot(xfit, np.exp(b + s * xfit / 1000.0), "--", color=c, lw=1.6, alpha=0.8, zorder=2)
    ax.plot(invT, D3, "o", color=c, ms=6, alpha=0.85, zorder=3, label=lab)

# LPSOCl fit line + points (4 seeds at every T)
ax.plot(xfit, np.exp(b_lp + s_lp * xfit / 1000.0), "-", color=SYS["lpsocl"], lw=2.4, zorder=4,
        label=f"+O LPSOCl (this work), Ea {Ea_lp:.3f}$\\pm${Ea_err:.3f}")
for i in range(3):
    ax.plot([invT[i], invT[i]], [Dlo[i], Dhi[i]], "-", color=SYS["lpsocl"], lw=1.3, zorder=5)
    ax.plot([invT[i]] * len(SEEDS), SEEDS[:, i], ".", color=SYS["lpsocl"], ms=5, alpha=0.55, zorder=6)
    ax.plot([invT[i]], [Dl[i]], "s", color=SYS["lpsocl"], ms=9, zorder=7)

ax.set_yscale("log")
ax.set_xlim(0.95, 1.72)
sec = ax.secondary_xaxis("top", functions=(lambda x: 1000.0 / x, lambda x: 1000.0 / x))
sec.set_xlabel("T (K)", fontsize=10, color=MUT)
sec.set_xticks([1000, 800, 600]); sec.set_xticklabels(["1000", "800", "600"])
sec.tick_params(colors=MUT)
apply_axes(ax, xlabel="1000 / T (K$^{-1}$)", ylabel="D$_{Li}$ (cm$^2$/s)",
           title="Li diffusion Arrhenius — O-doping raises the barrier (2$\\sigma$)")
ax.legend(loc="upper right", fontsize=8.5, frameon=False)
ax.text(0.5, 0.02,
        "UMA-s-1p1 (omat), 2-50 ps window.  ALL T = 4 seeds (dots=seeds, whisker=min-max, square=mean);\n"
        "SEM-weighted fit -> Ea +63 meV vs modelC = 2.0$\\sigma$ (higher barrier confirmed).  "
        "Absolute $\\sigma$ withheld (discipline).",
        transform=ax.transAxes, fontsize=7.3, color=MUT, va="bottom", ha="center")

OUTD = REPO / "docs/figures/lpsocl"; OUTD.mkdir(parents=True, exist_ok=True)
png = OUTD / "lpsocl_arrhenius.png"
fig.savefig(png, dpi=300)
print("->", png)

csvp = REPO / "db/properties/lpsocl_arrhenius_origin.csv"
with open(csvp, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["system", "invT_1000overT", "T_K", "D_cm2_s", "note"])
    for x, tt, d in zip(invT, T, Dl):
        w.writerow(["LPSOCl", f"{x:.4f}", int(tt), f"{d:.4e}",
                    "600K=4seed mean" if tt == 600 else "single seed"])
    for si, row in enumerate(SEEDS, 1):
        for x, tt, d in zip(invT, T, row):
            w.writerow([f"LPSOCl_s{si}", f"{x:.4f}", int(tt), f"{d:.4e}", "individual seed"])
    for x, tt, d in zip(invT, T, Dmod):
        w.writerow(["modelC", f"{x:.4f}", int(tt), f"{d:.4e}", "anchor"])
    for x, tt, d in zip(invT, T, Db):
        w.writerow(["b2o3", f"{x:.4f}", int(tt), f"{d:.4e}", "anchor"])
print("->", csvp)
Eas = np.array([-np.polyfit(xv, np.log(m), 1)[0] * kB for m in SEEDS])
print(f"Ea LPSOCl {Ea_lp:.4f} +/- {Ea_err:.4f} eV (SEM-weighted) | per-seed {Eas.round(3)}")
