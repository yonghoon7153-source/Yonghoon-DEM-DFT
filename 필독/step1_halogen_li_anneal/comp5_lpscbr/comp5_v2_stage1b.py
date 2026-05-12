"""comp3 v2 — Stage 1b ONE chunk.
Usage: python comp3_v2_stage1b.py 0|1|2
  chunk 0: jobs 0-99
  chunk 1: jobs 100-199
  chunk 2: jobs 200-279
Each chunk ~20-25 min (100 LBFGS x ~12-15s). Fits 2h walltime safely."""
import sys, json, time
from pathlib import Path
from itertools import combinations
from ase.optimize import LBFGS
from comp5_v2_lib import (load_ref, get_li_configs, build, new_calc,
                           get_adaptor, jx, COMP_NAME, N_CL)

if len(sys.argv) < 2:
    print("Usage: python comp3_v2_stage1b.py <chunk 0|1|2>"); sys.exit(1)
CHUNK = int(sys.argv[1])

CHUNK_SIZES = [100, 100, 80]   # sum = 280 for comp3 (5 × C(8,5)=56)
assert 0 <= CHUNK < len(CHUNK_SIZES)

CACHE = Path(f'cache_stage1b_c{CHUNK}.json')
if CACHE.exists():
    print(f"[{COMP_NAME}] Stage 1b chunk {CHUNK} already done — exit 0."); sys.exit(0)

# Need Stage 1a results
S1A_CACHE = Path('cache_stage1a.json')
if not S1A_CACHE.exists():
    print(f"ERROR: {S1A_CACHE} not found. Run stage1a first."); sys.exit(2)

t0 = time.time()
ref, li, p, sfw, free = load_ref()
li_configs = get_li_configs(len(li))
li_rep = li_configs[0]
s_results = json.load(open(S1A_CACHE))
s_results.sort(key=lambda r: r['E'])
top5_s = [r['s_idx'] for r in s_results[:5]]

halogen_perms = list(combinations(range(8), N_CL))
total = 5 * len(halogen_perms)
assert sum(CHUNK_SIZES) == total, f"chunk sums {sum(CHUNK_SIZES)} != total {total}"

# Build flat job list
jobs = []
for s_rank, s_idx in enumerate(top5_s):
    for h_idx, cl_local in enumerate(halogen_perms):
        jobs.append((s_rank, s_idx, h_idx, cl_local))

lo = sum(CHUNK_SIZES[:CHUNK])
hi = lo + CHUNK_SIZES[CHUNK]
print(f"[{COMP_NAME}] Stage 1b chunk {CHUNK} (jobs {lo}-{hi-1}, n={hi-lo}) START")

adaptor = get_adaptor()
results = []
for jidx in range(lo, hi):
    s_rank, s_idx, h_idx, cl_local = jobs[jidx]
    remaining = [i for i in range(len(free)) if i not in s_idx]
    cl = [remaining[j] for j in cl_local]
    br = [remaining[j] for j in range(8) if j not in cl_local]
    s = build(ref, li, p, sfw, free, s_idx, cl, br, li_rep)
    a = adaptor.get_atoms(s); a.calc = new_calc()
    try: LBFGS(a, logfile=None).run(fmax=0.01, steps=200)
    except: pass
    e = float(a.get_potential_energy())
    results.append({'s_rank': s_rank, 's_idx': list(s_idx), 'h_idx': h_idx,
                    'cl': cl, 'br': br, 'E': e, 'job': jidx})
    if (jidx - lo + 1) % 5 == 0 or jidx == hi-1:
        print(f"  job {jidx+1}/{total}: S{s_rank} h{h_idx} Cl={cl} Br={br} E={e:.4f}",
              flush=True)

json.dump(results, open(CACHE, 'w'), default=jx)
elapsed = (time.time() - t0) / 60
print(f"[{COMP_NAME}] Stage 1b chunk {CHUNK} DONE ({elapsed:.1f} min) → {CACHE}")
