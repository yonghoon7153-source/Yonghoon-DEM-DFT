#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rint ② S1 — PTFE 면 개구율 연산자 `face_alpha` 시험 (시험 먼저 · 규율 ② · 2026-10-20).

정본 설계 = docs/reviews/rint_carbon_additive_design_v1_20261020.md §3 (S1) · §7 (세대 · 영수증) · Codex R18 판정문 Q6
(docs/reviews/codex_r18_verdict_20260831.md) · 1저자 10-20 설계 §10 N1–N18 = 권고대로.

  python3 scripts/test_ptfe_face_alpha.py                     # 전부 (payload 끝-끝 포함 · 수 분)
  python3 scripts/test_ptfe_face_alpha.py --skip-payload      # payload 끝-끝 빼고
  python3 scripts/test_ptfe_face_alpha.py --only F16,C        # 이름 접두로 고르기
  python3 scripts/test_ptfe_face_alpha.py --s3 OLD.py         # 다른 step3_sigma (고치기 전 blob) — 실패 기록용
  python3 scripts/test_ptfe_face_alpha.py --old-scripts DIR   # 끔 비트 동일 대조 (DIR = 고치기 전 scripts/ 사본) — B 묶음

묶음 (설계 §3-4 표 · §3-3 계약 · §7):
  F1–F17  R18 종료조건 8 (α=1/0 극한 · 상호성 · KCL · 회전/반사 · 주기 seam · 고정 기하 격자 조임 · origin 불변 · 투여 단조)
          + PTFE 없음 no-op · 부피 · 같은 물체 면제 · 채널 독립 · 변이 · 입구 거부 · 해석 개구율 (판별력) · 판 근처 캡슐
  C       계약 — 계획 무결성 (지문 · 격자 · 불변량 · 행 자격) · 동시 사용 거부 · 진단 거부 (E2) · 영수증 · 기록
  R       run_contract — p3ca id · unknown:ca_ext · ptfe_record_ok · ca_ext_record_ok · 봉인 p2 코호트 32 팔 · CLI 회계
  P       payload 끝-끝 — `--ptfe-stamp face_alpha` (세 분기 · 거부 조합 · 매니페스트 · sid = off 격자 · 채널 독립)
  B       (--old-scripts) 끔 비트 동일 — 솔버 (σ · φ · n_dof) · payload 매니페스트 (code_sha · exec_env 빼고)
⚠ PASS 는 계약 · 구현의 증거이지 S1 의 물리 검증이 아니다 (지름 Ø0.248 = 1저자 규약 선택 · `DIA_UNCHECKED` · 불투과 가정).
  F7 · F8 = **보고** (합격선 = 실행 전 봉인 · 개발 판과 분리 · v3 D12-V 규칙) — 실행 · 유한만 본다.
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

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, 'scripts')
sys.path.insert(0, SCRIPTS)

S3 = None                       # main() 이 채운다
FA = None
RC = None
ARGS = None
_ok, _fail = 0, []
_MUTE = []                      # 변이 모드 — chk 결과를 여기 모으고 전역 집계에 넣지 않는다 (F14)


def chk(name, cond, why=''):
    global _ok
    cond = bool(cond)
    if _MUTE:
        _MUTE[-1].append(cond)
        return cond
    if cond:
        _ok += 1
        print(f'  PASS  {name}')
    else:
        _fail.append(name)
        print(f'  FAIL  {name}' + (f'  ({why})' if why else ''))
    return cond


CASES = []


def case(tag):
    def deco(fn):
        CASES.append((tag, fn))
        return fn
    return deco


def quiet(fn, *a, **k):
    with contextlib.redirect_stdout(io.StringIO()):
        return fn(*a, **k)


def raises(fn, exc=(ValueError, TypeError)):
    try:
        quiet(fn)
    except exc:
        return True
    return False


_CG_CALLS = [0]


@contextlib.contextmanager
def direct_solver(capture=None):
    """작은 픽스처 = 직접 풀이 (기계 정밀도) — 조립 · 항등식을 CG 허용오차 없이 본다.  생산 경로 아님.
    capture (list) 를 주면 조립된 L 을 담는다 (F3 대칭)."""
    from scipy.sparse.linalg import spsolve
    old = S3._solve_cg

    def _direct(L, b):
        _CG_CALLS[0] += 1
        if capture is not None:
            capture.append(L.copy())
        return spsolve(L.tocsc(), b), 0
    S3._solve_cg = _direct
    try:
        yield
    finally:
        S3._solve_cg = old


# ═════════════════════════ 공용 픽스처 ═════════════════════════
H = 0.25                         # dyadic 격자 간격 (µm) — 대칭 시험에서 반올림 동률을 피한다
SIG_SE, SIG_SDCP_I = 0.003, 0.001


def ti():
    return S3.ionic_sigma_table(SIG_SDCP_I, SIG_SE)


def te():
    return S3.electronic_sigma_table(0.010, 0.005, 100.0, 10.0, 250.0)


def line(a, b, n):
    a = np.asarray(a, np.float64)
    b = np.asarray(b, np.float64)
    return a + (b - a) * np.linspace(0.0, 1.0, int(n))[:, None]


def mkpaths(*paths):
    """경로 목록 (각 (n,3) µm 점열) → (pts, fid, kind) — fid 는 경로마다 연속 블록."""
    if not paths:
        return np.zeros((0, 3)), np.zeros(0, np.int64), np.zeros(0, np.int8)
    P = [np.asarray(p, np.float64).reshape(-1, 3) for p in paths]
    pts = np.vstack(P)
    fid = np.concatenate([np.full(len(p), i, np.int64) for i, p in enumerate(P)])
    return pts, fid, np.ones(len(pts), np.int8)


def caps_of(*paths, dia_law='rope'):
    p, f, k = mkpaths(*paths)
    return FA.build_capsules(p, f, k, dia_law=dia_law)


def plan_of(sid, table, caps, h, channel, pid=None, K=None, lo=(0.0, 0.0, 0.0)):
    kw = {} if K is None else {'K': K}
    return FA.build_plan(sid, table, caps, lo=lo, vox=h, channel=channel, pid=pid, **kw)


def solve(sid, table, h, plan=None, pid=None, capture=None, **kw):
    args = dict(return_field=True, z_top_um=sid.shape[2] * h, z_bot_um=0.0)
    args.update(kw)
    if plan is not None:
        args['face_alpha'] = plan
    if pid is not None:
        args['pid'] = pid
    with direct_solver(capture):
        return quiet(S3.solve_sigma_z, sid, table, h, **args)


def same_solve(r1, r2):
    """두 해가 비트 같은가 — σ · n_dof · φ 바이트."""
    if r1.get('sigma_eff') != r2.get('sigma_eff') or r1.get('n_dof') != r2.get('n_dof'):
        return False
    p1, p2 = r1.get('phi'), r2.get('phi')
    if (p1 is None) != (p2 is None):
        return False
    return p1 is None or (p1.dtype == p2.dtype and p1.shape == p2.shape and p1.tobytes() == p2.tobytes())


def rand_ion_grid(shape, seed):
    """SE (6) · SDCP (5) 섞인 이온 격자 (모든 셀 점유 · 비대칭)."""
    rng = np.random.default_rng(seed)
    return np.where(rng.random(shape) < 0.25, 5, 6).astype(np.int8)


def ref_sigma(sig_cells, h, alpha=None):
    """**독립 참조 해** (생산 조립과 다른 코드 · 조밀 풀이) — 직육면체 격자 · 비주기 · 판 = k=0 층 (φ=1) · k=nz-1 층 (φ=0) ·
    판 g = σ·h²/(h/2) · 면 g = 조화평균 σ·h × α(축, 아래 셀 선형번호) · α=0 = 간선 없음 · 어느 판에도 안 닿는 성분 제거."""
    s = np.asarray(sig_cells, np.float64)
    nx, ny, nz = s.shape
    alpha = alpha or {}
    cells = [tuple(int(v) for v in c) for c in np.argwhere(s > 0)]
    index = {c: n for n, c in enumerate(cells)}
    edges = []
    for c in cells:
        for ax in range(3):
            nb = list(c)
            nb[ax] += 1
            nb = tuple(nb)
            if nb in index:
                lin = int(np.ravel_multi_index(c, s.shape))
                g = 2.0 * s[c] * s[nb] / (s[c] + s[nb]) * h * float(alpha.get((ax, lin), 1.0))
                if g > 0:
                    edges.append((index[c], index[nb], g))
    bot = [(index[c], s[c] * h * h / (h / 2.0)) for c in cells if c[2] == 0]
    top = [(index[c], s[c] * h * h / (h / 2.0)) for c in cells if c[2] == nz - 1]
    par = list(range(len(cells)))

    def fnd(x):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x
    for a_, b_, _g in edges:
        ra, rb = fnd(a_), fnd(b_)
        if ra != rb:
            par[ra] = rb
    roots = {fnd(i) for i, _g in bot} | {fnd(i) for i, _g in top}
    keep = [i for i in range(len(cells)) if fnd(i) in roots]
    if not keep:
        return 0.0
    pos = {i: n for n, i in enumerate(keep)}
    L = np.zeros((len(keep), len(keep)))
    b = np.zeros(len(keep))
    for a_, b_, g in edges:
        if a_ in pos and b_ in pos:
            ia, ib = pos[a_], pos[b_]
            L[ia, ia] += g
            L[ib, ib] += g
            L[ia, ib] -= g
            L[ib, ia] -= g
    for i, g in bot:
        L[pos[i], pos[i]] += g
        b[pos[i]] += g
    for i, g in top:
        L[pos[i], pos[i]] += g
    phi = np.linalg.solve(L, b)
    I = sum(g * (1.0 - phi[pos[i]]) for i, g in bot)
    return I * nz * h / (nx * ny * h * h)


def plan_alpha_dict(plan):
    out = {}
    for ax in range(3):
        a = plan['axes'][ax]
        for lin, al in zip(np.asarray(a['lin']).tolist(), np.asarray(a['alpha']).tolist()):
            out[(ax, int(lin))] = float(al)
    return out


def plan_rows(plan):
    return sum(len(plan['axes'][ax]['lin']) for ax in range(3))


# ── 해석 면적 (생산 함수 밖 · 설계 §3-4 F16) ─────────────────────────────────
def _P(X, r):
    """∫ 2√(r²−X²) dX 의 원시함수."""
    X = max(-r, min(r, X))
    return X * math.sqrt(max(r * r - X * X, 0.0)) + r * r * math.asin(X / r)


def _Q(X, r, y):
    """∫ (y + √(r²−X²)) dX 의 원시함수."""
    X = max(-r, min(r, X))
    return y * X + 0.5 * _P(X, r)


def _Aq(x, y, r):
    """원 (중심 원점 · 반지름 r) ∩ {X ≤ x, Y ≤ y} 의 넓이 — 닫힌꼴."""
    if x <= -r or y <= -r:
        return 0.0
    xc = min(x, r)
    if y >= r:
        return _P(xc, r) - _P(-r, r)
    u = math.sqrt(r * r - y * y)
    if y >= 0:
        A = _P(min(xc, -u), r) - _P(-r, r)
        if xc > -u:
            A += _Q(min(xc, u), r, y) - _Q(-u, r, y)
        if xc > u:
            A += _P(xc, r) - _P(u, r)
        return A
    if xc <= -u:
        return 0.0
    return _Q(min(xc, u), r, y) - _Q(-u, r, y)


def disk_rect_area(cx, cy, r, x0, x1, y0, y1):
    f = lambda x, y: _Aq(x - cx, y - cy, r)          # noqa: E731
    return f(x1, y1) - f(x0, y1) - f(x1, y0) + f(x0, y0)


def _clip(poly, nx_, ny_, c):
    """다각형 ∩ {nx·x + ny·y ≤ c} (Sutherland–Hodgman)."""
    out = []
    for i in range(len(poly)):
        p, q = poly[i], poly[(i + 1) % len(poly)]
        fp, fq = nx_ * p[0] + ny_ * p[1] - c, nx_ * q[0] + ny_ * q[1] - c
        if fp <= 0:
            out.append(p)
        if (fp < 0 < fq) or (fq < 0 < fp):
            t = fp / (fp - fq)
            out.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
    return out


