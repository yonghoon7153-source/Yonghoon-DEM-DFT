#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rint G2 ①′ AM–AM 계면 막 — 계약 v3.1 시험 (반례 먼저 · 규율 ② · 2026-10-07).

정본 계약 = docs/reviews/contact_resistance_pipeline_draft_v2_20261006.md + …_v3_20261006.md + …_v3_1_20261007.md
(겹치면 뒤가 이긴다) · 판정 docs/reviews/codex_review_rint_g2_v3_20261007.md (계약 정정 둘 뒤 AM–AM ①′ 구현 GO ·
정량 채택 · 생산 HOLD) · 반례 수치 = docs/reviews/codex_rint_g2_v3_review_evidence_20261007/ (`evidence_v3.json` ·
`evidence.json`).  ⚠ 이 시험의 PASS 는 **계약 · 구현의 증거**이지 ①′ 정량 채택 · 검증 (T2/T3 · D12-V) 의 증거가 아니다.

  python3 scripts/test_rint_g2_am_iface.py                  # 현 구현
  python3 scripts/test_rint_g2_am_iface.py --s3 PATH         # 다른 step3_sigma (예: 고치기 전 blob) 로 — 실패 기록용

묶음 (원장):
  RINTV-01  T0-1e owner_eps_set · N8b reject_concentric · N8 reject_dup · ε_p 봉인
  RINTV-02  T0-1d raw_perm_mask_diag (3170 ↔ 3171 · 실제 rasterize) · T0-1′ own_perm_frozen ⓐⓑⓒⓓ · T0-1g mask_claimed
  I2        T0-5′ off_bitid (입력 순서마다 legacy · 막 0 + 예외 융합) · 옛 raster 지문 (rasterize 리팩터 비트 같음)
  단위      T1-4′ units_direct_vs_face (같은 리드) · T1-11 units_atrue (1e−8·A_true/r)
  탄소      T1-10 carbon_cover_law (막 소자만 2 Ω/1 Ω · raster N_c^0 · N_c^surv)
  E4′       T0-3′ class_sensitivity (에너지 · 중심 로그 FD · h 둘 · 혼합 σ · 판) · T0-3m e4_printed_mutant · T0-3i multiclass_integral
  거부      N2 · N3 · N4 · N6 · N7 · 채널 · 거부 계획 → 솔브 거부
  원장      T0-6b ledger_integrity (변조 · 끼워 넣기 거부) · E2 진단이 원장을 읽는다 (AST) · 기록 필드 · PROTOCOL_FIELDS 밖
  보류      N9 (RRM) · T2 · T3 · D12-V · T4-1 · T4-3 · N1 · N5′ · 직접 R_j 간선 (②) — 이 묶음 밖 (PENDING 줄로 표시)
