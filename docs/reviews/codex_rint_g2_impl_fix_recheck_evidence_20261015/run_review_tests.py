"""Review-only regression runner; never edits the pinned source."""
from pathlib import Path
import subprocess, os, json, time, hashlib, sys

R = Path(__file__).resolve().parent
PY = Path(sys.executable)
env = dict(os.environ, PYTHONPATH=os.pathsep.join(
    ([str(R/'support')] if os.name == 'nt' else []) + [str(R/'source/scripts'),
    str(R.parent/'lhs_coverage_review_20260930/deps'),
    str(R.parent/'gen2_network_reverify3_20261007/deps')] +
    [p for p in os.environ.get('PYTHONPATH','').split(os.pathsep) if p]),
    PYTHONDONTWRITEBYTECODE='1', PYTHONIOENCODING='utf-8',
    OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1',
    TEMP=str(R/'tmp'), TMP=str(R/'tmp'), TMPDIR=str(R/'tmp'))
jobs = [['test_rint_g2_am_iface.py'], ['test_rint_g2_rrm.py'],
        ['test_rint_g2_join.py'], ['test_rint_t4_census.py'],
        ['test_rint_t43_order.py'], ['test_rint_t2_dev.py'],
        ['step3_sigma.py','--selftest'], ['step3_sigma.py','--selftest-rint'],
        ['rint_t41_census.py','--selftest']]
rows = []
for args in jobs:
    name = '_'.join(args).replace('.py','').replace('--','')
    cmd = [str(PY), '-X', 'utf8', '-B', 'scripts/'+args[0], *args[1:]]
    t = time.time()
    p = subprocess.run(cmd, cwd=R/'source', env=env, stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT, timeout=600)
    (R/'evidence'/('baseline_'+name+'.log')).write_bytes(p.stdout)
    row = dict(command=cmd, rc=p.returncode, seconds=time.time()-t,
               log_sha256=hashlib.sha256(p.stdout).hexdigest())
    rows.append(row)
    (R/'evidence/baseline_tests.json').write_text(json.dumps(rows, indent=2), encoding='utf8')
    print(json.dumps(row), flush=True)
