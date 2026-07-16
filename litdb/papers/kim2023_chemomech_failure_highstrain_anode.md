# ⭐필독 / 우리-랩 — Chemo-mechanical Failure of Solid Composite Cathodes Accelerated by High-Strain Anodes — Kang & Shin (Energy Storage Materials 2023)

> slug `kim2023_chemomech_failure_highstrain_anode` · DOI `10.1016/j.ensm.2023.103049` · type `exp + FEM (electrochemo-mechanical)` · PDF `Kim_2023_EnergyStorageMater_ChemoMechFailure_HighStrainAnode_main.pdf` (+ `_SI.docx`) · digested `2026-06-26` · status ✅
>
> ## ★★★ 우리 랩(Hanyang, **Jong-Won Lee** 그룹) 자체 논문 — **Kang 2025(ACS AMI)의 ref [27]·자매논문의 *원조*** ★★★
> 저자 = **Junhee Kang, Hong Rim Shin, Jonghyeok Yun, Siwon Kim, Beomsu Kim, Kyeongsu Lee(Next Generation
> Development Team, Samsung SDI), Youngjun Lim(Samsung SDI), Jong-Won Lee\*(Hanyang Univ., Division of
> Materials Science and Engineering)**.  교신 = **jongwonlee@hanyang.ac.kr**.
>
> ⚠ **메타 정정 (사용자 시드 vs PDF):** 사용자 시드는 제1저자를 "J. Kim"으로 추정하고 slug 를
> `kim2023_…`로 지정했으나, **PDF 헤더의 실제 제1저자는 Junhee Kang** (Kang 2025 ACS AMI 와 *같은*
> 제1저자).  파일 slug 는 사용자 지정(`kim2023_…`)을 그대로 유지하되, **실제 인용 시 제1저자 = Kang
> 임을 명기**.  "Siwon Kim, Beomsu Kim" 은 공동저자(3·4번째)로 존재 → "Kim" 시드는 이들과 혼동된 듯.
>
> ## 이 논문의 위상 — **랩의 chemo-mechanical 3부작 중 *anode-driven* 균열 축**
> 같은 그룹·같은 핵심 인력(Junhee Kang, Hong Rim Shin, Jonghyeok Yun, Jong-Won Lee)의 세 논문이
> **같은 NCA·NCM/LPSCl 계면을 세 렌즈**로 본다.  이 2023 ESM 논문이 **시간적 원조**(Kang 2025 가
> 이 논문을 ref [27]로 인용):
> - **이 논문 (Kang 2023, ESM)** = **음극이 양극 균열을 *가속***. driver = **고-strain 음극(Li-In, ±3.8 MPa)
>   의 부피변화 → "dynamic contact" → 계면 불균일 → 확산응력(GPa)·균열**.  비교군 = 제로-strain LTO.
> - **Kang 2025 (ACS AMI)** = **bimodal 패킹의 *역학적 대가*** (큰 입자 균열). driver = **NCA/LPSCl 계면분해
>   → Li 농도·응력 *구배*, 큰 입자(10 µm)일수록 ~10× 심함**.  LZO 코팅으로 toughen.
> - **Kim·Kang·Park·Lee 2025 (Electrochim. Acta)** = 같은 계면의 *kinetics* (modified TLM 으로 R_ct/C_dl/확산 분해).
>
> ★ **두 cracking driver 의 쌍 (사용자 핵심 요청):**  Kang 2025 = **양극 내부 원인**(Li-gradient, 큰 입자).
> 이 논문 = **양극 외부 원인**(음극 strain 이 *밀어넣는* 응력).  **둘 다 같은 결과(NCA 입계 균열·pulverization)
> 를 *다른 origin* 에서** → 우리 fracture 모델이 흡수해야 할 균열 driver 가 *최소 둘*임을 못 박는다.

---

## 1. 한 줄 요약
**고-strain 음극(Li-In, 사이클 중 부피 ±, in-situ 압력 ±3.8 MPa)이 같은 NCA/LPSCl 복합 *양극*의
chemo-mechanical 열화를 *가속*** — 제로-strain LTO 음극(±0.2 MPa)과 *동일 양극*을 비교하면 Li-In 셀은
**~120 사이클 후 급락(200th 에 ~9 mAh/g)**, LTO 셀은 **75.6 % 유지/200 cyc**.  메커니즘 = 음극 부피변화가
양극 구성요소 사이에 **"dynamic contact"(붙었다 떨어졌다 하는 동적 접촉)**을 유발 → SE/NCA 계면 분해
부산물(Li₂Sₙ·P₂Sₓ·PO₄³⁻) 증가 → 계면 불균일(interfacial heterogeneity) → NCA 내 **GPa급 확산-유발 응력**
국소화 → **다결정 NCA 입계 균열·pulverization**.  2D electrochemo-mechanical FEM 으로 음극 팽창압
σ_anode + 계면 불균일이 von Mises 응력을 입계에 집중시켜 **intergranular fracture 가 지배 손상모드**임을 확인.

> ★ **우리에게 왜 중요한가 (3줄):** (1) **균열 driver 의 *외부* 축** — Kang 2025 가 *양극 내부*(Li-gradient)면
> 이 논문은 *음극이 양극으로 전달하는 응력*. 우리 DEM 은 *제조 압밀* 접촉응력만 → "음극→양극 사이클 응력 전달"은
> **우리가 *전혀* 안 가진 축**(frame[5] 미보유, future). (2) **"dynamic contact"** = 사이클 중 접촉이 *생겼다
> 사라졌다* 하는 현상 = 우리 정적 DEM 접촉망(coordination Z, coverage)·fracture-aware σ(f_intact)의 *시간변화*
> 버전. (3) **압력 ≠ 균열 주범** 재확인 — in-situ ΔP 는 ±3.8 MPa 로 작지만 그 *부피변화*가 만드는 확산응력은
> GPa → 우리 "stack pressure 가 압밀 porosity 의 주역이지 *사이클 균열*의 주역은 아님"(Kang 2025·Doux) 일관.

