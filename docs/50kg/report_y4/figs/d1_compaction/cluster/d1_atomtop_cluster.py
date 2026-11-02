#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""D1 (kg50_d1_b50) 원자 기준 두께 — D1 런 기계에서 돌리는 준비 · 훑기 (1저자 11-02 밤 *"첫번째부터 예전처럼 particle packing도 넣어야지"*).

방법 = ps73 (`docs/data/ps73_compaction_curve_20261006/README.md` §7 · `early_ckpt/make_early_decks.py` · `atom_top_scan.py`):
  ① 삽입 재현 `in.replay_0_20000` = 삽입 전용 덱 처음 → `unfix ins_mix` 그대로 + 정착 블록 (shell · restart 줄 뺌) + 원자 덤프 (step 1 ·
     1,000 마다 → 20,000) + run 20000 = 삽입 런 전체 (0 → 20 ms · 1저자 11-02 밤 *"삽입부터"*) · NP 1 (원 삽입 런과 같은 코어 수 —
     KE 가 원 로그와 1,000 step 마다 같아야 같은 궤적) · 원 삽입 화면 실측 4,584 s ≈ 76 분
  ② 체크포인트 `in.ckpt_<step>` = 본 덱 머리 + read_restart (런 폴더 원본 · 읽기만) + 이웃 · 재료 · 접촉 · 벽 · 템플릿 (덱 줄 그대로) +
     원자 덤프 + run 0 (움직이지 않음 — setup KE · 원자 수 = 원 로그)
  ③ 훑기 = ①② 덤프 + 원 런 atom 덤프 (450,000 … 2,750,000 · atom_end_2785002 · 읽기만) → 모든 원자의 max(z + r) (µm) · 검사 열 →
     `kg50_d1_atomtop.csv` 하나 (앞 네 열 = step · time_ms · ztop_um · source)
런 폴더는 읽기만 (덱 · 로그 sha256 대조 — 리포 기록과 다르면 아무것도 만들지 않는다) · 새 work 폴더에만 쓴다 (있으면 거부).

    python3 -I d1_atomtop_cluster.py prepare [--run DIR] [--work DIR] [--lmp BIN]
    cd <work> && setsid nohup bash run_atomtop.sh > run_atomtop.log 2>&1 < /dev/null &     # 끝 줄 = ATOMTOP_DONE <csv>
    python3 -I d1_atomtop_cluster.py scan [--run DIR] [--work DIR]                          # run_atomtop.sh 가 끝에 부른다
    python3 -I d1_atomtop_cluster.py --selftest
