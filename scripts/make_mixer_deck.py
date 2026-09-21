#!/usr/bin/env python3
"""믹싱 드럼 덱 생성기 — 조성에서 치수·개수·섬유파일을 **유도**한다.

왜 생성기인가
  치수가 조성에서 유도된다 (부피분율 → 개수비 → 드럼 크기).  손으로 적으면
  조성을 바꿀 때마다 틀린다.  `docs/reviews/mixing_model_design_20260919.md` §11 의
  계산을 그대로 코드로 옮긴 것이다.

⚠⚠ 생산 압축 덱의 `scale=1000` 규약을 **쓰지 않는다**.
  그 규약은 `E_sim = E_real/scale` · `R_sim = R_real×scale` 이라 접촉력은 `scale¹`,
  중력은 `scale³` 로 스케일된다 ⇒ 중력/접촉 비가 `scale²` 만큼 틀어진다.
  압축 덱은 **플래튼 구동**이라 중력이 무시돼 무해했지만 **드럼은 중력 구동**이다.
  ⇒ 대신 문헌 방식(`lischka`·`hare`)을 쓴다: **coarse-graining(CGF) + 중력 실제값 유지**,
  점착은 무차원수 보존으로 재보정(⬜ `D11`, 지수 미측정).

⚠ 전단탄성률을 낮춘다 — `lischka` 가 *"계산비용 때문에 G=1e8 로 낮췄다, 물성이 아니다"*
  라고 명시한 것과 같은 조작이고, 튜토리얼 `Mixer` 도 `E=1e7` 을 쓴다.
  ⇒ **탄성 물성으로 인용 금지.**

usage
  python3 scripts/make_mixer_deck.py --out dem_scripts/mixer_20260919 --n-total 50000
  python3 scripts/make_mixer_deck.py --selftest
"""
import argparse
import math
import os
import sys

#: 밀도 (g/cm³) — `scripts/additives.py` 정본과 같은 값.  여기서 다시 적는 이유는
#  이 생성기가 리포 밖(1저자 WSL)에서도 단독으로 돌 수 있어야 하기 때문이다.
DENS = {'AM': 4.80, 'SE': 2.00, 'VGCF': 2.00, 'PTFE': 2.20}
#: 1저자 지시 조성 (2026-09-19) — 에너지밀도 최대 조합
WT = {'AM': 80.0, 'SE': 18.0, 'VGCF': 1.0, 'PTFE': 1.0}
PS = (7.0, 3.0)                       # P:S (wt%)
#: **모델이 실제로 쓰는** 지름 (µm) — 이 표가 유일한 출처다.
#  ⚠⚠ 2026-09-21 이전 판은 이 표에 `SE 1.0` 을 적어 놓고 **쓰지 않았다**.  지름은
#    `AM_P` 만 읽고 나머지는 `dP/3` · `dP×0.25` 로 깎았다.  AM_P 12 에서 우연히
#    `AM_S 4` 는 맞았지만 `SE` 는 실제로 **3 µm** 였다 = **선언과 사용이 갈린 표**.
#    AM_P 를 바꾸는 순간 나머지가 조용히 따라 움직이는 구조였다.  ⇒ 전 상을 여기서 읽는다.
#  ★ AM_P 9 · AM_S 4 는 **소재 실측** (1저자, 2026-09-21).  AM_S 는 단결정이다.
#  ⚠ SE·VGCF·PTFE 의 값은 **소재 크기가 아니라 계산비용 바닥**이다 — 실제 SE 는 1 µm,
#    VGCF 지름은 0.15 µm 다 (`CL-66`).  1 µm 로 풀면 SE 입자가 11배(≈67,000)로 늘고
#    `dt` 가 0.44배라 비용이 **약 19배**가 된다 (층상 한 블록 6.5 h → 5일).  ⇒ 굵힌 채로
#    가되 **굵혔다는 것을 표가 말하게** 둔다.  이 값들을 "소재 크기" 로 인용하지 말 것.
D_REAL_UM = {'AM_P': 12.0, 'AM_S': 4.0, 'SE': 3.0, 'VGCF': 3.0, 'PTFE': 3.0}
L_FIB_UM = 10.0                       # ⚠ VGCF 길이.  PTFE 길이는 출처 없음 (`CL-67`)
#: 타입 순서 — 덱의 `peratomtypepair` 행렬 순서와 같아야 한다
TYPES = ('AM_P', 'AM_S', 'SE', 'VGCF', 'PTFE')
#: 점착 원점 (J/m³) — 튜토리얼 `cohesion` 예제값.  ⚠ 우리 소재의 물성이 아니다.
#  ── 점착 눈금 — **CED(J/m³) 가 아니라 Bond 수로 건다** (2026-09-19 실측으로 갈아엎음) ──
#
# ⛔ 초판은 `CED0 = 3.0e5` 에 ×1/×10/×100 을 걸었다.  **5 팔 중 4 팔이 접촉모델 밖으로
#    나갔다** (`scripts/check_contact_validity.py` 로 실측):
#        E0 CED 0     겹침 중앙 0.09 %              손실 0 %      ✓
#        E1 3e5 균일  겹침 중앙 3.50 %              손실 0 %      ⚠
#        E2 AM 3e6    겹침 **최대 196 %**           손실 4.8 %    ⛔ (KE 가 안 떨어짐)
#        E3 SE 3e6    겹침 중앙 **55 %**            손실 **63 %** ⛔
#        E4 AM 3e7    겹침 최대 197 %               손실 28.7 %   ⛔
#    δ/r = 1.97 은 한 구의 중심이 상대 구 **반대편 바깥**에 있다는 뜻 = 겹침이 아니라 통과.
#
# ★ 왜 그랬나 — **SJKR 은 겹침에 선형, Hertz 반발은 δ^1.5** 다.
#       (4/3)·E*·√R*·δ^1.5  =  W + CED·2π·R*·δ
#    점착 지배 극한에서 `δ = (3·CED·2π·√R* / (4E*))²` ⇒ **δ ∝ CED²**.
#    ⇒ CED 를 ×10 하면 겹침이 **×100**.  ×1/×10/×100 사다리는 겹침으로 ×1/×100/×10⁴ 다.
#    ★ 이 식이 실측을 맞힌다 — 예측 3.3~3.5 % vs E1 실측 중앙 **3.50 %**.
#      ⚠ 초판은 3.54 % 라 적었다 — 섬유 **자기 겹침**(설계상 δ/r = 0.4)이 섞인 값이다.
#        `MIX-05` 로 고쳤고, 고친 값이 예측에 **더 가깝다**.
#
# ★ 그리고 F_coh ∝ CED·δ ∝ **CED³** 이므로 Bond 수도 CED³ 다.
#    ⇒ 물리 눈금(Bo)에서 고르게 놓으려면 **CED ∝ Bo^(1/3)** 로 걸어야 한다.
#    ⇒ Bo = F_coh/W ∝ CED³/(R·ρ·E*²) — 같은 CED 라도 **작고 가벼운 상이 훨씬 점착적**이다
#      (CED 1.65e5 에서 AM_P 23 · AM_S 70 · SE 210).  그래서 **상마다 CED 를 다르게** 준다.
#    ⚠ 겹침은 그렇지 않다 — 같은 CED 에서 `δ/r` 은 **반경과 무관**하다 (ν 만 다르다).
#      ⇒ 두 축이 따로 논다: **Bo 는 크기에 민감하고 겹침은 아니다.**  섞지 말 것.
#      이것이 설계문서 §11-5 의 열린 질문 `D11`(CG 하면 점착을 어떻게 다시 주나)에 대한
#      SJKR+Hertz 계의 유도 답이다.
#
# ⚠⚠ 한정어를 지우지 말 것 — 이 유도는 ① **점착 지배 극한**(무게항 무시)이고
#    ② **단일 접촉**이다.  침대에서는 입자가 묻혀 접촉이 여럿이다.  CED 3e5 에서
#    예측이 맞았다고 낮은 CED 에서도 맞는다는 뜻이 아니다 (거기선 무게항이 지배한다).
#    ⇒ **모든 팔은 돌린 뒤 `check_contact_validity.py` 로 확인한다.**  식은 사다리를
#      고르는 도구이지 유효성의 증명이 아니다.

OVL_CEILING = 0.01          # 겹침 천장 δ/r — DEM 연질구 관례 1 %
#: 상별 (반경 m, 포아송비, 밀도 g/cm³) — 덱의 `property/global` 과 같아야 한다
PHASE_MECH = {'AM_P': (0.25, 'AM'), 'AM_S': (0.25, 'AM'), 'SE': (0.30, 'SE'),
              'VGCF': (0.30, 'VGCF'), 'PTFE': (0.30, 'PTFE')}
E_YOUNG = 1.0e7             # Pa — 계산비용용 연화값.  ⚠ 물성 인용 금지


def _estar(nu):
    return E_YOUNG / (2.0 * (1.0 - nu ** 2))


def overlap_for_ced(ced, radius, nu):
    """CED → 평형 겹침 `δ/r` (점착 지배 극한).  ★ 실측 검증: 3e5·SE → 3.31 % vs 3.54 %."""
    if ced <= 0:
        return 0.0
    rs = radius / 2.0                                   # 같은 크기 두 구의 R*
    return (3.0 * ced * 2.0 * math.pi * math.sqrt(rs) / (4.0 * _estar(nu))) ** 2 / radius


def bond_for_ced(ced, radius, nu, rho_gcc, g=9.81):
    """CED → Bond 수 `F_coh / W`.  **∝ CED³** 이다."""
    if ced <= 0:
        return 0.0
    rs = radius / 2.0
    delta = overlap_for_ced(ced, radius, nu) * radius
    f_coh = ced * 2.0 * math.pi * rs * delta
    w = (4.0 / 3.0) * math.pi * radius ** 3 * (rho_gcc * 1000.0) * g
    return f_coh / w


def ced_for_bond(bo, radius, nu, rho_gcc, g=9.81):
    """목표 Bond 수 → CED.  `Bo ∝ CED³` 이므로 한 점에서 세제곱근으로 뽑는다."""
    if bo <= 0:
        return 0.0
    ref = 1.0e5
    return ref * (bo / bond_for_ced(ref, radius, nu, rho_gcc, g)) ** (1.0 / 3.0)


