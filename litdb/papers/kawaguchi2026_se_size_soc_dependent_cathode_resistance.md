<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 사용자가 특히 원한 항목. 깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md ·
     형식 이웃 = schlautmann2023_se_particle_size_composite_transport.md (같은 크기 묶음 · 이 논문 ref [31]) · otani2023_ionic_conductivity_path_resistance_separation_model.md (같은 LIBTEC · ref [32]).
     파일 판정: 사용자가 준 두 파일 이름이 모두 "Sup" 이지만 내용으로 갈랐다 —
       `…Resistance_Analysis_2.pdf` (8 쪽) = **본문** (학술지 머리 · 초록 · Figure 1–6 · Experimental · 참고문헌 [1]–[45] · "Batteries & Supercaps 2026, 9, e202500337 (n of 8)").
       `…Resistance_Analysis_1.pdf` (12 쪽) = **SI** ("Supporting Information" 머리 · Table S1 · Figure S1–S9 · MS Word 인쇄본).
     쪽 표기: 본문 "p.n" = 인쇄 쪽 "(n of 8)" = PDF n 쪽.  SI "SI p.n" = SI PDF n 쪽 (인쇄 쪽 번호 없음).
     값 표지: [인쇄] = 본문 · SI 문장 · 표 · 그림 안 글자로 적힌 값 · [판독] = 그림에서 읽은 값 (200 dpi 크롭 · 필요한 곳 400 dpi 확대 · TREND 전용) ·
     [우리 산술] = 인쇄값으로 우리가 다시 한 계산 · [추정] = 논문이 말하지 않은 우리 해석 · [미확인] = 본문 8 쪽 + SI 12 쪽 전수에 없음.
     원문 전수: 본문 텍스트 층 전부 + SI 텍스트 층 전부 정독 · SI 는 그림이 타일 래스터라 모든 쪽을 렌더 이미지로 열람 · 크롭 16 장 (본문 6 + SI 그림 9 + SI 표 1) 전부 열람. -->
# 황화물 (LPSCl) 복합양극의 **SE 입도 효과는 충전 상태 (SOC) 에 따라 뒤집힌다** — D50 ≈6 µm vs <1 µm Li₆PS₅Cl 계 아지로다이트 (NCM523 · VGCF) 반쪽셀의 EIS · 양극 대칭셀 EIS · GITT 1 % SOC 계단 저항 분해: SOC > 20 % 에서는 큰 SE (이온전도 우세), SOC < 20 % 에서는 작은 SE (AM–SE 계면 · 전하이동) 가 저항이 낮고, 충전 율속은 큰 SE · 방전 율속은 작은 SE 가 낫다 — Kawaguchi · Fukiya · Ehara · Ichikawa · Yoshimura · Iso · Sasaki · Horisawa · Shimada · Kuzuhara · Miyuki (LIBTEC · Batteries & Supercaps 2026)

> slug `kawaguchi2026_se_size_soc_dependent_cathode_resistance` · DOI `10.1002/batt.202500337` · type `exp (resistance analysis — cathode half-cell EIS · cathode symmetric-cell EIS (SE/SE split-cell) · GITT 1 % SOC steps mapped to EIS time constants R1/R2/R3 · charge/discharge rate tests · composite σ_ion/σ_e table; no simulation)` · PDF `83dadec4-5._Sup_Interface_Engineering_in_Sulfide_Based_All_Solid_State_Batteries_Insights_from_Resistance_Analysis_2.pdf` (**본문** 8 쪽) + `2dc11202-5._Sup_Interface_Engineering_in_Sulfide_Based_All_Solid_State_Batteries_Insights_from_Resistance_Analysis_1.pdf` (**SI** 12 쪽) · digested `2026-10-30` · status ✅
> topic: size_effect (SE 입도 효과)
> 묶음 역할: **최적 입도의 SOC 의존 · 저항 분해**
>
> **저자 · 소속 (p.1 · SI p.1)**: **Shunsuke Kawaguchi**\*[+] · Naomi Fukiya · Kei Ehara · Tomoyuki Ichikawa · Manami Yoshimura · Eishi Iso · Yuji Sasaki · Yuhei Horisawa · Masaki Shimada · Minoru Kuzuhara · Takuhiro Miyuki — Consortium of Lithium Ion Battery Technology and Evaluation Research Center (**LIBTEC**), Ikeda, Osaka · [+] 현 소속 Nissan Motor Co., Ltd. · 교신 kawaguchi.shunsuke@libtec.or.jp · *Batteries & Supercaps* **2026**, 9, e202500337 (8 쪽) · 원고 접수 2025-05-03 · 수정 2025-07-24 · "Version of record online:" 칸 비어 있음 · © 2025 Wiley-VCH GmbH · 연구비 NEDO **SOLiD-Next (JPNP23005)** · 이해충돌 없음 · 자료 = 요청 시 [인쇄 p.1 · p.7–8].
> **정본 litdb 이웃 (링크만)**: [`otani2023_ionic_conductivity_path_resistance_separation_model`](otani2023_ionic_conductivity_path_resistance_separation_model.md) (같은 LIBTEC · 공저자 Miyuki · 이 논문 ref [32]) · [`schlautmann2023_se_particle_size_composite_transport`](schlautmann2023_se_particle_size_composite_transport.md) (ref [31] · SE 4–40 µm 의 "균형 전달") · [`shi2019_high_am_loading_particle_size_assb`](shi2019_high_am_loading_particle_size_assb.md) (ref [19] · [30] · λ) · [`kaiser2018_ion_transport_limitations_assb_sulfide_electrodes`](kaiser2018_ion_transport_limitations_assb_sulfide_electrodes.md) (ref [26] · 복합체 σ 측정법) · [`aminchiang2016_nmc_electronic_ionic_transport_vs_li`](aminchiang2016_nmc_electronic_ionic_transport_vs_li.md) (ref [27] · NMC 전자 σ).

---

## 0. 결론 먼저 — 우리 질문 (50 kg 4차년도 SE 입도 보고 · p5 손익분기 · p7 "최적 입도" 금지 · p3 접촉) 에 대한 답

