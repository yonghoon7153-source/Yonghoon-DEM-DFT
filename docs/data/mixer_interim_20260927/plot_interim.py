"""Interim M(t) curves for the layered mixer campaign (descriptive only - not the verdict).

Usage : python3 plot_interim.py <this folder> <out.png>
Input : <ARM>_s<SEED>_c<CELL>.json  (measure_mixing_index.py output, 30 files)
Full revolution bin = 25 frames (rev 0 has 26 incl. t0); shorter bins are partial and not tabulated.
Output: interim_Mt_v09.png  +  summary table on stdout (per full revolution bin, n >= 25 frames)
"""
import glob
import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

SRC = sys.argv[1]
OUT = sys.argv[2]

SURFACE = "#fcfcfb"
INK, INK2, GRID = "#0b0b0b", "#52514e", "#e4e3df"
C_LA, C_LC, C_L0 = "#2a78d6", "#eb6834", "#6f6e69"      # slot 1 blue · slot 2 orange · neutral control
CELLS = [("c8x2", "8x8x2 cells  (decision cell under HOLD fix (b))"),
         ("c12x3", "12x12x3 cells"),
         ("c16x4", "16x16x4 cells  (sec.2 primary grid; floor ratio < 5)")]
SEEDS = ["32452843", "49979687", "67867967"]


def load(arm, seed, cell):
    f = os.path.join(SRC, f"{arm}_s{seed}_{cell}.json")
    d = json.load(open(f))[0]
    rev = np.array([r["rev"] for r in d["rows"]])
    m = np.array([r["M"] for r in d["rows"]])
    return rev, m, d


def smooth(y, k=5):
    """centered moving average over k frames (k=5 = 0.2 rev); ends use what is available"""
    out = np.empty_like(y)
    h = k // 2
    for i in range(len(y)):
        out[i] = y[max(0, i - h):i + h + 1].mean()
    return out


plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10,
                     "axes.edgecolor": GRID, "axes.labelcolor": INK2,
                     "xtick.color": INK2, "ytick.color": INK2})
fig, axes = plt.subplots(1, 3, figsize=(15, 4.9), sharey=True, facecolor=SURFACE)
for ax, (cell, title) in zip(axes, CELLS):
    ax.set_facecolor(SURFACE)
    ratios = []
    last_rev = 0.0
    for arm, col in (("LA", C_LA), ("LC", C_LC)):
        stack = []
        for s in SEEDS:
            rev, m, d = load(arm, s, cell)
            ratios.append(d["S0"] / d["SR"])
            last_rev = max(last_rev, rev[-1])
            ax.plot(rev, smooth(m), color=col, lw=1.0, alpha=0.45, solid_capstyle="round")
            stack.append((rev, m))
        n = min(len(r) for r, _ in stack)
        rev0 = stack[0][0][:n]
        mean = np.mean([smooth(m)[:n] for _, m in stack], axis=0)
        ax.plot(rev0, mean, color=col, lw=2.2, solid_capstyle="round", solid_joinstyle="round",
                label=f"{arm}  ({'uncoated AM, Bo_AM-AM 3.0' if arm == 'LA' else 'coated AM, Bo_AM-AM ~0.001'})  - 3 seeds, thick = mean")
    rev, m, d = load("L0", SEEDS[0], cell)
    ratios.append(d["S0"] / d["SR"])
    last_rev = max(last_rev, rev[-1])
    ax.plot(rev, smooth(m), color=C_L0, lw=1.6, ls=(0, (4, 3)),
            label="L0  (no cohesion anywhere, negative control) - 1 seed")
    ax.axhline(1.0, color=INK2, lw=0.8, alpha=0.6)
    ax.text(7.93, 1.012, "M = 1 (E0 ref.)", color=INK2, fontsize=8, va="bottom", ha="right")
    ax.axvspan(last_rev, 8.0, color="#f0efec", zorder=0)
    ax.axvline(8.0, color=INK, lw=1.0)
    ax.text(7.93, 0.06, "verdict at 8 rev\n(not yet run)", ha="right", va="bottom", fontsize=8.5, color=INK)
    ax.set_xlim(0, 8.15)
    ax.set_ylim(0, 1.12)
    ax.set_xticks(range(0, 9))
    ax.grid(axis="y", color=GRID, lw=0.8)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.set_title(f"{title}\nS0^2 / S_R^2 = {min(ratios):.2f}-{max(ratios):.2f}", fontsize=9.5, color=INK, loc="left")
    ax.set_xlabel("drum revolutions")
axes[0].set_ylabel("Lacey mixing index M  (5-frame moving mean)")
h, l = axes[0].get_legend_handles_labels()
fig.legend(h, l, loc="lower center", ncol=3, frameon=False, fontsize=9, bbox_to_anchor=(0.5, -0.01))
fig.suptitle("Layered mixer campaign - INTERIM M(t) at ~5 of 8 revolutions  (descriptive only; the registered verdict uses 8-rev values)",
             x=0.01, ha="left", fontsize=11.5, color=INK)
fig.tight_layout(rect=(0, 0.07, 1, 0.95))
fig.savefig(OUT, dpi=150, facecolor=SURFACE)
print("wrote", OUT)

# ---- summary table (full revolution bins only) ----
print("\ncell  run  seed  | M per full rev bin (mean +- sd, n frames)")
for cell, _t in CELLS:
    for f in sorted(glob.glob(os.path.join(SRC, f"*_{cell}.json"))):
        d = json.load(open(f))[0]
        br = d["by_rev"]
        full = [k for k in sorted(br, key=int) if br[k]["n"] >= 25]
        part = [k for k in sorted(br, key=int) if br[k]["n"] < 25]
        name = os.path.basename(f)[:-5]
        print(f"{cell:6s} {name:24s} " + "  ".join(f"r{k}:{br[k]['M_mean']:.3f}+-{br[k]['M_sd']:.3f}" for k in full)
              + (f"   [partial r{part[0]}: n={br[part[0]]['n']}]" if part else ""))
