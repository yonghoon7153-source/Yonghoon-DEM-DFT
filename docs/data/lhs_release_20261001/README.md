# LHS 구조 디스크립터 — 배포 v1 (2026-10-01 · 1저자 배포 보류 해제)

> 수영 님 ML 용 **구조 디스크립터 최소 단위**.  DEM (LIGGGHTS) 으로 압밀한 복합 양극 침대를 설계 입력 → 구조 값으로 정리한 표다.
> 정본 (전체 열 · 내부 QC · 출처 해시) = `docs/data/lhs_handover_20261001.csv` · `lhsx_handover_20261001.csv` · 판정 기록 = `docs/reviews/lhs_handover_judgments_20260924.md` (J20 계열).

## 1. 파일

| 파일 | 행 × 열 | 내용 |
|---|---|---|
| `lhs_release_20261001.csv` | 130 × 74 | LHS 설계 130 침대 (bimodal 100 · mono AM_P 15 · mono AM_S 15) |
| `lhsx_release_20261001.csv` | 64 × 73 | 확장 64 침대 (bimodal 48 · mono 16) — **전부 SE-rich** (SE/고체 부피 0.51–0.85 · 분포가 130 과 다르다) |
| `*_columns.tsv` | 열마다 한 줄 | 뜻 · 분모 · 주의 · 판정 근거 (이 README 보다 자세하다) |

한 행 = 한 침대 (300 MPa 압밀 뒤 한 프레임).  `case_id` 가 키다.

## 2. 열 묶음

| 묶음 | 열 | 한 줄 뜻 |
|---|---|---|
| 설계 입력 | `am_pct` · `ps_frac` (AM_P 몫) · `d_am_p_um` · `d_am_s_um` · `d_se_um` · 반경 · 크기비 · `loading_mAh_cm2` (130 만) · `pressure_MPa` · `e_se_gpa` · `rve_um` · `block` | 시뮬레이션 전에 정한 값 = **특징 (X) 후보** |
| 기본 구조 | `n_*_measured` · `thickness_mass_conserving_um` · `porosity_union_exact_pct` · `se_rich` · `se_of_solid_vol` · `phi_se_mass_conserving` · `phi_am_mass_conserving` | 입자 수 · 두께 · 기공률 · 부피분율 |
| 피복률 | `coverage_AM_{P,S,total}_hertz_pct` | AM 표면 중 SE 와 맞닿은 기하 면적 비율 (%) |
| 접촉 위상 | `area_<쌍>_n` · `se_se_cn(_std)` · `am_am_cn(_std)` · `am_am_n_contacts` | 쌍별 접촉 개수 · 한 입자당 이웃 수 |
| AM–SE 접촉 (7c) | `am_se_cn_*` · `AM_P_se_cn_*` · `AM_S_se_cn_*` · `*_vulnerable_pct` | AM 한 알이 닿은 SE 수 (평균 · 분포) · 고립 **위험** 비율 |
| 퍼콜레이션 | `percolation_pct` · `top_reachable_pct` · `n_components` · `n_large_components` · `ionic_active_pct` · `se_se_cn_perc` · `se_se_cn_n_perc` | SE 망이 위아래로 이어지는가 · 이온이 닿는 AM 비율 |
| 벽 τ | `tortuosity_SE_wall` · `tortuosity_SE_wall_median` | 바닥 ↔ 플래튼을 잇는 **가장 짧은 SE 길**의 굽이 |
| 벽 접촉 | `wall_touch_frac_<상>_<floor|plate>` | 바닥 · 플래튼에 닿은 입자 비율 (벽 효과 설명 변수) |

## 3. 꼭 지킬 규약

1. **빈칸 = 없음 (N/A) 이지 0 이 아니다.**  ① mono 침대의 없는 상 칸 (예: mono_AM_S 의 `AM_P_*`) ② 관통하지 않은 침대의 `se_se_cn_perc` · `se_se_cn_n_perc` · `tortuosity_SE_wall` (130 중 24).
   0 으로 채우지 말 것.  단 접촉 개수 `area_<쌍>_n` 의 0 은 **측정된 0** 이다.
