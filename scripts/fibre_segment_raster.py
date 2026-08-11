#!/usr/bin/env python3
"""섬유를 **선분(segment)** 으로 복셀에 굽는다 — 6-face 연결이 **보장**되는 래스터.

왜 (SR-01, 2026-08-11):
  현행 STEP3 는 첨가제를 **점**으로 스탬프한다 (`step3_sigma.rasterize()`).  그런데 점 간격이
  MPM dx 에 묶여 σ-격자와 무관하게 고정돼 있어, 선이 복셀 경계를 비스듬히 지나면 연속한 두
  점이 **face 를 공유하지 않는 대각 셀**에 찍힌다.  실측: vox 0.4 에서 10 µm 직선 섬유의
  **95.7 % 가 평균 4.9 조각**으로 끊긴다.  솔버는 6-face conductance 를 쓰므로 그 조각들은
  **전기적으로 분리**된다 — STEP3 σ_e 의 "VGCF 퍼콜 망" 을 절대 해석할 수 없는 이유다.

  ★ 점 재샘플링으로는 못 고친다 (Codex CR-01 + 자체 재현):
      step 0.35·vox → 97.5 % 단절 · 0.05·vox → 51.8 % · **0.02·vox → 30.7 %**
    대각 셀은 얼마나 촘촘히 찍든 face 를 공유하지 않기 때문이다.
  ★ 26-connectivity 로 라벨만 바꾸는 것도 답이 아니다 — 라벨 지표와 transport 그래프가
    어긋난다 (솔버는 6-face).

무엇을 하나:
  Amanatides–Woo 복셀 순회로 **선분이 실제로 지나는 셀을 순서대로** 방문한다.  이 순회는
  **한 번에 한 축만** 전진하므로 연속한 두 셀이 **항상 face 를 공유**한다 = 연결이 구성상 보장.
  (edge/corner 를 정확히 지나는 퇴화 케이스는 축 우선순위를 고정해 하나씩 전진 — 그래서
   여전히 face-연결이다.  기하적으로는 corner 를 "자르는" 셈이지만 전기적으로는 옳은 쪽:
   실제 섬유는 유한 직경이라 그 셀들을 실제로 채운다.)

무엇을 **하지 않나** (정직):
  · 직경을 부피분율로 반영하지 않는다 — 이 v1 은 **연결성 문제만** 푼다.  단면적은 여전히
    복셀 1개로 양자화되고, 그 인플레(⌀150 nm @vox 0.4 → 9.1×)는 **그대로 남는다**.
    직경-aware conductance 는 **아직 없다** (v2 과제).  이 v1 을 σ 절대값에 쓰지 말 것.
  · 이것을 production STEP3 에 배선하지 않는다.  A/B 측정용 프로토타입이다.

사용:
    python3 scripts/fibre_segment_raster.py --selftest
    python3 scripts/fibre_segment_raster.py --ab --vox 0.4 --n-fib 300
"""
from __future__ import annotations

import argparse
import math
import sys

import numpy as np


