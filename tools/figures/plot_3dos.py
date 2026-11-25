#!/usr/bin/env python3
"""comp1 / modelc / Nd2O3-doped DOS-PDOS 3-panel comparison (eigenvalue gaps)."""
import numpy as np
from scipy.ndimage import gaussian_filter1d
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SIG = 0.08  # Gaussian eV
SYS = {
    "comp1":  dict(csv="docs/figures/comp1_pdos_compact.csv",   gap=2.066, vbm=-1.596, cbm=0.470, title="comp1  (LPSCl, ordered)"),
    "modelc": dict(csv="docs/figures/modelc_pdos_compact.csv",  gap=2.099, vbm=-1.042, cbm=1.057, title="modelc  (LPSCl$_{1.6}$, disordered)"),
    "nd":     dict(csv="docs/figures/nd_dos/nd_pdos_compact.csv", gap=1.632, vbm=-0.798, cbm=0.833, title="Nd$_2$O$_3$-doped modelc"),
}
COL = {"S":"tab:green","P":"tab:orange","Cl":"tab:purple","O":"tab:red","Li":"tab:blue","Nd":"tab:cyan"}

fig, axs = plt.subplots(3, 1, figsize=(8, 9), sharex=True)
for ax, (k, info) in zip(axs, SYS.items()):
    hdr = open(info["csv"]).readline().strip().split(",")
    d = np.loadtxt(info["csv"], delimiter=",", skiprows=1)
    E = d[:, 0]
    dE = np.median(np.diff(E)); sig = max(1.0, SIG/dE)
    C = {h: d[:, i] for i, h in enumerate(hdr)}
    tot = gaussian_filter1d(C["total"], sig)
    ax.plot(E, tot, "k", lw=1.4, label="Total", zorder=6)
    for el in ["S", "P", "Cl", "O", "Li", "Nd"]:
        if el in C:
            ax.fill_between(E, 0, gaussian_filter1d(C[el], sig), color=COL[el], alpha=0.45, label=el, lw=0)
    ax.axvspan(info["vbm"], info["cbm"], color="0.88", zorder=0)
    ax.axvline(0, color="gray", ls="--", lw=0.9)
    win = (E > -7) & (E < 4)
    ax.set_xlim(-7, 4); ax.set_ylim(0, tot[win].max()*1.12)
    ax.set_ylabel("DOS (states/eV)", fontsize=10)
    ax.set_title(f"{info['title']}    gap = {info['gap']:.2f} eV  (eigenvalue)", fontsize=11)
    ax.legend(ncol=4, fontsize=7.5, loc="upper right", framealpha=0.95)
    ax.text(0.01, 0.93, "N(E$_F$)=0 (clean)", transform=ax.transAxes, fontsize=8, va="top", color="0.3")
axs[-1].set_xlabel(r"$E - E_F$ (eV)", fontsize=12)
fig.suptitle("Argyrodite DOS/PDOS — eigenvalue gaps (PBE/USPP, Gaussian 0.08 eV)", fontsize=12, y=1.005)
plt.tight_layout()
plt.savefig("docs/figures/dos_compare_3.png", dpi=200, facecolor="white", bbox_inches="tight")
print("-> docs/figures/dos_compare_3.png")
