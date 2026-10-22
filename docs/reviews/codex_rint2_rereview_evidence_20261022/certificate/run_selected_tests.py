"""Run only bounded certificate regression groups; source is never modified."""
import os
from pathlib import Path
import subprocess
import sys

here = Path(__file__).resolve().parent
source = Path(os.environ.get('RINT_REVIEW_SOURCE', str(here.parent / 'source'))).resolve() / 'scripts'
groups = 'T1,T2,T3,T6,T7,T8,T10,T11,T13,T15,T16,T19,T21'
run = subprocess.run([sys.executable, '-B', str(source / 'test_step3_target_cert.py'), '--only', groups],
                     capture_output=True, text=True, encoding='utf-8', env=os.environ.copy())
(here / 'selected_target_tests.log').write_text(run.stdout + run.stderr, encoding='utf-8')
print(run.stdout[-1200:])
print(run.stderr[-1200:])
print('exit_code:', run.returncode)
sys.exit(run.returncode)