def segment_cells(p0, p1, vox, eps=1e-12):
    """선분 p0→p1 이 지나는 복셀 인덱스를 **순서대로** → (N,3) int64.

    Amanatides–Woo.  연속한 두 셀은 **한 축만** 다르므로 6-face 인접이 보장된다.
    """
    p0 = np.asarray(p0, np.float64)
    p1 = np.asarray(p1, np.float64)
    d = p1 - p0
    L = float(np.linalg.norm(d))
    cur = np.floor(p0 / vox).astype(np.int64)
    if L < eps:
        return cur[None, :]
    u = d / L
    step = np.where(u > 0, 1, -1).astype(np.int64)
    out = [cur.copy()]
    tmax = np.empty(3)
    tdel = np.empty(3)
    for a in range(3):
        if abs(u[a]) < eps:
            tmax[a] = math.inf
            tdel[a] = math.inf
        else:
            # 다음 경계까지의 파라미터 거리
            nxt = (cur[a] + (1 if step[a] > 0 else 0)) * vox
            tmax[a] = (nxt - p0[a]) / u[a]
            tdel[a] = vox / abs(u[a])
    guard = 0
    guard_max = int(4 * (L / vox + 3)) + 16
    while True:
        a = int(np.argmin(tmax))          # 동률이면 낮은 축부터 = 한 번에 한 축만 전진
        if tmax[a] > L or guard > guard_max:
            break
        cur = cur.copy()
        cur[a] += step[a]
        out.append(cur)
        tmax[a] += tdel[a]
        guard += 1
    # ★ 끝점 셀 보장 (2026-08-11 디버깅): 끝점이 복셀 경계에 **정확히** 놓이면
    #   (예 5.2 = 13×0.4) 마지막 경계 통과의 tmax 가 부동소수에서 L 을 아주 살짝 넘어
    #   잘린다 → floor(p1) 셀이 빠진다.  일반 끝점은 루프가 이미 포함하지만, 계약을
    #   "p1 을 담는 셀은 **항상** 방문" 으로 못박는다.  한 축씩 걸어가므로 face-연결 유지.
    endc = np.floor(p1 / vox).astype(np.int64)
    while not np.array_equal(cur, endc):
        diff = endc - cur
        nz = np.nonzero(diff)[0]
        if not len(nz) or guard > guard_max + 8:
            break
        a = int(nz[0])
        cur = cur.copy()
        cur[a] += 1 if diff[a] > 0 else -1
        out.append(cur)
        guard += 1
    return np.asarray(out, np.int64)


def polyline_cells(pts, vox):
    """폴리라인(점열)의 셀 순회 — 인접 선분을 이어 붙인다 (중복 제거, 순서 보존)."""
    pts = np.asarray(pts, np.float64)
    if len(pts) < 2:
        return np.floor(pts / vox).astype(np.int64)
    chunks = [segment_cells(pts[i], pts[i + 1], vox) for i in range(len(pts) - 1)]
    allc = np.vstack(chunks)
    keep = np.ones(len(allc), bool)
    keep[1:] = np.any(allc[1:] != allc[:-1], axis=1)      # 연속 중복만 제거
    return allc[keep]


def point_cells(pts, vox):
    """현행 STEP3 규약 — 점을 각각 floor 스탬프 (비교군)."""
    return np.unique(np.floor(np.asarray(pts, np.float64) / vox).astype(np.int64), axis=0)


def n_components_6face(cells):
    """셀 집합의 6-face 연결성분 수 (솔버와 같은 인접 규약)."""
    S = {tuple(int(v) for v in c) for c in np.atleast_2d(cells)}
    seen, n = set(), 0
    for c in S:
        if c in seen:
            continue
        n += 1
        stack = [c]
        seen.add(c)
        while stack:
            x, y, z = stack.pop()
            for dd in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)):
                q = (x + dd[0], y + dd[1], z + dd[2])
                if q in S and q not in seen:
                    seen.add(q)
                    stack.append(q)
    return n


def _straight_fibre(rng, L, box):
    d = rng.normal(size=3)
    d /= np.linalg.norm(d)
    p0 = rng.uniform(0.15 * box, 0.85 * box, 3)
    return p0, p0 + L * d


def ab_compare(vox=0.4, n_fib=300, L=10.0, box=20.0, mpm_dx=0.141, seed=0):
    """점-스탬프 vs 선분-스탬프 A/B → dict.  현행 점 간격 = 0.7·dx_MPM."""
    rng = np.random.default_rng(seed)
    step = 0.7 * mpm_dx
    npt = max(2, int(L / step) + 1)
    t = np.arange(npt) * step
    pt_comp, sg_comp, pt_cells, sg_cells = [], [], [], []
    for _ in range(n_fib):
        p0, p1 = _straight_fibre(rng, L, box)
        u = (p1 - p0) / L
        pts = p0 + t[:, None] * u
        pc = point_cells(pts, vox)
        sc = polyline_cells(np.vstack([p0, p1]), vox)
        pt_comp.append(n_components_6face(pc))
        sg_comp.append(n_components_6face(sc))
        pt_cells.append(len(pc))
        sg_cells.append(len(np.unique(sc, axis=0)))
    pt_comp = np.array(pt_comp); sg_comp = np.array(sg_comp)
    return {
        'vox': vox, 'n_fib': n_fib, 'L_um': L, 'point_step_um': round(step, 4),
        'point_broken_pct': round(100.0 * (pt_comp > 1).mean(), 2),
        'point_mean_components': round(float(pt_comp.mean()), 3),
        'segment_broken_pct': round(100.0 * (sg_comp > 1).mean(), 2),
        'segment_mean_components': round(float(sg_comp.mean()), 3),
        'point_cells_mean': round(float(np.mean(pt_cells)), 2),
        'segment_cells_mean': round(float(np.mean(sg_cells)), 2),
        'cells_ratio_seg_over_pt': round(float(np.mean(sg_cells) / max(np.mean(pt_cells), 1e-9)), 3),
    }


