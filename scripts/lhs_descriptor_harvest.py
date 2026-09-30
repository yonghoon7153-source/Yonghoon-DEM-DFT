#!/usr/bin/env python3
"""LHS 130 구조 디스크립터 수확기 — **일곱 등록 열을 원 dump 에서** 낸다.

    python3 scripts/lhs_descriptor_harvest.py --atom post/atom_2425000.liggghts \\
        --contact post/contact_2425000.liggghts --mesh post/mesh.stl \\
        --deck input_lhs00_000.liggghts --n-types 3 --case lhs00_000
    python3 scripts/lhs_descriptor_harvest.py --selftest

이 파일은 **판정문 §7 의 최소 계약 6개**를 도구에 고정한 것이다.
판정 = `docs/reviews/codex_verdict_lhs_descriptors_20260913.md` (HOLD) · 원장 `DESC-01~09`.
선례 = `lhs_perc_extract.py` — *"추출기와 경계 fixture 를 **결과 전에** 커밋해야 이 규약이
실재한다"* (Codex R11 B1).  그 파일의 덤프 읽기·경계 검사·쌍 찾기를 **재사용**한다
(규율 ①: 새로 짜기 전에 리포에 있는 것부터 — 어댑터에서 `run_contract.py` 를 못 보고 새로
짠 것이 `PA12-01~05` 의 절반이었다).

═══ 왜 `full_metrics.json` 을 읽지 않나 ═══

`DESC-01` 이 재현한 것: `dem_analysis_core.py:938` 이 `phi_se` 를 **이미 계산해 놓고**
`:941` 에서 τ 가 없으면 `return None` 하고, `analyze_contacts.py:430` 의 `if eff_cond:`
가드가 **기하량인 φ 두 개를 통째로 누락**시킨다.  `NET_MERGE_KEYS` 에도 φ 가 없어 복구되지
않는다.  ⇒ 완전행 필터로 학습셋을 만들면 **연결성이 약한 침대가 구조 타깃째 탈락**한다
= 결측이 물리와 상관된다.  파생물을 읽으면 그 결함을 그대로 상속한다.

═══ 계약 ① — 일곱 별칭 ↔ 실제 계산량 ═══

기호: `V_B = L_x·L_y·H` (H = **플래튼 높이**, §계약⑤) · `V_i = 4πr_i³/3`.

| 등록 별칭 | 이 도구가 내는 양 |
|---|---|
| `phi_se`  | `Σ_{i∈SE} V_i / V_B`.  **τ·전도도와 무관하게** 항상 낸다 (계약②) |
| `phi_am`  | `Σ_{i∈AM} V_i / V_B` — **직접 합**이다.  `1−φ_SE−ε/100` 같은 잔차가 아니다 |
| `coverage_AM_P_hertz_pct` | 아래 `c_i` 의 **AM_P 입자별 산술평균** (유효 분모만) |
| `coverage_AM_S_hertz_pct` | 같은 계산의 AM_S 평균 |
| `coverage_AM_total_hertz_pct` | `(N_P·C_P + N_S·C_S)/(N_P+N_S)`, **실측 입자수** 가중 |
| `tortuosity_dijkstra_SE` | SE 접촉그래프 최단경로 / 끝점 z 거리 — 아래 §τ |
| `porosity_sphere_pct_RECORD_ONLY` | `100(1 − Σ_i V_i / V_B)`.  겹침을 빼지 않는다 |

**Hertz 피복률의 정확한 정의** (`dem_analysis_core.py:172` 규약):
```
F_i = 4π r_i²  −  Σ(i 에 붙은 AM–AM 접촉면적)
c_i = min(100, 100 · Σ(i 에 붙은 AM–SE 접촉면적) / F_i)      [F_i > 0]
c_i = FREE_SURFACE_INVALID                                    [F_i ≤ 0]
```
분자는 **LIGGGHTS 가 보고한 `contact_area`**(`c_cpl[22]`)다 — 이 도구가 `πR*δ` 를 다시
계산하는 것이 **아니다**.  ⚠ `F_i ≤ 0` 을 **0 으로 접지 않는다** (`DESC-05`: 실제 무접촉과
분모 붕괴가 섞인다).  cap 발동 횟수와 분모붕괴 횟수를 **따로** 보고한다.

⚠⚠ **`hertz` 라는 별칭은 물려받은 오해다** (`L1-04`, 2026-09-13 L1 판정).  공식 LIGGGHTS
문서·구현에서 `contactArea` 는 역학 해가 아니라 **기하학적 교차 원판**이다:
`A_LIGG = π(rδ − δ²/4)` vs `A_Hertz = πR*δ` ⇒ 동일 반경에서 비 = `2 − δ/(2r)`
(r = 0.5 µm · δ/R* = 0.05 에서 **1.9875배**, 이 리포에서 재현).  등록 별칭은 **바꾸지
않지만**(판정문: *"기존 키와 frozen feature 를 세대 표시 없이 바꾸면 안 된다"*) 매 행에
`area_channel` 을 박아 **무엇을 센 값인지**를 남긴다.  권고 이름 구분은
`A_dem_geometric` / `A_hertz_elastic` / `A_plastic_model` 이다.

⚠ **전체 평균의 함정** (판정문 반례): P 1개·10 % · S 3개·각 90 % 이면 **전체 70 %** 다.
상 평균의 평균은 50 %, 총면적비는 30 %, 질량가중은 18 % — **넷이 다른 양**이다.

⚠ **Physics 피복률은 여기서 계산하지 않는다** (계약④).  `DESC-03` 이 `plastic_coverage.py`
의 `A_volume = V_overlap / H_FILM_MIN` 에서 **확대 DEM 길이 ÷ 미확대 5 nm** 혼용을
재현했고, 그 때문에 `min(caps)` 의 binding cap 이 `tabor ↔ volume` 로 뒤집힌다.  Hertz 는
그 영향 밖이지만(재현 결과 불변), **섞지 않기 위해** 이 도구는 Physics 를 아예 안 부른다.

═══ §τ — 계약 ③ ═══

`DESC-02` 가 양방향 반례를 냈다:
① `dem_analysis_core.py:502-509` 가 바닥판 source 가 없으면 **위판에 닿는 성분의 최저 z**
   를 새 source 로 승격한다 ⇒ `percolation_pct = 0` 인데 `τ = 1` 이 나온다.
② 같은 함수 `:517-522` 가 `src × top` 전수 쌍을 shuffle 해 앞 200 개만 남기므로 **서로 다른
   성분의 무경로 쌍**이 예산을 먹는다 ⇒ 관통 성분이 200 개여도 `τ = None` 이 된다.

이 도구의 규약 (**legacy 와 다르다 — 같은 컬럼에 섞지 말 것**, `DESC-04`):
- **fallback source 승격 없음.**  source = 아래 슬래브의 SE **이면서** 위 슬래브에 닿는
  성분의 구성원.  없으면 `NOT_PERCOLATING` 이고 **유한 τ 를 내지 않는다**.
- **쌍은 같은 성분 안에서만** 뽑는다 ⇒ 예산이 무경로 쌍에 소진되지 않는다.
- **간선 가중치와 경로 길이는 xy 최소영상**(`_mi_dist`) — 쌍 찾기와 **같은 규약**이다.
  (`P1-HARV-01`: 초판은 raw 좌표차를 써서 평행이동만으로 τ 가 9.66배 바뀌었다.)
- 슬래브 = 고체(AM ∪ SE) z 범위 `[min(z−r), max(z+r)]` 의 양 끝, 두께 = `r_SE,max`.
  (`lhs_perc_extract` ④ 와 같은 사고 — AM 만의 범위를 쓰면 희박한 침대에서 판정이 쉬워진다.)
  ⚠⚠ **이 규약은 아직 정당화되지 않았다** (`LHS-08`, 열림).  z 범위는 **전 입자(AM 포함)**
  가 정하는데 밴드 소속은 **SE 만** 보므로, AM 이 SE 보다 위로 솟은 침대는 위 밴드가
  구조적으로 빌 수 있다 — 실제 전극면인 `plate_z_sim` 은 이미 출력에 있는데 **안 쓴다**.
  ⇒ 산출물에 `band_detail.alt_n_top`(plate_z 규약이면 몇 명인지)을 **진단으로만** 적는다.
  규약을 바꾸는 것은 재측정 **뒤**다 — 먼저 바꾸면 바꾼 규약으로 잰 수로 그 규약을
  정당화하게 된다 (`규율 ⑤`: 후보를 고르는 코드가 곧 사각지대).
- 통계량을 **이름으로 가른다**: `tau_mean`(절단본, legacy 호환) · `tau_median` ·
  `tau_mean_untruncated` · `n_truncated`.  등록 별칭 `tortuosity_dijkstra_SE` = **`tau_mean`**.
  ⚠ 판정문 반례: `[1,1,10]` → mean **4** / recommended **1**; `[1, 20.024984]` → 절단 후
  mean **1** vs 무절단 **10.512492**.  이름이 통계량을 정하지 않으면 target 이 갈린다.

═══ 계약 ⑤ — 프로비넌스 fail-closed ═══

- atom · contact 덤프의 **TIMESTEP 이 같아야** 한다.  다르면 거부.
  (`DESC-06`: `parse_liggghts.py:243` 은 종류별 최신 파일을 **독립 선택**해 `atom_100 +
  contact_200` 을 rc=0 으로 받았다.  그리고 그 파서는 **모든 프레임 행을 이어 붙인다**.)
- `H`(플래튼 높이)는 **mesh STL 또는 명시 `--plate-z`** 로만 받는다.  **추정 금지** —
  `dem_analysis_core.py:110` 의 "mesh 없으면 최고 입자 중심" 이 부피분율에 **5.263 %**
  상대차를 낸다.
- 모든 원파일의 **sha256** 과 상별 입자수, **target 별 상태**를 함께 낸다.
- `--n-types` **필수** (`lhs_perc_extract` ⑥ 과 같은 이유: AM_P 가 우연히 0개면 2-type 으로
  보이고 AM_S 가 SE 로 오사상된다).

═══ 계약 ⑥ — 130 단독 ═══

출력은 자기 CSV/JSON 이다.  `design_performance_corpus.csv` 291 행과 **합치지 않는다**
(`DESC-08`: `d_am=0` 40 건이 지금도 학습 입력에 들어가고 `use_porosity_pct` closure 잔차가
ε SD 의 77.82 % 다).  `docs/lhs_design_dataset_20260818.md` §O-4 ⑤ 와 같은 결론.

═══ 상태 코드 ═══

`OK` · `N_A_PHASE_ABSENT`(없는 상 — 존재하는데 무접촉인 `0` 과 다르다) ·
`NOT_PERCOLATING` · **`ELECTRODE_BAND_EMPTY`** · `NO_VALID_SAMPLED_PAIR` ·
`FREE_SURFACE_INVALID` · `INPUT_MISSING`.
⚠ 한 타깃이 미정의라고 **다른 타깃이 있는 행을 통째로 버리지 않는다** (`DESC-01` 의 교훈).
⚠ `ELECTRODE_BAND_EMPTY` 는 `NOT_PERCOLATING` 의 **하위분류가 아니라 다른 사유**다
(`LHS-08`): 전자는 **규약(밴드 정의)** 을, 후자는 **물리(연결성)** 를 겨눈다.  둘을 같은
값으로 내면 *"코드 문제냐"* 에 답할 수 없다 — 실제로 130 중 116 이 그 상태였다.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

#  ★ 규율 ①: 덤프 읽기·경계 검사·주기 쌍 찾기·상 사상은 **이미 봉인돼 있다**.
from lhs_perc_extract import (  # noqa: E402
    AM_LABELS, BedRefusal, REQUIRED_BC, TYPE_MAP,
    _pairs_within, check_boundary_flags, read_atom_dump,
)
#  item 2 (09-29) — 두 구의 **정확한 교차 원판** 은 이미 있다 (규율 ①: 다시 짜지 않는다).  ★ 09-30 (Codex `LHSC-05` · 계약 (a)):
#  그 순수 기하는 `lens_geometry` 로 분리됐다 — 이 도구는 **plastic_coverage 를 어떤 모양으로도 가져오지 않는다** (DESC-03 · 계약④:
#  Physics 피복률 경로 film_area_from_overlap · A_volume = V/H_FILM_MIN 에 의존 없음).  selftest ⑬ · ㉑′ 이 소스 **전체** AST 로
#  강제한다 (허용 이름 = `PLASTIC_COVERAGE_ALLOWED` = 없음 · 가드 = `_plastic_coverage_uses` — lint 이지 완전 증명이 아니다).
from lens_geometry import intersection_disc_area as _intersection_disc_area  # noqa: E402

#: 계약 ③ — τ 표본 예산.  legacy 와 같은 수지만 **같은 성분 안에서만** 쓴다.
N_TAU_PAIRS = 200
#: 계약 ③ — legacy 절단 구간 (`dem_analysis_core.py:533`).
TAU_LO, TAU_HI = 1.0, 20.0
#: 접촉 덤프의 면적·겹침 열 (`parse_liggghts.py:47` 과 같은 규약).
COL_AREA, COL_D1, COL_D2 = 'c_cpl[22]', 'c_cpl[7]', 'c_cpl[8]'
#: J20-a (1저자 비준 09-28 밤 "권고하는걸로") — 접촉 덤프 점검용 두 열: 주기 경계 플래그 · 겹침 δ (`parse_liggghts.py` 열 사전과 같은 번호).
COL_PERIODIC, COL_DELTA = 'c_cpl[9]', 'c_cpl[23]'
#: J20-a ⓓ — 상별 벽 · 플래튼 **접촉 입자 비율**.  닿음 = 구가 그 면과 **겹친다** (겹침 깊이 r − dist > 0 · sim 단위 · 허용오차 없음).
#: ★ item 4 (09-29 · 1저자 "권고대로") — 규칙은 **하나**다: `_wall_side` (→ `wall_record` · 벽 밖 부피) · `wall_touch_fractions` ·
#:   벽 분할 피복률이 같은 함수 `_wall_contact` 를 부른다.  옛 문자열 `z - r <= z_floor · z + r >= plate_z` (접선 = 닿음) 은
#:   `_wall_side` 의 `r − dist > 0` (접선 = 안 닿음) 과 접선 입자에서 갈렸다 (selftest ⑲).  고른 쪽과 이유 = `_wall_contact` 독스트링.
WALL_TOUCH_RULE = ('floor: r - (z - z_floor) > 0 · plate: r - (plate_z - z) > 0 — overlap depth > 0; tangent (depth = 0) is '
                   'not touching (sim units, no tolerance) · one implementation `_wall_contact` shared by wall_record, '
                   'wall_touch and the coverage wall split')
#: DESC-03 · 계약④ (item 2 개정 · 09-30 LHSC-05 (a)) — 이 도구가 plastic_coverage 에서 가져와도 되는 이름: **없다** (순수 기하는
#:   `lens_geometry` 에 있다).  비어 있어야 ⑬ · ㉑′ 이 "사용 0" 을 강제한다.
PLASTIC_COVERAGE_ALLOWED = frozenset()
#: item 2 — 접촉 면적 대조 (진단 기록) 의 유효숫자 전제: LIGGGHTS `dump local` 기본 `%g` = 6 유효숫자 (`lhs_contact_audit.SIGFIG_FLOOR`
#:   와 같은 값 · WSL 감사 v2 130/130 관측 최대 6).  전제가 틀린 침대는 `n_values_beyond_6sig` 가 0 이 아니다 (그때 허용폭이 헐겁다).
AREA_CHECK_SIGFIG = 6
#: LHSC-04 R2 — 포괄 구간이 넓은 행 (기술량 · **lo 기준** · A_dump 무관 · R3b 에서 분모를 바꿨다): (hi − lo) > 이 비율 × lo.
#:   1 % 검출 **보증**은 이것이 아니라 `n_detect_1pct` (규칙 문자열) 가 준다.
AREA_CHECK_WIDE_REL = 1e-2
#: LHSC-04 R3a (Codex 재검증 2 · 09-30 밤 · 1저자 비준 "비준이야") — 생산자 (LIGGGHTS `compute pair/gran/local` add_pair) 면적 산술의 모델.
#:   공개 PUBLIC master 의 식 (Codex 열람 2026-09-30).  설치 빌드 (WSL lmp_serial · ibb lmp_mpi) 가 같은 소스인지는 **pin 파일**로만 인증한다
#:   (`producer_pin`) — 핀 없이는 결과에 installed_build_pinned=False 가 실린다 (짐작하지 않는다).
PRODUCER_AREA_MODEL = dict(
    formula=('A = -π/4 · (r−r1−r2)(r+r1−r2)(r−r1+r2)(r+r1+r2) / rsq,  r = sqrt(rsq) (rsq = dx²+dy²+dz²),  δ = r1 + r2 − r  '
             '(binary64 · 음수 · 0 을 자르지 않는다 · C++ 괄호 · 좌결합 순서 그대로 = producer_area_binary64)'),
    source=('LIGGGHTS-PUBLIC master src/compute_pair_gran_local.cpp add_pair (Codex 열람 2026-09-30) — 설치 빌드와 같은 소스인지는 '
            'pin 파일 (docs/data/liggghts_add_pair_pin.json · 환경변수 LHS_PRODUCER_PIN_FILE) 의 sha256 · formula_confirmed 로만 인증'),
    error_bound=('상자 (토큰 반올림 상자 + 생산자 δ 형성 오차 Δδ) 전체에서 |A_p − A_e| ≤ E = (π/4)/d_min² · [Π_k(m_k + Δ_k)·(1 + 13·eps) − Π_k m_k]  '
                 '— m_k = 인수 (δ, 2r1−δ, 2r2−δ, 2r1+2r2−δ) 의 상자 최대 절댓값 · Δ_k = eps·(3·S + m_k) (sqrt 뒤 두 뺄셈의 인수 형성 절대오차 · '
                 'S = r + r1 + r2 = 2r1+2r2−δ 의 상자 최대) · 13·eps ≥ 곱 3 · rsq 5 · 나눗셈 1 · π/4 2 (단위 반올림 u = eps/2 로 세면 11u) · '
                 'eps = 2^-52 · d_min ≤ 0 이면 E 가 서지 않아 미인증 (n_producer_uncertified).  실증 = --selftest ㉑‴ (공개 식 binary64 '
                 '4000 점 · 여섯 영역 · Decimal 60 자리) — 설치 빌드의 실행이 아니다.'),
)
PRODUCER_PIN_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'docs', 'data',
                                 'liggghts_add_pair_pin.json')
PRODUCER_PIN_ENV = 'LHS_PRODUCER_PIN_FILE'
PRODUCER_PIN_SCHEMA = 'liggghts_add_pair_pin/1'
AREA_CHECK_TOL_RULE = (
    '행마다 덤프 토큰 구간 [A_dump ± h(A_dump)] 이 허용 구간 [lo − E, hi + E] 와 만나지 않으면 초과로 센다 (셈만 · 거부 없음 · 피복률 값 불변).  '
    '[lo, hi] = 반올림 상자 {r1 ± h(r1)} × {r2 ± h(r2)} × {δ ± (h(δ) + Δδ)} (Δδ = eps·(3S + |δ|) = 생산자 δ 형성 오차 — 상자가 정확한 δ 를 담게) '
    '위 교차 원판 A 의 포괄 구간 (LHSC-04 R2): A = lens_geometry.intersection_disc_area 와 같은 식의 인수형 '
    'π·δ(2r1−δ)(2r2−δ)(2r1+2r2−δ)/(4d²) (d = r1 + r2 − δ · 상쇄 없음) · ① 상자가 δ ≤ 0 · d ≤ 0 · 한 구가 다른 구 안 (2r_i − δ ≤ 0) 에 '
    '통째로 있으면 A ≡ 0 · ② 네 인수가 상자 전체에서 양수이고 ln A 의 편도함수 세 구간 (인수 역수의 합) 이 0 을 포함하지 않으면 두 꼭짓점 값이 '
    '정확한 최소 · 최대 (각 인수의 형성 오차만큼 상대 여유) · ③ 아니면 인수 구간의 곱 ∩ 덧셈형 항별 구간 π/4·[2(r1²+r2²) − d² − (r1²−r2²)²/d²] ∩ '
    '기하 상한 π·min(r1, r2)² · ④ 인수가 상자 안에서 부호를 바꾸면 (포함 경계 · d → 0 · δ → 0 이 상자 안) 하한 0 (boundary 가지) · 상한 = 덧셈형 '
    '항별 상한 ∩ 기하 상한.  [lo, hi] 에는 기준 평가 여유 16·eps·π·max(r1, r2)² (부동소수 덧셈형 원판으로 대조할 때의 상쇄 오차 · 생산자 여유 아님) 만 바깥으로 더한다.  E = 생산자 (PRODUCER_AREA_MODEL) 산술의 상자 절대 오차 상한 (LHSC-04 R3a — 옛 고정 "생산자 바닥" 여유는 없앴다): '
    'd_min ≤ 0 이면 E 가 서지 않아 **미인증** (n_producer_uncertified · 시험 · 초과에서 뺀다) · 음수 A_dump 는 정의역 밖 생산값 '
    '(n_area_dump_negative · 초과 아님 · 시험에서 뺀다).  h(v) = 0.5·10^(E(v) − 5) = 6 유효숫자 %g 토큰의 반올림 반폭 (E = 십진 지수 · '
    '끝 0 이 지워진 토큰도 형식 정밀도 6 으로).  기하: A 는 δ 에 따라 0 에서 d² = |r1² − r2²| 의 극대 π·min(r1, r2)² 까지 올랐다가 포함 경계 '
    'd = |r1 − r2| 에서 다시 0 으로 **연속**해서 내려간다 (동일 반경 d → 0 퇴화만 식의 극한 π r² 과 코드의 d ≤ 0 → 0 이 어긋난다).  '
    '보고: n_tested (인증 · 비음수 행) · n_beyond_tol · n_producer_uncertified · n_area_dump_negative · n_area_dump_zero · '
    'n_lower_bound_zero (실제 lo == 0 — 너무 작은 면적은 못 잡는다) · n_boundary_branch (④ 가지 수) · n_wide_enclosure ((hi − lo) > '
    'AREA_CHECK_WIDE_REL·lo · lo > 0 · 기술량) · n_detect_1pct = 검출 보증 (LHSC-04 R3b): 참 면적이 [lo, hi] 어디에 있어도 ±1 % 치환의 '
    '토큰 구간이 허용 구간과 분리 — 1.01·(lo − E) − 2h₊ > hi + E ∧ 0.99·(hi + E) + 2h₋ < lo − E (h± = 그 크기 범위의 출력 반올림 반폭 최대 · '
    '인증 행 · lo − E > 0) — A_dump 와 무관 (치환해도 분류가 안 바뀐다).')
#: L1-04 — 이 열이 **무엇인지** 매 행에 박는다 (별칭의 `hertz` 는 물려받은 오해다).
AREA_CHANNEL = ('dem_geometric_c_cpl22 — LIGGGHTS 기하 교차 원판 pi(r d - d^2/4); '
                'Hertz 탄성 pi R* d 가 **아니다** (동일 반경 비 = 2 - d/(2r))')

STATUS_OK = 'OK'
STATUS_ABSENT = 'N_A_PHASE_ABSENT'
STATUS_NOPERC = 'NOT_PERCOLATING'
#: LHS-08 — `NOT_PERCOLATING` 이 접고 있던 **다른 원인**: 전극 밴드에 SE 가 0 명이라
#: 성분을 볼 것도 없이 끝난 경우.  ⓐ(밴드 빔)/ⓑ(진짜 미관통)를 같은 값으로 내면
#: 실물 116 건이 어느 쪽인지 **산출물만으로 판별 불가**다.
STATUS_BAND_EMPTY = 'ELECTRODE_BAND_EMPTY'
STATUS_NOPAIR = 'NO_VALID_SAMPLED_PAIR'
STATUS_MISSING = 'INPUT_MISSING'
#: 벽 τ 는 플래튼 높이가 있어야 밴드가 선다 — 없으면 추정하지 않고 이 상태로 둔다.
STATUS_NO_PLATE = 'PLATE_Z_MISSING'
#: LHS-08 규약 판단 (1저자 비준 2026-09-28 "벽 기준 τ 새 열") — 밴드 = 바닥 벽 (z = Z_FLOOR) · 플래튼 (plate_z) 에서
#: 반지름 최대값 두께.  옛 `harvest_v1/solid_zrange/…` 는 **그대로** 두고 이 규약은 새 키 (`wall_tau`) 로만 낸다.
TAU_WALL_CONVENTION = 'harvest_v3/wall_z0_plate/rSEmax/no_fallback/same_component'


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        for blk in iter(lambda: fh.read(1 << 20), b''):
            h.update(blk)
    return h.hexdigest()


def last_timestep(path):
    """마지막 `ITEM: TIMESTEP` 값.  atom·contact 덤프 모두에 쓴다 (계약⑤)."""
    ts = None
    with open(path, 'r', encoding='utf-8', errors='replace') as fh:
        want = False
        for ln in fh:
            if want:
                try:
                    ts = int(float(ln.split()[0]))
                except (ValueError, IndexError):
                    pass
                want = False
            elif ln.startswith('ITEM: TIMESTEP'):
                want = True
    if ts is None:
        raise BedRefusal(f'{path}: `ITEM: TIMESTEP` 이 없다')
    return ts


def read_contact_dump(path, extra_cols=None):
    """**마지막 프레임만**의 (id1, id2, contact_area) (+ `extra_cols` 를 주면 그 열들의 dict 를 다섯째로).

    ⚠ `parse_liggghts.parse_contact_file` 은 모든 프레임 행을 **이어 붙인다**
    (`DESC-06`).  여기서는 마지막 `ITEM: ENTRIES` 블록만 읽는다.
    `extra_cols` 의 열이 헤더에 없으면 그 값은 None (거부하지 않는다 — 점검 도구가 "열 없음" 으로 적는다).
    """
    with open(path, 'r', encoding='utf-8', errors='replace') as fh:
        lines = fh.read().splitlines()
    starts = [i for i, ln in enumerate(lines) if ln.startswith('ITEM: ENTRIES')]
    if not starts:
        raise BedRefusal(f'{path}: `ITEM: ENTRIES` 가 없다 — LIGGGHTS local 덤프가 아니다')
    i = starts[-1]
    headers = lines[i].replace('ITEM: ENTRIES', '').strip().split()
    for col in (COL_D1, COL_D2, COL_AREA):
        if col not in headers:
            raise BedRefusal(
                f'{path}: 접촉 열 {col} 이 없다 (있는 열: {headers}).  '
                'DEM contact-area 규약을 모르는 채로 피복률을 내지 않는다')
    ia, i1, i2 = headers.index(COL_AREA), headers.index(COL_D1), headers.index(COL_D2)
    ix = {c: (headers.index(c) if c in headers else None) for c in (extra_cols or ())}
    id1, id2, area = [], [], []
    xv = {c: [] for c in ix}
    i += 1
    while i < len(lines) and not lines[i].startswith('ITEM:'):
        v = lines[i].split()
        if len(v) == len(headers):
            id1.append(int(float(v[i1])))
            id2.append(int(float(v[i2])))
            area.append(float(v[ia]))
            for c, k in ix.items():
                if k is not None:
                    xv[c].append(float(v[k]))
        i += 1
    base = (np.asarray(id1, dtype=np.int64), np.asarray(id2, dtype=np.int64),
            np.asarray(area, dtype=np.float64), tuple(headers))
    if extra_cols is None:
        return base
    return base + ({c: (np.asarray(xv[c], dtype=np.float64) if ix[c] is not None else None) for c in ix},)


def count_blocks(path, marker):
    """파일 안 `marker` 로 시작하는 줄 수 — 'ITEM: ENTRIES' = 접촉 프레임 수 · 'ITEM: TIMESTEP' = 원자 프레임 수."""
    n = 0
    with open(path, 'r', encoding='utf-8', errors='replace') as fh:
        for ln in fh:
            if ln.startswith(marker):
                n += 1
    return n


def _pair_dup_counts(id1, id2):
    """무순서 쌍 기준 (고유 쌍 수, 두 번 이상 나온 쌍 수, 초과 행 수, 자기쌍 행 수) — a–b 와 b–a 는 같은 쌍이다.

    item 3 — `scan_contact_dump` (기록) 와 `contact_gate` (거부) 가 **같은 정의 하나**를 쓴다 (계산은 옛 `scan_contact_dump` 그대로).
    """
    id1, id2 = np.asarray(id1, dtype=np.int64), np.asarray(id2, dtype=np.int64)
    n_self = int((id1 == id2).sum())
    if not id1.size:
        return 0, 0, 0, n_self
    a, b = np.minimum(id1, id2), np.maximum(id1, id2)
    _u, cnt = np.unique(np.stack([a, b], axis=1), axis=0, return_counts=True)
    return int(_u.shape[0]), int((cnt > 1).sum()), int((cnt - 1).sum()), n_self


def scan_contact_dump(path):
    """J20-a ⓐ·ⓑ — 접촉 덤프가 "한 프레임 · 쌍마다 한 행" 인지 센다 (수확 값에는 영향 없음 — 수확은 마지막 블록만 읽는다).

    웹앱 경로 (`parse_liggghts.parse_contact_file` → `dem_analysis_core.calc_*_cn` · `calc_interface_area`) 는 **모든 프레임 행을
    이어 붙이고 행마다 두 입자에 +1** 한다 — 거르지 않는다.  합성 2 프레임 파일에서 SE-SE CN 이 정확히 2 배 (DESC-06 실증).
    ⇒ `n_frames ≠ 1` 이나 `n_dup_rows > 0` 이면 웹앱 CN · 접촉 수 · 면적 합이 부푼다.  δ ≤ 0 행도 접촉으로 센다 (있는지 기록).
    """
    n_frames = count_blocks(path, 'ITEM: ENTRIES')
    if n_frames == 0:
        raise BedRefusal(f'{path}: `ITEM: ENTRIES` 가 없다 — LIGGGHTS local 덤프가 아니다')
    id1, id2, _area, headers, ex = read_contact_dump(path, extra_cols=(COL_DELTA, COL_PERIODIC))
    n = int(id1.size)
    n_unique, n_dup_pairs, n_dup_rows, n_self = _pair_dup_counts(id1, id2)   # item 3 — `contact_gate` 와 같은 정의 하나
    dl, pf = ex[COL_DELTA], ex[COL_PERIODIC]
    return dict(n_frames=int(n_frames), n_rows_last=n, n_unique_pairs=n_unique,
                n_dup_pairs=n_dup_pairs, n_dup_rows=n_dup_rows, n_self_pairs=n_self,
                n_delta_nonpos=(None if dl is None else int((dl <= 0.0).sum())),
                delta_min=(None if dl is None or not dl.size else float(dl.min())),
                n_periodic_flag=(None if pf is None else int((pf != 0.0).sum())),
                has_delta_col=dl is not None, has_periodic_col=pf is not None)


#: item 3 — 접촉 행의 문 규칙 (피복률 · 면적 대조가 실제로 쓰는 마지막 블록 배열 그대로).
CONTACT_GATE_RULE = ('중복 무순서 쌍 (a–b 두 번 · a–b 와 b–a) · 자기쌍 (a–a) → BedRefusal (중복은 한 접촉의 면적이 피복률 분자 · 분모에 '
                     '두 번 들어가는데 status 는 OK 로 남는다 · 자기쌍은 접촉이 아니다 — AM 이면 그 입자 분모에서 면적이 두 번 빠진다) · '
                     '고아 행 (id 가 원자 프레임에 없다) → 셈만 (그 행은 전처럼 피복률 · 면적 대조에서 빠진다 — 이제 기록된다)')


def contact_gate(ids, c1, c2):
    """item 3 (09-29 · 1저자 "권고대로") — 피복률에 들어가는 접촉 행의 문 (마지막 블록 · 수확이 실제로 쓰는 배열).

    ① 중복 무순서 쌍 · 자기쌍 → **거부** (`BedRefusal` — 수확기의 기존 거부 형식 · CLI rc 2 · 배치는 케이스 실패로 적는다)
    ② 고아 행 → **셈** (그 행은 전처럼 피복률 · 면적 대조에서 빠진다).
    옛 코드는 둘 다 조용했다: `coverage_hertz` 가 고아 행을 `continue` 로 건너뛰었고, 같은 AM–SE 행 두 번은 면적을 두 번 더해 피복률을
    두 배로 status OK 로 냈다 (selftest ㉒).  `scan_contact_dump` 는 중복을 세기만 했다 (J20-a · 수확 값 무영향).  중복 정의는
    `scan_contact_dump` 와 같은 `_pair_dup_counts` 하나.
    ⚠ 130 실측 (J20-a ① 감사 v2 · WSL 09-29): 중복 0 · 자기쌍 0 · 고아 0 ⇒ 이 문은 130 에서 거부하지 않는다.  lhsx 64 는 그 감사를
      받지 않았다 — 재수확 v3 에서 이 문을 처음 지난다.
    """
    c1, c2 = np.asarray(c1, dtype=np.int64), np.asarray(c2, dtype=np.int64)
    known = np.asarray(ids, dtype=np.int64)
    in1, in2 = np.isin(c1, known), np.isin(c2, known)
    n_u, n_dp, n_dr, n_self = _pair_dup_counts(c1, c2)
    rec = dict(n_rows=int(c1.size), n_unique_pairs=n_u, n_orphan_rows=int((~(in1 & in2)).sum()),
               n_orphan_ids=int(np.union1d(c1[~in1], c2[~in2]).size),
               n_dup_pairs=n_dp, n_dup_rows=n_dr, n_self_rows=n_self, rule=CONTACT_GATE_RULE)
    if n_dr or n_self:
        raise BedRefusal(f'접촉 덤프 마지막 블록에 중복 무순서 쌍 {n_dp} (초과 행 {n_dr}) · 자기쌍 {n_self} — 중복은 한 접촉의 면적을 '
                         '피복률에 두 번 넣고 자기쌍은 접촉이 아니다 (item 3).  숫자를 내지 않는다')
    return rec


def _half_unit(v, sig=AREA_CHECK_SIGFIG):
    """`%g` 로 sig 유효숫자를 적은 토큰의 반올림 반폭 0.5·10^(E − sig + 1) (E = |v| 의 십진 지수) · 0 → 0 (배열).

    `%g` 는 끝의 0 을 지우므로 토큰 자신의 자릿수가 아니라 **형식 정밀도 sig** 로 잰다 (`lhs_contact_audit._half_ulp` 와 같은 규약 —
    `0.005` 의 반폭은 5e-9 이지 5e-4 가 아니다: 토큰 자릿수로 재면 폭이 10⁵ 배 헐거워진다 = false-green.  감사기 v2 가 `SELF-63`
    (v1 의 고정 폭이 반올림보다 좁아 거짓 FLAG) 을 고칠 때 적은 반대쪽 함정).
    """
    v = np.abs(np.asarray(v, dtype=np.float64))
    out = np.zeros_like(v)
    nz = v > 0
    if nz.any():
        x = v[nz]
        e = np.floor(np.log10(x))
        e = np.where(np.power(10.0, e) > x, e - 1.0, e)            # log10 반올림이 십진 지수를 한 칸 틀리는 경우 (10 의 거듭제곱 근처)
        e = np.where(np.power(10.0, e + 1.0) <= x, e + 1.0, e)
        out[nz] = 0.5 * np.power(10.0, e - sig + 1)
    return out


def _n_beyond_sig(v, sig=AREA_CHECK_SIGFIG):
    """sig 유효숫자로 다시 적어 되읽으면 값이 바뀌는 (유한) 값의 수 — 0 이 아니면 덤프가 sig 보다 정밀하다 (그러면 반폭 h 가 헐겁다)."""
    fmt = '{:.%dg}' % sig
    return int(sum(1 for x in np.asarray(v, dtype=np.float64).ravel().tolist()
                   if np.isfinite(x) and float(fmt.format(x)) != x))


_EPS = float(np.finfo(np.float64).eps)


def _iv_lin(parts):
    """Σ c·[lo, hi] (서로 독립인 구간의 선형 결합) — 정확한 끝점 + 부동소수 바깥 여유 (곱 · 합 반올림 몫)."""
    lo = hi = mag = 0.0
    for c, a, b in parts:
        x, y = c * a, c * b
        lo += min(x, y)
        hi += max(x, y)
        mag += max(abs(x), abs(y))
    pad = 4.0 * _EPS * mag
    return lo - pad, hi + pad


def _lens_factored(a, b, dl):
    """교차 원판 A = π·δ(2r1−δ)(2r2−δ)(2r1+2r2−δ) / (4(r1+r2−δ)²) — `lens_geometry` 의 덧셈형 a² 와 **같은 식**의 인수분해.

    4d²a² = 4d²r1² − (d² − r2² + r1²)² = (r1+r2−d)(r2−r1+d)(r1−r2+d)(r1+r2+d) 이고 d = r1 + r2 − δ 를 넣으면 위 네 인수가 된다
    (상쇄 없음 — 얕은 접촉에서도 상대 오차가 작다).  부분 겹침 (네 인수 · d 가 양수) 에서만 부른다."""
    d = a + b - dl
    return float(np.pi * dl * (2.0 * a - dl) * (2.0 * b - dl) * (2.0 * a + 2.0 * b - dl) / (4.0 * d * d))


def _token_box(r1, r2, delta, sig=AREA_CHECK_SIGFIG):
    """한 행의 토큰 반올림 상자 → 인수 구간 (A · B · D · f1 · f2 · f3 · dd · dpad) — `_area_enclosure` · `_producer_error_bound` 가 **같은 상자**를 쓴다.

    sig=None 이면 반폭 0 (점 — 끝점의 부동소수 바깥 여유만).  δ 상자는 반폭 h(δ) 에 **생산자 δ 형성 오차** Δδ = eps·(3S + |δ|) 를 더한다 —
    덤프의 δ = r1 + r2 − sqrt(rsq) 는 binary64 로 만들어져 정확한 δ 와 그만큼 다를 수 있고, 상자가 정확한 δ 를 담아야 [lo, hi] 가 정확한
    면적을 담는다 (LHSC-04 R3a).  반지름은 생산자가 그대로 쓰는 double 이라 토큰 반폭만.  (Δδ ≈ 1e-18·(r 1e-3) ≪ h ≥ 5e-10·(δ 1e-3))."""
    a, b, dl = float(r1), float(r2), float(delta)
    if sig is None:
        h1 = h2 = hd = 0.0
    else:
        h1, h2, hd = (float(_half_unit(v, sig)) for v in (a, b, dl))
    s_up = 2.0 * (abs(a) + h1) + 2.0 * (abs(b) + h2) + abs(dl) + hd          # S = 2r1 + 2r2 − δ 의 상자 상한
    dpad = _EPS * (3.0 * s_up + abs(dl) + hd)
    A0, A1 = _iv_lin([(1.0, a - h1, a - h1)])[0], _iv_lin([(1.0, a + h1, a + h1)])[1]
    B0, B1 = _iv_lin([(1.0, b - h2, b - h2)])[0], _iv_lin([(1.0, b + h2, b + h2)])[1]
    D0, D1 = _iv_lin([(1.0, dl - hd - dpad, dl - hd - dpad)])[0], _iv_lin([(1.0, dl + hd + dpad, dl + hd + dpad)])[1]
    A0, B0 = max(A0, 0.0), max(B0, 0.0)
    return dict(A=(A0, A1), B=(B0, B1), D=(D0, D1), dpad=dpad,
                f1=_iv_lin([(2.0, A0, A1), (-1.0, D0, D1)]),                  # 2r1 − δ
                f2=_iv_lin([(2.0, B0, B1), (-1.0, D0, D1)]),                  # 2r2 − δ
                f3=_iv_lin([(2.0, A0, A1), (2.0, B0, B1), (-1.0, D0, D1)]),   # 2r1 + 2r2 − δ  (= r + r1 + r2 = S)
                dd=_iv_lin([(1.0, A0, A1), (1.0, B0, B1), (-1.0, D0, D1)]))   # d = r1 + r2 − δ


def _area_enclosure(r1, r2, delta, sig=AREA_CHECK_SIGFIG):
    """LHSC-04 R2 (Codex 09-30 밤) — 행마다 토큰 반올림 상자 (`_token_box`) 위 교차 원판 A 의 포괄 구간 (lo, hi) · 하한 0 표지 · 방법.

    규칙 = `AREA_CHECK_TOL_RULE` ①–④.  옛 판 (축별 탐침의 합 B) 은 "A 가 각 입력에 단조" 라는 틀린 가정 위에 있었고, 다른 두 반지름이
    한 토큰으로 합쳐지는 **공동** 반올림을 덮지 못했다 (Codex 반례 diff/B 1.332).  여기서는 상자 전체를 감싼다 — 꼭짓점 두 개가 정확한
    최소 · 최대인 것은 ln A 의 편도함수 세 구간이 0 을 포함하지 않을 때뿐이고 (인수 역수의 합으로 상자 위에서 잰다), 그렇지 않으면
    구간 곱 · 덧셈형 항별 구간 · 기하 상한의 교집합으로 **넓게** 감싼다 (넓다는 것은 `n_wide_enclosure` 로 따로 센다).
    ★ R3a (Codex 재검증 2): 옛 판이 바깥에 더하던 고정 여유 32·eps·π·max(r)² ("생산자 부동소수 바닥") 은 없앴다 — 생산자 산술 오차는
    상자 위 절대 상한 E (`_producer_error_bound`) 가 행마다 따로 준다 (거리 하한이 0 에 닿는 상자는 인증하지 않는다).
    반환: lo · hi (배열) · lb0 (하한 0 = ④ 가지) · how ('zero' · 'corner' · 'interval' · 'boundary')."""
    r1, r2, delta = (np.asarray(v, dtype=np.float64).ravel() for v in (r1, r2, delta))
    n = int(r1.size)
    lo, hi = np.zeros(n), np.zeros(n)
    lb0 = np.zeros(n, dtype=bool)
    how = np.empty(n, dtype=object)
    for i in range(n):
        bx = _token_box(float(r1[i]), float(r2[i]), float(delta[i]), sig)
        (A0, A1), (B0, B1), (D0, D1) = bx['A'], bx['B'], bx['D']
        f1, f2, f3, dd = bx['f1'], bx['f2'], bx['f3'], bx['dd']
        cap = np.pi * min(A1, B1) ** 2 * (1.0 + 4.0 * _EPS)           # 0 ≤ A ≤ π·min(r1, r2)² (교차원 반지름 ≤ 작은 구의 반지름)
        #  기준 평가 여유 — 정확한 A 의 포괄에는 불필요하나, 원판을 **부동소수** 덧셈형 (lens_geometry 의 a² − p² · 큰 반지름끼리 상쇄) 으로
        #  평가해 대조할 때 (㉑″ · Codex audit_geometry 의 actual_float) 극값 근처에서 ~2·eps·(max r)² 만큼 넘을 수 있다.  생산자 여유가 아니다
        #  (그것은 E · `_producer_error_bound`).
        refpad = 16.0 * _EPS * np.pi * max(A1, B1) ** 2
        if D1 <= 0.0 or dd[1] <= 0.0 or f1[1] <= 0.0 or f2[1] <= 0.0:
            lo[i], hi[i], how[i] = 0.0, refpad, 'zero'                # ① 상자 전체가 안 닿음 · d ≤ 0 · 포함 → A ≡ 0
            continue
        #  덧셈형 항별 상한 (d > 0 인 점에서 성립 — ③ · ④ 공통)
        t1 = (2.0 * (A0 * A0 + B0 * B0), 2.0 * (A1 * A1 + B1 * B1))
        u = (A0 * A0 - B1 * B1, A1 * A1 - B0 * B0)
        nlo = 0.0 if u[0] <= 0.0 <= u[1] else min(u[0] * u[0], u[1] * u[1])
        nhi = max(u[0] * u[0], u[1] * u[1])
        dlo_pos = max(dd[0], 0.0)
        add_hi = np.pi * (t1[1] - dlo_pos * dlo_pos - nlo / (dd[1] * dd[1])) / 4.0 + 8.0 * _EPS * np.pi * t1[1]
        if D0 > 0.0 and f1[0] > 0.0 and f2[0] > 0.0 and dd[0] > 0.0:
            #  ② · ③ 부분 겹침 내부 — ln A 편도함수 구간 (인수 역수의 합) 이 0 을 포함하지 않으면 꼭짓점 두 개가 정확한 최소 · 최대
            inv = {k: (1.0 / v[1], 1.0 / v[0]) for k, v in (('d', (D0, D1)), ('1', f1), ('2', f2), ('3', f3), ('D', dd))}
            gr1 = _iv_lin([(2.0, *inv['1']), (2.0, *inv['3']), (-2.0, *inv['D'])])
            gr2 = _iv_lin([(2.0, *inv['2']), (2.0, *inv['3']), (-2.0, *inv['D'])])
            gdl = _iv_lin([(1.0, *inv['d']), (-1.0, *inv['1']), (-1.0, *inv['2']), (-1.0, *inv['3']), (2.0, *inv['D'])])
            if all(g[0] > 0.0 or g[1] < 0.0 for g in (gr1, gr2, gdl)):
                up = [(A1 if gr1[0] > 0.0 else A0), (B1 if gr2[0] > 0.0 else B0), (D1 if gdl[0] > 0.0 else D0)]
                dn = [(A0 if gr1[0] > 0.0 else A1), (B0 if gr2[0] > 0.0 else B1), (D0 if gdl[0] > 0.0 else D1)]

                def _rel(x, y, z):                                    # 인수형 한 점 계산의 상대 오차 상한 (인수 형성 · 곱 · 나눗셈)
                    dz = x + y - z
                    return _EPS * (8.0 + (2 * x + abs(z)) / (2 * x - z) + (2 * y + abs(z)) / (2 * y - z)
                                   + (2 * x + 2 * y + abs(z)) / (2 * x + 2 * y - z) + 2.0 * (x + y + abs(z)) / dz)
                lo[i] = _lens_factored(*dn) * (1.0 - 2.0 * _rel(*dn)) - refpad
                hi[i] = _lens_factored(*up) * (1.0 + 2.0 * _rel(*up)) + refpad
                how[i] = 'corner'
                continue
            #  ③ 인수 구간 곱 ∩ 덧셈형 항별 구간 ∩ 기하 상한
            p_lo = np.pi * D0 * f1[0] * f2[0] * f3[0] / (4.0 * dd[1] * dd[1]) * (1.0 - 16.0 * _EPS)
            p_hi = np.pi * D1 * f1[1] * f2[1] * f3[1] / (4.0 * dd[0] * dd[0]) * (1.0 + 16.0 * _EPS)
            t3hi = nhi / (dd[0] * dd[0])
            add_lo = (np.pi * (t1[0] - dd[1] * dd[1] - t3hi) / 4.0
                      - 8.0 * _EPS * np.pi * (t1[1] + dd[1] * dd[1] + t3hi))
            lo[i] = max(p_lo, add_lo, 0.0) - refpad
            hi[i] = min(p_hi, add_hi, cap) + refpad
            how[i] = 'interval'
            continue
        #  ④ 인수가 상자 안에서 부호를 바꾼다 (포함 경계 · d → 0 · δ → 0 이 상자 안) — 그 점에서 A = 0 이 되므로 하한 0
        lo[i], hi[i], lb0[i], how[i] = 0.0, min(add_hi, cap) + refpad, True, 'boundary'
    return np.maximum(lo, 0.0), hi, lb0, how


def _producer_abs_error(dl, f1, f2, f3, dd):
    """`PRODUCER_AREA_MODEL['error_bound']` — 인수 구간 다섯 ((lo, hi) · δ · 2r1−δ · 2r2−δ · 2r1+2r2−δ · d) 위 생산자 면적의 **절대** 오차 상한.

    d 하한 ≤ 0 이면 inf (미인증 — 상자가 동심 · 그 너머를 담아 1/rsq 가 서지 않는다).  유도 (LHSC-04 R3a): 생산 식은 (π/4)·Π_k f_k / rsq 의
    binary64 계산이고 f_k 는 sqrt(rsq) 뒤 두 뺄셈으로 만들어진다 → |δf_k| ≤ eps·(3S + |f_k|) (단위 반올림 u = eps/2 로 세면 상수 2.75 · 0.5 —
    여유를 둔 값) · 곱 3 · rsq 5 · 나눗셈 1 · π/4 2 회 반올림 = 11u ≤ 13·eps 의 상대 오차 → |Π(f+δf)(1+ε) − Π f| ≤ Π(m+Δ)(1+13eps) − Π m
    (m = |f| 의 상자 최대 · 전개가 전부 양수라 2 차 이상 항까지 포함 — 상쇄 없이 항별로 더한다) · 1/rsq ≤ 1/d_min².  실증 ㉑‴."""
    dmin = float(dd[0])
    if not dmin > 0.0:
        return float('inf')
    m = [max(abs(float(v[0])), abs(float(v[1]))) for v in (dl, f1, f2, f3)]
    S = m[3]
    dlt = [_EPS * (3.0 * S + mk) for mk in m]
    err = 0.0                                                          # Σ_{T ≠ ∅} Π_{k∈T} Δ_k Π_{k∉T} m_k (상쇄 없음)
    for mask in range(1, 16):
        term = 1.0
        for k in range(4):
            term *= dlt[k] if (mask >> k) & 1 else m[k]
        err += term
    pmd = (m[0] + dlt[0]) * (m[1] + dlt[1]) * (m[2] + dlt[2]) * (m[3] + dlt[3])
    return float((np.pi / 4.0) / (dmin * dmin) * (err + 13.0 * _EPS * pmd))


def _producer_error_bound(r1, r2, delta, sig=AREA_CHECK_SIGFIG):
    """행마다 (E, 미인증) — E = `_producer_abs_error` (같은 `_token_box`) · 미인증 = E 가 유한하지 않다 (d 하한 ≤ 0)."""
    r1, r2, delta = (np.asarray(v, dtype=np.float64).ravel() for v in (r1, r2, delta))
    E = np.empty(int(r1.size), dtype=np.float64)
    for i in range(int(r1.size)):
        bx = _token_box(float(r1[i]), float(r2[i]), float(delta[i]), sig)
        E[i] = _producer_abs_error(bx['D'], bx['f1'], bx['f2'], bx['f3'], bx['dd'])
    return E, ~np.isfinite(E)


def producer_area_binary64(radi, radj, dx):
    """공개 LIGGGHTS-PUBLIC add_pair 의 면적 · δ 를 **연산 순서대로** 옮긴 binary64 스칼라 (`PRODUCER_AREA_MODEL`) — 시험 · 감사용.

    ⚠ DEM 실행도 설치 빌드의 인증도 아니다 (Codex 재검증 2 `audit_producer.py` 와 같은 이식 · dy = dz = 0).  C++ `(r-radi-radj)` 는
    `((r-radi)-radj)` · 곱은 좌결합 · 그 뒤 rsq 로 나눈다 · 음수 · 0 을 자르지 않는다."""
    rsq = dx * dx + 0.0 * 0.0 + 0.0 * 0.0
    r = math.sqrt(rsq)
    area = -math.pi / 4 * ((r - radi - radj) * (r + radi - radj) * (r - radi + radj) * (r + radi + radj)) / rsq
    return area, radi + radj - r


def producer_pin(path=None):
    """설치된 생산자 (LIGGGHTS 빌드) 의 add_pair 소스 핀 → {pinned, pin, reason, file}.

    파일 = `path` · 환경변수 `LHS_PRODUCER_PIN_FILE` · 기본 `docs/data/liggghts_add_pair_pin.json` 순.  형식 (`liggghts_add_pair_pin/1`):
    source_file (빌드 소스의 compute_pair_gran_local.cpp 경로) · sha256 (64 hex) · host · date · build · formula_confirmed (사람이 add_pair
    본문이 `PRODUCER_AREA_MODEL['formula']` 와 같음을 확인했다는 뜻 · true 여야 핀).  없거나 깨지면 pinned False + 사유 — 결과
    (`contact_area_check`.producer_model) 에 그대로 실린다 (짐작하지 않는다 · 규율 ④)."""
    file = path or os.environ.get(PRODUCER_PIN_ENV) or PRODUCER_PIN_FILE
    try:
        with open(file, encoding='utf-8') as fh:
            raw = json.load(fh)
    except (OSError, ValueError) as e:
        return dict(pinned=False, pin=None, file=file, reason=f'pin 파일 없음 또는 못 읽음 ({type(e).__name__}) — 설치 빌드 add_pair 미인증')
    if not isinstance(raw, dict) or raw.get('schema') != PRODUCER_PIN_SCHEMA:
        return dict(pinned=False, pin=None, file=file, reason=f'pin schema 가 {PRODUCER_PIN_SCHEMA} 가 아니다')
    sha = raw.get('sha256')
    if not (isinstance(sha, str) and re.fullmatch(r'[0-9a-f]{64}', sha)):
        return dict(pinned=False, pin=None, file=file, reason='pin sha256 이 64 hex 가 아니다')
    if not (isinstance(raw.get('source_file'), str) and raw['source_file'].strip()):
        return dict(pinned=False, pin=None, file=file, reason='pin source_file 이 비었다')
    if raw.get('formula_confirmed') is not True:
        return dict(pinned=False, pin=None, file=file, reason='formula_confirmed 가 true 가 아니다 (add_pair 본문 대조를 사람이 확인해야 핀)')
    pin = {k: raw.get(k) for k in ('source_file', 'sha256', 'host', 'date', 'build')}
    return dict(pinned=True, pin=pin, file=file, reason='')


def _contact_area_rows(r1, r2, delta, area):
    """행마다 (A_calc, lo, hi, lb0, 초과 여부, 진단 dict) — 규칙 `AREA_CHECK_TOL_RULE`.  A_calc = lens_geometry 의 교차 원판 (점 값 ·
    기술 통계용 · 재구현 없음) · 초과 = 인증 · 비음수 행에서 덤프 토큰 구간 [A ± h(A)] 이 허용 구간 [lo − E, hi + E] 와 만나지 않는다.
    진단 dict (배열): producer_err E · uncertified · negative · detect_1pct (R3b 검출 보증) · how · wide (lo 기준) · lo_zero."""
    r1, r2 = np.asarray(r1, dtype=np.float64).ravel(), np.asarray(r2, dtype=np.float64).ravel()
    delta, area = np.asarray(delta, dtype=np.float64).ravel(), np.asarray(area, dtype=np.float64).ravel()
    ac = np.asarray([_intersection_disc_area(a, b, d) for a, b, d in zip(r1.tolist(), r2.tolist(), delta.tolist())],
                    dtype=np.float64).reshape(r1.shape)
    lo, hi, lb0, how = _area_enclosure(r1, r2, delta)
    E, unc = _producer_error_bound(r1, r2, delta)
    Ef = np.where(unc, 0.0, E)
    neg = area < 0.0
    ha = _half_unit(area)
    lo_p, hi_p = lo - Ef, hi + Ef
    beyond = (~unc) & (~neg) & ((area - ha > hi_p) | (area + ha < lo_p))
    #  R3b — 검출 보증: 참 면적이 [lo, hi] 어디에 있어도 ±1 % 치환의 토큰 구간 (출력 반올림 2h 포함) 이 허용 구간과 분리
    okp = (~unc) & (lo_p > 0.0)
    hplus = np.maximum(_half_unit(1.01 * np.maximum(lo_p, 0.0)), _half_unit(1.01 * np.maximum(hi_p, 0.0)))
    hminus = np.maximum(_half_unit(0.99 * np.maximum(lo_p, 0.0)), _half_unit(0.99 * np.maximum(hi_p, 0.0)))
    det = okp & (1.01 * lo_p - 2.0 * hplus > hi_p) & (0.99 * hi_p + 2.0 * hminus < lo_p)
    extra = dict(producer_err=E, uncertified=unc, negative=neg, detect_1pct=det, how=how,
                 wide=(lo > 0.0) & ((hi - lo) > AREA_CHECK_WIDE_REL * lo), lo_zero=(lo == 0.0))
    return ac, lo, hi, lb0, beyond, extra


def contact_area_check(ids, labels, radius, c1, c2, carea, delta, pflag):
    """item 2 (09-29 · 1저자 "권고대로") — **진단 기록** (거부 없음 · 피복률 값에 안 쓴다).

    덤프 면적 `c_cpl[22]` (피복률의 분자 · 분모에 들어가는 값) 이 두 반지름과 δ = `c_cpl[23]` 로 다시 잰 **정확한 교차 원판**
    (plastic_coverage 의 `_intersection_disc_area`) 과 토큰 반올림 안에서 같은가 — L1-04 의 "A_LIGG = 기하 교차 원판" 을 행마다
    확인한다.  허용폭 = `AREA_CHECK_TOL_RULE` (6 유효숫자 `%g` 토큰의 반올림 상자 위 포괄 구간 · LHSC-04 R2).  주기 플래그 `c_cpl[9]` 0/1 과 쌍 종류
    (AM-SE = 분자 · AM-AM = 분모 · SE-SE) 로 가른다.  고아 행 (id 가 원자 프레임에 없다) · 비유한 행은 비교에서 빼고 센다.
    δ 열이 없으면 대조하지 않고 `NO_DELTA_COLUMN` 으로 적는다.
    """
    n = int(len(c1))
    _pin = producer_pin()
    base = dict(role='진단 기록 — 거부하지 않는다 · 피복률 값에 쓰지 않는다 (item 2)',
                reference='lens_geometry.intersection_disc_area(r1, r2, delta = c_cpl[23]) — 두 구의 교차 원판 (L1-04 A_LIGG)',
                compared_to=COL_AREA, delta_col=COL_DELTA, flag_col=COL_PERIODIC,
                tolerance_rule=AREA_CHECK_TOL_RULE, sigfig_assumed=AREA_CHECK_SIGFIG, n_rows=n,
                producer_model=dict(PRODUCER_AREA_MODEL, installed_build_pinned=_pin['pinned'], pin=_pin['pin'],
                                    pin_reason=_pin['reason'], pin_file=_pin['file']))
    if delta is None:
        return dict(base, status='NO_DELTA_COLUMN')
    labs = np.asarray([str(q) for q in labels], dtype=object)
    pos = {int(a): k for k, a in enumerate(ids)}
    ka = np.asarray([pos.get(int(a), -1) for a in c1], dtype=np.int64)
    kb = np.asarray([pos.get(int(b), -1) for b in c2], dtype=np.int64)
    ok = (ka >= 0) & (kb >= 0)
    rad = np.asarray(radius, dtype=np.float64)
    r1 = np.where(ok, rad[np.maximum(ka, 0)], np.nan)
    r2 = np.where(ok, rad[np.maximum(kb, 0)], np.nan)
    dl, ad = np.asarray(delta, dtype=np.float64), np.asarray(carea, dtype=np.float64)
    fin = ok & np.isfinite(r1) & np.isfinite(r2) & np.isfinite(dl) & np.isfinite(ad)
    idx = np.flatnonzero(fin)
    ac, elo, ehi, lb0, beyond, xd = _contact_area_rows(r1[idx], r2[idx], dl[idx], ad[idx])
    A = ad[idx]
    diff = np.abs(A - ac)
    unc, neg, det = xd['uncertified'], xd['negative'], xd['detect_1pct']
    E = np.where(unc, 0.0, xd['producer_err'])
    tested = (~unc) & (~neg)
    #  LHSC-04 R2 · R3: 범위로 빼는 행은 없다 — 인증 · 비음수 행을 전부 포괄 구간 + 생산자 오차 상한으로 **시험**하고, 미인증 (d ≤ 0 이 상자 안)
    #  · 음수 덤프 면적 · 하한 0 · 폭 넓음 · 검출 보증은 따로 센다 (A_dump 에 걸리지 않는 행 성질)
    gap = np.maximum.reduce([(elo - E) - (A + _half_unit(A)), (A - _half_unit(A)) - (ehi + E), np.zeros_like(A)])

    def _grp(m):
        k = int(m.sum())
        p = m & (A > 0)
        q = m & (elo > 0)
        c = m & (~unc) & (elo > 0)
        rel, wid = diff[p] / A[p], (ehi[q] - elo[q]) / elo[q]
        pb = E[c] / elo[c]
        bx = m & beyond & (A > 0)
        return dict(n_rows=k, n_tested=int((m & tested).sum()), n_area_dump_zero=int((m & (A == 0)).sum()),
                    n_beyond_tol=int((m & beyond).sum()),
                    n_producer_uncertified=int((m & unc).sum()), n_area_dump_negative=int((m & neg).sum()),
                    n_lower_bound_zero=int((m & xd['lo_zero']).sum()), n_boundary_branch=int((m & (xd['how'] == 'boundary')).sum()),
                    n_wide_enclosure=int((m & xd['wide']).sum()), n_detect_1pct=int((m & det).sum()),
                    rel_diff_max=(float(rel.max()) if rel.size else None),
                    rel_diff_median=(float(np.median(rel)) if rel.size else None),
                    enclosure_rel_width_median=(float(np.median(wid)) if wid.size else None),
                    producer_bound_rel_median=(float(np.median(pb)) if pb.size else None),
                    producer_bound_rel_max=(float(pb.max()) if pb.size else None),
                    excess_rel_max=(float((gap[bx] / A[bx]).max()) if bx.any() else None))

    every = np.ones(idx.size, dtype=bool)
    if pflag is None:
        by_flag = {'no_flag_column': _grp(every)}
    else:
        pf = np.asarray(pflag, dtype=np.float64)[idx]
        by_flag = {'0': _grp(pf == 0.0), '1': _grp(pf == 1.0)}
        oth = ~((pf == 0.0) | (pf == 1.0))
        if oth.any():
            by_flag['other'] = _grp(oth)
    kind = np.asarray(['-'.join(sorted(('AM' if labs[i] in AM_LABELS else str(labs[i]),
                                        'AM' if labs[j] in AM_LABELS else str(labs[j]))))
                       for i, j in zip(ka[idx].tolist(), kb[idx].tolist())], dtype=object)
    by_kind = {kd: _grp(kind == kd) for kd in sorted(set(kind.tolist()))}
    return dict(base, status=(STATUS_OK if idx.size else 'NO_COMPARABLE_ROWS'), n_compared=int(idx.size),
                n_orphan_rows_skipped=int((~ok).sum()), n_nonfinite_skipped=int((ok & ~fin).sum()),
                n_values_beyond_6sig=dict(area=_n_beyond_sig(A), delta=_n_beyond_sig(dl[idx]), radius=_n_beyond_sig(rad)),
                all=_grp(every), by_periodic_flag=by_flag, by_pair_kind=by_kind)


def _plastic_coverage_uses(src):
    """소스 **전체** AST 에서 plastic_coverage 를 쓰는 곳 — (가져온 이름 집합, 위반 목록).  DESC-03 · 계약④ 의 selftest ⑬ · ㉑′ 가드.

    위반 = `PLASTIC_COVERAGE_ALLOWED` (09-30 부터 비어 있다) 밖 이름 · `*` · 모듈째 import (`import plastic_coverage` · 점 경로) ·
    **패키지 경유** (`from scripts import plastic_coverage as pc` — ImportFrom 의 이름 쪽) · 동적 import (`import_module` / `__import__`
    와 그 **별칭** — `from importlib import import_module as im` · `import importlib as il` 을 1 패스에서 모아 둔다; 인자가 문자열
    상수가 아니면 무엇을 가져오는지 검증할 수 없어 위반).  ★ Codex `LHSC-05` (09-30): 옛 판은 패키지 경유 (module == 'scripts') 와
    별칭 호출 (`im(...)`) 을 통과시켰다.  ⚠ 이것은 **lint** 이지 임의 Python 실행의 안전 증명이 아니다 (getattr · exec · 문자열 조립은
    못 본다) — 그래서 계약 (a) 로 의존 자체를 없앴다 (순수 기하 = `lens_geometry`).
    item 2 전의 ⑬ 은 "머리 (첫 함수 독스트링 앞) 에 문자열 plastic_coverage 가 없다" 였다 — 머리 밖 (함수 안 지연 import) 을 못 봤고,
    순수 기하 함수 하나를 가져오는 것도 막았다.
    """
    import ast
    mod = 'plastic_coverage'
    names, bad = set(), []
    tree = ast.parse(src)
    dyn_names = {'import_module', '__import__'}          # 동적 import 를 부르는 이름 (별칭 포함)
    for node in ast.walk(tree):                            # 1 패스 — importlib 별칭 수집
        if isinstance(node, ast.ImportFrom) and (node.module or '') == 'importlib':
            for a in node.names:
                if a.name in ('import_module', '__import__'):
                    dyn_names.add(a.asname or a.name)
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if (node.module or '').split('.')[-1] == mod:
                for a in node.names:
                    names.add(a.name)
                    if a.name not in PLASTIC_COVERAGE_ALLOWED:
                        bad.append(f'from {node.module} import {a.name} (줄 {node.lineno})')
            else:
                for a in node.names:
                    if a.name == mod:
                        bad.append(f'from {node.module} import {mod} (줄 {node.lineno}) — 패키지 경유 모듈째 import')
        elif isinstance(node, ast.Import):
            for a in node.names:
                if a.name.split('.')[-1] == mod:
                    bad.append(f'import {a.name} (줄 {node.lineno}) — 모듈째 가져오면 Physics 경로가 열린다')
        elif isinstance(node, ast.Call):
            fn = node.func
            nm = (fn.attr if isinstance(fn, ast.Attribute) and fn.attr in ('import_module', '__import__')
                  else fn.id if isinstance(fn, ast.Name) and fn.id in dyn_names else None)
            if nm is not None:
                arg = node.args[0] if node.args else None
                if not (isinstance(arg, ast.Constant) and isinstance(arg.value, str)):
                    bad.append(f'{nm}(<상수 아님>) (줄 {node.lineno}) — 무엇을 가져오는지 검증할 수 없다')
                elif arg.value.split('.')[-1] == mod:
                    bad.append(f'{nm}({arg.value!r}) (줄 {node.lineno}) — 동적 import')
    return names, bad


PLATE_SPAN_TOL = 1e-7      # sim (= 0.1 nm 실물).  평판이면 꼭짓점 z 가 전부 같다 (실측: heckel 메시 6 꼭짓점 동일)


def plate_stl_info(path):
    """STL 꼭짓점 z 의 평균 · 폭 · 개수 — HND-06 (Codex 09-25): 평판인지 **검사**한다 (평균만 받지 않는다)."""
    zs = []
    with open(path, 'r', encoding='utf-8', errors='replace') as fh:
        for ln in fh:
            p = ln.split()
            if len(p) == 4 and p[0] == 'vertex':
                zs.append(float(p[3]))
    if not zs:
        raise BedRefusal(f'{path}: STL 에 vertex 가 없다')
    zmin, zmax = min(zs), max(zs)
    return dict(z_mean_sim=float(np.mean(zs)), z_min_sim=zmin, z_max_sim=zmax,
                span_sim=float(zmax - zmin), n_vertices=len(zs))


def plate_z_from_stl(path):
    """`parse_liggghts.parse_mesh_stl` 과 **같은 정의** — 전 꼭짓점 z 평균.  단 평판이 아니면 거부 (HND-06)."""
    info = plate_stl_info(path)
    if info['span_sim'] > PLATE_SPAN_TOL:
        raise BedRefusal(f'{path}: 플래튼 STL 이 평판이 아니다 — 꼭짓점 z 폭 {info["span_sim"]:.3g} > {PLATE_SPAN_TOL} '
                         f'(HND-06).  평균 {info["z_mean_sim"]:.6g} 을 높이로 받지 않는다')
    return info['z_mean_sim']


def phase_labels(types, n_types):
    """계약⑤ — 선언 밖 type 이 있으면 거부한다."""
    tmap = TYPE_MAP[n_types]
    seen = set(int(t) for t in np.unique(types))
    bad = sorted(seen - set(tmap))
    if bad:
        raise BedRefusal(f'선언(--n-types {n_types}) 밖 type {bad} 이 파일에 있다')
    return np.asarray([tmap[int(t)] for t in types], dtype=object), tmap


SIM_TO_UM = 1e3    # LHS · 생산 덱의 길이 스케일 ×1000: sim 0.001 = 실물 1 µm (`parse_liggghts` 의 scale=1000 과 같은 규약)
MEASUREMENT_PROTOCOL_ID = 'harvest_v2_20260925/spheresum_nominal_gap/wall_z0/exact_step_mesh'
Z_FLOOR = 0.0      # 바닥 벽 — LHS 덱 `wall/gran … zplane 0.0`.  웹앱 `dem_analysis_core.calc_porosity` 의 V_box = L²·plate_z 와 같은 규약


def check_deck_floor(path):
    """LHS-12 (판단 J14): 바닥 벽 위치를 **덱에서 직접** 읽는다 — 입자 깊이로 추정하지 않는다.

    `fix … wall/gran … primitive type N zplane Z` 를 찾아 가장 낮은 Z 가 `Z_FLOOR` 인지 본다.
    주석 (`#` 뒤) 은 버리고 `&` 로 이어진 줄은 붙여 읽는다.  Z 를 숫자로 못 읽거나 (변수 등) 바닥 벽이 없거나
    0 이 아니면 **거부**한다 — 못 읽은 값을 0 으로 치지 않는다.
    ⛔ J13 판은 이 확인을 입자 깊이 (z − r < −½·r_max) 로 대신했다 — 실제 130 에서 가장 큰 AM 과 바닥의 **깊은 겹침**
      (연속 분포) 을 문턱에서 잘라 58 건을 거부했다 (재수확 09-24).
    """
    if not path or not os.path.exists(path):
        raise BedRefusal(f'{path}: 덱이 없다 — 바닥 벽 위치를 확인할 수 없다 (LHS-12)')
    logical, buf = [], ''
    with open(path, encoding='utf-8', errors='replace') as fh:
        for raw in fh:
            s = raw.split('#', 1)[0].rstrip()
            if s.endswith('&'):
                buf += s[:-1] + ' '
                continue
            logical.append(buf + s)
            buf = ''
    if buf:
        logical.append(buf)
    #  ★ HND-02 (Codex 09-25): "발견한 모든 zplane 중 min" 은 활성 벽 증명이 아니다 — unfix · 재정의 · 부분 group 을
    #    전부 통과시켰다.  지원 문법을 **제한**한다: fix id 생명주기를 따라가고 (unfix → 삭제 · 같은 id 재정의 → 교체),
    #    group 은 `all` 이어야 하며, 벽 정의/삭제가 흐름 제어 (label · jump · if · next) **뒤**에 오거나 include · read_restart ·
    #    python 이 있으면 "검증 불가" 로 거부한다 — 그 밖의 동적 규약은 여기서 검증하지 않는다.
    active, seen, n_defs = {}, 0, 0
    flow_seen = False
    for ln in logical:
        tok = ln.split()
        if not tok:
            continue
        cmd = tok[0]
        if cmd in ('include', 'read_restart', 'read_data', 'python'):
            raise BedRefusal(f'{path}: `{cmd}` 가 있어 바닥 벽을 정적으로 검증할 수 없다 (HND-02 — 지원 밖 문법, 검증 불가)')
        if cmd in ('label', 'jump', 'if', 'next'):
            flow_seen = True
            continue
        if cmd == 'unfix' and len(tok) > 1:
            if tok[1] in active:
                if flow_seen:
                    raise BedRefusal(f'{path}: 바닥 벽 `{tok[1]}` 의 unfix 가 흐름 제어 뒤에 있다 — 활성 여부를 정적으로 알 수 없다 (HND-02)')
                active.pop(tok[1])
            continue
        if cmd != 'fix' or len(tok) < 3:
            continue
        fid, grp = tok[1], tok[2]
        if fid in active and not ('wall/gran' in tok and 'primitive' in tok and 'zplane' in tok):
            active.pop(fid)                      # 같은 id 를 다른 fix 로 재정의 → 벽은 사라진다
            continue
        if 'wall/gran' not in tok or 'primitive' not in tok or 'zplane' not in tok:
            continue
        if flow_seen:
            raise BedRefusal(f'{path}: 바닥 벽 `{fid}` 정의가 흐름 제어 (label/jump/if) 뒤에 있다 — 검증 불가 (HND-02)')
        if grp != 'all':
            raise BedRefusal(f'{path}: 바닥 벽 `{fid}` 의 group 이 `{grp}` 다 — 모든 상을 구속한다는 증거가 없다 (HND-02)')
        kz, kp = tok.index('zplane'), tok.index('primitive')
        zs = tok[kz + 1] if kz + 1 < len(tok) else ''
        try:
            z = float(zs)
        except ValueError:
            raise BedRefusal(f'{path}: 바닥 벽 zplane 값을 숫자로 못 읽는다 ({zs!r}) — 0 으로 치지 않는다 (LHS-12)')
        wt = tok[kp + 2] if kp + 2 < len(tok) and tok[kp + 1] == 'type' else ''
        active[fid] = dict(fix_id=fid, z=z, wall_type=int(wt) if wt.isdigit() else None, line=' '.join(tok))
        n_defs += 1
    if not active:
        raise BedRefusal(f'{path}: 활성 바닥 벽 (`wall/gran … primitive … zplane`, unfix 되지 않은 것) 이 없다 — '
                         f'벽 = {Z_FLOOR} 가정을 확인할 수 없다 (LHS-12 · HND-02)')
    walls = list(active.values())
    floor = min(walls, key=lambda w: w['z'])
    if floor['z'] != Z_FLOOR:
        raise BedRefusal(f'{path}: 활성 바닥 벽이 z = {floor["z"]} 다 — 웹앱 규약 (벽 = {Z_FLOOR}) 이 이 덱에 맞지 않는다 (LHS-12)')
    return dict(z=floor['z'], wall_type=floor['wall_type'], fix_id=floor['fix_id'],
                n_active_walls=len(walls), n_zplane_walls=n_defs, line=floor['line'],
                grammar='static: fix/unfix lifecycle · group=all · 흐름 제어 앞에서만 (HND-02)')


def _wall_dists(z, plate_z, z_floor=Z_FLOOR):
    """두 벽까지의 **부호 있는** 중심–면 거리 (상자 안쪽 +): (바닥 z − z_floor, 플래튼 plate_z − z).

    item 4 — `volumes_and_phi` (→ `_wall_side`) · `wall_touch_fractions` · 벽 분할 피복률이 **같은 식**으로 거리를 잰다 (식이 둘이면
    접선 근처에서 부동소수 반올림 경로가 갈려 같은 규칙도 다른 답을 낼 수 있다).
    """
    return z - z_floor, plate_z - z


def _wall_contact(r, dist):
    """`WALL_TOUCH_RULE` 의 **유일한 구현** — 한 벽에 대해 (depth, touch, center_out, fully_out, h).

    depth = r − dist (벽 밖 cap 깊이 · 자르지 않은 값) · touch ⟺ depth > 0 · center_out ⟺ dist < 0 · fully_out ⟺ dist < −r ·
    h = clip(depth, 0, 2r) (벽 밖 cap 높이).  dist = `_wall_dists` 의 부호 있는 거리.
    ★ item 4 판단 — 접선 (depth = 0, 구가 면에 한 점으로 닿음) 은 **안 닿음**이다:
      ① 이 규칙을 쓰는 양이 전부 h > 0 에서만 0 이 아니다 — 벽 밖 부피 π h²(3r − h)/3 (`wall_record`) · 벽이 가린 표면 2π r h
         (벽 제외 피복률).  접선을 닿음으로 세면 가린 것이 0 인 입자가 '닿음' 칸에 들어가 분할과 보정이 어긋난다.
      ② 09-24 · 09-25 커밋 수확 JSON 의 `wall_record.*.n_touch` · `n_touch_by_phase` 가 이미 이 규칙 (r − dist > 0) 의 값이다 —
         반대쪽 (<=) 을 고르면 커밋된 키의 뜻이 조용히 바뀐다.  `wall_touch` (옛 `<=`) 는 커밋된 산출물이 없다 (수확 v3 미실행).
    ⚠ 판정 경계에 허용오차는 없다 (덤프 6 유효숫자 반올림 폭 안의 '거의 접선' 은 어느 쪽으로도 갈릴 수 있다 — 세는 수의 뜻은
      "그 좌표에서 겹침 깊이가 양수" 까지다).
    """
    depth = r - dist
    return depth, depth > 0, dist < 0, dist < -r, np.clip(depth, 0.0, 2.0 * r)


def _wall_side(labels, r, z, dist, vsum):
    """벽 한쪽 (바닥 또는 플래튼) 의 기록.  dist = 중심에서 벽까지의 **부호 있는** 거리 (상자 안쪽이 +).

    HND-03 (Codex 09-25): 기하 깊이 (cap depth = r − dist) 와 솔버의 접촉 겹침 (r − |dist|) 은 중심이 평면을 넘으면
    갈린다 — z = −0.98r 이면 cap 깊이 1.98r 이지만 접촉 겹침은 0.02r.  둘 다 따로 적는다 (옛 `overlap_over_r` 는 오도).
    """
    #  item 4 — 깊이 · 닿음 · 중심 밖 · 통째로 밖 · cap 높이는 `_wall_contact` 하나에서 (옛 식과 같은 식 · 같은 값)
    depth, touch, center_out, fully_out, h = _wall_contact(r, dist)
    v_out = np.pi * h ** 2 * (3.0 * r - h) / 3.0                       # 구 cap 부피 π h²(3r − h)/3
    i = int(np.argmax(depth))
    deepest = None
    if depth[i] > 0:
        deepest = dict(phase=str(labels[i]), r_sim=float(r[i]), z_sim=float(z[i]),
                       depth_sim=float(depth[i]), outside_cap_depth_over_r=float(depth[i] / r[i]),
                       contact_overlap_over_r=float(max(0.0, r[i] - abs(dist[i])) / r[i]),
                       center_out=bool(center_out[i]))
    labs = sorted({str(l) for l in labels})
    return dict(n_touch=int(touch.sum()), n_center_out=int(center_out.sum()),
                n_fully_out=int(fully_out.sum()),
                n_center_out_by_phase={l: int(sum(1 for q in labels[center_out] if str(q) == l)) for l in labs
                                       if int(sum(1 for q in labels[center_out] if str(q) == l))},
                n_touch_by_phase={l: int(sum(1 for q in labels[touch] if str(q) == l)) for l in labs},
                v_out_by_phase={l: float(v_out[np.asarray([str(q) == l for q in labels])].sum()) for l in labs},
                v_out_sim=float(v_out.sum()), v_out_pct=100.0 * float(v_out.sum()) / vsum,
                deepest=deepest)


def wall_touch_fractions(labels, z, r, plate_z, z_floor=Z_FLOOR):
    """J20-a ⓓ (1저자 비준 09-28 밤) — 상별 바닥 벽 · 플래튼 **접촉 입자 비율** (0–1).

    CN (`dem_analysis_core.calc_se_se_cn` · `calc_am_isolation_risk` · `calc_am_am_cn`) 은 벽 · 플래튼 접촉을 세지 않고
    그 상 **전 입자**로 나눈다 ⇒ 벽에 닿은 입자는 그쪽 이웃이 없어 CN 이 낮다 (정의 주의이지 결함 아님).  이 비율이 그 몫을
    가르는 설명 변수다 — 벽 인접 입자를 뺀 CN 은 AM_P 가 두께 2–10 개인 얇은 침대에서 남는 입자가 거의 없어 택하지 않았다.
    규칙 `WALL_TOUCH_RULE`.  3 상 침대는 AM_P · AM_S 에 더해 합친 'AM' 도 낸다 (am_se_cn_mean 과 같은 모집단).
    상이 없으면 키가 없다 (= N/A · 0 이 아니다, DESC-05).
    ⚠ item 4 (09-29): 옛 판은 `z − r <= z_floor` · `z + r >= plate_z` (접선 = 닿음) 로 `_wall_side` 와 접선에서 갈렸다 — 이제
      같은 `_wall_contact` (접선 = 안 닿음).  바뀐 것은 **정확히 접선인 입자**뿐이다 (selftest ⑲).
    """
    labels = np.asarray([str(q) for q in labels], dtype=object)
    z, r = np.asarray(z, dtype=np.float64), np.asarray(r, dtype=np.float64)
    d_f, d_p = _wall_dists(z, float(plate_z), z_floor)
    fl, pl = _wall_contact(r, d_f)[1], _wall_contact(r, d_p)[1]        # item 4 — `_wall_side` 와 같은 함수
    groups = {ph: labels == ph for ph in sorted(set(labels))}
    if 'AM_P' in groups and 'AM_S' in groups:
        groups['AM'] = groups['AM_P'] | groups['AM_S']
    out = {}
    for ph, m in groups.items():
        k = int(m.sum())
        if k == 0:
            continue
        out[ph] = dict(n=k, n_floor=int(fl[m].sum()), n_plate=int(pl[m].sum()),
                       floor=float(fl[m].mean()), plate=float(pl[m].mean()), either=float((fl[m] | pl[m]).mean()))
    return out


def volumes_and_phi(atoms, labels, box_lo, box_hi, plate_z):
    """계약② — φ 는 **기하만**으로, τ·전도도 성공과 무관하게.

    ⛔ LHS-10 (2026-09-24): 옛 판은 분모 높이를 `plate_z − box_lo[2]` (덤프 상자 바닥) 로 쟀다.  덱 상자가 벽보다 10 µm 아래서
      시작해 (`region … -0.01 1.0`) 입자가 없는 층이 분모에 들어갔다 — φ 가 0.742–0.825 배, porosity 중앙 30.65 % (벽 기준 9.89 %).
      이제 **벽 (Z_FLOOR)** 에서 잰다 — 벽 위치는 덱에서 확인한다 (`check_deck_floor`).
    ★ LHS-12 (판단 J14, 비준 09-24): 벽 밖으로 나간 입자는 **거부하지 않는다**.  (가) 주 값은 웹앱 식 그대로
      (ΣV 전부 / L²·plate_z — 벽 밖 부피도 벽 안 빈틈을 메운 것으로 센다) 이고, 벽 밖 부피 · 입자 수 · 가장 깊은 입자와
      (나) 그 부피를 벽 안으로 되돌려 두께에 더한 값 (`wall_record.pushback`) 을 **기록**한다.
    """
    r = atoms['radius']
    z = atoms['z']
    v = (4.0 / 3.0) * np.pi * r ** 3
    lx = float(box_hi[0] - box_lo[0])
    ly = float(box_hi[1] - box_lo[1])
    zb = float((z - r).min())
    zt = float((z + r).max())
    h = float(plate_z - Z_FLOOR)
    if not (lx > 0 and ly > 0 and h > 0):
        raise BedRefusal(f'전극 부피가 양수가 아니다: lx={lx} ly={ly} H={h}')
    v_box = lx * ly * h
    vsum = float(v.sum())
    is_se = labels == 'SE'
    is_am = np.asarray([l in AM_LABELS for l in labels])
    phi_se = float(v[is_se].sum() / v_box)
    phi_am = float(v[is_am].sum() / v_box)
    eps = 100.0 * (1.0 - vsum / v_box)

    dist_f, dist_p = _wall_dists(z, plate_z)                           # item 4 — 같은 식 (z − Z_FLOOR · plate_z − z) 한 곳
    floor = _wall_side(labels, r, z, dist_f, vsum)
    plate = _wall_side(labels, r, z, dist_p, vsum)
    w_tot = floor['v_out_sim'] + plate['v_out_sim']
    h_pb = h + w_tot / (lx * ly)
    v_box_pb = lx * ly * h_pb
    w_se = floor['v_out_by_phase'].get('SE', 0.0) + plate['v_out_by_phase'].get('SE', 0.0)
    w_am = sum(floor['v_out_by_phase'].get(k, 0.0) + plate['v_out_by_phase'].get(k, 0.0) for k in AM_LABELS)
    n_co = floor['n_center_out'] + plate['n_center_out']
    n_fo = floor['n_fully_out'] + plate['n_fully_out']
    codes = []
    if n_co:
        codes.append('BOUNDARY_CENTER_OUT')       # HND-03: 중심이 평면을 넘은 입자 — 정상 압입과 구분 · 물리 타깃 보류
    if eps < 0:
        codes.append('NEGATIVE_POROSITY')         # HND-04 · LHS-15: φ 합 > 1 — 값은 그대로 내고 물리 타깃은 보류
    wall_record = dict(
        floor=floor, plate=plate,
        pushback=dict(H_sim=h_pb, dH_sim=h_pb - h, V_box_sim=v_box_pb,
                      phi_se=float(v[is_se].sum() / v_box_pb), phi_am=float(v[is_am].sum() / v_box_pb),
                      porosity_pct_RECORD_ONLY=100.0 * (1.0 - vsum / v_box_pb)),
        clipped=dict(W_sim=w_tot, W_se_sim=w_se, W_am_sim=w_am,
                     phi_se=float((v[is_se].sum() - w_se) / v_box), phi_am=float((v[is_am].sum() - w_am) / v_box),
                     porosity_pct_RECORD_ONLY=100.0 * (1.0 - (vsum - w_tot) / v_box)),
        convention='(가) 주 값 = 웹앱 ε_sphere = **명목 구 부피 / 틀 간격 부피** (ΣV 전부 / L²·plate_z, 장부값 — 틀 안 점유율이 아니다) · '
                   '(나) pushback = 벽 밖 부피를 두께에 더한 등가 산술값 (hard-bottom 예측 아님, HND-01) · '
                   '(다) clipped = 벽 밖 cap 을 뺀 ROI 값 (아직 합집합 점유율 아님) — 판단 J14 · J18')
    boundary = dict(calculation_status='OK',
                    n_center_out=n_co, n_fully_out=n_fo,
                    boundary_state=('FULLY_OUT' if n_fo else 'CENTER_CROSSED' if n_co else 'INSIDE'),
                    phi_sum_gt_one=bool(phi_se + phi_am > 1.0),
                    hold_reason_codes=codes,
                    physical_target_status=('HOLD' if codes else 'OK'))
    return dict(phi_se=phi_se, phi_am=phi_am,
                porosity_sphere_pct_RECORD_ONLY=eps,
                V_box_sim=v_box, H_sim=h, lx_sim=lx, ly_sim=ly, z_floor_sim=Z_FLOOR,
                solid_bot_sim=zb, solid_top_sim=zt, wall_record=wall_record, boundary=boundary,
                closure_residual=phi_se + phi_am + eps / 100.0 - 1.0)


#: item 1 (09-29 · 1저자 "권고대로") — 벽이 가린 AM 표면을 분모에서 뺀 피복률 (**새 키만** · 오늘 식 `coverage_*_hertz_pct` 는 그대로).
WALLEXCL_FORMULA = ('c_i = min(100, 100 · ΣA22(AM–SE) / (4πr² − ΣA22(AM–AM) − Σ_{바닥, 플래튼} 2πr·clip(r − dist, 0, 2r))) · '
                    'dist = 중심–면 부호 거리 (상자 안 +) · 벽이 가린 표면 = 벽 밖 구면 cap 넓이 2πrh (h = cap 높이) · '
                    '분모 ≤ 0 → 제외하고 셈 · 상 = 유효 입자 평균 · 전체 = 유효 입자수 가중 (오늘 식과 같은 규칙) · '
                    '분자 = 원 AM–SE 합 그대로 (벽 자체 접촉을 더하지 않을 뿐 ROI 밖 원판을 잘라내지 않는다) = 분모 보정 proxy (LHSC-06)')
#: item 1 — 벽 분할 등급 (한 벽 기준 · `_wall_contact`): interior = 안 닿음 · touch = 닿음 (중심은 안) · center_out = 중심이 벽 밖
#:   (구는 걸침) · fully_out = 통째로 벽 밖.  'any' = 두 벽 중 더 심한 쪽 (interior = 어느 벽에도 안 닿음).
WALL_CLASSES = ('interior', 'touch', 'center_out', 'fully_out')


def _coverage_sums(ids, labels, radius, c1, c2, carea):
    """피복률의 접촉 합 — (free = 4πr² − Σ(AM–AM 면적), am_se = Σ(AM–SE 면적), 건너뛴 고아 행 수 (한쪽 id 가 원자 프레임에 없다)).

    item 1 — `coverage_hertz` (오늘 식) 와 `coverage_wall` (벽 분할 · 벽 제외) 이 **이 루프 하나**를 쓴다 (행 순서 · 합 순서가
    같아 부동소수 값까지 같다).  루프 본문은 옛 `coverage_hertz` 그대로 옮겼다.
    """
    pos = {int(a): k for k, a in enumerate(ids)}
    n = len(ids)
    free = 4.0 * np.pi * radius ** 2
    am_se = np.zeros(n)
    n_orphan = 0
    for a, b, ar in zip(c1, c2, carea):
        ka, kb = pos.get(int(a)), pos.get(int(b))
        if ka is None or kb is None:
            n_orphan += 1
            continue
        la, lb = labels[ka], labels[kb]
        a_am, b_am = la in AM_LABELS, lb in AM_LABELS
        if a_am and b_am:
            free[ka] -= ar
            free[kb] -= ar
        elif a_am and lb == 'SE':
            am_se[ka] += ar
        elif b_am and la == 'SE':
            am_se[kb] += ar
    return free, am_se, n_orphan


def coverage_hertz(ids, labels, radius, c1, c2, carea):
    """계약① — Hertz 피복률.  단위는 면적/면적이라 **scale 에 불변**이다.

    (item 1 — 합은 `_coverage_sums`, 요약은 `_coverage_from_sums` 로 나눴다: 벽 분할이 같은 합 · 같은 요약 규칙을 쓰게.
     값은 그대로 — selftest ⑳ 의 변경 전 황금 해시.)
    (item 3 — 건너뛴 고아 행 수를 `n_orphan_rows` 로 돌려준다 (새 키만 · 조용히 버리지 않는다).  중복 · 자기쌍 거부는 `harvest` 의
     `contact_gate` 가 한다 — 이 함수를 직접 부르는 쪽은 그 문을 따로 거쳐야 한다.)
    """
    free, am_se, n_orphan = _coverage_sums(ids, labels, radius, c1, c2, carea)
    res = _coverage_from_sums(labels, am_se, free)[0]
    res['n_orphan_rows'] = n_orphan
    return res


def _coverage_from_sums(labels, am_se, free):
    """입자별 c_i → 상 평균 · 전체 — 옛 `coverage_hertz` 의 요약 규칙 그대로.  (요약 dict, 입자별 c_i (AM 아님 · 분모 ≤ 0 → NaN))."""
    n = len(labels)
    out, n_cap, n_bad = {}, 0, 0
    per = np.full(n, np.nan)
    for k in range(n):
        if labels[k] not in AM_LABELS:
            continue
        if free[k] <= 0:
            n_bad += 1
            continue
        c = 100.0 * am_se[k] / free[k]
        if c > 100.0:
            c, n_cap = 100.0, n_cap + 1
        per[k] = c

    counts = {}
    for lab in ('AM_P', 'AM_S', 'AM'):
        sel = np.asarray([l == lab for l in labels])
        n_exist = int(sel.sum())
        vals = per[sel & ~np.isnan(per)]
        counts[lab] = dict(n_particles=n_exist, n_valid=int(vals.size))
        if n_exist == 0:
            out[lab] = (None, STATUS_ABSENT)
        elif vals.size == 0:
            out[lab] = (None, 'FREE_SURFACE_INVALID')
        else:
            out[lab] = (float(vals.mean()), STATUS_OK)

    #  ★ 전체 = **실측 입자수 가중** (상 평균의 평균도, 총면적비도, 질량가중도 아니다).
    num = den = 0.0
    for lab in ('AM_P', 'AM_S', 'AM'):
        val, st = out[lab]
        if st == STATUS_OK:
            w = counts[lab]['n_valid']
            num += w * val
            den += w
    total = (float(num / den), STATUS_OK) if den > 0 else (None, 'FREE_SURFACE_INVALID')
    return dict(per_phase=out, total=total, counts=counts,
                n_capped=n_cap, n_free_surface_invalid=n_bad), per


def coverage_wall(ids, labels, radius, z, c1, c2, carea, plate_z, z_floor=Z_FLOOR):
    """item 1 (09-29 · 1저자 "권고대로") — ① **벽 분할**: AM 입자를 바닥 · 플래튼 기준 `WALL_CLASSES` 로 가르고 등급마다 수 ·
    오늘 식 평균 · 벽 제외 평균 · 가린 면 비율 ② **벽 제외 피복률**: 분모에서 벽이 가린 구면 cap 2πrh 도 뺀다 (`WALLEXCL_FORMULA`).
    등급 · h 는 `_wall_contact` (item 4 의 규칙 하나 — `wall_record` · `wall_touch` 와 같은 함수).

    ★ 왜: 오늘 식 분모 4πr² − ΣA(AM–AM) 는 바닥 (z = 0) 밑 · 플래튼 위로 나간 AM 표면도 '덮이지 않은 자유 표면' 으로 센다.  벽 접촉은
      덤프 (pair/gran/local) 에 없어서 그 몫의 크기가 재어진 적이 없다 — 분할이 그 크기 (벽 등급별 평균 차) 를 잰다.
    ⚠ 근사 (오늘 식과 같은 층위 · 교차는 계산하지 않는다): 분모에서 빼는 AM–AM 원판과 cap 곡면이 겹칠 수 있다 (벽 밖에서 난 AM–AM
      접촉이면 두 번 뺀다) · 분자 AM–SE 원판이 cap 안에 있을 수 있다 (벽 밖에 매달린 SE — HND-03).
    ⚠ 두 벽은 뜻이 다르다 (`LHS-14`): 플래튼 = SUS 플런저 (AM 물성) — 가린 면은 SE 가 못 닿는 면이다.  바닥 = SE 물성 평면 = 분리막 SE
      의 proxy — 바닥이 가린 면은 표현하려는 전지에서는 '분리막 SE 에 눌린 면' 이다.  이 열은 **분모 보정 proxy** 다 (★ 정정 09-30 ·
      Codex `LHSC-06`): 분모에서만 벽 cap 을 빼고, 분자는 원 AM–SE 면적합 **그대로**다 — 벽 자체 접촉을 분자에 더하지 않는다는 뜻이지
      ROI 밖 AM–SE 원판을 잘라낸다는 뜻이 아니다 (Codex 반례: 바닥 아래 SE 와의 접촉 원판이 전부 ROI 밖인데 31.6 % · OK 로 남는다).
      옛 문구 "분자 · 분모 모두에서 뺀 값 (= 전극 안 SE 입자가 덮은 몫)" 은 부정확했다 — '벽 안 SE 가 덮은 순수 면적' 으로 읽지 말 것.
      그 면을 덮인 것으로 세는 읽기는 내지 않는다 (벽 접촉 면적이 덤프에 없고 h 는 연화된 바닥 강성이 정한다).  분모 ≤ 0 인 입자를
      뺀 유효 입자 평균이라 편향 방향은 정해져 있지 않다 (`OK` = 남은 유효 입자의 계산 상태 · 물리 적격성 아님).  두 표의
      `mean_wallexcl_pct` 는 각각 한 벽만 교정한 값이 아니라 **두 벽을 다 뺀** 같은 입자값을 등급별로 다르게 모은 평균이다.
      그래서 분할은 바닥 · 플래튼을 **따로** 낸다.
    반환: dict(wallexcl = `_coverage_from_sums` 요약 (분모 = 벽 제외), split = 벽 분할 (JSON 용), n_orphan_rows).
    """
    radius = np.asarray(radius, dtype=np.float64)
    free, am_se, n_orphan = _coverage_sums(ids, labels, radius, c1, c2, carea)
    _today, per0 = _coverage_from_sums(labels, am_se, free)                  # 오늘 식 입자값 (coverage_hertz 와 같은 값)
    d_f, d_p = _wall_dists(np.asarray(z, dtype=np.float64), float(plate_z), z_floor)
    cf, cp = _wall_contact(radius, d_f), _wall_contact(radius, d_p)
    s_f, s_p = 2.0 * np.pi * radius * cf[4], 2.0 * np.pi * radius * cp[4]  # 벽이 가린 구면 cap 넓이 2πrh
    wx, perw = _coverage_from_sums(labels, am_se, free - s_f - s_p)
    sphere = 4.0 * np.pi * radius ** 2

    def _sev(c):                                                             # 0 interior · 1 touch · 2 center_out · 3 fully_out
        return np.where(c[3], 3, np.where(c[2], 2, np.where(c[1], 1, 0)))

    sev_f, sev_p = _sev(cf), _sev(cp)
    sev_any = np.maximum(sev_f, sev_p)
    labs = np.asarray([str(q) for q in labels], dtype=object)
    groups = {ph: labs == ph for ph in ('AM_P', 'AM_S', 'AM') if bool((labs == ph).any())}   # 없는 상 = 키 없음 (N/A)
    is_am = np.asarray([q in AM_LABELS for q in labs], dtype=bool)
    if is_am.any():
        groups['total'] = is_am                                              # 전 AM = 상 평균의 유효 입자수 가중과 같다
    by_phase = {}
    for ph, m in groups.items():
        by_phase[ph] = {}
        for wall, sev, blk in (('any', sev_any, s_f + s_p), ('floor', sev_f, s_f), ('plate', sev_p, s_p)):
            row = {}
            for ci, cname in enumerate(WALL_CLASSES):
                sel = m & (sev == ci)
                v0, v1 = per0[sel], perw[sel]
                v0, v1 = v0[~np.isnan(v0)], v1[~np.isnan(v1)]
                row[cname] = dict(n=int(sel.sum()), n_valid=int(v0.size),
                                  mean_pct=(float(v0.mean()) if v0.size else None),
                                  n_valid_wallexcl=int(v1.size),
                                  mean_wallexcl_pct=(float(v1.mean()) if v1.size else None),
                                  blocked_frac_mean=(float((blk[sel] / sphere[sel]).mean()) if sel.any() else None))
            by_phase[ph][wall] = row
    split = dict(
        rule=WALL_TOUCH_RULE, classes=list(WALL_CLASSES),
        class_rule=('벽마다 dist = 중심–면 부호 거리 (안 +): fully_out = dist < −r · center_out = −r ≤ dist < 0 · '
                    'touch = dist ≥ 0 이고 r − dist > 0 · interior = r − dist ≤ 0 (접선 포함) · any = 바닥 · 플래튼 중 심한 쪽'),
        fields=('n = 입자 수 · n_valid / mean_pct = 오늘 식 (분모 4πr² − ΣA(AM–AM)) 의 유효 입자 수 · 평균 · '
                'n_valid_wallexcl / mean_wallexcl_pct = 벽 제외 (두 벽 cap 을 다 뺀 입자값 — floor · plate 분할도 같은 입자값을 묶는다) · '
                'blocked_frac_mean = 그 분할의 벽이 가린 면 / 4πr² 평균'),
        walls=dict(floor='SE 물성 평면 = 분리막 SE proxy (LHS-14) — 가린 면은 표현 전지에서 분리막에 눌린 면',
                   plate='SUS 플런저 (AM 물성 메시) — 가린 면은 SE 가 못 닿는 면'),
        z_floor_sim=float(z_floor), plate_z_sim=float(plate_z), by_phase=by_phase)
    return dict(wallexcl=wx, split=split, n_orphan_rows=n_orphan)


def _mi_dist(p, q, lx, ly):
    """xy **주기** · z 개방의 최소영상 거리.

    ⚠ `P1-HARV-01` (L4/L5 판정, 2026-09-13): 초판은 쌍 찾기만 주기로 하고 **간선 가중치와
    경로 길이는 raw 좌표차**로 계산했다.  그래서 **같은 침대를 평행이동만 해도** τ 가
    9.850888284819803 → 1.0198039027185568 (**9.6596배**) 로 바뀌었다.
    `_pairs_within` 이 minimum-image 로 이웃을 찾는 한, 길이도 같은 규약이어야 한다.
    """
    d = p - q
    d[0] -= lx * round(d[0] / lx)
    d[1] -= ly * round(d[1] / ly)
    return float(np.linalg.norm(d))


def tortuosity_se(atoms, labels, box_lo, box_hi, n_pairs=N_TAU_PAIRS, seed=42,
                  plate_z=None):
    """계약③ — fallback source 승격 **없음**, 쌍은 **같은 성분 안에서만**.

    ★ `LHS-08` (2026-09-19): 초판은 **두 개의 `return base`** 가 같은 `NOT_PERCOLATING`
    을 냈다 — ⓐ 전극 밴드에 SE 가 0 명이라 **볼 성분이 애초에 없던** 경우와 ⓑ 밴드는
    찼는데 어떤 성분도 두 밴드를 못 잇던 경우.  실물 130 중 **116** 이 그 값이었고
    산출물만으로는 어느 쪽인지 알 수 없었다 ⇒ *"우리 코드 문제냐"* 에 답할 수가 없었다.
    ⓐ 는 규약(밴드 정의)을 겨누고 ⓑ 는 물리를 겨누는데 **처방이 정반대**다.
    ⇒ ⓐ = `ELECTRODE_BAND_EMPTY`, ⓑ = `NOT_PERCOLATING`, 그리고 두 경우 모두
    `band_detail` 에 **왜 그랬는지 세는 수**를 남긴다.

    ⚠ `plate_z` 는 **진단 전용**이다.  보고되는 τ 도 `tau_convention` 도 `solid_zrange`
    규약 **그대로**다 (selftest ⑭ 가 그것을 강제한다).  규약 판단은 재측정 **뒤**다 —
    LHS-08 처방 순서 = 진단 분리 → 재측정 → 규약 판단.  순서를 바꾸면 규약을 바꾼 뒤
    그 규약으로 잰 수로 규약을 정당화하게 된다.
    """
    import networkx as nx

    sel = np.flatnonzero(np.asarray([l == 'SE' for l in labels]))
    band = dict(
        n_se=int(sel.size), z_lo=None, z_hi=None, band_t=None,
        se_z_lo=None, se_z_hi=None, n_bot=0, n_top=0,
        n_components=0, n_span_components=0,
        largest_comp_frac=None, largest_comp_z_span_frac=None,
        alt_plate_z=(None if plate_z is None else float(plate_z)),
        alt_n_top=None, alt_plate_above_solid=None,
        alt_note=('진단 전용 (LHS-08) — 위 전극면을 plate_z 로 뒀을 때의 밴드 인원. '
                  '보고 τ 는 solid_zrange 규약 그대로이며 이 수는 τ 에 안 들어간다.'))
    base = dict(tau_mean=None, tau_median=None, tau_mean_untruncated=None,
                n_sampled=0, n_valid=0, n_truncated=0, status=STATUS_NOPERC,
                tau_convention='harvest_v1/solid_zrange/rSEmax/no_fallback/same_component',
                band_detail=band)
    #  벽 τ 의 기본값 — plate_z 가 없으면 **추정하지 않는다** (DESC-06 과 같은 원칙)
    base['wall_tau'] = dict(tau_mean=None, tau_median=None, tau_mean_untruncated=None,
                            n_sampled=0, n_valid=0, n_truncated=0, n_span_components=None,
                            status=(STATUS_NO_PLATE if plate_z is None else STATUS_NOPERC),
                            tau_convention=TAU_WALL_CONVENTION)
    if sel.size < 2:
        base['status'] = STATUS_ABSENT
        if plate_z is not None:
            base['wall_tau']['status'] = STATUS_ABSENT
        return base

    r_all, z_all = atoms['radius'], atoms['z']
    z_lo = float((z_all - r_all).min())
    z_hi = float((z_all + r_all).max())
    xyz = np.column_stack([atoms['x'][sel], atoms['y'][sel], atoms['z'][sel]])
    rad = r_all[sel]
    t = float(rad.max())
    lx = float(box_hi[0] - box_lo[0])
    ly = float(box_hi[1] - box_lo[1])
    band.update(z_lo=z_lo, z_hi=z_hi, band_t=t,
                se_z_lo=float((xyz[:, 2] - rad).min()),
                se_z_hi=float((xyz[:, 2] + rad).max()))

    pairs = _pairs_within(xyz, rad, lx, ly, z_pad=t)
    G = nx.Graph()
    G.add_nodes_from(range(sel.size))
    for i, j in pairs:
        d = _mi_dist(xyz[i].copy(), xyz[j].copy(), lx, ly)   # ★ P1-HARV-01
        G.add_edge(int(i), int(j), distance=d)

    #  ★ LHS-08: 성분 통계를 **밴드 검사 전에** 낸다 — ⓐ 로 빠져도 "SE 가 한 덩어리였나
    #  산산조각이었나" 를 알아야 밴드 정의가 용의자인지 판별된다.
    comps = list(nx.connected_components(G))
    band['n_components'] = int(len(comps))
    if comps:
        big = max(comps, key=len)
        bi = np.fromiter(big, dtype=np.int64, count=len(big))
        band['largest_comp_frac'] = float(len(big) / sel.size)
        _span = float((xyz[bi, 2] + rad[bi]).max() - (xyz[bi, 2] - rad[bi]).min())
        band['largest_comp_z_span_frac'] = (
            float(_span / (z_hi - z_lo)) if z_hi > z_lo else None)

    bot = set(np.flatnonzero((xyz[:, 2] - rad) <= z_lo + t).tolist())
    top = set(np.flatnonzero((xyz[:, 2] + rad) >= z_hi - t).tolist())
    band.update(n_bot=int(len(bot)), n_top=int(len(top)))
    if plate_z is not None:                    # ⚠ 진단만 — τ 에 안 들어간다
        band['alt_n_top'] = int(np.count_nonzero(
            (xyz[:, 2] + rad) >= float(plate_z) - t))
        band['alt_plate_above_solid'] = bool(float(plate_z) >= z_hi)
    #  ★ 벽 기준 밴드 진단 (Codex §8-3 · 판단 J18 C): solid 아래 밴드는 min(z − r) 가 정하는데 벽 아래로 샌 입자가 그것을
    #    끌어내려 SE 가 비는 일이 130 중 110 건 — 바닥 (Z_FLOOR) · 플래튼 (plate_z) 기준 인원과 그 둘을 잇는 성분 수를 적는다.
    #    보고 τ · tau_convention 은 solid_zrange 규약 **그대로** (LHS-08 규약 판단은 재측정 뒤).
    wall_bot = set(np.flatnonzero((xyz[:, 2] - rad) <= Z_FLOOR + t).tolist())
    band['wall_z_floor'] = Z_FLOOR
    band['wall_n_bot'] = int(len(wall_bot))
    if plate_z is not None:
        wall_top = set(np.flatnonzero((xyz[:, 2] + rad) >= float(plate_z) - t).tolist())
        band['wall_n_top'] = int(len(wall_top))
        band['wall_n_span_components'] = int(sum(1 for comp in comps if (comp & wall_bot) and (comp & wall_top)))
    else:
        band['wall_n_top'] = None
        band['wall_n_span_components'] = None
    band['wall_note'] = '진단 전용 — 벽 (z = Z_FLOOR) · 플래튼 기준 밴드 인원 (Codex §8-3).  보고 τ 는 solid_zrange 규약 그대로.'
    #  ★ 벽 기준 τ — **새 열** (1저자 비준 09-28 "벽 기준 τ 새 열", 판단 J20).  같은 성분 그래프 · 같은 표본 규칙 · 같은 seed,
    #    밴드만 벽 (바닥 z = Z_FLOOR · 플래튼 plate_z) 이다.  옛 τ (아래) 는 그대로 — 규약 판단은 새 이름으로 드러낸다.
    if plate_z is not None:
        wt = _tau_sample(G, xyz, comps, wall_bot, wall_top, lx, ly, n_pairs, seed)
        wt['tau_convention'] = TAU_WALL_CONVENTION
        base['wall_tau'] = wt
    if not bot or not top:
        base['status'] = STATUS_BAND_EMPTY      # ⓐ — 규약(밴드 정의)이 용의자
        return base

    res = _tau_sample(G, xyz, comps, bot, top, lx, ly, n_pairs, seed)
    band['n_span_components'] = res.pop('n_span_components')
    base.update(res)                            # ⓑ (관통 성분 0) 이면 NOT_PERCOLATING · 유한 τ 없음 — 물리
    return base


def _tau_sample(G, xyz, comps, bot, top, lx, ly, n_pairs, seed):
    """두 밴드 (`bot` · `top`, SE 색인 집합) 를 **같은 성분 안에서** 잇는 쌍으로 τ 를 표본한다.

    옛 규약 (solid_zrange) 과 벽 규약 (wall_z0_plate) 이 **이 함수 하나**를 쓴다 — 밴드만 다르고 규칙은 같다
    (selftest ⑰: 두 밴드가 같은 침대에서 두 τ 가 같다 · 옛 τ 는 옮기기 전 값 그대로).
    """
    import networkx as nx

    out = dict(tau_mean=None, tau_median=None, tau_mean_untruncated=None,
               n_sampled=0, n_valid=0, n_truncated=0, status=STATUS_NOPERC, n_span_components=0)
    if not bot or not top:
        out['status'] = STATUS_BAND_EMPTY
        return out
    cands = []
    for comp in comps:
        cb, ct = comp & bot, comp & top
        if cb and ct:
            cands.append((sorted(cb), sorted(ct)))
    out['n_span_components'] = int(len(cands))
    if not cands:                                   # ⓑ — 유한 τ 를 내지 않는다 (물리)
        return out

    rng = np.random.default_rng(seed)
    allp = [(s, tt) for cb, ct in cands for s in cb for tt in ct if s != tt]
    if not allp:
        out['status'] = STATUS_NOPAIR
        return out
    idx = rng.permutation(len(allp))[:n_pairs]
    taus = []
    for k in idx:
        s, tt = allp[int(k)]
        try:
            path = nx.shortest_path(G, s, tt, weight='distance')
        except nx.NetworkXNoPath:                   # 같은 성분이라 원래 안 난다
            continue
        plen = sum(_mi_dist(xyz[path[m]].copy(), xyz[path[m + 1]].copy(), lx, ly)
                   for m in range(len(path) - 1))              # ★ P1-HARV-01
        dz = abs(float(xyz[tt, 2] - xyz[s, 2]))
        if dz > 0:
            taus.append(plen / dz)

    if not taus:
        out['status'] = STATUS_NOPAIR
        out['n_sampled'] = int(len(idx))
        return out
    raw = np.asarray(taus)
    keep = raw[(raw >= TAU_LO) & (raw < TAU_HI)]
    out.update(n_sampled=int(len(idx)), n_valid=int(raw.size),
               n_truncated=int(raw.size - keep.size),
               tau_mean_untruncated=float(raw.mean()))
    if keep.size == 0:
        out['status'] = STATUS_NOPAIR
        return out
    out.update(tau_mean=float(keep.mean()), tau_median=float(np.median(keep)),
               status=STATUS_OK)
    return out


def harvest(atom_path, contact_path, n_types, case, plate_z=None, mesh_path=None,
            allow_any_bc=False, n_pairs=N_TAU_PAIRS, deck_path=None):
    for p in (atom_path, contact_path):
        if not os.path.exists(p):
            raise BedRefusal(f'{p}: 없다')
    #  LHS-12: 바닥 벽 위치를 덱에서 확인한다 (CLI 는 --deck 필수 · 라이브러리 호출은 None 이면 '미확인' 으로 남긴다)
    deck = check_deck_floor(deck_path) if deck_path is not None else None
    ts_a, ts_c = last_timestep(atom_path), last_timestep(contact_path)
    if ts_a != ts_c:
        raise BedRefusal(
            f'TIMESTEP 불일치: atom={ts_a} contact={ts_c}.  '
            '종류별 최신 파일을 독립 선택하면 다른 프레임이 섞인다 (DESC-06)')

    atoms, box_lo, box_hi, bc = read_atom_dump(atom_path)
    bc_note = check_boundary_flags(bc, allow_any_bc)
    if 'id' not in atoms:
        pass
    labels, tmap = phase_labels(atoms['type'], n_types)

    if (plate_z is None) == (mesh_path is None):
        raise BedRefusal('플래튼 높이는 --mesh 또는 --plate-z 로 **정확히 하나** 주어야 한다.  '
                         '추정하지 않는다 (DESC-06: 최고 입자 중심 추정은 5.263 % 상대차)')
    if mesh_path is not None:
        if not os.path.exists(mesh_path):
            raise BedRefusal(f'{mesh_path}: 없다')
        plate_z = plate_z_from_stl(mesh_path)
        h_src = 'mesh_stl'
    else:
        h_src = 'cli_explicit'

    phi = volumes_and_phi(atoms, labels, box_lo, box_hi, plate_z)

    ids = _atom_ids(atom_path)
    #  item 2 — δ · 주기 플래그 열도 같은 마지막 블록에서 (앞 넷은 extra_cols 없이 읽은 것과 같은 배열)
    c1, c2, carea, cheaders, cextra = read_contact_dump(contact_path, extra_cols=(COL_DELTA, COL_PERIODIC))
    #  item 3 — 문: 중복 무순서 쌍 · 자기쌍이면 **여기서 거부** (피복률 · 면적 대조 전 · 숫자를 내지 않는다) · 고아 행은 센다
    gate = contact_gate(ids, c1, c2)
    #  J20-a — 새 키만 더한다 (옛 키 · status 는 그대로: run_lhs_fill_wsl.sh [2] 의 옛 수확 대조가 선다)
    wall_touch = wall_touch_fractions(labels, atoms['z'], atoms['radius'], plate_z)
    contact_scan = scan_contact_dump(contact_path)
    n_atom_frames = count_blocks(atom_path, 'ITEM: TIMESTEP')
    cov = coverage_hertz(ids, labels, atoms['radius'], c1, c2, carea)
    #  item 1 — 벽 분할 · 벽 제외 피복률 (새 키만) · 같은 접촉 합 · 같은 벽 규칙 (`_wall_contact`)
    covw = coverage_wall(ids, labels, atoms['radius'], atoms['z'], c1, c2, carea, plate_z)
    #  item 2 — 접촉 면적 대조 (진단 기록 · 거부 없음 · 피복률 값 불변)
    area_check = contact_area_check(ids, labels, atoms['radius'], c1, c2, carea,
                                    cextra[COL_DELTA], cextra[COL_PERIODIC])
    #  plate_z 는 **진단 전용**으로만 넘긴다 (LHS-08) — 보고 τ 의 규약은 안 바뀐다.
    tau = tortuosity_se(atoms, labels, box_lo, box_hi, n_pairs=n_pairs,
                        plate_z=plate_z)
    #  벽 τ 는 **따로** 싣는다 — 옛 `tau_detail` 은 키 하나 늘지 않게 (09-25 산출물과 같은 모양) 둔다.
    tau_wall = tau.pop('wall_tau')

    raw = {'atom': dict(path=os.path.basename(atom_path), sha256=sha256_of(atom_path)),
           'contact': dict(path=os.path.basename(contact_path),
                           sha256=sha256_of(contact_path))}
    if mesh_path:
        raw['mesh'] = dict(path=os.path.basename(mesh_path), sha256=sha256_of(mesh_path))
    if deck_path is not None:
        raw['deck'] = dict(path=os.path.basename(deck_path), sha256=sha256_of(deck_path))

    cp, sp = cov['per_phase']['AM_P']
    cs, ss = cov['per_phase']['AM_S']
    ca, sa = cov['per_phase']['AM']
    ct, st = cov['total']
    if n_types == 2:                       # 2-type 침대는 AM 이 한 상이다
        cp, sp = None, STATUS_ABSENT
        cs, ss = None, STATUS_ABSENT
        ct, st = (ca, sa)
    wx = covw['wallexcl']                  # item 1 — 벽 제외 피복률 (위와 같은 상 규칙)
    xp, xps = wx['per_phase']['AM_P']
    xs, xss = wx['per_phase']['AM_S']
    xa, xas = wx['per_phase']['AM']
    xt, xts = wx['total']
    if n_types == 2:
        xp, xps = None, STATUS_ABSENT
        xs, xss = None, STATUS_ABSENT
        xt, xts = (xa, xas)

    wr, bd = phi['wall_record'], phi['boundary']
    fl, pl, pb, cl = wr['floor'], wr['plate'], wr['pushback'], wr['clipped']
    fd, pd_ = fl.get('deepest') or {}, pl.get('deepest') or {}
    v_full = {k: float(atoms['radius'][labels == k].__pow__(3).sum() * (4.0 / 3.0) * np.pi) for k in tmap.values()}
    handover_qc = dict(
        #  등록 alias 의 정본 의미 (HND-01) — 같은 값, 이름만 규약을 말한다
        phi_se_spheresum_nominal_gap=phi['phi_se'], phi_am_spheresum_nominal_gap=phi['phi_am'],
        porosity_spheresum_nominal_gap_pct=phi['porosity_sphere_pct_RECORD_ONLY'],
        #  두께 (µm) — 주 값은 같은 프레임의 플래튼 − 바닥 간격 (Q2 ACCEPT)
        thickness_wall_gap_um=phi['H_sim'] * SIM_TO_UM,
        thickness_pushback_equiv_um=pb['H_sim'] * SIM_TO_UM,
        thickness_envelope_um=(phi['solid_top_sim'] - phi['solid_bot_sim']) * SIM_TO_UM,
        solid_bottom_um=phi['solid_bot_sim'] * SIM_TO_UM, solid_top_um=phi['solid_top_sim'] * SIM_TO_UM,
        plate_minus_solid_top_um=(float(plate_z) - phi['solid_top_sim']) * SIM_TO_UM,
        #  보조 지표 — (나) 등가 산술값 · (다) ROI clipped
        porosity_pushback_equiv_pct=pb['porosity_pct_RECORD_ONLY'],
        phi_se_pushback_equiv=pb['phi_se'], phi_am_pushback_equiv=pb['phi_am'],
        phi_se_clipped_spheresum_gap=cl['phi_se'], phi_am_clipped_spheresum_gap=cl['phi_am'],
        porosity_clipped_spheresum_gap_pct=cl['porosity_pct_RECORD_ONLY'],
        #  부피 감사 (µm³) — 겹침 중복을 포함하는 구 합
        V_AM_full_um3=sum(v_full.get(k, 0.0) for k in AM_LABELS) * SIM_TO_UM ** 3,
        V_SE_full_um3=v_full.get('SE', 0.0) * SIM_TO_UM ** 3,
        V_AM_out_floor_um3=sum(fl['v_out_by_phase'].get(k, 0.0) for k in AM_LABELS) * SIM_TO_UM ** 3,
        V_AM_out_plate_um3=sum(pl['v_out_by_phase'].get(k, 0.0) for k in AM_LABELS) * SIM_TO_UM ** 3,
        V_SE_out_floor_um3=fl['v_out_by_phase'].get('SE', 0.0) * SIM_TO_UM ** 3,
        V_SE_out_plate_um3=pl['v_out_by_phase'].get('SE', 0.0) * SIM_TO_UM ** 3,
        #  경계 QC
        n_floor_center_out=fl['n_center_out'], n_floor_fully_out=fl['n_fully_out'],
        n_plate_center_out=pl['n_center_out'], n_plate_fully_out=pl['n_fully_out'],
        floor_out_pct=fl['v_out_pct'], plate_out_pct=pl['v_out_pct'],
        floor_outside_cap_depth_over_r_max=fd.get('outside_cap_depth_over_r'),
        floor_deepest_phase=fd.get('phase'), floor_deepest_r_um=(None if fd.get('r_sim') is None else fd['r_sim'] * SIM_TO_UM),
        floor_deepest_z_um=(None if fd.get('z_sim') is None else fd['z_sim'] * SIM_TO_UM),
        floor_deepest_contact_overlap_over_r=fd.get('contact_overlap_over_r'),
        plate_outside_cap_depth_over_r_max=pd_.get('outside_cap_depth_over_r'),
        boundary_state=bd['boundary_state'],
        #  적격성 — 계산 성공과 물리/ML 용도 허용을 분리 (HND-04)
        calculation_status=bd['calculation_status'], physical_target_status=bd['physical_target_status'],
        hold_reason_codes='|'.join(bd['hold_reason_codes']), phi_sum_gt_one=bd['phi_sum_gt_one'],
        #  프로비넌스
        measurement_protocol_id=MEASUREMENT_PROTOCOL_ID,
        boundary_model_id=(f"floor=primitive_zplane_type{deck['wall_type']}" if deck else 'floor=unverified')
                          + ('|platen=mesh_stl' if mesh_path else '|platen=cli_plate_z'),
        scale_sim_per_um=1.0 / SIM_TO_UM, deck_floor_z_sim=(None if deck is None else deck['z']),
        deck_wall_type=(None if deck is None else deck['wall_type']),
        atom_sha256=raw['atom']['sha256'], contact_sha256=raw['contact']['sha256'],
        deck_sha256=(raw.get('deck') or {}).get('sha256'), mesh_sha256=(raw.get('mesh') or {}).get('sha256'))

    return dict(
        case=case, timestep=ts_a, n_types=n_types, type_map=tmap,
        phase_counts={k: int(sum(1 for l in labels if l == k)) for k in tmap.values()},
        boundary=bc_note, plate_z_sim=float(plate_z), plate_z_source=h_src,
        phi_se=phi['phi_se'], phi_am=phi['phi_am'],
        porosity_sphere_pct_RECORD_ONLY=phi['porosity_sphere_pct_RECORD_ONLY'],
        closure_residual=phi['closure_residual'],
        z_floor_sim=phi['z_floor_sim'], H_sim=phi['H_sim'],
        solid_bot_sim=phi['solid_bot_sim'], solid_top_sim=phi['solid_top_sim'],
        deck_floor=deck, wall_record=phi['wall_record'], boundary_qc=phi['boundary'], handover_qc=handover_qc,
        coverage_AM_P_hertz_pct=cp, coverage_AM_S_hertz_pct=cs,
        coverage_AM_total_hertz_pct=ct, coverage_AM_only_hertz_pct=ca,
        tortuosity_dijkstra_SE=tau['tau_mean'],
        tortuosity_dijkstra_SE_wall=tau_wall['tau_mean'],
        status=dict(phi=STATUS_OK, porosity=STATUS_OK,
                    coverage_AM_P=sp, coverage_AM_S=ss, coverage_AM_total=st,
                    tortuosity=tau['status'], tortuosity_wall=tau_wall['status']),
        tau_detail=tau, tau_wall_detail=tau_wall, coverage_detail=dict(
            n_capped=cov['n_capped'],
            n_free_surface_invalid=cov['n_free_surface_invalid'],
            counts=cov['counts'], contact_headers=cheaders),
        V_box_sim=phi['V_box_sim'], raw=raw, area_channel=AREA_CHANNEL,
        wall_touch=wall_touch, wall_touch_rule=WALL_TOUCH_RULE,
        contact_scan=contact_scan, n_atom_frames=int(n_atom_frames),
        contract='codex_verdict_lhs_descriptors_20260913 §7 (1~6)',
        #  ── item 1 (09-29 · 1저자 "권고대로") — **새 키만** (옛 키 · status · handover_qc 는 그대로: WSL [2] 옛 수확 대조가 선다) ──
        #  벽 제외 피복률 = 분모에서 벽이 가린 구면 cap 2πrh 도 뺀 값 (`WALLEXCL_FORMULA`) · 상 규칙 · 상태 코드는 오늘 식과 같다
        coverage_AM_P_wallexcl_pct=xp, coverage_AM_S_wallexcl_pct=xs,
        coverage_AM_total_wallexcl_pct=xt, coverage_AM_only_wallexcl_pct=xa,
        coverage_AM_P_wallexcl_status=xps, coverage_AM_S_wallexcl_status=xss,
        coverage_AM_total_wallexcl_status=xts, coverage_AM_only_wallexcl_status=xas,
        coverage_wallexcl_detail=dict(n_capped=wx['n_capped'], n_free_surface_invalid=wx['n_free_surface_invalid'],
                                      counts=wx['counts'], formula=WALLEXCL_FORMULA, wall_rule=WALL_TOUCH_RULE),
        #  벽 분할 = 상 (AM_P · AM_S · AM · total) × 벽 (any · floor · plate) × 등급 (interior · touch · center_out · fully_out)
        coverage_wall_split=covw['split'],
        #  ── item 2 — c_cpl[22] ↔ 정확한 교차 원판 (r1 · r2 · δ = c_cpl[23]) 대조 · 주기 플래그 0/1 · 쌍 종류별 (진단 기록) ──
        contact_area_check=area_check,
        #  ── item 3 — 접촉 행의 문 기록 (중복 · 자기쌍이면 이 dict 대신 거부 · 고아 행 수는 여기에) ──
        contact_gate=gate)


def _atom_ids(path):
    """원자 덤프의 `id` 열 (접촉 덤프의 id 와 맞춘다)."""
    with open(path, 'r', encoding='utf-8', errors='replace') as fh:
        lines = fh.read().splitlines()
    starts = [i for i, ln in enumerate(lines) if ln.startswith('ITEM: ATOMS')]
    i = starts[-1]
    headers = lines[i].replace('ITEM: ATOMS', '').strip().split()
    if 'id' not in headers:
        raise BedRefusal(f'{path}: `id` 열이 없다 — 접촉 덤프와 입자를 맞출 수 없다')
    k = headers.index('id')
    out = []
    i += 1
    while i < len(lines) and not lines[i].startswith('ITEM:'):
        v = lines[i].split()
        if len(v) == len(headers):
            out.append(int(float(v[k])))
        i += 1
    return np.asarray(out, dtype=np.int64)


# ──────────────────────────────────────────────────────────────────────────────
# 자기검사 — **각 P1 의 반례를 먼저 재현**한다 (규율 ②)
# ──────────────────────────────────────────────────────────────────────────────

_FAILS = []


def chk(name, ok):
    print(('  ✓ ' if ok else '  ✗ ') + name)
    if not ok:
        _FAILS.append(name)


def neg(name, fn, want=BedRefusal):
    """음성대조 — **그 오류 종류로** 거부해야 통과.  아무 예외나 세지 않는다.

    (`PA12-09`: 어댑터의 ⑨ 가 `SystemExit` 이면 전부 성공으로 세어 **장식**이었다.)
    """
    try:
        fn()
    except want as e:
        print(f'  ✓ {name} — 거부: {str(e)[:72]}')
        return
    except Exception as e:                                    # noqa: BLE001
        chk(f'{name} (기대 {want.__name__}, 실제 {type(e).__name__}: {e})', False)
        return
    chk(f'{name} (거부하지 않았다)', False)


def _atom_file(tmp, rows, name='atom_100.liggghts', ts=100,
               lo=(0.0, 0.0, 0.0), hi=(10.0, 10.0, 20.0), bc='pp pp ff'):
    """rows = (id, x, y, z, radius, type)"""
    p = os.path.join(tmp, name)
    with open(p, 'w') as fh:
        fh.write(f'ITEM: TIMESTEP\n{ts}\nITEM: NUMBER OF ATOMS\n{len(rows)}\n')
        fh.write(f'ITEM: BOX BOUNDS {bc}\n')
        for k in range(3):
            fh.write(f'{lo[k]} {hi[k]}\n')
        fh.write('ITEM: ATOMS id x y z radius type\n')
        for r in rows:
            fh.write(' '.join(str(x) for x in r) + '\n')
    return p


def _contact_file(tmp, rows, name='contact_100.liggghts', ts=100, headers=None):
    """rows = (id1, id2, area)"""
    p = os.path.join(tmp, name)
    hd = headers or [COL_D1, COL_D2, COL_AREA]
    with open(p, 'w') as fh:
        fh.write(f'ITEM: TIMESTEP\n{ts}\nITEM: NUMBER OF ENTRIES\n{len(rows)}\n')
        fh.write('ITEM: ENTRIES ' + ' '.join(hd) + '\n')
        for r in rows:
            fh.write(' '.join(str(x) for x in r) + '\n')
    return p


def _stl(tmp, z=20.0, name='mesh.stl'):
    p = os.path.join(tmp, name)
    with open(p, 'w') as fh:
        fh.write('solid p\nfacet normal 0 0 1\nouter loop\n')
        for xy in ((0, 0), (1, 0), (0, 1)):
            fh.write(f'vertex {xy[0]} {xy[1]} {z}\n')
        fh.write('endloop\nendfacet\nendsolid p\n')
    return p


def selftest():
    import tempfile

    print('lhs_descriptor_harvest — 자기검사 (계약 6개 + P1 반례)')
    with tempfile.TemporaryDirectory() as tmp:

        # ── ① DESC-01 반례: τ 가 없어도 φ 는 나온다 ──────────────────────────
        #  SE 두 알이 서로 안 닿고 슬래브도 못 채운다 ⇒ τ = NOT_PERCOLATING.
        rows = [(1, 2.0, 2.0, 1.0, 0.5, 1), (2, 8.0, 8.0, 18.0, 0.5, 2)]
        a = _atom_file(tmp, rows)
        c = _contact_file(tmp, [])
        r = harvest(a, c, 2, 'desc01', mesh_path=_stl(tmp))
        chk('① DESC-01: τ 실패인데 phi_se 가 나온다',
            r['status']['tortuosity'] != STATUS_OK and r['phi_se'] is not None)
        chk('① DESC-01: phi_am 도 나온다', r['phi_am'] is not None)
        v = (4 / 3) * np.pi * 0.5 ** 3
        chk('① phi 값이 기하 그대로 (V_i/V_B)',
            abs(r['phi_se'] - v / 2000.0) < 1e-12 and abs(r['phi_am'] - v / 2000.0) < 1e-12)
        chk('① 공극률 closure 가 항등식', abs(r['closure_residual']) < 1e-12)

        # ── ② DESC-02 ①: 비관통에 유한 τ 를 주지 않는다 ────────────────────
        #  아래판에 닿는 SE 3알(고립) + 위쪽에 닿는 기둥 3알(아래판 미연결).
        rows = [(1, 1.0, 1.0, 0.5, 0.5, 2), (2, 3.0, 1.0, 0.5, 0.5, 2),
                (3, 5.0, 1.0, 0.5, 0.5, 2),
                (4, 9.0, 9.0, 18.5, 0.5, 2), (5, 9.0, 9.0, 19.4, 0.5, 2),
                (6, 9.0, 9.0, 19.9, 0.5, 2), (7, 5.0, 5.0, 10.0, 0.5, 1)]
        a2 = _atom_file(tmp, rows, name='atom_200.liggghts', ts=200)
        c2 = _contact_file(tmp, [], name='contact_200.liggghts', ts=200)
        r2 = harvest(a2, c2, 2, 'desc02a', mesh_path=_stl(tmp))
        chk('② DESC-02①: 비관통 → τ = None · NOT_PERCOLATING',
            r2['tortuosity_dijkstra_SE'] is None
            and r2['status']['tortuosity'] == STATUS_NOPERC)

        # ── ③ DESC-02 ②: 관통 성분이 있으면 예산이 무경로 쌍에 안 샌다 ──────
        #  관통 기둥 하나 + 무관한 고립 SE 덩어리 300알.
        col = [(i + 1, 5.0, 5.0, 0.5 + 0.9 * i, 0.5, 2) for i in range(22)]
        junk = [(1000 + i, 1.0 + 0.01 * i, 1.0, 10.0, 0.05, 2) for i in range(300)]
        a3 = _atom_file(tmp, col + junk, name='atom_300.liggghts', ts=300,
                        hi=(10.0, 10.0, 21.0))
        c3 = _contact_file(tmp, [], name='contact_300.liggghts', ts=300)
        r3 = harvest(a3, c3, 2, 'desc02b', mesh_path=_stl(tmp, z=21.0))
        chk('③ DESC-02②: 무경로 쌍이 예산을 안 먹는다 (τ 가 나온다)',
            r3['status']['tortuosity'] == STATUS_OK and r3['tortuosity_dijkstra_SE'] is not None)
        chk('③ 직선 기둥이면 τ ≈ 1', abs(r3['tortuosity_dijkstra_SE'] - 1.0) < 1e-6)
        chk('③ 표본이 전부 유효 (무경로 0건)',
            r3['tau_detail']['n_valid'] == r3['tau_detail']['n_sampled'])

        # ── ④ 계약①: 전체 피복률은 **실측 입자수 가중** ─────────────────────
        #  판정문 반례: P 1개 10 % · S 3개 90 % → 70 % (상평균평균 50 · 면적비 30).
        #  자유표면 4πr² = 4π, AM–SE 면적을 c% 가 되게 준다.
        fp = 4.0 * np.pi
        rows = [(1, 1.0, 1.0, 5.0, 1.0, 1), (2, 3.0, 1.0, 5.0, 1.0, 2),
                (3, 5.0, 1.0, 5.0, 1.0, 2), (4, 7.0, 1.0, 5.0, 1.0, 2),
                (90, 1.0, 5.0, 5.0, 1.0, 3), (91, 3.0, 5.0, 5.0, 1.0, 3),
                (92, 5.0, 5.0, 5.0, 1.0, 3), (93, 7.0, 5.0, 5.0, 1.0, 3)]
        con = [(1, 90, 0.10 * fp), (2, 91, 0.90 * fp),
               (3, 92, 0.90 * fp), (4, 93, 0.90 * fp)]
        a4 = _atom_file(tmp, rows, name='atom_400.liggghts', ts=400)
        c4 = _contact_file(tmp, con, name='contact_400.liggghts', ts=400)
        r4 = harvest(a4, c4, 3, 'cov', mesh_path=_stl(tmp))
        chk('④ P 평균 = 10 %', abs(r4['coverage_AM_P_hertz_pct'] - 10.0) < 1e-9)
        chk('④ S 평균 = 90 %', abs(r4['coverage_AM_S_hertz_pct'] - 90.0) < 1e-9)
        chk('④ 전체 = 70 % (상평균평균 50 이 아니다)',
            abs(r4['coverage_AM_total_hertz_pct'] - 70.0) < 1e-9)

        # ── ⑤ 계약④: Hertz 는 길이 scale 에 불변 ────────────────────────────
        k = 1000.0
        rows_s = [(r[0], r[1] * k, r[2] * k, r[3] * k, r[4] * k, r[5]) for r in rows]
        con_s = [(x[0], x[1], x[2] * k * k) for x in con]
        a5 = _atom_file(tmp, rows_s, name='atom_500.liggghts', ts=500,
                        hi=(10.0 * k, 10.0 * k, 20.0 * k))
        c5 = _contact_file(tmp, con_s, name='contact_500.liggghts', ts=500)
        r5 = harvest(a5, c5, 3, 'scale', plate_z=20.0 * k)
        chk('⑤ 계약④: scale ×1000 에도 Hertz 피복률 불변',
            abs(r5['coverage_AM_total_hertz_pct']
                - r4['coverage_AM_total_hertz_pct']) < 1e-9)
        chk('⑤ φ 도 불변 (무차원)', abs(r5['phi_se'] - r4['phi_se']) < 1e-12)

        # ── ⑥ DESC-05: 없는 상 = N/A, 존재하는데 무접촉 = 0 ─────────────────
        rows = [(1, 1.0, 1.0, 5.0, 1.0, 2), (90, 5.0, 5.0, 5.0, 1.0, 3)]
        a6 = _atom_file(tmp, rows, name='atom_600.liggghts', ts=600)
        c6 = _contact_file(tmp, [], name='contact_600.liggghts', ts=600)
        r6 = harvest(a6, c6, 3, 'absent', mesh_path=_stl(tmp))
        chk('⑥ DESC-05: 없는 AM_P → N/A (0 이 아니다)',
            r6['coverage_AM_P_hertz_pct'] is None
            and r6['status']['coverage_AM_P'] == STATUS_ABSENT)
        chk('⑥ DESC-05: 존재하는데 무접촉 AM_S → 0.0',
            r6['coverage_AM_S_hertz_pct'] == 0.0
            and r6['status']['coverage_AM_S'] == STATUS_OK)

        # ── ⑦ DESC-05: free surface ≤ 0 은 0 이 아니라 invalid ──────────────
        rows = [(1, 1.0, 1.0, 5.0, 1.0, 1), (2, 3.0, 1.0, 5.0, 1.0, 1),
                (90, 5.0, 5.0, 5.0, 1.0, 3)]
        con = [(1, 2, 99.0 * fp), (1, 90, 0.5 * fp)]
        a7 = _atom_file(tmp, rows, name='atom_700.liggghts', ts=700)
        c7 = _contact_file(tmp, con, name='contact_700.liggghts', ts=700)
        r7 = harvest(a7, c7, 3, 'freebad', mesh_path=_stl(tmp))
        chk('⑦ DESC-05: 분모붕괴가 0 으로 안 접힌다',
            r7['coverage_detail']['n_free_surface_invalid'] == 2)

        # ── ⑧ 음성대조: DESC-06 — 프레임이 섞이면 거부 ──────────────────────
        neg('⑧ DESC-06: atom_100 + contact_200 을 거부',
            lambda: harvest(a, c2, 2, 'mix', mesh_path=_stl(tmp)))

        # ── ⑨ 음성대조: 플래튼 높이 추정 금지 ───────────────────────────────
        neg('⑨ 계약⑤: mesh 도 --plate-z 도 없으면 거부',
            lambda: harvest(a, c, 2, 'noh'))
        neg('⑨ 계약⑤: 둘 다 주면 거부',
            lambda: harvest(a, c, 2, 'bothh', plate_z=20.0, mesh_path=_stl(tmp)))

        # ── ⑩ 음성대조: 선언 밖 type · 경계 플래그 ──────────────────────────
        bad = _atom_file(tmp, [(1, 1.0, 1.0, 5.0, 0.5, 9)],
                         name='atom_900.liggghts', ts=900)
        neg('⑩ 계약⑤: 선언 밖 type 을 거부',
            lambda: harvest(bad, _contact_file(tmp, [], name='contact_900.liggghts', ts=900),
                            2, 'badtype', mesh_path=_stl(tmp)))
        bbc = _atom_file(tmp, [(1, 1.0, 1.0, 5.0, 0.5, 1)],
                         name='atom_950.liggghts', ts=950, bc='pp pp pp')
        neg('⑩ 경계 플래그가 규약과 다르면 거부',
            lambda: harvest(bbc, _contact_file(tmp, [], name='contact_950.liggghts', ts=950),
                            2, 'badbc', mesh_path=_stl(tmp)))

        # ── ⑪ 음성대조: 접촉 면적 열이 없으면 거부 ──────────────────────────
        noarea = _contact_file(tmp, [(1, 2)], name='contact_960.liggghts', ts=960,
                               headers=[COL_D1, COL_D2])
        a11 = _atom_file(tmp, [(1, 1.0, 1.0, 5.0, 0.5, 1), (2, 2.0, 1.0, 5.0, 0.5, 2)],
                         name='atom_960.liggghts', ts=960)
        neg('⑪ 계약④: contact_area 열이 없으면 거부 (규약을 모른 채 안 낸다)',
            lambda: harvest(a11, noarea, 2, 'noarea', mesh_path=_stl(tmp)))

        # ── ⑫ 음성대조가 장식이 아닌지 (PA12-09 의 교훈) ────────────────────
        #  ⑧ 의 가드를 퇴행시키면 ⑧ 이 **반드시** 깨져야 한다.
        import lhs_descriptor_harvest as M
        keep = M.last_timestep
        M.last_timestep = lambda p: 0                     # 항상 같은 값 = 검사 무력화
        broke = False
        try:
            M.harvest(a, c2, 2, 'mut', mesh_path=_stl(tmp))
        except BedRefusal:
            broke = True
        except Exception:                                 # noqa: BLE001
            broke = True
        M.last_timestep = keep
        chk('⑫ PA12-09: TIMESTEP 가드를 퇴행시키면 ⑧ 이 실제로 뚫린다 (대조가 살아있다)',
            not broke)

        # ── ⑬a P1-HARV-01: τ 가 **평행이동에 불변**인가 ─────────────────────
        #  L4/L5 판정 반례: 쌍 찾기는 주기인데 길이를 raw 좌표차로 재면 같은 침대를
        #  옮기기만 해도 τ 가 9.850888284819803 → 1.0198039027185568 (9.6596배).
        def _chain(xs):
            n = len(xs)
            at = dict(x=np.array(xs, float), y=np.full(n, 5.0),
                      z=np.arange(1.0, n + 1.0), radius=np.full(n, 0.55),
                      type=np.full(n, 2, dtype=np.int64))
            return at, np.array(['SE'] * n, dtype=object)

        _lo, _hi = np.array([0., 0., 0.]), np.array([10., 10., 10.])
        _xs = [0.1, 9.9, 0.1, 9.9, 0.1]
        _t1 = tortuosity_se(*_chain(_xs), _lo, _hi)['tau_mean']
        _t2 = tortuosity_se(*_chain([(x + 5.0) % 10.0 for x in _xs]), _lo, _hi)['tau_mean']
        chk('⑬a P1-HARV-01: τ 가 xy 평행이동에 불변',
            _t1 is not None and _t2 is not None and abs(_t1 - _t2) < 1e-12)
        #  참값은 minimum-image 로 독립 계산한 것
        def _mi_ref(p, q):
            d = np.asarray(p, float) - np.asarray(q, float)
            d[0] -= 10.0 * round(d[0] / 10.0); d[1] -= 10.0 * round(d[1] / 10.0)
            return float(np.linalg.norm(d))
        _pts = np.column_stack([_xs, [5.] * 5, np.arange(1., 6.)])
        _ref = sum(_mi_ref(_pts[k], _pts[k + 1]) for k in range(4)) / 4.0
        chk('⑬a τ 가 minimum-image 해석값과 일치 (1.019803903)',
            _t1 is not None and abs(_t1 - _ref) < 1e-12 and abs(_ref - 1.019803903) < 1e-9)

        # ── ⑬b L1-04: 면적 채널 라벨이 매 행에 박히는가 ─────────────────────
        chk('⑬b L1-04: area_channel 이 출력에 있다',
            'dem_geometric_c_cpl22' in str(r4.get('area_channel', '')))
        chk('⑬b L1-04: 그 라벨이 Hertz 가 아님을 명시한다',
            'Hertz' in str(r4.get('area_channel', ''))
            and '2 - d/(2r)' in str(r4.get('area_channel', '')))
        #  기하 교차면적 ÷ Hertz = 2 − δ/(2r) 을 실제로 확인 (판정문 1.9875)
        _r, _d = 0.5, 0.05 * 0.25
        _ratio = (np.pi * (_r * _d - _d * _d / 4)) / (np.pi * (_r / 2) * _d)
        chk('⑬b L1-04: A_LIGG/A_Hertz = 2 − δ/(2r) = 1.9875',
            abs(_ratio - 1.9875) < 1e-9)

        # ── ⑭ LHS-08: 미관통의 **두 원인**을 산출물이 가르는가 ───────────────
        #  초판은 ⓐ 전극 밴드가 비어 **표본이 애초에 없는** 경우와 ⓑ 밴드는 찼는데
        #  성분이 안 이어진 경우를 **같은 `NOT_PERCOLATING`** 으로 접었다 (두 `return
        #  base` 가 같은 값을 낸다).  실물 130 중 **116** 이 그 값이었고 어느 쪽인지
        #  산출물만으로는 알 수 없었다 — φ_SE 로도 안 갈린다 (τ-OK 최소 φ_SE 0.1860
        #  보다 SE 가 많은데 실패한 케이스가 **53건**).
        def _bed(rows):
            """rows = (x, y, z, r, label) — 라벨을 직접 준다 (AM 이 z 범위를 정하는 경우)"""
            at = dict(x=np.array([q[0] for q in rows], float),
                      y=np.array([q[1] for q in rows], float),
                      z=np.array([q[2] for q in rows], float),
                      radius=np.array([q[3] for q in rows], float),
                      type=np.ones(len(rows), dtype=np.int64))
            return at, np.array([q[4] for q in rows], dtype=object)

        _lo8, _hi8 = np.array([0., 0., 0.]), np.array([10., 10., 20.])
        #  ⓐ 밴드가 빔 — SE 는 **하나로 이어져 있는데** 위 전극 밴드에 닿지 않는다.
        #    z_hi 를 **AM** 이 정한다 = 고체 z 범위 규약이라 SE 만 봐선 안 보이는 실패.
        _a_rows = [(5.0, 5.0, 0.5 + 0.9 * k, 0.5, 'SE') for k in range(11)]
        _a_rows += [(1.0, 1.0, 19.0, 0.5, 'AM_S')]
        _ta = tortuosity_se(*_bed(_a_rows), _lo8, _hi8)
        #  ⓑ 진짜 미관통 — 양 밴드에 SE 가 **있는데** 두 덩어리가 끊겼다.
        _b_rows = [(5.0, 5.0, 0.5 + 0.9 * k, 0.5, 'SE') for k in range(5)]
        _b_rows += [(5.0, 5.0, 15.5 + 0.9 * k, 0.5, 'SE') for k in range(5)]
        _tb = tortuosity_se(*_bed(_b_rows), _lo8, _hi8)
        _bda = _ta.get('band_detail') or {}
        _bdb = _tb.get('band_detail') or {}
        chk('⑭ LHS-08 ★재현: ⓐ(밴드 빔) 과 ⓑ(진짜 미관통) 의 status 가 **다르다**',
            _ta['status'] != _tb['status'])
        chk('⑭ LHS-08: ⓐ = ELECTRODE_BAND_EMPTY', _ta['status'] == STATUS_BAND_EMPTY)
        chk('⑭ LHS-08: ⓑ = NOT_PERCOLATING', _tb['status'] == STATUS_NOPERC)
        chk('⑭ LHS-08: 둘 다 유한 τ 를 내지 않는다 (판정은 그대로 보수적)',
            _ta['tau_mean'] is None and _tb['tau_mean'] is None)
        chk('⑭ LHS-08: 진단 블록 band_detail 이 붙는다', bool(_bda) and bool(_bdb))
        #  ⓐ 는 **한 덩어리인데도** 실패했다 = 규약(밴드 정의)이 용의자라는 신호
        chk('⑭ LHS-08 ⓐ: 위 밴드가 0 명 · 아래는 있다 · 성분은 하나',
            _bda.get('n_top', -1) == 0 and _bda.get('n_bot', -1) >= 1
            and _bda.get('n_components', -1) == 1)
        #  ⓑ 는 양쪽 밴드가 찼는데 성분이 둘 = 물리
        chk('⑭ LHS-08 ⓑ: 양 밴드가 차 있고 성분이 둘, 관통 성분 0',
            _bdb.get('n_bot', -1) >= 1 and _bdb.get('n_top', -1) >= 1
            and _bdb.get('n_components', -1) == 2
            and _bdb.get('n_span_components', -1) == 0)
        #  규약 판단(LHS-08 3단계)에 필요한 수치가 같은 수확에서 나온다 — 그러나
        #  **보고되는 τ 는 건드리지 않는다**.  이 두 줄이 그것을 강제한다.
        _tb2 = tortuosity_se(*_bed(_b_rows), _lo8, _hi8, plate_z=12.0)
        chk('⑭ LHS-08: plate_z 진단은 보고값·규약 문자열을 **안 바꾼다**',
            _tb2['status'] == _tb['status'] and _tb2['tau_mean'] == _tb['tau_mean']
            and _tb2['tau_convention'] == _tb['tau_convention'])
        chk('⑭ LHS-08: 규약 문자열이 solid_zrange 그대로다 (규약 판단은 재측정 뒤)',
            _tb['tau_convention']
            == 'harvest_v1/solid_zrange/rSEmax/no_fallback/same_component')
        chk('⑭ LHS-08: 그래도 plate_z 밴드 인원은 따로 적힌다 (규약 판단용)',
            (_tb2.get('band_detail') or {}).get('alt_n_top', -1)
            != (_tb2.get('band_detail') or {}).get('n_top', -1))
        #  ★ 날카로운 쪽 — ⓐ 는 규약을 바꾸면 **판정이 뒤집히는** 침대다 (BAND_EMPTY →
        #  OK, τ None → 유한).  여기서 plate_z 가 무해해야 "진단 전용"이 실재한다.
        #  (ⓑ 로만 검사하면 규약을 바꿔도 답이 안 변해 **통과해 버린다** = 약한 가드.)
        _ta2 = tortuosity_se(*_bed(_a_rows), _lo8, _hi8, plate_z=10.5)
        chk('⑭ LHS-08 ★가드: 판정이 뒤집히는 침대에서도 plate_z 가 τ 를 안 건드린다',
            _ta2['status'] == _ta['status'] and _ta2['tau_mean'] is None
            and (_ta2.get('band_detail') or {}).get('n_top', -1) == 0)
        chk('⑭ LHS-08: 그 침대의 alt_n_top 이 **규약을 바꾸면 몇 명인지**를 적는다',
            (_ta2.get('band_detail') or {}).get('alt_n_top', -1) >= 1
            and (_ta2.get('band_detail') or {}).get('alt_plate_above_solid') is False)
        #  양성 대조 — 진단을 붙였다고 성공 경로가 깨지면 안 된다
        _c_rows = [(5.0, 5.0, 0.5 + 0.9 * k, 0.5, 'SE') for k in range(22)]
        _tc = tortuosity_se(*_bed(_c_rows), _lo8, _hi8)
        chk('⑭ LHS-08: 관통 침대는 그대로 OK (진단이 성공을 안 깬다)',
            _tc['status'] == STATUS_OK
            and (_tc.get('band_detail') or {}).get('n_span_components', -1) == 1)

        # ── ⑬ 계약⑥: 291 코퍼스를 읽지 않는다 (정적) ────────────────────────
        src = open(os.path.abspath(__file__), encoding='utf-8').read()
        chk('⑬ 계약⑥: design_performance_corpus 를 읽는 코드가 없다',
            'design_performance_corpus' not in src.split('"""')[2])
        chk('⑬ full_metrics.json 을 읽는 코드가 없다',
            'full_metrics' not in src.split('"""')[2])
        #  item 2 (09-29) 개정 — 옛 검사는 "머리 (첫 함수 독스트링 앞 58 줄) 에 문자열 plastic_coverage 가 없다" 였다: ① 머리 밖
        #  (함수 안 지연 import) 은 못 봤고 ② 순수 기하 `_intersection_disc_area` 하나를 가져오는 것 (item 2 의 요구 · 규율 ①) 도 막았다.
        #  ⇒ 소스 **전체** AST 로 보고, 허용 이름을 그 하나로 한정한다.  DESC-03 의 뜻 (Physics 피복률 경로를 부르지 않는다) 은 그대로
        #  — 금지 모양 여섯 (Physics 이름 · * · 모듈째 · 동적 import 상수/비상수) 을 잡는지는 ㉑ 의 변이 검사가 본다.
        _pcn, _pcb = _plastic_coverage_uses(src)
        chk(f'⑬ DESC-03: plastic_coverage 를 어떤 모양으로도 쓰지 않는다 (소스 전체 AST · 허용 이름 없음 · 09-30 LHSC-05 (a) · 위반 {_pcb})',
            _pcn <= PLASTIC_COVERAGE_ALLOWED and not _pcb)

        # ── ⑭ LHS-10 (2026-09-24): 분모 바닥 = 벽 z = 0 (웹앱 `V_box = L²·plate_z`) — 덤프 상자 바닥이 아니다 ──
        rows14 = [(1, 2.0, 2.0, 1.0, 0.5, 1), (2, 5.0, 5.0, 2.0, 0.5, 2), (3, 8.0, 3.0, 3.0, 0.5, 3)]
        at14, lo14, hi14, _bc14 = read_atom_dump(
            _atom_file(tmp, rows14, name='atom_14.liggghts', lo=(0.0, 0.0, -1.0), hi=(10.0, 10.0, 20.0)))
        v14 = volumes_and_phi(at14, phase_labels(at14['type'], 3)[0], lo14, hi14, 5.0)
        chk('⑭ LHS-10: 상자 바닥이 −1 이어도 분모 높이 = plate_z − 벽 = 5', abs(v14['H_sim'] - 5.0) < 1e-12)
        _vs = 3 * (4.0 / 3.0) * np.pi * 0.5 ** 3
        chk('⑭ porosity = 1 − ΣV / (L²·plate_z) — 웹앱 calc_porosity 와 같은 식',
            abs(v14['porosity_sphere_pct_RECORD_ONLY'] - 100.0 * (1.0 - _vs / (10.0 * 10.0 * 5.0))) < 1e-9)
        #  ── ⑭ LHS-12 (판단 J14, 비준 09-24): 벽 밖 입자는 **거부하지 않고 기록**한다 ──
        #     J13 의 가드 (z − r < −½·r_max 면 거부) 가 실제 130 에서 58 건을 막았다 — 가장 큰 AM 이 바닥과
        #     깊게 겹친 **연속 분포**를 문턱에서 자른 것이었다.  (가) 주 값은 웹앱 식 그대로 · (나) 되돌려 놓은 값은 기록.
        _v1 = (4.0 / 3.0) * np.pi * 0.5 ** 3
        at14b, lo14b, hi14b, _bc14b = read_atom_dump(_atom_file(
            tmp, [(1, 2.0, 2.0, -0.9, 0.5, 1)] + rows14[1:], name='atom_14b.liggghts',
            lo=(0.0, 0.0, -1.0), hi=(10.0, 10.0, 20.0)))
        try:
            v14b = volumes_and_phi(at14b, phase_labels(at14b['type'], 3)[0], lo14b, hi14b, 5.0)
        except BedRefusal as e:
            v14b = None
            chk(f'⑭ LHS-12: 벽 아래 입자가 있어도 거부하지 않는다 (거부됨: {str(e)[:60]})', False)
        if v14b is not None:
            chk('⑭ LHS-12: 벽 아래 입자가 있어도 porosity 는 웹앱 식 그대로 (ΣV 전부 · L²·plate_z)',
                abs(v14b['porosity_sphere_pct_RECORD_ONLY'] - 100.0 * (1.0 - _vs / (10.0 * 10.0 * 5.0))) < 1e-9)
            _wf = (v14b.get('wall_record') or {}).get('floor') or {}
            chk('⑭ 기록: 중심이 벽 아래인 입자 1 · 통째로 벽 아래 1',
                _wf.get('n_center_out') == 1 and _wf.get('n_fully_out') == 1)
            chk('⑭ 기록: 벽 아래 부피 = 구 하나 통째 = ΣV 의 1/3',
                abs((_wf.get('v_out_pct') or -1.0) - 100.0 / 3.0) < 1e-9)
            _pb = (v14b.get('wall_record') or {}).get('pushback') or {}
            chk('⑭ (나) 되돌려 놓은 두께 = plate_z + 벽 밖 부피 / 면적',
                abs((_pb.get('H_sim') or -1.0) - (5.0 + _v1 / 100.0)) < 1e-12)
            chk('⑭ (나) porosity = 1 − ΣV / (L²·H′)',
                abs((_pb.get('porosity_pct_RECORD_ONLY') or -1.0)
                    - 100.0 * (1.0 - _vs / (100.0 * (5.0 + _v1 / 100.0)))) < 1e-9)
        #     부분 겹침 — 바닥 cap (z 0.2, r 0.5 → h 0.3) · 플래튼 cap (z 4.8, plate 5 → h 0.3)
        at14c, lo14c, hi14c, _bc14c = read_atom_dump(_atom_file(
            tmp, [(1, 2.0, 2.0, 0.2, 0.5, 1), (2, 5.0, 5.0, 2.0, 0.5, 2), (3, 8.0, 3.0, 4.8, 0.5, 3)],
            name='atom_14c.liggghts', lo=(0.0, 0.0, -1.0), hi=(10.0, 10.0, 20.0)))
        _cap = np.pi * 0.3 ** 2 * (3 * 0.5 - 0.3) / 3.0
        try:
            _wc = volumes_and_phi(at14c, phase_labels(at14c['type'], 3)[0], lo14c, hi14c, 5.0).get('wall_record') or {}
        except BedRefusal:
            _wc = {}
        _f, _p = _wc.get('floor') or {}, _wc.get('plate') or {}
        chk('⑭ 바닥 cap 부피 = π h²(3r − h)/3 (h 0.3)', abs((_f.get('v_out_sim') or -1.0) - _cap) < 1e-12)
        chk('⑭ 플래튼 cap 도 같은 식', abs((_p.get('v_out_sim') or -1.0) - _cap) < 1e-12)
        chk('⑭ 가장 깊은 입자: 상 · cap 깊이/반지름 0.6 (= 이 경우 접촉 겹침과 같다) · 중심은 벽 위',
            (_f.get('deepest') or {}).get('phase') == 'AM_P'
            and abs(((_f.get('deepest') or {}).get('outside_cap_depth_over_r') or -1.0) - 0.6) < 1e-12
            and _f.get('n_center_out') == 0 and _f.get('n_touch') == 1)
        #     덱에서 바닥을 **직접** 확인한다 (입자 깊이로 추정하지 않는다)
        def _deck(name, body):
            p = os.path.join(tmp, name)
            open(p, 'w', encoding='utf-8').write(body)
            return p
        _wall = ('fix zwall_bot all wall/gran model hooke/hysteresis tangential history '
                 'rolling_friction cdt primitive type 1 zplane {z}\n')
        d_ok = _deck('in.ok', 'region reg_box block 0.0 0.05 0.0 0.05 -0.01 1.0 units box\n' + _wall.format(z='0.0'))
        try:
            _df = check_deck_floor(d_ok)
        except Exception as e:                                           # noqa: BLE001
            _df = {'err': f'{type(e).__name__}: {e}'}
        chk('⑭ 덱: 바닥 zplane 0.0 · 벽 재질 type 1 을 읽는다',
            _df.get('z') == 0.0 and _df.get('wall_type') == 1)
        neg('⑭ 덱: 바닥이 0 이 아니면 (zplane −0.01) 거부',
            lambda: check_deck_floor(_deck('in.shift', _wall.format(z='-0.01'))))
        neg('⑭ 덱: 바닥 벽이 없으면 거부 (메시 바닥 등 — 가정을 확인할 수 없다)',
            lambda: check_deck_floor(_deck('in.none', 'fix m1 all property/global youngsModulus peratomtype 1 2\n')))
        neg('⑭ 덱: zplane 이 변수면 거부 (못 읽은 값을 0 으로 치지 않는다)',
            lambda: check_deck_floor(_deck('in.var', _wall.format(z='${z0}'))))
        try:
            _dc = check_deck_floor(_deck('in.cont', '# fix old all wall/gran model hooke primitive type 2 zplane -5\n'
                                           'fix zwall_bot all wall/gran model hooke/hysteresis &\n'
                                           '    tangential history primitive type 1 zplane 0.0  # 바닥\n'))
        except Exception:                                                # noqa: BLE001
            _dc = {}
        chk('⑭ 덱: 주석 줄은 무시 · `&` 로 이어진 줄은 붙여 읽는다', _dc.get('z') == 0.0 and _dc.get('wall_type') == 1)
        #     CLI 는 덱 없이 돌지 않는다 · 산출물에 덱 확인 · 벽 기록 · 덱 sha 가 남는다
        a14 = _atom_file(tmp, [(1, 2.0, 2.0, 1.0, 0.5, 1), (2, 5.0, 5.0, 2.0, 0.5, 2)], name='atom_140.liggghts', ts=140)
        c14 = _contact_file(tmp, [(1, 2, 0.01)], name='contact_140.liggghts', ts=140)
        neg('⑭ CLI: --deck 없이는 돌지 않는다 (바닥 확인 없이 수확하지 않는다)',
            lambda: main(['--atom', a14, '--contact', c14, '--plate-z', '5.0', '--n-types', '2']), want=SystemExit)
        try:
            r14 = harvest(a14, c14, 2, 'deck', plate_z=5.0, deck_path=d_ok)
        except TypeError as e:
            r14 = {}
            chk(f'⑭ harvest(deck_path=…) 를 받는다 ({e})', False)
        chk('⑭ 산출물에 덱 확인 · 벽 기록 · 덱 sha · 벽 z 가 남는다',
            (r14.get('deck_floor') or {}).get('z') == 0.0 and 'wall_record' in r14
            and 'deck' in (r14.get('raw') or {}) and r14.get('z_floor_sim') == 0.0)

        # ── ⑮ Codex HND-01 · 02 · 03 · 04 · 06 (판정 09-25 · 비준 09-25 "ㅇㅇ ㄱ ㄱ") — 재현 먼저 ──
        _wr14b = (v14b or {}).get('wall_record') or {}
        _fd = (_wr14b.get('floor') or {}).get('deepest') or {}
        chk('⑮ HND-03: 깊이 필드는 `outside_cap_depth_over_r` — `overlap_over_r` 는 없다 (접촉 겹침과 다른 양)',
            'outside_cap_depth_over_r' in _fd and 'overlap_over_r' not in _fd)
        chk('⑮ HND-03: 통째로 벽 아래인 입자의 접촉 겹침 = 0 (평면의 접촉 범위 밖)',
            _fd.get('contact_overlap_over_r') == 0.0)
        _fc = (_wc.get('floor') or {}).get('deepest') or {}
        chk('⑮ HND-03: 부분 겹침 입자 (z 0.2 · r 0.5) 의 접촉 겹침 = (r − |dist|)/r = 0.6',
            abs((_fc.get('contact_overlap_over_r') if _fc.get('contact_overlap_over_r') is not None else -1.0) - 0.6) < 1e-12)
        _vbp = (_wr14b.get('floor') or {}).get('v_out_by_phase') or {}
        chk('⑮ HND-01 (§8-1): 상별 벽 밖 부피 — 14b 바닥 = AM_P 구 하나 통째 · SE 0',
            abs(_vbp.get('AM_P', -1.0) - _v1) < 1e-12 and _vbp.get('SE', -1.0) == 0.0)
        _cl = _wr14b.get('clipped') or {}
        chk('⑮ (다) clipped: porosity = 1 − (ΣV − W)/(L²·plate_z) — 14b 는 구 둘만 남는다',
            abs((_cl.get('porosity_pct_RECORD_ONLY') if _cl.get('porosity_pct_RECORD_ONLY') is not None else -1.0)
                - 100.0 * (1.0 - 2 * _v1 / 500.0)) < 1e-9)
        chk('⑮ (다) clipped: phi_am = (V_AM − W_AM)/V — AM_S 하나만 남는다 (AM_P 는 통째로 밖)',
            abs((_cl.get('phi_am') if _cl.get('phi_am') is not None else -1.0) - _v1 / 500.0) < 1e-12)
        _bd = (v14b or {}).get('boundary') or {}
        chk('⑮ HND-03/04 적격성: 중심이 벽 밖인 입자가 있으면 physical_target_status HOLD + BOUNDARY_CENTER_OUT (계산 상태는 OK)',
            _bd.get('physical_target_status') == 'HOLD' and 'BOUNDARY_CENTER_OUT' in (_bd.get('hold_reason_codes') or [])
            and _bd.get('calculation_status') == 'OK')
        _bd14 = v14.get('boundary') or {}
        chk('⑮ 적격성: 전부 안이면 OK (보류 코드 없음)',
            _bd14.get('physical_target_status') == 'OK' and not _bd14.get('hold_reason_codes'))
        at14n, lo14n, hi14n, _bc14n = read_atom_dump(_atom_file(
            tmp, [(1, 5.0, 5.0, 2.5, 4.0, 1), (2, 5.0, 5.0, 2.5, 4.0, 3)], name='atom_14n.liggghts',
            lo=(0.0, 0.0, 0.0), hi=(10.0, 10.0, 20.0)))
        v14n = volumes_and_phi(at14n, phase_labels(at14n['type'], 3)[0], lo14n, hi14n, 5.0)
        _bdn = v14n.get('boundary') or {}
        chk('⑮ HND-04 적격성: porosity < 0 이면 HOLD + NEGATIVE_POROSITY · phi_sum_gt_one (값은 그대로 낸다)',
            v14n['porosity_sphere_pct_RECORD_ONLY'] < 0 and 'NEGATIVE_POROSITY' in (_bdn.get('hold_reason_codes') or [])
            and _bdn.get('phi_sum_gt_one') is True and _bdn.get('physical_target_status') == 'HOLD')
        #  HND-06: STL 평판 검사
        _np = os.path.join(tmp, 'nonplanar.stl')
        with open(_np, 'w') as fh:
            fh.write('solid p\nfacet normal 0 0 1\nouter loop\nvertex 0 0 0\nvertex 1 0 0\nvertex 0 1 2\nendloop\nendfacet\nendsolid p\n')
        neg('⑮ HND-06: 평판이 아닌 STL (z 0 과 2) 은 거부 — 평균 1 을 높이로 받지 않는다', lambda: plate_z_from_stl(_np))
        _psi = globals().get('plate_stl_info')
        try:
            _pi = _psi(_stl(tmp, z=7.0, name='flat.stl')) if _psi else {}
        except Exception:                                                # noqa: BLE001
            _pi = {}
        chk('⑮ HND-06: 평판 STL 은 span 0 · 꼭짓점 수 · z 평균 기록',
            _pi.get('span_sim') == 0.0 and _pi.get('n_vertices') == 3 and _pi.get('z_mean_sim') == 7.0)
        #  HND-02: 덱의 **활성** 바닥 벽 — fix 생명주기 · group · 지원 밖 명령
        _W = 'fix {id} {grp} wall/gran model hooke/hysteresis primitive type 1 zplane {z}\n'
        neg('⑮ HND-02: unfix 된 바닥 (활성 벽 없음) 은 거부',
            lambda: check_deck_floor(_deck('in.unfix', _W.format(id='floor', grp='all', z='0.0') + 'unfix floor\nrun 100\n')))
        neg('⑮ HND-02: 재정의된 바닥 (마지막 활성 = 2) 은 거부',
            lambda: check_deck_floor(_deck('in.redef', _W.format(id='floor', grp='all', z='0.0') + 'unfix floor\n'
                                           + _W.format(id='floor', grp='all', z='2.0') + 'run 100\n')))
        try:
            _dr = check_deck_floor(_deck('in.redef0', _W.format(id='floor', grp='all', z='2.0') + 'unfix floor\n'
                                         + _W.format(id='floor', grp='all', z='0.0')))
        except Exception as e:                                           # noqa: BLE001
            _dr = {'err': f'{type(e).__name__}: {e}'}
        chk('⑮ HND-02: 재정의로 마지막 활성이 0 이면 통과 · 활성 벽 1', _dr.get('z') == 0.0 and _dr.get('n_active_walls') == 1)
        neg('⑮ HND-02: group 이 all 이 아닌 바닥은 거부 (전 상 구속 증거 없음)',
            lambda: check_deck_floor(_deck('in.grp', _W.format(id='floor', grp='AM_only', z='0.0'))))
        neg('⑮ HND-02: include · jump · if · read_restart 가 있으면 "검증 불가" 로 거부',
            lambda: check_deck_floor(_deck('in.inc', 'include other.in\n' + _W.format(id='floor', grp='all', z='0.0'))))
        chk('⑮ HND-02: 기존 산출물 키 유지 (fix_id · wall_type)', _df.get('fix_id') == 'zwall_bot' and _df.get('wall_type') == 1)
        #  HND-04: 인계용 평면 QC 가 산출물에 있다
        _q = r14.get('handover_qc') or {}
        chk('⑮ HND-04: `handover_qc` — 두께 µm (sim × 1e3) · 적격성 · 보류 코드 · 규약 ID · sha 셋',
            abs((_q.get('thickness_wall_gap_um') if _q.get('thickness_wall_gap_um') is not None else -1.0) - 5000.0) < 1e-9
            and _q.get('physical_target_status') == 'OK' and _q.get('hold_reason_codes') == ''
            and _q.get('boundary_model_id') and _q.get('measurement_protocol_id')
            and len(_q.get('deck_sha256') or '') == 64 and len(_q.get('contact_sha256') or '') == 64)
        chk('⑮ HND-01: 등록 열의 명목 alias (`phi_se_spheresum_nominal_gap`) = phi_se 그대로',
            _q.get('phi_se_spheresum_nominal_gap') == r14.get('phi_se') and _q.get('porosity_spheresum_nominal_gap_pct') == r14.get('porosity_sphere_pct_RECORD_ONLY'))

        # ── ⑯ C (τ 진단, LHS-08 · Codex §8-3): 벽 기준 밴드 — 벽 아래로 샌 입자가 solid 아래 밴드를 비운다 ──
        _c_rows2 = [(5.0, 5.0, 0.5 + 0.9 * k, 0.5, 'SE') for k in range(22)] + [(2.0, 2.0, -1.5, 0.5, 'AM_P')]
        _tw = tortuosity_se(*_bed(_c_rows2), _lo8, _hi8, plate_z=20.0)
        _bw = _tw.get('band_detail') or {}
        chk('⑯ 벽 아래 입자 (z −1.5) 가 solid 아래 밴드를 [−2, −1] 로 끌어내려 SE 가 없다 (BAND_EMPTY 재현)',
            _tw['status'] == STATUS_BAND_EMPTY and _bw.get('n_bot') == 0)
        chk('⑯ 벽 기준 진단: 바닥 밴드 [0, t] 의 SE ≥ 1 · 플래튼 밴드 인원 · 벽 z 기록',
            (_bw.get('wall_n_bot') or 0) >= 1 and _bw.get('wall_n_top') is not None and _bw.get('wall_z_floor') == 0.0)
        chk('⑯ 벽 기준 진단: 벽 밴드 둘을 잇는 성분 수 (여기선 1)', _bw.get('wall_n_span_components') == 1)
        chk('⑯ 보고 τ 규약은 불변 (solid_zrange 문자열 그대로)', 'solid_zrange' in _tw['tau_convention'])

        # ── ⑰ LHS-08 규약 판단 (1저자 비준 09-28 "벽 기준 τ 새 열"): 바닥 벽 (z = Z_FLOOR) · 플래튼 밴드 τ 를 **새 열**로 ──
        #  옛 τ (solid_zrange) 는 바이트 그대로 둔다 — 새 규약은 새 키 (`wall_tau`) · 새 규약 문자열.
        _tw3 = tortuosity_se(*_bed(_c_rows2), _lo8, _hi8, plate_z=20.0)
        _ww = _tw3.get('wall_tau') or {}
        chk('⑰ ★ 벽 τ: 옛 규약이 BAND_EMPTY 인 침대 (벽 아래 AM) 에서 새 규약은 OK · τ = 1 (곧은 기둥)',
            _ww.get('status') == STATUS_OK and _ww.get('tau_mean') is not None and abs(_ww['tau_mean'] - 1.0) < 1e-12)
        chk('⑰ 벽 τ 규약 문자열 = TAU_WALL_CONVENTION (harvest_v3/wall_z0_plate/…)',
            _ww.get('tau_convention') == 'harvest_v3/wall_z0_plate/rSEmax/no_fallback/same_component')
        chk('⑰ 옛 τ 는 그대로 — status · 값 · 규약 문자열 (solid_zrange)',
            _tw3['status'] == STATUS_BAND_EMPTY and _tw3['tau_mean'] is None
            and _tw3['tau_convention'] == 'harvest_v1/solid_zrange/rSEmax/no_fallback/same_component')
        chk('⑰ 벽 τ 의 관통 성분 수 = 진단 wall_n_span_components (같은 밴드 정의)',
            _ww.get('n_span_components') == (_tw3.get('band_detail') or {}).get('wall_n_span_components') == 1)
        _tb3 = tortuosity_se(*_bed(_b_rows), _lo8, _hi8, plate_z=20.0)
        chk('⑰ 벽 τ 도 진짜 미관통 (두 덩어리) 은 NOT_PERCOLATING · 유한 τ 없음',
            (_tb3.get('wall_tau') or {}).get('status') == STATUS_NOPERC
            and (_tb3.get('wall_tau') or {}).get('tau_mean') is None)
        _tn3 = tortuosity_se(*_bed(_c_rows2), _lo8, _hi8)
        chk('⑰ plate_z 가 없으면 벽 τ 를 내지 않는다 (추정하지 않는다)',
            (_tn3.get('wall_tau') or {}).get('status') == 'PLATE_Z_MISSING'
            and (_tn3.get('wall_tau') or {}).get('tau_mean') is None)
        #  ★ 회귀 — 옛 τ 가 바이트 그대로인가 (공통 표본 함수로 옮기기 **전** 값, 2026-09-28 기록)
        _rng7 = np.random.default_rng(7)
        _rr = [(float(x), float(y), float(z), 0.6, 'SE')
               for x, y, z in _rng7.uniform([0, 0, 0.3], [10, 10, 19.7], size=(900, 3))]
        _tr = tortuosity_se(*_bed(_rr), _lo8, _hi8, plate_z=20.0)
        chk('⑰ 회귀: 옛 τ (무작위 900 SE) = 옮기기 전 값 그대로 (mean · median · 표본 수)',
            _tr['status'] == STATUS_OK and _tr['tau_mean'] == 2.0612290410739833
            and _tr['tau_median'] == 2.0805329527696066 and _tr['n_sampled'] == 160 and _tr['n_valid'] == 160)
        chk('⑰ 회귀: 옛 τ (⑬a 사슬) = 1.0198039027185568 그대로', _t1 == 1.0198039027185568)
        #  두 규약의 밴드가 **같은** 침대 (맨 아래 입자가 바닥에 · 맨 위 입자가 플래튼에 닿는다) 에서는 같은 표본 규칙이므로 τ 가 같아야 한다
        _tc = tortuosity_se(*_chain(_xs), _lo, _hi, plate_z=5.55)
        chk('⑰ 밴드가 같은 침대에서는 벽 τ = 옛 τ (같은 표본 규칙 · 같은 seed)',
            (_tc.get('wall_tau') or {}).get('status') == STATUS_OK
            and (_tc.get('wall_tau') or {}).get('tau_mean') == _tc['tau_mean'] == _t1)
        #  수확 산출물 — 새 키 셋 (옛 키는 그대로)
        chk('⑰ harvest() 산출물: tortuosity_dijkstra_SE_wall · tau_wall_detail · status.tortuosity_wall',
            'tortuosity_dijkstra_SE_wall' in r14 and isinstance(r14.get('tau_wall_detail'), dict)
            and 'tortuosity_wall' in (r14.get('status') or {})
            and 'tortuosity_dijkstra_SE' in r14 and 'tau_detail' in r14)

        # ── ⑱ J20-a (1저자 비준 09-28 밤 "권고하는걸로") — 접촉 덤프 점검 · 상별 벽 접촉 비율 (새 키만 · 옛 키 그대로) ──
        _hd18 = [COL_D1, COL_D2, COL_PERIODIC, COL_AREA, COL_DELTA]
        _rows18 = [(1, 2, 1, 0.1, 0.2), (2, 3, 0, 0.1, 0.1), (3, 2, 0, 0.1, 0.1), (4, 5, 0, 0.0, -0.3)]
        _c18 = _contact_file(tmp, _rows18, name='contact_180.liggghts', ts=180, headers=_hd18)
        with open(_c18, 'a') as _fh:                              # 같은 파일에 둘째 프레임 (LIGGGHTS 고정 파일명 덤프 모양)
            _fh.write('ITEM: TIMESTEP\n181\nITEM: NUMBER OF ENTRIES\n1\nITEM: ENTRIES ' + ' '.join(_hd18) + '\n1 2 1 0.1 0.2\n')
        _s18 = scan_contact_dump(_c18)
        chk('⑱ scan: 프레임 2 · 마지막 블록만 행으로 (1 행) — 수확의 읽기와 같다',
            _s18['n_frames'] == 2 and _s18['n_rows_last'] == 1)
        _c18b = _contact_file(tmp, _rows18, name='contact_181.liggghts', ts=181, headers=_hd18)
        _s18b = scan_contact_dump(_c18b)
        chk('⑱ scan: 중복 무순서 쌍 (2–3 · 3–2) 1 쌍 · 초과 행 1 · δ ≤ 0 행 1 · 주기 플래그 행 1 · δ 최솟값 −0.3',
            _s18b['n_frames'] == 1 and _s18b['n_dup_pairs'] == 1 and _s18b['n_dup_rows'] == 1
            and _s18b['n_delta_nonpos'] == 1 and _s18b['n_periodic_flag'] == 1 and _s18b['delta_min'] == -0.3
            and _s18b['n_unique_pairs'] == 3 and _s18b['n_self_pairs'] == 0)
        _s18c = scan_contact_dump(_contact_file(tmp, [(1, 2, 0.1)], name='contact_182.liggghts', ts=182))
        chk('⑱ scan: δ · 주기 열이 없는 덤프 → 그 칸은 None (거부하지 않는다 · "열 없음" 으로 적는다)',
            _s18c['n_delta_nonpos'] is None and _s18c['n_periodic_flag'] is None
            and _s18c['has_delta_col'] is False and _s18c['n_rows_last'] == 1)
        _wt = wall_touch_fractions(np.asarray(['SE', 'SE', 'AM_P', 'AM_S'], dtype=object),
                                   np.asarray([0.5, 10.0, 0.9, 19.5]), np.asarray([1.0, 1.0, 1.0, 1.0]), 20.0)
        chk('⑱ 벽 접촉 비율: SE 바닥 1/2 · AM_P 바닥 1 · AM_S 플래튼 1 · 합친 AM 바닥 1/2 · 플래튼 1/2',
            _wt['SE']['floor'] == 0.5 and _wt['SE']['plate'] == 0.0 and _wt['AM_P']['floor'] == 1.0
            and _wt['AM_S']['plate'] == 1.0 and _wt['AM']['floor'] == 0.5 and _wt['AM']['plate'] == 0.5
            and _wt['AM']['n'] == 2)
        _wt2 = wall_touch_fractions(np.asarray(['AM', 'SE'], dtype=object), np.asarray([0.5, 5.0]),
                                    np.asarray([1.0, 1.0]), 20.0)
        chk('⑱ 2-type 침대: AM_P · AM_S 키 없음 (N/A · 0 이 아니다) · AM 은 그대로',
            'AM_P' not in _wt2 and 'AM_S' not in _wt2 and _wt2['AM']['floor'] == 1.0)
        chk('⑱ harvest() 산출물: wall_touch · wall_touch_rule · contact_scan · n_atom_frames (새 키) · status 키는 늘지 않았다',
            isinstance(r14.get('wall_touch'), dict) and r14.get('wall_touch_rule') == WALL_TOUCH_RULE
            and isinstance(r14.get('contact_scan'), dict) and r14.get('n_atom_frames') == 1
            and set((r14.get('status') or {}).keys()) == {'phi', 'porosity', 'coverage_AM_P', 'coverage_AM_S',
                                                           'coverage_AM_total', 'tortuosity', 'tortuosity_wall'})

        # ── ⑲ item 4 (09-29 · 1저자 "권고대로") — 벽 닿음 규칙 **하나** (`_wall_side` ↔ `wall_touch_fractions`) · 접선 반례 먼저 ──
        #  옛 코드: `_wall_side` (→ wall_record · 벽 밖 부피) 는 겹침 깊이 r − dist > 0 (접선 = 안 닿음), `wall_touch_fractions` 는
        #  z − r <= z_floor · z + r >= plate_z (접선 = 닿음) ⇒ 바닥에 정확히 맞닿은 입자 (z − r = 0) · 플래튼에 정확히 맞닿은 입자
        #  (z + r = plate_z) 에서 **같은 침대의 두 기록이 갈린다**.
        _lab19 = np.asarray(['SE', 'SE', 'AM_P', 'AM_S'], dtype=object)
        _at19 = dict(z=np.array([1.0, 19.0, 5.0, 0.5]), radius=np.array([1.0, 1.0, 1.0, 1.0]))
        _v19 = volumes_and_phi(_at19, _lab19, np.zeros(3), np.array([10.0, 10.0, 20.0]), 20.0)
        _w19 = wall_touch_fractions(_lab19, _at19['z'], _at19['radius'], 20.0)
        _wf19, _wp19 = _v19['wall_record']['floor'], _v19['wall_record']['plate']
        chk('⑲ item 4 ★반례: 바닥 접선 SE (z − r = 0) — wall_record 닿음 수 = wall_touch 닿음 수 (한 침대 · 한 규칙)',
            _wf19['n_touch_by_phase'].get('SE') == _w19['SE']['n_floor'])
        chk('⑲ item 4 ★반례: 플래튼 접선 SE (z + r = plate_z) — 두 기록이 같다',
            _wp19['n_touch_by_phase'].get('SE') == _w19['SE']['n_plate'])
        chk('⑲ item 4: 접선 = **안 닿음** (겹침 깊이 0 · 벽 밖 부피 0 · 가린 면 0) — SE 바닥 0 · 플래튼 0 · 겹친 AM_S (z 0.5) 는 닿음',
            _w19['SE']['n_floor'] == 0 and _w19['SE']['n_plate'] == 0
            and _w19['AM_S']['n_floor'] == 1 and _w19['AM_P']['n_floor'] == 0 and _wf19['v_out_by_phase']['SE'] == 0.0)
        #  무작위 200 침대 — 반 칸 격자 (정확한 접선이 많다) 와 연속값을 번갈아: 상별 · 벽별 닿음 수가 **모든** 침대에서 같아야 한다
        _rng19 = np.random.default_rng(19)
        _bad19 = 0
        for _t in range(200):
            _n = 40
            _rr = _rng19.choice([0.5, 1.0, 1.5], _n)
            _zz = (_rng19.integers(-4, 45, _n) * 0.5) if _t % 2 == 0 else np.round(_rng19.uniform(-2.0, 22.0, _n), 5)
            _pz = 20.0 if _t % 2 == 0 else float(np.round(_rng19.uniform(15.0, 21.0), 5))
            _lb = np.asarray(_rng19.choice(['SE', 'AM_P', 'AM_S'], _n), dtype=object)
            _vv = volumes_and_phi(dict(z=_zz, radius=_rr), _lb, np.zeros(3), np.array([10.0, 10.0, 30.0]), _pz)
            _ww = wall_touch_fractions(_lb, _zz, _rr, _pz)
            for _ph in ('SE', 'AM_P', 'AM_S'):
                if _ph in _ww and (_vv['wall_record']['floor']['n_touch_by_phase'].get(_ph, 0) != _ww[_ph]['n_floor']
                                   or _vv['wall_record']['plate']['n_touch_by_phase'].get(_ph, 0) != _ww[_ph]['n_plate']):
                    _bad19 += 1
        chk(f'⑲ item 4: 무작위 200 침대 (정확한 접선 포함) — 상별 · 벽별 닿음 수가 두 기록에서 전부 같다 (어긋남 {_bad19})', _bad19 == 0)
        chk('⑲ item 4: 규칙 문자열이 접선 = 안 닿음을 적는다 (옛 `<=` · `>=` 문자열이 아니다)',
            'tangent' in WALL_TOUCH_RULE and '<=' not in WALL_TOUCH_RULE and '>=' not in WALL_TOUCH_RULE)

        # ── ⑳ item 1 (09-29 · 1저자 "권고대로") — 벽 분할 · 벽 제외 피복률 (새 키만 · 옛 키 바이트 그대로) · 반례 먼저 ──
        def _nz(x):
            return float('nan') if x is None else x
        #  ★ 반례: 두 AM_S (r 1) 가 같은 AM–SE 면적 π (= 4πr² 의 25 %) — 하나는 안쪽 (z 5), 하나는 중심이 바닥 z = 0 위.
        #    오늘 식은 둘 다 25 % (바닥 밑 반구 2πr² 도 '덮이지 않은 자유 표면' 으로 센다) — 벽 분할은 touch 1 ·
        #    벽 제외는 π / (4π − 2π) = 50 % · AM_S 37.5 %.
        _rows20 = [(1, 2.0, 2.0, 0.0, 1.0, 2), (2, 5.0, 5.0, 5.0, 1.0, 2),
                   (90, 2.0, 5.0, 2.0, 0.5, 3), (91, 7.0, 5.0, 5.0, 0.5, 3)]
        _a20 = _atom_file(tmp, _rows20, name='atom_2000.liggghts', ts=2000)
        _c20 = _contact_file(tmp, [(1, 90, np.pi), (2, 91, np.pi)], name='contact_2000.liggghts', ts=2000)
        r20 = harvest(_a20, _c20, 3, 'wallsplit', mesh_path=_stl(tmp))
        _any20 = (((r20.get('coverage_wall_split') or {}).get('by_phase') or {}).get('AM_S') or {}).get('any') or {}
        _in20, _to20 = _any20.get('interior') or {}, _any20.get('touch') or {}
        chk('⑳ item 1: 오늘 식은 그대로 — 두 입자 다 25 % → AM_S 25 % (분모가 바닥 밑 반구도 센다)',
            abs(r20['coverage_AM_S_hertz_pct'] - 25.0) < 1e-12)
        chk('⑳ item 1 ★반례: 벽 분할 — touch 1 (오늘 식 25 %) · interior 1 (25 %) · center_out · fully_out 0',
            _to20.get('n') == 1 and _in20.get('n') == 1 and abs(_nz(_to20.get('mean_pct')) - 25.0) < 1e-12
            and abs(_nz(_in20.get('mean_pct')) - 25.0) < 1e-12
            and (_any20.get('center_out') or {}).get('n') == 0 and (_any20.get('fully_out') or {}).get('n') == 0)
        chk('⑳ item 1 ★반례: 벽 제외 — touch 입자 50 % · interior 25 % · AM_S 37.5 % · 전체 37.5 % (status OK)',
            abs(_nz(_to20.get('mean_wallexcl_pct')) - 50.0) < 1e-9 and abs(_nz(_in20.get('mean_wallexcl_pct')) - 25.0) < 1e-9
            and abs(_nz(r20.get('coverage_AM_S_wallexcl_pct')) - 37.5) < 1e-9
            and abs(_nz(r20.get('coverage_AM_total_wallexcl_pct')) - 37.5) < 1e-9
            and r20.get('coverage_AM_S_wallexcl_status') == STATUS_OK
            and r20.get('coverage_AM_total_wallexcl_status') == STATUS_OK)
        chk('⑳ item 1: 가린 면 비율 — touch 0.5 (반구) · interior 0',
            abs(_nz(_to20.get('blocked_frac_mean')) - 0.5) < 1e-12 and _in20.get('blocked_frac_mean') == 0.0)
        #  등급 넷 · 플래튼 · 무효 — AM_P 넷 (r 1): 안쪽 (z 5) · 플래튼 cap (z 19.5 → h 0.5 → 가린 면 π) · 중심 밖 (z −0.5 → h 1.5 → 3π) ·
        #  통째로 밖 (z −1.5 → h 2 → 4π = 온 구면).  AM–SE 면적 π · π · π/2 · π/10.
        _rows20b = [(1, 2.0, 2.0, 5.0, 1.0, 1), (2, 5.0, 5.0, 19.5, 1.0, 1), (3, 8.0, 2.0, -0.5, 1.0, 1),
                    (4, 8.0, 8.0, -1.5, 1.0, 1), (90, 1.0, 5.0, 5.0, 0.5, 3)]
        _c20b = _contact_file(tmp, [(1, 90, np.pi), (2, 90, np.pi), (3, 90, 0.5 * np.pi), (4, 90, 0.1 * np.pi)],
                              name='contact_2001.liggghts', ts=2001)
        r20b = harvest(_atom_file(tmp, _rows20b, name='atom_2001.liggghts', ts=2001), _c20b, 3, 'wallsplit4',
                       mesh_path=_stl(tmp))
        _sp20 = ((r20b.get('coverage_wall_split') or {}).get('by_phase') or {}).get('AM_P') or {}
        _wa, _wf, _wp = _sp20.get('any') or {}, _sp20.get('floor') or {}, _sp20.get('plate') or {}
        _CL = ('interior', 'touch', 'center_out', 'fully_out')
        chk('⑳ item 1: 등급 넷 (any = 두 벽 중 심한 쪽) — interior · touch (플래튼) · center_out · fully_out 각 1',
            [(_wa.get(c) or {}).get('n') for c in _CL] == [1, 1, 1, 1])
        chk('⑳ item 1: 벽별 — 바닥 interior 2 · center_out 1 · fully_out 1 / 플래튼 interior 3 · touch 1',
            [(_wf.get(c) or {}).get('n') for c in _CL] == [2, 0, 1, 1]
            and [(_wp.get(c) or {}).get('n') for c in _CL] == [3, 1, 0, 0])
        chk('⑳ item 1: 벽 제외 입자값 — 플래튼 cap 33.3 % (π/3π) · 중심 밖 50 % (0.5π/π) · 통째로 밖은 분모 0 → 제외하고 셈',
            abs(_nz((_wa.get('touch') or {}).get('mean_wallexcl_pct')) - 100.0 / 3.0) < 1e-9
            and abs(_nz((_wa.get('center_out') or {}).get('mean_wallexcl_pct')) - 50.0) < 1e-9
            and (_wa.get('fully_out') or {}).get('n_valid_wallexcl') == 0 and (_wa.get('fully_out') or {}).get('n_valid') == 1
            and (r20b.get('coverage_wallexcl_detail') or {}).get('n_free_surface_invalid') == 1)
        chk('⑳ item 1: AM_P 벽 제외 = 유효 셋 평균 (25 + 33.3 + 50)/3 · 오늘 식 = 넷 평균 (25 + 25 + 12.5 + 2.5)/4 = 16.25 (그대로)',
            abs(_nz(r20b.get('coverage_AM_P_wallexcl_pct')) - (25.0 + 100.0 / 3.0 + 50.0) / 3.0) < 1e-9
            and abs(r20b['coverage_AM_P_hertz_pct'] - 16.25) < 1e-9)
        chk('⑳ item 1: 가린 면 비율 — 플래튼 cap 0.25 · 중심 밖 0.75 · 통째로 밖 1.0',
            abs(_nz((_wa.get('touch') or {}).get('blocked_frac_mean')) - 0.25) < 1e-12
            and abs(_nz((_wa.get('center_out') or {}).get('blocked_frac_mean')) - 0.75) < 1e-12
            and abs(_nz((_wa.get('fully_out') or {}).get('blocked_frac_mean')) - 1.0) < 1e-12)

        def _reagg(row, n_key, m_key):
            nv = sum((row.get(c) or {}).get(n_key) or 0 for c in _CL)
            return (sum(((row.get(c) or {}).get(n_key) or 0) * ((row.get(c) or {}).get(m_key) or 0.0) for c in _CL) / nv
                    if nv else None)
        chk('⑳ item 1: 분할을 다시 모으면 상 평균 (오늘 식 · 벽 제외 — any · floor · plate 세 분할 모두)', all(
            abs(_nz(_reagg(_sp20.get(w) or {}, 'n_valid', 'mean_pct')) - r20b['coverage_AM_P_hertz_pct']) < 1e-9
            and abs(_nz(_reagg(_sp20.get(w) or {}, 'n_valid_wallexcl', 'mean_wallexcl_pct'))
                    - _nz(r20b.get('coverage_AM_P_wallexcl_pct'))) < 1e-9
            for w in ('any', 'floor', 'plate')))
        #  AM–AM 면적 · 벽 cap 이 함께 빠진다 (함수 직접) — p1: 오늘 0.25π/(4π − 0.5π) · 벽 제외 0.25π/(4π − 0.5π − 2π)
        _cw = globals().get('coverage_wall')
        try:
            _w20 = _cw(np.array([1, 2, 3]), np.asarray(['AM_S', 'AM_S', 'SE'], dtype=object), np.array([1.0, 1.0, 0.5]),
                       np.array([0.0, 5.0, 5.0]), [1, 1], [2, 3], [0.5 * np.pi, 0.25 * np.pi], 20.0) if _cw else {}
        except Exception as e:                                              # noqa: BLE001
            _w20 = {'err': f'{type(e).__name__}: {e}'}
        _t20 = ((_w20.get('split') or {}).get('by_phase') or {}).get('AM_S', {}).get('any', {}).get('touch') or {}
        chk('⑳ item 1: AM–AM 면적과 벽 cap 이 분모에서 함께 빠진다 (오늘 0.25/3.5 · 벽 제외 0.25/1.5)',
            abs(_nz(_t20.get('mean_pct')) - 100.0 * 0.25 / 3.5) < 1e-9
            and abs(_nz(_t20.get('mean_wallexcl_pct')) - 100.0 * 0.25 / 1.5) < 1e-9)
        #  2-type 침대 — AM 이 한 상 ('AM'): AM_P · AM_S 는 N/A, 전체 = AM (오늘 식과 같은 규칙)
        _rows20c = [(1, 2.0, 2.0, 0.0, 1.0, 1), (2, 5.0, 5.0, 5.0, 1.0, 1), (90, 1.0, 5.0, 5.0, 0.5, 2)]
        r20c = harvest(_atom_file(tmp, _rows20c, name='atom_2002.liggghts', ts=2002),
                       _contact_file(tmp, [(1, 90, np.pi), (2, 90, np.pi)], name='contact_2002.liggghts', ts=2002),
                       2, 'wallsplit2', mesh_path=_stl(tmp))
        chk('⑳ item 1: 2-type — AM_P · AM_S 벽 제외 = N/A (N_A_PHASE_ABSENT) · AM = 전체 = 37.5 % · 분할 상은 AM · total',
            r20c.get('coverage_AM_P_wallexcl_status') == STATUS_ABSENT and r20c.get('coverage_AM_P_wallexcl_pct') is None
            and r20c.get('coverage_AM_S_wallexcl_status') == STATUS_ABSENT
            and abs(_nz(r20c.get('coverage_AM_only_wallexcl_pct')) - 37.5) < 1e-9
            and abs(_nz(r20c.get('coverage_AM_total_wallexcl_pct')) - 37.5) < 1e-9
            and set(((r20c.get('coverage_wall_split') or {}).get('by_phase') or {}).keys()) == {'AM', 'total'})
        #  ★ 옛 키 · 값 바이트 그대로 — 황금 해시는 **변경 전 코드** (item 1–4 전, `e72067854`) 에서 이 selftest 의 픽스처를 그대로
        #    돌려 잰 값 (옛 키 JSON (sort_keys) 의 sha256 앞 16 자).  `wall_touch` · `wall_touch_rule` 은 item 4 가 **일부러** 바꾼
        #    두 키라 따로 (item 4 뒤 값) 본다 — item 1–3 은 둘 다 건드리지 않는다.
        def _gh(o):
            return hashlib.sha256(json.dumps(o, ensure_ascii=False, sort_keys=True, default=str)
                                  .encode('utf-8')).hexdigest()[:16]
        _OLD_KEYS = ('case', 'timestep', 'n_types', 'type_map', 'phase_counts', 'boundary', 'plate_z_sim', 'plate_z_source',
                     'phi_se', 'phi_am', 'porosity_sphere_pct_RECORD_ONLY', 'closure_residual', 'z_floor_sim', 'H_sim',
                     'solid_bot_sim', 'solid_top_sim', 'deck_floor', 'wall_record', 'boundary_qc', 'handover_qc',
                     'coverage_AM_P_hertz_pct', 'coverage_AM_S_hertz_pct', 'coverage_AM_total_hertz_pct',
                     'coverage_AM_only_hertz_pct', 'tortuosity_dijkstra_SE', 'tortuosity_dijkstra_SE_wall', 'status',
                     'tau_detail', 'tau_wall_detail', 'coverage_detail', 'V_box_sim', 'raw', 'area_channel', 'wall_touch',
                     'wall_touch_rule', 'contact_scan', 'n_atom_frames', 'contract')
        _TOUCH = ('wall_touch', 'wall_touch_rule')
        _G_PRE = dict(desc01='aa9210f2032bed60', desc02a='ecd0413206a2a2f0', desc02b='58669b2a61312bac',
                      cov='043c0150cdefb746', scale='9dc041bab9c6614c', absent='7c90d0dd315d5832',
                      freebad='67fbc1e66a5f4cee', deck='1c153cc04d22e97a')
        _G_TOUCH = dict(desc01='eb9da009240956c0', desc02a='fd14da7515fc2202', desc02b='a4f7da4a155afe5a',
                        cov='f2fd1f9e1c492566', scale='f2fd1f9e1c492566', absent='012ff6777b9ea570',
                        freebad='6cf2b1e6f8f1beea', deck='eb9da009240956c0')
        _fx20 = dict(desc01=r, desc02a=r2, desc02b=r3, cov=r4, scale=r5, absent=r6, freebad=r7, deck=r14)
        _gbad = [nm for nm, res in _fx20.items()
                 if tuple(list(res.keys())[:len(_OLD_KEYS)]) != _OLD_KEYS
                 or _gh({k: res[k] for k in _OLD_KEYS if k not in _TOUCH}) != _G_PRE[nm]
                 or _gh({k: res.get(k) for k in _TOUCH}) != _G_TOUCH[nm]]
        chk(f'⑳ item 1–3 ★옛 키 바이트 그대로: 수확 픽스처 8 — 옛 38 키가 같은 순서로 맨 앞 · 값 해시 = 변경 전 (어긋남 {_gbad})',
            not _gbad)
        chk('⑳ item 1–3: volumes_and_phi 픽스처 4 (벽 기록 포함) · scan_contact_dump 픽스처 3 해시 = 변경 전',
            [_gh(v14), _gh(v14b), _gh(_wc), _gh(v14n)] == ['31438b087c2a236e', '4f0d8e0e2aa67f66', 'ed7aa1fccbadb9c8',
                                                           '691f36dc3b5b6d1b']
            and [_gh(_s18), _gh(_s18b), _gh(_s18c)] == ['0795432d89503b95', 'f61e50166dc92e49', 'dc71ae98e4af7ef3'])
        _NEW_KEYS = ('coverage_AM_P_wallexcl_pct', 'coverage_AM_S_wallexcl_pct', 'coverage_AM_total_wallexcl_pct',
                     'coverage_AM_only_wallexcl_pct', 'coverage_AM_P_wallexcl_status', 'coverage_AM_S_wallexcl_status',
                     'coverage_AM_total_wallexcl_status', 'coverage_AM_only_wallexcl_status', 'coverage_wallexcl_detail',
                     'coverage_wall_split', 'contact_area_check', 'contact_gate')
        chk('⑳ item 1: 새 키는 정해진 이름으로 옛 키 **뒤에만** 붙는다 (status · handover_qc 는 늘지 않는다 — WSL [2] 옛 수확 대조)',
            all(tuple(res.keys())[len(_OLD_KEYS):] == _NEW_KEYS for res in (r4, r20, r20c))
            and set(r20['status']) == set(r4['status']) and set(r20['handover_qc']) == set(r4['handover_qc']))

        # ── ㉑ item 2 (09-29 · 1저자 "권고대로") — 접촉 면적 대조 (진단 기록 · 거부 없음) · 반례 먼저 ──
        #  ★ 반례: AM_S–SE 행 하나의 덤프 면적이 정확한 교차 원판보다 1 % 크다 (나머지 두 행은 6 유효숫자 반올림만).  옛 코드는
        #    c_cpl[22] 를 확인 없이 피복률 분자로 썼고 **대조 기록이 없었다**.
        _cac = globals().get('contact_area_check')
        _car = globals().get('_contact_area_rows')
        _ida = globals().get('_intersection_disc_area')
        _hu = globals().get('_half_unit')
        _nbs = globals().get('_n_beyond_sig')
        _pcu = globals().get('_plastic_coverage_uses')

        def _g6(x):
            return float(f'{x:.6g}')
        _hd21 = [COL_D1, COL_D2, COL_PERIODIC, COL_AREA, COL_DELTA]
        _rows21 = [(1, 2.0, 2.0, 5.0, 1.0, 1), (2, 5.0, 5.0, 5.0, 0.8, 2),
                   (90, 3.0, 2.0, 5.0, 0.5, 3), (91, 6.0, 5.0, 5.0, 0.5, 3), (92, 8.0, 8.0, 5.0, 0.5, 3)]
        if _ida is not None:
            _con21 = [(1, 90, 0, _g6(_ida(1.0, 0.5, 0.05)), 0.05),                 # AM_P–SE · 플래그 0 · 반올림만
                      (90, 92, 1, _g6(_ida(0.5, 0.5, 0.02)), 0.02),                # SE–SE · 플래그 1 · 반올림만
                      (2, 91, 1, _g6(1.01 * _ida(0.8, 0.5, 0.03)), 0.03)]          # AM_S–SE · 플래그 1 · ★ 1 % 틀림
        else:
            _con21 = [(1, 90, 0, 0.1, 0.05), (90, 92, 1, 0.1, 0.02), (2, 91, 1, 0.1, 0.03)]
        _a21 = _atom_file(tmp, _rows21, name='atom_2100.liggghts', ts=2100)
        _c21 = _contact_file(tmp, _con21, name='contact_2100.liggghts', ts=2100, headers=_hd21)
        r21 = harvest(_a21, _c21, 3, 'areacheck', mesh_path=_stl(tmp))
        _ac21 = r21.get('contact_area_check') or {}
        _bf21 = _ac21.get('by_periodic_flag') or {}
        _bk21 = _ac21.get('by_pair_kind') or {}
        chk('㉑ item 2 ★반례: 1 % 틀린 행 하나가 허용폭 밖으로 세어진다 — 전체 1 · 플래그 1 에서 1 · 플래그 0 에서 0 (status OK · 비교 3 행)',
            _ac21.get('status') == STATUS_OK and _ac21.get('n_compared') == 3
            and (_ac21.get('all') or {}).get('n_beyond_tol') == 1
            and (_bf21.get('1') or {}).get('n_beyond_tol') == 1 and (_bf21.get('1') or {}).get('n_rows') == 2
            and (_bf21.get('0') or {}).get('n_beyond_tol') == 0 and (_bf21.get('0') or {}).get('n_rows') == 1)
        chk('㉑ item 2: 쌍 종류로도 갈린다 — AM-SE 2 행 중 1 초과 (피복률 분자) · SE-SE 0 · 최대 상대차 = 0.01/1.01 (덤프 값 기준)',
            (_bk21.get('AM-SE') or {}).get('n_rows') == 2 and (_bk21.get('AM-SE') or {}).get('n_beyond_tol') == 1
            and (_bk21.get('SE-SE') or {}).get('n_beyond_tol') == 0
            and abs(_nz((_ac21.get('all') or {}).get('rel_diff_max')) - 0.01 / 1.01) < 2e-5)
        chk('㉑ item 2: 진단 기록일 뿐 — 거부하지 않고 피복률은 덤프 면적 그대로 (AM_S = 100 · A22 / 4π·0.8²)',
            abs(r21['coverage_AM_S_hertz_pct'] - 100.0 * _con21[2][3] / (4.0 * np.pi * 0.8 ** 2)) < 1e-9)
        chk('㉑ item 2: 교차 원판은 한 구현 그대로 (다시 짜지 않았다 — 규율 ① · 09-30 부터 `lens_geometry` · plastic_coverage 도 같은 객체)',
            _ida is not None and getattr(_ida, '__module__', '') in ('plastic_coverage', 'lens_geometry'))
        chk('㉑ item 2: δ 열이 없는 덤프는 대조하지 않고 NO_DELTA_COLUMN 으로 적는다 (거부 없음)',
            (r20.get('contact_area_check') or {}).get('status') == 'NO_DELTA_COLUMN')
        #  허용폭 — 6 유효숫자 `%g` 토큰의 반올림만 있는 합성 3000 행 (반지름 0.4–6 µm · δ/r 1e-7–0.3) 은 **0 행 초과** 여야 하고,
        #  폭이 헐거우면 안 된다 (상대 폭 중앙 < 1e-5 · 최대 < 2e-5 · 3e-5 상대 오차 · Hertz 면적은 전부 초과)
        if _car is not None and _ida is not None:
            _rng21 = np.random.default_rng(21)
            _n21 = 3000
            _r1 = _rng21.uniform(0.0004, 0.006, _n21)
            _r2 = _rng21.uniform(0.0004, 0.006, _n21)
            _dd = 10.0 ** _rng21.uniform(-7.0, np.log10(0.3), _n21) * np.minimum(_r1, _r2)
            _At = np.asarray([_ida(a, b, d) for a, b, d in zip(_r1.tolist(), _r2.tolist(), _dd.tolist())])
            _R1, _R2 = np.asarray([_g6(x) for x in _r1]), np.asarray([_g6(x) for x in _r2])
            _D, _Ad = np.asarray([_g6(x) for x in _dd]), np.asarray([_g6(x) for x in _At])
            _ac, _lo21, _hi21, _lb21, _bz = _car(_R1, _R2, _D, _Ad)[:5]
            _bz3 = _car(_R1, _R2, _D, _Ad * (1.0 + 3e-5))[4]
            _Rs = _R1 * _R2 / (_R1 + _R2)
            _bzh = _car(_R1, _R2, _D, np.asarray([_g6(x) for x in np.pi * _Rs * _D]))[4]
            _tr = ((_hi21 - _lo21) / 2.0 + _hu(_Ad)) / _Ad             # 실효 상대 반폭 = 포괄 반폭 + 덤프 토큰 반폭 (옛 B/A 와 같은 뜻)
            chk(f'㉑ item 2: 허용폭 — 반올림만 있는 합성 3000 행 초과 {int(_bz.sum())} (0 이어야)', int(_bz.sum()) == 0)
            chk(f'㉑ item 2: 허용폭은 헐겁지 않다 — 실효 상대 반폭 중앙 {float(np.median(_tr)):.2e} < 1e-5 · 최대 {float(_tr.max()):.2e} < 2e-5',
                float(np.median(_tr)) < 1e-5 and float(_tr.max()) < 2e-5)
            chk('㉑ item 2: 판별력 — 면적 3e-5 상대 오차 · Hertz 면적 (π R* δ) 은 3000 행 전부 초과',
                int(_bz3.sum()) == _n21 and int(_bzh.sum()) == _n21)
        else:
            chk('㉑ item 2: 허용폭 함수 `_contact_area_rows` 가 있다', False)
        chk('㉑ item 2: 반폭 = 0.5·10^(E−5) (%g 끝 0 을 지워도 형식 정밀도 6 으로 — 0.005 → 5e-9 · 0 → 0)',
            _hu is not None and np.allclose(_hu(np.array([0.005, 0.0304637, 3.34479e-06, 0.0, 1000.0, 0.001, 9.99999e-3])),
                                            [5e-9, 5e-8, 5e-12, 0.0, 5e-3, 5e-9, 5e-9], rtol=1e-12, atol=0.0))
        chk('㉑ item 2: 6 유효숫자 전제 점검 — 7 유효숫자 값 (0.1234567) 하나를 센다',
            _nbs is not None and _nbs(np.array([0.1234567, 0.123457, 3.34479e-06, np.nan])) == 1)
        #  ⑬ 가드 변이 — Physics 이름 · * · 모듈째 · 동적 import (상수 · 비상수) 여섯 모양을 전부 잡고, 허용 이름 하나는 통과시킨다
        _bad_src = ('from plastic_coverage import film_area_from_overlap\n', 'from plastic_coverage import *\n',
                    'import plastic_coverage as P\nP.film_area_from_overlap(1.0, 1.0, 1.0)\n',
                    'import importlib\nimportlib.import_module("plastic_coverage")\n', '__import__("plastic_coverage")\n',
                    'import importlib\nm = "x"\nimportlib.import_module(m)\n')
        chk('㉑ item 2: ⑬ 가드 변이 — 금지 모양 여섯을 전부 위반으로 잡는다',
            _pcu is not None and all(bool(_pcu(s)[1]) for s in _bad_src))

        # ── ㉑′ ★ Codex LHSC-04 · LHSC-05 (09-30 · P2 · 1저자 비준 "권고대로") — 반례 먼저 ──
        #  LHSC-04: 허용폭 B 는 축별 탐침의 합이라 **포함 경계** (한 구가 다른 구 안에 들어가기 직전 — 중심거리 d 와 |r1 − r2| 의 차가
        #    토큰 반올림 폭 안) 에서 순수 반올림 입력을 초과로 셌고 (Codex: 되읽은 토큰이 경계를 넘어 A_calc = 0 · diff/tol 1.18e6),
        #    d → 0 (같은 경계 · 깊은 겹침) 에서는 B 가 면적보다 커 Hertz · 3e-5 치환도 못 잡았다.  계약: 그런 행은 "면적 불일치" 가 아니라
        #    **지원 범위 밖 (containment_boundary)** 으로 따로 센다 (초과 수에서 뺀다 · 전역 상수 AREA_CHECK_MARGIN 은 그대로).
        #  ⚠ R2 (09-30 밤) 에서 이 계약은 **바뀌었다** — 범위로 빼지 않고 반올림 상자 포괄 구간으로 시험한다 (아래 ㉑″ · 판정은 개정된 값).
        #  LHSC-05: 옛 가드가 `from scripts import plastic_coverage as pc` (module == 'scripts') · `from importlib import import_module as
        #    im; im("plastic_coverage")` (호출 이름이 별칭) 을 통과시켰다.  계약 (a): 순수 기하 `_intersection_disc_area` 는 별도 모듈
        #    `lens_geometry` 로 — 수확기는 plastic_coverage 를 **어떤 모양으로도** 가져오지 않는다 (허용 이름 없음) · 가드는 패키지 경유 ·
        #    별칭 동적 import 도 잡는다 (완전 증명이 아니라 lint — 동적 import 의 비상수 인자는 전부 위반).
        _idr = globals().get('_in_domain_rows')
        _cb = (2.0, 1.0000049, 2.0000051)                                  # Codex rounding_only_false_alarm (×1000): d − |r1−r2| = 4.7e-6
        if _ida is not None:
            _con21b = [(1, 90, 0, _g6(_ida(*_cb)), _g6(_cb[2])),                    # AM_P–SE · 토큰은 반올림만 (r2 → 1.0 · δ → 2.00001) · 경계
                       (91, 92, 0, _g6(np.pi * 0.25 * 0.999999), 0.999999),         # SE–SE · d = 1e-6 (깊은 겹침 = 같은 경계) · Hertz 면적 치환
                       (1, 91, 0, _g6(1.01 * _ida(2.0, 0.5, 0.05)), 0.05)]           # AM_P–SE · 범위 안 · ★ 1 % 틀림 = 초과
        else:
            _con21b = [(1, 90, 0, 0.1, 2.00001), (91, 92, 0, 0.1, 0.999999), (1, 91, 0, 0.1, 0.05)]
        _rows21b = [(1, 2.0, 2.0, 5.0, 2.0, 1), (90, 5.0, 5.0, 5.0, 1.0, 3), (91, 6.0, 5.0, 5.0, 0.5, 3), (92, 8.0, 8.0, 5.0, 0.5, 3)]
        _a21b = _atom_file(tmp, _rows21b, name='atom_2150.liggghts', ts=2150)
        _c21b = _contact_file(tmp, _con21b, name='contact_2150.liggghts', ts=2150, headers=_hd21)
        r21b = harvest(_a21b, _c21b, 3, 'areaboundary', mesh_path=_stl(tmp))
        _ac21b = r21b.get('contact_area_check') or {}
        _all21b, _bk21b = (_ac21b.get('all') or {}), (_ac21b.get('by_pair_kind') or {})
        chk('㉑′ ★ LHSC-04 (R2 에서 개정 · R3a 에서 재개정): 포함 경계 반올림 행은 초과 0 · 깊은 겹침 (d → 0 이 상자 안) Hertz 치환 행은 '
            '**미인증** (생산자 오차 상한이 서지 않는다 · 시험에서 뺀다) · 전체: 비교 3 · 시험 2 · 초과 1 (1 % 행) · 미인증 1 · '
            '실제 하한 0 두 행 (경계 가지 1 + 미인증 행) · AM-SE (초과 1 · 하한 0 1) · SE-SE (초과 0 · 하한 0 1 · 미인증 1)',
            _ac21b.get('status') == STATUS_OK and _ac21b.get('n_compared') == 3 and _all21b.get('n_tested') == 2
            and _all21b.get('n_beyond_tol') == 1 and _all21b.get('n_lower_bound_zero') == 2 and _all21b.get('n_producer_uncertified') == 1
            and (_bk21b.get('AM-SE') or {}).get('n_beyond_tol') == 1 and (_bk21b.get('AM-SE') or {}).get('n_lower_bound_zero') == 1
            and (_bk21b.get('SE-SE') or {}).get('n_beyond_tol') == 0 and (_bk21b.get('SE-SE') or {}).get('n_lower_bound_zero') == 1
            and (_bk21b.get('SE-SE') or {}).get('n_producer_uncertified') == 1 and 'n_boundary_excluded' not in _all21b)
        chk('㉑′ LHSC-04 R2: 옛 범위 분류 함수 `_in_domain_rows` 는 없다 (범위 밖으로 빼던 행도 이제 포괄 구간으로 시험한다)', _idr is None)
        _aenc21 = globals().get('_area_enclosure')
        if _car is not None and _ida is not None and _aenc21 is not None:
            _how21 = _aenc21(_R1, _R2, _D)[3]
            chk(f'㉑′ LHSC-04 R2: 합성 3000 행 (δ/r 1e-7–0.3) 은 전부 꼭짓점 방법 (편도함수 부호 일정 → 정확한 최소 · 최대) · '
                f'방법별 {dict(zip(*np.unique(_how21.astype(str), return_counts=True)))}',
                bool(np.all(_how21.astype(str) == 'corner')))
        else:
            chk('㉑′ LHSC-04 R2: 포괄 구간 함수가 있다', False)
        _bypass = ('from scripts import plastic_coverage as pc\npc.film_area_from_overlap(.1, .5)\n',
                   'from importlib import import_module as im\npc = im("plastic_coverage")\n',
                   'import importlib as il\nil.import_module("plastic_coverage")\n',
                   'from scripts.plastic_coverage import _intersection_disc_area\n',
                   'from plastic_coverage import _intersection_disc_area\n')            # 옛 허용 이름 — 이제 수확기에서는 위반
        chk('㉑′ ★ LHSC-05: 가드가 패키지 경유 · 별칭 동적 import · 점 경로 · 옛 허용 이름을 전부 위반으로 잡는다 · '
            '`lens_geometry` 에서 가져오는 소스는 통과 · 허용 이름 집합은 비어 있다',
            _pcu is not None and all(bool(_pcu(s)[1]) for s in _bypass)
            and not _pcu('from lens_geometry import intersection_disc_area\n')[1] and not PLASTIC_COVERAGE_ALLOWED)
        chk('㉑′ LHSC-05 (a): 교차 원판은 순수 기하 모듈 `lens_geometry` 의 함수 — 수확기 소스에 plastic_coverage 사용 0 (소스 전체 AST)',
            _ida is not None and getattr(_ida, '__module__', '') == 'lens_geometry' and not _pcn and not _pcb)

        # ── ㉑″ ★ Codex LHSC-04 R2 (09-30 밤 재검증 · P2 · 1저자 비준 09-30 낮 "비준이야") — 반례 먼저 ──
        #  R2 반례 (Codex `audit_delta.py` in_domain_rounding_false_alarm): 옛 지원 범위 **안** (gap 3.0e-8 > margin 2.5e-8) 에서 네 값을
        #    정상 `%.6g` 로 적기만 했는데 초과 1 — 축별 탐침 합 B 는 **공동** 반올림 (다른 두 반지름이 한 토큰으로 합쳐짐 · (r1²−r2²)²/d²
        #    항) 을 덮지 못한다 (diff/B 1.332).  "각 입력에 단조" · "포함 경계에서 불연속" · "구간 상한이 서지 않는다" 도 틀렸다.
        #  계약: 허용폭 = 반올림 상자 (x ± h(x)) 위 A 의 **포괄 구간** — 덤프 토큰 구간 [A ± h(A)] 이 그것과 만나지 않을 때만 초과.
        #    범위로 빼지 않는다 (상자가 δ ≤ 0 · d ≤ 0 · 포함에 닿으면 하한 0 으로 시험) · 시험 · 하한 0 · 폭 넓은 행 수를 따로 적는다.
        _aenc = globals().get('_area_enclosure')
        _cx = (0.0012345649, 0.0012345551, 0.00246909)                      # Codex 반례의 참 입력 (sim)
        _cxA = _ida(*_cx) if _ida is not None else float('nan')
        _cxr = (_cac([1, 2], ['AM_P', 'SE'], [_g6(_cx[0]), _g6(_cx[1])], [1], [2], [_g6(_cxA)], [_g6(_cx[2])], [0])
                if _cac is not None else {})
        _cxa = _cxr.get('all') or {}
        chk(f'㉑″ ★ LHSC-04 R2: Codex 반례 (두 반지름 → 한 토큰 0.00123456 · δ 0.00246909 · A {_g6(_cxA):.6g} = 정상 반올림) 는 '
            f'초과 0 · 시험 1 · 폭 넓은 행 1 (깊은 겹침 — 검출력이 약하다고 적는다) · 판정 {_cxa.get("n_beyond_tol")!r}',
            _cxa.get('n_beyond_tol') == 0 and _cxa.get('n_tested') == 1 and _cxa.get('n_wide_enclosure') == 1)
        if _aenc is not None and _ida is not None and _hu is not None:
            #  포괄성: 여섯 영역 (보통 · 깊은 겹침 · 포함 경계 근처 · 거의 같은 반경 d → 0 · 극값 d² ≈ |r1² − r2²| 근처 · δ ≈ 0) 의
            #  토큰 상자마다 꼭짓점 8 + 내부 24 점에서 잰 A (lens_geometry) 가 전부 [lo, hi] 안
            _rg = np.random.default_rng(2104)
            _bx = []
            for _k in range(600):
                _a, _b = _rg.uniform(4e-4, 6e-3), _rg.uniform(4e-4, 6e-3)
                _kd = _k % 6
                if _kd == 0:
                    _dl = 10.0 ** _rg.uniform(-7.0, np.log10(0.3)) * min(_a, _b)
                elif _kd == 1:
                    _dl = _a + _b - 10.0 ** _rg.uniform(-9.0, -5.0)
                elif _kd == 2:
                    _dl = _a + _b - abs(_a - _b) * (1.0 + _rg.choice([-1.0, 1.0]) * 10.0 ** _rg.uniform(-7.0, -2.0))
                elif _kd == 3:
                    _b = _a * (1.0 + 10.0 ** _rg.uniform(-8.0, -5.0))
                    _dl = _a + _b - 10.0 ** _rg.uniform(-9.0, -6.0)
                elif _kd == 4:
                    _dl = _a + _b - np.sqrt(abs(_a * _a - _b * _b)) * (1.0 + _rg.choice([-1.0, 1.0]) * 10.0 ** _rg.uniform(-6.0, -2.0))
                else:
                    _dl = _rg.uniform(-1e-7, 1e-7)
                _bx.append((_g6(_a), _g6(_b), _g6(_dl)))
            _B1, _B2, _BD = (np.asarray(c, dtype=np.float64) for c in zip(*_bx))
            _enc = _aenc(_B1, _B2, _BD)
            _lo, _hi = _enc[0], _enc[1]
            _h1b, _h2b, _hdb = _hu(_B1), _hu(_B2), _hu(_BD)
            _pts = [np.array(s, dtype=np.float64) for s in ((1, 1, 1), (1, 1, -1), (1, -1, 1), (1, -1, -1),
                                                           (-1, 1, 1), (-1, 1, -1), (-1, -1, 1), (-1, -1, -1))]
            _pts += [_rg.uniform(-1.0, 1.0, 3) for _ in range(24)]
            _viol = []
            for _i in range(_B1.size):
                for _s in _pts:
                    _A = _ida(_B1[_i] + _s[0] * _h1b[_i], _B2[_i] + _s[1] * _h2b[_i], _BD[_i] + _s[2] * _hdb[_i])
                    if not (_lo[_i] <= _A <= _hi[_i]):
                        _viol.append((_i % 6, _i))
            chk(f'㉑″ LHSC-04 R2: 포괄 구간은 토큰 상자 안의 모든 점을 담는다 — 여섯 영역 × 100 상자 × 32 점 · 벗어남 {len(_viol)} '
                f'(영역별 {sorted(set(v[0] for v in _viol))})', not _viol)
            #  Codex 가 적은 구간 (손 계산 ≈ [2.66e-6, 4.79e-6]) 과 같은 자리 — 덤프 값 4.27727e-6 을 담고 기하 상한 π·min(r)² 을 넘지 않는다
            _e1 = _aenc(np.array([_g6(_cx[0])]), np.array([_g6(_cx[1])]), np.array([_g6(_cx[2])]))
            chk(f'㉑″ LHSC-04 R2: Codex 반례의 포괄 구간 [{float(_e1[0][0]):.4e}, {float(_e1[1][0]):.4e}] ∋ 4.27727e-6 · 하한 > 2.6e-6 · '
                f'상한 ≤ π·(r+h)² (0 ≤ A ≤ π·min(r1, r2)² — 유한 상한은 늘 있다)',
                float(_e1[0][0]) > 2.6e-6 and float(_e1[0][0]) <= 4.27727e-6 <= float(_e1[1][0])
                and float(_e1[1][0]) <= np.pi * (_g6(_cx[0]) + 5e-9) ** 2 * (1 + 1e-12))
        else:
            chk('㉑″ LHSC-04 R2: 포괄 구간 함수 `_area_enclosure` 가 있다', False)
        chk('㉑″ LHSC-04 R2: 규칙 문자열에 틀린 서술 ("단조" · "불연속" · 축별 탐침 합) 이 없고 포괄 구간 · 하한 0 · 폭 넓은 행을 적는다',
            '단조' not in AREA_CHECK_TOL_RULE and '불연속' not in AREA_CHECK_TOL_RULE and 'Σ_{x∈r1,r2,δ}' not in AREA_CHECK_TOL_RULE
            and '포괄' in AREA_CHECK_TOL_RULE and 'n_lower_bound_zero' in AREA_CHECK_TOL_RULE and 'n_wide_enclosure' in AREA_CHECK_TOL_RULE)

        # ── ㉑‴ ★ Codex LHSC-04 R3a · R3b (09-30 밤 재검증 2 · P2 · 1저자 비준 09-30 밤 "비준이야") — 반례 먼저 ──
        #  R3a: 고정 여유 fp = 32·eps·π·max(r)² 가 "LIGGGHTS 생산자 계산 오차를 덮는다" 는 전역 주장에 반례 — 공개 PUBLIC add_pair 는
        #    r = sqrt(rsq) 뒤 (r−r1−r2)(r+r1−r2)(r−r1+r2)(r+r1+r2)/rsq (거리 인수 곱 / rsq · 음수를 0 으로 안 자름) 라 동심 근접
        #    (r1 = r2 = 0.001 · d = 1e-15) 에서 변조 없이 A 3.142020e-6 > π r² → 6 자리 토큰이 구간 밖 = 초과 1.  완전 포함 · 비접촉에서는
        #    생산 식이 **음수** — 정의역 밖 생산값과 클립된 기준 기하의 의미 차이 (반올림 검사와 다른 사유).
        #  계약: 생산 식 형태를 핀하고 (PRODUCER_AREA_MODEL · 설치 빌드 sha 는 pin 파일) 상자 전체의 절대 오차 상한 E 를 유도해 허용폭에
        #    넣는다 · 상자가 d ≤ 0 에 닿거나 δ 토큰 반폭이 생산자 δ 오차보다 작으면 E 가 서지 않아 **미인증** (n_producer_uncertified ·
        #    시험 · 초과에서 뺀다) · 음수 덤프 면적은 n_area_dump_negative (초과 아님) · 고정 fp 는 없앤다.
        #  R3b: n_power_1pct 는 분모가 검사 대상 A_dump 라 +1 % 치환이 폭 분류까지 바꿨다 (놓치면서 power 1).  계약: 검출 보증
        #    n_detect_1pct = ±1 % 치환의 **토큰 구간**이 허용 구간과 분리 (출력 반올림 2h · E 포함 · A_dump 무관) · 폭 기술량은 lo 기준 ·
        #    n_lower_bound_zero = 실제 lo == 0 · n_boundary_branch = 가지 진입 수.
        _peb = globals().get('_producer_error_bound')
        _pae = globals().get('_producer_abs_error')
        _ppa = globals().get('producer_area_binary64')
        _ppin = globals().get('producer_pin')
        _pam = globals().get('PRODUCER_AREA_MODEL')

        def _cac1(r1, r2, dl, A):                                          # 한 행 (AM_P–SE · 플래그 0) 의 all 그룹
            return ((_cac([1, 2], ['AM_P', 'SE'], [r1, r2], [1], [2], [A], [dl], [0]) if _cac is not None else {}).get('all') or {})
        _u12 = _cac1(0.001, 0.001, 0.002, 3.14202e-6)                      # Codex equal_deep_1e-12 (생산 식 그대로 · 변조 없음)
        _u13 = _cac1(0.001, 0.001, 0.002, 3.1393e-6)                       # equal_deep_1e-13 (아래쪽 오차)
        chk(f'㉑‴ ★ R3a: 동심 근접 (r1 = r2 = 0.001 · δ 토큰 0.002 → 상자가 d ≤ 0 에 닿음) 두 행은 **미인증** — 초과 0 · 시험 0 · '
            f'미인증 1 (옛: 3.14202e-6 이 초과 1) · {_u12.get("n_beyond_tol")!r}/{_u12.get("n_producer_uncertified")!r}',
            all(g.get('n_producer_uncertified') == 1 and g.get('n_beyond_tol') == 0 and g.get('n_tested') == 0 for g in (_u12, _u13)))
        _ng1 = _cac1(0.002, 0.001, 0.0021, -1.5088371383490986e-6)         # Codex contained (생산 식 음수)
        _ng2 = _cac1(0.001, 0.001, -0.0001, -3.2201324699295325e-7)        # Codex no_contact (생산 식 음수)
        chk('㉑‴ ★ R3a: 음수 덤프 면적 (완전 포함 · 비접촉의 생산 식 값) 은 n_area_dump_negative 로 따로 센다 — 초과 0 · 시험 0',
            all(g.get('n_area_dump_negative') == 1 and g.get('n_beyond_tol') == 0 and g.get('n_tested') == 0 for g in (_ng1, _ng2)))
        _nc = _cac1(0.001, 0.001, 0.0, 1e-6)                               # δ = 0 인데 양수 면적 — 검출 유지
        _nz = _cac1(0.001, 0.001, -0.0001, 0.0)
        chk('㉑‴ R3a: 비접촉 (δ = 0 · 음수 δ) 에 0 면적은 통과 · δ = 0 에 양수 면적 (1e-6) 은 여전히 초과 (미인증 아님 · 고정 fp 없이)',
            _nc.get('n_beyond_tol') == 1 and _nc.get('n_producer_uncertified') == 0 and _nz.get('n_beyond_tol') == 0
            and _nz.get('n_area_dump_zero') == 1)
        # R3b — Codex 검출력 반례 (seed 4813 · 431 번째 상자): 정상 토큰과 +1 % 토큰의 분류가 **같아야** 한다 (A_dump 무관)
        _pw = (0.00348428, 0.00164629, 0.00328959)
        _pw_ok, _pw_mut = _cac1(*_pw, 5.81675e-8), _cac1(*_pw, 5.87492e-8)
        chk(f'㉑‴ ★ R3b: Codex 검출력 반례 — 정상 토큰 · +1 % 토큰 둘 다 초과 0 · 폭 넓음 1 (lo 기준) · **검출 보증 0** (옛: 치환 행이 '
            f'power 1) · {(_pw_ok.get("n_detect_1pct"), _pw_mut.get("n_detect_1pct"), _pw_mut.get("n_wide_enclosure"))}',
            all(g.get('n_beyond_tol') == 0 and g.get('n_wide_enclosure') == 1 and g.get('n_detect_1pct') == 0 and 'n_power_1pct' not in g
                for g in (_pw_ok, _pw_mut)))
        # 보증 = 실제 검출: 조밀한 행 (2.0 · 0.5 · 0.05 — ㉑′ 세 번째 행) 은 검출 보증 1 이고 ±1 % 토큰이 실제로 초과
        if _ida is not None:
            _tA = _ida(2.0, 0.5, 0.05)
            _tg = [_cac1(2.0, 0.5, 0.05, _g6(f * _tA)) for f in (1.0, 1.01, 0.99)]
            chk('㉑‴ R3b: 조밀한 행 (2.0 · 0.5 · 0.05) 은 검출 보증 1 · 정상 토큰 초과 0 · +1 % · −1 % 토큰은 실제로 초과 1',
                _tg[0].get('n_detect_1pct') == 1 and _tg[0].get('n_beyond_tol') == 0
                and _tg[1].get('n_beyond_tol') == 1 and _tg[2].get('n_beyond_tol') == 1)
            #  3000 합성 행: 검출 보증 행의 ±1 % 치환은 **전부** 실제 초과 (보증 ⇒ 검출 · 반대 방향은 요구하지 않는다)
            if _car is not None:
                _rows3 = _car(_R1, _R2, _D, _Ad)
                _det3 = (_rows3[5] or {}).get('detect_1pct') if len(_rows3) > 5 else None
                _bp = _car(_R1, _R2, _D, np.asarray([_g6(x) for x in 1.01 * _Ad]))[4]
                _bm = _car(_R1, _R2, _D, np.asarray([_g6(x) for x in 0.99 * _Ad]))[4]
                chk(f'㉑‴ R3b: 합성 3000 행 — 검출 보증 행 {int(_det3.sum()) if _det3 is not None else "?"} 개의 +1 % · −1 % 치환은 전부 초과 · '
                    f'정상 토큰은 초과 0 · 미인증 0',
                    _det3 is not None and _det3.size == _R1.size and bool(np.all(_bp[_det3]) and np.all(_bm[_det3]))
                    and int(_det3.sum()) > 2900 and not bool(_car(_R1, _R2, _D, _Ad)[4].any())
                    and not bool((_rows3[5] or {}).get('uncertified').any()))
        # P3 — n_lower_bound_zero = 실제 lo == 0 · n_boundary_branch = 가지 진입 수
        _z = _cac1(0.002, 0.001, 0.0021, 0.0)                              # Codex 예: zero 가지 · lo 0
        _bd = _cac1(2.0, 1.0000049 if False else _g6(1.0000049), _g6(2.0000051), _g6(_ida(2.0, 1.0000049, 2.0000051)) if _ida else 0.0)
        chk('㉑‴ P3: zero 가지 행 (.002 · .001 · .0021 · A 0) 은 실제 하한 0 = 1 · 경계 가지 0 · 경계 가지 행은 둘 다 1',
            _z.get('n_lower_bound_zero') == 1 and _z.get('n_boundary_branch') == 0
            and _bd.get('n_lower_bound_zero') == 1 and _bd.get('n_boundary_branch') == 1)
        # 생산자 오차 모델 — 공개 add_pair 를 연산 순서대로 옮긴 binary64 스칼라 (DEM 실행 아님) 를 Decimal 60 자리 정확값과 대조:
        #  ① 절대 오차 |A_p − A_e| ≤ E(점) (모델 자체) · ② 6 자리 토큰 경로 전체에서 인증 행의 거짓 초과 0 (허용폭 = 상자 + E + 출력 반올림)
        if _ppa is not None and _pae is not None and _car is not None and _aenc is not None:
            from decimal import Decimal as _Dc, localcontext as _lc
            _PI = _Dc('3.14159265358979323846264338327950288419716939937510582097494459230781640628620899')
            _rg3 = np.random.default_rng(20260930)
            _viol_e, _viol_t, _ncert, _nunc, _ratio = 0, 0, 0, 0, 0.0
            _rel_e = []
            for _k in range(4000):
                _a = 10.0 ** _rg3.uniform(-5.0, -2.0)
                _b = _a * 10.0 ** _rg3.uniform(-1.5, 1.5)
                _m = _k % 6
                if _m == 0:
                    _dl = min(_a, _b) * 10.0 ** _rg3.uniform(-6.0, -0.3)           # 보통 부분 겹침
                elif _m == 1:
                    _dl = min(_a, _b) * _rg3.uniform(0.5, 1.9)                     # 깊은 겹침
                elif _m == 2:
                    _dl = _a + _b - abs(_a - _b) * (1.0 + _rg3.choice([-1.0, 1.0]) * 10.0 ** _rg3.uniform(-9.0, -3.0))   # 포함 경계 근처
                elif _m == 3:
                    _b = _a * (1.0 + 10.0 ** _rg3.uniform(-9.0, -4.0)); _dl = _a + _b - _a * 10.0 ** _rg3.uniform(-12.0, -4.0)  # 동심 근접
                elif _m == 4:
                    _dl = min(_a, _b) * 10.0 ** _rg3.uniform(-9.0, -6.0)           # 아주 얕음
                else:
                    _dl = -min(_a, _b) * 10.0 ** _rg3.uniform(-6.0, 0.0)           # 비접촉 (생산 식 음수)
                _dist = _a + _b - _dl
                if _dist <= 0.0:
                    continue
                _Ap, _dp = _ppa(_a, _b, _dist)                                     # 생산 식 (binary64 · 연산 순서 보존)
                with _lc() as _cx3:
                    _cx3.prec = 60
                    _A_, _B_, _R_ = (_Dc(float(v)) for v in (_a, _b, _dist))
                    _Ae = -_PI / 4 * ((_R_ - _A_ - _B_) * (_R_ + _A_ - _B_) * (_R_ - _A_ + _B_) * (_R_ + _A_ + _B_)) / (_R_ * _R_)
                    _de = _A_ + _B_ - _R_
                    _fs = [(abs(_de), abs(2 * _A_ - _de), abs(2 * _B_ - _de), abs(2 * _A_ + 2 * _B_ - _de), _R_)]
                    _E = _pae(*[(float(v), float(v)) for v in _fs[0]])            # 점 (상자 폭 0) 의 절대 오차 상한
                    _err = abs(_Dc(float(_Ap)) - _Ae)
                    if _err > _Dc(float(_E)):
                        _viol_e += 1
                    if _Ae > 0:
                        _rel_e.append(float(_Dc(float(_E)) / _Ae))
                        _ratio = max(_ratio, float(_err / _Dc(float(_E))) if _E > 0 else float('inf'))
                #  토큰 경로 — 인증된 행은 거짓 초과가 없어야 한다 (변조 없음)
                _t = (_g6(_a), _g6(_b), _g6(_dp), _g6(_Ap))
                _rw = _car(np.array([_t[0]]), np.array([_t[1]]), np.array([_t[2]]), np.array([_t[3]]))
                _ex = _rw[5] if len(_rw) > 5 else {}
                if bool(_ex.get('uncertified', np.array([True]))[0]):
                    _nunc += 1
                elif _t[3] >= 0.0:
                    _ncert += 1
                    _viol_t += int(bool(_rw[4][0]))
            chk(f'㉑‴ ★ R3a: 생산자 오차 모델 — 공개 add_pair binary64 재현 4000 점 (여섯 영역) 의 |A_p − A_e| ≤ E(점) 위반 {_viol_e} · '
                f'실측/상한 최대 비 {_ratio:.3g} (< 1 이어야) · 헐겁지 않은지: E/A 중앙 {np.median(_rel_e):.1e} < 1e-8 (얕은 접촉은 E/A ∝ S/δ · '
                f'출력 반올림 5e-7 의 1/1000 아래)',
                _viol_e == 0 and _ratio < 1.0 and float(np.median(_rel_e)) < 1e-8)
            chk(f'㉑‴ ★ R3a: 6 자리 토큰 경로 — 인증 행 {_ncert} 의 거짓 초과 {_viol_t} (0 이어야) · 미인증 {_nunc} (동심 근접 · 상자가 d ≤ 0 · '
                f'δ 반폭 < 생산자 δ 오차) — 미인증은 초과가 아니라 따로 센다',
                _viol_t == 0 and _ncert > 2300 and 0 < _nunc < 1500)
        else:
            chk('㉑‴ R3a: 생산자 오차 모델 함수 (producer_area_binary64 · _producer_abs_error · _producer_error_bound) 가 있다', False)
        # pin 파일 — 설치 빌드의 add_pair 소스 sha 를 대조하기 전에는 "핀 안 됨" 을 결과에 적는다 (짐작하지 않는다)
        if _ppin is not None:
            import json as _js
            _env_prev = os.environ.pop('LHS_PRODUCER_PIN_FILE', None)
            try:
                _pin0 = _ppin(os.path.join(tmp, 'no_such_pin.json'))
                _pf = os.path.join(tmp, 'pin.json')
                with open(_pf, 'w', encoding='utf-8') as _fh:
                    _js.dump({'schema': 'liggghts_add_pair_pin/1', 'source_file': 'src/compute_pair_gran_local.cpp',
                              'sha256': 'ab' * 32, 'host': 'wsl', 'date': '2026-09-30', 'formula_confirmed': True,
                              'build': 'lmp_serial'}, _fh)
                _pin1 = _ppin(_pf)
                with open(_pf, 'w', encoding='utf-8') as _fh:
                    _js.dump({'schema': 'liggghts_add_pair_pin/1', 'source_file': 'x', 'sha256': 'zz', 'formula_confirmed': True}, _fh)
                _pin2 = _ppin(_pf)
                os.environ['LHS_PRODUCER_PIN_FILE'] = _pf
                _r_env = (_cac([1, 2], ['AM_P', 'SE'], [2.0, 0.5], [1], [2], [_g6(_ida(2.0, 0.5, 0.05))], [0.05], [0])
                          if (_cac is not None and _ida is not None) else {})
            finally:
                os.environ.pop('LHS_PRODUCER_PIN_FILE', None)
                if _env_prev is not None:
                    os.environ['LHS_PRODUCER_PIN_FILE'] = _env_prev
            _pm = _r_env.get('producer_model') or {}
            chk('㉑‴ R3a: pin 파일 — 없음 → pinned False + 사유 · 형식 맞음 → True + sha 회신 · sha 형식 깨짐 → False + 사유 · 결과의 '
                'producer_model 에 식 · 출처 · 오차 상한 문장 · pinned 가 실린다',
                _pin0.get('pinned') is False and _pin0.get('reason') and _pin1.get('pinned') is True
                and (_pin1.get('pin') or {}).get('sha256') == 'ab' * 32 and _pin2.get('pinned') is False and _pin2.get('reason')
                and _pm.get('installed_build_pinned') is False and all(k in _pm for k in ('formula', 'source', 'error_bound'))
                and isinstance(_pam, dict) and 'add_pair' in _pam.get('source', ''))
        else:
            chk('㉑‴ R3a: producer_pin 함수가 있다', False)
        chk('㉑‴ R3a · R3b: 규칙 문자열 — 생산자 오차 모델 · 미인증 · 음수 면적 · 검출 보증 (n_detect_1pct) 을 적고 n_power_1pct · 고정 32·eps 는 없다',
            'n_producer_uncertified' in AREA_CHECK_TOL_RULE and 'n_detect_1pct' in AREA_CHECK_TOL_RULE and 'n_area_dump_negative' in AREA_CHECK_TOL_RULE
            and 'n_boundary_branch' in AREA_CHECK_TOL_RULE and 'n_power_1pct' not in AREA_CHECK_TOL_RULE and '32·eps' not in AREA_CHECK_TOL_RULE)

        # ── ㉒ item 3 (09-29 · 1저자 "권고대로") — 접촉 행의 문: 중복 · 자기쌍 **거부** · 고아 행 **기록** · 반례 먼저 ──
        #  ★ 반례: 같은 AM–SE 행이 두 번 — 옛 코드는 면적을 두 번 더해 AM_S 피복률 25 → 50 % 를 status OK 로 냈다.
        _rows22 = [(1, 5.0, 5.0, 5.0, 1.0, 2), (90, 5.0, 5.0, 6.4, 0.5, 3)]
        _a22 = _atom_file(tmp, _rows22, name='atom_2200.liggghts', ts=2200)
        _c22 = {nm: _contact_file(tmp, rows, name=f'contact_22{i:02d}.liggghts', ts=2200) for i, (nm, rows) in enumerate((
            ('ok', [(1, 90, np.pi)]),
            ('dup', [(1, 90, np.pi), (1, 90, np.pi)]),                 # a–b 두 번
            ('rev', [(1, 90, np.pi), (90, 1, np.pi)]),                 # a–b 와 b–a
            ('self', [(1, 90, np.pi), (90, 90, 0.1)]),                 # 자기쌍
            ('orph', [(1, 90, np.pi), (1, 999, np.pi), (777, 90, 0.2)])))}   # 고아 행 둘 (없는 id 999 · 777)
        r22 = harvest(_a22, _c22['ok'], 3, 'gate_ok', mesh_path=_stl(tmp))
        chk('㉒ item 3: 깨끗한 덤프 — 피복률 25 % · 문 기록 (행 1 · 고아 0 · 중복 0 · 자기쌍 0)',
            abs(r22['coverage_AM_S_hertz_pct'] - 25.0) < 1e-12
            and (r22.get('contact_gate') or {}).get('n_rows') == 1 and (r22.get('contact_gate') or {}).get('n_orphan_rows') == 0
            and (r22.get('contact_gate') or {}).get('n_dup_rows') == 0 and (r22.get('contact_gate') or {}).get('n_self_rows') == 0)
        neg('㉒ item 3 ★반례: 같은 AM–SE 행 두 번 → 거부 (옛 코드: 피복률 25 → 50 %, status OK)',
            lambda: harvest(_a22, _c22['dup'], 3, 'gate_dup', mesh_path=_stl(tmp)))
        neg('㉒ item 3: a–b 와 b–a (무순서 중복) → 거부',
            lambda: harvest(_a22, _c22['rev'], 3, 'gate_rev', mesh_path=_stl(tmp)))
        neg('㉒ item 3: 자기쌍 (90–90) → 거부',
            lambda: harvest(_a22, _c22['self'], 3, 'gate_self', mesh_path=_stl(tmp)))
        r22o = harvest(_a22, _c22['orph'], 3, 'gate_orph', mesh_path=_stl(tmp))
        _g22 = r22o.get('contact_gate') or {}
        chk('㉒ item 3: 고아 행은 거부하지 않고 **센다** — 행 3 · 고아 행 2 · 없는 id 2 (999 · 777) · 피복률은 고아 없는 덤프와 같다',
            _g22.get('n_rows') == 3 and _g22.get('n_orphan_rows') == 2 and _g22.get('n_orphan_ids') == 2
            and r22o['coverage_AM_S_hertz_pct'] == r22['coverage_AM_S_hertz_pct'])
        _chz = coverage_hertz(np.array([1, 90]), np.asarray(['AM_S', 'SE'], dtype=object), np.array([1.0, 0.5]),
                              [1, 1, 777], [90, 999, 90], [np.pi, np.pi, 0.2])
        chk('㉒ item 3: coverage_hertz 도 건너뛴 고아 행 수를 돌려준다 (문의 수와 같은 정의 · 새 키만)',
            _chz.get('n_orphan_rows') == 2 == _g22.get('n_orphan_rows'))
        _pdc = globals().get('_pair_dup_counts')
        _sd22 = scan_contact_dump(_c22['rev'])
        chk('㉒ item 3: 중복 정의는 scan_contact_dump 와 하나 (`_pair_dup_counts`) — a–b · b–a 덤프에서 (고유 1 · 중복 쌍 1 · 초과 행 1 · 자기쌍 0)',
            _pdc is not None and _pdc(np.array([1, 90]), np.array([90, 1]))
            == (_sd22['n_unique_pairs'], _sd22['n_dup_pairs'], _sd22['n_dup_rows'], _sd22['n_self_pairs']) == (1, 1, 1, 0))
        #  변이 대조 (⑫ 와 같은 방식) — 문을 무력화하면 반례가 **실제로** 뚫려 피복률이 두 배가 된다 = 음성대조가 살아있다
        _keep22 = getattr(M, 'contact_gate', None)
        _mut22 = None
        if _keep22 is not None:
            M.contact_gate = lambda ids, a, b: {}
            try:
                _mut22 = M.harvest(_a22, _c22['dup'], 3, 'gate_mut', mesh_path=_stl(tmp))
            except Exception:                                              # noqa: BLE001
                _mut22 = None
            finally:
                M.contact_gate = _keep22
        chk('㉒ item 3: 변이 대조 — 문을 끄면 같은 행 두 번이 통과해 피복률 50 % (옛 코드의 거동) · 문이 그것을 막고 있다',
            _mut22 is not None and abs(_mut22['coverage_AM_S_hertz_pct'] - 50.0) < 1e-12)

    print()
    if _FAILS:
        print(f'✗ {len(_FAILS)} 건 실패')
        for f in _FAILS:
            print('   -', f)
        return 1
    print('✓ 전부 통과   ⚠ 이 통과는 **계약이 도구에 박혔다**는 뜻이지 '
          '실제 130 배치가 깨끗하다는 뜻이 아니다')
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(
        description='LHS 130 구조 디스크립터 수확 — 판정문 §7 계약 6개를 고정한다')
    ap.add_argument('--atom')
    ap.add_argument('--contact')
    ap.add_argument('--mesh', help='플래튼 STL (--plate-z 와 택일)')
    ap.add_argument('--plate-z', type=float, help='플래튼 높이 직접 지정 (--mesh 와 택일)')
    ap.add_argument('--n-types', type=int, choices=(2, 3),
                    help='필수 — 자동 추론은 거부한다 (AM_P 가 0개면 오사상된다)')
    ap.add_argument('--deck', help='필수 — 이 케이스의 LIGGGHTS 덱.  바닥 벽 (`zplane`) 이 0 인지 확인한다 (LHS-12)')
    ap.add_argument('--case', default='')
    ap.add_argument('--allow-any-bc', action='store_true')
    ap.add_argument('--n-pairs', type=int, default=N_TAU_PAIRS)
    ap.add_argument('--out', help='결과 JSON 경로')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)

    if a.selftest:
        return selftest()
    if not (a.atom and a.contact and a.n_types and a.deck):
        ap.error('--atom · --contact · --n-types · --deck 는 필수다 (--deck: 바닥 벽 위치를 덱에서 확인한다, LHS-12)')
    try:
        r = harvest(a.atom, a.contact, a.n_types, a.case or os.path.basename(a.atom),
                    plate_z=a.plate_z, mesh_path=a.mesh,
                    allow_any_bc=a.allow_any_bc, n_pairs=a.n_pairs, deck_path=a.deck)
    except BedRefusal as e:
        print(f'거부 — {e}', file=sys.stderr)
        return 2
    txt = json.dumps(r, ensure_ascii=False, indent=1, default=str)
    if a.out:
        open(a.out, 'w', encoding='utf-8').write(txt + '\n')
        print(f'→ {a.out}')
    else:
        print(txt)
    return 0


if __name__ == '__main__':
    sys.exit(main())
