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
            # ⚠⚠ 2026-08-13 (Codex CDX-02) — 첫 판은 `np.unique(cells, axis=0)` 였다.
            #   그것은 **경로 순서와 재방문을 통째로 버리고** 고유 셀 수만 세므로 순서 있는
            #   저항 경로 길이가 아니다.  `segment_cells` 는 DDA 라 이미 순서를 지켜 내주는데
            #   그걸 버리고 있었다.  ⇒ **연속 중복만** 없애고 순서를 지킨다.
            keep = np.ones(len(cells), bool)
            keep[1:] = (cells[1:] != cells[:-1]).any(1)
            cells = cells[keep]
            if len(cells) < 2:
                continue
            # 6-face 솔버가 실제로 지나야 하는 홉 수 = 연속 셀 사이 L1 거리의 합.
            # (DDA 가 대각으로 튀면 L1 이 2~3 이고, 그것이 6-face 로는 2~3 홉이다.)
            n_hops = int(np.abs(np.diff(cells.astype(np.int64), axis=0)).sum())
            L_arc = float(np.linalg.norm(np.diff(R, axis=0), axis=1).sum())
            L_chord = float(np.linalg.norm(R[-1] - R[0]))         # 끝점 사이 직선거리
            # ⚠ 분모를 호길이 전체로 두면 **끝 셀의 부분 통과**만큼 체계적으로 짧게 나온다
            #   (축정렬 픽스처가 k = 0.940 < 1 로 나왔던 이유 — 경로가 직선보다 짧을 수 없는데도).
            #   래스터 경로의 양 끝은 **셀 중심**이므로, 참길이도 같은 두 중심 사이로 재야 한다.
            c0 = (cells[0] + 0.5) * vox
            c1 = (cells[-1] + 0.5) * vox
            span = float(np.linalg.norm(c1 - c0))
            if L_chord <= 0 or L_arc <= 0 or span <= 0:
                continue
            L_ref = L_arc * (span / L_chord)          # 호길이를 중심-중심 구간으로 환산
            tot_path += n_hops * vox
            tot_true += L_ref
            per_seg.append((n_hops * vox / L_ref, L_ref, L_chord / L_arc))
    if not per_seg:
        raise ValueError('측정할 폴리라인 구간이 없다')
    a = np.array(per_seg)
    # ── ★ 짧은 구간 경고 (2026-08-13) ────────────────────────────────────────────────
    #   통제 실험(등방 랜덤 다발, 참값 1.5): estimator 의 **격자 간 산포는 구간 길이에
    #   좌우된다**.  vox 0.4/0.3/0.25 에서 폭 —
    #     구간 7.08 µm → 옛 0.0028 · 새 0.0011      구간 1.08 µm → 옛 0.0417 · 새 0.0187
    #     구간 0.60 µm → 옛 0.1443 · 새 0.0658      구간 0.36 µm → 옛 0.2149 · 새 0.0409
    #   실침대 재실측 폭 0.0456 은 **구간 ~1 µm 대의 estimator 편향과 같은 크기**다.
    #   ⇒ "k 가 격자에 의존한다" 는 결론을 내리기 전에 이 편향부터 빼야 한다.
    #   ⚠ 새 estimator 도 아주 짧은 구간에서는 편향된다 (0.36 µm 에서 1.345 < 1.5) —
    #     방향만 반대다.  둘 다 짧은 구간에서는 못 믿는다.
    short = float((a[:, 1] < 1.0).mean())
    return float(tot_path / tot_true), {
        'n_segments': len(per_seg),
        'run_len_um_med': float(f'{np.median(a[:, 1]):.4g}'),
        'short_run_frac': float(f'{short:.4f}'),
        'short_run_warning': (
            None if short < 0.2 else
            f'구간의 {short:.0%} 가 1 µm 미만 — 이 영역에서 estimator 는 격자마다 최대 '
            f'0.04~0.21 흔들린다 (통제실험).  k 의 격자 의존을 물리로 읽지 말 것'),
        'k_length_weighted': float(f'{tot_path / tot_true:.4f}'),
        'k_unweighted_med': float(f'{np.median(a[:, 0]):.4f}'),
        'k_p10_p90': [float(f'{np.percentile(a[:, 0], 10):.4f}'),
                      float(f'{np.percentile(a[:, 0], 90):.4f}')],
        'total_true_um': float(f'{tot_true:.4g}'),
        'total_path_um': float(f'{tot_path:.4g}'),
        'straightness_med': float(f'{np.median(a[:, 2]):.4f}'),   # 끝점거리/호길이 (1 = 직선)
        'note': ('k > 1 이면 래스터 경로가 길어 저항이 크다.  등방 랜덤 이론값 1.5 · '
                 '축정렬 1 · 대각 √3=1.732.  ⚠⚠ **k 로 σ_e 에 하한/상한을 붙이지 말 것** '
                 '(CL-20 retired, 2026-08-13): 계단 길이는 σ_e 를 낮추지만 격자가 만드는 '
                 '섬유 간 **가짜 상호연결**은 높이고, 관측 구간에서는 후자가 더 크다 (CL-24). '
                 '그리고 k 자신이 격자에 의존한다 — 아래 grid_dependence 참조'),
        'grid_dependence': ('옛 estimator 로 잰 실침대 k 는 격자마다 달랐다 — 1.4855@0.4 · '
                            '1.4917@0.3 · 1.4461@0.25 (폭 0.046).  ⚠ 그러나 통제실험은 그 '
                            '폭이 **짧은 구간에서의 estimator 편향**과 같은 크기임을 보인다 '
                            '(구간 1.08 µm 에서 옛 폭 0.0417).  ⇒ "k 가 격자에 의존한다" 는 '
                            '**아직 성립하지 않는다**; 새 estimator 로 재고 short_run_frac 을 '
                            '함께 볼 것'),
    }


