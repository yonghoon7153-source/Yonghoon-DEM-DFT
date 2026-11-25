<!-- digest 표준 양식. ★ = 사용자가 특히 원한 항목. COMPREHENSIVE / paper-level STANDALONE digest. 깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md · 같은 묶음 = zhou2019_mpfem_2d_copper_powder_die_compaction_release.md · huang2017_mpfem_2d_binary_al_sic_hard_soft_compaction.md -->
# 같은 크기 (지름 1 mm) 의 무른 + 단단한 금속 구를 입자마다 FE 메시로 (3D MPFEM · MSC.Marc) 원통 다이 압축 → 하중 유지 → **탈압** — 진동 충전 ↔ 자연 충전 · 상대밀도 ≈0.48 → ≈0.84 (200 MPa) · 단단한 구에 응력이 모이고 무른 구는 단단한 구에 눌려 **안으로 오목** 해져 옆 공극을 못 채운다 · 탈압 뒤 가운데 응력이 크게 빠지고 (단단 230 → ≈88 · 무름 ≈180 → ≈40 MPa) 모서리에 남는다 ★ [DEM 우선 (수영)] 의 3D 단단한 + 무른 짝 (AM + SE) 과 탈압 (R4) 의 가장 가까운 3D 선례 — 단 입자 ≈50 개 (판독) — Li, Han, Xu, Liu, Zhang, Xu (Math. Probl. Eng. 2022)

> slug `li2022_mpfem_3d_soft_hard_composite_compaction_vibration_unloading` · DOI `10.1155/2022/8580849` · type `MPFEM 3D (MSC.Marc · 입자마다 요소 1014 · 절점 872 · 갱신 라그랑주 · node-to-segment 접촉 · 아크탄젠트 정칙화 Coulomb µ 0.2 · 무른 + 단단한 탄소성 멱경화 · 강체 매끈 원통 다이 · 펀치) + DEM (자연 · 진동 초기 충전) + 실험 (압축 곡선 · 소재 · 조건 미기재)` · PDF `li2022.pdf` · digested `2026-11-25` · status ✅

> 표지: **[인쇄]** = 본문 · 표 · 캡션 · 그림 패널의 값 · **[판독]** = 그림에서 읽은 값 (그림 2 · 7 · 8 · 9 는 PDF 벡터 표식을 눈금 표식으로 환산 — `litdb/figures/li2022_mpfem_3d_soft_hard_composite_compaction_vibration_unloading/digitized.csv`) · **[카드 산술]** · **[추정]** · **[미확인]**.
> Hindawi 판이라 본문 글꼴에서 "Th" 가 "'" 로 깨져 있다 ("The" → "'e").  인용은 "The" 로 바로잡아 옮긴다.

---

## 0. 이 논문이 우리에게 *왜* 필요한가 (한눈 positioning)

같은 묶음의 두 2D 카드 (`zhou2019_…` = 2D 단일 재료 + 탈압 · `huang2017_…` = 2D 단단 + 무름) 를 **3D** 로 옮긴 같은 그룹 (University of Science and Technology Liaoning · Peng Han 교신) 의 후속이다.  우리에게 값진 것은 셋이다.

1. **3D 단단 + 무른 혼합의 FE 모습** — 응력이 단단한 구에 모이고 (그림 3 · 9), 무른 구는 단단한 구에 눌린 자리가 **안으로 오목** 해진다 — *"The irregular particle shape produced by this depression is difficult to squeeze into the adjacent pores inside the compact, which hinders further filling of the pores."* [인쇄].  우리 AM (단단) 이 SE (무름) 를 누르는 자리의 형상 기전 후보다.
2. **3D 탈압 (R4)** — 하중 유지 → 탈압을 풀고 입자 안 응력 단면을 냈다 (그림 6–9).
3. **3D MPFEM 의 규모 한계** — 입자 수는 원문에 없고 그림으로 어림하면 ≈50 개다 [판독 · 자릿수].  메모 3.2 의 "3D MPFEM = 작은 상자 검산 자리" 판단에 한 점을 더한다.

| 우리가 필요한 것 | 이 논문이 주는 것 | 주지 않는 것 |
|---|---|---|
| 3D 단단 + 무른 FE | 무름 (E 62.59 GPa · C 225.9 MPa · n 0.25) + 단단 (E 120 GPa · C 575.3 MPa · n 0.237) · 같은 크기 · X_soft 25 wt% [인쇄] | 소재 이름 · 밀도 · 수 분율 [미확인] |
| 압축 곡선 + 실험 | 모의 · 실험 × 진동 유무 4 곡선 (0–200 MPa) [판독 표 §3-2] | 실험 소재 · 분말 · 다이 · 진동 조건 [미확인] |
| 탈압 관측량 | 입자 안 von Mises 단면 (가운데 · 세 축) · 절점 4 개 이력 · 탈압 뒤 잔류 [판독 + 인쇄] | 탈압 뒤 상대밀도 · 되튐 [미확인] |
| 3D 규모 · 해상도 | 구마다 요소 1014 (부피 등가 지름당 ≈12.5 요소 [카드 산술]) | 입자 수 · 다이 크기 · 메시 수렴 [미확인] |
| 마찰 법칙 | 아크탄젠트 정칙화 Coulomb (Eq. 1 · rv_cnst = 붙음 경계 상대 속도) [인쇄] | rv_cnst 값 [미확인] |

