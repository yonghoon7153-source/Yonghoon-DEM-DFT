"""
Model C (Li5.4PS4.4Cl1.6) Pipeline v2
Step 1: 45 halogen configs screening
Step 2: Top 5 halogen × 20 Li configs = 100 configs
Step 3: Overall top 5 → 500K annealing → champion
"""
import numpy as np
from pymatgen.core import Structure
from pymatgen.io.ase import AseAtomsAdaptor
from itertools import combinations
from ase import units
from ase.md.langevin import Langevin
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
from ase.optimize import LBFGS
from fairchem.core import pretrained_mlip
from fairchem.core.calculate.ase_calculator import FAIRChemCalculator
from ase.io import write
import json

predictor = pretrained_mlip.get_predict_unit("uma-s-1p1", device="cuda")
adaptor = AseAtomsAdaptor()

def new_calc():
    return FAIRChemCalculator(predictor, task_name="omat")

# ═══════════════════════════════════════════
# 1. Load reference structure + classify sites
# ═══════════════════════════════════════════
ref = Structure.from_file('/scratch/x3430a02/kgy/manuscript_support/comp3_lpsc10b06/configs/comp3_lpsc10b06_config_000.cif')
print(f"Reference: {ref.composition}, {len(ref)} atoms")

li_sites = []; p_sites = []; s_framework = []; free_sites = []

for i, site in enumerate(ref):
    sp = str(site.specie)
    fc = site.frac_coords
    if sp == 'Li':
        li_sites.append(fc)
    elif sp == 'P':
        p_sites.append(fc)
    else:
        # P와 거리로 PS4 내부 S 판별
        p_coords = np.array(p_sites) if p_sites else np.zeros((1,3))
        dists = ref.lattice.get_all_distances(fc.reshape(1,-1), p_coords)[0]
        if sp == 'S' and len(p_sites) > 0 and min(dists) < 2.5:
            s_framework.append(fc)
        else:
            free_sites.append(fc)

n_li = len(li_sites)
print(f"Li: {n_li}, P: {len(p_sites)}, S_fw: {len(s_framework)}, Free: {len(free_sites)}")

# ═══════════════════════════════════════════
# 2. Step 1: Halogen enumerate C(10,2)=45
# ═══════════════════════════════════════════
n_S_free = 2  # Model C: S 2개 on free sites, Cl 8개
halogen_configs = list(combinations(range(len(free_sites)), n_S_free))
print(f"\n{'='*60}")
print(f"Step 1: Halogen screening ({len(halogen_configs)} configs, Li fixed)")
print(f"{'='*60}")

halogen_results = []
for idx, s_idx in enumerate(halogen_configs):
    species = []; coords = []
    for c in li_sites: species.append('Li'); coords.append(c)
    for c in p_sites: species.append('P'); coords.append(c)
    for c in s_framework: species.append('S'); coords.append(c)
    for i, c in enumerate(free_sites):
        species.append('S' if i in s_idx else 'Cl'); coords.append(c)

    struct = Structure(ref.lattice, species, coords)
    atoms = adaptor.get_atoms(struct)
    atoms.calc = new_calc()
    try: LBFGS(atoms, logfile=None).run(fmax=0.01, steps=200)
    except: pass
    e = atoms.get_potential_energy()
    halogen_results.append({'idx': idx, 'energy': e, 's_indices': list(s_idx)})
    print(f"  {idx}/{len(halogen_configs)}: E={e:.4f}, S at {list(s_idx)}", flush=True)

halogen_results.sort(key=lambda x: x['energy'])
print(f"\nTop 5 halogen:")
for r in halogen_results[:5]:
    print(f"  #{r['idx']}: E={r['energy']:.4f}, S at {r['s_indices']}")

# ═══════════════════════════════════════════
# 3. Step 2: Top 5 halogen × 20 Li = 100 configs
# ═══════════════════════════════════════════
print(f"\n{'='*60}")
print(f"Step 2: Top 5 halogen × 20 Li = 100 configs")
print(f"{'='*60}")

n_li_select = 27  # Li5.4 × 5
rng = np.random.RandomState(42)
Li_configs = [sorted(rng.choice(n_li, n_li_select, replace=False).tolist()) for _ in range(20)]

