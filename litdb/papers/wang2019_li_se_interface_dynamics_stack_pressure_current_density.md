<!-- digest 표준 양식 (paper-level STANDALONE). 깊이 기준 = papers/zuo2022_chlorination_cathode_interface.md
     2026-11-24 신규 (litdb-curator · 병렬 인입 한 편 · 공유 파일 (INDEX · comparison) 은 메인 세션이 합친다).
     ① 그림: 자동 추출 11 장 (본문 Fig. 1–8 · SI Fig. S1 · S2 · Table S1) — 놓친 그림 0.
        도구의 '번호 공백' S3–S8 은 오탐 (SI 글의 'in Figure 5' · 'in Figure 8' 을 S5 · S8 로 읽음) → figures.json missing_labels 에 not_cropped 사유.
        그림 10 장 전부 실독 (Fig. 2 · Fig. 6 은 확대 크롭으로 한 번 더). Table S1 은 PDF 글자로 읽었다 (tab_S1.png 는 이미지로 안 봄).
     ② 값 표지: 본문 숫자는 그대로 (쪽 병기) · 그림에서만 읽은 값 = 'figure-read ≈' · 우리가 계산한 값 = '✎ 우리 산술' · 해석 = '[우리 해석]'.
        판독 · 재계산 129 행 = litdb/figures/<slug>/digitized.csv (축 눈금 · 식 · 가정이 note 열에).
     ③ 핵심 발견: Fig. 8 의 크리프 점은 아래 축 라벨보다 한 단 위 압력의 값이다 (Table S1 로 재계산 · 이웃 점 비 검산은 T 무관) →
        본문의 '0.4 MPa 에서 모형 = 실측' 은 라벨 읽기에서 나온 일치다 (5.11 · 10-①). 모형의 전류 의존 (σ⋆ ∝ j^0.15) 은 실측 (≈ j^1) 과 자릿수가 다르다 (10-②).
     ④ 쪽 표기 = 저널 쪽 (PDF 쪽 = 저널 쪽 − 2163 · PDF p.1 = 그래픽 초록 표지 · 저널 2165 = PDF p.2). SI 쪽 = SI PDF 쪽 (p.1 표지 · p.2 Fig. S1 · S2 · p.3 Table S1).
     ⑤ 병렬 규칙: 우리 점착 (W) 값은 싣지 않는다 — 위치만. -->

# Characterizing the Li-Solid-Electrolyte Interface Dynamics as a Function of Stack Pressure and Current Density — Wang · Choudhury · Sakamoto (*Joule* 3, 2165–2178 (2019))

> slug `wang2019_li_se_interface_dynamics_stack_pressure_current_density` · DOI `10.1016/j.joule.2019.06.017` · type `exp (Li|LLZO|Li 대칭셀 · in operando 하중 제어 적층압 · 정전류 단방향 박리 + 사이클 · operando EIS · Ni 기준전극 3-전극 · 1차 크리프–전류 변형률 균형식) — DFT · MD · 연속체 수치해석 없음` · PDF `litdb/inbox/wang2019_li_se_stack_pressure_main.pdf` (본문 15 pp) + `litdb/inbox/wang2019_li_se_stack_pressure_SI.pdf` (SI 3 pp — Fig. S1 · S2 · Table S1) · digested `2026-11-24` · status ✅ · 태그 **[외부]**
> elements: Li, La, Zr, Ta, Al, O
> methods: —

> **저자**: Michael J. Wang ¹ · Rishav Choudhury ¹ · **Jeff Sakamoto\*** ¹,²,³ (교신 · jeffsaka@umich.edu) — ¹ Department of Materials Science & Engineering, University of Michigan (Ann Arbor) · ² Department of Mechanical Engineering, University of Michigan · ³ Lead Contact · 투고 2019-03-01 · 수정 2019-04-18 · 수락 2019-06-13 · 온라인 2019-07-12 · 권호 2019-09-18 · 자금 US DOE Advanced Battery Materials Research (BMR, bat276) + ARPA-E (DE-AR0000653) · 이해상충 없음 · 기여: 구상 M.J.W.·J.S. / 실험 M.J.W.·R.C. / 집필 M.J.W. / 지도 J.S.
>
> **계보 (이 논문 참고문헌 기준)**: [10] Wang & Sakamoto 2018 *J. Power Sources* (R_int ↔ 표면 점착) · [3] Wang, Wolfenstine & Sakamoto 2019 *Electrochim. Acta* (온도 의존 flux balance) → **본 논문** (적층압 × 전류 축) ← 공극 가설 [16] Koshikawa 2018 · [17] Krauskopf 2019 · Li 크리프 물성 [26] Masias 2019 · [27] LePage 2019.
> **litdb 이웃 (링크만)**: [`doux2020_stack_pressure_assb`](doux2020_stack_pressure_assb.md) (LPSCl 쪽 적층압 앵커) · [`tron2023_lpscl_ccd_ambient_pressure`](tron2023_lpscl_ccd_ambient_pressure.md) (상압 0.20–0.28 MPa 의 LPSCl CCD) · [`liao2025_interfacial_adhesion_li_plating_carbon_interlayer`](liao2025_interfacial_adhesion_li_plating_carbon_interlayer.md) (탄소 인터레이어 점착 ↔ Li 석출 위치) · [`kang2026_stress_regulated_li_plating_ag_c_cnf_hybrid_anode`](kang2026_stress_regulated_li_plating_ag_c_cnf_hybrid_anode.md) (Ag–C + CNF · Li 를 Coble 크리프 점성 유체로 다룬 phase-field) · [`burov2026_li_llzo_charge_transfer_mlmd`](burov2026_li_llzo_charge_transfer_mlmd.md) (Li|LLZO 계면 전하이동 MLMD) · [`deysher2022_transport_mechanical_aspects_assb_review`](deysher2022_transport_mechanical_aspects_assb_review.md) (이 논문을 ref [105] 로 소개)
> **같은 날 들어온 Li 금속 계면 묶음 (링크만)**: [`masias2019_li_metal_elastic_plastic_creep_properties`](masias2019_li_metal_elastic_plastic_creep_properties.md) (이 논문 ref [26] · 크리프 원전) · [`seymour2021_void_suppression_interfacial_adhesion_vacancy_transport`](seymour2021_void_suppression_interfacial_adhesion_vacancy_transport.md) (점착 W ↔ 계면 공공 · W ≥ 2σ 기준) · [`lee2022_thin_insitu_li_void_rewetting_llzo`](lee2022_thin_insitu_li_void_rewetting_llzo.md) (LLZO 위 얇은 Li · 고갈 vs 공극) · [`shi2026_argyrodite_stack_pressure_viscoplastic_deformation`](shi2026_argyrodite_stack_pressure_viscoplastic_deformation.md) (**LPSCl** 쪽 적층압 · 공극 닫힘 · 점소성) · [`kim2026_operando_void_detection_single_frequency_impedance`](kim2026_operando_void_detection_single_frequency_impedance.md) (박리 중 공극의 임피던스 검출 · LPSCl · LLZO) · [`sharafi2017_llzo_surface_chemistry_li_wetting_interfacial_resistance`](sharafi2017_llzo_surface_chemistry_li_wetting_interfacial_resistance.md) (LLZO 표면 화학 · Li 젖음 — §4a 의 400 °C 처리 근거 계열) · [`chatterjee2025_diffuse_interface_metal_anode_void_model`](chatterjee2025_diffuse_interface_metal_anode_void_model.md) (공극 연속체 모형 · 역학 없음) · [`sandoval2025_electro_chemo_mechanics_anode_free_ssb`](sandoval2025_electro_chemo_mechanics_anode_free_ssb.md) (무음극 전기-화학-역학) · [`yang2021_flat_li_stripping_lithiophilic_interface_design`](yang2021_flat_li_stripping_lithiophilic_interface_design.md) · [`yang2021_atomistic_li_stripping_plating_interface_md`](yang2021_atomistic_li_stripping_plating_interface_md.md) (박리 계면 원자 모형 · 친Li 계면 설계)

> **본 digest 에서 실제로 본 그림 (2026-11-24)**: `Fig. 1` `Fig. 2` `Fig. 3` `Fig. 4` `Fig. 5` `Fig. 6` `Fig. 7` `Fig. 8` `Fig. S1` `Fig. S2` — **10 장 전부** (`Fig. 2` · `Fig. 6` 은 확대 크롭으로 다시 봤다).
> 안 본 것: `Table S1` 의 이미지 (값은 PDF 글자로 확보 — 표는 글자가 정확) · 그래픽 초록 (PDF p.1 — 크롭 없음 · 쪽 렌더로만 봤다).
> 그림에서만 읽은 값은 **`figure-read ≈`** 로 표시했다.

---

## 0. 이 digest 를 읽는 법

읽기 축 셋:
1. **W_ad 보고서 7 절 (Li 친화성 · 점착과 공극의 관계)** — 이 논문은 점착을 재지 않는다. 점착이 *어디에 어떤 방향으로* 들어오는지만 준다 (§6 · §12-①).
2. **연속체 · DEM 모형 입력** — 임계 적층압 σ_crit(j) 실측표, Li 크리프 매개변수 (`Table S1` — 2 차 인용), 그리고 그 둘을 잇는 1 차 균형식이 실측을 *못* 맞춘다는 사실 (§3f · §5.11 · §10).
3. **LLZO 한정** — 아래 상자.

> ⚠⚠ **이 논문의 모든 값은 Li | LLZO (가넷 · 대부분 Ta-LLZO) 계다.** LLZO 는 Li 금속과 화학적으로 안정하다는 것이 논문의 출발 전제이고 (p.2166 — 황화물 · 페로브스카이트와 달리 계면 반응 가능성을 없앤다), 그래서 공극 효과를 화학과 떼어 볼 수 있었다. 우리 LPSCl 은 Li 와 반응해 Li₂S · Li₃P · LiCl 층을 만든다 (`comparison_vs_ours.md` §E · SEI 트랙) — **값을 LPSCl 로 옮기지 않는다.** LPSCl 쪽 대응 실측은 Kasemchainan 2019 (*Nat. Mater.* 18, 1105 — litdb 카드 없음 · 리뷰 카드 넷이 인용) 이다.

> ⚠ **'임계 적층압 (critical stack pressure)' 은 논문이 *"Loosely defining"* 이라고 스스로 쓴 정성 판정이다** — 단 간격 0.4 MPa · 단마다 5 h · 단방향 박리 · 조건마다 셀 하나. 연속체 · DEM 에는 **대조 표적** 으로만 쓴다 (frame[4] — 보정 표적 아님).

---

## 1. 한 줄 요약

