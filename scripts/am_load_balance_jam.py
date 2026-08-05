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

# ── real_14 정착 SE 응답곡선 (2026-08-05 **11점 재생성**, GPU 5.5 h) ────────────────────
#    (φ_SE_local, 정착 wallP GPa).  wallP 는 전체 면적 정규화값이라 그대로 더한다
#    (A_supp 로 다시 나누지 말 것 — 이 식이 (1−A)·σ 꼴이 아닌 이유).
#    조건: n_grid 384 · sub 160 · --protocol hold · --periodic · --arch cuda --gpu-mem 8
#          --compact-to <ε_target> (변위구동 → 실측 정착 두께·wallP 를 그대로 기록)
#    ★ 옛 5점 폐기 이유: 실행 조건(--sub/--frames)이 복구 불가였고(json 미기록·산출물 부재),
#      같은 목표로 재현하니 σ 가 **계통적으로 +8~19 % 높았다** = 다른 프로토콜 확정.
#      MPM 은 random_seed 고정 결정론이라 런-투-런 노이즈가 아니다.
#
#    ★★ 곡선의 두 성질 (이 트랙의 물리 결론):
#      (1) φ ≲ 0.58 → σ ≈ 0.  SE 가 **jamming 전**이라 하중을 못 받는다 (진짜 0).
#      (2) φ ≳ 0.81 → **포화**.  von Mises σ_y = 0.30 GPa 에서 항복하므로 측정 최대가
#          0.2771 < 0.30 이다.  ⇒ **SE 혼자서는 target 0.30 GPa 를 원리적으로 못 낸다** —
#          2026-08-05 오전 "freeze-probe 로는 어떤 scaffold 런도 정지 불가" 의 물리적 근거.
#          하중-분담 항 A_supp·H_AM 이 없으면 방정식에 해가 없다.
#
#    ★ 색인 변수가 두께(µm)가 아니라 φ_SE_local = V_SE/(A·h − V_AM) 인 이유:
#      두께는 베드마다 다른 양이라 real_14(26~31µm) 곡선을 6mAh 베드(111~116µm)에 대면
#      4배 외삽이 되어 wallP_SE 가 0 으로 붕괴한다 (10케이스 런에서 전 행 0.0000 로 실제 발생).
#      SE 응력은 SE 가 자기 몫의 공간에서 얼마나 조밀한가에 달린 물성이므로 φ 로 색인하면
#      두께가 달라도 곡선 안에 떨어진다.  real_14 환산: V_AM 46679.9 · V_SE 17190.8 · A 2500
#
#    ★★★ 전이 가정은 실측으로 **기각되었다** (2026-08-06, scripts/analyze_se_curve_transfer.py).
#      φ 색인이 두께 외삽 붕괴를 고치는 것은 맞지만, **다른 베드에 그대로 쓸 수는 없다**.
#      kit_ps_7_3(P:S 7:3, SE/solid 34.2 %, 108–117 µm)을 real_14 와 **재하율까지 맞춰**
#      (--platen-mach, V/c_P 0.030 vs 0.0306) 같은 φ 에서 재니:
#          φ 0.700 → 2.96×   0.754 → 2.83×   0.851 → 3.65×   0.905 → 3.83×
#      즉 같은 φ 에서 kit 의 SE 가 **3배 안팎의 응력**을 받는다.  (재하율을 맞추기 전에는
#      2.3~3.0× 로 보였다 — kit 이 3.4배 빨리 눌려 σ 가 과소평가돼 있었다.  재하율 교정은
#      결론을 뒤집은 게 아니라 20~28 % 강화했다.)
#      부수 관찰: kit 은 φ 0.632 에서 아직 σ=0 (real_14 는 이미 0.073) → **개시가 늦고 그 뒤
#      훨씬 가파르다**; kit 최대 σ 1.012 GPa = σ_y(0.30)의 3.4배 → 편차응력은 σ_y 에 갇혀도
#      **정수압은 안 갇힌다**.  real_14(최대 0.278 < σ_y)는 아직 공극으로 흐르는 중이고,
#      kit 은 잔여 공극에 닿지 못해 가압되는 중이라는 뜻 = 같은 φ 라도 **잔여 공극의
#      도달가능성(채널 기하)이 다르다**.
#      ⇒ 이 곡선은 **real_14 전용**이다.  다른 베드에 쓰려면 그 베드에서 직접 재야 한다
#        (scripts/plan_se_curve_targets.py 가 φ 격자 측정점을 설계해 준다).
#        미측정 베드에 쓰면 아래 CURVE_BED / assert_curve_bed 가 경고한다.
#      아직 안 갈린 것: 3배 차가 **조성(채널 기하)** 때문인지 **두께(≈4배)** 때문인지.
#        kit_ps_{0_10,3_7,5_5,7_3,10_0} 를 같은 두께에서 비교하면 분리된다 (다음 실험).
#
#: 이 곡선을 잰 베드.  다른 베드에 쓰면 assert_curve_bed 가 경고한다 (위 ★★★ 참조).
CURVE_BED = 'real_14'
REAL14_SE_CURVE = np.array([
    [0.5356, 0.0000],   # ε_union 20.090 %  t 31.511 µm  — jamming 前
    [0.5593, 0.0001],   #        18.685     30.967
    [0.5785, 0.0004],   #        17.598     30.558
    [0.5956, 0.0117],   #        16.670     30.218   ← DEM 두께(30.28) 근방
    [0.6174, 0.0388],   #        15.529     29.810
    [0.6707, 0.1157],   #        12.945     28.925
    [0.7184, 0.1582],   #        10.847     28.244
    [0.7617, 0.1850],   #         9.095     27.700
    [0.8106, 0.1979],   #         7.272     27.155   ← 포화 시작
    [0.8588, 0.2376],   #         5.616     26.679
    [0.9131, 0.2771],   #         3.900     26.203   ★ σ_y 0.30 근접, 최대
])

