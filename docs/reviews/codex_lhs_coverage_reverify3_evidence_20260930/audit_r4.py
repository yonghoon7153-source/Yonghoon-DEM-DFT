"""Independent pin and producer-ledger counterexamples. No DEM or server."""
import os, sys, json, copy, contextlib, io, subprocess
from pathlib import Path
E=Path(__file__).resolve().parent; C=E.parent/'candidate'; W=E.parent.parent
sys.path[:0]=[str(C/'scripts'),str(C/'webapp'),str(W/'lhs_coverage_review_20260930/deps')]
os.environ.update(SUPABASE_URL='',SUPABASE_KEY='',PYTHONDONTWRITEBYTECODE='1')
import pandas as pd
import lhs_descriptor_harvest as h
import coverage_physics_vs_hertzian as cv
import app, pipeline_service as ps
F=E/'r4_fixtures';F.mkdir(exist_ok=True)
def save(obj,p):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
def diag():
    return h.contact_area_check([1,2],['AM_P','SE'],[.001,.001],[1],[2],[3.06305e-7],[.0001],[0])
R={'pin':{},'schema':{}}
fake=dict(schema='liggghts_add_pair_pin/1',source_file=str(F/'nonexistent.cpp'),sha256='0'*64,formula_confirmed=True)
assert not Path(fake['source_file']).exists()
p=F/'fake_pin_missing.json';save(fake,p)
os.environ[h.PRODUCER_PIN_ENV]=str(p)
R['pin']['nonexistent_source_missing_build']=dict(input=copy.deepcopy(fake),result=h.producer_pin(),diagnostic=diag()['producer_model'])
wrong=F/'wrong_source.cpp';wrong.write_text('/* deliberately no add_pair function */\n',encoding='utf-8')
fake.update(source_file=str(wrong),host='unknown',date='not-a-date',build='unknown')
p=F/'fake_pin_wrong_source.json'
save(fake,p)
os.environ[h.PRODUCER_PIN_ENV]=str(p)
R['pin']['unrelated_source_wrong_hash']=dict(input=copy.deepcopy(fake),result=h.producer_pin(),diagnostic=diag()['producer_model'])
os.environ.pop(h.PRODUCER_PIN_ENV,None)
R['pin']['missing_default']=h.producer_pin()
def produce(name,zero=False):
    d,tm,scale=cv._selftest_fixture(F/name)
    if zero:
        pd.DataFrame([],columns=['id1','id2','delta','contact_area']).to_csv(d/'contacts.csv',index=False)
    with contextlib.redirect_stdout(io.StringIO()):cv.compute_case(name,d,tm,scale=scale)
    fm=json.loads((d/'full_metrics.json').read_text(encoding='utf-8'))
    assert app._coverage_v2_written(str(d))
    return fm
base=produce('base');zero=produce('zero_am_contacts',True)
R['schema']['positive_controls']={k:{kk:vv for kk,vv in v.items() if kk.endswith('_physics_v2')} for k,v in [('base',base),('zero',zero)]}
def probe(name,fm):
    d=F/'mutants'/name;save(fm,d/'full_metrics.json')
    accepted=app._coverage_v2_written(str(d))
    prev=ps._RUNNER
    def writer(cmd,**kw):
        save(fm,d/'full_metrics.json')
        return subprocess.CompletedProcess(cmd,0,'counterexample record delivery only','')
    ps._RUNNER=writer
    try:
        st=app._coverage_stage([sys.executable,'coverage_physics_vs_hertzian.py',name],str(d),'coverage')
        status,failed=ps.summarize([st])
    finally:ps._RUNNER=prev
    R['schema'][name]=dict(accepted=accepted,stage=st,pipeline_status=status,record={k:v for k,v in fm.items() if k.endswith('_physics_v2')})
x=copy.deepcopy(zero)
for k in x:
    if k.startswith('coverage_') and k.endswith('_mean_physics_v2'):x[k]=50.0
probe('zero_contacts_positive_coverage',x)
x=copy.deepcopy(base);x['am_denominator_physics_v2']['n_coverage_clipped_100']=x['am_denominator_physics_v2']['n_am']
probe('all_am_clipped_but_mean_not_100',x)
x=copy.deepcopy(base)
for k in x:
    if k.startswith('coverage_') and k.endswith('_std_physics_v2'):x[k]=75.0
probe('impossible_population_std_75',x)
x=copy.deepcopy(base);x['n_cap_branch_physics_v2']=x['n_contacts_physics_v2']
x['cap_conflict_frac_cap_branch_physics_v2']=round(x['cap_conflict_n_physics_v2']/x['n_cap_branch_physics_v2'],6)
probe('cap_branch_count_includes_elastic_and_none',x)
save(R,E/'r4_results.json')
print(json.dumps(dict(pin={k:v.get('result',v) for k,v in R['pin'].items()},schema={k:{kk:vv for kk,vv in v.items() if kk in ('accepted','pipeline_status')} for k,v in R['schema'].items()}),ensure_ascii=False,indent=2))