⚠ **단단한 상도 금속이라 우리 AM 과 다르다** — 이 논문의 '단단' 은 항복 강도가 무름의 ≈2.5 배 (C 575.3 / 225.9) 인 **소성 금속**이고 같은 크기다.  우리 AM (NCM) 은 거의 항복하지 않고 깨지며, SE 보다 지름이 4–12 배 크다.  가져가는 것은 *형상 · 응력 · 탈압의 방향* 이다.

---

## 1. 한 줄 요약

DEM 으로 만든 자연 · 진동 무작위 충전의 같은 크기 (지름 1 mm) 무른 + 단단한 구마다 FE 메시 (요소 1014 · 절점 872) 를 주고 MSC.Marc 로 3D 원통 다이 단동 압축 (≈200 MPa) · 하중 유지 · 탈압을 풀었다.  진동 충전은 압축 초반 밀도를 조금 더 빨리 올리지만 (실험 25 MPa 에서 +0.035 [판독]) ≈100 MPa 위에서 곡선이 모이고 끝 밀도 (≈0.83–0.84) 는 거의 같다.  하중은 단단한 구에 모이고 무른 구가 크게 변형해 공극을 채우되, 단단한 구에 눌린 무른 구 표면은 오목해져 이웃 공극으로 못 들어간다.  압분체는 위가 아래보다 조밀하다.  탈압하면 두 구의 가운데 응력이 크게 빠지고 (단단 ≈230 → ≈88 · 무름 ≈180 → ≈40 MPa [판독]) 모서리 · 접점에 큰 잔류 응력이 남는다 — 본문은 이를 소결 때 균열 위험으로 읽는다.

---

## 2. 메타

| 항목 | 내용 |
|---|---|
| 저자 | **Junnan Li · Peng Han** (교신, hanpeng@ustl.edu.cn) · **Yingshi Xu · Kun Liu · Guoxin Zhang · Peng Xu** |
| 소속 | School of Materials and Metallurgy, University of Science and Technology Liaoning, Anshan 114000, China (Xu Yingshi 제외) · Angang Steel Corporation Limited, Anshan 114000, China (Xu Yingshi) |
| 저널 | **Mathematical Problems in Engineering, Volume 2022, Article ID 8580849** (11 쪽) · Hindawi · Research Article |
| DOI | **10.1155/2022/8580849** |
| 이력 | Received 2021-05-21 · Accepted 2022-01-18 · Published 2022-02-10 · Academic Editor: AMA Neves |
| 라이선스 | Creative Commons Attribution (open access) [인쇄] |
| 연구비 | Education Department Project of Liaoning Province (2020LNQN12) · National Key R&D Project of China (2017YFC0805100) · Fundamental Research Funds for University of Science and Technology Liaoning (2018QN13) |
| 자료 공개 | *"The data used to support the findings of this study are included within the article."* [인쇄] |
| 연구유형 | **3D MPFEM** (MSC.Marc) + DEM (초기 충전 · 진동 포함) + 실험 (압축 곡선만) |
| 같은 그룹 | `zhou2019_mpfem_2d_copper_powder_die_compaction_release` (같은 교신 · 같은 Cu 상수) · `huang2017_mpfem_2d_binary_al_sic_hard_soft_compaction` ([23] 로 인용 · 같은 Al 상수) |

---

## 3. 핵심 수치

### 3-1. 모델 구성 (Table 1 전사 + 유도)

**Table 1** — *Materials parameters of soft and hard particles used in the simulation* [인쇄 · `tab_1.png`]

| Materials | Young's modulus Y/GPa | Poisson's ratio ν/- | Hardening index n/- | Strength coefficient C/MPa |
|---|---|---|---|---|
| Soft | 62.59 | 0.33 | 0.25 | 225.9 |
| Hard | 120 | 0.25 | 0.237 | 575.3 |

