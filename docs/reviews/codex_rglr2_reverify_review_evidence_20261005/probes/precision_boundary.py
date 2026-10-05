"""Independent half-grid and adjacent-float checks; no solver or temperature fit."""
from pathlib import Path
from fractions import Fraction as F
import sys,json,math,numpy as np
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/'source/scripts'))
from tau_flux import ion_record_problem,sigma_identity_tol
import se_material
rates=[.003]+[se_material.sigma_grain_S_cm(t,e) for t in (-30.,25.,60.,120.) for e in (.29,.41,.46)]
counts=dict(positive=0,rounded_zero=0,positive_rejected=0,zero_accepted=0)
worst=dict(ratio=-1)
errors=[]
for s0 in rates:
 for k in (0,1,2,10,49,50,100,999,10000,400387,9999999,149999999):
  half=(k+.5)*1e-8
  for q0 in (math.nextafter(half,0.),half,math.nextafter(half,math.inf)):
   for cast in (float,np.float64):
    q,sd=float(round(cast(q0),8)),float(round(cast(q0)*s0*1000,6))
    rec=dict(sigma_full_status='computed',sigma_full=q,sigma_full_mScm=sd,percolating_fraction=1.,sigma_grain_S_cm=s0)
    problem=ion_record_problem(rec)
    if q<=0 or sd<=0:
     counts['rounded_zero']+=1;counts['zero_accepted']+=problem is None;continue
    counts['positive']+=1
    if problem:
     counts['positive_rejected']+=1;errors.append(dict(rec=rec,problem=problem))
    exact_diff=abs(F(sd)-1000*F(s0)*F(q))
    tol=sigma_identity_tol(s0,q,sd);rat=float(exact_diff)/tol
    if rat>worst['ratio']:worst=dict(ratio=rat,exact_diff=float(exact_diff),tolerance=tol,rec=rec)
base=dict(sigma_full_status='computed',sigma_full=.00400388,sigma_full_mScm=.012012,percolating_fraction=1.,sigma_grain_S_cm=.003)
t=sigma_identity_tol(.003,base['sigma_full'],base['sigma_full_mScm'])
c=1000*.003*base['sigma_full']
inside=dict(base,sigma_full_mScm=c+.999*t);outside=dict(base,sigma_full_mScm=c+1.001*t)
out=dict(counts=counts,worst=worst,positive_rejections=errors,fixture_tolerance=t,fixture_quantization_only=5e-7+3*5e-9,
 inside_problem=ion_record_problem(inside),outside_problem=ion_record_problem(outside),numpy=np.__version__,python=sys.version)
assert counts['positive_rejected']==counts['zero_accepted']==0
assert out['inside_problem'] is None and out['outside_problem'] is not None
(R/'evidence/precision_boundary.json').write_text(json.dumps(out,indent=2),encoding='utf8')
print(json.dumps(out,indent=2))
