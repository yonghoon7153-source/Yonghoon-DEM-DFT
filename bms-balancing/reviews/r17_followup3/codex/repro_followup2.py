"""Synthetic-only R17 follow-up review. No production edits or real-data fits.

Run: python repro_followup2.py --target /path/to/bms-balancing
rc=0 means this diagnostic completed, NOT that the product passed.
All gc deletion targets are freshly created children of this script's directory.
"""
import argparse, copy, csv, hashlib, io, json, os, pathlib, subprocess, sys, tempfile
import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
ap = argparse.ArgumentParser()
ap.add_argument('--target', required=True, type=pathlib.Path)
a = ap.parse_args()
ROOT = a.target.resolve()
sys.path[:0] = [str(ROOT),str(ROOT/'tests'),str(ROOT/'reviews'),str(ROOT/'scripts')]
from test_widths import _fake_widths_csv
from bms_balancing import model, verify as V, schema as S, data as D, cycles as C
import evidence_gate as G
ENV = dict(os.environ,PYTHONUTF8='1',PYTHONDONTWRITEBYTECODE='1')
FIX = pathlib.Path(tempfile.mkdtemp(prefix='synthetic-',dir=HERE)).resolve()
RESULT = {}

def dump(p, obj):
    p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def git(*args):
    return subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()

def persist():
    dump(HERE/'REPRO_RESULTS.json',dict(target=git('rev-parse','HEAD'),fixture_root=str(FIX),cases=RESULT))

def run(name, script, *args):
    cmd = [sys.executable,str(ROOT/script),*map(str,args)]
    p = subprocess.run(cmd,cwd=ROOT,env=ENV,capture_output=True,text=True,encoding='utf-8',timeout=120)
    RESULT[name] = dict(rc=p.returncode,command=cmd,stdout=p.stdout,stderr=p.stderr)
    (HERE/(name+'.log')).write_text(p.stdout+'\nSTDERR\n'+p.stderr,encoding='utf-8')
    persist()
    return p

def pair(name, change=None, meta_change=None, both_meta=None):
    paths=[]
    for i in range(2):
        p=_fake_widths_csv(FIX/name/str(i),'cycles_syn_Li.csv',w_dqdv=i)
        rows=list(csv.DictReader(io.StringIO(p.read_text(encoding='utf-8'))))
        m=json.loads(p.with_name(p.name+'.meta.json').read_text(encoding='utf-8'))
        m.update(git_commit=git('rev-parse','HEAD'),dataset_manifest=D.half_cell_manifest_identity())
        if i and change:
            change(rows)
            with p.open('w',newline='',encoding='utf-8') as f:
                w=csv.DictWriter(f,fieldnames=S.CYCLES_ROW);w.writeheader();w.writerows(rows)
        if both_meta: both_meta(m)
        if i and meta_change: meta_change(m)
        m['sha256']=hashlib.sha256(p.read_bytes()).hexdigest()
        dump(p.with_name(p.name+'.meta.json'),m)
        paths.append(p)
    return run(name,'scripts/width_report.py',*paths,'--axis','w_dqdv')

# Original counterexamples are each run, independent of their observed return codes.
pair('width_positive')
pair('width_seed_negative',meta_change=lambda m:m.update(seed=7))
pair('width_meta_version_negative',meta_change=lambda m:m.update(objective_version='chain_rule_v2'))
for name,key,value in [('body_version','objective_version','chain_rule_v2'),('body_tol','width_tol','.90'),
                       ('body_cell','cell','OTHER'),('body_run','run_id','unrelated')]:
    pair('width_'+name,change=lambda rs,k=key,v=value:[r.update({k:v}) for r in rs])
pair('width_body_mixed_version',change=lambda rs:rs[1].update(objective_version='chain_rule_v2'))
pair('width_fractional_cycles',change=lambda rs:[r.update(cycle=str(float(r['cycle'])+.9)) for r in rs])
pair('width_null_identity',both_meta=lambda m:m.update(git_commit=None,env=None,dataset_manifest=None))
pair('width_null_settings',both_meta=lambda m:m.update(seed=None,lb=None,ub=None,initial=None,objective_version=None))

