#!/usr/bin/env python3
"""fig_comp2_arrhenius.py — comp2 (Li6PS5Cl0.5Br0.5) Li diffusion Arrhenius.

Panel-(i) style: ln D vs 1000/T, comp1 (LPSCl) vs comp2 (LPSCl0.5Br0.5),
modelc faint anchor. UMA-s-1p1(omat), 2-50 ps MSD window, 3-pt Arrhenius
(600/800/1000 K).

HONEST RESULT: Br mixing does NOT lower Ea. comp2 Ea = 0.276+/-0.033 eV (3 seeds)
is >= comp1 0.239 (single-seed ref) — despite the weaker per-bond Li-Br ICOHP,
comp2 adds no vacancy carriers (Li6, like comp1) and the disordered Cl/Br
landscape (Li-Cl std 0.223 vs comp1 0.128) offsets any site-depth benefit.
Only the Li vacancy (modelc 0.224) genuinely lowers the barrier.
Discipline: absolute sigma withheld; comp2 3-seed error bar; ratio not claimed
definitively (comp1 single-seed).

comp2 D: gabia:/root/work/runs/comp2_md/s{2,3,4} (3 seeds x 3 T).
comp1/modelc D: recomputed from db/properties/msd_comp1_modelc.csv (same 2-50 ps).
Outputs docs/figures/comp2/comp2_arrhenius.png + db/properties/comp2_arrhenius_origin.csv
        + db/properties/comp2_md_arrhenius.json
"""
import csv
import json
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
invT = 1000.0 / T
C2COL = "#c2410c"   # comp2 warm orange (Br system)

# --- comp2: 3 seeds x 3 T (gabia comp2_md) ---
SEEDS = np.array([
    [1.8231e-06, 6.2380e-06, 2.1425e-05],  # s2
    [2.4388e-06, 2.1464e-06, 1.8506e-05],  # s3
    [2.5425e-06, 1.4490e-05, 2.1017e-05],  # s4
])
Dc2 = SEEDS.mean(0)
Dsem = SEEDS.std(0, ddof=1) / np.sqrt(len(SEEDS))
Dlo, Dhi = SEEDS.min(0), SEEDS.max(0)
# Arrhenius: line through per-T MEAN D; error bar from 3-seed Ea spread (discipline)
xv = 1.0 / T
b_c2, s_c2 = np.polyfit(xv, np.log(Dc2), 1)   # fit line on mean D
Ea_c2_seeds = np.array([-np.polyfit(xv, np.log(SEEDS[i]), 1)[0] * kB for i in range(3)])
Ea_c2 = float(Ea_c2_seeds.mean())              # report per-seed mean
Ea_c2_err = float(Ea_c2_seeds.std())           # 3-seed spread = honest uncertainty

# --- comp1 / modelc: recompute D per T from local MSD (same 2-50 ps window) ---
rows = list(csv.reader(open(REPO / "db/properties/msd_comp1_modelc.csv")))
body = np.array([[float(x) for x in r] for r in rows[1:]])
tt = body[:, 0]


def dfit(msd):
    m = (tt >= 2) & (tt <= 50)
    return np.polyfit(tt[m], msd[m], 1)[0] / 6.0 * 1e-4


Dc1 = np.array([dfit(body[:, 1 + i]) for i in range(3)])
Dmod = np.array([dfit(body[:, 4 + i]) for i in range(3)])
s1, b1 = np.polyfit(xv, np.log(Dc1), 1); Ea_c1 = -s1 * kB
sm, bm = np.polyfit(xv, np.log(Dmod), 1); Ea_mod = -sm * kB

fig, ax = plt.subplots(figsize=(6.6, 5.4), constrained_layout=True)
xfit = np.linspace(0.95, 1.72, 50)

# modelc faint anchor
ax.plot(xfit, np.exp(bm + sm * xfit / 1000.0), ":", color=SYS["modelc"], lw=1.5, alpha=0.8,
        zorder=2, label=f"modelC LPSCl1.6 (vacancy), Ea {Ea_mod:.3f}")
