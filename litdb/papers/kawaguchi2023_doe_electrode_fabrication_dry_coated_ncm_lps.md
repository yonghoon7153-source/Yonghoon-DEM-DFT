<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 사용자가 특히 원한 항목. 깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md ·
     형식 이웃 = nakamura2020_dry_coating_ncm_li3ps4_core_shell.md · kawaguchi2017_dry_coating_parametric_na2so4_model_se.md (같은 그룹 · 같은 날 묶음).
     쪽 표기 = 본문 "p.N" (본문 PDF N 쪽 = 학술지 인쇄 쪽 N, 1–15 · 논문 번호 104264) · SI "SI p.N" (SI PDF 1–3 쪽).
     값 표지: [인쇄] = 본문 · SI · 표 · 그림 안에 숫자로 적힌 값 · [판독] = 그림에서 읽은 값 (litdb/figures/<slug>/digitized.csv — 그림 4 · 8 막대 높이를
     PDF 벡터 경로에서 읽음, ±0.001) · [우리 산술] = 인쇄값으로 우리가 다시 한 계산 · [추정] = 우리 해석 · 가정이 든 어림 (가정을 그 자리에 적음) ·
     [미확인] = 원문 (본문 15 쪽 + SI 3 쪽 전수) 에 없음.
     원문 18 쪽 텍스트 층 전수 + 그림 9 · 표 4 · SI 그림 3 · 표 1 = 크롭 17 장 전부 렌더로 열람.  표 1–4 는 칸마다 렌더와 대조했고 ANOVA · MLR 은 표 (a) 값으로 전부 다시 계산했다. -->

# 건식 충격 코팅 NCM@Li₃PS₄ 코어–셸 vs 막자 단순 혼합 — 전극 제작 조건 (SE 질량비 Xs 0.1 / 0.3 · 압축압 P 180 / 360 MPa · 셀 체결 토크 Ts 0.5 / 2.5 N·m) 2³ 완전요인 DOE · ANOVA · 다중선형회귀: 단순 혼합은 **P** 가, 코팅은 **Xs** 가 첫 방전 용량을 좌우 (도전재 없음 — 코팅 Xs 0.3 셀은 NCM–NCM 전자 접촉이 끊겨 1.8–11.0 mAh/g) · 코팅 Xs 0.1 (129.9 mAh/g) 이 단순 혼합 Xs 0.3 (119.8) 을 넘는다 — Takashi Kawaguchi · Hideya Nakamura · Eiji Hayakawa · Shuji Ohsaki · Satoru Watano (오사카공립대, Adv. Powder Technol. 2023)

> slug `kawaguchi2023_doe_electrode_fabrication_dry_coated_ncm_lps` · DOI `10.1016/j.apt.2023.104264` · type `exp + 통계 (건식 충격 블렌딩 코팅 · SEM/EDX · 입도 · UV-vis 순조성 · 반쪽셀 충방전 50 회 · EIS Rs/Rct · 2³ 완전요인 DOE · ANOVA · MLR · 반응표면 · 표준화 편회귀계수; DEM · MPM · 수송 계산 없음)` · PDF `d9f5750a-26._Statistical_analysis_of_electrode_fabrication_process_for_all-solid-state_batteries_and_effects_of_electrode_fabrication_conditions_on_battery_performance.pdf` · SI `264c2375-26._Sup_Statistical_analysis_of_electrode_fabrication_process_for_all-solid-state_batteries_and_effects_of_electrode_fabrication_conditions_on_battery_performance.pdf` · digested `2026-10-13` · status ✅
>
> **원제**: *Statistical analysis of electrode fabrication process for all-solid-state batteries and effects of electrode fabrication conditions on battery performance* (p.1)
> **저자 · 소속 (p.1 · SI p.1 같음)**: Takashi Kawaguchi · **Hideya Nakamura\*** · Eiji Hayakawa · Shuji Ohsaki · Satoru Watano — Department of Chemical Engineering, **Osaka Metropolitan University**, 1-1 Gakuen-cho, Naka-ku, Sakai, Osaka 599-8531, Japan (\* 교신 hideyanakamura@omu.ac.jp)
> *Advanced Powder Technology* **34** (2023) 104264 · 접수 2023-07-05 · 수정 2023-10-12 · 승인 2023-10-23 · 온라인 2023-11-01 (p.1) · 연구비 JSPS KAKENHI 18H01769 · 23H01748 + JST ALCA-SPRING (p.14) · 이해상충 없음 진술 (p.14) · 데이터 공개 진술 없음.
> **같은 그룹 계보 · 같은 축 카드 (링크만)**: [`nakamura2020_dry_coating_ncm_li3ps4_core_shell`](nakamura2020_dry_coating_ncm_li3ps4_core_shell.md) (ref 24 — 같은 장치 · 같은 13,000 rpm · 5 min · 같은 NCM111 (LiNbO₃) · 같은 순조성 정량 (UV-vis) · 같은 총 SE 비교의 원형) · [`kawaguchi2017_dry_coating_parametric_na2so4_model_se`](kawaguchi2017_dry_coating_parametric_na2so4_model_se.md) (ref 28 — 공정 창) · [`sakuda2013_sulfide_mechanical_property`](sakuda2013_sulfide_mechanical_property.md) (ref 20 — 상온 가압 소결) · [`asano2017_ncm111_li3ps4_composite_electronic_ionic_conductivity`](asano2017_ncm111_li3ps4_composite_electronic_ionic_conductivity.md) (같은 NMC111–Li₃PS₄ 계의 σ_e · σ_ion — 이 논문에는 σ 측정이 없다) · [`so2022_dem_compaction_coated_particles_assb`](so2022_dem_compaction_coated_particles_assb.md) (코팅 vs 혼합의 DEM 압축 · 코팅의 σ_e 차폐).
> **판독 원자료**: `litdb/figures/kawaguchi2023_doe_electrode_fabrication_dry_coated_ncm_lps/digitized.csv` (27 행 — 그림 4 · 8 막대 높이 벡터 판독 + 표 (a) 값으로 다시 계산한 표준화 계수) · 크롭 17 장 `figures.json`.

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: NCM111 (LiNbO₃ 1 wt% 선코팅 · 개수 중앙 4.70 µm) 에 액상 진탕 합성 Li₃PS₄ (개수 중앙 0.37 µm · 0.91 × 10⁻⁴ S/cm) 를 **Nara 건식 충격 블렌딩 (13,000 rpm · 5 min · 투입 90 : 10)** 으로 입힌 코어–셸 분말 (순 LPS **5.6 wt%**) 과 막자 30 min 단순 혼합을, **도전재 없는** 반쪽셀 (복합 양극 10 mg / LPS 80 mg / Li–In) 에서 SE 비 Xs · 압축압 P · 체결 토크 Ts 의 2³ 완전요인으로 각 8 셀 (총 16 셀 · 조건마다 1 셀) 돌려 ANOVA · MLR 로 보면, **단순 혼합의 첫 방전 용량은 P > Xs > Ts 순으로 (P 가 미세공극을 없애 Rs 를 낮춤), 코팅은 Xs > Ts > Xs·Ts 순으로 (Xs 를 올리면 NCM–NCM 접촉이 사라져 Rct ↑ · 용량 ↓)** 좌우되고, 코팅 Xs 0.1 이 단순 혼합 Xs 0.3 과 같거나 높은 성능 (첫 방전 129.9 vs 119.8 mAh/g 실측 · 50 회 유지율 최대 92 vs 90 %) 을 낸다 — 다만 **코팅 Xs 0.3 셀은 1.8–11.0 mAh/g 로 무너진다** (p.10–14 · 표 1–4).

