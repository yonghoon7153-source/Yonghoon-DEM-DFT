#!/usr/bin/env python3
"""믹서 **실행 덱 되읽기** — 내보낸 `in.mixer` 텍스트만 읽어 강성 축 (표 E) 과 LC↔LH 공동 개입 (표 B) 을 독립 검산한다 (2026-09-30).

왜
  Codex 9 차 §3 (표 B · 표 E 형식) · §6-2 · 7 차 §5 · 6 차 HBR6-02.  생성기 함수의 기대값 표는 **출력 과정 · 옵션 배선 · 타입 순서**가
  틀렸는지까지 확인하지 못한다 — *"문서의 올바른 공식 ≠ 출력 덱의 올바른 값 ≠ 실제 실행물과 봉인의 동일성"*.  이 도구는 둘째를 본다:
  **실제로 봉인할 덱**의 타입별 E · ν · 반지름 (템플릿) · CED 를 덱 텍스트에서 되읽고, 쌍별 E* · R* · F₀ 를 **덱 값에서** 다시 계산한다.
  ⛔ 생성기 (`make_mixer_deck.py`) 를 import 하지 않는다 (셀프테스트의 고정물 덱을 만들 때만 쓴다).  등록 상수 (타입 사전 · 템플릿
    시드 · 인쇄 정밀도 · 덤프/체크포인트 규칙 · Codex 7 차 §5 산술) 는 **사본**이다 — 생성기가 바뀌면 여기서 어긋나 드러난다 (fail-closed).

표 (`--table KIND OLD NEW` 여러 번)
  E    같은 팔 · 다른 강성 (soft → ×14 · ×14 → ×28): 9 비영 항 F₀ 비 = 1 · 0 은 정확히 0 · SE 영률만 · 물리 시간 · 덤프/체크포인트 규칙
  E0   E0 팔 · 다른 강성: 위 + 두 덱 모두 **전 점착 0** (정확히)
  DT   같은 강성 · dt 만 1/k: E · ν · CED 정확히 같다 · dt 정확히 1/k (k = 2 등록) · 정착 · 회전 · 덤프 step 정확히 k 배 · 계획 t₀ 시각 같다
  B    같은 강성 · LC ↔ LH (OLD = LC · NEW = LH): 다섯 쌍 (AM–AM 셋 · AM–벽 둘) 만 증가 · 나머지 전부 **정확히** 같다 · 0 기준 비 N/A
  U    (2026-10-05 · 개발 탐색 dev-u · 강성 축 사전등록 §12) 같은 강성 · LC → LU (OLD = LC · NEW = LU): **9 비영 항 전부 한 공통 배율**
       (퍼짐 max/min − 1 ≤ u_spread_rel) · 배율 > 1 · 벽–벽 0 — 균일 γ 배율 (쌍 집합이 아니라 배율 하나를 허용)
  GM   (2026-10-21 · 원장 MXD2-01 · D2 결합 규칙) 같은 ρ 세계의 NCM 표면 대비 (비코팅 ↔ 코팅): 두 덱 모두 D2 덱 · 같은 강성 · 세대 · γ_W · Bo_SE ·
       NCM 상 γ 만 1 ↔ ρ 로 바뀜 · 바뀌는 CED = 규칙이 정하는 원소 **정확히** — 배수 [√(γ'_iγ'_j)/√(γ_iγ_j)]^(1/3) (AM–AM (1/ρ)^(1/3) · AM–SE · AM–벽
       (1/ρ)^(1/6)) · 나머지 (SE–SE · SE–벽 · 벽–벽) 토큰까지 같다
  D2 덱 (머리에 "D2 결합 규칙 (기하평균" · 2026-10-21 MXD2-01 · 02) 은 표 종류와 무관하게 덱마다 **덱 텍스트에서** 결합 규칙을 다시 검산한다:
       쌍마다 F₀_ij/F₀_SS = √(γ_iγ_j)·R*_ij/R*_SS (머리 선언 γ) · 절대 수준 Bo_SE = F₀_SS / SE 무게 (덱 r · ρ · 중력) = 머리 선언 · Q2 벽 (γ_W = 0.0256·ρ ·
       NCM γ ∈ {1, ρ}) · 겹침 천장 모든 쌍 · 머리 표 (CED · F0/F0_SS · δ0) = 덱 값 · 세대 표기 = 템플릿 밀도 · 덱 옆 deck_meta.json 이 있으면 기록 결합
       (deck_sha256 · schema /2 · 세대 · adhesion_rule γ · γ_W · Bo · 벽 규칙 · ρ · 표면 · 층상 = 덱)
  공통: 파싱 (필수 명령 · run 구조 [1, F, F, N]) · 타입 사전 (밀도 · 반지름 비 · 템플릿 시드 · 메시 타입) = 등록 · 대칭 · 벽–벽 0 ·
        dt = Rayleigh 규칙을 **이 덱의** E · ν · 반지름 · 밀도로 다시 낸 값 (E · E0 · DT 옛 덱: 그대로 · B · U: 정확히 1/k) ·
        허용 밖 명령은 토큰까지 같다 (주석은 **메타**로 따로 센다 — 판정 밖)

허용오차 — 인쇄 형식에서 **비교 전에** 정한다 (결과를 보고 넓히지 않는다 · `TOL`)
  CED `%g` = 6 유효숫자 → 한 값 ≤ 5e-6 · 두 값 배수 ≤ 1e-5 · F₀ ∝ CED³ → 비 ≤ 3e-5 · 같은 참 배율인 두 원소의 배율 퍼짐 ≤ 2e-5 (표 U)
  E · ν 는 **덱 값이 곧 시뮬레이션 값**이라 오차로 치지 않는다 (생성기가 4 유효숫자 밖 경화 배수를 거부 — ST⑧)
  dt `.4g` → 5e-4 (생성기는 반올림 **전** dt 로 step 을 센다) ⇒ 표 E 의 물리 시간 대조 = 2 × 5e-4 × T + 반올림 step
    ⚠ 한계: 그보다 작은 step 변조는 표 E 가 못 잡는다 — `mixer_deck_diff.py --allow E --expect-deck` (재생성 덱 · 전 명령 토큰 동일) 의 몫
  DT 는 정확 (인쇄된 ref dt 의 1/k · 정수배 step) — 1e-12

usage
  python3 scripts/mixer_deck_readback.py --table E  <LC_soft/in.mixer> <LC_ref/in.mixer> \\
                                         --table B  <LC_ref/in.mixer>  <LH_ref/in.mixer> --json out.json --md out.md
  python3 scripts/mixer_deck_readback.py --table U  <LC_ref_r2/in.mixer> <LU212_ref_r2/in.mixer> --json out.json --md out.md
  python3 scripts/mixer_deck_readback.py --table GM <GMuu…/in.mixer> <GMcc…/in.mixer> --json out.json   # 같은 ρ 세계 비코팅 → 코팅 (D2)
  python3 scripts/mixer_deck_readback.py --selftest
"""
import argparse
import collections
import hashlib
import json
import math
import os
import re
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
TOOL = 'scripts/mixer_deck_readback.py'
TOOL_VERSION = 'mixer_deck_readback/3 (2026-10-21 · 밀도 세대 · D2 결합 규칙 · 표 GM)'
KINDS = ('E', 'E0', 'DT', 'B', 'U', 'GM')

#: ── 등록 상수 (사본 — 생성기를 import 하지 않는다) ─────────────────────────────────────────────────────────────
#: 사전등록 docs/reviews/mixer_highbo_stiffness_prereg_20260929.md §3 · 모체 §2-2 · 생성기 TPL_SEED · D_REAL_UM · E_PHASE · PHASE_MECH
REG_TYPES = {1: 'AM_P', 2: 'AM_S', 3: 'SE', 4: 'WALL'}
REG_TPL_SEED = {10487: 'AM_P', 11887: 'AM_S', 13901: 'SE'}
#: ★ 밀도 세대 (2026-10-21 · 원장 MXD2-01) — 생성기 DENS_GENERATIONS 의 AM · SE (kg/m³ · 덱의 `density constant`).  옛 판은 gen1 하나만 등록해
#   lab 세대 덱 (4850 · 1640) 을 타입 사전에서 거부했다.  덱의 세대 = 템플릿 밀도가 맞는 **하나의** 세대 (셀프테스트 MX⑦ 이 생성기 표와 대조).
REG_DENSITY_GEN = {'gen1': {'AM': 4800.0, 'SE': 2000.0}, 'lab20261014': {'AM': 4850.0, 'SE': 1640.0}}
REG_DENSITY = REG_DENSITY_GEN['gen1']                                 # 옛 이름 (gen1 · 보고 호환)
REG_G = 9.81                                                          # 덱 `fix gravi … gravity` (D2 절대 수준 Bo = F₀_SS / SE 무게)
#: ── D2 결합 규칙 (2026-10-21 · MXD2-01 · 02) — 생성기 머리 주석의 꼴 사본 · 벽 Hare 2026 0.0256 사본 ───────────────────────────────────
GM_WALL = (0.04 / 0.25) ** 2
D2_MARK = 'D2 결합 규칙 (기하평균'
D2_HEAD = '★ ' + D2_MARK                                              # D2 덱 머리 블록의 첫 줄 (생성기 _gm_header)
D2_WALL_NCM, D2_WALL_EXPLICIT = 'hare2026_x_rho_uncoated_ncm', 'explicit_coated'
D2_META_SCHEMA = 'mixer_deck_meta/2'
D2_NCM = ('AM_P', 'AM_S')                                             # Q2 (벽 = 비코팅 NCM) 가 다루는 상
OVL_CEILING = 0.01
_RE_D2_DECL = re.compile(r'γ/γ_SE: AM_P (\S+) · AM_S (\S+) · SE (\S+) · γ_W/γ_SE (\S+) · SE–SE Bo_code (\S+) \(')
_RE_D2_NCM = re.compile(r'벽 = 비코팅 NCM 에 묶음 .*× ρ_비코팅 (\S+) = (\S+) —')
_RE_D2_EXP = re.compile(r'벽 γ_W/γ_SE = 명시 입력 (\S+) — .*함의 ρ = γ_W/0\.0256 = (\S+)$')
_RE_D2_SURF = re.compile(r'NCM 표면 [^:]*: AM_P (코팅|비코팅) · AM_S (코팅|비코팅) · 삽입 = (층상|균일)')
_RE_D2_ROW = re.compile(r'^(AM_P|AM_S|SE|WALL)–(AM_P|AM_S|SE|WALL)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)%$')
_RE_DENS_HDR = re.compile(r'★ 밀도 세대 dens_gen = (\S+) ')
_RE_DEC = re.compile(r'(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?')  # 머리 주석의 수 토큰 (`:g` · `.6g` · `.4f` 인쇄 · 양수)
REG_D_UM = {'AM_P': 9.0, 'AM_S': 4.0, 'SE': 1.0}                      # 소재 지름 — 반지름 **비**만 대조한다 (CGF 무관)
REG_E_FIXED = {'AM_P': 1.037e9, 'AM_S': 1.037e9, 'WALL': 1.48e9}      # 강성 축에서 불변이어야 할 영률 (SE 만 경화)
REG_E_SE = {1.0e7: 'soft (×1)', 2.0e8: 'ref (×20 · v2.6)', 4.0e8: 'ref2 (×40 · v2.6)',
            1.4e8: 'v2.5 ref (×14 · DEV7 실측 뒤 개정)', 2.8e8: 'v2.5 ref2 (×28)'}
REG_NU = {'AM_P': 0.25, 'AM_S': 0.25, 'SE': 0.30, 'WALL': 0.30}
REG_DT_K = 2                                                          # DEV `E0_ref@dt/2`
PAIRS = (('AM_P', 'AM_P'), ('AM_P', 'AM_S'), ('AM_S', 'AM_S'), ('AM_P', 'SE'), ('AM_S', 'SE'), ('SE', 'SE'),
         ('AM_P', 'WALL'), ('AM_S', 'WALL'), ('SE', 'WALL'), ('WALL', 'WALL'))
B_PAIRS = {('AM_P', 'AM_P'), ('AM_P', 'AM_S'), ('AM_S', 'AM_S'), ('AM_P', 'WALL'), ('AM_S', 'WALL')}
#: Codex 7 차 §5 독립 산술 (E* 배수, 필요한 CED 배수) — soft → ×F.  AM–AM · AM–벽 은 E* 불변 ⇒ (1, 1).
_UNITY = {p: (1.0, 1.0) for p in (('AM_P', 'AM_P'), ('AM_P', 'AM_S'), ('AM_S', 'AM_S'), ('AM_P', 'WALL'), ('AM_S', 'WALL'))}
CODEX = {14.0: {**_UNITY, ('AM_P', 'SE'): (12.412672571, 5.360971926), ('AM_S', 'SE'): (12.412672571, 5.360971926),
                ('SE', 'SE'): (14.0, 5.808785734), ('SE', 'WALL'): (12.876543210, 5.493715853)},
         28.0: {**_UNITY, ('AM_P', 'SE'): (22.123962626, 7.880890212), ('AM_S', 'SE'): (22.123962626, 7.880890212),
                ('SE', 'SE'): (28.0, 9.220872584), ('SE', 'WALL'): (23.704545455, 8.251908834)},
         #  ★ v2.6 (09-30 밤 · 1저자 비준) ×20 · ×40 — Codex 표가 아니라 **우리 산술** (E* = 1/((1−ν₁²)/E₁ + (1−ν₂²)/E₂) · CED 배수 = E* 배수^(2/3) ·
         #    같은 식이 ×14 · ×28 에서 위 Codex 7 차 값과 9 자리 일치) — Codex 10 차가 독립 검산할 자리
         20.0: {**_UNITY, ('AM_P', 'SE'): (16.85060601, 6.572698075), ('AM_S', 'SE'): (16.85060601, 6.572698075),
                ('SE', 'SE'): (20.0, 7.368062997), ('SE', 'WALL'): (17.738095238, 6.801499256)},
         40.0: {**_UNITY, ('AM_P', 'SE'): (28.909279805, 9.419434887), ('AM_S', 'SE'): (28.909279805, 9.419434887),
                ('SE', 'SE'): (40.0, 11.696070953), ('SE', 'WALL'): (31.70212766, 10.016721683)}}

#: ── 허용오차 — 인쇄 형식에서 비교 **전에** (결과를 보고 넓히지 않는다) ─────────────────────────────────────────
CED_SIG, DT_SIG, RADIUS_SIG = 6, 4, 6
_U6 = 0.5 * 10.0 ** (1 - 6)                                  # 5e-6 — 6 유효숫자로 찍힌 값 하나의 반올림 상한 (CED %g · 머리 :g / .6g · 반지름 .6g)
TOL = dict(
    ced_value_rel=0.5 * 10.0 ** (1 - CED_SIG),                # 5e-6  — CED 한 값 (`%g` 6 유효숫자)
    ced_mult_rel=2 * 0.5 * 10.0 ** (1 - CED_SIG),             # 1e-5  — 두 CED 의 배수
    f0_ratio=3 * 2 * 0.5 * 10.0 ** (1 - CED_SIG),             # 3e-5  — F₀ ∝ CED³ 의 비
    radius_ratio_rel=2 * 0.5 * 10.0 ** (1 - RADIUS_SIG),      # 1e-5  — 반지름 비 (`:.6g`)
    rayleigh_rel=0.5 * 10.0 ** (1 - DT_SIG) + 0.5 * 10.0 ** (1 - RADIUS_SIG),   # 5.05e-4 — 덱 dt (.4g) ↔ 덱 값으로 다시 낸 Rayleigh dt
    codex_estar_rel=1e-9,                                     # Codex 산술 (9–10 자리) ↔ 덱 E 로 계산한 E* 배수
    dt_print_rel=0.5 * 10.0 ** (1 - DT_SIG),                  # 5e-4  — dt `.4g` (생성기는 반올림 전 dt 로 step 을 센다)
    exact_rel=1e-12,                                          # DT 표 · 정수배 · 같은 인쇄 토큰
    u_spread_rel=2 * 2 * 0.5 * 10.0 ** (1 - CED_SIG),         # 2e-5  — 표 U: 같은 참 배율인 두 원소의 배율 퍼짐 (배율 하나 = 두 반올림 · 두 원소)
    #  ── D2 결합 규칙 (2026-10-21 · MXD2-01 · 02) — 인쇄 형식에서 비교 **전에** (u = 6 유효숫자 하나 = 5e-6) ───────────────────────────
    gm_law_rel=9 * _U6,      # 4.5e-5 — F₀_ij/F₀_SS ↔ √(γ_iγ_j)·R*_ij/R*_SS: CED³ 두 쌍 6u · R* 한 제곱 남음 두 쌍 2u · 선언 γ 의 √ u
    gm_bo_rel=5 * _U6,       # 2.5e-5 — Bo_SE = F₀_SS / SE 무게: CED³ 3u · r (F₀ ∝ R*² · 무게 ∝ r³ ⇒ r⁻¹) u · 선언 Bo u (ρ · g 는 덱 토큰 그대로)
    gm_hdr_rel=11 * _U6,     # 5.5e-5 — 머리 표 칸 (R* · E* · F0 · F0/F0_SS) ↔ 덱 값: 비 칸이 가장 넓다 (CED³ 6u · R*² 4u · 머리 인쇄 u)
    gm_q2_rel=2 * _U6,       # 1e-5  — Q2 (γ_W = 0.0256·ρ · NCM γ ∈ {1, ρ} · 명시 벽 함의 ρ): 찍힌 두 값
    gm_mult_rel=2 * _U6 + (2.0 / 3.0) * _U6,   # 1.33e-5 — 표 GM: CED 배수 (두 반올림) · 기대 배수 [√(γ'γ')/√(γγ)]^(1/3) 의 선언 γ 넷
    gm_ovl_rel=4 * _U6,      # 2e-5  — δ0/min r (∝ CED² · R* / E*² / r): 덱 값에서 다시 낸 겹침
    gm_ovl_abs=0.5e-4,       # 머리 표 δ0 칸은 `.4f` % — 퍼센트 점 0.5e-4
)
TOL_WHY = dict(
    ced_value_rel='CED 는 %g (6 유효숫자) 로 찍힌다 — 한 값의 반올림 상한 0.5×10^(1−6)',
    ced_mult_rel='두 CED 의 배수 = 두 반올림',
    f0_ratio='F₀ ∝ CED³ ⇒ 비의 상한 = 3 × 두 반올림.  E · ν 는 덱 값 = 시뮬레이션 값 (생성기가 인쇄 밖 배수를 거부) 이라 넣지 않는다',
    radius_ratio_rel='템플릿 반지름 :.6g 두 값',
    rayleigh_rel='덱 dt 는 .4g · 다시 낸 규칙 dt 는 반지름 :.6g 에서 — 둘의 인쇄 반올림 (dt 가 규칙과 2 배 넘게 어긋나는 것을 잡는 검사다)',
    codex_estar_rel='Codex 7 차 §5 표는 9–10 자리로 적혀 있다',
    dt_print_rel='timestep 은 .4g — 생성기가 반올림 전 dt 로 step 을 세므로 두 덱의 물리 시간이 이만큼 어긋날 수 있다',
    exact_rel='DT 표 (dt 정확히 1/k · step 정확히 k 배) · 부동소수 비교 여유',
    u_spread_rel='표 U — 원소 하나의 배율 오차 ≤ 두 반올림 (1e-5) ⇒ 같은 참 배율인 두 원소 배율의 max/min − 1 ≤ 2 × 1e-5',
    gm_law_rel='D2 법칙 — 덱 CED (6 자리) 로 다시 낸 F₀ 비 (∝ CED³ · 두 쌍) · 템플릿 반지름 (6 자리 · R* 는 가중 평균이라 u) · 머리 선언 γ (√) ⇒ 9u',
    gm_bo_rel='D2 절대 수준 — F₀_SS ∝ R*²·CED³ · SE 무게 ∝ r³ (같은 r 이라 r⁻¹ 만 남음) · 선언 Bo 6 자리 ⇒ 5u (밀도 · 중력 = 덱 토큰 그대로)',
    gm_hdr_rel='머리 표 칸 = 생성기의 참값을 6 자리로 · 되읽기는 찍힌 CED · 반지름에서 ⇒ 비 칸 11u (다른 칸은 그 안)',
    gm_q2_rel='Q2 — 머리에 찍힌 두 값 (γ_W ↔ ρ · γ ↔ ρ) 의 반올림',
    gm_mult_rel='표 GM — 두 덱 CED 의 배수 (2u) + 머리 선언 γ 넷이 기대 배수에 주는 (2/3)u',
    gm_ovl_rel='겹침 δ0 = (3π·CED·√R*/(2E*))² / min r — CED² 2u · R* u · r u',
    gm_ovl_abs='머리 표 δ0/min r 칸 `.4f` % 인쇄 (퍼센트 점)',
)
DUMP_RULE = 'dump 간격 = max(1000, 회전 step // 200)'
RAYLEIGH_RULE = 'dt = min_t 0.2·π·r_t·√(ρ_t/G_t)/(0.1631ν_t + 0.8766) · G = E/(2(1+ν)) (생성기 plan() 의 식 사본)'
RESTART_RULE = 'restart 간격 = max(50000, min(200000, (회전 step 또는 2·정착 step) // 20))'


