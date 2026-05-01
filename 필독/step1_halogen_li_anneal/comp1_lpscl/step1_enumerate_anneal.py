"""
Pipeline v2 Step 1: Halogen enumerate + Li annealing
Li₆PS₅Cl (comp1): 52 atoms, 4 f.u., F-43m
4a: 4 sites, 4c: 4 sites → S/Cl 배치
48h: 24 sites → Li 24개 (occ=0.5, 모두 채움 = stoichiometric)
"""
import numpy as np
from pymatgen.core import Structure, Lattice, Element
from pymatgen.symmetry.groups import SpaceGroup
from pymatgen.io.ase import AseAtomsAdaptor
from itertools import combinations
from ase import units
from ase.md.langevin import Langevin
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
from ase.optimize import LBFGS
from fairchem.core import pretrained_mlip
from fairchem.core.calculate.ase_calculator import FAIRChemCalculator
import json, os

# ═══════════════════════════════════════════
# 1. Build conventional cell
# ═══════════════════════════════════════════
a_exp = 9.852  # experimental lattice parameter
sg = SpaceGroup("F-43m")
lattice = Lattice.cubic(a_exp)

# Wyckoff positions (conventional cell)
wyckoff = {
    'Li': [0.1766, 0.1766, 0.0224],   # 48h → 24 sites in conv
    'P':  [0.5, 0.5, 0.5],             # 4b → 4 sites
    'S_16e': [0.6205, 0.6205, 0.6205], # 16e → 16 sites (PS₄ 내부)
    'X_4c': [0.25, 0.25, 0.25],        # 4c → 4 sites (free anion)
    'X_4a': [0.0, 0.0, 0.0],           # 4a → 4 sites (free anion)
}

def get_orbits(pos):
    orbits = sg.get_orbit(np.array(pos))
    unique = []
    for c in orbits:
        c_mod = np.mod(c, 1.0)
        if not any(np.allclose(c_mod, u, atol=0.01) for u in unique):
            unique.append(c_mod)
    return unique

Li_sites = get_orbits(wyckoff['Li'])
P_sites = get_orbits(wyckoff['P'])
S16e_sites = get_orbits(wyckoff['S_16e'])
X4c_sites = get_orbits(wyckoff['X_4c'])
X4a_sites = get_orbits(wyckoff['X_4a'])

print(f"Li(48h): {len(Li_sites)} sites")
print(f"P(4b):   {len(P_sites)} sites")
print(f"S(16e):  {len(S16e_sites)} sites")
print(f"X(4c):   {len(X4c_sites)} sites")
print(f"X(4a):   {len(X4a_sites)} sites")

# ═══════════════════════════════════════════
# 2. Halogen enumerate
# Li₆PS₅Cl: per f.u. = 1 Cl + 1 S on free sites (4a+4c)
# Conventional cell (4 f.u.): 8 free sites, 4 Cl + 4 S
# ═══════════════════════════════════════════
free_sites = X4c_sites + X4a_sites  # 8 sites total
n_free = len(free_sites)
n_Cl = 4  # 4 Cl per conv cell

# All combinations of choosing 4 sites for Cl
configs = list(combinations(range(n_free), n_Cl))
print(f"\nHalogen configs: C({n_free},{n_Cl}) = {len(configs)}")

# ═══════════════════════════════════════════
# 3. Build structures + MLIP screening
# ═══════════════════════════════════════════
predictor = pretrained_mlip.get_predict_unit("uma-s-1p1", device="cuda")
calc = FAIRChemCalculator(predictor, task_name="omat")
adaptor = AseAtomsAdaptor()

results = []

for idx, cl_indices in enumerate(configs):
    # Build structure
    species = []
    coords = []

    # Li
    for c in Li_sites:
        species.append('Li')
        coords.append(c)
    # P
    for c in P_sites:
        species.append('P')
        coords.append(c)
    # S (16e)
    for c in S16e_sites:
        species.append('S')
        coords.append(c)
    # Free sites: Cl or S
    for i, c in enumerate(free_sites):
        if i in cl_indices:
            species.append('Cl')
        else:
            species.append('S')
        coords.append(c)

    struct = Structure(lattice, species, coords)
    atoms = adaptor.get_atoms(struct)
    atoms.calc = calc

    # MLIP relax
    try:
        opt = LBFGS(atoms, logfile=None)
        opt.run(fmax=0.01, steps=200)
    except:
        pass

    e = atoms.get_potential_energy()
    e_per_atom = e / len(atoms)

    cl_pos = [free_sites[i] for i in cl_indices]
    cl_site_types = []
    for i in cl_indices:
        if i < len(X4c_sites):
            cl_site_types.append('4c')
        else:
            cl_site_types.append('4a')

    results.append({
        'idx': idx,
        'energy': e,
        'e_per_atom': e_per_atom,
        'cl_indices': list(cl_indices),
        'cl_sites': cl_site_types,
        'n_4c_Cl': cl_site_types.count('4c'),
        'n_4a_Cl': cl_site_types.count('4a'),
    })

    if idx % 10 == 0:
        print(f"  config {idx}/{len(configs)}: E={e:.4f} eV, 4c_Cl={cl_site_types.count('4c')}, 4a_Cl={cl_site_types.count('4a')}", flush=True)

