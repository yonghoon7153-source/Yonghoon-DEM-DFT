"""Read-only submitted numerical tests; all outputs stay in new review folder."""
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT.parent
for k in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[k] = '1'
os.environ['TMP'] = os.environ['TEMP'] = str(ROOT / 'tmp')
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
os.environ['PYTHONPATH'] = os.pathsep.join(str(p) for p in (
    ROOT/'source/scripts', ROOT/'source/webapp',
    WORK/'lhs_coverage_review_20260930/deps', WORK/'gen2_network_reverify3_20261007/deps'))
rows = []
for name in ('test_l214r_r01_restored_full.py', 'test_l214r_r04_cf_label.py'):
    start = time.perf_counter()
    run = subprocess.run([sys.executable, '-X', 'utf8', '-B', str(ROOT/'source/scripts'/name)],
                         cwd=ROOT/'source', env=os.environ, capture_output=True, text=True, encoding='utf8')
    target = ROOT/'evidence'/('rr_numeric_submitted_'+name.removesuffix('.py')+'.log')
    target.write_text(run.stdout + '\n--- STDERR ---\n' + run.stderr, encoding='utf8')
    row = dict(test=name, rc=run.returncode, elapsed=time.perf_counter()-start,
               tail=run.stdout.splitlines()[-4:], log=str(target))
    rows.append(row)
    print(json.dumps(row, ensure_ascii=False), flush=True)
(ROOT/'evidence/rr_numeric_submitted.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding='utf8')
sys.exit(int(any(r['rc'] for r in rows)))