| 항목 | 값 | 표지 |
|---|---|---|
| 소재 이름 | 원문에 없다 ("soft" · "hard" 뿐) | [미확인] |
| 상수의 출처로 보이는 것 | 무름의 E 62.59 · C 225.9 = Huang 2017 의 Al 값과 같다 (n 은 0.25 ↔ Huang 0.05) · 단단의 C 575.3 · n 0.237 = Zhou 2019 의 Cu 값과 같다 (E 120 ↔ 128 · ν 0.25 ↔ 0.33) | [카드 대조] |
| 강도 · 강성 비 (단단 / 무름) | C 575.3 / 225.9 = **2.55** · E 120 / 62.59 = **1.92** | [카드 산술] |
| 입자 | 3D 구 · **무름 · 단단 모두 지름 1 mm** · 각 입자 독립 변형체 | [인쇄] |
| 조성 | **X_soft = 25 wt%** (그림 1 · 3) · 밀도가 없어 부피 · 수 분율은 모른다 | [인쇄] · 분율 [미확인] |
| 메시 | **구마다 요소 1014 · 절점 872** (그림 1b: 안쪽 정육면체 + 바깥 껍질 — 육면체 O-격자 꼴) | [인쇄] · 요소 꼴 이름 [미확인] |
| 부피 등가 해상도 | (1014 / (π/6))^(1/3) ≈ **12.5 요소 / 지름** | [카드 산술] |
| 입자 수 | **원문에 없다.**  그림 1a · 3a 에서 다이 안지름 ≈4 지름 · 충전 높이 ≈4.6 지름 · 초기 상대밀도 ≈0.48 로 어림하면 ≈50 개 | [판독 + 카드 산술 · 자릿수만] |
| 다이 | 원통 (그림 1a) · 강체 · 매끈 · 크기 [미확인] | [인쇄] · 크기 [미확인] |
| 재료식 | Eq. (2) σ_y = C(ε₀ + ε̄)ⁿ + D(ε̄̇)ᵏ (`eq_02_power_law_flow_stress.png`) · Eq. (3) von Mises · Eq. (4) 등가 변형률 속도 (변형률 텐서로 씀) · 초기 항복 변형률은 C · n · E 로 계산 | [인쇄] |
| 정식화 | Cauchy 응력 · 로그 변형률 · 갱신 라그랑주 · Eq. (5)–(13) (가상일 선형화 · 재료 · 기하 강성 K₁ + K₂ · Truesdell 응력률) | [인쇄] |
| 접촉 | 접촉 표 + **node-to-segment** | [인쇄] |
| 마찰 | Eq. (1) **σ_fr = −µ σ_n (2/π) arctan(v_r / rv_cnst) t** — rv_cnst = *"the relative velocity below which sticking occurs"* · 입자 간 **µ 0.2** · 다이 · 펀치 = 강체 · 매끈 (`eq_01_arctangent_regularised_coulomb_friction.png`) | [인쇄] · rv_cnst 값 · 벽 µ [미확인] |
| 경계 · 구동 | 강체 위 펀치에 변위 · 다이 벽과 아래 펀치 고정 · 밀도 변화 = 위 펀치 변위 · 속도 무관 재료 | [인쇄] · 펀치 속도 [미확인] |
| 하중 이력 | 압축 (7 · 50 · 100 · 200 MPa) → **하중 유지 (pressure holding)** → **탈압 (pressure releasing)** (그림 3e · f) | [인쇄] |

### 3-2. 압축 곡선 — 그림 2 (PDF 벡터 표식 판독)

| 압력 (MPa) | 모의 · 자연 충전 (□) | 모의 · 진동 (○) | 실험 · 자연 (△) | 실험 · 진동 (☆) |
|---|---|---|---|---|
| ≈0 | 0.474 → 0.496 (P ≈ 0–1) | 0.478 → 0.502 | 0.498 (3) | — |
| ≈12–17 | 0.534 (12) · 0.548 (17) | 0.548 (14) → **0.581 (15)** → 0.559 (16) | 0.534 (10) | 0.567 (17) |
| ≈25 | 0.563 (22) · 0.579 (28) | 0.604 (25) | 0.568 (25) | **0.603 (25)** |
| ≈37–40 | 0.613 (38) | 0.629 (40) | 0.625 (40) | **0.645 (37)** |
| ≈50 | 0.651 (53) | 0.643 (49) | 0.665 (52) | 0.669 (52) |
| ≈70–77 | 0.695 (77) | 0.685 (72) | 0.693 (70) | 0.702 (71) |
| ≈100 | 0.744 (102) | 0.742 (107) | 0.733 (96) | 0.743 (103) |
| ≈120 | 0.768 (118) | 0.758 (118) | 0.760 (122) | 0.761 (118) |
| ≈145–150 | 0.787 (136) | 0.794 (145) · 0.796 (150) | 0.786 (148) | 0.793 (143) |
| ≈170–185 | 0.807 (164) · 0.826 (185) | 0.810 (167) · 0.823 (182) | 0.812 (175) | 0.805 (169) |
| ≈195–200 | — | **0.837 (196)** | **0.838 (201)** | **0.828 (195)** |

- 표식 수: □ 21 · ○ 38 · △ 11 · ☆ 11 (범례 표식 제외).
- **진동 효과는 초반만** — 실험: 25 MPa 에서 +0.035 · 37–40 MPa 에서 ≈+0.02 · ≈120 MPa 위에서 같다.  모의: ○ 은 15 MPa 에서 한 번에 0.548 → 0.581 로 뛴다 (재배열 무너짐) · ≈90 MPa (0.719) 에서 □ 과 같아진다 [판독].  초록의 *"the relative density is much higher"* 는 이 그림으로는 초반에만 맞다.
- **모의 ↔ 실험**: 같은 압력에서 대체로 ±0.02 안 [판독] — 본문 *"in agreement"* 는 이 그림 범위에서 맞다.  단 실험 소재 · 방법이 없어 무엇과 맞췄는지 알 수 없다 (§10-B).
- P ≈ 0 의 출발점이 진동 유무에 상관없이 ≈0.47–0.50 이다 — 진동 충전의 '더 높은 초기 밀도' 가 그림에서는 보이지 않는다 [판독].

