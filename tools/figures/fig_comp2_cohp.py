#!/usr/bin/env python3
"""fig_comp2_cohp.py — comp2 (Li6PS5Cl0.5Br0.5) energy-resolved pCOHP curves.

Panel-style COHP (matching the paper Fig-v layout): three vertical panels
Li-S | Li-Cl | Li-Br, filled -pCOHP vs E-E_F, E_F dashed, ICOHP box.
The Cl-vs-Br punchline is INTRA-CELL (same structure, same LOBSTER basis, no
comp1 needed): per-bond Li-Br (-1.934) weaker than Li-Cl (-2.111).

Curves are per-bond MEAN (-pCOHP summed over matched bonds / n) so Li-Cl (10
bonds) and Li-Br (12 bonds) are compared as bond STRENGTH, not bond count; the
integral of each mean curve to E_F = the canonical mean ICOHP.

Data provenance: gabia:/data/work/runs/comp2_lobster/COHPCAR.lobster
(LOBSTER 5.1.1, comp2_V0_v3_relaxed champion, pbeVaspFit2015, spilling 1.37%),
parsed via tools/modelc_v3/plot_lobster_4panel.parse_cohpcar with comp2.json
distance cutoffs (Li-S 2.9 / Li-Cl 3.3 / Li-Br 3.5 A). Cross-checked: n=72/10/12,
mean ICOHP -2.504/-2.111/-1.934 eV == db/compositions/comp2.json icohp_lobster_v3.
Outputs docs/figures/comp2/comp2_cohp.png + db/properties/comp2_cohp_curves_origin.csv
"""
import csv
import io
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))
from tools.figures.house_style import INK, MUT, ELEM, apply_axes  # noqa: E402

BR = "#a16207"  # amber-700 for Br (consistent with fig_comp2_icohp.py)
BONDCOL = {"Li-S": ELEM["S"], "Li-Cl": ELEM["Cl"], "Li-Br": BR}
NBOND = {"Li-S": 72, "Li-Cl": 10, "Li-Br": 12}  # matched bonds (comp2.json cutoffs)

# canonical ICOHP (eV/bond) from comp2.json icohp_lobster_v3 (cross-checked)
ic = json.loads((REPO / "db/compositions/comp2.json").read_text())["icohp_lobster_v3"]
ICOHP = {"Li-S": ic["mean_ICOHP_eV"]["Li-S"], "Li-Cl": ic["mean_ICOHP_eV"]["Li-Cl"],
         "Li-Br": ic["mean_ICOHP_eV"]["Li-Br"]}

