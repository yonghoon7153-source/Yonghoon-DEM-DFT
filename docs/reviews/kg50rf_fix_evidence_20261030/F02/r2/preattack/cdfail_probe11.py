#!/usr/bin/env python3
"""[10-30 고친 도구 인자 11 에 맞춘 사본 — 리뷰어 원본 바이트에서 바꾼 곳만: 인자 끝 체크포인트 · 재개 덱 · 시험 덱 · 체크포인트 파일 만듦]
Render the canonical runner with the tool's own runnerck, then run it with bash after the work folder is gone.
Shows whether mpirun still starts (and in which cwd) when `cd` fails.  Fake mpirun prints its cwd and -in."""
import os, subprocess, sys, tempfile

tool = sys.argv[1]
src = open(tool, encoding='utf-8').read()
a = src.index("runnerck(){ python3 -I - \"$@\" <<'PY'\n") + len("runnerck(){ python3 -I - \"$@\" <<'PY'\n")
code = src[a:src.index('\nPY\n}', a)] + '\n'
tmp = tempfile.mkdtemp(prefix='cdfail_')
W = os.path.join(tmp, 'root', 'case1')
os.makedirs(os.path.join(W, 'restart_case1'))
sub = os.path.join(tmp, 'submitdir')
os.makedirs(sub)
bindir = os.path.join(tmp, 'bin')
os.makedirs(bindir)
with open(os.path.join(bindir, 'mpirun'), 'w') as f:
    f.write('#!/bin/sh\necho "FAKE mpirun cwd=$(pwd -P) args=$*"\n')
os.chmod(os.path.join(bindir, 'mpirun'), 0o755)
C, SFX, NP = 'case1', 'r4', '4'
helper = os.path.join(tmp, 'helper.sh')
with open(helper, 'w') as f:
    f.write('#!/bin/bash\n#SBATCH --job-name=case1_r4\n#SBATCH --output=logs/output_case1_r4_%%j.out\n#SBATCH -n 4\n'
            '#SBATCH --time=01:00:00\ncd %s\nmpirun --oversubscribe --bind-to none -np 4 lmp_mpi -in input_case1_r4.liggghts\n' % W)
D, TD = os.path.join(W, 'input_case1_r4.liggghts'), os.path.join(W, 'input_case1_r4t.liggghts')
CK = os.path.join(os.path.realpath(W), 'restart_case1', 'restart_settling_1.bin')
for _p, _b in ((D, b'run 1\n'), (TD, b'run 1\n'), (CK, b'\x00' * 64)):
    open(_p, 'wb').write(_b)
OM, OT = os.path.join(sub, 'run_main.sh'), os.path.join(sub, 'run_trial.sh')   # write runners outside W so they survive
p = subprocess.run(['python3', '-I', '-', helper, C, SFX, NP, W, os.path.realpath(W), D, TD, OM, OT, CK], input=code.encode(),
                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
print('runnerck rc', p.returncode)
os.rename(os.path.join(tmp, 'root'), os.path.join(tmp, 'root_moved'))       # work folder gone before the job starts
env = dict(os.environ, PATH=bindir + ':' + os.environ['PATH'])
q = subprocess.run(['bash', OM], cwd=sub, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
print('runner rc', q.returncode)
print(q.stdout.decode()[-600:])
subprocess.run(['rm', '-rf', tmp])
