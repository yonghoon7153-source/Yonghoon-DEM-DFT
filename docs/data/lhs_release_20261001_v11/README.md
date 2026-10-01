# LHS 구조 디스크립터 — 배포 v1.1 (2026-10-01 · J20-p)

> 수영 님 ML 용 **구조 디스크립터 최소 단위**.  DEM (LIGGGHTS) 으로 압밀한 복합 양극 침대를 설계 입력 → 구조 값으로 정리한 표다.
> 정본 (전체 열 · 내부 QC · 출처 해시) = `docs/data/lhs_handover_20261001.csv` · `lhsx_handover_20261001.csv` · 판정 기록 = `docs/reviews/lhs_handover_judgments_20260924.md` (J20 계열).
> v1 (`docs/data/lhs_release_20261001/`) 은 그대로 둔다 — v1 의 74 · 73 열은 v1.1 에서 **값 · 순서가 한 글자도 안 바뀌었다** (뒤에 열만 붙였다).

## 0. v1 → v1.1 에서 바뀐 것

| 무엇 | 왜 |
|---|---|
| **이온 경로 고립** 9 열 (`am_ionic_isolated_pct` · 단절 · 무접촉 · 상별 6) | v1 의 `*_vulnerable_pct` 는 고립 **위험** (접촉 개수) 이라 실제로 이온이 못 가는 AM 과 다르다 (J20-p ① ②) |
| **가장 큰 SE 덩어리** 2 열 | 관통하지 않은 24 침대 (130) 의 "얼마나 관통에 가까웠나" 연속값 (J20-p ③) |
| `thickness_wall_gap_um` | 측정한 판 간격 두께 — v1 에는 유도값 (질량 보존 두께) 만 있었다 |
| **적격성 표지** 3 열 (`physical_target_status` · `hold_reason_codes` · `boundary_state`) | 정본 인계표의 HOLD 표지가 v1 에서 빠져 있었다 (§3-7) |
| 접촉 단계 원천 = `d1ec42fba` 재실행 | F1 근접쌍 수정 (`LHS-22`) 뒤 세대 · 배포 열 값 변화 0 (F1 은 배포 밖) |
| README §3 · §5 · §6 · §7 정정 | 상수 열을 특징 후보로 적었던 것 · "전부 1e-9 로 검사" 과장 · 옛 코퍼스와 섞지 말 것 · 두 두께 |

## 1. 파일

| 파일 | 행 × 열 | 내용 |
|---|---|---|
| `lhs_release_20261001_v11.csv` | 130 × 89 | LHS 설계 130 침대 (bimodal 100 · mono AM_P 15 · mono AM_S 15) |
| `lhsx_release_20261001_v11.csv` | 64 × 88 | 확장 64 침대 (bimodal 48 · mono 16) — **전부 SE-rich** (SE/고체 부피 0.51–0.85 · 분포가 130 과 다르다) |
| `*_columns.tsv` | 열마다 한 줄 | 뜻 · 분모 · 주의 · 판정 근거 (이 README 보다 자세하다 · 정본 인계표 열 사전과 같은 줄) |

한 행 = 한 침대 (300 MPa 압밀 뒤 한 프레임).  `case_id` 가 키다.

## 2. 열 묶음