| Q | 판정 (한 줄) | 근거 |
|---|---|---|
| **Q1 작은 SE 가 늘 이기나** | **아니다 — SOC 에 따라 뒤집힌다.** 전하이동 저항 R2: SOC 30–100 % 는 큰 SE (L_SE) 가 낮고 (예: SOC 50 % L ≈14 · S ≈19 Ω) · SOC 20 % 에서 같고 (≈37 · ≈38) · SOC 5–10 % 는 작은 SE (S_SE) 가 낮다 (SOC 5 % L ≈123 · S ≈87 Ω).  저자 판정: *"performance levels of S_SE and L_SE are reversed at an SOC of ≈20%"* | [인쇄 p.4–5] · `Fig. 5c–d` [판독] |
| **Q2 복합체 유효 σ** | **σ_ion: 큰 SE 3.5 × 10⁻⁴ > 작은 SE 1.5 × 10⁻⁴ S cm⁻¹ (2.33 배)** · σ_e: 5.2 × 10⁻⁵ ≈ 5.8 × 10⁻⁵ S cm⁻¹ (차이 없음).  저자: 복합체 이온 σ 는 SE 자체 σ 에 크게 걸린다 [26] · 전자 σ 는 AM 이 정한다 [27, 28].  ⚠ **순수 SE 펠릿 σ 는 측정법만 적고 값이 없다** [미확인] | [인쇄 SI Table S1 · p.2] |
| **Q3 율속** | 충전 율속 = 큰 SE 우세 (2 C 충전 ≈145 vs ≈138 mAh g⁻¹, 유지율 ≈85 vs ≈81 %) · 방전 율속 = 작은 SE 우세 (2 C 방전 ≈113 vs ≈103, 유지율 ≈67 vs ≈63.5 %) · 0.1 C 방전도 작은 SE 가 큼 (≈170 vs ≈163) | [인쇄 p.5] · `Fig. 6` [판독] |
| **Q4 기전 (저자)** | 높은 SOC = 이온전도 지배 → 큰 SE 유리 · 낮은 SOC (양극 저항이 크게 오르는 구간) = AM–SE 의 고른 접촉 · 전도 경로가 결정적 → 작은 SE 유리.  큰 SE 는 사이클 중 부피 변화에 따른 재배열에서 AM 과 밀착을 잃기 쉽다는 **가설** (분석 필요라고 스스로 적음) · 계면 용량 (접촉 지표) 은 첫 사이클 전 S/L ≈**0.85** → 뒤 ≈**1.30** | [인쇄 p.5] · `Fig. S9` [판독] |
| **Q5 우리에게** | ① **"최적 입도" 는 한 값이 아니다** — 우리 `KG50B-02` (*"최적 입도"* 금지) 의 직접 문헌 근거 ② p5: 작은 SE (<1 µm) 복합체의 σ_ion 이 큰 SE (≈6 µm) 의 **1/2.33** — 구조 이득이 재료 손해를 못 넘긴 실측 사례일 수 있으나 **펠릿 σ 가 없어 갈라낼 수 없다** ③ p3: 계면 용량으로 본 접촉이 **새 전극에서는 작은 SE 쪽이 오히려 작다** (0.85 배) — *"접촉이 늘면 피복이 는다"* 의 반례 후보 ④ 우리 망 (SOC 무관 오믹 수송) 은 R2 · R3 (SOC 의존 동역학 · 확산) 을 **못 낸다** — 이 논문의 핵심 (SOC 역전) 은 우리 범위 밖 | §8 |

⇒ **한 문장**: 같은 회사 (Mitsui Mining & Smelting) 의 LPSCl 두 입도만 바꾼 NCM523 복합양극에서, 저항을 SOC 1 % 단위로 R1 (접촉 · 셀) · R2 (전하이동) · R3 (확산) 로 나눠 보니 **SOC 20 % 근처에서 큰 SE ↔ 작은 SE 의 우열이 뒤집힌다** — *"작은 SE 가 좋다"* 도 *"큰 SE 가 좋다"* 도 SOC 를 빼면 틀린 문장.  단 **두 입도 · 한 조성 · 반복 · 면적 · 공극 · 순수 SE σ 미기재 · 성형압 서술 불일치** 를 한정어로 붙인다.

---

## 1. 한 줄 요약
D50 ≈6 µm (L_SE) 과 <1 µm (S_SE) LPSCl 로 만든 NCM523 : SE : VGCF = 75 : 22 : 3 wt% 양극 반쪽셀 (In–Li 대극) 에서 0.1 C 곡선은 거의 같지만 저 SOC 에서 갈라지고, 2 C 에서는 방전 곡선이 서로 교차한다.  양극 대칭셀 (SE/SE 경계에서 갈라지는 셀을 같은 SOC 끼리 짝지음) EIS 의 시정수 (R1 460 kHz · R2 100 Hz · R3 0.2 mHz) 로 GITT (0.5 C × 72 s = 1 % SOC · 5000 s 휴지) 저항을 R1 · R2 · R3 로 나누면, R1 은 두 SE 가 같고, R2 · R3 는 SOC > 20 % 에서 L_SE 가 · SOC < 20 % 에서 S_SE 가 낮다.  충전 율속은 L_SE, 방전 율속은 S_SE 가 이기는 것이 이 저항 분해와 맞다.  저자는 *"최적 SE 입도는 SOC 에 따라 다르다"* 고 결론하고 크고 작은 SE 혼합을 다음 단계로 든다.

## 2. 메타 / 동기 / 질문

| 저자 | 저널 / 년 | DOI | 소재 (CAM / SE) | 연구유형 |
|---|---|---|---|---|
| Kawaguchi\* · … · Miyuki (LIBTEC · 현 Nissan) | *Batteries & Supercaps* **9**, e202500337 (2026) | 10.1002/batt.202500337 | **NCM523** (LiNi₀.₅Co₀.₂Mn₀.₃O₂ · 공급사 · 입경 [미확인]) + **LPSCl** (Li₇₋ₓPS₆₋ₓClₓ, Mitsui Mining & Smelting, D50 ≈6 · <1 µm) + **VGCF** (Resonac) = 75 : 22 : 3 wt% | 실험 (EIS · 대칭셀 EIS · GITT · 율속) |

- **동기 (p.1–2)**: 황화물 SE 전극은 성형압과 성능이 맞바뀐다 (낮은 압력에서 고체–고체 계면이 덜 생긴다 [18]) · SE 입도는 AM 과의 접점 수 · 전도 경로를 바꾼다 [19, 20] · 입도 분포도 중요하다 [21] → 고체–고체 계면 형성의 설계 지침이 없다.
- **질문**: SE 입도가 양극층 저항의 **어느 성분**을 **어느 SOC** 에서 바꾸는가 · 그것이 실제 율속 시험과 맞는가.
- **방법의 주장**: 흔한 DC (GITT) + AC (대칭셀 EIS) 를 엮으면 SOC 별 저항 성분을 가를 수 있다 — *"simple analysis method"* [인쇄 p.2].

## 3. 핵심 수치 ★

