"""anneal_rank.py — comp5 v2 Stage 2+3 for halogen rank N.

SPAWNED FROM comp4 anneal_rank.py — only filenames changed (comp4_v2_* -> comp5_v2_*).

Usage: python anneal_rank.py 1   (run rank 1 halogen)
       python anneal_rank.py 2   (run rank 2)
       python anneal_rank.py 3
       python anneal_rank.py 4

Loads cache_stage1b.json from initial run.
Output: comp5_v2_rank{N}_anneal_{0-4}.xyz, comp5_v2_rank{N}_results.json
"""
import sys, json, time, shutil
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
from pathlib import Path

if len(sys.argv) < 2:
    print("Usage: python anneal_rank.py <rank>  (rank=1,2,3,4)")
    sys.exit(1)
RANK = int(sys.argv[1])
print(f"=== Running Stage 2+3 for halogen rank {RANK} ===")

predictor = pretrained_mlip.get_predict_unit("uma-s-1p1", device="cuda")
adaptor = AseAtomsAdaptor()
def new_calc(): return FAIRChemCalculator(predictor, task_name="omat")

t0 = time.time()
def t(): return f"[{(time.time()-t0)/3600:.2f}h]"

# Load reference
ref = Structure.from_file('ref_comp3.cif')
li_sites, p_sites, s_framework, free_sites = [], [], [], []
for site in ref:
    sp = str(site.specie); fc = site.frac_coords
    if sp == 'Li': li_sites.append(fc)
    elif sp == 'P': p_sites.append(fc)
    else:
        p_coords = np.array(p_sites) if p_sites else np.zeros((1,3))
        dists = ref.lattice.get_all_distances(fc.reshape(1,-1), p_coords)[0]
        if sp == 'S' and len(p_sites) > 0 and min(dists) < 2.5:
            s_framework.append(fc)
        else:
            free_sites.append(fc)

n_li = len(li_sites); n_li_select = 27
rng = np.random.RandomState(42)
Li_configs = [sorted(rng.choice(n_li, n_li_select, replace=False).tolist()) for _ in range(20)]

def build(s_idx, cl_idx, br_idx, li_idx):
    species, coords = [], []
    for i in li_idx: species.append('Li'); coords.append(li_sites[i])
    for c in p_sites: species.append('P'); coords.append(c)
    for c in s_framework: species.append('S'); coords.append(c)
    for i, c in enumerate(free_sites):
        if i in s_idx: species.append('S')
        elif i in cl_idx: species.append('Cl')
        elif i in br_idx: species.append('Br')
        else: species.append('Cl')
        coords.append(c)
    return Structure(ref.lattice, species, coords)

# Load Stage 1b cache
S1B = Path('cache_stage1b.json')
if not S1B.exists():
    print("ERROR: cache_stage1b.json not found. Run main script first.")
    sys.exit(1)
h_results = json.load(open(S1B))
h_results.sort(key=lambda r: r['E'])

if RANK >= len(h_results):
    print(f"ERROR: rank {RANK} out of range (max={len(h_results)-1})")
    sys.exit(1)

target = h_results[RANK]
print(f"{t()} Target rank {RANK}: S={target['s_idx']} Cl={target['cl']} Br={target['br']} E={target['E']:.4f}")

# Stage 2: rank N halogen × 20 Li
print(f"\n=== Stage 2: rank{RANK} halogen × 20 Li ===")
li_results = []
for li_trial, li in enumerate(Li_configs):
    s = build(target['s_idx'], target['cl'], target['br'], li)
    a = adaptor.get_atoms(s); a.calc = new_calc()
    try: LBFGS(a, logfile=None).run(fmax=0.01, steps=200)
    except: pass
    e = a.get_potential_energy()
    li_results.append({'li_trial': li_trial, 'li_idx': li, 'E': float(e)})
    print(f"{t()}  Li{li_trial:2d}/20: E={e:.4f}", flush=True)

li_results.sort(key=lambda r: r['E'])
spread = (li_results[-1]['E'] - li_results[0]['E']) * 1000
print(f"\n{t()} Li spread: {spread:.1f} meV")

# Stage 3: top 5 × anneal
print(f"\n=== Stage 3: top 5 × anneal 500K 100ps ===")
anneal_results = []
for rank, r in enumerate(li_results[:5]):
    s = build(target['s_idx'], target['cl'], target['br'], r['li_idx'])
    a = adaptor.get_atoms(s); a.calc = new_calc()
    e_before = a.get_potential_energy()
    print(f"\n{t()} Rank {rank} (Li{r['li_trial']}): E_init={e_before:.4f}", flush=True)
    print(f"{t()}   500K 100ps...", flush=True)
    MaxwellBoltzmannDistribution(a, temperature_K=500)
    Langevin(a, 1.0*units.fs, temperature_K=500, friction=0.01).run(100000)
    print(f"{t()}   300K 10ps quench...", flush=True)
    Langevin(a, 1.0*units.fs, temperature_K=300, friction=0.05).run(10000)
    print(f"{t()}   LBFGS relax...", flush=True)
    try: LBFGS(a, logfile=None).run(fmax=0.005, steps=300)
    except: pass
    e_after = a.get_potential_energy()
    anneal_results.append({'rank': rank, 'li_trial': r['li_trial'],
                            'e_before': float(e_before), 'e_after': float(e_after)})
    write(f'comp5_v2_rank{RANK}_anneal_{rank}.xyz', a)
    print(f"{t()}   E_after={e_after:.4f} (dE={(e_after-e_before)*1000:.0f} meV)", flush=True)

anneal_results.sort(key=lambda x: x['e_after'])
champ = anneal_results[0]
print(f"\n{t()} Rank{RANK} CHAMPION: rank{champ['rank']} Li{champ['li_trial']} E={champ['e_after']:.4f}")

shutil.copy(f'comp5_v2_rank{RANK}_anneal_{champ["rank"]}.xyz',
             f'comp5_v2_rank{RANK}_champion.xyz')

with open(f'comp5_v2_rank{RANK}_results.json', 'w') as f:
    def jx(x):
        if isinstance(x, np.ndarray): return x.tolist()
        if isinstance(x, (np.integer,)): return int(x)
        if isinstance(x, (np.floating,)): return float(x)
        return x
    json.dump({
        'rank': RANK,
        'halogen': {'s_idx': target['s_idx'], 'cl': target['cl'], 'br': target['br'], 'E_lbfgs': target['E']},
        'stage2_li': li_results,
        'stage3_anneal': anneal_results,
        'champion': champ,
        'total_h': (time.time()-t0)/3600,
    }, f, indent=2, default=jx)

print(f"\n{t()} DONE rank{RANK}. Total: {(time.time()-t0)/3600:.1f}h")