def _poly_area(poly):
    if len(poly) < 3:
        return 0.0
    return 0.5 * abs(sum(poly[i][0] * poly[(i + 1) % len(poly)][1] - poly[(i + 1) % len(poly)][0] * poly[i][1]
                         for i in range(len(poly))))


def strip_square_area(px, py, dx, dy, w, h):
    """띠 {|n·(x − p)| ≤ w} (n ⊥ (dx, dy)) ∩ 정사각형 [0,h]² 의 넓이."""
    nn = math.hypot(dx, dy)
    nx_, ny_ = -dy / nn, dx / nn
    c0 = nx_ * px + ny_ * py
    sq = [(0.0, 0.0), (h, 0.0), (h, h), (0.0, h)]
    poly = _clip(sq, nx_, ny_, c0 + w)
    poly = _clip(poly, -nx_, -ny_, -(c0 - w))
    return _poly_area(poly)


# ═════════════════════════ F 묶음 (설계 §3-4) ═════════════════════════
def _ion_slab(shape):
    return np.full(shape, 6, np.int8)


@case('F1 α=1 극한 (캡슐 없음 · 멀리) — off 와 σ · φ · n_dof 비트 같음')
def t_f1():
    sid = rand_ion_grid((3, 3, 4), 11)
    far = caps_of(line((0.1, 0.1, 9.0), (0.6, 0.1, 9.0), 6))         # 격자 (z ≤ 1.0) 밖
    p = plan_of(sid, ti(), far, H, 'ionic')
    chk('F1-a 먼 캡슐 → 계획 행 0', plan_rows(p) == 0, plan_rows(p))
    r0 = solve(sid, ti(), H)
    r1 = solve(sid, ti(), H, plan=p)
    chk('F1-b σ · φ · n_dof 비트 같음 (α ≡ 1)', same_solve(r0, r1), (r0['sigma_eff'], r1['sigma_eff']))
    chk('F1-c 기록 = 행 0 · solved', (r1.get('face_alpha') or {}).get('n_rows_used') == 0
        and (r1.get('face_alpha') or {}).get('solved') is True, r1.get('face_alpha'))


@case('F2 α=0 극한 — 손으로 절단한 면 (g=0) 과 σ · 성분 가지치기 같음')
def t_f2():
    h = 0.125                                                        # r 0.124 ≥ h/2 → 면 전체 덮음
    sid = _ion_slab((1, 1, 4))
    cap = caps_of(line((0.5 * h, -h, 2 * h), (0.5 * h, 2 * h, 2 * h), 13))   # z=2h 면 위 y 축 캡슐
    p = plan_of(sid, ti(), cap, h, 'ionic')
    a = plan_alpha_dict(p)
    lin_mid = int(np.ravel_multi_index((0, 0, 1), sid.shape))
    chk('F2-a 가운데 z 면 α = 0', a.get((2, lin_mid)) == 0.0, a)
    r = solve(sid, ti(), h, plan=p)
    ref = ref_sigma(np.where(sid > 0, SIG_SE, 0.0), h, {(2, lin_mid): 0.0})
    chk('F2-b 기둥 절단 → 관통 없음 (σ 0 · reason) = 손 절단 참조 0',
        r['sigma_eff'] == 0.0 and r.get('reason') == 'no_through_component' and ref == 0.0, (r.get('reason'), ref))
    #  옆 셀이 절단 면 하나로만 붙은 침대 — 절단되면 떠 있는 성분으로 가지치기된다 (E3 · 실제 간선 그래프).
    #  ⚠ 판 결합 띠 = vox + 0.1 µm (h 0.125 에서 1.8h) — 옆 셀은 두 판 모두에서 띠 밖 (nz 6 · k 2) 이어야 떠 있다.
    sid2 = np.zeros((2, 1, 6), np.int8)
    sid2[0] = 6
    sid2[1, 0, 2] = 6
    cap2 = caps_of(line((h, -h, 2.5 * h), (h, 2 * h, 2.5 * h), 13))        # x = h 면 위 (옆 셀의 유일한 면)
    p2 = plan_of(sid2, ti(), cap2, h, 'ionic')
    a2 = plan_alpha_dict(p2)
    lin_side = int(np.ravel_multi_index((0, 0, 2), sid2.shape))
    chk('F2-c 옆 면 α = 0', a2.get((0, lin_side)) == 0.0, a2.get((0, lin_side)))
    r2 = solve(sid2, ti(), h, plan=p2)
    s2 = np.where(sid2 > 0, SIG_SE, 0.0)
    ref2 = ref_sigma(s2, h, a2)
    chk('F2-d σ = 독립 참조 (같은 α · 손 절단) 1e-12', abs(r2['sigma_eff'] - ref2) <= 1e-12 * max(ref2, 1e-30),
        (r2['sigma_eff'], ref2))
    chk('F2-e 옆 셀 가지치기 (n_floating_dropped 1 · n_dof 6)',
        r2.get('n_floating_dropped') == 1 and r2.get('n_dof') == 6, (r2.get('n_floating_dropped'), r2.get('n_dof')))
    chk('F2-f 기록 n_isolated_by_cut = 1', (r2.get('face_alpha') or {}).get('n_isolated_by_cut') == 1,
        r2.get('face_alpha'))


def _f3_fixture():
    sid = rand_ion_grid((4, 3, 5), 7)
    cap = caps_of(line((0.13, 0.07, 0.61), (0.93, 0.66, 0.37), 9), line((0.71, 0.11, 0.18), (0.29, 0.69, 1.06), 7))
    return sid, cap


@case('F3 상호성 — 행렬 대칭 · 판을 바꿔 풀어도 같은 단자 컨덕턴스 (1e-12)')
def t_f3():
    sid, cap = _f3_fixture()
    p = plan_of(sid, ti(), cap, H, 'ionic')
    chk('F3-a 비대칭 픽스처에 α 행 있음', plan_rows(p) > 0, plan_rows(p))
    cap_L = []
    r = solve(sid, ti(), H, plan=p, capture=cap_L)
    L = cap_L[0]
    chk('F3-b 조립 행렬 정확 대칭', abs(L - L.T).max() == 0.0, abs(L - L.T).max())
    nz = sid.shape[2]
    Lz = nz * H
    pts, fid, kind = mkpaths(line((0.13, 0.07, Lz - 0.61), (0.93, 0.66, Lz - 0.37), 9),
                             line((0.71, 0.11, Lz - 0.18), (0.29, 0.69, Lz - 1.06), 7))
    capf = FA.build_capsules(pts, fid, kind)
    sidf = sid[:, :, ::-1].copy()
    pf = plan_of(sidf, ti(), capf, H, 'ionic')
    rf = solve(sidf, ti(), H, plan=pf)
    chk('F3-c 판 바꿈 (z 뒤집기) σ 같음 1e-12', abs(rf['sigma_eff'] - r['sigma_eff']) <= 1e-12 * r['sigma_eff'],
        (r['sigma_eff'], rf['sigma_eff']))


@case('F4 KCL — 노드 Σ 전류 0 (원장 g) · I_bot = I_top (직접 풀이)')
def t_f4():
    sid, cap = _f3_fixture()
    p = plan_of(sid, ti(), cap, H, 'ionic')
    r = solve(sid, ti(), H, plan=p)
    phi, cond = r['phi'], r['cond']
    sig = np.where(cond, ti()[sid], 0.0)
    led = r.get('_face_alpha') or {}
    over = {}
    for ax in range(3):
        e = (led.get('axes') or ({}, {}, {}))[ax]
        for lin, g in zip(np.asarray(e.get('lin', [])).tolist(), np.asarray(e.get('g', [])).tolist()):
            over[(ax, int(lin))] = float(g)
    net = np.zeros(sid.shape)
    for ax in range(3):
        sa = [slice(None)] * 3
        sb = [slice(None)] * 3
        sa[ax] = slice(0, -1)
        sb[ax] = slice(1, None)
        both = cond[tuple(sa)] & cond[tuple(sb)]
        for c in np.argwhere(both):
            c = tuple(int(v) for v in c)
            nb = list(c)
            nb[ax] += 1
            nb = tuple(nb)
            lin = int(np.ravel_multi_index(c, sid.shape))
            g = over.get((ax, lin), 2.0 * sig[c] * sig[nb] / (sig[c] + sig[nb]) * H)
            I = g * (phi[c] - phi[nb])
            net[c] += I
            net[nb] -= I
    (cb, gb, _), (ct, gt, _) = r['plate_edges']['bot'], r['plate_edges']['top']
    Ib = float(np.sum(gb * (1.0 - phi[cb])))
    It = float(np.sum(gt * (phi[ct] - 0.0)))
    np.add.at(net, cb, -gb * (1.0 - phi[cb]))
    np.add.at(net, ct, gt * phi[ct])
    chk('F4-a 노드 KCL (원장 g · 판 간선) max|Σ| ≤ 1e-10·I', np.abs(net[cond]).max() <= 1e-10 * Ib,
        np.abs(net[cond]).max() / max(Ib, 1e-30))
    chk('F4-b I_bot = I_top (1e-12)', abs(Ib - It) <= 1e-12 * Ib, (Ib, It))
    chk('F4-c 원장 행 = 계획 α × g0 (조립이 쓴 g 를 원장이 싣는다)', len(over) > 0, len(over))


@case('F5 회전 · 반사 — z 축 90° 회전 · x 반사에 σ_z 같음 (1e-12)')
def t_f5():
    n = 4
    W = n * H
    sid = rand_ion_grid((n, n, 5), 5)
    P1 = line((0.09375, 0.15625, 0.34375), (0.84375, 0.59375, 0.65625), 9)
    P2 = line((0.53125, 0.03125, 0.96875), (0.21875, 0.90625, 0.28125), 7)
    p = plan_of(sid, ti(), caps_of(P1, P2), H, 'ionic')
    r = solve(sid, ti(), H, plan=p)

    def rot(P):
        P = np.asarray(P, np.float64)
        return np.column_stack([W - P[:, 1], P[:, 0], P[:, 2]])
    sid_r = np.rot90(sid, 1, axes=(0, 1)).copy()
    pr = plan_of(sid_r, ti(), caps_of(rot(P1), rot(P2)), H, 'ionic')
    rr = solve(sid_r, ti(), H, plan=pr)
    chk('F5-a 90° 회전 σ 같음 1e-12', abs(rr['sigma_eff'] - r['sigma_eff']) <= 1e-12 * r['sigma_eff'],
        (r['sigma_eff'], rr['sigma_eff']))
    chk('F5-b 회전 α 다중집합 정확 같음', sorted(plan_alpha_dict(p).values()) == sorted(plan_alpha_dict(pr).values()))

    def refl(P):
        P = np.asarray(P, np.float64)
        return np.column_stack([W - P[:, 0], P[:, 1], P[:, 2]])
    sid_x = sid[::-1].copy()
    px = plan_of(sid_x, ti(), caps_of(refl(P1), refl(P2)), H, 'ionic')
    rx = solve(sid_x, ti(), H, plan=px)
    chk('F5-c x 반사 σ 같음 1e-12', abs(rx['sigma_eff'] - r['sigma_eff']) <= 1e-12 * r['sigma_eff'],
        (r['sigma_eff'], rx['sigma_eff']))


@case('F6 주기 seam — 정량 모드 거부 (seam 지원 = 나중)')
def t_f6():
    sid, cap = _f3_fixture()
    p = plan_of(sid, ti(), cap, H, 'ionic')
    _CG_CALLS[0] = 0
    chk('F6-a periodic_xy + face_alpha → 거부', raises(lambda: solve(sid, ti(), H, plan=p, periodic_xy=True)))
    chk('F6-b 거부는 CG 전 (호출 0)', _CG_CALLS[0] == 0, _CG_CALLS[0])