# ────────────────────────────────────────────────────────────────────────────
def _selftest():
    ok = fail = 0

    def chk(msg, cond):
        nonlocal ok, fail
        print(('  PASS  ' if cond else '  FAIL  ') + msg)
        ok, fail = ok + (1 if cond else 0), fail + (0 if cond else 1)

    rng = np.random.default_rng(1)

    # ① 연속 셀은 항상 face 인접 (구성상 보장 — 이것이 이 파일의 존재 이유)
    bad = 0
    for _ in range(400):
        p0, p1 = _straight_fibre(rng, 10.0, 20.0)
        c = segment_cells(p0, p1, 0.4)
        dif = np.abs(np.diff(c, axis=0)).sum(axis=1)
        if len(dif) and dif.max() != 1:
            bad += 1
    chk('1) ★ 연속 셀이 항상 정확히 한 축만 1칸 이동 (6-face 보장)', bad == 0)

    # ② 직선 섬유는 단일 연결성분 — 어떤 vox 에서도
    for vox in (0.4, 0.2, 0.141, 0.05):
        nb = 0
        for _ in range(150):
            p0, p1 = _straight_fibre(rng, 10.0, 20.0)
            if n_components_6face(segment_cells(p0, p1, vox)) != 1:
                nb += 1
        chk(f'2) vox {vox}: 직선 섬유 150개 전부 단일 성분 (끊김 {nb})', nb == 0)

    # ③ 점-스탬프는 같은 섬유에서 실제로 끊긴다 (결함 재현 = 대조군이 유효한가)
    r = ab_compare(vox=0.4, n_fib=150, seed=7)
    chk(f"3) ★ 결함 재현: 점-스탬프 단절 {r['point_broken_pct']}% "
        f"(평균 {r['point_mean_components']} 성분)", r['point_broken_pct'] > 80)
    chk(f"4) ★ 선분-스탬프 단절 {r['segment_broken_pct']}%  = 0", r['segment_broken_pct'] == 0.0)

    # ④ 폴리라인(굽은 섬유)도 이어진다 — curl 이 있는 실제 VGCF/PTFE 대비
    nb = 0
    for _ in range(120):
        p = [rng.uniform(4, 16, 3)]
        d = rng.normal(size=3); d /= np.linalg.norm(d)
        for _ in range(12):                      # persistent random walk (curl 모사)
            d = d + 0.35 * rng.normal(size=3)
            d /= np.linalg.norm(d)
            p.append(p[-1] + 0.8 * d)
        if n_components_6face(polyline_cells(np.array(p), 0.4)) != 1:
            nb += 1
    chk(f'5) ★ 굽은 폴리라인 120개도 단일 성분 (끊김 {nb}) — curl 있는 실제 섬유 대비', nb == 0)

    # ⑤ 셀 수는 점-스탬프보다 많지 않아야 자연스럽다 (중복 없이 경로만 채움)
    chk(f"6) 선분/점 셀 수 비 {r['cells_ratio_seg_over_pt']} — 폭증하지 않는다 (<1.6)",
        r['cells_ratio_seg_over_pt'] < 1.6)

    # ⑥ 축 정렬·퇴화 케이스 (edge/corner 통과, 0-길이)
    chk('7) 축 정렬 선분 (x축)', n_components_6face(
        segment_cells([0.05, 0.05, 0.05], [3.05, 0.05, 0.05], 0.4)) == 1)
    chk('8) ★ 정확히 대각선 (corner 통과 퇴화) 도 단일 성분',
        n_components_6face(segment_cells([0.0, 0.0, 0.0], [4.0, 4.0, 4.0], 0.4)) == 1)
    chk('9) 0-길이 선분 → 셀 1개', len(segment_cells([1.0, 1.0, 1.0], [1.0, 1.0, 1.0], 0.4)) == 1)
    chk('10) 음의 방향도 동작', n_components_6face(
        segment_cells([5.0, 5.0, 5.0], [1.0, 2.0, 3.0], 0.4)) == 1)

    # ⑦ 셀 순회가 실제로 선분을 덮는가 (중점 샘플이 전부 방문 셀 안에)
    p0, p1 = np.array([1.13, 2.71, 0.37]), np.array([7.9, 5.2, 9.1])
    cells = {tuple(c) for c in segment_cells(p0, p1, 0.4)}
    ts = np.linspace(0, 1, 2000)[:, None]
    sm = np.floor((p0 + ts * (p1 - p0)) / 0.4).astype(np.int64)
    miss = sum(1 for c in sm if tuple(c) not in cells)
    chk(f'11) ★ 선분 위 2000 샘플이 전부 방문 셀 안 (누락 {miss})', miss == 0)
    # 끝점이 복셀 경계에 정확히 놓이는 퇴화 케이스 (위 버그의 회귀)
    _p0, _p1 = np.array([1.13, 2.71, 0.37]), np.array([7.9, 5.2, 9.1])   # 5.2 = 13×0.4
    _c = segment_cells(_p0, _p1, 0.4)
    chk('12) ★ 끝점이 복셀 경계에 정확히 놓여도 끝점 셀이 포함된다 (회귀)',
        tuple(_c[-1]) == tuple(np.floor(_p1 / 0.4).astype(np.int64)))
    chk('13) 그때도 연속 셀은 face 인접 유지',
        int(np.abs(np.diff(_c, axis=0)).sum(axis=1).max()) == 1)
    # 시작점도 마찬가지
    chk('14) 시작 셀 = floor(p0)',
        tuple(segment_cells([2.0, 3.0, 4.0], [5.5, 3.3, 4.7], 0.4)[0])
        == tuple(np.floor(np.array([2.0, 3.0, 4.0]) / 0.4).astype(np.int64)))

    print(f'\nfibre_segment_raster selftest: {ok}/{ok + fail} PASS')
    return fail == 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--ab', action='store_true', help='점 vs 선분 A/B')
    ap.add_argument('--vox', type=float, default=0.4, help='STEP3 복셀 (기본 0.4 = production)')
    ap.add_argument('--n-fib', type=int, default=300)
    ap.add_argument('--mpm-dx', type=float, default=0.141, help='점 간격 = 0.7·dx')
    a = ap.parse_args()
    if a.selftest:
        sys.exit(0 if _selftest() else 1)
    if a.ab:
        for vox in ([a.vox] if a.vox else []) or [0.4]:
            r = ab_compare(vox=vox, n_fib=a.n_fib, mpm_dx=a.mpm_dx)
            print(f"vox {r['vox']}  (점 간격 {r['point_step_um']} µm, 섬유 {r['n_fib']}개)")
            print(f"  점-스탬프 (현행)  단절 {r['point_broken_pct']:5.1f}%  "
                  f"평균성분 {r['point_mean_components']:5.2f}  셀 {r['point_cells_mean']:.1f}")
            print(f"  선분-스탬프       단절 {r['segment_broken_pct']:5.1f}%  "
                  f"평균성분 {r['segment_mean_components']:5.2f}  셀 {r['segment_cells_mean']:.1f}"
                  f"  (셀비 {r['cells_ratio_seg_over_pt']})")
        return
    ap.print_help()


if __name__ == '__main__':
    main()
