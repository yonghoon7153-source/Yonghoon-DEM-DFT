#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rint ② S1 — PTFE 면 개구율 연산자 `face_alpha` (Codex R18 Q6 · 설계 v1 §3 · 1저자 10-20 설계 §10 N1–N18 권고대로).

무엇:  PTFE 피브릴 **중심선** (MPM phase 4 점 · fid · kind) + 지름 (규약 선택) 으로 캡슐 C_i = {x : dist(x, s_i) ≤ r_P} 를 세우고,
       STEP3 복셀 FV 의 면 f (셀 a · b 사이 h × h 정사각형) 마다 **열린 면적분율**
           α_f = 1 − (1/K²) Σ_q 1[x_q ∈ ∪_i C_i]       (x_q = 면 위 K × K 중점 구적점 · K = 8 봉인)
       을 구해 면 컨덕턴스를 g_f = α_f · g0_f (g0 = 조화평균 · 불투과 PTFE (가정 고정) · 막 직렬 항 없음) 로 둔다.
       **셀을 찍지 않는다** — sid 격자 = `ptfe_stamp off` 격자 (PTFE 셀 0).  R18 Q6 끝 문단: 셀 스탬프 (capsule 예약값의
       원래 뜻) 와 면 개구율은 *"다른 물건"* — 그래서 새 이름 `face_alpha` (예약값 `capsule` 은 그대로 거부 · N1).

어디에 걸리나 (설계 §3-1 · 같은 물체 안 면 면제 = '자르기' 인공물 방지):
  전자 — 두 셀 다 전자 도체인 면 중 **면제가 아닌** 것 (AM|탄소 · AM|SDCP · 탄소|SDCP · AM_S|AM_P · 같은 sid AM 의 다른 pid = AM–AM 목).
  이온 — 두 셀 다 이온 도체인 면 중 면제가 아닌 것 (SE|SE · SE|SDCP — SE 는 입자 번호가 없는 연속체).
  면제 — ⓐ 같은 AM 입자 (pid 같음 ≥ 0) ⓑ 같은 탄소 상 (3|3 · 4|4 · 8|8 — 접합은 S2 의 P-junc 법칙 소관) ⓒ SDCP|SDCP.
  판 결합 — v0 는 α 를 **걸지 않는다** (판 쪽 면을 캡슐이 가로지르는 기둥 수만 기록 · F17 · `plate_coupling_factor`).
  α = 0 면 = 절단 (E3 — 실제 간선 그래프로 떠 있는 성분 가지치기 · 사방 절단 셀 = 고립 · 수 기록).