### 3-1. 재료 · 조성 · 셀 (p.6–7 · SI p.2–3)
| 항목 | 값 | 표지 |
|---|---|---|
| CAM | NCM523 · 입경 · 형상 · 코팅 [미확인] (SI Table S1 단면 SEM 에 구형 이차입자로 보임) | [인쇄 · 판독] |
| SE | Mitsui Mining & Smelting 아지로다이트 두 종 · 평균 입경 **ca. 6 µm** (L_SE) · **ca. <1 µm** (S_SE) · Table S1 표기 = D50 | [인쇄 p.6 · SI Table S1] |
| SE 제조 · 입도 제어 방법 | [미확인] (공급사 시료) | — |
| 도전재 | VGCF (Resonac Holdings) | [인쇄 p.6] |
| 조성 | **NCM : SE : VGCF = 75 : 22 : 3 wt%** · 막자 ca. 15 min | [인쇄 p.6 · SI Table S1] |
| 순수 SE 측정법 | 100 mg → 100 MPa 1 min → **600 MPa** 1 min 펠릿 → SUS 박/SE/SUS 봉입 → 볼트로 **200 MPa** → EIS (최대 7 MHz, VSP-300) | [인쇄 p.6] |
| **순수 SE σ 값** | **[미확인]** — 측정법은 있으나 값이 본문 · SI 어디에도 없다 | — |
| 반쪽셀 (성능) | LPSCl 100 mg → 100 MPa 1 min → 양극 복합체 **22 mg** → 100 MPa 1 min → **900 MPa** 1 min → In–Li 대극 · **1C = 3 mA cm⁻²** | [인쇄 p.6–7] |
| ⚠ 성형압 서술 | 결과 절: *"forming pressure and the stack pressure … were set to 600 and 200 MPa"* ↔ 실험 절: 양극–SE 적층 **900 MPa** · 200 MPa 는 순수 SE 측정 셀에만 | [인쇄 p.2 ↔ p.6] |
| 대칭셀용 반쪽셀 | LPSCl 100 mg 100 MPa → 양극 22 mg 100 MPa → 900 MPa → LPSCl 100 mg 100 MPa → 900 MPa → In–Li 100 MPa (`Fig. S1` Step 1–5) · Step 2 의 강한 성형으로 SE 면이 매끈해져 SE/SE 경계가 붙지 않음 → 시험 뒤 그 경계에서 분리 (Step 6) · 2 층 SE 셀도 성능 차 없음 (`Fig. S2`) | [인쇄 p.7 · SI p.3–4] |
| 대칭셀 조립 | 시험 뒤 OCV 8 h → Ar 글로브박스 (이슬점 *"ca. 80 °C"* 로 인쇄 — −80 °C 오기로 보임 [추정] · O₂ < 1 ppm) 에서 해체 → **같은 SOC 로 평형한 양극 둘**을 SE 층째 맞대 대칭셀 → EIS 10 mHz–1 MHz · 10 mV | [인쇄 p.7–8] |
| 순환 · EIS | OCV 8 h → 0.1 C/0.1 C CC-CV **3.0–4.35 V vs Li/Li⁺** 3 사이클 → 0.1 C 로 SOC 50 % 까지 충전 → 4 h 휴지 → EIS 10 mHz–1 MHz · 10 mV | [인쇄 p.7] |
| 면적 · 로딩 · 두께 · 공극 | **[미확인]** (모두 미기재 → Ω 를 Ω·cm² 로 못 바꾼다) | — |
| 반복 수 · 오차 | [미확인] (*"GITT tests were performed on the cells that showed no abnormalities"* 만) | [인쇄 p.7] |

### 3-2. 복합체 유효 전도도 — SI `Table S1` 전문 [인쇄 SI p.2]
| | L_SE (≈6 µm) | S_SE (<1 µm) | 비 (우리 산술) |
|---|---|---|---|
| 조성 | 75 : 22 : 3 wt% | 같음 | — |
| σ_ion,eff (S cm⁻¹) | **3.5 × 10⁻⁴** | **1.5 × 10⁻⁴** | L/S = **2.33** |
| σ_e,eff (S cm⁻¹) | **5.2 × 10⁻⁵** | **5.8 × 10⁻⁵** | S/L = 1.12 |
| σ_ion/σ_e | ≈6.7 | ≈2.6 | [우리 산술] |
| 측정법 | *"previously described methods [25, 26]"* (Shiroma 2016 · Kaiser 2018) — 셀 · 두께 · 압력 · 온도 [미확인] | | |
- 단면 SEM (Table S1, 1 µm 막대): L_SE 쪽은 넓은 SE 덩어리 영역 · S_SE 쪽은 NCM 사이를 고운 SE 가 메운 모습 [판독 · 정량 없음].

### 3-3. 저항 성분 정의 (`Fig. S6` · p.4)
| 성분 | 대칭셀 EIS 시정수 [인쇄] | 저자 귀속 [인쇄] | GITT 에서 대응 |
|---|---|---|---|
| R1 | **460 kHz (2 × 10⁻⁶ s)** | 접촉 저항 + 셀 자체 · *"can be used to determine the electronic conductivity of the electrode"* | 매우 고주파 → *"strongly influenced by the measurement accuracy of the equipment"* [40] |
| R2 | **100 Hz (0.01 s)** | AM–SE 전하이동 저항 R_ct | |
| R3 | **0.2 mHz (5000 s)** | AM 안 Li 확산 저항 | GITT 5000 s 휴지 뒤 저항 = 이론상 R3 |

### 3-4. GITT 저항 분해 (`Fig. 5`) [판독 — 막대 높이 · ±2 Ω]
| SOC (%) | 5 | 10 | 20 | 30 | 50 | 80 | 100 |
|---|---|---|---|---|---|---|---|
| R1 L / S (Ω) | ≈24 / 24 | ≈24 / 23 | ≈24 / 24 | ≈24 / 25 | ≈24 / 25 | ≈24 / 24 | ≈22 / 22 |
| **R2 L / S (Ω)** | **≈123 / 87** | **≈74 / 57** | ≈37 / 38 | ≈15 / 19 | ≈14 / 19 | ≈18 / 27 | ≈12 / 21 |
| R3 L / S (Ω) | ≈103 / 89 | ≈76 / 69 | ≈34 / 33 | ≈12 / 13 | ≈12 / 12 | ≈14 / 16 | ≈13 / 17 |
| R2 비 L/S [우리 산술] | 1.41 | 1.30 | ≈0.97 | 0.79 | 0.74 | 0.67 | 0.57 |
- `Fig. 5a` 총 저항 (전위 축): 최소 ≈3.8 V (= SOC ≈50 %, 저자 *"good agreement with previous results [38, 39]"*) — L ≈50 · S ≈56 Ω · 3.9–4.35 V 에서 L ≈48–56 · S ≈60–68 Ω · 3.68 V (저 SOC) 에서 L ≈330 · S ≈250 Ω [판독].
- `Fig. S7`: GITT 총 저항 ↔ 대칭셀 EIS 의 5000 s 표지점 Z′ (L ≈38 · S ≈58 Ω, SOC 50 % 로 보임) — 저자 *"approximately consistent"* [인쇄 SI p.9 + 판독].

### 3-5. 율속 · 곡선 (`Fig. 1` · `Fig. 6` · `Fig. S2` · `S3` · `S8`) [판독]
| 지표 | L_SE | S_SE | 비고 |
|---|---|---|---|
| 첫 충전 / 방전 (0.1 C, 3.0–4.35 V, `Fig. S2`) | ≈206 / ≈162 mAh g⁻¹ (CE ≈79 %) | ≈208 / ≈170 (CE ≈82 %) | CE = 우리 산술 |
| 0.1 C · 2 C 방전 (`Fig. 1`, 하한 ≈2.5 V 로 보임) | ≈162 · ≈98 | ≈168 · ≈112 | 2 C 곡선이 ≈80 mAh g⁻¹ 근처에서 교차 (그 전엔 L 이 높음) |
| 충전 율속 (`Fig. 6a–b`) 0.1 · 0.5 · 1 · 2 C | ≈171 · 163 · 155 · 145 (유지 100 · 95.7 · 90.5 · 85 %) | ≈171 · 160 · 150 · 138 (100 · 93.7 · 87.6 · 81 %) | **L 우세** |
| 방전 율속 (`Fig. 6c–d`) 0.1 · 0.5 · 1 · 2 C | ≈163 · 149 · 130 · 103 (100 · 91.8 · 79.8 · 63.5 %) | ≈170 · 159 · 140 · 113 (100 · 93.7 · 82.7 · 67 %) | **S 우세** |
| 재조립 반쪽셀 (`Fig. S3`) | 충전 ≈165–170 · 방전 ≈157 — 해체 전 · 후 곡선 겹침 | (어느 SE 셀인지 미표기) | 대칭셀 해체가 양극을 망가뜨리지 않는다는 대조 |

