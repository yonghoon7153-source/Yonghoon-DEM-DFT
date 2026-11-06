"""Independent review probes; no repository source mutation or production campaign."""
import os
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[k] = '1'
import sys, json, warnings, math, random
from pathlib import Path
from fractions import Fraction
ROOT = Path(__file__).resolve().parent.parent/'received'/'repo'
sys.path.insert(0,str(ROOT/'scripts'))
import numpy as np
from scipy import sparse
import carbon_junction as CJ
import step3_conv_cert as CC
OUT=Path(__file__).resolve().parent
results={}

# Recheck RR1-02 in both warning modes against real target certificate code.
ix=np.arange(3); gb=np.full(3,8e307); gt=np.ones(3); phi=np.full(3,.2)
L=sparse.diags(gb+gt,format='csr'); b=gb.copy()
results['RR1-02']={}
for mode in ('always','error'):
    with warnings.catch_warnings(record=True) as seen:
        warnings.simplefilter(mode)
        rec=CC.target_bracket(L,b,phi,ix,gb,ix,gt)
    results['RR1-02'][mode]={'warnings':[str(w.message) for w in seen], 'record':rec}
    assert not seen and rec['target_ledger_ok'] is False and rec['target_kcl_raw'] is None
with warnings.catch_warnings(record=True) as seen:
    warnings.simplefilter('error')
    rec=CC.certify(L,b,phi,0,0.,1e-12,ix,gb,ix,gt,1.,lambda A,b,x0,rt:(x0,0))
assert rec['status']=='NOT_CERTIFIABLE' and rec['ok'] is False and not seen
results['RR1-02']['certify']={k:rec[k] for k in ('status','ok','pass_a','pass_b','pass_c','pass_d')}

# Independent exact rational oracle for fingerprint's canonical group reduction.
rng=random.Random(6917)
cases=[np.array([0.,-0.]),np.array([1.,2**-60]),np.array([1.,-1.,2**-1074]),
       np.full(513,np.nextafter(2.,1.)),np.full(512,np.nextafter(2.,1.)),
       np.array([np.finfo(float).max,np.finfo(float).max]),
       np.array([np.finfo(float).max,-np.finfo(float).max,2**-1074])]
for _ in range(300):
    vals=[]
    for j in range(rng.randrange(1,80)):
        x=math.ldexp(rng.uniform(-1,1),rng.randrange(-1070,1024))
        vals.append(x)
    cases.append(np.array(vals))
checks=0
for vals in cases:
    keys=np.array([rng.randrange(5) for _ in vals],dtype=np.int64)
    want={}
    for k,x in zip(keys,vals): want[int(k)]=want.get(int(k),Fraction(0))+Fraction(float(x))
    want={k:v for k,v in want.items() if v}
    for _ in range(3):
        order=rng.sample(range(len(vals)),len(vals))
        kk,vv,bb=CJ._gfp_sums(keys[order],vals[order])
        got={int(k):Fraction(float(v)) for k,v in zip(kk,vv)}
        got.update({int(k):Fraction(int(n))*Fraction(2)**int(e) for k,n,e in bb})
        assert got==want,(vals.tolist(),got,want)
        checks+=1
results['exact_group_reduction']={'cases':len(cases),'permutation_checks':checks,'mismatches':0}

# Distinguish equal topology from unequal weights; preserve equivalent decomposition.
def fp(vals,edges=None,bot=None,top=None,ids=(0,1,2)):
    edges=edges or [(0,1)]*len(vals)
    bot=bot or ([0],[3.]); top=top or ([2],[4.])
    return CJ.solved_graph_fp(ids,[a for a,b in edges],[b for a,b in edges],vals,*bot,*top)
a=fp([1.,2**-60]); b=fp([1.]); c=fp([.5,.5]); d=fp([.5,.5],edges=[(1,0),(0,1)])
assert a!=b and b==c==d
results['fingerprint_binding']={'subulp_parallel_change_detected':a!=b,'exact_decomposition_and_orientation_invariant':b==c==d}
OUT.joinpath('graph_core_results.json').write_text(json.dumps(results,indent=2,ensure_ascii=False,allow_nan=False),encoding='utf-8')
print(json.dumps({'RR1-02':results['RR1-02']['certify'],**{k:v for k,v in results.items() if k!='RR1-02'}},indent=2))
