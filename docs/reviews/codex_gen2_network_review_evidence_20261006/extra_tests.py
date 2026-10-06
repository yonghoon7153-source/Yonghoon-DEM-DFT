from pathlib import Path
import os, sys, subprocess, json
R=Path(__file__).resolve().parent
sys.stdout.reconfigure(encoding='utf8')
env=dict(os.environ,PYTHONUTF8='1',PYTHONDONTWRITEBYTECODE='1',OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1')
env['PYTHONPATH']=os.pathsep.join([str(R.parent/'lhs_coverage_review_20260930/deps'),str(R/'source/scripts'),str(R/'source/webapp')])
paths=['scripts/lhs_release_build.py','scripts/constriction_reference.py','docs/data/gen2_design_20261006/c1/fv_sphere_chain.py']
rows=[]
for p in paths:
    x=subprocess.run([sys.executable,p,'--selftest'],cwd=R/'source',env=env,capture_output=True,text=True,encoding='utf8',errors='strict',timeout=240)
    log=x.stdout+x.stderr
    (R/'evidence'/(Path(p).stem+'_selftest.log')).write_text(log,encoding='utf8')
    row=dict(path=p,rc=x.returncode,tail=log.splitlines()[-5:]);rows.append(row);print(json.dumps(row,ensure_ascii=False),flush=True)
(R/'evidence/extra_tests.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False),encoding='utf8')
