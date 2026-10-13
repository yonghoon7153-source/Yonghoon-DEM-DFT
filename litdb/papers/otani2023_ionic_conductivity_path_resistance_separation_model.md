<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 사용자가 특히 원한 항목. 깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md ·
     형식 이웃 = asano2017_ncm111_li3ps4_composite_electronic_ionic_conductivity.md (τ 묶음) · nakamura2020_dry_coating_ncm_li3ps4_core_shell.md (같은 날).
     쪽 표기 = 본문 "p.N" (PDF N 쪽 = 학술지 인쇄 쪽 N, 1–6).  SI 없음 (본문도 SI 를 인용하지 않는다).
     값 표지: [인쇄] = 본문 · 그림 안에 숫자로 적힌 값 · [판독] = 그림에서 읽은 값 (litdb/figures/<slug>/digitized.csv — Fig 4 · 6 원 래스터 300 dpi,
     색 마스크 + 거리변환 정점) · [우리 산술] = 인쇄값 · 이 논문 식으로 우리가 다시 한 계산 · 우리 자료와 엮은 계산 · [추정] = 우리 해석 ·
     [미확인] = 원문 (본문 6 쪽 전수) 에 없음.  원문 6 쪽 텍스트 층 전수 + 그림 7 장 전부 렌더로 열람. -->

# 황화물 복합양극의 이온전도 저하 인자를 셋으로 가르고 (공극 우회 · 입자 접촉 면적 · 계면 접촉 저항) "경로 저항 계수" 곱 모형으로 예측 — 순수 LPSCl 층은 Bruggeman β = 4 (공극 30 % 에서 경로 저항 ≈3 = 경로 ≈1.2 × 접촉 면적 ≈2.5 · 격자 부정합 저항은 무시 가능) · 복합 = AM 우회 (β 1.5) × SE 안 공극 우회 (β 4) — SE 54 · 35 % 에서 실측과 일치, 21 % 저공극 · 10 % 에서 어긋남 — Kazufumi Otani · … · Gen Inoue (LIBTEC · 규슈대, J. Energy Storage 2023)

> slug `otani2023_ionic_conductivity_path_resistance_separation_model` · DOI `10.1016/j.est.2022.106279` · type `exp + 해석 모형 (LPSCl 층 · NCM523 복합 공극률 열 EIS · 2D SEM 무작위 행보 경로 저항 계수 · 경로 저항 분리 곱 모형; DEM/MPM 없음)` · PDF `5d4c2f6e-46._Ionic_conductivity_prediction_model_for_composite_electrodes_and_quantification_of_ionic_conductivity_reduction_factors_in_sulfide-based_all-solid-state_batteries.pdf` · digested `2026-10-13` · status ✅
>
> **원제**: *Ionic conductivity prediction model for composite electrodes and quantification of ionic conductivity reduction factors in sulfide-based all-solid-state batteries* (p.1)
> **저자 · 소속 (p.1)**: Kazufumi Otani ᵃ · Takahisa Muta ᵃ · Terumi Furuta ᵃ · Takuhiro Miyuki ᵃ · Tomohiro Kaburagi ᵃ · **Gen Inoue ᵇ\*** (\* 교신 ginoue@chem-eng.kyushu-u.ac.jp)
> ᵃ Consortium of Lithium-Ion Battery Technology and Evaluation Center (LIBTEC), Ikeda, Osaka · ᵇ Department of Chemical Engineering, Faculty of Engineering, Kyushu University, Fukuoka
> *J. Energy Storage* **58** (2023) 106279 · 접수 2022-04-27 · 수정 2022-10-03 · 승인 2022-11-26 · 온라인 2022-12-15 (p.1) · NEDO SOLiD-EV 과제 · 이해상충 없음 · **데이터 = 기밀 ("confidential")** (p.5) · 기여: 개념 · 작성 · 방법 · 소프트웨어 · 해석 = K. Otani / 조사 · 자료 = T. Muta · T. Furuta · T. Miyuki · T. Kaburagi / 지휘 · 연구비 = G. Inoue (p.5).
> **같은 계보 · 같은 축 카드 (링크만)**: 같은 교신 (G. Inoue, 규슈대) 의 DEM 계보 [`so2021_dem_mold_pressure_assb_coldpress`](so2021_dem_mold_pressure_assb_coldpress.md) (ref 7) · [`so2022_dem_compaction_coated_particles_assb`](so2022_dem_compaction_coated_particles_assb.md) (ref 10) · [`so2022_dem_contact_model_assb_compaction_sintering`](so2022_dem_contact_model_assb_compaction_sintering.md) · 1저자의 후속 DEM [`otani2025_dem_se_dispersion_aggregation_compression`](otani2025_dem_se_dispersion_aggregation_compression.md) · 측정 방법 [`siroma2015_transmission_line_model_porous_electrode_impedance`](siroma2015_transmission_line_model_porous_electrode_impedance.md) (ref 18) · 문헌 대조 [`asano2017_ncm111_li3ps4_composite_electronic_ionic_conductivity`](asano2017_ncm111_li3ps4_composite_electronic_ionic_conductivity.md) (ref 5) · [`hlushkou2018_void_space_ion_transport_assb_cathode`](hlushkou2018_void_space_ion_transport_assb_cathode.md) (ref 4) · [`minnmann2021_jes_charge_transport_bottlenecks`](minnmann2021_jes_charge_transport_bottlenecks.md) (ref 6) · [`tjaden2018_tortuosity_review_calculation_approaches`](tjaden2018_tortuosity_review_calculation_approaches.md) (ref 21) · [`shi2019_high_am_loading_particle_size_assb`](shi2019_high_am_loading_particle_size_assb.md) (ref 25) · 이 논문을 인용하는 카드: [`miss2026_insitu_conductivity_porosity_pressure_compaction`](miss2026_insitu_conductivity_porosity_pressure_compaction.md) (ref 26) · [`lee2024_multiphysics_dem_fem_initial_pressure_assb`](lee2024_multiphysics_dem_fem_initial_pressure_assb.md) (§10-1 — 선형식 귀속 문제).
> **판독 원자료**: `litdb/figures/otani2023_ionic_conductivity_path_resistance_separation_model/digitized.csv` (71 행 — Fig 4 순수 SE 층 · Fig 6 복합 네 조성) · 크롭 7 장 `figures.json`.

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: 같은 아지로다이트 LPSCl (Mitsui, D50 0.7 µm, 재료 σ ≈2×10⁻³ S cm⁻¹) 의 순수 층을 압력 열로 다공도만 바꿔 재면 σ 가 **σ₀(1−p)⁴ (Bruggeman β = 4)** 를 따르고, 같은 층의 2D SEM 단면에서 무작위 행보로 낸 "경로 저항 계수" 가 실측 σ 를 재현하므로 **입자 계면의 격자 부정합 저항 (③) 은 무시할 만하고, 저하의 대부분은 입자 접촉 면적 (② 목) — 공극 30 % 에서 경로 ≈1.2 × 접촉 면적 ≈2.5 = ≈3** 이라고 판정한다 (p.4).  복합양극은 **τ_all = τ_macro (AM 우회, β 1.5) × τ_micro (SE 안 공극 우회, β 4)** 로 예측하며 SE 54 · 35 vol% (고체 기준) 에서 실측과 맞고, 21 % 저공극 · 10 % 에서 어긋난다 (Fig 6).  **이 τ 는 우리 수송 tortuosity (tau2) 와 정의가 같다** — 이 모형을 우리 ps45 다섯 침대 (φ_SE · ε_sphere) 에 넣으면 tau2 가 우리 Hertz 망 값의 **0.94–1.02 배** [우리 산술].

