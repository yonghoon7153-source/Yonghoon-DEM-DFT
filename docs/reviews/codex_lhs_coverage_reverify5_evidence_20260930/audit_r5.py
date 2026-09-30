"""Review the new pin states, actual producer clip controls, and residual identities."""
import os,sys,json,hashlib,copy,contextlib,io,subprocess,math
from pathlib import Path
E=Path(__file__).resolve().parent;C=E.parent/'candidate';W=E.parent.parent
sys.path[:0]=[str(C/'scripts'),str(C/'webapp'),str(W/'lhs_coverage_review_20260930/deps')]
os.environ.update(SUPABASE_URL='',SUPABASE_KEY='',PYTHONDONTWRITEBYTECODE='1')
import pandas as pd
import numpy as np
import lhs_descriptor_harvest as h
import coverage_physics_vs_hertzian as cv
import app,pipeline_service as ps
F=E/'r5_fixtures';F.mkdir(exist_ok=True)
def save(x,p):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
def diag():return h.contact_area_check([1,2],['AM_P','SE'],[.001,.001],[1],[2],[3.06305e-7],[.0001],[0])
R={'pin':{},'producer_controls':{},'mutations':{},'domain':{}}
src=F/'source.txt';src.write_text('independent non-engine hash fixture\n',encoding='utf-8')
dig=hashlib.sha256(src.read_bytes()).hexdigest()
base=dict(schema='liggghts_add_pair_pin/1',source_file=str(src),sha256=dig,host='local-fixture',date='2026-09-30',build='not-an-engine',formula_confirmed=True)
for name in ['match','mismatch','remote','relative_with_hosts','mixed_hosts','missing_build','bad_hosts_type','date_shape_only']:
    x=copy.deepcopy(base)
    if name=='mismatch':x['sha256']='0'*64
    if name=='remote':x['source_file']='/nonexistent-review-host/src/file.cpp'
    if name=='relative_with_hosts':x.update(source_file='src/compute_pair_gran_local.cpp',hosts=[{'path':str(src),'sha256':dig}])
    if name=='mixed_hosts':x['hosts']=[{'path':str(src),'sha256':'0'*64}]
    if name=='missing_build':del x['build']
    if name=='bad_hosts_type':x['hosts']=1
    if name=='date_shape_only':x['date']='2026-99-99'
    p=F/'pins'/(name+'.json');save(x,p)
    os.environ[h.PRODUCER_PIN_ENV]=str(p)
    try:R['pin'][name]=dict(input=x,parsed=h.producer_pin(),emitted=diag()['producer_model'])
    except Exception as ex:R['pin'][name]=dict(input=x,exception=type(ex).__name__,message=str(ex))
os.environ.pop(h.PRODUCER_PIN_ENV,None)

def produce(name,counts):
    d=F/'producer'/name;d.mkdir(parents=True,exist_ok=True)
    save({'case_id':name},d/'full_metrics.json')
    rows=[(1,1,.001,0,0,0),(2,2,.001,.01,0,0)];contacts=[]
    for am,n in enumerate(counts,1):
        for j in range(n):
            sid=len(rows)+1;angle=2*math.pi*j/max(n,1)
            rows.append((sid,3,.001,(am-1)*.01+.001*math.cos(angle),.001*math.sin(angle),0))
            contacts.append((am,sid,.001,math.pi*(.001**2-(.001/2)**2)))
    pd.DataFrame(rows,columns=['id','type','radius','x','y','z']).to_csv(d/'atoms.csv',index=False)
    pd.DataFrame(contacts,columns=['id1','id2','delta','contact_area']).to_csv(d/'contacts.csv',index=False)
    with contextlib.redirect_stdout(io.StringIO()):cv.compute_case(name,d,{1:'AM_P',2:'AM_S',3:'SE'},scale=1000)
    fm=json.loads((d/'full_metrics.json').read_text(encoding='utf-8'))
    R['producer_controls'][name]=dict(accepted=app._coverage_v2_written(str(d)),record={k:v for k,v in fm.items() if k.endswith('_physics_v2')})
    return fm
zero=produce('zero',(0,0));part=produce('partial_clip',(4,1));full=produce('full_clip',(4,4))
def probe(name,x):
    d=F/'mutations'/name;save(x,d/'full_metrics.json')
    accepted=app._coverage_v2_written(str(d));prev=ps._RUNNER
    def writer(cmd,**kw):
        save(x,d/'full_metrics.json');return subprocess.CompletedProcess(cmd,0,'synthetic mutation delivery only','')
    ps._RUNNER=writer
    try:
        st=app._coverage_stage([sys.executable,'coverage_physics_vs_hertzian.py',name],str(d),'coverage')
        status,_=ps.summarize([st])
    finally:ps._RUNNER=prev
    R['mutations'][name]=dict(accepted=accepted,stage=st,pipeline_status=status,record={k:v for k,v in x.items() if k.endswith('_physics_v2')})
x=copy.deepcopy(part)
x['coverage_AM_mean_physics_v2']=1.0
# Retain legitimate clip count -> this must be refused by R4 rule.
probe('below_clip_lower_bound',x)
x=copy.deepcopy(full)
x['coverage_AM_P_mean_physics_v2']=0.0
probe('all_clipped_but_phase_mean_zero',x)
x=copy.deepcopy(full)
x['coverage_AM_S_std_physics_v2']=40.0
probe('all_clipped_but_phase_std_40',x)
x=copy.deepcopy(part)
x['coverage_AM_mean_physics_v2']=99.0
probe('unverified_phase_weight_example',x)
for name,a,b,dl in [('previous_underflow',1e-100,1e-100,1e-101),('huge_radii',1e160,1e160,1e159),
                    ('normal',.001,.001,.0001),('small_supported',1e-60,1e-60,1e-61)]:
    z={}
    with np.errstate(all='ignore'):
        try:
            ee,unc=h._producer_error_bound([a],[b],[dl]);z['E']=float(ee[0]);z['uncertified']=bool(unc[0])
        except Exception as ex:z['bound_exception']=dict(type=type(ex).__name__,message=str(ex))
        try:
            out=h.contact_area_check([1,2],['AM_P','SE'],[a,b],[1],[2],[0.0],[dl],[0]);z['all']=out['all']
        except Exception as ex:z['entry_exception']=dict(type=type(ex).__name__,message=str(ex))
    R['domain'][name]=dict(inputs=[a,b,dl],result=z)
save(R,E/'r5_results.json')
print(json.dumps(dict(pin={k:v.get('parsed',v) for k,v in R['pin'].items()},
    producer_controls={k:dict(accepted=v['accepted'],mean=v['record'].get('coverage_AM_mean_physics_v2'),diag=v['record'].get('am_denominator_physics_v2')) for k,v in R['producer_controls'].items()},
    mutations={k:dict(accepted=v['accepted'],pipeline_status=v['pipeline_status']) for k,v in R['mutations'].items()},domain=R['domain']),ensure_ascii=False,indent=2))
