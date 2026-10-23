"""Launcher: nice 19 + single-thread BLAS + RINT_REVIEW_SOURCE, then run a script (runpy) with its own argv.
usage: python3 -I -B run.py <src_tree|-> <script.py> [args...]
The script's own directory is put first on sys.path (as plain `python script.py` would; -I drops it)."""
import os
import runpy
import sys

os.nice(19)
for k in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[k] = '1'
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
sys.dont_write_bytecode = True
src, script = sys.argv[1], sys.argv[2]
if src != '-':
    os.environ['RINT_REVIEW_SOURCE'] = src
sys.path.insert(0, os.path.dirname(os.path.abspath(script)))
sys.argv = [script] + sys.argv[3:]
runpy.run_path(script, run_name='__main__')
