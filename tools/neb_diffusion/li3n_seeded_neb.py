#!/usr/bin/env python3
"""li3n_seeded_neb.py — CI-NEB seeded from the measured PES minimax path (mep_path.xyz).

Fixes the 3x-failed Path D: instead of IDPP interpolation (which exploded over
on-top N), the initial images come from the PES-measured MEP, so the optimizer
starts near the true path. Endpoints are re-relaxed with free xy (true minima),
interior images CI-NEB refined. Reaction coordinate = adatom path length (A).

  conda activate uma
  python3 li3n_seeded_neb.py [pes_out_dir]      # default /data/work/runs/li3n_pes_uma
Outputs (in pes_out_dir): neb_seeded_final.xyz, neb_seeded_profile.json
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
calc = FAIRChemCalculator(pretrained_mlip.get_predict_unit("uma-s-1p1", device="cuda"),
                          task_name="oc20")
imgs = read(f"{D}/mep_path.xyz", index=":")
ad = len(imgs[0]) - 1

# --- unwrap adatom across the periodic boundary (minimax path may wrap the cell) ---
cell = imgs[0].cell.array
icell = np.linalg.inv(cell)
for k in range(1, len(imgs)):
    dr = imgs[k].positions[ad] - imgs[k - 1].positions[ad]
    f = dr @ icell
    f -= np.round(f)
    imgs[k].positions[ad] = imgs[k - 1].positions[ad] + f @ cell
_j = [float(np.linalg.norm(imgs[k + 1].positions[ad] - imgs[k].positions[ad]))
      for k in range(len(imgs) - 1)]
print("adatom jumps (A):", np.round(_j, 2), flush=True)
assert max(_j) < 4.0, "path still has a >4A jump after unwrap -- inspect mep_path.xyz"
zs = imgs[0].positions[:, 2]
zsl = np.delete(zs, ad)
zcut = zsl.min() + 0.5 * (zsl.max() - zsl.min())
fix = [i for i in range(len(imgs[0])) if i != ad and imgs[0].positions[i, 2] < zcut]

A = imgs[0]
sym = np.array(A.get_chemical_symbols())
top = [i for i in range(len(A)) if i != ad and A.positions[i, 2] > zsl.max() - 1.6]
def site(p):
    d = [(np.linalg.norm((A.positions[t] - p)[:2]), sym[t]) for t in top]
    d.sort()
    return ", ".join(f"{s}:{r:.2f}A" for r, s in d[:3])
print("min  site env :", site(imgs[0].positions[ad]), flush=True)
print("saddle guess  :", site(imgs[4].positions[ad]), flush=True)

for im in imgs:
    im.set_constraint(FixAtoms(fix))
    im.calc = calc
for k in (0, len(imgs) - 1):
    FIRE(imgs[k], logfile=None).run(fmax=0.03, steps=250)
    print(f"endpoint {k}: {imgs[k].get_potential_energy():.4f} eV", flush=True)

neb = NEB(imgs, k=0.1, allow_shared_calculator=True)
FIRE(neb, logfile="-").run(fmax=0.1, steps=60)     # warmup
neb.climb = True
FIRE(neb, logfile="-").run(fmax=0.05, steps=250)   # climbing image

E = np.array([im.get_potential_energy() for im in imgs])
E -= E.min()
s = [0.0]
for a_, b_ in zip(imgs[:-1], imgs[1:]):
    s.append(s[-1] + np.linalg.norm(b_.positions[ad] - a_.positions[ad]))
print("\n=== CI-NEB profile (s_A, E_eV) ===")
for x, e in zip(s, E):
    print(f"  {x:6.2f}  {e:.4f}")
print(f"BARRIER = {E.max():.3f} eV at s={s[int(E.argmax())]:.2f} A (image {int(E.argmax())})")
write(f"{D}/neb_seeded_final.xyz", imgs)
json.dump({"s_A": list(map(float, s)), "E_eV": list(map(float, E))},
          open(f"{D}/neb_seeded_profile.json", "w"), indent=1)
print("saved: neb_seeded_final.xyz / neb_seeded_profile.json")