#: 팔 — **Bond 수 배수**를 건다 (CED 배수가 아니다).  나머지는 전부 고정.
#  `mult[(a,b)]` 가 없으면 1.0.  대칭은 코드가 강제한다.
#  ★ 기준 Bond 수는 **천장에서 거꾸로 푼다** — 손으로 박지 않는다.
#    초판은 `CED0 = 3.0e5` 를 박았고 4/5 팔이 접촉모델 밖으로 나갔다.  여기서는
#    `_solve_bond0()` 가 **가장 센 팔이 겹침 천장에 딱 닿도록** 잡으므로, 나중에
#    ×1000 팔을 더해도 사다리 전체가 자동으로 내려앉는다 (시험 ㉙ 가 강제한다).
ARMS = {
    'E0': dict(desc='음성 대조 — 점착 0.  지표가 0 을 내는가', bond=0.0, mult={}),
    'E1': dict(desc='균일 Bo=1 (상별 CED 는 다르다 — 그래야 Bo 가 같다)',
               bond=1.0, mult={}),
    'E2': dict(desc='★ AM 만 Bo ×10 — 1저자 질문의 축', bond=1.0,
               mult={('AM_P', 'AM_P'): 10., ('AM_P', 'AM_S'): 10., ('AM_S', 'AM_S'): 10.}),
    'E3': dict(desc='SE 만 Bo ×10 (대조)', bond=1.0, mult={('SE', 'SE'): 10.}),
    'E4': dict(desc='AM 만 Bo ×100 (축 확장)', bond=1.0,
               mult={('AM_P', 'AM_P'): 100., ('AM_P', 'AM_S'): 100., ('AM_S', 'AM_S'): 100.}),
    #  ★★ 코팅 — **AM 표면이 황화물(SE)이 된다** (1저자 질문, 2026-09-20)
    #  코팅은 **닿는 면을 바꾼다**: 코팅된 AM 끼리의 접촉은 `SE 표면 ↔ SE 표면` 이다.
    #  ⇒ AM-AM 쌍의 CED 를 **SE-SE 쌍의 값으로 덮는다**.
    #  ⚠ 바꾸는 것은 **표면 물성(CED)** 이지 Bond 수가 **아니다** — 코팅층은 얇아
    #    입자의 크기·질량이 안 바뀌므로 `Bo = F_coh/W` 는 **따라 나오게** 둬야 한다.
    #    (Bo 를 SE 와 같게 맞추면 코팅이 입자를 가볍게 만든 셈이 되어 틀린다.)
    #  ⚠ AM-SE 쌍은 이미 SE 값이다 (`min(cand)` 규약) — 코팅해도 그대로다.
    #  ⛔ **피복률(patchy)은 축에 없다** — 1저자 지시 2026-09-20: *"피복률까지 넣으면
    #    계산이 복잡해진다.  이 전극이 더 잘 믹싱되는지만 보고 싶다"*.
    #    ⇒ 이 팔은 **완전 피복**을 뜻한다.  부분 피복은 이 결과와 무피복 사이에 있다.
    'C1': dict(desc='★ AM 에 황화물 코팅 — AM 표면이 SE 가 된다 (완전 피복)',
               bond=1.0, mult={}, coat={'AM_P': 'SE', 'AM_S': 'SE'}),
    #  ★★ 고-G 믹서 (Thinky · 볼텍스) — **중력을 올리지 않고 Bo 를 내린다**
    #  1저자 정정 2026-09-20: 우리 영률 1e7 은 임의 연화가 아니라 **스케일 팩터**다
    #  (압축 덱이 300 MPa·E_real 을 0.3 MPa·E/1000 으로 내려 `P/E` 를 보존한 것).
    #  ⇒ 중력만 268배 올리고 E 를 그대로 두면 `P/E` 가 268배가 되어 **그 규약을 깬다**.
    #    실측: Π₁ = ρaR/E 가 5.7e-6 → 1.5e-3, 찌그러짐 0.032 % → 1.32 %.
    #    실제 Thinky 안의 NCM 은 Π₁ 5.4e-10 = **거의 강체**이므로 중력을 올리면
    #    **실제에서 오히려 멀어진다**.
    #  ★ 믹서의 물리를 정하는 무차원수는 둘뿐이다:
    #      Fr = ω²R/a   (유동 영역)     Bo = F_점착/(m·a)   (점착 지배도)
    #    Fr 은 이미 맞다 — Thinky 컵프레임 0.055~0.086 vs 우리 드럼 60 rpm 0.083.
    #    ⇒ **Bo 만 1/G 로 내리면 같은 물리다.**  그리고 Bo 는 CED 로 내릴 수 있어
    #      겹침이 **더 작아진다** (δ ∝ CED²) = 접촉모델이 더 안전해지고 비용은 0.
    #  ⚠ 이 팔들은 `E4` 의 재료(끈적한 맨 AM)를 **그 기계에서** 섞는 것이다.
    'T1': dict(desc='★ Thinky 268 G 에서 본 E4 (Bo 를 268 로 나눈다)',
               bond=1.0 / 268.0,
               mult={('AM_P', 'AM_P'): 100., ('AM_P', 'AM_S'): 100., ('AM_S', 'AM_S'): 100.}),
    'T2': dict(desc='볼텍스 45 G 에서 본 E4 (Bo 를 45 로 나눈다)',
               bond=1.0 / 45.0,
               mult={('AM_P', 'AM_P'): 100., ('AM_P', 'AM_S'): 100., ('AM_S', 'AM_S'): 100.}),
    #  ★★ 경계 탐침 — 측정된 점 사이가 **비어 있다**
    #    Bo 0.212 → H/R 1.573 (깨끗)  ·  Bo 2.124 → 2.020 (뭉침)
    #    그 사이 **10배 구간**에 경계가 있는데 아무것도 안 찍었다.  경계를 모르면
    #    코팅(0.0235)·볼텍스(0.07)·Thinky(0.012) 의 **여유 배수**를 말할 수 없다.
    #  ⚠ AM 쌍에만 배수를 건다 — E2·E4 와 같은 구조여야 비교가 한 축이다.
    #    배수 = 목표Bo / BOND0(0.2124),  그리고 Bo ∝ 배수 (BOND0 이 이미 Bo 단위다).
    'B5': dict(desc='경계 탐침 — AM Bo 0.5', bond=1.0,
               mult={('AM_P', 'AM_P'): 0.5 / 0.21244, ('AM_P', 'AM_S'): 0.5 / 0.21244,
                     ('AM_S', 'AM_S'): 0.5 / 0.21244}),
    'B10': dict(desc='경계 탐침 — AM Bo 1.0', bond=1.0,
                mult={('AM_P', 'AM_P'): 1.0 / 0.21244, ('AM_P', 'AM_S'): 1.0 / 0.21244,
                      ('AM_S', 'AM_S'): 1.0 / 0.21244}),
    #  ★★ §24 (2026-09-20) — **층상 시작**.  1저자 비준: 헤드라인은 *"코팅하면 더 잘 섞이나"*.
    #  삽입만 두 층으로 나눈다 (아래 AM · 위 SE+VGCF+PTFE); 나머지는 전부 그대로.
    #  ⚠ 점착이 걸리는 상(AM)을 **아래**에 둔다 — 깨져야 하는 층을 통째로 두고 시작한다.
    #    반대로 두면 작은 SE 가 큰 AM 틈으로 체질돼 내려가는 것이 "혼합" 으로 읽힌다 (교락).
    #  ⚠ 새 팔의 배수는 E4(100) 보다 작아야 BOND0 이 안 밀린다 — 셀프테스트 ㉞ 가 단언한다.
    'L0': dict(desc='§24 층상 · 점착 0 — 지표 상한 (음성 대조)', bond=0.0, mult={},
               layered=True),
    'LA': dict(desc='§24 층상 · 무코팅 AM Bo 3.0 = 문헌 앵커 (hare2026) — 헤드라인 무코팅',
               bond=1.0, layered=True,
               mult={('AM_P', 'AM_P'): 3.0 / 0.21244, ('AM_P', 'AM_S'): 3.0 / 0.21244,
                     ('AM_S', 'AM_S'): 3.0 / 0.21244}),
    'LC': dict(desc='§24 층상 · 코팅 (AM 표면 = SE, C1 규약) — 헤드라인 코팅',
               bond=1.0, mult={}, coat={'AM_P': 'SE', 'AM_S': 'SE'}, layered=True),
}


def _solve_bond0(d, ceiling=None):
    """모든 팔이 겹침 천장 안에 들도록 기준 Bond 수를 푼다.

    겹침은 `Bo^(2/3)` 에 비례하므로 가장 센 팔·가장 무른 상에서 닫힌형으로 나온다.
    ⚠ 천장 1 % 는 **관례**다.  실측으로는 δ/r 3.54 % 인 팔이 원자 손실 0 · KE 정착
      으로 멀쩡했고, 무너진 팔은 중앙 40 % 였다 — **그 사이는 안 재봤다**.
      ⇒ 1 % 는 외삽하지 않는 쪽으로 고른 값이지 무너지는 경계가 아니다.
    ⚠ 그리고 이 식 자체가 점착 지배·단일 접촉 극한이다 (모듈 머리말 참조).
      ⇒ 고른 사다리는 돌린 뒤 `check_contact_validity.py` 로 **반드시** 확인한다.
    """
    ceiling = OVL_CEILING if ceiling is None else ceiling
    worst = 0.0
    for a in ARMS.values():
        if not a['bond']:
            continue
        for t in TYPES:
            nu, mat = PHASE_MECH[t]
            r = d[t] / 2.0
            #  이 상에 걸린 가장 큰 Bond 배수
            f = max([v for (x, y), v in a['mult'].items() if t in (x, y)] or [1.0])
            #  ⚠ `bond` 는 이제 0/1 이 아니라 **배율**이다 (고-G 팔이 1/268 을 쓴다).
            #    a['bond'] 를 안 곱하면 약한 팔을 강한 팔로 오해해 BOND0 이 잘못 풀린다.
            base = overlap_for_ced(ced_for_bond(1.0, r, nu, DENS[mat]), r, nu)
            worst = max(worst, base * (a['bond'] * f) ** (2 / 3.))
    return (ceiling / worst) ** 1.5 if worst > 0 else 0.0


