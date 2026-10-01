# LHS 구조 디스크립터 — 배포 v1.1 (2026-10-01 · J20-p · J20-q · ML 인계본 J20-r)

> 수영 님 ML 용 **구조 디스크립터 최소 단위**.  DEM (LIGGGHTS) 으로 300 MPa 압밀한 복합 양극 침대를 설계 입력 → 구조 값으로 정리한 표다.
> **이 README 하나로 ML 에 쓸 수 있게 썼다** — 열 역할 (§2) · 지킬 규약 (§3) · 오해 주의 (§4) · ML 적용 안내 (§5) · AI 프롬프트 (§8).
> 정본 (전체 열 · 내부 QC · 출처 해시) = `docs/data/lhs_handover_20261001.csv` · `lhsx_handover_20261001.csv` · 판정 기록 = `docs/reviews/lhs_handover_judgments_20260924.md` (J20 계열).

## 외부 검토 (Codex 최종 · 2026-10-01) — 먼저 읽을 것

- **판정: 고정된 v1.1 DEM 계산값 전달 = GO · 실제 전극의 물리적 학습 타깃 인증 = HOLD 유지 · 새 P1 없음** (P2 다섯 · P3 하나 — 원장 `LREL-01`~`06`).
  판정문 `docs/reviews/codex_lhs_release_final_verdict_20261001.md` · 증거 `docs/reviews/codex_lhs_release_final_evidence_20261001/`.
- 검토가 확인한 것: 커밋된 중간 산출물 → 인계표 재생성이 **바이트까지 일치** · 194 행 전수 대조 · 키 중복 0 · 누락 0 · 항등식 산술 전수 일치 · 적격성 표지 재계산 일치.
- 검토 범위 밖: 원시 덤프 재감사 · 실행 바이너리 · 목표 압력 도달 인증 · 실험 검증.  관문 반례 (음수 이온 분할 · 적격성 누락 · 중복 행) 는 **현재 배포값에는 없다** — 앞으로 다시 생성할 도구의 보증 문제다.
- 고정 파일 (이 README 개정 뒤에도 CSV · 열 사전은 한 바이트도 바뀌지 않았다):

  | 파일 | 행 × 열 | sha256 |
  |---|---|---|
  | `lhs_release_20261001_v11.csv` | 130 × 89 | `b12ca6206e04d6aba181dacf19c666a91e4adb27f05176ac530a1eee1d96a635` |
  | `lhsx_release_20261001_v11.csv` | 64 × 88 | `39adf263f674ccdb073a5c2e139b63581c3aadd78c873d97a99cc0dc07031ffc` |

> **인계 문단 (판정문 §8 그대로)**: v1.1은 커밋된 중간 산출물에서 전수 재생성됐으며, 정본·배포·열 사전이 일치한다. 이는 고정 DEM 규약의 구조 디스크립터 자료이지 실험적으로 검증된 물리 타깃 표가 아니다. 적격성 HOLD는 130 중 59행, 확장 64 중 62행이다. H_mc·φ_mc는 등가 장부량, 이온 고립은 경계 띠 기준 그래프 지표, τ는 경계 쌍 Δz 기준 기하 최단경로 지표다. 원시 덤프의 재감사·실행 바이너리·완료 압력은 이번 검토에 포함되지 않았다. 타깃의 항등식·상수·빈칸 규약과 HOLD 상태를 보존해서 사용한다.

## 0. 바뀐 것

| 언제 | 무엇 | 왜 |
|---|---|---|
| v1 → v1.1 | **이온 경로 고립** 9 열 · **가장 큰 SE 덩어리** 2 열 · `thickness_wall_gap_um` · **적격성 표지** 3 열 | v1 은 고립 **위험** 만 있었다 · 비관통 침대의 연속값 · 측정 두께 · v1 에서 HOLD 표지가 빠져 있었다 (`REL-01`) |
| v1 → v1.1 | 접촉 단계 원천 = `d1ec42fba` 재실행 | F1 근접쌍 수정 (`LHS-22`) 뒤 세대 · 배포 열 값 변화 0 |
| **10-01 (이 판)** | README 만 개정 — Codex 최종 판정 반영 · ML 적용 안내 (§5) · 용어 **Tortuosity (기하학적)** · **Coverage (DEM)** | τ 분모 · 이온 고립 문구 정정 (`LREL-05`) · 질량 % 분모 · 상수 문구 · MC 오차 · 15:1 (`LREL-06`) · HOLD · 등가 장부량 문구 (판정문 §4 · §5) |

