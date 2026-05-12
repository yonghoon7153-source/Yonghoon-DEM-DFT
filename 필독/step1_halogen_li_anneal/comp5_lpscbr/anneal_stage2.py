"""anneal_stage2.py — Stage 2 (20 Li) for one halogen rank.
Output: cache_stage2_rank{RANK}.json (best halogen + top 20 Li).
Time: ~5 min. Fits any walltime.

For RANK=0: detects existing cache_stage2.json (made by stage2.py), uses it.

Usage: python anneal_stage2.py <rank>
"""
import sys, json, time
from pathlib import Path
from itertools import combinations
from ase.optimize import LBFGS

RANK = int(sys.argv[1])
COMP_NAME = sys.argv[2] if len(sys.argv) > 2 else 'comp'

CACHE = Path(f'cache_stage2_rank{RANK}.json')
if CACHE.exists():
    print(f"[stage2_rank{RANK}] already done — exit 0"); sys.exit(0)

# Rank 0 shortcut: cache_stage2.json (from stage2.py) is rank 0
if RANK == 0 and Path('cache_stage2.json').exists():
    d = json.load(open('cache_stage2.json'))
    json.dump(d, open(CACHE, 'w'), indent=2)
    print(f"[stage2_rank0] copied from cache_stage2.json"); sys.exit(0)

# Otherwise compute Stage 2 for this rank
import numpy as np
from pymatgen.core import Structure
from pymatgen.io.ase import AseAtomsAdaptor
from fairchem.core import pretrained_mlip
from fairchem.core.calculate.ase_calculator import FAIRChemCalculator

predictor = pretrained_mlip.get_predict_unit("uma-s-1p1", device="cuda")
adaptor = AseAtomsAdaptor()
def new_calc(): return FAIRChemCalculator(predictor, task_name="omat")

# Reload reference
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

h_results = json.load(open('cache_stage1b.json'))
h_results.sort(key=lambda r: r['E'])
if RANK >= len(h_results):
    print(f"ERROR: RANK {RANK} out of range"); sys.exit(2)
target = h_results[RANK]
print(f"[stage2_rank{RANK}] target: S={target['s_idx']} Cl={target['cl']} Br={target['br']} E={target['E']:.4f}")

t0 = time.time()
li_results = []
for idx, li in enumerate(Li_configs):
    s = build(target['s_idx'], target['cl'], target['br'], li)
    a = adaptor.get_atoms(s); a.calc = new_calc()
    try: LBFGS(a, logfile=None).run(fmax=0.01, steps=200)
    except: pass
    e = float(a.get_potential_energy())
    li_results.append({'li_trial': idx, 'li_idx': li, 'E': e})
    print(f"  Li{idx:2d}/20: E={e:.4f}", flush=True)
li_results.sort(key=lambda r: r['E'])
spread = (li_results[-1]['E'] - li_results[0]['E']) * 1000

json.dump({
    'rank': RANK,
    'best_s': target['s_idx'], 'best_cl': target['cl'], 'best_br': target['br'],
    'halogen_E': target['E'],
    'li_spread_meV': spread,
    'stage2_li_top20': li_results,
}, open(CACHE, 'w'), indent=2,
   default=lambda x: x.tolist() if hasattr(x,'tolist') else x)
print(f"[stage2_rank{RANK}] DONE ({(time.time()-t0)/60:.1f} min, spread {spread:.1f} meV)")