# --- SUMMED -pCOHP curves (E-E_F, Li-S, Li-Cl, Li-Br), gabia comp2_lobster ---
DATA = """\
E_minus_EF_eV,-pCOHP_Li-S,-pCOHP_Li-Cl,-pCOHP_Li-Br
-12.000,1.68570,-0.00168,-0.00265
-11.925,0.15274,-0.00012,-0.00023
-11.849,0.01333,-0.00001,-0.00002
-11.774,0.00000,0.00000,-0.00000
-11.322,0.00487,0.00000,0.00000
-11.247,0.15975,0.00001,0.00003
-11.172,1.39361,0.00012,0.00025
-11.096,9.58293,0.00087,0.00155
-11.021,33.86848,0.00314,0.00497
-10.946,77.21142,0.00729,0.00974
-10.870,106.42758,0.01011,0.01120
-10.795,85.98918,0.00815,0.00703
-10.720,42.73903,0.00401,0.00238
-10.644,13.33725,0.00124,0.00046
-10.569,2.15141,0.00020,0.00002
-10.494,0.27946,0.00003,-0.00000
-10.418,0.01053,0.00000,-0.00000
-8.987,0.00010,-0.00000,-0.00000
-8.912,0.00230,-0.00001,-0.00001
-8.837,0.02454,-0.00014,-0.00016
-8.762,0.14704,-0.00083,-0.00094
-8.686,0.56671,-0.00319,-0.00362
-8.611,1.32570,-0.00724,-0.00825
-8.536,2.29087,-0.01096,-0.01268
-8.460,4.04318,-0.01364,-0.01624
-8.385,8.33418,-0.01687,-0.01994
-8.310,15.18461,-0.01590,-0.01671
-8.234,21.99293,-0.00432,0.00005
-8.159,24.95837,0.00896,0.01607
-8.084,22.29925,0.01201,0.01660
-8.008,16.37110,0.00757,0.00862
-7.933,9.71829,0.00339,0.00310
-7.858,4.33704,0.00148,0.00125
-7.782,1.36710,0.00060,0.00056
-7.707,0.26271,0.00016,0.00016
-7.632,0.03661,0.00003,0.00003
-5.975,0.00005,0.00000,0.00000
-5.900,0.00279,0.00001,0.00002
-5.824,0.03121,0.00014,0.00019
-5.749,0.25141,0.00115,0.00147
-5.674,1.15748,0.00528,0.00654
-5.598,3.54446,0.01663,0.01954
-5.523,7.31151,0.03784,0.04053
-5.448,11.27636,0.07525,0.06851
-5.372,14.63943,0.13764,0.10820
-5.297,16.54247,0.21133,0.15632
-5.222,16.13879,0.25829,0.19271
-5.146,14.92324,0.27694,0.21818
-5.071,15.85488,0.30805,0.25886
-4.996,19.30584,0.35101,0.30683
-4.921,22.57186,0.36385,0.32425
-4.845,22.69908,0.32073,0.28995
-4.770,19.10743,0.23660,0.21855
-4.695,13.16085,0.14365,0.13651
-4.619,7.06141,0.06806,0.06639
-4.544,2.78213,0.02388,0.02370
-4.469,0.72445,0.00555,0.00558
-4.393,0.12516,0.00086,0.00088
-4.318,0.01332,0.00014,0.00009
-4.243,0.00257,0.00917,0.00033
-4.167,0.01842,0.09561,0.00311
-4.092,0.14302,0.77659,0.02319
-4.017,0.57572,3.25316,0.09141
-3.941,1.46583,8.67297,0.24866
-3.866,2.38238,14.29386,0.57001
-3.791,3.10039,16.01313,1.75604
-3.715,4.56390,16.50245,5.00859
-3.640,7.10434,20.04112,10.70973
-3.565,8.71645,22.91639,15.89844
-3.490,8.01031,19.26373,17.39763
-3.414,6.85722,11.30608,17.33486
-3.339,7.09741,4.65469,18.93169
-3.264,8.05430,1.39761,20.45027
-3.188,8.81799,0.46442,18.42527
-3.113,9.81308,0.12056,13.19984
-3.038,11.65416,-0.14089,7.01433
-2.962,14.35859,-0.27904,2.48780
-2.887,18.58152,-0.24897,0.78778
-2.812,23.26220,-0.19175,0.66177
-2.736,25.87940,-0.24229,1.04098
-2.661,27.05028,-0.37059,1.33736
-2.586,30.09683,-0.47662,1.33588
-2.510,35.87017,-0.56359,1.13697
-2.435,41.40910,-0.67078,0.91506
-2.360,43.84614,-0.76144,0.74572
-2.285,41.52394,-0.78520,0.59198
-2.209,35.51343,-0.76777,0.41886
-2.134,28.54492,-0.75642,0.23809
-2.059,23.09282,-0.74318,0.07088
-1.983,19.07925,-0.65964,-0.05295
-1.908,16.16505,-0.51706,-0.14742
-1.833,16.81058,-0.42927,-0.26448
-1.757,20.97980,-0.45021,-0.40544
-1.682,26.30077,-0.54187,-0.53279
-1.607,30.99067,-0.63318,-0.63931
-1.531,35.02609,-0.67388,-0.71069
-1.456,38.26520,-0.66239,-0.74092
-1.381,40.30836,-0.63624,-0.75914
-1.305,40.89692,-0.61739,-0.78720
-1.230,38.13588,-0.57254,-0.78430
-1.155,32.77840,-0.49668,-0.73304
-1.079,27.49205,-0.42260,-0.66295
-1.004,23.84063,-0.36670,-0.60746
-0.929,20.17584,-0.30688,-0.53326
-0.854,14.78218,-0.22649,-0.40306
-0.778,8.73199,-0.14091,-0.23982
-0.703,4.13366,-0.07377,-0.10877
-0.628,1.78133,-0.03474,-0.04184
-0.552,0.61959,-0.01282,-0.01210
-0.477,0.18947,-0.00395,-0.00330
-0.402,0.03439,-0.00071,-0.00056
-0.326,0.00543,-0.00011,-0.00009
-0.251,0.00032,-0.00001,-0.00001
-0.100,0.00000,0.00000,0.00000
1.105,-0.00003,-0.00000,-0.00000
1.180,-0.00066,-0.00001,-0.00001
1.255,-0.00517,-0.00011,-0.00007
1.331,-0.03146,-0.00067,-0.00041
1.406,-0.09929,-0.00211,-0.00130
1.481,-0.19604,-0.00417,-0.00257
1.556,-0.23374,-0.00497,-0.00307
1.632,-0.15978,-0.00340,-0.00210
1.707,-0.06468,-0.00138,-0.00085
1.782,-0.01804,-0.00041,-0.00028
1.858,-0.01531,-0.00068,-0.00067
1.933,-0.09674,-0.00528,-0.00541
2.008,-0.37338,-0.02274,-0.02357
2.084,-0.97565,-0.06702,-0.07026
2.159,-1.61188,-0.12319,-0.12972
2.234,-1.82130,-0.15708,-0.16408
2.310,-1.65416,-0.16022,-0.16298
2.385,-1.33908,-0.13693,-0.13228
2.460,-1.02902,-0.10149,-0.09142
2.536,-0.87357,-0.07963,-0.06860
2.611,-0.84764,-0.07617,-0.06586
2.686,-0.66973,-0.06614,-0.05733
2.762,-0.31068,-0.04589,-0.03897
2.837,-0.04256,-0.04039,-0.03467
2.912,0.02301,-0.06362,-0.05891
2.987,-0.07872,-0.12736,-0.12610
3.063,-0.34012,-0.27650,-0.27824
3.138,-0.93222,-0.71074,-0.71669
3.213,-2.05612,-1.62510,-1.68837
3.289,-3.66032,-2.90891,-3.16093
3.364,-5.03301,-3.89484,-4.40520
3.439,-5.47510,-3.98715,-4.67599
3.515,-4.84576,-3.27179,-3.97333
3.590,-3.54296,-2.32515,-2.89150
3.665,-2.77392,-1.94463,-2.34942
3.741,-3.32174,-2.44496,-2.70151
3.816,-4.57035,-3.34065,-3.48877
3.891,-5.61204,-3.94925,-4.17007
3.967,-6.63957,-4.22722,-4.67032
4.042,-8.43854,-4.77384,-5.32905
4.117,-9.84198,-5.31295,-5.76293
4.192,-9.02588,-4.92147,-5.24334
4.268,-6.96157,-3.98864,-4.30306
4.343,-5.68760,-3.39989,-3.77452
4.418,-6.30521,-3.26089,-3.79791
4.494,-9.38475,-3.46863,-4.32701
4.569,-14.05918,-3.96009,-5.13947
4.644,-18.55415,-4.33120,-5.68824
4.720,-22.57047,-4.06662,-5.42362
4.795,-27.85406,-3.27480,-4.40527
4.870,-33.91367,-2.60468,-3.39928
4.946,-36.72248,-2.31850,-2.88620
5.021,-35.30967,-2.31184,-2.86689
5.096,-32.65706,-2.45446,-3.09999
5.172,-30.65076,-2.47593,-3.08865
5.247,-30.11463,-2.30795,-2.73150
5.322,-31.92412,-2.19182,-2.46706
5.397,-35.28852,-2.20234,-2.52246
5.473,-37.89195,-2.27423,-2.74542
5.548,-38.66354,-2.45434,-2.93310
5.623,-38.63180,-2.69260,-2.97071
5.699,-37.65495,-2.83352,-2.92606
5.774,-34.22907,-2.86596,-2.97132
5.849,-29.44593,-2.85318,-3.06791
5.925,-26.73361,-2.82848,-2.98655
6.000,-27.87810,-2.90246,-2.80507
"""

