---
title: "Miß, Ramanayagam, Roling 2022 — Which Exchange Current Densities Can Be Achieved in Composite Cathodes of Bulk-Type All-Solid-State Batteries? A Comparative Case Study (ACS Appl. Mater. Interfaces 14, 38246-38254)"
source_url: local-upload/12._Which_exchange_current_densities_can_be_achieved_in_composite_cathodes_of_bulk-type_all-solid-state_batteries_A_comparative_case_study.pdf + 12._Sup_Which_exchange_current_densities_can_be_achieved_in_composite_cathodes_of_bulk-type_all-solid-state_batteries_A_comparative_case_study.pdf (SI)
source_url_note: "본문 9 쪽(참고문헌 52 편) + SI 8 쪽(그림 S1-S7 · 표 S1). 크로퍼가 본문 8 + SI 7 = 15 장(+ 표 4)을 잡았고 12 장 봤다(Fig. 2-8 · S2 · S3 · S5 · S6 · S7). 식 (1)-(7)은 쪽 렌더로 확인. 원자료는 커밋하지 않는다. 16호(Ramanayagam 2026) ref [30]."
source_doi: 10.1021/acsami.2c06460
source_license: "'© 2022 The Authors. Published by American Chemical Society' (라이선스 종류는 추출 텍스트에 없음)"
pdf_sha256: 9490cf469451f7b7b2c87829914b5a5155b9698a9a14d6f1a0b4c7b43029ff99
si_sha256: 6478b2937c032a969081b6998b3e4a55229d33e0e4f11a86c03ccd96d2783964
ingested: 2026-09-23
sha256: 894757eb3373d2af9588fae41f4249f986b620b2068ee5726bde31640932267c
---

# 수집 목적

`assb` 섹션 **50호**. 큐 **51번** — 2차 묶음(큐 40~59, 원장 §1 상단 순서)의 **열두째 편** (`bms-balancing/docs/ASSB_TRANSFER_NOTE.md` §6-3-g).
닻은 `questions/assb-contact-loss-vs-lampe.md`. 원장(`bms-balancing/docs/ASSB_WANTED_PAPERS.md`) 행: "**TLM(전송선 모델) 원본** — 16호의 곱 축퇴 실측 표본이 기대는 모형".
16호(Ramanayagam et al. 2026, ref [30])가 **방법의 원본**으로 인용한 편 — 두께 가변 TLM · 교환전류밀도 `j₀` · 초기값 · `r_CAM = 2.5 µm` 가 여기서 왔다고 16호 digest 가 적었다.
이 digest 의 1순위 물음: **`j₀` 를 `R_CT` 에서 뽑을 때 면적을 무엇으로 넣었나 — 두께 가변 TLM 이 면적과 `j₀` 를 가르는가.**

Vanessa Miß, Asvitha Ramanayagam, **Bernhard Roling**(교신) —
**"Which Exchange Current Densities Can Be Achieved in Composite Cathodes of Bulk-Type All-Solid-State Batteries? A Comparative Case Study"**,
*ACS Appl. Mater. Interfaces* **2022**, **14**, 38246–38254, doi `10.1021/acsami.2c06460`.
`[인쇄]` 접수 2022-04-12 · 수리 2022-08-03 · 게재 2022-08-15. `[인쇄]` "© 2022 The Authors. Published by American Chemical Society" (라이선스 종류는 추출 텍스트에 없음).
소속: Philipps-Universität Marburg 화학과(세 저자 모두). 경쟁 이해 없음. 사사: NMC 코팅(Marvin Cronau). 자금 문장 없음.

본문 PDF **9 쪽**(본문 7 + 참고문헌 52 편) · SI PDF **8 쪽**(그림 S1–S7 · 표 S1 · 참고문헌 4). sha256 은 frontmatter(본문 `pdf_sha256` · SI `si_sha256`). 원자료는 커밋하지 않는다.

> ⚠ **표기**: `[인쇄]` = 지면에 문자 그대로 있는 것 · `[도표]` = 그림을 열어 눈으로 읽은 값(figure-read ≈) ·
> `[재현]` = 지면의 수치로 이 위키가 다시 계산한 것 · `[해석]`/`[추론]` = 이 위키의 해석. 표시가 없는 서술은 원문이 실제로 말한 것이다.
> ⚠ 식 (1)–(7)은 pymupdf 추출에서 글자 조각으로 흩어진다 — **쪽을 렌더링해 눈으로 읽었다**(p4 식 1–3 · p5 식 6–7 · p5 두 극한식).

---

# 판정 (먼저)

> ★★★★ **면적과 `j₀` 를 가르지 않았다. 면적은 완전구 기하 면적으로 넣었고(접촉 분율 ≡ 1), 두께 가변은 `R_ion` 과 `R_CT/(a_v d)` 를 가를 뿐 `a_v` 와 `j₀` 를 가르지 못한다.**
>
> **(a) 식.** `[인쇄]` "The active area of the CAM particles **in contact to SE** normalized by the cathode volume is given by `a_v = (ε_CAM·A_CAM)/V_CAM = (3ε_CAM)/r_CAM`" · `[인쇄]` 식 (5) `R_CT = RT/(F·j₀)`.
> 모든 스펙트럼은 식 (7)의 `Z_loc/(a_v·d)` 로만 계면을 본다 ⇒ `[해석]` 데이터가 정하는 것은 **`j₀·a_v = 3·j₀·ε_CAM/r_CAM`**(그리고 `Q_DL·a_v`)이고, `j₀` 는 `a_v` 를 **기하로 고정**한 뒤의 나머지다.
> **16호가 옮긴 "접촉 면적" 이름 붙은 `a_v = 3ε/r` 문장의 출생지가 여기다** — 16호의 "in contact with the SE" 는 이 편의 "in contact to SE" 다.
>
> **(b) 면적은 무엇으로 넣었나.** 기하 면적 = `r_CAM` 과 `ε_CAM`. **BET 0 · 영상 접촉 분율 0.** `r_CAM = 2.5 µm` 는 `[인쇄]` "determined by SEM imaging of the purchased CAM powder as well as by SEM/EDX imaging … in focused ion beam-generated cross sections … in good agreement with the values provided by the suppliers" — **SEM 으로 공급자 공칭값(LCO 지름 5 µm · NMC 3–6 µm)을 확인한 것**이고 입자 수 · 분포 · 평균 계산법은 인쇄되지 않았다. `ε_CAM` 은 질량비 · 밀도에서 계산(SI 식 S1), **공극을 뺀 두 상의 비**(0.495 + 0.505 = 1.000).
> FIB-SEM/EDX 단면(Co · Ni · Mn · P · S 지도)이 **접촉을 볼 재료로 지면에 있는데 반경에만 썼다**.
>
> **(c) 저자의 틀에서 `j₀` 는 정의상 접촉을 품는다.** `[인쇄]` 초록 "These contacts determine the Li⁺ exchange current density at the CAM | SE interfaces" · 결론 "the influence of stack pressure on the achievable exchange current density should be studied" — **압력(접촉)이 `j₀` 를 바꾼다는 틀**이다. `[해석]` 이 편의 `j₀` 는 **기하 면적당 유효 교환전류밀도** = `j₀^true × (접촉 분율)` 이고, 저자도 그 뜻으로 쓴다 — 곱을 모르고 밟은 것이 아니라 **곱 전체에 `j₀` 라는 이름을 붙였다**.
>
> **(d) ★★★★ 면적 규약 자체가 모형 수정 하나로 바뀐다 — 값이 정확히 τ 배 움직이는 선택.** `[인쇄]` 수정 (ii): 원래 TLM(식 1)의 계면 면적 인자 `a_v·l_SE = a_v·τ·d` 를 "the interfacial CAM | SE area normalized by the nominal cathode area should be better described by `a_v·d`" 로 바꿨다(식 7). 근거는 **기하 논증**("mapping the 3D morphology … on 1D pores") + "for improving the agreement".
> `[재현]` 식 (1)의 모든 계면 항은 `Z_loc/(a_v·ℓ)` 로만 들어가므로 `ℓ = τd ↔ d` 교체는 **`(j₀, Q_DL, dU/dc) → (j₀/τ, Q_DL/τ, τ·dU/dc)` 와 정확히 같은 스펙트럼**을 준다. 즉 식 (1)을 그대로 썼다면 **LCO `j₀` 25.8 → 4.2 A m⁻² · NMC 0.11 → 0.016 A m⁻²**. 저자는 이 대수를 인쇄하지 않았다.
>
> **비교의 유효성**: (i) **LCO ↔ NMC(같은 지면)** — 두 재료가 같은 규약(`r_CAM` 2.5 µm · 수정 (ii) · 같은 SE · 같은 압력)이라 **비(×235)는 규약에 무관**하고, `[재현]` 1단계 R·C 로 보면 `C_eff` 비 ×2.2(Brug) · τ_CT 비 ×106 — **면적 서명이 아니다**(면적이 설명할 수 있는 몫은 많아야 ×2.2, `Q_DL` 원값으로 ×10). **비교는 면적 반론을 견딘다 — `C ∝ θ` 전제 위에서.** 단 코팅(구입 LCO ≈12 nm LiNbO₃ ↔ 자체 졸–겔 NMC 1 wt%) · NMC 전용 고주파 호의 배정(아래) · LCO 가 두께 전 구간 두꺼운 극한이라는 점이 남는다.
> (ii) **액체 문헌값과의 비교**("almost 2 orders of magnitude higher") — 문헌값의 면적 규약이 지면에 없고, 이 편 값의 ×6.1 이 수정 (ii)에서 온다(`[재현]` 식 (1)이면 ×10.6). **방향은 서되 자릿수는 규약 선택에 걸린다.**
> (iii) **16호의 편 간 비교**("about one order of magnitude higher than [30]" → "교환전류밀도가 SE 이온전도도와 함께 오른다") — `[재현]` 같은 NMC 분말 · 같은 코팅 처방 · 같은 389 MPa · 같은 `r_CAM`/`ε` 규약에서 `1/R_CT` ×12.1 ↔ `Q_DL` ×13.5 · `C_eff` ×15.4 ⇒ **τ_CT ×1.28 — 면적 서명**. 16호의 "SE 전도도 → `j₀`" 는 R·C 로는 **접촉 면적 차이와 구별되지 않는다**(전제 `C ∝ θ` 가 **다른 SE 사이**에서 서야 한다 — 약하다).
>
> **Q2**: 두께 가변이 이온 수송(`R_ion ∝ d`)과 전하이동(`R_CT/(a_v d) ∝ 1/d`)을 가른다 — **`[인쇄]` 방법 명제이고 NMC 에서만 실제로 작동한다**(두께 31 → 221 µm 가 `R_ion/(R_CT/a_v d)` 0.45 → 23 으로 전이 구간을 가로지른다). **LCO 는 네 두께 전부 두꺼운 극한**(`[재현]` 비 92 → 4,300) — `[인쇄]` 극한식 `R_semicircle ≈ √(R_CT·R_ion/(a_v d))` 만 보이고, 이것은 **`j₀·a_v/τ` 한 조합**이다. `[인쇄]` TLM 은 두께 무관 반원을 예측하는데 실험은 두께와 함께 줄어든다 — "The origin of this discrepancy … is unclear at present". 그래도 `j₀` = 25.8 을 보고하고 "leaves no doubt about the much higher exchange current density" 로 **값이 아니라 비로 물러선다**.
> **Q4**: `identifiab*` · `uniqu*` · `uncertain*` · `error` · `standard deviation` · `residual` · `least` · `sensitiv*` **전수 0**. **`j₀` 는 적합이 아니라 "simulation … compared"** 로 정해졌다(`fit*` 4 회는 전부 SE 전도도 · NMC 고주파 R‖CPE · SI 목록) — 목적함수 · 잔차 · ± 0. ⇒ **마흔두 번째 성질 "면적 규약을 적합 개선으로 골랐다 — 값이 τ 배 움직이는 선택을 기하 논증으로 하고, 곱만 보이는 극한의 값을 보고했다"**.
> **16호가 가져간 것**: `r_CAM = 2.5 µm` = **SEM 확인 공칭값**(측정 아님, 같은 NMC 분말이라 이식은 정당) · 초기값 = **문헌**(τ ← Kaiser 2018 [24], `D` ← [49–51]) + 자기 1/30 C 기울기(`dU/dc`) · ⚠ 16호 Table 1 의 `ε_SE 0.505 / ε_CAM 0.495` 는 **이 편 LCO 칸과 셋째 자리까지 같다**(이 편 NMC 칸은 0.491 / 0.509).

