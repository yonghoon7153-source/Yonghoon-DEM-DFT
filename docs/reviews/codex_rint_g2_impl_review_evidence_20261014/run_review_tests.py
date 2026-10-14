from pathlib import Path
import subprocess, os, json, time, hashlib, shutil
R=Path(__file__).resolve().parent
PY=Path('C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe')
env=dict(os.environ, PYTHONPATH=os.pathsep.join([str(R/'source/scripts'),str(R.parent/'lhs_coverage_review_20260930/deps'),str(R.parent/'gen2_network_reverify3_20261007/deps')]), PYTHONDONTWRITEBYTECODE='1', PYTHONIOENCODING='utf-8', OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1', TEMP=str(R/'tmp'),TMP=str(R/'tmp'),TMPDIR=str(R/'tmp'))
jobs=[['test_rint_g2_am_iface.py'],['test_rint_g2_rrm.py'],['test_rint_g2_join.py'],['test_rint_t4_census.py'],['test_rint_t43_order.py'],['test_rint_t2_dev.py'],['step3_sigma.py','--selftest'],['step3_sigma.py','--selftest-rint']]
rows=[]
for args in jobs:
    name='_'.join(args).replace('.py','').replace('--','')
    t=time.time()
    p=subprocess.run([str(PY),'-X','utf8','-B','scripts/'+args[0],*args[1:]],cwd=R/'source',env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=600)
    (R/'evidence'/('baseline_'+name+'.log')).write_bytes(p.stdout)
    row={'args':args,'rc':p.returncode,'seconds':time.time()-t,'log_sha256':hashlib.sha256(p.stdout).hexdigest()}
    rows.append(row);print(json.dumps(row),flush=True)
(R/'evidence/baseline_tests.json').write_text(json.dumps(rows,indent=2),encoding='utf8')
