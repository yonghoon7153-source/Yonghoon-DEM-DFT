"""Run repro_codex.py under OPENBLAS_CORETYPE=Haswell and the default path; print a compact table."""
import json
import os
import subprocess
import sys

scripts = sys.argv[1]
here = os.path.dirname(os.path.abspath(__file__))
for ct in ('Haswell', None):
    env = {k: v for k, v in os.environ.items() if k not in ('PYTHONPATH', 'OPENBLAS_CORETYPE')}
    env['OPENBLAS_NUM_THREADS'] = '1'
    if ct:
        env['OPENBLAS_CORETYPE'] = ct
    p = subprocess.run([sys.executable, '-I', os.path.join(here, 'repro_codex.py'), scripts], capture_output=True, text=True, env=env)
    d = json.loads(p.stdout)
    print(f'== OPENBLAS_CORETYPE={ct or "default"}')
    for k, v in d.items():
        print(f"  {k:9s} rel_err {v['rel_err']:+.12e}  A {v['pass_a']} B {v['pass_b']} C {v['pass_c']} D {v['pass_d']} ok {v['ok']}  "
              f"imb {v['imbalance']:.4e}  err_bound {v['target_err_bound_rel']}")
