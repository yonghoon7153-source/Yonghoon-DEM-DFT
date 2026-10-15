#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rint G2 ①′ — T2 **개발** harness 시험 (T2-1′ mms_linear_jump · T2-4a trace_jump_operator · 반례 먼저 · 2026-10-13).

⚠ 개발 실행 — D12-V 봉인 전 · 검증 PASS 아님 (v3.1 §6-2 · 판정문 §4 · §8).  이 시험이 PASS/FAIL 로 보는 것은 **정확한 층**뿐이다:
  ① 제조해 자체 (조화 · flux 연속 · jump = r·J_n · Codex `mms_sign_check` 재현)
  ② 정확 이산 층 — θ 0 (계면 = 면 평면) · β 0 (각 영역 선형) 이면 FV 해 = 제조해 (반올림 안 · v2 §3-11 "정확 이산 · 기계 정밀도") ·
     막 삭제 · 단위 (×1e4 누락) · jump 부호 반전 변이는 그 층에서 반올림이 아닌 차를 낸다 (판별력)
  ③ harness 가 생산 면 함수 `step3_sigma.interface_face_g` 를 **공유**한다 (v2 §4 · v3 §4-1 — 따로 짜면 같은 법칙을 검증하지 못한다)
  ④ T2-4a 연속 극한 = Codex 값 (1.0796 · 1.2304) — 개발 사다리 숫자는 산출 (docs/data/rint_t2_dev_20261013/) 이지 합격선이 없다
  ⑤ RIMP-01 (Codex 10-14 · 판정문 §2) — 경계 반 셀이 계면을 가로지르면 그 반 셀에도 두 상과 막이 있다 (거리 가중 직렬 + 같은 법칙의
     r_face · 판정문 §2 의 교차 연결 꼴): D6 정확 이산 층 (θ 0 · β 0 · 계면이 경계 반 셀 안 → 반올림 안) · D7 tie 없는 15° n64 ·
     30° n16 · 이동 45° n128 (+ 15° n64 L1) 의 Codex 경계 대조 값 재현 (판정문 §2 표 · 1e−9) · D8 tie · 경계 교차 수 기록.
     ⚠ D7 은 **회귀 판별** (같은 꼴이면 같은 수) — D11 · D12-V 허용치 · 수렴 판정이 아니다 (개발 표지 그대로)
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

    # ═════════════════ RIMP-01 (Codex 10-14 · 판정문 §2) — 경계 반 셀의 상 · 막 교차 ═════════════════
    def shifted(alpha, beta, s1, s2, r_face, theta, off):
        """계면 평면을 법선 방향으로 off µm 옮긴 제조해 — Codex `ShiftMms` 와 같은 꼴 (u → u − off).  harness 의 offset 인자에
        기대지 않는 subclass 라 고치기 전 harness 에서도 돈다 (수치 실패를 기록하려고)."""
        class _S(T2.Mms):
            def uv(self, x, y):
                u, v = T2.Mms.uv(self, x, y)
                return u - off, v
        return _S(alpha, beta, s1, s2, r_face, theta)

    def geom(M, n, L):
        """시험 쪽 독립 기하 — 셀 중심 u · tie 셀 수 (|u| < 1e−12) · 경계 반 셀 교차 수 (셀 중심 ↔ 경계면 중심의 영역이 다름)."""
        h = L / n
        xc = -0.5 * L + (np.arange(n) + 0.5) * h
        X, Y = np.meshgrid(xc, xc, indexing='ij')
        U, _ = M.uv(X, Y)
        n_cross = 0
        half = 0.5 * L
        for ii, jj, fx, fy in ((np.zeros(n, int), np.arange(n), np.full(n, -half), xc),
                               (np.full(n, n - 1), np.arange(n), np.full(n, half), xc),
                               (np.arange(n), np.zeros(n, int), xc, np.full(n, -half)),
                               (np.arange(n), np.full(n, n - 1), xc, np.full(n, half))):
            uf, _ = M.uv(fx, fy)
            n_cross += int(((uf >= 0.0) != (U[ii, jj] >= 0.0)).sum())
        return int((np.abs(U) < 1e-12).sum()), n_cross

    @case
    def d6a_boundary_exact():
        print('D6a — RIMP-01 정확 이산 층: θ 0 · β 0 · 계면이 경계 반 셀 안 (n 16 · L 1.6 · h 0.1 · 계면 x = −0.78 / +0.78) → FV 해 = 제조해')
        for off in (-0.78, 0.78):
            for law in ('L1', 'axis'):
                M = shifted(2.0, 0.0, 2.0, 5.0, 1e-5, 0.0, off)
                tie, nx = geom(M, 16, 1.6)
                out = T2.mms_solve(M, n=16, L=1.6, law=law)
                scale = float(np.abs(out['phi_exact']).max())
                chk(f'D6a 계면 x = {off:+.2f} µm · {law}: 경계 반 셀 교차 {nx} (> 0) · tie 0 · 내부 막 면 0 → FV 해 = 제조해 '
                    f'(최대 오차 ≤ 1e−12 × max|φ|) — 경계 반 셀의 막 · 두 상이 직렬로 들어가야 정확하다',
                    nx == 16 and tie == 0 and out['n_film_faces'] == 0 and out['err_max'] <= 1e-12 * scale,
                    f"err_max {out['err_max']:.3e} · scale {scale:.3e} · 교차 {nx} · 막 면 {out['n_film_faces']}")

    @case
    def d6b_boundary_api():
        print('D6b — RIMP-01 harness 인자: Mms(offset_um) = 위 subclass 와 같은 해 · 교차 수 기록 · 변이 셋이 경계 막에도 걸린다')
        M = T2.Mms(alpha=2.0, beta=0.0, s1=2.0, s2=5.0, r_face=1e-5, theta_deg=0.0, offset_um=-0.78)
        Ms = shifted(2.0, 0.0, 2.0, 5.0, 1e-5, 0.0, -0.78)
        a, b = T2.mms_solve(M, n=16, L=1.6, law='L1'), T2.mms_solve(Ms, n=16, L=1.6, law='L1')
        chk('D6b offset_um 인자 = subclass (u − off) — 오차 · 정답 φ 비트 같음 · 출력에 offset_um',
            a['err_max'] == b['err_max'] and np.array_equal(a['phi_exact'], b['phi_exact']) and a.get('offset_um') == -0.78,
            f"{a['err_max']!r} {b['err_max']!r} {a.get('offset_um')!r}")
        chk('D6b 출력: 경계 반 셀 교차 수 n_bc_cross = 16 (시험 쪽 독립 기하와 같음) · tie_count 0 · 경계 규칙 이름',
            a.get('n_bc_cross') == geom(M, 16, 1.6)[1] == 16 and a.get('tie_count') == 0
            and 'crossing' in str(a.get('boundary_rule', '')), repr({k: a.get(k) for k in ('n_bc_cross', 'tie_count', 'boundary_rule')}))
        scale = float(np.abs(a['phi_exact']).max())
        bad = {mut: T2.mms_solve(M, n=16, L=1.6, law='L1', mutant=mut)['err_max']
               for mut in ('film_deleted', 'unit_1e4_missing', 'jump_sign_flipped')}
        chk('D6b 판별력: 경계 막뿐인 배치에서도 변이 셋 (막 삭제 · ×1e4 누락 · jump 부호) 이 반올림 아닌 차 (> 1e6 × 정답 · > 1e−6 × max|φ|)',
            all(e > 1e6 * max(a['err_max'], 1e-300) and e > 1e-6 * scale for e in bad.values()), repr(bad))
        z = T2.mms_solve(T2.Mms(alpha=2.0, beta=0.0, s1=2.0, s2=5.0, r_face=1e-5, theta_deg=0.0), n=16, L=1.6, law='L1')
        chk('D6b offset 0 (기본) = 옛 배치 — 교차 0 · 정확 이산 (D3 와 같은 층)',
            z.get('n_bc_cross') == 0 and z['err_max'] <= 1e-12 * float(np.abs(z['phi_exact']).max()), repr(z.get('n_bc_cross')))

    #  판정문 §2 표 (Codex `rrm_probe.py` boundary_control · 경계 교차 연결 대조) — 같은 꼴이면 같은 수 (회귀 · 개발 표지 · 허용치 아님)
    D7_CODEX = ((15.0, 64, 'axis', 0.0, 0.0004495112904, 0.006475555385),
                (30.0, 16, 'axis', 0.0, 0.003087791839, 0.01633704071),
                (45.0, 128, 'axis', 0.001, 0.0009823643239, 0.004030350534),
                (15.0, 64, 'L1', 0.0, 0.001406042364, 0.02030409571))

    @case
    def d7_tilt_regression():
        print('D7 — RIMP-01 회귀: tie 없는 15° n64 · 30° n16 · 이동 45° n128 (+ 15° n64 L1) — Codex 경계 대조 값 (판정문 §2 표) 재현')
        for th, n, law, off, l2_c, mx_c in D7_CODEX:
            M = shifted(2.0, 3.0, 2.0, 5.0, 1e-5, th, off) if off else T2.Mms(2.0, 3.0, 2.0, 5.0, 1e-5, th)
            tie, nx = geom(M, n, 1.6)
            out = T2.mms_solve(M, n, 1.6, law)
            ok = (tie == 0 and nx > 0 and abs(out['err_l2'] / l2_c - 1.0) < 1e-9 and abs(out['err_max'] / mx_c - 1.0) < 1e-9)
            chk(f'D7 θ {th:g}° n {n} {law} 이동 {off:g} µm: tie 0 · 경계 교차 {nx} > 0 · L2 {l2_c:.10g} · 최대 {mx_c:.10g} (Codex 대조 · 상대 1e−9) '
                f'— 회귀 판별 (D11 · D12-V 근거 아님)', ok,
                f"tie {tie} · 교차 {nx} · L2 {out['err_l2']:.10g} · 최대 {out['err_max']:.10g}")

    @case
    def d8_tie_record():
        print('D8 — tie · 경계 교차 수 기록 (45° n128 원점 대칭 = 셀 중심이 계면 위인 셀 n 개 — 배정은 부동소수 반올림에 걸린다 · 플랫폼 의존)')
        M = T2.Mms(2.0, 3.0, 2.0, 5.0, 1e-5, 45.0)
        out = T2.mms_solve(M, 128, 1.6, 'axis')
        tie, nx = geom(M, 128, 1.6)
        chk('D8 45° n128: tie_count = 128 (시험 쪽 독립 셈과 같음) · n_bc_cross = 독립 셈', out.get('tie_count') == tie == 128
            and out.get('n_bc_cross') == nx, repr({k: out.get(k) for k in ('tie_count', 'n_bc_cross')}) + f' · 독립 {tie} {nx}')

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
