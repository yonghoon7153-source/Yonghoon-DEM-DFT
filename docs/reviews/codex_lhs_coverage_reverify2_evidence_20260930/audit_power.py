"""Does a row labelled n_power_1pct actually reject a +1% substitution?"""
import sys, json, random, itertools
from pathlib import Path
E=Path(__file__).resolve().parent; C=E.parent/'candidate'; W=E.parent.parent
sys.path[:0]=[str(C/'scripts'),str(W/'lhs_coverage_review_20260930/deps')]
import numpy as np
import lhs_descriptor_harvest as h
import lens_geometry as lg
q=lambda x:float(format(x,'.6g'))
rng=random.Random(4813)
found=None
for i in range(50000):
    a=q(rng.uniform(.001,.009)); b=q(a*rng.uniform(.15,.9))
    dl=q(2*b*(1-rng.uniform(.0001,.002)))
    lo,hi,lb,how=h._area_enclosure(np.array([a]),np.array([b]),np.array([dl]))
    if lo[0]<=0 or not (.0097<(hi[0]-lo[0])/lo[0]<.0102):continue
    hs=[float(h._half_unit(v)) for v in (a,b,dl)]
    for w in itertools.product((-0.999999,0.999999),repeat=3):
        point=[v+hw*s for v,hw,s in zip((a,b,dl),hs,w)]
        if list(map(q,point))!=[a,b,dl]:continue
        truth=lg.intersection_disc_area(*point)
        correct=q(truth); mutant=q(1.01*truth)
        args=(np.array([1,2]),np.array(['AM','SE']),np.array([a,b]),np.array([1]),np.array([2]))
        def chk(v):return h.contact_area_check(*args,np.array([v]),np.array([dl]),np.array([0]))
        original=chk(correct); mutated=chk(mutant)
        if original['all']['n_beyond_tol']==0 and mutated['all']['n_beyond_tol']==0 and mutated['all']['n_power_1pct']==1:
            found=dict(iteration=i,point=point,tokens=[a,b,dl],true_area=truth,correct_token=correct,mutant_token=mutant,
                actual_relative_change=mutant/truth-1,enclosure=dict(lo=float(lo[0]),hi=float(hi[0]),method=str(how[0])),
                correct=original,mutated=mutated)
            break
    if found:break
R=dict(seed=4813,attempted=i+1,counterexample=found)
(E/'power_results.json').write_text(json.dumps(R,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({**{k:v for k,v in R.items() if k!='counterexample'},'counterexample':{k:v for k,v in found.items() if k not in ('correct','mutated')} if found else None,
    'correct_summary':found['correct']['all'] if found else None,'mutated_summary':found['mutated']['all'] if found else None},ensure_ascii=False,indent=2))