| 우리 질문 | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① 그들 τ 는 우리 어느 양 | 경로 저항 계수 τ_L/S 의 정의 = **σ_eff = σ₀ ε_SE / τ_L/S_all** (식 4) → τ_L/S_all = ε_SE σ₀/σ_eff = 우리 **tau2 (수송 tortuosity)** 와 같은 식 · ⚠ 식 1 (τ = l/L, 기하) 을 식 2 (σ = σ₀ε/τ) 에 그대로 넣어 **기하 τ 와 tortuosity factor 를 한 기호로 섞는다** (우리 τ 명명 규약이 막는 바로 그 혼동) | [인쇄] p.1 · p.3 |
| ② ★ 우리 tau2 분해와의 정량 대조 | 그들: tau2 = τ_macro (AM 우회) × τ_micro (공극 · 목) / 우리 (ps45 Hertz): tau2 = tau2_CF (협착 뺀 같은 망) × 모형 내부 협착비 σ_CF/σ_FULL.  [우리 산술] 우리 침대에 그들 식을 넣으면 **총 tau2 는 거의 같고 (0.94–1.02 배, ε_sphere 기준) 나눔은 다르다** — 그들 τ_macro 1.45–1.49 ↔ 우리 CF 1.25–1.79 · 그들 τ_micro 3.4–4.7 ↔ 우리 협착비 3.92–4.24 (§7-2 표) | §7-2 [우리 산술] |
| ③ 실험 앵커 (우리 대칭셀 계획 조성) | **SE 35 vol% (고체 기준) 복합의 실측 σ** — 공극 14.6–18.7 % 에서 **0.075–0.13 mS cm⁻¹** [판독 Fig 6] ↔ ps45 (SE/고체 ≈35 vol% · ε_sphere 15.0–19.2 %) Hertz σ_ion **0.059–0.089 mS cm⁻¹ @ σ₀ 1.5** · 그들 재료 σ₀ 2.0 으로 다시 매기면 0.078–0.119 [우리 산술] | [판독] Fig 6 · [우리 산술] |
| ④ "접촉 저항" 이 정말 0 인가 | 순수 층에서 그림 기반 계수가 실측과 맞으므로 **③ 격자 부정합 저항 무시 가능** (황화물은 입계 저항이 작다는 refs 7 · 22 와 같은 방향) — 단 ② 접촉 면적 (목) 이 가장 큰 인자 | [인쇄] p.4 · p.5 |
| ⑤ 이종기술 논지 (분산) | 모형은 SE 분포 · 응집을 **입력으로 갖지 않는다** (ε 와 공극만) — 가정 셋 (SE ≪ AM · 경로 끊김 무시 · 전극 안 분포 무시) ⇒ **같은 ε · 공극에서 분산 효과가 0 인 귀무 모형**으로 쓸 수 있다 [추정].  [우리 산술] Nakamura 2020 의 두 전극 (같은 SE 량 · 코팅 vs 혼합) 에 넣으면 이 모형은 **혼합 τ 8.5 (측정 복셀 8.86) 와 맞고 코팅 τ 는 9.7 로 예측하는데 측정은 5.49** — 코팅 효과는 이 귀무 모형 밖에 있다 (§7-3) | p.4 · [우리 산술] |
| ⑥ `lee2024_multiphysics_…` 카드의 선형식 τ = −11.7·ε_SE + 8.54 (그 카드가 "Otani 2023 ref 46" 으로 적음) | **이 논문 본문 · 그림 어디에도 없다** — 식은 식 1–9 (Bruggeman 두 개의 곱) 뿐 · 그림 7 장에 맞춤 직선 없음.  [우리 산술] 이 논문 모형을 공극 10 % 에서 SE 21–54 % 사이 직선으로 근사하면 기울기 ≈ −15 · 절편 ≈ 9.4 — 같은 자릿수 ⇒ Lee 2024 가 Otani 모형 · 자료에 맞춘 식일 수 있다 [추정 — Lee 2024 원문 ref 46 · 식 38 근거 확인 전] | 본문 · 그림 전수 · §10-1 |

⛔ **한정어 (떼지 말 것)**: ① 재료 = Mitsui LPSCl (x ≈1, D50 0.7 µm, σ "~2×10⁻³" = 공급처 값) · NCM523 (Sumitomo, D50 5.02 µm, 단봉) — 우리 NCM811 바이모달 아님 ② 복합 = **막자 혼합** · 압력 열로 공극을 바꿈 · 측정은 SUS 사이 **전자–전자 연결형 EIS (Siroma TLM)** ③ β = 4 는 **순수 층에 맞춘 값** (복합에는 그대로 옮김) · β 1.5 는 구형 AM 가정 ④ 경로 저항 계수는 **2D SEM 단면 · 무구속 시료** (공극률이 측정 상태와 다름 — 이진화 공극을 씀) ⑤ 표본 · 반복 · 오차 [미확인] · **데이터 기밀**.

---

## 1. 한 줄 요약

황화물 전고체 전극의 이온전도도가 재료값보다 크게 떨어지는 이유를 ① 공극을 피해 도는 경로 ② 입자 사이 접촉 면적 (병목) ③ 계면 격자 부정합에 의한 접촉 저항 세 가지로 나누고 (Fig 1), ①②를 "경로 저항 계수 (path resistance coefficient, τ_L/S)" 로 묶는다.  순수 LPSCl 층을 0.4 → 6.0 t f cm⁻² 로 다시 눌러 가며 공극률별 σ 를 재고 (Fig 4), 2D SEM 이진화 단면 (Fig 5) 에서 무작위 행보로 경로 저항 계수를 내니 실측과 맞아 ③ 은 무시 가능 · 공극 30 % 에서 계수 ≈3 (경로 ≈1.2 × 접촉 면적 ≈2.5) · 전체는 Bruggeman β = 4 로 맞는다.  복합양극은 "AM 을 피하는 거시 경로 (공극 무시, β 1.5)" × "그 경로 안에서 공극을 피하는 미시 경로 (β 4)" 의 곱 (식 9) 으로 예측 — SE 54 · 35 % 에서 실측과 맞고, 21 % 의 저공극 영역은 AM 변형으로 거시 β 가 1.5 보다 커져 어긋나며, 10 % 는 퍼콜레이션 붕괴로 실측이 훨씬 낮다 (Fig 6).  공극 9 % 에서 SE 54 % 는 AM 우회 1.3 · 공극 우회 1.7, SE 21 % 는 1.9 · 3.2 (Fig 7) — AM 이 많아질수록 공극 쪽 벌점이 커지므로 고에너지 전극일수록 공극을 줄여야 한다.

