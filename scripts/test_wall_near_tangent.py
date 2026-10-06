#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""벽 접촉 판정의 **근접 접선 수** — 원장 LHSC-08 (Codex 09-30 · P3 · 5번 재수확 보고 항목).

  python3 scripts/test_wall_near_tangent.py      # 종료코드 0 = PASS

결함 (LHSC-08): 수확기의 벽 규칙은 **저장 좌표에서** 양의 cap 깊이 (`_wall_contact` · depth = r − dist > 0) 이지 반올림 전 실제 접촉 분류가
아니다 — 깊이 r − z + z_벽 의 불확실폭 (토큰 반올림 반폭 합) 안에 드는 |depth| 수를 상 · 벽별로 보고하지 않았다 · STL 정밀도는 atom dump 의
6 자리 가정을 복제하지 말고 따로 읽어야 한다.
처방 (원장 그대로): 분류는 **바꾸지 않는다** (조용히 정하지 않는다) — 근접 접선 수를 상 · 벽별로 **센다** (새 키 `wall_near_tangent`) ·
정밀도는 파일마다 토큰에서 읽는다 (atom = 마지막 프레임 x · y · z · radius · 판 = STL 꼭짓점 좌표 · 바닥 = 덱 zplane 리터럴 0 = 반폭 0).

★ 시험 먼저 — 옛 코드 (a0a24c538) 에는 함수 · 키가 없다 → W · H 가 빨갛다.
  W1 토큰 유효숫자 (끝 0 도 센다 · %g 끝 0 지움과 같은 값) · W2 손으로 짠 배치의 상 · 벽별 근접 수 (경계에서 여유를 둔 값) ·
  H1 harvest() 산출 = 같은 배열의 함수 값 · 정밀도 출처 · H2 ★ 같은 판 높이를 STL 에 6 자리 ↔ 9 자리 (끝 0) 로 적으면 판 근접 수가 달라진다
  (atom 의 6 자리를 복제했다면 같았다) · H3 CLI plate_z 는 그 수의 자릿수 · H4 분류 (wall_touch · wall_record) 는 그대로 ·
  R  실침대 real_14 · case15 (커밋 덤프 · 덱 · STL) 의 상 · 벽별 근접 수 (값은 보고 · 구조만 단언)