---

# 0. 원문에 없어서 확인이 필요한 것

| # | 공백 | 왜 중요한가 |
|---|---|---|
| G1 | **셀 수 · 반복 · 산포 0.** 두께당 셀 몇 개인지 미인쇄(`n =` 0 · `error` 0 · `standard deviation` 0). 대칭셀은 "Two ASSBs" 로 **한 쌍** | `j₀` 25.8 / 0.11 에 ± 가 없다. 비 ×235 가 셀 간 산포보다 큰지는 반원 크기(5 ↔ 80 Ω cm²)로 보아 거의 확실하나, 16호와의 ×12 는 산포로 판정 불가 |
| G2 | **`j₀` 를 정한 절차가 적합인지 수동 대조인지 미인쇄.** "simulations … compared" · "good agreement" 뿐, 목적함수 · 가중 · 주파수 창 · 잔차 0 | 파라미터 폭(근최적 집합)을 원리적으로 알 수 없다 |
| G3 | **"variables"(τ · `D` · `dU/dc`) 와 "freely adjustable"(`j₀` · `Q_DL` · β)의 구분이 불명.** Table 2 의 `dU/dc` 는 시작값과 다르다(`[재현]` ×1.31 · ×1.07 — SI Fig. S6 범례 시작값 대비) | 자유도가 3 인지 6 인지 모른다. `dU/dc` 가 움직였다면 면적 규약과 거래하는 통로가 열려 있었다(판정 (d)) |
| G4 | **LCO 의 τ(6.1)가 무엇으로 정해졌는지 미인쇄.** 두꺼운 극한에서 반원은 `j₀·a_v/τ` 만 본다 | `j₀`(LCO) ∝ τ. Kaiser 2018 시작값에서 얼마나 움직였는지도 모른다 |
| G5 | **대칭셀의 측정 압력 미인쇄.** 조립 "pressed at 125 MPa in the atlas manual hydraulic press" 뒤 Alpha-AK 측정 — ASSB 는 389 MPa | 빼는 음극 임피던스가 다른 압력의 값이다(16호: 음극 호 4 ↔ 9 Ω cm², 389 ↔ 97 MPa) |
| G6 | **대칭셀 음극 Li 함량(40 at%)과 ASSB 음극 Li 함량의 대응 미기재** | `[재현]` ASSB 음극은 SOC50 · 2 사이클째에 ≈5–30 at%(양극 두께에 따라 증가) — 아래 §5.6 |
| G7 | **LPSI 전도도 0.8 mS cm⁻¹ 의 온도 · 압력.** `[인쇄]` 측정 범위 −120 → **20 °C**, 펠릿 276 MPa · Au 스퍼터 · 무가압 셀; Table 1 은 T = 25 °C | 25 °C 값의 출처(외삽?) 미기재. 389 MPa 복합체 안 SE 에 그대로 쓴다 — τ 가 흡수한다(16호 G10 과 같은 구조) |
| G8 | **NMC 고주파 호("possibly … current collector and NMC particles")의 검증 0** | `[도표]` SI Fig. S7(31 µm)에서 이 호 ≈48 Ω cm² — `R_semicircle` 138 의 ≈35 %. 일부라도 CAM\|SE 쪽(코팅층 등)이면 `j₀`(NMC)가 바뀐다 |
| G9 | **두께는 잰 값이 아니라 계산값**(SI 식 S2, 공극 10 % 가정 — ref 37 Kroll 2021) | `a_v·d` 와 `R_ion` 둘 다 `d` 에 선형 — 두께 오차는 `R_ion` 과 면적에 같은 방향으로 들어간다 |
| G10 | **원자료 공개 문장 없음** | 재적합 불가 |

---

# 1. 서지 · 낱말 지문

규칙: NFKC 뒤 · 대소문자 구분 · 낱말 경계 · 본문은 참고문헌 전까지, SI 는 참고문헌 전까지(괄호). 줄끝 하이픈은 이은 판을 병기.

| `identifiab` | `uncertaint` | `confidence interval` | `Bayes` | `posterior` | `calibrat` | `LLI` | `LAM` | `degradation mode` | `contact loss` | `MPa` |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 (SI 0) | 0 (0) | 0 (0) | 0 (0) | 0 (0) | 0 (0) | 0 (0) | 0 (0) | 0 (0) | **0** (0) | **8** (SI 1) |

- NFKC 변경: 본문 **3 자**(U+2033 이중 프라임 3) · SI **132 자**(수학 이탤릭 글리프 U+1D4xx · U+1D7xx — 식 S1–S4 의 기호) — **열 변화 0**. 소프트 하이픈 0. 줄끝 하이픈 본문 19 곳 · SI 0 — **이어도 열 변화 0**.
- `MPa` 8 = 초록 "in the range of 400 MPa" · 전도도 펠릿 276 · 분리막 선압 97 · 셀 압착 389 · 사이클 스택 389 · 대칭셀 125 · 논의 "about 400" · 결론 "about 400". SI 1 = 389(전자전도도 셀).
- 보조: `contact` 9(물리 접촉 5 — 초록 2 · 서론 2 · `a_v` 정의 1) · `interfacial area` 2 · `area` 7 · `double layer` 6 · `capacitan*` 1(SI 1) · `tortuosit*` 6 · `simulat*` **19** · `fit*` 4(`j₀` 적합 0) · `agreement` 4 · `unclear` 1 · `radius` 4 · `SEM` 7(SI 6) · `FIB` 2 · `porosity` 1(SI 1) · `stack pressure` 7 · `degrad*` · `aging` · `void` · `BET` · `coverage` · `residual` · `least` · `sensitiv*` · `correlat*` **0**.
- Q5 보조: `reference electrode` 0 · `vs. Li` 0 · `Li+/Li` 0 — 전위 축은 그림(Fig. 2)에만 "Potential vs. In/InLi / V". `In:Li` 2(60:40).
- `[해석]` **`contact` 은 초록에서 `j₀` 를 정의하는 낱말로 쓰이고, `contact loss` · `void` 는 0** — 접촉을 **형성 조건**(압력)으로만 다룬다.

---

# 2. 셀 · 실험 (`[인쇄]`)

