#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rint G2 ①′ — T4-1 `ledger_census` 계산 시험 (합성 침대 · 반례 먼저 · 2026-10-13).

T4-1 (v2 §4 L414 · v3 §7-1 L327 · v3.1 §1 N8b) census 의 **셈 자체**가 맞는지 합성 침대로 본다 — 실침대 수치는 보고 전용 산출
(docs/data/rint_t41_census_20261013/) 이지 이 시험의 대상이 아니다.  예외 법칙 (D4′) 결정 아님 · 솔브 없음.

  python3 scripts/test_rint_t4_census.py
"""
import os
import sys
import tempfile

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))

_ok, _fail = 0, []


def chk(name, cond, why=''):
    global _ok
    if cond:
        _ok += 1
        print(f'  PASS  {name}')
    else:
        _fail.append(name)
        print(f'  FAIL  {name}' + (f'  ({why})' if why else ''))
    return bool(cond)


def write_scaffold(td, rows, name='s.csv'):
    p = os.path.join(td, name)
    with open(p, 'w', encoding='utf-8') as fh:
        fh.write('# type,x,y,z,r  # test scaffold (AM_P=1,AM_S=2)\n' + '\n'.join(rows) + '\n')
    return p


def run_case(T, td, rows, L_um, cfg=(0.2, 0.24), db=0.0029):
    p = write_scaffold(td, rows)
    T.CONFIGS['_t'] = {'vox': cfg[0], 'bridge_um': cfg[1], 'basis': 'test'}
    try:
        return T.census_job('t', '_t', scaffold=p, box_lateral_um=L_um, delta_bound_um=db, delta_bound_source='test')
    finally:
        T.CONFIGS.pop('_t', None)


def main():
    try:
        import rint_t41_census as T
    except Exception as e:                                  # noqa: BLE001 — 고치기 전 (모듈 없음) 도 사례 단위로 기록
        print(f'  (rint_t41_census import 실패: {type(e).__name__}: {e})')
        T = None
    cases = []

    def case(fn):
        cases.append(fn)
        return fn

    @case
    def c1(td):
        print('C1 — 합성 침대: AM_S 접촉 1 · AM_P 간극 브리지 1 · 옆면 주기로만 닿는 AM_S 쌍 1')
        rows = ['2,0.003000,0.003000,0.002000,0.001000', '2,0.003000,0.003000,0.003980,0.001000',
                '1,0.007000,0.006500,0.002000,0.001500', '1,0.010040,0.006500,0.002000,0.001500',
                '2,0.000500,0.010000,0.002000,0.001000', '2,0.011480,0.010000,0.002000,0.001000']
        res = run_case(T, td, rows, 12.0)
        cl = res['classes']
        chk('C1 부류 합 = 등록 쌍 2 · contact 1 · gap_bridged 1 · ambiguous 0', sum(cl.values()) == res['n_registered_pairs'] == 2
            and cl['contact'] == 1 and cl['gap_bridged'] == 1 and cl['ambiguous'] == 0, repr(cl))
        chk('C1 종류별: contact = AM_S|AM_S · gap = AM_P|AM_P', res['classes_by_type']['AM_S|AM_S']['contact'] == 1
            and res['classes_by_type']['AM_P|AM_P']['gap_bridged'] == 1, repr(res['classes_by_type']))
        sot = res['support_over_true_contact']
        chk('C1 support/true 표본 1 (contact 중 면 있는 것) · 값 > 1 (브리지 0.24 > a — 원판보다 넓은 support)',
            sot is not None and sot['n'] == 1 and sot['p50'] > 1.0, repr(sot))
        chk('C1 미실현 0 · 탄소 덮인 목 몫 = 0 (정의상 · 첨가제 점 집합 없음 표지)', res['unrealized']['n'] == 0
            and res['carbon_covered_neck_share'] == 0.0 and '첨가제' in res['carbon_covered_neck_share_note'])
        chk('C1 옆면 주기로만 닿는 쌍 = seam 1 (닿음 · 브리지 규칙)', res['seam_scaffold'] == {**res['seam_scaffold'], 'n_touch': 1, 'n_bridge_rule': 1},
            repr(res['seam_scaffold']))
        chk('C1 거부 없음 · N8 · N8b = 0 · a_lt_h 분모 = contact 수', res['rejections'] == [] and res['n8_exact_duplicate'] == 0
            and res['n8b_concentric_nonidentical'] == 0 and res['a_lt_h']['contact_of'] == 1)

    @case
    def c2(td):
        print('C2 — 동심 비동일 (N8b) 쌍이 있는 침대 → census 가 수를 싣고 owner 없음 표지')
        rows = ['2,0.003000,0.003000,0.002000,0.001000', '1,0.003000,0.003000,0.002000,0.001500',
                '2,0.008000,0.003000,0.002000,0.001000']
        res = run_case(T, td, rows, 12.0)
        chk('C2 N8b 수 1 · owner 없음 note · 나머지 census 없음', res['n8b_concentric_nonidentical'] == 1 and 'note' in res
            and 'classes' not in res, repr({k: res.get(k) for k in ('n8b_concentric_nonidentical', 'note')}))

    @case
    def c3(td):
        print('C3 — 접촉점이 raster 상자 밖 (바닥 아래) 인 contact → 미실현 box_clip')
        rows = ['2,0.003000,0.003000,0.000500,0.001000', '2,0.003000,0.003000,-0.001480,0.001000',
                '2,0.006000,0.003000,0.002000,0.001000']
        res = run_case(T, td, rows, 12.0)
        u = res.get('unrealized', {})
        chk('C3 contact 1 · 미실현 1 = box_clip 1 · no_support 0 · carbon 0', res.get('classes', {}).get('contact') == 1
            and u.get('n') == 1 and u.get('box_clip') == 1 and u.get('no_support') == 0 and u.get('carbon') == 0, repr(u))

    with tempfile.TemporaryDirectory() as td:
        for fn in cases:
            print(f'\n── {fn.__name__}')
            try:
                if T is None:
                    raise ImportError('rint_t41_census 없음')
                fn(td)
            except Exception as e:                          # noqa: BLE001
                chk(f'{fn.__name__}: 실행', False, f'{type(e).__name__}: {e}')
    print(f'\n{_ok} PASS · {len(_fail)} FAIL')
    if _fail:
        for n in _fail:
            print('  -', n)
        sys.exit(1)


if __name__ == '__main__':
    main()