v1 (`docs/data/lhs_release_20261001/`) 은 그대로 둔다 — v1 의 74 · 73 열은 v1.1 에서 값 · 순서가 한 글자도 안 바뀌었다.

## 1. 파일

| 파일 | 행 × 열 | 내용 |
|---|---|---|
| `lhs_release_20261001_v11.csv` | 130 × 89 | LHS 설계 130 침대 (bimodal 100 · mono AM_P 15 · mono AM_S 15) |
| `lhsx_release_20261001_v11.csv` | 64 × 88 | 확장 64 침대 (bimodal 48 · mono 16) — **전부 SE-rich** (SE/고체 부피 0.51–0.85 · 분포가 130 과 다르다) · `loading_mAh_cm2` 열 없음 · 설계 열은 `scripts/lhsx_design_adapter.py` 가 확장 설계에서 만들었다 (mono 는 `ps_frac` 0/1 · 없는 상 칸 빈칸으로 접음) |
| `*_columns.tsv` | 열마다 한 줄 | 뜻 · 분모 · 주의 · 판정 근거 (정본 인계표 열 사전과 같은 줄 · 이 README 와 다르면 **이 README 가 정정판**이다 — `LREL-06`) |

한 행 = 한 침대 (300 MPa 압밀 뒤 한 프레임).  `case_id` 가 키다.

## 2. 열 역할 (두 CSV 의 **모든** 열 — 130: 89 · 64: 88 · 빠진 열 0 으로 검산)

| 역할 | 열 | 130 · 64 |
|---|---|---|
| **ID** (특징 금지) | `case_id` | 1 · 1 |
| **적격성 표지** (특징 금지 · 타깃 적격성 · 진단용) | `physical_target_status` · `hold_reason_codes` · `boundary_state` | 3 · 3 |
| **상수** (특징 · 타깃 금지) | 130: `loading_mAh_cm2` 2.0 · `pressure_MPa` 300 · `e_se_gpa` 1.35 · `rve_um` 50 / 64: `pressure_MPa` · `e_se_gpa` · `rve_um` (+ 64 에서 전 행 같은 값: `se_rich` = True · `n_large_components` = 1 · `ionic_dead_pct` = 0.0) | 4 · 3 |
| **자유 설계 노브** (X) | `am_pct` (**고체 중 AM 질량 %**) · `ps_frac` (**AM 중 AM_P 질량 몫** — AM_P · AM_S 밀도가 같아 부피 몫과 같다 · 개수 몫 아님) · `d_am_p_um` · `d_am_s_um` · `d_se_um` | 5 · 5 |
| **설계 유도 표현** (X 의 중복 — 같이 넣어도 정보 안 늘어남) | `block` · `ps_label` · `r_AM_P_um` · `r_AM_S_um` · `r_SE_um` · `size_ratio_P_over_S` · `size_ratio_AM_over_SE` | 7 · 7 |
| **실측 입자 수** (결과 — 설계 → 구조 예측에서 X 로 쓰면 누설) | `n_AM_P_measured` · `n_AM_S_measured` · `n_SE_measured` | 3 · 3 |
| **Y1 두께 · 기공 · 분율** | `thickness_wall_gap_um` · `thickness_mass_conserving_um` · `porosity_union_exact_pct` · `se_rich` · `se_of_solid_vol` · `phi_se_mass_conserving` · `phi_am_mass_conserving` | 7 · 7 |
| **Y2 Coverage (DEM)** | `coverage_AM_P_hertz_pct` · `coverage_AM_S_hertz_pct` · `coverage_AM_total_hertz_pct` | 3 · 3 |
| **Y3 접촉 개수 · CN** | `area_AM_P_AM_P_n` · `area_AM_P_AM_S_n` · `area_AM_P_SE_n` · `area_AM_S_AM_S_n` · `area_AM_S_SE_n` · `area_AM전체_SE_n` · `area_SE_SE_n` · `se_se_cn` · `se_se_cn_std` · `am_am_cn` · `am_am_cn_std` · `am_am_n_contacts` | 12 · 12 |
| **Y4 AM–SE CN · 고립 위험** | `am_se_cn_{mean,surface_weighted,std,median,max}` · `AM_P_se_cn_{mean,std,median,max}` · `AM_S_se_cn_{…}` · `am_vulnerable_pct` · `AM_P_vulnerable_pct` · `AM_S_vulnerable_pct` | 16 · 16 |
| **Y5 관통 · Tortuosity (기하학적)** | `percolation_pct` · `top_reachable_pct` · `n_components` · `n_large_components` · `se_se_cn_perc` · `se_se_cn_n_perc` · `tortuosity_SE_wall` · `tortuosity_SE_wall_median` | 8 · 8 |
| **Y6 이온 경로 고립** | `ionic_active_pct` · `am_ionic_isolated_pct` · `ionic_dead_pct` · `ionic_no_se_pct` · `{AM_P,AM_S}_ionic_{active,dead,no_se}_pct` | 10 · 10 |
| **Y7 SE 덩어리** | `se_largest_comp_frac` · `se_largest_comp_wall_span_frac` | 2 · 2 |
| **Y8 벽 접촉** (결과 · 벽 효과 설명 변수) | `wall_touch_frac_{SE,AM_P,AM_S,AM}_{floor,plate}` | 8 · 8 |

