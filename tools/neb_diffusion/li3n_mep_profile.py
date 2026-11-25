#!/usr/bin/env python3
"""li3n_mep_profile.py — 1D reaction-coordinate profile extracted from the measured 2D PES.

WHY NOT NEB (4 failed attempts, see li_adatom_neb_protocol.md):
  free top-half slab  -> surface reconstructs near the on-top-Li saddle (8.95 eV blowups)
  fully frozen slab   -> slab remembers the initial adatom site (endpoint asymmetry
                         0.73 eV >> 0.156 eV barrier) and the rigid landscape is rough
On this soft ionic surface the robust object IS the constrained PES scan itself
(per-point z-relaxed adatom + relaxed top half). This script turns that scan into
the reviewer-facing 1D profile: E vs path length s along the minimax MEP,
truncated to a single hop (min -> equivalent min through one saddle).

  python3 li3n_mep_profile.py [pes_out_dir]     # default /data/work/runs/li3n_pes_uma
Outputs: mep_profile.csv (s_A, E_eV), mep_profile.png (markers = computed grid points).
CPU-only (numpy + matplotlib + ase for the cell).
"""
import sys
import numpy as np

D = sys.argv[1] if len(sys.argv) > 1 else "/data/work/runs/li3n_pes_uma"

E = np.loadtxt(f"{D}/pes_grid.csv", delimiter=",")
N = E.shape[0]
assert E.shape == (N, N), f"grid not square: {E.shape}"

from ase.io import read
cell = read(f"{D}/mep_path.xyz", index=0).cell.array
av, bv = cell[0], cell[1]


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
    return best[goal], path[::-1]


# --- minima on the periodic grid (same logic as the PES scanner) ---
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
assert equiv, "no equivalent second minimum on the grid"
barrier_full, path = minimax_path(E, gmin, equiv[0][0])

# --- path -> real-space arclength (periodic min-image on grid deltas) ---
def wrapd(d):
    return d - N * round(d / N)

s = [0.0]
for (i1, j1), (i2, j2) in zip(path[:-1], path[1:]):
    dr = (wrapd(i2 - i1) / N) * av + (wrapd(j2 - j1) / N) * bv
    s.append(s[-1] + float(np.linalg.norm(dr)))
s = np.array(s)
Ep = np.array([E[p] for p in path])

# --- truncate to a single hop: cut at the first interior minimum near 0 ---
cut = None
for k in range(1, len(path) - 1):
    if Ep[k] <= Ep[k - 1] and Ep[k] <= Ep[k + 1] and Ep[k] < 0.05:
        cut = k
        break
if cut is not None:
    path, Ep, s = path[:cut + 1], Ep[:cut + 1], s[:cut + 1]
    print(f"truncated at interior minimum (point {cut}) -> single hop")

ks = int(np.argmax(Ep))
si, sj = path[ks]
print(f"single-hop length = {s[-1]:.2f} A over {len(path)} grid points")
print(f"BARRIER = {Ep.max():.3f} eV at s = {s[ks]:.2f} A, grid ({si},{sj}) = frac ({si/N:.3f},{sj/N:.3f})")

np.savetxt(f"{D}/mep_profile.csv", np.column_stack([s, Ep]), delimiter=",",
           header="s_A,E_eV  (relaxed PES energies along minimax MEP, single hop; "
                  "adatom z-relaxed + top slab half relaxed per point)", comments="# ")

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.4, 3.8))
ax.plot(s, Ep, "o-", ms=5, lw=1.6, color="#1f6fb2", label="computed images (PES MEP)")
ax.plot(s[ks], Ep[ks], "r*", ms=15, label=f"saddle {Ep.max():.3f} eV (on-top Li)")
ax.set_xlabel("reaction coordinate s along MEP (Å)")
ax.set_ylabel("E (eV, min = 0)")
ax.set_title("Li adatom hop on Li$_3$N(001) — measured MEP profile (UMA)")
ax.legend(fontsize=8, frameon=False)
ax.grid(alpha=0.25)
fig.tight_layout()
fig.savefig(f"{D}/mep_profile.png", dpi=220)
print(f"saved: {D}/mep_profile.csv, {D}/mep_profile.png")