## 2. 메타

| 저자 | 저널/년 | DOI | 소재 (SE/CAM) | 연구유형 |
|---|---|---|---|---|
| K. Otani · T. Muta · T. Furuta · T. Miyuki · T. Kaburagi (LIBTEC) · **G. Inoue\*** (규슈대 화공) | *J. Energy Storage* 58 (2023) 106279 | 10.1016/j.est.2022.106279 | **아지로다이트 Li(7−x)PS(6−x)Clx (x ≈1)** (Mitsui Mining & Smelting · 1.8 g cm⁻³ · ≈2×10⁻³ S cm⁻¹ · D50 0.7 µm) · **LiNi₀.₅Co₀.₂Mn₀.₃O₂** (Sumitomo Metal Mining · D10 4.09 · D50 5.02 · D90 6.29 µm · 부피 평균 5.12 µm) · 도전재 · 바인더 없음 | 실험 (순수 SE 층 · 복합 공극률 열 EIS) + 2D 이미지 무작위 행보 + **해석 모형** (경로 저항 분리).  **DEM · MPM · 3D 시뮬 없음** |

- 키워드 (p.1): Ionic conductivity · All-solid-state battery · Path-resistance-separation model.

---

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. 재료 · 시료 · 측정 (p.2–3)

| 항목 | 값 | 표지 · 쪽 |
|---|---|---|
| SE | 아지로다이트 Li(7−x)PS(6−x)Clx (**x ≈1**) · 밀도 **1.8 g cm⁻³** · σ **≈2×10⁻³ S cm⁻¹** · D50 **0.7 µm** (Mitsui Mining & Smelting) · SEM 사진 (Fig 2, 1 µm 막대) = 1 µm 안팎의 덩이진 입자 | [인쇄] p.2 · [판독 · 정성] Fig 2 |
| CAM | LiNi₀.₅Co₀.₂Mn₀.₃O₂ (Sumitomo Metal Mining) · D10 4.09 · D50 5.02 · D90 6.29 µm · 부피 평균 5.12 µm | [인쇄] p.2 |
| 순수 SE 층 | Ar 글러브박스 (이슬점 < −80 °C) · SUS 판 사이 **0.2 t f cm⁻²** 펠릿 → 성형 압력을 **0.4 → 6.0 t f cm⁻²** 로 올리며 반복 측정 → 다공도 열 · 측정 = 건조실 (이슬점 < −60 °C) EIS + **구속 상태 두께** · 공극률 = 두께 + 재료 밀도 | [인쇄] p.2 |
| 압력 환산 | 0.2 t f cm⁻² ≈ **20 MPa** · 0.4 ≈ 39 MPa · 6.0 ≈ **588 MPa** (1 t f = 9.80665 kN) | [우리 산술] |
| 복합 | 막자 혼합 · SE 부피 **54 · 35 · 21 · 10 %** (NCM 46 · 65 · 79 · 90 %) — **고체 기준** · 공극률은 전체 부피 기준 · 같은 압력 열로 재측정 | [인쇄] p.2–3 |
| 복합 측정 | SUS 사이 **전자–전자 연결형 EIS** (Siroma 외 refs 17 · 18 — TLM) · 공극률 = 두께 + 두 재료 밀도 | [인쇄] p.2–3 |
| 경로 저항 계수 (그림) | CROSS SECTION POLISHER (JEOL) 단면 → FE-SEM → SE / 공극 이진화 → **무작위 행보자 200 개**를 그림 중앙 근처에서 상하좌우 한 화소씩 → 일정 거리까지의 평균 걸음 수 (장애물 있는 그림 ÷ 빈 공간) · 공극 화소로 가면 이전 자리로 되돌아감 · 공극률 = **이진화 그림에서** (SEM 시료는 구속 못 해 측정 공극률과 다름) | [인쇄] p.3 |
| 그림 크기 · 화소 · 시료 수 · 반복 | [미확인] | — |

### 3-2. ★ 모형 — 식 1–9 (p.1–3)

- 식 1: **τ = l/L** (경로 길이 ÷ 두께) · 식 2: **σ_eff = σ₀ ε/τ** · 식 3: **τ = ε^(1−β)** (Bruggeman — 구형 장애물이면 β = 1.5, 누른 납작한 장애물이면 β 증가 · 액체 LIB 양극 ≈1.5 (ref 16) · 전고체 ≥ 3 (refs 3 · 4)) [인쇄 p.1–2].
- 경로 저항 계수 τ_L/S: ①② 의 저항 증가율을 "겉보기 tortuosity" 로 둔 양 — 단면적 감소를 경로 증가로 본다 [인쇄 p.2].
- **경로 저항 분리 모형** (Fig 3): 전체 경로 (a) = AM 을 피하고 공극은 무시하는 **거시 경로** (b) 와, 그 거시 경로 안에서 SE 의 작은 공극을 피하는 **미시 경로** (c) 로 나눈다.
  - 식 4: σ_all = σ₀ ε_SE / τ_L/S_all · 식 5: σ_all = σ_macro ε_macro / τ_L/S_macro · 식 6: σ_macro = σ₀ ε_micro / τ_L/S_micro · 식 7: **ε_macro = ε_SE + ε_void** · 식 8: **ε_micro = ε_SE / (ε_SE + ε_void)** · 식 9: **τ_L/S_all = τ_L/S_macro × τ_L/S_micro** [인쇄 p.3].
  - 적용: 거시 = Bruggeman **β = 1.5** (구형 AM, 액체 양극과 같게) · 미시 = 순수 SE 층 실측에 맞춘 **β = 4.0** [인쇄 p.4].
  - 가정 셋: ① SE 입자가 AM 보다 충분히 작다 ② 경로 끊김 (퍼콜레이션) 기여 무시 (SE 부피분율이 작아도) ③ 전극 안 분포 무시 [인쇄 p.4 · p.5].
- [우리 산술] 식 4–9 를 합치면 **f = σ_all/σ₀ = ε_SE^4 × (ε_SE + ε_void)^(−2.5)** · τ_all = (ε_SE+ε_void)^(−0.5) × (ε_SE/(ε_SE+ε_void))^(−3).

### 3-3. ★ 순수 SE 층 (Fig 4 · Fig 5 · p.4)