## 3. 꼭 지킬 규약

1. **빈칸 = 없음 (N/A) 이지 0 이 아니다.**  ① mono 침대의 없는 상 칸 (130: 30 행 중 상마다 15 · 64: 16 행 중 8) ② 관통하지 않은 침대의 `se_se_cn_perc` · `se_se_cn_n_perc` · `tortuosity_SE_wall(_median)` (130 중 24 · 64 중 0) ③ `hold_reason_codes` 의 빈칸 = 사유 없음 (OK 행).
   0 으로 채우지 말 것.  단 접촉 개수 `area_<쌍>_n` 의 0 은 **측정된 0** 이다.
2. **mono 침대의 상별 칸 = 단일 AM 값** (전체 열과 같은 값 · 설계 `block` 이 상을 정한다).
3. **항등식으로 묶인 열은 독립 타깃이 아니다** — 이 README 개정 때 두 CSV 전 행에서 다시 검산했다 (최대 오차 1.5e-11 · 대부분 0):
   - `porosity_union_exact_pct/100 + phi_se_mass_conserving + phi_am_mass_conserving = 1`
   - `phi_se_mass_conserving = (1 − porosity_union_exact_pct/100) × se_of_solid_vol` ⇒ ε 와 SE 몫이 정해지면 φ 둘이 정해진다 (판정문 §5)
   - `se_se_cn = 2·area_SE_SE_n / n_SE_measured` · `am_am_cn = 2·am_am_n_contacts / N_AM` · `am_se_cn_mean × N_AM = area_AM전체_SE_n` (N_AM = 두 상 실측 수 합) · `AM_x_se_cn_mean × N_x = area_AM_x_SE_n`
   - `se_se_cn_n_perc = percolation_pct × n_SE_measured / 100`
   - `ionic_active_pct + ionic_dead_pct + ionic_no_se_pct = 100` (상별도 · **자유도 둘**) · `am_ionic_isolated_pct = 100 − ionic_active_pct`
   - `am_se_cn_mean` · `coverage_AM_total_hertz_pct` 는 상별 값의 **실측 유효 입자 수 가중평균** · `am_se_cn_surface_weighted` 는 반경² 가중 (다른 estimand)
   - ⚠ 생성기 관문이 대부분을 행마다 검사하지만 `coverage_AM_total` 가중평균은 검사 밖이다 (`DESC-07`).
