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

  python3 scripts/test_step3_target_cert.py               # 전부 (빠름 · 수십 초)
  python3 scripts/test_step3_target_cert.py --only T1,T13 # 이름 접두
"""
import argparse
import contextlib
import importlib.util
import io
import json
import math
import os
import subprocess
import sys
import tempfile
import time

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, 'scripts')
sys.path.insert(0, SCRIPTS)
BASE_COMMIT = '47d23baba'                 # 이 수정의 기반 (Z3 합친 메인) — 끈 경로 비트 대조 · A/B/C 값 대조

S3 = CC = RC = None
ARGS = None
_ok, _fail = 0, []
CASES = []


def chk(name, cond, why=''):
    global _ok
    cond = bool(cond)
    if cond:
        _ok += 1
        print(f'  PASS  {name}')
    else:
        _fail.append(name)
        print(f'  FAIL  {name}' + (f'  ({why})' if why != '' else ''))
    return cond


def case(tag):
    def deco(fn):
        CASES.append((tag, fn))
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


@case('T4 양성 (정상 수렴) — 정확 해 · 무작위 침대 생산 CG · 봉인 탐침 침대 (섬유 · 접합) rtol 1e-12 → ⓓ 통과')
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
    for variant, sysd in (('plain', base), ('junction', quiet(CC.junction_variant, base, sidp))):
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


@case('T5 건전성 — Codex 생성기 그대로 (seed 611 · 막다른 / 연결 각 1,500) · ⓓ 거짓 통과 0 · 구간 빗나감 0')
def t5():
    with s3_knobs(GPU_SOLVE=False, AMG_SOLVE=False, CG_MAXITER=300):
        for variant in ('deadend', 'connected'):
            t0 = time.time()
            o = quiet(_search, variant, int(ARGS.search_n))
            print(f'    [{variant}] {o} ({time.time() - t0:.1f}s)')
            chk(f'T5a [{variant}] 생산 술어 거짓 수렴 (info 0 · 오차 > 1e-4) 이 많다 = 판별력 있는 표본 (≥ 100)', o['bad'] >= 100, o)
            chk(f'T5b [{variant}] 그 해들 중 ⓓ · 증서 통과 0 (거짓 통과 없음)', o['false_d'] == 0 and o['problem'] == 0, o)
            chk(f'T5c [{variant}] 모든 해에서 구간이 정확 G* 를 담는다 (빗나감 0)', o['miss'] == 0, o)
            chk(f'T5d [{variant}] ⓓ 가 모든 해를 거부하지는 않는다 (통과 ≥ 50 — 보수만이 아니다)', o['pass_d'] >= 50, o)


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


def _load_base(rel, name):
    src = subprocess.run(['git', '-C', ROOT, 'show', f'{BASE_COMMIT}:{rel}'], capture_output=True, check=True).stdout
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


@case('T13 run_contract.conv_cert_problem — ⓓ 를 기록된 수로 다시 판정 · 상태 먼저 분기 · 영값 위상 σ 0 수용 · 나머지 거부')
def t13():
    good, sig = _real_cert()
    chk('T13a 실제 양의 증서 → 문제 없음', RC.conv_cert_problem(good, sig) is None, RC.conv_cert_problem(good, sig))
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
        '원장 실패인데 통과 표지': lambda c: dict(c, target_ledger_ok=False),
        '위상 영인데 POSITIVE': lambda c: dict(c, target_topology='zero'),
    }
    for nm, fn in muts.items():
        chk(f'T13b 거부 [{nm}]', RC.conv_cert_problem(fn(dict(good)), sig) is not None)
    zero = CC.early_record({'sigma_eff': 0.0, 'n_dof': 4, 'n_through_dof': 0, 'reason': 'no_through_component'},
                           zero_graph='cell6', fp_sid='a' * 32, fp_sig='b' * 32)
    chk('T13c 영값 위상 증서 + 결과 σ 0 → 문제 없음 (바닥 극한 σ 0 = 정상 결과 · NOT_COMPUTED 로 멈추지 않는다)',
        RC.conv_cert_problem(zero, 0.0) is None, RC.conv_cert_problem(zero, 0.0))
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
        chk(f'T13d 영값 증서 거부 [{nm}]', RC.conv_cert_problem(cz, sg) is not None)
    short = CC.early_record({'sigma_eff': 0.0, 'n_dof': 4, 'reason': 'cjunc_electrode_short'}, zero_graph='cjunc_assembled',
                            fp_sid='a' * 32, fp_sig='b' * 32)
    chk('T13e 단락 증서 → 거부 (게시 가능 상태 아님)', RC.conv_cert_problem(short, 0.0) is not None)
    chk('T13f 다음 세대 게시 조건 — 영값 위상 팔 (σ 0) 통과 · 증서 없는 팔 거부',
        RC.next_gen_cert_ok({'sigma_e_eff_S_cm': 0.0, 'manifest': {'ca_ext': {}}, 'conv_cert': zero})[0]
        and not RC.next_gen_cert_ok({'sigma_e_eff_S_cm': 0.0, 'manifest': {'ca_ext': {}}})[0])


@case('T14 시간 비용 (기록 · 합격선 없음) — 탐침 침대 41,472 dof · 무작위 격자 147,456 dof')
def t14():
    sidp = CC.probe_bed(0)
    base = quiet(CC.probe_system, sidp, CC.probe_sigma_table(), s3=S3)
    t0 = time.perf_counter()
    r = CC.target_bracket(base['L'], base['b'], base['phi_direct'], base['Ab'], base['gb'], base['At'], base['gt'])
    t1 = time.perf_counter()
    print(f'    탐침 침대 n {base["L"].shape[0]:,} · nnz {base["L"].nnz:,} · ⓓ {t1 - t0:.3f} s · 트리 층 {r.get("target_tree_levels")}')
    L, b, phi, Ab, gb, At, gt = _grid_system((48, 48, 64), 2, direct=False)
    t0 = time.perf_counter()
    r2 = CC.target_bracket(L, b, phi, Ab, gb, At, gt)
    t1 = time.perf_counter()
    print(f'    무작위 격자 n {L.shape[0]:,} · nnz {L.nnz:,} · ⓓ {t1 - t0:.3f} s ({1e6 * (t1 - t0) / L.shape[0]:.2f} µs/dof) · '
          f'트리 층 {r2.get("target_tree_levels")}')
    chk('T14 두 계 모두 관통 · 유한 구간 (시간은 기록)', r.get('target_topology') == r2.get('target_topology') == 'through'
        and _fin(r.get('target_lo')) and _fin(r2.get('target_hi')))


def main():
    global S3, CC, RC, ARGS
    ap = argparse.ArgumentParser(description='STEP3 수렴 증서 ⓓ 목표량 증서 + 해 상태 시험 (시험 먼저)')
    ap.add_argument('--only', default='', help='쉼표로 나눈 이름 접두 (예: T1,T13)')
    ap.add_argument('--search-n', default=1500, type=int, help='T5 표본 수 (변형마다 · 기본 1,500)')
    ARGS = ap.parse_args()
    import step3_sigma as _s3
    S3 = _s3
    import step3_conv_cert as _cc
    CC = _cc
    import run_contract as _rc
    RC = _rc
    only = [x.strip() for x in ARGS.only.split(',') if x.strip()]
    t0 = time.time()
    for tag, fn in CASES:
        if only and not any(tag.startswith(o) for o in only):
            continue
        print(f'\n── {tag}')
        try:
            fn()
        except Exception as e:                              # noqa: BLE001 — 구현 전 (API 없음) 도 시험 단위로 기록
            import traceback
            traceback.print_exc(limit=3)
            chk(f'{tag.split()[0]}: 실행', False, f'{type(e).__name__}: {e}')
    print(f'\n== test_step3_target_cert: {_ok}/{_ok + len(_fail)} PASS ({time.time() - t0:.1f} s)')
    if _fail:
        print('FAIL: ' + ' · '.join(_fail))
    return 0 if not _fail else 1


if __name__ == '__main__':
    sys.exit(main())
