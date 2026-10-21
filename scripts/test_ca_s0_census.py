#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rint ② S0 표현 원장 — 시험 (시험 먼저 · 규율 ② · 2026-10-20).

정본 = docs/reviews/rint_carbon_additive_design_v1_20261020.md §2 (S0 ① 양 · ③ 계약 · ④ S0-1 … S0-7) · 등록 R
docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md §2-1 (문턱 식 · 숫자 = S0 단계 1 · 계획 해시) · §11 ④.

  python3 scripts/test_ca_s0_census.py

묶음:
  G   기하 원시 — 선분 최근접 (해석 · 무작위 대조) · 조각 규칙 (gap_tol) · 점 간격 u (조각 안만)
  C   접합 census 미리보기 (B0) — 손계산: 평행 접촉 · 수직 접촉 (스침 · 관통) · 떨어진 두 자리 · 꼭짓점 걸침 (J2c) ·
      U 턴 자기 접촉 · 문턱 경계 · 섬유 순열 불변 — ⚠ 접촉 길이 L_c 는 계약에 정의가 없어 두 판 (touch · band) 을 같이 낸다
  P   격자 원시 — 복셀 관계 · 포트 (직접 · 덮임 → 탐색 · 동률 · 미실현 · 상자 밖) · SDCP 경유 섬유 연결 · 부피로 이어진 깊이 ·
      교차 셀 멤버십 · 섬유–구 (J2b · T1-9)
  L   계획 — 식 (tol_ff = min(u, r_f) · L_par = 2(r_fi + r_fj) · r_port 0.30 · tol_P = tol_sj = tol_ff · K 8 · k 2) ·
      정준 바이트 · sha256 · 손댄 계획 거부 · 개정 커밋 대조 (임시 git 저장소: 통과 · 없음 · 조상 아님 · 해시 없음 ·
      계획 없음 · 전각 sha)
  S   스키마 — σ · 전류 · 소산 칸 없음 (S0-2)
  E   끝-끝 (payload 를 실제로 돌려 생산 raster 입력을 잡는다) — 픽스처 A (SBE 꼴 · 손계산 원장) · B (DBE 꼴) ·
      단계 관문 (S0-7) · 거부 (S0-5) · 순열 불변 (S0-4) · 상자 밖 · 판 위 (S0-6) · 위생 · 솔브 0 · 킷 폴더 불변 (S0-3) ·
      payload 자신의 rasterize-only 원장과 셀 수 대조 · 가로채기 안 걸림 = 거부
  R   접합 census 의 판정 · 보고 판 = B3 `carbon_junction.cjunc_registry` 와 **같은 함수** (설계 §4-1 끝 · 2 일 차) — 픽스처 J
      (나란한 두 섬유 = 긴 접촉 손계산 · U 자 섬유 = 자기 후보 · s 손계산) · 엿보기 (S0 가 그 함수를 off 격자 · 계획 문턱 · s_min 미등록
      으로 부르고 보고 · npz 가 그 원장 값 그대로) · 후보별 목록 (s · L_c · 배율) · 배율 합 · σ 칸 없음 · 단계 2 (픽스처 B)
  R8  ★ 10-21 (Codex RCA-03 · 05 · Q11 일부) census 보탬 — 픽스처 RV (판정문 RCA-03 고리 · 나란한 쌍 + 시작 근처 PTFE): 같은 셀 비연속
      재방문 (쌍 · 셀 · 섬유 · s) · 포트 동률 수 · 긴 접촉 · 분산 간선 · 간선별 PTFE 덮임 · 부분 덮임 instance · npz 간선별 배열 · σ 칸 없음