### 3-3. 미시 · 국소 (그림 3–6)

| 관측 | 내용 | 표지 |
|---|---|---|
| 압축 단계 (그림 3) | (a) 7 (b) 50 (c) 100 (d) 200 MPa (e) 하중 유지 (f) 탈압 · 색 띠 0–511.2 MPa · 'soft' 이름표가 붙은 구는 파랗고 (낮은 응력) 단단한 구가 붉다 · 노랑 (≈400–460 MPa) 은 단단한 구 | [인쇄 + 판독] |
| 다이 벽 쪽 | 벽에 닿은 부분은 곡면 → 평면 · 두 구의 변형량이 거의 같다 · 탈압 뒤 벽 근처 잔류 응력은 두 구가 거의 같다 | [인쇄] |
| 높이별 (그림 4 · 200 MPa) | (a) 위 (b) 가운데 (c) 아래 — **아래가 위보다 덜 조밀**하다 (단동 · 위에서 힘이 전달) · 위 펀치 가까운 무른 구일수록 더 변형 · 아래 무른 구의 변형은 주로 단단한 구 때문 | [인쇄] |
| 무른 구의 오목 | 단단한 구와 닿는 무른 구 표면은 안으로 오목 · 그 꼴은 이웃 공극으로 밀려 들어가기 어렵다 → 공극 채움을 막는다 | [인쇄] |
| 단일 입자 (그림 5) | ρ 0.64 · 0.74 · 0.84 에서 단단 · 무른 구 하나씩 — 단단한 구는 거의 변형하지 않고 색만 바뀐다 · 무른 구는 크게 변형 · 오목 | [인쇄] · 그림 5 곡선 = 진동 충전 모의 |
| 무른 구의 두 꼴 | 평평 = 무름–무름 접촉 (점 → 면) · 오목 = 무름–단단 접촉 | [인쇄] |
| 최대 응력 자리 | *"Highest stress regions occur in most cases at a grain boundary with large curvature after deformation."* (초록) · 단단한 구는 다른 단단한 구와 닿는 자리에서 모양 변화가 크다 | [인쇄] |

### 3-4. 입자 안 응력 단면 · 탈압 (그림 6–9 · ★ R4)

그림 7 · 8 의 거리 축 0–1 mm 는 지름을 따라간 위치 (가운데 = 0.5 mm · 세 축이 그 점에서 만난다) 로 읽힌다 [판독].

| 관측량 | P = 200 MPa | 탈압 뒤 | 표지 |
|---|---|---|---|
| 단단한 구 · 가운데 (0.5 mm) | **≈230 MPa** (본문 *"about 230 MPa"*) | **≈88 MPa** (본문 *"drops from 230 MPa to 80 MPa"*) | [판독 + 인쇄] |
| 단단한 구 · 범위 (세 축) | 178–339 MPa (본문 175–340 · 최대 = Z 축 위 표면 ≈340) | 56–244 MPa (본문 60–250) | [판독 + 인쇄] |
| 무른 구 · 가운데 | **≈180 MPa** (본문 *"about 175 MPa, which is 55 MPa lower than"* 단단) | **≈36–40 MPa** | [판독 + 인쇄] |
| 무른 구 · 범위 | 135–238 MPa (본문 137–240 · 최대 = 아래 표면 — 단단한 구에 눌린 오목) | 20–173 MPa (본문 25–175) | [판독 + 인쇄] |
| 가운데 응력 감소 | 단단 −62 % · 무름 −78 % | — | [카드 산술] |
| 절점 Node 17672 (무름 · 가운데 구 · 표면 최대) | 정점 ≈194 MPa (360 단계) | **≈190** (400 단계 · 본문 *"about 187 MPa"*) | [판독 + 인쇄] |
| 절점 Node 52206 (단단 · 가운데 구) | 정점 ≈372 (≈380 단계 · 선) · 299 (360) | **≈351** (본문 *"about 337 MPa"*) | [판독 + 인쇄] |
| 절점 Node 62086 (무름 · 벽 근처) | ≈166 (360) | **≈93** (본문 *"about 80 MPa"*) | [판독 + 인쇄] |
| 절점 Node 23250 (단단 · 벽 근처) | ≈435 (360) | **≈398** (선 끝 · 표식 없음 · 본문 *"about 385 MPa"*) | [판독 + 인쇄] |
| 무름 ↔ 단단 차이 | 같은 단계에서 가운데 ≈200 MPa · 벽 근처 ≈300 MPa (본문) · 단단은 가운데 ↔ 벽 차이가 크고 (최대 220 MPa) 무름은 작다 | — | [인쇄] |
| 하중 이력 길이 | 압축 + 유지 + 탈압이 증분 ≈400 단계 · 탈압은 마지막 ≈20–40 단계 (그림 9) | — | [판독] |