## 2. 메타
| 항목 | 값 |
|---|---|
| 저자 | **Junhee Kang**ᵃ, **Hong Rim Shin**ᵇ, Jonghyeok Yunᵃ, Siwon Kimᵃ, Beomsu Kimᵃ, Kyeongsu Leeᶜ, Youngjun Limᶜ, **Jong-Won Lee**\*ᵃ |
| 소속 | ᵃ Hanyang Univ. (Div. Materials Science and Engineering, Seoul) · ᵇ DGIST (Dept. Energy Science and Engineering, Daegu) · ᶜ Next Generation Development Team, **Samsung SDI** (Suwon) |
| 교신 | jongwonlee@hanyang.ac.kr (Jong-Won Lee) |
| 저널/년 | **Energy Storage Materials 63 (2023) 103049** |
| DOI | 10.1016/j.ensm.2023.103049 (Received 2023-08-03; revised 2023-10-23; accepted 2023-11-04; online 2023-11-05) |
| 소재 (CAM/SE/도전제) | **CAM = 다결정 NCA LiNi₀.₈₈Co₀.₀₉Al₀.₀₃O₂** (Samsung SDI) · **SE = LPSCl Li₆PS₅Cl** (Samsung SDI) · 도전제 = Super P carbon |
| 양극 조성 | **NCA : LPSCl : Super P = 72:27:1 wt%** (ball-mill 혼합) |
| **음극 (비교의 핵심)** | **고-strain = Li-In 합금** (In 100 µm/10 mm dia + Li 200 µm/4 mm) · **제로-strain = LTO Li₄Ti₅O₁₂** 복합 (LTO:LPSCl:Super P = 50:40:10 wt%) |
| 셀 | NCA‖LPSCl‖(Li-In 또는 LTO) 풀셀; PEEK 몰드 0.5 mm dia, SUS rod 10 mm; 양극 로딩 12.7 mg cm⁻² |
| 압력 | **제조(fab) 433 MPa** (양극+SE 동일) / **작동(operating) stack 250 MPa** (볼트 조임, 압력센서 모니터) |
| LTO 음극 조건 | 로딩 20.4 mg cm⁻², **N/P 비 = 1.66**, 433 MPa 가압 |
| 사이클 조건 | 30 °C, **2.5–4.3 V vs Li/Li⁺**, 1st 0.05C(CC-CV, CV cutoff 20 %), 이후 0.5C |
| 연구유형 | **실험**(in-situ 압력, EIS-decoupling/TLM, SEM/EDS 단면, XPS, cycling) **+ 2D FEM electrochemical-mechanical 모델**(COMSOL Multiphysics, Voronoi 다결정 NCA + diffusion-induced strain) |

## 3. 핵심 물성 (수치)

> ⚠ 이 논문은 *압밀 porosity*를 직접 측정·보고하지 않는다 (Kang 2025 와 동일).  porosity 칸 n/a — 우리 압밀
> 앵커(Minnmann 14 %, Doux 18 %)와 직접 비교 금지.  정량 앵커 = **in-situ ΔP·EIS R_ion/R_int/R_w·용량유지·E·
> FEM 파라미터**.

| 물성 | 값 | 조건 | stated/digitized | 비고 |
|---|---|---|---|---|
| **E_NCA** | n/a (본문 미명시) | — | — | ★ Kang 2025 는 175 GPa; **이 논문은 NCA 모듈러스 *수치* 미보고**(FEM 은 NCA·LPSCl "175 / 22.1 GPa"를 본문에 명시 — 아래) |
| **E (FEM mechanical moduli)** | **NCA 175 / LPSCl 22.1 GPa** | FEM 입력 (ref [39]) | stated (본문 §2.5) | ★ Kang 2025·Bazzoun 2026·우리 real-bulk 24 와 일치; **이 논문이 175/22.1 의 *원조*(Kang 2025 가 계승)** |
| **NCA volume change** | **5.9 %** (충전 시 수축) | Li deintercalation | stated (§2.5) | Ω(partial molar vol) 유도; **ε_d = Ω/3 × Δc_Li** |
| **in-situ ΔP (Li-In 셀)** | **±3.8 MPa** (충전 팽창/방전 수축) | 250 MPa stack, 0.05C 1st | stated (Fig 1b) | ★ 음극 high-strain 시그니처; NCA 양극은 *반대* 위상(충전 시 수축) |
| **in-situ ΔP (LTO 셀)** | **±0.2 MPa** (미미한 변동) | 250 MPa stack | stated (Fig 1c) | ★ 제로-strain 음극; 본문 "≈4.0 vs 0.2 MPa" — Li-In ≈4.0 / LTO ≈0.2 |
| 1st 방전용량 (0.5C) | **Li-In 셀 152.7 / LTO 셀 152.4 mAh g⁻¹** | 30 °C | stated | ★ 초기엔 *동일*(차이 무의미) → 차이는 *사이클*에서만 발생 |
| **용량유지 (Li-In 셀)** | **82.5 %** @100 cyc; **200th 에 ~9 mAh g⁻¹** (급락) | 0.5C | stated (Fig 1e) | ★ >120 cyc 급격 붕괴 |
| **용량유지 (LTO 셀)** | **75.6 %** @200 cyc; **CE 99.97 %** | 0.5C | stated (Fig 1g) | ★ 200 cyc 안정 cyclability |
| **R_ion (Li-In, TLM)** | **27.8 → 37.2 Ω·cm²** (cyc 1→200) | EIS-decoupling | stated (Table S3) | ★ 거의 불변 — 이온망 멀쩡 |
| **R_int (Li-In, TLM)** | **28.8 → 170.4 Ω·cm²** (cyc 1→200, 5.9×) | EIS-decoupling | stated (Table S3) | ★ 계면저항 급등; 100→150 cyc 에서 65.2→115.7 급변 |
| **R_w (Li-In, Warburg)** | **21.6 → 174.5 Ω·cm²** (cyc 1→200, 8.1×) | EIS-decoupling | stated (Table S3) | ★ 확산저항 급등; 100→150 에서 24.4→128.6 급변(균열) |
| R_ion (LTO, TLM) | **28.8 → 38.1 Ω·cm²** (1→200) | EIS | stated (Table S3) | 완만 |
| R_int (LTO, TLM) | **8.7 → 74.0 Ω·cm²** (1→200) | EIS | stated (Table S3) | 완만(LTO/LPSCl 계면 안정화) |
| R_w (LTO, Warburg) | **13.1 → 29.7 Ω·cm²** (1→200) | EIS | stated (Table S3) | 완만 |
| **R_Ohmic (Li-In vs LTO)** | **Li-In ~34→45 / LTO ~3200→4232 Ω·cm²** | 1→200 cyc | stated (Table S3) | ★ LTO 가 R_Ohmic 100× 큼(낮은 전위 SE 분해층?) — 그러나 *변화 추세*는 둘 다 완만 → SE층은 열화 주역 아님 |
| **σ_Mises (FEM)** | 입계에서 더 빠르게 증가 (값 미명시) | SOC charging, σ_anode 인가 | stated (Fig 6 정성) | ★ 음극압↑ → 입계 von Mises 응력↑ → 소성/균열 |
| **확산-유발 응력 스케일** | **GPa급** | NCA 내부 | stated (Discussion) | ★ stack pressure(수백 MPa) ≪ 확산응력(GPa) |
| LPSCl PSD | n/a (구형, SEM/XRD 확인) | — | Fig S3/S4 | argyrodite 구조 |
| NCA / LTO PSD | **2차입자 ~10 µm** (1차입자 nm 응집) | SEM | stated (Fig S1) | NCA·LTO 둘 다 ~10 µm |
| Heckel / P_y / porosity | n/a | — | — | 압밀곡선·porosity 미보고 |