Li|LLZO|Li 대칭셀을 하중 틀 (Instron) 안에서 적층압 3.2 MPa → 0 MPa 로 **5 h 마다 0.4 MPa 씩** 내리며 정전류로 한쪽만 벗기면 (박리), 전위가 폭주하는 '임계 적층압' 이 전류와 함께 커진다 — **0.1 / 0.2 / 0.4 mA cm⁻² → 0.4 / 1.2 / 2.0 MPa** (0.05 mA cm⁻² 는 0.4 MPa 까지 폭주 없음). Ni 기준전극으로 갈라 보면 그 분극은 **전부 박리 전극 (WE)** 에서 나고 석출 전극 (CE) 은 평평하다. 임계압 위에서는 압력을 내리고 올리는 대로 저주파 저항이 가역적으로 오르내린다. 저자들은 이를 *"박리 속도 > Li 크리프 공급 속도 → 계면 공극"* 으로 해석하고, 전류가 만드는 두께 변형률 jM/(ρFl₀) 와 거듭제곱 크리프 Aσ^m exp(−Q/RT) (m 6.6 · Q 37 kJ mol⁻¹ · 문헌값) 의 대소로 1 차 설명한다.

⚠ 단 **그 1 차 모형은 실측의 전류 의존을 재현하지 못한다** — 모형 교차압은 j^(1/6.6) 로 거의 평평하고 (✎ 0.05 → 0.4 mA cm⁻² 에서 0.97 → 1.33 MPa), 실측은 대략 j 에 비례한다 (0.4 → 2.0 MPa). 본문이 말하는 '0.1 mA cm⁻² · 0.4 MPa 에서의 일치' 는 `Fig. 8` 의 아래 축 라벨이 한 단 밀린 데서 나온 것이다 (§5.11 · §10-①).

---

## 2. 메타 / 동기 / 질문

| 항목 | 내용 |
|---|---|
| 계 | Li 금속 (750 µm 박, Alfa Aesar) \| **Li₆.₅La₃Zr₁.₅Ta₀.₅O₁₂ (Ta-LLZO · 대부분)** \| Li 금속 · 대조 **Li₆.₂₅Al₀.₂₅La₃Zr₂O₁₂ (Al-LLZO)** (`Fig. S1`) |
| 왜 LLZO 인가 (p.2166) | 높은 전도도 · Li 보다 훨씬 큰 탄성률 · **Li 금속과 화학적으로 안정** (계면 반응 가능성 제거) · 상대밀도 > 95 % · 계면 개질 없이 낮은 R_int (refs 3, 12) · 안정/불안정 석출 영역이 이미 정의됨 (refs 3, 8) |
| 던지는 질문 | 박리 (방전) 쪽 계면이 적층압 · 전류에 따라 어떻게 무너지나. 두 전극 셀로는 석출과 박리를 못 가르니 3-전극으로 가르고, 공극 가설은 압력 가역성으로 시험한다 |
| 문헌 갭 (p.2165–2166) | 석출 쪽 (필라멘트) 연구는 많고 석출 전류는 > 1 mA cm⁻² 까지 개선됐는데, **박리 쪽 계면은 묻혀 있어 못 봤다**. Kirkendall 공극 가설 (refs 16–18) · Ag 금속–고체전해질 계 (refs 19, 20) 에서는 잘 연구됐지만 Li 는 상동온도 · 항복강도가 달라서 따로 봐야 한다 |
| 핵심 장치 | Ar 글러브박스 속 **Instron 5944** 하중 제어 (적층압을 운전 중에 바꾼다 = *in operando*) + Biologic VMP-300 + DC 위에 AC 를 얹은 operando EIS + 빌릿 측면의 Ni 기준전극 |
| 저자 전제 | LLZO 의 t_Li⁺ ≈ 1 → 전류 = Li 플럭스 → 박리 전극의 두께 변화율 = 변형률 (p.2173) |

- **Context & Scale** (PDF p.2): 고에너지 Li 금속 전고체전지의 율속 한계는 고율 사이클 중 계면 형상 변화 → 계면 저항 변화다. 적층압이 정전류 사이클에 필요한 과전압을 극적으로 바꾼다는 것을 보이고, 내부 저항 증가 기전을 제안하며, 적층압을 고출력 전고체전지의 설계 변수로 내세운다.
- **Highlights** (PDF p.1): ① Li 금속 전고체전지에 적층압이 필요함 ② 전류 밀도 ↔ '임계 적층압' ③ 3 전극으로 박리 전극 거동을 분리 ④ 적층압 · 전류 ↔ 계면 공극 형성.
- **그래픽 초록** (PDF p.1 · 쪽 렌더로 봄): 전위 (0–1.5 V) 가 계단식 적층압 (0–3.5 MPa) 이 σ_crit 아래 (빨간 영역) 로 들어가면 치솟는 도식 + σ > σ_crit / σ < σ_crit 계면 도식 (`Fig. 7` 과 같은 그림).

---

## 3. 핵심 수치 총정리 ★

> 쪽은 저널 쪽. `figure-read ≈` = 그림에서만 읽은 값 · ✎ = 우리 산술 (식은 그 자리에).

### 3a. 셀 · 재료 (Experimental Procedures, p.2176–2177)

| 항목 | 값 | 비고 |
|---|---|---|
| LLZO 조성 | Li₆.₅La₃Zr₁.₅Ta₀.₅O₁₂ (주) · Li₆.₂₅Al₀.₂₅La₃Zr₂O₁₂ (`Fig. S1` 대조) | rapid-induction hot-pressing (refs 3, 8) |
| 펠릿 두께 | ≈1.3 mm (다이아몬드 톱) · 3-전극용 빌릿 **5.7 mm** | 사포 + 다이아몬드 페이스트 단계 연마 → 0.1 µm (Buehler EcoMet250) |
| 표면 처리 | Ar 글러브박스 보관 · **400 °C 3 h** 열처리로 표면 Li₂CO₃ 제거 | 낮은 R_int 의 전제 (refs 3, 12) |
| Li 전극 | 750 µm Li 박을 양면에 **3.2 MPa** 로 누른 뒤 **≈170 °C · ≈1 MPa** 가열 (계면 접촉 개선) | Li 녹는점 180.5 °C 바로 아래 (✎ 상수) · `Table S1` 의 l₀ = **700 µm** (압착 뒤 두께로 보이나 설명 없음) |
| 전극 면적 | **본문 미기재** | 도식 축척으로 Li Ø `figure-read ≈`9 mm (`Fig. 1`) · 6–7 mm (`Fig. 4A,B`) — 도식이라 신뢰 낮음. 전류 밀도로만 읽는다 |
| Ni 기준전극 | 빌릿에 위 · 아래 면과 수직한 셋째 면을 톱으로 내고 **≈200 nm Ni 스퍼터** (Angstrom Engineering NexDep) + Ni 박 탭을 은 페이스트로 | EIS 로 WE · CE 와 전기적 분리 확인 (`Fig. 4C`) · Li vs Ni 개회로 전압 **2.78 V** (`Fig. S2` 캡션) |
| 온도 | **미기재** (글러브박스 상온으로 보임) | 크리프 계산의 T 도 미기재 — 우리 재계산은 298 K 가정 (§3f) |

### 3b. 임계 적층압 — 단방향 박리 (`Fig. 2`, p.2167) ★

프로토콜: 3.2 MPa 에서 정전류 5 h → 0.4 MPa 내림 (하중 전환 1 mm min⁻¹) → 5 h → … → 0 MPa (p.2177). 세로축 = (E_we − E₀)/E₀ (E₀ = 시작 전위 · 셀 사이 총저항 편차를 지우려는 정규화 — **E₀ 값은 안 적었다**).

| j (mA cm⁻²) | 논문 판정 '임계 적층압' | `figure-read ≈` 상승이 시작된 단 | `figure-read ≈` 축을 뚫은 (발산) 단 | ✎ 발산까지 벗긴 Li |
|---|---|---|---|---|
| 0.05 | — (*"does not exhibit a drastic potential increase at any stack pressure"* · 0.4 MPa 단 끝에 눈에 띄는 분극) | 0.4 MPa 단 (35 → 40 h: 0.13 → 0.30) | 없음 (그림은 40 h = 0.4 MPa 단 끝에서 끝난다) | 40 h 까지 2.0 mAh cm⁻² ≈ 9.7 µm |
| 0.1 | **0.4 MPa** | 0.8 MPa 단 (30 → 35 h: 0.27 → 0.92) | 0.4 MPa 단 (≈35.5 h) | 3.55 mAh cm⁻² ≈ 17 µm |
| 0.2 | **1.2 MPa** | 1.6 MPa 단 (20 → 25 h: 0.2 → 0.7) | 1.2 MPa 단 (≈28.3 h) | 5.7 mAh cm⁻² ≈ 27 µm |
| 0.4 | **2.0 MPa** | **3.2 MPa 첫 단부터** (0 → ≈0.8 in ≈3 h · 2.8 MPa 단 ≈0.9–1.0) · 둘째 상승 2.4 MPa 단 (1.0 → 2.0) | 1.6 MPa 단 (≈21.5 h) — 2.0 MPa 단에서는 2.4 → 5.9 | 8.6 mAh cm⁻² ≈ 42 µm |

- 그림의 적층압 계단은 `figure-read ≈` 3.15 / 2.75 / 2.35 / 1.95 / 1.55 / 1.15 / 0.74 / 0.33 MPa — 명목값 (3.2 − 0.4k) 보다 ≈0.05 MPa 낮게 그려져 있다 (단 간격에 비하면 무시할 만하다).
- ✎ 박리 속도 v = jM/(ρF) = **0.1 mA cm⁻² 당 0.485 µm h⁻¹** (1 mAh cm⁻² ≈ 4.85 µm Li) → 0.05 / 0.1 / 0.2 / 0.4 mA cm⁻² = 0.24 / 0.49 / 0.97 / 1.94 µm h⁻¹.
- **Ta- vs Al-LLZO** (`Fig. S1`, 0.2 mA cm⁻²): 둘 다 **1.2 MPa 단** 에서 발산한다 — Ta 는 `figure-read ≈`26–28.4 h, Al 은 ≈29.7 h (같은 단 안에서 Al 이 1.5–3 h 늦다). 논문: *"the same behavior was observed at the same stack pressures"* → "전해질 조성이 아니라 Li 전극 탓".
- **문헌 대조** (p.2172): 다른 연구도 > 0.2–0.5 mA cm⁻² 에서 눈에 띄는 분극 · 낮은 전류에서 평탄 (refs 3, 14, 17). 적층압은 잘 안 적지만 < 1 MPa 로 돌렸을 것 (refs 11, 15, 24). 높은 전류나 낮은 압력에서 낮은 과전압을 보인 연구는 Li | LLZO 사이에 **계면층 (interlayer)** 을 넣었다 (refs 13, 25) — Li 이동도와 계면 역학을 바꿨을 것.
- Li-ion 셀의 제조 적층압은 **0.1–1 MPa** (refs 28, 29). 0.4 mA cm⁻² 라는 낮은 전류에서도 2.0 MPa 가 필요하다는 것이 *"important constraint on the mechanical properties of viable solid electrolytes"* 가 된다 (p.2175).

