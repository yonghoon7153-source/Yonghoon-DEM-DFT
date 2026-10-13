<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 사용자가 특히 원한 항목. 깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md · 형식 이웃 = hare2026_dem_pept_dry_mixing_nmc622_eirich.md · lischka2025_dem_eirich_intensive_mixer_dry_mixing.md.
     쪽 표기 = "p.N" (PDF N 쪽 = 인쇄 788+N · Powder Technol. 339, 789–800).
     값 표지: [인쇄] = 본문 · 표 · 그림 안에 숫자로 인쇄된 값 · [판독] = 그림에서 읽은 값 (litdb/figures/<slug>/digitized.csv) · [우리 산술] = 인쇄값으로 다시 한 계산 · [미확인] = 원문 (본문 전수) 에 없음 · [추정] = 우리 해석.
     원문 = 본문 12 쪽 (SI 없음) — 텍스트 층 전수 + 식 (1)–(4) 렌더 대조 · 그림 20 · 표 3 = 크롭 23 장 전부 열람. -->

# **코팅으로 끈적해진 소량 성분의 점착을 안식각으로 보정** 하는 DEM 절차 — PEG 400 코팅 효소 위약 과립 (2 wt%) + 세제 분말 3 성분 더미 형성 · JKR 계면 에너지 Γ 를 **응집수 (Cohesion number) 불변** 으로 강성 · 크기 환산 · 코팅–비코팅 접촉 = Γ 의 **절반** · 코팅이 분리 지수를 낮추지만 (실험 CoV 1.33 → 0.83) 지나친 점착은 미분이 들러붙은 덩어리로 **다시 분리** (S_n 2.58) — Alizadeh · Asachi · Ghadiri · Bayly · Hassanpour (Powder Technology 2018)

> slug `alizadeh2018_dem_adhesion_calibration_segregation_heap` · DOI `10.1016/j.powtec.2018.08.028` · type `DEM (EDEM 2.7.1, Hertz–Mindlin + JKR adhesion, sphere clumps from XRT) + exp (heap-formation segregation of a ternary detergent powder mixture, angle of repose, Jenike ring shear)` · PDF `6d4100ce-43._A_methodology_for_calibration_of_DEM_input_parameters_in_simulation_of_segregation_of_powder_mixtures_a_special_focus_on_adhesion.pdf` · digested `2026-10-13` · status ✅
>
> **원제**: *A methodology for calibration of DEM input parameters in simulation of segregation of powder mixtures, a special focus on adhesion* (p.1)
> **저자**: Mohammadreza Alizadeh · Maryam Asachi · Mojtaba Ghadiri · Andrew Bayly · Ali Hassanpour (교신, A.Hassanpour@leeds.ac.uk) — School of Chemical and Process Engineering, University of Leeds, UK (p.1)
> *Powder Technol.* **339** (2018) 789–800 · 접수 2018-03-19 · 수정 2018-08-02 · 승인 2018-08-08 · 온라인 2018-08-09 (p.1) · 연구비 UK AMSCI "Chariot" (grant 31587, 233189) (p.11).
> **판독 원자료**: `litdb/figures/alizadeh2018_dem_adhesion_calibration_segregation_heap/digitized.csv` · 크롭 23 장 `figures.json`.
> **이 카드가 서랍에 들어온 이유**: 이종기술 논지 (`docs/hetero_thesis.md`) 의 **D3** (SE 분말 점착 앵커 + DEM 보정 런) · **D2** (혼합쌍 · 벽 결합 규칙) 의 **보정 레시피** 원형 — 1저자 읽기 목록 `docs/mixer_coating_reading_list_20261013.md` B5-2.  같은 Leeds 그룹 (Ghadiri · Hassanpour) 의 같은 날 카드 후보 #44 (Geldart 2006 안식각 측정기) 와 짝.

> ★★ **한 줄로 왜 중요한가**: "**코팅으로 한 성분의 표면만 바꾸면 혼합 · 분리가 바뀐다**" 를 실험 + DEM 으로 함께 보인 몇 안 되는 사례이고, 그 DEM 에 넣은 점착값을 **어떻게 정했는지** (단일 성분 안식각 → JKR Γ · 응집수로 강성 연화와 크기 차를 환산 · 코팅–비코팅 = 절반) 가 단계별로 적혀 있다.  우리 D3 (SE 점착 앵커) · D2 (AM–SE 혼합쌍 규칙) 를 정할 때 **바로 비교할 절차** 다.
> ⚠ 단 **인쇄 식 · 숫자 사이 불일치가 넷** 이다 (§3-6): 식 (4) 의 크기비 방향이 응집수 불변과 반대 · 인쇄 응집수 1.6 × 10⁻³ 은 R\* = R/2 가 아니라 R 일 때 재현 · 교차쌍 Γ (0.037 · 0.060) 은 서술 ("2.5 wt% 의 0.25 의 절반") 이 아니라 Γ₁ ≈ 0.05 에서 재현 · 분리 지수 감소율 서술 (40 % · 70 %) 이 그림 (35–45 %) 과 다름.  **절차는 옮기고 숫자는 다시 계산한다.**

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: 세제 분말 (BP 425–500 µm · 92 wt%) + TAED (850–1000 µm · 6 wt%) + 효소 위약 과립 EP (600–700 µm · 2 wt%) 를 깔때기로 떨어뜨려 16 mm 두께 상자에 더미를 쌓으면 무겁고 둥근 EP 가 더미 **가운데로 분리** 되는데, EP 를 PEG 400 으로 코팅해 끈적하게 하면 (DEM: EP–EP Γ 0.25 J m⁻² · EP–BP 0.037 · EP–TAED 0.060) **앞면 CoV 가 실험 1.33 → 0.83 · DEM 1.44 → 0.94** 로, 전체 더미 S_n 이 **1.57 → 0.86** 으로 내려간다 [판독 Fig 10 · 13].  기전 (DEM 입자 추적): 비코팅 EP 는 더미 표면에 떨어지면 **아래층으로 파고들어** 흐르는 위층을 벗어나고 (push-away), 코팅 EP 는 **위층에 붙잡혀** 다른 입자와 함께 모서리까지 흘러간다.  모든 EP 접촉을 0.25 로 올리면 BP 미분이 EP 에 들러붙은 **덩어리** 가 사태로 모서리에 쌓여 **S_n 2.58** 로 오히려 나빠진다.

