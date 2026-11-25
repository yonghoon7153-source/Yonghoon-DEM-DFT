#!/usr/bin/env python3
"""li3n_figset.py — professor-style two-panel figure for the Li3N revision:
(a) site-resolved Li adsorption energies (bar + top-view insets)
(b) single-hop migration profile (normalized path coordinate, meV, dE label)

Data sources: the measured PES campaign (mep_path.xyz for the slab+adatom
frame, hop_profile.csv for panel b). Panel (a) recomputes 4 characteristic
sites with the SAME constrained protocol as the PES (adatom xy-pinned,
z free; top slab half free) plus two references (bare slab, isolated Li):
  E_ads(site) = E(slab+Li@site) - E(bare slab) - E(Li atom)

  conda activate uma
  python3 li3n_figset.py [pes_out_dir]     # default /data/work/runs/li3n_pes_uma
Outputs: li3n_figset.png, li3n_site_ads.csv  (in pes_out_dir)
"""
import sys
import numpy as np

D = sys.argv[1] if len(sys.argv) > 1 else "/data/work/runs/li3n_pes_uma"

from ase import Atoms
from ase.io import read
from ase.constraints import FixAtoms, FixedLine
from ase.optimize import FIRE
from fairchem.core import pretrained_mlip
from fairchem.core.calculate.ase_calculator import FAIRChemCalculator

calc = FAIRChemCalculator(pretrained_mlip.get_predict_unit("uma-s-1p1", device="cuda"),
                          task_name="oc20")

A0 = read(f"{D}/mep_path.xyz", index=0)
ad = len(A0) - 1
z0 = A0.positions[ad, 2]
sym = np.array(A0.get_chemical_symbols())
zs = A0.positions[:, 2]
z_slab = np.delete(zs, ad)
z_cut = z_slab.min() + 0.5 * (z_slab.max() - z_slab.min())
fixed_idx = [i for i in range(len(A0)) if i != ad and zs[i] < z_cut]
top = [i for i in range(len(A0)) if i != ad and zs[i] > z_slab.max() - 1.6]
topLi = [i for i in top if sym[i] == "Li"]
topN = [i for i in top if sym[i] == "N"]

# ---------- references ----------
bare = A0.copy()
del bare[ad]
bare.set_constraint(FixAtoms(indices=[i for i in range(len(bare)) if bare.positions[i, 2] < z_cut]))
bare.calc = calc
FIRE(bare, logfile=None).run(fmax=0.05, steps=120)
E_bare = bare.get_potential_energy()
print(f"E_bare_slab = {E_bare:.4f} eV", flush=True)

li = Atoms("Li", positions=[[7.5, 7.5, 7.5]], cell=[15, 15, 15], pbc=True)
li.calc = calc
E_li = li.get_potential_energy()
print(f"E_Li_atom   = {E_li:.4f} eV", flush=True)

# ---------- characteristic sites (xy targets on the surface) ----------
min_xy = A0.positions[ad, :2].copy()                       # PES global min (bridge-type)
saddle_xy = None
try:
    hp = np.loadtxt(f"{D}/hop_profile.csv", delimiter=",")
except OSError:
    hp = None
# saddle xy: from mep_path mid image (unwrapped path midpoint)
seed = read(f"{D}/mep_path.xyz", index=":")
cell = A0.cell.array
icell = np.linalg.inv(cell)
pts = [seed[0].positions[ad].copy()]
for im in seed[1:]:
    f = (im.positions[ad] - pts[-1]) @ icell
    f -= np.round(f)
    pts.append(pts[-1] + f @ cell)
