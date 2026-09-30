"""Run the submitted CPU selftests in the isolated copy; retain failures verbatim."""
import os, sys, subprocess, json
from pathlib import Path
E = Path(__file__).resolve().parent
C = E.parent/'candidate'
W = E.parent.parent
os.environ.update(PYTHONDONTWRITEBYTECODE='1', PYTHONUTF8='1', PYTHONIOENCODING='utf-8',
                  PYTHONPATH=str(W/'lhs_coverage_review_20260930/deps'), SUPABASE_URL='', SUPABASE_KEY='')
tests = [('scripts/lens_geometry.py',['--selftest']),('scripts/plastic_coverage.py',['--selftest']),
         ('scripts/coverage_physics_vs_hertzian.py',['--selftest']),('scripts/lhs_descriptor_harvest.py',['--selftest']),
         ('webapp/test_pipeline_provenance.py',[]),('scripts/lhs_webapp_batch.py',['--selftest'])]
results = []
for name, args in tests:
    p = subprocess.run([sys.executable, name, *args], cwd=C, encoding='utf-8', errors='replace', capture_output=True)
    out = p.stdout+p.stderr
    (E/(Path(name).stem+'.log')).write_text(out, encoding='utf-8')
    rec = dict(test=name, returncode=p.returncode, tail=out.splitlines()[-5:])
    results.append(rec)
    print(json.dumps(rec, ensure_ascii=False), flush=True)
(E/'selftests.json').write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding='utf-8')
