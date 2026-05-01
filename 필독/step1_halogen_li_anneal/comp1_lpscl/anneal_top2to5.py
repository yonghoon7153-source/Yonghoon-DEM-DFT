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
from mace.calculators import mace_mp

calc = mace_mp(model="medium", default_dtype="float64")

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

# Best halogen = config #39 재현
halogen_configs = list(combinations(range(8), 4))
best_halogen = list(halogen_configs[39])
print(f"Best halogen: config #39 = {best_halogen}", flush=True)

# Li configs 재현 (same seed=42)
rng = np.random.RandomState(42)
Li_configs = []
for i in range(20):
    indices = rng.choice(48, 24, replace=False)
    Li_configs.append(sorted(indices.tolist()))

top_li = [0, 1, 8, 15, 9]  # from log
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

print(f"\n=== Top 2~5 Annealing (MACE CPU, 100ps) ===", flush=True)
results = []

for rank, li_idx in enumerate([1, 8, 15, 9], start=2):
    print(f"\n--- Rank {rank} (Li config #{li_idx}) ---", flush=True)
    struct = build(best_halogen, Li_configs[li_idx])
    atoms = adaptor.get_atoms(struct)
    atoms.calc = calc

    try:
        LBFGS(atoms, logfile=None).run(fmax=0.01, steps=200)
    except: pass
    e_before = atoms.get_potential_energy()
    print(f"  E before: {e_before:.4f} eV", flush=True)

    print(f"  Annealing 500K, 100ps...", flush=True)
    MaxwellBoltzmannDistribution(atoms, temperature_K=500)
    Langevin(atoms, 1.0*units.fs, temperature_K=500, friction=0.01).run(100000)

    print(f"  Quench 300K, 10ps...", flush=True)
    Langevin(atoms, 1.0*units.fs, temperature_K=300, friction=0.05).run(10000)

    try:
        LBFGS(atoms, logfile=None).run(fmax=0.005, steps=300)
    except: pass

    e_after = atoms.get_potential_energy()
    print(f"  E after:  {e_after:.4f} eV", flush=True)
    print(f"  dE = {(e_after-e_before)*1000:.1f} meV", flush=True)

    results.append({'rank': rank, 'li': li_idx, 'e_before': e_before, 'e_after': e_after})
    write(f'comp1_v2_rank{rank}_annealed.xyz', atoms)

print(f"\n{'='*60}")
print(f"=== SUMMARY ===")
for r in results:
    print(f"  Rank {r['rank']} (#{r['li']}): {r['e_before']:.4f} → {r['e_after']:.4f} dE={r['e_after']-r['e_before']:.4f}")
best = min(results, key=lambda x: x['e_after'])
print(f"\n★ Best: Rank {best['rank']}, E={best['e_after']:.4f}")
print(f"  → Rank 1 (E_after=??) 와 비교 필요!")
