#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""STEP3 수렴 증서 ⓓ (목표량 증서) + 해 상태 분리 — 시험 먼저 (규율 ② · 2026-10-21 · Codex RCA-07 · RCA-13 · 1저자 Q5 (가) ·
Q7 일부).

ⓓ = ΔV = 1 에서 단자 전도도 G* 를 두 원리로 감싼다 (근사 φ 하나로):
  상한  U = Σ g (Δφ)²                                 (Dirichlet 원리 — 어떤 φ 의 에너지도 G* 이상)
  하한  (F − D)² / W                                  (Thomson 원리 — 해의 간선 전류에서 내부 KCL 결손을 신장 트리로 지운 흐름 ·
                                                       W = Σ q²/g · F = 판 흐름 · D = 남은 결손 (부동소수) 의 보수 상한)
  게시 G (= 아래 판 전류 I_bot) 가 |G − G*| ≤ 1e-4 · G 를 **보장**할 때만 통과 = 구간 폭 ≤ 1e-4 · G 이고 두 끝까지 거리 ≤ 1e-4 · G.
  A/B/C 는 경험적 검사로 그대로 (값 · 판정 바이트 같음 — T12).
해 상태 (RCA-13): POSITIVE_SOLVED (증서 필요) · VALID_ZERO_TOPOLOGY (조립 그래프에 두 판을 잇는 성분 없음 = σ 0 이 정상 결과) ·
  ELECTRODE_SHORT · NOT_CERTIFIABLE (그 밖 — 증서 실패가 아니라 증서를 세울 수 없는 해).

반례 (판정문 §3 · 증거 `docs/reviews/codex_rint2_carbon_design_review_evidence_20261021/geometry/convergence_probes.py`):
  주 (11 자유도 · 첫 CG 10 회) · 연결 보조 (7 자유도 · 모든 노드가 관통 성분) · 23 반복 (24 자유도) — 실제 생산 `_solve_cg` 가 만든 해.
  ⚠ 합성 고대비 망 (6.6e11 · 5.1e14) — 실침대 오차 크기 주장 아님.
엄밀성 · 환경 (★ 10-21 · 1저자 "더 꼼꼼하게"):
  T7h 검사 전 정규화 (숫자 글자 · bool 을 float 로 바꿔 계산) · 넘침 → NOT_CERTIFIABLE (예외 아님)
  T7u 밑넘침 (부정규 g · 곱이 0 으로) → NOT_CERTIFIABLE (상대 반올림 모형 밖) · 작지만 정상 범위 (1e-290) 는 통과
  T15 원장 허용 = 반올림 수준만 (중복 합 순서 비대칭 · 큰 차수 행 합 반올림 · b 합 순서는 받고 · 참 비대칭 · 참 접지 · 참 b 불일치는 거부)
  T16 손계산 회로 (정확 분수 G* — 직렬 · 병렬 · 고리 · 막다른 노드 · 대비 1e12 · 1e15 · 다리 · 영값 · R_j = ∞ · 무작위 200)
  T17 반올림 순서 (노드 순열) · OpenBLAS 경로 6 꼴 (Haswell · SkylakeX × 스레드 1 · 4 · Sandybridge · Nehalem · 자식 프로세스) —
      분명한 사례 = 결론 같음 · 칼날 (실제 오차 ≈ τ · 봉인 표 접합 rtol 1e-10 행) = 통과하면 실제 오차 ≤ τ
  T18 변이 표 (증서 · 계약 한 줄 · 기준선에서 통과한 단언이 변이에서 실패해야 적발 · 빠른 판 = 변이 자리 존재만)
  T19 칼날 (정확 분수 판정 = 보수)
  T20 묶음 합 `_fsum_bound` (2²⁰ 넘는 배열 = 생산 침대의 길 · 묶음 사이 상쇄) 오차 상한 · 합 넘침 = (inf, inf)
증서 ↔ 런 결합 (★ 10-21 사전 리뷰 PRE-impl-07 · 1저자 "권고대로 해"):
  T21 증서의 격자 · 계획 지문 ↔ 매니페스트 정본 지문 칸 (생산 배선 함수가 만든 것) — 지문만 바꾼 영값 증서 (판정문 반례) · 다른 침대의
      영값 증서 · 같은 σ 의 다른 침대 (거울) · 다른 접합 계획 (cut ↔ fused) · 다른 face_alpha 계획 (PTFE 자리) · 채널 맞바꿈 · 지문 칸
      없는 매니페스트 = 거부 · 정당한 짝 = 받는다 · 두 인자 호출 = TypeError
  T22 실제 payload (face_alpha + 접합 + rtol · LEAN 3) 끝-끝 — 정당한 런 통과 · 같은 σ 의 다른 계획 런 증서 = 거부
  T23 기반 (a76f59d0d) 대조 — 증서 끔 = 결과 같음 · 증서 켬 = 기반 칸 그대로 · 더해진 칸 = 결합 칸뿐
합산 넘침 (★ 10-23 · Codex 재검토 RCA2-08 · 1저자 10-23 Q1–Q8 권고대로):
  T24 유한 중간값의 최종 합 (U · W fsum) · 원장 행 허용 · 판 전류 합 넘침 → 예외 · 경고 대신 NOT_CERTIFIABLE (판정문 5 노드 8e307 꼴 ·
      U 만 · W 만 · 숨은 접지 + 허용 넘침) · 정상 회로 증서 = 기반 (49a1af626) 과 비트 같음
빠른 판 (기본 · 게이트) ↔ 긴 판 (`--long` · 따로): 긴 판만 = T5 표본 1,500 (빠른 300) · T16 무작위 200 (빠른 40) · T17 순열 20
  (빠른 3) + 탐침 순열 (T17b) + OpenBLAS 경로 자식 여섯 (T17c) · T4 접합 탐침 · T14 시간 (간선 > 2²⁰ 계) · T18 변이 표.

  python3 scripts/test_step3_target_cert.py               # 빠른 판 (게이트)
  python3 scripts/test_step3_target_cert.py --long        # 긴 판 (자식 프로세스 넷 · 변이 표 — 따로 · nice)
  python3 scripts/test_step3_target_cert.py --only T1,T13 # 시험 번호 (첫 낱말 정확히)
