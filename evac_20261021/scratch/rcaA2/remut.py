"""Re-run chosen mutants of mutsweep.py against the CURRENT worktree test file (one temp module each, removed after).
usage: python3 remut.py M10 M12 M27 ..."""
import os
import shutil
import subprocess
import sys
import tempfile

D = '/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/rcaA2/'
WT = '/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a1ea4b71aa06a03ee'
src = open(D + 'mutsweep.py', encoding='utf-8').read()
head, rest = src.split('\nMUTS = [', 1)
body, _tail = rest.split('\n]\n', 1)
ns = {}
exec('MUTS = [' + body + '\n]\n', {'CJ': 'carbon_junction.py', 'CW': 'ca_ext_cjunc.py', 'S0': 'ca_s0_census.py',
                                   'S3': 'step3_sigma.py'}, ns)
want = set(sys.argv[1:])
for m in ns['MUTS']:
    key = m[0].split()[0]
    if key not in want:
        continue
    nm, fn, old, new, kind, tags = m
    assert kind == 'cj', (key, kind)
    s = open(os.path.join(WT, 'scripts', fn), encoding='utf-8').read()
    assert s.count(old) == 1, (key, s.count(old))
    td = tempfile.mkdtemp(prefix='remut_', dir=D)
    try:
        open(os.path.join(td, fn), 'w', encoding='utf-8').write(s.replace(old, new))
        env = dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1')
        p = subprocess.run([sys.executable, D + 'drv.py', '--impl', td, '--mods', fn[:-3], '--', '--only', tags],
                           capture_output=True, text=True, timeout=900, env=env, cwd=WT)
        out = p.stdout + p.stderr
        fails = [ln.strip()[:150] for ln in out.splitlines() if ln.strip().startswith('FAIL ')]
        summ = [ln for ln in out.splitlines() if 'test_carbon_junction:' in ln]
        print(key, tags, '|', summ[-1] if summ else out[-200:], '| rc', p.returncode)
        for f in fails:
            print('    ', f)
    finally:
        shutil.rmtree(td, ignore_errors=True)
