#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""`scripts/compaction_curve.py` 반례 시험 — 합성 LIGGGHTS 로그 · 판 메시 (재시작 r1 · r2 · r3 를 흉내).

    python3 scripts/test_compaction_curve.py

왜 (2026-10-06 밤 · 이종기술 2-1 장 7:3 압축 곡선 — x = step):
  ps_7_3_r45 는 한 번에 돌지 않았다 (09-21 진행 기록) — r1 이 체크포인트 1,450,000 뒤에 끊겼고, r2 는 재시작하며 판을
  7.4–8.2 µm 다시 들어 올린 궤적 (버림), r3 은 판을 그 체크포인트 높이로 되돌려 끝까지 갔다.  로그를 그냥 이어 붙이면
  r2 의 압력 0 구간이나 run 경계 설정 줄 (같은 step 앞 줄과 압력이 다르게 찍힌다 — CLAUDE.md 재개 체크리스트 ⑤) 이
  곡선에 섞인다.  아래 반례가 전부 **거부** 되거나 **버려져야** 한다.

합성 모형 (덱 단위 — 진짜 런의 1/1000 축소판):
  정착 1 → 2,001 · zmax 2,001 → 2,002 · 안정화 2,002 → 4,002 (판 고정 z0) · 압축 run 500 step 반복 (판 1e-6 /step 하강) ·
  압력 p(s) = 0.05·((s − 6,000)/1,000)² (접촉 뒤) · 목표 0.3 · 체크포인트 7,500 · r1 은 7,800 에서 잘림 ·
  r3 은 7,500 에서 다시 시작 → 8,500 에서 목표 통과 → 이완 1,000 step.
