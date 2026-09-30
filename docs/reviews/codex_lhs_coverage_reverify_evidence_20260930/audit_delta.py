"""Additional adversarial checks of patches 0008-0011; synthetic data only."""
import os, sys, json, copy, contextlib, io, subprocess, math
from decimal import Decimal, localcontext
from pathlib import Path
E=Path(__file__).resolve().parent; W=E.parent
C=Path(os.environ.get('LHS_REVIEW_REPO',W/'lhs_coverage_reverify_20260930/candidate'))
sys.path[:0]=[str(C/'scripts'),str(C/'webapp'),str(W/'lhs_coverage_review_20260930/deps')]
os.environ.update(SUPABASE_URL='',SUPABASE_KEY='',PYTHONDONTWRITEBYTECODE='1')
import numpy as np
import pandas as pd
import lhs_descriptor_harvest as h
import lens_geometry as lg
import coverage_physics_vs_hertzian as cv
import app
import pipeline_service as ps

root=E/'delta_fixtures'; root.mkdir(exist_ok=True)
R={}
def save(obj,p):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
def compute(name,atoms=None,contacts=None,variant='base'):
    d,tm,_=cv._selftest_fixture(root/name,variant=variant)
    if atoms is not None:pd.DataFrame(atoms,columns=['id','type','radius','x','y','z']).to_csv(d/'atoms.csv',index=False)
    if contacts is not None:pd.DataFrame(contacts,columns=['id1','id2','delta','contact_area']).to_csv(d/'contacts.csv',index=False)
    with contextlib.redirect_stdout(io.StringIO()):cv.compute_case(name,d,tm)
    fm=json.loads((d/'full_metrics.json').read_text())
    return d,fm
d,healthy=compute('healthy')
R['actual_producer_controls']={'healthy':app._coverage_v2_written(str(d))}
for variant in ['denom_zero','nan_radius','isolated_zero','nan_delta','scale1','no_ligg_col']:
    d,tm,sc=cv._selftest_fixture(root/variant,variant=variant)
    with contextlib.redirect_stdout(io.StringIO()):cv.compute_case(variant,d,tm,scale=sc)
    fm=json.loads((d/'full_metrics.json').read_text())
    R['actual_producer_controls'][variant]={'accepted':app._coverage_v2_written(str(d)),
        'status':fm.get('coverage_status_physics_v2'),'diag':fm.get('am_denominator_physics_v2'),
        'cov':fm.get('coverage_AM_mean_physics_v2'),'area':fm.get('area_AM전체_SE_total_physics_v2')}
d,seonly=compute('se_only',[(1,3,.001,0,0,0),(2,3,.001,0,0,.003)],[])
R['actual_producer_controls']['se_only']={'accepted':app._coverage_v2_written(str(d)),
    'status':seonly.get('coverage_status_physics_v2'),'diag':seonly.get('am_denominator_physics_v2'),
    'has_cov':'coverage_AM_mean_physics_v2' in seonly,'area':seonly.get('area_AM전체_SE_total_physics_v2')}

R['schema_mutations']={}
for name in ['missing_n_am_and_coverage','negative_n_am_and_no_coverage','nan_n_am_and_no_coverage',
             'ok_but_invalid_denom_count','area_nan','area_string','area_negative','coverage_negative',
             'ok_but_contact_failures','blank_with_positive_values']:
    x=copy.deepcopy(healthy)
    if name.endswith('no_coverage') or name=='missing_n_am_and_coverage':
        for k in list(x):
            if k.startswith('coverage_AM') and k.endswith('_physics_v2'):del x[k]
    if name=='missing_n_am_and_coverage':del x['am_denominator_physics_v2']['n_am']
    elif name=='negative_n_am_and_no_coverage':x['am_denominator_physics_v2']['n_am']=-1
    elif name=='nan_n_am_and_no_coverage':x['am_denominator_physics_v2']['n_am']=float('nan')
    elif name=='ok_but_invalid_denom_count':x['am_denominator_physics_v2']['n_free_surface_nonpositive']=1
    elif name=='area_nan':x['area_AM전체_SE_total_physics_v2']=float('nan')
    elif name=='area_string':x['area_AM전체_SE_total_physics_v2']='broken'
    elif name=='area_negative':x['area_AM전체_SE_total_physics_v2']=-1.
    elif name=='coverage_negative':x['coverage_AM_mean_physics_v2']=-1.
    elif name=='ok_but_contact_failures':x['n_contact_failures_physics_v2']=1
    elif name=='blank_with_positive_values':x['coverage_status_physics_v2']='blank: undefined denominator'
    d=root/'schema'/name;save(x,d/'full_metrics.json')
    R['schema_mutations'][name]={'accepted':app._coverage_v2_written(str(d))}
    if name in ('missing_n_am_and_coverage','area_nan'):
        prev=ps._RUNNER
        def malformed_writer(cmd,**kw):
            save(x,d/'full_metrics.json')
            return subprocess.CompletedProcess(cmd,0,'synthetic malformed producer','')
        ps._RUNNER=malformed_writer
        try:
            stage=app._coverage_stage([sys.executable,'coverage_physics_vs_hertzian.py',name],str(d),'coverage')
            status,failed=ps.summarize([stage])
            R['schema_mutations'][name].update(required_stage_ok=stage.get('ok'),pipeline_status=status)
        finally:ps._RUNNER=prev