def ced_matrix(arm, d):
    """팔 이름 + 상별 지름 → 5×5 `cohesionEnergyDensity` 행렬.  **대칭을 강제한다.**

    ⚠ 쌍 (i, j) 는 두 상의 목표 CED 중 **작은 쪽**을 쓴다 = 보수적인 쪽.
      ★ 왜 그게 보수적인가 — 같은 CED 에서 `δ/r` 은 **반경과 무관**하다
        (`δ ∝ R*` 이고 `δ/r` 에서 반경이 약분된다.  실측 검증: CED 3e5 에서
         AM_P 3.51 % · AM_S 3.51 % · SE 3.31 %, 차이는 ν 0.25↔0.30 뿐).
        따라서 **CED 가 낮은 쪽 = 겹침이 작은 쪽**이고 min() 이 곧 안전한 쪽이다.
      ★ 거꾸로 **같은 Bo** 에서는 `δ/r ∝ (R·ρ)^(2/3)` 이라 **크고 무거운 상이
        겹침을 더 먹는다** (Bo=1 에서 AM_P 0.130 % vs SE 0.028 %) ⇒ 천장을 정하는
        것은 AM_P 다.
      ⚠ 실측에서 SE 팔(E3)이 AM 팔(E4)보다 **낮은 CED 로 더 크게 무너진 것**은
        상별 민감도 때문이 **아니라** SE 가 침대의 73 % 라 잃은 원자가 많았기
        때문이다 (손실 63 % vs 28.7 %; 최대 겹침은 187 % vs 197 % 로 비슷하다).
        ⛔ 이 둘을 섞어 *"작은 상이 먼저 깨진다"* 고 적지 말 것.
      ★ min() 이라 (i, j) 와 (j, i) 가 **정의상 같다** — 초판은 `d[ti] <= d[tj]` 로
        골라 SE·VGCF·PTFE 처럼 **지름이 같고 밀도가 다른** 상 쌍에서 순서에 따라
        답이 갈렸고, 아래 대칭 단언이 그것을 잡았다.
    """
    a = ARMS[arm]
    n = len(TYPES)
    bond0 = _solve_bond0(d)
    M = [[0.0] * n for _ in range(n)]
    for i, ti in enumerate(TYPES):
        for j, tj in enumerate(TYPES):
            if a['bond'] <= 0:
                continue
            f = a['mult'].get((ti, tj), a['mult'].get((tj, ti), 1.0))
            cand = []                     # ★ 두 상의 목표 CED 중 작은 쪽 (위 설명)
            for t in (ti, tj):
                nu, mat = PHASE_MECH[t]
                cand.append(ced_for_bond(bond0 * a['bond'] * f,
                                         d[t] / 2.0, nu, DENS[mat]))
            M[i][j] = min(cand)
    #  ★ 코팅 — 코팅된 두 상이 닿으면 **둘 다 코팅재 표면**이므로 그 쌍의 CED 를
    #    코팅재끼리의 값으로 **덮는다**.  설계식을 다시 풀지 않고 **값을 복사**한다
    #    (그래야 "표면이 그 재료가 된다" 는 뜻이 그대로 담긴다).
    coat = a.get('coat') or {}
    if coat:
        for i, ti in enumerate(TYPES):
            for j, tj in enumerate(TYPES):
                si, sj = coat.get(ti, ti), coat.get(tj, tj)   # 실제 닿는 표면
                if (si, sj) != (ti, tj):
                    M[i][j] = M[TYPES.index(si)][TYPES.index(sj)]
    for i in range(n):                                # ★ 비대칭 입력을 막는다
        for j in range(i + 1, n):
            assert abs(M[i][j] - M[j][i]) < 1e-9, '행렬이 비대칭이다'
    return M


def volume_fractions():
    wt = {'AM_P': WT['AM'] * PS[0] / sum(PS), 'AM_S': WT['AM'] * PS[1] / sum(PS),
          'SE': WT['SE'], 'VGCF': WT['VGCF'], 'PTFE': WT['PTFE']}
    rho = {'AM_P': DENS['AM'], 'AM_S': DENS['AM'], 'SE': DENS['SE'],
           'VGCF': DENS['VGCF'], 'PTFE': DENS['PTFE']}
    v = {k: wt[k] / rho[k] for k in wt}
    tot = sum(v.values())
    return {k: v[k] / tot for k in v}, wt


def plan(n_total, cgf=200.0,
         fill=0.30, pack=0.60, drum_r_over_l=2.5, shear_mod=3.85e6, nu=0.25):
    """조성 → 개수 · 드럼 치수 · 시간스텝.  **순수 함수**라 시험 가능하다.

    ★ 지름은 전부 `D_REAL_UM` 에서 나온다 (비율 노브 없음).  옛 `d_se_over_am` ·
      `d_fib_over_am` 인자는 **삭제**했다 — 아무도 넘기지 않으면서 표를 무력화하고
      있었다 (선언 ≠ 사용).  셀프테스트 ㊵ 가 "표 = 사용" 을 강제한다.
    """
    phi, wt = volume_fractions()
    d = {k: D_REAL_UM[k] * 1e-6 * cgf for k in TYPES}        # m
    #  ⚠⚠ LIGGGHTS `particledistribution/discrete` 는 분율을 **mass%** 로 읽는다
    #    (실행으로 확인: 로그가 "distribution based on mass%" 를 먼저 찍고 number% 를 유도한다).
    #    초판은 개수분율을 넣어 AM_P 가 744 → **6개**로 들어갔다.
    #    ⇒ 우리 조성이 이미 wt% 이므로 **그대로 넣는다**.
    #  섬유 — 구 개수는 종횡비가 정한다 (길이는 CGF 로 같이 늘어난다)
    L_fib = L_FIB_UM * 1e-6 * cgf
    nsph = max(2, int(round(L_fib / d['VGCF'])))
    NSPH = {'AM_P': 1, 'AM_S': 1, 'SE': 1, 'VGCF': nsph, 'PTFE': nsph}
    rho_i = {'AM_P': DENS['AM'], 'AM_S': DENS['AM'], 'SE': DENS['SE'],
             'VGCF': DENS['VGCF'], 'PTFE': DENS['PTFE']}
    #  템플릿 1개의 질량 (섬유는 구 nsph 개)
    #  ★ 섬유는 구가 겹쳐 있어 nsph 개 합보다 가볍다 — 기하로 보정한다 (실측 +3.8 % 편향 제거)
    fac = {k: (chain_volume_factor(NSPH[k]) if NSPH[k] > 1 else 1.0) for k in d}
    m_tpl = {k: NSPH[k] * fac[k] * rho_i[k] * 1000.0 * (math.pi / 6) * d[k] ** 3 for k in d}
    massfrac = {k: wt[k] / 100.0 for k in wt}
    #  템플릿 개수비 = 질량분율 / 템플릿질량
    c = {k: massfrac[k] / m_tpl[k] for k in d}
    per = sum(c.values())
    #  `particles_in_region` 은 **템플릿** 수다.  목표는 원자 수로 준다.
    atoms_per_tpl = sum(c[k] / per * NSPH[k] for k in d)
    n_tpl_total = int(round(n_total / atoms_per_tpl))
    n_tpl = {k: int(round(n_tpl_total * c[k] / per)) for k in d}
    n = {k: n_tpl[k] * NSPH[k] for k in d}                    # 원자 수
    n_fib = {k: n_tpl[k] for k in ('VGCF', 'PTFE')}
    #  드럼 — 고체 부피에서 역산
    v_solid = n['AM_P'] * (math.pi / 6) * d['AM_P'] ** 3 / phi['AM_P']
    v_drum = v_solid / (fill * pack)
    R = (drum_r_over_l * v_drum / math.pi) ** (1 / 3.0)
    L = R / drum_r_over_l
    #  시간스텝 — Rayleigh 의 20 %, 가장 작은 입자·SE 밀도 기준
    d_small = min(d.values())
    rho_si = DENS['SE'] * 1000.0
    dt = 0.2 * math.pi * (d_small / 2) * math.sqrt(rho_si / shear_mod) \
        / (0.1631 * nu + 0.8766)
    rpm_crit = 60 / (2 * math.pi) * math.sqrt(9.81 / R)
    return dict(phi=phi, wt=wt, d=d, n=n, n_tpl=n_tpl, n_tpl_total=n_tpl_total,
                massfrac=massfrac, n_fib=n_fib, nsph=nsph, L_fib=L_fib,
                v_solid=v_solid, v_drum=v_drum, R=R, L=L, dt=dt,
                rpm_crit=rpm_crit, cgf=cgf, stl_scale=R / 0.5, n_total=sum(n.values()))


def chain_volume_factor(nsph, spacing_over_d=0.8):
    """겹친 구 사슬의 부피 / (구 부피 × nsph).

    ⚠ 이 보정이 없으면 섬유 질량을 **과대**평가해 LIGGGHTS 가 1 wt% 를 맞추려고
      가닥을 더 넣는다 (실측 +3.8 %).  등반경 렌즈 부피는 해석적이다:
        d = s·D,  δ = D − d,  V_lens = π δ²(d + 2D)/12
    """
    if nsph < 2:
        return 1.0
    D = 1.0
    d = spacing_over_d * D
    delta = D - d
    v_sph = (math.pi / 6) * D ** 3
    v_lens = math.pi * delta ** 2 * (d + 2 * D) / 12.0
    return (nsph * v_sph - (nsph - 1) * v_lens) / (nsph * v_sph)


def fibre_file(nsph, d_sph):
    """multisphere 구 파일 — `x y z radius` 한 줄씩 (튜토리얼 `stone1.multisphere` 형식).

    ⚠ 겹치게 둔다 (중심간 거리 = 0.8·d).  떨어뜨리면 강체가 아니라 염주가 된다.
    """
    step = 0.8 * d_sph
    x0 = -0.5 * step * (nsph - 1)
    return ''.join(f'{x0 + i*step:.8g} 0 0 {d_sph/2:.8g}\n' for i in range(nsph))