# Adjacent row/sidecar axes and nested identities, while the CSV SHA remains correct.
pair('width_row_scale_seed',change=lambda rs:[r.update(scale_seed='99') for r in rs])
pair('width_row_n_starts',change=lambda rs:[r.update(n_starts='999') for r in rs])
pair('width_row_scale_mixed',change=lambda rs:rs[1].update(scale_seed='99'))
pair('width_scale_meta_negative',meta_change=lambda m:m.update(scale_seed=99))
pair('width_starts_meta_negative',meta_change=lambda m:m.update(starts=999,n_multistart=999))
pair('width_env_python_only',both_meta=lambda m:m.update(env={'python':sys.version.split()[0]}))
pair('width_env_null_values',both_meta=lambda m:m.update(env={k:None for k in S.ENV_KEYS}))
pair('width_env_whitespace',both_meta=lambda m:m.update(env={k:' \t\u00a0' for k in S.ENV_KEYS}))
pair('width_manifest_whitespace',both_meta=lambda m:m.update(dataset_manifest='   '))
pair('width_bounds_singleton',both_meta=lambda m:m.update(lb=[0],ub=[0],initial=[0]))
pair('width_bounds_nan',both_meta=lambda m:m.update(lb=[float('nan')]*5))
pair('width_untyped_width_starts',both_meta=lambda m:m.update(width_starts=None))

# Receipt tests use real commit/tree/blob and a synthetic (not executed) run declaration.
base=G.run_receipt(head=git('rev-parse','HEAD'),tree=git('rev-parse','HEAD^{tree}'),
    instrument={'reviews/evidence_gate.py':git('rev-parse','HEAD:./reviews/evidence_gate.py')},
    package_digest='a'*64,materialized={'mode':'synthetic-review-fixture'},
    runtime={'python':sys.version.split()[0],'platform':sys.platform})
variants={'receipt_positive':{},'receipt_null_runtime':{'runtime':None},
    'receipt_bad_runtime':{'runtime':'not-a-runtime-object'},'receipt_bad_materialized':{'materialized':17},
    'receipt_bad_date':{'produced_utc':'not-a-date'},'receipt_non_digest':{'package':{'digest':'not-a-digest'}},
    'receipt_runtime_python_null':{'runtime':{'python':None,'platform':None}},
    'receipt_runtime_wrong_keys':{'runtime':{'irrelevant':True}},
    'receipt_materialized_wrong_fields':{'materialized':{'mode':17}}}
for name,change in variants.items():
    r=copy.deepcopy(base);r.update(change);r['signature']=G.receipt_signature(r)
    p=FIX/(name+'.json');dump(p,r)
    out=run(name,'scripts/verify_run_receipt.py','--receipt',p,'--target',ROOT)
    for line in out.stdout.splitlines():
        if line.startswith('RUN_RECEIPT_VERIFY '): RESULT[name]['verdict']=json.loads(line.split(' ',1)[1])
r=copy.deepcopy(base);del r['runtime'];r['signature']=G.receipt_signature(r)
p=FIX/'receipt_missing_runtime.json';dump(p,r)
run('receipt_missing_runtime_negative','scripts/verify_run_receipt.py','--receipt',p,'--target',ROOT)
packages=[]
for name,body in [('package_A','content-A'),('package_B','DIFFERENT content-B')]:
    pkg=FIX/name;pkg.mkdir();(pkg/'one.txt').write_text(body,encoding='utf-8')
    sha=hashlib.sha256((pkg/'one.txt').read_bytes()).hexdigest()
    sums=pkg/'SUMS.txt';sums.write_text(sha+'  one.txt\n',encoding='utf-8')
    ok,status=G.package_digest(pkg,sums)
    packages.append(dict(status_ok=ok,status=status,content=G.package_content_digest(pkg,sums),sha256=sha))
RESULT['package_content_control']=dict(packages=packages,content_distinct=packages[0]['content']!=packages[1]['content'])

