"""Independent sufficient-condition stress near decimal decade rollover; no source edits."""
import sys,json
from pathlib import Path
E=Path(__file__).resolve().parent;C=E.parent/'candidate';W=E.parent.parent
sys.path[:0]=[str(C/'scripts'),str(W/'lhs_coverage_review_20260930/deps')]
import numpy as np
import lhs_descriptor_harvest as h
rng=np.random.default_rng(9312026)
n=500000
# Permitted producer intervals L,H (already include E). Concentrate one mutated
# endpoint within +/- 10 ppm of a decade, ratios near 1% and interior cases.
rat=rng.uniform(1.0,1.0102,n)
rat[:n//2]=rng.uniform(1.00998,1.01011,n//2)
target=10.0**rng.integers(-12,1,n)*rng.uniform(1-1e-5,1+1e-5,n)
L=target/1.01;H=L*rat
L[n//2:]=target[n//2:]/(.99*rat[n//2:]);H[n//2:]=L[n//2:]*rat[n//2:]
hp=np.maximum(h._half_unit(1.01*L),h._half_unit(1.01*H))
hm=np.maximum(h._half_unit(.99*L),h._half_unit(.99*H))
det=(1.01*L-2*hp>H)&(.99*H+2*hm<L)
fail=[];tested=0
for factor in (1.01,.99):
    mn,mx=factor*L[det],factor*H[det]
    ld,hd=L[det],H[det]
    values=[mn,mx,(mn+mx)/2]
    # Include values on both sides of every possible decade boundary in each
    # narrow interval, not just endpoints (token interval is not monotone there).
    decade=10.**np.ceil(np.log10(mn))
    values.extend([decade,decade*(1-1e-7),decade*(1+1e-7)])
    for v in values:
        valid=(v>=mn)&(v<=mx)
        tokens=np.array([float(format(x,'.6g')) for x in v])
        hh=h._half_unit(tokens)
        miss=valid&~((tokens-hh>hd)|(tokens+hh<ld))
        tested+=int(valid.sum())
        for j in np.flatnonzero(miss)[:5]:
            fail.append(dict(L=float(ld[j]),H=float(hd[j]),factor=factor,value=float(v[j]),token=float(tokens[j]),half=float(hh[j])))
R=dict(seed=9312026,intervals=n,detect_intervals=int(det.sum()),mutated_values_checked=tested,misses=fail,
       limitation='Tests the sufficient-condition inequality for synthetic intervals, not new physical geometry or proof of every input')
(E/'power_boundary_results.json').write_text(json.dumps(R,indent=2),encoding='utf-8')
print(json.dumps(R,indent=2))
