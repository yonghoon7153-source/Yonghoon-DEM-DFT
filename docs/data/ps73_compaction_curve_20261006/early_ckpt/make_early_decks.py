#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ps73 앞 구간 (0–400 ms) 원자 최대 높이 — ibb 에서 덱 · 러너 · 훑기 스크립트를 만든다 (1저자 10-08 밤 · 설명 = ../README.md §7).
원 런 폴더는 읽기만 · 새 폴더 ~/ps73_early_20261008 에만 쓴다 (있으면 거부).  덱 줄은 원 덱에서 그대로 잘라 쓴다.
  in.replay_0_1000 = 원 덱 처음 → unfix ins_mix + 정착 블록 (shell · restart 뺌) + 원자 덤프 1 · 1000 step + run 1000 (원 런과 같은 2 코어)
  in.ckpt_<태그>   = 원 덱 머리 + read_restart + 이웃 · 재료 · 접촉 · 벽 · 템플릿 + 원자 덤프 + run 0 (움직이지 않음)
  run_early.sh    = sbatch 2 코어 · 끝에 scan_early.py → ~/ps73_early_atomtop_20261008.csv
    python3 -I make_early_decks.py   ·   python3 -I make_early_decks.py --deck <원 덱> --print (시험)
"""
import os
import sys

HOME = os.path.expanduser('~')
RUN = os.path.join(HOME, 'dem_test/ps45/ps_7_3_r45')
DECK = os.path.join(RUN, 'input_ps_7_3_r45.liggghts')
CKD = os.path.join(RUN, 'restart_ps_7_3_r45')
W = os.path.join(HOME, 'ps73_early_20261008')
CKPTS = [('settling_%d' % s, 'restart_settling_%d.bin' % s) for s in range(50000, 400001, 50000)] + \
        [('after_settling', 'restart_after_settling.bin')]
DUMP_COLS = 'id type x y z radius'

SCAN_EARLY = r'''# ps73 앞 구간 덤프 훑기 — make_early_decks.py 가 만든 폴더에서 (run_early.sh 끝에 자동).
import glob, os, re, csv
W = os.path.expanduser('~/ps73_early_20261008')
OUT = os.path.expanduser('~/ps73_early_atomtop_20261008.csv')
def thermo(log):
    out, on = {}, False
    for ln in open(log, errors='replace'):
        t = ln.split()
        if t[:2] == ['Step', 'Atoms']:
            on = True; continue
        if on and len(t) >= 3 and t[0].isdigit() and t[1].isdigit():
            out.setdefault(int(t[0]), (int(t[1]), t[2]))
        elif on:
            on = False
    return out
ke, ins = {}, ''
for log in sorted(glob.glob(os.path.join(W, 'log.*'))):
    for s, v in thermo(log).items():
        ke.setdefault(s, (os.path.basename(log),) + v)
    for ln in open(log, errors='replace'):
        if 'inserted' in ln and 'particle templates' in ln and 'a total' not in ln:
            ins = ln.strip()
pat = re.compile(r'atom_(\d+)\.liggghts$')
rows = []
for p in sorted(glob.glob(os.path.join(W, 'dump', 'atom_*.liggghts')), key=lambda p: int(pat.search(p).group(1))):
    step = int(pat.search(p).group(1))
    with open(p) as f:
        head = [f.readline() for _ in range(9)]
        ts, n = int(head[1]), int(head[3])
        cols = head[8].split()[2:]
        iz, ir, ii, it = cols.index('z'), cols.index('radius'), cols.index('id'), cols.index('type')
        tops, zc, best, bad = [], -1e9, None, 0
        for line in f:
            t = line.split()
            if len(t) != len(cols):
                bad += 1; continue
            z = float(t[iz]); r = float(t[ir]); h = z + r
            tops.append(h)
            if z > zc: zc = z
            if best is None or h > best[0]: best = (h, t[ii], t[it], r)
    tops.sort()
    k = ke.get(step, ('', '', ''))
    rows.append([step, ts, n, len(tops), bad, '%.9g' % zc, '%.9g' % best[0], best[1], best[2], '%.9g' % best[3],
                 '%.9g' % tops[int(0.999 * (len(tops) - 1))], k[0], k[1], k[2]])
with open(OUT, 'w', newline='') as fo:
    w = csv.writer(fo, lineterminator='\n')
    w.writerow(['step', 'dump_timestep', 'n_header', 'n_rows', 'n_bad_lines', 'zc_max_deck_m', 'ztop_max_deck_m', 'ztop_id',
                'ztop_type', 'ztop_radius_deck_m', 'ztop_p999_deck_m', 'log', 'log_atoms', 'log_ke'])
    w.writerows(rows)
    w.writerow(['#insertion', ins])
for r in rows:
    print(r[0], 'n', r[2], '윗면 µm %.3f' % (float(r[6]) * 1000), '· 로그', r[11], r[12], r[13])
print('투입:', ins)
print('→', OUT)
'''


def one(lines, pred, what, start=0):
    hit = [i for i in range(start, len(lines)) if pred(lines[i].split('#', 1)[0].strip())]
    if len(hit) != 1:
        raise SystemExit('⛔ 원 덱에서 %s 줄이 %d 개 (1 개여야)' % (what, len(hit)))
    return hit[0]


def build(deck_text):
    """원 덱 글 → {파일 이름: 덱 글}.  줄은 원 덱에서 그대로 잘라 쓴다 (값을 다시 적지 않는다)."""
    L = deck_text.splitlines()
    i_box = one(L, lambda s: s.startswith('region reg_box block'), 'region reg_box block')
    i_cb = one(L, lambda s: s.startswith('create_box'), 'create_box')
    i_mix = one(L, lambda s: s.startswith('region reg_mix block'), 'region reg_mix block')   # `fix ins_mix … region reg_mix &` 의 이음 줄과 가른다
    i_unfix = one(L, lambda s: s == 'unfix ins_mix', 'unfix ins_mix')
    runs = [i for i in range(i_unfix + 1, len(L)) if L[i].split('#', 1)[0].strip().startswith('run ')]
    if not runs:
        raise SystemExit('⛔ 원 덱에 정착 run 줄이 없다')
    i_run = runs[0]
    if not (i_box < i_cb < i_mix < i_unfix < i_run) or L[i_run].split()[1] != '200000':
        raise SystemExit('⛔ 원 덱 순서가 예상과 다르다 (reg_box < create_box < reg_mix < unfix < run 200000)')
    settle = [l for l in L[i_unfix + 1:i_run] if not l.split('#', 1)[0].strip().startswith(('shell', 'restart'))]
    out = {'in.replay_0_1000.liggghts': '\n'.join(
        ['# ps73 투입 재현 — 원 덱 처음 → unfix ins_mix 그대로 · 정착 블록 (shell · restart 뺌) · 원자 덤프 1 · 1000 step · run 1000 (원 런 2 코어)']
        + L[:i_unfix + 1] + settle
        + ['dump dE all custom 1000 dump/atom_*.liggghts ' + DUMP_COLS, 'dump_modify dE first yes', 'run 1000',
           'print "EARLY_REPLAY_DONE"', ''])}
    head, mid = L[:i_box], L[i_cb + 1:i_mix]
    for tag, ck in CKPTS:
        out['in.ckpt_%s.liggghts' % tag] = '\n'.join(
            ['# ps73 체크포인트 %s — 원 덱 머리 + read_restart + 이웃 · 재료 · 접촉 · 벽 · 템플릿 (원 덱 그대로) · run 0 (움직이지 않음) · 원자 덤프' % ck]
            + head + ['read_restart    ' + os.path.join(CKD, ck)] + mid
            + ['thermo_style    custom step atoms ke', 'thermo          1',
               'dump dC all custom 1 dump/atom_*.liggghts ' + DUMP_COLS, 'dump_modify dC first yes', 'run 0',
               'print "EARLY_CKPT_DONE"', ''])
    return out


RUNNER = r'''#!/bin/bash
#SBATCH --job-name=ps73_early
#SBATCH --output=early_%j.out
#SBATCH --qos=cpu-60
#SBATCH --partition=cpu
#SBATCH -n 2
#SBATCH --time=02:00:00
source ~/.bashrc
conda activate myenv
cd ~/ps73_early_20261008
mpirun --oversubscribe -np 2 lmp_mpi -in in.replay_0_1000.liggghts -log log.replay
for T in __TAGS__; do
  mpirun --oversubscribe -np 2 lmp_mpi -in in.ckpt_$T.liggghts -log log.ckpt_$T
done
python3 -I scan_early.py
'''


def main():
    args = sys.argv[1:]
    deck = args[args.index('--deck') + 1] if '--deck' in args else DECK
    files = build(open(deck, encoding='utf-8', errors='replace').read())
    if '--print' in args:
        for k, v in files.items():
            print('=====', k)
            print(v)
        return
    missing = [ck for _, ck in CKPTS if not os.path.isfile(os.path.join(CKD, ck))]
    if missing:
        raise SystemExit('⛔ 체크포인트 없음: %s' % missing)
    if os.path.exists(W):
        raise SystemExit('⛔ %s 이 이미 있다 — 덮어쓰지 않는다 (지우거나 이름을 바꾼 뒤 다시)' % W)
    os.makedirs(os.path.join(W, 'dump'))
    for k, v in files.items():
        with open(os.path.join(W, k), 'w') as f:
            f.write(v)
    with open(os.path.join(W, 'run_early.sh'), 'w') as f:
        f.write(RUNNER.replace('__TAGS__', ' '.join(t for t, _ in CKPTS)))
    with open(os.path.join(W, 'scan_early.py'), 'w') as f:
        f.write(SCAN_EARLY)
    print('덱 %d · run_early.sh · scan_early.py → %s' % (len(files), W))
    print('다음: cd %s && sbatch run_early.sh' % W)


if __name__ == '__main__':
    main()
