"""comp3 v2 — Stage 1a (45 S placements, all-Cl, Li_rep).
Independent script: exits 0 if cache_stage1a.json exists or after successful save.
Time: ~5 min (45 LBFGS x ~6s each)."""
import sys, json, time
from pathlib import Path
from itertools import combinations
from ase.optimize import LBFGS
from comp5_v2_lib import (load_ref, get_li_configs, build, new_calc,
                           get_adaptor, jx, COMP_NAME)

CACHE = Path('cache_stage1a.json')
if CACHE.exists():
    print(f"[{COMP_NAME}] Stage 1a already done — {CACHE} exists. Exit 0.")
    sys.exit(0)

t0 = time.time()
ref, li, p, sfw, free = load_ref()
li_configs = get_li_configs(len(li))
li_rep = li_configs[0]
print(f"[{COMP_NAME}] Stage 1a START — 45 S placements")

s_configs = list(combinations(range(len(free)), 2))
results = []
adaptor = get_adaptor()
for idx, s_idx in enumerate(s_configs):
    cl_only = [i for i in range(len(free)) if i not in s_idx]
    s = build(ref, li, p, sfw, free, list(s_idx), cl_only, [], li_rep)
    a = adaptor.get_atoms(s); a.calc = new_calc()
    try: LBFGS(a, logfile=None).run(fmax=0.01, steps=200)
    except: pass
    e = float(a.get_potential_energy())
    results.append({'idx': idx, 's_idx': list(s_idx), 'E': e})
    print(f"  {idx+1}/45: S={list(s_idx)} E={e:.4f}", flush=True)

json.dump(results, open(CACHE, 'w'), default=jx)
elapsed = (time.time() - t0) / 60
print(f"[{COMP_NAME}] Stage 1a DONE ({elapsed:.1f} min) → {CACHE}")
