#!/usr/bin/env python3
"""Anode-interface decomposition: B2O3-doped vs undoped LPSCl1.6 (MLIP-MD, 50 ps).
Single-seed preliminary; error bars come from the 3-seed campaign."""
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

# single-seed initial -> final (from analyze_interface_decomp.py)
M = dict(PS_i=3.80, PS_f=2.00, PLi_i=0.80, PLi_f=4.20, SLi_i=3.36, SLi_f=5.18, pen_i=28, pen_f=38)  # modelc
B = dict(PS_i=3.25, PS_f=3.00, PLi_i=1.00, PLi_f=1.62, SLi_i=3.73, SLi_f=4.10, pen_i=60, pen_f=64)  # b2o3
# decomposition amounts (bigger = worse)
met = [
    ("PS$_4$ break\n(P–S loss %)",  (M["PS_i"]-M["PS_f"])/M["PS_i"]*100, (B["PS_i"]-B["PS_f"])/B["PS_i"]*100),
    ("Li$_3$P form\n($\\Delta$P–Li)", M["PLi_f"]-M["PLi_i"],              B["PLi_f"]-B["PLi_i"]),
    ("Li$_2$S form\n($\\Delta$S–Li)", M["SLi_f"]-M["SLi_i"],              B["SLi_f"]-B["SLi_i"]),
    ("Li ingress\n($\\Delta$atoms)",  M["pen_f"]-M["pen_i"],              B["pen_f"]-B["pen_i"]),
]
labels = [m[0] for m in met]
mval = np.array([m[1] for m in met]); bval = np.array([m[2] for m in met])
frac = bval / mval * 100                 # b2o3 as % of modelc
fold = mval / bval

fig, (axL, axR) = plt.subplots(1, 2, figsize=(12.4, 4.7), gridspec_kw={"width_ratios": [1.15, 1]})

# ---- Left: the chemistry (coordination before -> after) ----
grp = [("P–S", M["PS_i"], M["PS_f"], B["PS_i"], B["PS_f"], "breaks"),
       ("P–Li", M["PLi_i"], M["PLi_f"], B["PLi_i"], B["PLi_f"], "Li$_3$P"),
       ("S–Li", M["SLi_i"], M["SLi_f"], B["SLi_i"], B["SLi_f"], "Li$_2$S")]
x = np.arange(len(grp)); w = 0.2
for i, (nm, mi, mf, bi, bf, tag) in enumerate(grp):
    axL.plot([x[i]-1.5*w, x[i]-0.5*w], [mi, mf], "-", color="#c0392b", lw=1, alpha=0.5, zorder=1)
    axL.plot([x[i]+0.5*w, x[i]+1.5*w], [bi, bf], "-", color="#159a8a", lw=1, alpha=0.5, zorder=1)
    axL.scatter([x[i]-1.5*w], [mi], s=45, facecolor="white", edgecolor="#c0392b", lw=1.6, zorder=3)
    axL.scatter([x[i]-0.5*w], [mf], s=55, color="#c0392b", zorder=3)
    axL.scatter([x[i]+0.5*w], [bi], s=45, facecolor="white", edgecolor="#159a8a", lw=1.6, zorder=3)
    axL.scatter([x[i]+1.5*w], [bf], s=55, color="#159a8a", zorder=3)
axL.set_xticks(x); axL.set_xticklabels([g[0] for g in grp], fontsize=11)
axL.set_ylabel("coordination number", fontsize=11)
axL.set_title("Interface chemistry:  initial $\\to$ final (50 ps)", fontsize=11, fontweight="bold")
axL.grid(axis="y", alpha=0.25, lw=0.6)
from matplotlib.lines import Line2D
axL.legend(handles=[
    Line2D([],[],marker='o',ls='',mfc='white',mec='#c0392b',mew=1.6,label='undoped init'),
    Line2D([],[],marker='o',ls='',color='#c0392b',label='undoped final'),
    Line2D([],[],marker='o',ls='',mfc='white',mec='#159a8a',mew=1.6,label='B$_2$O$_3$ init'),
    Line2D([],[],marker='o',ls='',color='#159a8a',label='B$_2$O$_3$ final')], fontsize=8, loc="upper left", ncol=2)
axL.annotate("P–S collapses,\nP/S grab Li\n(decomposition)", xy=(0.05,4.3), xytext=(0.05,4.3),
             fontsize=8, color="#c0392b", ha="left")

# ---- Right: normalized suppression (b2o3 as % of undoped) ----
xb = np.arange(len(labels))
axR.bar(xb-0.21, [100]*len(labels), 0.42, color="#c0392b", alpha=0.85, label="undoped LPSCl1.6", edgecolor="k", lw=0.4)
bars = axR.bar(xb+0.21, frac, 0.42, color="#159a8a", alpha=0.9, label="B$_2$O$_3$-doped", edgecolor="k", lw=0.4)
for i, (fr, fo) in enumerate(zip(frac, fold)):
    axR.text(xb[i]+0.21, fr+3, f"{fr:.0f}%\n({fo:.1f}×↓)", ha="center", va="bottom", fontsize=8.2, color="#0e7a6d", fontweight="bold")
    axR.text(xb[i]-0.21, 101, "100%", ha="center", va="bottom", fontsize=7.5, color="#8a2a20")
axR.set_xticks(xb); axR.set_xticklabels(labels, fontsize=8.6)
axR.set_ylabel("decomposition, % of undoped", fontsize=11)
axR.set_ylim(0, 125); axR.set_title("B$_2$O$_3$ suppresses every channel", fontsize=11, fontweight="bold")
axR.legend(fontsize=9, loc="upper right"); axR.grid(axis="y", alpha=0.25, lw=0.6)

fig.suptitle("B$_2$O$_3$ protects the Li-metal anode interface  —  ~2.5–6× less decomposition across all channels  "
             "(UMA-MD, 50 ps, 600 K; single-seed, 3-seed campaign in progress)",
             fontsize=11, fontweight="bold", y=1.01)
fig.tight_layout()
OUT="/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/82ea256b-12bc-5a75-994e-7718d79c71ba/scratchpad/interface_decomp_b2o3_vs_undoped.png"
fig.savefig(OUT, dpi=200, bbox_inches="tight"); print("saved", OUT)
print("fractions (b2o3 % of undoped):", np.round(frac,0), " fold:", np.round(fold,1))