### Table S3 — 양극 EIS (Z-type TLM) 사이클별 피팅 [SI verbatim] ★핵심 degradation 시그니처
| Cell | Cycle | R_Ohmic (Ω·cm²) | **R_ion** | **R_int** | **R_w** | CPE_int C (µF sᵑ⁻¹cm⁻²) | η |
|---|---|---|---|---|---|---|---|
| **Li-In** | 1 | 34.0 | **27.8** | **28.8** | **21.6** | 152.7 | 0.50 |
| | 50 | 40.8 | 33.4 | 52.0 | 21.8 | 61.8 | 0.62 |
| | 100 | 46.0 | 37.6 | 65.2 | 24.4 | 50.9 | 0.64 |
| | 150 | 43.3 | 35.4 | **115.7** | **128.6** | 34.5 | 0.65 |
| | 200 | 45.4 | **37.2** | **170.4** | **174.5** | 26.4 | 0.65 |
| **LTO** | 1 | 3199.5 | 28.8 | 8.7 | 13.1 | 55.5 | 0.70 |
| | 50 | 3681.9 | 33.1 | 39.0 | 20.4 | 66.4 | 0.68 |
| | 100 | 3694.7 | 33.3 | 52.8 | 21.8 | 61.8 | 0.68 |
| | 150 | 3958.2 | 35.6 | 72.6 | 25.6 | 61.8 | 0.69 |
| | 200 | 4232.1 | **38.1** | **74.0** | **29.7** | 56.4 | 0.70 |
> ★ **읽는 법:** Li-In 셀에서 **R_ion 은 27.8→37.2 로 *거의 불변*(이온 전송망은 멀쩡)**, **R_int(계면) 28.8→170.4
> = 5.9×, R_w(확산) 21.6→174.5 = 8.1× 가 100→150 사이클에서 *급등***(R_int 65→116, R_w 24→129) — **이것이
> ~120 cyc 용량 급락(Fig 1e)의 직접 원인**.  LTO 셀은 같은 저항들이 *완만*하게만 증가(R_int 8.7→74, R_w 13→30).
> CPE_int C 가 Li-In 에서 152.7→26.4 로 *감소*(η 0.50→0.65) = 계면 활성면적 축소 + 비이상성 증가(균열·접촉손실).
> R_Ohmic 은 Li-In(34→45) vs LTO(3200→4232) — LTO 가 100× 크나 *둘 다 추세 완만* → **SE 분리막층은 열화 주역
> 아님**(본문 Fig S10 으로 ohmic 불변 확인 → 열화는 *양극 계면/확산*에서).

### 음극 EIS (Fig S8) — 음극은 열화 주범 아님
| 음극 | 200 cyc 변화 | 해석 |
|---|---|---|
| Li-In | **거의 불변**(3-전극, Fig S8a) | Li-In 자체 계면은 안정 — *전달하는 응력*이 문제이지 음극 *자체* 열화 아님 |
| LTO | 50 cyc 후 반원 약간↑ 후 **빠르게 안정화** | LTO/LPSCl 계면이 큰 접촉면적으로 재배열·안정화 |
> ★ 3-전극(lithiated Ag wire 기준전극, Fig S6) 구성으로 *음극*과 *양극*을 분리 측정 → **음극 임피던스는
> 200 cyc 동안 변화 거의 없음** → Fig 1e 의 급락은 *음극 자체*가 아니라 *양극*에서 발생.  대칭셀
> [Li-In|LPSCl|Li-In] (Fig S9, 0.9 mA cm⁻², 1.8 mAh cm⁻²) 도 600 h(150 cyc) 안정 cycling → **Li-In/LPSCl
> 계면 자체는 안정**, 문제는 *부피변화가 양극에 전달하는 동적 응력*.

### Table S1 — FEM electrochemical 모델 파라미터 [SI verbatim] ★우리 MPM/FEM 이 미러할 값
| Parameter [unit] | value | 비고 |
|---|---|---|
| Cell dimension [L×W, µm] | **815 × 100** | (셀 스케일; 양극 균열 해석 도메인 = **12.5 µm** — 본문 §2.5) |
| Temperature [K] | 298.15 | |
| Reference exchange current density [A m⁻²] | **10** | i₀ (Butler-Volmer) |
| Reference concentration [mol m⁻³] | **48000** [S3] | c_max (Li in NCA) — ref [S3] Nitta 2015 |
| Radius of active material [µm] | **5** | (대표 단일 반경; 본문은 다결정 2차입자 ~10 µm) |
| Max / Min cell voltage [V] | 4.3 / 2.5 | |
| C-rate | **0.33** | (FEM 충전) |
| Electrical conductivity of AM [S m⁻¹] | **1** [S4] | σ_e(NCA) FEM 입력 — ref [S4] Amin 2015 |
| Diffusion coefficient of Li in AM [m² s⁻¹] | **3 × 10⁻¹⁴** [S4] | D_Li(NCA) |
| Electrolyte conductivity [S m⁻¹] | **0.02** [S5] | σ_ion(LPSCl) = **0.2 mS/cm** (FEM 입력) — ref [S5] Park 2022 |
> ★ **Kang 2025 Table S4 와 거의 동일**(i₀=10, c_max=48000, σ_e=1, D=3e-14, σ_ion=0.02) — Kang 2025 가
> 이 논문의 FEM 을 *계승·확장*(Kang 2025 는 여기에 cohesive-zone CZM·E_NCA=175 명시·LZO 케이스 추가).
> **이 논문의 FEM 은 *cohesive-zone 균열*이 아니라 *응력장 예측*(σ_anode 인가 → von Mises 분포)**에 집중.

