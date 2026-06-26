# 복합 양극 계면 임피던스 *정식화*(TLM 등가회로)로 고에너지·고출력 ASSB 설계규칙 도출 — Choi 외 (ACS AMI 2024)

> slug `interfacial_impedance_formulation_assb_cathode` · (first-author+year: **choi2024**) · DOI `10.1021/acsami.4c01322` · type `exp + equivalent-circuit modeling (TLM / de Levie)` · PDF `InterfacialImpedances_HighEnergyHighPower_ASSBCathode.pdf` · digested `2026-06-26` · status ✅
>
> ★ slug 은 메인 세션 검색용으로 `interfacial_impedance_formulation_assb_cathode` 유지.  논문 = **Choi, Ku, Kim, Gwon, Yoon, Yu, Kim — ACS Appl. Mater. Interfaces 16 (2024) 26066–26078** (Samsung Advanced Institute of Technology, SAIT).
>
> ## ★★★ 위치 — 이 논문은 우리 kim2025 임피던스-분해 앵커의 *방법론적 부모(parent)* ★★★
> 우리 INDEX 의 MUST-READ **kim2025**(Hanyang Lee 그룹, Electrochim. Acta 2025)가 *modified TLM* 으로 R_ion/R_ct/C_dl/Warburg 를 분해한 **자매 실험 논문**이라면, **이 Choi 2024(SAIT)** 는 그 TLM 회로 family 를 **NCM/NCA + LPSC 복합 양극용으로 *정식화*하고 검증한 출발점**이다.  핵심:
> - 이 논문의 **eq 1**(대칭셀 TLM 해석해)·**eq 7**(full-cell 양극 임피던스 z_cathode,i–e)은 **kim2025 의 e-block 해석해, Bazzoun 2026 의 eq 1 과 *동일한* de Levie/transmission-line 식** (계보: Siroma 2016 → Minnmann 2021 → Jung 2019(SAIT 자체) → 이 논문 → kim2025).
> - kim2025 가 *분해 가능성 조건*(R_int/R_i 비, Morasch)을 강조했다면, 이 논문은 거기에 더해 **(a) 압밀압력 → r_i,gb 의 정량 의존, (b) CAM 입경 → r_i,gb ↔ r_i/e 의 trade-off, (c) bimodal CAM 으로 그 trade-off 돌파** 라는 *설계규칙*을 추가한다.
> - ★ **우리에게 왜 중요한가 (3줄):** (1) **계면 임피던스를 r_i,bulk + r_i,gb + r_i/e(=R_ct) + r_e + Z_low(Warburg) 로 *해석적으로 분해*한 정식화** = 우리 Kirchhoff/Holm σ-솔버가 *구조적으로* 계산하는 ASR 의 *주파수영역 카운터파트*. (2) 그들 **r_i,gb(입계)·r_i,bulk(입내) 분리**가 우리 Cronau(r_SE) GB 인자를 정당화하고, 그들 **r_i/e(=R_ct)·Z_low(Warburg)** 는 우리 *미보유* frame[5] kinetics 칸(kim2025 와 동일 빈 칸)을 정확히 짚어 준다. (3) 그들 **"r_i,gb ↔ r_i/e trade-off → bimodal CAM 으로 돌파"** 설계규칙은 우리 predictor·Furnas-dip 작업과 교차검증할 *설계 가설*.

---

## §0. 이 논문의 위치 — TLM 앵커 4종 지도 + 우리 ASR 와의 관계 (이 절이 framing)

