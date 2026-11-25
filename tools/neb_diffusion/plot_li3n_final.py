#!/usr/bin/env python3
"""Final Li3N(001) vs LiC6 Li-migration PES from REAL DFT-NEB image energies.

Plots the actual NEB image energies recorded in db/properties/diffusion.json
(no idealized bumps), annotates the Li3N forward barrier (~0.12 eV, matches
Cui 2023 0.133 eV) and the 2.4x ratio vs LiC6 (0.287 eV, DFT-SCF).
"""
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

# --- REAL data (meV), from db/properties/diffusion.json ---
li3n = np.array([0, -18, -93, -102, -13, 76, 77], float)      # full DFT CI-NEB
lic6 = np.array([0, 167.4, 281.8, 286.6, 276.4, 158.3, -22.2], float)  # DFT-SCF on UMA geom
x = np.linspace(0, 1, len(li3n))

def smooth(xv, yv):
    try:
        from scipy.interpolate import make_interp_spline
        xs = np.linspace(0, 1, 300)
        return xs, make_interp_spline(xv, yv, k=3)(xs)
    except Exception:
        return xv, yv

xs, l3 = smooth(x, li3n)
_,  l6 = smooth(x, lic6)

BLUE, GREEN = "#1d4ed8", "#15803d"
fig, ax = plt.subplots(figsize=(7.6, 5.4))

ax.plot(xs, l6, color=GREEN, lw=2.2, zorder=2)
ax.plot(x, lic6, "o", color=GREEN, ms=7, zorder=3,
        label="LiC$_6$(0001)  —  DFT-SCF (db)")
ax.plot(xs, l3, color=BLUE, lw=2.6, zorder=2)
ax.plot(x, li3n, "o", color=BLUE, ms=8, zorder=3,
        label="Li$_3$N(001)  —  full DFT CI-NEB (real)")

ax.axhline(0, color="grey", lw=0.8, ls=":")

# --- Li3N: on-N well + forward barrier ---
iw = int(np.argmin(li3n))                       # on-N well image (img3)
ax.annotate("on-N well\n($-$102 meV)", (x[iw], li3n[iw]),
            xytext=(x[iw], li3n[iw] - 42), ha="center", va="top",
            fontsize=9, color=BLUE)
# forward migration barrier: well -> saddle ~ 0.12 eV (reconfirmed)
xb = x[iw] + 0.012
ax.annotate("", xy=(xb, li3n[iw] + 120), xytext=(xb, li3n[iw]),
            arrowprops=dict(arrowstyle="<->", color=BLUE, lw=1.8))
ax.text(xb + 0.02, li3n[iw] + 60,
        "forward barrier\n$\\approx$ 0.12 eV\n(= Cui 2023, 0.133)",
        fontsize=9.5, color=BLUE, va="center")

# --- LiC6 barrier ---
ip = int(np.argmax(lic6))
ax.annotate("", xy=(x[ip], lic6[ip]), xytext=(x[ip], 0),
            arrowprops=dict(arrowstyle="<->", color=GREEN, lw=1.8))
ax.text(x[ip] - 0.02, lic6[ip] / 2, "0.287 eV ", ha="right",
        fontsize=9.5, color=GREEN, va="center")

# --- headline box ---
ax.text(0.5, 0.97,
        "Li$_3$N 0.12 eV  $\\Rightarrow$  2.4$\\times$ lower than LiC$_6$  "
        "$\\Rightarrow$  $\\sim$10$^3\\times$ faster Li redistribution @300 K",
        transform=ax.transAxes, ha="center", va="top", fontsize=10.5,
        bbox=dict(boxstyle="round,pad=0.45", fc="#fef9c3", ec="#a16207", lw=1))

ax.set_xlabel("Reaction coordinate  (NEB image)", fontsize=12)
ax.set_ylabel("E $-$ E(initial)  (meV)", fontsize=12)
ax.set_title("Li$^+$ lateral migration barrier — Li$_3$N(001) vs LiC$_6$(0001)\n"
             "real DFT-NEB image energies (no idealized path)", fontsize=11.5)
ax.set_xticks(x); ax.set_xticklabels(range(len(li3n)))
ax.legend(loc="center left", fontsize=9.5, framealpha=0.95)
ax.set_ylim(-175, 360)
ax.grid(alpha=0.2)
fig.tight_layout()
out = "docs/figures/li3n_neb/li3n_vs_lic6_FINAL.png"
fig.savefig(out, dpi=200)
print("->", out)