# 곡선 밖으로 이만큼(φ 단위)까지만 외삽을 허용한다.  그 너머는 값을 만들지 않고 거부한다 —
# 조용한 외삽이 0.0000 을 내놓고 "SE 항이 없는 계산" 을 정상 결과처럼 보이게 만들었다.
SE_EXTRAP_MARGIN = 0.03

#: 곡선을 다른 베드에 쓸 때 나가는 경고를 케이스당 한 번만 (배치 출력이 뒤덮이지 않게).
_CURVE_BED_WARNED = set()


def assert_curve_bed(case_name, curve_bed=None, quiet=False):
    """이 케이스가 곡선을 잰 베드가 아니면 경고한다 (2026-08-06 전이 기각 — 상단 ★★★).

    거부가 아니라 경고인 이유: 베드별 곡선을 다 재기 전까지는 real_14 곡선이 유일한
    수단이고, 그걸 막으면 파이프라인이 통째로 선다.  대신 **결과에 이 사실이 반드시
    따라붙게** 해서 "곡선 하나로 전 코퍼스" 로 읽히는 것을 막는다.  실측 배수는
    같은 φ 에서 최대 3.8× 였으므로 미측정 베드의 절대값은 그 정도 불확실하다.
    """
    bed = curve_bed or CURVE_BED
    key = (str(case_name), bed)
    if quiet or key in _CURVE_BED_WARNED:
        return False
    if bed.lower() in str(case_name).lower():
        return False                                  # 곡선을 잰 그 베드 → 정상
    _CURVE_BED_WARNED.add(key)
    print(f"  ⚠ [curve] '{case_name}' 는 곡선을 잰 베드({bed})가 아닙니다 — SE 응답곡선의 "
          f"베드-전이는 실측으로 기각됐습니다 (같은 φ 에서 최대 3.8× 차, 2026-08-06). "
          f"이 케이스의 SE 응력·유도량은 ORDER-OF-MAGNITUDE 로만 읽으십시오. "
          f"정확한 값이 필요하면 plan_se_curve_targets.py 로 이 베드의 곡선을 직접 재십시오.",
          file=sys.stderr)
    return True


def phi_se_local(h, v_am, v_se, area):
    """비-AM 공간에서의 SE 충전율.  AM 이 차지한 부피를 뺀 곳에 SE 가 얼마나 들어찼는가."""
    free = area * h - v_am
    return float(v_se / free) if free > 0 else float('inf')


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


def se_response(phi, curve=REAL14_SE_CURVE):
    """측정 SE 응답곡선 wallP_SE(φ_SE_local) — **선형 보간** (log 아님).  반환 (GPa, inside).

    ★ 2026-08-05 11점 재생성으로 보간 방식을 바꿨다.  옛 5점은 좁은 구간(φ 0.596~0.762)만
    덮어 지수적으로 보였고 log 보간이 맞았지만, 넓힌 곡선은 **S-커브**다:
      · 아래쪽에 σ = 0 인 점이 실재 → log 는 −inf 라 다룰 수 없다
      · 위쪽은 σ_y 포화 → 지수 외삽하면 σ_y 를 넘어 발산한다
    11점이 φ 0.5356~0.9131 을 Δφ ≈ 0.02~0.05 로 촘촘히 덮으므로 선형이면 충분하다.

    경계 처리는 **물리적으로 비대칭**이다:
      · φ < 최소 → **0.0 반환 (inside=True)**.  더 느슨하면 jamming 이 더 멀어질 뿐 —
        외삽이 아니라 확실한 물리다.
      · φ > 최대 → **거부(nan)**.  포화하는 건 알지만 정확한 값은 모른다 (σ_y 근방).
    """
    xs = np.asarray(curve[:, 0], float)
    ys = np.asarray(curve[:, 1], float)
    if xs[0] > xs[-1]:
        xs, ys = xs[::-1], ys[::-1]
    if phi < xs[0]:
        return 0.0, True                      # jamming 전 — 물리적 0
    if phi > xs[-1] + SE_EXTRAP_MARGIN:
        return float('nan'), False            # 포화 구간 — 값 미상, 거부
    if phi > xs[-1]:                          # 좁은 마진: 마지막 값 유지 (포화 → 상수 근사)
        return float(ys[-1]), False
    return float(np.interp(phi, xs, ys)), True


def porosities(h, solid_union_um, solid_sphere_um):
    """같은 높이의 두 관례 porosity (%) — union(MPM 부기) / sphere(DEM 정본)."""
    return (max(0.0, 1.0 - solid_union_um / h) * 100.0,
            max(0.0, 1.0 - solid_sphere_um / h) * 100.0)


def _p_of_h(centres, radii, box_um, h_am, h, v_am, v_se, curve):
    """P(h) = A_supp(h)·H_AM + wallP_SE(φ_SE_local(h)).  SE 거부 구간은 0 으로 두되 flag."""
    a = support_fraction(centres, radii, h, box_um)
    s, ins = se_response(phi_se_local(h, v_am, v_se, box_um ** 2), curve)
    ok = np.isfinite(s)
    return a * h_am + (s if ok else 0.0), a, (s if ok else float('nan')), ins