# Safe synthetic GC fixtures. No symlinks, no user data, no targets outside FIX.
def gc_fixture(name, mode='ordinary'):
    out=FIX/name; partial=out/'partial';rows=[]
    for att,body in [('A','old'),('B','new')]:
        p=partial/'matrix'/att/'matrix_100.csv';p.parent.mkdir(parents=True);p.write_text(body,encoding='utf-8')
        rows.append(dict(attempt=att,kind='matrix',artifact='matrix_100.csv',status='partial',
            path=p.relative_to(partial).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),recorded_utc=att))
    watched=None
    if mode=='duplicate':
        rows=[rows[0],copy.deepcopy(rows[0]),dict(rows[1],artifact='matrix_200.csv')]
        watched=partial/'matrix/A/matrix_100.csv'
    if mode=='escape':
        watched=out/'victim/sentinel.txt';watched.parent.mkdir();watched.write_text('synthetic',encoding='utf-8')
        rows[0].update(kind='..',attempt='victim');rows[1]['kind']='..'
        rows += [dict(attempt=at,kind='matrix',artifact='keep_'+at,status='partial',
                      path='matrix/'+at+'/retained.txt',sha256='c'*64) for at in ('A','B')]
    if mode in ('cross_artifact','retained_path_alias'):
        watched=partial/'matrix/A/matrix_200.csv';watched.write_text('RETAIN THIS',encoding='utf-8')
        att='A' if mode=='cross_artifact' else 'C'
        if att=='C': (partial/'matrix/C').mkdir()
        rows.insert(1,dict(attempt=att,kind='matrix',artifact='matrix_200.csv',status='partial',
              path='matrix/A/matrix_200.csv',sha256=hashlib.sha256(watched.read_bytes()).hexdigest()))
    if mode=='unknown_file':
        watched=partial/'matrix/A/unindexed.txt';watched.write_text('UNKNOWN: retain or refuse',encoding='utf-8')
    if mode=='unknown_dir':
        watched=partial/'matrix/U/sentinel.txt';watched.parent.mkdir();watched.write_text('unknown dir',encoding='utf-8')
    dump(partial/'index.json',dict(index_version=1,attempts=rows))
    # Validate every prospective deletion target, including deliberately malformed metadata.
    for p in out.rglob('*'):
        if p.is_symlink() or not p.resolve().is_relative_to(FIX): raise RuntimeError('Unsafe GC fixture')
    for row in rows:
        for p in (partial/row['path'],partial/row['kind']/row['attempt']):
            if not p.resolve().is_relative_to(FIX): raise RuntimeError('Unsafe metadata deletion target')
    before={p.relative_to(out).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in out.rglob('*') if p.is_file()}
    run(name,'scripts/gc_partial.py','--root',out,'--keep',1,'--apply')
    after={p.relative_to(out).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in out.rglob('*') if p.is_file()}
    RESULT[name].update(before=before,after=after,watched=str(watched),watched_exists=watched.exists() if watched else None,
        retained_index=json.loads((partial/'index.json').read_text(encoding='utf-8')))
    persist()

for name,mode in [('gc_control','ordinary'),('gc_old_cross_artifact','cross_artifact'),
    ('gc_duplicate','duplicate'),('gc_cleanup_escape','escape'),('gc_retained_path_alias','retained_path_alias'),
    ('gc_unknown_file','unknown_file'),('gc_unknown_dir_negative','unknown_dir')]:
    gc_fixture(name,mode)

# Numerical witnesses: analytic synthetic objectives only, not real-data fitting.
bp=(model.LB5+model.UB5)/2
def numerical(name, best, bestval, obj, seeds=(), tol=.01):
    record=dict(best=best.tolist(),best_val=bestval,tol=tol)
    try:
        record['result']=V.near_optimal_extrema(obj,bp,1.,1.,best,bestval,tol=tol,seeds=list(seeds),
            n_starts=len(seeds),seed=0,lb=model.LB5,ub=model.UB5)
    except Exception as e:
        record.update(exception=type(e).__name__,message=str(e))
    RESULT[name]=record;persist()
seed=bp.copy();seed[0]=10
numerical('width_out_of_box_seed',bp,1.,lambda p:1.,[seed])
best=bp.copy();best[0]=1.4
obj=lambda p:float(1+(p[0]-1.)**2)
numerical('width_infeasible_best',best,1.,obj)
RESULT['width_infeasible_best']['published_fields']=C._width_fields(True,obj,bp,1.,1.,best,1.,.01,0,0,model.LB5,lambda s:None)
best=bp.copy();best[0]=float('nan')
numerical('width_nan_best',best,1.,lambda p:1.)
RESULT['width_nan_best']['published_fields']=C._width_fields(True,lambda p:1.,bp,1.,1.,best,1.,.01,0,0,model.LB5,lambda s:None)
best=bp.copy();best[0]=1.
numerical('width_stale_high_best_val',best,100.,obj)
numerical('width_high_control_true_best_val',best,1.,obj)
numerical('width_true_empty_control',bp,1.,lambda p:2.,tol=0.)
persist()
print(json.dumps({k:v.get('rc',v.get('exception','observed')) for k,v in RESULT.items()},indent=2))
print('Diagnostic complete; rc 0 is NOT product acceptance.')
