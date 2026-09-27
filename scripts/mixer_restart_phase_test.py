#!/usr/bin/env python3
"""mixer_restart_phase_test.py — 재개-위상 영수증 (2026-09-27 저녁, Codex 재리뷰 HBR2-01 · K2).

왜 — 믹서 드럼은 39 각형이라 벽 겹침은 회전각에 걸린다 (면 한가운데와 꼭짓점의 차 = SE 반경의 56 %).  덱은 mesh 를 덤프하지
않으므로 벽 판정의 근거는 **예정각** (2π·(s − start)·dt/period) 뿐인데, 그 식이 **재개 (read_restart) 뒤에도 이어지는지**는
소스 근거 (FixMoveMesh::restart 가 time_ 을 복원 · MeshMoverRotate 가 ω·dt 누적) 이지 이 바이너리의 실측이 아니었다.
입자 배치로 각을 되읽는 fitting 은 증거가 아니다 (참 겹침 2 % + 반 면각 어긋남을 PASS 로 승격 — `check_contact_validity` ⑮).

무엇 — 실제 캠페인 덱에서 **입자만 뺀** 두 덱을 만든다 (같은 바이너리 · 같은 fix ID · 같은 메시 · 같은 주기):
  A (기준)  회전 N1 step → `write_restart` → N2 step 더 · `dump mesh/stl` 로 드럼을 매 E step 덤프
  B (재개)  `read_restart` 로 N1 에서 이어 N2 step · 같은 덤프
그리고 B 의 mesh 덤프를 (i) 같은 step 의 A 덤프와 (꼭짓점 좌표 일치) (ii) 예정각 2π·s·dt/period 와 (iii) "재개 때 위상이 0 으로
돌아간" 대안 2π·(s − N1)·dt/period 와 대조한다.  (i)(ii) 가 맞고 (iii) 과 구분되면 **통과** → 영수증 JSON.
`check_contact_validity.py --contract --phase-receipt <영수증>` 은 그 영수증의 주기 · 축이 덱과 맞을 때만 예정각 (± 각 오차) 으로 벽을 잰다.

⚠ 영수증은 **바이너리의 성질** (재개가 위상을 잇는다) 이지 어느 런의 벽 좌표가 아니다.  바이너리가 바뀌면 다시 만든다.
⚠ 입자 0 개로 돈다 — LIGGGHTS 가 빈 계에서 거부하는 명령이 있으면 로그를 보고 여기를 고친다 (WSL 에서만 실행 가능).

    python3 scripts/mixer_restart_phase_test.py gen --deck runs/LC_s32452843/in.mixer --out phase_test
    bash phase_test/run.sh                      # WSL · lmp_serial (LMP=… 로 바꿈) · 초 단위
    python3 scripts/mixer_restart_phase_test.py analyze phase_test --binary "$(command -v lmp_serial)" \
        --out docs/data/mixer_phase_receipt_<날짜>.json
    python3 scripts/mixer_restart_phase_test.py --selftest
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
import shutil
import sys

import numpy as np

_SCR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _SCR)
from make_mixer_resume import logical_commands, _tokens                  # noqa: E402  덱 논리 명령 파서 — 한 벌만 둔다

N1, N2, EVERY = 20000, 10000, 5000        # 회전 N1 → 체크포인트 → N2 · mesh 덤프 간격 (캠페인 dt 0.7 µs · 주기 ≈ 0.8 s ⇒ N1 ≈ 6.3°)
DROP_FIX = ('particletemplate/', 'particledistribution/', 'insert/')
TOL_DEG, RESET_GAP_DEG = 0.05, 1.0        # 예정각 허용 오차 · 재개-리셋 대안과의 최소 간격


def gen_decks(deck_text, n1=N1, n2=N2, every=EVERY):
    """캠페인 덱 → (덱 A, 덱 B).  입자 관련 명령 (템플릿 · 분포 · 삽입 · 그 region · unfix · 원자 dump · run · restart · write_restart ·
    shell) 을 빼고 나머지 (재료 · 메시 · 벽 · 회전 · 적분기) 는 **순서 · ID 그대로**."""
    kept = []
    box_region = None
    for _, blk in logical_commands(deck_text):
        t = _tokens(blk)
        if not t:
            continue
        if t[0] == 'create_box':
            box_region = t[2] if len(t) > 2 else None
    for _, blk in logical_commands(deck_text):
        t = _tokens(blk)
        if not t:
            continue
        k = t[0]
        if k in ('run', 'write_restart', 'restart', 'unfix', 'dump', 'shell'):
            continue
        if k == 'fix' and len(t) > 3 and any(s in t[3] for s in DROP_FIX):
            continue
        if k == 'region' and t[1] != box_region:
            continue
        kept.append(' '.join(t))
    if not any(c.startswith('create_box') for c in kept):
        raise ValueError('덱에 create_box 가 없다')
    if not any('move/mesh' in c for c in kept):
        raise ValueError('덱에 move/mesh 가 없다 — 회전 덱이 아니다')
    dump = f'dump dmesh all mesh/stl {every} post_mesh/mesh_*.stl'
    a = kept + ['shell mkdir post_mesh restart_pt', dump, f'run {n1}', 'write_restart restart_pt/ckpt.bin', f'run {n2}']
    b = []
    for c in kept:
        if c.startswith('region ') and box_region and c.split()[1] == box_region:
            continue
        if c.startswith('create_box'):
            b.append('read_restart restart_pt/ckpt.bin')
            continue
        b.append(c)
    b += ['shell mkdir post_mesh', dump, f'run {n2}']
    hdr = '# 재개-위상 영수증 덱 {} — scripts/mixer_restart_phase_test.py 가 캠페인 덱에서 입자만 빼고 만듦 (fix ID · 메시 · 주기 그대로)\n'
    return hdr.format('A (기준)') + '\n'.join(a) + '\n', hdr.format('B (read_restart 재개)') + '\n'.join(b) + '\n'


RUN_SH = """#!/bin/bash
# 재개-위상 시험 — A (기준 · 체크포인트) → B (read_restart 재개).  WSL 에서: bash run.sh   (LMP=경로 로 바이너리 지정)
set -e
cd "$(dirname "$0")"
LMP=${LMP:-lmp_serial}
( cd A && mkdir -p post_mesh restart_pt && "$LMP" -in in.phase_a > log.lmp 2>&1 )
( cd B && mkdir -p post_mesh && rm -rf restart_pt && cp -r ../A/restart_pt . && "$LMP" -in in.phase_b > log.lmp 2>&1 )
echo "끝 — 분석: python3 scripts/mixer_restart_phase_test.py analyze $(pwd) --binary \\"$(command -v "$LMP")\\" --out docs/data/mixer_phase_receipt_$(date +%Y%m%d).json"
"""


def gen(deck_path, out):
    text = open(deck_path, encoding='utf-8', errors='replace').read()
    a, b = gen_decks(text)
    src = os.path.dirname(os.path.abspath(deck_path))
    for sub, dk, nm in (('A', a, 'in.phase_a'), ('B', b, 'in.phase_b')):
        d = os.path.join(out, sub)
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, nm), 'w', encoding='utf-8').write(dk)
        for stl in ('Drum.stl', 'Front.stl', 'Back.stl'):
            p = os.path.join(src, stl)
            if os.path.isfile(p):
                shutil.copyfile(p, os.path.join(d, stl))
    open(os.path.join(out, 'run.sh'), 'w', encoding='utf-8').write(RUN_SH)
    json.dump(dict(deck=os.path.abspath(deck_path), deck_sha256=hashlib.sha256(text.encode()).hexdigest(),
                   n1=N1, n2=N2, every=EVERY), open(os.path.join(out, 'gen.json'), 'w'), indent=1)
    print(f'→ {out}/A/in.phase_a · B/in.phase_b · run.sh   (다음: WSL 에서 bash {out}/run.sh)')


def _drum_angle(tris, axis, ref_vertex=None):
    """mesh 덤프 삼각형 → (드럼 표지 꼭짓점의 축 둘레 각, 그 꼭짓점).  드럼 = 법선이 축과 나란하지 않은 첫 삼각형."""
    a, b, c = tris[:, 0], tris[:, 1], tris[:, 2]
    nv = np.cross(b - a, c - a)
    nv = nv / np.maximum(np.linalg.norm(nv, axis=1), 1e-300)[:, None]
    drum = np.where(np.abs(nv @ axis) < 0.99)[0]
    if not len(drum):
        raise ValueError('드럼 삼각형이 없다')
    v = tris[drum[0], 0]
    e1 = np.cross(axis, [0.0, 0.0, 1.0])
    if np.linalg.norm(e1) < 1e-6:
        e1 = np.cross(axis, [0.0, 1.0, 0.0])
    e1 = e1 / np.linalg.norm(e1)
    e2 = np.cross(axis, e1)
    return float(np.arctan2(v @ e2, v @ e1)), v


def _wrap(x):
    return (x + np.pi) % (2 * np.pi) - np.pi


def analyze(d, binary=None, out=None, tol_deg=TOL_DEG):
    from check_contact_validity import read_stl, deck_walls
    deck_a = open(os.path.join(d, 'A', 'in.phase_a'), encoding='utf-8').read()
    spec = deck_walls(deck_a)
    mv = spec['moves']['Drum']
    dt, period, axis = spec['dt'], mv['period'], mv['axis']
    g = json.load(open(os.path.join(d, 'gen.json'))) if os.path.isfile(os.path.join(d, 'gen.json')) else dict(n1=N1, n2=N2)
    n1 = int(g['n1'])
    f, sc = spec['meshes']['Drum']
    T0 = read_stl(os.path.join(d, 'A', f)) * sc
    th0, _ = _drum_angle(T0, axis)
    stepsB = sorted(int(x[5:-4]) for x in os.listdir(os.path.join(d, 'B', 'post_mesh')) if x.startswith('mesh_') and x.endswith('.stl'))
    rows, err, gap, ab = [], 0.0, float('inf'), 0.0
    for s in stepsB:
        TB = read_stl(os.path.join(d, 'B', 'post_mesh', f'mesh_{s}.stl'))
        thB, _ = _drum_angle(TB, axis)
        obs = _wrap(thB - th0)
        cont = _wrap(2 * np.pi * s * dt / period)
        reset = _wrap(2 * np.pi * (s - n1) * dt / period)
        e = abs(np.degrees(_wrap(obs - cont)))
        gp = abs(np.degrees(_wrap(cont - reset)))
        pa = os.path.join(d, 'A', 'post_mesh', f'mesh_{s}.stl')
        dab = float(np.abs(read_stl(pa) - TB).max()) if os.path.isfile(pa) else float('nan')
        rows.append(dict(step=s, observed_deg=float(np.degrees(obs)), expected_continuity_deg=float(np.degrees(cont)),
                         expected_reset_deg=float(np.degrees(reset)), error_deg=float(e), reset_gap_deg=float(gp), ab_max_vertex_diff_m=dab))
        err, gap = max(err, e), min(gap, gp)
        if np.isfinite(dab):
            ab = max(ab, dab)
    scale = float(np.abs(T0).max())
    ok = bool(rows) and err <= tol_deg and gap >= RESET_GAP_DEG and ab <= 1e-9 * scale
    ver = ''
    for sub in ('A', 'B'):
        lp = os.path.join(d, sub, 'log.lmp')
        if os.path.isfile(lp):
            for line in open(lp, encoding='utf-8', errors='replace'):
                if 'LIGGGHTS' in line and 'Version' in line:
                    ver = line.strip()
                    break
        if ver:
            break
    rc = dict(test='restart_phase', passed=ok, period=float(period), axis=[float(x) for x in axis], dt=float(dt), n1=n1,
              n2=int(g.get('n2', N2)), steps_checked=stepsB, angle_error_deg=float(err), reset_alternative_gap_deg=float(gap) if rows else None,
              ab_max_vertex_diff_m=float(ab), rows=rows, liggghts_version=ver,
              binary_path=os.path.abspath(binary) if binary else None,
              binary_sha256=hashlib.sha256(open(binary, 'rb').read()).hexdigest() if binary and os.path.isfile(binary) else None,
              deck_source=g.get('deck'), deck_source_sha256=g.get('deck_sha256'),
              date=datetime.date.today().isoformat(),
              note='바이너리의 성질 (read_restart 뒤에도 메시 회전 위상이 이어진다) 의 실측 — 어느 런의 벽 좌표가 아니다.  바이너리가 바뀌면 다시 만든다.')
    if not rows:
        rc['note'] = 'B/post_mesh 에 mesh 덤프가 없다 — run.sh 가 돌지 않았거나 dump mesh/stl 이 거부됐다 (log.lmp 확인)'
    if out:
        json.dump(rc, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print(f'→ {out}')
    print(f'재개-위상 시험: {"통과" if ok else "실패"} — step {stepsB} · 예정각 오차 최대 {err:.4f}° (허용 {tol_deg}°) · '
          f'리셋 대안과 간격 최소 {gap if rows else float("nan"):.3f}° (요구 ≥ {RESET_GAP_DEG}°) · A↔B 꼭짓점 차 최대 {ab:.3g} m')
    return rc


def _selftest():
    import tempfile
    import importlib.util
    ok, fail = 0, []

    def chk(name, cond):
        nonlocal ok
        if cond:
            ok += 1
        else:
            fail.append(name)
        print(('  PASS  ' if cond else '  FAIL  ') + name)
    spec = importlib.util.spec_from_file_location('mmd', os.path.join(_SCR, 'make_mixer_deck.py'))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    lc = m.deck(m.plan(8000), rpm=60, revolutions=2, seed=32452843, arm='LC')
    a, b = gen_decks(lc)
    ta = [_tokens(x) for _, x in logical_commands(a)]
    tb = [_tokens(x) for _, x in logical_commands(b)]
    heads_a = [' '.join(t[:2]) for t in ta if t]
    heads_b = [' '.join(t[:2]) for t in tb if t]
    chk('① A: 입자 명령 (템플릿 · 분포 · 삽입 · unfix · 원자 dump · 원 run/restart/write_restart) 이 없다',
        not any(t and t[0] == 'fix' and any(s in t[3] for s in DROP_FIX) for t in ta)
        and not any(h.startswith(('unfix', 'dump dmp', 'restart ')) for h in heads_a)
        and sum(h.startswith('write_restart') for h in heads_a) == 1 and sum(h.startswith('run ') for h in heads_a) == 2)
    fa = [t[1] for t in ta if t and t[0] == 'fix']
    fb = [t[1] for t in tb if t and t[0] == 'fix']
    chk(f'② A · B 의 fix ID 열이 같다 (재료 · 메시 · 벽 · 회전 · 적분기 그대로) — {fa}',
        fa == fb and {'Drum', 'Front', 'Back', 'walls', 'mvD', 'mvF', 'mvB', 'mC'} <= set(fa))
    ib = next(i for i, t in enumerate(tb) if t and t[0] == 'read_restart')
    chk('③ B: create_box (와 그 region) 자리에 read_restart · write_restart 없음 · run 하나 · dump mesh/stl',
        'create_box' not in heads_b and not any(h.startswith('region') for h in heads_b)
        and not any(h.startswith('write_restart') for h in heads_b) and sum(h.startswith('run ') for h in heads_b) == 1
        and any(t and t[0] == 'dump' and t[3] == 'mesh/stl' for t in tb) and ib < next(i for i, t in enumerate(tb) if t and t[0] == 'fix'))
    from check_contact_validity import deck_walls, read_stl, _rot
    sa, s0 = deck_walls(a), deck_walls(lc)
    chk('④ 덱 A 의 드럼 회전 (주기 · 축) 이 캠페인 덱과 같고 회전 시작 step = 0',
        abs(sa['moves']['Drum']['period'] - s0['moves']['Drum']['period']) < 1e-12 and sa['moves']['Drum']['start_step'] == 0)
    #  ⑤ 합성 덤프로 분석기: 연속 (통과) · 리셋 (실패)
    stl = os.path.join(_SCR, '..', 'dem_scripts', 'mixer_20260919')

    def _write(path, T):
        with open(path, 'w') as fh:
            fh.write('solid m\n')
            for tri in T:
                fh.write(' facet normal 0 0 0\n  outer loop\n' + ''.join(f'   vertex {v[0]:.12e} {v[1]:.12e} {v[2]:.12e}\n' for v in tri)
                         + '  endloop\n endfacet\n')
            fh.write('endsolid m\n')
    with tempfile.TemporaryDirectory() as td:
        for sub in ('A', 'B'):
            os.makedirs(os.path.join(td, sub, 'post_mesh'))
            for nm in ('Drum.stl', 'Front.stl', 'Back.stl'):
                shutil.copyfile(os.path.join(stl, nm), os.path.join(td, sub, nm))
        open(os.path.join(td, 'A', 'in.phase_a'), 'w').write(a)
        open(os.path.join(td, 'A', 'log.lmp'), 'w').write('LIGGGHTS (Version LIGGGHTS-PUBLIC 3.8.0, compiled test)\n')
        json.dump(dict(n1=N1, n2=N2, every=EVERY, deck='x', deck_sha256='0' * 64), open(os.path.join(td, 'gen.json'), 'w'))
        f, sc = sa['meshes']['Drum']
        dt, per, ax = sa['dt'], sa['moves']['Drum']['period'], sa['moves']['Drum']['axis']
        T = np.vstack([read_stl(os.path.join(td, 'A', nm)) * sa['meshes'][k][1] for k, nm in (('Drum', 'Drum.stl'), ('Front', 'Front.stl'), ('Back', 'Back.stl'))])

        def dumps(shift):
            for s in (N1 + EVERY, N1 + 2 * EVERY):
                for sub, off in (('A', 0), ('B', shift)):
                    R = _rot(ax, 2 * np.pi * (s - off) * dt / per)
                    _write(os.path.join(td, sub, 'post_mesh', f'mesh_{s}.stl'), T @ R.T)
        bin_ = os.path.join(td, 'lmp_fake')
        open(bin_, 'wb').write(b'fake')
        dumps(0)
        rc = analyze(td, binary=bin_, out=os.path.join(td, 'r.json'))
        chk(f'⑤ 연속 (재개가 위상을 잇는다) → 통과 · 각 오차 {rc["angle_error_deg"]:.2e}° · 리셋 대안과 {rc["reset_alternative_gap_deg"]:.2f}° 차 · 버전 · sha 기록',
            rc['passed'] and rc['angle_error_deg'] < 1e-6 and rc['reset_alternative_gap_deg'] > RESET_GAP_DEG
            and rc['liggghts_version'].startswith('LIGGGHTS') and len(rc['binary_sha256']) == 64)
        dumps(N1)
        rc2 = analyze(td, binary=bin_)
        chk(f'⑤b 리셋 (재개 때 위상이 0 으로) → 실패 · 각 오차 {rc2["angle_error_deg"]:.3f}° ≈ N1 만큼',
            not rc2['passed'] and abs(rc2['angle_error_deg'] - 360 * N1 * dt / per) < 1e-6 and rc2['ab_max_vertex_diff_m'] > 0)
        #  ⑥ check_contact_validity 가 이 영수증을 받는다 (주기 · 축 일치) · 주기가 다른 덱은 거부
        from check_contact_validity import load_phase_receipt
        r_ok = load_phase_receipt(os.path.join(td, 'r.json'), s0)
        s_bad = dict(s0)
        s_bad['moves'] = dict(s0['moves'])
        s_bad['moves']['Drum'] = dict(s0['moves']['Drum'], period=s0['moves']['Drum']['period'] * 2)
        try:
            load_phase_receipt(os.path.join(td, 'r.json'), s_bad)
            rej = False
        except ValueError:
            rej = True
        chk('⑥ 영수증을 검사기가 받고 (같은 주기 · 축), 주기가 다른 덱에는 거부한다', r_ok['passed'] and rej)
    print(f'\nmixer_restart_phase_test selftest: {ok}/{ok + len(fail)} PASS' + (f'   FAILED: {fail}' if fail else ''))
    return 1 if fail else 0


def main():
    ap = argparse.ArgumentParser(description='재개-위상 영수증 (Codex HBR2-01 · K2) — 덱 생성 · 분석')
    sub = ap.add_subparsers(dest='cmd')
    g = sub.add_parser('gen', help='캠페인 덱 → 입자 없는 A/B 덱 + run.sh')
    g.add_argument('--deck', required=True, help='실행 덱 (runs/<팔>_s<시드>/in.mixer) — STL 은 옆에서 복사')
    g.add_argument('--out', required=True)
    an = sub.add_parser('analyze', help='run.sh 뒤: mesh 덤프 대조 → 영수증 JSON')
    an.add_argument('dir')
    an.add_argument('--binary', default=None, help='돌린 lmp 바이너리 경로 (sha256 을 영수증에)')
    an.add_argument('--out', default=None)
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        raise SystemExit(_selftest())
    if a.cmd == 'gen':
        gen(a.deck, a.out)
    elif a.cmd == 'analyze':
        rc = analyze(a.dir, a.binary, a.out)
        raise SystemExit(0 if rc['passed'] else 1)
    else:
        ap.error('gen | analyze | --selftest')


if __name__ == '__main__':
    main()