def solve_height(centres, radii, box_um, h_am, p_target, lo, hi,
                 v_am=0.0, v_se=0.0, curve=REAL14_SE_CURVE, tol=1e-4):
    """P(h) = p_target 를 만족하는 h (이분법).

    P(h) 는 h 감소에 단조 증가(그림자↑·SE응력↑)하므로 이분법이 안전하다.
    v_am/v_se 를 안 주면 SE 항은 real_14 곡선을 그대로 h 로 쓰던 옛 거동이 아니라
    **0** 이 된다 (φ 를 만들 수 없으므로) — 호출부가 의도적으로 기하만 쓸 때의 경로.
    """
    def P(h):
        return _p_of_h(centres, radii, box_um, h_am, h, v_am, v_se, curve)[0]
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


def invert_h_am(centres, radii, box_um, h_dem, p_target,
                curve=REAL14_SE_CURVE, v_am=0.0, v_se=0.0):
    """주어진 두께가 나오려면 H_AM 이 얼마여야 하나 — **문헌값과 대조하기 위한 역산**.

    ⚠ 이 방향은 **조건이 나쁘다**: h_DEM 의 서브미크론 오차가 1/(dA_supp/dh) 만큼 증폭된다
    (real_14 실측: A_supp 1.5 %↔7.3 % 가 평면 0.56 µm 차이 → H_AM 이 20↔4 로 5배 튄다).
    판정에는 정방향(H_AM 고정 → h 예측)을 쓸 것 — 같은 배수로 **억제**된다.
    """
    a = support_fraction(centres, radii, h_dem, box_um)
    s, ins = se_response(phi_se_local(h_dem, v_am, v_se, box_um ** 2), curve)
    if not np.isfinite(s):
        s, ins = 0.0, False
    if a <= 0:
        return float('inf'), a, s
    return (p_target - s) / a, a, s


def dA_dh(centres, radii, box_um, h, eps=0.05):
    """dA_supp/dh — 조건수.  역산이 얼마나 증폭하고 정방향이 얼마나 억제하는지의 척도."""
    return (support_fraction(centres, radii, h - eps, box_um)
            - support_fraction(centres, radii, h + eps, box_um)) / (2 * eps)


def run_forward(cases, h_am=4.0, med_tol=0.015, max_tol=0.04):
    """★ 정방향 검증 — H_AM 을 **문헌값에 고정**하고 두께를 예측해 DEM 과 대조한다.

    왜 역산이 아니라 이 방향인가: A_supp 는 자유표면에서 가파르다 (real_14 실측
    ~10 %/µm).  그래서 h_DEM → H_AM 역산은 서브미크론 두께 정의 오차를 배수로 **증폭**하고
    (2026-08-05 10케이스: A_supp 4.9× 산포 = 평면 0.56 µm), H_AM → h 정방향은 같은 배수로
    **억제**한다 (H_AM 을 5배 틀려도 h 는 0.57 µm 이동).  모델을 실제로 쓰는 방향도 이쪽이다.

    사전등록 문턱 (2026-08-05, 실행 전 고정):
      PASS : median |Δh|/h ≤ 1.5 %  **그리고**  max |Δh|/h ≤ 4 %
      FAIL : 그 외
    상대 기준인 이유는 베드 두께가 30~116 µm 로 4배 흩어져 있기 때문.
    ★ Δh 는 **관례 무관**이다 (두께엔 sphere/union 구분이 없다) — 이 검증이 오늘의
      1.25 %p 관례 함정을 아예 비껴가는 이유.  Δε 는 참고로 sphere 관례로 환산해 병기.
    """
    rows = []
    for c in cases:
        am_c, am_r, _ = read_scaffold(c['am'])
        se_c, se_r, _ = read_scaffold(c['se'])
        v_am = float((4.0 / 3.0 * np.pi * am_r ** 3).sum())
        v_se = float((4.0 / 3.0 * np.pi * se_r ** 3).sum())
        area = c['box'] ** 2
        curve = read_curve(c['curve']) if c['curve'] else REAL14_SE_CURVE
        if not c['curve']:                       # 내장 real_14 곡선을 쓸 때만 베드 경고
            assert_curve_bed(c.get('name', '?'))
        lo = max(float(am_c[:, 2].min()), (v_am + v_se) / area * 1.001)
        hi = float((am_c[:, 2] + am_r).max())
        h, pach, st = solve_height(am_c, am_r, c['box'], h_am, c['p'], lo, hi,
                                   v_am, v_se, curve)
        _, a, s, ins = _p_of_h(am_c, am_r, c['box'], h_am, h, v_am, v_se, curve)
        dh = h - c['h_dem']
        solid = (v_am + v_se) / area                  # sphere 관례 고체 높이
        de = solid * (1.0 / c['h_dem'] - 1.0 / h) * 100.0
        rows.append(dict(label=c['label'], p=c['p'], h_dem=c['h_dem'], h=h, dh=dh,
                         rel=abs(dh) / c['h_dem'], de=de, a=a, s=s, inside=ins,
                         status=st, phi=phi_se_local(h, v_am, v_se, area)))
    rel = np.array([r['rel'] for r in rows], float)
    med, mx = float(np.median(rel)), float(rel.max())
    bad = [r['label'] for r in rows if r['status'] != 'ok']
    if bad:
        verdict = (f'FAIL — 경계에서 해가 안 잡힌 케이스 {len(bad)}개 '
                   f'({", ".join(bad[:3])}…): 모델이 그 압력에 도달 못 하거나 이미 초과')
    elif med <= med_tol and mx <= max_tol:
        verdict = ('PASS — 문헌 H_AM 하나로 모든 두께를 사전등록 문턱 안에서 재현 '
                   '(비순환 검증 통과)')
    else:
        verdict = (f'FAIL — median {med:.1%} (문턱 {med_tol:.1%}) · '
                   f'max {mx:.1%} (문턱 {max_tol:.1%})')
    return rows, dict(median=med, max=mx, verdict=verdict, h_am=h_am,
                      n_outside=sum(1 for r in rows if not r['inside']))


