#!/usr/bin/env python3
"""fig_comp2_msd.py — Li MSD(t) for comp1 (LPSCl) vs comp2 (LPSCl0.5Br0.5).

Panel-(ii) style: two sub-panels (comp1 | comp2), each with 600/800/1000 K Li
MSD vs time (0-100 ps). D is fit on the 2-50 ps window (dashed guide).

comp2 MSD: gabia:/root/work/runs/comp2_md/s{2,3,4} seed-averaged.
comp1 MSD: db/properties/msd_comp1_modelc.csv (cols comp1_*).
Outputs docs/figures/comp2/comp2_msd.png + db/properties/comp2_msd_origin.csv
"""
import csv
import io
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))
from tools.figures.house_style import INK, MUT, apply_axes  # noqa: E402

TCOL = {600: "#2563eb", 800: "#ea580c", 1000: "#b91c1c"}   # temperature ramp

# --- comp2 seed-averaged MSD (gabia), 0-100 ps ---
C2 = """\
t_ps,comp2_600K,comp2_800K,comp2_1000K
0.000,0.0000,0.0000,0.0000
1.600,3.3870,5.9327,6.5360
3.200,5.3959,7.9581,9.0131
4.800,5.2621,8.6242,12.5158
6.400,6.3607,10.2820,15.3388
8.000,8.8218,10.3062,18.1040
9.600,8.8309,11.4881,17.2833
11.200,8.7630,14.9142,20.5085
12.800,8.0654,15.5284,21.7153
14.400,9.5160,15.3740,24.7761
16.000,8.2786,15.4943,25.9394
17.600,9.3526,15.6183,24.6041
19.200,9.4047,14.9287,29.8245
20.800,9.5093,17.3553,31.5621
22.400,10.5978,17.5500,34.4735
24.000,10.7045,21.5480,37.8097
25.600,10.6826,22.0503,39.8307
27.200,11.9935,22.3737,44.2608
28.800,12.9232,22.9002,47.2674
30.400,13.5525,23.3422,46.6464
32.000,13.4307,24.2699,49.7888
33.600,12.3099,22.9410,50.3316
35.200,13.0708,25.8466,51.0819
36.800,13.9431,27.2654,52.8941
38.400,12.4458,26.1228,50.0823
40.000,11.5400,27.7820,55.8347
41.600,11.6846,24.9712,58.3739
43.200,11.6615,27.1628,61.0739
44.800,11.1484,25.1961,61.0064
46.400,11.1610,27.0450,62.9210
48.000,11.4597,29.6380,61.6243
49.600,11.8500,29.7620,63.6696
51.200,12.0387,29.3363,66.4397
52.800,12.2390,28.2221,71.7016
54.400,12.8915,28.0757,73.7089
56.000,12.3670,26.9727,72.0054
57.600,12.3074,24.8691,71.8143
59.200,12.4718,24.9394,73.3125
60.800,13.1236,25.0240,73.3891
62.400,12.4524,25.9863,77.9093
64.000,12.1523,24.0579,83.6645
65.600,12.7307,26.1481,88.8978
67.200,12.1189,27.2361,93.2331
68.800,12.0916,23.8201,97.4514
70.400,11.8126,24.1042,101.6862
72.000,12.2357,22.7525,103.9574
73.600,11.4237,24.4022,98.8899
75.200,12.4540,28.2579,102.0112
76.800,13.4747,28.3855,105.5799
78.400,13.0569,29.1225,108.6694
80.000,13.0252,28.5205,107.0861
81.600,13.6325,27.4624,109.4403
83.200,13.6028,28.0364,112.0548
84.800,13.7287,27.9207,114.8675
86.400,13.5679,31.9510,117.6591
88.000,12.5936,31.5661,119.9945
89.600,12.2910,30.7984,117.8652
91.200,12.2350,30.3070,120.3009
92.800,14.1605,29.0457,121.0566
94.400,13.0807,28.0529,120.5622
96.000,12.3160,29.2767,120.5647
97.600,12.4783,33.0976,115.4390
99.200,12.7189,33.4908,113.6787
100.800,12.0182,31.3356,114.6551
"""
r2 = np.array([[float(x) for x in row] for row in list(csv.reader(io.StringIO(C2)))[1:]])
t2 = r2[:, 0]
msd2 = {600: r2[:, 1], 800: r2[:, 2], 1000: r2[:, 3]}