### 3-6. EIS 판독 (`Fig. 2` 반쪽셀 · `Fig. 3` 대칭셀) [판독]
| 셀 · SOC | L_SE | S_SE | 저자 문장 |
|---|---|---|---|
| 반쪽셀 SOC 50 % | 고주파 절편 ≈8 Ω · 작은 호 · 마지막 점 Z′ ≈35 Ω | ≈9 Ω · 마지막 점 Z′ ≈41 Ω | *"L_SE has a lower resistance"* |
| 반쪽셀 SOC 0 % | ≈12 Ω 에서 시작 · 마지막 점 Z′ ≈268 Ω (−Z″ ≈125) | **≈75–80 Ω 에서 시작** · 마지막 점 Z′ ≈247 Ω (−Z″ ≈79) | *"S_SE has a lower total resistance"* · In–Li 저항이 섞여 분류가 어렵다고 스스로 적음 |
| 대칭셀 SOC 50 % | ≈9.5 Ω · 호 끝 ≈20 Ω | ≈12 Ω · 호 끝 ≈26 Ω | |
| 대칭셀 SOC 0 % | ≈45° 직선 · 마지막 점 Z′ ≈450 Ω | 같은 꼴 · ≈330 Ω | |
- ⚠ SOC 0 % 반쪽셀의 S_SE 고주파 절편이 L_SE 보다 ≈65 Ω 크다 — 본문은 설명하지 않는다 [판독 · §9-5].

### 3-7. 계면 용량 (접촉 지표) — `Fig. S9` [판독]
| | 첫 사이클 전 | 첫 사이클 뒤 |
|---|---|---|
| L_SE (정규화 기준) | 1.00 | 1.00 |
| S_SE / L_SE | **≈0.85** | **≈1.30** |
- SOC 0 % 대칭셀 EIS 에서 추정 · 방법 = 저자 자신의 이전 논문 (Kawaguchi 2025, J. Colloid Interface Sci. 696, 137878) · **각 조건에서 L_SE 값으로 나눈 상대값** → 절대 변화 (S 가 늘었는지 L 이 줄었는지) 는 모른다 [인쇄 SI p.11 + 추정].

### 3-8. GITT 조건 (p.7 · SI p.6–7)
- 0.1 C CC-CV 충전 → **0.5 C × 72 s 방전 + 5000 s 휴지** 반복 · 한 계단 = 용량 기준 1 % SOC (100 계단 = 7200 s 방전) · *"relaxation 때문에 실제 계단당 SOC 는 1 % 보다 작다"* · 전위 요동이 멈출 때까지 [인쇄].
- `Fig. S4`: 한 계단 — 4.31 V 에서 펄스 중 ≈4.21 V 까지 강하 → 5000 s 동안 ≈4.29 V 로 회복 [판독].  `Fig. S5`: 펄스 중 전위가 t^½ 에 선형 (**R² = 0.9998**) → 전극층 안이 정상 상태 [인쇄 SI p.7].
- `Fig. 4`: 전체 ≈600,000 s · 영역 I (0–200,000 s, ≈4.3 → 3.85 V) · II (200,000–400,000 s, ≈3.85 → 3.71 V) · III (400,000–600,000 s) — 영역 III 에서 펄스 끝 전위가 하한까지 떨어지기 시작하는 시각 ≈480,000 s (L) · ≈490,000 s (S) [판독].

## 4. 방법 ★

### 4-1. 저항 분해 사슬
① 반쪽셀 EIS (SOC 50 · 0 %) — 대극 (In–Li) 저항이 섞여 분류 곤란 → ② **양극 대칭셀**: 두 층 SE 로 만든 반쪽셀을 시험 뒤 SE/SE 경계에서 갈라 같은 SOC 양극끼리 맞댐 → 대극 없는 양극만의 EIS → 호가 또렷해 R1 · R2 · R3 의 시정수를 정함 (`Fig. S6`) → ③ GITT (1 % 계단) 의 시간 영역 응답을 그 시정수 위치에서 읽어 SOC 별 R1 · R2 · R3 로 분류 (`Fig. 5b–d`) → ④ GITT 총 저항 ↔ 대칭셀 EIS 대조 (`Fig. S7`) → ⑤ 율속 시험과 대조 (`Fig. 6`).
- GITT 저항 = 인가 전류 대비 전위 변화 (*"calculated using the applied current values in response to potential fluctuations"*) [인쇄 SI p.9].  각 시정수에서 어떻게 값을 뽑았는지 (보간 · 샘플링 간격) 는 [미확인] — R1 의 2 µs 를 GITT 시간 자료에서 직접 읽는 것은 일반 장비 샘플링으로는 어렵다 [추정].
- 접촉 지표: 대칭셀 EIS 의 AM–SE 계면 용량 (상대값) (`Fig. S9`).

### 4-2. 입자 처리 ★ · 시뮬레이션 · frame[5]
- **시뮬레이션 없음.**  입자 크기는 공급사 표기 D50 두 값뿐 · PSD 곡선 · 비표면적 · 공극 · 미세구조 정량 없음 · 단면 SEM 두 장 (정성).
- frame[5]: 이 논문은 **전기화학 (SOC 의존 저항 · 율속)** 을 잰다 — 우리 DEM 접촉망이 주는 **오믹 수송 (σ_ion · σ_e)** 과는 `Table S1` 한 줄에서만 겹치고, R2 (전하이동) · R3 (고체 확산) 은 우리 모델의 **바깥** (STEP4 전기화학 영역).  MPM 형상 · 공극 쪽 정보도 없다.

### 4-3. 기법 미니 용어집
- **GITT (galvanostatic intermittent titration technique)** — 짧은 정전류 펄스 + 긴 휴지 반복.  펄스 직후 · 휴지 중 전위 변화로 저항 · 확산을 SOC 별로 잰다.  여기 = 0.5 C × 72 s (1 % SOC) + 5000 s.
- **양극 대칭셀** — 같은 양극 둘을 SE 로 맞댄 셀.  대극 (In–Li) 의 저항이 빠져 양극 성분만 보인다.  이 논문은 2 층 SE 로 만든 반쪽셀을 SE/SE 경계에서 갈라 같은 SOC 양극을 짝지어 만들었다.
- **시정수 (time constant)** — 저항 × 용량 (τ = RC), 그 성분이 응답하는 시간 척도.  여기 R1 2 µs · R2 10 ms · R3 5000 s.
- **R_ct (전하이동 저항)** — AM–SE 계면에서 Li⁺ 가 넘나드는 반응의 저항.  NCM 은 저 SOC (방전 끝, Li 가 거의 찬 상태) 에서 R_ct · 고체 확산 저항이 크게 오른다 (본문 [38, 39]).
- **계면 용량 (interfacial capacitance)** — AM–SE 계면의 이중층 용량 ∝ 전기화학적으로 닿은 계면 면적 → 접촉 지표 (저자 방법).
- **CC-CV** — 정전류 뒤 정전압 유지 충전.

## 5. 결과 — 절별 (그림 실독 포함)

