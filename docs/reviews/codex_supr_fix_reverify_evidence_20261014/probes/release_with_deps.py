"""Unchanged release regression with already-installed scientific dependencies."""
from pathlib import Path
import json, os, subprocess, sys, time
R=Path(__file__).resolve().parents[1]
S=R/'source'
deps=[R.parent/'lhs_coverage_review_20260930/deps', R.parent/'gen2_network_reverify3_20261007/deps']
env=dict(os.environ, PYTHONUTF8='1', PYTHONDONTWRITEBYTECODE='1',
         PYTHONPATH=os.pathsep.join(map(str, deps)),
         OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1',
         TEMP=str(R/'tmp'), TMP=str(R/'tmp'), TMPDIR=str(R/'tmp'))
start=time.monotonic()
p=subprocess.run([sys.executable,'-X','utf8','-B','scripts/test_lhs_release_v13.py'],
                 cwd=S,env=env,capture_output=True,timeout=240)
(R/'evidence/release_v13_with_deps.log').write_bytes(p.stdout+p.stderr)
result=dict(rc=p.returncode,seconds=time.monotonic()-start,dependency_dirs=list(map(str,deps)),
            failures=[s for s in (p.stdout+p.stderr).decode('utf8','replace').splitlines() if 'FAIL' in s])
(R/'evidence/release_v13_with_deps.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(result,ensure_ascii=False))