### 3c. 임계압 위의 압력 사이클 — 가역성 + operando EIS (`Fig. 3`, p.2167–2169) ★

| 항목 | 값 | 출처 |
|---|---|---|
| 조건 | 0.1 mA cm⁻² · 적층압 2.4 ↔ 1.2 MPa 를 0.4 MPa 씩 · 단마다 hold **2 h** (방법) · 총 25 단 · 단 끝마다 EIS (DC 위에 AC) | p.2167, p.2177 |
| ⚠ 단 길이 | `figure-read ≈` **2.5 h** (25 단 ≈ 62.5 h · 그림 끝 ≈62 h) | `Fig. 3A` — 방법의 2 h 와 다르다 (차이 ≈0.5 h 가 EIS 시간일 수 있으나 미기재) |
| E_we (DC) | 2.4 MPa 시작 `figure-read ≈` 0.028 V → 첫 1.2 MPa 단 끝 ≈0.0357 V (+27 %) · 넷째 바퀴 1.2 MPa 는 ≈0.031 V (+11 %) | `Fig. 3A` — 내리면 약간 오르고 올리면 약간 내린다 · 단 끝에서 평탄 |
| EIS 표지 | Bulk **0.8 MHz** · GB **60 kHz** · Int **170 Hz** · ECR **0.1 Hz** (inset) | `Fig. 3B` |
| 고주파 | 2.4 vs 1.2 MPa **거의 동일** — 벌크 · 입계 변화 없음 · 고주파 호 끝 `figure-read ≈` **333 Ω cm²** | `Fig. 3B` |
| 저주파 'ECR' 호 | 1.2 MPa 에서 크고 2.4 MPa 에서 작다 · 등가회로 적합의 특성 정전용량 **≈10⁻³ F** → Irvine 1990 분류로 '전기화학 반응' (ref 21) | p.2169 |
| R_ECR (`Fig. 3C`) | 2.4 MPa `figure-read ≈` 83 (시작) → 45 → 44 → 32 → 33 Ω cm² · 1.2 MPa ≈256 → 233 → 170 → 170 Ω cm² (바퀴 1 → 4) — **≈5 배 진폭 · 가역 · 바퀴마다 조금씩 내려감** | 25 점 전부 `digitized.csv` |
| 저자 해석 | 임계압 위에서는 접촉 면적 손실이 거의 없다 (면적이 바뀌면 고주파 · 저주파 모두에 보일 것이므로). 대신 **계면 전기화학 동역학이 압력 의존** — Li 공공 · 흡착원자 (adatom) 이동과 관련될 수 있다 (Krauskopf, ref 17) | p.2169 |

### 3d. 3-전극 — 박리/석출 분리 (`Fig. 4`, `Fig. 5`, `Fig. S2`, p.2169–2170) ★

| 항목 | 값 | 출처 |
|---|---|---|
| 설계 근거 | Ni 는 상온에서 Li 와 합금하지 않아 **Li⁺ 를 완전히 차단** (ref 22) · LLZO 와 비반응 → 기준전극으로 이상적 | p.2169 |
| 검증 | WE–CE 비차단 (Li–Li) · WE–RE · CE–RE 차단 (Li–Ni: 곧게 솟는 용량성 선 · `figure-read ≈` 760–790 Ω cm² 에서 −Z″ ≈830) · 세 스펙트럼의 고주파 호 끝 `figure-read ≈` **400 Ω cm²** (5.7 mm 빌릿) · WE–CE 는 그 뒤 ≈400 → 510 Ω cm² 에 낮은 꼬리 (−Z″ ≲ 30) = 'R_int − Li/LLZO' 표지 | `Fig. 4C` |
| 조건 | 0.2 mA cm⁻² · 3.2 → 0.8 MPa (5 h 단 · 35 h 까지) | `Fig. 5` |
| E_WE − E_CE | `figure-read ≈` 0.1 V (평탄) → 20 h 0.2 → 25 h 1.2 → 30 h 5.8 → 35 h **8.2 V** · 본문 *"dramatically increases at 1.2 MPa"* | `Fig. 5` |
| E_WE (박리, vs Ni) | −2.74 V (0–10 h) → −2.722 (15 h) → **−2.63 (20 h · 2.0 MPa 단 끝)** → 21 h 에 −2.5 를 넘는다 → 30 h +3.2 → 35 h **+5.4 V** | `Fig. 5` · `Fig. S2` |
| E_CE (석출, vs Ni) | ≈ **−2.815 → −2.818 V** (0–25 h) · 35 h 까지 −2.82 로 평탄 | `Fig. S2` · `Fig. 5` |
| ✎ 20 h 까지의 변화 | WE **+0.11 V** vs CE **−0.003 V** (≈35 배) | `figure-read` 차 |
| 본문 판정 | WE 상승은 **≈2 MPa** 부터 · CE 는 시험 내내 평탄 → *"entirely due to the formation of voids at the Li stripping interface"* · 석출 Li 의 표면 거칠기 기여를 배제 | p.2170 |
| 9 V | WE–CE 전위차가 **9 V** 까지 올라 potentiostat 차단 값에 닿을 때까지 **단락 없음** (`Fig. 2` · `Fig. 5`) → *"the absolute potential of the CE is the main factor in Li filament initiation"* (Garcia-Mendez, ref 23 — 참고문헌에 저널 없음) | p.2170–2171 · ⚠ `Fig. 5` 에 그려진 최대는 `figure-read ≈`8.2 V (35 h) |

### 3e. 양방향 사이클 — 높은 / 낮은 적층압 (`Fig. 6`, p.2171–2172)

| 항목 | 값 | 출처 |
|---|---|---|
| 조건 | 0.2 mA cm⁻² · **3.2 MPa vs 0.4 MPa** (각 셀 하나) · 반주기 **0.35 mAh cm⁻²** (캡션은 단위를 "mA cm⁻²" 로 오기) · 주기 사이 15 min 휴지 | 캡션 · p.2171–2172 |
| ✎ 반주기당 Li | 0.35 mAh cm⁻² ≈ **1.7 µm** · 반주기 1.75 h (그림의 주기 ≈4 h · 40 h 에 10 주기와 맞는다) | 우리 산술 |
| 3.2 MPa | 평탄 `figure-read ≈` ±0.027 V (후반 ≈0.0265) | `Fig. 6` |
| 0.4 MPa | 평탄부는 같고 **반주기 끝에 위로 꺾이는 갈고리** — 정점 ≈0.029 (1 주기) → 0.031 → 0.0325 → 0.0336 → 0.035 → **≈0.036 V (6 주기 이후 포화)** · 양 극성 거의 같음 (*"approximately equal for both polarities"*) | `Fig. 6` · 확대 크롭 |
| 해석 | 15 min 휴지로는 *"insufficient time, temperature, and pressure to recreate an intimate contact and good adhesion between the Li and LLZO"* → 주기마다 공극이 더 빨리 생긴다 | p.2171–2172 |

### 3f. 크리프 균형 모형의 입력 (`Table S1`, SI p.3) 과 우리 재계산 ★★

| 매개변수 | 기호 | 값 | 출처 (논문 표기) |
|---|---|---|---|
| Li 몰질량 | M | 6.941 g mol⁻¹ | — |
| Li 밀도 | ρ | 0.534 g cm⁻³ | — |
| Faraday 상수 | F | 96485 C mol⁻¹ | — |
| 초기 전극 두께 | l₀ | **700 µm** | — |
| 크리프 매개변수 (보고값) | A′ | **7 × 10⁻³⁷ Pa⁻ᵐ s⁻¹** | LePage et al. [27] |
| 크리프 매개변수 (Masias 의 변형률 속도 감쇠 반영) | A | **9 × 10⁻⁴¹ Pa⁻ᵐ s⁻¹** | LePage [27] · Masias [26] |
| 거듭제곱 크리프 지수 | m | **6.6** (상온 · 전위 상승 (dislocation climb) 지배) | LePage · Masias [26, 27] |
| 활성화 에너지 | Q | **37 kJ mol⁻¹** | LePage [27] |
| 기체 상수 | R | 8.31 J mol⁻¹ K⁻¹ | — |

- 원전 대조: [`masias2019_li_metal_elastic_plastic_creep_properties`](masias2019_li_metal_elastic_plastic_creep_properties.md) 카드가 인장 크리프 지수 **n = 6.56** · σ_y 0.73–0.81 MPa 를 적었다 ([다른 카드] — 이 논문 m 6.6 과 같은 축 · 압축에서는 마찰 · 종횡비가 변형을 좌우한다는 그 카드의 서술이 아래 '감쇠 10⁻⁴' 의 뿌리다).
- 식: 전류 변형률 **ε̇_j = Δl̇ / l₀ = jM/(ρFl₀)** (식 2) · 크리프 변형률 **ε̇_creep = Aσ^m exp(−Q/RT)** (식 3) · 공극 조건 **ε̇_j > ε̇_creep** (식 4) · 접촉 면적 ↔ 저항 **R = ρl/A** (식 1).
- A/A′ = 1.29 × 10⁻⁴ — 본문 *"assuming a decay of ~10⁻⁴ due to frictional and adhesive forces at the interface"*. 근거는 Masias: 일정 응력 압축에서 Li 원기둥이 기판과의 마찰 · 점착 때문에 배럴링하고, 5 h 뒤 변형률 속도가 10⁻³–10⁻⁴ 배로 준다.
- **✎ 우리 재계산 (T = 298 K 가정 — 논문은 T 를 안 적었다)**:

| j (mA cm⁻²) | ε̇_j (s⁻¹) | σ⋆ 교차압 (A = 9e-41) | σ⋆ (A′ · 감쇠 없음) | σ⋆ (감쇠 10⁻³) | 모형상 첫 미달 단 (실제 σ 기준) | 논문 판정 σ_crit |
|---|---|---|---|---|---|---|
| 0.05 | 9.6 × 10⁻⁸ | **0.97 MPa** | 0.25 | 0.71 | 0.8 MPa | — (폭주 없음) |
| 0.1 | 1.9 × 10⁻⁷ | **1.08** | 0.28 | 0.79 | 0.8 | 0.4 |
| 0.2 | 3.8 × 10⁻⁷ | **1.20** | 0.31 | 0.88 | 1.2 (경계 — 두 값 차 0.5 %) · 확실히는 0.8 | 1.2 |
| 0.4 | 7.7 × 10⁻⁷ | **1.33** | 0.34 | 0.98 | 1.2 | 2.0 |

  - σ⋆ = (ε̇_j / (A e^(−Q/RT)))^(1/m) ∝ **j^0.15** — 이 전류 범위에서 모형은 사실상 '전류와 거의 무관한 ≈1 MPa' 를 말한다. T 를 295–303 K 로 바꿔도 σ⋆ 는 ±3 % 만 움직인다. 반면 감쇠 가정 (1 → 10⁻³ → 10⁻⁴) 은 σ⋆ 를 0.28 → 0.79 → 1.08 MPa (0.1 mA cm⁻²) 로 바꾼다 — **모형 예측을 정하는 것은 Li 물성이 아니라 감쇠 가정이다.**
  - 감쇠 없는 A′ 로는 3.2 MPa 에서 ε̇_creep ≈ **2 s⁻¹** (✎) — Li 박이 몇 초에 납작해지는 속도라 그대로는 못 쓴다.
  - 실측 σ_crit 의 전류 지수 (✎ log-log 기울기): 논문 값 (0.4 · 1.2 · 2.0) → **n ≈ 1.16** (0.1 → 0.4) · 발산 단 (0.4 · 1.2 · 1.6) → 1.0 · 상승 시작 단 (0.8 · 1.6 · 2.4–3.2) → 0.8–1.0. **어느 기준으로 읽어도 ≈ j^1 이고, 모형의 j^0.15 와 자릿수가 다르다.**

### 3g. 홉 수 검산 (CLAUDE.md 규율 — 차수 검산이지 크리프 속도가 아니다)

Q = 37 kJ mol⁻¹ = **0.383 eV** · T = 298 K (가정) · ν₀ = 10¹³ s⁻¹ (가정) → Γ = ν₀ e^(−Q/kT) ≈ **3 × 10⁶ s⁻¹** · 평균 대기 ≈ **0.3 µs** · 5 h 단 (1.8 × 10⁴ s) 동안 N ≈ 6 × 10¹⁰. → Q 자체는 상온에서 빠른 열활성 과정이다. 공급을 '느리게' 만드는 것은 σ^6.6 의 낮은 응력 쪽 급감 (0.8 → 0.4 MPa 에서 97 배) 과 마찰 감쇠 (10⁻⁴) 이지 Q 가 아니다 — 논문 서술과 차수상 충돌은 없다. ✎ Li 의 상동온도 T/T_m = 298/453.7 ≈ 0.66 (상온에서 크리프가 활발한 이유 · 논문은 '상동온도 차이' 라고만 쓴다).

---

## 4. 재료 & 방법 — 같은 축을 흉내 낼 때 필요한 조건 전부 ★

### 4a. LLZO
- Li₆.₅La₃Zr₁.₅Ta₀.₅O₁₂ — rapid-induction hot-pressing (refs 3, 8) · 다이아몬드 톱으로 ≈1.3 mm · 사포 + 다이아몬드 페이스트 단계 연마 → 0.1 µm (Buehler EcoMet250 자동 연마기) · Ar 글러브박스 보관 · 400 °C 3 h 로 표면 Li₂CO₃ 제거.
- 비교용 Li₆.₂₅Al₀.₂₅La₃Zr₂O₁₂ — 합성 상세는 본문 · SI 어디에도 없다 (`Fig. S1` 캡션의 조성뿐).

### 4b. 대칭셀
- 750 µm Li 박 (Alfa Aesar) 을 펠릿 양면에 · 3.2 MPa 압착 → ≈170 °C · ≈1 MPa 가열 (계면 접촉 개선).
- ⚠ 즉 이 셀들은 **잘 젖은 계면 (탄산염 제거 · 녹는점 근처 열처리)** 에서 출발한다. 낮은 초기 R_int 는 그 덕이다 — 임계압 값은 이 계면 상태에 딸린 값이다.

### 4c. 3-전극
- 1.3 mm 펠릿 대신 **5.7 mm 빌릿** 으로 대칭셀을 같은 방법으로 → 다이아몬드 톱으로 위 · 아래 면에 수직한 셋째 면 → ≈200 nm Ni 스퍼터 (Angstrom Engineering NexDep) → Ni 박 탭 + 은 페이스트 → EIS 로 WE · CE 와 전기적으로 분리됐는지 확인.
- 평면도 (`Fig. 4B`): 원판의 한쪽을 평평하게 깎은 'D' 모양 빌릿 · 가운데 Li 원판.

### 4d. 기계 시험 (하중 제어)
- Instron 5944 (인장 · 압축 시험기) 를 Ar 글러브박스 안에 · 적층압을 동적으로 제어.
- 단방향 박리: 3.2 MPa 에서 정전류 5 h (정상상태 도달용) → 전류를 끊지 않고 0.4 MPa 내림 (**1 mm min⁻¹**) → 5 h 유지 → 반복 → 0 MPa. 최대 3.2 MPa 는 선행 연구와 견주려고 골랐다 (refs 8, 10, 15).
- 압력 사이클: 0.1 mA cm⁻² · 1.2–2.4 MPa · 단마다 2 h (방법) · 0.4 MPa 씩 오르내림 · 총 25 단.
- ⚠ **하중 제어 (P 고정)** 다 — 우리 DEM 압밀 · 박리와 같은 경계조건 종류다 (정간극 볼트 지그와 반대 — `comparison_vs_ours_DEM.md` §I-7 이 그 차이를 다룬다).

### 4e. 전기화학
- Biologic VMP-300 · 모든 사이클은 Instron 안에서 · 0.05–0.4 mA cm⁻² — *"low enough such that Li filaments should not initiate in the LLZO and introduce extraneous variables"*.
- EIS: **7 MHz – 1 Hz** · 섭동 10 mV · 등가회로로 R_int 를 벌크 · 입계와 분리 · **modified Huggins model** · **RC 셋 직렬** (벌크 · 입계 · 계면) · 커패시터 대신 CPE (시간 상수 분포). ⚠ `Fig. 3B` 의 표지는 넷 (ECR 0.1 Hz 포함) — §10-⑥.
- operando EIS: AC 를 DC 위에 얹어 잰다. DC 를 끊으면 '압력은 있고 Li 용해는 없는' 상태라 사이클 중 계면 형상이 아니게 된다 (p.2168).

### 4f. 임계 적층압 판정
- *"Loosely defining this pressure as the 'critical stack pressure'"* — 전위가 '극적으로 오르는' 단. 수치 문턱 · 기울기 기준은 없다. 분해능 = 단 간격 0.4 MPa.

### 4g. 해석 모형 (전부)
- 식 1: R = ρl/A — 공극이 접촉 면적 A 를 줄이면 R_int 가 오른다 (도입부 p.2166).
- 식 2–4 (p.2173–2174): §3f. 거시 변형률끼리의 비교이고, 공극 핵생성은 훨씬 국소적이라 변형률 장이 크게 다를 수 있다고 저자 스스로 적는다 (p.2174).
- Ȧ/A₀ (`Fig. 8` 빨간 선): *"assuming the polarization exhibited in Figure 2 is dominated by changes in contact area below the 'critical stack pressure,' the change in area versus time is calculated by taking the derivative of the curve in Figure 2"* — 전위 → 면적 환산식은 적지 않았다.

---

## 5. 결과 — 섹션별 상세 (그림 실독 포함)

### 5.1 셀 도식 (`Fig. 1`)
Li WE (위) · LLZO (가운데 얇은 판) · Li CE (아래) 를 위아래 σ 화살표가 누른다. 검은 덩어리가 하중 판이고 (라벨 'Li WE / Li CE' 가 그 위에 적혀 있다), LLZO 에 닿은 회색 원기둥이 Li 다. 빨간 Li⁺ 화살표는 위 → 아래 (WE 박리 · CE 석출). 축척 3 mm 로 `figure-read ≈` LLZO 두께 ≈1.45 mm · 폭 ≈12 mm · Li Ø ≈9 mm (도식).

### 5.2 적층압 계단 × 전류 (`Fig. 2`) ★
곡선 넷 (0.4 긴 점선 · 0.2 일점쇄선 · 0.1 실선 · 0.05 짧은 점선) 과 빨간 계단 (오른쪽 축 0–3.5 MPa). 세로축 0–10 은 (E_we − E₀)/E₀ — 10 이면 전위가 시작의 11 배다.
- 0.1 · 0.2 · 0.4 는 각자 다른 단에서 거의 수직으로 축을 뚫는다 (≈35.5 · ≈28.3 · ≈21.5 h).
- 실제로 보면 '평탄 → 폭주' 사이에 **한 단짜리 완만한 전조** 가 늘 있다 (0.1: 0.8 MPa 단 · 0.2: 1.6 MPa 단 · 0.4: 2.4 MPa 단). 논문 판정 (0.4 · 1.2 · 2.0) 은 0.1 · 0.2 에서는 발산 단을, 0.4 에서는 큰 상승 단을 골랐다 (§10-④).
- 0.4 mA cm⁻² 는 **3.2 MPa 첫 단에서부터** ≈0.8 까지 오른다 — 이 전류에서 '높은 압력에서 평탄' 은 상대적이다.
- 0.05 는 40 h (0.4 MPa 단 끝) 에 ≈0.30.
- 본문 해석: 이 분극은 Li–LLZO 계면 근처의 **Li 플럭스 불균형** 과 강하게 상관한다 (ref 3).

### 5.3 Ta- vs Al-LLZO (`Fig. S1`)
같은 계단 · 0.2 mA cm⁻² · Ta (점선) 와 Al (실선) 모두 1.2 MPa 단 안에서 발산. Al 이 ≈1.5–3 h 늦다 (`figure-read`). 25 h (1.6 MPa 단 끝) 값은 Ta ≈0.8 vs Al ≈0.4. "전해질 조성과 무관 → Li 전극의 문제" 라는 결론은 **단 (0.4 MPa) 해상도에서만** 맞다 (셀 하나씩).