### 5.1 복합체 전도도 — 큰 SE 가 이온 σ 높고 전자 σ 는 같다 (`Table S1`)
본문: *"L_SE exhibited higher ionic conductivity values, attributed to the significant dependence of the ionic conductivity of the cathode layer on the ionic conductivity of the SE [26]. However, no significant difference was observed in the electronic conductivities … depends on the electronic conductivity of the AM [27, 28]"* [인쇄 p.2].  ⚠ VGCF 3 wt% 가 든 전극의 전자 σ 를 *"AM 이 정한다"* 고 쓴 것은 논문 안에서 설명되지 않는다 [§9-6].

### 5.2 방전 곡선 — 0.1 C 는 거의 같고 2 C 에서 교차 (`Fig. 1`)
0.1 C 곡선은 저 SOC 에서만 갈라짐 · L_SE 의 방전 용량이 작다 (선행 연구 [30–32] 와 같은 경향) · 그러나 과전압은 방전 도중 **역전** — 어느 지점까지는 L_SE 과전압이 낮다 (이온전도 영향) · 2 C 에서 곡선 교차 [인쇄 p.2–3].

### 5.3 반쪽셀 · 대칭셀 EIS — SOC 에 따라 서열이 바뀐다 (`Fig. 2` · `Fig. 3` · `Fig. S3`)
반쪽셀: SOC 50 % L_SE 저항 낮음 · SOC 0 % S_SE 총저항 낮음 · *"LIBs based on liquid electrolytes do not exhibit such a behavior even if the electrolyte is changed. This is a unique characteristic specific to ASSBs [33]"* [인쇄 p.3].  대칭셀: 두 SOC 모두에서 *"No change in the resistance sequence"* (성분 순서) · 양극층 저항이 입도로 바뀌고 성분이 SOC 로 바뀜 · 해체 셀을 다시 조립해도 성능 그대로 (`Fig. S3`) [인쇄 p.3].

### 5.4 GITT 세 영역 (`Fig. 4`)
영역 I: L_SE 의 IR 강하 · 과전압이 작다 (액체 LIB 와 같은 전해질 이온전도 효과 [38, 39]) · 영역 II: 양극 저항이 SOC 와 함께 줄어 차이가 작다 · 영역 III: 저 SOC 에서 양극 저항 급증 → 하한 도달.  본문 문장 *"L_SE exhibits a lower potential drop at each discharge step, and the discharge progresses more gradually. Therefore, in the low-SOC region, the S_SE cathode layer has a lower resistance"* [인쇄 p.4] — ⚠ 앞뒤가 맞지 않고, 그림에서는 L_SE (빨강) 펄스가 **더 일찍 · 더 깊게** 떨어진다 [판독] → 이 문장의 L/S 가 뒤바뀐 것으로 보인다 [추정 · §9-4].

### 5.5 저항 분해 (`Fig. 5`)
R1 은 SOC · 입도 무관 (≈22–25 Ω) · R2 는 SOC > 20 % 에서 L_SE 가 낮다 (이온전도 영향) · SOC < 20 % 에서 양극 저항이 급증하며 L_SE 가 더 큼 → *"in the region with the highest resistance of the cathode layer, S_SE is the superior cathode material"* · R3 도 같은 경향 · 저자 *"the difference … is more pronounced in this region (R3)"* — ⚠ 판독상 SOC 5 % 차는 R2 ≈36 Ω > R3 ≈14 Ω [판독 · §9-4] · 확산을 통한 Li 전도의 중요성 [41] · *"performance levels of S_SE and L_SE are reversed at an SOC of ≈20%"* [인쇄 p.4–5].

### 5.6 율속 · 접촉 (`Fig. 6` · `Fig. S8` · `Fig. S9`)
충전 율속 = L_SE 우세 → *"except in the extremely low SOC region, ionic conductivity plays a dominant role"* · 방전 율속 = S_SE 우세 · 0.1 C 에서도 L_SE 방전 용량이 작음 → *"AM becomes isolated in L_SE at low SOC"* [30–32] [인쇄 p.5].  사이클 중 AM–SE 접촉 손실 선행 보고 · 실제로 두 SE 의 *"electrochemical contact states … reverse as a function of the SOC during cycling (Figure S9)"* · 큰 SE 는 부피 변화에 따른 재배열에서 밀착 유지가 어려울 수 있다 (분석 필요) [인쇄 p.5].

### 5.7 결론 · 제안 (p.5–6, 인쇄)
- 이온 σ 와 AM–SE 계면 접촉을 **동시에** 최적화해야 전 SOC 에서 좋다 [43, 44] · 큰 · 작은 SE 혼합이 가능한 전략이나 미세구조 안 **선택적 배치**가 어렵다 [45 = So 2022] · PSD · 절대 입도 조정과 양극 기계 물성과의 상관이 다음 과제.
- *"a clear solution for optimizing the SE particle size for each SOC region cannot be provided at this time"* — 그래도 *"distinct design parameters may be more effective at different SOC levels"* [인쇄 p.6].

## 6. Figure set ★ (크롭 16 장 = `figures/kawaguchi2026_se_size_soc_dependent_cathode_resistance/`)
| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1 | 0.1 C · 2 C 방전 곡선 (S_SE 검정 · L_SE 빨강) | 2 C 교차 = SOC 의존 우열의 첫 증거 |
| 2 | 반쪽셀 Nyquist (a) SOC 50 % (0–50 Ω) (b) SOC 0 % (0–500 Ω) | SOC 0 % S_SE 고주파 절편 이상 (§9-5) |
| 3 | 양극 대칭셀 Nyquist (a) SOC 50 % (b) SOC 0 % | 대극 없는 양극 저항 |
| 4 | GITT 방전 전체 + 영역 I · II · III 확대 | 저 SOC 에서 하한 도달 |
| 5 ★ | (a) 총 저항 vs 전위 (b) R1 (c) R2 (d) R3 vs SOC 5–100 % | ★ **SOC 20 % 역전의 정량 원판** |
| 6 | 충전 (a 용량 · b 유지율) · 방전 (c · d) 율속 0.1–2 C | 충전 L · 방전 S 우세 |
| 표 S1 ★ | 단면 SEM 두 장 · 조성 · D50 · **복합체 σ_ion · σ_e** | p5 의 σ_ion 비 2.33 |
| S1 | 대칭셀용 반쪽셀 6 단계 (압력 · SE/SE 경계 · 분리) | 방법 |
| S2 | Step 2–3 ↔ 2–4 셀의 첫 충방전 (S_SE · L_SE) | 2 층 SE 무영향 · 첫 CE |
| S3 | 재조립 반쪽셀 해체 전 · 후 충방전 | 해체 무손상 대조 |
| S4 | GITT 한 계단 (0.5 C × 72 s · 5000 s) | 조건 |
| S5 | 펄스 중 전위 vs t^½ (R² 0.9998) | 정상 상태 근거 |
| S6 | 대칭셀 EIS 위 R1 (460 kHz) · R2 (100 Hz) · R3 (0.2 mHz) 표지 | ★ 저항 분류 기준 |
| S7 | GITT 총 저항 (전위 축) ↔ 대칭셀 EIS (5000 s 표지) | 두 방법 대조 |
| S8 | 율속 곡선 (충전 a · b · 방전 c · d, 0.1–2 C) | Fig. 6 원곡선 |
| S9 ★ | 계면 용량 (L_SE 로 정규화) — 첫 사이클 전 · 후 | ★ p3 접촉 반례 후보 |

