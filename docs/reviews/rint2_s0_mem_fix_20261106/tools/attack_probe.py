#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""사전 공격 탐침 (2026-11-06 · `SELF-155` 고침) — 새 후보 검색의 칼날 입력에서 상위집합 · 정준 순서를 brute force 로 본다.

꼴 다섯: 퇴화 선분만 (점 300) · 같은 선분 두 번 (공유) · 큰 좌표 (1e6 µm 이동 · 긴 선분 섞임) · 길이 비 1e5 · 중점이 모두 같은 선분 60.
`_near_seg_pairs` = L0 (기본 · D/7 · 1.0) × 질의 덩어리 (1 · 13 · 기본) · `_ball_seg_candidates` = 점 200 (반지름 0–0.6 무작위).

  python3 docs/reviews/rint2_s0_mem_fix_20261106/tools/attack_probe.py
"""
import os
import sys

import numpy as np

W = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, W + '/scripts')
import carbon_junction as CJ  # noqa: E402
import ca_s0_census as S0     # noqa: E402


def truth(P0, P1, D):
    n = len(P0)
    if n < 2:
        return set()
    I, J = np.triu_indices(n, 1)
    d1 = CJ.seg_seg_closest(P0[I], P1[I], P0[J], P1[J])[0]
    d2 = CJ.seg_seg_closest(P0[J], P1[J], P0[I], P1[I])[0]
    m = (d1 <= D) | (d2 <= D)
    return set(zip(I[m].tolist(), J[m].tolist()))


def ball_truth(X, rq, P0, P1):
    out = set()
    for q in range(len(X)):
        d2 = S0._pt_seg_d2(np.repeat(X[q][None], len(P0), 0), P0, P1)
        for s in np.flatnonzero(np.sqrt(d2) <= rq[q]):
            out.add((q, int(s)))
    return out


rng = np.random.default_rng(5)
cases = []
P = rng.uniform(0, 2, (300, 3))
cases.append(('퇴화 선분만 (점 300)', P, P.copy(), 0.2))
A0 = rng.uniform(0, 2, (100, 3)); A1 = A0 + rng.normal(size=(100, 3)) * 0.05
cases.append(('같은 선분 두 번 (공유)', np.vstack([A0, A0]), np.vstack([A1, A1]), 0.2))
off = np.array([1.0e6, -2.0e6, 3.0e5])
B0 = rng.uniform(0, 3, (400, 3)); B1 = B0 + rng.normal(size=(400, 3)) * 0.08
B0[:3] = [[0, 0, 0], [0.5, 0.5, 0.5], [1, 1, 1]]; B1[:3] = [[2.9, 2.9, 2.9], [0.5, 2.5, 0.5], [1, 1, 2.9]]
cases.append(('큰 좌표 (1e6 µm 이동 · 긴 선분 섞임)', B0 + off, B1 + off, 0.2))
C0 = rng.uniform(0, 3, (500, 3)); C1 = C0 + rng.normal(size=(500, 3)) * 1e-4
C0[0] = [0.0, 0.0, 0.0]; C1[0] = [3.0, 3.0, 3.0]
cases.append(('길이 비 1e5 (짧은 선분 499 + 대각선 하나)', C0, C1, 0.2))
M = np.repeat(np.array([[1.0, 1.0, 1.0]]), 60, 0)
dirs = rng.normal(size=(60, 3)); dirs /= np.linalg.norm(dirs, axis=1)[:, None]
cases.append(('중점이 모두 같은 선분 60', M - 0.3 * dirs, M + 0.3 * dirs, 0.2))
bad = 0
for nm, P0, P1, D in cases:
    t = truth(P0, P1, D)
    for L0 in (None, D / 7.0, 1.0):
        for bud in (1, 13, None):
            old = CJ._PAIR_ENTRY_BUDGET
            if bud is not None:
                CJ._PAIR_ENTRY_BUDGET = bud
            try:
                pr = CJ._near_seg_pairs(P0, P1, D, L0=L0)
            finally:
                CJ._PAIR_ENTRY_BUDGET = old
            s = set(map(tuple, pr.tolist()))
            ok = (t <= s) and (bool(np.all(pr[:, 0] < pr[:, 1])) if len(pr) else True)
            if not ok:
                bad += 1
                print('FAIL', nm, L0, bud, len(t - s))
    print(f'{nm}: 참 쌍 {len(t)} · 후보 (기본) {len(CJ._near_seg_pairs(P0, P1, D))}')
X = rng.uniform(0, 3, (200, 3))
rq = rng.uniform(0.0, 0.6, 200)
for nm, P0, P1, D in cases[:2] + cases[3:]:
    t = ball_truth(X, rq, P0, P1)
    q, sgs = CJ._ball_seg_candidates(X, rq, P0, P1)
    s = set(zip(q.tolist(), sgs.tolist()))
    key = q * len(P0) + sgs
    canon = bool(np.all(np.diff(key) > 0))
    print(f'공 {nm}: 참 {len(t)} · 후보 {len(s)} · 상위집합 {t <= s} · 정준 {canon}')
    bad += 0 if (t <= s and canon) else 1
Xo = X + off                                                  # 큰 좌표의 공 검색
t = ball_truth(Xo, rq, cases[2][1], cases[2][2])
q, sgs = CJ._ball_seg_candidates(Xo, rq, cases[2][1], cases[2][2])
s = set(zip(q.tolist(), sgs.tolist()))
print(f'공 큰 좌표 (1e6 µm 이동): 참 {len(t)} · 후보 {len(s)} · 상위집합 {t <= s}')
bad += 0 if t <= s else 1
print('bad', bad)
sys.exit(1 if bad else 0)