| 우리 질문 | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① 공정 변수 (장치 · 속도 · 시간 · 에너지 · 온도) | 코팅: **dry impact-blending device (Nara Machinery Co., Ltd.)** — 챔버 (냉각 재킷) · 날 달린 회전자 · 순환관 · 배출 밸브 · 회수 용기 · 백 필터 (Fig 2) · 막자 예비 혼합 → 투입 · **NCM : LPS = 90.0 : 10.0 wt% · 13,000 rpm · 5 min** · Ar 글러브박스 이슬점 < 193 K.  회전자 지름 · 선속도 · 투입 질량 · 에너지 · 온도 [미확인] — [우리 산술] 같은 그룹 Kawaguchi 2017 의 Hybridizer NHS-0 회전자 (118 mm) 라면 13,000 rpm ≈ **80 m/s** (장치 모델명이 이 논문에 없어 같은 회전자인지는 [추정]) | [인쇄] p.3–4 · Fig 2 |
| ② 피복을 어떻게 쟀나 · 값 | 피복률 % · 두께 **없음** — SEM/EDX (Mn · S 가 같은 자리) 정성 + 입도 (코팅 전후 NCM 분포 같음 = 파손 없음) + UV-vis (255 nm) 순 LPS **5.6 wt%**.  [추정 — 밀도 NCM 4.7 · LPS 1.9 g/cm³ 가정 (원문에 밀도 없음)] 5.6 wt% 를 반지름 2.35 µm 구에 고르게 입히면 껍질 ≈ **0.11 µm** | [인쇄] p.5 · p.9 · Fig 3 |
| ③ 코팅이 SE 를 얼마나 쓰나 · 잃나 | 투입 10 → 순 **5.6 wt%** (투입 LPS 의 56 % 만 분말에 남음 [우리 산술]) — 손실 원인 서술 없음 · 모자란 몫은 **막자로 자유 LPS 추가** (원문 "4.4 wt% for Xs = 0.1 and 24.4 wt% for Xs = 0.3" = Xs − 5.6 의 차; 정확한 추가 질량분율은 4.66 · 25.85 wt% [우리 산술]) ⇒ 양극 안 LPS 중 **껍질 몫 53 % (Xs 0.1) · 14 % (Xs 0.3)** [우리 산술] | [인쇄] p.9 · [우리 산술] |
| ④ σ_ion · σ_e · 공극률 · 용량 | **σ_ion · σ_e · 공극률 · 두께 미측정**.  EIS: Rs (> 100 kHz · "solid electrolyte") · Rct (100 k–100 Hz) · 첫 방전 Q1st · 50 회 유지율 Qr.  최고 셀: 단순 혼합 No.8 (Xs 0.3 · 360 MPa · 2.5 N·m) **119.8 mAh/g · Rs 935.9 Ω · Rct 56.4 Ω** ↔ 코팅 No.4 (Xs 0.1 · 360 · 2.5) **129.9 · 830.4 · 31.8** · 코팅 Xs 0.3: **2.4 · 4.5 · 1.8 · 11.0 mAh/g** | [인쇄] 표 1a · 2a · p.11 |
| ⑤ ★ 같은 Xs (= 같은 총 SE) 에서 코팅 ÷ 단순 혼합 | Xs 0.1: Q1st **×3.20 · ×3.57 (180 MPa)** · **×1.09 · ×1.21 (360 MPa)** · Rs ×0.63 · ×0.63 (180) · ×1.06 · ×0.88 (360) · Rct ×2.09 · ×1.15 · ×1.30 · ×0.77 (**4 중 3 에서 코팅이 높다**) · Qr 4 중 3 에서 코팅이 높다 (66 vs 70 % 하나 낮음) / Xs 0.3: Q1st **×0.02–0.09** | [우리 산술] 표 1a–4a |
| ⑥ 공정 민감도 (Xs 0.1 안에서만 — 코팅 Xs 0.3 붕괴를 뺀 비교) | P 180 → 360 MPa: Q1st **+60.7 (단순) vs +10.8 mAh/g (코팅)** · Rs −1,098 vs −310 Ω / Ts 0.5 → 2.5 N·m: Q1st **+22.3 vs +42.1 mAh/g** ⇒ 코팅은 **압축압 의존을 체결압 의존으로 바꾼다** | [우리 산술] 표 1a · 2a |
| ⑦ DEM · 모델 | **없음** — 통계 모형 (MLR) 뿐.  기전 설명 = SEM 단면 정성 (미세공극 · NCM 균열 · NCM–NCM 접촉) | [인쇄] p.10–13 |

⛔ **한정어 (떼지 말 것)**: ① **조건마다 셀 1 개** (반복 없음) — ANOVA 오차 = F < 2 인 상호작용 항을 모은 것 (p.8) · 일부 모형은 계수 7 개 / 점 8 개 (R² 0.999 는 거의 포화) ② SE = **Li₃PS₄** (액상 진탕 · 0.91 × 10⁻⁴ S/cm — LPSCl 아님) · CAM = **NCM111** (LiNbO₃) · **도전재 · 바인더 없음** ③ **Rs 는 복합 양극만의 저항이 아니다** — 같은 P 로 함께 눌린 LPS 분리막 (80 mg) 의 직렬 저항이 들어 있고 원문은 나누지 않는다 (§10-3) ④ **표 1 (d) 는 표 2 (d) 의 복사** — 단순 혼합 Rct 의 ANOVA · MLR 로 쓸 수 없다 (그림 4c 는 맞다 · §10-1) ⑤ MLR 의 상호작용 항은 **평균 중심화** 로 읽어야 인쇄 계수 · 본문 최댓값이 재현된다 (원문 미기재 · §10-2) ⑥ Xs 0.2 반응표면 (그림 7b · e · 9b) = 측정 없는 **선형 보간** ⑦ 반쪽셀 · 25 °C · 0.13 mA/cm² · 50 회.

---

## 1. 한 줄 요약

같은 그룹이 앞서 보인 "건식 코팅 코어–셸 분말이 막자 혼합보다 낫다" (Nakamura 2020 — 같은 장치 · 같은 조건) 를, 분말 뒤의 **전극 제작 조건** (SE 비 · 압축압 · 셀 체결 토크) 까지 넓혀 통계적으로 다시 본 논문.  2³ 완전요인 실험 (각 시료 8 셀) 의 첫 방전 용량 · 50 회 유지율 · EIS 저항을 ANOVA 와 다중선형회귀로 분석해, 단순 혼합은 압축압이 (공극 제거 → Rs ↓), 코팅은 SE 비가 (높이면 NCM 사이 전자 접촉이 막힘 → Rct ↑) 첫 용량의 지배 인자임을 보이고 (그림 4 · 5 · 6), 유지율은 단순 혼합에서 SE 비가 지배 (높으면 NCM 균열 억제) 하지만 코팅에서는 어느 조건도 유의하지 않다고 (표 4) 정리한다.  결론 문장은 "코팅 분말은 더 적은 SE · 더 낮은 압축압 · 체결 토크에서도 같거나 높은 성능" (p.1 · p.14).

## 2. 메타

| 저자 | 저널/년 | DOI | 소재 | 연구유형 |
|---|---|---|---|---|
| T. Kawaguchi · **H. Nakamura\*** · E. Hayakawa · S. Ohsaki · S. Watano (오사카공립대 화공) | *Adv. Powder Technol.* 34 (2023) 104264 | 10.1016/j.apt.2023.104264 | **LiNi₁/₃Co₁/₃Mn₁/₃O₂ (NCM111)** LiNbO₃ 1 wt% 선코팅 · 개수 중앙 4.70 µm (공급처 [미확인]) / **Li₃PS₄ (LPS)** 75Li₂S·25P₂S₅ 액상 진탕 합성 [29,30] · 개수 중앙 0.37 µm · 0.91 × 10⁻⁴ S/cm (측정 조건 [미확인]) · 도전재 · 바인더 없음 | 실험 (건식 코팅 · SEM/EDX · 입도 · UV-vis · 반쪽셀 · EIS) + 통계 (DOE · ANOVA · MLR · 반응표면 · 감도).  **DEM · MPM · 수송 계산 없음** |

- 키워드 (p.1): All-solid-state battery · Electrode fabrication · Design of experiment · Dry coating.
- KETI 단서와는 무관 (소속 = 오사카공립대 단독).

---

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. 시료 · 코팅 (p.3–5 · p.9 · Fig 1–3)