## 7. Post-processing ★
- **무엇을**: EIS Nyquist (맞춤 회로 · 소프트웨어 [미확인]) · 대칭셀 시정수로 GITT 응답을 세 시간대에서 읽어 SOC 별 막대그림 · 율속 = 용량 · 0.1 C 대비 유지율 · 계면 용량 = 대칭셀 EIS 에서 추정 후 L_SE 로 정규화.
- **도구**: VSP-300 (BioLogic) · 맞춤 · 그림 도구 [미확인].
- **안 한 것**: 면적 정규화 (Ω·cm²) · 공극 · 두께 · PSD · 순수 SE σ 값 · 반복 셀 수 · 오차막대 · 회로 맞춤 값 · 액체 대조 실험 · 혼합 SE.
- **우리 후처리 (이 카드)**: Table S1 비 · R2 비 · 그림 판독 (막대 ±2 Ω · 곡선 ±3 mAh g⁻¹) · 첫 CE 계산.

---

## 8. 우리 DEM+MPM 대비 ★ (우리 값의 출처 = `docs/50kg/report_y4/storyline_draft1.md` · `docs/50kg/report_y4/lit_se_size_map_20261030.md`)

### 8-1. 비교표
| 항목 | 이 논문 | 우리 (50 kg 4차년도) | 같음 / 다름 · 왜 |
|---|---|---|---|
| SE 입도 | **두 점** ≈6 µm (L) · <1 µm (S) · 공급사 시료 · PSD 없음 | 단분산 대리 D50 0.7 · 1 · 2 · 3 µm (네 점) | S_SE ≈ 우리 D0.7 · D1 자리 · L_SE (6 µm) 는 우리 범위 **밖** (= CAM 과 같은 크기) |
| CAM · 크기비 | NCM523 · 입경 [미확인] → λ 계산 불가 | NCM D6 단일 · λ = 8.57–2 | 크기비 축으로 놓을 수 없다 |
| 조성 | 75 : 22 : 3 (VGCF) wt% | 85 wt% AM · 탄소 [미확인] (size map p4) | AM 분율 · 탄소 다름 |
| 압밀 | 900 MPa (실험 절) / 600 MPa (결과 절) · 운전 압력 [미확인] | 목표 300 MPa → 판 고정 이완 (279.8 · 291.4 MPa) | 압밀 크게 다름 (서술 불일치까지) |
| 측정 / 계산 대상 | SOC 별 R1 · R2 · R3 · 율속 · 복합체 σ (한 상태) | 가압 상태 망의 f · tau2 · 협착 몫 (SOC 무관 오믹 수송) | 겹치는 곳 = **Table S1 의 복합체 σ 한 줄**뿐 · R2 · R3 는 우리 범위 밖 |
| "최적 입도" | **SOC 에 따라 뒤집힘** (≈20 %) | `KG50B-02`: 덱에서 *"최적 입도"* 금지 | ★ 금지의 **직접 문헌 근거** |
| 접촉 | 계면 용량 S/L 0.85 → 1.30 (첫 사이클 전 → 뒤) | p3 = AM 구면 기하 캡 합집합 · AM 마다 접촉 수 × 면적 (계산 전) | 새 전극에서 작은 SE 의 접촉이 **작을 수 있다**는 실측 정황 — 우리 p3 의 질문 (*"접촉이 늘면 피복도 느는가"*) 에 맞닿음 |

### 8-2. 50 kg 문헌 지도 (`lit_se_size_map_20261030.md` §6 순위 5 *"최적 입도의 SOC 의존 · 저항 분해 · p7 · p5"*) 에서의 자리
- **p7 (관측된 경향 · 다음 검증)** — 문헌 마무리가 *"최적"* 인 경우가 많은데 (지도 §3 p7), 이 논문은 같은 두 전극의 우열이 **SOC · 충방전 방향**으로 바뀜을 보인다.  ⇒ p7 의 *"문헌 방향 (카드)"* 열에 **"우열이 SOC 에 따라 뒤집힘 (≈20 %) — 한 값의 최적 없음"** 을 넣을 수 있다.  우리 지표 (구조 · 오믹 수송) 는 SOC 를 모르므로, 우리 표의 칸은 *"계산 / 모형 한계"* 상태로 이 축을 표시하는 것이 정직하다 [추정 · 권고].
- **p5 (구조 전달계수와 물성 가정의 분리)** — 복합체 σ_ion 이 **큰 SE 쪽 2.33 배** · 저자는 SE 자체 σ 차이를 원인으로 지목하지만 값이 없다.  우리 손익분기선 (f(1)/f(3) > 2.217) 의 언어로 쓰면: *"이 실측에서는 (<1 µm 의) 구조 이득이 있었더라도 재료 쪽 손해를 넘지 못했다"* 일 수 있다 — 단 펠릿 σ 가 없어 **f 비와 σ₀ 비를 가를 수 없다** [우리 산술 + 추정].  ⚠ 지도 §6 순위 4 의 *"LPSCl 에서 큰 PSD 가 이긴 반례"* (같은 묶음 스테이징 카드 `yadav2021_lpscl_sieved_psd_impedance_tortuosity` — 내용은 그 카드에서 확인) 와 같은 방향의 사례.
- **p3 (접촉 · 피복)** — `Fig. S9`: 새 전극의 계면 용량 S/L ≈0.85.  *"작은 SE → 접점 수 ↑"* (본문 서론 문장) 와 반대로, 전기화학적으로 닿은 면적은 작은 SE 쪽이 **작게** 시작한다 → 우리 p3 의 *"접촉 수 · 크기 · 겹침을 나눠 본다"* 설계가 맞다는 정황 (접촉 수 ≠ 유효 면적) [추정].  ⚠ 상대값 · 방법 1 개 · 반복 [미확인].
- **p4 · p6** — 이 논문에 해당 자료 없음.

### 8-3. 우리 모델이 이 논문을 따라 할 수 있나
- **할 수 있는 것**: 같은 두 입도 꼴 (D1 vs 큰 입도) 의 가압 침대에서 이온 · 전자 f · tau2 · 접촉 면적 (기하 캡) 을 내어 `Table S1` 의 **방향** (σ_ion 은 SE 자체 σ 에 걸림 · σ_e 는 입도 무관) 을 구조 쪽에서 볼 수 있다 — 우리 σ₀ 는 입력이므로 **구조 몫만** 낸다 [추정].
- **할 수 없는 것**: R2 (전하이동) · R3 (고체 확산) 의 SOC 의존 · 충방전 비대칭 · 사이클 중 접촉 재배열 (언로딩 · 부피 변화 없음) · 계면 용량.  ⇒ 이 논문의 결론은 우리 DEM 결과로 **검증도 반박도 할 수 없다** — 다음 보고 (3D 전기화학) 의 영역.

