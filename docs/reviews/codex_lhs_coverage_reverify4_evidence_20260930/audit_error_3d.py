"""Three nonzero coordinate differences, Decimal90 oracle, pointwise E + token checks."""
import sys, math, random, json
from pathlib import Path
from decimal import Decimal as D, localcontext
E=Path(__file__).resolve().parent;C=E.parent/'candidate';W=E.parent.parent
sys.path[:0]=[str(C/'scripts'),str(W/'lhs_coverage_review_20260930/deps')]
import numpy as np
import lhs_descriptor_harvest as h
PI=D('3.141592653589793238462643383279502884197169399375105820974944592307816406286208998628')
rng=random.Random(309302026);q=lambda x:float(format(x,'.6g'))
rows=[];viol=[];worst=None;regions={str(k):0 for k in range(6)}
for j in range(18000):
    a=10**rng.uniform(-6,-1);b=a*10**rng.uniform(-3,3);m=j%6
    if m==0:dl=min(a,b)*10**rng.uniform(-11,-.1)
    elif m==1:dl=2*min(a,b)*rng.uniform(.01,.999999)
    elif m==2:dl=2*min(a,b)*(1+rng.uniform(-1e-6,1e-6))
    elif m==3:b=a;dl=2*a-a*10**rng.uniform(-13,-3)
    elif m==4:dl=-min(a,b)*rng.uniform(.01,1)
    else:dl=2*min(a,b)*rng.uniform(1.001,1.2)
    dist=a+b-dl
    if dist<=0:continue
    uv=[rng.uniform(.05,1)*rng.choice([-1,1]) for _ in range(3)];norm=math.sqrt(sum(v*v for v in uv))
    off=[dist*rng.uniform(-2,2) for _ in range(3)]
    xx=[o+dist*v/norm for o,v in zip(off,uv)]
    dv=[x-y for x,y in zip(xx,off)]
    rsq=dv[0]*dv[0]+dv[1]*dv[1]+dv[2]*dv[2];rd=math.sqrt(rsq)
    ap=-math.pi/4*((rd-a-b)*(rd+a-b)*(rd-a+b)*(rd+a+b))/rsq
    dp=a+b-rd
    with localcontext() as ctx:
        ctx.prec=90
        av,bv=D(a),D(b);dvv=[D(x)-D(y) for x,y in zip(xx,off)]
        dsq=sum(v*v for v in dvv);d=dsq.sqrt();dlv=av+bv-d
        ae=-PI/4*((d-av-bv)*(d+av-bv)*(d-av+bv)*(d+av+bv))/dsq
        vals=(dlv,2*av-dlv,2*bv-dlv,2*av+2*bv-dlv,d)
        errbound=h._producer_abs_error(*[(float(v),float(v)) for v in vals])
        err=abs(D(ap)-ae);ratio=float(err/D(errbound))
        rec=dict(r1=a,r2=b,x=xx,y=off,producer_area=ap,decimal90_area=str(ae),error=str(err),E=errbound,error_over_E=ratio)
        if worst is None or ratio>worst['error_over_E']:worst=rec
        if err>D(errbound):viol.append(rec)
    rows.append([q(a),q(b),q(dp),q(ap)]);regions[str(m)]+=1
arr=np.array(rows);a,b,dl,ad=arr.T
out=h._contact_area_rows(a,b,dl,ad);extra=out[5]
cert=(~extra['uncertified']) & (~extra['negative'])
det=extra['detect_1pct']
power={}
for factor in (1.01,.99):
    mut=np.array([q(float(v)*factor) for v in ad]);new=h._contact_area_rows(a,b,dl,mut)
    power[str(factor)]=dict(detection_misses=int((det & ~new[4]).sum()),classification_changes=int((det!=new[5]['detect_1pct']).sum()))
R=dict(seed=309302026,points=len(rows),regions=regions,pointwise_E_violations=viol,worst_point=worst,
    token_certified_nonnegative=int(cert.sum()),token_false_beyond=int((cert&out[4]).sum()),
    token_uncertified=int(extra['uncertified'].sum()),token_negative=int(extra['negative'].sum()),
    detect_1pct=int(det.sum()),power=power,limitation='Finite synthetic CPU sample; normal range, not installed native binary or global proof')
(E/'error_3d_results.json').write_text(json.dumps(R,indent=2),encoding='utf-8')
print(json.dumps(R,indent=2))
