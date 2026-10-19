"""Run unmodified old/new submitted R01 tests, keeping complete stdout/stderr."""
from pathlib import Path
import hashlib
import json
import os
import platform
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT.parent
label = sys.argv[1]
SOURCE = ROOT / 'source' if label == 'new' else WORK / 'lhs214rr_recheck_20261019/source'
tmp = ROOT / 'tmp' / ('s02_' + label)
tmp.mkdir(parents=True, exist_ok=True)
env = os.environ.copy()
env.update({k: '1' for k in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS')})
env['TEMP'] = env['TMP'] = str(tmp)
env['PYTHONDONTWRITEBYTECODE'] = '1'
env['PYTHONPATH'] = os.pathsep.join(str(p) for p in (
    SOURCE / 'scripts', SOURCE / 'webapp',
    WORK / 'lhs_coverage_review_20260930/deps', WORK / 'gen2_network_reverify3_20261007/deps'))
target = SOURCE / 'scripts/test_l214r_r01_restored_full.py'
cmd = [sys.executable, '-X', 'utf8', '-B', str(target)]
start = time.perf_counter()
run = subprocess.run(cmd, cwd=SOURCE, env=env, capture_output=True, text=True, encoding='utf8')
elapsed = time.perf_counter() - start
log = ROOT / 'evidence' / f's02_{label}_full.log'
log.write_text(run.stdout + '\n--- STDERR ---\n' + run.stderr, encoding='utf8')
metadata = dict(label=label, source=str(SOURCE), sha256=hashlib.sha256(target.read_bytes()).hexdigest(),
                command=cmd, cwd=str(SOURCE), python=sys.version, platform=platform.platform(),
                returncode=run.returncode, seconds=elapsed, stdout_tail=run.stdout.splitlines()[-3:],
                env={k: env[k] for k in ('PYTHONPATH', 'TMP', 'TEMP', 'OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS')}, log=str(log))
(ROOT / 'evidence' / f's02_{label}_full.json').write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding='utf8')
print(json.dumps(metadata, ensure_ascii=False))
sys.exit(run.returncode)