| 항목 | 값 | 표지 · 쪽 |
|---|---|---|
| NCM | NCM111 · **LiNbO₃ 1 wt% 선코팅** (계면 저항 감소 목적) · **개수 기준 중앙 지름 4.70 µm** · 1 차 입자가 "rectangular-shaped primary grains" (p.9 · Fig 1a · 3a) | [인쇄] p.3 · p.9 |
| LPS | 75 mol% Li₂S + 25 mol% P₂S₅ → **액상 진탕법** (ref 29 · 30) · **개수 중앙 0.37 µm** · **0.91 × 10⁻⁴ S/cm** (= 0.091 mS/cm) · SEM 은 얇은 판 조각 덩어리 (Fig 1b [판독 — 육안]) | [인쇄] p.3 · Fig 1 |
| 장치 | dry impact-blending device (Nara Machinery Co., Ltd.) — 챔버 · 날 달린 회전자 · 순환관 (본문) + 냉각 재킷 · 배출 밸브 · 회수 용기 · 백 필터 (Fig 2 표지) · 입자–장치 · 입자–입자 충돌의 큰 충격력 → 무른 LPS 가 단단한 NCM 표면에서 **소성 변형 · 합체** → 고른 코팅층 (ref 24) | [인쇄] p.3 · Fig 2 |
| 조건 | **90.0 : 10.0 wt% · 13,000 rpm · 5 min** (앞선 연구 [24–28] 에 근거) · Ar · 이슬점 < 193 K · 막자 예비 혼합 (시간 [미확인]) | [인쇄] p.3–4 |
| 순조성 | 코팅 분말 + 에탄올 → 진탕 1,500 rpm · 900 s (CM-1000, EYELA) 로 LPS 완전 용해 → 원심 13,000 rpm · 600 s (3700, KUBOTA) → 상등액 **255 nm** 흡광 (UV-1800, Shimadzu) → **순 LPS 5.6 wt%** (세부 = ref 24) | [인쇄] p.5 · p.9 |
| NCM 손상 | LPS 를 에탄올로 씻어 낸 NCM 의 레이저 회절 입도 (SALD-7100, Shimadzu) = 원 NCM 과 같음 → **파손 없음** (Fig 3c) · 코팅 분말 곡선에 LPS 크기 봉우리 없음 [판독 — 육안] | [인쇄] p.9 · Fig 3c |
| 형태 | 단순 혼합: NCM 1 차 입자 표면이 그대로 드러나고 LPS 몇 개만 붙음 / 코팅: 매끈한 표면 · Mn (NCM) 과 S (LPS) 가 EDX 에서 같은 자리 (Fig 3a · b) | [인쇄] p.9 |
| 양극 분말 조립 | 단순 혼합 = NCM + LPS 막자 **30 min** / 코팅 = 코팅 분말 + 자유 LPS 를 **막자**로 섞어 Xs 를 맞춤 (그 막자 시간 [미확인]) | [인쇄] p.4 · p.9–10 |

### 3-2. 반쪽셀 · 시험 (p.4–6 · SI Fig S1 · Table S1 · Fig S2)

| 항목 | 값 | 표지 · 쪽 |
|---|---|---|
| 층 쌓기 | LPS **80 mg** → 다이 (안지름 **10.1 mm**) **40 MPa · 5 s** → 복합 양극 **10 mg** → **P · 300 s** 단축 압축 (2 층 펠릿) → In · Li 박을 펀치 (지름 **10.0 mm**) 에 붙여 **90 MPa · 300 s** (Li–In 음극) | [인쇄] p.4 |
| 음극 박 | In (φ9 × 0.1 mm) · Li (φ7 × 0.25 mm) · In (φ9 × 0.3 mm) | [인쇄] SI Fig S1 |
| 체결 | 위아래 펀치를 두 판 사이에 끼우고 **볼트 4 개** 를 토크 **Ts** 로 조임 (너트 M6 × 4 · 절연 시트 · 금속판) · 토크 → 압력 환산 **없음** | [인쇄] p.4 · SI Fig S1 |
| [우리 산술 · 추정] 체결압 | 볼트 식 T = K·F·d 에 **K = 0.2 (가정 — 원문 없음)** · d = 6 mm (M6) · 힘이 전부 10.0 mm 펀치로 간다고 놓으면 Ts 0.5 → **≈21 MPa** · 2.5 → **≈106 MPa** (마찰 · 와셔 · 절연 시트 무시 — 자릿수 감만) | [추정] |
| [우리 산술] 면적 · 적재 | 다이 면적 0.801 cm² · 복합 양극 **12.5 mg/cm²** (NCM 11.2 · 8.7 mg/cm² at Xs 0.1 · 0.3) | [우리 산술] |
| 충방전 | BTS2004 (Nagano) · **298 K** · 조정 4 회 CC **0.064 mA/cm²** · 3.1–4.3 V (vs. Li⁺/Li 표기) → 시험 50 회: 충전 **CCCV 0.13 mA/cm² → 4.3 V (끝 전류 0.026 mA/cm²)** · 방전 **CC 0.13 mA/cm² → 3.1 V** | [인쇄] p.5 · Table S1 |
| [우리 산술] 율 | 0.13 mA/cm² = 0.104 mA → NCM 질량당 **11.6 mA/g (Xs 0.1) · 14.9 mA/g (Xs 0.3)** · 실측 용량 기준 ≈0.09 C (코팅 No.4) · ≈0.12 C (단순 No.8) — **같은 면적 전류라 Xs 0.3 쪽 질량당 전류가 1.29 배** | [우리 산술] |
| EIS | SP-200 (Bio-Logic) · SOC 100 % · 10 mV · 7 MHz–10 mHz · **Rs = > 100 kHz** ("resistance of solid electrolyte", ref 32) · **Rct = 100 k–100 Hz** (양극 고체–고체 계면 전하이동) · 100–0.2 Hz = 음극 Li 확산 (분석 제외) · 등가회로 맞춤 방법 [미확인] | [인쇄] p.5–6 · Fig S2 |
| 용량 단위 | mAh/g-NCM (Fig S3 축) | [인쇄] SI p.3 |

### 3-3. DOE · 통계 절차 (p.6–9)

| 항목 | 값 | 표지 · 쪽 |
|---|---|---|
| 설계 | **3 인자 2 수준 완전요인** — Xs 0.1 / 0.3 (양극 안 LPS 질량비) · P 180 / 360 MPa · Ts 0.5 / 2.5 N·m · 수준 범위 = 기존 연구 [11,19] 의 조건 · 시료 2 종 × 8 = **16 셀** · **반복 없음** (표에 조건마다 값 하나 · 반복 서술 없음) | [인쇄] p.6 · 표 1–4 |
| 반응값 | Q1st (첫 방전 · mAh/g) · Qr1st-50th = Q50th/Q1st · Rs · Rct (1 회 뒤) · ΔRs = Rs50th − Rs1th · ΔRct (원문 "1th" 표기) | [인쇄] p.6 · p.11 |
| 절차 | ① DOE 데이터 ② ANOVA → 유의 인자 ③ 그 인자로 MLR ④ 반응표면 ⑤ 표준화 편회귀계수로 감도 | [인쇄] p.6 |
| ANOVA | 주효과 SS (식 1–6) · 상호작용 SS (식 7–12) · SSe = SST − Σ (식 14) · MS = SS/df · F = MS/MSe · **F < 2 인 항은 오차에 합침** (다른 항의 F 가 줄면 안 합침) · p 값 = Excel FDIST · 유의 p < 0.05 · "dominant trend" p < 0.10 | [인쇄] p.7–8 · p.10 |
| MLR · 감도 | Y = b₀ + Σ bᵢXᵢ + Σ bᵢⱼXᵢXⱼ + e (식 17) · 최소제곱 · **표준화 편회귀계수 bᵢ\* = bᵢ·σᵢ/σ_Y** (식 18) | [인쇄] p.8–9 |

### 3-4. ★ 첫 사이클 결과 — 표 1 (a) 단순 혼합 · 표 2 (a) 코팅 [인쇄]

| No. | Xs | P (MPa) | Ts (N·m) | 단순 Q1st | 단순 Rs1st (Ω) | 단순 Rct1st (Ω) | 코팅 Q1st | 코팅 Rs1st (Ω) | 코팅 Rct1st (Ω) |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.1 | 180 | 0.5 | 24.1 | 2300.5 | 63.5 | 77.1 | 1450.1 | 132.7 |
| 2 | 0.1 | 180 | 2.5 | 29.5 | 2072.3 | 63.8 | 105.2 | 1310.8 | 73.1 |
| 3 | 0.1 | 360 | 0.5 | 67.9 | 1233.2 | 79.6 | 73.9 | 1310.6 | 103.4 |
| 4 | 0.1 | 360 | 2.5 | 107.1 | 944.1 | 41.5 | **129.9** | 830.4 | 31.8 |
| 5 | 0.3 | 180 | 0.5 | 42.1 | 2519.9 | 202.4 | 2.4 | 1357.4 | 363.5 |
| 6 | 0.3 | 180 | 2.5 | 63.0 | 2245.6 | 127.4 | 4.5 | 1395.7 | 285.7 |
| 7 | 0.3 | 360 | 0.5 | 102.7 | 1157.3 | 94.2 | 1.8 | 1272.4 | 524.0 |
| 8 | 0.3 | 360 | 2.5 | **119.8** | 935.9 | 56.4 | 11.0 | 790.6 | 165.1 |

(Q1st 단위 mAh/g.  두 표의 셀 배치는 같다 — No.1–4 Xs 0.1 · No.5–8 Xs 0.3 · 그 안에서 P · Ts 순.)

### 3-5. ★ ANOVA · MLR 인쇄값 (표 1 b–d · 2 b–d) + 우리 대조

