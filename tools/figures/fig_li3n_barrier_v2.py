#!/usr/bin/env python3
"""fig_li3n_barrier_v2.py — Li3N(001) adsorption/migration 2-panel, 2026-07-17 update.

(a) SLAB absolute adsorption energies (E_ads vs isolated spin-pol Li atom):
      on-N min4 -2.9877 / bridge saddle3 -2.8695 (2-point barrier 0.118 eV)
      + NEW: KISTI drag p0 on-N endpoint -3.0731 eV = 85 meV BELOW min4
      (li3n_adsorption.json + drag p0 E=-2176.45100463 Ry, bare/Li-atom refs unchanged)
(b) Migration profiles: LiC6(0001) real 7-image DFT-SCF profile (0.287 eV,
      diffusion.json lic6_0001_dft_scf) vs Li3N 2-point guide (0.118 eV)
      + converged KISTI 9-point drag points (2/9 as of 07-17 10:00 KST):
      p0=0, p1=+0.184 eV; p2/p3 shown off-scale as unconverged upper bounds.
    Each profile vs its OWN minimum; note that the drag reference p0 sits
    0.085 eV below min4 (the 2-point reference).

Regenerate at 9/9 with the final drag profile (this is the in-progress cut).
Outputs: docs/figures/li3n/li3n_barrier_v2.png + db/properties/li3n_barrier_fig_origin.csv
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

RY = 13.605693
# ---- registered numbers ----
E_BARE, E_LIATOM = -2161.86788071, -14.35726314          # li3n_adsorption.json
E_MIN4, E_SADDLE3 = -2176.44473796, -2176.43605123
E_DRAG_P0, E_DRAG_P1 = -2176.45100463, -2176.43742826    # KISTI 852647, converged
EADS = {k: (v - E_BARE - E_LIATOM) * RY
        for k, v in [("onN_min4", E_MIN4), ("bridge_saddle3", E_SADDLE3), ("onN_dragp0", E_DRAG_P0)]}
BARRIER_2PT = (E_SADDLE3 - E_MIN4) * RY                   # 0.1182
DRAG = {"xi": [0.0, 1 / 8], "eV": [0.0, (E_DRAG_P1 - E_DRAG_P0) * RY]}          # converged
DRAG_RUNNING = {"xi": [2 / 8, 3 / 8], "eV": [0.596, 0.893]}                     # * upper bounds (07-17 10:00)
LIC6_X = np.linspace(0, 1, 7)
LIC6_Y = np.array([0.0, 0.1674, 0.2818, 0.2866, 0.2764, 0.1583, -0.0222])       # diffusion.json
KBT300 = 0.02569

VIOLET, TEAL, ORANGE = ELEM["P"], ELEM["Li"], "#f59e0b"

fig, (ax, bx) = plt.subplots(1, 2, figsize=(13.2, 5.4), constrained_layout=True)

# ================= (a) slab adsorption energies — level diagram =================
labels = ["on-N (top)\nmin4 (2-pt ref)", "bridge (TS)\nsaddle3", "drag p0 = 2N-bridge pocket\n(NOT on-N; coord. 07-17)"]
vals = [EADS["onN_min4"], EADS["bridge_saddle3"], EADS["onN_dragp0"]]
cols = [INK, VIOLET, ORANGE]
xpos = [0, 1, 2]
HW = 0.30
for x, v, c in zip(xpos, vals, cols):
    ax.hlines(v, x - HW, x + HW, color=c, lw=5, zorder=3)
    ax.text(x, v + 0.010, f"{v:.3f} eV", ha="center", va="bottom", fontsize=11.5,
            fontweight="bold", color=c)
# dotted reference extension of min4 level under the two comparisons
ax.hlines(EADS["onN_min4"], xpos[0] + HW, xpos[2] + HW, color=INK, lw=0.9,
          ls=(0, (2, 3)), alpha=0.55, zorder=1)
# 2-point barrier bracket (min4 -> saddle3)
xb = 0.62
ax.annotate("", xy=(xb, EADS["bridge_saddle3"]), xytext=(xb, EADS["onN_min4"]),
            arrowprops=dict(arrowstyle="<->", color=VIOLET, lw=1.5))
ax.text(xb - 0.06, (EADS["onN_min4"] + EADS["bridge_saddle3"]) / 2,
        f"+{BARRIER_2PT:.3f} eV\n2-point barrier", fontsize=10, color=VIOLET,
        va="center", ha="right")
# drag p0 deeper-minimum bracket
xb2 = 2.44
ax.annotate("", xy=(xb2, EADS["onN_dragp0"]), xytext=(xb2, EADS["onN_min4"]),
            arrowprops=dict(arrowstyle="<->", color=ORANGE, lw=1.5))
ax.text(xb2 + 0.06, (EADS["onN_dragp0"] + EADS["onN_min4"]) / 2,
        f"{EADS['onN_dragp0']-EADS['onN_min4']:+.3f} eV\ndeeper site\n(pocket, not on-N)", fontsize=10,
        color="#b45309", va="center", ha="left")
ax.set_xticks(xpos)
ax.set_xticklabels(labels, fontsize=10.5)
ax.set_ylim(-3.16, -2.79)
ax.set_xlim(-0.75, 3.15)
apply_axes(ax, ylabel="$E_{\\mathrm{ads}}$ vs isolated Li atom (eV)",
           title="(a) Li adatom adsorption on Li$_3$N(001) — slab DFT values")
ax.text(0.5, 0.022, "$E_{\\mathrm{ads}}$ = E(slab+ad) $-$ E(bare slab) $-$ E(Li atom);  PBE USPP 60/480, k221\n"
        "all sites $\\gg$ bulk-Li reference (lit. ~$-$1.6 eV) → Li wets Li$_3$N(001)",
        transform=ax.transAxes, fontsize=8.8, color=MUT, va="bottom", ha="center")

# ================= (b) migration profiles =================
# LiC6 real 7-image profile
bx.plot(LIC6_X, LIC6_Y, "-o", color=TEAL, lw=2.4, ms=5, zorder=3,
        label="LiC$_6$(0001) DFT-SCF profile, $\\Delta E$ = 0.287 eV")
# Li3N 2-point guide (sin^2 scaled)
xg = np.linspace(0, 1, 200)
bx.plot(xg, BARRIER_2PT * np.sin(np.pi * xg) ** 2, "--", color=VIOLET, lw=2.0, zorder=2,
        label=f"Li$_3$N(001) 2-point estimate, $\\Delta E$ = {BARRIER_2PT:.3f} eV (guide)")
bx.plot([0.5], [BARRIER_2PT], "D", color=VIOLET, ms=8, zorder=4)
bx.text(0.5, BARRIER_2PT + 0.016, "TS (saddle3)", ha="center", fontsize=9.5, color=VIOLET)
# KISTI drag — converged points
bx.plot(DRAG["xi"], DRAG["eV"], "o", color="#4c1d95", ms=9, zorder=5,
        label="Li$_3$N(001) DFT drag (pocket path), 2/9")
for x, y, t in zip(DRAG["xi"], DRAG["eV"], ["p0", "p1"]):
    bx.text(x + 0.015, y + 0.012, f"{t}  {y:+.3f}" if y else f"{t} (ref)",
            fontsize=9.5, color="#4c1d95", fontweight="bold")
# running points: off-scale arrows at top edge
YTOP = 0.46
for x, y, t in zip(DRAG_RUNNING["xi"], DRAG_RUNNING["eV"], ["p2", "p3"]):
    bx.annotate("", xy=(x, YTOP - 0.055), xytext=(x, YTOP - 0.005),
                arrowprops=dict(arrowstyle="-|>", color=MUT, lw=1.3))
    bx.text(x, YTOP - 0.002, f"{t} +{y:.2f}*", ha="center", va="bottom",
            fontsize=8.8, color=MUT)
bx.text(0.315, YTOP - 0.095, "*still relaxing → upper bounds,\n  will come down",
        fontsize=8.6, color=MUT, ha="center")
bx.axhline(KBT300, color="#b91c1c", ls=":", lw=1.2)
bx.text(0.995, KBT300 + 0.008, "$k_\\mathrm{B}T$ (300 K)", ha="right", fontsize=9, color="#b91c1c")
bx.set_xlim(-0.03, 1.03)
bx.set_ylim(-0.06, YTOP)
bx.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
apply_axes(bx, xlabel="reaction coordinate $\\xi$ (drag point index / 8)",
           ylabel="Relative energy (eV)",
           title="(b) Li adatom migration — DFT profiles + drag points")
bx.text(0.0, -0.048, "p0 (pocket)", fontsize=9.5, color=MUT)
bx.text(1.0, -0.048, "p8", fontsize=9.5, color=MUT, ha="right")
bx.text(0.13, 0.015, "profiles vs own minima;  drag p0 = 2N-bridge pocket, 0.085 eV below on-N min4",
        transform=bx.transAxes, fontsize=8.6, color=MUT, va="bottom", ha="left")
bx.legend(loc="upper right", fontsize=9, frameon=False)

OUTD = REPO / "docs/figures/li3n"
OUTD.mkdir(parents=True, exist_ok=True)
png = OUTD / "li3n_barrier_v2.png"
fig.savefig(png, dpi=300)
print("->", png)

# Origin-ready csv
import csv
csvp = REPO / "db/properties/li3n_barrier_fig_origin.csv"
with open(csvp, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["series", "x_xi_or_site", "energy_eV", "status"])
    for lbl, v in zip(["onN_min4", "bridge_saddle3", "dragp0_2Nbridge_pocket"], vals):
        w.writerow(["Eads_slab_abs", lbl, f"{v:.4f}", "converged"])
    for x, y in zip(LIC6_X, LIC6_Y):
        w.writerow(["LiC6_dft_scf_profile", f"{x:.4f}", f"{y:.4f}", "converged"])
    for x, y in zip(DRAG["xi"], DRAG["eV"]):
        w.writerow(["Li3N_drag_dft", f"{x:.4f}", f"{y:.4f}", "converged"])
    for x, y in zip(DRAG_RUNNING["xi"], DRAG_RUNNING["eV"]):
        w.writerow(["Li3N_drag_dft", f"{x:.4f}", f"{y:.4f}", "RUNNING_upper_bound_2026-07-17"])
    w.writerow(["Li3N_2point_guide", "0.5", f"{BARRIER_2PT:.4f}", "TS_saddle3_vs_min4"])
print("->", csvp)
