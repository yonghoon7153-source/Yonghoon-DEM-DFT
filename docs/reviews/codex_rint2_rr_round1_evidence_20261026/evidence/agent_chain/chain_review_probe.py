"""Imported real decision functions; synthetic records; no solver or repo writes."""
import argparse, importlib, itertools, json, math, platform, sys
from fractions import Fraction as F
from pathlib import Path
ap=argparse.ArgumentParser(); ap.add_argument('--repo',required=True); a=ap.parse_args()
sys.path.insert(0,str(Path(a.repo)/'scripts'))
import rint_r_chain as R
import step3_conv_cert as C
LAD={law:dict(R_j_lo='0.5',R_j0='1.0',R_j_hi='2.0',r0_sigma=.00163) for law in R.LAWS}
BASE={.5:5.,1.:4.7,2.:4.4}
def record(sigma,half=1e-5):
    if sigma==0: return dict(sigma=0.,state='zero',err_rel=0.,n_sdcp_near=3)
    j=C.target_judge(1-half,1+half,1.)
    assert j['pass_d']
    return dict(sigma=sigma,state='positive',err_rel=j['target_err_bound_rel'],target_lo=1-half,target_hi=1+half,scale=sigma,n_sdcp_near=3)
def predict(fn,old_fields=False):
    calls=[]
    def fetch(kit,role,law,c,rj,arms,sv_cf=False):
        ii=list(range(arms)) if isinstance(arms,int) else list(arms)
        calls.append([kit,role,law,c,rj,ii,sv_cf])
        if kit==R.SBE_KIT: return [dict(record(.00163),n_sdcp_near=0)]
        out=[record(fn(float(rj),i,role)*(1.5 if c=='1' else 1.)*.001) for i in ii]
        if old_fields: out=[{k:v for k,v in t.items() if k not in ('target_lo','target_hi','scale')} for t in out]
        return out
    p=R.Predict(fetch,LAD,None,sv_scope='all3')
    try: p.run(); status,reason='PREDICTED',None
    except R.Stop as e: status,reason=e.code,e.cause
    return dict(status=status,reason=reason,adjusted=len(p.adj),checks=p.checks,values={str(k):v for k,v in p.values().items()},calls=calls)
out={'python':sys.version,'platform':platform.platform(),'repo':str(Path(a.repo).resolve())}
cases={
 'prior_4.2_4.7_4.4':lambda r,i,role:{.5:4.2,1.:4.7,2.:4.4}[r],
 'normal':lambda r,i,role:BASE[r], 'flat':lambda r,i,role:4.7,
 'zero_at_hi':lambda r,i,role:0. if r==2 else BASE[r],
 'origin1_nonmonotone_no_adjust':lambda r,i,role:{.5:4.80,1.:4.85,2.:4.4}[r] if i==1 else BASE[r],
 'corner0_nonmonotone_adjusted_mean_monotone':lambda r,i,role:{.5:4.6,1.:4.7,2.:4.4}[r] if i==0 else BASE[r],
 'origin8_3_nonmonotone_mean_monotone':lambda r,i,role:BASE[r]*1.08 if i in (1,2) and r==.5 else ({.5:4.4,1.:4.7,2.:4.4}[r] if i==3 else BASE[r]),
 'all_monotone_adjusted':lambda r,i,role:BASE[r]*1.08 if i in (1,2) and r==.5 else BASE[r],
 'nominal_small_increase_bands_overlap':lambda r,i,role:{.5:4.69995,1.:4.7,2.:4.4}[r]}
out['predict']={name:predict(fn) for name,fn in cases.items()}
out['old_field_format']=predict(cases['normal'],old_fields=True)
# Independent exhaustive existence oracle: enumerate allowed point selections.
intervals=[(F(lo),F(hi)) for lo in range(4) for hi in range(lo,4)]
grid=list(map(F,range(4)))
def exists_monotone(pts):
    allowed=[[v for v in grid if b[0]<=v<=b[1]] for r,n,b in pts]
    return any(all((vv[i]>=vv[j] if pts[i][0]<pts[j][0] else vv[i]<=vv[j] if pts[i][0]>pts[j][0] else vv[i]==vv[j])
                   for i in range(3) for j in range(i+1,3)) for vv in itertools.product(*allowed))