# 통과 밴드가 이 배수를 넘으면 그 PASS 는 정보가 아니다 — 떨어질 수 없는 시험은 시험이 아니다.
VACUOUS_BAND_RATIO = 3.0
H_AM_GRID = [0.5, 0.75, 1, 1.5, 2, 3, 4, 6, 8, 12, 20, 40]


def scan_h_am(cases, grid=None, med_tol=0.015, max_tol=0.04, band=(3.0, 6.0)):
    """★ 판정력 검사 — H_AM 을 얼마나 틀려도 이 시험을 통과하는가.

    2026-08-05 에 실제로 당한 것: 10케이스 정방향이 PASS 였는데, H_AM 을 0.5~40 GPa
    (80배) 로 흔들어도 전부 PASS 였다.  A_supp 가 ~10 %/µm 로 가팔라 h 가 H_AM 에 둔감하고
    (모델을 **쓰기엔** 좋은 성질), 상대 문턱은 두꺼운 베드에서 더 헐거워지기 때문이다.
    → PASS/FAIL 을 헤드라인으로 삼지 말고 **통과 밴드**를 보고한다.  밴드가 3배를 넘으면
      VACUOUS: 그 데이터셋은 H_AM 을 제약하지 못하므로 모델의 증거가 될 수 없다.
    """
    grid = list(grid) if grid is not None else list(H_AM_GRID)
    passed = [H for H in grid
              if run_forward(cases, h_am=H, med_tol=med_tol,
                             max_tol=max_tol)[1]['verdict'].startswith('PASS')]
    if not passed:
        return dict(passed=[], lo=None, hi=None, ratio=float('inf'),
                    verdict='FAIL — 어떤 H_AM 으로도 문턱을 못 넘는다 (모델 기각)')
    lo, hi = min(passed), max(passed)
    ratio = hi / lo
    lit_in = any(band[0] <= H <= band[1] for H in passed)
    if ratio > VACUOUS_BAND_RATIO:
        v = (f'VACUOUS — 통과 밴드 {lo:g}~{hi:g} GPa ({ratio:.0f}배).  이 데이터는 H_AM 을 '
             f'제약하지 못하므로\n     PASS 가 모델의 증거가 되지 않는다 '
             f'(떨어질 수 없는 시험은 시험이 아니다)')
    elif not lit_in:
        v = f'FAIL — 통과 밴드 {lo:g}~{hi:g} GPa 가 문헌대 {band[0]:g}~{band[1]:g} 를 배제'
    else:
        v = (f'PASS — 통과 밴드 {lo:g}~{hi:g} GPa ({ratio:.1f}배) 가 좁고 문헌대 '
             f'{band[0]:g}~{band[1]:g} 를 포함')
    return dict(passed=passed, lo=lo, hi=hi, ratio=ratio, verdict=v)


def read_curve(path):
    """SE 응답곡선 CSV (두께_µm, wallP_GPa) → ndarray.  베드마다 다른 곡선을 줄 수 있다."""
    rows = [r for r in csv.reader(open(path)) if r and not r[0].lstrip().startswith('#')]
    arr = np.array([[float(r[0]), float(r[1])] for r in rows])
    if len(arr) < 2:
        sys.exit(f'{path}: 응답곡선은 최소 2점 필요')
    return arr[np.argsort(-arr[:, 0])]        # 두께 내림차순 (REAL14_SE_CURVE 규약)


def read_cases(path):
    """케이스 매니페스트 CSV → dict 리스트.

    헤더: label,p_gpa,am_csv,se_csv,h_dem_um[,curve_csv,box_um]
    상대경로는 매니페스트 파일 기준으로 푼다 (킷 폴더를 통째로 옮겨도 깨지지 않게).
    """
    import os
    base = os.path.dirname(os.path.abspath(path))
    with open(path) as f:
        rd = csv.DictReader(r for r in f if not r.lstrip().startswith('#'))
        need = {'label', 'p_gpa', 'am_csv', 'se_csv', 'h_dem_um'}
        if not need <= set(rd.fieldnames or []):
            sys.exit(f'{path}: 헤더에 {sorted(need)} 가 모두 있어야 합니다 (현재 {rd.fieldnames})')
        out = []
        for r in rd:
            if not (r.get('label') or '').strip():
                continue
            rel = lambda k: (os.path.join(base, r[k]) if r.get(k) and not os.path.isabs(r[k])
                             else r.get(k) or '')
            out.append(dict(label=r['label'].strip(), p=float(r['p_gpa']),
                            am=rel('am_csv'), se=rel('se_csv'),
                            h_dem=float(r['h_dem_um']), curve=rel('curve_csv'),
                            box=float(r.get('box_um') or 50.0)))
    if not out:
        sys.exit(f'{path}: 케이스가 없습니다')
    return out