- 실측 (파랑) · 경로 저항 계수로 낸 계산 (빨강) · Bruggeman β = 4 곡선 (점선) 이 0–41 % 공극에서 겹친다 [판독].  곡선 절편 **2.0×10⁻³ S cm⁻¹** (공극 0) [판독].
- [판독 Fig 4] 실측: 공극 3.0 % 1.71 · 5.4 % 1.42 · 8.2 % 1.69 · 19.1 % 0.92 · 25.0 % 0.56 · 29.0 % 0.46 · 34.9 % 0.32 · 40.8–41.0 % 0.24–0.28 (×10⁻³ S cm⁻¹) · 계산: 3.9 % 1.55 · 11.7 % 1.53 · 13.9 % 0.92 · 19.9 % 0.77 · 30.6 % 0.40.
- 본문: *"Approximately a 20 % decrease in porosity results in a 50 % increase in ionic conductivity"* (기준 공극이 없어 상대 · 절대 판독이 모호 — §10-4) · 그림 계수가 실측과 맞으므로 *"the influence of the third factor in lowering the conductivity is considered to be negligible"* (refs 7 · 22 의 황화물 입계 저항 무시와 정합) [인쇄 p.4].
- 공극 30 %: 경로 저항 계수 **≈3** · 그중 **① 경로 (tortuosity) ≈1.2 · ② 접촉 면적 ≈2.5** (Fig 5 — 이진화 단면 · 이온 경로 그림) [인쇄 p.4].  [우리 산술] β 4 식으로 (0.7)^(−3) = **2.92** · 1.2 × 2.5 = 3.0.
- β = 4 의 뜻: 압력으로 공극 부피는 줄지만 공극 모양 특성은 크게 안 바뀌어 β 가 일정 · 구형 장애물의 1.5 보다 큰 것은 공극이 전도를 막기 쉬운 모양이라서 [인쇄 p.4].
- *"For full utilization of the ionic conductivity of the SE material in the electrode, the contact area between the SE particles should be increased"* [인쇄 p.4].

### 3-4. ★ 복합양극 — 실측 vs 모형 (Fig 6 · p.4)

[판독 Fig 6 — 공극 % : σ (S cm⁻¹), 마커 중심]:

| SE (고체 기준 vol%) | 실측 점 | 모형과 |
|---|---|---|
| 54 % | 8.1 : 3.0e-4 · 8.9 : 3.5e-4 · 10.8 : 2.3e-4 / 3.9e-4 · 13.2 : 2.8e-4 · 13.4 : 3.2e-4 · 15.5 : 3.2e-4 · 18.4 : 1.8e-4 · 19.7 : 2.2e-4 · 24.6 : 1.7e-4 · 28.0 : 1.3e-4 · 33.0 : 8.1e-5 · 33.5 : 7.3e-5 | 일치 [인쇄] |
| **35 %** | 7.2 : 1.7e-4 · 8.6 : 9.4e-5 · 9.3 : 1.3e-4 · 10.1 : 1.1e-4 · 11.7 : 1.2e-4 · 12.4 : 1.1e-4 · **14.6 : 1.3e-4 · 14.9 : 1.0e-4 · 18.2 : 8.9e-5 · 18.7 : 7.5e-5** · 26.6 : 3.0e-5 · 27.4 : 4.1e-5 · 30.6 : 1.9e-5 · 31.0 : 1.4e-5 | 일치 [인쇄] |
| 21 % | 8.9 : 2.0e-5 · 9.4 : 2.4e-5 · 10.0 : 2.3e-5 · 10.3 : 1.8e-5 · 14.6 : 1.5e-5 · 16.6 : 1.5e-5 · 19.7 : 1.2e-5 · 20.6 : 9.2e-6 · 28.4 : 4.7e-6 · 30.0 : 5.0e-6 · 34.5 : 3.6e-6 · 36.3 : 1.7e-6 | **저공극 영역에서 실측 < 모형** — AM 이 가압 충돌로 변형돼 거시 β > 1.5 [인쇄 · 저자 해석] |
| 10 % | 11.8 : 9.7e-7 · 12.4 : 1.2e-6 | **실측 ≪ 모형** — 퍼콜레이션 붕괴 (refs 23–25) · 높은 공극에서는 Nyquist 반원이 안 보여 σ 를 못 얻음 [인쇄] |

- [우리 산술] 모형 식으로 SE 35 % · 공극 15 % → τ_all = 5.09 · σ = 2.0×10⁻³ × 0.2975 / 5.09 = **1.17×10⁻⁴ S cm⁻¹** (그림 점선과 맞음 [판독]).
- 결론 (p.4): 공극이 크고 SE 가 적을수록 σ 가 낮다 · *"this model can be used to predict the ionic conductivity for different active material ratios and porosities and is useful for designing all-solid-state batteries and determining the target porosity values"*.

### 3-5. 경로 저항 분리 (Fig 7 · p.4–5)

| 공극 9 % | τ_L/S_AM (거시) | τ_L/S_Void (미시) | [우리 산술] 곱 = τ_all |
|---|---|---|---|
| SE 54 % | **1.3** | **1.7** | 2.17 |
| SE 21 % | **1.9** | **3.2** | 6.00 |

- [우리 산술] 식 7–9 + β 1.5 · 4 로 다시 내면 1.311 · 1.656 / 1.886 · 3.183 — 그림 표지와 맞는다 (공극 9 % · 고체 기준 SE 를 전체 기준으로 바꿔 넣음).
- 저자: 같은 성형 · 구속 압력인데 SE 가 적으면 SE 대비 공극 비가 커져 β = 4 인 미시 쪽 벌점이 크게 는다 → *"when increasing the active material ratio to increase the energy density, the porosity of the electrode should be reduced to ensure the output power"* [인쇄 p.4–5].
- 음극 (흑연) 이야기: 흑연은 SE 보다 탄성률이 낮아 눌리면 납작해져 거시 β 가 커질 것 [인쇄 p.5 — 시험 안 함].

---

## 4. ★ 방법 — 측정 사슬 · 입자 처리

### 4-1. 측정 사슬
SE (또는 SE + NCM 막자 혼합) → SUS 판 사이 펠릿 → 성형 압력 계단 (0.4 → 6.0 t f cm⁻²) 마다 구속 두께 · EIS → 공극률 (두께 · 밀도) – σ 쌍 / 별도 시료 단면 SEM → 이진화 → 2D 무작위 행보 → 경로 저항 계수 → σ 계산 → 실측 대조 / Bruggeman β 맞춤 → 곱 모형 → 복합 예측 · 대조.

### 4-2. ★ 입자 처리 (우리 축 언어로)
- **실험**: 실제 분말 압축 — SE 의 소성 · 치밀화가 압력 열에 들어 있다 (공극 41 → 3 %).  AM 은 21 % 조성에서 가압 충돌로 변형된다고 저자가 해석 (β > 1.5).
- **모형**: 입자 · 접촉이 없다 — 두 상의 부피분율 (ε_SE · ε_void) 과 장애물 모양 (β) 만.  ② 접촉 면적 (목) 효과는 β = 4 안에 **뭉뚱그려** 들어간다 (따로 매개변수 없음).
- **우리 대응**: DEM 접촉망 = 목 (Holm 협착 · 접촉 반경) 을 **접촉마다 명시** · STEP3 복셀 = 목을 격자로 (계면 항 0).  ⇒ 그들의 β 4 (미시) ↔ 우리 망의 협착비, 그들의 β 1.5 (거시) ↔ 우리 CF 가지가 대응한다 [추정 — §7-2].