### 5.4 임계압 위 가역성 (`Fig. 3`) ★
- (A) 0.1 mA cm⁻² 에서 압력 지그재그 2.4 → 2.0 → 1.6 → 1.2 → 1.6 → … (4 바퀴). E_we 는 압력을 내리면 오르고 올리면 내린다 · 단 끝에서 평탄 · 단 끝마다 AC 를 얹은 흔적 (뾰족한 스파이크 — 24.8 h 에는 0.020 V 아래로 꺼진다). 첫 바퀴 진폭 ≈+27 % · 넷째 바퀴 ≈+11 % (`figure-read`) — 바퀴가 갈수록 계면이 '길들여진다'.
- (B) Nyquist: 큰 반원 하나 (벌크 + 입계가 겹침 · 꼭짓점 ≈(150, 125) Ω cm²) · 끝 ≈333 Ω cm² 에 'Int 170 Hz' 표지 · inset (320–380 Ω cm²) 에서 2.4 MPa (검정) 는 ≈345 에서 끝나는 작은 호, 1.2 MPa (빨강) 는 ≈368 · −Z″ ≈28 까지 곧게 오른다 — **측정 창 안에서 ECR 호의 앞부분만 보인다.**
- (C) R_ECR 25 점 vs 압력 지그재그 (빨간 점선): 1.2 MPa 마다 봉우리 (256 · 233 · 170 · 170) · 2.4 MPa 마다 골 (45 · 44 · 32 · 33) · 시작점 (2.4 MPa) 83. 같은 압력에서 '내려가는 길' 이 '올라가는 길' 보다 높은 경우가 8 쌍 중 6 쌍 (1 쌍 같음 · 1 쌍 반대 · 예: 첫 바퀴 1.6 MPa ↓ ≈235 vs ↑ ≈114) — 이력처럼 보이지만 전체가 시간에 따라 내려가는 추세와 구분되지 않는다. 논문은 언급하지 않는다.
- 의미: 0.1 mA cm⁻² 의 임계압 (0.4 MPa) 보다 **3–6 배 높은 압력에서도** 저주파 저항이 ≈5 배 움직인다 — '임계압 위 = 압력 무관' 이 아니다.

### 5.5 3-전극 설계 (`Fig. 4`)
(A) 빌릿 옆면에 Ni RE (회색 직사각형) · 전압계는 WE–RE 사이 · 전원은 WE–CE 사이. (B) D 자 빌릿 위 Li 원판 (`figure-read ≈` 빌릿 Ø ≈12 mm · Li Ø ≈6 mm). (C) Li–Ni 두 쌍은 차단 (거의 수직인 용량성 직선) · Li–Li 는 비차단 (작은 꼬리) · 세 쌍의 고주파 호가 겹친다.

### 5.6 박리 / 석출 분리 (`Fig. 5`, `Fig. S2`) ★ 이 논문의 핵심 증거
- `Fig. 5`: 검정 (WE − CE) 은 `Fig. 2` 와 같은 모양 · 노랑 (WE vs Ni) 이 그 증가를 거의 다 들고 · 파랑 (CE vs Ni) 은 −2.82 V 에 수평. 35 h 에 8.2 = 5.4 − (−2.8) — 그림 안의 산술이 맞는다.
- `Fig. S2` (확대 · −2.90 ~ −2.50 V): WE 는 2.4 MPa 단에서 이미 ≈+0.011 V 기어오르고, 2.0 MPa 단 (15–20 h) 에서 ≈+0.09 V 더 오르고, 1.6 MPa 단 시작 직후 화면을 벗어난다. CE 는 25 h 동안 ≈−0.003 V.
- ✎ 시작 과전압: WE −2.738 − (−2.78) = +0.04 V · CE −2.815 − (−2.78) = −0.035 V · 합 ≈0.077 V ≈ `Fig. 5` 검정의 시작값 ≈0.08–0.1 V (측면 RE 라서 WE–RE · CE–RE 에 벌크 IR 일부가 각각 들어간다).
- 결론: 분극은 박리 전극에 있고 석출 쪽 거칠기는 무시할 만하다 — **이 전류 · 압력 범위 · LLZO 에서.**

### 5.7 9 V 무단락 → 필라멘트 개시 해석 (p.2170–2171)
WE–CE 9 V 에서도 단락이 없다 → WE 분극도, 전위차도 필라멘트를 만들지 않는다 → CE 의 *절대 전위* 가 개시 요인이다 (Garcia-Mendez: 석출 전극의 underpotential 이 가전자대 · 전도대 겹침을 일으켜 Li 가 석출된다). ⚠ 셀 하나 · 낮은 전류 · 석출 쪽 과전압 ≈−35 mV 에서의 음성 관찰 하나로 일반화한 문장이다 (§10-⑩).

### 5.8 양방향 사이클 (`Fig. 6`)
3.2 MPa 셀 (빨강) 은 네모 파형 · 0.4 MPa 셀 (검정) 은 반주기 끝마다 위로 꺾이는 갈고리. 갈고리 높이는 ≈+1.5 mV (1 주기) → ≈+9 mV (6 주기 이후 포화) (`figure-read`). 0.4 MPa 는 0.2 mA cm⁻² 의 임계압 1.2 MPa 의 ⅓ 인데도 분극이 평탄부의 +33 % 수준에서 멈춘다 — 반주기당 1.7 µm 만 벗기기 때문으로 보인다 (`Fig. 2` 의 단방향은 발산까지 27 µm). [우리 해석] **임계압은 j 만이 아니라 반주기 용량의 함수다.**

### 5.9 공극 기전 — 플럭스 균형 (p.2172, `Fig. 7`)
적층압이 Li 를 계면 쪽으로 크리프시켜 공급한다 → 임계압 = '압력이 밀어 넣는 Li 플럭스 = LLZO 로 녹아 나가는 Li 플럭스' 인 점 → 그 위에서는 공급이 충분해 공극이 미미하고 (`Fig. 7A`), 아래에서는 공급이 모자라 공극이 생기고 자란다 (`Fig. 7B`). 전류 의존이 그 근거다 (높은 j → 더 높은 공급 필요). 압력만 올려도 분극이 되돌아오므로 *"purely mechanical in nature, rather than chemical"* (화학이면 압력으로 안 돌아올 것). `Fig. 7B` 는 박리 쪽 (위) 계면에만 반구형 공극을 그렸다 — 도식이지 관찰이 아니다.

### 5.10 1 차 모형 (식 2–4)
§3f. 저자 서술: Masias · LePage 모두 상온 Li 크리프를 거듭제곱 · 전위 상승 지배 (m 6.6) 로 결론. Masias: 일정 응력 압축에서 배럴링 때문에 변형률 속도가 시간에 따라 감쇠 (5 h 뒤 10⁻³–10⁻⁴) → 단 끝 변형률을 감쇠 10⁻⁴ 로 계산 (`Table S1`).

### 5.11 `Fig. 8` — 모형 대 실측, 그리고 우리 재구성 ★★
- 그림: 왼쪽 로그축 ε̇ (s⁻¹, 10⁻¹⁰–10⁻¹) · 오른쪽 로그축 Ȧ/A₀ (s⁻¹, 10⁻⁴–10⁰) · 아래 축 적층압 3.2 → 0 MPa · 위 축 시간 0–40 h. 열린 원 = 크리프 변형률 (8 점, t = 5…40 h) · × = 전류 변형률 (`figure-read ≈` 1.7 × 10⁻⁷ s⁻¹ — ✎ 식 2 값 1.9 × 10⁻⁷ 와 맞는다) · 빨간 선 = Ȧ/A₀ (≈32.9 h 에 10⁻⁴ 위로 · ≈35 h 에 급등 · ≈37 h 에 ≈0.15 봉우리 · 40 h 에 ≈7 × 10⁻³).
- 본문: *"at all stack pressures from 3.2 to 0.8 MPa, ε̇_creep exceeds ε̇_j … around 0.4 MPa, which is the same pressure at which ε̇_j first begins to exceed ε̇_creep."*
- **✎ 우리 재구성 — 원 8 점은 각 단의 *끝* (t = 5, 10, …, 40 h) 에서 *막 끝난 단의 압력* 으로 계산됐고, 아래 축은 그 시각에 *시작하는* 압력을 적었다 → 아래 축으로 읽으면 한 단씩 밀린다.** 근거 넷:
  ① **'0 MPa' 위치에 0 이 아닌 점** (`figure-read ≈` 3 × 10⁻¹⁰) — σ^6.6 은 σ = 0 에서 0 이라 불가능하다.
  ② 이웃 점의 비 (T · A 와 무관): 마지막 두 점 비 ≈97 = 2^6.6 = (0.8/0.4)^6.6 · 그 앞 ≈16 ≈ (1.2/0.8)^6.6 · 첫 두 점 비 ≈2.4 → σ 비 1.143 = 3.2/2.8 (라벨대로면 2.8/2.4 = 1.167).
  ③ 절대값: 첫 점 `figure-read ≈` 2.9 × 10⁻⁴ ↔ ✎ σ = 3.2 MPa 에서 2.5 × 10⁻⁴ (σ = 2.8 이면 1.0 × 10⁻⁴) · 마지막 점 3 × 10⁻¹⁰ ↔ σ = 0.4 MPa 에서 2.75 × 10⁻¹⁰ (298 K).
  ④ 위 시간 축: 점들이 t = 5 … 40 h 에 있고, 방법은 *"the strain-rate at the end of each pressure step"*.
- 결과: 실제 압력으로 읽으면 0.1 mA cm⁻² 에서 ε̇_j 가 처음 이기는 단은 **0.8 MPa** (σ⋆ ≈1.08 MPa). 실측 Ȧ/A₀ 의 상승 시작 (≈32.9 h) 도 0.8 MPa 단 안이다 → '모형 ≈ 실측' 은 **한 단 (0.4 MPa) 안의 일치** 로는 성립하지만, 본문이 말한 '0.4 MPa 에서 같다' 는 라벨 읽기의 산물이다.
- 다른 전류 (본문 *"The same behavior is observed with current densities of 0.05 and 0.2 mA cm⁻²"* · 0.4 만 불일치 — *"the ε̇_j does not dominate until 1.2 MPa"*): 0.4 mA cm⁻² 의 '1.2 MPa' 는 **실제 σ 로 읽어야** 나오는 값이다 (라벨로 읽으면 0.8). 즉 본문은 0.1 에서는 라벨로, 0.4 에서는 실제 σ 로 읽었다 — **한 그림을 두 방식으로 읽었다.** 실제 σ 로 통일하면 (모형 첫 미달 단 / 실측): 0.05 → 0.8 / 폭주 없음 (0.4 단 끝에 약간) · 0.1 → 0.8 / 0.4 · 0.2 → 1.2 경계 / 1.2 ✓ · 0.4 → 1.2 / 2.0.
- 저자가 든 불일치 후보 (p.2174): 공극이 생기면 실효 전류 밀도가 올라 ε̇_j 가 커진다 · 높은 전류에서 공극 핵생성 확률이 높을 수 있다 · 압력을 내리는 동안의 변형률 · 표면 거칠기로 인한 국소 전류 · 계면 동역학의 압력 의존 · 마찰 · 점착력. 거시 변형률 vs 국소 핵생성. → Li 압축 역학 (크리프 매개변수 정량) 과 정교한 모형이 필요하다고 맺는다.