4. **개수 열은 총량**이다 (`area_*_n` · `am_am_n_contacts` · `n_components` · `n_*_measured`) — 두께 · 입자 수에 비례하므로 입자당 · 부피당으로 나눠 쓸 것.
5. **CN · 비율 열에는 벽 효과가 섞여 있다** — 벽 · 플래튼에 닿은 입자는 그쪽 이웃이 없다 (분모에는 벽 입자 포함 · 벽 자체는 이웃으로 안 셈) → `wall_touch_frac_*` 를 함께 볼 것.
6. **상수 열은 특징이 아니다** (§2 표) — 고정 상자 (50 µm) · 고정 압력 (300 MPa) · 고정 SE 강성 · (130) 고정 적재량 안의 예측이다.  압력 · 상자 · 강성 · 적재량의 영향은 이 데이터로 배울 수 없다.
   64 에서는 `n_large_components` 가 **전부 1**, `ionic_dead_pct` 가 **전부 0.0** 이다 (따로 적는다 — 붙여 쓰지 않는다).
7. **적격성 HOLD (판정문 §4 문안)** — *이 표는 고정된 DEM 규약이 낸 수치적 구조량이다.  HOLD 행도 계산값으로 보존하지만 실제 전극의 물리 타깃으로 인증하지 않는다.  OK 는 기록된 경계 이탈/음수 구 부피 합 기공률 조건이 없다는 뜻이지 물리 검증 완료가 아니다.  HOLD 포함·제외 분석은 별도 민감도 결과로 보고하며, 그 비교 자체를 타당성 증거로 쓰지 않는다.*
   - `boundary_state` — 바닥 (z = 0) · 플래튼 평면 기준: **CENTER_CROSSED** = 중심이 평면을 넘은 입자가 있다 · **FULLY_OUT** = 통째로 평면 밖인 입자가 있다 · **INSIDE** = 없다.  130: INSIDE 87 · CENTER_CROSSED 27 · FULLY_OUT 16 / 64: 53 · 6 · 5.
   - `hold_reason_codes` — **BOUNDARY_CENTER_OUT** · **NEGATIVE_POROSITY** (구 부피 합 기공률 < 0 = 겹침이 큰 침대 · 배포 기공률은 정확 union 이라 양수) · `|` 로 잇는다.
   - `physical_target_status` — 130: **OK 71 · HOLD 59** (BOUNDARY 41 · NEGATIVE 16 · 둘 다 2) / 64: **OK 2 · HOLD 62** (NEGATIVE 51 · 둘 다 9 · BOUNDARY 2).
   - 쓰는 법: 행을 **지우거나 빈칸으로 덮지 않는다**.  `model_descriptor` (DEM 산출물 에뮬레이터 — HOLD 포함 가능) 와 `physical_target_candidate` (HOLD 불허 · OK 도 실험 타당성 아님) 를 **명시적으로 구분**한다.  확장 64 단독 물리 타깃 모델은 OK 2 행으로 정당화할 수 없다.  QC 상태를 일반 X 로 넣어 "모델이 흡수하게" 하지 않는다 (계산 결과에서 나온 사후 정보다).
   - HOLD 의 **인과적 오차 크기는 현 자료로 계산할 수 없다** (경계를 고친 반사실 결과가 없다 · OK/HOLD 평균 차이는 조성 · 입경 차이와 섞여 있다) — 영향권은 porosity 한 열이 아니라 **모든 계산 구조 타깃의 물리적 해석**이다.
8. **다른 코퍼스와 섞지 말 것** — 웹앱의 옛 케이스 모음 (291 행 · 구 부피 합 porosity · d_am 0 행 · MPM/DEM 혼합) 과는 규약이 다르다 (`DESC-08`).  130 과 64 를 함께 쓸 때도 데이터셋 표지를 둔다.

## 4. 이름과 뜻이 다른 곳 (오해 주의)

