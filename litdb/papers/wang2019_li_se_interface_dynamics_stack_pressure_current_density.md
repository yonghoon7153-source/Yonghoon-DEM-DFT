<!-- digest 표준 양식 (paper-level STANDALONE). 깊이 기준 = papers/zuo2022_chlorination_cathode_interface.md
     2026-11-24 신규 (litdb-curator · 병렬 인입 한 편 · 공유 파일 (INDEX · comparison) 은 메인 세션이 합친다).
     ① 그림: 자동 추출 11 장 (본문 Fig. 1–8 · SI Fig. S1 · S2 · Table S1) — 놓친 그림 0.
        도구의 '번호 공백' S3–S8 은 오탐 (SI 글의 'in Figure 5' · 'in Figure 8' 을 S5 · S8 로 읽음) → figures.json missing_labels 에 not_cropped 사유.
        그림 10 장 전부 실독 (Fig. 2 · Fig. 6 은 확대 크롭으로 한 번 더). Table S1 은 PDF 글자로 읽었다 (tab_S1.png 는 이미지로 안 봄).
     ② 값 표지: 본문 숫자는 그대로 (쪽 병기) · 그림에서만 읽은 값 = 'figure-read ≈' · 우리가 계산한 값 = '✎ 우리 산술' · 해석 = '[우리 해석]'.
        판독 · 재계산 129 행 = litdb/figures/<slug>/digitized.csv (축 눈금 · 식 · 가정이 note 열에).
     ③ 핵심 발견: Fig. 8 의 크리프 점은 아래 축 라벨보다 한 단 위 압력의 값이다 (Table S1 로 재계산 · 이웃 점 비 검산은 T 무관) →
        본문의 '0.4 MPa 에서 모형 = 실측' 은 라벨 읽기에서 나온 일치다 (5.11 · 10-①). 모형의 전류 의존 (σ* ∝ j^0.15) 은 실측 (≈ j^1) 과 자릿수가 다르다 (10-②).
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

- 식: 전류 변형률 **ε̇_j = Δl̇ / l₀ = jM/(ρFl₀)** (식 2) · 크리프 변형률 **ε̇_creep = Aσ^m exp(−Q/RT)** (식 3) · 공극 조건 **ε̇_j > ε̇_creep** (식 4) · 접촉 면적 ↔ 저항 **R = ρl/A** (식 1).
- A/A′ = 1.29 × 10⁻⁴ — 본문 *"assuming a decay of ~10⁻⁴ due to frictional and adhesive forces at the interface"*. 근거는 Masias: 일정 응력 압축에서 Li 원기둥이 기판과의 마찰 · 점착 때문에 배럴링하고, 5 h 뒤 변형률 속도가 10⁻³–10⁻⁴ 배로 준다.
- **✎ 우리 재계산 (T = 298 K 가정 — 논문은 T 를 안 적었다)**:

| j (mA cm⁻²) | ε̇_j (s⁻¹) | σ* 교차압 (A = 9e-41) | σ* (A′ · 감쇠 없음) | σ* (감쇠 10⁻³) | 모형상 첫 미달 단 (실제 σ 기준) | 논문 판정 σ_crit |
|---|---|---|---|---|---|---|
| 0.05 | 9.6 × 10⁻⁸ | **0.97 MPa** | 0.25 | 0.71 | 0.8 MPa | — (폭주 없음) |
| 0.1 | 1.9 × 10⁻⁷ | **1.08** | 0.28 | 0.79 | 0.8 | 0.4 |
| 0.2 | 3.8 × 10⁻⁷ | **1.20** | 0.31 | 0.88 | 1.2 (경계 — 두 값 차 0.5 %) · 확실히는 0.8 | 1.2 |
| 0.4 | 7.7 × 10⁻⁷ | **1.33** | 0.34 | 0.98 | 1.2 | 2.0 |

  - σ* = (ε̇_j / (A e^(−Q/RT)))^(1/m) ∝ **j^0.15** — 이 전류 범위에서 모형은 사실상 '전류와 거의 무관한 ≈1 MPa' 를 말한다. T 를 295–303 K 로 바꿔도 σ* 는 ±3 % 만 움직인다. 반면 감쇠 가정 (1 → 10⁻³ → 10⁻⁴) 은 σ* 를 0.28 → 0.79 → 1.08 MPa (0.1 mA cm⁻²) 로 바꾼다 — **모형 예측을 정하는 것은 Li 물성이 아니라 감쇠 가정이다.**
  - 감쇠 없는 A′ 로는 3.2 MPa 에서 ε̇_creep ≈ **2 s⁻¹** (✎) — Li 박이 몇 초에 납작해지는 속도라 그대로는 못 쓴다.
  - 실측 σ_crit 의 전류 지수 (✎ log-log 기울기): 논문 값 (0.4 · 1.2 · 2.0) → **n ≈ 1.16** (0.1 → 0.4) · 발산 단 (0.4 · 1.2 · 1.6) → 1.0 · 상승 시작 단 (0.8 · 1.6 · 2.4–3.2) → 0.8–1.0. **어느 기준으로 읽어도 ≈ j^1 이고, 모형의 j^0.15 와 자릿수가 다르다.**

### 3g. 홉 수 검산 (CLAUDE.md 규율 — 차수 검산이지 크리프 속도가 아니다)

Q = 37 kJ mol⁻¹ = **0.383 eV** · T = 298 K (가정) · ν₀ = 10¹³ s⁻¹ (가정) → Γ = ν₀ e^(−Q/kT) ≈ **3 × 10⁶ s⁻¹** · 평균 대기 ≈ **0.3 µs** · 5 h 단 (1.8 × 10⁴ s) 동안 N ≈ 6 × 10¹⁰. → Q 자체는 상온에서 빠른 열활성 과정이다. 공급을 '느리게' 만드는 것은 σ^6.6 의 낮은 응력 쪽 급감 (0.8 → 0.4 MPa 에서 97 배) 과 마찰 감쇠 (10⁻⁴) 이지 Q 가 아니다 — 논문 서술과 차수상 충돌은 없다. ✎ Li 의 상동온도 T/T_m = 298/453.7 ≈ 0.66 (상온에서 크리프가 활발한 이유 · 논문은 '상동온도 차이' 라고만 쓴다).

---