def run_cases(cases, band=(3.0, 6.0), tol_frac=0.25):
    """★ 비순환 검증 — 케이스마다 H_AM 을 역산하고 **하나의 상수로 수렴하는지** 본다.

    사전등록한 판정 규칙 (실행 전에 고정, 결과를 보고 바꾸지 않는다):
      PASS  : 역산 H_AM 의 (최대−최소)/중앙값 ≤ 25 % **이고** 중앙값이 문헌대 3~6 GPa 안
      FAIL  : 흩어짐이 25 % 초과 — 단일 재료상수로 설명되지 않음 = 모델 기각
      DRIFT : 흩어짐은 크지만 P 에 대해 **단조**이면 기각이 아니라 진단이다 —
              압입경도의 압력의존(Meyer 법칙 / 구속 경화).  log-log 기울기 m 을 함께 낸다
              (H ∝ P^m; m≈0 이 순수 상수, m>0 이 경화).  이 경우 다음 실험은 m 의 문헌 대조.
    """
    rows = []
    for c in cases:
        am_c, am_r, _ = read_scaffold(c['am'])
        se_c, se_r, _ = read_scaffold(c['se'])
        v_am = float((4.0 / 3.0 * np.pi * am_r ** 3).sum())
        v_se = float((4.0 / 3.0 * np.pi * se_r ** 3).sum())
        curve = read_curve(c['curve']) if c['curve'] else REAL14_SE_CURVE
        if not c['curve']:                       # 내장 real_14 곡선을 쓸 때만 베드 경고
            assert_curve_bed(c.get('name', '?'))
        h_am, asup, sse = invert_h_am(am_c, am_r, c['box'], c['h_dem'], c['p'],
                                      curve, v_am, v_se)
        _, inside = se_response(phi_se_local(c['h_dem'], v_am, v_se, c['box'] ** 2), curve)
        rows.append(dict(label=c['label'], p=c['p'], h=c['h_dem'], a=asup, s=sse,
                         hm=h_am, n_am=len(am_r), inside=inside,
                         dadh=dA_dh(am_c, am_r, c['box'], c['h_dem'])))
    return _score_cases(rows, band, tol_frac)