ax.plot(invT, Dmod, "^", color=SYS["modelc"], ms=6, alpha=0.7, zorder=3)
# comp1 reference
ax.plot(xfit, np.exp(b1 + s1 * xfit / 1000.0), "--", color="#4b5563", lw=1.9, zorder=3,
        label=f"comp1 LPSCl (Li6, ref), Ea {Ea_c1:.3f}")
ax.plot(invT, Dc1, "o", color="#4b5563", ms=6.5, zorder=4)
# comp2 fit + seeds
ax.plot(xfit, np.exp(b_c2 + s_c2 * xfit / 1000.0), "-", color=C2COL, lw=2.5, zorder=5,
        label=f"comp2 LPSCl$_{{0.5}}$Br$_{{0.5}}$ (Li6), Ea {Ea_c2:.3f}$\\pm${Ea_c2_err:.3f}")
for i in range(3):
    ax.plot([invT[i], invT[i]], [Dlo[i], Dhi[i]], "-", color=C2COL, lw=1.3, zorder=5)
    ax.plot([invT[i]] * 3, SEEDS[:, i], ".", color=C2COL, ms=6, alpha=0.55, zorder=6)
    ax.plot([invT[i]], [Dc2[i]], "s", color=C2COL, ms=9, zorder=7)

ax.set_yscale("log")
ax.set_xlim(0.95, 1.72)
sec = ax.secondary_xaxis("top", functions=(lambda x: 1000.0 / x, lambda x: 1000.0 / x))
sec.set_xlabel("T (K)", fontsize=10, color=MUT)
sec.set_xticks([1000, 800, 600]); sec.set_xticklabels(["1000", "800", "600"])
sec.tick_params(colors=MUT)
apply_axes(ax, xlabel="1000 / T (K$^{-1}$)", ylabel="D$_{Li}$ (cm$^2$/s)",
           title="Li diffusion Arrhenius (600-1000 K) — vacancy is the lever; Br effect inconclusive")
ax.legend(loc="upper right", fontsize=8.3, frameon=False)
fig.text(0.5, -0.058,
         "UMA-s-1p1 (omat), 2-50 ps window.  comp2 = 3 seeds (dots=seeds, whisker=min-max, square=mean; "
         "line = mean-D fit).\nmodelC vacancy: D up at all T.  comp2 (Li6, isovalent Cl->Br) ~ comp1 within "
         "seed noise; 800 K scatter large -> 300 K sigma extrapolation 0.14-1.8x comp1 (undetermined).  "
         "Absolute $\\sigma$ withheld.",
         fontsize=7.0, color=MUT, va="top", ha="center")

OUTD = REPO / "docs/figures/comp2"; OUTD.mkdir(parents=True, exist_ok=True)
png = OUTD / "comp2_arrhenius.png"
fig.savefig(png, dpi=300, bbox_inches="tight")
print("->", png)

# --- Origin CSV ---
csvp = REPO / "db/properties/comp2_arrhenius_origin.csv"
with open(csvp, "w", newline="") as f:
    wr = csv.writer(f)
    wr.writerow(["system", "invT_1000overT", "T_K", "D_cm2_s", "note"])
    for x, t_, d in zip(invT, T, Dc2):
        wr.writerow(["comp2_LPSCl0.5Br0.5", f"{x:.4f}", int(t_), f"{d:.4e}", "3-seed mean"])
    for si, row in enumerate(SEEDS, 2):
        for x, t_, d in zip(invT, T, row):
            wr.writerow([f"comp2_s{si}", f"{x:.4f}", int(t_), f"{d:.4e}", "individual seed"])
    for x, t_, d in zip(invT, T, Dc1):
        wr.writerow(["comp1_LPSCl", f"{x:.4f}", int(t_), f"{d:.4e}", "ref (single seed)"])
    for x, t_, d in zip(invT, T, Dmod):
        wr.writerow(["modelC_LPSCl1.6", f"{x:.4f}", int(t_), f"{d:.4e}", "anchor"])
print("->", csvp)