"""
import argparse
import ast
import contextlib
import importlib.util
import io
import itertools
import math
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, 'scripts')
sys.path.insert(0, SCRIPTS)

S3 = None                       # main() 이 채운다 (기본 = scripts/step3_sigma.py · --s3 로 바꿀 수 있다)
S3_PATH = None
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
    """작은 픽스처 = 직접 풀이 (기계 정밀도 · v2 §3-11) — 조립 · 항등식을 CG 허용오차 없이 본다.  생산 경로 아님."""
    from scipy.sparse.linalg import spsolve
    old = S3._solve_cg
    S3._solve_cg = lambda L, b: (spsolve(L.tocsc(), b), 0)
    try:
        yield
    finally:
        S3._solve_cg = old


def te():
    return S3.electronic_sigma_table(0.010, 0.005, 100.0, 10.0, 250.0)


def raster(c, r, t, lo, hi, vox, bridge_um=0.24, add=None, ph=None, tol=0.10, **kw):
    sid, pid = S3.rasterize(c, r, t, add, ph, lo, hi, vox, bridge_um=bridge_um, tol_am_um=tol, **kw)
    sid_pre, _ = S3.rasterize(c, r, t, None, None, lo, hi, vox, bridge_um=bridge_um, tol_am_um=tol)
    return sid, pid, sid_pre


def ledger(c, r, t, sid, sid_pre, lo, vox, bridge_um=0.24, db=0.0, **kw):
    return S3.am_iface_ledger(c, r, t, sid, sid_pre, lo, vox, delta_bound_um=db, bridge_um=bridge_um, **kw)


def led_sig(L):
    """원장의 canonical 부분 (입력 순서와 무관해야 하는 것) → 비교용 바이트."""
    if L['owner'] is None:
        return ('rejected', tuple(x['code'] for x in L['rejections']))
    out = [L['owner'].tobytes()]
    for grp in ('contacts', 'faces'):
        for k in sorted(L[grp]):
            v = np.asarray(L[grp][k])
            out.append((grp, k, v.dtype.str, v.shape, v.tobytes()))
    out.append(tuple(sorted(x['code'] for x in L['rejections'])))
    return tuple(out)


def plan_sig(P):
    return tuple((k, np.asarray(ax[k]).tobytes()) for ax in P['axes'] for k in sorted(ax))


def codes(obj):
    return sorted(x['code'] for x in obj['rejections'])


def raises(fn, exc=(ValueError, TypeError)):
    try:
        fn()
    except exc:
        return True
    return False


def gl_nodes(n):
    x, w = np.polynomial.legendre.leggauss(n)
    return 0.5 * (x + 1.0), 0.5 * w


# ═════════════════════════ 픽스처 (판정문 · 증거 리터럴) ═════════════════════════
#  RINTG-01 (Codex G2 판정 · evidence.json:actual_raster_order) — 혼합 종류 두 구
CODEX_C = np.array([[1., 1., 1.], [1., 1., 2.9]]); CODEX_R = np.ones(2); CODEX_T = np.array([2, 1])
CODEX_LO, CODEX_HI, CODEX_VOX = (0.0, 0.0, 0.0), (2.0, 2.0, 3.9), 0.1
#  RINTV-02 (Codex v3 판정 §3 · evidence_v3.json:fixed_bridge_AM_mask_permutation) — 판정문 인쇄 리터럴
V02_C = np.array([[1.9748831001799223, 1.8791293045780670, 1.7896943576126298],
                  [1.0611990064053260, 0.8549090548944595, 1.7364778658264648]])
V02_R = np.array([0.5348361452776790, 0.8437277367739292]); V02_T = np.array([2, 1])
V02_LO, V02_HI, V02_VOX = (0.0, 0.0, 0.0), (3.2, 3.2, 3.2), 0.1
#  RINTV-01 (Codex v3 판정 §2 · evidence_v3.json:epsilon_tie) — 세 청구자 (관측점 기준 상대 중심) · ε_p 1e−6 µm²
EPS_FIX = 1e-6
EPS_POW = np.array([-1 + 1.5 * EPS_FIX, -1 + 0.75 * EPS_FIX, -1.0])
EPS_REL = np.array([[0., 0., 0.], [1., 0., 0.], [2., 0., 0.]])
EPS_RAD = np.sqrt((EPS_REL ** 2).sum(axis=1) - EPS_POW)
#  ⓑ 세 구 (혼합 종류 · 겹침 + 브리지가 셋째 구 근처) — 판정문에 형상 없음 → 여기서 고정 (v3.1 §4)
TRI_C = np.array([[1.0, 1.0, 1.0], [1.0, 1.0, 2.55], [1.0, 1.7, 1.78]])
TRI_R = np.array([0.8, 0.8, 0.6]); TRI_T = np.array([2, 1, 2])
TRI_LO, TRI_HI, TRI_VOX = (0.0, 0.0, 0.0), (2.0, 2.6, 3.4), 0.1
#  T0-3′ 두 부류 사슬 (AM_S–AM_S · AM_S–AM_P · 혼합 σ · 판에 닿음)
CH_C = np.array([[1., 1., 1.], [1., 1., 2.95], [1., 1., 4.9]]); CH_R = np.ones(3); CH_T = np.array([2, 2, 1])
CH_LO, CH_HI = (0.0, 0.0, 0.0), (2.0, 2.0, 5.9)
CH_RT = {'AM_S|AM_S': 1.0e-3, 'AM_S|AM_P': 2.0e-3, 'AM_P|AM_P': 1.5e-3}


def fx_codex(perm):
    perm = list(perm)
    return CODEX_C[perm], CODEX_R[perm], CODEX_T[perm]


# ═════════════════════════════════ RINTV-01 ═════════════════════════════════
def old_pairwise_fold(cell, rank, part, p, eps):
    """v3 I8 를 쌍 비교기로 읽은 **옛 규칙** (판별력 대조용 변이) — |Δp| ≤ ε 이면 canonical 키, 아니면 작은 power,
    항목 순서대로 fold (승자의 power 를 다음 비교 기준으로)."""
    cell = np.asarray(cell); rank = np.asarray(rank); p = np.asarray(p)
    starts = np.flatnonzero(np.r_[True, cell[1:] != cell[:-1]])
    ends = np.r_[starts[1:], len(cell)]
    own = []
    for s_, e_ in zip(starts, ends):
        w = s_
        for k in range(s_ + 1, e_):
            if abs(p[w] - p[k]) <= eps:
                w = w if rank[w] < rank[k] else k
            else:
                w = w if p[w] < p[k] else k
        own.append(rank[w])
    z = np.zeros(len(starts), np.int64)
    return cell[starts], np.asarray(own, np.int64), z, z


@case('T0-1e owner_eps_set (RINTV-01 · v3.1 §1 I8′)')
def t_owner_eps_set():
    print('T0-1e owner_eps_set — 세 청구자 · 6 순열 · ε_p = 1e−6 µm² (픽스처 인자 · 생산 ε_p 아님)')
    rank = np.array([0, 1, 2])                          # 중심 사전순 = 0 · 1 · 2 (증거 그대로)
    cells = np.zeros(3, np.int64)
    #  판별력 먼저 (새 API 없이 돈다 — 고치기 전 코드에서도 이 줄은 결과를 낸다)
    wins_old = {int(old_pairwise_fold(cells, rank[list(p_)], np.array(p_), EPS_POW[list(p_)], EPS_FIX)[1][0])
                for p_ in itertools.permutations(range(3))}
    chk('T0-1e (판별력) 옛 쌍별 fold 는 순서마다 승자가 다르다 ({0, 1, 2} — 순열 불변 단언이 실패해야 한다)',
        wins_old == {0, 1, 2}, repr(wins_old))
    wins_new, bands = set(), set()
    for perm in itertools.permutations(range(3)):
        perm = list(perm)
        _, own, band, ncl = S3._iface_owner_select(cells, rank[perm], np.array(perm), EPS_POW[perm], EPS_FIX)
        wins_new.add(int(own[0])); bands.add(int(band[0]))
    chk('T0-1e I8′ 집합 규칙: 6 순열 모두 주인 1 · 띠 크기 2 (T = {1, 2})', wins_new == {1} and bands == {2},
        f'{wins_new} {bands}')
    chk('T0-1e 봉인: 생산 ε_p = 1e−9 µm² · 규칙 이름 · power 평가 규약 이름',
        S3.IFACE_EPS_P_UM2 == 1e-9 and S3.IFACE_TIE_RULE == 'global_pmin_eps_band_center_lex_v1'
        and S3.IFACE_POWER_EVAL.startswith('cell_centre') and S3.IFACE_OWNER_RULE == 'claimant_power_partition_v1')
    #  fail-closed — 띠 안에 같은 canonical 키 (같은 중심) 둘
    chk('T0-1e fail-closed: 띠 안에 같은 canonical 키 두 입자 → 오류 (반경 · 종류 · 행 번호로 가르지 않는다)',
        raises(lambda: S3._iface_owner_select(np.zeros(2, np.int64), np.array([0, 0]), np.array([0, 1]),
                                              np.array([-1.0, -1.0 + 0.5e-6]), 1e-6)))


@case('N8b reject_concentric · N8 reject_dup (RINTV-01)')
def t_reject_concentric_dup():
    print('N8b · N8 — 동심 비동일 · 정확 중복 = 정량 거부 (입력 단계 · 종류 같음 · 다름 · 두 순서)')
    lo, hi, vox = (-1.5, -1.5, -1.5), (1.6, 1.6, 1.6), 0.1
    r_in = np.array([1.0, 1.0000002499999687])          # power 차 5.0e−7 µm² (ε 1e−6 안 · 판정문 리터럴)
    r_out = np.array([1.0, 1.3])                         # 띠 밖 동심 쌍
    for lbl, rr in (('띠 안', r_in), ('띠 밖', r_out)):
        for tt in (np.array([2, 2]), np.array([2, 1])):
            for perm in ([0, 1], [1, 0]):
                c = np.zeros((2, 3)); cc, r_, t_ = c[perm], rr[perm], tt[perm]
                sid, _, sp = raster(cc, r_, t_, lo, hi, vox)
                L = ledger(cc, r_, t_, sid, sp, lo, vox)
                chk(f'N8b {lbl} 종류 {tt.tolist()} 순서 {perm}: concentric_nonidentical 거부 · owner 없음',
                    'concentric_nonidentical' in codes(L) and L['owner'] is None, repr(codes(L)))
                P = S3.am_iface_plan(L, {'AM_S|AM_S': 1e-3, 'AM_S|AM_P': 1e-3, 'AM_P|AM_P': 1e-3})
                chk(f'N8b {lbl} 종류 {tt.tolist()} 순서 {perm}: 정량 솔브 거부',
                    raises(lambda: quiet(S3.solve_sigma_z, sid, te(), vox, iface=P)))
    #  판별력 — 중심만 키로 쓰고 입력 순서가 동률을 가르면 승자가 순서를 따른다 (01 → 0 · 10 → 1)
    pw = np.array([-1.0, -(1.0000002499999687 ** 2)])
    w = []
    for perm in ([0, 1], [1, 0]):
        order = sorted(perm, key=lambda k: (0.0, 0.0, 0.0))   # 같은 중심 → 안정 정렬 = 입력 순서
        w.append(order[0] if abs(pw[0] - pw[1]) <= 1e-6 else int(np.argmin(pw)))
    chk('N8b (판별력) 중심만 키 + 입력 순서 동률 → 승자가 순서를 따른다 (01 → 0 · 10 → 1)', w == [0, 1], repr(w))
    for tt in (np.array([2, 2]), np.array([2, 1])):
        c = np.zeros((2, 3)); rr = np.array([1.0, 1.0])
        sid, _, sp = raster(c, rr, tt, lo, hi, vox)
        L = ledger(c, rr, tt, sid, sp, lo, vox)
        chk(f'N8 정확 중복 (종류 {tt.tolist()}) → exact_duplicate 거부 · owner 없음',
            'exact_duplicate' in codes(L) and L['owner'] is None, repr(codes(L)))


# ═════════════════════════════════ RINTV-02 ═════════════════════════════════
@case('T0-1d raw_perm_mask_diag (RINTV-02 · v3.1 §2)')
def t_raw_perm_mask_diag():
    print('T0-1d raw_perm_mask_diag — 판정문 리터럴 · 실제 rasterize · 순서 [0,1] ↔ [1,0]')
    sa, _ = S3.rasterize(V02_C, V02_R, V02_T, None, None, V02_LO, V02_HI, V02_VOX, bridge_um=0.24)
    sb, _ = S3.rasterize(V02_C[[1, 0]], V02_R[[1, 0]], V02_T[[1, 0]], None, None, V02_LO, V02_HI, V02_VOX, bridge_um=0.24)
    Ma, Mb = np.isin(sa, (1, 2)), np.isin(sb, (1, 2))
    diff = np.argwhere(Ma != Mb).tolist()
    chk('T0-1d 반례 재현: AM 마스크 3170 ↔ 3171 · 바뀐 셀 (15,15,15) 하나 · sid 0 ↔ 2',
        (int(Ma.sum()), int(Mb.sum())) == (3170, 3171) and diff == [[15, 15, 15]]
        and (int(sa[15, 15, 15]), int(sb[15, 15, 15])) == (0, 2), f'{int(Ma.sum())} {int(Mb.sum())} {diff}')
    D = S3.am_iface_raw_perm_diag(V02_C, V02_R, V02_T, [0, 1], [1, 0], V02_LO, V02_HI, V02_VOX,
                                  delta_bound_um=0.0, bridge_um=0.24)
    chk('T0-1d 진단: 마스크 다름 검출 (masks_equal False · n_M 3170/3171) · 청구자 기하 G 는 같음',
        D['masks_equal'] is False and tuple(D['n_M']) == (3170, 3171) and D['claims_equal'] is True, repr(D)[:300])
    d0 = (D.get('diff') or [{}])[0]
    chk('T0-1d 진단: 차이 = 셀 (15,15,15) · sid 0 ↔ 2 · 청구자 = 두 입자 (canonical 0 · 1)',
        D.get('n_diff_cells') == 1 and tuple(d0.get('ijk', ())) == (15, 15, 15)
        and (d0.get('sid_a'), d0.get('sid_b')) == (0, 2) and d0.get('claimants_canonical') == [0, 1], repr(d0))
    chk('T0-1d 진단: owner 를 판정하지 않는다 (owner_judged False — 통과/실패로 대신 판정 금지)',
        D.get('owner_judged') is False and 'owner_equal' not in D)
    #  판별력 — v3 T0-1′ 팔 B (raw 순서마다 다시 raster 한 마스크 위 owner 동일 단언) 는 이 픽스처에서 **실패해야** 한다
    La = ledger(V02_C, V02_R, V02_T, sa, sa, V02_LO, V02_VOX)
    Lb = ledger(V02_C[[1, 0]], V02_R[[1, 0]], V02_T[[1, 0]], sb, sb, V02_LO, V02_VOX)
    chk('T0-1d (판별력) raw 마스크 위 owner 배열 동일 단언 (옛 팔 B) 은 여기서 실패한다',
        not np.array_equal(La['owner'], Lb['owner']))
    #  같은 마스크면 owner 를 판정한다 (양성 대조) — Codex 혼합 종류 두 구는 두 순서의 AM 마스크가 같다 (라벨만 다르다)
    D2 = S3.am_iface_raw_perm_diag(CODEX_C, CODEX_R, CODEX_T, [0, 1], [1, 0], CODEX_LO, CODEX_HI, CODEX_VOX,
                                   delta_bound_um=0.0, bridge_um=0.24)
    chk('T0-1d 양성 대조: 마스크 · 청구자 같음 → owner/support 판정 · 같음 (혼합 종류 두 구 · sid 16 셀 라벨 차이는 무관)',
        D2['masks_equal'] and D2['claims_equal'] and D2.get('owner_judged') is True and D2.get('owner_equal') is True,
        repr(D2)[:300])


def frozen_perm_identity(tag, c, r, t, sid, sid_pre, lo, vox, perms, rt=None, solve_kw=None):
    """동결 M · M0 위에서 입자 목록 순열 → 원장 (owner · 접점 · 면) · 계획 행 비트 같음 · σ(r > 0) 비트 같음."""
    sigs, psigs, sig_eff = set(), set(), set()
    for perm in perms:
        perm = list(perm)
        L = ledger(c[perm], r[perm], t[perm], sid, sid_pre, lo, vox)
        sigs.add(led_sig(L))
        if rt is not None and L['owner'] is not None:
            P = S3.am_iface_plan(L, rt, gap_law='fused', unreg_law='fused', ambiguous_arm='a_hi')
            psigs.add(plan_sig(P))
            if solve_kw is not None:
                with direct_solver():
                    res = quiet(S3.solve_sigma_z, sid, te(), vox, return_field=True, iface=P, **solve_kw)
                sig_eff.add(float(res['sigma_eff']).hex())
    ok = len(sigs) == 1 and (rt is None or len(psigs) == 1) and (solve_kw is None or len(sig_eff) == 1)
    return ok, len(sigs), len(psigs), len(sig_eff), L


@case('T0-1′ own_perm_frozen ⓐⓑⓒⓓ (RINTV-02 · v3.1 §2 I1‴)')
def t_own_perm_frozen():
    print('T0-1′ own_perm_frozen — 동결 AM 마스크 M + 동결 청구자 기하 G 위 입자 목록 순열')
    #  ⓐ Codex 혼합 종류 두 구 — 순서 [0,1] 의 raster 를 동결
    sid, _, sp = raster(CODEX_C, CODEX_R, CODEX_T, CODEX_LO, CODEX_HI, CODEX_VOX)
    ok, n1, n2, n3, L = frozen_perm_identity('ⓐ', CODEX_C, CODEX_R, CODEX_T, sid, sp, CODEX_LO, CODEX_VOX,
                                             itertools.permutations(range(2)), rt=CH_RT,
                                             solve_kw=dict(z_bot_um=0.0, z_top_um=3.9))
    chk('T0-1′ ⓐ 두 구: 원장 · 계획 행 · σ(r > 0) 순열마다 비트 같음', ok and L['contacts']['nsurv'].sum() > 0,
        f'{n1} {n2} {n3}')
    #  ⓑ 세 구 (혼합 · 겹침 셋 · 셋이 다투는 셀)
    sid, _, sp = raster(TRI_C, TRI_R, TRI_T, TRI_LO, TRI_HI, TRI_VOX)
    ok, n1, n2, n3, L = frozen_perm_identity('ⓑ', TRI_C, TRI_R, TRI_T, sid, sp, TRI_LO, TRI_VOX,
                                             itertools.permutations(range(3)), rt=CH_RT,
                                             solve_kw=dict(z_bot_um=0.2, z_top_um=3.35))
    chk('T0-1′ ⓑ 세 구 6 순열: 원장 · 계획 행 · σ(r > 0) 비트 같음 · 셋이 다투는 셀 있음 (|C| ≥ 3)',
        ok and L['n_cells_multi_claim'] > 0 and len(L['contacts']['a']) == 3,
        f'{n1} {n2} {n3} multi={L["n_cells_multi_claim"]}')
    #  ⓒ RINTV-02 픽스처 — 셀 (15,15,15) 을 **포함하는** 순서 [1,0] (3171) 의 마스크를 동결
    sb, _ = S3.rasterize(V02_C[[1, 0]], V02_R[[1, 0]], V02_T[[1, 0]], None, None, V02_LO, V02_HI, V02_VOX, bridge_um=0.24)
    ok, n1, n2, n3, L = frozen_perm_identity('ⓒ', V02_C, V02_R, V02_T, sb, sb, V02_LO, V02_VOX, ([0, 1], [1, 0]),
                                             rt=CH_RT)
    chk('T0-1′ ⓒ 3171 마스크 동결 · 두 순서: 원장 · 계획 행 비트 같음 · 거부 없음',
        ok and L['rejections'] == [] and L['owner'][15, 15, 15] >= 0, f'{n1} {n2} {codes(L)}')
    #  ⓒ 판별력 — 행 순서 한 쪽만 브리지를 청구하면 ([0,1] 목록) 그 셀이 청구자를 잃는다 (청구자 집합이 바뀐다)
    old = S3._am_bridge_claim_mids
    S3._am_bridge_claim_mids = lambda am_c, am_r, i, j, d: (S3._am_bridge_mid(am_c, am_r, i, j, d),)
    try:
        La = ledger(V02_C, V02_R, V02_T, sb, sb, V02_LO, V02_VOX)
        Lb = ledger(V02_C[[1, 0]], V02_R[[1, 0]], V02_T[[1, 0]], sb, sb, V02_LO, V02_VOX)
    finally:
        S3._am_bridge_claim_mids = old
    chk('T0-1′ ⓒ (판별력) 행 순서 한 쪽 브리지 청구 → [0,1] 목록에서 (15,15,15) 청구자 없음 (mask_unclaimed) · [1,0] 은 통과',
        'mask_unclaimed' in codes(La) and 'mask_unclaimed' not in codes(Lb), f'{codes(La)} {codes(Lb)}')
    #  ⓓ 세 청구자가 한 셀을 다투는 raster 판 (ε 픽스처 · 관측점 = 셀 (5,5,5) 중심)
    x0 = (np.array([5, 5, 5]) + 0.5) * 0.1
    c = x0 + EPS_REL; r = EPS_RAD.copy(); t = np.array([2, 1, 2])
    lo, hi, vox = (0.0, 0.0, 0.0), (4.8, 1.1, 1.1), 0.1
    sid, _, sp = raster(c, r, t, lo, hi, vox)
    owners, owners_old = set(), set()
    for perm in itertools.permutations(range(3)):
        perm = list(perm)
        L = ledger(c[perm], r[perm], t[perm], sid, sp, lo, vox, eps_p_um2=EPS_FIX)
        owners.add(int(L['owner'][5, 5, 5]))
        oldsel = S3._iface_owner_select
        S3._iface_owner_select = old_pairwise_fold
        try:
            Lo = ledger(c[perm], r[perm], t[perm], sid, sp, lo, vox, eps_p_um2=EPS_FIX)
        finally:
            S3._iface_owner_select = oldsel
        owners_old.add(int(Lo['owner'][5, 5, 5]))
    ok, n1, n2, n3, L = frozen_perm_identity('ⓓ', c, r, t, sid, sp, lo, vox, itertools.permutations(range(3)))
    chk('T0-1′ ⓓ ε 세 청구자 raster: 관측 셀 주인 = canonical 1 (중심 (1,0,0)+x0) · 6 순열 원장 비트 같음 (ε_p 1e−6 인자)',
        owners == {1} and ok, f'{owners} {n1}')
    chk('T0-1′ ⓓ (판별력) 쌍별 fold 변이 → 관측 셀 주인이 순열에 따라 바뀐다', len(owners_old) > 1, repr(owners_old))


@case('T0-1g mask_claimed (RINTV-02 · M ⊆ claimed(G))')
def t_mask_claimed():
    print('T0-1g mask_claimed — 두 legacy 순서 마스크 모두 청구됨 · 청구자 없는 AM 셀 변이 → 거부 + 기록')
    for perm in ([0, 1], [1, 0]):
        s_, _ = S3.rasterize(V02_C[perm], V02_R[perm], V02_T[perm], None, None, V02_LO, V02_HI, V02_VOX, bridge_um=0.24)
        L = ledger(V02_C, V02_R, V02_T, s_, s_, V02_LO, V02_VOX)
        chk(f'T0-1g legacy 순서 {perm} 마스크 ({int(np.isin(s_, (1, 2)).sum())} 셀) ⊆ claimed(G) — 거부 없음',
            L['rejections'] == [] and not (np.isin(s_, (1, 2)) & (L['owner'] < 0)).any(), repr(codes(L)))
    s_, _ = S3.rasterize(V02_C, V02_R, V02_T, None, None, V02_LO, V02_HI, V02_VOX, bridge_um=0.24)
    sm = s_.copy(); sm[0, 0, 0] = 1                       # 어떤 구 · 브리지에도 없는 모서리 셀
    L = ledger(V02_C, V02_R, V02_T, sm, sm, V02_LO, V02_VOX)
    rj = [x for x in L['rejections'] if x['code'] == 'mask_unclaimed']
    chk('T0-1g 변이 (청구자 없는 AM 셀) → mask_unclaimed 거부 · 수 1 · 자리 (0,0,0) 기록',
        len(rj) == 1 and rj[0]['n'] == 1 and tuple(rj[0]['detail'][0]) == (0, 0, 0), repr(rj))
    P = S3.am_iface_plan(L, CH_RT)
    chk('T0-1g 변이 계획 → 정량 솔브 거부 (조용한 bulk 면 없음)', raises(lambda: quiet(S3.solve_sigma_z, sm, te(), V02_VOX, iface=P)))


# ═════════════════════════════════ I2 (OFF) ═════════════════════════════════
#  옛 raster 지문 — **고치기 전** step3_sigma (HEAD f59570602 · blob 23f1e22e…) 로 잰 값 (rasterize 리팩터 비트 같음 증거)
GOLDEN_RASTER = {
    'codex_mixed_01': ('89941daffffe', '0cd97733f9ba', 8416),
    'codex_mixed_10': ('8068d3f1a96c', 'a346f2c61a37', 8416),
    'rintv02_01': ('19415619d4ed', '36553911ffe8', 3170),
    'rintv02_10': ('1af5116923c2', '284b3afbfbfc', 3171),
}


@case('T0-5′ off_bitid (I2 · 입력 순서마다 legacy · 막 0 + 예외 융합)')
def t_off_bitid():
    print('T0-5′ off_bitid — OFF ↔ (막 0 ∧ 예외 융합): σ · φ · n_dof · 분담 · je 비트 같음 (순서마다 · 그 순서의 legacy 기준)')
    for nm, (c, r, t, lo, hi, vox) in (('codex_mixed', (CODEX_C, CODEX_R, CODEX_T, CODEX_LO, CODEX_HI, CODEX_VOX)),
                                        ('rintv02', (V02_C, V02_R, V02_T, V02_LO, V02_HI, V02_VOX))):
        for perm in ([0, 1], [1, 0]):
            s_, p_ = S3.rasterize(c[perm], r[perm], t[perm], None, None, lo, hi, vox, bridge_um=0.24)
            g = GOLDEN_RASTER[f'{nm}_{perm[0]}{perm[1]}']
            chk(f'T0-5′ 옛 raster 지문 {nm} {perm}: sid · pid 지문 · AM 셀 수 = 고치기 전 코드',
                (S3._grid_fp(s_)[:12], S3._grid_fp(p_)[:12], int(np.isin(s_, (1, 2)).sum())) == g,
                f'{S3._grid_fp(s_)[:12]} {S3._grid_fp(p_)[:12]}')
    for perm in ([0, 1], [1, 0]):
        c, r, t = fx_codex(perm)
        sid, pid, sp = raster(c, r, t, CODEX_LO, CODEX_HI, CODEX_VOX)
        L = ledger(c, r, t, sid, sp, CODEX_LO, CODEX_VOX)
        kw = dict(return_field=True, z_bot_um=0.0, z_top_um=3.9)
        off = quiet(S3.solve_sigma_z, sid, te(), CODEX_VOX, **kw)
        P0 = S3.am_iface_plan(L, {'AM_S|AM_S': 0.0, 'AM_S|AM_P': 0.0, 'AM_P|AM_P': 0.0},
                              gap_law='fused', unreg_law='fused', ambiguous_arm='a_hi')
        on0 = quiet(S3.solve_sigma_z, sid, te(), CODEX_VOX, iface=P0, **kw)
        sh_o = S3.phase_current_share(off, sid, te()); sh_z = S3.phase_current_share(on0, sid, te())
        je_o = S3.per_particle_current(off, sid, pid, te(), 2); je_z = S3.per_particle_current(on0, sid, pid, te(), 2)
        jm_o = S3.field_point_cloud(off, sid, te(), CODEX_VOX, (1, 2))[2]
        jm_z = S3.field_point_cloud(on0, sid, te(), CODEX_VOX, (1, 2))[2]
        chk(f'T0-5′ {perm}: σ (hex) · φ · n_dof · 분담 (키 · hex) · je · |J| 통계 비트 같음 · 막 행 0',
            off['sigma_eff'].hex() == on0['sigma_eff'].hex() and np.array_equal(off['phi'], on0['phi'])
            and off['n_dof'] == on0['n_dof'] and set(sh_o) == set(sh_z)
            and all(float(sh_o[k]).hex() == float(sh_z[k]).hex() for k in sh_o)
            and np.array_equal(je_o, je_z) and jm_o == jm_z and P0['n_film_rows'] == 0,
            f"{off['sigma_eff']!r} {on0['sigma_eff']!r}")
        chk(f'T0-5′ {perm}: iface 를 안 주면 해 dict 에 iface 키가 없다 (옛 키 그대로) · 주면 기록이 있다',
            'iface' not in off and '_iface' not in off and on0.get('iface', {}).get('iface_model') == 'r2-owner-cnc')
        Pt = S3.am_iface_plan(L, {'AM_S|AM_P': 1e-15}, gap_law='fused', unreg_law='fused', ambiguous_arm='a_hi')
        tiny = quiet(S3.solve_sigma_z, sid, te(), CODEX_VOX, iface=Pt, **kw)
        chk(f'T0-5′ {perm}: r → 0⁺ (1e−15 Ω·cm²) 연속 — σ 상대 차 < 1e−9 · 막 행 > 0',
            abs(tiny['sigma_eff'] / off['sigma_eff'] - 1.0) < 1e-9 and Pt['n_film_rows'] > 0,
            f"{tiny['sigma_eff'] / off['sigma_eff'] - 1.0:.3e}")
    #  절단 팔에는 OFF 동일을 요구하지 않는다 (위상을 바꾼다) — 간극 브리지 쌍 · cut 이면 관통이 끊긴다
    c = np.array([[1., 1., 1.], [1., 1., 3.05]]); r = np.ones(2); t = np.array([2, 2])
    sid, _, sp = raster(c, r, t, (0, 0, 0), (2, 2, 4.05), 0.1)
    L = ledger(c, r, t, sid, sp, (0, 0, 0), 0.1)
    off = quiet(S3.solve_sigma_z, sid, te(), 0.1, return_field=True, z_bot_um=0.0, z_top_um=4.05)
    Pc = S3.am_iface_plan(L, {'AM_S|AM_S': 0.0}, gap_law='cut')
    cut = quiet(S3.solve_sigma_z, sid, te(), 0.1, return_field=True, z_bot_um=0.0, z_top_um=4.05, iface=Pc)
    chk('T0-5′ cut 팔: 간극 브리지 절단 → OFF 와 다르다 (요구 없음 · 기록: 관통 성분 없음) · 절단 tombstone 행',
        off['sigma_eff'] > 0 and cut['sigma_eff'] == 0.0 and Pc['n_cut_rows'] > 0
        and cut.get('reason') == 'no_through_component', f"{off['sigma_eff']} {cut.get('reason')}")


# ═════════════════════════════════ 단위 ═════════════════════════════════
@case('T1-4′ units_direct_vs_face (RINTG-09)')
def t_units_direct_vs_face():
    print('T1-4′ units_direct_vs_face — R_j 100 Ω · h 1 µm · σ 1e8 S/cm')
    Rj, h, sig = 100.0, 1.0, 1e8
    rf = float(S3.iface_rface_ohm_cm2(Rj * 1e-8 * 1.0, 1, h, 1.0))      # 접합 R_j 를 A = 1 µm² 접점의 막으로: r = R_j·1e−8·A
    chk('T1-4′ 면 분배 r_face = R_j·N·h²·1e−8 = 1e−6 Ω·cm²', abs(rf - 1e-6) <= 1e-18, repr(rf))
    Rf = float(S3.iface_face_film_R_ohm(rf, h))
    chk('T1-4′ 막 성분만: R_f = r_face/(h²·1e−8) = R_j = 100 Ω (정확)', abs(Rf - Rj) <= 1e-12 * Rj, repr(Rf))
    g = S3.interface_face_g(np.array([sig * h]), np.array([sig]), np.array([sig]), np.array([rf]), h)
    G = float(S3.iface_code_G_S(g)[0])
    lead = 1e4 / (sig * h)                                               # 반셀 둘 = 0.0001 Ω (같은 리드)
    chk('T1-4′ 면 경로 G = 0.00999999000001 S = 직접 간선 + 같은 리드 1/(R_j + 0.0001 Ω) (상대 1e−12)',
        abs(G - 1.0 / (Rj + lead)) <= 1e-12 * G and abs(G - 0.00999999000001) <= 1e-12 * G, repr(G))
    chk('T1-4′ (판별력) "면 G = 직접 0.01 S" 를 1e−12 로 주장하면 실패 (차 약 1e−6)',
        abs(G - 1.0 / Rj) > 1e-12 * G, f'{abs(G - 0.01) / G:.2e}')


@case('T1-11 units_atrue (RINTG-07)')
def t_units_atrue():
    print('T1-11 units_atrue — ΣG_film = 1e−8·A_true[µm²]/r[Ω·cm²] (R 1 µm 두 구 · δ 0.02 · vox 0.2 · r 1e−3 · Codex 픽스처)')
    from lens_geometry import intersection_disc_area
    c = np.array([[1., 1., 1.], [1., 1., 2.98]]); r = np.ones(2); t = np.array([2, 2])
    lo, hi, vox = (0.0, 0.0, 0.0), (2.0, 2.0, 3.98), 0.2
    sid, _, sp = raster(c, r, t, lo, hi, vox)
    L = ledger(c, r, t, sid, sp, lo, vox)
    A = intersection_disc_area(1.0, 1.0, 0.02)
    P = S3.am_iface_plan(L, {'AM_S|AM_S': 1e-3})
    G = S3.iface_plan_film_G_S(P)
    exp = 1e-8 * A / 1e-3
    chk('T1-11 A_true = 0.0625176938064 µm² (lens_geometry · 판정문 값)', abs(L['contacts']['A_true'][0] - A) <= 1e-15
        and abs(A - 0.0625176938064) < 1e-12, repr(A))
    chk('T1-11 계획 행에서 ΣG_film = 6.25176938064e−7 S = 1e−8·A_true/r (상대 1e−12) · 접점 공식 함수와 같음',
        len(G) == 1 and abs(G[0] - exp) <= 1e-12 * exp and abs(float(S3.iface_contact_film_G_S(A, 1e-3)) - exp) <= 1e-12 * exp
        and abs(exp - 6.25176938064e-7) < 1e-17, f'{G} {exp}')
    chk('T1-11 (판별력) 1e−8 을 뺀 변이 (A/r) 는 1e8 배 — 실패', abs(A / 1e-3 - G[0]) > 1e6 * G[0])
    chk('T1-11 기록: film_G_S_total 두 판 (탄소 없음 → 같음 = ΣG)',
        abs(P['record']['iface_contact_ledger']['film_G_S_total']['remove_area'] - exp) <= 1e-12 * exp
        and abs(P['record']['iface_contact_ledger']['film_G_S_total']['renormalize'] - exp) <= 1e-12 * exp)


# ═════════════════════════════════ 탄소 ═════════════════════════════════
@case('T1-10 carbon_cover_law (RINTG-02 · v3.1 §5 · 막 소자만)')
def t_carbon_cover_law():
    print('T1-10 carbon_cover_law — 순수 막 회로 2 Ω / 1 Ω · raster N_c^0 · N_c^surv · 총량 비 (전체 단자 저항은 요구 안 함)')
    #  ① 순수 막 회로 — 패치 둘 (N_0 = 2) 중 하나가 덮임 (N_surv = 1) · 접점 막 총량 1 S (1e−8·A/r = 1)
    r_, A_, h = 1e-8, 1.0, 0.37
    rf_rm = float(S3.iface_rface_ohm_cm2(r_, 2, h, A_)); rf_rn = float(S3.iface_rface_ohm_cm2(r_, 1, h, A_))
    R_rm = float(S3.iface_face_film_R_ohm(rf_rm, h)); R_rn = float(S3.iface_face_film_R_ohm(rf_rn, h))
    R_full = 1.0 / (2.0 / float(S3.iface_face_film_R_ohm(rf_rm, h)))
    chk('T1-10 ① 덮이기 전 (패치 둘 병렬) = 1 Ω · remove_area 남은 패치 = 2 Ω · renormalize = 1 Ω',
        abs(R_full - 1.0) < 1e-12 and abs(R_rm - 2.0) < 1e-12 and abs(R_rn - 1.0) < 1e-12, f'{R_full} {R_rm} {R_rn}')
    #  ② raster — 두 AM_S 구의 목 셀 일부를 탄소 (VGCF 점 스탬프) 가 덮는다
    c = np.array([[1., 1., 1.], [1., 1., 2.9]]); r = np.ones(2); t = np.array([2, 2])
    lo, hi, vox = (0.0, 0.0, 0.0), (2.0, 2.0, 3.9), 0.1
    _, _, sp = raster(c, r, t, lo, hi, vox)
    L0 = ledger(c, r, t, sp, sp, lo, vox)
    F = L0['faces']
    n0 = int(L0['contacts']['n0'][0])
    lin_lo = F['lin'][F['cid'] == 0]
    pick = lin_lo[: max(1, n0 // 3)]
    ijk = np.stack(np.unravel_index(pick, sp.shape), axis=1)
    add = (ijk + 0.5) * vox; ph = np.full(len(add), 2)
    sid, _, sp2 = raster(c, r, t, lo, hi, vox, add=add, ph=ph)
    L = ledger(c, r, t, sid, sp2, lo, vox)
    C = L['contacts']
    ns = int(C['nsurv'][0])
    chk(f'T1-10 ② N_c^0 = {n0} (첨가제 전) · 0 < N_c^surv = {ns} < N_c^0 · S_surv ⊆ S_0 (거부 없음)',
        int(C['n0'][0]) == n0 and 0 < ns < n0 and L['rejections'] == [], f'{n0} {ns} {codes(L)}')
    Prm = S3.am_iface_plan(L, {'AM_S|AM_S': 1e-3}, carbon_cover='remove_area')
    Prn = S3.am_iface_plan(L, {'AM_S|AM_S': 1e-3}, carbon_cover='renormalize')
    Gfull = 1e-8 * C['A_true'][0] / 1e-3
    g_rm, g_rn = S3.iface_plan_film_G_S(Prm)[0], S3.iface_plan_film_G_S(Prn)[0]
    chk('T1-10 ② 막 원장 총량: remove_area = (N_surv/N_0)·1e−8·A/r · renormalize = 1e−8·A/r (상대 1e−12)',
        abs(g_rm - Gfull * ns / n0) <= 1e-12 * Gfull and abs(g_rn - Gfull) <= 1e-12 * Gfull, f'{g_rm} {g_rn} {Gfull}')
    rec = Prm['record']['iface_contact_ledger']
    chk('T1-10 ② 두 판의 r_face 를 둘 다 기록 · 적용 법칙 표지 · N_surv/N_0 = 격자 support 면 비율 표지',
        rec['rface_ohm_cm2']['remove_area'] is not None and rec['rface_ohm_cm2']['renormalize'] is not None
        and Prm['record']['iface_carbon_cover'] == 'remove_area' and Prn['record']['iface_carbon_cover'] == 'renormalize'
        and abs(rec['Nsurv_over_N0']['median'] - ns / n0) < 1e-12 and '격자 support' in rec['Nsurv_over_N0_meaning'])
    #  ③ 목 전부 덮임 → N_surv = 0 = unrealized (탄소) · 나눗셈 전에 상태 · 막 없음 · '절연 아님' 표지
    pick = lin_lo
    ijk = np.stack(np.unravel_index(pick, sp.shape), axis=1)
    add = np.vstack([(ijk + 0.5) * vox])
    sid3, _, sp3 = raster(c, r, t, lo, hi, vox, add=add, ph=np.full(len(add), 2))
    L3 = ledger(c, r, t, sid3, sp3, lo, vox)
    P3 = S3.am_iface_plan(L3, {'AM_S|AM_S': 1e-3})
    u = P3['record']['iface_contact_ledger']['unrealized']
    chk('T1-10 ③ 목 전부 덮임 → unrealized 1 (탄소) · 막 행 0 · 의미 = AM–AM 막이 남지 않음 (전체 절연 아님)',
        int(L3['contacts']['nsurv'][0]) == 0 and u['n'] == 1 and u['carbon'] == 1 and P3['n_film_rows'] == 0
        and '절연이 아니다' in u['meaning'], repr(u))
    chk('T1-10 범위: 전체 단자 저항에 2 Ω/1 Ω 을 요구하지 않는다 — 한정어 (상·하한 아님 · 탄소 접합 미식별) 가 기록에',
        any('상·하한이 아니다' in q for q in Prm['record']['iface_qualifiers']))


# ═════════════════════════════════ E4′ (RINT-16 행동) ═════════════════════════════════
def chain_solve(vox, rt, iface=True, carbon='remove_area'):
    sid, pid, sp = raster(CH_C, CH_R, CH_T, CH_LO, CH_HI, vox)
    kw = dict(return_field=True, z_bot_um=0.0, z_top_um=5.9)
    if not iface:
        with direct_solver():
            return sid, quiet(S3.solve_sigma_z, sid, te(), vox, **kw), None
    L = ledger(CH_C, CH_R, CH_T, sid, sp, CH_LO, vox)
    P = S3.am_iface_plan(L, rt, carbon_cover=carbon)
    with direct_solver():
        return sid, quiet(S3.solve_sigma_z, sid, te(), vox, iface=P, **kw), P


@case('T0-3′ class_sensitivity (RINTG-03 · E4′ · RINT-16 행동)')
def t_class_sensitivity():
    print('T0-3′ class_sensitivity — 부류 둘 (AM_S|AM_S · AM_S|AM_P) · 혼합 σ · 판 포함 · h 0.2 · 0.1 · 직접 풀이')
    eps = 1e-4
    for vox in (0.2, 0.1):
        sid, res, P = chain_solve(vox, CH_RT)
        sh, tot = S3.phase_current_share(res, sid, te(), return_total=True)
        cc, gb, _ = res['plate_edges']['bot']
        I = float((np.asarray(gb) * (1.0 - res['phi'][cc])).sum())
        kSS, kSP = S3.SID_IFACE_AM['AM_S|AM_S'], S3.SID_IFACE_AM['AM_S|AM_P']
        chk(f'T0-3′ h {vox}: 부류 버킷 둘 · 몫 > 0 · 분담 합 1 · 에너지 Σ P (bulk + 막 + 판) = I·ΔV (상대 1e−10)',
            kSS in sh and kSP in sh and sh[kSS] > 0 and sh[kSP] > 0 and abs(sum(sh.values()) - 1.0) < 1e-12
            and abs(tot / I - 1.0) < 1e-10, f'{ {S3.share_label(k): round(v, 5) for k, v in sh.items()} } {tot / I - 1:.2e}')
        fd = {}
        for nm, keys in (('SS', ('AM_S|AM_S',)), ('SP', ('AM_S|AM_P',)), ('joint', ('AM_S|AM_S', 'AM_S|AM_P'))):
            vals = []
            for sgn in (+1, -1):
                rt = dict(CH_RT)
                for k in keys:
                    rt[k] = CH_RT[k] * math.exp(sgn * eps)
                vals.append(chain_solve(vox, rt)[1]['sigma_eff'])
            fd[nm] = -(math.log(vals[0]) - math.log(vals[1])) / (2 * eps)
        chk(f'T0-3′ h {vox}: s(AM_S|AM_S) = −∂lnσ/∂ln r (FD) · s(AM_S|AM_P) = FD · 함께 = Σ_c s_c (각 1e−6)',
            abs(sh[kSS] - fd['SS']) < 1e-6 and abs(sh[kSP] - fd['SP']) < 1e-6
            and abs(sh[kSS] + sh[kSP] - fd['joint']) < 1e-6,
            f"s {sh[kSS]:.9f}/{fd['SS']:.9f} · {sh[kSP]:.9f}/{fd['SP']:.9f} · Σ {sh[kSS] + sh[kSP]:.9f}/{fd['joint']:.9f}")
        if vox == 0.2:
            #  판별력 — 옛 단일 버킷 (부류 합) 을 한 부류의 민감도로 읽으면 틀린다 (RINT-16)
            chk('T0-3′ (판별력) 부류 합 버킷을 한 부류 민감도로 읽으면 FD 와 어긋난다',
                abs((sh[kSS] + sh[kSP]) - fd['SS']) > 1e-3)


@case('T0-3m e4_printed_mutant (RINTG-03)')
def t_e4_printed_mutant():
    print('T0-3m e4_printed_mutant — h 0.2 µm · σ 0.01 S/cm · r_face 0.01024 Ω·cm² (판정문 픽스처 · 면 하나)')
    h, s_, rf = 0.2, 0.01, 0.01024
    g0 = np.array([s_ * h]); sa = sb = np.array([s_])
    g = float(S3.interface_face_g(g0, sa, sb, np.array([rf]), h)[0])
    chk('T0-3m 실제 interface_face_g = 0.000326797385621 (판정문)', abs(g - 0.00032679738562091506) < 1e-16, repr(g))
    e = 1e-5
    gp = float(S3.interface_face_g(g0, sa, sb, np.array([rf * math.exp(e)]), h)[0])
    gm = float(S3.interface_face_g(g0, sa, sb, np.array([rf * math.exp(-e)]), h)[0])
    fd = -(math.log(gp) - math.log(gm)) / (2 * e)
    rprime = rf * 1e4
    printed = g * rprime                                   # v2 E4 문구: I_code²·r′ / P (Δφ = 1) = g·r′
    chk('T0-3m (판별력) 인쇄식 I_code²·r′ (÷h² 없음) = 0.0334640522876 — FD (0.836601307164) 와 어긋나 실패',
        abs(printed - 0.0334640522875817) < 1e-12 and abs(printed - fd) > 0.5 and abs(fd - 0.8366013071636756) < 1e-9,
        f'{printed!r} {fd!r}')
    share = float(S3.iface_face_split(sa, sb, np.array([rf]), h)[2][0])
    chk('T0-3m 막 몫 (E4′ r′/(R_half + r′) · 생산 iface_face_split) = 0.836601307190 = 중심 로그 FD (1e−8) · 인쇄식의 25 배',
        abs(share - 0.8366013071895424) < 1e-12 and abs(share - fd) < 1e-8 and abs(share / printed - 25.0) < 1e-9,
        f'{share!r} {fd!r}')


@case('T0-3i multiclass_integral (RINTG-03 · E4′ 적분 = Σ_c)')
def t_multiclass_integral():
    print('T0-3i multiclass_integral — ln σ(r)/σ(0) = −∫₀¹ Σ_c s_c(t·r) dt/t (실제 솔버 · 직접 풀이 · Gauss–Legendre 12)')
    #  산술 기준 (판정문): 직렬 bulk 3 · A 1 · B 2 Ω
    t_, w_ = gl_nodes(12)
    sA = lambda t: t * 1.0 / (3.0 + t * 3.0)               # noqa: E731
    sB = lambda t: t * 2.0 / (3.0 + t * 3.0)               # noqa: E731
    jnt = -sum(w * (sA(x) + sB(x)) / x for x, w in zip(t_, w_))
    onlyA = -sum(w * sA(x) / x for x, w in zip(t_, w_))
    chk('T0-3i 산술: Σ_c 적분 = −0.693147180560 · A 만 = −0.231049060187 (판정문 · 구적 1e−10)',
        abs(jnt - math.log(0.5)) < 1e-10 and abs(onlyA - (-0.23104906018664842)) < 1e-10, f'{jnt!r} {onlyA!r}')
    vox = 0.2
    _, off, _ = chain_solve(vox, CH_RT, iface=False)
    _, on, _ = chain_solve(vox, CH_RT)
    lhs = math.log(on['sigma_eff'] / off['sigma_eff'])
    kSS, kSP = S3.SID_IFACE_AM['AM_S|AM_S'], S3.SID_IFACE_AM['AM_S|AM_P']
    tot_int, a_int = 0.0, 0.0
    for x, w in zip(t_, w_):
        rt = {k: v * x for k, v in CH_RT.items()}
        sid, res, _ = chain_solve(vox, rt)
        sh = S3.phase_current_share(res, sid, te())
        tot_int += w * (sh.get(kSS, 0.0) + sh.get(kSP, 0.0)) / x
        a_int += w * sh.get(kSS, 0.0) / x
    chk('T0-3i 솔버: ln σ(r)/σ(0) = −∫ Σ_c s_c dt/t (1e−7)', abs(lhs + tot_int) < 1e-7, f'{lhs!r} {-tot_int!r}')
    chk('T0-3i (판별력) 한 부류만 적분한 변이는 어긋난다', abs(lhs + a_int) > 1e-3, f'{lhs!r} {-a_int!r}')


# ═════════════════════════════════ T1-2 · T0-4 · T0-6a ═════════════════════════════════
#  Codex 1 단계 판정 증거 (docs/reviews/codex_rint_stage1_review_evidence_20261003/evidence_area/probe_outputs.json
#  AM_boundary_placement) — R 1 µm 두 AM_S 구 · δ 0.02 · bridge 0.24 · r 1e−3 · 같은 Σg_film
T12_CODEX = {0.2: {'contact_midplane': (16, 0.6474454905222262), 'rasterize_pid': (24, 0.6241260200703511)},
             0.1: {'contact_midplane': (32, 0.699948650839772), 'rasterize_pid': (64, 0.6755034001272918)}}


@case('T1-2 two_sphere_axis (배치 회귀 표지 · v3 §6-1 — 정확성 증거 아님)')
def t_two_sphere_axis():
    print('T1-2 two_sphere_axis — CNC owner 면 = Codex contact_midplane 면 집합 · σON/σOFF 재현 (배치 회귀) · r1 pid 경계와 다름')
    from lens_geometry import intersection_disc_area
    c = np.array([[1., 1., 1.], [1., 1., 2.98]]); r = np.ones(2); t = np.array([2, 2])
    sig = np.zeros(10); sig[1] = 0.01
    A = intersection_disc_area(1.0, 1.0, 0.02)
    for vox in (0.2, 0.1):
        sid, pid = S3.rasterize(c, r, t, None, None, (0, 0, 0), (2, 2, 3.98), vox, bridge_um=0.24)
        n_mid, q_mid = T12_CODEX[vox]['contact_midplane']
        n_pid, q_pid = T12_CODEX[vox]['rasterize_pid']
        with direct_solver():
            off = quiet(S3.solve_sigma_z, sid, sig, vox, z_bot_um=0.0, z_top_um=3.98)
            r1 = quiet(S3.solve_sigma_z, sid, sig, vox, z_bot_um=0.0, z_top_um=3.98, pid=pid,
                       rint={(1, 1): 1e-3 * n_pid * vox * vox / A})
        chk(f'T1-2 h {vox}: (대조) r1 pid 경계 = {n_pid} 면 · σON/σOFF {q_pid:.10f} (옛 탐침 · 곡면 위치 — Codex 값 재현 1e−9)',
            r1['interface']['n_faces_rint'] == n_pid and abs(r1['sigma_eff'] / off['sigma_eff'] / q_pid - 1) < 1e-9,
            f"{r1['interface']['n_faces_rint']} {r1['sigma_eff'] / off['sigma_eff']!r}")
        L = ledger(c, r, t, sid, sid, (0, 0, 0), vox)
        P = S3.am_iface_plan(L, {'AM_S|AM_S': 1e-3})
        with direct_solver():
            on = quiet(S3.solve_sigma_z, sid, sig, vox, z_bot_um=0.0, z_top_um=3.98, iface=P)
        chk(f'T1-2 h {vox}: CNC owner 면 N_c = {n_mid} · σON/σOFF = {q_mid:.10f} (Codex contact_midplane · 1e−9)',
            int(L['contacts']['n0'][0]) == n_mid and abs(on['sigma_eff'] / off['sigma_eff'] / q_mid - 1) < 1e-9,
            f"{int(L['contacts']['n0'][0])} {on['sigma_eff'] / off['sigma_eff']!r}")


@case('T0-4 rayleigh (I6 · 같은 그래프 · 같은 BC)')
def t_rayleigh():
    print('T0-4 rayleigh — σ(r) 비증가 · 절단 ≤ 막 ≤ 융합 (고정 그래프의 조건부 순서 · 신뢰구간 아님)')
    vals = []
    for sc in (0.0, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1):
        vals.append(chain_solve(0.2, {k: v * sc for k, v in CH_RT.items()})[1]['sigma_eff'])
    chk('T0-4 사슬: r 배율 0 → 1e−1 에서 σ 비증가 (이 직렬 형상에서는 엄격 감소)',
        all(b < a for a, b in zip(vals, vals[1:])), ' > '.join(f'{v:.6g}' for v in vals))
    c4 = np.array([[1., 1., 1.], [1., 1., 2.995]]); r4 = np.ones(2); t4 = np.array([2, 2])
    s4, _, p4 = raster(c4, r4, t4, (0, 0, 0), (2, 2, 4.0), 0.1)
    L4 = ledger(c4, r4, t4, s4, p4, (0, 0, 0), 0.1, db=0.01)
    kw = dict(return_field=True, z_bot_um=0.0, z_top_um=3.995)
    with direct_solver():
        s_cut = quiet(S3.solve_sigma_z, s4, te(), 0.1, iface=S3.am_iface_plan(L4, {'AM_S|AM_S': 1e-3}, ambiguous_arm='cut'), **kw)
        s_film = quiet(S3.solve_sigma_z, s4, te(), 0.1, iface=S3.am_iface_plan(L4, {'AM_S|AM_S': 1e-3}, ambiguous_arm='a_hi'), **kw)
        s_fuse = quiet(S3.solve_sigma_z, s4, te(), 0.1, **kw)
    chk('T0-4 모호 접점: 절단 (0) ≤ A_hi 막 ≤ 융합 (OFF)',
        s_cut['sigma_eff'] <= s_film['sigma_eff'] <= s_fuse['sigma_eff'] and s_film['sigma_eff'] < s_fuse['sigma_eff'],
        f"{s_cut['sigma_eff']} {s_film['sigma_eff']} {s_fuse['sigma_eff']}")


@case('T0-6a ledger_consistency (원장 수정 → 새로 조립 · 솔브 · 진단이 함께)')
def t_ledger_consistency():
    print('T0-6a ledger_consistency — 막 행 하나를 뺀 (지문을 다시 만든) 계획 → 조립 · 해의 원장 · 진단이 함께 바뀐다')
    sid, res, P = chain_solve(0.2, CH_RT)
    k = next(i for i, ax in enumerate(P['axes']) if len(ax['lin']))
    axes = [dict(ax) for ax in P['axes']]
    axes[k] = {kk: v[1:] for kk, v in axes[k].items()}
    P2 = dict(P); P2['axes'] = tuple(axes); P2['fp_rows'] = S3._iface_rows_fp(P2['axes'])
    P2['n_film_rows'] = P['n_film_rows'] - 1
    with direct_solver():
        res2 = quiet(S3.solve_sigma_z, sid, te(), 0.2, return_field=True, z_bot_um=0.0, z_top_um=5.9, iface=P2)
    sh2, tot2 = S3.phase_current_share(res2, sid, te(), return_total=True)
    cc, gb, _ = res2['plate_edges']['bot']
    I2 = float((np.asarray(gb) * (1.0 - res2['phi'][cc])).sum())
    chk('T0-6a 막 하나를 빼면 σ 증가 · 해의 원장 행 −1 · 에너지 항등식 유지 (1e−10) · 부류 몫이 바뀐다',
        res2['sigma_eff'] > res['sigma_eff']
        and sum(len(ax['lin']) for ax in res2['_iface']['axes']) == P['n_film_rows'] - 1
        and abs(tot2 / I2 - 1.0) < 1e-10
        and S3.phase_current_share(res, sid, te()) != sh2, f"{res['sigma_eff']} → {res2['sigma_eff']}")


# ═════════════════════════════════ 거부 (N) ═════════════════════════════════
@case('N2 · N3 · N4 · N6 · N7 · 채널 · 거부 계획 (정량 모드 거부)')
def t_rejections():
    print('N — 정량 모드 거부 (자동 fallback 없음)')
    c, r, t = fx_codex([0, 1])
    sid, pid, sp = raster(c, r, t, CODEX_LO, CODEX_HI, CODEX_VOX)
    L = ledger(c, r, t, sid, sp, CODEX_LO, CODEX_VOX)
    P = S3.am_iface_plan(L, CH_RT)
    kw = dict(z_bot_um=0.0, z_top_um=3.9)
    chk('N2 주기 + 정량 → 거부', raises(lambda: quiet(S3.solve_sigma_z, sid, te(), CODEX_VOX, periodic_xy=True, iface=P, **kw)))
    chk('N3 r1 AM 쌍 키 (AM_S|AM_P) + 정량 → 거부',
        raises(lambda: quiet(S3.solve_sigma_z, sid, te(), CODEX_VOX, rint={(1, 2): 1e-3}, pid=pid, iface=P, **kw)))
    chk('N3 r1 탐침 표 (AM_S|VGCF) 도 정량 모드와 함께면 거부 (r1 = 탐침 전용)',
        raises(lambda: quiet(S3.solve_sigma_z, sid, te(), CODEX_VOX, rint={(1, 3): 1e-3}, iface=P, **kw)))
    chk('채널: 이온 표 (AM σ = 0) 에 ①′ 막 → 거부 (막이 조용히 무효 · RINT-14 부류)',
        raises(lambda: quiet(S3.solve_sigma_z, sid, S3.ionic_sigma_table(1e-3, 3e-3), CODEX_VOX, iface=P, **kw)))
    chk('E5 다른 격자 (sid 한 셀 변경) 의 계획 → 거부',
        raises(lambda: quiet(S3.solve_sigma_z, np.where(np.arange(sid.size).reshape(sid.shape) == 0, 3, sid).astype(sid.dtype),
                             te(), CODEX_VOX, iface=P, **kw)))
    Pm = dict(P); Pm['axes'] = tuple(dict(ax) for ax in P['axes'])
    Pm['axes'][2]['rface'] = Pm['axes'][2]['rface'] * 2.0
    chk('E5 계획 행 변조 (만든 뒤 r_face × 2) → 거부', raises(lambda: quiet(S3.solve_sigma_z, sid, te(), CODEX_VOX, iface=Pm, **kw)))
    chk('계획이 아닌 것 (원장 · dict) → 거부', raises(lambda: quiet(S3.solve_sigma_z, sid, te(), CODEX_VOX, iface=L, **kw))
        and raises(lambda: quiet(S3.solve_sigma_z, sid, te(), CODEX_VOX, iface={'kind': 'am_iface_plan'}, **kw)))
    #  N4 모호 — δ 0.005 · δ_bound 0.01 → |δ| ≤ δ_bound · 팔 선언 없으면 거부 · 팔마다 다른 해
    c4 = np.array([[1., 1., 1.], [1., 1., 2.995]]); r4 = np.ones(2); t4 = np.array([2, 2])
    s4, _, p4 = raster(c4, r4, t4, (0, 0, 0), (2, 2, 4.0), 0.1)
    L4 = ledger(c4, r4, t4, s4, p4, (0, 0, 0), 0.1, db=0.01)
    chk('N4 모호 부류 1 (|δ| = 0.005 ≤ 0.01) · A_hi = 구간 위 끝 원판 (lens δ = 0.015)',
        int((L4['contacts']['cls'] == 1).sum()) == 1
        and abs(L4['contacts']['A_hi'][0] - __import__('lens_geometry').intersection_disc_area(1.0, 1.0, 0.015)) < 1e-15)
    P4 = S3.am_iface_plan(L4, {'AM_S|AM_S': 1e-3})
    chk('N4 팔 선언 없음 → ambiguous_without_arms 거부 · 솔브 거부',
        'ambiguous_without_arms' in codes(P4) and raises(lambda: quiet(S3.solve_sigma_z, s4, te(), 0.1, iface=P4)))
    P4a = S3.am_iface_plan(L4, {'AM_S|AM_S': 1e-3}, ambiguous_arm='a_hi')
    P4c = S3.am_iface_plan(L4, {'AM_S|AM_S': 1e-3}, ambiguous_arm='cut')
    chk('N4 두 팔 각각 계획 OK · a_hi = 막 행 · cut = 절단 행 · 기록에 팔 표지',
        P4a['rejections'] == [] and P4a['n_film_rows'] > 0 and P4c['n_cut_rows'] > 0
        and P4a['record']['iface_exception_law']['ambiguous_arm'] == 'a_hi')
    #  N6 간극 브리지 · 미등록
    c6 = np.array([[1., 1., 1.], [1., 1., 3.05]]); r6 = np.ones(2); t6 = np.array([2, 2])
    s6, _, p6 = raster(c6, r6, t6, (0, 0, 0), (2, 2, 4.05), 0.1)
    L6 = ledger(c6, r6, t6, s6, p6, (0, 0, 0), 0.1)
    chk('N6 간극 (gap 0.05 ≤ tol) = gap_bridged 부류', int((L6['contacts']['cls'] == 2).sum()) == 1)
    chk('N6 gap_law 선언 없음 → gap_law_undeclared 거부 (L1 · fused 자동 적용 없음)',
        'gap_law_undeclared' in codes(S3.am_iface_plan(L6, {'AM_S|AM_S': 1e-3})))
    chk('N6 gap_law = reject → 거부 · fused → 막 없음 (OFF 와 같은 면)',
        'gap_law_reject' in codes(S3.am_iface_plan(L6, {'AM_S|AM_S': 1e-3}, gap_law='reject'))
        and S3.am_iface_plan(L6, {'AM_S|AM_S': 1e-3}, gap_law='fused')['n_film_rows'] == 0)
    c7 = np.array([[1., 1., 1.], [1., 1., 3.15]]); r7 = np.ones(2); t7 = np.array([2, 2])
    s7, _, p7 = raster(c7, r7, t7, (0, 0, 0), (2, 2, 4.15), 0.4)
    L7 = ledger(c7, r7, t7, s7, p7, (0, 0, 0), 0.4)
    nunreg = int(((L7['faces']['cid'] < 0) & L7['faces']['surv']).sum())
    chk('N6 미등록 (gap 0.15 > tol · 양자화로 면 공유) — 등록 쌍 0 · 미등록 면 > 0', len(L7['contacts']['a']) == 0 and nunreg > 0,
        f'{nunreg}')
    P7 = S3.am_iface_plan(L7, {'AM_S|AM_S': 1e-3})
    chk('N6 unreg_law 선언 없음 → unreg_law_undeclared 거부', 'unreg_law_undeclared' in codes(P7))
    P7c = S3.am_iface_plan(L7, {'AM_S|AM_S': 1e-3}, unreg_law='cut')
    r7c = quiet(S3.solve_sigma_z, s7, te(), 0.4, return_field=True, z_bot_um=0.0, z_top_um=4.15, iface=P7c)
    r7o = quiet(S3.solve_sigma_z, s7, te(), 0.4, return_field=True, z_bot_um=0.0, z_top_um=4.15)
    chk('N6 unreg_law = cut → 절단 행 = 미등록 면 · 관통이 끊긴다 (OFF > 0) · E3 실제 간선 연결성',
        P7c['n_cut_rows'] == nunreg and r7o['sigma_eff'] > 0 and r7c['sigma_eff'] == 0.0
        and r7c.get('reason') == 'no_through_component', f"{r7o['sigma_eff']} {r7c.get('reason')}")
    #  N7 — SDCP–AM 브리지 raster 선언
    L_n7 = ledger(c, r, t, sid, sp, CODEX_LO, CODEX_VOX, raster_sdcp_bridge_um=0.05)
    chk('N7 raster sdcp_bridge_um > 0 → sdcp_bridge_raster 거부', 'sdcp_bridge_raster' in codes(L_n7))
    #  표에 없는 종류 쌍 · 0 면적
    chk('표에 없는 종류 쌍 (AM_S|AM_P 접점 · 표 AM_S|AM_S 뿐) → r_type_missing 거부',
        'r_type_missing' in codes(S3.am_iface_plan(L, {'AM_S|AM_S': 1e-3})))
    for bad in ({'AM_X|AM_S': 1e-3}, {'AM_S|AM_S': -1.0}, {'AM_S|AM_S': float('nan')}, {'AM_S|AM_S': True},
                {'AM_S|AM_S': '1e-3'}, {'AM_S': 1e-3}, {'AM_S|AM_P': 1e-3, 'AM_P|AM_S': 2e-3}):
        chk(f'r_type 파서 거부 {bad!r}', raises(lambda b=bad: S3.parse_iface_r_type(b)))
    chk('r_type 파서: AM_P|AM_S → AM_S|AM_P 정규화', S3.parse_iface_r_type({'AM_P|AM_S': 2e-3}) == {'AM_S|AM_P': 2e-3})
    for bad in (dict(carbon_cover='both'), dict(gap_law='l1'), dict(unreg_law='fallback'), dict(ambiguous_arm='mid')):
        chk(f'계획 인자 거부 {bad}', raises(lambda b=bad: S3.am_iface_plan(L, CH_RT, **b)))
    chk('원장: delta_bound_um 없음 (기본값 없음) → TypeError',
        raises(lambda: S3.am_iface_ledger(c, r, t, sid, sp, CODEX_LO, CODEX_VOX), (TypeError,)))


# ═════════════════════════════════ 원장 · 진단 (E2 · E5) ═════════════════════════════════
@case('T0-6b ledger_integrity · E2 진단이 원장을 읽는다')
def t_ledger_integrity():
    print('T0-6b ledger_integrity — 해에 실린 간선 원장 변조 · 다른 해의 원장 끼우기 → 진단 거부 · 진단 = 조립 원장')
    sid, res, P = chain_solve(0.2, CH_RT)
    chk('E2 해에 간선 원장 (막 행 = 조립이 쓴 것) · 지문', res.get('_iface', {}).get('kind') == 'am_iface_edges'
        and sum(len(ax['lin']) for ax in res['_iface']['axes']) == P['n_film_rows'])
    S3.phase_current_share(res, sid, te())
    bad = dict(res); bad['_iface'] = dict(res['_iface'])
    bad['_iface']['axes'] = tuple(dict(ax) for ax in res['_iface']['axes'])
    k = next(i for i, ax in enumerate(bad['_iface']['axes']) if len(ax['lin']))
    bad['_iface']['axes'][k]['g'] = bad['_iface']['axes'][k]['g'] * 2.0
    chk('T0-6b 원장 g 변조 → phase_current_share 거부', raises(lambda: S3.phase_current_share(bad, sid, te())))
    _, res2, _ = chain_solve(0.2, {k_: v * 3 for k_, v in CH_RT.items()})
    sw = dict(res); sw['_iface'] = res2['_iface']
    chk('T0-6b 다른 해 (r × 3) 의 원장을 끼움 → 거부 (φ 지문)', raises(lambda: S3.phase_current_share(sw, sid, te()))
        and raises(lambda: S3.per_particle_current(sw, sid, np.zeros(sid.shape, np.int32), te(), 1)))
    chk('E5 다른 σ 로 진단 → 거부', raises(lambda: S3.phase_current_share(res, sid, S3.electronic_sigma_table(0.02, 0.005, 100.0, 10.0, 250.0))))
    #  진단 함수가 원장을 재계산하지 않는다 (AST): 원장 · 계획 · face_rint 를 부르지 않고 iface_ctx 를 쓴다
    src = open(S3_PATH, encoding='utf-8').read()
    tree = ast.parse(src)
    fns = {n.name: n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)}
    bad_calls, uses = {}, {}
    for nm in ('phase_current_share', 'per_particle_current', '_voxel_jmag', 'joule_hotspot', 'field_point_cloud'):
        calls = {getattr(x.func, 'id', getattr(x.func, 'attr', None)) for x in ast.walk(fns[nm]) if isinstance(x, ast.Call)}
        bad_calls[nm] = calls & {'am_iface_ledger', 'am_iface_plan', 'iface_rface_ohm_cm2', '_iface_owner_select'}
        names = {getattr(x, 'id', None) for x in ast.walk(fns[nm])} | {getattr(x, 'arg', None) for x in ast.walk(fns[nm])}
        uses[nm] = bool(names & {'iface_ctx_from', 'iface_ctx'}) or 'iface_ctx_from' in calls
    chk('E2 (AST) 진단 다섯이 원장 · 계획을 다시 만들지 않는다 · 원장 맥락 (iface_ctx) 을 읽는다',
        not any(bad_calls.values()) and all(uses.values()), f'{bad_calls} {uses}')
    #  막 면에서 전류 연속 (진단 g = 조립 g) — 에너지 항등식이 진단 원장으로 맞는다 (T0-2)
    sh, tot = S3.phase_current_share(res, sid, te(), return_total=True)
    cc, gb, _ = res['plate_edges']['bot']
    I = float((np.asarray(gb) * (1.0 - res['phi'][cc])).sum())
    chk('T0-2 에너지 ledger: Σ P = I·ΔV (진단이 조립 원장 g 를 써야 맞는다 · 1e−10)', abs(tot / I - 1.0) < 1e-10, f'{tot / I - 1:.2e}')


@case('기록 필드 (v3 §6-6 이름) · PROTOCOL_FIELDS 밖 · a < h')
def t_record_fields():
    print('기록 — iface_model · iface_owner_rule · iface_area_law · iface_carbon_cover … · 정량 채택 HOLD 표지')
    sid, res, P = chain_solve(0.2, CH_RT)
    rec = res.get('iface') or {}
    want = {'iface_model': 'r2-owner-cnc', 'iface_owner_rule': 'claimant_power_partition_v1',
            'iface_tie_rule': 'global_pmin_eps_band_center_lex_v1', 'iface_area_law': 'contact_normalized_coarse_closure',
            'iface_carbon_cover': 'remove_area', 'iface_area_source': 'scaffold_lens_geometry',
            'iface_bridge_claim': 'union_both_orders_v1', 'iface_eps_p_um2': 1e-9, 'unit': 'ohm_cm2'}
    chk('기록 v3 이름 · 봉인 값', all(rec.get(k) == v for k, v in want.items()) and rec.get('solved') is True,
        repr({k: rec.get(k) for k in want}))
    chk('기록 키 전부 (예외 법칙 · 접촉 원장 요약 · 조인 표지 · 상태 · 한정어)',
        {'iface_exception_law', 'iface_contact_ledger', 'iface_join', 'iface_geom_reuse', 'iface_status',
         'iface_qualifiers', 'iface_r_type_ohm_cm2', 'iface_power_eval'} <= set(rec), sorted(rec))
    chk('상태 = 기구만 · 정량 채택 · 생산 HOLD · 검증 PASS 아님 · 한정어 (CNC ≠ 정확 · 2 Ω/1 Ω ≠ 상·하한)',
        'HOLD' in rec.get('iface_status', '') and 'PASS 아님' in rec.get('iface_status', '')
        and any('정확한 구현이 아니다' in q for q in rec.get('iface_qualifiers', ())))
    cl = rec.get('iface_contact_ledger') or {}
    chk('접촉 원장 요약: 부류 수 · a_lt_h (풀이 뒤 막 전류 몫) · 미등록 · 3중 · support/true · 쓴 막 행',
        cl.get('n_contacts', {}).get('contact') == 2 and isinstance(cl.get('a_lt_h', {}).get('film_current_share'), float)
        and 'unregistered' in cl and 'n_faces_triple' in cl and cl.get('support_over_true', {}).get('pre') is not None
        and cl.get('n_film_rows_used') == P['n_film_rows'], repr(cl)[:300])
    import run_contract as RC
    chk('PROTOCOL_FIELDS 에 iface 축이 없다 (정량 채택 HOLD — p2 코호트 그대로)',
        not any(str(f).startswith('iface') or 'iface' in str(f) for f in RC.PROTOCOL_FIELDS), repr(RC.PROTOCOL_FIELDS))
    #  a < h 접점의 막 전류 몫 — h 0.2 사슬 (a ≈ 0.31 µm > h) 은 0 · 굵은 격자 (h 0.4 > a) 는 1
    sid4, pid4, sp4 = raster(CH_C, CH_R, CH_T, CH_LO, CH_HI, 0.4, bridge_um=None)       # 기본 브리지 1.2·vox
    L4 = ledger(CH_C, CH_R, CH_T, sid4, sp4, CH_LO, 0.4, bridge_um=None)
    with direct_solver():
        r4 = quiet(S3.solve_sigma_z, sid4, te(), 0.4, return_field=True, z_bot_um=0.0, z_top_um=5.9,
                   iface=S3.am_iface_plan(L4, CH_RT))
    a4 = r4['iface']['iface_contact_ledger']['a_lt_h']
    chk('a_lt_h: h 0.4 > a → 수 2 · 막 전류 몫 1.0 · h 0.2 → 몫 0.0',
        a4['n'] == 2 and abs(a4['film_current_share'] - 1.0) < 1e-12
        and cl['a_lt_h']['film_current_share'] == 0.0, f"{a4} {cl['a_lt_h']}")


@case('PENDING (이 묶음 밖)')
def t_pending():
    print('PENDING — 계약에 있으나 이 묶음 밖 (실패가 아니라 보류 · 원장 · 보고에 남는다):')
    for p in ('N9 reject_film_off_outside — RRM (해상 기준 모형) 미구현 (T2-4 · T3-B 와 함께)',
              'T2-1′ · T2-2a/b/m · T2-4a/b · T3-D/B/P — D12-V 수치 봉인 전 (검증 PASS 발행 불가 · 개발 판만 가능)',
              'T4-1 ledger_census · T4-3 raster_order_size (RINTG-11) — 실침대 (real_14 · ps45 · Phase A) CPU census',
              'N1 reject_dilate · N5′ reject_frame · T4-2 join_gate — payload 배선 · 덤프 (c_cpl[22]) 경로 때',
              'T0-3′ 직접 R_j 간선 팔 · T1-5′ · T1-6~9 — ② 섬유 접합 단계',
              '탄소 경유 전류 몫 — 정의 미등록 (② 전 · 기록 not_computed)'):
        print(f'  PENDING  {p}')


def main():
    global S3, S3_PATH
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--s3', default=os.path.join(SCRIPTS, 'step3_sigma.py'),
                    help='시험할 step3_sigma.py 경로 (기본 = 리포 현 파일 · 고치기 전 blob 으로 실패를 기록할 때)')
    a = ap.parse_args()
    S3_PATH = os.path.abspath(a.s3)
    spec = importlib.util.spec_from_file_location('step3_sigma_under_test', S3_PATH)
    S3 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(S3)
    print(f'step3_sigma = {S3_PATH}')
    for tag, fn in CASES:
        print(f'\n── {tag}')
        try:
            fn()
        except Exception as e:                              # noqa: BLE001 — 옛 코드 (API 없음) 도 시험 단위로 기록
            chk(f'{tag}: 실행', False, f'{type(e).__name__}: {e}')
    print(f'\n{_ok} PASS · {len(_fail)} FAIL')
    if _fail:
        for n in _fail:
            print('  -', n)
        sys.exit(1)


if __name__ == '__main__':
    main()