- **SE**: 0.67 Li₃PS₄ + 0.33 LiI (LPSI), 비정질. 2 g 배치 · Pulverisette 7 · ZrO₂ 20 mL + 볼 10 개(∅10 mm) · **700 rpm · 8 h**(99 사이클 = 5 min 밀링 / 15 min 휴지) · 마노 분쇄. 밀도 **2.15 g cm⁻³**(SI).
- **전도도**: 펠릿 ∅6 mm · **276 MPa / 30 min** · Au 스퍼터 양면 · 자작 2전극 셀 · Alpha-AK 1 MHz–0.1 Hz · 10 mV_rms · Quatro 저온 −120 → 20 °C(±0.1 °C) · RelaxIS 적합. 결과 **0.8 mS cm⁻¹**(Table 1 `σ` = 0.08 S m⁻¹, T = 25 °C).
- **CAM**: 단결정 **LiCoO₂**(Toda, 지름 5 µm, 구입 시 **LiNbO₃ ≈12 nm 코팅**) · 단결정 **LiNi₀.₈₃Mn₀.₀₆Co₀.₁₁O₂**(MSE Supplies, 지름 3–6 µm — SI 는 "4 – 6 µm") + **LiNbO₃ 1 wt%** 졸–겔(Li 에톡사이드 1 M : Nb 에톡사이드 0.5 M = 1 : 2 부피, 초음파 30 min · 진공 건조 · 공기 **300 °C / 2 h**, 5 °C min⁻¹).
- **복합양극**: CAM : SE = **70 : 30 질량**(SI 정밀값 LCO 0.695/0.305 · NMC 0.7003/0.2997), 마노 15 min, **탄소 없음**.
- **셀**: CompreCell + CompreDrive(active force control). LPSI ≈100 mg → **97 MPa / 5 min**(WC 피스톤) → In 박 100 µm(∅12 mm) 한쪽 + 복합양극 다른 쪽(10 · 20 · 40 · 80 mg 명목; SI 실측 LCO 11.6 · 19.1 · 41.4 · 80.2 · NMC 11.3 · 20.6 · 39.2 · 79.9 mg) → **389 MPa** 압착. 분리막 두께 **≈400 µm**("to avoid short circuits"). 셀 면적 **1.13 × 10⁻⁴ m²**(r = 0.6 cm).
- **두께**: 계산(SI 식 S1–S2, 공극 10 % 가정): LCO **32 · 52 · 113 · 219 µm** · NMC **31 · 57 · 108 · 221 µm**.
- **전기화학**: Autolab PGSTAT302N · **스택 389 MPa · 실온 · 0.1 C** · LCO 3.9–2.7 V · NMC 3.9–2.5 V(그림 축 "vs. In/InLi"). 1 사이클 완료 → 2 사이클째 **SOC50** 충전 → 개방 30 min 이완 → EIS **0.1 MHz – 5 × 10⁻⁴ Hz** · 10 mV_rms · RelaxIS 분석.
- **대칭셀 In–Li \| LPSI \| In–Li**(Fig. 1b): ASSB 두 개를 음극 In : Li = **60 : 40** 까지 충전 → 양극을 기계적으로 떼고 → 한쪽 펠릿을 PEEK 관(≈10 mm)에서 밀어내 → 다른 쪽(≈10.2 mm) 위에 SE 분말 소량을 깔고 겹침 → **125 MPa**(Specac 수동 프레스) → Alpha-AK 1 MHz–0.01 Hz · 10 mV_rms.
- **FIB-SEM/EDX**: Zeiss Crossbeam 550 · 불활성 이송 · 단면 폭 20 µm × 깊이 10 µm · Ga 30 kV(3 nA → 700 pA → 100 pA) · SEM 5 kV / 100 pA(InLens · SE) · EDX 5 kV / 2 nA(Oxford Ultim Max).
- **SI 전자전도도(NMC, SOC0)**: 금속 \| NMC 복합양극 \| 금속, 제조 · 측정 모두 389 MPa, 0.1 MHz–0.1 Hz.

---

# 3. 절별 해체

## 3.1 서론 (p1–2)

- `[인쇄]` "The SE | SE contacts determine the ion transport resistance of the cathode, `R_ion`, whereas the CAM | SE contacts determine the charge transfer resistance, `R_CT`."
- `R_ion` 은 대칭셀(양극\|SE\|양극 또는 Li\|SE\|양극\|SE\|Li)로 잴 수 있지만 `R_CT` 는 "more challenging due to the complex morphology"(ref 24 Kaiser 2018).
- TLM 은 "assume cylindrical pores between the CAM particles, which are filled by the electrolyte"(refs 25–28).
- 액체 문헌값: 흑연 두께 가변(Morasch 2021, ref 34) **1–6 A m⁻²** · LCO + LP40 **0.4 A m⁻²**(ref 31 Hess 2015 — 제목상 GITT · 비대칭 BV) · NMC622 + EC/EMC/DMC **2–4 A m⁻²**(SOC 의존, refs 32 · 33).
- `[인쇄]` "there are virtually no TLM-based studies on composite cathodes of ASSBs". 대안으로 **Bielefeld 2022**(ref 35 = **큐 57**)가 정전류 곡선 + 형태 반영 FEM 으로 NMC811\|Li₆PS₅Cl 에서 **"in the range of 10⁻⁵ A cm⁻²"**. `[재현]` = **0.1 A m⁻²** — 이 편 NMC 0.11 과 ≈10 % 안. ⚠ 이 편은 이 일치를 논의하지 않는다(액체와만 비교).
- `[인쇄]` 두께 가변의 논리: "the ion transport resistance of composite electrodes increases with increasing cathode thickness and the charge transfer resistance decreases with increasing cathode thickness (**due to the increasing interfacial area between CAM particles and SE particles**)" (ref 36 Cronau 2020).

## 3.2 Fig. 2 — 첫 사이클 (52 · 57 µm, 0.1 C)

- `[인쇄]` "The observed discharge capacities in the first cycle are in good agreement with practical capacities reported for LCO in the range of 180−200 mAh g⁻¹ and for NMC in the range of 190−200 mAh g⁻¹".
- `[도표]` 충전 LCO ≈190 · NMC ≈235 mAh g⁻¹ / **방전 LCO ≈170 · NMC ≈171 mAh g⁻¹** — **방전이 인용 범위 아래**(D1). 첫 효율 `[재현]` LCO ≈0.89 · NMC ≈0.73.
- 축 "Potential vs. In/InLi / V" — LCO 는 3.9 V vs In/InLi 까지(`[해석]` Li 대비 ≈4.5 V, 0.62 V 가정 — 이 편에 Li 대비 환산 0).

## 3.3 Fig. 3 — 두께별 완전지 스펙트럼 (SOC50, 2 사이클째, 고주파 저항 뺌)

- `[인쇄]` 고주파 저항(분리막 지배)을 뺐다. 분리막 ≈400 µm.
- **LCO**(3a): `[인쇄]` 반원 둘 + Warburg 형 저주파, 두 반원 합 **12–18 Ω cm²**, 고주파 반원은 두께와 함께 줄고 저주파 반원은 두께 무관. `[도표]` 인셋: 첫 극소 ≈8–12 Ω cm², 저주파 꼬리 0.5 mHz 에서 −Z″ ≈30–60.
- **NMC**(3b): `[인쇄]` 합 **90–200 Ω cm²**, 고주파 반원은 두께 무관 · 저주파 반원이 두께와 함께 준다(LCO 와 **반대 배치**). `[도표]` 극소 31 µm ≈200 · 57 ≈120 · 108 ≈110 · 221 ≈90 Ω cm².
- `[인쇄]` 두 반원의 전극 배정은 문헌에서 "not yet been clarified"(refs 42–44 — 43 = **10호 Vadhva**).

## 3.4 Fig. 4 — 대칭셀, 그리고 빼기 (Fig. 5 · 6)

- `[인쇄]` 대칭셀(LPSI 저항 뺌): 반원 **≈3 Ω cm²(고주파) · ≈9 Ω cm²(중간)**, 저주파에 셋째 반원 **≈15 Ω cm²** "indication". "A detailed analysis … is beyond the scope". `[도표]` 0.01 Hz 에서 Z′ ≈21 로 닫히지 않음.
- `[인쇄]` "Since the symmetric cells contain two In−Li electrodes, we subtracted **50 %** of the impedance of the symmetric cell from the impedance of the ASSBs."
- **LCO 52 µm (Fig. 5a)**: `[인쇄]` 1 × 10⁵ – ≈1 × 10³ Hz 는 빼기에 거의 무관, 저주파는 크게 영향 ⇒ "strong indication that the high-frequency semicircle originates from `R_ion` and `R_CT` of the cathode".
  ★ `[도표]` 뺀 뒤 **−(Z″ − 0.5 Z″_anode) 가 ≈10 Hz 근방에서 0.1 · 0.4 까지 곤두박질치고, ≈10–≈120 Hz 사이에는 점이 그려져 있지 않다**(로그 축이라 음수는 안 그려진다) — `[해석]` **그 대역에서 뺀 허수부가 음(유도성 부호)** = 과차감. Z′ 도 ≈10 Hz 에서 ≈6.5 → ≈100 Hz 에서 ≈7.7 로 **주파수와 함께 증가**(수동 RC 망에서 비정상). 본문은 이 부호 반전을 말하지 않는다(D7). Fig. 5b 는 0.1 MHz – **300 Hz** 만 쓴다 — 과차감 대역 바로 위에서 자른다.
- **LCO 뺀 뒤 고주파 반원(Fig. 5b)**: `[인쇄]` "4−8 Ω cm²"(p7). `[도표]` 300 Hz 끝점 Z′: 32 µm ≈6.4 · **52 µm ≈7.3** · 113 ≈4.9 · 219 ≈4.2 — 닫히지 않음(끝점 −Z″ ≈0.4–1.0) · **52 > 32 로 단조 아님**(D11).
- **NMC 57 µm (Fig. 6a)**: `[인쇄]` "Due to the higher impedances … only a small influence … Only in a frequency range around **0.1 Hz** is an influence … on the imaginary part". `[도표]` −Z″ 극소 ≈0.1 Hz(≈14 → ≈10). Fig. 6b 는 Fig. 3b 와 `[인쇄]` "very similar". `[도표]` 극소 31 ≈192 · 57 ≈113 · 108 ≈101 · 221 ≈82 Ω cm².
- `[인쇄]` NMC 의 두께 무관 고주파 반원: "it is likely that this semicircle is caused by an interfacial impedance, **possibly** the impedance between current collector and NMC particles" — **소거법 배정**, 검증 0(G8).

