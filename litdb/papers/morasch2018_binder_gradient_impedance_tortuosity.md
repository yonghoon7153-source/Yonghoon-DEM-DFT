<!-- digest 표준 양식 확장 (paper-level STANDALONE).  ★ = 사용자가 특히 원한 항목.
     깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md · τ 묶음 형식 기준 = landesfeind2016_… · landesfeind2018_… · siroma2015_… · tjaden2018_… · taufactor_… 카드.
     이 논문은 DEM/MPM 이 아니라 액체 전해질 LIB 흑연 전극의 (i) 불균일 이온 저항 RC 전송선 모형 (COMSOL) 모의 + (ii) 건조 온도로 만든 바인더 구배의 EDS 정량 +
     (iii) 차단 대칭셀 EIS 겉보기 τ + (iv) 율속 시험 논문이다.  그래서 §4 = 모의 → 방향 가중 원리 → 실험 사슬, "§ τ 정의 대조" 를 §7 뒤에 두고,
     §8 = 이 묶음이 닫는 항목 ("구배 전극의 방향 의존 τ — graded-z").
     쪽 표기 = 학술지 인쇄 쪽 A3459–A3467.  PDF 10 쪽 중 1 쪽은 IOP 표지 + "You may also like" (본문 아님) → PDF n 쪽 = 학술지 A(3457 + n).  SI 없음 (본문이 SI 를 인용하지 않는다).
     식 번호: 이 논문에는 번호 붙은 식이 하나도 없다 (본문 · 캡션 전수).  그림 번호 = 원문.  그림 · 수식이 든 쪽은 렌더해서 읽었다.
     값 표지: stated = 본문 · 캡션 · 그림 안 인쇄 숫자 / 판독 = 그림에서 읽은 근사 (TREND 전용 — 그림 6 은 벡터 그림이라 좌표에서 0.01 단위로 읽었지만 여전히 판독) /
     파생 = 카드 작성자 계산 (식 명시) / 우리 유도 = 원문에 없는 식을 카드 작성자가 끌어낸 것 (수치 검산 기록 §4-4). -->
# 차단 EIS 의 겉보기 τ 는 방향을 본다 — 같은 총 이온 저항이라도 분리막 쪽에 몰리면 +25 · +66 %, 집전체 쪽이면 −25 · −46 % (RC 전송선 모의) · 급속 건조 바인더 구배로 겉보기 τ 3.4 → 5.7, 같은 전극을 뒤집으면 2.7 · 위상각 극소로 구배 검출 — Morasch (J. Electrochem. Soc. 2018)

> slug `morasch2018_binder_gradient_impedance_tortuosity` · DOI `10.1149/2.1021814jes` · type `exp + model (COMSOL RC-TLM 차단 EIS 모의 · EDS 바인더 구배 · 차단 대칭셀 겉보기 τ · 정/역 조립 · 율속; liquid-LIB graphite)` · PDF `27. Detection of binder gradients using impedance spectroscopy and their influence on the tortuosity of Li-ion battery graphite electrodes.pdf` · digested `2026-10-03` · status ✅
>
> ★ **정의 판정 (이 카드의 목적)** — 이 논문의 τ 는 *"electrode resistance tortuosities (τ)"* (A3465) · *"apparent tortuosity"* (A3463–A3466) 이고 **식이 인쇄되어 있지 않다**: *"determined using the electrolyte bulk conductivity (κ = 0.258 mS/cm), the electrode porosity (ε = 0.55), and the measured electrode thickness (ranging from 245 to 260 μm), as described in Ref. 18"* (A3465).  Ref. 18 = Landesfeind 2016 → 대칭셀 Eq 13 `τ = R_Ion·A·κ·ε/(2d)` (그 카드 §4, A1382) — **제곱 없는 tortuosity factor = 우리 tau2**.  그림 6a 곡선을 벡터 좌표로 외삽해 이 식으로 되계산하면 그림 6d 평균 (3.40–5.85) 을 감싸는 범위 (2.3–6.4) 가 나온다 (§4-6, 파생) → √ 관례 (≈ 1.5–2.5) 가 아님이 확인된다.  "MacMullin" · "tortuosity factor" · "effective tortuosity" · "Bruggeman" 낱말은 **0 회** (전수 검색).
> ★ **측정 경로** — 비삽입 염 (TBAClO₄) 차단 대칭셀 EIS + 균질 RC 전송선 모형 (TLM) 해석 = Nguyen 2020 분류의 **eSCM → τ_e 계열**, 경계는 **반사형** (집전체에서 이온 전류 0).  원문이 직접 대비한다: *"This is in contrast to a setup with transmissive boundary condition, where the measured apparent resistance is directionally independent … all of the resistance profiles shown in Fig. 3 would yield the same apparent resistance (hence the same apparent tortuosity)"* (A3463).  ⇒ **우리 tau2 (DEM 접촉망 · STEP3 복셀) = 투과형 (방향 무관) 쪽**이다.
> ★ **핵심 결과** — ① 모의 (총 이온 저항 고정): 선형 1.5 : 0.5 구배 **±25 %** · 1/4 두께 2.5 배 계단 **−46 % / +66 %** (A3462–A3463, stated) ② 실험 (같은 조성 · 적재 · 두께): 겉보기 τ **RT 3.40 → 125 °C 5.73**, 같은 125 °C 전극을 **뒤집어 조립하면 2.70** (그림 6d 판독 · 원문 "~2.7") ③ 위상각 극소 (저주파) 가 구배의 존재 · 방향 지표 ④ **같은 겉보기 τ (4.4–4.6) 인데 율속이 크게 다르다** (그림 7).
>
> 출처 PDF = `litdb/inbox/27. ….pdf` (10 쪽).  PDF 1 쪽 = IOP 표지 (본문 · 인용 아님).  본문 = PDF 2–10 쪽 = **A3459–A3467**.  보충자료 (SI) 없음.

---

## 0. 결론 먼저

| 질문 | 답 | 근거 (쪽) |
|---|---|---|
| 이 논문의 τ 는 τ 인가 τ² 인가? | **제곱 없는 τ** (Ref. 18 = Landesfeind 2016 Eq 13 · 식은 이 논문에 미인쇄) = 우리 **tau2** 정의식 | A3465 · 그림 6a 외삽 되계산 (§4-6, 파생) |
| 어느 측정 계열인가? | 차단 대칭셀 EIS (반사 경계) → **τ_e 계열의 "겉보기" 값** — 저자도 *"apparent tortuosity"* 로 부른다 | A3460 · A3463 · A3466 |
| 불균일 이온 저항 TLM 의 식은? | **원문에 없다** — COMSOL 전지 모듈 (Newman 모형, 패러데이 반응 끔) 수치 모의 + 그림 2 회로도뿐.  해석적 선행 연구 (Refs 11–13) 는 인용만.  카드 유도: 균일 용량이면 저주파 겉보기 저항 = ∫₀ᴸ r(x)(1 − x/L)² dx (x = 분리막에서 깊이) — 원문 네 수치 (~25 · ~25 · ~46 · ~66 %) 를 반올림 안에서 재현 (−25.0 · +25.0 · −46.9 · +65.6 %) | A3459 · A3460 · §4-4 (우리 유도) |
| 구배가 겉보기 τ 를 얼마나 바꾸나 (모의) | 같은 총저항에서 lb **−25 %** · lt **+25 %** · sb **−46 %** · st **+66 %** | A3462–A3463 (stated) |
| 실험에서는? | RT **3.40** · 50 °C **4.53** · 75 °C **5.13** · 100 °C **5.85** · 125 °C **5.73** · 125 °C 역조립 **2.70** (± 0.15–0.29, n = 4) · 원문 배율 R_ion "~1.4-fold" (50 · 75 °C) · "~1.7-fold" (100 · 125 °C) | 그림 6d (판독) · A3464 (stated) |
| 같은 전극의 방향 효과 (실험) | 125 °C 정 / 역 = 5.73 / 2.70 = **2.12 배** — 모의 선형 쌍 1.67 배와 계단 쌍 3.12 배 사이 (파생) | 그림 6d · §8-3 |
| 바인더 구배 검출법 | HFR 보정 위상각 그림의 **저주파 극소** — 기준보다 깊으면 분리막 쪽 고저항, 45° 위 극소 (~47°) 면 집전체 쪽 고저항.  고주파 위상은 HFR ±1–2 % 오차로 못 쓴다 | A3462–A3465 · 그림 6c |
| 균질 TLM 으로 맞추면? | *"apparent tortuosities which obviously cannot be directly applied to a macro-homogeneous battery model"* · *"Any calculated tortuosity is a mere apparent tortuosity"* — 편향의 크기는 모의에서만 정해진다 (실험엔 방향 무관 기준값이 없다) | A3466 |
| 결정 13 (τ_e 는 z 균질도를 요구) | **확인 + 크기 부여**.  dead-end 가 없어도 z 구배만으로 τ_e 형 측정이 투과형 tau2 에서 −46 … +66 % (모의) 벗어나고 부호는 방향이 정한다 → "부호 불정" 유지 · 권고 변경 없음.  진단 하나 추가 제안 (z 단면 저항 → 반사 가중 인자 F_z, §8-5) | §8-5 |
| 우리 솔버는? | DEM 접촉망 · STEP3 = 투과형 (방향 맹).  STEP4 (`scripts/step4_dyn.py:1086–1088`: 아래 집전체 φ_e = V_app · 위 분리막 φ_i = 0) 는 이온이 위에서만 들어오는 반사형 배치라 방향을 본다 | §7 |

## 1. 한 줄 요약
급속 건조로 PVDF 바인더가 전극 윗면 (분리막 쪽) 으로 몰리면 율속이 나빠지는 이유를 찾으려고, (i) 이온 저항 R_ion 이 두께 방향으로 고르지 않은 다공 전극의 차단 EIS 를 RC 전송선 모형으로 모의해 **같은 총저항이라도 고저항층이 분리막 쪽이면 겉보기 R_ion 이 커지고 (+25 · +66 %) 집전체 쪽이면 작아지며 (−25 · −46 %), 위상각 그림에 특징적인 극소/극대가 생김**을 보이고, (ii) 실온–125 °C 로 건조한 두꺼운 흑연 전극 (~245 µm) 의 바인더 구배를 EDS 단면으로 정량한 뒤 같은 전극의 차단 대칭셀 EIS 에서 **겉보기 τ 가 3.4 → 5.7 로 오르고 위상 극소가 깊어지며, 같은 125 °C 전극을 뒤집어 조립하면 2.7 로 떨어짐**을 확인하고, (iii) 얇은 전극 (~74 µm) 에서 **겉보기 τ 가 같아도 (4.4–4.6) 바인더 구배가 큰 쪽의 충전 율속이 크게 나쁨**을 보인다.
우리에게는 **(a) τ_e 계열 (반사 경계) 측정이 z 구배에 방향 가중으로 반응하는 크기 (b) 투과형 tau2 (우리 두 솔버) 는 그 방향을 원리적으로 못 본다는 원문 진술 (c) 구배 검출 · 정/역 조립이라는 실험 설계** 를 준다.  수치는 액체 LIB 흑연이라 전이 불가.

## 2. 메타

