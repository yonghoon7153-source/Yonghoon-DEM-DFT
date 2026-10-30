#!/usr/bin/env python3
"""[10-30 고친 도구 인자 11 에 맞춘 사본 — 리뷰어 원본 바이트에서 바꾼 곳만: 인자 끝 체크포인트 · 재개 덱 · 시험 덱 · 체크포인트 파일 만듦 · 그린 러너의 환경 줄 걸러내기에 ds= · [ "$ds" · command mpirun 줄 뺌]
Run the tool's embedded runnerck Python (extracted verbatim) on helper-runner variants.  Usage: rck_probe.py <tool.sh>"""
import os, subprocess, sys, tempfile

tool = sys.argv[1]
src = open(tool, encoding='utf-8').read()
a = src.index("runnerck(){ python3 -I - \"$@\" <<'PY'\n") + len("runnerck(){ python3 -I - \"$@\" <<'PY'\n")
b = src.index('\nPY\n}', a)
code = src[a:b] + '\n'

tmp = tempfile.mkdtemp(prefix='rckp_')
root = os.path.join(tmp, 'root')
W = os.path.join(root, 'kg50_d2_b50')
os.makedirs(os.path.join(W, 'restart_kg50_d2_b50'))
WR = os.path.realpath(W)
C, SFX, NP = 'kg50_d2_b50', 'r56', '56'
D = os.path.join(W, 'input_%s_%s.liggghts' % (C, SFX))
TD = os.path.join(W, 'input_%s_%st.liggghts' % (C, SFX))
OM = os.path.join(W, 'run_%s_%s.sh' % (C, SFX))
OT = os.path.join(W, 'run_%s_%st.sh' % (C, SFX))
CS = '%s_%s' % (C, SFX)
CK = os.path.join(WR, 'restart_kg50_d2_b50', 'restart_settling_250000.bin')
for _p, _b in ((D, b'run 1\n'), (TD, b'run 1\n'), (CK, b'\x00' * 64)):
    open(_p, 'wb').write(_b)
BASE = ('#!/bin/bash\n#SBATCH --job-name=%s\n#SBATCH --output=logs/output_%s_%%j.out\n#SBATCH --qos=cpu-60\n#SBATCH --partition=cpu\n'
        '#SBATCH -n 56\n#SBATCH --time=5-00:00:00\n\nsource ~/.bashrc\nconda activate myenv\n\nexport OMP_NUM_THREADS=1\n\n'
        'cd %s\nmpirun --oversubscribe --bind-to none -np 56 lmp_mpi -in input_%s.liggghts\n') % (CS, CS, WR, CS)
MP = 'mpirun --oversubscribe --bind-to none -np 56 lmp_mpi -in input_%s.liggghts\n' % CS


def sub(old, new):
    assert BASE.count(old) == 1, old
    return BASE.replace(old, new)


V = [
    ('base (real D2 form)', BASE),
    ('export PATH=/evil/bin (no $)', sub('export OMP_NUM_THREADS=1\n', 'export PATH=/evil/bin\n')),
    ('export LD_PRELOAD=/x/evil.so', sub('export OMP_NUM_THREADS=1\n', 'export LD_PRELOAD=/x/evil.so\n')),
    ('conda activate x; mpirun other', sub('conda activate myenv\n', 'conda activate myenv; mpirun -np 1 lmp_mpi -in other.liggghts\n')),
    ('conda activate ..', sub('conda activate myenv\n', 'conda activate ..\n')),
    ('conda activate .', sub('conda activate myenv\n', 'conda activate .\n')),
    ('source /tmp/evil.sh', sub('source ~/.bashrc\n', 'source /tmp/evil.sh\n')),
    ('. ~/.bashrc (dot form)', sub('source ~/.bashrc\n', '. ~/.bashrc\n')),
    ('module load liggghts', sub('conda activate myenv\n', 'module load liggghts\n')),
    ('no trailing newline', BASE[:-1]),
    ('empty runner', ''),
    ('mpirun line + trailing space', sub(MP, MP[:-1] + ' \n')),
    ('mpirun line + tab sep', sub(MP, MP.replace(' -in ', '\t-in '))),
    ('NBSP in mpirun', sub(MP, MP.replace(' -in ', ' -in '))),
    ('vertical tab line', sub('\nsource', '\n\x0b\nsource')),
    ('form feed line', sub('\nsource', '\n\x0c\nsource')),
    ('U+2028 inside mpirun line', sub(MP, MP[:-1] + ' mpirun -np 1 lmp_mpi -in other.liggghts\n')),
    ('NEL (U+0085) inside mpirun line', sub(MP, MP[:-1] + '\u0085x\n')),
    ('backslash-continued blank line', sub('\nsource', '\n \\\nsource')),
    ('#SBATCH --time with trailing space', sub('#SBATCH --time=5-00:00:00\n', '#SBATCH --time=5-00:00:00 \n')),
    ('#SBATCH --qos=a,--exclusive', sub('#SBATCH --qos=cpu-60\n', '#SBATCH --qos=cpu-60,--exclusive\n')),
    ('#SBATCH --partition=cpu:gpu', sub('#SBATCH --partition=cpu\n', '#SBATCH --partition=cpu:gpu\n')),
    ('#PBS -l nodes=2 (comment-like)', sub('#SBATCH --time=5-00:00:00\n', '#SBATCH --time=5-00:00:00\n#PBS -l nodes=2\n')),
    ('#SBATCH -n 56 on CRLF only last', BASE + '\r'),
    ('cd via symlink alias to WR', None),
    ('shebang #!/bin/bash -e', sub('#!/bin/bash\n', '#!/bin/bash -e\n')),
    ('BOM before shebang', '﻿' + BASE),
    ('exec mpirun', sub(MP, 'exec ' + MP)),
    ('time mpirun', sub(MP, 'time ' + MP)),
    ('srun lmp_mpi', sub(MP, 'srun lmp_mpi -in input_%s.liggghts\n' % CS)),
]

alias = os.path.join(tmp, 'alias')
os.symlink(root, alias)
for i, (name, text) in enumerate(V):
    if text is None:
        text = sub('cd %s\n' % WR, 'cd %s/kg50_d2_b50\n' % alias)
    rn = os.path.join(tmp, 'helper_%02d.sh' % i)
    with open(rn, 'w', encoding='utf-8', newline='') as f:
        f.write(text)
    for p in (OM, OT):
        if os.path.exists(p):
            os.remove(p)
    p = subprocess.run(['python3', '-I', '-', rn, C, SFX, NP, W, WR, D, TD, OM, OT, CK], input=code.encode(),
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = p.stdout.decode('utf-8', 'replace').strip()
    rendered = open(OM).read() if os.path.exists(OM) else None
    extra = ''
    if rendered is not None:
        env_lines = [l for l in rendered.splitlines() if l and not l.startswith('#') and not l.startswith('cd ') and not l.startswith('echo ') and not l.startswith('mpirun ') and not l.startswith('command mpirun ') and not l.startswith('ds=') and not l.startswith('[ "$ds"')]
        extra = ' | rendered env lines: %r' % env_lines
    print('%-38s rc=%d  %s%s' % (name, p.returncode, out[:230].replace('\n', ' '), extra))
subprocess.run(['rm', '-rf', tmp])