| 열 | 실제 뜻 |
|---|---|
| `coverage_*_hertz_pct` = **Coverage (DEM)** | 이름의 hertz 는 물려받은 이름.  **각 AM 의 SE 접촉 원판 면적 합 / (구 표면적 − AM–AM 접촉 원판 면적 합)** 을 입자별로 구해 평균한 것 (DEM 겹침 기하 · LIGGGHTS 접촉 면적) — 원래 구 전체 표면적 기준이나 표면 패치 합집합 면적과 **같지 않다**.  소성 보정 (physics) 면적은 안 넘긴다 (SE 많은 침대에서 100 % 에 붙는다 · J20-m).  현 자료 cap · 분모 무효 0/194 |
| `porosity_union_exact_pct` | 입자 겹침을 뺀 합집합 기준 기공률 (몬테카를로 · 세 입자 이상 겹침까지).  **exact = 정의가 쌍 렌즈 근사가 아니라는 뜻이지 MC 오차가 0 이라는 뜻이 아니다** — ε 의 MC 표준오차 130: 0.01194–0.02264 %p · 64: 0.01133–0.01461 %p (마지막 소수 자리를 측정 정밀도로 인용하지 말 것) |
| `thickness_wall_gap_um` ↔ `thickness_mass_conserving_um` | **벽 간격** = 같은 프레임의 플래튼 − 바닥 (측정값).  **H_mc 는 nominal 구 부피와 MC union 기공률을 함께 만족시키도록 정의한 등가 장부 두께다.  원래 침대의 측정 두께 또는 경계 결함을 고친 예측이 아니다.  φ_mc 는 이 가상 용적에서의 nominal 상분율이다** (판정문 §5).  H_mc / H_gap = 130: 1.0153–1.1139 (중앙 1.0430) · 64: 1.0741–1.1533 (중앙 1.1181).  "실제 두께" 는 벽 간격 |
| `*_vulnerable_pct` ↔ `am_ionic_isolated_pct` | 고립 **위험** (SE 접촉 0–1 개) ↔ 경로 기준 고립 (= 100 − `ionic_active_pct`).  130 비관통 24: 경로 기준 고립 61.4–96.9 % · 예 `lhs00_018` 위험 0.09 % ↔ 85.4 % |
| `am_ionic_isolated_pct` · `ionic_active_pct` | **이온 경로 고립은 등록된 상단 2r 경계 띠와 SE 접촉 그래프로 연결되지 않은 AM 의 비율이다.  실제 분리막 접촉, 계면저항 및 이온 전류는 계산하지 않는다** (판정문 `LREL-05` 문안).  위 띠에 앉았지만 위 평면에 닿지 않은 SE 도 "도달" 로 센다 |
| `percolation_pct` | 위 · 아래 가장자리 띠 (입자 반지름 2 배) 를 **둘 다** 잇는 SE 덩어리에 속한 SE 비율.  그래프 연결이지 전류 계산이 아니다.  **0.0 = 잇는 덩어리가 없다 (진짜 0)** · 일반 함수에는 띠 폴백 (L1/L2) 이 남아 있다 — 현 배포는 전부 L0 (감사 CLEAN) 이지만 미래 침대의 보증은 아니다 |
| `top_reachable_pct` | 위 띠에 닿는 SE 기준 — 외톨이 SE 도 센다.  top_reachable ≥ percolation 이 늘 성립 |
| `n_components` | SE 덩어리 수 — **외톨이 SE (접촉 0) 도 한 덩어리**.  `n_large_components` 의 문턱 10 은 출처 없는 코드 상수 |
| `tortuosity_SE_wall(_median)` = **Tortuosity (기하학적)** | **τ 는 벽 인접 띠에서 선택한 같은 성분의 SE 중심 쌍에 대해, 기하 최단경로 길이를 해당 쌍의 z 방향 중심 간격으로 나눈 값이다.  최대 200 쌍의 평균/중앙값을 각각 보고하며 수송 τ (tortuosity factor) 가 아니다** (판정문 `LREL-05` 문안 · 분모는 두께가 아니다).  열 이름의 wall = 바닥 · 플래튼 **경계 띠**.  [1, 20) 밖 절단 0/194 · 130: 1.29–4.15 · 64: 1.26–1.60 |
| `se_largest_comp_frac` · `_wall_span_frac` | 가장 큰 = **SE 수** 기준 덩어리 (가장 멀리 뻗은 덩어리가 아닐 수 있다 — "관통에 얼마나 가까운가" 의 유일한 순위로 쓰지 말 것).  폭은 입자 **표면** 기준 z 폭 / 벽 간격이라 관통 침대는 1 을 조금 넘는다 (130: 1.011–1.045 · 64: 1.023–1.062) · 비관통 24: 비율 0.002–0.908 · 폭 0.11–0.96 |

## 5. ML 적용 안내 (판정문 §7 정리)