## 3.5 TLM 식 (p4–5, 렌더로 확인)

```
[인쇄] (1)  Z_cathode = √(Z_loc·R_ion/(a_v·l_SE)) · coth( √(R_ion·a_v·l_SE / Z_loc) )      (ref 46 Huang & Zhang 2016)
[인쇄] (2)  R_ion = τ_Li⁺ · d / (ε_SE · σ)
[인쇄] (3)  Z_loc = ( 1/(R_CT + (dU/dc_Li)·Y_CAM) + iω·C_DL )⁻¹
[인쇄] (4)  Y_CAM = Y_CAM(r_CAM, D_CAM)   — 구 확산, tanh 형
[인쇄]      a_v = (ε_CAM·A_CAM)/V_CAM = 3·ε_CAM/r_CAM   "active area of the CAM particles in contact to SE normalized by the cathode volume"
[인쇄]      l_SE = τ_Li⁺·d   "effective diffusion path length in the SE"
[인쇄] (5)  R_CT = R·T/(F·j₀)
[인쇄] (6)  Z_loc = ( 1/(R_CT + (dU/dc)·Y_CAM) + (iω)^β·Q_DL )⁻¹        ← 수정 (i): CPE
[인쇄] (7)  Z_cathode = √(Z_loc·R_ion/(a_v·d)) · coth( √(R_ion·a_v·d / Z_loc) )   ← 수정 (ii): l_SE → d
```

- **적용 전제**: `[인쇄]` 전자 저항 ≪ 이온 저항. LCO(SOC50) 전자전도도 ≈0.1 S cm⁻¹(refs 47 · 48) — LPSI 0.8 mS cm⁻¹ 의 ≈2 자릿수 위. NMC 는 SOC50 문헌값이 없어 SOC0 복합체를 쟀고(SI) "this resistance is lower than the ionic resistance" + SOC 가 오르면 더 준다 "expected".
- **수정 (i)**: 이중층 → CPE, "reported in the literature"(refs 27 · 34).
- **수정 (ii)** 전문: `[인쇄]` "In eq 1, the factor `a_v·l_SE` describes the CAM | SE interfacial area normalized by the nominal area of the cathode. However, the appearance of the ionic tortuosity in the factor `a_v·l_SE = a_v·τ_Li⁺·d` is caused by mapping the 3D morphology of the composite electrode on 1D pores with tortuosities >1. However, in a 3D composite electrode, the interfacial CAM | SE area normalized by the nominal cathode area should be better described by `a_v·d`".
  `[해석]` 논리 자체는 합당하다 — 전극 부피당 CAM 표면은 굴곡도와 무관하다. 문제는 (1) 이것이 "for improving the agreement" 의 두 수정 중 하나로 소개되고, (2) **이 선택이 `j₀` 를 정확히 τ 배 바꾼다는 것**(§5.3)이 지면에 없으며, (3) 비교한 액체 문헌들이 어느 규약인지 적지 않았다는 것.

## 3.6 Table 1 · 2 — 고정 · 가변 파라미터

| 고정 (Table 1) | LCO | NMC |
|---|---|---|
| `σ` | 0.08 S m⁻¹ | 0.08 S m⁻¹ |
| T | 25 °C | 25 °C |
| A | 1.13 × 10⁻⁴ m² | 1.13 × 10⁻⁴ m² |
| `ε_SE` / `ε_CAM` | **0.505 / 0.495** | **0.491 / 0.509** |
| `r_CAM` | 2.5 × 10⁻⁶ m | 2.5 × 10⁻⁶ m |

| 가변 (Table 2) | LCO | NMC | 단위 |
|---|---|---|---|
| τ_Li⁺ | 6.1 | 6.8 | — |
| **`j₀`** | **25.8** | **0.11** | A m⁻² |
| `dU/dc_Li` | −2.65 × 10⁻⁵ | −3.59 × 10⁻⁵ | V m³ mol⁻¹ |
| `Q_DL` | 0.4 | 0.04 | F m⁻² s^(β−1) |
| β | 0.78 | 0.87 | — |
| `D_CAM` | 3.9 × 10⁻¹⁵ | 3.8 × 10⁻¹⁶ | m² s⁻¹ |

- **시작값**(`[인쇄]`): τ ← "An ion transport tortuosity value for a composite electrode with 50 vol % SE phase taken from the literature24"(Kaiser 2018) · `D` ← LCO ref 49(Tang 2019) · NMC refs 50 · 51(Cui 2016 · Wei 2015) · `dU/dc` ← 1/30 C 충·방전 **평균** 곡선의 SOC50 선형 적합(SI Fig. S6; `[인쇄]` 범례 **m = −2.024 × 10⁻⁵ (LCO) · −3.358 × 10⁻⁵ (NMC)**). `[인쇄]` "Only the parameters `j₀`, `Q_DL`, and β were considered as freely adjustable parameters."
- `[인쇄]` 반경: "determined by SEM imaging of the purchased CAM powder as well as by SEM/EDX imaging … (Figures S3−S5). The obtained particle radii were in good agreement with the values provided by the suppliers." — **평균 반경의 수 · 분포 · 방법(투영 지름? 입자 수?) 0**.

## 3.7 NMC — Fig. 7 · Table 3

- `[인쇄]` 고주파 계면 호를 R‖CPE 로 **적합**(SI Fig. S7)해 TLM 모의에 **직렬로 더했다**. "Overall, there is a good agreement between simulated and experimental spectra for different thicknesses".
- `[도표]` Fig. 7 극소: 31 µm 모의 ≈191 ↔ 실험 ≈192 · 57 ≈116 ↔ ≈113 · 108 ≈99 ↔ ≈101 · **221 µm 모의 ≈94 ↔ 실험 ≈82**(모의가 ≈+12 Ω cm² — 가장 두꺼운 셀에서 과대). 16호도 207 µm(389 MPa)에서 같은 방향의 과대를 인쇄했다(D10).
- `[인쇄]` `j₀` = **0.11 A m⁻²** — "more than one order of magnitude lower than … LiNi₀.₆Mn₀.₂Co₀.₂O₂ … liquid electrolyte (`j₀` = 2−4 A m⁻²)".
- **Table 3**(`[인쇄]`):

| 두께 µm | `R_ion` Ω cm² | `R_CT/(a_v d)` Ω cm² |
|---|---:|---:|
| LCO 32 | 48.3 | 0.52 |
| LCO 52 | 78.5 | 0.32 |
| LCO 113 | 170.6 | 0.15 |
| LCO 219 | 330.7 | 0.08 |
| NMC 31 | 53.7 | 120.1 |
| NMC 57 | 98.7 | 65.3 |
| NMC 108 | 187 | 34.5 |
| NMC 221 | 382.6 | 16.8 |

- `[인쇄]` 극한: 얇은 쪽 `R_semicircle ≈ R_ion/3 + R_CT/(a_v d)` = **138 Ω cm²**(31 µm) · 두꺼운 쪽 `R_semicircle ≈ √(R_CT·R_ion/(a_v d))` = **80 Ω cm²**(221 µm) · 그 사이 전이가 "decrease in the semicircle resistance with increasing thickness" 를 만든다.
- `[재현]` 138 = 53.7/3 + 120.1 ✓ · 80 = √(382.6 × 16.8) = 80.2 ✓ · 정확한 coth 식(순수 저항 `Z_loc`)으로 140.7 · 81.4.
- `[도표]` SI Fig. S7: 31 µm 고주파 계면 호(초록) 지름 **≈48 Ω cm²** — 138 + 48 ≈186 ↔ 극소 ≈192 와 맞는다.

## 3.8 LCO — Fig. 8

- `[인쇄]` "much higher values for the exchange current density than for the NMC-based cathodes have to be chosen" · "For all thicknesses, the resistance of the high-frequency semicircle is much smaller than `R_ion`, so that the TLM-limiting case `R_semicircle ≈ √(R_CT·R_ion/(a_v d))` should be applicable" · `j₀` = **25.8 A m⁻²** → `R_CT/(a_v d)` 0.08–0.52 Ω cm².
- ★ `[인쇄]` "However, in the limiting case … the TLM predicts a semicircle resistance, **which is independent of thickness**, see Figure 8, while the experimental spectra are characterized by a decrease … The origin of this discrepancy between experimental and simulated spectra is **unclear at present**. In order to elucidate the origin in future work, it will be important to carry out tomographic reconstructions …".
- `[도표]` Fig. 8: 네 두께의 모의가 **한 곡선으로 겹친다** — 호 Z′ ≈1.1 → 극소 ≈5.2(−Z″ ≈0.45), 정점 −Z″ ≈1.3 · 그 뒤 45°–급 상승. `[재현]` 두꺼운 극한식 5.0 Ω cm²(네 두께 동일).
- `[인쇄]` "Nevertheless, the much lower semicircle resistance for the thick LCO-based cathodes as compared to thick NMC-based cathodes, for both of which the limiting case … is applicable, **leaves no doubt** about the much higher exchange current density of the LCO-based cathodes."
- `[인쇄]` "the value of 25.8 A m⁻² … is **almost 2 orders of magnitude higher** than the value reported for a LCO-based composite cathode with the pore space filled by liquid electrolyte (`j₀` = 0.4 A m⁻²)" ⇒ "under the applied stack pressures of about 400 MPa, the exchange current densities in the cathodes of ASSBs can compete with those or even exceed those of composite electrodes filled with liquid electrolyte".

## 3.9 결론 (p7)