saddle_xy = pts[len(pts) // 4][:2]                          # 1-hop midpoint region (grid saddle)
ontopLi_xy = A0.positions[min(topLi, key=lambda i: np.linalg.norm(A0.positions[i, :2] - saddle_xy)), :2]
ontopN_xy = A0.positions[min(topN, key=lambda i: np.linalg.norm(A0.positions[i, :2] - min_xy)), :2]
# hollow: farthest point from all top atoms within one cell around the min
gx = np.linspace(-0.5, 0.5, 21)
best, bxy = -1, None
for fa in gx:
    for fb in gx:
        p = min_xy + fa * cell[0][:2] + fb * cell[1][:2]
        dmin = min(np.linalg.norm((A0.positions[t, :2] - p)) for t in top)
        if dmin > best:
            best, bxy = dmin, p
hollow_xy = bxy

SITES = [("bridge (min)", min_xy), ("hollow", hollow_xy),
         ("on-top Li (TS)", ontopLi_xy), ("on-top N", ontopN_xy)]

rows = []
for name, xy in SITES:
    At = A0.copy()
    At.positions[ad, :2] = xy
    At.positions[ad, 2] = z0
    At.set_constraint([FixAtoms(indices=fixed_idx), FixedLine(ad, direction=[0, 0, 1])])
    At.calc = calc
    FIRE(At, logfile=None).run(fmax=0.05, steps=100)
    E = At.get_potential_energy()
    rows.append((name, xy, E, E - E_bare - E_li))
    print(f"{name:16s} E_ads = {rows[-1][3]:+.3f} eV", flush=True)

np.savetxt(f"{D}/li3n_site_ads.csv",
           np.array([[r[3]] for r in rows]),
           delimiter=",", comments="# ",
           header="E_ads_eV rows: " + " | ".join(r[0] for r in rows) +
                  f" ; refs: E_bare={E_bare:.4f}, E_Li_atom={E_li:.4f} (UMA oc20, constrained protocol)")

# ---------- figure ----------
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

fig, (axa, axb) = plt.subplots(1, 2, figsize=(11, 4.4))

# (a) bars + insets
names = [r[0] for r in rows]
vals = [r[3] for r in rows]
colors = ["#d46a6a", "#4a90c4", "#4a90c4", "#9ec9e8"]
bars = axa.bar(range(len(rows)), vals, color=colors, width=0.62)
for i, v in enumerate(vals):
    axa.text(i, v + 0.05, f"{v:.3f}", ha="center", va="bottom", fontsize=9, color="white", fontweight="bold")
axa.set_xticks(range(len(rows)))
axa.set_xticklabels(names, fontsize=9)
axa.set_ylabel("Adsorption energy (eV)")
axa.set_xlabel("Adsorption site")
axa.set_ylim(min(vals) - 0.55, 0.0)
axa.grid(axis="y", alpha=0.25)
# top-view insets under each bar
for i, (name, xy, E, ea) in enumerate(rows):
    axi = axa.inset_axes([0.03 + i * 0.245, 0.04, 0.21, 0.30])
    for t in top:
        p = A0.positions[t]
        for da in (-1, 0, 1):
            for db in (-1, 0, 1):
                q = p[:2] + da * cell[0][:2] + db * cell[1][:2]
                if np.all(np.abs(q - xy) < 4.2):
                    axi.plot(*q, "o", ms=5 if sym[t] == "Li" else 6,
                             color="#7fb37f" if sym[t] == "Li" else "#8888cc", mec="none")
    axi.plot(*xy, "o", ms=7, color="#d4a017", mec="k", mew=0.6, zorder=5)
    axi.set_xlim(xy[0] - 4.2, xy[0] + 4.2); axi.set_ylim(xy[1] - 4.2, xy[1] + 4.2)
    axi.set_xticks([]); axi.set_yticks([])
    for s_ in axi.spines.values(): s_.set_alpha(0.3)

# (b) migration profile
if hp is not None:
    s_, e_ = hp[:, 0], hp[:, 1] * 1000.0          # meV
    x = s_ / s_[-1]
    axb.plot(x, e_, "o-", ms=5, lw=1.6, color="#1f6fb2")
    k = int(np.argmax(e_))
    axb.annotate(f"$\\Delta E$ = {e_[k]:.0f} meV", xy=(x[k], e_[k]),
                 xytext=(x[k] + 0.16, e_[k] * 0.92), fontsize=11,
                 arrowprops=dict(arrowstyle="-", lw=0.8))
    axb.set_xlabel("Li$^+$ migration path (normalized)")
    axb.set_ylabel("Energy (meV)")
    axb.set_xlim(-0.02, 1.02)
    axb.grid(alpha=0.25)
    axb.set_title("Li adatom hop on Li$_3$N(001) — measured profile (UMA)", fontsize=10)
else:
    axb.text(0.5, 0.5, "hop_profile.csv not found\n(run li3n_hop_densify.py first)",
             ha="center", va="center")

fig.tight_layout()
fig.savefig(f"{D}/li3n_figset.png", dpi=250)
print(f"saved: {D}/li3n_figset.png, {D}/li3n_site_ads.csv")
