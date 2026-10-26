#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""STEP3 수렴 증서 (설계 v1 `docs/reviews/rint_carbon_additive_design_v1_20261020.md` §6 · 등록 R 초안 §3-5 · N15 = 1저자 10-20
권고대로) — 다음 세대 판정 해의 게시 조건.

왜: 지금 생산 술어 (`step3_sigma.solve_sigma_z` — CG `info` 0 · 잔차 유한 · 잔차 ≤ 1e-6 · rtol 1e-8 고정) 는 다음 세대 꼴
(섬유 σ 7,853.98 ↔ σ_NCM 0.0041 = 대비 1.9 × 10⁶ · 아래 판에 매달린 섬유) 에서 **틀린 σ 를 수렴으로 인증**한다 (사전 리뷰 ② 탐침 ·
이 모듈의 `probe_table` 이 리포 시험으로 다시 만든다).  잔차의 상대 기준 ‖b‖ 이 섬유의 판 결합 g (2σ_f·h) 에 지배돼 NCM 영역이
덜 풀린 채 rtol 에 닿는다.

증서 넷 (σ 를 게시하려면 넷 다 · 하나라도 실패 = 미수렴 = 미게시):
  ⓐ 정지 규칙  CG rtol ≤ `CERT_RTOL_MAX` (봉인) · info 0 · 잔차 유한
  ⓑ 판 전류 불균형  |I_bot − I_top| / I_bot ≤ `CERT_EPS_I` (봉인) — 정확한 해에서는 KCL 로 0 (두 판 전류가 같다)
  ⓒ 조임 재풀이  앞 해를 초기값으로 max(rtol × `CERT_RESOLVE_FACTOR`, 1e-14) 까지 이어 풀어 |Δσ|/σ ≤ `CERT_RESOLVE_TOL`
                 (재풀이 자체도 info 0 · 바닥 1e-14 = 설계 권고값 — 봉인 체제 1e-12 에서는 걸리지 않는다)
  ⓓ 목표량 증서 (★ 2026-10-21 · Codex RCA-07 · 1저자 Q5 (가)) — ⓐ ⓑ ⓒ 는 **경험적 검사** (판정문 §3: 실제 생산 CG 해가 셋을 다
                 통과하면서 단자 전도도 오차 1e-4 를 넘는 양의 저항망 셋 — `scripts/test_step3_target_cert.py` T1).  ⓓ 는 단자 목표량을
                 직접 감싼다 (ΔV = 1 · 원장 = 행렬 L 의 비대각 −g + 판 간선 gb · gt):
                   상한  U = Σ g (Δφ)²  (근사 φ 의 에너지 ≥ G* — Dirichlet 원리)
                   하한  (F − D)² / W   (해의 간선 전류에서 내부 KCL 결손을 신장 트리 (두 판을 묶은 뿌리 · 넓이 우선 · 간선 g 큰 쪽) 로
                                         판까지 밀어 지운 흐름 · W = Σ q²/g · F = 판 흐름 · D = 남은 결손 (부동소수) 의 보수 상한 —
                                         Thomson 원리를 결손 허용 꼴로: G* ≥ (F_bot − Σ max(d, 0))² / W · 최대 원리 0 ≤ φ* ≤ 1)
                 게시 G (= 아래 판 전류 I_bot) 가 |G − G*| ≤ `CERT_TARGET_TOL` · G 를 **보장**할 때만 통과 — 구간 폭 ≤ τ·G 이고
                 두 끝까지 거리 ≤ τ·G.  ⚠ 판정문 · 계획의 문자 그대로 ("G ∈ [하한, 상한]") 는 쓰지 않았다: 판 전류는 잔차의 1 차 ·
                 구간은 2 차라 정상 수렴 해의 G 가 구간 **밖**에 놓인다 (탐침 침대 rtol 1e-12: 폭 1e-10 · G 오차 2.5e-8 — T4e) →
                 문자 그대로면 모든 정상 해를 거부.  보장 오차 꼴은 문자 그대로의 조건을 포함한다 (G ∈ 구간 이고 폭 ≤ τG ⇒ 통과).
                 부동소수 보수 (`TARGET_FP_RULE` v2): 합 = 묶음 `math.fsum` (정확 반올림 · 상한 2u) · 순서 고정 (넓이 우선 층 · 배열 순서) ·
                 항 반올림 (U 항 4u · W 항 2u) 의 2 배를 묶음 상한에 더함 · U · W 끝 여유 (1 + 8u) · 판 흐름 −2u|F| · 분자의 뺄셈 반올림
                 −4u(|F| + D) (절대) · 하한 끝 (1 − 4u) · 노드 결손 반올림 상한 (2·차수 + 8)·u·Σ|흐름| — float64 오차 해석 (상대 반올림 모형
                 |δ| ≤ u) 이지 구간 산술 증명은 아니다.  모형 밖 (곱 · 나눗셈이 부정규 범위 · 완전 밑넘침 · 넘침) = NOT_CERTIFIABLE.
                 판정 비교 = 정확 분수 (τ = 1/10⁴ · 칼날에서 float 나눗셈이 통과 쪽으로 기울지 않게) ·
                 입력 = 수 dtype 만 (글자 · bool 을 float 로 조용히 바꾸지 않는다) · 원장 허용 = 반올림 수준 (대칭 상대 1e-12 · 행 합 항 수 비례).
해 상태 (★ 2026-10-21 · RCA-13 · Q7 일부 — `status`): POSITIVE_SOLVED (관통 성분 있음 · 증서 ⓐ–ⓓ 필요) · VALID_ZERO_TOPOLOGY (조립 ·
  축약 · 절단 그래프에 두 판을 잇는 성분이 없다 = σ 0 이 **정상 결과** · 증서 실패 아님 · 게시 σ 가 정확히 0 일 때만) ·
  ELECTRODE_SHORT (축약 무리가 두 판을 잇는다) · NOT_CERTIFIABLE (그 밖 — 얇은 침대 · 모르는 사유 · 원장 ↔ 행렬 불일치 · 비유한 φ).
  조기 반환 해 (솔버가 CG 없이 σ 0 을 낸 해) 는 `early_record` · 푼 해는 `certify` 가 같은 판 (`CERT_VERSION`) 으로 낸다.
증서 ↔ 런 결합 (★ 2026-10-21 · 사전 리뷰 PRE-impl-07 · 1저자 "권고대로 해" — `bind_record` · 판 `BIND_VERSION`): 솔버가 증서 (영값 ·
  양의 해 · 조기 반환 · 행렬 그래프) 에 그 해의 솔브 입력 지문을 싣는다 — 격자 `fp_sid` · σ 표 `fp_sig` (`step3_sigma._grid_fp`) ·
  face_alpha 계획 `fp_face_plan` (`fp_plan` — σ 표 · pid · 캡슐 · 행 지문을 품는다) · 접합 원장 `fp_cjunc_registry` · 계획 행
  `fp_cjunc_rows`.  `run_contract.cert_binding_problem` 이 매니페스트의 정본 지문 칸과 대조한다 (옛 판: 영값 증서 지문 = hex32 형식만 ·
  σ 결합 0 = 0 은 아무것도 안 묶었다 → 다른 침대의 영값 증서를 받았다 · 양의 해 증서는 지문 칸이 없었다).
  ⚠ 계 (행렬 L · b) 지문은 아니다 — 결합 = 솔브 입력 (격자 · σ 표 · 계획) 까지.

봉인 (설계 §6 절차 3 · 결과 전 · 합성 직접해 대조 — 실침대 σ 를 보지 않는다):
  `probe_table()` = 24 × 24 × 72 · vox 0.15 · AM (σ 0.0041) 바탕에 아래 판에서 자라 위 판에 안 닿는 섬유 기둥 (σ 7,853.98 · 셀 10 %) ·
  시드 0 · 1 · 2 · 꼴 둘 (`plain` · 기둥 가운데 축방향 면 하나를 접합 간선 g = 1e4/R_j (R_j 1e6 Ω) 로 바꾼 `junction`) ·
  rtol {1e-8, 1e-10, 1e-12, 1e-14} × CPU Jacobi CG (생산 `_solve_cg`) ↔ 같은 행렬 직접해.
  `derive_seal(table)` = 정지 rtol = 모든 행에서 σ 오차 ≤ 1e-4 인 가장 느슨한 rtol · ε_I 구간 = [σ 오차 ≤ 1e-4 인 해의 불균형 최댓값,
  σ 오차 > 1e-4 인 해의 최솟값) · 1e-4 가 구간 안이면 1e-4 · 아니면 기하 중점 · 구간이 비면 ⓑ = 진단 칸 (증서 = ⓐ + ⓒ).
  ⇒ 아래 상수는 그 규칙의 결과다 — `scripts/test_step3_conv_cert.py` K8 이 다시 계산해 대조한다 (상수만 바꾸면 실패).