### 8-4. frame[4] / [5]
- frame[5]: 이 논문 = 전기화학 결과 (SOC 의존) · 우리 DEM = 구조 → 오믹 수송.  겹침은 복합체 σ 한 줄.  MPM (형상 · 공극) 쪽 정보 없음.
- frame[4]: 맞춰 볼 숫자가 없다 (면적 · 공극 · PSD · 순수 σ 미기재) → 이 논문으로 우리 모델을 보정하지 않는다.  쓰임은 **문장의 한정어** (최적 입도 · 접촉) 쪽.

## 9. 비판 / 주의 / 한계 ★ (over-claim 방지)
1. **두 점 · 한 조성** — 입도 ≈6 vs <1 µm 두 값 · NCM523 한 종 · 75 : 22 : 3 한 조성 · PSD · 비표면적 · 공극 · 두께 · 면적 · 로딩 없음 → *"최적 입도가 SOC 에 따라 달라진다"* 는 **두 전극의 우열 역전**이지 최적값 곡선이 아니다.
2. **순수 SE σ 미보고** — 측정법은 적고 값이 없다.  S_SE 가 어떻게 작아졌는지 (분쇄? 합성?) 도 [미확인] → 복합체 σ_ion 차 (2.33 배) 를 구조 · 재료 중 어디에 돌릴지 가를 수 없다.  저자의 *"SE 자체 σ 에 걸린다"* 는 인용 [26] 에 기댄 서술.
3. **성형압 서술 불일치** — 결과 절 600 MPa (+ 스택 200 MPa) ↔ 실험 절 900 MPa (200 MPa 는 순수 SE 측정 셀) [인쇄 p.2 ↔ p.6].
4. **본문 ↔ 그림 불일치** [판독]: (a) GITT 영역 III 문장의 L/S 뒤바뀜 의심 (§5.4) (b) *"R3 에서 차이가 더 크다"* ↔ 판독 R2 차가 더 큼 (c) *"This trend can be visualized from the discharge curves shown in Figure 2"* — Figure 2 는 EIS (방전 곡선은 Figure 1 · 4) (d) `Fig. S9` 를 *"SOC 의 함수로 역전"* 이라 했으나 그림은 **첫 사이클 전 · 후** 비교 (SOC 0 %) (e) SI 머리말 *"Table S1 and Figures S1–S8"* ↔ 실제 S9 까지 (f) `Fig. 6` 축 *"Rention ratio"* 오자 (g) 이슬점 *"ca. 80 °C"* (h) 참고문헌 [19] (*Adv. Energy Mater.* 2019, 2, 1902881) 과 [30] (2020, 10, 1902881) 이 같은 Shi 논문의 다른 서지.
5. **SOC 0 % 반쪽셀의 S_SE 고주파 절편 ≈75–80 Ω (L ≈12)** — 설명 없음.  대극 (In–Li) · 셀 접촉 문제일 수 있으나 [추정], *"SOC 0 % 에서 S_SE 총저항이 낮다"* 는 이 오프셋을 포함한 비교다.
6. **VGCF 3 wt% 전극의 σ_e 0.052–0.058 mS cm⁻¹** — 같은 정본의 탄소 포함 황화물 복합양극 값 (Lee 2025 33–34 · Kim 2024 38.6–65.2 mS cm⁻¹, `schlautmann2023` 카드 §7c 인용) 보다 두 자릿수 낮고, 무탄소 NCM811 복합체 (Schlautmann 0.26–0.41) 보다도 낮다 [교차 카드 비교].  측정 셀 · 압력 · 두께 [미확인] → 절대값을 다른 문헌과 같은 줄에 놓지 말 것.  *"전자 σ 는 AM 이 정한다"* 는 탄소가 있는 전극에서 이 논문 안에서는 검증되지 않았다.
7. **R1 귀속** — 양극|SE|SE|양극 대칭셀의 2 µs 성분에는 SE 층 이온 저항이 들어갈 수 있다 [추정]; 저자도 *"장비 정확도에 크게 영향"* 이라 적는다 → R1 으로 전극 전자 σ 를 정한다는 문장은 근거가 약하다.
8. **GITT ↔ EIS 시정수 대응** — R1 (2 µs) · R2 (10 ms) 를 GITT 시간 자료에서 어떻게 읽었는지 [미확인] · `Fig. S7` 의 *"approximately consistent"* 는 정량 대조가 아니다 (5000 s 점 L ≈38 ↔ GITT ≈50 Ω) [판독].
9. **"ASSB 고유" 주장** — *"has not been reported for liquid-based LIBs and is unique to ASSBs [24]"* · *"[33]"* — 액체 대조 실험 없이 인용 (ref [24] = 2003 년 액체계 양극 논문) 으로 주장.
10. **접촉 지표 (S9)** — 각 조건 L_SE 로 정규화한 상대값 · 방법 1 개 · 반복 [미확인] → *"작은 SE 가 접촉을 더 잘 유지한다"* 의 정량 근거로는 약하다.
11. **하한 전압** — 실험 절 3.0–4.35 V ↔ `Fig. 1` · `Fig. 4` 는 ≈2.5 V 까지 내려감 (율속 · GITT 하한 미기재) [판독].
12. **전이 한계 (우리 쪽)**: L_SE 6 µm = CAM 급 크기 (우리 범위 밖) · NCM523 · VGCF · 900 MPa · Ω (면적 없음) → **절대값 · 크기비 대조 불가**.  쓰임 = 한정어 (*"SOC 의존"* · *"접촉 ≠ 접점 수"*) 와 p5 의 방향 사례.

## 10. 적용 인사이트
1. **p7 문장** — *"SE 입도에 따른 우열은 SOC · 충방전 방향에 따라 뒤집힐 수 있다 (D50 ≈6 vs <1 µm LPSCl, SOC ≈20 % 에서 전하이동 저항 역전 · Kawaguchi 2026) — 이 보고는 SOC 무관 구조 · 오믹 수송만 보며 '최적 입도' 를 정하지 않는다."*
2. **p5 각주** — 복합체 σ_ion 이 큰 SE 쪽 2.33 배인 실측이 있다 · 단 SE 펠릿 σ 미보고라 구조 몫 (f) 과 재료 몫 (σ₀) 을 가를 수 없다.  우리 f(d) 계산이 바로 그 *"구조 몫"* 을 따로 내는 일이다 (KG50B-02 · 07 문구와 같은 결).
3. **p3 설계 확인** — 접점 수와 유효 접촉 면적을 따로 세는 우리 p3 설계가 맞다 (새 전극에서 작은 SE 계면 용량 0.85 배 · 사이클 뒤 1.30 배) — 단 우리는 사이클을 못 돌리므로 *"새 전극 (가압 상태)"* 쪽 값만 낸다.
4. **다음 보고 (3D 전기화학)** — 이 논문의 R2 · R3 SOC 지도 (`Fig. 5`) 는 STEP4 류 반응 모델의 정성 표적이 될 수 있다: 저 SOC 에서 R_ct · 확산이 커질 때 작은 SE (넓은 계면) 가 유리해지는가 [추정].