| 저자 | 저널/년 | DOI | 재료계 | 연구유형 |
|---|---|---|---|---|
| **Robert Morasch** (교신 · ECS student member), Johannes Landesfeind, Bharatkumar Suthar (ECS member), **Hubert A. Gasteiger** (ECS fellow) — Chair of Technical Electrochemistry, Department of Chemistry and Catalysis Research Center, Technical University of Munich | **J. Electrochem. Soc. 165 (14) A3459–A3467 (2018)** | **10.1149/2.1021814jes** | 흑연 (Timcal T311, D50 19 µm, 3 m²/g) : PVDF (Arkema) = 95 : 5 wt, Cu 집전체, NMP 슬러리, 미압축 (ε ~55 %).  차단 전해질 = ~10 mM TBAClO₄ in EC:EMC 3:7 (wt), κ 0.258 mS/cm (25 °C) · 율속 = LP57 | **실험** (EDS 단면 · 차단 대칭셀 EIS · 3 전극 율속) + **모의** (COMSOL 전지 · 연료전지 모듈, Newman 모형, 패러데이 반응 끔 = RC-TLM) |

- 접수 2018-08-29 · 수정본 2018-10-12 · 게재 2018-11-08.  **Open access CC BY-NC-ND 4.0** (A3459).
- 연구비: BMWi SurfaLIB (03ET6103F) — R.M. / BMBF ExZellTUM II (03XP0081) — J.L. · B.S.  사의: Ana Marija Damjanović (단면 측정) (A3467).
- 참고문헌 26 편 (A3467).  Ref. 17 = Landesfeind 2018 (`landesfeind2018_tortuosity_impedance_vs_tomography`) · Ref. 18 = Landesfeind 2016 (`landesfeind2016_tortuosity_eis_electrodes_separators`) · Ref. 20 = Cooper 2017 (반사 ↔ 투과 경계 — 이 묶음 inbox 25 번).

## 3. 핵심 수치 (이 논문이 주는 것)
> 우리 소재 물성 앵커 (porosity@P · σ_ion/e/thermal · E_SE · coverage · Z · Heckel) 는 **주지 않는다** → 전부 n/a.  주는 것은 ① 불균일 R_ion 의 차단 EIS 모의 결과, ② 건조 속도 ↔ 바인더 구배 (EDS), ③ 같은 전극들의 겉보기 τ · 위상 극소, ④ 같은 겉보기 τ · 다른 율속.

| 양 | 값 | 조건 | 표지 | 쪽 |
|---|---|---|---|---|
| 모의 매개변수 | 전극 50 µm × 260 µm (폭 × 두께, 2D · "1D 로도 충분") · κ **0.258 mS/cm** · σ_s **10 S/cm** · ε_l **55 %** (두께 방향 균일) · 분리막 50 µm (다공도 · τ = 1) · 기준 τ **5** · c_dl **0.2 F/m²_BET** · r_p 10 µm · **a_dl = 3·(1−ε_l)/r_p = 1.35 × 10⁵ m²/m³** · 섭동 20 mV · 0.01 Hz–10 kHz · HFR 보정 | COMSOL 전지 모듈, 패러데이 반응 끔 | stated | A3460 · 그림 4 캡션 |
| 모의의 전제 | 전자 저항이 다공 전극 안 이온 저항보다 **두 자릿수 이상 작을 것** | — | stated | A3460 |
| 대표 R_ion | **~1 kΩ cm²** (두꺼운 전극 · 차단 전해질에서 얻은 값의 대표) · Nyquist 축은 R_ion/1.5 로 정규화 | — | stated | A3461 |
| 매개변수 산술 | R_ion = L·τ/(κ·ε) = **916 Ω cm²** (τ 를 1 승으로 넣은 경우) · τ² 관례면 4.58 kΩ cm² · C_tot = c_dl·a_dl·L = **0.70 mF/cm²** | 위 값 | 파생 | — |
| 균질 기준 (ng) | 45° 평탄 뒤 **~43.4°** 작은 우묵 → 용량성 상승 | — | stated | A3461 |
| lb (선형, 집전체 쪽 1.5 배 → 분리막 쪽 0.5 배) | 겉보기 R_ion **~25 % 감소** · 위상 45° 에서 계속 올라 **~48.6° (~0.3 Hz)** 중간 극대 → 다시 상승 | 총저항 = ng | stated | A3462 |
| lt (선형, 반대) | **~25 % 증가** · 극소 **~40.3° (~0.1 Hz)** | 총저항 = ng | stated | A3462 |
| sb (집전체 쪽 1/4 두께 2.5 배) | **~46 % 감소** · 아주 얕은 극소 **~44.5°** | 총저항 = ng | stated | A3463 |
| st (분리막 쪽 1/4 두께 2.5 배) | **~66 % 증가** · 극소 본문 **"~39.1°"** ↔ 그림 4b **≈ 33.6°** (판독) | 총저항 = ng | stated / ⚠ 불일치 (§10) | A3463 · 그림 4b |
| 카드 재계산 (같은 매개변수 RC 사다리 4000 요소) | 겉보기 R 비 **1.000 · 0.750 · 1.250 · 0.531 · 1.656** (ng · lb · lt · sb · st) · 위상 극소 **43.39° · 48.59° (옆 극대 48.95°) · 40.34° · 44.43° · 33.58°** | 원문 매개변수 | 파생 (§4-4) | — |
| PVDF 부피분율 | 고체의 **~6 %** · 전극 부피의 **~2.7 %** (95/5 wt, 밀도 ~2.2 · ~1.8 g/cm³, ε ~55 %) | — | stated (카드 재계산 6.04 % · 2.72 %) | A3463 |
| 건조 (IR 램프, Al 판 온도) | 125 °C (28 cm) **~2 min** · 100 °C (41 cm) **~7 min** · 75 °C (63 cm) **~18 min** · 50 °C (91 cm) **~90 min** · RT (램프 끔) **수 시간** (그림 6d 에선 8 h 로 둠) | 습막 500 µm (EIS · EDS) · 150 µm (율속) | stated | A3460 · 그림 6 캡션 |
| 건조 전극 | EIS · EDS용 **~245 µm (±6 %)** · **~25.5 mg/cm² (±6 %)** / 율속용 **~74 µm (±2 %)** · **~7.4 mg/cm² (±2 %)** · **~2.4 mAh/cm²** (350 mAh/g 기준) · 미압축 · ε **~55 %** (두께 + 면적 무게) · 지름 10.95 mm (~0.94 cm²) | — | stated | A3460 |
| EDS 바인더 프로파일 (정규화 F 신호, 5 구간 중점 0.1 → 0.9 = 집전체 → 분리막; 1.0 = 5 % 바인더) | RT 1.23 · 1.00 · 0.98 · 0.92 · 0.91 / 50 °C 0.87 · 0.82 · 0.88 · 1.10 · 1.35 / 75 °C 0.66 · 0.65 · 0.87 · 1.20 · 1.65 / 100 °C 0.27 · 0.35 · 0.80 · 1.35 · 2.22 / 125 °C −0.12 · 0.11 · 0.50 · 1.00 · 3.53 (각 줄 평균 ≈ 1.00 — 캡션 정규화와 정합) | 그림 5b | 판독 | A3463 |
| 겉보기 τ (4 회 평균 ± SD) | RT **3.40 ± 0.29** · 50 °C **4.53 ± 0.15** · 75 °C **5.13 ± 0.23** · 100 °C **5.85 ± 0.26** · 125 °C **5.73 ± 0.25** · 125 °C 역조립 **2.70 ± 0.18** (원문 "~2.7") | ε 0.55 · κ 0.258 · 두께 245–260 µm | 판독 (그림 6d 벡터 좌표) · 역조립만 stated | 그림 6d · A3465 |
| 위상각 극소 | RT **43.1°** · 50 °C **42.0°** · 75 °C **39.9° (±1.0)** · 100 °C **34.4° (±1.1)** · 125 °C **32.9° (±1.3)** · 역조립 **46.8°** (~1 Hz 마지막 평탄 · 원문 "~47°") — RT · 50 °C · 역조립의 오차막대는 표지 안 (≲ ±0.5°) | 그림 6d | 판독 · 역조립 stated | 그림 6d · A3465 |
| 겉보기 R_ion 배율 (RT 대비) | **~1.4 배** (50 · 75 °C) · **~1.7 배** (100 · 125 °C) | 그림 6a 예시 곡선 | stated | A3464 |
| 같은 배율 (그림 6d 평균) | 1.33 · 1.51 · 1.72 · 1.69 · 역조립 0.79 | — | 파생 | — |
| HFR 민감도 | HFR **226 Ω** (75 °C 시료) · **±2 Ω (≈ ±1 %)** · **±4 Ω (≈ ±2 %)** 만으로 극소보다 높은 주파수 (**> ~1–2 Hz**) 의 위상이 크게 흔들림 · 첫 표지 주파수 **37 Hz** 가 Nyquist 원점 근처인데 위상 그림의 **~50 %** 를 차지 | 그림 6c | stated | A3464–A3465 |
| 얇은 전극 겉보기 τ | 75 °C **4.6 ± 0.03** · 125 °C **4.4 ± 0.3** (원문 "4.4–4.6") | ~74 µm | stated (그림 안 인쇄) | 그림 7a · A3465 |
| 얇은 전극 위상 극소 | 75 °C ≈ **43.2°** · 125 °C ≈ **40.6°** (둘 다 ≈ 5.7 Hz) | 그림 7a | 판독 | A3466 |
| 충전 (리튬화) 용량 75 °C / 125 °C | C/5 ≈ 331 / 275 · C/2 ≈ 310 / 224 · 1C ≈ 267 / 154 · 1.5C ≈ 201 / 89 · 2C ≈ 138 / 51 · 2.5C ≈ 93 / 34 · 3C ≈ 67 / 27 · 5C ≈ 35 / 14 mAh/g · C/10 둘 다 ≈ 330–345 · 10C 둘 다 < 20 | 0.01–1.5 V vs Li 기준전극, 셀 3 개 평균 ± SD | 판독 (원문은 숫자 없이 "inferior performance") | 그림 7b · A3465 |

## 4. 방법 ★

### 4-1. 정의 · 식 — 이 논문에는 번호 붙은 식이 없다

| 자리 | 원문 형태 (그대로) | 쪽 | 뜻 · 단서 |
|---|---|---|---|
| τ 결정 | *"electrode resistance tortuosities (τ) were determined using the electrolyte bulk conductivity (κ = 0.258 mS/cm), the electrode porosity (ε = 0.55), and the measured electrode thickness (ranging from 245 to 260 μm), as described in Ref. 18"* | A3465 | 식 미인쇄.  Ref. 18 = Landesfeind 2016 Eq 13 `τ = R_Ion·A·κ·ε/(2d)` (대칭셀 두 전극 합 R_Ion · 2016 카드 §4 기록) |
| R_ion 추출 | *"obtained from the HFR-corrected Nyquist plots in Fig. 6a by interpolating the low frequency data to the Re(Z)-axis"* | A3465 | 그래프법 (2016 Eq 12 계열: 저주파 가지 실축 절편 = R_Ion/3).  외삽 창은 적혀 있지 않다 |
| 유일한 인라인 식 | `a_dl = 3 × (1−ε_l)/r_p = 1.35 × 10⁵ m²/m³` | A3460 · 그림 4 캡션 | 구형 입자 비표면적 (입자 표면적 / 전극 부피) |
| 정규화 | Nyquist 실 · 허수부를 **(R_ion/1.5)** 로 나눔 — *"corresponds to the ionic resistance in the electrolyte phase of one porous electrode in the symmetric cell, namely to 2/3 × Re(Z) in the symmetric cell"* | A3461 | 대칭셀 저주파 절편 = 2 × R_ion/3 = R_ion/1.5 → ng 의 수직선이 **1.0** 에 선다 (그림 4a 점선 = 1.0 확인).  "2/3 × Re(Z)" 문구는 관계가 거꾸로 읽힌다 (§10) |
| 총저항 고정 | *"Note that the total ionic resistance summed up over the entire electrode thickness is the same in all cases."* | 그림 3 캡션 (A3462) | 다섯 프로파일 = **같은 투과형 저항 · 같은 두께 평균 τ** |
| 저항 변화 = τ 변화 | *"The ionic resistance within the porous electrodes (i.e., the tortuosity, since the porosity was set constant) was then varied linearly or stepwise"* | A3460 | 국소 R_ion ∝ 국소 τ/ε → 국소 tau2 프로파일 |
| 방향 가중 | *"higher current flows through the resistances near the separator region than the current collector region (reflective boundary condition case)"* · 투과형이면 *"weighed solely by their thickness fraction"* | A3463 | §4-4 |