def settle_time(drop_m, restitution=0.3, g=9.81, margin=2.0):
    """정착 시간 — **유도값**이지 눈대중이 아니다.

    반발계수 e 의 공에서 튐의 총 시간은 등비급수로 `t_ff·(1+e)/(1−e)` 다.
    ★ 이 식이 실측을 맞힌다 — 튜토리얼 `cohesion` 대조쌍은 낙하 60 mm · e = 0.9 이고
      `t_ff = 0.111 s` 이므로 식이 **2.11 s** 를 준다.  실제로 250,000 step(2.5 s)
      에서 정착했고 50,000 step(0.5 s = 정착의 24 %)에서는 지표가 **부호까지 반대**로
      나왔다.  ⇒ `steps_fill = 20000` 같은 **상수는 쓰지 않는다**.
    ⚠ 이 식은 홑 입자의 튐만 센다.  무리의 재배열은 더 걸리므로 `margin` 을 곱하고,
      그래도 맞았는지는 `measure_bed_aspect.py` 의 φ(포락) 경고로 **반드시 확인**한다.
    """
    t_ff = math.sqrt(2.0 * drop_m / g)
    return margin * t_ff * (1.0 + restitution) / (1.0 - restitution)


def _next_prime(n):
    """n 이상의 첫 소수 — 층상 삽입의 둘째 insert/pack·pdd 시드용 (둘 다 소수여야 한다)."""
    n = int(n)
    while not _is_prime(n):
        n += 1
    return n