`[인쇄]` 두 값(25.8 · 0.11 A m⁻²) 재진술 · LCO 가 액체 LCO 보다 높다 · "This shows under the applied stack pressure of about 400 MPa, high exchange current densities … are achievable" · LCO ↔ NMC 차이의 기원은 DFT 공간전하층 계산(ref 52 Haruyama 2014) 제안 · 압력 영향은 실험으로 볼 것.

## 3.10 SI (8 쪽)

- **S1–S2 두께**: `V_i = m·x_i/ρ_i`, `d = (V_CAM + V_SE)/(πr²) × 1.1`. `ρ` LCO 5.01 · NMC 4.83(SI refs 2 · 3) · SE 2.15 g cm⁻³.
- **Fig. S1**: 첫 사이클(안 봄 — §12).
- **전자전도도**(Fig. S2, SOC0, 389 MPa): 고주파 `R_par` = (σ_ion + σ_eon)⁻¹·d/A · 중간 호 **C = 6 × 10⁻⁶ F cm⁻²** → 두 금속\|양극 계면 · 저주파 호 = 이온 차단 ⇒ `σ_eon = d/((R_ω→0 − R_int)·A)` ⇒ **σ_eon = 2.2 × 10⁻³ S cm⁻¹ · σ_ion = 1.3 × 10⁻⁴ S cm⁻¹**(SI ref 4 **Minnmann 2021** 방법). `[도표]` `R_par` ≈5.35 · 계면 호 끝 ≈8.9 · `R_ω→0` ≈9.3 Ω cm². 두께 · 셀 번호 미인쇄.
- **Fig. S3** 분말 SEM · **S4** LCO 단면 SEM/EDX(Co · P · S) · **S5** NMC 단면 SEM/EDX(Co · Ni · Mn · P · S).
- **Fig. S6** 1/30 C 곡선(시작값 `dU/dc`) · **Fig. S7** NMC 31 µm 고주파 R‖CPE 적합(회로: R₁‖CPE₁ – R₂‖CPE₂ – CPE₃).

---

# 4. ★★★★ 면적과 `j₀` — 식 수준 판정

```
[인쇄] a_v = 3·ε_CAM / r_CAM     ("in contact to SE" — 접촉 분율 인자 없음)
[인쇄] R_CT = R·T / (F·j₀)
[인쇄] (7)  계면은 언제나  Z_loc / (a_v·d)  로만 들어간다
─────────────────────────────────────────────────────────────────
[해석] 얇은 전극 쪽:  R_CT/(a_v d) = R·T·r_CAM / (3·F·j₀·ε_CAM·d)     ⇒  식별 = j₀·ε_CAM/r_CAM
[해석] 두꺼운 극한:   √(R_ion·R_CT/(a_v d)) = √( τ·R·T·r_CAM / (3·F·σ·ε_SE·ε_CAM·j₀) )   ⇒  식별 = j₀·ε_CAM/(τ·r_CAM)
[해석] 이중층:        Q_DL 도 a_v·d 로 정규화                             ⇒  식별 = Q_DL·ε_CAM/r_CAM
```

- 두께 가변이 하는 일: `R_ion ∝ d` 와 `R_CT/(a_v d) ∝ 1/d` 의 **d 의존성 차이**로 두 항을 가른다. **`a_v` 와 `j₀` 는 둘 다 d 와 무관**이므로 두께는 그 둘을 가를 수 없다. `[해석]` 두께 스윕은 "계면 면적이 d 에 비례한다" 는 **척도 법칙**은 시험하지만(NMC 에서 통과, LCO 에서 실패), **접촉 분율 θ** 는 시험하지 않는다.
- 접촉 분율 θ 를 넣으면(`a_v → θ·a_v`): `j₀^report = θ·j₀^true` · `Q^report = θ·Q^true` ⇒ **`R_CT·Q` 는 θ 무관**(16호 digest T3 · 개념 페이지 1단계와 같은 대수).
- **"comparative case study" 의 두 재료는 같은 면적 가정**(`r_CAM` 둘 다 2.5 µm · 기하 `a_v` · 수정 (ii))을 쓴다 ⇒ 재료 간 `j₀` **비**는 규약과 무관하고, 남는 문제는 **두 재료의 θ 가 같은가**다 — 이것을 1단계 R·C 가 본다(§5.2).

---

# 5. `[재현]` 검산

## 5.1 Table 3 재현

`R·T/F` = 0.025693 V(298.15 K). `a_v` LCO 5.94 × 10⁵ · NMC 6.108 × 10⁵ m⁻¹.
- `R_ion`: 8 행 전부 소수 첫째 자리까지 재현(식 2, τ · ε_SE · σ 인쇄값).
- `R_CT/(a_v d)`: LCO 0.524 · 0.322 · 0.148 · 0.077 ↔ 인쇄 0.52 · 0.32 · 0.15 · 0.08 ✓ · NMC **123.4 · 67.1 · 35.4 · 17.3 ↔ 인쇄 120.1 · 65.3 · 34.5 · 16.8** — 전부 **−2.7 %**. 인쇄 표에서 역산한 `j₀` = **0.113**(LCO 26.0) — 0.11 은 반올림(D4, 작다).
- 두께: SI 질량 · 밀도로 LCO 31.7 · 52.1 · 113.0 · 218.9 · NMC 31.3 · 57.0 · 108.4 · 221.0 µm ✓ · `ε_CAM` LCO 0.4944 · NMC 0.5098 ✓.
- `a_v·d`(공칭 면적당 CAM 계면 면적): LCO 19.0 · 30.9 · 67.1 · 130 · NMC 18.9 · 34.8 · 66.0 · 135.
- ⚠ **공극 처리의 이중성**(D3): 두께는 공극 10 % 로 ×1.1 부풀리고 `ε_CAM` 은 공극을 뺀 비(합 1.000)라 `ε_CAM·d = 1.1·V_CAM/A` — `a_v·d` 가 실제 CAM 표면을 **×1.1 과대** ⇒ 같은 데이터에서 `j₀` ×1/1.1 과소. 작다.

## 5.2 ★★★ 1단계 R·C · 3-b 상한

CPE → 유효 용량(Brug 형 `C = Q^{1/β}·R^{(1−β)/β}`, `R` = 계면 면적당 `R_CT`):

| | `R_CT` (Ω cm², CAM 면적당) | `Q_DL` | β | `C_eff` (µF cm⁻², CAM 기하 면적당) | τ_CT = `R·C` | 꼭짓점 1/(2πτ) |
|---|---:|---:|---:|---:|---:|---:|
| LCO (이 편) | 9.96 | 0.4 | 0.78 | **4.4** | 4.4 × 10⁻⁵ s | ≈3.6 kHz |
| NMC (이 편) | 2,336 | 0.04 | 0.87 | **2.0** | 4.6 × 10⁻³ s | ≈34 Hz |
| NMC (16호, 389 MPa · argyrodite) | 193 | 0.54 | 0.89 | **30.7** | 5.9 × 10⁻³ s | ≈27 Hz |
| NMC (16호, 97 MPa) | 347 | 0.18 | 0.81 | 5.5 | 1.9 × 10⁻³ s | ≈84 Hz |

- **LCO ↔ NMC(이 편)**: `1/R_CT` ×235 · `Q` ×10 · `C_eff` ×2.2 · **τ ×106** ⇒ **면적 서명 아님**. 면적(θ)이 설명할 수 있는 몫은 `C` 비까지(×2.2, 원값 `Q` 로 ×10) — 나머지 ×24–107 은 곱의 다른 인자(`j₀^true` · 코팅층 · 배정)에 있다. `[해석]` **이 편의 비교 결론은 R·C 로 견딘다**(전제: 같은 SE 에서 `C_dl ∝ 접촉 면적`).
- **16호(389) ↔ 이 편 NMC**: 같은 NMC 83\|6\|11 분말(MSE, 3–6 µm) · 같은 LiNbO₃ 1 wt% 처방 · 같은 389 MPa · 같은 `r_CAM` · 다른 SE(LPSClBr₀.₇ ↔ LPSI) — `1/R_CT` **×12.1** ↔ `Q` **×13.5** · `C_eff` **×15.4** ⇒ **τ ×1.28 — 면적 서명**. 16호의 `[인쇄]` "about one order of magnitude higher than [30] … exchange current density increases with the ionic conductivity of the SE" 는 R·C 로는 **접촉 면적 ×12–15 와 구별되지 않는다**. ⚠ 전제가 약하다 — 두 SE 가 다르면 **면적당 이중층 용량 자체**가 다를 수 있다(공간전하 · 계면 화학). 그래서 이것은 "16호가 틀렸다" 가 아니라 "그 비교가 곱을 가르지 않았다" 까지다.
- **3-b 상한**(이중층 비용량 ≈10 µF cm⁻² 기준): 이 편 LCO 4.4 · NMC 2.0 µF cm⁻² ✅ **통과** — "전하이동" 호가 이중층 자릿수 안에 있다(19–21 · 43 · 48호 계열 실패와 다르다). 16호 389 MPa 는 30.7 — 기하 면적당 이미 ×3; θ ≤ 1 이면 실접촉 면적당 ≥30.7 ⚠.
- 꼭짓점: LCO ≈3.6 kHz 는 Fig. 5b 고주파 호(0.1 MHz–300 Hz)와 · NMC ≈34 Hz 는 Fig. 6b 중간 호와 정합.

## 5.3 ★★★★ 면적 규약의 대수 — 수정 (ii)는 `j₀` 를 정확히 τ 배 움직인다

