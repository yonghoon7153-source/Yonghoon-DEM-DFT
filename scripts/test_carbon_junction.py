#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rint ② S2 탄소 접합 R_j v0 (VGCF–VGCF) + S3 SDCP 접합 수정자 — 시험 먼저 (규율 ② · 2026-10-20).

정본 = 설계 v1 `docs/reviews/rint_carbon_additive_design_v1_20261020.md` §4 · §5 (+ 계약 v2 §3-8 J1–J8 · v3 §5 J2a–J12 · v3.1) ·
1저자 10-20 N1–N18 = 권고대로.  ⚠ 이 시험의 PASS 는 **계약 · 구현의 증거**이지 R_j 값 · 판정 (R) 의 증거가 아니다.
기대값은 **모듈 밖에서** 손으로 세운 회로 (직렬 사슬 · 사다리) 를 직접 풀어 만든다 — 같은 함수로 정답을 다시 만들지 않는다.

  python3 scripts/test_carbon_junction.py            # 현 구현
  python3 scripts/test_carbon_junction.py --quick    # 끔 비트 동일 (C0) 의 무작위 침대 수를 줄인다

픽스처 단위: h = 1 µm · r_f = 0.5 µm (섬유 지름 = 1 복셀 — 생산 Ø0.15 @ vox 0.15 와 같은 비) · tol_ff = 0.1 · L_par = 2(r_fi + r_fj) = 2.0 ·
r_port = 2.0 (= 2h) · gap_tol 2.0 · σ_VGCF = 100 S/cm → 축방향 면 g = σ·h = 100 · 판 결합 g = σ·h²/(h/2) = 200 (코드 단위 S/cm·µm) ·
접합 간선 g = 1e4/R_j (설계 §4-1 J5).

묶음 (설계 §4-4 · §5-4 · 브리프 B):
  C0     끔 = 옛 경로 비트 동일 (기준 = 커밋 d1768cf0c 의 step3_sigma · 무작위 침대 16 입력 · σ · φ · n_dof · cg_info · resid · sid)
  C1     cross_shared — 판 ↔ A ↔ 교차 셀 (멤버십 dof 둘) ↔ B ↔ 판 = 해석 직렬 사슬 (1e-12) · R_j 스윕 Rayleigh 단조
  T1-7   R_j → 0 = 축약 그래프 (C1 = 옛 융합 · C2a = 포트 병합 회로) · R_j = ∞ = 가닥 사이 전류 0 · 가닥 안 연속
  C2     cross_face (옛 융합 면 절단 + 간선 하나) · cross_edge (옛 단절 → 접합으로 연결 · 가지치기가 안 지움 = J12)
  C3     pass_through — 교차 셀을 지나는 가닥은 R_j 와 무관 (J6 · J12)
  C4     series_chain — R = 기저 + (N−1)·R_j (기울기 정확) · 단위 변이 (1e4 빠짐 · ×1e8) 실패
  C5     instance — 같은 접촉을 조각 더 잘게 · 섬유 순서 · 점 역순 = instance 수 · σ 불변 (J2c) · 같은 쌍 두 곳 = instance 둘
  T1-6   junction_multi — 두 자리 사다리 회로 (1e-12) · 등전위 극한 R → R_j/2
  T1-8   crossing_k3 / J9 — 한 셀 세 가닥 → dof 셋 · instance 셋 · 포트 dof 서로 다름
  T1-9   fiber_sphere_threshold (J2b) — r_f 0.075 · R_AM 2 · d 2.12 µm = 접촉 아님 (문자식 2.15 오판 아님)
  T1-10  self_contact — 같은 fid 비연속 두 셀 면 → 자기 접합 instance 하나 · 0 저항 지름길 없음
  T1-11  port_tie — 등거리 두 후보 → 정준 방향 경로 번호가 작은 셀 · 동률 수 · 점 역순 · 섬유 순서에 σ 불변
  T1-12  site_cut — 같은 쌍 두 자리 중 한 자리만 instance → 그 발자국 면만 절단 · 다른 자리 = 미등록 법칙 (cut ≤ fused)
  T1-5′  lead_reference — 단자 기준 R_j · 리드 빼기 · 음수 = 거부 (v0 = 모형 내부값만)
  ── 길이 법칙 v0 (1저자 10-20 밤 Q17 · J8 "긴 접촉 = 정량 거부" 를 대체): G_j = max(1, L_c/L_par)/R_j,0 ──
  LEN-X  깊은 직교 교차 (L_c = L_par) → 배율 1 · σ = 옛 점 접합 회로 (1e-12)
  LEN-BIT 긴 접촉 없는 침대 9 개 = 구현 B (61b6a9ec5 · 점 접합) 와 σ · n_dof · cg_info · resid · 접합 전류 비트 같음
  LEN-P  나란한 두 섬유 L_c = 3 L_par → 배율 3 → σ = 판 + 섬유 + 접합 1/(3/R_j,0) 해석 회로 (기계 정밀도 · cut · fused)
  LEN-O  비스듬한 깊은 교차 → 배율 = 1/sin θ · 90° 에서 1 정확히 · 연속 · 각도에 단조
  J8     long_contact — 긴 접촉 = 표지 · 집계 칸 그대로 · 정량 거부 없음 (옛 동작 제거) · 정량 솔브 진행
  FOOT   절단 발자국 = 접촉 run 전체 — fused 법칙에서도 run 위 A|B 융합 면 0 (면 tombstone · 간선 원장 · σ 해석)
  KINK   U 자로 접힌 한 섬유 — 경로 호 길이 s (손으로 잰 값) · s < s_min = 접합 없음 (옛 복셀 융합 그대로 = 옛 경로 σ) ·
         s ≥ s_min = 자기 접합 하나 (절단 + R_j 간선 × 같은 배율) · s_min 없음 + 정량 = 구조화 거부 · 자기 L_c = 닿음 규칙
  INV    점 역순 · 원점 이동 · 섬유 번호 바꿈 → sid · instance 수 · 배율 · σ 같음 (LP · KU)
  SMIN   s_min_um = 필수 키워드 · 기본값 없음 · 비유한 · 음수 · bool · 문자 거부
  REC    기록 — 법칙 이름 len_scaled_v0 · s_min · L_c 분위 · 배율 합 · 자기 접합 (후보 · 거른 수 · 남은 수 · s 분포) · 지문에 s_min
  MUT-LEN 변이 넷 (배율 제곱 · max(1, ·) 빼기 · s 거르기 끔 · 발자국 = 최근접 쌍만) 이 위 시험에 걸린다
  J11    electrode_short — 축약 무리가 두 판에 다 닿으면 단락 상태 (유한 σ 로 위장하지 않는다)
  C6     energy — Σ P (면 + 접합 + 판) = I·ΔV · 접합 몫 = −∂lnσ/∂lnR_j (중심 FD)
  C8     guards — r1 · ①′ · 주기 · return_field · 다른 vox · sid · 계획 · 원장 변조 · NaN · 길이 불일치 · 떨어진 같은 fid · kind 없음 ·
         VGCF 절연 채널 · 법칙 미선언 · R_j 극한 → 조립 전 거부 (CG 호출 0)
  P-1/2  PTFE–접합 법칙 — P1 = 덮인 instance 만 절단 · P0 = 영향 없음 · 경계 = 정확히 tol_P 포함 · centerline + P1 = 거부 ·
         (P1, c = 1) = 절단 먼저 (N18)
  FA+CJ  S1 face_alpha × S2 cjunc 를 한 솔브에 같이 = ★ Z3 (10-20) 받음 (설계 조합 규칙 — α 먼저 · 접합 훅 다음 · α 는 접합 간선에 안 걸림 ·
         옛 임시 거부를 뺐다) · 각각 홀로도 받음 · 조합 σ ≤ 접합만 σ (α ≤ 1 · Rayleigh) · 접합 기록 = 접합만과 같음
         (조합 규칙의 전수 시험 = `scripts/test_ca_ext_z3.py` A)
  S3-1…11 SDCP 접합 수정자 (c = 0 비트 같음 · SBE no-op · c 단조 · c = 1 축약 · 순열 · 경계 · 펠릿 no-op · 변이 · S2 없이 거부 ·
         sid 불변 · 우선순위)
  SV     SV 면 · SDCP 셀 소산 몫 · SV_DOMINANT 표지 · SDCP 경유 섬유 연결 수
  PIECE  멤버십 셀 = `_fibre_segment_ijk` 의 VGCF 셀 (같은 끊기 규칙 · 복제 + 동등 시험)
  PIECE4 끊기 규칙 사본 대조 (2 일 차) — 생산 `step3_sigma._fibre_segment_ijk` ↔ B `carbon_junction.fibre_pieces` ↔
         C `ca_s0_census.pieces_of` ↔ A `ptfe_face_alpha.build_capsules`: 끊김이 있는 합성 침대에서 조각 경계 · 셀 열 · 셀 집합 같음 ·
         네 곳 각각의 `>` → `>=` 변이 사본이 시험을 떨어뜨린다 (하나로 합치는 리팩터는 하지 않는다 — 생산 경로 비트 동일 부담)
  FP     지문 재현 (RINT-23 · 2 일 차) — 같은 내용 · 다른 객체 → 같은 지문 · 별도 `python3 -I` 하위 프로세스 둘 → 같은 지문 ·
         한 글자 다름 → 다른 지문.  `carbon_junction._fp` (객체 배열 = 내용 직렬화 · 숫자 배열 = dtype · 모양 · C 순서 바이트) ·
         원장 · 계획 지문 · 격자 지문 감싸개 (`_grid_fp` — 객체 격자 거부) · 같은 꼴 확인 = `ptfe_face_alpha` (캡슐 · 행 · 계획 ·
         간선) · `ca_s0_census` (계획 sha256 · 파일 sha256) · `step3_conv_cert` (지문 함수 없음 — 목록 시험이 지킨다)