| 묶음 | 열 | 한 줄 뜻 |
|---|---|---|
| 설계 입력 | `am_pct` · `ps_frac` (AM_P 몫) · `d_am_p_um` · `d_am_s_um` · `d_se_um` · 반경 · 크기비 · `block` (+ 상수 열 — §3-6) | 시뮬레이션 전에 정한 값 = **특징 (X) 후보** |
| 기본 구조 | `n_*_measured` · `thickness_mass_conserving_um` · `thickness_wall_gap_um` · `porosity_union_exact_pct` · `se_rich` · `se_of_solid_vol` · `phi_se_mass_conserving` · `phi_am_mass_conserving` | 입자 수 · 두께 둘 (§4) · 기공률 · 부피분율 |
| 피복률 | `coverage_AM_{P,S,total}_hertz_pct` | AM 표면 중 SE 와 맞닿은 기하 면적 비율 (%) |
| 접촉 위상 | `area_<쌍>_n` · `se_se_cn(_std)` · `am_am_cn(_std)` · `am_am_n_contacts` | 쌍별 접촉 개수 · 한 입자당 이웃 수 |
| AM–SE 접촉 (7c) | `am_se_cn_*` · `AM_P_se_cn_*` · `AM_S_se_cn_*` · `*_vulnerable_pct` | AM 한 알이 닿은 SE 수 (평균 · 분포) · 고립 **위험** 비율 (SE 접촉 0–1 개) |
| 퍼콜레이션 | `percolation_pct` · `top_reachable_pct` · `n_components` · `n_large_components` · `ionic_active_pct` · `se_se_cn_perc` · `se_se_cn_n_perc` | SE 망이 위아래로 이어지는가 · 이온이 닿는 AM 비율 |
| **이온 경로 고립 (v1.1)** | `am_ionic_isolated_pct` · `ionic_dead_pct` · `ionic_no_se_pct` · `{AM_P,AM_S}_ionic_{active,dead,no_se}_pct` | 이온이 분리막 쪽에서 **실제로 닿지 못하는** AM 비율과 그 원인 (단절 = 닿은 SE 가 끊긴 덩어리 · 무접촉 = SE 접촉 0) |
| 벽 τ | `tortuosity_SE_wall` · `tortuosity_SE_wall_median` | 바닥 ↔ 플래튼을 잇는 **가장 짧은 SE 길**의 굽이 |
| **SE 덩어리 (v1.1)** | `se_largest_comp_frac` · `se_largest_comp_wall_span_frac` | 가장 큰 SE 덩어리에 든 SE 비율 · 그 덩어리의 두께 방향 폭 / 벽 간격 |
| 벽 접촉 | `wall_touch_frac_<상>_<floor|plate>` | 바닥 · 플래튼에 닿은 입자 비율 (벽 효과 설명 변수) |
| **적격성 표지 (v1.1)** | `physical_target_status` · `hold_reason_codes` · `boundary_state` | 물리 타깃으로 쓰기 전에 볼 표지 (§3-7) |

## 3. 꼭 지킬 규약

1. **빈칸 = 없음 (N/A) 이지 0 이 아니다.**  ① mono 침대의 없는 상 칸 (예: mono_AM_S 의 `AM_P_*`) ② 관통하지 않은 침대의 `se_se_cn_perc` · `se_se_cn_n_perc` · `tortuosity_SE_wall` (130 중 24) ③ `hold_reason_codes` 의 빈칸 = 사유 없음 (OK).
   0 으로 채우지 말 것.  단 접촉 개수 `area_<쌍>_n` 의 0 은 **측정된 0** 이다.
2. **mono 침대의 상별 칸 = 단일 AM 값** (전체 열과 같은 값 · 설계 `block` 이 상을 정한다) — 새 상별 이온 열도 같다.
3. **파생 · 항등식 열은 독립 타깃이 아니다** — 같은 값의 다른 표현이다:
   `porosity_union_exact_pct/100 + phi_se_mass_conserving + phi_am_mass_conserving = 1` ·
   `am_se_cn_mean × N_AM = area_AM전체_SE_n` · `AM_x_se_cn_mean × N_x = area_AM_x_SE_n` · `se_se_cn = 2·area_SE_SE_n / N_SE` ·
   `am_am_cn = 2·am_am_n_contacts / N_AM` · `se_se_cn_n_perc = percolation_pct × N_SE / 100` ·
   `ionic_active_pct + ionic_dead_pct + ionic_no_se_pct = 100` (상별도) · `am_ionic_isolated_pct = 100 − ionic_active_pct` ·
   `am_se_cn_mean` · `_surface_weighted` 와 `coverage_AM_total` 은 상별 값의 가중평균.
   생성기 관문이 위 등식 대부분을 행마다 검사한다 (1e-9 · 정수 개수).  ⚠ `coverage_AM_total` 의 가중평균은 관문이 **검사하지 않는다** (정의상 성립 — v1 README 의 "전부 검사" 는 과장이었다).
4. **개수 열은 총량**이다 (`area_*_n` · `am_am_n_contacts` · `n_components` · `n_*_measured`) — 두께 · 입자 수에 비례하므로 특징으로 쓰려면 입자당 · 부피당으로 나눌 것.
5. **CN · 비율 열에는 벽 효과가 섞여 있다** — 벽 · 플래튼에 닿은 입자는 그쪽 이웃이 없다.  얇은 침대일수록 크다 → `wall_touch_frac_*` 를 함께 볼 것.
6. **상수 열은 특징이 아니다** — 모든 행에서 값이 같다 (고정 상자 · 고정 조건 안의 예측이라는 뜻):
   130 = `rve_um` 50 · `pressure_MPa` 300 · `e_se_gpa` 1.35 · `loading_mAh_cm2` 2.0 / 64 = `rve_um` · `pressure_MPa` · `e_se_gpa` (+ 64 에서는 `se_rich` 전부 참 · `n_large_components` · `ionic_dead_pct` 0 도 상수).
   ⇒ 이 데이터로 압력 · 상자 크기 · SE 강성 · 적재량의 영향을 배울 수 없다.
