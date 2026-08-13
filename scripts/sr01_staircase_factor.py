"""계단식 경로 인자 k 를 **실측**한다 — 직경-보존 σ 가 상한인가 하한인가를 가르는 양.

★ 왜 (2026-08-13 자기정정): 나는 게이트 ⑥/⑤ 에서 "계단식 여분 길이는 σ_e 를 더 낮추므로
  직경-보존 값은 **상한**" 이라고 적었다.  **부호가 반대다.**

    참 섬유   R_true = L / (σ_bulk · A_real)
    래스터    R_ras  = L_path / (σ_eff · A_vox),   L_path = k·L
    재척도    σ_eff  = σ_bulk · A_real / A_vox
    ⇒ R_ras = k · R_true   ⇒ 래스터가 k 배 **더 저항이 크다** ⇒ σ_e 가 k 배 **낮게** 나온다
    ⇒ 직경-보존 값은 **하한**이다.

  k 는 방향에 따라 1(축정렬) ~ √3(대각).  등방 랜덤이면 3·E[|cosθ|] = 1.5.
  그러나 **가정하지 않고 실측한다** — 압밀된 침대의 섬유는 등방이 아닐 수 있다
  (플래튼이 눌러 면내로 눕는다면 k 가 달라진다).

측정: 폴리라인 구간마다  (셀 수 − 1)·vox  vs  유클리드 길이.
      6-face 경로에서 한 스텝 = 한 면 = vox 이므로 그 합이 경로 길이다.

사용:  python3 scripts/sr01_staircase_factor.py [--kit kit_ps_7_3] [--vox 0.4]
"""
from __future__ import annotations

import argparse
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fibre_segment_raster import segment_cells                 # noqa: E402


def staircase_factor(pts, fid, vox, gap_tol=2.0, phase=None, sel_phase=None):
    """(k_len_weighted, stats) — 길이-가중 계단 인자.

    길이 가중이 옳다: 전체 저항은 Σ(경로길이)/Σ(참길이) 로 정해지고, 짧은 구간이
    같은 무게를 갖는 단순평균은 그것을 왜곡한다.
    """
    P = np.asarray(pts, np.float64)
    F = np.asarray(fid)
    if phase is not None and sel_phase is not None:
        m = np.asarray(phase) == sel_phase
        P, F = P[m], F[m]
    tot_path = 0.0
    tot_true = 0.0
    per_seg = []
    for f in np.unique(F):
        Q = P[F == f]
        if len(Q) < 2:
            continue
        d = np.linalg.norm(np.diff(Q, axis=0), axis=1)
        med = float(np.median(d)) if len(d) else 0.0
        brk = (np.nonzero(d > gap_tol * med)[0] + 1) if med > 0 else np.array([], int)
        for R in (np.split(Q, brk) if len(brk) else [Q]):
            if len(R) < 2:
                continue
            cells = np.vstack([segment_cells(R[i], R[i + 1], vox) for i in range(len(R) - 1)])
            cells = np.unique(cells, axis=0)
            n_steps = max(len(cells) - 1, 0)
            L_true = float(np.linalg.norm(R[-1] - R[0]))          # 끝점 사이 직선거리
            L_arc = float(np.linalg.norm(np.diff(R, axis=0), axis=1).sum())
            if L_arc <= 0:
                continue
            tot_path += n_steps * vox
            tot_true += L_arc                                     # 곡률은 물리 — 호길이가 참길이
            per_seg.append((n_steps * vox / L_arc, L_arc, L_true / L_arc))
    if not per_seg:
        raise ValueError('측정할 폴리라인 구간이 없다')
    a = np.array(per_seg)
    return float(tot_path / tot_true), {
        'n_segments': len(per_seg),
        'k_length_weighted': float(f'{tot_path / tot_true:.4f}'),
        'k_unweighted_med': float(f'{np.median(a[:, 0]):.4f}'),
        'k_p10_p90': [float(f'{np.percentile(a[:, 0], 10):.4f}'),
                      float(f'{np.percentile(a[:, 0], 90):.4f}')],
        'total_true_um': float(f'{tot_true:.4g}'),
        'total_path_um': float(f'{tot_path:.4g}'),
        'straightness_med': float(f'{np.median(a[:, 2]):.4f}'),   # 끝점거리/호길이 (1 = 직선)
        'note': ('k > 1 이면 래스터 경로가 길어 저항이 크다 ⇒ 직경-보존 σ_e 는 **하한**이고 '
                 '참값은 그만큼 위다.  등방 랜덤 이론값 1.5 · 축정렬 1 · 대각 √3=1.732'),
    }


def _selftest():
    ok, fail = 0, []

    def chk(n, c):
        nonlocal ok
        (ok := ok + 1) if c else fail.append(n)
        print(('  PASS  ' if c else '  FAIL  ') + n)

    vox = 0.4
    # 축정렬 → k = 1
    t = np.arange(0, 40) * 0.12
    P = np.stack([t, np.full_like(t, 1.1), np.full_like(t, 2.1)], 1)
    k, _ = staircase_factor(P, np.zeros(len(P), int), vox)
    chk(f'축정렬 k ≈ 1 (측정 {k:.3f})', abs(k - 1.0) < 0.06)
    # 대각 (1,1,1) → k = √3
    P = np.stack([t, t + 0.20, t + 0.10], 1)
    k, _ = staircase_factor(P, np.zeros(len(P), int), vox)
    chk(f'대각 k ≈ √3 = 1.732 (측정 {k:.3f})', abs(k - 3 ** 0.5) < 0.10)
    # 등방 랜덤 다발 → k ≈ 1.5
    rng = np.random.default_rng(0)
    pts, fids = [], []
    for i in range(300):
        u = rng.normal(size=3); u /= np.linalg.norm(u)
        s = np.arange(0, 60) * 0.12
        pts.append(np.array([10.0, 10.0, 10.0]) + np.outer(s, u))
        fids.append(np.full(60, i))
    k, st = staircase_factor(np.vstack(pts), np.concatenate(fids), vox)
    chk(f'등방 랜덤 k ≈ 1.5 (측정 {k:.3f}, 이론 1.5)', abs(k - 1.5) < 0.08)
    chk('k 는 항상 ≥ 1 (경로가 직선보다 짧을 수 없다)', st['k_p10_p90'][0] >= 0.98)
    print(f'\nsr01_staircase_factor selftest: {ok}/{ok + len(fail)} PASS'
          + (f'   FAILED: {fail}' if fail else ''))
    return 1 if fail else 0


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--kit', default='kit_ps_7_3')
    ap.add_argument('--vox', type=float, default=0.4)
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        raise SystemExit(_selftest())
    from sr01_realbed_ab import seed_carbon_on_kit               # noqa: E402
    S = seed_carbon_on_kit(a.kit, 288, 1.0, 0, max_fibres=0)
    k, st = staircase_factor(S['pts'], S['fid'], a.vox)
    import json as _j
    print(_j.dumps({'kit': a.kit, 'vox_um': a.vox, **st}, ensure_ascii=False, indent=2))
    print(f'\n⇒ 직경-보존 σ_e 는 **하한**.  참값 ≈ 측정값 × {k:.3f} (섬유 지배 극한)')