# --- comp1 MSD from local (0.1 ps grid to 100 ps) ---
rows = list(csv.reader(open(REPO / "db/properties/msd_comp1_modelc.csv")))
b1 = np.array([[float(x) for x in r] for r in rows[1:]])
t1 = b1[:, 0]
msd1 = {600: b1[:, 1], 800: b1[:, 2], 1000: b1[:, 3]}

fig, (axA, axB) = plt.subplots(1, 2, figsize=(9.6, 4.6), sharey=True, constrained_layout=True)
for ax, (t, msd, name) in [(axA, (t1, msd1, "comp1  Li$_6$PS$_5$Cl  (LPSCl)")),
                           (axB, (t2, msd2, "comp2  Li$_6$PS$_5$Cl$_{0.5}$Br$_{0.5}$"))]:
    m = t <= 100
    for T in (600, 800, 1000):
        ax.plot(t[m], msd[T][m], "-", color=TCOL[T], lw=1.8, label=f"{T} K")
    # 2-50 ps fit window shading
    ax.axvspan(2, 50, color="#f1f5f9", zorder=0)
    apply_axes(ax, xlabel="Time (ps)", title=name)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 125)
axA.set_ylabel(r"Li MSD ($\AA^2$)", fontsize=12, color=INK)
axB.legend(loc="upper left", fontsize=9, frameon=False, title="Temperature")
axA.text(26, 118, "2-50 ps\nfit window", fontsize=7.2, color=MUT, ha="center", va="top", style="italic")

fig.suptitle("Li mean-squared displacement — comp1 vs comp2 (UMA-s-1p1, seed-averaged)",
             fontsize=11.5, color=INK, y=1.05)
fig.text(0.5, -0.04,
         "comp2 = 3-seed mean (gabia comp2_md); comp1 = db msd_comp1_modelc.  "
         "1000 K nearly identical (~115 $\\AA^2$ @100 ps); comp2 800 K noisier (seed scatter).  "
         "D from 2-50 ps slope -> Arrhenius (see comp2_arrhenius).",
         ha="center", fontsize=7.4, color=MUT)

OUTD = REPO / "docs/figures/comp2"; OUTD.mkdir(parents=True, exist_ok=True)
png = OUTD / "comp2_msd.png"
fig.savefig(png, dpi=300, bbox_inches="tight")
print("->", png)

# --- Origin CSV: common 0-100 ps grid (0.5 ps), comp1 + comp2 interpolated ---
grid = np.arange(0, 100.01, 0.5)
csvp = REPO / "db/properties/comp2_msd_origin.csv"
with open(csvp, "w", newline="") as f:
    wr = csv.writer(f)
    wr.writerow(["t_ps", "comp1_600K", "comp1_800K", "comp1_1000K",
                 "comp2_600K", "comp2_800K", "comp2_1000K"])
    for g in grid:
        row = [f"{g:.2f}"]
        row += [f"{np.interp(g, t1, msd1[T]):.4f}" for T in (600, 800, 1000)]
        row += [f"{np.interp(g, t2, msd2[T]):.4f}" for T in (600, 800, 1000)]
        wr.writerow(row)
print("->", csvp)
print(f"comp2 @100ps: 600K {msd2[600][-1]:.1f} / 800K {msd2[800][-1]:.1f} / 1000K {msd2[1000][-1]:.1f} A^2")
print(f"comp1 @100ps: 600K {msd1[600][-1]:.1f} / 800K {msd1[800][-1]:.1f} / 1000K {msd1[1000][-1]:.1f} A^2")