⚠ 합성 격자 · 실침대 아님 · 수치 인용 불가 ([탐침]).  실침대 반복 수 · 시간은 숫자 탐침 (값 봉인) 에서 따로 잰다.

  python3 scripts/step3_conv_cert.py --table      # 봉인 표 (CPU · 수 분)
"""
import argparse
import math
import os
import sys

import numpy as np

#: ★ 2026-10-21 — v1 → v2: ok = ⓐ ∧ ⓑ ∧ ⓒ ∧ ⓓ (양의 해) · 상태 칸 (`status`) · 조기 반환 해의 상태 증서.  v1 증서 (ⓓ 없음) 는
#:   `run_contract.conv_cert_problem` 이 판 이름으로 거부한다 (다음 세대 판정 런은 아직 없다 — 소급 대상 0).
CERT_VERSION = 'conv-cert-v2'
#: ⓐ 정지 rtol 상한 — `derive_seal(probe_table())` 의 결과 (2026-10-20 · 봉인 · 바꾸려면 새 봉인 = 표를 다시 · R 개정)
CERT_RTOL_MAX = 1.0e-12
#: ⓑ 판 전류 불균형 문턱 — 같은 표의 기계 규칙 결과 (권고 출발 1e-4 가 구간 안)
CERT_EPS_I = 1.0e-4
#: ⓒ 이어 풀기 rtol = 정지 rtol × 이 값 (설계: 1/100) · 허용 |Δσ|/σ
CERT_RESOLVE_FACTOR = 1.0e-2
CERT_RESOLVE_TOL = 1.0e-4
#: ⓒ 이어 풀기 rtol 의 바닥 — 설계 권고값 1e-14 (= 봉인 정지 rtol 1e-12 × 1/100).  정지 rtol 을 그보다 조이면 1/100 은 1e-16 근처
#:   (float64 CG 가 늘 닿지 못하는 곳) 이 되어 maxiter 까지 돈다 → 바닥에서 멈춘다 (봉인 체제 1e-12 에서는 바닥이 걸리지 않는다).
CERT_RESOLVE_RTOL_FLOOR = 1.0e-14
#: 생산 술어의 잔차 상한 (비교용 — `step3_sigma.solve_sigma_z` 의 `resid > 1e-6`)
PROD_RESID_MAX = 1.0e-6
#: ⓓ 목표량 증서 — 보장할 상대 오차 τ (설계 §6 의 목표 1e-4 그대로 · `SEAL_ERR_TOL` · `CERT_RESOLVE_TOL` 과 같은 수 · 새 합격선 아님)
CERT_TARGET_TOL = 1.0e-4
TARGET_VERSION = 'target-cert-v1'
TARGET_FP_RULE = 'fsum-bfs-defect-margin-v2'   # 부동소수 보수 규칙 (머리 주석 ⓓ) — 바꾸면 이름도 바꾼다 (★ 10-21 v2: 항 반올림 · 분자 절대
#                                                여유 · 밑넘침 거부 · 정확 분수 판정 — v1 은 세 묶음 최악 정렬에서 1 차 여유 0)
#: 해 상태 (RCA-13) — 게시 가능 = POSITIVE_SOLVED (ok) · VALID_ZERO_TOPOLOGY (ok) 뿐
STATUS_POSITIVE = 'POSITIVE_SOLVED'
STATUS_ZERO = 'VALID_ZERO_TOPOLOGY'
STATUS_SHORT = 'ELECTRODE_SHORT'
STATUS_NOT_CERTIFIABLE = 'NOT_CERTIFIABLE'
CERT_STATUSES = (STATUS_POSITIVE, STATUS_ZERO, STATUS_SHORT, STATUS_NOT_CERTIFIABLE)
#: 조기 반환 사유 → 상태 (사유 머리 = 괄호 앞 · 정확 일치).  영값 위상 = 두 판을 잇는 성분이 없다는 것이 그 사유의 정의인 것만.
ZERO_REASONS = ('no_through_component', 'all_floating_dropped', 'no_plate_contact', 'no_conductive_voxels')
SHORT_REASONS = ('cjunc_electrode_short',)
ZERO_SOURCES = ('early_return', 'matrix_graph')
#: ★ 2026-10-21 (사전 리뷰 PRE-impl-07) — 증서 ↔ 런 결합 칸 (`bind_record`) · 판 이름 (바꾸면 이름도 바꾼다 · 계약이 봉인한다)
BIND_VERSION = 'cert-bind-v1'
BIND_KEYS = ('fp_sid', 'fp_sig', 'fp_face_plan', 'fp_cjunc_registry', 'fp_cjunc_rows')
_UNIT = 2.0 ** -53                             # float64 단위 반올림 u
_LEDGER_TOL = 64.0 * _UNIT                     # 원장 ↔ 행렬 대조 (행 합 · b) 허용 = 조립 합 순서 반올림 여유 × (그 행의 항 수 + 8)
_SYM_TOL = 1.0e-12                             # L 대칭 (값) 허용 — 상대 · 중복 간선을 두 방향에서 다른 순서로 더한 반올림 (k·u) 만 받는다
_NUM_KINDS = 'fiu'                             # 받는 수 dtype (부동 · 정수) — 글자 · bool · object · 복소 = 거부 (조용히 바꿔 계산하지 않는다)
_TINY = 2.0 ** -1022                           # 가장 작은 정규수 — 이보다 작은 0 아닌 곱 = 상대 반올림 모형 밖 (`_uflow`)
_FSUM_CHUNK = 1 << 20

PROBE_SHAPE = (24, 24, 72)
PROBE_VOX = 0.15
PROBE_FRAC = 0.10
PROBE_SIGMA_FIBRE = 7853.98
PROBE_SIGMA_AM = 0.0041
PROBE_SEEDS = (0, 1, 2)
PROBE_RTOLS = (1e-8, 1e-10, 1e-12, 1e-14)
PROBE_RJ_OHM = 1.0e6
PROBE_MAXITER = 400000
SEAL_ERR_TOL = 1.0e-4
SEAL_EPS_START = 1.0e-4


def plate_currents(phi, Ab, gb, At, gt):
    """해 → (아래 판 전류 I_bot = Σ g_b (1 − φ) · 위 판 전류 I_top = Σ g_t φ) — 코드 단위 · ΔV = 1.
    ★ 10-23 (Codex 재검토 RCA2-08 같은 부류) — 유한 항의 합이 넘치면 ±inf 그대로 (경고 없이 · 값은 옛 판과 같다 · ⓑ ⓒ 가 비유한으로 실패하고
    ⓓ 원장이 NOT_CERTIFIABLE 을 낸다)."""
    phi = np.asarray(phi, np.float64)
    with np.errstate(over='ignore', invalid='ignore'):
        Ib = float(np.sum(np.asarray(gb, np.float64) * (1.0 - phi[np.asarray(Ab)]))) if Ab is not None and len(Ab) else 0.0
        It = float(np.sum(np.asarray(gt, np.float64) * phi[np.asarray(At)])) if At is not None and len(At) else 0.0
    return Ib, It


def certify(L, b, phi, info, resid, rtol_used, Ab, gb, At, gt, scale, resolve):
    """증서 ⓐ ⓑ ⓒ ⓓ + 해 상태 → dict (모든 칸 · ok).  resolve(L, b, x0, rtol) → (φ, info) = 생산 솔버로 이어 풀기.
    scale = σ_eff / I_bot (L_gap / A) — ⓒ 는 상대 변화라 scale 과 무관하지만 기록용 σ 를 같이 남긴다.
    ★ 2026-10-21 — ⓐ ⓑ ⓒ 의 계산 · 칸 · 값은 v1 그대로 (경험적 검사 · T12) · 판 간선 번호가 φ 밖이면 예외 대신 NOT_CERTIFIABLE.
    ok = ⓐ ∧ ⓑ ∧ ⓒ ∧ ⓓ (POSITIVE_SOLVED) · 게시 σ 가 정확히 0 (VALID_ZERO_TOPOLOGY = 행렬 그래프에 관통 성분 없음) · 그 밖 False."""
    bad = _plate_input_problem(phi, Ab, gb, At, gt)
    if bad:
        return _uncertifiable_record(bad, info, resid, rtol_used, scale)
    out = _certify_abc(L, b, phi, info, resid, rtol_used, Ab, gb, At, gt, scale, resolve)
    tb = target_bracket(L, b, phi, Ab, gb, At, gt)
    a_ok, b_ok, c_ok = out['pass_a'], out['pass_b'], out['pass_c']
    if not tb['target_ledger_ok']:
        st = STATUS_NOT_CERTIFIABLE
        jd = {'pass_d': False, 'target_width_rel': None, 'target_err_bound_rel': None, 'target_in_bracket': None,
              'target_why': f'ledger: {tb["target_ledger_problem"]}'}
        ok = False
    elif tb['target_topology'] == 'zero':
        st = STATUS_ZERO
        zero_exact = bool(out['I_bot'] == 0.0 and out['I_top'] == 0.0 and out['sigma'] == 0.0)
        jd = {'pass_d': None, 'target_width_rel': None, 'target_err_bound_rel': None, 'target_in_bracket': None,
              'target_why': None if zero_exact else 'zero topology but posted plate current != 0 (not certified as zero)'}
        out.update(zero_source='matrix_graph', zero_exact=zero_exact, n_through_dof=0, reason=None)
        ok = zero_exact
    else:
        st = STATUS_POSITIVE
        jd = target_judge(tb['target_lo'], tb['target_hi'], out['I_bot'])
        ok = bool(a_ok and b_ok and c_ok and jd['pass_d'])
    out.update(tb)
    out.update(jd)
    out.update(status=st, target_tol=CERT_TARGET_TOL, scale=_float_or_none(scale), ok=bool(ok))
    return out


def _float_or_none(x):
    try:
        v = float(x)
    except (TypeError, ValueError):
        return None
    return v if math.isfinite(v) else None


def _plate_input_problem(phi, Ab, gb, At, gt):
    """판 간선 입력이 φ 와 맞는가 (번호 = φ 안의 정수 · g 와 길이 같음) — 아니면 사유 (ⓐ–ⓓ 를 세울 수 없다)."""
    p = np.asarray(phi)
    if p.ndim != 1:
        return f'phi shape {p.shape} (1-D 이어야 한다)'
    if p.dtype.kind not in _NUM_KINDS:
        return f'phi dtype {p.dtype} (수 배열 — 글자 · bool · object 를 float 로 조용히 바꿔 계산하지 않는다)'
    for nm, A_, g_ in (('bot', Ab, gb), ('top', At, gt)):
        if A_ is None or not len(A_):
            continue
        A_ = np.asarray(A_)
        if A_.ndim != 1 or A_.dtype == bool or not np.issubdtype(A_.dtype, np.integer):
            return f'plate {nm}: index array dtype {A_.dtype} / shape {A_.shape}'
        if A_.min() < 0 or A_.max() >= len(p):
            return f'plate {nm}: index out of range [0, {len(p)})'
        if g_ is None or np.asarray(g_).shape != A_.shape:
            return f'plate {nm}: conductance length ≠ index length'
        if np.asarray(g_).dtype.kind not in _NUM_KINDS:
            return f'plate {nm}: conductance dtype {np.asarray(g_).dtype} (수 배열)'
    return None


def _uncertifiable_record(why, info, resid, rtol_used, scale):
    rec = {'version': CERT_VERSION, 'rtol_used': _float_or_none(rtol_used), 'rtol_max': CERT_RTOL_MAX, 'eps_I': CERT_EPS_I,
           'resolve_rtol': None, 'resolve_rtol_floor': CERT_RESOLVE_RTOL_FLOOR, 'resolve_tol': CERT_RESOLVE_TOL,
           'info': (int(info) if isinstance(info, (int, np.integer)) and not isinstance(info, bool) else None),
           'resid': _float_or_none(resid), 'I_bot': None, 'I_top': None, 'imbalance': None, 'sigma': None, 'sigma_resolve': None,
           'dsigma_rel': None, 'resolve_info': None, 'resolve_I_bot': None, 'resolve_I_top': None,
           'pass_a': False, 'pass_b': False, 'pass_c': False, 'pass_d': False, 'ok': False}
    rec.update(_target_empty(f'input: {why}'))
    rec.update(status=STATUS_NOT_CERTIFIABLE, target_tol=CERT_TARGET_TOL, scale=_float_or_none(scale),
               target_width_rel=None, target_err_bound_rel=None, target_in_bracket=None, target_why=f'input: {why}')
    return rec


def _certify_abc(L, b, phi, info, resid, rtol_used, Ab, gb, At, gt, scale, resolve):
    """증서 ⓐ ⓑ ⓒ (v1 그대로 — 계산 · 칸 · 값 · 실패 처리 바이트 같음 · `scripts/test_step3_target_cert.py` T12)."""
    Ib, It = plate_currents(phi, Ab, gb, At, gt)
    imb = abs(Ib - It) / abs(Ib) if (Ib != 0.0 and math.isfinite(Ib) and math.isfinite(It)) else math.inf
    try:
        rt = float(rtol_used)
    except (TypeError, ValueError):
        rt = math.nan
    a_ok = (type(info) is int or isinstance(info, (np.integer,))) and int(info) == 0 \
        and resid is not None and math.isfinite(float(resid)) and math.isfinite(rt) and rt <= CERT_RTOL_MAX
    b_ok = bool(math.isfinite(imb) and imb <= CERT_EPS_I)
    rr = max(rt * CERT_RESOLVE_FACTOR, CERT_RESOLVE_RTOL_FLOOR) if math.isfinite(rt) else math.nan
    s1 = Ib * float(scale)
    try:
        phi2, info2 = resolve(L, b, np.asarray(phi, np.float64), rr)
        Ib2, It2 = plate_currents(phi2, Ab, gb, At, gt)
        s2 = Ib2 * float(scale)
        d = abs(s2 - s1) / abs(s1) if (s1 != 0.0 and math.isfinite(s1) and math.isfinite(s2)) else math.inf
        info2 = int(info2)
    except Exception as e:                                 # noqa: BLE001 — 재풀이 실패 = ⓒ 실패 (fail-closed)
        s2, d, info2, Ib2, It2 = math.nan, math.inf, -1, math.nan, math.nan
        _err = f'{type(e).__name__}: {e}'
    else:
        _err = None
    c_ok = bool(info2 == 0 and math.isfinite(d) and d <= CERT_RESOLVE_TOL)
    out = {'version': CERT_VERSION, 'rtol_used': rt, 'rtol_max': CERT_RTOL_MAX, 'eps_I': CERT_EPS_I,
           'resolve_rtol': rr, 'resolve_rtol_floor': CERT_RESOLVE_RTOL_FLOOR, 'resolve_tol': CERT_RESOLVE_TOL,
           'info': int(info) if info is not None else None,
           'resid': (float(resid) if resid is not None else None), 'I_bot': Ib, 'I_top': It, 'imbalance': imb,
           'sigma': s1, 'sigma_resolve': s2, 'dsigma_rel': d, 'resolve_info': info2,
           'resolve_I_bot': Ib2, 'resolve_I_top': It2,
           'pass_a': bool(a_ok), 'pass_b': b_ok, 'pass_c': c_ok, 'ok': bool(a_ok and b_ok and c_ok)}
    if _err:
        out['resolve_error'] = _err
    return out


# ═════════════════════════ ⓓ 목표량 증서 (Codex RCA-07 · 1저자 10-21 Q5 (가)) ═════════════════════════
def _fsum_bound(x):
    """Σ x (float64 배열) → (합, 절대 오차 상한).  묶음 (2²⁰) 마다 `math.fsum` (정확 반올림) 뒤 묶음 합을 다시 `fsum` —
    상한 = 2u · (Σ_k |묶음 합_k| + |합|) (묶음 합 반올림 + 마지막 반올림 · 넉넉히 2 배).  항 자체의 반올림은 호출자가 따로 센다.
    합이 넘치면 (`math.fsum` OverflowError · ±inf 섞임 ValueError) 예외 대신 (inf, inf) — 호출자가 비유한으로 거부한다."""
    x = np.asarray(x, np.float64).ravel()
    try:
        if x.size <= _FSUM_CHUNK:
            s = math.fsum(x.tolist())
            return s, 2.0 * _UNIT * abs(s)
        parts = [math.fsum(x[i:i + _FSUM_CHUNK].tolist()) for i in range(0, x.size, _FSUM_CHUNK)]
        s = math.fsum(parts)
        return s, 2.0 * _UNIT * (math.fsum(abs(p) for p in parts) + abs(s))
    except (OverflowError, ValueError):
        return math.inf, math.inf


def _uflow(z, *ops):
    """곱 · 나눗셈 결과 z (피연산자 ops) 가 상대 반올림 모형 (fl(x∘y) = (x∘y)(1+δ) · |δ| ≤ u) 밖인가 — 0 아닌 |z| < 2⁻¹⁰²² (부정규 ·
    절대 오차 2⁻¹⁰⁷⁵ 가 상대 여유를 넘을 수 있다) 또는 0 아닌 피연산자들의 결과가 0 (완전 밑넘침).  덧셈 · 뺄셈은 점진 밑넘침으로 늘 모형 안."""
    z = np.asarray(z)
    az = np.abs(z)
    bad = (az > 0.0) & (az < _TINY)
    nz = np.ones(z.shape, bool)
    for o in ops:
        nz &= np.asarray(o) != 0.0
    return bool(bad.any() or (nz & (z == 0)).any())


def _target_empty(problem=None):
    """ⓓ 칸 (값 없음) — 원장 · 입력 문제로 구간을 세울 수 없을 때."""
    return {'target_version': TARGET_VERSION, 'target_fp': TARGET_FP_RULE, 'target_ledger_ok': problem is None,
            'target_ledger_problem': problem, 'target_topology': None, 'target_lo': None, 'target_hi': None, 'target_U': None,
            'target_W': None, 'target_flow_bot': None, 'target_flow_top': None, 'target_kcl_raw': None,
            'target_kcl_defect_bound': None, 'target_n_dof': None, 'target_n_edges': None, 'target_n_plate_bot': None,
            'target_n_plate_top': None, 'target_n_through_components': None, 'target_n_floating_nodes': None,
            'target_tree_levels': None}


def _ledger(L, b, Ab, gb, At, gt):
    """행렬 L · 우변 b ↔ 간선 원장 대조 → (원장 dict | None, 문제 | None).
    원장 = L 위 삼각의 비대각 (g = −L_uv > 0 · 0 은 버린다) + 판 간선 (아래 φ 1 · 위 φ 0).  거부 (fail-closed): 정방 아님 · 수 dtype
    아님 (글자 · bool · object — 검사 전에 float 로 바꾸지 않는다) · 비유한 · 비대칭 (모양 · 값 상대 `_SYM_TOL`) · 양의 비대각 (음
    컨덕턴스) · 행 합 ≠ 그 노드의 판 결합 합 (원장 밖 대각 = 접지 · 허용 64u × (그 행 칸 수 + 판 간선 수 + 8) × (|행| 합 + 판 결합)) ·
    b ≠ 아래 판 결합 합 (64u × (아래 판 간선 수 + 8)) · 판 g 비유한 · ≤ 0.
    허용은 반올림 수준만 (`scripts/test_step3_target_cert.py` T15 — 중복 간선 합 순서 · 큰 차수 행의 대각 반올림 · b 합 순서는 받고 참
    비대칭 1e-9 · 참 접지 1e-6 · 참 b 불일치 1e-6 은 거부).  원장 G* 는 비대각 · 판 g 로만 정해지므로 받은 반올림 비대칭 (≤ 1e-12) 이 바꾸는 G* 는 상대 1e-12 이하
    (G* 는 g 에 대해 단조 · 1 차 동차).  ⚠ L 은 바꾸지 않는다 (정준 꼴이 아니면 사본)."""
    from scipy import sparse
    try:
        Lc = sparse.csr_matrix(L)
    except Exception as e:                                 # noqa: BLE001
        return None, f'L 을 CSR 로 못 읽는다 ({type(e).__name__})'
    if Lc.ndim != 2 or Lc.shape[0] != Lc.shape[1]:
        return None, f'L shape {Lc.shape} (정방이어야 한다)'
    if Lc.dtype.kind not in _NUM_KINDS:
        return None, f'L dtype {Lc.dtype} (수 행렬이어야 한다)'
    n = int(Lc.shape[0])
    if Lc.dtype != np.float64:
        Lc = Lc.astype(np.float64)
    if not Lc.has_canonical_format:
        Lc = Lc.copy()
        Lc.sum_duplicates()
        Lc.sort_indices()
    if Lc.nnz and not np.isfinite(Lc.data).all():
        return None, 'L 에 비유한 값'
    up = sparse.triu(Lc, k=1, format='csr')
    lw = sparse.tril(Lc, k=-1, format='csr').T.tocsr()
    for M in (up, lw):
        M.sum_duplicates()
        M.sort_indices()
    if not (np.array_equal(up.indptr, lw.indptr) and np.array_equal(up.indices, lw.indices)):
        return None, 'L 비대칭 (모양)'
    if up.nnz and (np.abs(up.data - lw.data) > _SYM_TOL * np.maximum(np.abs(up.data), np.abs(lw.data))).any():
        return None, 'L 비대칭 (값)'
    if up.nnz and (up.data > 0.0).any():
        return None, 'L 비대각 > 0 (음 컨덕턴스 — 수동 저항망이 아니다)'
    idx = []
    for nm, A_ in (('bot', Ab), ('top', At)):
        A_ = np.zeros(0, np.int64) if A_ is None else np.asarray(A_)
        if A_.size and (A_.ndim != 1 or A_.dtype == bool or not np.issubdtype(A_.dtype, np.integer)):
            return None, f'판 {nm} 간선 번호 dtype {A_.dtype} · 모양 {A_.shape} (1 차원 정수 — 조용히 바꾸지 않는다)'
        idx.append(A_.astype(np.int64).ravel())
    Ab, At = idx
    gg = []
    for nm, g_ in (('bot', gb), ('top', gt)):
        g_ = np.zeros(0) if g_ is None else np.asarray(g_)
        if g_.size and g_.dtype.kind not in _NUM_KINDS:
            return None, f'판 {nm} 컨덕턴스 dtype {g_.dtype} (수 배열 — 조용히 바꾸지 않는다)'
        gg.append(g_.astype(np.float64).ravel())
    gb, gt = gg
    for nm, A_, g_ in (('bot', Ab, gb), ('top', At, gt)):
        if A_.shape != g_.shape or (len(A_) and (A_.min() < 0 or A_.max() >= n)):
            return None, f'판 {nm} 간선 번호 · 길이'
        if len(g_) and not (np.isfinite(g_).all() and (g_ > 0.0).all()):
            return None, f'판 {nm} 컨덕턴스 비유한 · ≤ 0'
    b0 = np.asarray(b)
    if b0.dtype.kind not in _NUM_KINDS:
        return None, f'b dtype {b0.dtype} (수 배열 — 조용히 바꾸지 않는다)'
    bv = b0.astype(np.float64).ravel()
    if bv.shape != (n,) or not np.isfinite(bv).all():
        return None, f'b 모양 {bv.shape} · 비유한'
    kb = np.bincount(Ab, minlength=n) if len(Ab) else np.zeros(n, np.int64)
    kt = np.bincount(At, minlength=n) if len(At) else np.zeros(n, np.int64)
    #  ★ 10-23 (Codex 재검토 RCA2-08 같은 부류 · 판정문 §4 · 우리 재현 stderr `overflow encountered in add`) — 행 합 · 판 결합 · 허용의 중간값이
    #    넘치면 (유한 원소 · 무한 허용 = 대조가 비어 버린다 · 경고) 예외 · 경고 대신 원장 문제 (NOT_CERTIFIABLE) — 원장을 대조할 수 없다
    with np.errstate(over='ignore', invalid='ignore'):
        rs = np.asarray(Lc.sum(axis=1)).ravel()
        ar = np.asarray(abs(Lc).sum(axis=1)).ravel()
        bb = np.bincount(Ab, gb, n) if len(Ab) else np.zeros(n)
        pl = bb + (np.bincount(At, gt, n) if len(At) else np.zeros(n))
        tol_r = _LEDGER_TOL * (np.diff(Lc.indptr) + kb + kt + 8.0) * (ar + pl)
        tol_b = _LEDGER_TOL * (kb + 8.0) * (np.abs(bv) + bb)
        fin_t = bool(np.isfinite(rs).all() and np.isfinite(ar).all() and np.isfinite(pl).all() and np.isfinite(tol_r).all()
                     and np.isfinite(tol_b).all())
        bad_r = bool((np.abs(rs - pl) > tol_r).any()) if fin_t else False
        bad_b = bool((np.abs(bv - bb) > tol_b).any()) if fin_t else False
    if not fin_t:
        return None, '원장 대조 넘침 (행 합 · 판 결합 · 허용의 중간값이 비유한 — 원장을 대조할 수 없다)'
    if bad_r:
        return None, '행 합 ≠ 판 결합 합 (원장 밖 대각 항 — 접지 · 다른 경계)'
    if bad_b:
        return None, 'b ≠ 아래 판 결합 합 (아래 판 φ 1 · 위 판 φ 0 이 아닌 경계)'
    rows = np.repeat(np.arange(n, dtype=np.int64), np.diff(up.indptr))
    keep = up.data < 0.0
    return {'n': n, 'eu': rows[keep], 'ev': up.indices[keep].astype(np.int64), 'eg': -up.data[keep],
            'Ab': Ab, 'gb': gb, 'At': At, 'gt': gt}, None


def _plate_reps(Ab, gb, At, gt):
    """노드마다 대표 판 간선 하나 (g 큰 것 → 같으면 아래 판 먼저 → 번호 작은 것) → (노드, 종류 1 아래 · 2 위, 판 간선 번호)."""
    node = np.concatenate([Ab, At]).astype(np.int64)
    if not len(node):
        z = np.zeros(0, np.int64)
        return z, np.zeros(0, np.int8), z.copy()
    g = np.concatenate([gb, gt])
    kind = np.concatenate([np.ones(len(Ab), np.int8), np.full(len(At), 2, np.int8)])
    idx = np.concatenate([np.arange(len(Ab)), np.arange(len(At))]).astype(np.int64)
    o = np.lexsort((idx, kind, -g, node))
    node, kind, idx = node[o], kind[o], idx[o]
    f = np.r_[True, node[1:] != node[:-1]]
    return node[f], kind[f], idx[f]


def _bfs_forest(n, eu, ev, eg, rn, rk, ri):
    """두 판을 한 뿌리로 묶은 넓이 우선 신장 숲 (층마다 벡터 · 새 노드의 부모 = 앞 층 이웃 중 간선 g 가 큰 것 → 부모 번호 → 간선 번호).
    → (층 목록 [노드 배열], 부모, 부모 종류 (0 내부 · 1 아래 판 · 2 위 판), 부모 간선 (내부 = 원장 번호 · 판 = 판 간선 번호), 도달)."""
    from scipy import sparse
    m = len(eu)
    parent = np.full(n, -1, np.int64)
    pkind = np.full(n, -1, np.int8)
    pedge = np.full(n, -1, np.int64)
    seen = np.zeros(n, bool)
    if not len(rn):
        return [], parent, pkind, pedge, seen
    A = sparse.csr_matrix((np.r_[np.arange(m), np.arange(m)].astype(np.int64) + 1,
                           (np.r_[eu, ev], np.r_[ev, eu])), shape=(n, n))
    indptr = A.indptr.astype(np.int64)
    nbrs = A.indices.astype(np.int64)
    eids = A.data.astype(np.int64) - 1
    seen[rn] = True
    parent[rn] = n
    pkind[rn] = rk
    pedge[rn] = ri
    levels = [rn]
    front = rn
    while True:
        st = indptr[front]
        ln = indptr[front + 1] - st
        tot = int(ln.sum())
        if tot == 0:
            break
        pos = np.repeat(st - (np.cumsum(ln) - ln), ln) + np.arange(tot, dtype=np.int64)
        nb, ed, pa = nbrs[pos], eids[pos], np.repeat(front, ln)
        new = ~seen[nb]
        if not new.any():
            break
        nb, ed, pa = nb[new], ed[new], pa[new]
        o = np.lexsort((ed, pa, -eg[ed], nb))
        nb, ed, pa = nb[o], ed[o], pa[o]
        f = np.r_[True, nb[1:] != nb[:-1]]
        nb, ed, pa = nb[f], ed[f], pa[f]
        seen[nb] = True
        parent[nb] = pa
        pkind[nb] = 0
        pedge[nb] = ed
        levels.append(nb)
        front = nb
    return levels, parent, pkind, pedge, seen


def _node_balance(n, eu, ev, c, Ab, cb, At, ct):
    """노드마다 (들어옴 − 나감) — 내부 간선 흐름 c (eu → ev) · 아래 판 → 노드 cb · 노드 → 위 판 ct."""
    d = np.bincount(eu, c, n) * -1.0 + np.bincount(ev, c, n)
    if len(Ab):
        d = d + np.bincount(Ab, cb, n)
    if len(At):
        d = d - np.bincount(At, ct, n)
    return d


def target_bracket(L, b, phi, Ab, gb, At, gt, *, _tree=True, _defect_term=True):
    """ⓓ — 행렬 L · b (생산 조립) 와 판 간선 (Ab, gb · At, gt) 의 원장 위에서 근사 φ 로 G* 를 감싼다 → dict (`target_*` 칸).
    상한 = (U + fsum 상한 + 항 반올림 8u·U) · (1 + 8u) · 하한 = (F − D − 4u(|F| + D))² / W⁺ · (1 − 4u) (F = 판 흐름 − fsum 상한 ·
    D = 남은 결손의 보수 합 · W⁺ = (W + fsum 상한 + 항 반올림 4u·W) · (1 + 8u)) — 두 판 중 큰 쪽.  관통 성분이 없으면 위상 'zero'
    (하한 0 · 상한 U).  흐름 · 합 넘침 · 곱의 부정규 범위 (`_uflow`) = 원장 문제 칸 (NOT_CERTIFIABLE) · 부정규 하한 = 0 (안전한 쪽).
    `_tree` · `_defect_term` = 시험 전용 (트리 보정 · 결손 항을 끈 변이 — 생산은 둘 다 켠다)."""
    rec = _target_empty()
    led, prob = _ledger(L, b, Ab, gb, At, gt)
    if prob is None:
        p = np.asarray(phi, np.float64).ravel() if phi is not None else np.zeros(0)
        if p.shape != (led['n'],) or not np.isfinite(p).all():
            prob = f'φ 모양 {p.shape} ≠ ({led["n"]},) · 비유한'
    if prob is not None:
        rec.update(_target_empty(prob))
        return rec
    from scipy import sparse
    from scipy.sparse.csgraph import connected_components
    n, eu, ev, eg = led['n'], led['eu'], led['ev'], led['eg']
    Ab, gb, At, gt = led['Ab'], led['gb'], led['At'], led['gt']
    rec.update(target_n_dof=n, target_n_edges=int(len(eu)), target_n_plate_bot=int(len(Ab)), target_n_plate_top=int(len(At)))
    ncomp, lab = connected_components(sparse.coo_matrix((np.ones(len(eu), np.int8), (eu, ev)), shape=(n, n)), directed=False)
    on_b = np.zeros(ncomp, bool)
    on_t = np.zeros(ncomp, bool)
    on_b[lab[Ab]] = True
    on_t[lab[At]] = True
    rec.update(target_n_through_components=int((on_b & on_t).sum()),
               target_n_floating_nodes=int((~(on_b | on_t))[lab].sum()))
    with np.errstate(over='ignore', invalid='ignore', under='ignore'):
        dphi = p[eu] - p[ev]
        c = eg * dphi
        cb = gb * (1.0 - p[Ab])
        ct = gt * p[At]
        tu = (c * dphi, cb * (1.0 - p[Ab]), ct * p[At])   # U 의 항 g Δφ² (한 번만 만든다 — 생산 침대 간선 수억 · 메모리)
        fin_u = all(bool(np.isfinite(t).all()) for t in tu)
        ufl_u = (_uflow(c, eg, dphi) or _uflow(tu[0], c, dphi) or _uflow(cb, gb, 1.0 - p[Ab])
                 or _uflow(tu[1], cb, 1.0 - p[Ab]) or _uflow(ct, gt, p[At]) or _uflow(tu[2], ct, p[At]))
    del dphi
    if not fin_u:                                          # 넘침 = φ 가 이 망의 근사 해가 아니다 (fsum 예외 대신 NOT_CERTIFIABLE)
        rec.update(_target_empty('φ: 흐름 · 에너지 항 넘침 (비유한)'))
        return rec
    if ufl_u:                                              # 밑넘침 = 상대 반올림 모형 밖 (여유가 보장하지 못한다 · 생산 범위 밖)
        rec.update(_target_empty('φ · g: 흐름 · 에너지 항 부정규 범위 (밑넘침 — 상대 반올림 모형 밖)'))
        return rec
    u1, e1 = _fsum_bound(tu[0])
    u2, e2 = _fsum_bound(tu[1])
    u3, e3 = _fsum_bound(tu[2])
    del tu
    #  항 반올림 상한 (Δφ · g·Δφ · ·Δφ 의 반올림 넷 = 항마다 상대 ≤ 4u · 항이 모두 ≥ 0) — 2 배 (8u) 를 묶음 상한에 더한다
    e1, e2, e3 = e1 + 8.0 * _UNIT * abs(u1), e2 + 8.0 * _UNIT * abs(u2), e3 + 8.0 * _UNIT * abs(u3)
    #  ★ 10-23 (Codex 재검토 RCA2-08) — 묶음 합은 유한한데 최종 합이 넘치면 (`math.fsum` OverflowError) 예외 대신 +inf → 아래 비유한 검사 =
    #    NOT_CERTIFIABLE (`_fsum_bound` = 같은 `math.fsum` · 유한이면 값 그대로)
    U = _fsum_bound([u1, u2, u3])[0]
    hi = (U + e1 + e2 + e3) * (1.0 + 8.0 * _UNIT)
    if not math.isfinite(hi):
        rec.update(_target_empty('φ: 에너지 합 넘침 (비유한)'))
        return rec
    rec.update(target_U=float(U), target_hi=float(hi))
    if not (on_b & on_t).any():
        rec.update(target_topology='zero', target_lo=0.0)
        return rec
    rec['target_topology'] = 'through'
    rn, rk, ri = _plate_reps(Ab, gb, At, gt)
    levels, parent, pkind, pedge, seen = _bfs_forest(n, eu, ev, eg, rn, rk, ri)
    rec['target_tree_levels'] = int(len(levels))
    c = c.copy()
    cb = cb.copy()
    ct = ct.copy()
    c[~seen[eu]] = 0.0                                     # 판에 안 닿는 성분 = 흐름 0 (정확 해도 0 · 그 노드 결손 0)
    #  ★ 10-26 묶음 B7 (Codex 회차 ① RR1-02 · 1저자 10-26 Q3 (가)) — 원 KCL 결손 진단 합 (노드 결손 · 그 절댓값 합) 이 넘치면 RuntimeWarning 대신
    #    구조화된 원장 문제 (NOT_CERTIFIABLE) · 유한이면 옛 식 그대로 (같은 연산 · 비트 같음 — errstate 는 경고만 막는다)
    with np.errstate(over='ignore', invalid='ignore'):
        d = _node_balance(n, eu, ev, c, Ab, cb, At, ct)
        kcl_raw = float(np.abs(d).sum())
    if not (math.isfinite(kcl_raw) and np.isfinite(d).all()):
        rec.update(_target_empty('φ: KCL 결손 진단 합 넘침 (비유한)'))
        return rec
    rec['target_kcl_raw'] = kcl_raw
    if _tree:
        acc = d.copy()
        for lv in reversed(levels):                        # 깊은 층부터 — 자식 결손을 모은 뒤 부모 간선으로 민다
            a = acc[lv]
            k = pkind[lv]
            m0 = k == 0
            if m0.any():
                vv, ee, aa = lv[m0], pedge[lv[m0]], a[m0]
                out = eu[ee] == vv                         # 간선 방향 eu → ev 가 자식 → 부모면 흐름을 더한다
                c[ee[out]] += aa[out]
                c[ee[~out]] -= aa[~out]
                np.add.at(acc, parent[vv], aa)
            m1 = k == 1
            if m1.any():
                cb[pedge[lv[m1]]] -= a[m1]                 # 아래 판 → 노드 흐름을 줄여 노드 남는 몫을 판이 받는다
            m2 = k == 2
            if m2.any():
                ct[pedge[lv[m2]]] += a[m2]
            acc[lv] = 0.0
    with np.errstate(over='ignore', invalid='ignore', under='ignore'):
        d2 = _node_balance(n, eu, ev, c, Ab, cb, At, ct)
        a2 = np.bincount(eu, np.abs(c), n) + np.bincount(ev, np.abs(c), n)
        deg = np.bincount(eu, minlength=n) + np.bincount(ev, minlength=n)
        if len(Ab):
            a2 = a2 + np.bincount(Ab, np.abs(cb), n)
            deg = deg + np.bincount(Ab, minlength=n)
        if len(At):
            a2 = a2 + np.bincount(At, np.abs(ct), n)
            deg = deg + np.bincount(At, minlength=n)
        err = (2.0 * deg + 8.0) * _UNIT * a2               # 노드 합 (bincount 순차 합 · 네 묶음 합침) 의 반올림 상한 (넉넉히)
        qg = (c / eg, cb / gb, ct / gt)
        wq = (c * qg[0], cb * qg[1], ct * qg[2])           # q²/g = q·(q/g) (q² 넘침 없이 · 항마다 반올림 둘 = 상대 ≤ 2u)
        fin_l = bool(np.isfinite(c).all() and np.isfinite(cb).all() and np.isfinite(ct).all() and np.isfinite(err).all()
                     and np.isfinite(d2).all() and all(np.isfinite(w).all() for w in wq))
        ufl_l = any(_uflow(r_, q_, g_) or _uflow(w_, q_, r_)
                    for q_, g_, r_, w_ in ((c, eg, qg[0], wq[0]), (cb, gb, qg[1], wq[1]), (ct, gt, qg[2], wq[2])))
    del qg
    if not fin_l:                                          # 트리로 민 흐름 · 결손 · Σq²/g 가 넘쳤다 — 하한을 세울 수 없다
        rec.update(_target_empty('φ: 보정 흐름 · 결손 · Σq²/g 넘침 (비유한)'))
        return rec
    if ufl_l:
        rec.update(_target_empty('φ · g: 보정 흐름 q/g · q²/g 부정규 범위 (밑넘침 — 상대 반올림 모형 밖)'))
        return rec
    if _defect_term:
        dp, dpe = _fsum_bound(np.maximum(d2 + err, 0.0))
        dm, dme = _fsum_bound(np.maximum(err - d2, 0.0))
        Dp = (dp + dpe) * (1.0 + 4.0 * _UNIT)
        Dm = (dm + dme) * (1.0 + 4.0 * _UNIT)
    else:
        Dp = Dm = 0.0
    FB, FBe = _fsum_bound(cb)
    FT, FTe = _fsum_bound(ct)
    w1, we1 = _fsum_bound(wq[0])
    w2, we2 = _fsum_bound(wq[1])
    w3, we3 = _fsum_bound(wq[2])
    del wq
    #  항 반올림 상한 (q/g · q·(q/g) = 상대 ≤ 2u · 항 ≥ 0) — 2 배 (4u) 를 묶음 상한에 더한다
    we1, we2, we3 = we1 + 4.0 * _UNIT * abs(w1), we2 + 4.0 * _UNIT * abs(w2), we3 + 4.0 * _UNIT * abs(w3)
    W = _fsum_bound([w1, w2, w3])[0]                       # ★ 10-23 (RCA2-08) — 최종 합 넘침 = +inf → 아래 비유한 검사 (예외 아님)
    Whi = (W + we1 + we2 + we3) * (1.0 + 8.0 * _UNIT)
    if not all(math.isfinite(v) for v in (Dp, Dm, FB, FBe, FT, FTe, W, Whi)):
        rec.update(_target_empty('φ: 하한 합 넘침 (비유한)'))
        return rec
    #  분자 = 판 흐름 − 그 반올림 상한 − 결손 상한 · 뺄셈 두 번의 반올림 (≤ u·크기 · 각) 을 절대 여유로 뺀다 (상쇄가 커도 분자가 참값을
    #  넘지 않게 — 상대 여유 (1 − 4u) 는 마지막 곱 · 나눗셈 몫)
    num = max(FB - FBe - Dp - 4.0 * _UNIT * (abs(FB) + Dp), FT - FTe - Dm - 4.0 * _UNIT * (abs(FT) + Dm))
    lo = (num * (num / Whi)) * (1.0 - 4.0 * _UNIT) if (num > 0.0 and Whi > 0.0) else 0.0
    if not math.isfinite(lo):                              # num²/W 넘침 — 하한을 세울 수 없다
        rec.update(_target_empty('φ: 하한 넘침 (비유한)'))
        return rec
    if 0.0 < lo < _TINY or (num > 0.0 and Whi > 0.0 and 0.0 < num / Whi < _TINY):
        lo = 0.0                                           # 부정규 하한 = 상대 모형 밖 → 0 (안전한 쪽 · 판정은 하한 0 이면 실패)
    rec.update(target_lo=float(lo), target_W=float(W), target_flow_bot=float(FB), target_flow_top=float(FT),
               target_kcl_defect_bound=float(Dp + Dm))
    return rec


def target_judge(lo, hi, G, tol=CERT_TARGET_TOL):
    """ⓓ 판정 (생산 · `run_contract.conv_cert_problem` 공용 — 같은 함수) — 구간 [lo, hi] ∋ G* 에서 게시 G 의 보장 상대 오차.
    통과 = 0 < lo ≤ hi 유한 · G > 0 유한 · (hi − lo) ≤ τ·G · max(hi − G, G − lo) ≤ τ·G (⇒ |G − G*| ≤ τ·G).
    ★ 비교는 **정확 분수** (lo · hi · G = 그 float 의 정확값 · τ = tol 의 10 진 글자 그대로 (1e-4 → 1/10⁴)) — float 나눗셈 (w > tol) 의
    반올림이 칼날 (보장 오차가 τ 를 1e-20 넘는 해) 에서 통과 쪽으로 기울지 않게 (`scripts/test_step3_target_cert.py` T19).  기록 칸
    `target_width_rel` · `target_err_bound_rel` 은 float 상대값 (사람이 읽는 값 · 판정에 쓰지 않는다)."""
    from fractions import Fraction
    out = {'pass_d': False, 'target_width_rel': None, 'target_err_bound_rel': None, 'target_in_bracket': None, 'target_why': None}

    def _num(x):
        return isinstance(x, (int, float, np.floating, np.integer)) and not isinstance(x, (bool, np.bool_)) and math.isfinite(x)
    if not (_num(lo) and _num(hi) and _num(G) and _num(tol) and float(tol) > 0.0):
        out['target_why'] = f'non-finite / non-numeric (lo {lo!r} · hi {hi!r} · G {G!r} · tol {tol!r})'
        return out
    lo, hi, G = float(lo), float(hi), float(G)
    if not (0.0 < lo <= hi):
        out['target_why'] = f'bracket not 0 < lo <= hi ({lo!r}, {hi!r})'
        return out
    if not G > 0.0:
        out['target_why'] = f'posted G {G!r} <= 0'
        return out
    w = (hi - lo) / G
    e = max(hi - G, G - lo) / G
    out.update(target_width_rel=w, target_err_bound_rel=e, target_in_bracket=bool(lo <= G <= hi))
    FL, FH, FG = Fraction(lo), Fraction(hi), Fraction(G)
    lim = Fraction(repr(float(tol))) * FG
    fw = FH - FL
    fe = max(FH - FG, FG - FL)
    if fw > lim:
        out['target_why'] = f'bracket width {w:.3e} > {float(tol):g} (bound too loose to certify · exact comparison)'
    elif fe > lim:
        out['target_why'] = f'posted G error bound {e:.3e} > {float(tol):g} (exact comparison)'
    else:
        out['pass_d'] = True
    return out


def classify_reason(reason):
    """조기 반환 사유 → 해 상태 (사유 머리 = 첫 '(' 앞 · 정확 일치 · 모르는 사유 = NOT_CERTIFIABLE)."""
    if not isinstance(reason, str) or not reason:
        return STATUS_NOT_CERTIFIABLE
    head = reason.split('(', 1)[0]
    if head in ZERO_REASONS:
        return STATUS_ZERO
    if head in SHORT_REASONS:
        return STATUS_SHORT
    return STATUS_NOT_CERTIFIABLE


def bind_record(*, fp_sid, fp_sig, fp_face_plan=None, fp_cjunc_registry=None, fp_cjunc_rows=None):
    """★ 2026-10-21 (사전 리뷰 PRE-impl-07) — 증서 ↔ 런 결합 칸 (영값 · 양의 해 같은 칸 · 솔버가 솔브 입력에서 낸다):
    fp_sid · fp_sig = 그 해의 sid · σ 표 격자 지문 (`step3_sigma._grid_fp`) · fp_face_plan = 그 솔브의 face_alpha 계획 지문 (`fp_plan` ·
    없으면 None) · fp_cjunc_registry · fp_cjunc_rows = 그 솔브의 탄소 접합 원장 · 계획 행 지문 (없으면 None).  대조 =
    `run_contract.cert_binding_problem` (매니페스트의 정본 지문 칸 · 채널)."""
    return {'bind_version': BIND_VERSION, 'fp_sid': fp_sid, 'fp_sig': fp_sig, 'fp_face_plan': fp_face_plan,
            'fp_cjunc_registry': fp_cjunc_registry, 'fp_cjunc_rows': fp_cjunc_rows}


def early_record(res, *, zero_graph, fp_sid, fp_sig, fp_face_plan=None, fp_cjunc_registry=None, fp_cjunc_rows=None):
    """조기 반환 해 (솔버가 CG 없이 σ 0 을 냈다) 의 상태 증서 — 같은 판 (`CERT_VERSION`) · ⓐ–ⓓ 칸 = None (해당 없음).
    VALID_ZERO_TOPOLOGY = 영값 위상 사유 · 관통 dof 0 (있으면) · σ 정확히 0 · ok True (σ 0 이 정상 결과 — 바닥 극한 R_j = ∞).
    모순 (영값 사유인데 관통 dof > 0 · σ ≠ 0) = NOT_CERTIFIABLE.  zero_graph = 그 0 을 정한 그래프 (조립 · 축약 · 절단 — 솔버가 준다) ·
    fp_sid · fp_sig = 그 해의 sid · σ 격자 지문 (`step3_sigma._grid_fp`) · ★ 10-21 (PRE-impl-07) 계획 지문 셋 = `bind_record` 와 같은 칸
    (증서 ↔ 런 결합 — 영값 증서는 σ 0 = 0 이 아무것도 안 묶으므로 이 칸이 유일한 결합이다)."""
    res = res if isinstance(res, dict) else {}
    reason = res.get('reason')
    st = classify_reason(reason)
    why = None
    ntd = res.get('n_through_dof')
    sig = res.get('sigma_eff')
    if st == STATUS_ZERO:
        if ntd is not None and (isinstance(ntd, (bool, np.bool_)) or not isinstance(ntd, (int, np.integer)) or int(ntd) != 0):
            st, why = STATUS_NOT_CERTIFIABLE, f'zero reason with n_through_dof {ntd!r}'
        elif isinstance(sig, (bool, np.bool_)) or not isinstance(sig, (int, float, np.floating)) or float(sig) != 0.0:
            st, why = STATUS_NOT_CERTIFIABLE, f'zero reason with sigma_eff {sig!r}'
    nd = res.get('n_dof')
    rec = {'version': CERT_VERSION, 'status': st, 'ok': st == STATUS_ZERO, 'zero_source': 'early_return',
           'reason': reason if isinstance(reason, str) else None, 'status_why': why, 'zero_graph': zero_graph,
           'n_through_dof': (0 if st == STATUS_ZERO else (int(ntd) if isinstance(ntd, (int, np.integer))
                                                         and not isinstance(ntd, (bool, np.bool_)) else None)),
           'n_dof': (int(nd) if isinstance(nd, (int, np.integer)) and not isinstance(nd, (bool, np.bool_)) else None),
           'sigma': 0.0, 'fp_sid': fp_sid, 'fp_sig': fp_sig,
           'rtol_max': CERT_RTOL_MAX, 'eps_I': CERT_EPS_I, 'resolve_tol': CERT_RESOLVE_TOL, 'target_tol': CERT_TARGET_TOL,
           'target_version': TARGET_VERSION, 'pass_a': None, 'pass_b': None, 'pass_c': None, 'pass_d': None}
    #  ★ 10-21 (PRE-impl-07) — 결합 칸 (fp_sid · fp_sig 는 위 자리 그대로 · 판 이름과 계획 지문 셋이 뒤에 붙는다)
    rec.update(bind_record(fp_sid=fp_sid, fp_sig=fp_sig, fp_face_plan=fp_face_plan,
                           fp_cjunc_registry=fp_cjunc_registry, fp_cjunc_rows=fp_cjunc_rows))
    return rec


# ═════════════════════════ 봉인 탐침 (합성 · 리포 시험) ═════════════════════════
def probe_bed(seed, shape=PROBE_SHAPE, frac=PROBE_FRAC):
    """AM 바탕 (sid 1) + 아래 판에서 자라 위 판에 안 닿는 섬유 기둥 (sid 3 · 셀 몫 ≈ frac) — 결정적 (시드)."""
    rng = np.random.default_rng(int(seed))
    nx, ny, nz = shape
    sid = np.ones(shape, np.int8)
    target = int(round(frac * nx * ny * nz))
    used = np.zeros((nx, ny), bool)
    count = 0
    cols = rng.permutation(nx * ny)
    for c in cols:
        if count >= target:
            break
        i, j = divmod(int(c), ny)
        if used[i, j]:
            continue
        L = int(rng.integers(nz // 4, nz - 3))             # 위 판에 안 닿는다 (위 셋 이상 비움)
        L = min(L, target - count) if target - count >= 4 else L
        sid[i, j, :L] = 3
        used[i, j] = True
        count += L
    return sid


def probe_sigma_table():
    t = np.zeros(10)
    t[1] = t[2] = PROBE_SIGMA_AM
    t[3] = PROBE_SIGMA_FIBRE
    return t


def _step3_module(mod):
    """`step3_sigma` 모듈 (주어지면 그것).  인자 이름과 지역 import 를 한 함수에 묶지 않는다
    (check_method_discipline 지역 import 그림자 검사)."""
    if mod is not None:
        return mod
    import step3_sigma
    return step3_sigma


def probe_system(sid, sig, vox=PROBE_VOX, s3=None):
    """생산 조립 (`solve_sigma_z`) 이 만든 행렬 L · b · 판 간선을 붙잡는다 (직접해로 푼다 — 그 해가 기준).
    → dict(L, b, Ab, gb, At, gt, phi_direct, idx)."""
    from scipy.sparse.linalg import spsolve
    s3 = _step3_module(s3)
    cap = {}
    old = s3._solve_cg

    def _rec(L, b, *a, **k):
        cap['L'] = L.tocsr(); cap['b'] = np.asarray(b, np.float64).copy()
        x = spsolve(cap['L'].tocsc(), cap['b'])
        cap['phi'] = x
        return x, 0
    s3._solve_cg = _rec
    try:
        res = s3.solve_sigma_z(sid, sig, vox, return_field=True, z_top_um=float(sid.shape[2]) * vox, z_bot_um=0.0)
    finally:
        s3._solve_cg = old
    cond = res['cond']
    idx = -np.ones(sid.shape, np.int64)
    idx[cond] = np.arange(int(cond.sum()))
    (cb, gb, _), (ct, gt, _) = res['plate_edges']['bot'], res['plate_edges']['top']
    Ab = idx[cb[0], cb[1], cb[2]]; At = idx[ct[0], ct[1], ct[2]]
    return {'L': cap['L'], 'b': cap['b'], 'Ab': Ab, 'gb': np.asarray(gb, np.float64), 'At': At,
            'gt': np.asarray(gt, np.float64), 'phi_direct': cap['phi'], 'idx': idx}


def junction_variant(sysd, sid, rj_ohm=PROBE_RJ_OHM):
    """`plain` 계에서 섬유 기둥마다 가운데 축방향 (z) 면 하나를 접합 간선 g_j = 1e4/R_j 로 바꾼다 (직렬 접합 꼴)."""
    from scipy import sparse
    from scipy.sparse.linalg import spsolve
    L = sysd['L'].tocsr().astype(np.float64)
    idx = sysd['idx']
    gj = 1.0e4 / float(rj_ohm)
    ui, vi, dg = [], [], []
    nx, ny, nz = sid.shape
    for i in range(nx):
        for j in range(ny):
            col = np.flatnonzero(sid[i, j, :] == 3)
            if len(col) < 4:
                continue
            km = int(col[len(col) // 2 - 1])
            u, v = int(idx[i, j, km]), int(idx[i, j, km + 1])
            if u < 0 or v < 0:
                continue
            gax = -float(L[u, v])
            ui.append(u); vi.append(v); dg.append(gj - gax)
    ui = np.asarray(ui); vi = np.asarray(vi); dg = np.asarray(dg)
    n = L.shape[0]
    D = sparse.coo_matrix((np.r_[-dg, -dg, dg, dg], (np.r_[ui, vi, ui, vi], np.r_[vi, ui, ui, vi])), shape=(n, n)).tocsr()
    L2 = (L + D).tocsr()
    out = dict(sysd)
    out['L'] = L2
    out['phi_direct'] = spsolve(L2.tocsc(), sysd['b'])
    out['n_junction'] = int(len(ui))
    return out


def probe_table(seeds=PROBE_SEEDS, rtols=PROBE_RTOLS, maxiter=PROBE_MAXITER, s3=None):
    """봉인 표 — 행마다 seed · 꼴 · rtol · info · 잔차 · 생산 술어 · σ 오차 (직접해 대비) · 판 전류 불균형 · 증서."""
    s3 = _step3_module(s3)
    rows = []
    old_mi = s3.CG_MAXITER
    s3.CG_MAXITER = int(maxiter)
    try:
        for seed in seeds:
            sid = probe_bed(seed)
            base = probe_system(sid, probe_sigma_table(), s3=s3)
            for variant, sysd in (('plain', base), ('junction', junction_variant(base, sid))):
                L, b = sysd['L'], sysd['b']
                Ib0, _ = plate_currents(sysd['phi_direct'], sysd['Ab'], sysd['gb'], sysd['At'], sysd['gt'])

                def _resolve(L_, b_, x0, rtol):
                    return s3._solve_cg(L_, b_, x0=x0, rtol=rtol)
                for rt in rtols:
                    it = [0]
                    phi, info = _cg_count(s3, L, b, rt, it)
                    resid = float(np.linalg.norm(L @ phi - b) / max(np.linalg.norm(b), 1e-30))
                    prod_ok = bool(int(info) == 0 and math.isfinite(resid) and resid <= PROD_RESID_MAX)
                    Ib, It = plate_currents(phi, sysd['Ab'], sysd['gb'], sysd['At'], sysd['gt'])
                    err = abs(Ib - Ib0) / abs(Ib0)
                    c = certify(L, b, phi, int(info), resid, rt, sysd['Ab'], sysd['gb'], sysd['At'], sysd['gt'], 1.0, _resolve)
                    rows.append({'seed': int(seed), 'variant': variant, 'rtol': float(rt), 'info': int(info),
                                 'resid': resid, 'prod_ok': prod_ok, 'sigma_err': float(err), 'imbalance': c['imbalance'],
                                 'cert_ok': c['ok'], 'pass_a': c['pass_a'], 'pass_b': c['pass_b'], 'pass_c': c['pass_c'],
                                 'dsigma_resolve': c['dsigma_rel'], 'iters': it[0],
                                 'n_dof': int(L.shape[0]), 'n_junction': int(sysd.get('n_junction', 0)),
                                 #  ★ 10-21 — ⓓ 목표량 증서 칸 (봉인 규칙 `derive_seal` 은 보지 않는다 · 기록)
                                 'pass_d': c.get('pass_d'), 'status': c.get('status'),
                                 'target_err_bound_rel': c.get('target_err_bound_rel'),
                                 'target_width_rel': c.get('target_width_rel')})
    finally:
        s3.CG_MAXITER = old_mi
    return rows


def _cg_count(s3, L, b, rt, it):
    """생산 `_solve_cg` 를 그대로 부르되 반복 수만 센다 (scipy cg 의 callback · 해는 같다)."""
    real = s3.cg

    def _wrap(A, bb, *a, **k):
        k = dict(k)
        k['callback'] = lambda xk: it.__setitem__(0, it[0] + 1)
        return real(A, bb, *a, **k)
    s3.cg = _wrap
    try:
        return s3._solve_cg(L, b, rtol=rt)
    finally:
        s3.cg = real


def derive_seal(rows, err_tol=SEAL_ERR_TOL, eps_start=SEAL_EPS_START):
    """설계 §6 절차 3 — 기계 규칙 (고르지 않는다)."""
    rts = sorted({r['rtol'] for r in rows}, reverse=True)          # 느슨한 것부터
    rtol_stop = None
    for rt in rts:
        sub = [r for r in rows if r['rtol'] == rt]
        if sub and all(r['sigma_err'] <= err_tol for r in sub):
            rtol_stop = rt
            break
    good = [r['imbalance'] for r in rows if r['sigma_err'] <= err_tol]
    bad = [r['imbalance'] for r in rows if r['sigma_err'] > err_tol]
    lo = max(good) if good else 0.0
    hi = min(bad) if bad else math.inf
    if lo < hi:
        if lo <= eps_start < hi:
            eps = eps_start
        elif math.isfinite(hi) and lo > 0.0:
            eps = math.sqrt(lo * hi)
        else:
            eps = max(lo, eps_start)
        diag_only = False
    else:
        eps, diag_only = None, True
    return {'rtol_stop': rtol_stop, 'eps_I': eps, 'interval': (lo, hi), 'b_diagnostic_only': diag_only,
            'n_rows': len(rows), 'n_good': len(good), 'n_bad': len(bad), 'err_tol': err_tol, 'eps_start': eps_start}


def main(argv=None):
    ap = argparse.ArgumentParser(description='STEP3 수렴 증서 봉인 표 (합성 직접해 대조 · 실침대 아님)')
    ap.add_argument('--table', action='store_true', help='봉인 표를 찍는다')
    a = ap.parse_args(argv)
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    if a.table:
        tab = probe_table()
        for r in tab:
            print(f"{r['variant']:9s} seed {r['seed']} rtol {r['rtol']:.0e} info {r['info']} resid {r['resid']:.2e} "
                  f"prod_ok {r['prod_ok']!s:5s} σerr {r['sigma_err']:.3e} imb {r['imbalance']:.3e} cert {r['cert_ok']} "
                  f"(a {r['pass_a']} b {r['pass_b']} c {r['pass_c']} d {r['pass_d']} · 보장 오차 {r['target_err_bound_rel']}) "
                  f"it {r['iters']}")
        print(derive_seal(tab))
    return 0


if __name__ == '__main__':
    sys.exit(main())