### Table S2 — FEM 경계조건 [SI verbatim]
| 경계 | Mass conservation | Charge conservation | Solid mechanics |
|---|---|---|---|
| Boundary 1 | n·∇c = 0 | n·∇φ_e=0, n·∇φ_s=i_total, φ_s=0 | **n·σ_yy = −P_app** (가압) |
| Boundary 2 | — | n·∇φ_e = 0 | n·u = 0 (고정) |
| Boundary 3 | (Boundary 2 와 동일) | | |
| Boundary 4 | — | n·∇φ_e=0, n·∇φ_s=i_total | — |
| Boundary 5 | — | −n·∇φ_s = 0 | — |
| 전해질-AM 계면 | **−n·D∇c = i_loc/(aF)** | — | — |
> ★ **Boundary 1 에 n·σ_yy = −P_app** = 음극 부피변화를 *y축 외부 압력*으로 인가 (본문 §2.5: "anode volume
> change was expressed as a constant external pressure in the y-axis direction" = **z-축 변위로도 표현** — 본문은
> "z-axis displacement of the anode-solid electrolyte interfacial boundary").  우리 MPM wallP/servo 의 FEM 버전.
> 전해질-AM 계면 flux = i_loc/aF (Butler-Volmer 전류 → Li flux).  **계면 불균일 표현 = inactive boundary 에서
> reference exchange current density 를 *낮춤*** (= 분해층이 덮인 영역은 반응 억제).

## 4. 시뮬레이션 방법 ★ — 2D FEM electrochemical-mechanical (우리 MPM/DEM 이 mirror할 모델)

> ★ 이 절이 우리 모델링과 가장 직접 대응.  **하중이 *음극 부피변화(σ_anode)*** — Kang 2025 의 *cycling*
> 하중과 같은 시간축이나, **여기선 *음극*이 양극에 압력을 *인가*** 하는 것이 핵심 차이.  Supplementary Note 2 + Tables S1/S2.

- **code**: **COMSOL Multiphysics** (본문 §2.5 명시 — Kang 2025 는 미명시였으나 이 *원조* 논문이 COMSOL 을 명시).
  2D electrochemical 모델 + mechanics 모듈 결합.
