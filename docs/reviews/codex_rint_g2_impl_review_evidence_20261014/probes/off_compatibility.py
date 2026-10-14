"""Independent old/new OFF behavior; no source mutations, small CPU fixtures only."""
from pathlib import Path
import sys, importlib.util, contextlib, io, hashlib, json
R=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(R/'source/scripts'),str(R.parent/'lhs_coverage_review_20260930/deps'),str(R.parent/'gen2_network_reverify3_20261007/deps')]
import numpy as np
from scipy.sparse.linalg import spsolve
def module(name,p):
    s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
oldpath=R/'source_prior/step3_sigma.py'
newpath=R/'source/scripts/step3_sigma.py'
old=module('s3_old',oldpath);new=module('s3_new',newpath)
for m in (old,new):m._solve_cg=lambda L,b:(spsolve(L.tocsc(),b),0)
def quiet(fn,*a,**k):
    with contextlib.redirect_stdout(io.StringIO()):return fn(*a,**k)
def eql(a,b):
    if type(a)!=type(b):return False
    if isinstance(a,np.ndarray):return a.dtype==b.dtype and a.shape==b.shape and a.tobytes()==b.tobytes()
    if isinstance(a,dict):return a.keys()==b.keys() and all(eql(a[k],b[k]) for k in a)
    if isinstance(a,(list,tuple)):return len(a)==len(b) and all(eql(x,y) for x,y in zip(a,b))
    return a==b
cases=[]
c=np.array([[1.,1.,1.],[1.,1.,2.9]]);r=np.ones(2);t=np.array([2,1])
for h in (.1,.2):
  for p in ([0,1],[1,0]):
    for bridge in (.24,None):
      for rint in (None,{(1,2):1e-3}):
        data=[]
        for m in (old,new):
            sid,pid=quiet(m.rasterize,c[p],r[p],t[p],None,None,(0,0,0),(2,2,3.9),h,bridge_um=bridge)
            sig=m.electronic_sigma_table(.01,.005,100.,10.,250.)
            res=quiet(m.solve_sigma_z,sid,sig,h,return_field=True,z_bot_um=0,z_top_um=3.9,rint=rint,pid=pid)
            data.append((sid,pid,res))
        cases.append({'h':h,'order':p,'bridge':bridge,'r1_on':bool(rint),'all_keys_values_array_bytes_equal':eql(data[0],data[1]),'sigma':data[1][2]['sigma_eff']})
out={'old_source_sha256':hashlib.sha256(oldpath.read_bytes()).hexdigest(),'new_source_sha256':hashlib.sha256(newpath.read_bytes()).hexdigest(),'solver':'same spsolve small-fixture control','cases':cases}
(R/'evidence/off_compatibility.json').write_text(json.dumps(out,indent=2),encoding='utf8')
print(json.dumps(out,indent=2))