def _is_prime(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True


def deck(p, rpm, revolutions, seed=32452843, arm='E1', settle_s=None, layered=None,
         restitution=0.3, n_baffles=0, baffle_h=0.10):
    #  ⚠⚠ LIGGGHTS 의 `fix insert/pack` 시드는 **소수여야 한다**.
    #    합성수를 주면 런이 `random.cpp:93` 에서 **죽는다** — 그런데 죽는 자리가
    #    셋업 뒤라 덤프 디렉터리는 이미 만들어져 있고, 배치로 돌리면 "덤프 0 개" 로만
    #    보여 **조용한 실패처럼** 읽힌다 (2026-09-19 실측: 시드 57204983 으로 두 팔이
    #    그렇게 죽었다).  ⇒ 덱을 **쓰기 전에** 막는다.
    if not _is_prime(int(seed)):
        raise SystemExit(
            f'⛔ 삽입 시드 {seed} 는 소수가 아니다 — LIGGGHTS 가 거부한다.\n'
            f'   예: 15485863 · 32452843 · 32452867 · 49979687 · 91648301')
    n, d = p['n'], p['d']
    period = 60.0 / rpm
    #  ★ 배플 — `D10(b)` 전단 축.  **원본 Drum.stl 은 안 건드린다** (별도 메시).
    #  ⚠ `n_baffles = 0` 이면 아래 두 조각이 **빈 문자열**이라 덱이 배플 이전과
    #    글자 그대로 같다 — 배플 없는 팔을 다시 돌릴 필요가 없다 (시험 ㉛ 이 강제).
    _baffle_mesh = ('' if not n_baffles else
                    f'fix Baffle all mesh/surface file Baffles.stl type 2 '
                    f'scale {p["stl_scale"]:.6g}\n')
    #  ⚠ 빈 문자열일 때 **줄이 남지 않게** 앞에 줄바꿈을 단다.  초판은 템플릿에서
    #    제 줄을 차지해 배플 0 인 덱에 **빈 줄 하나**가 더 생겼고, 그래서 이미 돌린
    #    런의 덱과 바이트가 달라졌다 (자기검사는 '지금 두 출력' 만 비교해 못 잡았다).
    _baffle_move = ('' if not n_baffles else
                    f'\nfix mvBf all move/mesh mesh Baffle rotate origin 0 0 0 '
                    f'axis 1. 0. 0. period {period:.6g}')
    #  낙하 높이 = 드럼 지름 (꼭대기에서 바닥까지)
    if settle_s is None:
        settle_s = settle_time(2.0 * p['R'], restitution)
    steps_fill = max(1000, int(round(0.5 * settle_s / p['dt'])))   # 두 번 돈다
    steps_run = int(round(revolutions * period / p['dt']))
    dump_every = max(1000, steps_run // 200)
    #  ── 삽입 블록 (§24 층상 vs 기존 균일) ─────────────────────────────────
    #  ⚠ 비층상 문자열은 옛 원문과 **바이트 동일**해야 한다 — 셀프테스트 ㉟ 골든 해시.
    if layered is None:
        layered = bool(ARMS[arm].get('layered', False))
    mf = p['massfrac']
    if not layered:
        _ins_block = f"""# ⚠ 분율은 **mass%** 다 (LIGGGHTS 규약 — 실행으로 확인).  우리 조성이 wt% 라 그대로 넣는다.
fix pdd all particledistribution/discrete 32452867 5 &
    pt1 {mf['AM_P']:.6f} pt2 {mf['AM_S']:.6f} pt3 {mf['SE']:.6f} &
    pt4 {mf['VGCF']:.6f} pt5 {mf['PTFE']:.6f}

region ins_reg cylinder x 0.0 0.0 {p['R']*0.9:.6g} -{p['L']*0.45:.6g} {p['L']*0.45:.6g} units box
fix ins all insert/pack seed {seed} distributiontemplate pdd &
    maxattempt 200 insert_every once overlapcheck yes all_in yes vel constant 0. 0. -0.2 &
    region ins_reg particles_in_region {p['n_tpl_total']} ntry_mc 20000   # 템플릿 수 (섬유 1가닥 = 1)
"""
        _unfix_ins = 'unfix ins'
        _unfix_ins2 = ''
    else:
        #  층별 mass% 는 층 안에서 다시 정규화한다 (pdd 는 자기 템플릿끼리의 분율만 본다)
        a_sum = mf['AM_P'] + mf['AM_S']
        b_sum = mf['SE'] + mf['VGCF'] + mf['PTFE']
        nA = p['n_tpl']['AM_P'] + p['n_tpl']['AM_S']
        nB = p['n_tpl']['SE'] + p['n_tpl']['VGCF'] + p['n_tpl']['PTFE']
        seedB = _next_prime(seed + 2)                 # insA 와 다른 소수
        pddB = _next_prime(32452867 + 2)              # pddA 와 다른 소수
        #  ★★ 순서가 물리다 (스모크 실측 2026-09-20): AM_P(Ø2.4 mm) 119 개를 작은 블록에
        #    `all_in` 으로 넣으면 중심 가용부피 대비 구 부피 59 % = RSA 잼 한계(~38 %) 초과 →
        #    삽입이 끝나지 않는다.  ⇒ AM 은 **원통 전체**(균일 삽입과 같은 영역)에 넣고 정착 ①
        #    로 바닥에 깔리게 한 뒤, SE+섬유를 **그 윗면 위 블록**에 넣는다 (정착 ②).
        #    = "AM 침대 위에 SE 를 붓는다" — 층상의 물리 그대로다.
        _v_am = sum(p['n'][k] * (math.pi / 6) * d[k] ** 3 for k in ('AM_P', 'AM_S'))
        _v_bed = _v_am / 0.60                          # plan() 의 pack 기본값
        _A = _v_bed / p['L']                           # 원 세그먼트 단면적
        _th = 2.0                                      # θ − sinθ = 2A/R²  (이분법)
        _lo_t, _hi_t = 0.0, 2 * math.pi
        for _ in range(60):
            _th = 0.5 * (_lo_t + _hi_t)
            if _th - math.sin(_th) < 2 * _A / p['R'] ** 2:
                _lo_t = _th
            else:
                _hi_t = _th
        _h = p['R'] * (1 - math.cos(_th / 2))          # 침대 높이 (바닥에서)
        _z_top = -p['R'] + _h
        _z_lo = _z_top + d['AM_P']                     # 여유 = AM_P 지름 하나
        _z_hi = 0.78 * p['R']                          # |y| ≤ 0.6R 이면 z ≤ 0.8R 가 원 안
        assert _z_hi - _z_lo > 4 * d['SE'], '층상 삽입: SE 층 높이가 너무 작다'
        _ins_block = f"""# ★ §24 층상 삽입 ① — AM 을 원통 전체에 넣는다 (정착 ① 로 바닥에 깔린다).  분율은 층 안 mass%.
fix pddA all particledistribution/discrete 32452867 2 &
    pt1 {mf['AM_P']/a_sum:.6f} pt2 {mf['AM_S']/a_sum:.6f}
fix pddB all particledistribution/discrete {pddB} 3 &
    pt3 {mf['SE']/b_sum:.6f} pt4 {mf['VGCF']/b_sum:.6f} pt5 {mf['PTFE']/b_sum:.6f}

region ins_reg cylinder x 0.0 0.0 {p['R']*0.9:.6g} -{p['L']*0.45:.6g} {p['L']*0.45:.6g} units box
fix insA all insert/pack seed {seed} distributiontemplate pddA &
    maxattempt 200 insert_every once overlapcheck yes all_in yes vel constant 0. 0. -0.2 &
    region ins_reg particles_in_region {nA} ntry_mc 20000   # AM 템플릿 수
"""
        _unfix_ins = f"""unfix insA
# ★ §24 층상 삽입 ② — 정착 ① 뒤, SE+VGCF+PTFE 를 AM 침대 **위** 블록에 붓는다 (정착 ② 시작 시 삽입).
#   AM 침대 윗면 추정: V_AM {_v_am*1e9:.0f} mm³ / pack 0.60 → 세그먼트 높이 {_h*1e3:.2f} mm → z_top {_z_top*1e3:.2f} mm
#   블록 z ∈ [{_z_lo*1e3:.2f}, {_z_hi*1e3:.2f}] mm · |y| ≤ 0.6R (원 안) · x ±0.45L
region ins_hi block -{p['L']*0.45:.6g} {p['L']*0.45:.6g} -{p['R']*0.6:.6g} {p['R']*0.6:.6g} {_z_lo:.6g} {_z_hi:.6g} units box
fix insB all insert/pack seed {seedB} distributiontemplate pddB &
    maxattempt 200 insert_every once overlapcheck yes all_in yes vel constant 0. 0. -0.2 &
    region ins_hi particles_in_region {nB} ntry_mc 20000   # SE+섬유 템플릿 수 (섬유 1가닥 = 1)"""
        _unfix_ins2 = '\nunfix insB'
    box = p['R'] * 1.15
    return f"""# 믹싱 드럼 — 표면에너지 스윕  (생성: scripts/make_mixer_deck.py)
# ⚠ 손으로 고치지 말 것 — 치수가 조성에서 유도된다.  조성을 바꾸면 생성기를 다시 돌린다.
#
# 조성 AM:SE:VGCF:PTFE = {WT['AM']:.0f}:{WT['SE']:.0f}:{WT['VGCF']:.0f}:{WT['PTFE']:.0f} (wt%) · P:S = {PS[0]:.0f}:{PS[1]:.0f}
# CGF = {p['cgf']:.0f}  (실제 AM_P {D_REAL_UM['AM_P']:.0f} µm → 사물 {d['AM_P']*1e3:.2f} mm)
# ⛔ 생산 scale=1000 규약을 쓰지 않는다 — 드럼은 중력 구동이라 중력/접촉 비가 깨진다.
# ⚠ 전단탄성률을 계산비용 때문에 낮췄다 (lischka 와 같은 조작) — 물성으로 인용 금지.

atom_style      granular
atom_modify     map array sort 0 0
boundary        f f f
newton          off
communicate     single vel yes
units           si
processors      1 1 1            # PUBLIC 판 multisphere 는 직렬만 지원

region          reg block -{box:.6g} {box:.6g} -{box:.6g} {box:.6g} -{box:.6g} {box:.6g} units box
create_box      5 reg
neighbor        {d['VGCF']*0.5:.6g} bin
neigh_modify    delay 0

# --- 물성 (1:AM_P 2:AM_S 3:SE 4:VGCF 5:PTFE) ---
# ⚠ 영률은 계산비용용 연화값이다.  생산 압축 덱의 값(AM 140 GPa · SE 1.35 GPa)이 아니다.
fix m1 all property/global youngsModulus peratomtype 1.e7 1.e7 1.e7 1.e7 1.e7
fix m2 all property/global poissonsRatio peratomtype 0.25 0.25 0.30 0.30 0.30
fix m3 all property/global coefficientRestitution peratomtypepair 5 &
{_mat(5, 0.3)}
fix m4 all property/global coefficientFriction peratomtypepair 5 &
{_mat(5, 0.5)}
fix m5 all property/global coefficientRollingFriction peratomtypepair 5 &
{_mat(5, 0.2)}
# ★ 스윕 축 — 표면에너지 대리 (SJKR, J/m³).  **팔 {arm}: {ARMS[arm]['desc']}**\n# ⚠ 이 블록만 팔마다 다르다.  나머지는 한 글자도 안 바뀐다.
fix mC all property/global cohesionEnergyDensity peratomtypepair 5 &
{_mat(5, ced_matrix(arm, d))}
fix m9 all property/global characteristicVelocity scalar 2.0

# ⚠ cohesion 은 tangential 뒤 · rolling_friction 앞 (순서가 실재하는 제약)
pair_style      gran model hertz tangential history cohesion sjkr rolling_friction cdt
pair_coeff      * *
timestep        {p['dt']:.4g}
fix             gravi all gravity 9.81 vector 0.0 0.0 -1.0

# --- 기구 (STL 은 튜토리얼 Mixer 원본을 scale 로 줄여 쓴다) ---
fix Drum  all mesh/surface file Drum.stl  type 2 scale {p['stl_scale']:.6g}
fix Front all mesh/surface file Front.stl type 2 scale {p['stl_scale']:.6g}
fix Back  all mesh/surface file Back.stl  type 2 scale {p['stl_scale']:.6g}
{_baffle_mesh}fix walls all wall/gran model hertz tangential history cohesion sjkr rolling_friction cdt &
    mesh n_meshes {3 + (1 if n_baffles else 0)} meshes Drum Front Back{' Baffle' if n_baffles else ''}

# --- 입자 ---
fix pt1 all particletemplate/sphere 10487 atom_type 1 density constant {DENS['AM']*1000:.0f} radius constant {d['AM_P']/2:.6g}
fix pt2 all particletemplate/sphere 11887 atom_type 2 density constant {DENS['AM']*1000:.0f} radius constant {d['AM_S']/2:.6g}
fix pt3 all particletemplate/sphere 13901 atom_type 3 density constant {DENS['SE']*1000:.0f} radius constant {d['SE']/2:.6g}
# ★ 섬유는 multisphere 강체 사슬 — 구 하나로 접지 않는다 (sun2026: 접으면 σ_e 순위가 뒤집힌다)
# ⚠ 끝의 `type` 은 **원자 타입이 아니라 multisphere 템플릿 번호**이고 **1 부터 연속**이어야 한다
#   (실행으로 확인: ERROR: multisphere template types have to be consecutive starting from 1)
fix pt4 all particletemplate/multisphere 15101 atom_type 4 density constant {DENS['VGCF']*1000:.0f} &
    nspheres {p['nsph']} ntry 1000000 spheres file data/vgcf.multisphere scale 1.0 type 1
fix pt5 all particletemplate/multisphere 17093 atom_type 5 density constant {DENS['PTFE']*1000:.0f} &
    nspheres {p['nsph']} ntry 1000000 spheres file data/ptfe.multisphere scale 1.0 type 2

{_ins_block}
# ⚠⚠ **적분기는 둘 다 필요하다** (2026-09-19 실측으로 확정)
#   `fix multisphere` 는 **강체만** 적분한다 — 평범한 구는 `body_[i] < 0` 로 건너뛴다.
#   이 줄 하나만 두고 돌렸더니 AM·SE 47,309 개가 **얼어붙은 조각상**이었다:
#   KE 가 삽입값에서 한 번도 안 움직였고 E0 과 E4 팔이 H/R 까지 동일했다.
#   ★ 직접 잰 것 — 평구 하나를 중력 아래 2,000 스텝 두니 z 가 0.02 그대로였다.
#   `nve/sphere` 를 얹으면 자유낙하가 정확히 복구되고(vz = −g·t),
#   섬유 결합거리는 0.48000/0.48000/0.96000 mm 로 **소수 5자리까지 불변**이며,
#   섬유 궤적은 nve 가 강체를 건드리지 않는 판과 **부동소수점까지 동일**하다
#   (`multisphere` 가 매 스텝 강체 상태를 다시 덮어쓴다 ⇒ 이중적분 피해 0).
fix integrS all nve/sphere        # ★ 평범한 구 (AM_P·AM_S·SE)
fix integr  all multisphere       # 강체 사슬 (VGCF·PTFE) — 뒤에 둬 강체를 최종 확정

compute rke all erotate/sphere
thermo_style custom step atoms ke c_rke vol
thermo 5000
thermo_modify lost ignore norm no

shell mkdir post
run 1
dump dmp all custom {dump_every} post/mix_*.liggghts id type mol x y z vx vy vz fx fy fz radius

# ① 채우고 정착 — ⚠ KE 가 떨어진 뒤에 회전을 시작한다 (정착 전에 돌리면 지표가 뒤집힌다)
#   정착 {2*steps_fill*p['dt']:.3f} s = 낙하 {2*p['R']*1e3:.1f} mm · e {restitution} 에서
#   유도한 t_ff·(1+e)/(1−e) 의 {2.0:.0f}배.  ⛔ 상수 20000 step 을 쓰지 않는다.
#   ⚠ 그래도 잰 뒤 φ(포락) 경고를 확인할 것 — 식은 홑 입자의 튐만 센다.
run {steps_fill}
{_unfix_ins}
run {steps_fill}{_unfix_ins2}

# ② 회전 {revolutions} 바퀴 @ {rpm:.0f} rpm  (임계 {p['rpm_crit']:.0f} rpm · Fr {(2*math.pi/period)**2*p['R']/9.81:.3f})
fix mvD all move/mesh mesh Drum  rotate origin 0 0 0 axis 1. 0. 0. period {period:.6g}
fix mvF all move/mesh mesh Front rotate origin 0 0 0 axis 1. 0. 0. period {period:.6g}
fix mvB all move/mesh mesh Back  rotate origin 0 0 0 axis 1. 0. 0. period {period:.6g}{_baffle_move}
run {steps_run}
"""


def _mat(n, val):
    """peratomtypepair n×n 행렬.  `val` 이 스칼라면 균일, 2차원이면 그대로."""
    if isinstance(val, (list, tuple)):
        return ' &\n'.join('    ' + ' '.join(f'{v:g}' for v in row) for row in val)
    return ' &\n'.join('    ' + ' '.join(f'{val:g}' for _ in range(n)) for _ in range(n))


def _raises(fn):
    try:
        fn()
        return False
    except SystemExit:
        return True


def _selftest():
    ok, fail = 0, []

    def chk(name, cond):
        nonlocal ok
        if cond:
            ok += 1
        else:
            fail.append(name)
        print(('  PASS  ' if cond else '  FAIL  ') + name)

    phi, wt = volume_fractions()
    chk('① 부피분율 합 = 1', abs(sum(phi.values()) - 1) < 1e-12)
    chk('② wt 합 = 100', abs(sum(wt.values()) - 100) < 1e-9)
    chk('③ AM_P:AM_S wt 비 = 7:3', abs(wt['AM_P'] / wt['AM_S'] - 7 / 3) < 1e-9)
    p = plan(50000)
    chk(f'④ 개수 합이 목표에 맞는다 ({p["n_total"]})', abs(p['n_total'] - 50000) / 50000 < 0.01)
    chk('⑤ SE 가 개수로 최다', max(p['n'], key=p['n'].get) == 'SE')
    #  ★ 변이 대조 — CGF 를 2배 하면 드럼 반경이 2배여야 한다 (부피 ∝ d³ · 개수 고정)
    p2 = plan(50000, cgf=400.0)
    chk('⑥ 변이: CGF ×2 → 드럼 R ×2', abs(p2['R'] / p['R'] - 2) < 0.02)
    chk('⑦ 변이: CGF ×2 → dt ×2', abs(p2['dt'] / p['dt'] - 2) < 0.02)
    #  ★ 섬유 파일 — 강체가 되도록 겹쳐야 한다
    txt = fibre_file(5, 1e-3)
    xs = [float(l.split()[0]) for l in txt.strip().split('\n')]
    gap = xs[1] - xs[0]
    chk('⑧ 섬유 구가 겹친다 (중심간 < 지름)', gap < 1e-3)
    chk('⑨ 섬유가 원점 대칭', abs(xs[0] + xs[-1]) < 1e-12)
    dk = deck(p, rpm=60, revolutions=5)
    chk('⑩ 덱에 cohesion 이 tangential 뒤·rolling 앞',
        'tangential history cohesion sjkr rolling_friction' in dk)
    chk('⑪ multisphere 적분기를 쓴다', 'fix integr  all multisphere' in dk)
    #  ★⑪b 재현 시험 — 이 결함이 실제로 났다.  `multisphere` 는 강체만 적분하므로
    #     평범한 구 템플릿이 있으면 `nve/sphere` 가 **반드시** 같이 있어야 한다.
    _has_sphere_tpl = 'particletemplate/sphere' in dk
    chk('⑪b 평범한 구가 있으면 nve/sphere 적분기도 있다 (없으면 조각상이 된다)',
        (not _has_sphere_tpl) or ('fix integrS all nve/sphere' in dk))
    #  ★⑪c 순서 — nve 가 먼저, multisphere 가 나중 (강체를 최종 확정)
    chk('⑪c nve/sphere 가 multisphere 보다 먼저 정의된다',
        dk.index('fix integrS all nve/sphere') < dk.index('fix integr  all multisphere'))
    #  ★⑪d 정착식 앵커 — 튜토리얼 실측을 맞히는가 (낙하 60 mm · e 0.9 → 2.1 s)
    _t = settle_time(0.060, 0.9, margin=1.0)
    chk(f'⑪d 정착식이 튜토리얼 실측 2.1 s 를 맞힌다 (식 {_t:.2f} s)',
        abs(_t - 2.1) < 0.1)
    #  ★⑪e 변이 — 정착 스텝이 **상수가 아니다** (드럼이 커지면 길어져야 한다)
    _small = deck(plan(4000), rpm=60, revolutions=1)
    _big = deck(plan(32000), rpm=60, revolutions=1)
    import re as _re
    _f = lambda t: int(_re.search(r'run (\d+)\nunfix ins', t).group(1))
    chk(f'⑪e 변이: 정착 스텝이 드럼 크기를 따라간다 ({_f(_small):,} → {_f(_big):,})',
        _f(_big) > _f(_small) * 1.3)
    chk('⑫ 생산 scale=1000 규약을 안 쓴다', 'scale 1000' not in dk)
    #  ★ 실행으로 배운 제약 — multisphere 템플릿 번호는 1 부터 연속이어야 한다
    import re as _re
    _t = [int(m) for m in _re.findall(r'\.multisphere scale [\d.]+ type (\d+)', dk)]
    chk(f'⑬ multisphere 템플릿 번호가 1 부터 연속 ({_t})',
        _t == list(range(1, len(_t) + 1)))
    #  변이 대조 — atom_type 은 그대로 4·5 여야 한다 (둘을 헷갈리면 상이 섞인다)
    #  ★ 겹침 보정 — 3구 사슬은 구 3개 합의 약 0.963 배여야 한다 (해석값)
    f3 = chain_volume_factor(3)
    chk(f'⑮ 3구 사슬 부피계수 {f3:.4f} ≈ 0.9627 (해석)', abs(f3 - 0.9627) < 5e-3)
    chk('⑯ 변이: nsph=1 이면 보정 없음', chain_volume_factor(1) == 1.0)
    chk('⑰ 변이: 사슬이 길수록 계수가 준다', chain_volume_factor(5) < f3)
    chk('⑭ 변이: atom_type 은 4·5 로 남아 있다',
        'atom_type 4' in dk and 'atom_type 5' in dk)
    #  ★ 팔 — 점착 블록만 달라야 한다
    d0, d1, d2 = (deck(p, 60, 5, arm=x) for x in ('E0', 'E1', 'E2'))
    def _strip_ced(t):
        '''점착 블록과 **주석**을 뺀 실행 줄만 남긴다.

        ⚠ 주석을 빼는 이유 — 팔 이름이 주석에 들어가서 달라진다.  주석은 물리가
          아니므로 비교 대상이 아니다.  그러나 **실행되는 줄은 한 글자도 달라서는
          안 된다** — 그것이 이 시험의 계약이다.
        '''
        out, skip = [], False
        for ln in t.split('\n'):
            if 'cohesionEnergyDensity' in ln:
                skip = True
                continue
            if skip:
                if ln.startswith('    ') or ln.strip() == '&':
                    continue
                skip = False
            st = ln.strip()
            if st.startswith('#') or not st:
                continue
            out.append(ln)
        return '\n'.join(out)
    chk('⑱ 팔끼리 점착 블록 **밖**은 한 글자도 안 다르다',
        _strip_ced(d0) == _strip_ced(d1) == _strip_ced(d2))
    chk('⑲ 팔끼리 점착 블록은 실제로 다르다', d0 != d1 != d2 and d0 != d2)
    dd = p['d']
    M0, M1, M2 = (ced_matrix('E0', dd), ced_matrix('E1', dd), ced_matrix('E2', dd))
    chk('⑳ E0 는 전부 0 (음성 대조)', all(v == 0 for r in M0 for v in r))
    chk('㉑ E2 는 AM-AM 만 Bo ×10 = CED ×10^(1/3)',
        abs(M2[0][0] / M1[0][0] - 10 ** (1 / 3.)) < 1e-6
        and abs(M2[2][2] - M1[2][2]) < 1e-9)
    chk('㉒ 행렬이 대칭이다 (비대칭 입력 방지)',
        all(M2[i][j] == M2[j][i] for i in range(5) for j in range(5)))
    #  변이 대조 — 대칭 강제가 장식이 아님을 보인다
    ARMS['_t'] = dict(desc='t', bond=1.0, mult={('AM_P', 'SE'): 7.0})
    Mt = ced_matrix('_t', dd); del ARMS['_t']
    chk('㉓ 변이: 한쪽만 준 배수가 양쪽에 반영된다',
        Mt[0][2] == Mt[2][0] and Mt[0][2] > Mt[2][2])

    #  ★ 시드 — 판정선(§7)이 SE_시드를 요구한다.  시드는 **삽입 줄 하나만** 바꿔야 한다
    ds1 = deck(p, rpm=60, revolutions=1, arm='E1', seed=32452843)
    ds2 = deck(p, rpm=60, revolutions=1, arm='E1', seed=91648301)
    dif = [(x, y) for x, y in zip(ds1.split('\n'), ds2.split('\n')) if x != y]
    chk(f'㉓b 시드는 삽입 줄 하나만 바꾼다 (다른 줄 {len(dif)})',
        len(dif) == 1 and 'insert/pack seed' in dif[0][0])

    #  ★ 시드 소수 검사 — 합성수를 주면 LIGGGHTS 가 셋업 뒤에 죽어 '조용한 실패' 로 읽힌다
    chk('㉓c 합성수 시드를 **덱 쓰기 전에** 거부한다 (57204983 = 합성수)',
        _raises(lambda: deck(p, rpm=60, revolutions=1, seed=57204983)))
    chk('㉓d 소수 시드는 통과한다 (49979687)',
        not _raises(lambda: deck(p, rpm=60, revolutions=1, seed=49979687)))

    #  ★★ ㉛ 배플 — `n=0` 이면 덱이 **배플 이전과 글자 그대로 같아야** 한다.
    #     이게 깨지면 "배플 없는 팔" 을 다시 돌려야 하고, 그러면 배플 비교가
    #     **두 축(배플 + 재실행 잡음)** 을 동시에 바꾼 비교가 된다.
    d_none = deck(p, rpm=60, revolutions=1, arm='E1', n_baffles=0)
    d_base = deck(p, rpm=60, revolutions=1, arm='E1')          # 기본값 = 배플 없음
    chk('㉛ ★ 배플 0 개면 덱이 배플 이전과 **바이트 동일**', d_none == d_base)
    d_baf = deck(p, rpm=60, revolutions=1, arm='E1', n_baffles=6, baffle_h=0.10)
    chk('㉛b 배플을 켜면 메시가 4개가 되고 회전도 같이 받는다',
        'n_meshes 4 meshes Drum Front Back Baffle' in d_baf
        and 'mvBf all move/mesh mesh Baffle rotate' in d_baf
        and 'Baffles.stl' in d_baf)
    #  ★ 변이 — 배플 덱과 무배플 덱의 차이가 **배플 줄뿐**이어야 한다
    _drop = lambda t: '\n'.join(l for l in t.split('\n')
                                if 'Baffle' not in l and 'n_meshes' not in l)
    chk('㉛c 변이: 배플 줄을 빼면 나머지는 한 글자도 안 다르다',
        _drop(d_baf) == _drop(d_none))
    #  ★ 회전 주기가 드럼과 같아야 한다 (따로 돌면 기구가 아니라 교반기가 된다)
    import re as _re2
    #  ⚠ 덱은 정렬용으로 `Drum  rotate` 처럼 **공백 두 개**를 쓴다 — ` +` 로 받는다
    #    (초판 정규식이 공백 하나라 4개 중 2개만 잡아 시험이 실패했다 — 코드가
    #     아니라 **시험이** 틀린 경우다)
    _per = _re2.findall(r'move/mesh mesh \w+ +rotate origin 0 0 0 axis 1\. 0\. 0\. '
                        r'period ([0-9.eE+-]+)', d_baf)
    chk(f'㉛d 배플이 드럼과 **같은 주기**로 돈다 ({len(_per)} 메시, 값 {set(_per)})',
        len(_per) == 4 and len(set(_per)) == 1)
    #  ★★ ㉛e — ㉛ 이 **놓쳤던** 것.  ㉛ 은 '지금 만든 두 출력' 을 비교하므로 둘 다
    #     똑같이 망가지면 통과한다.  실제로 `{_baffle_move}` 가 제 줄을 차지해
    #     배플 0 덱에 **빈 줄 하나**가 더 생겼고, 이미 돌린 런의 덱과 바이트가
    #     달라졌는데 ㉛ 은 초록이었다.  ⇒ **구조를 직접 못 박는다.**
    _lines = d_none.split('\n')
    _mvb = next(i for i, l in enumerate(_lines) if 'move/mesh mesh Back' in l)
    chk('㉛e ★ 배플 0 덱의 회전 블록 뒤에 **빈 줄이 안 생긴다** '
        '(두 출력 비교로는 못 잡는 자리)',
        _lines[_mvb + 1].strip() != '')
    #  배플 덱은 정확히 **세 줄만** 다르다 (메시 · n_meshes · 회전)
    import difflib as _dl
    _dif = [l for l in _dl.unified_diff(d_none.split('\n'), d_baf.split('\n'), n=0)
            if l[:1] in '+-' and l[:3] not in ('+++', '---')]
    chk(f'㉛f 배플 덱은 정확히 메시·n_meshes·회전 **세 자리만** 다르다 (실제 {len(_dif)} 줄)',
        len(_dif) == 4 and sum(1 for l in _dif if l.startswith('+')) == 3)

    #  ★★ ㉜ 코팅 팔 — "AM 표면이 SE 가 된다"
    Mc = ced_matrix('C1', dd)
    M1 = ced_matrix('E1', dd)
    _i = {t: k for k, t in enumerate(TYPES)}
    chk(f'㉜ 코팅하면 AM-AM CED 가 **SE-SE 값**이 된다 '
        f'({M1[_i["AM_P"]][_i["AM_P"]]:.3g} → {Mc[_i["AM_P"]][_i["AM_P"]]:.3g})',
        abs(Mc[_i['AM_P']][_i['AM_P']] - Mc[_i['SE']][_i['SE']]) < 1e-9
        and abs(Mc[_i['AM_S']][_i['AM_S']] - Mc[_i['SE']][_i['SE']]) < 1e-9
        and abs(Mc[_i['AM_P']][_i['AM_S']] - Mc[_i['SE']][_i['SE']]) < 1e-9)
    chk('㉜b SE-SE 자신은 안 바뀐다 (코팅재를 건드리지 않는다)',
        abs(Mc[_i['SE']][_i['SE']] - M1[_i['SE']][_i['SE']]) < 1e-9)
    chk('㉜c AM-SE 는 원래 SE 값이었으므로 코팅해도 그대로',
        abs(Mc[_i['AM_P']][_i['SE']] - M1[_i['AM_P']][_i['SE']]) < 1e-9)
    chk('㉜d 코팅 행렬도 대칭이다',
        all(Mc[i][j] == Mc[j][i] for i in range(5) for j in range(5)))
    #  ★ 변이 — 코팅 안 하면 AM-AM 이 SE-SE 와 **다르다** (덮어쓰기가 장식이 아님)
    chk(f'㉜e 변이: 코팅 없으면 AM-AM ≠ SE-SE '
        f'({M1[_i["AM_P"]][_i["AM_P"]]:.3g} vs {M1[_i["SE"]][_i["SE"]]:.3g})',
        abs(M1[_i['AM_P']][_i['AM_P']] - M1[_i['SE']][_i['SE']]) > 1e3)
    #  ★ 코팅은 **덜 끈적하게** 만든다 (AM 이 크고 무거워 같은 Bo 에 더 큰 CED 가 필요했다)
    chk('㉜f 코팅이 AM-AM 점착을 **낮춘다** (방향)',
        Mc[_i['AM_P']][_i['AM_P']] < M1[_i['AM_P']][_i['AM_P']])

    #  ★★ ㉝ 고-G 팔 — 중력이 아니라 **Bo 를 내려** 기계를 표현한다
    M4, MT1, MT2 = ced_matrix('E4', dd), ced_matrix('T1', dd), ced_matrix('T2', dd)
    _bo = lambda M: bond_for_ced(M[0][0], dd['AM_P'] / 2, .25, DENS['AM'])
    chk(f'㉝ T1 의 Bo 가 E4 의 **1/268** ({_bo(M4):.3f} → {_bo(MT1):.5f})',
        abs(_bo(MT1) * 268.0 / _bo(M4) - 1.0) < 1e-6)
    chk(f'㉝b T2 의 Bo 가 E4 의 **1/45** ({_bo(MT2):.5f})',
        abs(_bo(MT2) * 45.0 / _bo(M4) - 1.0) < 1e-6)
    #  ★ 핵심 — 고-G 팔은 겹침이 **더 작다** (중력을 올렸다면 커졌을 것)
    _ov = lambda M: overlap_for_ced(M[0][0], dd['AM_P'] / 2, .25)
    chk(f'㉝c ★ 고-G 팔의 겹침이 E4 보다 **작다** '
        f'({_ov(M4)*100:.3f} % → {_ov(MT1)*100:.3f} %) — 접촉모델이 더 안전해진다',
        _ov(MT1) < _ov(M4) and _ov(MT2) < _ov(M4))
    #  ★ 변이 — 중력을 268배 올렸다면 Π₁ 이 268배가 되어 규약이 깨진다는 것을 못 박는다
    _P1 = lambda a, E: 4800.0 * a * (dd['AM_P'] / 2) / E
    chk(f'㉝d 변이: 중력을 268배 올리면 Π₁=ρaR/E 가 268배가 된다 '
        f'({_P1(9.81, E_YOUNG):.2e} → {_P1(9.81*268, E_YOUNG):.2e}) — 스케일 팩터 위반',
        abs(_P1(9.81 * 268, E_YOUNG) / _P1(9.81, E_YOUNG) - 268.0) < 1e-6)
    #  ★ BOND0 은 약한 팔이 늘어도 안 흔들린다 (천장은 가장 센 팔이 정한다)
    chk('㉝e 고-G 팔을 더해도 BOND0 이 안 바뀐다 (천장은 최강 팔이 정한다)',
        abs(_solve_bond0(dd) - 0.2124) < 1e-3)

    #  ★★ 점착 눈금 — **실측 앵커**.  이 다섯이 새 사다리의 근거다.
    #  실측 3.50 % — 강체 내부 쌍을 제외하고 다시 잰 값 (초판 3.54 % 는 섬유 자기겹침 포함)
    chk(f'㉔ 겹침식이 E1 실측을 맞힌다 (예측 {overlap_for_ced(3e5, 3e-4, .30)*100:.2f} % '
        f'vs 실측 3.50 %)',
        abs(overlap_for_ced(3e5, 3e-4, .30) - 0.0350) < 0.006)
    chk(f'㉕ 겹침식이 ×10 붕괴를 설명한다 (CED 3e6 → '
        f'{overlap_for_ced(3e6, 3e-4, .30)*100:.0f} % = 통과)',
        overlap_for_ced(3e6, 3e-4, .30) > 1.0)
    chk('㉖ δ/r 은 CED 의 **제곱**이다 (×10 이 ×100)',
        abs(overlap_for_ced(2e5, 3e-4, .30) / overlap_for_ced(1e5, 3e-4, .30) - 4.0) < 1e-9)
    chk('㉗ Bo 는 CED 의 **세제곱**이다 (사다리를 Bo 로 거는 이유)',
        abs(bond_for_ced(2e5, 3e-4, .30, 2.0) / bond_for_ced(1e5, 3e-4, .30, 2.0) - 8.0) < 1e-9)
    chk('㉘ ced_for_bond ↔ bond_for_ced 왕복',
        abs(bond_for_ced(ced_for_bond(7.0, 3e-4, .30, 2.0), 3e-4, .30, 2.0) - 7.0) < 1e-9)
    #  ★★ 천장 — **모든 팔이 겹침 천장 안**이어야 한다.  초판은 4/5 가 밖이었다.
    worst = []
    for arm in sorted(ARMS):
        M = ced_matrix(arm, dd)
        for i, ti in enumerate(TYPES):
            small_r = dd[ti] / 2.0
            worst.append((overlap_for_ced(M[i][i], small_r, PHASE_MECH[ti][0]), arm, ti))
    wv, wa, wt = max(worst)
    chk(f'㉙ ★ 모든 팔이 겹침 천장 {OVL_CEILING*100:.0f} % 안 '
        f'(최악 {wa}·{wt} {wv*100:.3f} %)', wv <= OVL_CEILING * (1 + 1e-9))
    #  ★ 변이 — 옛 사다리(CED 3e5 에 ×100)를 넣으면 이 검사가 **걸려야** 한다
    chk('㉙b 변이: 옛 사다리(CED 3e7)는 천장을 넘는다',
        overlap_for_ced(3e7, 3e-4, .30) > OVL_CEILING)
    #  ★ 상별 CED 가 실제로 다르다 (같은 Bo 를 만들려면 달라야 한다)
    chk(f'㉚ 같은 Bo 를 위해 상별 CED 가 다르다 '
        f'(AM_P {M1[0][0]:.3g} vs SE {M1[2][2]:.3g})',
        abs(M1[0][0] - M1[2][2]) / M1[2][2] > 0.1)
    #  ── §24 층상 팔 ──────────────────────────────────────────────────────────
    import hashlib as _hl
    _p8 = plan(8000)
    chk('㉞ 새 팔(L0·LA·LC)을 넣어도 BOND0 이 0.21244 그대로다 (Bo 라벨이 안 밀린다)',
        abs(_solve_bond0(_p8['d']) - 0.21244) < 5e-6)
    _gold = {'E0': '475de96f647f99cb', 'E1': '73292b46192dc5cc', 'E4': '7787d125dfb80d01',
             'C1': 'fbcd03663fe780cb', 'T1': '60a212d1722da1ec', 'B5': 'da609bb4b5245534'}
    _got = {a: _hl.sha256(deck(_p8, rpm=60, revolutions=2, seed=32452843, arm=a)
                          .encode()).hexdigest()[:16] for a in _gold}
    chk('㉟ 기존 6 팔 덱이 편집 전과 **바이트 동일** (골든 해시, plan(8000)·2바퀴·시드 32452843)',
        _got == _gold)
    _la = deck(_p8, rpm=60, revolutions=2, seed=32452843, arm='LA')
    chk('㊱ LA 는 insert/pack 둘(insA→원통 전체, insB→AM 침대 위 블록), pdd 둘, unfix 둘',
        _la.count('insert/pack') == 2 and 'pddA' in _la and 'pddB' in _la
        and 'unfix insA' in _la and 'unfix insB' in _la
        and 'region ins_reg particles_in_region' in _la and 'region ins_hi particles_in_region' in _la)
    _i_s1 = _la.index('run 36308') if 'run 36308' in _la else _la.index('run ', _la.index('unfix insA') - 40)
    chk('㊱b 순서: insA → 정착① → unfix insA·insB 정의 → 정착② → unfix insB → 회전',
        _la.index('fix insA') < _la.index('unfix insA') < _la.index('fix insB')
        < _la.index('unfix insB') < _la.index('fix mvD'))
    import re as _re
    _nA = int(_re.search(r'region ins_reg particles_in_region (\d+)', _la).group(1))
    _nB = int(_re.search(r'region ins_hi particles_in_region (\d+)', _la).group(1))
    #  ⚠ plan() 은 상별로 반올림하므로 상별 합이 n_tpl_total 과 ±1~2 다를 수 있다.
    #    균일 삽입은 총수(n_tpl_total)를, 층상은 상별 합을 쓴다 — 층상이 조성에 더 충실하다.
    _sum_tpl = sum(_p8['n_tpl'].values())
    chk('㊲ 두 층의 템플릿 수 합 = 상별 계획의 합 (입자를 잃지 않는다; 총수와는 반올림 ±2 안)',
        _nA + _nB == _sum_tpl and abs(_sum_tpl - _p8['n_tpl_total']) <= 2
        and _nA == _p8['n_tpl']['AM_P'] + _p8['n_tpl']['AM_S'])
    _seeds = [int(x) for x in _re.findall(r'insert/pack seed (\d+)', _la)]
    _pdds = [int(x) for x in _re.findall(r'particledistribution/discrete (\d+)', _la)]
    chk('㊳ 삽입·분포 시드 넷이 전부 소수이고 쌍끼리 다르다',
        all(_is_prime(x) for x in _seeds + _pdds) and _seeds[0] != _seeds[1] and _pdds[0] != _pdds[1])
    _hi = _re.search(r'region ins_hi block \S+ \S+ (\S+) (\S+) (\S+) (\S+)', _la).groups()
    _y, _zl, _zh = abs(float(_hi[0])), float(_hi[2]), float(_hi[3])
    _ztop = float(_re.search(r'z_top (\S+) mm', _la).group(1)) * 1e-3
    chk('㊴ SE 층 블록: 아랫면 ≥ AM 침대 윗면 + AM_P 지름, 윗면 0.78R, 모서리가 원 안(y²+z²<R²)',
        #  덱은 z_top 을 0.01 mm, 좌표를 6 유효숫자로 찍는다 → 허용오차 1e-5 m / 상대 1e-4
        _zl >= _ztop + _p8['d']['AM_P'] - 1e-5 and abs(_zh - 0.78 * _p8['R']) < 1e-4 * _p8['R']
        and _y ** 2 + _zh ** 2 < _p8['R'] ** 2 and _y ** 2 + _zl ** 2 < _p8['R'] ** 2)
    #  RSA 여유: SE 층 블록의 중심 가용부피 대비 SE+섬유 구 부피 (스모크 사고의 정량 가드)
    _dse = _p8['d']['SE']
    _vsol = sum(_p8['n'][k] * (math.pi / 6) * _p8['d'][k] ** 3 for k in ('SE', 'VGCF', 'PTFE'))
    _vc = (0.9 * _p8['L'] - _dse) * (1.2 * _p8['R'] - _dse) * ((_zh - _zl) - _dse)
    chk(f'㊴b SE 층 삽입 밀도 {_vsol/_vc*100:.0f} % < 30 % (RSA 잼 한계 아래)', _vsol / _vc < 0.30)
    _fa = [float(x) for x in _re.search(r'pt1 (\S+) pt2 (\S+)\n', _la).groups()]
    _fb = [float(x) for x in _re.search(r'pt3 (\S+) pt4 (\S+) pt5 (\S+)', _la).groups()]
    chk('㊵ 층별 mass% 가 각각 1 로 재정규화된다',
        abs(sum(_fa) - 1) < 2e-6 and abs(sum(_fb) - 1) < 2e-6)
    _M = ced_matrix('LA', _p8['d'])
    chk('㊶ LA 의 AM_P–AM_P Bo 가 3.0 (앵커) 이다',
        abs(bond_for_ced(_M[0][0], _p8['d']['AM_P'] / 2, .25, DENS['AM']) - 3.0) < 1e-3)
    _Mc = ced_matrix('LC', _p8['d']); _M1 = ced_matrix('C1', _p8['d'])
    chk('㊷ LC 의 CED 행렬은 C1 과 같다 (코팅 규약을 두 벌 두지 않는다)', _Mc == _M1)
    _l0 = deck(_p8, rpm=60, revolutions=2, seed=32452843, arm='L0')
    chk('㊸ L0 도 층상이고 점착 0 이다', _l0.count('insert/pack') == 2 and 'cohesionEnergyDensity' in _l0)

    #  ★★ 선언 ↔ 사용 — 이 결함이 실제로 있었다 (2026-09-21).  표에 `SE 1.0` 을 적어 두고
    #     코드는 `AM_P×0.25` 를 썼다.  AM_P 12 에서 `AM_S` 만 우연히 맞아 **아무도 못 봤다**.
    #     ⇒ 표에 적힌 값이 **실제로 쓰인 값**인지 매번 확인한다.
    for _cg in (200.0, 137.0):
        _pd = plan(8000, cgf=_cg)['d']
        _bad = [k for k in TYPES if abs(_pd[k] / _cg * 1e6 - D_REAL_UM[k]) > 1e-9]
        chk(f'㊹ CGF {_cg:g}: 표의 실제 지름 = 실제로 쓰인 지름 (어긋남 {len(_bad)})', not _bad)
    #  ⚠ 변이 대조 — 표를 바꾸면 덱도 바뀌어야 한다 (표가 장식이 아님을 보인다)
    _base_s = plan(8000)['d']['AM_S']
    _orig = D_REAL_UM['AM_S']
    try:
        D_REAL_UM['AM_S'] = _orig * 1.5
        _moved = plan(8000)['d']['AM_S']
    finally:
        D_REAL_UM['AM_S'] = _orig
    chk('㊹b 변이: 표의 AM_S 를 ×1.5 하면 지름도 ×1.5 (표가 실제로 쓰인다)',
        abs(_moved / _base_s - 1.5) < 1e-9)
    print(f'\nmake_mixer_deck selftest: {ok}/{ok+len(fail)} PASS'
          + (f'   FAILED: {fail}' if fail else ''))
    return 1 if fail else 0


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default='', help='덱을 쓸 디렉터리')
    ap.add_argument('--n-total', type=int, default=50000)
    ap.add_argument('--cgf', type=float, default=200.0)
    ap.add_argument('--rpm', type=float, default=60.0)
    ap.add_argument('--revolutions', type=int, default=5)
    ap.add_argument('--baffles', type=int, default=0,
                    help='배플 개수 (D10(b) 전단 축).  0 이면 덱이 배플 이전과 바이트 동일')
    ap.add_argument('--baffle-h', type=float, default=0.10,
                    help='드럼 반경 대비 배플 높이.  기본 0.10')
    ap.add_argument('--seed', type=int, default=32452843,
                    help='삽입 시드.  ⚠ 판정선(§7)이 SE_시드를 요구하므로 **반복이 필요하다**')
    ap.add_argument('--settle-s', type=float, default=None,
                    help='정착 시간 (s).  기본은 낙하높이·반발계수에서 유도')
    ap.add_argument('--arm', default='E1', choices=sorted(ARMS),
                    help='점착 팔.  `all` 대신 하나씩 — 디렉터리가 갈린다')
    ap.add_argument('--all-arms', action='store_true',
                    help='--out 아래에 팔마다 하위 디렉터리를 만든다')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        raise SystemExit(_selftest())
    p = plan(a.n_total, cgf=a.cgf)
    print(f'조성 → 개수 (N={p["n_total"]:,})')
    for k in ('AM_P', 'AM_S', 'SE', 'VGCF', 'PTFE'):
        print(f'   {k:5s} φ {p["phi"][k]:.4f} · d {p["d"][k]*1e3:6.3f} mm · n {p["n"][k]:8,d}'
              + (f'  ({p["n_fib"][k]:,} 가닥 × {p["nsph"]} 구)' if k in p['n_fib'] else ''))
    print(f'\n드럼  R {p["R"]*1e3:.1f} mm (지름 {2*p["R"]*1e3:.0f} mm) · L {p["L"]*1e3:.1f} mm'
          f' · 부피 {p["v_drum"]*1e6:.0f} mL · STL scale {p["stl_scale"]:.4f}')
    print(f'시간  dt {p["dt"]:.3g} s · 임계 {p["rpm_crit"]:.0f} rpm'
          f' · {a.rpm:.0f} rpm 에서 Fr {(2*math.pi*a.rpm/60)**2*p["R"]/9.81:.3f}')
    steps = int(round(a.revolutions * (60/a.rpm) / p['dt']))
    print(f'비용  {a.revolutions} 바퀴 = {steps:,} step · 직렬 추정 '
          f'{p["n_total"]*steps/2.99e6/3600:.1f} h  (실측 처리율 2.99e6 p·step/s)')
    if a.out:
        os.makedirs(os.path.join(a.out, 'data'), exist_ok=True)
        with open(os.path.join(a.out, 'data', 'vgcf.multisphere'), 'w') as f:
            f.write(fibre_file(p['nsph'], p['d']['VGCF']))
        with open(os.path.join(a.out, 'data', 'ptfe.multisphere'), 'w') as f:
            f.write(fibre_file(p['nsph'], p['d']['PTFE']))
        arms = sorted(ARMS) if a.all_arms else [a.arm]
        for arm in arms:
            d = os.path.join(a.out, arm) if a.all_arms else a.out
            os.makedirs(os.path.join(d, 'data'), exist_ok=True)
            with open(os.path.join(d, 'data', 'vgcf.multisphere'), 'w') as f:
                f.write(fibre_file(p['nsph'], p['d']['VGCF']))
            with open(os.path.join(d, 'data', 'ptfe.multisphere'), 'w') as f:
                f.write(fibre_file(p['nsph'], p['d']['PTFE']))
            with open(os.path.join(d, 'in.mixer'), 'w') as f:
                f.write(deck(p, a.rpm, a.revolutions, arm=arm,
                             settle_s=a.settle_s, seed=a.seed,
                             n_baffles=a.baffles, baffle_h=a.baffle_h))
            if a.baffles:
                import importlib.util as _iu
                _sp = _iu.spec_from_file_location(
                    '_bf', os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                        'make_mixer_baffles.py'))
                _bf = _iu.module_from_spec(_sp); _sp.loader.exec_module(_bf)
                with open(os.path.join(d, 'Baffles.stl'), 'w') as f:
                    f.write(_bf.to_stl(_bf.baffle_tris(a.baffles, a.baffle_h)))
            print(f'   → {d}/in.mixer   [{arm}] {ARMS[arm]["desc"]}')
        print('⬜ STL 3개(Drum·Front·Back)를 각 디렉터리에 두어야 한다')