- **카드 유도 (우리 유도 — 원문에 없음)**: 이중층 용량이 두께 방향으로 균일하고 (원문 가정: ε · 비표면적 균일, A3460) 전자 레일 저항이 0 이면, 저주파에서 깊이 x (분리막 = 0, 집전체 = L) 의 기공 이온 전류는 그 아래 남은 용량에 비례해 I·(1 − x/L) 이고, 소산 = ∫ r(x) I²(1 − x/L)² dx 이므로
  **R_app = ∫₀ᴸ r(x)·(1 − x/L)² dx** · 균질이면 R_ion/3 (2016 Eq 12 의 1/3 규칙).
  ⇒ 겉보기 / 투과형 비 **F = ∫₀¹ (r/r̄)·3(1 − u)² du** (u = x/L).  이것은 `siroma2015_…` 카드 §3-5 일반식 ∫ r(1 − C(x)/C_tot)² dx 의 균일 용량 판이다.
  재현 (파생): lb 0.7500 · lt 1.2500 · sb 0.5312 · st 1.6562 — 원문 "~25 · ~25 · ~46 · ~66 %" 와 반올림 안에서 일치 (§4-4).

### 4-2. 논증 순서 (사슬)

| 단계 | 질문 | 방법 | 결과 | 쪽 |
|---|---|---|---|---|
| ① | 두께 방향 R_ion 구배가 차단 EIS 에 어떻게 보이나 | COMSOL RC-TLM, 총저항 고정 다섯 프로파일 (그림 3) | 겉보기 R_ion ±25 · −46/+66 % · 위상 극소/극대 (그림 4) | A3461–A3463 |
| ② | 왜 방향이 문제인가 | 반사 경계 ↔ 투과 경계 비교 (Refs 20–22) | 분리막 쪽 저항이 더 무겁게 잡힌다 · 투과형이면 방향 무관 | A3463 |
| ③ | 바인더 구배를 실제로 만들 수 있나 | 건조 온도 (= 건조 속도) RT–125 °C | 고온일수록 윗면 (분리막 쪽) 바인더 집중 (그림 5) | A3460 · A3463–A3464 |
| ④ | 그 구배가 R_ion 구배로 보이나 | 같은 전극 차단 대칭셀 EIS (그림 6a · b) | 겉보기 R_ion ~1.4 → ~1.7 배 · 위상 극소 깊어짐 = 모의 lt/st 쪽 | A3464–A3465 |
| ⑤ | 방향을 뒤집으면 | 125 °C 자립 전극을 뒤집어 조립 | 겉보기 R_ion ↓ (τ ~2.7) · 극소 ~47° (45° 위) = 모의 lb 쪽 | A3465 |
| ⑥ | 고주파 위상을 믿을 수 있나 | HFR ±2 · ±4 Ω 감도 (그림 6c) | 극소 위쪽 (> ~1–2 Hz) 은 못 쓴다 · 극소 크기는 강건 | A3464–A3465 |
| ⑦ | 성능과 연결되나 | 얇은 전극 75 vs 125 °C (그림 7) | 겉보기 τ 같은데 125 °C 의 극소가 깊고 충전 율속이 나쁨 | A3465–A3466 |

### 4-3. 모의 — 다섯 프로파일 (그림 3 · 그림 4, A3461–A3463)

| 프로파일 (그림 3) | 정의 (평균 R_ion 대비 · 위치 0 = 집전체, 1 = 분리막) | 원문 겉보기 R_ion | 원문 위상 특징 | 카드 재계산 R 비 | 카드 재계산 위상 | 그림 4b 판독 |
|---|---|---|---|---|---|---|
| ng ("no gradient") | 1.0 균일 | 기준 | 45° 평탄 → ~43.4° 우묵 | 1.000 | 43.39° | ≈ 43.4° @ ≈ 0.12 Hz |
| lb ("linear bottom") | 1.5 (집전체) → 0.5 (분리막) 선형 | ~ −25 % | 45° 에서 계속 상승 → ~48.6° @ ~0.3 Hz 중간 극대 → 다시 상승 | 0.750 | 극소 48.59° · 옆 극대 48.95° | 극소 ≈ 48.6° @ ≈ 0.15 Hz · 극대 ≈ 48.9° @ ≈ 0.27 Hz |
| lt ("linear top") | 0.5 (집전체) → 1.5 (분리막) 선형 | ~ +25 % | 극소 ~40.3° @ ~0.1 Hz | 1.250 | 40.34° | ≈ 40.3° @ ≈ 0.1 Hz |
| sb ("step bottom") | 집전체 쪽 1/4 두께 2.5 · 나머지 0.5 | ~ −46 % | 아주 얕은 극소 ~44.5° (저주파) | 0.531 | 44.43° | ≈ 44.5° @ ≈ 0.5 Hz |
| st ("step top") | 분리막 쪽 1/4 두께 2.5 · 나머지 0.5 | ~ +66 % | *"significantly more pronounced phase angle minimum of ∼39.1°"* | 1.656 | **33.58°** | **≈ 33.6°** @ ≈ 0.1 Hz (+ 작은 극대 ≈ 45.6° @ ≈ 0.8 Hz) |

- 그림 4a (Nyquist, R_ion/1.5 정규화): 수직 점근선 ng **1.0** · lb ≈ 0.75 · sb ≈ 0.53 · lt ≈ 1.25 · st ≈ 1.66 (판독) — 원문 백분율과 정합.  st 는 45° 직선 뒤 ≈ 0.85–0.9 높이의 어깨를 지나 수직으로 꺾인다 (판독).
- 원문 요지: *"linear R_ion gradients across the thickness of a porous electrode affect the apparent R_ion values, and their presence and direction is indicated by characteristic maxima/minima in modeled phase angle plots"* (A3462).
- **주파수 축 (파생 · 원인 [미확인])**: 원문 매개변수 (C_tot 0.70 mF/cm², R_ion 916 Ω cm²) 로 계산한 극소는 1.4–6.5 Hz 인데 그림 4b 는 ≈ 0.1–0.5 Hz — **약 16 배 낮다**.  원문은 *"the modeled Bode plots are specific to a given modeled electrode"* (A3461) 라 적는다.  각도 · 겉보기 R 비는 R·C 척도와 무관하므로 위 표의 핵심 값에는 영향 없음.

### 4-4. 방향 가중의 원리 — 반사 경계 ↔ 투과 경계 (A3463) + 카드 검산

- 원문 (A3463): 용량 sink 가 전극 전체에 고르게 있으면 *"higher current flows through the resistances near the separator region than the current collector region (reflective boundary condition case)"*.  *"No ionic current passes through the current collector. Hence a resistance at the top (electrode/separator interface) is weighed higher than a resistance at the bottom."*  투과형 (transmissive) 이면 *"the resistances through the electrode are weighed solely by their thickness fraction of the electrode"* → 그림 3 의 모든 프로파일이 같은 겉보기 저항 · 같은 겉보기 τ (Refs 20–22).
- 적용 범위 (원문, A3463): 이 RC-TLM 기술은 **두 상 계 (바인더 + 흑연)** 에 맞다.  도전 탄소 · 첨가제가 있는 양극에서는 전제 (낮은 전기 저항) 가 깨져 *"could lead to data misinterpretation"* (Ref. 17).
- **카드 검산 (파생)**: 위 §4-1 식의 가중 w(u) = 3(1 − u)² 로 보면, **균질 전극의 저주파 겉보기 저항의 57.8 % 가 분리막 쪽 1/4 두께에서 · 1.6 % 가 집전체 쪽 1/4 두께에서** 온다 (분리막 쪽 절반 87.5 %).
  - 같은 매개변수의 RC 사다리 (4000 요소) 와 de Levie 해석해 √(R/jωC)·coth√(jωRC) 로 ng 를 풀면 극소 43.40° (ωRC ≈ 7.7) · 저주파 Re/(R/3) = 1.0000 — 원문 43.4° 그대로.
  - 정 · 역 쌍 (프로파일을 뒤집은 짝): 선형 lt/lb = **1.667** · 계단 st/sb = **3.118**.  가중의 정 · 역 평균 1.5[(1 − u)² + u²] 의 범위는 **0.75–1.5** 이므로, 정 · 역 두 겉보기 값의 평균은 **선형 구배에서 투과형 값과 정확히 같고** (lt · lb 평균 1.000) 1/4 계단에서는 1.094 배로 크다.  일반 분포에서 투과형 값은 [평균/1.5, 평균/0.75] 안이다.
  - `siroma2015_…` 카드의 2 층 3 : 1 예 (±37.5 %) 도 같은 가중으로 재현된다 (1.375 · 0.625).

### 4-5. 전극 제조 · 건조 · EDS 바인더 구배 (A3460 · A3463–A3464 · 그림 1 · 그림 5)
- 슬러리: 흑연 T311 : PVDF = 95 : 5 (wt), NMP 와 고 : 액 = 5 : 4 (wt), Thinky ARV-310 2000 rpm 5 분 → 유리판 위 Cu 박 (MTI, 12 µm) 에 gap bar coater (RK PrintCoat).
- 건조: IR 램프 (IH2000IR, ELV, 1300 W) 아래 Al 판, 램프-판 거리로 판 온도 (열전대) 조절 → 판 위에 코팅 유리판을 놓고 눈으로 마를 때까지 (시간은 §3 표).  원문 강조: 바인더 구배의 구동력은 온도가 아니라 **건조 속도** (A3463).
- EDS 시편: 두꺼운 전극의 집전체를 손으로 벗겨 Al 판 (1 × 1 × 0.1 cm) 두 장 사이에 끼우고 수지 (EpoThin 2, Buehler) 진공 함침 → SiC P320 · P1200 · 다이아몬드 9 µm (TexMet C) 연마 → JEOL JCM-6000 SEM, 영역 ~600 × 300 µm.  신호를 두께 방향 **같은 길이 5 구간**으로 나눠 구간별 F 평균.  배경: 전체 영역 스펙트럼에서 배경 총량의 1/5 을 각 구간에서 뺐다 (구간별 배경 보정이 소프트웨어에서 안 됨).
- 그림 5a: 100 °C 전극의 C (÷45) · F · Al (÷165) 원신호 — Al · C 신호가 전극의 위 · 아래 끝을 표시.  경계 밖 F 신호는 Al 간섭.
- 그림 5b 해석 (원문): RT 는 거의 균일하되 바닥 쪽이 약간 높음 (*"possibly … a small degree of binder sedimentation"*) · 50 °C 부터 윗면 이동 + 바닥 고갈 · 75 °C 는 *"resembles a linearly increasing binder distribution toward the separator-side"* · 125 °C 가 가장 강함.  125 °C 바닥 신호가 0 아래인 것은 배경 보정 오차 · 125 °C 는 집전체 접착이 매우 나빠 **자립 전극**을 만들 수 있었다 (A3464).
- 판독 크기 (파생): 맨 위 ÷ 맨 아래 구간 RT 0.74 · 50 °C 1.55 · 75 °C 2.5 · 100 °C 8.2 · 125 °C 정의 불가 (바닥 음수).  125 °C 맨 위 구간 ≈ 3.5 배 = 오른축 ≈ 17.6 % (원문 단위 표기 "%" — 평균 5 % = 95 : 5 wt 조성).