@case('F7 고정 기하 격자 조임 — h · K 사다리 (보고 · 합격선 미봉인 · K = 8 봉인)')
def t_f7():
    chk('F7-a K 는 F7 을 보기 전에 봉인 (K_SEALED = 8)', FA.K_SEALED == 8, FA.K_SEALED)
    Lb = 1.2
    path = line((-0.3, 0.61, 0.57), (1.5, 0.61, 0.57), 25)               # SE 판을 가로지르는 고정 캡슐 (x 축)

    def sig_at(h, K=None):
        n = int(round(Lb / h))
        sid = _ion_slab((n, n, n))
        pl = plan_of(sid, ti(), caps_of(path), h, 'ionic', K=K)
        return solve(sid, ti(), h, plan=pl)['sigma_eff']
    ref = sig_at(0.0375)
    rows = []
    for h in (0.3, 0.15, 0.075):
        s = sig_at(h)
        rows.append((h, s, abs(s - ref) / ref))
    ks = [(K, sig_at(0.15, K=K)) for K in (4, 8, 16)]
    ok = all(math.isfinite(s) and s > 0 for _h, s, _e in rows) and all(math.isfinite(s) for _k, s in ks)
    print('    보고 F7 (기준 h 0.0375 · σ_ref %.9g):' % ref)
    for h, s, e in rows:
        print(f'      h {h:<6} σ {s:.9g}  상대오차 {e:.3e}')
    if rows[1][2] > 0 and rows[2][2] > 0:
        print(f'      관측 차수 (0.15→0.075) {math.log(rows[1][2] / rows[2][2]) / math.log(2):.3f}')
    for K, s in ks:
        print(f'      K {K:<3} (h 0.15) σ {s:.9g}')
    chk('F7-b 사다리 실행 · 유한 (보고 — 합격선은 실행 전 봉인)', ok)


@case('F8 origin 8 위상 — σ 산포 보고 (face_alpha ↔ centerline 나란히 · 합격선 없음)')
def t_f8():
    h = 0.25
    Lb = 2.0
    g = np.arange(0.06, Lb, 0.08)
    se = np.array([[x, y, z] for x in g for y in g for z in g], np.float64)
    pt = line((-0.2, 0.93, 1.07), (2.2, 1.11, 0.91), 31)               # PTFE 중심선 (µm)
    out = {'face_alpha': [], 'centerline': []}
    for sx in (0.0, h / 2):
        for sy in (0.0, h / 2):
            for sz in (0.0, h / 2):
                lo = (-sx, -sy, -sz)
                hi = (Lb + sx, Lb + sy, Lb + sz)
                sid_off, _ = S3.rasterize(np.zeros((0, 3)), np.zeros(0), np.zeros(0, int), None, None, lo, hi, h,
                                          se_pts=se)
                plan = FA.build_plan(sid_off, ti(), FA.build_capsules(pt, np.zeros(len(pt), np.int64),
                                                                      np.ones(len(pt), np.int8)),
                                     lo=lo, vox=h, channel='ionic')
                rfa = solve(sid_off, ti(), h, plan=plan, z_top_um=Lb + sz, z_bot_um=sz)
                sid_cl, _ = S3.rasterize(np.zeros((0, 3)), np.zeros(0), np.zeros(0, int), pt, np.full(len(pt), 4),
                                         lo, hi, h, se_pts=se, add_fid=np.zeros(len(pt), np.int64))
                rcl = solve(sid_cl, ti(), h, z_top_um=Lb + sz, z_bot_um=sz)
                out['face_alpha'].append(rfa['sigma_eff'])
                out['centerline'].append(rcl['sigma_eff'])
    for k, v in out.items():
        v = np.asarray(v)
        print(f'    보고 F8 {k:<10} σ 평균 {v.mean():.6g} · CV {v.std() / v.mean():.3e} · max/min {v.max() / v.min():.6f}')
    chk('F8-a 8 위상 실행 · 유한 (보고만)', all(np.isfinite(v).all() and len(v) == 8 for v in map(np.asarray, out.values())))


@case('F9 투여 단조 — 캡슐 집합 A ⊂ B 면 α_B ≤ α_A (면마다 정확) · σ(B) ≤ σ(A)')
def t_f9():
    sid, _cap = _f3_fixture()
    PA = line((0.13, 0.07, 0.61), (0.93, 0.66, 0.37), 9)
    PB = line((0.71, 0.11, 0.18), (0.29, 0.69, 1.06), 7)
    pa = plan_of(sid, ti(), caps_of(PA), H, 'ionic')
    pb = plan_of(sid, ti(), caps_of(PA, PB), H, 'ionic')
    aa, ab = plan_alpha_dict(pa), plan_alpha_dict(pb)
    chk('F9-a A 의 모든 면이 B 에 있고 α_B ≤ α_A', all(k in ab and ab[k] <= v for k, v in aa.items()))
    chk('F9-b B 가 더 막는다 (행 수 ≥ · 어떤 면 α 감소)', len(ab) >= len(aa) and len(ab) > 0)
    ra = solve(sid, ti(), H, plan=pa)
    rb = solve(sid, ti(), H, plan=pb)
    chk('F9-c σ(B) ≤ σ(A) (Rayleigh)', rb['sigma_eff'] <= ra['sigma_eff'] * (1 + 1e-13), (ra['sigma_eff'], rb['sigma_eff']))


@case('F10 PTFE 없음 no-op — 빈 캡슐 → off 와 셀 · σ 비트 같음')
def t_f10():
    sid = rand_ion_grid((3, 4, 4), 3)
    caps = FA.build_capsules(np.zeros((0, 3)), np.zeros(0, np.int64), np.zeros(0, np.int8))
    chk('F10-a 빈 입력 → 선분 0 · 부피 0', caps['n_segments'] == 0 and caps['volume_um3'] == 0.0, caps.get('n_segments'))
    p = plan_of(sid, ti(), caps, H, 'ionic')
    r0 = solve(sid, ti(), H)
    r1 = solve(sid, ti(), H, plan=p)
    chk('F10-b σ · φ · n_dof 비트 같음', same_solve(r0, r1))


@case('F11 부피 — 조각마다 Σ(선분 길이·πr²) + 구 하나 (4/3·πr³) · 겹침 미차감 · 밴드 [0.5, 2]')
def t_f11():
    r = FA.ROPE_D_UM / 2.0
    c1 = caps_of(line((0, 0, 0), (1.0, 0, 0), 2))
    chk('F11-a 직선 하나', abs(c1['volume_um3'] - (1.0 * math.pi * r * r + 4.0 / 3.0 * math.pi * r ** 3)) < 1e-15,
        c1['volume_um3'])
    c2 = caps_of(np.array([[0, 0, 0], [0.3, 0, 0], [0.3, 0.4, 0]], float))
    chk('F11-b 꺾인 선 (이음마다 구를 더하지 않는다)',
        abs(c2['volume_um3'] - (0.7 * math.pi * r * r + 4.0 / 3.0 * math.pi * r ** 3)) < 1e-15, c2['volume_um3'])
    q = np.array([[0, 0, 0], [0.1, 0, 0], [0.2, 0, 0], [1.2, 0, 0], [1.3, 0, 0]], float)     # 0.2 → 1.2 = gap 분할
    c3 = caps_of(q)
    chk('F11-c gap 분할 = 조각 둘 (구 둘)', c3['n_pieces'] == 2
        and abs(c3['volume_um3'] - (0.3 * math.pi * r * r + 2 * 4.0 / 3.0 * math.pi * r ** 3)) < 1e-15,
        (c3['n_pieces'], c3['volume_um3']))
    c4 = caps_of(np.array([[0.5, 0.5, 0.5]]))
    chk('F11-d 점 하나 = 구 캡슐 (수 기록)', c4['n_point_pieces'] == 1
        and abs(c4['volume_um3'] - 4.0 / 3.0 * math.pi * r ** 3) < 1e-15, c4)
    chk('F11-e 밴드 판정 (닫힌 구간 · 참부피 없음 = unknown)',
        FA.volume_band_status(1.0, 2.0)[1] == 'in_band' and FA.volume_band_status(2.0, 1.0)[1] == 'in_band'
        and FA.volume_band_status(0.49, 1.0)[1] == 'out_of_band' and FA.volume_band_status(2.01, 1.0)[1] == 'out_of_band'
        and FA.volume_band_status(1.0, None)[1] == 'unknown_true_volume'
        and FA.volume_band_status(1.0, float('nan'))[1] == 'unknown_true_volume'
        and FA.volume_band_status(1.0, 0.0)[1] == 'unknown_true_volume')


def _f12_vgcf():
    """VGCF 기둥 (sid 3) 1×1×4 + 그 축방향 면 (3|3) 을 지나는 PTFE 캡슐."""
    h = 0.25
    sid = np.full((1, 1, 4), 3, np.int8)
    pid = np.full(sid.shape, -1, np.int32)
    cap_pts = line((-0.2, 0.125, 2 * h), (0.45, 0.125, 2 * h), 14)
    return h, sid, pid, cap_pts


def _f12_check():
    h, sid, pid, cap_pts = _f12_vgcf()
    p = plan_of(sid, te(), caps_of(cap_pts), h, 'electronic', pid=pid)
    chk('F12-a VGCF 축방향 면 (3|3) 면제 → 계획 행 0', plan_rows(p) == 0, plan_rows(p))
    r0 = solve(sid, te(), h, pid=pid)
    r1 = solve(sid, te(), h, plan=p, pid=pid)
    chk('F12-b σ · φ 비트 같음 (캡슐 없는 것과)', same_solve(r0, r1), (r0['sigma_eff'], r1['sigma_eff']))
    return h, sid, cap_pts, r0


@case('F12 같은 물체 면제 — AM 같은 입자 · VGCF 축방향 = g 그대로 · centerline 은 자른다 (판별) · AM–AM 목은 α')
def t_f12():
    h, sid, cap_pts, r0 = _f12_check()
    sid_cl, _ = S3.rasterize(np.zeros((0, 3)), np.zeros(0), np.zeros(0, int),
                             np.vstack([line((0.125, 0.125, 0.0), (0.125, 0.125, 1.0), 9), cap_pts]),
                             np.concatenate([np.full(9, 2), np.full(len(cap_pts), 4)]), (0, 0, 0), (0.25, 0.25, 1.0), h,
                             add_fid=np.concatenate([np.zeros(9, np.int64), np.ones(len(cap_pts), np.int64)]))
    rcl = solve(sid_cl, te(), h)
    chk('F12-c 대조: centerline 은 VGCF 셀을 sid 7 로 덮어 자른다 (σ 0)', r0['sigma_eff'] > 0
        and int((sid_cl == 7).sum()) > 0 and rcl['sigma_eff'] == 0.0, (int((sid_cl == 7).sum()), rcl['sigma_eff']))
    am = np.full((2, 2, 4), 2, np.int8)
    pid1 = np.zeros(am.shape, np.int32)
    capa = caps_of(line((-0.1, 0.27, 0.43), (0.6, 0.21, 0.61), 12))
    pa = plan_of(am, te(), capa, h, 'electronic', pid=pid1)
    chk('F12-d 같은 AM 입자 (pid 같음) 안 면 면제 → 행 0', plan_rows(pa) == 0, plan_rows(pa))
    chk('F12-e σ 비트 같음', same_solve(solve(am, te(), h, pid=pid1), solve(am, te(), h, plan=pa, pid=pid1)))
    pid2 = np.where(np.arange(4)[None, None, :] >= 2, 1, 0).astype(np.int32) * np.ones(am.shape, np.int32)
    capn = caps_of(line((-0.1, 0.27, 0.5), (0.6, 0.27, 0.5), 12))     # pid 경계 면 (z = 2h) 위
    pn = plan_of(am, te(), capn, h, 'electronic', pid=pid2)
    an = plan_alpha_dict(pn)
    chk('F12-f AM–AM 목 (같은 sid · 다른 pid) 면에 α < 1', any(k[0] == 2 for k in an) and min(an.values()) < 1.0, an)
    rn0 = solve(am, te(), h, pid=pid2)
    rn1 = solve(am, te(), h, plan=pn, pid=pid2)
    chk('F12-g 목이 막혀 σ 감소', rn1['sigma_eff'] < rn0['sigma_eff'], (rn0['sigma_eff'], rn1['sigma_eff']))


def _f13_fixture():
    """전자 (AM 기둥) · 이온 (SE) 두 채널이 다 도는 침대 + 둘을 다 가로지르는 캡슐."""
    h = 0.25
    sid = np.full((4, 2, 4), 6, np.int8)
    sid[0:2] = 2
    pid = np.full(sid.shape, -1, np.int32)
    pid[0:2] = np.where(np.arange(4)[None, None, :] >= 2, 1, 0)
    cap = caps_of(line((-0.1, 0.25, 0.5), (1.1, 0.25, 0.5), 25))          # z = 2h 면 · y = h 모서리
    return h, sid, pid, cap