식 (1)과 (7)에서 계면 쪽은 `Z_loc/(a_v·ℓ)` 한 조합으로만 들어간다(`R_ion·a_v·ℓ/Z_loc` 도 같은 조합의 역수 × `R_ion`). `ℓ = s·d` 로 바꾸면 `Z_loc → s·Z_loc` 가 **같은 스펙트럼**을 준다. 식 (6)에서 `s·Z_loc` 은 `R_CT → s·R_CT` · `dU/dc → s·dU/dc` · `Q_DL → Q_DL/s`(β · `D` 불변)로 정확히 만들어진다.

| | 이 편 (식 7, `ℓ = d`) | 식 (1) 그대로 (`ℓ = τd`) |
|---|---:|---:|
| `j₀` LCO | 25.8 | **4.2** A m⁻² |
| `j₀` NMC | 0.11 | **0.016** A m⁻² |
| LCO ÷ 액체 LCO(0.4) | ×64.5 ("almost 2 orders") | ×10.6 |
| NMC ÷ 액체 NMC622(2–4) | ×1/18–1/36 | ×1/125–1/250 |
| `dU/dc` 가 가야 할 값 | ×1 | ×τ (≈6–7) |

- `[해석]` 수정 (ii)는 물리적으로 옹호되지만, **결과 `j₀` 의 자릿수 하나(×6.1–6.8)가 이 한 줄에 걸려 있다**. 비교 대상 액체 문헌이 어느 규약(τ 포함 여부 · BET · 구 기하)을 썼는지 지면에 없다 ⇒ 편 간 `j₀` 비교는 **규약을 맞췄다는 확인 없이는 방향까지만** 선다.
- `[해석]` **`dU/dc` 가 규약의 유일한 닻이다** — 저주파 화학 용량(공칭 면적당) = `a_v·d · F·r/(3|dU/dc|) = F·ε_CAM·d/|dU/dc|`(r 약분). 모형이 확산을 전하이동과 **같은 `a_v`** 로 통과시키므로 면적 척도 s 와 `dU/dc` 가 곱으로 묶이고, `dU/dc` 를 OCV 기울기로 고정하면 s 가 정해진다. 이 편은 `dU/dc` 를 "variable" 로 두었고 적합값은 시작값의 **×1.31(LCO) · ×1.07(NMC)** — 규약 교체(×6–7)는 이 닻과 맞지 않는다. ⚠ 닻의 조건: 스펙트럼이 **용량성 극한**에 닿아야 한다. `[재현]` `r²/D` = LCO ≈1.6 × 10³ s · NMC ≈1.6 × 10⁴ s ↔ NMC 비교 창의 하한 0.01 Hz(Fig. 7) ⇒ ωτ ≈10³ — **반무한 Warburg 영역**이라 닻은 `s·√D/|dU/dc|` 로 약해지고 가변 `D` 가 흡수한다(개념 페이지 38호 줄 "저주파 꼬리의 반무한 곱"). 그리고 **진짜 부분 접촉(θ < 1)은 물리적으로 화학 용량을 줄이지 않는데**(입자는 좁은 접촉으로도 다 찬다) 이 모형 구조에서는 줄인다 — 닻이 θ 에 대해서는 **모형 가정의 산물**이다.

## 5.4 LCO — 두꺼운 극한만 본다

`R_ion/(R_CT/a_v d)` LCO **92 · 244 · 1,150 · 4,300** — 네 두께 전부 두꺼운 극한 ⇒ 반원은 `√(R_ion·R_CT/(a_v d))` = **5.0 Ω cm² 한 값**(τ, `j₀`, `a_v`, σ, ε 의 한 조합). `[재현]` `j₀`(LCO) ∝ τ/(`R_semicircle`²): τ 가 Kaiser 시작값에서 ±20 % 움직이면 `j₀` 도 ±20 %. `[재현]` 두꺼운 두 재료의 비: `j₀` ∝ τ/`R_semicircle`² 이므로 (80/5)² × (6.1/6.8) ≈ 230 ≈ 인쇄 ×235 — **저자의 "no doubt" 논증은 반원 지름 비의 제곱이 주는 것이고 그 부분은 선다.** 절대값 25.8 은 τ 와 모형 불일치(두께 추세 재현 실패) 위에 있다.

## 5.5 SI 전자전도도 셀의 이온 전도도 ↔ TLM τ

- `[재현]` SI σ_ion(복합체, SOC0) = 1.3 × 10⁻⁴ S cm⁻¹ ⇒ 식 (2)의 유효 τ = ε_SE·σ/σ_ion = 0.491 × 8 × 10⁻⁴ / 1.3 × 10⁻⁴ = **3.0** ↔ TLM 적합 τ = **6.8** ⇒ **`R_ion` ×2.25 불일치**(같은 NMC 복합체 · 같은 389 MPa). 지면 논의 0(D6).
- ⚠ 그러나 σ_ion 은 **거의 같은 두 수의 차**다 — σ_ion/(σ_ion + σ_eon) = **5.6 %** ⇒ `R_par` 이나 `R_ω→0 − R_int` 가 ±3 % 만 흔들려도 σ_ion 은 ±50 % 이상. `[도표]` Fig. S2 판독(5.35 · ≈3.3–3.6 · 9.3)으로 σ_ion/σ_eon ≈0.06–0.13 — 판독 한계 안에서 인쇄값과 양립하지만 **분해능이 없다**. ⇒ 반례가 아니라 **독립 `R_ion` 채널이 지면에 있었고 분해능이 없어 쓰이지 않았다**까지.

## 5.6 대칭셀 빼기 — 음극 상태의 불일치

`[재현]` In 박 100 µm × 1.131 cm² × 7.31 g cm⁻³ = 82.7 mg = **0.720 mmol In**. SOC50(2 사이클째)까지 음극에 들어간 Li ≈ (첫 사이클 비가역 + 두 번째 충전 절반) — `[도표]` Fig. 2 용량 사용:
- LCO 52 µm(13.3 mg LCO): (190 − 170) + 85 ≈105 mAh g⁻¹ → 1.40 mAh = 0.052 mmol ⇒ **≈6.8 at% Li** · LCO 219 µm(55.7 mg) ⇒ **≈23 at%**
- NMC 57 µm(14.4 mg): (235 − 171) + 85.5 ≈150 mAh g⁻¹ → 0.080 mmol ⇒ **≈10 at%** · NMC 221 µm(56.0 mg) ⇒ **≈30 at%**
- (비가역 Li 가 음극에 남지 않았다고 두면 하한 ≈5.5 at%.)
⇒ `[해석]` **ASSB 음극은 ≈5–30 at% Li 이고 양극 두께와 함께 커진다. 빼는 대칭셀은 40 at% · 125 MPa(조립) 한 점이다.** 두 가지를 부른다: (1) 과차감(§3.4 Fig. 5a 허수부 부호 반전 ≈10–120 Hz)과 방향이 맞는다(16호: 음극 호가 압력에 민감 · 16호 digest Q5 ⑤ 평탄 구간 안 음극 DRT 봉우리 ×15 이동) · (2) **음극 몫이 양극 두께와 함께 바뀌어 "두께 의존 = 양극" 배정 논리를 오염**시킬 수 있다 — LCO 처럼 양극 호(4–8 Ω cm²)가 음극 호(3 · 9 · 15 Ω cm²)와 같은 크기일 때 특히.

## 5.7 NMC 고주파 호의 배정이 `j₀` 를 움직인다

`[도표]` S7 의 고주파 호 ≈48 Ω cm²(31 µm)는 "possibly current collector \| NMC" 로 **TLM 밖**에 두었다. `[해석]` 이 호가 CAM\|SE 계면(예: 졸–겔 LiNbO₃ 층 · 계면 분해층)의 일부라면 TLM 이 설명해야 할 계면 저항은 **더 커지고** `j₀` 는 **더 작아진다**; 반대로 TLM 호의 일부가 집전체 쪽이면 커진다. 두께 무관이라는 한 가지 성질로 배정했다 — 계면층 저항(`R_CT/(a_v d)` 처럼 1/d 로 줄어야 하는)과는 구별되지만 **집전체\|양극 외의 두께 무관 후보(분리막 쪽 계면 · 기준 없는 2전극의 음극 쪽 호)** 는 검사되지 않았다.

---

# 6. 비교의 유효성 — 요약

| 비교 | 면적 가정이 같은가 | 1단계 R·C | 판정 |
|---|---|---|---|
| **LCO ↔ NMC**(같은 지면) | ✅ 같다(`r_CAM` 2.5 µm 둘 다 · 수정 (ii) · 같은 SE · 같은 389 MPa) | τ ×106 — 면적 서명 아님 | ✅ **비는 선다**(C ∝ θ 전제 위). ⚠ 코팅 · NMC 고주파 호 배정 · LCO 두꺼운 극한(τ 의존) · n 미인쇄 |
| **이 편 ↔ 액체 문헌**(LCO 0.4 · NMC622 2–4 A m⁻²) | ❓ 문헌 규약 미기재 · 방법 다름(GITT/BV · TLM) · 액체는 θ ≈ 1 | 불가(문헌 `C` 0) | ⚠ **방향만** — "2 orders" 의 ×6.1 이 수정 (ii) |
| **이 편 ↔ Bielefeld 2022**(NMC811\|LPSCl, 10⁻⁵ A cm⁻²) | ❓ FEM 형태 반영(큐 57 에서 확인) | 불가 | `[재현]` 0.1 ↔ 0.11 A m⁻² — **지면 논의 0**. 일치가 규약 일치인지 큐 57 로 |
| **16호 ↔ 이 편 NMC**(16호의 "SE 전도도와 함께 오른다") | ✅ 같은 규약 · 같은 분말 · 같은 압력 · ⚠ 다른 SE | **τ ×1.28 — 면적 서명** | ⚠ **곱을 가르지 않았다** — 전도도 서사와 접촉 면적 ×12–15 가 구별되지 않는다 |

---

# 7. 16호가 가져간 것 — 대조