### 4-6. 차단 EIS · 겉보기 τ (그림 6, A3464–A3465)
- 셀: T-cell 대칭 (두 전극, OCV, 25 °C), ø 10.95 mm, 비삽입 전해질 100 µL (EC:EMC 3:7 wt + ~10 mM TBAClO₄; 전도도계 SI-Analytics LF 1100 T+ 로 **0.258 mS/cm**), 20 mV, 10 mHz–200 kHz (그림 6 캡션), 시료당 4 회.  ⚠ 대칭셀 분리막 종류는 이 논문에 없다 (*"as described previously, Ref. 18"*).
- 원문 해석: 겉보기 R_ion 최저 = RT (가장 균일) → 50 · 75 °C ~1.4 배 → 100 · 125 °C ~1.7 배 *"despite the rather small volume fraction of binder"*; *"even small amounts of binder can substantially influence the apparent ionic resistance"* (A3464–A3465).  위상 극소는 건조 온도와 함께 깊어진다 (그림 6b).  100 · 125 °C 는 τ 가 비슷하지만 125 °C 의 극소가 더 낮다 = 더 강한 구배 (그림 5b 와 정합) (A3465).
- **역조립** (A3465): 125 °C 자립 전극을 원래 분리막 쪽이 집전체를 보게 다시 조립 → 바인더 프로파일이 그림 5b 짙은 녹색을 x = 0.5 에서 뒤집은 꼴 → 겉보기 R_ion 이 RT 보다 낮고 위상에 **~47°** 국소 극소 (45° 위) — *"perfectly consistent with the EIS model … linear R_ion gradient"*.  겉보기 τ ~2.7.
- **그림 6d 판독 (벡터 좌표)**: §3 표.  가로축 판독 건조 시간 2.1 · 6.8 · 17.6 · 93 · 481 min (원문 ~2 · ~7 · ~18 · ~90 min · 8 h 와 정합).
- **카드 검산 — τ 척도 (파생)**: 그림 6a (HFR 보정 Nyquist, Ω) 곡선을 벡터 좌표로 꺼내 저주파 가지를 직선 외삽하면 절편 RT 421–471 · 50 °C 499–618 · 75 °C 510–606 · 100 °C 668–744 · 125 °C 740–787 · 역조립 303–327 Ω (맞춤 창 −Im 600–1000 / 700–1100 / 800–1300 Ω).  τ = 3·절편·A·κ·ε/(2t) (A 0.94 cm², κ 0.258 mS/cm, ε 0.55, t 245–260 µm) → **RT 3.2–3.9 · 50 °C 3.8–5.1 · 75 °C 3.9–5.0 · 100 °C 5.1–6.1 · 125 °C 5.7–6.4 · 역조립 2.3–2.7** — 그림 6d 평균을 감싼다.  √ 관례였다면 ≈ 1.5–2.5 → **이 논문 τ = tau2 척도 확인**.
  - 같은 계산이 보여 주는 것: 저주파 가지가 기울어 있어 (CPE 형, dRe/d(−Im) 0.08–0.26) 외삽 절편이 **맞춤 창에 ±10 % 안팎으로 민감**하다.  원문은 창을 적지 않는다.

### 4-7. 율속 시험 (그림 7, A3460–A3461 · A3465–A3466)
- 3 전극 Swagelok T-cell + Li 금속 기준전극 (Ref. 19 Fig 1a) · 흑연 작동전극 (~2.4 mAh/cm²) · Li 상대전극 (0.45 mm · ø 11 mm, Rockwood) · 유리섬유 분리막 2 장 (ø 11 mm, VWR, 250 µm 미압축, 다공도 90 %) · 부품 120 °C 진공 8 h · LP57 (1 M LiPF₆ EC:EMC 3:7 wt) 주 80 µL + 기준전극 칸 50 µL · Maccor · 25 °C · 0.01–1.5 V vs Li⁺/Li (기준전극 대비 제어 · 측정).
- 절차: OCV 3 h → 형성 없이 CC 리튬화 C/10 × 4 → C/5 · C/2 · 1C · 1.5C · 2C · 2.5C · 3C · 5C · 10C 각 5 사이클.  탈리튬화 = 같은 C 율 CCCV, 단 0.5C 를 넘지 않음.  전극 종류당 셀 3 개 평균 ± SD.
- 결과 (원문): 두 전극의 겉보기 τ 가 비슷 (4.4–4.6) 하지만 125 °C 의 위상 극소가 훨씬 깊어 *"the binder is significantly more inhomogeneously distributed"*; 125 °C 의 충전 율속이 열등 (Jaiser 등과 같은 경향).  카본블랙 이동 가설은 *"clearly can be ruled out"* (이 전극엔 카본블랙이 없다).  저자 가설: *"a high ionic resistance in the electrolyte phase near the anode/separator interface"* · *"a partially pore-blocking binder layer at/near the anode/separator interface"* (A3465–A3466).
- 판독 크기 (파생): 125 °C / 75 °C 충전 용량 비 C/5 0.83 · C/2 0.72 · 1C 0.58 · 1.5C 0.44 · 2C 0.37.

### 4-8. 측정 조건 일람

| 항목 | 모의 (그림 4) | 차단 EIS (그림 6) | 얇은 전극 EIS (그림 7a) | 율속 (그림 7b) |
|---|---|---|---|---|
| 두께 | 260 µm | ~245 µm (±6 %) · τ 계산엔 245–260 µm | ~74 µm (±2 %) | ~74 µm |
| 다공도 | 55 % 균일 | ~55 % (τ 계산 ε = 0.55) | ~55 % | ~55 % |
| 전해질 | κ 0.258 mS/cm | ~10 mM TBAClO₄ EC:EMC 3:7 · 0.258 mS/cm | 같음 | LP57 |
| 진폭 · 주파수 | 20 mV · 0.01 Hz–10 kHz | 20 mV · 10 mHz–200 kHz | (원문 그림 7 캡션에 진폭 없음 [미확인]) | — |
| 반복 | — | 4 회 | τ ± (그림 인쇄) | 셀 3 개 |
| 셀 | 2D 대칭 (분리막 50 µm, τ = 1) | T-cell 대칭, 0.94 cm² | T-cell 대칭 | Swagelok 3 전극 |

### 4-9. 시뮬레이션 · 입자 처리 ★
- **DEM · MPM · 미세구조 FEM · RNM 없음.**  모의는 COMSOL 전지 · 연료전지 모듈 (Newman 다공전극 모형, Refs 14 · 15) 을 **패러데이 반응 끄고** 이중층만 sink 로 둔 2D (사실상 1D) 연속체 = 균질화된 RC 전송선.  R_ion 프로파일은 국소 τ 를 바꿔 준다 (다공도 · 비표면적 고정).
- **입자 처리 ★** — 모형 안에 입자가 없다 (구형 입자는 a_dl 계산에만: r_p 10 µm).  실험 전극은 실제 흑연 판상 입자 · PVDF.  **바인더는 모형에서 상으로 존재하지 않고** "R_ion 프로파일" 로만 들어간다 — 바인더 → R_ion 의 정량 연결은 원문이 *"not yet possible"* 이라 적는다 (A3466).
- 바인더의 면내 분포 (입자를 덮는 층인지, 기공을 가로지르는 거미줄형인지) 는 *"Entirely unclear"* (A3466).

### 4-10. 기법 미니 용어집

| 용어 | 뜻 (이 논문에서) |
|---|---|
| **RC-TLM** | 저항 (기공 이온 저항 요소) + 용량 (이중층) 사다리 — 전자 레일 저항 0.  그림 2a 균질 · 2b 구배 (R₁ > R₂ > … 분리막 쪽이 큼) |
| **차단 전해질** (blocking) | 흑연에 삽입되지 않는 이온 (TBAClO₄) → 전하이동 없음, 이중층 충전만 |
| **반사 경계** (reflective) | 집전체에서 이온 전류 0 — 모든 이온 전류가 분리막 계면으로 들어와 두께 안에서 소모 (전지와 같은 배치) |
| **투과 경계** (transmissive) | 전극을 관통해 흐르는 배치 — 저항이 두께 비율로만 가중 → 방향 무관 (Refs 20–22) |
| **겉보기 R_ion · 겉보기 τ** | 균질 TLM 해석 (저주파 실축 외삽) 을 구배 전극에 적용해 얻은 값 |
| **HFR 보정** | 고주파 실축 절편 (분리막 전해질 · 셀 접촉 옴 성분) 을 빼고 그린 Nyquist · 위상 |
| **위상각 극소** | HFR 보정 Bode 위상의 저주파 극소 (용량성 상승 직전) — 구배 지표 |
| **역조립** (reversed) | 자립 전극을 위아래 뒤집어 조립 → 바인더 프로파일 반전 |
| **ng · lb · lt · sb · st** | no gradient · linear bottom · linear top · step bottom · step top (bottom = 집전체 쪽 · top = 분리막 쪽) |
| **eSCM / τ_e** | Nguyen 2020 의 이름 (이 논문에는 없음) — 차단 대칭셀 EIS 로 정한 electrode tortuosity factor |

---

## 5. Figure set ★ (크롭 권고 = ★)

| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| 1 (A3461) | 수지 함침 · 연마한 전극 단면 광학 사진 (Al 스페이서 사이, 1000 µm 축척) | EDS 시편 형상 — 참고만 |
| ★ 2 (A3461) | RC-TLM 회로: (a) 균질 (같은 R) (b) 구배 (분리막 쪽 R₁ 이 가장 큼) · 용량 동일 | 반사형 TLM 의 그림 정의 — 우리 z 단면 저항 → TLM 사다리 대응 (§8-5) |
| ★ 3 (A3462) | 다섯 R_ion 프로파일 (ng · lb · lt · sb · st) — 총저항 같음 | ★ **같은 투과형 저항 · 다른 방향** 의 정의 그림 |
| ★★ 4 (A3462) | 모의 (a) R_ion/1.5 정규화 Nyquist (b) 위상 (Bode) | ★★ 방향 가중의 크기 (±25 · −46/+66 %) 와 위상 지표.  ⚠ st 극소 그림 ≈ 33.6° ↔ 본문 ~39.1° (§10) |
| ★ 5 (A3463) | (a) 100 °C 전극 EDS 원신호 (C · F · Al) (b) 건조 온도별 5 구간 F 프로파일 (1.0 = 5 % 바인더) | 건조 속도 → 바인더 z 구배의 정량 — A7 `--cb-grad` 류 설계 프로파일의 실측 꼴 |
| ★★ 6 (A3464) | (a) HFR 보정 Nyquist (75 °C 에 37 · 3 · 0.38 Hz 표지) (b) 위상 (c) 75 °C 위상의 HFR ±2 · ±4 Ω 감도 (d) 겉보기 τ · 위상 극소 vs 건조 시간 (125 °C 역조립 포함) | ★★ 실험 핵심 — 같은 125 °C 전극의 정 5.73 / 역 2.70 (판독) · HFR 오차가 고주파 위상을 망치는 실례 |
| ★ 7 (A3466) | 얇은 전극 (~74 µm) (a) 위상 + τ (75 °C 4.6 ± 0.03 · 125 °C 4.4 ± 0.3) (b) 충전 율속 vs C 율 | ★ **같은 겉보기 τ · 다른 성능** — 단일 τ 로 구배 전극을 매개변수화할 수 없다는 실측 |