@case('F13 채널 독립 — 전자 계획은 전자 면만 · 이온 계획은 이온 면만 · 다른 채널 계획 = 거부')
def t_f13():
    h, sid, pid, cap = _f13_fixture()
    pe = plan_of(sid, te(), cap, h, 'electronic', pid=pid)
    pi = plan_of(sid, ti(), cap, h, 'ionic')
    se_, si_ = te()[sid] > 0, ti()[sid] > 0

    def rows_ok(plan, cond):
        for ax in range(3):
            for lin in np.asarray(plan['axes'][ax]['lin']).tolist():
                c = np.unravel_index(lin, sid.shape)
                nb = list(c)
                nb[ax] += 1
                if not (cond[c] and cond[tuple(nb)]):
                    return False
        return True
    chk('F13-a 전자 계획 행 > 0 · 전부 전자 도체 면', plan_rows(pe) > 0 and rows_ok(pe, se_), plan_rows(pe))
    chk('F13-b 이온 계획 행 > 0 · 전부 이온 도체 면', plan_rows(pi) > 0 and rows_ok(pi, si_), plan_rows(pi))
    ri0, ri1 = solve(sid, ti(), h), solve(sid, ti(), h, plan=pi)
    chk('F13-c 이온 계획이 이온 σ 를 바꾼다 (감소)', ri1['sigma_eff'] < ri0['sigma_eff'], (ri0['sigma_eff'], ri1['sigma_eff']))
    _CG_CALLS[0] = 0
    chk('F13-d 이온 계획을 전자 솔브에 = 거부 (CG 전)',
        raises(lambda: solve(sid, te(), h, plan=pi, pid=pid)) and _CG_CALLS[0] == 0)
    chk('F13-e 전자 계획을 이온 솔브에 = 거부', raises(lambda: solve(sid, ti(), h, plan=pe, pid=pid)))


# ── F16 해석 개구율 ─────────────────────────────────────────────────────────
F16_H = 0.5


def _f16_cases():
    """(이름, 경로 점열, 해석 막힌 넓이) — 두 셀 (1×1×2) 의 가운데 면 (z = h) 기준."""
    h = F16_H
    r = FA.ROPE_D_UM / 2.0
    out = []
    for nm, (cx, cy) in (('수직·면중앙', (0.25, 0.25)), ('수직·모서리걸침', (0.05, 0.25)), ('수직·꼭짓점', (0.03, 0.04)),
                         ('수직·밖걸침', (-0.06, 0.25))):
        out.append((nm, line((cx, cy, h - 0.2), (cx, cy, h + 0.2), 9), disk_rect_area(cx, cy, r, 0, h, 0, h)))
    for t in (0.0, 0.05, 0.11):
        for y0 in (0.25, 0.05):
            w = math.sqrt(r * r - t * t)
            ov = max(0.0, min(y0 + w, h) - max(y0 - w, 0.0))
            out.append((f'평행·t{t}·y{y0}', line((-0.5, y0, h + t), (1.0, y0, h + t), 31), h * ov))
    d = np.array([1.0, 0.5, 0.0]) / math.sqrt(1.25)
    p0 = np.array([0.25, 0.25, h])
    out.append(('평행·사선', line(p0 - 0.9 * d, p0 + 0.9 * d, 19), strip_square_area(0.25, 0.25, d[0], d[1], r, h)))
    return out


def _f16_alpha_check(K_list=(8, 1024)):
    h = F16_H
    worst = 0.0
    for nm, pts, area in _f16_cases():
        cp = caps_of(pts)
        exact = 1.0 - area / (h * h)
        errs = {K: abs(float(FA.face_alpha_values(cp, 2, np.array([[0, 0, 0]]), (0, 0, 0), h, K=K)[0]) - exact)
                for K in K_list}
        worst = max(worst, errs[K_list[-1]])
        chk(f'F16-α {nm}: K→∞ 극한 = 해석식 (K {K_list[-1]} 오차 {errs[K_list[-1]]:.2e} < 2e-3 · K 8 오차 {errs[8]:.2e} = 보고)',
            errs[K_list[-1]] < 2e-3, errs)
    return worst


def ref_alpha_K(pts, h, K, r, z_face):
    """**독립** K × K 중점 구적 (생산 코드 밖 · 선분마다 루프) — 정사각형 [0,h]² × {z = z_face} 면의 열린 분율."""
    u = (np.arange(K) + 0.5) / K * h
    X, Y = np.meshgrid(u, u, indexing='ij')
    Q = np.stack([X.ravel(), Y.ravel(), np.full(K * K, z_face)], -1)
    inside = np.zeros(K * K, bool)
    P = np.asarray(pts, np.float64)
    for a, b in zip(P[:-1], P[1:]):
        d = b - a
        t = np.clip(((Q - a) @ d) / (d @ d), 0.0, 1.0)
        w = Q - a - t[:, None] * d
        inside |= (w * w).sum(1) <= r * r
    return 1.0 - inside.sum() / float(K * K)


def _f16_series_check():
    h = F16_H
    sid = _ion_slab((1, 1, 2))
    for nm, pts, _area in _f16_cases():
        cp = caps_of(pts)
        pl = plan_of(sid, ti(), cp, h, 'ionic')
        al = plan_alpha_dict(pl).get((2, 0), 1.0)
        al_ref = ref_alpha_K(pts, h, 8, FA.ROPE_D_UM / 2.0, h)
        chk(f'F16-구적 {nm}: 계획 α_K8 = 독립 K=8 중점 구적 (정확)', al == al_ref, (al, al_ref))
        r = solve(sid, ti(), h, plan=pl)
        want = 2.0 * SIG_SE * al_ref / (al_ref + 1.0)
        chk(f'F16-직렬 {nm}: σ = 2σα/(α+1) (독립 α_K8 {al_ref:.6f}) 1e-12',
            abs(r['sigma_eff'] - want) <= 1e-12 * want, (r['sigma_eff'], want))


@case('F16 해석 개구율 (판별력) — 원 · 띠 ∩ 정사각형 해석 넓이 · 두 셀 직렬 g = α·g0')
def t_f16():
    _f16_alpha_check()
    _f16_series_check()


def _f17_check():
    h = 0.25
    sid = _ion_slab((2, 2, 3))
    cap = caps_of(line((-0.2, 0.125, 0.0), (0.7, 0.125, 0.0), 19))       # 바닥 판 평면 (z = 0) 위 · y 0.125 (j=0 줄 한가운데)
    p = plan_of(sid, ti(), cap, h, 'ionic')
    r0 = solve(sid, ti(), h)
    r1 = solve(sid, ti(), h, plan=p)
    (c0, g0, _), (c1, g1, _) = r0['plate_edges']['bot'], r1['plate_edges']['bot']
    chk('F17-a 판 결합 g 비트 같음 (v0 = 판에 α 미적용)',
        np.asarray(g0).tobytes() == np.asarray(g1).tobytes() and all(np.array_equal(a, b) for a, b in zip(c0, c1)))
    pc = (r1.get('face_alpha') or {}).get('plate_cross_columns') or {}
    chk('F17-b 가로지름 기둥 수 기록 (바닥 2 · 위 0)', pc.get('bot') == 2 and pc.get('top') == 0, pc)
    return r0, r1


@case('F17 판 근처 캡슐 — 판 결합 g = 캡슐 없는 것과 비트 같음 · 기둥 수 기록')
def t_f17():
    _f17_check()


@case('F14 변이 — α² · α^p · (1−α) · 반 셀 어긋남 · 면제 무시 · 판에 α · 다른 채널 · 절단 미가지치기 = 실패해야')
def t_f14():
    def caught(fn):
        _MUTE.append([])
        try:
            quiet(fn)
            res = _MUTE[-1]
            return bool(res) and not all(res)
        except Exception:                                 # noqa: BLE001 — 변이가 시험을 죽여도 적발이다
            return True
        finally:
            _MUTE.pop()

    @contextlib.contextmanager
    def patched(mod, name, value):
        old = getattr(mod, name)
        setattr(mod, name, value)
        try:
            yield
        finally:
            setattr(mod, name, old)
    _orig_alpha = FA._alpha_from_cover
    _orig_cond = FA._channel_cond

    def _f13_ion_check():
        h_, sid_, _pid, cap_ = _f13_fixture()
        pl = plan_of(sid_, ti(), cap_, h_, 'ionic')
        chk('F13 이온 계획이 이온 면에서 σ 를 낮춘다', plan_rows(pl) > 0
            and solve(sid_, ti(), h_, plan=pl)['sigma_eff'] < solve(sid_, ti(), h_)['sigma_eff'])
    muts = [
        ('α²', '_alpha_from_cover', lambda n, K: _orig_alpha(n, K) ** 2, _f16_series_check),
        ('α^0.5', '_alpha_from_cover', lambda n, K: _orig_alpha(n, K) ** 0.5, _f16_series_check),
        ('1−α', '_alpha_from_cover', lambda n, K: 1.0 - _orig_alpha(n, K), _f16_series_check),
        ('반 셀 어긋남 (면 평면 = 셀 중심)', '_FACE_PLANE_OFFSET', 0.5, _f16_alpha_check),
        ('면제 무시', '_exempt_mask', lambda ch, sa, sb, pa, pb: np.zeros(np.shape(sa), bool), _f12_check),
        ('판에 α', 'plate_coupling_factor', lambda fap, ii, jj, kk, side: FA._plate_alpha(fap, ii, jj, kk, side),
         _f17_check),
        ('다른 채널 (이온 계획을 전자 도체로)', '_channel_cond',
         lambda ch, sg, sid, lin=None: _orig_cond('electronic', te(), sid, lin), _f13_ion_check),
        ('절단 면을 가지치기에 안 넘김', 'cut_lin', lambda fap: tuple(np.zeros(0, np.int64) for _ in range(3)), t_f2),
    ]
    for nm, attr, val, fn in muts:
        with patched(FA, attr, val):
            chk(f'F14 변이 [{nm}] 적발', caught(fn))


@case('F15 입구 거부 — NaN · inf · 길이 불일치 · 떨어진 같은 fid · 정확 중복 · fid 형 · kind · 지름 법칙 · K (조립 전 · CG 0)')
def t_f15():
    P = line((0, 0, 0), (1, 0, 0), 5)
    Q = line((0, 0.5, 0), (1, 0.5, 0), 5)
    pts, fid, kind = mkpaths(P, Q)
    bad = pts.copy()
    bad[3, 1] = np.nan
    chk('F15-a NaN 좌표', raises(lambda: FA.build_capsules(bad, fid, kind)))
    bad2 = pts.copy()
    bad2[2, 0] = np.inf
    chk('F15-b inf 좌표', raises(lambda: FA.build_capsules(bad2, fid, kind)))
    chk('F15-c fid 길이 불일치', raises(lambda: FA.build_capsules(pts, fid[:-1], kind)))
    chk('F15-d kind 길이 불일치', raises(lambda: FA.build_capsules(pts, fid, kind[:-1])))
    split = np.array([0, 0, 0, 1, 1, 1, 1, 1, 0, 0], np.int64)
    chk('F15-e 같은 fid 가 떨어진 두 블록', raises(lambda: FA.build_capsules(pts, split, kind)))
    dup_pts, dup_fid, dup_kind = mkpaths(P, P)
    chk('F15-f 정확 중복 경로', raises(lambda: FA.build_capsules(dup_pts, dup_fid, dup_kind)))
    chk('F15-g 음수 fid', raises(lambda: FA.build_capsules(pts, fid - 1, kind)))
    chk('F15-h fid 실수형', raises(lambda: FA.build_capsules(pts, fid.astype(np.float64), kind)))
    chk('F15-i fid 전각 숫자 문자열', raises(lambda: FA.build_capsules(pts, np.array(['１'] * 5 + ['２'] * 5), kind)))
    chk('F15-j kind = 그룹 (경로 아님)', raises(lambda: FA.build_capsules(pts, fid, np.zeros(len(pts), np.int8))))
    chk('F15-k 모르는 지름 법칙', raises(lambda: FA.build_capsules(pts, fid, kind, dia_law='seeder_di')))
    sid = _ion_slab((2, 2, 2))
    cp = FA.build_capsules(pts, fid, kind)
    chk('F15-l K = 0 · 2.5 · True 거부', all(raises(lambda K=K: plan_of(sid, ti(), cp, H, 'ionic', K=K)) for K in (0, 2.5, True)))
    chk('F15-m 모르는 채널', raises(lambda: plan_of(sid, ti(), cp, H, 'thermal')))
    chk('F15-n 전자 채널인데 pid 없음', raises(lambda: plan_of(sid, te(), cp, H, 'electronic', pid=None)))
    chk('F15-o 정수 좌표 배열 (float 아님) 은 받는다 · 객체 배열은 거부',
        FA.build_capsules(np.array([[0, 0, 0], [1, 0, 0]]), np.array([0, 0]), np.array([1, 1]))['n_segments'] == 1
        and raises(lambda: FA.build_capsules(np.array([[0, 0, 0], [1, 0, 0]], object), np.array([0, 0]), np.array([1, 1]))))


