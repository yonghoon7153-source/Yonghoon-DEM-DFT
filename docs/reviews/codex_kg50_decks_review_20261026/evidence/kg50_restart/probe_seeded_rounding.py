from pathlib import Path
import json, math

base=Path(__file__).resolve().parent
pdd=(base/'upstream_src_fix_particledistribution_discrete.cpp').read_text(encoding='utf-8')
rng=(base/'upstream_src_random.cpp').read_text(encoding='utf-8')
park=(base/'upstream_src_random_park.cpp').read_text(encoding='utf-8')
header=(base/'upstream_src_random_park.h').read_text(encoding='utf-8')
assert 'random = new RanPark(lmp, arg[3], true);' in pdd
assert 'const int offset = proc_shift ? multiplier*comm->me : 0;' in rng
assert 'int multiplier = 1' in header
assert '#define IA 16807' in park and '#define IM 2147483647' in park

def first_uniform(seed,rank):
    state=seed+rank
    k=state//127773
    state=16807*(state-k*127773)-2836*k
    if state<0: state+=2147483647
    return state/2147483647

def two_template_local(n,w,u):
    result=[int(n*w),int(n*(1-w))]
    remainders=[n*w-result[0],n*(1-w)-result[1]]
    gap=n-sum(result)
    assert gap in (0,1)
    if gap:
        j=0
        running=remainders[0]
        while running<u*gap and j<1:
            j+=1
            running+=remainders[j]
        result[j]+=1
    return result

n=312506
am=4850*.003**3
se=1640*.00035**3
w=(.85/am)/(.85/am+.15/se)
rankn=[n//56+int(rank<n%56) for rank in range(56)]
reproductions=[]
for seed in [11300017,32452867]:
    draws=[first_uniform(seed,rank) for rank in range(56)]
    counts=[two_template_local(nloc,w,u) for nloc,u in zip(rankn,draws)]
    reproductions.append(dict(pdd_seed=seed,NP=56,supplied_rank_totals=rankn,first_draw_min=min(draws),first_draw_max=max(draws),AM_remainder_min=min((x*w)%1 for x in rankn),AM_remainder_max=max((x*w)%1 for x in rankn),AM=sum(x[0] for x in counts),SE=sum(x[1] for x in counts),total=sum(sum(x) for x in counts)))
assert reproductions[0]['AM']==952
assert reproductions[1]['AM']==896
out={
 'method':'Source-guarded Python translation of first Park-Miller draw and two-template exact_number allocation. No C++/DEM execution.',
 'assumption':'Supply hypothetical equal-distribution local totals5580/5581 summing312506. Actual rank allocation may differ; successful placement is not asserted.',
 'finding':'Rank seeds shift by1; their first draws are strongly correlated. A fixed seed can repeatedly produce deficits, but another fixed seed produces surplus. Neither compulsory downward bias nor independent per-rank fluctuations follows from the source.',
 'cases':reproductions}
(base/'seeded_rounding_results.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out,indent=2))
