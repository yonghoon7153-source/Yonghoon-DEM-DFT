import os, sys, subprocess, json
from pathlib import Path
E = Path(__file__).resolve().parent
C = Path(os.environ.get('LHS_REVIEW_REPO',E.parent/'lhs_coverage_review_20260930/candidate'))
os.environ.update(PYTHONDONTWRITEBYTECODE='1', PYTHONUTF8='1', PYTHONIOENCODING='utf-8')
tests = [('scripts/lhs_descriptor_harvest.py',['--selftest']),('scripts/plastic_coverage.py',['--selftest']),('scripts/coverage_physics_vs_hertzian.py',['--selftest']),('scripts/lhs_webapp_batch.py',['--selftest']),('webapp/test_pipeline_provenance.py',[]),('scripts/lhs_design_dataset.py',['--selftest'])]
tests.insert(0, ('scripts/lens_geometry.py',['--selftest']))
results=[]
for name,args in tests:
    p=subprocess.run([sys.executable,name,*args],cwd=C,encoding='utf-8',errors='replace',capture_output=True)
    (E/(Path(name).stem+'.log')).write_text(p.stdout+p.stderr,encoding='utf-8')
    results.append({'test':name,'returncode':p.returncode,'tail':(p.stdout+p.stderr).splitlines()[-4:]})
    print(results[-1],flush=True)
(E/'selftests.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