def area_check(a,b,dl,ad):
    return h.contact_area_check(np.array([1,2]),np.array(['AM','SE']),np.array([a,b]),
        np.array([1]),np.array([2]),np.array([ad]),np.array([dl]),np.array([0]))
q=lambda a:float(format(a,'.6g'))
# Radii round to the same token; opposite radius errors combine nonlinearly.
truth=(.0012345649,.0012345551,.00246909)
trueA=lg.intersection_disc_area(*truth)
tok=tuple(q(x) for x in (*truth,trueA))
ac,df,bd=h._contact_area_rows(*[np.array([x]) for x in tok])
R['in_domain_rounding_false_alarm']={'true_r1_r2_delta':truth,'true_area':trueA,'tokens':tok,
    'in_domain':bool(h._in_domain_rows(*[np.array([x]) for x in tok[:3]])[0]),
    'gap':tok[0]+tok[1]-tok[2]-abs(tok[0]-tok[1]),
    'margin':float(2*h._half_unit(tok[0])+2*h._half_unit(tok[1])+h._half_unit(tok[2])),
    'recalc':float(ac[0]),'diff':float(df[0]),'tolerance':float(bd[0]),'diff_over_tol':float(df[0]/bd[0]),
    'contact_area_check':area_check(*tok)}
with localcontext() as ctx:
    ctx.prec=60
    a,b,dl=map(Decimal,('0.0012345649','0.0012345551','0.00246909'))
    d=a+b-dl
    pi=Decimal('3.14159265358979323846264338327950288419716939937510582097494459')
    exact=pi*(4*d*d*a*a-(d*d-b*b+a*a)**2)/(4*d*d)
    R['in_domain_rounding_false_alarm']['decimal60_area']=str(exact)
    R['in_domain_rounding_false_alarm']['decimal60_6sig_token']=format(exact,'.6g')
    assert float(format(exact,'.6g')) == tok[3]
assert R['in_domain_rounding_false_alarm']['in_domain']
assert R['in_domain_rounding_false_alarm']['contact_area_check']['all']['n_boundary_excluded'] == 0
assert R['in_domain_rounding_false_alarm']['contact_area_check']['all']['n_beyond_tol'] == 1

old=json.loads((E/'prior_audit_results.json').read_text(encoding='utf-8'))
oldround=old['rounding_only_false_alarm']['rounded_r1_r2_delta_area']
R['old_examples_at_production_entry']={
    'rounding':area_check(*oldround),
    'hertz_deep':area_check(.0005,.0005,.000999999,old['hertz_miss']['hertz_dump']),
    '3e-5_deep':area_check(.0005,.0005,.000999999,old['3e-5_miss_deep']['dump'])}
R['noncontact_boundary_controls']={
    'zero_delta_zero_area':area_check(.001,.001,0.,0.)['all'],
    'negative_delta_zero_area':area_check(.001,.001,-.0001,0.)['all'],
    'zero_delta_positive_area':area_check(.001,.001,0.,1e-6)['all']}

# The stated component-wise monotonicity is false even inside the support.
a,b,dl=.002,.001,.0016
ac=lg.intersection_disc_area(a,b,dl)
R['interior_geometry_nonmonotonic']={'r1':a,'r2':b,'delta':dl,'area':ac,
    'more_overlap_area':lg.intersection_disc_area(a,b,dl+.00001),
    'in_domain':bool(h._in_domain_rows(np.array([a]),np.array([b]),np.array([dl]))[0])}

# Load harvester alone in a clean interpreter: no transitive Physics import.
code="import sys;sys.path.insert(0,"+repr(str(C/'scripts'))+");import lhs_descriptor_harvest;print('plastic_coverage' in sys.modules)"
proc=subprocess.run([sys.executable,'-c',code],capture_output=True,text=True)
R['clean_harvester_import']={'rc':proc.returncode,'stdout':proc.stdout.strip(),'stderr':proc.stderr[-1000:]}
assert all(R['schema_mutations'][k]['pipeline_status']=='done' for k in ('missing_n_am_and_coverage','area_nan'))
assert R['clean_harvester_import']['rc']==0 and R['clean_harvester_import']['stdout']=='False'
save(R,E/'delta_results.json')
print(json.dumps({k:v for k,v in R.items() if k not in ['old_examples_at_production_entry']},ensure_ascii=False,indent=2))
