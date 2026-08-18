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
import csv
import json
import sys

import numpy as np

#  범위 = 사용자 지정 (2026-08-18).  직경 µm / wt% / 무차원.
RANGES = {
    'd_am_p_um': (5.0, 15.0),      # 대립 (poly NCM 2차입자)
    'd_am_s_um': (1.0, 5.0),       # 소립 (single-crystal)
    'ps_frac':   (0.0, 1.0),       # 바이모달 비율 = AM_P 몫 (0 = 소립만, 1 = 대립만)
    'd_se_um':   (0.5, 2.0),       # 전해질
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


#  ── 고정 상수 (인자가 아니다 — 2026-08-18 지시) ──────────────────────────────────
#    면용량 2 mAh/cm² = wall effect 가 거의 안 나오는 최소 단위 · RVE 50×50 µm.
#    ★ 인자에서 빼는 것이 이득이다: 기존 ML 설계층은 `rve` 와 `loading` 을 **자유 노브**로
#      두는데(ml_design_structure.FREE_KNOBS), 그 둘을 고정하면 5 인자에 예산을 다 쓴다.
FIXED = {'rve_um': 50.0, 'loading_mAh_cm2': 2.0}
#  두께는 로딩의 함수다 — 코퍼스 291건 원점회귀 (3σ 제거 후) **19.64 µm per mAh/cm²**
#  ⇒ 면용량 2.0 → 두께 ≈ 39 µm.  DEM 이 실제 두께를 낼 것이고 이 값은 **사전 점검용**이다.
THICK_PER_LOADING_UM = 19.64


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


def build(n_interior=60, n_end=10, seed=0, restarts=400, grid=True):
    rng = np.random.default_rng(seed)
    rows = []

    # ── 블록 A: 내부(양상 공존) 5-인자 ────────────────────────────────────────
    if grid:
        LV = [levels_of(f, PS_INTERIOR) for f in FACTORS]
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
            IB = lhs_grid(n_end, LVb, rng, restarts)
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
        #  기존 ML 설계층은 AM 크기 노브가 **하나**(`d_am`)다 → ps 가중 평균으로 하위호환 열을
        #  같이 낸다.  ⚠ 이것은 요약이고, 새 데이터셋의 정본은 d_am_p/d_am_s **두 열**이다.
        if np.isnan(dP):
            r['d_am_um'] = dS
        elif np.isnan(dS):
            r['d_am_um'] = dP
        else:
            r['d_am_um'] = (1.0 - p) * dS + p * dP
        for src, dst in (('d_am_p_um', 'r_AM_P_um'), ('d_am_s_um', 'r_AM_S_um'),
                         ('d_se_um', 'r_SE_um')):
            r[dst] = r[src] / 2.0                       # ← LIGGGHTS 입력은 **반경**
        r['ps_label'] = (f'{round(p * 10):d}:{10 - round(p * 10):d}')   # 7:3 식 표기
        #  ★ 정수 격자(ps 눈금 0.1)에서는 이 라벨이 **반올림이 아니라 정확**하다
        r['size_ratio_P_over_S'] = (dP / dS) if (dP == dP and dS == dS) else float('nan')
        r['size_ratio_AM_over_SE'] = r['d_am_um'] / r['d_se_um']
        #  ── 고정 상수와 그로부터 나오는 유한크기 점검 ────────────────────────────
        r.update(FIXED)
        r['thickness_est_um'] = FIXED['loading_mAh_cm2'] * THICK_PER_LOADING_UM
        dmax = r['d_am_um'] if np.isnan(dP) else dP          # 가장 큰 입자가 상자를 정한다
        r['rve_over_d_am_max'] = FIXED['rve_um'] / dmax           # 측면 상자 / 최대 입자
        r['thick_over_d_am_max'] = r['thickness_est_um'] / dmax   # 두께 / 최대 입자
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
        r['finite_size_flag'] = '+'.join(f)
    return rows


DESCRIPTORS = ['porosity_pct', 'coverage_AM_P_pct', 'coverage_AM_S_pct',
               'coverage_AM_total_pct', 'tortuosity']


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
    chk('⑩b 수준 점유가 균형이다 (최대−최소 ≤ 1)',
        all(int(v.split('점유 ')[1].split('–')[1]) - int(v.split('점유 ')[1].split('–')[0]) <= 1
            for v in dgg['levels'].values()))
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
    #  ⑪ 연속 모드도 여전히 된다 (되돌릴 길을 남긴다)
    c = build(20, 4, 0, 40, grid=False)
    chk('⑪ --continuous 경로 보존 (눈금 밖 값이 나온다)',
        any(not onstep(r['d_am_p_um'], 1.0) for r in c if not np.isnan(r['d_am_p_um'])))
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
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        raise SystemExit(_selftest())

    rows = build(a.n, a.n_end, a.seed, a.restarts, grid=not a.continuous)
    if a.as_radius:                                   # 범위를 반경으로 읽으면 직경이 2배
        for r in rows:
            for d, rr in (('d_am_p_um', 'r_AM_P_um'), ('d_am_s_um', 'r_AM_S_um'),
                          ('d_se_um', 'r_SE_um'), ('d_am_um', None)):
                if rr:
                    r[rr] = r[d]
                r[d] = r[d] * 2.0
    cols = (['case_id', 'block', 'd_am_p_um', 'd_am_s_um', 'ps_frac', 'ps_label', 'd_se_um',
             'am_pct', 'rve_um', 'loading_mAh_cm2', 'thickness_est_um',
             'd_am_um', 'r_AM_P_um', 'r_AM_S_um', 'r_SE_um',
             'size_ratio_P_over_S', 'size_ratio_AM_over_SE',
             'rve_over_d_am_max', 'thick_over_d_am_max', 'finite_size_flag'] + DESCRIPTORS)
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
    print(f"  ⚠ 유한크기 플래그 {len(fl)}/{len(rows)} 행 — **거부가 아니라 라벨**이다 "
          f"(Ø15 µm 입자에 39 µm 전극이면 실제로 2.6층이다).  "
          f"학습 시 이 열을 공변량으로 남겨 두면 유한크기 효과를 흡수할 수 있다.")
    print('\n⚠ 디스크립터 열은 **비어 있다** — DEM 이 채운다: ' + ', '.join(DESCRIPTORS))
    sys.stdout.flush()