"""
import argparse
import contextlib
import importlib.util
import io
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile
import time

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, 'scripts')
sys.path.insert(0, SCRIPTS)
BASE_COMMIT = '47d23baba'                 # 이 수정의 기반 (Z3 합친 메인) — 끈 경로 비트 대조 · A/B/C 값 대조
BIND_BASE = 'a76f59d0d'                   # ★ 10-21 증서 ↔ 런 결합 (PRE-impl-07) 의 기반 — T23 끈 경로 · 새 칸 대조

S3 = CC = RC = None
ARGS = None
_ok, _fail = 0, []
CASES = []
_MUTE = []                      # 변이 모드 (T18) — chk 결과를 여기 모으고 전역 집계 · 출력에 넣지 않는다


def chk(name, cond, why=''):
    global _ok
    cond = bool(cond)
    if _MUTE:
        _MUTE[-1].append((name, cond))
        return cond
    if cond:
        _ok += 1
        print(f'  PASS  {name}')
    else:
        _fail.append(name)
        print(f'  FAIL  {name}' + (f'  ({why})' if why != '' else ''))
    return cond


def case(tag, long_only=False):
    """시험 단위 등록 — long_only = 긴 판 (`--long`) 에서만 돈다 (게이트 = 빠른 판 · 메인 10-21)."""
    def deco(fn):
        CASES.append((tag, fn, long_only))
        return fn
    return deco


def quiet(fn, *a, **k):
    with contextlib.redirect_stdout(io.StringIO()):
        return fn(*a, **k)


@contextlib.contextmanager
def s3_knobs(**kw):
    """S3 모듈 전역을 잠시 바꾼다 (CONV_CERT · CG_RTOL · CG_MAXITER · GPU_SOLVE · AMG_SOLVE) — 끝나면 되돌린다."""
    old = {k: getattr(S3, k) for k in kw}
    try:
        for k, v in kw.items():
            setattr(S3, k, v)
        yield
    finally:
        for k, v in old.items():
            setattr(S3, k, v)


def _resolve(L, b, x0, rt):
    return S3._solve_cg(L, b, x0=x0, rtol=rt)


def _fin(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)


# ═════════════════════════ 반례 (판정문 §3 · Codex convergence_probes.py 고정값 그대로) ═════════════════════════
def codex_chain(which):
    """양의 저항 직렬 + 아래 판 막다른 노드 (연결 보조 = 그 노드를 첫 직렬 노드에 약하게 잇는다) → (L, b, Ab, gb, At, gt, G*).
    G* = 정확 직렬 공식 1/Σ(1/g) (직접해 기준 아님)."""
    from scipy.sparse import csr_matrix
    k = np.array([0.03542843081279895, 21.113990671509995, 0.20370714955448593, 0.000808971961390796, 0.06976120349186236,
                  1.6912757790891766, 0.021238765753829096, 0.0007609288395839504, 0.20701635367585214,
                  0.004052240218237343, 31752.40122359974, 0.00015528936294781815, 2.8720471611538324e-05,
                  0.33794145566284794, 0.035436507440546515, 5.089363857396167, 0.0020462968348843712, 4.924555717512331,
                  0.10125977682414762, 1.3150225184986553, 1.1619900367249028, 9.217092548952976e-05,
                  3.113347553856885e-05, 225.4217993099028])
    G = 6507979.172281959
    bridge = None
    if which == 'main':
        k = np.array([3.9749047010591427, 0.006535081136400995, 0.003293084534476289, 22992.948551542082,
                      0.00035278660732561336, 0.0004798389751913557, 1339.2933113393337, 70807.2008252101,
                      0.4385075410195556, 3.1577098692370925e-05, 84788.55607773518]) / 16384
        G = 20815016.44294986 / 16384
    elif which == 'connected':
        k = np.array([0.1036251621769631, 77264.71177376187, 115.83302628384007, 188.05389893808805, 15.658598399603378,
                      7.184589096729567e-05, 0.004872796993466964])
        G = 36509171569.75918
        bridge = 0.0009451405762888877 / float(k.min())
        k = k / (2 ** 25)
        G = G / (2 ** 25)
    n = len(k) - 1
    a = np.zeros((n + 1, n + 1))
    b = np.zeros(n + 1)
    a[0, 0] = k[0]
    a[n - 1, n - 1] = k[-1]
    a[n, n] = G
    b[0] = k[0]
    b[n] = G
    for i in range(n - 1):
        a[i, i] += k[i + 1]
        a[i + 1, i + 1] += k[i + 1]
        a[i, i + 1] -= k[i + 1]
        a[i + 1, i] -= k[i + 1]
    eps = 0.0 if bridge is None else float(k.min() * bridge)
    if eps:
        a[n, n] += eps
        a[0, 0] += eps
        a[n, 0] -= eps
        a[0, n] -= eps
    keff = k.copy()
    keff[0] += G * eps / (G + eps)
    return (csr_matrix(a), b, np.array([0, n]), np.array([k[0], G]), np.array([n - 1]), np.array([k[-1]]),
            float(1.0 / np.sum(1.0 / keff)))


CODEX = ('main', 'connected', 'iter23')


def codex_cert(which):
    L, b, Ab, gb, At, gt, Gs = codex_chain(which)
    with s3_knobs(GPU_SOLVE=False, AMG_SOLVE=False, CG_MAXITER=1000):
        phi, info = quiet(S3._solve_cg, L, b, rtol=1e-12)
        resid = float(np.linalg.norm(L @ phi - b) / np.linalg.norm(b))
        c = quiet(CC.certify, L, b, phi, int(info), resid, 1e-12, Ab, gb, At, gt, 1.0, _resolve)
    return c, Gs, (L, b, phi, Ab, gb, At, gt)


@case('T1 Codex 반례 셋 (주 · 연결 보조 · 23 반복) — 실제 생산 CG 해 · ⓓ 실패 · 증서 실패 · 구간이 정확 G* 를 담는다')
def t1():
    for which in CODEX:
        c, Gs, _sys = codex_cert(which)
        rel = c['sigma'] / Gs - 1.0
        print(f'    [{which}] 게시 G 상대 오차 {rel:+.6e} · A {c.get("pass_a")} B {c.get("pass_b")} (불균형 {c.get("imbalance"):.3e}) '
              f'C {c.get("pass_c")} · 경험 검사만이면 {"통과" if (c.get("pass_a") and c.get("pass_b") and c.get("pass_c")) else "실패"}')
        chk(f'T1a [{which}] ⓓ 실패 (pass_d False) · 증서 실패 (ok False) · 상태 POSITIVE_SOLVED',
            c.get('pass_d') is False and c.get('ok') is False and c.get('status') == getattr(CC, 'STATUS_POSITIVE', '?'),
            {k: c.get(k) for k in ('pass_d', 'ok', 'status')})
        lo, hi = c.get('target_lo'), c.get('target_hi')
        chk(f'T1b [{which}] 구간 [하한, 상한] 이 정확 직렬 G* 를 담는다 (Dirichlet · Thomson)',
            _fin(lo) and _fin(hi) and 0.0 < lo <= Gs <= hi, (lo, Gs, hi))
        eb = c.get('target_err_bound_rel')
        true_g = abs(c['sigma'] - Gs) / abs(c['sigma'])           # 게시 G 기준 실제 상대 오차 (보장 오차 상한과 같은 분모)
        chk(f'T1c [{which}] 게시 G 의 보장 오차 상한 > 1e-4 · ≥ 실제 오차 {true_g:.3e} · 구간 폭은 그보다 훨씬 작다',
            _fin(eb) and eb > getattr(CC, 'CERT_TARGET_TOL', 1e-4) and eb >= true_g * (1 - 1e-9)
            and c.get('target_width_rel', math.inf) < eb, (eb, c.get('target_width_rel'), true_g))


@case('T2 Codex 설명용 후보 φ (A/B/C 통과 · G 0.25 ↔ G* 1/3) — ⓓ 실패 · 하한 = 1/3 (KCL 보정 흐름) · 상한 = 0.375')
def t2():
    from scipy.sparse import csr_matrix
    G = 1e15
    L = csr_matrix([[2., -1., 0.], [-1., 2., 0.], [0., 0., G]])
    b = np.array([1., 0., G])
    p = np.array([.75, .25, 1.])
    resid = float(np.linalg.norm(L @ p - b) / np.linalg.norm(b))
    with s3_knobs(GPU_SOLVE=False, AMG_SOLVE=False):
        c = quiet(CC.certify, L, b, p, 0, resid, 1e-12, np.array([0, 2]), np.array([1., G]), np.array([1]), np.array([1.]),
                  1.0, _resolve)
    chk('T2a A/B/C 통과 (경험 검사가 이 후보를 못 잡는다 — 판정문 그대로)', c['pass_a'] and c['pass_b'] and c['pass_c'],
        {k: c.get(k) for k in ('pass_a', 'pass_b', 'pass_c')})
    chk('T2b ⓓ 실패 · 증서 실패', c.get('pass_d') is False and c.get('ok') is False, {k: c.get(k) for k in ('pass_d', 'ok')})
    lo, hi = c.get('target_lo'), c.get('target_hi')
    chk('T2c 하한 = 1/3 (1e-14) · 상한 = 0.375 (1e-14) — 후보 φ 의 에너지 · 보정 흐름의 Thomson 값',
        _fin(lo) and _fin(hi) and abs(lo - 1.0 / 3.0) <= 1e-14 and abs(hi - 0.375) <= 1e-14 and lo <= 1.0 / 3.0, (lo, hi))


@case('T3 Codex 영값 반례 (두 판에 각각 붙은 두 노드 · 정확 KCL · σ 0) — VALID_ZERO_TOPOLOGY · 증서 실패 아님')
def t3():
    from scipy.sparse import diags
    L = diags([1., 1.], format='csr')
    b = np.array([1., 0.])
    p = b.copy()
    with s3_knobs(GPU_SOLVE=False, AMG_SOLVE=False):
        c = quiet(CC.certify, L, b, p, 0, 0.0, 1e-12, np.array([0]), np.array([1.]), np.array([1]), np.array([1.]), 1.0, _resolve)
    chk('T3a 상태 VALID_ZERO_TOPOLOGY · ok True · σ 0 · 출처 = 행렬 그래프',
        c.get('status') == getattr(CC, 'STATUS_ZERO', '?') and c.get('ok') is True and c.get('sigma') == 0.0
        and c.get('zero_source') == 'matrix_graph', {k: c.get(k) for k in ('status', 'ok', 'sigma', 'zero_source')})
    chk('T3b 관통 성분 0 · ⓓ 판정 칸 = 해당 없음 (None)', c.get('target_n_through_components') == 0 and c.get('pass_d') is None,
        {k: c.get(k) for k in ('target_n_through_components', 'pass_d')})
    p2 = np.array([1.0 - 2.0 ** -40, 0.0])
    with s3_knobs(GPU_SOLVE=False, AMG_SOLVE=False):
        c2 = quiet(CC.certify, L, b, p2, 0, 0.0, 1e-12, np.array([0]), np.array([1.]), np.array([1]), np.array([1.]), 1.0,
                   _resolve)
    chk('T3c 영값 위상인데 게시 G ≠ 0 (근사 φ) → ok False (CG 오차를 0 으로 둔갑시키지 않는다)',
        c2.get('status') == getattr(CC, 'STATUS_ZERO', '?') and c2.get('ok') is False and c2.get('sigma') != 0.0,
        {k: c2.get(k) for k in ('status', 'ok', 'sigma')})


def _exact2():
    from scipy import sparse
    from scipy.sparse.linalg import spsolve
    L = sparse.csr_matrix(np.array([[3.0, -1.0], [-1.0, 3.0]]))
    b = np.array([2.0, 0.0])
    return L, b, spsolve(L.tocsc(), b), np.array([0]), np.array([2.0]), np.array([1]), np.array([2.0])


def rand_bed(shape, seed, frac_am=0.7):
    rng = np.random.default_rng(seed)
    return np.where(rng.random(shape) < frac_am, rng.integers(1, 3, shape), 3).astype(np.int8)


def te():
    return S3.electronic_sigma_table(0.01, 0.005, 100.0, 10.0, 250.0)


@case('T4 양성 (정상 수렴) — 정확 해 · 무작위 침대 생산 CG · 봉인 탐침 침대 (섬유 · 긴 판은 접합도) rtol 1e-12 → ⓓ 통과')
def t4():
    L, b, phi, Ab, gb, At, gt = _exact2()
    c = quiet(CC.certify, L, b, phi, 0, 0.0, 1e-12, Ab, gb, At, gt, 1.0, lambda L_, b_, x0, rt: (phi, 0))
    chk('T4a 두 셀 직렬 정확 해 → POSITIVE_SOLVED · ⓓ 통과 · ok · 구간 ∋ 0.5 · 폭 ≤ 1e-12',
        c.get('status') == getattr(CC, 'STATUS_POSITIVE', '?') and c.get('pass_d') is True and c.get('ok') is True
        and c.get('target_lo', 1) <= 0.5 <= c.get('target_hi', 0) and c.get('target_width_rel', 1) <= 1e-12,
        {k: c.get(k) for k in ('status', 'pass_d', 'ok', 'target_lo', 'target_hi', 'target_width_rel')})
    sid = rand_bed((6, 6, 12), 3)
    with s3_knobs(CONV_CERT=True, CG_RTOL=1e-12, GPU_SOLVE=False, AMG_SOLVE=False):
        r = quiet(S3.solve_sigma_z, sid, te(), 0.15, z_top_um=12 * 0.15, z_bot_um=0.0)
    cc = r.get('conv_cert') or {}
    chk('T4b 무작위 AM/VGCF 침대 · 생산 CG rtol 1e-12 → POSITIVE_SOLVED · ⓓ 통과 · ok · 미수렴 아님',
        cc.get('status') == getattr(CC, 'STATUS_POSITIVE', '?') and cc.get('pass_d') is True and cc.get('ok') is True
        and r['unconverged'] is False, {k: cc.get(k) for k in ('status', 'pass_d', 'ok', 'target_err_bound_rel')})
    sidp = CC.probe_bed(0)
    base = quiet(CC.probe_system, sidp, CC.probe_sigma_table(), s3=S3)
    variants = [('plain', base)]
    if ARGS.long:                                          # 접합 꼴 = 긴 판 (빠른 판 = plain 하나 · 같은 침대)
        variants.append(('junction', quiet(CC.junction_variant, base, sidp)))
    for variant, sysd in variants:
        Lp, bp = sysd['L'], sysd['b']
        rows = {}
        for rt in (1e-8, 1e-12):
            with s3_knobs(GPU_SOLVE=False, AMG_SOLVE=False, CG_MAXITER=400000):
                ph, info = quiet(S3._solve_cg, Lp, bp, rtol=rt)
                rs = float(np.linalg.norm(Lp @ ph - bp) / np.linalg.norm(bp))
                rows[rt] = quiet(CC.certify, Lp, bp, ph, int(info), rs, rt, sysd['Ab'], sysd['gb'], sysd['At'], sysd['gt'], 1.0,
                                 _resolve)
        c12 = rows[1e-12]
        chk(f'T4c [{variant}] 봉인 탐침 침대 (섬유 σ 7,853.98 · AM 0.0041) rtol 1e-12 → ⓓ 통과 · ok',
            c12.get('pass_d') is True and c12.get('ok') is True,
            {k: c12.get(k) for k in ('pass_a', 'pass_b', 'pass_c', 'pass_d', 'target_err_bound_rel', 'target_width_rel')})
        c8 = rows[1e-8]
        chk(f'T4d [{variant}] rtol 1e-8 → ⓓ 실패 (구간이 넓다 = 증명 못 함 · 근사값이 맞아도 게시 못 한다 — 보수 방향)',
            c8.get('pass_d') is False, {k: c8.get(k) for k in ('pass_d', 'target_err_bound_rel', 'target_width_rel')})
        if variant == 'plain':
            chk('T4e [plain rtol 1e-12] 게시 G 는 2 차로 좁은 구간 **밖** (in_bracket False) 인데 보장 오차 ≤ 1e-4 → 통과 '
                '(문자 그대로 "G ∈ 구간" 규칙이면 정상 수렴 해를 거부 — 보장 오차 꼴을 쓴 근거)',
                c12.get('target_in_bracket') is False and c12.get('pass_d') is True
                and c12.get('target_err_bound_rel', 1) <= 1e-4 and c12.get('target_width_rel', 1) < 1e-8,
                {k: c12.get(k) for k in ('target_in_bracket', 'target_err_bound_rel', 'target_width_rel')})


def _search(variant, N, seed=611):
    """Codex search_cg_counterexample.py 생성기 그대로 (양의 직렬 + 아래 판 막다른 노드 · 연결 보조 = 약한 다리) — 생산 CG rtol 1e-12."""
    from scipy.sparse import csr_matrix
    rng = np.random.default_rng(seed)
    out = {'n': 0, 'bad': 0, 'false_d': 0, 'miss': 0, 'pass_d': 0, 'abc_false': 0, 'problem': 0}
    for _s in range(N):
        n = int(rng.integers(6, 26))
        k = 10. ** rng.uniform(-5, 5, n + 1)
        G = 10. ** rng.uniform(6, 17)
        A = np.zeros((n + 1, n + 1))
        b = np.zeros(n + 1)
        b[0] = k[0]
        b[-1] = G
        A[0, 0] += k[0]
        A[n - 1, n - 1] += k[-1]
        A[-1, -1] = G
        for j in range(n - 1):
            A[j, j] += k[j + 1]
            A[j + 1, j + 1] += k[j + 1]
            A[j, j + 1] -= k[j + 1]
            A[j + 1, j] -= k[j + 1]
        eps = float(k.min() * 10. ** rng.uniform(-3, 2)) if variant == 'connected' else 0.0
        if eps:
            A[-1, -1] += eps
            A[0, 0] += eps
            A[-1, 0] -= eps
            A[0, -1] -= eps
        L = csr_matrix(A)
        phi, info = S3._solve_cg(L, b, rtol=1e-12)
        resid = float(np.linalg.norm(L @ phi - b) / np.linalg.norm(b))
        c = CC.certify(L, b, phi, int(info), resid, 1e-12, np.array([0, n]), np.array([k[0], G]), np.array([n - 1]),
                       np.array([k[-1]]), 1.0, _resolve)
        keff = k.copy()
        keff[0] += G * eps / (G + eps)
        true = 1.0 / np.sum(1.0 / keff)
        err = abs(c['sigma'] - true) / true
        out['n'] += 1
        if c.get('status') != getattr(CC, 'STATUS_POSITIVE', '?'):
            out['problem'] += 1
            continue
        lo, hi = c.get('target_lo'), c.get('target_hi')
        if not (_fin(lo) and _fin(hi) and lo <= true <= hi):
            out['miss'] += 1
        out['pass_d'] += c.get('pass_d') is True
        if int(info) == 0 and err > 1e-4:
            out['bad'] += 1
            out['false_d'] += c.get('pass_d') is True or c.get('ok') is True
            out['abc_false'] += bool(c['pass_a'] and c['pass_b'] and c['pass_c'])
    return out


@case('T5 건전성 — Codex 생성기 그대로 (seed 611 · 막다른 / 연결 각 N — 빠른 판 300 · 긴 판 1,500) · ⓓ 거짓 통과 0 · 구간 빗나감 0')
def t5():
    N = int(ARGS.search_n)
    nb, npd = max(20, N // 15), max(10, N // 30)           # 판별력 · 비보수 하한 (N 1,500 → 100 · 50 = 처음 판 그대로)
    with s3_knobs(GPU_SOLVE=False, AMG_SOLVE=False, CG_MAXITER=300):
        for variant in ('deadend', 'connected'):
            t0 = time.time()
            o = quiet(_search, variant, N)
            print(f'    [{variant}] {o} ({time.time() - t0:.1f}s)')
            chk(f'T5a [{variant}] 생산 술어 거짓 수렴 (info 0 · 오차 > 1e-4) 이 많다 = 판별력 있는 표본 (≥ {nb} · N {N})', o['bad'] >= nb, o)
            chk(f'T5b [{variant}] 그 해들 중 ⓓ · 증서 통과 0 (거짓 통과 없음)', o['false_d'] == 0 and o['problem'] == 0, o)
            chk(f'T5c [{variant}] 모든 해에서 구간이 정확 G* 를 담는다 (빗나감 0)', o['miss'] == 0, o)
            chk(f'T5d [{variant}] ⓓ 가 모든 해를 거부하지는 않는다 (통과 ≥ {npd} — 보수만이 아니다)', o['pass_d'] >= npd, o)


@case('T6 q 보존성 · 결손 항 · 트리 보정 — 보정 뒤 KCL 결손 ≪ 원 결손 · F_bot = F_top · 결손 항 없는 순진한 하한은 G* 를 넘는다')
def t6():
    for which in CODEX:
        c, Gs, (L, b, phi, Ab, gb, At, gt) = codex_cert(which)
        raw, dfb = c.get('target_kcl_raw'), c.get('target_kcl_defect_bound')
        fb, ft = c.get('target_flow_bot'), c.get('target_flow_top')
        chk(f'T6a [{which}] 트리 보정 뒤 남은 결손 상한 ≤ 1e-6 × 원 결손 + 1e-12 × F (부동소수 수준)',
            _fin(raw) and _fin(dfb) and _fin(fb) and dfb <= 1e-6 * raw + 1e-12 * abs(fb), (raw, dfb, fb))
        chk(f'T6b [{which}] 보정 흐름의 F_bot = F_top (1e-12 상대)', _fin(fb) and _fin(ft) and abs(fb - ft) <= 1e-12 * abs(fb), (fb, ft))
        nt = CC.target_bracket(L, b, phi, Ab, gb, At, gt, _tree=False)
        chk(f'T6c [{which}] 트리 보정 없이도 하한은 유효 (결손 항 · ≤ G*) 이지만 보정이 구간을 100 배 이상 좁힌다',
            _fin(nt.get('target_lo')) and nt['target_lo'] <= Gs
            and (nt['target_hi'] - nt['target_lo']) >= 100.0 * (c['target_hi'] - c['target_lo']),
            (nt.get('target_lo'), Gs, nt.get('target_hi'), c.get('target_lo'), c.get('target_hi')))
    _c, Gs, (L, b, phi, Ab, gb, At, gt) = codex_cert('iter23')
    naive = CC.target_bracket(L, b, phi, Ab, gb, At, gt, _tree=False, _defect_term=False)
    chk('T6d [iter23] 결손 항 · 보정 둘 다 빼면 하한이 G* 를 넘는다 (변이 적발 — 결손 항이 하한의 유효성 조건)',
        _fin(naive.get('target_lo')) and naive['target_lo'] > Gs, (naive.get('target_lo'), Gs))
    from scipy.sparse import csr_matrix
    L1, b1, p1 = csr_matrix([[2.0]]), np.array([1.0]), np.array([0.0])        # 판–노드–판 (g 1 · 1) · G* 0.5 · 나쁜 φ 0
    one = (np.array([0]), np.array([1.0]), np.array([0]), np.array([1.0]))
    nv = CC.target_bracket(L1, b1, p1, *one, _tree=False, _defect_term=False)
    ok_t = CC.target_bracket(L1, b1, p1, *one)
    ok_n = CC.target_bracket(L1, b1, p1, *one, _tree=False)
    chk('T6e 손 계산 (G* 0.5 · φ 0): 순진한 F²/W = 1 > G* · 결손 항 있는 하한 ≤ 0.5 (트리 · 트리 없음 둘 다)',
        abs(nv.get('target_lo', 0) - 1.0) <= 1e-12 and ok_t.get('target_lo', 1) <= 0.5 and ok_n.get('target_lo', 1) <= 0.5,
        (nv.get('target_lo'), ok_t.get('target_lo'), ok_n.get('target_lo')))


def _cert_of(L, b, phi, Ab, gb, At, gt):
    return quiet(CC.certify, L, b, phi, 0, 0.0, 1e-12, Ab, gb, At, gt, 1.0, lambda L_, b_, x0, rt: (np.asarray(x0), 0))


@case('T7 원장 ↔ 행렬 fail-closed — 접지 항 · b 불일치 · 비대칭 · 양의 비대각 · NaN φ · g ≤ 0 · 번호 밖 · 비정방 → NOT_CERTIFIABLE')
def t7():
    from scipy import sparse
    L, b, phi, Ab, gb, At, gt = _exact2()
    cases = {
        '접지 항 (원장 밖 대각)': (L + sparse.diags([0.1, 0.0]), b, phi, Ab, gb, At, gt),
        'b ≠ 아래 판 결합': (L, b + np.array([0.0, 0.5]), phi, Ab, gb, At, gt),
        '비대칭': (sparse.csr_matrix(np.array([[3.0, -1.0], [-0.9, 2.9]])), b, phi, Ab, gb, At, gt),
        '양의 비대각 (음 컨덕턴스)': (sparse.csr_matrix(np.array([[1.0, 1.0], [1.0, 1.0]])), b, phi, Ab, gb, At, gt),
        'NaN φ': (L, b, np.array([np.nan, 0.25]), Ab, gb, At, gt),
        'gb ≤ 0': (L, b, phi, Ab, np.array([-2.0]), At, gt),
        'Ab 번호 밖': (L, b, phi, np.array([5]), gb, At, gt),
        '비정방 L': (sparse.csr_matrix(np.ones((2, 3))), b, phi, Ab, gb, At, gt),
    }
    for nm, args in cases.items():
        try:
            c = _cert_of(*args)
        except Exception as e:                              # noqa: BLE001 — 예외 = 거부가 아니다 (증서가 상태로 말해야 한다)
            chk(f'T7 [{nm}] → 예외 없이 NOT_CERTIFIABLE', False, f'{type(e).__name__}: {e}')
            continue
        chk(f'T7 [{nm}] → NOT_CERTIFIABLE · ok False · 원장 문제 기록',
            c.get('status') == getattr(CC, 'STATUS_NOT_CERTIFIABLE', '?') and c.get('ok') is False
            and c.get('target_ledger_ok') is False and isinstance(c.get('target_ledger_problem'), str),
            {k: c.get(k) for k in ('status', 'ok', 'target_ledger_ok', 'target_ledger_problem')})
    c0 = _cert_of(L, b, phi, Ab, gb, At, gt)
    chk('T7 대조 — 같은 계 정상 원장 → POSITIVE_SOLVED · 원장 문제 없음', c0.get('status') == getattr(CC, 'STATUS_POSITIVE', '?')
        and c0.get('target_ledger_ok') is True and c0.get('target_ledger_problem') is None, c0.get('target_ledger_problem'))
    #  ★ 사전 공격 리뷰 (CLAUDE.md ②) — 검사 전 정규화 (숫자 글자 · bool 을 float 로 조용히 바꿔 계산) · 넘침 (fsum ±inf 예외)
    hard = {
        'φ 숫자 글자 (\'0.75\')': (L, b, np.array(['0.75', '0.25']), Ab, gb, At, gt),
        'φ bool': (L, b, np.array([True, False]), Ab, gb, At, gt),
        'gb 숫자 글자': (L, b, phi, Ab, np.array(['2.0']), At, gt),
        'b 숫자 글자': (L, np.array(['2.0', '0']), phi, Ab, gb, At, gt),
        'φ 넘침 (±1.7e308 → 흐름 ±inf)': (L, b, np.array([1.7e308, -1.7e308]), Ab, gb, At, gt),
    }
    for nm, args in hard.items():
        try:
            with np.errstate(over='ignore', invalid='ignore'):  # 넘침 경우의 numpy 경고만 끈다 (예외 · 판정은 그대로 본다)
                c = _cert_of(*args)
        except Exception as e:                              # noqa: BLE001
            chk(f'T7h [{nm}] → 예외 없이 NOT_CERTIFIABLE', False, f'{type(e).__name__}: {e}')
            continue
        chk(f'T7h [{nm}] → NOT_CERTIFIABLE · ok False (조용히 바꿔 계산하지 않는다 · 예외 아님)',
            c.get('status') == getattr(CC, 'STATUS_NOT_CERTIFIABLE', '?') and c.get('ok') is False,
            {k: c.get(k) for k in ('status', 'ok', 'target_ledger_problem')})
    #  ★ 사전 공격 리뷰 — 밑넘침 (넘침의 쌍둥이).  상한 · 하한의 여유는 상대 반올림 모형 (|δ| ≤ u) 위에 있다 — 곱이 부정규 범위 (< 2⁻¹⁰²²)
    #  로 떨어지면 절대 오차 (2⁻¹⁰⁷⁵) 가 상대 여유를 넘을 수 있다 → 모형 밖 = NOT_CERTIFIABLE (생산 g ≥ 1e-17 · Δφ ≥ 1e-17 근처라 닿지 않는다)
    from fractions import Fraction as Fr
    for nm, gv, phi_u in (('부정규 g (1e-310 직렬 · 정확 해)', 1e-310, None),
                          ('곱 완전 밑넘침 (g 1e-200 · Δφ 1e-150 → 0)', 1e-200, np.array([1e-150, 0.0]))):
        edges, bot, top = [(0, 1, gv)], [(0, gv)], [(1, gv)]
        Ls, bs, Abs, gbs, Ats, gts = _hand_system(2, edges, bot, top)
        ps = np.array([float(x) for x in _fr_solve(2, edges, bot, top)[0]]) if phi_u is None else phi_u
        cs = _cert_of(Ls, bs, ps, Abs, gbs, Ats, gts)
        chk(f'T7u [{nm}] → NOT_CERTIFIABLE (상대 반올림 모형 밖 · 예외 아님)', cs.get('status') == getattr(CC, 'STATUS_NOT_CERTIFIABLE', '?')
            and cs.get('ok') is False, {k: cs.get(k) for k in ('status', 'ok', 'pass_d', 'target_ledger_problem')})
    edges, bot, top = [(0, 1, 1e-290)], [(0, 1e-290)], [(1, 1e-290)]
    Ls, bs, Abs, gbs, Ats, gts = _hand_system(2, edges, bot, top)
    pfr, Gs = _fr_solve(2, edges, bot, top)
    cs = _cert_of(Ls, bs, np.array([float(x) for x in pfr]), Abs, gbs, Ats, gts)
    chk('T7u 대조 — 작지만 정상 범위 (g 1e-290 · 항 ~1e-291) 정확 해 → POSITIVE_SOLVED · ⓓ 통과 · 구간 ∋ G* (분수) (거짓 거부 없음)',
        cs.get('status') == getattr(CC, 'STATUS_POSITIVE', '?') and cs.get('pass_d') is True and _fin(cs.get('target_lo'))
        and _fin(cs.get('target_hi')) and Fr(cs['target_lo']) <= Gs <= Fr(cs['target_hi']),
        {k: cs.get(k) for k in ('status', 'pass_d', 'target_lo', 'target_hi')} | {'G*': float(Gs)})


@case('T15 원장 허용 = 반올림 수준만 — 중복 합 순서가 다른 비대칭 (1e16 + 1 × 40) · 큰 차수 행 합 반올림 (1e16 + 1 × 200 이 대각에서 사라짐) '
      '· b 합 순서 (판 간선 301 개) = 받는다 (거짓 거부 없음) · 참 비대칭 · 참 접지 · 참 b 불일치는 그대로 거부')
def t15():
    from scipy import sparse
    from scipy.sparse.linalg import spsolve
    big = 1e16
    #  병렬 41 간선 (1e16 + 1 × 40) 을 두 방향에서 다른 순서로 더한 결과 그대로: (0,1) = 1e16 먼저 → 1 들이 묻혀 −1e16 ·
    #  (1,0) = 1 들 먼저 → −(1e16 + 40).  (scipy 의 중복 합 순서에 기대지 않고 CSR 배열을 직접 쓴다 — 결정적)
    L = sparse.csr_matrix((np.array([big + 42.0, -big, -(big + 40.0), big + 42.0]), np.array([0, 1, 0, 1]), np.array([0, 2, 4])),
                          shape=(2, 2))
    asym = abs(L[0, 1] - L[1, 0]) / abs(L[0, 1])
    b = np.array([1.0, 0.0])
    phi = spsolve(L.tocsc(), b)
    c = _cert_of(L, b, phi, np.array([0]), np.array([1.0]), np.array([1]), np.array([1.0]))
    from fractions import Fraction as Fr
    Gs = 1 / (1 + 1 / Fr(big) + 1)                        # 원장 (위 삼각 g 1e16 · 판 1 · 1) 의 정확 직렬 G* (분수)
    chk(f'T15a 합 순서만 다른 (0,1) ↔ (1,0) (상대 차 {asym:.1e} = 36u · 반올림) → 원장 받음 · POSITIVE_SOLVED · 구간 ∋ 원장 G* (분수)',
        asym > 4 * 2.0 ** -53 and c.get('target_ledger_ok') is True and c.get('status') == getattr(CC, 'STATUS_POSITIVE', '?')
        and _fin(c.get('target_lo')) and _fin(c.get('target_hi')) and Fr(c['target_lo']) <= Gs <= Fr(c['target_hi']),
        (asym, c.get('target_ledger_problem'), c.get('status'), c.get('target_lo'), c.get('target_hi')))
    n_dead = 200                                          # 노드 0: 위로 1e16 · 막다른 노드 200 개 (각 g 1 · 아래 판 g 1)
    diag0 = 0.0
    for x in [big] + [1.0] * n_dead:                       # 생산 조립처럼 앞에서부터 더한다 — 1 들이 1e16 에 묻혀 사라진다
        diag0 += x
    diag0 += 1.0                                          # 노드 0 의 아래 판 결합
    nn = 2 + n_dead
    rr, cc_, vv = [0, 1], [1, 0], [-big, -big]
    for j in range(2, nn):
        rr += [0, j]
        cc_ += [j, 0]
        vv += [-1.0, -1.0]
    rr += list(range(nn))
    cc_ += list(range(nn))
    vv += [diag0, big + 1.0] + [2.0] * n_dead
    L2 = sparse.coo_matrix((vv, (rr, cc_)), shape=(nn, nn)).tocsr()
    Ab2 = np.r_[0, np.arange(2, nn)].astype(np.int64)
    gb2 = np.ones(len(Ab2))
    b2 = np.bincount(Ab2, gb2, nn)
    p2 = spsolve(L2.tocsc(), b2)
    lost = (big + n_dead + 1.0) - diag0
    c2 = _cert_of(L2, b2, p2, Ab2, gb2, np.array([1]), np.array([1.0]))
    G2 = 1 / (1 / (1 + Fr(n_dead, 2)) + 1 / Fr(big) + 1)  # 원장 G* (분수): 아래 판 → 노드 0 = 직접 1 + 200 길 (각 1/2) · 1e16 · 위 판 1
    chk(f'T15b 차수 201 행 — 대각 반올림으로 {lost:.0f} 이 사라진 행 합 (반올림 · 64u 고정 허용 밖) → 원장 받음 · POSITIVE_SOLVED · '
        f'구간 ∋ 원장 G* (분수 · 이 φ 는 반올림된 행렬의 해라 원장 망의 해가 아니다 — 판정은 ⓓ 가 한다 · 건전성만 본다)',
        lost >= n_dead and c2.get('target_ledger_ok') is True and c2.get('status') == getattr(CC, 'STATUS_POSITIVE', '?')
        and _fin(c2.get('target_lo')) and _fin(c2.get('target_hi')) and Fr(c2['target_lo']) <= G2 <= Fr(c2['target_hi']),
        (lost, c2.get('target_ledger_problem'), c2.get('status'), c2.get('target_lo'), float(G2), c2.get('target_hi')))
    L3 = L.tolil()
    L3[1, 0] = L[1, 0] * (1 + 1e-9)
    c3 = _cert_of(L3.tocsr(), b, phi, np.array([0]), np.array([1.0]), np.array([1]), np.array([1.0]))
    L4 = (L + sparse.diags([1e-6 * big, 0.0])).tocsr()
    c4 = _cert_of(L4, b, phi, np.array([0]), np.array([1.0]), np.array([1]), np.array([1.0]))
    chk('T15c 대조 — 참 비대칭 (상대 1e-9) · 참 접지 (대각 +1e-6 상대) 는 그대로 NOT_CERTIFIABLE',
        c3.get('status') == getattr(CC, 'STATUS_NOT_CERTIFIABLE', '?') and c4.get('status') == getattr(CC, 'STATUS_NOT_CERTIFIABLE', '?'),
        (c3.get('target_ledger_problem'), c4.get('target_ledger_problem')))
    #  ★ 변이 표가 찾은 것 — T15c 의 비대칭은 행 합 검사도 잡아서 대칭 검사 하나를 가르지 못했다.  행 합을 맞춘 참 비대칭 (원장 = 위 삼각 그대로 ·
    #  행렬만 비대칭 = 솔버가 다른 계를 푼다) 은 대칭 검사만 잡는다.
    L6 = L.tolil()
    d10 = L[1, 0] * 1e-9
    L6[1, 0] = L[1, 0] + d10
    L6[1, 1] = L[1, 1] - d10                              # 행 1 합 그대로 (반올림 안)
    L6 = L6.tocsr()
    c7 = _cert_of(L6, b, phi, np.array([0]), np.array([1.0]), np.array([1]), np.array([1.0]))
    chk('T15f 행 합을 맞춘 참 비대칭 (상대 1e-9) → NOT_CERTIFIABLE · 사유 = 비대칭 (대칭 검사만 잡는 꼴)',
        c7.get('status') == getattr(CC, 'STATUS_NOT_CERTIFIABLE', '?') and '비대칭' in str(c7.get('target_ledger_problem')),
        c7.get('target_ledger_problem'))
    #  b 의 합 순서 — 한 노드에 아래 판 간선 301 개 (1e16 + 1 × 300).  조립이 1 들을 먼저 더하면 b = 1e16 + 300 · 원장 (bincount = 배열
    #  순서 · 1e16 먼저) 은 1e16 → 차 300 (반올림 · 64u 고정 허용 ≈ 142 밖) → 받는다.  참 불일치 (b + 1e-6 상대) 는 거부.
    kb = 300
    gb5 = np.r_[big, np.ones(kb)]
    Ab5 = np.zeros(kb + 1, np.int64)
    b0 = 0.0
    for x in list(np.ones(kb)) + [big]:                    # 1 들 먼저 (생산과 다른 순서)
        b0 += x
    L5 = sparse.csr_matrix(np.array([[b0 + 1.0, -1.0], [-1.0, 2.0]]))   # 노드 0: 판 결합 (b0) + 면 1 · 노드 1: 면 1 + 위 판 1
    b5 = np.array([b0, 0.0])
    p5 = spsolve(L5.tocsc(), b5)
    c5 = _cert_of(L5, b5, p5, Ab5, gb5, np.array([1]), np.array([1.0]))
    bb5 = float(np.bincount(Ab5, gb5, 2)[0])
    G5 = 1 / (1 / (Fr(big) + kb) + 2)                     # 원장 G* (분수 · 판 간선 301 개의 정확 합 1e16 + 300 → 면 1 → 위 판 1)
    chk(f'T15d 한 노드 아래 판 간선 {kb + 1} 개 — b 합 순서만 다름 (b − 원장 = {b0 - bb5:.0f}) → 원장 받음 · POSITIVE_SOLVED · 구간 ∋ G* (분수)',
        abs(b0 - bb5) >= kb - 2 and c5.get('target_ledger_ok') is True and c5.get('status') == getattr(CC, 'STATUS_POSITIVE', '?')
        and _fin(c5.get('target_lo')) and _fin(c5.get('target_hi')) and Fr(c5['target_lo']) <= G5 <= Fr(c5['target_hi']),
        (b0 - bb5, c5.get('target_ledger_problem'), c5.get('status'), c5.get('target_lo'), float(G5), c5.get('target_hi')))
    c6 = _cert_of(L5, b5 * (1 + 1e-6), p5, Ab5, gb5, np.array([1]), np.array([1.0]))
    chk('T15e 대조 — b 참 불일치 (상대 1e-6) 는 그대로 NOT_CERTIFIABLE', c6.get('status') == getattr(CC, 'STATUS_NOT_CERTIFIABLE', '?'),
        c6.get('target_ledger_problem'))


@case('T8 떠 있는 성분 · 병렬 판 간선 · 한 노드 두 판 — 구간 유효 · 정확 해면 통과')
def t8():
    from scipy import sparse
    from scipy.sparse.linalg import spsolve
    L, b, phi, Ab, gb, At, gt = _exact2()
    Lf = sparse.block_diag([L, sparse.csr_matrix(np.array([[1.0, -1.0], [-1.0, 1.0]]))], format='csr')
    bf = np.r_[b, 0.0, 0.0]
    pf = np.r_[phi, 0.5, 0.5]
    c = _cert_of(Lf, bf, pf, Ab, gb, At, gt)
    chk('T8a 판에 안 닿는 성분 둘 (상수 φ) → 떠 있는 노드 2 기록 · ⓓ 통과 · 구간 ∋ 0.5',
        c.get('target_n_floating_nodes') == 2 and c.get('pass_d') is True and c.get('target_lo', 1) <= 0.5 <= c.get('target_hi', 0),
        {k: c.get(k) for k in ('target_n_floating_nodes', 'pass_d', 'target_lo', 'target_hi')})
    Lp = sparse.csr_matrix(np.array([[3.0, -1.0], [-1.0, 3.0]]))          # 노드 0 에 아래 판 간선 둘 (g 1 · 1) + 면 1 · 위 2
    bp = np.array([2.0, 0.0])
    pp = spsolve(Lp.tocsc(), bp)
    Gs = 1.0 / (1.0 / 2.0 + 1.0 + 1.0 / 2.0)
    c2 = _cert_of(Lp, bp, pp, np.array([0, 0]), np.array([1.0, 1.0]), np.array([1]), np.array([2.0]))
    chk('T8b 같은 노드 아래 판 간선 둘 (병렬) → 구간 ∋ G* 0.5 · 통과', c2.get('pass_d') is True
        and c2.get('target_lo', 1) <= Gs <= c2.get('target_hi', 0), {k: c2.get(k) for k in ('pass_d', 'target_lo', 'target_hi')})
    L3 = sparse.csr_matrix(np.array([[2.0]]))
    c3 = _cert_of(L3, np.array([1.0]), np.array([0.5]), np.array([0]), np.array([1.0]), np.array([0]), np.array([1.0]))
    chk('T8c 한 노드가 두 판에 다 붙음 (판–노드–판) → G* 0.5 · 구간 [0.5, 0.5] · 통과', c3.get('pass_d') is True
        and abs(c3.get('target_lo', 0) - 0.5) <= 1e-14 and abs(c3.get('target_hi', 0) - 0.5) <= 1e-14,
        {k: c3.get(k) for k in ('pass_d', 'target_lo', 'target_hi')})


def _grid_system(shape, seed, direct=True):
    """생산 조립 (`solve_sigma_z`) 이 만든 L · b · 판 간선 + 해 (직접해 · 큰 격자는 생산 CG rtol 1e-10) — 계 붙잡기."""
    from scipy.sparse.linalg import spsolve
    sid = rand_bed(shape, seed)
    cap = {}
    old = S3._solve_cg

    def _rec(L, b, *a, **k):
        cap['L'] = L.tocsr()
        cap['b'] = np.asarray(b, np.float64).copy()
        if direct:
            return spsolve(cap['L'].tocsc(), cap['b']), 0
        return old(cap['L'], cap['b'], rtol=1e-10)
    S3._solve_cg = _rec
    try:
        with s3_knobs(GPU_SOLVE=False, AMG_SOLVE=False):
            res = quiet(S3.solve_sigma_z, sid, te(), 0.15, return_field=True, z_top_um=shape[2] * 0.15, z_bot_um=0.0)
    finally:
        S3._solve_cg = old
    cond = res['cond']
    idx = -np.ones(sid.shape, np.int64)
    idx[cond] = np.arange(int(cond.sum()))
    (cb, gb, _), (ct, gt, _) = res['plate_edges']['bot'], res['plate_edges']['top']
    phi = res['phi'][cond]
    return cap['L'], cap['b'], phi, idx[cb[0], cb[1], cb[2]], np.asarray(gb), idx[ct[0], ct[1], ct[2]], np.asarray(gt)


@case('T9 결정성 · 재표지 — 같은 입력 두 번 = 기록 바이트 같음 · 노드 순열 = 같은 구간 (1e-12) · 같은 상태')
def t9():
    from scipy import sparse
    L, b, phi, Ab, gb, At, gt = _grid_system((5, 5, 10), 7)
    r1 = CC.target_bracket(L, b, phi, Ab, gb, At, gt)
    r2 = CC.target_bracket(L, b, phi, Ab, gb, At, gt)
    chk('T9a 같은 입력 두 번 → 기록 JSON 바이트 같음', json.dumps(r1, sort_keys=True) == json.dumps(r2, sort_keys=True))
    n = L.shape[0]
    perm = np.random.default_rng(5).permutation(n)
    inv = np.empty(n, np.int64)
    inv[perm] = np.arange(n)
    P = sparse.csr_matrix((np.ones(n), (np.arange(n), perm)), shape=(n, n))
    Lq = (P @ L @ P.T).tocsr()
    rq = CC.target_bracket(Lq, b[perm], phi[perm], inv[Ab], gb, inv[At], gt)
    chk('T9b 노드 순열 → 구간 같음 (상대 1e-12) · 관통 위상 같음',
        rq.get('target_topology') == r1.get('target_topology') == 'through'
        and abs(rq['target_lo'] - r1['target_lo']) <= 1e-12 * r1['target_lo']
        and abs(rq['target_hi'] - r1['target_hi']) <= 1e-12 * r1['target_hi'],
        (r1.get('target_lo'), rq.get('target_lo'), r1.get('target_hi'), rq.get('target_hi')))


@case('T10 조기 반환 해의 상태 분류 — 영값 위상 (넷) · 단락 · 얇은 침대 · 모르는 사유 · 모순 (영값 사유인데 관통 dof · σ ≠ 0)')
def t10():
    Z, S, N = (getattr(CC, k, '?') for k in ('STATUS_ZERO', 'STATUS_SHORT', 'STATUS_NOT_CERTIFIABLE'))
    table = (('no_through_component', Z), ('all_floating_dropped', Z), ('no_conductive_voxels', Z),
             ('no_plate_contact(bot=0,top=3,z_b=0.00,z_plate=1.50,band=0.25)', Z), ('cjunc_electrode_short', S),
             ('degenerate_thin_bed', N), ('mystery_reason', N), (None, N))
    for reason, want in table:
        rec = CC.early_record({'sigma_eff': 0.0, 'n_dof': 4, 'reason': reason}, zero_graph='cell6', fp_sid='a' * 32, fp_sig='b' * 32)
        chk(f'T10a [{reason}] → {want} · ok = (영값 위상일 때만) · σ 0 · 판 이름 · 출처 early_return',
            rec.get('status') == want and rec.get('ok') is (want == Z) and rec.get('sigma') == 0.0
            and rec.get('version') == CC.CERT_VERSION and rec.get('zero_source') == 'early_return',
            {k: rec.get(k) for k in ('status', 'ok', 'sigma', 'version', 'zero_source')})
    bad1 = CC.early_record({'sigma_eff': 0.0, 'n_dof': 4, 'n_through_dof': 3, 'reason': 'no_through_component'},
                           zero_graph='cell6', fp_sid='a' * 32, fp_sig='b' * 32)
    bad2 = CC.early_record({'sigma_eff': 1e-9, 'n_dof': 4, 'reason': 'no_through_component'}, zero_graph='cell6',
                           fp_sid='a' * 32, fp_sig='b' * 32)
    chk('T10b 모순 (영값 사유인데 관통 dof 3 · σ ≠ 0) → NOT_CERTIFIABLE · ok False',
        bad1.get('status') == N and bad1.get('ok') is False and bad2.get('status') == N and bad2.get('ok') is False,
        (bad1.get('status'), bad2.get('status')))


def _early_beds():
    s_nt = np.zeros((4, 1, 8), np.int8)
    s_nt[0, 0, 0:3] = 3
    s_nt[3, 0, 5:8] = 3
    s_np = np.zeros((3, 3, 10), np.int8)
    s_np[1, 1, 3:7] = 3
    return (('no_through_component', s_nt, {}), ('no_plate_contact', s_np, {}),
            ('no_conductive_voxels', np.zeros((3, 3, 6), np.int8), {}),
            ('degenerate_thin_bed', np.ones((2, 2, 1), np.int8), {'z_top_um': 0.15}))


@case('T11 solve_sigma_z 통합 — 증서 켬: 조기 반환 해에 상태 증서 (영값 위상 · 얇은 침대) · 양의 해에 ⓓ · 증서 끔 = 칸 없음')
def t11():
    Z, N = getattr(CC, 'STATUS_ZERO', '?'), getattr(CC, 'STATUS_NOT_CERTIFIABLE', '?')
    for want_reason, sid, kw in _early_beds():
        args = dict(z_top_um=sid.shape[2] * 0.15, z_bot_um=0.0)
        args.update(kw)
        with s3_knobs(CONV_CERT=True, CG_RTOL=1e-12, GPU_SOLVE=False):
            r = quiet(S3.solve_sigma_z, sid, te(), 0.15, **args)
        with s3_knobs(CONV_CERT=False):
            r0 = quiet(S3.solve_sigma_z, sid, te(), 0.15, **args)
        cc = r.get('conv_cert') or {}
        want = N if want_reason == 'degenerate_thin_bed' else Z
        chk(f'T11a [{want_reason}] 사유 그대로 · 증서 상태 {want} · ok = (영값일 때만) · σ 0 · 지문 hex32 · 증서 끔이면 칸 없음',
            str(r.get('reason', '')).startswith(want_reason) and cc.get('status') == want and cc.get('ok') is (want == Z)
            and cc.get('sigma') == 0.0 and isinstance(cc.get('fp_sid'), str) and len(cc.get('fp_sid')) == 32
            and 'conv_cert' not in r0, ({k: cc.get(k) for k in ('status', 'ok', 'reason', 'zero_graph')}, r.get('reason')))
    sid = rand_bed((5, 5, 10), 11)
    with s3_knobs(CONV_CERT=True, CG_RTOL=1e-12, GPU_SOLVE=False, AMG_SOLVE=False):
        r = quiet(S3.solve_sigma_z, sid, te(), 0.15, z_top_um=10 * 0.15, z_bot_um=0.0)
    cc = r.get('conv_cert') or {}
    chk('T11b 양의 해 → POSITIVE_SOLVED · ⓓ 칸 (하한 · 상한 · 보장 오차) · 증서 σ = 결과 σ · scale 기록',
        cc.get('status') == getattr(CC, 'STATUS_POSITIVE', '?') and cc.get('pass_d') is True and cc.get('ok') is True
        and _fin(cc.get('target_lo')) and _fin(cc.get('target_hi')) and _fin(cc.get('scale'))
        and abs(cc.get('sigma', 0) - r['sigma_eff']) <= 1e-12 * r['sigma_eff'],
        {k: cc.get(k) for k in ('status', 'pass_d', 'ok', 'target_err_bound_rel', 'scale')})


def _load_base(rel, name, commit=None):
    src = subprocess.run(['git', '-C', ROOT, 'show', f'{commit or BASE_COMMIT}:{rel}'], capture_output=True,
                         check=True).stdout
    d = tempfile.mkdtemp(prefix='tcbase_')
    p = os.path.join(d, name + '.py')
    with open(p, 'wb') as fh:
        fh.write(src)
    spec = importlib.util.spec_from_file_location(name, p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def _same(a, b):
    if isinstance(a, dict) or isinstance(b, dict):
        return isinstance(a, dict) and isinstance(b, dict) and sorted(a) == sorted(b) and all(_same(a[k], b[k]) for k in a)
    if isinstance(a, (list, tuple)) or isinstance(b, (list, tuple)):
        return (type(a) is type(b) and len(a) == len(b) and all(_same(x, y) for x, y in zip(a, b)))
    if isinstance(a, np.ndarray) or isinstance(b, np.ndarray):
        return (isinstance(a, np.ndarray) and isinstance(b, np.ndarray) and a.dtype == b.dtype and a.shape == b.shape
                and a.tobytes() == b.tobytes())
    if isinstance(a, float) and isinstance(b, float) and math.isnan(a) and math.isnan(b):
        return True
    return type(a) is type(b) and a == b


@case('T12 끈 경로 비트 같음 (기반 47d23baba) — 증서 끔 solve 결과 전체 · 증서 켬 A/B/C 칸 값 같음 (경험 검사 그대로)')
def t12():
    S3b = quiet(_load_base, 'scripts/step3_sigma.py', 'step3_sigma_base_tc')
    CCb = quiet(_load_base, 'scripts/step3_conv_cert.py', 'step3_conv_cert_base_tc')
    beds = [('양의 침대', rand_bed((5, 5, 10), 11), {})] + [(nm, s, kw) for nm, s, kw in _early_beds()]
    for nm, sid, kw in beds:
        for how in ('직접', 'CG'):
            outs = []
            for mod in (S3b, S3):
                o = mod._solve_cg
                if how == '직접':
                    from scipy.sparse.linalg import spsolve
                    mod._solve_cg = lambda L, b: (spsolve(L.tocsc(), b), 0)
                try:
                    args = dict(return_field=True, z_top_um=sid.shape[2] * 0.15, z_bot_um=0.0)
                    args.update(kw)
                    outs.append(quiet(mod.solve_sigma_z, sid, te(), 0.15, **args))
                finally:
                    mod._solve_cg = o
            chk(f'T12a [{nm} · {how}] 증서 끔 — 기반 ↔ 새 solve 결과 (키 · 값 · φ 바이트) 같음', _same(outs[0], outs[1]),
                sorted(set(outs[0]) ^ set(outs[1])))
    for which in CODEX + ('warm', 'exact'):
        if which in CODEX:
            L, b, Ab, gb, At, gt, _Gs = codex_chain(which)
            with s3_knobs(GPU_SOLVE=False, AMG_SOLVE=False, CG_MAXITER=1000):
                phi, info = quiet(S3._solve_cg, L, b, rtol=1e-12)
            resid = float(np.linalg.norm(L @ phi - b) / np.linalg.norm(b))
        elif which == 'warm':
            from scipy.sparse import csr_matrix
            L = csr_matrix([[2., -1., 0.], [-1., 2., 0.], [0., 0., 1e15]])
            b, phi, info = np.array([1., 0., 1e15]), np.array([.75, .25, 1.]), 0
            Ab, gb, At, gt = np.array([0, 2]), np.array([1., 1e15]), np.array([1]), np.array([1.])
            resid = float(np.linalg.norm(L @ phi - b) / np.linalg.norm(b))
        else:
            L, b, phi, Ab, gb, At, gt = _exact2()
            info, resid = 0, 0.0
        outs = []
        for mod in (CCb, CC):
            with s3_knobs(GPU_SOLVE=False, AMG_SOLVE=False, CG_MAXITER=1000):
                outs.append(quiet(mod.certify, L, b, phi, int(info), resid, 1e-12, Ab, gb, At, gt, 1.0, _resolve))
        old, new = outs
        #  ok = 논리곱 — 뜻이 바뀐 칸 (ⓓ 포함) 이라 뺀다 · 나머지 기반 칸 (ⓐ ⓑ ⓒ 의 수 · 판정 · 이어 풀기) 은 그대로여야 한다
        diff = [k for k in old if k not in ('version', 'ok') and not _same(old[k], new.get(k))]
        chk(f'T12b [{which}] 증서 켬 — A/B/C 칸 (기반 증서의 모든 칸 · 판 이름 · 논리곱 ok 빼고) 값 같음 (경험 검사 그대로)', not diff, diff)
    sid = rand_bed((5, 5, 10), 11)
    outs = []
    for mod, ccm in ((S3b, CCb), (S3, CC)):
        saved = sys.modules.get('step3_conv_cert')
        sys.modules['step3_conv_cert'] = ccm
        try:
            o = (mod.CONV_CERT, mod.CG_RTOL, mod.GPU_SOLVE, mod.AMG_SOLVE)
            mod.CONV_CERT, mod.CG_RTOL, mod.GPU_SOLVE, mod.AMG_SOLVE = True, 1e-12, False, False
            outs.append(quiet(mod.solve_sigma_z, sid, te(), 0.15, z_top_um=10 * 0.15, z_bot_um=0.0))
        finally:
            mod.CONV_CERT, mod.CG_RTOL, mod.GPU_SOLVE, mod.AMG_SOLVE = o
            if saved is None:
                sys.modules.pop('step3_conv_cert', None)
            else:
                sys.modules['step3_conv_cert'] = saved
    old, new = outs
    rest = [k for k in old if k != 'conv_cert' and not _same(old[k], new.get(k))]
    cdiff = [k for k in old['conv_cert'] if k != 'version' and not _same(old['conv_cert'][k], new['conv_cert'].get(k))]
    chk('T12c 증서 켬 solve — σ · φ · 미수렴 · 반복 수 같음 · 증서의 기반 칸 (판 이름 빼고) 같음 · 새 칸은 더해지기만', not rest and not cdiff
        and set(old['conv_cert']) <= set(new['conv_cert']), (rest, cdiff))


def _real_cert():
    sid = rand_bed((5, 5, 10), 11)
    with s3_knobs(CONV_CERT=True, CG_RTOL=1e-12, GPU_SOLVE=False, AMG_SOLVE=False):
        r = quiet(S3.solve_sigma_z, sid, te(), 0.15, z_top_um=10 * 0.15, z_bot_um=0.0)
    return dict(r['conv_cert']), float(r['sigma_eff'])


def _ccp(cert, sigma, man=None, channel='electronic'):
    """`run_contract.conv_cert_problem` — 결합 판 (★ 10-21 PRE-impl-07 · 매니페스트 · 채널 필수) 과 옛 판 (두 인자 · 결합 없음) 둘 다
    부른다 (시험 먼저 기록용 — 옛 판에서 결합 시험은 '다른 침대 증서를 받는다' 는 옳은 이유로 실패한다).  새 판에서는 늘 넷을 넘긴다."""
    import inspect
    if len(inspect.signature(RC.conv_cert_problem).parameters) >= 3:
        return RC.conv_cert_problem(cert, sigma, man, channel)
    return RC.conv_cert_problem(cert, sigma)


def _man_of_cert(cert, channel='electronic'):
    """증서 자신의 결합 칸으로 맞춘 최소 매니페스트 — 결합이 **아닌** 칸 (ⓐ–ⓓ · 상태 · 영값) 을 보는 시험용 (T13).  결합 시험 (T21) 은
    생산 배선 함수 (`ca_ext_cjunc.payload_prepare` · `ptfe_face_alpha.payload_block`) 가 만든 지문 칸을 쓴다 (사본 아님)."""
    c = cert if isinstance(cert, dict) else {}
    ca = {}
    if c.get('fp_cjunc_registry') is not None or c.get('fp_cjunc_rows') is not None:
        ca['cjunc'] = {'evidence': {'fp': {'sid': c.get('fp_sid'), 'registry': c.get('fp_cjunc_registry'),
                                           'plan_rows': c.get('fp_cjunc_rows')}}}
    if c.get('fp_face_plan') is not None or 'cjunc' not in ca:
        other = 'ionic' if channel == 'electronic' else 'electronic'
        ca['ptfe_face'] = {'evidence': {'fp': {'sid_off': c.get('fp_sid'), f'plan_{channel}': c.get('fp_face_plan'),
                                               f'plan_{other}': None}}}
    return {'ca_ext': ca}


@case('T13 run_contract.conv_cert_problem — ⓓ 를 기록된 수로 다시 판정 · 상태 먼저 분기 · 영값 위상 σ 0 수용 · 나머지 거부')
def t13():
    good, sig = _real_cert()
    mg = _man_of_cert(good)
    chk('T13a 실제 양의 증서 → 문제 없음', _ccp(good, sig, mg) is None, _ccp(good, sig, mg))
    lo, hi, G = good.get('target_lo', 1.0), good.get('target_hi', 1.0), good.get('I_bot', 1.0)
    muts = {
        '판 v1 (ⓓ 없는 옛 증서)': lambda c: {k: v for k, v in dict(c, version='conv-cert-v1').items() if not k.startswith('target_')},
        'ⓓ 칸 빠짐 (판 이름은 새것)': lambda c: {k: v for k, v in c.items() if k not in ('target_lo', 'target_hi')},
        'pass_d 빠짐': lambda c: {k: v for k, v in c.items() if k != 'pass_d'},
        'pass_d 문자열': lambda c: dict(c, pass_d='True'),
        '상태 빠짐': lambda c: {k: v for k, v in c.items() if k != 'status'},
        '모르는 상태': lambda c: dict(c, status='MAYBE'),
        '단락 상태': lambda c: dict(c, status=getattr(CC, 'STATUS_SHORT', 'ELECTRODE_SHORT')),
        '증서 못 세움 상태': lambda c: dict(c, status=getattr(CC, 'STATUS_NOT_CERTIFIABLE', 'NOT_CERTIFIABLE')),
        'ok ↔ pass_d 모순 (pass_d False)': lambda c: dict(c, pass_d=False),
        '구간이 G 에서 멀다 (pass_d 는 True 인 채)': lambda c: dict(c, target_lo=G * (1 - 3e-4), target_hi=G * (1 + 3e-4)),
        '구간 폭 > 1e-4 (G 는 가운데)': lambda c: dict(c, target_lo=G * (1 - 8e-5), target_hi=G * (1 + 8e-5)),
        '하한 > 상한': lambda c: dict(c, target_lo=hi * 1.01, target_hi=lo),
        '하한 0': lambda c: dict(c, target_lo=0.0),
        'NaN 하한': lambda c: dict(c, target_lo=float('nan')),
        'inf 상한': lambda c: dict(c, target_hi=float('inf')),
        'I_bot · scale ≠ σ (구간 ↔ 게시값 결합)': lambda c: dict(c, I_bot=G * (1 + 1e-6)),
        '목표 허용 손으로 (1e-2)': lambda c: dict(c, target_tol=1e-2),
        '부동소수 보수 규칙 판본 다름 (옛 v1 여유)': lambda c: dict(c, target_fp='fsum-bfs-defect-margin-v1'),
        '부동소수 보수 규칙 칸 빠짐': lambda c: {k: v for k, v in c.items() if k != 'target_fp'},
        '원장 실패인데 통과 표지': lambda c: dict(c, target_ledger_ok=False),
        '위상 영인데 POSITIVE': lambda c: dict(c, target_topology='zero'),
    }
    for nm, fn in muts.items():
        chk(f'T13b 거부 [{nm}]', _ccp(fn(dict(good)), sig, mg) is not None)
    zero = CC.early_record({'sigma_eff': 0.0, 'n_dof': 4, 'n_through_dof': 0, 'reason': 'no_through_component'},
                           zero_graph='cell6', fp_sid='a' * 32, fp_sig='b' * 32)
    mz = _man_of_cert(zero)
    chk('T13c 영값 위상 증서 + 결과 σ 0 → 문제 없음 (바닥 극한 σ 0 = 정상 결과 · NOT_COMPUTED 로 멈추지 않는다)',
        _ccp(zero, 0.0, mz) is None, _ccp(zero, 0.0, mz))
    zmut = {
        '결과 σ ≠ 0': (zero, 1e-9),
        '증서 σ ≠ 0': (dict(zero, sigma=1e-12), 0.0),
        '관통 dof > 0': (dict(zero, n_through_dof=2), 0.0),
        '영값 아닌 사유': (dict(zero, reason='degenerate_thin_bed'), 0.0),
        'ok False': (dict(zero, ok=False), 0.0),
        '모르는 출처': (dict(zero, zero_source='guess'), 0.0),
        '판 v1': (dict(zero, version='conv-cert-v1'), 0.0),
        '결과 σ bool': (zero, False),
    }
    for nm, (cz, sg) in zmut.items():
        chk(f'T13d 영값 증서 거부 [{nm}]', _ccp(cz, sg, mz) is not None)
    short = CC.early_record({'sigma_eff': 0.0, 'n_dof': 4, 'reason': 'cjunc_electrode_short'}, zero_graph='cjunc_assembled',
                            fp_sid='a' * 32, fp_sig='b' * 32)
    chk('T13e 단락 증서 → 거부 (게시 가능 상태 아님)', _ccp(short, 0.0, _man_of_cert(short)) is not None)
    chk('T13f 다음 세대 게시 조건 — 영값 위상 팔 (σ 0) 통과 · 증서 없는 팔 거부',
        RC.next_gen_cert_ok({'sigma_e_eff_S_cm': 0.0, 'manifest': mz, 'conv_cert': zero})[0]
        and not RC.next_gen_cert_ok({'sigma_e_eff_S_cm': 0.0, 'manifest': mz})[0])


@case('T14 시간 비용 (기록 · 합격선 없음) — 탐침 침대 41,472 dof · 무작위 격자 393,216 dof (간선 > 2²⁰ = 묶음 합 길)', long_only=True)
def t14():
    sidp = CC.probe_bed(0)
    base = quiet(CC.probe_system, sidp, CC.probe_sigma_table(), s3=S3)
    t0 = time.perf_counter()
    r = CC.target_bracket(base['L'], base['b'], base['phi_direct'], base['Ab'], base['gb'], base['At'], base['gt'])
    t1 = time.perf_counter()
    print(f'    탐침 침대 n {base["L"].shape[0]:,} · nnz {base["L"].nnz:,} · ⓓ {t1 - t0:.3f} s · 트리 층 {r.get("target_tree_levels")}')
    L, b, phi, Ab, gb, At, gt = _grid_system((64, 64, 96), 2, direct=False)
    t0 = time.perf_counter()
    r2 = CC.target_bracket(L, b, phi, Ab, gb, At, gt)
    t1 = time.perf_counter()
    print(f'    무작위 격자 n {L.shape[0]:,} · nnz {L.nnz:,} · 간선 {r2.get("target_n_edges")} · ⓓ {t1 - t0:.3f} s '
          f'({1e6 * (t1 - t0) / L.shape[0]:.2f} µs/dof) · 트리 층 {r2.get("target_tree_levels")}')
    chk('T14 두 계 모두 관통 · 유한 구간 (시간은 기록)', r.get('target_topology') == r2.get('target_topology') == 'through'
        and _fin(r.get('target_lo')) and _fin(r2.get('target_hi')))
    w2 = (r2['target_hi'] - r2['target_lo']) / r2['target_hi'] if _fin(r2.get('target_hi')) and r2['target_hi'] > 0 else math.inf
    chk(f'T14b 간선 > 2²⁰ (묶음 합 길 · 생산 침대 꼴) 계 — 원장 받음 · 0 < 하한 ≤ 상한 · 상대 폭 {w2:.1e} < 1e-6 (생산 CG rtol 1e-10 해)',
        isinstance(r2.get('target_n_edges'), int) and r2['target_n_edges'] > (1 << 20) and r2.get('target_ledger_ok') is True
        and 0.0 < r2.get('target_lo', 0.0) <= r2.get('target_hi', 0.0) and w2 < 1e-6, (r2.get('target_n_edges'), w2))


# ═════════════════════════ T16 손계산 회로 (정확 분수 G*) ═════════════════════════
def _fr_solve(n, edges, bot, top):
    """손 회로 정확 풀이 (분수 가우스 소거) → (φ 분수 목록, G* 분수).  아래 판 φ 1 · 위 판 φ 0 · 간선 = (u, v, g) · 판 = (노드, g) · g = float
    (그 float 의 정확한 값을 분수로 — 원장과 같은 수)."""
    from fractions import Fraction as Fr
    A = [[Fr(0)] * n for _ in range(n)]
    r = [Fr(0)] * n
    for u, v, g in edges:
        g = Fr(g)
        A[u][u] += g
        A[v][v] += g
        A[u][v] -= g
        A[v][u] -= g
    for i, g in bot:
        A[i][i] += Fr(g)
        r[i] += Fr(g)
    for i, g in top:
        A[i][i] += Fr(g)
    M = [row[:] + [r[i]] for i, row in enumerate(A)]
    for col in range(n):
        piv = next(i for i in range(col, n) if M[i][col] != 0)
        M[col], M[piv] = M[piv], M[col]
        p = M[col][col]
        M[col] = [x / p for x in M[col]]
        for i in range(n):
            if i != col and M[i][col] != 0:
                f = M[i][col]
                M[i] = [a - f * b for a, b in zip(M[i], M[col])]
    phi = [M[i][n] for i in range(n)]
    G = sum((Fr(g) * (1 - phi[i]) for i, g in bot), Fr(0))
    return phi, G


def _fr_energy(phi, edges, bot, top):
    """임의 φ (float 목록) 의 정확 에너지 Σ g (Δφ)² (분수) — Dirichlet 원리의 좌변."""
    from fractions import Fraction as Fr
    p = [Fr(x) for x in phi]
    e = sum((Fr(g) * (p[u] - p[v]) ** 2 for u, v, g in edges), Fr(0))
    e += sum((Fr(g) * (1 - p[i]) ** 2 for i, g in bot), Fr(0))
    e += sum((Fr(g) * p[i] ** 2 for i, g in top), Fr(0))
    return e


def _hand_system(n, edges, bot, top):
    from scipy import sparse
    A = np.zeros((n, n))
    b = np.zeros(n)
    for u, v, g in edges:
        A[u, u] += g
        A[v, v] += g
        A[u, v] -= g
        A[v, u] -= g
    for i, g in bot:
        A[i, i] += g
        b[i] += g
    for i, g in top:
        A[i, i] += g
    return (sparse.csr_matrix(A), b, np.array([i for i, _ in bot], np.int64), np.array([g for _, g in bot], np.float64),
            np.array([i for i, _ in top], np.int64), np.array([g for _, g in top], np.float64))


#: 손계산 회로 — (이름, 노드 수, 간선, 아래 판, 위 판, 닫힌꼴 G* (분수 문자열 · 풀이와 대조) 또는 None)
HAND = (
    ('직렬 (2 · 3 · 5)', 2, [(0, 1, 3.0)], [(0, 2.0)], [(1, 5.0)], '30/31'),
    ('병렬 (두 가지 · 판–노드–판 1·1 ‖ 2·6)', 2, [], [(0, 1.0), (1, 2.0)], [(0, 1.0), (1, 6.0)], '2'),
    ('병렬 안 고리 (직접 1 ‖ 2·2 우회)', 3, [(0, 1, 1.0), (0, 2, 2.0), (2, 1, 2.0)], [(0, 1.0)], [(1, 1.0)], '2/5'),
    ('막다른 노드 (판 하나 · 경로 곁가지)', 4, [(0, 1, 3.0), (0, 3, 4.0)], [(0, 2.0), (2, 7.0)], [(1, 5.0)], '30/31'),
    ('대비 1e12 직렬 (1 · 1e12 · 1)', 2, [(0, 1, 1e12)], [(0, 1.0)], [(1, 1.0)], None),
    ('대비 1e15 막다른 판 노드 (Codex 꼴)', 3, [(0, 1, 1.0)], [(0, 1.0), (2, 1e15)], [(1, 1.0)], '1/3'),
    ('대비 1e-12 병렬 가지', 3, [(0, 2, 1e-12), (2, 1, 1e-12), (0, 1, 1.0)], [(0, 1.0)], [(1, 1.0)], None),
    ('다리 (Wheatstone · 전 자유도 한 관통 성분 · 고리)', 2, [(0, 1, 5.0)], [(0, 1.0), (1, 2.0)], [(0, 3.0), (1, 4.0)], None),
    ('연결 막다른 (1e12 판 노드를 1e-6 다리로 경로에)', 3, [(0, 1, 1.0), (2, 0, 1e-6)], [(0, 1.0), (2, 1e12)], [(1, 1.0)], None),
)


@case('T16 손계산 회로 (정확 분수 G*) — 직렬 · 병렬 · 고리 · 막다른 노드 · 대비 1e12 · 1e15 · 다리 (전 자유도 관통) · 정확 영값: '
      '상한 ≥ G* ≥ 하한 (분수 비교) · 망가뜨린 φ 는 거부 · 영값은 VALID_ZERO_TOPOLOGY')
def t16():
    from fractions import Fraction as Fr
    tau = Fr(1, 10 ** 4)
    for nm, n, edges, bot, top, closed in HAND:
        phi_fr, Gs = _fr_solve(n, edges, bot, top)
        if closed is not None:
            chk(f'T16-0 [{nm}] 분수 풀이 = 닫힌꼴 G* {closed}', Gs == Fr(closed), (Gs, closed))
        L, b, Ab, gb, At, gt = _hand_system(n, edges, bot, top)
        phi = np.array([float(x) for x in phi_fr])
        c = _cert_of(L, b, phi, Ab, gb, At, gt)
        lo, hi = c.get('target_lo'), c.get('target_hi')
        ok_num = _fin(lo) and _fin(hi)
        chk(f'T16a [{nm}] 정확 해 → POSITIVE_SOLVED · ⓓ 통과 · 상한 ≥ G* ≥ 하한 (분수) · 구간 상대 폭 ≤ 1e-12',
            c.get('status') == getattr(CC, 'STATUS_POSITIVE', '?') and c.get('pass_d') is True and ok_num
            and Fr(lo) <= Gs <= Fr(hi) and (Fr(hi) - Fr(lo)) <= Fr(1, 10 ** 12) * Gs,
            {k: c.get(k) for k in ('status', 'pass_d', 'target_lo', 'target_hi')} | {'G*': float(Gs)})
        e_fr = _fr_energy(phi, edges, bot, top)
        chk(f'T16b [{nm}] Dirichlet — 정확 에너지 (분수) ≥ G* · 기록 상한 ≥ 정확 에너지 (부동소수 여유가 덮는다)',
            ok_num and e_fr >= Gs and Fr(hi) >= e_fr, (float(e_fr - Gs), float(Fr(hi) - e_fr) if ok_num else None))
        for dl in (1e-3, 1e-13):
            pb = phi.copy()
            pb[0] += dl
            cb = _cert_of(L, b, pb, Ab, gb, At, gt)
            lb, hb = cb.get('target_lo'), cb.get('target_hi')
            sound = _fin(lb) and _fin(hb) and Fr(lb) <= Gs <= Fr(hb) and _fr_energy(pb, edges, bot, top) <= Fr(hb)
            Gp = cb.get('I_bot')
            if dl == 1e-3:
                chk(f'T16c [{nm}] φ 를 망가뜨림 (노드 0 + 1e-3) → ⓓ 거부 · 구간은 여전히 G* 를 담는다 (건전)',
                    cb.get('pass_d') is False and cb.get('ok') is False and sound,
                    {k: cb.get(k) for k in ('pass_d', 'target_why', 'target_lo', 'target_hi')} | {'G*': float(Gs)})
            else:
                exact_ok = _fin(Gp) and abs(Fr(Gp) - Gs) <= tau * Fr(Gp)
                chk(f'T16d [{nm}] 아주 작게 (+1e-13) → 건전 · 통과면 게시 G 의 실제 오차 ≤ 1e-4 (분수)',
                    sound and (cb.get('pass_d') is not True or exact_ok), {k: cb.get(k) for k in ('pass_d', 'target_err_bound_rel')})
    for nm, n, edges, bot, top in (('정확 영값 (두 판 각각 한 노드)', 2, [], [(0, 1.0)], [(1, 1.0)]),
                                   ('바닥 극한 R_j = ∞ (사슬 가운데 접합 없음)', 4, [(0, 1, 1.0), (2, 3, 1.0)], [(0, 1.0)], [(3, 1.0)])):
        phi_fr, Gs = _fr_solve(n, edges, bot, top)
        L, b, Ab, gb, At, gt = _hand_system(n, edges, bot, top)
        phi = np.array([float(x) for x in phi_fr])
        c = _cert_of(L, b, phi, Ab, gb, At, gt)
        chk(f'T16e [{nm}] G* = 0 (분수) · 정확 해 → VALID_ZERO_TOPOLOGY · ok True · 게시 0 · 상한 ≥ 0 = 하한',
            Gs == 0 and c.get('status') == getattr(CC, 'STATUS_ZERO', '?') and c.get('ok') is True and c.get('sigma') == 0.0
            and c.get('target_lo') == 0.0 and _fin(c.get('target_hi')) and c['target_hi'] >= 0.0,
            {k: c.get(k) for k in ('status', 'ok', 'sigma', 'target_lo', 'target_hi')})
        pb = phi.copy()
        pb[0] = 1.0 - 1e-9
        cb = _cert_of(L, b, pb, Ab, gb, At, gt)
        chk(f'T16f [{nm}] 영값 위상인데 φ 를 망가뜨려 게시 전류 ≠ 0 → ok False (영값 위상 그대로 · CG 오차를 0 으로 바꾸지 않는다)',
            cb.get('status') == getattr(CC, 'STATUS_ZERO', '?') and cb.get('ok') is False and cb.get('sigma') != 0.0,
            {k: cb.get(k) for k in ('status', 'ok', 'sigma')})
    rng = np.random.default_rng(161)
    n_case = n_pass = n_bad = 0
    miss = []
    false_pass = []
    under = []                                              # 기록 상한 < 그 φ 의 정확 에너지 (부동소수 여유가 못 덮음)
    for k in range(int(ARGS.circuits_n)):
        n = int(rng.integers(2, 7))
        edges = [(i, i + 1, float(10.0 ** rng.uniform(-6, 6))) for i in range(n - 1)]
        for _ in range(int(rng.integers(0, n + 1))):
            u, v = (int(x) for x in rng.choice(n, 2, replace=False))
            edges.append((min(u, v), max(u, v), float(10.0 ** rng.uniform(-6, 6))))
        bot = [(0, float(10.0 ** rng.uniform(-3, 3)))] + [(int(i), float(10.0 ** rng.uniform(-6, 6)))
                                                          for i in rng.choice(n, int(rng.integers(0, 2)), replace=False)]
        top = [(n - 1, float(10.0 ** rng.uniform(-3, 3)))]
        phi_fr, Gs = _fr_solve(n, edges, bot, top)
        L, b, Ab, gb, At, gt = _hand_system(n, edges, bot, top)
        for dl in (0.0, 10.0 ** rng.uniform(-9, -2)):
            phi = np.array([float(x) for x in phi_fr])
            if dl:
                phi[int(rng.integers(0, n))] += dl
                n_bad += 1
            c = _cert_of(L, b, phi, Ab, gb, At, gt)
            n_case += 1
            lo, hi, Gp = c.get('target_lo'), c.get('target_hi'), c.get('I_bot')
            if not (_fin(lo) and _fin(hi) and Fr(lo) <= Gs <= Fr(hi)):
                miss.append((k, dl, lo, float(Gs), hi))
            if _fin(hi) and Fr(hi) < _fr_energy(phi, edges, bot, top):
                under.append((k, dl, hi, float(_fr_energy(phi, edges, bot, top))))
            if c.get('pass_d') is True:
                n_pass += 1
                if not (_fin(Gp) and abs(Fr(Gp) - Gs) <= tau * Fr(Gp)):
                    false_pass.append((k, dl, Gp, float(Gs)))
    print(f'    무작위 손 회로 {n_case} 해 (망가뜨림 {n_bad}) · ⓓ 통과 {n_pass} · 구간 빗나감 {len(miss)} · 거짓 통과 {len(false_pass)}')
    chk(f'T16g 무작위 손 회로 {int(ARGS.circuits_n)} 개 (노드 2–6 · g 1e-6–1e6 · 정확 해 + 망가뜨린 해) — 구간이 정확 분수 G* 를 다 담는다',
        not miss, miss[:3])
    chk('T16h 같은 표본 — ⓓ 통과한 해의 게시 G 는 정확 분수 G* 와 상대 1e-4 안 (거짓 통과 0) · 통과 ≥ 1 (보수만이 아니다)',
        not false_pass and n_pass >= 1, (false_pass[:3], n_pass))
    chk('T16i 같은 표본 — 기록 상한 ≥ 그 φ 의 정확 에너지 (분수 · Dirichlet 좌변 그 자체 · 부동소수 여유가 항 · 합 반올림을 덮는다)',
        not under, under[:3])


# ═════════════════════════ T17 반올림 순서 · BLAS 스레드 · 칼날 ═════════════════════════
def _permute(L, b, Ab, At, seed):
    from scipy import sparse
    n = L.shape[0]
    perm = np.random.default_rng(seed).permutation(n)
    inv = np.empty(n, np.int64)
    inv[perm] = np.arange(n)
    P = sparse.csr_matrix((np.ones(n), (np.arange(n), perm)), shape=(n, n))
    return (P @ L @ P.T).tocsr(), b[perm], inv[np.asarray(Ab)], inv[np.asarray(At)]


def _cg_cert(L, b, Ab, gb, At, gt, rt=1e-12, maxiter=1000):
    with s3_knobs(GPU_SOLVE=False, AMG_SOLVE=False, CG_MAXITER=maxiter):
        phi, info = quiet(S3._solve_cg, L, b, rtol=rt)
        resid = float(np.linalg.norm(L @ phi - b) / np.linalg.norm(b))
        return quiet(CC.certify, L, b, phi, int(info), resid, rt, Ab, gb, At, gt, 1.0, _resolve)


def _decisions(c):
    return {k: c.get(k) for k in ('pass_a', 'pass_b', 'pass_c', 'pass_d', 'ok', 'status')}


#: T17c 탐침 rtol — 1e-10 = 봉인 표의 칼날 행 (메인 10-21: Sandybridge 경로에서 접합 seed 0 rtol 1e-10 의 σ 오차 1.005e-4 ·
#   불균형 9.790e-5 = ε_I 구간 위 끝 → K8b 실패 · ⓐ ⓒ 가 거부)
PROBE_ENV_RTOLS = (1e-8, 1e-10, 1e-12)
#: T17c 환경 꼴 — OpenBLAS 계산 경로 × 스레드 (메인 10-21 봉인 표 6 조합 그대로 · 기본 = 이 CPU 의 SkylakeX)
PROBE_ENVS = (('Haswell', '1'), ('default', '1'), ('default', '4'), ('Haswell', '4'), ('Sandybridge', '1'), ('Nehalem', '1'))


def probe_env():
    """`--probe-env` (자식 프로세스) — 같은 문제의 판정을 JSON 한 줄로 (T17c 가 OpenBLAS 경로 × 스레드 꼴 `PROBE_ENVS` 로 띄워 대조)."""
    out = {}
    for which in CODEX:
        L, b, Ab, gb, At, gt, _Gs = codex_chain(which)
        c = _cg_cert(L, b, Ab, gb, At, gt)
        out[which] = _decisions(c) | {'sigma_hex': float(c['sigma']).hex(), 'imbalance': c.get('imbalance'),
                                      'err_bound': c.get('target_err_bound_rel'), 'width': c.get('target_width_rel')}
    sidp = CC.probe_bed(0)
    base = quiet(CC.probe_system, sidp, CC.probe_sigma_table(), s3=S3)
    for variant, sysd in (('plain', base), ('junction', quiet(CC.junction_variant, base, sidp))):
        for rt in PROBE_ENV_RTOLS:
            c = _cg_cert(sysd['L'], sysd['b'], sysd['Ab'], sysd['gb'], sysd['At'], sysd['gt'], rt=rt, maxiter=400000)
            out[f'probe_{variant}_{rt:.0e}'] = _decisions(c) | {'sigma_hex': float(c['sigma']).hex(), 'imbalance': c.get('imbalance'),
                                                                'err_bound': c.get('target_err_bound_rel'),
                                                                'width': c.get('target_width_rel')}
    try:
        from threadpoolctl import threadpool_info
        out['_blas'] = [{k: d.get(k) for k in ('internal_api', 'prefix', 'version', 'num_threads', 'architecture')}
                        for d in threadpool_info()]
    except Exception as e:                                  # noqa: BLE001
        out['_blas'] = f'n/a ({type(e).__name__})'
    print('PROBE_ENV ' + json.dumps(out, sort_keys=True))


#: 칼날 (상대 오차 상한이 정확히 1e-4 를 1.1e-20 넘는 (lo, hi, G) — float 나눗셈 비교면 통과 · 정확 분수 비교면 거부).  G = m·2⁻⁵² (m ≡ 9999 mod 10⁴)
KNIFE = ((float.fromhex('0x1.fd70a3d70875fp+0'), float.fromhex('0x1.fd7dae8186635p+0')),
         (float.fromhex('0x1.fd70a3d70604fp+0'), float.fromhex('0x1.fd7dae8183f24p+0')),
         (float.fromhex('0x1.fd70a3d70393fp+0'), float.fromhex('0x1.fd7dae8181813p+0')))


@case('T17 반올림 순서 · OpenBLAS 경로 · 스레드 — 노드 순열 (빠른 판 3 · 긴 판 20) · 긴 판: 탐침 순열 · OpenBLAS 경로 6 꼴 (Haswell · '
      'SkylakeX × 1 · 4 · Sandybridge · Nehalem) — 분명한 사례는 ⓓ 결론 같음 · 칼날 사례는 통과하면 실제 오차 ≤ 1e-4 (ⓑ 는 뒤집힐 수 있다 — 기록)')
def t17():
    flips = {}
    for which in CODEX:
        L, b, Ab, gb, At, gt, Gs = codex_chain(which)
        c0 = _cg_cert(L, b, Ab, gb, At, gt)
        dec = [_decisions(c0)]
        for s in range(int(ARGS.perm_n)):
            Lq, bq, Abq, Atq = _permute(L, b, Ab, At, 100 + s)
            dec.append(_decisions(_cg_cert(Lq, bq, Abq, gb, Atq, gt)))
        flips[which] = {k: sum(d[k] != dec[0][k] for d in dec[1:]) for k in ('pass_a', 'pass_b', 'pass_c', 'pass_d', 'ok')}
        print(f'    [{which}] 노드 순열 {int(ARGS.perm_n)} 개 — 판정이 원 순서와 다른 수 {flips[which]} (원 {dec[0]})')
        chk(f'T17a [{which}] 노드 순열 {int(ARGS.perm_n)} 개 (CG 합 순서가 바뀐다) — ⓓ · 증서 결론 전부 같음 (거부 · POSITIVE_SOLVED)',
            all(d['pass_d'] is False and d['ok'] is False and d['status'] == getattr(CC, 'STATUS_POSITIVE', '?') for d in dec),
            flips[which])
    if not ARGS.long:
        print('    (T17b 탐침 침대 순열 · T17c OpenBLAS 경로 × 스레드 자식 여섯 = 긴 판 전용 — --long)')
        return
    sidp = CC.probe_bed(0)
    base = quiet(CC.probe_system, sidp, CC.probe_sigma_table(), s3=S3)
    sys_probe = []
    for variant, sysd in (('plain', base), ('junction', quiet(CC.junction_variant, base, sidp))):
        sys_probe.append((variant, sysd))
        for rt in (1e-8, 1e-12):
            ds = []
            for s in (None, 7, 8):
                L, b, Ab, At = sysd['L'], sysd['b'], sysd['Ab'], sysd['At']
                if s is not None:
                    L, b, Ab, At = _permute(L, b, Ab, At, s)
                ds.append(_decisions(_cg_cert(L, b, Ab, sysd['gb'], At, sysd['gt'], rt=rt, maxiter=400000)))
            chk(f'T17b [탐침 {variant} · rtol {rt:.0e}] 노드 순열 둘 — ⓓ 결론 같음 (ⓐ ⓑ ⓒ 차이는 기록)',
                len({d['pass_d'] for d in ds}) == 1, ds)
    #  ── 환경 꼴 (자식 프로세스 · 환경변수는 프로세스 시작 전에) — OpenBLAS 계산 경로 (`PROBE_ENVS` — Haswell = Codex 와 비트 같은 경로 ·
    #     기본 = 이 CPU 의 SkylakeX · Sandybridge · Nehalem) × 스레드.  판정 규칙:
    #       분명한 사례 (모든 환경에서 실제 오차 > τ = 분명한 거부 · 보장 오차 상한 ≤ τ/2 = 분명한 통과 · 구간 폭 > τ = 분명한 거부) →
    #         ⓓ · 상태 결론이 모든 환경에서 같아야 한다.
    #       칼날 사례 (그 밖 — 실제 오차가 τ 근처라 해가 경로마다 τ 의 양쪽에 놓일 수 있다 · 예: 봉인 표의 접합 rtol 1e-10 행) →
    #         판정이 경로마다 달라도 되지만 (각 해의 판정이므로) 통과한 해는 전부 실제 오차 ≤ τ (건전 · 보수 쪽 = 거부).
    #     ⓐ ⓑ ⓒ 의 칼날 (주 반례 ⓑ 불균형 9.15e-5 ↔ 1.47e-4) 은 경로마다 다르게 판정되는 것이 정상 — 기록 (단언 아님).
    envs = {}
    for ct, nthr in PROBE_ENVS:
        env = {k: v for k, v in os.environ.items() if k not in ('PYTHONPATH', 'PYTHONHOME', 'OPENBLAS_CORETYPE')}
        env.update(OPENBLAS_NUM_THREADS=nthr, OMP_NUM_THREADS=nthr, MKL_NUM_THREADS=nthr, NUMEXPR_NUM_THREADS=nthr)
        if ct != 'default':
            env['OPENBLAS_CORETYPE'] = ct
        p = subprocess.run([sys.executable, '-I', os.path.abspath(__file__), '--probe-env'], capture_output=True, text=True,
                           env=env, timeout=7200)
        line = [x for x in p.stdout.splitlines() if x.startswith('PROBE_ENV ')]
        envs[f'{ct}/{nthr}'] = (json.loads(line[-1][len('PROBE_ENV '):]) if (p.returncode == 0 and line)
                                else {'_error': (p.returncode, p.stderr[-400:])})
    refs = {which: codex_chain(which)[-1] for which in CODEX}            # Codex = 정확 직렬 공식 G*
    for variant, sysd in sys_probe:                                      # 탐침 = 같은 행렬 직접해 (자기 오차 ≪ 1e-6)
        Ib0, _ = CC.plate_currents(sysd['phi_direct'], sysd['Ab'], sysd['gb'], sysd['At'], sysd['gt'])
        for rt in PROBE_ENV_RTOLS:
            refs[f'probe_{variant}_{rt:.0e}'] = Ib0
    keys = sorted(refs)
    errs = {e: v['_error'] for e, v in envs.items() if '_error' in v}
    arch = {e: sorted({str(d.get('architecture')) for d in (v.get('_blas') or [])
                       if isinstance(d, dict) and d.get('internal_api') == 'openblas'})
            for e, v in envs.items() if '_error' not in v}
    tau, slack = 1e-4, 1e-6                                 # 탐침 참조 = 직접해 (자기 오차 ~1e-8) — 실제 오차 판정의 여유

    def _act(k, r):                                         # 실제 상대 오차 (게시 G 기준 · 참조값 대비)
        G = float.fromhex(r['sigma_hex']) if isinstance(r.get('sigma_hex'), str) else math.nan
        return abs(G - refs[k]) / abs(G) if _fin(G) and G != 0.0 else math.inf
    kind = {}
    for k in keys:
        rs = [envs[e].get(k) or {} for e in envs if '_error' not in envs[e]]
        acts = [_act(k, r) for r in rs]
        ebs = [r.get('err_bound') if _fin(r.get('err_bound')) else math.inf for r in rs]
        wds = [r.get('width') if _fin(r.get('width')) else math.inf for r in rs]
        if rs and min(acts) > tau + slack:
            kind[k] = '분명 거부 (실제 오차 > τ)'
        elif rs and min(wds) > tau:
            kind[k] = '분명 거부 (구간 폭 > τ)'
        elif rs and max(ebs) <= tau / 2:
            kind[k] = '분명 통과 (상한 ≤ τ/2)'
        else:
            kind[k] = '칼날'
    print(f'    환경 꼴 표 (OpenBLAS 실제 경로 {arch}) — 칸 = ⓐⓑⓒⓓ (1 통과 · 0 거부) · ⓓ 보장 오차 상한 · 실제 오차 · ⓑ 불균형:')
    if len({tuple(a) for a in arch.values()}) < 2:
        print('    ⚠ 이 기계에서 두 설정이 같은 OpenBLAS 경로 — 아래 표는 경로 차를 보지 못한다 (스레드 차만)')
    for k in keys:
        print(f'      {k:20s} [{kind[k]}]')
        for e in envs:
            r = envs[e].get(k) or {}
            f = ''.join('1' if r.get(x) else '0' for x in ('pass_a', 'pass_b', 'pass_c', 'pass_d'))
            eb, im = r.get('err_bound'), r.get('imbalance')
            print(f'          {e:14s} {f}  상한 {eb if not isinstance(eb, float) else format(eb, ".3e")}  실제 {_act(k, r):.3e}  '
                  f'불균형 {im if not isinstance(im, float) else format(im, ".3e")}' if r else f'          {e:14s} -')
    clear = [k for k in keys if kind[k] != '칼날']
    same_d = all(len({(envs[e].get(k) or {}).get('pass_d') for e in envs}) == 1
                 and len({(envs[e].get(k) or {}).get('status') for e in envs}) == 1 for k in clear)
    unsound = []
    for e, out in envs.items():
        for k in keys:
            r = out.get(k) or {}
            if r.get('pass_d') is True:
                lim = tau if k in CODEX else tau + slack
                if not _act(k, r) <= lim:
                    unsound.append((e, k, _act(k, r)))
    abc_flip = [k for k in keys if len({tuple((envs[e].get(k) or {}).get(x) for x in ('pass_a', 'pass_b', 'pass_c')) for e in envs}) > 1]
    d_flip = [k for k in keys if len({(envs[e].get(k) or {}).get('pass_d') for e in envs}) > 1]
    bit_flip = [k for k in keys if len({(envs[e].get(k) or {}).get('sigma_hex') for e in envs}) > 1]
    print(f'    σ 비트가 환경마다 다른 사례 {bit_flip} · ⓐ ⓑ ⓒ 판정이 환경마다 다른 사례 (칼날 · 정상 · 기록) {abc_flip} · '
          f'ⓓ 판정이 환경마다 다른 사례 {d_flip} (칼날만 허용)')
    must_clear = set(CODEX) | {f'probe_{v}_{r:.0e}' for v in ('plain', 'junction') for r in (1e-8, 1e-12)}
    chk(f'T17c 환경 꼴 {len(PROBE_ENVS)} (OpenBLAS 경로 × 스레드 · 자식 프로세스) — 분명한 사례 {len(clear)}/{len(keys)} (Codex 셋 · 탐침 '
        'rtol 1e-8 · 1e-12 는 반드시 분명) 는 ⓓ · 상태 결론이 모든 환경에서 같음', not errs and same_d and must_clear <= set(clear),
        errs or ([(k, kind[k]) for k in d_flip], sorted(must_clear - set(clear))))
    chk('T17c2 같은 표 — 어느 환경 · 어느 사례 (칼날 포함) 에서든 ⓓ 통과한 해의 실제 오차 ≤ 1e-4 (참조 = Codex 정확 직렬 G* · 탐침 직접해) '
        '— 보수 · 거짓 통과 0', not errs and not unsound, unsound[:3])
    hw = [e for e in envs if e.startswith('Haswell/') and arch.get(e) and all(a == 'Haswell' for a in arch[e])]
    if hw:
        m = [envs[e].get('main') or {} for e in hw]
        chk('T17c3 Haswell 경로 (Codex 와 같은 계산 경로) — 주 반례가 Codex 판정문 그대로 ⓐ ⓑ ⓒ 를 다 통과하는데 ⓓ 가 거부 '
            '(ⓓ 가 막는 것이 이 꼴이다)', all(r.get('pass_a') and r.get('pass_b') and r.get('pass_c') and r.get('pass_d') is False
                                             and r.get('ok') is False for r in m), m)
    else:
        print(f'    (T17c3 생략 — 이 기계에서 OPENBLAS_CORETYPE=Haswell 이 실제 경로를 바꾸지 않았다: {arch})')


@case('T19 칼날 — 보장 오차 상한이 τ = 1e-4 를 1.1e-20 넘는 (lo, hi, G) 는 거부 (정확 분수 비교 · float 나눗셈이면 통과) · 한 ulp 안쪽은 통과 · '
      '증서 전체 칼날 훑기 (단조 · 통과 점은 정확 오차 ≤ 1e-4)')
def t19():
    from fractions import Fraction as Fr
    tau = Fr(1, 10 ** 4)
    for i, (G, hi) in enumerate(KNIFE):
        ex = (Fr(hi) - Fr(G)) / Fr(G)
        flt = not ((hi - G) / G > 1e-4)
        j = CC.target_judge(G, hi, G)
        chk(f'T19a 칼날 {i} — 정확 오차 상한이 τ 를 {float(ex - tau):.1e} 넘는다 (float 나눗셈 비교면 통과 = {flt}) → ⓓ 거부 (보수 · 정확 비교)',
            ex > tau and j.get('pass_d') is False, (j.get('pass_d'), j.get('target_why')))
        hi2 = math.nextafter(hi, 0.0)
        j2 = CC.target_judge(G, hi2, G)
        chk(f'T19b 칼날 {i} 한 ulp 안쪽 (정확 오차 상한 ≤ τ) → 통과 (보수가 지나치지 않다)',
            (Fr(hi2) - Fr(G)) / Fr(G) <= tau and j2.get('pass_d') is True, (j2.get('pass_d'), j2.get('target_why')))
    j_in = CC.target_judge(1.0, 1.0 + 2.0 ** -20, 1.0)                # 정확히 τ 아래 (폭 = 오차 = 9.5e-7)
    chk('T19c 칼날 대조 — 안쪽 (9.5e-7 ≪ τ) 은 통과', j_in.get('pass_d') is True, j_in)
    L, b, phi, Ab, gb, At, gt = _exact2()
    scan = []
    for dl in np.linspace(0.24e-4, 0.26e-4, 41):
        pb = phi.copy()
        pb[0] += dl                                         # 게시 G = 2 (1 − φ₀) 를 −2δ 옮긴다 (G* 0.5) — 상대 ≈ 4δ · 칼날 δ ≈ 2.5e-5
        cb = _cert_of(L, b, pb, Ab, gb, At, gt)
        Gp = cb.get('I_bot')
        scan.append((float(dl), cb.get('pass_d'), cb.get('target_err_bound_rel'),
                     bool(_fin(Gp) and abs(Fr(Gp) - Fr(1, 2)) <= tau * Fr(Gp))))
    passes = [s for s in scan if s[1] is True]
    mono = all(not (scan[i][1] is not True and scan[i + 1][1] is True) for i in range(len(scan) - 1))
    chk('T19d 증서 전체 칼날 훑기 (두 셀 직렬 · 게시 오차 ≈ 1e-4 둘레 41 점) — 통과는 앞쪽 연속 구간 (단조) · 통과한 점은 전부 정확 오차 ≤ 1e-4 · '
        '통과 · 거부 둘 다 있다', mono and passes and len(passes) < len(scan) and all(s[3] for s in passes),
        [(round(s[0] * 1e6, 3), s[1], s[2]) for s in scan[18:24]])


@case('T20 묶음 합 (`_fsum_bound`) — 2²⁰ 넘는 배열 (생산 침대 = 간선 수천만 → 묶음 길) 의 합 · 오차 상한이 한 번의 정확 반올림 합 (math.fsum) '
      '을 덮는다 (양수 · 묶음 사이 큰 상쇄) · 합 넘침 = 예외 대신 (inf, inf)')
def t20():
    rng = np.random.default_rng(2020)
    n = (1 << 20) + 4099
    pos = 10.0 ** rng.uniform(-8, 8, n)
    mix = rng.standard_normal(n) * 10.0 ** rng.uniform(-3, 3, n)
    mix[:1000] += 1e20                                      # 첫 묶음 = +1e20 · 둘째 묶음 = −1e20 (묶음 사이 상쇄)
    mix[(1 << 20):(1 << 20) + 1000] -= 1e20
    for nm, x in (('양수', pos), ('묶음 사이 상쇄', mix)):
        s, e = CC._fsum_bound(x)
        ref = math.fsum(x.tolist())                         # 정확 합의 정확 반올림 (오차 ≤ u|ref|)
        chk(f'T20a [{nm} · n {n:,}] 묶음 합 오차 상한 ≥ |묶음 합 − 정확 반올림 합| + u|정확 반올림 합| (정확 합까지 덮는다)',
            _fin(s) and _fin(e) and abs(s - ref) + 2.0 ** -53 * abs(ref) <= e, (s, ref, e))
    big = np.full(4, 1.7e308)
    try:
        r = CC._fsum_bound(big)
        ok = (r[0] == math.inf and r[1] == math.inf)
    except Exception as ex:                                 # noqa: BLE001
        ok, r = False, f'{type(ex).__name__}: {ex}'
    chk('T20b 합 넘침 (1.7e308 × 4) → (inf, inf) · 예외 아님 (호출자가 비유한으로 NOT_CERTIFIABLE)', ok, r)


#: ★ 10-23 (Codex 재검토 RCA2-08 · 1저자 10-23 Q1–Q8 권고대로) — 합산 넘침 고침의 기반 (묶음 A 시작 판) · T24 정상 회로 비트 대조
RCA208_BASE = '49a1af626'


def _rca208_sys(n, g):
    """판정문 RCA2-08 꼴 — 독립 노드 n 개 (내부 간선 없음) · 노드마다 아래 · 위 판 간선 g (L 대각 2g · b = g · 모두 유한)."""
    return _hand_system(n, [], [(i, g) for i in range(n)], [(i, g) for i in range(n)])


def _cert_with(mod, L, b, phi, Ab, gb, At, gt):
    """모듈 mod (지금 판 · 기반 판) 의 certify — `_cert_of` 와 같은 인자 (이어 풀기 = 같은 φ)."""
    return quiet(mod.certify, L, b, phi, 0, 0.0, 1e-12, Ab, gb, At, gt, 1.0, lambda L_, b_, x0, rt: (np.asarray(x0), 0))


@case('T24 ★ 10-23 (Codex 재검토 RCA2-08 · P3) 합산 넘침 — 유한 중간값의 최종 합 (U · W `fsum`) · 원장 행 허용 (tol_r) · 판 전류 합이 넘치면 '
      '예외 · 경고 대신 NOT_CERTIFIABLE (판정문 꼴 5 노드 gb = gt = 8e307 · p 0.5 · 원장 허용 유한 · U 합만 넘침 10 노드 4e307 · U 유한 · '
      'W 합만 넘침 5 노드 3e307 · p 1) · 경고를 오류로 바꿔 본다 · 정상 회로 증서 = 고치기 전 판 (49a1af626) 과 비트 같음')
def t24():
    import warnings
    N = getattr(CC, 'STATUS_NOT_CERTIFIABLE', '?')
    cases = (('판정문 꼴 — 독립 노드 5 · gb = gt = 8e307 · p 0.5 (원장 행 허용 :344 · U 최종 합 :476)', 5, 8e307, 0.5),
             ('독립 노드 10 · gb = gt = 4e307 · p 0.5 (원장 허용 유한 · U 최종 합 :476 만 넘침)', 10, 4e307, 0.5),
             ('독립 노드 5 · gb = gt = 3e307 · p 1 (U 유한 · W 최종 합 :553 만 넘침)', 5, 3e307, 1.0))
    for nm, n, g, p in cases:
        L, b, Ab, gb, At, gt = _rca208_sys(n, g)
        phi = np.full(n, p)
        for how, fn in (('target_bracket (판정문 탐침과 같은 호출)', lambda: CC.target_bracket(L, b, phi, Ab, gb, At, gt)),
                        ('certify', lambda: _cert_of(L, b, phi, Ab, gb, At, gt))):
            try:
                with warnings.catch_warnings():
                    warnings.simplefilter('error')             # numpy RuntimeWarning (넘침 · 무효) = 예외 → 시험 실패
                    r = fn()
                err = None
            except Exception as e:                              # noqa: BLE001 — 예외 · 경고 = 고치기 전 꼴 (증서가 상태로 말해야 한다)
                r, err = {}, f'{type(e).__name__}: {e}'
            why = r.get('target_ledger_problem')
            ok = (err is None and r.get('target_ledger_ok') is False and isinstance(why, str) and '넘침' in why
                  and r.get('target_lo') is None and r.get('target_hi') is None)
            if how == 'certify':
                ok = ok and r.get('status') == N and r.get('ok') is False and r.get('pass_d') is False
            chk(f'T24a [{nm} · {how}] → 예외 · 경고 없이 원장 문제 (넘침 사유 · 구간 없음)' + (' · NOT_CERTIFIABLE · ok False' if how == 'certify'
                                                                                     else ''),
                ok, err or {k: r.get(k) for k in ('status', 'ok', 'target_ledger_ok', 'target_ledger_problem', 'target_lo')})
    #  같은 부류의 판별 — 원장 행 허용이 넘치면 (옛 판: 허용 = inf → 행 합 대조가 비어 버린다) 숨은 접지 항 (대각 8e307 · 원장 밖) 을 받았다.
    #  노드 1 · gb = gt = 4e307 · 접지 8e307 (대각 1.6e308 유한) · φ = 접지 계의 정확 해 0.25 → 원장 문제 '원장 대조 넘침' (NOT_CERTIFIABLE)
    from scipy import sparse
    Lg = sparse.csr_matrix(np.array([[1.6e308]]))
    try:
        with warnings.catch_warnings():
            warnings.simplefilter('error')
            cg = _cert_of(Lg, np.array([4e307]), np.array([0.25]), np.array([0]), np.array([4e307]), np.array([0]), np.array([4e307]))
        errg = None
    except Exception as e:                                      # noqa: BLE001
        cg, errg = {}, f'{type(e).__name__}: {e}'
    chk('T24c 숨은 접지 항 + 원장 허용 넘침 (노드 1 · gb = gt = 4e307 · 접지 8e307) → 예외 · 경고 없이 NOT_CERTIFIABLE · 원장 문제 = 대조 넘침 '
        '(옛 판 = 허용 inf 로 행 합 대조가 비어 원장 통과 · POSITIVE_SOLVED)',
        errg is None and cg.get('status') == N and cg.get('target_ledger_ok') is False
        and '원장 대조 넘침' in str(cg.get('target_ledger_problem')),
        errg or {k: cg.get(k) for k in ('status', 'ok', 'target_ledger_ok', 'target_ledger_problem', 'pass_d')})
    #  정상 회로 — 지금 판 ↔ 고치기 전 판 (기반 49a1af626) 의 증서 dict 전체가 비트 같다 (넘침 보호가 정상 값을 바꾸지 않는다)
    try:
        CCb = quiet(_load_base, 'scripts/step3_conv_cert.py', 'step3_conv_cert_rca208_base', commit=RCA208_BASE)
    except Exception as e:                                      # noqa: BLE001
        chk(f'T24b 기반 판 ({RCA208_BASE}) step3_conv_cert 불러오기', False, f'{type(e).__name__}: {e}')
        return
    systems = []
    for nm, n, edges, bot, top, _closed in HAND:
        L, b, Ab, gb, At, gt = _hand_system(n, edges, bot, top)
        ph = np.array([float(x) for x in _fr_solve(n, edges, bot, top)[0]])
        systems += [(f'{nm} · 정확 해', (L, b, ph, Ab, gb, At, gt)), (f'{nm} · 흔든 해 (×(1 + 1e-7))', (L, b, ph * (1.0 + 1e-7), Ab, gb, At, gt))]
    systems.append(('무작위 침대 5×5×10 · 직접해', _grid_system((5, 5, 10), 7)))
    systems.append(('정확 2 노드', _exact2()))
    bad = []
    for nm, args in systems:
        a, c = _cert_with(CC, *args), _cert_with(CCb, *args)
        if not _same(a, c):
            bad.append((nm, sorted(k for k in set(a) | set(c) if not _same(a.get(k), c.get(k)))[:6]))
    chk(f'T24b 정상 회로 {len(systems)} 개 — 증서 dict 전체 = 고치기 전 판 ({RCA208_BASE}) 과 비트 같음 (ⓐ–ⓓ · 구간 · 상태 · 칸)', not bad, bad[:4])


# ═════════════════════════ 증서 ↔ 런 결합 (사전 리뷰 PRE-impl-07 · 1저자 10-21 "권고대로 해") ═════════════════════════
#  반례 (판정문 PRE-impl-07 · 탐침 `probe_zero_binding.py`): CX 바닥 (R_j = ∞) 의 실제 영값 증서에서 지문만 바꾼 사본을
#  `conv_cert_problem` · `next_gen_cert_ok` 가 받았다 — 영값 증서의 `fp_sid` · `fp_sig` 는 hex32 형식만 · σ 결합 (0 = 0) 은 아무것도 묶지
#  않는다 · 양의 해 증서는 지문 칸 자체가 없었다 (σ 1e-9 결합뿐 — 같은 σ 의 다른 침대 · 다른 계획 증서를 받는다).
#  침대 = 생산 단위 (test_ca_ext_z3 와 같은 값 — vox 0.15 · r_f 0.075 · tol_ff 0.05 · s_min 0.6) · 매니페스트 지문 칸 = 생산 배선 함수
#  (`ca_ext_cjunc.payload_prepare` 의 fp · `ptfe_face_alpha.payload_block` 의 evidence.fp) 가 만든 것 그대로 (사본 없음).
BH = 0.15
BN = (6, 3, 8)
BREQ = {'R_j_ohm': 1.0e6, 'len_law': 'len_scaled_v0', 'unreg_law': 'cut', 's_min_um': 0.6, 'tol_ff_um': 0.05, 'ptfe_jlaw': 'P0'}
#: PTFE 선 둘 — 도체 면 (VGCF 기둥 · SE 기둥) 에서 r_P + 여유 밖 (α < 1 행 0 · 캡슐 지문만 다르다 → 같은 계 · 같은 σ · 다른 계획 지문)
PT1 = ((0.88, 0.0, 0.60), (0.88, 0.45, 0.60))
PT2 = ((0.88, 0.0, 0.30), (0.88, 0.45, 0.30))
_BIND_NEW = ('bind_version', 'fp_sid', 'fp_sig', 'fp_face_plan', 'fp_cjunc_registry', 'fp_cjunc_rows')


def _bcell(ix, iy, iz, mirror=False):
    x = (BN[0] - 1 - ix) if mirror else ix
    return ((x + 0.5) * BH, (iy + 0.5) * BH, (iz + 0.5) * BH)


def _bline(a, b, step=BH / 3.0):
    a, b = np.asarray(a, np.float64), np.asarray(b, np.float64)
    n = max(1, int(math.ceil(np.linalg.norm(b - a) / step - 1e-12)))
    return np.asarray([a + (b - a) * (i / n) for i in range(n + 1)])


def _bed_rows(name, ptfe=None, mirror=False):
    """Z = VGCF A (x 1 · z 0..3 · 아래 판) + B (x 2 · z 3..7 · 위 판) — 끝 셀이 면으로 맞닿는 접합 instance 하나 · Z2 = 같은 꼴, 맞닿는
    층 4 (다른 격자) · P = Z + 우회 VGCF C (x 4 · 두 판) · mirror = x 거울 (같은 회로 · 다른 격자) · ptfe = PTFE 선 (µm) 또는 None."""
    zc = {'Z': 3, 'Z2': 4, 'P': 3}[name]
    polys = [(_bcell(1, 1, 0, mirror), _bcell(1, 1, zc, mirror)), (_bcell(2, 1, zc, mirror), _bcell(2, 1, 7, mirror))]
    if name == 'P':
        polys.append((_bcell(4, 1, 0, mirror), _bcell(4, 1, 7, mirror)))
    P, PH, F, K = [], [], [], []
    for i, (a, b) in enumerate(polys):
        pts = _bline(a, b)
        P.append(pts); PH.append(np.full(len(pts), 2)); F.append(np.full(len(pts), 10 + 10 * i)); K.append(np.full(len(pts), 1))
    if ptfe is not None:
        pts = _bline(*ptfe)
        P.append(pts); PH.append(np.full(len(pts), 4)); F.append(np.full(len(pts), 900)); K.append(np.full(len(pts), 1))
    return (np.vstack(P), np.concatenate(PH).astype(np.int64), np.concatenate(F).astype(np.int64),
            np.concatenate(K).astype(np.int64))


def _bsig():
    return (S3.electronic_sigma_table(0.0041, 0.0041, 7853.98, 10.0, 256.6), S3.ionic_sigma_table(0.3e-3, 3e-3))


def _brun(name, cfg, ptfe=None, mirror=False, unreg='cut', se=True, cert=True):
    """침대 · 배선 (cj = 접합만 · fa = face_alpha 만 · cjfa = 둘) → 실제 솔브 둘 (전자 · 이온 · 증서 켬 · 생산 CG) + 생산 배선 함수가 만든
    매니페스트 지문 칸 → {'s3': step3 꼴 블록, 'sid', 'cj', 'fa'}.  Z · Z2 의 접합 = 바닥 극한 (R_j = ∞ · 자리 면 절단 → 관통 없음).
    se = SE 기둥 (x 0 · 이온 채널 관통 — 이온 증서 양의 해) · False 면 이온 도체 없음 (이온 증서 = 영값)."""
    import ca_ext_cjunc as CW
    import ptfe_face_alpha as FA
    P, PH, F, K = _bed_rows(name, ptfe=ptfe, mirror=mirror)
    m = PH != 4                                             # face_alpha 침대 = off 격자 (PTFE 셀 없음)
    hi = tuple(BN[i] * BH for i in range(3))
    se_pts = (np.asarray([_bcell(0, 1, k, mirror) for k in range(BN[2])], np.float64) if se else None)
    sid, pid = S3.rasterize(np.zeros((0, 3)), np.zeros(0), np.zeros(0, np.int64), P[m], PH[m], (0.0, 0.0, 0.0), hi, BH,
                            se_pts=se_pts, add_fid=F[m], add_kind=K[m])
    sig_e, sig_i = _bsig()
    ca, cj, fa = {}, None, None
    if cfg in ('cj', 'cjfa'):
        req = dict(BREQ, unreg_law=unreg)
        if name in ('Z', 'Z2'):
            req.update(R_j_ohm=None, rj_limit='inf')
        mc = np.isin(PH, CW.ADD_PHASES)
        cj = quiet(CW.payload_prepare, sid, lo=(0.0, 0.0, 0.0), vox=BH, pts=P[mc], phase=PH[mc], fid=F[mc], kind=K[mc], cjunc=req,
                   sdcp_mod=None, ptfe_stamp=('face_alpha' if cfg == 'cjfa' else 'off'))
        ca['cjunc'] = {'evidence': {'fp': dict(cj['fp'])}}
    if cfg in ('fa', 'cjfa'):
        m4 = PH == 4
        fa = quiet(FA.payload_prepare, sid, pid, lo=(0.0, 0.0, 0.0), vox=BH, sig_e=sig_e, sig_i=sig_i, pts=P[m4], fid=F[m4],
                   kind=K[m4], channels=('electronic', 'ionic'), dia_law='rope', true_volume_um3=None, build_ionic=True)
        ca['ptfe_face'] = {'evidence': {'fp': dict(FA.payload_block(fa, {})['evidence']['fp'])}}
    kw_e, kw_i = {}, {}
    if cj is not None:
        kw_e['cjunc'] = cj['plan']
    if fa is not None:
        kw_e.update(face_alpha=fa['plans']['electronic'], pid=pid)
        kw_i['face_alpha'] = fa['plans']['ionic']
    knobs = dict(CONV_CERT=True, CG_RTOL=1e-12) if cert else dict(CONV_CERT=False)
    with s3_knobs(GPU_SOLVE=False, AMG_SOLVE=False, **knobs):
        r_e = quiet(S3.solve_sigma_z, sid, sig_e, BH, z_top_um=BN[2] * BH, z_bot_um=0.0, **kw_e)
        r_i = quiet(S3.solve_sigma_z, sid, sig_i, BH, z_top_um=BN[2] * BH, z_bot_um=0.0, **kw_i)
    man = {'ca_ext': ca, 'component_plan': {'electronic': True, 'ionic': True}, 'components': {'ionic': {'status': 'complete'}}}
    s3 = {'sigma_e_eff_S_cm': float(r_e['sigma_eff']), 'sigma_ion_eff_S_cm': float(r_i['sigma_eff']), 'manifest': man,
          'conv_cert': dict(r_e.get('conv_cert') or {}), 'ion_conv_cert': dict(r_i.get('conv_cert') or {})}
    return {'s3': s3, 'sid': sid, 'cj': cj, 'fa': fa, 'r_e': r_e, 'r_i': r_i}


def _ng(s3, **repl):
    return RC.next_gen_cert_ok(dict(s3, **repl))


def _rej(run, cert=None, man=None, channel='electronic'):
    """그 런의 칸 (σ · 매니페스트) 에 증서 (기본 = 그 런의 것) 를 붙여 계약이 거부하는가 — conv_cert_problem · next_gen_cert_ok 둘 다."""
    s3 = run['s3']
    sk = 'conv_cert' if channel == 'electronic' else 'ion_conv_cert'
    sg = s3['sigma_e_eff_S_cm'] if channel == 'electronic' else s3['sigma_ion_eff_S_cm']
    c = s3[sk] if cert is None else cert
    m = s3['manifest'] if man is None else man
    p = _ccp(c, sg, m, channel)
    ok, why = RC.next_gen_cert_ok(dict(s3, manifest=m, **{sk: c}))
    return (p is not None and not ok), (p, why)


def _acc(run):
    s3 = run['s3']
    pe = _ccp(s3['conv_cert'], s3['sigma_e_eff_S_cm'], s3['manifest'], 'electronic')
    pi = _ccp(s3['ion_conv_cert'], s3['sigma_ion_eff_S_cm'], s3['manifest'], 'ionic')
    return pe is None and pi is None and RC.next_gen_cert_ok(s3) == (True, None), (pe, pi, RC.next_gen_cert_ok(s3))


@case('T21 증서 ↔ 런 결합 (사전 리뷰 PRE-impl-07) — 증서의 격자 · 계획 지문 = 매니페스트의 정본 지문 칸 (접합 원장 sid · registry · '
      'plan_rows · face_alpha sid_off · plan_<채널>) · 다른 침대 · 다른 계획 · 다른 채널 · 지문 칸 없는 매니페스트 = 거부 (영값 · 양의 해 둘 다)')
def t21():
    Z, POS = getattr(CC, 'STATUS_ZERO', '?'), getattr(CC, 'STATUS_POSITIVE', '?')
    z = _brun('Z', 'cjfa', ptfe=PT1)
    z2 = _brun('Z2', 'cjfa', ptfe=PT1)
    p = _brun('P', 'cjfa', ptfe=PT1)
    pc = _brun('P', 'cj')
    pcm = _brun('P', 'cj', mirror=True)
    pcf = _brun('P', 'cj', unreg='fused')
    pf1 = _brun('P', 'fa', ptfe=PT1)
    pf2 = _brun('P', 'fa', ptfe=PT2)
    zn = _brun('Z', 'cjfa', ptfe=PT1, se=False)
    zc = _brun('Z', 'cj')
    st = {nm: (r['s3']['conv_cert'].get('status'), r['s3']['ion_conv_cert'].get('status'))
          for nm, r in (('Z', z), ('Z2', z2), ('P', p), ('Pc', pc), ('Pcm', pcm), ('Pcf', pcf), ('Pf1', pf1), ('Pf2', pf2),
                        ('Zn', zn), ('Zc', zc))}
    chk('T21 고정물 — 바닥 극한 (Z · Z2 · Zc) 전자 = VALID_ZERO (조기 반환 · 관통 없음) · P 꼴 = POSITIVE · SE 기둥 이온 = POSITIVE · '
        'SE 없음 (Zn) 이온 = VALID_ZERO',
        all(st[k][0] == Z for k in ('Z', 'Z2', 'Zc', 'Zn')) and all(st[k][0] == POS for k in ('P', 'Pc', 'Pcm', 'Pcf', 'Pf1', 'Pf2'))
        and all(st[k][1] == POS for k in st if k != 'Zn') and st['Zn'][1] == Z
        and z['s3']['conv_cert'].get('zero_source') == 'early_return'
        and str(z['r_e'].get('reason', '')).startswith('no_through_component'), st)
    #  ── 정당한 짝 (자기 런의 증서 · 매니페스트) = 받는다 — 고치기 전에도 받는다 (결합이 정당한 런을 막지 않는다) ──
    for nm, r in (('Z cjfa · 영값 + 이온 양', z), ('Z2 cjfa', z2), ('P cjfa · 양 + 이온 양', p), ('P cj', pc), ('P cj 거울', pcm),
                  ('P cj fused', pcf), ('P fa PT1', pf1), ('P fa PT2', pf2), ('Z cjfa SE 없음 · 영값 + 영값', zn), ('Z cj', zc)):
        ok, why = _acc(r)
        chk(f'T21a 정당한 짝 [{nm}] — 자기 증서 + 자기 매니페스트 = 전자 · 이온 둘 다 문제 없음 · next_gen_cert_ok (True, None)', ok, why)
    #  ── PRE-impl-07 반례 그대로 — 실제 영값 증서에서 지문만 바꾼 사본 ──
    ze = z['s3']['conv_cert']
    forged = dict(ze, fp_sid='0123456789abcdef' * 2, fp_sig='fedcba9876543210' * 2)
    ok, why = _rej(z, forged)
    chk('T21b PRE-impl-07 반례 — 바닥 극한 실제 영값 증서의 지문만 바꾼 사본 → conv_cert_problem · next_gen_cert_ok 거부', ok, why)
    #  ── 실제 다른 침대의 영값 증서 · 다른 침대의 매니페스트 ──
    chk('T21c 다른 침대 (Z2 — 맞닿는 층만 다름 · 둘 다 정당한 영값) 의 실제 영값 증서를 Z 런에 붙임 → 거부 (σ 0 = 0 은 아무것도 안 묶는다)',
        *_rej(z, z2['s3']['conv_cert']))
    chk('T21d Z 의 자기 영값 증서 + 다른 침대 (Z2) 의 매니페스트 → 거부', *_rej(z, man=z2['s3']['manifest']))
    #  ── 양의 해 — σ 결합 (1e-9) 이 못 가르는 다른 침대 · 다른 계획 (σ 같음 = 전제 · 기록) ──
    sp, spm = pc['s3']['sigma_e_eff_S_cm'], pcm['s3']['sigma_e_eff_S_cm']
    chk('T21e 전제 — 거울 침대 (같은 회로 · 다른 격자) σ 같음 (상대 1e-12 · 옛 σ 결합 1e-9 안) · 격자 다름',
        abs(sp - spm) <= 1e-12 * sp and pc['sid'].tobytes() != pcm['sid'].tobytes(), (sp, spm))
    chk('T21e 거울 침대의 양의 증서 (σ 같음) 를 P 런에 붙임 → 거부 (격자 지문 · 접합 계획 지문)', *_rej(pc, pcm['s3']['conv_cert']))
    sf = pcf['s3']['sigma_e_eff_S_cm']
    chk('T21f 전제 — 같은 침대 · 미등록 면 법칙만 다름 (cut ↔ fused · 미등록 VV 면 0) = 같은 격자 · 같은 σ (바이트) · 다른 접합 계획 지문',
        pc['sid'].tobytes() == pcf['sid'].tobytes() and sf == sp and pc['cj']['fp']['plan_rows'] != pcf['cj']['fp']['plan_rows'],
        (sf, sp))
    chk('T21f 접합 계획 지문 — fused 런의 증서를 cut 런에 붙임 → 거부 (σ · 격자 같음 · 계획 행 지문 다름)', *_rej(pc, pcf['s3']['conv_cert']))
    fe1, fe2 = pf1['fa']['plans']['electronic']['fp_plan'], pf2['fa']['plans']['electronic']['fp_plan']
    chk('T21g 전제 — 같은 침대 · PTFE 캡슐 자리만 다름 (도체 면 밖 · α 행 0) = 같은 격자 · 같은 σ (바이트) · 다른 face_alpha 계획 지문',
        pf1['sid'].tobytes() == pf2['sid'].tobytes() and pf1['s3']['sigma_e_eff_S_cm'] == pf2['s3']['sigma_e_eff_S_cm']
        and fe1 != fe2, (pf1['s3']['sigma_e_eff_S_cm'], pf2['s3']['sigma_e_eff_S_cm']))
    chk('T21g face_alpha 계획 지문 — PT2 런의 전자 증서를 PT1 런에 붙임 → 거부', *_rej(pf1, pf2['s3']['conv_cert']))
    chk('T21g face_alpha 계획 지문 — PT2 런의 이온 증서를 PT1 런의 이온 자리에 → 거부',
        *_rej(pf1, pf2['s3']['ion_conv_cert'], channel='ionic'))
    #  ── 채널 — 전자 · 이온 둘 다 영값 (σ 0 = 0) 인 런에서 증서를 맞바꿈 ──
    zne, zni = zn['s3']['conv_cert'], zn['s3']['ion_conv_cert']
    ok1, w1 = _rej(zn, zni, channel='electronic')
    ok2, w2 = _rej(zn, zne, channel='ionic')
    chk('T21h 채널 — 영값 · 영값 런에서 이온 증서를 전자 자리에 · 전자 증서를 이온 자리에 → 둘 다 거부 (face_alpha 채널 계획 · 접합 = 전자 주 '
        '솔브만)', ok1 and ok2, (w1, w2))
    #  ── 매니페스트에 지문 칸이 없다 · 모양이 틀리다 ──
    for nm, mm in (('ca_ext 비었다', {'ca_ext': {}}), ('하위 블록에 evidence 없음', {'ca_ext': {'cjunc': {}, 'ptfe_face': {}}}),
                   ('매니페스트 None', None), ('매니페스트 dict 아님', ['ca_ext'])):
        p_ = _ccp(ze, 0.0, mm, 'electronic')
        ok_ = RC.next_gen_cert_ok({'sigma_e_eff_S_cm': 0.0, 'manifest': mm, 'conv_cert': ze})[0] if isinstance(mm, dict) else False
        chk(f'T21i 지문 칸 없는 매니페스트 [{nm}] → conv_cert_problem 거부' + (' · next_gen_cert_ok 거부' if isinstance(mm, dict) else ''),
            p_ is not None and not ok_, p_)
    #  ── 칸 하나씩 (증서 · 매니페스트) ──
    pe, pman = p['s3']['conv_cert'], p['s3']['manifest']
    cjfp = pman['ca_ext']['cjunc']['evidence']['fp']
    fafp = pman['ca_ext']['ptfe_face']['evidence']['fp']

    def _m(cj=None, fa=None):
        out = json.loads(json.dumps(pman))
        if cj is not None:
            out['ca_ext']['cjunc']['evidence']['fp'] = cj
        if fa is not None:
            out['ca_ext']['ptfe_face']['evidence']['fp'] = fa
        return out
    cert_muts = {
        '결합 판 칸 빠짐': {k: v for k, v in pe.items() if k != 'bind_version'},
        '결합 판 다름': dict(pe, bind_version='cert-bind-v0'),
        '격자 지문 대문자 (같은 수)': dict(pe, fp_sid=str(pe.get('fp_sid')).upper()),
        'σ 표 지문 hex 아님': dict(pe, fp_sig='x' * 32),
        'σ 표 지문 빠짐': {k: v for k, v in pe.items() if k != 'fp_sig'},
        'face_alpha 계획 지문 None (face_alpha 런인데)': dict(pe, fp_face_plan=None),
        '접합 계획 행 지문 다름': dict(pe, fp_cjunc_rows='0' * 32),
        '접합 원장 지문 None': dict(pe, fp_cjunc_registry=None),
    }
    for nm, c in cert_muts.items():
        chk(f'T21j 증서 칸 [{nm}] → 거부', *_rej(p, c))
    pi_ = p['s3']['ion_conv_cert']
    chk('T21j 이온 증서가 접합 지문을 싣는다 (접합 = 전자 주 솔브만) → 거부',
        *_rej(p, dict(pi_, fp_cjunc_registry=pe.get('fp_cjunc_registry'), fp_cjunc_rows=pe.get('fp_cjunc_rows')), channel='ionic'))
    man_muts = {
        'face_alpha fp 에 plan_electronic 칸 없음': _m(fa={k: v for k, v in fafp.items() if k != 'plan_electronic'}),
        '접합 fp 에 plan_rows 칸 없음': _m(cj={k: v for k, v in cjfp.items() if k != 'plan_rows'}),
        '접합 fp 에 registry 칸 없음': _m(cj={k: v for k, v in cjfp.items() if k != 'registry'}),
        '접합 fp sid hex 아님': _m(cj=dict(cjfp, sid='s' * 32)),
        '접합 fp sid 다른 hex': _m(cj=dict(cjfp, sid='a' * 32)),
    }
    for nm, mm in man_muts.items():
        chk(f'T21j 매니페스트 칸 [{nm}] → 거부', *_rej(p, man=mm))
    chk('T21j 접합 런 매니페스트 registry None + 증서도 None (둘이 같아도) → 거부 (접합 런의 주 전자 솔브는 계획이 있다 · 사전 공격 리뷰)',
        *_rej(p, dict(pe, fp_cjunc_registry=None), man=_m(cj=dict(cjfp, registry=None))))
    #  ── 정본 격자 칸 — 조합 런 = 접합 원장 sid (솔버 입구가 실제 격자와 대조) · off 격자 sid_off 와의 일치 = ca_ext 계약 (cjunc_block_problem) 몫 ──
    ok, why = _rej(p, man=_m(fa=dict(fafp, sid_off='b' * 32)))
    chk('T21k 정본 칸 — 조합 런에서 sid_off 만 틀림 (접합 원장 sid 맞음) → 증서 결합은 받는다 (매니페스트 자기 일관 = ca_ext 계약 · 사슬 멈춤 '
        '코드 CA_EXT_RECORD 그대로)', not ok and _ccp(pe, p['s3']['sigma_e_eff_S_cm'], _m(fa=dict(fafp, sid_off='b' * 32))) is None, why)
    pfm = json.loads(json.dumps(pf1['s3']['manifest']))
    pfm['ca_ext']['ptfe_face']['evidence']['fp']['sid_off'] = 'c' * 32
    chk('T21k 정본 칸 — face_alpha 만 런 (접합 없음) 은 sid_off 가 정본 · 다른 hex → 거부', *_rej(pf1, man=pfm))
    #  ── API — 매니페스트 없이 부르면 (두 인자) 결합을 건너뛰는 길이 없다 ──
    try:
        RC.conv_cert_problem(ze, 0.0)
        api = '두 인자 호출이 통과 (결합 생략 길)'
    except TypeError as e:
        api = f'TypeError: {e}'
    chk('T21l API — conv_cert_problem(증서, σ) (매니페스트 없이) = TypeError (조용히 결합을 건너뛰는 기본값 없음)', api.startswith('TypeError'),
        api)
    #  ── 증서 결합 칸 = 솔브 입력의 정본 지문 (같은 함수 · 계획 객체의 칸) ──
    pe_rec = {k: pe.get(k) for k in _BIND_NEW}
    want = {'bind_version': getattr(CC, 'BIND_VERSION', '?'), 'fp_sid': S3._grid_fp(p['sid']),
            'fp_sig': S3._grid_fp(np.asarray(_bsig()[0], np.float64)), 'fp_face_plan': p['fa']['plans']['electronic']['fp_plan'],
            'fp_cjunc_registry': p['cj']['plan']['registry']['fp']['registry'], 'fp_cjunc_rows': p['cj']['plan']['fp_rows']}
    chk('T21m 양의 증서 결합 칸 = 솔브 입력 지문 (step3_sigma._grid_fp(sid) · σ 표 · face_alpha 계획 fp_plan · 접합 원장 · 계획 행)',
        pe_rec == want, (pe_rec, want))
    ze_rec = {k: ze.get(k) for k in _BIND_NEW}
    want_z = {'bind_version': getattr(CC, 'BIND_VERSION', '?'), 'fp_sid': S3._grid_fp(z['sid']),
              'fp_sig': S3._grid_fp(np.asarray(_bsig()[0], np.float64)), 'fp_face_plan': z['fa']['plans']['electronic']['fp_plan'],
              'fp_cjunc_registry': z['cj']['plan']['registry']['fp']['registry'], 'fp_cjunc_rows': z['cj']['plan']['fp_rows']}
    chk('T21m 조기 반환 영값 증서 결합 칸 = 같은 지문 (계획 지문까지)', ze_rec == want_z, (ze_rec, want_z))
    zi_rec = {k: zn['s3']['ion_conv_cert'].get(k) for k in _BIND_NEW}
    want_i = {'bind_version': getattr(CC, 'BIND_VERSION', '?'), 'fp_sid': S3._grid_fp(zn['sid']),
              'fp_sig': S3._grid_fp(np.asarray(_bsig()[1], np.float64)), 'fp_face_plan': zn['fa']['plans']['ionic']['fp_plan'],
              'fp_cjunc_registry': None, 'fp_cjunc_rows': None}
    chk('T21m 이온 영값 증서 결합 칸 = 이온 σ 표 · 이온 face_alpha 계획 · 접합 칸 None', zi_rec == want_i, (zi_rec, want_i))


@case('T22 payload 끝-끝 결합 — 실제 생산 payload (face_alpha + 접합 + rtol · LEAN 3) 의 매니페스트 ↔ 증서 · 정당한 런 = next_gen_cert_ok '
      '통과 · 같은 σ 의 다른 계획 (미등록 면 법칙) 런 증서를 붙이면 거부')
def t22():
    sys.path.insert(0, SCRIPTS)
    import test_ca_ext_b6 as B6
    B6.ARGS = argparse.Namespace(skip_payload=False, old_scripts='', only='')
    td = tempfile.mkdtemp(prefix='tc_bind_')
    try:
        d = os.path.join(td, 'w')
        os.makedirs(d)
        B6.make_fixture(d)
        base = ['--ptfe-stamp', 'face_alpha'] + B6.LEAN3 + ['--step3-rtol', '1e-12']
        rc1, log1, p1 = quiet(B6.run_payload, d, base + B6.CJ, out='bind_cut.json')
        rc2, log2, p2 = quiet(B6.run_payload, d, base + B6.cj_with(unreg_law='fused'), out='bind_fused.json')
        s1, s2 = B6.s3_of(p1), B6.s3_of(p2)
        chk('T22a payload 두 런 rc 0 · 전자 · 이온 증서 있음', rc1 == 0 and rc2 == 0 and isinstance(s1.get('conv_cert'), dict)
            and isinstance(s1.get('ion_conv_cert'), dict) and isinstance(s2.get('conv_cert'), dict),
            (rc1, rc2, (log1 or '')[-300:], (log2 or '')[-300:]))
        chk('T22b 정당한 런 (자기 증서 · 자기 매니페스트) → next_gen_cert_ok (True, None) — 두 런',
            RC.next_gen_cert_ok(s1) == (True, None) and RC.next_gen_cert_ok(s2) == (True, None),
            (RC.next_gen_cert_ok(s1), RC.next_gen_cert_ok(s2)))
        m1 = s1.get('manifest') or {}
        cjf = (((m1.get('ca_ext') or {}).get('cjunc') or {}).get('evidence') or {}).get('fp') or {}
        faf = (((m1.get('ca_ext') or {}).get('ptfe_face') or {}).get('evidence') or {}).get('fp') or {}
        c1, i1 = s1.get('conv_cert') or {}, s1.get('ion_conv_cert') or {}
        chk('T22c 생산 증서 결합 칸 = 생산 매니페스트 지문 (전자: 접합 sid · registry · plan_rows · sid_off · plan_electronic / 이온: '
            'plan_ionic · 접합 칸 None)',
            c1.get('fp_sid') == cjf.get('sid') == faf.get('sid_off') and c1.get('fp_cjunc_registry') == cjf.get('registry')
            and c1.get('fp_cjunc_rows') == cjf.get('plan_rows') and c1.get('fp_face_plan') == faf.get('plan_electronic')
            and i1.get('fp_sid') == cjf.get('sid') and i1.get('fp_face_plan') == faf.get('plan_ionic')
            and i1.get('fp_cjunc_registry') is None and i1.get('fp_cjunc_rows') is None,
            ({k: c1.get(k) for k in _BIND_NEW}, cjf, faf))
        se1, se2 = s1.get('sigma_e_eff_S_cm'), s2.get('sigma_e_eff_S_cm')
        print(f'    (σ_e cut {se1!r} · fused {se2!r} · 같음 = {se1 == se2})')
        ok, why = RC.next_gen_cert_ok(dict(s1, conv_cert=s2.get('conv_cert')))
        chk('T22d fused 런의 전자 증서를 cut 런에 붙임 → next_gen_cert_ok 거부 (σ 같아도 · 접합 계획 지문)', not ok and se1 == se2, (ok, why))
    finally:
        shutil.rmtree(td, ignore_errors=True)


@case('T23 끈 경로 · 기반 (a76f59d0d) 대조 — 증서 끔: 접합 · face_alpha 솔브 결과 전체 같음 · 증서 켬: 기반 증서 칸 값 그대로 · 새 칸 = 결합 '
      '칸뿐 (양의 해 여섯 · 조기 반환 넷)')
def t23():
    S3b = quiet(_load_base, 'scripts/step3_sigma.py', 'step3_sigma_base_bind', BIND_BASE)
    CCb = quiet(_load_base, 'scripts/step3_conv_cert.py', 'step3_conv_cert_base_bind', BIND_BASE)
    new_pos, new_early = set(_BIND_NEW), set(_BIND_NEW) - {'fp_sid', 'fp_sig'}
    for nm, cfg, bed in (('Z cjfa · 조기 반환 영값', 'cjfa', 'Z'), ('P cjfa · 양', 'cjfa', 'P'), ('P fa · 양', 'fa', 'P'),
                         ('P cj · 양', 'cj', 'P')):
        outs_off, outs_on = [], []
        for mod, ccm in ((S3b, CCb), (S3, CC)):
            saved = sys.modules.get('step3_conv_cert')
            sys.modules['step3_conv_cert'] = ccm
            g = globals()
            old_s3 = g['S3']
            g['S3'] = mod
            try:
                outs_off.append(_brun(bed, cfg, ptfe=PT1 if 'fa' in cfg else None, cert=False)['r_e'])
                outs_on.append(_brun(bed, cfg, ptfe=PT1 if 'fa' in cfg else None)['r_e'])
            finally:
                g['S3'] = old_s3
                if saved is None:
                    sys.modules.pop('step3_conv_cert', None)
                else:
                    sys.modules['step3_conv_cert'] = saved
        r_off_b, r_off_n = outs_off
        chk(f'T23a [{nm}] 증서 끔 — 기반 ↔ 새 전자 솔브 결과 (키 · 값 · 배열 바이트) 같음 · 증서 칸 없음',
            _same(r_off_b, r_off_n) and 'conv_cert' not in r_off_n, sorted(set(r_off_b) ^ set(r_off_n)))
        cb, cn = outs_on[0].get('conv_cert') or {}, outs_on[1].get('conv_cert') or {}
        rest = [k for k in outs_on[0] if k != 'conv_cert' and not _same(outs_on[0][k], outs_on[1].get(k))]
        diff = [k for k in cb if not _same(cb[k], cn.get(k))]
        added = set(cn) - set(cb)
        want = new_early if cn.get('zero_source') == 'early_return' else new_pos
        chk(f'T23b [{nm}] 증서 켬 — 솔브 결과 (증서 밖) 같음 · 기반 증서의 모든 칸 값 같음 · 더해진 칸 = 결합 칸 {sorted(want)} 뿐',
            not rest and not diff and added == want, (rest, diff, sorted(added)))


# ═════════════════════════ T18 변이 시험 (소스 몇 글자 · 되돌린다) ═════════════════════════
#: (이름, 모듈, ((바꿀 원문 (정확히 한 번), 바꿀 글), …), 돌릴 시험, 잡아야 할 시험 이름 접두)
MUTANTS = (
    ('U 에서 내부 간선 하나 뺌', 'step3_conv_cert', (('u1, e1 = _fsum_bound(tu[0])', 'u1, e1 = _fsum_bound(tu[0][:-1])'),),
     ('t16',), ('T16a', 'T16b', 'T16i')),
    ('q 트리 보정 생략', 'step3_conv_cert', (('    if _tree:\n        acc = d.copy()', '    if False:\n        acc = d.copy()'),),
     ('t6', 't1'), ('T6c', 'T1c')),
    ('오차 상한 비교 부등호 반대', 'step3_conv_cert', (('elif fe > lim:', 'elif fe < lim:'),), ('t1',), ('T1a',)),
    ('결손 항 뺌 (D = 0)', 'step3_conv_cert', (('    if _defect_term:\n', '    if False:\n'),), ('t6',), ('T6c',)),
    ('상한의 부동소수 여유 뺌 (상한 = 계산된 U 그대로)', 'step3_conv_cert',
     (('hi = (U + e1 + e2 + e3) * (1.0 + 8.0 * _UNIT)', 'hi = U'),), ('t16',), ('T16a', 'T16b', 'T16g', 'T16i')),
    ('원장 행 합 검사 뺌', 'step3_conv_cert', (("        bad_r = bool((np.abs(rs - pl) > ", "        bad_r = False and bool((np.abs(rs - pl) > "),),
     ('t7',), ('T7 [접지',)),                               # ★ 10-23 (RCA2-08) — 행 합 대조가 넘침 보호 안으로 옮겨 글자 자리만 바뀜
    ('영값 위상의 정확 0 요구 뺌', 'step3_conv_cert',
     (("zero_exact = bool(out['I_bot'] == 0.0 and out['I_top'] == 0.0 and out['sigma'] == 0.0)", 'zero_exact = True'),),
     ('t3', 't16'), ('T3c', 'T16f')),
    ('구간 폭 검사 뺌', 'step3_conv_cert', (('    if fw > lim:', '    if False:'),), ('t13',), ('T13b 거부 [구간 폭',)),
    ('게시값 대신 위 판 전류로 판정', 'step3_conv_cert', (("jd = target_judge(tb['target_lo'], tb['target_hi'], out['I_bot'])",
                                                  "jd = target_judge(tb['target_lo'], tb['target_hi'], out['I_top'])"),),
     ('t1',), ('T1a',)),
    ('계약이 ⓓ 를 다시 판정하지 않음', 'run_contract', (("    if jd['pass_d'] is not True:", '    if False:'),), ('t13',),
     ('T13b 거부 [구간이 G',)),
    ('계약이 영값 σ 0 을 요구하지 않음', 'run_contract', (('and s == 0.0 and _fin_num(sigma) and sigma == 0.0', 'and _fin_num(sigma)'),),
     ('t13',), ('T13d 영값 증서 거부 [결과 σ',)),
    #  ★ 굳히기 (사전 공격 리뷰) 의 자리 — 정확 분수 판정 · 입력 dtype · 밑넘침 · 원장 허용의 두 방향 (너무 넓게 · 너무 좁게)
    ('판정 비교를 float 나눗셈으로 (정확 분수 뺌)', 'step3_conv_cert',
     (('    if fw > lim:', '    if w > tol:'), ('elif fe > lim:', 'elif e > tol:')), ('t19',), ('T19a',)),
    ('φ dtype 검사 뺌 (숫자 글자 · bool 을 float 로)', 'step3_conv_cert',
     (("    if p.dtype.kind not in _NUM_KINDS:\n        return f'phi dtype", "    if False:\n        return f'phi dtype"),),
     ('t7',), ('T7h [φ 숫자 글자', 'T7h [φ bool')),
    ('b dtype 검사 뺌', 'step3_conv_cert', (('    if b0.dtype.kind not in _NUM_KINDS:', '    if False:'),), ('t7',),
     ('T7h [b 숫자 글자',)),
    ('밑넘침 검사 뺌', 'step3_conv_cert', (('    return bool(bad.any() or (nz & (z == 0)).any())', '    return False'),), ('t7',),
     ('T7u [부정규', 'T7u [곱 완전')),
    ('대칭 허용을 넓게 (1e-12 → 1e-3)', 'step3_conv_cert', (('_SYM_TOL = 1.0e-12 ', '_SYM_TOL = 1.0e-3 '),), ('t15',), ('T15f',)),
    ('행 합 허용에서 항 수 비례 뺌 (고정 64u)', 'step3_conv_cert',
     (('tol_r = _LEDGER_TOL * (np.diff(Lc.indptr) + kb + kt + 8.0) * (ar + pl)', 'tol_r = _LEDGER_TOL * (ar + pl)'),), ('t15',),
     ('T15b',)),
    ('계약이 부동소수 보수 규칙을 봉인하지 않음', 'run_contract',
     (("                    ('target_fp', _cc.TARGET_FP_RULE)):", '                    ):'),), ('t13',), ('T13b 거부 [부동소수 보수 규칙',)),
    #  ★ 10-21 (사전 리뷰 PRE-impl-07) — 증서 ↔ 런 결합의 자리 (계약 · 솔버 · 증서 기록)
    ('계약이 결합을 안 본다 (증서 안 검사만)', 'run_contract',
     (('    return why or cert_binding_problem(cert, man, channel)', '    return why'),), ('t21',), ('T21b', 'T21c', 'T21e')),
    ('격자 지문 = 모양만 (같음 대조 뺌)', 'run_contract', (("    if cert.get('fp_sid') != want_sid:", '    if False:'),), ('t21',),
     ('T21b', 'T21c', 'T21d')),
    ('face_alpha 계획 지문 대조 뺌', 'run_contract', (("    if cert.get('fp_face_plan') != want_fa:", '    if False:'),), ('t21',),
     ('T21g',)),
    ('접합 계획 지문 대조 뺌', 'run_contract',
     (("    if (cert.get('fp_cjunc_registry'), cert.get('fp_cjunc_rows')) != want_cj:", '    if False:'),), ('t21',), ('T21f',)),
    ('이온 증서를 전자 채널로 대조', 'run_contract',
     (("s.get('sigma_ion_eff_S_cm'), man, 'ionic')", "s.get('sigma_ion_eff_S_cm'), man, 'electronic')"),), ('t21',), ('T21a', 'T21g')),
    ('접합 지문을 채널 안 가리고 요구', 'run_contract',
     (("    if cjf is not None and channel == 'electronic':", '    if cjf is not None:'),), ('t21',), ('T21a',)),
    ('결합 판 이름 봉인 뺌', 'run_contract', (("    if cert.get('bind_version') != _cc.BIND_VERSION:", '    if False:'),), ('t21',),
     ('T21j 증서 칸 [결합 판',)),
    ('정본 격자 칸 = off 격자 먼저 (접합 원장 뒤)', 'run_contract',
     (("    if cjf is not None:\n        want_sid, src = cjf.get('sid'), 'ca_ext.cjunc.evidence.fp.sid'\n    elif faf is not None:\n"
       "        want_sid, src = faf.get('sid_off'), 'ca_ext.ptfe_face.evidence.fp.sid_off'\n",
       "    if faf is not None:\n        want_sid, src = faf.get('sid_off'), 'ca_ext.ptfe_face.evidence.fp.sid_off'\n    elif cjf is not None:\n"
       "        want_sid, src = cjf.get('sid'), 'ca_ext.cjunc.evidence.fp.sid'\n"),), ('t21',), ('T21k',)),
    ('솔버가 격자 지문 자리에 σ 표 지문', 'step3_sigma',
     (("        return {'fp_sid': _grid_fp(sid), ", "        return {'fp_sid': _grid_fp(np.asarray(sigma_of_sid, np.float64)), "),),
     ('t21',), ('T21a', 'T21m')),
    ('솔버가 face_alpha 계획 지문을 안 싣는다', 'step3_sigma',
     (("'fp_face_plan': (_fap['fp_plan'] if _fap is not None else None),", "'fp_face_plan': None,"),), ('t21',), ('T21a', 'T21m')),
    ('솔버가 접합 계획 행 지문을 안 싣는다', 'step3_sigma',
     (("'fp_cjunc_rows': (_cjp['fp_rows'] if _cjp is not None else None)}", "'fp_cjunc_rows': None}"),), ('t21',),
     ('T21a', 'T21m')),
    ('조기 반환 증서에 계획 지문 안 실음 (격자 둘만 · 옛 꼴)', 'step3_sigma',
     (("zero_graph=_zero_graph(d.get('reason')), **_cert_bind_kw())",
       "zero_graph=_zero_graph(d.get('reason')), fp_sid=_grid_fp(sid),\n"
       "                                               fp_sig=_grid_fp(np.asarray(sigma_of_sid, np.float64)))"),), ('t21',),
     ('T21a', 'T21m')),
    ('양의 해 증서에 결합 칸 안 실음 (옛 꼴)', 'step3_sigma', (('        _cert.update(_cc.bind_record(**_cert_bind_kw()))', '        pass'),),
     ('t21',), ('T21a', 'T21m')),
    ('조기 반환 기록이 계획 지문을 버림', 'step3_conv_cert',
     (('fp_face_plan=fp_face_plan,\n                           fp_cjunc_registry=fp_cjunc_registry, fp_cjunc_rows=fp_cjunc_rows))',
       'fp_face_plan=None,\n                           fp_cjunc_registry=None, fp_cjunc_rows=None))'),), ('t21',), ('T21a', 'T21m')),
    #  ★ 10-23 (Codex 재검토 RCA2-08) — 합산 넘침 보호의 자리 (최종 U · W 합 · 원장 허용 · 판 전류 합의 경고)
    ('최종 U 합 보호 뺌 (math.fsum 그대로)', 'step3_conv_cert', (('    U = _fsum_bound([u1, u2, u3])[0]', '    U = math.fsum([u1, u2, u3])'),),
     ('t24',), ('T24a [독립 노드 10',)),
    ('최종 W 합 보호 뺌 (math.fsum 그대로)', 'step3_conv_cert', (('    W = _fsum_bound([w1, w2, w3])[0]', '    W = math.fsum([w1, w2, w3])'),),
     ('t24',), ('T24a [독립 노드 5 · gb = gt = 3e307',)),
    ('원장 허용 넘침 검사 뺌 (허용 inf = 대조 비움)', 'step3_conv_cert', (('    if not fin_t:\n', '    if False:\n'),), ('t24',), ('T24c',)),
    ('원장 대조 경고 막기 뺌', 'step3_conv_cert',
     (("    with np.errstate(over='ignore', invalid='ignore'):\n        rs = np.asarray(Lc.sum(axis=1)).ravel()",
       '    if True:\n        rs = np.asarray(Lc.sum(axis=1)).ravel()'),), ('t24',), ('T24a [판정문 꼴',)),
    ('판 전류 합 경고 막기 뺌', 'step3_conv_cert',
     (("    with np.errstate(over='ignore', invalid='ignore'):\n        Ib = float(", '    if True:\n        Ib = float('),), ('t24',),
     ('T24a [판정문 꼴 — 독립 노드 5 · gb = gt = 8e307 · p 0.5 (원장 행 허용 :344 · U 최종 합 :476) · certify',
      'T24a [독립 노드 10 · gb = gt = 4e307 · p 0.5 (원장 허용 유한 · U 최종 합 :476 만 넘침) · certify')),
)


def _mutant(modname, pairs):
    path = os.path.join(SCRIPTS, modname + '.py')
    with open(path, encoding='utf-8') as fh:
        src = fh.read()
    for old, _new in pairs:
        if src.count(old) != 1:
            raise AssertionError(f'{modname}: 변이 자리 {src.count(old)} 곳 (정확히 1 이어야 한다): {old!r}')
    for old, new in pairs:
        src = src.replace(old, new)
    m = type(sys)(modname)
    m.__file__ = path
    m.__dict__['__mutant__'] = tuple(pairs)
    exec(compile(src, path + ' [변이]', 'exec'), m.__dict__)   # noqa: S102 — 시험 전용 변이 (되돌린다)
    return m


def _muted(fns, run):
    """시험 함수들을 조용히 돌려 (단언 이름, 결과) 목록을 모은다 — 함수가 예외로 죽으면 그것도 실패 단언 하나."""
    _MUTE.append([])
    err = None
    try:
        for f in run:
            try:
                quiet(fns[f])
            except Exception as e:                          # noqa: BLE001 — 변이가 시험을 죽여도 적발이다
                err = f'{type(e).__name__}: {e}'
                _MUTE[-1].append((f'{f}: 예외', False))
    finally:
        res = _MUTE.pop()
    return res, err


@case('T18 변이 시험 — 증서 · 계약 구현 몇 글자를 틀리게 하면 시험이 옳은 이유로 실패한다 (변이 표 · 원 모듈로 되돌림 · 기준선 통과 단언만 '
      '센다 · 빠른 판 = 변이 자리 존재만)')
def t18():
    global CC, RC, S3
    fns = {'t1': t1, 't3': t3, 't6': t6, 't7': t7, 't13': t13, 't15': t15, 't16': t16, 't19': t19, 't21': t21, 't24': t24}
    srcs = {}
    for mod in sorted({m[1] for m in MUTANTS}):
        with open(os.path.join(SCRIPTS, mod + '.py'), encoding='utf-8') as fh:
            srcs[mod] = fh.read()
    miss = [(nm, old) for nm, mod, pairs, _r, _w in MUTANTS for old, _n in pairs if srcs[mod].count(old) != 1]
    chk(f'T18 변이 자리 {sum(len(m[2]) for m in MUTANTS)} 곳이 모듈에 정확히 한 번씩 (시험 ↔ 구현 글자 대조 · 변이 {len(MUTANTS)})',
        not miss, miss[:3])
    if not ARGS.long:
        print('    (변이 표 = 긴 판 전용 — --long)')
        return
    #  기준선 — 변이 없이 같은 시험.  변이에서 실패한 단언 중 **기준선에서 통과한** 것만 적발 근거로 센다 (원래 실패하는 단언으로 적발을
    #  꾸미지 않는다 · 같은 이름이 여럿이면 전부 통과해야 통과로 친다).
    base_res, base_err = _muted(fns, sorted({f for m in MUTANTS for f in m[3]}))
    base_pass = {}
    for n, c in base_res:
        base_pass[n] = base_pass.get(n, True) and c
    base_fail = [n for n, v in base_pass.items() if not v]
    chk(f'T18 기준선 — 변이 없이 돌린 단언 {len(base_res)} 개 전부 통과 (예외 없음)', not base_fail and base_err is None,
        (base_fail[:4], base_err))
    table = []
    for nm, mod, pairs, run, want in MUTANTS:
        orig_cc, orig_rc, orig_s3 = CC, RC, S3
        saved = sys.modules.get(mod)
        try:
            m = _mutant(mod, pairs)
        except Exception as e:                              # noqa: BLE001
            chk(f'T18 [{nm}] 변이 만들기', False, f'{type(e).__name__}: {e}')
            continue
        sys.modules[mod] = m
        if mod == 'step3_conv_cert':
            CC = m
        elif mod == 'step3_sigma':
            S3 = m
        else:
            RC = m
        try:
            res, err = _muted(fns, run)
        finally:
            CC, RC, S3 = orig_cc, orig_rc, orig_s3
            if saved is None:
                sys.modules.pop(mod, None)
            else:
                sys.modules[mod] = saved
        failed = [n for n, c in res if not c]
        right = [n for n in failed if base_pass.get(n) is True and any(n.startswith(w) for w in want)]
        table.append((nm, len(res), len(failed), len(right), right[:2]))
        chk(f'T18 [{nm}] 적발 — 실패 {len(failed)}/{len(res)} · 옳은 이유 (기준선에서 통과한 기대 시험 {want} 가 실패) {len(right)} · '
            f'{right[:2]}', bool(right), (failed[:4], err))
    print('    변이 표 (이름 · 돌린 단언 · 실패 · 옳은 이유 (기준선 통과 → 변이 실패) 수 · 예):')
    for row in table:
        print(f'      {row[0]:40s} {row[1]:4d} {row[2]:4d} {row[3]:4d}  {row[4]}')
    chk('T18 되돌림 — 변이 뒤 시험이 쓰는 모듈 = 원 모듈 (sys.modules · 전역 CC · RC · S3 · 변이 표지 없음)',
        CC is sys.modules.get('step3_conv_cert') and RC is sys.modules.get('run_contract') and S3 is sys.modules.get('step3_sigma')
        and '__mutant__' not in CC.__dict__ and '__mutant__' not in RC.__dict__ and '__mutant__' not in S3.__dict__, (CC, RC, S3))


def main():
    global S3, CC, RC, ARGS
    ap = argparse.ArgumentParser(description='STEP3 수렴 증서 ⓓ 목표량 증서 + 해 상태 시험 (시험 먼저 · 기본 = 빠른 판 · --long = 긴 판)')
    ap.add_argument('--only', default='', help='쉼표로 나눈 시험 번호 (첫 낱말 정확히 · 예: T1,T13)')
    ap.add_argument('--long', action='store_true',
                    help='긴 판 — 표본 크게 (T5 1,500 · T16 200 · T17 순열 20) + 탐침 순열 · OpenBLAS 경로 자식 여섯 (T17) · 시간 (T14) · '
                         '변이 표 (T18).  게이트에는 빠른 판만 (메인 10-21)')
    ap.add_argument('--search-n', default=None, type=int, help='T5 표본 수 (변형마다 · 빠른 판 300 · 긴 판 1,500)')
    ap.add_argument('--circuits-n', default=None, type=int, help='T16 무작위 손 회로 수 (빠른 판 40 · 긴 판 200)')
    ap.add_argument('--perm-n', default=None, type=int, help='T17 Codex 사례마다 노드 순열 수 (빠른 판 3 · 긴 판 20)')
    ap.add_argument('--probe-env', action='store_true', help='(T17 자식 프로세스) 판정을 JSON 한 줄로 찍고 끝낸다')
    ARGS = ap.parse_args()
    for k, fast, slow in (('search_n', 300, 1500), ('circuits_n', 40, 200), ('perm_n', 3, 20)):
        if getattr(ARGS, k) is None:
            setattr(ARGS, k, slow if ARGS.long else fast)
    import step3_sigma as _s3
    S3 = _s3
    import step3_conv_cert as _cc
    CC = _cc
    import run_contract as _rc
    RC = _rc
    if ARGS.probe_env:
        probe_env()
        return 0
    only = [x.strip() for x in ARGS.only.split(',') if x.strip()]
    mode = '긴 판' if ARGS.long else '빠른 판'
    t0 = time.time()
    for tag, fn, long_only in CASES:
        if only and tag.split()[0] not in only:
            continue
        if long_only and not ARGS.long:
            print(f'\n── {tag}\n    (긴 판 전용 — 빠른 판에서는 돌지 않는다 · --long)')
            continue
        print(f'\n── {tag}')
        tc = time.time()
        try:
            fn()
        except Exception as e:                              # noqa: BLE001 — 구현 전 (API 없음) 도 시험 단위로 기록
            import traceback
            traceback.print_exc(limit=3)
            chk(f'{tag.split()[0]}: 실행', False, f'{type(e).__name__}: {e}')
        print(f'    ({tag.split()[0]} {time.time() - tc:.1f} s)')
    print(f'\n== test_step3_target_cert [{mode}]: {_ok}/{_ok + len(_fail)} PASS ({time.time() - t0:.1f} s)')
    if _fail:
        print('FAIL: ' + ' · '.join(_fail))
    return 0 if not _fail else 1


if __name__ == '__main__':
    sys.exit(main())