all_li_results = []
for h_rank, h_res in enumerate(halogen_results[:5]):
    s_idx = h_res['s_indices']
    print(f"\n  --- Halogen #{h_res['idx']} (rank {h_rank}) ---", flush=True)

    for li_trial, li_select in enumerate(Li_configs):
        species = []; coords = []
        for i in li_select: species.append('Li'); coords.append(li_sites[i])
        for c in p_sites: species.append('P'); coords.append(c)
        for c in s_framework: species.append('S'); coords.append(c)
        for i, c in enumerate(free_sites):
            species.append('S' if i in s_idx else 'Cl'); coords.append(c)

        struct = Structure(ref.lattice, species, coords)
        atoms = adaptor.get_atoms(struct)
        atoms.calc = new_calc()
        try: LBFGS(atoms, logfile=None).run(fmax=0.01, steps=200)
        except: pass
        e = atoms.get_potential_energy()

        all_li_results.append({
            'h_rank': h_rank, 'h_idx': h_res['idx'], 's_indices': s_idx,
            'li_trial': li_trial, 'li_indices': li_select, 'energy': e
        })
        print(f"    H{h_rank}_Li{li_trial}: E={e:.4f}", flush=True)

all_li_results.sort(key=lambda x: x['energy'])
E_spread = (all_li_results[-1]['energy'] - all_li_results[0]['energy']) * 1000
print(f"\nOverall energy spread: {E_spread:.1f} meV")
print(f"\nTop 5 (halogen, Li) pairs:")
for r in all_li_results[:5]:
    print(f"  H{r['h_rank']}_Li{r['li_trial']}: E={r['energy']:.4f}, halogen={r['s_indices']}")

# ═══════════════════════════════════════════
# 4. Step 3: Top 1 → annealing (unified with comp1/comp2 protocol)
# ═══════════════════════════════════════════
print(f"\n{'='*60}")
print(f"Step 3: Top 1 annealing (500K, 100ps)")
print(f"{'='*60}")

anneal_results = []
for rank, r in enumerate(all_li_results[:1]):
    species = []; coords = []
    for i in r['li_indices']: species.append('Li'); coords.append(li_sites[i])
    for c in p_sites: species.append('P'); coords.append(c)
    for c in s_framework: species.append('S'); coords.append(c)
    for i, c in enumerate(free_sites):
        species.append('S' if i in r['s_indices'] else 'Cl'); coords.append(c)

    struct = Structure(ref.lattice, species, coords)
    atoms = adaptor.get_atoms(struct)
    atoms.calc = new_calc()

    e_before = atoms.get_potential_energy()
    MaxwellBoltzmannDistribution(atoms, temperature_K=500)
    Langevin(atoms, 1*units.fs, temperature_K=500, friction=0.01).run(100000)
    Langevin(atoms, 1*units.fs, temperature_K=300, friction=0.05).run(10000)
    try: LBFGS(atoms, logfile=None).run(fmax=0.005, steps=300)
    except: pass
    e_after = atoms.get_potential_energy()

    anneal_results.append({
        'rank': rank, 'h_rank': r['h_rank'], 'li_trial': r['li_trial'],
        'e_before': e_before, 'e_after': e_after
    })
    write(f'modelC_v2_champion.xyz', atoms)
    print(f"  Champion (H{r['h_rank']}_Li{r['li_trial']}): "
          f"{e_before:.4f} → {e_after:.4f} (dE={(e_after-e_before)*1000:.0f} meV)", flush=True)

champ = anneal_results[0]
print(f"\n★ Champion: H{champ['h_rank']}_Li{champ['li_trial']}")
print(f"  E = {champ['e_after']:.4f} eV")

with open('modelC_v2_results.json', 'w') as f:
    json.dump({'halogen': halogen_results[:10], 'li_top': all_li_results[:20],
               'anneal': anneal_results}, f, indent=2)

print(f"\n{'='*60}")
print(f"★★★ Model C v2 COMPLETE ★★★")
print(f"Next: MLIP EOS → DFT EOS")
print(f"{'='*60}")
