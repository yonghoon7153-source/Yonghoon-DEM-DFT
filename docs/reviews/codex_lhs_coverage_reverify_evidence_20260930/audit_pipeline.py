import os,sys,json,subprocess,contextlib,io,shutil,builtins
from pathlib import Path
E=Path(__file__).resolve().parent
ROOT=E.parent/'lhs_coverage_review_20260930'
C=Path(os.environ.get('LHS_REVIEW_REPO',ROOT/'candidate'))
sys.path[:0]=[str(C/'webapp'),str(C/'scripts'),str(ROOT/'deps')]
os.environ.update(PYTHONDONTWRITEBYTECODE='1',SUPABASE_URL='',SUPABASE_KEY='')
import app as app
import pipeline_service as ps
import lhs_webapp_batch as batch
R={}
root=E/'pipeline_fixtures';root.mkdir(exist_ok=True)
app.app.config['UPLOAD_FOLDER']=str(root/'uploads')
app.app.config['RESULTS_FOLDER']=str(root/'results')
app.app.config['ARCHIVE_FOLDER']=str(root/'archive')
for mode in ['standard','bimodal']:
    cid='stale_'+mode
    up=root/'uploads'/cid;rd=root/'results'/cid
    up.mkdir(parents=True,exist_ok=True);rd.mkdir(parents=True,exist_ok=True)
    (up/'atom_1.liggghts').write_text('x');(up/'contact_1.liggghts').write_text('x')
    (rd/'full_metrics.json').write_text('{"coverage_status_physics_v2":"ok","coverage_AM_mean_physics_v2":999}')
    calls=[]
    def runner(cmd,**kw):
        sc=Path(cmd[1]).name;calls.append(sc)
        if sc=='parse_liggghts.py':
            for f in ['atoms.csv','contacts.csv']:(rd/f).write_text('x\n')
        elif sc in ['analyze_contacts.py','analyze_contacts_bimodal.py']:
            for f in ['full_metrics.json','atoms_analyzed.csv','contacts_analyzed.csv','network_summary.csv']:
                (rd/f).write_text('{}' if f.endswith('.json') else 'x\n')
        return subprocess.CompletedProcess(cmd,0,'deliberately no coverage write','')
    ps._RUNNER=runner
    out=app.run_pipeline(cid,mode,'1:AM,2:SE' if mode=='standard' else '1:AM_P,2:AM_S,3:SE',1000,figures=False,auto_db=False,stop_after='coverage')
    R[cid]={'status':out.get('status'),'failed_stages':out.get('failed_stages'),'calls':calls,'final_metrics':json.loads((rd/'full_metrics.json').read_text())}

# Atoms-only early return bypasses the new requested stop-stage contract.
cid='atoms_only';up=root/'uploads'/cid;up.mkdir(parents=True,exist_ok=True)
(up/'atoms.csv').write_text('id,type,radius,x,y,z\n1,1,.001,0,0,0\n')
out=app.run_pipeline(cid,'standard','1:AM,2:SE',1000,figures=False,auto_db=False,stop_after='coverage')
R['atoms_only']={'return':out,'batch_status_expression':out.get('status') or ('done' if out.get('success') else 'failed'),'metrics':json.loads((root/'results'/cid/'full_metrics.json').read_text()) if (root/'results'/cid/'full_metrics.json').exists() else None}

# Validator accepts any string, not the stated outcome schema.
rd=root/'string_validator';rd.mkdir(exist_ok=True)
R['status_schema']={}
for val in ['', 'not_run', 'ok','blank: cause']:
    (rd/'full_metrics.json').write_text(json.dumps({'coverage_status_physics_v2':val}))
    R['status_schema'][val]=app._coverage_v2_written(str(rd))

# Platform compatibility shim ONLY for tests: copy instead of OS symlink.
# No production source mutation. This cannot validate deployment symlink permissions.
original=Path.symlink_to
def copy_link(self,target,target_is_directory=False):
    shutil.copyfile(target,self)
Path.symlink_to=copy_link
buf=io.StringIO()
try:
    with contextlib.redirect_stdout(buf),contextlib.redirect_stderr(buf):
        rc=batch._selftest()
finally:
    Path.symlink_to=original
(E/'lhs_webapp_batch_copyshim.log').write_text(buf.getvalue(),encoding='utf-8')
R['batch_copyshim']={'rc':rc,'tail':buf.getvalue().splitlines()[-2:],'scope':'symlink operation replaced by byte copy; remaining production functions/test body unchanged'}
(E/'pipeline_results.json').write_text(json.dumps(R,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(R,ensure_ascii=False,indent=2))
