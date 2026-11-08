"""탐침 여럿을 차례로 (같은 env · 출력 = <out_dir>/<이름>_<꼬리>.out) — 쓰임: run_probes.py <scripts 뿌리> <탐침 폴더> <출력 폴더> <꼬리> <탐침 이름[:인자,인자…]> …"""
import os
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
scripts, pdir, odir, tail = sys.argv[1:5]
odir = Path(odir)
odir.mkdir(parents=True, exist_ok=True)
env = dict(os.environ, PA13_SCRIPTS=scripts, TMPDIR=str(HERE / 'tmp'))
for spec in sys.argv[5:]:
    name, _, arg = spec.partition(':')
    argv = [sys.executable, str(Path(pdir) / f'{name}.py')] + (arg.split(',') if arg else [])
    t0 = time.time()
    r = subprocess.run(argv, cwd=str(HERE / 'tmp'), env=env, capture_output=True, text=True, timeout=3600)
    lab = name + (('_' + arg.replace(',', '_')) if arg else '')
    (odir / f'{lab}_{tail}.out').write_text(r.stdout + (('\n[stderr]\n' + r.stderr) if r.stderr.strip() else ''), encoding='utf-8')
    print(f'{lab} rc={r.returncode} {time.time() - t0:.1f}s', flush=True)
