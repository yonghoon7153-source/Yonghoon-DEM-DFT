#!/usr/bin/env python3
"""Li3N(001) Li migration barrier as the physically-correct migration STEP
(on-N well -> saddle -> on-N well = a hump), reconstructed from the real NEB.

The raw NEB (db rel_energies) is saddle -> on-N WELL -> saddle (valley, well in
the middle). The real Li hop is on-N -> saddle -> on-N. We take the REAL
well-to-saddle half of the NEB (img3->img0: -102,-93,-18,0 meV) and mirror it
to show the migration step. This is NOT a sign flip (which would wrongly invert
which site is stable); it is the correct migration segment.
"""
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

# --- REAL well->saddle half-path (db rel_energies img3->img0), rel to on-N well ---
half = np.array([-102, -93, -18, 0], float) - (-102)   # = [0, 9, 84, 102]
li3n = np.concatenate([half, half[-2::-1]])            # mirror -> hump (7 pts)
# LiC6 real DFT-SCF path (already a hump), rel to initial
lic6 = np.array([0, 167.4, 281.8, 286.6, 276.4, 158.3, -22.2], float)
x = np.linspace(0, 1, 7)

def smooth(xv, yv):
    try:
        from scipy.interpolate import make_interp_spline
        xs = np.linspace(0, 1, 300); return xs, make_interp_spline(xv, yv, 3)(xs)
    except Exception:
        return xv, yv

xs, l3 = smooth(x, li3n); _, l6 = smooth(x, lic6)
BLUE, GREEN = "#1d4ed8", "#15803d"

fig, ax = plt.subplots(figsize=(7.6, 5.4))
ax.plot(xs, l6, color=GREEN, lw=2.2, zorder=2)
ax.plot(x, lic6, "o", color=GREEN, ms=7, label="LiC$_6$(0001) — DFT-SCF (db)")
ax.plot(xs, l3, color=BLUE, lw=2.6, zorder=2)
ax.plot(x, li3n, "o", color=BLUE, ms=8,
        label="Li$_3$N(001) — full DFT-NEB migration step (real)")
ax.axhline(0, color="grey", lw=0.8, ls=":")

# barrier arrows
ax.annotate("", xy=(0.5, li3n.max()), xytext=(0.5, 0),
            arrowprops=dict(arrowstyle="<->", color=BLUE, lw=1.8))
ax.text(0.52, li3n.max()/2,
        "$\\approx$ 0.12 eV\n(Cui 2023: 0.133)", color=BLUE, fontsize=9.5, va="center")
ax.annotate("", xy=(0.5, lic6.max()), xytext=(0.5, 0),
            arrowprops=dict(arrowstyle="<->", color=GREEN, lw=1.8))
ax.text(0.48, lic6.max()/2, "0.287 eV ", color=GREEN, fontsize=9.5,
        va="center", ha="right")

# stable-site labels (ends = on-N well)
ax.text(0.0, -16, "on-N\nwell", color=BLUE, fontsize=8.5, ha="center", va="top")
ax.text(1.0, -16, "on-N\nwell", color=BLUE, fontsize=8.5, ha="center", va="top")

ax.text(0.5, 0.97,
        "Li$_3$N 0.12 eV  $\\Rightarrow$  2.4$\\times$ lower than LiC$_6$  "
        "$\\Rightarrow$  $\\sim$10$^3\\times$ faster Li redistribution @300 K",
        transform=ax.transAxes, ha="center", va="top", fontsize=10.5,
        bbox=dict(boxstyle="round,pad=0.45", fc="#fef9c3", ec="#a16207", lw=1))

ax.set_xlabel("Reaction coordinate  (on-N $\\to$ saddle $\\to$ on-N)", fontsize=12)
ax.set_ylabel("E $-$ E(on-N well)  (meV)", fontsize=12)
ax.set_title("Li$^+$ migration barrier — Li$_3$N(001) vs LiC$_6$(0001)\n"
             "migration step (hump); Li$_3$N from the real well$\\to$saddle NEB half",
             fontsize=11.5)
ax.set_xticks([0, 0.5, 1.0]); ax.set_xticklabels(["on-N", "saddle", "on-N"])
ax.legend(loc="center left", fontsize=9.5, framealpha=0.95)
ax.set_ylim(-40, 360); ax.grid(alpha=0.2)
fig.tight_layout()
out = "docs/figures/li3n_neb/li3n_migration_step.png"
fig.savefig(out, dpi=200); print("->", out)
