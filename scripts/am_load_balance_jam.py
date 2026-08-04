#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AM 지지-하중평형 정지 (load-balance jam) — 순수 기하 + 측정 응답곡선으로 플래튼 정지 높이를 푼다.

═══ 왜 이게 필요한가 ═══════════════════════════════════════════════════════════════════
scaffold MPM 에서 얼린 AM 은 `wallP` 에 기여가 **정확히 0** 이다 (am_mask 가 grid_v 를 0 으로
못박고, 플래튼 반력은 Σ m·(v−v_wall) 로 적분되므로 정지 상태에서 0·0).  그래서
  · 응력으로 정직하게 멈추면 → SE 혼자 300 MPa 를 지라는 요구 → 실험보다 5~6 %p 과압축
  · 기하(percentile jam)로 멈추면 → DEM 표면의 되읽기 (2026-08-05 적대리뷰 2건 판정)
둘 다 porosity 를 "계산" 하지 못한다.

빠진 것은 **플래튼이 AM 크라운에 얹히는 하중** 하나다.  그 몫은 기하로 잴 수 있고
(A_supp(h) = 평면 h 에서 AM 이 가리는 면적 비율, scaffold CSV 에서 직접),
그 접촉이 견디는 압력은 재료 상수다 (압입 경도 H_AM, 문헌 앵커).  나머지는 SE 가 진다:

    P_target = A_supp(h)·H_AM  +  wallP_SE(h)
               └ 기하 (CSV)       └ 측정 응답곡선 (--compact-to 정착값)

★ 이 식의 자유 파라미터는 H_AM **하나**이고 문헌에서 온다.  porosity 를 보고 맞추는 값이
  아니다 — 그게 percentile jam(=DEM 두께에 q 를 맞춤)과의 결정적 차이다.
★ 그리고 **압력 의존이 살아난다**: A_supp(h)·H_AM 항이 P 에 따라 다른 h 를 준다 →
  Heckel 이 표현 가능해진다.  기하 jam 은 P 와 무관한 상수를 뱉어 이게 불가능했다.

═══ 검증 규약 (사전등록) ═══════════════════════════════════════════════════════════════
비순환 검증의 형태는 하나뿐이다 — **단일 H_AM 이 여러 압력의 DEM 두께를 동시에 재현**해야 한다.
H_AM 을 300 MPa 한 점에 역산해 맞추면 그건 q 를 맞추던 것과 같은 순환이다.
  · `--invert` 는 "이 두께가 나오려면 H_AM 이 얼마여야 하나" 를 역산한다 → **문헌값과 비교용**
    (LPSCl-NCM 계 NCM811 압입 경도 문헌대 ≈ 3~6 GPa).  역산값이 그 밴드 밖이면 모델이 틀린 것.
  · `--sweep-p` 로 100/300/600 MPa 를 돌려 **같은 H_AM 으로** 세 두께를 낸 뒤 DEM 과 대조한다.
    압력에 따라 필요한 H_AM 이 드리프트하면 이 가설은 기각된다.

═══ porosity 관례 (★ 반드시 병기) ══════════════════════════════════════════════════════
DEM 정본 = ε_sphere (구 부피 합, 접촉 겹침 이중계상 — 소성 material-conserving 관례)
MPM 부기 = union   (복셀 합 + SE-in-AM 축출)
같은 베드·같은 높이에서 **1.25 %p** 차이난다 (SE-SE 렌즈 0.402 + AM-SE 축출 0.848, 2026-08-05
적대리뷰가 소수 셋째 자리까지 분해).  두 값을 항상 같이 찍는다 — 하나만 보면 오늘의 사고가 반복된다.

  python3 scripts/am_load_balance_jam.py --am docs/data/real14_am_scaffold.csv \\
      --se docs/data/real14_se_scaffold.csv --h-am 4.0 --dem-thickness 30.28
  python3 scripts/am_load_balance_jam.py --am ... --se ... --invert --dem-thickness 30.28
  python3 scripts/am_load_balance_jam.py --am ... --se ... --h-am 4.0 --sweep-p 0.1,0.3,0.6
  python3 scripts/am_load_balance_jam.py --selftest