| 모형 | 인쇄 ANOVA (유의 인자 · p) | 인쇄 MLR (R²) | 우리 대조 [우리 산술] |
|---|---|---|---|
| 단순 Q1st (1b) | Xs 0.015 · **P 0.001** · Ts 0.027 · 오차 df 4 | Q1st = −60.2 + 123.8Xs + 0.3P + 10.3Ts (0.945) | 계수 재현 (P 기울기 0.3317) · R² 는 보정 전 **0.969** — 0.945 = **자유도 보정 R²** (다른 모형은 보정 전 값) |
| 단순 Rs1st (1c) | Xs 0.019 · **P 5.8 × 10⁻⁶** · Ts 0.001 · XsP 0.006 | 3614.3 + 385.8Xs − 6.8P − 126.6Ts − 6.6XsP (0.999) | 재현 (상호작용 = 중심화) |
| 단순 Rct1st (1d) | Xs 0.009 · Ts 0.052 · XsTs 0.214 | 67.0 + 1246.7Xs − 71.0Ts − 381.8XsTs (0.892) | ⛔ **표 2 (d) 와 글자 단위로 같다** — 표 1a Rct 로 다시 하면 SS_Xs 6,728 · SST 19,019 (인쇄 124,341.7 · 197,731.3 은 표 2a 값) · 실제 인자 = Xs · P · XsP · Ts (그림 4c 와 일치) |
| 코팅 Q1st (2b) | **Xs 0.003** · Ts 0.035 · XsTs 0.058 · (P 0.275 · PTs 0.197 도 모형에 남김) · 오차 df 2 | 114.2 − 458.0Xs + 3.8 × 10⁻²P + 11.9Ts − 91.1XsTs + 4.9 × 10⁻²PTs (0.996) | 재현 — 단 상호작용을 **(Xs − 0.2)(Ts − 1.5) · (P − 270)(Ts − 1.5)** 로 읽을 때만 본문 최댓값 125.4 가 나온다 (그냥 곱으로 읽으면 133.2) |
| 코팅 Rs1st (2c) | P 0.0007 · Ts 0.0015 · PTs 0.0033 | 1905.3 − 1.8P − 132.9Ts − 1.2PTs (0.979) | 재현 |
| 코팅 Rct1st (2d) | **Xs 0.009** · Ts 0.052 · XsTs 0.214 | 67.0 + 1246.7Xs − 71.0Ts − 381.8XsTs (0.892) | 재현 |

- 감도 순서 (그림 4 · 본문 p.10): 단순 Q1st **P > Xs > Ts** (모두 양) · 단순 Rs1st **P** 가 지배 (음) · 코팅 Q1st **Xs > Ts > Xs·Ts** (Xs 음) · 코팅 Rct1st **Xs** 가 지배 (양).  막대 높이 벡터 판독 = 표 (a) 로 다시 계산한 값과 ±0.002 안 (19 막대 · digitized.csv).
- 반응표면 최댓값 (본문 p.11): 단순 **122.1 mAh/g** (Xs 0.3 · P 360 · Ts 2.5 — MLR 예측, 실측 119.8) · 코팅 **125.4 mAh/g** (Xs 0.1 · 360 · 2.5 — 예측, 실측 129.9) · 그때 Rs/Rct = 935.9/56.4 vs **830.4/31.8 Ω**.  충방전 곡선은 "no significant difference" (Fig S3).

### 3-6. ★ 사이클 결과 — 표 3 (단순 혼합) · 표 4 (코팅 · Xs 0.1 만) [인쇄]

| No. | Xs | P | Ts | 단순 Qr | 단순 ΔRs (Ω) | 단순 ΔRct (Ω) | 코팅 Qr | 코팅 ΔRs (Ω) | 코팅 ΔRct (Ω) |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.1 | 180 | 0.5 | 58 % | 851.9 | 66.2 | **92 %** | 650.5 | 97.7 |
| 2 | 0.1 | 180 | 2.5 | 70 % | 704.9 | 29.4 | 66 % | 455.6 | 48.9 |
| 3 | 0.1 | 360 | 0.5 | 50 % | 547.0 | 92.8 | 91 % | 395.8 | 136.4 |
| 4 | 0.1 | 360 | 2.5 | 64 % | 266.2 | 65.1 | 80 % | 155.2 | 25.8 |
| 5 | 0.3 | 180 | 0.5 | 71 % | 623.9 | 95.3 | — | — | — |
| 6 | 0.3 | 180 | 2.5 | 77 % | 1249.8 | 70.3 | — | — | — |
| 7 | 0.3 | 360 | 0.5 | 81 % | 409.4 | 67.5 | — | — | — |
| 8 | 0.3 | 360 | 2.5 | **90 %** | 247.9 | 44.0 | — | — | — |

- 코팅 Xs 0.3 은 "< 11.0 mAh/g … extremely low capacity" 라 분석에서 뺐다 (p.11).
- 단순 혼합 MLR (표 3): Qr = 0.4 + 9.5 × 10⁻¹Xs + 1.3 × 10⁻⁴P + 5.0 × 10⁻²Ts + 5.0 × 10⁻³XsP − 1.5 × 10⁻¹XsTs + 7.1 × 10⁻⁵PTs (**R² 0.999 — 계수 7 개 · 점 8 개 · 오차 df 1**) · ΔRs = 1347.5 − 2.7P (**R² 0.623** — 원문도 "not a good fit") · ΔRct = 78.6 + 29.5Xs + 1.1 × 10⁻²P − 14.1Ts − 1.6XsP + 20.1XsTs + 1.5 × 10⁻²PTs (R² 0.998).  감도 (그림 8): Qr **Xs > Ts > XsP > XsTs > P** · ΔRs = P (−0.79) · ΔRct = XsP (−0.70) · Ts (−0.68) [판독 = 다시 계산과 일치].
- 코팅 ANOVA (표 4): Qr 의 P p 0.551 · Ts p 0.253 (둘 다 유의 아님) · ΔRs P 0.052 · Ts 0.067 (dominant trend) · ΔRct 둘 다 유의 아님.
- 최고 유지율: 단순 **90 %** (Xs 0.3 · 360 · 2.5) ↔ 코팅 **92 %** (Xs 0.1 · **180 · 0.5**) (p.12).

### 3-7. 기전 서술 (SEM 단면 · 정성) (p.11–13 · Fig 5 · 6)

| 관찰 | 원문 해석 | 표지 · 쪽 |
|---|---|---|
| 단순 Xs 0.3: 180 MPa 에서 LPS 영역의 미세공극 (흰 화살표) → 360 MPa 에서 거의 사라짐 | LPS 의 소성 변형 · 합체 → **Rs ↓ → Q1st ↑** (단순 혼합의 P 지배) | [인쇄] p.11 · Fig 5c · d |
| 코팅: Xs 가 오르면 NCM–NCM 접촉이 줄어든다 (단순 혼합은 Xs 0.3 에서도 NCM–NCM 접촉이 남음 — Fig 5d 화살표) | 개별 NCM 전 표면이 LPS 로 덮여 **전자 전도 경로 (= NCM–NCM 접촉) 감소 → Rct ↑ → Q1st ↓** | [인쇄] p.11 · Fig 6 |
| 최고 셀끼리 Rs · Rct 모두 코팅이 낮다 | LPS 의 고른 분포 · LPS 안 균열 적음 · 고체–고체 계면 잘 형성 (코어–셸 덕) | [인쇄] p.11 |
| 단순 Xs 0.1 에서 NCM 안 균열 · Xs 0.3 에서 억제 | 높은 Xs 가 NCM 에 걸리는 압축 응력을 완화 → **Qr ↑** | [인쇄] p.12 |
| 코팅 Xs 0.1 은 균열이 억제되고 LPS 가 양극 층에 고르게 분포 | 코어–셸이 압축 응력을 완화 · 끊김 없는 Li 이온 경로 → 낮은 P · Ts 에서도 Qr 높음 | [인쇄] p.12–13 |

---

## 4. ★ 방법 — 측정 사슬 · 입자 처리

### 4-1. 측정 사슬
NCM (LiNbO₃) + 액상 진탕 LPS → 막자 예비 혼합 → 건식 충격 블렌딩 (13,000 rpm · 5 min · Ar) → 코팅 분말 (SEM/EDX · 입도 · UV-vis 순조성 5.6 wt%) → 자유 LPS 막자 추가로 Xs 0.1 / 0.3 ↔ 막자 30 min 단순 혼합 → LPS 80 mg (40 MPa) + 양극 10 mg (P 180/360 MPa · 300 s) + Li–In (90 MPa) → 볼트 4 개 Ts 0.5/2.5 N·m → 25 °C 조정 4 회 + 50 회 · EIS (1 · 50 회 뒤 · SOC 100 %) → Rs · Rct → ANOVA · MLR · 반응표면 · 표준화 계수 → 단면 SEM 으로 해석.