### 5.12 함의 (p.2174–2176)
- 공극은 전해질과 상관없이 Li 금속 음극의 문제다. 극성을 바꾸기 전에 공극이 닫히지 않으면 석출 때 줄어든 접촉 면적에 전류가 모여 국소 고과전압 → 필라멘트 개시 · 단락이 될 수 있다 (ref 16).
- 급속 충전 Li 금속 전고체전지는 Li-ion (0.1–1 MPa) 보다 훨씬 높은 적층압이 필요할 수 있다 · 전해질은 2.0 MPa 이상을 견뎌야 한다 · 높은 압력이 필라멘트 전파에 주는 영향은 미지 (플럭스 불균형에 해로울 수도, 석출 균일성에 이로울 수도) · 재료 · 미세구조 · 형상이 허용 압력 상한, 따라서 허용 박리 전류 상한을 정한다.
- 대안: **운전 온도를 올려** Li 크리프를 빠르게 (refs 3, 8, 15) · 코팅으로 계면 Li 확산도를 · 야금 공학으로 Li 크리프 속도를 올린다.

### 5.13 결론 (p.2176)
임계 적층압 아래에서 셀 전위가 급증하고, 그 임계압은 0.1 mA cm⁻² 0.4 MPa → 0.4 mA cm⁻² 2.0 MPa 로 커진다 · 임계압 위에서는 EIS 상 가역 · Ni RE 로 R_int 증가가 박리 전극에만 있음을 보였다 · 확산 · 크리프에 의한 계면 쪽 Li 공급이 녹아 나가는 플럭스를 못 따라가면 공극이 생긴다는 가설을 지지 · 적층압은 공극 방지뿐 아니라 전해질 선택의 기준이 된다.

---

## 6. 메커니즘 종합

논문의 논증 사슬:
1. 박리 쪽만 분극한다 (3-전극) → 공극 · 접촉 손실이 박리 쪽에 있다 (추론 — 공극을 직접 보지는 않았다).
2. 압력을 올리면 되돌아온다 → 화학이 아니라 기계다 (LLZO 는 Li 와 안정하다는 전제와 함께).
3. 임계압이 전류와 함께 커진다 → 공급 (압력 구동 크리프) 과 소모 (박리) 의 플럭스 균형.
4. 1 차 모형: 거시 변형률 ε̇_j vs ε̇_creep.

[우리 해석] 4 는 3 의 *방향* 은 맞추지만 *크기* 는 못 맞춘다 (σ⋆ ∝ j^0.15 vs 실측 ≈ j^1). 겉보기 지수 ≈1 은 거듭제곱 (m 6.6) 공급보다 **응력에 1 차인 공급 (확산 크리프 · 공공 확산 꼴)** 과 더 닮았다. 또는 계면의 실효 응력이 적층압과 다르거나 (마찰 · 국소 접촉), 프로토콜의 누적 손상 (§10-③) 이 섞였다. 이 논문은 이 비교를 하지 않는다. 같은 흐름의 후속 — Krauskopf 의 공공 확산 한계 (ref 17) · Seymour & Aguadero 2021 ([`seymour2021_…`](seymour2021_void_suppression_interfacial_adhesion_vacancy_transport.md) · 점착 ↔ 알칼리 금속 공공 수송) — 이 이 빈칸을 다룬다.

**점착이 들어오는 자리** (논문 서술을 우리가 정리 · 정량 0):
- (가) **Li | 하중판 (기판)** 의 마찰 · 점착 → 배럴링 → 크리프 속도 10⁻³–10⁻⁴ 감쇠 → **공급을 늦춘다 (공극 쪽으로 민다).**
- (나) **Li | LLZO** 의 접촉 · 점착 회복 → 15 min 휴지로는 부족하다 (`Fig. 6`) → **회복 쪽 (공극을 줄이는 쪽).**
- ⇒ 같은 '점착' 이 자리에 따라 반대 방향으로 들어간다. 우리 W_ad 보고서 7 절이 Li 친화성을 W(Li | 표면) 로 정량하자고 할 때, **어느 계면의 W 인지** 를 먼저 적어야 하는 이유다.

---

## 7. 우리 계산과의 대조 ★ (`../our_dft_baseline.md` · `../our_dem_baseline.md` · `db/properties/`)

> 이 논문에는 우리 물성 4 축 (σ · 산화 · SE 기계 · 전자구조) 에 겹치는 값이 **없다** (LLZO · Li 금속 · 셀 전기화학). 우리 DFT · DEM 기준선 파일에도 Li|LLZO · Li 크리프 · 적층압-공극 양이 없다 (두 파일 검색 0 건 · 2026-11-24). 그래서 '같다 / 다르다' 판정이 아니라 **어디에 끼우는가** 를 적는다.

| 항목 | 이 논문 | 우리 | 차이 / 이유 |
|---|---|---|---|
| 계면 쌍 | Li \| LLZO (Ta · Al) | W_ad 쌍: LPSCl\|Ag(111) · LPSCl\|흑연 · Ag\|C · C\|C (값은 `db/properties/adhesion.json` · `db/properties/wad_*` — 위치만) · Li 금속이 한쪽인 쌍은 보고서 7 절의 **제안** 단계 | Li 금속 계면 계산은 우리에게 아직 없다 |
| 점착 양 | **측정 · 계산 없음** — 마찰 · 점착은 크리프 감쇠 10⁻⁴ 가정과 '접촉 회복' 서술로만 나온다 | 고정 기하 분리 에너지 (DFT · 0 K) | 같은 줄에 놓을 문헌 값이 없다 · W_ad ≠ G_c 전제 그대로 |
| 압력 | 운전 적층압 0–3.2 MPa · **하중 제어** | DEM 압밀 · 박리의 P (하중 제어) | 경계조건 종류는 같다 · 우리 DEM 에는 Li 금속 · 크리프 상이 없다 |
| Li 크리프 | `Table S1` 인용 (m 6.6 · Q 37 kJ mol⁻¹ · A 9e-41 감쇠 반영) | 없음 · `kang2026_stress_regulated…` 의 phase-field 는 Li 를 **Coble (선형, n = 1)** 점성으로 다룸 | 지수가 다르다 (6.6 vs 1) — 실측 σ_crit(j) 의 겉보기 지수 ≈1 은 오히려 선형 쪽과 닮았다 (§6) · 단 기하 (벌크 박 vs 기공) 가 다르다 |
| 계면 화학 | LLZO 는 Li 와 안정 (전제) | LPSCl 은 Li 와 반응 → Li₂S · Li₃P · LiCl (`comparison_vs_ours.md` §E · SEI 트랙) | LPSCl 로 옮기면 SEI 층이 공극 기전에 끼어든다 — '순수 기계' 결론은 LPSCl 에 그대로 가지 않는다 |
| 온도 | 상온 (미기재) | DFT 0 K · MLIP-MD 600–1000 K | 크리프의 T 의존 (Q 37 kJ mol⁻¹) 은 우리 쪽에 없다 |
| 박리 vs 석출 | 분극은 박리 쪽 (3-전극) | — | 모형 범위의 우선순위: 박리 계면 먼저 (LLZO 한정 근거) |

---

## 8. DFT/계산 방법 ★
**없다.** code · functional · pseudo · k-point · supercell · DFT+U · AIMD · MLIP · 무질서 처리 전부 **n/a**. 이론은 식 1–4 (해석식) 와 문헌 크리프 매개변수 (`Table S1`) 뿐이고, FEM · phase-field · DEM 같은 수치해석도 없다 (저자: *"detailed computational models would be necessary to accurately simulate the chemo-mechanical interactions at the Li stripping interface"*, p.2173).
⇒ 우리 W_ad (DFT) · DEM 이 이 논문의 '계면 역학 모형' 빈칸 쪽에 서는 관계다. 이 논문에서 계산 수치를 가져올 것은 없다 — 크리프 매개변수는 2 차 인용이라 원전 (LePage 2019 · Masias 2019) 을 봐야 한다.

---

## 9. Figure set ★

| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1 | Li WE \| LLZO \| Li CE 대칭셀을 하중 틀이 누르는 도식 · Li⁺ 위 → 아래 · 축척 3 mm (LLZO `figure-read ≈`1.45 mm) | 하중 제어 경계조건의 표준 그림 — DEM 박리 시험 설정을 설명할 때 대응 |
| 2 | 0.05 / 0.1 / 0.2 / 0.4 mA cm⁻² 단방향 박리 + 3.2 → 0.4 MPa 계단 · (E−E₀)/E₀ · 발산 ≈35.5 / 28.3 / 21.5 h · 논문 σ_crit 0.4 / 1.2 / 2.0 MPa | **σ_crit(j) 대조 표적** (LLZO) · ⚠ 발산 한 단 앞에 전조 · 0.4 mA cm⁻² 는 첫 단부터 상승 · 누적 박리 17–42 µm 와 교락 |
| 3A–C | 0.1 mA cm⁻² 압력 지그재그 2.4 ↔ 1.2 MPa · DC 진폭 +27 → +11 % · Nyquist (Bulk 0.8 MHz · GB 60 kHz · Int 170 Hz · ECR 0.1 Hz) · R_ECR 1.2 MPa ≈256 → 170 / 2.4 MPa ≈45 → 33 Ω cm² | 공극 없는 영역에서도 **압력 의존 계면 저항** 항이 필요하다는 근거 · ⚠ ECR 호는 일부만 측정 · 이름 R_int / R_ECR 혼용 |
| 4A–C | Ni 측면 기준전극 3-전극 도식 · D 자 빌릿 평면도 · Li–Ni 차단 / Li–Li 비차단 EIS (고주파 호 ≈400 Ω cm²) | 3-전극 설계 레시피 — 실험 협업에 제안할 때의 원형 |
| 5 | 0.2 mA cm⁻² · 3-전극 · E_WE − E_CE 0.1 → 8.2 V · E_WE −2.74 → +5.4 V · E_CE −2.82 V 평탄 | **분극 = 박리 쪽** 의 1 차 증거 → 모형은 박리 계면 먼저 (LLZO 한정) |
| 6 | 0.2 mA cm⁻² 양방향 · 반주기 0.35 mAh cm⁻² · 3.2 MPa 평탄 vs 0.4 MPa 반주기 끝 갈고리 +1.5 → ≈+9 mV (6 주기 이후 포화) | **σ_crit 은 반주기 용량에 의존** — 얕은 사이클은 단방향 σ_crit 보다 낮은 압력을 견딘다 |
| 7A,B | σ > σ_crit 밀착 / σ < σ_crit 박리 쪽 계면의 반구형 공극 도식 | 발표용 공극 도식 · ⚠ 관찰 아님 |
| 8 | ε̇_creep (원) vs ε̇_j (×, ≈1.7e-7 s⁻¹) vs Ȧ/A₀ (빨강 · 봉우리 ≈0.15 @ ≈37 h) · 0.1 mA cm⁻² | ⚠ **원 점은 한 단 위 압력의 값** (§5.11 재계산) · 모형 σ⋆ ∝ j^0.15 — '크리프 균형식' 을 연속체 입력으로 쓸 때의 반례 |
| S1 | Ta- vs Al-LLZO 0.2 mA cm⁻² — 둘 다 1.2 MPa 단에서 발산 (Al 이 ≈1.5–3 h 늦음) | 전해질 조성 무관 주장의 근거 (단 해상도 0.4 MPa · n = 1) |
| S2 | `Fig. 5` 확대 (−2.90 ~ −2.50 V) · Li vs Ni 개회로 2.78 V · WE +0.011 V (15 h) → +0.11 V (20 h) · CE −0.003 V | 박리 전극 분극이 ≈2 MPa 부터라는 근거 |
| Table S1 | 식 2–3 매개변수: M · ρ · F · l₀ 700 µm · A′ 7e-37 · A 9e-41 · m 6.6 · Q 37 kJ mol⁻¹ · R | **Li 크리프 입력값 (2 차 인용)** · ⚠ A 는 마찰 감쇠 10⁻⁴ 를 곱한 모형 매개변수 · T 미기재 |

