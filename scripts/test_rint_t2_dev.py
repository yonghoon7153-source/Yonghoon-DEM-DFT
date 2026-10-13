#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rint G2 ①′ — T2 **개발** harness 시험 (T2-1′ mms_linear_jump · T2-4a trace_jump_operator · 반례 먼저 · 2026-10-13).

⚠ 개발 실행 — D12-V 봉인 전 · 검증 PASS 아님 (v3.1 §6-2 · 판정문 §4 · §8).  이 시험이 PASS/FAIL 로 보는 것은 **정확한 층**뿐이다:
  ① 제조해 자체 (조화 · flux 연속 · jump = r·J_n · Codex `mms_sign_check` 재현)
  ② 정확 이산 층 — θ 0 (계면 = 면 평면) · β 0 (각 영역 선형) 이면 FV 해 = 제조해 (반올림 안 · v2 §3-11 "정확 이산 · 기계 정밀도") ·
     막 삭제 · 단위 (×1e4 누락) · jump 부호 반전 변이는 그 층에서 반올림이 아닌 차를 낸다 (판별력)
  ③ harness 가 생산 면 함수 `step3_sigma.interface_face_g` 를 **공유**한다 (v2 §4 · v3 §4-1 — 따로 짜면 같은 법칙을 검증하지 못한다)
  ④ T2-4a 연속 극한 = Codex 값 (1.0796 · 1.2304) — 개발 사다리 숫자는 산출 (docs/data/rint_t2_dev_20261013/) 이지 합격선이 없다
수렴 차수 · L1 ↔ 축별 (D11) · 허용치 = D12-V (1저자) — 여기서 정하지 않는다.

  python3 scripts/test_rint_t2_dev.py