### 4-3. 기법 미니 용어집
- **경로 저항 계수 (path resistance coefficient, τ_L/S)** = ε σ₀/σ_eff — 경로 연장과 단면 감소 (목) 를 함께 담은 겉보기 tortuosity = 우리 **tau2** (기하 τ 아님).
- **경로 저항 분리 모형** = τ_all = τ_macro (AM 우회) × τ_micro (공극 우회).
- **Bruggeman 지수 β**: σ_eff/σ₀ = ε^β ⇔ τ = ε^(1−β) — 장애물 모양의 지표.
- **무작위 행보 (random walk) tortuosity**: 장애물 그림 ÷ 빈 공간의 평균 걸음 수 비 — 확산 계수 비 = tortuosity factor 계열 (ref 19 · 21 = `tjaden2018_…` 카드).
- **전자–전자 연결형 EIS**: 이온 차단 (SUS) 전극 사이 복합층의 TLM 임피던스로 이온 저항을 읽는 법 (Siroma — `siroma2015_…` 카드).

---

## 5. Figure set ★ (크롭 7 장 = `litdb/figures/otani2023_ionic_conductivity_path_resistance_separation_model/`)

| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1 | 저하 인자 셋 — ① 공극 우회 tortuosity ② 접촉 면적 (병목) ③ 접촉 저항 (격자 부정합) · ①② = 계산 (경로 저항) · ①②③ = 실험 (이온전도도) | ★ 우리 tau2 분해 (경로 × 협착) 의 실험 쪽 언어 |
| 2 | SE (Mitsui LPSCl) SEM — 1 µm 안팎 덩이 입자 | 입자 형상 (구 아님) |
| 3 | 경로 저항 분리 모식 — (a) 전체 (b) 거시 (AM 우회) (c) 미시 (공극 우회) | ★ 곱 모형 그림 — 우리 CF × 협착비와 같은 구조 |
| 4 | 순수 SE 층 σ vs 공극 (실측 · 그림 계수 계산 · β 4 곡선) | ★ LPSCl 순수 층의 공극–σ 곡선 (σ₀ 기준 상태 논의) |
| 5 | 공극 30 % 이진화 단면 + 이온 경로 그림 | 경로 ≈1.2 · 목 ≈2.5 의 근거 그림 |
| 6 | 복합 σ vs 공극 (SE 54 · 35 · 21 · 10 %) 실측 + 모형 점선 (로그) | ★★ SE 35 % = 우리 ps45 조성 — 같은 띠 실측 |
| 7 | 공극 9 % 에서 τ_AM · τ_Void (SE 54 · 21 %) 막대 | AM 이 많을수록 공극 벌점 ↑ |

## 6. Post-processing ★
- **무엇을**: 공극–σ 쌍 · 2D 무작위 행보 경로 저항 계수 · Bruggeman β 맞춤 · 곱 모형 예측 · 실측 대조 · 거시/미시 분리 막대.
- **도구**: 자체 무작위 행보 프로그램 (그림 크기 · 화소 [미확인]) · ref 19 (RW3D) 계열.
- **안 한 것**: 3D 재구성 · 복합의 그림 계수 · 오차 · 반복 · 전자 전도 · 접촉 면적 직접 측정 · β 의 압력 의존 · 21 % 의 거시 β 재맞춤.
- **우리 후처리 (이 카드)**: Fig 4 · 6 판독 · 식 4–9 합성 (f = ε_SE⁴ (ε_SE+ε_void)^−2.5) · Fig 7 재현 · ps45 · Nakamura 2020 에 모형 적용 (§7).

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (⚠ 정본 브랜치에서는 값 자리표시 상태 — 우리 수치는 메인 리포 CLAUDE.md · `docs/` 출처를 병기해 적는다)

### 7-1. 비교표

| 항목 | 이 논문 | 우리 | 같음 / 다름 · 왜 |
|---|---|---|---|
| σ 를 내는 방법 | 실측 (EIS · TLM) + 해석 곱 모형 (Bruggeman 둘) | DEM 접촉망 Kirchhoff + Holm 협착 (Hertz 주) · STEP3 복셀 | 그들 = 평균장 · 우리 = 구조 해 |
| τ 정의 | τ_L/S_all = ε_SE σ₀/σ_eff | tau2 = φ_SE σ₀/σ_eff (메인 CLAUDE.md τ 명명 규약 2026-10-03) | **같은 양** |
| 분해 | 거시 (AM 우회, β 1.5) × 미시 (공극 · 목, β 4) | CF (협착 뺀 같은 망) × 모형 내부 협착비 | 구조가 같다 — 값의 나눔은 다르다 (§7-2) |
| 접촉 저항 (격자 부정합) | 무시 가능 (실측 = 그림 계수) | 망에 별도 항 없음 (Holm 은 기하 협착) · STEP3 ① r_int 기구는 기본 끔 | 같은 판단 — 단 그들 "목" 은 β 안에 숨어 있다 |
| 조성 | SE 54 · 35 · 21 · 10 vol% (고체) | ps45 SE/고체 ≈35 vol% (`PS45E-01` — AM 고체 64.7–64.9 %) | ★ SE 35 % 계열 = 우리 조성 |
| SE · CAM | Mitsui LPSCl D50 0.7 µm · NCM523 D50 5 µm 단봉 | LPSCl r 0.5 µm · NCM811 PC 9 / SC 4 µm | SE 크기 비슷 · CAM 다름 |
| σ₀ | "~2×10⁻³" (공급처 재료값) · Fig 4 절편 2.0 | 솔버 3.0 · 보고 기준 1.5 (CLAUDE.md 2026-10-12) | 기준 상태가 다르다 (§8-4) |

### 7-2. ★ 정량 대조 — 그들 모형을 우리 ps45 다섯 침대에 넣으면 [우리 산술]

입력 = 우리 φ_SE (`docs/data/ps45_r45_network_webapp_20261005/network_5comp.tsv`) · 공극 (ε_sphere 같은 표 · union 은 `docs/symmetric_cell_ionic_plan_20261013.md` §2) · 우리 값 = Hertz tau2 · CF tau2 · 협착비 (`docs/data/ps45_r45_network_g2_20261007/README.md` 분해 표).

