#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rint G2 ①′ — RRM (resolved reference model · 시험 전용) + N9 `reject_film_off_outside` 시험 (반례 먼저 · 규율 ② · 2026-10-13).

정본 계약 = v2 + v3 (§2-1 CNC ↔ RRM · §2-3 N9 · §8-2 D17) + v3.1 (§5 · §6) — 겹치면 뒤가 이긴다.
판정 = docs/reviews/codex_review_rint_g2_v3_20261007.md (RRM 은 시험 전용 해상 기준 · 생산 경로에 넣지 않는다).

⚠ 이 시험의 PASS 는 **기구 (RRM 면 가중 · 절단 tombstone · N9 원장 검사) 의 증거**다.  RRM 자체 오차 · CNC 편향 · T2/T3 수렴의
  검증이 아니다 (D12-V 수치 봉인 전 · 개발 판만 가능 · 판정문 §4 · §8).  D17 (원판 밖 = 절단 ↔ 재구성) = 권고 기본값 절단 · 1저자 확인 전.

  python3 scripts/test_rint_g2_rrm.py
  python3 scripts/test_rint_g2_rrm.py --s3 PATH    # 다른 step3_sigma 로 (고치기 전 기록용)

묶음:
  RRM-0  disc_rect_area — 원판 ∩ 직사각형 정확 면적 (안 · 밖 · 사분원 · 반원 · 분할 합 = π a²)
  RRM-1  contact_disc — 근축면 원판 (π a² = lens_geometry · 근축면 위 · 축 정렬 판정)
  RRM-2  rrm_plan — 해상 축 정렬 접점 (두꺼운 고정 브리지로 원판 밖 support) · 면 가중 = 면 ∩ 원판 · 원판 밖 = 절단 tombstone ·
         모든 S_c^surv 면이 정확히 한 번 · 기록 (iface_reference · D17 권고 기본값 · 1저자 확인 전)
  N9     reject_film_off_outside — 원판 밖 owner 쌍 면을 막 OFF (조화평균) 로 둔 변이 = 원장 검사가 거부 · 우회 G > 절단 G 기록
  RRM-3  적격성 — 기울기 (D11 미정) · 미해상 (a < k·h) · k 인자 필수
  RRM-4  r → 0 = OFF 아님 (원판 밖 절단이 남는다)
  RRM-5  생산 격리 (step3_sigma 가 이 모듈을 모른다 · 함수 객체 그대로)
  RRM-6  혼합 종류 (AM_S|AM_P · 반경 다름)
  ── RIMP-04 · 06 (Codex 10-14 · 판정문 §5 · §7 · 수정 계획 Q3 (가)) ──
  N9b    복합 변이 — 원판 밖 cut 행 삭제 + 기록 resolve_k 4→5 · + r 표 비움 · film rface NaN (cut 유지) · 음수 rface · k 만 바꿈 ·
         RRM 기록 없음 → rrm_check 위반 · rrm_require · rrm_solve 거부 (메타데이터로 검사 집합을 비울 수 없다) · 우회 σ 기록 (Codex 값) ·
         양성: 정상 계획 · 등록된 r = 0 계획 = 위반 없음
  RRM-7  표준 요약 = 실제 RRM 행 — film 67 · cut 85 · 순수 막 G (행 합 = 접점 기록) · CNC 값 = 별도 이름공간 (`iface_cnc_comparison`) ·
         반쪽 탄소 변형 (Codex: 행 37 · 42 · G 2.7535056597827278e−6 S ↔ CNC 2.612935414333538e−6 / 5.027420037705035e−6)