### 4-2. ★ 입자 처리 (우리 축 언어로)
- **실험**: LPS 는 충격으로 **진짜 형상 소성 · 합체** (낱알 → 껍질) · 압축에서도 소성 · 합체 (미세공극 소멸) · NCM 은 압축 중 **균열** (단순 Xs 0.1) — 높은 Xs 나 껍질이 완충.
- **우리 대응**: DEM 은 강체 구 + 겹침 (E_SE 1.35 GPa 연화 · 형상 소성 없음 · AM 파괴는 접촉 판정만) · MPM 은 SE 형상 소성 (σ_y 0.30 GPa) 이 있으나 AM 은 얼린 골격 · 둘 다 **껍질 (코어–셸) 을 표현하지 않는다** — 코팅 상태는 우리 모델에서 입력 (믹서 DEM 의 코팅 대리 = AM–AM 점착 제거 등) 이고 껍질의 전자 차폐는 원리적으로 안 나온다 [추정 — §7].

### 4-3. 기법 미니 용어집
- **DOE (design of experiment) · 2³ 완전요인**: 세 인자 × 두 수준의 모든 조합 8 개를 돌리는 설계 — 주효과와 상호작용을 직교로 가른다.
- **ANOVA · F 값 · p 값**: 각 인자가 만든 제곱합 (SS) 을 오차 평균제곱으로 나눈 F 로 유의성을 본다.  반복이 없으면 오차를 상호작용 항에서 빌린다 (이 논문 = F < 2 항을 오차로 합침).
- **MLR (multiple linear regression)**: 유의 인자로 Y = b₀ + Σbᵢxᵢ + Σbᵢⱼxᵢxⱼ 를 최소제곱으로 맞춘 식.
- **표준화 편회귀계수 b\***: bᵢ·σ(xᵢ)/σ(Y) — 단위가 다른 인자들의 영향 크기를 같은 눈금으로 비교 (식 18).
- **반응표면 (response surface)**: MLR 식을 두 인자 평면 위에 그린 면 (그림 7 · 9).
- **자유도 보정 R² (adjusted R²)**: 1 − (1 − R²)(n − 1)/(n − k − 1) — 항이 많을 때 R² 부풀림을 줄인 값.
- **Rs / Rct (이 논문의 정의)**: 주파수 창으로 나눈 저항 — Rs = > 100 kHz (SE 벌크 · 분리막 포함) · Rct = 100 k–100 Hz (양극 고체–고체 계면 전하이동).
- **dry impact-blending (건식 충격 블렌딩)**: 고속 회전자 · 날 · 순환관에서 입자를 충돌시켜 작은 게스트 (LPS) 를 큰 호스트 (NCM) 위에 소성 · 합체시켜 입히는 무용매 공정.

---

## 5. Figure set ★ (크롭 17 장 = `litdb/figures/kawaguchi2023_doe_electrode_fabrication_dry_coated_ncm_lps/`)

| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1 | NCM (a) · LPS (b) SEM (축척 1 µm) — NCM 2 차 입자 · LPS 얇은 판 조각 덩어리 | 크기비 ≈12.7 (개수 중앙 4.70/0.37) — 우리 PC/SE 9 · SC/SE 4 보다 크다 |
| 2 | 건식 충격 블렌딩 장치 (정면 · 측면 · 7 부품 표지) | 코팅 장치 실체 — 우리 드럼 믹서와 다른 장치 |
| 3 | (a) 단순 혼합 · (b) 코팅 분말 SEM + Mn · S EDX 지도 (c) 개수 입도 4 곡선 (원 NCM · 원 LPS · 코팅 분말 · 씻은 NCM) | ★ 코팅 분말에 자유 LPS 미분 없음 · NCM 파손 없음 |
| 4 | 표준화 편회귀계수 6 패널 (단순 a–c · 코팅 d–f: Q1st · Rs1st · Rct1st) | ★ 지배 인자가 뒤집힌다 (P ↔ Xs) · (c) 가 표 1d 오류를 드러냄 (§10-1) |
| 5 | 단순 혼합 단면 SEM 2 × 2 (Xs 0.1 / 0.3 × P 180 / 360) · 흰 화살표 = 미세공극 (c) · NCM–NCM 접촉 (d) | 압축압이 SE 영역 공극을 없애는 그림 · 고 SE 에서도 NCM–NCM 접촉이 남는다 |
| 6 | 코팅 단면 SEM 2 × 2 | ★ Xs 0.3 에서 NCM 이 LPS 기지 안 섬처럼 떨어짐 = 무탄소 전자 경로 붕괴의 그림 |
| 7 | Q1st 반응표면 (P × Ts) — 단순 (a–c) · 코팅 (d–f) × Xs 0.1 / 0.2 / 0.3 | 코팅 Xs 0.1 이 전 영역 높고 Xs 0.3 은 바닥 (0–20) · ⚠ Xs 0.2 = 보간 |
| 8 | 단순 혼합 사이클 감도 (Qr · ΔRs · ΔRct) | Xs 가 유지율을 지배 (균열 억제 해석) |
| 9 | 단순 혼합 Qr 반응표면 × Xs 0.1 / 0.2 / 0.3 | Xs 0.3 · 고압 · 고토크에서 85–90 % |
| S1 | 셀 모식 (볼트 · 너트 M6 × 4 · 절연 시트 · 금속판 · 층 구성) | 체결 구조 — 토크가 압력으로 바뀌는 경로 |
| S2 | 전형 Nyquist (Rs · Rct · 음극 확산 주파수 창) | Rs 가 분리막을 포함하는 정의라는 근거 |
| S3 | 최고 셀 둘의 첫 충방전 곡선 (mAh/g-NCM) | 코팅 No.4 ≈130 · 단순 No.8 ≈120 방전 끝 [판독 — 육안] |
| 표 1 | 단순 혼합 DOE 8 셀 + ANOVA/MLR (Q1st · Rs1st · Rct1st) | ★ 원자료 (단 (d) 는 복사 오류) |
| 표 2 | 코팅 DOE 8 셀 + ANOVA/MLR | ★ 원자료 |
| 표 3 | 단순 혼합 사이클 (Qr · ΔRs · ΔRct) + ANOVA/MLR | (c) · (d) Total 행 오류 (§10-1) |
| 표 4 | 코팅 사이클 (Xs 0.1 · 4 셀) + ANOVA | 유의 인자 없음 |
| 표 S1 | 충방전 조건 (조정 · 시험) | 시험 조건 원문 |

## 6. Post-processing ★
- **원문이 한 것**: SEM/EDX 정성 · 개수 입도 · UV-vis 순조성 · EIS 주파수 창 분할 (등가회로 맞춤 방식 미기재) · Excel FDIST 로 p 값 · MLR · 반응표면 · 표준화 계수.
- **안 한 것**: 반복 · 오차 막대 · 피복률 · 두께 · 공극률 · σ_ion · σ_e · 분리막 저항 분리 · 체결 토크 → 압력 환산 · 단면 정량 (균열 · 접촉 수).
- **우리 후처리 (이 카드)**: ① 모든 MLR 을 표 (a) 값으로 다시 맞춤 (상호작용 중심화) — 계수 · 최댓값 재현, 표 1d 복사 · 표 3c · 3d Total 오류 · 표 1b 의 보정 R² 를 찾음 ② 그림 4 · 8 막대를 **PDF 벡터 경로**에서 읽어 (눈금 표시로 보정) 다시 계산한 표준화 계수와 대조 (27 막대 · ±0.002 · Qr 은 정수 % 반올림 때문에 ±0.01) ③ 같은 조건 짝의 비 (§0 ⑤) · Xs 0.1 안 인자 효과 (§0 ⑥) ④ 껍질 몫 · 적재 · 질량당 전류 · 체결압 · 분리막 저항 어림.

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (⚠ 정본 브랜치에서는 값 자리표시 상태 — 우리 수치는 메인 리포 `docs/data/ps45_r45_network_g2_20261007/README.md` · `docs/data/ps45_sigmae_factor_off_20261013/README.md` · CLAUDE.md 의 ps45 줄을 병기해 적는다)

### 7-1. 비교표