- **기하 / 입자 처리** ★:
  - **다결정 NCA 를 Voronoi tessellation 으로 생성** (2차입자 = 1차입자 다결정 집합).  **2차입자 ~10 µm**
    가정.  양극 도메인 = **12.5 µm (x–y 방향)** — 양극 내 NCA·LPSCl 부피분율 고려한 크기.
  - ⇒ **진짜 SHAPE 변형 아님 — *Voronoi 다결정 입자* 안에서 확산-유발 strain(ε_d)으로 응력장 계산.**
    Kang 2025 와 달리 **이 논문의 본문 FEM 은 명시적 cohesive-zone damage scalar 를 *주 결과로 강조하지 않고*,
    *σ_anode + 계면 불균일 → 입계 von Mises 응력 집중* 의 *경향*에 집중**(Fig 6).  ("intergranular fracture 가
    dominant damage mode" 는 von Mises 응력이 *입계*에서 더 빠르게 증가함으로 *추론*).
  - NCA 입자는 *완전 리튬화(방전) 상태*에서 시작, 부피 전체 균일 Li 농도 가정.
- **지배방정식 (Supplementary Note 2)**:
  - **Butler-Volmer** 국소전류: `i_loc = −i₀[exp(α_a Fη/RT) − exp(−(1−α_a)Fη/RT)]` (NCA/LPSCl 계면).
  - **Fick 확산** (고상 Li): `∂c/∂t − D∇²c = 0`.
  - **선형탄성**: `ε_ij^e = (1/E)[(1+ν)σ_ij − νσ_kk δ_ij]`.
  - **전변형 = 탄성 + 확산유발**: `ε_ij = ε_ij^e + ε_ij^d = (1/E)[(1+ν)σ_ij − νσ_kk δ_ij] + (Ω/3)Δc`
    — ★ **확산유발 변형 ε_d = (Ω/3)·Δc**, **Ω = NCA 5.9 % 부피변화에서 유도한 partial molar volume**.
    (Kang 2025 와 동일한 핵심 구성식 — 이 논문이 원조.)
- **계면 불균일(interfacial heterogeneity) 표현** ★:
  - NCA 입자의 **inactive boundary 에서 reference exchange current density(i₀)를 *감소***시켜 비활성 계면
    (분해층이 덮인 영역)을 표현 → **불균일한 Li⁺ flux** → 국소 c_Li 구배 → 국소 ε_d → 국소 응력 집중.
  - = **"dynamic contact"의 결과**(동적 접촉이 만든 계면 분해 부산물이 i₀ 를 깎음)를 FEM 경계조건으로 인코딩.
- **음극압 σ_anode 인가**: 양극 도메인 Boundary 1 에 `n·σ_yy = −P_app`(또는 z-축 변위)로 음극 팽창압 인가.
  **다양한 SOC 에서 측정한 σ_anode 값 시리즈**로 numerical test → 음극 팽창이 NCA 입자 응력에 미치는 영향 분리.
- **MPM/DPC/cap / cohesive CZM**: 본문 주결과로는 없음 (Kang 2025 가 cohesive-zone CZM·damage scalar 를 *추가*).
  이 논문은 **응력장(σ_Mises) + Li 분포(c_Li)** 까지 — 균열은 그 응력 집중으로 *해석*.
- **전달 솔버 / RNM**: 없음 (전달은 *실험 EIS-decoupling/TLM*; FEM 은 σ_ion=0.02 S/m·σ_e=1 S/m 을 *입력*만,
  σ_eff 를 풀지 않음).  ⇒ **transport σ 를 시뮬로 안 뽑음** — 우리 Kirchhoff/Holm σ 삼중항이 그 칸(frame[5]).
- **특이사항**: **stack pressure(수백 MPa) ≪ 확산-유발 응력(GPa)** → 균열 주범은 *압력*이 아니라 *음극이 유발한
  동적접촉 → 계면 불균일 → 국소 GPa 확산응력* (본문 Discussion 명시).

## 5. Figure set ★ (모든 그림 + 우리가 쓸 점)

| Fig | 내용 (무엇을 보여주나) | 핵심 수치 | 우리가 참고할 점 |
|---|---|---|---|
| **1a** | in-situ 압력측정 셀 모식 (압력센서 양극\|SE\|음극 스택 위) | 250 MPa stack | ★ in-situ ΔP 측정 셋업 |
| **1b** | Li-In 셀 ΔP + 전압프로파일 (충방전) | **ΔP ±3.8 MPa** | ★ 고-strain 음극: 충전 팽창/방전 수축; NCA 는 *반대* 위상 |
| **1c** | LTO 셀 ΔP + 전압프로파일 | **ΔP ±0.2 MPa** | ★ 제로-strain 음극: 거의 평평 |
| **1d** | Li-In 셀 전압-용량 곡선 (1st→200th, 0.05→0.5C) | — | 200th 에서 심한 저하·곡선 붕괴 |
| **1e** | **Li-In 셀 용량·CE vs cycle** | **82.5 %@100; ~9 mAh/g@200th** (>120 cyc 급락) | ★ 핵심 결과: 급격 붕괴 |
| **1f** | LTO 셀 전압-용량 곡선 (1st→200th) | — | 200th 까지 안정 유지 |
| **1g** | **LTO 셀 용량·CE vs cycle** | **75.6 %@200; CE 99.97 %** | ★ 제로-strain 음극 = 안정 cyclability |
| **2a** | Li-In 양극 Nyquist (50씩, pre→200) | — | 반원 급성장 |
| **2b** | LTO 양극 Nyquist (50씩) | — | 반원 완만 성장 |
| **2c** | **등가회로 (Z-type TLM)** | r_ion–(cpe_int‖(r_int+Z_w))–r_ele | ★ SE/AM/계면 분포저항 분해 회로 |
| **2d** | **R_ion vs cycle** (Li-In vs LTO) | **둘 다 거의 불변(~28→38)** | ★ 이온망 멀쩡 — 양 셀 공통 |
| **2e** | **R_int vs cycle** | **Li-In 28.8→170.4(급등), LTO 8.7→74(완만)** | ★ 계면열화가 Li-In 에서 압도적 |
| **2f** | **R_w vs cycle** | **Li-In 21.6→174.5(급등, 특히 100→150), LTO 13→30(완만)** | ★ 확산경로 tortuosity↑(균열) |
| **3a** | **Li-In 양극 XPS S2p·P2p** (pre→200 cyc) | Li₂Sₙ 162.7, P₂Sₓ 163.4; PO₄³⁻ **134.1 eV** | ★ 분해 부산물 *대량* 생성(특히 PO₄³⁻) |
| **3b** | LTO 양극 XPS S2p·P2p (pre→200 cyc) | Li₂Sₙ·P₂Sₓ *소량* | ★ LTO 셀은 분해 훨씬 적음 |
| **4a** | **pristine NCA 양극 단면 SEM** | 8 µm/4 µm scale; NCA 무손상 | ★ 출발점 (균열 없음) |
| **4b** | **Li-In 셀 NCA 양극 단면 (150 cyc)** | **다결정 NCA 심한 균열·pulverization** | ★ 큰 NCA 입자 입계 균열 |
| **4c** | **Li-In 셀 NCA 균열 입자 갤러리 (6종)** | "various types of cracked NCA particles" | ★ 다양한 균열 패턴 |
| **4d** | **LTO 셀 NCA 양극 단면 (200 cyc)** | **NCA 거의 무손상** | ★ 제로-strain 음극 → NCA 건전 |
| **5** | **chemo-mechanical 열화 메커니즘 모식** | dynamic contact→불균일→Li flux→GPa응력→입계균열→새표면→불균일↑(악순환) | ★ 전체 스토리 한 장 (detrimental cycle) |
| **6** | **FEM σ_Mises (입자, σ_anode 인가)** | 입계에서 von Mises 더 빠르게 증가 | ★ intergranular fracture = dominant mode |
| **S1** | NCA·LTO SEM | **둘 다 2차입자 ~10 µm**(nm 1차 응집) | 입경 |
| **S2** | NCA·LTO XRD | NCA = R-3m 층상 / LTO = Fd-3m 스피넬 | 상 확인 |
| **S3** | LPSCl SEM/EDS | 구형 | SE 형상 |
| **S4** | LPSCl XRD | argyrodite | SE 상 |
| **S5** | FEM 기하 (양극 도메인) | 12.5 µm | 모델 도메인 |
| **S6** | 3-전극 ASSB 모식 | lithiated Ag wire 기준전극 | ★ 음극/양극 분리측정 |
| **S7** | Li-In·LTO 풀셀 AC-임피던스 | — | 전체 셀 EIS |
| **S8** | **음극 AC-임피던스 (Li-In·LTO)** | **둘 다 거의 변화 없음** | ★ 음극 *자체*는 안정 — 열화는 양극 |
| **S9** | **대칭셀 [Li-In\|LPSCl\|Li-In] cycling** | **0.9 mA cm⁻², 1.8 mAh cm⁻², 600 h(150 cyc) 안정** | ★ Li-In/LPSCl 계면 자체 안정 |
| **S10** | **Ohmic 저항 vs cycle (Li-In·LTO)** | 둘 다 완만 | ★ SE층 열화는 주역 아님 |
| **S11** | 양극 AC-임피던스 (pre-conditioning 전, Li-In·LTO) | 비슷 | 초기엔 둘 다 동일 |
| **S12** | **XPS S2p·P2p (pre-conditioning 전)** | LPSCl 분해 *없음* | ★ pre-cond 전엔 무분해 → 분해는 *사이클*에서 |
| **S13** | **재가압(250 MPa, 150 cyc 후) 후 방전용량** | **25.2 → 38.3 mAh g⁻¹** (일부 회복) | ★ 접촉손실 일부 회복하나 불완전 |
| **S14** | 재가압 전후 양극 임피던스 (R_int·R_w) | R_int 약간↓ | ★ 재가압이 접촉 일부 복구 |
| **S15** | **제조 직후 양극 단면 SEM** | **NCA 무손상(균열 없음)** | ★ 433 MPa 제조는 균열 안 만듦 |
| **S16** | **충전 시 Li 농도분포 (FEM)** | 불균일 c_Li | ★ 계면 불균일 → Li flux 불균일 |
| **S17** | **다른 stack pressure 에서 Li-In 셀 cycling** | **100 MPa 작동 → 300 cyc 안정** | ★ *낮은* 작동압 → 더 안정(아래 §10 nuance) |

## 6. Post-processing ★

- **무엇**:
  - **in-situ 압력 측정**: 압력센서(Bongshin 로드셀, 분해능 0.01 MPa)를 양극\|SE\|음극 스택 위에 배치
    → 충방전 중 ΔP 실시간 모니터.  음극 부피변화(팽창/수축)와 양극 부피변화(NCA 충전 시 수축)가 *반대 위상*.
  - **EIS-decoupling (Z-type TLM 피팅)**: 양극 복합층의 분포형 저항을 **R_ion(이온전송)·R_int(NCA/SE 계면)·
    R_w(NCA 내 고상확산 Warburg)·R_ele(전자전송)** 로 분해.  3-전극(lithiated Ag) → 음극·양극 분리.
    회로(Fig 2c) = `r_ion(전송선) — (cpe_int ‖ (r_int + Z_w))` + 양 끝 r_ele/SE.  CPE_int(C, η) 동반.
  - **FEM 후처리**: c_Li 분포(Fig S16)·σ_Mises 분포(Fig 6)·다양한 SOC 의 σ_anode 인가 numerical test.
  - **XPS 디컨볼루션** (S2p / P2p): PS₄³⁻ 본 피크 + 산화분해 부산물 **Li₂Sₙ(~162.7 eV, n>1)·P₂Sₓ(~163.4, x>5)·
    PO₄³⁻(134.1 eV)** 정량 → Li-In vs LTO 비교로 *고-strain 음극이 분해를 가속*함을 입증.
    - P₂Sₓ = 황 원자 *bridging*(S–…–S 사슬) → 산화 시 결합에너지 양의 시프트.  PO₄³⁻ = 전해질 산화분해.
  - **단면 SEM** (Ar ion polishing, ArBlade5000): pristine / 150 cyc(Li-In) / 200 cyc(LTO) NCA 입자 균열 비교.
- **도구**: Biologic SP-300(EIS, 7 MHz–10 mHz, 5 mV AC); ESCALAB 250Xi(XPS, mono Al Kα 1486.6 eV);
  Hitachi S-4800(SEM/EDS); Hitachi ArBlade5000(cross-section Ar polishing); Miniflex 600(XRD, Cu Kα 1.541 Å);
  Bongshin 로드셀(in-situ 압력, 0.01 MPa); COMSOL Multiphysics(FEM).
- **수치화·기록**: 사이클(1/50/100/150/200)별 R_Ohmic/R_ion/R_int/R_w + CPE(C, η) (Table S3); in-situ ΔP 곡선;
  XPS 결합에너지 피크; 단면 SEM 균열 갤러리.

## 7. 우리 DEM+MPM 대비  →  `our_dem_baseline.md`

> ★ 사용자 핵심 요청 절.  이 논문은 **(1) 우리 Auerbach/fracture-aware σ(cathode cracking)**, **(2) Kang 2025
> 자매(같은 그룹, 다른 균열 origin)**, **(3) operating-vs-fab 압력(Doux/Lee2025)** 에 직접 연결되며, **anode→cathode
> 사이클 chemo-mechanics 는 우리 *구조* DEM+MPM 이 *전혀* 안 다루는 future 축**임을 분명히 한다.

| 항목 | 이 논문(Kang 2023, ESM) | 우리 | 차이 / 이유 |
|---|---|---|---|
| **균열 driver** | **음극 strain → "dynamic contact" → 계면 불균일 → GPa 확산응력 → NCA 입계균열** | **압밀 접촉응력(Auerbach), fracture-aware σ(f_intact, frac_severe)** | ★ **driver 가 *외부·사이클*(음극 부피변화)** — 우리 DEM 은 *제조 압밀* 시점 균열만 → **anode-coupled cycling 균열은 우리 미보유**(frame[5] future) |
| **vs Kang 2025 균열 driver** | **음극(외부)이 미는 응력** | (Kang 2025 = **양극 내부 Li-gradient, 큰 입자**) | ★ **두 cracking driver 의 쌍**: Kang 2023=*외부 음극* / Kang 2025=*내부 Li구배* → 우리 fracture 모델은 *최소 2 origin* 흡수 필요 |
| **CAM 소재·E** | **NCA Ni₀.₈₈** (FEM E=175 GPa) | NMC811, E=140 GPa | ★ 다른 CAM·다른 E (Kang 2025 와 동일 이슈; §8 A1) |
| **SE E** | LPSCl **22.1 GPa** (FEM) | E_eff 1.35(연화)/MPM 1.53 / real 24 | ★ **22.1 = 우리 real-bulk 24 ≈ Bazzoun 22.1** — E_SE 앵커 *원조*; 우리 1.35 는 압밀-프록시 |
| **NCA 부피변화** | **5.9 %** (사이클) | (우리는 압밀만, 사이클 부피변화 미모델) | ★ 우리 미보유 — 사이클 chemo-mechanics 는 그들 FEM 영역 |
| **하중축** | **사이클(음극 부피변화 σ_anode 가 양극에 인가)** | **압밀(제조 press 300 MPa)** | ★ *다른 하중*: 그들=음극→양극 동적응력 / 우리=제조 압밀 — frame[5] *시간축* 분업 |
| **"dynamic contact"** | **사이클 중 접촉 생성/소멸(동적)** | **정적 접촉망**(coordination Z, coverage Hertz/Tabor) | ★ 우리는 *한 시점* 접촉; 그들 = *시간변화* 접촉 → 우리 f_intact·Z 의 *사이클 동역학* 버전(미보유) |
| **역학모델** | 2D FEM, Voronoi 다결정 + diffusion-induced ε_d(σ_anode 인가) | 3D/2D MPM, J2 연속체 소성 *형상* 흐름 | ★ 둘 다 연속체; 그들 = *확산-유발 응력*(전기화학 결합) ↔ 우리 = *압밀 소성*(순역학) |
| **transport σ** | **시뮬 미산출**(σ는 실험 EIS-TLM만; FEM 은 σ_ion/σ_e *입력*) | **Kirchhoff/Holm σ_ionic+σ_e+σ_thermal 삼중항** | ★ 우리 σ-솔버가 그들 빈 칸(frame[5] 전달 절반) |
| **계면저항 분해** | **EIS-TLM R_ion(불변)/R_int·R_w(급등)** 사이클 시계열 | σ_ionic 폼 + ASR_ionic (정적) | ★ 그들 *사이클 열화 시그니처* — 우리는 정적; 흡수 가치(§8 ④) |
| **압력 분리** | **fab 433 / operating 250 MPa** 명시; **압력은 *사이클 균열* 주범 아님(GPa 확산응력이 주범)** | fab 300(Heckel P_y 138) ≠ operating 수~수십 MPa | ★ 같은 *제조≠작동* 인식(Doux/Lee2025); 단 "압력 균열기여 미미"는 *사이클* 맥락 한정 |
| **재가압 회복** | **250 MPa 재가압(150 cyc 후) → 용량 25.2→38.3 회복(불완전)** | (우리 압밀은 1회) | ★ 사이클 중 접촉손실 → 재가압으로 *일부*만 회복 = *비가역* 손상(균열) 존재 증거 |
| **압력-사이클 trade** | **100 MPa 작동 → 300 cyc 안정** (Fig S17) | (우리 operating 압력축 미보유) | ★ *낮은* 작동압이 *더* 안정 — Doux(5 MPa 최적) 와 합류, 단 메커니즘 다름(여기선 음극 strain 완화) |

## 8. 적용 인사이트 (내 연구에 어떻게) — ★ 우리 랩 trend 정렬

- ① **균열 driver 의 *2-origin* 골격을 우리 fracture 모델에 명문화 (강링크, Kang 2025 와 쌍)**:
  랩의 두 논문이 NCA 입계 균열의 **서로 다른 두 origin** 을 못 박았다 — **Kang 2025 = 양극 *내부* Li-gradient
  (큰 입자 ~10× 심함)**, **이 논문(Kang 2023) = *외부* 음극 strain → dynamic contact → 계면 불균일**.  우리
  DEM Auerbach/fracture-aware σ(f_intact, frac_severe)는 *압밀 접촉응력* 단일 origin 만 → **(a) "큰 입자 더 깨짐"
  (Kang 2025) 은 압밀-접촉응력 ∝ 입경 으로 흡수**, **(b) "음극 strain 유발 균열"(이 논문)은 우리 구조모델이
  *못 다루는 future 축*(사이클)으로 명시** → frame[5] 의 *시간축* 미보유 칸을 분명히.  → `comparison_vs_ours.md`
  C(mechanics) + F(미보유) 축에 "anode-coupled cycling cracking" 신규 항목.

- ② **"dynamic contact" ↔ 우리 정적 접촉망의 *사이클 동역학* 버전 (방법론 신규축)**:
  이 논문의 핵심 신개념 = **사이클 중 접촉이 *생성/소멸*(dynamic)** — 음극 팽창 시 양극 구성요소가 밀착했다가
  수축 시 떨어짐.  우리 DEM coordination Z·coverage(Hertz/Tabor)·f_intact 는 *한 시점*(제조 후) 정적.
  → **사이클당 ΔZ / Δcoverage(접촉 생성·소멸 빈도)** 를 *미래* 동적 지표로 기록; 우리 fracture-aware Holm
  (broken contacts retain ~60 %)의 *사이클 누적* 버전과 연결.  ⚠ 우리 DEM 은 *압밀 1회* — 이건 명백히
  frame[5] 미보유(사이클 시뮬 필요)임을 분명히.

- ③ **E_SE=22.1 GPa 앵커의 *원조* 확정 + NCA E=175 옵션 (A1, Kang 2025 와 동일 권고)**:
  이 논문이 **NCA 175 / LPSCl 22.1 GPa** 의 *최초 출처*(2023) → Kang 2025·Bazzoun 2026 이 계승.  우리 real-bulk
  24·E_eff 1.35/1.53 의 SE-모듈러스 baseline 을 *세 논문(이 논문·Kang 2025·Bazzoun) 모두 22.1* 로 교차확인.
  → `our_dem_baseline.md §0` 에 **"E_LPSCl 22.1 GPa 출처 = Kang 2023 ESM(원조)·Kang 2025·Bazzoun 2026 일치"**
  주석; CAM 을 NCA(E=175)로 확장하는 A1 권고는 Kang 2025 와 동일(σ_e·D_Li 재보정 필요).

- ④ **EIS-TLM 사이클 시그니처(R_ion 불변 / R_int·R_w 급등)를 우리 σ 예측의 *열화 축*으로 (B6-인접, Kang 2025 와 동일 패턴)**:
  **R_ion 27.8→37.2(불변) + R_int 28.8→170.4(5.9×)·R_w 21.6→174.5(8.1×, 특히 100→150 cyc 급변)** = 균열의
  명확한 시그니처 — **Kang 2025 의 R_ion 불변/R_int·R_w 급등과 *동일 패턴*** (두 논문 교차확인).  우리는 *정적*
  σ만 → "R_ion stable / R_int+R_w rising"을 *예측 가능한 열화 패턴*으로 추가(균열 → NCA 내 확산경로 tortuosity↑
  → R_w↑; 계면 분해 → R_int↑).  → backlog B6 에 *사이클-Warburg* 축(Kang 2023+2025 공통 앵커).

- ⑤ **음극이 *양극* 응력의 *경계조건* — 우리 wallP/servo 의 전기화학 결합 버전 (방법 흡수 후보)**:
  그들 FEM 의 **Boundary 1: n·σ_yy = −P_app (음극 부피변화 = 외부압)** = 우리 MPM wallP/servo 와 *같은 발상의
  전기화학-결합 FEM*.  우리 MPM 은 *제조 압밀* wallP 만 — **음극 strain 을 *시간변화 P_app(t)* 로 인가**하면
  사이클 중 양극 응력장을 우리 MPM 으로도 근사 가능(단 확산-유발 ε_d 결합 필요 = 현재 미보유).  → 우리 MPM
  문서에 "P_app(t) = 음극 strain 곡선(in-situ ΔP ±3.8 MPa) 인가" 를 *future* electrochemo-mechanical 확장으로 기록.

- ⑥ **그들 FEM ↔ 우리 MPM 패럴렐 + Kang 2025 cohesive 와의 *진화* (방법론)**:
  **Kang 2023(이 논문) = 응력장(σ_Mises) + Li 분포까지** → **Kang 2025 = 거기에 cohesive-zone damage scalar
  D(0→1) 추가**.  우리 MPM 누적 소성변형 Σdg 는 *연성* 손상; 그들 cohesive 는 *취성* 입계 박리.  → 우리 MPM
  문서에 "랩 FEM 진화: 2023 응력장 → 2025 cohesive damage; 우리 MPM = *압밀* 소성 J2(상보)" 명문화 → frame[5] 확장.

## 9. 인용 가능 문장 (deck/paper용)

- "Our group's earlier work (Kang, Shin et al., *Energy Storage Mater.* 2023, the reference [27] of our
  2025 study) established that a **high-strain Li-In anode mechanically accelerates the chemo-mechanical
  failure of the NCA/LPSCl composite cathode**: against a zero-strain LTO anode in an otherwise identical
  cell, the Li-In cell (in-situ pressure swing ±3.8 MPa vs ±0.2 MPa for LTO) collapsed to ~9 mAh g⁻¹ by
  the 200th cycle while the LTO cell retained 75.6 % over 200 cycles."