@case('F-DIA 지름 법칙 — (가) rope Ø0.248 단일 · (다) 두 집단 = 경로 정준 키 해시 (순열 불변 · 보고만)')
def t_fdia():
    chk('DIA-a rope = 모든 경로 r 0.124', FA.ROPE_D_UM == 0.248 and FA.DIA_LAWS == ('rope', 'two_pop'))
    rng = np.random.default_rng(3)
    paths = [line(rng.random(3) * 5, rng.random(3) * 5, 4) for _ in range(400)]
    c = caps_of(*paths, dia_law='two_pop')
    frac = c['dia_classes']['rope'] / 400.0
    chk(f'DIA-b 두 집단 개수비 ≈ 0.13 (실측 {frac:.3f})', 0.08 <= frac <= 0.18, c['dia_classes'])
    perm = [paths[i] for i in rng.permutation(400)]
    c2 = caps_of(*perm, dia_law='two_pop')
    chk('DIA-c 순열 불변 (경로 순서 · fid 번호와 무관)', c2['dia_classes'] == c['dia_classes']
        and abs(c2['volume_um3'] - c['volume_um3']) <= 1e-12 * c['volume_um3'])


# ═════════════════════════ C 묶음 — 계약 ═════════════════════════
def _base_plan():
    sid, cap = _f3_fixture()
    return sid, cap, plan_of(sid, ti(), cap, H, 'ionic')


def _remake_fp(plan):
    """변조 뒤 지문을 다시 만든 계획 (지문만으로 막는 게 아니라 불변량이 막는지 본다 · Q7 교훈)."""
    plan = dict(plan)
    plan['fp_rows'] = FA.rows_fp(plan['axes'])
    plan['fp_plan'] = FA.plan_fp(plan)
    return plan


def _tamper(plan, ax, **repl):
    axes = [dict(a) for a in plan['axes']]
    for k, v in repl.items():
        axes[ax][k] = v
    p = dict(plan)
    p['axes'] = tuple(axes)
    return _remake_fp(p)


@case('C 계약 — 계획 무결성 (지문 · 격자 · 불변량 · 행 자격) · 동시 사용 거부 · CG 0')
def t_contract():
    sid, cap, p = _base_plan()
    ax = next(a for a in range(3) if len(p['axes'][a]['lin']))
    lin0 = np.asarray(p['axes'][ax]['lin'])
    al0 = np.asarray(p['axes'][ax]['alpha'])
    bad = {
        'C1 모양 다름': (lambda: solve(sid[:, :, :-1].copy(), ti(), H, plan=p)),
        'C2 솔버 vox ≠ 계획 vox (RIMP-05)': (lambda: solve(sid, ti(), H * 1.0000001, plan=p)),
        'C3 sid 바뀜 (지문)': (lambda: solve(np.where(sid == 5, 6, 5).astype(np.int8), ti(), H, plan=p)),
        'C4 σ 표 다름 (다른 채널 · 지문)': (lambda: solve(sid, S3.ionic_sigma_table(SIG_SDCP_I, 0.004), H, plan=p)),
        'C5 α 격자 밖 (0.3 · 지문 다시)': (lambda: solve(sid, ti(), H, plan=_tamper(p, ax, alpha=np.where(
            np.arange(len(al0)) == 0, 0.3, al0)))),
        'C6a α NaN': (lambda: solve(sid, ti(), H, plan=_tamper(p, ax, alpha=np.where(np.arange(len(al0)) == 0, np.nan, al0)))),
        'C6b α = 1 행 (계획에 없어야)': (lambda: solve(sid, ti(), H, plan=_tamper(p, ax, alpha=np.where(
            np.arange(len(al0)) == 0, 1.0, al0)))),
        'C6c α > 1': (lambda: solve(sid, ti(), H, plan=_tamper(p, ax, alpha=np.where(np.arange(len(al0)) == 0, 1.25, al0)))),
        'C6d α < 0': (lambda: solve(sid, ti(), H, plan=_tamper(p, ax, alpha=np.where(np.arange(len(al0)) == 0, -0.25, al0)))),
        'C7 중복 행': (lambda: solve(sid, ti(), H, plan=_tamper(p, ax, lin=np.concatenate([lin0, lin0[:1]]),
                                                             alpha=np.concatenate([al0, al0[:1]])))),
        'C7b 행 범위 밖 (축 끝 셀)': (lambda: solve(sid, ti(), H, plan=_tamper(p, ax, lin=np.where(
            np.arange(len(lin0)) == len(lin0) - 1, sid.size - 1, lin0)))),
        'C8 지문 그대로 · 행만 바꿈 (E5)': (lambda: solve(sid, ti(), H, plan=dict(p, axes=tuple(
            dict(a, alpha=np.asarray(a['alpha']) * 0.5) if i == ax else a for i, a in enumerate(p['axes']))))),
        'C10a + rint 표': (lambda: solve(sid, ti(), H, plan=p, rint={(5, 6): 1e-3})),
        'C10b + ①′ iface': (lambda: solve(sid, ti(), H, plan=p, iface={'kind': 'x'})),
        'C11 모르는 계획 판': (lambda: solve(sid, ti(), H, plan=dict(p, version='s1-face-alpha-v0'))),
        'C11b 모르는 계획 종류': (lambda: solve(sid, ti(), H, plan=dict(p, kind='am_iface_plan'))),
    }
    for nm, fn in bad.items():
        _CG_CALLS[0] = 0
        chk(f'{nm} → 거부 · CG 0', raises(fn) and _CG_CALLS[0] == 0, _CG_CALLS[0])
    #  C9 — 면제 면 · 비도체 면 행 (지문 다시) = 거부
    h, sidv, pidv, capv = _f12_vgcf()
    pv = plan_of(sidv, te(), caps_of(capv), h, 'electronic', pid=pidv)
    pv_bad = _tamper(pv, 2, lin=np.array([int(np.ravel_multi_index((0, 0, 1), sidv.shape))], np.int64),
                     alpha=np.array([0.875]))
    _CG_CALLS[0] = 0
    chk('C9a 면제 면 (VGCF|VGCF) 에 행 → 거부', raises(lambda: solve(sidv, te(), h, plan=pv_bad, pid=pidv))
        and _CG_CALLS[0] == 0)
    sid_h = _ion_slab((1, 1, 4))
    sid_h[0, 0, 2] = 0
    ph = plan_of(sid_h, ti(), FA.build_capsules(np.zeros((0, 3)), np.zeros(0, np.int64), np.zeros(0, np.int8)), H, 'ionic')
    ph_bad = _tamper(ph, 2, lin=np.array([int(np.ravel_multi_index((0, 0, 1), sid_h.shape))], np.int64),
                     alpha=np.array([0.5]))
    chk('C9b 비도체 셀이 낀 면에 행 → 거부', raises(lambda: solve(sid_h, ti(), H, plan=ph_bad)))
    _h, sid13, pid13, cap13 = _f13_fixture()
    pe = plan_of(sid13, te(), cap13, _h, 'electronic', pid=pid13)
    chk('C12 전자 계획 + pid 없음 → 거부', raises(lambda: solve(sid13, te(), _h, plan=pe)))
    chk('C13 전자 계획 + 다른 pid → 거부', raises(lambda: solve(sid13, te(), _h, plan=pe, pid=np.where(pid13 >= 0, 1 - pid13, -1)
                                                          .astype(np.int32))))
    r = solve(sid, ti(), H, plan=p)
    rec = r.get('face_alpha') or {}
    chk('C14 기록 필드 (판 · 채널 · K · 행 · 절단 · 판 규칙 · 지문 · solved)',
        rec.get('operator') == FA.S1_OPERATOR_VERSION and rec.get('channel') == 'ionic' and rec.get('K') == 8
        and isinstance(rec.get('n_rows_used'), int) and rec.get('n_rows_used') > 0
        and rec.get('plate_rule') == FA.PLATE_RULE and rec.get('fp_plan') == p['fp_plan'] and rec.get('solved') is True,
        rec)
    rx = solve(sid[:, :, :1].copy(), ti(), H, plan=plan_of(sid[:, :, :1].copy(), ti(), cap, H, 'ionic'))
    chk('C15 조기 반환 해에도 기록 (solved False)', (rx.get('face_alpha') or {}).get('solved') is False
        and bool(rx.get('reason')), (rx.get('reason'), rx.get('face_alpha')))
    led = r.get('_face_alpha') or {}
    chk('C16 원장 (E1 · E5) — 지문 · 축 원장', led.get('kind') == FA.EDGES_KIND and led.get('fp_sid')
        and led.get('fp_edges') == FA.edges_fp(led.get('axes')), sorted(led))
    chk('C17 원장 읽기 = 지문 대조 (정상 통과)', FA.edges_ctx_from(r, sid, ti()) is not None)
    r_bad = dict(r)
    r_bad['_face_alpha'] = dict(led, axes=tuple(dict(a, g=np.asarray(a['g']) * 2) if i == ax else a
                                                for i, a in enumerate(led['axes'])))
    chk('C18 원장 변조 → 읽기 거부 (E5)', raises(lambda: FA.edges_ctx_from(r_bad, sid, ti())))
    chk('C19 다른 sid 로 원장 읽기 → 거부', raises(lambda: FA.edges_ctx_from(r, np.where(sid == 5, 6, 5).astype(np.int8), ti())))
    r0 = solve(sid, ti(), H)
    chk('C20 끈 해 = 기록 · 원장 키 없음 (옛 반환 키 그대로)', 'face_alpha' not in r0 and '_face_alpha' not in r0, sorted(r0))
    old_chunk = FA._FACE_CHUNK
    try:
        FA._FACE_CHUNK = 3
        p3 = plan_of(sid, ti(), cap, H, 'ionic')
    finally:
        FA._FACE_CHUNK = old_chunk
    chk('C21 면 묶음 크기 불변 (묶음 3 ↔ 기본) — 행 · α 바이트 같음', p3['fp_rows'] == p['fp_rows'] and plan_rows(p3) == plan_rows(p))
    capt = dict(cap, A=np.asarray(cap['A']) + 0.01)
    chk('C22 캡슐 기하 변조 (끝점 이동 · 지문 그대로) → 계획 입구 거부', raises(lambda: solve(sid, ti(), H, plan=dict(p, caps=capt))))

    def iso_brute(cond, cuts):
        shape = cond.shape
        deg = np.zeros(shape, int)
        dc = np.zeros(shape, int)
        for ax in range(3):
            sa = [slice(None)] * 3
            sb = [slice(None)] * 3
            sa[ax] = slice(0, -1)
            sb[ax] = slice(1, None)
            both = cond[tuple(sa)] & cond[tuple(sb)]
            deg[tuple(sa)] += both
            deg[tuple(sb)] += both
            for lin in np.asarray(cuts[ax]).tolist():
                c = np.unravel_index(lin, shape)
                nb = list(c)
                nb[ax] += 1
                if cond[c] and cond[tuple(nb)]:
                    dc[c] += 1
                    dc[tuple(nb)] += 1
        return int((cond & (deg > 0) & (deg == dc)).sum())
    rng = np.random.default_rng(4)
    okk = True
    for _ in range(20):
        cnd = rng.random((4, 3, 5)) < 0.7
        cuts = tuple(np.flatnonzero((rng.random(cnd.shape) < 0.4).reshape(-1)
                                    & (np.stack(np.unravel_index(np.arange(cnd.size), cnd.shape), -1)[:, a]
                                       < cnd.shape[a] - 1)) for a in range(3))
        okk &= FA.isolated_by_cut(cnd, cuts) == iso_brute(cnd, cuts)
    chk('C23 isolated_by_cut (절단 면 주변만) = 격자 전체 무차별 계산 (무작위 20)', okk)