| 항목 | 이 논문 | 우리 ps45 (NCM 81.6 : LPSCl 18.4 wt% · 300 MPa · 무탄소) | 같음 / 다름 · 왜 |
|---|---|---|---|
| 비교 설계 | **같은 Xs (총 SE) 에서** 코팅 (껍질 몫 53 / 14 %) vs 막자 혼합 · 압축압 · 체결 토크까지 2³ | 논지: 같은 총 SE 에서 선코팅 vs 비코팅 (믹서 DEM → 압축 → 접촉망) · 압축 300 MPa 하나 | 설계 축 같음 + 이 논문은 **공정 두 인자 (P · Ts) 를 더 가졌다** |
| SE · 크기 | Li₃PS₄ · 0.37 µm · 0.091 mS/cm | LPSCl · 1 µm · σ₀ 1.5 mS/cm (보고 기준) | 재료 · 크기 다름 — 절대값 대조 불가 |
| CAM | NCM111 단봉 · 4.70 µm (개수 중앙) | NCM811 PC 9 · SC 4 µm 바이모달 | SC 와 크기 띠 비슷 |
| 조성 (고체 부피) | Xs 0.1 ≈ **22 vol%** · Xs 0.3 ≈ **52 vol%** [추정 — 밀도 NCM 4.7 · LPS 1.9 가정] | ≈35 vol% (`PS45E-01` 계열 산술) | 우리 조성은 두 수준 사이 |
| 도전재 | **없음** (전자 = NCM 만) | **없음** (σ_e = AM 망 · 인자 끔 0.375–0.467 mS/cm @ σ_AM 4.1) | ★ 같은 무탄소 조건 — 이 논문의 전자 붕괴가 우리 V1 에 직접 걸린다 (§7-3) |
| 압력 | 180 / 360 MPa (+ 체결 ≈21–106 MPa [추정]) | 300 MPa (판 속도 0.01 mm/s) | 우리 압력은 고압 쪽 — 이 논문에서 코팅 이점이 작아지는 쪽 |
| 수송 지표 | Rs (분리막 포함 · Ω) · Rct · 용량 | σ_ion Hertz 0.0587–0.0893 · Tabor 0.103–0.162 mS/cm · 수송 tortuosity Hertz 7.24–5.03 · Tabor 4.12–2.78 · φ_SE 0.284–0.299 · 공극률 union 16.5–20.6 % | ⛔ 같은 양이 하나도 없다 — 방향 · 순서만 |
| SE 거동 | 압축 중 소성 · 합체 (미세공극 소멸 — SEM) | DEM: 강체 구 겹침 (연화 E) · MPM: J2 소성 (σ_y 0.30 GPa) | 공극 소멸 기전 = MPM 쪽 |
| AM 파쇄 | 단순 Xs 0.1 에서 균열 (SEM 정성) | DEM: 접촉 판정 (Auerbach) · 조각 없음 | 균열 몫을 못 그린다 |
| 껍질 | LPS 껍질 (≈0.1 µm [추정]) — NCM–NCM 전자 접촉을 막음 | 없음 (코팅 대리 = 점착 행렬만) | ⛔ 껍질의 전자 차폐는 우리 모델 밖 |

### 7-2. 이종기술 논지 (`docs/hetero_thesis.md` 비준 블록 2026-10-05) 와의 관계
- **P1 (비코팅은 오래 섞어도 SE–SE 응집이 남는다)**: 시험하지 않는다 — 혼합 시간 열이 없다 (단순 혼합 = 막자 30 min 하나).  단순 혼합 분말의 S 지도 (그림 3a) 에 LPS 덩어리가 따로 보이는 정성 정황뿐.
- **P2 (코팅하면 응집이 사라진다)**: 코팅 분말 입도에 LPS 봉우리가 없다 (그림 3c — 자유 LPS 미분 없음) — Nakamura 2020 과 같은 정황.  단 이 논문의 양극은 **그 뒤에 자유 LPS 를 막자로 다시 넣는다** (Xs 0.1 에서 LPS 의 47 % · Xs 0.3 에서 86 % [우리 산술]) — "코팅 전극" 도 자유 SE 를 품는다.
- **P3 (혼합 상태 → 압축 뒤 SE 경로)**: 방향이 같은 정황 — 같은 Xs 0.1 · 180 MPa 에서 Rs ×0.63 · Q1st ×3.2–3.6 [우리 산술] · 저자 서술 *"the LPS was more uniformly distributed in the cathode layer … uninterruptedly connected Li-ion conduction paths"* [인쇄 p.13].  ⚠ 단 Rs 에 분리막이 섞여 있고 (§10-3) σ_ion 이 없다 — 수치 근거로 쓰지 않는다.
- **"하지 않는 말" (계면 면적 · 보호막)**: 원문은 Rct 감소를 "well-constructed solid–solid interface" 로 설명하지만, **같은 조건 짝에서는 코팅의 Rct 가 4 중 3 에서 더 높다** (×2.09 · ×1.15 · ×1.30 · ×0.77 [우리 산술]) — 계면 면적 축으로 이 논문을 빌리지 않는다 (논지와도 맞다).

### 7-3. ★ "같은 총 SE 에서 코팅 상태" 실험 (`docs/mixer_paper_pipeline_draft_20261013.md` V1 코팅 상태 · V2 혼합 시간 · V3 SE 함량) 에 주는 것
1. **코팅 이점은 압축압에 걸린다**: Xs 0.1 에서 Q1st 비 ×3.2–3.6 (180 MPa) → ×1.09–1.21 (360 MPa) · Rs 비 ×0.63 → ×0.88–1.06 [우리 산술] — 300 MPa 의 V1 (모델 · 대칭셀 계획 `docs/symmetric_cell_ionic_plan_20261013.md`) 에서는 **차이가 작게 나올 수 있다** → 효과를 보려면 낮은 압력 한 수준을 더 두거나, 작게 나올 것을 결과 전에 적어 둔다 [추정].  (같은 그룹 Nakamura 2020 은 360 MPa 에서도 DC σ_ion +58 % 를 냈다 — 이 논문의 Rs 에는 분리막이 섞여 차이가 묽어졌을 수 있다 [추정].)
2. **무탄소 코팅은 SE 가 많으면 전자 경로가 끊긴다**: 코팅 Xs 0.3 은 1.8–11.0 mAh/g (단순 혼합 42.1–119.8) — 껍질 + 많은 자유 LPS 가 NCM 을 섬으로 만든다 (그림 6c · d).  우리 ps45 (≈35 vol% SE) 와 대칭셀 계획도 **무탄소**라 V1 코팅 팔에서는 **σ_e (TLM 의 R_ele) 를 반드시 같이** 재야 한다 — 우리 DEM 에는 껍질이 없어 이 붕괴를 예측하지 못한다 (상한 대리 = 코팅 쌍의 AM–AM 접촉 전도를 끊은 σ_e — 미실행 [추정]).
3. **"같은 총 SE" ≠ "같은 껍질 몫"**: 이 설계에서 껍질 몫은 Xs 와 함께 53 → 14 % 로 움직인다 [우리 산술] — V1 의 "코팅 SE 몫 2 수준" 은 **총 SE 를 고정하고 껍질 몫을 따로** 움직여야 교락이 없다 (그 설계는 `kim2024_optimal_cathode_composite_mechanical_mixing_se_coverage` 가 했다 — 껍질 몫에 최적점).
4. **순조성 먼저**: 투입 10 → 순 5.6 wt% (56 % 잔존) — 같은 장치 · 같은 조건의 Nakamura 2020 (15 → 13.1) · 모델 물질 Kawaguchi 2017 (≤ 10 wt% 손실 없음) 보다 손실이 크다 · 원인 미기재.  ⇒ 코팅 분말의 순조성을 재고 (UV-vis · ICP) 나서 자유 SE 를 맞춘다.
5. **체결압을 고정 · 보고**: Xs 0.1 에서 코팅 셀은 체결 토크에 더 민감 (Q1st +42.1 vs +22.3 mAh/g [우리 산술]) — 대칭셀 · 반쪽셀의 스택 압력을 결과 전에 고정하고 적는다.
6. **SE 가 모자랄 때 이점이 크다 (V3)**: Xs 0.1 (≈22 vol% [추정]) 에서 코팅 이점 최대 — 파이프라인 V3 의 *"같은 SE 로 경로를 먼저 까는 효과는 SE 가 모자랄 때 클 수 있다 [추정]"* 과 같은 방향 (`kim2023_…` 의 "SE 가 적을수록 이득 증가" 와도 같다).  단 무탄소에서는 반대쪽 끝 (SE 많음) 에 전자 붕괴가 있어 **창이 양쪽에서 닫힌다**.

### 7-4. frame[5] — 어느 반쪽을 가졌나
- **가진 것**: 공정 (코팅 · 압축압 · 체결 토크 · SE 비) → 셀 성능 (용량 · 유지율 · Rs · Rct) 의 **통계 지도** (16 셀) + 단면 SEM 정성.
- **없는 것**: 미세구조 정량 (공극률 · 접촉 · 피복) · σ_ion/σ_e · 반복 · 모델.  ⇒ 이 논문은 우리 DEM (접촉망 수송) · MPM (소성 공극 소멸) 어느 쪽의 **보정 앵커도 되지 못한다** (frame [4] — 같은 양이 없다) · 실험 설계 · 해석의 **방향 지도**로만 쓴다.

---

