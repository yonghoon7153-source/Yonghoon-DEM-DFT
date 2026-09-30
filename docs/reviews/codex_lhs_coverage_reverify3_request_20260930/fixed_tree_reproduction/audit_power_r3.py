"""Codex audit_power.py 의 R3 판 — 같은 탐색 (seed 4813) 을 새 키로: '+1 % 치환을 놓치면서 검출 보증 (n_detect_1pct) 1' 인 행이 있는가 (있으면 안 된다).
원본은 없앤 키 n_power_1pct 를 읽어 KeyError — 의도된 제거 (LHSC-04 R3b).  Codex 431 번째 상자의 정상 · +1 % 토큰 결과도 그대로 적는다."""
import sys, json, random, itertools
from pathlib import Path
E=Path(__file__).resolve().parent; C=E.parent/'candidate'
sys.path[:0]=[str(C/'scripts')]
import numpy as np
import lhs_descriptor_harvest as h
import lens_geometry as lg
q=lambda x:float(format(x,'.6g'))
args=lambda a,b:(np.array([1,2]),np.array(['AM','SE']),np.array([a,b]),np.array([1]),np.array([2]))
def chk(a,b,dl,v):
    return h.contact_area_check(*args(a,b),np.array([v]),np.array([dl]),np.array([0]))['all']
# ① Codex 반례 토큰 그대로
cx=(0.00348428,0.00164629,0.00328959)
R={'codex_431_box':{'tokens':cx,'correct_token':chk(*cx,5.81675e-8),'mutant_token':chk(*cx,5.87492e-8)}}
# ② 같은 탐색 — 보증 1 인데 치환을 놓치는 행 (있으면 반례)
rng=random.Random(4813); found=None; n_guar=n_miss_guar=0; boxes=0
for i in range(50000):
    a=q(rng.uniform(.001,.009)); b=q(a*rng.uniform(.15,.9)); dl=q(2*b*(1-rng.uniform(.0001,.002)))
    lo,hi,lb,how=h._area_enclosure(np.array([a]),np.array([b]),np.array([dl]))
    if lo[0]<=0: continue
    boxes+=1
    hs=[float(h._half_unit(v)) for v in (a,b,dl)]
    for w in itertools.product((-0.999999,0.999999),repeat=3):
        point=[v+hw*s for v,hw,s in zip((a,b,dl),hs,w)]
        if list(map(q,point))!=[a,b,dl]: continue
        truth=lg.intersection_disc_area(*point)
        correct=q(truth); mp=q(1.01*truth); mm=q(0.99*truth)
        o=chk(a,b,dl,correct); p=chk(a,b,dl,mp); m=chk(a,b,dl,mm)
        if o['n_detect_1pct']==1:
            n_guar+=1
            if p['n_beyond_tol']==0 or m['n_beyond_tol']==0:
                n_miss_guar+=1
                if found is None: found=dict(iteration=i,point=point,tokens=[a,b,dl],correct=o,plus=p,minus=m)
        if o['n_detect_1pct']!=p['n_detect_1pct'] or o['n_wide_enclosure']!=p['n_wide_enclosure'] or o['n_detect_1pct']!=m['n_detect_1pct']:
            found=found or dict(iteration=i,tokens=[a,b,dl],note='classification depends on A_dump',correct=o,plus=p,minus=m)
        break
R['search']=dict(seed=4813,iterations=50000,boxes_with_positive_lo=boxes,guaranteed_rows=n_guar,guaranteed_but_missed=n_miss_guar,counterexample=found)
(E/'power_results_r3.json').write_text(json.dumps(R,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'codex_431_box':{k:{kk:v[kk] for kk in ('n_tested','n_beyond_tol','n_wide_enclosure','n_detect_1pct','n_producer_uncertified')} for k,v in R['codex_431_box'].items() if k!='tokens'},'search':{k:v for k,v in R['search'].items() if k!='counterexample'},'counterexample':bool(found)},ensure_ascii=False,indent=1))