| 우리 질문 | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① **D3** — 분말 점착을 DEM 값으로 앵커하는 절차? | **단일 성분 (EP 만) 더미 안식각 vs 코팅량** 을 실험으로 재고 (0 · 0.5 · 1.5 · 2.5 · 3.5 wt% PEG → 31 · 37 · 48 · 48.5 · 55.5° [판독]), DEM 에서 **Γ 를 바꿔 같은 각도** 를 찾는다 (Γ 0 · 0.05 · 0.15 · 0.25 · 0.35 J m⁻² → 31 · 38 · 45 · 48 · 57° [인쇄 Fig 7]).  출발값 = 코팅재 표면장력 × 2 (Γ ≈ 2γ_PEG = 0.086 J m⁻²) → 응집수로 연화 강성에 환산 | [인쇄] p.4–5 · Fig 4 · 6 · 7 |
| ② **D2** — 코팅–비코팅 (혼합쌍) 규칙? | **Γ_코팅–비코팅 = 0.5 × Γ_코팅–코팅** (JKR 근거라 적음 · Fig 4 흐름도에 인쇄) + 크기가 다르면 응집수 불변으로 Γ ∝ R\*^{8/5}.  = 비점착 Γ = 0 일 때 **산술평균** 규칙.  같은 날 카드 `jarray2019_…` 의 실측 F_AB/F_AA ≈ 0.5 와 같은 방향 · 우리 덱 **min** 규칙 · 논지 §2 **기하평균** 은 둘 다 0 을 준다 | [인쇄] p.5 · Fig 4 · [우리 산술] |
| ③ 강성 연화 · 크기 환산의 **불변량**? | **응집수 Coh = (1/ρg)·(Γ⁵/(E\*²R\*⁸))^{1/3}** (= JKR 분리 일 ÷ 중력 위치 에너지 꼴, Behjani 2017) 을 고정 → **Γ ∝ E\*^{2/5}** (강성 연화) · **Γ ∝ R\*^{8/5}** (크기).  우리 Bo_code (힘 ÷ 무게) 와 **다른 불변량** — 에너지 기준 | [인쇄] 식 (1)–(3) · p.3 |
| ④ **코팅 → 분산** 의 실물 대조? | 소량 성분 코팅 → 분리 감소 (실험 CoV −38 % · DEM −35 % · 전체 S_n −45 % [판독]) · **지나친 점착 → 미분 부착 덩어리 → 재분리** (S_n 2.58) = **최적 코팅량** 존재 (선행 실험 Asachi 2017: 2.5 wt% 최저) | [판독] Fig 10 · 13 · [인쇄] p.11 |
| ⑤ 혼합지수 (우리 Lacey 문제)? | **S_n = CoV_m / CoV_r** — 무작위 CoV_r 를 **칸마다 들어갈 EP 개수 (칸 부피 × 0.6 ÷ EP 부피) 로 이항 분포 몬테카를로 100 회** 로 만든다.  칸 크기 = "세제 한 숟갈" (**관찰 척도를 용도에서 고른다**).  CoV_r 은 칸 체계마다 다르다 (전체 0.21 · 앞면 0.50) | [인쇄] 식 (5)–(7) · p.6 · p.8 |
| ⑥ 벽 · 단면 측정의 함정? | 16 mm 상자에서 **벽 층 CoV 가 가운데의 2–3 배** (비코팅 0.94 · 0.77 vs 0.30 [판독]) — **앞면 영상은 침대 전체를 대표하지 못한다** (저자) | [판독] Fig 12 · [인쇄] p.8 |
| ⑦ 벌크 유동성으로 소량 성분 점착을 잴 수 있나? | **못 잰다** — 2 wt% EP 를 코팅해도 혼합물 안식각 36.4 → 38.0° (실험) · ffc 6.3 → 4.4 (여전히 '쉽게 흐름') · 깔때기 배출 2.22 → 2.32 s (+5 %) 뿐인데 분리는 크게 바뀐다 ⇒ 점착 보정은 **단일 성분 시험** 으로 해야 한다 | [인쇄] p.9 · Fig 14 · 15 |

⛔ **한정어 (떼지 말 것)**: ① 입자 = **수백 µm 세제 과립** · Bo 낮은 영역 (비코팅은 JKR 끔) — µm SE 분말이 아니다 ② 공정 = **더미 형성 (깔때기 붓기)** — 회전 드럼 혼합이 아니다 ③ 점착 = **PEG 400 액상 고분자 막 (모세관 다리 없음이라 적음)** — 반데르발스 · 정전기 지배인 건식 미분과 기전이 다르다 ④ **런 수 미기재** (DEM 은 조건마다 1 런으로 보인다 [추정]) ⑤ 숫자 불일치 넷 (§3-6).

---

## 1. 한 줄 요약

**DEM 입력값을 측정 · 보정으로 정하는 절차를 세 단계로 짠 논문**: ① 모양 = XRT 로 찍은 실제 입자를 sphere-clump 로 근사하고 **입자 수를 안식각이 맞는 최소** 로 (BP · TAED 5 구 · EP 1–3 구) ② 마찰 · 구름마찰 · 반발 = 선행 보정값 [30] ③ 점착 (코팅 EP 만) = PEG 표면장력에서 출발 → **응집수 불변으로 연화 영률에 맞게 환산** → **단일 성분 더미 안식각을 맞추도록 Γ 조정** → 혼합쌍은 **절반 + 크기 환산**.  그 입력으로 3 성분 더미 형성의 EP 분리를 DEM 과 실험 (앞면 영상) 에서 비교: 코팅이 앞면 CoV 를 35–38 % 낮추고 (DEM ↔ 실험 차 ≈ 10 %), DEM 3D 분석에서 **벽 층이 가운데보다 훨씬 분리돼 보이는** 2D 측정의 편향을 드러낸다.  기전 = 충돌 직후 운동 에너지 · 표면 침투 (push-away) 차이.

## 2. 메타

| 저자 | 저널/년 | DOI | 소재 | 연구유형 |
|---|---|---|---|---|
| M. Alizadeh · M. Asachi · M. Ghadiri · A. Bayly · A. Hassanpour (교신, Leeds) | *Powder Technol.* 339 (2018) 789–800 | 10.1016/j.powtec.2018.08.028 | 세제 분말 BP (분무건조 · 780 kg m⁻³) · TAED (850 kg m⁻³) · 효소 위약 과립 EP (2320 kg m⁻³) · 코팅 = **PEG 400** (0.5–3.5 wt%) · 상자 = Perspex | **DEM** (EDEM 2.7.1 · Hertz–Mindlin + JKR) + **실험** (더미 앞면 영상 · 안식각 · Schulze 링 전단 Jenike ffc) |

