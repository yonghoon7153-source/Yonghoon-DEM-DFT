"""Rerun prior independent probes without changing their numerical content."""
from pathlib import Path
import subprocess,os,json,hashlib,time,sys
R=Path(__file__).resolve().parent
env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1',PYTHONIOENCODING='utf-8',
         OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',
         TEMP=str(R/'tmp'),TMP=str(R/'tmp'),TMPDIR=str(R/'tmp'))
jobs=[('vox_original',['probes/owner_vox_mismatch.py']),
      ('off_pre_impl',['probes/off_compatibility.py']),
      ('off_pre_fix',['probes/off_before_fix.py']),
      ('owner_independent',['probes/owner_independent.py'])]
rows=[]
for name,args in jobs:
    cmd=[sys.executable,'-X','utf8','-B',*args]
    t=time.time()
    p=subprocess.run(cmd,cwd=R,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=900)
    (R/'evidence'/f'{name}.log').write_bytes(p.stdout)
    rows.append({'name':name,'command':cmd,'rc':p.returncode,'seconds':time.time()-t,
                 'log_sha256':hashlib.sha256(p.stdout).hexdigest()})
    (R/'evidence/parent_probe_runs.json').write_text(json.dumps(rows,indent=2),encoding='utf8')
    print(json.dumps(rows[-1]),flush=True)