2. **mono 침대의 상별 칸 = 단일 AM 값** (전체 열과 같은 값 · 설계 `block` 이 상을 정한다).
3. **파생 · 항등식 열은 독립 타깃이 아니다** — 같은 값의 다른 표현이다 (생성기가 전부 1e-9 로 검사했다):
   `porosity_union_exact_pct/100 + phi_se_mass_conserving + phi_am_mass_conserving = 1` ·
   `am_se_cn_mean × N_AM = area_AM전체_SE_n` · `AM_x_se_cn_mean × N_x = area_AM_x_SE_n` · `se_se_cn = 2·area_SE_SE_n / N_SE` ·
   `am_am_cn = 2·am_am_n_contacts / N_AM` · `se_se_cn_n_perc = percolation_pct × N_SE / 100` · `am_se_cn_mean` · `_surface_weighted` · `coverage_AM_total` 은 상별 값의 가중평균.
4. **개수 열은 총량**이다 (`area_*_n` · `am_am_n_contacts` · `n_components` · `n_*_measured`) — 두께 · 입자 수에 비례하므로 특징으로 쓰려면 입자당 · 부피당으로 나눌 것.
5. **CN · 비율 열에는 벽 효과가 섞여 있다** — 벽 · 플래튼에 닿은 입자는 그쪽 이웃이 없다.  얇은 침대일수록 크다 → `wall_touch_frac_*` 를 함께 볼 것.

## 4. 이름과 뜻이 다른 곳 (오해 주의)

| 열 | 실제 뜻 |
|---|---|
| `coverage_*_hertz_pct` | 이름의 hertz 는 물려받은 이름 — **기하 교차 원판 면적** (LIGGGHTS 접촉 면적) 이다.  소성 보정 (physics) 면적은 **안 넘긴다** (SE 많은 침대에서 100 % 에 붙는다) |
| `porosity_union_exact_pct` | 입자 겹침을 뺀 정확한 부피 기준 기공률 (몬테카를로) — 소성 압밀에서 밀려난 재료를 고체로 안 세는 **상한 규약**.  구 부피 합 기공률은 겹침을 두 번 세어 음수가 나와 **안 넘긴다** |
| `*_vulnerable_pct` | SE 접촉이 0–1 개인 AM 비율 = **고립 위험** (접촉 하나만 끊겨도 고립).  **실제로 이온이 못 가는 AM 은 `100 − ionic_active_pct`** 다 (SE 무접촉 + 닿은 SE 가 분리막 쪽으로 안 이어짐).  예: `lhs00_083` 은 vulnerable 0.1 % 인데 이온이 못 가는 AM 89 % (SE 망이 끊긴 침대) |
| `percolation_pct` | 위 · 아래 가장자리 띠 (입자 반지름 2 배) 를 **둘 다** 잇는 SE 덩어리에 속한 SE 비율.  그래프 연결이지 전류 계산이 아니다.  **0.0 = 잇는 덩어리가 없다 (진짜 미관통)** |
| `top_reachable_pct` · `ionic_active_pct` | 위 띠 (분리막 쪽) 에 닿는 SE 기준 — 위 띠에 혼자 앉은 외톨이 SE 도 센다.  top_reachable ≥ percolation 이 늘 성립 |
| `n_components` | SE 덩어리 수 — **외톨이 SE (접촉 0) 도 한 덩어리**로 센다.  끊긴 침대에서는 사실상 외톨이 수.  `n_large_components` 의 문턱 10 은 출처 없는 코드 상수 |
| `tortuosity_SE_wall` | **기하 최단경로 τ** (SE 중심을 잇는 가장 짧은 길 / 두께 · 무작위 200 쌍 평균) — 병목 · 협착을 안 봐서 1 근처 (130: 1.29–4.15 · 64: 1.26–1.60).  **수송 τ 가 아니다** — COMSOL · 유효 전도도 입력용 τ (τ_Laplace) 는 이 표에 없다 |

## 5. 들어 있지 않은 것 (의도적으로)

전도도 (σ_ion · σ_e · κ) · τ_Laplace (망 계산 단계 — 나중) · 소성 보정 피복률 · 응력 (σ_VM) · 근접쌍 (F1) · 파괴 (Auerbach) · 접촉 면적 합 · 구 부피 합 기공률 · 내부 QC · 상태 열 · 출처 해시 (정본 표에 있다).