> ★ **계보 · 짝**: 실험 = Asachi 2017 (*EPJ Web Conf.* 140, 13013 — ref 7) · 모양 보정 = Alizadeh 2017 (*Powder Technol.* 319, 313 — ref 30) · 응집수 = Behjani 2017 (*Adv. Powder Technol.* 28, 2456 — ref 3).  강성 연화 JKR 해석 = Hærvig 2017 (*Powder Technol.* 319, 472 — ref 2, "같은 함수 꼴").  같은 Leeds 저자의 Geldart 2006 (안식각 측정기 — 같은 날 카드 후보 #44) 과 Hassanpour 가 겹친다.

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. 시험 장치 (Fig 1 · p.2) + 우리 산술
| 항목 | 값 | 표지 |
|---|---|---|
| 상자 | **200 (폭) × 191 (높이) × 16 mm (두께)** · 앞뒤 Perspex · 틀 금속 | [판독] Fig 1 |
| 깔때기 | 위 지름 **120 mm** · 벽 **45°** · 출구 **15 mm** · 관 아래 **10 mm** · 깔때기 전체 높이 **100 mm** | [판독] Fig 1 |
| ⚠ 관 길이 라벨 | **"450 mm"** — 전체 100 mm 안에 들어갈 수 없다 (원뿔 높이 (120−15)/2 = 52.5 mm + 관 ≈ 45 mm ≈ 100 mm) ⇒ **45 mm 의 오기** 로 읽힌다 | [우리 산술] |
| 혼합 | 손으로 섞어 깔때기에 붓기 (Asachi 2017 절차) · DEM = 세 성분을 **동시에 일정 속도로 무작위 생성** (dynamic factory, 질량비 Table 1) → 깔때기로 낙하 | [인쇄] p.2 · p.6–7 |
| DEM 깊이 분해 | 두께 16 mm 를 **8 층 (2 mm)** | [인쇄] p.7 |
| 2D 칸 | 앞면 영상을 **21 칸** (7 × 3) — 칸 크기 = "세제 한 숟갈" 관찰 척도 | [인쇄] p.5–6 · [판독] Fig 8 |

### 3-2. 재료 · DEM 입력 (Table 1 · Table 2 · p.3 · p.5)

| 항목 | BP | TAED | EP (효소 위약) | Perspex 벽 |
|---|---|---|---|---|
| 체 크기 (µm) | 425–500 | 850–1000 | 600–700 | — |
| 입자 수 | **633,597** | 4,667 | 1,401 | — |
| 총 질량 (g) | 28.53 | 1.71 | 0.61 | — |
| 질량 % (표) | 92.0 | 6.0 | 2.0 | — |
| 모양 | 5-구 clump | 5-구 clump | 1 · 2 · 3-구 (구 · 장구 근사) | 벽 |
| 안식각 (비코팅, °) | 40.0 | 36.0 | 31.0 | — |
| 전단탄성률 (MPa) | 100 | 100 | 100 | 1000 |
| 밀도 (kg m⁻³) | 780 | 850 | 2320 | 1180 |
| 구름마찰 계수 | 0.10 | 0.01 | 0.05 | 0.01 |
| 포아송비 | 0.25 | 0.25 | 0.25 | 0.25 |
| 미끄럼마찰 (BP · TAED · EP 와) | 0.62 · 0.69 · 0.70 | 0.69 · 0.75 · 0.75 | 0.70 · 0.75 · 0.75 | 0.42 · 0.36 · 0.75 |
| 반발 (BP · TAED · EP 와) | 0.20 · 0.30 · 0.20 | 0.30 · 0.32 · 0.20 | 0.20 · 0.20 · **0.10** | 0.28 · 0.32 · 0.20 |

[인쇄] Table 1.  ⚠ 표의 "CoR (x-particle)" 행 (0.10–0.32) 은 **반발계수** 로 읽힌다 (§2.5.1 "점성 소산 때문에 낮은 반발계수") — 그런데 §2.3 본문은 "CoR" 을 **구름마찰** 약어로 정의한다 (약어 충돌).
- **EP (Table 2)**: 체 600–700 µm · ρ 2320 · **실제 영률 1.6 GPa** [ref 37] · ν 0.25 · DEM 표면 에너지 **0.0–0.350 J m⁻²** · PEG 400 표면 에너지 (실험) **0.043 J m⁻²** [ref 34 · 35].
- **DEM 영률**: G 100 MPa · ν 0.25 ⇒ E = 2G(1+ν) = **0.25 GPa** — 저자 "실제 (1.6 GPa) 의 약 1/10 (~0.25 GPa)" [인쇄 p.5 · 우리 산술 = 1/6.4].
- 질량 합 30.85 g ⇒ **92.5 : 5.5 : 2.0 wt%** (표 92.0 · 6.0 · 2.0) · Fig 9 캡션 "50 : 3 : 1" ⇒ 92.6 : 5.6 : 1.9 [우리 산술].
- 표의 질량 · 개수 · 밀도로 부피 등가 지름 = **BP 480 · TAED 937 · EP 710 µm** — BP · TAED 는 체 범위 안 · EP 는 상한 (700) 을 약간 넘는다 [우리 산술].
- 접촉: **Hertz–Mindlin** (탄성 · 마찰) + **JKR** (점착) · 입자가 크고 무르며 응력이 낮아 Tabor 기준상 JKR 타당 · **비코팅 계는 JKR 끔** (낮은 입상 Bond 수) (p.2).

### 3-3. ★ 점착 보정 (§2.5 · Fig 4 · 6 · 7 · p.3–5)

**흐름 (Fig 4 흐름도)**: 마른 EP 로 DEM 입력 보정 → 실험 안식각 검증 → (점착) 응집수로 Γ 초기값 → DEM 안식각 → 실험과 비교 → 맞을 때까지 Γ 수정 → 코팅량 ↔ Γ 관계 확립 → 원하는 Γ 선택 → **코팅–코팅 Γ_CC = Γ_선택 · 코팅–비코팅 Γ_CD = 0.5 Γ_CC** → clump 크기 차는 **응집수로 환산 ((Γ₂/Γ₁)⁵ = (R₁/R₂)⁸ — 인쇄 그대로, §3-6 ①)** → DEM 혼합 런 → 실험과 비교.

| 단계 | 값 | 표지 |
|---|---|---|
| 응집수 (식 1) | **Coh = (1/(ρg))·(Γ⁵/(E\*²R\*⁸))^{1/3}** · R\* = (1/R₁ + 1/R₂)⁻¹ · E\* = ((1−ν₁²)/E₁ + (1−ν₂²)/E₂)⁻¹ — "분리 일 ÷ 중력 위치 에너지" (Behjani 2017) | [인쇄] 식 (1)–(3) |
| 대안 스케일링 (저자 언급) | 입상 Bond 수 (힘 ÷ 무게 — **영률 없음**) · Thakur 2016: Γ ∝ R² | [인쇄] p.3 |
| 출발값 | Γ_EP ≅ **2γ_PEG = 0.086 J m⁻²** ⇒ 실험 계 응집수 **1.6 × 10⁻³** | [인쇄] p.5 |
| 연화 강성 환산 | DEM E ≈ 0.25 GPa (실제 1.6) · Coh 고정 ⇒ **Γ = 0.046 J m⁻²** → DEM 안식각 **37.6°** = 실험 **0.5 wt% PEG** 와 일치 | [인쇄] p.5 |
| 보정 결과 (Fig 7 인쇄) | PEG 0 · 0.5 · 1.5 · 2.5 · 3.5 wt% ↔ Γ **0.0 · 0.05 · 0.15 · 0.25 · 0.35 J m⁻²** ↔ DEM AoR **31 · 38 · 45 · 48 · 57°** | [인쇄] Fig 7 |
| 실험 AoR (Fig 6) | 31 · 37 · 48 (±2.5) · 48.5 (±3) · 55.5 (±2.5)° — **5 회 반복 평균** · 끈적할수록 막대가 크다 | [판독] · [인쇄] p.4 |
| "거의 선형" | Fig 6 의 위 축 (Γ 0–0.4) 과 아래 축 (PEG 0–4 wt%) 이 **같은 위치** = Γ = 0.1 × wt% 로 맞춘 표시 | [판독] Fig 6 · [인쇄] p.5 |
| 주 조건 | **2.5 wt% PEG** (선행 실험의 분리 지수 최저) → **EP–EP Γ = 0.250 J m⁻²** | [인쇄] p.5 |
| 혼합쌍 | 코팅–비코팅 = **절반** (JKR 근거라 적음) · 크기 차 = 식 (4) **Γ₂ = Γ₁ (R₁\*/R₂\*)^{8/5}** (인쇄 그대로) → **EP–BP 0.037 · EP–TAED 0.060 J m⁻²** | [인쇄] p.5 · 식 (4) |
| 안식각 측정법 (Fig 5) | 더미를 좌우로 나눠 **높이 10–90 % 구간** 의 수평 거리로 각도 → 좌우 평균 (코팅 많으면 표면 요동 때문) | [인쇄] p.4 |

### 3-4. 분리 결과 (§3 · Fig 9–14 · 20 · p.7–11)

| 양 | 비코팅 | 코팅 (2.5 wt%) | 표지 |
|---|---|---|---|
| 앞면 CoV — 실험 | **1.33 ± 0.12** | **0.83 ± 0.12** (−38 %) | [판독] Fig 10 |
| 앞면 CoV — DEM | 1.44 | 0.94 (−35 %) | [판독] Fig 10 |
| 본문 서술 | — | "CoV 최소 40 % 감소" · DEM ↔ 실험 "약 10 % 차" | [인쇄] p.7 |
| 무작위 CoV_r | 전체 더미 **0.21** · 앞면 층 **0.50** | 같음 | [인쇄] p.8 |
| S_n 앞면 — 실험 | 2.65 ± 0.27 | 1.66 ± 0.16 | [판독] Fig 13 (= CoV/0.50 [우리 산술]) |
| S_n 앞면 — DEM | 2.88 | 1.88 | [판독] Fig 13 |
| S_n 전체 더미 — DEM | **1.57** | **0.86** (−45 %) | [판독] Fig 13 |
| 본문 서술 | — | "총 70 % 넘게 감소" (§3.2) · "총 40 %, 벽 근처 거의 100 %" (결론) — **서로 다르고 그림과도 다름** | [인쇄] p.8 · p.11 |
| 층별 CoV (DEM, 뒤벽 1 → 앞벽 8) | 0.94 · 0.44 · 0.36 · 0.30 · 0.41 · 0.42 · 0.51 · 0.77 | 0.38 · 0.38 · 0.38 · 0.29 · 0.30 · 0.31 · 0.37 · 0.45 | [판독] Fig 12 |
| 층 평균 = Fig 14 CoV_enz | 0.519 (인쇄 0.52) | 0.358 (인쇄 0.36) | [우리 산술] · [인쇄] Fig 14 |
| TAED CoV | 0.74 (Fig 14) / 0.76 (본문) | 0.76 (Fig 14) / 0.74 (본문) — **순서가 그림 ↔ 본문 반대** · 어느 쪽이든 변화 무시 가능 | [인쇄] |
| 혼합물 안식각 | 실험 36.4° · DEM 36.0° | 실험 38.0° · DEM 37.6° | [인쇄] p.9 |
| 깔때기 배출 시간 | 2.22 s | 2.32 s (+5 %) | [인쇄] p.9 |
| Jenike ffc (2–8 kPa 평균) | **6.3** (6.15 · 6.55 · 5.75 · 6.55) | **4.4** (4.6 · 4.6 · 4.2 · 4.25) — 둘 다 '쉽게 흐름' (4–10) | [인쇄] p.9 · [판독] Fig 15 |
| 지나친 점착 (모든 EP 접촉 Γ 0.25) | — | **S_n 2.58 (CoV 0.98)** — 비코팅보다도 나쁨 · BP 미분이 EP 에 들러붙은 덩어리가 사태로 모서리에 | [인쇄] p.11 · Fig 20 |

- **비코팅 분리 모습**: EP 가 둥글고 BP 보다 크지만 **밀도 (2320 vs 780)** 때문에 더미 **가운데** 에 모이고 모서리 · 벽 · 바닥엔 적다 (크기 · 모양만이면 모서리로 갔을 것 — 저자).
- **깔때기 안 사전 분리 없음**: 출구 질량분율 TAED ≈ 0.053 · EP ≈ 0.020 이 시간에 따라 일정 (Fig 16) ⇒ 분리는 **더미 형성 중** 에 일어난다.
- **기전 (Fig 17–19)**: 비코팅 EP 는 표면에 떨어지며 다른 입자를 밀어내고 (**push-away**) 아래층에 묻혀 흐르는 위층을 벗어난다 — 충돌 뒤 비운동에너지가 ≈ 0.015 → 0 으로 빨리 떨어짐.  코팅 EP 는 위층에 붙잡혀 (**damper effect**) 0.022 → 0.0025 J kg⁻¹ 로 **더 오래 움직이며** 흐름을 따라 모서리까지 간다 (실험 윗면 사진에도 코팅 EP 가 표면에 보임, Fig 18).
- **처방 제언**: 붓는 높이를 낮추면 (충돌 속도 ↓ → 침투 ↓) 밀도 분리를 줄일 수 있다 (p.10).

### 3-5. 혼합 · 분리 지표 정의 (§2.6 · 식 5–7 · p.5–6)
- **CoV_i = σ_i / μ_i** (식 5) — 칸별 EP 화소 농도 (2D) · 질량분율 (3D) 의 표준편차 ÷ 평균.
- 무작위 기준: **σ_R = √(P(1−P)/N)** (식 6) — N = 칸에 들어갈 **같은 크기 · 모양** EP 수 = 칸 부피 × **0.6** (느슨한 충전, Onoda–Liniger) ÷ EP 부피 · 모서리 · 가장자리 칸은 부분 칸으로 보정 → 엑셀 난수로 칸마다 질량분율 배정 → **100 회 반복 평균 = CoV_r**.
- **S_n = CoV_m / CoV_r** (식 7, Poole 1964 와 같은 꼴) — **≤ 1 이면 잘 섞임 · > 1 이면 분리**.
- 유동성: 안식각 + **Jenike ffc = σ₁/σ_c** (식 8, Schulze 링 전단 · Table 3 분류: < 1 안 흐름 · 1–2 매우 점착 · 2–4 점착 · 4–10 쉽게 흐름 · ≥ 10 자유 흐름 — ⚠ 표 마지막 행이 "ffc < 10" 으로 인쇄 오기).

### 3-6. ★ 우리 산술 묶음 — 인쇄 식 · 숫자의 정합 점검

① **식 (4) 의 방향.**  식 (1) 에서 Coh = 일정이면 Γ⁵ ∝ R\*⁸ ⇒ **Γ₂ = Γ₁ (R₂\*/R₁\*)^{8/5}** 이다.  인쇄 식 (4) · Fig 4 흐름도는 **(R₁\*/R₂\*)** — 역수.  그리고 **인쇄 결과 (EP–BP 0.037 < EP–TAED 0.060)** 는 응집수 불변 방향과 맞는다 (R\*(EP–BP) < R\*(EP–TAED) 이므로 인쇄 식대로면 대소가 뒤집힌다) ⇒ **식 (4) 가 조판 · 표기 오류** 이고 계산은 불변 방향으로 한 것으로 보인다 [우리 산술 · 추정].  (정본 카드 `lischka2025_dem_eirich_intensive_mixer_dry_mixing` §4.3 도 같은 식에서 **γ ∝ R\*^{8/5}** 를 유도한다.)

② **교차쌍 Γ 의 출발값.**  본문 서술은 "2.5 wt% 의 0.250 → 코팅–비코팅 절반 0.125 → 크기 환산".  그런데 0.125 에서 불변 방향으로 환산하면 EP–BP **0.089–0.093** · EP–TAED **0.154–0.162** (반경 = 체 범위 중앙 또는 표의 부피 등가) 로 인쇄값의 **2.5–2.7 배**.  인쇄 **0.037 · 0.060** 은 출발값을 **Γ₁ ≈ 0.046–0.05 J m⁻²** (0.5 wt% 수준) 로 두면 재현된다 (0.034–0.037 · 0.057–0.065) [우리 산술] ⇒ 실제 DEM 에 들어간 교차쌍 값의 근거가 서술과 다를 가능성 — **원문으로는 판정 불가** [미확인].

③ **인쇄 응집수 1.6 × 10⁻³.**  Γ 0.086 · E 1.6 GPa · ν 0.25 · ρ 2320 · 반경 325 µm 로 식 (1)–(3) 그대로 (두 같은 구 R\* = 162.5 µm) 계산하면 **1.04 × 10⁻²** — 인쇄값의 6.5 배.  **R\* 자리에 입자 반경 325 µm** 를 넣으면 **1.64 × 10⁻³** 으로 재현된다 [우리 산술].  ⇒ 응집수를 **값으로** 다른 계와 비교하지 말 것 (비 · 환산에는 같은 R\* 규약이면 상쇄).

④ **연화 환산 0.086 → 0.046.**  Γ ∝ E\*^{2/5} 로 1.6 → 0.25 GPa 면 **0.041 J m⁻²** — 인쇄 0.046 은 E_DEM ≈ 0.34 GPa 에 해당 [우리 산술] (12 % 차 · 출처 [미확인]).

⑤ **감소율 서술.**  그림 판독: 앞면 CoV −35 · −38 % · 전체 S_n −45 % ↔ 본문 "최소 40 %" · "70 % 넘게" · 결론 "총 40 %, 벽 근처 거의 100 %" — 벽 층 CoV 는 0.94 → 0.38 (−60 %) · 0.77 → 0.45 (−42 %) [판독].

⑥ **지나친 점착의 S_n.**  CoV 0.98 · S_n 2.58 이면 CoV_r = **0.38** — 인쇄된 두 기준 (전체 0.21 · 앞면 0.50) 어느 쪽과도 맞지 않는다 [우리 산술] ⇒ 2.58 을 다른 S_n 과 직접 비교하지 말 것.

---

## 4. ★ 방법 — DEM · 모양 · 보정 · 입자 처리

### 4-1. 코드 · 접촉 (§2.2 · p.2)
EDEM 2.7.1 (DEM Solutions) · **Hertz–Mindlin** (탄성 · 마찰) + **JKR** (점착, "Tabor 기준상 큰 · 무른 입자 · 낮은 응력이라 타당") · 비코팅 계는 JKR 끔 (Hertz–Mindlin 만).  모델 세부는 ref 25 · 26 로 미룸.

### 4-2. 모양 (§2.4 · Fig 3)
XRT (Phoenix Nanotom) → Avizo 3D 재구성 → STL → **ASG (Cogency) sphere-clump** → **clump 구 수를 늘려가며 DEM 안식각이 실험 안식각에 닿는 최소 수** 를 고름 (BP · TAED 5 구, EP 1 · 2 · 3 구 — 장구 근사 3 구).  상세는 ref 30.

### 4-3. 점착 보정 — §3-3 표 · Fig 4 흐름도.

### 4-4. ★ 입자 처리 (우리 축 언어로)
- **강체 clump DEM** (형상 = XRT 근사 · 형상 변화 없음) · 연화 탄성 (G 100 MPa — 실제 EP 1.6 GPa 대비 E ≈ 1/6.4) · 소성 없음.
- 점착 = **JKR (탄성 점착)** — 코팅 EP 가 낀 접촉에만 · 혼합쌍 절반.
- 반발계수를 **점성 소산 대리** 로 낮춤 (EP–EP 0.10).
- 개수 ≈ 64 만 입자 (5-구 clump 라 구 요소 ≈ 320 만 [우리 산술]).

### 4-5. 기법 미니 용어집
- **응집수 (Cohesion number)** — JKR 분리 일 ÷ 중력 위치 에너지 꼴의 무차원수 · 강성 · 크기를 바꿀 때 Γ 를 환산하는 불변량.
- **JKR Γ (interfacial energy)** — 두 표면을 떼는 데 드는 단위 면적 에너지 (= 접착일 W) · 이 논문은 "Γ ≅ 2γ".
- **push-away 효과** — 떨어진 입자가 표면 입자를 밀어내고 아래층으로 파고드는 분리 기전 (Félix & Thomas 2004).
- **damper effect** — 끈적한 입자가 주변 상대 운동을 감쇠시켜 흐르는 층에 붙잡히는 것 (저자 용어).
- **Jenike ffc** — 최대 주응력 ÷ 비구속 항복응력 · 클수록 잘 흐른다.
- **CoV · S_n** — 칸 농도 변동계수 · 무작위 대비 비.

---

## 5. Figure set ★ (크롭 23 장 = `litdb/figures/alizadeh2018_dem_adhesion_calibration_segregation_heap/`)

| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1 | 실험 상자 사진 + DEM 기하 (치수 라벨 — '450 mm' 오기 의심) | D3 보정 장치 설계 예 |
| 2 | BP · TAED · EP 광학 사진 (400 µm 막대) | — |
| Table 1 | 입자 수 · 질량 · 모양 · 안식각 · G · ρ · 마찰 · 반발 (BP · TAED · EP · 벽) | ★ 보정된 입력 세트의 형식 — 우리 덱 표와 같은 칸 구성 |
| 3 | 모양 최적화 — clump 구 수 vs 안식각 (TAED) + XRT ↔ clump | 모양 보정의 "최소 구 수" 기준 |
| 4 | ★★ 점착 보정 흐름도 (Γ_CD = 0.5 Γ_CC · 응집수 크기 환산 인쇄) | ★★ D2 · D3 절차의 원형 |
| 5 | 점착 분말 안식각 측정법 (10–90 % 높이 · 좌우 평균) | D3 측정 규약 |
| 6 | 코팅량 vs 안식각 (실험 · DEM) + 위 축 보정 Γ | ★ 점착 ↔ 벌크 각도 보정 곡선 |
| Table 2 | EP · PEG 400 물성 (E 1.6 GPa · γ_PEG 0.043) | 출발값 출처 |
| 7 | 코팅량별 실험 더미 사진 ↔ DEM 더미 (Γ · AoR 인쇄) | ★ 보정 결과 한 컷 |
| 8 | 더미의 3D 칸 나누기 | 칸 = 관찰 척도 |
| Table 3 | Jenike ffc 흐름 분류 (⚠ 마지막 행 오기) | D3 앵커 해석 |
| 9 | 3 성분 더미 — 실험 · DEM · 지표 영상, 코팅 전후 | 분리 모습 |
| 10 | 앞면 CoV — 실험 · DEM, 코팅 전후 | §3-4 |
| 11 | DEM 층 (1 · 3 · 6 · 8) 별 EP 분포 | 깊이 방향 분리 |
| 12 | ★ 층별 CoV (뒤벽 → 앞벽) | ★ 벽 효과 정량 — 앞면 영상 편향 |
| 13 | S_n — 앞면 실험 · 앞면 DEM · 전체 DEM | ★ 2D ↔ 3D 지표 차 |
| 14 | DEM 더미 앞면 — 전 입자 · EP · TAED (CoV · AoR 인쇄) | 소량 성분만 바뀜 |
| 15 | Jenike ffc vs 예비 전단응력 (코팅 전후) | 벌크 유동성의 둔감함 |
| 16 | 깔때기 출구 질량분율 (TAED · EP) vs 시간 | 사전 분리 없음 |
| 17 | ★ 선택 EP 의 낙하 · 침투 (비코팅) ↔ 표면 체류 (코팅) + 모식 | ★ 점착이 흐르는 층에서의 체류를 바꾸는 기전 그림 |
| 18 | 실험 윗면 — 코팅 EP 가 표면에 보임 | 기전의 실험 증거 (정성) |
| 19 | 충돌 전후 비운동에너지 (코팅 · 비코팅) | 충돌 뒤 감속 차 |
| 20 | 지나친 점착 — 미분이 붙은 EP 덩어리 · 모서리 분리 | ★ 과점착 → 덩어리 → 재분리 |

## 6. Post-processing ★
- **무엇을**: 앞면 영상 색 분할 → 21 칸 화소 농도 → CoV · 몬테카를로 CoV_r → S_n · DEM 3D 칸 질량분율 → CoV · S_n · 8 층 CoV · 선택 입자 추적 (위치 · 비운동에너지) · 깔때기 출구 질량분율 · 안식각 (10–90 % 높이) · Jenike ffc.
- **도구**: EDEM 후처리 · 영상 분석 (도구명 미기재) · Excel 난수 (CoV_r).
- **안 한 것**: DEM 시드 반복 · 오차막대 (DEM) · 칸 크기 민감도 · 다른 무작위 기준 (3D 칸의 CoV_r 계산 상세) · 마찰 · 점착 동시 식별 (마찰은 선행 고정) · 입자 수준 접촉 지표.
- **우리 후처리 (이 카드)**: §3-6 ①–⑥ (식 4 방향 · 교차쌍 출발값 · 응집수 R\* 규약 · 연화 환산 · 감소율 · 과점착 CoV_r) · 부피 등가 지름 · 질량% · Fig 1 · 6 · 10 · 12 · 13 · 15 · 16 · 19 판독 (digitized.csv).

---

## 7. 우리 DEM+MPM 대비  →  `our_dem_baseline.md` (⚠ 정본 브랜치에서는 값 자리표시 상태 — 우리 수치는 메인 리포 코드 · 문서 출처를 병기)

| 항목 | 이 논문 (Alizadeh 2018) | 우리 (LIGGGHTS 믹서 드럼) | 차이 / 판정 |
|---|---|---|---|
| 공정 | 깔때기 → **더미 형성** (16 mm 상자) | **회전 드럼** 혼합 (CGF 151.4 · Fr 0.0827) | 분리 기전 (표면 침투 · 사태) 은 드럼 폭포층과 공유 · 장치는 다름 |
| 코드 · 점착 | EDEM · **JKR Γ** (면적당 에너지) | LIGGGHTS · **SJKR CED** (부피당 에너지 × 겹침 면적) | 정의가 다르다 — 다리 = 정본 `johnson1971_jkr_surface_energy_contact_elastic_solids` §7-1 (떼는 힘을 맞추면 CED = [9·W·E\*²/(4π²R\*)]^{1/3}) |
| 무차원 불변량 | **응집수** (에너지 · E\* 포함) | **Bo_code** (SJKR 평형 겹침 힘 ÷ 무게 — `scripts/make_mixer_deck.py` `bond_for_ced`) | ★ 다른 불변량 — 연화 · CG 때 어느 쪽을 지키는지에 따라 같은 실험 앵커에서 다른 CED 가 나온다 (§8-3) |
| 혼합쌍 규칙 | 코팅–비코팅 = **½ Γ** + 크기 환산 | 두 상 후보 CED 의 **min** · 벽 = 대각 ÷ 1.842 | ★ D2 — 그들 규칙이면 비점착 상대와도 절반의 점착이 남고, 우리 min 이면 0 쪽 |
| 보정 시험 | **단일 성분 더미 안식각** (코팅량 5 수준 × 5 회) | 없음 — SE–SE Bo_code 0.212 · LA AM_P 3.0 등은 **내부 기준점** (문헌 앵커 아님) | ★★ D3 의 빈칸을 이 절차가 채운다 (§8-1) |
| 강성 연화 | G 100 MPa (E 0.25 GPa · 실제 EP 1.6 GPa 의 1/6.4) | SE 1 × 10⁷ Pa · AM 1.037 × 10⁹ Pa (÷ 135) | 같은 인식론 (frame[2]) — 배수 전이 금지 |
| 모양 | XRT sphere-clump (안식각 최소 구 수) | 구 | 우리 구름마찰이 모양 대리 (μ_r 0.075, hare2026 세트) |
| 지표 | CoV · **S_n = CoV/CoV_r** (몬테카를로 무작위) · 칸 = 관찰 척도 | Lacey M (S_R² 실측 E0) | 둘 다 무작위 기준을 **같은 칸** 에서 잡는다 — 그들은 이항 몬테카를로 · 우리는 균일 삽입 런 |
| 결과 | 소량 성분 코팅 → 분리 감소 · 과점착 → 재분리 | (DEV) dev-bo AM–AM 응집 · dev-u 균일 γ 배율 — 논지 §3 어긋남 | 방향 정보만 — 계가 다르다 |

### 7-1. frame[5] — 어느 반쪽을 가졌나
**입자 배치 (분리) · 벌크 유동성** — DEM 쪽 반쪽 (그것도 혼합 단계) 만.  압축 · 전달 · 형상 소성은 없다.

---

## 8. ★★ 우리 연구에 주는 insight (번호마다: 논문이 보인 것 → 우리에게 뜻 → 할 일)

1. **D3 레시피 — 단일 성분부터.**  그들은 혼합물이 아니라 **EP 만의 더미 안식각** 으로 Γ 를 정했고, 혼합물의 안식각 · ffc 는 2 wt% 성분의 점착에 거의 반응하지 않았다 (36.4 → 38.0° · 6.3 → 4.4 · §3-4).  → 우리 D3: **SE 분말 단독** (그리고 NCM 단독) 의 안식각 · 유동성을 재고, 같은 기하의 **DEM 보정 런** (SE 단독 드럼 또는 더미) 에서 CED 를 맞춘다.  혼합물 시험은 검증용.  ⚠ 마찰을 고정한 채 점착만 맞췄다 — 우리도 **마찰 세트 (hare2026) 를 고정** 했으니 같은 식별 가정을 명시해야 한다.
2. **D2 — "절반" 규칙의 두 번째 근거.**  모델링 관례 (Alizadeh: Γ_CD = 0.5 Γ_CC) 와 측정 (Jarray: F_AB/F_AA ≈ 0.5, 같은 날 카드 `jarray2019_cohesion_driven_mixing_segregation_drum`) 이 같은 방향.  → 코팅 NCM (표면 = SE) 과 비코팅 NCM 이 섞인 실제 계나 부분 코팅을 표현할 때, **min 규칙은 혼합쌍 점착을 지운다** — 결합 규칙 후보에 **산술평균** 을 넣고 결과 전 등록 (논지 §4 D2).  ⚠ 두 근거 모두 "한쪽 표면만 끈적한" 특수 계 (실란 · PEG 막) — 반데르발스 지배 분말의 일반 규칙은 아니다.
3. **불변량 선택 = 결과를 바꾸는 결정.**  JKR 에서 떼는 힘은 E 와 무관하지만 분리 **일** 은 E\*^{−2/3} 에 걸린다 → 강성을 연화하면 Bo (힘) 를 지키느냐 Coh (에너지) 를 지키느냐에 따라 Γ 가 **E\*^{2/5}** 만큼 달라진다 (그들 E 1/6.4 연화면 ×0.48).  우리는 SJKR · 절대 Bo (힘) 를 지킨다.  → 논지 §2-4 ("살아남는 접촉" = 충돌 에너지 vs 접착 에너지) 가 맞다면 **에너지 기준 (응집수 · 붙는 임계 속도)** 이 더 직접적인 불변량일 수 있다 [추정] — 정본 `thorntonning1998_adhesive_elastoplastic_contact` (붙는 임계 속도) 와 함께, D2 를 정할 때 **어느 불변량을 지키는지** 를 등록 문서에 명시.
4. **코팅은 최적값이 있다 — 과점착은 덩어리를 만든다.**  EP 를 적당히 끈적하게 하면 분리가 줄지만 모든 EP 접촉을 0.25 로 올리면 미분 (BP) 이 EP 둘레에 붙은 **"씨앗 + 껍질" 덩어리** 가 사태로 모서리에 쌓여 S_n 2.58.  → 우리 논지의 "SE 가 코팅 AM 에 붙어 흩어진다" 는 **덩어리 크기 · 흐름 거동** 을 함께 봐야 한다 — 코팅 AM 이 SE 를 너무 많이 끌어당기면 SE 가 **AM 둘레에만 몰리고** (자유 SE 고갈) 덩어리가 크기 분리를 일으킬 수 있다 [추정].  → 관측량에 **AM–SE 부착 수 분포 (s2) + 덩어리 크기** 를 같이.
5. **2D 단면 · 벽 측정은 분리를 과장한다.**  16 mm 상자에서 벽 층 CoV 가 가운데의 2–3 배 · 앞면 S_n (2.88) 이 전체 (1.57) 의 1.8 배.  → 실험 대조 (SEM-EDS 단면 · 앞면 영상) 를 DEM 지표와 비교할 때 **같은 위치 · 같은 칸** 으로 (DEM 쪽에서 벽 층만 뽑아 비교).  같은 날 카드 `jarray2019_…` (드럼 앞면 영상) 에도 같은 한정어.
6. **무작위 기준을 같은 칸에서 몬테카를로로.**  CoV_r 를 칸마다 들어갈 입자 수로 이항 생성 → 칸 크기 의존을 **비** 로 상쇄 (S_n).  우리 Lacey 는 S_R² 를 **균일 삽입 런 실측** 으로 잡는다 (다분산 · 부피 가중이라 이항이 안 맞아서 — `scripts/measure_mixing_index.py` 머리말).  → 두 방식을 같은 침대에서 비교해 보는 것이 싸다 (계산만) [제안].  칸 크기는 **관찰 척도** (그들 = 세제 한 숟갈) 로 정당화 — 우리 칸 16×16×4 의 척도 근거를 등록 문서에 적을 것.

## 9. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "For a PEG-coated minor component, the DEM interfacial energy was calibrated against the single-component angle of repose (0–3.5 wt% PEG → Γ 0–0.35 J m⁻², AoR 31–57°), starting from twice the coating surface tension and rescaled with a cohesion number when the elastic modulus was softened (Alizadeh et al., Powder Technol. 2018)." [인쇄 p.5 · Fig 7]
- "Contacts between a coated and an uncoated particle were assigned half the coated–coated interfacial energy." [인쇄 p.5 · Fig 4]
- "Coating the 2 wt% enzyme placebo granules lowered the front-face coefficient of variation from about 1.33 to 0.83 in experiment and from 1.44 to 0.94 in DEM, while the bulk flowability of the mixture barely changed (ffc 6.3 → 4.4)." [판독 Fig 10 · 인쇄 p.9]
- "Setting all placebo contacts to a high interfacial energy (0.25 J m⁻²) produced agglomerates of fines around the granules and a higher segregation index than the uncoated case." [인쇄 p.11]
- ⚠ 식 (4) · 응집수 1.6 × 10⁻³ · 교차쌍 Γ · 감소율 40/70 % 는 §3-6 점검 없이 인용하지 말 것.

## 10. 주의/한계 (over-claim 방지 · 원문 비판)
1. **식 (4) 방향 오류** (응집수 불변과 역수 · 결과값과도 반대) — §3-6 ①.
2. **교차쌍 Γ 의 출발값이 서술과 다름** (재현 = Γ₁ ≈ 0.05) — §3-6 ②.
3. **응집수 값 1.6 × 10⁻³ 은 R\* 규약이 식 (2) 와 다를 때만** — §3-6 ③.
4. **0.086 → 0.046 환산** 이 Γ ∝ E\*^{2/5} 로는 0.041 — §3-6 ④.
5. **감소율 서술 셋이 서로 · 그림과 다름** (40 · 70 · 40 / 그림 35–45 %) — §3-6 ⑤.
6. **과점착 S_n 2.58 의 기준 CoV_r 0.38** 이 인쇄 기준과 다름 — §3-6 ⑥.
7. **표 약어 충돌** ("CoR" = 구름마찰 (본문) ↔ 반발 (표)) · Table 3 마지막 행 · Fig 1 '450 mm' · TAED CoV 순서 · 캡션 'TEAD' · 범례 'Unoated' · Table 2 'granul‘s'.
8. **"모세관 다리 없이 끈적" 의 근거 미제시** — PEG 400 은 상온 액체 [추정 · 일반 사실] 이라 액상 다리 · 점성력이 섞일 수 있다 — JKR 만으로 표현한 것이 가정.
9. **DEM 반복 · 오차 없음** · 비교 지표 (CoV) 가 칸 체계마다 다른 값 (앞면 21 칸 · 3D · 층) — 같은 이름의 다른 양.
10. **보정 식별성** — 마찰 · 구름마찰 · 반발을 고정 (선행 [30]) 한 뒤 Γ 하나를 안식각 하나로 맞춤 → 마찰 오차가 Γ 로 흡수될 수 있다.
11. **전이 한계** — 수백 µm 과립 · 낮은 Bo · 액상 고분자 코팅 · 더미 형성 ≠ µm 황화물 SE · 반데르발스 · 회전 드럼.  **숫자 전이 금지 · 절차 (단일 성분 보정 · 불변량 명시 · 혼합쌍 규칙 · 2D/3D 비교) 만 옮긴다.**

## 11. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)

| 번호 | 서지 (원문 목록 그대로) | 왜 · 카드 |
|---|---|---|
| 2 | J. Hærvig, U. Kleinhans, C. Wieland, H. Spliethoff, A.L. Jensen, K. Sørensen, T.J. Condra, On the adhesive JKR contact and rolling models for reduced particle stiffness discrete element simulations, Powder Technol. 319 (2017) 472–482 | ★ 연화 강성 JKR 의 엄밀 환산 — 우리 SJKR 연화와 직접 관련 · 카드 없음 |
| 3 | M.A. Behjani, N. Rahmanian, N. Fardina bt Abdul Ghani, A. Hassanpour, … Adv. Powder Technol. 28 (2017) 2456–2464 | 응집수 원전 — 카드 없음 |
| 7 | M. Asachi, A. Hassanpour, M. Ghadiri, A. Bayly, Analysis of minor component segregation in ternary powder mixtures, EPJ Web Conf. 140 (2017) 13013 | 같은 실험의 원전 (2.5 wt% 최적) — 카드 없음 |
| 8 | I. Figueroa, H. Li, J. McCarthy, Predicting the impact of adhesive forces on particle mixing and segregation, Powder Technol. 195 (2009) 203–212 | 점착 혼합 · 분리 예측 — 카드 없음 · ★ 다음 후보 (McCarthy 계열) |
| 9 | J. Yang, A. Silva, A. Banerjee, R.N. Dave, R. Pfeffer, Dry particle coating for improving the flowability of cohesive powders, Powder Technol. 158 (2005) 21–33 | 건식 코팅 → 유동성 (같은 날 카드 후보 #23 Pfeffer 2001 의 후속) — 카드 없음 |
| 12 | F. Fulchini, U. Zafar, C. Hare, M. Ghadiri, … Powder Technol. 322 (2017) 417–427 | 유동 보조제 표면 피복률 ↔ 유동성 — 카드 없음 |
| 18 | K.L. Johnson, K. Kendall, A.D. Roberts, Surface energy and the contact of elastic solids, … 324 (1971) 301–313 | 정본 카드 `johnson1971_jkr_surface_energy_contact_elastic_solids` |
| 20 | M. Pasha, S. Dogbe, C. Hare, A. Hassanpour, M. Ghadiri, A linear model of elasto-plastic and adhesive contact deformation, Granul. Matter 16 (2014) 151–162 | 탄소성 점착 선형 모델 — 카드 없음 |
| 21 | C. Thornton, Z. Ning, A theoretical model for the stick/bounce behaviour of adhesive, elastic-plastic spheres, Powder Technol. 99 (1998) 154–162 | 정본 카드 `thorntonning1998_adhesive_elastoplastic_contact` |
| 27 | M. Capece, R. Ho, J. Strong, P. Gao, Prediction of powder flow performance using a multi-component granular Bond number, Powder Technol. 286 (2015) 561–571 | **다성분 입상 Bond 수** — 우리 3 상 Bo 정의에 직접 · 카드 없음 · ★ 다음 후보 |
| 30 | M. Alizadeh, A. Hassanpour, M. Pasha, M. Ghadiri, A. Bayly, The effect of particle shape on predicted segregation in binary powder mixtures, Powder Technol. 319 (2017) 313–322 | 마찰 · 모양 보정 원전 — 카드 없음 |
| 33 | S.C. Thakur, J.Y. Ooi, H. Ahmadian, Scaling of discrete element model parameters for cohesionless and cohesive solid, Powder Technol. 293 (2016) 130–137 | Γ ∝ R² 스케일링 (대안) — 카드 없음 |
| 43 | G.R. Chandratilleke, A.B. Yu, J. Bridgwater, K. Shinohara, A particle-scale index in the quantification of mixing of particles, AICHE J. 58 (2012) 1099–1118 | 정본 카드 `chandratilleke2012_particle_scale_mixing_index` |
| 44 | P.M.C. Lacey, The mixing of solid particles, Chem. Eng. Res. Des. 75 (1997) S49–S55 | Lacey 재수록판 (원저 1954 = 같은 날 카드 후보 #30) |
| 45 · 46 | A. Kukukova, J. Aubin, S.M. Kresta, Chem. Eng. Res. Des. 87 (2009) 633–647 · AICHE J. 54 (2008) 3068–3083 | 혼합의 세 차원 · 표본 방법 · 척도의 CoV 영향 — 카드 없음 |
| 49 | G.Y. Onoda, E.G. Liniger, Random loose packings of uniform spheres and the dilatancy onset, Phys. Rev. Lett. 64 (1990) 2727–2730 | CoV_r 의 0.6 출처 — 카드 없음 |
| 55 | G. Félix, N. Thomas, Evidence of two effects in the size segregation process in dry granular media, Phys. Rev. E 70 (2004) 051307 | push-away 효과 — 카드 없음 |

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-10-13)
- 본문 12 쪽 텍스트 층 전수 (pdftotext raw · layout) · 식 (1)–(4) = 300 dpi 렌더로 대조 (텍스트 층이 지수 · 분수를 깨뜨림 — 식 (4) 의 8/5 · 방향 확인).
- 그림 20 · 표 3 = 크롭 23 장 (래스터 16 = 원본 300 dpi 경계 · 벡터 그림 4 (Fig 6 · 12 · 15 · 16) = 그리기 요소 합집합 + 축 라벨 여백 · 표 3 = 벡터 텍스트) — 전부 열람.
- 수치 재현: 응집수 (R\* 규약 3 × E\* 규약 3) · 연화 환산 · 교차쌍 Γ (출발값 3 × 반경 규약 2) · 부피 등가 지름 · 질량% · 감소율 · CoV_r 역산 · Fig 12 층 평균 — scratch 스크립트 (저장 안 함), 결과는 §3-6.
- 정본 litdb 중복 확인: DOI `powtec.2018.08.028` · 'Alizadeh' · 제목 낱말로 `litdb/` 전수 grep — 원저 카드 없음 (`jadidi2023_…` 가 Alizadeh 2013 · 2014 를 인용할 뿐).

## 🔗 관련 카드
- 점착 접촉 · 보정: [`johnson1971_jkr_surface_energy_contact_elastic_solids`](johnson1971_jkr_surface_energy_contact_elastic_solids.md) (JKR 원전 · SJKR CED 대응식) · [`thorntonning1998_adhesive_elastoplastic_contact`](thorntonning1998_adhesive_elastoplastic_contact.md) · [`luding2008_cohesive_frictional_contact_models`](luding2008_cohesive_frictional_contact_models.md) · [`coetzee2017_dem_calibration_review`](coetzee2017_dem_calibration_review.md) · [`paulick2015_elastic_particle_properties_dem_review`](paulick2015_elastic_particle_properties_dem_review.md).
- 건식 혼합 DEM · 응집수 스케일링: [`lischka2025_dem_eirich_intensive_mixer_dry_mixing`](lischka2025_dem_eirich_intensive_mixer_dry_mixing.md) (γ ∝ R\*^{8/5}) · [`hare2026_dem_pept_dry_mixing_nmc622_eirich`](hare2026_dem_pept_dry_mixing_nmc622_eirich.md) · [`frankenberg2024_dem_high_intensity_mixer_assb`](frankenberg2024_dem_high_intensity_mixer_assb.md).
- 같은 날 카드: [`jarray2019_cohesion_driven_mixing_segregation_drum`](jarray2019_cohesion_driven_mixing_segregation_drum.md) (실측 F_AB ≈ ½ F_AA · 드럼 앞면) · [`chandratilleke2012_particle_scale_mixing_index`](chandratilleke2012_particle_scale_mixing_index.md).
- 혼합지수: [`jadidi2023_dem_batch_solid_mixers_review`](jadidi2023_dem_batch_solid_mixers_review.md) · [`nadeem2023_gnn_mixing_index`](nadeem2023_gnn_mixing_index.md) · [`chibwe2020_nnsi_segregation_index`](chibwe2020_nnsi_segregation_index.md).

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
