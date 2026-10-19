"""Isolated, logged execution of the assigned display review tests."""
import json
import os
from pathlib import Path
import subprocess
import sys
import time

review = Path(__file__).resolve().parents[1]
workspace = review.parent
tag, script, *args = sys.argv[1:]
env = os.environ.copy()
env['PYTHONPATH'] = os.pathsep.join(str(workspace / p) for p in (
    'lhs_coverage_review_20260930/deps', 'gen2_network_reverify3_20261007/deps'))
for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    env[key] = '1'
isolated = review / 'evidence' / ('rr_display_' + tag + '_work')
isolated.mkdir(parents=True, exist_ok=True)
for key in ('TMP', 'TEMP', 'TMPDIR'):
    env[key] = str(isolated)
for key, name in (('WEBAPP_UPLOAD_FOLDER', 'uploads'), ('WEBAPP_RESULTS_FOLDER', 'results'),
                  ('WEBAPP_ARCHIVE_FOLDER', 'archive'), ('WEBAPP_MPM_LAB_FOLDER', 'mpm'), ('MPLCONFIGDIR', 'mpl')):
    env[key] = str(isolated / name)
env['SUPABASE_URL'] = env['SUPABASE_KEY'] = ''
env['PYTHONDONTWRITEBYTECODE'] = '1'
env['PYTHONIOENCODING'] = 'utf-8'
command = [sys.executable, '-X', 'utf8', '-B', str(review / script), *args]
start = time.monotonic()
p = subprocess.run(command, cwd=review / 'source', env=env, text=True, encoding='utf-8', errors='replace', capture_output=True)
log = review / 'evidence' / ('rr_display_' + tag + '.log')
log.write_text(p.stdout + '\nSTDERR\n' + p.stderr, encoding='utf-8')
result = dict(command=command, returncode=p.returncode, seconds=round(time.monotonic()-start, 3), log=str(log))
(review / 'evidence' / ('rr_display_' + tag + '_run.json')).write_text(json.dumps(result, indent=2), encoding='utf-8')
print(json.dumps(result))
print('\n'.join(p.stdout.splitlines()[-3:]))
sys.exit(p.returncode)