- ⚠ 본문은 *"the stress in the center of both soft and hard particles is reduced almost to zero"* 라 적었지만 그림 7b · 8b 의 가운데 값은 ≈88 · ≈40 MPa 다.  **숫자는 그림을 따른다.**
- 표면 최대 절점은 탈압에도 거의 안 빠진다 (단단 −6 … −9 % · 가운데 무름 −2 %) — 벽 근처 무름 절점만 −44 % [판독 + 카드 산술].  다이 벽이 옆을 잡은 채 (배출 없음) 하중만 뺀 상태다.

### 3-5. 이 논문에 **없는** 값

소재 이름 · 밀도 · 부피/수 분율 · 입자 수 · 다이 지름 · 충전 높이 · 펀치 속도 · 증분 크기 · rv_cnst · 벽 µ · 하중 유지 시간 · 탈압 방법 · **탈압 뒤 상대밀도 · 되튐** · 메시 수렴 · 요소 꼴 · DEM 코드 · 진동 조건 (진폭 · 진동수 · 시간) · 실험의 소재 · 분말 크기 · 다이 · 측정법 · 시드 반복.

---

## 4. 시뮬레이션 방법 ★

### 4-1. 흐름

1. **DEM 충전** — *"DEM dynamic modelling was employed to generate initial random packing structure"* · 자연 충전 + **기계적 진동** 충전 (*"in order to increase the loose density of the composite powder, mechanical vibration to the composite powder in the DEM simulation was applied"*) [인쇄].  DEM 코드 · 접촉 · 진동 매개변수 [미확인] — 저자들의 앞선 DEM 충전 연구 [24–27] 를 근거로 든다.
2. **FE 이식** — 구마다 메시 (1014 요소) · MSC.Marc 3D 모형.
3. **압축 → 하중 유지 → 탈압** — 위 펀치 변위 · 서버 계산.

### 4-2. 입자 처리 (DEM 판 "무질서 처리")

- **같은 크기 단분산 구 (1 mm)** · 두 재료 (무름 · 단단) · 무작위 충전 1 개씩 (자연 · 진동).
- **둘 다 탄소성 변형체** — 진짜 형상 소성 (무른 구 평탄화 · 오목 · 단단한 구도 접점에서 조금 변형).
- 다시 메시 · 요소 뒤틀림 처리 언급 없음.

### 4-3. 마찰 법칙 (Eq. 1)

- 아크탄젠트 정칙화 Coulomb: 상대 속도 v_r 이 rv_cnst 보다 작으면 마찰 응력이 v_r 에 거의 비례 (붙음 근사) · 크면 µσ_n 으로 포화 [인쇄 식 + 카드 해석].  MSC.Marc 의 표준 정칙화 꼴로 읽힌다 [추정].
- ⇒ 우리 2D F 팔 (겹치는 노드에서 접근하는 쌍의 비탄성 · 쿨롱 충격량 · `docs/reviews/suyoung_u6_first_development_20261118/README.md`) 과는 정칙화 방식이 다르다 — FE 팔을 짤 때 붙음 경계 (rv_cnst) 를 결과 전에 정해 적어야 같은 '마찰' 이 된다.

---

## 5. Figure set ★ (9 개 전부 + 표 1 · 식 2 개 — 모두 렌더해서 열어 봤다)

| Fig | 내용 | 우리가 참고할 점 |
|---|---|---|
| **1** ★ | (a) 원통 다이 속 DEM 충전 (무름 = 초록 · 단단 = 파랑 · 다이 = 갈색) (b) 구 하나의 메시 (안쪽 정육면체 노랑) (c) 진동 충전 (d) 자연 충전 | 입자 수 어림 (≈50) · 3D 육면체 O-격자 메시 |
| **2** ★★ | 압축 곡선 4 개 (모의 · 실험 × 진동 유무) 0–200 MPa | ★★ 벡터 판독표 §3-2 · 진동 효과는 초반만 · 모의 ↔ 실험 ±0.02 |
| **3** ★★★ | 압축 → 유지 → 탈압 6 단계 von Mises (X_soft 25 wt% · 진동) | ★★★ 응력 = 단단한 구 · 'soft' 구는 파랑 · 3D 형상 소성 |
| **4** ★★ | 200 MPa 압분체를 위 · 가운데 · 아래로 잘라 본 국소 구조 | ★★ 높이 밀도 차 (아래 < 위) — 우리 압밀 침대의 z 분포 판독과 같은 질문 |
| **5** ★ | ρ 0.64 · 0.74 · 0.84 의 단단 · 무른 구 하나씩 + 진동 모의 곡선 | 단단은 거의 안 변하고 무름은 오목 |
| **6** ★★ | 단단 (a · b) · 무름 (c · d) 구의 200 MPa ↔ 탈압 응력 (색 띠 두 개: 0–511 · 0–300 MPa) | ★★ 탈압 뒤 가운데가 빠지고 모서리에 남는다 · ⚠ (c)(d) 색 띠 눈금 "9.000e+002 · 6.000e+002" 는 9.0e+001 · 6.0e+001 의 인쇄 오류로 읽음 |
| **7** ★★ | 단단한 구의 세 축 von Mises 단면 (a) 200 MPa (b) 탈압 | ★★ 가운데 230 → ≈88 MPa [판독] |
| **8** ★★ | 무른 구의 세 축 단면 (a) 200 MPa (b) 탈압 | ★★ 가운데 ≈180 → ≈40 MPa [판독] |
| **9** ★★ | 절점 4 개 (무름 · 단단 × 가운데 · 벽 근처) 의 von Mises vs 증분 단계 0–400 | ★★ 표면 최대 절점은 탈압에도 거의 그대로 (벽 구속) |
| 표 1 | 두 재료 상수 | §3-1 · 같은 그룹 Al · Cu 값과 대조 |
| 식 (1) · (2) | 정칙화 마찰 · 멱경화 | `eq_*.png` |

