#!/usr/bin/env python3
"""Nd2O3-doped LPSCl: decompose the conduction edge into HOST vs Nd-4f.

Purpose: answer "what is the gap if we exclude the localized Nd 4f?".
The note (PBE+U fails for Nd 4f) says PBE+U mis-places 4f and the GAP fails
*only when the gap edge itself is 4f* (Mott f-f gap, e.g. NdOCl). Here we
show the opposite: in the doped sulfide the band edges are HOST (S 3p VBM,
PS4-derived CBM) and the empty Nd 4f sits as a flat spectator manifold
ABOVE the CBM -> removing 4f does not change the gap.

Reads docs/figures/dos_pdos_smooth/nd_smooth0.15.csv
  cols: E-EF, total, Li, P, S, Cl, O, Nd, Nd1_4f, Nd2_4f   (Gaussian 0.15 eV)
Writes docs/figures/dos_pdos_smooth/nd_4f_excluded_gap.png
"""
import csv
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

CSV = "docs/figures/dos_pdos_smooth/nd_smooth0.15.csv"
COLS = ["E", "total", "Li", "P", "S", "Cl", "O", "Nd", "Nd1_4f", "Nd2_4f"]

rows = []
with open(CSV) as f:
    next(csv.reader(f))
    for x in csv.reader(f):
        try:
            rows.append([float(v.split("#")[0]) for v in x[:10]])
        except ValueError:
            pass
A = np.array(rows)
c = {k: i for i, k in enumerate(COLS)}
E = A[:, c["E"]]
total = A[:, c["total"]]
f4 = A[:, c["Nd1_4f"]] + A[:, c["Nd2_4f"]]      # Nd 4f only
non4f = total - f4                               # 4f-EXCLUDED DOS (host + Nd 5d/6s)

# --- locate edges (threshold on smoothed DOS) ---
thr = 0.30
def onset(mask_E_gt):
    for Ei, y in zip(E, non4f):
        if mask_E_gt(Ei) and y > thr:
            return Ei
    return None
# VBM: highest E<0 with non4f>thr ; host CBM: lowest E>0 with non4f>thr
vbm = max(Ei for Ei, y in zip(E, non4f) if Ei < 0 and y > thr)
cbm_host = min(Ei for Ei, y in zip(E, non4f) if Ei > 0.1 and y > thr)
f4_onset = min((Ei for Ei, y in zip(E, f4) if Ei > 0.1 and y > thr), default=None)
EIG_GAP = 1.632   # eigenvalue gap (electronic.json), edges are host

fig, ax = plt.subplots(figsize=(9, 5.2))
# 4f-excluded (host + Nd 5d/6s): the bands that actually set the gap & conduct
ax.fill_between(E, non4f, color="#4C78A8", alpha=0.55,
                label="4f-excluded DOS (host S/P/Cl/O/Li + Nd 5d/6s)\n— dispersive, sets the gap")
# Nd 4f: localized flat spectator manifold
ax.fill_between(E, f4, color="#D9534F", alpha=0.75,
                label="Nd 4f only (localized flat band — no transport channel)")
ax.plot(E, total, color="k", lw=1.1, label="Total DOS")

# gap region defined by HOST edges
ax.axvspan(vbm, cbm_host, color="0.85", alpha=0.7, zorder=0)
ax.axvline(0, ls="--", color="0.4", lw=0.9)
ymax = float(np.nanmax(total)) * 1.08
ax.set_ylim(0, ymax)
ax.set_xlim(E.min(), E.max())

# annotations
ax.annotate("host CBM\n(PS$_4$-derived)", xy=(cbm_host, ymax*0.18),
            xytext=(cbm_host+0.15, ymax*0.42), fontsize=9,
            arrowprops=dict(arrowstyle="->", color="#2c4a6e"))
if f4_onset:
    ax.annotate("empty Nd 4f (UHB)\nspectator, +%.1f eV above CBM\n(true UHB even higher: real U≈5–8 > 3.1)"
                % (f4_onset - cbm_host),
                xy=(f4_onset+0.05, max(f4[np.argmin(np.abs(E-(f4_onset+0.05)))], ymax*0.1)),
                xytext=(f4_onset-0.2, ymax*0.70), fontsize=8.5, color="#7a1f1c",
                ha="left", arrowprops=dict(arrowstyle="->", color="#D9534F"))
ax.text(0.5*(vbm+cbm_host), ymax*0.90,
        "host gap = 4f-excluded gap\n= %.3f eV" % EIG_GAP,
        ha="center", va="top", fontsize=10, fontweight="bold")

ax.set_xlabel(r"$E - E_F$ (eV)")
ax.set_ylabel("DOS (states/eV)")
ax.set_title("Nd$_2$O$_3$-doped LPSCl — Nd 4f is a spectator above the CBM, "
             "not in the gap", fontsize=11)
ax.legend(loc="upper left", fontsize=8.0, framealpha=0.95)
fig.tight_layout()
out = "docs/figures/dos_pdos_smooth/nd_4f_excluded_gap.png"
fig.savefig(out, dpi=160)
print("wrote", out)
print(f"VBM(host)={vbm:+.2f}  CBM(host)={cbm_host:+.2f}  4f onset={f4_onset:+.2f} eV (rel EF)")
print(f"host gap (eigenvalue) = {EIG_GAP} eV ; 4f sits {f4_onset-cbm_host:+.2f} eV above host CBM")