"""
from __future__ import annotations

import argparse
import csv
import sys

import numpy as np

UM_PER_LU = 1000.0        # scaffold CSV 는 LIGGGHTS 단위(LU); 1 LU = 1000 µm 규약

# ── real_14 정착 SE 응답곡선 (2026-08-05 실측, --compact-to + hold, n_grid 384, sub 160) ──────
#    (두께 µm, 정착 wallP GPa).  wallP 는 **전체 면적**으로 정규화된 값이므로 그대로 더하면 된다
#    (A_supp 로 다시 나누지 말 것 — 그게 이 식이 (1−A)·σ 꼴이 아닌 이유).
#    30.22 점은 --am-jam q=95 런, 나머지 4점은 --compact-to 스윕.
REAL14_SE_CURVE = np.array([
    [30.22, 0.0098],
    [29.81, 0.0359],
    [28.92, 0.1038],
    [28.24, 0.1411],
    [27.70, 0.1690],
])


def read_scaffold(path):
    """scaffold CSV → (centres[N,3] µm, radii[N] µm, types[N])."""
    rows = [r for r in csv.reader(open(path)) if r and not r[0].lstrip().startswith('#')]
    if not rows:
        sys.exit(f'{path}: 데이터 행이 없습니다')
    t = np.array([int(float(r[0])) for r in rows])
    c = np.array([[float(v) for v in r[1:4]] for r in rows]) * UM_PER_LU
    r = np.array([float(r[4]) for r in rows]) * UM_PER_LU
    return c, r, t


def support_fraction(centres, radii, h, box_um):
    """평면 h 에서 AM 이 가리는 면적 비율 (그림자).

    ★ 단면적 π(r²−(r−d)²) 이 아니라 **그림자** 를 쓴다: 평면을 완전히 통과한 입자(d>2r)의
    단면적은 기하상 0 이라 척도가 비단조가 된다 (실측: q=75 66.5 % → q=70 64.4 %).
    d 를 r 로 캡하면 d≥r 에서 πr² (최대 그림자)로 포화하고 단조가 된다.
    """
    d = (centres[:, 2] + radii) - h          # 구 꼭대기가 평면 위로 나온 깊이
    m = d > 0
    if not m.any():
        return 0.0
    rr = radii[m]
    dc = np.minimum(d[m], rr)
    return float(np.pi * np.maximum(rr ** 2 - (rr - dc) ** 2, 0.0).sum()) / float(box_um ** 2)


def se_response(h, curve=REAL14_SE_CURVE):
    """측정 SE 응답곡선 wallP_SE(h) — log 선형 보간, 밖은 양끝 기울기로 외삽.

    응력은 두께에 대해 지수적으로 오르므로 log 공간에서 보간한다 (실측 구간 기울기
    0.10~0.41 /%p, 포화 경향).  외삽은 양끝 기울기를 유지 — **외삽 구간은 신뢰구간 밖**이라
    호출부가 flag 를 함께 받는다.
    """
    xs = curve[:, 0][::-1]                    # 두께 오름차순
    ys = np.log(curve[:, 1][::-1])
    inside = bool(xs[0] <= h <= xs[-1])
    if h < xs[0]:
        k = (ys[1] - ys[0]) / (xs[1] - xs[0])
        return float(np.exp(ys[0] + k * (h - xs[0]))), inside
    if h > xs[-1]:
        k = (ys[-1] - ys[-2]) / (xs[-1] - xs[-2])
        return float(np.exp(ys[-1] + k * (h - xs[-1]))), inside
    return float(np.exp(np.interp(h, xs, ys))), inside


def porosities(h, solid_union_um, solid_sphere_um):
    """같은 높이의 두 관례 porosity (%) — union(MPM 부기) / sphere(DEM 정본)."""
    return (max(0.0, 1.0 - solid_union_um / h) * 100.0,
            max(0.0, 1.0 - solid_sphere_um / h) * 100.0)


def solve_height(centres, radii, box_um, h_am, p_target, lo, hi, tol=1e-4):
    """P(h) = A_supp(h)·H_AM + wallP_SE(h) = p_target 를 만족하는 h (이분법).

    P(h) 는 h 감소에 단조 증가(그림자↑·SE응력↑)하므로 이분법이 안전하다.
    """
    def P(h):
        return support_fraction(centres, radii, h, box_um) * h_am + se_response(h)[0]
    if P(hi) > p_target:                      # 가장 느슨한 높이에서도 이미 초과
        return hi, P(hi), 'above_at_hi'
    if P(lo) < p_target:                      # 가장 조밀한 높이에서도 미달
        return lo, P(lo), 'below_at_lo'
    a, b = lo, hi
    for _ in range(80):
        m = 0.5 * (a + b)
        if P(m) > p_target:
            a = m
        else:
            b = m
        if b - a < tol:
            break
    h = 0.5 * (a + b)
    return h, P(h), 'ok'


def invert_h_am(centres, radii, box_um, h_dem, p_target):
    """주어진 두께가 나오려면 H_AM 이 얼마여야 하나 — **문헌값과 대조하기 위한 역산**."""
    a = support_fraction(centres, radii, h_dem, box_um)
    s, _ = se_response(h_dem)
    if a <= 0:
        return float('inf'), a, s
    return (p_target - s) / a, a, s


def _selftest():
    ok, fail = 0, []

    def chk(name, cond):
        nonlocal ok
        if cond:
            ok += 1
        else:
            fail.append(name)

    # 그림자: 단조 + 완전통과 포화 (단면적 공식의 d>2r 비단조 버그 회귀 방지)
    c = np.array([[0.0, 0.0, 10.0]] * 3)
    r = np.array([1.0, 1.0, 1.0])
    s = [support_fraction(c, r, h, 10.0) for h in (12.0, 11.0, 10.5, 10.0, 9.0, 8.0, 7.0)]
    chk('그림자는 평면을 내릴수록 단조 증가 (d>2r 경계 너머 포함)',
        all(s[i] <= s[i + 1] + 1e-12 for i in range(len(s) - 1)))
    chk('완전 통과 입자의 그림자 = πr² (0 으로 사라지지 않는다)',
        abs(s[-1] - 3 * np.pi / 100.0) < 1e-9)
    chk('최고점 평면의 그림자 = 0', support_fraction(c, r, 11.0, 10.0) == 0.0)

    # 응답곡선: 측정점 재현 + 두께↓ 이면 응력↑
    for hh, ss in REAL14_SE_CURVE:
        chk(f'응답곡선이 측정점 {hh:.2f}µm 을 재현', abs(se_response(hh)[0] - ss) < 1e-9)
    chk('응답곡선은 두께가 얇을수록 크다', se_response(28.0)[0] > se_response(30.0)[0])
    chk('측정 구간 밖은 inside=False 로 표시', se_response(35.0)[1] is False)

    # 하중평형: H_AM 이 크면 더 느슨한(두꺼운) 높이에서 멈춘다 = 압력 의존이 살아있다
    cc = np.array([[0.0, 0.0, 29.0 + 0.2 * i] for i in range(50)])
    rr = np.full(50, 1.0)
    h1, _, _ = solve_height(cc, rr, 50.0, 2.0, 0.30, 27.0, 31.0)
    h2, _, _ = solve_height(cc, rr, 50.0, 6.0, 0.30, 27.0, 31.0)
    chk('H_AM 이 크면 더 두꺼운 높이에서 정지', h2 > h1)
    hp1, _, _ = solve_height(cc, rr, 50.0, 4.0, 0.10, 27.0, 31.0)
    hp2, _, _ = solve_height(cc, rr, 50.0, 4.0, 0.60, 27.0, 31.0)
    chk('압력이 높으면 더 얇은 높이에서 정지 (Heckel 방향)', hp2 < hp1)
    chk('압력 의존이 실재 — 100 vs 600 MPa 두께 차 > 0.1µm', (hp1 - hp2) > 0.1)

    # 역산은 정방향과 일관 (같은 H_AM 을 돌려줘야 한다)
    hstar, _, _ = solve_height(cc, rr, 50.0, 4.0, 0.30, 27.0, 31.0)
    hb, _, _ = invert_h_am(cc, rr, 50.0, hstar, 0.30)
    chk('역산 H_AM 이 정방향과 일치', abs(hb - 4.0) < 0.02)

    # 관례: union 은 sphere 보다 항상 크다(= 고체를 적게 세므로) — 부호 회귀 방지
    pu, ps = porosities(30.28, 25.170, 25.548)
    chk('union porosity > sphere porosity (같은 높이)', pu > ps)

    print(f'selftest: {ok}/{ok + len(fail)} PASS' + (f'   FAILED: {fail}' if fail else ''))
    return 0 if not fail else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--am', help='AM scaffold CSV (type,x,y,z,r  LU)')
    ap.add_argument('--se', help='SE scaffold CSV — 고체부피(두 관례) 계산용')
    ap.add_argument('--box-um', type=float, default=50.0, help='측면 박스 한 변 (µm)')
    ap.add_argument('--h-am', type=float, default=4.0,
                    help='AM 압입 경도 (GPa).  ★문헌 앵커 — porosity 에 맞추지 말 것. '
                         'NCM811 계 문헌대 ≈ 3~6')
    ap.add_argument('--p-target', type=float, default=0.30, help='제작 압력 (GPa)')
    ap.add_argument('--sweep-p', default='', help='쉼표 구분 압력 스윕 (GPa), 예 0.1,0.3,0.6')
    ap.add_argument('--dem-thickness', type=float, default=0.0,
                    help='DEM 실측 두께 (µm) — 있으면 대조·역산에 쓴다')
    ap.add_argument('--invert', action='store_true',
                    help='주어진 --dem-thickness 가 나오려면 H_AM 이 얼마여야 하는지 역산 '
                         '(문헌 밴드와 대조용; 이 값을 그대로 --h-am 에 넣으면 순환이다)')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)

    if a.selftest:
        return _selftest()
    if not a.am or not a.se:
        ap.error('--am 과 --se 가 필요합니다 (또는 --selftest)')

    am_c, am_r, am_t = read_scaffold(a.am)
    se_c, se_r, _ = read_scaffold(a.se)
    A = a.box_um ** 2

    # 고체 부피 — 두 관례.  sphere = 구 부피 합(겹침 이중계상, DEM 정본).
    # union 은 렌즈 겹침을 빼서 근사한다 (SE-SE + AM-SE; 삼중 겹침은 무시 = 상한).
    v_sph = float((4.0 / 3.0 * np.pi * am_r ** 3).sum() + (4.0 / 3.0 * np.pi * se_r ** 3).sum())

    def lens_overlap(c1, r1, c2, r2, same):
        from scipy.spatial import cKDTree
        tot = 0.0
        tree2 = cKDTree(c2)
        for i in range(len(c1)):
            for j in tree2.query_ball_point(c1[i], r1[i] + r2.max()):
                if same and j <= i:
                    continue
                d = float(np.linalg.norm(c1[i] - c2[j]))
                ra, rb = float(r1[i]), float(r2[j])
                if d < ra + rb and d > abs(ra - rb):
                    tot += (np.pi * (ra + rb - d) ** 2
                            * (d ** 2 + 2 * d * rb - 3 * rb ** 2 + 2 * d * ra + 6 * ra * rb
                               - 3 * ra ** 2) / (12.0 * d))
                elif d <= abs(ra - rb):
                    tot += 4.0 / 3.0 * np.pi * min(ra, rb) ** 3
        return tot

    try:
        ov = lens_overlap(se_c, se_r, se_c, se_r, True) + lens_overlap(am_c, am_r, se_c, se_r, False)
    except Exception as e:                                  # scipy 없음 등 — 관례차 없이 진행
        print(f'  ⚠ 겹침 계산 실패 ({type(e).__name__}) → union 관례 생략, sphere 만 보고')
        ov = 0.0
    v_uni = v_sph - ov
    solid_sph, solid_uni = v_sph / A, v_uni / A

    print(f'베드: AM {len(am_r)} (r {am_r.min():.1f}~{am_r.max():.1f}µm) + SE {len(se_r)}, '
          f'박스 {a.box_um:g}×{a.box_um:g}µm')
    print(f'고체/면적:  sphere 관례 {solid_sph:.3f} µm  ·  union 관례 {solid_uni:.3f} µm  '
          f'(겹침 {ov:.1f} µm³ = {ov / A:.3f} µm)')
    print(f'AM 압입 경도 H_AM = {a.h_am:g} GPa   (문헌 앵커; --invert 로 역산값 확인)\n')

    if a.invert:
        if a.dem_thickness <= 0:
            ap.error('--invert 에는 --dem-thickness 가 필요합니다')
        hb, asup, sse = invert_h_am(am_c, am_r, a.box_um, a.dem_thickness, a.p_target)
        print(f'역산 @ {a.dem_thickness:.2f}µm, P={a.p_target:g} GPa:')
        print(f'  AM 지지 면적 {asup:.3%}  ·  SE 응답 {sse:.4f} GPa (= P 의 {sse / a.p_target:.1%})')
        print(f'  → 필요한 H_AM = ({a.p_target:g} − {sse:.4f}) / {asup:.5f} = **{hb:.2f} GPa**')
        band = 3.0 <= hb <= 6.0
        print(f'  NCM811 압입경도 문헌대 3~6 GPa 대비: {"안에 있음 ✓" if band else "밖 ✗ — 모델 재검토"}')
        print('\n  ⚠ 이 값을 --h-am 에 그대로 넣으면 순환이다.  검증은 --sweep-p 로 '
              '**한 H_AM 이 여러 압력의 DEM 두께를 동시에** 재현하는지 보는 것.')
        return 0

    ps = ([float(x) for x in a.sweep_p.split(',') if x.strip()] if a.sweep_p else [a.p_target])
    lo = float(max(am_c[:, 2].min(), solid_uni * 1.001))
    hi = float((am_c[:, 2] + am_r).max())
    print(f'{"P (GPa)":>8} {"h (µm)":>8} {"A_supp":>8} {"SE (GPa)":>9} {"AM 몫":>7} '
          f'{"ε_union":>9} {"ε_sphere":>9} {"vs DEM":>8}')
    for p in ps:
        h, pach, st = solve_height(am_c, am_r, a.box_um, a.h_am, p, lo, hi)
        asup = support_fraction(am_c, am_r, h, a.box_um)
        sse, inside = se_response(h)
        pu, psph = porosities(h, solid_uni, solid_sph)
        vs = f'{h - a.dem_thickness:+.2f}' if a.dem_thickness > 0 else '—'
        flag = ('' if st == 'ok' else f'  ⚠{st}') + ('' if inside else '  ⚠SE외삽')
        print(f'{p:8.3f} {h:8.2f} {asup:8.2%} {sse:9.4f} {asup * a.h_am / p:7.1%} '
              f'{pu:8.2f}% {psph:8.2f}% {vs:>8}{flag}')
    if len(ps) > 1:
        print('\n  ★ 압력 의존이 살아있는지가 이 모델의 시험대다 — 기하 jam 은 P 와 무관한 '
              '상수를 뱉는다.\n     같은 H_AM 으로 여러 P 의 DEM 두께를 재현하면 비순환 검증 통과.')
    print('\n  관례: ε_union = MPM 부기(복셀 합) · ε_sphere = DEM 정본(구 부피 합).  '
          '둘은 같은 높이에서\n        구조적으로 다르다 — 하나만 인용하면 비교가 깨진다.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