---

## 6. Post-processing ★

| 무엇 | 어떻게 | 우리 대응물 |
|---|---|---|
| 압축 곡선 ρ(P) | 모의 · 실험 × 진동 유무 | 3D MPM wallP vs ε · DEM 압밀 곡선 |
| 응력장 3D 그림 | 압축 단계별 · 유지 · 탈압 von Mises 색 띠 | `viz_mpm_morphology.py` (단면) |
| 높이별 잘라 보기 | 200 MPa 압분체 위 · 가운데 · 아래 | 우리 침대 z 분포 (공극 · 응력) |
| 입자 안 단면 | 구 가운데를 지나는 X · Y · Z 축 위 von Mises (200 MPa · 탈압) | 없음 (MPM 은 입자별 장이 없다 · DEM 은 입자 안 응력이 없다) |
| 절점 이력 | 표면 최대 절점 4 개의 von Mises vs 증분 | 없음 |
| 도구 | MSC.Marc · DEM 코드 [미확인] | — |

---

## 7. 우리 DEM+MPM 대비  →  `comparison_vs_ours_DEM.md` · `our_dem_baseline.md` (⛔ 자리표시 — 우리 값은 CLAUDE.md · 리포 기록에서 직접)

### 7-0. 요약표

| 항목 | 이 논문 (3D MPFEM · 무름 + 단단) | 우리 | 판정 |
|---|---|---|---|
| 차원 · 규모 | 3D · ≈50 구 [판독 · 자릿수] | 3D DEM ≈33 k (real_14: AM 457 + SE 32,832) · 3D MPM 10⁷–10⁸ 점 | **우리 규모가 자릿수로 크다** — 3D MPFEM 은 작은 상자 검산 자리 (메모 3.2) |
| 단단한 상 | 소성 금속 (C 575.3 MPa) · 같은 크기 · 하중을 진다 | AM (NCM): DEM 강구 · 3D MPM 얼린 장애물 (하중 0) · 실물은 깨짐 | 방향만 (단단이 하중을 진다) — `huang2017_…` 와 같은 결론 |
| 무른 상 | Al 꼴 탄소성 · 오목 · 공극 채움 | SE: MPM J2 (E 1.53 · ν 0.49 · σ_y 0.30) · DEM 연화 탄성 | 같은 편 (MPM) |
| 크기비 | 1 (같은 크기) | AM : SE 지름 4–12 | ✗ |
| 단단 / 무름 강성 · 강도 | E 1.92 · 강도 2.55 | 실물 E ≈7.3 (Bazzoun 2026 입력 161.5 / 22.1) · AM 은 거의 항복 안 함 | ✗ — 이 논문의 '단단' 은 덜 단단하다 |
| 탈압 | ✅ 유지 → 탈압 · 입자 안 단면 | ❌ (2D 단계 6 미수행 · 3D hold) | **그들 우세** |
| 밀도 끝 | ≈0.84 (200 MPa) | 3D MPM 의 기공 값은 정지 규약에 매인다 (CLAUDE.md SE-DUMP 절 정정 · R1 정직 준정적 = ε_sphere 1.13 % 과압축) · 랩 표준 = 순수 SE 기공 10–13 % · 진밀도 1.64 | 압력 · 재료가 달라 비교 안 함 |
| 실험 | 압축 곡선 4 개 · 소재 미기재 | 랩 표준 (순수 SE 기공 10–13 % · 진밀도 1.64) | 그들의 '검증' 은 대상이 불분명 |

### ★ 7-A. (나) 단단 + 무른 짝 — AM + SE 에 옮길 것

| 이 논문의 기전 | 우리 계의 읽기 | 옮김 |
|---|---|---|
| 응력이 단단한 구에 모인다 (그림 3 · 9 — 단단 절점이 무름보다 ≈200–300 MPa 높다) | 단단 상이 하중을 진다 = MPM DO-NOT ② 의 반대 극 (`huang2017_…` §7-B 와 같은 방향) | **방향 ✅** |
| 단단에 눌린 무른 표면이 **오목** → 이웃 공극으로 못 들어간다 | AM 이 SE 를 누르는 자리에서 SE 가 AM 둘레를 감싸고 (envelop) 공극 쪽으로는 덜 흐를 수 있다 → 복합 기공 바닥의 형상 기전 후보 | 방향 ✅ · **[추정 · 우리 MPM 에서 같은 꼴이 나오는지 그림으로 확인할 것]** |
| 무른 구가 단단한 구를 감싼다 (*"soft particles exhibit large plastic deformation and can envelop the hard particles"*) | SE 가 AM 을 덮는 피복 (coverage) 의 형상 쪽 기전 | 방향 ✅ · 값 ✗ |
| 높이 밀도 차 (아래 < 위 · 매끈한 벽에서도) | 단동 압축의 z 기울기 — 우리 DEM · MPM 침대의 z 분포 판독 | 방향 ✅ (금속 · 매끈 벽 · 50 구 한정) |

