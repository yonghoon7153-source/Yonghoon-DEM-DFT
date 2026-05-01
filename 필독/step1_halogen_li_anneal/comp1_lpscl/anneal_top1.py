import numpy as np
from pymatgen.core import Structure, Lattice
from pymatgen.symmetry.groups import SpaceGroup
from pymatgen.io.ase import AseAtomsAdaptor
from ase import units
from ase.md.langevin import Langevin
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
from ase.optimize import LBFGS
from ase.io import write
from itertools import combinations
from fairchem.core import pretrained_mlip
from fairchem.core.calculate.ase_calculator import FAIRChemCalculator

predictor = pretrained_mlip.get_predict_unit("uma-s-1p1", device="cuda")
calc = FAIRChemCalculator(predictor, task_name="omat")

a_exp = 9.852
sg = SpaceGroup("F-43m")
lattice = Lattice.cubic(a_exp)

def get_orbits(pos):
    orbits = sg.get_orbit(np.array(pos))
    unique = []
    for c in orbits:
        c_mod = np.mod(c, 1.0)
        if not any(np.allclose(c_mod, u, atol=0.01) for u in unique):
            unique.append(c_mod)
    return unique

Li48h = get_orbits([0.1766, 0.1766, 0.0224])
P_sites = get_orbits([0.5, 0.5, 0.5])
S16e = get_orbits([0.6205, 0.6205, 0.6205])
X4c = get_orbits([0.25, 0.25, 0.25])
X4a = get_orbits([0.0, 0.0, 0.0])
free_sites = X4c + X4a

halogen_configs = list(combinations(range(8), 4))
best_halogen = list(halogen_configs[39])

rng = np.random.RandomState(42)
Li_configs = []
for i in range(20):
    indices = rng.choice(48, 24, replace=False)
    Li_configs.append(sorted(indices.tolist()))

adaptor = AseAtomsAdaptor()

def build(halogen_idx, li_idx):
    sp = []; co = []
    for i in li_idx:
        sp.append('Li'); co.append(Li48h[i])
    for c in P_sites:
        sp.append('P'); co.append(c)
    for c in S16e:
        sp.append('S'); co.append(c)
    for i, c in enumerate(free_sites):
        sp.append('Cl' if i in halogen_idx else 'S'); co.append(c)
    return Structure(lattice, sp, co)

print("=== Rank 1 (Li config #0) Annealing (50ps) ===", flush=True)

struct = build(best_halogen, Li_configs[0])
atoms = adaptor.get_atoms(struct)
atoms.calc = calc

try:
    LBFGS(atoms, logfile=None).run(fmax=0.01, steps=200)
except: pass
e_before = atoms.get_potential_energy()
print(f"  E before: {e_before:.4f} eV", flush=True)

print(f"  Annealing 500K, 50ps...", flush=True)
MaxwellBoltzmannDistribution(atoms, temperature_K=500)
Langevin(atoms, 1.0*units.fs, temperature_K=500, friction=0.01).run(50000)

print(f"  Quench 300K, 5ps...", flush=True)
Langevin(atoms, 1.0*units.fs, temperature_K=300, friction=0.05).run(5000)

try:
    LBFGS(atoms, logfile=None).run(fmax=0.005, steps=300)
except: pass

e_after = atoms.get_potential_energy()
print(f"  E after:  {e_after:.4f} eV", flush=True)
print(f"  dE = {(e_after-e_before)*1000:.1f} meV", flush=True)

write('comp1_v2_rank1_annealed.xyz', atoms)

print(f"\n=== FINAL RANKING ===")
print(f"  Rank 1 (#0):  {e_after:.4f} eV")
print(f"  Rank 4 (#15): -217.0421 eV")
print(f"  Rank 3 (#8):  -217.0300 eV")
print(f"  Rank 5 (#9):  -217.0131 eV")
print(f"  Rank 2 (#1):  -216.9528 eV")
if e_after < -217.0421:
    print(f"  ★ Rank 1 유지! Champion = #0")
else:
    print(f"  ★ Rank 4가 Champion! #15가 최종 승자!")