# Sort by energy
results.sort(key=lambda x: x['energy'])

print(f"\n{'='*60}")
print(f"Top 5 configurations:")
print(f"{'='*60}")
for r in results[:5]:
    print(f"  #{r['idx']:3d}: E={r['energy']:.4f} eV ({r['e_per_atom']:.6f}/atom), 4c_Cl={r['n_4c_Cl']}, 4a_Cl={r['n_4a_Cl']}")

print(f"\nBottom 5:")
for r in results[-5:]:
    print(f"  #{r['idx']:3d}: E={r['energy']:.4f} eV, 4c_Cl={r['n_4c_Cl']}, 4a_Cl={r['n_4a_Cl']}")

print(f"\nEnergy spread: {(results[-1]['energy'] - results[0]['energy'])*1000:.1f} meV")

# Save best config
best = results[0]
print(f"\n★ Best config: #{best['idx']}, 4c_Cl={best['n_4c_Cl']}, 4a_Cl={best['n_4a_Cl']}")

# Save results
with open('halogen_screening_results.json', 'w') as f:
    json.dump(results, f, indent=2)

# ═══════════════════════════════════════════
# 4. Li annealing on best config (500K, 100ps)
# ═══════════════════════════════════════════
print(f"\n{'='*60}")
print(f"Step 2: Li annealing (500K, 100ps) on best config")
print(f"{'='*60}")

# Rebuild best structure
species_best = []
coords_best = []
for c in Li_sites:
    species_best.append('Li'); coords_best.append(c)
for c in P_sites:
    species_best.append('P'); coords_best.append(c)
for c in S16e_sites:
    species_best.append('S'); coords_best.append(c)
for i, c in enumerate(free_sites):
    if i in best['cl_indices']:
        species_best.append('Cl')
    else:
        species_best.append('S')
    coords_best.append(c)

struct_best = Structure(lattice, species_best, coords_best)
atoms_best = adaptor.get_atoms(struct_best)
atoms_best.calc = calc

# Record pre-annealing positions
pos_before = atoms_best.get_positions().copy()
sp_list = atoms_best.get_chemical_symbols()

# Annealing
print("  Annealing 500K, 100ps...", flush=True)
MaxwellBoltzmannDistribution(atoms_best, temperature_K=500)
dyn = Langevin(atoms_best, 1.0*units.fs, temperature_K=500, friction=0.01)
dyn.run(100000)  # 100ps

# Quench
print("  Quench 300K, 10ps...", flush=True)
Langevin(atoms_best, 1.0*units.fs, temperature_K=300, friction=0.05).run(10000)

# Final relax
print("  Final MLIP relax...", flush=True)
try:
    LBFGS(atoms_best, logfile=None).run(fmax=0.005, steps=300)
except:
    pass

e_after = atoms_best.get_potential_energy()
print(f"  E before annealing: {best['energy']:.4f} eV")
print(f"  E after annealing:  {e_after:.4f} eV")
print(f"  ΔE = {(e_after - best['energy'])*1000:.1f} meV")

# Check displacement by element
pos_after = atoms_best.get_positions().copy()
print(f"\n  Displacement by element:")
for elem in ['Li', 'P', 'S', 'Cl']:
    disps = []
    for i in range(len(sp_list)):
        if sp_list[i] == elem:
            d = np.linalg.norm(pos_after[i] - pos_before[i])
            disps.append(d)
    if disps:
        arr = np.array(disps)
        print(f"    {elem:4s}: mean={arr.mean():.3f} Å, max={arr.max():.3f} Å")

# Save annealed structure
from ase.io import write
write('comp1_lpscl_v2_annealed.xyz', atoms_best)
# Also save as CIF
struct_annealed = adaptor.get_structure(atoms_best)
struct_annealed.to('comp1_lpscl_v2_annealed.cif')

print(f"\n★ Saved: comp1_lpscl_v2_annealed.xyz/.cif")
print(f"★ Next: MLIP EOS → DFT relax → DFT EOS")