| PC : SC | φ_SE | ε_sphere (%) | 그들 τ_macro | 그들 τ_micro | **그들 τ_all** | 우리 CF tau2 | 우리 협착비 | **우리 tau2 (Hertz)** | 비 (그들/우리) |
|---|---|---|---|---|---|---|---|---|---|
| 0:10 | 0.284 | 19.16 | 1.450 | 4.696 | **6.81** | 1.789 | 4.05 | **7.24** | 0.94 |
| 3:7 | 0.291 | 17.16 | 1.470 | 4.017 | **5.91** | 1.503 | 3.97 | **5.97** | 0.99 |
| 5:5 | 0.296 | 16.20 | 1.478 | 3.704 | **5.47** | 1.372 | 3.97 | **5.45** | 1.00 |
| 7:3 | 0.299 | 14.95 | 1.493 | 3.375 | **5.04** | 1.282 | 3.92 | **5.03** | 1.00 |
| 10:0 | 0.295 | 15.82 | 1.485 | 3.626 | **5.39** | 1.247 | 4.24 | **5.29** | 1.02 |

- union 공극 (20.6 · 18.7 · 17.7 · 16.5 · 16.9 %) 을 넣으면 그들 τ_all = 7.33 · 6.40 · 5.92 · 5.48 · 5.71 → 비 1.01–1.09.
- **뜻 [추정]**: ① 실제 LPSCl 펠릿에 맞춘 경험 모형 (β 4) 과 우리 Hertz 접촉망이 **같은 φ · 공극에서 총 tau2 를 ±6 % 안**에서 낸다 — 우리 Hertz 협착 (전력의 73–75 %) 이 "실물 목 저항" 의 크기와 어긋나지 않는다는 외부 정황.  ② 그러나 **조성 의존이 어디서 오나**는 다르다 — 그들은 공극 (τ_micro 4.7 → 3.4) 에서, 우리는 CF (SE–SE 연결 · CN 4.41 → 5.57, 1.79 → 1.25) 에서 온다 · 우리 협착비는 3.9–4.2 로 거의 일정.  ③ 그들 τ_macro (AM 우회 1.45–1.49) 는 조성에 둔하지만 우리 CF 는 0:10 → 10:0 에 1.79 → 1.25 — **작은 NCM 이 많을수록 SE 가 AM 표면 덮기에 쓰여 SE–SE 망이 끊긴다** 는 우리 기전 (대칭셀 계획 §2) 은 그들 모형에 **없는 항**이다 (구형 AM · Bruggeman 1.5 는 AM 크기를 모른다).
- ⚠ 한정: 그들 β 4 는 Mitsui LPSCl 순수 층 맞춤 · 우리 φ_SE 는 망의 질량 보존 기준 · 공극 관례 (ε_sphere vs union) 에 따라 비가 ±0.08 움직인다 · 우리 tau2 는 시드 1 개 침대.

### 7-3. ★ 이종기술 논지 — "분산을 모르는 귀무 모형" 으로 쓰기 [우리 산술 · 추정]
- 이 모형은 SE 의 분포 (응집 · 분산 · 코팅) 를 모른다 — 같은 ε_SE · 공극이면 같은 σ.  ⇒ 같은 SE 량 · 같은 공극에서 실측이 이 모형에서 벗어나는 만큼이 **분산 (또는 코팅) 효과의 크기 후보** (논지 P3 의 정량 기준선).
- 시험 삼아 같은 묶음 `nakamura2020_dry_coating_ncm_li3ps4_core_shell` 의 두 전극 (Table 1a 의 부피분율) 에 넣으면:

| Nakamura 2020 전극 | ε_SE | ε_void | 이 모형 τ_all | 측정 (복셀 FIB-SEM) τ |
|---|---|---|---|---|
| 막자 혼합 | 0.2165 | 0.1592 | **8.52** | **8.86** |
| 코팅 (NCM@LPS) | 0.2044 | 0.1654 | **9.74** | **5.49** |

  - 혼합은 귀무 모형과 ±4 % 로 맞고, 코팅은 귀무 모형보다 **0.56 배** — 코팅 효과는 (ε, 공극) 두 수로 설명되지 않는 "배치" 효과다 [추정 — 재료 다름 (Li₃PS₄ 유리 ↔ β 4 는 LPSCl 맞춤) · 복셀 τ 와 모형 τ 의 기준 차 · 표본 하나].
- 같은 관점에서 PTFE 카드 (`lee2026_unveiling_…`) 의 0.0 ↔ 0.2PTFE (재구성 LPSCl 23.5 ↔ 23.6 % 같음 · 시뮬 σ_ion +57 %) 도 이 모형 밖의 배치 효과 사례다.
- 논지 프레이밍과의 거리: 이 논문은 "접촉 면적 (목) 을 늘려라" 를 결론으로 낸다 — 논지는 계면 면적 (SE–AM) 이 아니라 SE–SE 이온 경로를 말하므로, 이 논문의 ② (SE–SE 목) 와는 **같은 편**이다.

### 7-4. 대칭셀 계획 (`docs/symmetric_cell_ionic_plan_20261013.md`) 에 주는 것
1. **예측 띠**: 그들 SE 35 % 실측 (공극 14.6–18.7 %) 0.075–0.13 mS cm⁻¹ [판독] — 우리 계획 조성 (81.6 : 18.4 wt% · SE/고체 ≈35 vol%) 의 실험 결과가 들어갈 자리를 미리 준다 (재료 · 입경 · 혼합 다름).
2. **공극을 같이 재야 한다** — 같은 조성에서 공극 7 → 31 % 사이 σ 가 한 자릿수 바뀐다 (Fig 6 SE 35 %: 1.7×10⁻⁴ → 1.4×10⁻⁵) · 우리 계획 §3 의 읽는 법은 공극을 공변량으로.
3. **순수 LPSCl 펠릿 σ₀ 의 공극 보정**: 순수 층이 σ₀(1−p)⁴ 를 따르면 펠릿 σ₀ 측정값은 그 펠릿 공극의 함수다 (공극 10 % 에서 재료값의 0.66 배 [우리 산술]) → 기준 시료의 두께 · 질량 · 압력을 반드시 기록 (`lee2024_shear_force_…` 카드 §8-6 과 같은 요구).
4. **측정 방식**: 전자–전자 연결형 EIS (TLM) — 우리 계획의 EIS + TLM 과 같은 계열.

### 7-5. frame[5] — 어느 반쪽을 가졌나
- **가진 것**: 순수 LPSCl 층 · 복합 (네 조성) 의 **공극–σ 실측 곡선** + 평균장 분해 모형.
- **없는 것**: 3D 구조 · 접촉 수 · 접촉 면적 · SE 분포 · 혼합 상태 · 전자 · 반복 통계.  ⇒ 우리 DEM 망 (구조 → σ) 과 맞대면 **같은 φ · 공극에서 분포 · 연결 효과만 남는다** — 이것이 이 논문을 귀무 모형으로 쓰는 이유.

---

## 8. ★★ 우리 연구에 주는 insight (번호마다: 논문이 보인 것 → 우리에게 뜻 → 할 일)