trials,mismatch=0,[]
for rs in [(0,1,2),(2,0,1),(0,0,1),(1,0,0),(0,0,0)]:
    for bs in itertools.product(intervals,repeat=3):
        pts=[(r,str(i),b) for i,(r,b) in enumerate(zip(rs,bs))]
        expected,observed=exists_monotone(pts),R.r_monotone_problem(pts) is None
        trials+=1
        if expected!=observed: mismatch.append([pts,expected,observed])
out['integer_interval_oracle']=dict(trials=trials,mismatches=mismatch)
def cert_rec(g,lo,hi,scale):
    jd=C.target_judge(lo,hi,g); assert jd['pass_d'],jd
    return dict(sigma=g*scale,err_rel=jd['target_err_bound_rel'],state='positive',target_lo=lo,target_hi=hi,scale=scale)
x=1.4656880073121192
aa=cert_rec(1.4656500700997732,1.4656491487242123,x,.001)
bb=cert_rec(1.4657027350682457,x,1.4657035569138221,.001)
gap=dict(bb,target_lo=math.nextafter(x,math.inf))
out['C4']={'touch':R.r_monotone_problem([(.5,'a',R.arm_band(aa)),(1.,'b',R.arm_band(bb))]),
 'one_ulp_gap':R.r_monotone_problem([(.5,'a',R.arm_band(aa)),(1.,'b',R.arm_band(gap))]),
 'touch_endpoint_code_units':x,'one_ulp_endpoint_code_units':gap['target_lo'],'a_err_rel':aa['err_rel'],'b_err_rel':bb['err_rel']}
recs=[dict(aa,scale=.001*(1+i/8),sigma=aa['sigma']*(1+i/8)) for i in range(8)]
out['C4']['mean_exact']=R.mean_band(recs)==(sum(F(t['target_lo'])*F(t['scale']) for t in recs)/8,sum(F(t['target_hi'])*F(t['scale']) for t in recs)/8)
# Resident pure unit checks directly, omitting fixtures() / CLI / subprocess.
T=importlib.import_module('test_rint_r_chain'); T.RR=R
ids={'U17','U17b','U19','U20','M44','M45','M46','M47','M49','M50'}
out['resident_direct']={cid:fn() for cid,title,fn in T.CHECKS if cid in ids}
assert set(out['resident_direct'])==ids and all(t[0] for t in out['resident_direct'].values())
assert not mismatch
bad={'prior_4.2_4.7_4.4','origin1_nonmonotone_no_adjust','corner0_nonmonotone_adjusted_mean_monotone','origin8_3_nonmonotone_mean_monotone'}
assert all(v['status']==('R_MONOTONE_VIOLATION' if k in bad else 'PREDICTED') for k,v in out['predict'].items())
assert out['predict']['origin1_nonmonotone_no_adjust']['adjusted']==0
assert out['predict']['corner0_nonmonotone_adjusted_mean_monotone']['adjusted']==12
assert out['predict']['origin8_3_nonmonotone_mean_monotone']['adjusted']==12
assert out['old_field_format']['status']=='ARM_UNREADABLE'
assert out['C4']['touch'] is None and out['C4']['one_ulp_gap']==('a','b')
out['all_assertions_pass']=True
dest=Path(__file__).with_name('chain_review_probe.json')
dest.write_text(json.dumps(out,ensure_ascii=False,indent=2,default=str)+'\n',encoding='utf-8')
print(json.dumps({'output':str(dest),'oracle':out['integer_interval_oracle'],'resident':{k:v[0] for k,v in out['resident_direct'].items()},
 'predict':{k:[v['status'],v['adjusted']] for k,v in out['predict'].items()},'C4':out['C4'],'all_assertions_pass':True},ensure_ascii=False,indent=2))