### ★ 7-B. 탈압 (R4) — 이 논문이 더하는 것

- **3D 입자 안 잔류 응력**: 가운데가 빠지고 (단단 −62 % · 무름 −78 % [판독 + 카드 산술]) 모서리 · 오목 · 접점에 남는다 — Zhou 2019 (2D) 의 *"maximum stress at the particles' edges"* 와 같은 방향.
- **표면 최대 절점은 탈압에도 거의 그대로** (단단 −6 … −9 % [판독]) — 다이 벽이 잡은 채 하중만 뺀 상태 (배출 없음).  우리 탈압 팔을 등록할 때 '하중 0 (벽 구속)' ↔ '배출 (벽 제거)' 을 따로 적어야 잔류 응력 · 되튐을 견줄 수 있다 [추정].
- **되튐 숫자는 없다** — 2D (Zhou) 처럼 패널 높이로 읽을 그림도 없다.

### 7-C. 판정 (frame [4] · [5])

- frame [5]: 역학 쪽만 (형상 · 응력 · 탈압) · 전달 0.
- frame [4]: 실험 대조가 소재 미기재라 교차검증으로 쓸 수 없다.  우리 쪽에서는 **기전 · 설정 · 탈압 관측량의 선례**로만.

---

## 8. 적용 인사이트 (실행 가능한 순서)

1. **3D 작은 상자 검산 (비교 문서 C 절 PyCompact 항목 ⑥ 의 '소형 SE-only REV 100–500 입자' · 메모 3.2 `docs/reviews/dem_redesign_direction_20261109/memo_v3_2.md`) 의 규모 근거** — 이 논문 3D 는 ≈50 구 [판독] · 구당 ≈12.5 요소/지름.  우리 MPFEM 검산 상자도 이 자릿수에서 시작해야 비용이 맞는다.
2. **우리 MPM 에서 '오목' 꼴을 찾는다** — scaffold MPM (AM 얼림) 의 SE 단면에서 AM 에 눌린 SE 표면이 오목해지는지 그림으로 본다 (새 계산 0 · 기존 결과 그림 판독) [추정].
3. **탈압 팔 등록 항목에 '입자 안 단면' 추가** — 입자별 장 (F) 이 생기면 입자 가운데 · 표면 응력 단면을 같은 꼴 (세 축 · 가운데 0.5 지름) 로 낸다.
4. **마찰 법칙 명시** — FE 팔이 정칙화 Coulomb 를 쓰면 rv_cnst 를 결과 전에 적는다 (우리 F 의 충격량 마찰과 다르다).
5. **진동 (충전 상태) 효과는 초반만** — 믹싱 · 충전 상태가 압밀 끝 밀도를 바꾼다는 주장을 이 논문으로 세우지 않는다 (끝에서 모인다).

---

## 9. 인용 가능 문장 (deck/paper 용)

- *"the limitation of DEM is that it is only suitable for the simulation of small deformation particle accumulation, and it is difficult to simulate the formation of particles with large plastic deformation; in particular when the packing density of particles exceeds 0.85, it is very difficult to implement DEM [28]."* (p.2) — 2 차 인용 (원전 [28] = Martin & Bouvard 2004).
- *"The irregular particle shape produced by this depression is difficult to squeeze into the adjacent pores inside the compact, which hinders further filling of the pores."* (p.5) — 무른 입자 오목의 기전.
- *"soft particles exhibit large plastic deformation and can envelop the hard particles. In this case, the maximum stress is concentrated in the depression of soft particles."* (p.7).
- 우리 문장 (한정어 포함): "같은 크기의 무른 + 단단한 금속 구 ≈50 개 (그림 판독) 의 3D MPFEM (Li 외 2022) 에서 탈압 뒤 입자 가운데 응력은 단단한 구 ≈230 → ≈88 MPa · 무른 구 ≈180 → ≈40 MPa 로 빠졌고 (그림 7 · 8 판독) 모서리 · 접점에 잔류 응력이 남았다."

---

## 10. 주의 / 한계 (over-claim 방지 + **이 논문에 대한 비판**)

### 10-A. 우리가 전이할 때의 한계

- **소재**: 이름 없는 두 금속 (Al 꼴 · Cu 꼴 상수) ≠ NCM811 + LPSCl.  '단단' 도 소성 금속이고 같은 크기다.
- **규모**: ≈50 구 · 벽 효과가 큰 원통 다이 — 우리 주기 RVE (real_14) 와 다르다.
- **압력**: ≤ 200 MPa · 끝 밀도 ≈0.84 — 우리 300 MPa · 기공 10–16 % 영역 밖.
- **탈압 = 벽 구속 하중 0** · 배출 없음.

### 10-B. ★ 이 논문 자체의 약점 (비판적으로)