## 8. ★★ 우리 연구에 주는 insight (번호마다: 논문이 보인 것 → 우리에게 뜻 → 할 일)

**8-1. 코팅은 "압축압 의존" 을 "체결압 의존" 으로 바꾼다.**
- 논문: Xs 0.1 안에서 P 180 → 360 MPa 의 Q1st 이득이 단순 +60.7 · 코팅 +10.8 mAh/g, Ts 0.5 → 2.5 N·m 이득은 단순 +22.3 · 코팅 +42.1 mAh/g [우리 산술 — 표 1a · 2a].
- 뜻: 코팅이 압축 전에 SE 경로를 깔아 압축압의 몫을 대신하지만, 껍질로 NCM–NCM 전자 접촉이 줄어 운전 중 스택 압력에 기대게 된다 [추정].
- 할 일: V1 실험에서 압축압 두 수준 (300 + 낮은 한 수준) · 체결압 고정을 결과 전에 등록 (§7-3-1 · 5).

**8-2. 무탄소 코팅 전극의 상한 SE — 전자 붕괴.**
- 논문: 코팅 Xs 0.3 = 1.8–11.0 mAh/g · SEM 에서 NCM 섬 (그림 6c · d) · Rct 165–524 Ω.
- 뜻: 우리 무탄소 ps45 · 대칭셀 계획에서 코팅 팔의 σ_e 가 무너질 수 있고, 그 몫은 우리 접촉망이 못 낸다 (껍질 없음).
- 할 일: 대칭셀 TLM 의 R_ele 를 코팅 · 비코팅 둘 다 보고 · 모델 쪽은 "코팅 쌍의 AM–AM 전도 끊음" σ_e 를 하한 대리로 계산 (제안 · 미등록).

**8-3. 같은 조건 짝으로 읽어라 — "최고 셀끼리" 비교는 다른 Xs 를 섞는다.**
- 논문: 본문 Rs/Rct 비교 (935.9/56.4 vs 830.4/31.8) 는 Xs 0.3 (단순) ↔ Xs 0.1 (코팅).  같은 Xs 0.1 짝에서는 코팅 Rct 가 4 중 3 에서 높다 · Qr 도 4 중 3 (본문 "same fabrication conditions" 에서 더 높다는 서술은 No.2 에서 틀림 — 66 vs 70 %).
- 할 일: 우리 보고 · 덱에 이 논문을 쓸 때 **같은 Xs · P · Ts 짝의 비**를 쓴다 (§0 ⑤).

**8-4. DOE 는 싸지만 반복이 없으면 p 값이 얇다.**
- 논문: 16 셀 · 반복 0 · 오차 = 상호작용 합침 · Qr 모형 계수 7 / 점 8.
- 할 일: 우리 실험 계획 (파이프라인 Q4) 에서 2³ 를 쓴다면 중심점 반복이나 핵심 대비 (코팅 vs 비코팅) 반복 n ≥ 3 을 넣는다 [추정].

**8-5. Rs 는 분리막을 포함한다 — 복합 양극 이온 저항은 TLM 으로.**
- 논문: Rs = > 100 kHz 저항 · LPS 분리막 80 mg 도 같은 P 로 눌림 · [추정 — 밀도 1.9 g/cm³ 가정 · 완전 치밀] 분리막만 ≈0.53 mm · 0.91 × 10⁻⁴ S/cm 로 **≥ 0.7 kΩ** = Rs1st (791–2,520 Ω) 와 같은 자릿수.
- 할 일: 대칭셀 계획대로 EIS + TLM (R_ion · R_ele 분리) — Rs 하나로 복합 양극 σ_ion 을 말하지 않는다.

## 9. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "In a 2³ factorial study of carbon-free NCM111/Li₃PS₄ half-cells, the initial capacity of mortar-mixed cathodes was governed by compaction pressure (180 → 360 MPa), whereas that of dry-coated core–shell NCM@Li₃PS₄ cathodes was governed by the solid-electrolyte fraction: at 30 wt% electrolyte the coated cathodes delivered only 1.8–11.0 mAh g⁻¹ because the electrolyte shells removed NCM–NCM electronic contacts (Kawaguchi et al., *Adv. Powder Technol.* 2023)."
- 국문: *"같은 SE 비 (10 wt%) 에서 건식 코팅 양극의 첫 용량은 180 MPa 압축에서 막자 혼합의 3.2–3.6 배, 360 MPa 에서 1.09–1.21 배였다 — 코팅의 이점은 압축압이 낮을수록 크다 (Kawaguchi 2023 표 1–2 로 우리가 계산 · 조건마다 셀 1 개)."*

## 10. 주의/한계 (over-claim 방지 · 원문 비판)
1. **표 오류 셋 [우리 산술]**: ① **표 1 (d) = 표 2 (d)** (SS · F · p · MLR 이 글자 단위로 같다) — 표 1a Rct 로 다시 하면 SS_Xs 6,728 · SST 19,019 · 실제 인자 Xs · P · Xs·P · Ts 이고, **그림 4c 막대 (+0.594 · −0.475 · −0.443 · −0.386 벡터 판독) 가 이 재계산 (+0.595 · −0.475 · −0.444 · −0.386) 과 맞는다** ⇒ 분석은 맞게 했고 표만 잘못 옮겼다.  ② 표 3 (c) Total 708,385.6 ≠ P + Error = 770,448.8 (R² 0.623 은 770,449 로 계산된 값 · 표 3a 재계산 SST 770,530) ③ 표 3 (d) Total 6,049.9 ≠ 행 합 3,427.5 (R² 0.998 = 1 − 7.2/3,427.5 · 재계산 SST 3,421).
2. **MLR 표기**: 상호작용 항은 **평균 중심화** ((Xs − 0.2)(P − 270) 등) 로 읽어야 인쇄 계수와 본문 최댓값이 나온다 — 그냥 곱으로 읽으면 코팅 최댓값이 125.4 대신 133.2 [우리 산술] · 원문은 중심화를 적지 않았다.  R² 는 표 1b 만 자유도 보정값 (0.945 · 보정 전 0.969) 이고 나머지는 보정 전 값.
3. **Rs = 분리막 + 복합 양극**: 원문은 Rs 를 "resistance of solid electrolyte" 라고만 적고 그 감소를 양극 안 미세공극 소멸로 설명하는데, 분리막 (80 mg · 40 MPa 예비 압축 뒤 **같은 P 로 다시 압축**) 도 P 에 따라 치밀해진다 — P 효과의 일부는 분리막일 수 있다 [추정] · 분리막 크기 어림 ≥ 0.7 kΩ (§8-5, 가정 포함).
4. **반복 없음 · 오차 빌림**: 조건마다 1 셀 · F < 2 항을 오차로 합침 · 표 3b Qr 모형 오차 df 1 · 표 2b 오차 df 2 — p 값은 반복 분산이 아니라 모형 밖 상호작용 크기에 기댄다.
5. **Xs 와 율속의 교락**: 면적 전류 고정 (0.13 mA/cm²) · 양극 질량 고정 (10 mg) 이라 Xs 0.3 의 NCM 질량당 전류가 1.29 배 [우리 산술] — Xs 효과에 율 효과가 섞인다 (원문 언급 없음).
6. **Xs 0.2 반응표면**: 측정 없는 선형 보간 — 코팅은 0.1 과 0.3 사이에서 붕괴하므로 Xs 0.2 의 38–70 mAh/g (MLR 값 [우리 산술]) 는 근거가 없다.
7. **"같은 조건에서 코팅 Qr 이 더 높다" (p.12)**: 4 짝 중 No.2 (66 vs 70 %) 는 반대.
8. **자유 LPS 추가량 표기**: "4.4 wt% · 24.4 wt%" 는 Xs − 5.6 의 차 — 실제 추가 질량분율 (4.66 · 25.85 wt%) 과 다르다 [우리 산술] · 추가 막자 시간 미기재.
9. **표기 · 오타**: 그림 4 캡션 "(e)" 자리에 "©" · 본문 "Fig. 4 and (f)" ((e) 빠짐) · 표 1 의 "(c)" 표지가 "©" · p.7 "subscripts ©, j, k" (i 자리) · 식 7–12 · p.7 의 "Tc" (= Ts) · "Mpa" · "Fig. 3S" (= Fig. S3) · "1th" · 참고문헌 [20] 쪽 "2–6".
10. **전이 한계**: NCM111 단봉 (LiNbO₃) · Li₃PS₄ (LPSCl 아님 · 0.091 mS/cm) · 무탄소 · 반쪽셀 · 25 °C · 50 회 · 한 장치 · 한 코팅 조건 · 순조성 5.6 wt% 한 배치.  공극률 · σ 가 없어 우리 모델 (DEM · MPM) 의 보정 · 검증 앵커가 되지 못한다 (frame [4]).

