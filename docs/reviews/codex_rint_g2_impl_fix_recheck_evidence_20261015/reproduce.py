"""Portable CPU-only rerun entry point; no git, network, MPI or scheduler."""
from pathlib import Path
import argparse,json,os,subprocess,sys,time,hashlib
R=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--baselines',action='store_true');args=ap.parse_args()
for p in ('tmp','evidence/replayed'):(R/p).mkdir(parents=True,exist_ok=True)
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONIOENCODING='utf-8',
    OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',
    TEMP=str(R/'tmp'),TMP=str(R/'tmp'),TMPDIR=str(R/'tmp'))
jobs=[('boundary',['probes/boundary_recheck.py']),('rrm',['probes/rrm_recheck.py']),
      ('join_independent',['probes/join_independent.py']),('join_parent',['probes/join_parent_replay.py']),
      ('vox',['probes/vox_binding.py']),('off_pre_impl',['probes/off_compatibility.py']),
      ('off_pre_fix',['probes/off_before_fix.py']),('owner',['probes/owner_independent.py'])]
if args.baselines:jobs.append(('baselines',['run_review_tests.py']))
rows=[]
for name,cmdargs in jobs:
    t=time.time();cmd=[sys.executable,'-X','utf8','-B',*cmdargs]
    p=subprocess.run(cmd,cwd=R,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=900)
    (R/'evidence/replayed'/f'{name}.log').write_bytes(p.stdout)
    if name=='rrm' and p.returncode==0:
        json.loads(p.stdout.decode('utf8'))
        (R/'evidence/rrm_recheck.json').write_bytes(p.stdout)
    row={'name':name,'command':cmd,'rc':p.returncode,'seconds':time.time()-t,
         'stdout_sha256':hashlib.sha256(p.stdout).hexdigest()}
    rows.append(row);print(json.dumps(row),flush=True)
    (R/'evidence/replayed/runs.json').write_text(json.dumps(rows,indent=2),encoding='utf8')
sys.exit(0 if all(r['rc']==0 for r in rows) else 1)
