"""Run review-only regression tests; no production command or Git mutation."""
from pathlib import Path
import json,os,subprocess,sys,time
R=Path(__file__).resolve().parent
env=os.environ.copy()
env.update(PYTHONDONTWRITEBYTECODE='1',PYTHONUTF8='1',OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',TEMP=str(R/'tmp'),TMP=str(R/'tmp'))
env['PYTHONPATH']=os.pathsep.join(str(p) for p in [R/'source/scripts',R/'source/webapp',R.parent/'lhs_coverage_review_20260930/deps',R.parent/'gen2_network_reverify3_20261007/deps'])
tasks=[('receipt',['scripts/supp20_input_receipt.py','--selftest']),('release',['scripts/test_lhs_release_v13.py']),('provenance',['webapp/test_pipeline_provenance.py']),('reread',['scripts/g2_network_reread.py','--selftest']),('reread_v12',['scripts/test_reread_v12.py'])]
suffix=sys.argv[1] if len(sys.argv)>1 else ''
if suffix:tasks=[t for t in tasks if t[0]!='provenance']
rows=[]
for name,args in tasks:
    t=time.monotonic();p=subprocess.run([sys.executable,'-X','utf8','-B',*args],cwd=R/'source',env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=900)
    (R/'evidence'/f'baseline_{name}{suffix}.log').write_bytes(p.stdout)
    row={'name':name,'command':args,'rc':p.returncode,'seconds':time.monotonic()-t,'log':f'evidence/baseline_{name}{suffix}.log'}
    rows.append(row);print(json.dumps(row),flush=True)
    (R/'evidence'/f'baseline_root{suffix}.json').write_text(json.dumps(rows,indent=2),encoding='utf8')