**5-1. 무엇을 X, 무엇을 Y 로**
- X = §2 의 **자유 설계 노브 5 개** (`am_pct` · `ps_frac` · `d_am_p_um` · `d_am_s_um` · `d_se_um`).  설계 유도 표현 (반경 · 크기비 · `block` · `ps_label`) 은 같은 정보의 재표현이다 — 넣는다면 독립 정보가 늘었다고 말하지 말 것.  mono 행의 없는 상 지름은 빈칸이므로, 모델이 결측을 못 받으면 `block` 을 함께 두고 결측 표지 열을 따로 만든다 (0 대입 금지).
- Y = §2 의 Y1–Y7 (Y8 은 결과지만 벽 효과 설명 변수로도 쓴다).  **항등식으로 정해지는 열은 한 묶음에서 하나만 독립 타깃으로 센다** (§3-3) — 예: ε 와 `se_of_solid_vol` 이 있으면 φ 둘은 계산된다 · N 이 알려지면 쌍 수 ↔ CN 평균은 같은 정보다 · 이온 분할은 자유도 둘.
- **누설 금지**: 설계 → 구조 예측에서 시험 행의 **실측** 입자 수 (`n_*_measured`) · 두께 · CN 을 X 로 쓰면 타깃 누설이다.  그런 값을 X 로 쓰는 문제는 inverse / conditional model 로 **이름을 붙여** 따로 보고한다.
- 적격성 표지 · ID 는 X 가 아니다 (§3-7).

**5-2. 권장 과제와 최소 기준선**

| 과제 | 대상 | 최소 기준선 |
|---|---|---|
| A. 설계 → 구조 회귀 | Y1 (`porosity_union_exact_pct` · `thickness_wall_gap_um`) · Y2 · Y3 CN · Y4 · Y6 · Y7 | 5 노브 표준화 + 선형 / 2 차 Ridge → GPR 또는 트리 앙상블 비교 · 타깃마다 따로 · 결측 상 열은 그 상이 있는 행만 |
| B. 관통 분류 → 조건부 Tortuosity (기하학적) | `percolation_pct > 0` (130: 관통 106 · 비관통 24 / 64: 전부 관통) → 관통 행에서만 `tortuosity_SE_wall` (또는 `_median`) 회귀 | 로지스틱 / 트리 분류 + 관통 행 Ridge / GPR · **비관통 τ 를 0 이나 큰 값으로 채우지 않는다** · 비관통의 연속 진단은 `se_largest_comp_wall_span_frac` (τ 의 대체값 아님) |
| C. (선택) 데이터셋 이동 | 130 학습 → 64 평가 (또는 반대) | 무작위 섞기 CV 성능과 **나란히** 보고 — 분포 차이는 표지만 붙여서는 사라지지 않는다 |

**5-3. 평가 규약**
- 변수 선택 · 스케일링 · 초매개변수 선택은 **모두 학습 fold 안에서** 한다 (중첩 CV).
- 130 과 64 를 섞을 때는 데이터셋 표지를 두고, 무작위 혼합 CV 와 130↔64 이동 성능을 구분해 보고한다.
- n 이 작다 (130 · 64) — 불확실성 (fold 간 분산 · 예측 구간) 을 함께 보고한다.  "특징 대비 표본 15:1" 은 **경험적 주의**일 뿐 안전 보증이 아니다 (작은 n · 분포 이동 · 타깃 누설 · 물리 부적격은 중첩 CV 로도 안 고쳐진다).
- HOLD 포함 · 제외 결과는 둘 다 보고하되 **민감도 진단**으로만 — 좋은 쪽을 대표 결과로 고르지 않는다 (§3-7).

**5-4. 이 데이터가 보증하지 않는 것**
- 실험 검증 · 원시 덤프 재감사 · 실행 바이너리 · 목표 압력 도달 (검토 범위 밖).
- 전도도 (σ_ion · σ_e · κ) · 수송 tortuosity factor · 소성 보정 coverage · 응력 — 들어 있지 않다 (§6).
- HOLD 행의 물리 타당성 (§3-7) · 64 단독 물리 타깃 모델.
- 앞으로 다시 생성할 표의 관문 보증 (`LREL-01`~`04` — 음수 이온 분할 · 적격성 누락 · 중복 행 · SE 몫 변조를 현 관문이 놓친다.  **현재 배포값에는 해당 오류가 없다**).

## 6. 들어 있지 않은 것 (의도적으로)