## 6. 알려진 한계

- 64 침대는 퍼콜레이션 감사기 (경계 폴백 · 겹침 검사) 를 **돌리지 않았다** — 수확기 독립 재현 (관통 판정 64/64 일치) 으로 대신했다.  130 은 감사 130/130 통과.
- 관통하지 않은 24 침대 (130) 의 τ 는 빈칸이다 — "얼마나 관통에 가까웠나" 를 나타내는 연속 디스크립터는 **다음 판에서 검토** 중 (가장 큰 SE 덩어리의 두께 도달 비율 등).
- 모든 값은 DEM (강체 구 · 연화 탄성) 모델 값이다 — 실험값이 아니다.  입자 모양 변형 (소성) 은 없다.

## 7. AI 도구에 붙여 넣을 프롬프트

```
너는 고체전지 복합 양극 DEM 시뮬레이션 데이터로 ML 을 하는 조수다.  데이터 = lhs_release_20261001.csv (130 행) ·
lhsx_release_20261001.csv (64 행, 전부 SE-rich — 분포가 달라 따로 보거나 그룹 변수를 둔다).  한 행 = 300 MPa 로 압밀한
전극 침대 하나.  열 뜻은 *_columns.tsv 에 있다.

규칙:
1) 특징 (X) 후보 = 설계 입력 (am_pct · ps_frac · d_am_p_um · d_am_s_um · d_se_um · 반경 · 크기비 · loading_mAh_cm2 ·
   pressure_MPa · e_se_gpa · rve_um · block).  나머지는 시뮬레이션이 낸 구조 값 = 타깃 (Y) 후보다.
2) 빈칸은 N/A 다.  0 으로 채우지 마라.  mono 침대의 없는 상 칸과 관통하지 않은 침대의 se_se_cn_perc ·
   se_se_cn_n_perc · tortuosity_SE_wall 이 빈칸이다.  τ 를 예측할 때는 관통 여부 (percolation_pct > 0) 를 먼저
   분류하고, 관통한 침대에서만 τ 를 회귀하라 (두 단계 모델).
3) 항등식으로 묶인 열을 서로 다른 타깃처럼 다루지 마라: porosity_union_exact_pct/100 + phi_se_mass_conserving +
   phi_am_mass_conserving = 1 · se_se_cn = 2·area_SE_SE_n/n_SE_measured · se_se_cn_n_perc = percolation_pct ×
   n_SE_measured/100 · am_se_cn_mean 과 surface_weighted 와 coverage_AM_total 은 상별 값의 가중평균.
4) 개수 열 (area_*_n · am_am_n_contacts · n_components · n_*_measured) 은 총량이다 — 입자 수나 부피로 정규화해서 써라.
5) 이름 주의: coverage_*_hertz_pct = 기하 접촉 면적 기반 피복률 · tortuosity_SE_wall = 기하 최단경로 (수송 τ 아님) ·
   *_vulnerable_pct = 고립 "위험" (SE 접촉 0–1 개) — 실제로 이온이 못 가는 AM 은 100 − ionic_active_pct.
6) 전도도는 이 데이터에 없다.  전도도를 말하지 말고, 구조 값 사이의 관계와 설계 → 구조 예측만 다뤄라.
7) 교차검증은 행 단위로 하되 130 과 64 를 섞을 때는 그룹 (데이터셋) 을 표시하라.  n 이 작으니 (130 · 64)
   특징 수 대비 표본 수를 지키고 (대략 15:1) 중첩 교차검증으로 과적합을 막아라.
```

## 8. 출처

생성기 `scripts/lhs_design_dataset.py` (`--export-handover … --webapp-groups contact,percolation`) · 수확 `docs/data/{lhs,lhsx}_descriptors_cov_1e09f661d/` ·
웹앱 배치 `docs/data/{lhs,lhsx}_webapp_coverage_1e09f661d/` · union `docs/data/lhs_union_20260927/` · 관문 (항등식 · 독립 재현) 전부 130/130 · 64/64 통과 ·
판정 J20-g ~ J20-o · 배포 표는 정본 인계표의 열 부분집합 (값 한 글자도 안 바꿈).
