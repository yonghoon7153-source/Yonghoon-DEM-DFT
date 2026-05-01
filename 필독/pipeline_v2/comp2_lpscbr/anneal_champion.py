"""comp2 champion anneal: best halogen + best Li → 500K 100ps + 300K 10ps + relax

Mirrored from KISTI: /scratch/x3430a02/kgy/manuscript_support/pipeline_v2/comp2_lpscbr/anneal_champion.py
NOTE: KISTI .py says 50ps, but actual log shows 100ps run.
This local copy reflects the actual production (100ps).
"""
import numpy as np
import json
from itertools import combinations
from pymatgen.core import Structure, Lattice
from pymatgen.symmetry.groups import SpaceGroup
from pymatgen.io.ase import AseAtomsAdaptor
from ase import units
from ase.io import write
from ase.md.langevin import Langevin
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
from ase.optimize import LBFGS
from fairchem.core import pretrained_mlip
from fairchem.core.calculate.ase_calculator import FAIRChemCalculator

a_exp = 9.852
sg = SpaceGroup("F-43m")
lat = Lattice.cubic(a_exp)

def get_orbits(pos):
    out = []
    for c in sg.get_orbit(np.array(pos)):
        cm = np.mod(c, 1.0)
        if not any(np.allclose(cm, u, atol=0.01) for u in out): out.append(cm)
    return out

Li48 = get_orbits([0.1766, 0.1766, 0.0224])
P_s  = get_orbits([0.5, 0.5, 0.5])
S16e = get_orbits([0.6205, 0.6205, 0.6205])
free = get_orbits([0.25, 0.25, 0.25]) + get_orbits([0.0, 0.0, 0.0])

# Best from Stage 1+2 (step1_v2.py output, hardcoded)
best_cl = [0, 2]
best_br = [5, 7]
rng = np.random.RandomState(42)
Li_configs = [sorted(rng.choice(48, 24, replace=False).tolist()) for _ in range(20)]
best_li = Li_configs[0]
print(f"Best halogen: Cl={best_cl} Br={best_br}")
print(f"Best Li config: #0 (24 of 48)")

def build(cl_idx, br_idx, li_idx):
    sp, co = [], []
    for i in li_idx: sp.append('Li'); co.append(Li48[i])
    for c in P_s:    sp.append('P');  co.append(c)
    for c in S16e:   sp.append('S');  co.append(c)
    for i, c in enumerate(free):
        sp.append('Cl' if i in cl_idx else ('Br' if i in br_idx else 'S'))
        co.append(c)
    return Structure(lat, sp, co)

predictor = pretrained_mlip.get_predict_unit("uma-s-1p1", device="cuda")
calc = FAIRChemCalculator(predictor, task_name="omat")
adaptor = AseAtomsAdaptor()

sb = build(best_cl, best_br, best_li)
a = adaptor.get_atoms(sb); a.calc = calc
print(f"Champion atoms: {len(a)}, E_init={a.get_potential_energy():.4f}")

e_before = a.get_potential_energy()
pos_before = a.get_positions().copy(); sp_list = a.get_chemical_symbols()

print("500K 100ps anneal...", flush=True)
MaxwellBoltzmannDistribution(a, temperature_K=500)
Langevin(a, 1.0*units.fs, temperature_K=500, friction=0.01).run(100000)

print("300K 10ps quench...", flush=True)
Langevin(a, 1.0*units.fs, temperature_K=300, friction=0.05).run(10000)

print("LBFGS final relax...", flush=True)
try: LBFGS(a, logfile=None).run(fmax=0.005, steps=300)
except: pass

e_after = a.get_potential_energy()
print(f"E after: {e_after:.4f}  ΔE = {(e_after-e_before)*1000:.1f} meV")

pos_after = a.get_positions().copy()
print("Element displacement:")
for elem in ['Li','P','S','Cl','Br']:
    d = [np.linalg.norm(pos_after[i]-pos_before[i]) for i in range(len(sp_list)) if sp_list[i]==elem]
    if d: print(f"  {elem:3s}: mean={np.mean(d):.3f} max={np.max(d):.3f} A")

write('comp2_v2_champion.xyz', a)
adaptor.get_structure(a).to('comp2_v2_champion.cif')
print(f"\nCHAMPION saved: comp2_v2_champion.xyz / .cif")
print(f"  {len(a)} atoms, E={e_after:.4f} eV")

with open('pipeline_v2_results.json', 'w') as f:
    json.dump({
        "best_cl": best_cl, "best_br": best_br, "best_li": best_li,
        "e_before_anneal": e_before, "e_after_anneal": e_after,
        "champion_atoms": len(a)
    }, f, indent=2)
