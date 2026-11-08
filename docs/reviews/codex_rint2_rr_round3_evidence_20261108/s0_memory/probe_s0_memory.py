"""Independent small synthetic SELF-155 audit. No real data, host, solver or S0 CLI.
Usage: python -I -B probe_s0_memory.py <package/repo> <result.json>
"""
import hashlib
import importlib
import json
import sys
from pathlib import Path

import numpy as np
import scipy
from scipy.spatial import cKDTree

repo = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(repo / 'scripts'))
cj = importlib.import_module('carbon_junction')
s0 = importlib.import_module('ca_s0_census')
tc = importlib.import_module('test_carbon_junction')
tc.CJ = cj
tc.S3 = importlib.import_module('step3_sigma')
results = {'python': sys.version, 'numpy': np.__version__, 'scipy': scipy.__version__,
           'pin': '17d45fb9cdfc7033bdfd41509527cea23ba1654c',
           'scope': 'small synthetic local functions only; no host/research data',
           'sources': {n: hashlib.sha256((repo/'scripts'/n).read_bytes()).hexdigest()
                       for n in ('carbon_junction.py','ca_s0_census.py','test_carbon_junction.py')},
           'checks': [], 'failures': []}

def check(name, ok, **detail):
    results['checks'].append(dict(name=name, ok=bool(ok), **detail))
    if not ok:
        results['failures'].append(name)

def dist_point(x, a, b):
    # Independent scalar projection formula, one point/segment.
    d = b-a
    q = float(d@d)
    t = 0.0 if q == 0 else max(0.0, min(1.0, float((x-a)@d)/q))
    return float(np.linalg.norm(x-(a+t*d)))

old_budget = cj._PAIR_ENTRY_BUDGET
rng = np.random.default_rng(806119)
pair_runs = ball_runs = truth_count = 0
max_sub_ratio = 0.0
for case in range(36):
    n = 24
    scale = (0.01, 0.1, 1., 10.)[case % 4]
    shift = (0., 1e6, -1e6)[case % 3]
    a = rng.normal(size=(n,3))*scale + shift
    b = a + rng.normal(size=(n,3))*scale * 0.1
    b[:2] = a[:2] + rng.normal(size=(2,3))*scale*9.0
    b[2:4] = a[2:4] # point segments
    if case % 2 == 0:
        a[5:8] = a[4]; b[5:8] = b[4] # duplicates
    D = scale*0.2
    ii,jj = np.triu_indices(n,1)
    d1 = cj.seg_seg_closest(a[ii],b[ii],a[jj],b[jj])[0]
    d2 = cj.seg_seg_closest(a[jj],b[jj],a[ii],b[ii])[0]
    truth = {(int(i),int(j)) for i,j,d,e in zip(ii,jj,d1,d2) if d<=D or e<=D}
    truth_count += len(truth)
    # Deliberately use different limits from resident tests, including one-row queries.
    for budget in (1,11,53,4_000_000):
        cj._PAIR_ENTRY_BUDGET = budget
        for L in (None, scale*0.35, scale*3.1):
            got = cj._near_seg_pairs(a,b,D,tag='independent',L0=L)
            pairs = [tuple(x) for x in got.tolist()]
            ok = truth.issubset(set(pairs)) and pairs == sorted(set(pairs)) and all(i<j for i,j in pairs)
            check(f'pair_case{case}_budget{budget}_L{L}',ok,truth=len(truth),candidates=len(pairs))
            pair_runs += 1
            if L is None:
                max_sub_ratio = max(max_sub_ratio,cj._PAIR_SEARCH_LAST['independent']['n_subpieces']/n)
    x = rng.normal(size=(13,3))*scale+shift
    rad = np.linspace(0.,scale*0.7,len(x))
    true_ball = {(q,s) for q in range(len(x)) for s in range(n) if dist_point(x[q],a[s],b[s])<=rad[q]}
    for budget in (1,17,4_000_000):
        cj._PAIR_ENTRY_BUDGET = budget
        q,s = cj._ball_seg_candidates(x,rad,a,b,tag='independent_ball')
        got = list(zip(q.tolist(),s.tolist()))
        check(f'ball_case{case}_budget{budget}',true_ball.issubset(set(got)) and got==sorted(set(got)),
              truth=len(true_ball),candidates=len(got))
        ball_runs += 1
cj._PAIR_ENTRY_BUDGET = old_budget
results['candidate_summary'] = dict(segment_queries=pair_runs, ball_queries=ball_runs,
                                    true_segment_pairs_over_36_beds=truth_count,max_default_subpieces_per_segment=max_sub_ratio)

# Reproduce the declared boundary exception without an old source module:
# old query_pairs radius from old arithmetic; final distance from current unchanged primitive.
P0=np.array([[.3,0,0],[.3+1.1+.2,0,0]])
P1=np.array([[.3+1.1,0,0],[.3+2*1.1+.2,0,0]])
D=.2
rad=float(np.linalg.norm(P1-P0,axis=1).max())+D
mid=.5*(P0+P1)
old=cKDTree(mid).query_pairs(rad,output_type='ndarray')
new=cj._near_seg_pairs(P0,P1,D)
d=float(cj.seg_seg_closest(P0[:1],P1[:1],P0[1:],P1[1:])[0][0])
check('declared_boundary_exception',len(old)==0 and new.tolist()==[[0,1]] and d<=D,
      distance=d,old_radius=rad,midpoint_distance=float(np.linalg.norm(mid[0]-mid[1])),old_pairs=old.tolist(),new_pairs=new.tolist())

# Resident tie fixture, independently permuted with 32 different seeds and varied chunks.
segs=tc._tie_segs()
base=cj._distinct_instances(segs,tc.TIE_D,tc.TIE_T)
pr=cj._near_seg_pairs(segs['P0'],segs['P1'],tc.TIE_D)
old_constants=(cj._CLOSEST_CHUNK,cj._TOUCH_ENTRY_BUDGET)
for seed in range(32):
    cj._CLOSEST_CHUNK=(1,3,8,100)[seed%4]
    cj._TOUCH_ENTRY_BUDGET=(1,5,19,100)[seed%4]
    perm=pr[np.random.default_rng(seed+1108).permutation(len(pr))]
    got=cj._distinct_from_pairs(segs,perm,tc.TIE_D,tc.TIE_T)
    diff=tc._deq(base,got)
    check(f'tie_order_{seed}',not diff,differences=diff)
cj._CLOSEST_CHUNK,cj._TOUCH_ENTRY_BUDGET=old_constants
results['tie_summary']={'canonical_keys':tc._tie_key(base),'Ci':base['Ci'].tolist(),'n_candidate_pairs':len(pr)}

# Exact point/segment boundary and outside cutoff behavior in callers, not just candidate search.
paths=[(0,[np.array([[0.,0.,0.],[1.,0.,0.]])])]
x=np.array([[.5,.5,0.],[.5,np.nextafter(.5,np.inf),0.],[.5,0.,0.]])
got=s0._min_dist_to_segments(x,paths,.5)
check('caller_min_dist_cutoff',got[0]==.5 and np.isinf(got[1]) and got[2]==0.,distance=[None if not np.isfinite(v) else float(v) for v in got])
check('zero_length_pair_candidates',cj._near_seg_pairs(np.zeros((4,3)),np.zeros((4,3)),0.).tolist()==[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]])
results['summary']={'checks':len(results['checks']),'failed':len(results['failures'])}
out=Path(sys.argv[2]);out.write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(results['summary'])); print('evidence='+str(out))
sys.exit(1 if results['failures'] else 0)
