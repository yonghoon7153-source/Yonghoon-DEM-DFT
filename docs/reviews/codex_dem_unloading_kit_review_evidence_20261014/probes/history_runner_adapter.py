"""Windows/Git Bash adapter for unchanged main runner; fake executables only.

Adapter changes path separators in generated fake scripts and environment,
adds -X utf8 to Python invocations, and chooses Git Bash (never WSL).
Source run_unload.sh and copied ul_reader.py are byte-for-byte unchanged.
"""
from pathlib import Path
import json
import os
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
KIT = ROOT / 'source/docs/data/ps45_unload_20261009'
sys.path.insert(0, str(KIT))
import ul_runner_test as T
import ul_reader as R
RUN = ROOT / 'evidence' / ('history_runner_' + str(time.time_ns()))
RUN.mkdir()
kit, work, log = T._setup(str(RUN))
for p in (RUN / 'bin').iterdir():
    txt = p.read_text()
    txt = txt.replace('\\', '/')
    txt = txt.replace(Path(sys.executable).as_posix(), Path(sys.executable).as_posix() + ' -X utf8')
    p.write_text(txt, newline='\n')
py = RUN / 'bin/py'
py.write_text('#!/bin/bash\nexec ' + Path(sys.executable).as_posix() + ' -X utf8 "$@"\n', newline='\n')
env = T._env(str(RUN), kit)
for k in ('WORK_ROOT', 'MPIRUN', 'LMP'):
    env[k] = env[k].replace('\\', '/')
env['PY'] = py.as_posix()
env['PATH'] = 'C:/Program Files/Git/bin;C:/Program Files/Git/usr/bin;' + env['PATH']
env['UL_KIT'] = '1'  # avoid relying on source Git metadata; sealed copied kit still checked
env['MSYS2_ARG_CONV_EXCL'] = ''
results = []

def run(job, **extra):
    p = subprocess.run(['C:/Program Files/Git/bin/bash.exe', Path(kit, 'run_unload.sh').as_posix(), T.B73, job],
                       env=dict(env, **extra), capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=60)
    name = str(len(results)) + '_' + job
    (RUN / (name + '.stdout.txt')).write_text(p.stdout, encoding='utf-8')
    (RUN / (name + '.stderr.txt')).write_text(p.stderr, encoding='utf-8')
    results.append({'job':job,'extra':extra,'rc':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
    return p

bed = Path(work) / T.B73
(bed / 'RJ').mkdir()
(bed / 'RJ/restore_verdict.json').write_text('{"status":"RESTORED"}')
(bed / 'ke_base.json').write_text('{"s2_limit":1.0,"trans":1.0,"rot":0.0}')
(bed / 'ul_base.in').write_text('variable ul_s2lim equal 1.0\n')
p = run('UB')
if p.returncode == 0:
    # No machine failure: completed UB still accepted for RESUME.
    run('UB', RESUME='1')
    run('UB', RESUME='1')
    # RJ/G cases never write screen_a2; this replays the whole operation.
    run('RJ', RESUME='1')
    run('RJ', RESUME='1')
(ROOT / 'evidence/history_runner_adapter_results.json').write_text(json.dumps({'run_dir':str(RUN),'results':results}, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'run_dir':str(RUN),'results':[{k:v for k,v in r.items() if k not in ('stdout','stderr')} for r in results],
                  'last_stdout': results[-1]['stdout'][-2000:], 'last_stderr': results[-1]['stderr'][-2000:]}, ensure_ascii=False, indent=2))