1. **실험이 무엇인지 없다** — *"corresponding physical experiments were carried out"* 만 있고 소재 · 분말 · 다이 · 진동 · 밀도 측정이 없다.  그림 2 의 '일치' 를 검증으로 읽을 수 없다.
2. **소재 이름 · 밀도가 없다** — X_soft 25 wt% 를 부피 · 수로 바꿀 수 없다.  상수는 같은 그룹의 Al (Huang 2017) · Cu (Zhou 2019) 값과 숫자가 같지만 n · E · ν 일부가 다르다 (§3-1).
3. **본문 ↔ 그림 어긋남** — 가운데 응력 *"reduced almost to zero"* ↔ 그림 7b · 8b ≈88 · ≈40 MPa.  초록의 진동 *"relative density is much higher"* ↔ 그림 2 의 끝 밀도 차 ≈0.
4. **참고문헌 번호가 어긋난다** — *"Only Wu et al. [40]"* 의 [40] 은 Güner 외 (Wu 외는 [41]) · *"our previous 2D simulation of composite powder [44, 45]"* 의 [44] 는 Harthong 외 2012 (저자들 논문 아님) · *"our previous two-dimensional simulation results [40, 44]"* 도 Güner · Harthong 이다.  인용 번호로 원전을 찾을 때 한 칸씩 확인한다.
5. **그림 6 (c)(d) 색 띠 눈금 오류** — 0–300 MPa 띠에 "9.000e+002 · 6.000e+002" (9.0e+001 · 6.0e+001 이어야 한다).
6. **메시 수렴 · 시드 반복 없음** — 구당 ≈12.5 요소/지름 하나 · 충전 1 개씩.  `demirtas2021_…` 은 3D 에서 접촉 면적이 3,363 요소/입자에서도 수렴하지 않았다고 보였다.
7. **재현 값이 빠졌다** — 입자 수 · 다이 크기 · 펀치 속도 · rv_cnst · 진동 조건 (§3-5).

### 10-C. frame 규율 재확인

- 이 논문 값으로 우리 MPM · DEM 을 보정하지 않는다 (frame [4]).  3D 결과도 2D 결과처럼 '같은 꼴' 의 선례로만 쓴다.

---

## 11. 관련 카드 (중복 서술 금지 — 겹치면 넘김)

- `zhou2019_mpfem_2d_copper_powder_die_compaction_release` — 같은 그룹 2D Cu (단일) · 탈압 · 높이 되튐 판독 · node-to-segment.
- `huang2017_mpfem_2d_binary_al_sic_hard_soft_compaction` — 2D 단단 (탄성 SiC) + 무름 (Al) · 정렬 ↔ 무작위 · 이 논문의 [23].
- `demirtas2021_mpfem_hollow_sphere_die_compaction` — 3D MPFEM (Abaqus/Explicit) 411–1979 입자 · 메시 수렴 · 되튐.
- `pycompact2025_dem_mpfem_workflow` — LIGGGHTS → 3D MPFEM 403–1033 입자 · 가압 + 제하 · 되튐 ≈ 재료 P/K 의 8 배.
- `cardenasbarrantes2022_soft_spheres_3d_compaction_nscd` — 3D 탄성 구 50 · 100 개 NSCD (같은 규모 자릿수).
- `martinbouvard2003_dem_composite_cold_compaction` — 무른 + 단단 DEM (이 논문 [28] 의 짝 논문).
- `singer2022_partitioned_mpm_dem_coupling_kratos` — 같은 날 묶음의 넷째: 강체 (DEM) + 연속체 (MPM) **분할 결합** (KRATOS) · 메모 3.2 후보 A 와 물리 짝은 같고 결합 알고리즘은 다름 · MPFEM 이 아니다.

---

## 12. 용어 (technique mini-glossary)

- **3D MPFEM** — 구마다 3D FE 메시 (여기서는 육면체 O-격자) + 접촉.
- **아크탄젠트 정칙화 Coulomb 마찰** — σ_fr = −µσ_n (2/π) arctan(v_r/rv_cnst) t.  미끄럼 속도가 rv_cnst 보다 작으면 마찰이 속도에 비례 (붙음 근사).
- **하중 유지 (pressure holding)** — 목표 압력에서 펀치를 멈춰 둔 단계.
- **탈압 (pressure releasing)** — 펀치 하중을 0 으로 빼는 단계 (배출 아님 · 다이 벽은 그대로).
- **진동 충전** — DEM 충전 중 기계적 진동으로 다리 · 아치 구조를 깨 초기 밀도를 올리는 방법.
- **X_soft** — 무른 입자의 질량 분율 (wt%).

---

## 🗨️ Q&A 로그

- (2026-11-25 · litdb-curator) 입자 수는 원문에 없어 그림 1a · 3a 의 다이 안지름 ≈4 지름 · 높이 ≈4.6 지름 · 초기 밀도 ≈0.48 로 어림했다 (≈50 · 자릿수만).  그림 2 · 7 · 8 · 9 의 숫자는 PDF 벡터 표식에서 읽은 값이라 원고에 인쇄값처럼 옮기지 않는다.