"""
import hashlib
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

import ca_s0_census as S0          # noqa: E402
import step3_sigma as S3           # noqa: E402

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


def run(name, fn):
    """묶음 하나 — 예외는 FAIL 로 센다 (구현 전 스텁의 NotImplementedError 포함)."""
    try:
        fn()
    except Exception as e:                                   # noqa: BLE001
        chk(name, False, f'{type(e).__name__}: {e}')


def raises(fn, exc=Exception):
    try:
        fn()
    except exc:
        return True
    except Exception:                                        # noqa: BLE001
        return False
    return False


def close(a, b, tol=1e-9):
    return a is not None and b is not None and abs(float(a) - float(b)) <= tol


R_F = 0.075                    # VGCF Ø0.15 / 2
THR = 2 * R_F + 0.075          # tol_ff = min(u, r_f) = 0.075 (u ≥ 0.075 in fixtures)
R_P = 0.124                    # PTFE rope Ø0.248 / 2


# ── 기하 원시 ──────────────────────────────────────────────────────────────────────────────────
def t_geometry():
    P1 = np.array([[0.0, 0, 0]]); Q1 = np.array([[1.0, 0, 0]])
    P2 = np.array([[0.5, -1, 0.3]]); Q2 = np.array([[0.5, 1, 0.3]])
    d, s, t, C1, C2 = S0.seg_seg_closest(P1, Q1, P2, Q2)
    chk('G1a 수직 엇갈림 — d = 0.3 · s = t = 0.5', close(d[0], 0.3, 1e-12) and close(s[0], 0.5, 1e-12)
        and close(t[0], 0.5, 1e-12))
    d, s, t, C1, C2 = S0.seg_seg_closest(np.array([[0.0, 0, 0]]), np.array([[2.0, 0, 0]]),
                                         np.array([[1.0, 0, 0.15]]), np.array([[3.0, 0, 0.15]]))
    chk('G1b 평행 겹침 — d = 0.15', close(d[0], 0.15, 1e-12))
    d, s, t, C1, C2 = S0.seg_seg_closest(np.array([[0.0, 0, 0]]), np.array([[0.0, 0, 0]]),
                                         np.array([[-1.0, 1, 0]]), np.array([[1.0, 1, 0]]))
    chk('G1c 퇴화 (점–선분) — d = 1', close(d[0], 1.0, 1e-12))
    rng = np.random.default_rng(7)
    A0, A1, B0, B1 = (rng.uniform(-1, 1, (300, 3)) for _ in range(4))
    B1[:40] = B0[:40] + (A1[:40] - A0[:40]) * rng.uniform(0.2, 2.0, (40, 1))     # 거의 평행 40 쌍
    d, s, t, C1, C2 = S0.seg_seg_closest(A0, A1, B0, B1)
    u = np.linspace(0, 1, 401)
    PA = A0[:, None, :] + u[None, :, None] * (A1 - A0)[:, None, :]
    PB = B0[:, None, :] + u[None, :, None] * (B1 - B0)[:, None, :]
    brute = np.sqrt(((PA[:, :, None, :] - PB[:, None, :, :]) ** 2).sum(-1)).min(axis=(1, 2))
    #  표본 401 점 = 매개변수 간격 1/400 → 가장 가까운 표본은 최근접점에서 각 선분 길이의 1/800 안 (1 차 오차 한계)
    bound = (np.linalg.norm(A1 - A0, axis=1) + np.linalg.norm(B1 - B0, axis=1)) / 800.0 + 1e-12
    chk('G1d 무작위 300 쌍 (평행 40 포함) — d ≤ 표본 최솟값 + 1e-12 · 차이 ≤ 표본 해상도 한계 (|d1| + |d2|)/800',
        bool((d <= brute + 1e-12).all() and (brute - d <= bound).all()),
        f'max diff {float((brute - d).max()):.3g} · worst ratio {float(((brute - d) / bound).max()):.3g}')
    chk('G1e 최근접점이 선분 위 · 거리 일치',
        bool(np.allclose(np.linalg.norm(C1 - C2, axis=1), d, atol=1e-12)
             and ((s >= 0) & (s <= 1) & (t >= 0) & (t <= 1)).all()))
    # 조각 규칙 = _fibre_segment_ijk 와 같은 식 (간격 > gap_tol · 중앙값 → 끊음)
    Q = np.array([[0.0, 0, 0], [0.3, 0, 0], [0.6, 0, 0], [0.9, 0, 0], [3.0, 0, 0], [3.3, 0, 0], [3.6, 0, 0]])
    pcs = S0.pieces_of(Q, 2.0)
    chk('G2a 조각 — 2.1 µm 틈에서 둘로 (4 점 · 3 점)', [len(p) for p in pcs] == [4, 3])
    st = S0.spacing_stats([pcs])
    chk('G2b 점 간격 = 조각 안 간격만 (틈 제외) — 중앙값 0.3 · u 0.15 · n 5',
        close(st['median_um'], 0.3, 1e-12) and close(st['u_um'], 0.15, 1e-12) and st['n'] == 5, str(st))
    chk('G2c 한 점 · 두 점 경로 — 조각 하나', [len(p) for p in S0.pieces_of(Q[:1], 2.0)] == [1]
        and [len(p) for p in S0.pieces_of(Q[:2], 2.0)] == [2])


# ── 접합 census 미리보기 (손계산) ─────────────────────────────────────────────────────────────
def _line(p0, p1, n):
    return np.linspace(np.asarray(p0, float), np.asarray(p1, float), n)


def _vv(paths, tol_ff=0.075, L_par=0.30):
    return S0.vv_census([(f, S0.pieces_of(np.asarray(P, float), 2.0)) for f, P in paths], R_F, tol_ff, L_par)


def t_census():
    # C1 평행 접촉 — A x∈[0,3] · B x∈[1,2] (z 0.15 = 2 r_f · 맞닿음)
    c = _vv([(0, _line([0, 0, 0], [3, 0, 0], 11)), (1, _line([1, 0, 0.15], [2, 0, 0.15], 5))])
    I = c['inst']
    Lb = 1.0 + 2 * math.sqrt(THR ** 2 - 0.15 ** 2)
    chk('C1a 평행 접촉 — instance 1', c['n_vv'] == 1 and c['n_self'] == 0, str((c['n_vv'], c['n_self'])))
    #  ⚠ 이 픽스처는 겹침 구간 전체가 정확히 d = D (퇴화 접점) — 제곱 거리 비교의 반올림이 양 끝에 √ulp(0.0225) ≈ 1.3e-9 씩
    #    남는다 (실측 2.6e-9) → L_touch 허용폭 1e-8 (L_band 는 경계가 비퇴화라 1e-9)
    chk('C1b L_touch = 겹침 길이 1.0 (퇴화 경계 1e-8) · L_band = 1 + 2√(thr² − 0.15²) = %.6f' % Lb,
        close(I['L_touch'][0], 1.0, 1e-8) and close(I['L_band'][0], Lb, 1e-9),
        f"{I['L_touch'][0]!r} {I['L_band'][0]!r}")
    chk('C1c 긴 접촉 (> L_par 0.30) — 두 판 모두 1 · 각 0°',
        c['n_long']['touch'] == 1 and c['n_long']['band'] == 1 and close(I['theta_deg'][0], 0.0, 1e-6))
    # C2 수직 스침 (중심 간격 0.15)
    c = _vv([(0, _line([-1, 0, 0], [1, 0, 0], 9)), (1, _line([0, -1, 0.15], [0, 1, 0.15], 9))])
    I = c['inst']
    Lb2 = 2 * math.sqrt(THR ** 2 - 0.15 ** 2)
    chk('C2a 수직 스침 — L_touch ≈ 0 · L_band = 2√(thr² − 0.15²) = %.6f · 틈 0' % Lb2,
        c['n_vv'] == 1 and I['L_touch'][0] < 1e-6 and close(I['L_band'][0], Lb2, 1e-9)
        and close(I['gap'][0], 0.0, 1e-12), f"{I['L_touch'][0]!r} {I['L_band'][0]!r}")
    chk('C2b ★ 정의 쟁점 — 같은 수직 스침이 band 판에서는 긴 접촉 (0.335 > 0.30) · touch 판에서는 아님',
        c['n_long']['touch'] == 0 and c['n_long']['band'] == 1)
    # C3 수직 관통 (중심 간격 0.10)
    c = _vv([(0, _line([-1, 0, 0], [1, 0, 0], 9)), (1, _line([0, -1, 0.10], [0, 1, 0.10], 9))])
    I = c['inst']
    chk('C3 수직 관통 — 틈 −0.05 · L_touch 2√(0.15²−0.1²) · L_band 2√(thr²−0.1²) · 90°',
        close(I['gap'][0], -0.05, 1e-12) and close(I['L_touch'][0], 2 * math.sqrt(0.0225 - 0.01), 1e-9)
        and close(I['L_band'][0], 2 * math.sqrt(THR ** 2 - 0.01), 1e-9) and close(I['theta_deg'][0], 90.0, 1e-6))
    # C4 같은 쌍의 떨어진 두 자리 = instance 둘
    B = np.array([[0.5, -1, 0.1], [0.5, 0, 0.1], [0.5, 1, 0.1], [1.5, 1, 0.1], [2.5, 1, 0.1], [2.5, 0, 0.1],
                  [2.5, -1, 0.1]])
    c = _vv([(0, _line([0, 0, 0], [3, 0, 0], 31)), (1, B)])
    chk('C4 떨어진 두 자리 — instance 2', c['n_vv'] == 2, str(c['n_vv']))
    # C5 J2c — A 의 꼭짓점이 교차점 위 (선분 둘에 걸친 접촉 = 하나)
    c = _vv([(0, np.array([[-1.0, 0, 0], [0, 0, 0], [1.0, 0, 0]])), (1, _line([0, -1, 0.1], [0, 1, 0.1], 3))])
    chk('C5 꼭짓점 걸침 — instance 1 (조각 · 선분 경계 넘어도)', c['n_vv'] == 1, str(c['n_vv']))
    # C6 자기 접촉 — U 턴 (지름 0.2 ≤ thr) = 1 · 직선 = 0 · 꺾임 (V · 반원 아님) = 0
    th = np.linspace(-math.pi / 2, math.pi / 2, 7)
    U = np.vstack([_line([-2, -0.1, 0], [0, -0.1, 0], 8)[:-1],
                   np.column_stack([0.1 * np.cos(th), 0.1 * np.sin(th), np.zeros_like(th)]),
                   _line([0, 0.1, 0], [-2, 0.1, 0], 8)[1:]])
    c = _vv([(0, U)])
    chk('C6a U 턴 — 자기 접촉 instance 1', c['n_self'] == 1 and c['n_vv'] == 0, str((c['n_vv'], c['n_self'])))
    c = _vv([(0, _line([0, 0, 0], [5, 0, 0], 21))])
    chk('C6b 직선 — 자기 접촉 0', c['n_self'] == 0)
    V = np.array([[0.0, 0, 0], [0.3, 0, 0], [0.6, 0, 0], [0.55, 0.15, 0], [0.5, 0.3, 0], [0.45, 0.45, 0]])
    c = _vv([(0, V)])
    chk('C6c 날카로운 꺾임 (반원 아님) — 자기 접촉 0', c['n_self'] == 0, str(c['n_self']))
    # C7 문턱 경계 — thr 밖 0 · 안 (맞닿지 않음) 1 · L_touch 0
    c0 = _vv([(0, _line([-1, 0, 0], [1, 0, 0], 9)), (1, _line([0, -1, THR + 0.01], [0, 1, THR + 0.01], 9))])
    c1 = _vv([(0, _line([-1, 0, 0], [1, 0, 0], 9)), (1, _line([0, -1, THR - 0.001], [0, 1, THR - 0.001], 9))])
    chk('C7 문턱 — thr + 0.01 → 0 · thr − 0.001 → 1 (L_touch 0)',
        c0['n_vv'] == 0 and c1['n_vv'] == 1 and c1['inst']['L_touch'][0] < 1e-12)
    # C8 순열 불변 — 경로 순서 · fid 이름 바꿈
    paths = [(0, _line([0, 0, 0], [3, 0, 0], 11)), (1, _line([1, 0, 0.15], [2, 0, 0.15], 5)),
             (2, _line([0.5, -1, 0.05], [0.5, 1, 0.05], 9)), (3, B)]
    a = _vv(paths)
    b = _vv([(17, paths[3][1]), (5, paths[1][1]), (40, paths[0][1]), (2, paths[2][1])])
    same = (a['n_vv'] == b['n_vv'] and a['n_self'] == b['n_self'] and a['n_long'] == b['n_long']
            and all(np.array_equal(np.sort(a['inst'][k]), np.sort(b['inst'][k]))
                    for k in ('gap', 'L_touch', 'L_band', 'theta_deg')))
    chk('C8 섬유 순열 · 이름 불변 — 수 · 분포 같음', same, f"{a['n_vv']} vs {b['n_vv']}")
    #  C8b 무작위 섬유 묶음 — 비대칭 기하에서도 **비트** 같음 (두 선분의 계산 순서 = 좌표 사전순 정준 · 입력 순서 · 이름 무관)
    rng = np.random.default_rng(11)
    rp = []
    for f in range(40):
        p0 = rng.uniform(0, 1.5, 3); u_ = rng.normal(size=3); u_ /= np.linalg.norm(u_)
        n_ = int(rng.integers(6, 12))
        rp.append((f, p0 + np.outer(np.arange(n_) * rng.uniform(0.25, 0.35), u_)))
    a = _vv(rp)
    perm = rng.permutation(len(rp))
    b = _vv([(100 + 7 * int(k), rp[int(k)][1]) for k in perm[::-1]])
    keys = ('gap', 'L_touch', 'L_band', 'theta_deg', 'd_min')
    chk('C8b 무작위 40 섬유 — instance ≥ 5 · 순열 · 이름 바꿔도 분포가 비트 같음',
        a['n_vv'] >= 5 and a['n_vv'] == b['n_vv'] and a['n_self'] == b['n_self']
        and all(np.array_equal(np.sort(a['inst'][k]), np.sort(b['inst'][k])) for k in keys),
        f"{a['n_vv']} vs {b['n_vv']} · " + str([k for k in keys if not np.array_equal(np.sort(a['inst'][k]),
                                                                                      np.sort(b['inst'][k]))]))
    chk('C9 정의 표지 — lc_definition 이 두 판을 이름으로 싣는다',
        isinstance(a.get('lc_definition'), dict) and set(a['lc_definition']) >= {'touch', 'band'})


# ── 격자 원시 ───────────────────────────────────────────────────────────────────────────────────
def t_grid():
    rel = S0.voxel_relation
    chk('P1 복셀 관계 — same · face · edge · vertex · apart',
        [rel((1, 1, 1), x) for x in ((1, 1, 1), (1, 1, 2), (1, 2, 2), (2, 2, 2), (1, 1, 3))]
        == ['same', 'face', 'edge', 'vertex', 'apart'])
    vox = 0.1; lo = np.zeros(3)
    G = np.zeros((20, 6, 6), np.int8)
    cells = np.array([[i, 2, 2] for i in range(2, 18)])
    G[cells[:, 0], cells[:, 1], cells[:, 2]] = 3
    st, cell, dist = S0.port_of(np.array([0.95, 0.25, 0.25]), cells, G, lo, vox, 0.30)
    chk('P2a 포트 직접 — 셀 (9,2,2) · 거리 0', st == 'direct' and tuple(cell) == (9, 2, 2) and dist < 1e-12,
        str((st, cell, dist)))
    G2 = G.copy(); G2[9, 2, 2] = 5
    st, cell, dist = S0.port_of(np.array([0.95, 0.25, 0.25]), cells, G2, lo, vox, 0.30)
    chk('P2b 덮임 (SDCP) → 탐색 — 등거리 (8 · 10) 동률 = 경로 열 번호 작은 (8,2,2) · 거리 0.1',
        st == 'covered:SDCP→searched' and tuple(cell) == (8, 2, 2) and close(dist, 0.1, 1e-12), str((st, cell, dist)))
    G3 = G.copy(); G3[5:14, 2, 2] = 5
    st, cell, dist = S0.port_of(np.array([0.95, 0.25, 0.25]), cells, G3, lo, vox, 0.30)
    chk('P2c r_port 안에 sid 3 없음 → 미실현', st == 'covered:SDCP→unrealized' and cell is None, str(st))
    st, cell, dist = S0.port_of(np.array([5.0, 0.25, 0.25]), cells, G, lo, vox, 0.30)
    chk('P2d 상자 밖 → outside_box', st == 'outside_box' and cell is None, str(st))
    # P3 SDCP 경유 섬유 연결 — 덩어리 하나가 두 섬유 셀에 면으로 닿음
    G = np.zeros((8, 8, 3), np.int8)
    G[1:7, 2, 1] = 3; G[1:7, 5, 1] = 3; G[3, 3:5, 1] = 5; G[6, 6, 1] = 5
    lin = np.ravel_multi_index(np.nonzero(G == 3), G.shape)
    fid = np.where(np.unravel_index(lin, G.shape)[1] == 2, 10, 20)
    v = S0.sdcp_via(G, lin, fid)
    chk('P3 SDCP 경유 — 덩어리 2 · 두 섬유를 잇는 것 1 · fid 쌍 1',
        v['n_components'] == 2 and v['n_bridging'] == 1 and v['n_fid_pairs'] == 1, str(v))
    # P4 부피로 이어진 깊이 (k = 2)
    G = np.zeros((10, 3, 3), np.int8)
    pa, pb = np.array([1, 1, 1]), np.array([3, 1, 1])
    G[1, 1, 1] = G[3, 1, 1] = 3; G[2, 1, 1] = 5
    d1 = S0.via_sdcp_depth(G, pa, pb, 2)
    G = np.zeros((10, 3, 3), np.int8); pb = np.array([4, 1, 1])
    G[1, 1, 1] = G[4, 1, 1] = 3; G[2:4, 1, 1] = 5
    d2 = S0.via_sdcp_depth(G, pa, pb, 2)
    G = np.zeros((10, 3, 3), np.int8); pb = np.array([5, 1, 1])
    G[1, 1, 1] = G[5, 1, 1] = 3; G[2:5, 1, 1] = 5
    d3 = S0.via_sdcp_depth(G, pa, pb, 2)
    chk('P4 SDCP 셀 1 · 2 · 3 개 사이 → 깊이 1 · 2 · 없음 (k = 2)', (d1, d2, d3) == (1, 2, None), str((d1, d2, d3)))
    # P5 교차 셀 멤버십
    a = np.array([[i, 1, 1] for i in range(5)]); b = np.array([[2, j, 1] for j in range(5)])
    c3 = np.array([[2, 1, k] for k in range(3)])
    lin, cnt = S0.membership_counts([a, b, c3], (6, 6, 6))
    chk('P5 교차 셀 — 멤버십 ≥ 2 한 셀 · ≥ 3 한 셀 (2,1,1)',
        int((cnt >= 2).sum()) == 1 and int((cnt >= 3).sum()) == 1
        and int(lin[cnt >= 3][0]) == int(np.ravel_multi_index((2, 1, 1), (6, 6, 6))))
    # P6 J2b · T1-9 — r_f 0.075 · R_AM 2 · d 2.12 = 접촉 아님 · 2.07 = 접촉 (tol_fs 0)
    paths = [(0, S0.pieces_of(_line([-1, 2.12, 0], [1, 2.12, 0], 9), 2.0)),
             (1, S0.pieces_of(_line([-1, -2.07, 0], [1, -2.07, 0], 9), 2.0))]
    fs = S0.fiber_sphere_instances(paths, np.zeros((1, 3)), np.array([2.0]), R_F, 0.0)
    chk('P6 섬유–구 (T1-9) — d 2.12 아님 · 2.07 맞음 → instance 1',
        fs['n_instances'] == 1 and close(fs['gap_um'][0], 2.07 - 2.075, 1e-9), str(fs))


# ── 계획 ───────────────────────────────────────────────────────────────────────────────────────
def _src():
    return {'stage': 1, 'kit_name': 'kit_fixture'}


def t_plan():
    p, b, h = S0.make_plan(0.15, R_F, 2.0, _src())
    v = p['values_um']
    chk('L1a 식 — u 0.15 → tol_ff = min(u, r_f) = 0.075 · L_par 0.30 · r_port 0.30 · tol_P = tol_sj = tol_ff',
        close(v['u'], 0.15, 0) and close(v['tol_ff'], 0.075, 0) and close(v['L_par'], 0.30, 1e-15)
        and close(v['r_port'], 0.30, 0) and v['tol_P'] == v['tol_ff'] == v['tol_sj'], str(v))
    p2, b2, h2 = S0.make_plan(0.05, R_F, 2.0, _src())
    chk('L1b u 0.05 → tol_ff 0.05', close(p2['values_um']['tol_ff'], 0.05, 0))
    chk('L1c K_alpha 8 · k 2 · gap_tol 2.0', p['integers'] == {'K_alpha': 8, 'k_sdcp_cells': 2} and p['gap_tol'] == 2.0)
    chk('L1d 정준 바이트 · sha256 = 바이트의 sha256 · 다시 만들어도 같음',
        h == hashlib.sha256(b).hexdigest() and S0.plan_bytes_of(p) == b and S0.make_plan(0.15, R_F, 2.0, _src())[2] == h)
    chk('L1e 계획에 σ 칸 없음', S0.schema_forbidden_keys(p) == [])
    bad = json.loads(b.decode()); bad['values_um']['tol_ff'] = 0.06
    chk('L2a 손댄 계획 (tol_ff ≠ min(u, r_f)) 거부', raises(lambda: S0.check_plan(bad), S0.S0Error))
    bad = json.loads(b.decode()); bad['values_um']['u'] = float('nan')
    chk('L2b 비유한 u 거부', raises(lambda: S0.check_plan(bad), S0.S0Error))
    bad = json.loads(b.decode()); bad['schema'] = 'other'
    chk('L2c 다른 스키마 거부', raises(lambda: S0.check_plan(bad), S0.S0Error))
    chk('L2d 정상 계획 통과', S0.check_plan(json.loads(b.decode())) is None)


def _git(repo, *a):
    return subprocess.run(['git', '-C', repo, '-c', 'user.name=s0test', '-c', 'user.email=s0@test', *a],
                          capture_output=True, text=True, check=True).stdout.strip()


def make_plan_repo(d, plan_bytes, plan_sha, *, put_hash=True, put_plan=True):
    """임시 git 저장소 — R 문서 (계획 해시 줄) + 계획 파일을 한 커밋에.  → (repo, sha, plan_rel, r_doc_rel)."""
    repo = os.path.join(d, 'repo')
    os.makedirs(os.path.join(repo, 'docs', 'reviews'))
    os.makedirs(os.path.join(repo, 'docs', 'data', 's0'))
    _git(repo, 'init', '-q')
    r_rel = 'docs/reviews/R.md'; p_rel = 'docs/data/s0/cjunc_plan.json'
    with open(os.path.join(repo, 'README'), 'w') as f:
        f.write('base\n')
    _git(repo, 'add', '-A'); _git(repo, 'commit', '-qm', 'base')
    with open(os.path.join(repo, r_rel), 'w', encoding='utf-8') as f:
        f.write('# R §2-1 개정\n' + (f'| 계획 해시 | `CJUNC_PLAN` sha256 | {plan_sha} |\n' if put_hash else '(해시 없음)\n'))
    if put_plan:
        with open(os.path.join(repo, p_rel), 'wb') as f:
            f.write(plan_bytes)
    _git(repo, 'add', '-A'); _git(repo, 'commit', '-qm', 'R 2-1 revision')
    return repo, _git(repo, 'rev-parse', 'HEAD'), p_rel, r_rel


def t_plan_commit():
    p, b, h = S0.make_plan(0.15, R_F, 2.0, _src())
    with tempfile.TemporaryDirectory() as d:
        repo, sha, prel, rrel = make_plan_repo(d, b, h)
        ok = S0.verify_plan_commit(repo, sha, prel, r_doc=rrel)
        chk('L3a 개정 커밋 · 계획 · 해시 일치 → 통과 (계획 · sha256 · 전체 sha)',
            ok[1] == h and ok[0]['values_um'] == p['values_um'] and ok[2] == sha)
        chk('L3b 없는 커밋 거부', raises(lambda: S0.verify_plan_commit(repo, 'deadbeef' * 5, prel, r_doc=rrel),
                                          S0.S0Error))
        chk('L3c 전각 · 비 ASCII sha 거부', raises(lambda: S0.verify_plan_commit(repo, '０' * 40, prel, r_doc=rrel),
                                                  S0.S0Error))
        chk('L3d 계획 경로 없음 거부', raises(lambda: S0.verify_plan_commit(repo, sha, 'docs/none.json', r_doc=rrel),
                                            S0.S0Error))
        # 조상 아님 — 다른 가지의 커밋
        base = _git(repo, 'rev-parse', 'HEAD~1')
        _git(repo, 'checkout', '-q', '-b', 'side', base)
        with open(os.path.join(repo, 'side.txt'), 'w') as f:
            f.write('x\n')
        _git(repo, 'add', '-A'); _git(repo, 'commit', '-qm', 'side')
        chk('L3e HEAD 의 조상 아닌 커밋 거부 (가지 밖)',
            raises(lambda: S0.verify_plan_commit(repo, sha, prel, r_doc=rrel), S0.S0Error))
    with tempfile.TemporaryDirectory() as d:
        repo, sha, prel, rrel = make_plan_repo(d, b, h, put_hash=False)
        chk('L3f R 문서에 계획 해시 없음 거부', raises(lambda: S0.verify_plan_commit(repo, sha, prel, r_doc=rrel),
                                                    S0.S0Error))
    with tempfile.TemporaryDirectory() as d:
        bb = b.replace(b'"gap_tol":2.0', b'"gap_tol":2.5')
        repo, sha, prel, rrel = make_plan_repo(d, bb, hashlib.sha256(bb).hexdigest())
        chk('L3g 커밋 안 계획이 식 어긋남 (손댐) → 거부', raises(lambda: S0.verify_plan_commit(repo, sha, prel, r_doc=rrel),
                                                         S0.S0Error))


def t_schema():
    bad = {'a': {'b': [{'sigma_e_eff': 1.0}]}, 'ok': 1}
    chk('S1a σ 칸 찾기 (중첩 · 목록)', S0.schema_forbidden_keys(bad) == ['a.b[0].sigma_e_eff'],
        str(S0.schema_forbidden_keys(bad)))
    chk('S1b 전류 · 소산 · 컨덕턴스 칸도', len(S0.schema_forbidden_keys(
        {'je_current': 1, 'dissipation_share': 2, 'conductance_g': 3, 'n_dof': 4})) == 4)
    chk('S1c 깨끗한 dict', S0.schema_forbidden_keys({'cells_by_sid': {'3': 1}, 'u_um': 0.1}) == [])


# ── 끝-끝 픽스처 (payload 실물) ────────────────────────────────────────────────────────────────
UMB, SW0, FL = 10.0, 0.04, 0.05           # µm / box · viz_mpm_continuum SW[0] · FLOOR
VOX = 0.1                                 # 손계산 격자 (구 Ø0.30 → 1.5 vox · 경계 여유 큼)

PAYLOAD_BLOCK = '''python3 "$SCR/mpm_webapp_payload.py" \\
  --se se_dump.npy --scaffold "$KIT/am_scaffold.csv" \\
  --n-vox 48 --tri-step 4 --smooth 1.5 --void-max 1000 --step3-vox 0.4 --metrics-json mpm_metrics.json --case fx --phase phase.npy --fibre fibre.npy --fibre-dia fibre_dia.npy{extra} --save-step4-grid step4_grid.npz --out mpm_payload.json \\
  || {{ echo "[run_mpm] STEP 2 (payload) FAILED"; exit 1; }}
'''

F1 = np.column_stack([2.05 + 0.3 * np.arange(14), np.full(14, 4.55), np.full(14, 2.05)])
P1 = np.column_stack([np.full(15, 4.05), 2.05 + 0.35 * np.arange(15), np.full(15, 2.05)])
F2 = np.column_stack([np.full(15, 5.05), 2.05 + 0.35 * np.arange(15), np.full(15, 2.15)])
S1 = np.array([[3.05, 4.55, 2.05]])
SE = np.array([[0.35 + 0.5 * a, 0.35 + 0.5 * b, 1.05] for a in range(18) for b in range(18)])
#  AM 둘 — 한 줄짜리 scaffold CSV 는 np.loadtxt 가 1 차원으로 돌려줘 payload 의 load_am 이 IndexError (실침대 AM 1271 개 = 무관 ·
#  픽스처 결함 · 처음 판에서 E1 · E10 · E11 이 그것으로 실패).  둘째 AM 은 섬유 · PTFE · SE 와 멀다.
AM = [(2, 1.0, 1.0, 2.5, 1.0), (2, 8.0, 1.0, 2.5, 1.0)]
V_SDCP1 = math.pi / 6 * 0.3 ** 3


def write_kit(root, name, *, vgcf, ptfe, sdcp=None, se=SE, am=AM, vol=None, extra='', mutate=None,
              kind=True, thickness=3.5):
    """킷 꼴 폴더 — run_mpm.sh (payload 블록) · am_scaffold.csv (mm) · latest_run → run_X/ (상자 단위 npy · metrics)."""
    kit = os.path.join(root, name)
    run_d = os.path.join(kit, 'run_fx_20261020_000000_1')
    os.makedirs(run_d)
    with open(os.path.join(kit, 'am_scaffold.csv'), 'w') as f:
        f.write('# type,x,y,z,r (mm)\n')
        for t, x, y, z, r in am:
            f.write(f'{t},{x / 1000:.9f},{y / 1000:.9f},{z / 1000:.9f},{r / 1000:.9f}\n')
    with open(os.path.join(kit, 'run_mpm.sh'), 'w') as f:
        f.write('#!/usr/bin/env bash\nset -uo pipefail\nKIT="$(cd "$(dirname "$0")" && pwd)"\n'
                + PAYLOAD_BLOCK.format(extra=extra) + 'ln -sfn "$RUN_DIR" "$KIT/latest_run"\n')
    pts, ph, fid, knd = [np.asarray(se, float)], [np.ones(len(se), np.int8)], [np.full(len(se), -1, np.int32)], \
        [np.zeros(len(se), np.int8)]
    nid = 0
    for P in vgcf:
        pts.append(np.asarray(P, float)); ph.append(np.full(len(P), 2, np.int8))
        fid.append(np.full(len(P), nid, np.int32)); knd.append(np.ones(len(P), np.int8)); nid += 1
    for P in ptfe:
        pts.append(np.asarray(P, float)); ph.append(np.full(len(P), 4, np.int8))
        fid.append(np.full(len(P), nid, np.int32)); knd.append(np.ones(len(P), np.int8)); nid += 1
    if sdcp is not None and len(sdcp):
        pts.append(np.asarray(sdcp, float)); ph.append(np.full(len(sdcp), 5, np.int8))
        fid.append(np.full(len(sdcp), 100000, np.int32)); knd.append(np.zeros(len(sdcp), np.int8))
    U = np.vstack(pts); PH = np.concatenate(ph); FI = np.concatenate(fid); KI = np.concatenate(knd)
    box = np.column_stack([SW0 + U[:, 0] / UMB, SW0 + U[:, 1] / UMB, FL + U[:, 2] / UMB])
    arrs = {'se_dump.npy': box, 'phase.npy': PH, 'fibre.npy': FI, 'fibre_kind.npy': KI,
            'fibre_dia.npy': np.ones(len(U), np.float32)}
    if mutate:
        mutate(arrs)
    for k, v in arrs.items():
        if v is not None:
            np.save(os.path.join(run_d, k), v)
    if not kind:
        os.remove(os.path.join(run_d, 'fibre_kind.npy'))
    met = {'um_box_um': UMB, 'thickness_um': thickness, 'porosity_settled_pct': 7.0,
           'E_anchor': 'ADD_E_SET_FIXTURE', 'additives': {k: {'vol_um3': v} for k, v in (vol or {}).items()}}
    with open(os.path.join(run_d, 'mpm_metrics.json'), 'w') as f:
        json.dump(met, f)
    open(os.path.join(run_d, 'mpm_done.marker'), 'w').close()
    os.symlink(run_d, os.path.join(kit, 'latest_run'))
    return kit


def _stage(stage, kits, out, **kw):
    return S0.run_stage(stage, kits, out, vox=VOX, bridge_um=0.48, sdcp_sphere_d=0.30, **kw)


def _load(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def _snap(d):
    out = {}
    for base, dirs, files in os.walk(d):
        for n in sorted(files):
            p = os.path.join(base, n)
            st = os.lstat(p)
            out[os.path.relpath(p, d)] = (st.st_size, st.st_mtime_ns)
    return out


def _capsule(P, r=R_P):
    L = float(np.linalg.norm(np.diff(P, axis=0), axis=1).sum())
    return L * math.pi * r * r + 4.0 / 3.0 * math.pi * r ** 3


STATE = {}


def t_e2e_stage1():
    tmp = STATE['tmp']
    kitA = write_kit(tmp, 'kit_A', vgcf=[F1], ptfe=[P1], vol={'VGCF': 0.04, 'PTFE': 0.1})
    STATE['kitA'] = kitA
    out = os.path.join(tmp, 'outA')
    ref_in = (np.array([[0.5, 0.5, 0.5]]), np.array([0.3]), np.array([2]), None, None, (0, 0, 0), (1.0, 1.0, 1.0), 0.1)
    ref_sid = S3.rasterize(*ref_in)[0].copy()
    before = {k: getattr(S3, k) for k in ('rasterize', 'GPU_SOLVE', 'CG_MAXITER', 'AMG_SOLVE', 'REQUIRE_GPU')}
    snap0 = _snap(kitA)

    def boom(*_a, **_k):
        raise AssertionError('S0 가 솔버를 불렀다')
    saved = {k: getattr(S3, k) for k in ('solve_sigma_z', '_solve_cg', 'solve_thermal')}
    for k in saved:
        setattr(S3, k, boom)
    try:
        res = _stage(1, [kitA], out)
    finally:
        for k, v in saved.items():
            setattr(S3, k, v)
    chk('E3 솔브 0 — solve_sigma_z · _solve_cg · solve_thermal 를 터지게 해도 단계 1 완주', isinstance(res, dict))
    after = {k: getattr(S3, k) for k in before}
    chk('E2a 위생 — rasterize · GPU · CG 노브가 원래 그대로', after == before, str([k for k in before if after[k] != before[k]]))
    chk('E2b 위생 — 같은 입력의 rasterize 결과 비트 같음 (전 · 후)',
        np.array_equal(S3.rasterize(*ref_in)[0], ref_sid))
    chk('E4a 킷 폴더 불변 (이름 · 크기 · mtime)', _snap(kitA) == snap0)
    names = sorted(os.listdir(out))
    chk('E4b payload 산출물 없음 (가로채기 = rasterize 전에 멈춤)',
        not any(n.startswith('_payload_') for n in names) and 's0_stage1_kit_A.json' in names
        and 'cjunc_plan.json' in names, str(names))
    rep = _load(os.path.join(out, 's0_stage1_kit_A.json'))
    STATE['repA'] = rep
    with open(os.path.join(out, 'cjunc_plan.json'), 'rb') as f:
        STATE['planA'] = f.read()
    cbs = rep['raster']['cells_by_sid']
    chk('E1a 생산 격자 — VGCF 39 · PTFE 50 · SE 324 (손계산)',
        cbs['prod'].get('3') == 39 and cbs['prod'].get('7') == 50 and cbs['prod'].get('6') == 324, str(cbs['prod']))
    chk('E1b off 격자 (= face_alpha sid 격자) — VGCF 40 · PTFE 0 · AM 같음',
        cbs['off'].get('3') == 40 and '7' not in cbs['off'] and cbs['off'].get('1') == cbs['prod'].get('1'),
        str(cbs['off']))
    L = rep['ledger']
    chk('E1c PTFE 가 덮은 셀 — off sid {3: 1 · 0: 49}', L['ptfe_cover']['prod_sid7_cells_by_off_sid'] == {'0': 49, '3': 1},
        str(L['ptfe_cover']))
    chk('E1d PTFE 가 끊은 VGCF 경로 — 1 개 · 조각 +1', L['ptfe_cut']['paths_cut'] == 1
        and L['ptfe_cut']['extra_components'] == 1 and L['ptfe_cut']['paths_total'] == 1, str(L['ptfe_cut']))
    vr = L['volume_ratio']
    chk('E1e 표현 부피 비 — VGCF 0.975 (생산) · 1.0 (off) · PTFE 0.5',
        close(vr['prod']['VGCF'], 0.975, 1e-12) and close(vr['off']['VGCF'], 1.0, 1e-12)
        and close(vr['prod']['PTFE'], 0.5, 1e-12), str(vr))
    cap = L['capsule']
    chk('E1f 캡슐 부피 비 = (Σ 선분 원기둥 + 조각마다 구 하나) / V_true — %.6f · 밴드 [0.5, 2] 밖' % (_capsule(P1) / 0.1),
        close(cap['volume_ratio'], _capsule(P1) / 0.1, 1e-9) and cap['in_band'] is False, str(cap))
    ti = rep['threshold_inputs']; tu = rep['thresholds_used']
    chk('E1g 문턱 입력 — 점 간격 중앙값 0.3 · u 0.15 · tol_ff 0.075 · L_par 0.30 · r_port 0.30',
        close(ti['spacing_median_um'], 0.3, 1e-9) and close(ti['u_um'], 0.15, 1e-9)
        and close(tu['tol_ff_um'], 0.075, 0) and close(tu['L_par_um'], 0.30, 1e-15) and close(tu['r_port_um'], 0.30, 0),
        str((ti, tu)))
    chk('E1h 계획 파일 sha256 = 보고의 plan.sha256 · 계획 = stage1 계산',
        hashlib.sha256(STATE['planA']).hexdigest() == rep['plan']['sha256'] and rep['plan']['source'] == 'stage1_computed')
    cp = rep['census_preview']
    chk('E1i 접합 census = B0 미리보기 표지 · VV 0 (섬유 하나)',
        cp['status'] == 'b0_preview' and 'verdict_use' in cp and cp['vv']['n_instances'] == 0, str(cp.get('status')))
    al = L.get('alpha') or {}
    named = [x.strip() for x in str(al.get('function', '')).replace('ptfe_face_alpha.', '').split('·') if x.strip()]
    import ptfe_face_alpha as FA
    chk('E1j α 분포 = S1 함수로 계산 (status computed · 사유 문장에 "함수가 없다" 류 주장 없음 · 이름 붙은 함수가 ptfe_face_alpha 에 실제로 '
        '있다 · K 8 · rope · off 격자)',
        al.get('status') == 'computed' and str(al.get('function', '')).startswith('ptfe_face_alpha.') and len(named) >= 3
        and all(callable(getattr(FA, nm, None)) for nm in named) and '없다' not in json.dumps(al, ensure_ascii=False)
        and al.get('K') == FA.K_SEALED and al.get('dia_law') == 'rope' and al.get('grid') == 'off'
        and al.get('operator') == FA.S1_OPERATOR_VERSION, str({k: al.get(k) for k in ('status', 'function', 'reason')}))
    notes = rep.get('notes') or []
    import carbon_junction as CJ
    chk('E1o 보고 notes 의 L_c 문장 — 판정 · 보고 판 L_c = 설계 §1-2 #13 (Q17) touch = cjunc_registry 규칙 이름 · '
        '"설계 · 등록 R 에 없다" 류 옛 주장 없음 (미리보기 두 판은 비교용)',
        any(CJ.CJUNC_LC_RULE in n for n in notes) and not any('에 없다' in n for n in notes),
        str([n[:60] for n in notes if 'L_c' in n]))
    chk('S0-2 보고 · 계획에 σ · 전류 · 소산 칸 없음',
        S0.schema_forbidden_keys(rep) == [] and S0.schema_forbidden_keys(json.loads(STATE['planA'])) == [],
        str(S0.schema_forbidden_keys(rep)[:5]))
    chk('E1k 코드 · 입력 지문 기록 (git · 파일 sha256 · 침대 점 수)',
        rep['code'].get('tool_sha256') and len(rep['inputs']['files']) >= 5
        and rep['inputs']['counts']['points_by_phase'] == {'1': 324, '2': 14, '4': 15})


def t_e2e_reject_stage():
    tmp = STATE['tmp']
    kitB = write_kit(tmp, 'kit_B', vgcf=[F1, F2], ptfe=[P1], sdcp=S1,
                     vol={'VGCF': 0.09, 'PTFE': 0.1, 'SDCP': V_SDCP1})
    STATE['kitB'] = kitB
    out = os.path.join(tmp, 'outB1')
    rej = raises(lambda: _stage(1, [kitB], out), S0.S0Error)
    chk('E6 단계 1 + SDCP 있는 침대 → 거부 (DBE 분포는 개정 커밋 뒤)', rej)
    chk('E6b 그 거부가 가로채기 전 (payload 로그 없음 · 헛통과 방지 = 거부가 실제로 일어났을 때만)',
        rej and (not os.path.exists(out) or not any(n.startswith('payload_capture') for n in os.listdir(out))))
    out2 = os.path.join(tmp, 'outB2a')
    chk('S0-7a 단계 2 + 개정 커밋 없음 → 거부', raises(lambda: _stage(2, [kitB], out2), S0.S0Error))
    chk('S0-7b 단계 1 에 킷 둘 → 거부', raises(lambda: _stage(1, [STATE['kitA'], STATE['kitA']],
                                                              os.path.join(tmp, 'outAA')), S0.S0Error))


def t_e2e_stage2():
    tmp = STATE['tmp']
    planA = STATE['planA']; h = hashlib.sha256(planA).hexdigest()
    repo, sha, prel, rrel = make_plan_repo(os.path.join(tmp, 'g'), planA, h)
    out = os.path.join(tmp, 'outB2')
    _stage(2, [STATE['kitB']], out, threshold_commit=sha, plan_path=prel, repo=repo, r_doc=rrel)
    rep = _load(os.path.join(out, 's0_stage2_kit_B.json'))
    STATE['repB'] = rep
    chk('E7a 단계 2 — 계획 = 커밋에서 (sha · 해시)', rep['plan']['source'] == f'commit:{sha}' and rep['plan']['sha256'] == h)
    cbs = rep['raster']['cells_by_sid']
    chk('E7b 생산 VGCF 86 · SDCP 19 · PTFE 50 / off VGCF 87 / SDCP 없는 생산 VGCF 89',
        cbs['prod'].get('3') == 86 and cbs['prod'].get('5') == 19 and cbs['prod'].get('7') == 50
        and cbs['off'].get('3') == 87 and cbs['nosdcp'].get('3') == 89, str(cbs))
    L = rep['ledger']
    chk('E7c SDCP 가 덮은 셀 — {VGCF 3 · 기공 16} (생산 · off 같음)',
        L['sdcp_cover']['prod'] == {'0': 16, '3': 3} and L['sdcp_cover']['off'] == {'0': 16, '3': 3}, str(L['sdcp_cover']))
    st = L['sdcp_stretch']['off']
    chk('E7d SDCP 가 덮은 섬유 구간 — 1 구간 · 3 셀 · 섬유 1', st['n_runs'] == 1 and st['cells_total'] == 3
        and st['fibres_affected'] == 1, str(st))
    chk('E7d2 섬유 축방향 경로가 지나는 3|5 면 (설계 §3-1 ⚠ 회색 지대) — 구간 양 끝 2', st.get('axial_3_5_faces') == 2, str(st))
    chk('E7e SDCP 표현 부피 비 = 19 셀 · vox³ / V_true', close(L['volume_ratio']['prod']['SDCP'], 0.019 / V_SDCP1, 1e-9))
    chk('E7f SDCP 경유 섬유 연결 — 덩어리 1 · 두 섬유 잇는 것 0',
        L['sdcp_via']['off']['n_components'] == 1 and L['sdcp_via']['off']['n_bridging'] == 0, str(L['sdcp_via']))
    vv = rep['census_preview']['vv']
    z = np.load(os.path.join(out, 's0_instances_kit_B.npz'))
    chk('E7g VV instance 1 — 틈 −0.05 · L_touch 0.2236 · L_band 0.4031 · 90° · 긴 접촉 touch 0 / band 1',
        vv['n_instances'] == 1 and close(z['gap'][0], -0.05, 1e-9)
        and close(z['L_touch'][0], 2 * math.sqrt(0.0225 - 0.01), 1e-9)
        and close(z['L_band'][0], 2 * math.sqrt(THR ** 2 - 0.01), 1e-9) and close(z['theta_deg'][0], 90.0, 1e-6)
        and vv['n_long'] == {'touch': 0, 'band': 1}, str(vv.get('n_long')))
    po = rep['census_preview']['ports']['off']
    chk('E7h 포트 (off 격자) — 둘 다 직접 · 복셀 관계 face',
        po['status_counts'] == {'direct': 2} and po['relation_counts'] == {'face': 1}, str(po))
    chk('E7i PTFE 근접 = |m − PTFE 중심선| − r_P − r_f = %.6f' % (math.hypot(1.0, 0.05) - (R_P + R_F)),
        close(z['ptfe_excess_um'][0], math.hypot(1.0, 0.05) - (R_P + R_F), 1e-9))
    chk('E7j SDCP 근접 = |m − c_s| − r_s = %.6f' % (math.hypot(2.0, 0.05) - 0.15),
        close(z['sdcp_excess_um'][0], math.hypot(2.0, 0.05) - 0.15, 1e-9))
    sv = rep['census_preview']['sv']
    chk('E7k SV 후보 — 쌍 1 · 섬유에 닿는 SDCP 1 · 둘 이상 섬유 0',
        sv['n_pairs'] == 1 and sv['n_particles_touching'] == 1 and sv['n_particles_ge2_fibres'] == 0, str(sv))
    chk('E7l 섬유당 접합 간격 ℓ_j — 3.9 · 4.9 µm', sorted(np.round(z['lj_um'], 9).tolist()) == [3.9, 4.9],
        str(z['lj_um']))
    chk('E7m npz 키에도 σ 칸 없음', S0.schema_forbidden_keys({k: 0 for k in z.files}) == [])
    jc = rep.get('junction_census') or {}
    cen = jc.get('census') or {}
    zjp = os.path.join(out, 's0_junctions_kit_B.npz')
    zj = np.load(zjp) if os.path.exists(zjp) else None
    lc2 = 2 * math.sqrt(0.0225 - 0.01)
    chk('E7n 단계 2 접합 census (원장 · 같은 함수 · off 격자) — VV 1 · L_c = 2√(0.15² − 0.1²) = %.6f · 배율 1 · 긴 접촉 0 · '
        '자기 후보 0 · SDCP 근접 0' % lc2,
        jc.get('function') == 'carbon_junction.cjunc_registry' and jc.get('grid') == 'off'
        and cen.get('n_instances_distinct') == 1 and cen.get('n_instances_self') == 0 and jc.get('n_long') == 0
        and zj is not None and len(zj['Lc']) == 1 and close(zj['Lc'][0], lc2, 1e-9) and float(zj['mult'][0]) == 1.0
        and jc.get('n_sdcp_near') == 0 and S0.schema_forbidden_keys({k: 0 for k in zj.files}) == [],
        str({k: jc.get(k) for k in ('function', 'grid', 'n_long', 'n_sdcp_near')}))


def t_e2e_payload_crosscheck():
    """생산 raster = payload 자신의 rasterize-only 원장과 셀 수 같음 (가로채기가 입력을 바꾸지 않았다)."""
    tmp = STATE['tmp']; kitB = STATE['kitB']
    od = os.path.join(tmp, 'xo'); os.makedirs(od)
    run_d = S0.find_run_dir(kitB)
    argv = S0.resolve_payload_argv(kitB, run_d, od, vox=VOX, bridge_um=0.48, sdcp_sphere_d=0.30)
    i = argv.index('--step3-rasterize-only')
    led = argv[i + 1]
    r = subprocess.run([sys.executable, os.path.join(SCRIPTS, 'mpm_webapp_payload.py'), *argv],
                       cwd=run_d, capture_output=True, text=True, timeout=600)
    ok = r.returncode == 0 and os.path.exists(led)
    chk('E5a payload 원장 생성 (rc 0)', ok, (r.stdout + r.stderr)[-300:])
    if ok:
        cb = {str(k): v for k, v in _load(led)['cells_by_sid'].items()}
        chk('E5b payload rasterize-only cells_by_sid == S0 생산 격자', cb == STATE['repB']['raster']['cells_by_sid']['prod'],
            f"{cb} vs {STATE['repB']['raster']['cells_by_sid']['prod']}")


def _perm_mutate(arrs):
    rng = np.random.default_rng(3)
    U, PH, FI, KI, DI = (arrs[k] for k in ('se_dump.npy', 'phase.npy', 'fibre.npy', 'fibre_kind.npy', 'fibre_dia.npy'))
    blocks = []
    se_idx = np.nonzero(PH == 1)[0]
    blocks.append(rng.permutation(se_idx))
    for f in np.unique(FI[(PH == 2) | (PH == 4)]):
        blocks.append(np.nonzero(FI == f)[0])
    blocks.append(np.nonzero(PH == 5)[0])
    order = [blocks[0]] + [blocks[j] for j in rng.permutation(np.arange(1, len(blocks)))]
    idx = np.concatenate(order)
    relabel = {0: 7, 1: 9, 2: 3}
    FI2 = FI[idx].copy()
    for a_, b_ in relabel.items():
        FI2[FI[idx] == a_] = b_
    arrs.update({'se_dump.npy': U[idx], 'phase.npy': PH[idx], 'fibre.npy': FI2, 'fibre_kind.npy': KI[idx],
                 'fibre_dia.npy': DI[idx]})


def t_e2e_perm():
    tmp = STATE['tmp']
    planA = STATE['planA']; h = hashlib.sha256(planA).hexdigest()
    repo, sha, prel, rrel = make_plan_repo(os.path.join(tmp, 'g2'), planA, h)
    kitP = write_kit(tmp, 'kit_Bperm', vgcf=[F1, F2], ptfe=[P1], sdcp=S1,
                     vol={'VGCF': 0.09, 'PTFE': 0.1, 'SDCP': V_SDCP1}, mutate=_perm_mutate)
    out = os.path.join(tmp, 'outBP')
    _stage(2, [kitP], out, threshold_commit=sha, plan_path=prel, repo=repo, r_doc=rrel)
    a, b = STATE['repB'], _load(os.path.join(out, 's0_stage2_kit_Bperm.json'))
    za = np.load(os.path.join(tmp, 'outB2', 's0_instances_kit_B.npz'))
    zb = np.load(os.path.join(out, 's0_instances_kit_Bperm.npz'))
    same_cells = a['raster']['cells_by_sid'] == b['raster']['cells_by_sid']
    same_led = all(a['ledger'][k] == b['ledger'][k] for k in ('ptfe_cover', 'ptfe_cut', 'sdcp_cover', 'sdcp_stretch',
                                                               'sdcp_via', 'crossing_cells', 'volume_ratio'))
    same_inst = all(np.array_equal(np.sort(za[k]), np.sort(zb[k])) for k in ('gap', 'L_touch', 'L_band', 'theta_deg',
                                                                             'ptfe_excess_um', 'sdcp_excess_um', 'lj_um'))
    chk('S0-4a 순열 (SE 행 섞음 · 섬유 블록 순서 · fid 이름 · SDCP 행) — 격자 셀 수 같음', same_cells)
    chk('S0-4b 원장 같음', same_led, str([k for k in a['ledger'] if a['ledger'][k] != b['ledger'].get(k)]))
    chk('S0-4c census 분포 같음', same_inst and a['census_preview']['vv']['n_instances']
        == b['census_preview']['vv']['n_instances'])


def t_e2e_reject_inputs():
    tmp = STATE['tmp']
    vol = {'VGCF': 0.04, 'PTFE': 0.1}

    def case(name, label, **kw):
        kit = write_kit(tmp, name, vgcf=kw.pop('vgcf', [F1]), ptfe=[P1], vol=vol, **kw)
        out = os.path.join(tmp, 'out_' + name)
        bad = raises(lambda: _stage(1, [kit], out), S0.S0Error)
        pre = not os.path.exists(out) or not any(n.startswith('payload_capture') for n in os.listdir(out))
        chk(label, bad and pre, f'rejected={bad} before_capture={pre}')

    def m_len(a):
        a['fibre.npy'] = a['fibre.npy'][:-1]

    def m_phase(a):
        a['phase.npy'] = a['phase.npy'][:-1]

    def m_val(v):
        def f(a):
            a['se_dump.npy'] = a['se_dump.npy'].copy(); a['se_dump.npy'][330, 1] = v
        return f

    def m_split(a):
        PH, FI = a['phase.npy'], a['fibre.npy']
        f1 = np.nonzero((PH == 2) & (FI == 0))[0]
        rest = np.setdiff1d(np.arange(len(PH)), f1)
        idx = np.concatenate([f1[:7], rest[:5], f1[7:], rest[5:]])
        for k in list(a):
            a[k] = a[k][idx]

    def m_kind0(a):
        a['fibre_kind.npy'] = a['fibre_kind.npy'].copy(); a['fibre_kind.npy'][a['phase.npy'] == 2] = 0

    case('kit_len', 'S0-5a fibre 길이 ≠ 점 수 → 거부 (조용한 강등 없음)', mutate=m_len)
    case('kit_plen', 'S0-5b phase 길이 ≠ 점 수 → 거부', mutate=m_phase)
    case('kit_nan', 'S0-5c NaN 좌표 → 거부', mutate=m_val(float('nan')))
    case('kit_pinf', 'S0-5d +inf 좌표 → 거부', mutate=m_val(float('inf')))
    case('kit_ninf', 'S0-5e −inf 좌표 → 거부', mutate=m_val(float('-inf')))
    case('kit_split', 'S0-5f 같은 fid 가 떨어진 두 블록 → 거부', mutate=m_split)
    case('kit_nokind', 'S0-5g fibre_kind.npy 없음 → 거부 (연속 중심선 근거 없음)', kind=False)
    case('kit_kind0', 'S0-5h VGCF 행 kind ≠ 1 (경로 아님) → 거부', mutate=m_kind0)
    case('kit_dup', 'S0-5i 정확 중복 경로 → 거부', vgcf=[F1, F1.copy()])
    kitA = STATE['kitA']
    out = os.path.join(tmp, 'out_nonempty'); os.makedirs(out)
    open(os.path.join(out, 'old.json'), 'w').close()
    chk('S0-5j 출력 폴더가 비어 있지 않음 → 거부', raises(lambda: _stage(1, [kitA], out), S0.S0Error))


def t_e2e_box_plate():
    tmp = STATE['tmp']
    F3 = np.column_stack([8.05 + 0.3 * np.arange(7), np.full(7, 6.55), np.full(7, 3.55)])
    F4 = np.column_stack([np.full(10, 8.55), 5.05 + 0.3 * np.arange(10), np.full(10, 3.55)])
    #  AM2 (중심 (8, 1, 2.5) · R 1) 곁을 지나는 섬유 둘 — 중심선 거리 1.115 (틈 +0.04 = VA 아님 · tol_fs 0) · 1.05 (틈 −0.025 = VA)
    F5 = np.column_stack([np.full(5, 9.115), 0.5 + 0.25 * np.arange(5), np.full(5, 2.5)])
    F6 = np.column_stack([np.full(5, 6.95), 0.5 + 0.25 * np.arange(5), np.full(5, 2.5)])
    kitC = write_kit(tmp, 'kit_C', vgcf=[F1, F3, F4, F5, F6], ptfe=[P1], vol={'VGCF': 0.08, 'PTFE': 0.1})
    out = os.path.join(tmp, 'outC')
    _stage(1, [kitC], out)
    rep = _load(os.path.join(out, 's0_stage1_kit_C.json'))
    vv = rep['census_preview']['vv']
    chk('S0-6a 판 위 (z 3.55 > 두께 3.5) instance → above_top_plate 1',
        vv['location'].get('above_top_plate') == 1 and vv['n_instances'] == 1, str(vv.get('location')))
    chk('S0-6b 상자 밖 VGCF 점 수 기록 (x > 9.2 µm → 3)', rep['inputs']['counts']['vgcf_points_outside_box'] == 3,
        str(rep['inputs']['counts']))
    va = rep['census_preview']['va']
    chk('E11c VA (J2b · tol_fs 0) — 틈 +0.04 섬유 아님 · −0.025 섬유 1 instance (보고값 = 생산 상수 경로)',
        va['tol_fs_um'] == 0.0 and va['n_instances'] == 1 and close(va['gap_um']['min'], 1.05 - 1.075, 1e-9), str(va))


#  ── 픽스처 J (단계 1 · vox 0.15 = r_f/h 0.5 — test_carbon_junction 의 KU 를 0.15 µm 로 줄인 꼴) ──
#  J1 · J2 = 나란한 두 VGCF (중심 간격 0.12 µm < 2 r_f · 겹침 x [4.02, 5.02]) → 닿음 길이 (J1 쪽) = 1 + 2√(0.15² − 0.12²) = 1.18 µm ·
#  배율 1.18 / 0.30.  KU = U 자로 접힌 한 섬유 (다리 1 · 기운 다리 2 · 중심선 최근접 0.8 h = 0.12 µm 유일) → 자기 후보 하나 ·
#  s = h (3 + 1 + √(0.2² + 3²)) · 자기 L_c = 3 h = 0.45 µm (배율 1.5).  꼭짓점 + 0.01 µm (셀 경계에 점이 놓이지 않게 · 셀 구조 = KU 그대로).
J_H = 0.15
J_KU = [(1.5, 1.5, 0.5), (1.5, 1.5, 4.5), (2.5, 1.5, 4.5), (2.3, 1.5, 1.5), (4.5, 1.5, 1.5), (4.5, 1.5, 7.5)]
J_KU_S = J_H * (3.0 + 1.0 + math.sqrt(0.2 ** 2 + 3.0 ** 2))
J_LC_PAR = 1.0 + 2.0 * math.sqrt(0.15 ** 2 - 0.12 ** 2)


def _densify(verts, step):
    V = np.asarray(verts, float)
    out = [V[0]]
    for a, b in zip(V[:-1], V[1:]):
        n = max(1, int(math.ceil(np.linalg.norm(b - a) / step - 1e-12)))
        for i in range(1, n + 1):
            out.append(a + (b - a) * (i / n))
    return np.asarray(out)


def _kit_j_fibres():
    J1 = np.column_stack([3.02 + 0.1 * np.arange(31), np.full(31, 6.04), np.full(31, 2.0)])
    J2 = np.column_stack([4.02 + 0.1 * np.arange(11), np.full(11, 6.16), np.full(11, 2.0)])
    KU = np.array([3.01, 3.01, 2.11]) + J_H * _densify(J_KU, 0.25)
    return [J1, J2, KU]


#: 나란한 접촉선 (y 6.10 · z 2.0) 위 0.2 µm 를 지나는 PTFE — 덮임 문턱 r_P + r_f + tol_P = 0.124 + 0.075 + 0.01875 ≥ 0.2 → 그 instance 만 덮임
J_PTFE = np.column_stack([3.62 + 0.1 * np.arange(21), np.full(21, 6.10), np.full(21, 2.20)])


def _spy_registry():
    """carbon_junction.cjunc_registry 엿보기 — 부른 인자 · 돌려준 원장을 모은다 (값은 그대로 돌려준다)."""
    import carbon_junction as CJ
    calls = []
    orig = CJ.cjunc_registry

    def spy(*a, **k):
        r = orig(*a, **k)
        calls.append((a, k, r))
        return r
    CJ.cjunc_registry = spy
    return CJ, orig, calls


def t_e2e_registry():
    tmp = STATE['tmp']
    kitJ = write_kit(tmp, 'kit_J', vgcf=_kit_j_fibres(), ptfe=[J_PTFE], vol={'VGCF': 0.05, 'PTFE': 0.1})
    out = os.path.join(tmp, 'outJ')
    CJ, orig, calls = _spy_registry()
    try:
        S0.run_stage(1, [kitJ], out, vox=J_H, bridge_um=0.48, sdcp_sphere_d=0.30)
    finally:
        CJ.cjunc_registry = orig
    rep = _load(os.path.join(out, 's0_stage1_kit_J.json'))
    jc = rep.get('junction_census') or {}
    thr = jc.get('thresholds') or {}
    chk('R1 접합 census (판정 · 보고 판) = carbon_junction.cjunc_registry — 표지 · off 격자 · s_min 미등록 (거르지 않음) · '
        '길이 법칙 len_scaled_v0 · B0 미리보기는 표지 그대로',
        jc.get('function') == 'carbon_junction.cjunc_registry' and jc.get('status') == 'registry' and jc.get('grid') == 'off'
        and 's_min_um' in thr and thr.get('s_min_um') is None and jc.get('len_law') == 'len_scaled_v0'
        and rep.get('census_preview', {}).get('status') == 'b0_preview', str({k: jc.get(k) for k in ('function', 'status', 'grid')}))
    reg = calls[0][2] if len(calls) == 1 else None
    a_, k_ = (calls[0][0], calls[0][1]) if reg is not None else ((), {})
    sid = a_[0] if a_ else None
    pv = rep.get('thresholds_used') or {}
    same_in = (reg is not None and sid is not None and not (np.asarray(sid) == 7).any()
               and S0._hist(np.asarray(sid)) == rep['raster']['cells_by_sid']['off'] and k_.get('s_min_um', 0) is None
               and all(k_.get(a) == pv.get(b) for a, b in (('tol_ff_um', 'tol_ff_um'), ('L_par_um', 'L_par_um'),
                                                          ('r_port_um', 'r_port_um'), ('tol_P_um', 'tol_P_um'),
                                                          ('tol_sj_um', 'tol_sj_um'), ('r_f_um', 'r_f_um'))))
    z = None
    zp = os.path.join(out, 's0_junctions_kit_J.npz')
    if os.path.exists(zp):
        z = np.load(zp)
    same_out = (reg is not None and z is not None and jc.get('census') == json.loads(json.dumps(reg['census']))
                and np.array_equal(z['Lc'], reg['instances']['Lc']) and np.array_equal(z['mult'], reg['instances']['mult'])
                and np.array_equal(z['s'], reg['instances']['s'], equal_nan=True)
                and np.array_equal(z['is_self'], reg['instances']['self'])
                and jc.get('n_long') == int(np.sum(reg['instances']['long']))
                and jc.get('len_mult_sum') == float(np.sum(reg['instances']['mult'])))
    chk('R2 같은 함수 — S0 가 cjunc_registry 를 한 번 (off 격자 · 계획 문턱 · s_min None) 불렀고 보고 · npz = 그 원장 값 '
        '(census · L_c · 배율 · s · 자기 표지 · 긴 접촉 수 · 배율 합)', same_in and same_out,
        f'호출 {len(calls)} · 입력 {same_in} · 출력 {same_out}')
    inst = reg['instances'] if reg is not None else None
    dl = []
    if inst is not None:
        dl = [q for q in range(len(inst['fi'])) if not inst['self'][q]]
    chk('R3 손계산 — 나란한 두 섬유 (중심 간격 0.12 · 겹침 1.0 µm) → VV instance 1 · L_c = 1 + 2√(0.15² − 0.12²) = %.6f · '
        '배율 L_c / 0.30 · 긴 접촉' % J_LC_PAR,
        inst is not None and len(dl) == 1 and close(inst['Lc'][dl[0]], J_LC_PAR, 1e-9)
        and close(inst['mult'][dl[0]], J_LC_PAR / 0.30, 1e-9) and bool(inst['long'][dl[0]]),
        str([(float(inst['Lc'][q]), float(inst['mult'][q])) for q in dl]) if inst is not None else 'no registry')
    sc = jc.get('self_candidates') or []
    cen = jc.get('census') or {}
    chk('R4 손계산 — U 자 섬유 (KU × 0.15) → 자기 후보 1 · s = 0.15 (4 + √9.04) = %.6f · 자기 L_c 0.45 · 배율 1.5 · '
        '거르지 않음 (s_min 미등록 · 거른 수 0)' % J_KU_S,
        len(sc) == 1 and close(sc[0].get('s_um'), J_KU_S, 1e-9) and close(sc[0].get('Lc_um'), 0.45, 1e-9)
        and close(sc[0].get('mult'), 1.5, 1e-9) and cen.get('n_self_candidates') == 1 and cen.get('n_self_filtered') == 0
        and cen.get('self_filter') == 'off_s_min_missing', str(sc))
    lc = jc.get('long_contacts') or []
    want_sum = J_LC_PAR / 0.30 + 1.5
    chk('R5 후보별 목록 — 긴 접촉 2 (distinct 1 · self 1) · 배율 합 = %.6f · 배율 > 1 수 2 · npz 키 (후보마다 L_c · 배율 · s)' % want_sum,
        jc.get('n_long') == 2 and jc.get('n_long_distinct') == 1 and jc.get('n_long_self') == 1 and len(lc) == 2
        and sorted(x.get('kind') for x in lc) == ['distinct', 'self'] and close(jc.get('len_mult_sum'), want_sum, 1e-9)
        and jc.get('n_mult_gt1') == 2 and z is not None and {'Lc', 'mult', 's', 'is_self', 'fi', 'fj'} <= set(z.files),
        str({k: jc.get(k) for k in ('n_long', 'n_long_distinct', 'n_long_self', 'len_mult_sum', 'n_mult_gt1')}))
    chk('R6 S0-2 — 보고 · 접합 npz 에 σ · 전류 · 소산 칸 없음 (원장 = 기하만)',
        S0.schema_forbidden_keys(rep) == [] and z is not None and S0.schema_forbidden_keys({k: 0 for k in z.files}) == [],
        str(S0.schema_forbidden_keys(rep)[:5]))
    n_pts = sum(int(v) for v in rep['inputs']['counts']['points_by_phase'].values()) - int(
        rep['inputs']['counts']['points_by_phase'].get('1', 0))
    ph_in = np.asarray(a_[4]) if len(a_) > 4 else np.zeros(0)
    cov = z['ptfe_cov'] if z is not None and 'ptfe_cov' in z.files else None
    chk('R7 원장 입력 = 잡은 첨가제 입력 전부 (PTFE 행 포함 · P-junc 덮임) — 접촉선 위 0.2 µm PTFE → 그 instance 만 덮임 '
        '(n_ptfe_cov 1 · 자기 후보는 아님)',
        reg is not None and len(a_) > 6 and len(ph_in) == n_pts and bool((ph_in == 4).any()) and jc.get('n_ptfe_cov') == 1
        and cov is not None and inst is not None and len(dl) == 1 and bool(cov[dl[0]]) and int(cov.sum()) == 1,
        f"입력 점 {len(ph_in)} ↔ {n_pts} · n_ptfe_cov {jc.get('n_ptfe_cov')}")


#  ── 픽스처 RV (단계 1 · ★ 10-21 Codex RCA-03 · 05 · Q11 일부 — census 보탬 · 시험 먼저) ──
#  RV_LOOP = 판정문 RCA-03 폴리라인 (h 0.15 · 셀 경계에서 0.01 떨어진 꼭짓점) 을 (3.0, 3.0, 2.1) 로 옮긴 것 (셀 구조 그대로) → 같은 fid 가
#  셀 넷을 두 번씩 지난다 (재방문 쌍 4 · 셀 4 · 섬유 1) · 자기 후보 하나 · 그 접점 = y 셀 경계 위 → 두 포트 다 ε 띠 동률 (2).
#  RV_P1 · RV_P2 = 나란한 두 VGCF (중심 간격 0.12 · 겹침 x [4.02, 5.82]) → 닿음 L_c = 1.8 + 2√(0.15² − 0.12²) = 1.98 → k = 7 분산 간선
#  (긴 접촉 간선 7) · RV_PT = 그 접촉 시작 근처 (x 4.07) 를 가로지르는 PTFE (z +0.2) → 첫 등분 간선만 덮임 (1/7 · 부분 덮임 instance 1).
RV_LOOP = [(.01, .01, .01), (.44, .01, .01), (.44, .44, .01), (.44, .44, .14), (.44, .14, .14), (.01, .14, .14)]
RV_LC = 1.8 + 2.0 * math.sqrt(0.15 ** 2 - 0.12 ** 2)


def _kit_rv():
    loop = np.array([3.0, 3.0, 2.1]) + _densify(RV_LOOP, 0.05)
    P1 = np.column_stack([3.02 + 0.1 * np.arange(31), np.full(31, 6.04), np.full(31, 2.0)])
    P2 = np.column_stack([4.02 + 0.1 * np.arange(19), np.full(19, 6.16), np.full(19, 2.0)])
    PT = np.column_stack([np.full(11, 4.07), 5.6 + 0.1 * np.arange(11), np.full(11, 2.2)])
    return [loop, P1, P2], [PT]


def t_e2e_registry_q11():
    tmp = STATE['tmp']
    vg, pt = _kit_rv()
    kitR = write_kit(tmp, 'kit_RV', vgcf=vg, ptfe=pt, vol={'VGCF': 0.05, 'PTFE': 0.1})
    out = os.path.join(tmp, 'outRV')
    S0.run_stage(1, [kitR], out, vox=J_H, bridge_um=0.48, sdcp_sphere_d=0.30)
    rep = _load(os.path.join(out, 's0_stage1_kit_RV.json'))
    jc = rep.get('junction_census') or {}
    cen = jc.get('census') or {}
    rv = jc.get('revisit') or {}
    chk('R8 같은 셀 비연속 재방문 (판정문 RCA-03 고리) — 쌍 4 · 셀 4 · 섬유 1 · s 분포 (재방문 든 자기 후보 1 · 유한) · 원장 census 와 '
        '보고 블록 같은 값',
        cen.get('n_revisit_pairs') == 4 and cen.get('n_revisit_cells') == 4 and cen.get('n_revisit_fibres') == 1
        and rv.get('n_pairs') == 4 and rv.get('n_cells') == 4 and rv.get('n_fibres') == 1
        and (rv.get('s_um') or {}).get('n') == 1 and math.isfinite(float((rv.get('s_um') or {}).get('min', math.nan))),
        str({'census': {k: cen.get(k) for k in ('n_revisit_pairs', 'n_revisit_cells', 'n_revisit_fibres')}, 'revisit': rv}))
    chk('R8 포트 동률 수 — 고리 자기 접합 두 포트 (셀 경계 위 접점 · ε 띠) = 2 (나란한 쌍 등분 간선은 동률 없음)',
        jc.get('n_port_ties') == 2 and cen.get('n_port_ties') == 2, str((jc.get('n_port_ties'), cen.get('n_port_ties'))))
    sub = jc.get('subedges') or {}
    chk('R8 긴 접촉 · 분산 간선 — 긴 instance 1 (L_c %.4f · k 7) · 간선 8 (자기 1 + 7) · 긴 접촉 간선 7' % RV_LC,
        jc.get('n_long') == 1 and sub.get('n') == 8 and sub.get('n_long') == 7 and cen.get('n_subedges') == 8, str(sub))
    chk('R8 간선별 PTFE 덮임 — 덮인 간선 1 (첫 등분점) · 부분 덮임 instance 1 · instance 대표점 덮임 1 (옛 칸 그대로)',
        sub.get('n_ptfe_cov') == 1 and sub.get('n_instances_ptfe_partial') == 1 and jc.get('n_ptfe_cov') == 1, str(sub))
    zp = os.path.join(out, 's0_junctions_kit_RV.npz')
    z = np.load(zp) if os.path.exists(zp) else None
    chk('R8 npz — 간선별 배열 (instance 번호 · PTFE 덮임 · SDCP 근접 · 실현) · S0-2 σ · 전류 · 소산 칸 없음',
        z is not None and {'sub_inst', 'sub_ptfe_cov', 'sub_a_sdcp', 'sub_realized'} <= set(z.files)
        and int(np.sum(z['sub_ptfe_cov'])) == 1 and len(z['sub_inst']) == 8
        and S0.schema_forbidden_keys(rep) == [] and S0.schema_forbidden_keys({k: 0 for k in z.files}) == [],
        str(None if z is None else sorted(z.files)))


#  ── 픽스처 AL (단계 1 · α 분포 판별) — 촘촘한 SE 판 (0.1 µm 간격 두 층 = SE|SE 면) 을 가로지르는 PTFE (이온 α < 1) ·
#     F1 (y 4.55) 아래에 붙은 AM 구 (꼭대기 y 4.5) 와 그 AM|VGCF 면 (y = 4.5) 을 지나는 PTFE (전자 AM|VGCF α < 1) ──
AL_SE = np.array([[4.05 + 0.1 * i, 8.05 + 0.1 * j, z] for i in range(10) for j in range(10) for z in (3.05, 3.15)])
AL_PA = np.column_stack([3.8 + 0.1 * np.arange(15), np.full(15, 8.5), np.full(15, 3.1)])
AL_PB = np.column_stack([np.full(13, 4.0), 3.6 + 0.1 * np.arange(13), np.full(13, 2.05)])
AL_AM = [(1, 4.0, 4.0, 2.05, 0.5), (2, 8.0, 1.0, 2.5, 1.0)]


def _arg(call, idx, name):
    """엿본 호출 (위치 인자, 키워드, 결과) 에서 인자 하나 — 위치 또는 키워드."""
    a, k = call[0], call[1]
    return a[idx] if len(a) > idx else k.get(name)


def _spy_alpha():
    """ptfe_face_alpha.build_capsules · build_plan 엿보기 — 부른 인자 · 결과를 모은다 (값은 그대로)."""
    import ptfe_face_alpha as FA
    rec = {'caps': [], 'plan': []}
    o_c, o_p = FA.build_capsules, FA.build_plan

    def caps_spy(*a, **k):
        r = o_c(*a, **k)
        rec['caps'].append((a, k, r))
        return r

    def plan_spy(*a, **k):
        r = o_p(*a, **k)
        rec['plan'].append((a, k, r))
        return r
    FA.build_capsules, FA.build_plan = caps_spy, plan_spy
    return FA, (o_c, o_p), rec


def t_e2e_alpha():
    tmp = STATE['tmp']
    kit = write_kit(tmp, 'kit_AL', vgcf=[F1], ptfe=[AL_PA, AL_PB], se=np.vstack([SE, AL_SE]), am=AL_AM,
                    vol={'VGCF': 0.04, 'PTFE': 0.1})
    out = os.path.join(tmp, 'outAL')
    FA, orig, rec = _spy_alpha()
    o_cap, got_kw = S0.capture_raster_inputs, {}

    def cap_spy(*a, **k):
        r = o_cap(*a, **k)
        got_kw['kw'] = r
        return r
    S0.capture_raster_inputs = cap_spy
    try:
        _stage(1, [kit], out)
    finally:
        FA.build_capsules, FA.build_plan = orig
        S0.capture_raster_inputs = o_cap
    #  독립 기대 off 격자 · pid = 잡은 생산 입력에서 PTFE (phase 4) 행을 뺀 생산 rasterize (ptfe_stamp off 의 _cond_ph)
    want_sid = want_pid = None
    if 'kw' in got_kw:
        k2 = dict(got_kw['kw'])
        keep = ~np.isin(np.asarray(k2['add_phase']), (4,))
        for nm in ('add_pts', 'add_phase', 'add_fid', 'add_kind'):
            k2[nm] = np.asarray(k2[nm])[keep]
        want_sid, want_pid = S3.rasterize(**k2)
    rep = _load(os.path.join(out, 's0_stage1_kit_AL.json'))
    al = (rep.get('ledger') or {}).get('alpha') or {}
    faces = al.get('faces') or {}
    fe, fi = faces.get('electronic') or {}, faces.get('ionic') or {}
    am_vgcf = sum(v.get('n_alpha_lt1', 0) for k, v in (fe.get('by_class') or {}).items() if k in ('AM_S|VGCF', 'AM_P|VGCF'))
    chk('A1 α 분포 판별 픽스처 — 이온 SE|SE 면 α < 1 행 > 0 · 전자 AM|VGCF 면 α < 1 행 > 0 (면 부류별 수 · Σ(1 − α)h² 기록)',
        al.get('status') == 'computed' and (fi.get('by_class') or {}).get('SE|SE', {}).get('n_alpha_lt1', 0) > 0
        and am_vgcf > 0
        and all('blocked_area_um2' in v for v in list((fe.get('by_class') or {}).values()) + list((fi.get('by_class') or {}).values())),
        f"전자 {fe.get('by_class')} · 이온 {fi.get('by_class')}")
    plans = {r[1].get('channel'): r for r in rec['plan']}
    ok_calls = (len(rec['caps']) == 1 and set(plans) == {'electronic', 'ionic'} and len(rec['plan']) == 2)
    same = False
    if ok_calls:
        sid_e = np.asarray(_arg(plans['electronic'], 0, 'sid'))
        caps_r = rec['caps'][0][2]
        same = (not (sid_e == 7).any() and S0._hist(sid_e) == rep['raster']['cells_by_sid']['off']
                and want_sid is not None and np.array_equal(sid_e, want_sid)
                and np.array_equal(np.asarray(_arg(plans['ionic'], 0, 'sid')), sid_e)
                and plans['electronic'][1].get('pid') is not None and plans['ionic'][1].get('pid') is None
                and np.array_equal(np.asarray(plans['electronic'][1].get('pid')), want_pid)
                and all(plans[c][1].get('K', FA.K_SEALED) == FA.K_SEALED for c in plans)
                and rec['caps'][0][1].get('dia_law', 'rope') == 'rope'
                and _arg(plans['electronic'], 2, 'caps') is caps_r and _arg(plans['ionic'], 2, 'caps') is caps_r
                and len(np.asarray(_arg(rec['caps'][0], 0, 'pts'))) == len(AL_PA) + len(AL_PB)
                and json.loads(json.dumps(FA.plan_face_summary(plans['electronic'][2]))) == fe
                and json.loads(json.dumps(FA.plan_face_summary(plans['ionic'][2]))) == fi
                and json.loads(json.dumps(FA.capsule_summary(caps_r))) == al.get('capsules'))
    chk('A2 같은 함수 — S0 가 build_capsules (PTFE 행 전부 · rope) 한 번 · build_plan 두 번 (off 격자 = PTFE 행 뺀 생산 rasterize · '
        '전자 = 그 pid · 이온 = pid 없음 · K 8 · 같은 캡슐) 을 불렀고 보고 = 그 계획 · 캡슐 요약 그대로', ok_calls and same,
        f"캡슐 {len(rec['caps'])} · 계획 {sorted(plans)}")
    vol = al.get('volume') or {}
    ptc = al.get('off_grid_ptfe_point_cells')
    m4 = np.asarray(_arg(rec['caps'][0], 0, 'pts')) if rec['caps'] else None
    want_pc = (FA.ptfe_point_cell_census(np.asarray(_arg(plans['electronic'], 0, 'sid')), m4, (0.0, 0.0, 0.0), VOX)
               if (ok_calls and m4 is not None) else None)
    chk('A3 캡슐 부피 기록 (S1 volume_record · 참부피 = mpm_metrics PTFE) · off 격자 PTFE 점 셀 sid 분포 (S1 ptfe_point_cell_census) · '
        '이 표 = 원장 capsule 과 같은 부피 (1e-12 상대)',
        vol.get('true_um3') == 0.1 and vol.get('status') in ('in_band', 'out_of_band') and want_pc is not None and ptc == want_pc
        and close(vol.get('capsule_um3'), (rep['ledger'].get('capsule') or {}).get('volume_ratio', math.nan) * 0.1,
                  1e-12 * max(1.0, abs(float(vol.get('capsule_um3') or 0.0)))),
        f'{vol} · 점 셀 {ptc} ↔ {want_pc}')
    chk('A4 S0-2 — α 블록에 σ · 전류 · 소산 칸 없음 (면 기하 · 수만)', S0.schema_forbidden_keys(al) == []
        and S0.schema_forbidden_keys(rep) == [], str(S0.schema_forbidden_keys(al)))


FAKE_PAYLOAD = '''import sys
import step3_sigma as _s3


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else 'none'
    if mode == 'raise':
        raise ValueError('fake payload failure')
    if mode == 'raster':
        _s3.rasterize([[0.5, 0.5, 0.5]], [0.3], [2], None, None, (0.0, 0.0, 0.0), (1.0, 1.0, 1.0), 0.1, bridge_um=0.48)
        print('NOT CAPTURED')
'''


def t_e2e_no_capture():
    tmp = STATE['tmp']
    kit = write_kit(tmp, 'kit_nostep3', vgcf=[F1], ptfe=[P1], vol={'VGCF': 0.04, 'PTFE': 0.1}, extra=' --no-step3')
    out = os.path.join(tmp, 'out_nostep3')
    chk('E10a --no-step3 킷 (payload 가 rasterize 전 · 뒤 경로에서 예외) → S0Error 로 거부 (fail-closed)',
        raises(lambda: _stage(1, [kit], out), S0.S0Error))
    fd = os.path.join(tmp, 'fakepay'); os.makedirs(fd)
    with open(os.path.join(fd, 'mpm_webapp_payload.py'), 'w') as f:
        f.write(FAKE_PAYLOAD)
    rd = os.path.join(tmp, 'fakerun'); os.makedirs(rd)
    orig = S3.rasterize
    chk('E10b payload main 이 rasterize 없이 정상 종료 → 거부 (가로채기 안 걸림)',
        raises(lambda: S0.capture_raster_inputs(['none'], rd, scripts_dir=fd), S0.S0Error) and S3.rasterize is orig)
    chk('E10c payload 예외 (ValueError) → S0Error · rasterize 원상',
        raises(lambda: S0.capture_raster_inputs(['raise'], rd, scripts_dir=fd), S0.S0Error) and S3.rasterize is orig)
    kw = S0.capture_raster_inputs(['raster'], rd, scripts_dir=fd)
    chk('E10d rasterize 호출 → 인자 (기본값 채움) 를 잡고 멈춤 · 원상 복구',
        S3.rasterize is orig and float(kw['vox']) == 0.1 and kw['bridge_um'] == 0.48 and kw['fid_gap_tol'] == 2.0
        and kw['se_pts'] is None, str(sorted(kw)))


def main():
    global S0
    if '--s0' in sys.argv:                               # 다른 판의 S0 모듈로 (변이 · 고치기 전 판 실패 기록용)
        import importlib.util
        p = sys.argv[sys.argv.index('--s0') + 1]
        spec = importlib.util.spec_from_file_location('ca_s0_census', p)
        S0 = importlib.util.module_from_spec(spec)
        sys.modules['ca_s0_census'] = S0
        spec.loader.exec_module(S0)
        print(f'  (S0 = {p})')
    print('── G 기하 원시'); run('G', t_geometry)
    print('── C 접합 census 미리보기'); run('C', t_census)
    print('── P 격자 원시'); run('P', t_grid)
    print('── L 계획'); run('L', t_plan); run('L3', t_plan_commit)
    print('── S 스키마'); run('S', t_schema)
    tmp = tempfile.mkdtemp(prefix='s0test_')
    STATE['tmp'] = tmp
    try:
        print('── E 끝-끝 (payload 실물)')
        run('E1', t_e2e_stage1)
        if 'kitA' in STATE:
            run('E6', t_e2e_reject_stage)
            if 'planA' in STATE and 'kitB' in STATE:
                run('E7', t_e2e_stage2)
                if 'repB' in STATE:
                    run('E5', t_e2e_payload_crosscheck)
                    run('E9', t_e2e_perm)
            run('E8', t_e2e_reject_inputs)
            run('E11', t_e2e_box_plate)
            run('E10', t_e2e_no_capture)
            print('── R 접합 census = cjunc_registry (같은 함수)'); run('R', t_e2e_registry)
            print('── R8 census 보탬 (재방문 · 동률 · 긴 접촉 간선 · 간선별 덮임 · 10-21)'); run('R8', t_e2e_registry_q11)
            print('── A α 분포 = ptfe_face_alpha 함수 (같은 함수)'); run('A', t_e2e_alpha)
        else:
            chk('E 묶음 — 픽스처 A 단계 1 이 서지 않아 나머지 끝-끝 시험을 못 돈다', False)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print(f'\n{_ok} PASS · {len(_fail)} FAIL')
    if _fail:
        print('FAIL: ' + ' | '.join(_fail))
        sys.exit(1)


if __name__ == '__main__':
    main()