def _score_cases(rows, band, tol_frac):
    hs = np.array([r['hm'] for r in rows], float)
    fin = np.isfinite(hs)
    med = float(np.median(hs[fin])) if fin.any() else float('nan')
    spread = float((hs[fin].max() - hs[fin].min()) / med) if fin.sum() > 1 and med else 0.0
    slope = float('nan')
    if fin.sum() >= 3:
        pp = np.array([r['p'] for r in rows], float)[fin]
        if pp.max() > pp.min():
            slope = float(np.polyfit(np.log(pp), np.log(hs[fin]), 1)[0])
    in_band = band[0] <= med <= band[1]
    if spread <= tol_frac and in_band:
        verdict = 'PASS — 단일 H_AM 이 모든 케이스를 설명한다 (비순환 검증 통과)'
    elif np.isfinite(slope) and abs(slope) > 0.15:
        verdict = (f'DRIFT — H_AM 이 P 에 단조 의존 (H ∝ P^{slope:+.2f}).  기각이 아니라 '
                   f'압입경도의 구속-경화(Meyer) 진단이다')
    else:
        verdict = 'FAIL — 단일 재료상수로 설명 안 됨.  A_supp 정의 또는 SE 곡선을 재검토'
    return rows, dict(median=med, spread=spread, slope=slope, in_band=in_band, verdict=verdict)


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
    chk('응답곡선은 SE 가 조밀할수록 크다', se_response(0.75)[0] > se_response(0.60)[0])
    # ★ 2026-08-05 11점 곡선의 **비대칭** 경계 (물리)
    chk('아래쪽 밖 = 0.0 + inside (jamming 전은 확실한 물리, 외삽 아님)',
        se_response(0.30) == (0.0, True))
    chk('위쪽 마진 밖 = nan 거부 (포화값 미상 — 조용한 값 생성 금지)',
        not np.isfinite(se_response(1.20)[0]) and se_response(1.20)[1] is False)
    chk('위쪽 좁은 마진 = 마지막 값 유지 + inside=False (포화 상수 근사)',
        abs(se_response(0.93)[0] - REAL14_SE_CURVE[:, 1].max()) < 1e-12
        and se_response(0.93)[1] is False)
    chk('★ σ_max < σ_y 0.30 — SE 혼자 target 0.30 도달 불가 (하중분담 항이 필수인 근거)',
        REAL14_SE_CURVE[:, 1].max() < 0.30)
    chk('곡선이 φ 로 단조 비감소 (S-커브: jamming 0 → 상승 → σ_y 포화)',
        all(REAL14_SE_CURVE[i, 1] <= REAL14_SE_CURVE[i + 1, 1] + 1e-12
            for i in range(len(REAL14_SE_CURVE) - 1)))
    chk('선형 보간이 측정 11점을 정확히 재현',
        all(abs(se_response(float(x))[0] - float(y)) < 1e-12 for x, y in REAL14_SE_CURVE))
    chk('φ_SE_local = V_SE/(A·h − V_AM)',
        abs(phi_se_local(30.22, 46679.9, 17190.8, 2500.0) - 0.5955) < 5e-4)
    # 베드를 통째로 k 배 (h→k·h, 부피→k·배) 하면 φ 는 정확히 불변 → 같은 응력이 나와야 한다.
    # 이게 곡선이 두께 30µm 베드에서 113µm 베드로 **옮겨갈 수 있는** 근거다.
    _k = 3.74
    chk('★ 베드를 4배 키워도 같은 조밀도면 같은 응력 (곡선이 베드를 옮겨간다)',
        abs(se_response(phi_se_local(30.22 * _k, 46679.9 * _k, 17190.8 * _k, 2500.0))[0]
            - se_response(phi_se_local(30.22, 46679.9, 17190.8, 2500.0))[0]) < 1e-9)
    chk('두께만 늘리고 부피를 그대로 두면 φ 가 떨어져 응력도 떨어진다 (자명하지 않은 방향)',
        se_response(phi_se_local(30.6, 46679.9, 17190.8, 2500.0))[0]
        < se_response(phi_se_local(30.22, 46679.9, 17190.8, 2500.0))[0])

    # 하중평형: H_AM 이 크면 더 느슨한(두꺼운) 높이에서 멈춘다 = 압력 의존이 살아있다
    cc = np.array([[0.0, 0.0, 27.0 + 0.02 * i] for i in range(200)])
    rr = np.full(200, 1.5)
    _clo, _chi = 28.0, float((cc[:, 2] + rr).max())
    h1, _, _ = solve_height(cc, rr, 50.0, 2.0, 0.30, _clo, _chi)
    h2, _, _ = solve_height(cc, rr, 50.0, 6.0, 0.30, _clo, _chi)
    chk('H_AM 이 크면 더 두꺼운 높이에서 정지', h2 > h1)
    hp1, _, _ = solve_height(cc, rr, 50.0, 4.0, 0.10, _clo, _chi)
    hp2, _, _ = solve_height(cc, rr, 50.0, 4.0, 0.60, _clo, _chi)
    chk('압력이 높으면 더 얇은 높이에서 정지 (Heckel 방향)', hp2 < hp1)
    chk('압력 의존이 실재 — 100 vs 600 MPa 두께 차 > 0.1µm', (hp1 - hp2) > 0.1)

    # 역산은 정방향과 일관 (같은 H_AM 을 돌려줘야 한다)
    hstar, _, _ = solve_height(cc, rr, 50.0, 4.0, 0.30, _clo, _chi)
    hb, _, _ = invert_h_am(cc, rr, 50.0, hstar, 0.30)
    chk('역산 H_AM 이 정방향과 일치', abs(hb - 4.0) < 0.02)

    # ★ 단일-베드 경로 회귀 (2026-08-05): --invert/--sweep-p 가 v_am/v_se 를 안 넘겨
    #   φ_SE_local=0 → SE 항이 통째로 사라지던 버그.  φ 를 제대로 주면 0 이 아니어야 한다.
    _vam = float((4.0 / 3.0 * np.pi * rr ** 3).sum())        # 위 합성 베드(r=1.5, 200개)
    _vse = _vam * 0.35                                        # 임의의 SE 부피
    _h0 = 29.0
    chk('★ 단일-베드: v_am/v_se 를 주면 φ>0 이고 SE 항이 살아있다',
        phi_se_local(_h0, _vam, _vse, 2500.0) > 0
        and invert_h_am(cc, rr, 50.0, _h0, 0.30, REAL14_SE_CURVE, _vam, _vse)[2] >= 0.0)
    chk('★ v_am/v_se 없이 호출하면 φ=0 → SE 항 0 (옛 버그의 서명 — 기본값 의존 금지)',
        phi_se_local(_h0, 0.0, 0.0, 2500.0) == 0.0
        and se_response(0.0) == (0.0, True))

    # 관례: union 은 sphere 보다 항상 크다(= 고체를 적게 세므로) — 부호 회귀 방지
    pu, ps = porosities(30.28, 25.170, 25.548)
    chk('union porosity > sphere porosity (같은 높이)', pu > ps)

    # ── 비순환 검증 판정기 (--cases) ────────────────────────────────────────────────
    # 합성 베드: 같은 기하를 여러 압력에 걸어 "진짜 상수 H_AM" 을 심어두고 회수되는지 본다.
    import os
    import tempfile
    td = tempfile.mkdtemp(prefix='albj_')
    amp = os.path.join(td, 'am.csv')
    with open(amp, 'w') as f:
        for i in range(200):
            f.write(f'1,{0.000003 * (i % 16)},{0.000003 * (i // 16)},'
                    f'{(27.0 + 0.02 * i) / UM_PER_LU},{1.5 / UM_PER_LU}\n')
    am_c, am_r, _ = read_scaffold(amp)
    _LO, _HI = 28.0, float((am_c[:, 2] + am_r).max())     # main 과 같은 규약: hi = 최고점
    H_TRUE = 4.0
    man = os.path.join(td, 'cases.csv')
    with open(man, 'w') as f:
        f.write('label,p_gpa,am_csv,se_csv,h_dem_um\n')
        for p in (0.10, 0.30, 0.60):
            h, _, st = solve_height(am_c, am_r, 50.0, H_TRUE, p, _LO, _HI)
            chk(f'합성 베드가 P={p:g} 에서 내부 해를 가진다', st == 'ok')
            f.write(f'P{int(p * 1000)},{p},am.csv,am.csv,{h:.6f}\n')
    rows, summ = run_cases(read_cases(man))
    chk('매니페스트가 케이스 3개를 읽는다', len(rows) == 3)
    chk('심어둔 H_AM 을 케이스마다 회수 (역산 ↔ 정방향 일관)',
        all(abs(r['hm'] - H_TRUE) < 0.05 for r in rows))
    chk('진짜 상수면 흩어짐 ≈ 0 → PASS 판정', summ['spread'] < 0.02 and summ['verdict'].startswith('PASS'))
    chk('상대경로를 매니페스트 위치 기준으로 푼다', os.path.isabs(read_cases(man)[0]['am']))

    # 압력에 따라 H_AM 이 실제로 드리프트하는 베드는 PASS 가 아니라 DRIFT 로 잡혀야 한다
    man2 = os.path.join(td, 'cases_drift.csv')
    with open(man2, 'w') as f:
        f.write('label,p_gpa,am_csv,se_csv,h_dem_um\n')
        for p, hh in ((0.10, 2.5), (0.30, 4.0), (0.60, 6.4)):
            h, _, _ = solve_height(am_c, am_r, 50.0, hh, p, _LO, _HI)
            f.write(f'P{int(p * 1000)},{p},am.csv,am.csv,{h:.6f}\n')
    _, s2 = run_cases(read_cases(man2))
    chk('P 에 단조 의존하는 H_AM 은 DRIFT 로 진단', s2['verdict'].startswith('DRIFT'))
    chk('DRIFT 의 Meyer 기울기가 양수로 회수', s2['slope'] > 0.3

        )
    # 판정이 결과를 보고 흔들리지 않게 — 문턱은 인자로 고정되어 있어야 한다
    _, s3 = run_cases(read_cases(man), tol_frac=0.0)
    chk('문턱을 0 으로 조이면 같은 데이터라도 PASS 가 아니다',
        not s3['verdict'].startswith('PASS'))

    # 베드별 SE 응답곡선 주입 (다른 조성은 다른 곡선을 써야 한다)
    cp = os.path.join(td, 'curve.csv')
    open(cp, 'w').write('# h_um,wallP_GPa\n30.0,0.005\n28.0,0.050\n')
    cc2 = read_curve(cp)
    chk('응답곡선 CSV 는 두께 내림차순으로 정규화', cc2[0, 0] > cc2[-1, 0])
    chk('주입한 곡선이 se_response 에 실제로 쓰인다',
        abs(se_response(30.0, cc2)[0] - 0.005) < 1e-12)

    # ★ 판정력 검사가 실제로 VACUOUS 를 잡는가 — 오늘의 사고를 회귀 테스트로 박는다
    man3 = os.path.join(td, 'cases_vac.csv')
    with open(man3, 'w') as f:
        f.write('label,p_gpa,am_csv,se_csv,h_dem_um\n')
        h, _, _ = solve_height(am_c, am_r, 50.0, 4.0, 0.30, _LO, _HI)
        f.write(f'thin,0.30,am.csv,am.csv,{h:.6f}\n')
        f.write(f'thick,0.30,am.csv,am.csv,{h:.6f}\n')
    sc = scan_h_am(read_cases(man3))
    chk('판정력 검사가 넓은 통과 밴드를 VACUOUS 로 잡는다',
        sc['ratio'] > VACUOUS_BAND_RATIO and sc['verdict'].startswith('VACUOUS'))
    sc2 = scan_h_am(read_cases(man3), med_tol=1e-6, max_tol=1e-6)
    chk('문턱을 극단으로 조이면 밴드가 좁아지거나 FAIL', not sc2['verdict'].startswith('VACUOUS'))

    # ── 베드-전이 가드 (2026-08-06 기각 이후) ──────────────────────────────────
    _CURVE_BED_WARNED.clear()
    chk('곡선을 잰 베드(real_14)에는 경고 없음',
        assert_curve_bed('input_real_14') is False
        and assert_curve_bed('real_14_P300') is False)
    chk('다른 베드에는 경고', assert_curve_bed('kit_ps_7_3') is True)
    chk('경고는 케이스당 한 번 (배치 출력 보호)', assert_curve_bed('kit_ps_7_3') is False)
    chk('--quiet 로 억제 가능', assert_curve_bed('kit_ps_5_5', quiet=True) is False)
    _CURVE_BED_WARNED.clear()

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
    ap.add_argument('--cases', default='',
                    help='★ 비순환 검증: 케이스 매니페스트 CSV '
                         '(label,p_gpa,am_csv,se_csv,h_dem_um[,curve_csv,box_um]).  '
                         '케이스마다 H_AM 을 역산해 **하나의 상수로 수렴하는지** 판정한다')
    ap.add_argument('--h-am-scan', action='store_true',
                    help='★ 판정력 검사 — H_AM 을 흔들어 **통과 밴드**를 낸다.  밴드가 3배를 '
                         '넘으면 그 PASS 는 정보가 아니다 (VACUOUS)')
    ap.add_argument('--forward', action='store_true',
                    help='★ --cases 를 **정방향**으로 판정 (H_AM 고정 → 두께 예측 → DEM 대조). '
                         '역산은 자유표면에서 조건이 나빠 두께 정의 오차를 배수로 증폭한다')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)

    if a.selftest:
        return _selftest()

    if a.cases and a.h_am_scan:
        cs = read_cases(a.cases)
        print('★ 판정력 검사 — H_AM 을 얼마나 틀려도 통과하는가\n')
        print(f'{"H_AM(GPa)":>10} {"median|Δh|/h":>13} {"max":>8}   판정')
        for H in H_AM_GRID:
            _, s1 = run_forward(cs, h_am=H)
            print(f'{H:10g} {s1["median"]:13.2%} {s1["max"]:8.2%}   '
                  f'{"PASS" if s1["verdict"].startswith("PASS") else "fail"}')
        sc = scan_h_am(cs)
        if sc['passed']:
            print(f'\n  통과 밴드: {sc["lo"]:g}~{sc["hi"]:g} GPa  ({sc["ratio"]:.0f}배)')
        print(f'\n  ▶ {sc["verdict"]}')
        return 0

    if a.cases and a.forward:
        rows, summ = run_forward(read_cases(a.cases), h_am=a.h_am)
        print(f'★ 정방향 검증 — H_AM = {summ["h_am"]:g} GPa 고정(문헌), 두께를 예측해 DEM 과 대조')
        print('   사전등록 문턱: median |Δh|/h ≤ 1.5 %  그리고  max ≤ 4 %\n')
        print(f'{"label":>24} {"P(GPa)":>7} {"h_DEM":>8} {"h_pred":>8} {"Δh(µm)":>8} '
              f'{"|Δh|/h":>7} {"Δε(%p)":>8} {"A_supp":>7} {"SE(GPa)":>8}')
        for r in rows:
            print(f'{r["label"]:>24} {r["p"]:7.3f} {r["h_dem"]:8.2f} {r["h"]:8.2f} '
                  f'{r["dh"]:+8.2f} {r["rel"]:7.2%} {r["de"]:+8.2f} {r["a"]:7.2%} '
                  f'{r["s"]:8.4f}'
                  + ('' if r['inside'] else '  ⚠SE외삽')
                  + ('' if r['status'] == 'ok' else f'  ⚠{r["status"]}'))
        print(f'\n  median |Δh|/h = {summ["median"]:.2%}   ·   max = {summ["max"]:.2%}')
        if summ['n_outside']:
            print(f'  ⚠ SE 응답곡선 밖 {summ["n_outside"]}/{len(rows)} 케이스 — '
                  f'그 행의 SE 항은 신뢰구간 밖')
        print(f'\n  ▶ {summ["verdict"]}')
        print('\n  Δh 는 **관례 무관**(두께엔 sphere/union 구분 없음) — 이 검증은 오늘의 '
              '1.25 %p\n  관례 함정을 비껴간다.  Δε 는 sphere 관례 환산 참고값.')
        return 0

    if a.cases:
        cases = read_cases(a.cases)
        rows, summ = run_cases(cases)
        print(f'비순환 검증 — 케이스 {len(rows)}개, 케이스별 H_AM 역산\n')
        print(f'{"label":>14} {"P(GPa)":>7} {"h_DEM(µm)":>10} {"A_supp":>8} {"SE(GPa)":>8} '
              f'{"SE/P":>6} {"H_AM(GPa)":>10}')
        for r in rows:
            print(f'{r["label"]:>14} {r["p"]:7.3f} {r["h"]:10.2f} {r["a"]:8.2%} {r["s"]:8.4f} '
                  f'{r["s"] / r["p"]:6.1%} {r["hm"]:10.2f}'
                  + ('' if r['inside'] else '   ⚠SE외삽'))
        print(f'\n  중앙값 H_AM = {summ["median"]:.2f} GPa   '
              f'(문헌대 3~6 GPa {"안 ✓" if summ["in_band"] else "밖 ✗"})')
        print(f'  흩어짐 (max−min)/median = {summ["spread"]:.1%}   '
              f'(사전등록 문턱 25 %)')
        if np.isfinite(summ['slope']):
            print(f'  압력 의존 log-log 기울기  H ∝ P^{summ["slope"]:+.3f}   '
                  f'(0 이면 순수 재료상수)')
        print(f'\n  ▶ {summ["verdict"]}')
        print('\n  ⚠ 케이스가 모두 같은 압력이면 이것은 **조성 축** 검증이고, 압력 축은 '
              '검증되지 않는다.\n     Heckel 을 주장하려면 같은 베드의 다압력 DEM 두께가 필요하다.')
        return 0

    if not a.am or not a.se:
        ap.error('--am 과 --se 가 필요합니다 (또는 --selftest)')

    am_c, am_r, am_t = read_scaffold(a.am)
    se_c, se_r, _ = read_scaffold(a.se)
    A = a.box_um ** 2

    # 고체 부피 — 두 관례.  sphere = 구 부피 합(겹침 이중계상, DEM 정본).
    # union 은 렌즈 겹침을 빼서 근사한다 (SE-SE + AM-SE; 삼중 겹침은 무시 = 상한).
    v_am_sph = float((4.0 / 3.0 * np.pi * am_r ** 3).sum())
    v_se_sph = float((4.0 / 3.0 * np.pi * se_r ** 3).sum())
    v_sph = v_am_sph + v_se_sph

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
        # ★ v_am/v_se 필수 — 없으면 φ_SE_local=0 이 되어 SE 항이 통째로 사라진다
        #   (2026-08-05: 11점 곡선 도입 후 이 경로가 옛 두께-색인 시그니처로 남아 있던 버그)
        hb, asup, sse = invert_h_am(am_c, am_r, a.box_um, a.dem_thickness, a.p_target,
                                    REAL14_SE_CURVE, v_am_sph, v_se_sph)
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
        h, pach, st = solve_height(am_c, am_r, a.box_um, a.h_am, p, lo, hi,
                                   v_am_sph, v_se_sph)
        asup = support_fraction(am_c, am_r, h, a.box_um)
        sse, inside = se_response(phi_se_local(h, v_am_sph, v_se_sph, A))
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
