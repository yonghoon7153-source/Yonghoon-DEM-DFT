"""Independent Decimal geometry oracle, interval sampling, and production-entry checks."""
import os, sys, math, json, itertools, random
from decimal import Decimal, localcontext
from pathlib import Path
from collections import Counter
E=Path(__file__).resolve().parent; C=E.parent/'candidate'; W=E.parent.parent
sys.path[:0]=[str(C/'scripts'),str(W/'lhs_coverage_review_20260930/deps')]
import numpy as np
import lhs_descriptor_harvest as h
import lens_geometry as lg
PI=Decimal('3.141592653589793238462643383279502884197169399375105820974944592307816406286208998628')
q=lambda v:float(format(v,'.6g'))
def exact(a,b,dl):
    # Independent circle-intersection equation, Decimal 80 arithmetic.
    with localcontext() as ctx:
        ctx.prec=80
        a,b,dl=[v if isinstance(v,Decimal) else Decimal.from_float(float(v)) for v in (a,b,dl)]
        d=a+b-dl
        if dl<=0 or d<=0 or d<=abs(a-b): return Decimal(0)
        plane=(d*d+a*a-b*b)/(2*d)
        return max(Decimal(0),PI*(a*a-plane*plane))
def bounds(a,b,dl):
    lo,hi,lb0,how=h._area_enclosure(*[np.array([v]) for v in (a,b,dl)])
    return dict(lo=float(lo[0]),hi=float(hi[0]),lower_bound_flag=bool(lb0[0]),method=str(how[0]))
def check(a,b,dl,area):
    return h.contact_area_check(np.array([1,2]),np.array(['AM','SE']),np.array([a,b]),
       np.array([1]),np.array([2]),np.array([area]),np.array([dl]),np.array([0]))
def record(a,b,dl,area):
    return dict(input=[a,b,dl,area],exact_at_tokens=str(exact(a,b,dl)),enclosure=bounds(a,b,dl),diagnostic=check(a,b,dl,area))
R={}
true=(.0012345649,.0012345551,.00246909)
area=lg.intersection_disc_area(*true)
R['old_R2_counterexample']=record(*map(q,true),q(area))
R['old_R2_counterexample']['truth']=dict(input=true,decimal80_area=str(exact(*true)),actual_area=area)
old=json.loads((W/'lhs_coverage_reverify_evidence_20260930/prior_audit_results.json').read_text(encoding='utf-8'))
R['old_examples']={
    'rounding':record(*old['rounding_only_false_alarm']['rounded_r1_r2_delta_area']),
    'hertz_deep':record(.0005,.0005,.000999999,old['hertz_miss']['hertz_dump']),
    '3e-5_deep':record(.0005,.0005,.000999999,old['3e-5_miss_deep']['dump'])}
R['boundary_controls']={
    'noncontact_zero':record(.001,.001,0.,0.),
    'negative_delta_zero':record(.001,.001,-.0001,0.),
    'noncontact_positive':record(.001,.001,0.,1e-6),
    'strict_containment_zero':record(.002,.001,.0021,0.),
    'tiny_positive_delta':record(.001,.001,1e-20,0.)}

rng=random.Random(20260930)
methods=Counter(); violations=[]; float_violations=[]; lb_mislabels=[]
regions=Counter(); points=0
for j in range(12000):
    a=10**rng.uniform(-6,-1)
    b=a*10**rng.uniform(-2,2)
    mode=j%8
    if mode==0: dl=min(a,b)*10**rng.uniform(-12,-.1)
    elif mode==1: dl=2*min(a,b)*rng.uniform(.01,.999999)
    elif mode==2: dl=2*min(a,b)*(1+rng.uniform(-1e-4,1e-4))
    elif mode==3:
        b=a*(1+rng.uniform(-1e-5,1e-5)); dl=(a+b)*(1-10**rng.uniform(-12,-4))
    elif mode==4: dl=a+b-math.sqrt(abs(a*a-b*b))*(1+rng.uniform(-1e-4,1e-4))
    elif mode==5: dl=-min(a,b)*10**rng.uniform(-12,0)
    elif mode==6: dl=2*min(a,b)*rng.uniform(1.001,2.0)
    else: dl=min(a,b)*rng.uniform(0,2)
    a,b,dl=map(q,(a,b,dl))
    en=bounds(a,b,dl); methods[en['method']]+=1; regions[str(mode)]+=1
    # The contract box is centered on float tokens with exact Decimal half-unit;
    # use decimal endpoints so endpoint creation cannot hide an outward-bound error.
    vals=[Decimal.from_float(v) for v in (a,b,dl)]
    hs=[Decimal.from_float(float(h._half_unit(v))) for v in (a,b,dl)]
    ptset=list(itertools.product((-1,1),repeat=3))
    ptset.extend(tuple(rng.uniform(-1,1) for _ in range(3)) for _ in range(16))
    for weights in ptset:
        p=[v+dx*Decimal.from_float(float(w)) for v,dx,w in zip(vals,hs,weights)]
        truth=exact(*p); points+=1
        if not Decimal.from_float(en['lo'])<=truth<=Decimal.from_float(en['hi']):
            if len(violations)<20: violations.append(dict(tokens=[a,b,dl],point=list(map(str,p)),exact=str(truth),enclosure=en))
        f=lg.intersection_disc_area(*map(float,p))
        if not en['lo']<=f<=en['hi']:
            if len(float_violations)<20:float_violations.append(dict(tokens=[a,b,dl],point=list(map(str,p)),value=f,enclosure=en))
    if en['lo']==0 and not en['lower_bound_flag'] and len(lb_mislabels)<8:
        lb_mislabels.append(dict(tokens=[a,b,dl],enclosure=en))
R['independent_stress']=dict(seed=20260930,boxes=12000,points=points,regions=dict(regions),methods=dict(methods),
    decimal80_violations=violations,actual_float_violations=float_violations,
    sampling_limitation='A finite adversarial sample, not a proof of all binary64 inputs',zero_lower_bound_flag_false_examples=lb_mislabels)
R['clean_import_physics_present']='plastic_coverage' in sys.modules
(E/'geometry_results.json').write_text(json.dumps(R,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in R.items() if k not in ['old_examples','boundary_controls']},ensure_ascii=False,indent=2))