7. **적격성 표지 (v1.1 에서 추가)** — 값은 모든 행에서 계산됐다 (계산 실패 없음).  표지는 "물리적 전극 구조 타깃으로 그대로 믿어도 되는가" 를 따로 적은 것이다:
   - `boundary_state` — 바닥 (z = 0) · 플래튼 평면 기준: **CENTER_CROSSED** = 중심이 평면을 넘은 입자가 있다 · **FULLY_OUT** = 통째로 평면 밖인 입자가 있다 · **INSIDE** = 없다.
     130: INSIDE 87 · CENTER_CROSSED 27 · FULLY_OUT 16 / 64: 53 · 6 · 5.
   - `hold_reason_codes` — **BOUNDARY_CENTER_OUT** (위의 중심이 넘은 입자 ≥ 1) · **NEGATIVE_POROSITY** (구 부피 합 porosity < 0 = 겹침이 큰 침대 · 배포 porosity 는 정확 union 이라 양수다) · `|` 로 잇는다.
   - `physical_target_status` — 사유가 하나라도 있으면 **HOLD**.  130: OK 71 · HOLD 59 (BOUNDARY 41 · NEGATIVE 16 · 둘 다 2) / 64: OK 2 · HOLD 62 (NEGATIVE 51 · 둘 다 9 · BOUNDARY 2).
   - 쓰는 법: 지우지 말고 **표지를 둔 채로** — HOLD 를 뺀 학습과 넣은 학습을 둘 다 해 보고 결론이 바뀌는지 볼 것.  64 는 거의 전부 HOLD (겹침이 큰 SE-rich 침대) 라 빼면 남는 것이 없다.
8. **다른 코퍼스와 섞지 말 것** — 웹앱의 옛 케이스 모음 (291 행 · 구 부피 합 porosity · d_am 0 행 · MPM/DEM 혼합) 과는 규약이 다르다 (`DESC-08`).  130 과 64 를 함께 쓸 때도 데이터셋 표지를 둔다.

## 4. 이름과 뜻이 다른 곳 (오해 주의)

| 열 | 실제 뜻 |
|---|---|
| `coverage_*_hertz_pct` | 이름의 hertz 는 물려받은 이름 — **기하 교차 원판 면적** (LIGGGHTS 접촉 면적) 이다.  소성 보정 (physics) 면적은 **안 넘긴다** (SE 많은 침대에서 100 % 에 붙는다 · J20-m) |
| `porosity_union_exact_pct` | 입자 겹침을 뺀 정확한 부피 기준 기공률 (몬테카를로 · 세 입자 이상 겹침까지) — 소성 압밀에서 밀려난 재료를 고체로 안 세는 **상한 규약** |
| `thickness_wall_gap_um` ↔ `thickness_mass_conserving_um` | **벽 간격** = 같은 프레임의 플래튼 − 바닥 (측정값) · **질량 보존** = 벽 간격 × (1 − ε_구부피합)/(1 − ε_union) — union 기공률과 **같은 고체**를 담는 두께 (유도값 · φ 두 열과 같은 장부).  질량 보존 / 벽 간격 = 130: 1.015–1.114 (중앙 1.043) · 64: 1.074–1.153 (중앙 1.118).  "실제 두께" 를 말할 때는 벽 간격, φ · ε 의 닫힘을 쓸 때는 질량 보존 |
| `*_vulnerable_pct` ↔ `am_ionic_isolated_pct` | 고립 **위험** (SE 접촉 0–1 개 — 하나만 끊겨도 고립) ↔ 경로 기준 **실제 고립** (= 100 − `ionic_active_pct` = 단절 + 무접촉).  관통하지 않은 침대에서 크게 갈린다 (130 비관통 24: 실제 고립 61.4–96.9 % · 예 `lhs00_018` 위험 0.09 % ↔ 실제 85.4 %) |
| `percolation_pct` | 위 · 아래 가장자리 띠 (입자 반지름 2 배) 를 **둘 다** 잇는 SE 덩어리에 속한 SE 비율.  그래프 연결이지 전류 계산이 아니다.  **0.0 = 잇는 덩어리가 없다 (진짜 0)** |
| `top_reachable_pct` · `ionic_active_pct` | 위 띠 (분리막 쪽) 에 닿는 SE 기준 — 위 띠에 혼자 앉은 외톨이 SE 도 센다.  top_reachable ≥ percolation 이 늘 성립 |
| `n_components` | SE 덩어리 수 — **외톨이 SE (접촉 0) 도 한 덩어리**로 센다.  `n_large_components` 의 문턱 10 은 출처 없는 코드 상수 |
| `tortuosity_SE_wall` | **기하 최단경로 τ** (SE 중심을 잇는 가장 짧은 길 / 두께 · 무작위 200 쌍 평균) — 병목 · 협착을 안 봐서 1 근처 (130: 1.29–4.15 · 64: 1.26–1.60).  **수송 τ 가 아니다** |
| `se_largest_comp_frac` · `_wall_span_frac` | 가장 큰 = **SE 수** 기준 덩어리 (가장 멀리 뻗은 덩어리가 아닐 수 있다).  폭은 입자 **표면** 기준이라 관통 침대는 1 을 조금 넘는다 (130: 1.011–1.045 · 64: 1.023–1.062) · 비관통 24: 비율 0.002–0.908 · 폭 0.11–0.96 (중앙 0.39) |

