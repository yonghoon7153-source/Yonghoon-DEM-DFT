"""Search the decimal-decade rollover missed by h(pre-rounded value)."""
import sys,json,math
from pathlib import Path
E=Path(__file__).resolve().parent;C=E.parent/'candidate';W=E.parent.parent
sys.path[:0]=[str(C/'scripts'),str(W/'lhs_coverage_review_20260930/deps')]
import numpy as np
from scipy.optimize import root
import lhs_descriptor_harvest as h
q=lambda x:float(format(x,'.6g'))
targetlo=(1e-7-1e-14)/1.01;targethi=1e-7-3e-13
def interval(a,b,dl):
    lo,hi,*_=h._area_enclosure([a],[b],[dl]);ee,_=h._producer_error_bound([a],[b],[dl])
    return lo[0]-ee[0],hi[0]+ee[0]
def eq(z,dl):
    a,b=z*.001
    try:lo,hi=interval(a,b,dl)
    except Exception:return np.array([1e3,1e3])
    return np.array([(lo-targetlo)/1e-7,(hi-lo-(targethi-targetlo))/1e-9])
best=[];found=None;start=np.array([2.39,1.6463])
for j in range(4000):
    dl=.00320+j*1e-8
    sol=root(eq,start,args=(dl,),tol=1e-10)
    if not sol.success or np.linalg.norm(eq(sol.x,dl))>1e-5:continue
    start=sol.x
    a,b=map(q,sol.x*.001);dl=q(dl)
    lo,hi=interval(a,b,dl)
    metric=abs(1.01*lo-(1e-7-1e-14))+abs(hi-(1e-7-3e-13))
    if len(best)<3 or metric<best[-1]['metric']:
        best.append(dict(a=a,b=b,dl=dl,lo=lo,hi=hi,metric=metric,continuous=sol.x.tolist()))
        best=sorted(best,key=lambda x:x['metric'])[:3]
    # Max derivative signs: near internal containment gr1 < 0, gr2 > 0, gd < 0.
    bx=h._token_box(a,b,dl)
    for aa in (a-float(h._half_unit(a))*.99999,a+float(h._half_unit(a))*.99999):
        for bb in (b-float(h._half_unit(b))*.99999,b+float(h._half_unit(b))*.99999):
            for dd in (dl-float(h._half_unit(dl))*.99999,dl+float(h._half_unit(dl))*.99999):
                ap,dp=h.producer_area_binary64(aa,bb,aa+bb-dd)
                if (q(aa),q(bb),q(dp))!=(a,b,dl):continue
                good=h._contact_area_rows([a],[b],[dl],[q(ap)])
                if not good[5]['detect_1pct'][0]:continue
                bad=h._contact_area_rows([a],[b],[dl],[q(ap*1.01)])
                if not bad[4][0]:
                    found=dict(a=a,b=b,dl=dl,truth=[aa,bb,dd],ap=ap,dp=dp,normal=q(ap),mutant=q(ap*1.01),lo=lo,hi=hi,
                       good_beyond=bool(good[4][0]),detect=bool(good[5]['detect_1pct'][0]),bad_beyond=bool(bad[4][0]),
                       h_pre=float(h._half_unit(ap*1.01)),h_post=float(h._half_unit(q(ap*1.01))),search_j=j)
                    break
            if found:break
        if found:break
    if found:break
R=dict(found=found,best=best,iterations=j+1)
(E/'decimal_boundary_search.json').write_text(json.dumps(R,indent=2),encoding='utf-8')
print(json.dumps(R,indent=2))
