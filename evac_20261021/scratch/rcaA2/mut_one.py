"""Run worktree test groups against ONE source mutant of a worktree module (temp dir with just that file · removed after).
usage: python3 mut_one.py <module.py> <old-snippet-file> <new-snippet-file> <tags>"""
import os
import shutil
import subprocess
import sys
import tempfile

WT = '/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a1ea4b71aa06a03ee'
D = '/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/rcaA2/'
fn, oldf, newf, tags = sys.argv[1:5]
old = open(oldf, encoding='utf-8').read()
new = open(newf, encoding='utf-8').read()
src = open(os.path.join(WT, 'scripts', fn), encoding='utf-8').read()
assert src.count(old) == 1, src.count(old)
td = tempfile.mkdtemp(prefix='mut1_', dir=D)
try:
    open(os.path.join(td, fn), 'w', encoding='utf-8').write(src.replace(old, new))
    mod = fn[:-3]
    env = dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1')
    p = subprocess.run([sys.executable, D + 'drv.py', '--impl', td, '--mods', mod, '--', '--only', tags], capture_output=True,
                       text=True, timeout=900, env=env, cwd=WT)
    out = p.stdout + p.stderr
    for ln in out.splitlines():
        if ln.strip().startswith('FAIL ') or 'test_carbon_junction:' in ln:
            print(ln[:260])
    print('rc', p.returncode)
finally:
    shutil.rmtree(td, ignore_errors=True)