---

## 10. 비판 — 이 논문의 약한 곳 ★

① **`Fig. 8` 의 크리프 점은 아래 축 라벨보다 한 단 위 압력의 값이고, 본문은 그 그림을 전류마다 다르게 읽었다.** 근거 넷은 §5.11. 0.1 mA cm⁻² 의 '0.4 MPa 에서 모형 = 실측' 은 라벨로 읽어야 나오고, 0.4 mA cm⁻² 의 '1.2 MPa 까지 ε̇_j 가 못 이긴다' 는 실제 σ 로 읽어야 나온다. 한 방식 (실제 σ) 으로 읽으면 네 전류 중 '일치' 는 0.2 mA cm⁻² 하나이고, 0.1 은 '한 단 안' 수준이다.

② **모형의 전류 의존이 실측과 자릿수로 다르다.** σ⋆ ∝ j^(1/m) = j^0.15 → 0.05–0.4 mA cm⁻² 에서 0.97–1.33 MPa (✎) · 실측 σ_crit 은 판정 기준과 무관하게 ≈ j^(0.8–1.2). 본문은 0.4 mA cm⁻² 에서만 불일치를 인정하고 '낮은 전류에서는 충분할 수 있다' 고 쓰지만, 0.05 에서도 모형은 0.8 MPa 단의 공극을 말하는데 실측은 0.4 MPa 단 끝까지 거의 평탄하다. 게다가 σ⋆ 를 정하는 것은 물성이 아니라 감쇠 가정이다 (10⁻⁴ vs 10⁻³ 에서 σ⋆ 27 % 차 · 감쇠 없이는 0.28 MPa).

③ **프로토콜이 압력과 시간 · 누적 박리량을 같이 움직인다.** 모든 셀이 3.2 MPa 에서 시작해 내려가므로, 낮은 압력 단에 닿을 때 이미 벗겨진 Li 가 셀마다 다르다 (발산 시점 ≈17 / 27 / 42 µm — ✎). 공극은 누적 손상이라 (`Fig. 6` 이 주기 의존을 보여준다) σ_crit 은 'j 만의 함수' 가 아니다. 압력 순서를 바꾼 대조 · 한 압력에 오래 둔 대조가 없다.

④ **임계압 판정이 정성적이고, 전류마다 기준이 다르게 읽힌다.** *"Loosely defining"* · 0.1 · 0.2 는 발산 단 · 0.4 는 큰 상승 단 (발산은 1.6 MPa). 모든 곡선에 한 단짜리 전조가 있다. 분해능 0.4 MPa 는 0.1 mA cm⁻² 의 0.4 MPa 에 대해 **100 %** 다.

⑤ **n = 1.** 조건마다 셀 하나 · 오차막대 · 반복 셀 없음. Ta vs Al (`Fig. S1`) 도 셀 하나씩이고, 같은 단 안에서 1.5–3 h 차가 난다.

⑥ **EIS 서술이 서로 맞지 않는다.** 방법은 RC 셋 (벌크 · 입계 · 계면) 인데 `Fig. 3B` 표지는 넷 (Bulk · GB · Int · ECR) · `Fig. 3C` 캡션은 'R_int' 인데 세로축은 'R_ECR' · 방법의 주파수 하한은 1 Hz 인데 inset 표지는 0.1 Hz · inset 에서 1.2 MPa 의 ECR 호는 앞부분 (실축 ≈35 Ω cm² 너비) 만 보이는데 R_ECR 은 ≈250 Ω cm² — **값의 대부분이 외삽이다.** 특성 정전용량 '≈10⁻³ F' 는 면적 정규화 여부를 안 적었다.

⑦ **DC 와 EIS 크기가 같은 셀이라면 맞지 않는다.** `Fig. 3A` 시작 E_we ≈0.028 V @ 0.1 mA cm⁻² → R_DC ≈280 Ω cm² (✎) 인데 `Fig. 3B` 는 ECR 앞까지만 ≈333 Ω cm² 다. 직류 전압이 교류 고주파 저항보다 작을 수는 없다 — B 가 A 와 같은 셀인지 논문이 밝히지 않는다. `Fig. 4C` 도 두께 5.7 mm (1.3 mm 의 4.4 배) 인데 고주파 호는 ≈400 Ω cm² (1.2 배) — 겉보기 σ 1.4 vs 0.39 mS cm⁻¹ (✎). 면적 정규화나 전류 경로가 다를 수 있으나 설명이 없다.

⑧ **Ȧ/A₀ 는 유도식이 없고 단위가 자릿수상 이상하다.** 전위 → 면적 환산식이 없다. 축 단위 s⁻¹ 을 문자 그대로 읽으면 봉우리 ≈0.15 s⁻¹ = 초당 접촉 면적 15 % 상실이라, 몇 초 만에 접촉이 사라져야 한다 — `Fig. 2` 의 발산 시간 척도 (≈0.5 h) 와 맞지 않는다. 정성 지표 (언제 오르기 시작하나) 로만 읽는다.

⑨ **방법 ↔ 그림 어긋남 셋.** 압력 사이클 단 2 h (방법) vs `figure-read ≈`2.5 h (`Fig. 3A`) · `Fig. 6` 캡션의 '0.35 mA cm⁻²' 는 0.35 mAh cm⁻² 의 오기 · '9 V 까지' (본문) vs `Fig. 5` 에 그려진 최대 ≈8.2 V.

⑩ **필라멘트 개시를 'CE 의 절대 전위' 로 일반화한 것은 과잉이다.** 근거는 '9 V 에서 단락 없음' 이라는 음성 관찰 하나 (셀 하나 · 0.2 mA cm⁻² · 석출 과전압 ≈−35 mV). 박리 쪽 공극이 다음 석출의 전류 집중을 만든다는 본문 자신의 함의 (p.2175) 와도 긴장이 있다.

⑪ **공극을 보지 않았다.** 공극은 전위 · EIS · 압력 가역성에서 추론했다 — 단면 SEM · XCT · operando 영상이 없다. `Fig. 7` 은 도식이다. '임계압 위에서는 면적 변화가 없다' 는 판단도 고주파 불변 하나에 기대는데 (전류 수축 이론과 양립하지만 직접 증거는 아니다), 바로 그 영역에서 R_ECR 이 5 배 움직인다.

⑫ **기하 의존이 모형에 숨어 있다.** ε̇_j = v/l₀ 라서 같은 j 에서도 Li 가 얇으면 ε̇_j 가 커지고 σ⋆ 가 오른다 (l₀ 비의 1/6.6 제곱). 실제 공급은 박의 반지름/두께 비와 마찰 조건에 달려 있는데 모형에 없다. 실용 두께의 Li (10–30 µm) 로 옮길 때 이 식을 그대로 쓰면 안 된다 (같은 그룹의 얇은 Li 실측: [`lee2022_thin_insitu_li_void_rewetting_llzo`](lee2022_thin_insitu_li_void_rewetting_llzo.md)).

⑬ **온도 미기재.** 크리프 계산의 T 를 안 적었다 (우리 재계산 298 K 에서 그림 점과 15 % 안에서 맞는다 → 상온으로 보인다). σ⋆ 에 주는 영향은 ±3 % (295–303 K) 로 작다.

---

## 11. 우리 원장 매핑 (요약표)

| 항목 | 이 논문 (exp · 소환값 · LLZO) | 우리 | 판정 |
|---|---|---|---|
| σ_crit(j) | 0.4 / 1.2 / 2.0 MPa @ 0.1 / 0.2 / 0.4 mA cm⁻² | 없음 | 연속체 · DEM 의 **대조 표적** (보정 표적 아님) |
| 분극 위치 | 박리 전극 (3-전극) | 없음 | 모형 범위를 정하는 근거 (LLZO) |
| 압력 의존 계면 저항 (공극 없는 영역) | R_ECR ≈5 배 (2.4 ↔ 1.2 MPa · `figure-read`) | 없음 | 계면 저항 항의 P 의존이 필요하다는 근거 (정량은 약함) |
| Li 크리프 | m 6.6 · Q 37 kJ mol⁻¹ · A 9e-41 (감쇠 반영) | 없음 · `kang2026_stress_regulated…` 는 Coble n = 1 | 원전 (LePage · Masias) 을 확인한 뒤에 입력 |
| 점착 | 정성 (마찰 감쇠 · 접촉 회복) | W_ad (위치: `db/properties/adhesion.json` · `db/properties/wad_*`) | 같은 줄 금지 · 연결은 개념뿐 |

---

## 12. 적용 인사이트 ★

① **W_ad 보고서 7 절 (Li 친화성 · 점착과 공극) 에는 '방향' 만 준다.** 이 논문은 점착을 재지 않는다. 쓸 수 있는 것은 "공극은 박리 쪽에서, Li 공급 (크리프) 이 박리를 못 따라갈 때 생기고, 점착은 (가) Li | 기판 마찰로 공급을 늦추고 (나) Li | SE 접촉 회복을 돕는다" 는 틀이다. 7 절이 W(Li | 표면) → Young–Dupré 젖음각을 제안할 때, **그 W 가 SE 쪽 (회복) 인지 집전체 · 하중면 쪽 (마찰) 인지** 를 먼저 적어야 한다. 정량 연결은 이 논문의 ref [10] (Wang & Sakamoto 2018 — R_int ↔ 표면 점착) 과 Seymour & Aguadero 2021 ([`seymour2021_…`](seymour2021_void_suppression_interfacial_adhesion_vacancy_transport.md) — W ≥ 2σ_m 일 때만 공공이 계면에 안 남는다는 이론 · 그 카드 요약) 이 할 일이다.