## 6. Post-processing ★
- **무엇**: HFR 보정 · 저주파 가지 실축 외삽 (겉보기 R_ion) → Ref. 18 식으로 τ · 위상각 극소 (저주파 · HFR 오차에 강건한 구간) · EDS 5 구간 평균 + 공통 배경 1/5 차감 · 정규화 (평균 = 1.0 = 5 % 바인더) · HFR ±1 · ±2 % 감도 시험 · 정/역 조립 대조 · 3 셀 평균 율속.
- **도구**: COMSOL Multiphysics (전지 · 연료전지 모듈) · JEOL JCM-6000 EDS · Maccor.  적합 소프트웨어 n/a (원문에 없음).
- **수치화 방식**: 그림 6d 하나에 겉보기 τ (왼축) 와 위상 극소 (오른축) 를 건조 시간 (로그) 에 함께 — "정량은 τ, 방향 · 구배 세기는 위상 극소" 의 이원 보고.  얇은 전극은 그림 안에 τ ± 인쇄.
- **검증 설계**: 모의 → EDS → EIS → 역조립 (방향 반전 대조군) → 성능.  방향 무관 기준값 (투과형 측정) 은 없다.

---

## 7. 우리 DEM+MPM 대비  →  `our_dem_baseline.md` (⛔ 기준값 자리표시 상태 — 비교는 정의 · 코드 단위로)

| 항목 | 이 논문 | 우리 | 같음 / 다름 · 이유 |
|---|---|---|---|
| 전도상 | 액체 전해질 (기공 연속체) | SE 입자 접촉망 (접촉마다 Holm 1/(2σa)) · STEP3 복셀 FV | **다름** — 협착 항은 우리만 있다 |
| τ 정의 | τ = R_Ion·A·κ·ε/(2d) (Ref. 18, 미인쇄) | **tau2** = φ_SE·σ₀/σ_eff | **정의식 같음** |
| 경계조건 | 교류 · 차단 대칭셀 · **반사형** (집전체 이온 전류 0) | 직류 · 두 띠 Dirichlet **투과형** (접촉망 `network_conductivity.py:225–249` · STEP3 `step3_sigma.py:835–840`) | **다름** — 원문 A3463: 투과형은 그림 3 의 모든 프로파일에 같은 값 → **우리 tau2 는 z 방향을 원리적으로 못 본다** |
| 방향을 보는 우리 경로 | — | STEP4 반응분포 (`step4_dyn.py:1086–1088`: 아래 집전체 φ_e = V_app · 위 분리막 φ_i = 0) — 이온이 위에서만 들어오는 반사형 | STEP4 를 뒤집은 침대로 돌리면 이 논문의 비대칭을 우리 침대에서 잴 수 있다 (미실행 · 아이디어) |
| z 불균일의 근원 | 건조 속도 → 바인더 이동 (PVDF ~2.7 vol% 전극) | 판 · 벽 근처 충전 층 · A7 설계 구배 (`--poro-grad` porosity(z) 총량 고정 · `--cb-ratio/--cb-grad` K = 8 설계 프로파일) · PTFE centerline 스탬프 분포 (원장 CL-60) | 원인은 다르지만 **같은 측정 편향**이 걸린다 (τ_e 형 실험 앵커와 맞댈 때) |
| 차단상 (바인더) | 2.7 vol% 로 겉보기 R_ion ×1.7 (위치 효과) | DEM 접촉망엔 바인더 없음 · STEP3 PTFE 스탬프 (CL-49: σ_e −25 %) | **같은 방향의 감수성** — 소량 · 위치가 크기를 정한다.  ⚠ 액체 기공 막힘 ↔ ASSB SE–SE 접촉 차단은 다른 물리 |
| σ₀ | κ = 액체 벌크 0.258 mS/cm (센서, 25 °C) | σ₀ = 3.0 mS/cm = 펠릿값 (원장 CL-91) | **성격 다름** — 절대 tau2 를 맞대기 전에 기준 상태부터 (결정 4) |
| 전자 저항 전제 | 전자 ≪ 이온 (두 자릿수) · 탄소 첨가 양극에서 깨질 수 있다 (원문) | ASSB 복합양극은 R_el/R_ion 이 1 근처일 수 있다 (`landesfeind2018_…` §8-5 ② 의 Minnmann 산술 19.8–0.0021) | 이 논문의 방향 판독은 **두 상 · 전자 레일 무시** 전제 — 우리 양극 실험 앵커에 그대로 옮기지 않는다 |
| 입자 · 형상 | 판상 흑연 (모형엔 입자 없음) | 강체 구 | 해당 없음 — 이 논문 결론은 형상과 무관한 TLM 가중 |
| 판정 구도 | "같은 총저항 · 다른 방향 → 다른 겉보기 값" | frame[4] 각 모형을 실험에 따로 보정 | 우리 tau2 를 τ_e 형 실험값에 맞대려면 그 실험 전극의 z 균질도부터 확인 |

- ⚠ **비판적 한정 (주장 전에 먼저 걸리는 것)**: ① 액체 LIB 흑연 → 전고체 LPSCl/NCM 수치 전이 불가 ② 실험은 바인더 → R_ion 연결을 정량하지 못했다 (원문) ③ 모의는 총저항 고정 · 균일 용량 · 전자 저항 0 의 이상화 ④ 실험엔 방향 무관 기준값 (투과형 τ) 이 없어 "편향" 크기는 모의에서만 정해진다 ⑤ 정 · 역 조립은 같은 건조 배치의 **다른 시편**일 가능성 (원문 미명시) · 두께 ±6 %.
- **frame[5]**: 수송 절반의 측정 · 해석 논문 — 압밀 · 형상 · 역학 없음.  우리 쪽 대응은 DEM 접촉망 tau2 · STEP3 복셀 tau2 (둘 다 투과형) · STEP4 (반사형 반응분포).  MPM 기계 쪽 대응 없음.
- **frame[4]**: 이 논문 수치로 우리 모형을 맞추지 않는다.  쓰는 것은 ① τ 척도 (tau2) · 측정 계열 (τ_e, 반사형) 판정 ② z 구배가 τ_e 형 측정을 움직이는 크기와 부호 규칙 ③ 위상 극소 · 정/역 조립이라는 실험 진단 설계.

---

## § τ 정의 대조 — 우리 규약 매핑

> **우리 규약** (메인 리포 CLAUDE.md ★★ τ 명명 규약, 1저자 비준 2026-10-03): f = σ_eff/σ₀ (`f_ion_<mode>`) · **tau2** = φ·σ₀/σ_eff = φ/f (`tau2_ion_<mode>`) · tau = √tau2 (`tau_ion_<mode>`, 웹앱 τ_Lap,eff) · τ_geo = 최단 경로 / 두께 (`tau_geo_SE_dij`, 수송 τ 아님) · τ_e = electrode tortuosity factor (우리에 없음).  'tortuosity factor' 는 tau2 에만 쓴다.
> **우리 tau2 의 정체**: 간선 재료 σ₀ 3.0 mS/cm (펠릿값) 위에 SE–SE Holm 협착을 직렬로 더한 **접촉망 모델 tau2** (hertz 면적 = LIGGGHTS c_cpl[22] 교차 원판 · 반공간 Maxwell R_c = 1/(2σa) — 1세대 협착식).  CF 가지 = "모델 내부 기준선", FULL/CF = "모델 내부 협착 비".  두 솔버 모두 **투과형** (두 띠 / 두 판 Dirichlet).

| 이 논문 기호 · 자리 (쪽) | 정의 · 정규화 (어느 부피 · 어느 단면 · 어느 경계) | 원문 이름 | σ₀ 기준 | 우리 다섯 양 중 | 환산 · 비고 |
|---|---|---|---|---|---|
| **τ** — A3465 · 그림 6d · 그림 7a | Ref. 18 대칭셀 식 τ = R_Ion·A·κ·ε/(2d) (미인쇄) · R_Ion = 두 전극 합 이온 저항 (저주파 외삽 × 3) · A = 전극 원판 0.94 cm² · d = 측정 두께 245–260 µm · ε = 0.55 (두께 + 면적 무게 — 전 기공) · **반사 경계** | "electrode resistance tortuosities (τ)" · **"apparent tortuosity"** | κ = 자가 조제 차단 전해질의 **벌크** 전도도 0.258 mS/cm (센서, 25 °C) — 미세구조 없음 | **tau2 (정의식)** · 측정 = **τ_e 계열 (반사형 · 겉보기)** | f = ε/τ · N_M = τ/ε · tau = √τ (RT 1.84 · 125 °C 2.39 · 역조립 1.64, 파생).  z 구배가 있으면 τ_e 형 겉보기 값 ≠ 투과형 tau2 (§8-4) |
| **τ = 5** (모의 입력) — A3460 | COMSOL 전지 모듈의 tortuosity 입력 (보정식 미인쇄) · 국소 R_ion ∝ τ/ε 로 프로파일을 만든다 | "tortuosity" | κ 0.258 mS/cm | **tau2 로 읽힌다 (판독)** — 근거: 그 값을 Ref. 18 의 흑연 통상값으로 인용 · "R_ion ~1 kΩ cm²" 진술이 1 승 산술 916 Ω cm² 와 맞음 (τ² 관례면 4.58 kΩ cm²) | ⚠ COMSOL 보정식이 인쇄되지 않았고 그림 4 주파수 축이 매개변수와 ≈ 16 배 어긋남 (§4-3) → 메모 v2 결정 5 의 "강하게 시사" 등급을 바꾸지 않는다 |
| **R_ion(x)** 프로파일 — 그림 3 | 국소 이온 저항 (평균 대비 0.5–2.5 배) · 총합 고정 | "ionic resistance in the electrolyte phase" | — | 국소 tau2/φ 프로파일의 상대값 | 우리 z 단면 저항 r_k 와 같은 양 (§8-5) |
| **R_ion/1.5 정규화** — A3461 | 대칭셀 저주파 절편 2·R_ion/3 | — | — | 없음 | ng → 1.0 |
| **겉보기 R_ion** (그림 4a · 6a) | 균질 TLM 그래프법을 구배 전극에 적용 | "apparent R_ion" | — | τ_e 형 겉보기 값 | 투과형 대비 F = ∫(r/r̄)·3(1 − u)² du (우리 유도) |
| 위상각 극소 (그림 4b · 6b · 6d · 7a) | HFR 보정 Bode 저주파 극소 | "phase angle minimum" | — | **대응 없음** | 정성 지표 (구배 존재 · 방향) |
| 분리막 τ = 1 (모의) | HFR 만 바꾸고 TLM 꼴은 안 바꿈 | "porosity and tortuosity was set to one" | — | — | — |
| τ_geo (기하 경로) | **이 논문에 없다** | — | — | 대응 없음 | — |
| Bruggeman | **언급 0 회** | — | — | — | 카드 산술: ε 0.55 → tau2_Brug = 1.348 → 겉보기 τ 의 Bruggeman 배수 RT 2.52 · 50 °C 3.36 · 75 °C 3.80 · 100 °C 4.34 · 125 °C 4.25 · 역조립 2.00 · 모의 기준 τ 5 = 3.71 (파생) |