- "The anode-induced degradation proceeds through **'dynamic contacts'** — repeated make-and-break of
  contacts among the cathode constituents driven by the anode's breathing — which roughen the NCA/LPSCl
  interface, increase parasitic decomposition (Li₂Sₙ, P₂Sₓ, PO₄³⁻ by XPS), and localize GPa-level
  diffusion-induced stress at the polycrystalline NCA grain boundaries, causing intergranular cracking and
  pulverization (impedance signature: R_ion flat 27.8→37.2 Ω·cm² while R_int 28.8→170.4 and Warburg R_w
  21.6→174.5 surge over cycles 100→200)."
- "Together with our group's 2025 bimodal study, these two papers pin **two distinct drivers of the same
  NCA grain-boundary cracking** — an *internal* one (Li-concentration/stress gradient, worst in large
  particles; Kang 2025) and an *external* one (anode-strain-induced dynamic contacts; Kang 2023) — both of
  which a complete fracture model of the composite cathode must capture."
- "The 2D electrochemo-mechanical FEM (COMSOL, Voronoi-tessellated polycrystalline NCA, ε_d = Ω/3·Δc with
  Ω from the 5.9 % NCA volume change, the anode expansion imposed as a y-axis boundary stress n·σ_yy =
  −P_app) shows that the **diffusion-induced stress (GPa) dominates the few-hundred-MPa stack-pressure
  stress** — so the cycling-fracture driver is the anode-coupled interfacial heterogeneity, not the applied
  pressure (E_LPSCl = 22.1 GPa, the origin of the value reused in Kang 2025 and Bazzoun 2026)."