@case('C-D 진단 거부 (E2) — je · 소산 분담 · |J| 점군 · Joule 은 face_alpha 해를 거부 (v0)')
def t_diag():
    h, sid, pid, cap = _f13_fixture()
    pe = plan_of(sid, te(), cap, h, 'electronic', pid=pid)
    r = solve(sid, te(), h, plan=pe, pid=pid)
    r0 = solve(sid, te(), h, pid=pid)
    sel = (1, 2, 3, 4, 5, 7, 8)
    for nm, fn in (('per_particle_current', lambda rr: S3.per_particle_current(rr, sid, pid, te(), 2)),
                   ('phase_current_share', lambda rr: S3.phase_current_share(rr, sid, te())),
                   ('field_point_cloud', lambda rr: S3.field_point_cloud(rr, sid, te(), h, sel)),
                   ('joule_hotspot', lambda rr: S3.joule_hotspot(rr, sid, te(), h, sel))):
        chk(f'D {nm}: face_alpha 해 거부 · 끈 해 정상', raises(lambda fn=fn: fn(r), (ValueError,))
            and not raises(lambda fn=fn: fn(r0), (ValueError,)))


@case('C-R 영수증 — not_requested · disabled · applied · absent_geometry · failed · missing (다른 계획)')
def t_receipt():
    sid, cap, p = _base_plan()
    r = solve(sid, ti(), H, plan=p)
    empty = plan_of(sid, ti(), FA.build_capsules(np.zeros((0, 3)), np.zeros(0, np.int64), np.zeros(0, np.int8)), H, 'ionic')
    r_e = solve(sid, ti(), H, plan=empty)
    other = plan_of(sid, ti(), caps_of(line((0.2, 0.2, 0.2), (0.6, 0.5, 0.9), 5)), H, 'ionic')
    prx = plan_of(sid[:, :, :1].copy(), ti(), cap, H, 'ionic')
    rx = solve(sid[:, :, :1].copy(), ti(), H, plan=prx)
    sr = FA.solve_receipt
    chk('R-a 요청 없음', sr(None, None, requested=False)['status'] == 'not_requested')
    chk('R-b 요청 · 끔', sr(None, None, requested=True, disabled_why='--no-ion')['status'] == 'disabled')
    chk('R-c applied (행 > 0)', sr(r, p, requested=True)['status'] == 'applied')
    chk('R-d absent_geometry (행 0)', sr(r_e, empty, requested=True)['status'] == 'absent_geometry')
    chk('R-e failed (조기 반환 · 사유)', sr(rx, prx, requested=True)['status'] == 'failed'
        and bool(sr(rx, prx, requested=True).get('why')))
    chk('R-f missing (다른 계획의 해)', sr(r, other, requested=True)['status'] == 'missing')
    chk('R-g missing (계획을 안 넘긴 해)', sr(solve(sid, ti(), H), p, requested=True)['status'] == 'missing')
    chk('R-h 요청 없는데 face_alpha 기록 = 위반 표지', sr(r, None, requested=False)['status'] == 'applied_without_request')


# ═════════════════════════ R 묶음 — run_contract ═════════════════════════
def _cohort_manifests():
    import glob
    out = []
    for f in sorted(glob.glob(os.path.join(ROOT, 'docs/data/w4_ptfe_centerline_20260827/p2_*.json'))
                    + glob.glob(os.path.join(ROOT, 'docs/data/w4b_ptfe_off_20260827/p2_*.json'))):
        out.append(json.load(open(f, encoding='utf-8'))['step3']['manifest'])
    return out


def fa_manifest(channels=('electronic', 'ionic'), dia_law='rope', ionic_plan=False):
    """봉인 코호트 매니페스트 하나를 face_alpha LEAN 2 꼴로 바꾼 합성 매니페스트 (계약 단위 시험용)."""
    m = json.loads(json.dumps(_cohort_manifests()[0]))
    m.update(ptfe_stamp='face_alpha', ptfe_stamp_requested='face_alpha', ptfe_zero_dof=False, ptfe_cells_observed=0,
             field_requested=False,
             component_plan={'electronic': True, 'ionic': bool(ionic_plan), 'thermal': False, 'pore': False,
                             'collector': False})
    prot = FA.protocol_record(channels, dia_law)
    rc = {'electronic_main': {'status': 'applied', 'n_rows_used': 7, 'n_cut_used': 0, 'solved': True, 'fp_plan': 'e' * 32},
          'electronic_wetted': {'status': 'disabled', 'why': '--no-collector'},
          'electronic_bare': {'status': 'disabled', 'why': '--no-collector'},
          'ionic': ({'status': 'disabled', 'why': '--no-ion'} if 'ionic' in channels else {'status': 'not_requested'})}
    if 'electronic' not in channels:
        rc['electronic_main'] = {'status': 'not_requested'}
        rc['electronic_wetted'] = rc['electronic_bare'] = {'status': 'not_requested'}
    ev = FA.evidence_record(capsules={'n_paths': 2, 'n_pieces': 2, 'n_point_pieces': 0, 'n_segments': 40,
                                      'volume_um3': 1.5, 'dia_classes': {'rope': 2}},
                            volume=FA.volume_record(1.5, None), faces={'electronic': None, 'ionic': None},
                            receipts=rc, off_grid_ptfe_point_cells={'0': 3, '6': 5},
                            fp={'caps': 'c' * 32, 'plan_electronic': ('e' * 32 if 'electronic' in channels else None),
                                'plan_ionic': None})
    m['ca_ext'] = {'schema': RC.CA_EXT_SCHEMA, 'ptfe_face': {'protocol': prot, 'evidence': ev}}
    m['physics_protocol_id'] = RC.physics_protocol_id(m)
    return m


@case('R run_contract — p3ca id · unknown:ca_ext · 세대 · PTFE 기록 · ca_ext_record_ok · 봉인 p2 코호트 · CLI 회계')
def t_rc():
    coh = _cohort_manifests()
    chk('R1 봉인 p2 코호트 32 팔 — 새 함수 재계산 = 저장값 32/32',
        len(coh) == 32 and all(RC.physics_protocol_id(m) == m['physics_protocol_id'] for m in coh), len(coh))
    m = fa_manifest()
    pid = m['physics_protocol_id']
    chk('R2 face_alpha + 블록 = p3ca- + 16 hex', pid.startswith(RC.CA_EXT_PREFIX + '-') and len(pid) == len('p3ca-') + 16, pid)
    chk('R3 protocol_ok (저장 = 재계산)', RC.protocol_ok(m) == (True, None), RC.protocol_ok(m))
    m_nob = {k: v for k, v in m.items() if k != 'ca_ext'}
    chk('R4 기능 켬 · 블록 없음 → unknown:ca_ext', RC.physics_protocol_id(m_nob) == RC.CA_EXT_UNKNOWN,
        RC.physics_protocol_id(m_nob))
    m_off = dict(m, ptfe_stamp='off')
    chk('R5 블록 있는데 ptfe_stamp off → unknown:ca_ext', RC.physics_protocol_id(m_off) == RC.CA_EXT_UNKNOWN)
    for nm, blk in (('모르는 하위 블록', dict(m['ca_ext'], mystery={'protocol': {}, 'evidence': {}})),
                    ('schema 다름', dict(m['ca_ext'], schema='ca-ext-v0')), ('빈 블록', {'schema': RC.CA_EXT_SCHEMA}),
                    ('protocol 없음', {'schema': RC.CA_EXT_SCHEMA, 'ptfe_face': {'evidence': {}}}), ('None', None)):
        chk(f'R6 블록 모양 틀림 [{nm}] → unknown:ca_ext', RC.physics_protocol_id(dict(m, ca_ext=blk)) == RC.CA_EXT_UNKNOWN)
    m_ev = json.loads(json.dumps(m))
    m_ev['ca_ext']['ptfe_face']['evidence']['receipts']['electronic_main']['n_rows_used'] = 9
    chk('R7 증거만 바뀜 → id 같음', RC.physics_protocol_id(m_ev) == pid)
    chk('R8 물리 칸 바뀜 (두 집단 지름) → id 다름', RC.physics_protocol_id(fa_manifest(dia_law='two_pop')) != pid)
    chk('R8b 채널 바뀜 → id 다름', RC.physics_protocol_id(fa_manifest(channels=('electronic',))) != pid)
    m_miss = {k: v for k, v in m.items() if k != 'vox_um'}
    chk('R9 p2 축 결손이 먼저 (unknown:vox_um 그대로)', RC.physics_protocol_id(m_miss) == 'unknown:vox_um',
        RC.physics_protocol_id(m_miss))
    chk('R10 관찰 세대 (p3ca = 현행) · 낮춘 신고 거부', RC.observed_generation(m) == RC.SCHEMA_VERSION
        and RC.schema_of(dict(m, schema_version=2))[0] is None)
    chk('R11 ptfe_record_ok — face_alpha · 관측 0 = 통과', RC.ptfe_record_ok(m) == (True, None), RC.ptfe_record_ok(m))
    chk('R12 ptfe_record_ok — face_alpha · 관측 3 = 거부 (도장 ≠ 실물)', not RC.ptfe_record_ok(dict(m, ptfe_cells_observed=3))[0])
    chk('R13 ca_ext_record_ok 정상 · 끈 매니페스트 (블록 없음) 통과', RC.ca_ext_record_ok(m) == (True, None)
        and RC.ca_ext_record_ok(coh[0]) == (True, None), RC.ca_ext_record_ok(m))

    def mut(fn):
        x = json.loads(json.dumps(m))
        fn(x)
        return RC.ca_ext_record_ok(x)[0]
    E = lambda x: x['ca_ext']['ptfe_face']['evidence']          # noqa: E731
    Pp = lambda x: x['ca_ext']['ptfe_face']['protocol']         # noqa: E731
    bad = {
        '블록 없음 (기능 켬)': lambda x: x.pop('ca_ext'),
        '영수증 키 빠짐': lambda x: E(x)['receipts'].pop('ionic'),
        'applied 인데 행 0': lambda x: E(x)['receipts']['electronic_main'].update(n_rows_used=0),
        '모르는 상태': lambda x: E(x)['receipts']['electronic_main'].update(status='mystery'),
        'missing 상태': lambda x: E(x)['receipts']['electronic_main'].update(status='missing'),
        '이온 요청인데 not_requested': lambda x: E(x)['receipts'].update(ionic={'status': 'not_requested'}),
        '주 전자 솔브 disabled': lambda x: E(x)['receipts'].update(electronic_main={'status': 'disabled', 'why': 'x'}),
        '집전체 계획 켬 (v0 = LEAN 2·3 만)': lambda x: x['component_plan'].update(collector=True),
        '필드 요청 (LEAN 4 거부)': lambda x: x.update(field_requested=True),
        'K 다름': lambda x: Pp(x).update(K=16),
        '판 이름 다름': lambda x: Pp(x).update(operator='s1-face-alpha-v0'),
        '지름 법칙 · 값 불일치': lambda x: Pp(x).update(dia_um={'rope': 0.25}),
        '모르는 채널': lambda x: Pp(x).update(channels=['electronic', 'thermal']),
        '부피 상태 거짓': lambda x: E(x)['volume'].update(status='in_band'),
        '관측 PTFE 셀 > 0': lambda x: x.update(ptfe_cells_observed=4),
        '진단 상태 빠짐': lambda x: E(x).pop('diagnostics'),
        '계획 지문 ↔ 영수증 불일치': lambda x: E(x)['receipts']['electronic_main'].update(fp_plan='f' * 32),
        'ptfe_stamp off 인데 블록': lambda x: x.update(ptfe_stamp='off'),
        #  소비자 쪽 조합 거부 = producer 거부의 짝 (payload 를 거치지 않은 매니페스트도 같은 판정)
        'σ_PTFE > 0': lambda x: x.update(sigma_ptfe_S_cm=0.5),
        'PTFE 차단 두께 > 0': lambda x: x.update(ptfe_block_um=0.2),
        'PTFE 차단 범위 ion (두께 0)': lambda x: x.update(ptfe_block_scope='ion'),
        '주기 xy': lambda x: x.update(periodic_xy=True),
        '계면 표 (r1) 동시': lambda x: x.update(interface_model='r1'),
    }
    for nm, fn in bad.items():
        chk(f'R14 ca_ext_record_ok 거부 [{nm}]', not mut(fn))
    m_noop = fa_manifest(channels=('ionic',), ionic_plan=False)
    chk('R14b ca_ext_record_ok 거부 [이온만 요청 + 이온 솔브 끔 = 어디에도 안 걸림 (조용한 no-op)]',
        not RC.ca_ext_record_ok(m_noop)[0], RC.ca_ext_record_ok(m_noop))
    chk('R14c 전자만 요청 + 이온 솔브 끔 = 정상 (전자 주 솔브가 적용)',
        RC.ca_ext_record_ok(fa_manifest(channels=('electronic',), ionic_plan=False)) == (True, None),
        RC.ca_ext_record_ok(fa_manifest(channels=('electronic',), ionic_plan=False)))
    acct = RC.CLI_ACCOUNTING
    chk('R15 CLI 회계 — 새 플래그 = protocol_ext (ca_ext 칸 이름)', 'protocol_ext' in RC.CLI_CATEGORIES
        and acct.get('--step3-face-alpha-channel', (None,))[0] == 'protocol_ext'
        and acct.get('--step3-face-alpha-dia-law', (None,))[0] == 'protocol_ext')
    import check_method_discipline as CMD
    probs, _w = quiet(CMD.check_cli_accounting, verbose=False)
    chk('R16 규칙 M (실물 파서 전수) 문제 0', probs == [], probs[:3])