| 16호가 쓴 것 | 이 편의 실체 | 판정 |
|---|---|---|
| `r_CAM = 2.5 µm` [30] | SEM 으로 **공급자 공칭** 확인, 수 · 분포 0. `[도표]` SI Fig. S3b: NMC 분말은 **≈1–2 µm 결정립이 뭉친 ≈3–5 µm 응집체**로 보이고, S5a 단면(2 µm 막대)의 NMC 조각은 대략 **1–3 µm 폭** | ⚠ **가정에 가깝다.** 같은 분말이라 이식은 정당하나, 응집체가 혼합 · 389 MPa 에서 쪼개지면 유효 `r` 이 작아져 `a_v` ↑ · `j₀` ↓(`r` 1 µm 면 ×1/2.5). 37호 `R_s` 9 배 · 9호 곱의 `R_s` 자리와 같은 약점 |
| 초기값 | τ ← Kaiser 2018(50 vol% SE) · `D` ← 문헌 3 편 · `dU/dc` ← 자기 1/30 C | **문헌값 + 자기 OCV 기울기**. 16호 `dU/dc` −3.48 × 10⁻⁵(고정)은 이 편 NMC 시작 −3.358 · 적합 −3.59 사이 |
| `ε_SE 0.505 / ε_CAM 0.495` | **이 편 LCO 칸**. NMC 칸은 0.491 / 0.509 | ⚠ `[재현]` 이 편 방식(S1)으로 NMC 70 wt% 가 ε_SE 0.505 가 되려면 ρ_SE ≈**2.03 g cm⁻³** — argyrodite 밀도로 가능한 범위인지 16호 지면으로 판정 불가(16호 digest G5 는 ≈1.7 가정). **복사인지 우연인지 가르지 않는다** |
| "같은 불일치가 [30] 에서도 있었고 이유는 기공 구조" | 이 편은 **"unclear at present"** — 이유 인쇄 0, 토모그래피 제안 | 기공 구조 설명은 **16호(2026)의 것** |
| "비교 대상 `j₀` 값이 16호 지면에 없다(≈0.13 이어야)" | **0.11 A m⁻²**(NMC, LPSI, 389 MPa) | 16호 1.33 ÷ 0.11 = **12.1** = "about one order" ✓ · 전도도 비 5.9 |
| 두꺼운 극한식 | `[인쇄]` `√(R_CT·R_ion/(a_v d))`(근호가 분모까지) | 16호 digest 의 `√(R_CT·R_ion)/(a_V·d)` 표기는 이 편 식과 다르다 — 16호 원문 인쇄를 다시 볼 것(`[재현]` 이 편 80 Ω cm² 는 근호 전체형으로만 나온다) |
| τ | 이 편 NMC 6.8(LPSI) | 16호 7.7 / 8.8(argyrodite, 389 / 97 MPa) |

---

# 8. ★★★★ 곱 축퇴 처방 — 서른세 번째 적용

### 입력 점검

| 단계 | 입력 | 판정 |
|---|---|---|
| **1단계** `R`·`C` | `j₀` · `Q_DL` · β 두 재료 인쇄(Table 2) · 같은 `a_v` 규약 | ✅ **완비** — LCO ↔ NMC τ ×106(면적 서명 아님) · 편 간(16호 ↔ 이 편) τ ×1.28(**면적 서명**) |
| **2단계** 면적 대조군 | 두께 4 점 = 공칭 면적당 계면 면적 ∝ d 의 **척도 대조** | ⚠ 부분 — 척도 법칙은 NMC 통과 · LCO 실패("unclear"). θ 는 안 건드린다 |
| **3단계-a** `Ea` | 실온 한 점 | ❌ |
| **3단계-b** `C` 상한 | Brug `C_eff` LCO 4.4 · NMC 2.0 µF cm⁻²(CAM 기하 면적당) | ✅ **통과** — 이중층 자릿수 안 |
| **4단계** 시간 영역 | 0.1 C · 1/30 C 곡선뿐, 펄스 · GITT 0 | ❌ |

### ⇒ 이 적용이 처방에 더하는 것

1. **새 줄 "면적 정규화 규약"** — 모형 수정 하나(`a_v·τd → a_v·d`)가 `(j₀, Q_DL, dU/dc) → (j₀/s, Q_DL/s, s·dU/dc)` 의 **정확한 재척도**다. 보고 `j₀` 옆에 (i) 면적 규약(구 기하 · BET · τ 포함 여부) (ii) 비교 대상의 규약 (iii) `dU/dc` 적합값 ÷ OCV 기울기(모형 안 면적 척도의 닻, 용량성 극한에 닿을 때만)를 적는다. 규약이 다른 편끼리의 `j₀` 비교는 방향까지만.
2. **1단계를 편 사이로 건 첫 표본** — 같은 분말 · 같은 규약 · 같은 압력, 다른 SE: R·C 가 면적 서명을 준다. 전제(`C ∝ θ`)가 **SE 가 바뀌면 약해진다**는 것을 줄 옆에 적는다.
3. **3-b 통과 표본** — 두 재료 모두 이중층 자릿수 안. "전하이동" 이름표가 이 호에서는 적어도 크기 검사를 통과한다.

### ⚠ 이것이 곱을 푼 것은 아니다

θ 를 잰 관측은 0 이다. 1단계 판정은 `C ∝ θ` 전제 위이고, CPE → `C_eff` 는 Brug 근사(분산 TLM 에서 모형 의존)다. 기여는 **(a) 곱의 이름이 붙은 출생지 확인 (b) 규약 재척도의 대수 (c) 같은 지면 비교의 R·C 통과 · 편 간 비교의 면적 서명**이다.

---

# 9. Q2 · Q4 · Q5

- **Q2(독립 관측)**: 두께 4 점 × 2 재료 · 대칭 음극셀 · 전자 차단셀 · FIB-SEM/EDX — 전부 **신품, 열화 0**. 두께 가변은 `R_ion` ↔ `R_CT` 를 가르는 **방법 원전**(ref 36 Cronau 2020 을 ASSB 에 처음 옮긴 편이라고 저자 주장: "virtually no TLM-based studies on composite cathodes of ASSBs"). `LAM_PE` ↔ 접촉 손실은 대상이 아니다.
- **Q4(유일성)**: 0/50. **마흔두 번째 성질 "면적 규약을 적합 개선으로 골랐다 — 값이 τ 배 움직이는 선택을 기하 논증으로 하고, 곱만 보이는 극한의 값을 보고했다"**. 저자는 두꺼운 극한식을 인쇄했고(비식별의 **재료**는 지면에 있다) 그 극한에서 모형이 두께 추세를 못 따른다는 것도 인쇄했다("unclear") — 식별성 낱말 0.
- **Q5(Li-In 기준)**: 기준극 0 · 전위 축 "vs. In/InLi"(그림) · Li 대비 환산 0 · **음극을 대칭셀 반 빼기로 제거** — 음극 조성 40 at% · 조립 125 MPa 한 점을 ≈5–30 at% · 389 MPa 셀에서 뺐다(`[재현]` §5.6), `[도표]` LCO 52 µm 에서 허수부 부호 반전(≈10–120 Hz). `[해석]` **스물다섯 번째 형태 "대칭셀 반 빼기 — 상대극을 다른 셀 · 다른 압력 · 다른 조성에서 재어 뺀다"**. `dU/dc` 시작값은 **완전지 전압**의 기울기(S6 축 "Potential / V")라 음극 평탄을 암묵 가정한다(In–Li 2상역이면 성립, ≈5–30 at% 는 42호 창 ≈1–47 at% 안).
- **Q6(압력)**: 제조 = 운전 389 MPa 한 점(분리막 선압 97 · 대칭셀 125 · SE 펠릿 276). 초록 "under the application of stack pressures in the range of 400 MPa" 는 **압력을 바꾸지 않고** `j₀` 에 붙인 문장 — 결론이 "should be studied" 로 스스로 미룬다. 16호가 그 후속(97 ↔ 389)이다.

---

# 10. 채움표 행 (Q1–Q8)

| Q1 정량 | Q2 독립관측 | Q3 라벨층위 | Q4 유일성 | Q5 Li-In | Q6 압력 | Q7 dead Li | Q8 화학·OCP |
|---|---|---|---|---|---|---|---|
| **없다 — `θ(N)` 0/50.** 그러나 **`a_v = 3ε/r` "in contact to SE" 의 출생지**(16호가 옮긴 문장) — 접촉 분율 ≡ 1 을 이름 붙여 가정 · 초록이 `j₀` 를 접촉이 정한다고 정의 · FIB-SEM/EDX 단면은 반경에만 | **부분(신품, 방법 원전)** — 두께 4 점 × 2 재료로 `R_ion` ↔ `R_CT/(a_v d)` 분리(NMC 만 전이 구간 통과, LCO 는 전부 두꺼운 극한) · 대칭 음극셀 반 빼기 · 차단셀 σ_eon/σ_ion(σ_ion 은 총량의 5.6 % 차분) | **simulation-matched, 목적함수 미인쇄** — "simulations … compared" · 재료당 공유 6 파라미터(3 "freely adjustable" + 3 "variables" 시작값 문헌/OCV) + NMC 고주파 R‖CPE 적합 · ± 0 · n 미인쇄 | **0/50 — 마흔두 번째 성질 "면적 규약을 적합 개선으로 골랐다"**(수정 (ii) = `j₀` ×1/τ 재척도, 대수 미인쇄) + 두꺼운 극한(곱만 보임)의 LCO 값 보고, 모형 불일치 "unclear" → 비 논증 "no doubt" | 기준극 0 · "vs. In/InLi" · **대칭셀 반 빼기**(40 at% · 125 MPa → ≈5–30 at% · 389 MPa 셀, `[도표]` 허수부 부호 반전) — 스물다섯 번째 형태 | 389 MPa 제조 = 운전 한 점 · 압력 효과 주장은 미시험(결론이 미룸) — 16호가 후속 | 해당 없음(In 음극) | LCO + NMC 83\|6\|11(LiNbO₃) · `dU/dc` 시작 −2.024 / −3.358 × 10⁻⁵ → 적합 −2.65 / −3.59 × 10⁻⁵ V m³ mol⁻¹(×1.31 / ×1.07) · 완전지 1/30 C 평균 곡선(음극 평탄 가정) |