rows = list(csv.reader(io.StringIO(DATA)))
hdr, body = rows[0], np.array([[float(x) for x in r] for r in rows[1:]])
E = body[:, 0]
order = ["Li-S", "Li-Cl", "Li-Br"]
# per-bond MEAN -pCOHP (sum / n) -> integral to E_F = mean ICOHP
mean_curve = {b: body[:, i + 1] / NBOND[b] for i, b in enumerate(order)}

fig, axes = plt.subplots(1, 3, figsize=(9.2, 5.0), sharey=True, constrained_layout=True)
YLIM = (-12, 6)
for ax, b in zip(axes, order):
    c = mean_curve[b]
    col = BONDCOL[b]
    xmax = max(np.abs(c).max() * 1.15, 0.2)
    bonding = np.where(c > 0, c, 0)
    anti = np.where(c < 0, c, 0)
    ax.fill_betweenx(E, 0, bonding, color=col, alpha=0.6, lw=0)
    ax.fill_betweenx(E, 0, anti, color=col, alpha=0.28, lw=0)
    ax.plot(c, E, "-", color=col, lw=1.0)
    ax.axvline(0, color="k", lw=0.7)
    ax.axhline(0, color=MUT, ls="--", lw=0.9)          # E_F
    ax.set_xlim(-xmax, xmax)
    ax.set_ylim(YLIM)
    apply_axes(ax, xlabel=r"$-$pCOHP / bond", title=b)
    ax.title.set_color(col)
    ax.title.set_fontweight("bold")
    # E_F, antibonding/bonding tags
    ax.text(xmax * 0.94, 0.15, r"$E_F$", fontsize=8.5, color=MUT, ha="right", va="bottom")
    ax.text(-xmax * 0.9, YLIM[1] - 0.7, "anti", fontsize=7.5, style="italic",
            color="#b0b0b0", ha="left", va="top")
    ax.text(xmax * 0.9, YLIM[1] - 0.7, "bond", fontsize=7.5, style="italic",
            color="#b0b0b0", ha="right", va="top")
    # ICOHP box
    ax.text(0, YLIM[0] + 0.5, f"ICOHP\n{ICOHP[b]:.3f} eV\n(n={NBOND[b]})",
            ha="center", va="bottom", fontsize=9, fontweight="bold", color=INK,
            bbox=dict(boxstyle="round,pad=0.35", facecolor="white", edgecolor=col, lw=1.1))
