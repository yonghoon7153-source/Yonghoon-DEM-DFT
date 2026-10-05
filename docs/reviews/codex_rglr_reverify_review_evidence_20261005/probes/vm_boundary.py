"""Independent exact diagonal-VM arithmetic vs pinned public function. No DEM runs."""
from pathlib import Path
from fractions import Fraction as F
import json, math, sys, numpy as np
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/'source/scripts'))
from dem_analysis_core import calc_von_mises_stress
def rad(t):
 x,y,z=t
 return x**2+y**2+z**2-x*y-y*z-x*z
def exact(t):
 x,y,z=map(F,t)
 return ((x-y)**2+(y-z)**2+(x-z)**2)/2
def atom(t,z):
 return dict(type=1,x=1.,y=1.,z=z,radius=1.,sigma_xx=t[0],sigma_yy=t[1],sigma_zz=t[2])
bad=None
for p in (1000.0*(1.0+0.0731*k) for k in range(1,500)):
 for f in (1e-8,2e-8,3e-8,5e-8,1e-9,1e-10):
  t=(p,p,p*(1+f))
  if rad(t)<0 and exact(t)>0:
   bad=t;break
 if bad:break
assert bad is not None
# A second particle with exactly the same principal-stress differences, but
# without a hydrostatic offset: same exact VM, independent of constitutive law.
x,y,z=bad
good=(0.,0.,z-x)
assert exact(bad)==exact(good)
v=calc_von_mises_stress({1:atom(bad,1.),2:atom(good,2.)},{1:'AM_P'},scale=1.,plate_z=10.)
uniform=calc_von_mises_stress({1:atom(good,1.),2:atom(good,2.)},{1:'AM_P'},scale=1.,plate_z=10.)
nv=calc_von_mises_stress({1:atom(tuple(map(np.float64,bad)),1.),2:atom(tuple(map(np.float64,good)),2.)},{1:'AM_P'},scale=1.,plate_z=10.)
result=dict(negative_radicand_inputs=list(bad),negative_radicand=rad(bad),stable_radicand=float(exact(bad)),
 same_VM_second_input=list(good),exact_VM_both=math.sqrt(float(exact(bad))),exact_CV_pct=0.,actual=v,numpy_input=nv,positive_control=uniform)
assert v['status']=='computed' and v['vm_cv']==100.0
assert uniform['status']=='computed' and uniform['vm_cv']==0.0
(R/'evidence/vm_boundary.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(result,ensure_ascii=False,indent=2))
