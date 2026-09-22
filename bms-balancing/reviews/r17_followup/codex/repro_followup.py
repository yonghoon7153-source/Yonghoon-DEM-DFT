"""R17 follow-up: synthetic fixtures only; no real-data fitting or target edits.

Run with Python having the target's test dependencies. Optional --target BMS_DIR.
Exit 0 means the recorded observations were reproduced, NOT a product PASS.
"""
import argparse, copy, csv, hashlib, importlib.util, io, json, os, pathlib, subprocess, sys, tempfile
import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
ap = argparse.ArgumentParser()
ap.add_argument('--target', type=pathlib.Path, default=HERE.parents[1]/'work/r17-response-7c8f61f9/bms-balancing')
a = ap.parse_args()
ROOT = a.target.resolve()
sys.path[:0] = [str(ROOT), str(ROOT/'tests'), str(ROOT/'reviews'), str(ROOT/'scripts')]
from test_widths import _fake_widths_csv
from bms_balancing import model, verify as V, schema as S, data as D
import evidence_gate as G
env = dict(os.environ, PYTHONUTF8='1', PYTHONDONTWRITEBYTECODE='1')
RESULT = {}
FIX = pathlib.Path(tempfile.mkdtemp(prefix='fixtures-', dir=HERE)).resolve()