전도도 (σ_ion · σ_e · κ) · τ_Laplace (망 계산 단계 — 나중) · 소성 보정 coverage · 응력 (σ_VM) · 근접쌍 (F1) · 파괴 (Auerbach) ·
접촉 면적 합 · 구 부피 합 기공률 · 내부 QC · 상세 출처 해시 — 정본 인계표에 있다.  새 디스크립터 후보 (응력 · 근접쌍 · 힘 · 겹침) 는 별도 검토 중.

## 7. 알려진 한계

- 퍼콜레이션 감사기 = 130 · 64 **모두 CLEAN** (`d1ec42fba` · `docs/data/lhs_perc_audit_20261001/`).
- 모든 값은 DEM (강체 구 · 연화 탄성) 모델 값이다 — 실험값이 아니다.  입자 모양 변형 (소성) 은 없다.
- 고정 상자 · 고정 압력 · 고정 SE 강성 안의 데이터다 (§3-6).
- 원천 작업 트리의 `dirty` 표지 · 실행 바이너리 · 완료 압력은 확인되지 않았다 — 검증은 **커밋된 중간 산출물에서 최종 표까지**는 강하고, 원시 덤프 → 중간 산출물 계보에는 제한적이다 (판정문 §1).
- 웹앱 쪽 일부 함수 (웹앱 τ · ε_union 쌍 렌즈 · 평판 높이 · 일반 coverage) 에는 결함이 남아 있다 — **배포 열은 그 함수를 쓰지 않는다** (수확기 · 정확 union · 벽 τ 경로).

## 8. AI 도구에 붙여 넣을 프롬프트

```
너는 고체전지 복합 양극 DEM 시뮬레이션 데이터로 ML 을 하는 조수다.  데이터 = lhs_release_20261001_v11.csv (130 행) ·
lhsx_release_20261001_v11.csv (64 행, 전부 SE-rich — 분포가 달라 따로 보거나 데이터셋 표지를 둔다).  한 행 = 300 MPa 로
압밀한 전극 침대 하나.  열 뜻은 README §2 · §4 와 *_columns.tsv 에 있다 (README 가 정정판).

규칙:
1) X = 자유 설계 노브 5 개 (am_pct = 고체 중 AM 질량 % · ps_frac = AM 중 AM_P 질량 몫 · d_am_p_um · d_am_s_um · d_se_um).
   반경 · 크기비 · block · ps_label 은 같은 정보의 재표현이다.  rve_um · pressure_MPa · e_se_gpa · loading_mAh_cm2 는 상수다
   (64 에서는 se_rich · n_large_components = 1 · ionic_dead_pct = 0 도 상수) — 특징 · 타깃으로 쓰지 마라.
   case_id · physical_target_status · hold_reason_codes · boundary_state 는 X 가 아니다.
   n_*_measured · 두께 · CN 같은 시뮬레이션 결과를 설계 → 구조 예측의 X 로 쓰면 누설이다.
2) 빈칸은 N/A 다.  0 으로 채우지 마라 (mono 의 없는 상 칸 · 관통하지 않은 침대의 se_se_cn_perc · se_se_cn_n_perc ·
   tortuosity_SE_wall).  Tortuosity (기하학적) 는 관통 여부 (percolation_pct > 0) 를 먼저 분류하고 관통한 침대에서만 회귀하라.
3) 항등식 열을 독립 타깃처럼 세지 마라: porosity_union_exact_pct/100 + phi_se_mass_conserving + phi_am_mass_conserving = 1 ·
   phi_se_mass_conserving = (1 − ε)·se_of_solid_vol · se_se_cn = 2·area_SE_SE_n/n_SE_measured · se_se_cn_n_perc = percolation_pct ×
   n_SE_measured/100 · ionic_active + dead + no_se = 100 · am_ionic_isolated_pct = 100 − ionic_active_pct ·
   am_se_cn_mean · coverage_AM_total 은 상별 값의 입자 수 가중평균.
4) 개수 열 (area_*_n · am_am_n_contacts · n_components · n_*_measured) 은 총량이다 — 정규화해서 써라.
5) 이름 주의: coverage_*_hertz_pct = Coverage (DEM) — AM 자유 표면 대비 SE 접촉 원판 면적 (DEM 겹침 기하 · 입자 평균) ·
   tortuosity_SE_wall = Tortuosity (기하학적) — 경계 띠 SE 중심 쌍의 최단경로 / 그 쌍의 z 간격 (수송 τ 아님) ·
   am_ionic_isolated_pct = 상단 경계 띠와 SE 접촉 그래프로 이어지지 않은 AM 비율 (실제 이온 전류 아님) ·
   *_vulnerable_pct = 고립 "위험" (SE 접촉 0–1 개) · thickness_mass_conserving_um 과 phi_* = 등가 장부량 (측정 두께는 thickness_wall_gap_um).
6) physical_target_status = HOLD 인 행 (130 중 59 · 64 중 62) 은 지우지 말고, DEM 에뮬레이터용 (HOLD 포함 가능) 과
   물리 타깃 후보 (HOLD 불허) 를 구분해 보고하라.  HOLD 포함 · 제외 비교는 민감도로만 쓰고 타당성 증거로 쓰지 마라.
7) 전도도는 이 데이터에 없다.  구조 값 사이의 관계와 설계 → 구조 예측만 다뤄라.
8) 변수 선택 · 스케일링 · 초매개변수는 학습 fold 안에서 (중첩 CV) · 130 과 64 는 데이터셋 표지 · 무작위 CV 와 데이터셋
   이동 성능을 구분 · 불확실성을 함께 보고하라.  다른 코퍼스와 합치지 마라.
```