## 5. 들어 있지 않은 것 (의도적으로)

전도도 (σ_ion · σ_e · κ) · τ_Laplace (망 계산 단계 — 나중) · 소성 보정 피복률 · 응력 (σ_VM) · 근접쌍 (F1 — `LHS-22` 로 주기 경계를 고쳤지만 여전히 배포 밖) · 파괴 (Auerbach) ·
접촉 면적 합 · 구 부피 합 기공률 · 내부 QC · 상세 출처 해시 — 정본 인계표에 있다.  새 디스크립터 후보 (응력 · 근접쌍 · 힘 · 겹침) 는 별도 검토 중.

## 6. 알려진 한계

- 퍼콜레이션 감사기 (경계 폴백 · 겹침 · 웹앱 정본 재현) = 130 · 64 **모두 CLEAN** (`d1ec42fba` · `docs/data/lhs_perc_audit_20261001/`) — 130 은 09-29 판과 공통 열 차이 0.
- 적격성 HOLD 는 130 의 45 % · 64 의 97 % 다 (§3-7).  HOLD 가 어느 배포 열을 얼마나 흔드는지는 아직 재지 않았다 (외부 검토 질문).
- 모든 값은 DEM (강체 구 · 연화 탄성) 모델 값이다 — 실험값이 아니다.  입자 모양 변형 (소성) 은 없다.
- 고정 상자 (50 µm) · 고정 압력 (300 MPa) · 고정 SE 강성 안의 데이터다 (§3-6).
- 웹앱 쪽 일부 함수 (예: 웹앱 τ · ε_union 쌍 렌즈 · 평판 높이) 에는 외부 검토가 찾은 결함이 남아 있다 — **배포 열은 그 함수를 쓰지 않는다** (수확기 · 정확 union · 벽 τ 경로).

## 7. AI 도구에 붙여 넣을 프롬프트

```
너는 고체전지 복합 양극 DEM 시뮬레이션 데이터로 ML 을 하는 조수다.  데이터 = lhs_release_20261001_v11.csv (130 행) ·
lhsx_release_20261001_v11.csv (64 행, 전부 SE-rich — 분포가 달라 따로 보거나 데이터셋 표지를 둔다).  한 행 = 300 MPa 로
압밀한 전극 침대 하나.  열 뜻은 *_columns.tsv 에 있다.

규칙:
1) 특징 (X) 후보 = 설계 입력 (am_pct · ps_frac · d_am_p_um · d_am_s_um · d_se_um · 반경 · 크기비 · block).
   rve_um · pressure_MPa · e_se_gpa · loading_mAh_cm2 는 모든 행에서 같은 상수다 — 특징으로 쓰지 마라.
   나머지는 시뮬레이션이 낸 구조 값 = 타깃 (Y) 후보다.
2) 빈칸은 N/A 다.  0 으로 채우지 마라.  mono 침대의 없는 상 칸과 관통하지 않은 침대의 se_se_cn_perc ·
   se_se_cn_n_perc · tortuosity_SE_wall 이 빈칸이다.  τ 를 예측할 때는 관통 여부 (percolation_pct > 0) 를 먼저
   분류하고, 관통한 침대에서만 τ 를 회귀하라 (두 단계 모델).  관통하지 않은 침대의 연속값은 se_largest_comp_wall_span_frac 이다.
3) 항등식으로 묶인 열을 서로 다른 타깃처럼 다루지 마라: porosity_union_exact_pct/100 + phi_se_mass_conserving +
   phi_am_mass_conserving = 1 · se_se_cn = 2·area_SE_SE_n/n_SE_measured · se_se_cn_n_perc = percolation_pct ×
   n_SE_measured/100 · ionic_active_pct + ionic_dead_pct + ionic_no_se_pct = 100 · am_ionic_isolated_pct = 100 − ionic_active_pct ·
   am_se_cn_mean 과 surface_weighted 와 coverage_AM_total 은 상별 값의 가중평균.
4) 개수 열 (area_*_n · am_am_n_contacts · n_components · n_*_measured) 은 총량이다 — 입자 수나 부피로 정규화해서 써라.
5) 이름 주의: coverage_*_hertz_pct = 기하 접촉 면적 기반 피복률 · tortuosity_SE_wall = 기하 최단경로 (수송 τ 아님) ·
   *_vulnerable_pct = 고립 "위험" (SE 접촉 0–1 개) · 실제로 이온이 못 가는 AM = am_ionic_isolated_pct ·
   두께는 둘이다 (thickness_wall_gap_um = 측정 · thickness_mass_conserving_um = union 과 같은 장부의 유도값).
6) physical_target_status 가 HOLD 인 행이 있다 (130 의 45 % · 64 의 97 %).  지우지 말고, HOLD 를 뺀 결과와 넣은 결과를
   둘 다 보고하라.  hold_reason_codes 와 boundary_state 가 사유다.
7) 전도도는 이 데이터에 없다.  전도도를 말하지 말고, 구조 값 사이의 관계와 설계 → 구조 예측만 다뤄라.
8) 교차검증은 행 단위로 하되 130 과 64 를 섞을 때는 그룹 (데이터셋) 을 표시하라.  다른 코퍼스와 합치지 마라.
   n 이 작으니 (130 · 64) 특징 수 대비 표본 수를 지키고 (대략 15:1) 중첩 교차검증으로 과적합을 막아라.
```