# ═════════════════════════ P 묶음 — payload 끝-끝 ═════════════════════════
UM_BOX = 1000.0 / ((0.96 - 0.04) / 0.05)
SW0, FLOOR = 0.04, 0.05


def _box(P_um):
    P = np.asarray(P_um, np.float64)
    return np.column_stack([SW0 + P[:, 0] / UM_BOX, SW0 + P[:, 1] / UM_BOX, FLOOR + P[:, 2] / UM_BOX])


def make_payload_fixture(d, with_ptfe=True):
    """2×2 AM 기둥 (구 셋씩 · r 4 µm) + 조밀 SE 점 + 짧은 VGCF + PTFE 중심선 둘 (pid 경계 면 위 — 목을 가로지른다)."""
    rows = ['# type,x,y,z,r  (S1 face_alpha 시험 픽스처)']
    for ix in range(2):
        for iy in range(2):
            for k in range(3):
                rows.append('2,%.6f,%.6f,%.6f,%.6f' % (0.020 + 0.008 * ix, 0.020 + 0.008 * iy, 0.004 + 0.0075 * k, 0.004))
    am = os.path.join(d, 'am.csv')
    with open(am, 'w', encoding='utf-8') as f:
        f.write('\n'.join(rows) + '\n')
    g = np.arange(12.0, 36.01, 0.75)
    gz = np.arange(0.3, 23.2, 0.75)
    se = np.array([[x, y, z] for x in g for y in g for z in gz], np.float64)
    blocks = [(_box(se), 1, -1, 0)]
    blocks.append((_box(line((18.0, 24.0, 18.0), (30.0, 24.0, 18.0), 49)), 2, 0, 1))
    if with_ptfe:
        blocks.append((_box(line((12.0, 20.0, 7.0), (36.0, 20.0, 7.0), 121)), 4, 1, 1))
        blocks.append((_box(line((28.0, 12.0, 14.0), (28.0, 36.0, 14.0), 121)), 4, 2, 1))
    pts = np.vstack([b[0] for b in blocks])
    ph = np.concatenate([np.full(len(b[0]), b[1], np.int32) for b in blocks])
    fid = np.concatenate([np.full(len(b[0]), b[2], np.int32) for b in blocks])
    kind = np.concatenate([np.full(len(b[0]), b[3], np.int8) for b in blocks])
    np.save(os.path.join(d, 'se.npy'), pts)
    np.save(os.path.join(d, 'phase.npy'), ph)
    np.save(os.path.join(d, 'fibre.npy'), fid)
    np.save(os.path.join(d, 'fibre_kind.npy'), kind)
    np.save(os.path.join(d, 'fibre_dia.npy'), np.ones(len(pts)))
    return d


LEAN2 = ['--no-step4', '--no-thermal', '--no-trackb', '--no-field', '--no-ion', '--no-pore', '--no-collector']
LEAN3 = [x for x in LEAN2 if x != '--no-ion']


def run_payload(d, extra, out='p.json', payload=None, drop=()):
    """`drop` = 기본 인자에서 뺄 플래그 (값과 함께 — 예: ('--phase',))."""
    pay = payload or os.path.join(SCRIPTS, 'mpm_webapp_payload.py')
    base = ['--scaffold', 'am.csv', '--se', 'se.npy', '--phase', 'phase.npy', '--fibre', 'fibre.npy',
            '--fibre-dia', 'fibre_dia.npy', '--n-vox', '24', '--step3-vox', '1.0', '--step3-fibre-stamp', 'segment']
    for fl in drop:
        i = base.index(fl)
        del base[i:i + 2]
    cmd = [sys.executable, pay, *base, '--out', out, '--show-results', *extra]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=900, cwd=d, stdin=subprocess.DEVNULL)
    log = (r.stdout or '') + (r.stderr or '')
    data = None
    if os.path.exists(os.path.join(d, out)):
        try:
            data = json.load(open(os.path.join(d, out), encoding='utf-8'))
        except Exception:                                  # noqa: BLE001
            data = None
    return r.returncode, log, data


def s3_of(data):
    return ((data or {}).get('mpm_metrics') or {}).get('step3') or {}


