"""Focused independent acceptance, boundary and rollback controls for patches 18/19."""
import os,sys,json,copy,math,hashlib,contextlib,io,subprocess,ast
from pathlib import Path
E=Path(__file__).resolve().parent;C=E.parent/'candidate';W=E.parent.parent
sys.path[:0]=[str(C/'scripts'),str(C/'webapp'),str(W/'lhs_coverage_review_20260930/deps')]
os.environ.update(SUPABASE_URL='',SUPABASE_KEY='',PYTHONDONTWRITEBYTECODE='1')
import pandas as pd
import app,pipeline_service as ps
import coverage_physics_vs_hertzian as cv
import lhs_descriptor_harvest as h
F=E/'r6_fixtures';F.mkdir(exist_ok=True)
def save(x,p):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
R={'producer_controls':{},'endpoint_mutations':{},'pin_cases':{}}
def stage(name,x):
    d=F/'stages'/name;save(x,d/'full_metrics.json')
    prev=ps._RUNNER
    def writer(cmd,**kw):
        save(x,d/'full_metrics.json');return subprocess.CompletedProcess(cmd,0,'synthetic record delivery','')
    ps._RUNNER=writer
    try:
        accepted=app._coverage_v2_written(str(d))
        st=app._coverage_stage([sys.executable,'coverage_physics_vs_hertzian.py',name],str(d),'coverage')
        status,_=ps.summarize([st])
    finally:ps._RUNNER=prev
    return dict(accepted=accepted,stage=st,pipeline_status=status)
def produce(name,spec):
    d=F/'producer'/name;d.mkdir(parents=True,exist_ok=True)
    save({'case_id':name},d/'full_metrics.json')
    rows=[(i+1,typ,.001,i*.01,0,0) for i,(typ,n) in enumerate(spec)];cons=[]
    for i,(typ,n) in enumerate(spec):
        for j in range(n):
            sid=len(rows)+1;ang=2*math.pi*j/n
            rows.append((sid,3,.001,i*.01+.001*math.cos(ang),.001*math.sin(ang),0))
            cons.append((i+1,sid,.001,math.pi*(.001**2-(.001/2)**2)))
    pd.DataFrame(rows,columns=['id','type','radius','x','y','z']).to_csv(d/'atoms.csv',index=False)
    pd.DataFrame(cons,columns=['id1','id2','delta','contact_area']).to_csv(d/'contacts.csv',index=False)
    with contextlib.redirect_stdout(io.StringIO()):cv.compute_case(name,d,{1:'AM_P',2:'AM_S',3:'SE'},scale=1000)
    fm=json.loads((d/'full_metrics.json').read_text(encoding='utf-8'))
    rec=stage(name,fm);rec['record']={k:v for k,v in fm.items() if k.endswith('_physics_v2')}
    R['producer_controls'][name]=rec
    assert rec['accepted'] is True and rec['pipeline_status']=='done',name
    return fm
monoP=produce('mono_P_full',[(1,4)])
monoS=produce('mono_S_full',[(2,4)])
partial=produce('unequal_phase_counts_partial',[(1,4),(2,1),(2,0)])
full=produce('unequal_phase_counts_full',[(1,4),(1,4),(2,4)])
zero=produce('mono_S_zero',[(2,0)])
assert 'coverage_AM_S_mean_physics_v2' not in monoP
assert 'coverage_AM_P_mean_physics_v2' not in monoS
assert partial['coverage_AM_P_mean_physics_v2']==100
assert partial['coverage_AM_S_mean_physics_v2']==25
assert partial['coverage_AM_S_std_physics_v2']==25
assert partial['coverage_AM_mean_physics_v2']==50
for key,vals in [('coverage_AM_S_mean_physics_v2',[0,99,99.999,100]),
                 ('coverage_AM_S_std_physics_v2',[0,.001,40])]:
    for v in vals:
        x=copy.deepcopy(full);x[key]=v;name=key+'_'+str(v)
        expected=(v==100 if '_mean_' in key else v==0)
        rec=stage(name,x);rec.update(value=v,key=key,expected=expected)
        R['endpoint_mutations'][name]=rec
        assert rec['accepted'] is expected and rec['pipeline_status']==('done' if expected else 'failed'),name