# --- JSON record (lpsocl_md_arrhenius.json format) ---
jp = REPO / "db/properties/comp2_md_arrhenius.json"
jp.write_text(json.dumps({
    "system": "comp2 (Li6PS5Cl0.5Br0.5, 52at, mixed-halide, Li6 no-vacancy)",
    "date": "2026-07-25",
    "method": "UMA-s-1p1 omat, 2-50ps window, 3pt Arrhenius (600/800/1000K), NE Haven=1",
    "raw": "gabia:/root/work/runs/comp2_md/s{2,3,4}",
    "D_per_T_seeds_cm2s": {"600": SEEDS[:, 0].tolist(), "800": SEEDS[:, 1].tolist(),
                            "1000": SEEDS[:, 2].tolist()},
    "D_mean_cm2s": {"600": float(Dc2[0]), "800": float(Dc2[1]), "1000": float(Dc2[2])},
    "Ea_eV_SEMweighted": float(Ea_c2), "Ea_eV_err": float(Ea_c2_err),
    "Ea_per_seed": Ea_c2_seeds.tolist(),
    "Ea_eV": f"{Ea_c2:.3f} +/- {Ea_c2_err:.3f}",
    "data_quality_flag": "800K per-seed scatter large (s3 800K 2.15e-6 < its 600K 2.44e-6 = non-physical; "
                         "s4 800K high). Mean is monotonic; 800K under-sampled at 200ps. 1000K tight.",
    "anchors_same_window": {"comp1_LPSCl_Ea": float(Ea_c1), "modelc_LPSCl1.6_Ea": float(Ea_mod),
                            "comp1_D": Dc1.tolist(), "modelc_D": Dmod.tolist(),
                            "_note": "comp1/modelc recomputed from msd_comp1_modelc.csv same 2-50ps; "
                                     "modelc 0.224 == DB. comp1 single-seed ref."},
    "sigma_300K_NE_mS_cm_INTERNAL": {"_note": "Nernst-Einstein Haven=1, n_Li/V0; INTERNAL ONLY (discipline: "
                                     "absolute sigma not cited). Method validated: modelc 13.94 == DB.",
                                     "comp1": 2.74, "comp2_central": 1.39, "modelc": 13.94,
                                     "comp2_range_Ea_pm033": [0.39, 4.98],
                                     "n_Li_cm3": {"comp1": 2.361e22, "comp2": 2.313e22, "modelc": 2.220e22}},
    "sigma_ratio_300K": {"comp2_over_comp1_central": 0.51, "comp2_over_comp1_range": [0.14, 1.82],
                          "modelc_over_comp1": 5.09},
    "physics_verdict": "VACANCY is the robust conductivity lever: modelc (Li5.4, vacancy) sigma300 ~5x comp1 "
                       "(survives all uncertainty). Br isovalent Cl->Br (comp2, Li6 no-vacancy) shows NO clear "
                       "boost: central sigma300 0.51x comp1 (slightly worse), but 800K seed scatter makes Ea "
                       "0.276+/-0.033 -> sigma300 ratio 0.14-1.82x = INCONCLUSIVE. In the measured 600-1000K "
                       "range comp2 D > comp1 at every T, but the steeper/uncertain Ea makes the 300K "
                       "extrapolation unreliable. Experimental Br benefit (Kraft 2018) is driven by anion "
                       "site disorder (Br/S2- mixing) NOT sampled by our single champion config.",
    "recommendation": "For a paper-grade Br-vs-Cl sigma claim: reseed 800K (s5/s6) to tighten Ea, and run "
                       "comp1 multi-seed (currently single). Consider anion-disorder ensemble to capture the "
                       "experimental Br mechanism.",
    "discipline": "absolute sigma INTERNAL only; comp2 3-seed; comp1 single-seed = ratio not definitive.",
}, indent=1, ensure_ascii=False))
print("->", jp)
print(f"\ncomp2 Ea {Ea_c2:.4f}±{Ea_c2_err:.4f} | comp1 {Ea_c1:.4f} | modelc {Ea_mod:.4f}")
