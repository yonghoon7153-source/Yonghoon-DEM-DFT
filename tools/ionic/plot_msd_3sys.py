#!/usr/bin/env python3
"""3-system Li MSD comparison: LPSCl vs LPSCl1.6 vs b2o3, at 600/800/1000 K."""
import csv, numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SRC = "/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/82ea256b-12bc-5a75-994e-7718d79c71ba/scratchpad/msd_LPSCl_LPSCl16_b2o3.csv"

# read (skip the two comment lines)
rows = []
with open(SRC) as f:
    for line in f:
        if line.startswith("#") or line.startswith('"#'):
            continue
        rows.append(line.rstrip("\n"))
hdr = rows[0].split(",")
data = np.array([[float(x) for x in r.split(",")] for r in rows[1:] if r.strip()])
col = {name: i for i, name in enumerate(hdr)}
t = data[:, col["t_ps"]]

SYS = [
    ("LPSCl",    "#6e6e6e", "o", "LPSCl (Li$_6$PS$_5$Cl)"),
    ("LPSCl1.6", "#1f6fb4", "s", "LPSCl1.6 (Cl-rich)"),
    ("b2o3",     "#d1352b", "^", "B$_2$O$_3$-doped"),
]
TEMPS = [600, 800, 1000]

# diffusive-window linear fit (slope = 6D); fit t in [5, 49] ps
def fit_slope(tt, msd, lo=5.0, hi=49.0):
    m = (tt >= lo) & (tt <= hi)
    A = np.vstack([tt[m], np.ones(m.sum())]).T
    slope, intc = np.linalg.lstsq(A, msd[m], rcond=None)[0]
    return slope, intc

fig, axes = plt.subplots(1, 3, figsize=(13.2, 4.3), sharex=True)
for ax, T in zip(axes, TEMPS):
    for key, c, mk, lab in SYS:
        y = data[:, col[f"{key}_{T}K"]]
        ax.plot(t, y, marker=mk, ms=3.2, lw=1.4, color=c, alpha=0.9,
                markevery=3, label=lab, zorder=3)
        s, b = fit_slope(t, y)
        ax.plot(t, s*t + b, ls="--", lw=1.0, color=c, alpha=0.55, zorder=2)
    ax.set_title(f"{T} K", fontsize=12, fontweight="bold")
    ax.set_xlabel("time (ps)", fontsize=11)
    ax.set_xlim(0, 49)
    ax.set_ylim(bottom=0)
    ax.grid(alpha=0.25, lw=0.6)
    ax.tick_params(labelsize=9)

axes[0].set_ylabel("Li MSD  (Å$^2$)", fontsize=11)
axes[0].legend(fontsize=8.5, loc="upper left", framealpha=0.9)

# annotate the D ratio (from the official conductivity CSV) on the 600 K panel
axes[0].text(0.97, 0.05,
             "b2o3 / LPSCl1.6:\nE$_a$ equal (0.22 $\\pm$ 0.03 eV)\n$\\sigma$ $\\approx$ 1.3× (not a barrier effect)",
             transform=axes[0].transAxes, ha="right", va="bottom", fontsize=7.2,
             bbox=dict(boxstyle="round,pad=0.35", fc="#fff5f2", ec="#d1352b", lw=0.8))

fig.suptitle("Li mean-squared displacement  —  LPSCl  vs  LPSCl1.6  vs  B$_2$O$_3$-doped   (MLIP-MD)",
             fontsize=12.5, fontweight="bold", y=1.02)
fig.tight_layout()
OUT = "/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/82ea256b-12bc-5a75-994e-7718d79c71ba/scratchpad/msd_3sys_compare.png"
fig.savefig(OUT, dpi=200, bbox_inches="tight")
print("saved", OUT)

# print the fitted slopes (6D) for a quick sanity read
print("\nfit slope (=6D, A^2/ps) in 5-49 ps window:")
for T in TEMPS:
    line = f"  {T}K: "
    for key, *_ in SYS:
        s, _ = fit_slope(t, data[:, col[f'{key}_{T}K']])
        line += f"{key}={s:.3f}  "
    print(line)