지름 (§1-2 #15 · N12): (가) **주** = 모든 경로 Ø0.248 µm (rope · [카드] Lee 2025 EES Fig. S2c) = **1저자 규약 선택** — 문헌 밴드는
  반증력 0 (R18 Q3) → 판정 문장 한정어 `DIA_UNCHECKED` 필수 · (다) 민감도만 = 경로 정준 키 해시로 13 % Ø0.248 · 87 % Ø0.048
  (표현 부피 ≈ 0.16 배 → 부피 밴드 밖 → **보고만**) · (나) 시더 d_i 분포 = 안 쓴다.  중심선 길이 = 시더 처방 그대로 (부피 보존 길이 ·
  지름을 부피에 다시 맞추지 않는다).
부피 (F11): 조각 (gap 분할 뒤 연속 폴리라인) 마다 Σ(선분 길이 · π r²) + 구 하나 (4/3 · π r³ = 조각 양끝 반구) · 경로 사이 겹침 미차감.
  실침대 비 = `CL-60` 등록의 2 배 밴드 [0.5, 2] 안이어야 S1 사용 — 밖이면 기록 (`out_of_band`) · R 판정 = NOT_COMPUTED (판정 사슬 소관).
  ★ 10-21 (Codex A4 · Q11) — 이 수는 **명목 tube 체적** (`VOLUME_BASIS`) 이지 굽은 · 자기 중첩 · 교차 캡슐의 **합집합 체적이 아니다**
  (교차 두 캡슐이면 Steinmetz 16r³/3 만큼 크다 — F19).  기록 칸 이름을 나눈다: `capsule_nominal_um3` (= 옛 `capsule_um3` · 밴드 비의 기준) ·
  `capsule_union_um3` = None (v0 미계산 · `capsule_union_status`).
구적 (★ 10-21 · Codex §4-1 · Q11) — K = 8 고정은 결과 뒤 조정을 막지만 정확하지는 않다: 정사각형 ∩ 중앙 원 (r/h 0.65) 의 참 α = 0.01345 인데
  K 4 · K 8 중점 구적 = 0 (거짓 절단 → 유일 경로면 단자 G 0 · F18).  면적 오차 (≤ 1/K²) 와 연결성 · 단자 G 처분을 나눠 기록한다:
  계획 `false_cut_check` = α = 0 면 수 · 그중 고운 구적 (K_refine = 2K) 에서 열리는 수 (진단 · 판정 · α 값은 그대로 K 8).
면제 가정 표지 (★ 10-21 · Codex §4-1) — 같은 AM pid 면제 = 한 입자 안을 자르지 않는 정의 · 같은 탄소 sid · SDCP|SDCP 면제 = 여러 물체를 한
  연속체로 묶는 **상 수준 융합 가정** (`EXEMPT_ASSUMPTIONS` · 증거 칸 `exempt_assumptions` · 계약이 대조).  VV 누락은 S2 P-junc 가 일부 보충 ·
  SDCP–SDCP 가 같은 방식으로 검증됐다는 뜻은 아니다.

⛔ 지위 — 다음 세대 (`p3ca`) 기구 · 기본 끔 (`solve_sigma_z(face_alpha=None)` = 옛 경로 비트 같음) · 생산 규약은 `centerline` (CL-60)
  그대로 · 이름 *"partial-volume PTFE"* 금지 (R18 P1-1) · 지름을 우리 피브릴의 물성 · 측정값으로 해석하지 않는다 · 펠릿 0.97 에
  지름 · K · R_int 를 다시 맞추지 않는다 (= calibration · R18 Q6 끝) · 진단 (je · 소산 분담 · |J| 점군 · Joule) 은 α 를 원장에서
  읽기 전까지 face_alpha 해를 **거부** (E2 · v0 = LEAN 2 · 3 만).
"""
import hashlib
import json
import math

import numpy as np

S1_OPERATOR_VERSION = 's1-face-alpha-v1'
PTFE_STAMP = 'face_alpha'
PLAN_KIND = 'ptfe_face_alpha_plan'
EDGES_KIND = 'ptfe_face_alpha_edges'
K_SEALED = 8                                   # α 구적 K — **지금 봉인** (F7 을 보고 고르지 않는다 · RINTG-06 · N12) · 바꾸면 새 세대 id
ROPE_D_UM = 0.248                              # (가) rope 지름 = 1저자 규약 선택 (`DIA_UNCHECKED`)
FIBRE_D_UM = 0.048                             # (다) 두 집단 민감도의 개별 섬유 지름 (보고만)
TWO_POP_ROPE_FRAC = 0.13                       # (다) rope 개수비 ([카드] Lee 2025 EES Fig. S2c · N = 100 · rope 13 · fibre 87)
DIA_LAWS = ('rope', 'two_pop')
CHANNELS = ('electronic', 'ionic')
CHANNEL_CHOICES = ('both', 'electronic', 'ionic')
GAP_TOL = 2.0                                  # 폴리라인 끊기 = 선분 스탬프와 같은 규칙 (`step3_sigma._fibre_segment_ijk` · §1-2 #25)
VOLUME_BAND = (0.5, 2.0)                       # CL-60 등록 2 배 밴드 (ptfe_convention_prereg_20260829.md §2-1)
PLATE_RULE = 'v0-not-applied'                  # 판 결합 면에 α 를 걸지 않는다 (기둥 수만 기록)
EXEMPT_RULE = 'same-object-v1'                 # 같은 AM pid · 같은 탄소 상 · SDCP|SDCP (★ 10-21 — 뒤 둘은 같은 물체가 아니라 상 융합 가정)
#: ★ 10-21 (Codex §4-1 · Q11) — 면제의 뜻 표지 (증거 칸 · p3ca id 밖 · 물리 규칙은 EXEMPT_RULE 그대로)
EXEMPT_ASSUMPTIONS = {'am_same_pid': 'same_particle_interior', 'carbon_same_sid': 'phase_level_fusion_assumed',
                      'sdcp_sdcp': 'phase_level_fusion_assumed'}
#: ★ 10-21 (Codex A4 · Q11) — 기록 부피의 정의 (명목 tube = Σ 선분 πr²L + 조각마다 구 하나 · 겹침 · 굽힘 미차감 — 합집합 아님)
VOLUME_BASIS = 'nominal_tube_v1'
#: ★ 10-21 (Codex §4-1) — 거짓 절단 진단의 고운 구적 배수 (K_refine = 2K · 진단만 · α 값 · 판정은 봉인 K 그대로)
FALSE_CUT_REFINE = 2
FACE_RULE = 'face-classes-v1'                  # 전자 = 다른 상 · 같은 sid AM 다른 pid / 이온 = SE|SE · SE|SDCP (면제 밖)
CENTERLINE_SOURCE = 'mpm-phase4-fid-kind-v1'   # 중심선 = MPM phase 4 점 · `fibre.npy` fid · `_kind.npy` (경로)
SOLVES = ('electronic_main', 'electronic_wetted', 'electronic_bare', 'ionic')   # = run_contract.INTERFACE_SOLVES 키
OK_STATUSES = ('applied', 'absent_geometry', 'failed', 'disabled', 'not_requested')   # run_contract.INTERFACE_OK_STATUSES 의 부분
DIAGNOSTICS_V0 = {'je': 'not_computed', 'dissipation_share': 'not_computed', 'ion_dissipation_share': 'not_computed',
                  'field': 'refused_v0', 'joule': 'refused_v0',
                  'why': 'S1 v0 — 진단이 α 를 원장에서 읽기 전 (E2 · 설계 §3-3) · LEAN 2 · 3 만'}
#: 화면 표지 (설계 §3-6) — 단일 출처.  payload 가 매니페스트 `ca_ext.ptfe_face.evidence.label` 로 싣고 웹앱 템플릿이 그것을 읽는다.
LABEL = 'PTFE 면 개구율 (α · Ø0.248 rope = 규약 선택 · 불투과 가정 · 전자/이온)'
PROTOCOL_KEYS = ('operator', 'channels', 'dia_law', 'dia_um', 'K', 'impermeable', 'gap_tol', 'face_rule', 'exempt_rule',
                 'plate_rule', 'centerline')
_FACE_PLANE_OFFSET = 1.0                       # 축 a 면 = 아래 셀 c 의 위쪽 면 (평면 lo_a + (c_a + 1)·h) — 변이 시험이 0.5 로 바꾼다
_SID_NAME = {1: 'AM_S', 2: 'AM_P', 3: 'VGCF', 4: 'SuperP', 5: 'SDCP', 6: 'SE', 7: 'PTFE', 8: 'SWCNT', 9: 'SE_blk'}


def _grid_fp(a):
    """격자 지문 — `step3_sigma._grid_fp` 그대로 (사본 금지 · 규율 ①).  격자는 수치 배열 계약 — 객체 (· 구조체 객체 칸) dtype 격자는
    원소 **포인터** 바이트가 지문에 들어가 프로세스 사이에서 재현되지 않으므로 (RINT-23 부류 · 2 일 차) 넘기기 전에 거부한다."""
    if a is not None and np.asarray(a).dtype.hasobject:
        raise TypeError(f'face_alpha: 격자 지문 — 객체 dtype ({np.asarray(a).dtype}) 격자 거부 (포인터 바이트 · RINT-23 부류 · '
                        f'격자는 수치 배열)')
    from step3_sigma import _grid_fp as _g
    return _g(a)


def _h16(*parts):
    h = hashlib.blake2b(digest_size=16)
    for p in parts:
        h.update(p if isinstance(p, (bytes, bytearray)) else str(p).encode('utf-8'))
        h.update(b'|')
    return h.hexdigest()


def _check_K(K):
    if isinstance(K, bool) or not isinstance(K, (int, np.integer)) or int(K) < 1:
        raise ValueError(f'face_alpha: 구적 K = {K!r} — 양의 정수여야 한다 (봉인 {K_SEALED})')
    return int(K)


def _inplane(axis):
    return {0: (1, 2), 1: (0, 2), 2: (0, 1)}[int(axis)]


# ══ 캡슐 (중심선 + 지름) ═══════════════════════════════════════════════════════════════════════
def _path_radius(Q, dia_law):
    """경로 하나의 반지름 + 부류.  rope = Ø0.248 · two_pop = 경로 정준 키 (점열 float64 바이트) 해시로 13 % rope (순열 불변)."""
    if dia_law == 'rope':
        return ROPE_D_UM / 2.0, 'rope'
    u = int.from_bytes(hashlib.sha256(np.ascontiguousarray(Q, np.float64).tobytes()).digest()[:8], 'big') / 2.0 ** 64
    return ((ROPE_D_UM / 2.0, 'rope') if u < TWO_POP_ROPE_FRAC else (FIBRE_D_UM / 2.0, 'fibre'))


def _caps_fp(caps):
    """캡슐 기하 지문 — 지름 법칙 · gap_tol · 선분 끝점 · 반지름 바이트 (계획 입구가 다시 계산해 기하 변조를 막는다)."""
    if not caps.get('n_segments'):
        return _h16('caps-v1', caps.get('dia_law'), repr(caps.get('gap_tol')), 'empty')
    return _h16('caps-v1', caps.get('dia_law'), repr(caps.get('gap_tol')),
                np.ascontiguousarray(np.asarray(caps['A'], np.float64)).tobytes(),
                np.ascontiguousarray(np.asarray(caps['B'], np.float64)).tobytes(),
                np.ascontiguousarray(np.asarray(caps['r'], np.float64)).tobytes())


def build_capsules(pts, fid, kind=None, *, dia_law='rope', gap_tol=GAP_TOL):
    """PTFE 중심선 점열 → 캡슐 기하 (선분 A–B · 반지름 · 조각 · 부피 · 표본점).  입력 계약 (설계 §3-3 · F15):
    점 float64 유한 · fid 정수 ≥ 0 · kind (있으면) 정수 ∈ {0, 1} 이고 PTFE 는 전부 경로 (1) · 길이 정확 일치 · 같은 fid 는 연속 한
    블록 (떨어진 두 블록 = 거부) · 정확 중복 경로 = 거부 · 점 하나인 조각 = 구 캡슐 (수 기록).  입력을 고치거나 버리지 않는다."""
    if dia_law not in DIA_LAWS:
        raise ValueError(f'face_alpha: 지름 법칙 {dia_law!r} — {DIA_LAWS} 중 하나 ((나) 시더 d_i 분포는 안 쓴다 · N12)')
    g_t = float(gap_tol)
    if not (math.isfinite(g_t) and g_t > 0):
        raise ValueError(f'face_alpha: gap_tol = {gap_tol!r} (유한 양수)')
    P = np.asarray(pts)
    if P.dtype == object or P.dtype == bool or not (np.issubdtype(P.dtype, np.floating) or np.issubdtype(P.dtype, np.integer)):
        raise ValueError(f'face_alpha: 중심선 좌표는 수치 배열이어야 한다 (dtype {P.dtype})')
    if P.size == 0:
        P = np.zeros((0, 3))
    if P.ndim != 2 or P.shape[1] != 3:
        raise ValueError(f'face_alpha: 중심선 좌표 모양 {P.shape} — (n, 3) 이어야 한다')
    P = P.astype(np.float64)
    if not np.isfinite(P).all():
        raise ValueError('face_alpha: 중심선 좌표에 NaN · inf — 조립 전 거부 (RIMPR-04 교훈 — 입력 유한 ≠ 파생 유한)')
    F = np.asarray(fid)
    if F.ndim != 1 or len(F) != len(P):
        raise ValueError(f'face_alpha: fid 길이 {F.shape} ≠ 점 {len(P)} — 조용히 점 스탬프로 내려가지 않는다 (RIMPR-01)')
    if len(F) and (F.dtype == bool or not np.issubdtype(F.dtype, np.integer)):
        raise ValueError(f'face_alpha: fid 는 정수 배열이어야 한다 (dtype {F.dtype} — 실수 · 문자열 (전각 숫자 포함) 거부)')
    F = F.astype(np.int64)
    if len(F) and (F < 0).any():
        raise ValueError('face_alpha: PTFE 점에 fid < 0 — 중심선을 세울 경로가 없다')
    if kind is not None:
        Kd = np.asarray(kind)
        if Kd.ndim != 1 or len(Kd) != len(P):
            raise ValueError(f'face_alpha: kind 길이 {Kd.shape} ≠ 점 {len(P)}')
        if len(Kd) and not (Kd.dtype == bool or np.issubdtype(Kd.dtype, np.integer)):
            raise ValueError(f'face_alpha: kind 는 정수 배열이어야 한다 (dtype {Kd.dtype})')
        if len(Kd) and not np.isin(Kd.astype(np.int64), (0, 1)).all():
            raise ValueError('face_alpha: kind 값은 {0, 1} 이어야 한다')
        if len(Kd) and (Kd.astype(np.int64) == 0).any():
            raise ValueError('face_alpha: PTFE fid 가 경로가 아니다 (kind = 그룹) — 캡슐 중심선이 없다')
    n = len(P)
    caps = {'kind': 'ptfe_capsules', 'dia_law': dia_law, 'gap_tol': g_t, 'n_paths': 0, 'n_pieces': 0, 'n_point_pieces': 0,
            'n_segments': 0, 'volume_um3': 0.0, 'r_max': 0.0, 'dia_classes': {'rope': 0, 'fibre': 0},
            'A': np.zeros((0, 3)), 'B': np.zeros((0, 3)), 'r': np.zeros(0), 'seg_path': np.zeros(0, np.int64),
            'samples': np.zeros((0, 3)), 'sample_seg': np.zeros(0, np.int64), 's_spacing': 0.0}
    if n == 0:
        caps['fp'] = _caps_fp(caps)
        return caps
    starts = np.r_[0, np.flatnonzero(np.diff(F) != 0) + 1]
    run_f = F[starts]
    if len(np.unique(run_f)) != len(run_f):
        raise ValueError('face_alpha: 같은 fid 가 떨어진 두 블록 — 경로를 확정할 수 없다 (거부 · 조용히 잇지 않는다)')
    ends = np.r_[starts[1:], n]
    seen = set()
    A, B, R, SP = [], [], [], []
    vol = 0.0
    n_pieces = n_point = 0
    cls = {'rope': 0, 'fibre': 0}
    for ip, (s, e) in enumerate(zip(starts, ends)):
        Q = P[s:e]
        key = Q.tobytes()
        if key in seen:
            raise ValueError(f'face_alpha: 정확 중복 경로 (fid {int(F[s])}) — 같은 PTFE 를 두 번 셀 수 없다')
        seen.add(key)
        r, c_ = _path_radius(Q, dia_law)
        cls[c_] += 1
        if len(Q) == 1:
            pieces = [Q]
        else:
            d = np.linalg.norm(np.diff(Q, axis=0), axis=1)
            med = float(np.median(d)) if len(d) else 0.0
            brk = (np.nonzero(d > g_t * med)[0] + 1) if med > 0 else np.array([], int)
            pieces = np.split(Q, brk) if len(brk) else [Q]
        for Rp in pieces:
            n_pieces += 1
            if len(Rp) == 1:
                n_point += 1
                A.append(Rp[:1])
                B.append(Rp[:1])
                R.append(np.array([r]))
                SP.append(np.array([ip]))
                vol += 4.0 / 3.0 * math.pi * r ** 3
                continue
            A.append(Rp[:-1])
            B.append(Rp[1:])
            R.append(np.full(len(Rp) - 1, r))
            SP.append(np.full(len(Rp) - 1, ip))
            vol += float(np.linalg.norm(np.diff(Rp, axis=0), axis=1).sum()) * math.pi * r * r + 4.0 / 3.0 * math.pi * r ** 3
    A = np.vstack(A)
    B = np.vstack(B)
    R = np.concatenate(R)
    SP = np.concatenate(SP).astype(np.int64)
    r_max = float(R.max())
    spacing = 0.5 * r_max
    L = np.linalg.norm(B - A, axis=1)
    ns = np.maximum(1, np.ceil(L / spacing).astype(np.int64)) + 1
    ns[L == 0] = 1
    seg_of = np.repeat(np.arange(len(A), dtype=np.int64), ns)
    first = np.repeat(np.cumsum(ns) - ns, ns)
    k = np.arange(int(ns.sum()), dtype=np.int64) - first
    t = np.where(ns[seg_of] > 1, k / np.maximum(ns[seg_of] - 1, 1), 0.0)
    samples = A[seg_of] + t[:, None] * (B - A)[seg_of]
    caps.update(n_paths=int(len(starts)), n_pieces=int(n_pieces), n_point_pieces=int(n_point), n_segments=int(len(A)),
                volume_um3=float(vol), r_max=r_max, dia_classes=cls, A=A, B=B, r=R, seg_path=SP,
                samples=samples, sample_seg=seg_of, s_spacing=float(spacing))
    caps['fp'] = _caps_fp(caps)
    return caps


def capsule_volume_um3(caps):
    return float(caps['volume_um3'])


def capsule_summary(caps):
    #  ★ 10-21 — volume_um3 = 명목 tube 체적 (VOLUME_BASIS · 합집합 아님) — 이름 칸을 같이 싣는다
    #  ⚠ dict-union `|` 금지 — kgy dem-venv = Python 3.8.10 (`|` 는 3.9+ · 10-24 kgy S0 단계 1 이 여기서 TypeError 로 멈췄다)
    return {**{k: caps[k] for k in ('n_paths', 'n_pieces', 'n_point_pieces', 'n_segments', 'volume_um3')},
            'dia_classes': dict(caps['dia_classes']), 'volume_basis': VOLUME_BASIS}


def _tree(caps):
    t = caps.get('_tree')
    if t is None:
        from scipy.spatial import cKDTree
        t = cKDTree(caps['samples'])
        caps['_tree'] = t
    return t


def _alpha_from_cover(count, K):
    """덮인 구적점 수 → α = 1 − count / K² (K = 8 이면 이진 정확 · α ∈ {0, 1/K², …, 1})."""
    return 1.0 - np.asarray(count, np.float64) / float(K * K)


def _quad_offsets(axis, K, h):
    b, c = _inplane(axis)
    u = (np.arange(K, dtype=np.float64) + 0.5) / K * h
    off = np.zeros((K * K, 3))
    off[:, b] = np.repeat(u, K)
    off[:, c] = np.tile(u, K)
    return off


_FACE_CHUNK = 100_000                          # 면 묶음 (실침대 면 수 10⁶ 규모에서 KD 쌍 · 덮임 배열 메모리를 묶음 크기로 묶는다)


def face_alpha_values(caps, axis, lower_ijk, lo, vox, K=K_SEALED):
    """면 α — 축 `axis` 의 면 (아래 셀 `lower_ijk` 와 그 위 셀 사이 · 평면 lo_a + (c_a + 1)·h) 마다 K × K 중점 구적.
    캡슐 안 판정 = 중심선 선분까지 거리 ≤ r (닫힌 캡슐 · `_ball_cells` 와 같은 ≤).  캡슐이 없으면 α ≡ 1.
    면 묶음마다 따로 푼다 (값은 묶음 크기와 무관 — 면마다 독립)."""
    K = _check_K(K)
    lower = np.asarray(lower_ijk, np.int64).reshape(-1, 3)
    out = np.ones(len(lower))
    if len(lower) == 0 or caps['n_segments'] == 0:
        return out
    for f0 in range(0, len(lower), _FACE_CHUNK):
        out[f0:f0 + _FACE_CHUNK] = _face_alpha_chunk(caps, axis, lower[f0:f0 + _FACE_CHUNK], lo, vox, K)
    return out


def _face_alpha_chunk(caps, axis, lower, lo, vox, K):
    h = float(vox)
    lo = np.asarray(lo, np.float64)
    b, c = _inplane(axis)
    base = lo[None, :] + lower.astype(np.float64) * h
    base[:, axis] = lo[axis] + (lower[:, axis].astype(np.float64) + _FACE_PLANE_OFFSET) * h
    ctr = base.copy()
    ctr[:, b] += 0.5 * h
    ctr[:, c] += 0.5 * h
    from scipy.spatial import cKDTree
    rad = caps['r_max'] + h * math.sqrt(0.5) + 0.5 * caps['s_spacing']
    rad = rad * (1.0 + 1e-9) + 1e-12
    sdm = cKDTree(ctr).sparse_distance_matrix(_tree(caps), rad, output_type='ndarray')
    if len(sdm) == 0:
        return np.ones(len(lower))
    nseg = int(caps['n_segments'])
    key = np.unique(sdm['i'].astype(np.int64) * nseg + caps['sample_seg'][sdm['j']])
    pf, ps = key // nseg, key % nseg
    off = _quad_offsets(axis, K, h)
    A, D, r2 = caps['A'], caps['B'] - caps['A'], caps['r'] ** 2
    covered = np.zeros((len(lower), K * K), bool)
    step = max(1, 2_000_000 // (K * K))
    for c0 in range(0, len(pf), step):
        f_, s_ = pf[c0:c0 + step], ps[c0:c0 + step]
        V = base[f_][:, None, :] + off[None, :, :] - A[s_][:, None, :]
        Ds = D[s_][:, None, :]
        L2 = (Ds * Ds).sum(-1)
        t = np.where(L2 > 0, (V * Ds).sum(-1) / np.where(L2 > 0, L2, 1.0), 0.0)
        t = np.clip(t, 0.0, 1.0)
        W = V - t[..., None] * Ds
        inside = (W * W).sum(-1) <= r2[s_][:, None]
        st = np.flatnonzero(np.r_[True, f_[1:] != f_[:-1]])
        covered[f_[st]] |= np.logical_or.reduceat(inside, st, axis=0)
    return _alpha_from_cover(covered.sum(1), K)


def _candidate_cells(caps, lo, vox, shape):
    """캡슐 근처 셀 (중심이 어떤 중심선 선분에서 r + h√3/2 안 · 표본점 기준 보수적 상위집합) → 격자 bool."""
    h = float(vox)
    lo = np.asarray(lo, np.float64)
    shape = tuple(int(x) for x in shape)
    mask = np.zeros(shape, bool)
    S = caps['samples']
    if not len(S):
        return mask
    Rr = caps['r_max'] + h * math.sqrt(3.0) / 2.0 + 0.5 * caps['s_spacing']
    Rr = Rr * (1.0 + 1e-9) + 1e-12
    w = int(math.ceil(Rr / h)) + 1
    g = np.arange(-w, w + 1)
    offs = np.stack(np.meshgrid(g, g, g, indexing='ij'), -1).reshape(-1, 3)
    n = np.asarray(shape)
    step = max(1, 3_000_000 // len(offs))
    for c0 in range(0, len(S), step):
        p = S[c0:c0 + step]
        cells = np.floor((p - lo) / h).astype(np.int64)[:, None, :] + offs[None, :, :]
        d2 = (((lo + (cells + 0.5) * h) - p[:, None, :]) ** 2).sum(-1)
        ok = (d2 <= Rr * Rr) & (cells >= 0).all(-1) & (cells < n).all(-1)
        q = cells[ok]
        mask[q[:, 0], q[:, 1], q[:, 2]] = True
    return mask


# ══ 계획 (채널 하나 · 격자 하나에 묶인 α 행) ══════════════════════════════════════════════════════
def _channel_cond(channel, sigma_of_sid, sid, lin=None):
    """그 채널의 도체 셀 (σ > 0) — 표 (sid → σ) 또는 복셀별 σ 장.  `lin` (평탄 번호) 을 주면 그 셀들만 (격자 전체 float 임시 없음 ·
    판정식은 솔버 `sigma_field` 와 같은 `σ[sid] > 0` — 표 밖 sid 는 같은 IndexError)."""
    s = np.asarray(sigma_of_sid, np.float64)
    sid = np.asarray(sid)
    if s.ndim == 1:
        return (s[sid] > 0) if lin is None else (s[sid.reshape(-1)[lin]] > 0)
    if s.shape == sid.shape:
        return (s > 0) if lin is None else (s.reshape(-1)[lin] > 0)
    raise ValueError(f'face_alpha: σ 표 모양 {s.shape} 를 sid {sid.shape} 에 쓸 수 없다')


def _exempt_mask(channel, sa, sb, pa, pb):
    """같은 물체 안 면 면제 (설계 §3-1) — ⓐ 같은 AM 입자 (pid 같음 ≥ 0) ⓑ 같은 탄소 상 3|3 · 4|4 · 8|8 ⓒ SDCP|SDCP."""
    sa = np.asarray(sa)
    sb = np.asarray(sb)
    ex = (sa == sb) & np.isin(sa, (3, 4, 5, 8))
    if channel == 'electronic' and pa is not None:
        pa = np.asarray(pa)
        pb = np.asarray(pb)
        ex |= np.isin(sa, (1, 2)) & np.isin(sb, (1, 2)) & (pa == pb) & (pa >= 0)
    return ex


def _class_key(sa, sb):
    lo_, hi_ = (sa, sb) if sa <= sb else (sb, sa)
    return f'{_SID_NAME.get(int(lo_), str(int(lo_)))}|{_SID_NAME.get(int(hi_), str(int(hi_)))}'


def rows_fp(axes):
    parts = ['rows-v1']
    for ax, a in enumerate(axes):
        parts += [str(ax), np.ascontiguousarray(np.asarray(a['lin'], np.int64)).tobytes(),
                  np.ascontiguousarray(np.asarray(a['alpha'], np.float64)).tobytes()]
    return _h16(*parts)


def plan_fp(plan):
    body = {k: plan.get(k) for k in ('kind', 'version', 'channel', 'K', 'vox_um', 'fp_sid', 'fp_sig', 'fp_pid', 'fp_caps',
                                     'fp_rows')}
    body['lo_um'] = [float(x) for x in plan.get('lo_um') or ()]
    body['shape'] = [int(x) for x in plan.get('shape') or ()]
    return _h16('plan-v1', json.dumps(body, sort_keys=True, ensure_ascii=False, separators=(',', ':')))


def build_plan(sid, sigma_of_sid, caps, *, lo, vox, channel, pid=None, K=K_SEALED):
    """캡슐 + 격자 + 채널 → α 계획 (α < 1 인 자격 면만 · 축마다 아래 셀 선형번호 오름차순).  지문 (sid · σ · pid · 캡슐 · 행) 으로
    그 격자 · 그 채널에 묶인다 — 솔버 입구 (`require_plan`) 가 대조한다 (E5 · RIMP-05)."""
    if channel not in CHANNELS:
        raise ValueError(f'face_alpha: 채널 {channel!r} — {CHANNELS} 중 하나')
    K = _check_K(K)
    sid = np.asarray(sid)
    if sid.ndim != 3 or not np.issubdtype(sid.dtype, np.integer):
        raise ValueError(f'face_alpha: sid 는 3 차원 정수 격자여야 한다 ({sid.shape} {sid.dtype})')
    h = float(vox)
    if not (math.isfinite(h) and h > 0):
        raise ValueError(f'face_alpha: vox = {vox!r} (유한 양수)')
    lo = tuple(float(x) for x in lo)
    if len(lo) != 3 or not all(math.isfinite(x) for x in lo):
        raise ValueError(f'face_alpha: lo = {lo!r}')
    if channel == 'electronic':
        if pid is None:
            raise ValueError('face_alpha: 전자 채널은 pid 가 있어야 한다 (같은 AM 입자 면제 · AM–AM 목 판정)')
        pid = np.asarray(pid)
        if pid.shape != sid.shape:
            raise ValueError(f'face_alpha: pid 모양 {pid.shape} ≠ sid {sid.shape}')
    else:
        pid = None
    shape = sid.shape
    axes, counts = [], {}
    cand = _candidate_cells(caps, lo, h, shape) if caps['n_segments'] else None
    #  후보 셀 목록 (오름차순 평탄 번호) 에서만 면을 만든다 — 격자 전체 임시 (bool · float) 를 만들지 않는다 (실침대 10⁸ 셀).
    cl = np.flatnonzero(cand.reshape(-1)) if cand is not None else np.zeros(0, np.int64)
    cijk = np.stack(np.unravel_index(cl, shape), -1) if len(cl) else np.zeros((0, 3), np.int64)
    stride = (shape[1] * shape[2], shape[2], 1)
    sid_f = sid.reshape(-1)
    pid_f = pid.reshape(-1) if pid is not None else None
    for ax in range(3):
        if not len(cl) or shape[ax] < 2:
            axes.append({'lin': np.zeros(0, np.int64), 'alpha': np.zeros(0)})
            continue
        lo_lin = cl[cijk[:, ax] < shape[ax] - 1]
        lo_lin = lo_lin[cand.reshape(-1)[lo_lin + stride[ax]]]
        if len(lo_lin):
            cnd = (_channel_cond(channel, sigma_of_sid, sid, lo_lin)
                   & _channel_cond(channel, sigma_of_sid, sid, lo_lin + stride[ax]))
            lo_lin = lo_lin[cnd]
        if not len(lo_lin):
            axes.append({'lin': np.zeros(0, np.int64), 'alpha': np.zeros(0)})
            continue
        up_lin = lo_lin + stride[ax]
        s_a, s_b = sid_f[lo_lin], sid_f[up_lin]
        p_a = pid_f[lo_lin] if pid_f is not None else None
        p_b = pid_f[up_lin] if pid_f is not None else None
        keep = ~_exempt_mask(channel, s_a, s_b, p_a, p_b)
        lo_lin, s_a, s_b = lo_lin[keep], s_a[keep], s_b[keep]
        low = np.stack(np.unravel_index(lo_lin, shape), -1)
        al = face_alpha_values(caps, ax, low, lo, h, K)
        hit = al < 1.0
        lin, al, s_a, s_b = lo_lin[hit].astype(np.int64), al[hit], s_a[hit], s_b[hit]
        o = np.argsort(lin, kind='stable')
        lin, al, s_a, s_b = lin[o], al[o], s_a[o], s_b[o]
        axes.append({'lin': lin, 'alpha': al.astype(np.float64)})
        for a_, b_, v in zip(s_a.tolist(), s_b.tolist(), al.tolist()):
            ck = _class_key(a_, b_)
            cc = counts.setdefault(ck, {'n_alpha_lt1': 0, 'n_alpha0': 0, 'blocked_area_um2': 0.0})
            cc['n_alpha_lt1'] += 1
            cc['n_alpha0'] += int(v == 0.0)
            cc['blocked_area_um2'] += (1.0 - v) * h * h
    plan = {'kind': PLAN_KIND, 'version': S1_OPERATOR_VERSION, 'channel': channel, 'K': K, 'vox_um': h, 'lo_um': lo,
            'shape': tuple(int(x) for x in shape), 'axes': tuple(axes), 'counts': dict(sorted(counts.items())),
            'n_rows': int(sum(len(a['lin']) for a in axes)),
            'n_cut_rows': int(sum(int((a['alpha'] == 0).sum()) for a in axes)),
            'caps': caps, 'fp_sid': _grid_fp(sid), 'fp_sig': _grid_fp(np.asarray(sigma_of_sid, np.float64)),
            'fp_pid': (_grid_fp(pid) if pid is not None else None), 'fp_caps': caps['fp'],
            'false_cut_check': false_cut_check(caps, axes, shape, lo, h, K)}
    plan['fp_rows'] = rows_fp(plan['axes'])
    plan['fp_plan'] = plan_fp(plan)
    return plan


def false_cut_check(caps, axes, shape, lo, vox, K):
    """★ 10-21 (Codex §4-1 · Q11) — 거짓 절단 진단: 계획의 α = 0 면 (절단) 을 고운 구적 K_refine = `FALSE_CUT_REFINE`·K 로 다시 봐서
    열리는 (α > 0) 수를 센다.  진단만 — 계획 α · 절단 · 판정은 봉인 K 그대로 (K 를 결과 뒤에 고르지 않는다).  열리는 수 > 0 = 그 면의 절단이
    구적 해상도 탓일 수 있다 (면적 오차는 ≤ 1/K² 로 작아도 유일 경로면 단자 G 가 0 으로 바뀐다 — 연결성 처분은 따로 본다)."""
    Kr = int(FALSE_CUT_REFINE) * int(K)
    n0 = n_open = 0
    for ax, a in enumerate(axes):
        cut = np.asarray(a['alpha']) == 0.0
        if not cut.any():
            continue
        low = np.stack(np.unravel_index(np.asarray(a['lin'], np.int64)[cut], tuple(shape)), -1)
        n0 += int(cut.sum())
        n_open += int((face_alpha_values(caps, ax, low, lo, vox, Kr) > 0.0).sum())
    return {'K': int(K), 'K_refine': Kr, 'n_alpha_zero': n0, 'n_open_at_refine': n_open}


def require_plan(plan, sid, sigma_of_sid, vox, pid=None):
    """솔버 입구 계약 (조립 전 · CG 0) — 판 · 종류 · 채널 · K · 격자 (모양 · vox (RIMP-05)) · 지문 (sid · σ · pid · 행 · 계획) ·
    행 불변량 (정수 · 오름차순 유일 · 범위 · 위 이웃 존재 · α 유한 · 0 ≤ α < 1 · K² 격자 위) · 행 자격 (두 셀 다 그 채널 도체 ·
    면제 아님) — **지문을 다시 만든 변조도 불변량이 막는다** (Q7 교훈).  → 솔버 내부용 정규화 dict (호출자의 계획은 안 바꾼다)."""
    if not isinstance(plan, dict) or plan.get('kind') != PLAN_KIND:
        raise ValueError('face_alpha: 계획 종류가 아니다 (ptfe_face_alpha_plan)')
    if plan.get('version') != S1_OPERATOR_VERSION:
        raise ValueError(f'face_alpha: 계획 판 {plan.get("version")!r} ≠ 이 코드 {S1_OPERATOR_VERSION!r}')
    ch = plan.get('channel')
    if ch not in CHANNELS:
        raise ValueError(f'face_alpha: 계획 채널 {ch!r}')
    K = _check_K(plan.get('K'))
    sid = np.asarray(sid)
    shape = tuple(int(x) for x in sid.shape)
    if tuple(plan.get('shape') or ()) != shape:
        raise ValueError(f'face_alpha: 계획 격자 {plan.get("shape")} ≠ 솔버 sid {shape}')
    if not isinstance(plan.get('vox_um'), (float, int)) or float(plan['vox_um']) != float(vox):
        raise ValueError(f'face_alpha: 계획 vox {plan.get("vox_um")!r} ≠ 솔버 vox {vox!r} — 조립 전 거부 (RIMP-05)')
    if plan.get('fp_sid') != _grid_fp(sid):
        raise ValueError('face_alpha: 계획을 만든 sid 와 솔브할 sid 가 다르다 (지문)')
    if plan.get('fp_sig') != _grid_fp(np.asarray(sigma_of_sid, np.float64)):
        raise ValueError('face_alpha: 계획을 만든 σ 표와 솔브할 σ 표가 다르다 (다른 채널 · 다른 σ — 지문)')
    if ch == 'electronic':
        if pid is None:
            raise ValueError('face_alpha: 전자 계획은 솔버에 pid 를 같이 넘겨야 한다 (면제 판정 증거)')
        if plan.get('fp_pid') != _grid_fp(np.asarray(pid)):
            raise ValueError('face_alpha: 계획을 만든 pid 와 솔브할 pid 가 다르다 (지문)')
    axes = plan.get('axes')
    if not isinstance(axes, (tuple, list)) or len(axes) != 3:
        raise ValueError('face_alpha: 계획 axes 는 축 셋')
    N = int(np.prod(shape))
    pidv = np.asarray(pid) if (ch == 'electronic') else None
    norm = []
    for ax in range(3):
        a = axes[ax]
        if not isinstance(a, dict):
            raise ValueError('face_alpha: 축 원장 모양')
        lin = np.asarray(a.get('lin'))
        al = np.asarray(a.get('alpha'))
        if lin.ndim != 1 or al.ndim != 1 or len(lin) != len(al):
            raise ValueError('face_alpha: 행 배열 모양')
        if len(lin) and (lin.dtype == bool or not np.issubdtype(lin.dtype, np.integer)):
            raise ValueError('face_alpha: 행 번호는 정수')
        if len(al) and not np.issubdtype(al.dtype, np.floating):
            raise ValueError('face_alpha: α 는 실수')
        lin = lin.astype(np.int64)
        al = al.astype(np.float64)
        if len(lin) and ((np.diff(lin) <= 0).any() or lin.min() < 0 or lin.max() >= N):
            raise ValueError('face_alpha: 행 번호가 오름차순 유일 · 격자 안이 아니다 (중복 · 범위)')
        if len(al) and (not np.isfinite(al).all() or (al < 0).any() or (al >= 1).any()):
            raise ValueError('face_alpha: α 가 유한 · 0 ≤ α < 1 이 아니다 (α = 1 행은 계획에 없어야 한다)')
        kk = al * (K * K)
        if len(al) and (kk != np.round(kk)).any():
            raise ValueError(f'face_alpha: α 가 구적 격자 {{0, 1/K², …}} 밖이다 (K = {K})')
        if len(lin):
            low = np.stack(np.unravel_index(lin, shape), -1)
            if (low[:, ax] >= shape[ax] - 1).any():
                raise ValueError('face_alpha: 행의 위 이웃 셀이 격자 밖 (축 끝 셀)')
            up = low.copy()
            up[:, ax] += 1
            ok = (_channel_cond(ch, sigma_of_sid, sid, lin)
                  & _channel_cond(ch, sigma_of_sid, sid, np.ravel_multi_index(tuple(up.T), shape)))
            if not ok.all():
                raise ValueError('face_alpha: 행에 그 채널의 비도체 셀이 낀 면 — 다른 격자 · 다른 채널의 계획')
            ex = _exempt_mask(ch, sid[tuple(low.T)], sid[tuple(up.T)],
                              None if pidv is None else pidv[tuple(low.T)], None if pidv is None else pidv[tuple(up.T)])
            if ex.any():
                raise ValueError('face_alpha: 면제 면 (같은 물체 안) 에 α 행 — 계획 변조')
        norm.append({'lin': lin, 'alpha': al, 'cut': al == 0.0})
    if rows_fp(norm) != plan.get('fp_rows'):
        raise ValueError('face_alpha: 행 지문 불일치 — 계획을 만든 뒤 행이 바뀌었다 (E5)')
    if plan_fp(plan) != plan.get('fp_plan'):
        raise ValueError('face_alpha: 계획 지문 불일치 (E5)')
    caps = plan.get('caps')
    if not isinstance(caps, dict) or caps.get('fp') != plan.get('fp_caps') or _caps_fp(caps) != caps.get('fp'):
        raise ValueError('face_alpha: 캡슐 기하 지문 불일치 (계획 · 기하 배열)')
    return {'channel': ch, 'K': K, 'shape': shape, 'vox': float(vox), 'lo': tuple(float(x) for x in plan['lo_um']),
            'axes': tuple(norm), 'caps': caps, 'n_rows': int(sum(len(a['lin']) for a in norm)),
            'n_cut_rows': int(sum(int(a['cut'].sum()) for a in norm)), 'fp_plan': plan['fp_plan'],
            '_plate_cross': {'bot': 0, 'top': 0}}


def cut_lin(fap):
    """절단 면 (α = 0) — 축마다 아래 셀 선형번호 (E3 연결성 · `_iface_label_cut` 입력)."""
    return tuple(a['lin'][a['cut']] for a in fap['axes'])


def assemble_axis(fap, axis, m, g, used):
    """`couple` 한 축의 면 g (마스크 m 의 평탄 순서) 에서 계획 행이 있는 면만 α·g0 로 · α = 0 면은 행렬에서 뺀다 (E6 — 원장에는
    tombstone 으로 남는다).  행이 없으면 g **그대로** (같은 객체 · 비트 같음).  → (g, keep|None) · used[axis] = 실제로 쓴 행."""
    a = fap['axes'][axis]
    used[axis] = {'lin': np.zeros(0, np.int64), 'alpha': np.zeros(0), 'g': np.zeros(0)}
    if not len(a['lin']):
        return g, None
    shp = list(fap['shape'])
    shp[axis] -= 1
    pos = np.ravel_multi_index(np.unravel_index(a['lin'], fap['shape']), tuple(shp))
    mf = np.flatnonzero(m)
    loc = np.searchsorted(mf, pos)
    ok = loc < len(mf)
    ok[ok] = mf[loc[ok]] == pos[ok]
    if not ok.any():
        return g, None
    g = np.array(g, np.float64, copy=True)
    L_ = loc[ok]
    al = a['alpha'][ok]
    g[L_] = g[L_] * al
    used[axis] = {'lin': a['lin'][ok], 'alpha': al, 'g': g[L_].copy()}
    cut = al == 0.0
    if cut.any():
        keep = np.ones(len(g), bool)
        keep[L_[cut]] = False
        return g[keep], keep
    return g, None


def _plate_alpha(fap, ii, jj, kk, side):
    """판 쪽 면의 α — 바닥 = 셀 (i, j, k) 의 아래 면 (아래 셀 k−1) · 위 = 셀의 위 면 (아래 셀 k)."""
    ii, jj, kk = (np.asarray(x, np.int64) for x in (ii, jj, kk))
    low = np.stack([ii, jj, kk - (1 if side == 'bot' else 0)], -1)
    return face_alpha_values(fap['caps'], 2, low, fap['lo'], fap['vox'], fap['K'])


def plate_coupling_factor(fap, ii, jj, kk, side):
    """판 결합 면의 배율 — **v0 = 1 (α 미적용 · `PLATE_RULE`)**.  판 쪽 면을 캡슐이 가로지르는 기둥 수만 기록한다 (F17)."""
    al = _plate_alpha(fap, ii, jj, kk, side)
    fap['_plate_cross'][side] = int((al < 1.0).sum())
    return np.ones(len(al))


def isolated_by_cut(cond, cuts):
    """사방 절단 셀 수 — 도체 이웃이 하나 이상 있고 그 면이 전부 절단된 셀 (기록 · 가지치기는 E3 가 한다).
    절단 면 양끝 셀만 본다 (격자 전체 배열 없음)."""
    cond = np.asarray(cond, bool)
    shape = cond.shape
    cf = cond.reshape(-1)
    stride = np.array([shape[1] * shape[2], shape[2], 1], np.int64)
    ends = []
    for ax in range(3):
        lin = np.asarray(cuts[ax], np.int64)
        if not len(lin):
            continue
        up = lin + stride[ax]
        ok = cf[lin] & cf[up]
        ends += [lin[ok], up[ok]]
    if not ends:
        return 0
    cells, dcut = np.unique(np.concatenate(ends), return_counts=True)
    ijk = np.stack(np.unravel_index(cells, shape), -1)
    deg = np.zeros(len(cells), np.int64)
    for ax in range(3):
        for sgn in (-1, 1):
            nb = ijk[:, ax] + sgn
            okb = (nb >= 0) & (nb < shape[ax])
            deg[okb] += cf[cells[okb] + sgn * stride[ax]]
    return int(((deg > 0) & (deg == dcut)).sum())


def edges_fp(axes):
    parts = ['edges-v1']
    for ax, a in enumerate(axes or ()):
        parts += [str(ax), np.ascontiguousarray(np.asarray(a.get('lin', ()), np.int64)).tobytes(),
                  np.ascontiguousarray(np.asarray(a.get('alpha', ()), np.float64)).tobytes(),
                  np.ascontiguousarray(np.asarray(a.get('g', ()), np.float64)).tobytes()]
    return _h16(*parts)


def solve_record(fap, used, *, solved, n_isolated=0):
    axes = tuple(used.get(a) or {'lin': np.zeros(0, np.int64), 'alpha': np.zeros(0), 'g': np.zeros(0)} for a in range(3))
    return {'operator': S1_OPERATOR_VERSION, 'channel': fap['channel'], 'K': int(fap['K']),
            'n_rows_plan': int(fap['n_rows']), 'n_rows_used': int(sum(len(a['lin']) for a in axes)),
            'n_cut_used': int(sum(int((np.asarray(a['alpha']) == 0).sum()) for a in axes)),
            'n_isolated_by_cut': int(n_isolated), 'plate_rule': PLATE_RULE,
            'plate_cross_columns': dict(fap['_plate_cross']), 'fp_plan': fap['fp_plan'], 'solved': bool(solved)}


def edges_ctx(fap, used, sid, sigma_of_sid, phi=None):
    axes = tuple(used.get(a) or {'lin': np.zeros(0, np.int64), 'alpha': np.zeros(0), 'g': np.zeros(0)} for a in range(3))
    return {'kind': EDGES_KIND, 'version': S1_OPERATOR_VERSION, 'vox_um': fap['vox'], 'shape': fap['shape'], 'axes': axes,
            'fp_sid': _grid_fp(sid), 'fp_sig': _grid_fp(np.asarray(sigma_of_sid, np.float64)),
            'fp_phi': (_grid_fp(phi) if phi is not None else None), 'fp_edges': edges_fp(axes), 'fp_plan': fap['fp_plan']}


def edges_ctx_from(res, sid, sigma_of_sid=None):
    """진단용 face_alpha 간선 원장 (E2 · E5) — 지문 대조 (sid · σ · φ · 원장).  face_alpha 를 안 쓴 해 → None."""
    e = (res or {}).get('_face_alpha') if isinstance(res, dict) else None
    if not e:
        return None
    if _grid_fp(sid) != e.get('fp_sid'):
        raise ValueError('face_alpha 원장: 진단에 넘긴 sid 가 솔브한 sid 와 다르다 (E5)')
    if sigma_of_sid is not None and _grid_fp(np.asarray(sigma_of_sid, np.float64)) != e.get('fp_sig'):
        raise ValueError('face_alpha 원장: 진단에 넘긴 σ 가 솔브한 σ 와 다르다 (E5)')
    if e.get('fp_phi') is not None and 'phi' in res and _grid_fp(res['phi']) != e['fp_phi']:
        raise ValueError('face_alpha 원장: 해의 φ 가 원장을 만든 솔브의 φ 가 아니다 (E5)')
    if edges_fp(e.get('axes')) != e.get('fp_edges'):
        raise ValueError('face_alpha 원장: 간선 원장이 솔브 뒤 바뀌었다 (지문 불일치 · E5)')
    return e


def refuse_diag(res, what):
    """진단 거부 (E2 · v0) — α 를 원장에서 읽지 않는 진단은 face_alpha 해를 받지 않는다 (fail-closed)."""
    if isinstance(res, dict) and (res.get('_face_alpha') is not None or res.get('face_alpha') is not None):
        raise ValueError(f'{what}: S1 face_alpha 해 — 이 진단은 면 α 를 원장에서 읽지 않는다 (조화평균을 다시 계산하면 '
                         f'막힌 면의 전류가 과대) · v0 = LEAN 2 · 3 만 (설계 §3-3 · E2)')


def solve_receipt(res, plan, *, requested, disabled_why=None):
    """솔브 한 건의 S1 영수증 (상태 어휘 = run_contract.INTERFACE_OK_STATUSES 부분 · 새 이름 없음 · 위반 표지 = missing ·
    applied_without_request).  요청 (채널) 과 솔브 기록을 **따로** 보고 정한다 (RINT-02 교훈)."""
    rec = res.get('face_alpha') if isinstance(res, dict) else None
    if not requested:
        if isinstance(rec, dict):
            return {'status': 'applied_without_request', 'n_rows_used': rec.get('n_rows_used')}
        return {'status': 'not_requested'}
    if disabled_why is not None:
        return {'status': 'disabled', 'why': str(disabled_why)}
    if not isinstance(res, dict):
        return {'status': 'missing', 'why': '솔브 결과가 없다'}
    if not isinstance(rec, dict):
        return {'status': 'missing', 'why': '솔브 결과에 face_alpha 기록이 없다 — 계획이 이 호출에 전달되지 않았다'}
    fp = plan.get('fp_plan') if isinstance(plan, dict) else None
    if fp is None or rec.get('fp_plan') != fp:
        return {'status': 'missing', 'why': '솔브가 쓴 계획 지문 ≠ 요청 계획 지문'}
    out = {k: rec.get(k) for k in ('n_rows_used', 'n_cut_used', 'n_isolated_by_cut', 'plate_cross_columns', 'solved')}
    out['fp_plan'] = fp
    if res.get('reason') or rec.get('solved') is not True:
        out.update(status='failed', why=str(res.get('reason') or 'unsolved'), n_rows_used=0)
        return out
    out['status'] = 'applied' if (rec.get('n_rows_used') or 0) > 0 else 'absent_geometry'
    return out


def volume_band_status(capsule_um3, true_um3):
    """→ (비 | None, 'in_band' | 'out_of_band' | 'unknown_true_volume') — 닫힌 밴드 [0.5, 2]."""
    try:
        t = float(true_um3)
    except (TypeError, ValueError):
        return None, 'unknown_true_volume'
    if not (math.isfinite(t) and t > 0):
        return None, 'unknown_true_volume'
    ratio = float(capsule_um3) / t
    return ratio, ('in_band' if VOLUME_BAND[0] <= ratio <= VOLUME_BAND[1] else 'out_of_band')


def volume_record(capsule_um3, true_um3):
    """부피 기록 — capsule_um3 = 명목 tube 체적 (옛 칸 이름 그대로 · 소비자 호환).  ★ 10-21 (Codex A4 · Q11): 이름을 나눈 칸을 같이 싣는다 —
    capsule_nominal_um3 (같은 값 · 밴드 비의 기준 `ratio_basis`) · capsule_union_um3 = None (합집합 체적 v0 미계산 · 겹침 · 굽힘 미차감 —
    명목 ≥ 합집합) · 체적 정의 이름 (`VOLUME_BASIS`)."""
    ratio, st = volume_band_status(capsule_um3, true_um3)
    t = None
    try:
        t = float(true_um3) if true_um3 is not None and math.isfinite(float(true_um3)) else None
    except (TypeError, ValueError):
        t = None
    return {'capsule_um3': float(capsule_um3), 'true_um3': t, 'ratio': ratio, 'band': list(VOLUME_BAND), 'status': st,
            'capsule_nominal_um3': float(capsule_um3), 'capsule_union_um3': None, 'capsule_union_status': 'not_computed_v0',
            'capsule_volume_basis': VOLUME_BASIS, 'ratio_basis': 'capsule_nominal_um3'}


def ptfe_point_cell_census(sid, pts, lo, vox):
    """off 격자에서 PTFE 점이 든 셀의 sid 분포 (설계 §3-2 · §3-5 이온 채널 겹침 진단) — {str(sid): 셀 수}."""
    P = np.asarray(pts, np.float64).reshape(-1, 3)
    if not len(P):
        return {}
    sid = np.asarray(sid)
    ijk = np.floor((P - np.asarray(lo, np.float64)) / float(vox)).astype(np.int64)
    ok = ((ijk >= 0) & (ijk < np.asarray(sid.shape))).all(1)
    if not ok.any():
        return {}
    u = np.unique(np.ravel_multi_index(tuple(ijk[ok].T), sid.shape))
    v, n = np.unique(sid.reshape(-1)[u], return_counts=True)
    return {str(int(a)): int(b) for a, b in zip(v, n)}


def protocol_record(channels, dia_law):
    """`ca_ext.ptfe_face.protocol` — 물리 칸 (p3ca id 에 들어간다 · 증거 · 지문 · 수는 안 들어간다)."""
    ch = sorted(set(channels))
    if not ch or any(c not in CHANNELS for c in ch) or len(ch) != len(list(channels)):
        raise ValueError(f'face_alpha: 채널 {channels!r} — {CHANNELS} 의 비지 않은 집합 (중복 없음)')
    if dia_law not in DIA_LAWS:
        raise ValueError(f'face_alpha: 지름 법칙 {dia_law!r}')
    dia = ({'rope': ROPE_D_UM} if dia_law == 'rope'
           else {'rope': ROPE_D_UM, 'fibre': FIBRE_D_UM, 'rope_count_frac': TWO_POP_ROPE_FRAC})
    return {'operator': S1_OPERATOR_VERSION, 'channels': ch, 'dia_law': dia_law, 'dia_um': dia, 'K': K_SEALED,
            'impermeable': True, 'gap_tol': GAP_TOL, 'face_rule': FACE_RULE, 'exempt_rule': EXEMPT_RULE,
            'plate_rule': PLATE_RULE, 'centerline': CENTERLINE_SOURCE}


def evidence_record(*, capsules, volume, faces, receipts, off_grid_ptfe_point_cells, fp, diagnostics=None):
    """`ca_ext.ptfe_face.evidence` — 증거 (id 에 안 들어간다 · `ptfe_face_block_problem` 이 대조한다)."""
    return {'capsules': dict(capsules), 'volume': dict(volume), 'faces': dict(faces), 'receipts': dict(receipts),
            'off_grid_ptfe_point_cells': dict(off_grid_ptfe_point_cells), 'fp': dict(fp),
            'diagnostics': dict(DIAGNOSTICS_V0 if diagnostics is None else diagnostics), 'label': LABEL,
            'exempt_assumptions': dict(EXEMPT_ASSUMPTIONS)}           # ★ 10-21 — 같은 sid 면제 = 상 수준 융합 가정 표지 (Codex §4-1)


def _jsonable_counts(counts):
    return {k: {'n_alpha_lt1': int(v['n_alpha_lt1']), 'n_alpha0': int(v['n_alpha0']),
                'blocked_area_um2': float(v['blocked_area_um2'])} for k, v in (counts or {}).items()}


def plan_face_summary(plan):
    if plan is None:
        return None
    fc = plan.get('false_cut_check') if isinstance(plan.get('false_cut_check'), dict) else {}
    #  ★ 10-21 (Codex §4-1 · Q11) — 진단 칸: α = 0 면 수 (= n_cut_rows · 이름 그대로) · 그중 고운 구적에서 열리는 수 · 그 구적 K
    return {'n_rows': int(plan['n_rows']), 'n_cut_rows': int(plan['n_cut_rows']), 'by_class': _jsonable_counts(plan['counts']),
            'alpha_zero_faces': int(plan['n_cut_rows']), 'alpha_zero_open_at_refine': fc.get('n_open_at_refine'),
            'alpha_refine_K': fc.get('K_refine')}


def payload_prepare(sid, pid, *, lo, vox, sig_e, sig_i, pts, fid, kind, channels, dia_law, true_volume_um3, build_ionic=True):
    """payload 한 런의 S1 준비 — 캡슐 · 채널마다 계획 · 증거 바탕 (영수증은 솔브 뒤 `payload_block`).  이온 솔브를 안 돌리면
    (`--no-ion`) 이온 계획을 만들지 않는다 (영수증 = disabled)."""
    caps = build_capsules(pts, fid, kind, dia_law=dia_law)
    plans = {'electronic': None, 'ionic': None}
    if 'electronic' in channels:
        plans['electronic'] = build_plan(sid, sig_e, caps, lo=lo, vox=vox, channel='electronic', pid=pid)
    if 'ionic' in channels and build_ionic:
        plans['ionic'] = build_plan(sid, sig_i, caps, lo=lo, vox=vox, channel='ionic')
    return {'caps': caps, 'plans': plans, 'protocol': protocol_record(channels, dia_law),
            'volume': volume_record(caps['volume_um3'], true_volume_um3),
            'census': ptfe_point_cell_census(sid, pts, lo, vox),
            #  ★ Z3 (10-20) — off 격자 sid 지문 (face_alpha 의 sid 격자 = `ptfe_stamp off` 격자 · 같은 함수 `step3_sigma._grid_fp` = 접합 원장
            #    `fp.sid` · S0 off 격자와 같은 꼴) — 사슬이 같은 킷 · 같은 래스터 런끼리 · 조합 런의 접합 원장과 대조한다.
            'sid_off': _grid_fp(sid)}


def payload_block(prep, receipts):
    """`ca_ext.ptfe_face` 하위 블록 = {'protocol', 'evidence'} (payload 가 바깥 `ca_ext` 에 schema 와 함께 싣는다)."""
    pe, pi = prep['plans']['electronic'], prep['plans']['ionic']
    ev = evidence_record(capsules=capsule_summary(prep['caps']), volume=prep['volume'],
                         faces={'electronic': plan_face_summary(pe), 'ionic': plan_face_summary(pi)},
                         receipts={k: receipts.get(k) or {'status': 'missing', 'why': '영수증 없음'} for k in SOLVES},
                         off_grid_ptfe_point_cells=prep['census'],
                         fp={'caps': prep['caps']['fp'], 'plan_electronic': (pe['fp_plan'] if pe else None),
                             'plan_ionic': (pi['fp_plan'] if pi else None), 'sid_off': prep['sid_off']})
    return {'protocol': dict(prep['protocol']), 'evidence': ev}


def ptfe_face_block_problem(man):
    """`ca_ext.ptfe_face` 계약 (run_contract.ca_ext_record_ok 가 producer 게시 전 · check_arm · 판정기에서 부른다) → 문제 | None.
    · 도장 ⇔ 블록 · protocol = 이 코드의 정본 (채널 · 지름 법칙만 고른다) · v0 조건 (LEAN 2 · 3 — 열 · pore · 집전체 · 필드 끔 ·
      주기 아님 · PTFE 차단 0 · σ_PTFE 0 · 계면 표 없음) · 관측 PTFE 셀 0 (도장 ≠ 실물)
    · 영수증 네 솔브 (채널 요청 ↔ 상태 · 계획 지문 ↔ 증거 지문 · applied ⇒ 행 > 0) · 부피 상태 = 기록된 비와 일치 · 진단 = v0 표 · 표지"""
    if not isinstance(man, dict):
        return 'manifest 가 dict 가 아니다'
    if man.get('ptfe_stamp') != PTFE_STAMP:
        return f'stamp| ptfe_face 블록인데 ptfe_stamp = {man.get("ptfe_stamp")!r}'
    blk = (man.get('ca_ext') or {}).get('ptfe_face') if isinstance(man.get('ca_ext'), dict) else None
    if not isinstance(blk, dict) or not isinstance(blk.get('protocol'), dict) or not isinstance(blk.get('evidence'), dict):
        return 'shape| ptfe_face = {protocol, evidence} dict 이어야 한다'
    prot, ev = blk['protocol'], blk['evidence']
    try:
        want = protocol_record(prot.get('channels') or (), prot.get('dia_law'))
    except (ValueError, TypeError) as e:
        return f'protocol| {e}'
    if prot != want:
        return 'protocol| 이 코드의 정본과 다르다 ' + str(sorted(k for k in set(prot) | set(want) if prot.get(k) != want.get(k)))
    chans = want['channels']
    if man.get('ptfe_cells_observed') != 0:
        return f'cells| face_alpha 인데 관측 PTFE 셀 {man.get("ptfe_cells_observed")!r} (sid 격자 = off 격자여야 한다)'
    plan = man.get('component_plan') if isinstance(man.get('component_plan'), dict) else {}
    for k in ('thermal', 'pore', 'collector'):
        if plan.get(k) is not False:
            return f'v0| component_plan.{k} = {plan.get(k)!r} — v0 = LEAN 2 · 3 만 (α 를 안 읽는 솔브 · 진단)'
    if man.get('field_requested') is not False:
        return 'v0| 필드 요청 (LEAN 4) — v0 거부 (|J| 점군이 α 를 원장에서 안 읽는다)'
    if man.get('periodic_xy') is not False:
        return 'v0| periodic_xy — 정량 모드 거부 (seam 미지원)'
    if float(man.get('ptfe_block_um') or 0.0) != 0.0 or float(man.get('sigma_ptfe_S_cm') or 0.0) != 0.0:
        return 'combo| PTFE 차단 · σ_PTFE 와 face_alpha 동시 (PTFE 셀이 없어 조용한 no-op)'
    if man.get('ptfe_block_scope') not in (None, 'se'):
        return (f'combo| PTFE 차단 범위 {man.get("ptfe_block_scope")!r} 와 face_alpha 동시 (차단할 PTFE 셀이 없다 · '
                f'기본 se 만)')
    if man.get('interface_model') is not None:
        return 'combo| 계면 표 (r1) 와 face_alpha 동시 — v0 미정의 조합'
    rc = ev.get('receipts')
    if not isinstance(rc, dict) or set(rc) != set(SOLVES):
        return f'receipts| 키 {sorted(rc) if isinstance(rc, dict) else rc!r} ≠ {sorted(SOLVES)}'
    fpd = ev.get('fp') if isinstance(ev.get('fp'), dict) else {}
    #  ★ Z3 — off 격자 sid 지문 (격자 지문 꼴 = blake2b 16 바이트 소문자 hex 32 · 없음 · 모양 틀림 = 거부)
    _so = fpd.get('sid_off')
    if not (isinstance(_so, str) and len(_so) == 32 and all(ch in '0123456789abcdef' for ch in _so)):
        return f'fp| off 격자 sid 지문 sid_off = {_so!r} (소문자 hex 32 — `step3_sigma._grid_fp`)'
    for name in SOLVES:
        r = rc[name]
        if not isinstance(r, dict):
            return f'receipts|{name}| dict 가 아니다'
        st = r.get('status')
        if st in ('missing', 'applied_without_request'):
            return f'receipts|{name}| 위반 표지 {st} ({r.get("why")})'
        if st not in OK_STATUSES:
            return f'receipts|{name}| 모르는 상태 {st!r}'
        ch = 'ionic' if name == 'ionic' else 'electronic'
        if ch not in chans:
            if st != 'not_requested':
                return f'receipts|{name}| 채널 {ch} 요청이 없는데 상태 {st}'
            continue
        if name == 'electronic_main':
            ok_st = ('applied', 'absent_geometry', 'failed')
        elif name in ('electronic_wetted', 'electronic_bare'):
            ok_st = ('disabled',)
        else:
            ok_st = ('disabled',) if plan.get('ionic') is False else ('applied', 'absent_geometry', 'failed')
        if st not in ok_st:
            return f'receipts|{name}| 상태 {st} — 이 계획에서 허용 {ok_st}'
        if st in ('applied', 'absent_geometry'):
            n = r.get('n_rows_used')
            if type(n) is not int or n < 0 or (st == 'applied') != (n > 0):                # noqa: E721
                return f'receipts|{name}| {st} 인데 n_rows_used = {n!r}'
            if r.get('solved') is not True:
                return f'receipts|{name}| {st} 인데 solved = {r.get("solved")!r}'
            if r.get('fp_plan') != fpd.get(f'plan_{ch}') or not r.get('fp_plan'):
                return f'receipts|{name}| 솔브 계획 지문 ≠ 증거의 {ch} 계획 지문'
        if st in ('failed', 'disabled') and not r.get('why'):
            return f'receipts|{name}| {st} 인데 사유 없음'
    #  요청한 채널의 솔브가 전부 꺼졌다 (예: 이온만 + --no-ion) = 연산자가 어디에도 안 걸린 조용한 no-op — producer 거부의 짝
    if not [n for n in ('electronic_main', 'ionic')
            if ('ionic' if n == 'ionic' else 'electronic') in chans and rc[n].get('status') != 'disabled']:
        return f'noop| 요청 채널 {chans} 의 솔브가 전부 disabled — face_alpha 가 어느 솔브에도 안 걸렸다'
    caps = ev.get('capsules') if isinstance(ev.get('capsules'), dict) else None
    if caps is None or any(type(caps.get(k)) is not int or caps.get(k) < 0                    # noqa: E721
                           for k in ('n_paths', 'n_pieces', 'n_point_pieces', 'n_segments')):
        return 'capsules| 수 기록 모양'
    vol = ev.get('volume') if isinstance(ev.get('volume'), dict) else None
    try:
        vwant = volume_record(caps.get('volume_um3'), (vol or {}).get('true_um3'))
    except (TypeError, ValueError):
        return 'volume| 기록 모양'
    if vol != vwant:
        return f'volume| 기록 {vol!r} ≠ 재계산 {vwant!r} (상태 · 비가 캡슐 부피 · 참부피와 맞지 않는다)'
    if ev.get('diagnostics') != DIAGNOSTICS_V0:
        return 'diagnostics| v0 진단 표 (je · 소산 분담 미계산 · 필드 · Joule 거부) 가 아니다'
    if ev.get('label') != LABEL:
        return 'label| 표지 문자열이 producer 상수와 다르다'
    if ev.get('exempt_assumptions') != EXEMPT_ASSUMPTIONS:            # ★ 10-21 — 면제 = 상 수준 융합 가정 표지 (Codex §4-1)
        return (f'exempt| 같은 sid 면제의 가정 표지 {ev.get("exempt_assumptions")!r} ≠ producer 상수 (같은 탄소 sid · SDCP|SDCP = '
                f'상 수준 융합 가정)')
    return None
