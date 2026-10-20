#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rint ② S2 탄소 접합 R_j v0 (VGCF–VGCF) + S3 SDCP 접합 수정자 — 기구 (2026-10-20 · 기본 끔).

정본 = 설계 v1 `docs/reviews/rint_carbon_additive_design_v1_20261020.md` §4 (S2 v0) · §5 (S3) · 계약 v2 §3-8 J1–J8 ·
v3 §5 J2a–J12 · v3.1 (겹치면 뒤가 이긴다) · 1저자 10-20 N1–N18 = 권고대로.  시험 = `scripts/test_carbon_junction.py`.

⛔ 지위 = **기구만** (mechanism_only): R_j 는 모형 내부 보정값 (재료값 아님 · 포트 직접 간선에 반셀 없음 = RINTG-09) ·
  VGCF–VGCF 만 정량 · VA · SV · SA 면 = 옛 융합 그대로 (선언 · 필수 한정어 "SDCP–VGCF 접촉 저항 0 가정") · payload CLI 미배선 ·
  `PROTOCOL_FIELDS` 밖 · `solve_sigma_z(cjunc=None)` (기본) = 옛 경로 비트 같음.

세 단 (①′ 와 같은 꼴):
  reg  = cjunc_registry(sid, lo, vox, add_pts, add_phase, add_fid, add_kind, r_f_um=…, tol_ff_um=…, L_par_um=…, r_port_um=…)
         기하만 — 멤버십 (J1) · instance (J2a · J2c · 자기 접합) · 포트 (J3 · J4) · 면 표 (축방향 · 접합 자리 절단 · 미등록 · VX) ·
         SDCP 근접 · PTFE 덮임 · census · 지문
  plan = cjunc_plan(reg, R_j_ohm, unreg_law=…, ptfe_stamp=…, ptfe_jlaw='P0', sdcp_mod=None)
         instance 마다 간선 · 축약 (R_j′ = 0) · 절단 (P1) · 미실현 — S3: R_j′ = R_j,0·(1 − c·a_j) · c = 1 = 축약 경로
  solve_sigma_z(…, cjunc=plan) → res['cjunc'] (기록) · res['_cjunc'] (dof 수준 원장 — 시험 · 진단)

구현이 정한 것 (설계에 식이 없던 자리 · 1저자 확인 대상 — 보고에 적는다):
  L_c (접촉 길이) = 두 가닥 각각에서 **중심선 거리 ≤ r_fi + r_fj (닿음)** 인 구간 길이의 최댓값 (`CJUNC_LC_RULE`) —
    L_par = 2(r_fi + r_fj) 가 "직교 교차의 최대 닿음 길이" 와 같아지는 읽기 (직교 교차 = 배율 1 · 비스듬한 깊은 교차는 길 수 있다).
  ★ 길이 법칙 v0 (`CJUNC_LEN_LAW` · 1저자 10-20 밤 Q17 · 옛 J8 "긴 접촉 = 정량 거부" 대체): 접합 G = max(1, L_c/L_par) / R_j,0 —
    긴 접촉 = 점 접합 L_c/L_par 개 병렬 (선 접촉 협착 컨덕턴스 ∝ 길이의 1차 근사) · 새 손잡이 없음 (R_j,0 하나) · instance 하나 =
    간선 하나 (lumped · 포트 규칙 그대로 · 접촉을 따라 ceil(L_c/L_par) 간선으로 나누는 분산판 = v1 후보).  L_c ≤ L_par·(1 + 1e-9) 이면
    배율 = 정확히 1 (`junction_len_mult`) — 법칙은 경계에서 연속이라 묶음의 크기 ≤ 1e-9 상대이고, 깊은 직교 교차 (L_c = L_par) 의
    선분 길이 합 반올림 몇 ulp 가 점 접합 결과를 비트에서 바꾸지 않게 한다 (긴 접촉 표지 · 집계 = 같은 문턱).
  자기 접합 = 같은 fid 의 비연속 두 위치가 면으로 닿거나 (설계 §4-1 J1) 같은 셀을 다시 지남 (재방문) — 이웃 위치로 무리 지은 후보 하나.
    ★ 꺾임 거르기: 후보마다 두 쪽 (항목의 앞 · 뒤 위치) 셀 조각 (그 셀 닫힌 상자로 자른 중심선) 사이 **최근접점 쌍** (거리² ε 띠 ·
      띠 안 동률 = 호 길이가 작은 쪽) 의 경로 호 길이 s (fid 경로를 정준 방향으로 누적 · 조각 사이 간격 현 포함 · 점 역순 불변) ·
      s < s_min = 같은 가닥의 연속 (접합 아님 · 면 = 옛 융합 그대로 · 재방문 = 옛 셀 한 노드) · s ≥ s_min = 진짜 접힘 · 고리 접촉
      (절단 + R_j 간선 · 같은 길이 법칙).  s_min = 필수 · 기본값 없음 (None = 미등록 → 정량 거부 · 시험 모드 = 거르지 않음).
    자기 접합 L_c = 닿음 규칙을 두 쪽 셀 조각 사이에 (구현 B 의 '위치 수 × vox' 셈을 대체 — 배율이 σ 에 들어가므로 격자 셈을 쓰지 않는다).
  절단 발자국 = instance 로 묶인 **선분 쌍 run 전체** (`_footprint_segs` — 구현 B 부터 최근접 쌍만이 아니었다) · 긴 접촉의 run 위
    융합 i|j 면이 lumped 간선을 우회하지 않는다.
  포트 동률 = 정준 방향 (조각의 사전순 작은 끝에서 시작) 경로 번호가 작은 위치 (점 역순에 불변).
  교차 셀의 비탄소 면 · 판 결합 · 미등록 융합 면 = 기하 최근접 멤버십 (J9 · ε 띠 1e-9 µm² · 최근접점 → 방향 → (fid, 조각, 번호)).