## 8. 출처 · 재현

- 인계표 (생성기 `scripts/lhs_design_dataset.py`):
  ```
  python3 scripts/lhs_design_dataset.py --export-handover docs/data/lhs_handover_20261001.csv --harvest docs/data/lhs_descriptors_cov_1e09f661d --union docs/data/lhs_union_20260927/lhs130_union.tsv --webapp docs/data/lhs_webapp_contact_d1ec42fba --webapp-groups contact,percolation
  python3 scripts/lhs_design_dataset.py --export-handover docs/data/lhsx_handover_20261001.csv --design docs/data/lhsx_design_adapted_20260929.csv --harvest docs/data/lhsx_descriptors_cov_1e09f661d --union docs/data/lhs_union_20260927/lhsx64_union.tsv --webapp docs/data/lhsx_webapp_contact_d1ec42fba --webapp-groups contact,percolation
  ```
  관문 (항등식 G1–G7 · P1–P3 · τ T1–T3 · v1.1 D1–D5 · C1–C3 · 같은 프레임 · 수확 세대) 130/130 · 64/64 통과 · 옛 칸 변경 0 (v1 인계표 대비 열 8 개만 추가).
- 배포 표 = 인계표의 **열 부분집합** (`scripts/lhs_release_build.py` — 만들 때 대조 내장 · v1 도 같은 도구로 바이트 재현된다):
  ```
  python3 scripts/lhs_release_build.py --handover docs/data/lhs_handover_20261001.csv --columns-from docs/data/lhs_release_20261001/lhs_release_20261001_columns.tsv \
      --add am_ionic_isolated_pct --add ionic_dead_pct --add ionic_no_se_pct --add AM_P_ionic_active_pct --add AM_P_ionic_dead_pct --add AM_P_ionic_no_se_pct \
      --add AM_S_ionic_active_pct --add AM_S_ionic_dead_pct --add AM_S_ionic_no_se_pct --add se_largest_comp_frac --add se_largest_comp_wall_span_frac \
      --add thickness_wall_gap_um --add physical_target_status --add hold_reason_codes --add boundary_state --out docs/data/lhs_release_20261001_v11/lhs_release_20261001_v11
  # 64 는 --handover docs/data/lhsx_handover_20261001.csv · --columns-from …/lhsx_release_20261001_columns.tsv · --out …/lhsx_release_20261001_v11
  ```
- 원자료: 수확 `docs/data/{lhs,lhsx}_descriptors_cov_1e09f661d/` · 웹앱 접촉 단계 `docs/data/{lhs,lhsx}_webapp_contact_d1ec42fba/` (1저자 WSL · 10-01 · 130 + 64 전부 done ·
  `status.json` 의 dirty 표지 = 작업 트리의 추적 파일 변경 — 사유 확인 중) · union `docs/data/lhs_union_20260927/` · 퍼콜 감사 `docs/data/lhs_perc_audit_20261001/`.
- 판정 J20-g ~ J20-p · 배포 v1.1 기록 = 같은 문서 J20-q.
