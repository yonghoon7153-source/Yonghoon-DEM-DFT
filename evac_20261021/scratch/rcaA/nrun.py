#!/usr/bin/env python3
"""Low-priority runner: nrun.py <script.py> [args...] -> os.nice(19), single-thread BLAS/OpenMP, then run the script as __main__
(prints wall time).  Thread caps are set before numpy/scipy are imported (they read these at import)."""
import os
import runpy
import sys
import time

for _k in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
    os.environ[_k] = '1'
os.nice(19)
script = sys.argv[1]
sys.argv = [script] + sys.argv[2:]
sys.path.insert(0, os.path.dirname(os.path.abspath(script)))
t0 = time.time()
code = 0
try:
    runpy.run_path(script, run_name='__main__')
except SystemExit as e:
    code = e.code if isinstance(e.code, int) else (0 if e.code is None else 1)
finally:
    sys.stdout.flush()
    print(f'[nrun] wall {time.time() - t0:.1f} s · exit {code}', file=sys.stderr, flush=True)
sys.exit(code)
