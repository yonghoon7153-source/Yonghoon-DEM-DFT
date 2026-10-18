"""Run a read-only review command with isolated temporary/output directories."""
import json
import os
from pathlib import Path
import subprocess
import sys
import time

review = Path(__file__).resolve().parents[1]
workspace = review.parent
env = os.environ.copy()
env['PYTHONPATH'] = os.pathsep.join(str(workspace / p) for p in (
    'lhs_coverage_review_20260930/deps', 'gen2_network_reverify3_20261007/deps'))
for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    env[key] = '1'
for key in ('TMP', 'TEMP', 'TMPDIR'):
    env[key] = str(review / 'tmp')
env['PYTHONDONTWRITEBYTECODE'] = '1'
env['PYTHONIOENCODING'] = 'utf-8'
tag, script, *args = sys.argv[1:]
command = [sys.executable, '-X', 'utf8', '-B', str(review / script), *args]
start = time.monotonic()
p = subprocess.run(command, cwd=review / 'source', env=env, text=True, encoding='utf-8', errors='replace', capture_output=True)
(review / f'evidence/display_{tag}.log').write_text(p.stdout + '\nSTDERR\n' + p.stderr, encoding='utf-8')
result = dict(command=command, returncode=p.returncode, seconds=round(time.monotonic()-start, 3),
              log=f'evidence/display_{tag}.log')
(review / f'evidence/display_{tag}_run.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
print(json.dumps(result))
print('\n'.join(p.stdout.splitlines()[-3:]))
sys.exit(p.returncode)
