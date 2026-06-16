#!/usr/bin/env python3
"""Nd2O3-doped modelc DOS/PDOS -> Gaussian-smoothed CSV + 2-panel figure.

Reads docs/figures/nd_dos/nd_pdos_compact.csv (k441 DFT+U, nspin2 AFM data:
columns E-EF, total, Li, P, S, Cl, O, Nd, Nd1_4f, Nd2_4f), applies a Gaussian
broadening (post-hoc convolution) for a smooth publication curve, writes the
smoothed CSV, and renders a 2-panel DOS/PDOS figure.

Gap annotation uses the EIGENVALUE gap (k661, from db modelc_nd_doped.json),
while the curve itself is the k441 DOS — both are labelled on the figure.
"""
import numpy as np
from scipy.ndimage import gaussian_filter1d
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

CSV      = "docs/figures/nd_dos/nd_pdos_compact.csv"
OUT_CSV  = "docs/figures/nd_dos/nd_dos_smoothed.csv"
OUT_PNG  = "docs/figures/nd_dos/nd_dos_pdos_v2.png"
SIGMA_EV = 0.10           # Gaussian broadening (eV) -- "더 gaussian"
GAP_EIG  = 1.632          # eigenvalue gap (k661, db); curve is k441 DOS
# eigenvalue band edges (k661, db: VBM 3.081, CBM 4.712, EF 3.879) -> relative to EF:
VBM_EIG, CBM_EIG = 3.081 - 3.879, 4.712 - 3.879   # = -0.798, +0.833 -> width 1.632

raw = np.loadtxt(CSV, delimiter=",", skiprows=1)
E = raw[:, 0]
names = ["total", "Li", "P", "S", "Cl", "O", "Nd", "Nd1_4f", "Nd2_4f"]
D = {n: raw[:, i + 1] for i, n in enumerate(names)}

dE = float(np.median(np.diff(E)))
sig = max(1.0, SIGMA_EV / dE)
S = {n: gaussian_filter1d(D[n], sig) for n in names}

# gap edges from RAW total (smoothing blurs the gap, so detect on raw)
thr = 0.03 * D["total"].max()
occ = E[(E < 0) & (D["total"] > thr)]
unocc = E[(E > 0) & (D["total"] > thr)]
vbm, cbm = occ.max(), unocc.min()

with open(OUT_CSV, "w") as f:
    f.write("E-EF," + ",".join(names) + f"   # Gaussian {SIGMA_EV} eV smoothed\n")
    for i in range(len(E)):
        f.write(f"{E[i]:.4f}," + ",".join(f"{S[n][i]:.5g}" for n in names) + "\n")

col = {"S": "tab:green", "P": "tab:orange", "Cl": "tab:purple",
       "O": "tab:red", "Li": "tab:blue", "Nd": "tab:cyan"}
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6), sharex=True,
                               gridspec_kw={"height_ratios": [2, 1]})
# --- top: total + element fills ---
ax1.plot(E, S["total"], color="black", lw=1.6, label="Total", zorder=6)
for k in ["S", "P", "Cl", "O", "Li", "Nd"]:
    ax1.fill_between(E, 0, S[k], color=col[k], alpha=0.45, label=k, lw=0)
ax1.axvspan(VBM_EIG, CBM_EIG, color="0.85", zorder=0)
ax1.axvline(0, color="gray", ls="--", lw=1.0)
ax1.set_ylabel("DOS (states/eV)", fontsize=12)
ax1.legend(loc="upper right", ncol=2, fontsize=8.5, framealpha=0.95)
ax1.set_ylim(bottom=0)
ax1.set_title(r"Nd$_2$O$_3$-doped modelc — DOS / PDOS", fontsize=12)
ax1.text(0.015, 0.95,
         f"gap (eigenvalue, k661) = {GAP_EIG:.2f} eV\nclean — no mid-gap states\n"
         f"curve: k441 DFT+U, Gaussian {SIGMA_EV} eV",
         transform=ax1.transAxes, va="top", fontsize=8.5,
         bbox=dict(fc="#fffae6", ec="0.6", alpha=0.95))
# --- bottom: O 2p + site-resolved Nd 4f ---
ax2.fill_between(E, 0, S["O"], color="tab:red", alpha=0.4, label="O 2p (in PS$_4$)", lw=0)
ax2.plot(E, S["Nd1_4f"], color="magenta", lw=1.5, ls="--", label="Nd1 4f (oxy, empty)")
ax2.plot(E, S["Nd2_4f"], color="saddlebrown", lw=1.5, ls=":", label="Nd2 4f (sulfide, filled)")
ax2.axvspan(VBM_EIG, CBM_EIG, color="0.85", zorder=0)
ax2.axvline(0, color="gray", ls="--", lw=1.0)
ax2.set_xlabel(r"$E - E_F$ (eV)", fontsize=12)
ax2.set_ylabel("PDOS", fontsize=12)
ax2.legend(loc="upper right", fontsize=8.5, framealpha=0.95)
ax2.set_xlim(-8, 4)
ax2.set_ylim(bottom=0)
plt.tight_layout()
plt.savefig(OUT_PNG, dpi=200, facecolor="white", bbox_inches="tight")
print(f"-> {OUT_PNG}")
print(f"-> {OUT_CSV}")
print(f"E grid dE={dE:.4f} eV  sigma={sig:.2f} pts ({SIGMA_EV} eV)")
print(f"DOS-edge gap (k441 curve): VBM={vbm:.3f} CBM={cbm:.3f} -> {cbm-vbm:.3f} eV")
print(f"eigenvalue gap (k661, label): {GAP_EIG} eV")