def dump(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()

def run(name, script, *args):
    cmd = [sys.executable, str(ROOT/script), *map(str,args)]
    p = subprocess.run(cmd, cwd=ROOT, env=env, capture_output=True, text=True, encoding='utf-8', timeout=120)
    (HERE/(name+'.log')).write_text(p.stdout+'\nSTDERR\n'+p.stderr, encoding='utf-8')
    RESULT[name] = dict(rc=p.returncode, command=cmd, stdout=p.stdout, stderr=p.stderr)
    return p

def read_rows(p):
    return list(csv.DictReader(io.StringIO(p.read_text(encoding='utf-8'))))

def alter(p, row_change=None, meta_change=None):
    mp = p.with_name(p.name+'.meta.json')
    rows = read_rows(p)
    m = json.loads(mp.read_text(encoding='utf-8'))
    if row_change:
        row_change(rows)
        with p.open('w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, fieldnames=S.CYCLES_ROW); w.writeheader(); w.writerows(rows)
    if meta_change:
        meta_change(m)
    m['sha256'] = hashlib.sha256(p.read_bytes()).hexdigest()
    dump(mp,m)

def pair(name, change=None, meta_change=None, both_meta=None, axis='w_dqdv'):
    paths = []
    for i in range(2):
        p = _fake_widths_csv(FIX/name/str(i), 'cycles_syn_Li.csv', w_dqdv=i)
        def normalize(m):
            m['git_commit']=git('rev-parse','HEAD')
            m['dataset_manifest']=D.half_cell_manifest_identity()
            if both_meta: both_meta(m)
            if i and meta_change: meta_change(m)
        alter(p, change if i else None, normalize)
        paths.append(p)
    r = run(name,'scripts/width_report.py',*paths,'--axis',axis)
    return r, paths

# C1: keep the successful control and single-axis negative controls next to each bypass.
assert pair('width_positive')[0].returncode == 0
assert pair('width_seed_negative', meta_change=lambda m:m.update(seed=7))[0].returncode == 2
assert pair('width_meta_version_negative', meta_change=lambda m:m.update(objective_version='chain_rule_v2'))[0].returncode == 2
assert pair('width_body_version', change=lambda rs:[r.update(objective_version='chain_rule_v2') for r in rs])[0].returncode == 0
assert pair('width_body_mixed_version', change=lambda rs:rs[1].update(objective_version='chain_rule_v2'))[0].returncode == 0
assert pair('width_body_tol', change=lambda rs:[r.update(width_tol='0.90') for r in rs])[0].returncode == 0
assert pair('width_body_cell', change=lambda rs:[r.update(cell='DIFFERENT_CELL') for r in rs])[0].returncode == 0
assert pair('width_body_run', change=lambda rs:[r.update(run_id='unrelated-run') for r in rs])[0].returncode == 0
assert pair('width_fractional_cycles', change=lambda rs:[r.update(cycle=str(float(r['cycle'])+.9)) for r in rs])[0].returncode == 0
assert pair('width_null_identity', both_meta=lambda m:m.update(git_commit=None,env=None,dataset_manifest=None))[0].returncode == 0
assert pair('width_null_settings', both_meta=lambda m:m.update(seed=None,lb=None,ub=None,initial=None,objective_version=None))[0].returncode == 0

# C2: real code/tree/blob; only structure is weakened, no cryptographic-forgery claim.
base = G.run_receipt(head=git('rev-parse','HEAD'), tree=git('rev-parse','HEAD^{tree}'),
                     instrument={'reviews/evidence_gate.py':git('rev-parse','HEAD:./reviews/evidence_gate.py')},
                     package_digest='a'*64, materialized={'mode':'synthetic-review-fixture'},runtime={'python':sys.version})
variants = {'receipt_positive':{}, 'receipt_null_runtime':{'runtime':None},
            'receipt_bad_runtime':{'runtime':'not-a-runtime-object'},
            'receipt_bad_materialized':{'materialized':17},
            'receipt_bad_date':{'produced_utc':'not-a-date'},
            'receipt_non_digest':{'package':{'digest':'not-a-digest'}}}
for name, change in variants.items():
    r = copy.deepcopy(base); r.update(change); r['signature']=G.receipt_signature(r)
    p=FIX/(name+'.json'); dump(p,r)
    out=run(name,'scripts/verify_run_receipt.py','--receipt',p,'--target',ROOT)
    verdict=json.loads(next(l for l in out.stdout.splitlines() if l.startswith('RUN_RECEIPT_VERIFY ')).split(' ',1)[1])
    RESULT[name]['verdict']=verdict
    assert out.returncode==0 and verdict['verified'] and verdict['checks']['complete']
r=copy.deepcopy(base); del r['runtime']; r['signature']=G.receipt_signature(r)
p=FIX/'receipt_missing_runtime.json';dump(p,r)
assert run('receipt_missing_runtime_negative','scripts/verify_run_receipt.py','--receipt',p,'--target',ROOT).returncode==3
# The live r11 replay writer serializes package_digest()'s STATUS dict as a digest.
package_values=[]
for name,body in [('package_A','content-A'),('package_B','DIFFERENT content-B')]:
    pkg=FIX/name;pkg.mkdir();payload=pkg/'one.txt';payload.write_text(body,encoding='utf-8')
    sha=hashlib.sha256(payload.read_bytes()).hexdigest()
    sums=pkg/'SUMS.txt';sums.write_text(sha+'  one.txt\n',encoding='utf-8')
    ok,status=G.package_digest(pkg,sums)
    assert ok
    r=copy.deepcopy(base);r['package']['digest']=str(status);r['signature']=G.receipt_signature(r)
    rp=FIX/(name+'_receipt.json');dump(rp,r)
    assert run(name,'scripts/verify_run_receipt.py','--receipt',rp,'--target',ROOT).returncode==0
    package_values.append(dict(content_sha256=sha,receipt_package_digest=r['package']['digest']))
assert package_values[0]['content_sha256']!=package_values[1]['content_sha256']
assert package_values[0]['receipt_package_digest']==package_values[1]['receipt_package_digest']
RESULT['receipt_package_status_collision']=dict(packages=package_values,production_writer='reviews/r11_repros/replay_codex_r11.py:349')

# C3: all deletion targets are reviewer-created files under FIX, not user artifacts.
def gc_fixture(name, duplicate=False, kind_escape=False):
    out=FIX/name; partial=out/'partial'; rows=[]
    for att, body in [('A','old'),('B','new')]:
        p=partial/'matrix'/att/'matrix_100.csv';p.parent.mkdir(parents=True);p.write_text(body,encoding='utf-8')
        rows.append(dict(attempt=att,kind='matrix',artifact='matrix_100.csv',status='partial',
                         path=p.relative_to(partial).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),recorded_utc=att))
    if duplicate:
        rows=[rows[0],copy.deepcopy(rows[0])]
        # Keep B indexed as another artifact, so the unknown-directory guard isn't the cause.
        rows.append(dict(attempt='B',kind='matrix',artifact='matrix_200.csv',status='partial',path='matrix/B/matrix_100.csv',sha256='b'*64))
    if kind_escape:
        victim=out/'victim';victim.mkdir();(victim/'sentinel.txt').write_text('review synthetic only',encoding='utf-8')
        assert victim.resolve().is_relative_to(FIX)
        # A's file path is safely inside partial, but the cleanup path is independently formed.
        rows[0]['kind']='..'; rows[0]['attempt']='victim'
        rows[1]['kind']='..'
        # Recognize actual directories so unknown-directory checks don't mask this axis.
        rows += [dict(attempt=att,kind='matrix',artifact='keep_'+att,status='partial',path='matrix/'+att+'/retained.txt',sha256='c'*64) for att in ('A','B')]
    dump(partial/'index.json',dict(index_version=1,attempts=rows))
    return out

gc=gc_fixture('gc_control')
assert run('gc_control','scripts/gc_partial.py','--root',gc,'--keep',1,'--apply').returncode==0
assert not (gc/'partial/matrix/A/matrix_100.csv').exists() and (gc/'partial/matrix/B/matrix_100.csv').exists()
# Exact prior counterexample: A/100 + A/200 + B/100 is now preserved correctly.
gc=gc_fixture('gc_old_cross_artifact')
v=gc/'partial/matrix/A/matrix_200.csv';v.write_text('only-200',encoding='utf-8')
ix=json.loads((gc/'partial/index.json').read_text())
ix['attempts'].insert(1,dict(attempt='A',kind='matrix',artifact='matrix_200.csv',status='partial',path='matrix/A/matrix_200.csv',sha256=hashlib.sha256(v.read_bytes()).hexdigest()))
dump(gc/'partial/index.json',ix)
assert run('gc_old_cross_artifact','scripts/gc_partial.py','--root',gc,'--keep',1,'--apply').returncode==0
assert v.read_text(encoding='utf-8')=='only-200'
RESULT['gc_old_cross_artifact']['retained_200_exists']=v.exists()
gc=gc_fixture('gc_duplicate',duplicate=True)
assert run('gc_duplicate','scripts/gc_partial.py','--root',gc,'--keep',1,'--apply').returncode==0
RESULT['gc_duplicate']['retained_index']=json.loads((gc/'partial/index.json').read_text())
RESULT['gc_duplicate']['retained_payload_exists']=(gc/'partial/matrix/A/matrix_100.csv').exists()
assert not RESULT['gc_duplicate']['retained_payload_exists']
gc=gc_fixture('gc_cleanup_escape',kind_escape=True)
assert run('gc_cleanup_escape','scripts/gc_partial.py','--root',gc,'--keep',1,'--apply').returncode==0
RESULT['gc_cleanup_escape']['outside_partial_sentinel_exists']=(gc/'victim/sentinel.txt').exists()
assert not RESULT['gc_cleanup_escape']['outside_partial_sentinel_exists']

# C4: actual bounded optimizers, a known analytical mode range; no fitting to real data.
bp=(model.LB5+model.UB5)/2
seed=bp.copy();seed[0]=10.0
res=V.near_optimal_extrema(lambda p:1.0,bp,1.,1.,bp,1.,tol=.01,seeds=[seed],n_starts=1,seed=0,lb=model.LB5,ub=model.UB5)
RESULT['width_out_of_box_seed']=dict(result=res,seed=seed.tolist(),lb=model.LB5.tolist(),ub=model.UB5.tolist(),
                                    true_LAM_PE_range_percent=[(1-model.UB5[0]/bp[0])*100,(1-model.LB5[0]/bp[0])*100])
assert res['LAM_PE']['min'] < -700 and res['LAM_PE']['is_lower_bound'] is True
# Stale best_val: valid feasible points exist, but best is not one of them.
best=bp.copy();best[0]=1.4
obj=lambda p:float(1+(p[0]-1.0)**2)
res=V.near_optimal_extrema(obj,bp,1.,1.,best,1.,tol=.01,seeds=[],n_starts=0,seed=0,lb=model.LB5,ub=model.UB5)
RESULT['width_infeasible_best']=dict(result=res,best=best.tolist(),best_actual_value=obj(best),declared_best_value=1.,limit=1.01,
                                    true_LAM_PE_range_percent=[(1-1.1/bp[0])*100,(1-1./bp[0])*100])
assert res['LAM_PE']['min'] < -16
# Exercise the actual cycles publisher helper as well: it still calls this measured.
from bms_balancing import cycles as C
w=C._width_fields(True,obj,bp,1.,1.,best,1.,.01,0,0,model.LB5,lambda s:None)
RESULT['width_infeasible_best']['published_fields']=w
assert w['width_status']=='measured' and w['LAM_PE_lo'] < -.16

# The named 'nothing is feasible' regression actually exits at the negative-tol guard.
calls=[]
try:
    V.near_optimal_extrema(lambda p:(calls.append(1) or 1.),bp,1.,1.,bp,1.,tol=-.5,seeds=[],n_starts=0,seed=0,lb=model.LB5,ub=model.UB5)
except ValueError as e:
    RESULT['empty_set_test_axis']=dict(objective_calls=len(calls),exception=type(e).__name__,message=str(e))
assert len(calls)==0
# A distinct valid-tol empty set must hit the RuntimeError path (positive negative control).
try:
    V.near_optimal_extrema(lambda p:2.,bp,1.,1.,bp,1.,tol=0.,seeds=[],n_starts=0,seed=0,lb=model.LB5,ub=model.UB5)
except RuntimeError as e:
    RESULT['true_empty_set_control']=dict(exception=type(e).__name__,message=str(e))
else:
    raise AssertionError('empty set unexpectedly accepted')

dump(HERE/'REPRO_RESULTS.json',dict(target=git('rev-parse','HEAD'),fixture_root=str(FIX),cases=RESULT))
print(json.dumps({k:v.get('rc','observed') for k,v in RESULT.items()},ensure_ascii=False,indent=2))
print('All assertions confirm observations, NOT target acceptance.')