def _selftest():
    ok, fail = 0, []

    def chk(n, c):
        nonlocal ok
        (ok := ok + 1) if c else fail.append(n)
        print(('  PASS  ' if c else '  FAIL  ') + n)

    vox = 0.4
    # ★ 축정렬 → k = 1 **정확히**.  옛 estimator 는 0.940 (< 1 = 비물리)인데 허용오차
    #   0.06 안에 0.0001 차로 들어와 PASS 했다 (Codex CDX-02).  이제 등호로 묶는다.
    t = np.arange(0, 40) * 0.12
    P = np.stack([t, np.full_like(t, 1.1), np.full_like(t, 2.1)], 1)
    k, st_ax = staircase_factor(P, np.zeros(len(P), int), vox)
    chk(f'축정렬 k = 1 **정확히** (측정 {k:.6f}; 옛 estimator 0.940)', abs(k - 1.0) < 1e-9)
    chk(f'★ 축정렬에서도 k ≥ 1 (경로가 직선보다 짧을 수 없다; p10={st_ax["k_p10_p90"][0]})',
        st_ax['k_p10_p90'][0] >= 1.0 - 1e-9)
    # 대각 (1,1,1) → k = √3.  ⚠ 여기는 정확히 안 맞는다 — 끝 셀 중심이 선 위에 있지 않아
    #   `span` 에 잔차가 남는다 (측정 1.7306 vs 1.7321 = **0.086 %**).  축정렬은 선과 중심이
    #   같은 직선이라 정확히 1 이 나온다.  ⇒ 잔차를 숨기지 말고 허용오차로 **명시**한다.
    P = np.stack([t, t + 0.20, t + 0.10], 1)
    k, _ = staircase_factor(P, np.zeros(len(P), int), vox)
    chk(f'대각 k = √3 = 1.732051 ± 0.086 % 끝셀잔차 (측정 {k:.6f}; 옛 estimator 1.678)',
        abs(k - 3 ** 0.5) < 0.005)
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