"""
import argparse
import ast
import contextlib
import importlib.util
import io
import math
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, 'scripts')
sys.path.insert(0, SCRIPTS)

S3 = None
S3_PATH = None
RRM = None
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


@contextlib.contextmanager
def direct_solver():
    """작은 픽스처 = 직접 풀이 (기계 정밀도) — 생산 경로 아님."""
    from scipy.sparse.linalg import spsolve
    old = S3._solve_cg
    S3._solve_cg = lambda L, b: (spsolve(L.tocsc(), b), 0)
    try:
        yield
    finally:
        S3._solve_cg = old


def raises(fn, exc=(ValueError, TypeError)):
    try:
        fn()
    except exc:
        return True
    return False


def te():
    return S3.electronic_sigma_table(0.010, 0.005, 100.0, 10.0, 250.0)


def codes(obj):
    return sorted(x['code'] for x in obj['rejections'])


# ═════════════════════════ 픽스처 ═════════════════════════
#  RRM_A — 해상 축 정렬 접점: R 1 µm 두 AM_S 구 · δ 0.167 µm → a ≈ 0.40003 µm · h 0.1 µm (a/h ≈ 4.0) · 두꺼운 고정 브리지 0.7 µm
#  (b > a — 원판 밖 support 를 일부러 만든다 · RINTG-02 의 support ≠ 참 원판 상황).  중심 x · y 를 셀 경계에서 비켜 둔다.
A_C = np.array([[1.03, 0.97, 1.0], [1.03, 0.97, 2.833]]); A_R = np.array([1.0, 1.0]); A_T = np.array([2, 2])
A_LO, A_HI, A_VOX, A_BR = (0.0, 0.0, 0.0), (2.0, 2.0, 3.833), 0.1, 0.7
#  RRM_B — 혼합 종류 · 반경 다름: AM_S R 1 · AM_P R 0.6 · δ 0.3 µm → a ≈ 0.4437 µm (≥ k·h 0.4)
#  (시험 먼저 커밋의 δ 0.2 는 a 0.371 < k·h 라 RRM 이 **옳게** 미해상 거부했다 — 픽스처 잘못 · 구현 아님 · 10-13 정정)
B_C = np.array([[1.03, 0.97, 1.0], [1.03, 0.97, 2.3]]); B_R = np.array([1.0, 0.6]); B_T = np.array([2, 1])
B_LO, B_HI = (0.0, 0.0, 0.0), (2.0, 2.0, 2.9)
#  기울기 접점 (중심선이 축과 어긋남 · D11 미정)
T_C = np.array([[1.0, 1.0, 1.0], [1.35, 1.0, 2.75]]); T_R = np.ones(2); T_T = np.array([2, 2])
T_LO, T_HI = (0.0, 0.0, 0.0), (2.4, 2.0, 3.8)
#  미해상 (Codex 1 단계 픽스처: R 1 · δ 0.02 → a 0.1411 µm · h 0.1)
U_C = np.array([[1., 1., 1.], [1., 1., 2.98]]); U_R = np.ones(2); U_T = np.array([2, 2])
U_LO, U_HI = (0.0, 0.0, 0.0), (2.0, 2.0, 3.98)
K_FIX = 4.0            # 해상 조건 a ≥ k·h 의 k — **픽스처 인자** (D12-V 숫자 아님 · 1저자 몫)
R_SS = 1.0e-3          # Ω·cm² — 픽스처 값 (재료값 아님 · [미확인])
RT = {'AM_S|AM_S': R_SS, 'AM_S|AM_P': 2.0e-3, 'AM_P|AM_P': 1.5e-3}


def bed(c, r, t, lo, hi, vox, bridge):
    sid, pid = S3.rasterize(c, r, t, None, None, lo, hi, vox, bridge_um=bridge)
    L = S3.am_iface_ledger(c, r, t, sid, sid, lo, vox, delta_bound_um=0.0, bridge_um=bridge)
    return sid, pid, L


def expected_faces(L, q):
    """원장에서 접점 q 의 S_c^surv 면 (축, 아래 셀 선형 번호) 집합 — 시험의 독립 대조용."""
    F = L['faces']
    m = (F['cid'] == q) & F['surv']
    return set(zip(F['axis'][m].tolist(), F['lin'][m].tolist()))


def rows_of(P):
    out = {}
    for ax, A in enumerate(P['axes']):
        for k in range(len(A['lin'])):
            out[(ax, int(A['lin'][k]))] = (bool(A['cut'][k]), float(A['rface'][k]), int(A['cid'][k]))
    return out


def with_rows(P, keep):
    """계획 행에서 keep(ax, lin, cut) 이 False 인 행을 뺀 변이 — 지문을 **다시 만든다** (생산 관문이 받는 모양 · N9 원장 검사만 가른다)."""
    Q = dict(P)
    axes = []
    for ax, A in enumerate(P['axes']):
        m = np.array([keep(ax, int(A['lin'][k]), bool(A['cut'][k])) for k in range(len(A['lin']))], bool)
        axes.append({k: (np.asarray(v)[m] if len(m) else np.asarray(v)) for k, v in A.items()})
    Q['axes'] = tuple(axes)
    Q['fp_rows'] = S3._iface_rows_fp(Q['axes'])
    Q['n_film_rows'] = int(sum(int((~a['cut']).sum()) for a in axes))
    Q['n_cut_rows'] = int(sum(int(a['cut'].sum()) for a in axes))
    return Q


def edit_row(P, sel, **vals):
    """sel(ax, lin) 인 행 하나의 값을 바꾼 변이 (지문 다시 만듦)."""
    Q = dict(P)
    axes = []
    done = False
    for ax, A in enumerate(P['axes']):
        A2 = {k: np.array(v, copy=True) for k, v in A.items()}
        for k in range(len(A2['lin'])):
            if not done and sel(ax, int(A2['lin'][k])):
                for kk, vv in vals.items():
                    A2[kk][k] = vv
                done = True
        axes.append(A2)
    Q['axes'] = tuple(axes)
    Q['fp_rows'] = S3._iface_rows_fp(Q['axes'])
    Q['n_film_rows'] = int(sum(int((~a['cut']).sum()) for a in axes))
    Q['n_cut_rows'] = int(sum(int(a['cut'].sum()) for a in axes))
    return Q, done


# ═════════════════════════ RRM-0 ═════════════════════════
@case('RRM-0 disc_rect_area — 원판 ∩ 직사각형 정확 면적')
def t_disc_rect():
    print('RRM-0 — 안 · 밖 · 사분원 · 반원 · 분할 합 (π a²) · 대칭')
    f = RRM.disc_rect_area
    a = 0.4
    chk('RRM-0 안쪽 정사각형 = h² (정확)', f(0.0, 0.0, a, -0.05, 0.05, -0.05, 0.05) == 0.1 * 0.1 or
        abs(f(0.0, 0.0, a, -0.05, 0.05, -0.05, 0.05) - 0.01) < 1e-17, repr(f(0.0, 0.0, a, -0.05, 0.05, -0.05, 0.05)))
    chk('RRM-0 바깥 정사각형 = 0 · 접하는 정사각형 = 0', f(0.0, 0.0, a, 0.5, 0.6, 0.0, 0.1) == 0.0
        and f(0.0, 0.0, a, 0.4, 0.5, -0.05, 0.05) == 0.0)
    chk('RRM-0 사분원 [c, c+L]² (L ≥ a) = π a²/4 (상대 1e−13)',
        abs(f(0.3, -0.2, a, 0.3, 1.0, -0.2, 0.6) - math.pi * a * a / 4) < 1e-13 * a * a)
    chk('RRM-0 반원 (직사각형이 원판 절반을 덮음) = π a²/2 (상대 1e−13)',
        abs(f(0.0, 0.0, a, 0.0, 2.0, -2.0, 2.0) - math.pi * a * a / 2) < 1e-13 * a * a)
    worst = 0.0
    for aa, h, (ox, oy) in ((0.4, 0.1, (0.013, 0.071)), (0.14106735979665894, 0.05, (0.0, 0.0)),
                            (0.6, 0.07, (0.031, 0.002)), (0.24, 0.02, (0.0049, 0.0151))):
        n = int(math.ceil(2 * aa / h)) + 3
        xs = ox - (n // 2 + 1) * h + np.arange(n + 3) * h
        s = sum(f(0.0, 0.0, aa, x0, x0 + h, y0, y0 + h) for x0 in xs for y0 in xs - ox + oy)
        worst = max(worst, abs(s / (math.pi * aa * aa) - 1.0))
    chk('RRM-0 평면 타일 분할 합 = π a² (네 경우 · 상대 1e−12 — 면 가중의 분할 성질)', worst < 1e-12, f'{worst:.2e}')
    v1 = f(0.1, 0.2, a, 0.25, 0.37, 0.05, 0.31); v2 = f(0.2, 0.1, a, 0.05, 0.31, 0.25, 0.37)
    v3 = f(-0.1, 0.2, a, -0.37, -0.25, 0.05, 0.31)
    chk('RRM-0 대칭: x ↔ y 교환 · x 반사 → 같은 면적 (상대 1e−14)', abs(v1 - v2) < 1e-14 * a * a and abs(v1 - v3) < 1e-14 * a * a,
        f'{v1!r} {v2!r} {v3!r}')


# ═════════════════════════ RRM-1 ═════════════════════════
@case('RRM-1 contact_disc — 근축면 원판')
def t_contact_disc():
    from lens_geometry import intersection_disc_area
    print('RRM-1 — π a² = lens_geometry · 근축면 위 (p_a = p_b) · 축 정렬 판정')
    ok_area, ok_plane = True, True
    for ra, rb, dl in ((1.0, 1.0, 0.167), (1.0, 0.6, 0.2), (1.0, 1.0, 0.02), (6.0, 2.0, 0.05)):
        ca = np.array([1.0, 2.0, 3.0]); cb = ca + np.array([0.0, 0.0, ra + rb - dl])
        D = RRM.contact_disc(ca, ra, cb, rb)
        A = intersection_disc_area(ra, rb, dl)
        ok_area &= abs(math.pi * D['a'] ** 2 / A - 1.0) < 1e-12
        pa = float(((D['p0'] - ca) ** 2).sum() - ra * ra); pb = float(((D['p0'] - cb) ** 2).sum() - rb * rb)
        ok_plane &= abs(pa - pb) < 1e-12 * ra * ra and D['axis'] == 2 and abs(np.linalg.norm(D['n']) - 1.0) < 1e-15
    chk('RRM-1 π a² = intersection_disc_area (네 경우 · 상대 1e−12)', ok_area)
    chk('RRM-1 원판 중심이 근축면 위 (p_a = p_b) · 법선 단위 · z 정렬 → axis 2', ok_plane)
    Dt = RRM.contact_disc(T_C[0], 1.0, T_C[1], 1.0)
    chk('RRM-1 기울기 중심선 → axis None (D11 미정)', Dt is not None and Dt['axis'] is None)
    chk('RRM-1 안 닿음 (δ < 0) · 포함 → None', RRM.contact_disc(np.zeros(3), 1.0, np.array([0, 0, 2.1]), 1.0) is None
        and RRM.contact_disc(np.zeros(3), 1.0, np.array([0, 0, 0.1]), 0.5) is None)


# ═════════════════════════ RRM-2 ═════════════════════════
@case('RRM-2 rrm_plan — 해상 축 정렬 · 원판 밖 = 절단 tombstone (D17 권고 기본값)')
def t_rrm_plan():
    print('RRM-2 — RRM_A (R 1 · δ 0.167 · h 0.1 · 고정 브리지 0.7) · r 1e−3 Ω·cm² (픽스처)')
    sid, pid, L = bed(A_C, A_R, A_T, A_LO, A_HI, A_VOX, A_BR)
    P = RRM.rrm_plan(L, RT, resolve_k=K_FIX)
    chk('RRM-2 거부 없음 · 계획 종류 = am_iface_plan (생산 솔버가 받는 행 모양) · 기록 iface_reference',
        P['rejections'] == [] and P['kind'] == 'am_iface_plan'
        and P['record'].get('iface_reference') == 'resolved_true_disc_v1', repr(codes(P)))
    E = expected_faces(L, 0)
    R_ = rows_of(P)
    W = RRM.rrm_face_weights(L, 0)
    wmap = {(int(a_), int(l_)): float(w_) for a_, l_, w_ in zip(W['axis'], W['lin'], W['w'])}
    n_out = sum(1 for k in E if wmap[k] == 0.0)
    n_in = sum(1 for k in E if wmap[k] > 0.0)
    chk(f'RRM-2 S_c^surv 면 {len(E)} = 행 집합 (정확히 한 번) · 원판 밖 {n_out} > 0 · 원판과 겹침 {n_in} > 0',
        set(R_) == E and set(wmap) == E and n_out > 0 and n_in > 0, f'{len(E)} {len(R_)} {n_out} {n_in}')
    h2 = A_VOX * A_VOX
    ok = all((R_[k][0] is True and R_[k][1] == 0.0) if wmap[k] == 0.0
             else (R_[k][0] is False and abs(R_[k][1] - R_SS * h2 / wmap[k]) <= 1e-12 * R_[k][1]) for k in E)
    chk('RRM-2 원판 밖 = 절단 tombstone (cut · r_face 0) · 원판과 겹침 = 막 r_face = r·h²/w (상대 1e−12)', ok)
    from lens_geometry import intersection_disc_area
    A = intersection_disc_area(1.0, 1.0, 0.167)
    G = float(S3.iface_plan_film_G_S(P)[0])
    sw = float(sum(wmap.values()))
    chk('RRM-2 ΣG_film = 1e−8·Σw/r (상대 1e−12) · Σw = π a² (원판 전부 owner 면이 덮음 — 덮임 = 1 · 상대 1e−12)',
        abs(G - 1e-8 * sw / R_SS) <= 1e-12 * G and abs(sw / A - 1.0) < 1e-12, f'{G!r} {sw!r} {A!r}')
    rec = P['record']
    rr = rec.get('iface_rrm') or {}
    chk('RRM-2 기록: D17 원판 밖 = 절단 · "권고 기본값 · 1저자 확인 전" · 해상 k = 픽스처 인자 (D12-V 아님) · 시험 전용 · 검증 PASS 아님',
        rr.get('outside_law') == 'cut' and '권고 기본값' in rr.get('outside_law_status', '')
        and '1저자 확인 전' in rr.get('outside_law_status', '') and rr.get('resolve_k') == K_FIX
        and 'D12-V' in rr.get('resolve_k_status', '') and '시험 전용' in rec.get('iface_status', '')
        and 'PASS 아님' in rec.get('iface_status', ''), repr(rr)[:300])
    c0 = (rr.get('contacts') or [{}])[0]
    chk('RRM-2 기록: 접점별 a · A_true · Σw · 덮임 · 면 수 (안 · 부분 · 밖)',
        abs(c0.get('a_um', 0) - math.sqrt(A / math.pi)) < 1e-12 and c0.get('n_faces_outside') == n_out
        and c0.get('n_faces_inside', 0) + c0.get('n_faces_partial', 0) == n_in and abs(c0.get('coverage', 0) - 1.0) < 1e-12,
        repr(c0))
    chk('RRM-2 N9 원장 검사 통과 (rrm_check 위반 0 · rrm_require 통과)',
        RRM.rrm_check(P, L) == [] and RRM.rrm_require(P, L) is P)
    kw = dict(z_bot_um=0.0, z_top_um=A_HI[2], return_field=True)
    with direct_solver():
        off = quiet(S3.solve_sigma_z, sid, te(), A_VOX, **kw)
        on = quiet(RRM.rrm_solve, sid, te(), A_VOX, P, L, **kw)
    chk('RRM-2 생산 솔버가 RRM 계획을 받는다 · 0 < σ_RRM < σ_OFF · 해 기록에 iface_reference',
        0.0 < on['sigma_eff'] < off['sigma_eff'] and on['iface'].get('iface_reference') == 'resolved_true_disc_v1',
        f"{on['sigma_eff']!r} {off['sigma_eff']!r}")


# ═════════════════════════ N9 ═════════════════════════
@case('N9 reject_film_off_outside — 원판 밖 owner 쌍 면을 막 OFF 로 둔 변이 거부 · 우회 G > 절단 G')
def t_n9():
    print('N9 — 원장 검사 (owner 쌍 면 = 막 행 또는 cut tombstone · 그 밖은 없다)')
    sid, pid, L = bed(A_C, A_R, A_T, A_LO, A_HI, A_VOX, A_BR)
    P = RRM.rrm_plan(L, RT, resolve_k=K_FIX)
    W = RRM.rrm_face_weights(L, 0)
    wmap = {(int(a_), int(l_)): float(w_) for a_, l_, w_ in zip(W['axis'], W['lin'], W['w'])}
    n_out = sum(1 for v in wmap.values() if v == 0.0)
    M = with_rows(P, lambda ax, lin, cut: not (cut and wmap.get((ax, lin), 1.0) == 0.0))   # 원판 밖 절단 행을 뺀다 = 조화평균 (막 OFF)
    V = RRM.rrm_check(M, L)
    vo = [v for v in V if v['code'] == 'film_off_outside']
    chk(f'N9 변이 (원판 밖 절단 {n_out} 행 제거 = 막 OFF) → 위반 film_off_outside n = {n_out} · rrm_require 거부',
        len(vo) == 1 and vo[0]['n'] == n_out and raises(lambda: RRM.rrm_require(M, L)), repr(V)[:300])
    chk('N9 범위 표지: 생산 관문 (iface_require_quantitative) 은 RRM 을 모른다 — 변이를 받는다 · N9 는 RRM 원장 검사가 맡는다',
        S3.iface_require_quantitative(M, sid, te()) is M)
    kw = dict(z_bot_um=0.0, z_top_um=A_HI[2], return_field=True)
    with direct_solver():
        off = quiet(S3.solve_sigma_z, sid, te(), A_VOX, **kw)
        s_cut = quiet(RRM.rrm_solve, sid, te(), A_VOX, P, L, **kw)['sigma_eff']
        s_mut = quiet(S3.solve_sigma_z, sid, te(), A_VOX, iface=M, **kw)['sigma_eff']   # 원장 검사를 우회해 크기만 잰다
    print(f'    기록 (개발 픽스처 · 재료값 아님): σ_cut {s_cut:.10g} · σ_막OFF우회 {s_mut:.10g} · σ_OFF {off["sigma_eff"]:.10g} S/cm · '
          f'우회/절단 = {s_mut / s_cut:.6f}')
    chk('N9 우회 G (원판 밖 막 OFF) > 절단 G (RRM) — σ_cut < σ_우회 < σ_OFF (같은 그래프 · Rayleigh)',
        s_cut < s_mut < off['sigma_eff'], f'{s_cut} {s_mut} {off["sigma_eff"]}')
    with direct_solver():
        chk('N9 rrm_solve 는 변이를 거부한다 (원장 검사가 솔브 앞)', raises(lambda: quiet(RRM.rrm_solve, sid, te(), A_VOX, M, L, **kw)))
    k_in = next(k for k, v in wmap.items() if v > 0.0)
    k_ou = next(k for k, v in wmap.items() if v == 0.0)
    M2 = with_rows(P, lambda ax, lin, cut: (ax, lin) != k_in)
    chk('N9 변이: 원판과 겹친 면 하나 제거 → film_off_inside', any(v['code'] == 'film_off_inside' for v in RRM.rrm_check(M2, L)))
    M3, d3 = edit_row(P, lambda ax, lin: (ax, lin) == k_ou, cut=False, rface=R_SS, ck=S3.SID_IFACE_AM['AM_S|AM_S'])
    chk('N9 변이: 원판 밖 면에 막 (절단 대신) → outside_not_cut', d3 and any(v['code'] == 'outside_not_cut' for v in RRM.rrm_check(M3, L)))
    M4, d4 = edit_row(P, lambda ax, lin: (ax, lin) == k_in, rface=2.0 * R_SS * A_VOX ** 2 / wmap[k_in])
    chk('N9 변이: 막 r_face × 2 (지문 다시 만듦) → rface_mismatch', d4 and any(v['code'] == 'rface_mismatch' for v in RRM.rrm_check(M4, L)))
    M5, d5 = edit_row(P, lambda ax, lin: (ax, lin) == k_in, cut=True, rface=0.0, ck=0)
    chk('N9 변이: 원판과 겹친 면을 절단 → inside_cut', d5 and any(v['code'] == 'inside_cut' for v in RRM.rrm_check(M5, L)))
    M6 = dict(P); M6['axes'] = tuple(dict(a) for a in P['axes'])
    M6['axes'][2]['rface'] = M6['axes'][2]['rface'] * 1.0 + 0.0
    M6['axes'][2]['rface'][0] = M6['axes'][2]['rface'][0] + 1.0                         # 지문 안 고침 (사후 변조)
    chk('N9 사후 변조 (지문 그대로) → rrm_check 가 fp_rows 위반', any(v['code'] == 'fp_rows' for v in RRM.rrm_check(M6, L)))


# ═════════════════════════ RRM-3 ═════════════════════════
@case('RRM-3 적격성 — 기울기 (D11) · 미해상 (a < k·h) · k 필수')
def t_eligible():
    print('RRM-3 — 기준 주장에서 빼는 접점은 거부 (조용히 CNC 로 돌아가지 않는다)')
    sid, _, L = bed(T_C, T_R, T_T, T_LO, T_HI, 0.1, 0.24)
    P = RRM.rrm_plan(L, RT, resolve_k=K_FIX)
    chk('RRM-3 기울기 접점 → rrm_unsupported_tilt 거부 (D11 = T2 결과 전) · 솔브 거부',
        'rrm_unsupported_tilt' in codes(P) and raises(lambda: quiet(S3.solve_sigma_z, sid, te(), 0.1, iface=P)), repr(codes(P)))
    sid, _, L = bed(U_C, U_R, U_T, U_LO, U_HI, 0.1, 0.24)
    P = RRM.rrm_plan(L, RT, resolve_k=K_FIX)
    rr = P['record'].get('iface_rrm') or {}
    chk('RRM-3 미해상 (a 0.141 < k·h 0.4) → rrm_unresolved_subgrid 거부 · 기록 unresolved_subgrid 수',
        'rrm_unresolved_subgrid' in codes(P) and rr.get('n_unresolved_subgrid') == 1, repr(codes(P)))
    _, _, L = bed(A_C, A_R, A_T, A_LO, A_HI, A_VOX, A_BR)
    chk('RRM-3 resolve_k 없음 → TypeError (기본값 없음 · D12-V 숫자를 지어내지 않는다)',
        raises(lambda: RRM.rrm_plan(L, RT), (TypeError,)))
    chk('RRM-3 resolve_k ≤ 0 · 비유한 → ValueError', raises(lambda: RRM.rrm_plan(L, RT, resolve_k=0.0), (ValueError,))
        and raises(lambda: RRM.rrm_plan(L, RT, resolve_k=float('nan')), (ValueError,)))


# ═════════════════════════ RRM-4 ═════════════════════════
@case('RRM-4 r → 0 — OFF 아님 (원판 밖 절단이 남는다)')
def t_r0():
    print('RRM-4 — r 0 의 RRM = 절단만 남은 그래프 (OFF 보다 작다)')
    sid, _, L = bed(A_C, A_R, A_T, A_LO, A_HI, A_VOX, A_BR)
    P0 = RRM.rrm_plan(L, {'AM_S|AM_S': 0.0}, resolve_k=K_FIX)
    Pc = with_rows(P0, lambda ax, lin, cut: cut)                                          # 절단 행만
    kw = dict(z_bot_um=0.0, z_top_um=A_HI[2], return_field=True)
    with direct_solver():
        off = quiet(S3.solve_sigma_z, sid, te(), A_VOX, **kw)['sigma_eff']
        s0 = quiet(RRM.rrm_solve, sid, te(), A_VOX, P0, L, **kw)['sigma_eff']
        sc = quiet(S3.solve_sigma_z, sid, te(), A_VOX, iface=Pc, **kw)['sigma_eff']
    chk('RRM-4 σ(RRM, r 0) < σ_OFF · = 절단 행만 둔 계획 (상대 1e−12)', s0 < off and abs(s0 / sc - 1.0) < 1e-12,
        f'{s0!r} {sc!r} {off!r}')


# ═════════════════════════ RRM-5 ═════════════════════════
@case('RRM-5 생산 격리 — step3_sigma · payload 가 RRM 을 모른다')
def t_isolation():
    print('RRM-5 — 생산 경로에 RRM 없음 (AST) · 함수 객체 그대로 · 상태 표지')
    for rel in ('scripts/step3_sigma.py', 'scripts/mpm_webapp_payload.py', 'scripts/run_contract.py'):
        src = open(os.path.join(ROOT, rel), encoding='utf-8').read()
        tree = ast.parse(src)
        names = set()
        for n in ast.walk(tree):
            if isinstance(n, ast.Import):
                names |= {a.name for a in n.names}
            elif isinstance(n, ast.ImportFrom):
                names.add(n.module or '')
        chk(f'RRM-5 {rel} 가 rint_rrm_reference 를 import 하지 않는다 · 문자열도 없음',
            'rint_rrm_reference' not in names and 'rint_rrm_reference' not in src)
    chk('RRM-5 RRM 모듈 import 뒤에도 step3_sigma 함수 객체 그대로 (몽키패치 없음)',
        RRM.S3.solve_sigma_z is RRM._S3_FN_IDS['solve_sigma_z'] and RRM.S3.am_iface_plan is RRM._S3_FN_IDS['am_iface_plan'])
    tree = ast.parse(open(os.path.join(SCRIPTS, 'rint_rrm_reference.py'), encoding='utf-8').read())
    bad = []
    for n in ast.walk(tree):
        tg = n.targets if isinstance(n, ast.Assign) else ([n.target] if isinstance(n, (ast.AugAssign, ast.AnnAssign)) else [])
        bad += [t.attr for t in tg if isinstance(t, ast.Attribute) and isinstance(t.value, ast.Name)
                and t.value.id in ('S3', 'step3_sigma')]
        if isinstance(n, ast.Call) and getattr(n.func, 'id', None) == 'setattr' and n.args \
                and isinstance(n.args[0], ast.Name) and n.args[0].id in ('S3', 'step3_sigma'):
            bad.append('setattr')
    chk('RRM-5 (AST) RRM 모듈이 step3_sigma 속성에 대입하지 않는다 (S3.x = … · setattr 없음)', not bad, repr(bad))
    chk('RRM-5 상태 문구: 시험 전용 · 생산 경로 아님 · 검증 PASS 아님 · D12-V 봉인 전',
        all(s in RRM.RRM_STATUS for s in ('시험 전용', '생산 경로 아님', 'PASS 아님', 'D12-V')))


# ═════════════════════════ RRM-6 ═════════════════════════
@case('RRM-6 혼합 종류 · 반경 다름 (AM_S|AM_P)')
def t_mixed():
    print('RRM-6 — RRM_B (AM_S R 1 · AM_P R 0.6 · δ 0.3 · 고정 브리지 0.7)')
    sid, _, L = bed(B_C, B_R, B_T, B_LO, B_HI, A_VOX, A_BR)
    P = RRM.rrm_plan(L, RT, resolve_k=K_FIX)
    W = RRM.rrm_face_weights(L, 0)
    wmap = {(int(a_), int(l_)): float(w_) for a_, l_, w_ in zip(W['axis'], W['lin'], W['w'])}
    R_ = rows_of(P)
    ok = set(R_) == set(wmap) and all(
        (R_[k][0] and R_[k][1] == 0.0) if w == 0.0 else (not R_[k][0] and abs(R_[k][1] - 2.0e-3 * A_VOX ** 2 / w) <= 1e-12 * R_[k][1])
        for k, w in wmap.items())
    chk('RRM-6 거부 없음 · 종류 키 AM_S|AM_P 의 r · 행 = 면 가중 규칙 · 원장 검사 통과',
        P['rejections'] == [] and ok and set(R_) == set(wmap) and RRM.rrm_check(P, L) == []
        and str(L['contacts']['type_key'][0]) == 'AM_S|AM_P', repr(codes(P)))


# ═════════════════════════ N9b (RIMP-04) ═════════════════════════
def _deep(P):
    """계획 깊은 사본 — 원장 (P['ledger']) 은 공유 (읽기만 · 변이는 행 · 기록에만)."""
    import copy
    Q = {k: (v if k == 'ledger' else copy.deepcopy(v)) for k, v in P.items()}
    return Q


@case('N9b 복합 변이 — 메타데이터 · NaN (RIMP-04 · Codex 10-14 판정문 §5)')
def t_n9b():
    print('N9b — 원판 밖 cut 85 행 삭제 + 기록 변조 · film rface NaN — 의미 검사가 메타데이터를 믿지 않는다 (판정문 §5 표)')
    sid, pid, L = bed(A_C, A_R, A_T, A_LO, A_HI, A_VOX, A_BR)
    P = RRM.rrm_plan(L, RT, resolve_k=K_FIX)
    kw = dict(z_bot_um=0.0, z_top_um=A_HI[2], return_field=True)
    chk('N9b 픽스처 = Codex: film 67 · cut 85 · 정상 계획 위반 없음', P['n_film_rows'] == 67 and P['n_cut_rows'] == 85
        and RRM.rrm_check(P, L) == [], f"{P['n_film_rows']} {P['n_cut_rows']}")
    M = with_rows(P, lambda ax, lin, cut: not cut)                                   # Codex: cut 85 행만 삭제 (지문 다시 만듦)
    muts = {}
    q = _deep(M); q['record']['iface_rrm']['resolve_k'] = 5.0
    muts['cut 삭제 + 기록 resolve_k 4→5'] = q
    q = _deep(M); q['record']['iface_r_type_ohm_cm2'] = {}
    muts['cut 삭제 + 기록 r 표 비움'] = q
    q = _deep(P)
    for ax in q['axes']:
        ax['rface'][~ax['cut']] = np.nan
    q['fp_rows'] = S3._iface_rows_fp(q['axes'])
    muts['cut 유지 + film 67 행 rface NaN'] = q
    q = _deep(P)
    for ax in q['axes']:
        ax['rface'][~ax['cut']] = -ax['rface'][~ax['cut']]
    q['fp_rows'] = S3._iface_rows_fp(q['axes'])
    muts['film rface 음수'] = q
    q = _deep(P); q['record']['iface_rrm']['resolve_k'] = 5.0
    muts['행 그대로 + 기록 resolve_k 만 4→5 (재계산하면 미해상 거부)'] = q
    q = _deep(P); q['record'].pop('iface_rrm')
    muts['RRM 기록 (iface_rrm) 삭제'] = q
    for tag, Q in muts.items():
        V = RRM.rrm_check(Q, L)
        with direct_solver():
            refused = raises(lambda Q=Q: quiet(RRM.rrm_solve, sid, te(), A_VOX, Q, L, **kw))
        chk(f'N9b {tag} → rrm_check 위반 > 0 · rrm_require 거부 · rrm_solve 거부 (고치기 전 = 위반 없음 · 풀이)',
            len(V) > 0 and raises(lambda Q=Q: RRM.rrm_require(Q, L)) and refused, repr([x['code'] for x in V]))
    #  우회 크기 (기록) — 일반 솔버는 RRM 을 모른다 (설계 · 공개된 범위) · Codex 값 재현
    with direct_solver():
        s_k = quiet(S3.solve_sigma_z, sid, te(), A_VOX, iface=muts['cut 삭제 + 기록 resolve_k 4→5'], **kw)['sigma_eff']
        s_n = quiet(S3.solve_sigma_z, sid, te(), A_VOX, iface=muts['cut 유지 + film 67 행 rface NaN'], **kw)
        s_0 = quiet(RRM.rrm_solve, sid, te(), A_VOX, P, L, **kw)['sigma_eff']
    print(f'    기록 (픽스처 · 재료값 아님): σ_RRM {s_0!r} · 우회 (cut 삭제) {s_k!r} · NaN rface {s_n["sigma_eff"]!r} S/cm · '
          f'NaN 해 unconverged {s_n["unconverged"]} · 잔차 {s_n["resid"]:.3e}')
    chk('N9b 기록: 막아야 할 우회 크기 = Codex 값 (σ_RRM 0.003334457143882423 · 우회 0.0040840140889134725 · NaN 0.0037299595666211234 · 상대 1e−9) '
        '— 작은 잔차가 틀린 조립을 구제하지 않는다 (NaN 해 unconverged False)',
        abs(s_0 / 0.003334457143882423 - 1) < 1e-9 and abs(s_k / 0.0040840140889134725 - 1) < 1e-9
        and abs(s_n['sigma_eff'] / 0.0037299595666211234 - 1) < 1e-9 and s_n['unconverged'] is False, f'{s_0} {s_k} {s_n["sigma_eff"]}')
    #  양성 — 등록된 r = 0 경로 (막 행 rface 0 · 절단 남음) 는 허용
    P0 = RRM.rrm_plan(L, {'AM_S|AM_S': 0.0}, resolve_k=K_FIX)
    chk('N9b 양성: 등록된 r = 0 계획 (막 행 rface 0) = 위반 없음 · 정상 계획 = 위반 없음',
        RRM.rrm_check(P0, L) == [] and RRM.rrm_check(P, L) == [], repr([x['code'] for x in RRM.rrm_check(P0, L)]))


# ═════════════════════════ RRM-7 (RIMP-06) ═════════════════════════
@case('RRM-7 표준 요약 = 실제 RRM 행 (RIMP-06 · Codex 10-14 판정문 §7)')
def t_rrm_summary():
    print('RRM-7 — RRM 계획 · 풀이 기록의 표준 원장 · 탄소 법칙 · 균일 r_face 가 CNC 값으로 남지 않는다 (CNC = 별도 이름공간)')
    sid, pid, L = bed(A_C, A_R, A_T, A_LO, A_HI, A_VOX, A_BR)
    P = RRM.rrm_plan(L, RT, resolve_k=K_FIX)
    rec = P['record']
    cl = rec.get('iface_contact_ledger') or {}
    G = float(S3.iface_plan_film_G_S(P).sum())
    c0 = (rec.get('iface_rrm') or {}).get('contacts', [{}])[0]
    chk('RRM-7 표준 원장 행 수 = 실제 RRM 행: film_faces.active 67 = n_film_rows · cut_faces 85 = n_cut_rows (고치기 전 = 152 · 0)',
        (cl.get('film_faces') or {}).get('active') == P['n_film_rows'] == 67 and cl.get('cut_faces') == P['n_cut_rows'] == 85,
        repr({k: cl.get(k) for k in ('film_faces', 'cut_faces')}))
    gt = cl.get('film_G_S_total') or {}
    chk('RRM-7 표준 순수 막 G = 행 합 ΣG (iface_plan_film_G_S) = iface_rrm.contacts[0].film_G_S (상대 1e−12) · 키 = rrm (CNC 판 이름 아님)',
        set(gt) == {'rrm'} and abs(gt['rrm'] / G - 1) < 1e-12 and abs(c0.get('film_G_S', 0) / G - 1) < 1e-12, repr(gt))
    cnc = rec.get('iface_cnc_comparison') or {}
    chk('RRM-7 탄소 법칙 표지: iface_carbon_cover ≠ CNC 이름 (RRM 은 탄소 가림 법칙 미사용) · CNC 값 = iface_cnc_comparison (active 152 · cut 0 · 표지)',
        rec.get('iface_carbon_cover') not in ('remove_area', 'renormalize')
        and ((cnc.get('iface_contact_ledger') or {}).get('film_faces') or {}).get('active') == 152
        and (cnc.get('iface_contact_ledger') or {}).get('cut_faces') == 0 and 'CNC' in str(cnc.get('meaning', '')),
        repr(rec.get('iface_carbon_cover')) + repr(list(cnc)))
    chk('RRM-7 계획 최상위 균일 rface_c (CNC) 가 RRM 계획의 값으로 남지 않는다 — CNC 비교값 안으로',
        P.get('rface_c') is None and 'rface_c' in (P.get('cnc_comparison') or {}), repr(type(P.get('rface_c'))))
    #  반쪽 탄소 변형 (Codex `geometry()` carbon_half — AM 셀의 왼쪽 절반을 탄소 sid 3 으로)
    sid0, _, _L0 = bed(A_C, A_R, A_T, A_LO, A_HI, 0.1, 0.7)
    csid = sid0.copy()
    csid[:10, :, :][np.isin(csid[:10, :, :], (1, 2))] = 3
    Lc = S3.am_iface_ledger(A_C, A_R, A_T, csid, sid0, A_LO, 0.1, delta_bound_um=0.0, bridge_um=0.7)
    Pc = RRM.rrm_plan(Lc, RT, resolve_k=K_FIX)
    Gc = float(S3.iface_plan_film_G_S(Pc).sum())
    clc = Pc['record'].get('iface_contact_ledger') or {}
    cncc = (Pc['record'].get('iface_cnc_comparison') or {}).get('iface_contact_ledger') or {}
    chk('RRM-7 반쪽 탄소: 행 37 · 42 · RRM ΣG 2.7535056597827278e−6 S (Codex · 1e−12) = 표준 film_G_S_total.rrm · '
        'CNC 비교값 remove_area 2.612935414333538e−6 · renormalize 5.027420037705035e−6 (비교 이름공간에만)',
        Pc['n_film_rows'] == 37 and Pc['n_cut_rows'] == 42 and abs(Gc / 2.7535056597827278e-6 - 1) < 1e-12
        and abs((clc.get('film_G_S_total') or {}).get('rrm', 0) / Gc - 1) < 1e-12
        and abs((cncc.get('film_G_S_total') or {}).get('remove_area', 0) / 2.612935414333538e-6 - 1) < 1e-12
        and abs((cncc.get('film_G_S_total') or {}).get('renormalize', 0) / 5.027420037705035e-6 - 1) < 1e-12
        and RRM.rrm_check(Pc, Lc) == [], f"{Pc['n_film_rows']} {Pc['n_cut_rows']} {Gc!r} {clc.get('film_G_S_total')}")
    with direct_solver():
        res = quiet(RRM.rrm_solve, sid, te(), A_VOX, P, L, z_bot_um=0.0, z_top_um=A_HI[2], return_field=True)
    rcl = res['iface'].get('iface_contact_ledger') or {}
    chk('RRM-7 풀이 기록: 표준 원장 = RRM 행 (summary_source 표지 · film_faces.active 67) · 쓴 막 행 ≤ 67 · CNC 비교값 = 따로 실림',
        'rrm' in str(rcl.get('summary_source', '')) and (rcl.get('film_faces') or {}).get('active') == 67
        and 0 < rcl.get('n_film_rows_used', -1) <= 67 and 'iface_cnc_comparison' in res['iface'],
        repr({k: rcl.get(k) for k in ('summary_source', 'n_film_rows_used')}))


def main():
    global S3, S3_PATH, RRM
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--s3', default=os.path.join(SCRIPTS, 'step3_sigma.py'))
    a = ap.parse_args()
    S3_PATH = os.path.abspath(a.s3)
    spec = importlib.util.spec_from_file_location('step3_sigma', S3_PATH)
    S3 = importlib.util.module_from_spec(spec)
    sys.modules['step3_sigma'] = S3                     # RRM 모듈이 같은 객체를 import 하게 (시험 대상 = 한 모듈)
    spec.loader.exec_module(S3)
    print(f'step3_sigma = {S3_PATH}')
    try:
        import rint_rrm_reference as _R
        RRM = _R
    except Exception as e:                              # noqa: BLE001 — 고치기 전 (모듈 없음) 도 사례 단위로 기록
        print(f'  (rint_rrm_reference import 실패: {type(e).__name__}: {e})')
        RRM = None
    for tag, fn in CASES:
        print(f'\n── {tag}')
        try:
            if RRM is None:
                raise ImportError('rint_rrm_reference 없음')
            fn()
        except Exception as e:                          # noqa: BLE001
            chk(f'{tag}: 실행', False, f'{type(e).__name__}: {e}')
    print(f'\n{_ok} PASS · {len(_fail)} FAIL')
    if _fail:
        for n in _fail:
            print('  -', n)
        sys.exit(1)


if __name__ == '__main__':
    main()