## 9. 출처 · 재현

- 인계표 (생성기 `scripts/lhs_design_dataset.py`):
  ```
  python3 scripts/lhs_design_dataset.py --export-handover docs/data/lhs_handover_20261001.csv --harvest docs/data/lhs_descriptors_cov_1e09f661d --union docs/data/lhs_union_20260927/lhs130_union.tsv --webapp docs/data/lhs_webapp_contact_d1ec42fba --webapp-groups contact,percolation
  python3 scripts/lhs_design_dataset.py --export-handover docs/data/lhsx_handover_20261001.csv --design docs/data/lhsx_design_adapted_20260929.csv --harvest docs/data/lhsx_descriptors_cov_1e09f661d --union docs/data/lhs_union_20260927/lhsx64_union.tsv --webapp docs/data/lhsx_webapp_contact_d1ec42fba --webapp-groups contact,percolation
  ```
  관문 (항등식 G1–G7 · P1–P3 · τ T1–T3 · v1.1 D1–D5 · C1–C3 · 같은 프레임 · 수확 세대) 130/130 · 64/64 통과.  Codex 가 같은 CLI 로 재생성 → 커밋본과 바이트 동일.
- 배포 표 = 인계표의 **열 부분집합** (`scripts/lhs_release_build.py` — 만들 때 대조 내장):
  ```
  python3 scripts/lhs_release_build.py --handover docs/data/lhs_handover_20261001.csv --columns-from docs/data/lhs_release_20261001/lhs_release_20261001_columns.tsv \
      --add am_ionic_isolated_pct --add ionic_dead_pct --add ionic_no_se_pct --add AM_P_ionic_active_pct --add AM_P_ionic_dead_pct --add AM_P_ionic_no_se_pct \
      --add AM_S_ionic_active_pct --add AM_S_ionic_dead_pct --add AM_S_ionic_no_se_pct --add se_largest_comp_frac --add se_largest_comp_wall_span_frac \
      --add thickness_wall_gap_um --add physical_target_status --add hold_reason_codes --add boundary_state --out docs/data/lhs_release_20261001_v11/lhs_release_20261001_v11
  # 64 는 --handover docs/data/lhsx_handover_20261001.csv · --columns-from …/lhsx_release_20261001_columns.tsv · --out …/lhsx_release_20261001_v11
  ```
- 원자료: 수확 `docs/data/{lhs,lhsx}_descriptors_cov_1e09f661d/` · 웹앱 접촉 단계 `docs/data/{lhs,lhsx}_webapp_contact_d1ec42fba/` · union `docs/data/lhs_union_20260927/` · 퍼콜 감사 `docs/data/lhs_perc_audit_20261001/`.
- 판정 J20-g ~ J20-q · ML 인계본 = J20-r · 외부 검토 = 위 "외부 검토" 절.
