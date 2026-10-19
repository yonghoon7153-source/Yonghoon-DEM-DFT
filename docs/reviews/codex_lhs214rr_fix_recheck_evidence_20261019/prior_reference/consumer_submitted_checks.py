"""Run the submitted R02 test unchanged with explicit environment; retain log."""
from pathlib import Path
import json
import os
import subprocess
import sys
import time

review = Path(__file__).resolve().parents[1]
workspace = review.parent
deps = [workspace / 'lhs_coverage_review_20260930/deps', workspace / 'gen2_network_reverify3_20261007/deps']
env = dict(os.environ)
env.update(PYTHONPATH=os.pathsep.join(map(str, deps)), PYTHONUTF8='1', PYTHONIOENCODING='utf-8',
           PYTHONDONTWRITEBYTECODE='1', TMP=str(review / 'tmp'), TEMP=str(review / 'tmp'))
env.update({k:'1' for k in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS')})
name = 'scripts/test_l214r02_model_limit_flag.py'
cmd = [sys.executable, '-X', 'utf8', '-B', str(review / 'source' / name)]
t0 = time.monotonic()
r = subprocess.run(cmd, cwd=review / 'source', env=env, capture_output=True)
out = r.stdout.decode('utf-8', errors='backslashreplace')
err = r.stderr.decode('utf-8', errors='backslashreplace')
(review / 'evidence/consumer_submitted_r02.log').write_text(out + '\nSTDERR\n' + err, encoding='utf-8')
result = dict(test=name, rc=r.returncode, seconds=time.monotonic()-t0, tail=out.splitlines()[-8:], stderr_tail=err.splitlines()[-5:])
(review / 'evidence/consumer_submitted_r02.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(result, ensure_ascii=False, indent=2))