"""
import hashlib
import math
import struct

import numpy as np
from scipy import ndimage, sparse

CJUNC_MODEL_VERSION = 'r3-carbon-junction-port'
CJUNC_SCHEMA = 'cjunc-v1'
CJUNC_LC_RULE = 'touch_len_max_v1'
CJUNC_SELF_LC_RULE = 'touch_len_max_cellclip_v1'   # 자기 접합 L_c — 같은 닿음 규칙 · 두 쪽 = 항목 위치들의 셀 조각
CJUNC_SELF_S_RULE = 'arc_between_nearest_points_cellclip_v1'
CJUNC_LEN_LAW = 'len_scaled_v0'            # G_j = max(1, L_c/L_par) / R_j,0 (lumped 간선 하나 · 1저자 10-20 밤 Q17)
CJUNC_PORT_RULE = 'nearest_cell_centre_within_rport_tie_canonical_seq_v1'
CJUNC_FOOTPRINT_RULE = 'owner_cells_within_D_plus_half_diag_v1'   # 발자국 선분 = instance run 전체 (`_footprint_segs` · B 와 같은 동작)
CJUNC_SELF_RULE = 'nonconsecutive_face_or_revisit_v1'
CJUNC_OWNER_RULE = 'nearest_centreline_eps_band_point_dir_lex_v1'
CJUNC_EPS_D2_UM2 = 1.0e-9                  # J9 집합 규칙 ε 띠 (거리² µm²) — 봉인 (①′ ε_p 와 같은 꼴) · 자기 접합 최근접점 띠도 같은 값
#: L_c ↔ L_par 비교의 **수치** 허용 (상대) — 깊은 직교 교차 (d0 = 0) 의 닿음 길이는 정확히 L_par = 2(r_fi + r_fj) 다.  선분 길이 합의
#:   반올림 (몇 ulp) 이 그 경계를 넘기지 않게 L_c > L_par·(1 + 이 값) 만 긴 접촉 (표지 · 집계) · 그 아래 배율 = 정확히 1 (점 접합과 비트
#:   같게) — 길이 법칙은 경계에서 연속이라 배율 쪽 묶음의 크기는 ≤ 이 값 (1e-9 상대 · 기하 뜻 없음 · 봉인).
CJUNC_LPAR_RTOL = 1.0e-9
RJ_REFERENCE_PLANE = 'model_internal_port_centre'
VGCF_R_UM = 0.075                          # 생산 VGCF Ø0.15 µm (`additives.VGCF_D`)
SDCP_R_UM = 0.15                           # SDCP 1 차 입자 Ø0.30 µm (설계 §5-1)
PTFE_R_UM = 0.124                          # PTFE rope Ø0.248 µm (설계 §3-1 (가) · 규약 선택)
UNREG_LAWS = ('cut', 'fused')
PTFE_JLAWS = ('P0', 'P1')
PTFE_STAMPS = ('off', 'face_alpha', 'centerline')
RJ_OHM_TO_CODE = 1.0e4                     # g_code [S/cm·µm] = 1e4 / R_j [Ω]  (물리 G = 1e−4 · g_code · `iface_code_G_S`)

MODE_EDGE, MODE_CONTRACT, MODE_CUT_P1, MODE_UNREALIZED, MODE_NONE_INF = 1, 2, 3, 4, 5
MODE_NAME = {MODE_EDGE: 'edge', MODE_CONTRACT: 'contract', MODE_CUT_P1: 'cut_p1', MODE_UNREALIZED: 'unrealized',
             MODE_NONE_INF: 'none_inf'}
K_AXIAL, K_VX, K_CUT_SITE, K_CUT_SELF, K_UNREG, K_SELF_FUSED = 1, 2, 3, 4, 5, 6

CJUNC_STATUS = ('mechanism_only — 탄소 접합 R_j v0 (VGCF–VGCF) · 정량 판정 = 등록 R 비준 · Codex GO · S0 문턱 개정 뒤 · '
                'payload 미배선 (B6) · 웹앱 표지 = 봉인 파일 (mpm_lab_register) 이라 보류')
CJUNC_QUALIFIERS = (
    'R_j = 모형 내부 보정값 (재료값 아님 · 포트 = 셀 중심 · 직접 간선에 반셀 · 접근 몫 없음 → 그 몫이 R_j 에 묶인다)',
    'VGCF–VGCF 만 정량 — VGCF–AM · SDCP–VGCF · SDCP–AM 면 = 옛 융합 (SDCP–VGCF 접촉 저항 0 가정)',
    'instance = 중심선 기하 근접 (관통 포함 · MPM 은 섬유 접촉 역학을 풀지 않는다) · 중심선 위치 불확도 = MPM 점 간격',
    'R_j,0 는 모든 VV instance 에 같은 값 · 접합 G = max(1, L_c/L_par)/R_j,0 (길이 법칙 v0 — 선 접촉 협착 ∝ 길이의 1차 근사 · '
    '점 접합 L_c/L_par 개 병렬 · instance 하나 = lumped 간선 하나 · 분산판 = v1 후보) · L_c = 닿음 길이 (중심선 기하 근접)',
    '꺾임 자기 접합 = 두 최근접점 사이 경로 호 길이 s < s_min 이면 접합 아님 (옛 복셀 융합 그대로) · s_min = 등록 문턱 (없으면 정량 거부)',
    'S3 c ∈ {0, 1} = 시나리오 끝 (재료 예측 아님 · c = 1 = 근접 접합 축약 끝 · 젖음 상한 아님)',
)

_TINY = 1.0e-24                            # 퇴화 선분 (길이² µm² · 1e-12 µm 미만)
_SID_NAME = {0: 'void', 1: 'AM_S', 2: 'AM_P', 3: 'VGCF', 4: 'SuperP', 5: 'SDCP', 6: 'SE', 7: 'PTFE', 8: 'SWCNT', 9: 'SE_blk'}


def junction_g_code(R_ohm):
    """접합 간선 코드 컨덕턴스 [S/cm·µm] = 1e4 / R_j [Ω] (설계 §4-1 J5 · 계약 v2 §3-5)."""
    return RJ_OHM_TO_CODE / np.asarray(R_ohm, np.float64)


def sdcp_rj_eff(R0, c, a):
    """S3 — R_j′ = R_j,0 · (1 − c · a_j) (설계 §5-1).  a ∈ {0, 1} · c ∈ [0, 1]."""
    return R0 * (1.0 - c * a)


def junction_len_mult(Lc, L_par):
    """길이 법칙 v0 (`CJUNC_LEN_LAW`) — instance 배율 m = max(1, L_c/L_par) · 접합 g_code = 1e4 · m / R_j.
    L_c ≤ L_par·(1 + `CJUNC_LPAR_RTOL`) = 정확히 1.0 (법칙은 연속 · 묶음 크기 ≤ 1e-9 상대 · 긴 접촉 없는 침대 = 점 접합과 비트 같음 —
    깊은 직교 교차의 L_c 는 L_par 보다 1–3 ulp 클 때가 많다).  NaN L_c = NaN (조용히 1 로 만들지 않는다 · 계획의 불변량이 거부)."""
    r = np.asarray(Lc, np.float64) / float(L_par)
    return np.where(np.isnan(r), np.nan, np.where(r > 1.0 + CJUNC_LPAR_RTOL, r, 1.0))


def _self_is_junction(s_um, s_min_um):
    """꺾임 자기 접합 거르기 — s ≥ s_min = 진짜 접힘 · 고리 접촉 (접합) · s < s_min = 같은 가닥의 연속 (접합 아님)."""
    return np.asarray(s_um, np.float64) >= float(s_min_um)


def _footprint_segs(inst, k):
    """J3 자리 발자국의 선분 — distinct instance k 로 묶인 선분 쌍 run 전체 (d ≤ r_fi + r_fj + tol_ff 인 쌍들의 i · j 선분).
    최근접 쌍만이면 긴 접촉 run 의 나머지 융합 i|j 면이 미등록 법칙 (fused) 으로 남아 lumped 접합 간선을 병렬로 우회한다."""
    return inst['seg_i'][k], inst['seg_j'][k]


# ═════════════════════════ 기하 원시 함수 ═════════════════════════
def _dot(a, b):
    return np.einsum('ij,ij->i', a, b)


def seg_seg_closest(P1, Q1, P2, Q2):
    """선분 P1→Q1 · P2→Q2 최근접 (Ericson 5.1.9 · 퇴화 · 평행 처리) — 배열 (m, 3) → (거리, s, t, C1, C2)."""
    P1 = np.asarray(P1, np.float64).reshape(-1, 3); Q1 = np.asarray(Q1, np.float64).reshape(-1, 3)
    P2 = np.asarray(P2, np.float64).reshape(-1, 3); Q2 = np.asarray(Q2, np.float64).reshape(-1, 3)
    d1 = Q1 - P1; d2 = Q2 - P2; r = P1 - P2
    a = _dot(d1, d1); e = _dot(d2, d2); f = _dot(d2, r); c = _dot(d1, r); bb = _dot(d1, d2)
    m = len(a)
    s = np.zeros(m); t = np.zeros(m)
    z1 = a <= _TINY; z2 = e <= _TINY
    a_ = np.where(z1, 1.0, a); e_ = np.where(z2, 1.0, e)
    k1 = z1 & ~z2
    t[k1] = np.clip(f[k1] / e_[k1], 0.0, 1.0)
    k2 = ~z1 & z2
    s[k2] = np.clip(-c[k2] / a_[k2], 0.0, 1.0)
    g = ~z1 & ~z2
    if g.any():
        den = a * e - bb * bb
        np_ = g & (den > 1.0e-14 * a * e)
        sg = np.zeros(m)
        sg[np_] = np.clip((bb[np_] * f[np_] - c[np_] * e[np_]) / den[np_], 0.0, 1.0)
        tg = (bb * sg + f) / e_
        lo = tg < 0.0; hi = tg > 1.0
        sg = np.where(lo, np.clip(-c / a_, 0.0, 1.0), np.where(hi, np.clip((bb - c) / a_, 0.0, 1.0), sg))
        tg = np.where(lo, 0.0, np.where(hi, 1.0, tg))
        s[g] = sg[g]; t[g] = tg[g]
    C1 = P1 + s[:, None] * d1; C2 = P2 + t[:, None] * d2
    return np.linalg.norm(C1 - C2, axis=1), s, t, C1, C2


def pt_seg_d2(X, A, B):
    """점 X ↔ 선분 A→B 거리² · 최근접점 · 매개 t (배열)."""
    X = np.asarray(X, np.float64).reshape(-1, 3); A = np.asarray(A, np.float64).reshape(-1, 3)
    B = np.asarray(B, np.float64).reshape(-1, 3)
    d = B - A; dd = _dot(d, d)
    t = np.where(dd > _TINY, np.clip(_dot(X - A, d) / np.where(dd > _TINY, dd, 1.0), 0.0, 1.0), 0.0)
    C = A + t[:, None] * d
    w = X - C
    return _dot(w, w), C, t


def _touch_intervals(S0, S1, Q0, Q1, T, ustar):
    """선분 S 위 점 S(u) 의 선분 Q 까지 거리 f(u) (볼록) ≤ T 인 u 구간 [ua, ub] — **안쪽 경계** (이분 60 회 · 길이를 늘리지 않는다).
    f(u*) > T 이면 (nan, nan)."""
    def f(u):
        X = S0 + u[:, None] * (S1 - S0)
        d2, _, _ = pt_seg_d2(X, Q0, Q1)
        return np.sqrt(d2)
    m = len(ustar)
    ua = np.full(m, np.nan); ub = np.full(m, np.nan)
    if m == 0:
        return ua, ub
    ok = f(ustar) <= T
    if not ok.any():
        return ua, ub
    S0o, S1o, Q0o, Q1o, us = S0[ok], S1[ok], Q0[ok], Q1[ok], ustar[ok]

    def fo(u):
        X = S0o + u[:, None] * (S1o - S0o)
        d2, _, _ = pt_seg_d2(X, Q0o, Q1o)
        return np.sqrt(d2)
    z = np.zeros(len(us)); one = np.ones(len(us))
    a_full = fo(z) <= T
    lo = z.copy(); hi = us.copy()
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        ins = fo(mid) <= T
        hi = np.where(ins, mid, hi); lo = np.where(ins, lo, mid)
    la = np.where(a_full, 0.0, hi)
    b_full = fo(one) <= T
    lo = us.copy(); hi = one.copy()
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        ins = fo(mid) <= T
        lo = np.where(ins, mid, lo); hi = np.where(ins, hi, mid)
    lb = np.where(b_full, 1.0, lo)
    ua[ok] = la; ub[ok] = lb
    return ua, ub


def _canon_dir(d):
    """선분 방향 단위 벡터 · 첫 비영 성분이 양수 (정준) — 퇴화 = 0 벡터."""
    n = np.linalg.norm(d, axis=1)
    u = np.where(n[:, None] > 0.0, d / np.where(n > 0.0, n, 1.0)[:, None], 0.0)
    first = np.where(u[:, 0] != 0.0, u[:, 0], np.where(u[:, 1] != 0.0, u[:, 1], u[:, 2]))
    return np.where((first < 0.0)[:, None], -u, u)


def fibre_pieces(Q, gap_tol):
    """같은 끊기 규칙 (`step3_sigma._fibre_segment_ijk` 의 gap_tol × 연속 점 간격 중앙값) → 점 번호 조각 목록.
    ⚠ 복제 (그 함수는 셀만 낸다) — 시험 PIECE 가 셀 집합으로 동등을 대조한다 (다른 판본이 되면 실패)."""
    Q = np.asarray(Q, np.float64)
    ar = np.arange(len(Q))
    if len(Q) < 2:
        return [ar]
    d = np.linalg.norm(np.diff(Q, axis=0), axis=1)
    med = float(np.median(d)) if len(d) else 0.0
    brk = (np.nonzero(d > gap_tol * med)[0] + 1) if med > 0 else np.array([], int)
    return np.split(ar, brk) if len(brk) else [ar]


#: 지문 (RINT-23 · 2026-10-20 2 일 차) — 같은 내용 = 같은 지문 (객체 · 프로세스 무관) · 내용 한 글자 다름 = 다른 지문.
#:   숫자 배열 = dtype · 모양 · C 순서 바이트 (옛 그대로 · 비트 유지) · 객체 배열 = 원소 **내용** 직렬화 (형 표지 · 길이 접두 · UTF-8 ·
#:   C 순서) — 옛 판은 객체 배열의 `x.data` = 원소 **포인터** 바이트를 해시했다 (원장 `instances['reason']` 의 f-문자열 사유 → 같은 입력으로
#:   다시 만든 원장 · 계획 지문이 프로세스 안 · 사이에서 갈렸다 = 거짓 거부).  내용 직렬화가 정의되지 않은 값 (임의 객체 · set — repr 에
#:   주소 · 해시 순서가 들어간다) = TypeError (조용히 주소로 지문을 만들지 않는다).
_FP_OBJ_HEADER = b'objarr-v1'
_FP_SCALARS = (str, bytes, bool, int, float, complex, type(None))
_FP_NP_KINDS = 'biufcSUMm'                 # repr 이 내용만 담는 numpy 스칼라 종류 (객체 'O' · 구조체 'V' 제외)


def _fp_len(b):
    return len(b).to_bytes(8, 'big')


def _fp_obj_item(v):
    """객체 배열 원소 하나 → 내용 바이트 (형 표지 + 길이 접두 · 문자열 = UTF-8 · 실수 = float64 큰 끝 바이트 · 중첩 = 그 `_fp`)."""
    if v is None:
        return b'N'
    if isinstance(v, (bool, np.bool_)):
        return b'T' if bool(v) else b'F'
    if isinstance(v, str):                                   # np.str_ 포함
        b = v.encode('utf-8')
        return b'S' + _fp_len(b) + b
    if isinstance(v, (bytes, bytearray)):                    # np.bytes_ 포함
        b = bytes(v)
        return b'Y' + _fp_len(b) + b
    if isinstance(v, (int, np.integer)):
        b = str(int(v)).encode('ascii')
        return b'I' + _fp_len(b) + b
    if isinstance(v, float) or (isinstance(v, np.floating) and v.dtype.itemsize <= 8):
        return b'R' + struct.pack('>d', float(v))
    if isinstance(v, (list, tuple, dict, np.ndarray)):
        return b'X' + _fp(v).encode('ascii')                 # 고정 길이 (32 hex)
    raise TypeError(f'② 탄소 접합 지문: 객체 배열 원소 형 {type(v).__name__} — 내용 직렬화가 정의되지 않았다 '
                    f'(포인터 · repr 주소로 지문을 만들지 않는다 · RINT-23) — 거부')


def _fp(*parts):
    """원장 · 계획 지문 (E5) — dict (키 정렬) · 목록 · 배열 · 스칼라.  RINT-23 규칙은 위 머리 주석."""
    h = hashlib.blake2b(digest_size=16)
    for p in parts:
        if isinstance(p, dict):
            for k in sorted(p):
                h.update(str(k).encode())
                h.update(_fp(p[k]).encode())
        elif isinstance(p, (list, tuple)):
            h.update(b'(')
            for q in p:
                h.update(_fp(q).encode())
            h.update(b')')
        elif isinstance(p, np.ndarray):
            if p.dtype.hasobject:                            # 객체 (· 구조체 객체 칸) 배열 = 내용 직렬화 (포인터 바이트 아님)
                h.update(_FP_OBJ_HEADER); h.update(repr(p.shape).encode())
                for v in p.reshape(-1, order='C'):
                    h.update(_fp_obj_item(v))
            else:
                x = np.ascontiguousarray(p)
                h.update(x.dtype.str.encode()); h.update(repr(x.shape).encode()); h.update(x.data)
        elif isinstance(p, _FP_SCALARS) or (isinstance(p, np.generic) and p.dtype.kind in _FP_NP_KINDS):
            h.update(repr(p).encode())
        else:
            raise TypeError(f'② 탄소 접합 지문: 값 형 {type(p).__name__} — 내용 직렬화가 정의되지 않았다 (repr 에 주소 · 해시 순서가 '
                            f'들어갈 수 있다 · RINT-23) — 거부')
    return h.hexdigest()


def _grid_fp(a):
    """격자 지문 — `step3_sigma._grid_fp` (사본 금지).  격자는 수치 배열 계약 — 객체 (· 구조체 객체 칸) dtype 격자는 원소 **포인터**
    바이트가 지문에 들어가 재현되지 않으므로 (RINT-23 부류) 넘기기 전에 거부한다."""
    if a is not None and np.asarray(a).dtype.hasobject:
        raise TypeError(f'② 탄소 접합: 격자 지문 — 객체 dtype ({np.asarray(a).dtype}) 격자 거부 (포인터 바이트 · RINT-23 부류 · '
                        f'격자는 수치 배열)')
    import step3_sigma as _s3
    return _s3._grid_fp(a)


# ═════════════════════════ 입력 · 경로 ═════════════════════════
def _input_check(add_pts, add_phase, add_fid, add_kind):
    if add_kind is None:
        raise ValueError('② 탄소 접합: 경로 의미 (`<fibre>_kind.npy`) 없음 — 연속 중심선 (MPM 끝 점 + fibre.npy + kind) 없는 침대 = 거부 '
                         '(점 · 복셀 인접으로 대신하지 않는다 · 설계 §4-2)')
    P = np.asarray(add_pts)
    PH = np.asarray(add_phase); F = np.asarray(add_fid); K = np.asarray(add_kind)
    if P.ndim != 2 or P.shape[1] != 3:
        raise ValueError(f'② 탄소 접합: 점 배열 모양 {P.shape} (N, 3) 이 아니다')
    n = len(P)
    if not (PH.shape == (n,) and F.shape == (n,) and K.shape == (n,)):
        raise ValueError(f'② 탄소 접합: 길이 불일치 — 점 {n} · phase {PH.shape} · fid {F.shape} · kind {K.shape} (조용한 강등 없음 · RIMPR-01)')
    if P.dtype.kind not in 'fiu' or not np.issubdtype(PH.dtype, np.integer) or not np.issubdtype(F.dtype, np.integer) \
            or not np.issubdtype(K.dtype, np.integer):
        raise ValueError('② 탄소 접합: 좌표 = 수치 · phase · fid · kind = 정수 배열 (텍스트 토큰 없음)')
    P = P.astype(np.float64)
    if not np.isfinite(P).all():
        raise ValueError('② 탄소 접합: 좌표 비유한 (NaN · ±inf) — 조립 전 거부 (RIMPR-02 · 04)')
    return P, PH.astype(np.int64), F.astype(np.int64), K.astype(np.int64)


def _paths_of(P, PH, F, K, phase, rej, label):
    """phase 의 fid 마다 행 (붙어 있어야 한다 · 정확 중복 경로 = 거부)."""
    out = []
    m = PH == phase
    if not m.any():
        return out
    sig = {}
    nc, mixed = [], []
    for f in np.unique(F[m]):
        r = np.flatnonzero(F == f)
        if not np.all(PH[r] == phase):
            mixed.append(int(f))
            r = r[PH[r] == phase]
        if len(r) > 1 and np.any(np.diff(r) != 1):
            nc.append(int(f))
        kind_path = bool(np.all(K[r] == 1))
        key = (len(r), P[r].tobytes())
        sig.setdefault(key, []).append(int(f))
        out.append((int(f), r, kind_path))
    if nc:
        rej.append({'code': 'fid_noncontiguous', 'test': 'S0-5', 'n': len(nc), 'detail': nc[:8], 'phase': label,
                    'why': '같은 fid 의 행이 떨어진 두 블록 — 경로 순서가 모호 (설계 §2 ③ · §3-3)'})
    if mixed:
        rej.append({'code': 'fid_phase_mixed', 'n': len(mixed), 'detail': mixed[:8], 'phase': label,
                    'why': '한 fid 가 두 상에 걸친다 (전역 고유 fid 규약 위반)'})
    dup = [v for v in sig.values() if len(v) > 1]
    if dup:
        rej.append({'code': 'duplicate_path', 'n': len(dup), 'detail': dup[:8], 'phase': label,
                    'why': '정확 중복 경로 (점 배열 비트 같음) — 병합 규칙 미등록'})
    return out


def _segments_of(paths, P, gap_tol):
    """경로 → 조각 (정준 방향) → 선분 표.  → dict(arrays) · 조각마다 (fid, 점 배열).
    arc_a · arc_b = 선분 두 끝의 **경로 호 좌표** (꺾임 자기 접합 s) — fid 경로 전체를 정준 방향 (사전순 작은 끝에서) 으로 놓고 연속 점
    거리를 누적 (조각 사이 간격 현 포함) · 점 역순 입력에서도 같은 비트.  선분 위 호 좌표 = arc_a + t·(arc_b − arc_a)."""
    sP0, sP1, sfid, spiece, sk, sa0, sa1 = [], [], [], [], [], [], []
    pieces = []
    for f, r, kind_path in paths:
        Q = P[r]
        flip = bool(kind_path and len(Q) > 1 and tuple(Q[-1]) < tuple(Q[0]))
        Qc = Q[::-1] if flip else Q
        cum = (np.r_[0.0, np.cumsum(np.linalg.norm(np.diff(Qc, axis=0), axis=1))] if (kind_path and len(Q) > 1)
               else np.zeros(len(Q)))
        arc_of = cum[::-1] if flip else cum                  # 원래 점 번호 → 호 좌표
        for ix in (fibre_pieces(Q, gap_tol) if kind_path else [np.arange(len(Q))]):
            R = Q[ix]
            ixo = ix
            if kind_path and len(R) > 1 and tuple(R[-1]) < tuple(R[0]):
                R = R[::-1]
                ixo = ix[::-1]
            gp = len(pieces)
            pieces.append((f, R, kind_path))
            if len(R) == 1 or not kind_path:
                A = R; B = R                                  # 점 = 퇴화 선분 (경로 아닌 fid 도 점마다)
                a0 = arc_of[ixo]; a1 = arc_of[ixo]
            else:
                A = R[:-1]; B = R[1:]
                a0 = arc_of[ixo[:-1]]; a1 = arc_of[ixo[1:]]
            sP0.append(A); sP1.append(B); sa0.append(a0); sa1.append(a1)
            sfid.append(np.full(len(A), f)); spiece.append(np.full(len(A), gp)); sk.append(np.arange(len(A)))
    if not pieces:
        z = np.zeros((0, 3))
        return {'P0': z, 'P1': z.copy(), 'fid': np.zeros(0, np.int64), 'piece': np.zeros(0, np.int64),
                'k': np.zeros(0, np.int64), 'arc_a': np.zeros(0), 'arc_b': np.zeros(0)}, pieces
    return {'P0': np.vstack(sP0), 'P1': np.vstack(sP1), 'fid': np.concatenate(sfid).astype(np.int64),
            'piece': np.concatenate(spiece).astype(np.int64), 'k': np.concatenate(sk).astype(np.int64),
            'arc_a': np.concatenate(sa0).astype(np.float64), 'arc_b': np.concatenate(sa1).astype(np.float64)}, pieces


def _positions(pieces, segs, lo, vox, n, sid):
    """조각 → 셀 열 (연속 중복 제거 · 정준 방향 번호) = 멤버십 위치.  생산 스탬프와 같은 원시 함수 (`segment_cells`) · 같은 셀."""
    from fibre_segment_raster import segment_cells
    pf, pp, pk, plin, pijk, ps0, ps1 = [], [], [], [], [], [], []
    seg_base = 0
    piece_pos = []
    npos = 0                                                 # 지금까지 위치 수 (조각마다 [시작, 끝) — 누적 · O(조각))
    for gp, (f, R, kind_path) in enumerate(pieces):
        nseg = 1 if (len(R) == 1 or not kind_path) else len(R) - 1
        if not kind_path:
            seg_base += len(R)
            piece_pos.append((npos, npos))
            continue
        if len(R) == 1:
            cells = np.floor((R - lo) / vox).astype(np.int64)
            sidx = np.zeros(1, np.int64)
        else:
            cl, si = [], []
            for i in range(len(R) - 1):
                c = segment_cells(R[i] - lo, R[i + 1] - lo, vox)
                cl.append(c); si.append(np.full(len(c), i))
            cells = np.vstack(cl).astype(np.int64); sidx = np.concatenate(si)
        new = np.ones(len(cells), bool)
        new[1:] = np.any(cells[1:] != cells[:-1], axis=1)
        grp = np.cumsum(new) - 1
        ng = int(grp[-1]) + 1
        cu = cells[new]
        s0 = np.full(ng, np.iinfo(np.int64).max); s1 = np.full(ng, -1)
        np.minimum.at(s0, grp, sidx); np.maximum.at(s1, grp, sidx)
        inb = ((cu >= 0) & (cu < n)).all(1)
        lin = np.full(ng, -1, np.int64)
        lin[inb] = np.ravel_multi_index(tuple(cu[inb].T), tuple(n))
        pf.append(np.full(ng, f)); pp.append(np.full(ng, gp)); pk.append(np.arange(ng)); plin.append(lin)
        pijk.append(cu); ps0.append(s0 + seg_base); ps1.append(s1 + seg_base)
        piece_pos.append((npos, npos + ng))
        npos += ng
        seg_base += nseg
    if pf:
        pos = {'fid': np.concatenate(pf).astype(np.int64), 'piece': np.concatenate(pp).astype(np.int64),
               'k': np.concatenate(pk).astype(np.int64), 'lin': np.concatenate(plin).astype(np.int64),
               'ijk': np.vstack(pijk).astype(np.int64), 's0': np.concatenate(ps0).astype(np.int64),
               's1': np.concatenate(ps1).astype(np.int64)}
    else:
        z = np.zeros(0, np.int64)
        pos = {'fid': z, 'piece': z.copy(), 'k': z.copy(), 'lin': z.copy(), 'ijk': np.zeros((0, 3), np.int64),
               's0': z.copy(), 's1': z.copy()}
    flat = np.asarray(sid).reshape(-1)
    pos['live'] = (pos['lin'] >= 0) & (flat[np.maximum(pos['lin'], 0)] == 3)
    return pos, piece_pos


def _owner_select(qid, pid, X, pos, segs, nq):
    """J9 집합 규칙 — 질의마다 후보 위치 중 중심선 최근접 (거리² ε 띠 · 정준 키 = 최근접점 → 방향 → (fid, 조각, 번호)).
    qid/pid = 후보 쌍 (질의 번호 · 위치 번호) · X = 질의 점 (nq, 3).  → owner (nq,) · 정준 키 못 가른 수."""
    owner = np.full(nq, -1, np.int64)
    if len(qid) == 0:
        return owner, 0
    cnt = pos['s1'][pid] - pos['s0'][pid] + 1
    rq = np.repeat(np.arange(len(qid)), cnt)
    off = np.arange(len(rq)) - np.repeat(np.cumsum(cnt) - cnt, cnt)
    sg = np.repeat(pos['s0'][pid], cnt) + off
    d2, C, _ = pt_seg_d2(X[qid[rq]], segs['P0'][sg], segs['P1'][sg])
    order = np.lexsort((d2, rq))
    first = np.ones(len(order), bool); first[1:] = rq[order][1:] != rq[order][:-1]
    best = order[first]                                      # 쌍마다 최근접 선분
    bd2 = d2[best]; bC = C[best]; bdir = _canon_dir(segs['P1'][sg[best]] - segs['P0'][sg[best]])
    q = qid; p = pid
    dmin = np.full(nq, np.inf)
    np.minimum.at(dmin, q, bd2)
    band = bd2 <= dmin[q] + CJUNC_EPS_D2_UM2
    keys = (pos['k'][p], pos['piece'][p], pos['fid'][p], bdir[:, 2], bdir[:, 1], bdir[:, 0], bC[:, 2], bC[:, 1], bC[:, 0],
            ~band, q)
    o = np.lexsort(keys)
    fq = np.ones(len(o), bool); fq[1:] = q[o][1:] != q[o][:-1]
    owner[q[o][fq]] = p[o][fq]
    # 정준 키 (점 · 방향) 가 못 가른 띠 안 동률 = (fid, 조각, 번호) 대체 — 수만 센다 (질의마다 첫째 · 둘째 후보)
    tie = 0
    sec = np.flatnonzero(~fq)
    if len(sec):
        prev = sec - 1
        qo = q[o]; bo = band[o]
        geo = np.c_[bC[o], bdir[o]]
        tie = int(np.sum(fq[prev] & (qo[sec] == qo[prev]) & bo[sec] & bo[prev] & np.all(geo[sec] == geo[prev], axis=1)))
    return owner, tie


class _UF:
    def __init__(self):
        self.p = {}

    def find(self, x):
        p = self.p
        p.setdefault(x, x)
        r = x
        while p[r] != r:
            r = p[r]
        while p[x] != r:
            p[x], x = r, p[x]
        return r

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            if rb < ra:
                ra, rb = rb, ra
            self.p[rb] = ra


# ═════════════════════════ 원장 (기하만) ═════════════════════════
def cjunc_registry(sid, box_lo, vox, add_pts, add_phase, add_fid, add_kind, *, r_f_um, tol_ff_um, L_par_um, r_port_um,
                   s_min_um, gap_tol=2.0, tol_P_um=None, tol_sj_um=None, r_ptfe_um=PTFE_R_UM, r_sdcp_um=SDCP_R_UM):
    """② 탄소 접합 원장 — **기하만** (σ · 전류 없음).  문턱 = 식 고정 · 숫자 = S0 단계 1 (설계 §4-1 · R §2-1) — 기본값을 두지 않는다
    (r_f · tol_ff · L_par · r_port · s_min 필수).  tol_P · tol_sj 기본 = tol_ff (설계: 한 숫자).  → dict (지문 포함).
    s_min_um = 꺾임 자기 접합 거르기 문턱 (경로 호 길이 µm) — None = 미등록 (구조화 거부 `self_s_min_missing` · 정량 계획이 막는다 ·
    시험 모드는 거르지 않고 진행 · 표지 `off_s_min_missing`)."""
    sid = np.asarray(sid)
    if sid.ndim != 3:
        raise ValueError('② 탄소 접합: sid 는 3 차원 격자')
    vox = float(vox)
    lo = np.asarray(box_lo, np.float64).reshape(3)
    if not (math.isfinite(vox) and vox > 0.0 and np.isfinite(lo).all()):
        raise ValueError(f'② 탄소 접합: vox · 상자 원점 유한 (vox > 0) — {vox!r} {lo!r}')
    thr = {'r_f_um': r_f_um, 'tol_ff_um': tol_ff_um, 'L_par_um': L_par_um, 'r_port_um': r_port_um, 'gap_tol': gap_tol,
           'tol_P_um': tol_ff_um if tol_P_um is None else tol_P_um, 'tol_sj_um': tol_ff_um if tol_sj_um is None else tol_sj_um,
           'r_ptfe_um': r_ptfe_um, 'r_sdcp_um': r_sdcp_um}
    for k_, v_ in thr.items():
        if isinstance(v_, bool) or not isinstance(v_, (int, float, np.floating, np.integer)) or not math.isfinite(float(v_)) \
                or float(v_) < 0.0:
            raise ValueError(f'② 탄소 접합: 문턱 {k_} = {v_!r} — 유한한 0 이상 실수 (R §2-1 · 숫자 = S0 단계 1)')
    thr = {k_: float(v_) for k_, v_ in thr.items()}
    if thr['r_f_um'] <= 0.0 or thr['gap_tol'] <= 0.0:
        raise ValueError('② 탄소 접합: r_f · gap_tol > 0')
    if thr['L_par_um'] <= 0.0:
        raise ValueError('② 탄소 접합: L_par > 0 (길이 법칙 v0 의 분모 · 배율 = max(1, L_c/L_par))')
    if s_min_um is not None and (isinstance(s_min_um, bool) or not isinstance(s_min_um, (int, float, np.floating, np.integer))
                                 or not math.isfinite(float(s_min_um)) or float(s_min_um) < 0.0):
        raise ValueError(f'② 탄소 접합: s_min = {s_min_um!r} — None (미등록 · 정량 거부) 또는 유한한 0 이상 실수 '
                         f'(꺾임 자기 접합 경로 호 길이 µm · 숫자 = S0 단계 1 뒤 R §2-1)')
    thr['s_min_um'] = None if s_min_um is None else float(s_min_um)
    P, PH, F, K = _input_check(add_pts, add_phase, add_fid, add_kind)
    n = np.array(sid.shape, np.int64)
    rej = []
    vg_paths = _paths_of(P, PH, F, K, 2, rej, 'VGCF')
    nonpath = [f for f, _, kp in vg_paths if not kp]
    if nonpath:
        rej.append({'code': 'vgcf_nonpath_fid', 'n': len(nonpath), 'detail': nonpath[:8],
                    'why': 'VGCF fid 가 경로 (kind 1) 가 아니다 — 점 스탬프 VGCF 는 중심선이 없다 (설계 §4-2 · 거부)'})
    vg_paths_ok = [(f, r, kp) for f, r, kp in vg_paths if kp]
    segs, pieces = _segments_of(vg_paths_ok, P, thr['gap_tol'])
    pos, piece_pos = _positions(pieces, segs, lo, vox, n, sid)
    flat = sid.reshape(-1)
    # 위치 정렬 (셀 → 멤버십 · 정준 순서) · 주 위치 (셀의 기본 dof)
    live = np.flatnonzero(pos['live'])
    o = live[np.lexsort((pos['k'][live], pos['piece'][live], pos['fid'][live], pos['lin'][live]))]
    primary = np.zeros(len(pos['lin']), bool)
    if len(o):
        fl = np.ones(len(o), bool); fl[1:] = pos['lin'][o][1:] != pos['lin'][o][:-1]
        primary[o[fl]] = True
    pos['primary'] = primary
    cell_lin, cell_cnt = (np.unique(pos['lin'][o], return_counts=True) if len(o) else
                          (np.zeros(0, np.int64), np.zeros(0, np.int64)))
    cell_ptr = np.r_[0, np.cumsum(cell_cnt)].astype(np.int64)
    cell_pos = o
    s3cells = np.flatnonzero(flat == 3)
    orphan = np.setdiff1d(s3cells, cell_lin, assume_unique=False)
    if len(orphan):
        rej.append({'code': 'vgcf_orphan_cells', 'n': int(len(orphan)),
                    'why': '멤버십 없는 VGCF 셀 (점 스탬프 · SDCP–VGCF 브리지 진단 팔 · 다른 입력) — 정량 거부'})
    n_extra = int(np.sum(pos['live'] & ~primary))

    def _cell_positions(lins):
        """셀 선형 번호들 → (질의 번호, 위치 번호) 쌍 (그 셀의 살아있는 위치 전부)."""
        j = np.searchsorted(cell_lin, lins)
        okj = (j < len(cell_lin))
        okj[okj] = cell_lin[j[okj]] == lins[okj]
        q = np.flatnonzero(okj)
        a0 = cell_ptr[j[q]]; cnt = cell_ptr[j[q] + 1] - a0
        qq = np.repeat(q, cnt)
        off = np.arange(len(qq)) - np.repeat(np.cumsum(cnt) - cnt, cnt)
        return qq, cell_pos[np.repeat(a0, cnt) + off]

    # ── distinct-fiber instances (J2a · J2c) ──
    rf = thr['r_f_um']
    D = 2.0 * rf + thr['tol_ff_um']
    T_touch = 2.0 * rf
    inst = _distinct_instances(segs, D, T_touch)
    # ── 면 표 ──
    stride = np.array([n[1] * n[2], n[2], 1], np.int64)
    rows_lin, rows_ax, rows_kind, rows_pa, rows_pb, rows_inst = [], [], [], [], [], []
    contact = []                                             # (lin_a, ax, oa, ob)
    owner_ties = 0
    for ax in range(3):
        sa = [slice(None)] * 3; sb = [slice(None)] * 3
        sa[ax] = slice(0, -1); sb[ax] = slice(1, None)
        g3 = sid[tuple(sa)] == 3; h3 = sid[tuple(sb)] == 3
        cand = g3 | h3
        if not cand.any():
            continue
        ii = np.nonzero(cand)
        la = np.ravel_multi_index(ii, tuple(n)).astype(np.int64)
        lb = la + stride[ax]
        fc = lo + (np.stack(ii, 1).astype(np.float64) + 0.5) * vox
        fc[:, ax] += 0.5 * vox                               # 면 중심
        qa, pa_all = _cell_positions(la)
        qb, pb_all = _cell_positions(lb)
        has_a = np.zeros(len(la), bool); has_a[qa] = True
        has_b = np.zeros(len(lb), bool); has_b[qb] = True
        # 축방향 쌍 (같은 fid · 조각 · 번호 차 1)
        vv = has_a & has_b
        axial_face = np.zeros(len(la), bool)
        if vv.any():
            # 면마다 a 위치 × b 위치 펼치기
            ca = np.bincount(qa, minlength=len(la)); cb = np.bincount(qb, minlength=len(la))
            sa_ = np.r_[0, np.cumsum(ca)]; sb_ = np.r_[0, np.cumsum(cb)]
            fv = np.flatnonzero(vv)
            na = ca[fv]; nb = cb[fv]
            rep = na * nb
            face_r = np.repeat(fv, rep)
            off = np.arange(len(face_r)) - np.repeat(np.cumsum(rep) - rep, rep)
            ia = off // np.repeat(nb, rep); ib = off % np.repeat(nb, rep)
            PA = pa_all[np.argsort(qa, kind='stable')][sa_[face_r] + ia]
            PB = pb_all[np.argsort(qb, kind='stable')][sb_[face_r] + ib]
            isax = (pos['fid'][PA] == pos['fid'][PB]) & (pos['piece'][PA] == pos['piece'][PB]) \
                & (np.abs(pos['k'][PA] - pos['k'][PB]) == 1)
            if isax.any():
                axial_face[face_r[isax]] = True
                rows_lin.append(la[face_r[isax]]); rows_ax.append(np.full(int(isax.sum()), ax))
                rows_kind.append(np.full(int(isax.sum()), K_AXIAL)); rows_pa.append(PA[isax]); rows_pb.append(PB[isax])
                rows_inst.append(np.full(int(isax.sum()), -1))
        # 접촉 면 (VV · 축방향 쌍 없음) · VX 면 (한쪽만 멤버십)
        need_a = (has_a & ~axial_face)
        need_b = (has_b & ~axial_face)
        sel_a = np.isin(qa, np.flatnonzero(need_a)); sel_b = np.isin(qb, np.flatnonzero(need_b))
        oa, ta = _owner_select(qa[sel_a], pa_all[sel_a], fc, pos, segs, len(la))
        ob, tb = _owner_select(qb[sel_b], pb_all[sel_b], fc, pos, segs, len(la))
        owner_ties += ta + tb
        cf = np.flatnonzero(vv & ~axial_face)
        for i in cf:
            contact.append((int(la[i]), ax, int(oa[i]), int(ob[i]), fc[i]))
        vx = np.flatnonzero(has_a ^ has_b)                    # 한쪽만 멤버십 (VGCF ↔ 비탄소 · 고아 VGCF 셀) — 축방향일 수 없다
        if len(vx):
            rows_lin.append(la[vx]); rows_ax.append(np.full(len(vx), ax)); rows_kind.append(np.full(len(vx), K_VX))
            rows_pa.append(np.where(has_a[vx], oa[vx], -1)); rows_pb.append(np.where(has_b[vx], ob[vx], -1))
            rows_inst.append(np.full(len(vx), -1))
    # ── 접촉 면 분류: 자기 · 접합 자리 절단 · 미등록 ──
    D_fp = D + math.sqrt(3.0) * 0.5 * vox
    by_pair = {}
    for k in range(len(inst['fi'])):
        by_pair.setdefault((int(inst['fi'][k]), int(inst['fj'][k])), []).append(k)
    self_items = []
    n_cut_site = 0
    n_unreg = 0
    multi_site = 0
    for (lin_a, ax, oa_, ob_, fcen) in contact:
        if oa_ < 0 or ob_ < 0:
            continue
        fa, fb = int(pos['fid'][oa_]), int(pos['fid'][ob_])
        if fa == fb:
            self_items.append((oa_, ob_, lin_a, ax, 1))
            continue
        key = (min(fa, fb), max(fa, fb))
        ca = lo + (np.array(np.unravel_index(lin_a, tuple(n)), np.float64) + 0.5) * vox
        cb_ = ca.copy(); cb_[ax] += vox
        best, bestd = -1, math.inf
        nmatch = 0
        for k in by_pair.get(key, ()):
            Si, Sj = _footprint_segs(inst, k)                # run 전체 (긴 접촉 = lumped 간선 · run 위 면이 남으면 우회)
            seg_of_fa = Si if int(inst['fi'][k]) == fa else Sj
            seg_of_fb = Sj if int(inst['fi'][k]) == fa else Si
            da = float(np.sqrt(np.min(pt_seg_d2(np.repeat(ca[None], len(seg_of_fb), 0), segs['P0'][seg_of_fb],
                                                segs['P1'][seg_of_fb])[0])))
            db = float(np.sqrt(np.min(pt_seg_d2(np.repeat(cb_[None], len(seg_of_fa), 0), segs['P0'][seg_of_fa],
                                                segs['P1'][seg_of_fa])[0])))
            if da <= D_fp and db <= D_fp:
                nmatch += 1
                if da + db < bestd:
                    best, bestd = k, da + db
        if best >= 0:
            multi_site += int(nmatch > 1)
            rows_lin.append(np.array([lin_a])); rows_ax.append(np.array([ax])); rows_kind.append(np.array([K_CUT_SITE]))
            rows_pa.append(np.array([oa_])); rows_pb.append(np.array([ob_])); rows_inst.append(np.array([best]))
            n_cut_site += 1
        else:
            rows_lin.append(np.array([lin_a])); rows_ax.append(np.array([ax])); rows_kind.append(np.array([K_UNREG]))
            rows_pa.append(np.array([oa_])); rows_pb.append(np.array([ob_])); rows_inst.append(np.array([-1]))
            n_unreg += 1
    # 재방문 (같은 셀 · 같은 fid · 비연속)
    for c_i in range(len(cell_lin)):
        mem = cell_pos[cell_ptr[c_i]:cell_ptr[c_i + 1]]
        if len(mem) < 2:
            continue
        for x in range(len(mem)):
            for y in range(x + 1, len(mem)):
                if pos['fid'][mem[x]] == pos['fid'][mem[y]]:
                    self_items.append((int(mem[x]), int(mem[y]), int(cell_lin[c_i]), -1, 0))
    selfcand, self_face_inst, self_groups, self_norm = _self_instances(self_items, pos, vox)
    # ── 꺾임 자기 접합 거르기 (s = 두 최근접점 사이 경로 호 길이 · s < s_min = 같은 가닥의 연속) · 자기 L_c (닿음) ──
    s_arc, s_lc = _self_geometry(self_groups, self_norm, pos, segs, lo, vox, T_touch)
    ncand = len(selfcand)
    if thr['s_min_um'] is None:
        keep = np.ones(ncand, bool)
        self_filter = 'off_s_min_missing'
        rej.append({'code': 'self_s_min_missing', 'test': 'J8-self', 'n': int(ncand),
                    'why': 's_min (꺾임 자기 접합 거르기 · 경로 호 길이) 미등록 — 숫자 = S0 단계 1 의 분포를 본 뒤 등록 R §2-1 개정 · '
                           '기본값 없음 (시험 모드 = 거르지 않고 진행)'})
    else:
        filt = np.asarray(_self_is_junction(s_arc, thr['s_min_um']), bool).reshape(ncand)
        keep = np.where(np.isfinite(s_arc), filt, True)     # 셀 조각이 없어 s 를 못 잰 후보 = 접합 그대로 (수 기록)
        self_filter = 'applied'
    kidx = np.cumsum(keep) - 1
    self_merge = []
    n_self_fused = 0
    for it_idx, (pa_, pb_, lin_a, ax, isface) in enumerate(self_items):
        g_ = self_face_inst[it_idx]
        if keep[g_]:
            if isface:
                rows_lin.append(np.array([lin_a])); rows_ax.append(np.array([ax])); rows_kind.append(np.array([K_CUT_SELF]))
                rows_pa.append(np.array([pa_])); rows_pb.append(np.array([pb_]))
                rows_inst.append(np.array([len(inst['fi']) + int(kidx[g_])]))
        elif isface:                                          # 같은 가닥의 연속 — 면 = 옛 융합 그대로 (접합 · 절단 아님)
            rows_lin.append(np.array([lin_a])); rows_ax.append(np.array([ax])); rows_kind.append(np.array([K_SELF_FUSED]))
            rows_pa.append(np.array([pa_])); rows_pb.append(np.array([pb_])); rows_inst.append(np.array([-1]))
            n_self_fused += 1
        else:                                                 # 같은 가닥의 연속 재방문 — 옛 셀 한 노드 (두 위치 합침)
            self_merge.append((int(pa_), int(pb_)))
    selfinst = []
    for g_ in np.flatnonzero(keep):
        d_ = dict(selfcand[g_])
        d_['Lc'] = float(s_lc[g_])
        d_['s'] = float(s_arc[g_])
        selfinst.append(d_)
    fin = s_arc[np.isfinite(s_arc)]
    self_census = {'self_filter': self_filter, 'n_self_candidates': int(ncand), 'n_self_kept': int(np.sum(keep)),
                   'n_self_filtered': int(ncand - np.sum(keep)), 'n_self_s_undefined': int(ncand - len(fin)),
                   'n_self_fused_faces': int(n_self_fused), 'n_self_merged_revisits': int(len(self_merge)),
                   'self_s_um': ({'min': float(fin.min()), 'median': float(np.median(fin)), 'max': float(fin.max())}
                                 if len(fin) else None)}
    # ── instance 합치기 (distinct + self) · 포트 ──
    allinst = _merge_instances(inst, selfinst, segs)
    ports = _ports(allinst, pos, piece_pos, segs, lo, vox, n, flat, thr['r_port_um'])
    allinst.update(ports)
    # ── SDCP 근접 · PTFE 덮임 ──
    cp = allinst['cp']
    nI = len(allinst['fi'])
    a_sdcp = np.zeros(nI, bool)
    sd = P[PH == 5]
    if nI and len(sd):
        from scipy.spatial import cKDTree
        dd, _ = cKDTree(sd).query(cp)
        a_sdcp = (dd - thr['r_sdcp_um']) <= thr['tol_sj_um']
    ptfe_cov = np.zeros(nI, bool)
    pt_paths = _paths_of(P, PH, F, K, 4, rej, 'PTFE')
    psegs, _ = _segments_of(pt_paths, P, thr['gap_tol'])
    if nI and len(psegs['P0']):
        lim = thr['r_ptfe_um'] + rf + thr['tol_P_um']
        for k in range(nI):
            d2, _, _ = pt_seg_d2(np.repeat(cp[k][None], len(psegs['P0']), 0), psegs['P0'], psegs['P1'])
            ptfe_cov[k] = math.sqrt(float(np.min(d2))) <= lim
    allinst['a_sdcp'] = a_sdcp
    allinst['ptfe_cov'] = ptfe_cov
    allinst['long'] = allinst['Lc'] > thr['L_par_um'] * (1.0 + CJUNC_LPAR_RTOL)   # 긴 접촉 표지 (집계 · 거부 아님) — 원장에서 한 번
    allinst['mult'] = np.asarray(junction_len_mult(allinst['Lc'], thr['L_par_um']), np.float64).reshape(nI)   # 길이 법칙 v0
    # ── 면 표 정렬 ──
    if rows_lin:
        ft = {'lin': np.concatenate(rows_lin).astype(np.int64), 'ax': np.concatenate(rows_ax).astype(np.int64),
              'kind': np.concatenate(rows_kind).astype(np.int64), 'pa': np.concatenate(rows_pa).astype(np.int64),
              'pb': np.concatenate(rows_pb).astype(np.int64), 'inst': np.concatenate(rows_inst).astype(np.int64)}
        oo = np.lexsort((ft['pb'], ft['pa'], ft['kind'], ft['ax'], ft['lin']))
        ft = {k_: v_[oo] for k_, v_ in ft.items()}
    else:
        z = np.zeros(0, np.int64)
        ft = {'lin': z, 'ax': z.copy(), 'kind': z.copy(), 'pa': z.copy(), 'pb': z.copy(), 'inst': z.copy()}
    ft['key'] = ft['lin'] * 3 + ft['ax']
    # ── census ──
    census = _census(allinst, pos, ft, cell_lin, cell_ptr, sid, flat, owner_ties, multi_site, n_cut_site, n_unreg, segs,
                     len(vg_paths_ok), len(pieces), rf)
    census.update(_sdcp_bridging(sid, ft, pos, n))
    census.update(self_census)
    reg = {'kind': 'cjunc_registry', 'version': CJUNC_MODEL_VERSION, 'schema': CJUNC_SCHEMA, 'vox': vox, 'lo': lo,
           'shape': tuple(int(x) for x in n), 'thresholds': thr,
           'rules': {'lc': CJUNC_LC_RULE, 'port': CJUNC_PORT_RULE, 'footprint': CJUNC_FOOTPRINT_RULE, 'self': CJUNC_SELF_RULE,
                     'owner': CJUNC_OWNER_RULE, 'eps_d2_um2': CJUNC_EPS_D2_UM2, 'lpar_rtol': CJUNC_LPAR_RTOL,
                     'len_law': CJUNC_LEN_LAW, 'self_lc': CJUNC_SELF_LC_RULE, 'self_s': CJUNC_SELF_S_RULE},
           'positions': pos, 'segments': segs, 'instances': allinst, 'faces': ft, 'cell_lin': cell_lin,
           'cell_ptr': cell_ptr, 'cell_pos': cell_pos, 'n_extra_dofs': n_extra,
           'self_merge': np.asarray(self_merge, np.int64).reshape(-1, 2), 'rejections': rej, 'census': census}
    reg['fp'] = {'sid': _grid_fp(sid), 'centreline': _fp(segs), 'membership': _fp(pos), 'registry': registry_fp(reg)}
    return reg


def registry_fp(reg):
    """원장 지문 (E5) — 기하 · 문턱 · 규칙 · 표 전부 (만든 뒤 바뀐 원장 = 계획 거부)."""
    return _fp(reg['vox'], reg['lo'], reg['shape'], reg['thresholds'], reg['rules'], reg['positions'], reg['segments'],
               reg['instances'], reg['faces'], reg['cell_lin'], reg['cell_ptr'], reg['cell_pos'], reg['n_extra_dofs'],
               reg['self_merge'], [x['code'] for x in reg['rejections']])


def _distinct_instances(segs, D, T):
    """J2a · J2c — 서로 다른 fid 선분 쌍 중 최근접 ≤ D · 같은 조각 이웃 선분끼리 이어진 쌍 = instance 하나."""
    P0, P1 = segs['P0'], segs['P1']
    ns = len(P0)
    empty = {'fi': np.zeros(0, np.int64), 'fj': np.zeros(0, np.int64), 'self': np.zeros(0, bool), 'd0': np.zeros(0),
             'Lc': np.zeros(0), 'Ci': np.zeros((0, 3)), 'Cj': np.zeros((0, 3)), 'seg_i': [], 'seg_j': [],
             'piece_i': np.zeros(0, np.int64), 'piece_j': np.zeros(0, np.int64), 'si_min': np.zeros(0, np.int64),
             'sj_min': np.zeros(0, np.int64)}
    if ns < 2:
        return empty
    from scipy.spatial import cKDTree
    mid = 0.5 * (P0 + P1)
    half = 0.5 * np.linalg.norm(P1 - P0, axis=1)
    rad = 2.0 * float(half.max()) + D
    pr = cKDTree(mid).query_pairs(rad, output_type='ndarray')
    if len(pr) == 0:
        return empty
    i, j = pr[:, 0], pr[:, 1]
    keep = segs['fid'][i] != segs['fid'][j]
    i, j = i[keep], j[keep]
    if len(i) == 0:
        return empty
    sw = segs['fid'][i] > segs['fid'][j]
    i, j = np.where(sw, j, i), np.where(sw, i, j)
    d, s, t, C1, C2 = seg_seg_closest(P0[i], P1[i], P0[j], P1[j])
    close = d <= D
    i, j, d, s, t, C1, C2 = i[close], j[close], d[close], s[close], t[close], C1[close], C2[close]
    if len(i) == 0:
        return empty
    uf = _UF()
    keyof = {}
    pi_, pj_ = segs['piece'], segs['piece']
    for x in range(len(i)):
        keyof[(int(pi_[i[x]]), int(segs['k'][i[x]]), int(pj_[j[x]]), int(segs['k'][j[x]]))] = x
    for x in range(len(i)):
        a0, ka, b0, kb = int(pi_[i[x]]), int(segs['k'][i[x]]), int(pj_[j[x]]), int(segs['k'][j[x]])
        for da in (-1, 0, 1):
            for db in (-1, 0, 1):
                y = keyof.get((a0, ka + da, b0, kb + db))
                if y is not None:
                    uf.union(x, y)
    groups = {}
    for x in range(len(i)):
        groups.setdefault(uf.find(x), []).append(x)
    out = {k: [] for k in ('fi', 'fj', 'd0', 'Ci', 'Cj', 'seg_i', 'seg_j', 'piece_i', 'piece_j', 'si_min', 'sj_min')}
    for g, mem in groups.items():
        mem = np.asarray(mem)
        b = mem[np.argmin(d[mem])]
        Si = np.unique(i[mem]); Sj = np.unique(j[mem])
        out['fi'].append(int(segs['fid'][i[b]])); out['fj'].append(int(segs['fid'][j[b]]))
        out['d0'].append(float(d[b])); out['Ci'].append(C1[b]); out['Cj'].append(C2[b])
        out['seg_i'].append(Si); out['seg_j'].append(Sj)
        out['piece_i'].append(int(segs['piece'][i[b]])); out['piece_j'].append(int(segs['piece'][j[b]]))
        out['si_min'].append(int(i[b])); out['sj_min'].append(int(j[b]))
    out['Lc'] = _touch_len_all(out['seg_i'], out['seg_j'], segs, T)
    o = np.lexsort((np.array([c[2] for c in out['Ci']]), np.array([c[1] for c in out['Ci']]),
                    np.array([c[0] for c in out['Ci']]), np.array(out['fj']), np.array(out['fi'])))
    res = {'fi': np.asarray(out['fi'], np.int64)[o], 'fj': np.asarray(out['fj'], np.int64)[o],
           'self': np.zeros(len(o), bool), 'd0': np.asarray(out['d0'])[o], 'Lc': np.asarray(out['Lc'])[o],
           'Ci': np.asarray(out['Ci']).reshape(-1, 3)[o], 'Cj': np.asarray(out['Cj']).reshape(-1, 3)[o],
           'seg_i': [out['seg_i'][x] for x in o], 'seg_j': [out['seg_j'][x] for x in o],
           'piece_i': np.asarray(out['piece_i'], np.int64)[o], 'piece_j': np.asarray(out['piece_j'], np.int64)[o],
           'si_min': np.asarray(out['si_min'], np.int64)[o], 'sj_min': np.asarray(out['sj_min'], np.int64)[o]}
    return res


def _touch_len_all(seg_i, seg_j, segs, T):
    """L_c (J8 · `CJUNC_LC_RULE`) — instance 마다 두 가닥 각각에서 상대 instance 선분까지 중심선 거리 ≤ T (닿음) 인 구간 길이
    (선분마다 구간 합집합 · 안쪽 경계) 의 최댓값.  모든 instance · 선분 쌍을 한 번에 (이분 한 번)."""
    P0, P1 = segs['P0'], segs['P1']
    nI = len(seg_i)
    Lc = np.zeros(nI)
    if nI == 0:
        return Lc
    K, SIDE, S, Q = [], [], [], []
    for k in range(nI):
        for side, (A, B) in enumerate(((seg_i[k], seg_j[k]), (seg_j[k], seg_i[k]))):
            S.append(np.repeat(A, len(B))); Q.append(np.tile(B, len(A)))
            K.append(np.full(len(A) * len(B), k)); SIDE.append(np.full(len(A) * len(B), side))
    K = np.concatenate(K); SIDE = np.concatenate(SIDE); S = np.concatenate(S).astype(np.int64)
    Q = np.concatenate(Q).astype(np.int64)
    _, us, _, _, _ = seg_seg_closest(P0[S], P1[S], P0[Q], P1[Q])
    ua, ub = _touch_intervals(P0[S], P1[S], P0[Q], P1[Q], T, us)
    ok = np.isfinite(ua)
    seglen = np.linalg.norm(P1 - P0, axis=1)
    if not ok.any():
        return Lc
    K, SIDE, S, ua, ub = K[ok], SIDE[ok], S[ok], ua[ok], ub[ok]
    o = np.lexsort((ua, S, SIDE, K))
    K, SIDE, S, ua, ub = K[o], SIDE[o], S[o], ua[o], ub[o]
    tot = np.zeros((nI, 2))
    start = 0
    n = len(K)
    while start < n:                                         # (instance, 쪽, 선분) 무리마다 구간 합집합
        end = start
        while end < n and K[end] == K[start] and SIDE[end] == SIDE[start] and S[end] == S[start]:
            end += 1
        cur_a, cur_b = ua[start], ub[start]
        acc = 0.0
        for x in range(start + 1, end):
            if ua[x] <= cur_b:
                cur_b = max(cur_b, ub[x])
            else:
                acc += cur_b - cur_a
                cur_a, cur_b = ua[x], ub[x]
        acc += cur_b - cur_a
        tot[K[start], SIDE[start]] += acc * seglen[S[start]]
        start = end
    return tot.max(axis=1)


def _self_instances(items, pos, vox):
    """자기 접합 후보 — 항목 (같은 fid 비연속 면 · 재방문) 을 이웃 위치끼리 무리 지은 하나.
    → (후보 표, 항목 → 후보, 후보마다 항목 번호 목록, 항목마다 (앞 위치, 뒤 위치)).  L_c · s 는 `_self_geometry` 가 셀 조각으로 잰다."""
    if not items:
        return [], {}, [], []
    norm = []
    for (p, q, lin, ax, isface) in items:
        kp = (int(pos['piece'][p]), int(pos['k'][p])); kq = (int(pos['piece'][q]), int(pos['k'][q]))
        if kq < kp:
            p, q = q, p
        norm.append((p, q))
    uf = _UF()
    keyof = {}
    for x, (p, q) in enumerate(norm):
        keyof.setdefault((int(pos['fid'][p]), int(pos['piece'][p]), int(pos['k'][p]), int(pos['piece'][q]), int(pos['k'][q])),
                         []).append(x)
    for x, (p, q) in enumerate(norm):
        f, pp, kp, pq, kq = int(pos['fid'][p]), int(pos['piece'][p]), int(pos['k'][p]), int(pos['piece'][q]), int(pos['k'][q])
        for da in (-1, 0, 1):
            for db in (-1, 0, 1):
                for y in keyof.get((f, pp, kp + da, pq, kq + db), ()):
                    uf.union(x, y)
    groups = {}
    for x in range(len(norm)):
        groups.setdefault(uf.find(x), []).append(x)
    out = []
    face_map = {}
    gl = sorted(groups.values(), key=lambda m: min((int(pos['fid'][norm[x][0]]), int(pos['piece'][norm[x][0]]),
                                                     int(pos['k'][norm[x][0]])) for x in m))
    for gi, mem in enumerate(gl):
        best, bkey = None, None
        for x in mem:
            p, q = norm[x]
            dc = float(np.linalg.norm((pos['ijk'][p] - pos['ijk'][q]).astype(np.float64))) * vox
            key = (dc, min(int(pos['lin'][p]), int(pos['lin'][q])), max(int(pos['lin'][p]), int(pos['lin'][q])), p, q)
            if bkey is None or key < bkey:
                best, bkey = (p, q), key
            face_map[x] = gi
        same_piece = [abs(int(pos['k'][norm[x][1]]) - int(pos['k'][norm[x][0]])) for x in mem
                      if pos['piece'][norm[x][0]] == pos['piece'][norm[x][1]]]
        out.append({'fid': int(pos['fid'][best[0]]), 'p': best[0], 'q': best[1], 'Lc': math.nan,
                    'n_items': len(mem), 'dk_min': (min(same_piece) if same_piece else -1)})
    # 면 항목 (원래 items 순서) → instance
    fmap = {}
    for x in range(len(items)):
        fmap[x] = face_map[x]
    return out, fmap, [list(m) for m in gl], norm


def _clip_box(P0, P1, bmin, bmax):
    """선분 P0→P1 ∩ 닫힌 상자 [bmin, bmax] (배열 · Liang–Barsky) → 매개 (t0, t1) · 빈 = t0 > t1."""
    d = P1 - P0
    t0 = np.zeros(len(P0))
    t1 = np.ones(len(P0))
    for ax in range(3):
        da = d[:, ax]
        z = da == 0.0
        out = z & ((P0[:, ax] < bmin[:, ax]) | (P0[:, ax] > bmax[:, ax]))
        den = np.where(z, 1.0, da)
        ta = np.where(z, -np.inf, (bmin[:, ax] - P0[:, ax]) / den)
        tb = np.where(z, np.inf, (bmax[:, ax] - P0[:, ax]) / den)
        t0 = np.maximum(t0, np.minimum(ta, tb))
        t1 = np.minimum(t1, np.maximum(ta, tb))
        t0 = np.where(out, 1.0, t0)
        t1 = np.where(out, 0.0, t1)
    return t0, t1


def _pos_portions(plist, pos, segs, lo, vox):
    """위치들의 셀 안 중심선 조각 — 각 위치의 선분 (s0..s1) 을 그 셀의 **닫힌 상자 그대로** (띠 없음) 로 자른 것.
    이웃 셀 상자는 같은 식 (lo + ijk·vox) 이라 경계가 비트로 같고, 경계에만 닿는 선분 (스냅된 셀) 은 길이 0 점이다 —
    띠를 두면 조각이 셀 밖으로 늘어 자기 L_c 가 부풀어진다.  → (X0, X1, a0, a1) = 조각 끝점 · 끝의 경로 호 좌표 (선분 위 선형)."""
    pl = np.asarray(sorted({int(p) for p in plist}), np.int64)
    if len(pl) == 0:
        z = np.zeros((0, 3))
        return z, z.copy(), np.zeros(0), np.zeros(0)
    cnt = pos['s1'][pl] - pos['s0'][pl] + 1
    rp = np.repeat(pl, cnt)
    sg = pos['s0'][rp] + (np.arange(len(rp)) - np.repeat(np.cumsum(cnt) - cnt, cnt))
    ijk = pos['ijk'][rp].astype(np.float64)
    bmin = lo + ijk * vox
    bmax = lo + (ijk + 1.0) * vox
    P0, P1 = segs['P0'][sg], segs['P1'][sg]
    t0, t1 = _clip_box(P0, P1, bmin, bmax)
    ok = t0 <= t1
    d = (P1 - P0)[ok]
    X0 = P0[ok] + t0[ok, None] * d
    X1 = P0[ok] + t1[ok, None] * d
    aa, ab = segs['arc_a'][sg][ok], segs['arc_b'][sg][ok]
    return X0, X1, aa + t0[ok] * (ab - aa), aa + t1[ok] * (ab - aa)


def _touch_len_sets(A0, A1, B0, B1, T):
    """닿음 길이 (`CJUNC_LC_RULE` 와 같은 규칙) — 두 선분 집합 사이: 쪽마다 선분별 구간 합집합 (안쪽 경계) 길이의 합 · 두 쪽의 최댓값."""
    best = 0.0
    for S0, S1, Q0, Q1 in ((A0, A1, B0, B1), (B0, B1, A0, A1)):
        ns, nq = len(S0), len(Q0)
        if ns == 0 or nq == 0:
            continue
        si = np.repeat(np.arange(ns), nq)
        qi = np.tile(np.arange(nq), ns)
        _, us, _, _, _ = seg_seg_closest(S0[si], S1[si], Q0[qi], Q1[qi])
        ua, ub = _touch_intervals(S0[si], S1[si], Q0[qi], Q1[qi], T, us)
        ok = np.isfinite(ua)
        if not ok.any():
            continue
        si, ua, ub = si[ok], ua[ok], ub[ok]
        o = np.lexsort((ua, si))
        si, ua, ub = si[o], ua[o], ub[o]
        seglen = np.linalg.norm(S1 - S0, axis=1)
        tot = 0.0
        start, n = 0, len(si)
        while start < n:                                     # 선분마다 구간 합집합
            end = start
            while end < n and si[end] == si[start]:
                end += 1
            cur_a, cur_b = ua[start], ub[start]
            acc = 0.0
            for x in range(start + 1, end):
                if ua[x] <= cur_b:
                    cur_b = max(cur_b, ub[x])
                else:
                    acc += cur_b - cur_a
                    cur_a, cur_b = ua[x], ub[x]
            acc += cur_b - cur_a
            tot += acc * seglen[si[start]]
            start = end
        best = max(best, tot)
    return best


def _self_geometry(groups, norm, pos, segs, lo, vox, T):
    """자기 접합 후보마다 (s, L_c) — 두 쪽 = 그 후보 항목의 앞 위치들 · 뒤 위치들의 셀 조각.
    s = 두 쪽 사이 **최근접점 쌍** (거리² ε 띠 `CJUNC_EPS_D2_UM2` · 띠 안 = 호 길이가 작은 쪽) 의 경로 호 길이 (`CJUNC_SELF_S_RULE`) ·
    L_c = 두 쪽 사이 닿음 길이 (`CJUNC_SELF_LC_RULE`).  조각이 없는 쪽 = s NaN (재지 못함 · 기록) · L_c 0."""
    ng = len(groups)
    s_out = np.full(ng, np.nan)
    lc_out = np.zeros(ng)
    for gi, mem in enumerate(groups):
        A0, A1, a0, a1 = _pos_portions([norm[x][0] for x in mem], pos, segs, lo, vox)
        B0, B1, b0, b1 = _pos_portions([norm[x][1] for x in mem], pos, segs, lo, vox)
        if len(A0) == 0 or len(B0) == 0:
            continue
        ia = np.repeat(np.arange(len(A0)), len(B0))
        ib = np.tile(np.arange(len(B0)), len(A0))
        d, s_, t_, _, _ = seg_seg_closest(A0[ia], A1[ia], B0[ib], B1[ib])
        sep = np.abs((a0[ia] + s_ * (a1[ia] - a0[ia])) - (b0[ib] + t_ * (b1[ib] - b0[ib])))
        d2 = d * d
        band = d2 <= float(d2.min()) + CJUNC_EPS_D2_UM2
        s_out[gi] = float(sep[band].min())
        lc_out[gi] = _touch_len_sets(A0, A1, B0, B1, T)
    return s_out, lc_out


def _merge_instances(inst, selfinst, segs):
    nI = len(inst['fi']); nS = len(selfinst)
    out = {'fi': np.r_[inst['fi'], np.array([s['fid'] for s in selfinst], np.int64)].astype(np.int64),
           'fj': np.r_[inst['fj'], np.array([s['fid'] for s in selfinst], np.int64)].astype(np.int64),
           'self': np.r_[np.zeros(nI, bool), np.ones(nS, bool)],
           'd0': np.r_[inst['d0'], np.full(nS, np.nan)],
           'Lc': np.r_[inst['Lc'], np.array([s['Lc'] for s in selfinst], np.float64)],
           's': np.r_[np.full(nI, np.nan), np.array([s['s'] for s in selfinst], np.float64)],   # 자기 접합 경로 호 길이 (distinct = NaN)
           'Ci': np.r_[inst['Ci'], np.zeros((nS, 3))].reshape(-1, 3),
           'Cj': np.r_[inst['Cj'], np.zeros((nS, 3))].reshape(-1, 3),
           'piece_i': np.r_[inst['piece_i'], np.full(nS, -1)].astype(np.int64),
           'piece_j': np.r_[inst['piece_j'], np.full(nS, -1)].astype(np.int64),
           'self_p': np.r_[np.full(nI, -1), np.array([s['p'] for s in selfinst], np.int64)].astype(np.int64),
           'self_q': np.r_[np.full(nI, -1), np.array([s['q'] for s in selfinst], np.int64)].astype(np.int64),
           'self_dk_min': np.r_[np.full(nI, -1), np.array([s['dk_min'] for s in selfinst], np.int64)].astype(np.int64)}
    out['seg_i'] = list(inst['seg_i']) + [np.zeros(0, np.int64)] * nS
    out['seg_j'] = list(inst['seg_j']) + [np.zeros(0, np.int64)] * nS
    return out


def _ports(allinst, pos, piece_pos, segs, lo, vox, n, flat, r_port):
    """J3 · J4 — instance 최근접점 → 그 fid 의 살아있는 위치 중 셀 중심이 r_port 안 최근접 (동률 = 정준 경로 번호 작은 쪽)."""
    nI = len(allinst['fi'])
    port_i = np.full(nI, -1, np.int64); port_j = np.full(nI, -1, np.int64)
    reason = np.array([''] * nI, dtype=object)
    tie_i = np.zeros(nI, bool); tie_j = np.zeros(nI, bool)
    disp = np.zeros(nI, bool); sdist = np.full(nI, np.nan)
    cp = np.zeros((nI, 3))
    centre = lambda p: lo + (pos['ijk'][p].astype(np.float64) + 0.5) * vox   # noqa: E731

    def _one(C, piece):
        a0, a1 = piece_pos[piece]
        cand = np.arange(a0, a1)
        cand = cand[pos['live'][cand]]
        if len(cand) == 0:
            return -1, False, np.inf
        cc = lo + (pos['ijk'][cand].astype(np.float64) + 0.5) * vox
        dd = np.sqrt(np.sum((cc - C) ** 2, axis=1))
        okc = dd <= r_port
        if not okc.any():
            return -1, False, np.inf
        dm = float(np.min(dd[okc]))
        best = cand[okc][dd[okc] == dm]
        kmin = best[np.argmin(pos['k'][best])]
        return int(kmin), bool(len(best) > 1), dm

    def _why(C):
        c = np.floor((C - lo) / vox).astype(np.int64)
        if np.any(c < 0) or np.any(c >= n):
            return 'out_of_box'
        s = int(flat[np.ravel_multi_index(tuple(c), tuple(n))])
        return 'no_live_port_in_rport' if s == 3 else f'covered_{_SID_NAME.get(s, str(s))}'

    for k in range(nI):
        if allinst['self'][k]:
            p, q = int(allinst['self_p'][k]), int(allinst['self_q'][k])
            port_i[k], port_j[k] = p, q
            cp[k] = 0.5 * (centre(p) + centre(q))
            sdist[k] = 0.0
            continue
        Ci, Cj = allinst['Ci'][k], allinst['Cj'][k]
        cp[k] = 0.5 * (Ci + Cj)
        pi_, ti, di = _one(Ci, int(allinst['piece_i'][k]))
        pj_, tj, dj = _one(Cj, int(allinst['piece_j'][k]))
        port_i[k], port_j[k] = pi_, pj_
        tie_i[k], tie_j[k] = ti, tj
        if pi_ < 0 or pj_ < 0:
            reason[k] = _why(Ci) if pi_ < 0 else _why(Cj)
            continue
        sdist[k] = max(di, dj)
        ni = np.floor((Ci - lo) / vox).astype(np.int64); nj = np.floor((Cj - lo) / vox).astype(np.int64)
        disp[k] = bool(np.any(pos['ijk'][pi_] != ni) or np.any(pos['ijk'][pj_] != nj))
    return {'port_i': port_i, 'port_j': port_j, 'realized': (port_i >= 0) & (port_j >= 0), 'reason': reason,
            'tie_i': tie_i, 'tie_j': tie_j, 'port_displaced': disp, 'port_search_um': sdist, 'cp': cp,
            'long': np.zeros(nI, bool)}


def _census(inst, pos, ft, cell_lin, cell_ptr, sid, flat, owner_ties, multi_site, n_cut_site, n_unreg, segs, nfib, npiece,
            rf):
    cnt = np.diff(cell_ptr)
    nI = len(inst['fi'])
    real = inst['realized']
    rel = {'same_cell': 0, 'face': 0, 'edge': 0, 'corner': 0, 'apart': 0}
    for k in np.flatnonzero(real):
        d = np.abs(pos['ijk'][inst['port_i'][k]] - pos['ijk'][inst['port_j'][k]])
        s = int(d.sum()); mx = int(d.max())
        rel['same_cell' if s == 0 else ('face' if s == 1 and mx == 1 else
                                         ('edge' if s == 2 and mx == 1 else ('corner' if s == 3 and mx == 1 else 'apart')))] += 1
    reasons = {}
    for r_ in inst['reason'][~real]:
        reasons[str(r_)] = reasons.get(str(r_), 0) + 1
    vx_by = {}
    vx = ft['kind'] == K_VX
    if vx.any():
        n3 = np.array(sid.shape)
        stride = np.array([n3[1] * n3[2], n3[2], 1])
        la = ft['lin'][vx]; lb = la + stride[ft['ax'][vx]]
        other = np.where(ft['pa'][vx] >= 0, flat[lb], flat[la])
        for s_, c_ in zip(*np.unique(other, return_counts=True)):
            vx_by[_SID_NAME.get(int(s_), str(int(s_)))] = int(c_)
    gap = inst['d0'][~inst['self']] - 2.0 * rf
    lc = inst['Lc']
    dk = inst['self_dk_min'][inst['self'] & (inst['self_dk_min'] >= 0)]
    return {'n_vgcf_fibres': int(nfib), 'n_pieces': int(npiece), 'n_segments': int(len(segs['P0'])),
            'n_positions': int(len(pos['lin'])), 'n_live_positions': int(np.sum(pos['live'])),
            'n_cross_cells': int(np.sum(cnt >= 2)), 'n_kway_cells_ge3': int(np.sum(cnt >= 3)),
            'n_instances': int(nI), 'n_instances_distinct': int(np.sum(~inst['self'])),
            'n_instances_self': int(np.sum(inst['self'])), 'n_realized': int(np.sum(real)), 'n_unrealized_by_reason': reasons,
            'n_port_ties': int(np.sum(inst['tie_i']) + np.sum(inst['tie_j'])), 'n_port_displaced': int(np.sum(inst['port_displaced'])),
            'port_relation': rel, 'n_cut_site_faces': int(n_cut_site), 'n_unreg_faces': int(n_unreg),
            'n_cut_self_faces': int(np.sum(ft['kind'] == K_CUT_SELF)), 'n_vx_faces_by_sid': vx_by,
            'owner_tie_noncanonical': int(owner_ties), 'n_faces_multi_site': int(multi_site),
            'surface_gap_um': ({'min': float(gap.min()), 'median': float(np.median(gap)), 'max': float(gap.max())}
                               if len(gap) else None),
            'Lc_um': ({'min': float(lc.min()), 'median': float(np.median(lc)), 'p90': float(np.quantile(lc, 0.90)),
                       'p99': float(np.quantile(lc, 0.99)), 'max': float(lc.max())} if len(lc) else None),
            #  길이 법칙 v0 배율 (max(1, L_c/L_par)) — 합 · 최댓값 · 1 넘는 수 (긴 접촉이 σ 에 얼마나 들어가는가 · S0 용)
            'len_mult': ({'sum': float(np.sum(inst['mult'])), 'max': float(np.max(inst['mult'])),
                          'n_gt1': int(np.sum(inst['mult'] > 1.0))} if len(lc) else None),
            #  긴 접촉이 꺾임 (같은 조각 · 경로 간격 작음) 에서 생기는지 고리 · 머리핀 (간격 큼) 에서 생기는지 가르는 진단 (S0 용 · 판정 아님)
            'n_long_distinct': int(np.sum(inst['long'] & ~inst['self'])) if 'long' in inst else None,
            'n_long_self': int(np.sum(inst['long'] & inst['self'])) if 'long' in inst else None,
            'self_dk_min': ({'min': int(dk.min()), 'median': float(np.median(dk)), 'max': int(dk.max()),
                             'n_le_4': int(np.sum(dk <= 4))} if len(dk) else None)}


def _sdcp_bridging(sid, ft, pos, n):
    """SDCP 경유 섬유 연결 수 (설계 §2 · §4-5) — SDCP 셀 6-면 성분 중 서로 다른 VGCF fid 둘 이상의 셀과 면으로 닿는 성분 · 이어지는 fid 쌍."""
    s5 = sid == 5
    if not s5.any():
        return {'n_sdcp_bridging_components': 0, 'n_sdcp_bridged_fid_pairs': 0}
    lab, _ = ndimage.label(s5)
    flat = sid.reshape(-1)
    labf = lab.reshape(-1)
    stride = np.array([n[1] * n[2], n[2], 1])
    vx = ft['kind'] == K_VX
    la = ft['lin'][vx]; lb = la + stride[ft['ax'][vx]]
    a_is3 = ft['pa'][vx] >= 0
    lin3 = np.where(a_is3, la, lb); lin5 = np.where(a_is3, lb, la)
    m = flat[lin5] == 5
    comp = {}
    order = np.argsort(pos['lin'])
    plin = pos['lin'][order]
    for c3, c5 in zip(lin3[m], lin5[m]):
        a0 = np.searchsorted(plin, c3, 'left'); a1 = np.searchsorted(plin, c3, 'right')
        fids = {int(pos['fid'][order[x]]) for x in range(a0, a1) if pos['live'][order[x]]}
        comp.setdefault(int(labf[c5]), set()).update(fids)
    nb = 0
    pairs = set()
    for fs in comp.values():
        if len(fs) >= 2:
            nb += 1
            fs = sorted(fs)
            for x in range(len(fs)):
                for y in range(x + 1, len(fs)):
                    pairs.add((fs[x], fs[y]))
    return {'n_sdcp_bridging_components': int(nb), 'n_sdcp_bridged_fid_pairs': int(len(pairs))}


# ═════════════════════════ 계획 ═════════════════════════
def plan_rows_fp(plan):
    return _fp(plan['mode'], plan['g_code'], plan['rj_eff'], plan['mult'], plan['registry']['fp']['registry'], plan['unreg_law'],
               plan['ptfe_jlaw'], plan['ptfe_stamp'], plan['sdcp_mod'], plan['quantitative'])


def cjunc_plan(reg, R_j_ohm, *, unreg_law, ptfe_stamp, ptfe_jlaw='P0', sdcp_mod=None, quantitative=True,
               allow_rj_limits=False, rj_reference=RJ_REFERENCE_PLANE, lead_subtraction=None):
    """instance 마다 간선 (g = 1e4·m/R_j′ · m = 길이 법칙 v0 배율) · 축약 (R_j′ = 0) · 절단 (P1) · 미실현.  S3 = sdcp_mod {'c': c}
    (S2 원장 없이 = 거부).  정량 (quantitative=True): R_j 유한 > 0 (극한 0 · ∞ = allow_rj_limits 사다리 진단 전용) · c ∈ {0, 1} ·
    원장 거부 사유 (s_min 미등록 포함) = 거부.  긴 접촉은 거부하지 않는다 (옛 J8 · 길이 법칙이 맡는다 · 수는 기록)."""
    if not isinstance(reg, dict) or reg.get('kind') != 'cjunc_registry':
        raise TypeError('cjunc_plan: 원장은 cjunc_registry 의 결과여야 한다 (S3 = S2 원장 없이 거부 · 설계 §5-2)')
    if registry_fp(reg) != reg.get('fp', {}).get('registry'):
        raise ValueError('cjunc_plan: 원장이 만든 뒤 바뀌었다 (지문 불일치 · E5)')
    if rj_reference != RJ_REFERENCE_PLANE:
        raise ValueError(f'cjunc_plan: R_j 기준면 {rj_reference!r} — v0 는 모형 내부값 ({RJ_REFERENCE_PLANE}) 만 받는다 (T1-5′ · J4)')
    if lead_subtraction is not None:
        raise ValueError('cjunc_plan: 리드 빼기 (단자 기준 R_j) = v0 미지원 · 거부 (T1-5′ — 실측 순접촉값 주장 없음)')
    if isinstance(R_j_ohm, bool) or not isinstance(R_j_ohm, (int, float, np.floating, np.integer)):
        raise TypeError(f'cjunc_plan: R_j = 실수 (Ω): {R_j_ohm!r}')
    R0 = float(R_j_ohm)
    if math.isnan(R0) or R0 < 0.0:
        raise ValueError(f'cjunc_plan: R_j 는 NaN · 음수일 수 없다: {R_j_ohm!r}')
    if (R0 == 0.0 or math.isinf(R0)) and not allow_rj_limits:
        raise ValueError('cjunc_plan: R_j 극한 (0 = 사다리 천장 축약 · ∞ = 바닥) 은 allow_rj_limits 표지 (사다리 진단) 와만 — 정량 거부')
    if unreg_law not in UNREG_LAWS:
        raise ValueError(f'cjunc_plan: 미등록 VV 면 법칙 {unreg_law!r} — 선언 필수 {UNREG_LAWS} (자동 fallback 없음 · v2 §3-6)')
    if ptfe_stamp not in PTFE_STAMPS:
        raise ValueError(f'cjunc_plan: ptfe_stamp 선언 필수 {PTFE_STAMPS}: {ptfe_stamp!r}')
    if ptfe_jlaw not in PTFE_JLAWS:
        raise ValueError(f'cjunc_plan: PTFE–접합 법칙 {ptfe_jlaw!r} ∉ {PTFE_JLAWS}')
    if ptfe_jlaw == 'P1' and ptfe_stamp != 'face_alpha':
        raise ValueError(f'cjunc_plan: P1 은 face_alpha 에서만 ({ptfe_stamp} — centerline 은 이미 VGCF 셀을 sid 7 로 잘라 겹친다 · '
                         f'off 는 PTFE 표현이 없다 · 설계 §4-1)')
    c = None
    if sdcp_mod is not None:
        if not isinstance(sdcp_mod, dict) or set(sdcp_mod) - {'c'} or 'c' not in sdcp_mod:
            raise TypeError(f"cjunc_plan: sdcp_mod = {{'c': c}} 만: {sdcp_mod!r}")
        cv = sdcp_mod['c']
        if isinstance(cv, bool) or not isinstance(cv, (int, float, np.floating, np.integer)):
            raise TypeError(f'cjunc_plan: c = 실수: {cv!r}')
        c = float(cv)
        if not (math.isfinite(c) and 0.0 <= c <= 1.0):
            raise ValueError(f'cjunc_plan: c ∈ [0, 1] 유한: {cv!r}')
        if quantitative and c not in (0.0, 1.0):
            raise ValueError(f'cjunc_plan: 정량 R 런의 c 는 {{0, 1}} 만 (시험 격자는 quantitative=False): {c}')
    inst = reg['instances']
    nI = len(inst['fi'])
    mode = np.zeros(nI, np.int64)
    g = np.zeros(nI, np.float64)
    rje = np.full(nI, np.nan)
    a = inst['a_sdcp'].astype(np.float64)
    mult = np.asarray(inst['mult'], np.float64).copy()       # 길이 법칙 v0 (원장에서 한 번 · 계획은 읽기만)
    if not (np.isfinite(mult).all() and (mult >= 1.0).all()):
        raise ValueError('cjunc_plan: 길이 법칙 배율은 유한 · ≥ 1 이어야 한다 (max(1, L_c/L_par)) — 원장 이상')
    for k in range(nI):
        if not inst['realized'][k]:
            mode[k] = MODE_UNREALIZED
            continue
        if ptfe_jlaw == 'P1' and inst['ptfe_cov'][k]:
            mode[k] = MODE_CUT_P1                            # N18 — 덮인 접합은 c 와 무관하게 먼저 절단
            continue
        r = R0 if c is None else float(sdcp_rj_eff(R0, c, a[k]))
        rje[k] = r
        if r == 0.0:
            mode[k] = MODE_CONTRACT
        elif math.isinf(r):
            mode[k] = MODE_NONE_INF
        else:
            mode[k] = MODE_EDGE
            g[k] = float(junction_g_code(r)) * float(mult[k])   # G_j = max(1, L_c/L_par) / R_j′ (lumped 간선 하나)
    long = np.asarray(inst['long'], bool)
    rej = [dict(x) for x in reg['rejections']]               # 긴 접촉 = 거부 아님 (길이 법칙 v0 · 1저자 10-20 Q17)
    if not quantitative:
        rej = []
    near = int(np.sum(inst['a_sdcp'] & inst['realized']))
    counts = {'n_instances': nI, 'n_edge': int(np.sum(mode == MODE_EDGE)), 'n_contract': int(np.sum(mode == MODE_CONTRACT)),
              'n_cut_p1': int(np.sum(mode == MODE_CUT_P1)), 'n_unrealized': int(np.sum(mode == MODE_UNREALIZED)),
              'n_none_inf': int(np.sum(mode == MODE_NONE_INF)), 'n_long': int(np.sum(long)), 'n_sdcp_near': near,
              'n_contracted_by_c': int(np.sum((mode == MODE_CONTRACT) & (R0 > 0.0))),
              'n_ptfe_cov': int(np.sum(inst['ptfe_cov'])),
              'len_mult_sum_edge': float(np.sum(mult[mode == MODE_EDGE])),
              'len_mult_max': (float(np.max(mult)) if nI else None)}
    record = {'model': CJUNC_MODEL_VERSION, 'schema': CJUNC_SCHEMA, 'status': CJUNC_STATUS,
              'qualifiers': list(CJUNC_QUALIFIERS), 'R_j_ohm': (R0 if math.isfinite(R0) else 'inf'),
              'len_law': CJUNC_LEN_LAW, 's_min_um': reg['thresholds']['s_min_um'],
              'rj_reference_plane': RJ_REFERENCE_PLANE, 'half_cell_in_edge': False, 'unreg_law': unreg_law,
              'ptfe_jlaw': ptfe_jlaw, 'ptfe_stamp': ptfe_stamp,
              'sdcp_mod': (None if c is None else {'c': c, 'tol_sj_um': reg['thresholds']['tol_sj_um'],
                                                   'r_sdcp_um': reg['thresholds']['r_sdcp_um']}),
              's3_discriminating': (None if c is None else bool(near > 0)),
              'quantitative': bool(quantitative), 'allow_rj_limits': bool(allow_rj_limits),
              'thresholds': dict(reg['thresholds']), 'rules': dict(reg['rules']), 'census': dict(reg['census']),
              'counts': counts, 'fp_registry': reg['fp']['registry'], 'fp_sid': reg['fp']['sid']}
    plan = {'kind': 'cjunc_plan', 'version': CJUNC_MODEL_VERSION, 'registry': reg, 'mode': mode, 'g_code': g, 'rj_eff': rje,
            'mult': mult, 'unreg_law': unreg_law, 'ptfe_jlaw': ptfe_jlaw, 'ptfe_stamp': ptfe_stamp,
            'sdcp_mod': (None if c is None else {'c': c}), 'quantitative': bool(quantitative), 'rejections': rej,
            'record': record}
    plan['fp_rows'] = plan_rows_fp(plan)
    return plan


def cjunc_require_quantitative(plan, sid, vox, sigma_of_sid=None, rint=None, iface=None, periodic_xy=False,
                               return_field=False):
    """솔브 입구 관문 (조립 전 · CG 0) — 계획 모양 · 지문 · 불변량 · 거부 사유 · 동시 사용 · 격자 결합 · 채널."""
    if not isinstance(plan, dict) or plan.get('kind') != 'cjunc_plan':
        raise TypeError('cjunc 는 cjunc_plan 의 결과여야 한다 (S3 sdcp_mod 단독 = 거부)')
    if plan.get('version') != CJUNC_MODEL_VERSION or plan.get('record', {}).get('schema') != CJUNC_SCHEMA:
        raise ValueError(f"cjunc: 다른 판본 계획 ({plan.get('version')!r}) — 거부")
    reg = plan['registry']
    if registry_fp(reg) != reg['fp']['registry']:
        raise ValueError('cjunc: 원장이 계획 뒤 바뀌었다 (지문 · E5)')
    if plan_rows_fp(plan) != plan.get('fp_rows'):
        raise ValueError('cjunc: 계획 행이 만든 뒤 바뀌었다 (지문 · E5)')
    if reg.get('rules', {}).get('len_law') != CJUNC_LEN_LAW or plan.get('record', {}).get('len_law') != CJUNC_LEN_LAW:
        raise ValueError(f"cjunc: 다른 접합 길이 법칙의 원장 · 계획 ({reg.get('rules', {}).get('len_law')!r}) — "
                         f'{CJUNC_LEN_LAW} 만 (옛 점 접합 · J8 거부 판 섞임 거부)')
    g = np.asarray(plan['g_code'], np.float64)
    e = plan['mode'] == MODE_EDGE
    if not (np.isfinite(g).all() and (g >= 0.0).all() and (g[e] > 0.0).all()):
        raise ValueError('cjunc: 계획 간선 g 는 유한 · 0 이상 (간선 행 > 0) — NaN · 음수 · inf = 조립 전 거부 (Q7 와 같은 꼴 · 지문을 다시 만든 변이도)')
    m = np.asarray(plan.get('mult'), np.float64)
    if m.shape != g.shape or not (np.isfinite(m).all() and (m >= 1.0).all()):
        raise ValueError('cjunc: 계획 배율 (길이 법칙 v0) 은 instance 마다 유한 · ≥ 1 — 조립 전 거부')
    if e.any() and not np.array_equal(g[e], junction_g_code(np.asarray(plan['rj_eff'], np.float64)[e]) * m[e]):
        raise ValueError('cjunc: 계획 간선 g ≠ 1e4·m/R_j′ — 배율 기록과 쓰는 값이 묶이지 않았다 (지문을 다시 만든 변이 · 조립 전 거부)')
    if plan['rejections']:
        raise ValueError('cjunc 정량 모드 거부 — ' + ' · '.join(f"{x['code']}(n={x.get('n')})" for x in plan['rejections']))
    if rint:
        raise ValueError('cjunc: r1 탐침 표 (--step3-rint-e/-i) 와 동시 사용 거부 (설계 §4-3)')
    if iface is not None:
        raise ValueError('cjunc: ①′ AM–AM 막 (iface) 과 동시 사용 거부 (생산 HOLD · 설계 §4-3)')
    if periodic_xy:
        raise ValueError('cjunc: 주기 경계 정량 거부 (raster 가 주기 영상을 안 만든다 · J10)')
    if return_field:
        raise ValueError('cjunc v0 = σ_e 전용 — 장 · je · 분담 · Joule 진단은 원장을 읽기 전이라 거부 (return_field · 설계 §3-3 · §7 LEAN 4)')
    if tuple(np.asarray(sid).shape) != tuple(reg['shape']) or _grid_fp(sid) != reg['fp']['sid']:
        raise ValueError('cjunc: 다른 격자 (sid 지문 · 모양) — 원장을 그 sid 에서 다시 만들 것 (E5)')
    v = float(vox)
    if not (math.isfinite(v) and v == float(reg['vox'])):
        raise ValueError(f"cjunc: 솔버 vox {vox!r} ≠ 원장 vox {reg['vox']!r} (RIMP-05 와 같은 부류)")
    if sigma_of_sid is not None:
        a = np.asarray(sigma_of_sid, np.float64)
        s = np.asarray(sid)
        bad = (not (a.shape[0] > 3 and a[3] > 0.0)) if a.ndim == 1 else (not (a[s == 3] > 0.0).all())
        if bad and len(reg['positions']['lin']):
            raise ValueError('cjunc: 이 채널에서 VGCF 절연 (σ_VGCF = 0 · 이온 표) — 접합 요청은 전자 채널뿐 (조용한 무효 금지)')
    return plan


# ═════════════════════════ 조립 (solve_sigma_z 훅) ═════════════════════════
_CAT = {'other_bulk': 0, 'vv_axial': 1, 'vv_unreg_fused': 2, 'va_face': 3, 'sv_face': 4, 'vx_other': 5, 'vv_junction': 6,
        'vv_self_fused': 7}
_CAT_NAME = {v: k for k, v in _CAT.items()}


class CjuncAssembler:
    """`solve_sigma_z` 가 셀 dof 로 만든 면 (couple) · 판 결합을 받아 멤버십 dof · 접합 간선 · 절단 · 축약 · 실제 그래프 가지치기를
    한 계를 만든다 (J1 · J3 · J5 · J6 · J7 · J9 · J11 · J12 · E1 · E3 · E6)."""

    def __init__(self, plan, sid, cond, idx, n_cells, sig, vox):
        self.plan = plan
        self.reg = reg = plan['registry']
        self.sid = sid
        self.flat = np.asarray(sid).reshape(-1)
        self.sigf = np.asarray(sig, np.float64).reshape(-1)
        self.vox = float(vox)
        self.cells_lin = np.flatnonzero(np.asarray(cond).reshape(-1))
        self.n_cells = int(n_cells)
        pos = reg['positions']
        live = pos['live'].copy()
        if live.any() and not np.asarray(cond).reshape(-1)[pos['lin'][live]].all():
            raise ValueError('cjunc: 멤버십 셀이 이 채널에서 도체가 아니다 (σ_VGCF > 0 이어야 · 조용한 무효 금지)')
        self.pos_dof = np.full(len(pos['lin']), -1, np.int64)
        prim = pos['primary']
        self.pos_dof[prim] = np.asarray(idx).reshape(-1)[pos['lin'][prim]]
        extra = np.flatnonzero(live & ~prim)
        self.pos_dof[extra] = self.n_cells + np.arange(len(extra))
        self.n_total = self.n_cells + len(extra)
        ft = reg['faces']
        self.ft = ft
        self.tkey = ft['key']
        self.E = []                                          # (u, v, g, cat, sa, sb, sida, sidb)
        self.tomb = {'cut_site': 0, 'cut_self': 0, 'unreg_cut': 0}
        self.n_unreg_fused = 0
        self.n_self_fused = 0

    def add_faces(self, axis, a2, b2, g):
        if axis is None:
            raise ValueError('cjunc: 주기 면 (axis None) — 정량 거부 (입구에서 막혀야 한다)')
        a2 = np.asarray(a2, np.int64); b2 = np.asarray(b2, np.int64); g = np.asarray(g, np.float64)
        la = self.cells_lin[a2]; lb = self.cells_lin[b2]
        key = la * 3 + axis
        lo_ = np.searchsorted(self.tkey, key, 'left'); hi_ = np.searchsorted(self.tkey, key, 'right')
        hit = hi_ > lo_
        pt = ~hit
        if pt.any():
            self._emit(a2[pt], b2[pt], g[pt], np.full(int(pt.sum()), _CAT['other_bulk']), la[pt], lb[pt])
        if not hit.any():
            return
        fh = np.flatnonzero(hit)
        nr = (hi_ - lo_)[fh]
        fi = np.repeat(fh, nr)
        row = np.repeat(lo_[fh], nr) + (np.arange(len(fi)) - np.repeat(np.cumsum(nr) - nr, nr))
        kind = self.ft['kind'][row]
        pa = self.ft['pa'][row]; pb = self.ft['pb'][row]
        m = kind == K_AXIAL
        if m.any():
            self._emit(self.pos_dof[pa[m]], self.pos_dof[pb[m]], g[fi[m]], np.full(int(m.sum()), _CAT['vv_axial']),
                       la[fi[m]], lb[fi[m]])
        m = kind == K_VX
        if m.any():
            u = np.where(pa[m] >= 0, self.pos_dof[np.maximum(pa[m], 0)], a2[fi[m]])
            v = np.where(pb[m] >= 0, self.pos_dof[np.maximum(pb[m], 0)], b2[fi[m]])
            sa_, sb_ = self.flat[la[fi[m]]], self.flat[lb[fi[m]]]
            pair = np.minimum(sa_, sb_) * 10 + np.maximum(sa_, sb_)
            cat = np.where(np.isin(pair, (13, 23)), _CAT['va_face'], np.where(pair == 35, _CAT['sv_face'], _CAT['vx_other']))
            self._emit(u, v, g[fi[m]], cat, la[fi[m]], lb[fi[m]])
        m = kind == K_UNREG
        if m.any():
            if self.plan['unreg_law'] == 'fused':
                self._emit(self.pos_dof[pa[m]], self.pos_dof[pb[m]], g[fi[m]], np.full(int(m.sum()), _CAT['vv_unreg_fused']),
                           la[fi[m]], lb[fi[m]])
                self.n_unreg_fused += int(m.sum())
            else:
                self.tomb['unreg_cut'] += int(m.sum())
        m = kind == K_SELF_FUSED
        if m.any():                                          # 꺾임 (s < s_min) = 같은 가닥의 연속 — 옛 복셀 융합 그대로 (접합 아님)
            self._emit(self.pos_dof[pa[m]], self.pos_dof[pb[m]], g[fi[m]], np.full(int(m.sum()), _CAT['vv_self_fused']),
                       la[fi[m]], lb[fi[m]])
            self.n_self_fused += int(m.sum())
        self.tomb['cut_site'] += int(np.sum(kind == K_CUT_SITE))
        self.tomb['cut_self'] += int(np.sum(kind == K_CUT_SELF))

    def _emit(self, u, v, g, cat, la, lb):
        u = np.asarray(u, np.int64)
        self.E.append((u, np.asarray(v, np.int64), np.asarray(g, np.float64), np.asarray(cat, np.int64), self.sigf[la],
                       self.sigf[lb], self.flat[la], self.flat[lb], np.full(len(u), -1, np.int64)))

    def _plate_owner(self, A, top):
        """판 결합 셀이 VGCF (멤버십) 이면 판 쪽 면 중심에 최근접 멤버십 dof (J9) — 아니면 그대로."""
        A = np.asarray(A, np.int64)
        if len(A) == 0:
            return A
        reg = self.reg
        pos = reg['positions']
        lin = self.cells_lin[A]
        j = np.searchsorted(reg['cell_lin'], lin)
        okj = j < len(reg['cell_lin'])
        okj[okj] = reg['cell_lin'][j[okj]] == lin[okj]
        if not okj.any():
            return A
        q = np.flatnonzero(okj)
        a0 = reg['cell_ptr'][j[q]]; cnt = reg['cell_ptr'][j[q] + 1] - a0
        qq = np.repeat(q, cnt)
        off = np.arange(len(qq)) - np.repeat(np.cumsum(cnt) - cnt, cnt)
        pp = reg['cell_pos'][np.repeat(a0, cnt) + off]
        ijk = np.stack(np.unravel_index(lin, reg['shape']), 1).astype(np.float64)
        X = reg['lo'] + (ijk + 0.5) * self.vox
        X[:, 2] += (0.5 if top else -0.5) * self.vox
        own, _ = _owner_select(qq, pp, X, pos, reg['segments'], len(A))
        out = A.copy()
        sel = own >= 0
        out[sel] = self.pos_dof[own[sel]]
        return out

    def build(self, Ab, gb, At, gt, cb=None, ct=None):
        plan, reg = self.plan, self.reg
        inst = reg['instances']
        # 접합 간선 · 축약
        mode = plan['mode']
        pu = self.pos_dof[np.maximum(inst['port_i'], 0)]; pv = self.pos_dof[np.maximum(inst['port_j'], 0)]
        e = np.flatnonzero(mode == MODE_EDGE)
        if len(e):
            gj = plan['g_code'][e]
            self.E.append((pu[e], pv[e], gj, np.full(len(e), _CAT['vv_junction']), np.full(len(e), np.nan),
                           np.full(len(e), np.nan), np.full(len(e), 3), np.full(len(e), 3), e.astype(np.int64)))
        self.junction_edge_inst = e
        rep = np.arange(self.n_total)
        #  ① 꺾임 (s < s_min) 재방문 = 같은 가닥의 연속 — 두 위치를 옛 셀 한 노드로 합친다 (접합 아님 · J11 단락 판정 밖)
        mg = np.asarray(reg.get('self_merge', np.zeros((0, 2), np.int64)), np.int64).reshape(-1, 2)
        if len(mg):
            uf0 = _UF()
            for p_, q_ in mg:
                uf0.union(int(self.pos_dof[p_]), int(self.pos_dof[q_]))
            for x in list(uf0.p):
                rep[x] = uf0.find(x)
        #  ② 접합 축약 (R_j′ = 0 · J6) — 단락 판정 (J11) 대상은 이 무리뿐
        con = np.flatnonzero(mode == MODE_CONTRACT)
        uf = _UF()
        for k in con:
            uf.union(int(rep[pu[k]]), int(rep[pv[k]]))
        members = {}
        for x in list(uf.p):
            members.setdefault(uf.find(x), []).append(x)
        if members:
            jr = np.arange(self.n_total)
            for r_, ms in members.items():
                jr[np.asarray(ms)] = r_
            rep = jr[rep]
        self.n_contracted = int(len(con))
        self.n_self_merged = int(len(mg))
        Ab2 = rep[self._plate_owner(Ab, False)] if Ab is not None else np.zeros(0, np.int64)
        At2 = rep[self._plate_owner(At, True)] if At is not None else np.zeros(0, np.int64)
        gb = np.asarray(gb if gb is not None else [], np.float64); gt = np.asarray(gt if gt is not None else [], np.float64)
        U = np.concatenate([x[0] for x in self.E]) if self.E else np.zeros(0, np.int64)
        V = np.concatenate([x[1] for x in self.E]) if self.E else np.zeros(0, np.int64)
        G = np.concatenate([x[2] for x in self.E]) if self.E else np.zeros(0)
        CAT = np.concatenate([x[3] for x in self.E]) if self.E else np.zeros(0, np.int64)
        SA = np.concatenate([x[4] for x in self.E]) if self.E else np.zeros(0)
        SB = np.concatenate([x[5] for x in self.E]) if self.E else np.zeros(0)
        IA = np.concatenate([x[6] for x in self.E]) if self.E else np.zeros(0, np.int64)
        IB = np.concatenate([x[7] for x in self.E]) if self.E else np.zeros(0, np.int64)
        TG = np.concatenate([x[8] for x in self.E]) if self.E else np.zeros(0, np.int64)
        U = rep[U]; V = rep[V]
        keep = (U != V) & (G > 0.0)
        U, V, G, CAT, SA, SB, IA, IB, TG = (U[keep], V[keep], G[keep], CAT[keep], SA[keep], SB[keep], IA[keep], IB[keep],
                                            TG[keep])
        # 단락 (J11) — 축약 무리가 두 판에 다 닿음
        short = False
        big = [r_ for r_, ms in members.items() if len(ms) >= 2]
        if big:
            bs = set(Ab2.tolist()); ts = set(At2.tolist())
            short = any((r_ in bs and r_ in ts) for r_ in big)
        # 실제 그래프 연결 성분 (J7 · J12 · E3)
        from scipy.sparse.csgraph import connected_components
        n = self.n_total
        A = sparse.coo_matrix((np.ones(len(U), np.int8), (U, V)), shape=(n, n))
        ncomp, lab = connected_components(A, directed=False)
        is_rep = rep == np.arange(n)
        bot_c = np.zeros(ncomp, bool); top_c = np.zeros(ncomp, bool)
        bot_c[lab[Ab2]] = True; top_c[lab[At2]] = True
        kept_c = bot_c | top_c
        thr_c = bot_c & top_c
        kept = kept_c[lab] & is_rep
        n_kept = int(kept.sum())
        n_through = int((thr_c[lab] & is_rep).sum())
        self.stats = {'n_extra_dofs': int(self.n_total - self.n_cells), 'n_contracted': self.n_contracted,
                      'n_floating_dropped': int((is_rep & ~kept).sum()), 'n_through_dof': n_through,
                      'n_plate_reachable_dof': n_kept, 'short': bool(short), 'tombstones': dict(self.tomb),
                      'n_unreg_fused': int(self.n_unreg_fused), 'n_junction_edges': int(np.sum(TG >= 0)),
                      'n_self_fused_faces': int(self.n_self_fused), 'n_self_merged_revisits': int(self.n_self_merged)}
        if short:
            return {'reason': 'cjunc_electrode_short'}
        if n_kept == 0:
            return {'reason': 'all_floating_dropped'}
        if n_through == 0:
            return {'reason': 'no_through_component'}
        new = -np.ones(n, np.int64)
        new[kept] = np.arange(n_kept)
        ek = kept[U] & kept[V]
        U, V, G, CAT, SA, SB, IA, IB, TG = U[ek], V[ek], G[ek], CAT[ek], SA[ek], SB[ek], IA[ek], IB[ek], TG[ek]
        self._jidx = np.flatnonzero(TG >= 0)
        self._jinst = TG[self._jidx]
        u, v = new[U], new[V]
        bk = kept[Ab2]; tk = kept[At2]
        Abn, gbn = new[Ab2[bk]], gb[bk]
        Atn, gtn = new[At2[tk]], gt[tk]
        cbn = tuple(np.asarray(x)[bk] for x in cb) if cb is not None else None
        ctn = tuple(np.asarray(x)[tk] for x in ct) if ct is not None else None
        diag = np.zeros(n_kept)
        np.add.at(diag, u, G); np.add.at(diag, v, G)
        np.add.at(diag, Abn, gbn); np.add.at(diag, Atn, gtn)
        b = np.zeros(n_kept)
        np.add.at(b, Abn, gbn)
        L = sparse.coo_matrix((np.concatenate([-G, -G, diag]), (np.concatenate([u, v, np.arange(n_kept)]),
                                                                  np.concatenate([v, u, np.arange(n_kept)]))),
                              shape=(n_kept, n_kept)).tocsr()
        self.sys = {'u': u, 'v': v, 'G': G, 'CAT': CAT, 'SA': SA, 'SB': SB, 'IA': IA, 'IB': IB, 'Ab': Abn, 'gb': gbn,
                    'At': Atn, 'gt': gtn, 'n': n_kept}
        return {'L': L, 'b': b, 'Ab': Abn, 'gb': gbn, 'At': Atn, 'gt': gtn, 'cb': cbn, 'ct': ctn, 'n_dof': n_kept}

    def record(self, phi):
        """원장을 읽는 소산 분담 · 접합 전류 (E1 · E2 · E4′) — 같은 단위 (코드) 로만 합친다."""
        s = self.sys
        u, v, G, CAT = s['u'], s['v'], s['G'], s['CAT']
        dphi = phi[u] - phi[v]
        P = G * dphi * dphi
        Pb = s['gb'] * (phi[s['Ab']] - 1.0) ** 2
        Pt = s['gt'] * (phi[s['At']]) ** 2
        Ptot = float(P.sum() + Pb.sum() + Pt.sum())
        share = {k: 0.0 for k in _CAT}
        share['sdcp_cell'] = 0.0
        share['plate'] = float(Pb.sum() + Pt.sum())
        sv = CAT == _CAT['sv_face']
        share['sv_face'] = float(P[sv].sum())
        rest = ~sv
        ia5 = (s['IA'] == 5) & rest; ib5 = (s['IB'] == 5) & rest
        with np.errstate(invalid='ignore', divide='ignore'):
            fa = np.where(ia5, s['SB'] / (s['SA'] + s['SB']), 0.0)        # a 쪽 (SDCP) 반셀 몫 = σb/(σa+σb)
            fb = np.where(ib5, s['SA'] / (s['SA'] + s['SB']), 0.0)
        fa = np.nan_to_num(fa); fb = np.nan_to_num(fb)
        ps = P * (fa + fb)
        share['sdcp_cell'] = float(ps[rest].sum())
        for k, c in _CAT.items():
            if k == 'sv_face':
                continue
            m = CAT == c
            share[k] = float((P[m] * (1.0 - fa[m] - fb[m])).sum())
        tot = sum(share.values())
        frac = {k: (x / Ptot if Ptot > 0 else 0.0) for k, x in share.items()}
        jI = np.full(len(self.reg['instances']['fi']), np.nan)       # instance 마다 접합 전류 (간선 없는 instance = NaN)
        jI[self._jinst] = G[self._jidx] * dphi[self._jidx]
        I_bot = float(np.sum(s['gb'] * (1.0 - phi[s['Ab']])))
        sv_total = share['sv_face'] + share['sdcp_cell']
        sv_I = float(np.sum(np.abs(G[sv] * dphi[sv]))) / I_bot if I_bot > 0 else None
        return {'P_total_code': Ptot, 'P_sum_check_code': float(tot), 'dissipation_share': frac,
                'sv_dominant': bool(sv_total >= share['vv_junction'] and sv_total > 0.0),
                'sv_face_abs_current_over_I': sv_I, 'junction_current_code': jI, 'I_bot_code': I_bot}


def early_record(plan, reason=None):
    r = dict(plan['record'])
    r.update(r['counts'])
    r['solved'] = False
    if reason:
        r['reason'] = reason
    return r


# ═════════════════════════ J2b census (VA · v0 = 간선 없음) ═════════════════════════
def va_census(add_pts, add_phase, add_fid, add_kind, am_c, am_r, *, r_f_um, tol_fs_um, gap_tol=2.0):
    """J2b fiber–sphere — 중심선 선분 ↔ 구 **중심** 최근접 ≤ r_f + R_AM + tol_fs 인 (fid, AM) 쌍 수 (v3 §5 · 판정문: 2.12 > 2.075)."""
    P, PH, F, K = _input_check(add_pts, add_phase, add_fid, add_kind)
    rej = []
    paths = [(f, r, kp) for f, r, kp in _paths_of(P, PH, F, K, 2, rej, 'VGCF') if kp]
    segs, _ = _segments_of(paths, P, gap_tol)
    am_c = np.asarray(am_c, np.float64).reshape(-1, 3); am_r = np.asarray(am_r, np.float64).ravel()
    n = 0
    for f in np.unique(segs['fid']):
        m = segs['fid'] == f
        for c, r in zip(am_c, am_r):
            d2, _, _ = pt_seg_d2(np.repeat(c[None], int(m.sum()), 0), segs['P0'][m], segs['P1'][m])
            if math.sqrt(float(d2.min())) <= float(r_f_um) + float(r) + float(tol_fs_um):
                n += 1
    return n