**8-1. 실측 맞춤 경험 모형과 우리 Hertz 망의 tau2 가 ±6 % 안 — 외부 대조점이 생겼다.**
- 논문: 순수 LPSCl 층 β 4 · 복합 = β 1.5 × β 4 · SE 35 % 에서 실측과 일치.
- 뜻 (§7-2): ps45 다섯 침대에서 그들 τ_all / 우리 Hertz tau2 = 0.94–1.02 (ε_sphere) — 수송 tortuosity 5.0–7.2 를 보일 때 *"LPSCl 실측 맞춤 모형 (Otani 2023) 과 같은 크기"* 라는 괄호를 붙일 수 있다 [추정 — 재료 · 공극 관례 한정어 필수].
- 할 일: 덱 · 보고 표에 비교 열로 (결과 전 등록 대상 아님 — 이미 있는 값의 대조) · 원장 기록은 1저자.

**8-2. 그러나 분해가 다르다 — 조성 의존의 출처가 우리 쪽이 더 많은 정보를 갖는다.**
- 논문: 조성 · 공극 의존이 τ_micro (공극) 와 τ_macro (AM 부피) 에만 있다 · AM 크기 · 분포 항 없음.
- 뜻: 우리 ps45 의 PC:SC 경향 (σ_ion 1 → 1.52 배) 은 **같은 공극 · φ 에서도** CF (SE–SE 연결) 로 생긴다 — 이 모형이 못 내는 몫이 곧 DEM 의 몫이다.
- 할 일: ps45 다섯 침대를 "같은 공극 · φ 로 맞췄을 때 남는 차" 로 보여 주는 그림 (그들 모형 = 기준선) 후보.

**8-3. 분산 효과의 귀무 모형 — Nakamura 2020 의 코팅은 0.56 배로 벗어나고 혼합은 맞는다.**
- 뜻 (§7-3): 논지 P3 의 실험 쪽 크기를 말할 때 "귀무 모형 대비 몇 배" 가 공극 · SE 량 차를 자동으로 빼 준다.
- 할 일: 우리 대칭셀 · 코팅 실험 결과를 이 모형 예측과 나란히 (같은 공극 · SE) — 예측식은 §3-2 끝의 f = ε_SE⁴(ε_SE+ε_void)^−2.5.

**8-4. 순수 SE 의 β 4 는 σ₀ 기준 상태 문제 (CL-91) 의 크기를 준다.**
- 논문: 순수 층 σ = 2.0×10⁻³ (1−p)⁴ (재료값 절편).
- 뜻: 펠릿 σ₀ 를 쓰는 우리 망은 펠릿 안의 목 저항을 σ₀ 에 이미 넣고 접촉마다 Holm 을 또 넣는다 (CL-91 의 부분 이중계상) — 이 모형으로 보면 공극 5–12 % 펠릿의 미시 몫은 (1−p)^−3 = **1.17–1.47** [우리 산술].  우리 σ₀ 1.5 가 공극 ≈7 % 펠릿이면 재료값 2.0 과 맞는다 (2.0 × 0.93⁴ ≈ 1.50) [추정 — Cronau 펠릿 공극 미상].
- 할 일: CL-91 재해석 논의 (1저자 결정) 에 이 숫자를 참고로 — 원장은 이 카드가 고치지 않는다.

**8-5. "목 (접촉 면적) 이 주범, 격자 부정합은 무시" — 우리 망 규약과 같은 판정.**
- 논문: 공극 30 % 에서 경로 1.2 × 목 2.5 · ③ 무시.
- 뜻: 우리 ps45 분해 (√CF 1.12–1.34 = 경로 몫 · 협착비 3.9–4.2 = 목 몫) 와 같은 구조 · 우리 목 몫이 더 큰 것은 공극이 작은 대신 SE 가 AM 표면에 쓰이는 복합 침대이기 때문일 수 있다 [추정].  STEP3 ① r_int (계면 저항 기구) 를 켤 근거는 이 논문에서는 약하다 (③ ≈ 0).
- 할 일: r_int 값 논의 (D12) 때 "황화물 순수 층에서 ③ ≈ 0 (Otani 2023)" 을 한 줄 근거로.

**8-6. 기호 혼동의 실례 — τ = l/L 을 σ = σ₀ε/τ 에 넣는다.**
- 논문: 식 1 (기하) 과 식 2 (tortuosity factor 자리) 를 같은 τ 로.
- 뜻: 우리 τ 명명 규약 (기하 τ_geo ↔ 수송 tortuosity tau2) 이 막는 혼동이 원문에 있다 — 그들 "tortuosity ≈1.2" (경로) 와 "경로 저항 계수 ≈3" 을 섞어 옮기지 않는다.
- 할 일: 인용할 때 그들 τ_L/S 는 "수송 tortuosity (경로 저항 계수)" 로, 1.2 는 "기하 경로 비" 로 표기.

## 9. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "For argyrodite Li₆PS₅Cl layers, Otani et al. (*J. Energy Storage* 2023) found that image-based path-resistance coefficients reproduce the measured conductivity–porosity curve (Bruggeman β = 4), implying negligible interfacial lattice-mismatch resistance; at 30 % porosity the coefficient of ≈3 splits into ≈1.2 from path length and ≈2.5 from the inter-particle contact area."
- "Their path-resistance-separation model (AM detour β = 1.5 × void detour β = 4) gives transport tortuosities within −6 to +2 % of our Hertz contact-network values for the same SE fraction and porosity (our calculation)."
- 국문: *"실측 맞춤 경험 모형 (Otani 2023) 을 같은 SE 부피 · 공극에 넣으면 우리 접촉망의 수송 tortuosity 와 ±6 % 안에서 같다 — 다만 조성 의존은 그 모형에 없는 SE–SE 연결 항에서 나온다."*

