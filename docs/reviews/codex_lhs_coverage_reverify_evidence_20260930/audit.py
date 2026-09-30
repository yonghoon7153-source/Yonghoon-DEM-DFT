"""Review-only synthetic counterexamples; no simulation, no production edits."""
import os,sys,json,math,tempfile,importlib.util,contextlib,io
from pathlib import Path
E=Path(__file__).resolve().parent
ROOT=E.parent/'lhs_coverage_review_20260930'
C=Path(os.environ.get('LHS_REVIEW_REPO',ROOT/'candidate'))
B=Path(os.environ.get('LHS_REVIEW_BASELINE',ROOT/'baseline'))
sys.path[:0]=[str(C/'scripts'),str(ROOT/'deps'),str(C)]
os.environ.update(PYTHONDONTWRITEBYTECODE='1',PYTHONUTF8='1',PYTHONIOENCODING='utf-8')
import numpy as np
import pandas as pd
import lhs_descriptor_harvest as h
import plastic_coverage as p
import coverage_physics_vs_hertzian as cv
R={}

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    return mod

def probe_case(label, atoms, contacts, tm):
    d=E/'fixtures'/label;d.mkdir(parents=True,exist_ok=True)
    pd.DataFrame(atoms,columns=['id','type','radius','x','y','z']).to_csv(d/'atoms.csv',index=False)
    pd.DataFrame(contacts,columns=['id1','id2','delta','contact_area']).to_csv(d/'contacts.csv',index=False)
    (d/'full_metrics.json').write_text('{}',encoding='utf-8')
    cv.compute_case(label,d,tm)
    fm=json.loads((d/'full_metrics.json').read_text())
    return {k:v for k,v in fm.items() if k.endswith('_physics_v2')}

# Valid finite contact inputs, yet denominator collapse becomes measured zero.
r=.001
ats=[(1,1,r,0,0,0),(2,1,r,.0008,0,0),(3,1,r,.0004,.0008*math.sqrt(3)/2,0),
     (4,1,r,.0004,.0008/(2*math.sqrt(3)),.0008*math.sqrt(2/3)),(5,2,r,0,0,-.0019)]
cts=[(a,b,d,p._intersection_disc_area(r,r,d)) for a,b,d in [(1,2,.0012),(1,3,.0012),(1,4,.0012),(2,3,.0012),(2,4,.0012),(3,4,.0012),(1,5,.0001)]]
R['denominator_zero']=probe_case('denominator_zero',ats,cts,{1:'AM',2:'SE'})
R['nan_isolated_radius']=probe_case('nan_isolated_radius',[(1,1,float('nan'),0,0,0),(2,2,r,0,0,0)],[],{1:'AM',2:'SE'})
R['valid_isolated_zero']=probe_case('valid_isolated_zero',[(1,1,r,0,0,0),(2,2,r,0,0,.003)],[],{1:'AM',2:'SE'})

# Same actual inputs through the old and new path: legacy bytes, CSV, return.
oldcv=load('baseline_cv',B/'scripts/coverage_physics_vs_hertzian.py')
R['legacy_comparison']={}
for variant in ['base','amam_x2','nan_delta','scale1','no_ligg_col','stale_v2']:
    d,tm,sc=cv._selftest_fixture(E/'fixtures'/('legacy_'+variant),variant=variant)
    oldret=oldcv.compute_case(d.name,d,tm,scale=sc)
    od=cv._legacy_digests(d,oldret)
    newret=cv.compute_case(d.name,d,tm,scale=sc)
    nd=cv._legacy_digests(d,newret)
    R['legacy_comparison'][variant]={'same':od==nd,'old':od,'new':nd}

# Wall-excluded numerator still includes a contact entirely below the floor.
# AM center z=-0.9,r=1; SE center z=-2.3,r=.5; separation 1.4, delta=.1.
aa=p._intersection_disc_area(1.,.5,.1)
cw=h.coverage_wall(np.array([1,2]),np.array(['AM','SE']),np.array([1.,.5]),np.array([-.9,-2.3]),np.array([1]),np.array([2]),np.array([aa]),10.)
R['wall_outside_numerator']={'disc_area':aa,'contact_plane_z':-.9-(1.4**2+1-.5**2)/(2*1.4),'expected_in_ROI_pct':0.,'actual':cw['wallexcl']}
# Selection bias: an invalid denominator can remove either high or low values.
R['wall_invalid_exclusion']=h.coverage_wall(np.array([1,2,3]),np.array(['AM','AM','SE']),np.array([1.,1.,1.]),np.array([-1.1,5.,5.]),np.array([1]),np.array([3]),np.array([math.pi]),10.)

