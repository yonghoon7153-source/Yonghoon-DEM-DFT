"""comp3 v2 — Stage 2: best halogen × 20 Li trials → cache_stage2.json.
Time: ~5 min (20 LBFGS x ~15s)."""
import sys, json, time
from pathlib import Path
from ase.optimize import LBFGS
from comp5_v2_lib import (load_ref, get_li_configs, build, new_calc,
                           get_adaptor, jx, COMP_NAME)

CACHE = Path('cache_stage2.json')
if CACHE.exists():
    print(f"[{COMP_NAME}] Stage 2 already done — exit 0."); sys.exit(0)

S1B_CACHE = Path('cache_stage1b.json')
if not S1B_CACHE.exists():
    print(f"ERROR: {S1B_CACHE} not found. Run stage1b chunks + merge first."); sys.exit(2)

t0 = time.time()
ref, li, p, sfw, free = load_ref()
li_configs = get_li_configs(len(li))

h_results = json.load(open(S1B_CACHE))
h_results.sort(key=lambda r: r['E'])
best = h_results[0]
best_s = best['s_idx']; best_cl = best['cl']; best_br = best['br']
print(f"[{COMP_NAME}] Stage 2 START — best halogen S={best_s} Cl={best_cl} Br={best_br}")

adaptor = get_adaptor()
li_results = []
for idx, li_idx in enumerate(li_configs):
    s = build(ref, li, p, sfw, free, best_s, best_cl, best_br, li_idx)
    a = adaptor.get_atoms(s); a.calc = new_calc()
    try: LBFGS(a, logfile=None).run(fmax=0.01, steps=200)
    except: pass
    e = float(a.get_potential_energy())
    li_results.append({'li_trial': idx, 'li_idx': li_idx, 'E': e})
    print(f"  Li{idx:2d}/20: E={e:.4f}", flush=True)

li_results.sort(key=lambda r: r['E'])
spread = (li_results[-1]['E'] - li_results[0]['E']) * 1000

cache2 = {
    'best_s': best_s, 'best_cl': best_cl, 'best_br': best_br,
    'li_spread_meV': spread,
    'stage1b_halogen_top10': h_results[:10],
    'stage2_li_top20': li_results,
}
json.dump(cache2, open(CACHE, 'w'), default=jx)
elapsed = (time.time() - t0) / 60
print(f"[{COMP_NAME}] Stage 2 DONE ({elapsed:.1f} min, Li spread {spread:.1f} meV) → {CACHE}")
print(f"[{COMP_NAME}] Next: run anneal_rank.py 0|1|2|3|4 for Stage 3.")