def dump_rule(n_run):
    return max(1000, n_run // 200)


def restart_rule(n_fill, n_run):
    return max(50_000, min(200_000, (n_run or 2 * n_fill) // 20))


def rayleigh_dt(D):
    """덱의 E · ν · 템플릿 반지름 · 밀도로 다시 낸 Rayleigh 규칙 dt 와 그것을 정한 상 (생성기 plan() 의 식 **사본**).

    ⚠ 이 검사가 없으면 SE 를 경화하고 dt 를 다시 안 센 덱 (soft dt 0.7055 µs = 경화 SE 한계 0.3132 µs 의 2.25 배 → 적분 불안정) 이
      물리 시간 · 덤프 · 체크포인트 규칙 · 쌍별 CED 를 **전부 통과**한다 (셀프테스트 ⑱ — 2026-09-30 C 설계 중 발견)."""
    best = None
    for k, tpl in sorted(D['templates'].items()):
        E, nu = D['E'][k - 1], D['nu'][k - 1]
        G = E / (2.0 * (1.0 + nu))
        dt = 0.2 * math.pi * tpl['radius'] * math.sqrt(tpl['density'] / G) / (0.1631 * nu + 0.8766)
        if best is None or dt < best[0]:
            best = (dt, D['names'].get(k, str(k)))
    return best


def planned_t0(n_fill, dump_every):
    """계획 t₀ = 정착 끝 직전 덤프 격자점 ⌊2F/D⌋·D (판독기 measure_mixing_index.planned_t0 와 같은 정의 — 사본)."""
    return (2 * n_fill // dump_every) * dump_every


# ══ 파서 (덱 텍스트만) ══════════════════════════════════════════════════════════════════════════════════════════
def _logical(text):
    """덱 → [(첫 줄 번호, 토큰, 주석)].  LIGGGHTS 규칙: 줄의 마지막 인쇄 문자가 `&` 면 다음 줄과 잇는다 · `#` 부터 끝은 주석."""
    lines = text.split('\n')
    out, i = [], 0
    while i < len(lines):
        start, buf = i, [lines[i]]
        while buf[-1].rstrip().endswith('&') and i + 1 < len(lines):
            i += 1
            buf.append(lines[i])
        joined = ' '.join(b.rstrip()[:-1] if b.rstrip().endswith('&') else b for b in buf)
        code, _, com = joined.partition('#')
        out.append((start + 1, code.split(), com.strip()))
        i += 1
    return out


def read_deck(text, label=None, path=None, meta=None):
    """덱 텍스트 → dict (E · ν · CED (토큰 · 값) · 템플릿 · 메시 타입 · dt · run · 덤프 · 체크포인트 · Drum 주기 · 중력 · 밀도 세대 · 타입 사전 · 문제).
    ★ `meta` (2026-10-21 · MXD2-02) = 덱 옆 `deck_meta.json` 의 내용 (없으면 None) — `d2_check` 가 덱과 결합해 본다 (덱 sha256 · 세대 · D2 선언)."""
    raw = text.encode('utf-8')
    D = dict(label=label, path=path, sha256=hashlib.sha256(raw).hexdigest(), bytes=len(raw), problems=[], type_problems=[],
             n_types=None, E=None, nu=None, ced=None, ced_tok=None, ced_n=None, templates={}, mesh_types=[], dt_txt=None, dt=None,
             runs=[], dump_every=None, restart_every=None, period=None, cmds=[], comments=[], names={},
             gravity=None, dens_gen=None, dens_decl=[], meta=meta)
    seen = collections.Counter()
    for ln, t, com in _logical(text):
        if com:
            D['comments'].append(com)
            md_ = _RE_DENS_HDR.match(com)
            if md_:
                D['dens_decl'].append(md_.group(1))
        if not t:
            continue
        D['cmds'].append((ln, t))
        try:
            key = None
            if t[0] == 'create_box':
                key = 'create_box'
                D['n_types'] = int(t[1])
            elif t[0] == 'timestep':
                key = 'timestep'
                D['dt_txt'], D['dt'] = t[1], float(t[1])
            elif t[0] == 'run':
                D['runs'].append(int(t[1]))
            elif t[0] == 'dump':
                key = 'dump'
                D['dump_every'] = int(t[4])
            elif t[0] == 'restart':
                key = 'restart'
                D['restart_every'] = int(t[1])
            elif t[0] == 'fix' and len(t) >= 4:
                st = t[3]
                if st == 'property/global' and len(t) >= 6:
                    if t[4] in ('youngsModulus', 'poissonsRatio') and t[5] == 'peratomtype':
                        key = t[4]
                        D['E' if key == 'youngsModulus' else 'nu'] = [float(x) for x in t[6:]]
                    elif t[4] == 'cohesionEnergyDensity' and t[5] == 'peratomtypepair':
                        key = 'cohesionEnergyDensity'
                        n = int(t[6])
                        vals = t[7:]
                        if len(vals) != n * n:
                            raise ValueError(f'CED 값 {len(vals)} 개 ≠ {n}×{n}')
                        D['ced_n'] = n
                        D['ced_tok'] = {(i + 1, j + 1): vals[i * n + j] for i in range(n) for j in range(n)}
                        D['ced'] = {k: float(v) for k, v in D['ced_tok'].items()}
                elif st.startswith('particletemplate/'):
                    at = int(t[t.index('atom_type') + 1])
                    if at in D['templates']:
                        raise ValueError(f'atom_type {at} 템플릿이 둘이다')
                    D['templates'][at] = dict(style=st, seed=int(t[4]),
                                              density=float(t[t.index('density') + 2]) if 'density' in t else None,
                                              radius=float(t[t.index('radius') + 2]) if 'radius' in t else None)
                elif st == 'mesh/surface' and 'type' in t:
                    D['mesh_types'].append(int(t[t.index('type') + 1]))
                elif st == 'move/mesh' and len(t) > 5 and t[5] == 'Drum' and 'period' in t:
                    key = 'Drum 주기'
                    D['period'] = float(t[t.index('period') + 1])
                elif st == 'gravity' and len(t) >= 5:          # (2026-10-21 · D2 절대 수준 Bo = F₀_SS / SE 무게 — 덱의 중력)
                    key = 'gravity'
                    D['gravity'] = float(t[4])
            if key:
                seen[key] += 1
        except (ValueError, IndexError) as e:
            D['problems'].append(f'줄 {ln}: `{" ".join(t)[:70]}` — 읽을 수 없다 ({e})')
    for k_, n_ in seen.items():
        if n_ > 1:
            D['problems'].append(f'{k_} 명령이 {n_} 개 — 하나여야 한다')
    for fld, name in (('n_types', 'create_box'), ('E', 'youngsModulus'), ('nu', 'poissonsRatio'), ('ced', 'cohesionEnergyDensity'),
                      ('dt', 'timestep'), ('dump_every', 'dump'), ('restart_every', 'restart'), ('period', 'Drum 회전 주기')):
        if D[fld] is None:
            D['problems'].append(f'{name} 이 없다')
    R = D['runs']
    if not (len(R) == 4 and R[0] == 1 and R[1] == R[2] and R[1] > 0 and R[3] >= 0):
        D['problems'].append(f'run 구조 {R} ≠ [1, F, F, N] (삽입 · 정착 ×2 · 회전)')
    N = D['n_types']
    if N is not None:
        for fld, name in (('E', '영률'), ('nu', 'ν')):
            if D[fld] is not None and len(D[fld]) != N:
                D['problems'].append(f'{name} 값 {len(D[fld])} 개 ≠ create_box {N}')
        if D['ced_n'] is not None and D['ced_n'] != N:
            D['problems'].append(f'CED 행렬 {D["ced_n"]}×{D["ced_n"]} ≠ create_box {N}')
    if not D['problems']:
        D['dens_gen'] = _dens_gen_of(D['templates'])
        D['names'], D['type_problems'] = _type_dict(D)
    return D


def _dens_gen_of(tpl):
    """템플릿 밀도 → 등록 세대 이름 — 입자 템플릿 밀도의 **집합**이 그 세대의 {AM, SE} 와 정확히 같을 때만 (못 정하면 None)."""
    dens = {v['density'] for v in tpl.values()}
    hits = [g for g, d in REG_DENSITY_GEN.items() if dens == {d['AM'], d['SE']}]
    return hits[0] if len(hits) == 1 else None


def _type_dict(D):
    """타입 번호 → 상 이름 — **밀도 · 반지름 · 메시**로 판정하고 템플릿 시드 (등록 사본) 로 교차 대조한다.  → (이름 사전, 문제).
    ★ 2026-10-21 (MXD2-01) — 밀도는 **세대별** 등록값 (REG_DENSITY_GEN) 으로 가른다 · 머리의 세대 표기 (`★ 밀도 세대 dens_gen = …`) 는
      템플릿 밀도로 판정한 세대와 같아야 한다 (표기 없음 = gen1 만 · 옛 덱 그대로)."""
    probs, names = [], {}
    N, tpl = D['n_types'], D['templates']
    walls = sorted(set(D['mesh_types']))
    if walls != [N]:
        probs.append(f'메시 (벽) 타입 {walls} ≠ [create_box {N}] — 벽 = 마지막 타입이어야 한다')
    if N in tpl:
        probs.append(f'벽 타입 {N} 에 입자 템플릿이 있다')
    names[N] = 'WALL'
    if any(v['style'] != 'particletemplate/sphere' for v in tpl.values()):
        probs.append('구가 아닌 템플릿 (섬유 multisphere) — 등록 3 상 밖')
    gen = D.get('dens_gen')
    reg = REG_DENSITY_GEN.get(gen)
    if reg is None:
        probs.append(f'입자 템플릿 밀도 {sorted({v["density"] for v in tpl.values()})} 가 등록 밀도 세대 어느 것과도 맞지 않는다 ('
                     + ' · '.join(f'{g_} AM {d_["AM"]:g} · SE {d_["SE"]:g}' for g_, d_ in REG_DENSITY_GEN.items()) + ')')
        return names, probs
    am = sorted((k for k, v in tpl.items() if v['density'] == reg['AM']), key=lambda k: -(tpl[k]['radius'] or 0.0))
    se = [k for k, v in tpl.items() if v['density'] == reg['SE']]
    if len(am) != 2 or len(se) != 1 or len(tpl) != 3 or sorted(tpl) != list(range(1, N)):
        probs.append(f'입자 템플릿이 등록 3 상 (세대 {gen}: 밀도 {reg["AM"]:g} 둘 · {reg["SE"]:g} 하나 · 타입 1..{N - 1}) 이 아니다: '
                     f'{ {k: (v["density"], v["radius"]) for k, v in sorted(tpl.items())} }')
        return names, probs
    dd = D.get('dens_decl') or []
    if len(dd) > 1:
        probs.append(f'밀도 세대 머리 표기가 {len(dd)} 개 ({dd}) — 하나여야 한다')
    elif not dd and gen != 'gen1':
        probs.append(f'밀도 세대 머리 표기가 없다 — 템플릿 밀도는 세대 {gen} (표기 없는 덱 = gen1 만 · 생성기 _dens_header)')
    elif dd and dd[0] != gen:
        probs.append(f'밀도 세대 머리 표기 {dd[0]} ≠ 템플릿 밀도로 판정한 세대 {gen}')
    if tpl[am[0]]['radius'] == tpl[am[1]]['radius']:
        probs.append('AM 두 상의 반지름이 같다 — AM_P / AM_S 를 가를 수 없다')
    names[am[0]], names[am[1]], names[se[0]] = 'AM_P', 'AM_S', 'SE'
    r = {names[k]: tpl[k]['radius'] for k in tpl}
    for a, b in (('AM_P', 'AM_S'), ('SE', 'AM_P')):
        want, got = REG_D_UM[a] / REG_D_UM[b], r[a] / r[b]
        if abs(got / want - 1.0) > TOL['radius_ratio_rel']:
            probs.append(f'반지름 비 {a}/{b} {got:.7g} ≠ 등록 {want:.7g}')
    for k, v in sorted(tpl.items()):
        sn = REG_TPL_SEED.get(v['seed'])
        if sn != names.get(k):
            probs.append(f'타입 {k}: 템플릿 시드 {v["seed"]} (등록 → {sn}) ≠ 밀도 · 반지름 판정 {names.get(k)}')
    if names != REG_TYPES:
        probs.append(f'타입-상 대응 {dict(sorted(names.items()))} ≠ 등록 {REG_TYPES}')
    return dict(sorted(names.items())), probs


# ══ 쌍 물리 (덱 값에서) ══════════════════════════════════════════════════════════════════════════════════════════
def _phases(D):
    """상 이름 → dict(type, E, nu, r) — r 는 템플릿 반지름 (벽 None)."""
    return {ph: dict(type=k, E=D['E'][k - 1], nu=D['nu'][k - 1], r=None if ph == 'WALL' else D['templates'][k]['radius'])
            for k, ph in D['names'].items()}


def estar(a, b):
    """E*_ij = [(1−ν_i²)/E_i + (1−ν_j²)/E_j]⁻¹ (벽 = 덱에 선언된 벽 E · ν)."""
    return 1.0 / ((1.0 - a['nu'] ** 2) / a['E'] + (1.0 - b['nu'] ** 2) / b['E'])


def rstar(a, b):
    """R* — 입자쌍 r_i·r_j/(r_i+r_j) · 벽 (평면) = r_입자."""
    if a['r'] is None:
        a, b = b, a
    if b['r'] is None:
        return a['r']
    return a['r'] * b['r'] / (a['r'] + b['r'])


def f0(ced, rs, es):
    """명목 소겹침 점착 힘 척도 F₀ = B³/A² = (9/2)π³R*²CED³/E*² (N) — A = (4/3)E*√R* · B = 2πR*·CED."""
    return 4.5 * math.pi ** 3 * rs ** 2 * ced ** 3 / es ** 2


def overlap(ced, rs, es, rmin):
    """점착 지배 평형 겹침 δ0 = (B/A)² = (3π·CED·√R*/(2E*))² 를 작은 반경으로 나눈 값 (생성기 pair_overlap 의 식 **사본** · 벽 = 입자 반경)."""
    return (3.0 * math.pi * ced * math.sqrt(rs) / (2.0 * es)) ** 2 / rmin


# ══ D2 결합 규칙 (2026-10-21 · 원장 MXD2-01 · 02) — 덱 텍스트에서 다시 검산 ═══════════════════════════════════════════════
#  왜 — 옛 되읽기는 gen1 밀도만 등록해 lab 세대 덱을 타입 사전에서 거부했고, D2 덱의 결합 규칙 (쌍마다 기하평균 · 절대 수준 Bo · Q2 벽 ·
#    머리 표 · 기록) 을 덱 텍스트에서 볼 경로가 없었다 (사전 공격 리뷰 PRE-01 · 02 · 변이 M04 · M15 · M16 이 살아남은 자리).
#  ★ 선언 (머리 주석) 은 **주장**이고 검산 대상이다 — 값은 덱의 CED · E · ν · 템플릿 반지름 · 밀도 · 중력 토큰에서 다시 낸다.
def _dec(tok):
    """머리 주석의 수 토큰 → float — ASCII 십진수 (지수 허용) · 유한만 (아니면 None · nan · inf · 밑줄 · 전각 거부)."""
    if not isinstance(tok, str) or not _RE_DEC.fullmatch(tok):
        return None
    v = float(tok)
    return v if math.isfinite(v) else None


def _near(x, y, tol):
    return x is not None and y is not None and y != 0.0 and math.isfinite(x) and abs(x / y - 1.0) <= tol


def _d2_decl(D, P):
    """D2 머리 선언 (γ/γ_SE 줄 · 벽 규칙 줄 · NCM 표면 · 삽입 줄 · 쌍 표) → dict 또는 None (읽을 수 없으면 사유를 P 에)."""
    com = D['comments']

    def one(rx, what):
        hits = [m for m in (rx.search(c) for c in com) if m]
        if len(hits) != 1:
            P.append(f'D2 머리: {what} 줄 {len(hits)} 개 — 정확히 하나여야 한다')
            return None
        return hits[0]
    md, ms = one(_RE_D2_DECL, 'γ/γ_SE 선언 (γ · γ_W · Bo_SE)'), one(_RE_D2_SURF, 'NCM 표면 · 삽입')
    mn = [m for m in (_RE_D2_NCM.search(c) for c in com) if m]
    me = [m for m in (_RE_D2_EXP.search(c) for c in com) if m]
    if len(mn) + len(me) != 1:
        P.append(f'D2 머리: 벽 규칙 줄 (비코팅 NCM 묶음 {len(mn)} · 명시 벽 {len(me)}) — 정확히 하나여야 한다')
        return None
    if md is None or ms is None:
        return None
    tok = dict(AM_P=md.group(1), AM_S=md.group(2), SE=md.group(3), gw=md.group(4), bo=md.group(5))
    if mn:
        rule, rho_tok, gw2 = D2_WALL_NCM, mn[0].group(1), mn[0].group(2)
    else:
        rule, gw2, rho_tok = D2_WALL_EXPLICIT, me[0].group(1), me[0].group(2)
    tok['rho'] = rho_tok
    num = {k: _dec(v) for k, v in tok.items()}
    bad = {k: tok[k] for k, v in num.items() if v is None or not v > 0.0}
    if bad:
        P.append(f'D2 머리: 선언 수 {bad} — ASCII 십진수 · 유한 양수가 아니다')
        return None
    if gw2 != tok['gw']:
        P.append(f"D2 머리: 벽 규칙 줄의 γ_W/γ_SE {gw2} ≠ 선언 줄 {tok['gw']}")
    table, dup = {}, []
    for c in com:
        m = _RE_D2_ROW.match(c)
        if m:
            k = f'{m.group(1)}–{m.group(2)}'
            if k in table:
                dup.append(k)
            table[k] = dict(R_star=m.group(3), E_star=m.group(4), CED=m.group(5), F0=m.group(6), ratio=m.group(7), ovl=m.group(8))
    want = [f'{a}–{b}' for a, b in PAIRS if not (a == b == 'WALL')]
    if dup or sorted(table) != sorted(want):
        P.append(f'D2 머리 표: 쌍 {sorted(table)} (중복 {dup}) ≠ 등록 9 쌍 (벽–벽 제외)')
    return dict(gamma={t: num[t] for t in ('AM_P', 'AM_S', 'SE')}, gamma_wall=num['gw'], bo_se=num['bo'], wall_rule=rule, rho=num['rho'],
                surface={'AM_P': 'coated' if ms.group(1) == '코팅' else 'uncoated', 'AM_S': 'coated' if ms.group(2) == '코팅' else 'uncoated'},
                layered=ms.group(3) == '층상', tokens=tok, table=table, dens_gen=D.get('dens_gen'))


def _tokg(v):
    """메타 수 값 → 머리와 같은 `:g` 토큰 (수가 아니면 repr — 결코 머리 토큰과 같지 않다)."""
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        return f'<{v!r}>'
    return f'{v:g}'


def _meta_problems(D, R):
    """덱 옆 deck_meta.json ↔ 덱 결합.  모든 덱: 세대 (메타 dens_gen 없음 = gen1).  D2 덱: schema /2 · deck_sha256 · 세대 명시 ·
    adhesion_rule (rule · γ · γ_W · Bo · 벽 규칙 · ρ · 표면 · 층상) = 덱 머리 선언 (같은 `:g` 토큰)."""
    m = D.get('meta')
    if m is None:
        return []
    d2 = R['is_d2']
    pre = 'D2 기록 (deck_meta.json)' if d2 else '기록 (deck_meta.json)'
    if not isinstance(m, dict):
        return [f'{pre}: JSON 사전이 아니다 ({type(m).__name__})']
    if '__unreadable__' in m:
        return [f"{pre}: 읽을 수 없다 ({m['__unreadable__']})"]
    P = []
    gen = D.get('dens_gen')
    mg = m.get('dens_gen', None if d2 else 'gen1')
    if gen is not None and mg != gen:
        P.append(f"{pre}: dens_gen {m.get('dens_gen')!r} ≠ 덱 템플릿 밀도의 세대 {gen}")
    if not d2:
        return P
    if m.get('schema') != D2_META_SCHEMA:
        P.append(f"{pre}: schema {m.get('schema')!r} ≠ {D2_META_SCHEMA} (D2 키를 담은 메타)")
    if m.get('deck_sha256') != D['sha256']:
        P.append(f"{pre}: deck_sha256 {str(m.get('deck_sha256'))[:16]}… ≠ 이 덱 {D['sha256'][:16]}…")
    ar = m.get('adhesion_rule')
    if not isinstance(ar, dict):
        P.append(f'{pre}: adhesion_rule 이 없다 — D2 덱의 메타는 결합 규칙을 기록한다')
        return P
    if ar.get('rule') != 'geomean':
        P.append(f"{pre}: adhesion_rule.rule {ar.get('rule')!r} ≠ 'geomean'")
    dc = R.get('decl')
    if dc is None:
        return P
    tk = dc['tokens']
    gm = ar.get('gamma')
    if not isinstance(gm, dict) or sorted(gm) != ['AM_P', 'AM_S', 'SE'] or any(_tokg(gm[t]) != tk[t] for t in ('AM_P', 'AM_S', 'SE')):
        P.append(f"{pre}: adhesion_rule.gamma {gm!r} ≠ 덱 머리 선언 γ (AM_P {tk['AM_P']} · AM_S {tk['AM_S']} · SE {tk['SE']})")
    for key, t_, what in (('gamma_wall', 'gw', 'γ_W/γ_SE'), ('bo_se', 'bo', 'SE–SE Bo_code (절대 수준)')):
        if _tokg(ar.get(key)) != tk[t_]:
            P.append(f'{pre}: adhesion_rule.{key} {ar.get(key)!r} ≠ 덱 머리 {what} {tk[t_]}')
    if ar.get('wall_rule') != dc['wall_rule']:
        P.append(f"{pre}: adhesion_rule.wall_rule {ar.get('wall_rule')!r} ≠ 덱 머리 벽 규칙 {dc['wall_rule']}")
    rk = 'rho_uncoated_ncm' if dc['wall_rule'] == D2_WALL_NCM else 'rho_world'
    if _tokg(ar.get(rk)) != tk['rho']:
        P.append(f"{pre}: adhesion_rule.{rk} {ar.get(rk)!r} ≠ 덱 머리 ρ {tk['rho']}")
    if ar.get('surface') != dc['surface']:
        P.append(f"{pre}: adhesion_rule.surface {ar.get('surface')!r} ≠ 덱 머리 NCM 표면 {dc['surface']}")
    if not isinstance(ar.get('layered'), bool) or ar.get('layered') != dc['layered']:
        P.append(f"{pre}: adhesion_rule.layered {ar.get('layered')!r} ≠ 덱 머리 삽입 ({'층상' if dc['layered'] else '균일'})")
    return P


def d2_check(D):
    """D2 결합 규칙 덱 검산 — 덱 텍스트 (CED · E · ν · 템플릿 반지름 · 밀도 · 중력) 에서 다시 낸 값 ↔ 머리 선언 · 머리 표 · (있으면) deck_meta.

    → dict(is_d2, decl, rows, bo_read, problems).  옛 팔 덱 (D2 머리 없음 · 메타도 D2 아님) = is_d2 False (메타 세대 대조만).
      · 쌍마다 F₀_ij/F₀_SS = √(γ_iγ_j)·R*_ij/R*_SS (γ_WALL = γ_W · 허용 gm_law_rel) · 겹침 δ0/min r ≤ 1 % (모든 쌍)
      · 절대 수준 Bo_SE = F₀_SS / ((4/3)π r_SE³ ρ_SE g) = 머리 선언 (gm_bo_rel) — M04 꼴 (다른 세대 밀도로 정한 CED) 을 잡는다
      · Q2 (1저자 10-14): 벽 = 비코팅 NCM ⇒ γ_W = 0.0256·ρ · NCM γ ∈ {1, ρ} · 명시 벽 = NCM γ 전부 1 · 함의 ρ = γ_W/0.0256 · 표면 줄 = γ
      · 머리 표 (R* · E* · CED · F0 · F0/F0_SS · δ0) = 덱 값 — M15 꼴 · 세대 표기 = 템플릿 밀도 · 삽입 줄 = 덱의 insert/pack 수
    결과는 D['_d2'] 에 담아 둔다 (같은 덱을 여러 표가 쓴다)."""
    if '_d2' in D:
        return D['_d2']
    R = dict(is_d2=False, decl=None, rows=[], bo_read=None, problems=[])
    D['_d2'] = R
    P = R['problems']
    heads = sum(1 for c in D['comments'] if c.startswith(D2_HEAD))
    meta = D.get('meta')
    R['is_d2'] = heads > 0 or (isinstance(meta, dict) and 'adhesion_rule' in meta)
    if not R['is_d2']:
        P += _meta_problems(D, R)
        return R
    names_ok = sorted(D['names'].values()) == sorted(REG_TYPES.values())
    if D['problems'] or not names_ok:
        P.append('덱 파싱 · 타입 사전 문제 — D2 검산 불가: ' + '; '.join((D['problems'] + D['type_problems'])[:4]))
        P += _meta_problems(D, R)
        return R
    P += [f'타입 사전: {x}' for x in D['type_problems']]       # (세대 표기 ↔ 템플릿 밀도 등 — 이름은 정해졌다)
    if heads == 0:
        P.append(f'D2 기록 (deck_meta.json): 메타는 D2 결합 규칙 (adhesion_rule) 인데 덱 머리에 "{D2_HEAD}" 선언이 없다')
        P += _meta_problems(D, R)
        return R
    if heads > 1:
        P.append(f'D2 머리 줄 "{D2_HEAD}" 이 {heads} 개 — 하나여야 한다')
    dc = _d2_decl(D, P)
    R['decl'] = dc
    if dc is None:
        P += _meta_problems(D, R)
        return R
    g, q = dc['gamma'], TOL['gm_q2_rel']
    tk = dc['tokens']
    if g['SE'] != 1.0:
        P.append(f"D2 머리: 기준 γ_SE/γ_SE = {tk['SE']} — 정확히 1 이어야 한다")
    q2 = '1저자 10-14 Q2 — 벽 = 비코팅 NCM'
    if dc['wall_rule'] == D2_WALL_NCM:
        if not _near(dc['gamma_wall'], GM_WALL * dc['rho'], q):
            P.append(f"Q2 — γ_W/γ_SE {tk['gw']} ≠ 0.0256 × ρ_비코팅 {tk['rho']} = {GM_WALL * dc['rho']:.6g} ({q2})")
        off = {t: tk[t] for t in D2_NCM if not (_near(g[t], 1.0, q) or _near(g[t], dc['rho'], q))}
        if off:
            P.append(f"Q2 — ρ_비코팅 {tk['rho']} 세계의 NCM 상 γ/γ_SE 는 1 (코팅) 또는 ρ (비코팅) 만: {off} ({q2})")
        allowed = {t: ({'coated'} if _near(g[t], 1.0, q) else set()) | ({'uncoated'} if _near(g[t], dc['rho'], q) else set()) for t in D2_NCM}
    else:
        off = {t: tk[t] for t in D2_NCM if not _near(g[t], 1.0, q)}
        if off:
            P.append(f'Q2 — 명시 벽 (explicit_coated) 은 NCM 상 γ 전부 1 (코팅) 인 팔만: {off} ({q2})')
        if not _near(dc['rho'], dc['gamma_wall'] / GM_WALL, q):
            P.append(f"Q2 — 명시 벽의 함의 ρ {tk['rho']} ≠ γ_W/0.0256 = {dc['gamma_wall'] / GM_WALL:.6g} ({q2})")
        allowed = {t: ({'coated'} if _near(g[t], 1.0, q) else set()) for t in D2_NCM}
    for t in D2_NCM:
        if dc['surface'][t] not in allowed[t]:
            P.append(f"D2 머리: NCM 표면 {t} {'코팅' if dc['surface'][t] == 'coated' else '비코팅'} ≠ γ {tk[t]} "
                     f"(코팅 = γ 1 · 비코팅 = γ ρ {tk['rho']} · {q2})")
    n_ins = sum(1 for _, t in D['cmds'] if t[0] == 'fix' and len(t) > 3 and t[3] == 'insert/pack')
    if dc['layered'] != (n_ins == 2):
        P.append(f"D2 머리: 삽입 = {'층상' if dc['layered'] else '균일'} ≠ 덱의 insert/pack {n_ins} 개 (층상 = insA · insB 둘)")
    V = _phases(D)
    gam = dict(g, WALL=dc['gamma_wall'])
    sk = (V['SE']['type'], V['SE']['type'])
    rss, ess = rstar(V['SE'], V['SE']), estar(V['SE'], V['SE'])
    fss = f0(D['ced'][sk], rss, ess)
    if not (math.isfinite(fss) and fss > 0.0):
        P.append(f'SE–SE CED {D["ced_tok"][sk]} — F₀_SS 가 유한한 양수가 아니다 (D2 절대 수준 없음)')
        P += _meta_problems(D, R)
        return R
    rho_se, r_se, grav = D['templates'][V['SE']['type']]['density'], V['SE']['r'], D.get('gravity')
    if grav is None or not (math.isfinite(grav) and grav > 0.0):
        P.append(f'중력 (fix … gravity) {grav!r} — 절대 수준 Bo 를 다시 낼 수 없다')
    else:
        R['bo_read'] = fss / ((4.0 / 3.0) * math.pi * r_se ** 3 * rho_se * grav)
        if not _near(R['bo_read'], dc['bo_se'], TOL['gm_bo_rel']):
            P.append(f"절대 수준 Bo_SE = F₀_SS / SE 무게 (덱 r {r_se:g} · ρ {rho_se:g} · g {grav:g}) = {R['bo_read']:.7g} ≠ 머리 선언 "
                     f"SE–SE Bo_code {tk['bo']} (허용 ±{TOL['gm_bo_rel']:.1e} · MXD2-02)")
    tab = dc['table']
    for ti, tj in PAIRS:
        a, b = V[ti], V[tj]
        key = (a['type'], b['type'])
        c = D['ced'][key]
        nm = f'{ti}–{tj}'
        r_ = dict(pair=nm, types=f'{key[0]}-{key[1]}', CED=c, reason='')
        if ti == tj == 'WALL':
            r_['ok'] = c == 0.0
            r_['reason'] = '' if r_['ok'] else f'벽–벽 CED {D["ced_tok"][key]} ≠ 0'
            R['rows'].append(r_)
            continue
        rs, es = rstar(a, b), estar(a, b)
        f = f0(c, rs, es)
        rmin = min(x['r'] for x in (a, b) if x['r'] is not None)
        ov = overlap(c, rs, es, rmin)
        ratio = f / fss
        expect = math.sqrt(gam[ti] * gam[tj]) * rs / rss
        r_.update(R_star=rs, E_star=es, F0=f, F0_ratio=ratio, expect=expect, overlap=ov, tol=TOL['gm_law_rel'])
        why = []
        if not (c > 0.0 and math.isfinite(c)):
            why.append(f'CED {D["ced_tok"][key]} — 벽–벽 밖 CED 는 유한한 양수여야 한다')
        elif not _near(ratio, expect, TOL['gm_law_rel']):
            why.append(f"F₀_ij/F₀_SS {ratio:.7g} ≠ 규칙 √(γ_iγ_j)·R*_ij/R*_SS {expect:.7g} (머리 선언 γ · 허용 ±{TOL['gm_law_rel']:.1e})")
        if not ov <= OVL_CEILING * (1.0 + TOL['gm_ovl_rel']):
            why.append(f'겹침 δ0/min r {ov * 100:.4f} % > 천장 {OVL_CEILING * 100:g} % (D2 = 모든 쌍)')
        h = tab.get(nm)
        if h is None:
            why.append('머리 표에 이 쌍이 없다')
        else:
            if h['CED'] != D['ced_tok'][key]:
                why.append(f"머리 표 CED {h['CED']} ≠ 덱 토큰 {D['ced_tok'][key]}")
            for col, val, tol_ in (('R_star', rs, TOL['gm_hdr_rel']), ('E_star', es, TOL['gm_hdr_rel']), ('F0', f, TOL['gm_hdr_rel']),
                                   ('ratio', ratio, TOL['gm_hdr_rel'])):
                hv = _dec(h[col])
                if not _near(hv, val, tol_):
                    why.append(f"머리 표 {'F0/F0_SS' if col == 'ratio' else col} {h[col]} ≠ 덱 값 {val:.7g} (허용 ±{tol_:.1e})")
            hv = _dec(h['ovl'])
            if hv is None or abs(hv - ov * 100.0) > TOL['gm_ovl_abs'] + TOL['gm_ovl_rel'] * ov * 100.0:
                why.append(f"머리 표 δ0/min r {h['ovl']}% ≠ 덱 값 {ov * 100:.6f}%")
        r_['ok'] = not why
        r_['reason'] = ' · '.join(why)
        if why:
            P.append(f'{nm}: ' + ' · '.join(why))
        R['rows'].append(r_)
    P += _meta_problems(D, R)
    return R


# ══ 표 ═══════════════════════════════════════════════════════════════════════════════════════════════════════
def _var_positions(t, kind):
    """이 표 종류에서 **달라도 되는** 토큰 위치 (값은 따로 검사한다).  나머지 토큰은 전부 같아야 한다."""
    steps = kind in ('E', 'E0', 'DT')
    if steps:
        if t[0] in ('timestep', 'run', 'restart'):
            return {1}
        if t[0] == 'dump':
            return {4}
    if t[0] == 'fix' and len(t) > 5 and t[3] == 'property/global':
        if kind in ('E', 'E0') and t[4] == 'youngsModulus':
            return set(range(6, len(t)))
        if kind in ('E', 'E0', 'B', 'U', 'GM') and t[4] == 'cohesionEnergyDensity':
            return set(range(7, len(t)))
    return set()


def _cmd_diff(A, B, kind):
    ca, cb = A['cmds'], B['cmds']
    out = []
    if len(ca) != len(cb):
        out.append(f'명령 수 {len(ca)} ≠ {len(cb)}')
    for (la, ta), (lb, tb) in zip(ca, cb):
        if ta[0] != tb[0] or len(ta) != len(tb):
            out.append(f'줄 {la}/{lb}: `{" ".join(ta)[:80]}` ⇄ `{" ".join(tb)[:80]}`')
            continue
        var = _var_positions(ta, kind)
        if any(x != y for q, (x, y) in enumerate(zip(ta, tb)) if q not in var):
            out.append(f'줄 {la}/{lb}: `{" ".join(ta)[:80]}` ⇄ `{" ".join(tb)[:80]}`')
    return out


def _final(T):
    head = f"{T['kind']} {T['old']} → {T['new']}"
    T['failures'] = ([f"{head}: {c['check']}" + (f" ({c['detail']})" if c['detail'] else '') for c in T['checks'] if not c['ok']]
                     + [f"{head}: 쌍 {r_['pair']} — {r_.get('reason') or '실패'}" for r_ in T['rows'] if not r_.get('ok')])
    T['verdict'] = 'PASS' if not T['failures'] else 'FAIL'
    return T


def compare(kind, A, B):
    """두 되읽은 덱 → 표 dict (kind · rows · checks · meta · failures · verdict).  kind ∈ E · E0 · DT · B · U · GM.
    ★ D2 덱 (또는 메타가 있는 덱) 은 표 종류와 무관하게 `d2_check` 검사가 덱마다 붙는다 (2026-10-21 · MXD2-01 · 02)."""
    T = dict(kind=kind, old=A['label'], new=B['label'], old_sha256=A['sha256'], new_sha256=B['sha256'],
             rows=[], checks=[], meta={}, k=None, level=None, verdict=None, failures=[])

    def check(name, cond, detail=''):
        T['checks'].append(dict(check=name, ok=bool(cond), detail=str(detail)))
        return bool(cond)
    if kind not in KINDS:
        check(f'표 종류 {kind!r} ∈ {KINDS}', False)
        return _final(T)
    for X in (A, B):
        check(f'덱 파싱 — {X["label"]} (필수 명령 · run 구조 [1, F, F, N] · 행렬 크기)', not X['problems'], '; '.join(X['problems']))
    if A['problems'] or B['problems']:
        return _final(T)
    for X in (A, B):
        check(f'타입 사전 = 등록 1 AM_P · 2 AM_S · 3 SE · 4 WALL (밀도 · 반지름 비 · 템플릿 시드 · 메시 타입) — {X["label"]}',
              not X['type_problems'], '; '.join(X['type_problems']))
    if A['type_problems'] or B['type_problems']:
        return _final(T)
    check('두 덱의 템플릿 (시드 · 밀도 · 반지름) · 타입 사전 동일', A['templates'] == B['templates'] and A['names'] == B['names'])
    for X in (A, B):
        R2 = d2_check(X)
        if R2['is_d2']:
            check(f'D2 결합 규칙 — 덱 텍스트 검산 (쌍별 기하평균 F₀ · 절대 수준 Bo · Q2 벽 · 겹침 천장 · 머리 표 · 세대 · 기록) — {X["label"]}',
                  not R2['problems'], '; '.join(R2['problems'][:12]) + (f' … 외 {len(R2["problems"]) - 12}' if len(R2['problems']) > 12 else ''))
        elif X.get('meta') is not None:
            check(f'기록 (deck_meta.json) = 덱 (밀도 세대 · 결합 규칙) — {X["label"]}', not R2['problems'], '; '.join(R2['problems']))
    if kind in ('E', 'E0', 'DT'):
        #  ★ 같은 팔 (2026-10-21 · MXD2-02) — D2 덱과 옛 팔 덱을 짝짓지 않는다 · 두 D2 덱의 선언 (γ · γ_W · Bo · ρ · 벽 규칙 · 표면 · 삽입) 이 같다
        RA_, RB_ = d2_check(A), d2_check(B)
        if RA_['is_d2'] or RB_['is_d2']:
            ka, kb = ((tuple(sorted(R_['decl']['tokens'].items())), R_['decl']['wall_rule'], tuple(sorted(R_['decl']['surface'].items())),
                       R_['decl']['layered']) if R_['decl'] else None for R_ in (RA_, RB_))
            check(f'{kind} 는 같은 팔 — 두 덱 모두 D2 이고 D2 선언 (γ · γ_W · Bo · ρ · 벽 규칙 · 표면 · 삽입) 이 같다',
                  RA_['is_d2'] and RB_['is_d2'] and ka is not None and ka == kb, f'{ka} ⇄ {kb}')
    N = A['n_types']
    VA, VB = _phases(A), _phases(B)
    for X, V in ((A, VA), (B, VB)):
        tok = X['ced_tok']
        check(f'CED 행렬 대칭 (인쇄 토큰까지) · 벽–벽 = 0 — {X["label"]}',
              all(tok[(i, j)] == tok[(j, i)] for i in range(1, N + 1) for j in range(1, N + 1)) and X['ced'][(N, N)] == 0.0)
        check(f'CED 전부 유한 · 비음수 — {X["label"]}', all(math.isfinite(v) and v >= 0.0 for v in X['ced'].values()))
        check(f'ν = 등록 (AM 0.25 · SE 0.30 · 벽 0.30) — {X["label"]}', all(V[ph]['nu'] == REG_NU[ph] for ph in REG_NU))
        check(f'AM · 벽 영률 = 등록 (1.037e9 · 1.037e9 · 1.48e9) · SE 영률 = 등록 수준 (1e7 · 1.4e8 · 2.8e8) — {X["label"]}',
              all(V[ph]['E'] == REG_E_FIXED[ph] for ph in REG_E_FIXED) and V['SE']['E'] in REG_E_SE,
              f"SE {V['SE']['E']:g} · AM_P {V['AM_P']['E']:g} · AM_S {V['AM_S']['E']:g} · 벽 {V['WALL']['E']:g}")
    rule_k = {}
    for X in (A, B):
        rule, by = rayleigh_dt(X)
        k_ = max(1, int(round(rule / X['dt'])))
        rule_k[X['label']] = k_
        if kind in ('E', 'E0') or (kind == 'DT' and X is A):
            check(f'dt = Rayleigh 규칙 (이 덱의 E · ν · 반지름 · 밀도 · 상별 최소) — {X["label"]}',
                  abs(X['dt'] / rule - 1.0) <= TOL['rayleigh_rel'],
                  f"덱 {X['dt_txt']} vs 규칙 {rule:.6g} s ({by} 가 정함 · 비 {X['dt'] / rule:.6f} · 허용 ±{TOL['rayleigh_rel']:.2e})")
        elif kind in ('B', 'U', 'GM'):
            check(f'dt = Rayleigh 규칙의 정확히 1/k (k 정수 ≥ 1 · k = 1 이면 규칙 그대로) — {X["label"]}',
                  abs(X['dt'] * k_ / rule - 1.0) <= TOL['rayleigh_rel'],
                  f"덱 {X['dt_txt']} × {k_} vs 규칙 {rule:.6g} s ({by})")
    if kind in ('B', 'U', 'GM'):
        T['k'] = rule_k[A['label']] if rule_k[A['label']] == rule_k[B['label']] else None
    ca, cb = collections.Counter(A['comments']), collections.Counter(B['comments'])
    only_a, only_b = ca - cb, cb - ca
    T['meta'] = dict(comment_only_old=sum(only_a.values()), comment_only_new=sum(only_b.values()),
                     examples_new=[c[:100] for c in list(only_b)[:3]],
                     note='주석 (팔 설명 · 강성 머리 블록 · 출처) — 허용 메타 (판정 밖)')
    diffs = _cmd_diff(A, B, kind)
    allowed = {'E': 'SE 영률 · CED 값 · timestep · run · dump 간격 · restart 간격',
               'E0': 'SE 영률 · CED 값 · timestep · run · dump 간격 · restart 간격',
               'DT': 'timestep · run · dump 간격 · restart 간격', 'B': 'CED 값', 'U': 'CED 값', 'GM': 'CED 값'}[kind]
    check(f'허용 밖 명령은 토큰까지 같다 (허용: {allowed})', not diffs, '; '.join(diffs[:4]) + (f' … 외 {len(diffs) - 4}' if len(diffs) > 4 else ''))
    FA, FB, NA, NB = A['runs'][1], B['runs'][1], A['runs'][3], B['runs'][3]
    DA, DB, dtA, dtB = A['dump_every'], B['dump_every'], A['dt'], B['dt']
    if kind in ('E', 'E0'):
        F = VB['SE']['E'] / VA['SE']['E']
        T['level'] = dict(old=REG_E_SE.get(VA['SE']['E'], '미등록'), new=REG_E_SE.get(VB['SE']['E'], '미등록'), F=F)
        check('SE 영률만 바뀌었다 — AM_P · AM_S · 벽 영률 정확히 같다 · ν 전부 같다 · SE 는 **달라야** 한다 (E 비교)',
              all(VA[ph]['E'] == VB[ph]['E'] for ph in ('AM_P', 'AM_S', 'WALL')) and A['nu'] == B['nu'] and F != 1.0,
              f'SE ×{F:g}')
        codex = next((CODEX[c] for c in CODEX if VA['SE']['E'] == 1.0e7 and abs(F - c) <= TOL['exact_rel'] * c), None)
        T['codex_level'] = None if codex is None else F
        for ti, tj in PAIRS:
            a, b, a2, b2 = VA[ti], VA[tj], VB[ti], VB[tj]
            key = (a['type'], b['type'])
            co, cn = A['ced'][key], B['ced'][key]
            r_ = dict(pair=f'{ti}–{tj}', types=f'{key[0]}-{key[1]}', CED_old=co, CED_new=cn, codex='N/A', reason='')
            if ti == tj == 'WALL':
                r_.update(ok=(co == 0.0 and cn == 0.0), F0_ratio=None)
                r_['reason'] = '' if r_['ok'] else f'벽–벽 ≠ 0 ({co:g} → {cn:g})'
                T['rows'].append(r_)
                continue
            rs, eo, en = rstar(a, b), estar(a, b), estar(a2, b2)
            fo, fn = f0(co, rs, eo), f0(cn, rs, en)
            r_.update(R_star=rs, Estar_old=eo, Estar_new=en, Estar_mult=en / eo, CED_mult=(cn / co) if co else None,
                      F0_old=fo, F0_new=fn, F0_ratio=None, tol=TOL['f0_ratio'] if co else None)   # 0 기준 = 정확히 0 (허용 없음)
            if co == 0.0:
                r_['ok'] = cn == 0.0
                r_['reason'] = '' if r_['ok'] else f'0 → {cn:g} (0 은 정확히 0 이어야 한다)'
            elif not (cn > 0.0 and math.isfinite(cn)):
                r_['ok'], r_['reason'] = False, f'{co:g} → {cn:g} (비영 항이 0 · 음수 · 비유한)'
            else:
                r_['F0_ratio'] = fn / fo
                r_['ok'] = abs(r_['F0_ratio'] - 1.0) <= TOL['f0_ratio']
                r_['reason'] = '' if r_['ok'] else f"F₀ 비 {r_['F0_ratio']:.6f} (허용 ±{TOL['f0_ratio']:.0e})"
            if codex is not None and (ti, tj) in codex:
                em, cm = codex[(ti, tj)]
                cok = abs(r_['Estar_mult'] / em - 1.0) <= TOL['codex_estar_rel'] and (co == 0.0 or abs(r_['CED_mult'] / cm - 1.0) <= TOL['ced_mult_rel'])
                r_['codex'] = 'PASS' if cok else 'FAIL'
                r_['codex_expect'] = dict(Estar_mult=em, CED_mult=cm)
                if not cok:
                    r_['ok'] = False
                    r_['reason'] = (r_['reason'] + ' · ' if r_['reason'] else '') + \
                        f"Codex 배수 불일치 (E* ×{r_['Estar_mult']:.9f} vs {em} · CED ×{(r_['CED_mult'] or 0):.6f} vs {cm})"
            T['rows'].append(r_)
        if kind == 'E0':
            check('전 점착 0 — 두 덱 CED 전 원소 정확히 0 (E0)', all(v == 0.0 for v in A['ced'].values()) and all(v == 0.0 for v in B['ced'].values()))
        tsA, tsB = 2 * FA * dtA, 2 * FB * dtB
        tol_s = 2 * TOL['dt_print_rel'] * max(tsA, tsB) + dtA + dtB
        check('물리 시간 — 정착 2F·dt 같다 (허용 = dt 인쇄 2 × 5e-4 · T + 반올림 1 step 씩)', abs(tsA - tsB) <= tol_s,
              f'{tsA:.9g} → {tsB:.9g} s (차 {tsB - tsA:+.3g} · 허용 {tol_s:.3g})')
        trA, trB = NA * dtA, NB * dtB
        tol_r = 2 * TOL['dt_print_rel'] * max(trA, trB) + 0.5 * (dtA + dtB)
        check('물리 시간 — 회전 N·dt 같다 (= 바퀴 수 같다 · Drum 주기는 명령 대조로 같다)', abs(trA - trB) <= tol_r,
              f'{trA:.9g} → {trB:.9g} s = {trA / A["period"]:.6f} → {trB / B["period"]:.6f} 바퀴 (차 {trB - trA:+.3g} s · 허용 {tol_r:.3g})')
        check(f'덤프 간격 = 등록 규칙 ({DUMP_RULE}) — 두 덱', DA == dump_rule(NA) and DB == dump_rule(NB),
              f'{DA} (규칙 {dump_rule(NA)}) → {DB} (규칙 {dump_rule(NB)})')
        check(f'체크포인트 간격 = 등록 규칙 ({RESTART_RULE}) — 두 덱',
              A['restart_every'] == restart_rule(FA, NA) and B['restart_every'] == restart_rule(FB, NB),
              f"{A['restart_every']} (규칙 {restart_rule(FA, NA)}) → {B['restart_every']} (규칙 {restart_rule(FB, NB)})")
        t0A, t0B = planned_t0(FA, DA) * dtA, planned_t0(FB, DB) * dtB
        check('계획 t₀ 물리 시각 — 차 ≤ 덤프 간격 하나 (t₀ = 정착 끝 직전 덤프 격자점)', abs(t0A - t0B) <= max(DA * dtA, DB * dtB) + tol_s,
              f'{t0A:.9g} → {t0B:.9g} s (step {planned_t0(FA, DA)} → {planned_t0(FB, DB)})')
    elif kind == 'DT':
        kr = dtA / dtB
        k = int(round(kr))
        T['k'] = k
        check('dt 가 정확히 1/k (k 정수 ≥ 2 · 인쇄된 dt 대조 1e-12)', k >= 2 and abs(dtB * k / dtA - 1.0) <= TOL['exact_rel'],
              f"{A['dt_txt']} → {B['dt_txt']} (비 {kr:.12g})")
        check(f'k = {REG_DT_K} (등록 E0_ref@dt/2)', k == REG_DT_K, f'k {k}')
        check('E · ν · CED (인쇄 토큰) · 템플릿 정확히 같다 — dt 만 다르다',
              A['E'] == B['E'] and A['nu'] == B['nu'] and A['ced_tok'] == B['ced_tok'] and A['templates'] == B['templates'])
        check('run 1 (삽입 step) 그대로 · 정착 · 회전 step 정확히 k 배',
              A['runs'][0] == B['runs'][0] == 1 and B['runs'][1:] == [k * x for x in A['runs'][1:]], f"{A['runs']} → {B['runs']}")
        check('덤프 간격 step 정확히 k 배 (덤프 시각 불변)', DB == k * DA, f'{DA} → {DB}')
        check(f'체크포인트 간격 = 등록 규칙 (새 step · {RESTART_RULE})', B['restart_every'] == restart_rule(FB, NB),
              f"{B['restart_every']} (규칙 {restart_rule(FB, NB)})")
        t0A, t0B = planned_t0(FA, DA) * dtA, planned_t0(FB, DB) * dtB
        check('계획 t₀ 물리 시각 같다 (1e-12)', abs(t0B / t0A - 1.0) <= TOL['exact_rel'] if t0A else t0B == 0.0,
              f'step {planned_t0(FA, DA)} → {planned_t0(FB, DB)} · {t0A:.12g} → {t0B:.12g} s')
        sA, sB = A['period'] / dtA, B['period'] / dtB
        check('바퀴당 step 정확히 k 배 (bin 경계 물리 시각 같다)', abs(sB / sA - k) <= TOL['exact_rel'] * max(k, 1), f'{sA:.9g} → {sB:.9g}')
        for ti, tj in PAIRS:
            key = (VA[ti]['type'], VA[tj]['type'])
            same = A['ced_tok'][key] == B['ced_tok'][key]
            T['rows'].append(dict(pair=f'{ti}–{tj}', types=f'{key[0]}-{key[1]}', CED_old=A['ced'][key], CED_new=B['ced'][key],
                                  ok=same, reason='' if same else '같아야 할 CED 가 다르다'))
    elif kind == 'GM':
        #  ★ 2026-10-21 (원장 MXD2-01 · D2 결합 규칙) — 같은 ρ 세계의 NCM 표면 대비 (비코팅 ↔ 코팅).  바뀌는 CED = 규칙이 정하는 원소 **정확히**:
        #    배수 [√(γ'_iγ'_j)/√(γ_iγ_j)]^(1/3) (F₀_SS · R* · E* 같다 ⇒ CED ∝ (√(γ_iγ_j))^(1/3)) · 배수 1 인 원소는 토큰까지 같다.
        check('같은 강성 — E · ν 정확히 같다', A['E'] == B['E'] and A['nu'] == B['nu'])
        RA, RB = d2_check(A), d2_check(B)
        both = bool(RA['is_d2'] and RB['is_d2'] and RA['decl'] is not None and RB['decl'] is not None)
        check(f'두 덱 모두 D2 결합 규칙 덱 (머리 "{D2_HEAD}" · γ 선언 · 벽 규칙 · NCM 표면 · 쌍 표를 읽었다)', both,
              f"{A['label']} {'D2' if RA['is_d2'] else '옛 팔'} · {B['label']} {'D2' if RB['is_d2'] else '옛 팔'}")
        if both:
            a_, b_ = RA['decl'], RB['decl']
            dif = [k for k, va, vb in (('밀도 세대', A.get('dens_gen'), B.get('dens_gen')), ('벽 규칙', a_['wall_rule'], b_['wall_rule']),
                                       ('ρ_비코팅', a_['tokens']['rho'], b_['tokens']['rho']), ('γ_W', a_['tokens']['gw'], b_['tokens']['gw']),
                                       ('SE γ', a_['tokens']['SE'], b_['tokens']['SE']), ('Bo_SE', a_['tokens']['bo'], b_['tokens']['bo']),
                                       ('삽입', a_['layered'], b_['layered'])) if va != vb]
            check('같은 ρ 세계 — 밀도 세대 · 벽 규칙 · ρ_비코팅 · γ_W · SE γ · Bo_SE · 삽입이 같다 (NCM 표면만 바뀐다)', not dif,
                  f"다른 칸 {dif} · ρ {a_['tokens']['rho']} → {b_['tokens']['rho']} · γ_W {a_['tokens']['gw']} → {b_['tokens']['gw']} · "
                  f"Bo {a_['tokens']['bo']} → {b_['tokens']['bo']}")
            check('NCM 표면이 바뀌었다 (비코팅 ↔ 코팅 — 같은 표면 둘은 대비가 아니다 · 빈 비교를 PASS 로 내지 않는다)',
                  a_['surface'] != b_['surface'], f"{a_['surface']} → {b_['surface']}")
            ga, gb = dict(a_['gamma'], WALL=a_['gamma_wall']), dict(b_['gamma'], WALL=b_['gamma_wall'])
            for ti, tj in PAIRS:
                key = (VA[ti]['type'], VA[tj]['type'])
                o_, n_ = A['ced'][key], B['ced'][key]
                r_ = dict(pair=f'{ti}–{tj}', types=f'{key[0]}-{key[1]}', CED_old=o_, CED_new=n_, ratio=(n_ / o_) if o_ else None,
                          expect=None, expect_change=False, reason='')
                if ti == tj == 'WALL':
                    r_['ok'] = o_ == 0.0 and n_ == 0.0
                    r_['reason'] = '' if r_['ok'] else f'벽–벽 ≠ 0 ({o_:g} → {n_:g})'
                else:
                    e_ = (math.sqrt(gb[ti] * gb[tj]) / math.sqrt(ga[ti] * ga[tj])) ** (1.0 / 3.0)
                    r_.update(expect=e_, expect_change=(e_ != 1.0))
                    if e_ != 1.0:
                        r_['ok'] = bool(o_ > 0.0 and n_ > 0.0 and math.isfinite(n_) and abs((n_ / o_) / e_ - 1.0) <= TOL['gm_mult_rel'])
                        r_['reason'] = '' if r_['ok'] else (f"배수 ×{(n_ / o_) if o_ else float('nan'):.7g} ≠ 규칙 ×{e_:.7g} "
                                                            f"(γ {ga[ti]:g}·{ga[tj]:g} → {gb[ti]:g}·{gb[tj]:g} · 허용 ±{TOL['gm_mult_rel']:.1e})")
                    else:
                        r_['ok'] = A['ced_tok'][key] == B['ced_tok'][key]
                        r_['reason'] = '' if r_['ok'] else (f'규칙이 안 바꾸는 원소가 바뀌었다 ({A["ced_tok"][key]} → {B["ced_tok"][key]} · '
                                                            f'γ {ga[ti]:g}·{ga[tj]:g} 그대로)')
                T['rows'].append(r_)
    elif kind == 'U':
        #  ★ 2026-10-05 (dev-u · 강성 축 사전등록 §12) — 균일 γ 배율: 9 비영 항 전부 한 공통 배율 · > 1 · 벽–벽 0.  쌍마다의 판정 기준 = 배율의 **중앙값**
        #    (한 원소만 바뀐 덱이면 그 원소만 짚는다) · 표 판정 = 퍼짐 (max/min − 1) + 방향.  배율 표시는 기하평균.
        check('같은 강성 — E · ν 정확히 같다', A['E'] == B['E'] and A['nu'] == B['nu'])
        rat = {}
        for ti, tj in PAIRS:
            key = (VA[ti]['type'], VA[tj]['type'])
            o_, n_ = A['ced'][key], B['ced'][key]
            if o_ > 0.0 and math.isfinite(n_) and n_ > 0.0:
                rat[f'{ti}–{tj}'] = n_ / o_
        med = sorted(rat.values())[len(rat) // 2] if rat else None
        sp = (max(rat.values()) / min(rat.values()) - 1.0) if rat else None
        T['u_ratio'] = math.exp(sum(math.log(v) for v in rat.values()) / len(rat)) if rat else None
        T['u_median'], T['u_spread'] = med, sp
        check('9 비영 항 전부 배율이 있다 (옛 · 새 CED 양수 · 유한 — 0 · 음수 · 비유한 없음)', len(rat) == len(PAIRS) - 1, f'{len(rat)} 항')
        check(f"배율 하나 — 퍼짐 max/min − 1 ≤ {TOL['u_spread_rel']:.0e} (두 덱 CED %g 인쇄 반올림)",
              sp is not None and sp <= TOL['u_spread_rel'],
              f"퍼짐 {sp:.3g} · ×{min(rat.values()):.7g} … ×{max(rat.values()):.7g}" if rat else '배율 없음')
        check('공통 배율 > 1 (같은 γ 세계를 키운다 — 줄어든 덱 · 빈 비교가 아니다)', med is not None and med > 1.0 + TOL['ced_mult_rel'],
              f'중앙값 ×{med:.7g}' if med is not None else '배율 없음')
        for ti, tj in PAIRS:
            key = (VA[ti]['type'], VA[tj]['type'])
            o_, n_ = A['ced'][key], B['ced'][key]
            r_ = dict(pair=f'{ti}–{tj}', types=f'{key[0]}-{key[1]}', CED_old=o_, CED_new=n_, ratio=(n_ / o_) if o_ else None)
            if ti == tj == 'WALL':
                r_['ok'] = o_ == 0.0 and n_ == 0.0
                r_['reason'] = '' if r_['ok'] else f'벽–벽 ≠ 0 ({o_:g} → {n_:g})'
            elif f'{ti}–{tj}' not in rat:
                r_['ok'], r_['reason'] = False, f'{o_:g} → {n_:g} (배율을 낼 수 없다 — 0 · 음수 · 비유한)'
            else:
                r_['ok'] = abs(rat[f'{ti}–{tj}'] / med - 1.0) <= TOL['u_spread_rel']
                r_['reason'] = '' if r_['ok'] else f"배율 ×{rat[f'{ti}–{tj}']:.7g} ≠ 공통 (중앙값) ×{med:.7g} (허용 ±{TOL['u_spread_rel']:.0e})"
            T['rows'].append(r_)
    else:                                                   # B
        check('같은 강성 — E · ν 정확히 같다', A['E'] == B['E'] and A['nu'] == B['nu'])
        for ti, tj in PAIRS:
            key = (VA[ti]['type'], VA[tj]['type'])
            lc, lh = A['ced'][key], B['ced'][key]
            exp = (ti, tj) in B_PAIRS
            r_ = dict(pair=f'{ti}–{tj}', types=f'{key[0]}-{key[1]}', LC=lc, LH=lh, diff=lh - lc,
                      ratio=(lh / lc) if lc else None, expect_change=exp)
            if ti == tj == 'WALL':
                r_['ok'] = lc == 0.0 and lh == 0.0
                r_['reason'] = '' if r_['ok'] else '벽–벽 ≠ 0'
            elif exp:
                r_['ok'] = lh > lc and (lh - lc) > TOL['ced_mult_rel'] * max(lc, lh)
                r_['reason'] = '' if r_['ok'] else ('방향 반대 (LH < LC)' if lh < lc else '개입 누락 (LH = LC)')
            else:
                r_['ok'] = A['ced_tok'][key] == B['ced_tok'][key]
                r_['reason'] = '' if r_['ok'] else f'바뀌면 안 되는 항이 바뀌었다 ({A["ced_tok"][key]} → {B["ced_tok"][key]})'
            T['rows'].append(r_)
    return _final(T)


# ══ 보고 (JSON · markdown) ══════════════════════════════════════════════════════════════════════════════════════
def _gen_cmd(path):
    """덱 옆 `gen_cmd.txt` (없으면 `deck_meta.json` 의 argv) — 없으면 None ('미기록')."""
    d = os.path.dirname(os.path.abspath(path))
    p1, p2 = os.path.join(d, 'gen_cmd.txt'), os.path.join(d, 'deck_meta.json')
    if os.path.exists(p1):
        return open(p1, encoding='utf-8').read().strip()
    if os.path.exists(p2):
        try:
            return 'python3 scripts/make_mixer_deck.py ' + ' '.join(json.load(open(p2, encoding='utf-8')).get('argv', []))
        except (OSError, ValueError):
            return None
    return None


def _load_meta(path):
    """덱 옆 `deck_meta.json` (2026-10-21 · MXD2-02) — 그 메타의 deck_file (기본 in.mixer) 이 이 덱 파일 이름일 때만 결합한다.
    없으면 None · 읽을 수 없으면 {'__unreadable__': 사유} (결합 검사가 실패로 적는다 — 조용히 넘기지 않는다)."""
    mp = os.path.join(os.path.dirname(os.path.abspath(path)), 'deck_meta.json')
    if not os.path.exists(mp):
        return None
    try:
        m = json.load(open(mp, encoding='utf-8'))
    except (OSError, ValueError) as e:
        return {'__unreadable__': f'{type(e).__name__}: {e}'[:200]} if os.path.basename(path) == 'in.mixer' else None
    if isinstance(m, dict) and m.get('deck_file', 'in.mixer') != os.path.basename(path):
        return None
    return m


def load(path):
    text = open(path, encoding='utf-8').read()
    base = os.path.basename(path)
    label = os.path.basename(os.path.dirname(os.path.abspath(path))) if base == 'in.mixer' else base
    D = read_deck(text, label=label, path=path, meta=_load_meta(path))
    D['gen_cmd'] = _gen_cmd(path)
    return D


def deck_summary(D):
    s = dict(label=D['label'], path=D['path'], sha256=D['sha256'], bytes=D['bytes'], gen_cmd=D.get('gen_cmd'),
             problems=D['problems'], type_problems=D['type_problems'], types={str(k): v for k, v in D['names'].items()},
             E=D['E'], nu=D['nu'], dt_txt=D['dt_txt'], runs=D['runs'], dump_every=D['dump_every'],
             restart_every=D['restart_every'], period_s=D['period'],
             templates={str(k): v for k, v in sorted(D['templates'].items())},
             ced={f'{i}-{j}': D['ced_tok'][(i, j)] for (i, j) in sorted(D['ced_tok'] or {}) if i <= j} if D['ced_tok'] else None,
             comment_lines=len(D['comments']), dens_gen=D.get('dens_gen'), gravity=D.get('gravity'),
             meta_bound=D.get('meta') is not None, d2=None)
    if not D['problems']:
        R2 = d2_check(D)
        if R2['is_d2']:
            dc = R2['decl'] or {}
            s['d2'] = dict(wall_rule=dc.get('wall_rule'), gamma=dc.get('gamma'), gamma_wall=dc.get('gamma_wall'), bo_se=dc.get('bo_se'),
                           bo_read=R2['bo_read'], rho=dc.get('rho'), surface=dc.get('surface'), layered=dc.get('layered'),
                           problems=R2['problems'])
        elif R2['problems']:
            s['meta_problems'] = R2['problems']
    if not D['problems'] and D['dt']:
        t0 = planned_t0(D['runs'][1], D['dump_every'])
        s.update(t0_planned=t0, t0_planned_s=t0 * D['dt'], steps_per_rev=D['period'] / D['dt'],
                 settle_s=2 * D['runs'][1] * D['dt'], rotation_s=D['runs'][3] * D['dt'])
    return s


def make_report(decks, tables, argv=None):
    me = os.path.abspath(__file__)
    fails = [f for T in tables for f in T['failures']]
    return dict(tool=TOOL, tool_version=TOOL_VERSION, tool_sha256=hashlib.sha256(open(me, 'rb').read()).hexdigest(),
                argv=list(argv or []), tolerances=TOL, tolerances_why=TOL_WHY,
                registered=dict(types={str(k): v for k, v in REG_TYPES.items()},
                                template_seeds={str(k): v for k, v in REG_TPL_SEED.items()}, density=REG_DENSITY, d_um=REG_D_UM,
                                E_fixed=REG_E_FIXED, E_SE_levels={f'{k:g}': v for k, v in REG_E_SE.items()}, nu=REG_NU,
                                B_pairs=sorted(f'{a}–{b}' for a, b in B_PAIRS),
                                U_rule='9 비영 항 (AM–AM 셋 · AM–SE 둘 · SE–SE · AM–벽 둘 · SE–벽) 전부 한 공통 배율 (퍼짐 ≤ u_spread_rel) · '
                                       '배율 > 1 · 벽–벽 0 · 같은 E · ν (2026-10-05 · dev-u · 강성 축 사전등록 §12)',
                                density_generations=REG_DENSITY_GEN, gravity=REG_G,
                                D2_rule=('F₀_ij/F₀_SS = √(γ_iγ_j)·R*_ij/R*_SS (γ_WALL = γ_W · 머리 선언) · Bo_SE = F₀_SS / ((4/3)π r_SE³ ρ_SE g) = 선언 · '
                                         'Q2 (1저자 10-14): 벽 = 비코팅 NCM ⇒ γ_W = 0.0256·ρ · NCM γ ∈ {1, ρ} · 명시 벽 = NCM γ 전부 1 · '
                                         f'모든 쌍 δ0/min r ≤ {OVL_CEILING:g} · 머리 표 = 덱 값 · deck_meta (있으면) = 덱 (2026-10-21 · MXD2-01 · 02)'),
                                D2_wall_hare2026=GM_WALL,
                                GM_rule=('같은 ρ 세계 (세대 · 벽 규칙 · ρ · γ_W · SE γ · Bo · 삽입 같다) · NCM 표면만 바뀜 · 바뀌는 CED = '
                                         '[√(γ\'_iγ\'_j)/√(γ_iγ_j)]^(1/3) ≠ 1 인 원소 정확히 (배수 · 허용 gm_mult_rel) · 나머지 토큰까지 같다'),
                                dt_k=REG_DT_K, dump_rule=DUMP_RULE,
                                restart_rule=RESTART_RULE, rayleigh_rule=RAYLEIGH_RULE,
                                codex_section5={f'{F:g}': {f'{a}–{b}': list(v) for (a, b), v in c.items()} for F, c in CODEX.items()}),
                decks={p: deck_summary(D) for p, D in decks.items()}, tables=tables,
                verdict='PASS' if not fails and tables else 'FAIL', failures=fails)


def _g(v, spec='.6g'):
    return '—' if v is None else format(v, spec)


def to_markdown(rep):
    n = len(rep['tables'])
    npass = sum(T['verdict'] == 'PASS' for T in rep['tables'])
    t = rep['tolerances']
    L = [f"# 믹서 실행 덱 되읽기 — `{rep['tool']}` ({rep['tool_version']})", '',
         f"- 판정 **{rep['verdict']}** — 표 {npass}/{n} PASS · 도구 sha256 `{rep['tool_sha256'][:16]}…`",
         f"- 허용오차 (비교 **전** · 인쇄 형식에서): F₀ 비 ±{t['f0_ratio']:.0e} · CED 배수 ±{t['ced_mult_rel']:.0e} · "
         f"Codex E* ±{t['codex_estar_rel']:.0e} · dt 인쇄 {t['dt_print_rel']:.0e} (표 E 물리 시간) · DT 표 정확 {t['exact_rel']:.0e}",
         '- 계산: 덱 텍스트에서 되읽은 E · ν · 반지름 (템플릿) · CED 로 E*_ij = [(1−ν_i²)/E_i + (1−ν_j²)/E_j]⁻¹ · '
         'R* (입자쌍 r_i r_j/(r_i+r_j) · 벽 = r) · F₀ = (9/2)π³R*²CED³/E*² — **생성기를 import 하지 않는다**',
         '', '## 덱', '',
         '| 라벨 | sha256 (앞 16) | bytes | SE 영률 | dt | run (삽입 · 정착 · 정착 · 회전) | 덤프 | 체크포인트 | 생성 명령 |',
         '|---|---|---:|---:|---:|---|---:|---:|---|']
    for p, d in rep['decks'].items():
        se = d['E'][2] if d['E'] and len(d['E']) > 2 else None
        #  ⚠ sha256 앞자리는 **백틱 없이** — docs/ 의 check_doc_refs 가 백틱 안 hex 를 커밋 SHA 로 읽는다 (셀프테스트 ㉑)
        L.append(f"| `{d['label']}` | {d['sha256'][:16]} | {d['bytes']:,} | {_g(se, '.4g')} | {d['dt_txt']} | "
                 f"{' · '.join(f'{x:,}' for x in d['runs'])} | {_g(d['dump_every'], ',')} | {_g(d['restart_every'], ',')} | "
                 f"{('`' + d['gen_cmd'] + '`') if d['gen_cmd'] else '미기록'} |")
    d2s = [(d['label'], d.get('dens_gen'), d['d2']) for d in rep['decks'].values() if d.get('d2')]
    if d2s:
        L += ['', '## D2 덱 (덱 텍스트에서 다시 낸 결합 규칙)', '',
              '| 라벨 | 세대 | 벽 규칙 | ρ | γ (AM_P · AM_S) | γ_W | Bo 선언 → 다시 낸 값 | NCM 표면 | 문제 |', '|---|---|---|---:|---|---:|---|---|---:|']
        for lb, gen_, x in d2s:
            gmm = x.get('gamma') or {}
            L.append(f"| `{lb}` | {gen_} | {x.get('wall_rule')} | {_g(x.get('rho'), 'g')} | {_g(gmm.get('AM_P'), 'g')} · {_g(gmm.get('AM_S'), 'g')} | "
                     f"{_g(x.get('gamma_wall'), 'g')} | {_g(x.get('bo_se'), 'g')} → {_g(x.get('bo_read'), '.7g')} | {x.get('surface')} | "
                     f"{len(x.get('problems') or [])} |")
    for T in rep['tables']:
        L += ['', f"## 표 {T['kind']} — `{T['old']}` → `{T['new']}` — **{T['verdict']}**", '']
        if T['kind'] in ('E', 'E0'):
            lv = T.get('level') or {}
            L += [f"SE 영률 {lv.get('old', '?')} → {lv.get('new', '?')} (×{_g(lv.get('F'), 'g')}) · "
                  f"Codex 7 차 §5 대조: {'×' + format(T['codex_level'], 'g') if T.get('codex_level') else 'N/A (soft → ×14 · ×28 만 등록)'}", '',
                  '| 쌍 | 타입 | R* (m) | E*_old → E*_new (Pa) | E* 배수 | CED_old → CED_new (J/m³) | CED 배수 | F₀_old → F₀_new (N) | F₀ 비 | 허용 | Codex | 판정 |',
                  '|---|---|---:|---|---:|---|---:|---|---:|---:|---|---|']
            for r_ in T['rows']:
                L.append(f"| {r_['pair']} | {r_['types']} | {_g(r_.get('R_star'))} | {_g(r_.get('Estar_old'))} → {_g(r_.get('Estar_new'))} | "
                         f"{_g(r_.get('Estar_mult'), '.9g')} | {_g(r_['CED_old'])} → {_g(r_['CED_new'])} | {_g(r_.get('CED_mult'), '.7g')} | "
                         f"{_g(r_.get('F0_old'))} → {_g(r_.get('F0_new'))} | {_g(r_.get('F0_ratio'), '.9f')} | "
                         f"{('±' + format(r_['tol'], '.0e')) if r_.get('tol') else ('0 = 0' if r_['CED_old'] == 0 else '—')} | "
                         f"{r_.get('codex', 'N/A')} | {'PASS' if r_['ok'] else 'FAIL · ' + r_['reason']} |")
        elif T['kind'] == 'U':
            L += [f"공통 배율 ×{_g(T.get('u_ratio'), '.7g')} (기하평균 · 쌍 판정 기준 = 중앙값 ×{_g(T.get('u_median'), '.7g')}) · "
                  f"퍼짐 {_g(T.get('u_spread'), '.3g')} (허용 {t['u_spread_rel']:.0e}) · k = {T.get('k')}", '',
                  '| 쌍 | 타입 | 옛 CED (J/m³) | 새 CED (J/m³) | 배율 | 판정 |', '|---|---|---:|---:|---:|---|']
            for r_ in T['rows']:
                L.append(f"| {r_['pair']} | {r_['types']} | {_g(r_['CED_old'])} | {_g(r_['CED_new'])} | "
                         f"{('×' + format(r_['ratio'], '.7g')) if r_.get('ratio') is not None else 'N/A (0)'} | "
                         f"{'PASS' if r_['ok'] else 'FAIL · ' + r_['reason']} |")
        elif T['kind'] == 'GM':
            L += ['같은 ρ 세계 NCM 표면 대비 (D2) — 바뀌는 CED = 규칙이 정하는 원소 정확히 · 배수 [√(γ\'_iγ\'_j)/√(γ_iγ_j)]^(1/3) · '
                  f"나머지 토큰까지 같다 · k = {T.get('k')}", '',
                  '| 쌍 | 타입 | 옛 CED (J/m³) | 새 CED (J/m³) | 배수 | 규칙 배수 | 바뀌어야 | 판정 |', '|---|---|---:|---:|---:|---:|---|---|']
            for r_ in T['rows']:
                L.append(f"| {r_['pair']} | {r_['types']} | {_g(r_['CED_old'])} | {_g(r_['CED_new'])} | "
                         f"{('×' + format(r_['ratio'], '.7g')) if r_.get('ratio') is not None else 'N/A (0)'} | "
                         f"{('×' + format(r_['expect'], '.7g')) if r_.get('expect') is not None else '—'} | "
                         f"{'예' if r_.get('expect_change') else '아니오'} | {'PASS' if r_['ok'] else 'FAIL · ' + r_['reason']} |")
        elif T['kind'] == 'DT':
            L += [f"k = {T.get('k')} (등록 {REG_DT_K})", '', '| 쌍 | 타입 | CED (ref) | CED (dt/2) | 판정 |', '|---|---|---:|---:|---|']
            for r_ in T['rows']:
                L.append(f"| {r_['pair']} | {r_['types']} | {_g(r_['CED_old'])} | {_g(r_['CED_new'])} | "
                         f"{'PASS (같다)' if r_['ok'] else 'FAIL · ' + r_['reason']} |")
        else:
            L += ['| 쌍 | 타입 | LC CED (J/m³) | LH CED (J/m³) | 차 (LH−LC) | LH/LC | 바뀌어야 | 판정 |', '|---|---|---:|---:|---:|---:|---|---|']
            for r_ in T['rows']:
                L.append(f"| {r_['pair']} | {r_['types']} | {_g(r_['LC'])} | {_g(r_['LH'])} | {_g(r_['diff'])} | "
                         f"{_g(r_['ratio'], '.6g') if r_['ratio'] is not None else 'N/A (LC = 0)'} | {'예 (B)' if r_['expect_change'] else '아니오'} | "
                         f"{'PASS' if r_['ok'] else 'FAIL · ' + r_['reason']} |")
        L += ['', '검사:', '']
        L += [f"- {'✓' if c['ok'] else '✗'} {c['check']}" + (f" — {c['detail']}" if c['detail'] else '') for c in T['checks']]
        m = T.get('meta') or {}
        if m:
            L.append(f"- (메타 · 판정 밖) 주석 줄 — 옛 덱에만 {m.get('comment_only_old', 0)} · 새 덱에만 {m.get('comment_only_new', 0)} "
                     f"({m.get('note', '')})")
    if rep['failures']:
        L += ['', '## 실패 항', ''] + [f'- {f}' for f in rep['failures']]
    return '\n'.join(L) + '\n'


def _selftest():
    """고정물 (fixture) 덱은 생성기로 만든다 — **검산은 생성기를 쓰지 않는다** (이 파일의 파서 · 산술만).
    반례 (Codex 9 차 §3 · §6-2 음성대조): 혼합쌍 하나 · SE–벽만 · 타입 순서 · 0 행렬 변조 · 덤프 간격 변조 + 비대칭 · 영률/ν · 명령 ·
    step 미재계산 · dt 비정수배 · B 몰래 변경/누락/방향 — 전부 **잡아야** 한다."""
    import re
    import subprocess
    import tempfile
    sys.path.insert(0, _HERE)
    import make_mixer_deck as gen                      # 고정물 전용 (검산 경로 밖)
    ok, fail = 0, []

    def chk(name, cond):
        nonlocal ok
        if cond:
            ok += 1
        else:
            fail.append(name)
        print(('  PASS  ' if cond else '  FAIL  ') + name)

    def _ok(fn):
        try:
            return bool(fn())
        except (Exception, SystemExit):
            return False

    pc = gen.plan(100000, cgf=151.4)
    rpm = gen.resolve_rpm(pc['R'])
    P = {F: gen.plan(100000, cgf=151.4, stiffen_se=F) for F in (1.0, 14.0, 28.0)}

    def mk(arm, F, rev, dtf=1.0):
        return gen.deck(P[F], rpm, rev, seed=32452843, arm=arm, hold_bo_pairwise=(F != 1.0), dt_factor=dtf)
    D = {'LC_soft': mk('LC', 1.0, 2), 'LH_soft': mk('LH', 1.0, 2), 'LC_ref': mk('LC', 14.0, 2), 'LH_ref': mk('LH', 14.0, 2),
         'LC_ref2': mk('LC', 28.0, 2), 'LH_ref2': mk('LH', 28.0, 2), 'LC_refdt': mk('LC', 14.0, 2, 0.5),
         'LH_refdt': mk('LH', 14.0, 2, 0.5),
         'E0_soft': mk('E0', 1.0, 0), 'E0_ref': mk('E0', 14.0, 0), 'E0_ref2': mk('E0', 28.0, 0), 'E0_refdt': mk('E0', 14.0, 0, 0.5)}

    def cmp_(kind, a, b, ta=None, tb=None):
        return compare(kind, read_deck(D[a] if ta is None else ta, a), read_deck(D[b] if tb is None else tb, b + ('*' if tb else '')))

    def row(T, pair):
        return next((r_ for r_ in T['rows'] if r_.get('pair') == pair), None)

    def failed_pairs(T):
        return sorted(r_['pair'] for r_ in T['rows'] if not r_.get('ok'))

    def sub1(text, pat, rep, flags=re.M):
        new, n = re.subn(pat, rep, text, count=1, flags=flags)
        assert n == 1, pat
        return new

    def set_ced(text, i, j, val, sym=True):
        """CED 행렬 (1-based 타입) 칸을 val 문자열로 — sym 이면 (j, i) 도.  줄 끝 `&` 는 그대로 둔다."""
        lines = text.split('\n')
        k0 = next(k for k, l in enumerate(lines) if l.startswith('fix ') and 'cohesionEnergyDensity' in l)
        for a_, b_ in dict.fromkeys(((i, j), (j, i)) if sym else ((i, j),)):
            raw = lines[k0 + a_].rstrip()
            amp = raw.endswith('&')
            vals = raw.rstrip('&').split()
            vals[b_ - 1] = val
            lines[k0 + a_] = '    ' + ' '.join(vals) + (' &' if amp else '')
        return '\n'.join(lines)

    def get_ced(text, i, j):
        lines = text.split('\n')
        k0 = next(k for k, l in enumerate(lines) if l.startswith('fix ') and 'cohesionEnergyDensity' in l)
        return float(lines[k0 + i].rstrip().rstrip('&').split()[j - 1])

    # ── 양성 (등록 설계대로 만든 덱) ─────────────────────────────────────────────────────────
    T = cmp_('E', 'LC_soft', 'LC_ref')
    chk(f"① 표 E LC soft → ×14: PASS · 9 비영 항 F₀ 비 = 1 (허용 {TOL['f0_ratio']:.0e}) · 벽–벽 0 · Codex ×14 배수 대조 PASS "
        f"(실패 {failed_pairs(T)})",
        _ok(lambda: T['verdict'] == 'PASS' and len(T['rows']) == 10
            and all(abs(r_['F0_ratio'] - 1.0) <= TOL['f0_ratio'] for r_ in T['rows'] if r_['pair'] != 'WALL–WALL')
            and row(T, 'AM_P–SE')['codex'] == 'PASS' and row(T, 'SE–WALL')['codex'] == 'PASS'
            and row(T, 'AM_P–AM_P')['codex'] == 'PASS'))
    Ts = [cmp_('E', 'LH_soft', 'LH_ref'), cmp_('E', 'LC_soft', 'LC_ref2'), cmp_('E', 'LH_soft', 'LH_ref2'),
          cmp_('E', 'LC_ref', 'LC_ref2')]
    chk('② 표 E LH soft → ×14 · LC/LH soft → ×28 (Codex ×28 대조) · LC ×14 → ×28 (배수 2 — Codex 대조 N/A) 모두 PASS',
        _ok(lambda: all(t_['verdict'] == 'PASS' for t_ in Ts) and row(Ts[1], 'SE–SE')['codex'] == 'PASS'
            and row(Ts[3], 'SE–SE')['codex'] == 'N/A'))
    Ts = [cmp_('E0', 'E0_soft', 'E0_ref'), cmp_('E0', 'E0_ref', 'E0_ref2'), cmp_('E0', 'E0_soft', 'E0_ref2')]
    #  ⚠ 적색 단계에서 이 항이 **빈 표**로 통과했다 (아무것도 안 하는 스텁 · 행 0 개에 all() = True) ⇒ 행 10 개 · 명시 검사 항을 요구한다
    chk('③ 표 E0 soft → ×14 · ×14 → ×28 · soft → ×28: 두 덱 모두 전 점착 0 (정확히 · 행 10 개 · 명시 검사) · 물리 시간 · '
        '덤프/체크포인트 규칙 PASS',
        _ok(lambda: all(t_['verdict'] == 'PASS' and len(t_['rows']) == 10
                        and any('전 점착 0' in c_['check'] and c_['ok'] for c_ in t_['checks']) for t_ in Ts)
            and all(r_['CED_old'] == 0.0 and r_['CED_new'] == 0.0 for t_ in Ts for r_ in t_['rows'])))
    Ts = [cmp_('DT', 'E0_ref', 'E0_refdt'), cmp_('DT', 'LC_ref', 'LC_refdt')]
    chk('④ 표 DT E0 ×14 → dt/2 · LC ×14 → dt/2: E · ν · CED 동일 · dt 정확히 ½ · step · 덤프 ×2 · 계획 t₀ 물리 시각 동일 → PASS',
        _ok(lambda: all(t_['verdict'] == 'PASS' for t_ in Ts) and all(t_['k'] == 2 for t_ in Ts)))
    Ts = [cmp_('B', 'LC_soft', 'LH_soft'), cmp_('B', 'LC_ref', 'LH_ref'), cmp_('B', 'LC_ref2', 'LH_ref2')]
    chk('⑤ 표 B soft · ×14 · ×28: LC↔LH 다섯 쌍 (AM–AM 셋 · AM–벽 둘) 만 증가 · 나머지 전부 정확히 같다 · 벽–벽 0 → PASS',
        _ok(lambda: all(t_['verdict'] == 'PASS' for t_ in Ts)
            and all(sorted(r_['pair'] for r_ in t_['rows'] if r_['expect_change']) ==
                    sorted(['AM_P–AM_P', 'AM_P–AM_S', 'AM_S–AM_S', 'AM_P–WALL', 'AM_S–WALL']) for t_ in Ts)
            and all(row(t_, 'SE–SE')['LH'] == row(t_, 'SE–SE')['LC'] for t_ in Ts)
            and row(Ts[0], 'WALL–WALL')['ratio'] is None))
    # ── 음성대조 (반례 — 전부 잡아야 한다) ─────────────────────────────────────────────────────
    c13 = get_ced(D['LC_soft'], 1, 3)
    bad6 = set_ced(D['LC_ref'], 1, 3, f'{c13 * 14 ** (2.0 / 3.0):g}')        # 옛 동일상 규칙 = SE 배수를 혼합쌍에
    T6 = cmp_('E', 'LC_soft', 'LC_ref', tb=bad6)
    chk(f"⑥ 반례 혼합쌍 하나 (AM_P–SE 를 옛 규칙 ×14^(2/3)) → FAIL · 그 쌍만 짚는다 {failed_pairs(T6)} · F₀ 비 "
        f"{(row(T6, 'AM_P–SE') or {}).get('F0_ratio', float('nan')):.4f} (Codex 1.272)",
        _ok(lambda: T6['verdict'] == 'FAIL' and failed_pairs(T6) == ['AM_P–SE']
            and abs(row(T6, 'AM_P–SE')['F0_ratio'] - 1.272112360) < 1e-4))
    c33 = get_ced(D['LC_ref'], 3, 3)
    bad7 = set_ced(D['LC_ref'], 3, 4, f'{c33 / 6.25 ** (1.0 / 3.0):g}')       # 옛 규칙: SE–벽 = 새 대각 ÷ 1.842
    T7 = cmp_('E', 'LC_soft', 'LC_ref', tb=bad7)
    chk(f"⑦ 반례 SE–벽만 (새 SE 대각 ÷ 1.842 로 다시) → FAIL · SE–WALL 만 {failed_pairs(T7)} · F₀ 비 "
        f"{(row(T7, 'SE–WALL') or {}).get('F0_ratio', float('nan')):.4f} (Codex 1.182)",
        _ok(lambda: T7['verdict'] == 'FAIL' and failed_pairs(T7) == ['SE–WALL']
            and abs(row(T7, 'SE–WALL')['F0_ratio'] - 1.182108914) < 1e-4))
    sw = D['LC_ref'].replace('atom_type 1 ', 'atom_type 9 ').replace('atom_type 2 ', 'atom_type 1 ').replace('atom_type 9 ', 'atom_type 2 ')
    sw_lh = D['LH_ref'].replace('atom_type 1 ', 'atom_type 9 ').replace('atom_type 2 ', 'atom_type 1 ').replace('atom_type 9 ', 'atom_type 2 ')
    e_sw = sub1(D['LC_ref'], r'(youngsModulus peratomtype \S+) (\S+) (\S+)', r'\1 \3 \2')
    T8 = [cmp_('E', 'LC_soft', 'LC_ref', tb=sw), cmp_('B', 'LC_ref', 'LH_ref', tb=sw_lh), cmp_('E', 'LC_soft', 'LC_ref', tb=e_sw)]
    chk('⑧ 반례 타입 순서 — 템플릿 atom_type 1↔2 (표 E · 표 B) · 영률 줄의 AM_S ↔ SE 자리 바꿈 → 셋 다 FAIL (타입 사전 · 영률 대조)',
        _ok(lambda: all(t_['verdict'] == 'FAIL' for t_ in T8)
            and any('타입' in c_['check'] and not c_['ok'] for c_ in T8[0]['checks'])
            and any('영률' in c_['check'] and not c_['ok'] for c_ in T8[2]['checks'])))
    z1 = set_ced(D['E0_ref'], 3, 3, '1000')
    z2 = set_ced(D['LC_ref'], 4, 4, '1')
    T9 = [cmp_('E0', 'E0_soft', 'E0_ref', tb=z1), cmp_('E', 'LC_soft', 'LC_ref', tb=z2), cmp_('E0', 'E0_soft', 'E0_ref', ta=z1)]
    chk('⑨ 반례 0 행렬 변조 — E0 ×14 의 SE–SE = 1000 (새 쪽 · 옛 쪽) · LC ×14 의 벽–벽 = 1 → 셋 다 FAIL',
        _ok(lambda: all(t_['verdict'] == 'FAIL' for t_ in T9) and 'SE–SE' in failed_pairs(T9[0])
            and 'WALL–WALL' in failed_pairs(T9[1])))
    dmp = lambda t, f: sub1(t, r'^(dump dmp all custom )(\d+)', lambda m: m.group(1) + str(f(int(m.group(2)))))
    T10 = [cmp_('E', 'LC_soft', 'LC_ref', tb=dmp(D['LC_ref'], lambda x: x + 1)),
           cmp_('DT', 'E0_ref', 'E0_refdt', tb=dmp(D['E0_refdt'], lambda x: x - 1000)),
           cmp_('E0', 'E0_soft', 'E0_ref', tb=dmp(D['E0_ref'], lambda x: 2 * x))]
    chk('⑩ 반례 덤프 간격 변조 — LC ×14 +1 step (규칙 밖) · E0 dt/2 가 2 배가 아님 · E0 ×14 를 2 배로 → 셋 다 FAIL',
        _ok(lambda: all(t_['verdict'] == 'FAIL' for t_ in T10)
            and all(any('덤프' in c_['check'] and not c_['ok'] for c_ in t_['checks']) for t_ in T10)))
    asym = set_ced(D['LC_ref'], 1, 3, f'{get_ced(D["LC_ref"], 1, 3) * 1.001:g}', sym=False)
    T11 = cmp_('E', 'LC_soft', 'LC_ref', tb=asym)
    chk('⑪ 반례 비대칭 (AM_P–SE 한쪽 칸만 ×1.001) → FAIL (대칭 검사)',
        _ok(lambda: T11['verdict'] == 'FAIL' and any('대칭' in c_['check'] and not c_['ok'] for c_ in T11['checks'])))
    se_se = set_ced(D['LH_ref'], 3, 3, f'{get_ced(D["LH_ref"], 3, 3) + 0.1:.1f}')
    miss = set_ced(D['LH_ref'], 1, 1, f'{get_ced(D["LC_ref"], 1, 1):g}')
    down = set_ced(D['LH_ref'], 2, 4, f'{get_ced(D["LC_ref"], 2, 4) / 2:g}')
    grav = sub1(D['LH_ref'], r'(gravity )9\.81', r'\g<1>9.80')
    T12 = [cmp_('B', 'LC_ref', 'LH_ref', tb=x) for x in (se_se, miss, down, grav)]
    chk(f"⑫ 반례 표 B — LH SE–SE +0.1 (몰래 변경) · AM_P–AM_P = LC (개입 누락) · AM_S–벽 ÷2 (방향 반대) · 중력 9.80 (명령) → 넷 다 FAIL "
        f"{[failed_pairs(t_) for t_ in T12]}",
        _ok(lambda: all(t_['verdict'] == 'FAIL' for t_ in T12) and failed_pairs(T12[0]) == ['SE–SE']
            and failed_pairs(T12[1]) == ['AM_P–AM_P'] and failed_pairs(T12[2]) == ['AM_S–WALL']
            and any('명령' in c_['check'] and not c_['ok'] for c_ in T12[3]['checks'])))
    am_e = sub1(D['LC_ref'], r'(youngsModulus peratomtype )1\.037e\+09', r'\g<1>1.1e+09')
    nu = sub1(D['LC_ref'], r'(poissonsRatio peratomtype \S+ \S+ )0\.30', r'\g<1>0.31')
    nb = sub1(D['LC_ref'], r'^(neighbor\s+)(\S+)', lambda m: m.group(1) + f'{float(m.group(2)) * 1.5:.6g}')
    soft_runs = re.findall(r'^run (\d+)$', D['LC_soft'], re.M)
    it = iter(soft_runs)
    norescale = re.sub(r'^run (\d+)$', lambda m: 'run ' + next(it), D['LC_ref'], flags=re.M)
    T13 = [cmp_('E', 'LC_soft', 'LC_ref', tb=x) for x in (am_e, nu, nb, norescale)]
    chk('⑬ 반례 표 E — AM_P 영률 변경 · SE ν 변경 · neighbor 변경 (허용 밖 명령) · step 을 새 dt 로 다시 안 셈 (soft step 그대로) → 넷 다 FAIL',
        _ok(lambda: all(t_['verdict'] == 'FAIL' for t_ in T13)
            and any('물리 시간' in c_['check'] and not c_['ok'] for c_ in T13[3]['checks'])))
    r1 = sub1(D['E0_refdt'], r'^run (\d+)$\n(?=unfix ins)', lambda m: f'run {int(m.group(1)) + 1}\n')
    dtx = sub1(D['E0_refdt'], r'^timestep\s+1\.566e-07$', 'timestep        1.567e-07')
    T14 = [cmp_('DT', 'E0_ref', 'E0_refdt', tb=x) for x in (r1, dtx)] + [cmp_('DT', 'LC_soft', 'LC_ref')]
    chk('⑭ 반례 표 DT — 정착 step +1 (정수배 아님) · dt 1.567e-07 (정확히 ½ 아님) · soft → ×14 를 DT 로 (k 비정수 · 영률 다름) → 셋 다 FAIL',
        _ok(lambda: all(t_['verdict'] == 'FAIL' for t_ in T14)))
    T15 = cmp_('E', 'LC_ref', 'LC_ref')
    chk('⑮ 같은 덱 둘을 표 E 로 → FAIL (SE 영률이 같다 = E 비교가 아니다 — 빈 비교를 PASS 로 내지 않는다)',
        _ok(lambda: T15['verdict'] == 'FAIL'))
    #  ⑱ 반례 (C 설계 중 발견 — 2026-09-30): SE 를 경화하고 **dt 를 다시 안 셌다** — soft 의 dt · step · 덤프 · 체크포인트를 그대로 두면
    #     물리 시간 · 덤프/체크포인트 규칙 · 쌍별 CED 가 **전부 맞아** 보인다.  그런데 dt 0.7055 µs 는 경화한 SE 의 Rayleigh 한계
    #     0.3132 µs 의 2.25 배 = 적분 불안정.  ⇒ dt 를 이 덱의 E · ν · 반지름 · 밀도로 다시 낸 Rayleigh 규칙과 대조해야 한다.
    def stale_dt(ref, soft):
        out = sub1(ref, r'^timestep\s+\S+$', re.search(r'^timestep\s+\S+$', soft, re.M).group(0))
        it2 = iter(re.findall(r'^run (\d+)$', soft, re.M))
        out = re.sub(r'^run (\d+)$', lambda m: 'run ' + next(it2), out, flags=re.M)
        de = re.search(r'^dump dmp all custom (\d+)', soft, re.M).group(1)
        out = sub1(out, r'^(dump dmp all custom )\d+', lambda m: m.group(1) + de)
        rs = re.search(r'^restart (\d+) ', soft, re.M).group(1)
        return sub1(out, r'^(restart )\d+', lambda m: m.group(1) + rs)
    T18 = [cmp_('E', 'LC_soft', 'LC_ref', tb=stale_dt(D['LC_ref'], D['LC_soft'])),
           cmp_('E0', 'E0_soft', 'E0_ref', tb=stale_dt(D['E0_ref'], D['E0_soft']))]
    bad18 = [[c_['check'] for c_ in t_['checks'] if not c_['ok']] for t_ in T18]
    chk(f'⑱ ★ 반례 — SE ×14 인데 dt · step · 덤프 · 체크포인트를 soft 그대로 (LC · E0): 물리 시간 · 규칙 · 쌍별 CED 는 다 맞아도 '
        f'**Rayleigh dt 대조 하나로** FAIL (적분 불안정 덱) {[len(b_) for b_ in bad18]}',
        _ok(lambda: all(t_['verdict'] == 'FAIL' for t_ in T18) and all(b_ and all('Rayleigh' in x for x in b_) for b_ in bad18)
            and all(r_['ok'] for t_ in T18 for r_ in t_['rows'])))
    T19 = cmp_('B', 'LC_refdt', 'LH_refdt')
    chk('⑲ 표 B 는 dt/2 짝 (LC ×14 dt/2 ↔ LH ×14 dt/2) 도 PASS — dt = Rayleigh 규칙의 정확히 1/k (k 정수) 는 허용 · k 를 적는다',
        _ok(lambda: T19['verdict'] == 'PASS' and T19.get('k') == 2))
    chk('⑳ Rayleigh 사본 = 생성기 plan() 의 dt (F 1 · 14 · 28 × CGF 151.4 · 200 — 덱에 찍힌 반지름 · 밀도 · E · ν 에서 다시 낸 값 · '
        '허용 rayleigh_rel) — 식이 갈리면 여기서 드러난다',
        _ok(lambda: all(abs(rayleigh_dt(read_deck(gen.deck(gen.plan(100000, cgf=c_, stiffen_se=F_), rpm, 0, arm='E0',
                                                           hold_bo_pairwise=True), 'x'))[0]
                            / gen.plan(100000, cgf=c_, stiffen_se=F_)['dt'] - 1.0) <= TOL['rayleigh_rel']
                        for F_ in (1.0, 14.0, 28.0) for c_ in (151.4, 200.0))))
    rd = read_deck(D['LC_ref'], 'x')
    chk('⑯ 되읽기 = 덱 텍스트: sha256 · 타입 사전 (1 AM_P · 2 AM_S · 3 SE · 4 WALL — 밀도 · 반지름 · 템플릿 시드 · 메시 타입) · '
        'E · ν · dt · run · 덤프 · 체크포인트',
        _ok(lambda: rd['sha256'] == hashlib.sha256(D['LC_ref'].encode('utf-8')).hexdigest()
            and rd['names'] == REG_TYPES and rd['E'] == [1.037e9, 1.037e9, 1.4e8, 1.48e9] and rd['nu'] == [0.25, 0.25, 0.30, 0.30]
            and rd['dt_txt'] == '3.132e-07' and rd['runs'] == [int(x) for x in re.findall(r'^run (\d+)$', D['LC_ref'], re.M)]
            and rd['dump_every'] == int(re.search(r'^dump dmp all custom (\d+)', D['LC_ref'], re.M).group(1))
            and not rd['problems'] and not rd['type_problems']))
    with tempfile.TemporaryDirectory() as td:
        paths = {}
        for k in ('LC_soft', 'LC_ref', 'LH_ref'):
            os.makedirs(os.path.join(td, k))
            paths[k] = os.path.join(td, k, 'in.mixer')
            open(paths[k], 'w', encoding='utf-8').write(D[k] if k != 'LH_ref' else se_se)
            open(os.path.join(td, k, 'gen_cmd.txt'), 'w', encoding='utf-8').write(f'python3 scripts/make_mixer_deck.py … ({k})\n')
        js, md = os.path.join(td, 'r.json'), os.path.join(td, 'r.md')
        me = os.path.abspath(__file__)
        a = subprocess.run([sys.executable, me, '--table', 'E', paths['LC_soft'], paths['LC_ref'], '--json', js, '--md', md],
                           capture_output=True, text=True)
        rep = json.load(open(js, encoding='utf-8')) if os.path.exists(js) else {}
        mdt = open(md, encoding='utf-8').read() if os.path.exists(md) else ''
        b = subprocess.run([sys.executable, me, '--table', 'E', paths['LC_soft'], paths['LC_ref'],
                            '--table', 'B', paths['LC_ref'], paths['LH_ref'], '--json', js], capture_output=True, text=True)
        rep_b = json.load(open(js, encoding='utf-8')) if os.path.exists(js) else {}
        chk('⑰ CLI: PASS 면 rc 0 · JSON (도구 sha256 · 버전 · 허용오차 · 덱 sha256 · 생성 명령 (gen_cmd.txt) · 타입 사전 · 표) · '
            'markdown 표 · FAIL 이 섞이면 rc 1 이고 실패 항 목록이 남는다',
            _ok(lambda: a.returncode == 0 and rep['verdict'] == 'PASS' and rep['tool_version'] == TOOL_VERSION
                and rep['tool_sha256'] == hashlib.sha256(open(me, 'rb').read()).hexdigest()
                and set(rep['tolerances']) >= {'f0_ratio', 'ced_mult_rel', 'dt_print_rel', 'exact_rel'}
                and rep['decks'][paths['LC_ref']]['sha256'] == hashlib.sha256(D['LC_ref'].encode('utf-8')).hexdigest()
                and rep['decks'][paths['LC_ref']]['gen_cmd'].endswith('(LC_ref)')
                and rep['decks'][paths['LC_ref']]['types'] == {str(k_): v_ for k_, v_ in REG_TYPES.items()}
                and '| AM_P–SE |' in mdt and 'F₀' in mdt
                and b.returncode == 1 and rep_b['verdict'] == 'FAIL'
                and any(f_.startswith('B ') and 'SE–SE' in f_ for f_ in rep_b['failures'])))
    #  ㉑ (2026-09-30 D 게이트에서 발견) — markdown 이 docs/ 에 커밋되면 scripts/check_doc_refs.py 가 **백틱 안 7~40 자 hex** 를
    #     커밋 SHA 로 읽는다 (표 머리에 'sha' 가 있으면 행 전부).  sha256 앞자리를 백틱으로 찍으면 '없는 커밋' 으로 게이트가 막힌다.
    import importlib.util as _iu
    _spec = _iu.spec_from_file_location('_cdr', os.path.join(_HERE, 'check_doc_refs.py'))
    _cdr = _iu.module_from_spec(_spec)
    _spec.loader.exec_module(_cdr)
    _md = to_markdown(make_report({'x/in.mixer': read_deck(D['LC_soft'], 'LC_soft'), 'y/in.mixer': read_deck(D['LC_ref'], 'LC_ref')},
                                  [cmp_('E', 'LC_soft', 'LC_ref'), cmp_('B', 'LC_ref', 'LH_ref')]))
    _hits = [h for ln in _md.split('\n') for h in _cdr._RE_SHA.findall(ln) if not h.isdigit()]
    chk(f'㉑ markdown 에 백틱 안 순수 hex (check_doc_refs 의 커밋 SHA 패턴) 가 없다 — sha256 앞자리는 백틱 없이 · 발견 {len(_hits)}',
        not _hits and '| AM_P–SE |' in _md)

    # ── 표 U (2026-10-05 · 개발 탐색 dev-u · 강성 축 사전등록 §12) — 같은 강성 · 9 비영 CED 가 한 공통 배율 (균일 γ 배율) ─────────────────────
    #  ★ 반례를 먼저 옮겼다 — 옛 되읽기에는 표 U 가 없다 ('표 종류 ∈ KINDS' 검사 FAIL · CLI 거부) ⇒ U① ~ U③ 전부 FAIL.
    P[20.0] = gen.plan(100000, cgf=151.4, stiffen_se=20.0)
    for k_, (a_, F_) in {'LC_ref20': ('LC', 20.0), 'LH_ref20': ('LH', 20.0), 'LU212_ref20': ('LU212', 20.0), 'LU637_ref20': ('LU637', 20.0),
                         'LU212_soft': ('LU212', 1.0)}.items():
        D[k_] = mk(a_, F_, 2)
    TU = [cmp_('U', 'LC_ref20', 'LU212_ref20'), cmp_('U', 'LC_ref20', 'LU637_ref20'), cmp_('U', 'LU212_ref20', 'LU637_ref20'),
          cmp_('U', 'LC_soft', 'LU212_soft')]
    chk('U① ★ 표 U (×20 · LC → LU212 · LU637 · LU212 → LU637 · soft LC → LU212) → PASS · 행 10 · 9 비영 항 전부 한 배율 (퍼짐 ≤ '
        f"{TOL.get('u_spread_rel', float('nan')):.0e}) · 공통 배율 ×10 · ×14.422496 · ×3^(1/3) · 벽–벽 0 · 같은 E · ν · dt",
        _ok(lambda: all(t_['verdict'] == 'PASS' and len(t_['rows']) == 10 for t_ in TU)
            and all(abs(t_['u_ratio'] / w_ - 1.0) <= TOL['u_spread_rel'] for t_, w_ in zip(TU, (10.0, 3000.0 ** (1.0 / 3.0), 3.0 ** (1.0 / 3.0), 10.0)))
            and all(t_['u_spread'] <= TOL['u_spread_rel'] for t_ in TU) and row(TU[0], 'WALL–WALL')['ok']))
    se_only = set_ced(D['LC_ref20'], 3, 3, f'{get_ced(D["LC_ref20"], 3, 3) * 10:g}')                       # S 형 — SE–SE 한 원소만 ×10
    e_chg = sub1(D['LU212_ref20'], r'(youngsModulus peratomtype \S+ \S+ )2e\+08', r'\g<1>2.2e+08')           # 균일 ×10 + SE 영률
    two = set_ced(D['LU212_ref20'], 1, 2, f'{get_ced(D["LC_ref20"], 1, 2) * 11:g}')                           # AM_P–AM_S 만 ×11
    wall = set_ced(D['LU212_ref20'], 4, 4, '1')                                                             # 벽–벽 0 → 1
    TU2 = {'se_only': cmp_('U', 'LC_ref20', 'LC_ref20', tb=se_only), 'E': cmp_('U', 'LC_ref20', 'LU212_ref20', tb=e_chg),
           'two': cmp_('U', 'LC_ref20', 'LU212_ref20', tb=two), 'wall': cmp_('U', 'LC_ref20', 'LU212_ref20', tb=wall),
           'down': cmp_('U', 'LU212_ref20', 'LC_ref20'), 'same': cmp_('U', 'LC_ref20', 'LC_ref20'), 'lh': cmp_('U', 'LH_ref20', 'LU212_ref20'),
           'as_B': cmp_('B', 'LC_ref20', 'LU212_ref20')}
    _bad = lambda t_, w_: any(w_ in c_['check'] and not c_['ok'] for c_ in t_['checks'])               # noqa: E731
    chk(f"U② ★ 반례 표 U → 전부 FAIL · 짚는 곳: SE–SE 한 원소만 ×10 (그 쌍만 {failed_pairs(TU2['se_only'])}) · 균일 ×10 + SE 영률 (영률) · "
        f"AM_P–AM_S 만 ×11 ({failed_pairs(TU2['two'])}) · 벽–벽 1 · 줄어든 덱 (증가) · 같은 덱 (빈 비교) · LH → LU212 (배율 하나 아님) · "
        "U 덱을 표 B 로 (SE 낀 쌍이 바뀌면 안 된다)",
        _ok(lambda: all(t_['verdict'] == 'FAIL' for t_ in TU2.values())
            and failed_pairs(TU2['se_only']) == ['SE–SE'] and _bad(TU2['se_only'], '배율 하나')
            and _bad(TU2['E'], '영률') and failed_pairs(TU2['two']) == ['AM_P–AM_S'] and 'WALL–WALL' in failed_pairs(TU2['wall'])
            and _bad(TU2['down'], '> 1') and _bad(TU2['same'], '> 1') and _bad(TU2['lh'], '배율 하나')
            and sorted(failed_pairs(TU2['as_B'])) == ['AM_P–SE', 'AM_S–SE', 'SE–SE', 'SE–WALL']))
    with tempfile.TemporaryDirectory() as td:
        paths = {}
        for k in ('LC_ref20', 'LU212_ref20'):
            os.makedirs(os.path.join(td, k))
            paths[k] = os.path.join(td, k, 'in.mixer')
            open(paths[k], 'w', encoding='utf-8').write(D[k])
        js, md = os.path.join(td, 'u.json'), os.path.join(td, 'u.md')
        cu = subprocess.run([sys.executable, os.path.abspath(__file__), '--table', 'U', paths['LC_ref20'], paths['LU212_ref20'],
                             '--json', js, '--md', md], capture_output=True, text=True)
        repu = json.load(open(js, encoding='utf-8')) if os.path.exists(js) else {}
        mdu = open(md, encoding='utf-8').read() if os.path.exists(md) else ''
    chk('U③ CLI --table U: rc 0 · JSON 표 (kind U · 공통 배율 · 퍼짐 · 등록 규칙 사본) · markdown 의 표 U (쌍마다 배율 · 판정)',
        _ok(lambda: cu.returncode == 0 and repu['verdict'] == 'PASS' and repu['tables'][0]['kind'] == 'U'
            and abs(repu['tables'][0]['u_ratio'] / 10.0 - 1.0) <= TOL['u_spread_rel'] and 'U_rule' in repu['registered']
            and '## 표 U' in mdu and '| SE–SE |' in mdu and '공통 배율' in mdu))

    # ── MX (2026-10-21 · 원장 MXD2-01 · 02 · D2 사전 공격 리뷰) — 밀도 세대 · D2 결합 규칙 되읽기 · 표 GM (같은 ρ 세계 코팅 ↔ 비코팅) ──────────────
    #  ★ 반례를 먼저 옮겼다 — 옛 되읽기: 등록 밀도가 gen1 (4800 · 2000) 뿐이라 lab 덱 (4850 · 1640) 을 타입 사전에서 거부 · D2 규칙 (쌍마다 기하평균 ·
    #    절대 수준 Bo · Q2 벽 · 머리 표 · 기록) 을 덱 텍스트에서 볼 경로 없음 · 표 GM 없음 · deck_meta 결합 없음 ⇒ MX① – ⑦ FAIL.
    LAB = 'lab20261014'
    PL = {(g_, F_): gen.plan(100000, cgf=151.4, stiffen_se=F_, dens_gen=g_) for g_ in (LAB, 'gen1') for F_ in (1.0, 20.0)}

    def mkgm(gp, gs, rho, bo, F, g_=LAB, wall=None):
        """D2 덱 + deck_meta (생성기 라이브러리 = CLI 와 같은 호출 · 팔 이름 GMRB) — 고정물 전용."""
        p_ = PL[(g_, F)]
        rpm_ = gen.resolve_rpm(p_['R'])
        if wall is None:
            a_ = gen.gm_arm({'AM_P': gp, 'AM_S': gs, 'SE': 1.0}, gamma_wall=gen.gm_wall_from_ncm(rho), bo_se=bo, rho_uncoated_ncm=rho)
        else:
            a_ = gen.gm_arm({'AM_P': gp, 'AM_S': gs, 'SE': 1.0}, gamma_wall=wall, bo_se=bo)
        nm_ = gen.register_arm('GMRB', a_)
        try:
            t_ = gen.deck(p_, rpm_, 2, seed=32452843, arm=nm_, hold_bo_pairwise=(F != 1.0))
            m_ = gen.deck_meta(p_, rpm_, 2, 32452843, nm_, t_, argv=['(selftest)'], hold_bo_pairwise=(F != 1.0))
        finally:
            gen.ARMS.pop(nm_, None)
        return t_, m_

    def rdm(tm, label, meta=True):
        return read_deck(tm[0], label, meta=tm[1] if meta else None)
    GX = {}

    def _gx(key, *a, **kw):
        if key not in GX:
            GX[key] = mkgm(*a, **kw)
        return GX[key]

    def _mx1():
        lc = {F_: gen.deck(PL[(LAB, F_)], gen.resolve_rpm(PL[(LAB, F_)]['R']), 2, seed=32452843, arm='LC', hold_bo_pairwise=(F_ != 1.0))
              for F_ in (1.0, 20.0)}
        t1 = compare('E', read_deck(lc[1.0], 'LC_lab_soft'), read_deck(lc[20.0], 'LC_lab_ref'))
        t2 = compare('E', rdm(_gx('uu_soft', 0.3, 0.3, 0.3, 0.5, 1.0), 'GMuu_lab_soft'), rdm(_gx('uu_ref', 0.3, 0.3, 0.3, 0.5, 20.0), 'GMuu_lab_ref'))
        Dl = read_deck(lc[1.0], 'x')
        ok_ = (t1['verdict'] == 'PASS' and t2['verdict'] == 'PASS' and Dl['dens_gen'] == LAB and not Dl['type_problems']
               and read_deck(D['LC_soft'], 'y')['dens_gen'] == 'gen1'
               and any('D2 결합 규칙' in c_['check'] and c_['ok'] for c_ in t2['checks']))
        if not ok_:
            print(f"        {t1['failures'][:2]} · {t2['failures'][:2]}")
        return ok_
    chk('MX① ★ lab 세대 덱 (MXD2-01) — 옛 팔 LC lab soft → ×20 · D2 덱 (ρ 0.3 세계 · Bo 0.5) soft → ×20 의 표 E = PASS · 세대 = 템플릿 밀도로 판정 '
        '(lab 4850 · 1640 / gen1 4800 · 2000) · D2 덱은 표마다 D2 규칙 검산이 붙는다', _ok(_mx1))

    def _mx2():
        uu = rdm(_gx('uu_soft', 0.3, 0.3, 0.3, 0.5, 1.0), 'GMuu')
        r_ = d2_check(uu)
        rows = {x['pair']: x for x in r_['rows']}
        return (r_['is_d2'] and not r_['problems'] and len(rows) == 10 and all(x['ok'] for x in r_['rows'])
                and abs(r_['bo_read'] / 0.5 - 1.0) <= TOL['gm_bo_rel'] and r_['decl']['gamma'] == {'AM_P': 0.3, 'AM_S': 0.3, 'SE': 1.0}
                and abs(r_['decl']['rho'] - 0.3) < 1e-15 and r_['decl']['wall_rule'] == D2_WALL_NCM
                and abs(rows['AM_P–SE']['F0_ratio'] / (math.sqrt(0.3) * rows['AM_P–SE']['R_star'] / rows['SE–SE']['R_star']) - 1.0) <= TOL['gm_law_rel']
                and not d2_check(read_deck(D['LC_soft'], 'LC'))['is_d2'])
    chk('MX② ★ D2 덱 되읽기 (덱 텍스트만) — 쌍 10 행 (벽 포함) 의 F₀_ij/F₀_SS = √(γ_iγ_j)·R*_ij/R*_SS (선언 γ · 허용 gm_law_rel) · Bo_SE = F₀_SS / '
        'SE 무게 (그 덱의 r · ρ · 중력) = 선언 0.5 · 선언 = γ · ρ · 벽 규칙 · 옛 팔 덱은 D2 아님', _ok(_mx2))

    def _mx3():
        t_, m_ = _gx('uu_soft', 0.3, 0.3, 0.3, 0.5, 1.0)
        th, mh = _gx('cc_soft_bo600', 1.0, 1.0, 1.0, 600.0, 1.0)                                   # SE–SE 0.70 % (천장 가까이)
        tmp = {}                                                                                    # 이름 → (덱, 메타 | None, 사유 낱말)
        tmp['Bo 선언'] = (re.sub(r'SE–SE Bo_code 0\.5 \(', 'SE–SE Bo_code 0.4 (', t_, count=1), None, 'Bo')    # 선언 ≠ 값 (M04 꼴)
        tmp['머리 표 비'] = (re.sub(r'^(#\s+AM_P–SE(?:\s+\S+){4}\s+)(\S+)', lambda mm: mm.group(1) + '9.99999', t_, count=1, flags=re.M),
                          None, '머리 표')                                                          # M15 꼴
        c13 = get_ced(t_, 1, 3)
        tmp['법칙 (산술평균)'] = (set_ced(t_, 1, 3, f'{c13 * ((0.5 * (0.3 + 1.0)) / math.sqrt(0.3)) ** (1.0 / 3.0):g}'), None, 'AM_P–SE')
        tmp['Q2 (선언 γ 0.5 ≠ ρ)'] = (re.sub(r'γ/γ_SE: AM_P 0\.3 ', 'γ/γ_SE: AM_P 0.5 ', t_, count=1), None, 'Q2')
        tmp['세대 표기'] = (re.sub(r'dens_gen = lab20261014', 'dens_gen = gen1', t_, count=1), None, '세대')
        tmp['천장'] = (set_ced(th, 3, 3, f'{get_ced(th, 3, 3) * 1.3:g}'), 'h', '천장')
        tmp['메타 Bo (M16 꼴)'] = (t_, dict(m_, adhesion_rule=dict(m_['adhesion_rule'], bo_se=0.21244)), '기록')
        tmp['메타 세대'] = (t_, dict(m_, dens_gen='gen1'), '기록')
        tmp['메타 sha'] = (t_, dict(m_, deck_sha256='0' * 64), '기록')
        tmp['메타 γ_W'] = (t_, dict(m_, adhesion_rule=dict(m_['adhesion_rule'], gamma_wall=0.0256)), '기록')
        tmp['메타 schema'] = (t_, dict(m_, schema='mixer_deck_meta/1'), '기록')
        got = {}
        for k_, (tt, mm, w_) in tmp.items():
            base_m = mh if mm == 'h' else m_
            mm2 = (dict(base_m, deck_sha256=hashlib.sha256(tt.encode('utf-8')).hexdigest()) if mm in (None, 'h') else mm)
            got[k_] = (d2_check(read_deck(tt, k_, meta=mm2))['problems'], w_)
        clean = d2_check(read_deck(t_, 'ok', meta=m_))['problems'] + d2_check(read_deck(th, 'ok2', meta=mh))['problems']
        miss = [k_ for k_, (v_, w_) in got.items() if not any(w_ in p_ for p_ in v_)]
        if miss or clean:
            print(f'        못 잡음 · 사유 어긋남 {miss} · 정상 덱 문제 {clean[:2]}')
        return not miss and not clean
    chk('MX③ ★ 반례 → D2 검산이 잡는다 (MXD2-02) — 머리 Bo 선언 ≠ 덱 값 (M04 꼴) · 머리 표 F0/F0_SS 칸 변조 (M15 꼴) · AM_P–SE 를 산술평균 값으로 · '
        '선언 γ 를 Q2 밖으로 · 세대 표기 ≠ 템플릿 밀도 · SE–SE 천장 넘김 · 메타 Bo 상수 (M16 꼴) · 메타 세대 · 메타 sha · 메타 γ_W · 메타 schema /1 — 정상 덱은 문제 0',
        _ok(_mx3))

    def _mx4():
        uu, cc, cu = (rdm(_gx(k_, gp, gs, 0.3, 0.5, 20.0), k_) for k_, gp, gs in (('uu_ref', 0.3, 0.3), ('cc_ref', 1.0, 1.0), ('cu_ref', 1.0, 0.3)))
        T1, T2 = compare('GM', uu, cc), compare('GM', uu, cu)
        ch1 = sorted(r_['pair'] for r_ in T1['rows'] if r_.get('expect_change'))
        ch2 = sorted(r_['pair'] for r_ in T2['rows'] if r_.get('expect_change'))
        m3, m6 = (1.0 / 0.3) ** (1.0 / 3.0), (1.0 / 0.3) ** (1.0 / 6.0)
        r1 = {r_['pair']: r_ for r_ in T1['rows']}
        ok_ = (T1['verdict'] == 'PASS' and T2['verdict'] == 'PASS'
               and ch1 == sorted(['AM_P–AM_P', 'AM_P–AM_S', 'AM_S–AM_S', 'AM_P–SE', 'AM_S–SE', 'AM_P–WALL', 'AM_S–WALL'])
               and ch2 == sorted(['AM_P–AM_P', 'AM_P–AM_S', 'AM_P–SE', 'AM_P–WALL'])
               and abs(r1['AM_P–AM_P']['expect'] / m3 - 1.0) < 1e-12 and abs(r1['AM_S–SE']['expect'] / m6 - 1.0) < 1e-12
               and r1['SE–SE']['expect'] == 1.0 and r1['SE–WALL']['expect'] == 1.0)
        if not ok_:
            print(f"        {T1['failures'][:3]} · {T2['failures'][:3]} · {ch1} · {ch2}")
        return ok_
    chk('MX④ ★ 표 GM (같은 ρ 세계 비코팅 ↔ 코팅 · MXD2-01) — ×20 lab ρ 0.3 · Bo 0.5: uu → cc 바뀌는 CED = 규칙이 정하는 일곱 (AM–AM 셋 × (1/ρ)^(1/3) · '
        'AM–SE 둘 · AM–벽 둘 × (1/ρ)^(1/6)) · SE–SE · SE–벽 · 벽–벽 그대로 · uu → cu (AM_P 만 코팅) = 넷 → PASS', _ok(_mx4))

    def _mx5():
        uu = _gx('uu_ref', 0.3, 0.3, 0.3, 0.5, 20.0)
        cc = _gx('cc_ref', 1.0, 1.0, 0.3, 0.5, 20.0)
        cc5 = _gx('cc_ref_rho05', 1.0, 1.0, 0.5, 0.5, 20.0)
        ccb = _gx('cc_ref_bo04', 1.0, 1.0, 0.3, 0.4, 20.0)
        ccs = _gx('cc_soft', 1.0, 1.0, 0.3, 0.5, 1.0)
        c11 = get_ced(cc[0], 1, 1)
        extra = (set_ced(cc[0], 1, 1, f'{c11 * 1.01:g}'), None)
        cases = {'다른 ρ 세계': (uu, cc5, '같은 ρ 세계'), '다른 Bo': (uu, ccb, '같은 ρ 세계'), '다른 강성': (uu, ccs, '명령'),
                 '같은 덱': (uu, uu, '표면'), '규칙 밖 원소': (uu, extra, 'AM_P–AM_P'),
                 '옛 팔 덱': ((D['LC_ref'], None), (D['LH_ref'], None), 'D2 결합 규칙 덱')}
        got = {}
        for k_, (a_, b_, w_) in cases.items():
            mb = b_[1] if b_[1] is not None else None
            T = compare('GM', read_deck(a_[0], 'A', meta=a_[1]), read_deck(b_[0], 'B', meta=mb))
            got[k_] = T['verdict'] == 'FAIL' and (any(w_ in f_ for f_ in T['failures']))
        miss = [k_ for k_, v_ in got.items() if not v_]
        if miss:
            print(f'        못 잡음 · 사유 어긋남 {miss}')
        return not miss
    chk('MX⑤ ★ 반례 표 GM → FAIL (사유를 짚는다) — 다른 ρ 세계 (γ_W 다름) · 다른 Bo · 다른 강성 · 같은 덱 (표면 안 바뀜) · 규칙이 안 정하는 원소 '
        '(AM_P–AM_P ×1.01) · 옛 팔 LC → LH (D2 덱 아님)', _ok(_mx5))

    def _mx6():
        uu, cc = _gx('uu_ref', 0.3, 0.3, 0.3, 0.5, 20.0), _gx('cc_ref', 1.0, 1.0, 0.3, 0.5, 20.0)
        with tempfile.TemporaryDirectory() as td:
            paths = {}
            for k_, (tt, mm) in (('uu', uu), ('cc', cc)):
                os.makedirs(os.path.join(td, k_))
                paths[k_] = os.path.join(td, k_, 'in.mixer')
                open(paths[k_], 'w', encoding='utf-8').write(tt)
                json.dump(mm, open(os.path.join(td, k_, 'deck_meta.json'), 'w', encoding='utf-8'), ensure_ascii=False)
            js = os.path.join(td, 'g.json')
            me = os.path.abspath(__file__)
            g1 = subprocess.run([sys.executable, me, '--table', 'GM', paths['uu'], paths['cc'], '--json', js], capture_output=True, text=True)
            rep = json.load(open(js, encoding='utf-8')) if os.path.exists(js) else {}
            json.dump(dict(cc[1], adhesion_rule=dict(cc[1]['adhesion_rule'], bo_se=0.21244)),
                      open(os.path.join(td, 'cc', 'deck_meta.json'), 'w', encoding='utf-8'), ensure_ascii=False)
            g2 = subprocess.run([sys.executable, me, '--table', 'GM', paths['uu'], paths['cc']], capture_output=True, text=True)
        return (g1.returncode == 0 and rep.get('verdict') == 'PASS' and rep['tables'][0]['kind'] == 'GM'
                and rep['decks'][paths['cc']].get('dens_gen') == LAB and rep['decks'][paths['cc']].get('d2', {}).get('wall_rule') == D2_WALL_NCM
                and g2.returncode == 1 and 'D2 기록' in g2.stdout)
    chk('MX⑥ CLI --table GM — 덱 옆 deck_meta.json 을 읽어 결합까지 본다: 정상 rc 0 (JSON 표 GM · 덱 세대 · D2 선언) · 메타 Bo 를 상수 0.21244 로 바꾸면 '
        'rc 1 ("D2 기록")', _ok(_mx6))

    def _mx7():
        want = {g_: {'AM': gen.DENS_GENERATIONS[g_]['AM'] * 1000.0, 'SE': gen.DENS_GENERATIONS[g_]['SE'] * 1000.0} for g_ in gen.DENS_GENERATIONS}
        return REG_DENSITY_GEN == want and GM_WALL == gen.GM_WALL_HARE2026 and REG_G == 9.81
    chk('MX⑦ 등록 사본 = 생성기 — 세대별 밀도 (AM · SE × 1000 kg/m³) · 벽 γ_W/γ = 0.0256 · 중력 9.81 (사본이 어긋나면 여기서 드러난다)', _ok(_mx7))
    print(f'\nmixer_deck_readback selftest: {ok}/{ok + len(fail)} PASS' + (f'   FAILED: {fail}' if fail else ''))
    return 1 if fail else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description='믹서 실행 덱 되읽기 — 덱 텍스트에서 E · ν · CED · dt · step 을 읽어 표 E · E0 · DT · B · U · GM 을 '
                                             '독립 검산 (D2 덱은 결합 규칙 · 덱 옆 deck_meta.json 결합까지)')
    ap.add_argument('--table', nargs=3, action='append', metavar=('KIND', 'OLD', 'NEW'),
                    help='KIND ∈ E · E0 · DT · B · U · GM — OLD · NEW = in.mixer 경로 (B 는 LC 다음 LH · U 는 LC 다음 LU · '
                         'GM 은 같은 ρ 세계 D2 덱 둘 (예: 비코팅 다음 코팅)).  여러 번 줄 수 있다')
    ap.add_argument('--json', help='JSON 보고 (도구 sha256 · 허용오차 · 등록 상수 · 덱 sha256 · 생성 명령 · 표 · 실패 항)')
    ap.add_argument('--md', help='사람이 읽는 표 (markdown)')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        raise SystemExit(_selftest())
    if not a.table:
        ap.error('--table KIND OLD NEW 가 하나도 없다')
    decks, tables = {}, []
    for kind, old, new in a.table:
        if kind not in KINDS:
            ap.error(f'표 종류 {kind!r} — {KINDS} 중 하나')
        for pth in (old, new):
            if pth not in decks:
                try:
                    decks[pth] = load(pth)
                except OSError as e:
                    ap.error(f'덱을 못 읽는다: {pth} ({e})')
        tables.append(compare(kind, decks[old], decks[new]))
    rep = make_report(decks, tables, sys.argv[1:] if argv is None else argv)
    for T in tables:
        print(f"── 표 {T['kind']:2s} {T['old']} → {T['new']}  {T['verdict']}")
        for f in T['failures'][:6]:
            print(f'     ⛔ {f}')
    if a.json:
        with open(a.json, 'w', encoding='utf-8') as f:
            json.dump(rep, f, ensure_ascii=False, indent=1)
            f.write('\n')
        print(f'→ {a.json}')
    if a.md:
        with open(a.md, 'w', encoding='utf-8') as f:
            f.write(to_markdown(rep))
        print(f'→ {a.md}')
    print(f"\n{sum(T['verdict'] == 'PASS' for T in tables)}/{len(tables)} 표 PASS" + ('' if rep['verdict'] == 'PASS' else '  ⛔ 되읽기 실패 — 봉인 · 발사 근거 없음'))
    raise SystemExit(0 if rep['verdict'] == 'PASS' else 1)


if __name__ == '__main__':
    main()