# Rounding tolerance tests: calculation on the actual function, not the printed formula.
rng=np.random.default_rng(20260930)
n=15000
r1=10**rng.uniform(-4,-2,n);r2=10**rng.uniform(-4,-2,n)
rs=r1*r2/(r1+r2);delta=rs*10**rng.uniform(-5,0,n)
area=np.array([p._intersection_disc_area(a,b,d) for a,b,d in zip(r1,r2,delta)])
q=lambda x:np.array([float(format(a,'.6g')) for a in x])
qr1,qr2,qd,qa=map(q,(r1,r2,delta,area))
calc,diff,tol=h._contact_area_rows(qr1,qr2,qd,qa)
ix=np.flatnonzero(diff>tol)
mut=q(area*(1+3e-5));_,md,mt=h._contact_area_rows(qr1,qr2,qd,mut)
miss=np.flatnonzero(md<=mt)
R['rounding_sweep']={'seed':20260930,'n':n,'false_alarms':len(ix),'3e-5_missed':len(miss),'first_miss':None if not len(miss) else {k:float(v[miss[0]]) for k,v in {'r1':qr1,'r2':qr2,'delta':qd,'area':qa,'mutant_area':mut,'diff':md,'tol':mt}.items()}}
rr=.0005;dd=.000999999
ah=np.pi*(rr/2)*dd
ac,df,bd=h._contact_area_rows(np.array([rr]),np.array([rr]),np.array([dd]),np.array([float(format(ah,'.6g'))]))
R['hertz_miss']={'r1':rr,'r2':rr,'delta':dd,'hertz_dump':float(format(ah,'.6g')),'calc':ac[0],'diff':df[0],'tol':bd[0],'caught':bool(df[0]>bd[0]),'domain':'deep overlap, not evidence of corpus incidence'}
badA=float(format(ac[0]*(1+3e-5),'.6g'))
_,df,bd=h._contact_area_rows(np.array([rr]),np.array([rr]),np.array([dd]),np.array([badA]))
R['3e-5_miss_deep']={'dump':badA,'diff':df[0],'tol':bd[0],'caught':bool(df[0]>bd[0])}
true=(.002,.0010000049,.0020000051)
trueA=p._intersection_disc_area(*true)
rounded=[float(format(t,'.6g')) for t in (*true,trueA)]
ac,df,bd=h._contact_area_rows(*[np.array([v]) for v in rounded])
R['rounding_only_false_alarm']={'true_r1_r2_delta':true,'true_area':trueA,'rounded_r1_r2_delta_area':rounded,'recalc_area':ac[0],'diff':df[0],'tol':bd[0],'diff_over_tol':df[0]/bd[0],'caught':bool(df[0]>bd[0]),'domain':'near containment boundary, no claim of observed corpus incidence'}

# Two ordinary import forms bypass the whole-source static guard.
R['ast_guard']={}
for src in ['from scripts import plastic_coverage as pc\npc.film_area_from_overlap(.1,.5)',
            'from importlib import import_module as im\npc = im("plastic_coverage")\npc.film_area_from_overlap(.1,.5)']:
    names,bad=h._plastic_coverage_uses(src)
    ns={};exec(src,ns)
    R['ast_guard'][src]={'names':sorted(names),'bad':bad,'actually_called':True}

# Yield discontinuity and unit invariance, actual v2 functions.
rr=.5e-6;dd=p.DR_YIELD_ONSET*(rr/2)
amin,cm=p.film_area_physics_v2(np.nextafter(dd,0),rr,rr,length_scale=1.)
aplus,cp=p.film_area_physics_v2(dd,rr,rr,length_scale=1.)
asi,cs=p.film_area_physics_v2(dd*1000,rr*1000,rr*1000,length_scale=1000.)
R['yield_jump']={'onset':p.DR_YIELD_ONSET,'delta_m':dd,'below_m2':amin,'at_m2':aplus,'ratio':aplus/amin,'sim_over_SI':asi/aplus,'binding':cp['binding'],'conflict':cp['cap_conflict']}

# No statistical corpus claims: only the deliberately specified synthetic inputs.
def clean(x):
    if isinstance(x,dict):return {str(k):clean(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)):return [clean(v) for v in x]
    if isinstance(x,np.generic):return x.item()
    return x
(E/'audit_results.json').write_text(json.dumps(clean(R),ensure_ascii=False,indent=2),encoding='utf-8')
for k,v in R.items():
    print(k,json.dumps(clean(v),ensure_ascii=False)[:3000])