### 0.1 EIS-TLM 앵커 4종 (우리가 가진 임피던스-분해 실험/이론 근거의 전체 지도)
| 논문 | 그룹 | 소재 | TLM 이 *주는* 것 | 우리에게 |
|---|---|---|---|---|
| **Minnmann 2021 JES** | Janek (Giessen) | NCM-622 + LPSCl | σ_ion,eff / σ_el,eff / **τ²** (T-type TLM) | porosity 14 %·σ_ion 0.17·τ_ion 2.07 앵커 출처 |
| **Bazzoun 2026 JPS** | Mercedes/Stuttgart | NMC811 + LPSCl | R_ion → σ_eff,ion (Z-type TLM) + **DEM→RNM 솔버** | σ_eff,ion 0.137/0.101/0.065 절대 앵커 + 같은 Holm/Kirchhoff |
| **Kim 2025 (우리 랩)** | Lee (Hanyang) | NCM811 + LPSCl + 할라이드 | R_ion/**R_ct/C_dl/Warburg** 동시 분해 + **T-의존 E_a** | 가장 완전한 *kinetic* 분해 + SAME LAB |
| **★ Choi 2024 (이 논문)** | **SAIT (Samsung)** | **NCM/NCA + LPSC** | ★ **r_i,bulk+r_i,gb+r_i/e+r_e+Z_low 정식화 + 압력·입경·bimodal *설계규칙*** | ★ **계면 임피던스 정식화의 *부모*** + r_i,gb↔r_i/e trade-off 설계가설 |

> ★ Minnmann/Bazzoun 은 주로 *수송* σ 를 주고, kim2025 는 *kinetics*(R_ct/C_dl/확산/E_a)를 깊게 준다.  이 **Choi 2024 는 그 둘을 잇는 *정식화 + 설계규칙*** — 어떤 미세구조 인자(SE 분율·압력·입경·PSD 모달리티)가 어떤 임피던스 항을 키우는지를 회로로 분해하고, **"r_i,gb 와 r_i/e 가 입경으로 *반대 방향* 변해 trade-off → bimodal 로 돌파"** 라는 설계 결론을 낸다.  우리 솔버는 **z_i(이온수송)만** 계산 → r_i/e(=R_ct)·Z_low(Warburg)는 우리 밖(frame[5]).

### 0.2 이 논문의 회로 = Bazzoun·kim2025 와 *같은* TLM 해석해 (계보 확인)
- 이 논문 본문이 명시하는 회로 계보(refs): **de Levie 1963(ref 16) = TLM 원전**, **Siroma 2015/2016(ref 19,20) = 추가 r 또는 r/c 분기 도입**, **Minnmann 2021(ref 22)** 과 **"our group" Jung 2019(ref 23, SAIT 자체)** 의 변형.  이 논문은 그 회로들의 *물리적 의미*를 EIS+미세구조 분석으로 검증해 "어느 회로가 복합 양극을 가장 잘 표현하나"를 가린다 → **Fig 1d (z_i = r_i,bulk + r_i,gb∥c_i,gb) 채택** 이 결론.
- ★ **eq 1**(대칭셀 TLM, charge-transfer 없음) ≡ **kim2025 의 ion-block 해석해** ≡ **Bazzoun 의 eq 1** (cosh/sinh 형태, 동일).  **eq 7**(full-cell 양극 z_cathode,i–e, charge-transfer z_i/e 포함) ≡ **kim2025 의 e-block 해석해**.  ⇒ 세 논문이 *같은 식*을 쓴다 → 우리 σ-솔버는 이 식의 *DC·공간 저항망* 등가물.

### 0.3 우리 ASR 와의 직접 매핑 (이 digest 의 핵심)
| 이 논문 회로 항 | 물리 | 우리 (DEM Kirchhoff/Holm + Stage-E) | 매핑 |
|---|---|---|---|
| **r_i,bulk** (입내 이온저항) | SE 입자 내부 Li⁺ 전도 | σ_grain (Cronau 3.0) 의 입내 부분 | **우리 보유** |
| **r_i,gb** (SE/SE 입계 이온저항) | cold-press 입계 이온 병목 | Cronau(r_SE) **GB 인자**(σ_grain prefactor 럼핑) | ★ **우리 GB 인자 정당화** — 그들이 *분리* |
| **r_i** = r_i,bulk + r_i,gb (조합) → σ_eff,ion | 복합 이온저항 → 유효전도도 | **σ_ionic** (R=L/σ, Kirchhoff/Holm; ASR_ionic) | ★ **우리 σ_ionic 의 정확한 카운터파트** |
| **r_e** (전자저항) | CAM+CF 전자 전도 | **σ_electronic** (ASR_electronic) | **우리 보유** |
| **r_i/e (= z_i/e, = R_ct)** (SE/CAM 전하전달) | Li⁺+e⁻→격자 *반응* | **미보유** (constriction-only) | ★ **우리 밖** (frame[5], kim2025 와 같은 빈 칸) |
| **Z_low (Warburg, Z_low)** | 활물질·음극 *고상 Li 확산* | **미보유** (D_Li 모델 없음) | ★ **우리 밖** |
| **tau_eff²** (Bruggeman, eq 5) | 이온경로 tortuosity factor | **τ_Laplace,eff** (= σ_0·φ/σ_eff 정의 동일) | ★ **정의 동일** — 단 그들 tau_eff ⊃ constriction-유사 효과 |
| **eps_pore** | 복합 양극 공극분율 | DEM porosity (15.6 %) | 추세 비교(절대 직접 금지) |
> ⇒ ★ **우리 ASR 는 그들 r_i(=r_i,bulk+r_i,gb) → σ_eff,ion → ASR_ionic 와 1:1 대응** (z_i 레일).  그들이 추가로 분해하는 **r_i/e(R_ct)·Z_low(Warburg)는 우리가 *전혀* 안 갖는 계면반응·확산 kinetics** = frame[5] 빈 칸.  단, **우리 우위**: 우리 σ_ionic 은 r_i,gb 를 *실제 접촉 constriction*(Holm 1/(2σr_c))으로 *구조적으로* 풀어 입계 면적·배위수·coverage 까지 주는데, 그들 r_i,gb 는 *측정된 lumped 파라미터* → 미세구조가 *입력*이 아니라 *fitted 결과*로만 들어온다.

---

## 1. 한 줄 요약
ASSB 복합 양극의 **높은 계면 임피던스**를 EIS 로 *정량 분석*하기 위해, **TLM(de Levie/transmission-line) 기반 등가회로를 NCM/NCA + LPSC 복합 양극용으로 정식화**하고(이온 z_i / 전자 z_e 두 레일 + 계면 charge-transfer z_i/e crossrail), 대칭셀과 full-cell EIS 로 **두 핵심 계면저항 — SE/SE 입계저항 r_i,gb 와 SE/CAM 전하전달저항 r_i/e** 를 분리한다.  체계적 분석 결과 **CAM 입경이 작아지면(반응 표면적↑) r_i/e 는 낮아지지만 r_i,gb 는 *오히려* 높아진다**(작은 CAM → 더 다공 → 입계 성장)는 **예상 밖 trade-off** 를 발견하고, **bimodal CAM**(작은+큰 입자 혼합)으로 두 저항을 *동시에* 낮춰 trade-off 를 돌파 → 고에너지(>800 Wh/kg·>1100 Wh/L)·고출력(2C 에서 7× 용량) ASSB 양극 설계규칙을 제시한다.  → "**계면 임피던스를 회로로 정식화해 미세구조 설계로 연결하는 정량 가이드라인**".

---

## 2. 메타
| 항목 | 값 |
|---|---|
| 저자 | **Wonsung Choi\***, Jun Hwan Ku, Youngeal Kim, Hyeokjo Gwon, Gabin Yoon, Daeun Yu, Ju-Sik Kim |
| 소속 | **Samsung Advanced Institute of Technology (SAIT)**, Samsung Electronics, Suwon 16678, Korea |
| 저널/년 | **ACS Appl. Mater. Interfaces 16 (2024) 26066–26078** |
| DOI | **10.1021/acsami.4c01322** (Received 2024-01-23, accepted 2024-04-24, published 2024-05-13) |
| Keywords | all-solid-state battery · **interfacial impedance** · composite cathode · **EIS** · grain-boundary resistance · charge-transfer resistance |
| 소재 (SE) | **LPSC argyrodite Li₅.₇₅PS₄.₇₅Cl₁.₂₅** (Mitsui Mining & Smelting) — ⚠ **Cl 함량 1.25, *우리 LPSCl Li₆PS₅Cl* 과 조성 약간 다름** (Cl-rich argyrodite) |
| 소재 (CAM) | **NCM LiNi₀.₉₀Co₀.₀₅Mn₀.₀₅O₂** (JX Nippon Mining & Metals) + **NCA LiNi₀.₉₄Co₀.₀₄Al₀.₀₂O₂** (Samsung SDI); 모두 **Li₂ZrO₃ 코팅**(sol-gel) |
| 도전제 | **carbon fiber CF** (Teijin) |
| 복합 양극 조성 | 대칭셀: **SSE:NCM = 50:50 v/v** (SE vol frac ε_i = 0.49–1.0 스윕); full cell: blade-coat 양극 = **CAM 85 wt% : LPSC 14.25 : CF 0.25 : acrylate binder 0.5 wt%** (NMP slurry, PVDF 3 wt% binder for SSE film) |
| 셀 종류 | (a) **대칭셀** SUS\|복합양극\|SUS (이온 차단, electron–electron) → r_i,gb 정량; (b) **full-cell ASSB** In/SSE\|양극+CF\|SSE → r_i/e 정량; (c) **pouch high-energy cell** (105 µm NCA-b-12 양극, 6.3 mAh/cm² projected) |
| 압력 | **제조/압밀 300–500 MPa** (UP-C uniaxial / IP-C isostatic-cylindrical / IP-P isostatic-pellet, ~800 µm 펠릿); ★ **작동/측정 stack pressure = 4 MPa** (pouch test 중) |
| 측정 | EIS: **VMP-3 (BioLogic), 1 MHz–10 mHz, ±20 mV**; 온도 의존 (warm isostatic 500 MPa 85°C 포함); cycling: TOSCAT-3100, **1.9–3.6 V (full cell) / 2.5–4.25 V (pouch)**, 0.01–2C |
| 연구유형 | **실험**(EIS-TLM 피팅 + cell test) **+ analytical equivalent-circuit *정식화*** (TLM 해석해 eq 1–7, model simulation Fig S5) |

> ⚠ **소재 미세 차이 주의:** SE = **Li₅.₇₅PS₄.₇₅Cl₁.₂₅** (Cl-rich argyrodite, Mitsui) ≠ 우리 **Li₆PS₅Cl**.  같은 argyrodite 황화물 계열이라 *물리·추세*는 직접 비교 OK, 단 **σ 절대값·r_i,gb 절대값 전이 시 조성차 주의**.  CAM 도 **NCM90/NCA94**(우리 NCM811 보다 Ni-rich) — 추세는 같으나 절대값 직접 매칭 금지.

---

## 3. 핵심 물성 (수치) — 모든 값

> ★ 이 논문은 *압밀 porosity*(eps_pore 는 줌), *상대밀도*, *coordination*, *coverage* 를 명시 측정·보고하지 **않는다**(주로 EIS-TLM 임피던스 논문 + cell test).  정량 앵커는 **r_i,bulk / r_i,gb / r_i/e / r_e / Z_low / tau_eff² / eps_pore / σ_eff,ion·E_a(pristine SE) / 입경 / cell 성능**.

| 물성 | 값 | 조건 (ε_i, P) | stated/digitized | 비고 |
|---|---|---|---|---|
| **r_i,bulk (pristine SE)** | **178 Ω·cm** | 순 SE 펠릿, 300 MPa | stated | Fig 2c 입내 이온저항 |
| **r_i,gb (pristine SE)** | **631 Ω·cm** | 〃 | stated | Fig 2d 입계(HF >100 kHz 작은 반원) |
| **r_i (pristine SE)** | **809 Ω·cm** | 〃 | stated | = 178+631; ★ **순 SE 도 입계가 입내의 3.5×** |
| **E_a (pristine SE 이온)** | **0.33 eV** | 〃 | stated | Fig 2c inset Arrhenius |
| **r_i (composite, ε_i=1.0)** | **12 800 Ω·cm** | 복합셀 ε_i=1.0 | stated | ★ pristine SE r_i(809)의 **~16×** (NCM 이 SE 소결 방해) |
| **r_i (composite, ε_i=0.54)** | **18 400 Ω·cm** (=18.4 kΩ·cm) | 저-SE | stated | bulk 0.61 + gb 17.7 kΩ·cm → **r_i,gb 가 29× 지배** |
| **r_i,bulk (composite, ε_i=0.54 / 1.0)** | **610 / 170 Ω·cm** | | stated | bulk 은 SE 분율에 둔감 |
| **r_i,gb (composite, ε_i=0.54 / 1.0)** | **17 700 / 630 Ω·cm** | | stated | ★ **GB 가 SE 감소에 폭증** (28× over ε 1.0→0.54) |
| **α (Bruggeman, r_i,bulk)** | **0.52** | eq 5 fit | stated | ≈ 이상 Bruggeman 0.5 (구형 절연입자) |
| **α (Bruggeman, r_i,gb)** | **4.3** | eq 5 fit | stated | ★ 이상 대비 *훨씬 큼* → **GB 성장**이 저항↑ 주역(경로 신장 아님) |
| **tau_eff² (bulk / gb, ε_i=0.54)** | **1.9 / 22** | | stated | Fig 3d; GB tortuosity factor 22 (매우 큼) |
| **eps_pore (ε_i=1.0 / 0.26)** | **0.16 / 0.23** | 복합셀 | stated | ★ **SE↓ → 공극↑** (rigid NCM 이 SE 소결 방해) |
| **전자 percolation 임계** | **ε_i ≈ 0.77** | | stated | < 0.77 서 NCM 전자망 percolate (r_e<r_i, Fig 3a 급변) |
| **순-R 회로 임계** | **ε_i ≤ 0.49** | | stated | 반원 사라짐 (전자경로 완전 확립) |
| **c_i,gb (composite)** | **10⁻¹¹–10⁻⁸ F** | ε_i 0.54–1.0 | stated | 입계 이온전도 용량 (Table S1) |
| **r_i,gb (UP-C 300 / IP-P 500)** | **8 700 / 2 650 Ω·cm** | ε_i=0.58 | digitized/stated | ★ **압력·등방가압이 r_i,gb 급감** |
| **eps_pore (IP-P 500 MPa)** | **0.046** | ε_i=0.58 | stated | 등방가압(fluidic media)이 SE 매끄럽게 소결 |
| **r_e (모든 셀, 500 MPa)** | **< 15 000 Ω·cm** | ε_i=0.58 | stated | 압력↑ → r_e↓ |
| **tau_eff² (IP-P, 500 MPa 85°C)** | **1.46** | ε_i=0.58 | stated | ★ ≈ 이상 Bruggeman **1.41**(α=0.5) → **거의 완전 SE 치밀화** |
| **r_i/e 기울기 vs 1/A_CAM** | **0.082 Ω·cm⁵** | NCA full cell | stated | ★ **r_i/e ∝ 1/A_CAM** (CAM 표면적 반비례) = SE/CAM 전하전달 재료물성 |
| **Z_low (확산)** | **13.9 ± 2.6 Ω·cm²** | NCA full cell | stated | 음극+양극 Li 고상확산 (Warburg) |
| **Z_SE (separator)** | **32.6 ± 1.4 Ω·cm²** | | stated | SE 분리막 bulk+GB |
| **R_cathode (NCA-15/NCA-4/NCM-7/NCA-b-12)** | **20 / 24 / 25 / 14 Ω·cm²** | full cell, 500 MPa | stated | ★ **bimodal NCA-b-12 최저(14)** |
| **r_i,gb (NCA-b-12 bimodal)** | **3 240 Ω·cm** | | stated | 최저 입계저항 (작은 NCA-4 가 큰 NCA-15 공극 충전) |
| **eps_pore (NCA-b-12 bimodal)** | **0.11** | | stated | unimodal 보다 낮음 (densify) |
| **CAM 입경 (NCA-4/15, NCM-7, NCA-b-12)** | **4 / 15 / 7 / 12 µm** | | stated | NCA-b-12 = 4+15 혼합 평균 12 µm |
| **internal R (NCA-b-12)** | **57–58 Ω·cm²** | IV slope ≈ EIS | stated | R_SE+R_cathode+R_anode |
| **discharge cap (NCA-b-12 / NCM-7, 0.1C)** | **4.1 / 3.5 mAh/cm²** | full cell | stated | 5 mAh/cm² projected |
| **discharge cap (NCA-b-12 / NCM-7, 2C)** | **2.1 / 0.3 mAh/cm²** | | stated | ★ **bimodal 이 고율 7× 용량** |
| **pouch 에너지밀도** | **>800 Wh/kg · >1100 Wh/L** | 105 µm NCA-b-12 | stated | 5.3 mAh/cm²@0.1C (171 mAh/g) |
| **pouch cycle** | **85 % over 300 cyc, CE 99.9 %** | 0.33C | stated | Fig 7g |
| **작동 stack pressure** | **4 MPa** | pouch test 중 | stated | ★ 제조 500 ≠ 작동 4 MPa (압력 구분) |
| porosity 절대 / 상대밀도 | **n/a** (eps_pore 만; 압밀 porosity 별도 보고 X) | — | — | — |
| coverage / coordination Z | **n/a** | — | — | EIS 논문 |
| E_SE / σ_y / ν / Heckel | **n/a** (역학 미모델) | — | — | (압밀곡선·modulus 없음) |
| PSD (D10/D50/D90) | **n/a** (CAM 평균 입경만) | SE n/a / CAM 4-15 µm | — | SE 입경 미보고 |

> ★ **σ 환산 (참고):** pristine SE r_i = 809 Ω·cm → **σ_eff,ion ≈ 1/809 = 1.24 mS/cm** (300 MPa 펠릿, GB-incl).  → Bazzoun pellet **1.02**·Minnmann/kim2025 **1.6**·Cronau 단결정 3.0 사이의 또 하나의 LPSC bulk 앵커 (단 Cl₁.₂₅ Cl-rich → 절대 직접대조 금지, 스프레드로만).  composite ε_i=1.0 의 r_i=12 800 Ω·cm → σ ≈ 0.078 mS/cm = 복합셀 안 SE(NCM 이 소결 방해) → 우리 σ_ionic 복합값(0.04–0.18)과 같은 대역.

---

## 4. 임피던스 *정식화* ★ — 모든 회로·방정식 (이 절이 digest 핵심)

> ★ 이 논문의 "모델"은 DEM/MPM/FEM 미세구조가 아니라 **분포 임피던스 등가회로(TLM)의 *해석해* + EIS 피팅 + model simulation(Fig S5)** 이다.  우리 Kirchhoff/Holm σ-솔버와 **목적은 같고(전달·계면 분해) 형식이 다르다**(그들=주파수영역 임피던스 회로 해석해, 우리=공간 저항망 DC 풀이).

### 4.1 회로 토폴로지 (Fig 1) — 두 레일 + crossrail (TLM = de Levie)
복합 양극 = **혼합 전도체** — 이온은 SE 입자망(상단 레일 z_i), 전자는 CAM+CF 망(하단 레일 z_e)을 *따로* 흐르고, **계면(crossrail z_i/e)에서 전하전달로 결합**.  이를 **두께 방향으로 분포된 무한 RC 사다리망(TLM)** 으로 모델 (Fig 1a 하단).
- **상단 레일 z_i (이온 임피던스)** [Ω·cm] = SE 상.  ★ **z_i = r_i,bulk + (r_i,gb ∥ c_i,gb)** — 입내(bulk) + 입계(GB) 직렬, GB 는 R∥C 병렬 (Fig 1c=r_i,bulk+r_i,gb/c_i,gb; Fig 1d 채택).
- **하단 레일 z_e (전자 임피던스)** [Ω·cm] = CAM+CF 상.
- **crossrail z_i/e (계면 임피던스)** [Ω·cm³] = SE/CAM 전하전달 (full cell 에서만 살아남, eq 7).
- ★ **Fig 1b (LE 양극) vs 1c/1d (SE 복합 양극) 차이:** LE 양극은 z_i 가 *순수 r_i,bulk*(pore-ionic, GB 없음); SE 복합 양극은 z_i 에 **r_i,gb(입계) 가 추가** — 이게 "**왜 SE 복합 양극 이온전도가 LE 보다 *훨씬* 낮은가**"의 핵심 (입계저항, *tortuous path 아님*).

### 4.2 ★ 두 경계조건(BC)별 해석해 — 어느 BC 가 어느 과정을 고립시키나
이 논문의 *방법론적* 핵심 (kim2025 와 동형).

**(A) 대칭셀 [SUS\|복합양극\|SUS] (이온 차단, charge-transfer 없음)** — Fig 1c,d / Fig 2g,h:
- 양 끝 SUS 가 이온 차단 → crossrail 에서 **전하전달 사라지고**, z_i = r_i,bulk + r_i,gb∥c_i,gb 만 (z_e=r_e).
- 채택 회로 = **Fig 1d** (z_i = r_i,bulk + r_i,gb/c_i,gb; z_e = r_e) → Fig 2h 가 EIS 를 *일관되게* 피팅.
- ⇒ ★ **대칭셀 = r_i,gb(입계 이온저항)를 정량하는 셀.**  Fig 2g(z_i=r_i,bulk 만, GB 없음)는 *deviate* → GB 항이 필수임을 검증.

**(B) full-cell ASSB [In/SSE\|복합양극+CF\|SSE] (전하전달 발생)** — Fig 1e / Fig 5:
- LPSC 가 전자 차단 → 이온이 계면 건너 **전하전달 z_i/e 살아남** → crossrail 에 R_ct 분기.
- **양극 임피던스 (eq 7):**
  ```
  Z_cathode,i–e = (z_i·z_e)/(z_i+z_e)·t_cathode
                + [√(z_i/e)/(z_i+z_e)^(3/2)]·{(z_i²+z_e²)·cosh[t_cathode·√((z_i+z_e)/z_i/e)] + 2·z_i·z_e}
                  / sinh[t_cathode·√((z_i+z_e)/z_i/e)]
  ```
  (z_i, z_e [Ω·cm], z_i/e [Ω·cm³] 전하전달 임피던스 per unit volume, t_cathode [cm] 양극 두께).
  ★ **이 eq 7 = kim2025 e-block 해석해 = Bazzoun eq 1 과 동일한 TLM 식.**
- **전체 full cell (eq 6):** `Z_total = Z_cathode,i–e + Z_SE + Z_low + Z_CC`
  (Z_SE = 분리막 bulk+GB, **Z_low = anode+cathode 고상 Li *확산*(Warburg, <30 Hz)**, Z_CC = 집전체).
- ⇒ ★ **full cell = r_i/e(=R_ct, charge-transfer) + Z_low(Warburg 확산)을 정량하는 셀.**

**(대칭셀 TLM, charge-transfer 없는 경우, eq 1)** — Fig 2 의 SSE/composite 피팅 (kim2025 ion-block 해석해와 동형):
```
Z_cathode,e–e = (z_i·z_e)/(z_i+z_e)·t_cathode
              + [2·z_e²·√(z_i/e)/(z_i+z_e)^(3/2)]·{cosh[t_cathode·√((z_i+z_e)/z_i/e)]−1}
                / sinh[t_cathode·√((z_i+z_e)/z_i/e)]
```
(symmetric cell SOC=0 → z_i/e *순수 용량*; eq 1 이 일반형, charge-transfer 항이 용량으로 환원).

### 4.3 ★ Bruggeman tortuosity 정식화 (eq 3–5) — 우리 τ_Laplace,eff 와 정의 동일
복합 양극의 *유효 이온전도도* 와 *tortuosity factor* 를 분리:
```
σ_i,eff = ε_i / τ_eff² · σ_i,0          (eq 3)
σ_i,eff = 1 / r_i                        (eq 4)
τ_eff² = ε_i^(−α)                        (eq 5, 경험적 Bruggeman)
```
- **σ_i,eff** = 복합 양극 유효 이온전도도, **σ_i,0** = pristine SE 펠릿 전도도, **τ_eff** = 유효 tortuosity, **ε_i** = SE 부피분율.
- ★ **eq 3 (σ_i,eff = ε_i/τ_eff²·σ_i,0) = 우리 τ_Laplace,eff 정의 동일** (= Minnmann eq 4 의 τ²=σ_0·φ/σ_eff 와 같은 식).
- ★ **핵심 정식화 통찰:** τ_eff 는 *기하학적* tortuosity τ(굽은 경로 길이/직선거리)와 *다르다* — **r_i,gb(GB)** 같은 *비-기하* 효과까지 τ_eff² 에 흡수 → **r_i,gb 의 τ_eff² = 22** (이상 Bruggeman ≪)·**α=4.3** ≫ 이상 0.5 → **"GB *성장*이 저항↑ 주역"** (tortuous-path 신장으로 설명 불가).  ⇒ ★ **우리 σ_ionic 은 이 r_i,gb 를 *실제 입계 constriction*(Holm)으로 *구조적*으로 풀어** τ_eff 에 럼핑되는 부분을 *명시적*으로 분해 → 우리 우위 (그들 τ_eff² 22 = lumped, 우리는 그 안을 본다).

### 4.4 r_i,gb ↔ r_i/e trade-off 정식화 (eq 7 + Fig 6) — 이 논문의 *설계규칙* 핵심
**미세구조 → 임피던스 항 매핑** (입경 d_CAM 함수):
- **r_i/e (전하전달)** ∝ **1/A_CAM** (CAM 표면적 반비례, Fig 6c): 기울기 **0.082 Ω·cm⁵** = SE/CAM 계면 전하전달 *재료물성*.  → **작은 CAM → A_CAM↑ → r_i/e↓** (전하전달 유리).
- **r_i,gb (입계 이온저항)** ∝ **eps_pore** (공극↑, Fig 6d): 작은 CAM → **비균질 응집(Roller's relationship, ref 44,45) → 더 다공 → r_i,gb↑**.  → **작은 CAM → eps_pore↑ → r_i,gb↑** (이온수송 불리).
- ⇒ ★ **trade-off (Fig 6f):** 작은 CAM = 낮은 r_i/e *but* 높은 r_i,gb; 큰 CAM = 높은 r_i/e *but* 낮은 r_i,gb.  unimodal CAM 으로는 둘 다 못 낮춤.
- ★ **돌파 = bimodal CAM (NCA-b-12 = NCA-4 + NCA-15):** 작은 NCA-4 가 큰 NCA-15 사이 공극을 *충전* → eps_pore 0.11(최저) → r_i,gb 3 240 Ω·cm(최저) *동시에* 큰 입자가 충분한 A_CAM 유지 → r_i/e 도 낮음 → **R_cathode 14 Ω·cm²(최저)**.  ⇒ "**bimodal 이 trade-off 를 돌파**" = 이 논문의 설계 결론.

### 4.5 압밀압력 정식화 (Fig 4) — 3종 가압법
- **UP-C (uniaxial press, cylindrical)** vs **IP-C (isostatic press, cylindrical)** vs **IP-P (isostatic press, pellet)**.
- ★ **r_i,gb 가 압력↑ + 등방가압으로 급감:** UP-C 300 ≈ 8 700 → IP-P 500 MPa = 2 650 Ω·cm; IP-P eps_pore = 0.046 (등방 fluidic-media 가 SE 매끄럽게 소결).  반면 **r_i,bulk 는 압력에 둔감**.
- ★ **IP-P 500 MPa 85°C 의 tau_eff² = 1.46 ≈ 이상 Bruggeman 1.41** → "**낮은 모듈러스 SE(LPSC)가 fluidic-media 가압으로 pristine 펠릿 수준까지 치밀화**" (저자 명시).  → 우리 "압력↑→접촉↑→σ↑·porosity↓" + MPM 소성 void-fill 와 같은 물리.
- ⚠ **단 UP-C 는 SUS 평판이 SSE·CAM 균일 가압 → IP-P 보다 SE 변형 적음**(rigid CAM 에 응력 집중) → 등방가압이 SE densify 에 유리.

### 4.6 입자 처리 ★ (DEM판 "무질서 처리"의 *부재* — 회로 모델)
- ★ **입자 형상·PSD·rigid/plastic 개념이 *명시적으로 없다*.**  미세구조를 *생성하지 않고* 복합 양극을 **분포 임피던스 사다리(z_i, z_e, z_i/e, t_cathode, ε_i)** 로 추상화.  미세구조는 **r_i,gb / r_i/e / eps_pore 라는 *fitted lumped 파라미터*** 로만 들어온다 (입경은 *측정값*으로 r_i/e∝1/A_CAM 회귀에만).
- ⇒ 우리 DEM(구·접촉망)·MPM(소성 형상)·Bazzoun(구 DEM)·Bielefeld(voxel)의 *구조 생성* 차원이 **이 논문엔 통째로 없다** → **frame[5]:** 그들 = *측정/회로/설계규칙*, 우리 = *구조→σ*.

---

## 5. 결과 상세 — Section-by-section (모든 수치)

### 5.1 회로 타당성 검증 (Fig 1, 2) — pristine SE vs composite
**목적:** Fig 1d 회로(z_i = r_i,bulk + r_i,gb∥c_i,gb)가 복합 양극을 가장 잘 표현함을 (i) EIS 피팅 + (ii) 미세구조 SEM 으로 이중 검증.
- **Fig 2a–d (pristine SE):** 단일 반원(저주파) + 고주파 작은 반원(>100 kHz) → **r_i,bulk 178 + r_i,gb 631 = r_i 809 Ω·cm**, E_a 0.33 eV.  ★ **순 SE 도 입계(631)가 입내(178)의 3.5×** → cold-press SE 입계가 이미 주 병목.  SEM: pristine SE = *monolithic*(연성 SE 가 가압으로 dense sinter).
- **Fig 2e–h (composite):** 두 반원(HF >10 Hz, LF <10 Hz) → 두 TLM 회로(Fig 2g vs 2h)로 피팅.  ★ **Fig 2g (z_e 기준, r_e,bulk+r_e,gb/q_e,gb)는 deviate** (NCM 같은 좋은 전자도체에 q_e,gb~10⁻⁹ F 용량은 비물리); **Fig 2h (z_i 기준, r_i,bulk+r_i,gb/q_i,gb)가 일관 피팅** → "**복합 양극 저이온전도 = 높은 r_i,gb(입계) 때문, *tortuous path 아님***" (저자 핵심 주장).  SEM: composite = SE 입자 사이 *void + grain* (NCM 이 SE 소결 방해).

### 5.2 SE 부피분율 스윕 (Fig 3) — r_i,gb 가 저-SE 서 폭증
**셀:** ε_i = 0.49–1.0 (10단계 감소), 대칭셀.
- **Fig 3a (Nyquist):** ε_i 1.0→0.77 = r_i,bulk∥(r_i,gb/q_i,gb) 회로 (HF 작은 반원); **ε_i 0.54–0.68 = teardrop**(r_e≈r_i); **ε_i ≤ 0.49 = 순-R**(반원 소멸, 전자 percolate).  ★ **ε_i 0.77 = NCM 전자 percolation 임계**(LF 급변), **ε_i ≤ 0.49 = 전자경로 완전 확립**.
- **Fig 3b (eps_pore):** ε_i 1.0→0.26 → eps_pore **0.16→0.23** ↑ (★ **SE↓ → 공극↑** — rigid NCM 이 SE 소결 방해).
- **Fig 3c (r_i,bulk vs r_i,gb vs ε_i):** ε_i=0.54 서 **r_i = 18.4 kΩ·cm** (bulk 0.61 + gb 17.7); ε_i=1.0 서 (bulk 0.17 + gb 0.63).  → **r_i,gb 가 저-SE 서 28× 폭증**(0.63→17.7 kΩ·cm), r_i,bulk 는 0.17→0.61 만.  ★ **저-SE 의 17.7 kΩ·cm 는 void-induced 경로신장만으로 설명 불가** (저자: "much higher than expected from elongation").
- **Fig 3d (tau_eff² vs ε_i):** **α(bulk)=0.52 ≈ 이상 0.5**; **α(gb)=4.3 ≫ 이상** → **"GB *성장*이 r_i 증가 주역"** (eq 5 fit).  tau_eff²(gb, ε_i=0.54)=22.
- **Fig 3e–p (SEM):** ε_i 0.49/0.59/0.85/1.0 단면 — 저-ε_i 일수록 void+GB 성장 *명확*.
- **Fig 3q (모식):** SE↓ → pore↑ → r_i,bulk(다소↑) + **r_i,gb(very high→low)**.

### 5.3 압밀압력 (Fig 4) — r_i,gb 가 압력·등방가압으로 급감
**셀:** ε_i=0.58, UP-C/IP-C/IP-P × 300/400/500 MPa.
- **Fig 4b (Nyquist):** 압력↑ → 두 반원 모두 축소 (r_i, r_e 둘 다↓).
- **Fig 4c (r_i,bulk·r_i,gb vs P):** **r_i,gb 가 remarkable 하게 급감** (UP-C 300 ≈8.7 → IP-P 500 = 2.65 kΩ·cm); r_i,bulk 둔감.
- **Fig 4d (eps_pore vs P):** IP-P 500 MPa = **0.046** (등방가압 SE 매끄럽게 소결); UP-C 가 가장 높음.
- **Fig 4e (IP-P 500 온도 스윕):** r_i,gb 가 온도↑로 더 감소 (큰 E_a).
- **Fig 4f (r_e vs P):** 500 MPa 서 모든 셀 r_e < 15 kΩ·cm; **UP-C/IP-C(SUS) < IP-P(pouch)** → SUS 평판이 CAM 에 응력 집중 → CAM 전자접촉 더 좋음(but SE densify 덜).
- **Fig 4g,h (요약):** IP-P 500 MPa 85°C tau_eff²=**1.46 ≈ 1.41 이상** → **거의 완전 SE 치밀화**.  ★ "**낮은 모듈러스 SE 가 fluidic-media 등방가압으로 pristine 수준까지 densify**" (저자).

### 5.4 CAM 입경 효과 (Fig 6) ★ trade-off 발견 + bimodal 돌파
**셀:** In/SSE\|CAM+CF\|SSE full cell, CAM = NCA-4(4µm)/NCA-15(15µm)/NCM-7(7µm)/NCA-b-12(bimodal 12µm).
- **Fig 6a (Nyquist + SEM):** 4 종 CAM 별 양극 임피던스; SEM 으로 입경·공극 확인.
- **Fig 6b (r_i,gb vs r_i/e 등고선 맵):** R_cathode = f(r_i,gb, r_i/e) (eq 7) → 2D 맵에 각 CAM 좌표.  ★ **NCA-4(작음) = 높은 r_i,gb·낮은 r_i/e**; **NCM-7 = 낮은 r_i,gb·높은 r_i/e** → *반대 위치* = **계면저항 구성이 입경으로 *반전*** (R_cathode 는 비슷해도).
- **Fig 6c (r_i/e vs 1/A_CAM):** ★ **r_i/e ∝ 1/A_CAM** (선형), 기울기 **0.082 Ω·cm⁵** = 전하전달 재료물성.  → 작은 CAM → A_CAM↑ → r_i/e↓.  NCM-7 의 r_i/e 가 NCA 보다 *훨씬 큼* (LPSC/NCM 계면 전하전달이 LPSC/NCA 보다 느림).
- **Fig 6d (r_i,gb vs eps_pore):** ★ **r_i,gb ∝ eps_pore** (거의 동일 양 셀). → 작은 CAM → 비균질 응집(Roller) → eps_pore↑ → r_i,gb↑.
- **Fig 6e (eps_pore vs d_CAM):** ★ **작은 CAM → eps_pore↑** (Roller's relationship, 작은 입자 비균질 응집 → 더 다공).
- **Fig 6f (모식):** **작은 CAM = 높은 r_i,gb·낮은 r_i/e·높은 A_CAM; 큰 CAM = 반대** → trade-off.
- ★ **bimodal NCA-b-12 돌파:** 작은 NCA-4 가 큰 NCA-15 사이 충전 → eps_pore **0.11**(최저) → r_i,gb **3 240 Ω·cm**(최저) + 큰 입자 충분한 A_CAM → r_i/e 도 낮음 → **R_cathode 14 Ω·cm²**(최저, unimodal 20–25 대비).  ⇒ "**bimodal CAM 이 r_i/e–r_i,gb trade-off 를 *동시* 돌파**".

### 5.5 셀 성능 (Fig 7) — bimodal 고에너지·고출력 실증
- **Fig 7a–c (rate capability):** NCA-b-12 vs NCA-15/NCA-4/NCM-7, 0.1–2C (projected 5 mAh/cm²).  ★ **NCA-b-12 0.1C = 4.1 vs NCM-7 3.5 mAh/cm²**; **2C(10 mA/cm²): NCA-b-12 2.1 vs NCM-7 0.3 = 7×** (낮은 R_cathode → 낮은 IR drop → 높은 초기 전압 3.00 vs 2.63 V).  ★ **"cathodic resistance 가 고율 용량을 직접 좌우"**.
- **Fig 7d–g (pouch high-energy):** 105 µm NCA-b-12 양극 → **5.3 mAh/cm²@0.1C(171 mAh/g), 5.0@0.33C(159 mAh/g)** → **>800 Wh/kg·>1100 Wh/L**; **85 % over 300 cyc, CE 99.9 %**.  internal R(IV slope)=58 ≈ EIS(R_SE+R_cathode+R_anode)=57 Ω·cm² (자기일관 검증).

### 5.6 §결론 (저자 요약)
- TLM 회로(Fig 1d, 두 핵심 계면저항 r_i,gb + r_i/e)로 복합 양극 charge-transport 정량 → **저이온전도 = 높은 r_i,gb(입계) 때문, *tortuous path 아님***.
- **저-SE·저압·작은 CAM → 높은 r_i,gb**; **작은 CAM → 낮은 r_i/e** → trade-off → **bimodal CAM 으로 둘 다↓** → 고에너지·고출력 ASSB.
- ★ **LE 양극엔 없는 현상** (LE 는 액체전해질이 입계 없음 → r_i,gb 무관).

---

## 6. Figure / Table set ★ (모든 그림 + 우리가 쓸 점)
| Fig | 내용 (무엇을 보여주나) | 핵심 수치 | 우리가 참고할 점 |
|---|---|---|---|
| **1a** | ASSB 복합 양극 전기화학 과정 + TLM 회로 모식 (z_i/z_e/z_i/e) | — | ★ 두 레일+crossrail = 우리 저항망의 임피던스판 |
| **1b** | LE 양극 TLM (z_i=r_i,bulk, GB 없음) | — | ★ **LE 엔 r_i,gb 없음** = SE 복합 양극과 본질 차이 |
| **1c,d** | SE 복합 양극 TLM (z_i = r_i,bulk+r_i,gb/c_i,gb) | — | ★ **Fig 1d 채택 회로** (kim2025·Bazzoun eq 1 동형) |
| **1e** | full-cell ASSB TLM (z_i/e=R_ct 살아남) | — | ★ **R_ct 분리 BC** (eq 7) |
| **2a–d** | pristine SE Nyquist + 회로 + Arrhenius | r_i,bulk 178·r_i,gb 631·E_a 0.33 eV | ★ **순 SE 입계 631 = 입내 178 의 3.5×** |
| **2e–h** | composite Nyquist + 두 회로 비교 (z_e vs z_i) | r_i=12.8 kΩ·cm; Fig 2h 채택 | ★ **저이온전도 = r_i,gb, not tortuous path** |
| **3a** | ε_i 0.49–1.0 Nyquist | 0.77 전자임계·0.49 순-R | ★ 전자 percolation 임계 |
| **3b** | eps_pore vs ε_i | 0.16(1.0)→0.23(0.26) | ★ **SE↓→공극↑** (rigid NCM) |
| **3c** | r_i,bulk·r_i,gb vs ε_i | 0.54: 18.4 kΩ·cm (gb 17.7) | ★ **r_i,gb 저-SE 서 28× 폭증** |
| **3d** | tau_eff² vs ε_i (Bruggeman α) | **α_bulk 0.52·α_gb 4.3** | ★ **GB 성장이 저항 주역; τ_eff 정의=우리 τ_Laplace** |
| **3e–p** | ε_i 0.49/0.59/0.85/1.0 SEM | — | void+GB 성장 시각화 |
| **3q** | SE↓ → r_i,bulk/r_i,gb 모식 | — | 정성 추세 |
| **4a** | 3종 가압법(UP-C/IP-C/IP-P) 모식 | — | 제조압 구분 |
| **4b** | 압력별 Nyquist+SEM | — | 압력↑→반원↓ |
| **4c** | r_i,bulk·r_i,gb vs P | UP-C 300 8.7→IP-P 500 2.65 kΩ·cm | ★ **압력·등방가압이 r_i,gb 급감** |
| **4d** | eps_pore vs P | IP-P 500 = 0.046 | 등방가압 SE 소결 |
| **4e** | IP-P 500 온도 스윕 | r_i,gb 온도↓ | GB 큰 E_a |
| **4f** | r_e vs P | <15 kΩ·cm@500; SUS<pouch | CAM 전자접촉 |
| **4g,h** | 압력 효과 요약 + tau_eff² | **IP-P 500 85°C tau_eff²=1.46≈1.41** | ★ **거의 완전 SE 치밀화 = MPM void-fill** |
| **5** | full-cell 회로 (eq 7) | — | ★ charge-transfer z_i/e |
| **6a** | 4종 CAM Nyquist+SEM | — | 입경별 임피던스 |
| **6b** | R_cathode 등고선 맵 (r_i,gb vs r_i/e) | NCA-4·NCM-7 반대 위치 | ★ **trade-off 시각화** |
| **6c** | r_i/e vs 1/A_CAM | **기울기 0.082 Ω·cm⁵** | ★ **r_i/e ∝ 1/A_CAM** (= 우리 coverage/A_AM-SE) |
| **6d** | r_i,gb vs eps_pore | 거의 동일선 | ★ **r_i,gb ∝ eps_pore** |
| **6e** | eps_pore vs d_CAM | 작은 CAM→eps_pore↑ | ★ Roller's relationship |
| **6f** | 입경 trade-off 모식 | — | ★ **작은 CAM = r_i/e↓·r_i,gb↑** |
| **7a–c** | rate capability (4종 CAM) | NCA-b-12 2C 2.1 vs NCM-7 0.3 (7×) | ★ **R_cathode→고율 용량** |
| **7d–g** | pouch 고에너지 (105 µm NCA-b-12) | >800 Wh/kg·>1100 Wh/L·85%@300cyc | ★ bimodal 실증 |
| **S5** | model simulation (회로요소→Nyquist 형태: teardrop/collapsed/double-peak) | — | ★ r_i,gb<r_i/e=teardrop; >=double-peak |
| **S7,TableS3** | stack number → energy density | >5 mAh/cm² stacked | 스택 설계 |

---

## 7. Post-processing ★
- **무엇:**
  - **TLM 등가회로 피팅** (대칭셀 eq 1 / full-cell eq 7) → r_i,bulk / r_i,gb / c_i,gb / r_e / r_i/e(=R_ct) / Z_low(Warburg) / Z_SE / Z_CC 분해.  해석해 = de Levie/Siroma TLM.
  - **Bruggeman tortuosity 분석** (eq 3–5): σ_i,eff = ε_i/τ_eff²·σ_i,0, τ_eff² = ε_i^(−α) → α(bulk)=0.52·α(gb)=4.3 → "GB 성장 vs 경로신장" 진단.
  - **eps_pore 측정** (펠릿 부피 − 성분 부피)/펠릿 부피 (FIB cross-section polish + SEM).
  - **r_i/e ∝ 1/A_CAM 회귀** (입경→표면적→전하전달) + **r_i,gb ∝ eps_pore** (입경→공극→입계).
  - **model simulation (Fig S5):** 회로요소 파라메트릭 → Nyquist 형태 변화 (r_i,gb<r_i/e → teardrop; r_i,gb≈r_i/e → collapsed-semicircle; r_i,gb>r_i/e → double-peak).  ★ **kim2025 의 R_int/R_i 분해 가능성 논리와 동형.**
  - **Kramers–Kronig (Fig S8–S10):** EIS 신뢰성(인과·선형) 검증, relative error <±1.0 %.
- **도구:** **BioLogic VMP-3**(EIS 1 MHz–10 mHz), **Excel Solver**(χ² 최소화 회로 피팅), **SU8030 FE-SEM**(Hitachi) + **IB-19520CCP**(JEOL, cooling cross-section polisher), TOSCAT-3100(cycling).
- **수치화·기록:** ε_i(0.49–1.0)·압력(300–500 MPa, UP-C/IP-C/IP-P)·온도·CAM 입경(4/7/12/15 µm)·모달리티(uni/bimodal)별 r_i,bulk/r_i,gb/r_i/e/r_e/eps_pore/tau_eff² 를 Fig + Table S1–S5 로.

---

## 8. ## 우리 DEM+MPM 대비 (comparison vs ours) → `our_dem_baseline.md`

> ★ 핵심 framing: **그들 = 계면 임피던스의 *해석적 정식화*(주파수영역 회로) + 설계규칙; 우리 = 미세구조→ASR 의 *수치 계산*(공간 Kirchhoff/Holm 저항망, constriction-resolved).**  목적(전달·계면 분해) 같음, 방법 다름 → frame[4] 외부 *방법론* 대조 + frame[5] 빈 칸 표시.

| 항목 | 이 논문 (Choi 2024) | 우리 | 차이 / 이유 |
|---|---|---|---|
| **방법** | **실험 EIS + TLM *해석적 정식화*** (주파수영역 임피던스 회로 eq 1–7) | **DEM Kirchhoff/Holm σ-솔버** (공간 저항망 DC 풀이) + Stage-E 소성면적 | ★ **목적 같음(전달·계면 분해), 형식 다름** — 그들=정식화/측정/회로, 우리=구조→σ.  frame[4] 방법론 대조 |
| **이온저항 → σ** | **r_i = r_i,bulk + r_i,gb → σ_i,eff = 1/r_i** (eq 4); 복합 ε_i=1.0 r_i=12.8 kΩ·cm → σ≈0.078 | **σ_ionic = R=L/σ on Kirchhoff/Holm net** (LOOCV 0.975); ASR_ionic | ★ **그들 r_i → σ_i,eff 가 우리 σ_ionic(ASR_ionic)의 *정확한* 카운터파트** — 같은 양을 측정 vs 계산 |
| **GB(입계) 저항** | ★ **r_i,gb 를 r_i,bulk 와 *분리*** (순SE 631 vs 178 = 3.5×; 복합 ε0.54 17.7 kΩ vs 0.61 = 29×) + **α_gb=4.3** | Cronau(r_SE) sub-µm **GB 인자** (σ_grain prefactor 럼핑) | ★ **그들이 GB 를 *분리 측정/정식화*** → 우리 GB 인자 정당화 (입계가 주 병목); kim2025·Minnmann 과 합류 |
| **tortuosity** | **τ_eff² = ε_i^(−α)** (eq 5); α_bulk 0.52·α_gb 4.3 | **τ_Laplace,eff = σ_0·φ/σ_eff** (정의 동일) | ★ **τ_eff 정의 *동일*** — 단 그들 τ_eff² 22(gb)는 *constriction+GB 럼핑*; ★ **우리 σ_ionic 은 그 안의 contact constriction(Holm 1/(2σr_c))을 *명시 분해*** = 우리 우위 |
| **constriction 저항** | **lumped (τ_eff·r_i,gb 에 흡수)** — 명시 안 함 | ★ **Holm 1/(2σr_c) + Stage-E 소성면적으로 *명시 계산*** (constriction-resolved) | ★ **우리 핵심 우위** — 그들이 r_i,gb 로 럼핑한 입계 constriction 을 우리는 *실제 접촉 반경*으로 풂 |
| **전자저항** | **r_e 측정** (전자 percolation 임계 ε_i=0.77) | **σ_electronic** (LOOCV 0.953; f_p percolation 항) | ★ 그들 ε_i=0.77 전자임계 ↔ 우리 σ_e f_p/dead-AM (Bielefeld p_c·Minnmann 42 vol% 교차) |
| **r_i/e (= R_ct, 전하전달)** | ★ **정식화·측정** (r_i/e ∝ 1/A_CAM, 기울기 0.082 Ω·cm⁵; full cell) | ★ **미보유** (constriction-only σ-솔버) | ★ **우리 *전혀* 안 잡는 계면반응** — frame[5] 빈 칸 (kim2025 와 동일) |
| **Z_low (Warburg 확산)** | ★ **정식화·측정** (13.9 Ω·cm², <30 Hz) | ★ **미보유** (D_Li 모델 없음) | ★ 활물질·음극 고상 Li 확산 = 우리 transport 밖 |
| **C_dl (이중층)** | c_i,gb·CPE (회로 요소) | ★ **미보유** | ★ 우리 밖 |
| **eps_pore** | **측정** (0.046–0.23, ε_i·압력·입경 함수) | DEM porosity 15.6 % / MPM 16.7 % | ★ **추세 비교**(SE↓→공극↑·압력↑→공극↓·작은CAM→공극↑ 다 우리와 정합); **절대 직접 금지** (그들 eps_pore = composite-cell 펠릿; Cl₁.₂₅ Cl-rich) |
| **압밀압력** | **r_i,gb 가 압력↑·등방가압 급감** (8.7→2.65 kΩ; IP-P 500 85°C tau_eff²=1.46≈이상) | DEM 300 MPa·Heckel P_y 138; MPM 소성 void-fill | ★ **"낮은 모듈러스 SE 가 등방가압으로 pristine 수준 densify"** = 우리 MPM void-fill·So 2021 H-cap 와 같은 물리 |
| **CAM 입경 trade-off** | ★ **r_i,gb↔r_i/e 입경 trade-off → bimodal 돌파** | DEM bimodal 12:4:1 Furnas dip (AM 70–85 wt%) | ★ **그들 bimodal 동기(trade-off 돌파) ≠ 우리 dip 동기(packing)** — 단 **둘 다 "bimodal 이 좋다"** (다른 이유로 수렴); ★ 우리 dip = *porosity/packing*, 그들 = *r_i,gb+r_i/e 임피던스* |
| **소재** | **LPSC Li₅.₇₅PS₄.₇₅Cl₁.₂₅ (Cl-rich) + NCM90/NCA94** | LPSCl Li₆PS₅Cl + NMC811 | ★ **같은 argyrodite 황화물 + Ni-rich NCM/NCA** → 추세 직접 비교; **조성 차(Cl₁.₂₅·Ni0.9-0.94) → 절대값 전이 주의** |
| **소성/morphology** | 없음 (회로 모델, 입자 형상 개념 X) | MPM 진짜 SHAPE 소성 | 우리 MPM 고유 (frame[5]) |
| **transport 채널** | σ_ion(r_i) + σ_e(r_e) + **R_ct(r_i/e) + Warburg(Z_low)** (계면·확산까지) | σ_ion + σ_e + σ_thermal (수송 삼중항) | ★ **상보**: 우리=수송 3채널 깊이(σ_thermal 그들 없음), 그들=수송+계면+확산 폭 |
| **설계규칙** | ★ **bimodal CAM·등방가압·고-CAM 으로 r_i,gb+r_i/e↓** → 고에너지·고출력 | predictor(σ 삼중항 LOOCV 0.90–0.975) → 설계공간 | ★ **그들 설계규칙 = 우리 predictor 교차검증 가설** (입경·압력·조성→σ) |

**핵심 정합/상보 4가지:**
1. **r_i → σ_i,eff = 우리 σ_ionic(ASR_ionic)의 정확한 카운터파트** — 같은 양을 그들 *측정/정식화* vs 우리 *구조 계산* (frame[4] 방법론 대조).
2. **r_i,gb 를 *분리 정식화*(α_gb=4.3 ≫ 이상)** — 우리 Cronau(r_SE) GB 인자를 정당화 (입계가 주 병목; kim2025·Minnmann 합류).  ★ 단 **우리 우위**: 우리 σ_ionic 은 r_i,gb 로 럼핑되는 *입계 constriction*(Holm)을 *명시 분해* — 그들 τ_eff²=22 의 *내부*를 본다.
3. **r_i/e(R_ct)·Z_low(Warburg)·C_dl = 우리 *전혀* 안 갖는 계면반응·확산 kinetics** — frame[5] 빈 칸 (kim2025 와 *동일*).
4. **압력·입경·SE 분율 → eps_pore·r_i,gb 추세 전부 우리와 정합** (SE↓→공극↑, 압력↑→공극↓, 작은 CAM→공극↑) → frame[4] 추세 교차검증.

---

## 9. ## 적용가능성 (applicability to our model)

> ★ 핵심: **이 논문의 임피던스 정식화 = 우리 *기하학적* ASR(constriction-resolved) 위에 charge-transfer R_ct / double-layer C_dl / Warburg 를 *얹는* 구체적 경로** (= kim2025 가 짚은 frame[5] kinetics 칸의 *정식화 버전*).  그들 설계규칙 = 우리 predictor 교차검증.

- ① **r_i → σ_i,eff 를 우리 σ_ionic(ASR_ionic) 의 *방법론적* 카운터파트로 명문화 (frame[4])**:
  같은 LPSC 황화물 복합 양극에서 그들 **r_i = r_i,bulk + r_i,gb** 가 우리 σ_ionic(R=L/σ on Kirchhoff/Holm)이 계산하는 바로 그 양.  ★ **우리 ASR_ionic = r_i·t_cathode** (eq 4 → ASR), **우리 σ_ionic = 1/r_i = σ_i,eff** 직접 대응.  → deck/paper 에 "우리 구조-기반 σ_ionic 은 Choi 2024 가 EIS 로 정식화/측정한 r_i 의 *first-principles 미세구조* 버전" 으로.  ⚠ 조성 차(Cl₁.₂₅·NCM90) → 추세·방법 대조, 절대값은 Bazzoun/Minnmann(우리 LPSCl) 우선.

- ② **r_i,gb ∝ eps_pore + α_gb=4.3 → 우리 σ_ionic 의 GB·porosity 결합 강화 (구체적 흡수)**:
  그들 핵심 정식화 = **r_i,gb 가 *tortuous path 가 아니라 GB 성장*(eps_pore↑)으로 폭증** (α_gb 4.3 ≫ 이상 0.5).  → ★ **흡수 후보:** 우리 σ_ionic 의 Cronau(r_SE) GB 인자를 *porosity-결합*(eps_pore↑ → GB density↑ → σ_grain prefactor↓)으로 확장.  우리는 이미 σ_thermal Ridge 에 grain-boundary-density feature 를 쓰므로 그 GB-density 를 σ_ionic 으로 끌어올 *정식화 근거*(r_i,gb ∝ eps_pore)를 이 논문이 제공.  ★ 단 **우리 우위 유지**: 우리는 GB constriction 을 Holm 으로 *명시 계산*하므로 α_gb 같은 *경험 지수*에 의존 안 함 — 우리 σ_ionic 이 그들 r_i,gb 를 *예측*할 수 있음(검증 lever, backlog B1).

- ③ **r_i/e(=R_ct) + C_dl + Z_low(Warburg) 정식화 = 우리 *미보유* kinetics 칸의 *구현 청사진* (backlog A1/kinetics)**:
  우리 σ-솔버는 **z_i(이온수송)만**.  이 논문(+kim2025)이 분해한 **r_i/e(전하전달)·c_i,gb(이중층)·Z_low(Warburg 확산)** 는 우리가 *전혀* 안 다룬다.  ★ **구체적 흡수 경로:**
  - **R_ct ∝ 1/A_CAM** (Fig 6c, 기울기 0.082 Ω·cm⁵) → 우리 **coverage/A_AM-SE** (Stage-E 가 이미 계산!) 에 *전하전달 재료물성 상수* 를 곱해 **R_ct = k_ct/A_AM-SE** 형태로 *얹기* 가능 — 우리 coverage 가 이미 A_CAM-SE 를 주므로 **R_ct 칸을 우리 기하 위에 직접 추가** (kim2025 R_ct 절대값 + 이 논문 1/A 스케일링).
  - **ASR_total = ASR_ionic(우리) + ASR_electronic(우리) + R_ct(1/A_AM-SE, 신규) + Z_low(Warburg, 신규 D_Li)** → *전체* 셀 임피던스로 확장.  → `our_dem_baseline.md §4` + `comparison_vs_ours.md F` 에 "계면 R_ct(∝1/coverage)·C_dl·Warburg = 우리 transport 밖, Choi 2024/kim2025 정식화로 *얹기* 가능" 명시.

- ④ **r_i,gb 의 압력·등방가압 의존 → 우리 압밀-σ 결합 검증 (frame[4])**:
  그들 **r_i,gb 가 압력↑·등방가압으로 급감** (8.7→2.65 kΩ; IP-P 500 85°C tau_eff²=1.46≈이상) → 우리 "압력↑→접촉↑→σ↑·porosity↓" + Heckel + MPM void-fill 와 *같은 물리*.  ★ **검증 가설:** 우리 σ_ionic 이 압력 sweep(우리 DEM 4압력)에서 r_i,gb↓ 추세를 재현하는지 (Bazzoun σ-vs-P·우리 Heckel P_y 138 와 합류).  IP-P 등방가압이 SE 를 pristine 수준 densify = 우리 MPM 소성 흐름의 *실험 대조*.

- ⑤ **bimodal CAM 설계규칙 ↔ 우리 Furnas dip (다른 동기, 같은 결론 — 교차검증)**:
  그들 bimodal 동기 = **r_i,gb↔r_i/e trade-off 돌파**(임피던스); 우리 dip 동기 = **packing/porosity 최소**(기하).  → ★ **두 *독립* 논리가 "bimodal CAM 이 최적"으로 수렴** = 강력한 frame[4] 교차검증.  우리 predictor 가 bimodal 12:4:1 에서 porosity dip + σ↑ 를 주는데, 그들은 그 *같은* bimodal 이 R_cathode 최저(14 Ω·cm²)를 줌을 *실험 실증*.  → deck: "우리 packing-기반 bimodal 최적이 Choi 2024 의 impedance-기반 bimodal 최적과 독립 수렴".  ⚠ 그들 bimodal = *CAM*(NCA-4+15), 우리 12:4:1 = *AM:SE_large:SE_small* → 모달리티 주체 다름(주의).

- ⑥ **설계규칙 → 우리 predictor 교차검증 (Phase 3–5)**:
  그들 정량 추세 (작은 CAM→r_i/e↓·r_i,gb↑; 고-CAM→고출력; 등방가압→densify) → 우리 predictor(σ 삼중항)가 같은 입경·압력·조성 의존을 주는지 cross-check.  특히 **R_cathode(14–25 Ω·cm²) = 우리 ASR_cathode 와 절대 대역 비교** (단 Cl₁.₂₅·NCM90 보정 후).

---

## 10. ## frame[4]/[5] 위치

> ★ 이 절은 "이게 무엇인가(positioning)" — **DEM 경쟁자 아님**, *분석적 임피던스 정식화 + 실험* 이다.  우리 network-resolved ASR 우위와 우리가 흡수할 R_ct/Warburg 정식화를 명확히 구분.

### 10.1 이 논문의 성격 — analytical theory + experiment (not simulation peer)
- **DEM/MPM/FEM 미세구조 *생성* 없음.**  미세구조는 r_i,gb/r_i/e/eps_pore 라는 *fitted lumped 파라미터*로만 들어온다 (입경은 r_i/e∝1/A_CAM 회귀에만).  ⇒ **우리 구조→σ 솔버의 *경쟁자가 아니라* 그 출력의 *주파수영역·실험 검증* 카운터파트** (frame[4] 외부 *방법론* 대조).
- **회로 = de Levie/Siroma TLM 의 *정식화*** (eq 1–7) — kim2025·Bazzoun 과 *같은 식*.  novelty = **(a) NCM/NCA+LPSC 복합 양극 적용 + 회로 타당성 이중검증(EIS+SEM), (b) r_i,gb↔r_i/e trade-off 발견, (c) bimodal 돌파 설계규칙**.  → *방법론 부모*(우리 kim2025 anchor 의 선행 정식화)이자 *설계규칙 제공자*.

### 10.2 우리 explicit-network 시뮬이 *더하는* 것 (network-resolved ASR 우위 — 명확히)
- ★ **그들 r_i,gb·τ_eff² 는 입계 constriction 을 *럼핑*** (τ_eff²=22, α_gb=4.3 = *경험 지수*).  ★ **우리 σ_ionic 은 그 입계 constriction 을 *명시* 분해** — Holm 1/(2σr_c) + 실제 접촉반경 r_c(구-구 교차/소성변형) + Stage-E 소성 접촉면적 → **입계 면적·배위수·coverage·percolation 까지 구조에서 직접** (그들은 측정된 lumped R 뿐).  ⇒ ★ **우리는 "왜 r_i,gb 가 그 값인가"를 *미세구조*로 설명**; 그들은 "r_i,gb 가 이 값이다"를 *측정*.  → **우리 σ_ionic 이 그들 r_i,gb 를 *예측*할 수 있다** (frame[4] 검증 lever; 우리 advantage).
- ★ **우리 σ_e + σ_thermal 삼중항** (그들 σ_thermal 없음); **Stage-E 소성 접촉면적** (RNM/τ_eff 가 못 잡는 plastic-area 보정); **MPM 진짜 SHAPE 소성·void-fill·변형장** (그들 입자 형상 개념 X); **Furnas dip 정량**(그들 bimodal 은 임피던스 동기, dip 위치/깊이 X); **fracture-Holm/Auerbach**.

### 10.3 우리가 *흡수*할 것 (우리 부족분 — 정직)
- ★ **R_ct(r_i/e) + C_dl(c_i,gb) + Warburg(Z_low) 정식화** = 우리 *미보유* frame[5] kinetics 칸 (kim2025 와 동일 빈 칸).  → ★ **이 논문이 그 *정식화 + 스케일링*을 줌:** R_ct ∝ 1/A_CAM (Fig 6c) → 우리 coverage(A_AM-SE, Stage-E 가 이미 계산) 위에 *직접 얹기* 가능 (§9③).  Z_low = anode+cathode 고상 Li 확산(Warburg) → 우리 D_Li 모델 신규.
- ★ **압력→r_i,gb 정식화** (등방가압 densify) = 우리 압밀-σ 결합 검증점.
- ★ **bimodal 설계규칙** = 우리 dip 의 *독립* 교차검증.

### 10.4 한 줄 정리 (positioning)
> **Choi 2024 = 우리 kim2025 임피던스-분해 앵커의 *방법론적 부모* — 계면 임피던스를 r_i,bulk/r_i,gb/r_i/e/r_e/Z_low 로 *해석적 정식화*하고 NCM/NCA+LPSC 에 적용해 *bimodal 설계규칙*까지 도출한 SAIT 논문.**  우리 network-resolved σ_ionic 은 그들이 *럼핑*한 입계 constriction(τ_eff²=22)을 *명시* 분해해 r_i,gb 를 *미세구조에서 예측*(우리 우위); 반대로 그들이 *정식화*한 **R_ct(∝1/A_CAM)·C_dl·Warburg 는 우리 *미보유* kinetics 칸의 *구현 청사진***(우리 coverage 위에 얹기).  소재 차(Cl₁.₂₅·NCM90)로 절대값 전이는 주의, 추세·방법·설계규칙은 직접 비교.

---

## 11. 인용 가능 문장 (deck/paper용)
- "Choi et al. (SAIT, ACS AMI 2024) **formulate the interfacial impedance of an LPSC/NCM(NCA) composite cathode** with a transmission-line (de Levie) circuit that decomposes it into bulk and grain-boundary ionic resistivity (r_i,bulk + r_i,gb), interfacial charge-transfer resistance (r_i/e), electronic resistance (r_e) and a low-frequency solid-state-diffusion (Warburg) element — the analytical, frequency-domain counterpart of our structurally-resolved Kirchhoff/Holm σ_ionic (= 1/r_i)."
- "Their fit attributes the high composite-cathode ionic resistivity to a **dominant grain-boundary term (r_i,gb), not to ion-path tortuosity** (Bruggeman exponent α_gb = 4.3 vs α_bulk = 0.52), and shows r_i,gb scales with pore volume — directly justifying the Cronau(r_SE) grain-boundary factor in our σ_ionic prefactor, which our explicit network resolves as Holm constriction rather than lumping it into τ_eff²."
- "They report an **unexpected r_i,gb ↔ r_i/e trade-off with CAM particle size** (smaller CAM → larger surface area → lower charge-transfer r_i/e ∝ 1/A_CAM, but more porous packing → higher grain-boundary r_i,gb) and resolve it with a **bimodal CAM** (NCA-4 + NCA-15) that minimises both (R_cathode 14 vs 20–25 Ω·cm²) — an impedance-driven optimum that independently converges with our packing-driven Furnas-dip optimum for bimodal mixtures."
- "Because the formulation provides r_i/e ∝ 1/A_CAM, it is a concrete route to **add the charge-transfer and Warburg kinetics our geometric ASR currently lacks** (frame [5]): R_ct can be placed on the Stage-E-computed AM/SE contact area (coverage) our solver already produces, extending ASR_total to ASR_ionic + ASR_electronic + R_ct + Z_low."

---

## 12. 주의/한계 (over-claim 방지)
- **임피던스 *정식화 + 실험* 논문 = DEM/MPM/FEM 미세구조 *생성 없음*.**  미세구조는 r_i,gb/r_i/e/eps_pore 라는 *fitted lumped 파라미터*로만 들어온다 (입자 형상·rigid/plastic 개념 X).  → frame[4] *방법론* 대조이지 *경쟁 솔버* 아님.
- **소재 차 주의:** SE = **Li₅.₇₅PS₄.₇₅Cl₁.₂₅ (Cl-rich argyrodite, Mitsui)** ≠ 우리 **Li₆PS₅Cl**; CAM = **NCM90/NCA94** ≠ 우리 **NCM811**.  같은 황화물·Ni-rich 계열이라 *추세·물리·방법*은 직접 비교 OK, **σ 절대값·r_i,gb·r_i/e 절대값 전이 금지** (조성차).  우리 LPSCl 절대 앵커는 Bazzoun/Minnmann/kim2025 우선.
- **r_i,gb/r_i/e 는 *측정+TLM 피팅* 값** → *예측 솔버* 산출 아님.  우리 σ_ionic(계산)과 비교 시 "그들=실험/정식화 진실, 우리=구조 예측"(frame[4]).
- **R_ct/Warburg/C_dl = 우리 *미보유* 칸** → 우리가 이걸 "재현/검증" 한다고 하면 *틀림*.  우리는 z_i(이온수송)만 → 이 논문이 정식화한 *계면반응·확산*은 우리 모델 밖 (frame[5] 빈 칸; kim2025 와 동일).  "우리가 cross-validate" 가 아니라 "이걸 *얹을* 정식화를 그들이 줌" 으로.
- **eps_pore ≠ 우리 압밀 porosity 직접 비교 금지:** 그들 eps_pore(0.046–0.23)는 *composite-cell 펠릿*(NCM 이 SE 소결 방해, 800 µm)이고 Cl-rich SE → 우리 DEM 15.6 %·Minnmann 14 %·Doux 18 % 와 *추세*만 (SE↓→공극↑·압력↑→공극↓·작은CAM→공극↑ 다 정합).
- **bimodal 동기 다름:** 그들 = *r_i,gb↔r_i/e 임피던스 trade-off*; 우리 = *packing/porosity dip*.  "둘 다 bimodal 최적" 은 *독립 수렴*(강한 교차검증)이지 *같은 메커니즘 아님*.  + 모달리티 주체 다름 (그들 CAM bimodal, 우리 AM:SE_L:SE_S 12:4:1).
- **r_i/e ∝ 1/A_CAM 기울기 0.082 Ω·cm⁵ = NCA 계** (LPSC/NCA 전하전달); NCM-7 의 r_i/e 는 *훨씬 큼*(LPSC/NCM 더 느림) → 재료-특이.  우리가 R_ct=k/A 로 얹을 때 k 는 *우리 NCM811/LPSCl* 값(kim2025 coated 17–22·uncoated 290–453 Ω·cm²)을 써야 (이 논문 NCA 슬로프 직접 전이 금지).
- **압력 3종 구분:** 제조/압밀 **300–500 MPa** (UP-C/IP-C/IP-P) ≠ **작동 stack 4 MPa** (pouch test).  r_i,gb 는 *압밀된 구조*를 측정한 값 — separator 433/제조 500 은 우리 300·Minnmann 380·Doux 370 보다 약간 높은 고압 (Cl-rich SE).
- **Bruggeman τ_eff² 는 *경험 fit*** (eq 5, α 자유): α_gb=4.3 = 비물리적으로 큼(이상 0.5) → "GB 성장" 해석은 옳으나 *τ_eff 가 constriction 까지 럼핑*한 결과 (Bielefeld 2020 "Bruggeman 4× 과소"와 같은 결).  우리 σ_ionic 은 이 럼핑을 *피해* constriction 을 명시 분해 → 우리 우위지만, 그들 τ_eff 절대값을 우리 τ_Laplace 와 byte-비교 금지.

---

## 13. 미니 용어집 (technique glossary)
- **TLM (Transmission Line Model) / de Levie 회로** — 다공·복합 매질의 *분포* 임피던스 모델.  이온/전자 두 레일을 무한 RC 사다리망으로 짜고 crossrail(계면)로 결합.  단순 R∥C 로 안 되는 복합 양극에 필수.  "interfacial impedance formulation" = 이 회로의 각 항을 물리 과정에 *매핑*해 정식화.
- **r_i,bulk (intragrain ionic resistivity)** — SE 입자 *내부* Li⁺ 전도 저항 [Ω·cm].  압력·SE분율에 둔감.
- **r_i,gb (grain-boundary ionic resistivity)** — SE/SE *입계* Li⁺ 저항 [Ω·cm].  ★ cold-press 황화물의 주 병목; eps_pore↑·저-SE·저압서 폭증; α_gb=4.3(이상 0.5≫) → "GB 성장이 주역".
- **r_i = r_i,bulk + r_i,gb → σ_i,eff = 1/r_i (eq 4)** — 복합 양극 *유효 이온저항 → 유효전도도*.  ★ **우리 σ_ionic 의 카운터파트.**
- **r_i/e (= z_i/e = R_ct, charge-transfer resistance)** — SE/CAM 계면에서 Li⁺+e⁻ → 활물질 격자 *반응* 저항 [Ω·cm³ per volume].  ★ **r_i/e ∝ 1/A_CAM** (CAM 표면적 반비례).  우리 *미보유*.
- **r_e (electronic resistivity)** — CAM+CF 전자 전도 저항.  전자 percolation 임계 ε_i≈0.77.
- **Z_low (Warburg, low-frequency diffusion)** — anode+cathode *고상 Li 확산* 임피던스 (<30 Hz).  우리 *미보유* (D_Li 모델 없음).
- **τ_eff² = ε_i^(−α) (Bruggeman, eq 5)** — 유효 tortuosity factor.  σ_i,eff = ε_i/τ_eff²·σ_i,0 (eq 3 = 우리 τ_Laplace,eff 정의).  τ_eff ⊃ 기하 tortuosity + *비-기하*(GB·constriction) 효과.  α_bulk 0.52(≈이상)·α_gb 4.3(≫이상).
- **eps_pore (pore volume fraction)** — (펠릿 − 성분)/펠릿 부피.  SE↓→↑, 압력↑→↓, 작은 CAM→↑ (Roller 응집).
- **Roller's relationship** — 작은 입자가 *비균질 응집* → 큰 입자보다 *더 다공* (powder engineering 경험칙, ref 44,45).  → 작은 CAM → eps_pore↑ → r_i,gb↑.
- **bimodal CAM (NCA-b-12)** — 작은(NCA-4) + 큰(NCA-15) CAM 혼합.  작은 입자가 큰 입자 공극 충전 → eps_pore↓ → r_i,gb↓ + 충분한 A_CAM → r_i/e↓ → **trade-off 돌파**.
- **UP-C / IP-C / IP-P** — uniaxial press-cylindrical / isostatic press-cylindrical / isostatic press-pellet.  ★ **등방가압(fluidic media)이 SE 매끄럽게 densify** (UP-C SUS 평판은 rigid CAM 에 응력 집중).
- **teardrop / collapsed-semicircle / double-peak (Fig S5)** — r_i,gb 와 r_i/e 의 *상대 크기*에 따른 Nyquist 형태 (r_i,gb<r_i/e=teardrop … >=double-peak).  ★ kim2025 의 R_int/R_i 분해 가능성 논리와 동형.

---

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
