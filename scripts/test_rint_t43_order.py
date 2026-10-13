#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rint G2 ①′ — T4-3 `raster_order_size` (RINTG-11) 진단 도구 시험 (합성 · 반례 먼저 · 2026-10-13).

등록 = docs/reviews/rint_t43_order_dependence_registration_20261013.md (K 7 · seed · 보고 항목 — 실행 전 커밋).
이 시험은 **도구의 셈**을 답이 알려진 합성 반례로 본다 — 실침대 수치는 보고 전용 산출 (docs/data/rint_t43_order_20261013/).

  python3 scripts/test_rint_t43_order.py
"""
import os
import sys

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


#  Codex RINTG2-01 혼합 종류 두 구 (sid 16 셀 · 렌즈 z 1.95 µm 한 층) · RINTV3-02 브리지 끝자리 (3170 ↔ 3171 · 셀 (15,15,15))
CODEX_C = np.array([[1., 1., 1.], [1., 1., 2.9]]); CODEX_R = np.ones(2); CODEX_T = np.array([2, 1])
V02_C = np.array([[1.9748831001799223, 1.8791293045780670, 1.7896943576126298],
                  [1.0611990064053260, 0.8549090548944595, 1.7364778658264648]])
V02_R = np.array([0.5348361452776790, 0.8437277367739292]); V02_T = np.array([2, 1])


def main():
    try:
        import rint_t43_order_diag as D
    except Exception as e:                                  # noqa: BLE001 — 고치기 전 (모듈 없음) 도 사례 단위로 기록
        print(f'  (rint_t43_order_diag import 실패: {type(e).__name__}: {e})')
        D = None
    cases = []

    def case(fn):
        cases.append(fn)
        return fn

    @case
    def o1():
        print('O1 — 혼합 종류 두 구 (Codex RINTG2-01) · 순서 [1,0] ↔ [0,1] · vox 0.1 · 브리지 0.24')
        R = D.order_diag_raster(CODEX_C, CODEX_R, CODEX_T, (0.0, 0.0, 0.0), (2.0, 2.0, 3.9), 0.1, 0.24,
                                [np.array([0, 1]), np.array([1, 0])])
        p = R['perms'][0]
        chk('O1 sid 다른 셀 16 = 라벨 전이 16 · 마스크 0 · 자리 lens 16 · 렌즈 종류 mixed 16',
            p['n_sid_diff'] == 16 and p['n_label'] == 16 and p['n_mask'] == 0 and p['loc']['lens'] == 16
            and p['loc']['bridge'] == 0 and p['loc']['other'] == 0 and p['lens_kind']['mixed'] == 16, repr(p)[:400])
        chk('O1 pid 다른 셀 ≥ 16 (렌즈 덮어쓰기) · n_M 같음', p['n_pid_diff'] >= 16 and p['n_M'] == R['ref']['n_M'], repr(p)[:300])

    @case
    def o2():
        print('O2 — RINTV-02 브리지 끝자리 (판정문 리터럴) · 순서 [1,0] ↔ [0,1] · vox 0.1 · 브리지 0.24')
        R = D.order_diag_raster(V02_C, V02_R, V02_T, (0.0, 0.0, 0.0), (3.2, 3.2, 3.2), 0.1, 0.24,
                                [np.array([0, 1]), np.array([1, 0])])
        p = R['perms'][0]
        chk('O2 sid 다른 셀 1 = 마스크 전이 1 (AM ↔ 비어 있음) · 자리 bridge · 셀 (15,15,15)',
            p['n_sid_diff'] == 1 and p['n_mask'] == 1 and p['n_label'] == 0 and p['loc']['bridge'] == 1
            and [tuple(x) for x in p['sample_cells']] == [(15, 15, 15)], repr(p)[:400])
        chk('O2 n_M 3170 (기준 [0,1]) ↔ 3171', R['ref']['n_M'] == 3170 and p['n_M'] == 3171, f"{R['ref']['n_M']} {p['n_M']}")

    @case
    def o3():
        print('O3 — 같은 종류 두 구 (AM_S 둘) 겹침 · sid 는 같고 pid 만 바뀐다')
        c = np.array([[1., 1., 1.], [1., 1., 2.9]]); r = np.ones(2); t = np.array([2, 2])
        R = D.order_diag_raster(c, r, t, (0.0, 0.0, 0.0), (2.0, 2.0, 3.9), 0.1, 0.24, [np.array([0, 1]), np.array([1, 0])])
        p = R['perms'][0]
        #  ⚠ 정정 (구현 전 · 10-13): 시험 먼저 커밋은 "pid 차이 = 렌즈뿐" 을 기대했다 — 틀렸다.  같은 종류 쌍의 브리지 pid = soft = (i, j) 의 j
        #    (`rasterize` 브리지 줄) 라 행 순서를 따른다 → 브리지 셀 (구 하나 안) 의 pid 도 바뀐다.  옳은 불변식 = 렌즈 · 브리지 밖 pid 변화 0.
        chk('O3 sid 다른 셀 0 · pid 다른 셀 > 0 (렌즈 덮어쓰기 + 브리지 soft = j) · 렌즈 · 브리지 밖 pid 변화 0',
            p['n_sid_diff'] == 0 and p['n_pid_diff'] > 0 and p['pid_loc']['lens'] > 0 and p['pid_loc']['other'] == 0, repr(p)[:300])

    @case
    def o4():
        print('O4 — 등록된 순서 (K 7 · seed 20261013 … 20261018)')
        P = D.registered_perms(11)
        chk('O4 π₀ = 파일 순서 · π₁ = 역순 · π₂ … π₇ = default_rng(seed).permutation(N) (등록 seed 그대로)',
            len(P) == 8 and np.array_equal(P[0], np.arange(11)) and np.array_equal(P[1], np.arange(11)[::-1])
            and all(np.array_equal(P[2 + k], np.random.default_rng(20261013 + k).permutation(11)) for k in range(6))
            and D.SEEDS == (20261013, 20261014, 20261015, 20261016, 20261017, 20261018) and D.K == 7)

    for fn in cases:
        print(f'\n── {fn.__name__}')
        try:
            if D is None:
                raise ImportError('rint_t43_order_diag 없음')
            fn()
        except Exception as e:                              # noqa: BLE001
            chk(f'{fn.__name__}: 실행', False, f'{type(e).__name__}: {e}')
    print(f'\n{_ok} PASS · {len(_fail)} FAIL')
    if _fail:
        for n in _fail:
            print('  -', n)
        sys.exit(1)


if __name__ == '__main__':
    main()