"""
import argparse
import ast
import contextlib
import hashlib
import importlib.util
import io
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, 'scripts')
sys.path.insert(0, SCRIPTS)

BASE_COMMIT = 'd1768cf0c'          # 끔 비트 동일의 기준 (이 묶음 전 원격 HEAD)

S3 = None
CJ = None
QUICK = False
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


CASES = []


def case(tag):
    def deco(fn):
        CASES.append((tag, fn))
        return fn
    return deco


def quiet(fn, *a, **k):
    with contextlib.redirect_stdout(io.StringIO()):
        return fn(*a, **k)


_CG_CALLS = [0]


@contextlib.contextmanager
def direct_solver():
    """작은 픽스처 = 직접 풀이 (기계 정밀도) — 조립 · 항등식을 CG 허용오차 없이 본다.  생산 경로 아님."""
    from scipy.sparse.linalg import spsolve
    old = S3._solve_cg

    def _direct(L, b, *a, **k):
        _CG_CALLS[0] += 1
        return spsolve(L.tocsc(), b), 0
    S3._solve_cg = _direct
    try:
        yield
    finally:
        S3._solve_cg = old


def raises(fn, exc=(ValueError, TypeError)):
    try:
        quiet(fn)
    except exc:
        return True
    except Exception:                                      # noqa: BLE001 — 다른 예외 = 거부 계약 위반
        return False
    return False


# ═════════════════════════ 픽스처 도구 ═════════════════════════
H = 1.0
RF = 0.5
TOL = 0.1
LPAR = 2.0 * (RF + RF)
RPORT = 2.0
SV = 100.0                       # σ_VGCF (S/cm)
G_AX = SV * H                    # 축방향 면 g (코드 단위)
G_PL = SV * H * H / (0.5 * H)    # 판 결합 g (셀 중심이 판에서 h/2)


def sig_e(s_vgcf=SV, s_am=0.010, s_sdcp=250.0):
    return S3.electronic_sigma_table(s_am, s_am * 0.5, s_vgcf, 10.0, s_sdcp)


def densify(verts, step=0.25):
    """꼭짓점 폴리라인 → 간격 ≤ step 인 점열 (끊기 규칙 gap_tol·중앙값 에 걸리지 않게 거의 고른 간격)."""
    V = np.asarray(verts, np.float64)
    out = [V[0]]
    for a, b in zip(V[:-1], V[1:]):
        n = max(1, int(math.ceil(np.linalg.norm(b - a) / step - 1e-12)))
        for i in range(1, n + 1):
            out.append(a + (b - a) * (i / n))
    return np.asarray(out)


def rows(polys, phase=2, kind=1, fid0=10, fid_step=10, step=0.25, fids=None):
    """폴리라인들 → (add_pts, add_phase, add_fid, add_kind) — fid 마다 행이 붙어 있다 (생산 규약)."""
    P, PH, F, K = [], [], [], []
    for i, v in enumerate(polys):
        pts = densify(v, step) if len(v) > 1 else np.asarray(v, np.float64)
        f = fids[i] if fids is not None else fid0 + fid_step * i
        P.append(pts); PH.append(np.full(len(pts), phase)); F.append(np.full(len(pts), f)); K.append(np.full(len(pts), kind))
    return (np.vstack(P), np.concatenate(PH).astype(np.int64), np.concatenate(F).astype(np.int64),
            np.concatenate(K).astype(np.int64))


def cat_rows(*rs):
    return tuple(np.concatenate([r[i] for r in rs]) for i in range(4))


NO_AM = (np.zeros((0, 3)), np.zeros(0), np.zeros(0, np.int64))


def bed(addr, n, am=NO_AM, stamp=None, vox=H, lo=(0.0, 0.0, 0.0), **kw):
    """격자 (sid, pid) — 생산 `rasterize` (선분 스탬프).  stamp = 스탬프할 행 마스크 (None = 전부) — face_alpha 침대는 PTFE 를 뺀다.
    lo = 상자 원점 (원점 이동 불변 시험 · 격자는 lo 기준이라 sid 는 같아야 한다)."""
    P, PH, F, K = addr
    m = np.ones(len(P), bool) if stamp is None else stamp
    lo = tuple(float(x) for x in lo)
    hi = tuple(lo[i] + float(n[i]) * vox for i in range(3))
    sid, pid = S3.rasterize(am[0], am[1], am[2], P[m], PH[m], lo, hi, vox, add_fid=F[m], add_kind=K[m], **kw)
    return sid, pid


S_MIN = 3.0                      # 꺾임 자기 접합 거르기 문턱 s_min [µm · fixture 단위] — 시험 명시 값 (생산 숫자 = S0 단계 1 뒤 R §2-1)


def _cj_has_smin():
    import inspect
    try:
        return 's_min_um' in inspect.signature(CJ.cjunc_registry).parameters
    except (TypeError, ValueError, AttributeError):
        return False


def reg_kw(kw):
    """cjunc_registry 문턱 키워드 — s_min_um 은 필수 (기본값 없음) 라 시험은 명시 값을 넘긴다.
    ⚠ 고치기 전 코드 (61b6a9ec5 · s_min 인자 없음) 에서는 그 키만 빼고 부른다 — 그 결손은 SMIN 시험이 따로 잡고, 나머지 시험은
      서명 오류로 한꺼번에 무너지지 않고 **각자의 이유**로 통과 · 실패한다 (반례 수 ≠ 검사 수 · SELF-124).  고친 코드에서는 늘 넘긴다."""
    k = dict(kw)
    if 's_min_um' in k and not _cj_has_smin():
        k.pop('s_min_um')
    return k


def registry(sid, addr, vox=H, lo=(0.0, 0.0, 0.0), **kw):
    P, PH, F, K = addr
    k = dict(r_f_um=RF, tol_ff_um=TOL, L_par_um=LPAR, r_port_um=RPORT, gap_tol=2.0, s_min_um=S_MIN)
    k.update(kw)
    return quiet(CJ.cjunc_registry, sid, tuple(float(x) for x in lo), vox, P, PH, F, K, **reg_kw(k))


def plan(reg, rj, **kw):
    k = dict(unreg_law='cut', ptfe_stamp='off')
    k.update(kw)
    return CJ.cjunc_plan(reg, rj, **k)


def solve(sid, sig, n, cj=None, vox=H, **kw):
    with direct_solver():
        return quiet(S3.solve_sigma_z, sid, sig, vox, z_top_um=float(n[2]) * vox, z_bot_um=0.0, cjunc=cj, **kw)


def solve_legacy(sid, sig, n, vox=H, **kw):
    with direct_solver():
        return quiet(S3.solve_sigma_z, sid, sig, vox, z_top_um=float(n[2]) * vox, z_bot_um=0.0, **kw)


def I_of(res, n, vox=H):
    """해 → 단자 전류 (코드 단위 · ΔV = 1) = σ_eff · A / L."""
    zb, zt = res['plate_z_um']
    return res['sigma_eff'] * (n[0] * n[1] * vox * vox) / (zt - zb)


def chain_I(gs):
    return 1.0 / sum(1.0 / g for g in gs)


def ref_I(nn, edges, bot, top):
    """손으로 세운 회로 (독립 기준) — 노드 nn 개 · edges = [(i, j, g)] · bot/top = [(i, g)] · ΔV = 1 → 아래 판 전류."""
    L = np.zeros((nn, nn)); b = np.zeros(nn)
    for i, j, g in edges:
        L[i, i] += g; L[j, j] += g; L[i, j] -= g; L[j, i] -= g
    for i, g in bot:
        L[i, i] += g; b[i] += g
    for i, g in top:
        L[i, i] += g
    phi = np.linalg.solve(L, b)
    return float(sum(g * (1.0 - phi[i]) for i, g in bot))


def rel(a, b):
    return abs(a - b) / max(abs(b), 1e-300)


def rjc(rj):
    """R_j [Ω] → 코드 단위 저항 (1/g · g = 1e4/R_j)."""
    return rj / 1.0e4


# ── 픽스처 정의 (꼭짓점 = 셀 중심 · µm) ──
#  F1 cross_shared: A 위로 (1,1,0..3) 끝 · B 는 A 끝점에서 +x 로 (1..4,1,3) 뒤 +z 로 (4,1,4..7) → 교차 셀 (1,1,3) = 멤버십 둘
F1_N = (6, 3, 8)
F1 = [[(1.5, 1.5, 0.5), (1.5, 1.5, 3.5)],
      [(1.5, 1.5, 3.5), (4.5, 1.5, 3.5), (4.5, 1.5, 7.5)]]
F1_I = lambda rj: chain_I([G_PL] + [G_AX] * 3 + ([1e4 / rj] if rj != 0 else []) + [G_AX] * 7 + [G_PL])   # noqa: E731
#  F2 cross_face: A (1,1,0..3) · B (2,1,3..7) — A 끝 ↔ B 시작 중심선 거리 1.0 (= r_A + r_B) · 면 (1,1,3)|(2,1,3)
F2_N = (5, 3, 8)
F2 = [[(1.5, 1.5, 0.5), (1.5, 1.5, 3.5)], [(2.5, 1.5, 3.5), (2.5, 1.5, 7.5)]]
#  F3 cross_edge: A 기둥 (1,1) · B 기둥 (2,2) — 모서리 인접 (옛 단절) · 중심선 거리 0.1414
F3_N = (4, 4, 8)
F3 = [[(1.95, 1.95, 0.5), (1.95, 1.95, 3.5)], [(2.05, 2.05, 3.5), (2.05, 2.05, 7.5)]]
#  F4 pass_through: A 전 높이 (1,1,0..7) · B 가로 (0..4,1,3) 가 교차 셀 (1,1,3) 을 지난다 (B = 매달린 가지)
F4_N = (6, 3, 8)
F4 = [[(1.5, 1.5, 0.5), (1.5, 1.5, 7.5)], [(0.5, 1.5, 3.5), (4.5, 1.5, 3.5)]]
#  F5 series: A (1,1,0..2) → B (2,2,2..4) → C (1,1,4..7) — 접합 둘 (모서리 인접 끝–끝)
F5_N = (4, 4, 8)
F5 = [[(1.95, 1.95, 0.5), (1.95, 1.95, 2.5)], [(2.05, 2.05, 2.5), (2.05, 2.05, 4.5)],
      [(1.95, 1.95, 4.5), (1.95, 1.95, 7.5)]]
#  F6 two_sites: A (1,1,0..4) 아래 판 · B 는 (2,1,1) 에서 A 에 닿고 돌아 (2,1,4) 에서 다시 닿은 뒤 위로 (2,1,4..8) 위 판
F6_N = (6, 3, 9)
F6 = [[(1.5, 1.5, 0.5), (1.5, 1.5, 4.5)],
      [(2.5, 1.5, 1.5), (4.5, 1.5, 1.5), (4.5, 1.5, 4.5), (2.5, 1.5, 4.5), (2.5, 1.5, 8.5)]]
#  F10 site_cut: F6 의 둘째 자리를 x 2.9 로 — 셀은 면 인접 (2,1,4)|(1,1,4) 인데 중심선 거리 1.4 > 1.1 (미등록)
F10 = [[(1.5, 1.5, 0.5), (1.5, 1.5, 4.5)],
       [(2.5, 1.5, 1.5), (4.5, 1.5, 1.5), (4.5, 1.5, 4.5), (2.9, 1.5, 4.5), (2.9, 1.5, 8.5)]]
#  K3 crossing_k3 (T1-8): 한 셀 (2,2,2) 에서 세 가닥 직교 교차
K3_N = (5, 5, 5)
K3 = [[(2.5, 2.5, 0.5), (2.5, 2.5, 4.5)], [(0.5, 2.5, 2.5), (4.5, 2.5, 2.5)], [(2.5, 0.5, 2.5), (2.5, 4.5, 2.5)]]
#  T110 self_contact (T1-10): 같은 fid 가 돌아와 (1,1,1)|(2,1,1) 면으로 닿는다 (경로 호 길이 s = 7 > S_MIN)
T110_N = (5, 5, 8)
T110 = [[(1.5, 1.5, 0.5), (1.5, 1.5, 3.5), (3.5, 1.5, 3.5), (3.5, 1.5, 1.5), (2.5, 1.5, 1.5), (2.5, 3.5, 1.5),
         (2.5, 3.5, 7.5)]]

# ── 길이 법칙 v0 픽스처 (J8 대체 · 1저자 10-20 밤 Q17) ──
#  LX 깊은 직교 교차: A (1,1,0..5) 아래 판 · B 가로 (0..4,1,3) 뒤 위로 (4,1,3..7) 위 판 — 중심선이 (1.5,1.5,3.5) 에서 만난다 (d0 = 0) ·
#     닿음 길이 = 각 가닥 2·(r_A + r_B) = L_par 정확히 → 배율 1 · 회로 = 판 + A 3 면 + 접합 + B 7 면 + 판
LX_N = (6, 3, 8)
LX = [[(1.5, 1.5, 0.5), (1.5, 1.5, 5.5)], [(0.5, 1.5, 3.5), (4.5, 1.5, 3.5), (4.5, 1.5, 7.5)]]
LX_I = lambda rj: chain_I([G_PL] + [G_AX] * 3 + [1e4 / rj] + [G_AX] * 7 + [G_PL])   # noqa: E731
#  LP 나란한 두 섬유: A (1,1,0..7) 아래 판 · B (2,1,2..10) 위 판 · 중심선 거리 0.6 (< r_A + r_B = 1) · 겹침 z [2.5, 7.7] = 5.2 →
#     닿음 길이 = 겹침 + √(1 − 0.6²) = 5.2 + 0.8 = 6.0 = 3 L_par (A 는 아래로 · B 는 위로 0.8 더 닿는다) → 배율 3 ·
#     포트는 같은 높이 (평행 최근접점 · 동률 = 같은 방향 규칙) → 회로 = 판 + 섬유 10 면 + 접합 1/(3/R_j,0) + 판.
#     ⚠ 거리를 정확히 r_A + r_B (1.0) 로 두면 닿음 경계가 접선이라 (거리 = √(1 + δ²)) sqrt 반올림이 δ ≲ 1.5e-8 을 닿음으로 세어
#       L_c = 6 + 1.8e-8 (구현 B 실측 · 고치기 전 실행) — 기계 정밀도 회로 대조가 깨진다.  0.6 이면 경계가 횡단 (기울기 0.8) 이다.
LP_N = (5, 3, 11)
LP = [[(1.5, 1.5, 0.5), (1.5, 1.5, 7.7)], [(2.1, 1.5, 2.5), (2.1, 1.5, 10.5)]]
LP_I = lambda rj, m=3.0: chain_I([G_PL] + [G_AX] * 10 + [m * 1e4 / rj] + [G_PL])   # noqa: E731
#  KU U 자로 접힌 한 섬유: 다리 1 위로 (1,1,0..4) · 위 가로 · 다리 2 아래로 (x 2.5 → 2.3 기울어 다리 1 에 다가간다 · (2,1,4..1)) ·
#     아래 가로 (2..4,1,1) · 다리 3 위로 (4,1,1..7) 위 판.  다리 1 ↔ 다리 2 = 같은 fid 비연속 면 셋 (z 1 · 2 · 3) = 자기 접합 후보 하나.
#     두 최근접점 = (1.5,1.5,1.5) ↔ (2.3,1.5,1.5) (거리 0.8 · 유일) → 경로 호 길이 s = 3 + 1 + √(0.2² + 3²)
KU_N = (6, 3, 8)
KU = [[(1.5, 1.5, 0.5), (1.5, 1.5, 4.5), (2.5, 1.5, 4.5), (2.3, 1.5, 1.5), (4.5, 1.5, 1.5), (4.5, 1.5, 7.5)]]
KU_S = 3.0 + 1.0 + math.sqrt(0.2 ** 2 + 3.0 ** 2)
#  KW 같은 U 인데 다리 2 가 x 2.7 (중심선 거리 1.2 > r_f + r_f) — 셀은 면으로 닿지만 중심선은 닿지 않는다 → 자기 L_c (닿음) = 0
KW = [[(1.5, 1.5, 0.5), (1.5, 1.5, 4.5), (2.7, 1.5, 4.5), (2.7, 1.5, 1.5), (4.5, 1.5, 1.5), (4.5, 1.5, 7.5)]]


def seq_cells(verts, vox=H):
    """폴리라인 → 셀 열 (연속 중복 제거) — 기대 회로를 세우는 독립 도구 (생산 스탬프와 같은 원시 함수 `segment_cells`)."""
    from fibre_segment_raster import segment_cells
    pts = densify(verts)
    cs = np.vstack([segment_cells(pts[i], pts[i + 1], vox) for i in range(len(pts) - 1)])
    keep = np.ones(len(cs), bool)
    keep[1:] = np.any(cs[1:] != cs[:-1], axis=1)
    return [tuple(int(v) for v in c) for c in cs[keep]]


# ═════════════════════════ C0 — 끔 비트 동일 ═════════════════════════
def _load_base():
    try:
        src = subprocess.run(['git', '-C', ROOT, 'show', f'{BASE_COMMIT}:scripts/step3_sigma.py'],
                             capture_output=True, check=True).stdout
    except Exception as e:                                 # noqa: BLE001
        return None, f'git show 실패 {type(e).__name__}: {e}'
    d = tempfile.mkdtemp(prefix='s3base_')
    p = os.path.join(d, 'step3_sigma_base_d1768.py')
    with open(p, 'wb') as fh:
        fh.write(src)
    spec = importlib.util.spec_from_file_location('step3_sigma_base_d1768', p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m, ''


def _random_bed(seed, mod, vox=0.25, n=(24, 24, 32)):
    rng = np.random.default_rng(seed)
    box = np.array(n, float) * vox
    na = int(rng.integers(5, 10))
    am_c = rng.uniform([0.5, 0.5, 0.5], box - 0.5, (na, 3)); am_r = rng.uniform(0.7, 1.4, na)
    am_t = rng.integers(1, 3, na)
    polys, ph = [], []
    for _ in range(int(rng.integers(4, 8))):                       # VGCF 경로
        p0 = rng.uniform(0.2, box - 0.2); d = rng.normal(size=3); d /= np.linalg.norm(d)
        p1 = np.clip(p0 + d * rng.uniform(2.0, 5.0), 0.05, box - 0.05)
        polys.append([p0, p1]); ph.append(2)
    for _ in range(2):                                              # PTFE 경로 (centerline 스탬프)
        p0 = rng.uniform(0.2, box - 0.2); d = rng.normal(size=3); d /= np.linalg.norm(d)
        polys.append([p0, np.clip(p0 + 3.0 * d, 0.05, box - 0.05)]); ph.append(4)
    P, PH, F, K = [], [], [], []
    for i, (v, p) in enumerate(zip(polys, ph)):
        pts = densify(v, 0.1)
        P.append(pts); PH.append(np.full(len(pts), p)); F.append(np.full(len(pts), 100 + i)); K.append(np.full(len(pts), 1))
    sd = rng.uniform(0.2, box - 0.2, (int(rng.integers(10, 30)), 3))    # SDCP 점 (구 스탬프)
    P.append(sd); PH.append(np.full(len(sd), 5)); F.append(np.arange(len(sd)) + 500); K.append(np.zeros(len(sd), int))
    P = np.vstack(P); PH = np.concatenate(PH); F = np.concatenate(F); K = np.concatenate(K)
    se = rng.uniform(0, box, (4000, 3))
    sid, pid = mod.rasterize(am_c, am_r, am_t, P, PH, (0., 0., 0.), tuple(box), vox, se_pts=se,
                             sdcp_sphere_d_um=0.5, add_fid=F, add_kind=K, bridge_um=0.3)
    return sid, pid, box


@case('C0')
def t_c0_off_bitid():
    base, why = _load_base()
    if not chk('C0 기준 모듈 (커밋 d1768cf0c 의 step3_sigma) 을 읽었다', base is not None, why):
        return
    nbed = 4 if QUICK else 8
    allsame, n_in = True, 0
    for s in range(nbed):
        sid_b, pid_b, box = quiet(_random_bed, 1000 + s, base)
        sid_c, pid_c, _ = quiet(_random_bed, 1000 + s, S3)
        same_raster = sid_b.tobytes() == sid_c.tobytes() and pid_b.tobytes() == pid_c.tobytes()
        allsame &= same_raster
        te_b = base.electronic_sigma_table(0.010, 0.005, 100.0, 10.0, 250.0)
        ti_b = base.ionic_sigma_table(0.3e-3, 3.0e-3)
        for tab, per in ((te_b, False), (ti_b, False) if s % 2 == 0 else (te_b, True)):
            n_in += 1
            rb = quiet(base.solve_sigma_z, sid_b, tab, 0.25, return_field=True, z_top_um=float(box[2]), z_bot_um=0.0,
                       periodic_xy=per)
            rc = quiet(S3.solve_sigma_z, sid_c, tab, 0.25, return_field=True, z_top_um=float(box[2]), z_bot_um=0.0,
                       periodic_xy=per)
            same = (np.float64(rb['sigma_eff']).tobytes() == np.float64(rc['sigma_eff']).tobytes()
                    and rb['n_dof'] == rc['n_dof'] and rb.get('cg_info') == rc.get('cg_info')
                    and np.float64(rb.get('resid', 0.0)).tobytes() == np.float64(rc.get('resid', 0.0)).tobytes()
                    and (('phi' not in rb and 'phi' not in rc) or rb['phi'].tobytes() == rc['phi'].tobytes())
                    and sorted(rb) == sorted(rc))
            if not same:
                print(f'    C0 차이 seed {1000 + s} per {per}: σ {rb["sigma_eff"]!r} ↔ {rc["sigma_eff"]!r} · '
                      f'키 {sorted(set(rb) ^ set(rc))}')
            allsame &= same
    chk(f'C0 끔 (cjunc=None · 수렴 증서 끔) = 옛 경로 비트 동일 — raster · σ · φ · n_dof · cg_info · resid · 결과 키 ({n_in} 입력)',
        allsame)


# ═════════════════════════ PIECE — 멤버십 셀 = 생산 스탬프 셀 ═════════════════════════
@case('PIECE')
def t_piece():
    rng = np.random.default_rng(7)
    allok = True
    for trial in range(12):
        n = (16, 16, 16); box = np.array(n, float) * 0.5
        polys = []
        for _ in range(5):
            p = [rng.uniform(1, box - 1)]
            for _ in range(int(rng.integers(1, 5))):
                d = rng.normal(size=3); d /= np.linalg.norm(d)
                p.append(np.clip(p[-1] + d * rng.uniform(0.5, 2.5), 0.01, box - 0.01))
            polys.append(p)
        P, PH, F, K = rows(polys, step=0.12)
        if trial % 3 == 0:                                  # 끊기 (gap) 가 걸리는 경로 하나
            m = F == F[0]
            idx = np.flatnonzero(m)
            if len(idx) > 6:
                keep = np.ones(len(P), bool); keep[idx[2:4]] = False
                P, PH, F, K = P[keep], PH[keep], F[keep], K[keep]
        sid, _ = S3.rasterize(*NO_AM, P, PH, (0., 0., 0.), tuple(box), 0.5, add_fid=F, add_kind=K)
        ijk, ph = S3._fibre_segment_ijk(P, PH, F, np.zeros(3), 0.5, np.array(n), 2.0, add_kind=K)
        want = {tuple(c) for c in ijk[ph == 2]}
        try:
            reg = quiet(CJ.cjunc_registry, sid, (0., 0., 0.), 0.5, P, PH, F, K,
                        **reg_kw(dict(r_f_um=0.25, tol_ff_um=0.05, L_par_um=1.0, r_port_um=1.0, gap_tol=2.0, s_min_um=1.5)))
            pos = reg['positions']
            inb = pos['lin'] >= 0
            got = {tuple(int(v) for v in np.unravel_index(int(l), n)) for l in pos['lin'][inb]}
        except Exception as e:                             # noqa: BLE001
            got = None
            print(f'    PIECE trial {trial}: {type(e).__name__}: {e}')
        allok &= (got == want)
    chk('PIECE 멤버십 셀 (상자 안 위치 전부) = `_fibre_segment_ijk` 의 VGCF 셀 (12 무작위 · 끊기 포함 · 같은 끊기 규칙)', allok)


# ═════════════════════════ C1 · T1-7 ═════════════════════════
@case('C1')
def t_c1_cross_shared():
    P = rows(F1)
    sid, _ = bed(P, F1_N)
    reg = registry(sid, P)
    inst = reg['instances']
    chk('C1 instance 하나 (A–B · 교차 셀) · 교차 셀 = 멤버십 둘 (추가 dof 1)',
        len(inst['fi']) == 1 and reg['n_extra_dofs'] == 1, f"n {len(inst['fi'])} extra {reg['n_extra_dofs']}")
    errs, Is = [], []
    for rj in (1.0e1, 1.0e3, 1.0e5):
        r = solve(sid, sig_e(), F1_N, plan(reg, rj))
        Is.append(I_of(r, F1_N)); errs.append(rel(Is[-1], F1_I(rj)))
    chk('C1 σ = 해석 직렬 사슬 판 + A 3 면 + R_j + B 7 면 + 판 (R_j 10 · 1e3 · 1e5 Ω · 1e-12)', max(errs) < 1e-12, f'{errs}')
    chk('C1 Rayleigh — R_j 가 커지면 σ 엄격히 줄어든다 (같은 그래프)', Is[0] > Is[1] > Is[2], f'{Is}')
    pe = r['plate_edges']
    chk('C1 판 간선 원장 = 남은 결합만 (좌표 · g 길이 같음 · 해의 판 전류와 같은 계)',
        all(len(pe[s][0][0]) == len(pe[s][1]) for s in ('bot', 'top')) and r['cjunc']['solved'] is True)
    r0 = solve(sid, sig_e(), F1_N, plan(reg, 0.0, allow_rj_limits=True))
    rl = solve_legacy(sid, sig_e(), F1_N)
    chk('T1-7 R_j → 0 (축약) = 축약 그래프 = 옛 융합 교차 셀 (1e-12)', rel(I_of(r0, F1_N), I_of(rl, F1_N)) < 1e-12
        and rel(I_of(r0, F1_N), F1_I(0)) < 1e-12, f'{I_of(r0, F1_N)} ↔ {I_of(rl, F1_N)}')
    ri = solve(sid, sig_e(), F1_N, plan(reg, math.inf, allow_rj_limits=True))
    chk('T1-7 R_j = ∞ → 가닥 사이 전류 0 (A–B 가 접합으로만 이어진다 → 관통 없음)',
        ri['sigma_eff'] == 0.0 and ri.get('reason') == 'no_through_component', f"{ri.get('reason')} σ {ri['sigma_eff']}")


@case('C2')
def t_c2_face_edge():
    P = rows(F2)
    sid, _ = bed(P, F2_N)
    reg = registry(sid, P)
    rj = 2.0e3
    r = solve(sid, sig_e(), F2_N, plan(reg, rj))
    want = chain_I([G_PL] + [G_AX] * 3 + [1e4 / rj] + [G_AX] * 4 + [G_PL])
    chk('C2a cross_face — 옛 융합 면 절단 + 접합 간선 하나 (해석 사슬 1e-12)', rel(I_of(r, F2_N), want) < 1e-12,
        f'{I_of(r, F2_N)} ↔ {want}')
    rl = solve_legacy(sid, sig_e(), F2_N)
    chk('C2a 옛 경로 = 융합 면 g (대조 · 다른 값)', rel(I_of(rl, F2_N), chain_I([G_PL] + [G_AX] * 8 + [G_PL])) < 1e-12)
    r0 = solve(sid, sig_e(), F2_N, plan(reg, 0.0, allow_rj_limits=True))
    want0 = chain_I([G_PL] + [G_AX] * 3 + [G_AX] * 4 + [G_PL])          # 포트 두 dof 병합 = 그 면이 사라진 사슬
    chk('T1-7 R_j → 0 = 포트 병합 회로 (옛 융합보다 강하다 · 1e-12)', rel(I_of(r0, F2_N), want0) < 1e-12,
        f'{I_of(r0, F2_N)} ↔ {want0}')
    P3 = rows(F3)
    sid3, _ = bed(P3, F3_N)
    reg3 = registry(sid3, P3)
    r3 = solve(sid3, sig_e(), F3_N, plan(reg3, rj))
    rl3 = solve_legacy(sid3, sig_e(), F3_N)
    want3 = chain_I([G_PL] + [G_AX] * 3 + [1e4 / rj] + [G_AX] * 4 + [G_PL])
    chk('C2b cross_edge — 옛 경로 단절 (관통 없음)', rl3['sigma_eff'] == 0.0)
    chk('C2b · J12 접합으로만 이어진 성분을 가지치기가 안 지운다 (해석 사슬 1e-12)', rel(I_of(r3, F3_N), want3) < 1e-12,
        f'{I_of(r3, F3_N)} ↔ {want3}')


@case('C3')
def t_c3_pass_through():
    P = rows(F4)
    sid, _ = bed(P, F4_N)
    reg = registry(sid, P)
    want = chain_I([G_PL] + [G_AX] * 7 + [G_PL])
    Is = [I_of(solve(sid, sig_e(), F4_N, plan(reg, rj, allow_rj_limits=True)), F4_N) for rj in (10.0, 1.0e5, math.inf)]
    chk('C3 · J6 교차 셀을 지나는 가닥 A 는 R_j 와 무관 · R_j = ∞ 에서도 연속 (1e-12)', max(rel(x, want) for x in Is) < 1e-12,
        f'{Is} ↔ {want}')
    chk('C3 교차 셀 = dof 둘 (A · B 각자 축방향 연결)', reg['n_extra_dofs'] == 1, f"{reg['n_extra_dofs']}")


@case('C4')
def t_c4_series_units():
    P = rows(F5)
    sid, _ = bed(P, F5_N)
    reg = registry(sid, P)
    base = [G_PL] + [G_AX] * 2 + [G_AX] * 2 + [G_AX] * 3 + [G_PL]
    rA, rB = 1.0e3, 5.0e3
    IA = I_of(solve(sid, sig_e(), F5_N, plan(reg, rA)), F5_N)
    IB = I_of(solve(sid, sig_e(), F5_N, plan(reg, rB)), F5_N)
    wA = chain_I(base + [1e4 / rA] * 2); wB = chain_I(base + [1e4 / rB] * 2)
    chk('C4 series_chain N = 3 · 접합 둘 — 해석 (1e-12) · 기울기 dR/dR_j = N − 1', rel(IA, wA) < 1e-12 and rel(IB, wB) < 1e-12
        and abs(((1 / IB - 1 / IA) / (rjc(rB) - rjc(rA))) - 2.0) < 1e-9, f'{IA} {wA} · {IB} {wB}')
    old = CJ.junction_g_code
    detected = []
    for nm, fn in (('1e4 빠짐', lambda r: 1.0 / r), ('×1e8', lambda r: 1.0e12 / r)):
        CJ.junction_g_code = fn
        try:
            Im = I_of(solve(sid, sig_e(), F5_N, plan(reg, rA)), F5_N)
            detected.append(rel(Im, wA) > 1e-6)
        except Exception:                                  # noqa: BLE001
            detected.append(True)
        finally:
            CJ.junction_g_code = old
    chk('C4 단위 변이 (1e4 빠짐 · ×1e8) 를 해석 대조가 잡는다', all(detected), f'{detected}')


@case('C5')
def t_c5_instances():
    P = rows(F5)
    sid, _ = bed(P, F5_N)
    reg = registry(sid, P)
    I0 = I_of(solve(sid, sig_e(), F5_N, plan(reg, 1e3)), F5_N)
    Pf = rows(F5, step=0.11)                                       # 같은 접촉을 더 잘게 (조각 수 ↑)
    sidf, _ = bed(Pf, F5_N)
    regf = registry(sidf, Pf)
    If = I_of(solve(sidf, sig_e(), F5_N, plan(regf, 1e3)), F5_N)
    chk('C5 · J2c 조각을 잘게 해도 instance 수 · σ 같다', len(regf['instances']['fi']) == len(reg['instances']['fi']) == 2
        and rel(If, I0) < 1e-12 and sidf.tobytes() == sid.tobytes(), f"{len(regf['instances']['fi'])} {If} {I0}")
    Pr = rows([F5[2], F5[0], F5[1]], fids=[30, 10, 20])            # 섬유 순서 바꿈 (fid 그대로)
    sidr, _ = bed(Pr, F5_N)
    regr = registry(sidr, Pr)
    Ir = I_of(solve(sidr, sig_e(), F5_N, plan(regr, 1e3)), F5_N)
    Pv = rows([v[::-1] for v in F5])                               # 점 역순
    sidv, _ = bed(Pv, F5_N)
    regv = registry(sidv, Pv)
    Iv = I_of(solve(sidv, sig_e(), F5_N, plan(regv, 1e3)), F5_N)
    chk('C5 · J2c 섬유 순서 · 점 역순에 instance 수 · σ 불변 (1e-12)',
        len(regr['instances']['fi']) == 2 and len(regv['instances']['fi']) == 2 and rel(Ir, I0) < 1e-12 and rel(Iv, I0) < 1e-12,
        f'{Ir} {Iv} {I0}')
    P6 = rows(F6)
    sid6, _ = bed(P6, F6_N)
    reg6 = registry(sid6, P6)
    chk('C5 같은 쌍 떨어진 두 곳 = instance 둘 (쌍 ID 로 접지 않는다)', len(reg6['instances']['fi']) == 2
        and len(set(zip(reg6['instances']['fi'].tolist(), reg6['instances']['fj'].tolist()))) == 1, f"{reg6['instances']['fi']}")


def _f6_reference(rj, sv=SV, second_site=True, fused_second=False):
    """F6/F10 사다리 — 노드: A (1,1,0..4) = 0..4 · B 셀 열 = 5.. · 접합 자리 1: A1 ↔ B0 · 자리 2: A4 ↔ B (2,1,4)."""
    A = [(1, 1, k) for k in range(5)]
    Bc = seq_cells(F6[1] if not fused_second else F10[1])
    nA = len(A)
    gax = sv * H; gpl = sv * H * H / (0.5 * H)
    E = [(i, i + 1, gax) for i in range(nA - 1)] + [(nA + i, nA + i + 1, gax) for i in range(len(Bc) - 1)]
    jB0 = nA + Bc.index((2, 1, 1)); jB4 = nA + Bc.index((2, 1, 4))
    E.append((1, jB0, 1e4 / rj))
    if second_site:
        E.append((4, jB4, gax if fused_second else 1e4 / rj))
    bot = [(0, gpl)]; top = [(nA + len(Bc) - 1, gpl)]
    return ref_I(nA + len(Bc), E, bot, top)


@case('T1-6')
def t_t16_multi():
    P = rows(F6)
    sid, _ = bed(P, F6_N)
    reg = registry(sid, P)
    rj = 3.0e3
    r6 = solve(sid, sig_e(), F6_N, plan(reg, rj))
    I = I_of(r6, F6_N)
    want = _f6_reference(rj)
    chk('T1-6 두 자리 사다리 회로 (손으로 세운 기준 · 1e-12)', rel(I, want) < 1e-12, f'{I} ↔ {want}')
    jI = r6['_cjunc']['junction_current_code']
    chk('T1-6 원장 — instance 마다 접합 전류 · 두 자리 합 = 단자 전류 (A → B 는 접합으로만 · 1e-10)',
        len(jI) == 2 and np.all(np.isfinite(jI)) and rel(float(np.sum(np.abs(jI))), I) < 1e-10, f'{jI} {I}')
    big = sig_e(s_vgcf=1.0e9)
    Ib = I_of(solve(sid, big, F6_N, plan(reg, rj)), F6_N)
    chk('T1-6 등전위 극한 (σ 1e9) — R → R_j/2 (상대 1e-5)', rel(1.0 / Ib, rjc(rj) / 2.0) < 1e-5, f'{1 / Ib} ↔ {rjc(rj) / 2}')


@case('T1-8')
def t_t18_k3():
    n = K3_N
    P = rows(K3)
    sid, _ = bed(P, n)
    reg = registry(sid, P)
    inst = reg['instances']
    pos = reg['positions']
    ok_ports = True
    for k in range(len(inst['fi'])):
        pi, pj = int(inst['port_i'][k]), int(inst['port_j'][k])
        ok_ports &= (pi >= 0 and pj >= 0 and pi != pj and pos['lin'][pi] == pos['lin'][pj])
    chk('T1-8 한 셀 세 가닥 → 추가 dof 2 · instance 3 (쌍마다) · J9 포트 = 같은 셀 · 서로 다른 dof',
        reg['n_extra_dofs'] == 2 and len(inst['fi']) == 3 and ok_ports, f"extra {reg['n_extra_dofs']} n {len(inst['fi'])}")
    want = chain_I([G_PL] + [G_AX] * 4 + [G_PL])
    Is = [I_of(solve(sid, sig_e(), n, plan(reg, rj, allow_rj_limits=True)), n) for rj in (1.0, 1e6, math.inf)]
    chk('T1-8 축 연결이 각자 fid 로 — 세로 가닥 σ 가 R_j 와 무관 (1e-12)', max(rel(x, want) for x in Is) < 1e-12, f'{Is} {want}')


@case('T1-9')
def t_t19_fiber_sphere():
    P = rows([[(0.0, 0.0, -1.0), (0.0, 0.0, 1.0)]], step=0.1)
    am_c = np.array([[2.12, 0.0, 0.0]]); am_r = np.array([2.0])
    n0 = CJ.va_census(P[0], P[1], P[2], P[3], am_c, am_r, r_f_um=0.075, tol_fs_um=0.0, gap_tol=2.0)
    am_c2 = np.array([[2.07, 0.0, 0.0]])
    n1 = CJ.va_census(P[0], P[1], P[2], P[3], am_c2, am_r, r_f_um=0.075, tol_fs_um=0.0, gap_tol=2.0)
    chk('T1-9 J2b 섬유–구 = 중심선 ↔ 구 중심 ≤ r_f + R_AM + tol_fs — d 2.12 = 접촉 아님 (2.15 문자식 오판 아님) · d 2.07 = 접촉',
        n0 == 0 and n1 == 1, f'{n0} {n1}')


@case('T1-10')
def t_t110_self():
    n = T110_N
    poly = T110
    P = rows(poly)
    sid, _ = bed(P, n)
    reg = registry(sid, P)
    inst = reg['instances']
    nself = int(np.sum(inst['self']))
    chk('T1-10 같은 fid 비연속 두 셀 면 → 자기 접합 instance (f, f) 하나', nself == 1 and len(inst['fi']) == 1,
        f"self {nself} n {len(inst['fi'])}")
    seq = seq_cells(poly[0])
    k1, k8 = seq.index((1, 1, 1)), seq.index((2, 1, 1))
    rj = 4.0e3
    E = [(i, i + 1, G_AX) for i in range(len(seq) - 1)] + [(k1, k8, 1e4 / rj)]
    want = ref_I(len(seq), E, [(0, G_PL)], [(len(seq) - 1, G_PL)])
    I = I_of(solve(sid, sig_e(), n, plan(reg, rj)), n)
    chk('T1-10 자기 접합 = R_j 간선 (0 저항 지름길 아님 · 사다리 기준 1e-12)', rel(I, want) < 1e-12, f'{I} ↔ {want}')
    Ii = I_of(solve(sid, sig_e(), n, plan(reg, math.inf, allow_rj_limits=True)), n)
    wi = chain_I([G_PL] + [G_AX] * (len(seq) - 1) + [G_PL])
    chk('T1-10 R_j = ∞ → 우회로 전부 (면 지름길 없음 · 1e-12)', rel(Ii, wi) < 1e-12, f'{Ii} ↔ {wi}')


@case('T1-11')
def t_t111_tie():
    #  A 아래 판 (1,1,0..5) · B 는 A 옆 x 2.5 · z = 3.0 (셀 경계) 에서 시작해 +x 뒤 위 판 — A 의 접점 (1.5,1.5,3.0) 은 A 의 두 셀
    #  (1,1,2) · (1,1,3) 중심에서 등거리 (0.5) → 동률.  B 가 전류를 나르므로 어느 포트냐가 회로를 바꾼다 (판별력).
    n = (6, 3, 8)
    polys = [[(1.5, 1.5, 0.5), (1.5, 1.5, 5.5)], [(2.5, 1.5, 3.0), (4.5, 1.5, 3.0), (4.5, 1.5, 7.5)]]
    P = rows(polys)
    sid, _ = bed(P, n)
    reg = registry(sid, P)
    inst = reg['instances']
    pos = reg['positions']
    ok = len(inst['fi']) == 1
    tie = int(reg['census'].get('n_port_ties', -1))
    pa = int(inst['port_i'][0]) if ok else -1
    cell = tuple(int(v) for v in np.unravel_index(int(pos['lin'][pa]), n)) if pa >= 0 else None
    chk('T1-11 등거리 두 후보 포트 → 정준 방향 경로 번호가 작은 셀 (1,1,2) · 동률 수 1 기록', ok and tie == 1 and cell == (1, 1, 2),
        f'tie {tie} cell {cell}')
    rj = 1e3
    I0 = I_of(solve(sid, sig_e(), n, plan(reg, rj)), n)
    want = chain_I([G_PL] + [G_AX] * 2 + [1e4 / rj] + [G_AX] * 6 + [G_PL])
    chk('T1-11 포트 (1,1,2) 회로 = 해석 사슬 (A 2 면 + R_j + B 6 면 · 1e-12)', rel(I0, want) < 1e-12, f'{I0} ↔ {want}')
    Pv = rows([polys[0][::-1], polys[1][::-1]])
    sidv = bed(Pv, n)[0]
    Iv = I_of(solve(sidv, sig_e(), n, plan(registry(sidv, Pv), rj)), n)
    Pr = rows([polys[1], polys[0]], fids=[20, 10])
    sidr = bed(Pr, n)[0]
    Ir = I_of(solve(sidr, sig_e(), n, plan(registry(sidr, Pr), rj)), n)
    chk('T1-11 점 역순 · 섬유 순서에 σ 불변 (동률 규칙이 방향 · 행 순서와 무관 · 1e-12)', rel(Iv, I0) < 1e-12 and rel(Ir, I0) < 1e-12,
        f'{I0} {Iv} {Ir}')


@case('T1-12')
def t_t112_site():
    P = rows(F10)
    sid, _ = bed(P, F6_N)
    reg = registry(sid, P)
    chk('T1-12 같은 쌍 두 자리 중 한 자리만 instance', len(reg['instances']['fi']) == 1, f"{len(reg['instances']['fi'])}")
    rj = 3.0e3
    Ic = I_of(solve(sid, sig_e(), F6_N, plan(reg, rj, unreg_law='cut')), F6_N)
    If = I_of(solve(sid, sig_e(), F6_N, plan(reg, rj, unreg_law='fused')), F6_N)
    wc = _f6_reference(rj, second_site=False, fused_second=True)
    wf = _f6_reference(rj, second_site=True, fused_second=True)
    chk('T1-12 미등록 자리 cut = 첫 자리 접합만 (1e-12) · fused = 첫 자리 접합 + 둘째 자리 융합 면 (1e-12)',
        rel(Ic, wc) < 1e-12 and rel(If, wf) < 1e-12, f'{Ic} {wc} · {If} {wf}')
    chk('T1-12 같은 그래프 Rayleigh: cut ≤ fused', Ic <= If * (1 + 1e-12))
    chk('T1-12 법칙 미선언 = 거부 (자동 fallback 없음)', raises(lambda: CJ.cjunc_plan(reg, rj, unreg_law=None, ptfe_stamp='off')))


@case('T1-5p')
def t_t15_lead():
    P = rows(F1)
    sid, _ = bed(P, F1_N)
    reg = registry(sid, P)
    chk("T1-5′ 단자 기준 R_j (리드 빼기 기록 없음) = 거부", raises(lambda: plan(reg, 1e3, rj_reference='terminal_two_probe')))
    chk("T1-5′ 리드 빼기 기록이 와도 v0 = 거부 (모형 내부값만)", raises(lambda: plan(reg, 1e3, lead_subtraction={'R_leads_ohm': 2.0})))
    chk('T1-5′ 음수 · NaN R_j = 거부', raises(lambda: plan(reg, -1.0)) and raises(lambda: plan(reg, float('nan'))))
    chk('T1-5′ R_j 극한 (0 · ∞) = 사다리 천장 · 바닥 표지 없이 정량 거부', raises(lambda: plan(reg, 0.0)) and raises(lambda: plan(reg, math.inf)))


# ═════════════════════════ 길이 법칙 v0 (J8 대체 · 1저자 10-20 밤 Q17 = 권고대로) ═════════════════════════
#  G_j = max(1, L_c/L_par) / R_j,0 — 긴 접촉 = 점 접합 L_c/L_par 개가 나란히 (선 접촉 협착 ∝ 길이의 1차 근사) · 새 손잡이 없음 ·
#  L_c = 닿음 (두 가닥 각각에서 중심선 거리 ≤ r_fi + r_fj 인 길이의 최댓값 · B 정의) · 간선 = instance 하나 (lumped) ·
#  절단 발자국 = 접촉 run 전체 · 꺾임 자기 접합 = 두 최근접점 사이 경로 호 길이 s < s_min 이면 접합 아님 (옛 복셀 융합 그대로).
#  기대값 = 손으로 세운 회로 · 손으로 잰 길이 (모듈 함수로 정답을 다시 만들지 않는다).
BASE_CJ_COMMIT = '61b6a9ec5'     # 점 접합 (길이 법칙 전 · 구현 B 끝) — 긴 접촉 없는 침대의 비트 같음 기준


def _plan_mult(p):
    """계획의 instance 배율 배열 (없으면 None — 고치기 전 코드)."""
    m = p.get('mult') if isinstance(p, dict) else None
    return None if m is None else np.asarray(m, np.float64)


def _try(fn, default=math.nan):
    try:
        return quiet(fn)
    except Exception as e:                                 # noqa: BLE001 — 거부 · 예외 = 기대값을 못 냄 (그 검사 실패)
        print(f'    (예외 {type(e).__name__}: {str(e)[:160]})')
        return default


def _load_base_cj():
    try:
        src = subprocess.run(['git', '-C', ROOT, 'show', f'{BASE_CJ_COMMIT}:scripts/carbon_junction.py'],
                             capture_output=True, check=True).stdout
    except Exception as e:                                 # noqa: BLE001
        return None, f'git show 실패 {type(e).__name__}: {e}'
    d = tempfile.mkdtemp(prefix='cjbase_')
    p = os.path.join(d, 'carbon_junction_base_61b6.py')
    with open(p, 'wb') as fh:
        fh.write(src)
    spec = importlib.util.spec_from_file_location('carbon_junction_base_61b6', p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m, ''


@contextlib.contextmanager
def cj_module(mod):
    """solve_sigma_z 는 호출 때 `import carbon_junction` 을 한다 — 기준 모듈로 풀 때 그 이름을 잠시 바꿔 끼운다."""
    old = sys.modules.get('carbon_junction')
    sys.modules['carbon_junction'] = mod
    try:
        yield
    finally:
        if old is None:
            sys.modules.pop('carbon_junction', None)
        else:
            sys.modules['carbon_junction'] = old


def _chain_edges(nn):
    return [(i, i + 1, G_AX) for i in range(nn - 1)]


@case('LEN-X')
def t_len_cross():
    P = rows(LX)
    sid, _ = bed(P, LX_N)
    reg = registry(sid, P)
    inst = reg['instances']
    chk('LEN-X 깊은 직교 교차 — instance 하나 · d0 = 0 · L_c = L_par = 2(r_A + r_B) (손으로 잰 닿음 길이 · 1e-12)',
        len(inst['fi']) == 1 and abs(float(inst['d0'][0])) < 1e-12 and abs(float(inst['Lc'][0]) - LPAR) < 1e-12,
        f"n {len(inst['fi'])} d0 {inst['d0']} Lc {inst['Lc']}")
    m = _plan_mult(plan(reg, 1e3))
    chk('LEN-X 배율 = 1 정확히 (max(1, L_c/L_par) · 경계 L_c = L_par 에서 연속)', m is not None and len(m) == 1 and m[0] == 1.0,
        f'{m}')
    errs = [rel(_try(lambda rj=rj: I_of(solve(sid, sig_e(), LX_N, plan(reg, rj)), LX_N)), LX_I(rj)) for rj in (1e1, 1e3, 1e5)]
    chk('LEN-X σ = 옛 점 접합 회로 (판 + A 3 면 + R_j + B 7 면 + 판 · R_j 10 · 1e3 · 1e5 Ω · 1e-12)', max(errs) < 1e-12, f'{errs}')


@case('LEN-BIT')
def t_len_bitid():
    """긴 접촉 없는 침대 (배율 전부 1) = 구현 B (61b6a9ec5 · 점 접합) 와 σ · n_dof · cg_info · resid · 접합 전류 비트 같음."""
    base, why = _load_base_cj()
    if not chk(f'LEN-BIT 기준 모듈 (커밋 {BASE_CJ_COMMIT} 의 carbon_junction) 을 읽었다', base is not None, why):
        return
    fx = (('F1', F1, F1_N), ('F2', F2, F2_N), ('F3', F3, F3_N), ('F5', F5, F5_N), ('F6', F6, F6_N), ('F10', F10, F6_N),
          ('LX', LX, LX_N), ('K3', K3, K3_N), ('T110', T110, T110_N))
    bad = []
    for nm, polys, n in fx:
        P = rows(polys)
        sid, _ = bed(P, n)
        for rj in (1e2, 3e3):
            try:
                rn = solve(sid, sig_e(), n, plan(registry(sid, P), rj))
                kb = dict(r_f_um=RF, tol_ff_um=TOL, L_par_um=LPAR, r_port_um=RPORT, gap_tol=2.0)
                regb = quiet(base.cjunc_registry, sid, (0.0, 0.0, 0.0), H, *P, **kb)
                pb = base.cjunc_plan(regb, rj, unreg_law='cut', ptfe_stamp='off')
                with cj_module(base):
                    rb = solve(sid, sig_e(), n, pb)
                same = (np.float64(rn['sigma_eff']).tobytes() == np.float64(rb['sigma_eff']).tobytes()
                        and rn['n_dof'] == rb['n_dof'] and rn.get('cg_info') == rb.get('cg_info')
                        and np.float64(rn.get('resid', 0.0)).tobytes() == np.float64(rb.get('resid', 0.0)).tobytes()
                        and np.asarray(rn['_cjunc']['junction_current_code']).tobytes()
                        == np.asarray(rb['_cjunc']['junction_current_code']).tobytes())
            except Exception as e:                         # noqa: BLE001
                same = False
                print(f'    LEN-BIT {nm} R_j {rj}: {type(e).__name__}: {e}')
            if not same:
                bad.append(f'{nm}@{rj:g}')
    chk(f'LEN-BIT 긴 접촉 없는 침대 {len(fx)} 개 × R_j 둘 = 점 접합 (구현 B) 과 σ · n_dof · cg_info · resid · 접합 전류 비트 같음',
        not bad, f'{bad}')


@case('LEN-P')
def t_len_parallel():
    P = rows(LP)
    sid, _ = bed(P, LP_N)
    reg = registry(sid, P)
    inst = reg['instances']
    chk('LEN-P 나란한 두 섬유 — instance 하나 · L_c = 6.0 = 3 L_par (손으로 센 겹침 · 1e-12)',
        len(inst['fi']) == 1 and abs(float(inst['Lc'][0]) - 3.0 * LPAR) < 1e-12, f"n {len(inst['fi'])} Lc {inst['Lc']}")
    m = _plan_mult(plan(reg, 1e3))
    chk('LEN-P 배율 = max(1, L_c/L_par) = 3 (1e-12)', m is not None and len(m) == 1 and abs(m[0] - 3.0) < 1e-12, f'{m}')
    errs = []
    for rj in (1e1, 1e3, 1e5):
        for law in ('cut', 'fused'):
            errs.append(rel(_try(lambda rj=rj, law=law: I_of(solve(sid, sig_e(), LP_N, plan(reg, rj, unreg_law=law)), LP_N)),
                            LP_I(rj)))
    chk('LEN-P σ = 해석 회로 (판 + 섬유 10 면 + 접합 1/(3/R_j,0) + 판 · R_j 10 · 1e3 · 1e5 Ω · 미등록 cut · fused · 기계 정밀도 1e-12)',
        max(errs) < 1e-12, f'{errs}')


@case('LEN-O')
def t_len_oblique():
    n = (12, 12, 5)
    C = np.array([6.0, 6.0, 2.5])
    ths = (90.0, 89.9, 80.0, 60.0, 45.0, 30.0)
    ms, n_inst = [], []
    for th in ths:
        u = np.array([math.cos(math.radians(th)), math.sin(math.radians(th)), 0.0])
        polys = [[(2.0, 6.0, 2.5), (10.0, 6.0, 2.5)], [tuple(C - 4.0 * u), tuple(C + 4.0 * u)]]
        P = rows(polys)
        sid, _ = bed(P, n)
        reg = registry(sid, P)
        n_inst.append(len(reg['instances']['fi']))
        m = _plan_mult(plan(reg, 1e3, quantitative=False))
        ms.append(float(m[0]) if m is not None and len(m) == 1 else math.nan)
    want = [1.0 / math.sin(math.radians(t)) for t in ths]     # 깊은 교차 (d0 = 0) · 각 θ: 닿음 길이 = 2(r_i + r_j)/sin θ
    chk('LEN-O 비스듬한 깊은 교차 — instance 하나씩 · 배율 = 1/sin θ (손으로 잰 닿음 길이 · 1e-9)',
        n_inst == [1] * len(ths) and all(abs(a - b) <= 1e-9 * b for a, b in zip(ms, want)), f'{n_inst} {ms} ↔ {want}')
    chk('LEN-O 경계 연속 — 직교 (90°) 배율 = 1 정확히 · 89.9° = 1 + (0, 2e-6) (뛰지 않는다)',
        ms[0] == 1.0 and 0.0 < ms[1] - 1.0 < 2e-6, f'{ms[:2]}')
    chk('LEN-O 각도에 단조 — θ 가 작아질수록 배율이 엄격히 커진다 (90 · 89.9 · 80 · 60 · 45 · 30°) · 모두 ≥ 1',
        all(ms[i + 1] > ms[i] for i in range(len(ms) - 1)) and min(ms) >= 1.0, f'{ms}')


@case('LEN-G')
def t_len_gate():
    """배율 기록 ↔ 쓰는 값 결합 — 계획의 배율만 바꾸고 행 지문을 다시 만든 변이 (g 는 옛 값) 는 솔브 입구에서 거부 (CG 0).
    구현과 같은 커밋에서 더한 시험 (자기 리뷰 · 증서 ↔ 결과 결합 부류)."""
    P = rows(LP)
    sid, _ = bed(P, LP_N)
    pl = plan(registry(sid, P), 1e3)
    ok_base = _try(lambda: I_of(solve(sid, sig_e(), LP_N, pl), LP_N)) > 0
    bad = []
    for nm, f in (('배율 ×2', 2.0), ('배율 ×0.5 (< 1)', 0.5)):
        pm = dict(pl)
        pm['mult'] = np.asarray(pl['mult'], np.float64) * f
        pm['fp_rows'] = CJ.plan_rows_fp(pm)
        _CG_CALLS[0] = 0
        rej = raises(lambda pm=pm: solve(sid, sig_e(), LP_N, pm))
        if not (rej and _CG_CALLS[0] == 0):
            bad.append(nm)
    chk('LEN-G 배율만 바꾸고 지문을 다시 만든 계획 (×2 · ×0.5) = 솔브 입구 거부 · CG 0 (정상 계획은 풀린다)', ok_base and not bad,
        f'base {ok_base} 통과한 변이 {bad}')


@case('J8')
def t_j8_long():
    P = rows(LP)
    sid, _ = bed(P, LP_N)
    reg = registry(sid, P)
    cen = reg['census']
    nl = int(np.sum(reg['instances']['long']))
    chk('J8 긴 접촉 (L_c > L_par) = 표지 · 집계 칸 그대로 (instance long · census n_long_distinct · L_c 최댓값)',
        nl == 1 and cen.get('n_long_distinct') == 1 and abs(float((cen.get('Lc_um') or {}).get('max', math.nan)) - 6.0) < 1e-12,
        f"{nl} {cen.get('n_long_distinct')} {cen.get('Lc_um')}")
    pq = plan(reg, 1e3)
    chk('J8 옛 동작 제거 — 긴 접촉이 있어도 정량 계획에 거부 사유 없음 (long_contact · 길이 법칙이 그 자리를 맡는다)',
        not pq['rejections'], f"{[x['code'] for x in pq['rejections']]}")
    r = _try(lambda: solve(sid, sig_e(), LP_N, pq), None)
    chk('J8 정량 솔브 진행 · 기록 (긴 접촉 수 1 영수증 · solved)',
        r is not None and r['sigma_eff'] > 0 and r['cjunc'].get('n_long') == 1 and r['cjunc'].get('solved') is True)


@case('FOOT')
def t_footprint():
    """절단 발자국 = 접촉 run 전체 — 긴 접촉 위의 A|B 융합 면이 하나라도 남으면 (미등록 법칙 fused) 접합 간선을 병렬로 우회한다."""
    P = rows(LP)
    sid, _ = bed(P, LP_N)
    reg = registry(sid, P)
    ft = reg['faces']
    pos = reg['positions']
    vv = (ft['pa'] >= 0) & (ft['pb'] >= 0)
    fa = np.where(vv, pos['fid'][np.maximum(ft['pa'], 0)], -1)
    fb = np.where(vv, pos['fid'][np.maximum(ft['pb'], 0)], -1)
    pair = vv & (np.minimum(fa, fb) == 10) & (np.maximum(fa, fb) == 20)
    n_site = int(np.sum(pair & (ft['kind'] == CJ.K_CUT_SITE)))
    n_unreg = int(np.sum(pair & (ft['kind'] == CJ.K_UNREG)))
    chk('FOOT 원장 — A|B 접촉 면 6 개 (z 2..7 · 손으로 센 run) 전부 자리 절단 · 미등록 0', n_site == 6 and n_unreg == 0,
        f'site {n_site} unreg {n_unreg}')
    rj = 1e3
    rt = _try(lambda: solve(sid, sig_e(), LP_N, plan(reg, rj, unreg_law='fused', quantitative=False)), None)
    ok_t = (rt is not None and rt['cjunc']['tombstones']['cut_site'] == 6 and rt['cjunc']['n_unreg_fused'] == 0
            and not np.any(rt['_cjunc']['sys']['CAT'] == 2))           # 간선 원장에 vv_unreg_fused (2) 없음
    chk('FOOT 미등록 법칙 fused 에서도 run 위 융합 i|j 면 0 — 면 tombstone 6 · 미등록 융합 0 · 간선 원장에 융합 VV 간선 없음', ok_t)
    I = _try(lambda: I_of(solve(sid, sig_e(), LP_N, plan(reg, rj, unreg_law='fused')), LP_N))
    chk('FOOT fused · 정량 σ = 해석 회로 (우회 없음 · 1e-12)', rel(I, LP_I(rj)) < 1e-12, f'{I} ↔ {LP_I(rj)}')


@case('KINK')
def t_kink():
    P = rows(KU)
    sid, _ = bed(P, KU_N)
    seq = seq_cells(KU[0])
    nn = len(seq)
    ix = {c: seq.index(c) for c in seq}
    lo_ = _try(lambda: registry(sid, P, s_min_um=KU_S - 0.5), None)       # s ≥ s_min → 진짜 접힘 (접합)
    hi_ = _try(lambda: registry(sid, P, s_min_um=KU_S + 0.5), None)       # s < s_min → 같은 가닥의 연속
    s_rec = (((lo_ or {}).get('census') or {}).get('self_s_um') or {}).get('min')
    chk('KINK s = 두 최근접점 사이 경로 호 길이 = 3 + 1 + √(0.2² + 3²) (손으로 잰 값 · 1e-9)',
        s_rec is not None and abs(float(s_rec) - KU_S) < 1e-9, f'{s_rec} ↔ {KU_S}')
    ok = lo_ is not None and hi_ is not None
    nlo = int(np.sum(lo_['instances']['self'])) if ok else -1
    nhi = int(np.sum(hi_['instances']['self'])) if ok else -1
    clo = lo_['census'] if ok else {}
    chi = hi_['census'] if ok else {}
    chk('KINK s ≥ s_min = 자기 접합 하나 · s < s_min = 접합 없음 (후보 1 · 거른 수 · 남은 수 기록)',
        nlo == 1 and nhi == 0 and clo.get('n_self_candidates') == 1 and clo.get('n_self_kept') == 1
        and clo.get('n_self_filtered') == 0 and chi.get('n_self_kept') == 0 and chi.get('n_self_filtered') == 1,
        f'{nlo} {nhi} · {[clo.get(k) for k in ("n_self_candidates", "n_self_kept", "n_self_filtered")]} · '
        f'{[chi.get(k) for k in ("n_self_candidates", "n_self_kept", "n_self_filtered")]}')
    rj = 1e3
    E_f = _chain_edges(nn) + [(ix[(1, 1, k)], ix[(2, 1, k)], G_AX) for k in (1, 2, 3)]
    w_f = ref_I(nn, E_f, [(0, G_PL)], [(nn - 1, G_PL)])
    I_leg = I_of(solve_legacy(sid, sig_e(), KU_N), KU_N)
    Ih = _try(lambda: I_of(solve(sid, sig_e(), KU_N, plan(hi_, rj)), KU_N))
    chk('KINK s < s_min — 접합 · 절단 없음 = 옛 복셀 융합 그대로 (σ = 옛 경로 = 사다리 기준 1e-12)',
        rel(Ih, I_leg) < 1e-12 and rel(Ih, w_f) < 1e-12, f'{Ih} ↔ 옛 {I_leg} · 사다리 {w_f}')
    E_j = _chain_edges(nn) + [(ix[(1, 1, 1)], ix[(2, 1, 1)], 1.5 * 1e4 / rj)]    # 자기 면 셋 절단 · 포트 = B 의 대표 항목
    w_j = ref_I(nn, E_j, [(0, G_PL)], [(nn - 1, G_PL)])
    Il = _try(lambda: I_of(solve(sid, sig_e(), KU_N, plan(lo_, rj)), KU_N))
    chk('KINK s ≥ s_min — 자기 면 셋 절단 + R_j 간선 × 같은 법칙 배율 (닿음 L_c 3.0 → 1.5 · 사다리 기준 1e-12)',
        rel(Il, w_j) < 1e-12, f'{Il} ↔ {w_j}')
    rn = _try(lambda: registry(sid, P, s_min_um=None), None)
    pq = _try(lambda: plan(rn, rj), None) if rn is not None else None
    chk('KINK s_min 없음 + 정량 = 구조화 거부 (계획 거부 사유 self_s_min_missing · 솔브 입구 거부 · CG 전)',
        pq is not None and any(x.get('code') == 'self_s_min_missing' for x in pq['rejections'])
        and raises(lambda: solve(sid, sig_e(), KU_N, pq)))
    pt = _try(lambda: plan(rn, rj, quantitative=False), None) if rn is not None else None
    chk('KINK s_min 없음 + 시험 모드 = 진행 · 거르기 안 함 표지 (자기 접합 그대로 · self_filter = off_s_min_missing)',
        pt is not None and not pt['rejections'] and rn['census'].get('self_filter') == 'off_s_min_missing'
        and int(np.sum(rn['instances']['self'])) == 1)
    PW = rows(KW)
    sidw, _ = bed(PW, KU_N)
    rw = _try(lambda: registry(sidw, PW, s_min_um=1.0), None)
    lcw = rw['instances']['Lc'][rw['instances']['self']] if rw is not None else []
    mw = _plan_mult(plan(rw, rj)) if rw is not None else None
    chk('KINK 자기 접합 L_c = 닿음 규칙 (셀 셈 아님) — 면으로 닿는 셀 셋 · 중심선 1.2 > r_f + r_f → L_c 0 · 배율 1',
        len(lcw) == 1 and float(lcw[0]) == 0.0 and mw is not None and list(mw) == [1.0], f'{list(lcw)} {mw}')


#  KR 꺾임 재방문: 위로 (1,1,0..3) → 오른쪽 (2,1,3) → 위 (2,1,4) → 왼쪽 (1,1,4) → 아래로 셀 (1,1,3) 에 **다시** 들어옴 → 왼쪽 (0,1,3) →
#     위로 (0,1,3..7) 위 판.  자기 후보 둘 = 재방문 (1,1,3) (s = 1.0 + 1.3 + 1.2 + 0.9 = 4.4) · 면 (1,1,4)|(0,1,4) (s ≲ 2.6).
KR_N = (4, 3, 8)
KR = [[(1.5, 1.5, 0.5), (1.5, 1.5, 3.2), (2.5, 1.5, 3.2), (2.5, 1.5, 4.5), (1.3, 1.5, 4.5), (1.3, 1.5, 3.6), (0.5, 1.5, 3.6),
       (0.5, 1.5, 7.5)]]


@case('KINK-R')
def t_kink_revisit():
    """s < s_min 재방문 = 옛 복셀 한 셀 (두 위치를 한 노드로) — 구현과 같은 커밋에서 더한 시험 (합침 경로의 판별력 · 변이 = 합침 끔)."""
    P = rows(KR)
    sid, _ = bed(P, KR_N)
    I_leg = I_of(solve_legacy(sid, sig_e(), KR_N), KR_N)
    rc = _try(lambda: registry(sid, P, s_min_um=10.0), None)            # 둘 다 s < s_min → 같은 가닥의 연속
    cc = (rc or {}).get('census') or {}
    chk('KINK-R s < s_min — 후보 2 · 거른 수 2 · 합친 재방문 1 · 융합 자기 면 1 · 접합 0',
        rc is not None and cc.get('n_self_candidates') == 2 and cc.get('n_self_filtered') == 2
        and cc.get('n_self_merged_revisits') == 1 and cc.get('n_self_fused_faces') == 1 and len(rc['instances']['fi']) == 0,
        f'{cc}')
    rj = 1e3
    r = _try(lambda: solve(sid, sig_e(), KR_N, plan(rc, rj)), None)
    chk('KINK-R s < s_min — σ = 옛 경로 (재방문 = 한 노드 · 면 = 융합 · 1e-12) · 솔브 기록 합침 1',
        r is not None and rel(I_of(r, KR_N), I_leg) < 1e-12 and r['cjunc'].get('n_self_merged_revisits') == 1,
        f"{None if r is None else I_of(r, KR_N)} ↔ {I_leg}")
    base_cls = CJ.CjuncAssembler

    class NoMerge(base_cls):                                # 변이 — 재방문 합침을 끈다 (두 위치가 따로 남는다)
        def build(self, *a, **k):
            self.reg = dict(self.reg)
            self.reg['self_merge'] = np.zeros((0, 2), np.int64)
            return super().build(*a, **k)
    CJ.CjuncAssembler = NoMerge
    try:
        Im = _try(lambda: I_of(solve(sid, sig_e(), KR_N, plan(rc, rj)), KR_N))
    finally:
        CJ.CjuncAssembler = base_cls
    chk('KINK-R 변이 (재방문 합침 끔) → 옛 경로에서 벗어난다', not rel(Im, I_leg) < 1e-12, f'{Im} ↔ {I_leg}')
    rj_ = _try(lambda: registry(sid, P, s_min_um=0.5), None)            # 둘 다 s ≥ s_min → 자기 접합 둘
    cj_ = (rj_ or {}).get('census') or {}
    chk('KINK-R s ≥ s_min — 자기 접합 둘 · 합친 재방문 0 · 융합 자기 면 0',
        rj_ is not None and int(np.sum(rj_['instances']['self'])) == 2 and cj_.get('n_self_merged_revisits') == 0
        and cj_.get('n_self_fused_faces') == 0, f'{cj_}')


@case('INV')
def t_invariance():
    rj = 1e3

    def run(polys, n, smin, fids=None, shift=(0.0, 0.0, 0.0), rev=False):
        pl_ = [v[::-1] for v in polys] if rev else polys
        P0 = rows(pl_, fids=fids)
        P = (P0[0] + np.asarray(shift, np.float64), P0[1], P0[2], P0[3])
        sid, _ = bed(P, n, lo=shift)
        reg = registry(sid, P, lo=shift, s_min_um=smin)
        pq = plan(reg, rj)
        return sid, len(reg['instances']['fi']), _plan_mult(pq), I_of(solve(sid, sig_e(), n, pq), n)

    for nm, polys, n, smin, fids in (('LP', LP, LP_N, S_MIN, [77, 33]), ('KU', KU, KU_N, KU_S - 0.5, [55])):
        b = _try(lambda: run(polys, n, smin), None)
        outs = {'점 역순': _try(lambda: run(polys, n, smin, rev=True), None),
                '원점 이동 (8, −4, 16)': _try(lambda: run(polys, n, smin, shift=(8.0, -4.0, 16.0)), None),
                '섬유 번호 바꿈': _try(lambda: run(polys, n, smin, fids=fids), None)}
        for what, o in outs.items():
            ok = (b is not None and o is not None and b[2] is not None and o[2] is not None and o[0].tobytes() == b[0].tobytes()
                  and o[1] == b[1] and len(o[2]) == len(b[2])
                  and np.allclose(np.sort(o[2]), np.sort(b[2]), rtol=1e-12, atol=0.0) and rel(o[3], b[3]) < 1e-12)
            chk(f'INV {nm} {what} → sid · instance 수 · 배율 · σ 같음 (1e-12)', ok,
                f'{None if b is None else (b[1], b[2], b[3])} ↔ {None if o is None else (o[1], o[2], o[3])}')


@case('SMIN')
def t_smin():
    import inspect
    try:
        prm = inspect.signature(CJ.cjunc_registry).parameters.get('s_min_um')
    except (TypeError, ValueError, AttributeError):
        prm = None
    chk('SMIN s_min_um = 필수 키워드 · 기본값 없음 (r_f · tol_ff · L_par · r_port 와 같은 꼴)',
        prm is not None and prm.kind == prm.KEYWORD_ONLY and prm.default is prm.empty, f'{prm}')
    P = rows(KU)
    sid, _ = bed(P, KU_N)
    k = dict(r_f_um=RF, tol_ff_um=TOL, L_par_um=LPAR, r_port_um=RPORT, gap_tol=2.0)
    chk('SMIN 빠뜨림 = 거부 (TypeError · 조용한 기본값 없음)',
        prm is not None and raises(lambda: CJ.cjunc_registry(sid, (0.0, 0.0, 0.0), H, *P, **k), TypeError))
    bad = (float('nan'), -1.0, math.inf, True, 'x')
    chk('SMIN 비유한 · 음수 · bool · 문자 = 거부 (조립 전)',
        prm is not None and all(raises(lambda v=v: CJ.cjunc_registry(sid, (0.0, 0.0, 0.0), H, *P, s_min_um=v, **k)) for v in bad))


@case('REC')
def t_record():
    P = rows(LP)
    sid, _ = bed(P, LP_N)
    reg = registry(sid, P)
    cen, thr, rules = reg['census'], reg['thresholds'], reg['rules']
    lc = cen.get('Lc_um') or {}
    lm = cen.get('len_mult') or {}
    chk('REC 원장 — 법칙 이름 len_scaled_v0 · s_min 문턱 · L_c 분포 (최댓값 · 분위 p90 · p99 · 중앙값) · 배율 합 (3)',
        rules.get('len_law') == 'len_scaled_v0' and thr.get('s_min_um') == S_MIN
        and all(x in lc for x in ('max', 'p90', 'p99', 'median'))
        and abs(float(lm.get('sum', math.nan)) - 3.0) < 1e-12 and abs(float(lm.get('max', math.nan)) - 3.0) < 1e-12,
        f"{rules.get('len_law')} {thr.get('s_min_um')} {lc} {lm}")
    pr = plan(reg, 1e3)['record']
    cn = pr.get('counts', {})
    chk('REC 계획 기록 — 법칙 이름 · 긴 접촉 수 1 · 간선 배율 합 3 · 한정어 = 길이 법칙 (J8 정량 거부 문장 없음)',
        pr.get('len_law') == 'len_scaled_v0' and cn.get('n_long') == 1
        and abs(float(cn.get('len_mult_sum_edge', math.nan)) - 3.0) < 1e-12
        and any('L_c/L_par' in q for q in pr.get('qualifiers', ())) and not any('정량 거부 (J8)' in q for q in pr.get('qualifiers', ())),
        f"{pr.get('len_law')} {cn}")
    PK = rows(KU)
    sidk, _ = bed(PK, KU_N)
    r1 = _try(lambda: registry(sidk, PK, s_min_um=KU_S - 0.5), None)
    r2 = _try(lambda: registry(sidk, PK, s_min_um=KU_S + 0.5), None)
    c1 = (r1 or {}).get('census') or {}
    chk('REC 자기 접합 기록 — 후보 · 남은 수 · 거른 수 · s 분포 (최솟값 · 중앙값 · 최댓값) · 거르기 적용 표지',
        c1.get('n_self_candidates') == 1 and c1.get('n_self_kept') == 1 and c1.get('n_self_filtered') == 0
        and all(x in (c1.get('self_s_um') or {}) for x in ('min', 'median', 'max')) and c1.get('self_filter') == 'applied',
        f'{c1}')
    r3 = _try(lambda: registry(sidk, PK, s_min_um=KU_S - 1.0), None)       # r1 과 같은 분류 (둘 다 접합) — s_min 숫자만 다르다
    chk('REC 지문에 s_min 포함 — 분류가 같고 s_min 숫자만 다른 두 원장의 원장 지문이 다르다 (instance 표는 같다)',
        r1 is not None and r3 is not None and r1['thresholds'].get('s_min_um') != r3['thresholds'].get('s_min_um')
        and len(r1['instances']['fi']) == len(r3['instances']['fi']) == 1 and r1['fp']['registry'] != r3['fp']['registry'])
    chk('REC 거른 원장 (s < s_min) — 거른 수 1 · 남은 수 0', r2 is not None and r2['census'].get('n_self_filtered') == 1
        and r2['census'].get('n_self_kept') == 0)


@case('J11')
def t_j11_short():
    n = (5, 5, 2)
    polys = [[(0.5, 2.5, 0.5), (4.5, 2.5, 0.5)], [(2.5, 0.5, 1.5), (2.5, 4.5, 1.5)]]   # 아래 층 · 위 층 십자 (거리 1.0)
    P = rows(polys)
    sid, _ = bed(P, n)
    reg = registry(sid, P)
    r0 = solve(sid, sig_e(), n, plan(reg, 0.0, allow_rj_limits=True))
    chk('J11 축약 무리가 두 판에 다 닿음 = 단락 상태 (유한 σ 로 위장 안 함 · 게시 안 함)',
        r0.get('reason') == 'cjunc_electrode_short' and r0['sigma_eff'] == 0.0, f"{r0.get('reason')}")
    r1 = solve(sid, sig_e(), n, plan(reg, 1e3))
    chk('J11 R_j > 0 = 정상 σ (단락 아님)', r1['sigma_eff'] > 0 and not r1.get('reason'))


@case('C6')
def t_c6_energy():
    P = rows(F6)
    sid, _ = bed(P, F6_N)
    reg = registry(sid, P)
    rj = 3.0e3
    r = solve(sid, sig_e(), F6_N, plan(reg, rj))
    cj = r['cjunc']
    I = I_of(r, F6_N)
    sh = cj['dissipation_share']
    chk('C6 에너지 항등식 Σ P (면 + 접합 + 판) = I·ΔV (코드 단위 · 1e-10)', rel(cj['P_total_code'], I) < 1e-10,
        f"{cj['P_total_code']} ↔ {I}")
    d = 1e-4
    Ip = I_of(solve(sid, sig_e(), F6_N, plan(reg, rj * (1 + d))), F6_N)
    Im = I_of(solve(sid, sig_e(), F6_N, plan(reg, rj * (1 - d))), F6_N)
    fd = -(math.log(Ip) - math.log(Im)) / (math.log(1 + d) - math.log(1 - d))
    chk('C6 접합 소산 몫 = −∂lnσ/∂lnR_j (중심 FD · 1e-6)', abs(sh['vv_junction'] - fd) < 1e-6, f"{sh['vv_junction']} ↔ {fd}")
    chk('C6 소산 몫 합 = 1', abs(sum(v for k, v in sh.items()) - 1.0) < 1e-12, f'{sh}')


@case('C8')
def t_c8_guards():
    P = rows(F1)
    sid, pid = bed(P, F1_N)
    reg = registry(sid, P)
    pl = plan(reg, 1e3)
    _CG_CALLS[0] = 0
    g = []
    g.append(('r1 표 동시', raises(lambda: solve(sid, sig_e(), F1_N, pl, rint={(3, 3): 1e-3}, pid=pid))))
    g.append(('주기', raises(lambda: solve(sid, sig_e(), F1_N, pl, periodic_xy=True))))
    g.append(('return_field (장 진단은 원장을 안 읽는다)', raises(lambda: solve(sid, sig_e(), F1_N, pl, return_field=True))))
    g.append(('솔버 vox ×2', raises(lambda: solve(sid, sig_e(), F1_N, pl, vox=2.0))))
    sid2 = sid.copy(); sid2[0, 0, 0] = 1
    g.append(('다른 sid', raises(lambda: solve(sid2, sig_e(), F1_N, pl))))
    pt = dict(pl); pt['g_code'] = pl['g_code'] * 2.0
    g.append(('계획 행 변조 (지문)', raises(lambda: solve(sid, sig_e(), F1_N, pt))))
    pt2 = dict(pl); pt2['g_code'] = np.full_like(pl['g_code'], np.nan)
    pt2['fp_rows'] = CJ.plan_rows_fp(pt2)
    g.append(('계획 g NaN (지문 다시 만든 변이 · Q7 불변량)', raises(lambda: solve(sid, sig_e(), F1_N, pt2))))
    rt = dict(reg); rt['instances'] = dict(reg['instances'])
    rt['instances']['port_i'] = reg['instances']['port_j'].copy()           # 포트를 다른 위치로 (값이 실제로 바뀐다)
    g.append(('원장 변조 (지문)', bool(np.any(rt['instances']['port_i'] != reg['instances']['port_i']))
              and raises(lambda: plan(rt, 1e3))))
    g.append(('VGCF 절연 채널 (이온 표)', raises(lambda: solve(sid, S3.ionic_sigma_table(0.3e-3, 3e-3), F1_N, pl))))
    cg_before = _CG_CALLS[0]
    Pn = (P[0].copy(), P[1], P[2], P[3]); Pn[0][3, 1] = np.nan
    g.append(('NaN 좌표', raises(lambda: registry(sid, Pn))))
    Pl = (P[0], P[1], P[2][:-1], P[3])
    g.append(('길이 불일치 (fid 한 줄 모자람)', raises(lambda: registry(sid, Pl))))
    g.append(('kind 없음 (연속 중심선 아님)', raises(lambda: quiet(CJ.cjunc_registry, sid, (0., 0., 0.), H, P[0], P[1], P[2], None,
                                                              **reg_kw(dict(r_f_um=RF, tol_ff_um=TOL, L_par_um=LPAR,
                                                                            r_port_um=RPORT, s_min_um=S_MIN))))))
    Fs = P[2].copy(); i0 = np.flatnonzero(Fs == 10)[2]; Fs[i0] = 20
    Ps = (P[0], P[1], Fs, P[3])
    rs = registry(sid, Ps)
    g.append(('떨어진 같은 fid = 정량 거부', any(x['code'] == 'fid_noncontiguous' for x in rs['rejections'])))
    pts_only = rows(F1, kind=0)
    sid_pt, _ = bed(pts_only, F1_N)
    rpt = registry(sid_pt, pts_only)
    g.append(('점 스탬프 VGCF (kind 0) = 정량 거부', any(x['code'] in ('vgcf_nonpath_fid', 'vgcf_orphan_cells')
                                                         for x in rpt['rejections'])))
    for nm, okk in g:
        chk(f'C8 거부 — {nm}', okk)
    chk('C8 거부 경로에서 CG 호출 0 (솔브 관문 아홉 · 조립 전)', cg_before == 0, f'{cg_before}')
    chk('C8 계획 · 기록 = 기구 표지 (mechanism_only · 모형 내부 R_j · 반셀 없음 · SDCP–VGCF 접촉 저항 0 가정)',
        pl['record']['status'].startswith('mechanism_only') and pl['record']['rj_reference_plane'] == 'model_internal_port_centre'
        and pl['record']['half_cell_in_edge'] is False
        and any('SDCP–VGCF 접촉 저항 0' in q for q in pl['record']['qualifiers']))


def _ptfe_rows(polys, fid0=900):
    return rows(polys, phase=4, fid0=fid0)


@case('P-junc')
def t_pjunc():
    P = rows(F1)
    #  PTFE 피브릴이 접점 (1.5,1.5,3.5) 근처를 지난다 — 중심선 거리 = r_P + r_f + tol_P 정확히 (경계 = 포함).
    #  경계값이 이진 정확 (0.25 + 0.5 + 0.25 = 1.0 · 좌표 2.5 − 1.5) 이어야 경계 시험이 반올림이 아닌 규칙을 본다.
    rP, tP = 0.25, 0.25
    dist = rP + RF + tP
    pt = _ptfe_rows([[(0.5, 1.5 + dist, 3.5), (5.5, 1.5 + dist, 3.5)]])
    allr = cat_rows(P, pt)
    sid, _ = bed(allr, F1_N, stamp=allr[1] != 4)                    # face_alpha 침대 = PTFE 셀 없음 (off 격자)
    reg = registry(sid, allr, tol_P_um=tP, r_ptfe_um=rP)
    cov = reg['instances']['ptfe_cov']
    chk('P-1 덮임 경계 = 정확히 tol_P 포함 (≤)', len(cov) == 1 and bool(cov[0]), f'{cov}')
    I0 = I_of(solve(sid, sig_e(), F1_N, plan(reg, 1e3, ptfe_stamp='face_alpha', ptfe_jlaw='P0')), F1_N)
    r1 = solve(sid, sig_e(), F1_N, plan(reg, 1e3, ptfe_stamp='face_alpha', ptfe_jlaw='P1'))
    chk('P-1 P0 = 영향 없음 (해석 사슬) · P1 = 덮인 instance 절단 (관통 없음)',
        rel(I0, F1_I(1e3)) < 1e-12 and r1['sigma_eff'] == 0.0 and r1['cjunc']['n_cut_p1'] == 1, f"{I0} {r1.get('reason')}")
    pt_far = _ptfe_rows([[(0.5, 1.5 + dist + 1e-9, 3.5), (5.5, 1.5 + dist + 1e-9, 3.5)]])
    allf = cat_rows(P, pt_far)
    regf = registry(sid, allf, tol_P_um=tP, r_ptfe_um=rP)
    chk('P-1 경계 밖 (+1e-9 µm) = 덮이지 않음', not bool(regf['instances']['ptfe_cov'][0]))
    chk('P-1 centerline + P1 = 거부 (centerline 이 이미 VGCF 셀을 sid 7 로 자른다)',
        raises(lambda: plan(reg, 1e3, ptfe_stamp='centerline', ptfe_jlaw='P1')))
    chk('P-1 off + P1 = 거부 (face_alpha 에서만)', raises(lambda: plan(reg, 1e3, ptfe_stamp='off', ptfe_jlaw='P1')))
    sd = rows([[(1.5, 2.5, 3.5)]], phase=5, kind=0, fid0=700)            # SDCP 점이 접점에 근접 (면 이웃 빈 셀)
    alls = cat_rows(P, pt, sd)
    sids, _ = bed(alls, F1_N, stamp=alls[1] != 4)
    regs = registry(sids, alls, tol_P_um=tP, r_ptfe_um=rP, tol_sj_um=0.5, r_sdcp_um=0.5)
    pp = plan(regs, 1e3, ptfe_stamp='face_alpha', ptfe_jlaw='P1', sdcp_mod={'c': 1.0})
    chk('P-2 PTFE 덮임 ∧ SDCP 근접 · (P1, c = 1) → 절단 먼저 (축약 아님 · N18)',
        int(pp['mode'][0]) == CJ.MODE_CUT_P1 and bool(regs['instances']['a_sdcp'][0]), f"{pp['mode']}")


# ═════════════════════════ FA+CJ — S1 face_alpha × S2 cjunc 한 솔브 (★ Z3 10-20 = 받음 · 옛 B6 임시 거부 뺌) ═════════════════════════
@case('FA+CJ')
def t_fa_cj_both_refused():
    """한 솔브에 S1 면 개구율 (face_alpha 계획) 과 S2 탄소 접합 (cjunc 계획) 을 **같이** 준다 — ★ Z3 (10-20) 설계 조합 규칙 (설계 §3 · §4 ·
    등록 R §10 꼴): α 를 `couple()` 에서 먼저 융합 면에 곱하고 (α = 0 면 = `_keep` 제거) · 그 다음 접합 훅이 발자국 면을 끊고 접합 간선을
    넣는다 · PTFE 가 접합 끝을 덮을 때는 P0/P1 법칙만 (α 를 접합 간선에 곱하지 않는다).  옛 판 (B6 통합) 은 이 조합을 조립 전에 임시로
    거부했다 (그 거부를 뺐다 — 함수 이름은 회귀 기록용으로 둔다).  양성 대조 = 같은 침대 · 같은 두 계획이 각각 홀로도 받아들여진다."""
    import ptfe_face_alpha as FA
    P = rows(F1)
    sd = rows([[(1.5, 2.5, 3.5)]], phase=5, kind=0, fid0=700)          # SDCP 셀 (1,2,3) — 교차 VGCF 셀 (1,1,3) 과 y 면 (y = 2) 공유
    pt = _ptfe_rows([[(1.5, 0.5, 3.5), (1.5, 2.5, 3.5)]])              # PTFE 가 그 VGCF|SDCP 면을 가로지른다 (α = 60/64 · 면 하나)
    allr = cat_rows(P, sd, pt)
    sid, pid = bed(allr, F1_N, stamp=allr[1] != 4)                     # face_alpha 침대 = PTFE 셀 없음 (off 격자)
    sig = sig_e()
    cj = plan(registry(sid, allr), 1e3, ptfe_stamp='face_alpha', ptfe_jlaw='P0')
    m4 = allr[1] == 4
    fa = FA.build_plan(sid, sig, FA.build_capsules(allr[0][m4], allr[2][m4], allr[3][m4]), lo=(0.0, 0.0, 0.0), vox=H,
                       channel='electronic', pid=pid)
    r_fa = solve(sid, sig, F1_N, None, face_alpha=fa, pid=pid)
    r_cj = solve(sid, sig, F1_N, cj)
    chk('FA+CJ 양성 대조 — face_alpha 홀로 = 받아들임 · 계획 행을 실제로 씀 (VGCF|SDCP 면 α 60/64)',
        r_fa['sigma_eff'] > 0.0 and r_fa['face_alpha']['n_rows_used'] == 1 and 'cjunc' not in r_fa,
        f"{r_fa.get('reason')} {r_fa.get('face_alpha')}")
    chk('FA+CJ 양성 대조 — cjunc 홀로 (ptfe_stamp face_alpha 선언) = 받아들임', r_cj['sigma_eff'] > 0.0
        and r_cj['cjunc']['solved'] is True and 'face_alpha' not in r_cj, f"{r_cj.get('reason')}")
    _CG_CALLS[0] = 0
    err, res = None, None
    try:
        res = solve(sid, sig, F1_N, cj, face_alpha=fa, pid=pid)
    except (ValueError, TypeError) as e:
        err = e
    res = res or {}
    _rj = (res.get('cjunc') or {})
    _keys = ('n_junction_edges', 'n_contracted', 'n_extra_dofs', 'tombstones')
    chk('FA+CJ 동시 (face_alpha + cjunc) = ★ Z3 받음 · 두 기록 다 · 계획 행 씀 · 조합 σ ≤ 접합만 σ (α ≤ 1 · Rayleigh) · '
        '접합 기록 (간선 · 축약 · 추가 dof · 끊은 면) = 접합만과 같음 (α 가 접합 간선에 안 걸림)',
        err is None and _CG_CALLS[0] >= 1 and (res.get('face_alpha') or {}).get('n_rows_used') == 1 and _rj.get('solved') is True
        and 0.0 < res.get('sigma_eff', 0.0) <= r_cj['sigma_eff'] * (1.0 + 1e-12)
        and all(_rj.get(k) == r_cj['cjunc'].get(k) for k in _keys),
        f'예외 {type(err).__name__ if err else None}: {str(err)[:120]} · CG {_CG_CALLS[0]} · '
        f"σ {res.get('sigma_eff')} ↔ 접합만 {r_cj['sigma_eff']} · {[(k, _rj.get(k), r_cj['cjunc'].get(k)) for k in _keys]}")


# ═════════════════════════ S3 ═════════════════════════
def _s3_fixture(with_sdcp=True, sdcp_pos=(1.5, 2.5, 3.5)):
    P = rows(F1)
    parts = [P]
    if with_sdcp:
        parts.append(rows([[sdcp_pos]], phase=5, kind=0, fid0=700))
    allr = cat_rows(*parts)
    sid, _ = bed(allr, F1_N)                                       # SDCP 점 스탬프 (h 1 에서 구 스탬프는 d/vox ≥ 2 게이트)
    reg = registry(sid, allr, tol_sj_um=0.5, r_sdcp_um=0.5)
    return sid, reg, allr


def _rows_sig(p):
    return (p['mode'].tobytes(), p['g_code'].tobytes(), p['rj_eff'].tobytes())


@case('S3')
def t_s3():
    sid, reg, allr = _s3_fixture()
    chk('S3 근접 판정 (SDCP 1 차 입자 표면 ↔ 접점 ≤ tol_sj)', bool(reg['instances']['a_sdcp'][0]))
    p_s2 = plan(reg, 1e3)
    p_c0 = plan(reg, 1e3, sdcp_mod={'c': 0.0})
    r_s2 = solve(sid, sig_e(), F1_N, p_s2)
    r_c0 = solve(sid, sig_e(), F1_N, p_c0)
    chk('S3-1 c = 0 → 계획 행 · σ 가 S2 와 비트 같음', _rows_sig(p_s2) == _rows_sig(p_c0)
        and np.float64(r_s2['sigma_eff']).tobytes() == np.float64(r_c0['sigma_eff']).tobytes())
    sid_n, reg_n, _ = _s3_fixture(with_sdcp=False)
    s2n = plan(reg_n, 1e3)
    same = True
    for c in (0.0, 0.5, 1.0):
        pc = plan(reg_n, 1e3, sdcp_mod={'c': c}, quantitative=(c in (0.0, 1.0)))
        same &= _rows_sig(pc) == _rows_sig(s2n)
        rc = solve(sid_n, sig_e(), F1_N, pc)
        same &= np.float64(rc['sigma_eff']).tobytes() == np.float64(solve(sid_n, sig_e(), F1_N, s2n)['sigma_eff']).tobytes()
    chk('S3-2 SBE (SDCP 없음) — 모든 c 에서 계획 행 · σ 비트 같음 (셀 · 원장 단위 no-op)', same)
    Is = [I_of(solve(sid, sig_e(), F1_N, plan(reg, 1e3, sdcp_mod={'c': c}, quantitative=False)), F1_N)
          for c in (0.0, 0.5, 0.9, 0.99)]
    TAU = 1e-12                                                    # 봉인 (직접 풀이 · 같은 그래프 = Rayleigh 정확)
    chk(f'S3-3 c 단조 — σ(c) 비감소 (c 격자 0 · 0.5 · 0.9 · 0.99 · 허용폭 {TAU} 봉인)',
        all(Is[i + 1] >= Is[i] * (1 - TAU) for i in range(len(Is) - 1)) and Is[-1] > Is[0], f'{Is}')
    want_c = [F1_I(1e3 * (1 - c)) for c in (0.0, 0.5, 0.9, 0.99)]
    chk('S3-3 R_j′ = R_j,0·(1 − c·a_j) — 해석 사슬 (1e-12)', max(rel(a, b) for a, b in zip(Is, want_c)) < 1e-12, f'{Is} {want_c}')
    p1 = plan(reg, 1e3, sdcp_mod={'c': 1.0})
    r1 = solve(sid, sig_e(), F1_N, p1)
    chk('S3-4 c = 1 = 근접 instance 축약 (축약 경로 · 정량 허용 예외 · 축약 수 기록 · 옛 융합과 같음 1e-12)',
        int(p1['mode'][0]) == CJ.MODE_CONTRACT and r1['cjunc']['n_contracted'] == 1
        and rel(I_of(r1, F1_N), F1_I(0)) < 1e-12, f"{p1['mode']} {r1['cjunc'].get('n_contracted')}")
    chk('S3 정량 모드 c ∈ {0, 1} 만 (0.5 = 거부)', raises(lambda: plan(reg, 1e3, sdcp_mod={'c': 0.5})))
    chk('S3 c 범위 밖 · NaN = 거부', raises(lambda: plan(reg, 1e3, sdcp_mod={'c': 1.5}, quantitative=False))
        and raises(lambda: plan(reg, 1e3, sdcp_mod={'c': float('nan')}, quantitative=False)))
    P, PH, F, K = allr
    m5 = np.flatnonzero(PH == 5)
    order = np.arange(len(P)); order[m5] = m5[::-1]
    regp = registry(sid, (P[order], PH[order], F[order], K[order]), tol_sj_um=0.5, r_sdcp_um=0.5)
    chk('S3-5 SDCP 점 순열 불변 (근접 · 계획 행 비트 같음)', _rows_sig(plan(regp, 1e3, sdcp_mod={'c': 1.0})) == _rows_sig(p1))
    d_edge = 0.5 + 0.5                                             # 접점 (1.5,1.5,3.5) ↔ SDCP 중심 = r_s + tol_sj 정확히
    sid_e, reg_e, _ = _s3_fixture(sdcp_pos=(1.5, 1.5 + d_edge, 3.5))
    sid_o, reg_o, _ = _s3_fixture(sdcp_pos=(1.5, 1.5 + d_edge + 1e-9, 3.5))
    chk('S3-6 근접 문턱 경계 = 포함 (≤) · +1e-9 µm = 밖', bool(reg_e['instances']['a_sdcp'][0])
        and not bool(reg_o['instances']['a_sdcp'][0]))
    #  S3-7 원고 펠릿 LPSCl:SDCP 9:1 (탄소 없음) — v0 의 S3 은 구성상 no-op (판별력 없음 · 그렇게 기록)
    rng = np.random.default_rng(3)
    n = (12, 12, 12); box = np.array(n, float) * 0.5
    sd = rng.uniform(0.2, box - 0.2, (60, 3))
    rp = (sd, np.full(len(sd), 5), np.arange(len(sd)) + 1, np.zeros(len(sd), int))
    sidp, _ = S3.rasterize(*NO_AM, rp[0], rp[1], (0., 0., 0.), tuple(box), 0.5, se_pts=rng.uniform(0, box, (20000, 3)),
                           sdcp_sphere_d_um=1.0, add_fid=rp[2], add_kind=rp[3])
    regp = quiet(CJ.cjunc_registry, sidp, (0., 0., 0.), 0.5, *rp,
                 **reg_kw(dict(r_f_um=0.25, tol_ff_um=0.05, L_par_um=1.0, r_port_um=1.0, tol_sj_um=0.05, r_sdcp_um=0.5,
                               s_min_um=1.5)))
    pc0 = plan(regp, 1e3, sdcp_mod={'c': 0.0}); pc1 = plan(regp, 1e3, sdcp_mod={'c': 1.0})
    rc0 = solve(sidp, sig_e(), n, pc0, vox=0.5); rc1 = solve(sidp, sig_e(), n, pc1, vox=0.5)
    chk('S3-7 펠릿 9:1 (탄소 없음) — c 0 ↔ 1 σ_e 비트 같음 = 구성상 no-op (판별력 없음 기록)',
        len(regp['instances']['fi']) == 0 and np.float64(rc0['sigma_eff']).tobytes() == np.float64(rc1['sigma_eff']).tobytes()
        and rc1['cjunc'].get('s3_discriminating') is False)
    #  S3-8 변이 — 비근접에 c · (1 − c) 뒤집힘 · G 에 곱함 · c = 1 을 큰 g 로 = 실패해야
    old = CJ.sdcp_rj_eff
    det = []
    muts = (('비근접에 c', lambda r0, c, a: r0 * (1.0 - c)),
            ('(1 − c) 뒤집힘', lambda r0, c, a: r0 * (c * a if a else 1.0)),
            ('G 에 곱함', lambda r0, c, a: r0 / (1.0 - c * a) if c * a < 1 else math.inf),
            ('c = 1 을 큰 g 로', lambda r0, c, a: r0 * (1.0 - c * a) if c * a < 1 else 1e-12))
    for nm, fn in muts:
        CJ.sdcp_rj_eff = fn
        try:
            bad = False
            pm = plan(reg, 1e3, sdcp_mod={'c': 1.0})
            if int(pm['mode'][0]) != CJ.MODE_CONTRACT:
                bad = True
            pmh = plan(reg, 1e3, sdcp_mod={'c': 0.5}, quantitative=False)
            Im = I_of(solve(sid, sig_e(), F1_N, pmh), F1_N)
            if rel(Im, F1_I(500.0)) > 1e-12:
                bad = True
            pn = plan(reg_n, 1e3, sdcp_mod={'c': 1.0})
            if _rows_sig(pn) != _rows_sig(s2n):
                bad = True
            det.append(bad)
        except Exception:                                  # noqa: BLE001
            det.append(True)
        finally:
            CJ.sdcp_rj_eff = old
    chk('S3-8 변이 넷 (비근접에 c · 뒤집힘 · G 곱 · c = 1 큰 g) 을 시험이 잡는다', all(det), f'{det}')
    chk('S3-9 S2 없이 (원장 없이) = 거부', raises(lambda: CJ.cjunc_plan(None, 1e3, unreg_law='cut', ptfe_stamp='off',
                                                                     sdcp_mod={'c': 1.0}))
        and raises(lambda: solve(sid, sig_e(), F1_N, {'c': 1.0})))
    fp0 = reg['fp']['sid']
    chk('S3-10 sid 불변 — 모든 c 에서 원장의 sid 지문 = 솔브 sid', all(plan(reg, 1e3, sdcp_mod={'c': c}, quantitative=False)
                                                                    ['registry']['fp']['sid'] == fp0 for c in (0.0, 0.5, 1.0))
        and fp0 == S3._grid_fp(sid))


@case('SV')
def t_sv():
    #  SV 면 우회: A 와 B 사이에 SDCP 덩어리가 끼어 SV 면 (융합) 으로 이어진다 — 접합 저항이 크면 SV 경로가 소산을 지배
    n = (7, 3, 8)
    polys = [[(1.5, 1.5, 0.5), (1.5, 1.5, 3.5)], [(3.5, 1.5, 3.5), (3.5, 1.5, 7.5)]]   # A–B 중심선 거리 2.0 (접합 아님)
    P = rows(polys)
    sd = rows([[(2.5, 1.5, 3.5)]], phase=5, kind=0, fid0=700)
    allr = cat_rows(P, sd)
    sid, _ = bed(allr, n)                                          # SDCP 점 스탬프 → 셀 (2,1,3) = A 와 B 사이
    reg = registry(sid, allr, tol_sj_um=0.1, r_sdcp_um=0.5)
    chk('SV SDCP 경유 섬유 연결 수 (S0 꼴 · σ 전) = 1 성분 · fid 쌍 1', reg['census'].get('n_sdcp_bridging_components') == 1
        and reg['census'].get('n_sdcp_bridged_fid_pairs') == 1, f"{reg['census']}")
    r = solve(sid, sig_e(), n, plan(reg, 1e3))
    cj = r['cjunc']
    chk('SV 접합 instance 0 → 소산 = SV 면 + SDCP 셀 몫 > 0 · SV_DOMINANT 표지 (PASS 문장 금지)',
        cj['n_instances'] == 0 and cj['dissipation_share']['sv_face'] + cj['dissipation_share']['sdcp_cell'] > 0
        and cj['sv_dominant'] is True, f"{cj.get('dissipation_share')} {cj.get('sv_dominant')}")
    P2 = rows(F1)
    sid2, _ = bed(P2, F1_N)
    r2 = solve(sid2, sig_e(), F1_N, plan(registry(sid2, P2), 1e3))
    chk('SV SDCP 없음 → SV 몫 0 · SV_DOMINANT 아님', r2['cjunc']['dissipation_share']['sv_face'] == 0.0
        and r2['cjunc']['sv_dominant'] is False)


@case('MUT')
def t_mutants():
    """설계 §4-4 변이 — 조립기를 바꿔 끼운 변이가 위 시험 (해석 회로) 에 **걸려야** 한다 (판별력 · 안 걸리면 시험 무효)."""
    base_cls = CJ.CjuncAssembler

    class SingleWinner(base_cls):                          # 멤버십 단일 승자 — 교차 셀의 추가 dof 를 주 dof 로 접는다
        def __init__(self, *a, **k):
            super().__init__(*a, **k)
            pos = self.reg['positions']
            ex = np.flatnonzero(pos['live'] & ~pos['primary'])
            prim_of = {int(pos['lin'][p]): int(self.pos_dof[p]) for p in np.flatnonzero(pos['primary'])}
            for p in ex:
                self.pos_dof[p] = prim_of[int(pos['lin'][p])]

    class KeepTomb(base_cls):                              # tombstone 삭제 — 접합 자리 면을 옛 융합으로 남긴다
        def __init__(self, *a, **k):
            super().__init__(*a, **k)
            ft = dict(self.ft)
            ft['kind'] = np.where(ft['kind'] == CJ.K_CUT_SITE, CJ.K_AXIAL, ft['kind'])
            self.ft = ft

    class WrongDof(base_cls):                              # 간선을 다른 dof 에 — 포트 j 를 그 경로의 다음 위치로
        def build(self, *a, **k):
            inst = self.reg['instances']
            pj = inst['port_j'].copy()
            self.reg = dict(self.reg)
            self.reg['instances'] = dict(inst)
            self.reg['instances']['port_j'] = np.minimum(pj + 1, len(self.reg['positions']['lin']) - 1)
            return super().build(*a, **k)

    class PairCut(base_cls):                               # 쌍 단위 절단 — 미등록 자리도 그 쌍이면 절단
        def __init__(self, *a, **k):
            super().__init__(*a, **k)
            ft = dict(self.ft)
            ft['kind'] = np.where(ft['kind'] == CJ.K_UNREG, CJ.K_CUT_SITE, ft['kind'])
            self.ft = ft

    def run_with(cls, fn):
        CJ.CjuncAssembler = cls
        try:
            v = fn()
            print(f'    MUT {cls.__name__}: σ 기반 전류 {v!r}')
            return v
        except Exception as e:                             # noqa: BLE001 — 변이가 예외로 끝나도 '걸렸다' (기록한다)
            print(f'    MUT {cls.__name__}: 예외 {type(e).__name__}: {e}')
            return None
        finally:
            CJ.CjuncAssembler = base_cls

    P1_ = rows(F1); sid1, _ = bed(P1_, F1_N); reg1 = registry(sid1, P1_)
    P2_ = rows(F2); sid2, _ = bed(P2_, F2_N); reg2 = registry(sid2, P2_)
    P10 = rows(F10); sid10, _ = bed(P10, F6_N); reg10 = registry(sid10, P10)
    rj = 1e3
    I1 = run_with(SingleWinner, lambda: I_of(solve(sid1, sig_e(), F1_N, plan(reg1, rj)), F1_N))
    chk('MUT 멤버십 단일 승자 → C1 해석 사슬에서 벗어난다 (R_j 가 사라짐)', I1 is None or rel(I1, F1_I(rj)) > 1e-6, f'{I1}')
    w2 = chain_I([G_PL] + [G_AX] * 3 + [1e4 / rj] + [G_AX] * 4 + [G_PL])
    I2 = run_with(KeepTomb, lambda: I_of(solve(sid2, sig_e(), F2_N, plan(reg2, rj)), F2_N))
    chk('MUT tombstone 삭제 (옛 융합 면이 접합을 우회) → C2a 해석에서 벗어난다', I2 is None or rel(I2, w2) > 1e-6, f'{I2} {w2}')
    I3 = run_with(WrongDof, lambda: I_of(solve(sid1, sig_e(), F1_N, plan(reg1, rj)), F1_N))
    chk('MUT 접합 간선을 다른 dof 에 → C1 해석에서 벗어난다', I3 is None or rel(I3, F1_I(rj)) > 1e-6, f'{I3}')
    I4 = run_with(PairCut, lambda: I_of(solve(sid10, sig_e(), F6_N, plan(reg10, 3e3, unreg_law='fused')), F6_N))
    wf = _f6_reference(3e3, second_site=True, fused_second=True)
    chk('MUT 쌍 단위 절단 (미등록 자리까지 자름) → T1-12 fused 기준에서 벗어난다', I4 is None or rel(I4, wf) > 1e-6, f'{I4} {wf}')


@case('MUT-LEN')
def t_mut_len():
    """길이 법칙 변이 넷 — 모듈 훅을 바꿔 끼운 변이가 새 시험 (해석 회로 · 원장) 에 **걸려야** 한다.  훅이 없으면 (고치기 전) 실패."""
    def hook(name):
        return CJ is not None and callable(getattr(CJ, name, None))

    @contextlib.contextmanager
    def patched(name, fn):
        old = getattr(CJ, name)
        setattr(CJ, name, fn)
        try:
            yield
        finally:
            setattr(CJ, name, old)

    rj = 1e3
    Plp = rows(LP)
    sidlp, _ = bed(Plp, LP_N)
    P1_ = rows(F1)
    sid1, _ = bed(P1_, F1_N)
    Pku = rows(KU)
    sidku, _ = bed(Pku, KU_N)

    def lp_err(law='cut'):
        return rel(_try(lambda: I_of(solve(sidlp, sig_e(), LP_N, plan(registry(sidlp, Plp), rj, unreg_law=law)), LP_N)), LP_I(rj))

    def f1_err():
        return rel(_try(lambda: I_of(solve(sid1, sig_e(), F1_N, plan(registry(sid1, P1_), rj)), F1_N)), F1_I(rj))

    def ku_cont_ok():
        """s < s_min — 자기 접합 0 · σ = 옛 경로 (1e-12)."""
        reg = _try(lambda: registry(sidku, Pku, s_min_um=KU_S + 0.5), None)
        if reg is None:
            return False
        Ih = _try(lambda: I_of(solve(sidku, sig_e(), KU_N, plan(reg, rj)), KU_N))
        return int(np.sum(reg['instances']['self'])) == 0 and rel(Ih, I_of(solve_legacy(sidku, sig_e(), KU_N), KU_N)) < 1e-12

    #  (이름 · 훅 · 변이 · 검사) — 변이 전 검사 통과 · 변이 뒤 같은 검사 실패 (예외로 멈춰도 '걸렸다' · B 의 MUT 와 같은 규약:
    #   max(1, ·) 빼기는 계획의 배율 ≥ 1 불변량이 해석 대조 전에 막는다)
    cases = (
        ('배율 제곱 → LEN-P 해석에서 벗어난다', 'junction_len_mult',
         lambda Lc, Lp: np.maximum(1.0, np.asarray(Lc, np.float64) / Lp) ** 2, lambda: lp_err() < 1e-12),
        ('max(1, ·) 빼기 (짧은 접촉이 약해짐) → C1 해석 · 배율 불변량에 걸린다', 'junction_len_mult',
         lambda Lc, Lp: np.asarray(Lc, np.float64) / Lp, lambda: f1_err() < 1e-12),
        ('s 거르기 끔 → s < s_min 인데 자기 접합이 생긴다 (KINK 연속 기준 실패)', '_self_is_junction',
         lambda s, smin: np.ones(np.shape(np.atleast_1d(s)), bool), ku_cont_ok),
        ('발자국 = 최근접 선분 쌍만 → run 위 A|B 면이 fused 로 남아 LEN-P (fused) 해석에서 벗어난다', '_footprint_segs',
         lambda inst, k: (np.atleast_1d(inst['si_min'][k]), np.atleast_1d(inst['sj_min'][k])),
         lambda: lp_err('fused') < 1e-12),
    )
    for nm, name, fn, check in cases:
        h = hook(name)
        b = bool(check()) if h else False
        c = None
        if h:
            with patched(name, fn):
                c = not bool(check())
        chk(f'MUT-LEN {nm} (훅 `{name}` 있음 · 변이 전 통과 · 변이 실패)', h and b and c is True, f'hook {h} base {b} caught {c}')


# ═════════════════════════ FP — 지문 재현 (RINT-23 · 같은 꼴 확인 · 2 일 차) ═════════════════════════
#  계약: 같은 내용 · 다른 객체 → 같은 지문 · 별도 `python3 -I` 하위 프로세스 둘 → 같은 지문 · 내용 한 글자 다름 → 다른 지문.
#  RINT-23 — `_fp` 가 dtype=object 배열의 **포인터 바이트** (`x.data`) 를 해시했다.  원장 `instances['reason']` (포트 미실현 사유 ·
#  f-문자열 = 호출마다 새 객체) 이 그 배열이라, 같은 입력으로 다시 만든 원장 · 계획 지문이 프로세스 안에서도 사이에서도 갈렸다 (거짓 거부).
#  픽스처 = F1 + 교차 셀 (1,1,3) 을 덮는 SDCP 점 (r_port 0.5 → 포트 미실현 'covered_SDCP') + z = 3 면 위 PTFE (S1 VGCF|SDCP 면 α < 1).
_FP_SDCP = [[(1.5, 1.5, 3.5)]]
_FP_PTFE = [[(0.5, 1.5, 3.0), (2.5, 1.5, 3.0)]]
_FP_RPORT = 0.5
_FP_WORDS = ('covered_SDCP', '', 'out_of_box', '탄소 접합 · 포트 (UTF-8)', 'no_live_port_in_rport')

#  하위 프로세스 · 이 프로세스가 **같은 글** 을 돌린다 (지문을 만드는 경로 하나 — 기대값을 이 파일이 따로 만들지 않는다).
_FP_PROG = r'''
def fp_values(cfg):
    import hashlib
    import numpy as np
    import step3_sigma as S3
    import carbon_junction as CJ
    import ptfe_face_alpha as FA
    import ca_s0_census as S0
    z = np.load(cfg['npz'])
    P, PH, F, K = z['P'], z['PH'], z['F'], z['K']
    n = tuple(int(x) for x in z['n'])
    vox = float(z['vox'])
    lo = (0.0, 0.0, 0.0)
    hi = tuple(n[i] * vox for i in range(3))
    m = PH != 4                                                # face_alpha 침대 = PTFE 셀 없음 (off 격자)
    sid, pid = S3.rasterize(np.zeros((0, 3)), np.zeros(0), np.zeros(0, np.int64), P[m], PH[m], lo, hi, vox,
                            add_fid=F[m], add_kind=K[m])
    reg = CJ.cjunc_registry(sid, lo, vox, P, PH, F, K, **cfg['thr'])
    pl = CJ.cjunc_plan(reg, 1.0e3, unreg_law='cut', ptfe_stamp='off')
    obj = np.empty(len(cfg['words']), dtype=object)
    for i, w in enumerate(cfg['words']):
        obj[i] = ''.join(list(w))                              # 실행 중 만든 문자열 (상수 · 인턴 객체 아님)
    m4 = PH == 4
    caps = FA.build_capsules(P[m4], F[m4], K[m4])
    sig = S3.electronic_sigma_table(0.010, 0.005, 100.0, 10.0, 250.0)
    fa = FA.build_plan(sid, sig, caps, lo=lo, vox=vox, channel='electronic', pid=pid)
    used = tuple({'lin': fa['axes'][a]['lin'], 'alpha': fa['axes'][a]['alpha'], 'g': fa['axes'][a]['alpha'] * 2.0}
                 for a in range(3))
    plan0, pbytes, psha = S0.make_plan(0.15, 0.075, 2.0, {'stage': 1, 'kit_name': ''.join(['kit', '_fp'])})
    return {'cj_objarr': CJ._fp(obj), 'cj_reg_sid': reg['fp']['sid'], 'cj_reg_centreline': reg['fp']['centreline'],
            'cj_reg_membership': reg['fp']['membership'], 'cj_reg_registry': reg['fp']['registry'],
            'cj_plan_rows': pl['fp_rows'], 'cj_plan_record_registry': pl['record']['fp_registry'],
            'fa_caps': caps['fp'], 'fa_rows': fa['fp_rows'], 'fa_plan': fa['fp_plan'], 'fa_edges': FA.edges_fp(used),
            'fa_grid_sid': FA._grid_fp(sid), 'fa_grid_pid': FA._grid_fp(pid),
            's0_plan_sha': psha, 's0_plan_bytes_sha': hashlib.sha256(S0.plan_bytes_of(plan0)).hexdigest(),
            's0_file_sha': S0._sha256_file(cfg['npz'])}
'''
_FP_CHILD_MAIN = r'''
import json, sys
cfg = json.loads(sys.argv[1])
for p in cfg['paths']:
    if p not in sys.path:
        sys.path.insert(0, p)
_junk = [str(i) * 7 for i in range(int(cfg['junk']))]        # 힙 배치를 바꾼다 (ASLR 이 꺼진 기계에서도 객체 주소가 갈리게)
g = {}
exec(compile(cfg['prog'], '<fp-prog>', 'exec'), g)
print('FPJSON ' + json.dumps(g['fp_values'](cfg), sort_keys=True))
'''


def _rt(s):
    """실행 중 새로 만든 같은 내용 문자열 — 두 글자 이상이면 다른 객체 (CPython 은 '' · 한 글자만 공유한다)."""
    return ''.join(list(s))


def _objarr(items):
    a = np.empty(len(items), dtype=object)
    for i, v in enumerate(items):
        a[i] = v
    return a


def _fp_numeric_formula(x):
    """숫자 배열 지문의 **독립** 식 (모듈 밖) — blake2b-16 (dtype.str · repr(모양) · C 순서 바이트)."""
    c = np.ascontiguousarray(x)
    h = hashlib.blake2b(digest_size=16)
    h.update(c.dtype.str.encode()); h.update(repr(c.shape).encode()); h.update(c.tobytes(order='C'))
    return h.hexdigest()


def _fp_fixture():
    P = cat_rows(rows(F1), rows(_FP_SDCP, phase=5, kind=0, fid0=700), _ptfe_rows(_FP_PTFE))
    sid, pid = bed(P, F1_N, stamp=P[1] != 4)
    return P, sid, pid


def _fp_thr():
    return dict(r_f_um=RF, tol_ff_um=TOL, L_par_um=LPAR, r_port_um=_FP_RPORT, gap_tol=2.0, s_min_um=S_MIN)


def _fp_children(tmpd, P):
    """같은 글 (`_FP_PROG`) 을 별도 `python3 -I` 하위 프로세스 둘 (힙 선할당 0 · 20000) 과 이 프로세스에서 돌린다 → (자식 둘, 이 프로세스)."""
    npz = os.path.join(tmpd, 'fp_fixture.npz')
    np.savez(npz, P=P[0], PH=P[1], F=P[2], K=P[3], n=np.array(F1_N), vox=np.float64(H))
    paths = [SCRIPTS]
    for mod in (np, __import__('scipy')):                 # 사용자 site 의 numpy 도 -I 에서 찾게 (명시 경로 · 암묵 경로 없음)
        d = os.path.dirname(os.path.dirname(os.path.abspath(mod.__file__)))
        if d not in paths:
            paths.append(d)
    thr = reg_kw(_fp_thr())
    cfg = {'paths': paths, 'npz': npz, 'thr': thr, 'words': list(_FP_WORDS), 'prog': _FP_PROG}
    kids = []
    for junk in (0, 20000):
        c = dict(cfg, junk=junk)
        r = subprocess.run([sys.executable, '-I', '-c', _FP_CHILD_MAIN, json.dumps(c)], capture_output=True, text=True,
                           timeout=600)
        line = [x for x in r.stdout.splitlines() if x.startswith('FPJSON ')]
        if r.returncode != 0 or not line:
            print(f'    FP 하위 프로세스 (junk {junk}) rc {r.returncode}: {(r.stderr or r.stdout)[-400:]}')
            kids.append(None)
        else:
            kids.append(json.loads(line[-1][len('FPJSON '):]))
    g = {}
    exec(compile(_FP_PROG, '<fp-prog>', 'exec'), g)
    here = quiet(g['fp_values'], dict(cfg, junk=0))
    return kids, here


#: 지문 · 해시 함수 목록 (AST — 본문이 `hashlib` 을 쓰는 함수) — 이 표 밖의 함수가 생기면 FP 시험이 그것을 덮지 못한다 → 실패.
FP_INVENTORY = {
    'carbon_junction': {'_fp': 'FP-a…h · FP-i (원장 · 계획 · 객체 배열)'},
    'ptfe_face_alpha': {'_h16': 'FP-i · FP-k (캡슐 · 행 · 계획 · 간선 지문 — 고정 dtype 바이트 · 문자열)',
                        '_path_radius': '두 집단 지름 분류 해시 (점열 float64 바이트 · F-DIA 순열 불변) — 지문 아님'},
    'ca_s0_census': {'_sha256_file': 'FP-i · FP-l', 'make_plan': 'FP-i · FP-l (정준 JSON 바이트)',
                     'verify_plan_commit': '커밋 안 계획 파일 바이트 sha256 (L3 시험)',
                     'validate_kit_arrays': '정확 중복 경로 = 점열 float64 바이트 sha256 (S0-5i)',
                     'census_kit': 'payload argv sha256 (NUL 결합 UTF-8 · 기록만)'},
    'step3_conv_cert': {},
}


def _hash_users(path):
    tree = ast.parse(open(path, encoding='utf-8').read())
    out = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if any(isinstance(x, ast.Name) and x.id == 'hashlib' for x in ast.walk(node)):
                out.add(node.name)
    return out


@case('FP')
def t_fp():
    import ptfe_face_alpha as FA
    import ca_s0_census as S0
    # ── FP-a · b · c · d · e · f — `_fp` 자체 ──
    a = _objarr([_rt(w) for w in _FP_WORDS])
    b = _objarr([_rt(w) for w in _FP_WORDS])
    distinct = any(x is not y for x, y in zip(a, b))
    chk('FP-a 객체 배열 — 같은 내용 · 다른 객체 (실행 중 만든 문자열 · UTF-8 · 빈 문자열) → 같은 지문 (원소 · dict 안 · 목록 안)',
        distinct and CJ._fp(a) == CJ._fp(b) and CJ._fp({'reason': a, 'k': 1}) == CJ._fp({'reason': b, 'k': 1})
        and CJ._fp([a, 3]) == CJ._fp([b, 3]), f'다른 객체 {distinct}')
    w2 = list(_FP_WORDS); w2[0] = 'covered_SDCQ'
    w3 = list(_FP_WORDS); w3[3] = w3[3].replace('접합', '접힙')
    chk('FP-b 한 글자 다름 (ASCII · 한글) → 다른 지문', CJ._fp(a) != CJ._fp(_objarr([_rt(w) for w in w2]))
        and CJ._fp(a) != CJ._fp(_objarr([_rt(w) for w in w3])))
    #  같은 모양 쌍이 경계 · 길이 접두를 본다 (모양이 다르면 머리의 모양만으로도 갈린다) — 변이 판별: '|'·'' 결합 · repr 결합 ([1, 23] ~
    #  [12, 3]) · 형 표지만 있고 길이 접두 없음 (['aSb', 'c'] ~ ['a', 'bSc'])
    pairs = ((['ab', 'c'], ['a', 'bc']), (['a|b', 'c'], ['a', 'b|c']), (['aSb', 'c'], ['a', 'bSc']), ([1, 23], [12, 3]),
             (['a', 'b'], ['b', 'a']), (['x'], ['x', '']), (['1'], [1]), ([None], ['None']), ([True], [1]), ([1.0], [1]),
             ([b'ab'], ['ab']))
    bad = [f'{p}~{q}' for p, q in pairs if CJ._fp(_objarr([_rt(x) if isinstance(x, str) else x for x in p]))
           == CJ._fp(_objarr([_rt(x) if isinstance(x, str) else x for x in q]))]
    sq = _objarr([_rt('ab'), _rt('cd')])
    if CJ._fp(sq) == CJ._fp(sq.reshape(1, 2)):
        bad.append('모양 (2,)~(1,2)')
    chk('FP-c 경계 · 순서 · 개수 · 모양 · 형 (길이 접두 · 순서 보존 · 형 표지) → 다른 지문', not bad, f'{bad}')

    def _mixed():
        k = int('1000') + 7
        return _objarr([None, bool(k), k, float(k) / 4.0, np.float64(k) / 8.0, np.int64(k) * 3, bytes([120, 121]),
                        (_rt('ab'), k), _rt('끝')])
    m1, m2 = _mixed(), _mixed()
    chk('FP-d 섞인 원소 (None · bool · int · float · numpy 수 · bytes · 튜플) — 같은 내용 · 다른 객체 → 같은 지문',
        CJ._fp(m1) == CJ._fp(m2))
    a2 = np.arange(12, dtype=np.int64).reshape(3, 4)
    nums = (a2, np.linspace(0.0, 1.0, 7), a2.T, a2[:, ::2], np.zeros((0, 3)), np.array([True, False]))
    chk('FP-e 숫자 배열 = dtype · 모양 · C 순서 바이트 그대로 (독립 식 · 연속 아닌 뷰 = 연속 사본) — 옛 지문 비트 유지',
        all(CJ._fp(x) == _fp_numeric_formula(x) for x in nums) and CJ._fp(a2.T) == CJ._fp(np.ascontiguousarray(a2.T)))
    refused = [raises(lambda v=v: CJ._fp(v), TypeError) for v in
               (_objarr([object()]), _objarr([_rt('ok'), {1, 2}]), object(), {1, 2}, np.zeros(2, dtype=[('a', 'O')]))]
    chk('FP-f 내용 직렬화가 없는 원소 · 값 (object() · set · 구조체 객체 칸) = 거부 (주소 · 해시 순서로 지문을 만들지 않는다)',
        all(refused), f'{refused}')
    # ── FP-g · h — 원장 · 계획 지문 (픽스처: 포트 미실현 사유 'covered_SDCP' = f-문자열) ──
    P, sid, pid = _fp_fixture()
    r1 = registry(sid, P, r_port_um=_FP_RPORT)
    r2 = registry(sid, P, r_port_um=_FP_RPORT)
    rs1, rs2 = r1['instances']['reason'], r2['instances']['reason']
    pre = (len(rs1) == 1 and rs1.dtype == object and rs1[0] == 'covered_SDCP' and rs1[0] is not rs2[0])
    p1 = _try(lambda: plan(r1, 1e3), None)
    p2 = _try(lambda: plan(r2, 1e3), None)
    chk('FP-g 같은 입력으로 다시 만든 원장 — 원장 지문 · 계획 행 지문 같음 (사유 = 실행 중 만든 다른 문자열 객체)',
        pre and r1['fp']['registry'] == r2['fp']['registry'] and p1 is not None and p2 is not None
        and p1['fp_rows'] == p2['fp_rows'], f"전제 {pre} · {r1['fp']['registry']} ↔ {r2['fp']['registry']}")
    rsame = dict(r1); rsame['instances'] = dict(r1['instances'])
    rsame['instances']['reason'] = _objarr([_rt(x) for x in rs1])
    ok_same = (CJ.registry_fp(rsame) == r1['fp']['registry']) and (_try(lambda: plan(rsame, 1e3), None) is not None)
    chk('FP-h 같은 내용 새 객체로 바꾼 원장 → 지문 같음 · 계획이 받아들인다 (거짓 거부 없음)', ok_same)
    rdiff = dict(r1); rdiff['instances'] = dict(r1['instances'])
    rdiff['instances']['reason'] = _objarr([_rt(x).replace('SDCP', 'SDCQ') for x in rs1])
    chk('FP-h 한 글자 바꾼 원장 (사유 SDCP → SDCQ) → 지문 다름 · 계획 거부 (E5)',
        CJ.registry_fp(rdiff) != r1['fp']['registry'] and raises(lambda: plan(rdiff, 1e3)))
    # ── FP-i — 별도 `python3 -I` 하위 프로세스 둘 · 이 프로세스 ──
    tmpd = tempfile.mkdtemp(prefix='cjfp_')
    try:
        kids, here = _fp_children(tmpd, P)
    finally:
        shutil.rmtree(tmpd, ignore_errors=True)
    for grp, nm in (('cj_', 'carbon_junction (객체 배열 · 원장 · 계획)'), ('fa_', 'ptfe_face_alpha (캡슐 · 행 · 계획 · 간선 · 격자)'),
                    ('s0_', 'ca_s0_census (계획 sha256 · 정준 바이트 · 파일 sha256)')):
        keys = sorted(k for k in (here or {}) if k.startswith(grp))
        same = (bool(keys) and all(k_ is not None for k_ in kids)
                and all(kids[0].get(k) == kids[1].get(k) == here[k] for k in keys))
        diff = [k for k in keys if not (kids[0] and kids[1]) or not (kids[0].get(k) == kids[1].get(k) == here.get(k))]
        chk(f'FP-i 별도 `python3 -I` 하위 프로세스 둘 (힙 선할당 0 · 20000) = 이 프로세스 — {nm} ({len(keys)} 지문)', same,
            f'다름 {diff}')
    # ── FP-j — 격자 지문 감싸개 (`_grid_fp` → step3_sigma._grid_fp) ──
    g0 = np.arange(24, dtype=np.int8).reshape(2, 3, 4)
    g1 = g0.copy()
    g2 = g0.copy(); g2[1, 2, 3] += 1
    gobj = np.empty((2, 2, 2), dtype=object)
    for i in range(gobj.size):
        gobj.flat[i] = int('100') + i
    for nm_, fn in (('carbon_junction', CJ._grid_fp), ('ptfe_face_alpha', FA._grid_fp)):
        chk(f'FP-j {nm_}._grid_fp 숫자 격자 — 같은 내용 다른 객체 = 같음 · 한 칸 다름 · dtype 다름 = 다름',
            fn(g0) == fn(g1) and fn(g0) != fn(g2) and fn(g0) != fn(g0.astype(np.int16)) and fn(None) is None)
        chk(f'FP-j {nm_}._grid_fp 객체 격자 = 거부 (포인터 바이트 · 격자는 수치 배열 계약)', raises(lambda f_=fn: f_(gobj), TypeError))
    # ── FP-k — S1 지문 (내용 기반 확인 · 옛 코드도 통과해야 한다) ──
    m4 = P[1] == 4
    Q, Fq, Kq = P[0][m4], P[2][m4], P[3][m4]
    big = np.repeat(Q, 2, axis=0)
    variants = (Q.copy(), np.asfortranarray(Q), big[::2], Q.tolist())
    fps = [FA.build_capsules(v, Fq, Kq)['fp'] for v in variants]
    Qd = Q.copy(); Qd[1, 0] = np.nextafter(Qd[1, 0], np.inf)
    sig = sig_e()
    pa = FA.build_plan(sid, sig, FA.build_capsules(Q, Fq, Kq), lo=(0.0, 0.0, 0.0), vox=H, channel='electronic', pid=pid)
    pb = FA.build_plan(sid.copy(), sig.copy(), FA.build_capsules(Q.copy(), Fq.copy(), Kq.copy()), lo=(0.0, 0.0, 0.0), vox=H,
                       channel='electronic', pid=pid.copy())
    ax = tuple({'lin': pa['axes'][k]['lin'].astype(np.int32), 'alpha': pa['axes'][k]['alpha']} for k in range(3))
    e1 = tuple({'lin': pa['axes'][k]['lin'], 'alpha': pa['axes'][k]['alpha'], 'g': pa['axes'][k]['alpha'] * 2.0} for k in range(3))
    e2 = tuple({kk: np.array(vv) for kk, vv in e.items()} for e in e1)
    e3 = tuple({kk: np.array(vv) for kk, vv in e.items()} for e in e1)
    nz = [k for k in range(3) if len(e3[k]['g'])]
    if nz:
        e3[nz[0]]['g'][0] = np.nextafter(e3[nz[0]]['g'][0], np.inf)
    chk('FP-k ptfe_face_alpha — 캡슐 지문 (사본 · F 순서 · 연속 아닌 뷰 · 목록 = 같음 · 좌표 1 ulp = 다름) · 계획 행 · 계획 · 간선 '
        '(같은 내용 = 같음 · 1 ulp = 다름)',
        len(set(fps)) == 1 and FA.build_capsules(Qd, Fq, Kq)['fp'] != fps[0] and pa['n_rows'] > 0
        and pa['fp_rows'] == pb['fp_rows'] and pa['fp_plan'] == pb['fp_plan'] and FA.rows_fp(ax) == pa['fp_rows']
        and FA.edges_fp(e1) == FA.edges_fp(e2) and bool(nz) and FA.edges_fp(e1) != FA.edges_fp(e3),
        f"캡슐 {len(set(fps))} · 행 {pa['n_rows']}")
    # ── FP-l — S0 계획 · 파일 sha256 ──
    _, b1, h1 = S0.make_plan(0.15, 0.075, 2.0, {'stage': 1, 'kit_name': _rt('kit_fp')})
    _, b2, h2 = S0.make_plan(float('0.15'), 0.075, 2.0, dict({'kit_name': _rt('kit_fp')}, stage=1))
    _, b3, h3 = S0.make_plan(0.15, 0.075, 2.0, {'stage': 1, 'kit_name': _rt('kit_fq')})
    tmpd = tempfile.mkdtemp(prefix='s0fp_')
    try:
        fa_, fb_, fc_ = (os.path.join(tmpd, x) for x in ('a.bin', 'b.bin', 'c.bin'))
        for pth, data in ((fa_, b1), (fb_, bytes(bytearray(b1))), (fc_, b1[:-2] + b'X\n')):
            with open(pth, 'wb') as fh:
                fh.write(data)
        same_f = S0._sha256_file(fa_) == S0._sha256_file(fb_) and S0._sha256_file(fa_) != S0._sha256_file(fc_)
    finally:
        shutil.rmtree(tmpd, ignore_errors=True)
    chk('FP-l ca_s0_census — 계획 sha256 · 정준 바이트 (다른 객체로 만든 같은 계획 = 같음 · 출처 한 글자 = 다름) · 파일 sha256',
        h1 == h2 and b1 == b2 and h1 != h3 and same_f)
    # ── FP-m — 목록 (이 시험이 덮는 지문 · 해시 함수 = 모듈 본문의 hashlib 사용 함수 전부) ──
    got = {m_: _hash_users(os.path.join(SCRIPTS, m_ + '.py')) for m_ in FP_INVENTORY}
    want = {m_: set(v) for m_, v in FP_INVENTORY.items()}
    chk('FP-m 지문 · 해시 함수 목록 = 이 시험의 표 (새 함수 = 덮을 때까지 실패 · step3_conv_cert = 없음)', got == want,
        f'{ {m_: sorted(got[m_] ^ want[m_]) for m_ in got if got[m_] != want[m_]} }')


# ═════════════════════════ PIECE4 — 끊기 규칙 사본 대조 (생산 · B · C · A · 2 일 차) ═════════════════════════
#  같은 gap_tol 규칙 (연속 점 간격 > gap_tol × 그 경로 간격 중앙값 → 끊음) 이 네 곳에 따로 있다: 생산 `step3_sigma._fibre_segment_ijk`
#  (셀만 낸다) · B `carbon_junction.fibre_pieces` · C `ca_s0_census.pieces_of` · A `ptfe_face_alpha.build_capsules` (안쪽 줄).
#  하나로 합치지 않는다 (생산 경로 비트 동일 부담) — 이 시험이 넷을 묶는다.  침대 (µm · vox 0.1): 틈 > 2 셀 · 한 점 조각 (앞 · 가운데 ·
#  뒤) · 정확히 경계인 틈 (d = gap_tol × 중앙값 → 끊지 않는다 · 이진 정확 좌표) · 두 점 · 한 점 경로 · 무작위 3D (지운 점 = 틈).
#  ① 조각 경계 (점 번호 구간) B = C = A ② 생산 셀 열 = 각 사본의 조각을 생산 원시 함수 (`segment_cells`) 로 다시 구운 셀 열 (순서 그대로)
#  ③ C 의 셀 빌더 (`_cells_from_pieces`) = 생산 셀 열 · B 의 멤버십 위치 셀 집합 = 생산 셀 집합.
PIECE4_VOX = 0.1
PIECE4_N = (40, 40, 40)
_PIECE4_MUT = {'step3_sigma': 'np.nonzero(d > gap_tol * med)', 'carbon_junction': 'np.nonzero(d > gap_tol * med)',
               'ca_s0_census': 'np.nonzero(d > gap_tol * med)', 'ptfe_face_alpha': 'np.nonzero(d > g_t * med)'}


def _piece4_beds():
    def line(x0, n, dx=0.1, y=1.05, z=1.05):
        return [(x0 + dx * k, y, z) for k in range(n)]
    beds = []
    beds.append(('틈 하나 (0.6 µm = 6 셀)', np.array(line(0.15, 10) + line(1.65, 10))))
    beds.append(('한 점 조각 — 앞 · 가운데 · 뒤', np.array([(0.15, 2.05, 1.05)] + line(0.75, 5, y=2.05) + [(1.85, 2.05, 1.05)]
                                                       + line(2.45, 4, y=2.05) + [(3.55, 2.05, 1.05)])))
    #  정확 경계: 간격 0.25 (이진 정확) · 0.5 = 2 × 중앙값 (끊지 않음 · 엄격 >) · 0.75 (끊음) — `>=` 변이는 0.5 에서도 끊는다
    xs = [0.25, 0.5, 0.75, 1.0, 1.5, 1.75, 2.0, 2.75, 3.0, 3.25]
    beds.append(('정확히 경계인 틈 (0.5 = 2 × 0.25 · 끊지 않음) + 끊는 틈 0.75', np.array([(x, 0.375, 2.125) for x in xs])))
    beds.append(('두 점 경로', np.array([(0.35, 3.05, 3.05), (0.95, 3.05, 3.05)])))
    beds.append(('한 점 경로', np.array([(2.35, 3.05, 3.05)])))
    rng = np.random.default_rng(20261020)
    box = np.array(PIECE4_N, float) * PIECE4_VOX
    for t in range(6):
        p = [rng.uniform(0.6, box - 0.6)]
        for _ in range(int(rng.integers(25, 45))):
            d = rng.normal(size=3); d /= np.linalg.norm(d)
            p.append(np.clip(p[-1] + d * rng.uniform(0.07, 0.12), 0.02, box - 0.02))
        Q = np.asarray(p)
        keep = np.ones(len(Q), bool)
        for _ in range(int(rng.integers(1, 4))):                # 지운 점 = 틈 (시더가 AM 안 점을 드랍하는 꼴)
            a = int(rng.integers(2, len(Q) - 6)); keep[a:a + int(rng.integers(3, 7))] = False
        beds.append((f'무작위 3D {t}', Q[keep]))
    return beds


def _piece4_ranges_index(Q, pcs):
    out, a = [], 0
    for ix in pcs:
        ix = np.asarray(ix)
        if not np.array_equal(ix, np.arange(a, a + len(ix))):
            return None
        out.append((a, a + len(ix))); a += len(ix)
    return out if a == len(Q) else None


def _piece4_ranges_points(Q, pcs):
    out, a = [], 0
    for R in pcs:
        R = np.asarray(R, np.float64).reshape(-1, 3)
        if not np.array_equal(R, Q[a:a + len(R)]):
            return None
        out.append((a, a + len(R))); a += len(R)
    return out if a == len(Q) else None


def _piece4_capsule_pieces(caps):
    """A — 캡슐 선분 (A→B) 에서 조각 점열을 되읽는다: 새 조각 = 앞 선분 끝 ≠ 이 선분 시작 · 선분 하나 · 길이 0 = 한 점 조각."""
    A, B = np.asarray(caps['A']), np.asarray(caps['B'])
    pieces = []
    for i in range(len(A)):
        if i == 0 or not np.array_equal(A[i], B[i - 1]):
            pieces.append([A[i], B[i]])
        else:
            pieces[-1].append(B[i])
    return [np.asarray(p[:1]) if len(p) == 2 and np.array_equal(p[0], p[1]) else np.asarray(p) for p in pieces]


def _piece4_cells(Q, ranges, lo, vox, n):
    from fibre_segment_raster import segment_cells
    out = []
    for a, b in ranges:
        R = Q[a:b]
        if len(R) == 1:
            out.append(np.floor((R - lo) / vox).astype(int))
        else:
            out.append(np.vstack([segment_cells(R[i] - lo, R[i + 1] - lo, vox) for i in range(len(R) - 1)]))
    ijk = np.vstack(out).astype(int) if out else np.zeros((0, 3), int)
    return ijk[((ijk >= 0) & (ijk < n)).all(1)]


def _piece4_compare(mods, gap_tols=(2.0, 3.0)):
    """네 구현 (mods = 생산 · B · C · A 모듈) 대조 → (불일치 목록, 정확 경계 틈이 있던 침대 수)."""
    s3m, cjm, s0m, fam = (mods[k] for k in ('step3_sigma', 'carbon_junction', 'ca_s0_census', 'ptfe_face_alpha'))
    lo = np.zeros(3); n = np.array(PIECE4_N); vox = PIECE4_VOX
    bad, n_exact = [], 0
    for nm, Q in _piece4_beds():
        Q = np.asarray(Q, np.float64)
        if len(Q) >= 2:
            d = np.linalg.norm(np.diff(Q, axis=0), axis=1)
            n_exact += int(np.any(d == 2.0 * float(np.median(d))))
        for gt in gap_tols:
            tag = f'{nm} · gap_tol {gt}'
            m = len(Q)
            prod, _ph = quiet(s3m._fibre_segment_ijk, Q, np.full(m, 2), np.full(m, 7), lo, vox, n, gt,
                              add_kind=np.ones(m, int))
            rB = _piece4_ranges_index(Q, cjm.fibre_pieces(Q, gt))
            pcsC = s0m.pieces_of(Q, gt)
            rC = _piece4_ranges_points(Q, pcsC)
            caps = fam.build_capsules(Q, np.zeros(m, np.int64), np.ones(m, np.int64), gap_tol=gt)
            rA = _piece4_ranges_points(Q, _piece4_capsule_pieces(caps))
            if rB is None or rC is None or rA is None or not (rB == rC == rA):
                bad.append(f'{tag}: 조각 경계 B {rB} · C {rC} · A {rA}')
                continue
            if caps['n_pieces'] != len(rA) or caps['n_point_pieces'] != sum(1 for a, b in rA if b - a == 1):
                bad.append(f'{tag}: A 조각 수 기록 {caps["n_pieces"]} · 한 점 {caps["n_point_pieces"]} ↔ {rA}')
            for who, rr in (('B', rB), ('C', rC), ('A', rA)):
                if not np.array_equal(_piece4_cells(Q, rr, lo, vox, n), prod):
                    bad.append(f'{tag}: 생산 셀 열 ≠ {who} 조각으로 다시 구운 셀 열')
            if not np.array_equal(s0m._cells_from_pieces(pcsC, lo, vox, n), prod):
                bad.append(f'{tag}: C 셀 빌더 ≠ 생산 셀 열')
            segs, pcs = cjm._segments_of([(7, np.arange(m), True)], Q, gt)
            pos, _pp = cjm._positions(pcs, segs, lo, vox, n, np.zeros(PIECE4_N, np.int8))
            inb = pos['lin'] >= 0
            if {tuple(int(v) for v in c) for c in pos['ijk'][inb]} != {tuple(int(v) for v in c) for c in prod}:
                bad.append(f'{tag}: B 멤버십 셀 집합 ≠ 생산 셀 집합')
    return bad, n_exact


def _piece4_mutant(modname, tmpd):
    src = open(os.path.join(SCRIPTS, modname + '.py'), encoding='utf-8').read()
    old = _PIECE4_MUT[modname]
    if src.count(old) != 1:
        return None, f'변이 대상 문자열 {old!r} 이 {modname}.py 에 {src.count(old)} 번 (1 번이어야)'
    p = os.path.join(tmpd, f'{modname}_piece4_mut.py')
    with open(p, 'w', encoding='utf-8') as fh:
        fh.write(src.replace(old, old.replace(' > ', ' >= ')))
    spec = importlib.util.spec_from_file_location(f'{modname}_piece4_mut', p)
    m = importlib.util.module_from_spec(spec)
    quiet(spec.loader.exec_module, m)
    return m, ''


@case('PIECE4')
def t_piece4():
    import ptfe_face_alpha as FA
    import ca_s0_census as S0
    real = {'step3_sigma': S3, 'carbon_junction': CJ, 'ca_s0_census': S0, 'ptfe_face_alpha': FA}
    bad, n_exact = _piece4_compare(real)
    nb = len(_piece4_beds())
    chk(f'PIECE4 네 구현 (생산 · B · C · A) — 조각 경계 같음 · 생산 셀 열 = 각 사본 조각을 다시 구운 셀 열 · C 셀 빌더 = 생산 · '
        f'B 멤버십 셀 집합 = 생산 ({nb} 침대 × gap_tol 2 · 3 · 정확 경계 틈 침대 {n_exact})', not bad and n_exact >= 1,
        f'{bad[:4]} · 정확 경계 {n_exact}')
    tmpd = tempfile.mkdtemp(prefix='piece4_')
    try:
        for modname in ('step3_sigma', 'carbon_junction', 'ca_s0_census', 'ptfe_face_alpha'):
            mut, why = _piece4_mutant(modname, tmpd)
            caught = False
            if mut is not None:
                mods = dict(real)
                mods[modname] = mut
                try:
                    mb, _ = _piece4_compare(mods)
                    caught = bool(mb)
                except Exception as e:                     # noqa: BLE001 — 변이가 예외로 끝나도 '걸렸다' (기록)
                    print(f'    PIECE4 변이 {modname}: 예외 {type(e).__name__}: {e}')
                    caught = True
            chk(f'PIECE4 변이 — {modname} 사본의 `>` → `>=` (나머지 셋은 그대로) → 시험이 떨어진다 (정확 경계 틈)',
                mut is not None and caught, why or 'not caught')
    finally:
        shutil.rmtree(tmpd, ignore_errors=True)


def main():
    global S3, CJ, QUICK
    ap = argparse.ArgumentParser(description='Rint ② S2/S3 시험 (시험 먼저)')
    ap.add_argument('--quick', action='store_true', help='C0 무작위 침대 수를 줄인다')
    ap.add_argument('--only', default='', help='쉼표로 묶음 태그만 (예: C1,S3)')
    a = ap.parse_args()
    QUICK = a.quick
    import step3_sigma as _s3
    S3 = _s3
    try:
        import carbon_junction as _cj
        CJ = _cj
    except Exception as e:                                 # noqa: BLE001
        print(f'  ⚠ carbon_junction import 실패: {type(e).__name__}: {e}')
        CJ = None
    only = {x.strip() for x in a.only.split(',') if x.strip()}
    for tag, fn in CASES:
        if only and tag not in only:
            continue
        print(f'── {tag}')
        try:
            fn()
        except Exception as e:                             # noqa: BLE001 — 묶음 하나의 예외 = 그 묶음 실패 (다음 묶음은 계속)
            import traceback
            traceback.print_exc(limit=2)
            chk(f'{tag} 묶음 예외 없이 끝남', False, f'{type(e).__name__}: {e}')
    print(f'\n== test_carbon_junction: {_ok}/{_ok + len(_fail)} PASS')
    if _fail:
        print('FAIL: ' + ' · '.join(_fail))
    return 0 if not _fail else 1


if __name__ == '__main__':
    sys.exit(main())