## 10. 주의/한계 (over-claim 방지)

- **압밀 porosity 미보고** → 이 논문은 *압밀 porosity/밀도*를 직접 측정·보고하지 않는다(Kang 2025 와 동일).
  우리 압밀 앵커(Minnmann 14 %, Doux 18 %, 우리 DEM 15.6 %)와 **직접 비교 금지** — 정량 앵커는 *in-situ ΔP·
  EIS 저항·용량·E·FEM 파라미터*.
- **하중축이 *사이클(음극 strain)* — 우리 *압밀*과 다름** → 그들 응력·균열은 *음극 부피변화가 양극에 전달하는
  동적 응력 + 확산-유발 응력*이 하중.  우리 DEM/MPM 압밀-응력과 *같은 현상 아님*.  "음극→양극 균열"은 우리 구조
  모델이 *전혀* 안 다루는 future 축 — 흡수 시 frame[5] 미보유로 분명히.
- **CAM 이 NCA(≠NMC811)** → FEM E=175(우리 140), σ_e=1 S/m·D=3e-14 도 NCM811 과 다름.  NMC811 결과를 NCA 에
  *절대값* 전이 금지 — E·σ_e 재보정 후 *추세*만.
- **transport σ 는 시뮬 아님** → σ_eff,ion/σ_e 를 *풀지 않는다*(실험 EIS-TLM + FEM σ 입력만).  R_ion/R_int/R_w
  는 *측정값*이지 *예측 솔버* 산출 아님 → 우리 Kirchhoff/Holm σ 와 *방법이 다름*.