**판정**
1. 이 논문 τ = Landesfeind 2016 τ (Ref. 18) = 우리 **tau2** 정의식 — 식은 미인쇄지만 그림 6a 외삽 되계산이 그림 6d 크기를 재현 (√ 관례 배제, §4-6).
2. 측정은 **차단 대칭셀 = 반사 경계 = τ_e 계열**이고, 저자 스스로 구배가 있으면 **"apparent"** 라 부른다.  우리 tau2 는 **투과형** — 원문 A3463 이 투과형은 방향 무관이라고 적는다 → 균질 전극에서만 두 값이 같다.
3. σ₀ = 액체 벌크 κ (미세구조 · 계면 없음) — 우리 3.0 (펠릿) 과 성격이 달라 tau2 절대값을 맞대기 전에 기준 상태부터 (결정 4).
4. ⛔ 이 논문의 "~1.7 배" 를 인용할 때는 **척도와 경계를 붙인다** — tau2 척도 · 반사형 겉보기 값 (√ 척도로는 1.30 배 · 정/역 2.12 배는 √ 로 1.46 배, 파생).

---

## 8. ★ 구배 전극의 방향 의존 τ — graded-z (판단 메모 v2 §7 ② "z 균질" · §8-2) — 이 묶음이 닫는 항목 + 적용 인사이트

### 8-1. 불균일 이온 저항 TLM 의 식
- **원문: 식 없음.**  수치 모의 (COMSOL Newman 모형, 패러데이 반응 끔, 전자 저항 무시 조건 σ_s 10 S/cm) 와 회로 그림 (그림 2) 만 있다.  해석적 처리는 *"While inhomogeneities of the ionic resistance across the thickness of a porous electrode have been analyzed analytically in the past using a transmission line model"* (A3459, Refs 11–13 = Paasch & Nguyen 1997 · Nguyen & Paasch 1999 · Keiser 1976) 로 넘긴다 — **세 원문 미열람 · 카드 없음**.
- **카드 유도 (우리 유도)**: 균일 용량 · 전자 레일 0 · 반사 경계에서 저주파 겉보기 저항 **R_app = ∫₀ᴸ r(x)(1 − x/L)² dx** (x = 분리막에서 깊이) → 투과형 저항 ∫ r dx 와의 비 **F = ∫₀¹ (r/r̄)·3(1 − u)² du**.  용량이 고르지 않으면 (1 − x/L) → (1 − C(x)/C_tot) (`siroma2015_…` §3-5).  원문 네 수치 (−25 · +25 · −46 · +66 %) 와 ng 위상 43.4° 를 재현한다 (§4-4).
- 이 식은 **저주파 실축 외삽 (겉보기 R_ion)** 에만 해당한다.  위상 곡선 전체는 RC 사다리 수치해 (§4-4 재계산) 가 필요하다.

### 8-2. 바인더 구배 검출 절차 (원문 그대로의 순서)
1. **차단 대칭셀 EIS** — 비삽입 염 (~10 mM TBAClO₄, EC:EMC 3:7, κ 0.258 mS/cm), T-cell, OCV, 25 °C, 20 mV, 10 mHz–200 kHz (A3460 · 그림 6 캡션).  현장 3 전극 배치 (Refs 25 · 26) 로도 가능 (A3466).
2. **HFR 보정** 후 Nyquist · 위상 그림.
3. **저주파 위상 극소**를 읽는다 — 균질 기준 (모의 ~43.4°, 실험 RT 43.1° 판독) 보다 **깊으면 분리막 쪽 고저항** (바인더 윗면 집중), **45° 위의 국소 극소 (~47°)** 면 집전체 쪽 고저항.  극소보다 높은 주파수 (> ~1–2 Hz) 의 위상은 HFR ±1–2 % 오차로 *"no reliable information"* (A3464–A3465).
4. 저주파 외삽으로 **겉보기 R_ion → 겉보기 τ** (Ref. 18).
5. (확인) **EDS 단면 5 구간** 바인더 프로파일 · 자립 전극이면 **역조립**으로 방향 대조.
- 원문 적용 범위 (A3466): *"most useful when comparing electrodes of the same composition and loading, but with different drying/aging history"* — 위상 극소는 *"an extremely important criterion … and should not be neglected"*.  정량 (구배 프로파일 복원) 은 하지 않는다.

### 8-3. 구배가 τ (MacMullin) 에 주는 영향의 크기

| 출처 | 대상 | 겉보기 τ (tau2 척도) | N_M = τ/ε (ε 0.55, 파생) | 기준 대비 | 표지 |
|---|---|---|---|---|---|
| 모의 (그림 4) | ng / lb / lt / sb / st (기준 τ 5) | 5 / 3.75 / 6.25 / 2.66 / 8.28 (파생 = 5 × 원문 비) | 9.1 / 6.8 / 11.4 / 4.8 / 15.1 | −25 · +25 · −46 · +66 % | 비 = stated · τ 환산 = 파생 |
| 실험 (그림 6d) | RT · 50 · 75 · 100 · 125 °C | 3.40 · 4.53 · 5.13 · 5.85 · 5.73 | 6.2 · 8.2 · 9.3 · 10.6 · 10.4 | 1 · 1.33 · 1.51 · 1.72 · 1.69 | 판독 (원문 "~1.4" · "~1.7") |
| 실험 (그림 6d) | 125 °C 역조립 | 2.70 | 4.9 | 0.79 (RT 대비) · 0.47 (같은 125 °C 정 대비) | 판독 · 원문 "~2.7" |
| 실험 (그림 7a) | 얇은 75 / 125 °C | 4.6 ± 0.03 / 4.4 ± 0.3 | 8.4 / 8.0 | ≈ 같음 — 성능은 다름 | stated |

- 정/역 비교 (파생): 실험 125 °C **2.12 배** ↔ 모의 선형 쌍 **1.67 배** · 1/4 계단 쌍 **3.12 배** — 그림 5b 의 윗면 집중형 프로파일 (맨 위 구간 3.5 배) 과 정합하는 중간값.
- ⚠ 실험의 RT → 125 °C 증가 (1.69 배) 는 **방향 가중 + 적분 저항 변화**가 섞인 값이다 — 모의처럼 총저항이 고정됐다는 보장이 없다.

### 8-4. 균질 TLM 으로 맞추면 생기는 편향 (원문 수치)

**구배 크기 ↔ 균질 TLM 편향 (같은 투과형 총저항 기준)**

| 구배 (최대 : 최소 국소 저항 · 모양) | 고저항이 분리막 쪽 | 고저항이 집전체 쪽 | 표지 · 출처 |
|---|---|---|---|
| 선형 1.5 : 0.5 (3 : 1) | **+25 %** (lt) | **−25 %** (lb) | stated · A3462 |
| 반 두께 2 층 1.5 : 0.5 (3 : 1) | +37.5 % | −37.5 % | `siroma2015_…` 카드 계산 · 이 카드 가중식으로 재현 (파생) |
| 1/4 두께 계단 2.5 : 0.5 (5 : 1) | **+66 %** (st) | **−46 %** (sb) | stated · A3463 |
| 실험 125 °C (EDS 맨 위 구간 ≈ 3.5 배 · 바닥 ≈ 0, 판독) | 겉보기 τ 5.73 | 겉보기 τ 2.70 (역조립) | 판독 · 투과형 값 미측정 → 괄호 3.85–4.22 기준 +36 … +49 % / −30 … −36 % (파생, 아래) |

- **원문 수치 = 모의뿐**: 같은 투과형 저항에서 균질 TLM 해석값이 **−46 % … +66 %** (네 프로파일) 벗어난다 (A3462–A3463).  원문 결론 문장: *"the tortuosities extracted from impedance analysis are apparent tortuosties which obviously cannot be directly applied to a macro-homogeneous battery model"* (A3466) · *"Any calculated tortuosity is a mere apparent tortuosity and is, in the case of strong binder gradients, not representative for the entire electrode. Electrodes of similar apparent tortuosity but different degrees of binder gradients show significant differences in performance."* (Conclusions, A3466).
- **실험에는 방향 무관 기준값이 없다** → 편향을 직접 잴 수 없다.  카드 괄호 (파생, §4-4): 정 · 역 겉보기 평균 = 선형 구배면 투과형 값.  125 °C 쌍 (5.73 · 2.70) → 평균 **4.22** (선형 가정) · **3.85** (1/4 계단 가정) · 일반 범위 **[2.81, 5.62]**.  그러면 정방향 겉보기 5.73 의 편향은 **+36 % (선형) · +49 % (계단)**, 역방향 2.70 은 −36 % · −30 % (파생 · 정/역이 같은 시편이라는 가정 · 두께 ±6 % 무시).
- 원문이 든 **함의** (A3466): 영상 (X선 단층촬영) τ 와 EIS τ 의 불일치 원인 중 하나일 수 있다 (Ref. 17 의 미해상 바인더와 함께) · 장기 사이클 "rollover" (Burns, Ref. 24 — 분리막 쪽 기공 막힘) 는 st 프로파일과 닮았고 현장 차단 EIS 의 위상 그림으로 검출 가능.

### 8-5. 결정 13 에 대한 답 — τ_e 는 z 균질도를 요구한다 (우리 z 단면 SE 컨덕턴스 진단 · A7 graded-z 설계 프로파일)
- **Q. 메모 v2 §7 ② "τ_e = T 에는 dead-end 가 없을 뿐 아니라 z 방향 균질 (TLM 균질화) 도 필요" 가 원문으로 서나?** → **선다 + 크기가 붙는다.**  dead-end · 접촉 저항 · 전자 레일이 전혀 없는 이상 RC-TLM 에서도 z 구배만으로 τ_e 형 (반사) 값이 투과형 값에서 **−46 … +66 %** (모의) 벗어나고, **부호는 고저항층이 분리막 쪽인지 집전체 쪽인지가 정한다**.  실험에서는 같은 전극이 방향만 바꿔 **2.12 배** (판독) 다르게 잰다.  ⇒ "부호 불정" 한정어 **유지**, 결정 13 권고 **변경 없음**.
- **Q. 우리 z 단면 SE 컨덕턴스 진단으로 무엇을 계산하나? (제안 · 미구현 · 우리 유도)**
  - FULL 해 (투과형) 의 전위장은 이미 나온다 (메모 v2 §7 "추가 솔브 없이": `solve_network(…, return_field=True)`).  침대를 z 로 K 층 나눠 층별 저항 r_k = (층 위 · 아래 경계 평균 전위차) / 총전류 → Σ r_k = 투과형 저항 (= tau2).
  - **반사 가중 인자 F_z = Σ_k r_k · 3⟨(1 − u)²⟩_k / Σ_k r_k** (u = 분리막 면에서 잰 깊이 / 두께, ⟨⟩_k = 층 평균).  분리막 면을 위로 둘 때와 아래로 둘 때 둘 다 낸다 (F_z,top · F_z,bottom).  |F_z − 1| 이 "z 구배만으로 τ_e ≠ tau2 가 되는 몫" 이다 (dead-end · sink 분포 몫은 따로).
  - ASSB 의 sink 는 AM–SE 접촉면이다 → 균일 가중 대신 (1 − C(u)/C_tot)², C(u) = 분리막 면부터 누적 AM–SE 접촉 면적 (siroma 일반식).  면적은 LHS-25 가 닫힌 뒤 · 그때까지 hertz 면적 (결정 3 의 순서).
  - 크기 감각 (이 논문, stated): 선형 3 : 1 → ±25 % · 1/4 두께 5 : 1 대비 계단 → −46 / +66 %.  판정선은 이 논문에 없다 — 쓰려면 런 전에 등록한다.
  - ⚠ 한계: 우리 침대 두께 ÷ 최대 AM 지름 중앙 4.7 (메모 v2 §7) → 층이 대표 부피가 아니어서 r_k 가 요동한다 · 층 평균 전위로 자르는 것은 1D 층상 가정이다.