**칸 이동: 없음(≈20.0 → ≈20.0).** 근거가 되는 **논문의 측정 · 명제**가 카드 물음(Q1 θ 정량 · Q2 `LAM_PE` ↔ 접촉 분리 · Q4 식별성)에 닿지 않는다 — R·C 검사 · 규약 대수 · 음극 조성은 **우리 재계산**이라 반 칸 검토 후 접는다.

---

# 11. 어긋남 (실제로 어긋난 것만)

| # | 어긋남 | 근거 |
|---|---|---|
| D1 | 첫 방전 "good agreement with … 180−200 (LCO) · 190−200 (NMC)" ↔ `[도표]` Fig. 2 방전 ≈170 · ≈171 mAh g⁻¹ | 인용 범위 아래 |
| D2 | NMC 입경 본문 "3−6 μm" ↔ SI "4 – 6 μm" | |
| D3 | 두께는 공극 10 %(×1.1) · `ε_SE + ε_CAM` = 1.000(공극 제외) | `a_v·d` ×1.1 과대 → `j₀` ×1/1.1 |
| D4 | NMC Table 3 `R_CT/(a_v d)` 에서 역산 `j₀` 0.113 ↔ 인쇄 0.11(−2.7 % 일정) | 반올림 · 작다 |
| D5 | σ 측정 범위 −120 → 20 °C ↔ Table 1 T = 25 °C · 펠릿 276 MPa ↔ 셀 389 MPa | 25 °C 값의 출처 미기재 |
| D6 | SI σ_ion 1.3 × 10⁻⁴ S cm⁻¹ ⇒ τ ≈3.0 ↔ TLM τ 6.8(`R_ion` ×2.25) | 지면 논의 0 · σ_ion 분해능 낮음(§5.5) |
| D7 | Fig. 5a 뺀 뒤 −Z″ 가 ≈10–120 Hz 에서 그려지지 않음(음수 — 과차감) · Z′ 가 ≈10 → 100 Hz 에서 증가 | 본문은 "strongly affected" 만 |
| D8 | "Only `j₀`, `Q_DL`, β … freely adjustable" ↔ Table 2 "Variable" 에 τ · `dU/dc` · `D` 포함, `dU/dc` 는 시작값에서 ×1.31 · ×1.07 | 자유도 불명 |
| D9 | LCO: TLM 두께 무관 반원 ↔ 실험 감소 | 저자 인쇄 "unclear" — 값은 보고 |
| D10 | "Overall, there is a good agreement" ↔ `[도표]` 221 µm 모의 극소 ≈94 ↔ 실험 ≈82 | 가장 두꺼운 셀 과대(16호 207 µm 와 같은 방향) |
| D11 | "high-frequency semicircle shrinks with increasing cathode thickness"(LCO) ↔ `[도표]` Fig. 5b 끝점 32 µm ≈6.4 < 52 µm ≈7.3 | 단조 아님 |
| D12 | 초록 "under the application of stack pressures in the range of 400 MPa" — 압력 한 점 | 결론이 스스로 미룸 |
| D13 | refs 30 과 33 이 같은 편(Costard … Ivers-Tiffée 2021 *Energy Technol.* 9, 2000866) | 중복 인용 |
| D14 | 오기 "substaction"(p7) · Fig. 7 범례 "substraction" | 사소 |

---

# 12. 그림 — 무엇을 봤나

크로퍼가 **본문 8 + SI 7 = 15 장**(+ 표 4 장)을 잡았다. **12 장을 봤다**: Fig. 2 · 3 · 4 · 5 · 6 · 7 · 8 · S2 · S3 · S5 · S6 · S7.
**안 본 것**: Fig. 1(셀 모식도) · Fig. S1(SI 첫 사이클 곡선 — 본문 Fig. 2 와 같은 종류) · Fig. S4(LCO 단면 SEM/EDX). 표 4 장은 이미지로 읽지 않았다(PDF 텍스트).
추가로 **p4 · p5 쪽 렌더**로 식 (1)–(3) · (6) · 두 극한식 · 수정 (ii) 문장을 확인했다.
**본문 서술과 어긋난 그림**: Fig. 2(D1 용량) · Fig. 5a(D7 과차감 — 본문 무언급) · Fig. 5b(D11 비단조) · Fig. 7(D10 두꺼운 셀 과대). Fig. 8 은 본문과 일치(모의가 두께 무관).

---

# 13. 참고문헌 중 후속 후보 (52 편 + SI 4 편, 서지 기준 — 미열람)

| 서지 | ref | 왜 | 축 |
|---|---|---|---|
| **Bielefeld, Weber, Rueß, Glavas, Janek 2022 *JES* 169, 020539** | 35 | **큐 57** — FEM 형태 반영으로 NMC811\|LPSCl `j₀` ≈10⁻⁵ A cm⁻²(= 0.1 A m⁻²) — 이 편 NMC 0.11 과 ≈10 % 안. 형태 반영 모델이 **실접촉 면적**을 썼다면 규약이 다른 두 값의 일치 | 곱 · 규약 |
| **Kaiser, Spannenberger, Schmitt, Cronau, Kato, Roling 2018 *JPS* 396, 175** | 24 · SI 2 | τ 시작값의 출처 · 대칭셀 TLM(10호 ref 57) — 10호(ref 57) · 48호 digest 후속(ref 23)에 이어 **다시 지목** | Q2 · τ |
| **Cronau, Kroll, Szabo, Sälzer, Roling 2020 *Batter. Supercaps* 3, 611** | 36 | 두께 가변 TLM 의 원형(이온 액체) — 극한식 출처 | Q2 · Q4 |
| **Morasch, Keilhofer, Gasteiger, Suthar 2021 *JES* 168, 080519** | 34 | 액체 두께 가변 TLM · 극한식 · 비이상 CPE 근거 — 면적 규약 대조 | 규약 |
| **Hess … Cuniberti 2015 *JPS* 299, 156** | 31 | 비교 기준 LCO 0.4 A m⁻² 의 원전(GITT 비대칭 BV) — 면적 규약 확인 | 비교 유효성 |
| Chaouachi … Bultel 2021 *Electrochim. Acta* 366, 137428 | 32 | NMC622 2–4 A m⁻² 원전 | 비교 유효성 |
| Huang & Zhang 2016 *JES* 163, A1983 | 46 | 식 (1)의 출처 — `a_v·l` 규약의 원래 뜻 | 규약 |
| Kroll … Roling · Tallarek 2021 *JPS* 505, 230064 | 37 · SI 1 | 공극 10 % 가정의 출처(형태 연구) | 두께 |
| **Minnmann, Quillman, Burkhardt, Richter, Janek 2021 *JES* 168, 040537** | SI 4 | 원장 "TLM 원전" · 차단셀 부분 전도도 방법 | Q2 |
| Haruyama … Tateyama 2014 *Chem. Mater.* 26, 4248 | 52 | LCO ↔ NMC 차이 설명 후보(공간전하층) | `k` 쪽 |

**큐 52–59 인용**: **57 Bielefeld 2022 만**(ref 35). 52 Illig 2012 · 53 Oh 2025 · 54 Ren 2023 · 55 Neumann 2021 · 56 Hlushkou 2018 · 58 Bielefeld 2020 · 59 Asheri 2023 — 인용 0.

---

# 14. 이 digest 가 주장하지 않는 것

- **`j₀` 25.8 · 0.11 이 틀렸다고 주장하지 않는다.** 주장하는 것은 **그 값이 `j₀·(접촉 분율)` 이고, 면적 규약 한 줄이 ×τ 를 정한다**는 것까지다 — 근거는 논문 자신의 식 (1)(5)(7)과 수정 (ii) 문장이다.
- **"LCO 가 NMC 보다 `j₀` 가 높다" 를 흔들지 않는다.** R·C 는 그 비교를 **지지**한다(τ ×106). 단서는 `C ∝ θ` 전제 · Brug 근사 · n 미인쇄.
- **16호가 틀렸다고 주장하지 않는다.** 편 간 R·C 가 면적 서명을 준다는 것은 **다른 SE 사이에서 면적당 이중층 용량이 같다는 약한 전제 위의 우리 계산**이다. 주장은 "16호의 SE 전도도 서사가 접촉 면적과 구별되지 않는다" 까지.
- **16호의 `ε` 값이 이 편 LCO 칸의 복사라고 주장하지 않는다.** 셋째 자리 일치와 필요한 밀도(≈2.03 g cm⁻³)까지다.
- **과차감(Fig. 5a)의 원인이 음극 조성 · 압력 불일치라고 확정하지 않는다.** 그림 판독(로그 축에서 점 부재) + 조성 계산(비가역 Li 위치 가정)의 **방향 정합**까지다.
- **σ_ion(SI) ↔ τ 불일치를 반례로 쓰지 않는다** — σ_ion 이 총량의 5.6 % 차분이라 분해능이 없다.
- **`r_CAM` 이 1 µm 대라고 주장하지 않는다** — S3 · S5 는 사진 판독이고 저자는 공급자 값과 일치한다고 적었다. 주장은 "반경이 수치로 측정되지 않았다" 까지.
