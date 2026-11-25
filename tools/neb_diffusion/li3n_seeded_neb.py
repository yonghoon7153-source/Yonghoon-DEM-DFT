#!/usr/bin/env python3
"""li3n_seeded_neb.py — CI-NEB seeded from the measured PES minimax path (v3).

Failure history (why v3 looks like this):
  v1  IDPP interpolation exploded over on-top N (3x).
  v2a seed wrapped the PBC -> 6 A image gap -> fake 8.95 eV image.  (fixed: unwrap)
  v2b STILL exploded (8.95 eV again) for three compounding reasons:
      1. linspace index resampling DUPLICATED consecutive images (jumps
         [0, 1.58, ...] -- degenerate tangents),
      2. the minimax path chains THROUGH an intermediate minimum (Dijkstra
         minimax passes minima for free) -> seed spanned a multi-hop path,
      3. free top-half slab + climbing image near the on-top-Li saddle let the
         SURFACE RECONSTRUCT: one image rammed to +8.95 eV, another fell 0.46 eV
         BELOW the relaxed endpoints.
  v3  therefore: dedupe seed points, TRUNCATE at the first intermediate minimum
      (single hop, single saddle), resample evenly along the adatom polyline,
      and run ADATOM-ONLY NEB (whole slab frozen -> 3 DOF/image, cannot explode).
      The rigid-surface barrier is quoted as a PATH-SHAPE refinement of the PES;
      the physical numbers remain the z-relaxed PES (0.156 eV) and the DFT P0 pair.

  conda activate uma
  python3 li3n_seeded_neb.py [pes_out_dir]      # default /data/work/runs/li3n_pes_uma
Outputs (in pes_out_dir): neb_seeded_final.xyz, neb_seeded_profile.json, seed profile print.
"""
import sys, json
import numpy as np
from ase.io import read, write
from ase.constraints import FixAtoms
from ase.optimize import FIRE
from ase.mep import NEB
from fairchem.core import pretrained_mlip
from fairchem.core.calculate.ase_calculator import FAIRChemCalculator

D = sys.argv[1] if len(sys.argv) > 1 else "/data/work/runs/li3n_pes_uma"
NIM = 7          # images after resampling (endpoints included)
calc = FAIRChemCalculator(pretrained_mlip.get_predict_unit("uma-s-1p1", device="cuda"),
                          task_name="oc20")
seed = read(f"{D}/mep_path.xyz", index=":")
ad = len(seed[0]) - 1
A0 = seed[0].copy()                     # slab identical across seed images (PES construction)
cell = A0.cell.array
icell = np.linalg.inv(cell)

# --- 1) unwrap adatom across PBC, collect path points ---
pts = [seed[0].positions[ad].copy()]
for im in seed[1:]:
    dr = im.positions[ad] - pts[-1]
    f = dr @ icell
    f -= np.round(f)
    pts.append(pts[-1] + f @ cell)

# --- 2) dedupe consecutive duplicates (linspace index collisions) ---
P = [pts[0]]
for p in pts[1:]:
    if np.linalg.norm(p - P[-1]) > 0.05:
        P.append(p)
print(f"seed points: {len(pts)} -> {len(P)} after dedupe", flush=True)

# --- 3) single-point seed profile; truncate at first intermediate minimum ---
def sp_energy(p):
    At = A0.copy()
    At.positions[ad] = p
    At.calc = calc
    return At.get_potential_energy()

Es = np.array([sp_energy(p) for p in P])
Es -= Es.min()
print("seed single-point profile (eV):", np.round(Es, 3), flush=True)
cutk = None
for k in range(1, len(P) - 1):
    if Es[k] <= Es[k - 1] and Es[k] <= Es[k + 1] and Es[k] < 0.08:
        cutk = k
        break
if cutk is not None:
    print(f"intermediate minimum at seed point {cutk} (E={Es[cutk]:.3f}) -> truncating: single hop", flush=True)
    P = P[:cutk + 1]

# --- 4) resample NIM points evenly along the polyline ---
seg = np.array([np.linalg.norm(b - a) for a, b in zip(P[:-1], P[1:])])
s_cum = np.concatenate([[0.0], np.cumsum(seg)])
targets = np.linspace(0.0, s_cum[-1], NIM)
Q = []
for t in targets:
    i = min(np.searchsorted(s_cum, t, side="right") - 1, len(seg) - 1)
    w = 0.0 if seg[i] == 0 else (t - s_cum[i]) / seg[i]
    Q.append((1 - w) * P[i] + w * P[i + 1])
print(f"resampled to {NIM} images over {s_cum[-1]:.2f} A", flush=True)

# --- 5) build adatom-only images: whole slab frozen (3 DOF per image) ---
fix = FixAtoms(indices=[i for i in range(len(A0)) if i != ad])
imgs = []
for q in Q:
    At = A0.copy()
    At.positions[ad] = q
    At.set_constraint(fix)
    At.calc = calc
    imgs.append(At)

sym = np.array(A0.get_chemical_symbols())
zsl = np.delete(A0.positions[:, 2], ad)
top = [i for i in range(len(A0)) if i != ad and A0.positions[i, 2] > zsl.max() - 1.6]
def site(p):
    d = sorted((np.linalg.norm((A0.positions[t] - p)[:2]), sym[t]) for t in top)
    return ", ".join(f"{s}:{r:.2f}A" for r, s in d[:3])
print("min  site env :", site(Q[0]), flush=True)
print("mid  site env :", site(Q[NIM // 2]), flush=True)

for k in (0, NIM - 1):
    FIRE(imgs[k], logfile=None).run(fmax=0.03, steps=200)
    print(f"endpoint {k}: {imgs[k].get_potential_energy():.4f} eV", flush=True)

neb = NEB(imgs, k=0.3, allow_shared_calculator=True)
FIRE(neb, logfile="-").run(fmax=0.1, steps=80)      # warmup
neb.climb = True
FIRE(neb, logfile="-").run(fmax=0.05, steps=300)    # climbing image

E = np.array([im.get_potential_energy() for im in imgs])
E -= E.min()
assert E.max() < 2.0, f"profile exploded ({E.max():.2f} eV) despite rigid slab -- inspect"
s = [0.0]
for a_, b_ in zip(imgs[:-1], imgs[1:]):
    s.append(s[-1] + np.linalg.norm(b_.positions[ad] - a_.positions[ad]))
print("\n=== CI-NEB profile, rigid-surface single hop (s_A, E_eV) ===")
for x, e in zip(s, E):
    print(f"  {x:6.2f}  {e:.4f}")
ib = int(E.argmax())
print(f"BARRIER = {E.max():.3f} eV at s={s[ib]:.2f} A (image {ib})")
print("TS  site env :", site(imgs[ib].positions[ad]))
write(f"{D}/neb_seeded_final.xyz", imgs)
json.dump({"s_A": list(map(float, s)), "E_eV": list(map(float, E)),
           "note": "adatom-only CI-NEB on rigid slab, single hop from measured PES MEP; "
                   "physical barrier refs: z-relaxed PES 0.156 eV + DFT P0 pair"},
          open(f"{D}/neb_seeded_profile.json", "w"), indent=1)
print("saved: neb_seeded_final.xyz / neb_seeded_profile.json")