"""
import math
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


def main():
    try:
        import rint_t2_dev as T2
        import step3_sigma as S3
    except Exception as e:                                  # noqa: BLE001 — 고치기 전 (모듈 없음) 도 사례 단위로 기록
        print(f'  (rint_t2_dev import 실패: {type(e).__name__}: {e})')
        T2 = S3 = None
    cases = []

    def case(fn):
        cases.append(fn)
        return fn

    @case
    def d1_sign():
        print('D1 — mms_sign_check (Codex 증거 evidence.json 값)')
        s = T2.mms_sign_check()
        chk('D1 J_n −6.4 · J_n(영역 2) −6.400000000000001 · φ1 − φ2 = −0.64 = r·J_n (Codex 값 그대로)',
            s['normal_flux_1'] == -6.4 and s['normal_flux_2'] == -6.400000000000001
            and s['phi1_minus_phi2'] == -0.6400000000000001 and s['r_times_Jn'] == -0.6400000000000001, repr(s))

    @case
    def d2_fields():
        print('D2 — 제조해 (θ 30° · σ1 2 · σ2 5 · r_face 1e−5 Ω·cm² → r′ = 0.1 µm·cm/S): 조화 · flux 연속 · jump = r′·σ1 ∂φ1/∂u')
        M = T2.Mms(alpha=2.0, beta=3.0, s1=2.0, s2=5.0, r_face=1e-5, theta_deg=30.0)
        rng = np.random.default_rng(1)
        v = rng.uniform(-1, 1, 7)
        ok_c, ok_j = True, True
        for vv in v:
            ok_c &= abs(M.s1 * M.dphi1_du(0.0, vv) - M.s2 * M.dphi2_du(0.0, vv)) <= 1e-12
            ok_j &= abs((M.phi1_uv(0.0, vv) - M.phi2_uv(0.0, vv)) - M.rprime * (-M.s1 * M.dphi1_du(0.0, vv))) <= 1e-12
        chk('D2 계면 u = 0 에서 σ1 ∂φ1/∂u = σ2 ∂φ2/∂u (1e−12)', ok_c)
        chk('D2 φ1 − φ2 = r′·J_n (J_n = −σ1 ∂φ1/∂u · r′ = 1e4·r_face — 단위 cm → µm)', ok_j and abs(M.rprime - 0.1) < 1e-15)
        chk('D2 두 영역 모두 조화 (쌍선형 — ∂²/∂u² + ∂²/∂v² = 0 · 해석)', M.is_harmonic())

    @case
    def d3_exact():
        print('D3 — 정확 이산 층: θ 0 · 계면 = 면 평면 · β 0 · σ1 ≠ σ2 · 막 r → FV 해 = 제조해 (반올림 안)')
        M = T2.Mms(alpha=2.0, beta=0.0, s1=2.0, s2=5.0, r_face=1e-5, theta_deg=0.0)
        out = T2.mms_solve(M, n=16, L=1.6, law='L1')
        scale = float(np.abs(out['phi_exact']).max())
        chk('D3 FV 해 = 제조해 (최대 오차 ≤ 1e−12 × 최대 |φ|) · 막 면 > 0',
            out['err_max'] <= 1e-12 * scale and out['n_film_faces'] > 0, f"{out['err_max']:.3e} {scale:.3e}")
        bad = {}
        for mut in ('film_deleted', 'unit_1e4_missing', 'jump_sign_flipped'):
            bad[mut] = T2.mms_solve(M, n=16, L=1.6, law='L1', mutant=mut)['err_max']
        chk('D3 판별력: 변이 셋 (막 삭제 · ×1e4 누락 · jump 부호 반전) 은 반올림이 아닌 차 (> 1e6 × 정답 오차 · > 1e−6 × 최대 |φ|)',
            all(e > 1e6 * max(out['err_max'], 1e-300) and e > 1e-6 * scale for e in bad.values()), repr(bad))
        chk('D3 축별 법칙도 θ 0 에서 같은 해 (두 법칙이 축 정렬 면에서 같다)',
            T2.mms_solve(M, n=16, L=1.6, law='axis')['err_max'] <= 1e-12 * scale)

    @case
    def d4_shared():
        print('D4 — harness 가 생산 면 함수 interface_face_g 를 공유한다')
        n_calls = [0]
        orig = S3.interface_face_g

        def spy(*a, **k):
            n_calls[0] += 1
            return orig(*a, **k)
        S3.interface_face_g = spy
        try:
            T2.mms_solve(T2.Mms(alpha=1.0, beta=1.0, s1=1.0, s2=3.0, r_face=1e-5, theta_deg=15.0), n=8, L=1.0, law='L1')
        finally:
            S3.interface_face_g = orig
        chk('D4 mms_solve 가 step3_sigma.interface_face_g 를 부른다 (호출 > 0)', n_calls[0] > 0, repr(n_calls))

    @case
    def d5_trace():
        print('D5 — T2-4a 연속 극한 (Codex support_smearing_continuum) · 개발 표지')
        a = math.sqrt(1.0 - 0.99 ** 2)
        chk('D5 RRM 연속 = 1 + β²a²/4 = 1.0796000000000001 · CNC (b 0.24) = 1.2304 (Codex 값 그대로)',
            T2.trace_energy_factor(a, 4.0) == 1.0796000000000001 and T2.trace_energy_factor(0.24, 4.0) == 1.2304)
        L_ = T2.trace_ladder(a, 0.24, 4.0, [0.05, 0.025], center=(0.013, 0.007))
        chk('D5 사다리 산출에 개발 표지 (D12-V 봉인 전 · 검증 PASS 아님) · RRM · CNC 값',
            'D12-V' in L_['label'] and 'PASS 아님' in L_['label'] and len(L_['rows']) == 2
            and all('rrm' in r_ and 'cnc' in r_ for r_ in L_['rows']), repr(L_)[:300])

    for fn in cases:
        print(f'\n── {fn.__name__}')
        try:
            if T2 is None:
                raise ImportError('rint_t2_dev 없음')
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
