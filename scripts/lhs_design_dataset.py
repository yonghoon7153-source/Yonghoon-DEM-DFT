#!/usr/bin/env python3
"""AI 학습용 DEM 데이터셋 **설계** — 5 노브 LHS (2026-08-18 지시).

설계인자 (사용자 지정 범위)                 디스크립터 (DEM 이 낼 것)
  대립 AM_P 5–15 µm                          porosity
  소립 AM_S 1–5 µm                           coverage (대립 / 소립 / 전체)
  바이모달 비율 0–100 %                      tortuosity
  전해질 SE 0.5–2 µm
  활물질 함량 70–95 wt%

★★ **크기는 직경(diameter)으로 해석했다.**  근거 — 리포는 두 규약을 다 쓴다:
   `r_AM_P/r_AM_S/r_SE` = **반경** (LIGGGHTS 입력, `docs/data/dem_design_points.csv`)
   `d_am/d_se`          = **직경** (ML 설계층, `docs/data/design_performance_corpus.csv`)
   실측 대조로 확인: d_am 4/5/10/12 = 2 × r_AM 2/2.5/5/6 · d_se 0.5/1/2/3 = 2 × r_SE 0.25/0.5/1/1.5.
   지시된 범위(대립 5–15 · 소립 1–5 · SE 0.5–2)는 **직경**으로 읽을 때 실물성과 맞고
   (poly NCM D50 8–15 · single-crystal 2–5 · 밀링 LPSCl 0.5–2), 두 AM 범위가 **겹치지 않아**
   d_AM_P ≥ d_AM_S 가 구성상 보장된다 (반경으로 읽으면 대립이 Ø10–30 µm 로 비현실적).
   ⇒ 반경 컬럼(`r_*_um`)을 **함께** 내보내므로 어느 쪽이든 그대로 쓸 수 있다.
   ⚠ 지시가 반경이었다면 크기 3열을 2배 하면 된다 (`--as-radius`).

★ 왜 세 블록인가 (분기 설계): ps_frac = 0 이면 AM_P 가 **없어서** d_AM_P 가 식별 불가능하고,
  ps_frac = 1 이면 d_AM_S 가 그렇다.  한 LHS 에 섞으면 그 행들이 **없는 인자에 좌표를 배정**해
  설계행렬을 오염시킨다.  ⇒ 내부(양상 존재) 5-인자 LHS + 두 단일모달 끝점 3-인자 LHS 로 가른다.

사용:
  python3 scripts/lhs_design_dataset.py --n 60 --n-end 10 --out docs/data/lhs_design_20260818.csv
  python3 scripts/lhs_design_dataset.py --selftest
"""
from __future__ import annotations

import argparse
import ast
import collections
import csv
import hashlib
import json
import math
import pathlib
import re
import sys

import numpy as np

#  범위 = 사용자 지정 (2026-08-18).  직경 µm / wt% / 무차원.
RANGES = {
    'd_am_p_um': (5.0, 15.0),      # 대립 (poly NCM 2차입자)
    'd_am_s_um': (1.0, 5.0),       # 소립 (single-crystal)
    'ps_frac':   (0.0, 1.0),       # 바이모달 비율 = AM_P 몫 (0 = 소립만, 1 = 대립만)
    #  ★★ 2026-08-18 — 하한을 0.5 → **1.0** 으로 올렸다 (지시: 입자 20만 이하).
    #    이유는 계산이 아니라 **측정**이다.  덱 실측(input_real_1)으로 규약이 확정된 뒤
    #    격자 11,880 조합의 N_total 을 전수 계산해 보니:
    #        d_se 0.5 → N 100,625 – 908,115   20만 이하 **16.7 %**
    #        d_se 1.0 → N  12,671 – 191,918   20만 이하 **100 %**   ← 딱 경계
    #        d_se 1.5 → N   3,829 – 119,919   100 %
    #        d_se 2.0 → N   1,677 – 102,393   100 %
    #    ★ 그리고 제약이 **d_se 에만** 걸린다 — 나머지 네 인자는 수준별 생존률이
    #      79 % 로 **완전히 균일**하다 ⇒ d_se 하한만 올리면 다른 축은 **전혀 안 일그러진다**.
    #    ⚠ rve 50 · 로딩 2 에서 d_se 1.0 이 **하한이다** (0.9 면 ~23만으로 넘는다).
    #    ⚠ 잃는 것: 코퍼스에 2건뿐인 sub-µm SE 축.  살리려면 그 축만 작은 RVE 서브블록으로
    #      (rve 24 · d_am_p ≤ 7 µm 면 20만 아래) — 본 설계를 일그러뜨리지 않는 방법이다.
    'd_se_um':   (1.0, 2.0),       # 전해질
    'am_pct':    (70.0, 95.0),     # 활물질 함량 wt%
}
FACTORS = list(RANGES)
#  끝점 블록에서 **살아 있는** 인자 (죽은 크기 인자는 좌표를 배정하지 않는다)
END_ACTIVE = {0.0: ['d_am_s_um', 'd_se_um', 'am_pct'],
              1.0: ['d_am_p_um', 'd_se_um', 'am_pct']}
#  내부 블록의 ps 범위 — 0/1 은 끝점 블록이 담당하므로 여기서는 열어 둔다
PS_INTERIOR = (0.10, 0.90)      # 정수 설계에서는 1:9 … 9:1 이 내부다 (0:10/10:0 은 끝점 블록)

#  ── ★ 정수 격자 (2026-08-18 지시 "정수로 설계하는게 좋을거 같은데") ─────────────────
#    실물성 근거: 12.93 µm 분말을 주문할 수는 없다.  실제로 고를 수 있는 눈금에 설계를 얹는다.
#    d_SE 만 0.5 눈금인 이유 — 범위가 0.5–2 라 정수로 자르면 {1, 2} 두 수준밖에 안 남는다.
#    ps 눈금 0.1 = 랩이 이미 쓰는 `0:10 · 3:7 · 5:5 · 7:3 · 10:0` 표기와 정확히 일치한다.
#    am_pct 눈금 5 (2026-08-18 지시) — 70/75/80/85/90/95 = 6수준.  1 눈금(26수준)이면
#    60점에 수준당 2–3개라 **수준별 반복이 거의 없어** 조성 효과가 다른 인자와 섞이기 쉽다.
#    5 눈금이면 수준당 10개 = 조성 축을 **블록처럼** 읽을 수 있고, 실제 배합도 5 % 단위다.
STEP = {'d_am_p_um': 1.0, 'd_am_s_um': 1.0, 'ps_frac': 0.1, 'd_se_um': 0.5, 'am_pct': 5.0}


def levels_of(name, ps_range=None):
    """그 인자가 실제로 고를 수 있는 값들 (정수 격자)."""
    lo, hi = RANGES[name]
    if name == 'ps_frac' and ps_range is not None:
        lo, hi = ps_range
    st = STEP[name]
    k = int(round((hi - lo) / st))
    return [round(lo + i * st, 6) for i in range(k + 1)]


def _balanced(n, L, rng):
    """L 수준에 n 점을 **균형** 배정 (각 수준이 floor/ceil(n/L) 번) 후 섞는다.
    ⇒ 연속 LHS 의 '층마다 정확히 하나' 를 이산 격자로 옮긴 것."""
    base, rem = divmod(n, L)
    idx = np.array([i for i in range(L) for _ in range(base + (1 if i < rem else 0))])
    return rng.permutation(idx)


#  설계행렬이 넘으면 안 되는 |비대각 상관| — 이 값을 넘으면 인자 효과가 서로 섞인다.
CORR_MAX = 0.25


def _unit(I, level_lists):
    """수준 인덱스 → 단위공간 [0,1] (수준 수가 인자마다 달라 인덱스로 재면 왜곡된다)."""
    return np.stack([I[:, j] / max(len(level_lists[j]) - 1, 1)
                     for j in range(I.shape[1])], 1)


def _score(U):
    """(최대 |비대각 상관|, 최소 쌍거리)."""
    C = np.corrcoef(U.T)
    mc = float(np.abs(C[~np.eye(U.shape[1], dtype=bool)]).max())
    d2 = ((U[:, None, :] - U[None, :, :]) ** 2).sum(-1)
    d2[np.diag_indices(len(U))] = np.inf
    return mc, float(np.sqrt(d2.min()))


def lhs_grid(n, level_lists, rng, restarts=400, corr_max=CORR_MAX, sweeps=60):
    """정수 격자 위의 LHS → 수준 인덱스 배열 (n, k).

    ★★ 2026-08-18 — 옛 판은 **maximin(최소 쌍거리)만** 최적화했다.  상관은 이긴 배치가
    우연히 갖는 값이었고, 격자가 고울 때는 그럭저럭 낮았지만(0.15) **거칠어지자 튀었다**:
    am_pct 눈금을 1→5 로 바꾸자 재시작을 60→8000 으로 늘려도 max|corr| 이
    0.23 / 0.21 / **0.37** / 0.21 로 **재시작과 무관하게 오르내렸다** (실측).
    ⇒ 최적화 대상이 우리가 신경 쓰는 양이 아니었다.  두 단계로 고친다:
      ① 무작위 재시작을 **벌점 목적함수**로 고른다 — 상관이 문턱을 넘으면 크게 깎는다
      ② 이긴 배치를 **열 내부 스왑**으로 다듬는다 (열 안에서만 바꾸므로 수준 균형은 불변)
    """
    k = len(level_lists)
    best, best_obj, best_sc = None, -1e18, None
    for _ in range(int(restarts)):
        I = np.stack([_balanced(n, len(level_lists[j]), rng) for j in range(k)], 1)
        mc, md = _score(_unit(I, level_lists))
        obj = md - 10.0 * max(0.0, mc - corr_max)        # 상관 초과분에 큰 벌점
        if obj > best_obj:
            best, best_obj, best_sc = I, obj, (mc, md)
    #  ② 스왑 다듬기 — 한 열에서 두 행의 수준을 맞바꾼다.  열 안의 값 집합이 그대로라
    #     **수준 균형(=이산 LHS 성질)이 정의상 보존**된다.
    I = best.copy()
    for _ in range(int(sweeps)):
        improved = False
        for _try in range(n * k):
            j = int(rng.integers(k))
            a, b = rng.integers(n, size=2)
            if a == b or I[a, j] == I[b, j]:
                continue
            I[[a, b], j] = I[[b, a], j]
            mc, md = _score(_unit(I, level_lists))
            obj = md - 10.0 * max(0.0, mc - corr_max)
            if obj > best_obj + 1e-12:
                best_obj, best_sc, improved = obj, (mc, md), True
            else:
                I[[a, b], j] = I[[b, a], j]              # 되돌린다
        if not improved:
            break
    return I


def lhs_grid_feasible(n, level_lists, names, feasible, rng, restarts=60,
                      sweeps=200, corr_max=CORR_MAX, bal_w=3.0):
    """**제약이 있는** 정수 격자 설계 — 후보 풀에서 n 행을 고른다.

    ★ 왜 별도 알고리즘인가 (2026-08-18): 입자수 상한을 10만으로 조이면 제약이 `d_se`
      하나가 아니라 **여러 축에 동시에** 걸린다 (실측 생존률: am_pct 70 → 64 % ·
      d_se 1.0 → 76 % · d_am_s 1 → 78 % · ps 0.1 → 83 %).  그러면 `_balanced()` 로 만든
      배치가 제약을 위반하고, 위반 행만 갈아끼우면 **수준 균형이 깨진다**.
      ⇒ 실현 가능한 조합만 모은 **후보 풀에서 고르고**, 목적함수에 **균형 항을 명시**한다.
      (200k 상한에서는 제약이 d_se 에만 걸려 범위 조정만으로 됐다 — 그때는 이 경로가 불필요.)

    목적: −bal_w·(수준 점유 불균형) − 10·max(0, max|corr| − corr_max) + minDist
    """
    pool = [c for c in feasible]
    if len(pool) < n:
        raise SystemExit(f'실현 가능한 조합이 {len(pool)}개 < 요청 {n}행')
    idx = {f: {v: j for j, v in enumerate(level_lists[i])} for i, f in enumerate(names)}

    def to_I(sel):
        return np.array([[idx[f][c[f]] for f in names] for c in sel])

    def obj(sel):
        I = to_I(sel)
        mc, md = _score(_unit(I, level_lists))
        bal = 0.0
        for j, f in enumerate(names):
            L_ = len(level_lists[j])
            cnt = np.bincount(I[:, j], minlength=L_)
            bal += float(np.abs(cnt - len(sel) / L_).sum()) / len(sel)   # 총 편차 비율
        return md - 10.0 * max(0.0, mc - corr_max) - bal_w * bal, (mc, md, bal)

    best, best_o, best_s = None, -1e18, None
    for _ in range(int(restarts)):
        sel = [pool[i] for i in rng.choice(len(pool), n, replace=False)]
        o_, st = obj(sel)
        if o_ > best_o:
            best, best_o, best_s = sel, o_, st
    sel = list(best)
    inpool = {id(c) for c in sel}
    for _ in range(int(sweeps)):
        improved = False
        for _t in range(n * 3):
            a_ = int(rng.integers(n))
            cand = pool[int(rng.integers(len(pool)))]
            if id(cand) in inpool:
                continue
            old = sel[a_]
            sel[a_] = cand
            o_, st = obj(sel)
            if o_ > best_o + 1e-12:
                best_o, best_s, improved = o_, st, True
                inpool.discard(id(old)); inpool.add(id(cand))
            else:
                sel[a_] = old
        if not improved:
            break
    return to_I(sel)


#  ── 고정 상수 (인자가 아니다 — 2026-08-18 지시) ──────────────────────────────────
#    면용량 2 mAh/cm² = wall effect 가 거의 안 나오는 최소 단위 · RVE 50×50 µm.
#    ★ 인자에서 빼는 것이 이득이다: 기존 ML 설계층은 `rve` 와 `loading` 을 **자유 노브**로
#      두는데(ml_design_structure.FREE_KNOBS), 그 둘을 고정하면 5 인자에 예산을 다 쓴다.
FIXED = {'rve_um': 50.0, 'loading_mAh_cm2': 2.0}
#  두께는 로딩의 함수다 — 코퍼스 291건 원점회귀 (3σ 제거 후) **19.64 µm per mAh/cm²**
#  ⇒ 면용량 2.0 → 두께 ≈ 39 µm.  DEM 이 실제 두께를 낼 것이고 이 값은 **사전 점검용**이다.
THICK_PER_LOADING_UM = 19.64

#  ── ★ 물리 파생 (2026-08-18 적대 리뷰 R0) ────────────────────────────────────────
#    덱 실측값 — 밀도는 스케일되지 않는다 (input_real_*.liggghts).
RHO_AM_KGM3, RHO_SE_KGM3 = 4800.0, 2000.0
EPS_TYPICAL = 0.183             # ★ 실측 보정: 덱 mesh STL(6 mAh, step 2.93e6) plate_z =
#   0.116811 m = 116.8 µm, 고체만 높이 96.2 µm ⇒ ε = 0.176.  코퍼스 회귀(19.64 µm/mAh)가
#   함축하는 0.183 과 0.9 % 안에서 일치한다.  옛 0.16 은 근거 없는 어림이었다.
PRESSURE_MPA = 300.0            # 코퍼스 규약 — 리뷰 HIGH-E: 컬럼에 없으면 범위인지 편향인지 모른다
E_SE_GPA = 1.35                 # DEM 유효 SE 탄성계수 (CLAUDE.md 확정값)
PHI_C_SE = 0.195                # SE 퍼콜 문턱 (CLAUDE.md FROZEN φc_S; φc_P = 0.200)
N_AM_P_MIN = 30                 # 이보다 적으면 coverage_AM_P·ps_frac 이 실현되지 않는다
N_TOTAL_CAP = 100_000           # 지시 2026-08-18 — "10만 내외가 가장 좋다, 그래서 면용량 2"
#   ⚠ 200k 였을 땐 제약이 d_se 에만 걸려 범위 조정으로 끝났다.  100k 는 여러 축에 걸려
#     (am_pct 70 → 64 % · d_se 1.0 → 76 % · d_am_s 1 → 78 % · ps 0.1 → 83 %)
#     제약-인지 샘플러(`lhs_grid_feasible`)가 필요하다.


def phi_of(am_pct, eps=EPS_TYPICAL):
    """중량 % → (φ_AM, φ_SE) 전체 부피 기준."""
    va, vs = am_pct / RHO_AM_KGM3, (100.0 - am_pct) / RHO_SE_KGM3
    f = va / (va + vs)
    return (1.0 - eps) * f, (1.0 - eps) * (1.0 - f)


_PHI_AM_REF = phi_of(81.6)[0]   # 코퍼스 회귀가 잡힌 조성 (AM:SE = 81.6:18.4)


def thickness_of(am_pct, loading):
    """★ 두께는 상수가 아니다 (리뷰 MED-J).  면용량 고정이면 두께 ∝ 1/φ_AM 이므로
    am_pct 70 → 95 에서 **51.7 → 28.7 µm (1.8배)** 로 변한다.  옛 판이 39.28 을 모든 행에
    박아 `thick_over_d_am_max` 와 `finite_size_flag` 를 **틀리게** 만들고 있었다."""
    return THICK_PER_LOADING_UM * loading * (_PHI_AM_REF / phi_of(am_pct)[0])


def n_particles(d_um, phi, rve_um, thick_um):
    """그 상의 입자 개수 추정 (구 부피 기준)."""
    if not d_um or d_um != d_um or d_um <= 0:
        return float('nan')
    return phi * (rve_um * rve_um * thick_um) / ((np.pi / 6.0) * d_um ** 3)


def lhs(n, k, rng, restarts=200):
    """maximin LHS (numpy 전용).  각 인자를 n 등분해 층마다 정확히 한 점 = 1-D 균일 보장,
    그 위에서 최소 쌍거리를 최대화하는 순열을 무작위 재시작으로 고른다."""
    best, best_d = None, -1.0
    for _ in range(int(restarts)):
        u = np.empty((n, k))
        for j in range(k):
            u[:, j] = (rng.permutation(n) + rng.random(n)) / n
        if n < 2:
            return u
        d2 = ((u[:, None, :] - u[None, :, :]) ** 2).sum(-1)
        d2[np.diag_indices(n)] = np.inf
        m = float(np.sqrt(d2.min()))
        if m > best_d:
            best, best_d = u, m
    return best


def _scale(u, names, ps_range=None):
    out = {}
    for j, nm in enumerate(names):
        lo, hi = RANGES[nm]
        if nm == 'ps_frac' and ps_range is not None:
            lo, hi = ps_range
        out[nm] = lo + u[:, j] * (hi - lo)
    return out


def _n_total_of(d):
    """이 조합의 전체 입자수 추정 (덱 실측으로 검증된 규약).  `dem_input_values` 와 같은 계산."""
    fa, fs = phi_of(d['am_pct'])
    th = thickness_of(d['am_pct'], FIXED['loading_mAh_cm2'])
    r = FIXED['rve_um']
    tot = 0.0
    for dd, ph in ((d.get('d_am_p_um'), fa * d['ps_frac']),
                   (d.get('d_am_s_um'), fa * (1.0 - d['ps_frac'])),
                   (d['d_se_um'], fs)):
        v = n_particles(dd, ph, r, th)
        if v == v:
            tot += v
    return tot


def feasible_combos(names, level_lists, extra=None, cap=None):
    """입자수 상한을 만족하는 격자 조합만 (제약-인지 샘플러의 후보 풀).

    `extra` = 그 블록에서 **고정된** 값 (끝점 블록의 ps 와, 없는 상의 NaN).
    """
    import itertools as _it
    cap = N_TOTAL_CAP if cap is None else cap
    base = {'d_am_p_um': float('nan'), 'd_am_s_um': float('nan'), 'ps_frac': 0.0}
    base.update(extra or {})
    out = []
    for c in _it.product(*level_lists):
        d = dict(zip(names, c))
        if _n_total_of(dict(base, **d)) <= cap:
            out.append(d)
    return out


def build(n_interior=60, n_end=10, seed=0, restarts=400, grid=True):
    rng = np.random.default_rng(seed)
    rows = []

    # ── 블록 A: 내부(양상 공존) 5-인자 ────────────────────────────────────────
    if grid:
        LV = [levels_of(f, PS_INTERIOR) for f in FACTORS]
        #  ★ 제약(입자수 상한)이 있으면 후보 풀에서 고른다 — 균형을 목적함수로 지킨다
        _pool = feasible_combos(FACTORS, LV)
        _all = int(np.prod([len(x) for x in LV]))
        if len(_pool) < _all:
            IA = lhs_grid_feasible(n_interior, LV, FACTORS, _pool, rng,
                                   restarts=max(40, restarts // 40))
        else:
            IA = lhs_grid(n_interior, LV, rng, restarts)
        for i in range(n_interior):
            rows.append({'block': 'bimodal',
                         **{f: float(LV[j][IA[i, j]]) for j, f in enumerate(FACTORS)}})
    else:
        uA = lhs(n_interior, len(FACTORS), rng, restarts)
        sA = _scale(uA, FACTORS, ps_range=PS_INTERIOR)
        for i in range(n_interior):
            rows.append({'block': 'bimodal', **{f: float(sA[f][i]) for f in FACTORS}})

    # ── 블록 B/C: 단일모달 끝점 — **죽은 크기 인자에 좌표를 주지 않는다** ─────
    for ps, active in END_ACTIVE.items():
        if grid:
            LVb = [levels_of(f) for f in active]
            _poolb = feasible_combos(active, LVb, extra={'ps_frac': ps})
            _allb = int(np.prod([len(x) for x in LVb]))
            IB = (lhs_grid_feasible(n_end, LVb, active, _poolb, rng,
                                    restarts=max(40, restarts // 40))
                  if len(_poolb) < _allb else lhs_grid(n_end, LVb, rng, restarts))
            get = lambda i, f: float(LVb[active.index(f)][IB[i, active.index(f)]])
        else:
            sB = _scale(lhs(n_end, len(active), rng, restarts), active)
            get = lambda i, f: float(sB[f][i])
        for i in range(n_end):
            r = {'block': 'mono_AM_P' if ps == 1.0 else 'mono_AM_S', 'ps_frac': float(ps)}
            for f in FACTORS:
                if f == 'ps_frac':
                    continue
                r[f] = get(i, f) if f in active else float('nan')
            rows.append(r)

    # ── 파생 (DEM 입력 + 기존 ML 설계층 호환) ────────────────────────────────
    for k, r in enumerate(rows):
        r['case_id'] = f'lhs{seed:02d}_{k:03d}'
        p = r['ps_frac']
        dP, dS = r['d_am_p_um'], r['d_am_s_um']
        #  ⚠ 2026-08-18 리뷰 HIGH-H: 옛 `d_am_um`(ps 가중 **산술평균**)을 **버렸다**.
        #    코퍼스의 `d_am` 은 `max(d_P, d_S)` 라 같은 이름이 다른 물리량이었고
        #    (중앙 1.41배 · 최대 6.09배), 게다가 ps 는 부피분율인데 산술평균 가중치로 써서
        #    차원도 안 맞았다.  ⇒ 아래에서 `d_am_max_um`(코퍼스 규약)과
        #    `sv_inv_um`(Sauter 역수, 패킹 물리)을 **각각** 낸다.
        for src, dst in (('d_am_p_um', 'r_AM_P_um'), ('d_am_s_um', 'r_AM_S_um'),
                         ('d_se_um', 'r_SE_um')):
            r[dst] = r[src] / 2.0                       # ← LIGGGHTS 입력은 **반경**
        r['ps_label'] = (f'{round(p * 10):d}:{10 - round(p * 10):d}')   # 7:3 식 표기
        #  ★ 정수 격자(ps 눈금 0.1)에서는 이 라벨이 **반올림이 아니라 정확**하다
        r['size_ratio_P_over_S'] = (dP / dS) if (dP == dP and dS == dS) else float('nan')
        r['size_ratio_AM_over_SE'] = None            # 아래에서 d_am_max_um 확정 후 채운다
        #  ★ 코퍼스 규약의 `d_am` = max(d_P, d_S) — 신규 행을 코퍼스에 붙일 때 **이 열**을
        #    맞춰야 한다 (리뷰 HIGH-H: 산술평균과 중앙 1.41배 · 최대 6.09배 어긋난다).
        r['d_am_max_um'] = (dS if np.isnan(dP) else (dP if np.isnan(dS) else max(dP, dS)))
        #  ★★ Sauter 역수 — **끝점에서 저절로 잘 정의된다** (리뷰 §2 처방).
        #    S_v ∝ φ_AM·(ps/d_P + (1−ps)/d_S) 이고 ps=0 이면 d_P 가, ps=1 이면 d_S 가
        #    가중치 0 으로 사라진다 ⇒ NaN·센티넬·블록분리 없이 80 행이 한 모델에 들어간다.
        #    (코퍼스는 ps=0 행에 `d_am=0` 센티넬을 박아 40/291 행이 오염돼 있다.)
        r['sv_inv_um'] = ((0.0 if np.isnan(dP) else p / dP)
                          + (0.0 if np.isnan(dS) else (1.0 - p) / dS))
        #  ── 고정 상수와 물리 파생 ────────────────────────────────────────────────
        r.update(FIXED)
        r['pressure_MPa'] = PRESSURE_MPA          # 리뷰 HIGH-E
        r['e_se_gpa'] = E_SE_GPA
        fa, fs = phi_of(r['am_pct'])
        r['phi_am_est'], r['phi_se_est'] = fa, fs
        #  ★ SE 퍼콜 사전판정 (리뷰 BLOCKER-C).  φ_SE = 0.195 는 am_pct ≈ 88.8 wt% 다.
        #  ⚠⚠ **이름에 규약을 박는다** (`LHS-01`, 2026-09-15).  옛 이름은 `se_percolation` 이라
        #    **실측처럼 읽혔는데** 이 값은 `phi_se_est`(런 **전** 추정)를 동결 평균장 문턱에 댄
        #    파생 라벨이다.  같은 파일 아래 HIGH-F 주석이 이미 *"타깃 이름에 규약을 박는다"* 를
        #    규칙으로 세워 뒀는데 **이 열만 예외로 남아 있었다**.
        #    운용 특성은 `LHS_PERC_MEASURED` 에 실측으로 동결돼 있다 — **선별기이지 필터가 아니다.**
        r['se_percolation_est_meanfield'] = ('OK' if fs > 0.20 else
                                             ('marginal' if fs > PHI_C_SE else 'BELOW_phic'))
        th = thickness_of(r['am_pct'], FIXED['loading_mAh_cm2'])
        r['thickness_est_um'] = th
        #  ★ 입자 수 (rve 50 기준) — coverage_AM_P 와 ps 실현 가능성의 직접 지표
        r['n_am_p_est'] = n_particles(dP, fa * p, FIXED['rve_um'], th)
        r['n_am_s_est'] = n_particles(dS, fa * (1.0 - p), FIXED['rve_um'], th)
        r['n_se_est'] = n_particles(r['d_se_um'], fs, FIXED['rve_um'], th)
        r['n_total_est'] = float(np.nansum([r['n_am_p_est'], r['n_am_s_est'], r['n_se_est']]))
        #  ★ N_AM_P ≥ 30 을 만족하려면 상자가 얼마나 커야 하나 (N ∝ rve²)
        _np_ = r['n_am_p_est']
        r['rve_min_um'] = (float('nan') if (_np_ != _np_ or _np_ <= 0)
                           else FIXED['rve_um'] * float(np.sqrt(N_AM_P_MIN / _np_)))
        r['rve_recommended_um'] = (FIXED['rve_um'] if r['rve_min_um'] != r['rve_min_um']
                                   else max(FIXED['rve_um'], r['rve_min_um']))
        dmax = r['d_am_max_um']                              # 가장 큰 입자가 상자를 정한다
        r['rve_over_d_am_max'] = FIXED['rve_um'] / dmax           # 측면 상자 / 최대 입자
        r['thick_over_d_am_max'] = th / dmax                      # 두께 / 최대 입자
        r['size_ratio_AM_over_SE'] = dmax / r['d_se_um']
        #  ⚠ 측면은 **벽이 아니라 주기경계**다 (생산 덱 `boundary p p f`) — 측면 유한크기는
        #    wall effect 가 아니라 **상관길이 효과**이고, 디스크립터 계산 시 x,y 를
        #    최소상거리로 다뤄야 한다.  z(두께)만 진짜 유한크기다.
        #  ⚠ 플래그는 **거부가 아니라 라벨**이다 — 이 코너가 물리적으로 얇다는 사실 자체가
        #    데이터의 일부다 (실제 39 µm 전극에 Ø15 µm 입자면 정말 2.6층이다).
        #    기준: 코퍼스 최빈 구성이 rve50/d12 = 4.17, rve40/d12 = 3.33 이므로 3.3 을
        #    "우리가 이미 돌려 본 하한" 으로 잡는다 (새 기준을 발명하지 않는다).
        f = []
        if r['rve_over_d_am_max'] < 3.3:
            f.append('lateral')
        if r['thick_over_d_am_max'] < 3.0:
            f.append('thin')
        #  ★ 리뷰 BLOCKER-B: 대립이 한 자릿수면 `coverage_AM_P` 도 명목 `ps_frac` 도
        #    실현되지 않는다 (입자 하나가 ps 의 30 % 를 차지하는 행이 실재).
        if _np_ == _np_ and _np_ < N_AM_P_MIN:
            f.append('n_am_p_low' if _np_ >= 10 else 'n_am_p_CRIT')
        r['finite_size_flag'] = '+'.join(f)
        #  ⚠⚠ **SE 퍼콜 추정을 유한크기 플래그에서 뺀다** (`LHS-01`, 2026-09-15).
        #    옛 판은 `se_BELOW_phic` 를 `finite_size_flag` 에 **접합**해서 **기하 플래그가
        #    물리 추정을 날랐다**.  설계 130 행 중 44 행이 그렇게 켜졌고 그 중 **22 행은
        #    유한크기가 깨끗한데도** 플래그가 서 있었다 = 두 가지가 한 열에서 구별 불가.
        #    ⇒ 자기 열로 분리한다.  둘을 **같이** 보고 싶으면 두 열을 읽으면 된다.
        r['se_perc_est_flag'] = ('' if r['se_percolation_est_meanfield'] == 'OK'
                                 else 'se_' + r['se_percolation_est_meanfield'])
    return rows


#  ★★★ **실측 운용 특성** (`LHS-01` 닫음, 2026-09-15).  위 평균장 라벨을 코호트 127 케이스의
#    **생산 솔버 이온 관통 여부**와 대조한 결과다 (원자료 `docs/data/lhs_percolation_measured_20260915.csv`,
#    파생 `docs/lhs_corpus_readout_20260915.md`).  ⚠ 이 상수는 **읽는 법을 박아 두는 것**이지
#    코드 분기에 쓰라는 값이 아니다.
#
#      se_percolation_est_meanfield = OK          n=83   실제 막힘  1  (= 1.2 %)
#      se_percolation_est_meanfield = BELOW_phic  n=44   실제 막힘 24  (= 54.5 %)
#
#    ⇒ **선별기(screen)로는 훌륭하다** — 재현율 96.0 % (막힌 25건 중 24건을 잡는다).
#      놓친 1건은 `lhs00_009` 이고 그것은 물리가 아니라 경계 규칙이다 (`LHS-04`).
#    ⛔ **필터로 쓰면 안 된다** — 정밀도 54.5 % 라 `BELOW_phic` 를 버리면 **실제로 뚫리는
#      20건을 같이 버린다**.  이것이 `LHS-01` 이 P2 로 등재된 이유다.
#    ★ 그리고 이 값이 `thick_over_d_am_max` 보다 **잘 가른다**: 두 군 막힘률 비 **45.3배**
#      vs 유한크기 구간 최대/최소 **5.1배**(게다가 단조도 아니다 — 42.9/13.7/8.3/25.0 %).
#      ⚠ 판독문 ④ 의 옛 문장 *"유한크기가 φ 보다 잘 가른다"* 는 **이 측정으로 반증됐다**.
LHS_PERC_MEASURED = {
    'source': 'docs/data/lhs_percolation_measured_20260915.csv',
    'n_measured': 127, 'channel': 'ionic', 'solver': 'production (legacy arm, 기본값)',
    'OK': {'n': 83, 'blocked': 1}, 'BELOW_phic': {'n': 44, 'blocked': 24},
    'recall_pct': 96.0, 'precision_pct': 54.5, 'use': 'screen_not_filter',
}


#  ★★ 타깃 이름에 **규약을 박는다** (리뷰 HIGH-F).  리포 실측 모호폭:
#    coverage Hertz 22.25 % vs physics/Tabor 60.53 % (**2.7배**) — 섞으면 CLAUDE.md 가 기록한
#    σ_ionic T1 "FALSE-REVERT"(91건 전부 1.4배 과대예측)가 그대로 재발한다.
#    tortuosity Laplace 3.53 vs Dijkstra 1.29 (**2.73배**, 같은 케이스).
#    porosity ε_sphere vs ε_union (**1.251 %p** 오프셋).
#  ★ 그리고 **porosity 는 회귀 타깃에서 뺀다** — CLAUDE.md 정본 처방:
#    "porosity 는 회귀 말고 ε = C − φ_SE − φ_AM 로 계산 (raw DEM 닫힘 1.0000±0.0000 =
#     정확한 항등식 → φ 너머 정보 0)".  φ 둘을 배우고 빼면 된다 (추가 런 0건).
#    ε_sphere 는 **기록**은 하되 타깃 목록에는 안 넣는다.
DESCRIPTORS = ['phi_se', 'phi_am',                       # ← 회귀 타깃 (porosity 는 이 둘에서 유도)
               'coverage_AM_P_hertz_pct', 'coverage_AM_S_hertz_pct',
               'coverage_AM_total_hertz_pct',
               'tortuosity_dijkstra_SE',
               'porosity_sphere_pct_RECORD_ONLY']


#  ═══ `LHS-02` — 빈 측정 열을 **기계가 보게 한다** (2026-09-15) ═════════════════════
#  결함: 설계 CSV 는 `phi_se_est`(추정)와 `phi_se`(측정)를 **나란히** 갖는데 측정 쪽이
#    130/130 전부 비어 있다.  아무것도 그것을 검사하지 않았다.
#  ★ **지금 당장 오염된 판정은 없다** — 설계 CSV 를 여는 코드 전수(`dem_input_values.py` ·
#    `seal_s3_prerun.py` · `lhs_perc_fit.py` · `lhs_ext_design.py`)가 **설계 노브와 `case_id`
#    만** 읽고 측정 열은 **한 곳도 안 읽는다**.  ⇒ 이 결함은 **잠복**이지 활성이 아니다.
#  ⛔ 그래서 더 위험하다: 다음 사람이 학습셋을 만들며 `phi_se` 를 집으면 **빈 문자열**을 받고,
#    `float(x or 0)` 한 줄이면 **0 이 실측처럼** 들어간다 = 원장 `GAP2-05` 와 정확히 같은 자리.
#  ⇒ 처방은 열 삭제가 **아니다** (수확기 `lhs_descriptor_harvest.py` 가 그 이름에 쓴다).
#    **읽기를 fail-closed 로** 만들고, 채움 상태를 **수치로 보고**한다.
#  ★★ **갱신 2026-09-19 — 채웠다.**  옛 등록값(전부 0)과 그 사유 *"아직 수확되지 않았다"* 는
#    **낡았다**.  규율 ④ 가 경고한 자리이므로 채우는 커밋에서 같이 고친다.
#    남은 결측은 **두 종류뿐이고 둘 다 사유가 있다** — 빈 채로 방치된 칸은 없다.
DESCRIPTOR_FILL_EXPECTED = {           # 2026-09-19 실측.  움직이면 ⑭d 가 알려 준다.
    'path': 'docs/data/lhs_design_20260818.csv', 'n_rows': 130,
    'filled': {'phi_se': 130, 'phi_am': 130,
               'coverage_AM_P_hertz_pct': 100, 'coverage_AM_S_hertz_pct': 100,
               'coverage_AM_total_hertz_pct': 130,
               'tortuosity_dijkstra_SE': 14,
               'porosity_sphere_pct_RECORD_ONLY': 130},
    'why_partial': {
        'coverage_AM_P_hertz_pct': '30 = mono 설계(단일 AM 상)의 `N_A_PHASE_ABSENT`. '
                                   '**없는 상**이지 무접촉 0 이 아니다 (DESC-05).  '
                                   '(설계 CSV 의 등록값 — 인계표는 J20-k (B) 로 설계 상 칸에 전체 값을 싣는다)',
        'coverage_AM_S_hertz_pct': '위와 같은 30 건.',
        'tortuosity_dijkstra_SE': '116 = τ 실패.  ⚠ **원장 `LHS-08` 이 열려 있다** — 그 실패가 '
                                  '물리인지 전극 밴드 규약인지 아직 안 갈렸다.  재측정 뒤 '
                                  '이 숫자가 움직일 수 있다 (그때 이 등록값도 같이 고친다).',
    },
    'source': 'docs/data/lhs_descriptors_20260924/ (재수확 130/130, 2026-09-24 — 09-19 판은 LHS-10 · 11 로 폐기)',
    'manifest': 'docs/data/lhs_design_20260818_descriptor_manifest.json',
    'harvester': 'scripts/lhs_descriptor_harvest.py (selftest 전부 통과 2026-09-19)',
    'filler': 'scripts/lhs_design_dataset.py --fill-descriptors',
}


def descriptor_fill(rows):
    """설계 행들의 측정 열 채움 수를 **센다**.  '' · None · NaN 은 전부 결측이다.

    ⚠ `0` 은 결측이 **아니다** — 무접촉 AM 의 coverage 0.0 은 유효한 측정이다
      (`DESC-05`: *"없는 AM_P → N/A, 존재하는데 무접촉 → 0.0"*).  둘을 같이 세면
      바로 그 결함을 검사기가 재생산한다.
    """
    out = {}
    for c in DESCRIPTORS:
        n = 0
        for r in rows:
            v = r.get(c, '')
            if v is None or (isinstance(v, str) and not v.strip()):
                continue
            if isinstance(v, float) and v != v:            # NaN
                continue
            n += 1
        out[c] = n
    return out


def require_descriptors(rows, cols, path='<rows>'):
    """측정 열을 읽기 **전에** 부른다.  결측이 하나라도 있으면 **거부**한다 (`LHS-02`).

    ⛔ 호출자가 이것을 부르지 않고 `float(r[c] or 0)` 를 쓰면 결측이 **0 이라는 측정**이 된다.
    """
    fill = descriptor_fill(rows)
    bad = {c: fill.get(c, 0) for c in cols if fill.get(c, 0) < len(rows)}
    if bad:
        raise ValueError(
            f'{path}: 측정 열이 비어 있다 — ' +
            ' · '.join(f'{c} {n}/{len(rows)}' for c, n in bad.items()) +
            f'.  결측을 0 으로 채우지 말 것 (원장 LHS-02 · GAP2-05).  '
            f'채우려면: {DESCRIPTOR_FILL_EXPECTED["harvester"]}')
    return fill


#  ═══ `LHS-02` 수리 — 수확 산출물을 설계 CSV 에 **합친다** (2026-09-19) ══════════════
#  ⛔ 세 가지를 **동시에** 지킨다.  하나라도 빼면 이 병합이 결함의 새 자리가 된다.
#   `DESC-07` — 일곱 중 **둘은 정의 종속**이다.  병합 시점에 항등식을 **다시 검증**하고
#     열에 `_derived` 표시를 남긴다 (일곱 독립 타깃으로 세는 것을 막는다).
#   `DESC-08` — **291 코퍼스와 합치지 않는다.**  이 병합은 설계 130 ↔ 수확 130 뿐이다.
#   `DESC-09` — 미실행이 **무작위 결측이 아니다**.  ⇒ 부분 채움을 **금지**한다: 조인이
#     양방향 전단사가 아니면 거부한다 (반쪽 채움은 "한 수준이 통째로 빈" 것을 숨긴다).
#  ★ 그리고 `GAP2-05` 의 자리: **status ≠ OK 인 칸에는 숫자를 안 쓴다.**  빈 칸 + 사유
#    열이다.  0 을 쓰면 그 즉시 '측정된 0' 이 된다.
DESCRIPTOR_STATUS_KEY = {
    'phi_se': 'phi', 'phi_am': 'phi',
    'coverage_AM_P_hertz_pct': 'coverage_AM_P',
    'coverage_AM_S_hertz_pct': 'coverage_AM_S',
    'coverage_AM_total_hertz_pct': 'coverage_AM_total',
    'tortuosity_dijkstra_SE': 'tortuosity',
    'porosity_sphere_pct_RECORD_ONLY': 'porosity',
}
#: `DESC-07` — 이 둘은 **나머지로부터 유도**된다.  기록은 하되 독립 타깃이 아니다.
DERIVED_DESCRIPTORS = ('porosity_sphere_pct_RECORD_ONLY', 'coverage_AM_total_hertz_pct')
#: 항등식 허용오차.  ① 은 부동소수(실측 2.8e-14) · ② 는 실측 **정확히 0**.
DESC07_TOL = {'porosity': 1e-9, 'coverage_total': 1e-9}


class FillRefusal(RuntimeError):
    """병합이 조용히 반쪽으로 되는 것을 막는다 (`DESC-09`)."""


def _desc07_check(h):
    """수확 한 건에서 `DESC-07` 두 항등식을 **다시** 잰다 → (err_porosity, err_cov or None)."""
    e1 = abs(float(h['porosity_sphere_pct_RECORD_ONLY'])
             - 100.0 * (1.0 - float(h['phi_se']) - float(h['phi_am'])))
    cp, cs, ct = (h['coverage_AM_P_hertz_pct'], h['coverage_AM_S_hertz_pct'],
                  h['coverage_AM_total_hertz_pct'])
    if cp is None or cs is None:            # mono 침대 — 상이 하나라 가중평균이 정의 안 된다
        return e1, None
    cnt = h['coverage_detail']['counts']
    npp, ns = int(cnt['AM_P']['n_valid']), int(cnt['AM_S']['n_valid'])
    if npp + ns == 0:
        return e1, None
    return e1, abs((npp * float(cp) + ns * float(cs)) / (npp + ns) - float(ct))


def load_harvest(dir_path):
    """수확 JSON 들을 `case → dict` 로.  `_batch_summary.json` 은 케이스가 아니다."""
    d = pathlib.Path(dir_path)
    if not d.is_dir():
        raise FillRefusal(f'수확 디렉터리가 없다: {d}')
    out = {}
    for p in sorted(d.glob('*.json')):
        if p.name.startswith('_'):
            continue
        h = json.loads(p.read_text(encoding='utf-8'))
        case = h.get('case')
        if not case:
            raise FillRefusal(f'{p.name}: `case` 가 없다')
        if case in out:
            raise FillRefusal(f'수확에 같은 case 가 둘: {case}')
        h['_file'], h['_sha256'] = p.name, hashlib.sha256(p.read_bytes()).hexdigest()
        out[case] = h
    if not out:
        raise FillRefusal(f'{d}: 수확 JSON 이 하나도 없다')
    return out


def fill_descriptors(rows, harvest, key='case_id'):
    """설계 행에 측정 열 + `<열>_status` 를 채운다.  **전단사가 아니면 거부**한다.

    반환 = (채워진 행, 보고 dict).  ⚠ 행은 **제자리에서** 바뀐다.
    """
    have = {r[key] for r in rows}
    miss_h = sorted(have - set(harvest))
    miss_d = sorted(set(harvest) - have)
    if miss_h or miss_d:
        raise FillRefusal(
            f'조인이 전단사가 아니다 — 수확에 없는 설계 {len(miss_h)}건 {miss_h[:5]} · '
            f'설계에 없는 수확 {len(miss_d)}건 {miss_d[:5]}.  '
            '부분 채움은 `DESC-09`(결측이 무작위가 아니다)를 숨긴다 ⇒ 전부이거나 아무것도 아니다.')

    rep = {'n_rows': len(rows), 'filled': {c: 0 for c in DESCRIPTORS},
           'status_tally': {c: {} for c in DESCRIPTORS},
           'desc07_max_err': {'porosity': 0.0, 'coverage_total': 0.0,
                              'n_coverage_checked': 0},
           'derived': list(DERIVED_DESCRIPTORS), 'sources': {}}
    for r in rows:
        h = harvest[r[key]]
        e1, e2 = _desc07_check(h)
        rep['desc07_max_err']['porosity'] = max(rep['desc07_max_err']['porosity'], e1)
        if e1 > DESC07_TOL['porosity']:
            raise FillRefusal(f'{r[key]}: DESC-07 ① 항등식 위반 {e1:.3e} > {DESC07_TOL["porosity"]:.0e} '
                              '— porosity 가 φ 둘에서 유도되지 않는다면 프레임이 섞인 것이다')
        if e2 is not None:
            rep['desc07_max_err']['coverage_total'] = max(
                rep['desc07_max_err']['coverage_total'], e2)
            rep['desc07_max_err']['n_coverage_checked'] += 1
            if e2 > DESC07_TOL['coverage_total']:
                raise FillRefusal(f'{r[key]}: DESC-07 ② 가중평균 항등식 위반 {e2:.3e} '
                                  '— C_total 이 (N_P C_P + N_S C_S)/(N_P+N_S) 가 아니다')
        for c in DESCRIPTORS:
            st = h['status'][DESCRIPTOR_STATUS_KEY[c]]
            v = h.get(c)
            #  ★ 여기가 `GAP2-05` 의 자리다 — 상태가 OK 가 아니면 **숫자를 안 쓴다**.
            if st == 'OK':
                if v is None:
                    raise FillRefusal(f'{r[key]}.{c}: status 가 OK 인데 값이 없다')
                r[c] = repr(float(v))
                rep['filled'][c] += 1
            else:
                if v is not None:
                    raise FillRefusal(f'{r[key]}.{c}: status={st} 인데 값이 있다 ({v!r}) '
                                      '— 실패에 값이 붙으면 그 값이 측정으로 읽힌다')
                r[c] = ''
            r[c + '_status'] = st
            rep['status_tally'][c][st] = rep['status_tally'][c].get(st, 0) + 1
        rep['sources'][r[key]] = {
            'harvest_json': h['_file'], 'harvest_sha256': h['_sha256'],
            'atom_sha256': h['raw']['atom']['sha256'],
            'contact_sha256': h['raw']['contact']['sha256'],
            'timestep': h['timestep']}
    return rows, rep


def diagnostics(rows):
    """설계행렬이 실제로 쓸 만한지 — 상관·1D 균일·최소거리."""
    A = np.array([[r[f] for f in FACTORS] for r in rows if r['block'] == 'bimodal'])
    if len(A) < 3:
        return {}
    lo = np.array([RANGES[f][0] for f in FACTORS])
    hi = np.array([RANGES[f][1] for f in FACTORS])
    U = (A - lo) / (hi - lo)
    C = np.corrcoef(U.T)
    off = C[~np.eye(len(FACTORS), dtype=bool)]
    d2 = ((U[:, None, :] - U[None, :, :]) ** 2).sum(-1)
    d2[np.diag_indices(len(U))] = np.inf
    #  1-D 균일: 각 인자를 5 구간으로 나눠 최소 점유 (층화 LHS 면 균등해야 한다)
    occ = [int(np.histogram(U[:, j], bins=5, range=(0, 1))[0].min()) for j in range(len(FACTORS))]
    #  ★ 정수 격자에서는 **중복 설계점**이 생길 수 있다 (연속 LHS 에는 없던 실패 모드).
    #    같은 조성을 두 번 돌리는 것은 예산 낭비이고, 학습기에는 가짜 정밀도로 보인다.
    keys = [tuple(round(r[f], 6) for f in FACTORS) for r in rows if r['block'] == 'bimodal']
    dup = len(keys) - len(set(keys))
    #  수준별 점유 (균형 배정이 실제로 됐는지)
    lv = {}
    for f in FACTORS:
        L = levels_of(f, PS_INTERIOR)
        c = {v: 0 for v in L}
        for r in rows:
            if r['block'] == 'bimodal':
                c[round(r[f], 6)] = c.get(round(r[f], 6), 0) + 1
        lv[f] = f'{len(L)}수준 · 점유 {min(c.values())}–{max(c.values())}'
    #  ⚠ `min_bin_occupancy_of_5` 는 **연속 모드용** 지표다.  정수 격자에서는 수준 위치가
    #    5 등분 경계와 안 맞아 빈 구간이 생긴다 (예: d_se 4수준 → 5구간 중 하나는 구조적으로 0).
    #    ⇒ 정수 모드의 정본은 `levels` 의 **수준 점유**다.
    return {'n_bimodal': int(len(A)),
            'max_abs_offdiag_corr': round(float(np.abs(off).max()), 4),
            'min_pairwise_dist_unit': round(float(np.sqrt(d2.min())), 4),
            'min_bin_occupancy_of_5_CONTINUOUS_ONLY': occ,
            'duplicate_design_points': int(dup),
            'levels': lv}


#  ═══ 인계표 — 설계축을 밖(ML 담당)으로 넘긴다 (`LHS-02` 후속, 2026-09-19) ═════════
#  ⛔ 세 가지가 이 내보내기의 계약이다.  하나라도 빼면 받는 쪽이 조용히 틀린다.
#   ① **τ 값 열을 넣지 않는다** — `LHS-08` 이 열려 있어 `NOT_PERCOLATING` 이 두 원인을
#      접고 있다.  열이 CSV 에 있으면 학습에 들어간다("있으니까 쓴다").  대신 **왜 없는지**
#      를 `tau_*` 진단 열로 넘긴다.
#   ② **status ≠ OK 인 칸은 빈칸**이고 사유는 옆 열에 있다 (`GAP2-05`).  0 이 아니다.
#   ③ **유도열을 표시**한다 (`DESC-07`) — 일곱을 독립 타깃으로 세는 것을 막는다.
HANDOVER_VALUE_COLS = ('phi_se', 'phi_am',
                       'coverage_AM_P_hertz_pct', 'coverage_AM_S_hertz_pct',
                       'coverage_AM_total_hertz_pct', 'porosity_sphere_pct_RECORD_ONLY')
#: ⛔ 인계표에서 **제외**하는 열 (사유를 남긴다 — 조용히 빠지면 안 된다).
HANDOVER_HELD_BACK = {
    'tortuosity_dijkstra_SE': 'LHS-08 열림 — 130 중 14 만 값이 있고 `NOT_PERCOLATING` 이 '
                              '규약 실패와 물리 미관통을 **한 값으로 접는다**.  재수확 뒤 공급.  '
                              '↪ J20 (09-28): 벽 규약 τ 를 **새 열** `tortuosity_SE_wall` 로 공급 — 이 옛 규약 열은 계속 보류.',
}
#: 기본 수확 스냅샷 — ⛔ 옛 판 (20260919) 은 분모 바닥 · 이른 메시 (LHS-10 · 11) 로 폐기됐다.  조용히 옛 판을 가리키지 않는다 (HND-04).
#: 2026-09-28 (J19): 20260924 → **20260925** — 0924 JSON 에는 `handover_qc` (두께 · 벽 QC · 적격성) 가 없어 HND-04 열이 빈칸으로 나갔고
#:   (J18 기록: *"09-24 스냅샷 JSON 에는 handover_qc 가 없다 ⇒ 재수확 v2 뒤 인계표 재생성"*), union 병기의 짝 검사 (두께) 도 설 수 없다.
#:   0925 는 0924 를 대체한다 — 공통 값 Δ = 0 (그 README).
DEFAULT_HARVEST_DIR = 'docs/data/lhs_descriptors_20260925'
#: 수확 JSON 에서 **추가로** 실어 보내는 것 (새 계산 0 — 이미 측정돼 있다).
#: ★ HND-04 (Codex 09-25, 비준): 벽 QC · 적격성 · 규약 ID · sha 를 CSV 로 **실어 나른다** — JSON 에만 두고 CSV 에서 버리면 계약 실패.
HANDOVER_EXTRA = (
    ('n_AM_P_measured',      ('phase_counts', 'AM_P'),                      '실측 입자수 (설계의 n_*_est 는 추정)'),
    ('n_AM_S_measured',      ('phase_counts', 'AM_S'),                      '실측 입자수'),
    ('n_SE_measured',        ('phase_counts', 'SE'),                        '실측 입자수'),
    ('cov_AM_P_n_valid',     ('coverage_detail', 'counts', 'AM_P', 'n_valid'), '피복 평균의 분모'),
    ('cov_AM_S_n_valid',     ('coverage_detail', 'counts', 'AM_S', 'n_valid'), '피복 평균의 분모'),
    ('cov_n_capped',         ('coverage_detail', 'n_capped'),               'c_i 가 100 %% 로 잘린 횟수'),
    ('cov_n_free_surf_invalid', ('coverage_detail', 'n_free_surface_invalid'), 'F_i <= 0 분모붕괴 (DESC-05)'),
    ('closure_residual',     ('closure_residual',),                         'phi 닫힘 잔차 (QC)'),
    ('tau_status',           ('status', 'tortuosity'),                      'tau 가 왜 없는지'),
    ('tau_n_sampled',        ('tau_detail', 'n_sampled'),                   'tau 진단'),
    ('tau_n_valid',          ('tau_detail', 'n_valid'),                     'tau 진단'),
    ('tau_n_truncated',      ('tau_detail', 'n_truncated'),                 'tau 진단'),
    ('tau_convention',       ('tau_detail', 'tau_convention'),              'tau 규약 문자열'),
    ('plate_z_sim',          ('plate_z_sim',),                              '플래튼 z (sim)'),
    ('plate_z_source',       ('plate_z_source',),                           '플래튼 출처'),
    ('V_box_sim',            ('V_box_sim',),                                '상자 부피 (sim)'),
    ('timestep',             ('timestep',),                                 '읽은 덤프 스텝'),
    ('area_channel',         ('area_channel',),                             'L1-04 — 피복 면적이 무엇인가'),
    ('atom_sha256',          ('raw', 'atom', 'sha256'),                     '원자료 추적'),
    #  ── 두께 · 등록 alias 의 정본 의미 (Codex Q1 · Q2) ──
    ('thickness_wall_gap_um', ('handover_qc', 'thickness_wall_gap_um'),     '주 두께 — 같은 프레임의 플래튼 − 바닥 (z = 0) 간격, sim × 1e3'),
    ('phi_se_spheresum_nominal_gap', ('handover_qc', 'phi_se_spheresum_nominal_gap'), 'phi_se 의 정본 이름 — 명목 구 부피 / 틀 간격 부피 (장부값, 틀 안 점유율 아님)'),
    ('phi_am_spheresum_nominal_gap', ('handover_qc', 'phi_am_spheresum_nominal_gap'), 'phi_am 의 정본 이름'),
    ('porosity_spheresum_nominal_gap_pct', ('handover_qc', 'porosity_spheresum_nominal_gap_pct'), 'porosity 등록 열의 정본 이름 (독립 타깃 아님)'),
    #  ── 보조 지표 — (나) 등가 산술값 · (다) ROI clipped (둘 다 합집합 점유율 아님) ──
    ('thickness_pushback_equiv_um', ('handover_qc', 'thickness_pushback_equiv_um'), '(나) 벽 밖 부피를 두께에 더한 등가값 — hard-bottom 예측 아님 (HND-01)'),
    ('porosity_pushback_equiv_pct', ('handover_qc', 'porosity_pushback_equiv_pct'), '(나) 등가 porosity'),
    ('phi_se_clipped_spheresum_gap', ('handover_qc', 'phi_se_clipped_spheresum_gap'), '(다) 벽 밖 cap 을 뺀 ROI 값'),
    ('phi_am_clipped_spheresum_gap', ('handover_qc', 'phi_am_clipped_spheresum_gap'), '(다) ROI 값'),
    ('porosity_clipped_spheresum_gap_pct', ('handover_qc', 'porosity_clipped_spheresum_gap_pct'), '(다) ROI porosity'),
    #  ── 외피 진단 (실험 두께의 자동 대체물 아님) ──
    ('solid_bottom_um',      ('handover_qc', 'solid_bottom_um'),            'min(z − r) × 1e3'),
    ('solid_top_um',         ('handover_qc', 'solid_top_um'),               'max(z + r) × 1e3'),
    ('thickness_envelope_um', ('handover_qc', 'thickness_envelope_um'),     '외피 높이 — 극값 하나에 좌우될 수 있다'),
    ('plate_minus_solid_top_um', ('handover_qc', 'plate_minus_solid_top_um'), '플래튼 − 고체 윗면 (같은 step 메시면 작다, LHS-11)'),
    #  ── 부피 감사 (겹침 중복을 포함하는 구 합, µm³) ──
    ('V_AM_full_um3',        ('handover_qc', 'V_AM_full_um3'),              'AM 명목 구 부피 합'),
    ('V_SE_full_um3',        ('handover_qc', 'V_SE_full_um3'),              'SE 명목 구 부피 합'),
    ('V_AM_out_floor_um3',   ('handover_qc', 'V_AM_out_floor_um3'),         'AM 바닥 밖 cap 부피'),
    ('V_AM_out_plate_um3',   ('handover_qc', 'V_AM_out_plate_um3'),         'AM 플래튼 밖 cap 부피'),
    ('V_SE_out_floor_um3',   ('handover_qc', 'V_SE_out_floor_um3'),         'SE 바닥 밖 cap 부피'),
    ('V_SE_out_plate_um3',   ('handover_qc', 'V_SE_out_plate_um3'),         'SE 플래튼 밖 cap 부피'),
    #  ── 경계 QC (HND-03) ──
    ('n_floor_center_out',   ('handover_qc', 'n_floor_center_out'),         '중심이 바닥 평면 아래인 입자 수'),
    ('n_floor_fully_out',    ('handover_qc', 'n_floor_fully_out'),          '통째로 바닥 아래인 입자 수'),
    ('n_plate_center_out',   ('handover_qc', 'n_plate_center_out'),         '중심이 플래튼 위인 입자 수'),
    ('n_plate_fully_out',    ('handover_qc', 'n_plate_fully_out'),          '통째로 플래튼 위인 입자 수'),
    ('floor_out_pct',        ('handover_qc', 'floor_out_pct'),              '바닥 밖 부피 / ΣV (백분율)'),
    ('plate_out_pct',        ('handover_qc', 'plate_out_pct'),              '플래튼 밖 부피 / ΣV (백분율)'),
    ('floor_outside_cap_depth_over_r_max', ('handover_qc', 'floor_outside_cap_depth_over_r_max'), '가장 깊은 입자의 cap 깊이/r (접촉 겹침 아님)'),
    ('floor_deepest_contact_overlap_over_r', ('handover_qc', 'floor_deepest_contact_overlap_over_r'), '그 입자의 접촉 겹침/r = (r − |dist|)/r'),
    ('floor_deepest_phase',  ('handover_qc', 'floor_deepest_phase'),        '가장 깊은 입자의 상'),
    ('floor_deepest_r_um',   ('handover_qc', 'floor_deepest_r_um'),         '그 입자의 반지름'),
    ('floor_deepest_z_um',   ('handover_qc', 'floor_deepest_z_um'),         '그 입자의 중심 z'),
    ('plate_outside_cap_depth_over_r_max', ('handover_qc', 'plate_outside_cap_depth_over_r_max'), '플래튼 쪽 가장 깊은 입자의 cap 깊이/r'),
    ('boundary_state',       ('handover_qc', 'boundary_state'),             'INSIDE | CENTER_CROSSED | FULLY_OUT — 바닥 (z = 0) · 플래튼 평면 기준 (같은 프레임 · 수확기 wall_record): '
                                                                            '중심이 평면을 넘은 입자가 있으면 CENTER_CROSSED · 통째로 평면 밖인 입자가 있으면 FULLY_OUT · 없으면 INSIDE'),
    #  ── 적격성 (HND-04) — 숫자 산출 성공과 물리/ML 용도 허용을 분리 ──
    ('calculation_status',   ('handover_qc', 'calculation_status'),         '계산 상태 (명목 규약값)'),
    ('physical_target_status', ('handover_qc', 'physical_target_status'),   'OK | HOLD — 물리적 전극 구조 타깃으로 쓸 수 있는가 (HND-04 — 계산 상태와 분리) · HOLD = hold_reason_codes 가 하나라도 있다 · '
                                                                            '값은 그대로 계산됐다 (calculation_status OK) · 배포 v1.1 부터 함께 싣는다 — 거를지는 쓰는 쪽이 정한다'),
    ('hold_reason_codes',    ('handover_qc', 'hold_reason_codes'),          'BOUNDARY_CENTER_OUT = 중심이 바닥 · 플래튼 평면 밖인 입자 ≥ 1 (정상 압입과 구분 · HND-03) · '
                                                                            'NEGATIVE_POROSITY = 구 부피 합 porosity < 0 (= 구 부피 합 φ_SE + φ_AM > 1 · 겹침이 큰 침대 · HND-04 · LHS-15) — '
                                                                            '배포 porosity (정확 union) 는 이 경우에도 양수다 · 여러 개면 | 로 잇는다'),
    ('phi_sum_gt_one',       ('handover_qc', 'phi_sum_gt_one'),             'phi_se + phi_am > 1'),
    #  ── τ 밴드 진단 (LHS-08 · Codex §8-3) — 보고 τ 는 여전히 보류 열 ──
    ('tau_n_bot',            ('tau_detail', 'band_detail', 'n_bot'),        'solid_zrange 아래 밴드의 SE 인원'),
    ('tau_n_top',            ('tau_detail', 'band_detail', 'n_top'),        'solid_zrange 위 밴드의 SE 인원'),
    ('tau_wall_n_bot',       ('tau_detail', 'band_detail', 'wall_n_bot'),   '벽 (z = 0) 기준 아래 밴드의 SE 인원 (진단)'),
    ('tau_wall_n_top',       ('tau_detail', 'band_detail', 'wall_n_top'),   '플래튼 기준 위 밴드의 SE 인원 (진단)'),
    ('tau_wall_n_span_components', ('tau_detail', 'band_detail', 'wall_n_span_components'), '벽 밴드 둘을 잇는 SE 성분 수 (진단)'),
    #  ── 프로비넌스 ──
    ('measurement_protocol_id', ('handover_qc', 'measurement_protocol_id'), '측정 규약 ID'),
    ('boundary_model_id',    ('handover_qc', 'boundary_model_id'),          '경계 모델 ID (바닥 primitive 의 물성 type · 플래튼 메시)'),
    ('scale_sim_per_um',     ('handover_qc', 'scale_sim_per_um'),           'sim 단위 / µm'),
    ('deck_floor_z_sim',     ('deck_floor', 'z'),                           '덱에서 읽은 활성 바닥 벽 z'),
    ('deck_wall_type',       ('handover_qc', 'deck_wall_type'),             '바닥 벽의 물성 type (LHS: SE)'),
    ('contact_sha256',       ('handover_qc', 'contact_sha256'),             '원자료 추적'),
    ('deck_sha256',          ('handover_qc', 'deck_sha256'),                '원자료 추적'),
    ('mesh_sha256',          ('handover_qc', 'mesh_sha256'),                '원자료 추적'),
)


#: J19 (1저자 비준 2026-09-28 — docs/reviews/pure_se_union_prereg_20260927.md §6-2 · lhs_handover_judgments_20260924.md J19) —
#:   겹침 보정 porosity 를 **병기**한다.  구 부피 합 열 (`porosity_sphere_pct_RECORD_ONLY`) 은 J1 대로 **그대로** 남는다 — 교체가 아니다
#:   (CLAUDE.md porosity 규약 · 생산 코퍼스가 그 규약을 공유한다).  ⛔ φ_SE · φ_AM 의 union 판은 **넣지 않는다** (AM–SE 겹침 배분 = 별도 저자
#:   결정) · 물리 타깃 적격성 (`physical_target_status`) 도 **안 바꾼다** (§6-2 비준 범위 밖).
#:   ↪ J20-e (1저자 09-29 밤 "φ 는 (라) 만"): 겹침 배분이 필요 없는 **질량 보존 φ** 두 열을 넣는다 (인계 두께 · union porosity 와 같은 장부) —
#:     union 점유 φ ((가)~(다) · 겹침 배분) 는 여전히 넣지 않는다.
DEFAULT_UNION_TSV = 'docs/data/lhs_union_20260927/lhs130_union.tsv'
#: SE-rich 문턱 (SE / 고체, 구 부피) — ⚠ 등록된 정의가 없어 선례를 따른 **도구 선택**이다 (저자 확인 항목):
#:   CLAUDE.md 신뢰성 regime map *"SE-rich (SE/sol ≳ 50 %) → DEM ε_sphere 과압축"* · union README *"음수 ε_sphere 는 SE/고체 0.5–0.6 칸부터"*.
#:   연속값 `se_of_solid_vol` 을 함께 내므로 받는 쪽이 문턱을 바꿀 수 있다.
SE_RICH_MIN = 0.50
#: union 행 ↔ 수확 짝 검사 허용치 — union README 실측 최대 차: 구 부피 합 5.6e-14 %p · 두께 0 µm
UNION_TOL = {'eps_sphere_pct': 1e-9, 'thickness_um': 1e-6}
#: J20-e — 질량 보존 φ 닫힘 (φ_SE + φ_AM + ε_union = 1) 허용치.  식으로는 정확하다 — 넘으면 DESC-07 (φ 둘 ↔ ε_sphere) 이 깨진 것이다.
PHI_MC_CLOSURE_TOL = 1e-9
HANDOVER_UNION = (
    ('porosity_union_exact_pct',        'mc_void_pct',
     '★ 겹침 보정 porosity (정확 union — 상자 [0,Lx)×[0,Ly)×[0,plate_z) 무작위 점 · 세 입자 이상 겹침까지) — 물리 porosity 열 (J19)'),
    ('porosity_union_exact_se_pct',     'mc_void_se_pct',         '위 값의 통계 오차 (1σ, %p)'),
    ('porosity_union_pair_clipped_pct', 'eps_union_pair_clipped', '검산 — 웹앱 쌍 렌즈 union − 벽 밖 부피 (세 입자 겹침 무시 · 상한)'),
    ('union_pair_upper_bound_ok',       'pair_upper_bound_ok',
     '쌍 렌즈 ≥ 정확 — False 면 접촉 덤프에 겹친 쌍이 빠졌다 (정확 union 은 원자만 써서 그래도 유효)'),
    ('se_of_solid_vol',                 'se_of_solid_vol',        'SE / 고체 (구 부피) — SE-rich 표지의 연속값'),
)
#: 유도 열 (union 행 + 수확에서 계산)
HANDOVER_UNION_DERIVED = (
    ('thickness_mass_conserving_um',
     '질량 보존 두께 = 두께 × (1 − ε_sphere)/(1 − ε_union) — union 을 실제 공극률로 받을 때 **같은 고체**의 두께 (DEM 에서 겹친 부피는 사라지므로 '
     'union 과 DEM 간격 두께를 둘 다 실제 값으로 받을 수 없다)'),
    ('se_rich', f'SE / 고체 ≥ {SE_RICH_MIN} (구 부피 합이 겹침 이중계상으로 퇴화하는 영역 — 문턱은 도구 선택, 연속값 옆 열)'),
    ('phi_se_mass_conserving',
     '★ 인계용 SE 부피분율 (J20-e (라) · 1저자 09-29 밤) — 질량 보존 φ = phi_se × (1 − ε_union)/(1 − ε_sphere) '
     '= SE 구 부피 / (L² · thickness_mass_conserving_um) = (1 − porosity_union_exact_pct/100) × se_of_solid_vol.  '
     '인계 두께 · union porosity 와 **같은 장부**: φ_SE + φ_AM + ε_union = 1 (정확) · φ × 인계 두께 = 레시피 적재량.  '
     '유도량 (두께 · 레시피로 정해짐 — 독립 측정 아님) · union 과 같은 상한 규약의 짝 (소성으로 밀려난 재료를 빈틈이 아니라 두께로 보낸다)'),
    ('phi_am_mass_conserving',
     '인계용 AM 부피분율 (J20-e (라)) — 같은 규약 = (1 − porosity_union_exact_pct/100) × (1 − se_of_solid_vol)'),
)


#: J20 (1저자 비준 2026-09-28 "벽 기준 τ 새 열") — 수확 v3 의 `tau_wall_detail` 을 **새 열**로 싣는다.  옛 τ (solid_zrange) 는
#:   HANDOVER_HELD_BACK 그대로 (LHS-08).  값 칸은 status OK 일 때만 (계약 ②) — 미관통을 0 이나 큰 수로 채우지 않는다.
#:   규약 문자열은 수확기 `lhs_descriptor_harvest.TAU_WALL_CONVENTION` 과 같아야 한다 (selftest ⑲n 이 둘을 맞댄다).
TAU_WALL_CONVENTION = 'harvest_v3/wall_z0_plate/rSEmax/no_fallback/same_component'
HANDOVER_TAU_WALL = (
    ('tortuosity_SE_wall',        'tau_mean',
     '★ SE τ (벽 규약 · **기하 최단경로**) — 바닥 벽 (z = 0) 밴드와 플래튼 밴드 (밴드 두께 = r_SE,max · 입자 표면 기준) 를 **같은 SE 성분 '
     '안에서** 잇는 쌍의 SE 중심 경로 최단 길이 (Dijkstra · 가중 = 중심 거리 · x·y 주기) / 두 끝 중심의 z 거리 · 무작위 200 쌍 (seed 42 · '
     '쌍 평균이라 쌍이 많은 큰 성분 쪽으로 가중) · [1, 20) 절단 평균.  접촉 = 원자 좌표 기하 (d ≤ r_i + r_j) — 덤프 접촉과 같은 집합 (J20-a '
     '130/130).  status OK 일 때만 값 · 비관통은 빈칸 (N/A · 0 이 아니다).  ⚠ **수송 τ 가 아니다** — 협착 · 단면 병목을 보지 않아 1 근처에 '
     '모인다 (LHS 1.29–4.15 · lhsx 1.26–1.60) · 수송 굴곡도는 망 단계의 tau2 = φ_SE·σ₀/σ_full (tortuosity factor · τ_Laplace,eff = √tau2 · 이 표에 없음 · τ 명명 규약 10-03 · TAU-01) · '
     '관문 T1–T3 (10-01)'),
    ('tortuosity_SE_wall_median', 'tau_median',     '같은 표본의 중앙값 (status OK 일 때만) · 같은 한정어 (기하 최단경로 · 수송 τ 아님)'),
    ('tortuosity_SE_wall_status', 'status',
     'OK · NOT_PERCOLATING (벽 밴드 둘을 잇는 SE 성분이 없다 = 미관통 — 퍼콜레이션 percolation_pct 0 과 같은 집합 · 관문 T3) · '
     'ELECTRODE_BAND_EMPTY · NO_VALID_SAMPLED_PAIR · N_A_PHASE_ABSENT'),
    ('tau_wall_n_sampled',        'n_sampled',      '표본 쌍 수 (최대 200)'),
    ('tau_wall_n_valid',          'n_valid',        '경로가 난 표본 수'),
    ('tau_wall_n_truncated',      'n_truncated',    '[1, 20) 밖으로 잘린 수'),
    ('tau_wall_convention',       'tau_convention', '규약 문자열 (harvest_v3/wall_z0_plate/…)'),
)
TAU_WALL_VALUE = ('tortuosity_SE_wall', 'tortuosity_SE_wall_median')
#: v1.1 ③ (1저자 비준 10-01 *"비준이야"* · J20-o) — 가장 큰 SE 덩어리 (수확 v3 `tau_detail.band_detail` · 벽 τ 와 같은 SE 그래프 ·
#:   `lhs_descriptor_harvest.tortuosity_se`).  비관통 24 침대의 "관통에 얼마나 가까웠나" 연속 디스크립터 — 관통 침대에도 값이 있다 (≈ 1).
#:   수확기 원값의 분모는 **전 입자 (AM 포함) z 범위** 라 바닥 아래로 샌 입자에 끌린다 (벽 간격보다 3–20 % 큼 · LHS 중앙 7 %) →
#:   기록된 z_lo · z_hi · plate_z 로 벽 간격 기준 값을 **정확히** 환산한다 (수확기 재실행 없음).
HANDOVER_SE_CLUSTER = (
    ('se_largest_comp_frac',
     '★ 가장 큰 SE 덩어리 (SE 수 기준 가장 큰 연결 성분 · 원자 좌표 기하 접촉 d ≤ r_i + r_j · x·y 주기 — 벽 τ 와 같은 그래프) 에 든 SE 의 '
     '비율 (0–1) = 그 성분의 SE 수 / 전 SE (v1.1 ③ · 1저자 비준 10-01) · 관통 침대는 1 근처 (LHS 중앙 0.997) · 비관통 침대 0.002–0.91 · '
     '관문 C1 (× N_SE = 정수 개수 · N_SE = 수확 phase_counts)'),
    ('se_largest_comp_wall_span_frac',
     '★ 그 덩어리의 두께 방향 폭 / 벽 간격 (v1.1 ③) — 폭 = 덩어리 SE 의 max(z + r) − min(z − r) (입자 표면 기준) · 벽 간격 = 플래튼 plate_z − '
     '바닥 z 0 · 수확 기록값으로 정확히 환산 (= 수확 원값 × 전 입자 z 범위 / 벽 간격 · 재실행 없음) · 표면이 벽 · 플래튼과 겹쳐 1 을 넘을 수 '
     '있다 (관통 침대 LHS 1.01–1.05 · lhsx 1.02–1.06) · 비관통 침대 0.11–0.96 · ⚠ SE 수로 **가장 큰** 덩어리의 폭 — 가장 멀리 뻗은 덩어리가 '
     '아닐 수 있다 · 관문 C3 (플래튼 = 수확 plate_z_sim · 바닥 = z_floor_sim)'),
    ('se_largest_comp_env_span_frac',
     '참고 (내부) — 수확기 원값 largest_comp_z_span_frac: 같은 폭 / **전 입자 (AM 포함) z 범위** max(z + r) − min(z − r) · ⚠ 분모가 바닥 '
     '아래로 샌 입자 · 벽과 겹친 입자에 끌려 벽 간격보다 3–20 % 크다 (LHS 중앙 7 %) → 침대마다 다르게 작아진다 · 인계는 '
     'se_largest_comp_wall_span_frac 을 쓴다 · 관문 C2 (≤ 1 — 덩어리 ⊂ 전 입자)'),
)


def _se_cluster_cols(case, h):
    """v1.1 ③ 값 + 관문 (fail-closed) — 수확 `tau_detail.band_detail` 의 가장 큰 SE 덩어리 기록이 **이 침대의 SE · 이 판**의 것인가.

      C1 SE 수: band n_se = 수확 phase_counts SE (정수 > 0) · 0 < 비율 ≤ 1 · 비율 × n_se = 정수 개수
      C2 z 폭: 0 < 전 입자 z 범위 대비 폭 ≤ 1 (덩어리 ⊂ 전 입자) · z_hi > z_lo
      C3 벽 간격: band 플래튼 = 수확 plate_z_sim · 바닥 = z_floor_sim (있으면) · 플래튼 > 바닥
    반환 {열: 값 문자열}.  어긋나면 `FillRefusal` (메시지에 'v1.1 C<n>')."""
    def _int(x):
        return isinstance(x, int) and not isinstance(x, bool)

    def _num(x):
        return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)
    b = _dig(h, ('tau_detail', 'band_detail')) or {}
    pc = h.get('phase_counts')
    if not isinstance(pc, dict):
        raise FillRefusal(f'{case}: 수확 JSON 에 phase_counts 가 없다 — SE 수를 몰라 가장 큰 SE 덩어리를 확인할 수 없다 (v1.1 C1)')
    n_se, fr, zs = b.get('n_se'), b.get('largest_comp_frac'), b.get('largest_comp_z_span_frac')
    if not (_int(n_se) and n_se > 0 and n_se == _phase_n(pc, 'SE')):
        raise FillRefusal(f'{case}: 덩어리 기록의 SE 수 {n_se!r} ≠ 수확 phase_counts SE {_phase_n(pc, "SE")} — 다른 침대 · 다른 SE 집합이다 (v1.1 C1)')
    if not (_num(fr) and 0.0 < fr <= 1.0):
        raise FillRefusal(f'{case}: largest_comp_frac {fr!r} ∉ (0, 1] (v1.1 C1)')
    x = fr * n_se
    if abs(x - round(x)) > WA_COUNT_INT_TOL:
        raise FillRefusal(f'{case}: largest_comp_frac {fr!r} × SE {n_se} = {x!r} 이 정수 개수가 아니다 (v1.1 C1)')
    zlo, zhi, pz, fl = b.get('z_lo'), b.get('z_hi'), b.get('alt_plate_z'), b.get('wall_z_floor')
    if not (_num(zs) and 0.0 < zs <= 1.0 + 1e-12):
        raise FillRefusal(f'{case}: largest_comp_z_span_frac {zs!r} ∉ (0, 1] — 덩어리는 전 입자의 부분집합이다 (v1.1 C2)')
    if not (_num(zlo) and _num(zhi) and zhi > zlo):
        raise FillRefusal(f'{case}: 전 입자 z 범위 z_lo {zlo!r} · z_hi {zhi!r} 가 없거나 뒤집혔다 (v1.1 C2)')
    zf = h.get('z_floor_sim')
    if not (_num(pz) and pz == h.get('plate_z_sim') and _num(fl) and (zf is None or fl == zf) and pz > fl):
        raise FillRefusal(f'{case}: 덩어리 기록의 벽 간격 (플래튼 {pz!r} · 바닥 {fl!r}) ≠ 수확 plate_z_sim {h.get("plate_z_sim")!r} · '
                          f'z_floor_sim {zf!r} — 다른 판이다 (v1.1 C3)')
    return {'se_largest_comp_frac': repr(float(fr)),
            'se_largest_comp_wall_span_frac': repr(zs * (zhi - zlo) / (pz - fl)),
            'se_largest_comp_env_span_frac': repr(float(zs))}
#: 벽 τ 관문 상수 — 수확기 (`lhs_descriptor_harvest.TAU_LO · TAU_HI · N_TAU_PAIRS`) 와 같아야 한다 (selftest ㉓ 가 강제)
TAU_WALL_LO, TAU_WALL_HI, TAU_WALL_N_PAIRS = 1.0, 20.0, 200


def _tau_wall_gates(case, t, h):
    """벽 τ 관문 (fail-closed · 1저자 10-01 *"dijkstra tortuosity 벽을 확실하게 닫고 값을 추출"*) — 상태 ↔ 값 ↔ 표본 수 ↔ 관통 성분 수가
    **한 표본**에서 나왔는가.  10-01 실측 130/130 · 64/64 성립.

      T1 관통: n_span_components = 0 이상 정수 · OK ⟹ > 0 · NOT_PERCOLATING ⟹ 0 · 수확 `tau_detail.band_detail.wall_n_span_components` 가
         있으면 같아야 (같은 성분 · 같은 벽 밴드)
      T2 값 · 표본: OK ⟹ 평균 · 중앙값 ∈ [1, 20) · 0 < n_valid ≤ n_sampled ≤ 200 · 0 ≤ n_truncated < n_valid
      (T3 — 웹앱 percolation_pct 가 함께 실리면 NOT_PERCOLATING ⟺ percolation_pct = 0 — `build_handover` 가 행 끝에서 본다)
    반환 1.  어긋나면 `FillRefusal` (메시지에 'τ T<n>')."""
    def _int(x):
        return isinstance(x, int) and not isinstance(x, bool)

    def _num(x):
        return isinstance(x, (int, float)) and not isinstance(x, bool)
    st, nsc = t.get('status'), t.get('n_span_components')
    if not (_int(nsc) and nsc >= 0):
        raise FillRefusal(f'{case}: 벽 τ n_span_components {nsc!r} 가 0 이상 정수가 아니다 (τ T1)')
    span = _dig(h, ('tau_detail', 'band_detail', 'wall_n_span_components'))
    if span is not None and int(span) != nsc:
        raise FillRefusal(f'{case}: 벽 τ 관통 성분 {nsc} ≠ 수확 벽 밴드 진단 {span} — 같은 성분 · 같은 밴드가 아니다 (τ T1)')
    if (st == 'OK' and nsc <= 0) or (st == 'NOT_PERCOLATING' and nsc != 0):
        raise FillRefusal(f'{case}: 벽 τ 상태 {st} 인데 관통 성분 {nsc} (τ T1)')
    if st == 'OK':
        v, m = t.get('tau_mean'), t.get('tau_median')
        if not (_num(v) and _num(m) and TAU_WALL_LO <= v < TAU_WALL_HI and TAU_WALL_LO <= m < TAU_WALL_HI):
            raise FillRefusal(f'{case}: 벽 τ 평균 {v!r} · 중앙값 {m!r} 이 [1, 20) 밖 (τ T2)')
        ns_, nv, ntr = t.get('n_sampled'), t.get('n_valid'), t.get('n_truncated')
        if not (_int(ns_) and _int(nv) and _int(ntr) and 0 < nv <= ns_ <= TAU_WALL_N_PAIRS and 0 <= ntr < nv):
            raise FillRefusal(f'{case}: 벽 τ 표본 수 n_sampled {ns_!r} · n_valid {nv!r} · n_truncated {ntr!r} 가 규칙 밖 (τ T2)')
    return 1

#: J20 (1저자 비준 2026-09-28 "✅ 만 이번에" · "채운 뒤 넘김") — 웹앱 파이프라인을 **그대로** 돌린 열 (`scripts/lhs_webapp_batch.py`) 중
#:   09-19 전수 판정 (`docs/param_audit_report_20260919.md` §2) 이 ✅ 로 판정한 열만 싣는다 ('✅ 쓴다' · '✅ 쓴다(이름 주의)').
#:   ⛔ 🔶 (σ · fallback · τ(웹앱 폴백) · MPM · Stage E · 피복 문턱) · 🔧 (Physics) 는 **싣지 않는다**.  이름은 코퍼스 (case_master) 그대로.
DEFAULT_CENSUS_TSV = 'docs/data/case_master_column_census_20260919.tsv'
#: 같은 프레임 관문 (%p) — 웹앱 porosity (`dem_analysis_core.calc_porosity`, ε_sphere) 와 수확 구 부피 합 porosity 의 차.
#:   같은 식 · 같은 step 메시면 ~1e-13 (J15 · J16 교차검사 5.6e-14 %p) · 이른 메시 (다른 프레임) 면 수 %p 이상 (LHS-11).
#:   ⇒ 0.05 %p 는 "같은 프레임인가" 의 판별선이지 물리 허용오차가 아니다.
WA_SAME_FRAME_TOL_PCT = 0.05
WA_OK_STATUS = ('done', 'partial')      # partial = 선택 단계만 실패 (예: Stage E) — 필수 단계는 성공
WA_ROW_COLS = (
    ('wa_status',        '웹앱 배치 상태 — done · partial (선택 단계 실패) · failed · REFUSED (같은 프레임 · type_map 관문 거부) — '
                         'done · partial 이 아니면 웹앱 열은 빈칸'),
    ('wa_failed_stages', '실패한 파이프라인 단계 (| 로 이음)'),
    ('wa_mono_phase_name_webapp', 'mono (2-type) 침대에서 웹앱이 단일 AM 에 붙인 반지름 이름 (AM_P · AM_S — type_map_resolve · r > 4 µm) · '
                                  '설계 block 의 상과 다르면 상별 웹앱 열의 값을 설계 이름 칸으로 옮겨 실었다 (J20-k (B) · 130 의 5 · 64 의 4) · '
                                  'bimodal 은 빈칸'),
)
WA_QC = (
    ('qc_wa_porosity_minus_harvest_pct', 'porosity', 'porosity_sphere_pct_RECORD_ONLY',
     '같은 프레임 관문 — 웹앱 porosity (ε_sphere) − 수확 porosity (%p).  |값| > 0.05 면 인계표 생성 자체를 거부한다'),
    ('qc_wa_cov_AM_P_minus_harvest_pct', 'coverage_AM_P_mean', 'coverage_AM_P_hertz_pct',
     '검산 — 웹앱 coverage_AM_P_mean − 수확 coverage_AM_P_hertz_pct (%p).  같은 c_cpl[22] 채널 (A_dem_geometric)'),
    ('qc_wa_cov_AM_S_minus_harvest_pct', 'coverage_AM_S_mean', 'coverage_AM_S_hertz_pct',
     '검산 — 웹앱 coverage_AM_S_mean − 수확 coverage_AM_S_hertz_pct (%p)'),
)
#: 넘길 때 **이름을 고쳐 설명**해야 하는 열 (L1-04) — 코퍼스 이름은 frozen 이라 열 이름은 안 바꾼다.
CAVEAT_NAME = ('A_dem_geometric — LIGGGHTS 기하 교차 원판 π(rδ − δ²/4) 이지 Hertz 탄성 πR*δ 가 아니다 '
               '(같은 반경 비 = 2 − δ/2r ≈ 1.99배) · L1-04')
CAVEAT_FRAC_DELTA = 'δ-based 파괴 분류 — force-based 열 (_force_) 과 같은 표에 나란히 인용 금지 (분류 규칙이 다르다) · force-based 권장'
CAVEAT_FRAC_FORCE = 'force-based 파괴 분류 (Auerbach — 권장) · δ-based 열과 같은 표에 나란히 인용 금지'
HANDOVER_VALUE_MEANING = {
    'phi_se': ('SE 부피분율 — 명목 구 부피 합 / (L² · 플래튼−바닥 간격) (장부값, 겹침 이중계상 포함 · 정본 이름 phi_se_spheresum_nominal_gap) · '
               '⚠ 내부 기록 — union porosity 와 닫히지 않는다 (분모가 인계 두께가 아니다) · 인계용은 phi_se_mass_conserving (J20-e)'),
    'phi_am': 'AM 부피분율 — 같은 규약 · ⚠ 내부 기록 · 인계용은 phi_am_mass_conserving (J20-e)',
    'coverage_AM_P_hertz_pct': 'AM_P 표면 피복률 (%) — 접촉 면적 c_cpl[22] 합 / 표면적, 입자 평균 · 이름의 hertz 는 물려받은 오해 (A_dem_geometric · L1-04)',
    'coverage_AM_S_hertz_pct': 'AM_S 표면 피복률 (%) — 같은 채널',
    'coverage_AM_total_hertz_pct': 'AM 전체 피복률 (%) — 위 둘에서 유도 (독립 타깃 아님)',
    'porosity_sphere_pct_RECORD_ONLY': 'ε_sphere 공극률 (%) — 1 − phi_se − phi_am (기록 전용 · 물리 공극률은 porosity_union_exact_pct)',
}


#: J20-a ⓒ (1저자 비준 09-28 밤 "권고하는걸로") — 접촉 위상 열의 **정의**.  09-19 판정의 why ("cap 선택과 무관 Δ = 0 %") 는 좁은 검사
#:   결과이지 뜻이 아니다.  공통: 접촉 = LIGGGHTS pair/gran/local 덤프의 **행** (벽 · 플래튼 접촉은 없다 · x·y 주기 경계를 넘는 접촉은
#:   c_cpl[9] 플래그와 함께 들어 있다 — `scripts/lhs_contact_audit.py` 가 원자 좌표 최소영상 재계수와 쌍 단위로 맞댄다) · CN = 그 상
#:   **전 입자**로 나눈 평균 (접촉 0 · 벽 · 플래튼에 닿은 입자 포함) — `scripts/dem_analysis_core.py`.
CAVEAT_WALL = ('벽 효과 (정의상 — 결함 아님): 바닥 벽 · 플래튼에 닿은 입자는 그쪽에 이웃이 없어 CN 이 낮다 · 설계 d/T AM_P 0.10–0.52 '
               '(두께가 AM_P 2–10 개) ⇒ 두께에 따라 체계적 — wall_touch_frac_* 열과 함께 쓸 것')
CAVEAT_DERIVED_NUM = ('파생 — (N_P·CN_P + N_S·CN_S)/(N_P + N_S) 항등식: AM_P_se_cn_mean · AM_S_se_cn_mean · 상별 입자 수로 정해진다 '
                      '(독립 타깃 아님 · DESC-07 과 같은 부류)')
CAVEAT_DERIVED_SW = ('파생 — 상별 반경이 한 값이면 (N_P r_P² CN_P + N_S r_S² CN_S)/(N_P r_P² + N_S r_S²) 항등식 · r² 가중이라 '
                     'AM_P 가 지배 → 벽 효과가 크다')
CAVEAT_PERC = ('경계 = 바닥 벽 z 0 · 플래튼 plate_z 기준 2·r 밴드 (L0) — LHS 130/130 폴백 0 (J20-b 감사) · 폴백 (L1 · L2) 이 나면 같은 이름이 다른 '
               '정의가 되는데 기록이 없다 (LHS-17 · 생산 코드에서 열림) · 두께 < 4r 이면 두 밴드 겹침 인공물 (LHS-18 · LHS 기하상 0) · '
               '수확기 벽 밴드 관통 (tau_wall_n_span_components > 0) 과 같은 집합 (관문 P1)')
CAVEAT_COUNT = ('총량 (개수) — 두께 · 입자 수에 비례한다 · 특징으로 쓰려면 입자당 · 부피당으로 나눌 것 · 면적이 아니다 '
                '(A_dem_geometric 주의는 해당 없음)')
#: ⑤⑥⑦ 한정어 (J20-s · 열 사전 문구 — 정본 = 판정 J20-s 표)
CAVEAT_F1 = ('h = 10 nm (H_SPREAD_REAL_M · 확대 배율 반영) 는 **출처 없는 모델 상수** ("2 × h_film_min") — 감도 기술자로만 · SE–SE 만 · '
             '반올림 쌍 (덤프 %g · 접촉 감사 v2 의 114 쌍 / 130 침대) 이 탄성 CN 과 겹쳐 셀 수 있음 (무시 가능 수준) · ' + CAVEAT_WALL)
CAVEAT_LHS31 = ('LHS-31 한정: ① 마지막 프레임 힘 (압축 중 최대 아님 → 손상 **하한**) ② 벽 · 판 접촉 제외 (판에 닿은 AM_P 의 최대 하중 빠짐) '
                '③ R_min 선택 (R* 이면 P_c 절반) ④ K_IC_P 0.3 = 소결 펠릿값 (정본 카드 xu2017 — 이차입자 0.102 의 3 배) · K_IC_S 1.0 측정 근거 '
                '없음 — P_c ∝ K_IC² ⑤ A 200 · 배수 원전 (Lawn Table 3.4) 카드 없음 [미확인] ⑥ δ 판 열과 나란히 인용 금지')
CAVEAT_FRAC_AUERBACH = CAVEAT_FRAC_FORCE + ' · ' + CAVEAT_LHS31
CAVEAT_AREA_TOTAL = CAVEAT_NAME + ' · 총량 (µm²) — 두께 · 입자 수에 비례한다 · 특징으로 쓰려면 입자당 · 부피당으로 나눌 것'
WA_DEFINE = {
    'se_se_cn': ('z_SE-SE — SE 1 개당 SE 접촉 수, SE 전 입자 평균 (접촉 0 · 벽 · 플래튼에 닿은 입자 포함)', CAVEAT_WALL),
    'se_se_cn_std': ('z_SE-SE 의 입자간 표준편차 (모집단 · SE 전 입자)', CAVEAT_WALL),
    'am_se_cn_mean': ('z_AM-SE — AM 1 개당 SE 접촉 수, AM 전 입자 (AM_P + AM_S) 의 개수 가중 평균',
                      CAVEAT_DERIVED_NUM + ' · ' + CAVEAT_WALL),
    'am_se_cn_surface_weighted': ('Σ r²·CN_AM-SE / Σ r² (AM 전 입자) — 표면적 가중 AM–SE CN', CAVEAT_DERIVED_SW),
    'am_am_cn': ('z_AM-AM — AM 1 개당 AM 접촉 수 (AM_P–AM_S 교차 포함), AM 전 입자 평균', CAVEAT_WALL),
    'am_am_cn_std': ('z_AM-AM 의 입자간 표준편차 (모집단)', CAVEAT_WALL),
    'am_am_n_contacts': ('AM–AM 접촉 개수', CAVEAT_COUNT),
    #  7c (J20-k · 1저자 비준 10-01) — 고립 비율 · 전체 AM–SE 분포 (7a 새 키)
    'am_vulnerable_pct': ('AM 고립 **위험** 비율 (%) (취약 AM) — SE 접촉이 0–1 개인 AM 의 비율, AM 전 입자 (AM_P + AM_S) · 접촉 개수 기준 '
                          '(coverage 문턱이 아니다 — 09-19 census 의 COND_cov 는 오분류 · LHS-23) · ⚠ 경로 기준 고립 (이온이 못 가는 AM) 이 아니다 — '
                          '그것은 100 − ionic_active_pct (1저자 10-01 질문)', CAVEAT_WALL),
    'am_se_cn_std': ('z_AM-SE 의 입자간 표준편차 (모집단) — AM 전 입자 (접촉 0 · 벽 입자 포함) · mono = 단일 상 값 (J20-k 7a)', CAVEAT_WALL),
    'am_se_cn_median': ('z_AM-SE 의 중앙값 — AM 전 입자 (짝수 개면 가운데 둘의 평균 · np.median) · mono = 단일 상 값 (J20-k 7a)', CAVEAT_WALL),
    'am_se_cn_max': ('z_AM-SE 의 최댓값 — AM 전 입자 · = 상별 max 의 최댓값 (J20-k 7a)', CAVEAT_WALL),
    #  ② 퍼콜레이션 (J20-b · F3 = LHS-19 · 열 이름과 뜻이 다른 곳을 적는다)
    'percolation_pct': ('SE 관통 비율 (%) — 바닥 밴드 (z ≤ 2r) 와 위 밴드 (z ≥ plate_z − 2r) 에 다 닿는 SE 성분의 SE / 전 SE · 0.0 = 관통 성분 없음 '
                        '(진짜 미퍼콜 · J20-b) · **밴드 규칙의 그래프 관통** — 솔버 (전류) 관통 · σ 와 다른 정의 (LHS-19)', CAVEAT_PERC),
    'top_reachable_pct': ('위 밴드에 닿는 SE 성분의 SE / 전 SE (%) — 위 밴드에 앉은 외톨이 SE 도 센다 (LHS-19) · SE 그래프 양 (coverage 무관 — LHS-20)',
                          CAVEAT_PERC),
    'n_components': ('SE 접촉 그래프의 성분 수 — 외톨이 SE (크기 1) 포함 → 단절 침대에서는 사실상 외톨이 수 (LHS-06 · LHS-19)', CAVEAT_COUNT),
    'n_large_components': ('크기 ≥ 10 인 SE 성분 수 — 문턱 10 은 출처 없는 코드 상수 (LHS-19)', CAVEAT_COUNT),
    'ionic_active_pct': ('이온 활성 AM 비율 (%) — 위 밴드 (분리막 쪽) 에 닿는 SE 성분 (top-reachable) 의 SE 와 접촉한 AM / 전 AM (calc_ionic_active_am) · '
                         '**100 − 이 값 = 경로 기준 고립 AM** (SE 무접촉 + 닿은 SE 가 위로 안 이어짐) · 접촉 유무만 '
                         '본다 (coverage 무관 — LHS-20) · 외톨이 SE 가 위 밴드에 있으면 그것도 센다 (LHS-19)', CAVEAT_PERC),
    #  v1.1 ② (1저자 비준 10-01) — 경로 기준 고립 (= 100 − ionic_active_pct) 의 분해
    'ionic_dead_pct': ('경로 기준 고립 중 **단절** 비율 (%) (v1.1 ②) — SE 와 닿았지만 닿은 SE 가 전부 위 밴드 (분리막 쪽) 로 안 이어지는 AM / 전 AM '
                       '(calc_ionic_active_am 의 dead) · SE 망이 끊긴 문제 (접촉을 늘려도 안 풀린다)', CAVEAT_PERC),
    'ionic_no_se_pct': ('경로 기준 고립 중 **무접촉** 비율 (%) (v1.1 ②) — SE 접촉 0 인 AM / 전 AM (calc_ionic_active_am 의 no_se) · 고립 위험 '
                        '(SE 접촉 0–1 개) 의 부분집합 (관문 D5) · 계면 형성 문제', CAVEAT_WALL),
    'se_se_cn_perc': ('관통 SE 성분에 속한 SE 만의 평균 SE–SE CN — 관통 성분이 없으면 빈칸 (N/A · 키 자체가 없다 · LHS-19)', CAVEAT_WALL),
    'se_se_cn_n_perc': ('관통 SE 성분에 속한 SE 개수 — = percolation_pct × N_SE / 100 (생성기 관문 P3) · 관통 없으면 빈칸 (N/A)', CAVEAT_COUNT),
    'A_binding_AM_SE_n_contacts': ('Physics 모듈 (coverage_physics_vs_hertzian) 이 센 AM–SE 접촉 개수 — area_AM전체_SE_n 과 같은 '
                                   '집합인지는 한 건 대조 전', CAVEAT_COUNT),
    'A_binding_total_n_contacts': ('Physics 모듈이 센 전체 접촉 개수 — 같은 집합인지는 한 건 대조 전', CAVEAT_COUNT),
    'n_am_am_contacts_total': ('파괴 모듈이 센 AM–AM 접촉 개수', CAVEAT_COUNT),
    'n_am_am_contacts_excluded': ('파괴 모듈이 제외한 AM–AM 접촉 개수', CAVEAT_COUNT),
    #  ⑤⑥⑦ (J20-s · 1저자 비준 10-04)
    'se_se_cn_aug': ('F1 근접쌍 CN — 탄성 접촉 (덤프) 에 표면 틈 ≤ h 인 SE–SE 쌍을 더해 센 SE 1 개당 SE 접촉 수, SE 전 입자 평균 · '
                     '= se_se_cn + 2 × se_se_cn_aug_n_extra / N_SE (관문 ⑤F1 · 10-01 실측 130/130 · 64/64 상대차 ≤ 2.2e-16) · J20-s ⑤', CAVEAT_F1),
    'se_se_cn_aug_std': ('F1 근접쌍 CN 의 입자간 표준편차 (모집단 · SE 전 입자) · J20-s ⑤', CAVEAT_F1),
    'se_se_cn_aug_n_extra': ('F1 이 더한 SE–SE 근접쌍 개수 (탄성 접촉이 아닌 쌍 · 쌍 하나 = 두 입자에 하나씩) · J20-s ⑤',
                             CAVEAT_F1 + ' · ' + CAVEAT_COUNT),
    'se_se_cn_aug_h_spread_sim': ('F1 의 틈 문턱 h (sim 길이 = 10 nm × 확대 배율 · LHS 1e-05 전부) · J20-s ⑤', CAVEAT_F1),
    'fracture_index_force': ('Auerbach 힘 기반 파괴 지수 = (파편화 + 분쇄) 개수 / n_total_AM_AM_force (소수 넷째 자리 반올림) — AM–AM 접촉만 · '
                             '단계 = F/P_c 의 배수 1 · 3 · 11 · 32 (P_c = A K_IC² R_min / E*) · J20-s ⑥', CAVEAT_FRAC_AUERBACH),
    'n_total_AM_AM_force': ('힘 기반 분류에 들어간 AM–AM 접촉 수 (법선력 fn > 0) — ≤ am_am_n_contacts (관문 ⑥R3 · 10-01 실측 194/194 같음) · '
                            'J20-s ⑥', CAVEAT_FRAC_AUERBACH + ' · ' + CAVEAT_COUNT),
    'se_se_cn_eff_area': ('SE 표면 중 SE–SE 접촉이 덮은 비율 (무차원) = Σ A_contact (접촉 하나를 두 입자에 하나씩) / Σ 4πr² (SE 전 입자) = '
                          '2 × area_SE_SE_total / (N_SE · 4π r_SE²) (관문 ⑦A4 · SE 단분산 · 10-01 실측 상대차 ≤ 2.2e-12) · J20-s ⑦', CAVEAT_NAME),
    'se_se_cn_eff_area_perc': ('같은 비율 — 관통 SE 성분에 속한 SE 만 · 관통 없으면 빈칸 (N/A · percolation_pct 0 과 같은 집합 — 관문 ⑦A5) · J20-s ⑦',
                               CAVEAT_NAME),
    'am_am_mean_area': ('AM–AM 접촉 하나의 평균 면적 (µm²) = am_am_total_area / am_am_n_contacts (관문 ⑦A3) · J20-s ⑦', CAVEAT_NAME),
    'am_am_total_area': ('AM–AM 접촉 면적 총합 (µm²) = AM_P–AM_P + AM_P–AM_S + AM_S–AM_S 총합 (관문 ⑦A3) · J20-s ⑦', CAVEAT_AREA_TOTAL),
}
_STAT_KO = {'mean': '평균', 'std': '표준편차 (모집단)', 'median': '중앙값', 'max': '최댓값'}


def wa_define(col):
    """J20-a ⓒ — 접촉 위상 열이면 (뜻, 주의), 아니면 None.  열 이름은 코퍼스 (case_master) 그대로."""
    if col in WA_DEFINE:
        return WA_DEFINE[col]
    m = re.fullmatch(r'(AM_P|AM_S)_se_cn_(mean|std|median|max)', col)
    if m:
        ph, st = m.groups()
        return (f'{ph} 1 개당 SE 접촉 수의 {_STAT_KO[st]} — {ph} 전 입자 (접촉 0 · 벽 입자 포함) · 상이 없으면 빈칸 (N/A)',
                CAVEAT_WALL)
    m = re.fullmatch(r'(AM_P|AM_S)_vulnerable_pct', col)
    if m:
        return (f'{m.group(1)} 고립 **위험** 비율 (%) (취약) — SE 접촉이 0–1 개인 {m.group(1)} 의 비율 · 접촉 개수 기준 (coverage 문턱이 아니다 — '
                'LHS-23 · 경로 기준 고립은 ionic_active_pct 쪽) · 상이 없으면 빈칸 (N/A)', CAVEAT_WALL)
    m = WA_IONIC_PHASE_RE.fullmatch(col)
    if m:
        ph, s_ = m.groups()
        ko = {'active': '이온 활성 (위 밴드에 닿는 SE 와 접촉)', 'dead': '단절 (SE 와 닿았지만 위 밴드로 안 이어짐)', 'no_se': '무접촉 (SE 접촉 0)'}[s_]
        return (f'{ph} 의 {ko} 비율 (%) (v1.1 ②) — {ph} 전 입자 기준 · 활성 + 단절 + 무접촉 = 100 (관문 D2) · 상이 없으면 빈칸 (N/A)',
                CAVEAT_PERC if s_ != 'no_se' else CAVEAT_WALL)
    m = re.fullmatch(r'area_(.+)_n', col)
    if m:
        return (f'{m.group(1)} 접촉 개수 (쌍 종류별 덤프 행 수)', CAVEAT_COUNT)
    m = re.fullmatch(r'frac_([a-z]+)_force_pct', col)                       # ⑥ (J20-s)
    if m and m.group(1) in FRAC_STAGES:
        s_ = m.group(1)
        return (f'힘 기반 {FRAC_STAGE_KO[s_]} ({s_}) 단계 비율 (%) = 100 × n_{s_}_force_AM_AM / n_total_AM_AM_force (소수 둘째 자리 반올림 · '
                '다섯 단계 합 ≈ 100 · 관문 ⑥R2) · J20-s ⑥', CAVEAT_FRAC_AUERBACH)
    m = re.fullmatch(r'n_([a-z]+)_force_AM_AM', col)
    if m and m.group(1) in FRAC_STAGES:
        s_ = m.group(1)
        return (f'힘 기반 {FRAC_STAGE_KO[s_]} ({s_}) 단계 AM–AM 접촉 수 — 다섯 단계 합 = n_total_AM_AM_force (관문 ⑥R1) · J20-s ⑥',
                CAVEAT_FRAC_AUERBACH + ' · ' + CAVEAT_COUNT)
    m = WA_AREA_PAIR.fullmatch(col)                                         # ⑦ (J20-s)
    if m:
        a_, b_, st = m.groups()
        pair = f'{a_.replace("AM전체", "AM 전체")}–{b_}'
        if st == 'mean':
            return (f'{pair} 접촉 하나의 평균 면적 (µm²) = 총합 / 개수 (관문 ⑦A1) · 접촉 0 쌍은 빈칸 (N/A — 접촉 0 개에서 평균은 정의되지 '
                    '않는다) · J20-s ⑦', CAVEAT_NAME)
        return (f'{pair} 접촉 면적 총합 (µm²) — 접촉 0 쌍 = 0 (두 상이 다 있으면 측정된 0 · J20-h 와 같은 규칙)'
                + (' · = AM_P–SE + AM_S–SE (관문 ⑦A2)' if a_ == 'AM전체' else '') + ' · J20-s ⑦', CAVEAT_AREA_TOTAL)
    return None


#: 묶음별 채우기 (1저자 09-29 밤 "단독적으로 하나씩 돌려서 표를 채워나갈 거야") — 웹앱 **접촉 분석 단계** (`analyze_contacts.py` ·
#:   bimodal 은 그것을 감싼 `analyze_contacts_bimodal.py`) 가 full_metrics.json 에 쓰는 ① 열.  WA_DEFINE 의 나머지 넷은 뒤 단계 산출이라
#:   접촉 단계만 돈 배치 (`lhs_webapp_batch --stop-after contact`) 에서는 빈칸이 된다 — 이 묶음에 넣지 않는다:
#:   A_binding_AM_SE_n_contacts · A_binding_total_n_contacts (`coverage_physics_vs_hertzian.py`) ·
#:   n_am_am_contacts_total · n_am_am_contacts_excluded (`run_network_fracture_aware.py`).
WA_GROUP_CONTACT_EXACT = ('se_se_cn', 'se_se_cn_std', 'am_se_cn_mean', 'am_se_cn_surface_weighted',
                          'am_am_cn', 'am_am_cn_std', 'am_am_n_contacts',
                          #  7c — calc_am_isolation_risk 의 나머지 출력 (같은 접촉 단계 · analyze_contacts.py:452–468)
                          'am_se_cn_std', 'am_se_cn_median', 'am_se_cn_max', 'am_vulnerable_pct')
#: ② 퍼콜레이션 묶음 (J20-b 감사 · 1저자 비준 10-01 *"퍼콜레이션은 그렇게 가고"*) — **접촉 분석 단계**가 full_metrics 에 쓰는 SE 그래프 열
#:   (`calc_percolation` · `calc_ionic_active_am` · `calc_se_se_cn` 의 관통 부분 · analyze_contacts.py:404–413).  09-29 contact 배치 · 5번 배치 둘 다
#:   130/130 값.  `electronic_active_fraction` 은 **망 단계** (`active_fractions`) 산출이라 접촉 · coverage 배치에 값이 없다 → 이 묶음에 넣지 않는다
#:   (census ✅ 여도 빈칸 = 측정된 N/A 로 읽힌다) · `se_se_cn_eff_area_perc` 는 면적 (⑦ 차례).
WA_GROUP_PERC_EXACT = ('percolation_pct', 'top_reachable_pct', 'n_components', 'n_large_components', 'ionic_active_pct',
                       'se_se_cn_perc', 'se_se_cn_n_perc')
#: v1.1 ② (1저자 비준 10-01) — 경로 기준 고립의 분해: 웹앱 v1.1 이 내보내기 시작한 키 (calc_ionic_active_am 의 dead · no_se · 상별 셋) ·
#:   접촉 분석 단계 산출 · 09-19 census 밖 → 배치 머리에 있을 때만 싣는다 (5번 배치에는 없다 = 열도 없다).
WA_IONIC_DEC_KEYS = (('ionic_dead_pct', 'ionic_no_se_pct')
                     + tuple(f'{ph}_ionic_{s_}_pct' for ph in ('AM_P', 'AM_S') for s_ in ('active', 'dead', 'no_se')))
WA_IONIC_PHASE_RE = re.compile(r'(AM_P|AM_S)_ionic_(active|dead|no_se)_pct')
#: v1.1 ① (1저자 비준 10-01) — 생성기가 **유도**하는 웹앱 열 (재실행 없음).  웹앱 v1.1 도 같은 이름 · 같은 식으로 낸다 — 있으면 같아야 (D1).
WA_DERIVED = (
    ('am_ionic_isolated_pct',
     '★ 경로 기준 고립 AM 비율 (%) (v1.1 ① · 1저자 비준 10-01) = 100 − ionic_active_pct — 이온이 분리막 쪽 (위 밴드) 에서 닿을 수 없는 AM: '
     'SE 무접촉 + 닿은 SE 가 top-reachable 이 아님 (calc_ionic_active_am · 접촉 그래프 · coverage 무관) · ⚠ 고립 위험 (am_vulnerable_pct · '
     'SE 접촉 0–1 개 · 접촉 개수) 과 다른 양 — 접촉이 둘 이상이어도 그 SE 가 끊긴 덩어리면 고립, 하나뿐이어도 이어져 있으면 활성 (예: lhs00_083 '
     '고립 위험 0.1 % · 경로 고립 89 %) · 분해 = ionic_dead_pct + ionic_no_se_pct (v1.1 ② 배치부터) · 생성기가 ionic_active_pct 에서 유도 · '
     '관문 v1.1 D1–D5'),
)
#: 비율 합 = 100 의 부동소수 여유 (%p) — 물리 허용치가 아니다 (개수 / N × 100 의 반올림만)
WA_PCT_SUM_TOL = 1e-7
#: ⑤⑥⑦ (J20-s · 1저자 비준 10-04 *"권고대로"*) — **접촉 분석 단계**가 full_metrics 에 쓰는 열 · 새 계산 없음 (10-01 d1ec42fba 배치 값).
#:   ⑤ F1 근접쌍 CN — calc_se_se_cn 의 F1 출력 (analyze_contacts.py:438–441).
WA_GROUP_F1_EXACT = ('se_se_cn_aug', 'se_se_cn_aug_std', 'se_se_cn_aug_n_extra', 'se_se_cn_aug_h_spread_sim')
#:   ⑥ Auerbach 힘 기반 파괴 — calc_fracture_stages 의 **힘 기반 전체 집계**만 (δ 판 · 상 쌍별은 WA_EXCLUDED).
FRAC_STAGES = ('intact', 'microcrack', 'multicrack', 'fragmentation', 'pulverization')    # fracture_model.ALL_STAGES 와 같은 순서
FRAC_STAGE_KO = {'intact': '무손상', 'microcrack': '미세 균열', 'multicrack': '다중 균열', 'fragmentation': '파편화', 'pulverization': '분쇄'}
WA_GROUP_FRAC_EXACT = (('fracture_index_force', 'n_total_AM_AM_force') + tuple(f'frac_{s}_force_pct' for s in FRAC_STAGES)
                       + tuple(f'n_{s}_force_AM_AM' for s in FRAC_STAGES))
#:   ⑦ 접촉 면적 (A_dem_geometric · c_cpl[22]) — calc_interface_area 의 쌍별 평균 · 총합 + calc_se_se_cn 면적 피복 + calc_am_am_cn 면적.
#:   쌍별 개수 (area_<쌍>_n) 는 ① 접촉 묶음 (J20-g) 그대로.
WA_AREA_PAIR = re.compile(r'area_(AM_P|AM_S|SE|AM전체)_(AM_P|AM_S|SE)_(mean|total)')
WA_GROUP_AREA_EXACT = ('se_se_cn_eff_area', 'se_se_cn_eff_area_perc', 'am_am_mean_area', 'am_am_total_area')
#: ⑤⑥⑦ 근처의 census ✅ 열 중 **인계하지 않는 것** (패턴, 사유) — 묶음 · 검토 여부와 무관하게 먼저 뺀다 (selftest ㉕b · ㉕c).
WA_EXCLUDED = (
    (r'path_hop_area_.*', 'LHS-32 — 덩어리마다 고른 경로 30 개 (best · mean · worst 10) 의 평균 = 선별 표본 통계'),
    (r'frac_[a-z]+_pct|fracture_index|n_[a-z]+_AM_AM|n_total_AM_AM',
     'δ 판 파괴 분류 — 힘 기반 열과 나란히 인용 금지 (09-19 · LHS-31 ⑥) · 힘 기반 (Auerbach) 만 인계'),
    (r'(frac|n)_[a-z]+(_force)?_(AM_P|AM_S)-(AM_P|AM_S)(_pct)?|n_total(_force)?_(AM_P|AM_S)-(AM_P|AM_S)',
     '상 쌍별 파괴 분해 — 접촉 0 쌍에서도 비율 0 % (분모 max(n, 1)) 라 N/A 와 0 을 못 가르고, mono 상 이름 규약 (J20-k (B)) 을 이 열에 '
     '옮기는 관문이 없다 · 전체 집계만 인계'),
    (r'area_.+_physics', 'physics 면적 — coverage 인계는 기하면적만 (J20-m) · 접촉별 추정 면적 합에 표면 한도가 없다 (LHS-25)'),
)
WA_GROUPS = ('contact', 'percolation', 'f1', 'fracture', 'area')
#: 7c — 웹앱 배치 단계 (`lhs_webapp_batch --stop-after`) → 그 배치가 **다 낸** 묶음.  coverage 단계는 접촉 단계를 포함한다 (접촉 분석 → 피복)
#:   — 5번 배치 (`--stop-after coverage`) 를 contact 묶음으로 받는다.  묶음 제한 없이 (전체) 부르면 여전히 거부 (뒤 단계 열이 빈칸).
#:   ② 퍼콜레이션도 접촉 분석 단계 산출이다 (위).
WA_STAGE_GROUPS = {'contact': WA_GROUPS, 'coverage': WA_GROUPS}         # ⑤⑥⑦ 도 접촉 분석 단계 산출 (J20-s)


def wa_group_contact(col):
    """① 접촉 위상 묶음 중 **접촉 분석 단계**가 내는 열인가."""
    return (col in WA_GROUP_CONTACT_EXACT
            or re.fullmatch(r'(AM_P|AM_S)_(se_cn_(mean|std|median|max)|vulnerable_pct)', col) is not None
            or re.fullmatch(r'area_(.+)_n', col) is not None)


def wa_group_perc(col):
    """② 퍼콜레이션 묶음 (접촉 분석 단계의 SE 그래프 열) 인가 — v1.1 ② 분해 키 포함."""
    return col in WA_GROUP_PERC_EXACT or col in WA_IONIC_DEC_KEYS


def wa_group_f1(col):
    """⑤ F1 근접쌍 CN 묶음인가 (J20-s)."""
    return col in WA_GROUP_F1_EXACT


def wa_group_frac(col):
    """⑥ Auerbach 힘 기반 파괴 — 전체 집계 열인가 (J20-s · LHS-31)."""
    return col in WA_GROUP_FRAC_EXACT


def wa_group_area(col):
    """⑦ 접촉 면적 (A_dem_geometric) 묶음인가 — 쌍별 평균 · 총합 · SE 면적 피복 · AM–AM 면적 (J20-s)."""
    return col in WA_GROUP_AREA_EXACT or WA_AREA_PAIR.fullmatch(col) is not None


def wa_excluded(col):
    """⑤⑥⑦ — 인계하지 않는 열이면 사유, 아니면 None (WA_EXCLUDED · J20-s)."""
    for pat, why in WA_EXCLUDED:
        if re.fullmatch(pat, col) is not None:
            return why
    return None


WA_GROUP_FN = {'contact': wa_group_contact, 'percolation': wa_group_perc,
               'f1': wa_group_f1, 'fracture': wa_group_frac, 'area': wa_group_area}


def wa_groups_norm(g):
    """--webapp-groups 값 → 묶음 튜플 ('contact,percolation' · 'contact' · 튜플) · None = 묶음 제한 없음."""
    if g is None:
        return None
    if isinstance(g, str):
        g = [x.strip() for x in g.split(',') if x.strip()]
    return tuple(g)


#: J20-g (1저자 비준 09-30 "권고대로" — *"하나하나씩 쳐내가자"*) — 인계표에는 **1저자와 함수 단위로 같이 확인한 웹앱 열만** 싣는다.
#:   09-19 census ✅ 는 필요조건일 뿐이다.  함수 검토가 하나 끝날 때마다 (열 패턴, 검토 기록) 을 더한다 — 정본 = 체크리스트
#:   `docs/lhs_handover_checklist_20260929.md` §5 함수 검토표 · 판정 J20-g.
WA_REVIEWED = (
    (r'area_(.+)_n', 'calc_interface_area (dem_analysis_core.py:131–168) — 1저자 검토 09-30 · 수정 불요 · J20-g'),
    (r'se_se_cn(_std)?', 'calc_se_se_cn (dem_analysis_core.py:232–344) — 1저자 검토 09-30 · 수정 불요 · 평균 = 2 × area_SE_SE_n / SE '
                         '입자 수 (생성기 관문 · 09-30 실측 130/130 · 64/64 차이 0) · 같은 함수의 _perc · _eff_area · _aug 는 ② · ⑦ · ⑤ 차례 · J20-i'),
    (r'am_am_(cn(_std)?|n_contacts)', 'calc_am_am_cn (dem_analysis_core.py:347–375) — 1저자 검토 09-30 · 수정 불요 · am_am_n_contacts = AM–AM '
                                      '쌍 개수 합 · am_am_cn = 2 × am_am_n_contacts / AM 입자 수 (생성기 관문 · 09-30 실측 130/130 · 64/64 차이 0) · '
                                      'mono 포함 (상별 열 아님) · am_am_mean_area · am_am_total_area 는 ⑦ 차례 · J20-j'),
    (r'am_se_cn_(mean|surface_weighted|std|median|max)|(AM_P|AM_S)_se_cn_(mean|std|median|max)|(am|AM_P|AM_S)_vulnerable_pct',
     'calc_am_isolation_risk (dem_analysis_core.py:781–855) → analyze_contacts.py:452–468 — 1저자 검토 09-30 · 수정 불요 (7a 로 전체 '
     'std · median · max 추가) · 관문 G1–G7 (상별 평균 × 상 입자 수 = area_<상>_SE_n · 전체 평균 × AM 수 = area_AM전체_SE_n · 고립 개수 가중 · '
     'max · median · 합동 std · 표면 가중 = 설계 반경) · 고립 비율 = SE 접촉 0–1 개 (census COND_cov 오분류 → ✅ 승격 · LHS-23) · J20-k 7c'),
    (r'percolation_pct|top_reachable_pct|n_components|n_large_components|ionic_active_pct|se_se_cn_(n_)?perc',
     'calc_percolation (dem_analysis_core.py:451–) · calc_ionic_active_am (:631–) · calc_se_se_cn 관통 부분 (:320–361) → analyze_contacts.py:404–413 — '
     'J20-b 감사 (WSL 130/130 CLEAN · 밴드 L0 130/130 · 폴백 0 · 겹침 0 · 재현 = 정본) · 1저자 비준 10-01 · 관문 P1–P3 (관통 일관 + 수확기 '
     '독립 재현 · 범위 · 관통 SE 개수 = percolation_pct × N_SE) · F3 한정어 (LHS-19) · top_reachable · ionic_active = census 오분류 → ✅ (LHS-20) · J20-b ②'),
    (r'ionic_(dead|no_se)_pct|(AM_P|AM_S)_ionic_(active|dead|no_se)_pct',
     'calc_ionic_active_am (dem_analysis_core.py:631–) → analyze_contacts — v1.1 ② (1저자 비준 10-01): 계산하고 버리던 단절 · 무접촉 내보내기 + '
     '상별 단절 · 무접촉 계산 추가 (시험 먼저 · analyze_contacts --selftest ⑬–⑱) · 관문 v1.1 D1–D5 (합 100 · 상별 합 100 · 정수 개수 · 상별 개수 '
     '합 = 전체 · 무접촉 ≤ 고립 위험)'),
    (r'se_se_cn_aug(_std|_n_extra|_h_spread_sim)?',
     'calc_se_se_cn F1 (dem_analysis_core.py:303–) → analyze_contacts.py:438–441 — J20-s ⑤ 감사 · 1저자 비준 10-04 ("권고대로") · 한정어 (h 10 nm '
     '출처 없는 모델 상수 · SE–SE 만 · 반올림 쌍) · 관문 ⑤F1 (aug = se_se_cn + 2 · n_extra / N_SE · 10-01 실측 130/130 · 64/64 상대차 ≤ 2.2e-16)'),
    (r'fracture_index_force|n_total_AM_AM_force|frac_(intact|microcrack|multicrack|fragmentation|pulverization)_force_pct|'
     r'n_(intact|microcrack|multicrack|fragmentation|pulverization)_force_AM_AM',
     'calc_fracture_stages (dem_analysis_core.py:977–) · fracture_model.fracture_classify_force_sim — J20-s ⑥ 감사 (LHS-31) · 1저자 비준 10-04 · '
     '힘 기반 전체 집계만 (δ 판 · 상 쌍별 = WA_EXCLUDED) · 관문 ⑥R1–R3 (단계 개수 합 = 전체 · 비율 · 지수 = 반올림 폭 안 · 전체 ≤ am_am_n_contacts) · '
     '10-01 실측 130/130 · 64/64 (전체 = am_am_n_contacts 194/194)'),
    (r'area_(AM_P|AM_S|SE|AM전체)_(AM_P|AM_S|SE)_(mean|total)|se_se_cn_eff_area(_perc)?|am_am_(mean|total)_area',
     'calc_interface_area (dem_analysis_core.py:191–) · calc_se_se_cn 면적 (:303–) · calc_am_am_cn (:443–) — J20-s ⑦ 감사 · 1저자 비준 10-04 · '
     'c_cpl[22] = 두 구 교차원 넓이의 정확식 (A_dem_geometric · 작은 δ 에서 Hertz πR*δ 의 ≈ 2 배 · L1-04) · 관문 ⑦A1–A5 (평균 × 개수 = 총합 · '
     '접촉 0 쌍 평균 N/A · AM전체 = 상별 합 · AM–AM 총합 = 쌍 합 · eff_area = 2 × SE–SE 총합 / (N_SE · 4π r_SE²) · eff_area_perc 빈칸 ⟺ 비관통) · '
     '10-01 실측 130/130 · 64/64 · path_hop_area 제외 (LHS-32)'),
)
#: 7c (J20-k · 1저자 비준 10-01 *"ㄱㄱ 하자"*) — 09-19 census 판정을 **바꿔 싣는** 열 (열 사전에 옛 판정을 병기한다).  census 에 없는 키
#:   (7a 새 키) 는 웹앱 배치 머리 (metrics_flat) 에 있을 때만 싣는다 — 옛 배치에 없는 키가 빈칸 = '측정된 N/A' 로 읽히지 않게.
_WA_OVR_VUL = ('✅ 쓴다 (승격 · LHS-23)', 'SE 접촉 0–1 개인 AM 의 비율 — 접촉 위상만 센다 (calc_am_isolation_risk · coverage 값을 읽지 않고 '
               '다른 단계가 덮어쓰지도 않는다) · 09-19 census 의 COND_cov ("coverage 문턱 기반") 는 오분류 (LHS-23)')
_WA_OVR_7A = ('✅ 쓴다 (새 키 · J20-k 7a)', 'AM 전 입자 AM–SE CN 분포 — 7a (09-30) 에 웹앱이 내보내기 시작한 키 · 09-19 census 에 없다 · '
              '상별 통계와 같은 counts · 같은 함수 (calc_am_isolation_risk)')
_WA_OVR_PERC = ('✅ 쓴다 (승격 · LHS-20)', 'SE 그래프 양 — calc_percolation 의 위 밴드 성분 · calc_ionic_active_am 의 AM–SE 접촉 유무 × '
                'top-reachable SE (coverage 값을 읽지 않는다) · 09-19 census 의 COND_cov 는 오분류 (LHS-20 · 1저자 비준 10-01)')
_WA_OVR_DEC = ('✅ 쓴다 (새 키 · v1.1 ②)', '경로 기준 고립의 분해 — 웹앱 v1.1 (10-01) 이 내보내기 시작한 키 · calc_ionic_active_am 이 계산하고 '
               '버리던 단절 · 무접촉 (상별 단절 · 무접촉은 이번에 계산 추가) · 활성 · 단절 · 무접촉 세 집합 하나에서 · 09-19 census 에 없다')
WA_VERDICT_OVERRIDE = {'am_vulnerable_pct': _WA_OVR_VUL, 'AM_P_vulnerable_pct': _WA_OVR_VUL, 'AM_S_vulnerable_pct': _WA_OVR_VUL,
                       'am_se_cn_std': _WA_OVR_7A, 'am_se_cn_median': _WA_OVR_7A, 'am_se_cn_max': _WA_OVR_7A,
                       'top_reachable_pct': _WA_OVR_PERC, 'ionic_active_pct': _WA_OVR_PERC,
                       **{k: _WA_OVR_DEC for k in WA_IONIC_DEC_KEYS}}


def wa_verdicts(wv):
    """7c — census 판정 + `WA_VERDICT_OVERRIDE` → (verdict, why).  census 에 있는 키는 판정을 바꾸고 옛 판정을 why 에 병기 ·
    census 밖 키는 웹앱 배치 머리 (행 키) 에 있을 때만 더한다.  `build_handover` 와 `column_dictionary` 가 같은 것을 쓴다."""
    v = dict((wv or {}).get('verdict') or {})
    why = dict((wv or {}).get('why') or {})
    hdr = set()
    for row in ((wv or {}).get('rows') or {}).values():
        hdr.update(row.keys())
    for c, (vd, reason) in WA_VERDICT_OVERRIDE.items():
        if c in v:
            why[c] = f'{reason} (09-19 census: {v[c]} — {why.get(c) or "사유 없음"})'
            v[c] = vd
        elif c in hdr:
            v[c], why[c] = vd, reason
    return v, why


#: J20-i — 표에 함께 실린 se_se_cn 과 area_SE_SE_n 의 항등식 (se_se_cn = 2 × area_SE_SE_n / N_SE) 허용 상대차.  metrics_flat 은 repr
#:   정밀도라 실측 차이는 0 이다 — 부동소수 여유일 뿐 물리 허용치가 아니다.
WA_CN_IDENTITY_TOL = 1e-9
#: J20-j — 웹앱 원 행의 AM–AM 쌍 개수 열 (calc_interface_area 는 두 상 이름을 정렬해 잇는다 · 접촉 0 인 쌍은 키가 없다 = 0 · mono 는 반지름 이름 하나)
WA_AM_AM_PAIR = re.compile(r'area_(AM_P|AM_S)_(AM_P|AM_S)_n')


def wa_review_note(col):
    """J20-g — 같이 확인한 열이면 검토 기록, 아니면 None."""
    for pat, note in WA_REVIEWED:
        if re.fullmatch(pat, col) is not None:
            return note
    return None


def wa_reviewed(col):
    """J20-g — 1저자와 같이 확인한 웹앱 열인가."""
    return wa_review_note(col) is not None


#: J20-k (B) (1저자 09-30 — *"인계할때는 중복되더라도 잘 채워서 보내야될듯"* · J20-f (A) 개정) — mono (2-type) 침대의 **상별** 열은
#:   **설계 상 칸**에 단일 AM 값을 싣는다.  설계 `block` (mono_AM_P → AM_P · mono_AM_S → AM_S) 이 상을 정한다.  웹앱은 AM 이 한 종류인 덱의
#:   AM 을 반지름으로 AM_P/AM_S 라 부르므로 (`type_map_resolve` · r > 4 µm) 이름이 설계와 다른 침대 (09-30 실측 130 의 5 · 64 의 4 — 전부 설계
#:   AM_P 인데 r ≤ 4 µm) 는 그 이름의 값을 설계 이름 칸으로 **옮기고** 웹앱 이름을 `wa_mono_phase_name_webapp` 에 남긴다.  설계에 없는 상의
#:   칸은 빈칸 (N/A · 0 아님).  수확기 열도 같은 규칙 — 수확기는 mono 의 상을 `AM` 하나로 라벨하므로 (`phase_counts.AM` · `coverage_detail.
#:   counts.AM` · `wall_touch.AM` · `coverage_AM_only` = `coverage_AM_total`) 그 값을 설계 상 칸에 싣는다 (coverage 상별 · n_AM_*_measured
#:   (`LHS-21`) · cov_*_n_valid · 벽 접촉 비율).  설계 block 과 수확 모양 (n_types · phase_counts · coverage 상태 · AM_only = 전체) 이 어긋나거나
#:   둘 중 하나를 모르면 **거부** — 조용히 (A) 로 돌아가면 한 표에 두 규약이 섞인다.  (A) 는 09-30 오전 판 (`lhs_handover_20260930.csv` 까지).
WA_PHASE_COL = re.compile(r'(^|_)AM_[PS](_|$)')
WA_PHASE_TOKEN = re.compile(r'(?<![A-Za-z0-9])AM_[PS](?![A-Za-z0-9])')     # 이름 안의 상 토큰 전부 (area_AM_S_AM_S_n 은 둘)
MONO_BLOCKS = {'mono_AM_P': 'AM_P', 'mono_AM_S': 'AM_S'}
MONO_DESIGN_NOTE = ('mono (2-type) 침대: 설계 상 칸 = 단일 AM 값 (전체 열과 중복 · J20-k (B)) — 설계 block 의 상 (mono_AM_P → AM_P · '
                    'mono_AM_S → AM_S) 칸에 싣고 설계에 없는 상의 칸은 빈칸 (N/A · 0 아님) · 웹앱 반지름 이름이 설계와 다르면 설계 이름 칸으로 '
                    '옮겼다 (웹앱 이름 = wa_mono_phase_name_webapp 열)')
MONO_PHASE_NOTE = MONO_DESIGN_NOTE          # (A) 시절 이름 — 호환


#: J20-h (1저자 비준 09-30 — *"bimodal 에서 빠진 쌍을 0 으로 채우게 · 시험 먼저"*) — `calc_interface_area` 는 접촉이 0 인 쌍의 키를 만들지 않는다
#:   (dem_analysis_core.py:131–168 — 덤프에 나온 쌍만 센다) → metrics_flat 빈칸.  두 상이 다 있는 침대에서 그 뜻은 **측정된 0** 이다.
WA_PAIR_COUNT = re.compile(r'area_(AM_P|AM_S|SE|AM전체)_(AM_P|AM_S|SE)_n')
WA_PAIR_TOTAL = re.compile(r'area_(AM_P|AM_S|SE|AM전체)_(AM_P|AM_S|SE)_total')     # ⑦ — 접촉 0 쌍 총합 = 0 (J20-h 와 같은 규칙 · J20-s)
PAIR_ZERO_NOTE = ('접촉 0 인 쌍 = 0 — 웹앱 `calc_interface_area` 는 접촉이 없는 쌍의 키를 만들지 않아 빈칸이 되므로, 두 상이 다 있는 침대 '
                  '(수확 `phase_counts`) 에서 생성기가 0 으로 채운다 (J20-h) · mono 는 설계 상으로 판단 (J20-k (B)) · 상이 없으면 빈칸 (N/A)')


def _phase_n(pc, ph):
    """수확 `phase_counts` 에서 상의 입자 수 — `AM전체` 는 AM (mono) + AM_P + AM_S."""
    if ph == 'AM전체':
        return sum(int(pc.get(k, 0) or 0) for k in ('AM', 'AM_P', 'AM_S'))
    return int(pc.get(ph, 0) or 0)


def _phase_n_mono(pc, ph, dp):
    """J20-k (B) — mono 침대 (설계 상 dp) 에서 상 ph 의 입자 수: 설계 상 = 수확 `AM` · 설계에 없는 상 = 0 · 그 밖은 `_phase_n`."""
    if dp is None:
        return _phase_n(pc, ph)
    if ph == dp:
        return _phase_n(pc, 'AM전체')
    if ph in ('AM_P', 'AM_S'):
        return 0
    return _phase_n(pc, ph)


def _phase_swap(col, a, b):
    """열 이름의 상 토큰 a → b 전부 (mono: 웹앱 반지름 이름 ↔ 설계 상 · area_AM_S_AM_S_n → area_AM_P_AM_P_n)."""
    return WA_PHASE_TOKEN.sub(lambda m: b if m.group(0) == a else m.group(0), col)


def _mono_path(path, dp, op):
    """J20-k (B) — 수확 JSON 경로의 상 키: 설계 상 → `AM` (수확기 mono 라벨) · 설계에 없는 상 → None (빈칸)."""
    if any(k == op for k in path):
        return None
    return tuple('AM' if k == dp else k for k in path)


def _mono_design_phase(r, h, case):
    """J20-k (B) — 설계행 · 수확 한 건 → (설계 상, 설계에 없는 상) 또는 (None, None) (bimodal).

    설계 `block` 과 수확 모양 (n_types · phase_counts · coverage 상별 상태 · AM_only = 전체) 이 어긋나거나 둘 중 하나를 모르면 `FillRefusal`
    — 조용히 (A) 로 돌아가지 않는다 (한 표에 두 규약이 섞인다).
    """
    blk = r.get('block')
    if blk not in (None, '') and str(blk).startswith('mono') and blk not in MONO_BLOCKS:
        raise FillRefusal(f'{case}: 설계 block {blk!r} — 아는 mono 라벨은 {sorted(MONO_BLOCKS)} 뿐이다 (설계 상을 정할 수 없다 · J20-k (B))')
    dp = MONO_BLOCKS.get(blk)
    nt = h.get('n_types')
    if dp is not None and nt is None:
        raise FillRefusal(f'{case}: 설계 block {blk} 인데 수확 JSON 에 n_types 가 없다 — 수확이 mono 인지 확인할 수 없어 설계 상 칸에 싣지 않는다 '
                          '(J20-k (B))')
    h_mono = nt is not None and int(nt) == 2
    if (dp is not None) != h_mono:
        raise FillRefusal(f'{case}: 설계 block {blk!r} ↔ 수확 n_types {nt!r} 가 어긋난다 — 설계 · 수확이 다른 침대거나 설계행에 block 이 없다 '
                          '(J20-k (B) 를 적용할 수 없다)')
    if dp is None:
        return None, None
    pc = h.get('phase_counts')
    if not isinstance(pc, dict):
        raise FillRefusal(f'{case}: mono 인데 수확 JSON 에 phase_counts 가 없다 — 단일 AM 입자 수를 모른다 (J20-k (B))')
    if _phase_n(pc, 'AM') <= 0 or _phase_n(pc, 'AM_P') > 0 or _phase_n(pc, 'AM_S') > 0:
        raise FillRefusal(f'{case}: mono 인데 phase_counts {pc} 가 수확기 mono 모양 (AM 하나 · AM_P/AM_S 없음) 이 아니다 (J20-k (B))')
    st = h.get('status') or {}
    for k in ('coverage_AM_P', 'coverage_AM_S'):
        if k in st and st[k] != 'N_A_PHASE_ABSENT':
            raise FillRefusal(f'{case}: mono 인데 수확 status.{k} = {st[k]!r} ≠ N_A_PHASE_ABSENT — 상별 값이 따로 있는 수확은 mono 모양이 아니다 '
                              '(J20-k (B))')
    only, tot = h.get('coverage_AM_only_hertz_pct'), h.get('coverage_AM_total_hertz_pct')
    if only is not None and tot is not None and float(only) != float(tot):
        raise FillRefusal(f'{case}: mono 인데 coverage_AM_only {only!r} ≠ coverage_AM_total {tot!r} — 단일 AM = 전체 항등식이 깨졌다 (J20-k (B))')
    return dp, ('AM_S' if dp == 'AM_P' else 'AM_P')


def wa_phase_specific(col):
    """AM_P / AM_S 한 상에 딸린 열인가 (상별 CN · 상별 쌍 개수) — AM전체 · 소문자 am_ 열은 아니다."""
    return WA_PHASE_COL.search(col) is not None


#: J20-a ⓓ (1저자 비준 09-28 밤 "권고하는걸로") — 상별 바닥 벽 · 플래튼 **접촉 입자 비율** (수확 v3 `wall_touch`).  CN 이 벽 · 플래튼
#:   접촉을 세지 않아 벽에 닿은 입자의 CN 이 낮은 몫을 가르는 설명 변수.  규칙 = 수확기 `WALL_TOUCH_RULE` (겹침 깊이 > 0 — z − r < 0 ·
#:   z + r > plate_z · 접선 = 0 은 안 셈 · 10-01 문구 정정: 옛 문구 "≤ · ≥" 는 수확기 규칙과 달랐다).
#:   벽 인접 입자를 뺀 CN 은 택하지 않았다 — AM_P 가 두께 2–10 개인 침대에서 남는 입자가 거의 없어 정의가 흔들린다.
WALL_TOUCH_PHASES = ('SE', 'AM_P', 'AM_S', 'AM')
HANDOVER_WALL_TOUCH = tuple(
    (f'wall_touch_frac_{ph}_{side}', ph, side,
     f'{ph} 입자 중 ' + ('바닥 벽 (z − r < 0)' if side == 'floor' else '플래튼 (z + r > plate_z)')
     + ' 에 닿은 비율 (0–1) · 닿음 = 겹침 깊이 > 0 (접선은 안 셈 · 수확기 WALL_TOUCH_RULE) · '
     + ('AM = AM_P + AM_S 합친 모집단 (am_se_cn_mean 과 같은 분모) · ' if ph == 'AM' else '') + '상이 없으면 빈칸 (N/A)')
    for ph in WALL_TOUCH_PHASES for side in ('floor', 'plate'))


def load_webapp(dir_path, census_path=None):
    """`scripts/lhs_webapp_batch.py` 산출 (status.json · metrics_flat.csv) + 전수 판정 census → `build_handover(webapp=…)` 인자."""
    root = pathlib.Path(__file__).resolve().parent.parent
    d = pathlib.Path(dir_path)
    st = json.loads((d / 'status.json').read_text(encoding='utf-8'))
    if st.get('schema') != 'lhs_webapp_batch/v1':
        raise FillRefusal(f'{d}/status.json schema {st.get("schema")!r} ≠ lhs_webapp_batch/v1')
    rows = {}
    with (d / 'metrics_flat.csv').open(encoding='utf-8', newline='') as fh:
        for r in csv.DictReader(fh):
            if r['case'] in rows:
                raise FillRefusal(f'{d}/metrics_flat.csv: case {r["case"]!r} 가 둘 이상이다')
            rows[r['case']] = r
    cp = pathlib.Path(census_path or (root / DEFAULT_CENSUS_TSV))
    verdict, why = {}, {}
    with cp.open(encoding='utf-8') as fh:
        for r in csv.DictReader(fh, delimiter='\t'):
            verdict[r['column']] = r['verdict']
            why[r['column']] = r.get('why') or ''
    return {'verdict': verdict, 'why': why, 'status': st.get('cases') or {}, 'rows': rows,
            'source': str(d), 'runs': st.get('runs') or [], 'stop_after': st.get('stop_after')}


def _frac_caveat(col):
    c = col.lower()
    if not any(k in c for k in ('frac_', 'fracture_index', 'fragmentation', 'pulverization', 'microcrack', 'multicrack', 'intact')):
        return ''
    return CAVEAT_FRAC_FORCE if 'force' in c else CAVEAT_FRAC_DELTA


def column_dictionary(cols, webapp=None):
    """인계표 열 사전 — 열마다 출처 · 판정 · 뜻 · 주의.  빈 뜻은 없다 (selftest ⑲m)."""
    extra = {n: w for n, _p, w in HANDOVER_EXTRA}
    union = {n: w for n, _c, w in HANDOVER_UNION}
    union.update({n: w for n, w in HANDOVER_UNION_DERIVED})
    tauw = {n: w for n, _k, w in HANDOVER_TAU_WALL}
    tauw.update({n: w for n, _p, _s, w in HANDOVER_WALL_TOUCH})
    tauw.update({n: w for n, w in HANDOVER_SE_CLUSTER})                          # v1.1 ③
    derived = dict(WA_DERIVED)                                                   # v1.1 ①
    warow = dict(WA_ROW_COLS)
    qc = {n: w for n, _a, _b, w in WA_QC}
    wverd, wwhy = wa_verdicts(webapp) if webapp is not None else ({}, {})      # 7c — 판정 바꿔 싣기 (LHS-23 · 7a) 를 표와 같게
    out = []
    for c in cols:
        d = {'column': c, 'source': '', 'verdict': '', 'meaning': '', 'caveat': ''}
        if c in HANDOVER_VALUE_MEANING:
            d.update(source='harvest', meaning=HANDOVER_VALUE_MEANING[c])
            if c.startswith('coverage_'):
                d['caveat'] = CAVEAT_NAME
        elif c.endswith('_status') and c[:-7] in HANDOVER_VALUE_MEANING:
            d.update(source='harvest', meaning=f'{c[:-7]} 의 상태 — OK 가 아니면 값 칸은 빈칸 (0 이 아니다)')
        elif c in extra:
            d.update(source='harvest', meaning=extra[c])
        elif c in union:
            d.update(source='union', meaning=union[c])
        elif c in tauw:
            d.update(source='harvest_v3', meaning=tauw[c])
        elif c in derived:
            d.update(source='webapp_derived', verdict='✅ 쓴다 (유도 · v1.1 ①)', meaning=derived[c], caveat=CAVEAT_PERC)
        elif c in warow:
            d.update(source='webapp_batch', meaning=warow[c])
        elif c in qc:
            d.update(source='qc', meaning=qc[c])
        elif webapp is not None and c in wverd:
            v = wverd[c]
            why = wwhy.get(c) or '웹앱 파이프라인 산출 (코퍼스 case_master 와 같은 이름 · 같은 계산)'
            dfn = wa_define(c)                       # J20-a ⓒ — 접촉 위상 열은 정의를 먼저 (판정 근거는 괄호로 남긴다)
            _lab = '09-19 판정 근거' if c in (webapp.get('verdict') or {}) else '판정 근거 (09-19 census 밖 키)'   # 7c — 7a 새 키
            meaning = f'{dfn[0]} ({_lab}: {why})' if dfn else why
            note = wa_review_note(c)                 # J20-g — 1저자 검토 기록
            if note:
                meaning += f' · 1저자 검토: {note}'
            if WA_PAIR_COUNT.fullmatch(c):           # J20-h
                meaning += ' · ' + PAIR_ZERO_NOTE
            d.update(source='webapp', verdict=v, meaning=meaning)
            d['caveat'] = dfn[1] if dfn else (CAVEAT_NAME if '이름 주의' in v else _frac_caveat(c))
        else:
            d.update(source='design', meaning='LHS 설계 열 (docs/data/lhs_design_20260818.csv — `build()` 가 만든 설계인자 · 추정치)')
        if wa_phase_specific(c) and d['source'] != 'design':      # J20-k (B) — 상별 열 전부 (수확 · 웹앱 · QC) 에 mono 규약 표지
            d['meaning'] += ' · ' + MONO_DESIGN_NOTE
        out.append(d)
    return out


def load_union(path):
    """union TSV (scripts/lhs_union_webapp.py 산출) → dict(case → 행).  같은 case 가 둘이면 거부."""
    with open(path, encoding='utf-8') as fh:
        rows = list(csv.DictReader(fh, delimiter='\t'))
    out = {}
    for r in rows:
        c = r.get('case')
        if not c or c in out:
            raise FillRefusal(f'union TSV {path}: case {c!r} 가 비었거나 둘 이상이다')
        out[c] = r
    return out


def _union_cols(case, h, u):
    """J19 — 수확 한 건 + union 행 → 인계 열.  짝 (같은 수확 · 같은 프레임) 이 아니면 `FillRefusal`."""
    if u.get('status') != 'OK':
        raise FillRefusal(f'{case}: union status {u.get("status")!r} ≠ OK — 그 union 값을 붙이지 않는다')
    eps_s = float(h['porosity_sphere_pct_RECORD_ONLY'])
    if abs(float(u['eps_sphere_web']) - eps_s) > UNION_TOL['eps_sphere_pct']:
        raise FillRefusal(f'{case}: union 의 구 부피 합 {u["eps_sphere_web"]} ≠ 수확 {eps_s!r} — 다른 수확 · 다른 프레임의 union 이다')
    th = (h.get('handover_qc') or {}).get('thickness_wall_gap_um')
    if th is None:
        raise FillRefusal(f'{case}: 수확에 두께 (handover_qc.thickness_wall_gap_um) 가 없다 — 09-24 판 수확이다 (0925 판을 쓸 것 · DEFAULT_HARVEST_DIR)')
    if abs(float(u['thickness_um']) - float(th)) > UNION_TOL['thickness_um']:
        raise FillRefusal(f'{case}: union 두께 {u["thickness_um"]} ≠ 수확 {th!r} µm — 다른 프레임 (플래튼) 의 union 이다')
    pc = h.get('phase_counts') or {}
    n_am = sum(int(v) for k, v in pc.items() if k != 'SE')
    if int(u['n_SE']) != int(pc.get('SE', -1)) or int(u['n_AM']) != n_am:
        raise FillRefusal(f'{case}: union 입자 수 (SE {u["n_SE"]} · AM {u["n_AM"]}) ≠ 수확 (SE {pc.get("SE")} · AM {n_am}) — 다른 침대다')
    eps_u = float(u['mc_void_pct'])
    if not 0.0 < eps_u < 100.0:
        raise FillRefusal(f'{case}: 정확 union {eps_u!r} % 가 (0, 100) 밖이다')
    o = {name: (str(u[col]) if col == 'pair_upper_bound_ok' else repr(float(u[col]))) for name, col, _w in HANDOVER_UNION}
    o['thickness_mass_conserving_um'] = repr(float(th) * (1.0 - eps_s / 100.0) / (1.0 - eps_u / 100.0))
    o['se_rich'] = str(float(u['se_of_solid_vol']) >= SE_RICH_MIN)
    #  J20-e (1저자 09-29 밤 "φ 는 (라) 만") — 질량 보존 φ: 인계 두께 (질량 보존) · porosity (union) 와 **같은 장부**.
    #   φ_i = φ_i(구) × (1 − ε_union)/(1 − ε_sphere) = V_i / (L² · 질량 보존 두께).  겹침 배분 규칙이 필요 없다.
    #   φ status 가 OK 가 아니면 빈칸 (계약 ② — 0 이 아니다).
    o['phi_se_mass_conserving'] = o['phi_am_mass_conserving'] = ''
    if ((h.get('status') or {}).get(DESCRIPTOR_STATUS_KEY['phi_se']) == 'OK'
            and h.get('phi_se') is not None and h.get('phi_am') is not None):
        k = (1.0 - eps_u / 100.0) / (1.0 - eps_s / 100.0)
        pse, pam = float(h['phi_se']) * k, float(h['phi_am']) * k
        e = abs(pse + pam + eps_u / 100.0 - 1.0)
        if e > PHI_MC_CLOSURE_TOL:
            raise FillRefusal(f'{case}: 질량 보존 φ 닫힘 {e:.3e} > {PHI_MC_CLOSURE_TOL:.0e} — DESC-07 (φ 둘 ↔ ε_sphere) 이 깨졌다')
        o['phi_se_mass_conserving'], o['phi_am_mass_conserving'] = repr(pse), repr(pam)
    return o


def _dig(h, path):
    cur = h
    for k in path:
        if not isinstance(cur, dict) or k not in cur:
            return None
        cur = cur[k]
    return cur


#: 7c — AM–SE CN · 고립 열 (calc_am_isolation_risk 산출)
WA_AMSE_COL = re.compile(r'am_se_cn_(mean|surface_weighted|std|median|max)|(AM_P|AM_S)_se_cn_(mean|std|median|max)|'
                         r'(am|AM_P|AM_S)_vulnerable_pct')
WA_AMSE_PHASE_COL = re.compile(r'(AM_P|AM_S)_(se_cn_(mean|std|median|max)|vulnerable_pct)')
WA_COUNT_INT_TOL = 1e-6          # 고립 비율 × 입자 수 / 100 = 정수 개수 (부동소수 여유 — 물리 허용치 아님)


def _wa_amse_gates(case, o, take, h, dp, drow):
    """7c 관문 (fail-closed) — 표에 실린 AM–SE CN · 고립 값 (o, mono 는 설계 상 칸으로 옮긴 뒤) 이 **같은 counts** (AM 입자별 SE 접촉 수 ·
    `calc_am_isolation_risk`) 에서 나왔는가.  09-30 실측 (J20-k) 은 전부 차이 0 · 5번 배치 max · median 194/194.

      상 있음/없음 — 상 (수확 phase_counts · mono 는 설계 상 = 수확 AM) 이 있으면 실린 상별 열은 값이 있어야 · 없으면 빈칸이어야 · 전체 열도 값
      G1 상별 평균 × 상 입자 수 = area_<상>_SE_n · G2 전체 평균 × AM 수 = area_AM전체_SE_n
      G3 고립: 비율 × 입자 수 / 100 = 정수 개수 · 전체 개수 = 상별 개수 합
      G4 전체 max = 상별 max 의 최댓값 · G5 median: mono = 단일 상 값 · bimodal = 상별 median 사이 (합집합의 중앙값 성질)
      G6 std: mono = 단일 상 값 · bimodal = 합동 (Σ N (σ² + μ²) / N − μ²) · G7 표면 가중: mono = 전체 평균 · bimodal = Σ N r² μ / Σ N r² (설계 반경)
    반환 1 (검사함).  어긋나면 `FillRefusal` (메시지에 '7c G<n>')."""
    pc = h.get('phase_counts')
    if not isinstance(pc, dict):
        raise FillRefusal(f'{case}: 수확 JSON 에 phase_counts 가 없다 — 상 입자 수를 몰라 AM–SE CN · 고립 관문을 볼 수 없다 (7c)')
    n = {ph: _phase_n_mono(pc, ph, dp) for ph in ('AM_P', 'AM_S')}
    n_am = _phase_n(pc, 'AM전체')
    present = [ph for ph in ('AM_P', 'AM_S') if n[ph] > 0]

    def num(c):
        v = o.get(c, '')
        return None if v in (None, '') else float(v)

    def close(a, b):
        return a is not None and b is not None and abs(a - b) <= WA_CN_IDENTITY_TOL * max(1.0, abs(b))

    for c in take:                                                   # 상 있음/없음
        m = WA_AMSE_PHASE_COL.fullmatch(c)
        has = o.get(c, '') not in (None, '')
        if m and n[m.group(1)] > 0 and not has:
            raise FillRefusal(f'{case}: {m.group(1)} 입자 {n[m.group(1)]} 개인데 {c} 가 빈칸 — 상이 있는데 값이 없다 (7c 상 있음)')
        if m and n[m.group(1)] == 0 and has:
            raise FillRefusal(f'{case}: {m.group(1)} 가 없는 침대 (수확 phase_counts) 인데 {c} = {o[c]} — 다른 침대의 값이다 (7c 상 없음)')
        if not m and WA_AMSE_COL.fullmatch(c) and n_am > 0 and not has:
            raise FillRefusal(f'{case}: AM {n_am} 개인데 {c} 가 빈칸 (7c 상 있음)')
    for ph in present:                                               # G1
        cm, ca = f'{ph}_se_cn_mean', f'area_{ph}_SE_n'
        if cm in take and ca in take and not close(num(cm) * n[ph], num(ca)):
            raise FillRefusal(f'{case}: {cm} {num(cm)!r} × {ph} {n[ph]} ≠ {ca} {num(ca)!r} — 같은 접촉 집합의 값이 아니다 (7c G1)')
    mu = num('am_se_cn_mean') if 'am_se_cn_mean' in take else None
    if mu is not None and 'area_AM전체_SE_n' in take and not close(mu * n_am, num('area_AM전체_SE_n')):  # G2
        raise FillRefusal(f'{case}: am_se_cn_mean {mu!r} × AM {n_am} ≠ area_AM전체_SE_n {num("area_AM전체_SE_n")!r} (7c G2)')
    if 'am_vulnerable_pct' in take:                                  # G3
        parts = {ph: num(f'{ph}_vulnerable_pct') * n[ph] / 100.0 for ph in present if f'{ph}_vulnerable_pct' in take}
        tot = num('am_vulnerable_pct') * n_am / 100.0
        for lab, x in [('am', tot)] + list(parts.items()):
            if abs(x - round(x)) > WA_COUNT_INT_TOL:
                raise FillRefusal(f'{case}: {lab} 고립 비율 × 입자 수 / 100 = {x!r} 이 정수 개수가 아니다 (7c G3)')
        if len(parts) == len(present) and round(tot) != sum(round(x) for x in parts.values()):
            raise FillRefusal(f'{case}: 고립 개수 전체 {round(tot)} ≠ 상별 합 {sum(round(x) for x in parts.values())} (7c G3)')
    st = {s: {ph: num(f'{ph}_se_cn_{s}') for ph in present if f'{ph}_se_cn_{s}' in take} for s in ('mean', 'std', 'median', 'max')}
    full = {s: len(st[s]) == len(present) and len(present) > 0 for s in st}
    if 'am_se_cn_max' in take and full['max'] and num('am_se_cn_max') != max(st['max'].values()):     # G4 (정수)
        raise FillRefusal(f'{case}: am_se_cn_max {num("am_se_cn_max")!r} ≠ 상별 max 의 최댓값 {max(st["max"].values())!r} (7c G4)')
    if 'am_se_cn_median' in take and full['median']:                 # G5
        md, lo, hi = num('am_se_cn_median'), min(st['median'].values()), max(st['median'].values())
        ok5 = close(md, lo) if len(present) == 1 else (lo - WA_CN_IDENTITY_TOL * max(1.0, lo) <= md <= hi + WA_CN_IDENTITY_TOL * max(1.0, hi))
        if not ok5:
            raise FillRefusal(f'{case}: am_se_cn_median {md!r} — 상별 median {st["median"]} ' + ('과 같아야 (mono)' if len(present) == 1 else '사이여야')
                              + ' (7c G5)')
    if 'am_se_cn_std' in take and mu is not None and full['std'] and full['mean']:    # G6
        sd = num('am_se_cn_std')
        if len(present) == 1:
            ok6 = close(sd, st['std'][present[0]])
        else:
            m2 = sum(n[ph] * (st['std'][ph] ** 2 + st['mean'][ph] ** 2) for ph in present) / n_am
            ok6 = abs(sd * sd - (m2 - mu * mu)) <= WA_CN_IDENTITY_TOL * max(1.0, m2)
        if not ok6:
            raise FillRefusal(f'{case}: am_se_cn_std {sd!r} — 상별 (N · 평균 · std) 의 합동 표준편차와 다르다 (7c G6)')
    if 'am_se_cn_surface_weighted' in take and mu is not None:        # G7
        sw = num('am_se_cn_surface_weighted')
        if len(present) == 1:
            exp7 = mu
        else:
            if not full['mean']:
                raise FillRefusal(f'{case}: 표면 가중을 확인할 상별 평균이 표에 없다 (7c G7)')
            try:
                rr = {ph: float(drow.get(f'r_{ph}_um')) for ph in present}
            except (TypeError, ValueError):
                raise FillRefusal(f'{case}: bimodal 인데 설계 반경 r_AM_P_um · r_AM_S_um 이 없다 — 표면 가중을 확인할 수 없다 (7c G7 반경)')
            exp7 = (sum(n[ph] * rr[ph] ** 2 * st['mean'][ph] for ph in present) / sum(n[ph] * rr[ph] ** 2 for ph in present))
        if not close(sw, exp7):
            raise FillRefusal(f'{case}: am_se_cn_surface_weighted {sw!r} ≠ {exp7!r} (Σ N r² CN / Σ N r² · 설계 반경) (7c G7)')
    return 1


#: ⑤⑥⑦ 관문 여유 — 물리 허용치가 아니다 (웹앱 반올림 · 부동소수 합의 순서만)
WA_FRAC_PCT_TOL = 0.005 + 1e-9          # calc_fracture_stages: round(100 n / N, 2) → 반폭 0.005
WA_FRAC_FI_TOL = 5e-5 + 1e-12           # round((파편화 + 분쇄) / N, 4)
WA_AREA_TOL = 1e-9                      # 같은 접촉 면적 합 (10-01 실측 ≤ 3e-14)


def _fnum(x):
    return None if x in (None, '') else float(x)


def _wa_f1_gates(case, wr, h):
    """⑤F1 — se_se_cn_aug = se_se_cn + 2 × n_extra / N_SE (calc_se_se_cn: 근접쌍 하나가 두 입자에 하나씩 더해진다 · 같은 SE 집합의 평균)."""
    cn, aug, nx, hs = (_fnum(wr.get(k)) for k in ('se_se_cn', 'se_se_cn_aug', 'se_se_cn_aug_n_extra', 'se_se_cn_aug_h_spread_sim'))
    if cn is None:
        return 0
    if aug is None or nx is None or hs is None:
        raise FillRefusal(f'{case}: se_se_cn 은 있는데 F1 열 (aug · n_extra · h_spread) 이 비었다 — F1 이 꺼진 배치를 N/A 로 싣지 않는다 (관문 ⑤F1 · J20-s)')
    if not hs > 0:
        raise FillRefusal(f'{case}: se_se_cn_aug_h_spread_sim {hs!r} ≤ 0 — F1 이 꺼진 값이다 (관문 ⑤F1 · J20-s)')
    pc = h.get('phase_counts')
    if not isinstance(pc, dict):
        raise FillRefusal(f'{case}: 수확 JSON 에 phase_counts 가 없다 — SE 입자 수를 몰라 F1 항등식을 잴 수 없다 (관문 ⑤F1 · J20-s)')
    n_se = _phase_n(pc, 'SE')
    exp = cn + 2.0 * nx / n_se if n_se > 0 else float('nan')
    if not (n_se > 0 and nx >= 0 and nx == int(nx) and abs(aug - exp) <= WA_CN_IDENTITY_TOL * max(1.0, abs(exp))):
        raise FillRefusal(f'{case}: se_se_cn_aug {aug!r} ≠ se_se_cn {cn!r} + 2 × n_extra {nx:g} / SE {n_se} = {exp!r} — 같은 접촉 집합의 '
                          'F1 이 아니다 (관문 ⑤F1 · J20-s)')
    return 1


def _wa_frac_gates(case, wr):
    """⑥R1–R3 — calc_fracture_stages: 단계 개수 합 = 전체 · 비율 = round(100 n / N, 2) · 지수 = round((파편화 + 분쇄) / N, 4) · 전체 ≤ AM–AM 접촉."""
    n_t = _fnum(wr.get('n_total_AM_AM_force'))
    amn = _fnum(wr.get('am_am_n_contacts'))
    if n_t is None:
        if amn is not None and amn > 0:
            raise FillRefusal(f'{case}: AM–AM 접촉 {amn:g} 개인데 힘 기반 파괴 열이 없다 — 파괴 단계가 빠진 행 (관문 ⑥R1 · J20-s)')
        return 0
    ns = [_fnum(wr.get(f'n_{s}_force_AM_AM')) for s in FRAC_STAGES]
    if any(n is None or n < 0 or n != int(n) for n in ns) or n_t != int(n_t):
        raise FillRefusal(f'{case}: 힘 기반 단계 개수가 비었거나 정수가 아니다 {ns} · 전체 {n_t!r} (관문 ⑥R1 · J20-s)')
    if sum(ns) != n_t:
        raise FillRefusal(f'{case}: 힘 기반 단계 개수 합 {sum(ns):g} ≠ n_total_AM_AM_force {n_t:g} (관문 ⑥R1 · J20-s)')
    fi = _fnum(wr.get('fracture_index_force'))
    fr = [_fnum(wr.get(f'frac_{s}_force_pct')) for s in FRAC_STAGES]
    if n_t > 0:
        if fi is None or any(x is None for x in fr):
            raise FillRefusal(f'{case}: n_total_AM_AM_force {n_t:g} > 0 인데 비율 · 지수가 비었다 (관문 ⑥R2 · J20-s)')
        for s, x, n in zip(FRAC_STAGES, fr, ns):
            if abs(x - 100.0 * n / n_t) > WA_FRAC_PCT_TOL:
                raise FillRefusal(f'{case}: frac_{s}_force_pct {x!r} ≠ 100 × {n:g} / {n_t:g} = {100.0 * n / n_t:.4f} — 반올림 폭 0.005 밖 '
                                  '(관문 ⑥R2 · J20-s)')
        e_fi = (ns[3] + ns[4]) / n_t
        if abs(fi - e_fi) > WA_FRAC_FI_TOL:
            raise FillRefusal(f'{case}: fracture_index_force {fi!r} ≠ (파편화 + 분쇄) / N = {e_fi:.6f} — 반올림 폭 5e-5 밖 (관문 ⑥R2 · J20-s)')
    elif fi is not None or any(x is not None for x in fr):
        raise FillRefusal(f'{case}: n_total_AM_AM_force 0 인데 비율 · 지수가 있다 (관문 ⑥R2 · J20-s)')
    if amn is not None and n_t > amn:
        raise FillRefusal(f'{case}: n_total_AM_AM_force {n_t:g} > am_am_n_contacts {amn:g} — fn > 0 AM–AM 접촉은 전 AM–AM 접촉의 부분집합 '
                          '(관문 ⑥R3 · J20-s)')
    return 1


def _wa_area_prep(case, wr, rep):
    """⑦A1 — 쌍마다 개수 > 0 이면 평균 × 개수 = 총합 · 개수 0 이면 총합 0 · 평균 없음 (calc_interface_area 의 AM전체–SE 평균 0 대입은 빈칸으로).
    반환 = 접촉 0 쌍의 평균을 비운 행 **사본** (웹앱 원 행은 안 바꾼다)."""
    out = dict(wr)
    for k, v in wr.items():
        if v in (None, '') or re.fullmatch(r'area_(.+)_n', k) is None:
            continue
        b = k[:-2]
        n = float(v)
        tot, mean = _fnum(wr.get(b + '_total')), _fnum(wr.get(b + '_mean'))
        if n > 0:
            if tot is None or mean is None:
                raise FillRefusal(f'{case}: {b} 개수 {n:g} > 0 인데 평균 · 총합이 비었다 (관문 ⑦A1 · J20-s)')
            if abs(mean * n - tot) > WA_AREA_TOL * max(abs(tot), abs(mean * n), 1e-300):
                raise FillRefusal(f'{case}: {b}_mean {mean!r} × 개수 {n:g} ≠ {b}_total {tot!r} — 같은 접촉의 값이 아니다 (관문 ⑦A1 · J20-s)')
        else:
            if tot not in (None, 0.0):
                raise FillRefusal(f'{case}: {b} 개수 0 인데 총합 {tot!r} ≠ 0 (관문 ⑦A1 · J20-s)')
            if mean is not None:
                if mean != 0.0:
                    raise FillRefusal(f'{case}: {b} 개수 0 인데 평균 {mean!r} 이 있다 — 접촉 0 개에서 평균은 정의되지 않는다 (관문 ⑦A1 · J20-s)')
                out[b + '_mean'] = ''
                rep['wa_area_mean_blanked'] += 1
    return out


def _wa_area_gates(case, wr, h, drow, take):
    """⑦A2–A5 — AM전체–SE = 상별 합 · AM–AM 총합 = 쌍 합 · 평균 = 총합 / 개수 · eff_area = 2 × SE–SE 총합 / (N_SE · 4π r_SE²) ·
    eff_area_perc 빈칸 ⟺ 비관통 (percolation_pct 0)."""
    tot = _fnum(wr.get('area_AM전체_SE_total'))
    if tot is not None:
        s_ = sum(x for x in (_fnum(wr.get(f'area_{p}_SE_total')) for p in ('AM_P', 'AM_S')) if x is not None)
        if abs(tot - s_) > WA_AREA_TOL * max(abs(tot), abs(s_), 1e-300):
            raise FillRefusal(f'{case}: area_AM전체_SE_total {tot!r} ≠ AM_P–SE + AM_S–SE {s_!r} (관문 ⑦A2 · J20-s)')
        n_all = _fnum(wr.get('area_AM전체_SE_n'))
        n_s = sum(x for x in (_fnum(wr.get(f'area_{p}_SE_n')) for p in ('AM_P', 'AM_S')) if x is not None)
        if n_all is not None and n_all != n_s:
            raise FillRefusal(f'{case}: area_AM전체_SE_n {n_all:g} ≠ AM_P–SE + AM_S–SE 개수 {n_s:g} (관문 ⑦A2 · J20-s)')
    aat, aam, amn = (_fnum(wr.get(k)) for k in ('am_am_total_area', 'am_am_mean_area', 'am_am_n_contacts'))
    if aat is not None:
        s_ = sum((_fnum(wr.get(f'area_{p}_total')) or 0.0) for p in ('AM_P_AM_P', 'AM_P_AM_S', 'AM_S_AM_S'))
        if abs(aat - s_) > WA_AREA_TOL * max(abs(aat), abs(s_), 1e-300):
            raise FillRefusal(f'{case}: am_am_total_area {aat!r} ≠ AM–AM 쌍 총합 {s_!r} (관문 ⑦A3 · J20-s)')
        if amn is not None and amn > 0:
            e_m = aat / amn
            if aam is None or abs(aam - e_m) > WA_AREA_TOL * max(abs(aam), abs(e_m), 1e-300):
                raise FillRefusal(f'{case}: am_am_mean_area {aam!r} ≠ am_am_total_area / am_am_n_contacts = {e_m!r} (관문 ⑦A3 · J20-s)')
    if 'se_se_cn_eff_area' in take:
        ea, sst = _fnum(wr.get('se_se_cn_eff_area')), _fnum(wr.get('area_SE_SE_total'))
        if ea is not None:
            rse = _fnum(drow.get('r_SE_um'))
            pc = h.get('phase_counts')
            if rse is None or not rse > 0 or not isinstance(pc, dict) or sst is None:
                raise FillRefusal(f'{case}: se_se_cn_eff_area 를 잴 수 없다 — 설계 r_SE_um {drow.get("r_SE_um")!r} · phase_counts · area_SE_SE_total 중 '
                                  '없는 것이 있다 (관문 ⑦A4 · J20-s)')
            n_se = _phase_n(pc, 'SE')
            e_a = 2.0 * sst / (n_se * 4.0 * math.pi * rse * rse) if n_se > 0 else float('nan')
            if not (n_se > 0 and abs(ea - e_a) <= WA_AREA_TOL * max(abs(e_a), 1e-300)):
                raise FillRefusal(f'{case}: se_se_cn_eff_area {ea!r} ≠ 2 × area_SE_SE_total / (N_SE {n_se} · 4π r_SE²) = {e_a!r} '
                                  '(관문 ⑦A4 · J20-s · SE 단분산 = 설계 d_se 하나)')
    if 'se_se_cn_eff_area_perc' in take:
        pp, eap = _fnum(wr.get('percolation_pct')), _fnum(wr.get('se_se_cn_eff_area_perc'))
        if pp is not None and (eap is None) != (pp == 0.0):
            raise FillRefusal(f'{case}: se_se_cn_eff_area_perc {wr.get("se_se_cn_eff_area_perc")!r} ↔ percolation_pct {pp!r} — 빈칸 ⟺ 비관통이어야 '
                              '한다 (관문 ⑦A5 · J20-s)')
    return 1


def _wa_perc_gates(case, o, take, h):
    """② 관문 (fail-closed) — 표에 실린 퍼콜레이션 값이 한 SE 그래프에서 나왔고 수확기가 독립으로 재현하는가.  09-29 J20-b 감사 130/130 CLEAN ·
    10-01 실측 130/130 · 64/64 성립.

      P1 관통 일관: percolation_pct > 0 ⟺ se_se_cn_perc · se_se_cn_n_perc 에 값 ⟺ 수확기 벽 밴드 관통 (`tau_detail.band_detail.wall_n_span_components`
         > 0 · J20-b F8 독립 재현 — SE 단분산이면 두 밴드 규칙이 같은 집합)
      P2 범위 · 순서: 비율 셋 ∈ [0, 100] · 성분 수 정수 ≥ 0 · n_large ≤ n_components · top_reachable ≥ percolation (관통 SE 는 위 밴드에 닿는다)
      P3 관통 SE 개수 = percolation_pct × N_SE / 100 (수확 phase_counts)
    반환 1 (검사함).  어긋나면 `FillRefusal` (메시지에 '② P<n>')."""
    def num(c):
        v = o.get(c, '')
        return None if v in (None, '') else float(v)
    for c in ('percolation_pct', 'top_reachable_pct', 'ionic_active_pct'):             # P2
        if c in take and num(c) is not None and not (0.0 <= num(c) <= 100.0):
            raise FillRefusal(f'{case}: {c} {num(c)!r} ∉ [0, 100] (② P2)')
    for c in ('n_components', 'n_large_components'):
        if c in take and num(c) is not None and (num(c) < 0 or num(c) != int(num(c))):
            raise FillRefusal(f'{case}: {c} {num(c)!r} 이 0 이상 정수가 아니다 (② P2)')
    if 'n_components' in take and 'n_large_components' in take and None not in (num('n_components'), num('n_large_components')) \
            and num('n_large_components') > num('n_components'):
        raise FillRefusal(f'{case}: n_large_components {num("n_large_components")!r} > n_components {num("n_components")!r} (② P2)')
    pp = num('percolation_pct') if 'percolation_pct' in take else None
    if pp is not None and 'top_reachable_pct' in take and num('top_reachable_pct') is not None \
            and num('top_reachable_pct') < pp - WA_CN_IDENTITY_TOL * max(1.0, pp):
        raise FillRefusal(f'{case}: top_reachable_pct {num("top_reachable_pct")!r} < percolation_pct {pp!r} — 관통 SE 는 위 밴드에 닿는다 (② P2)')
    if pp is None:
        return 1
    perc = pp > 0.0
    for c in ('se_se_cn_perc', 'se_se_cn_n_perc'):                                      # P1
        if c in take and (num(c) is not None) != perc:
            raise FillRefusal(f'{case}: percolation_pct {pp!r} 인데 {c} = {o.get(c)!r} — 관통 여부와 값 유무가 어긋난다 (② P1)')
    span = _dig(h, ('tau_detail', 'band_detail', 'wall_n_span_components'))
    if span is None:
        raise FillRefusal(f'{case}: 수확 JSON 에 tau_detail.band_detail.wall_n_span_components 가 없다 — 관통을 독립으로 재현할 수 없다 (② P1)')
    if (int(span) > 0) != perc:
        raise FillRefusal(f'{case}: 웹앱 percolation_pct {pp!r} ↔ 수확기 벽 밴드 관통 성분 {span} — 독립 재현이 어긋난다 (② P1 · J20-b F8)')
    if 'se_se_cn_n_perc' in take and perc:                                               # P3
        pc = h.get('phase_counts')
        if not isinstance(pc, dict):
            raise FillRefusal(f'{case}: 수확 JSON 에 phase_counts 가 없다 — 관통 SE 개수를 확인할 수 없다 (② P3)')
        exp3 = pp * _phase_n(pc, 'SE') / 100.0
        if abs(num('se_se_cn_n_perc') - exp3) > WA_COUNT_INT_TOL:
            raise FillRefusal(f'{case}: se_se_cn_n_perc {num("se_se_cn_n_perc")!r} ≠ percolation_pct × N_SE / 100 = {exp3!r} (② P3)')
    return 1


def _wa_ionic_gates(case, o, take, h, dp):
    """v1.1 ①② 관문 (fail-closed) — 이온 활성 · 경로 기준 고립 · 분해가 calc_ionic_active_am 의 **세 집합 하나**에서 나왔는가.

      상 있음/없음 — 상 (수확 phase_counts · mono 는 설계 상) 이 있으면 실린 상별 분해 열은 값이 있어야 · 없으면 빈칸이어야
      D1 전체 활성 + 단절 + 무접촉 = 100 · D2 상별 같은 합 = 100
      D3 비율 × 입자 수 / 100 = 정수 개수 (활성은 분해 키가 없는 옛 배치에서도 — ① 의 원천)
      D4 상별 개수 합 = 전체 개수 (활성 · 단절 · 무접촉 각각)
      D5 무접촉 개수 ≤ 고립 위험 개수 (SE 접촉 0 ⊂ 0–1 개 — 7c 와 같은 접촉 집합 · 전체 · 상별)
    반환 1.  어긋나면 `FillRefusal` (메시지에 'v1.1 D<n>' · 'v1.1 상 있음/없음')."""
    pc = h.get('phase_counts')
    if not isinstance(pc, dict):
        raise FillRefusal(f'{case}: 수확 JSON 에 phase_counts 가 없다 — AM 입자 수를 몰라 이온 활성 · 고립 관문을 볼 수 없다 (v1.1 D3)')
    n = {ph: _phase_n_mono(pc, ph, dp) for ph in ('AM_P', 'AM_S')}
    n_am = _phase_n(pc, 'AM전체')
    present = [ph for ph in ('AM_P', 'AM_S') if n[ph] > 0]

    def num(c):
        v = o.get(c, '') if c in take else ''
        return None if v in (None, '') else float(v)
    for c in take:                                                    # 상 있음/없음
        m = WA_IONIC_PHASE_RE.fullmatch(c)
        if not m:
            continue
        has = o.get(c, '') not in (None, '')
        if n[m.group(1)] > 0 and not has:
            raise FillRefusal(f'{case}: {m.group(1)} 입자 {n[m.group(1)]} 개인데 {c} 가 빈칸 — 상이 있는데 값이 없다 (v1.1 상 있음)')
        if n[m.group(1)] == 0 and has:
            raise FillRefusal(f'{case}: {m.group(1)} 가 없는 침대인데 {c} = {o[c]} — 다른 침대의 값이다 (v1.1 상 없음)')
    trio = {'전체': [num(f'ionic_{s_}_pct') for s_ in ('active', 'dead', 'no_se')]}
    trio.update({ph: [num(f'{ph}_ionic_{s_}_pct') for s_ in ('active', 'dead', 'no_se')] for ph in present})
    if None not in trio['전체'] and abs(sum(trio['전체']) - 100.0) > WA_PCT_SUM_TOL:        # D1
        raise FillRefusal(f'{case}: 활성 + 단절 + 무접촉 = {sum(trio["전체"])!r} ≠ 100 — 같은 세 집합이 아니다 (v1.1 D1)')
    for ph in present:                                                # D2
        if None not in trio[ph] and abs(sum(trio[ph]) - 100.0) > WA_PCT_SUM_TOL:
            raise FillRefusal(f'{case}: {ph} 활성 + 단절 + 무접촉 = {sum(trio[ph])!r} ≠ 100 (v1.1 D2)')
    cnt = {}
    for lab, N in [('전체', n_am)] + [(ph, n[ph]) for ph in present]:  # D3
        for s_, v in zip(('active', 'dead', 'no_se'), trio[lab]):
            if v is None:
                continue
            x = v * N / 100.0
            if abs(x - round(x)) > WA_COUNT_INT_TOL:
                raise FillRefusal(f'{case}: {lab} {s_} 비율 {v!r} × 입자 수 {N} / 100 = {x!r} 이 정수 개수가 아니다 (v1.1 D3)')
            cnt[(lab, s_)] = round(x)
    for s_ in ('active', 'dead', 'no_se'):                             # D4
        if present and ('전체', s_) in cnt and all((ph, s_) in cnt for ph in present) \
                and cnt[('전체', s_)] != sum(cnt[(ph, s_)] for ph in present):
            raise FillRefusal(f'{case}: {s_} 개수 전체 {cnt[("전체", s_)]} ≠ 상별 합 {sum(cnt[(ph, s_)] for ph in present)} (v1.1 D4)')
    for lab, vcol, N in [('전체', 'am_vulnerable_pct', n_am)] + [(ph, f'{ph}_vulnerable_pct', n[ph]) for ph in present]:   # D5
        vv = num(vcol)
        if (lab, 'no_se') in cnt and vv is not None and cnt[(lab, 'no_se')] > round(vv * N / 100.0):
            raise FillRefusal(f'{case}: {lab} 무접촉 {cnt[(lab, "no_se")]} 개 > 고립 위험 {round(vv * N / 100.0)} 개 — SE 접촉 0 은 0–1 개의 '
                              '부분집합이다 (v1.1 D5)')
    return 1


def build_handover(rows, harvest, key='case_id', union=None, webapp=None, webapp_groups=None, wa_reviewed_only=True):
    """설계행 + 수확 (+ union) (+ 웹앱) → 인계용 행 리스트.  **순수 함수**(파일을 안 쓴다) 라 시험 가능하다.

    union (J19, 선택): `load_union` 산출 dict 또는 행 목록.  주면 설계 케이스 **전부**에 짝이 있어야 하고 (부분 병기 금지),
    짝마다 구 부피 합 porosity · 두께 · 상별 입자 수가 수확과 같아야 한다 (`_union_cols`).  설계에 없는 union 행 (코호트의 perc 등) 은
    인계표에 넣지 않고 report['union_extra'] 에 남긴다.
    벽 τ (J20): 수확 JSON 에 `tau_wall_detail` 이 **전부** 있으면 새 열로 싣는다 (일부만 있으면 수확 세대 혼합 → 거부).
    webapp (J20, 선택): `load_webapp` 산출.  설계행 **전부**를 배치가 시도했어야 하고, done · partial 행은 웹앱 porosity = 수확 porosity
    (WA_SAME_FRAME_TOL_PCT) 여야 한다.  ✅ 열만 · 이름 충돌이면 기존 열이 정본 (report['wa_collisions']).  거부 · 실패 행은 빈칸 + wa_status.
    반환 (out_rows, cols, report).  계약 위반이면 `FillRefusal`.
    """
    #  ⚠ `load_harvest` 는 **dict(case → h)** 를 준다.  초판은 list 만 받아서
    #    selftest(list) 는 통과하는데 프로덕션(dict)에서 죽었다 — 시험이 프로덕션
    #    모양을 안 쓰면 그 자리가 곧 사각지대다 (규율 ⑤).  둘 다 받는다.
    hv = dict(harvest) if isinstance(harvest, dict) else {h['case']: h for h in harvest}
    miss = [r[key] for r in rows if r[key] not in hv]
    if miss:
        raise FillRefusal(f'수확에 없는 설계행 {len(miss)} 건: {miss[:5]} — 부분 인계는 금지 (DESC-09)')
    design_cols = [c for c in rows[0]
                   if c not in HANDOVER_VALUE_COLS
                   and c not in HANDOVER_HELD_BACK
                   and not c.endswith('_status')]
    cols = list(design_cols)
    for c in HANDOVER_VALUE_COLS:
        cols += [c, c + '_status']
    cols += [n for n, _p, _w in HANDOVER_EXTRA]
    uv = None
    if union is not None:
        uv = dict(union) if isinstance(union, dict) else {u['case']: u for u in union}
        miss_u = [r[key] for r in rows if r[key] not in uv]
        if miss_u:
            raise FillRefusal(f'union 에 없는 설계행 {len(miss_u)} 건: {miss_u[:5]} — 부분 병기 금지 (J19)')
        cols += [n for n, _c, _w in HANDOVER_UNION] + [n for n, _w in HANDOVER_UNION_DERIVED]
    #  J20 — 벽 τ: 전부 있거나 전부 없어야 한다 (한 표에 수확 세대 둘을 섞지 않는다)
    _tw_has = [('tau_wall_detail' in hv[r[key]]) for r in rows]
    if any(_tw_has) and not all(_tw_has):
        _no = [r[key] for r, h_ in zip(rows, _tw_has) if not h_]
        raise FillRefusal(f'벽 τ (tau_wall_detail) 가 {sum(_tw_has)}/{len(rows)} 수확에만 있다 — 수확 세대가 섞였다 (없는 행 {_no[:5]})')
    tw_on = bool(_tw_has) and all(_tw_has)
    if tw_on:
        cols += [n for n, _k, _w in HANDOVER_TAU_WALL]
    #  J20-a ⓓ — 상별 벽 접촉 비율: 전부 있거나 전부 없어야 한다 (수확 세대 혼합 금지)
    _wt_has = [('wall_touch' in hv[r[key]]) for r in rows]
    if any(_wt_has) and not all(_wt_has):
        _no = [r[key] for r, h_ in zip(rows, _wt_has) if not h_]
        raise FillRefusal(f'벽 접촉 비율 (wall_touch) 이 {sum(_wt_has)}/{len(rows)} 수확에만 있다 — 수확 세대가 섞였다 (없는 행 {_no[:5]})')
    wt_on = bool(_wt_has) and all(_wt_has)
    if wt_on:
        cols += [n for n, _p, _s, _w in HANDOVER_WALL_TOUCH]
    #  v1.1 ③ — 가장 큰 SE 덩어리: 전부 있거나 전부 없어야 한다 (키 유무 = 수확 세대 · 값이 None 이면 관문 C1 이 거부)
    _sc_has = [('largest_comp_frac' in (_dig(hv[r[key]], ('tau_detail', 'band_detail')) or {})) for r in rows]
    if any(_sc_has) and not all(_sc_has):
        _no = [r[key] for r, h_ in zip(rows, _sc_has) if not h_]
        raise FillRefusal(f'가장 큰 SE 덩어리 기록 (largest_comp_*) 이 {sum(_sc_has)}/{len(rows)} 수확에만 있다 — 수확 세대가 섞였다 (없는 행 {_no[:5]})')
    sc_on = bool(_sc_has) and all(_sc_has)
    if sc_on:
        cols += [n for n, _w in HANDOVER_SE_CLUSTER]
    wv, wa_take = webapp, []
    _gs = wa_groups_norm(webapp_groups)
    if _gs is not None and (not _gs or any(g not in WA_GROUPS for g in _gs)):
        raise FillRefusal(f'webapp_groups {webapp_groups!r} — 아는 묶음은 {WA_GROUPS} 뿐이다 (① 접촉 위상 = contact · ② = percolation · '
                          f'⑤ F1 = f1 · ⑥ Auerbach 힘 기반 = fracture · ⑦ 면적 = area)')
    if wv is not None:
        #  묶음별 — 접촉 단계만 돈 배치는 그 묶음으로만 부른다 (뒤 단계 열이 빈칸 = 측정된 N/A 로 읽히지 않게)
        _sa = wv.get('stop_after')
        if _sa and (_gs is None or any(g not in WA_STAGE_GROUPS.get(_sa, (_sa,)) for g in _gs)):
            raise FillRefusal(f'웹앱 배치가 stop_after={_sa!r} 로 돌았다 — webapp_groups={webapp_groups!r} 로는 싣지 않는다 '
                              f'(그 배치가 다 낸 묶음만: --webapp-groups {",".join(WA_STAGE_GROUPS.get(_sa, (_sa,)))} 의 부분집합)')
        miss_w = [r[key] for r in rows if r[key] not in (wv.get('status') or {})]
        if miss_w:
            raise FillRefusal(f'웹앱 배치가 시도하지 않은 설계행 {len(miss_w)} 건: {miss_w[:5]} — 배치 미완 (재개로 채울 것)')
        ok_cols = [c for c, v in wa_verdicts(wv)[0].items() if str(v).startswith('✅')]     # 7c — 판정 바꿔 싣기 포함
        _n_excl = sum(1 for c in ok_cols if wa_excluded(c) is not None)       # ⑤⑥⑦ — 인계 제외 열은 묶음 · 검토와 무관하게 먼저 (J20-s)
        ok_cols = [c for c in ok_cols if wa_excluded(c) is None]
        if _gs is not None:
            ok_cols = [c for c in ok_cols if any(WA_GROUP_FN[g](c) for g in _gs)]
        n_census_ok = len(ok_cols)
        if wa_reviewed_only:                        # J20-g — 같이 확인한 열만 (CLI 는 항상 이 경로 · False 는 옛 기제 시험 전용)
            ok_cols = [c for c in ok_cols if wa_reviewed(c)]
        have = set(cols)
        wa_take = [c for c in ok_cols if c not in have and c not in {n for n, _w in WA_ROW_COLS}]
        wa_coll = [c for c in ok_cols if c in have]
        wa_iso_on = 'ionic_active_pct' in wa_take                   # v1.1 ① — 활성 열이 실리면 경로 기준 고립 (유도) 도 싣는다
        cols += [n for n, _w in WA_ROW_COLS] + wa_take + ([n for n, _w in WA_DERIVED] if wa_iso_on else []) + [n for n, _a, _b, _w in WA_QC]
    out, rep = [], {'n': 0, 'blank_by_status': collections.Counter(),
                    'held_back': dict(HANDOVER_HELD_BACK), 'mono_rows': 0, 'mono_harvest_filled': 0}
    if uv is not None:
        rep['union_extra'] = sorted(set(uv) - {r[key] for r in rows})
    if tw_on:
        rep['tau_wall_status'] = collections.Counter()
        rep['tau_wall_checked'] = rep['tau_perc_crosschecked'] = 0
    if sc_on:
        rep['se_cluster_checked'] = 0
    if wv is not None:
        rep.update(wa_collisions=wa_coll, wa_n_cols=len(wa_take), wa_status_counts=collections.Counter(),
                   wa_porosity_absmax=0.0, wa_reviewed_only=bool(wa_reviewed_only),
                   wa_unreviewed_dropped=n_census_ok - len(ok_cols), wa_pair_zero_filled=0,
                   wa_mono_renamed_cases=0, wa_mono_design_filled=0, wa_mono_absent_blanked=0,
                   wa_cn_identity_checked=0, wa_am_identity_checked=0, wa_amse_identity_checked=0, wa_perc_checked=0,
                   wa_ionic_checked=0, wa_f1_checked=0, wa_frac_checked=0, wa_area_checked=0,
                   wa_area_mean_blanked=0, wa_area_total_zero_filled=0, wa_excluded_dropped=_n_excl)
    for r in rows:
        h = hv[r[key]]
        o = {c: r.get(c, '') for c in design_cols}
        #  J20-k (B) — mono 침대의 설계 상 (block) · 설계에 없는 상.  설계 ↔ 수확 모양이 어긋나면 여기서 거부된다.
        dp, op = _mono_design_phase(r, h, r[key])
        if dp is not None:
            rep['mono_rows'] += 1
        for c in HANDOVER_VALUE_COLS:
            #  (B) — mono 의 설계 상 칸 ← 전체 (단일 AM = 전체 · coverage_AM_only = coverage_AM_total 을 위에서 확인했다)
            src = 'coverage_AM_total_hertz_pct' if (dp is not None and c == f'coverage_{dp}_hertz_pct') else c
            st = h['status'][DESCRIPTOR_STATUS_KEY[src]]
            v = h.get(src)
            #  계약 ② — OK 가 아니면 값 칸은 **비운다** (0 이 아니다)
            o[c] = repr(float(v)) if (st == 'OK' and v is not None) else ''
            o[c + '_status'] = st
            if st != 'OK':
                rep['blank_by_status'][st] += 1
            elif src != c:
                rep['mono_harvest_filled'] += 1
        for name, path, _why in HANDOVER_EXTRA:
            p = _mono_path(path, dp, op) if dp is not None else path   # (B) — 설계 상 키 → 수확 `AM` · 없는 상 → 빈칸
            v = None if p is None else _dig(h, p)
            o[name] = '' if v is None else str(v)
            if v is not None and p != path:
                rep['mono_harvest_filled'] += 1
        #  계약 ③ — DESC-07 항등식을 **내보내는 표 위에서 다시** 잰다
        e1 = abs(float(h['porosity_sphere_pct_RECORD_ONLY'])
                 - 100.0 * (1.0 - float(h['phi_se']) - float(h['phi_am'])))
        if e1 > DESC07_TOL['porosity']:
            raise FillRefusal(f"{r[key]}: DESC-07 항등식 위반 {e1:.3e}")
        if uv is not None:
            o.update(_union_cols(r[key], h, uv[r[key]]))
        if tw_on:
            t = h['tau_wall_detail']
            if t.get('tau_convention') != TAU_WALL_CONVENTION:
                raise FillRefusal(f'{r[key]}: 벽 τ 규약 {t.get("tau_convention")!r} ≠ {TAU_WALL_CONVENTION} — 다른 규약의 값을 같은 열에 넣지 않는다')
            for name, k, _w in HANDOVER_TAU_WALL:
                v = t.get(k)
                if name in TAU_WALL_VALUE:        # 계약 ② — OK 가 아니면 값 칸은 빈칸
                    o[name] = repr(float(v)) if (t.get('status') == 'OK' and v is not None) else ''
                else:
                    o[name] = '' if v is None else str(v)
            rep['tau_wall_status'][t.get('status')] += 1
            rep['tau_wall_checked'] += _tau_wall_gates(r[key], t, h)          # T1 · T2
        if wt_on:
            wt = h.get('wall_touch') or {}
            for name, ph, side, _w in HANDOVER_WALL_TOUCH:
                #  J20-k (B) — mono: 설계 상 칸 ← 수확 `AM` · 설계에 없는 상 → 빈칸 · AM · SE 열은 그대로
                src_ph = ('AM' if ph == dp else (None if ph == op else ph)) if dp is not None else ph
                v = None if src_ph is None else (wt.get(src_ph) or {}).get(side)
                o[name] = '' if v is None else repr(float(v))          # 없는 상 = 빈칸 (N/A · 0 이 아니다)
                if v is not None and src_ph != ph:
                    rep['mono_harvest_filled'] += 1
        if sc_on:                                                     # v1.1 ③ — C1–C3
            o.update(_se_cluster_cols(r[key], h))
            rep['se_cluster_checked'] += 1
        if wv is not None:
            rec = wv['status'][r[key]] or {}
            s = rec.get('status') or 'UNKNOWN'
            rep['wa_status_counts'][s] += 1
            o['wa_status'] = s
            o['wa_failed_stages'] = '|'.join(str(x) for x in (rec.get('failed_stages') or []))
            wr = (wv.get('rows') or {}).get(r[key]) if s in WA_OK_STATUS else None
            if s in WA_OK_STATUS and wr is None:
                raise FillRefusal(f'{r[key]}: 배치 상태 {s} 인데 metrics_flat 행이 없다')
            #  J20-f 관문 — 상별 열을 실을 때 수확 JSON 에 n_types 가 없으면 거부 (mono 인지 모른다 — 반지름 이름을 그대로 싣지 않는다)
            phase_cols = [c for c in wa_take if wa_phase_specific(c)]
            nt = h.get('n_types')
            if phase_cols and wr is not None and nt is None:
                raise FillRefusal(f'{r[key]}: 수확 JSON 에 n_types 가 없다 — mono 인지 몰라 상별 웹앱 열 {phase_cols[:3]} 을 '
                                  '실을 수 없다 (J20-f · 반지름 이름을 그대로 싣지 않는다)')
            #  J20-k (B) — mono: 웹앱이 단일 AM 에 붙인 반지름 이름을 접촉 열에서 읽는다 (두 이름이 다 있으면 mono 행이 아니다)
            wname = None                                                  # 웹앱이 mono 의 AM 에 붙인 이름 (아래 QC 의 wp = porosity 와 다른 변수)
            o['wa_mono_phase_name_webapp'] = ''
            if dp is not None and wr is not None:
                toks = set()
                for k, v in wr.items():
                    if v not in (None, '') and wa_group_contact(k) and wa_phase_specific(k):
                        toks.update(WA_PHASE_TOKEN.findall(k))
                if len(toks) > 1:
                    raise FillRefusal(f'{r[key]}: 설계 mono ({r.get("block")}) 인데 웹앱 접촉 열에 AM_P · AM_S 두 이름 다 값이 있다 {sorted(toks)} — '
                                      'mono 행이 아니거나 다른 침대의 행이다 (J20-k (B))')
                wname = next(iter(toks)) if toks else None
                o['wa_mono_phase_name_webapp'] = wname or ''
                if wname is not None and wname != dp:
                    rep['wa_mono_renamed_cases'] += 1
            if wr is not None and any(wa_group_area(c) for c in wa_take):
                wr = _wa_area_prep(r[key], wr, rep)                         # ⑦A1 — 접촉 0 쌍 평균 = N/A (웹앱 원 행은 안 바꾼다 · J20-s)
            for c in wa_take:
                src, absent = c, False
                if dp is not None and wa_phase_specific(c):
                    absent = any(t == op for t in WA_PHASE_TOKEN.findall(c))     # 설계에 없는 상이 낀 열 → 빈칸 (N/A)
                    if not absent and wname is not None and wname != dp:
                        src = _phase_swap(c, dp, wname)                          # 설계 이름 칸 ← 웹앱 이름의 값
                v = None if (wr is None or absent) else wr.get(src)
                if absent and wr is not None:
                    rep['wa_mono_absent_blanked'] += 1
                elif dp is not None and wa_phase_specific(c) and v not in (None, ''):
                    rep['wa_mono_design_filled'] += 1
                _pm = ((WA_PAIR_COUNT.fullmatch(c) or WA_PAIR_TOTAL.fullmatch(c))
                       if (v in (None, '') and wr is not None and not absent) else None)
                if _pm is not None:
                    #  J20-h — 웹앱 행이 있는데 쌍 키가 없다 = 접촉 0.  두 상이 다 있어야 0 (없으면 N/A 빈칸) · 상을 모르면 거부 ·
                    #   mono 는 설계 상으로 판단 (J20-k (B) — 설계 상 = 수확 AM)
                    pc = h.get('phase_counts')
                    if not isinstance(pc, dict):
                        raise FillRefusal(f'{r[key]}: 수확 JSON 에 phase_counts 가 없다 — {c} 의 빈칸이 접촉 0 인지 상이 없는 것인지 '
                                          '가를 수 없다 (J20-h)')
                    if all(_phase_n_mono(pc, ph, dp) > 0 for ph in _pm.groups()):
                        if c.endswith('_n'):
                            v = '0'
                            rep['wa_pair_zero_filled'] += 1
                        else:                                            # ⑦ — 총합도 측정된 0 (평균은 N/A 로 둔다 · J20-s)
                            v = '0.0'
                            rep['wa_area_total_zero_filled'] += 1
                o[c] = '' if v is None else str(v)
            #  J20-i — 표에 함께 실린 평균 SE–SE CN 과 SE–SE 접촉 수가 같은 접촉 집합에서 왔는가: se_se_cn = 2 × area_SE_SE_n / N_SE
            #   (calc_se_se_cn 은 SE 전 입자로 나눈 평균 · 접촉 하나가 두 입자에 하나씩).  SE 입자 수를 모르거나 어긋나면 거부한다.
            if ('se_se_cn' in wa_take and 'area_SE_SE_n' in wa_take
                    and o.get('se_se_cn', '') != '' and o.get('area_SE_SE_n', '') != ''):
                pc = h.get('phase_counts')
                if not isinstance(pc, dict):
                    raise FillRefusal(f'{r[key]}: 수확 JSON 에 phase_counts 가 없다 — SE 입자 수를 몰라 se_se_cn = 2 × area_SE_SE_n / N_SE '
                                      '를 확인할 수 없다 (J20-i)')
                n_se = _phase_n(pc, 'SE')
                cn_v, n_pairs = float(o['se_se_cn']), float(o['area_SE_SE_n'])
                expect = 2.0 * n_pairs / n_se if n_se > 0 else float('nan')
                if not (n_se > 0 and abs(cn_v - expect) <= WA_CN_IDENTITY_TOL * max(1.0, abs(expect))):
                    raise FillRefusal(f'{r[key]}: se_se_cn {cn_v!r} ≠ 2 × area_SE_SE_n {n_pairs:g} / SE {n_se} = {expect!r} — '
                                      '같은 접촉 집합의 값이 아니다 (J20-i · 다른 프레임 · 다른 접촉 필터)')
                rep['wa_cn_identity_checked'] += 1
            #  J20-j — AM–AM: am_am_n_contacts = 웹앱 원 행의 AM–AM 쌍 개수 합 (없는 쌍 = 0 · J20-h 와 같은 뜻) ·
            #   am_am_cn = 2 × am_am_n_contacts / N_AM (calc_am_am_cn 은 AM 전 입자로 나눈 평균 · 접촉 하나가 두 입자에 하나씩).
            if 'am_am_n_contacts' in wa_take and o.get('am_am_n_contacts', '') != '':
                n_pairs_am = float(o['am_am_n_contacts'])
                s_pairs_am = sum(float(v) for k, v in wr.items() if WA_AM_AM_PAIR.fullmatch(k) and v not in (None, ''))
                if n_pairs_am != s_pairs_am:
                    raise FillRefusal(f'{r[key]}: am_am_n_contacts {n_pairs_am:g} ≠ AM–AM 쌍 개수 합 {s_pairs_am:g} — 같은 접촉 집합의 값이 아니다 (J20-j)')
                if 'am_am_cn' in wa_take and o.get('am_am_cn', '') != '':
                    pc = h.get('phase_counts')
                    if not isinstance(pc, dict):
                        raise FillRefusal(f'{r[key]}: 수확 JSON 에 phase_counts 가 없다 — AM 입자 수를 몰라 am_am_cn = 2 × am_am_n_contacts / '
                                          'N_AM 을 확인할 수 없다 (J20-j)')
                    n_am = _phase_n(pc, 'AM전체')
                    cn_am = float(o['am_am_cn'])
                    expect_am = 2.0 * n_pairs_am / n_am if n_am > 0 else float('nan')
                    if not (n_am > 0 and abs(cn_am - expect_am) <= WA_CN_IDENTITY_TOL * max(1.0, abs(expect_am))):
                        raise FillRefusal(f'{r[key]}: am_am_cn {cn_am!r} ≠ 2 × am_am_n_contacts {n_pairs_am:g} / AM {n_am} = {expect_am!r} — '
                                          '같은 접촉 집합의 값이 아니다 (J20-j)')
                rep['wa_am_identity_checked'] += 1
            #  7c — AM–SE CN · 고립 (G1–G7 · 상 있음/없음): 표에 실린 값들이 calc_am_isolation_risk 의 counts 하나에서 나왔는가
            if wr is not None and any(WA_AMSE_COL.fullmatch(c) for c in wa_take):
                rep['wa_amse_identity_checked'] += _wa_amse_gates(r[key], o, wa_take, h, dp, r)
            #  ② — 퍼콜레이션 (P1 관통 일관 + 수확기 독립 재현 · P2 범위 · P3 관통 SE 개수)
            if wr is not None and any(wa_group_perc(c) for c in wa_take):
                rep['wa_perc_checked'] += _wa_perc_gates(r[key], o, wa_take, h)
            #  ⑤⑥⑦ (J20-s) — 관문은 웹앱 원 행으로 잰다 (상 이름 옮기기와 무관한 항등식 · 같은 묶음의 짝 열이 표에 없어도 잰다)
            if wr is not None and any(wa_group_f1(c) for c in wa_take):
                rep['wa_f1_checked'] += _wa_f1_gates(r[key], wr, h)
            if wr is not None and any(wa_group_frac(c) for c in wa_take):
                rep['wa_frac_checked'] += _wa_frac_gates(r[key], wr)
            if wr is not None and any(wa_group_area(c) for c in wa_take):
                rep['wa_area_checked'] += _wa_area_gates(r[key], wr, h, r, wa_take)
            #  v1.1 ① — 경로 기준 고립 = 100 − 활성 (유도) · 웹앱 v1.1 이 같은 이름을 내면 같아야 · ①② 관문 D1–D5
            if wa_iso_on:
                a_ = o.get('ionic_active_pct', '')
                o['am_ionic_isolated_pct'] = repr(100.0 - float(a_)) if a_ not in ('', None) else ''
                w_iso = wr.get('am_ionic_isolated_pct') if wr is not None else None
                if w_iso not in (None, '') and a_ not in ('', None) and abs(float(w_iso) - (100.0 - float(a_))) > WA_PCT_SUM_TOL:
                    raise FillRefusal(f'{r[key]}: 웹앱 am_ionic_isolated_pct {w_iso} ≠ 100 − ionic_active_pct {a_} (v1.1 D1)')
                if wr is not None:
                    rep['wa_ionic_checked'] += _wa_ionic_gates(r[key], o, wa_take, h, dp)
            for name, wcol, hcol, _w in WA_QC:
                o[name] = ''
            if wr is not None:
                wp = wr.get('porosity_spheresum') or wr.get('porosity')
                if wp in (None, ''):
                    raise FillRefusal(f'{r[key]}: 웹앱 행에 porosity 가 없다 — 같은 프레임인지 확인할 수 없다')
                dpor = float(wp) - float(h['porosity_sphere_pct_RECORD_ONLY'])
                if abs(dpor) > WA_SAME_FRAME_TOL_PCT:
                    raise FillRefusal(f'{r[key]}: 웹앱 porosity − 수확 porosity = {dpor:+.4f} %p (> {WA_SAME_FRAME_TOL_PCT}) — '
                                      '다른 프레임 · 다른 메시의 웹앱 행이다')
                rep['wa_porosity_absmax'] = max(rep['wa_porosity_absmax'], abs(dpor))
                o['qc_wa_porosity_minus_harvest_pct'] = repr(dpor)
                for name, wcol, hcol, _w in WA_QC[1:]:
                    wc, hc = wcol, hcol
                    if dp is not None:                                   # J20-k (B) — 설계 상 칸 검산 = 웹앱 <웹앱 이름> − 수확 전체 · 없는 상 빈칸
                        toks_q = WA_PHASE_TOKEN.findall(name)
                        if any(t == op for t in toks_q):
                            continue
                        if any(t == dp for t in toks_q):
                            hc = 'coverage_AM_total_hertz_pct'
                            wc = _phase_swap(wcol, dp, wname) if (wname is not None and wname != dp) else wcol
                    a, b = wr.get(wc), h.get(hc)
                    st_h = (h.get('status') or {}).get(DESCRIPTOR_STATUS_KEY.get(hc, ''), '')
                    if a not in (None, '') and b is not None and st_h == 'OK':
                        o[name] = repr(float(a) - float(b))
        #  τ T3 — 벽 τ 와 ② 퍼콜레이션이 함께 실리면 비관통 판정이 같아야 한다 (수확기 벽 밴드 ↔ 웹앱 밴드 규칙 · SE 단분산이면 같은 집합 · J20-b F8)
        if tw_on and o.get('percolation_pct', '') not in ('', None):
            if (o.get('tortuosity_SE_wall_status') == 'NOT_PERCOLATING') != (float(o['percolation_pct']) == 0.0):
                raise FillRefusal(f'{r[key]}: 벽 τ 상태 {o.get("tortuosity_SE_wall_status")} ↔ 웹앱 percolation_pct {o["percolation_pct"]} — '
                                  '관통 판정이 어긋난다 (τ T3)')
            rep['tau_perc_crosschecked'] += 1
        out.append(o)
        rep['n'] += 1
    return out, cols, rep



def _selftest():
    ok, fail = 0, []

    def chk(n, c):
        nonlocal ok
        (ok := ok + 1) if c else fail.append(n)
        print(('  PASS  ' if c else '  FAIL  ') + n)

    rows = build(n_interior=40, n_end=8, seed=0, restarts=60)
    chk(f'① 행 수 = 40 + 8 + 8 ({len(rows)})', len(rows) == 56)
    bi = [r for r in rows if r['block'] == 'bimodal']
    #  ② 모든 값이 지정 범위 안
    inb = all(RANGES[f][0] - 1e-9 <= r[f] <= RANGES[f][1] + 1e-9 for r in bi for f in FACTORS)
    chk('② 내부 블록의 모든 인자가 지정 범위 안', inb)
    #  ③ ★ 대립 ≥ 소립 이 **구성상** 보장된다 (범위가 안 겹친다)
    chk('③ d_AM_P ≥ d_AM_S 가 모든 행에서 성립 (범위 비중첩)',
        all(r['d_am_p_um'] >= r['d_am_s_um'] for r in bi))
    #  ④ ★ 끝점 블록은 죽은 크기 인자에 좌표를 주지 않는다 (NaN)
    mp = [r for r in rows if r['block'] == 'mono_AM_P']
    ms = [r for r in rows if r['block'] == 'mono_AM_S']
    chk('④ ps=1 행은 d_AM_S 가 NaN (없는 상에 좌표를 안 준다)',
        all(np.isnan(r['d_am_s_um']) for r in mp) and all(r['ps_frac'] == 1.0 for r in mp))
    chk('④b ps=0 행은 d_AM_P 가 NaN',
        all(np.isnan(r['d_am_p_um']) for r in ms) and all(r['ps_frac'] == 0.0 for r in ms))
    #  ⑤ 반경 = 직경/2 (DEM 입력 규약)
    chk('⑤ r_* = d_*/2 (LIGGGHTS 입력은 반경)',
        all(abs(r['r_SE_um'] * 2 - r['d_se_um']) < 1e-12 for r in rows))
    #  ⑥ LHS 층화 — 각 인자가 n 개 층에 정확히 하나씩 (1-D 균일).
    #    ⚠ 이것은 **연속 LHS 의 성질**이다.  정수 격자에서는 수준 수 < n 이라 각 수준이
    #      복제되므로 성립할 수 없다 — 이산 대응물은 ⑩b(수준 점유 균형)다.
    #      ⇒ 이 검사는 연속 경로에 건다 (그 경로를 살려 두는 한 회귀로 유효하다).
    bic = [r for r in build(40, 8, 0, 60, grid=False) if r['block'] == 'bimodal']
    U = np.array([[(r[f] - RANGES[f][0]) / (RANGES[f][1] - RANGES[f][0]) for f in FACTORS]
                  for r in bic])
    strat = all(sorted((U[:, j] * len(bic)).astype(int)) == list(range(len(bic)))
                for j in range(len(FACTORS)) if FACTORS[j] != 'ps_frac')
    chk('⑥ (연속 모드) 각 인자가 n 개 층에 정확히 하나씩 — 이산 대응물은 ⑩b', strat)
    #  ⑦ 재현성 — 같은 seed 는 같은 설계
    chk('⑦ 같은 seed = 같은 설계 (재현 가능)',
        build(40, 8, 0, 60)[7]['d_am_p_um'] == rows[7]['d_am_p_um'])
    #  ⑧ 상관이 낮다 (설계행렬이 교락되지 않았다)
    dg = diagnostics(rows)
    #  ★★ 문턱을 0.35 → 0.30 으로 **조인다** (2026-08-18).  옛 판(maximin 만 최적화)은
    #    am_pct 눈금이 거칠어지자 0.37 까지 튀었다 — 그 회귀를 잡으려면 문턱이 그 아래여야 한다.
    #    현행 기준(상관 벌점 + 열내부 스왑)은 n 40/60 × seed 0–5 에서 전부 ≤ 0.247 이었다.
    chk(f"⑧ 최대 |비대각 상관| < 0.30 ({dg['max_abs_offdiag_corr']})",
        dg['max_abs_offdiag_corr'] < 0.30)
    #  ── ★ 정수 격자 회귀 (2026-08-18) ─────────────────────────────────────
    g = build(40, 8, 1, 60, grid=True)
    def onstep(v, st):
        return abs(v / st - round(v / st)) < 1e-9
    chk('⑨ 모든 크기·조성 값이 지정 눈금 위에 있다 (d 1 µm · SE 0.5 µm · AM 1 %)',
        all(onstep(r[f], STEP[f]) for r in g for f in FACTORS if not np.isnan(r[f])))
    chk('⑨b ps 가 0.1 눈금 → `ps_label` 이 반올림이 아니라 **정확**하다',
        all(abs(r['ps_frac'] * 10 - round(r['ps_frac'] * 10)) < 1e-9 for r in g))
    dgg = diagnostics(g)
    chk(f"⑩ 중복 설계점 0 ({dgg['duplicate_design_points']}건)",
        dgg['duplicate_design_points'] == 0)
    #  ★★ ⑩b 는 **제약이 없을 때**의 성질이다 (2026-08-18).  입자수 상한이 걸리면 후보 풀이
    #    잘려 완전 균형이 **원리적으로 불가능**하다 — `_balanced()` 가 만든 배치가 제약을
    #    위반하고, 위반 행을 갈아끼우면 균형이 깨진다.  ⇒ 두 경로로 나눈다:
    #      · 제약 없음 → 최대−최소 ≤ 1 (엄격, 옛 성질 그대로)
    #      · 제약 있음 → 편차가 기대 점유의 25 % 이내 (후보 풀이 허용하는 최선)
    #    실패한 테스트를 **지우지 않고 적용 범위를 좁힌다** (⑥ 과 같은 처리).
    def _spread(dg_):
        return {k: (int(v.split('점유 ')[1].split('–')[1])
                    - int(v.split('점유 ')[1].split('–')[0]))
                for k, v in dg_['levels'].items()}
    _LVf = [levels_of(f, PS_INTERIOR) for f in FACTORS]
    _constrained = len(feasible_combos(FACTORS, _LVf)) < int(np.prod([len(x) for x in _LVf]))
    if not _constrained:
        chk('⑩b (제약 없음) 수준 점유 최대−최소 ≤ 1', all(v <= 1 for v in _spread(dgg).values()))
    else:
        _n = len([r for r in g if r['block'] == 'bimodal'])
        #  허용폭 = max(2, 기대점유의 25 %).  2 는 이상적 배분 ±1 = 이산 배정의 자연 여유이고,
        #  큰 n 에서는 25 % 가 이긴다 (n=100·11수준이면 기대 9.09 → 허용 2.27).
        _tol = {k: max(2, 0.25 * _n / len(levels_of(k, PS_INTERIOR))) for k in FACTORS}
        _sp = _spread(dgg)
        chk(f'⑩b (제약 있음) 수준 점유 편차가 기대의 25 % 이내 {_sp}',
            all(_sp[k] <= _tol[k] for k in _sp))
        #  ⑩d 제약이 실제로 걸려 있는지 (안 걸렸는데 느슨한 검사를 쓰면 안 된다)
        chk(f'⑩d 제약이 실제로 후보를 자른다 '
            f'({len(feasible_combos(FACTORS, _LVf)):,} / {int(np.prod([len(x) for x in _LVf])):,})',
            True)
    #  ⑩c ★ 기준이 **상관을 실제로 본다** — 순수 maximin 대비 개선되는가.
    #      (옛 결함의 직접 회귀: maximin 만 쓰면 상관이 운에 맡겨진다)
    rng_ = np.random.default_rng(7)
    LV = [levels_of(f, PS_INTERIOR) for f in FACTORS]
    pure, pure_d = None, -1.0                                # 순수 maximin 재현
    for _ in range(400):
        Ic = np.stack([_balanced(40, len(LV[j]), rng_) for j in range(len(LV))], 1)
        _, md = _score(_unit(Ic, LV))
        if md > pure_d:
            pure, pure_d = Ic, md
    mc_pure, _ = _score(_unit(pure, LV))
    mc_new, _ = _score(_unit(lhs_grid(40, LV, np.random.default_rng(7), 400), LV))
    chk(f'⑩c 상관-인지 기준이 순수 maximin 보다 낫다 ({mc_new:.3f} < {mc_pure:.3f})',
        mc_new < mc_pure)
    #  ⑫ ★ 입자수 상한 — 모든 행이 N_TOTAL_CAP 이하 (지시 2026-08-18)
    chk(f'⑫ 모든 행이 입자 {N_TOTAL_CAP:,} 이하 '
        f"(최대 {max(r['n_total_est'] for r in g):,.0f})",
        all(r['n_total_est'] <= N_TOTAL_CAP for r in g))
    #  ⑪ 연속 모드도 여전히 된다 (되돌릴 길을 남긴다)
    c = build(20, 4, 0, 40, grid=False)
    chk('⑪ --continuous 경로 보존 (눈금 밖 값이 나온다)',
        any(not onstep(r['d_am_p_um'], 1.0) for r in c if not np.isnan(r['d_am_p_um'])))
    #  ── ★★ `LHS-01` 회귀 (2026-09-15) ─────────────────────────────────────
    #    규율 ②: 결함을 재현하는 검사를 **먼저** 세우고 고친다.  옛 코드는 ⑬·⑬b 를
    #    **둘 다** 실패했다 (열 이름이 `se_percolation` · 플래그에 `se_` 접합).
    chk('⑬ SE 퍼콜 **추정** 열 이름이 규약을 담는다 (`_est_meanfield`)',
        all('se_percolation_est_meanfield' in r and 'se_percolation' not in r for r in rows))
    #  ⑬b **기하 플래그가 물리 추정을 나르지 않는다** — 두 종류를 한 열에 접합하면
    #      "유한크기가 깨끗한데 플래그가 켜진 행" 과 구별이 불가능해진다.
    chk('⑬b finite_size_flag 에 `se_` 조각이 하나도 없다 (기하 ↔ 물리추정 분리)',
        not any(t.startswith('se_') for r in rows
                for t in (r['finite_size_flag'].split('+') if r['finite_size_flag'] else [])))
    #  ⑬c ★ 분리가 **정보를 잃지 않는다** — 두 열을 합치면 옛 열이 정확히 복원된다.
    def _legacy(r):
        return '+'.join([t for t in (r['finite_size_flag'].split('+')
                                     if r['finite_size_flag'] else [])]
                        + ([r['se_perc_est_flag']] if r['se_perc_est_flag'] else []))
    chk('⑬c 두 열을 합치면 옛 `finite_size_flag` 가 정확히 복원된다 (무손실 분리)',
        all(_legacy(r) == '+'.join(
            [t for t in ([] if not r['finite_size_flag'] else r['finite_size_flag'].split('+'))]
            + ([] if r['se_percolation_est_meanfield'] == 'OK'
               else ['se_' + r['se_percolation_est_meanfield']])) for r in rows))
    #  ⑬d ★★ **실측 상수가 자기 원자료와 일치한다** — 숫자를 주석에 손으로 적고 끝내면
    #      원자료가 바뀌어도 아무도 모른다 (규율 ④: 정본은 밖으로 강제되지 않으면 샌다).
    #      원자료가 없으면 **건너뛰지 않고 실패**한다 (fail-closed).
    _mp = pathlib.Path(__file__).resolve().parent.parent / LHS_PERC_MEASURED['source']
    if _mp.exists():
        #  ⚠ 파일 머리에 `#` 출처 주석이 있다 — 그것을 헤더로 읽으면 **조용히 0행**이 되고
        #    검사가 통과해 버린다 (규율 ⑤ false-green).  주석은 명시적으로 걷어낸다.
        _rows = list(csv.DictReader(
            [ln for ln in _mp.read_text(encoding='utf-8').splitlines()
             if not ln.startswith('#')]))
        _agg = {}
        for _r in _rows:
            _k = _r['se_percolation_est_meanfield']
            _a = _agg.setdefault(_k, [0, 0])
            _a[0] += 1
            _a[1] += (_r['ionic_percolates'] == 'False')
        _hit = (len(_rows) == LHS_PERC_MEASURED['n_measured']
                and all(_agg.get(k, [0, 0]) == [v['n'], v['blocked']]
                        for k, v in LHS_PERC_MEASURED.items()
                        if isinstance(v, dict) and 'blocked' in v))
        chk(f'⑬d LHS_PERC_MEASURED 가 원자료와 일치한다 '
            f'(n={len(_rows)} · {({k: v for k, v in _agg.items()})})', _hit)
    else:
        chk(f'⑬d 실측 원자료가 있다 ({LHS_PERC_MEASURED["source"]})', False)
    #  ── ★★ `LHS-02` 회귀 (2026-09-15) ─────────────────────────────────────
    #    ⑭ **0 을 결측으로 세지 않는다** — 그렇게 세면 검사기가 `DESC-05` 결함을 재생산한다
    #      (*"없는 AM_P → N/A · 존재하는데 무접촉 → 0.0"*).  합성 3행으로 직접 가른다.
    _probe = [{c: '' for c in DESCRIPTORS}, {c: 0.0 for c in DESCRIPTORS},
              {c: float('nan') for c in DESCRIPTORS}]
    _f3 = descriptor_fill(_probe)
    chk(f'⑭ 채움 계수가 0.0 은 **측정으로**, ""·NaN 은 **결측으로** 센다 ({_f3["phi_se"]}/3 = 1)',
        all(v == 1 for v in _f3.values()))
    #  ⑭b **읽기 전 가드가 실제로 거부한다** — 있기만 하고 안 막으면 없는 것과 같다.
    try:
        require_descriptors(_probe, ['phi_se'], 'probe')
        _refused = ''
    except ValueError as e:
        _refused = str(e)
    chk(f'⑭b require_descriptors 가 결측을 **거부**한다 ({_refused[:48]}…)',
        'phi_se 1/3' in _refused and '0 으로 채우지 말 것' in _refused)
    #  ⑭c ★ 그리고 **완전한 행은 통과시킨다** (거부만 하면 그것도 결함이다 — 양방향 확인)
    try:
        require_descriptors([{c: 1.0 for c in DESCRIPTORS}], DESCRIPTORS, 'full')
        _passed = True
    except ValueError:
        _passed = False
    chk('⑭c 완전한 행은 통과시킨다 (거부 과잉이 아니다)', _passed)
    #  ⑮ `LHS-02` 병합 — **거부가 실재하는가** (거부 로직은 안 쏘면 장식이다)
    def _h(case, **kw):
        """최소 수확 fixture — 기본은 전부 OK 인 정상 건."""
        b = dict(case=case, timestep=100, phi_se=0.2, phi_am=0.3,
                 porosity_sphere_pct_RECORD_ONLY=50.0,
                 coverage_AM_P_hertz_pct=10.0, coverage_AM_S_hertz_pct=20.0,
                 coverage_AM_total_hertz_pct=17.5,     # (1·10 + 3·20)/4 = 17.5
                 tortuosity_dijkstra_SE=1.5,
                 status=dict(phi='OK', porosity='OK', coverage_AM_P='OK',
                             coverage_AM_S='OK', coverage_AM_total='OK', tortuosity='OK'),
                 coverage_detail=dict(counts={'AM_P': {'n_valid': 1}, 'AM_S': {'n_valid': 3}}),
                 raw=dict(atom=dict(sha256='a' * 64), contact=dict(sha256='b' * 64)),
                 _file=case + '.json', _sha256='c' * 64)
        b.update(kw)
        return b

    def _neg(name, fn):
        nonlocal ok
        try:
            fn()
        except FillRefusal as e:
            ok += 1
            print(f'  PASS  {name} — 거부: {str(e)[:64]}')
            return
        except Exception as e:                                    # noqa: BLE001
            chk(f'{name} (기대 FillRefusal, 실제 {type(e).__name__}: {e})', False)
            return
        chk(f'{name} (거부하지 않았다)', False)

    _dr = [{'case_id': 'c1'}, {'case_id': 'c2'}]
    _hv = {'c1': _h('c1'), 'c2': _h('c2')}
    _r2, _rp = fill_descriptors([dict(x) for x in _dr], _hv)
    chk('⑮ 정상 건은 일곱 열이 전부 찬다',
        all(_rp['filled'][c] == 2 for c in DESCRIPTORS))
    chk('⑮ 값이 왕복 가능한 정밀도로 쓰인다 (반올림 손실 없음)',
        float(_r2[0]['phi_se']) == 0.2 and _r2[0]['phi_se_status'] == 'OK')
    #  ── ⑰ HND-04 (Codex 09-25 · 비준 09-25): 인계표가 벽 QC · 적격성 · 규약 ID · sha 를 실어 나른다 · 음수도 원값 보존 ──
    _hn = _h('c1', phi_se=0.5135813340456643, phi_am=0.4996409958699752,
             porosity_sphere_pct_RECORD_ONLY=-1.3222329915639541)          # = lhs00_005 실측 (Codex 반례)
    _hn['handover_qc'] = dict(calculation_status='OK', physical_target_status='HOLD',
                              hold_reason_codes='NEGATIVE_POROSITY|BOUNDARY_CENTER_OUT', phi_sum_gt_one=True,
                              thickness_wall_gap_um=45.9, n_floor_center_out=4,
                              boundary_model_id='floor=primitive_zplane_type3|platen=mesh_stl',
                              measurement_protocol_id='harvest_v2_20260925/spheresum_nominal_gap/wall_z0',
                              deck_sha256='d' * 64, contact_sha256='b' * 64, mesh_sha256='m' * 64)
    _hn['deck_floor'] = dict(z=0.0, wall_type=3)
    try:
        _on, _cn, _repn = build_handover([{'case_id': 'c1'}], {'c1': _hn})
        _row = _on[0]
    except Exception as e:                                                # noqa: BLE001
        _row, _cn = {'_err': f'{type(e).__name__}: {e}'}, []
    chk('⑰ HND-04: 음수 porosity · φ 합 > 1 도 **원값 그대로** 나간다 (0 접기 · 빈칸 아님)',
        _row.get('phi_se') == repr(0.5135813340456643)
        and _row.get('porosity_sphere_pct_RECORD_ONLY') == repr(-1.3222329915639541))
    chk('⑰ HND-04: 계산 상태 OK 와 별도로 physical_target_status HOLD · 보류 코드 · phi_sum_gt_one 이 열로 나간다',
        _row.get('phi_se_status') == 'OK' and _row.get('physical_target_status') == 'HOLD'
        and 'NEGATIVE_POROSITY' in (_row.get('hold_reason_codes') or '') and _row.get('phi_sum_gt_one') == 'True')
    chk('⑰ HND-04: 두께 µm · 벽 QC · 규약 ID · deck/contact/mesh sha · 덱 바닥 z 가 열에 있다',
        _row.get('thickness_wall_gap_um') == '45.9' and _row.get('n_floor_center_out') == '4'
        and bool(_row.get('boundary_model_id')) and bool(_row.get('measurement_protocol_id'))
        and len(_row.get('deck_sha256') or '') == 64 and _row.get('deck_floor_z_sim') == '0.0')
    _dh = pathlib.Path(__file__).resolve().parent.parent / str(globals().get('DEFAULT_HARVEST_DIR', ''))
    _dj = sorted(_dh.glob('lhs*.json'))[:1] if _dh.is_dir() else []
    chk('⑰ HND-04 · J19: 기본 수확 디렉터리 = 20260925 판 — 그 JSON 에 handover_qc 가 **실제로** 있다 (0924 판은 없어 HND-04 열이 빈칸이었다)',
        'lhs_descriptors_20260925' in str(globals().get('DEFAULT_HARVEST_DIR', ''))
        and bool(_dj) and 'handover_qc' in json.loads(_dj[0].read_text(encoding='utf-8')))
    #  ★ `DESC-09` — 반쪽 채움 금지 (양방향)
    _neg('⑮a DESC-09: 수확에 없는 설계가 있으면 거부',
         lambda: fill_descriptors([{'case_id': 'c1'}, {'case_id': 'zz'}], _hv))
    _neg('⑮a DESC-09: 설계에 없는 수확이 있으면 거부',
         lambda: fill_descriptors([{'case_id': 'c1'}], _hv))
    #  ★ `DESC-07` — 두 항등식이 병합 시점에 **다시** 검증된다
    _neg('⑮b DESC-07①: porosity 가 φ 둘에서 안 나오면 거부',
         lambda: fill_descriptors([{'case_id': 'c1'}],
                                  {'c1': _h('c1', porosity_sphere_pct_RECORD_ONLY=49.0)}))
    _neg('⑮b DESC-07②: C_total 이 입자수 가중평균이 아니면 거부',
         lambda: fill_descriptors([{'case_id': 'c1'}],
                                  {'c1': _h('c1', coverage_AM_total_hertz_pct=15.0)}))
    #  ★ `GAP2-05` — 실패에 숫자가 붙거나, 성공에 값이 없으면 거부
    _neg('⑮c GAP2-05: status≠OK 인데 값이 있으면 거부',
         lambda: fill_descriptors(
             [{'case_id': 'c1'}],
             {'c1': _h('c1', status=dict(phi='OK', porosity='OK', coverage_AM_P='OK',
                                         coverage_AM_S='OK', coverage_AM_total='OK',
                                         tortuosity='NOT_PERCOLATING'))}))
    _neg('⑮c status 가 OK 인데 값이 없으면 거부',
         lambda: fill_descriptors([{'case_id': 'c1'}],
                                  {'c1': _h('c1', tortuosity_dijkstra_SE=None)}))
    #  ★ 그리고 실패 칸은 **빈 칸 + 사유**다 — 0 이 아니다 (이 한 줄이 GAP2-05 그 자체)
    _hf = _h('c1', tortuosity_dijkstra_SE=None,
             status=dict(phi='OK', porosity='OK', coverage_AM_P='OK', coverage_AM_S='OK',
                         coverage_AM_total='OK', tortuosity='NOT_PERCOLATING'))
    _r3, _rp3 = fill_descriptors([{'case_id': 'c1'}], {'c1': _hf})
    chk('⑮d 실패 칸은 빈 칸이고 사유가 옆에 붙는다 (0 이 아니다)',
        _r3[0]['tortuosity_dijkstra_SE'] == ''
        and _r3[0]['tortuosity_dijkstra_SE_status'] == 'NOT_PERCOLATING'
        and _rp3['filled']['tortuosity_dijkstra_SE'] == 0)
    chk('⑮d 그 행의 다른 여섯 열은 그대로 찬다 (DESC-01: 한 타깃 실패로 행을 안 버린다)',
        all(_rp3['filled'][c] == 1 for c in DESCRIPTORS if c != 'tortuosity_dijkstra_SE'))
    #  ★ `DESC-08` — 291 코퍼스를 읽는 코드가 이 파일에 없다 (정적, AST)
    #  ⚠ 소박한 `낱말 not in src` 는 **자기 자신을 탐지한다** (이 검사문에 그 낱말이 있다).
    #    초판이 실제로 그렇게 FAIL 했다.  그리고 docstring 구분자로 자르는 방식은 **첫 함수
    #    docstring 까지만** 보므로 뒤쪽 본문을 통째로 놓친다 = false-green.  ⇒ AST 로
    #    **문자열 상수의 자리**를 보고, 모듈 docstring 과 이 selftest 는 제외한다.
    _tree = ast.parse(pathlib.Path(__file__).read_text(encoding='utf-8'))
    _skip = set()
    if (_tree.body and isinstance(_tree.body[0], ast.Expr)
            and isinstance(_tree.body[0].value, ast.Constant)):
        _d = _tree.body[0].value
        _skip |= set(range(_d.lineno, (_d.end_lineno or _d.lineno) + 1))
    for _n in ast.walk(_tree):
        if isinstance(_n, ast.FunctionDef) and _n.name == '_selftest':
            _skip |= set(range(_n.lineno, (_n.end_lineno or _n.lineno) + 1))
    _needle = 'design_performance' + '_corpus'
    _hits = sorted({_n.lineno for _n in ast.walk(_tree)
                    if isinstance(_n, ast.Constant) and isinstance(_n.value, str)
                    and _needle in _n.value and _n.lineno not in _skip})
    chk(f'⑮e DESC-08: 291 코퍼스 경로가 코드에 없다 (AST · docstring/selftest 제외; 적중 {_hits})',
        not _hits)
    #  ★ 그 검사가 **실제로 쏘는지** — 같은 판정기에 심은 참조를 먹여 본다 (변이 대조)
    _mut = ast.parse('def f():\n    return open("docs/data/' + _needle + '.csv")\n')
    _mhits = [_n.lineno for _n in ast.walk(_mut)
              if isinstance(_n, ast.Constant) and isinstance(_n.value, str)
              and _needle in _n.value]
    chk('⑮e 그 정적 검사가 장식이 아니다 (심은 참조를 잡는다)', len(_mhits) == 1)

    #  ⑭d ★★ **동결 설계 CSV 의 채움 상태를 수치로 못박는다.**  누가 채우면 이 검사가
    #      실패하면서 알려 준다 — "아무도 안 봤다" 를 "리포가 본다" 로 바꾸는 자리다.
    _dp = pathlib.Path(__file__).resolve().parent.parent / DESCRIPTOR_FILL_EXPECTED['path']
    if _dp.exists():
        _dr = list(csv.DictReader(_dp.open(encoding='utf-8-sig')))
        _df = descriptor_fill(_dr)
        chk(f'⑭d 동결 설계 CSV 채움 상태가 등록값과 일치 '
            f'({len(_dr)}행 · 채움 {sorted(set(_df.values()))})',
            len(_dr) == DESCRIPTOR_FILL_EXPECTED['n_rows']
            and _df == DESCRIPTOR_FILL_EXPECTED['filled'])
    else:
        chk(f'⑭d 동결 설계 CSV 가 있다 ({DESCRIPTOR_FILL_EXPECTED["path"]})', False)

    #  ═══ ⑯ 인계표 계약 (`build_handover`) — 규율 ② 대로 **먼저** 쓴 시험 ═══════════
    def _hrow(case, tau_ok=False, mono=False):
        """수확 한 건을 최소로 흉내낸다.  mono = 수확기의 2-type 모양 (상 라벨 `AM` 하나 · coverage 상별 둘 다 N_A_PHASE_ABSENT ·
        `coverage_AM_only` = 전체 — 실측 0925 130/64 JSON 과 같은 모양)."""
        phi_se, phi_am = 0.20, 0.50
        return {
            'case': case, 'timestep': 100, 'plate_z_sim': 0.04, 'plate_z_source': 'mesh_stl',
            'V_box_sim': 1.0e-4, 'area_channel': 'dem_geometric_c_cpl22 …', 'closure_residual': 0.0,
            'phi_se': phi_se, 'phi_am': phi_am,
            'porosity_sphere_pct_RECORD_ONLY': 100.0 * (1 - phi_se - phi_am),
            'n_types': (2 if mono else 3),
            'phase_counts': ({'AM': 7, 'SE': 50} if mono else {'AM_P': 5, 'AM_S': 9, 'SE': 50}),
            'coverage_AM_P_hertz_pct': (None if mono else 11.0),
            'coverage_AM_S_hertz_pct': (None if mono else 22.0),
            'coverage_AM_only_hertz_pct': (20.0 if mono else None),
            'coverage_AM_total_hertz_pct': 20.0,
            'tortuosity_dijkstra_SE': (1.5 if tau_ok else None),
            'status': {'phi': 'OK', 'porosity': 'OK',
                       'coverage_AM_P': ('N_A_PHASE_ABSENT' if mono else 'OK'),
                       'coverage_AM_S': ('N_A_PHASE_ABSENT' if mono else 'OK'), 'coverage_AM_total': 'OK',
                       'tortuosity': ('OK' if tau_ok else 'NOT_PERCOLATING')},
            'tau_detail': {'n_sampled': 7, 'n_valid': (7 if tau_ok else 0), 'n_truncated': 0,
                           'tau_convention': 'harvest_v1/…'},
            'coverage_detail': {'n_capped': 0, 'n_free_surface_invalid': 0,
                                'counts': {'AM_P': {'n_valid': (0 if mono else 5)},
                                           'AM_S': {'n_valid': (0 if mono else 9)},
                                           'AM': {'n_valid': (7 if mono else 0)}}},
            'raw': {'atom': {'sha256': 'deadbeef'}},
        }
    _drows = [{'case_id': 'c1', 'block': 'bimodal', 'd_am_p_um': 5.0, 'am_pct': 80.0},
              {'case_id': 'c2', 'block': 'mono_AM_P', 'd_am_p_um': 9.0, 'am_pct': 90.0}]
    _harv = [_hrow('c1', tau_ok=True), _hrow('c2', mono=True)]
    _o, _c, _rep = build_handover(_drows, _harv)
    chk('⑯a 행 수 보존 (2)', len(_o) == 2)
    #  ★ 계약 ① — τ 값 열이 **없어야** 한다 (있으면 학습에 들어간다)
    chk('⑯b τ 값 열이 인계표에 없다', 'tortuosity_dijkstra_SE' not in _c)
    chk('⑯c 대신 τ 진단 열이 있다',
        all(k in _c for k in ('tau_status', 'tau_n_valid', 'tau_convention')))
    #  ★ 계약 ② — status != OK 는 **빈칸**이고 0 이 아니다.  ★ J20-k (B) (1저자 09-30 *"인계할때는 중복되더라도 잘 채워서"* · J20-f (A) 개정):
    #    mono 는 **설계 상 칸** (block mono_AM_P → AM_P) 에 단일 AM 값 (= 전체 열) 을 싣고, 설계에 없는 상 (AM_S) 의 칸은 빈칸 (N/A · 0 아님).
    #    수확기 열 전부 같은 규칙 — coverage 상별 · n_AM_*_measured (LHS-21 해소) · cov_*_n_valid.
    _mono = [r for r in _o if r['case_id'] == 'c2'][0]
    chk('⑯d ★ J20-k (B) mono_AM_P — coverage_AM_P 칸 = 전체 값 (status OK) · AM_S 칸 빈칸 (N_A_PHASE_ABSENT · 0 아님) · '
        'n_AM_P_measured = phase_counts.AM · n_AM_S_measured 빈칸 · cov_AM_P_n_valid = counts.AM · 보고 mono_rows',
        _mono['coverage_AM_P_hertz_pct'] == repr(20.0) and _mono['coverage_AM_P_hertz_pct_status'] == 'OK'
        and _mono['coverage_AM_S_hertz_pct'] == '' and _mono['coverage_AM_S_hertz_pct_status'] == 'N_A_PHASE_ABSENT'
        and _mono['coverage_AM_total_hertz_pct'] == repr(20.0)
        and _mono['n_AM_P_measured'] == '7' and _mono['n_AM_S_measured'] == '' and _mono['n_SE_measured'] == '50'
        and _mono['cov_AM_P_n_valid'] == '7' and _mono['cov_AM_S_n_valid'] == ''
        and _rep.get('mono_rows') == 1)
    _bim = [r for r in _o if r['case_id'] == 'c1'][0]
    chk('⑯d1 bimodal 은 그대로 — 상별 값 둘 다 · n_AM_P/S_measured = phase_counts',
        _bim['coverage_AM_P_hertz_pct'] == repr(11.0) and _bim['coverage_AM_S_hertz_pct'] == repr(22.0)
        and _bim['n_AM_P_measured'] == '5' and _bim['n_AM_S_measured'] == '9' and _bim['cov_AM_S_n_valid'] == '9')
    _drows_s = [dict(_drows[0]), dict(_drows[1], block='mono_AM_S')]
    _mono_s = [r for r in build_handover(_drows_s, _harv)[0] if r['case_id'] == 'c2'][0]
    chk('⑯d2 mono_AM_S 는 거울 — AM_S 칸에 값 · AM_P 칸 빈칸',
        _mono_s['coverage_AM_S_hertz_pct'] == repr(20.0) and _mono_s['coverage_AM_S_hertz_pct_status'] == 'OK'
        and _mono_s['coverage_AM_P_hertz_pct'] == '' and _mono_s['coverage_AM_P_hertz_pct_status'] == 'N_A_PHASE_ABSENT'
        and _mono_s['n_AM_S_measured'] == '7' and _mono_s['n_AM_P_measured'] == ''
        and _mono_s['cov_AM_S_n_valid'] == '7' and _mono_s['cov_AM_P_n_valid'] == '')
    #  ★ (B) 는 설계 block 과 수확 모양이 맞을 때만 — 어긋나거나 모르면 거부 (조용히 (A) 로 돌아가면 한 표에 규약이 섞인다)
    _neg('⑯d3 설계 block mono_AM_P 인데 수확 n_types 3 이면 거부',
         lambda: build_handover(_drows, [_hrow('c1', tau_ok=True), dict(_hrow('c2', mono=True), n_types=3)]))
    _neg('⑯d4 수확 n_types 2 인데 설계 block bimodal 이면 거부',
         lambda: build_handover([dict(_drows[0]), dict(_drows[1], block='bimodal')], _harv))
    _neg('⑯d5 수확 n_types 2 인데 설계행에 block 이 없으면 거부 (설계 상을 모른다)',
         lambda: build_handover([dict(_drows[0]), {k: v for k, v in _drows[1].items() if k != 'block'}], _harv))
    _neg('⑯d6 mono 인데 수확 coverage_AM_S 상태가 N_A_PHASE_ABSENT 가 아니면 거부 (mono 모양이 아니다)',
         lambda: build_handover(_drows, [_hrow('c1', tau_ok=True),
                                         dict(_hrow('c2', mono=True), coverage_AM_S_hertz_pct=22.0,
                                              status=dict(_hrow('c2', mono=True)['status'], coverage_AM_S='OK'))]))
    _neg('⑯d7 설계 block mono 인데 수확 JSON 에 n_types 가 없으면 거부',
         lambda: build_handover(_drows, [_hrow('c1', tau_ok=True), {k: v for k, v in _hrow('c2', mono=True).items() if k != 'n_types'}]))
    _neg('⑯d8 mono 인데 coverage_AM_only ≠ coverage_AM_total 이면 거부 (단일 AM = 전체 항등식)',
         lambda: build_handover(_drows, [_hrow('c1', tau_ok=True), dict(_hrow('c2', mono=True), coverage_AM_only_hertz_pct=19.0)]))
    _neg('⑯d9 mono 인데 phase_counts 에 AM_P 가 있으면 거부 (수확기 mono 라벨은 AM 하나)',
         lambda: build_handover(_drows, [_hrow('c1', tau_ok=True), dict(_hrow('c2', mono=True), phase_counts={'AM': 4, 'AM_P': 3, 'SE': 50})]))
    _neg('⑯d10 설계 block 이 모르는 mono 라벨 (mono_AM) 이면 거부',
         lambda: build_handover([dict(_drows[0]), dict(_drows[1], block='mono_AM')], _harv))
    chk('⑯e 값 칸마다 _status 짝이 있다',
        all(v + '_status' in _c for v in HANDOVER_VALUE_COLS))
    #  ★ 실측 입자수가 설계 추정과 **다른 열**로 들어간다
    chk('⑯f 실측 입자수 열이 있다',
        all(k in _c for k in ('n_AM_P_measured', 'n_SE_measured', 'cov_AM_P_n_valid')))
    #  ★ 변이 대조 1 — 항등식을 깨면 **거부**해야 한다 (안 깨지면 시험이 무의미)
    _bad = [_hrow('c1', tau_ok=True), _hrow('c2', mono=True)]
    _bad[0]['porosity_sphere_pct_RECORD_ONLY'] += 1.0
    try:
        build_handover(_drows, _bad); _r1 = False
    except FillRefusal:
        _r1 = True
    chk('⑯g 변이① DESC-07 항등식을 깨면 거부한다', _r1)
    #  ★ 변이 대조 2 — 수확이 모자라면 **부분 인계 금지**
    try:
        build_handover(_drows, [_hrow('c1')]); _r2 = False
    except FillRefusal:
        _r2 = True
    chk('⑯h 변이② 수확 누락 시 부분 인계를 거부한다', _r2)
    #  ★ 보류 사유가 **기계가 읽는 자리**에 있다 (산문에만 있으면 낡는다)
    #  ★ 변이 대조 3 — **프로덕션 모양(dict)** 으로도 같은 결과여야 한다
    _od, _cd, _ = build_handover(_drows, {h['case']: h for h in _harv})
    chk('⑯j dict 모양(load_harvest 산출)으로도 동일', _od == _o and _cd == _c)
    chk('⑯i 보류 열과 사유가 등록돼 있다',
        'tortuosity_dijkstra_SE' in HANDOVER_HELD_BACK
        and 'LHS-08' in HANDOVER_HELD_BACK['tortuosity_dijkstra_SE'])

    #  ═══ ⑱ J19 (1저자 비준 09-28) — 겹침 보정 porosity 를 **병기** (구 부피 합 열 유지 · 교체 아님) ═══════════════════
    #   union TSV (scripts/lhs_union_webapp.py 산출) 를 수확과 **짝지어** 붙인다.  짝이 맞는지 (같은 수확 · 같은 프레임) 를
    #   구 부피 합 porosity · 두께 · 상별 입자 수로 다시 재고, 어긋나면 거부한다 — 다른 수확 · 다른 프레임의 union 을 붙이지 않는다.
    def _hq(case, eps_s=11.0, th=34.0, n_se=100, n_p=1, n_s=10):
        h = _h(case, porosity_sphere_pct_RECORD_ONLY=eps_s, phi_se=0.5, phi_am=0.5 - eps_s / 100.0)
        h['phase_counts'] = {'AM_P': n_p, 'AM_S': n_s, 'SE': n_se}
        h['handover_qc'] = {'thickness_wall_gap_um': th}
        h['n_types'] = 3                                      # J20-f — 수확 JSON 의 type 수 (bimodal)
        return h

    def _u(case, eps_s=11.0, th=34.0, eps_u=14.0, se=0.6, n_se=100, n_am=11, status='OK', ub='True'):
        return {'case': case, 'eps_sphere_web': repr(eps_s), 'thickness_um': repr(th), 'mc_void_pct': repr(eps_u),
                'mc_void_se_pct': '0.014', 'eps_union_pair_clipped': repr(eps_u + 0.004), 'pair_upper_bound_ok': ub,
                'se_of_solid_vol': repr(se), 'n_SE': str(n_se), 'n_AM': str(n_am), 'status': status}
    _dq = [{'case_id': 'q1'}, {'case_id': 'q2'}]
    _hqs = {'q1': _hq('q1', eps_s=-2.0, th=30.0), 'q2': _hq('q2', eps_s=20.0, th=40.0)}
    _uq = {'q1': _u('q1', eps_s=-2.0, th=30.0, eps_u=6.5, se=0.62), 'q2': _u('q2', eps_s=20.0, th=40.0, eps_u=21.0, se=0.25),
           'perc': _u('perc', status='MISSING')}
    try:
        _oq, _cq, _rq = build_handover(_dq, _hqs, union=_uq)
        _eq = ''
    except Exception as e:                                                # noqa: BLE001
        _oq, _cq, _rq, _eq = [], [], {}, f'{type(e).__name__}: {e}'
    _q1 = next((r for r in _oq if r['case_id'] == 'q1'), {})
    _q2 = next((r for r in _oq if r['case_id'] == 'q2'), {})
    chk('⑱a J19 union 열 · 질량 보존 두께 · SE-rich 표지 (+ 통계 오차 · 쌍 렌즈 검산 · SE/고체 연속값) 가 인계표에 있다' + (f' — {_eq}' if _eq else ''),
        not _eq and all(c in _cq for c in ('porosity_union_exact_pct', 'porosity_union_exact_se_pct', 'porosity_union_pair_clipped_pct',
                                            'union_pair_upper_bound_ok', 'se_of_solid_vol', 'thickness_mass_conserving_um', 'se_rich')))
    chk('⑱b 병기 — 구 부피 합 열 (porosity_sphere_pct_RECORD_ONLY) 은 **원값 그대로** 남는다 (음수 −2.0 도 · 교체 아님)',
        _q1.get('porosity_sphere_pct_RECORD_ONLY') == repr(-2.0) and _q1.get('porosity_union_exact_pct') == repr(6.5))
    chk('⑱c 질량 보존 두께 = 두께 × (1 − ε_sphere)/(1 − ε_union) (같은 고체를 union 공극률로 받을 때의 두께)',
        _q1.get('thickness_mass_conserving_um') == repr(30.0 * (1 - (-2.0) / 100) / (1 - 6.5 / 100)))
    chk(f'⑱d SE-rich 표지 = SE/고체 ≥ {globals().get("SE_RICH_MIN")} (0.62 → True · 0.25 → False) · 연속값도 함께',
        _q1.get('se_rich') == 'True' and _q2.get('se_rich') == 'False' and _q1.get('se_of_solid_vol') == repr(0.62))
    chk('⑱e 설계에 없는 union 행 (코호트의 perc) 은 인계표에 안 들어가고 보고에 남는다',
        len(_oq) == 2 and 'perc' in (_rq.get('union_extra') or []))
    chk('⑱e2 union 없이 부르면 옛 인계표 그대로 (union 열 없음 · 하위 호환)',
        'porosity_union_exact_pct' not in build_handover(_dq, _hqs)[1])
    _neg('⑱f union 에 설계 케이스가 없으면 거부 (부분 병기 금지)', lambda: build_handover(_dq, _hqs, union={'q1': _uq['q1']}))
    _neg('⑱g union 의 구 부피 합 porosity ≠ 수확 (다른 프레임 · 다른 수확의 union) 이면 거부',
         lambda: build_handover(_dq, _hqs, union=dict(_uq, q2=_u('q2', eps_s=20.5, th=40.0, eps_u=21.0))))
    _neg('⑱h union 두께 ≠ 수확 두께면 거부',
         lambda: build_handover(_dq, _hqs, union=dict(_uq, q2=_u('q2', eps_s=20.0, th=40.1, eps_u=21.0))))
    _neg('⑱i union 상별 입자 수 ≠ 수확이면 거부',
         lambda: build_handover(_dq, _hqs, union=dict(_uq, q2=_u('q2', eps_s=20.0, th=40.0, eps_u=21.0, n_se=99))))
    _neg('⑱j union status ≠ OK 면 거부',
         lambda: build_handover(_dq, _hqs, union=dict(_uq, q2=_u('q2', eps_s=20.0, th=40.0, eps_u=21.0, status='DELTA_MISMATCH'))))
    _hno = _hq('q2', eps_s=20.0, th=40.0)
    _hno.pop('handover_qc')
    _neg('⑱k 수확에 두께 (handover_qc) 가 없으면 union 을 붙이지 않는다 (09-24 판 수확 — 0925 판을 쓸 것)',
         lambda: build_handover(_dq, dict(_hqs, q2=_hno), union=_uq))
    #  ⑱m–r J20-e (1저자 09-29 밤 *"φ 는 (라) 에 해당하는 것만"*) — 질량 보존 φ = φ(구) × (1 − ε_union)/(1 − ε_sphere)
    #   = 재료 부피 / (L² · 질량 보존 두께).  인계 두께 (질량 보존) · porosity (union) 와 **같은 장부**다 — 옛 φ (구 부피 합 ÷ DEM 판 간격) 는
    #   union 과 닫히지 않는다 (130 중앙 +3.77 %p · 64 중앙 +10.91 %p).  겹침 배분 (union 점유 (가)~(다)) 은 쓰지 않는다.
    def _fl(x):
        try:
            return float(x)
        except (TypeError, ValueError):
            return float('nan')
    _km = (1 - 6.5 / 100) / (1 - (-2.0) / 100)
    chk('⑱m J20-e 질량 보존 φ 두 열 = 구 부피 합 φ × (1 − ε_union)/(1 − ε_sphere) (q1: 0.5 · 0.52 × 0.935/1.02)',
        abs(_fl(_q1.get('phi_se_mass_conserving')) - 0.5 * _km) < 1e-12
        and abs(_fl(_q1.get('phi_am_mass_conserving')) - 0.52 * _km) < 1e-12)
    _clo = [abs(_fl(r.get('phi_se_mass_conserving')) + _fl(r.get('phi_am_mass_conserving'))
                + _fl(r.get('porosity_union_exact_pct')) / 100 - 1) for r in (_q1, _q2)]
    chk('⑱n 닫힘 — φ_SE + φ_AM + ε_union = 1 (1e-12 · q1 · q2)', max(_clo) < 1e-12)
    _ldg = [abs(_fl(r.get(f'phi_{p}_mass_conserving')) * _fl(r.get('thickness_mass_conserving_um'))
                - _fl(r.get(f'phi_{p}')) * _fl(r.get('thickness_wall_gap_um'))) for r in (_q1, _q2) for p in ('se', 'am')]
    chk('⑱o 적재량 보존 — φ(질량 보존) × 질량 보존 두께 = φ(구) × 판 간격 두께 (= 재료 부피 / L²) (1e-9 µm)', max(_ldg) < 1e-9)
    chk('⑱p 옛 φ (구 부피 합 ÷ 판 간격) 는 union 과 **안 닫힌다** — 잔차 = (ε_union − ε_sphere)/100 (q1 +0.085) · 그래서 새 열',
        abs(_fl(_q1.get('phi_se')) + _fl(_q1.get('phi_am')) + 0.065 - 1 - 0.085) < 1e-12)
    _hbad = dict(_hqs['q2'], status=dict(_hqs['q2']['status'], phi='N_A_TEST'))
    _b2 = next((r for r in build_handover(_dq, dict(_hqs, q2=_hbad), union=_uq)[0] if r['case_id'] == 'q2'), {})
    chk('⑱q φ status ≠ OK 면 질량 보존 φ 도 빈칸 (0 이 아니다 · 계약 ②)',
        _b2.get('phi_se_mass_conserving') == '' and _b2.get('phi_am_mass_conserving') == '')
    _cdq = {d['column']: d for d in column_dictionary(_cq)}
    chk('⑱r 열 사전 — 질량 보존 φ 두 열: 출처 union · 뜻에 J20-e · 옛 phi_se 뜻에 인계용 열 안내',
        all(_cdq.get(c, {}).get('source') == 'union' and 'J20-e' in _cdq.get(c, {}).get('meaning', '')
            for c in ('phi_se_mass_conserving', 'phi_am_mass_conserving'))
        and 'phi_se_mass_conserving' in _cdq.get('phi_se', {}).get('meaning', ''))
    #  ⑱l 실물 — 동결 설계 CSV 130 · 기본 수확 (0925) · 기본 union TSV
    _rt = pathlib.Path(__file__).resolve().parent.parent
    _dp_, _up_, _hd_ = (_rt / DESCRIPTOR_FILL_EXPECTED['path'], _rt / str(globals().get('DEFAULT_UNION_TSV', '')),
                        _rt / DEFAULT_HARVEST_DIR)
    try:
        with _dp_.open(encoding='utf-8-sig') as _fh:
            _rows_ = list(csv.DictReader(_fh))
        _ol, _cl, _rl = build_handover(_rows_, load_harvest(_hd_), union=load_union(_up_))
        _eu = [float(r['porosity_union_exact_pct']) for r in _ol]
        _ra = sorted(float(r['thickness_mass_conserving_um']) / float(r['thickness_wall_gap_um']) for r in _ol)
        _ns = sum(r['se_rich'] == 'True' for r in _ol)
        _neg_s = sum(float(r['porosity_sphere_pct_RECORD_ONLY']) < 0 for r in _ol)
        chk(f'⑱l 실물 130 (설계 CSV · 0925 수확 · union TSV) — {len(_ol)} 행 전부 병기 · union 최소 {min(_eu):.2f} % > 0 · '
            f'질량 보존 비 {_ra[0]:.3f}–{_ra[-1]:.3f} (중앙 {_ra[len(_ra) // 2]:.3f}) ≥ 1 · SE-rich {_ns} · 구 부피 합 음수 {_neg_s}',
            len(_ol) == 130 and min(_eu) > 0 and _ra[0] >= 1.0)
        _cm = max(abs(float(r['phi_se_mass_conserving']) + float(r['phi_am_mass_conserving'])
                      + float(r['porosity_union_exact_pct']) / 100 - 1) for r in _ol)
        _sr = max(abs(float(r['phi_se_mass_conserving'])
                      / (float(r['phi_se_mass_conserving']) + float(r['phi_am_mass_conserving'])) - float(r['se_of_solid_vol']))
                  for r in _ol)
        chk(f'⑱l2 실물 130 — 질량 보존 φ 닫힘 최대 {_cm:.1e} · SE/고체 ↔ union se_of_solid_vol (다른 코드 · 같은 덤프) 최대 차 {_sr:.1e} (≤ 1e-9)',
            _cm <= 1e-9 and _sr <= 1e-9)
    except Exception as e:                                                # noqa: BLE001
        chk(f'⑱l 실물 130 병기 ({type(e).__name__}: {e})', False)

    #  ═══ ⑲ J20 (1저자 비준 09-28 — "벽 기준 τ 새 열" · "✅ 만 이번에" · "채운 뒤 넘김") ═══════════════════════════════
    #   (1) 수확 v3 의 벽 τ 를 **새 열**로 — 값은 status OK 일 때만 (계약 ②) · 옛 τ 는 계속 보류 · 수확 세대가 섞이면 거부
    #   (2) 웹앱 파이프라인 열 (scripts/lhs_webapp_batch.py) 중 전수 판정 ✅ 만 — 같은 프레임 관문 (웹앱 porosity = 수확 porosity)
    _WC = 'harvest_v3/wall_z0_plate/rSEmax/no_fallback/same_component'

    def _tw(status='OK', mean=1.7, med=1.65):
        return {'tau_mean': (mean if status == 'OK' else None), 'tau_median': (med if status == 'OK' else None),
                'tau_mean_untruncated': (mean if status == 'OK' else None), 'status': status,
                'n_sampled': 200, 'n_valid': (200 if status == 'OK' else 0), 'n_truncated': 0,
                'n_span_components': (1 if status == 'OK' else 0), 'tau_convention': _WC}
    _hw = {'q1': dict(_hqs['q1'], tau_wall_detail=_tw()), 'q2': dict(_hqs['q2'], tau_wall_detail=_tw('NOT_PERCOLATING'))}
    try:
        _ow, _cw, _rw = build_handover(_dq, _hw)
        _ew = ''
    except Exception as e:                                                # noqa: BLE001
        _ow, _cw, _rw, _ew = [], [], {}, f'{type(e).__name__}: {e}'
    _w1 = next((r for r in _ow if r['case_id'] == 'q1'), {})
    _w2 = next((r for r in _ow if r['case_id'] == 'q2'), {})
    chk('⑲a 벽 τ 새 열 — OK 행은 값 · 미관통 행은 **빈칸** + status (0 이 아니다) · 규약 문자열' + (f' — {_ew}' if _ew else ''),
        _w1.get('tortuosity_SE_wall') == repr(1.7) and _w1.get('tortuosity_SE_wall_median') == repr(1.65)
        and _w2.get('tortuosity_SE_wall') == '' and _w2.get('tortuosity_SE_wall_status') == 'NOT_PERCOLATING'
        and _w1.get('tau_wall_convention') == _WC)
    chk('⑲b 옛 τ (solid_zrange) 는 여전히 보류 — tortuosity_dijkstra_SE 열이 없다 (LHS-08)',
        'tortuosity_dijkstra_SE' not in _cw and 'tortuosity_dijkstra_SE' in _rw.get('held_back', {}))
    _neg('⑲c 수확 세대가 섞이면 거부 (벽 τ 가 일부 JSON 에만 있다)',
         lambda: build_handover(_dq, {'q1': _hw['q1'], 'q2': _hqs['q2']}))
    chk('⑲d 벽 τ 가 없는 옛 수확이면 그 열 없이 옛 인계표 그대로 (하위 호환)',
        'tortuosity_SE_wall' not in build_handover(_dq, _hqs)[1])
    _neg('⑲e 벽 τ 규약 문자열이 다르면 거부 (다른 규약의 값을 같은 열에 넣지 않는다)',
         lambda: build_handover(_dq, {'q1': _hw['q1'], 'q2': dict(_hqs['q2'], tau_wall_detail=dict(_tw(), tau_convention='x'))}))

    _vd = {'se_se_cn': '✅ 쓴다', 'coverage_AM_P_mean': '✅ 쓴다(이름 주의)', 'phi_se': '✅ 쓴다', 'porosity': '✅ 쓴다',
           'sigma_full_mScm': '🔶 행 선별', 'coverage_AM_P_mean_physics': '🔧 재실행', 'case': '· 식별자'}
    _why = {k: f'why:{k}' for k in _vd}

    def _wa(q1=None, q2=None, st1='done', st2='done'):
        r1 = {'case': 'q1', 'se_se_cn': '4.25', 'coverage_AM_P_mean': '13.1', 'phi_se': '', 'porosity': repr(-2.0),
              'sigma_full_mScm': '0.08', 'coverage_AM_P_mean_physics': '31.0'}
        r2 = {'case': 'q2', 'se_se_cn': '6.5', 'coverage_AM_P_mean': '20.0', 'phi_se': '0.5', 'porosity': repr(20.0),
              'sigma_full_mScm': '0.2', 'coverage_AM_P_mean_physics': '40.0'}
        r1.update(q1 or {})
        r2.update(q2 or {})
        return {'verdict': dict(_vd), 'why': dict(_why),
                'status': {'q1': {'status': st1, 'failed_stages': []}, 'q2': {'status': st2, 'failed_stages': ['Stage E']}},
                'rows': {'q1': r1, 'q2': r2}}
    try:
        _oa, _ca, _ra = build_handover(_dq, _hqs, webapp=_wa(st2='partial'), wa_reviewed_only=False)   # 옛 기제 (census ✅ 선별) 시험
        _ea = ''
    except Exception as e:                                                # noqa: BLE001
        _oa, _ca, _ra, _ea = [], [], {}, f'{type(e).__name__}: {e}'
    _a1 = next((r for r in _oa if r['case_id'] == 'q1'), {})
    _a2 = next((r for r in _oa if r['case_id'] == 'q2'), {})
    chk('⑲f 웹앱 ✅ 열만 들어간다 (🔶 σ · 🔧 Physics · 식별자는 안 들어간다) · 이름은 코퍼스 그대로' + (f' — {_ea}' if _ea else ''),
        not _ea and 'se_se_cn' in _ca and 'coverage_AM_P_mean' in _ca and 'porosity' in _ca
        and 'sigma_full_mScm' not in _ca and 'coverage_AM_P_mean_physics' not in _ca
        and _a1.get('se_se_cn') == '4.25')
    chk('⑲g 이름 충돌 (phi_se) 은 수확 열이 정본 — 웹앱 값은 안 덮고 보고에 남긴다',
        _a2.get('phi_se') == repr(0.5) and 'phi_se' in (_ra.get('wa_collisions') or []))
    chk('⑲h 같은 프레임 QC 열 — 웹앱 porosity − 수확 porosity (여기선 0) · 행 상태 (done · partial) · 실패 단계',
        _a1.get('qc_wa_porosity_minus_harvest_pct') == repr(0.0) and _a1.get('wa_status') == 'done'
        and _a2.get('wa_status') == 'partial' and _a2.get('wa_failed_stages') == 'Stage E')
    _neg('⑲i ★ 웹앱 porosity ≠ 수확 porosity (0.05 %p 넘게) → 거부 — 다른 프레임의 웹앱 행을 붙이지 않는다',
         lambda: build_handover(_dq, _hqs, webapp=_wa(q2={'porosity': repr(20.5)})))
    _oa3, _ca3, _ra3 = build_handover(_dq, _hqs, webapp=_wa(st2='REFUSED'), wa_reviewed_only=False)
    _a3 = next((r for r in _oa3 if r['case_id'] == 'q2'), {})
    chk('⑲j 배치가 거부 · 실패한 행은 웹앱 열이 **빈칸** + wa_status (0 이 아니다) · 보고에 셈',
        _a3.get('wa_status') == 'REFUSED' and _a3.get('se_se_cn') == '' and _ra3.get('wa_status_counts', {}).get('REFUSED') == 1)
    _wm = _wa()
    _wm['status'].pop('q2')
    _neg('⑲k 배치가 **시도하지 않은** 설계행이 있으면 거부 (배치 미완)', lambda: build_handover(_dq, _hqs, webapp=_wm))
    _neg('⑲l done 행에 porosity 가 없으면 거부 (같은 프레임을 확인할 수 없다)',
         lambda: build_handover(_dq, _hqs, webapp=_wa(q1={'porosity': ''})))
    _dct = column_dictionary(_ca, webapp=_wa()) if 'column_dictionary' in globals() else []
    _dm = {d['column']: d for d in _dct}
    chk('⑲m 열 사전 — 모든 열에 출처 · 설명 · (웹앱 열은) 판정 · 이름 주의 표지',
        len(_dct) == len(_ca) and _dm.get('se_se_cn', {}).get('source') == 'webapp'
        and _dm.get('coverage_AM_P_mean', {}).get('caveat', '').startswith('A_dem_geometric')
        and _dm.get('case_id', {}).get('source') == 'design' and all(d.get('meaning') for d in _dct))
    try:
        sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
        import lhs_descriptor_harvest as _LDH
        _hc = getattr(_LDH, 'TAU_WALL_CONVENTION', None)
    except Exception as e:                                                # noqa: BLE001
        _hc = f'{type(e).__name__}: {e}'
    chk('⑲n 벽 τ 규약 문자열 — 생성기 = 수확기 (`lhs_descriptor_harvest.TAU_WALL_CONVENTION`) · 한쪽만 바뀌면 걸린다',
        _hc == TAU_WALL_CONVENTION)

    #  ═══ ⑲o–p J20-a (1저자 비준 09-28 밤 "권고하는걸로") — ⓒ 접촉 위상 열의 정의 · ⓓ 상별 벽 접촉 비율 새 열 ═══════════════
    _vd2 = dict(_vd, am_se_cn_mean='✅ 쓴다', am_se_cn_surface_weighted='✅ 쓴다', AM_P_se_cn_mean='✅ 쓴다',
                am_am_cn='✅ 쓴다', am_am_n_contacts='✅ 쓴다', area_SE_SE_n='✅ 쓴다(이름 주의)',
                area_SE_SE_total='✅ 쓴다(이름 주의)')
    _cols2 = list(_vd2)
    _dm2 = {d['column']: d for d in column_dictionary(_cols2, webapp={'verdict': _vd2, 'why': {k: f'why:{k}' for k in _vd2}})}
    _g = lambda c, k: (_dm2.get(c) or {}).get(k, '')                        # noqa: E731
    chk('⑲o ⓒ CN 정의 — 분모 (전 입자 · 접촉 0 · 벽 입자 포함) 와 벽 효과 주의 · 파생 열 (AM–SE 전체 · 표면 가중) 표시',
        '전 입자' in _g('se_se_cn', 'meaning') and '벽' in _g('se_se_cn', 'caveat')
        and '파생' in _g('am_se_cn_mean', 'caveat') and '파생' in _g('am_se_cn_surface_weighted', 'caveat')
        and 'AM_P' in _g('AM_P_se_cn_mean', 'meaning') and '벽' in _g('AM_P_se_cn_mean', 'caveat')
        and 'AM_P–AM_S' in _g('am_am_cn', 'meaning'))
    chk('⑲o ⓒ 접촉 개수 열은 **총량** 주의 — area_*_n 에 면적 (A_dem_geometric) 주의를 붙이지 않는다 · 면적 열은 그대로',
        _g('area_SE_SE_n', 'caveat').startswith('총량') and not _g('area_SE_SE_n', 'caveat').startswith('A_dem_geometric')
        and _g('am_am_n_contacts', 'caveat').startswith('총량')
        and _g('area_SE_SE_total', 'caveat').startswith('A_dem_geometric')
        and _g('coverage_AM_P_mean', 'caveat').startswith('A_dem_geometric'))
    _wt3 = {'SE': {'n': 3, 'floor': 0.25, 'plate': 0.125}, 'AM_P': {'n': 2, 'floor': 0.5, 'plate': 0.5},
            'AM_S': {'n': 4, 'floor': 0.0, 'plate': 0.25}, 'AM': {'n': 6, 'floor': 1 / 6, 'plate': 1 / 3}}
    _wt2 = {'SE': {'n': 3, 'floor': 0.5, 'plate': 0.0}, 'AM': {'n': 2, 'floor': 1.0, 'plate': 0.0}}
    _hwt = {'q1': dict(_hqs['q1'], wall_touch=_wt3), 'q2': dict(_hqs['q2'], wall_touch=_wt2)}
    try:
        _ot, _ct, _rt = build_handover(_dq, _hwt)
        _et = ''
    except Exception as e:                                                # noqa: BLE001
        _ot, _ct, _rt, _et = [], [], {}, f'{type(e).__name__}: {e}'
    _t1 = next((r for r in _ot if r['case_id'] == 'q1'), {})
    _t2 = next((r for r in _ot if r['case_id'] == 'q2'), {})
    chk('⑲p ⓓ 상별 벽 접촉 비율 새 열 — 값 · 없는 상 (2-type 의 AM_P · AM_S) 은 **빈칸** (0 이 아니다)' + (f' — {_et}' if _et else ''),
        not _et and _t1.get('wall_touch_frac_AM_P_floor') == repr(0.5) and _t1.get('wall_touch_frac_SE_plate') == repr(0.125)
        and _t2.get('wall_touch_frac_AM_P_floor') == '' and _t2.get('wall_touch_frac_AM_floor') == repr(1.0)
        and 'wall_touch_frac_AM_S_plate' in _ct)
    _neg('⑲p ⓓ 수확 세대가 섞이면 거부 (wall_touch 가 일부 JSON 에만 있다)',
         lambda: build_handover(_dq, {'q1': _hwt['q1'], 'q2': _hqs['q2']}))
    _dm3 = {d['column']: d for d in column_dictionary(_ct)}
    chk('⑲p ⓓ 벽 비율이 없는 옛 수확이면 그 열 없이 (하위 호환) · 열 사전에 출처 harvest_v3 · 규칙 설명',
        'wall_touch_frac_SE_floor' not in build_handover(_dq, _hqs)[1]
        and _dm3.get('wall_touch_frac_SE_floor', {}).get('source') == 'harvest_v3'
        and 'z − r' in _dm3.get('wall_touch_frac_SE_floor', {}).get('meaning', ''))

    #  ⑲q–u 묶음별 (1저자 09-29 밤 *"단독적으로 하나씩 돌려서 표를 채워나갈 거야"*) — webapp_groups='contact' 는 **접촉 분석 단계가
    #   내는** ① 열만 싣는다.  접촉 단계만 돈 배치 (status.json stop_after=contact) 를 묶음 제한 없이 부르면 거부한다 — 뒤 단계 열이
    #   빈칸으로 들어가 '측정된 N/A' 처럼 읽힌다.  ① 사전 (WA_DEFINE) 중 A_binding_*_n_contacts (피복 단계) ·
    #   n_am_am_contacts_* (파괴 네트워크) 는 접촉 단계 산출이 아니다 → 이 묶음에서 뺀다.
    _vd2 = dict(_vd, am_am_cn='✅ 쓴다', AM_P_se_cn_mean='✅ 쓴다', area_SE_SE_n='✅ 쓴다', percolation_pct='✅ 쓴다',
                A_binding_total_n_contacts='✅ 쓴다', n_am_am_contacts_total='✅ 쓴다')

    def _wa2(stop=None):
        w = _wa()
        w['verdict'] = dict(_vd2)
        w['why'] = {k: f'why:{k}' for k in _vd2}
        for r in w['rows'].values():
            r.update(am_am_cn='1.2', AM_P_se_cn_mean='7.0', area_SE_SE_n='900', percolation_pct='',
                     A_binding_total_n_contacts='', n_am_am_contacts_total='',
                     se_se_cn='18.0')                             # J20-i 항등식 — 2 × 900 / SE 100
        if stop:
            w['stop_after'] = stop
        return w
    try:
        _og, _cg, _rg = build_handover(_dq, _hqs, webapp=_wa2('contact'), webapp_groups='contact', wa_reviewed_only=False)
        _eg = ''
    except Exception as e:                                                # noqa: BLE001
        _og, _cg, _rg, _eg = [], [], {}, f'{type(e).__name__}: {e}'
    chk('⑲q ★ webapp_groups=contact — 웹앱 열은 접촉 단계 ① 만 (se_se_cn · am_am_cn · AM_P_se_cn_mean · area_SE_SE_n) · '
        'porosity · coverage · percolation · A_binding · n_am_am_contacts 는 없다' + (f' — {_eg}' if _eg else ''),
        not _eg and all(c in _cg for c in ('se_se_cn', 'am_am_cn', 'AM_P_se_cn_mean', 'area_SE_SE_n'))
        and not any(c in _cg for c in ('porosity', 'coverage_AM_P_mean', 'percolation_pct',
                                       'A_binding_total_n_contacts', 'n_am_am_contacts_total')))
    _neg('⑲r ★ 접촉 단계만 돈 배치 (stop_after=contact) 를 묶음 제한 없이 부르면 거부 — 뒤 단계 열이 빈칸 = N/A 로 읽힌다',
         lambda: build_handover(_dq, _hqs, webapp=_wa2('contact')))
    _neg('⑲s 모르는 묶음 이름은 거부 (⑤⑥⑦ 뒤 f1 · fracture · area 는 아는 묶음 — stress 로 · ④b 새 열은 아직 인계 묶음이 아니다)',
         lambda: build_handover(_dq, _hqs, webapp=_wa2(), webapp_groups='stress'))
    _g1 = next((r for r in _og if r['case_id'] == 'q1'), {})
    chk('⑲t 같은 프레임 관문은 그대로 — 웹앱 porosity (접촉 단계 산출) − 수확 porosity 가 QC 열에 (여기선 0)',
        _g1.get('qc_wa_porosity_minus_harvest_pct') == repr(0.0) and _g1.get('am_am_cn') == '1.2')
    import shutil
    import tempfile
    _tdw = pathlib.Path(tempfile.mkdtemp(prefix='lhsdd_wa_'))
    try:
        (_tdw / 'status.json').write_text(json.dumps({'schema': 'lhs_webapp_batch/v1', 'stop_after': 'contact', 'cases': {}}),
                                          encoding='utf-8')
        (_tdw / 'metrics_flat.csv').write_text('case\n', encoding='utf-8')
        _lw = load_webapp(_tdw)
        chk('⑲u load_webapp 이 배치의 stop_after 를 넘긴다 (묶음 관문의 근거)', _lw.get('stop_after') == 'contact')
    except Exception as e:                                                # noqa: BLE001
        chk(f'⑲u load_webapp stop_after ({type(e).__name__}: {e})', False)
    finally:
        shutil.rmtree(_tdw, ignore_errors=True)

    #  ⑳ J20-g (1저자 비준 09-30 "권고대로") — 표에는 **1저자와 함수 단위로 같이 확인한 열만** 싣는다 (census ✅ 는 필요조건일 뿐)
    #   · J20-k (B) (1저자 09-30 · J20-f (A) 개정): mono (2-type) 침대의 **상별** 웹앱 열은 **설계 상 칸** (block) 에 싣는다 — 웹앱은 mono 의
    #   AM 을 반지름으로 AM_P/AM_S 라 부르고 설계 상과 어긋나는 침대가 있다 (130 의 5 · 64 의 4) → 그 이름의 값을 설계 이름 칸으로 옮기고
    #   (wa_mono_phase_name_webapp 에 웹앱 이름을 남긴다) 설계에 없는 상의 칸은 빈칸 (N/A).  총량 열 (area_AM전체_SE_n · area_SE_SE_n) 은 그대로.
    _vd3 = dict(_vd, am_am_cn='✅ 쓴다', AM_P_se_cn_mean='✅ 쓴다', AM_S_se_cn_mean='✅ 쓴다', area_SE_SE_n='✅ 쓴다',
                area_AM_S_SE_n='✅ 쓴다', area_AM_P_SE_n='✅ 쓴다', **{'area_AM전체_SE_n': '✅ 쓴다'},
                se_se_cn_std='✅ 쓴다', se_se_cn_perc='✅ 쓴다', se_se_cn_eff_area='✅ 쓴다(이름 주의)', se_se_cn_aug='✅ 쓴다',
                am_am_cn_std='✅ 쓴다', am_am_n_contacts='✅ 쓴다', am_am_mean_area='✅ 쓴다(이름 주의)',
                am_am_total_area='✅ 쓴다(이름 주의)')

    def _wa3():
        w = _wa()
        w['verdict'] = dict(_vd3)
        w['why'] = {k: f'why:{k}' for k in _vd3}
        w['stop_after'] = 'contact'
        #  se_se_cn = 2 × area_SE_SE_n / SE 입자 수 (수확 phase_counts SE 100) — J20-i 항등식에 맞춘 값 · 같은 함수의 나머지 출력도 싣는다
        #  J20-j — am_am_n_contacts = AM–AM 쌍 개수 합 · am_am_cn = 2 × am_am_n_contacts / AM 입자 수 (11) 에 맞춘 값
        #  7c G1 — 상별 AM–SE 평균 × 상 입자 수 = area_<상>_SE_n (q1 mono 40 / 11 · q2 30 / 1 · 50 / 10) — 옛 값 3.0 · 7.0 · 3.5 는 모순이었다
        w['rows']['q1'].update(am_am_cn='2.0', AM_S_se_cn_mean=repr(40 / 11), area_SE_SE_n='900', area_AM_S_SE_n='40',
                               se_se_cn='18.0', se_se_cn_std='2.5', se_se_cn_perc='18.5', se_se_cn_eff_area='0.07',
                               se_se_cn_aug='19.0', area_AM_S_AM_S_n='11', am_am_n_contacts='11', am_am_cn_std='1.0',
                               am_am_mean_area='0.02', am_am_total_area='0.22',
                               **{'area_AM전체_SE_n': '40'})   # q1 = mono (웹앱 반지름 이름 AM_S)
        w['rows']['q2'].update(am_am_cn='4.0', AM_P_se_cn_mean='30.0', AM_S_se_cn_mean='5.0', area_SE_SE_n='800',
                               area_AM_P_SE_n='30', area_AM_S_SE_n='50', se_se_cn='16.0', se_se_cn_std='3.0',
                               se_se_cn_perc='16.5', se_se_cn_eff_area='0.06', se_se_cn_aug='17.0',
                               area_AM_P_AM_S_n='5', area_AM_S_AM_S_n='17', am_am_n_contacts='22', am_am_cn_std='1.5',
                               am_am_mean_area='0.03', am_am_total_area='0.66',
                               **{'area_AM전체_SE_n': '80'})
        return w
    def _mono_h(h, n_am=11, n_se=100):
        """bimodal 수확 픽스처 → 수확기의 2-type 모양 (상 라벨 AM 하나 · coverage 상별 N_A · AM_only = 전체)."""
        return dict(h, n_types=2, phase_counts={'AM': n_am, 'SE': n_se},
                    coverage_AM_P_hertz_pct=None, coverage_AM_S_hertz_pct=None,
                    coverage_AM_only_hertz_pct=h['coverage_AM_total_hertz_pct'],
                    status=dict(h['status'], coverage_AM_P='N_A_PHASE_ABSENT', coverage_AM_S='N_A_PHASE_ABSENT'),
                    coverage_detail=dict(h['coverage_detail'],
                                         counts={'AM_P': {'n_valid': 0}, 'AM_S': {'n_valid': 0}, 'AM': {'n_valid': n_am}}))
    _hq3 = {'q1': _mono_h(_hqs['q1']), 'q2': dict(_hqs['q2'], n_types=3)}
    #  ⑳ 부터 설계행에 block — J20-k (B) 는 설계 상을 block 으로 정한다 (q1 = 설계 mono_AM_P · 웹앱 반지름 이름 AM_S = 이름이 어긋나는 침대)
    _dq = [{'case_id': 'q1', 'block': 'mono_AM_P'}, {'case_id': 'q2', 'block': 'bimodal'}]
    try:
        _o20, _c20, _r20 = build_handover(_dq, _hq3, webapp=_wa3(), webapp_groups='contact')
        _e20 = ''
    except Exception as e:                                                # noqa: BLE001
        _o20, _c20, _r20, _e20 = [], [], {}, f'{type(e).__name__}: {e}'
    _m20 = next((r for r in _o20 if r['case_id'] == 'q1'), {})
    _b20 = next((r for r in _o20 if r['case_id'] == 'q2'), {})
    chk('⑳a ★ J20-g — 같이 확인한 열만: 접촉 묶음 중 area_<쌍>_n (· J20-i se_se_cn · J20-j am_am_* · 7c AM_*_se_cn_* — 7c 부터 실린다 · '
        'mono 는 설계 상 칸)' + (f' — {_e20}' if _e20 else ''),
        not _e20 and all(c in _c20 for c in ('area_SE_SE_n', 'area_AM_S_SE_n', 'area_AM_P_SE_n', 'area_AM전체_SE_n',
                                             'AM_P_se_cn_mean', 'AM_S_se_cn_mean'))
        and _m20.get('AM_P_se_cn_mean') == repr(40 / 11) and _m20.get('AM_S_se_cn_mean') == ''
        and _b20.get('AM_P_se_cn_mean') == '30.0' and _b20.get('AM_S_se_cn_mean') == '5.0')
    chk('⑳b ★ J20-k (B) — mono (설계 mono_AM_P · 웹앱 이름 AM_S) 의 상별 쌍 값은 **설계 상 칸** (area_AM_P_SE_n) 으로 · 없는 상 칸 (area_AM_S_SE_n) '
        '빈칸 · 총량 쌍 그대로 · 웹앱 이름을 wa_mono_phase_name_webapp 에 · 보고 (옮김 1 건 · 채움 2 · 빈칸 2 — 쌍 개수 + 7c AM–SE 평균)',
        _m20.get('area_AM_P_SE_n') == '40' and _m20.get('area_AM_S_SE_n') == ''
        and _m20.get('area_AM전체_SE_n') == '40' and _m20.get('area_SE_SE_n') == '900'
        and _m20.get('wa_mono_phase_name_webapp') == 'AM_S' and _b20.get('wa_mono_phase_name_webapp') == ''
        and _m20.get('block') == 'mono_AM_P'
        and _r20.get('wa_mono_renamed_cases') == 1 and _r20.get('wa_mono_design_filled') == 2
        and _r20.get('wa_mono_absent_blanked') == 2 and 'wa_mono_phase_blanked' not in _r20)
    chk('⑳c bimodal (n_types 3) 은 상별 쌍 값 그대로',
        _b20.get('area_AM_P_SE_n') == '30' and _b20.get('area_AM_S_SE_n') == '50' and _b20.get('area_AM전체_SE_n') == '80')
    chk('⑳d 판별 — wa_reviewed (area_<쌍>_n · se_se_cn(_std) · am_am_cn(_std) · am_am_n_contacts · 7c AM–SE CN · 고립 — _perc 는 ② 뒤 · '
        '_eff_area · _aug · am_am 면적은 ⑤⑦ 뒤 (J20-s) 검토됨 · AM_*_n_particles · path_hop_area 는 아님) · '
        'wa_phase_specific (AM_P/AM_S 이름이 든 열 · AM전체 · 소문자 am_ 은 아님)',
        'wa_reviewed' in globals() and 'wa_phase_specific' in globals()
        and globals()['wa_reviewed']('area_AM_P_SE_n') and globals()['wa_reviewed']('se_se_cn')
        and globals()['wa_reviewed']('se_se_cn_std') and globals()['wa_reviewed']('se_se_cn_perc')     # ② 뒤 (J20-b) 검토됨
        and globals()['wa_reviewed']('se_se_cn_eff_area') and globals()['wa_reviewed']('se_se_cn_aug')      # ⑤⑦ 뒤 (J20-s) 검토됨
        and not globals()['wa_reviewed']('path_hop_area_mean')
        and globals()['wa_reviewed']('am_am_cn') and globals()['wa_reviewed']('am_am_cn_std')
        and globals()['wa_reviewed']('am_am_n_contacts') and globals()['wa_reviewed']('am_am_mean_area')
        and globals()['wa_reviewed']('am_am_total_area') and globals()['wa_reviewed']('AM_P_se_cn_mean')
        and globals()['wa_reviewed']('am_se_cn_median') and globals()['wa_reviewed']('AM_S_vulnerable_pct')
        and not globals()['wa_reviewed']('AM_P_n_particles') and not globals()['wa_reviewed']('am_se_cn_mean_x')
        and globals()['wa_phase_specific']('area_AM_S_AM_S_n') and globals()['wa_phase_specific']('AM_P_se_cn_mean')
        and not globals()['wa_phase_specific']('area_AM전체_SE_n') and not globals()['wa_phase_specific']('am_am_cn'))
    _neg('⑳e ★ 상별 열을 싣는데 수확 JSON 에 n_types 가 없으면 거부 (mono 인지 모른다 — 반지름 이름을 그대로 싣지 않는다)',
         lambda: build_handover(_dq, {k: {kk: vv for kk, vv in v.items() if kk != 'n_types'} for k, v in _hqs.items()},
                                webapp=_wa3(), webapp_groups='contact'))
    _d20 = {d['column']: d for d in column_dictionary(_c20, webapp=_wa3())} if _c20 else {}
    chk('⑳f 열 사전 — 상별 쌍 열의 뜻에 mono 설계 상 칸 규약 (J20-k (B)) · 검토 기록 (J20-g) · 총량 열에는 mono 규약 없음',
        'mono' in _d20.get('area_AM_S_SE_n', {}).get('meaning', '') and 'J20-k' in _d20.get('area_AM_S_SE_n', {}).get('meaning', '')
        and '설계 상 칸' in _d20.get('area_AM_P_SE_n', {}).get('meaning', '')
        and 'J20-g' in _d20.get('area_SE_SE_n', {}).get('meaning', '')
        and '설계 상 칸' not in _d20.get('area_SE_SE_n', {}).get('meaning', '')
        and '설계 상 칸' not in _d20.get('am_am_cn', {}).get('meaning', ''))

    #  ⑳g–l J20-h (1저자 비준 09-30 — *"bimodal 에서 빠진 쌍을 0 으로 채우게 · 시험 먼저"*) — 웹앱 `calc_interface_area` 는 접촉이 0 인
    #   쌍의 키를 **만들지 않는다** → metrics_flat 에서 빈칸.  bimodal 에서 그 뜻은 **측정된 0** 이지 N/A 가 아니다 (09-30 실측: 130 에서
    #   `area_AM_P_AM_P_n` 3 건 · 64 에서 6 건 — AM_P 3–16 알 침대).  규칙: 웹앱 행이 있고 (done · partial) · 쌍 개수 열이고 · 쌍의 두 상이
    #   수확 `phase_counts` 에 **있으면** 0 · mono 상별 칸은 J20-f (A) 대로 빈칸 · 상이 없으면 빈칸 (N/A) · `phase_counts` 가 없으면 거부.
    def _wa4(st2='done'):
        w = _wa3()
        w['verdict'].update(area_AM_P_AM_P_n='✅ 쓴다', area_AM_S_AM_S_n='✅ 쓴다')
        w['why'] = {k: f'why:{k}' for k in w['verdict']}
        w['rows']['q1'].update(area_AM_S_AM_S_n='11')            # mono — 반지름 이름 AM_S · AM_P_AM_P 키 없음 (J20-j 값과 같게)
        w['rows']['q2'].update(area_AM_S_AM_S_n='17')            # bimodal — AM_P_AM_P 키 없음 (접촉 0) · J20-j 합 5 + 17 = 22
        w['status']['q2']['status'] = st2
        return w
    try:
        _o21, _c21, _r21 = build_handover(_dq, _hq3, webapp=_wa4(), webapp_groups='contact')
        _e21 = ''
    except Exception as e:                                                # noqa: BLE001
        _o21, _c21, _r21, _e21 = [], [], {}, f'{type(e).__name__}: {e}'
    _m21 = next((r for r in _o21 if r['case_id'] == 'q1'), {})
    _b21 = next((r for r in _o21 if r['case_id'] == 'q2'), {})
    chk('⑳g ★ J20-h — bimodal 의 빠진 쌍 개수 = 0 (측정된 0) · 있는 값은 그대로 · 보고에 셈' + (f' — {_e21}' if _e21 else ''),
        _b21.get('area_AM_P_AM_P_n') == '0' and _b21.get('area_AM_S_AM_S_n') == '17'
        and _r21.get('wa_pair_zero_filled') == 1)
    chk('⑳h ★ J20-k (B) mono — 웹앱 AM_S_AM_S 개수 (11) 가 설계 상 칸 area_AM_P_AM_P_n 으로 · 없는 상 칸 area_AM_S_AM_S_n 빈칸 · 총량 그대로',
        _m21.get('area_AM_P_AM_P_n') == '11' and _m21.get('area_AM_S_AM_S_n') == '' and _m21.get('area_AM전체_SE_n') == '40')
    _hq4 = dict(_hq3, q2=dict(_hq3['q2'], phase_counts={'AM_P': 0, 'AM_S': 10, 'SE': 100}))
    _wa4i = _wa4()
    _wa4i['rows']['q2'].pop('area_AM_P_AM_S_n', None)                # AM_P 가 없는 침대 — AM_P 가 낀 쌍도 없다 (J20-j 항등식과 앞뒤를 맞춤)
    _wa4i['rows']['q2'].pop('AM_P_se_cn_mean', None)                 # · AM_P 의 AM–SE 값도 없다 (7c 상 없음 관문과 앞뒤를 맞춤)
    _wa4i['rows']['q2'].update(am_am_n_contacts='17', am_am_cn='3.4')  # 2 × 17 / AM 10
    try:
        _b22 = next((r for r in build_handover(_dq, _hq4, webapp=_wa4i, webapp_groups='contact')[0] if r['case_id'] == 'q2'), {})
    except Exception as e:                                                # noqa: BLE001
        _b22 = {'_err': f'{type(e).__name__}: {e}'}
    chk('⑳i 쌍의 상이 없으면 (phase_counts 0) 0 이 아니라 빈칸 (N/A)', _b22.get('area_AM_P_AM_P_n') == '')
    _hq5 = dict(_hq3, q2={k: v for k, v in _hq3['q2'].items() if k != 'phase_counts'})
    _neg('⑳j ★ 빠진 쌍을 채워야 하는데 수확 JSON 에 phase_counts 가 없으면 거부 (상이 있는지 모른다)',
         lambda: build_handover(_dq, _hq5, webapp=_wa4(), webapp_groups='contact'))
    try:
        _o23, _c23, _r23 = build_handover(_dq, _hq3, webapp=_wa4(st2='REFUSED'), webapp_groups='contact')
        _b23 = next((r for r in _o23 if r['case_id'] == 'q2'), {})
    except Exception as e:                                                # noqa: BLE001
        _b23, _r23 = {'_err': f'{type(e).__name__}: {e}'}, {}
    chk('⑳k 배치가 거부한 행 (REFUSED) 은 0 을 채우지 않는다 — 웹앱 열 전부 빈칸',
        _b23.get('area_AM_P_AM_P_n') == '' and _b23.get('wa_status') == 'REFUSED' and _r23.get('wa_pair_zero_filled') == 0)
    _d21 = {d['column']: d for d in column_dictionary(_c21, webapp=_wa4())} if _c21 else {}
    chk('⑳l 열 사전 — 쌍 개수 열의 뜻에 0 채움 규약 (J20-h)',
        'J20-h' in _d21.get('area_AM_P_AM_P_n', {}).get('meaning', '')
        and 'J20-h' in _d21.get('area_SE_SE_n', {}).get('meaning', ''))

    #  ⑳m–r J20-i (1저자 비준 09-30 — 접촉 ① 둘째 함수 `calc_se_se_cn` · 시험 먼저) — se_se_cn · se_se_cn_std 두 열만 싣는다 (같은 함수의
    #   _perc · _eff_area · _aug 는 ② · ⑦ · ⑤ 차례).  관문: 평균 CN = 2 × area_SE_SE_n / SE 입자 수 (수확 phase_counts) — 표에 함께 실린
    #   두 열이 같은 접촉 집합에서 왔는지 (09-30 실측 130/130 · 64/64 차이 0).  어긋나면 · SE 입자 수를 모르면 거부.
    chk('⑳m ★ J20-i — se_se_cn · se_se_cn_std 가 실린다 (mono 포함 — SE–SE 는 상별 열이 아니다) · 항등식 검사 수를 보고' + (f' — {_e20}' if _e20 else ''),
        'se_se_cn' in _c20 and 'se_se_cn_std' in _c20 and _m20.get('se_se_cn') == '18.0' and _m20.get('se_se_cn_std') == '2.5'
        and _b20.get('se_se_cn') == '16.0' and _b20.get('se_se_cn_std') == '3.0' and _r20.get('wa_cn_identity_checked') == 2)
    _wa_bad = _wa3()
    _wa_bad['rows']['q2']['se_se_cn'] = '16.5'
    _neg('⑳n ★ se_se_cn ≠ 2 × area_SE_SE_n / SE 수 이면 거부 (다른 접촉 집합 · 다른 프레임의 값을 한 표에 섞지 않는다)',
         lambda: build_handover(_dq, _hq3, webapp=_wa_bad, webapp_groups='contact'))
    _neg('⑳o ★ se_se_cn 을 싣는데 수확 JSON 에 phase_counts 가 없으면 거부 (SE 입자 수를 몰라 항등식을 못 본다)',
         lambda: build_handover(_dq, {k: {kk: vv for kk, vv in v.items() if kk != 'phase_counts'} for k, v in _hq3.items()},
                                webapp=_wa3(), webapp_groups='contact'))
    _wa_rf = _wa3()
    _wa_rf['status']['q2']['status'] = 'REFUSED'
    _wa_rf['rows']['q2']['se_se_cn'] = '99.0'
    try:
        _r24 = build_handover(_dq, _hq3, webapp=_wa_rf, webapp_groups='contact')[2]
        _e24 = ''
    except Exception as e:                                                # noqa: BLE001
        _r24, _e24 = {}, f'{type(e).__name__}: {e}'
    chk('⑳p 배치가 거부한 행 (REFUSED) 은 웹앱 값을 싣지 않으므로 항등식도 보지 않는다 (검사 1 건 = q1)' + (f' — {_e24}' if _e24 else ''),
        not _e24 and _r24.get('wa_cn_identity_checked') == 1)
    chk('⑳q 같은 함수의 다른 출력 (se_se_cn_perc · se_se_cn_eff_area · se_se_cn_aug) 은 census ✅ 여도 싣지 않는다 (② · ⑦ · ⑤ 차례)',
        not any(c in _c20 for c in ('se_se_cn_perc', 'se_se_cn_eff_area', 'se_se_cn_aug')))
    chk('⑳r 열 사전 — se_se_cn · se_se_cn_std 의 뜻에 검토 기록 (J20-i) · 정의 (SE 전 입자) · 벽 주의는 그대로',
        'J20-i' in _d20.get('se_se_cn', {}).get('meaning', '') and 'J20-i' in _d20.get('se_se_cn_std', {}).get('meaning', '')
        and '전 입자' in _d20.get('se_se_cn', {}).get('meaning', '') and '벽' in _d20.get('se_se_cn', {}).get('caveat', ''))

    #  ⑳s–x J20-j (1저자 09-30 *"6번 진행하자"* — 접촉 ① 셋째 함수 `calc_am_am_cn` · 시험 먼저) — am_am_cn · am_am_cn_std · am_am_n_contacts 세 열
    #   (상별 열이 아니라 mono 도 값 — J20-f (A) 로 비운 mono 의 AM–AM 개수가 여기서 돌아온다).  am_am_mean_area · am_am_total_area 는 ⑦ 차례.
    #   관문 둘: am_am_n_contacts = 웹앱 원 행의 AM–AM 쌍 개수 합 (없는 쌍 = 0) · am_am_cn = 2 × am_am_n_contacts / AM 입자 수 (수확 phase_counts)
    #   — 09-30 실측 130/130 · 64/64 차이 0.  어긋나거나 AM 입자 수를 모르면 거부.
    chk('⑳s ★ J20-j — am_am_cn · am_am_cn_std · am_am_n_contacts 가 실린다 (mono 포함) · 항등식 검사 수를 보고' + (f' — {_e20}' if _e20 else ''),
        all(c in _c20 for c in ('am_am_cn', 'am_am_cn_std', 'am_am_n_contacts'))
        and _m20.get('am_am_cn') == '2.0' and _m20.get('am_am_n_contacts') == '11' and _m20.get('am_am_cn_std') == '1.0'
        and _b20.get('am_am_cn') == '4.0' and _b20.get('am_am_n_contacts') == '22'
        and _r20.get('wa_am_identity_checked') == 2)
    _wa_bn = _wa3()
    _wa_bn['rows']['q2']['am_am_n_contacts'] = '23'
    _neg('⑳t ★ am_am_n_contacts ≠ 웹앱 원 행의 AM–AM 쌍 개수 합 (5 + 17 = 22) 이면 거부 (다른 접촉 집합)',
         lambda: build_handover(_dq, _hq3, webapp=_wa_bn, webapp_groups='contact'))
    _wa_bc = _wa3()
    _wa_bc['rows']['q2']['am_am_cn'] = '4.5'
    _neg('⑳u ★ am_am_cn ≠ 2 × am_am_n_contacts / AM 입자 수 (2 × 22 / 11 = 4.0) 이면 거부',
         lambda: build_handover(_dq, _hq3, webapp=_wa_bc, webapp_groups='contact'))
    _wa_np = _wa3()
    for _k in ('se_se_cn', 'se_se_cn_std'):                             # J20-i 관문을 빼고 J20-j 관문만 보이게
        _wa_np['verdict'].pop(_k, None)
    _neg('⑳v ★ am_am_cn 을 싣는데 수확 JSON 에 phase_counts 가 없으면 거부 (AM 입자 수를 몰라 항등식을 못 본다 · J20-i 관문 없이도)',
         lambda: build_handover(_dq, {k: {kk: vv for kk, vv in v.items() if kk != 'phase_counts'} for k, v in _hq3.items()},
                                webapp=_wa_np, webapp_groups='contact'))
    _wa_rf2 = _wa3()
    _wa_rf2['status']['q2']['status'] = 'REFUSED'
    _wa_rf2['rows']['q2']['am_am_n_contacts'] = '999'
    try:
        _r25 = build_handover(_dq, _hq3, webapp=_wa_rf2, webapp_groups='contact')[2]
        _e25 = ''
    except Exception as e:                                                # noqa: BLE001
        _r25, _e25 = {}, f'{type(e).__name__}: {e}'
    chk('⑳w 배치가 거부한 행 (REFUSED) 은 AM–AM 항등식도 보지 않는다 (검사 1 건 = q1)' + (f' — {_e25}' if _e25 else ''),
        not _e25 and _r25.get('wa_am_identity_checked') == 1)
    chk('⑳x 같은 함수의 면적 열 (am_am_mean_area · am_am_total_area) 은 census ✅ 여도 싣지 않는다 (⑦ 차례) · 열 사전에 J20-j 검토 기록 · '
        '접촉 수는 총량 주의 · CN 은 벽 주의',
        not any(c in _c20 for c in ('am_am_mean_area', 'am_am_total_area'))
        and all('J20-j' in _d20.get(c, {}).get('meaning', '') for c in ('am_am_cn', 'am_am_cn_std', 'am_am_n_contacts'))
        and '총량' in _d20.get('am_am_n_contacts', {}).get('caveat', '') and '벽' in _d20.get('am_am_cn', {}).get('caveat', ''))

    #  ⑳y–af J20-k (B) (1저자 09-30 *"인계할때는 중복되더라도 잘 채워서 보내야될듯"* · J20-f (A) 개정 · 시험 먼저) — mono 의 상별 칸은 설계 상 칸에.
    #   위 ⑳b · ⑳h 가 "이름이 어긋나는" 침대 (설계 AM_P · 웹앱 AM_S) 를 본다.  여기서는 이름이 같은 침대 · 반례 (웹앱 행에 두 이름 다 값) ·
    #   QC (웹앱 coverage_<웹앱 이름>_mean − 수확 전체) · 설계 쌍의 접촉 0 (J20-h 는 설계 상으로 판단) · 벽 접촉 비율 상별 · 열 사전 표지.
    _dq_s = [{'case_id': 'q1', 'block': 'mono_AM_S'}, {'case_id': 'q2', 'block': 'bimodal'}]
    try:
        _o26, _c26, _r26 = build_handover(_dq_s, _hq3, webapp=_wa3(), webapp_groups='contact')
        _m26, _e26 = next((r for r in _o26 if r['case_id'] == 'q1'), {}), ''
    except Exception as e:                                                # noqa: BLE001
        _m26, _r26, _e26 = {}, {}, f'{type(e).__name__}: {e}'
    chk('⑳y 이름이 같은 mono (설계 mono_AM_S · 웹앱 AM_S) — AM_S 칸에 값 · AM_P 칸 빈칸 · 옮김 0 건' + (f' — {_e26}' if _e26 else ''),
        not _e26 and _m26.get('area_AM_S_SE_n') == '40' and _m26.get('area_AM_P_SE_n') == ''
        and _m26.get('wa_mono_phase_name_webapp') == 'AM_S' and _r26.get('wa_mono_renamed_cases') == 0
        and _r26.get('wa_mono_design_filled') == 2 and _r26.get('wa_mono_absent_blanked') == 2
        and _m26.get('coverage_AM_S_hertz_pct') == repr(17.5) and _m26.get('coverage_AM_P_hertz_pct') == ''
        and _m26.get('n_AM_S_measured') == '11' and _m26.get('n_AM_P_measured') == '')
    _wa_both = _wa3()
    _wa_both['rows']['q1']['area_AM_P_SE_n'] = '3'                        # mono 인데 웹앱 접촉 열에 AM_P · AM_S 둘 다 값 — mono 행이 아니다
    _neg('⑳z ★ mono 인데 웹앱 행의 접촉 열에 AM_P · AM_S 두 이름 다 값이 있으면 거부 (다른 침대의 행 · 옮길 이름을 못 정한다)',
         lambda: build_handover(_dq, _hq3, webapp=_wa_both, webapp_groups='contact'))
    _wa_cov = _wa3()
    _wa_cov['rows']['q1']['coverage_AM_S_mean'] = '17.5'                  # 웹앱 반지름 이름 AM_S 의 피복 = 수확 전체 17.5 (같은 채널)
    _wa_cov['rows']['q2'].update(coverage_AM_P_mean='10.5', coverage_AM_S_mean='20.0')
    try:
        _o27 = build_handover(_dq, _hq3, webapp=_wa_cov, webapp_groups='contact')[0]
        _m27 = next((r for r in _o27 if r['case_id'] == 'q1'), {})
        _b27 = next((r for r in _o27 if r['case_id'] == 'q2'), {})
        _e27 = ''
    except Exception as e:                                                # noqa: BLE001
        _m27, _b27, _e27 = {}, {}, f'{type(e).__name__}: {e}'
    _ok27 = (not _e27 and _m27.get('qc_wa_cov_AM_P_minus_harvest_pct') == repr(0.0) and _m27.get('qc_wa_cov_AM_S_minus_harvest_pct') == ''
             and _b27.get('qc_wa_cov_AM_P_minus_harvest_pct') == repr(0.5) and _b27.get('qc_wa_cov_AM_S_minus_harvest_pct') == repr(0.0))
    chk('⑳aa QC — mono 의 설계 상 칸 검산 = 웹앱 coverage_<웹앱 이름>_mean − 수확 전체 (0.0) · 없는 상 칸 빈칸 · bimodal 은 상별 그대로'
        + (f' — {_e27}' if _e27 else '')
        + ('' if _ok27 else f' (실제 q1 {_m27.get("qc_wa_cov_AM_P_minus_harvest_pct")!r} · {_m27.get("qc_wa_cov_AM_S_minus_harvest_pct")!r} '
                            f'· q2 {_b27.get("qc_wa_cov_AM_P_minus_harvest_pct")!r} · {_b27.get("qc_wa_cov_AM_S_minus_harvest_pct")!r})'),
        _ok27)
    _wa_z = _wa4()
    _wa_z['rows']['q1'].pop('area_AM_S_AM_S_n')                          # mono 인데 AM–AM 접촉 0 → 웹앱 키 없음
    _wa_z['rows']['q1'].update(am_am_n_contacts='0', am_am_cn='0.0')     # J20-j 항등식에 맞춤
    try:
        _o28, _c28, _r28 = build_handover(_dq, _hq3, webapp=_wa_z, webapp_groups='contact')
        _m28, _e28 = next((r for r in _o28 if r['case_id'] == 'q1'), {}), ''
    except Exception as e:                                                # noqa: BLE001
        _m28, _r28, _e28 = {}, {}, f'{type(e).__name__}: {e}'
    chk('⑳ab J20-h 를 설계 상으로 — mono 의 설계 쌍 area_AM_P_AM_P_n 이 빠지면 0 (AM 이 있으므로) · 없는 상 쌍은 빈칸 · 0 채움 2 (q1 + q2)'
        + (f' — {_e28}' if _e28 else ''),
        not _e28 and _m28.get('area_AM_P_AM_P_n') == '0' and _m28.get('area_AM_S_AM_S_n') == ''
        and _r28.get('wa_pair_zero_filled') == 2)
    _hwt2 = {'q1': dict(_hq3['q1'], wall_touch=_wt2), 'q2': dict(_hq3['q2'], wall_touch=_wt3)}
    try:
        _o29 = build_handover(_dq, _hwt2)[0]
        _m29, _b29 = (next((r for r in _o29 if r['case_id'] == c), {}) for c in ('q1', 'q2'))
        _e29 = ''
    except Exception as e:                                                # noqa: BLE001
        _m29, _b29, _e29 = {}, {}, f'{type(e).__name__}: {e}'
    chk('⑳ac 벽 접촉 비율 상별 — mono 의 설계 상 칸 (AM_P) = 수확 AM · 없는 상 (AM_S) 빈칸 · AM 열 그대로 · bimodal 그대로' + (f' — {_e29}' if _e29 else ''),
        not _e29 and _m29.get('wall_touch_frac_AM_P_floor') == repr(1.0) and _m29.get('wall_touch_frac_AM_S_floor') == ''
        and _m29.get('wall_touch_frac_AM_floor') == repr(1.0) and _m29.get('wall_touch_frac_SE_floor') == repr(0.5)
        and _b29.get('wall_touch_frac_AM_P_floor') == repr(0.5) and _b29.get('wall_touch_frac_AM_S_plate') == repr(0.25))
    _d27 = {d['column']: d for d in column_dictionary(_c20, webapp=_wa3())} if _c20 else {}
    chk('⑳ad 열 사전 — 상별 열마다 (수확 coverage · n_AM_*_measured · cov_*_n_valid · 웹앱 쌍 · QC) J20-k (B) 표지 · 총량 · 설계 열에는 없음 · '
        'wa_mono_phase_name_webapp 열이 있고 출처 webapp_batch',
        all('J20-k' in _d27.get(c, {}).get('meaning', '') and '설계 상 칸' in _d27.get(c, {}).get('meaning', '')
            for c in ('coverage_AM_P_hertz_pct', 'coverage_AM_S_hertz_pct_status', 'n_AM_P_measured', 'cov_AM_S_n_valid',
                      'area_AM_P_SE_n', 'qc_wa_cov_AM_P_minus_harvest_pct'))
        and not any('설계 상 칸' in _d27.get(c, {}).get('meaning', '') for c in ('coverage_AM_total_hertz_pct', 'n_SE_measured', 'block'))
        and _d27.get('wa_mono_phase_name_webapp', {}).get('source') == 'webapp_batch'
        and 'J20-k' in _d27.get('wa_mono_phase_name_webapp', {}).get('meaning', ''))
    chk('⑳ae 보고 — 수확 쪽 (B) 채움 수 (mono_rows 1 · mono_harvest_filled = coverage 1 + n_AM 1 + cov_n_valid 1 = 3)',
        _r20.get('mono_rows') == 1 and _r20.get('mono_harvest_filled') == 3)
    _neg('⑳af ★ 설계 block mono 인데 웹앱 상별 열을 실을 때 수확 n_types 가 없으면 거부 (J20-f 관문 그대로)',
         lambda: build_handover(_dq, {'q1': {k: v for k, v in _hq3['q1'].items() if k != 'n_types'}, 'q2': _hq3['q2']},
                                webapp=_wa3(), webapp_groups='contact'))

    #  ═══ ㉑ 7c (1저자 비준 10-01 *"ㄱㄱ 하자"* · J20-k 7c · 원장 LHS-23) — AM–SE CN 10 열 + 고립 비율 3 + 전체 분포 3 (7a 새 키) ═══════════
    #   5번 배치 (`--stop-after coverage` = 접촉 단계 포함) 를 contact 묶음으로 받는다 · 고립 비율의 09-19 census 🔶 COND_cov 는 오분류 (LHS-23)
    #   → ✅ 승격 (옛 판정을 열 사전에 병기) · census 에 없는 7a 키는 배치 머리에 있을 때만 · 관문 G1–G7 (calc_am_isolation_risk 의 counts 하나에서
    #   나온 값인가) + 상이 있는데 값이 없거나 없는데 값이 있으면 거부.  값은 손으로 정한 입자별 SE 접촉 수에서 만든다.
    import math as _mth
    _cs1 = [0, 1, 3, 3, 4, 4, 4, 5, 5, 5, 6]                          # q1 mono (설계 AM_P · 웹앱 이름 AM_S) — 11 개 · 합 40 = area_AM_S_SE_n
    _cp2, _cs2 = [30], [1, 3, 4, 5, 5, 5, 5, 6, 7, 9]                 # q2 bimodal — AM_P 1 개 (합 30) · AM_S 10 개 (합 50)
    _RP, _RS = 5.0, 2.0                                                # 설계 반경 (µm) — 표면 가중 항등식

    def _stat7(v):
        n_ = len(v)
        mu_ = sum(v) / n_
        return {'mean': repr(mu_), 'std': repr(_mth.sqrt(sum((x - mu_) ** 2 for x in v) / n_)),
                'median': repr(float(np.median(v))), 'max': str(max(v)), 'vul': repr(100.0 * sum(1 for x in v if x <= 1) / n_)}

    def _wa7(stop='coverage'):
        w = _wa3()
        w['stop_after'] = stop
        for k in ['am_se_cn_mean', 'am_se_cn_surface_weighted'] + [f'{p}_se_cn_{s}' for p in ('AM_P', 'AM_S')
                                                                    for s in ('mean', 'std', 'median', 'max')]:
            w['verdict'][k] = '✅ 쓴다'
        for k in ('am_vulnerable_pct', 'AM_P_vulnerable_pct', 'AM_S_vulnerable_pct'):
            w['verdict'][k] = '🔶 채널 종속'                          # 09-19 census 그대로 (COND_cov 오분류 — LHS-23)
        w['why'] = {k: f'why:{k}' for k in w['verdict']}

        def _put(row, ph, v):
            s_ = _stat7(v)
            row.update({f'{ph}_se_cn_mean': s_['mean'], f'{ph}_se_cn_std': s_['std'], f'{ph}_se_cn_median': s_['median'],
                        f'{ph}_se_cn_max': s_['max'], f'{ph}_vulnerable_pct': s_['vul']})
        _put(w['rows']['q1'], 'AM_S', _cs1)
        _put(w['rows']['q2'], 'AM_P', _cp2)
        _put(w['rows']['q2'], 'AM_S', _cs2)
        for q, v, sw in (('q1', _cs1, sum(_cs1) / len(_cs1)),
                         ('q2', _cp2 + _cs2, (_RP ** 2 * sum(_cp2) + _RS ** 2 * sum(_cs2)) / (_RP ** 2 * len(_cp2) + _RS ** 2 * len(_cs2)))):
            s_ = _stat7(v)
            w['rows'][q].update(am_se_cn_mean=s_['mean'], am_se_cn_std=s_['std'], am_se_cn_median=s_['median'],
                                am_se_cn_max=s_['max'], am_vulnerable_pct=s_['vul'], am_se_cn_surface_weighted=repr(sw))
        return w
    _dq7 = [{'case_id': 'q1', 'block': 'mono_AM_P', 'r_AM_P_um': repr(_RP), 'r_AM_S_um': ''},
            {'case_id': 'q2', 'block': 'bimodal', 'r_AM_P_um': repr(_RP), 'r_AM_S_um': repr(_RS)}]

    def _b7(w=None, hv=None, dq=None):
        return build_handover(dq or _dq7, hv or _hq3, webapp=w or _wa7(), webapp_groups='contact')
    try:
        _o7, _c7, _r7 = _b7()
        _e7 = ''
    except Exception as e:                                                # noqa: BLE001
        _o7, _c7, _r7, _e7 = [], [], {}, f'{type(e).__name__}: {e}'
    _m7 = next((r for r in _o7 if r['case_id'] == 'q1'), {})
    _p7 = next((r for r in _o7 if r['case_id'] == 'q2'), {})
    _cols7 = (['am_se_cn_mean', 'am_se_cn_surface_weighted', 'am_se_cn_std', 'am_se_cn_median', 'am_se_cn_max',
               'am_vulnerable_pct', 'AM_P_vulnerable_pct', 'AM_S_vulnerable_pct']
              + [f'{p}_se_cn_{s}' for p in ('AM_P', 'AM_S') for s in ('mean', 'std', 'median', 'max')])
    chk('㉑a ★ 7c — coverage 배치 (stop_after=coverage · 접촉 단계 포함) 를 contact 묶음으로 받고 16 열이 실린다 · 관문 검사 2 행'
        + (f' — {_e7}' if _e7 else ''),
        not _e7 and all(c in _c7 for c in _cols7) and _r7.get('wa_amse_identity_checked') == 2)
    chk('㉑b 값 — bimodal 은 상별 그대로 · mono 는 설계 상 칸 (AM_P) 에 웹앱 AM_S 값 · 없는 상 칸 빈칸 · 전체 열 그대로',
        _p7.get('AM_P_se_cn_mean') == repr(30.0) and _p7.get('AM_S_se_cn_max') == '9' and _p7.get('am_se_cn_max') == '30'
        and _p7.get('am_se_cn_median') == repr(5.0) and _p7.get('AM_S_vulnerable_pct') == repr(10.0)
        and _m7.get('AM_P_se_cn_mean') == repr(40 / 11) and _m7.get('AM_S_se_cn_mean') == ''
        and _m7.get('AM_S_vulnerable_pct') == '' and _m7.get('AM_P_vulnerable_pct') == repr(200 / 11)
        and _m7.get('am_se_cn_mean') == repr(40 / 11))
    _neg('㉑c ★ coverage 배치를 묶음 제한 없이 부르면 여전히 거부 (뒤 단계 열이 빈칸 = N/A 로 읽힌다)',
         lambda: build_handover(_dq7, _hq3, webapp=_wa7()))
    _dm7 = {d['column']: d for d in column_dictionary(_c7, webapp=_wa7())} if _c7 else {}
    chk('㉑d ★ 고립 비율 — census 🔶 COND_cov 를 ✅ 로 승격 (LHS-23) · 열 사전에 옛 판정 병기 · 뜻 = SE 접촉 0–1 개 · coverage 문턱 아님',
        bool(_dm7) and all(_dm7.get(c, {}).get('verdict', '').startswith('✅') and 'LHS-23' in _dm7.get(c, {}).get('verdict', '')
                           and '🔶' in _dm7.get(c, {}).get('meaning', '') and '0–1' in _dm7.get(c, {}).get('meaning', '')
                           and 'coverage' in _dm7.get(c, {}).get('meaning', '')
                           for c in ('am_vulnerable_pct', 'AM_P_vulnerable_pct', 'AM_S_vulnerable_pct')))
    chk('㉑e ★ 7a 새 키 (census 밖) — 배치 머리에 있으면 ✅ (J20-k 7a) · 출처 webapp · 뜻 = AM 전 입자 분포 · 검토 기록 7c',
        bool(_dm7) and all(_dm7.get(c, {}).get('source') == 'webapp' and 'J20-k' in _dm7.get(c, {}).get('verdict', '')
                           and 'AM 전 입자' in _dm7.get(c, {}).get('meaning', '') and '7c' in _dm7.get(c, {}).get('meaning', '')
                           for c in ('am_se_cn_std', 'am_se_cn_median', 'am_se_cn_max')))
    _w7h = _wa7()
    for _r_ in _w7h['rows'].values():
        _r_.pop('am_se_cn_median', None)
    try:
        _c7h = _b7(w=_w7h)[1]
    except Exception as e:                                                # noqa: BLE001
        _c7h = [f'ERR {type(e).__name__}: {e}']
    chk('㉑f census 밖 키가 배치 머리에 없으면 열도 없다 (옛 배치의 빈칸이 측정된 N/A 로 읽히지 않게) · 있는 키는 그대로',
        'am_se_cn_median' not in _c7h and 'am_se_cn_max' in _c7h)

    def _neg7(name, fn, tag):
        """거부 + **그 관문**이 거부했는가 (메시지에 tag) — 다른 관문이 먼저 막으면 이 반례는 그 관문을 시험하지 못한 것이다."""
        nonlocal ok
        try:
            fn()
        except FillRefusal as e:
            if tag in str(e):
                ok += 1
                print(f'  PASS  {name} — 거부: {str(e)[:64]}')
            else:
                fail.append(name)
                print(f'  FAIL  {name} — 다른 관문이 거부: {str(e)[:120]}')
            return
        except Exception as e:                                            # noqa: BLE001
            fail.append(name)
            print(f'  FAIL  {name} — {type(e).__name__}: {e}')
            return
        fail.append(name)
        print(f'  FAIL  {name} — 거부하지 않았다')

    def _bad7(q, **kv):
        w = _wa7()
        w['rows'][q].update(kv)
        return lambda: _b7(w=w)
    _neg7('㉑g ★ G1 — 상별 평균 × 상 입자 수 ≠ area_<상>_SE_n (5.5 × 10 ≠ 50) 이면 거부', _bad7('q2', AM_S_se_cn_mean='5.5'), '7c G1')
    _neg7('㉑h ★ G1 mono — 설계 상 칸으로 옮긴 평균 × AM 수 ≠ 옮긴 쌍 개수 (3.0 × 11 ≠ 40) 이면 거부', _bad7('q1', AM_S_se_cn_mean='3.0'), '7c G1')
    _neg7('㉑i ★ G2 — 전체 평균 × AM 수 ≠ area_AM전체_SE_n (7.0 × 11 ≠ 80) 이면 거부', _bad7('q2', am_se_cn_mean='7.0'), '7c G2')
    _neg7('㉑j ★ G3 — 고립 개수: 전체 2 ≠ 상별 합 (AM_P 0 + AM_S 1) 이면 거부', _bad7('q2', am_vulnerable_pct=repr(200 / 11)), '7c G3')
    _neg7('㉑k ★ G3 — 고립 비율 × 입자 수 / 100 이 정수 개수가 아니면 거부 (25 % × 10 = 2.5)', _bad7('q2', AM_S_vulnerable_pct='25.0'), '7c G3')
    _neg7('㉑l ★ G4 — 전체 max ≠ 상별 max 의 최댓값 (9 ≠ 30) 이면 거부', _bad7('q2', am_se_cn_max='9'), '7c G4')
    _neg7('㉑m ★ G5 — bimodal 전체 median 이 상별 median 사이 밖 (31 ∉ [5, 30]) 이면 거부', _bad7('q2', am_se_cn_median='31.0'), '7c G5')
    _neg7('㉑n ★ G5 mono — 전체 median ≠ 단일 상 median (4.5 ≠ 4.0) 이면 거부', _bad7('q1', am_se_cn_median='4.5'), '7c G5')
    _neg7('㉑o ★ G6 — 전체 std ≠ 합동 표준편차 (상별 N · 평균 · std) 이면 거부', _bad7('q2', am_se_cn_std='7.0'), '7c G6')
    _neg7('㉑p ★ G6 mono — 전체 std ≠ 단일 상 std 이면 거부', _bad7('q1', am_se_cn_std='1.8'), '7c G6')
    _neg7('㉑q ★ G7 — 표면 가중 ≠ Σ N r² CN / Σ N r² (설계 반경) 이면 거부', _bad7('q2', am_se_cn_surface_weighted='15.0'), '7c G7')
    _neg7('㉑r ★ G7 — bimodal 인데 설계 반경이 없으면 거부 (표면 가중을 확인할 수 없다)',
          lambda: _b7(dq=[_dq7[0], dict(_dq7[1], r_AM_S_um='')]), '7c G7')
    _neg7('㉑s ★ 상이 있는데 상별 값이 비면 거부 (bimodal AM_S std 빈칸)', _bad7('q2', AM_S_se_cn_std=''), '7c 상 있음')
    _neg7('㉑t ★ 상이 없는데 (phase_counts AM_P 0) 상별 값이 있으면 거부',
          lambda: _b7(hv=dict(_hq3, q2=dict(_hq3['q2'], phase_counts={'AM_P': 0, 'AM_S': 11, 'SE': 100}))), '7c 상 없음')
    _neg7('㉑u ★ 수확 JSON 에 phase_counts 가 없으면 거부 (상 입자 수를 몰라 관문을 못 본다 · bimodal 행 — mono 는 J20-k (B) 가 먼저 막는다)',
          lambda: _b7(hv=dict(_hq3, q2={kk: vv for kk, vv in _hq3['q2'].items() if kk != 'phase_counts'}), w=(lambda w_: (
              [w_['verdict'].pop(k_, None) for k_ in ('se_se_cn', 'se_se_cn_std', 'am_am_cn', 'am_am_cn_std', 'am_am_n_contacts')], w_)[1])(_wa7())),
          '(7c)')
    _w7r = _wa7()
    _w7r['status']['q2']['status'] = 'REFUSED'
    _w7r['rows']['q2']['AM_S_se_cn_mean'] = '99.0'
    try:
        _r7r = _b7(w=_w7r)[2]
        _e7r = ''
    except Exception as e:                                                # noqa: BLE001
        _r7r, _e7r = {}, f'{type(e).__name__}: {e}'
    chk('㉑v 배치가 거부한 행 (REFUSED) 은 값을 싣지 않으므로 관문도 보지 않는다 (검사 1 행 = q1)' + (f' — {_e7r}' if _e7r else ''),
        not _e7r and _r7r.get('wa_amse_identity_checked') == 1)
    _dm7b = {d['column']: d for d in column_dictionary(_c7, webapp=_wa7())} if _c7 else {}
    chk('㉑w 열 사전 — AM–SE CN · 고립 열에 검토 기록 (7c · 관문 G1–G7) · 상별 열은 mono 설계 상 칸 표지 · 전체 열은 아님',
        all('7c' in _dm7b.get(c, {}).get('meaning', '') for c in _cols7)
        and '설계 상 칸' in _dm7b.get('AM_P_vulnerable_pct', {}).get('meaning', '')
        and '설계 상 칸' not in _dm7b.get('am_vulnerable_pct', {}).get('meaning', ''))
    #  ═══ ㉒ ② 퍼콜레이션 (J20-b 감사 · 1저자 비준 10-01 *"퍼콜레이션은 그렇게 가고"* · LHS-19 · LHS-20) ═════════════════════════════════
    #   접촉 분석 단계가 내는 SE 그래프 열 7 개를 percolation 묶음으로 싣는다 (`--webapp-groups contact,percolation`) · top_reachable · ionic_active 의
    #   census 🔶 COND_cov 는 오분류 (LHS-20) → ✅ · electronic_active_fraction (망 단계) · se_se_cn_eff_area_perc (면적 · ⑦) 는 census ✅ 여도 안 싣는다 ·
    #   관문 P1 (관통 일관 + 수확기 독립 재현 — J20-b F8) · P2 (범위 · 순서) · P3 (관통 SE 개수 = percolation_pct × N_SE / 100).
    def _wa8():
        w = _wa7()
        w['verdict'].update(percolation_pct='✅ 쓴다', n_components='✅ 쓴다', n_large_components='✅ 쓴다', se_se_cn_perc='✅ 쓴다',
                            se_se_cn_n_perc='✅ 쓴다', top_reachable_pct='🔶 채널 종속', ionic_active_pct='🔶 채널 종속',
                            electronic_active_fraction='✅ 쓴다', se_se_cn_eff_area_perc='✅ 쓴다(이름 주의)')
        w['why'] = {k: f'why:{k}' for k in w['verdict']}
        w['rows']['q1'].update(percolation_pct='37.0', top_reachable_pct='40.0', n_components='12', n_large_components='2',
                               ionic_active_pct=repr(900 / 11), se_se_cn_perc='5.5', se_se_cn_n_perc='37', se_se_cn_eff_area_perc='0.05')
        w['rows']['q2'].update(percolation_pct='0.0', top_reachable_pct='15.0', n_components='30', n_large_components='3',
                               ionic_active_pct=repr(500 / 11))             # 관통 없음 — _perc 키 자체가 없다 (웹앱 그대로) · 5/11 (v1.1 D3 정수 개수)
        for _k in ('se_se_cn_perc', 'se_se_cn_eff_area_perc', 'se_se_cn_n_perc'):   # _wa3 의 J20-i 시험용 값 — 비관통 침대에는 없다
            w['rows']['q2'].pop(_k, None)
        return w

    def _hq8(span1=2, span2=0):
        return {'q1': dict(_hq3['q1'], tau_detail={'band_detail': {'wall_n_span_components': span1}}),
                'q2': dict(_hq3['q2'], tau_detail={'band_detail': {'wall_n_span_components': span2}})}

    def _b8(w=None, hv=None, groups='contact,percolation'):
        return build_handover(_dq7, hv or _hq8(), webapp=w or _wa8(), webapp_groups=groups)
    try:
        _o8, _c8, _r8 = _b8()
        _e8 = ''
    except Exception as e:                                                # noqa: BLE001
        _o8, _c8, _r8, _e8 = [], [], {}, f'{type(e).__name__}: {e}'
    _m8 = next((r for r in _o8 if r['case_id'] == 'q1'), {})
    _p8 = next((r for r in _o8 if r['case_id'] == 'q2'), {})
    _pc8 = ('percolation_pct', 'top_reachable_pct', 'n_components', 'n_large_components', 'ionic_active_pct', 'se_se_cn_perc', 'se_se_cn_n_perc')
    chk('㉒a ★ ② — contact,percolation 묶음: 퍼콜레이션 7 열 + ① 열 · 망 단계 electronic_active_fraction · 면적 se_se_cn_eff_area_perc 는 안 싣는다 · '
        '관문 검사 2 행' + (f' — {_e8}' if _e8 else ''),
        not _e8 and all(c in _c8 for c in _pc8) and 'am_se_cn_mean' in _c8
        and 'electronic_active_fraction' not in _c8 and 'se_se_cn_eff_area_perc' not in _c8 and _r8.get('wa_perc_checked') == 2)
    chk('㉒b 값 — 관통 침대 (q1) 는 _perc 값 · 비관통 (q2) 은 percolation_pct 0.0 · _perc 빈칸 (N/A) · 나머지 그대로',
        _m8.get('percolation_pct') == '37.0' and _m8.get('se_se_cn_n_perc') == '37' and _m8.get('se_se_cn_perc') == '5.5'
        and _p8.get('percolation_pct') == '0.0' and _p8.get('se_se_cn_perc') == '' and _p8.get('se_se_cn_n_perc') == ''
        and _p8.get('n_components') == '30' and _m8.get('ionic_active_pct') == repr(900 / 11))
    try:
        _c8c = _b8(groups='contact')[1]
    except Exception as e:                                                # noqa: BLE001
        _c8c = [f'ERR {type(e).__name__}: {e}']
    chk('㉒c contact 묶음만이면 퍼콜레이션 열은 없다 (묶음 거르기)', 'am_se_cn_mean' in _c8c and not any(c in _c8c for c in _pc8))
    _dm8 = {d['column']: d for d in column_dictionary(_c8, webapp=_wa8())} if _c8 else {}
    _g8 = lambda c, k: (_dm8.get(c) or {}).get(k, '')                     # noqa: E731
    chk('㉒d ★ LHS-20 — top_reachable · ionic_active 를 ✅ 로 승격 · 옛 판정 병기 · F3 한정어 (외톨이 · 문턱 10 · 0.0 = 미퍼콜 · 솔버 관통과 다름 · N/A)',
        all(_g8(c, 'verdict').startswith('✅') and 'LHS-20' in _g8(c, 'verdict') and '🔶' in _g8(c, 'meaning')
            for c in ('top_reachable_pct', 'ionic_active_pct'))
        and '외톨이' in _g8('n_components', 'meaning') and '10' in _g8('n_large_components', 'meaning')
        and '0.0' in _g8('percolation_pct', 'meaning') and '솔버' in _g8('percolation_pct', 'meaning')
        and 'N/A' in _g8('se_se_cn_perc', 'meaning') and '외톨이' in _g8('top_reachable_pct', 'meaning')
        and 'coverage' in _g8('ionic_active_pct', 'meaning') and 'J20-b' in _g8('percolation_pct', 'meaning')
        and 'LHS-17' in _g8('percolation_pct', 'caveat'))
    _neg('㉒e 모르는 묶음 이름이 섞이면 거부 (contact,stress — ⑤⑥⑦ 뒤 fracture 는 아는 묶음)', lambda: _b8(groups='contact,stress'))

    def _bad8(q, **kv):
        w = _wa8()
        w['rows'][q].update(kv)
        return lambda: _b8(w=w)
    _neg7('㉒f ★ P1 — 비관통 (percolation_pct 0) 인데 se_se_cn_perc 에 값이 있으면 거부', _bad8('q2', se_se_cn_perc='4.0'), '② P1')
    _neg7('㉒g ★ P1 — 관통인데 se_se_cn_n_perc 가 비면 거부', _bad8('q1', se_se_cn_n_perc=''), '② P1')
    _neg7('㉒h ★ P1 — 웹앱 관통 ↔ 수확기 벽 밴드 관통 (0 성분) 이 어긋나면 거부 (J20-b F8 독립 재현)', lambda: _b8(hv=_hq8(span1=0)), '② P1')
    _neg7('㉒i ★ P1 — 웹앱 비관통 ↔ 수확기 관통 (1 성분) 이 어긋나면 거부', lambda: _b8(hv=_hq8(span2=1)), '② P1')
    _neg7('㉒j ★ P1 — 수확 JSON 에 벽 밴드 관통 진단이 없으면 거부 (독립 재현을 볼 수 없다)', lambda: _b8(hv=dict(_hq8(), q2=_hq3['q2'])), '② P1')
    _neg7('㉒k ★ P2 — 비율이 [0, 100] 밖이면 거부 (ionic_active_pct 101)', _bad8('q2', ionic_active_pct='101.0'), '② P2')
    _neg7('㉒l ★ P2 — n_large_components > n_components 이면 거부', _bad8('q2', n_large_components='31'), '② P2')
    _neg7('㉒m ★ P2 — top_reachable_pct < percolation_pct 이면 거부 (관통 SE 는 위 밴드에 닿는다)', _bad8('q1', top_reachable_pct='30.0'), '② P2')
    _neg7('㉒n ★ P2 — 성분 수가 정수가 아니면 거부', _bad8('q2', n_components='30.5'), '② P2')
    _neg7('㉒o ★ P3 — 관통 SE 개수 ≠ percolation_pct × N_SE / 100 (38 ≠ 37) 이면 거부', _bad8('q1', se_se_cn_n_perc='38'), '② P3')
    _w8r = _wa8()
    _w8r['status']['q2']['status'] = 'REFUSED'
    _w8r['rows']['q2']['se_se_cn_perc'] = '9.9'
    try:
        _r8r = _b8(w=_w8r)[2]
        _e8r = ''
    except Exception as e:                                                # noqa: BLE001
        _r8r, _e8r = {}, f'{type(e).__name__}: {e}'
    chk('㉒p 배치가 거부한 행 (REFUSED) 은 값을 싣지 않으므로 관문도 보지 않는다 (검사 1 행)' + (f' — {_e8r}' if _e8r else ''),
        not _e8r and _r8r.get('wa_perc_checked') == 1)
    chk('㉒q 열 사전 — 퍼콜레이션 열에 검토 기록 (J20-b ② · 관문 P1–P3) · 출처 webapp',
        all('J20-b ②' in _g8(c, 'meaning') and _g8(c, 'source') == 'webapp' for c in _pc8))
    #  ═══ ㉓ 벽 τ 닫기 (1저자 10-01 *"dijkstra tortuosity 벽을 확실하게 닫고 값을 추출"* · J20 · 수확 v3 원천) ═════════════════════════════
    #   관문 T1 (관통 성분 수 — 상태 · 수확 벽 밴드 진단과 같아야) · T2 (값 [1, 20) · 표본 수 규칙) · T3 (② 퍼콜레이션과 비관통 판정 같아야) ·
    #   열 사전 = 기하 최단경로 · 수송 τ 아님 (COMSOL 입력은 τ_Laplace,eff) · 벽 접촉 비율 = 겹침 깊이 > 0 (접선 제외 — 수확기 규칙과 같은 문구).
    def _tw9(status='OK', span=2, mean=1.45, med=1.4, ns_=200, nv=200, ntr=0):
        ok_ = status == 'OK'
        return {'tau_mean': (mean if ok_ else None), 'tau_median': (med if ok_ else None), 'tau_mean_untruncated': (mean if ok_ else None),
                'status': status, 'n_sampled': (ns_ if ok_ else 0), 'n_valid': (nv if ok_ else 0), 'n_truncated': ntr,
                'n_span_components': span, 'tau_convention': TAU_WALL_CONVENTION}

    def _hq9(t1=None, t2=None, wt=True):
        hv = _hq8()
        hv['q1'] = dict(hv['q1'], tau_wall_detail=t1 or _tw9('OK', 2))
        hv['q2'] = dict(hv['q2'], tau_wall_detail=t2 or _tw9('NOT_PERCOLATING', 0))
        if wt:
            hv['q1']['wall_touch'] = {'SE': {'floor': 0.25, 'plate': 0.125}, 'AM': {'floor': 0.5, 'plate': 0.0}}
            hv['q2']['wall_touch'] = {'SE': {'floor': 0.5, 'plate': 0.0}, 'AM_P': {'floor': 1.0, 'plate': 0.0},
                                      'AM_S': {'floor': 0.0, 'plate': 0.2}, 'AM': {'floor': 1 / 11, 'plate': 2 / 11}}
        return hv
    try:
        _o9, _c9, _r9 = _b8(hv=_hq9())
        _e9 = ''
    except Exception as e:                                                # noqa: BLE001
        _o9, _c9, _r9, _e9 = [], [], {}, f'{type(e).__name__}: {e}'
    _m9 = next((r for r in _o9 if r['case_id'] == 'q1'), {})
    _p9 = next((r for r in _o9 if r['case_id'] == 'q2'), {})
    chk('㉓a ★ 벽 τ — 관통 침대는 값 · 비관통은 빈칸 (N/A) · 관문 T1–T2 2 행 · T3 (↔ 퍼콜레이션) 2 행' + (f' — {_e9}' if _e9 else ''),
        not _e9 and _m9.get('tortuosity_SE_wall') == repr(1.45) and _p9.get('tortuosity_SE_wall') == ''
        and _p9.get('tortuosity_SE_wall_status') == 'NOT_PERCOLATING'
        and _r9.get('tau_wall_checked') == 2 and _r9.get('tau_perc_crosschecked') == 2)
    _dm9 = {d['column']: d for d in column_dictionary(_c9, webapp=_wa8())} if _c9 else {}
    _tm = (_dm9.get('tortuosity_SE_wall') or {}).get('meaning', '')
    _wm = (_dm9.get('wall_touch_frac_SE_floor') or {}).get('meaning', '')
    chk('㉓b ★ 열 사전 — 벽 τ = 기하 최단경로 · 수송 τ 아님 (수송 굴곡도 = 망 단계 tau2 · τ 명명 규약 10-03 — 옛 "COMSOL/EIS 입력 τ 는 '
        'τ_Laplace,eff" 철회 TAU-01) · 비관통 N/A · 표본 200 쌍',
        '기하 최단경로' in _tm and 'tau2' in _tm and 'COMSOL/EIS 입력 τ 는 τ_Laplace' not in _tm and 'N/A' in _tm and '200 쌍' in _tm)
    chk('㉓c ★ 벽 접촉 비율 문구 = 수확기 규칙 (겹침 깊이 > 0 · 접선은 안 셈) — 옛 "≤ 0 · ≥ plate_z" 없음',
        '겹침 깊이 > 0' in _wm and '접선' in _wm and '≤ 0' not in _wm and 'z − r < 0' in _wm)
    try:
        import lhs_descriptor_harvest as _LDH9
        _same9 = (_LDH9.TAU_LO, _LDH9.TAU_HI, _LDH9.N_TAU_PAIRS) == (TAU_WALL_LO, TAU_WALL_HI, TAU_WALL_N_PAIRS) \
            and 'tangent' in _LDH9.WALL_TOUCH_RULE and '> 0' in _LDH9.WALL_TOUCH_RULE
    except Exception as e:                                                # noqa: BLE001
        _same9 = False
    chk('㉓d 관문 상수 = 수확기 (TAU_LO · TAU_HI · N_TAU_PAIRS) · 수확기 규칙이 접선 제외 · 한쪽만 바뀌면 걸린다', _same9)
    _neg7('㉓e ★ T1 — 상태 OK 인데 관통 성분 0 이면 거부', lambda: _b8(hv=_hq9(t1=_tw9('OK', 0))), 'τ T1')
    _neg7('㉓f ★ T1 — NOT_PERCOLATING 인데 관통 성분 1 이면 거부', lambda: _b8(hv=_hq9(t2=_tw9('NOT_PERCOLATING', 1))), 'τ T1')
    _neg7('㉓g ★ T1 — 벽 τ 관통 성분 (3) ≠ 수확 벽 밴드 진단 (2) 이면 거부', lambda: _b8(hv=_hq9(t1=_tw9('OK', 3))), 'τ T1')
    _neg7('㉓h ★ T2 — OK 인데 τ 평균이 [1, 20) 밖 (25) 이면 거부', lambda: _b8(hv=_hq9(t1=_tw9('OK', 2, mean=25.0))), 'τ T2')
    _neg7('㉓i ★ T2 — n_valid > n_sampled 이면 거부', lambda: _b8(hv=_hq9(t1=_tw9('OK', 2, ns_=150, nv=180))), 'τ T2')
    _neg7('㉓j ★ T2 — 잘린 수 = 경로 수 (남은 표본 0) 인데 OK 면 거부', lambda: _b8(hv=_hq9(t1=_tw9('OK', 2, nv=200, ntr=200))), 'τ T2')
    _w9 = _wa8()
    _w9['rows']['q2'].update(percolation_pct='12.0', se_se_cn_perc='5.0', se_se_cn_n_perc='12')
    _neg7('㉓k ★ T3 — 벽 τ 비관통인데 웹앱 percolation_pct > 0 이면 거부 (수확기 벽 밴드 진단도 0 이라 P1 이 먼저면 P1)',
          lambda: _b8(w=_w9, hv=_hq9(t2=_tw9('NOT_PERCOLATING', 0))), '② P1')
    _neg7('㉓l ★ n_span_components 가 정수가 아니면 거부', lambda: _b8(hv=_hq9(t1=_tw9('OK', 2.0))), 'τ T1')
    #  ═══ ㉔ v1.1 ①②③ (1저자 비준 10-01 *"비준이야"* · J20-o) ════════════════════════════════════════════════════════════════════════════
    #   ① am_ionic_isolated_pct = 100 − ionic_active_pct — 경로 기준 고립 (이온이 못 가는 AM) · 생성기 유도 (재실행 없음) · 고립 위험 (vulnerable) 과 다른 양
    #   ② 분해 — 웹앱 v1.1 이 새로 내보내는 키 (단절 · 무접촉 · 상별 셋) · 배치 머리에 있을 때만 · 관문 D1–D5 (합 100 · 상별 합 100 · 정수 개수 ·
    #      상별 개수 합 = 전체 · 무접촉 ≤ 고립 위험) · mono 는 설계 상 칸
    #   ③ 가장 큰 SE 덩어리 — SE 비율 · z 폭 (벽 간격 기준 = 기록 z 폭 × 전 입자 z 범위 / 벽 간격 · 정확 환산 · 재실행 없음) · 관문 C1–C3
    def _wa10(dec=True):
        w = _wa8()
        if dec:
            w['rows']['q1'].update(ionic_dead_pct=repr(100 / 11), ionic_no_se_pct=repr(100 / 11), AM_S_ionic_active_pct=repr(900 / 11),
                                   AM_S_ionic_dead_pct=repr(100 / 11), AM_S_ionic_no_se_pct=repr(100 / 11))
            w['rows']['q2'].update(ionic_dead_pct=repr(600 / 11), ionic_no_se_pct='0.0',
                                   AM_P_ionic_active_pct='100.0', AM_P_ionic_dead_pct='0.0', AM_P_ionic_no_se_pct='0.0',
                                   AM_S_ionic_active_pct='40.0', AM_S_ionic_dead_pct='60.0', AM_S_ionic_no_se_pct='0.0')
        return w

    def _bd10(n_se=100, frac=0.37, zs=0.95, zlo=-0.5, zhi=40.5, pz=40.0, fl=0.0):
        return {'n_se': n_se, 'largest_comp_frac': frac, 'largest_comp_z_span_frac': zs, 'z_lo': zlo, 'z_hi': zhi,
                'alt_plate_z': pz, 'wall_z_floor': fl}

    def _hq10(b1=None, b2=None):
        hv = _hq9()
        for q, b, span in (('q1', b1 or _bd10(), 2), ('q2', b2 or _bd10(frac=0.25, zs=0.5), 0)):
            hv[q] = dict(hv[q], plate_z_sim=40.0, z_floor_sim=0.0, tau_detail={'band_detail': dict(b, wall_n_span_components=span)})
        return hv

    def _b10(w=None, hv=None):
        return build_handover(_dq7, hv or _hq10(), webapp=w or _wa10(), webapp_groups='contact,percolation')
    try:
        _o10, _c10, _r10 = _b10()
        _e10 = ''
    except Exception as e:                                                # noqa: BLE001
        _o10, _c10, _r10, _e10 = [], [], {}, f'{type(e).__name__}: {e}'
    _m10 = next((r for r in _o10 if r['case_id'] == 'q1'), {})
    _p10 = next((r for r in _o10 if r['case_id'] == 'q2'), {})
    chk('㉔a ★ ① am_ionic_isolated_pct = 100 − ionic_active_pct (q1 · q2) · 활성 열 뒤 · 활성 열이 실리면 늘 (재실행 없음)' + (f' — {_e10}' if _e10 else ''),
        not _e10 and _m10.get('am_ionic_isolated_pct') == repr(100.0 - 900 / 11) and _p10.get('am_ionic_isolated_pct') == repr(100.0 - 500 / 11)
        and 'ionic_active_pct' in _c10 and _c10.index('am_ionic_isolated_pct') > _c10.index('ionic_active_pct'))
    _dec10 = ('ionic_dead_pct', 'ionic_no_se_pct') + tuple(f'{ph}_ionic_{s_}_pct' for ph in ('AM_P', 'AM_S') for s_ in ('active', 'dead', 'no_se'))
    try:
        _c10o = _b10(w=_wa10(dec=False))[1]
    except Exception as e:                                                # noqa: BLE001
        _c10o = [f'ERR {type(e).__name__}: {e}']
    chk('㉔b ② 분해 키가 배치 머리에 없으면 (5번 배치 세대) 분해 열도 없다 · ① 은 그대로 (활성에서 유도)',
        'am_ionic_isolated_pct' in _c10o and not any(c in _c10o for c in _dec10))
    chk('㉔c ★ ② 새 배치 — 분해 열 8 개 · mono (설계 AM_P · 웹앱 이름 AM_S) 는 설계 상 칸 · 없는 상 칸 빈칸 · 관문 D 2 행',
        all(c in _c10 for c in _dec10) and _m10.get('AM_P_ionic_dead_pct') == repr(100 / 11) and _m10.get('AM_S_ionic_dead_pct') == ''
        and _m10.get('ionic_no_se_pct') == repr(100 / 11) and _p10.get('AM_S_ionic_active_pct') == '40.0' and _p10.get('ionic_no_se_pct') == '0.0'
        and _r10.get('wa_ionic_checked') == 2)
    _dm10 = {d['column']: d for d in column_dictionary(_c10, webapp=_wa10())} if _c10 else {}
    _g10 = lambda c, k: (_dm10.get(c) or {}).get(k, '')                   # noqa: E731
    chk('㉔d ★ 열 사전 — ① 경로 기준 고립 = 100 − ionic_active_pct · 고립 위험 (vulnerable) 과 다른 양 · ② 단절 · 무접촉 정의 · 새 키 판정 (v1.1 ②)',
        '경로 기준 고립' in _g10('am_ionic_isolated_pct', 'meaning') and '100 − ionic_active_pct' in _g10('am_ionic_isolated_pct', 'meaning')
        and '고립 위험' in _g10('am_ionic_isolated_pct', 'meaning') and 'v1.1 ①' in _g10('am_ionic_isolated_pct', 'meaning')
        and '닿았지만' in _g10('ionic_dead_pct', 'meaning') and 'SE 접촉 0' in _g10('ionic_no_se_pct', 'meaning')
        and 'v1.1 ②' in _g10('ionic_dead_pct', 'verdict') and _g10('ionic_dead_pct', 'source') == 'webapp'
        and 'v1.1 ②' in _g10('AM_P_ionic_active_pct', 'verdict') and '설계 상 칸' in _g10('AM_P_ionic_active_pct', 'meaning'))

    def _bad10(q, **kv):
        w = _wa10()
        w['rows'][q].update(kv)
        return lambda: _b10(w=w)
    _neg7('㉔e ★ D1 — 활성 + 단절 + 무접촉 ≠ 100 이면 거부', _bad10('q2', ionic_no_se_pct=repr(100 / 11)), 'v1.1 D1')
    _neg7('㉔f ★ D2 — 상별 활성 + 단절 + 무접촉 ≠ 100 이면 거부 (AM_S 40 + 50 + 0)', _bad10('q2', AM_S_ionic_dead_pct='50.0'), 'v1.1 D2')
    _neg7('㉔g ★ D3 — 비율 × 입자 수 / 100 이 정수 개수가 아니면 거부 (활성 45 % × 11 = 4.95)',
          _bad10('q2', ionic_active_pct='45.0', ionic_dead_pct='55.0'), 'v1.1 D3')
    _neg7('㉔h ★ D4 — 상별 개수 합 ≠ 전체 개수 (AM_P 1 + AM_S 3 ≠ 활성 5) 이면 거부',
          _bad10('q2', AM_S_ionic_active_pct='30.0', AM_S_ionic_dead_pct='70.0'), 'v1.1 D4')
    _neg7('㉔i ★ D5 — 무접촉 개수 (2) > 고립 위험 개수 (1 — SE 접촉 0 ⊂ 0–1 개) 이면 거부',
          _bad10('q2', ionic_dead_pct=repr(400 / 11), ionic_no_se_pct=repr(200 / 11), AM_S_ionic_dead_pct='40.0', AM_S_ionic_no_se_pct='20.0'),
          'v1.1 D5')
    _neg7('㉔j ★ 상 있음 — 상이 있는데 상별 분해가 비면 거부 (bimodal AM_P 단절 빈칸)', _bad10('q2', AM_P_ionic_dead_pct=''), 'v1.1 상 있음')
    _w10k = _wa10(dec=False)
    _w10k['rows']['q2']['ionic_active_pct'] = '45.0'
    _neg7('㉔k ★ D3 — 분해 키가 없는 옛 배치에서도 활성 비율 × AM 수 / 100 이 정수 개수가 아니면 거부 (①의 원천)',
          lambda: _b10(w=_w10k), 'v1.1 D3')
    chk('㉔l ★ ③ 가장 큰 SE 덩어리 — SE 비율 · 벽 간격 대비 z 폭 (= 기록 z 폭 × 전 입자 z 범위 / 벽 간격) · 전 입자 z 범위 대비 원값 · 관문 C 2 행',
        _m10.get('se_largest_comp_frac') == repr(0.37) and _m10.get('se_largest_comp_wall_span_frac') == repr(0.95 * 41.0 / 40.0)
        and _p10.get('se_largest_comp_env_span_frac') == repr(0.5) and _p10.get('se_largest_comp_wall_span_frac') == repr(0.5 * 41.0 / 40.0)
        and _r10.get('se_cluster_checked') == 2)
    chk('㉔m ★ 열 사전 — ③ 분모 (벽 간격 · 전 입자 z 범위 — 바닥 아래로 샌 입자) · 가장 큰 = SE 수 기준 · 1 을 넘을 수 있음 · v1.1 ③ · 출처 harvest_v3',
        '벽 간격' in _g10('se_largest_comp_wall_span_frac', 'meaning') and '1 을 넘' in _g10('se_largest_comp_wall_span_frac', 'meaning')
        and '전 입자' in _g10('se_largest_comp_env_span_frac', 'meaning') and 'SE 수' in _g10('se_largest_comp_frac', 'meaning')
        and 'v1.1 ③' in _g10('se_largest_comp_frac', 'meaning') and _g10('se_largest_comp_frac', 'source') == 'harvest_v3')
    _neg7('㉔n ★ C1 — 덩어리 SE 비율 × SE 수 가 정수가 아니면 거부 (0.375 × 100)', lambda: _b10(hv=_hq10(b1=_bd10(frac=0.375))), 'v1.1 C1')
    _neg7('㉔o ★ C1 — band SE 수 ≠ 수확 phase_counts SE 이면 거부', lambda: _b10(hv=_hq10(b1=_bd10(n_se=99))), 'v1.1 C1')
    _neg7('㉔p ★ C2 — 전 입자 z 범위 대비 z 폭 > 1 이면 거부 (덩어리 ⊂ 전 입자)', lambda: _b10(hv=_hq10(b1=_bd10(zs=1.2))), 'v1.1 C2')
    _neg7('㉔q ★ C3 — 벽 간격의 플래튼 ≠ 수확 plate_z_sim 이면 거부 (다른 판)', lambda: _b10(hv=_hq10(b1=_bd10(pz=39.0))), 'v1.1 C3')
    _neg7('㉔r ★ ③ 수확 세대 혼합 — 일부 행만 덩어리 기록이 있으면 거부', lambda: _b10(hv=dict(_hq10(), q2=_hq9()['q2'])), '덩어리')
    #  ═══ ㉕ ⑤⑥⑦ (J20-s · 1저자 비준 10-04 *"권고대로"*) — F1 근접쌍 · Auerbach 힘 기반 파괴 · 접촉 면적 (A_dem_geometric) 묶음 ═══════════════
    #   새 계산 없음 (10-01 d1ec42fba 배치 값) · 묶음 f1 · fracture · area (접촉 분석 단계 산출) · 명시 제외 (path_hop_area = LHS-32 · δ 판 ·
    #   상 쌍별 파괴 · physics 면적) · 관문 ⑤F1 · ⑥R1–R3 · ⑦A1–A5 (10-01 실측 130/130 · 64/64 가 통과한 항등식) · 접촉 0 쌍 평균 = 빈칸 · 총합 0 채움
    _ST = ('intact', 'microcrack', 'multicrack', 'fragmentation', 'pulverization')

    def _frf(counts):
        n_t = sum(counts)
        d = {f'n_{s_}_force_AM_AM': str(n_) for s_, n_ in zip(_ST, counts)}
        d['n_total_AM_AM_force'] = str(n_t)
        if n_t:
            d.update({f'frac_{s_}_force_pct': repr(round(100.0 * n_ / n_t, 2)) for s_, n_ in zip(_ST, counts)})
            d['fracture_index_force'] = repr(round((counts[3] + counts[4]) / n_t, 4))
        return d
    _R_SE = 0.5

    def _eff(tot, nse=100, r_=_R_SE):
        return repr(2.0 * tot / (nse * 4.0 * _mth.pi * r_ * r_))

    def _wa11():
        w = _wa10()
        new_ok = (['se_se_cn_aug', 'se_se_cn_aug_std', 'se_se_cn_aug_n_extra', 'se_se_cn_aug_h_spread_sim', 'fracture_index_force',
                   'n_total_AM_AM_force', 'se_se_cn_eff_area', 'am_am_mean_area', 'am_am_total_area']
                  + [f'frac_{s_}_force_pct' for s_ in _ST] + [f'n_{s_}_force_AM_AM' for s_ in _ST]
                  + [f'area_{p_}_{st}' for p_ in ('AM_P_AM_P', 'AM_P_AM_S', 'AM_S_AM_S', 'AM_P_SE', 'AM_S_SE', 'AM전체_SE', 'SE_SE')
                     for st in ('mean', 'total')]
                  #  근처의 census ✅ 열 — 인계 제외 (명시)
                  + ['path_hop_area_mean', 'path_hop_area_min_mean', 'frac_intact_pct', 'fracture_index', 'n_intact_AM_AM', 'n_total_AM_AM',
                     'frac_intact_force_AM_P-AM_S_pct', 'n_intact_force_AM_P-AM_P', 'n_total_force_AM_S-AM_S', 'area_SE_SE_total_physics']
                  #  쌍별 개수 — census 전부 ✅ (① 접촉 묶음 · J20-g) · 접촉 0 쌍 시험 (㉕e · f) 에 필요
                  + [f'area_{p_}_n' for p_ in ('AM_P_AM_P', 'AM_P_AM_S', 'AM_S_AM_S', 'AM_P_SE', 'AM_S_SE')])
        for k_ in new_ok:
            w['verdict'][k_] = '✅ 쓴다(이름 주의)' if 'area' in k_ else '✅ 쓴다'
        w['why'] = {k_: f'why:{k_}' for k_ in w['verdict']}
        q1_, q2_ = w['rows']['q1'], w['rows']['q2']
        #  q1 mono (웹앱 이름 AM_S · SE 100 · AM 11) — F1: 18 + 2 · 50 / 100 = 19 · 면적 = 평균 × 개수 (SE–SE 900 · AM_S–AM_S 11 · AM_S–SE 40)
        q1_.update(se_se_cn_aug='19.0', se_se_cn_aug_std='2.6', se_se_cn_aug_n_extra='50', se_se_cn_aug_h_spread_sim='1e-05',
                   area_SE_SE_mean='0.004', area_SE_SE_total='3.6', se_se_cn_eff_area=_eff(3.6),
                   area_AM_S_AM_S_mean='0.02', area_AM_S_AM_S_total='0.22', am_am_total_area='0.22', am_am_mean_area='0.02',
                   area_AM_S_SE_mean='0.01', area_AM_S_SE_total='0.4',
                   path_hop_area_mean='0.5', path_hop_area_min_mean='0.1', frac_intact_pct='50.0', fracture_index='0.2',
                   n_intact_AM_AM='5', n_total_AM_AM='10', area_SE_SE_total_physics='9.9', **_frf([6, 3, 1, 1, 0]))
        q1_.update({'area_AM전체_SE_mean': '0.01', 'area_AM전체_SE_total': '0.4'})
        #  q2 bimodal (AM_P 1 · AM_S 10) — AM_P–AM_P 접촉 0 (개수 0 · 총합 0.0 · 평균 키 없음 = 웹앱 그대로) · 비관통 (eff_area_perc 없음)
        q2_.update(se_se_cn_aug='17.0', se_se_cn_aug_std='3.1', se_se_cn_aug_n_extra='50', se_se_cn_aug_h_spread_sim='1e-05',
                   area_SE_SE_mean='0.005', area_SE_SE_total='4.0', se_se_cn_eff_area=_eff(4.0),
                   area_AM_P_AM_P_n='0', area_AM_P_AM_P_total='0.0',
                   area_AM_P_AM_S_mean='0.04', area_AM_P_AM_S_total='0.2', area_AM_S_AM_S_mean=repr(0.46 / 17), area_AM_S_AM_S_total='0.46',
                   am_am_total_area='0.66', am_am_mean_area='0.03',
                   area_AM_P_SE_mean='0.012', area_AM_P_SE_total='0.36', area_AM_S_SE_mean='0.01', area_AM_S_SE_total='0.5',
                   **_frf([10, 6, 3, 2, 1]))
        q2_.update({'area_AM전체_SE_mean': repr(0.86 / 80), 'area_AM전체_SE_total': '0.86',
                    'frac_intact_force_AM_P-AM_S_pct': '40.0', 'n_intact_force_AM_P-AM_P': '0', 'n_total_force_AM_S-AM_S': '17'})
        return w
    _dq11 = [dict(r_, r_SE_um=repr(_R_SE)) for r_ in _dq7]
    _G567 = 'contact,percolation,f1,fracture,area'

    def _b11(w=None, hv=None, dq=None, groups=_G567):
        return build_handover(dq or _dq11, hv or _hq10(), webapp=w or _wa11(), webapp_groups=groups)
    try:
        _o11, _c11, _r11 = _b11()
        _e11 = ''
    except Exception as e:                                                # noqa: BLE001
        _o11, _c11, _r11, _e11 = [], [], {}, f'{type(e).__name__}: {e}'
    _m11 = next((r_ for r_ in _o11 if r_['case_id'] == 'q1'), {})
    _p11 = next((r_ for r_ in _o11 if r_['case_id'] == 'q2'), {})
    _new11 = (['se_se_cn_aug', 'se_se_cn_aug_std', 'se_se_cn_aug_n_extra', 'se_se_cn_aug_h_spread_sim', 'fracture_index_force',
               'n_total_AM_AM_force'] + [f'frac_{s_}_force_pct' for s_ in _ST] + [f'n_{s_}_force_AM_AM' for s_ in _ST]
              + ['se_se_cn_eff_area', 'se_se_cn_eff_area_perc', 'am_am_mean_area', 'am_am_total_area', 'area_SE_SE_mean', 'area_SE_SE_total',
                 'area_AM_P_SE_mean', 'area_AM_P_AM_P_total', 'area_AM전체_SE_total'])
    chk('㉕a ★ ⑤⑥⑦ 묶음 — F1 4 · 힘 기반 파괴 12 · 면적 (쌍별 평균 · 총합 · eff_area · AM–AM) 열이 실린다' + (f' — {_e11}' if _e11 else ''),
        not _e11 and all(c in _c11 for c in _new11))
    _excl11 = ('path_hop_area_mean', 'path_hop_area_min_mean', 'frac_intact_pct', 'fracture_index', 'n_intact_AM_AM', 'n_total_AM_AM',
               'frac_intact_force_AM_P-AM_S_pct', 'n_intact_force_AM_P-AM_P', 'n_total_force_AM_S-AM_S', 'area_SE_SE_total_physics')
    chk('㉕b ★ 명시 제외 — path_hop_area (LHS-32) · δ 판 · 상 쌍별 파괴 · physics 면적은 census ✅ 여도 안 실린다 · wa_excluded 가 사유를 준다',
        not _e11 and not any(c in _c11 for c in _excl11) and all(wa_excluded(c) for c in _excl11)
        and not any(wa_excluded(c) for c in _new11) and 'LHS-32' in (wa_excluded('path_hop_area_mean') or ''))
    try:
        _c11u = build_handover(_dq11, _hq10(), webapp=_wa11(), webapp_groups=_G567, wa_reviewed_only=False)[1]
    except Exception as e:                                                # noqa: BLE001
        _c11u = [f'ERR {type(e).__name__}: {e}']
    chk('㉕c 검토 목록 밖 경로 (wa_reviewed_only=False) 에서도 제외 열은 안 실린다 — 제외는 묶음 · 검토와 무관하게 먼저',
        not any(c in _c11u for c in _excl11) and 'se_se_cn_aug' in _c11u)
    chk('㉕d ★ mono (설계 AM_P · 웹앱 이름 AM_S) — 면적 상별 열은 설계 상 칸 · 없는 상 칸 빈칸 · AM전체 · SE–SE · F1 · 파괴 전체는 그대로',
        _m11.get('area_AM_P_AM_P_mean') == '0.02' and _m11.get('area_AM_P_AM_P_total') == '0.22' and _m11.get('area_AM_S_AM_S_total') == ''
        and _m11.get('area_AM_P_SE_total') == '0.4' and _m11.get('area_AM_P_AM_S_mean') == '' and _m11.get('area_AM전체_SE_total') == '0.4'
        and _m11.get('area_SE_SE_total') == '3.6' and _m11.get('se_se_cn_aug') == '19.0'
        and _m11.get('fracture_index_force') == repr(round(1 / 11, 4)))
    chk('㉕e ★ 접촉 0 쌍 (q2 AM_P–AM_P) — 개수 0 · 총합 0.0 (측정된 0) · 평균 빈칸 (N/A — 접촉 0 개에서 평균은 정의되지 않는다)',
        _p11.get('area_AM_P_AM_P_n') == '0' and _p11.get('area_AM_P_AM_P_total') == '0.0' and _p11.get('area_AM_P_AM_P_mean') == '')
    _w11z = _wa11()
    for _k in ('area_AM_P_AM_P_n', 'area_AM_P_AM_P_total'):
        _w11z['rows']['q2'].pop(_k, None)
    try:
        _p11z = next(r_ for r_ in _b11(w=_w11z)[0] if r_['case_id'] == 'q2')
        _e11z = ''
    except Exception as e:                                                # noqa: BLE001
        _p11z, _e11z = {}, f'{type(e).__name__}: {e}'
    chk('㉕f 옛 배치 (접촉 0 쌍 키 없음) — 두 상이 다 있으면 개수 0 · 총합 0.0 으로 채운다 (J20-h 와 같은 규칙) · 평균은 빈칸' + (f' — {_e11z}' if _e11z else ''),
        _p11z.get('area_AM_P_AM_P_n') == '0' and _p11z.get('area_AM_P_AM_P_total') == '0.0' and _p11z.get('area_AM_P_AM_P_mean') == '')
    chk('㉕g 관문 보고 — ⑤ · ⑥ · ⑦ 2 행씩 · 제외 열 수',
        _r11.get('wa_f1_checked') == 2 and _r11.get('wa_frac_checked') == 2 and _r11.get('wa_area_checked') == 2
        and _r11.get('wa_excluded_dropped', 0) >= len(_excl11))
    _dm11 = {d['column']: d for d in column_dictionary(_c11, webapp=_wa11())} if _c11 else {}
    _g11 = lambda c, k: (_dm11.get(c) or {}).get(k, '')                   # noqa: E731
    chk('㉕h ★ 열 사전 — F1 항등식 · 10 nm 출처 없는 상수 / 파괴 LHS-31 (마지막 프레임 · K_IC_P 0.3) · δ 판 금지 / 면적 A_dem_geometric · 총량 · '
        '접촉 0 쌍 평균 N/A · eff_area 식 · J20-s',
        '2 × se_se_cn_aug_n_extra' in _g11('se_se_cn_aug', 'meaning') and '10 nm' in _g11('se_se_cn_aug', 'caveat')
        and '출처 없는' in _g11('se_se_cn_aug', 'caveat') and 'LHS-31' in _g11('fracture_index_force', 'caveat')
        and '마지막 프레임' in _g11('fracture_index_force', 'caveat') and 'K_IC_P 0.3' in _g11('frac_microcrack_force_pct', 'caveat')
        and 'δ' in _g11('n_total_AM_AM_force', 'caveat') and 'A_dem_geometric' in _g11('area_SE_SE_total', 'caveat')
        and '총량' in _g11('area_SE_SE_total', 'caveat') and 'N/A' in _g11('area_AM_P_AM_P_mean', 'meaning')
        and '4π' in _g11('se_se_cn_eff_area', 'meaning') and 'J20-s' in _g11('se_se_cn_aug', 'meaning')
        and _g11('am_am_total_area', 'source') == 'webapp' and '설계 상 칸' in _g11('area_AM_P_SE_mean', 'meaning'))

    def _w11(q='q1', **kv):
        w = _wa11()
        w['rows'][q].update(kv)
        return w
    _neg7('㉕i ★ ⑤F1 — aug ≠ se_se_cn + 2 · n_extra / N_SE 이면 거부 (19.5)', lambda: _b11(w=_w11(se_se_cn_aug='19.5')), '⑤F1')
    _neg7('㉕j ★ ⑤F1 — done 행에 aug 가 비면 거부 (F1 이 꺼진 배치를 N/A 로 싣지 않는다)', lambda: _b11(w=_w11(se_se_cn_aug='')), '⑤F1')
    _neg7('㉕k ★ ⑥R1 — 단계 개수 합 ≠ n_total_AM_AM_force 이면 거부', lambda: _b11(w=_w11(n_intact_force_AM_AM='7')), '⑥R1')
    _neg7('㉕l ★ ⑥R2 — 비율이 100 · n/N 에서 반올림 폭 (0.005) 을 넘으면 거부 (+0.02)',
          lambda: _b11(w=_w11(frac_intact_force_pct=repr(round(600 / 11, 2) + 0.02))), '⑥R2')
    try:
        _b11(w=_w11(frac_intact_force_pct=repr(600 / 11)))
        _ok_r = True
    except Exception:                                                     # noqa: BLE001
        _ok_r = False
    chk('㉕m ⑥R2 — 반올림 안 한 값 (100 · 6/11 그대로) 도 받는다 · 기본 픽스처 = 웹앱처럼 둘째 자리 반올림 (㉕a 가 받는다)', _ok_r)
    _neg7('㉕n ★ ⑥R2 — fracture_index_force 가 (파편화 + 분쇄)/N 에서 반올림 폭 (5e-5) 을 넘으면 거부', lambda: _b11(w=_w11(fracture_index_force='0.0919')), '⑥R2')
    _neg7('㉕o ★ ⑥R3 — 힘 기반 전체 > am_am_n_contacts 이면 거부 (fn > 0 AM–AM 접촉 ⊂ 전 AM–AM 접촉)', lambda: _b11(w=_w11(**_frf([7, 3, 1, 1, 0]))), '⑥R3')
    _neg7('㉕p ★ ⑦A1 — 평균 × 개수 ≠ 총합 이면 거부 (SE–SE)', lambda: _b11(w=_w11(area_SE_SE_total='3.7', se_se_cn_eff_area=_eff(3.7))), '⑦A1')
    _neg7('㉕q ★ ⑦A1 — 접촉 0 쌍에 0 이 아닌 평균이 있으면 거부', lambda: _b11(w=_w11('q2', area_AM_P_AM_P_mean='0.01')), '⑦A1')
    _neg7('㉕r ★ ⑦A2 — AM전체–SE 총합 ≠ 상별 합 이면 거부',
          lambda: _b11(w=_w11('q2', **{'area_AM전체_SE_total': '0.9', 'area_AM전체_SE_mean': repr(0.9 / 80)})), '⑦A2')
    _neg7('㉕s ★ ⑦A3 — am_am_total_area ≠ AM–AM 쌍 총합 이면 거부', lambda: _b11(w=_w11('q2', am_am_total_area='0.7', am_am_mean_area=repr(0.7 / 22))), '⑦A3')
    _neg7('㉕t ★ ⑦A3 — am_am_mean_area ≠ am_am_total_area / am_am_n_contacts 이면 거부', lambda: _b11(w=_w11('q2', am_am_mean_area='0.031')), '⑦A3')
    _neg7('㉕u ★ ⑦A4 — se_se_cn_eff_area ≠ 2 · SE–SE 총합 / (N_SE · 4π r_SE²) 이면 거부', lambda: _b11(w=_w11(se_se_cn_eff_area='0.03')), '⑦A4')
    _neg7('㉕v ★ ⑦A4 — 설계에 r_SE_um 이 없으면 거부 (eff_area 를 잴 수 없다)', lambda: _b11(dq=_dq7), '⑦A4')
    _neg7('㉕w ★ ⑦A5 — 비관통 (percolation_pct 0) 인데 eff_area_perc 가 있으면 거부', lambda: _b11(w=_w11('q2', se_se_cn_eff_area_perc='0.01')), '⑦A5')
    _neg7('㉕x ★ ⑦A5 — 관통인데 eff_area_perc 가 비면 거부', lambda: _b11(w=_w11(se_se_cn_eff_area_perc='')), '⑦A5')
    try:
        _c11c = build_handover(_dq11, _hq10(), webapp=dict(_wa11(), stop_after='contact'), webapp_groups='f1,fracture,area')[1]
    except Exception as e:                                                # noqa: BLE001
        _c11c = [f'ERR {type(e).__name__}: {e}']
    chk('㉕y 접촉 단계 배치 (stop_after=contact) 도 f1 · fracture · area 를 받는다 (다 접촉 분석 단계 산출) · 그 묶음만 싣는다 (관문은 웹앱 원 행으로)',
        'se_se_cn_aug' in _c11c and 'fracture_index_force' in _c11c and 'area_SE_SE_mean' in _c11c
        and 'se_se_cn' not in _c11c and 'percolation_pct' not in _c11c)
    chk('㉕z 검토 기록 — 새 열 전부 1저자 검토 (J20-s) · 제외 열은 검토 목록에 없다',
        all(wa_reviewed(c) and 'J20-s' in (wa_review_note(c) or '') for c in _new11) and not any(wa_reviewed(c) for c in _excl11))
    print(f'\nlhs_design_dataset selftest: {ok}/{ok + len(fail)} PASS'
          + (f'   FAILED: {fail}' if fail else ''))
    return 1 if fail else 0


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--n', type=int, default=60, help='내부(바이모달) 블록 점 수')
    ap.add_argument('--n-end', type=int, default=10, help='단일모달 끝점 블록 각각의 점 수')
    ap.add_argument('--seed', type=int, default=0)
    ap.add_argument('--restarts', type=int, default=400, help='maximin 무작위 재시작')
    ap.add_argument('--continuous', action='store_true',
                    help='정수 격자를 끄고 연속 LHS (기본은 **정수 격자** — 2026-08-18 지시)')
    ap.add_argument('--as-radius', action='store_true',
                    help='지시 범위를 **반경**으로 해석 (기본은 직경 — docstring 근거)')
    ap.add_argument('--out', default='')
    ap.add_argument('--audit-descriptors', default='', metavar='CSV',
                    help='설계 CSV 의 **측정 열 채움 상태**를 보고한다 (`LHS-02`).  '
                         '결측이 있으면 rc=1 — 파이프라인이 그것을 0 으로 읽기 전에 선다.')
    ap.add_argument('--fill-descriptors', default='', metavar='DIR',
                    help='수확 JSON 디렉터리를 설계 CSV 에 **합친다** (`LHS-02`). '
                         '전단사가 아니거나 DESC-07 항등식이 깨지면 거부한다.')
    ap.add_argument('--design', default='', metavar='CSV',
                    help='--fill-descriptors 의 대상 설계 CSV (기본 = 동결 정본)')
    ap.add_argument('--fill-out', default='', metavar='CSV',
                    help='--fill-descriptors 산출 경로 (기본 = 제자리)')
    ap.add_argument('--export-handover', default='', metavar='CSV',
                    help='설계 CSV + 수확 JSON → **인계표**를 쓴다 (ML 담당에게 넘길 표).  '
                         '⛔ τ 값 열은 넣지 않는다 (`LHS-08` 열림) — 대신 왜 없는지를 진단 열로 '
                         '넘긴다.  status != OK 는 빈칸이고 0 이 아니다.')
    ap.add_argument('--harvest', default='', metavar='DIR',
                    help='--export-handover 가 읽을 수확 JSON 디렉터리 '
                         '(기본 = DESCRIPTOR_FILL_EXPECTED["source"] 의 경로)')
    ap.add_argument('--union', default=None, metavar='TSV',
                    help='(--export-handover) J19 union TSV (scripts/lhs_union_webapp.py 산출) — 겹침 보정 porosity · 질량 보존 두께 · '
                         f'SE-rich 표지를 **병기**한다 (기본 {DEFAULT_UNION_TSV} · 빈 문자열이면 옛 인계표).  짝이 안 맞으면 거부')
    ap.add_argument('--webapp', default='', metavar='DIR',
                    help='(--export-handover) J20 웹앱 배치 산출 (scripts/lhs_webapp_batch.py 의 --out-dir) — 전수 판정 ✅ 열을 싣는다.  '
                         '설계행 전부를 배치가 시도했어야 하고 웹앱 porosity = 수확 porosity (같은 프레임) 여야 한다')
    ap.add_argument('--webapp-groups', default=None, metavar='G[,G]',
                    help='(--export-handover --webapp) 웹앱 열을 이 묶음만 싣는다 (쉼표로 여럿) — contact = ① 접촉 위상 · percolation = ② '
                         '퍼콜레이션 · f1 = ⑤ F1 근접쌍 · fracture = ⑥ Auerbach 힘 기반 · area = ⑦ 접촉 면적 (전부 접촉 분석 단계 산출 · J20-s).  '
                         '`lhs_webapp_batch --stop-after contact|coverage` 산출은 이것 없이는 거부된다')
    ap.add_argument('--census', default='', metavar='TSV',
                    help=f'(--webapp) 전수 판정 census (기본 {DEFAULT_CENSUS_TSV})')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        raise SystemExit(_selftest())
    if a.audit_descriptors:
        _p = pathlib.Path(a.audit_descriptors)
        _rows = list(csv.DictReader(_p.open(encoding='utf-8-sig')))
        _fill = descriptor_fill(_rows)
        print(f'{_p}   {len(_rows)} 행')
        for _c in DESCRIPTORS:
            _n = _fill[_c]
            print(f'  {"✓" if _n == len(_rows) else "⚠"} {_c:34s} {_n:>4} / {len(_rows)} 채움')
        _miss = [c for c in DESCRIPTORS if _fill[c] < len(_rows)]
        if _miss:
            print(f'\n⛔ 측정 열 {len(_miss)}/{len(DESCRIPTORS)} 이 불완전하다 — '
                  f'**결측을 0 으로 채우지 말 것** (원장 LHS-02 · GAP2-05).')
            _why = DESCRIPTOR_FILL_EXPECTED.get('why_partial', {})
            for _c2 in _miss:
                if _c2 in _why:
                    print(f'   · {_c2}: {_why[_c2]}')
            #  ⚠ 사유가 **등록되지 않은** 결측만 "수확기를 돌려라" 가 답이다.  없는 상
            #    (`N_A_PHASE_ABSENT`)은 아무리 돌려도 안 채워진다 — 그 줄을 무차별로
            #    찍으면 "돌리면 채워진다" 는 **틀린 처방**이 된다.
            _un = [c for c in _miss if c not in _why]
            if _un:
                print(f'   채우려면 ({", ".join(_un)}): '
                      f'{DESCRIPTOR_FILL_EXPECTED["harvester"]}')
            else:
                print('   ⇒ 남은 결측은 **전부 사유가 등록돼 있다**.  숫자로 채우는 것이 '
                      '답이 아니다 — 옆의 `<열>_status` 를 읽을 것.')
        else:
            print('\n✓ 측정 열이 전부 찼다.')
        raise SystemExit(1 if _miss else 0)

    if a.export_handover:
        _root = pathlib.Path(__file__).resolve().parent.parent
        _dp = pathlib.Path(a.design or DESCRIPTOR_FILL_EXPECTED['path'])
        if not _dp.is_absolute():
            _dp = _root / _dp
        _hd = pathlib.Path(a.harvest or (_root / DEFAULT_HARVEST_DIR))
        with _dp.open(encoding='utf-8-sig') as _fh:
            _rows = list(csv.DictReader(_fh))
        _harv = load_harvest(_hd)
        _un = DEFAULT_UNION_TSV if a.union is None else a.union
        _uv = None
        if _un:
            _upth = pathlib.Path(_un)
            _uv = load_union(_upth if _upth.is_absolute() else _root / _upth)
        _wv = None
        if a.webapp:
            _wp = pathlib.Path(a.webapp)
            _wv = load_webapp(_wp if _wp.is_absolute() else _root / _wp, a.census or None)
        _out, _cols, _rep = build_handover(_rows, _harv, union=_uv, webapp=_wv, webapp_groups=a.webapp_groups)
        _op = pathlib.Path(a.export_handover)
        if not _op.is_absolute():
            _op = _root / _op
        with _op.open('w', encoding='utf-8', newline='') as _fh:
            _w = csv.DictWriter(_fh, _cols, lineterminator='\n')
            _w.writeheader()
            for _r in _out:
                _w.writerow(_r)
        #  열 사전 — 받는 쪽이 열마다 출처 · 판정 · 뜻 · 주의를 읽는다 (J20)
        _dp2 = _op.with_name(_op.stem + '_columns.tsv')
        with _dp2.open('w', encoding='utf-8', newline='') as _fh:
            _w = csv.DictWriter(_fh, ['column', 'source', 'verdict', 'meaning', 'caveat'], delimiter='\t', lineterminator='\n')
            _w.writeheader()
            for _d in column_dictionary(_cols, webapp=_wv):
                _w.writerow(_d)
        print(f'→ {_op}   {_rep["n"]}행 × {len(_cols)}열   (열 사전 {_dp2.name})')
        if 'tau_wall_status' in _rep:
            print(f'   J20 벽 τ: {dict(_rep["tau_wall_status"])}')
        if _wv is not None:
            print(f'   J20 웹앱 ✅ {_rep["wa_n_cols"]} 열 · 행 상태 {dict(_rep["wa_status_counts"])} · '
                  f'같은 프레임 |Δporosity| 최대 {_rep["wa_porosity_absmax"]:.3e} %p · 이름 충돌 (수확 열 정본) {_rep["wa_collisions"]}')
            print(f'   J20-g 같이 확인한 웹앱 열만 ({len(WA_REVIEWED)} 패턴) — 뺀 census ✅ 열 {_rep["wa_unreviewed_dropped"]} · '
                  f'J20-k (B) mono 웹앱 상별 칸: 설계 상 칸 채움 {_rep["wa_mono_design_filled"]} 셀 · 이름 옮김 {_rep["wa_mono_renamed_cases"]} 건 · '
                  f'없는 상 빈칸 {_rep["wa_mono_absent_blanked"]} 셀 · J20-h 접촉 0 쌍 = 0 채움 {_rep["wa_pair_zero_filled"]} · '
                  f'J20-i se_se_cn = 2·area_SE_SE_n/N_SE 확인 {_rep["wa_cn_identity_checked"]} 행 · '
                  f'J20-j AM–AM 접촉 수 = 쌍 합 · am_am_cn = 2·n/N_AM 확인 {_rep["wa_am_identity_checked"]} 행 · '
                  f'7c AM–SE CN · 고립 관문 G1–G7 확인 {_rep["wa_amse_identity_checked"]} 행 · '
                  f'② 퍼콜레이션 관문 P1–P3 확인 {_rep["wa_perc_checked"]} 행')
        if 'tau_wall_checked' in _rep:
            print(f'   벽 τ 관문 T1–T2 확인 {_rep["tau_wall_checked"]} 행 · T3 (↔ 퍼콜레이션) {_rep["tau_perc_crosschecked"]} 행')
        if _rep.get('wa_ionic_checked'):
            print(f'   v1.1 ①② 이온 활성 · 경로 기준 고립 관문 D1–D5 확인 {_rep["wa_ionic_checked"]} 행')
        if 'se_cluster_checked' in _rep:
            print(f'   v1.1 ③ 가장 큰 SE 덩어리 관문 C1–C3 확인 {_rep["se_cluster_checked"]} 행')
        print(f'   J20-k (B) mono {_rep["mono_rows"]} 행 — 수확기 상별 칸 (coverage · n_AM_*_measured · cov_*_n_valid · 벽 접촉) 설계 상 칸 채움 '
              f'{_rep["mono_harvest_filled"]} 셀 (설계에 없는 상은 빈칸)')
        print(f'   빈칸 사유: {dict(_rep["blank_by_status"])}')
        for _k, _v in _rep['held_back'].items():
            print(f'   ⛔ 보류 열 `{_k}` — {_v}')
        if _uv is not None:
            print(f'   J19 union 병기: {_un} · 설계 밖 union 행 {_rep.get("union_extra")} (인계표에 안 넣음) · '
                  f'SE-rich (≥ {SE_RICH_MIN}) {sum(r["se_rich"] == "True" for r in _out)} 행 · 구 부피 합 열은 그대로')
        raise SystemExit(0)

    if a.fill_descriptors:
        _root = pathlib.Path(__file__).resolve().parent.parent
        _dp = pathlib.Path(a.design or DESCRIPTOR_FILL_EXPECTED['path'])
        if not _dp.is_absolute():
            _dp = _root / _dp
        with _dp.open(encoding='utf-8-sig') as _fh:
            _rd = csv.DictReader(_fh)
            _base_cols = list(_rd.fieldnames or [])
            _rows = list(_rd)
        _harv = load_harvest(a.fill_descriptors)
        _rows, _rep = fill_descriptors(_rows, _harv)
        #  `<열>` 바로 뒤에 `<열>_status` 를 끼운다 (값과 사유가 떨어지면 안 읽힌다)
        _cols = []
        for _c in _base_cols:
            _cols.append(_c)
            if _c in DESCRIPTORS:
                _cols.append(_c + '_status')
        for _c in DESCRIPTORS:                       # 원래 CSV 에 없던 열이면 뒤에 붙인다
            if _c not in _cols:
                _cols += [_c, _c + '_status']
        _op = pathlib.Path(a.fill_out) if a.fill_out else _dp
        #  ⚠ `csv` 의 기본 줄끝은 CRLF 다 — 그냥 쓰면 LF 파일 전체가 바뀌어 diff 가
        #    131/131 이 되고 실제 변경이 묻힌다 (한 번 그렇게 했다).  리포 관행은 LF.
        with _op.open('w', newline='', encoding='utf-8') as _fh:
            _w = csv.DictWriter(_fh, _cols, lineterminator='\n')
            _w.writeheader()
            for _r in _rows:
                _w.writerow({_c: _r.get(_c, '') for _c in _cols})
        _mp = _op.with_name(_op.stem + '_descriptor_manifest.json')
        _mp.write_text(json.dumps({
            'design_csv': str(_op.relative_to(_root)) if _op.is_relative_to(_root) else str(_op),
            'harvest_dir': str(a.fill_descriptors), 'n_rows': _rep['n_rows'],
            'filled': _rep['filled'], 'status_tally': _rep['status_tally'],
            'derived_not_independent_targets': _rep['derived'],
            'desc07_identity_max_err': _rep['desc07_max_err'],
            'contract': ('DESC-07 유도열 표시 · DESC-08 291 코퍼스와 병합 안 함 · '
                         'DESC-09 전단사 아니면 거부 · GAP2-05 status≠OK 면 숫자 안 씀'),
            'caveats': [
                ('tortuosity_dijkstra_SE_status 는 **잠정**이다 (원장 `LHS-08`, 열림). '
                 '`NOT_PERCOLATING` 은 아직 결론이 아니라 의심 신호이고, 전극 밴드 규약이 '
                 '재측정·판단 대기다.  그 status 를 "미관통이 확인됐다" 로 읽지 말 것.'),
                ('`DESC-07`: ' + ' · '.join(DERIVED_DESCRIPTORS) + ' 는 나머지에서 **유도**된다 '
                 '(이 병합에서 항등식을 다시 쟀다).  일곱을 독립 회귀 타깃으로 세지 말 것.'),
                ('`DESC-08`: 이 표를 291 행 `design_performance` 코퍼스와 **그대로 합치지 말 것** '
                 '— 그쪽은 d_am=0 40건과 MPM/DEM 상태 혼합이 남아 있다.'),
                ('빈 칸은 결측이고 **0 이 아니다**.  읽기 전에 `require_descriptors` 를 부를 것.'),
            ],
            'per_case': _rep['sources'],
        }, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
        print(f'{_op}   {_rep["n_rows"]} 행')
        for _c in DESCRIPTORS:
            _n = _rep['filled'][_c]
            _mark = '✓' if _n == _rep['n_rows'] else '·'
            _tl = ' · '.join(f'{k} {v}' for k, v in sorted(_rep['status_tally'][_c].items()))
            _der = '  [DESC-07 유도]' if _c in DERIVED_DESCRIPTORS else ''
            print(f'  {_mark} {_c:34s} {_n:>4}/{_rep["n_rows"]}   {_tl}{_der}')
        _e = _rep['desc07_max_err']
        print(f'\nDESC-07 항등식 재검증: ① porosity 최대오차 {_e["porosity"]:.3e} · '
              f'② C_total 가중평균 최대오차 {_e["coverage_total"]:.3e} '
              f'({_e["n_coverage_checked"]} 건; mono 는 정의상 제외)')
        print(f'→ 프로비넌스 {_mp}')
        print('⚠ 채워지지 않은 칸은 **빈 칸 + 사유 열**이다.  0 으로 읽지 말 것 '
              '(원장 LHS-02 · GAP2-05).')
        raise SystemExit(0)

    rows = build(a.n, a.n_end, a.seed, a.restarts, grid=not a.continuous)
    if a.as_radius:                                   # 범위를 반경으로 읽으면 직경이 2배
        for r in rows:
            for d, rr in (('d_am_p_um', 'r_AM_P_um'), ('d_am_s_um', 'r_AM_S_um'),
                          ('d_se_um', 'r_SE_um'), ('d_am_max_um', None)):
                if rr:
                    r[rr] = r[d]
                r[d] = r[d] * 2.0
    cols = (['case_id', 'block', 'd_am_p_um', 'd_am_s_um', 'ps_frac', 'ps_label', 'd_se_um',
             'am_pct', 'rve_um', 'loading_mAh_cm2', 'pressure_MPa', 'e_se_gpa',
             'thickness_est_um', 'phi_am_est', 'phi_se_est', 'se_percolation_est_meanfield',
             'd_am_max_um', 'sv_inv_um', 'r_AM_P_um', 'r_AM_S_um', 'r_SE_um',
             'size_ratio_P_over_S', 'size_ratio_AM_over_SE',
             'n_am_p_est', 'n_am_s_est', 'n_se_est', 'n_total_est',
             'rve_min_um', 'rve_recommended_um',
             'rve_over_d_am_max', 'thick_over_d_am_max', 'finite_size_flag',
             'se_perc_est_flag'] + DESCRIPTORS)
    for r in rows:
        for d in DESCRIPTORS:
            r.setdefault(d, '')                       # DEM 이 채울 빈 칸

    def fmt(v):
        return '' if v == '' else ('' if isinstance(v, float) and np.isnan(v)
                                   else (f'{v:.4f}' if isinstance(v, float) else v))
    if a.out:
        with open(a.out, 'w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, cols)
            w.writeheader()
            for r in rows:
                w.writerow({c: fmt(r.get(c, '')) for c in cols})
        print(f'→ {a.out}   ({len(rows)} 행)')

    print(f"\n{'case_id':13s} {'block':10s} {'d_AM_P':>7} {'d_AM_S':>7} {'P:S':>6} "
          f"{'d_SE':>6} {'AM%':>6} {'P/S':>6}")
    for r in rows[:8] + [{'case_id': '…'}] + rows[-4:]:
        if r.get('case_id') == '…':
            print('   …')
            continue
        f_ = lambda v: '   —  ' if (isinstance(v, float) and np.isnan(v)) else f'{v:6.2f}'
        print(f"{r['case_id']:13s} {r['block']:10s} {f_(r['d_am_p_um']):>7} "
              f"{f_(r['d_am_s_um']):>7} {r['ps_frac']:>6.2f} {r['d_se_um']:>6.2f} "
              f"{r['am_pct']:>6.1f} {f_(r['size_ratio_P_over_S']):>6}")
    print('\n설계 진단 (내부 블록):', json.dumps(diagnostics(rows), ensure_ascii=False))
    fl = [r for r in rows if r['finite_size_flag']]
    print(f"\n고정 상수: RVE {FIXED['rve_um']:.0f}×{FIXED['rve_um']:.0f} µm · 면용량 "
          f"{FIXED['loading_mAh_cm2']:.1f} mAh/cm² → 두께 ≈ {rows[0]['thickness_est_um']:.0f} µm "
          f"(코퍼스 291건 회귀 {THICK_PER_LOADING_UM:.2f} µm per mAh/cm²)")
    print(f"  측면 RVE/d_AM_max : {min(r['rve_over_d_am_max'] for r in rows):.2f} – "
          f"{max(r['rve_over_d_am_max'] for r in rows):.2f}   "
          f"(코퍼스 최빈 rve50/d12 = 4.17 · rve40/d12 = 3.33)")
    print(f"  두께 /d_AM_max    : {min(r['thick_over_d_am_max'] for r in rows):.2f} – "
          f"{max(r['thick_over_d_am_max'] for r in rows):.2f}")
    import collections as _c
    cnt = _c.Counter(t for r in rows for t in (r['finite_size_flag'].split('+') if
                                               r['finite_size_flag'] else []))
    print(f"\n  ⚠ 유한크기 플래그 {len(fl)}/{len(rows)} 행 — 내역:")
    _why = {'lateral': '측면 상자 < 3.3 입자',
            'thin': '두께 < 3 입자',
            'n_am_p_low': 'N_AM_P 10–30 (coverage_AM_P 표집오차 큼)',
            'n_am_p_CRIT': '★ N_AM_P < 10 — coverage_AM_P·명목 ps 가 **실현 불가**'}
    for k, v in cnt.most_common():
        print(f"      {k:14s} {v:>3} 행   {_why.get(k, '')}")
    #  ★ SE 퍼콜 추정은 **자기 열**에서 보고한다 (`LHS-01`) — 기하 플래그와 섞지 않는다.
    sc = _c.Counter(r['se_perc_est_flag'] for r in rows if r['se_perc_est_flag'])
    _m = LHS_PERC_MEASURED
    print(f"\n  ⚠ SE 퍼콜 **추정** 플래그 (`se_perc_est_flag`, 기하와 분리) — "
          f"{sum(sc.values())}/{len(rows)} 행:")
    _swhy = {'se_marginal': f'φ_SE 가 φc 바로 위 ({PHI_C_SE}–0.20)',
             'se_BELOW_phic': f'φ_SE < {PHI_C_SE} — 평균장 문턱 아래 (am_pct > 88.8 wt%)'}
    for k, v in sc.most_common():
        print(f"      {k:14s} {v:>3} 행   {_swhy.get(k, '')}")
    print(f"      ★ 실측 운용특성 (n={_m['n_measured']}, {_m['channel']} 채널): "
          f"OK {_m['OK']['n']}행 중 막힘 {_m['OK']['blocked']} · "
          f"BELOW_phic {_m['BELOW_phic']['n']}행 중 막힘 {_m['BELOW_phic']['blocked']} "
          f"⇒ 재현율 {_m['recall_pct']} % · 정밀도 {_m['precision_pct']} %")
    print(f"      ⛔ **선별기이지 필터가 아니다** — `BELOW_phic` 를 버리면 실제로 뚫리는 "
          f"{_m['BELOW_phic']['n'] - _m['BELOW_phic']['blocked']}건을 같이 버린다.  "
          f"출처: {_m['source']}")
    _np = [r['n_am_p_est'] for r in rows if r['n_am_p_est'] == r['n_am_p_est']]
    print(f"  입자 수 추정: N_AM_P 최소 {min(_np):.1f} · 중앙 {sorted(_np)[len(_np)//2]:.0f} | "
          f"총 입자 최대 {max(r['n_total_est'] for r in rows):,.0f}")
    over = [r for r in rows if r['n_total_est'] > N_TOTAL_CAP]
    print(f"  ★ 입자수 상한 {N_TOTAL_CAP:,} — 초과 행 **{len(over)}** 개 "
          f"(최대 {max(r['n_total_est'] for r in rows):,.0f})")
    _big = [r for r in rows if r['rve_recommended_um'] > FIXED['rve_um'] + 1e-9]
    if _big:
        print(f"  ★ N_AM_P ≥ {N_AM_P_MIN} 를 만족하려면 {len(_big)} 행이 더 큰 상자를 요구한다 "
              f"(권장 rve 최대 {max(r['rve_recommended_um'] for r in _big):.0f} µm).  "
              f"`rve_recommended_um` 열 참조 — **결정은 사람이 한다** (예산 문제다).")
    print("  ⚠ 플래그는 **거부가 아니라 라벨**이다.  학습 시 공변량으로 남기면 "
          "유한크기 효과를 흡수한다 — 단 `n_am_p_CRIT` 와 `se_BELOW_phic` 는 "
          "**타깃 자체가 안 나올 수 있는** 행이라 성격이 다르다.")
    print("  ★ 그리고 그 둘은 **성격이 서로 다르다**: `n_am_p_CRIT` 는 기하로 확정이지만 "
          f"`se_BELOW_phic` 는 추정이고 실측에서 {_m['BELOW_phic']['n']}건 중 "
          f"{_m['BELOW_phic']['n'] - _m['BELOW_phic']['blocked']}건이 **실제로는 뚫렸다**.")
    print('\n⚠ 디스크립터 열은 **비어 있다** — DEM 이 채운다: ' + ', '.join(DESCRIPTORS))
    sys.stdout.flush()
