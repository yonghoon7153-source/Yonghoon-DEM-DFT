"""
Pipeline v2 Step 1: Li₆PS₅Cl
Halogen enumerate (4a/4c S/Cl) × Li enumerate (48h 중 24개)
→ MLIP relax screening → best config → Li annealing
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
import json

# ═══════════════════════════════════════════
# 1. Build sites
# ═══════════════════════════════════════════
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

Li48h_sites = get_orbits([0.1766, 0.1766, 0.0224])  # 48 sites
P_sites = get_orbits([0.5, 0.5, 0.5])                # 4 sites
S16e_sites = get_orbits([0.6205, 0.6205, 0.6205])    # 16 sites
X4c_sites = get_orbits([0.25, 0.25, 0.25])            # 4 sites
X4a_sites = get_orbits([0.0, 0.0, 0.0])               # 4 sites

print(f"Li(48h): {len(Li48h_sites)} sites → 24개 선택 필요")
print(f"P(4b):   {len(P_sites)}")
print(f"S(16e):  {len(S16e_sites)}")
print(f"X(4c):   {len(X4c_sites)}")
print(f"X(4a):   {len(X4a_sites)}")

# ═══════════════════════════════════════════
# 2. Halogen enumerate
# 8 free sites (4c+4a), 4 Cl + 4 S
# ═══════════════════════════════════════════
free_sites = X4c_sites + X4a_sites
n_Cl = 4
halogen_configs = list(combinations(range(8), n_Cl))
print(f"\nHalogen configs: C(8,4) = {len(halogen_configs)}")

# ═══════════════════════════════════════════
# 3. Li enumerate: 48 sites 중 24개 선택
# C(48,24) = 12억 → 불가능!
# 대안: random 20개 Li 배열 시도
# ═══════════════════════════════════════════
n_Li_configs = 20
rng = np.random.RandomState(42)
Li_configs = []
for i in range(n_Li_configs):
    indices = rng.choice(48, 24, replace=False)
    Li_configs.append(sorted(indices.tolist()))

print(f"Li configs: {n_Li_configs} random selections")
print(f"Total: {len(halogen_configs)} × {n_Li_configs} = {len(halogen_configs)*n_Li_configs} configs")
print(f"→ 너무 많으면 halogen top5 × Li 20 = 100개로 축소")

# ═══════════════════════════════════════════
# 4. Two-stage screening
# Stage 1: Halogen screening (Li 고정, 1개 대표 Li config)
# Stage 2: Li screening (best halogen 고정, 20 Li configs)
# ═══════════════════════════════════════════
predictor = pretrained_mlip.get_predict_unit("uma-s-1p1", device="cuda")
calc = FAIRChemCalculator(predictor, task_name="omat")
adaptor = AseAtomsAdaptor()

def build_structure(halogen_idx, li_indices):
    """Build Li6PS5Cl structure"""
    species = []
    coords = []
    # Li (24개만!)
    for i in li_indices:
        species.append('Li')
        coords.append(Li48h_sites[i])
    # P
    for c in P_sites:
        species.append('P')
        coords.append(c)
    # S (16e)
    for c in S16e_sites:
        species.append('S')
        coords.append(c)
    # Free sites
    for i, c in enumerate(free_sites):
        if i in halogen_idx:
            species.append('Cl')
        else:
            species.append('S')
        coords.append(c)
    return Structure(lattice, species, coords)

# Stage 1: Halogen screening (대표 Li config = config 0)
print(f"\n{'='*60}")
print(f"Stage 1: Halogen screening ({len(halogen_configs)} configs)")
print(f"{'='*60}")

li_rep = Li_configs[0]  # 대표 Li 배열
halogen_results = []

for idx, cl_idx in enumerate(halogen_configs):
    struct = build_structure(cl_idx, li_rep)
    atoms = adaptor.get_atoms(struct)
    atoms.calc = calc
    try:
        opt = LBFGS(atoms, logfile=None)
        opt.run(fmax=0.01, steps=200)
    except:
        pass
    e = atoms.get_potential_energy()

    cl_types = ['4c' if i < 4 else '4a' for i in cl_idx]
    halogen_results.append({
        'idx': idx, 'energy': e, 'cl_indices': list(cl_idx),
        'n_4c': cl_types.count('4c'), 'n_4a': cl_types.count('4a')
    })
    if idx % 10 == 0:
        print(f"  config {idx}/{len(halogen_configs)}: E={e:.4f} eV, 4c={cl_types.count('4c')}, 4a={cl_types.count('4a')}", flush=True)

halogen_results.sort(key=lambda x: x['energy'])
print(f"\nTop 5 halogen configs:")
for r in halogen_results[:5]:
    print(f"  #{r['idx']}: E={r['energy']:.4f}, 4c_Cl={r['n_4c']}, 4a_Cl={r['n_4a']}")

best_halogen = halogen_results[0]['cl_indices']
print(f"\n★ Best halogen: 4c_Cl={halogen_results[0]['n_4c']}, 4a_Cl={halogen_results[0]['n_4a']}")

# Stage 2: Li screening (best halogen 고정, 20 Li configs)
print(f"\n{'='*60}")
print(f"Stage 2: Li screening ({n_Li_configs} configs)")
print(f"{'='*60}")

li_results = []
for idx, li_idx in enumerate(Li_configs):
    struct = build_structure(best_halogen, li_idx)
    atoms = adaptor.get_atoms(struct)
    atoms.calc = calc
    try:
        opt = LBFGS(atoms, logfile=None)
        opt.run(fmax=0.01, steps=200)
    except:
        pass
    e = atoms.get_potential_energy()
    li_results.append({'idx': idx, 'energy': e, 'li_indices': li_idx})
    print(f"  Li config {idx}/{n_Li_configs}: E={e:.4f} eV", flush=True)

li_results.sort(key=lambda x: x['energy'])
print(f"\nTop 5 Li configs:")
for r in li_results[:5]:
    print(f"  #{r['idx']}: E={r['energy']:.4f}")

best_li = li_results[0]['li_indices']
E_spread = (li_results[-1]['energy'] - li_results[0]['energy']) * 1000
print(f"\nLi energy spread: {E_spread:.1f} meV")
print(f"★ Best Li config: #{li_results[0]['idx']}")

# ═══════════════════════════════════════════
# 5. Li annealing on best config (500K, 100ps)
# ═══════════════════════════════════════════
print(f"\n{'='*60}")
print(f"Stage 3: Li annealing (500K, 100ps)")
print(f"{'='*60}")

struct_best = build_structure(best_halogen, best_li)
atoms_best = adaptor.get_atoms(struct_best)
atoms_best.calc = calc

print(f"  Structure: {len(atoms_best)} atoms")
pos_before = atoms_best.get_positions().copy()
sp_list = atoms_best.get_chemical_symbols()
e_before = atoms_best.get_potential_energy()

print(f"  E before: {e_before:.4f} eV")
print(f"  Annealing 500K, 100ps...", flush=True)
MaxwellBoltzmannDistribution(atoms_best, temperature_K=500)
dyn = Langevin(atoms_best, 1.0*units.fs, temperature_K=500, friction=0.01)
dyn.run(100000)

print(f"  Quench 300K, 10ps...", flush=True)
Langevin(atoms_best, 1.0*units.fs, temperature_K=300, friction=0.05).run(10000)

print(f"  Final relax...", flush=True)
try:
    LBFGS(atoms_best, logfile=None).run(fmax=0.005, steps=300)
except:
    pass

e_after = atoms_best.get_potential_energy()
print(f"  E after:  {e_after:.4f} eV")
print(f"  ΔE = {(e_after - e_before)*1000:.1f} meV")

# Displacement check
pos_after = atoms_best.get_positions().copy()
print(f"\n  Displacement by element:")
for elem in ['Li', 'P', 'S', 'Cl']:
    disps = []
    for i in range(len(sp_list)):
        if sp_list[i] == elem:
            disps.append(np.linalg.norm(pos_after[i] - pos_before[i]))
    if disps:
        arr = np.array(disps)
        print(f"    {elem:4s}: mean={arr.mean():.3f} Å, max={arr.max():.3f} Å")

# Save
from ase.io import write
write('comp1_v2_champion.xyz', atoms_best)
struct_final = adaptor.get_structure(atoms_best)
struct_final.to('comp1_v2_champion.cif')

print(f"\n{'='*60}")
print(f"★★★ CHAMPION STRUCTURE SAVED ★★★")
print(f"  comp1_v2_champion.xyz / .cif")
print(f"  {len(atoms_best)} atoms, E={e_after:.4f} eV")
print(f"  Next: MLIP EOS → DFT relax → DFT EOS")
print(f"{'='*60}")

# Save all results
with open('pipeline_v2_results.json', 'w') as f:
    json.dump({
        'halogen_results': halogen_results[:10],
        'li_results': li_results[:10],
        'best_halogen': best_halogen,
        'best_li': best_li,
        'e_before_anneal': e_before,
        'e_after_anneal': e_after,
    }, f, indent=2)