axes[0].set_ylabel(r"$E - E_F$  (eV)", fontsize=12, color=INK)

# Cl vs Br punchline between panels 2 and 3
dlt = -ICOHP["Li-Cl"] - (-ICOHP["Li-Br"])
fig.suptitle("comp2  Li$_6$PS$_5$Cl$_{0.5}$Br$_{0.5}$  —  LOBSTER pCOHP  "
             f"(same-cell Cl vs Br:  Br weaker by {dlt:.3f} eV)",
             fontsize=11.5, color=INK, y=1.04)
fig.text(0.5, -0.03,
         "Per-bond mean $-$pCOHP (v3 champion, spilling 1.37%).  Bonding states fill below $E_F$; "
         "Li-halide bonding centered ~$-$3.5 eV.  Li-Br ICOHP (-1.934) < Li-Cl (-2.111) = Br softens the ionic bond.",
         ha="center", fontsize=7.6, color=MUT)

OUTD = REPO / "docs/figures/comp2"; OUTD.mkdir(parents=True, exist_ok=True)
png = OUTD / "comp2_cohp.png"
fig.savefig(png, dpi=300, bbox_inches="tight")
print("->", png)

# ---- Origin-ready CSV (per-bond mean -pCOHP curves) ----
csvp = REPO / "db/properties/comp2_cohp_curves_origin.csv"
with open(csvp, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["E_minus_EF_eV", "mean_pCOHP_Li-S", "mean_pCOHP_Li-Cl", "mean_pCOHP_Li-Br"])
    for i, e in enumerate(E):
        w.writerow([f"{e:.3f}"] + [f"{mean_curve[b][i]:.5f}" for b in order])
print("->", csvp)
# integral cross-check: integral of (-pCOHP) to E_F = -ICOHP (downsampled -> approximate)
_trapz = getattr(np, "trapezoid", getattr(np, "trapz", None))
for b in order:
    m = E <= 0
    integ = _trapz(mean_curve[b][m], E[m])
    print(f"  {b}: integral(-pCOHP,mean) to E_F = {integ:+.3f}  vs -ICOHP {-ICOHP[b]:+.3f} (approx, downsampled)")