## 11. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)
| 번호 | 서지 (원문 목록 그대로) | 왜 · 카드 |
|---|---|---|
| 10 | F. Strauss, T. Bartsch, L. De Biasi, A.Y. Kim, J. Janek, P. Hartmann, T. Brezesinski, Impact of cathode material particle size on the capacity of bulk-type all-solid-state batteries, ACS Energy Lett. 3 (2018) 992–996 | 카드 없음 — CAM 입경 효과 (우리 PC/SC) |
| 11 | C. Park, S. Lee, K. Kim, M. Kim, S. Choi, D. Shin, Electrochemical properties of composite cathode using bimodal sized electrolyte for all-solid-state batteries, J. Electrochem. Soc. 166 (2019) A5318–A5322 | 카드 없음 — 이 논문 DOE 수준 범위의 근거 · SE 바이모달 |
| 19 | A. Sakuda, A. Hayashi, T. Ohtomo, S. Hama, M. Tatsumisago, All-solid-state lithium secondary batteries using LiCoO2 particles with pulsed laser deposition coatings of Li2S-P2S5 solid electrolytes, J. Power Sources 196 (2011) 6735–6741 | 카드 없음 — PLD SE 코팅 · DOE 수준 범위의 근거 |
| 20 | A. Sakuda, A. Hayashi, M. Tatsumisago, Sulfide solid electrolyte with favorable mechanical property for all-solid-state lithium battery, Sci. Rep. 3 (2013) 2–6 | 정본 카드 `sakuda2013_sulfide_mechanical_property` — 상온 가압 소결 (원문 쪽 표기 "2–6" 그대로) |
| 24 | H. Nakamura, T. Kawaguchi, T. Masuyama, A. Sakuda, T. Saito, K. Kuratani, S. Ohsaki, S. Watano, Dry coating of active material particles with sulfide solid electrolytes for an all-solid-state lithium battery, J. Power Sources 448 (2020) 227579 | 정본 카드 `nakamura2020_dry_coating_ncm_li3ps4_core_shell` |
| 25 | E. Hayakawa, H. Nakamura, S. Ohsaki, S. Watano, Characterization of solid-electrolyte/active-material composite particles with different surface morphologies for all-solid-state batteries, Adv. Powder Technol. 33 (3) (2022) 103470 | 카드 없음 — 같은 그룹 · 껍질 형태별 비교 (V1 의 "불연속 · 연속" 축) |
| 26 | E. Hayakawa, H. Nakamura, S. Ohsaki, S. Watano, Design of active-material/solid-electrolyte composite particles with conductive additives for all-solid-state lithium-ion batteries, J. Power Sources 555 (2023) 232379 | 카드 없음 — ★ 코팅 입자의 전자 경로 문제 (이 논문 Xs 0.3 붕괴) 를 도전재로 푸는 같은 그룹 후속 · 비교 = `kim2025_conductive_agent_se_coating_cathode` |
| 27 | T. Kawaguchi, H. Nakamura, S. Watano, Dry coating of electrode particle with model particle of sulfide solid electrolytes for all-solid-state secondary battery, Powder Technol. 323 (2018) 581–587 | 카드 없음 — 모델 물질 선정 · 기전 원전 |
| 28 | T. Kawaguchi, H. Nakamura, S. Watano, Parametric study of dry coating process of electrode particle with model material of sulfide solid electrolytes for all-solid-state battery, Powder Technol. 305 (2017) 241–249 | 정본 카드 `kawaguchi2017_dry_coating_parametric_na2so4_model_se` |
| 29 | S. Ohsaki, T. Yano, A. Hatada, H. Nakamura, S. Watano, Size control of sulfide-based solid electrolyte particles through liquid-phase synthesis, Powder Technol. 387 (2021) 415–420 | 카드 없음 — 이 논문 LPS 의 합성 |
| 30 | N.H.H. Phuc, K. Morikawa, T. Mitsuhiro, H. Muto, A. Matsuda, Synthesis of plate-like Li3PS4 solid electrolyte via liquid-phase shaking for all-solid-state lithium batteries, Ionics 23 (2017) 2061–2067 | 카드 없음 — 판 모양 LPS (그림 1b) |
| 31 | A. Sakuda, T. Takeuchi, H. Kobayashi, Electrode morphology in all-solid-state lithium secondary batteries consisting of LiNi1/3Co1/3Mn1/3O2 and Li2S-P2S5 solid electrolytes, Solid State Ion. 285 (2016) 112–117 | 카드 없음 — 반쪽셀 제작 절차의 출처 |
| 32 | A. Sakuda, H. Kitaura, A. Hayashi, K. Tadanaga, M. Tatsumisago, Modification of interface between LiCoO2 electrode and Li2S–P2S5 solid electrolyte using Li2O–SiO2 glassy layers, J. Electrochem. Soc. 156 (2009) A27 | 카드 없음 — Rs · Rct 주파수 창 귀속의 출처 |

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-10-13)
- 본문 15 쪽 + SI 3 쪽 텍스트 층 전수 · 저자 · 소속 · 날짜 · 연구비 · DOI = p.1 · p.14 · SI p.1.  LPS 전도도 "0.91 × 10⁻⁴ S/cm" 와 MLR 의 부호 (텍스트 층에서 "×" · "−" 가 빠짐) 는 **쪽 렌더 (표 1–3 크롭)** 로 확인.
- 표 1–4 · 표 S1 = 칸마다 렌더와 대조.  설계 순서 (No.1–8) 는 표 4a 와 각 표의 인자 칸으로 확인 · 모든 ANOVA SS 와 MLR 계수를 표 (a) 값으로 다시 계산 (표 1b · 1c · 2b · 2c · 2d · 3b · 3d 는 반올림 안에서 재현 · 1d · 3c · 3d 의 오류는 §10-1).
- 그림 4 · 8 = 벡터 그림 (막대 · 눈금 = 경로, 글자 = 윤곽) — 막대 27 개를 경로 좌표로 읽어 다시 계산과 대조 (digitized.csv) · 그림 4 (c) · (f) 가로축 표지 밑 잔 표시는 원문 그대로 (확대 렌더로 확인).
- 그림 · 표 17 장 = 캡션 17 개 (본문 그림 9 · 표 4 · SI 그림 3 · 표 1) 전부 렌더로 열람.  자동 추출의 표 1–3 은 쪽 전체 (294 dpi) 라 표 영역으로, SI 그림 S1 (좌우 표지 잘림) · S2 (그림 아래 1/3 만) · S3 (여백) 은 다시 잘랐다 · 래스터 그림 7 장은 원 해상도 (300 dpi) 경계로 · `figures.json` 의 `recrop` · `manual_crop` · `caption_note`.
- 정본 litdb 중복 확인: `git ls-tree` 로 `litdb/papers/` 전수 + DOI · 제목 낱말 · 참고문헌 DOI 들 (`apt.2022.103470` · `jpowsour.2022.232379`) 로 `litdb/` grep — 이 논문 카드 없음 · 같은 그룹 카드 = `nakamura2020_…` · `kawaguchi2017_…` (같은 날 묶음).

## 🔗 관련 카드
- 같은 그룹: `nakamura2020_dry_coating_ncm_li3ps4_core_shell` · `kawaguchi2017_dry_coating_parametric_na2so4_model_se`.
- 같은 총 SE 에서 코팅 상태 · 껍질 몫: `kim2024_optimal_cathode_composite_mechanical_mixing_se_coverage` (껍질 몫 최적) · `kim2023_mechanofusion_ncm811_lpscl_core_shell_intimate_contact` (메카노퓨전 · SE 가 적을수록 이득) · `lee2026_lpscl_coating_thickness_ncm811` (껍질 두께 ↔ σ_e) · `kim2025_conductive_agent_se_coating_cathode` (코팅에 도전재).
- 건식 공정 · 압축 · 미세구조: `frankenberg2025_milling_dry_processed_sulfide_cathode_microstructure` · `hippauf2019_dry_film_ptfe_sulfide_cathode_sheet` · `lee2024_shear_force_dry_process_cathode_coverage` · `lee2026_unveiling_ptfe_dry_electrode_digital_twin` (PTFE 건식 양극 디지털 트윈) · `lee2026_mechanical_halogen_argyrodite_drycoating` (1저자 공저 — RAM 건식 코팅의 기계 물성 축).
- 수송 해석: `otani2023_ionic_conductivity_path_resistance_separation_model` · `asano2017_ncm111_li3ps4_composite_electronic_ionic_conductivity` · `so2022_dem_compaction_coated_particles_assb`.
- SE 기계 물성: `sakuda2013_sulfide_mechanical_property`.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
