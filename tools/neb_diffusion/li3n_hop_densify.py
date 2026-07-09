#!/usr/bin/env python3
"""li3n_hop_densify.py — densify the single-hop MEP into a smooth MEASURED profile.

The minimax hop from the 12x12 PES is only 3 grid points (min-saddle-min, 2.49 A)
— too sparse for a reviewer-facing 1D curve. This samples NPTS points along that
polyline and runs the SAME constrained relaxation as the PES grid at each one
(adatom xy-pinned via FixedLine z, bottom slab half frozen, top half free).
Each point is independent -> none of the NEB pathologies can occur.

  conda activate uma
  python3 li3n_hop_densify.py [pes_out_dir] [npts]    # defaults: /data/work/runs/li3n_pes_uma, 13
Outputs: hop_profile.csv, hop_profile.png  (dense markers + coarse grid anchors)
Log-friendly: prints "point k/N ..." per point and a final "DENSE BARRIER =" line.
"""
import sys
import numpy as np

D = sys.argv[1] if len(sys.argv) > 1 else "/data/work/runs/li3n_pes_uma"
NPTS = int(sys.argv[2]) if len(sys.argv) > 2 else 13

E = np.loadtxt(f"{D}/pes_grid.csv", delimiter=",")
N = E.shape[0]

from ase.io import read
from ase.constraints import FixAtoms, FixedLine
from ase.optimize import FIRE

A0 = read(f"{D}/mep_path.xyz", index=0)
ad = len(A0) - 1
av, bv = A0.cell.array[0], A0.cell.array[1]
z0 = A0.positions[ad, 2]


def minimax_path(E, start, goal):
    import heapq
    n, m = E.shape
    best = np.full((n, m), np.inf)
    prev = {}
    h = [(E[start], start)]
    best[start] = E[start]
    while h:
        c, (i, j) = heapq.heappop(h)
        if (i, j) == goal:
            break
        if c > best[i, j]:
            continue
        for di in (-1, 0, 1):
            for dj in (-1, 0, 1):
                if di == dj == 0:
                    continue
                k, l = (i + di) % n, (j + dj) % m
                nc = max(c, E[k, l])
                if nc < best[k, l]:
                    best[k, l] = nc
                    prev[(k, l)] = (i, j)
                    heapq.heappush(h, (nc, (k, l)))
    path = [goal]
    while path[-1] != start:
        path.append(prev[path[-1]])
    return path[::-1]


minima = []
for i in range(N):
    for j in range(N):
        nb = [E[(i + di) % N, (j + dj) % N]
              for di in (-1, 0, 1) for dj in (-1, 0, 1) if (di, dj) != (0, 0)]
        if E[i, j] <= min(nb):
            minima.append(((i, j), E[i, j]))
minima.sort(key=lambda t: t[1])
gmin = minima[0][0]
equiv = [m for m in minima[1:] if abs(m[1] - minima[0][1]) < 0.005]
path = minimax_path(E, gmin, equiv[0][0])
Ep = np.array([E[p] for p in path])
for k in range(1, len(path) - 1):                      # truncate: single hop
    if Ep[k] <= Ep[k - 1] and Ep[k] <= Ep[k + 1] and Ep[k] < 0.05:
        path, Ep = path[:k + 1], Ep[:k + 1]
        break

# grid -> real space: origin anchored on mep_path image 0 (= path[0] cell)
def wrapd(d):
    return d - N * round(d / N)

i0, j0 = path[0]
origin = A0.positions[ad] - (i0 / N) * av - (j0 / N) * bv
pts = [A0.positions[ad].copy()]
for (i1, j1), (i2, j2) in zip(path[:-1], path[1:]):
    step = (wrapd(i2 - i1) / N) * av + (wrapd(j2 - j1) / N) * bv
    pts.append(pts[-1] + step)
pts = np.array(pts)
seg = np.linalg.norm(np.diff(pts, axis=0), axis=1)
s_cum = np.concatenate([[0.0], np.cumsum(seg)])
print(f"hop polyline: {len(pts)} anchors, length {s_cum[-1]:.2f} A; coarse barrier {Ep.max():.3f} eV", flush=True)

# constrained-relax protocol identical to the PES grid
zs = A0.positions[:, 2]
z_slab = np.delete(zs, ad)
z_cut = z_slab.min() + 0.5 * (z_slab.max() - z_slab.min())
fixed_idx = [i for i in range(len(A0)) if i != ad and zs[i] < z_cut]

from fairchem.core import pretrained_mlip
from fairchem.core.calculate.ase_calculator import FAIRChemCalculator
calc = FAIRChemCalculator(pretrained_mlip.get_predict_unit("uma-s-1p1", device="cuda"),
                          task_name="oc20")

targets = np.linspace(0.0, s_cum[-1], NPTS)
Ed, sd = [], []
for k, t in enumerate(targets):
    i = min(int(np.searchsorted(s_cum, t, side="right")) - 1, len(seg) - 1)
    w = 0.0 if seg[i] == 0 else (t - s_cum[i]) / seg[i]
    r = (1 - w) * pts[i] + w * pts[i + 1]
    At = A0.copy()
    At.positions[ad] = r
    At.positions[ad, 2] = z0
    At.set_constraint([FixAtoms(indices=fixed_idx), FixedLine(ad, direction=[0, 0, 1])])
    At.calc = calc
    FIRE(At, logfile=None).run(fmax=0.05, steps=100)
    e = At.get_potential_energy()
    Ed.append(e)
    sd.append(t)
    print(f"point {k + 1}/{NPTS}  s={t:5.2f} A  E={e:.4f} eV", flush=True)

Ed = np.array(Ed) - min(Ed)
kb_ = int(Ed.argmax())
print(f"DENSE BARRIER = {Ed.max():.3f} eV at s = {sd[kb_]:.2f} A  ({NPTS} constrained-relaxed points)")
np.savetxt(f"{D}/hop_profile.csv", np.column_stack([sd, Ed]), delimiter=",",
           header="s_A,E_eV  (dense single-hop profile: xy-pinned z-relaxed adatom + free top slab half, "
                  "same protocol as pes_grid; independent points, no NEB)", comments="# ")

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.4, 3.8))
ax.plot(sd, Ed, "o-", ms=5, lw=1.6, color="#1f6fb2", label=f"constrained scan ({NPTS} pts)")
ax.plot(s_cum, Ep - Ep.min(), "s", ms=7, mfc="none", mec="#444444", label="PES grid anchors")
ax.plot(sd[kb_], Ed.max(), "r*", ms=15, label=f"saddle {Ed.max():.3f} eV (on-top Li)")
ax.set_xlabel("reaction coordinate s along MEP (Å)")
ax.set_ylabel("E (eV, min = 0)")
ax.set_title("Li adatom hop on Li$_3$N(001) — measured profile (UMA)")
ax.legend(fontsize=8, frameon=False)
ax.grid(alpha=0.25)
fig.tight_layout()
fig.savefig(f"{D}/hop_profile.png", dpi=220)
print(f"saved: {D}/hop_profile.csv, {D}/hop_profile.png")
