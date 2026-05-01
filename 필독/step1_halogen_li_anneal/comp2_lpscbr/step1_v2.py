"""comp2 v2 (Li6PS5Cl0.5Br0.5): halogen enum (Cl=2, Br=2) + Li screen + 500K anneal

Mirrored from KISTI production: /scratch/x3430a02/kgy/manuscript_support/pipeline_v2/comp2_lpscbr/step1_v2.py
Verified 2026-05-01 (CODE_INVENTORY.md step 1-3).
"""
import json, numpy as np
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
print(f"sites: Li={len(Li48)} P={len(P_s)} S(16e)={len(S16e)} free={len(free)}")

# 20 random Li configs
rng = np.random.RandomState(42)
Li_configs = [sorted(rng.choice(48, 24, replace=False).tolist()) for _ in range(20)]
li_rep = Li_configs[0]

# Halogen enum: 2 Cl + 2 Br + 4 S in 8 free sites
halogen_configs = []
for cl in combinations(range(8), 2):
    rest = [i for i in range(8) if i not in cl]
    for br in combinations(rest, 2):
        halogen_configs.append((list(cl), list(br)))
print(f"halogen configs: {len(halogen_configs)}")

predictor = pretrained_mlip.get_predict_unit("uma-s-1p1", device="cuda")
calc = FAIRChemCalculator(predictor, task_name="omat")
adaptor = AseAtomsAdaptor()

def build(cl_idx, br_idx, li_idx):
    sp, co = [], []
    for i in li_idx: sp.append('Li'); co.append(Li48[i])
    for c in P_s:    sp.append('P');  co.append(c)
    for c in S16e:   sp.append('S');  co.append(c)
    for i, c in enumerate(free):
        sp.append('Cl' if i in cl_idx else ('Br' if i in br_idx else 'S'))
        co.append(c)
    return Structure(lat, sp, co)

# Stage 1: halogen screening (Li=rep)
print(f"\n=== Stage 1: halogen screening (Li=rep, {len(halogen_configs)} cfg) ===")
hresults = []
for idx, (cl, br) in enumerate(halogen_configs):
    s = build(cl, br, li_rep)
    a = adaptor.get_atoms(s); a.calc = calc
    try: LBFGS(a, logfile=None).run(fmax=0.01, steps=200)
    except: pass
    e = a.get_potential_energy()
    hresults.append({"idx": idx, "cl": cl, "br": br, "E": e})
    if idx % 20 == 0:
        print(f"  cfg {idx}/{len(halogen_configs)}: Cl={cl} Br={br} E={e:.4f}", flush=True)

hresults.sort(key=lambda r: r["E"])
top5_h = hresults[:5]
print(f"\nTop 5 halogen:")
for r in top5_h:
    print(f"  cfg{r['idx']:3d}: Cl={r['cl']} Br={r['br']}  E={r['E']:.4f}")
best_cl, best_br = top5_h[0]["cl"], top5_h[0]["br"]
print(f"★ best halogen: Cl={best_cl} Br={best_br}")

# Stage 2: Li screening (best halogen × 20 Li)
print(f"\n=== Stage 2: Li screening (best halogen × 20 Li) ===")
liresults = []
for idx, li in enumerate(Li_configs):
    s = build(best_cl, best_br, li)
    a = adaptor.get_atoms(s); a.calc = calc
    try: LBFGS(a, logfile=None).run(fmax=0.01, steps=200)
    except: pass
    e = a.get_potential_energy()
    liresults.append({"idx": idx, "li": li, "E": e})
    print(f"  Li{idx:2d}: E={e:.4f}", flush=True)
liresults.sort(key=lambda r: r["E"])
best_li = liresults[0]["li"]
spread = (liresults[-1]["E"] - liresults[0]["E"]) * 1000
print(f"\nLi spread: {spread:.1f} meV  ★ best Li #{liresults[0]['idx']}")

# Stage 3: 500K anneal on best config
print(f"\n=== Stage 3: anneal best (500K 100ps + 300K quench + relax) ===")
sb = build(best_cl, best_br, best_li)
a = adaptor.get_atoms(sb); a.calc = calc
print(f"  start atoms: {len(a)}  E_init={a.get_potential_energy():.4f}")
e_before = a.get_potential_energy()
pos_before = a.get_positions().copy(); sp_list = a.get_chemical_symbols()

print("  500K 100ps...", flush=True)
MaxwellBoltzmannDistribution(a, temperature_K=500)
Langevin(a, 1.0*units.fs, temperature_K=500, friction=0.01).run(100000)
print("  300K 10ps quench...", flush=True)
Langevin(a, 1.0*units.fs, temperature_K=300, friction=0.05).run(10000)
print("  LBFGS relax...", flush=True)
try: LBFGS(a, logfile=None).run(fmax=0.005, steps=300)
except: pass
e_after = a.get_potential_energy()
print(f"  E after: {e_after:.4f}  ΔE={(e_after-e_before)*1000:.1f} meV")

# displacement
pos_after = a.get_positions().copy()
print("  displacement:")
for elem in ['Li','P','S','Cl','Br']:
    d = [np.linalg.norm(pos_after[i]-pos_before[i]) for i in range(len(sp_list)) if sp_list[i]==elem]
    if d: print(f"    {elem:3s}: mean={np.mean(d):.3f}A max={np.max(d):.3f}A")

write('comp2_v2_champion.xyz', a)
adaptor.get_structure(a).to('comp2_v2_champion.cif')
print(f"\n★★★ CHAMPION saved: comp2_v2_champion.xyz / .cif ({len(a)} atoms, E={e_after:.4f}) ★★★")

with open('pipeline_v2_results.json', 'w') as f:
    json.dump({"halogen_top5": top5_h, "li_results": liresults, "best_cl": best_cl,
               "best_br": best_br, "best_li": best_li,
               "e_before_anneal": e_before, "e_after_anneal": e_after}, f, indent=2)
