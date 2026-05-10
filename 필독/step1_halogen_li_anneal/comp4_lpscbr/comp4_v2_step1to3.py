"""comp4 v2 (Li5.4 PS4.4 Cl0.8 Br0.8) — Pipeline v2 Steps 1-3.
Stage 1a: 45 S placements × all-Cl × Li_rep -> top 5 S
Stage 1b: top 5 S × 70 Cl/Br configs × Li_rep -> top 1 (S, halogen)
Stage 2:  top 1 halogen × 20 Li -> top 5
Stage 3:  top 5 × anneal 500K 100ps + quench -> champion
"""
import numpy as np, json, time
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

predictor = pretrained_mlip.get_predict_unit("uma-s-1p1", device="cuda")
adaptor = AseAtomsAdaptor()
def new_calc(): return FAIRChemCalculator(predictor, task_name="omat")

t0 = time.time()
def t(): return f"[{(time.time()-t0)/3600:.2f}h]"

ref = Structure.from_file('ref_comp3.cif')
print(f"{t()} Reference: {ref.composition}, {len(ref)} atoms", flush=True)

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

n_li = len(li_sites)
print(f"{t()} Li={n_li}, P={len(p_sites)}, S_PS4={len(s_framework)}, Free={len(free_sites)}", flush=True)

n_li_select = 27
rng = np.random.RandomState(42)
Li_configs = [sorted(rng.choice(n_li, n_li_select, replace=False).tolist()) for _ in range(20)]
li_rep = Li_configs[0]

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

# Stage 1a
print(f"\n=== Stage 1a: 45 S placements (all-Cl) ===", flush=True)
s_configs = list(combinations(range(len(free_sites)), 2))
s_results = []
for idx, s_idx in enumerate(s_configs):
    cl_only = [i for i in range(len(free_sites)) if i not in s_idx]
    s = build(list(s_idx), cl_only, [], li_rep)
    a = adaptor.get_atoms(s); a.calc = new_calc()
    try: LBFGS(a, logfile=None).run(fmax=0.01, steps=200)
    except: pass
    e = a.get_potential_energy()
    s_results.append({'idx': idx, 's_idx': list(s_idx), 'E': e})
    print(f"{t()}  Stage1a {idx+1}/45: S={list(s_idx)} E={e:.4f}", flush=True)
s_results.sort(key=lambda r: r['E'])
top5_s = [r['s_idx'] for r in s_results[:5]]
print(f"\n{t()} Top 5 S:", flush=True)
for i, r in enumerate(s_results[:5]):
    print(f"  rank{i}: S={r['s_idx']} E={r['E']:.4f}", flush=True)

# Stage 1b
print(f"\n=== Stage 1b: top 5 S × 70 Cl/Br = 350 LBFGS ===", flush=True)
halogen_perms = list(combinations(range(8), 4))
h_results = []; total = 5*70; done = 0
for s_rank, s_idx in enumerate(top5_s):
    print(f"\n{t()} --- S rank{s_rank} = {s_idx} ---", flush=True)
    remaining = [i for i in range(len(free_sites)) if i not in s_idx]
    for h_idx, cl_local in enumerate(halogen_perms):
        cl = [remaining[j] for j in cl_local]
        br = [remaining[j] for j in range(8) if j not in cl_local]
        s = build(s_idx, cl, br, li_rep)
        a = adaptor.get_atoms(s); a.calc = new_calc()
        try: LBFGS(a, logfile=None).run(fmax=0.01, steps=200)
        except: pass
        e = a.get_potential_energy()
        h_results.append({'s_rank': s_rank, 's_idx': s_idx, 'cl': cl, 'br': br, 'E': e, 'h_idx': h_idx})
        done += 1
        if done % 5 == 0 or done == total:
            print(f"{t()}   Stage1b {done}/{total}: S{s_rank} h{h_idx} Cl={cl} Br={br} E={e:.4f}", flush=True)

h_results.sort(key=lambda r: r['E'])
print(f"\n{t()} Top 5 (S, halogen):", flush=True)
for i, r in enumerate(h_results[:5]):
    print(f"  rank{i}: S{r['s_rank']}={r['s_idx']} Cl={r['cl']} Br={r['br']} E={r['E']:.4f}", flush=True)
best = h_results[0]
best_s, best_cl, best_br = best['s_idx'], best['cl'], best['br']
print(f"\n{t()} Best halogen: S={best_s} Cl={best_cl} Br={best_br}", flush=True)

# Stage 2
print(f"\n=== Stage 2: best halogen × 20 Li ===", flush=True)
li_results = []
for idx, li in enumerate(Li_configs):
    s = build(best_s, best_cl, best_br, li)
    a = adaptor.get_atoms(s); a.calc = new_calc()
    try: LBFGS(a, logfile=None).run(fmax=0.01, steps=200)
    except: pass
    e = a.get_potential_energy()
    li_results.append({'li_trial': idx, 'li_idx': li, 'E': e})
    print(f"{t()}  Stage2 Li{idx:2d}/20: E={e:.4f}", flush=True)
li_results.sort(key=lambda r: r['E'])
spread = (li_results[-1]['E'] - li_results[0]['E']) * 1000
print(f"\n{t()} Li spread: {spread:.1f} meV. Top 5:", flush=True)
for r in li_results[:5]:
    print(f"  Li{r['li_trial']:2d}: E={r['E']:.4f}", flush=True)

# Stage 3
print(f"\n=== Stage 3: top 5 × anneal 500K 100ps ===", flush=True)
anneal_results = []
for rank, r in enumerate(li_results[:5]):
    s = build(best_s, best_cl, best_br, r['li_idx'])
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
    anneal_results.append({'rank': rank, 'li_trial': r['li_trial'], 'e_before': e_before, 'e_after': e_after})
    write(f'comp4_v2_anneal_rank{rank}.xyz', a)
    print(f"{t()}   E_after={e_after:.4f} (dE={(e_after-e_before)*1000:.0f} meV)", flush=True)
anneal_results.sort(key=lambda x: x['e_after'])
champ = anneal_results[0]
print(f"\n{t()} CHAMPION: rank{champ['rank']} Li{champ['li_trial']} E={champ['e_after']:.4f}", flush=True)

import shutil
shutil.copy(f'comp4_v2_anneal_rank{champ["rank"]}.xyz', 'comp4_v2_champion.xyz')

def jx(x):
    if isinstance(x, np.ndarray): return x.tolist()
    if isinstance(x, (np.integer,)): return int(x)
    if isinstance(x, (np.floating,)): return float(x)
    return x

with open('comp4_v2_results.json', 'w') as f:
    json.dump({'best_s': best_s, 'best_cl': best_cl, 'best_br': best_br, 'li_spread_meV': spread,
               'stage1a_S_top10': s_results[:10], 'stage1b_halogen_top10': h_results[:10],
               'stage2_li_top10': li_results[:10], 'stage3_anneal': anneal_results,
               'champion': champ, 'total_h': (time.time()-t0)/3600}, f, indent=2, default=jx)
print(f"\n{t()} DONE. Total: {(time.time()-t0)/3600:.1f}h", flush=True)