- **이 논문 FEM 의 본문 주결과 = 응력장(σ_Mises) — 명시적 cohesive-zone damage scalar 는 Kang 2025 가 *추가*** →
  이 논문은 "von Mises 응력이 입계에서 더 빨리 증가 → intergranular fracture 가 dominant" 로 *추론*(2025 처럼
  D=0→1 정량 박리값을 주결과로 강조하진 않음).  damage scalar 정량은 *2025* 인용.
- **stack pressure "균열 기여 미미"는 *사이클 균열* 맥락 한정** → 우리 *압밀 porosity/Heckel*에서는 압력이 주역.
  "압력 기여 미미"를 우리 압밀 결론으로 잘못 전이 금지 — 그들 진술은 *cycling 중 균열*에 국한(확산응력 GPa ≫
  stack 수백 MPa).  ★ 추가 nuance: **Fig S17 = 100 MPa 작동압이 300 cyc 안정** — *낮은* 작동압이 음극 strain
  전달을 줄여 *덜* 깨짐(250 MPa 대비). Doux(5 MPa 최적)와 *방향 일치*하나 메커니즘은 *음극 strain 완화*.
- **메타 정정 (slug ≠ 제1저자)**: 파일 slug 는 사용자 지정 `kim2023_…` 이나 **실제 제1저자 = Junhee Kang**
  (Kang 2025 와 동일). 인용 시 "Kang et al. 2023" 로. (Siwon Kim·Beomsu Kim 은 공동저자.)
- **N/P 비 영향 미미 (LTO 셀)** → 본문: LTO 셀의 stress/strain 은 *양극* 용량이 결정하므로 N/P 비(1.66)가
  열화에 영향 무시 가능 (양극 기준 비교 공정성 확보).  ★ Li-In 셀은 N/P 자유(Li 무한공급) → 두 셀 비교는
  *음극 strain* 차이만 분리됨.
- **digitized 구분**: in-situ ΔP "±3.8/±0.2"·"≈4.0/0.2"·Fig 6 σ_Mises 경향·Fig S13 "25.2→38.3" 일부는 *그림에서
  읽거나 본문 근사값*(±, 추세) — Table S3 stated 저항·용량(82.5/75.6 %·CE 99.97 %)과 구분.

## Supplementary Information (.docx — 2026-06-26 추출)
원본 `docs/literature_coverage/pdfs/Kim_2023_EnergyStorageMater_ChemoMechFailure_HighStrainAnode_SI.docx`,
데이터 `docs/data/kim2023_chemomech_failure_highstrain_anode.csv`.
- **Supplementary Note 1** = NCA/LTO/LPSCl 소재 특성(SEM/XRD; 둘 다 ~10 µm 2차입자, NCA=R-3m·LTO=Fd-3m 스피넬·
  LPSCl=argyrodite 구형).
- **Supplementary Note 2** = electrochemical-mechanical 모델링 (Butler-Volmer + Fick + 선형탄성 + ε_d=Ω/3·Δc;
  Table S1 파라미터·Table S2 경계조건; 음극압 = z-축 변위/y-축 응력; inactive boundary 에서 i₀ 감소로 계면 불균일 표현).
- **Table S3** = Li-In·LTO 양극 EIS Z-type TLM 사이클별 피팅(위 §3 표) — *본 digest 의 핵심 정량 시계열*.
- **Refs S1–S5**: Peng 2016(NCA+황화물)·Cheng 2017(LTO)·Nitta 2015(c_ref)·Amin 2015(NCA σ_e·D)·Park 2022(σ_ion).

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