"""
from __future__ import annotations

import json
import math
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

Z0 = 0.1383            # 판 놓은 높이 (덱 m)
V = 1e-6               # 판 하강 (덱 m / step)
S2, S3 = 2002, 4002    # 안정화 · 압축 시작
CKPT = 7500
EXIT = 8500            # 목표 통과 run 끝
END = 9500
TARGET = 0.3
LIFT = 0.0078          # r2 의 판 재부양 (덱 m)

HDR_P = ['Step', 'Atoms', 'KinEng', 'CPU', 'v_pressMPa']
HDR_4 = ['Step', 'Atoms', 'KinEng', 'CPU']


def z_of(s):
    if s <= S3:
        return Z0
    return Z0 - V * (min(s, EXIT) - S3)


def p_of(s):
    if s < S3 or s <= 6000:
        return 0.0
    if s <= EXIT:
        return 0.05 * ((s - 6000) / 1000.0) ** 2
    return p_of(EXIT) * math.exp(-(s - EXIT) / 400.0)


def fmt(v):
    return f'{v:.10g}'


def block(header, steps, val, *, setup_scale=1.08, loop=True, truncated=None):
    """thermo 블록 — 첫 줄 = 설정 줄 (압력이 앞 run 끝 줄과 다르게 찍힌다: × setup_scale)."""
    out = ['Setting up run ...', 'Memory usage per processor = 10 Mbytes', '    ' + '    '.join(header)]
    for i, s in enumerate(steps):
        vals = val(s)
        if i == 0 and 'v_pressMPa' in header:
            vals = vals[:-1] + [vals[-1] * setup_scale]
        out.append(f'{s:9d} ' + ' '.join(fmt(x) for x in [100] + vals))
    if truncated is not None:
        out.append(truncated)
    if loop:
        out.append(f'Loop time of 1.234 on 2 procs for {steps[-1] - steps[0]} steps with 100 atoms')
    return out


def pvals(s):
    return [1e-6, 12.5, p_of(s)]


def kvals(s):
    return [1e-6, 12.5]


def thermo_steps(a, b, every=100):
    st = [a] + [s for s in range((a // every + 1) * every, b, every)] + [b]
    return sorted(set(st))


def judge(s, target=TARGET, value=None):
    v = p_of(s) if value is None else value
    return [f'print "Current Pressure: {v:.15g} MPa (Target: {target})"', f'Current Pressure: {v:.15g} MPa (Target: {target})']


def r1_lines(*, end_at=7800, header_p=HDR_P):
    L = ['LIGGGHTS (Version LIGGGHTS-PUBLIC 3.8.0, compiled 2026-08-25)', 'fix zwall_bot all wall/gran model hooke/hysteresis primitive type 1 zplane 0.0',
         'print "====== INSERTING PARTICLES ====="', '====== INSERTING PARTICLES =====']
    L += block(HDR_4, [0, 1], kvals)
    L += ['print "====== PHASE 1: SETTLING ======"', '====== PHASE 1: SETTLING ======']
    L += block(HDR_4, thermo_steps(1, 2001, 1000), kvals)
    L += ['====== RESTART SAVED ======']
    L += block(['Step', 'Atoms', 'c_zmax'], [2001, 2002], lambda s: [0.1308])
    L += [f'print "====== PLATE HEIGHT: {Z0} ======"', f'====== PLATE HEIGHT: {Z0} ======']
    L += ['print "====== PHASE 2: STABILIZE ======"', '====== PHASE 2: STABILIZE ======']
    L += block(header_p, thermo_steps(S2, S3, 1000), pvals)
    L += ['print "====== PHASE 3: COMPRESSION (Speed 0.01) ======"', '====== PHASE 3: COMPRESSION (Speed 0.01) ======']
    a = S3
    while True:
        b = a + 500
        if b > end_at:      # 잘린 run — Loop time 없음 · 마지막 줄이 반쯤 쓰였다
            steps = [s for s in thermo_steps(a, b) if s <= end_at]
            L += block(header_p, steps, pvals, loop=False, truncated=f'{end_at + 100:9d} 100 1e-')
            break
        L += block(header_p, thermo_steps(a, b), pvals)
        L += judge(b)
        a = b
    return L


def restart_lines(*, plate, ckpt_name=f'restart_ps/restart_settling_{CKPT}.bin', first=CKPT, phase3_marker=True,
                  phase4_marker=True, lifted=False, end=END, judge_tamper=None):
    L = ['LIGGGHTS (Version LIGGGHTS-PUBLIC 3.8.0, compiled 2026-08-25)', f'read_restart {ckpt_name}',
         '  orthogonal box = (0 0 -0.01) to (0.05 0.05 1)', f'print "====== PLATE HEIGHT: {plate} ======"',
         f'====== PLATE HEIGHT: {plate} ======']
    if phase3_marker:
        L += ['====== PHASE 3: COMPRESSION (Speed 0.01) ======']
    pv = (lambda s: [1e-6, 12.5, 0.0]) if lifted else pvals
    a = first
    while a < EXIT if not lifted else a < 9000:
        b = a + 500
        L += block(HDR_P, thermo_steps(a, b), pv, setup_scale=0.0 if a == first else 1.08)
        jv = 0.0 if lifted else None
        if judge_tamper is not None and b == judge_tamper:
            jv = p_of(b) * 1.5
        L += judge(b, value=jv)
        a = b
    if lifted:
        return L
    if phase4_marker:
        L += ['print "====== PHASE 4: RELAXATION ======"', '====== PHASE 4: RELAXATION ======']
    L += block(HDR_P, thermo_steps(EXIT, end), pvals)
    L += ['====== Simulation Finished! ======']
    return L


def restart_r3style(*, plate, ckpt=CKPT, ckpt_name=None, lifted=False, echo=True):
    """실제 r3 · r5 덱 꼴 — read_restart → zmax `run 1` (ckpt → ckpt+1) → PLATE HEIGHT → PHASE 2 `run 0` (설정 줄만) →
    PHASE 3 루프가 ckpt+1 부터 → 이완.  (2026-10-06 ibb ps_7_3_r45 r3 로그 머리와 같은 순서)"""
    name = ckpt_name or f'restart_ps/restart_settling_{ckpt}.bin'
    L = ['LIGGGHTS (Version LIGGGHTS-PUBLIC 3.8.0, compiled 2026-03-26)']
    if echo:
        L.append(f'read_restart {name}')
    L += ['Reading restart file ...', '  160420 atoms']
    L += block(['Step', 'Atoms', 'zmax'], [ckpt, ckpt + 1], lambda s: [0.1340])
    L += ['====== SETTLING COMPLETE ======', f'====== PLATE HEIGHT: {plate} ======', '====== PHASE 2: STABILIZE ======']
    L += block(HDR_P, [ckpt + 1], pvals)                       # run 0 — 설정 줄 하나
    L += ['====== PHASE 3: COMPRESSION (Speed 0.01) ======']
    pv = (lambda s: [1e-6, 12.5, 0.0]) if lifted else pvals
    a = ckpt + 1
    while True:
        b = a + 500
        L += block(HDR_P, thermo_steps(a, b), pv, setup_scale=1.08)
        x = 0.0 if lifted else p_of(b)
        L += judge(b, value=x)[1:] if not echo else judge(b, value=x)
        a = b
        if lifted and b >= 9001:
            return L
        if not lifted and x >= TARGET:
            break
    L += ['====== PHASE 4: RELAXATION ======']
    L += block(HDR_P, thermo_steps(a, a + 1000), pvals)
    return L


def screen_only(lines):
    """SLURM 화면 출력 꼴 — 명령 되풀이 (echo) 줄이 없다: read_restart · print "…" · fix … 줄을 지운다."""
    return [ln for ln in lines if not ln.lstrip().startswith(('read_restart', 'print "', 'fix '))]


def write(path, lines):
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')


def stl(path, z, tilt=0.0):
    with open(path, 'w', encoding='utf-8') as f:
        f.write('solid LIGGGHTS_STL_EXPORT\n')
        for tri in (((0, 0), (0.05, 0.05), (0.05, 0)), ((0, 0), (0, 0.05), (0.05, 0.05))):
            f.write(' facet normal 0 0 -1\n  outer loop\n')
            for k, (x, y) in enumerate(tri):
                f.write(f'   vertex {x:.6f} {y:.6f} {z + (tilt if k == 1 else 0):.6f}\n')
            f.write('  endloop\n endfacet\n')
        f.write('endsolid LIGGGHTS_STL_EXPORT\n')


def mesh_dir(root, *, lift_at=None, tilt_at=None):
    d = os.path.join(root, 'post')
    os.makedirs(d, exist_ok=True)
    for s in range(2500, END + 1, 500):
        z = z_of(s) + (LIFT if s == lift_at else 0.0)
        stl(os.path.join(d, f'mesh_{s}.stl'), z, tilt=1e-4 if s == tilt_at else 0.0)
    return d


def case(root):
    os.makedirs(root, exist_ok=True)
    p = {k: os.path.join(root, f'{k}.out') for k in ('r1', 'r2', 'r3')}
    write(p['r1'], r1_lines())
    write(p['r2'], restart_lines(plate=f'{z_of(CKPT) + LIFT:.6f}', lifted=True))
    write(p['r3'], restart_lines(plate=f'{z_of(CKPT):.6f}'))
    return p


def run(argv):
    import compaction_curve as CC     # noqa: E402 — 시험 대상
    return CC.main(argv)


def load(out):
    with open(os.path.join(out, 'curve_summary.json'), encoding='utf-8') as f:
        return json.load(f)


def read_csv(path):
    import csv
    with open(path, encoding='utf-8') as f:
        return list(csv.DictReader(f))


def main():
    ok = bad = 0
    tmp = tempfile.mkdtemp(prefix='cc_test_')

    def check(name, cond, detail=''):
        nonlocal ok, bad
        if cond:
            ok += 1
            print(f'  ✓ {name}')
        else:
            bad += 1
            print(f'  ✗ {name}  {detail}')

    def refused(name, argv, why_part):
        # ★ 반례마다 **새** 출력 폴더 — 같은 폴더를 쓰면 둘째부터 '폴더가 비어 있지 않다' 로 거부돼 거짓 통과한다 (초판 결함)
        out = tempfile.mkdtemp(dir=tmp, prefix='out_')
        try:
            rc = run(argv + ['--out', out])
        except Exception as e:           # 시험 대상이 없거나 죽으면 실패로 센다 (반례 먼저 단계)
            check(name, False, f'예외 {type(e).__name__}: {e}')
            return
        s = load(out) if os.path.isfile(os.path.join(out, 'curve_summary.json')) else {}
        why = ' '.join(s.get('why', []))
        check(name, rc == 2 and s.get('status') == 'REFUSED' and why_part in why
              and not os.path.exists(os.path.join(out, 'pressure.csv')),
              f'rc={rc} status={s.get("status")} why={why[:160]!r}')

    try:
        root = os.path.join(tmp, 'a')
        p = case(root)
        md = mesh_dir(root)

        # ── 양성: r1 + r3 ──
        out = os.path.join(tmp, 'ok')
        try:
            rc = run(['--segment', p['r1'], '--segment', p['r3'], '--mesh-dir', md, '--out', out])
        except Exception as e:
            rc = None
            check('① 양성 r1 + r3 — 돈다', False, f'예외 {type(e).__name__}: {e}')
        if rc is not None:
            s = load(out)
            check('① 양성 r1 + r3 — OK', rc == 0 and s.get('status') == 'OK', f'rc={rc} why={s.get("why")}')
        if rc != 0:
            check('②–⑪ 양성 산출 확인 (산출 없음 — ① 실패)', False)
        else:
            pr = read_csv(os.path.join(out, 'pressure.csv'))
            st = [int(r['step']) for r in pr]
            check('② step 엄격 증가 (중복 0)', all(b > a for a, b in zip(st, st[1:])))
            seg_at = {int(r['step']): r['segment'] for r in pr}
            check('③ 잇는 자리 — 7,500 까지 r1 · 7,600 부터 r3 (r1 의 7,502 · 7,800 은 버림)',
                  seg_at.get(7500) == 'r1.out' and seg_at.get(7600) == 'r3.out'
                  and 7502 not in seg_at and seg_at.get(7800) == 'r3.out',
                  f'7500={seg_at.get(7500)} 7600={seg_at.get(7600)} 7502={seg_at.get(7502)} 7800={seg_at.get(7800)}')
            pmap = {int(r['step']): r['pressure_mpa'] for r in pr}
            # ★ 압력이 0 이 아닌 경계를 본다 — 초판은 4,502 (접촉 전 압력 0 → ×1.08 도 0) 를 봐서 가르지 못했다
            check('④ 설정 줄 버림 — run 경계 7,002 · 8,000 압력 = 앞 run 끝 줄 (×1.08 아님)',
                  p_of(7002) > 0 and abs(float(pmap[7002]) - p_of(7002) * 1000) < 1e-6
                  and abs(float(pmap[8000]) - p_of(8000) * 1000) < 1e-6,
                  f'7002={pmap.get(7002)} 기대 {p_of(7002) * 1000} · 8000={pmap.get(8000)} 기대 {p_of(8000) * 1000}')
            check('⑤ 재시작 설정 줄 (압력 0) 대신 r1 의 7,500 줄', abs(float(pmap[7500]) - p_of(7500) * 1000) < 1e-6,
                  f'7500={pmap.get(7500)} 기대 {p_of(7500) * 1000}')
            check('⑥ 단위 — 압력 MPa = 덱 × 1000', abs(float(pmap[EXIT]) - p_of(EXIT) * 1000) < 1e-6, f'{pmap.get(EXIT)}')
            ph = s.get('phase_bounds', {})
            check('⑦ 단계 경계 1 · 2,002 · 4,002 · 8,500 (표지 · 첫 출현)',
                  [ph.get(k, {}).get('step') for k in ('1', '2', '3', '4')] == [1, S2, S3, EXIT], f'{ph}')
            pl = read_csv(os.path.join(out, 'plate.csv'))
            last = pl[-1]
            check('⑧ 끝 두께 µm = 판 z × 1000', int(last['step']) == END and abs(float(last['thickness_um']) - z_of(EXIT) * 1000) < 2e-3,
                  f'{last}')
            check('⑨ 목표 통과 기록 (300 MPa · reached)', s.get('target_mpa') == 300.0 and s.get('reached') is True,
                  f'{s.get("target_mpa")} {s.get("reached")}')
            c = s.get('checks', {})
            check('⑩ 검사 C1–C6 전부 ok', all(c.get(k, {}).get('ok') for k in ('C1', 'C2', 'C3', 'C4', 'C5', 'C6')), f'{c}')
            check('⑪ 판 하강 속도 = 1e-6 /step (µm / 1,000 step = 1)', abs(s.get('plate_speed_um_per_1000step', 0) - 1.0) < 1e-3,
                  f'{s.get("plate_speed_um_per_1000step")}')

        # ── 반례 ──
        refused('⑫ r2 (판 재부양) 를 이으면 거부 — C3', ['--segment', p['r1'], '--segment', p['r2'], '--mesh-dir', md], 'C3')
        refused('⑬ r1 + r2 + r3 모두 주면 거부', ['--segment', p['r1'], '--segment', p['r2'], '--segment', p['r3'], '--mesh-dir', md], 'C')

        g = os.path.join(tmp, 'gap')
        os.makedirs(g)
        write(os.path.join(g, 'r1.out'), r1_lines(end_at=7300))
        shutil.copy(p['r3'], os.path.join(g, 'r3.out'))
        refused('⑭ 빈 구간 (r1 이 7,300 에서 끝 · r3 은 7,500 부터) 거부 — C2', ['--segment', os.path.join(g, 'r1.out'),
                                                                          '--segment', os.path.join(g, 'r3.out'), '--mesh-dir', md], 'C2')

        w = os.path.join(tmp, 'rr')
        os.makedirs(w)
        write(os.path.join(w, 'r3.out'), restart_lines(plate=f'{z_of(CKPT):.6f}', ckpt_name='restart_ps/restart_settling_7000.bin'))
        refused('⑮ read_restart 파일 step ≠ 첫 step 거부 — C2', ['--segment', p['r1'], '--segment', os.path.join(w, 'r3.out'), '--mesh-dir', md], 'C2')

        t = os.path.join(tmp, 'tamper')
        os.makedirs(t)
        write(os.path.join(t, 'r3.out'), restart_lines(plate=f'{z_of(CKPT):.6f}', judge_tamper=8000))
        refused('⑯ 판정 줄 ≠ thermo 압력 거부 — C4 (압력 열 오인 방지)', ['--segment', p['r1'], '--segment', os.path.join(t, 'r3.out'), '--mesh-dir', md], 'C4')

        h = os.path.join(tmp, 'hdr')
        os.makedirs(h)
        write(os.path.join(h, 'r1.out'), r1_lines(header_p=['Step', 'Atoms', 'KinEng', 'CPU', 'v_press']))
        refused('⑰ 압력 열 이름 모름 (v_press) 거부 — C1', ['--segment', os.path.join(h, 'r1.out'), '--segment', p['r3'], '--mesh-dir', md], 'C1')

        for tag, kw, part in (('lift3', dict(lift_at=8000), 'C5'), ('lift4', dict(lift_at=9000), 'C5'), ('tilt', dict(tilt_at=6000), 'C5')):
            r = os.path.join(tmp, tag)
            os.makedirs(r)
            refused(f'⑱ 판 메시 반례 ({tag}) 거부 — C5', ['--segment', p['r1'], '--segment', p['r3'], '--mesh-dir', mesh_dir(r, **kw)], part)

        n = os.path.join(tmp, 'nan')
        os.makedirs(n)
        lines = r1_lines()
        k = next(i for i, ln in enumerate(lines) if ln.strip().startswith('5100 '))
        lines[k] = lines[k].rsplit(' ', 1)[0] + ' -nan'
        write(os.path.join(n, 'r1.out'), lines)
        refused('⑲ 비유한 압력 거부 — C1', ['--segment', os.path.join(n, 'r1.out'), '--segment', p['r3'], '--mesh-dir', md], 'C1')

        # ── 산출 폴더가 비어 있지 않으면 거부 (옛 산출을 덮지 않는다) ──
        busy = tempfile.mkdtemp(dir=tmp, prefix='busy_')
        write(os.path.join(busy, 'keep.txt'), ['옛 산출'])
        try:
            rc = run(['--segment', p['r1'], '--segment', p['r3'], '--mesh-dir', md, '--out', busy])
            check('㉑ 비어 있지 않은 --out 거부 · 아무것도 안 씀', rc == 2 and sorted(os.listdir(busy)) == ['keep.txt'],
                  f'rc={rc} {sorted(os.listdir(busy))}')
        except Exception as e:
            check('㉑ 비어 있지 않은 --out 거부', False, f'예외 {type(e).__name__}: {e}')

        # ── 실제 ibb 로그 꼴 (2026-10-06 수신 — SLURM 화면 출력 · r3 식 재시작) ──
        def ok_case(name, segs, mdir=md, want_note=None):
            out = tempfile.mkdtemp(dir=tmp, prefix='okc_')
            try:
                rc = run(sum((['--segment', s_] for s_ in segs), []) + ['--mesh-dir', mdir, '--out', out])
                s_ = load(out)
                notes = ' '.join(d for c in s_.get('checks', {}).values() for d in c.get('detail', []))
                check(name, rc == 0 and s_.get('status') == 'OK' and (want_note is None or want_note in notes),
                      f'rc={rc} why={s_.get("why")} notes={notes[:200]!r}')
            except Exception as e:
                check(name, False, f'예외 {type(e).__name__}: {e}')

        sc = os.path.join(tmp, 'screen')
        os.makedirs(sc)
        write(os.path.join(sc, 'r1.out'), screen_only(r1_lines()))
        write(os.path.join(sc, 'r3.out'), screen_only(restart_lines(plate=f'{z_of(CKPT):.6f}')))
        ok_case('㉒ 화면 출력 꼴 (read_restart · print 되풀이 줄 없음) — 통과 · read_restart 대조 못 함 표지',
                [os.path.join(sc, 'r1.out'), os.path.join(sc, 'r3.out')], want_note='read_restart')

        r3s = os.path.join(tmp, 'r3style')
        os.makedirs(r3s)
        write(os.path.join(r3s, 'r3.out'), screen_only(restart_r3style(plate=f'{z_of(CKPT):.6f}', echo=False)))
        write(os.path.join(r3s, 'r2.out'), screen_only(restart_r3style(plate=f'{z_of(CKPT) + LIFT:.6f}', lifted=True, echo=False)))
        ok_case('㉓ r3 식 재시작 (zmax run 1 · run 0 · 루프 ckpt+1) — 통과 (짧은 블록은 압력 열 검사 밖) · 판 높이 = 메시 보간',
                [os.path.join(sc, 'r1.out'), os.path.join(r3s, 'r3.out')], want_note='보간')
        refused('㉔ r3 식 구조의 판 재부양 (r2 꼴) 거부 — C3 (메시 보간 대조)',
                ['--segment', os.path.join(sc, 'r1.out'), '--segment', os.path.join(r3s, 'r2.out'), '--mesh-dir', md], 'C3')
        write(os.path.join(r3s, 'r5.out'), screen_only(restart_r3style(plate=f'{z_of(CKPT):.6f}', ckpt=8000, echo=False)))
        refused('㉕ 늦은 체크포인트에 옛 판 높이 (r5 꼴 · 판 재부양) 거부 — C3',
                ['--segment', os.path.join(sc, 'r1.out'), '--segment', os.path.join(r3s, 'r3.out'),
                 '--segment', os.path.join(r3s, 'r5.out'), '--mesh-dir', md], 'C3')

        # ── 표지 없는 이완: 판정 줄 탈출 step 으로 경계 ──
        q = os.path.join(tmp, 'nomark')
        os.makedirs(q)
        write(os.path.join(q, 'r3.out'), restart_lines(plate=f'{z_of(CKPT):.6f}', phase4_marker=False))
        out2 = os.path.join(tmp, 'ok_nomark')
        try:
            rc = run(['--segment', p['r1'], '--segment', os.path.join(q, 'r3.out'), '--mesh-dir', md, '--out', out2])
            s2 = load(out2)
            b4 = s2.get('phase_bounds', {}).get('4', {})
            check('⑳ PHASE 4 표지 없음 → 판정 줄 탈출 step 8,500 (출처 loop_exit)',
                  rc == 0 and b4.get('step') == EXIT and b4.get('source') == 'loop_exit', f'rc={rc} {b4}')
        except Exception as e:
            check('⑳ PHASE 4 표지 없음 → 판정 줄 탈출 step', False, f'예외 {type(e).__name__}: {e}')
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print(f'compaction_curve 시험: {ok} 통과 · {bad} 실패')
    return 0 if bad == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