## 10. 주의/한계 (over-claim 방지 · 원문 비판)
1. **선형식 귀속 문제**: `lee2024_multiphysics_dem_fem_initial_pressure_assb` 카드가 *"τ_L/S_all = −11.7·ε_SE + 8.54 (eq38, 선형 경험식, Otani 2023 ref46)"* 라 적는데, 이 논문에는 선형식이 **없다** (식 1–9 · 그림 7 장 전수).  Lee 2024 원문의 ref 46 이 이 논문인지 · 식 38 이 Lee 2024 자체 맞춤인지 [미확인] — 그 카드의 귀속 문장은 Lee 2024 원문 대조 전까지 "Otani 2023 에서 유도 (추정)" 로 읽어야 한다 (이 카드는 그 카드를 고치지 않는다).
2. **데이터 기밀** — 원자료 · 그림 크기 · 화소 · 반복 · 오차 없음 · 그림 판독이 유일한 수치원.
3. **2D 무작위 행보**: 2D 단면은 3D 연결을 과소 · 과대평가할 수 있다 (2D 퍼콜레이션 문턱이 다르다) · 무구속 시료라 공극률이 측정 상태와 다름 (이진화 공극으로 대신).
4. **문장 모호**: *"Approximately a 20 % decrease in porosity results in a 50 % increase in ionic conductivity"* — 기준 공극 · 상대/절대 미기재 (β 4 식으로는 공극 40 → 32 % 에서 +65 %, 30 → 24 % 에서 +39 % [우리 산술]).
5. **β 4 의 전이**: 순수 층 맞춤값을 복합의 미시 경로에 그대로 — SE 가 AM 사이에서 다르게 눌리는 효과 (AM 이 하중을 지는 차폐) 는 반영 안 됨 · 21 % 저공극 어긋남을 "AM 변형 → 거시 β > 1.5" 로 설명하나 재맞춤 없음.
6. **용어 · 단위**: 식 1 τ = l/L 을 식 2 의 τ 자리에 씀 (§8-6) · 용어집 단위 "S•m" (S m⁻¹ 이어야) · 본문 "Shiroma" ↔ 참고문헌 "Siroma" · 서론 한 문단 (*"Nevertheless, such simulation software may be difficult …"*) 이 두 번 반복 (p.1 · p.2).
7. **σ₀ "~2×10⁻³"** 는 공급처 값 — 순수 층 실측 최고 ≈1.7×10⁻³ (공극 3 %) [판독] · 측정 셀 · 압력 · 온도 [미확인].
8. **전이 한계**: NCM523 단봉 · 막자 혼합 · 도전재 없음 · 공극을 압력으로 바꿈 (공극과 압력이 함께 움직인다) — 우리 바이모달 · 300 MPa 한 점과 다르다.

## 11. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)
| 번호 | 서지 (원문 목록 그대로) | 왜 · 카드 |
|---|---|---|
| 4 | D. Hlushkou, A.E. Reising, N. Kaiser, et al., J. Power Sources 396 (2018) 363–370 | 정본 카드 `hlushkou2018_void_space_ion_transport_assb_cathode` |
| 5 | T. Asano, S. Yubuchi, A. Sakuda, A. Hayashi, M. Tatsumisago, J. Electrochem. Soc. 164 (14) (2017) A3960–A3963 | 정본 카드 `asano2017_ncm111_li3ps4_composite_electronic_ionic_conductivity` |
| 6 | P. Minnmann, L. Quillman, S. Burkhardt, F.H. Richter, J. Janek, J. Electrochem. Soc. 168 (4) (2021) 040537 | 정본 카드 `minnmann2021_jes_charge_transport_bottlenecks` |
| 7 | M. So, G. Inoue, R. Hirate, et al., J. Power Sources 508 (2021) 230344 | 정본 카드 `so2021_dem_mold_pressure_assb_coldpress` |
| 8 | M. So, G. Inoue, R. Hirate, et al., J. Electrochem. Soc. 168 (2021) 030538 | 카드 없음 — 연성 입자 제조 · 열화 DEM |
| 10 | M. So, G. Inoue, K. Park, et al., J. Power Sources 530 (2022) 231279 | 정본 카드 `so2022_dem_compaction_coated_particles_assb` |
| 14 | G. Inoue, M. Kawase, J. Power Sources 342 (2017) 476–488 | 카드 없음 — 다공 전극 구조 ↔ 유효 전도도 (같은 교신) |
| 17 · 18 | Z. Siroma et al., J. Power Sources 316 (2016) 215–223 · Electrochim. Acta 160 (2015) 313–322 | 18 = 정본 카드 `siroma2015_transmission_line_model_porous_electrode_impedance` · 17 카드 없음 |
| 21 | B. Tjaden, D.J.L. Brett, P.R. Shearing, Int. Mater. Rev. 63 (2018) 47–67 | 정본 카드 `tjaden2018_tortuosity_review_calculation_approaches` |
| 22 | M. Kodama, S. Komiyama, A. Ohashi, et al., J. Power Sources 462 (2020) 228160 | 카드 없음 — 고압 in situ XCT · 황화물 입계 저항 무시 근거 |
| 23 · 24 | A. Bielefeld, D.A. Weber, J. Janek, J. Phys. Chem. C 123 (2019) · ACS Appl. Mater. Interfaces 12 (2020) | 정본 카드 `bielefeld2019_microstructural_modeling_composite_cathode` · `bielefeld2020_effective_ionic_conductivity_binder` |
| 25 | T. Shi, Q. Tu, Y. Tian, et al., Adv. Energy Mater. (2019) 1902881 | 정본 카드 `shi2019_high_am_loading_particle_size_assb` |

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-10-13)
- 본문 6 쪽 텍스트 층 전수 (PyMuPDF) · 저자 · 소속 · 날짜 = p.1 · DOI = p.1 인쇄 · 식 1–9 = 텍스트 층 (분수 배치는 렌더로 확인).
- 그림 7 장 = 캡션 7 개 (표 · SI 없음) — 전부 렌더로 열람 · 래스터 경계 · 원본 300 dpi 로 재크롭.
- 선형식 τ = −11.7·ε + 8.54: 본문 텍스트 층 전수 + 그림 7 장에서 **없음** 확인 (§10-1).
- Fig 7 표지 (1.3 · 1.7 · 1.9 · 3.2) = 식 7–9 + β 1.5 · 4 로 소수 둘째 자리까지 재현 [우리 산술].
- Fig 4 · 6 판독 = 원 래스터 화소 (눈금 · 격자선 보정, 색 마스크 + 거리변환 정점) · Fig 4 점선 절편 1.98×10⁻³ (인쇄 2.0 과 맞음) · Fig 6 SE 35 % · 15 % 공극의 모형 계산 1.17×10⁻⁴ 이 점선과 맞음.
- 정본 litdb 중복 확인: DOI · 제목 낱말 · "path resistance" 로 `litdb/` 전수 grep — 이 논문 카드 없음 (miss2026 카드 ref 26 · lee2024_multiphysics 카드 "ref46" 으로만 언급).

## 🔗 관련 카드
- 같은 계보 (Inoue): `so2021_dem_mold_pressure_assb_coldpress` · `so2022_dem_contact_model_assb_compaction_sintering` · `so2022_dem_compaction_coated_particles_assb` · `otani2025_dem_se_dispersion_aggregation_compression`.
- 복합 σ 실측 · 모형: `asano2017_ncm111_li3ps4_composite_electronic_ionic_conductivity` · `minnmann2021_jes_charge_transport_bottlenecks` · `hlushkou2018_void_space_ion_transport_assb_cathode` · `bielefeld2019_microstructural_modeling_composite_cathode` · `bazzoun2026_dem_fem_rnm_ionic` · `miss2026_insitu_conductivity_porosity_pressure_compaction`.
- τ 규약: `tjaden2018_tortuosity_review_calculation_approaches` · `siroma2015_transmission_line_model_porous_electrode_impedance` · `kato2018_thick_electrode_assb_cycle_tortuosity`.
- 같은 날 묶음: `nakamura2020_dry_coating_ncm_li3ps4_core_shell` (귀무 모형 대조 §7-3) · `lee2024_shear_force_dry_process_cathode_coverage`.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
