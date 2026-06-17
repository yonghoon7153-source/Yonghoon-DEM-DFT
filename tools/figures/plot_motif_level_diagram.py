#!/usr/bin/env python3
"""Schematic energy-level diagram: how each structural motif touches the gap.

Positions are taken from the Nd-doped PDOS (E-EF, eV):
  VBM (host free/non-bonding S 3p)   = -0.63   <- gap ceiling
  CBM (pristine PS4 sigma* + Li)     = +0.53   <- gap floor (Nd pulls down)
  O 2p bonding peak                  = -3.91   (deep)
  empty Nd 4f (UHB)                  = +1.1..1.9 (spectator flat)
  filled Nd 4f (LHB)                 = -7.4    (deep)
Writes docs/figures/dos_pdos_smooth/motif_level_diagram.png
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

VBM, CBM = -0.63, 0.53
fig, ax = plt.subplots(figsize=(10.5, 6.4))

# gap band
ax.axhspan(VBM, CBM, color="0.88", zorder=0)
ax.axhline(0, ls="--", color="0.5", lw=0.9)
ax.text(5.92, 0.0, r"$E_F$", va="center", fontsize=9, color="0.4")
ax.text(0.1, (VBM+CBM)/2, "GAP\n1.632 eV", ha="left", va="center",
        fontsize=11, fontweight="bold", color="#333")

# columns: x-center, label, list of (E, color, text, role)
def lvl(x, E, color, txt, w=0.62, lw=3.2, fs=8.2, dy=0.0, ha="center"):
    ax.plot([x-w/2, x+w/2], [E, E], color=color, lw=lw, solid_capstyle="round")
    ax.text(x, E+dy, txt, ha=ha, va="bottom" if dy >= 0 else "top",
            fontsize=fs, color=color)

# 1) HOST that SETS the gap
ax.text(1.0, 6.0, "HOST\n(sets the gap)", ha="center", fontsize=9, fontweight="bold")
lvl(1.0, CBM, "#1f6fb2", "pristine PS$_4$ $\\sigma^*$ + Li  → CBM", dy=0.12)
lvl(1.0, VBM, "#1f6fb2", "free / non-bonding S 3p  → VBM", dy=-0.42)
lvl(1.0, -6.1, "#7aa6c2", "P–S bonding $\\sigma$", dy=0.10, fs=7.6)

# 2) O motifs (PS3O / PS2O2)
ax.text(3.0, 6.0, "O in PS$_4$\n(PS$_3$O, PS$_2$O$_2$)", ha="center", fontsize=9, fontweight="bold")
lvl(3.0, 2.7, "#2ca25f", "P–O $\\sigma^*$ pushed UP\n(out of the way)", dy=0.12, fs=7.8)
lvl(3.0, -3.91, "#2ca25f", "O 2p bonding (deep, inert)", dy=-0.42, fs=7.8)
ax.annotate("", xy=(3.0, 2.7), xytext=(3.0, 0.7),
            arrowprops=dict(arrowstyle="-|>", color="#2ca25f", lw=1.6))
ax.text(2.32, 1.85, "widening\n(weak, local)", color="#2ca25f", fontsize=7.6,
        va="center", ha="right")

# 3) Cl
ax.text(4.4, 6.0, "Cl$^-$", ha="center", fontsize=9, fontweight="bold")
lvl(4.4, -3.4, "#8c6bb1", "Cl 3p (below VBM)", w=0.5, dy=0.10, fs=7.8)

# 4) Nd (the narrowing agent)
ax.text(5.9, 6.0, "Nd$^{3+}$ + Li-vac\n(narrowing agent)", ha="center", fontsize=9, fontweight="bold")
lvl(5.9, 1.5, "#d9534f", "Nd 5d/6s", w=0.5, dy=0.10, fs=7.8)
lvl(5.9, 1.4, "#e8a0a0", "empty Nd 4f (UHB, spectator)", w=0.66, lw=6, dy=-0.5, fs=7.4)
lvl(5.9, -7.4, "#e8a0a0", "filled Nd 4f (LHB, deep)", w=0.5, dy=0.10, fs=7.6)
# arrow: Nd pulls CBM DOWN
ax.annotate("", xy=(1.55, CBM-0.02), xytext=(5.55, 1.35),
            arrowprops=dict(arrowstyle="-|>", color="#d9534f", lw=1.8,
                            connectionstyle="arc3,rad=-0.18"))
ax.text(3.5, -1.45, "Nd pulls CBM DOWN\n→ NARROWING (dominant, −0.55 eV)",
        color="#b52b27", fontsize=8.6, ha="center", fontweight="bold")

ax.set_ylim(-8.2, 6.6)
ax.set_xlim(0.0, 6.6)
ax.set_ylabel(r"$E - E_F$ (eV)")
ax.set_xticks([])
ax.set_title("Which structural motif sets which band edge — Nd$_2$O$_3$-doped LPSCl",
             fontsize=12)
for s in ("top", "right", "bottom"):
    ax.spines[s].set_visible(False)
fig.tight_layout()
out = "docs/figures/dos_pdos_smooth/motif_level_diagram.png"
fig.savefig(out, dpi=160)
print("wrote", out)