- **Q. A7 graded-z 설계 프로파일에는?**
  - A7 (`--poro-grad` porosity(z) 총량 고정 게이트 · `--cb-ratio/--cb-grad` K = 8 설계 프로파일 — 메인 리포 `docs/backlog_solved_vs_todo.md` A7 행) 은 **총량 고정에서 방향을 바꾸는 설계** 다.  이 논문은 바로 그 상황 (총저항 고정 · 방향만 다름) 에서 τ_e 형 측정과 성능이 둘 다 방향을 따른다는 것을 보인다.
  - ⇒ **투과형 tau2 (인계 열) 는 A7 의 방향 변형 (정 · 역) 을 구별하지 못한다** — 같은 값이 나온다 (원문 A3463 의 투과형 문장).  A7 변형의 순위는 F_z (반사 가중) 또는 STEP4 (분리막 쪽 이온 입구) 로 매긴다.  인계 열 사전에는 "z 균질 침대에서만 τ_e 근사로 읽는다" 한정어.
  - 설계 방향 (이 논문 · 액체 흑연): 고저항층 (바인더 · 조밀층) 을 **분리막 쪽에 두지 말 것** — 역조립이 RT 균일보다도 낮은 겉보기 τ (2.70 < 3.40) 를 냈다.  같은 방향을 `nguyen2020_…` (2 층 모의: 조밀층 집전체 쪽 τ_e 4.0 ↔ 분리막 쪽 11.9, τ 는 7.4 하나) 과 `yoo2026_…` (top porous · bottom dense 구배, `bak2024_…` 카드 기술) 가 가리키고, `bak2024_…` (NCM 양극 바인더 3 층) 는 균일을 최적으로 본다 (카드 기술 — 재료 · 목적이 다르다).

### 8-6. 앞 묶음 TLM 과 같은 계열인가

| 카드 | 그 카드의 TLM | 이 논문과의 관계 |
|---|---|---|
| `landesfeind2016_…` | 간이 TLM (R_El → 0, R_CT → ∞) · 1/3 규칙 (Eq 12) · 대칭셀 τ (Eq 13) | **같은 방법 그대로** (Ref. 18) — 이 논문은 r(x) 가 불균일할 때의 겉보기 값을 본다 |
| `landesfeind2018_…` | 일반 TLM (Eq 1, 두 레일) · R_El/R_Ion < 10⁻² 창 | 같은 계열 · 같은 전제 ("두 자릿수", A3460) · 같은 저자군 (Landesfeind 공저) |
| `siroma2015_…` | Z/E형 open–open (z_C = 0) = de Levie · TML-Y 층 직렬 · 일반식 ∫ r(1 − C/C_tot)² dx · 2 층 3:1 ±37.5 % | **같은 계열** — 이 논문은 그 비균질 경우의 **발표된 모의 수치 + 실험** 을 준다.  투과형 대응 = Siroma T형 (DC = ∫ r dx, 방향 맹) |
| `nguyen2020_…` | eSCM (voxel 모사 + TLM 적합) | 같은 τ_e 계열 · Fig 6 2 층 모사가 voxel 판 대응 (단 dead-end 33 % · 다공도 대비가 섞여 순수 R_ion 구배가 아니다) |
| `pouraghajan2018_…` | PI (eRDM · 투과형 Thorat) vs BE (eSCM · 반사형) — 상용 전극에서 불확도 안 일치 | 그 일치는 **z 균질 전극에서만** 기대되는 결과 — 구배 전극이면 BE 는 방향에 따라 갈릴 것 (이 논문 모의).  같은 전극의 PI ↔ BE 대조 실측은 이 논문에 없다 |
| `kaiser2018_…` | ASSB TLM τ (문턱 근처 TLM ≫ DC) | ASSB 에서의 τ_e ↔ 관통 갈림 사례 · 이 논문은 그 갈림의 **또 다른 원인 (z 구배)** 을 준다 |

### 8-7. 결정 16 묶음에 주는 인사이트 (결정 번호 · 권고 변경 여부)

| 결정 | 인사이트 | 권고 변경 |
|---|---|---|
| **13** (τ_e) | z 구배만으로 τ_e 형 값이 −46 … +66 % (모의) · 같은 전극 정/역 2.12 배 (실험 판독) — 부호는 방향이 정한다.  진단 제안: z 단면 저항 → 반사 가중 인자 F_z (정 · 역 둘 다) | **no** (보강 · 진단 추가) |
| **5** (COMSOL/EIS 표기) | "EIS τ" 에는 **경계 종류 (반사 / 투과) 와 어느 면이 분리막인지** 를 함께 적어야 한다 (Siroma 연결형 한정어와 같은 줄) · 모의 τ = 5 → R_ion 916 Ω cm² 산술은 COMSOL τ 칸 = tau2 와 정합하지만 인쇄 근거가 아니다 | **no** (한정어) |
| **9 · 3** (LHS-25 · 면적 모드) | ASSB 에서 반사 가중의 sink = AM–SE 접촉 면적 분포 → F_z 를 sink 가중으로 내려면 면적이 먼저 (hertz 먼저 · physics 는 LHS-25 뒤) | **no** (순서 지지) |
| **14** (전자 · 열) | 방향 판독의 전제 = 전자 저항 ≪ 이온 (두 자릿수) · 탄소 첨가 양극에서 깨질 수 있다 (원문 A3463) → 부록의 넷째 진단 (전자 레일) 과 같은 줄 | **no** |
| 메모 §3-5 (Bruggeman 배수) | 같은 재료 · 조성에서 방향만으로 2.00–4.25 배 (파생) — "액체 전극 ≈ 1.5–3×" 위로 넘는 값이 구배 전극에서 나온다 | — (보강) |

### 8-8. 적용 인사이트 (일반)
- ① ★ **투과형 tau2 는 방향 맹** — 우리 인계 열 (DEM 접촉망 · STEP3) 로는 A7 의 정 · 역 설계를 가를 수 없다.  가르려면 반사 가중 (F_z) 이나 STEP4.
- ② ★ **τ_e 형 실험 앵커를 쓸 때 먼저 그 전극의 z 균질도를 본다** — 건조 속도 · 바인더 이동 · 층상 설계 전극은 겉보기 값이다.  위상 극소가 균질 기준보다 깊으면 앵커로 쓰지 않거나 방향 한정어를 붙인다.
- ③ ★ **정/역 조립** — 자립 전극 (ASSB 건식 PTFE 전극도 자립) 이면 두 방향을 재 투과형 값을 괄호로 묶을 수 있다 (선형이면 평균이 정확, §4-4).
- ④ **소량 차단상의 위치가 크기를 정한다** — PVDF 2.7 vol% 로 겉보기 ×1.7.  우리 PTFE 스탬프 (CL-49 · CL-60) 와 같은 감수성 축 (액체 ↔ 고체 물리는 다름).
- ⑤ **고주파 위상은 HFR 1 % 오차로 망가진다** — 위상으로 판정할 때는 저주파 극소만.
- ⑥ **"~1.7 배" 류 인용엔 척도 · 경계** — tau2 척도 · 반사형 겉보기 (√ 로는 1.30 배).

## 9. 인용 가능 문장 (deck/paper용)
- "Morasch et al. (J. Electrochem. Soc. 165, A3459, 2018) showed with an RC transmission-line model of blocking-electrolyte impedance that, for the same thickness-integrated ionic resistance, a resistance profile peaking at the separator side raises the apparent ionic resistance by about 25 % (linear 1.5:0.5 profile) or 66 % (2.5-fold resistance in the separator-side quarter), whereas the mirrored profiles lower it by 25 % and 46 %; with a transmissive boundary condition all profiles would give the same apparent resistance."
- "In graphite electrodes whose PVDF binder migrated to the top surface during fast drying (binder about 2.7 vol% of the electrode), the impedance-derived apparent tortuosity rose from about 3.4 (room-temperature drying) to about 5.7–5.9 (100–125 °C), while the same 125 °C electrode re-assembled upside down gave about 2.7 (values read from their Fig. 6d)."
- "Two electrodes with nearly equal apparent tortuosity (4.4–4.6) differed strongly in charge rate capability, so a single impedance-derived tortuosity cannot parametrize an electrode with a through-thickness binder gradient; the low-frequency phase-angle minimum is the qualitative indicator."

## 10. 주의/한계 (over-claim 방지)
- ⚠ **액체 전해질 LIB 흑연** (PVDF · 미압축 · 카본블랙 없음).  LPSCl 전고체로 **수치 전이 불가** — 쓰는 것은 측정 계열 판정 · 방향 가중의 크기와 부호 규칙 · 진단 설계뿐 (§7).
- ⚠ **τ 식 미인쇄** — 정의는 Ref. 18 로 넘긴다.  척도 판정 (tau2) 은 카드의 외삽 되계산 (§4-6) 과 2016 카드 Eq 13 에 기댄다.
- ⚠ **바인더 → R_ion 정량 연결 없음** (원문 *"not yet possible to quantitatively correlate binder gradients with R_ion gradients"*, A3466) · 바인더 면내 분포 미상.
- ⚠ **실험엔 투과형 기준값이 없다** — 모의의 "총저항 고정" 을 실험이 만족한다는 근거가 없고, RT → 125 °C 증가 (1.69 배) 는 방향 가중과 적분 저항 변화가 섞여 있다.  정/역은 다른 시편일 수 있다 (원문 미명시) · 두께 ±6 % · n = 4.
- ⚠ **모의 이상화** — 균일 용량 · 전자 저항 0 · 패러데이 없음 · 두 상 (원문 스스로 탄소 첨가 양극에서 전제가 깨질 수 있다고 적음, A3463).
- ⚠ **판독값은 TREND 전용** — 그림 5b · 6d · 7 의 수치는 원문에 숫자로 없다 (그림 6d 는 벡터 좌표로 읽어 정밀하지만 판독 표지 유지 · 그림 7 은 래스터).
- ⚠ **원문 내부 불일치 · 오기** (원문 그대로 두고 표지만):
  - **st 위상 극소**: 본문 A3463 *"∼39.1°"* ↔ 그림 4b **≈ 33.6°** (판독) ↔ 카드 RC 사다리 재계산 **33.58°**.  나머지 네 위상값 (43.4 · 48.6 · 40.3 · 44.5) 은 재계산과 0.1° 안에서 맞는다 → 본문 39.1 은 오기로 보인다.  인용은 그림값 (≈ 33–34°, 판독) 으로 하고 표지.
  - **lb "intermediate maximum of ∼48.6°"** (A3462) — 그림 · 재계산에서는 극소 48.6° 와 극대 48.9° 가 붙어 있다 (작은 차).
  - A3461 *"namely to 2/3 × Re(Z) in the symmetric cell"* — R_ion/1.5 정규화와 맞는 관계는 **대칭셀 저주파 절편 = (2/3)·R_ion** 이다 (그림 4a ng = 1.0).  문구는 R_ion = (2/3)·Re(Z) 로 거꾸로 읽힌다.
  - A3465 *"(red line labelled lt in Fig. 6) … (blue line labelled lb in Fig. 6)"* — lt · lb 모의 곡선은 **그림 4** 에 있다.
  - A3464 *"(black symbols in Fig. 5a)"* (RT 균일 바인더) — RT 프로파일은 **그림 5b** 다 (5a 는 100 °C 원신호).
  - 그림 4 의 주파수 위치가 원문 매개변수 (a_dl · c_dl) 로 계산한 값보다 ≈ 16 배 낮다 (§4-3) — 원인 [미확인].
  - 참고문헌 6 *"H. Hagiwara, W. J. Suszynski, and L. F. Francis, 8 (2013)."* — 학술지명 · 권 빠짐 (원문 서지 불완전).
  - "EDS" (본문 대부분) 와 "EDX" (A3465) 혼용 · "liniear" · "tortuosties" · "publications" 오탈자.