## 11. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "In NCM523 composite cathodes with argyrodite LPSCl of D50 ≈6 µm versus <1 µm (NCM:SE:VGCF = 75:22:3 wt%), the charge-transfer resistance obtained by combining GITT with cathode symmetric-cell impedance was lower for the larger electrolyte above ≈20 % SOC but lower for the finer electrolyte below ≈20 % SOC, and the larger electrolyte gave better charge-rate while the finer one gave better discharge-rate capability (Kawaguchi et al., *Batteries & Supercaps* 2026)."
- "The effective ionic conductivity of the same composites was 3.5 × 10⁻⁴ (≈6 µm) versus 1.5 × 10⁻⁴ S cm⁻¹ (<1 µm), while the electronic conductivity was similar (5.2 vs 5.8 × 10⁻⁵ S cm⁻¹); the pellet conductivities of the two electrolytes were not reported."
- 국문: *"LPSCl 입도 (≈6 vs <1 µm) 의 우열은 SOC ≈20 % 에서 뒤집힌다 — 높은 SOC 는 큰 SE (이온전도), 낮은 SOC 는 작은 SE (계면 접촉 · 전하이동) 가 저항이 낮다 (두 입도 · 한 조성 · 면적 · 공극 · 순수 SE σ 미보고)."*

## 12. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유)
| 번호 | 서지 (원문 그대로) | 왜 |
|---|---|---|
| 21 | C. Yu, S. Ganapathy, H. E.R., H. Wang, S. Basak, Z. Li, M. Wagemaker, Nat. Commun. 2017, 8, 1086. | 입도 분포의 중요성 (서론 근거) |
| 25 | Z. Shiroma, J. Power Sources 2016, 316, 215. | 복합체 σ 측정법 (Table S1 의 근거) |
| 26 | N. Kaiser, S. Spannenberger, M. Schmitt, M. Cronau, Y. Kato, B. Roling, J. Power Sources 2018, 396, 175. | 정본 카드 있음 (`kaiser2018_ion_transport_limitations_assb_sulfide_electrodes`) — 복합체 이온 σ 측정 · *"SE 자체 σ 에 걸림"* 의 근거 |
| 29 | S. Kawaguchi, N. Fukiya, … T. Miyuki, Adv. Mater. 2025, e07963, https://doi.org/10.1002/adma.202507963. | 같은 그룹 — 성형 · 스택압 설정의 근거 (600/200 MPa 서술의 출처 확인용) |
| 32 | K. Otani, T. Muta, T. Furuta, T. Miyuki, T. Kaburagi, G. Inoue, J. Energy Storage 2023, 58, 106279. | 정본 카드 있음 (`otani2023_ionic_conductivity_path_resistance_separation_model`) — 같은 LIBTEC |
| 31 | E. Schlautmann, … W. G. Zeier, Adv. Energy Mater. 2023, 13, 2302309. | 정본 카드 있음 (`schlautmann2023_se_particle_size_composite_transport`) |
| 36 | S. Yanev, H. Auer, R. Pertsch, C. Heubner, K. Nikolowski, M. Partsch, A. Michaelis, J. Electrochem. Soc. 2024, 171, 050530. | SOC 의존 양극 저항 (ASSB) |
| 42 | S. Kawaguchi, H. Yasuda, W. Ogihara, H. Sano, M. Kuzuhara, T. Miyuki, J. Colloid Interface Sci. 2025, 696, 137878. | ★ 계면 용량 = 접촉 지표 방법 (`Fig. S9` 의 근거) |
| 45 | M. So, G. Inoue, K. Park, K. Nunoshita, S. Ishikawa, Y. Tsuge, J. Power Sources 2022, 530, 231279. | 크고 작은 SE 의 선택적 배치 (혼합 전략의 난점) |
| 38 · 39 | A. Verma, … P. P. Mukherjee, J. Electrochem. Soc. 2017, 164, A3380 · T. Schied, … G. Cuniberti, ChemPhysChem 2021, 22, 885. | NCM 저항의 SOC 의존 (액체계) |

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-10-30)
- 두 파일을 내용으로 판정 (본문 = `…_2.pdf` 8 쪽 · SI = `…_1.pdf` 12 쪽) · 본문 텍스트 층 전수 · SI 텍스트 층 전수 + 전 쪽 렌더 열람 (SI 는 Word 인쇄본이라 그림이 수십 개 타일 래스터로 쪼개져 있어 `get_image_info` bbox 대신 캡션 위 영역을 잘랐다).
- 크롭 16 장 = 본문 Figure 1–6 (임베드 래스터 bbox) + SI Table S1 + SI Figure S1–S9 (캡션 위 영역 + 흰 여백 자동 정리) · 200 dpi `pdftoppm` → PIL · 전부 열람 · `Fig. 2b` 는 400 dpi 로 확대 판독.
- 막대 · 곡선 수치는 전부 [판독] (막대 ±2 Ω · 용량 ±3 mAh g⁻¹ · 저항–전위 ±5 Ω) — 논문은 수치표를 주지 않는다 (Table S1 의 σ 네 값만 인쇄).
- 정본 litdb 확인 (coordinator 사전 확인 · 같은 DOI · 제목 카드 없음) · 이웃 카드 slug 는 `git ls-tree origin/claude/friendly-meitner-lldvar litdb/papers/` 로 존재 확인.

## 🔗 관련 카드
- 같은 그룹 · 방법: `otani2023_ionic_conductivity_path_resistance_separation_model` (LIBTEC) · `kaiser2018_ion_transport_limitations_assb_sulfide_electrodes` · `malifarge2017_tortuosity_symmetric_cell_impedance_tlm` (대칭셀 임피던스) · `siroma2015_transmission_line_model_porous_electrode_impedance`.
- SE 입도 · 복합양극: `schlautmann2023_se_particle_size_composite_transport` · `shi2019_high_am_loading_particle_size_assb` · `minnmann2021_jes_charge_transport_bottlenecks` · `minnmann2024_microstructure_porosity_visualization` · `bazzoun2025_dem_parameter_sensitivity_assb_cathode` · `tailored_cathode_microstructure_low_pressure_assb` · `cronau2022_wet_milling_particle_size_ionic_conductivity` · `frankenberg2025_milling_dry_processed_sulfide_cathode_microstructure`.
- NCM 전자 · SOC: `aminchiang2016_nmc_electronic_ionic_transport_vs_li` · `asano2017_ncm111_li3ps4_composite_electronic_ionic_conductivity`.
- 탄소 포함 σ_e 비교군: `lee2025_corolling_dryprocess_lpscl_ptfe` · `kim2024_carbon_volumetric_occupation_se_domain` · 접촉 · 피복: `kim2024_optimal_cathode_composite_mechanical_mixing_se_coverage` · `lee2024_shear_force_dry_process_cathode_coverage`.
- 같은 주제 태그 (size_effect): `lei2026_se_particle_size_effects_review` · `stavola2023_thick_nmc111_lpscl_lithiation_gradient_tortuosity`.
- 같은 묶음 (10-30 스테이징 · 다른 에이전트 · 제목만 확인): `yadav2021_lpscl_sieved_psd_impedance_tortuosity` (큰 PSD 쪽 결과 — 지도 순위 4) · `lin2025_submicron_lpscl_cathode_li_kinetics` (서브 µm LPSCl 양극의 동역학 — 이 논문의 S_SE 와 같은 크기대) · `tron2023_rational_cathode_composite_optimization_lpscl` (LPSCl 입도를 다른 설계 변수와 함께) · `yano2026_se_psd_width_ionic_tortuosity_dem` · `calpa2019_small_li7p3s11_liquid_phase_composite_cathode`.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
