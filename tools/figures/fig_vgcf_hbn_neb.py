#!/usr/bin/env python3
"""fig_vgcf_hbn_neb.py — Li migration CI-NEB in the h-BN@VGCF system, 2026-07-27.

Layout follows the conference-slide grammar the user picked as reference
(MEP with open image markers + interpolated curve | forward/backward barrier bars),
re-drawn in house style (white ground, INK/MUT, no top/right spines, English labels).

Data: QE 7.4.1-GPU neb.x, 7 images, CI_scheme='auto', path_thr=0.05 eV/A,
hollow->hollow hop +a1 = 2.46 A, endpoints pre-relaxed (fixed in NEB).
Run on esp-Z590, harvested 2026-07-27 from ~/work/vgcf_hbn/neb/<case>/{neb.out,*.dat,*.int}.
  <case>.dat = 7 NEB images (reaction coord, E-E_first in eV)
  <case>.int = neb.x cubic interpolation (energies + tangential forces), 0.02 grid

  Li_on_hbn           Ea-> 0.007357 / <- -0.000000 eV  (11 iter, converged)
  Li_on_graphene      Ea-> 0.272950 / <-  0.272018 eV  (14 iter, converged)
  Li_in_gallery 1L1L  Ea-> 0.356724 / <-  0.349193 eV  (29 iter, converged)
  Li_in_gallery 2L2L  Ea-> 0.147314 / <-  0.145777 eV  (52 iter, converged)

Layer-count caveat (see kb note): the 1L1L->2L2L barrier shift is -209 meV, four
times the 52 meV spread the 2x2 binding matrix showed for E_bind. The barrier is
NOT layer-insensitive, so the 1L NEB justification in
db/properties/vgcf_hbn_binding_matrix.json ("headline") no longer holds.
2L2L is quoted as the representative value, matching that file's
representative_for_paper = gallery_2L2L (E_bind -1.626 eV).

Outputs: docs/figures/vgcf_hbn/vgcf_hbn_neb.png
         db/properties/vgcf_hbn_neb_origin.csv         (interpolated MEP, wide)
         db/properties/vgcf_hbn_neb_images_origin.csv  (7 image points per case)
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))
from tools.figures.house_style import INK, MUT, ELEM, apply_axes  # noqa: E402

KBT300 = 25.69  # meV

# ---------------- harvested data (eV -> plotted in meV) ----------------
# 7-image points: (reaction coordinate, E - E_first) in eV
DAT = {
    "hbn": [(0.0000000000, 0.0000000000), (0.1922545407, -0.0009433710),
            (0.3880476626, -0.0011051079), (0.5734823139, 0.0016057380),
            (0.7299782542, 0.0050840166), (0.8668564069, 0.0070414474),
            (1.0000000000, 0.0073573825)],
    "graphene": [(0.0000000000, 0.0000000000), (0.1946143614, 0.1177238834),
                 (0.3553932821, 0.2315958189), (0.4998587133, 0.2729499278),
                 (0.6445009937, 0.2316213588), (0.8053800471, 0.1181357541),
                 (1.0000000000, 0.0009316009)],
    "g1L1L": [(0.0000000000, 0.0000000000), (0.2000130688, 0.0830632876),
              (0.3660064920, 0.2658803222), (0.5072470625, 0.3567241391),
              (0.6452948019, 0.2703978978), (0.8061565098, 0.0947758819),
              (1.0000000000, 0.0075308672)],
    "g2L2L": [(0.0000000000, 0.0000000000), (0.1895986772, 0.0762871102),
              (0.3446900038, 0.1439176392), (0.4885989580, 0.1316287043),
              (0.6335860707, 0.1473143100), (0.7984897818, 0.0765496229),
              (1.0000000000, 0.0015373127)],
}

# neb.x cubic interpolation, shared xi grid 0.00 -> 1.00 step 0.02 (eV)
XI = np.round(np.arange(0.0, 1.0001, 0.02), 2)
INT = {
    "hbn": [0.0000000000, -0.0000215228, -0.0000808367, -0.0001700603, -0.0002813119,
            -0.0004067099, -0.0005383729, -0.0006684191, -0.0007889672, -0.0008921354,
            -0.0009806398, -0.0011408203, -0.0013621803, -0.0016057504, -0.0018325608,
            -0.0020036420, -0.0020800244, -0.0020227383, -0.0017928142, -0.0013512823,
            -0.0007365801, -0.0002356354, 0.0001441723, 0.0004302436, 0.0006499791,
            0.0008307793, 0.0010000450, 0.0011851767, 0.0014135750, 0.0017133725,
            0.0021053878, 0.0025680984, 0.0030725842, 0.0035899253, 0.0040912017,
            0.0045474933, 0.0049298803, 0.0052254483, 0.0055110616, 0.0057996137,
            0.0060892542, 0.0063781324, 0.0066643979, 0.0069461999, 0.0071977773,
            0.0073490798, 0.0074176907, 0.0074282182, 0.0074052705, 0.0073734558,
            0.0073573825],
    "graphene": [0.0000000000, 0.0017511586, 0.0067719563, 0.0147133758, 0.0252263999,
                 0.0379620113, 0.0525711928, 0.0687049271, 0.0860141971, 0.1041499854,
                 0.1227103911, 0.1404385311, 0.1569639168, 0.1723414127, 0.1866258832,
                 0.1998721929, 0.2121352061, 0.2234697873, 0.2339282986, 0.2434525272,
                 0.2518936820, 0.2591116638, 0.2649663733, 0.2693177112, 0.2720255784,
                 0.2729498756, 0.2719992247, 0.2692698939, 0.2649033074, 0.2590408896,
                 0.2518240648, 0.2433942574, 0.2338928917, 0.2234678876, 0.2121722598,
                 0.1999534765, 0.1867568025, 0.1725275025, 0.1572108412, 0.1407520832,
                 0.1230964934, 0.1046135995, 0.0865555594, 0.0693220783, 0.0532602544,
                 0.0387171855, 0.0260399699, 0.0155757056, 0.0076714906, 0.0026744230,
                 0.0009316009],
    "g1L1L": [0.0000000000, 0.0005169544, 0.0022071718, 0.0052796838, 0.0099435217,
              0.0164077171, 0.0248813014, 0.0355733061, 0.0486927626, 0.0644487023,
              0.0830501568, 0.1037669359, 0.1255141105, 0.1479719432, 0.1708206969,
              0.1937406348, 0.2164120196, 0.2385151145, 0.2597301824, 0.2799058044,
              0.2990440131, 0.3165153703, 0.3316542267, 0.3437949327, 0.3522718389,
              0.3564192958, 0.3556519687, 0.3501871635, 0.3406853172, 0.3278100193,
              0.3122248592, 0.2945934265, 0.2755793105, 0.2555712172, 0.2343693743,
              0.2122926687, 0.1896919720, 0.1669181557, 0.1443220915, 0.1222546509,
              0.1010667053, 0.0814269428, 0.0643967599, 0.0499042011, 0.0378066606,
              0.0279615323, 0.0202262104, 0.0144580888, 0.0105145617, 0.0082530232,
              0.0075308672],
    "g2L2L": [0.0000000000, 0.0006418914, 0.0026651973, 0.0062163650, 0.0114418419,
              0.0184880753, 0.0275015125, 0.0386286010, 0.0520157881, 0.0678095212,
              0.0854467422, 0.1011055863, 0.1142394776, 0.1249025235, 0.1331488318,
              0.1390325101, 0.1426076662, 0.1439284075, 0.1433413169, 0.1417409837,
              0.1395182820, 0.1370395006, 0.1346709284, 0.1327788542, 0.1317295669,
              0.1318919018, 0.1333331460, 0.1356881370, 0.1385669663, 0.1415797250,
              0.1443365046, 0.1464473961, 0.1474751830, 0.1464796886, 0.1432084634,
              0.1376504587, 0.1297946260, 0.1196299164, 0.1071452813, 0.0923296721,
              0.0751866413, 0.0585883908, 0.0445565324, 0.0328981124, 0.0234201766,
              0.0159297713, 0.0102339424, 0.0061397360, 0.0034541982, 0.0019843751,
              0.0015373127],
}

# activation energies from neb.out (eV)
EA = {"hbn": (0.007357, -0.000000), "graphene": (0.272950, 0.272018),
      "g1L1L": (0.356724, 0.349193), "g2L2L": (0.147314, 0.145777)}

ORDER = ["hbn", "graphene", "g1L1L", "g2L2L"]
LABEL = {"hbn": "Li on h-BN (1L)", "graphene": "Li on graphene (1L)",
         "g1L1L": "Li in gallery  1L|1L", "g2L2L": "Li in gallery  2L|2L"}
COLOR = {"hbn": ELEM["B"], "graphene": INK, "g1L1L": ELEM["S"], "g2L2L": ELEM["Li"]}
LIT = {"hbn": (100.0, "Shi17"), "graphene": (300.0, "lit.")}   # full refs in the caption

fig, (ax, bx) = plt.subplots(1, 2, figsize=(13.4, 5.4),
                             gridspec_kw={"width_ratios": [1.45, 1.0]},
                             constrained_layout=True)

# ================= (a) minimum-energy paths =================
for k in ORDER:
    c, lw = COLOR[k], 2.6 if k == "g2L2L" else 1.9
    ax.plot(XI, np.array(INT[k]) * 1000.0, color=c, lw=lw, zorder=3,
            label=f"{LABEL[k]}   $E_\\mathrm{{a}}$ = {EA[k][0]*1000:.0f} meV")
    xd, yd = zip(*DAT[k])
    ax.plot(xd, np.array(yd) * 1000.0, "o", ms=6.4, mfc="white", mec=c, mew=1.7, zorder=4)

# 2L2L plateau callout: two saddles 3.4 meV apart, sub-kT dip between them
ax.annotate("flat-topped saddle\n(2 maxima 3 meV apart,\ndip 16 meV < $k_\\mathrm{B}T_{300}$)",
            xy=(0.49, 133.0), xytext=(0.215, 215.0), fontsize=9.5, color=ELEM["Li"],
            ha="center", va="center",
            arrowprops=dict(arrowstyle="->", color=ELEM["Li"], lw=1.2, alpha=0.85,
                            connectionstyle="arc3,rad=-0.15"))
ax.annotate("sharp single saddle", xy=(0.50, 356.4), xytext=(0.72, 330.0),
            fontsize=9.5, color=ELEM["S"], ha="left", va="center",
            arrowprops=dict(arrowstyle="->", color=ELEM["S"], lw=1.2, alpha=0.85))
ax.text(0.50, 16.0, "h-BN surface: $E_\\mathrm{a}$ < 10 meV (below numerical resolution)",
        fontsize=9.5, color=ELEM["B"], ha="center", va="bottom")

ax.axhline(0.0, color=MUT, lw=0.8, ls=(0, (2, 3)), alpha=0.6, zorder=1)
apply_axes(ax, xlabel="Diffusion coordinate  (hollow $\\rightarrow$ hollow, 2.46 $\\mathrm{\\AA}$)",
           ylabel="Energy  (meV)", title="(a)  Li migration paths — CI-NEB, 7 images")
ax.set_xlim(-0.02, 1.02)
ax.set_ylim(-25, 395)
ax.legend(frameon=False, fontsize=10.2, loc="upper left", labelcolor=INK)

# ================= (b) forward / backward barriers =================
xb = np.arange(len(ORDER))
W = 0.36
for i, k in enumerate(ORDER):
    ef, eb = EA[k][0] * 1000.0, EA[k][1] * 1000.0
    c = COLOR[k]
    bx.bar(xb[i] - W / 2, ef, W, color=c, alpha=0.92, zorder=3)
    bx.bar(xb[i] + W / 2, eb, W, color=c, alpha=0.38, edgecolor=c, lw=1.3, zorder=3)
    # graphene label is nudged clear of its literature marker at 300 meV
    dy = 46 if k == "graphene" else 26
    bx.text(xb[i] - W / 2, ef + dy, f"{ef:.2f}", ha="center", va="bottom",
            fontsize=10, fontweight="bold", color=c)
    bx.text(xb[i] + W / 2, eb + 7, f"{eb:.2f}", ha="center", va="bottom",
            fontsize=10, color=c, alpha=0.85)
    if k in LIT:
        v, tag = LIT[k]
        bx.hlines(v, xb[i] - 0.44, xb[i] + 0.10, color=MUT, lw=1.5, ls="--", zorder=4)
        bx.text(xb[i] + 0.13, v, tag, fontsize=8.8, color=MUT, ha="left", va="center")

bx.axhline(KBT300, color=MUT, lw=0.9, ls=(0, (1, 2)), alpha=0.8, zorder=1)
bx.text(3.82, KBT300 + 6, "$k_\\mathrm{B}T$ (300 K)", fontsize=8.8, color=MUT,
        va="bottom", ha="right")
apply_axes(bx, ylabel="Activation barrier  (meV)",
           title="(b)  Forward (solid) / backward (open)")
bx.set_xticks(xb)
bx.set_xticklabels(["Li on\nh-BN", "Li on\ngraphene", "gallery\n1L|1L", "gallery\n2L|2L"],
                   fontsize=10.2, color=INK)
bx.set_ylim(0, 470)
bx.set_xlim(-0.62, 3.86)

# layer-sensitivity callout between the two gallery groups
bx.annotate("", xy=(2.0, 420), xytext=(3.0, 420),
            arrowprops=dict(arrowstyle="<->", color=INK, lw=1.4))
bx.text(2.5, 428, "$-$209 meV with layer count", ha="center", va="bottom",
        fontsize=9.8, fontweight="bold", color=INK)

OUT = REPO / "docs/figures/vgcf_hbn"
OUT.mkdir(parents=True, exist_ok=True)
fig.savefig(OUT / "vgcf_hbn_neb.png", dpi=300, bbox_inches="tight", facecolor="white")
print(f"[fig] {OUT / 'vgcf_hbn_neb.png'}")

# ================= Origin-ready CSVs =================
PROP = REPO / "db/properties"
cols = ["Li_on_hBN_1L", "Li_on_graphene_1L", "Li_in_gallery_1L1L", "Li_in_gallery_2L2L"]
with open(PROP / "vgcf_hbn_neb_origin.csv", "w") as f:
    f.write("# h-BN@VGCF Li migration MEP - QE neb.x cubic interpolation, 7-image CI-NEB, "
            "hollow->hollow 2.46 A. Energies in meV relative to the first image.\n")
    f.write("reaction_coordinate," + ",".join(f"E_meV_{c}" for c in cols) + "\n")
    for j, x in enumerate(XI):
        f.write(f"{x:.2f}," + ",".join(f"{INT[k][j]*1000:.4f}" for k in ORDER) + "\n")
print(f"[csv] {PROP / 'vgcf_hbn_neb_origin.csv'}")

with open(PROP / "vgcf_hbn_neb_images_origin.csv", "w") as f:
    f.write("# h-BN@VGCF Li migration - the 7 CI-NEB image points per case (neb.x .dat). "
            "Energies in meV relative to the first image.\n")
    f.write(",".join(f"xi_{c},E_meV_{c}" for c in cols) + "\n")
    for i in range(7):
        f.write(",".join(f"{DAT[k][i][0]:.6f},{DAT[k][i][1]*1000:.4f}" for k in ORDER) + "\n")
print(f"[csv] {PROP / 'vgcf_hbn_neb_images_origin.csv'}")