- ⚠ **저주파 외삽 창 미기재** — 카드 계산상 절편이 창에 ±10 % 안팎 민감 (§4-6).
- **인용 카드 대조** (그 카드들은 고치지 않았다 — 메인 판단):
  1. `nguyen2020_electrode_tortuosity_factor` §6-bis 6 *"분리막 쪽 고다공도 구배 설계 지지 (Morasch ref 33)"* — 이 논문은 **다공도를 균일 (55 %) 로 고정**하고 (A3460) 바인더 / R_ion 분포만 바꿨다.  지지하는 것은 "분리막 쪽 저(이온)저항" 이지 다공도 구배 자체가 아니다.  Nguyen 원문 p7 문장은 이 작업 환경에서 미열람 → 그 표현이 Nguyen 의 것인지 카드 요약인지 [확인 필요].  같은 카드 §11 ref 33 행 *"구배 전극의 방향 의존 τ 실측"* 은 원문과 맞는다 — 단 방향 의존은 **반사형 (차단 EIS) 겉보기 값**의 성질이다 (A3463).
  2. `kim2025_impedance_decoupling_tlm_assb` (§5.5 · §8 Post-processing · §13 용어집) · `interfacial_impedance_formulation_assb_cathode` (머리 10 행) · `comparison_vs_ours_DEM.md` (1139 · 3368 행) 의 **"Morasch R_int/R_i 비" 는 이 논문이 아니다** — kim2025 원문 PDF 참고문헌 [48] = *"R. Morasch, J. Keilhofer, H.A. Gasteiger, B. Suthar, Methods—Understanding porous electrode impedance and the implications for the impedance analysis of Li-ion battery electrodes, J. Electrochem. Soc. 168 (2021) 080519"* (kim2025 PDF 목록 문자열 그대로 · 그 2021 원문은 미열람).  이 2018 논문은 패러데이 반응을 끈 차단 조건뿐이라 R_ct 비 분석이 **없다** (전 10 쪽).  choi2024 원문 PDF 에는 Morasch 인용이 0 건이다 (그 카드의 언급은 kim2025 경유).  ⇒ 그 세 자리를 이 카드에 잇지 말 것 · 2021 논문 카드는 정본 `papers/` 에 없다 (전수 · DOI grep).
- **메모 v2 정정 후보** (`docs/reviews/tau_conventions_judgment_v2_20261003.md`, 메인 리포):
  1. **§8-2 Morasch 행 "왜"** *"구배 전극의 방향 의존 τ — graded-z"* → **"구배 전극에서 차단 EIS (반사 경계) 겉보기 τ 의 방향 의존 — 투과형 τ 는 방향 무관 (A3463) · 모의 −46 … +66 % (같은 총저항, A3462–A3463) · 실험 정 5.73 / 역 2.70 (그림 6d 판독, A3464–A3465)"**.  지금 문구는 τ 자체가 방향 의존이라고 읽힌다.
  2. (보강) **§7 ② "z 방향 균질 (TLM 균질화) 도 필요"** — 크기와 부호 규칙 한 줄: "고저항층이 분리막 쪽이면 τ_e 형 값 ↑ · 집전체 쪽이면 ↓ — 선형 3:1 ±25 % · 1/4 계단 5:1 −46/+66 % (A3462–A3463)".
  3. (보강) **§1 τ_e 행** — Morasch "apparent tortuosity" (Ref. 18 법, 차단 대칭셀) 를 τ_e 계열에 추가 · **§0-2 결정 13 이유 칸** "τ_e = T 는 z 균질도 요구" 에 위 크기 병기.
  4. (보강) **§3-5 Bruggeman 배수 행** "액체 전극 ≈ 1.5–3×" — 구배 전극은 같은 재료에서 방향만으로 2.00–4.25× (이 카드 § τ 정의 대조, 파생).
  5. (보강 — 부록) 부록 §1 결정 13 ⓑ "R_ion = 3·R_eff 는 균일 r · c · z_C = 0 일 때만 정확 (2 층 3:1 ±37.5 %)" 에 **발표된 모의 수치** 병기: 선형 ±25 % · 계단 −46/+66 % (A3462–A3463).
- **형제 카드 정정 후보**: 위 인용 카드 대조 1 · 2.  `nguyen2020_…` §11 ref 33 행 "(litdb 에 이름만 2 곳 등장, 카드 없음)" → 이 카드로 해소 (링크 갱신은 메인).

## 11. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)

| 원문 ref | 목록 서지 (그대로) | 왜 볼 만한가 |
|---|---|---|
| 11 | G. Paasch and P. H. Nguyen, Electrochem. Appl., 1, 1 (1997). | 불균일 TLM 의 **해석해** — 이 논문이 인쇄하지 않은 식 (§8-1) 의 원전 |
| 12 | P. H. Nguyen and G. Paasch, J. Electroanal. Chem., 460, 63 (1999). | 같은 축 (비균질 다공 전극 임피던스) |
| 13 | H. Keiser, K. D. Beccu, and M. A. Gutjahr, Electrochim. Acta, 21, 539 (1976). | 기공 형상 · 비균질 TLM 고전 |
| 20 | S. J. Cooper, A. Bertei, D. P. Finegan, and N. P. Brandon, Electrochim. Acta, 251, 681 (2017). | **반사 ↔ 투과 경계**의 원 비교 — 이 논문 방향 가중 논거의 출처 (이 묶음 inbox 25 번 · 메모 v2 §8-2 의 nguyen ref 42 와 같은 서지) |
| 21 | I. V. Thorat, D. E. Stephenson, N. A. Zacharias, K. Zaghib, J. N. Harb, and D. R. Wheeler, J. Power Sources, 188, 592 (2009). | 투과형 측정 (eRDM 원조) — 방향 무관 쪽 |
| 22 | D. Kramer, S. A. Freunberger, R. Flückiger, I. A. Schneider, A. Wokaun, F. N. Büchi, and G. G. Scherer, J. Electroanal. Chem., 612, 63 (2008). | 투과형 확산 측정 (연료전지 GDL) |
| 10 | J. Landesfeind, A. Eldiven, and H. A. Gasteiger, J. Electrochem. Soc., 165, A1122 (2018). | 바인더 **종류**가 흑연 tortuosity · 율속을 바꾼다 — 바인더 감수성의 두 번째 축 |
| 17 | J. Landesfeind, M. Ebner, A. Eldiven, V. Wood, and H. A. Gasteiger, J. Electrochem. Soc., 165, A469 (2018). | 카드 `landesfeind2018_tortuosity_impedance_vs_tomography` (미해상 바인더 → 영상 τ 과소) |
| 18 | J. Landesfeind, J. Hattendorff, A. Ehrl, W. A. Wall, and H. A. Gasteiger, J. Electrochem. Soc., 163, A1373 (2016). | τ 정의 정본 — 카드 `landesfeind2016_tortuosity_eis_electrodes_separators` |
| 1 | S. Jaiser, M. Müller, M. Baunach, W. Bauer, P. Scharfer, and W. Schabel, J. Power Sources, 318, 210 (2016). | 건조 속도 → PVDF 윗면 이동 · 접착 · 율속 (이 논문 출발점) |
| 2 | M. Müller, L. Pfaffmann, S. Jaiser, M. Baunach, V. Trouillet, F. Scheiba, P. Scharfer, W. Schabel, and W. Bauer, J. Power Sources, 340, 1 (2017). | 건조 속도별 바인더 구배 EDS 정량 |
| 7 | S. Jaiser, J. Kumberg, J. Klaver, J. L. Urai, W. Schabel, J. Schmatz, and P. Scharfer, J. Power Sources, 345, 97 (2017). | 건조 중 동결 단면 — 구배 형성 시점 (용매 14 % 증발부터) |
| 24 | J. C. Burns, A. Kassam, N. N. Sinha, L. E. Downie, L. Solnickova, B. M. Way, and J. R. Dahn, J. Electrochem. Soc., 160, A1451 (2013). | "rollover" — 분리막 쪽 기공 막힘 (st 프로파일 유사) |
| 25 · 26 | J. Landesfeind, D. Pritzl, and H. A. Gasteiger, J. Electrochem. Soc., 164, A1773 (2017). · D. Pritzl, J. Landesfeind, S. Solchenbach, and H. A. Gasteiger, J. Electrochem. Soc., 165, A2145 (2018). | 현장 (3 전극) 차단 EIS — 사이클 중 구배 감시 |
| 23 | S. A. Orfanidi, P. J. Rheinländer, N. Schulte, and H. A. Gasteiger, Submitted (2018). | 연료전지 이오노머 패치 (면내 차단상 분포) — 출판 서지 [미확인] |
| 16 | M. Ender, A. Weber, and E. Ivers-Tiffée, Electrochem. commun., 34, 130 (2013). | 모의 σ_s 10 S/cm 의 근거로 인용 (A3460) |

## 🔗 이 논문과 함께 읽을 corpus 카드
- `landesfeind2016_tortuosity_eis_electrodes_separators` — Ref. 18 · τ 정의 · 1/3 규칙 · 비삽입 염 차단법의 정본.
- `landesfeind2018_tortuosity_impedance_vs_tomography` — Ref. 17 · 같은 저자군 · R_El/R_Ion 창 · 미해상 바인더.
- `siroma2015_transmission_line_model_porous_electrode_impedance` — TLM 연결형 · 비균질 일반식 · 2 층 3:1 ±37.5 % (이 논문의 해석적 짝).
- `nguyen2020_electrode_tortuosity_factor` — 이 논문 = ref 33 · eSCM/τ_e · Fig 6 2 층 방향 효과 (voxel 판).
- `pouraghajan2018_tortuosity_polarization_interrupt_vs_blocking_electrolyte` — 투과형 (PI) ↔ 반사형 (BE) 실측 대조 (균질 전극에서 일치).
- `kaiser2018_ion_transport_limitations_assb_sulfide_electrodes` — ASSB TLM ↔ 관통 갈림.
- `bak2024_binder_distribution_multilayer` (A7 의 #20 바인더 z 분포) · `yoo2026_porosity_gradient_dry_electrode` (A7 의 #286 다공도 구배) · `luan2025_graded_cathode_400whkg_pouch` (ASSB graded 복합양극 — Phase 5 · A7) · `bielefeld2020_effective_ionic_conductivity_binder` (ASSB 바인더 → 유효 이온전도도 모델).

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
