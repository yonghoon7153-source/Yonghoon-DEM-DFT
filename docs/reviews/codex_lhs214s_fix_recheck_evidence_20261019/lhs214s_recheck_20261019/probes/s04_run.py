"""Read-only S04 test runner; all runtime outputs stay under s04 evidence."""
import json
import os
from pathlib import Path
import subprocess
import sys
import time

REVIEW = Path(__file__).resolve().parents[1]
tag, script, *args = sys.argv[1:]
env = os.environ.copy()
env['PYTHONPATH'] = os.pathsep.join(str(REVIEW.parent / p) for p in (
    'lhs_coverage_review_20260930/deps', 'gen2_network_reverify3_20261007/deps'))
for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    env[key] = '1'
work = REVIEW / 'evidence' / ('s04_' + tag + '_runtime')
work.mkdir(parents=True, exist_ok=True)
for key in ('TMP', 'TEMP', 'TMPDIR'):
    env[key] = str(work)
for key, name in (('WEBAPP_UPLOAD_FOLDER', 'uploads'), ('WEBAPP_RESULTS_FOLDER', 'results'),
                  ('WEBAPP_ARCHIVE_FOLDER', 'archive'), ('WEBAPP_MPM_LAB_FOLDER', 'mpm'), ('MPLCONFIGDIR', 'mpl')):
    env[key] = str(work / name)
env['SUPABASE_URL'] = env['SUPABASE_KEY'] = ''
env['PYTHONDONTWRITEBYTECODE'] = '1'
env['PYTHONIOENCODING'] = 'utf-8'
command = [sys.executable, '-X', 'utf8', '-B', str(REVIEW / script), *args]
start = time.monotonic()
p = subprocess.run(command, cwd=REVIEW / 'source', env=env, text=True, encoding='utf-8', errors='replace', capture_output=True)
log = REVIEW / 'evidence' / ('s04_' + tag + '.log')
log.write_text(p.stdout + '\nSTDERR\n' + p.stderr, encoding='utf-8')
result = dict(command=command, returncode=p.returncode, seconds=round(time.monotonic()-start, 3), log=str(log))
(REVIEW / 'evidence' / ('s04_' + tag + '_run.json')).write_text(json.dumps(result, indent=2), encoding='utf-8')
print(json.dumps(result))
print('\n'.join(p.stdout.splitlines()[-4:]))
sys.exit(p.returncode)