② **연속체 · DEM 입력으로 σ_crit(j) 표를 쓸 때는 세 단서를 같이 싣는다**: LLZO · 단 0.4 MPa · 단방향 5 h 단 (누적 박리 17–42 µm). 그리고 **크리프 균형식 (m 6.6) 으로는 이 표의 전류 의존을 재현할 수 없다** — 맞추려면 겉보기 지수 ≈1 의 공급 (선형 크리프 · 공공 확산) 이나 국소 응력 집중이 필요하다. 이것은 우리 모형이 '맞춰야 할 것' 이 아니라 '설명해야 할 것' 이다 (frame[4]).

③ **얕은 사이클은 단방향 임계압보다 낮은 압력을 견딘다** (`Fig. 6`: 임계압의 ⅓ 에서 평탄부 +33 % 분극에 포화). 운전 프로토콜 (반주기 용량) 이 임계압의 변수다. 우리 Ag–C 층 셀 조건으로 이 수치를 옮기지 않고, '반주기 용량 × 적층압' 2 차원으로 물어야 한다는 근거로만 쓴다.

④ **LPSCl 로 옮길 때는 화학이 끼어든다.** LLZO 는 Li 와 안정해서 '공극 = 순수 역학' 이 성립했다. LPSCl | Li 는 SEI (Li₂S · Li₃P · LiCl) 가 자라서 접촉 · 점착 · 저항이 시간에 따라 바뀐다. LPSCl 대응 실측인 Kasemchainan 2019 (*Nat. Mater.* 18, 1105 — 3 MPa 에서 임계 박리 전류 0.2 mA cm⁻² · 7 MPa 에서 1.0 · `deysher2022` digest 의 인용값) 을 먹이는 것이 다음 순서다. 같은 날 들어온 [`shi2026_argyrodite_stack_pressure_viscoplastic_deformation`](shi2026_argyrodite_stack_pressure_viscoplastic_deformation.md) 이 LPSCl | Li 에서 **적층압 + 영전류 유지 시간** 을 축으로 공극 닫힘을 직접 본다 — 이 논문의 '압력 · 시간 교락' (§10-③) 을 LPSCl 에서 푸는 짝이다.

---

## 13. 인용 가능 문장 (영문 초안 · 랩 표기 *Joule*, 3, 2165 (2019).)

- "In symmetric Li|garnet (Ta-doped Li₇La₃Zr₂O₁₂) cells held under load-controlled stack pressure, rapid polarization during unidirectional stripping occurred at higher stack pressures as the current density increased (0.4, 1.2, and 2.0 MPa at 0.1, 0.2, and 0.4 mA cm⁻², respectively, resolved in 0.4 MPa steps)." — *Joule*, 3, 2165 (2019).
- "With a Ni reference electrode, the polarization was attributed to the stripping electrode, whereas the potential of the plating electrode remained essentially unchanged." — *Joule*, 3, 2165 (2019).
- "The authors attributed this polarization to interfacial voids that form when pressure-driven creep of Li cannot replenish the Li removed by stripping." — *Joule*, 3, 2165 (2019).
- ⛔ 쓰지 않는다: "The creep-balance model predicts the critical stack pressure." (§10-① · ②)

(BML 시제: 실험 행위 · 관찰 결과 = 과거 · 그림 서술 = 현재.)

---

## 14. 주의 / 한계 (인용 규율)

- ⛔ **LLZO 계 값을 LPSCl 로 옮기지 않는다** — LPSCl 은 Li 와 반응한다 (SEI).
- ⛔ **σ_crit 0.4 / 1.2 / 2.0 MPa** 는 '0.4 MPa 단 · 정성 판정 · n = 1 · 단방향 5 h 단 · 750 µm Li · 170 °C 열처리 계면 · 상온' 조건부다. 발산 한 단 앞에 전조가 있다는 것을 같이 적는다.
- ⛔ **`Fig. 8` 의 '0.4 MPa 에서 모형 일치' 를 인용하지 않는다** (축 밀림 · 혼용 읽기).
- ⛔ **A = 9 × 10⁻⁴¹ 은 Li 물성이 아니다** — 마찰 · 배럴링 감쇠 10⁻⁴ 를 곱한 모형 매개변수다. 크리프 물성은 원전 (LePage 2019 · Masias 2019) 에서 가져온다.
- ⛔ **R_ECR 값은 `figure-read` 이고 외삽 비중이 크다** — 정량 입력으로 쓰지 않는다.
- ⛔ **Ȧ/A₀ 를 면적 손실 속도로 인용하지 않는다** (유도식 없음 · 단위 의문).
- ⚠ frame[4]: 문헌 값은 대조 표적이지 보정 표적이 아니다.
- ⚠ 우리 W_ad 와 같은 줄에 놓지 않는다 — 이 논문에는 점착 정량값이 없다 (우리 값 위치: `db/properties/adhesion.json` · `db/properties/wad_*`).
- ⚠ '임계 적층압' · 'CCD (임계 전류 밀도)' · '임계 박리 전류' 는 다른 양이다 — 이 논문은 전류를 고정하고 압력을 내렸다.

## 15. 기법 용어 미니사전

- **적층압 (stack pressure)**: 셀을 운전하는 동안 위아래로 누르는 압력. 제조압 (펠릿 성형 · 전극 압착) 과 다르다. 이 논문은 0–3.2 MPa.
- **하중 제어 vs 간극 제어**: 하중을 고정하면 셀 두께가 바뀌어도 압력이 유지된다 (이 논문 · 우리 DEM). 간극을 고정하면 압력이 셀의 부피 변화를 따라 출력으로 움직인다 (볼트 지그).
- **대칭셀 · WE / CE / RE**: 같은 Li 두 장. 한쪽에서 벗기고 (박리 · stripping) 다른 쪽에 쌓는다 (석출 · plating). 두 전극만 재면 둘의 합만 보인다 → 기준전극 (RE) 을 넣어 각각의 전위를 본다.
- **차단 전극 (blocking electrode)**: 이온이 반응하지 않는 전극 (여기서는 Ni — Li 와 합금하지 않는다). 전류는 안 받고 전위만 감지하는 의사 기준전극으로 쓴다.
- **EIS · Nyquist 그림**: 작은 교류로 주파수를 훑어 저항 성분을 나눈다. 높은 주파수 = 벌크 · 입계, 낮은 주파수 = 계면 · 반응. 호의 특성 정전용량 크기로 어느 과정인지 분류한다 (Irvine 1990: 벌크 ≈10⁻¹² · 입계 ≈10⁻¹¹–10⁻⁸ · 시료–전극 계면 ≈10⁻⁷–10⁻⁵ · 전기화학 반응 ≈10⁻⁴ F 급).
- **CPE (constant phase element)**: 이상적 커패시터 대신 쓰는 '찌그러진 반원' 원소. 시간 상수가 분포할 때 쓴다.
- **operando EIS**: 직류를 흘리는 중에 교류를 얹어 잰다 — 사이클 중인 계면을 그대로 본다.
- **Kirkendall 공극**: 확산 플럭스가 비대칭일 때 빈자리가 모여 생기는 공극. 여기서는 Li 가 계면에서 빠져나가는 속도 > 채워지는 속도일 때.
- **거듭제곱 크리프 (power-law creep)**: ε̇ = Aσ^m exp(−Q/RT). m 이 크면 (6.6) 응력이 조금만 줄어도 속도가 크게 준다 (σ 가 절반이면 1/97). 전위 상승 (dislocation climb) 이 지배. m = 1 이면 확산 크리프 (Nabarro–Herring · Coble) — 응력에 비례.
- **상동온도 (homologous temperature)**: T/T_m. Li 는 상온에서 ≈0.66 → 크리프가 활발하다.
- **배럴링 (barreling)**: 원기둥을 누를 때 위아래 면이 판에 붙잡혀 (마찰 · 점착) 가운데가 불룩해지는 것. 겉보기 변형률 속도를 떨어뜨린다.
- **전류 수축 (current constriction)**: 접촉이 점으로 줄면 전류가 그 점에 모여 전해질 쪽 저항이 커진다 — 공극의 전기적 서명. 이 논문은 '면적이 줄면 고주파에도 보여야 한다' 는 논리로 썼다.
- **임계 전류 밀도 (CCD) / 임계 박리 전류 / 임계 적층압**: 전류를 올려 단락까지 · 박리 쪽 분극 폭주까지 · 압력을 내려 분극 폭주까지. 고정하는 변수가 다르다.

---

## 16. 참고문헌 중 먹일 만한 것 (litdb 상태 2026-11-24)

| ref | 서지 (이 논문 참고문헌 그대로) | 왜 | litdb |
|---|---|---|---|
| [10] | Wang, M., and Sakamoto, J., *J. Power Sources* 377, 7–11 (2018) — "Correlating the interface resistance and surface adhesion of the Li metal-solid electrolyte interface" | R_int ↔ 점착 — W_ad 보고서 7 절에 바로 닿는다 | 카드 없음 (`banerjee2020` 이 인용만) |
| [27] | LePage, W.S. et al., *J. Electrochem. Soc.* 166, A89–A97 (2019) — "Lithium mechanics: roles of strain rate and temperature and implications for lithium metal batteries" | `Table S1` 의 A′ · m · Q 원전 | 카드 없음 (리뷰 카드 셋이 인용) |
| [26] | Masias, A. et al., *J. Mater. Sci.* 54, 2585–2600 (2019) — "Elastic, plastic, and creep mechanical properties of lithium metal" | 배럴링 감쇠 10⁻³–10⁻⁴ · m 6.6 의 원전 | ✅ 카드 있음 — [`masias2019_li_metal_elastic_plastic_creep_properties`](masias2019_li_metal_elastic_plastic_creep_properties.md) (같은 날 묶음) |
| [17] | Krauskopf, T., Hartmann, H., Zeier, W.G., and Janek, J., *ACS Appl. Mater. Interfaces* 11, 14463–14477 (2019) | 공공 확산 한계 · 압력 — '선형 공급' 후보 | 카드 없음 |
| [16] | Koshikawa, H. et al., *J. Power Sources* 376, 147–151 (2018) | 용해 중 R_ct 의 동적 변화 (공극 가설 원전) | 카드 없음 |
| [3] | Wang, M., Wolfenstine, J.B., and Sakamoto, J., *Electrochim. Acta* 296, 842–847 (2019) — "Temperature dependent flux balance of the Li/Li7La3Zr2O12 interface" | 같은 플럭스 균형의 온도 축 | 카드 없음 |
| [25] | Fu, K. et al., *Sci. Adv.* 3, e1601659 (2017) | Li \| 가넷 인터레이어 (높은 전류 · 낮은 압력) | 카드 없음 |
| [28] | Cannarella, J., and Arnold, C.B., *J. Power Sources* 245, 745–751 (2014) | Li-ion 적층압 0.1–1 MPa 의 출처 | 카드 없음 |
