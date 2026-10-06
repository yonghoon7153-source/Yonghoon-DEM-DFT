"""Run one Codex probe copy under `python3 -I -B`, adding only the user site (dateutil · requests live there on this machine).

usage: python3 -I -B run_isolated.py <user_site_dir> <probe.py> <cwd>
The probe computes its bundle root from its own __file__ (parents[1]) — we keep that by running it with runpy.run_path.
Children the probe spawns inherit PYTHONDONTWRITEBYTECODE=1 · single-thread BLAS env · cwd = <cwd> (an empty scratch dir).
"""
import os
import runpy
import sys

site_dir, probe, cwd = sys.argv[1], os.path.abspath(sys.argv[2]), os.path.abspath(sys.argv[3])
if site_dir not in sys.path:
    sys.path.append(site_dir)
os.environ.update(PYTHONDONTWRITEBYTECODE='1', OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1',
                  MPLBACKEND='Agg')
os.environ.pop('PYTHONPATH', None)
os.chdir(cwd)
sys.argv = [probe]
runpy.run_path(probe, run_name='__main__')