"""
import csv
import hashlib
import os
import sys
import time

RUN = os.path.expanduser('~/simulation/kg50_d1_b50')        # 리포 기록: docs/data/kg50_decks_20261027_v3_b50/README.md §3
WORK = os.path.expanduser('~/kg50_d1_atomtop_20261102')
LMP = os.path.expanduser('~/LIGGGHTS-PUBLIC/src/lmp_auto')   # 같은 README §3 의 삽입 런 명령
CASE = 'kg50_d1_b50'
#: 런 폴더 파일 sha256 (리포 · 끝 묶음 기록) — 다르면 거부
SHA = {'input_kg50_d1_b50.liggghts': '514afdb705613dab876c9c0ff5c1f2fef3fad3e029d71778875c08b89edfde91',
       'input_kg50_d1_b50_insert.liggghts': 'e5218b4dbf606215eea88212ac4796bdd405d47a1061d1184e6aff9ca0aacd5e',
       'log.liggghts': '6a90f706da68e3d5041ff063d0ffd4f61e9d89a5823f29e0755a23ed679bc1b5',
       'log_kg50_d1_b50_ins.out': 'a83ee39e902e43abe9fca663d26e15d397992f0433980fa3d0a14868177278da'}
REPLAY_STEPS = [1] + list(range(1000, 20001, 1000))     # 삽입 런 전체 (원 삽입 덱 `run 20000` 과 같은 길이) · 1,000 step 마다 덤프
REPLAY_RUN = 20000
CKPTS = [(20001, 'restart_settling_20001.bin'), (50000, 'restart_settling_50000.bin'), (100000, 'restart_settling_100000.bin'),
         (150000, 'restart_settling_150000.bin'), (200000, 'restart_settling_200000.bin'), (200001, 'restart_after_settling.bin'),
         (250000, 'restart_settling_250000.bin'), (300000, 'restart_settling_300000.bin'), (350000, 'restart_settling_350000.bin'),
         (400000, 'restart_settling_400000.bin')]
DUMP_STEPS = list(range(450000, 2750001, 50000)) + [2785002]
END_STEP = 2785002
MS_PER_STEP = 1e-3            # dt 1e-6 s (덱 `variable dt equal 1.0e-6`)
UM = 1000.0                   # 덱 m → µm (Scale r×1000)
DUMP_COLS = 'id type x y z radius'
HEAD = ['step', 'time_ms', 'ztop_um', 'source', 'dump_file', 'dump_timestep', 'n_header', 'n_rows', 'n_bad_lines', 'zc_max_um',
        'ztop_id', 'ztop_type', 'ztop_radius_um', 'ztop_p999_um', 'bytes', 'mtime', 'run_log', 'run_log_atoms', 'run_log_ke',
        'orig_log', 'orig_log_atoms', 'orig_log_ke']


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def one(lines, pred, what, start=0):
    hit = [i for i in range(start, len(lines)) if pred(lines[i].split('#', 1)[0].strip())]
    if len(hit) != 1:
        raise ValueError('덱에서 %s 줄이 %d 개 (1 개여야)' % (what, len(hit)))
    return hit[0]


def build_decks(main_deck, insert_deck, run_dir):
    """덱 글 → {파일 이름: 덱 글} (ps73 make_early_decks.build 와 같은 자르기 · 줄은 덱에서 그대로)."""
    M, I = main_deck.splitlines(), insert_deck.splitlines()
    out = {}
    i_unfix = one(I, lambda s: s == 'unfix ins_mix', 'unfix ins_mix (삽입 덱)')
    runs = [i for i in range(i_unfix + 1, len(I)) if I[i].split('#', 1)[0].strip().startswith('run ')]
    if not runs or I[runs[0]].split()[1] != '20000':
        raise ValueError('삽입 덱의 정착 run 이 run 20000 이 아니다')
    settle = [ln for ln in I[i_unfix + 1:runs[0]] if not ln.split('#', 1)[0].strip().startswith(('shell', 'restart'))]
    out['in.replay_0_%d.liggghts' % REPLAY_RUN] = '\n'.join(
        ['# D1 삽입 재현 — 삽입 전용 덱 처음 → unfix ins_mix 그대로 · 정착 블록 (shell · restart 뺌) · 원자 덤프 step 1 · 1000 마다 · '
         'run %d = 삽입 런 전체 (NP 1 = 원 삽입 런)' % REPLAY_RUN]
        + I[:i_unfix + 1] + settle
        + ['dump dE all custom 1000 dump/atom_*.liggghts ' + DUMP_COLS, 'dump_modify dE first yes', 'run %d' % REPLAY_RUN,
           'print "EARLY_REPLAY_DONE"', ''])
    i_box = one(M, lambda s: s.startswith('region reg_box block'), 'region reg_box block')
    i_cb = one(M, lambda s: s.startswith('create_box'), 'create_box')
    i_mix = one(M, lambda s: s.startswith('region reg_mix block'), 'region reg_mix block')
    if not (i_box < i_cb < i_mix):
        raise ValueError('본 덱 순서가 예상과 다르다 (reg_box < create_box < reg_mix)')
    head, mid = M[:i_box], M[i_cb + 1:i_mix]
    for step, ck in CKPTS:
        out['in.ckpt_%d.liggghts' % step] = '\n'.join(
            ['# D1 체크포인트 %s — 본 덱 머리 + read_restart (런 폴더 · 읽기만) + 이웃 · 재료 · 접촉 · 벽 · 템플릿 (덱 그대로) · run 0 · 원자 덤프' % ck]
            + head + ['read_restart    ' + os.path.join(run_dir, 'restart_' + CASE, ck)] + mid
            + ['thermo_style    custom step atoms ke', 'thermo          1',
               'dump dC all custom 1 dump/atom_*.liggghts ' + DUMP_COLS, 'dump_modify dC first yes', 'run 0',
               'print "EARLY_CKPT_DONE"', ''])
    return out


RUNNER = r'''#!/bin/bash
# D1 원자 기준 두께 — 체크포인트 run 0 (NP 1 · 몇 분 · 먼저 = 덱 문제면 일찍 멈춘다) → 삽입 재현 (NP 1 · ≈ 76 분) → 훑기.
# 런 폴더는 읽기만 · 이 폴더에만 쓴다.
set -u
cd "$(dirname "$0")"
LMP="__LMP__"
for S in __STEPS__; do
  echo "ckpt $S $(date +%T)"
  mpirun --oversubscribe --bind-to none -np 1 "$LMP" -in in.ckpt_$S.liggghts -log log.ckpt_$S > screen.ckpt_$S 2>&1 || { echo "ATOMTOP_FAIL ckpt $S"; exit 1; }
  grep -q EARLY_CKPT_DONE log.ckpt_$S || { echo "ATOMTOP_FAIL ckpt $S (끝 표지 없음)"; exit 1; }
done
echo "replay start $(date +%T)"
mpirun --oversubscribe --bind-to none -np 1 "$LMP" -in __REPLAY__ -log log.replay > screen.replay 2>&1 || { echo "ATOMTOP_FAIL replay"; exit 1; }
grep -q EARLY_REPLAY_DONE log.replay || { echo "ATOMTOP_FAIL replay (끝 표지 없음)"; exit 1; }
echo "replay done $(date +%T)"
python3 -I "__SCRIPT__" scan --run "__RUN__" --work "$(pwd)" || { echo "ATOMTOP_FAIL scan"; exit 1; }
echo "ATOMTOP_DONE $(pwd)/kg50_d1_atomtop.csv"
'''


def thermo_ke(path):
    """로그 → {step: (atoms, KE 글자)} — 머리에 KinEng 가 있는 thermo 블록만 · 같은 step 은 처음 것 (ps73 make_fig_ms.log_thermo_ke 와 같은 규칙)."""
    out, on = {}, False
    with open(path, errors='replace') as f:
        for ln in f:
            t = ln.split()
            if t[:2] == ['Step', 'Atoms']:
                on = 'KinEng' in t
                continue
            if on and len(t) >= 3 and t[0].isdigit() and t[1].isdigit():
                out.setdefault(int(t[0]), (int(t[1]), t[2]))
            elif on:
                on = False
    return out


def insertion_line(path):
    with open(path, errors='replace') as f:
        for ln in f:
            if 'inserted' in ln and 'particle templates' in ln and 'a total' not in ln:
                return ln.strip()
    return ''


def scan_dump(path):
    """덤프 하나 → 머리 TIMESTEP · 원자 수 · 줄 · 깨진 줄 · 중심 max z · 윗면 max(z + r) 와 그 입자 · 윗면 p99.9 (atom_top_scan.py 와 같은 계산)."""
    with open(path) as f:
        head = [f.readline() for _ in range(9)]
        ts, n = int(head[1]), int(head[3])
        cols = head[8].split()[2:]
        iz, ir, ii, it = cols.index('z'), cols.index('radius'), cols.index('id'), cols.index('type')
        tops, zc, best, bad = [], -1e30, None, 0
        for line in f:
            t = line.split()
            if len(t) != len(cols):
                bad += 1
                continue
            z, r = float(t[iz]), float(t[ir])
            h = z + r
            tops.append(h)
            if z > zc:
                zc = z
            if best is None or h > best[0]:
                best = (h, t[ii], t[it], r)
    tops.sort()
    p999 = tops[int(0.999 * (len(tops) - 1))] if tops else float('nan')
    st = os.stat(path)
    b = best or (float('nan'), '', '', float('nan'))
    return {'dump_timestep': ts, 'n_header': n, 'n_rows': len(tops), 'n_bad_lines': bad, 'zc_max_um': zc * UM,
            'ztop_um': b[0] * UM, 'ztop_id': b[1], 'ztop_type': b[2], 'ztop_radius_um': b[3] * UM, 'ztop_p999_um': p999 * UM,
            'bytes': st.st_size, 'mtime': time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(st.st_mtime))}


def check_inputs(run_dir):
    prob = []
    for name, want in SHA.items():
        p = os.path.join(run_dir, name)
        if not os.path.isfile(p):
            prob.append('없음 %s' % p)
        elif sha256(p) != want:
            prob.append('sha256 다름 %s' % p)
    for _, ck in CKPTS:
        if not os.path.isfile(os.path.join(run_dir, 'restart_' + CASE, ck)):
            prob.append('체크포인트 없음 restart_%s/%s' % (CASE, ck))
    for s in DUMP_STEPS:
        name = 'atom_end_%d.liggghts' % s if s == END_STEP else 'atom_%d.liggghts' % s
        if not os.path.isfile(os.path.join(run_dir, 'post_' + CASE, name)):
            prob.append('덤프 없음 post_%s/%s' % (CASE, name))
    return prob


def fmt(v):
    return '%.9g' % v if isinstance(v, float) else str(v)


def scan(run_dir, work):
    """work 의 재현 · 체크포인트 덤프 + 런 폴더 atom 덤프 → kg50_d1_atomtop.csv (+ #insertion · #sha256 줄)."""
    ins_ref = os.path.join(run_dir, 'log_kg50_d1_b50_ins.out')
    main_ref = os.path.join(run_dir, 'log.liggghts')
    k_ins, k_main = thermo_ke(ins_ref), thermo_ke(main_ref)
    rows = []
    rep = thermo_ke(os.path.join(work, 'log.replay'))
    for s in REPLAY_STEPS:
        d = scan_dump(os.path.join(work, 'dump', 'atom_%d.liggghts' % s))
        rows.append(dict(d, step=s, source='replay', dump_file='work:dump/atom_%d.liggghts' % s, run_log='log.replay',
                         run_log_atoms=rep.get(s, ('', ''))[0], run_log_ke=rep.get(s, ('', ''))[1],
                         orig_log='log_kg50_d1_b50_ins.out', orig_log_atoms=k_ins.get(s, ('', ''))[0], orig_log_ke=k_ins.get(s, ('', ''))[1]))
    for s, _ in CKPTS:
        lg = thermo_ke(os.path.join(work, 'log.ckpt_%d' % s))
        d = scan_dump(os.path.join(work, 'dump', 'atom_%d.liggghts' % s))
        rows.append(dict(d, step=s, source='checkpoint', dump_file='work:dump/atom_%d.liggghts' % s, run_log='log.ckpt_%d' % s,
                         run_log_atoms=lg.get(s, ('', ''))[0], run_log_ke=lg.get(s, ('', ''))[1],
                         orig_log='log.liggghts', orig_log_atoms=k_main.get(s, ('', ''))[0], orig_log_ke=k_main.get(s, ('', ''))[1]))
    for s in DUMP_STEPS:
        name = 'atom_end_%d.liggghts' % s if s == END_STEP else 'atom_%d.liggghts' % s
        d = scan_dump(os.path.join(run_dir, 'post_' + CASE, name))
        rows.append(dict(d, step=s, source='atom dump', dump_file='run:post_%s/%s' % (CASE, name), run_log='', run_log_atoms='',
                         run_log_ke='', orig_log='log.liggghts', orig_log_atoms=k_main.get(s, ('', ''))[0],
                         orig_log_ke=k_main.get(s, ('', ''))[1]))
    out = os.path.join(work, 'kg50_d1_atomtop.csv')
    with open(out, 'w', newline='') as fo:
        w = csv.writer(fo, lineterminator='\n')
        w.writerow(HEAD)
        for r in rows:
            r['time_ms'] = '%.3f' % (r['step'] * MS_PER_STEP)
            w.writerow([fmt(r[k]) for k in HEAD])
        w.writerow(['#insertion', insertion_line(os.path.join(work, 'log.replay'))])
        w.writerow(['#insertion_orig', insertion_line(ins_ref)])
        for name in sorted(SHA):
            w.writerow(['#sha256', name, sha256(os.path.join(run_dir, name))])
        w.writerow(['#script_sha256', sha256(os.path.abspath(__file__))])   # 이 CSV 를 만든 스크립트 = 리포 파일인지 (생성기가 대조)
    for r in rows:
        print(r['step'], r['source'], 'ztop %.3f µm' % r['ztop_um'], 'n', r['n_header'], 'KE', r['run_log_ke'], '/', r['orig_log_ke'])
    # 바로 보는 대조 (판정은 리포 생성기 check_atomtop 이 다시 한다) — 재현 · 체크포인트 KE 상대 1e-6 · 원자 수 · 덤프 머리 = 줄
    early = [r for r in rows if r['source'] != 'atom dump']
    bad = [r['step'] for r in early if not same_ke(r['run_log_ke'], r['orig_log_ke']) or r['run_log_atoms'] != r['n_header']
           or r['orig_log_atoms'] != r['n_header']]
    bad += [r['step'] for r in rows if r['n_header'] != r['n_rows'] or r['n_bad_lines'] or r['dump_timestep'] != r['step']]
    print('KE_CHECK %d/%d 같음' % (len(early) - len(set(bad) & {r['step'] for r in early}), len(early))
          + ('' if not bad else ' · ⚠ 다른 step %s (CSV 는 그대로 썼다 — 리포 생성기가 거부한다)' % sorted(set(bad))))
    print('→', out)
    return out


def same_ke(a, b, rtol=1e-6):
    try:
        fa, fb = float(a), float(b)
    except (TypeError, ValueError):
        return False
    return abs(fa - fb) <= rtol * abs(fb)


def prepare(run_dir, work, lmp):
    prob = check_inputs(run_dir)
    if prob:
        raise SystemExit('⛔ 런 폴더 확인 실패 — 아무것도 만들지 않았다:\n  ' + '\n  '.join(prob))
    if os.path.exists(work):
        raise SystemExit('⛔ %s 이 이미 있다 — 덮어쓰지 않는다 (이름을 바꾸거나 지운 뒤 다시)' % work)
    with open(os.path.join(run_dir, 'input_kg50_d1_b50.liggghts'), errors='replace') as f:
        main_deck = f.read()
    with open(os.path.join(run_dir, 'input_kg50_d1_b50_insert.liggghts'), errors='replace') as f:
        insert_deck = f.read()
    try:
        decks = build_decks(main_deck, insert_deck, run_dir)
    except ValueError as e:
        raise SystemExit('⛔ ' + str(e))
    os.makedirs(os.path.join(work, 'dump'))
    for k, v in decks.items():
        with open(os.path.join(work, k), 'w') as f:
            f.write(v)
    with open(os.path.join(work, 'run_atomtop.sh'), 'w') as f:
        f.write(RUNNER.replace('__LMP__', lmp).replace('__STEPS__', ' '.join(str(s) for s, _ in CKPTS))
                .replace('__REPLAY__', 'in.replay_0_%d.liggghts' % REPLAY_RUN)
                .replace('__SCRIPT__', os.path.abspath(__file__)).replace('__RUN__', run_dir))
    print('덱 %d · run_atomtop.sh → %s (런 폴더 sha256 4 개 · 체크포인트 %d · 덤프 %d 확인)' % (len(decks), work, len(CKPTS), len(DUMP_STEPS)))
    print('다음: cd %s && setsid nohup bash run_atomtop.sh > run_atomtop.log 2>&1 < /dev/null &' % work)


def selftest():
    import tempfile
    ok = fail = 0

    def chk(name, cond):
        nonlocal ok, fail
        ok, fail = ok + bool(cond), fail + (not cond)
        print(('PASS ' if cond else 'FAIL ') + name)

    with tempfile.TemporaryDirectory() as tmp:
        p = os.path.join(tmp, 'atom_5.liggghts')
        with open(p, 'w') as f:
            f.write('ITEM: TIMESTEP\n5\nITEM: NUMBER OF ATOMS\n3\nITEM: BOX BOUNDS pp pp ff\n0 0.05\n0 0.05\n-0.01 1\n'
                    'ITEM: ATOMS id type x y z radius\n1 1 0 0 0.100 0.003\n2 3 0 0 0.1045 0.0005\n3 3 0 0 0.050 0.0005\n')
        d = scan_dump(p)
        chk('S1 덤프 읽기: 윗면 = max(z + r) · 그 입자 · 중심 max · 줄 수',
            abs(d['ztop_um'] - 105.0) < 1e-9 and d['ztop_id'] in ('2', '1') and abs(d['zc_max_um'] - 104.5) < 1e-9
            and d['n_rows'] == 3 and d['n_header'] == 3 and d['dump_timestep'] == 5 and d['n_bad_lines'] == 0)
        with open(p, 'a') as f:
            f.write('4 3 0 0\n')
        chk('S2 깨진 줄 = 셈', scan_dump(p)['n_bad_lines'] == 1)
        lg = os.path.join(tmp, 'log')
        with open(lg, 'w') as f:
            f.write('    Step    Atoms         KinEng            CPU \n       1   168457     0.11946798      17.7 \nLoop time\n'
                    '    Step    Atoms           zmax \n  200001   168457     0.13944572 \n'
                    'INFO: Particle insertion ins_mix: inserted 168457 particle templates (mass 9.557438e-01) at step 1\n')
        k = thermo_ke(lg)
        chk('S3 KE 읽기: KinEng 블록만 (zmax 블록 제외)', k == {1: (168457, '0.11946798')})
        chk('S4 삽입 줄', insertion_line(lg).endswith('at step 1'))
    main = ('atom_style granular\nunits si\nregion reg_box block 0 0.05 0 0.05 -0.01 1.0 units box\ncreate_box 3 reg_box\n'
            'neighbor 0.002 bin\nfix pts1 all particletemplate/sphere 1 atom_type 1 density constant 4850 radius constant 0.003\n'
            'region reg_mix block 0.0 0.05 0.0 0.05 0.005 0.3227 units box\n')
    ins = (main + 'fix ins_mix all insert/pack seed 1 &\n    region reg_mix\nrun 1\nunfix ins_mix\nshell mkdir post\nthermo 1000\n'
           'fix gravi all gravity 98.1 vector 0.0 0.0 -1.0\nrestart 50000 r/restart_settling_*.bin\nrun 20000\n')
    dk = build_decks(main, ins, '/RUN')
    rp = dk['in.replay_0_%d.liggghts' % REPLAY_RUN]
    lines = [ln.strip() for ln in rp.splitlines()]
    chk('S5 재현 덱: 삽입까지 그대로 · shell · restart 뺌 · 덤프 first yes 뒤 run 20000 하나 (원 정착 run 은 뺌) · 끝 표지',
        'unfix ins_mix' in lines and not any(ln.startswith(('shell', 'restart', 'write_restart')) for ln in lines)
        and lines.count('run %d' % REPLAY_RUN) == 1 and lines.index('dump_modify dE first yes') < lines.index('run %d' % REPLAY_RUN)
        and rp.rstrip().endswith('print "EARLY_REPLAY_DONE"') and REPLAY_STEPS[:3] == [1, 1000, 2000] and REPLAY_STEPS[-1] == 20000)
    ck = dk['in.ckpt_20001.liggghts']
    chk('S6 체크포인트 덱: 머리 + read_restart (런 폴더) + 재료 · 템플릿 · reg_box · create_box · reg_mix 없음 · run 0',
        'read_restart    /RUN/restart_kg50_d1_b50/restart_settling_20001.bin' in ck and 'fix pts1' in ck and 'create_box' not in ck
        and 'region reg_mix' not in ck and 'run 0' in ck and len([x for x in dk if x.startswith('in.ckpt_')]) == len(CKPTS))
    try:
        build_decks(main, ins.replace('run 20000', 'run 1000'), '/RUN')
        chk('S7 삽입 덱 정착 run ≠ 20000 = 거부', False)
    except ValueError:
        chk('S7 삽입 덱 정착 run ≠ 20000 = 거부', True)
    print('d1_atomtop_cluster selftest: %d PASS · %d FAIL' % (ok, fail))
    return fail == 0


def main():
    a = sys.argv[1:]
    if '--selftest' in a:
        sys.exit(0 if selftest() else 1)

    def opt(k, d):
        return os.path.abspath(os.path.expanduser(a[a.index(k) + 1])) if k in a else d
    run_dir, work = opt('--run', RUN), opt('--work', WORK)
    if not a or a[0] not in ('prepare', 'scan'):
        raise SystemExit(__doc__)
    if a[0] == 'prepare':
        prepare(run_dir, work, opt('--lmp', LMP))
    else:
        scan(run_dir, work)


if __name__ == '__main__':
    main()