src=F/'not_engine.txt';src.write_text('not installed engine evidence\n',encoding='utf-8')
sha=hashlib.sha256(src.read_bytes()).hexdigest()
base=dict(schema='liggghts_add_pair_pin/1',source_file=str(src),sha256=sha,host='review',date='2026-09-30',build='synthetic',formula_confirmed=True)
cases={'int':1,'string':'x','false':False,'object':{},'list_int':[1],
       'missing_path':[{'sha256':sha}],'path_number':[{'path':3}],
       'sha_number':[{'path':str(src),'sha256':3}], 'sha_bad':[{'path':str(src),'sha256':'zz'}],
       'mixed_valid_invalid':[{'path':str(src),'sha256':sha},1],
       'none':None,'empty':[],'valid_default_sha':[{'path':str(src)}],
       'valid_explicit_sha':[{'path':str(src),'sha256':sha}],
       'mismatch':[{'path':str(src),'sha256':'0'*64}]}
prev=os.environ.get(h.PRODUCER_PIN_ENV)
try:
    for name,hosts in cases.items():
        x=dict(base,hosts=hosts);p=F/'pin'/(name+'.json');save(x,p)
        os.environ[h.PRODUCER_PIN_ENV]=str(p)
        parsed=h.producer_pin()
        emitted=h.contact_area_check([1,2],['AM_P','SE'],[.001,.001],[1],[2],[3.06305e-7],[.0001],[0])['producer_model']
        R['pin_cases'][name]=dict(input=x,parsed=parsed,emitted=emitted)
        assert parsed['installed_build_pinned'] is False and emitted['installed_build_pinned'] is False
        assert parsed['claim_present'] is True and emitted['source_claim_present'] is True
        want=False if name=='mismatch' else True if name in ['none','empty','valid_default_sha','valid_explicit_sha'] else None
        assert parsed['source_hash_verified_locally'] is want and emitted['source_hash_verified_locally'] is want,name
        if want is None:assert 'hosts' in parsed['verify_note']
finally:
    if prev is None:os.environ.pop(h.PRODUCER_PIN_ENV,None)
    else:os.environ[h.PRODUCER_PIN_ENV]=prev
# Restore only the pre-patch validator IN MEMORY, then run new resident tests.
# No source file is edited; detects whether T11s/t test the changed behavior.
old_path=W/'lhs_coverage_reverify4_20260930/candidate/webapp/app.py'
tree=ast.parse(old_path.read_text(encoding='utf-8'))
old_node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='_v2_ok_record')
ns=dict(app.__dict__);exec(compile(ast.Module(body=[old_node],type_ignores=[]),str(old_path),'exec'),ns)
actual=app._v2_ok_record;app._v2_ok_record=ns['_v2_ok_record']
import test_pipeline_provenance as resident
buf=io.StringIO()
try:
    with contextlib.redirect_stdout(buf),contextlib.redirect_stderr(buf):rc=resident.main()
finally:app._v2_ok_record=actual
(E/'resident_rollback.log').write_text(buf.getvalue(),encoding='utf-8')
R['resident_rollback']=dict(returncode=rc,passed=resident._ok,failed=resident._fail,
    expected_failed_prefixes=['T11s)','T11t)'],source_files_edited=False)
assert rc==1 and len(resident._fail)==2 and all(any(n.startswith(p) for n in resident._fail) for p in ['T11s)','T11t)'])
save(R,E/'r6_results.json')
print(json.dumps(dict(producer={k:dict(accepted=v['accepted'],status=v['pipeline_status'],mean=v['record']['coverage_AM_mean_physics_v2']) for k,v in R['producer_controls'].items()},
    endpoint={k:dict(accepted=v['accepted'],status=v['pipeline_status']) for k,v in R['endpoint_mutations'].items()},
    pin={k:v['parsed']['source_hash_verified_locally'] for k,v in R['pin_cases'].items()},rollback=R['resident_rollback']),ensure_ascii=False,indent=2))