@case('P payload 끝-끝 — face_alpha 세 분기 · 거부 조합 · 매니페스트 · sid = off 격자 · 채널 독립')
def t_payload():
    if ARGS.skip_payload:
        print('    (--skip-payload — 건너뜀)')
        return
    td = tempfile.mkdtemp(prefix='s1fa_')
    try:
        os.makedirs(os.path.join(td, 'with'))
        os.makedirs(os.path.join(td, 'none'))
        d = make_payload_fixture(os.path.join(td, 'with'), True)
        dn = make_payload_fixture(os.path.join(td, 'none'), False)
        FAL = ['--ptfe-stamp', 'face_alpha']
        refuse = {
            'SEGMENT (점 스탬프)': (FAL + LEAN2, ['--step3-fibre-stamp', 'point']),
            'SIGMA_PTFE': (FAL + LEAN2 + ['--sigma-ptfe', '0.5'], None),
            'PTFE_BLOCK': (FAL + LEAN2 + ['--step3-ptfe-block-um', '0.2'], None),
            #  ★ PTFE_BLOCK_* 의 둘째 손잡이 — 범위만 바꿔도 (두께 0) 차단할 PTFE 셀이 없어 조용한 no-op
            'PTFE_BLOCK (범위 ion · 두께 0)': (FAL + LEAN2 + ['--step3-ptfe-block-scope', 'ion'], None),
            'PERIODIC': (FAL + LEAN2 + ['--periodic'], None),
            'FIELD (LEAN 4)': (FAL + [x for x in LEAN2 if x != '--no-field'], None),
            'COLLECTOR': (FAL + [x for x in LEAN2 if x != '--no-collector'], None),
            'THERMAL': (FAL + [x for x in LEAN2 if x != '--no-thermal'], None),
            'PORE': (FAL + [x for x in LEAN2 if x != '--no-pore'], None),
            'STEP4': (FAL + [x for x in LEAN2 if x != '--no-step4'], None),
            'TRACKB': (FAL + [x for x in LEAN2 if x != '--no-trackb'], None),
            'JOULE': (FAL + LEAN2 + ['--joule-heat'], None),
            'STEP4_GRID': (FAL + LEAN2 + ['--save-step4-grid', 'g.npz'], None),
            'RINT': (FAL + LEAN2 + ['--step3-rint-e', 'AM_S|VGCF=1e-3'], None),
            'NO_STEP3': (FAL + LEAN2 + ['--no-step3'], None),
            #  이온만 요청 + --no-ion (LEAN 2) = 계획이 어느 솔브에도 안 걸린다 (조용한 no-op)
            'NOOP_CHANNEL (이온만 + --no-ion)': (FAL + LEAN2 + ['--step3-face-alpha-channel', 'ionic'], None),
            '채널 플래그만 (face_alpha 아님)': (['--ptfe-stamp', 'off'] + LEAN2 + ['--step3-face-alpha-channel', 'ionic'], None),
            '지름 법칙 플래그만 (face_alpha 아님)': (['--ptfe-stamp', 'off'] + LEAN2 + ['--step3-face-alpha-dia-law', 'rope'],
                                         None),
        }
        for i_r, (nm, (extra, override)) in enumerate(refuse.items()):
            ex = list(extra)
            if override:
                ex += override
            rc, log, _d = run_payload(d, ex, out=f'refuse_{i_r}.json')
            chk(f'P-거부 [{nm}] → rc ≠ 0 · 표지 S1_FACE_ALPHA_REFUSED', rc != 0 and 'S1_FACE_ALPHA_REFUSED' in log,
                (rc, log.strip()[-160:]))
        rc, log, _d = run_payload(d, FAL + LEAN2, out='refuse_nophase.json', drop=('--phase',))
        chk('P-거부 [NO_PHASE (--phase 없음)] → rc ≠ 0 · 표지 S1_FACE_ALPHA_REFUSED|NO_PHASE',
            rc != 0 and 'S1_FACE_ALPHA_REFUSED|NO_PHASE' in log, (rc, log.strip()[-160:]))
        rc_o, log_o, p_off = run_payload(d, ['--ptfe-stamp', 'off'] + LEAN2, out='off.json')
        rc_c, log_c, p_cl = run_payload(d, ['--ptfe-stamp', 'centerline'] + LEAN2, out='cl.json')
        rc_f, log_f, p_fa = run_payload(d, FAL + LEAN2, out='fa.json')
        mo, mc, mf = (s3_of(p).get('manifest') or {} for p in (p_off, p_cl, p_fa))
        chk('P1 off LEAN 2 — rc 0 · 블록 없음 · p2 id · PTFE 셀 0', rc_o == 0 and 'ca_ext' not in mo
            and str(mo.get('physics_protocol_id', '')).startswith('p2-') and mo.get('ptfe_cells_observed') == 0,
            (rc_o, log_o.strip()[-200:]))
        chk('P2 centerline — PTFE 셀 > 0 · exact-zero DOF · p2 id', rc_c == 0 and (mc.get('ptfe_cells_observed') or 0) > 0
            and mc.get('ptfe_zero_dof') is True and str(mc.get('physics_protocol_id', '')).startswith('p2-'),
            (rc_c, mc.get('ptfe_cells_observed')))
        chk('P3 face_alpha LEAN 2 — rc 0', rc_f == 0, log_f.strip()[-400:])
        ca = (mf.get('ca_ext') or {})
        pf = (ca.get('ptfe_face') or {})
        ev = pf.get('evidence') or {}
        rcp = ev.get('receipts') or {}
        chk('P4 매니페스트 — 도장 face_alpha · PTFE 셀 0 · zero_dof False · 블록 · p3ca id · protocol_ok · ca_ext_record_ok',
            mf.get('ptfe_stamp') == 'face_alpha' and mf.get('ptfe_cells_observed') == 0 and mf.get('ptfe_zero_dof') is False
            and ca.get('schema') == RC.CA_EXT_SCHEMA and str(mf.get('physics_protocol_id', '')).startswith('p3ca-')
            and RC.protocol_ok(mf) == (True, None) and RC.ca_ext_record_ok(mf) == (True, None),
            (mf.get('physics_protocol_id'), RC.ca_ext_record_ok(mf) if mf else None))
        chk('P5 영수증 (LEAN 2) — 주 applied · wetted/bare disabled · 이온 disabled',
            (rcp.get('electronic_main') or {}).get('status') == 'applied'
            and (rcp.get('electronic_wetted') or {}).get('status') == 'disabled'
            and (rcp.get('electronic_bare') or {}).get('status') == 'disabled'
            and (rcp.get('ionic') or {}).get('status') == 'disabled', rcp)
        so, sf = s3_of(p_off), s3_of(p_fa)
        chk('P6 σ_e(face_alpha) < σ_e(off) — 목 면이 막힌다', 0 < (sf.get('sigma_e_eff_S_cm') or 0) < (so.get('sigma_e_eff_S_cm') or 0),
            (so.get('sigma_e_eff_S_cm'), sf.get('sigma_e_eff_S_cm')))
        chk('P7 진단 미계산 (E2 · v0) — 소산 분담 None · je 없음 · 상태 기록',
            sf.get('dissipation_share') is None and all('je' not in q for q in (p_fa or {}).get('particles', [{}]))
            and (ev.get('diagnostics') or {}).get('je') == 'not_computed', ev.get('diagnostics'))
        chk('P8 캡슐 증거 — 경로 2 · 참부피 없음 = unknown · 표지 문자열', (ev.get('capsules') or {}).get('n_paths') == 2
            and (ev.get('volume') or {}).get('status') == 'unknown_true_volume' and ev.get('label') == FA.LABEL, ev.get('capsules'))
        chk('P9 check_arm (sr01) 이 실제 산출물을 받는다', subprocess.run(
            [sys.executable, os.path.join(SCRIPTS, 'sr01_stamp_compare.py'), '--check-arm', os.path.join(d, 'fa.json'),
             '--stamp', 'segment'], capture_output=True, text=True, timeout=300, cwd=d).returncode == 0)
        #  sid 격자 = off 격자 (raster-only 원장)
        rc_ro, _l1, _ = run_payload(d, ['--ptfe-stamp', 'off', '--step3-rasterize-only', 'r_off.json'] + LEAN2, out='x1.json')
        rc_rf, _l2, _ = run_payload(d, FAL + ['--step3-rasterize-only', 'r_fa.json'] + LEAN2, out='x2.json')
        led_o = json.load(open(os.path.join(d, 'r_off.json'))) if os.path.exists(os.path.join(d, 'r_off.json')) else {}
        led_f = json.load(open(os.path.join(d, 'r_fa.json'))) if os.path.exists(os.path.join(d, 'r_fa.json')) else {}
        chk('P10 face_alpha 의 sid 격자 = off 격자 (셀 수 상별 같음 · sid 7 없음)', rc_ro == 0 and rc_rf == 0
            and led_o.get('cells_by_sid') == led_f.get('cells_by_sid') and '7' not in (led_f.get('cells_by_sid') or {'7': 1}),
            (led_o.get('cells_by_sid'), led_f.get('cells_by_sid')))
        #  PTFE 없는 침대 — no-op
        rc_no, _l3, p_no = run_payload(dn, ['--ptfe-stamp', 'off'] + LEAN2, out='off.json')
        rc_nf, _l4, p_nf = run_payload(dn, FAL + LEAN2, out='fa.json')
        en = ((s3_of(p_nf).get('manifest') or {}).get('ca_ext') or {}).get('ptfe_face', {}).get('evidence', {})
        chk('P11 PTFE 없음 — σ_e 비트 같음 · 주 영수증 absent_geometry', rc_no == 0 and rc_nf == 0
            and s3_of(p_no).get('sigma_e_eff_S_cm') == s3_of(p_nf).get('sigma_e_eff_S_cm')
            and (en.get('receipts') or {}).get('electronic_main', {}).get('status') == 'absent_geometry',
            (s3_of(p_no).get('sigma_e_eff_S_cm'), s3_of(p_nf).get('sigma_e_eff_S_cm')))
        #  LEAN 3 — 채널 독립 (F13 생산 경로)
        _r1, _ll1, q_off = run_payload(d, ['--ptfe-stamp', 'off'] + LEAN3, out='l3_off.json')
        _r2, _ll2, q_e = run_payload(d, FAL + LEAN3 + ['--step3-face-alpha-channel', 'electronic'], out='l3_e.json')
        _r3, _ll3, q_i = run_payload(d, FAL + LEAN3 + ['--step3-face-alpha-channel', 'ionic'], out='l3_i.json')
        _r4, _ll4, q_b = run_payload(d, FAL + LEAN3, out='l3_b.json')
        so3, se3, si3, sb3 = (s3_of(q) for q in (q_off, q_e, q_i, q_b))
        chk('P12 전자만 — σ_ion = off 비트 같음 · σ_e 감소 · 이온 영수증 not_requested',
            _r2 == 0 and se3.get('sigma_ion_eff_S_cm') == so3.get('sigma_ion_eff_S_cm')
            and (se3.get('sigma_e_eff_S_cm') or 0) < (so3.get('sigma_e_eff_S_cm') or 0)
            and ((se3.get('manifest') or {}).get('ca_ext') or {}).get('ptfe_face', {}).get('evidence', {})
            .get('receipts', {}).get('ionic', {}).get('status') == 'not_requested', (_r2, _ll2.strip()[-200:]))
        chk('P13 이온만 — σ_e = off 비트 같음 · σ_ion 감소', _r3 == 0 and si3.get('sigma_e_eff_S_cm') == so3.get('sigma_e_eff_S_cm')
            and (si3.get('sigma_ion_eff_S_cm') or 0) < (so3.get('sigma_ion_eff_S_cm') or 0),
            (si3.get('sigma_ion_eff_S_cm'), so3.get('sigma_ion_eff_S_cm')))
        rb = ((sb3.get('manifest') or {}).get('ca_ext') or {}).get('ptfe_face', {}).get('evidence', {}).get('receipts', {})
        chk('P14 둘 다 (LEAN 3) — 이온 영수증 applied · 이온 소산 분담 None · ca_ext_record_ok',
            _r4 == 0 and (rb.get('ionic') or {}).get('status') == 'applied' and sb3.get('ion_dissipation_share') is None
            and RC.ca_ext_record_ok(sb3.get('manifest') or {}) == (True, None), (_r4, rb))
        print(f"    보고 P (픽스처 · vox 1.0) σ_e off {so.get('sigma_e_eff_S_cm')!r} → face_alpha {sf.get('sigma_e_eff_S_cm')!r} · "
              f"LEAN 3 σ_ion off {so3.get('sigma_ion_eff_S_cm')!r} → 이온만 {si3.get('sigma_ion_eff_S_cm')!r} · "
              f"전자 행 {((ev.get('faces') or {}).get('electronic') or {}).get('n_rows')} · 캡슐 {ev.get('capsules')} · "
              f"off 격자 PTFE 점 셀 {ev.get('off_grid_ptfe_point_cells')}")
        rc_t = subprocess.run([sys.executable, os.path.join(SCRIPTS, 'mpm_webapp_payload.py'), '--selftest-temperature'],
                              capture_output=True, text=True, timeout=300, cwd=td)
        chk('P15 payload --selftest-temperature (PTFE 규약 문자열 검사 포함) rc 0', rc_t.returncode == 0,
            ((rc_t.stdout or '') + (rc_t.stderr or '')).strip()[-300:])
    finally:
        shutil.rmtree(td, ignore_errors=True)


# ═════════════════════════ B 묶음 — 끔 비트 동일 (고치기 전 코드 대조) ═════════════════════════
@case('B 끔 비트 동일 — 고치기 전 step3_sigma · payload 와 대조 (--old-scripts)')
def t_bitid():
    if not ARGS.old_scripts:
        print('    (--old-scripts 없음 — 건너뜀 · 커밋 증거는 그 인자로 돌린 기록)')
        return
    spec = importlib.util.spec_from_file_location('step3_sigma_old', os.path.join(ARGS.old_scripts, 'step3_sigma.py'))
    OLD = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(OLD)
    fixtures = [('ion rand', rand_ion_grid((4, 3, 5), 7), ti, None), ('ion rand2', rand_ion_grid((3, 4, 6), 9), ti, None)]
    _h, s13, p13, _c = _f13_fixture()
    fixtures.append(('mixed e', s13, te, p13))
    am = np.full((2, 2, 4), 2, np.int8)
    fixtures.append(('AM block', am, te, np.zeros(am.shape, np.int32)))
    from scipy.sparse.linalg import spsolve
    for nm, sid, tab, pid in fixtures:
        for how in ('직접', 'CG'):
            outs = []
            for mod in (OLD, S3):
                o = mod._solve_cg
                if how == '직접':
                    mod._solve_cg = lambda L, b: (spsolve(L.tocsc(), b), 0)
                try:
                    outs.append(quiet(mod.solve_sigma_z, sid, tab(), H, return_field=True, z_top_um=sid.shape[2] * H,
                                      z_bot_um=0.0, pid=pid))
                finally:
                    mod._solve_cg = o
            chk(f'B1 솔버 끔 [{nm} · {how}] — σ · n_dof · φ 비트 같음 (옛 ↔ 새)', same_solve(outs[0], outs[1])
                and outs[0].get('resid') == outs[1].get('resid') and sorted(outs[0]) == sorted(outs[1]),
                (outs[0]['sigma_eff'], outs[1]['sigma_eff']))
    if ARGS.skip_payload:
        return
    td = tempfile.mkdtemp(prefix='s1fa_b_')
    try:
        os.makedirs(os.path.join(td, 'w'))
        d = make_payload_fixture(os.path.join(td, 'w'), True)
        for nm, extra in (('off', ['--ptfe-stamp', 'off'] + LEAN2), ('centerline', ['--ptfe-stamp', 'centerline'] + LEAN2),
                          ('off LEAN3', ['--ptfe-stamp', 'off'] + LEAN3)):
            r_old = run_payload(d, extra, out=f'old_{nm}.json', payload=os.path.join(ARGS.old_scripts, 'mpm_webapp_payload.py'))
            r_new = run_payload(d, extra, out=f'new_{nm}.json')
            m_old = dict(s3_of(r_old[2]).get('manifest') or {})
            m_new = dict(s3_of(r_new[2]).get('manifest') or {})
            for k in ('code_sha', 'exec_env'):
                m_old.pop(k, None)
                m_new.pop(k, None)
            s_old = {k: v for k, v in s3_of(r_old[2]).items() if k != 'manifest'}
            s_new = {k: v for k, v in s3_of(r_new[2]).items() if k != 'manifest'}
            diff = sorted(k for k in set(m_old) | set(m_new) if m_old.get(k) != m_new.get(k))
            chk(f'B2 payload [{nm}] — 매니페스트 (code_sha · exec_env 빼고) 바이트 같음 · id 같음 · step3 값 같음',
                r_old[0] == 0 and r_new[0] == 0 and json.dumps(m_old, sort_keys=True) == json.dumps(m_new, sort_keys=True)
                and s_old == s_new, (r_old[0], r_new[0], diff[:6]))
    finally:
        shutil.rmtree(td, ignore_errors=True)


def main():
    global S3, FA, RC, ARGS
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--s3', default=os.path.join(SCRIPTS, 'step3_sigma.py'))
    ap.add_argument('--old-scripts', default='', help='고치기 전 scripts/ 사본 (B 묶음 · 끔 비트 동일 대조)')
    ap.add_argument('--skip-payload', action='store_true')
    ap.add_argument('--only', default='', help='쉼표로 나눈 이름 접두 (예: F16,C)')
    ARGS = ap.parse_args()
    spec = importlib.util.spec_from_file_location('step3_sigma_under_test', os.path.abspath(ARGS.s3))
    S3 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(S3)
    print(f'step3_sigma = {os.path.abspath(ARGS.s3)}')
    try:
        import ptfe_face_alpha as _fa
        FA = _fa
    except Exception as e:                                  # noqa: BLE001 — 구현 전 (모듈 없음) 도 시험 단위로 기록
        print(f'  ⚠ ptfe_face_alpha 를 못 불러온다 ({type(e).__name__}: {e})')
    import run_contract as _rc
    RC = _rc
    only = [x.strip() for x in ARGS.only.split(',') if x.strip()]
    for tag, fn in CASES:
        if only and not any(tag.startswith(o) for o in only):
            continue
        print(f'\n── {tag}')
        try:
            fn()
        except Exception as e:                              # noqa: BLE001 — 옛 코드 (API 없음) 도 시험 단위로 기록
            chk(f'{tag.split()[0]}: 실행', False, f'{type(e).__name__}: {e}')
    print(f'\n{_ok} PASS · {len(_fail)} FAIL')
    if _fail:
        for n in _fail:
            print('  -', n)
        sys.exit(1)


if __name__ == '__main__':
    main()