"""
import gzip
import os
import shutil
import sys
import tempfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
_ok, _fail = 0, []


def chk(name, cond, extra=''):
    global _ok
    if cond:
        _ok += 1
        print(f'  PASS  {name}' + (f'   {extra}' if extra else ''))
    else:
        _fail.append(name)
        print(f'  FAIL  {name}' + (f'   {extra}' if extra else ''))
    return bool(cond)


def _guard(label, fn):
    try:
        fn()
    except Exception as e:                                       # noqa: BLE001 — 옛 코드 = 없는 함수 · 키도 FAIL 로 센다
        import traceback
        traceback.print_exc()
        chk(f'{label} — 예외 {type(e).__name__}: {e}', False)


# ── 손으로 짠 배치 (덤프 단위 · 6 유효숫자 토큰) ─────────────────────────────────────────
#: 판 = 0.0198765 (6 자리 → 반폭 5e-8).  바닥 = 0 (덱 리터럴 · 반폭 0).  반폭 h(v) = 0.5·10^(E(v) − 6 + 1).
#: (id, type, r, z, 벽, 기대: 'near_touch' · 'near_not' · 'far')  — 깊이 · 허용폭은 주석 (여유를 경계에서 뗐다)
PLATE = 0.0198765
BED = [
    # 바닥: depth = r − z
    (1, 3, 0.001, 0.000999999, 'floor', 'near_touch'),   # depth +1e-9 · u = 5e-9 + 5e-10 = 5.5e-9
    (2, 3, 0.001, 0.001, 'floor', 'near_not'),           # depth 0 (정확히 접선 — 규칙은 안 닿음) · u = 1e-8
    (3, 3, 0.001, 0.00100002, 'floor', 'far'),           # depth −2e-8 · u = 1e-8
    (4, 1, 0.003, 0.0005, 'floor', 'far'),               # depth +2.5e-3 (깊이 닿음)
    (5, 2, 0.001, 0.005, 'floor', 'far'),                # depth −4e-3 (안쪽)
    # 판: depth = r + z − 판
    (6, 1, 0.003, 0.0168765, 'plate', 'near_touch'),     # 토큰상 정확히 접선인데 부동소수 합 = +8.7e-19 → 규칙은 '닿음' (LHSC-08 이 겨누는 경우) ·
                                                         # u = 5e-9 + 5e-8 + 5e-8 = 1.05e-7
    (7, 1, 0.003, 0.0168766, 'plate', 'near_touch'),     # depth +1e-7 · u = 1.05e-7
    (8, 2, 0.001, 0.018876, 'plate', 'far'),             # depth −5e-7 (안쪽)
    (9, 3, 0.0005, 0.0193763, 'plate', 'far'),           # depth −2e-7 · u = 1.005e-7
    (10, 3, 0.0005, 0.0193764, 'plate', 'near_not'),     # depth −1e-7 · u = 1.005e-7
]


def _expect(phase_of, wall):
    out = {}
    for _i, t, _r, _z, w, kind in BED:
        if w != wall:
            continue
        for ph in (phase_of[t], 'total') + (('AM',) if phase_of[t] in ('AM_P', 'AM_S') else ()):
            d = out.setdefault(ph, {'n_near': 0, 'n_near_touch': 0, 'n_near_not': 0})
            if kind != 'far':
                d['n_near'] += 1
                d['n_near_touch' if kind == 'near_touch' else 'n_near_not'] += 1
    return out


def _write_atom(path, rows, ts=100):
    with open(path, 'w') as fh:
        fh.write(f'ITEM: TIMESTEP\n{ts}\nITEM: NUMBER OF ATOMS\n{len(rows)}\nITEM: BOX BOUNDS pp pp ff\n')
        fh.write('0 0.05\n0 0.05\n-0.01 1\nITEM: ATOMS id type x y z radius\n')
        for i, t, r, z, *_ in rows:
            fh.write(f'{i} {t} {0.0012345 + 0.004 * (i % 10):.6g} 0.0251234 {z!r} {r!r}\n')   # 6 유효숫자 토큰만


def _write_contact(path, ts=100):
    with open(path, 'w') as fh:
        fh.write(f'ITEM: TIMESTEP\n{ts}\nITEM: NUMBER OF ENTRIES\n1\nITEM: ENTRIES c_cpl[7] c_cpl[8] c_cpl[22]\n')
        fh.write('4 1 1e-07\n')


def _write_stl(path, ztok):
    with open(path, 'w') as fh:
        fh.write('solid p\n  facet normal 0 0 -1\n    outer loop\n')
        for xy in ('0 0', '0.05 0.05', '0.05 0'):
            fh.write(f'      vertex {xy} {ztok}\n')
        fh.write('    endloop\n  endfacet\nendsolid p\n')


def _write_deck(path):
    with open(path, 'w') as fh:
        fh.write('region reg_box block 0.0 0.05 0.0 0.05 -0.01 1.0 units box\n'
                 'fix zwall_bot all wall/gran model hooke/hysteresis tangential history rolling_friction cdt primitive type 1 '
                 'zplane 0.0\n')


def section_w():
    print('[W] 함수 — 토큰 유효숫자 · 상 · 벽별 근접 접선 수')
    import lhs_descriptor_harvest as H
    ts, wn = getattr(H, '_token_sigfig', None), getattr(H, 'wall_near_tangent', None)
    if not chk('W0 _token_sigfig · wall_near_tangent · atom_dump_sigfig · plate_stl_sigfig 가 있다',
               callable(ts) and callable(wn) and callable(getattr(H, 'atom_dump_sigfig', None))
               and callable(getattr(H, 'plate_stl_sigfig', None))):
        return
    cases = {'0.0302845': 6, '0.030000': 5, '0.0198765000': 9, '3.34479e-06': 6, '-0.00123': 3, '0': 0, '0.05': 1,
             '1e-05': 1, '120': 3}
    got = {k: ts(k) for k in cases}
    chk('W1 토큰 유효숫자 = 앞 0 · 부호 · 소수점 · 지수 빼고 끝 0 은 센다 (lhs_contact_audit._sigfigs 와 같은 규칙)', got == cases,
        repr({k: (got[k], v) for k, v in cases.items() if got[k] != v}))
    labels = np.asarray([H.TYPE_MAP[3][t] for _i, t, *_ in BED], dtype=object)
    z = np.asarray([b[3] for b in BED])
    r = np.asarray([b[2] for b in BED])
    res = wn(labels, z, r, PLATE, sig_atom=6, sig_plate=6)
    bp = res.get('by_phase') or {}
    for wall in ('floor', 'plate'):
        want = _expect(H.TYPE_MAP[3], wall)
        gotw = {ph: {k: (bp.get(ph) or {}).get(wall, {}).get(k) for k in ('n_near', 'n_near_touch', 'n_near_not')}
                for ph in want}
        chk(f'W2 {wall}: 상별 근접 접선 수 = 손계산 (경계 여유 둔 깊이 · 정확히 접선 depth 0 도 근접 · 분류 쪽까지)', gotw == want,
            f'{gotw} vs {want}')
    chk('W3 상 그룹 = 있는 상 + AM (P · S 둘 다 있을 때) + total · n = 그 상의 입자 수',
        set(bp) == {'AM_P', 'AM_S', 'SE', 'AM', 'total'} and bp['SE']['n'] == 5 and bp['total']['n'] == 10, repr(sorted(bp)))


def _bed_files(tmp, ztok, name):
    a, c, s, d = (os.path.join(tmp, f'{name}_{x}') for x in ('atom_100.liggghts', 'contact_100.liggghts', 'mesh.stl', 'in.deck'))
    _write_atom(a, BED)
    _write_contact(c)
    _write_stl(s, ztok)
    _write_deck(d)
    return a, c, s, d


def section_h(tmp):
    print('[H] harvest() — 새 키 wall_near_tangent · 정밀도 출처 · 분류 불변')
    import lhs_descriptor_harvest as H
    a, c, s, d = _bed_files(tmp, '0.0198765', 'six')
    r6 = H.harvest(a, c, 3, 'near6', mesh_path=s, deck_path=d)
    w6 = r6.get('wall_near_tangent')
    if not chk('H0 harvest 산출에 wall_near_tangent 가 있다 (맨 뒤 새 키)', isinstance(w6, dict) and list(r6)[-1] == 'wall_near_tangent',
               repr(list(r6)[-3:])):
        return
    labels = np.asarray([H.TYPE_MAP[3][t] for _i, t, *_ in BED], dtype=object)
    ref = H.wall_near_tangent(labels, np.asarray([b[3] for b in BED]), np.asarray([b[2] for b in BED]), PLATE,
                              sig_atom=6, sig_plate=6)
    chk('H1 harvest 값 = 같은 배열 · 같은 자릿수의 함수 값 · atom 자릿수 6 (덤프 토큰에서) · 판 6 (STL 토큰에서) · 바닥 = 덱 리터럴',
        w6.get('by_phase') == ref.get('by_phase') and w6.get('sigfig_atom') == 6 and w6.get('sigfig_plate') == 6
        and w6.get('plate_z_source') == 'mesh_stl' and str(w6.get('floor_z_source', '')).startswith('deck'),
        repr({k: w6.get(k) for k in ('sigfig_atom', 'sigfig_plate', 'plate_z_source', 'floor_z_source')}))
    a2, c2, s2, d2 = _bed_files(tmp, '0.0198765000', 'ten')
    r10 = H.harvest(a2, c2, 3, 'near10', mesh_path=s2, deck_path=d2)
    w10 = r10['wall_near_tangent']
    n6 = w6['by_phase']['AM_P']['plate']
    n10 = w10['by_phase']['AM_P']['plate']
    chk('H2 ★ 같은 판 높이를 STL 에 9 자리 (끝 0 셋) 로 적으면 판 반폭이 줄어 AM_P 근접 2 → 1 (depth +1e-7 이 빠진다 · +8.7e-19 는 남는다) · '
        '바닥은 그대로 · atom 자릿수는 6 그대로 — STL 정밀도를 따로 읽는다 (atom 의 6 자리를 복제했다면 같았다)',
        w10['sigfig_plate'] == 9 and w10['sigfig_atom'] == 6 and n6['n_near'] == 2 and n6['n_near_touch'] == 2
        and n10['n_near'] == 1 and n10['n_near_touch'] == 1 and w10['by_phase']['total']['floor'] == w6['by_phase']['total']['floor'],
        f'6 자리 {n6} · 9 자리 {n10}')
    rc = H.harvest(a, c, 3, 'nearcli', plate_z=PLATE, deck_path=d)
    wc = rc['wall_near_tangent']
    chk('H3 CLI plate_z → 판 자릿수 = 그 수의 자릿수 (repr 0.0198765 → 6) · 출처 cli_explicit · 값 = STL 6 자리와 같다',
        wc['plate_z_source'] == 'cli_explicit' and wc['sigfig_plate'] == 6 and wc['by_phase'] == w6['by_phase'],
        repr({k: wc.get(k) for k in ('plate_z_source', 'sigfig_plate')}))
    keep = ('wall_touch', 'wall_touch_rule', 'wall_record', 'coverage_wall_split', 'status')
    hq6 = {k: v for k, v in r6['handover_qc'].items() if k != 'mesh_sha256'}
    hq10 = {k: v for k, v in r10['handover_qc'].items() if k != 'mesh_sha256'}
    chk('H4 분류는 그대로 — STL 자릿수만 다른 두 수확의 wall_touch · wall_record · 벽 분할 · status · handover_qc (메시 해시 빼고) 가 같다 '
        '(근접 수만 다르다) · 토큰상 접선인 입자 6 은 규칙대로 닿음으로 남는다',
        all(r6[k] == r10[k] for k in keep) and hq6 == hq10 and r6['wall_near_tangent'] != r10['wall_near_tangent']
        and r6['wall_touch']['AM_P']['n_plate'] == 2)
    chk('H5 규칙 문자열 = 분류 불변 · 정밀도 출처 (STL 따로) · LHSC-08', all(x in str(w6.get('rule')) for x in ('LHSC-08', 'STL', '바꾸지')),
        str(w6.get('rule'))[:160])


def section_r(tmp):
    print('[R] 실침대 — 커밋 덤프 · 덱 · STL 의 상 · 벽별 근접 접선 수 (보고)')
    import lhs_descriptor_harvest as H
    from lhs_perc_extract import read_atom_dump
    for bed, d, fa, deck, stl, nt in (
            ('real14', 'docs/data/real14_reference_20260928', 'atom_2060000.liggghts.gz', 'input_real_14.liggghts',
             'mesh_2060000.stl', 3),
            ('case15', 'docs/data/case15_corner_20261001', 'atom_v4_1710000.liggghts.gz', 'input_case15.liggghts',
             'mesh_v4_1710000.stl', 2)):
        base = os.path.join(ROOT, d)
        atom = os.path.join(tmp, f'{bed}_atom.liggghts')
        with open(atom, 'wb') as fh:
            fh.write(gzip.open(os.path.join(base, fa)).read())
        atoms, _lo, _hi, _bc = read_atom_dump(atom)
        labels, _tm = H.phase_labels(atoms['type'], nt)
        sa, sp = H.atom_dump_sigfig(atom), H.plate_stl_sigfig(os.path.join(base, stl))
        H.check_deck_floor(os.path.join(base, deck))
        pz = H.plate_z_from_stl(os.path.join(base, stl))
        w = H.wall_near_tangent(labels, atoms['z'], atoms['radius'], pz, sig_atom=sa, sig_plate=sp)
        tot = w['by_phase']['total']
        print(f'    {bed}: atom 자릿수 {sa} · STL {sp} · 판 {pz} · 근접 (바닥 · 판) = '
              + ' · '.join(f"{ph} {v['floor']['n_near']}/{v['plate']['n_near']} (n {v['n']})" for ph, v in w['by_phase'].items()))
        chk(f'R {bed}: 자릿수 atom 6 · STL 6 (각 파일 토큰에서) · 근접 수는 0 ≤ k ≤ n 정수 · touch + not = near',
            sa == 6 and sp == 6 and all(isinstance(v[wl]['n_near'], int) and 0 <= v[wl]['n_near'] <= v['n']
                                        and v[wl]['n_near_touch'] + v[wl]['n_near_not'] == v[wl]['n_near']
                                        for v in w['by_phase'].values() for wl in ('floor', 'plate')),
            f"total 바닥 {tot['floor']} · 판 {tot['plate']}")


def main():
    tmp = tempfile.mkdtemp(prefix='lhsc08_')
    try:
        _guard('[W]', section_w)
        _guard('[H]', lambda: section_h(tmp))
        _guard('[R]', lambda: section_r(tmp))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print(f'\n{_ok} PASS · {len(_fail)} FAIL')
    if _fail:
        for f in _fail:
            print('  -', f)
        return 1
    print('ALL PASS')
    return 0


if __name__ == '__main__':
    sys.exit(main())
