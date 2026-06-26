# ⭐필독 / 우리-랩 — Toughened Bimodal Cathodes for ASSBs via Controlled Interfacial Heterogeneity — Kang & Shin (ACS Appl. Mater. Interfaces 2025)

> slug `kang2025_toughened_bimodal_nca_lzo` · DOI `10.1021/acsami.5c14519` · type `exp + FEM (electrochemo-mechanical)` · PDF `Kang_2025_ACSAMI_ToughenedBimodalCathodes_LZO_main.pdf` (+ `_SI.pdf`) · digested `2026-06-26` · status ✅
>
> ## ★★★ 우리 랩(Hanyang, **Jong-Won Lee** 그룹) 자체 논문 — 모델이 따라가야 할 실험 trend의 기준점 ★★★
> 저자 = **Junhee Kang, Hong Rim Shin (공동1저), Jonghyeok Yun, Young Jun Lim, Riyul Kim\*(Samsung SDI),
> Jong-Won Lee\*(Hanyang Univ., Division of Materials Science and Engineering / Department of Battery
> Engineering)**.  이 논문이 정하는 실험 방향(소재 = **NCA**, bimodal 패킹의 *역학적 대가*, 큰 입자의
> 크기-의존 균열, LZO 코팅, EIS-TLM 분해, FEM electrochemo-mechanical 모델)에 우리 DEM+MPM이 정렬해야 한다.
> "이 논문을 기반으로 받아야지 우리 실험실 trend를 따라갈 수 있다" — 사용자.

---

## 1. 한 줄 요약
복합 양극에 **bimodal(3+10 µm) NCA**를 쓰면 패킹·전자전도가 좋아지지만(펠릿 0.74→0.68 mm, 부피로딩 1.1×),
**큰 10 µm 입자가 사이클 중 입계 균열(intergranular cracking)**을 일으켜 **용량유지 67.3 %(단봉)→47.7 %(bimodal)
@100 cyc**로 급락한다.  그 균열의 원인은 **NCA/LPSCl 계면 분해(interfacial heterogeneity)가 만든 *공간적으로
불균일한 Li 농도·응력 구배***이며, **입자가 클수록 더 심하다**(c_Li 구배가 10 µm에서 3 µm 대비 ~10×, von
Mises 응력 구배도 큼; cohesive-zone "damage"가 10 µm 다결정 여러 입계에서 1=완전박리).  **결정적 nuance:
가압(작동 stack 200 MPa, 제조 400 MPa)이 만드는 응력(수백 MPa)은 *확산-유발* 응력(최대 GPa)보다 훨씬 작아
균열 기여는 미미** — 균열의 주범은 압력이 아니라 Li-불균일이다.  해법 = **Li₂ZrO₃(LZO) 6–8 nm 비정질 코팅**으로
계면을 패시베이션(XPS로 산화분해 부산물 억제) → 큰 입자도 100 cyc까지 integrity 유지, LZO-bimodal은 120 cyc
안정 + 100th에서 +54.4 mAh/g, 에너지밀도 손실 없음(0.67 vs 0.68 mm).

> ★ **우리에게 왜 중요한가 (3줄):** (1) **재료가 NCA(E=175 GPa)** — 우리가 모델한 NMC811(E=140)과 다르다 →
> CAM 모듈러스 선택지를 재고해야 함; **LPSCl E=22.1 GPa는 Bazzoun 2026·우리 real-bulk 24와 일치**(우리 E_eff
> 1.35/1.53는 연화 프록시). (2) **bimodal의 패킹 이득 vs 균열 페널티**가 우리 Furnas-dip·porosity-vs-조성 작업과
> 직결되며, "큰 입자일수록 깨진다"는 우리 **DEM Auerbach/fracture-aware σ(f_intact, frac_severe)**의 *크기-의존*
> 방향을 실험으로 못 박는다. (3) 그들의 **FEM = 사이클 중 volume-change + cohesive-zone 입계 damage**는 우리
> **MPM = 압밀 중 소성 형상변화**와 같은 연속체 역학이지만 *하중이 다르다*(cycle vs press) → frame[5] 분업의 또
> 다른 축(우리 MPM이 *압밀* morphology를, 그들 FEM이 *사이클* chemo-mechanical을).

## 2. 메타
| 항목 | 값 |
|---|---|
| 저자 | **Junhee Kang**ǁ, **Hong Rim Shin**ǁ (ǁ=equal), Jonghyeok Yun, Young Jun Lim(Samsung SDI), **Riyul Kim**\*(Samsung SDI), **Jong-Won Lee**\*(Hanyang) |
| 소속 | Hanyang Univ. (MSE + Dept. Battery Eng.) + Samsung SDI (Suwon) |
| 저널/년 | ACS Appl. Mater. Interfaces **2025, 17, 60558−60567** |
| DOI | 10.1021/acsami.5c14519 (Received 2025-07-25, Published 2025-10-24) |
| 소재 (CAM/SE/도전제) | **CAM = 다결정 NCA LiNi₀.₈₈Co₀.₀₉Al₀.₀₃O₂** · **SE = LPSCl Li₆PS₅Cl** · 도전제 = Super P carbon |
| 조성 | 복합 양극 NCA:LPSCl:Super P = **72:27:1 wt%** (Samsung SDI 분말) |
| 셀 | NCA\|LPSCl\|Li-In 풀셀 (Li-In 대극); 분리막 = LPSCl 0.1 g 펠릿 |
| 압력 | **제조(fab) 400 MPa** / **작동(operating) stack 200 MPa** (★ fab≠operating 명시) |
| 사이클 조건 | 30 °C, 2.5–4.3 V vs Li/Li⁺, 1st 0.1C(CC-CV charge/CC discharge, CV cutoff 20 %), 이후 0.5C |
| 연구유형 | **실험**(EIS-TLM, SEM/EDS, XPS, cycling) **+ 2D FEM electrochemo-mechanical 모델**(COMSOL-style, Voronoi NCA + cohesive zone) |
| 비교군 | **U-NCA**(unimodal 3 µm 다결정) vs **B-NCA**(bimodal 3+10 µm) vs **LZO-coated B-NCA** |

## 3. 핵심 물성 (수치)

> ⚠ 이 논문은 *압밀 porosity*를 직접 측정·보고하지 않는다(펠릿 *두께*만).  porosity 칸은 n/a — 우리 압밀
> 앵커(Minnmann 14 %, Doux 18 %)와 직접 비교 금지.  대신 **EIS-TLM 저항·용량·E·코팅두께·c_Li 구배비**가
> 이 논문의 정량 앵커.

| 물성 | 값 | 조건 | stated/digitized | 비고 |
|---|---|---|---|---|
| **E_NCA** | **175 GPa** | NCA 다결정 CAM | stated (FEM, ref 42) | ★ 우리 NMC811 140과 다름; ref [42] Koerver 2018 |
| **E_LPSCl** | **22.1 GPa** | LPSCl SE | stated (FEM) | ★ Bazzoun 2026(22.1)·우리 real-bulk 24와 일치 |
| NCA volume change | **5.9 %** (충방전) | Li (de)intercalation | stated | Ω(partial molar volume) = 5.9 % 에서 유도; ε_d = Ω/3·Δc_Li |
| 펠릿 두께 (0.15 g, 400 MPa) | **U-NCA 0.74 / B-NCA 0.68 / LZO-B-NCA 0.67 mm** | 10 mm dia 펠릿 | stated | bimodal이 패킹↑(두께↓); LZO 코팅 영향 무시 |
| 부피 로딩 (NCA) | **B-NCA = 1.1× U-NCA** | mg cm⁻³ | stated (Fig S2: ~1.87 vs ~2.02) | bimodal 패킹 이득 |
| 1st 방전용량 (0.5C) | **U-NCA 183.1 / B-NCA 177.1 mAh g⁻¹** | 30 °C | stated | U가 약간 높음 |
| 1st 방전용량 (0.1C, large 단독) | ~210 mAh g⁻¹ | 10 µm NCA‖Li-In | Fig S4 stated | large 입자도 1st는 정상 작동 |
| **용량유지 @100 cyc** | **U-NCA 67.3 % / B-NCA 47.7 %** | 0.5C, 200 MPa | stated | ★ 핵심 결과; B-NCA는 ~80 cyc 후 급락 |
| **용량유지 @120 cyc (LZO-B-NCA)** | **안정**(급락 없음) | 0.5C | stated | LZO 코팅 효과 |
| LZO 효과 (100th 용량차) | **+54.4 mAh g⁻¹** (LZO vs bare B-NCA) | 100th cyc | stated | |
| **σ_Mises** (FEM, 충전) | **3 µm: 2.6–2.9 GPa / 10 µm: 1.5–3.0 GPa** | SOC charging 0.5C | Fig 3e 컬러바 stated | 큰 입자에서 *구배*가 큼 (표면↔코어) |
| **c_Li** (FEM) | **3 µm: 12.25–12.75 / 10 µm: 12.5–17.5+ kmol m⁻³** | SOC charging | Fig 3d 컬러바 stated | ★ 10 µm 구배가 3 µm 대비 **~10×** |
| cohesive damage | **0(intact)→1(완전박리)** | scalar 변수 | stated | 10 µm 여러 입계에서 →1; 3 µm는 낮음 |
| **R_ion (symmetric, bulk+gb)** | **U-NCA 67.4 / B-NCA 59.8 Ω·cm²** | 펠릿 대칭셀 | stated | 본문값; bimodal이 약간 낮음(유사) |
| R_ele (symmetric) | **B-NCA = U-NCA −33.9 Ω·cm²** | 펠릿 대칭셀 | stated | ★ bimodal 전자전도 ↑(큰 입자 percolation) |
| LZO 두께 | **6–8 nm** 비정질 | sol-gel, NCA 표면 균일 | stated (TEM Fig 4b) | LiNbO₃/Li₄Ti₅O₁₂보다 σ_ion 높음 |
| LPSCl PSD | n/a (직접 미보고) | — | — | NCA만 3 µm / 10 µm (Fig S1) |
| Heckel / P_y | n/a | — | — | 압밀 곡선 없음 |

### Table S1 — 대칭셀 EIS 피팅 (Ω·cm²) [SI verbatim]
| Cathode | R_ion,bulk | R_ion,gb | R_ele |
|---|---|---|---|
| U-NCA | 10.5 | 56.9 | **89.9** |
| B-NCA | 7.4 | 52.4 | **20.0** |
> 본문 "R_ion 67.4 / 59.8" = R_ion,bulk + R_ion,gb (10.5+56.9 / 7.4+52.4).  R_ele 차이 89.9−20.0 = **69.9**;
> 본문 "33.9 Ω·cm² lower"는 다른 정규화/대칭셀 환산(2층) — 두 값 다 "B-NCA 전자저항 낮음"으로 일치, 절대수는 표 우선.

### Table S2 — B-NCA‖LPSCl‖Li-In 풀셀 사이클 중 EIS (0.5C, Ω·cm²) [SI verbatim] ★핵심 degradation 시그니처
| Cycle | R_Ohmic | R_anode | **R_ion** | **R_int** | **R_w** | CPE C (µF sᵑ⁻¹cm⁻²) | η |
|---|---|---|---|---|---|---|---|
| 1 | 16.7 | 13.4 | **5.7** | **113.5** | **70.7** | 112.6 | 0.84 |
| 25 | 17.7 | 15.1 | 6.0 | 275.6 | 106.0 | 29.7 | 0.91 |
| 50 | 17.7 | 15.6 | 6.6 | 332.2 | 176.7 | 28.3 | 0.91 |
| 75 | 17.7 | 1.14† | 6.7 | 335.7 | 212.0 | 21.2 | 0.90 |
| 100 | 17.7 | 15.6 | **6.7** | **501.8** | **353.4** | 14.2 | 0.90 |
> ★ **R_ion 거의 불변(5.7→6.7)** = 이온망은 멀쩡; **R_int(계면) 113.5→501.8(4.4×)·R_w(Warburg) 70.7→353.4(5×)
> 가 75th→100th에서 급등** = 계면열화 + NCA 내 확산경로 tortuosity↑(균열).  R_anode(Li-In 계면)도 거의 불변
> (13.4→15.6, Fig S7) = 열화는 *양극*에서.  (†75 cyc R_anode 1.14는 피팅 이상치로 보임.)

### Table S3 — U-NCA 풀셀 EIS (0.5C) [SI verbatim]
| Cycle | R_Ohmic | R_anode | R_ion | R_int | R_w | CPE C | η |
|---|---|---|---|---|---|---|---|
| 1 | 20.7 | 8.0 | 10.4 | 56.0 | **59.5** | 29.5 | 0.86 |
| 100 | 21.3 | 8.6 | 11.2 | 84.5 | **123.4** | 24.7 | 0.81 |
> U-NCA는 R_int 56→84.5(1.5×)·R_w 59.5→123.4(2.1×)로 *완만* 상승(B-NCA의 4.4×/5× 대비 훨씬 낮음) = 단봉이
> 더 안정.  ★ R_w(1st): U-NCA **59.5** vs B-NCA **70.7** → 본문 "U 59.5 / B 70.7" 일치; R_w ∝ δ_s(확산거리) →
> 큰 입자 = 긴 δ_s = 더 큰 R_w = 더 나쁜 rate.

### Table S6 — LZO-coated B-NCA 풀셀 EIS (0.5C) [SI verbatim] ★코팅 효과
| Cycle | R_Ohmic | R_anode | R_ion | R_int | R_w | CPE C | η |
|---|---|---|---|---|---|---|---|
| 1 | 15.7 | 7.1 | 5.9 | 36.8 | **58.7** | 141.5 | 0.71 |
| 50 | 21.9 | 8.6 | 9.3 | 73.0 | **76.5** | 127.3 | 0.68 |
| 100 | 20.4 | 8.9 | 10.2 | **102.5** | **77.7** | 113.2 | 0.72 |
> ★ **R_w 50→100 = 76.5→77.7 (+1.2 Ω·cm²만)** = 거의 불변(bare B-NCA는 176.7→353.4, +176.7) → LZO가 균열을
> 막아 확산경로 유지.  R_int도 bare(501.8) 대비 100th에서 102.5로 훨씬 낮음.

### Table S4 — FEM electrochemical modeling 파라미터 [SI verbatim] ★우리 MPM/FEM이 미러할 값
| Parameter [unit] | value | 비고 |
|---|---|---|
| Cell dimension [L×W, µm] | **815 × 100** | (셀 스케일; 양극 도메인은 12.5 µm — 본문) |
| Temperature [K] | 298.15 | |
| Reference exchange current density [A m⁻²] | 10 | i₀ (Butler-Volmer) |
| Reference concentration [mol m⁻³] | 48000 [S1] | c_max (Li in NCA) — ref [S1] Yu 2023 |
| Radius of active material [µm] | 5 | (3/10 µm 입자의 대표 반경 가정) |
| Max / Min cell voltage [V] | 4.3 / 2.5 | |
| C-rate | 0.33 | (FEM 충전; 셀 cycling은 0.1/0.5C) |
| **Electrical conductivity of active material [S m⁻¹]** | **1** | σ_e(NCA) FEM 입력 |
| **Diffusion coefficient of Li in AM [m² s⁻¹]** | **3 × 10⁻¹⁴** [S1] | D_Li(NCA) |
| **Electrolyte conductivity [S m⁻¹]** | **0.02** [S2] | σ_ion(LPSCl) = 0.2 mS/cm (FEM 입력) |
| **Interfacial strength [MPa]** | **100** [S3] | cohesive 강도 σ_t^c/σ_s^c (Singh-Pal 2022) |
| **Critical energy release rate [J m⁻²]** | **1** [S4] | G_c (cohesive); ref [S4] Boyce 2022 |

### Table S5 — FEM 경계조건 [SI verbatim]
| 경계 | Mass conservation | Charge conservation | Solid mechanics |
|---|---|---|---|
| Boundary 1 | n·∇c = 0 | n·∇φ_e=0, n·∇φ_s=i_total, φ_s=0 | **n·σ_yy = −P_app** (가압) |
| Boundary 2,3 | n·∇c = 0 | n·∇φ_e = 0 | n·u = 0 (고정) |
| Boundary 4 | n·∇c = 0 | n·∇φ_e=0, n·∇φ_s=i_total | n·u = 0 |
| Boundary 5 | – | n·∇φ_s = 0 | – |
| 전해질-AM 계면 | **−n·D∇c = i_loc/(aF)** | – | – |
> ★ **Boundary 1에 n·σ_yy = −P_app** = 외부 가압을 역학 경계조건으로 인가(우리 MPM wallP/servo와 같은 발상의
> FEM 버전).  전해질-AM 계면 flux = i_loc/aF (Butler-Volmer 전류 → Li flux 변환).

## 4. 시뮬레이션 방법 ★ — FEM electrochemo-mechanical (우리 MPM/DEM이 mirror해야 할 모델)

> ★ 이 절이 우리 모델링과 가장 직접 대응하는 부분.  Supporting Note 1 전체 + Tables S4/S5를 정리.
> **하중이 *사이클(volume change)*이지 *압밀(press)*이 아니다** — 우리 MPM(압밀 소성)과 *상보*(frame[5]).

- **code / 방법**: 2D **유한요소(FEM)** electrochemical + mechanics 결합 (논문은 COMSOL을 명시하진 않으나 Table
  S5 경계조건 표기·multiphysics 구조가 COMSOL 관행).  in-house 가능성도 있으나 ref 체계상 상용 FEM.
- **기하 / 입자 처리** ★:
  - **다결정 NCA를 Voronoi tessellation으로 생성** (secondary particle = 1차입자 다결정 집합).  2차입자 크기 =
    **3 µm와 10 µm** 두 종.  양극 도메인 = **12.5 µm (x–y 방향)**.
  - ⇒ **진짜 SHAPE 변형이 아니라 *Voronoi 다결정 + 입계 cohesive-zone 분리*** — 입자 *형상*은 고정, **입계가
    벌어지는(debonding) damage**가 변형의 본질.  우리 MPM(연속체 소성 *형상* 흐름)과 *다른 종류*의 역학:
    그들 = 취성 입계 박리(cohesive), 우리 = 연성 소성 흐름(J2).
  - NCA 입자는 *완전 방전 상태*에서 시작, 부피 전체 균일 Li 농도 가정.  계산부담 절감 위해 **Li 확산·intercalation
    strain은 등방(isotropic)** 가정.
- **지배방정식 (Supporting Note 1)**:
  - **(S1) Butler-Volmer** 국소전류: `i_loc = −i₀[exp(α_a Fη/RT) − exp(−(1−α_a)Fη/RT)]` (NCA/LPSCl 계면).
  - **(S2) Fick 확산** (고상 Li): `∂c/∂t − D∇²c = 0`.
  - **(S3) 선형탄성**: `ε_ij^e = (1/E)[(1+ν)σ_ij − νσ_kk δ_ij]`.
  - **(S4) 전변형 = 탄성 + 확산유발**: `ε_ij = ε_ij^e + ε_ij^d = (1/E)[(1+ν)σ_ij − νσ_kk δ_ij] + (Ω/3)Δc`
    — ★ **확산유발 변형 ε_d = (Ω/3)·Δc_Li**, **Ω = NCA 5.9 % 부피변화에서 유도한 partial molar volume**.
    (본문 eq: ε_d = Ω/3 × Δc_Li.)
- **계면 박리 = cohesive zone model (CZM)** ★:
  - 두께 0 cohesive 요소를 입계에 삽입(초기 역학 연속성 보존).  **bilinear traction-separation law**.
  - **(S5) 손상개시 = 2차 nominal stress 기준**: `(⟨σ_t⟩/σ_t^c)² + (σ_s/σ_s^c)² = 1`
    (⟨⟩ = Macaulay bracket — *압축* 법선응력은 손상 기여 제외; σ_t/σ_s = 인장/전단 traction, σ_t^c/σ_s^c = 임계값).
  - **(S6) 혼합모드 유효변위**: `d_m = √(⟨d_n⟩² + d_s²)`.
  - **(S7) 손상 전 traction**: `σ_i = K_i d_i` (K = cohesive 강성).
  - **(S8) 손상개시 혼합변위** d_m0 (d_n>0: `d_n^0 d_s^0 √(d_m²/((d_s^0 d_n)²+(d_n^0 d_s)²))`, d_n<0: `d_s^0`).
  - **(eq 1, 본문) damage scalar D**:
    `D = 0` if `d_m,max < d_m0`, else `D = min[ d_fm(d_m,max − d_m0) / (d_m,max(d_fm − d_m0)), 1 ]`
    — d_m,max = 혼합모드 변위 최대값, d_fm = 완전파괴 변위.  **D=0 intact → D=1 완전분리(입계 박리)**.
  - cohesive 입력 = **interfacial strength 100 MPa, G_c = 1 J/m²** (Table S4).
- **MPM/DPC/cap**: 없음 (그들은 사이클 chemo-mechanics; 압밀 소성 J2/cap 없음 — 우리 MPM이 그 칸).
- **전달 솔버 / RNM**: 없음 (전달은 *실험 EIS-TLM*으로; FEM은 σ_ion=0.02 S/m·σ_e=1 S/m을 *입력*만, σ_eff를 풀지
  않음).  ⇒ 그들은 **transport σ를 시뮬로 안 뽑는다** — 우리 Kirchhoff/Holm σ 삼중항이 그 칸(frame[5]).
- **도메인/하중**: 양극 12.5 µm 2D; 가압 P_app을 Boundary 1에 `n·σ_yy = −P_app`로 인가; 충전 시 NCA가
  Li deintercalation으로 수축 → 계면 traction → cohesive damage.
- **특이사항**: **stack pressure(수백 MPa) ≪ 확산유발 응력(GPa)** → 균열의 주범은 가압이 아니라 *Li 불균일*
  (본문 명시; 우리 압밀-응력 중심 관점과 *다른 하중축*임을 분명히).

## 5. Figure set ★ (모든 그림 + 우리가 쓸 점)

| Fig | 내용 (무엇을 보여주나) | 핵심 수치 | 우리가 참고할 점 |
|---|---|---|---|
| **TOC** | bare bimodal(균열) vs LZO-coated(integrity) 모식 | Li₂Sₙ/P₂Sₓ/PO₄³⁻ 부산물 | 균열↔코팅 한눈에 |
| **1a** | U-NCA vs B-NCA 적층 모식 | — | bimodal이 큰입자 사이 작은입자 충전(우리 Furnas 그림) |
| **1b** | 펠릿 사진(0.15 g, 400 MPa) | **0.74 vs 0.68 mm** | 패킹 이득(두께↓) — 우리 porosity-vs-조성 |
| **1c** | 대칭셀 Nyquist + 등가회로 | — | σ_ion/σ_e 추출법 |
| **1d** | R_ion / R_ele 막대 | R_ion 67.4/59.8; R_ele B−33.9 | ★ bimodal: R_ion ≈ 유사, R_ele *크게 낮음* |
| **2a** | 전압프로파일(1st vs 100th) | — | B-NCA 100th 심한 저하 |
| **2b** | ΔV(SOC50 %) vs cycle | B-NCA ≫ U-NCA | 분극 급증 = 균열 시그니처 |
| **2c** | 용량·CE vs cycle | **유지 67.3 %(U) / 47.7 %(B) @100; B는 ~80 cyc 후 급락** | ★ 핵심 결과 |
| **2d** | R_ion vs cycle | 거의 불변(~6) | ★ 이온망 멀쩡 |
| **2e** | R_int vs cycle | 급등(특히 75→100) | 계면열화 |
| **2f** | R_w vs cycle | 급등(70→210+) | 확산거리↑(균열) |
| **3a–c** | 단면 SEM (5/50/100 cyc) | **100 cyc에서 큰입자 균열 출현(노란 점선)** | ★ 균열이 *큰 입자*에 |
| **3d** | FEM c_Li 분포 (3 vs 10 µm) | **10 µm 구배 ~10× 큼** | ★ Li-불균일 = 균열 driver |
| **3e** | FEM σ_Mises (3 vs 10 µm) | 3µm 2.6–2.9 / 10µm 1.5–3.0 GPa | ★ 큰입자 응력 *구배* 큼 |
| **3f** | FEM cohesive damage | **10 µm 여러 입계 D→1(완전박리)** | ★ 크기-의존 입계 균열 정량 |
| **4a** | LZO-B-NCA SEM+EDS (Ni/Zr) | Zr 표면 분포 | 코팅 균일성 |
| **4b** | LZO 단면 TEM | **6–8 nm 비정질** | 코팅 두께 |
| **4c** | LZO-B-NCA rate(0.1–1C) 전압 | — | rate 개선 |
| **4d** | LZO-B-NCA 용량/CE vs cycle | **120 cyc 안정** | 코팅 효과 |
| **4e–g** | LZO-B-NCA R_ion/R_int/R_w vs cycle | **R_w 50→100 +1.2만** | ★ 균열 억제 직접증거 |
| **5a,b** | XPS S2p/P2p (bare vs LZO, 5 cyc) | PS₄³⁻ 161.3/162.5; P₂Sₓ 133.5; **Li₂Sₙ 163.0; PO₄³⁻ 134.4** | ★ LZO가 산화분해 부산물 억제 |
| **5c–e** | LZO-B-NCA SEM(5/50/100 cyc) | **큰입자도 100 cyc integrity** | 균열 억제 |
| **5f–h** | LZO-NCA FEM c_Li/σ_Mises/damage (SOC100 %) | **구배·damage 모두 완화** | ★ 코팅이 Li-구배·응력·박리 다 줄임 |
| **6** | 열화 메커니즘 + LZO 완화 모식 | — | 전체 스토리 한 장 |
| **S1** | 작은/큰 NCA SEM | **3 / 10 µm** | 입경 확인 |
| **S2** | U-NCA vs B-NCA 부피로딩 | ~1.87 vs ~2.02 g cm⁻³ (1.1×) | bimodal 로딩 이득 |
| **S3** | rate(0.1/0.5/1C) U vs B | — | U가 rate 우수 |
| **S4** | large(10µm) NCA 1st 0.1C | ~210 mAh/g | 큰입자도 1st 정상 |
| **S5** | B-NCA EIS vs cycle(25씩, SOC100) | 반원 급성장 | 사이클별 임피던스 원자료 |
| **S6** | 등가회로(TLM) | r_Ohmic/r_anode/(r_ion+(cpe_int‖(r_int+Z_w))) | ★ TLM 회로 구조 |
| **S7** | R_anode vs cycle | 거의 불변(~13–16) | 열화는 양극(음극계면 아님) |
| **S8** | U-NCA EIS(pre/100th) | 완만 성장 | U 안정 |
| **S9** | 제조 직후 단면 SEM | 균열 없음 | 400 MPa 제조는 균열 안 만듦 |
| **S10** | 100 cyc 큰 NCA 균열 단면 | 입계 분리 | ★ 큰입자 균열 직접 |
| **S11** | bare vs LZO-B-NCA 단면 | 코팅 무손상 | LZO가 미세구조 영향 無 |

## 6. Post-processing ★

- **무엇**:
  - **EIS Z-type TLM(transmission line model) 피팅** → 양극 복합층의 분포형 이온/전자/계면 저항 분해.
    회로(Fig S6) = `r_Ohmic — (r_anode ‖ cpe_anode) — 복합양극[ r_ion(전송선) + (cpe_int ‖ (r_int + Z_w)) ]`.
    - **r_ion** = 양극 내 이온전송 저항, **r_anode** = Li-In/LPSCl 계면, **r_int** = NCA/LPSCl 계면저항,
      **cpe_int** = 계면 상수위상요소, **Z_w** = Warburg(NCA 내 고상확산).
  - **Warburg 저항 (eq 2, 본문)**: `R_w = R T δ_s / (z² F² c_{Li⁺,s}² √2 D_s)` — δ_s=확산거리(∝입자크기),
    D_s=Li 유효확산계수, c_{Li⁺,s}=표면 Li 농도, z=전자수.  ★ **R_w ∝ δ_s** → 큰 입자 = 긴 δ_s = 큰 R_w =
    나쁜 rate; 균열은 δ_s(유효확산경로 tortuosity)를 키워 R_w를 추가로 증가.
  - **FEM 후처리**: c_Li 분포·σ_Mises 분포·cohesive damage scalar 맵(입자크기별 3 vs 10 µm).
  - **XPS 디컨볼루션** (S2p / P2p): PS₄³⁻(161.3/162.5 eV)·P₂Sₓ(~133.5)·산화분해 부산물 Li₂Sₙ(~163.0)·
    P₂Sₓ·PO₄³⁻(134.4 eV) 정량 → bare vs LZO 비교로 계면분해 억제 입증.
- **도구**: Biologic SP-300(EIS, 7 MHz–10 mHz, 5 mV AC); ESCALAB 250Xi(XPS, mono Al Kα 1486.6 eV);
  Verios G4UC FEI(SEM/EDS); FEM(상용 multiphysics).  TLM 등가회로 피팅(소프트 미명시).
- **수치화·기록**: 사이클(1/25/50/75/100)별 R_Ohmic/R_anode/R_ion/R_int/R_w + CPE(C, η) 테이블(S2/S3/S6).

## 7. 우리 DEM+MPM 대비  →  `our_dem_baseline.md`

| 항목 | 이 논문(Kang 2025) | 우리 | 차이 / 이유 |
|---|---|---|---|
| **CAM 소재·E** | **NCA Ni₀.₈₈, E=175 GPa** | NMC811, E=140 GPa | ★ **다른 CAM·다른 E** — 우리 CAM 모듈러스 재고 필요(아래 §8 A1) |
| **SE E** | LPSCl **22.1 GPa** | E_eff 1.35(연화)/MPM 1.53 / real 24 | ★ **그들 22.1 = 우리 real-bulk 24 ≈ Bazzoun 22.1** — E_SE 앵커 교차확인; 우리 1.35는 압밀-프록시 |
| **NCA 부피변화** | **5.9 %** (사이클) | (우리 모델은 압밀만, 사이클 부피변화 미모델) | ★ 우리 미보유 — 사이클 chemo-mechanics는 그들 FEM 영역 |
| **하중축** | **사이클(Li deintercalation volume change)** | **압밀(제조 press 300 MPa)** | ★ *다른 하중* — frame[5]의 *시간축* 분업(압밀 vs 사이클) |
| **역학모델** | 2D FEM, Voronoi 다결정 + **cohesive-zone 입계 damage(취성 박리)** | 3D/2D MPM, **J2 연속체 소성 *형상* 흐름(연성)** | ★ 둘 다 연속체지만 *파괴 방식 다름*: 그들 입계 cohesive 박리 ↔ 우리 소성 void-fill; **damage scalar D ↔ 우리 Σdg 소성변형** |
| **fracture driver** | **Li 불균일(농도·응력 구배), 큰 입자일수록 심함** | **압밀 응력(Auerbach), fracture-aware σ(f_intact, frac_severe)** | ★ *driver 다름*(cycling Li-gradient vs 압밀 stress)이나 **"큰 입자 더 깨짐"은 공통** → 우리 크기-의존 파괴 방향 정렬 |
| **bimodal** | 3+10 µm; 패킹 이득(1.1× 로딩) **+ 균열 페널티** | AM_P/AM_S ~6/2 µm + SE 0.5 µm; Furnas dip | ★ 그들 패킹 이득은 우리 dip 이득과 같은 물리; **균열 페널티는 우리 transport-only 모델엔 없음**(사이클 필요) |
| **stack pressure 기여** | **균열에 미미**(수백 MPa ≪ GPa 확산응력) | 압밀 porosity/Heckel의 *주역* | ★ *맥락 다름*: 그들=*사이클 균열*에 압력 미미; 우리=*제조 압밀*에 압력 주역 — 모순 아님(다른 현상) |
| **transport σ** | **시뮬 미산출**(σ는 실험 EIS-TLM만; FEM은 σ_ion/σ_e *입력*만) | **Kirchhoff/Holm σ_ionic+σ_e+σ_thermal 삼중항** | ★ 우리 σ-솔버가 그들 빈 칸(frame[5] 전달 절반) |
| **계면저항 분해** | **EIS-TLM R_ion/R_int/R_w**(사이클 시계열) | σ_ionic 폼 + ASR_ionic (정적) | ★ 그들 R_ion(불변)/R_int·R_w(급등) = *사이클 열화 시그니처* — 우리는 정적; 흡수 가치 |
| **코팅/계면** | **LZO 6–8 nm + XPS 부산물 억제** | coverage(Tabor/Hertz) + se_coating backlog A4(carbon) | ★ LZO=*화학 패시베이션* 코팅 ↔ 우리 coverage=*기계 접촉면적* — 다른 종류; A4(carbon coating)와 다름 |
| **압력 분리** | **fab 400 / operating 200 MPa 명시** | fab 300(Heckel P_y 138) ≠ operating 수~수십 MPa | ★ 같은 *제조≠작동* 인식(Doux/Lee2025 합류); 단 그들 operating 200은 Doux 최적 5보다 높음(고압 운용) |

## 8. 적용 인사이트 (내 연구에 어떻게) — ★ 우리 랩 trend 정렬

- ① **CAM을 NCA로 확장 / E=175 GPa 옵션 추가 (A1-인접, 신규 action)**:
  랩의 실험 trend가 **NCA(Ni₀.₈₈)**다 — 우리는 NMC811(E=140)로 모델했다.  **NCA E=175 GPa**를 CAM 모듈러스
  옵션으로 추가하면 (i) 우리 porosity-vs-조성·load-shielding이 *더 뻣뻣한 CAM*에서 어떻게 변하는지(AM이 더 강하게
  하중지지 → SE 더 적게 변형), (ii) σ_e(NCA) 앵커를 랩 소재로 맞출 수 있다.  ⚠ 단 **NCA σ_e·D_Li는 NMC811과
  다름**(FEM 입력 σ_e=1 S/m, D=3e-14) → σ_e 폼의 σ_AM 재보정 필요.  → `our_dem_baseline.md §0`에 NCA 행 추가 제안.
- ② **크기-의존 파괴(size-dependent cracking)를 우리 Auerbach/fracture-aware σ에 반영 (강링크)**:
  그들 핵심 = **큰 입자(10 µm)가 작은 입자(3 µm)보다 압도적으로 더 깨진다**(c_Li 구배 ~10×, damage→1).  우리 DEM
  fracture(AM_P 92:8 8mAh서 37–40 % cracked)·f_intact·frac_severe는 *크기-의존성*을 명시적으로 안 가짐.
  → **AM_P(큰 다결정)일수록 fracture 확률↑** 하도록 Auerbach 임계를 입경-스케일링(σ_crit ∝ 1/√d 또는 Li-구배
  proxy)으로 보강.  ⚠ **driver 다름 명시**: 그들=*사이클 Li-구배*, 우리=*압밀 응력* — 우리 DEM은 *압밀-시점* 파괴만
  표현하므로 "큰 입자 깨짐"의 *압밀* 버전(접촉응력 집중 ∝ 입경)으로 흡수하고, *사이클* 버전은 frame[5] 미보유로 명시.
- ③ **bimodal의 *역학적 대가*를 우리 Furnas-dip 서사에 추가 (직접)**:
  우리 dip/packing 작업은 bimodal을 *순이득*(porosity↓)으로만 본다.  이 논문 = **패킹 이득(1.1× 로딩) ↔ 균열
  페널티(유지 47.7 % vs 67.3 %)** trade-off를 실험으로 못 박음.  → 우리 "bimodal porosity 이득" 결론에 **"단 큰
  입자 사이클 균열 리스크"** caveat을 붙이고, *최적 입경비*는 패킹만이 아니라 *균열 회피*도 고려해야 함을 명기
  (랩 trend = "toughened" = 균열 억제가 목표).
- ④ **EIS-TLM 사이클 시그니처를 우리 σ 예측의 *열화 축*으로 (흡수 후보, B6-인접)**:
  **R_ion 불변 + R_int·R_w 급등**(75→100 cyc)이 균열의 명확한 시그니처.  우리는 *정적* σ만 예측 → "R_ion stable /
  R_int+R_w rising"을 *예측 가능한 열화 패턴*으로 추가하면(δ_s↑ → R_w↑ via eq 2; 균열 → tortuosity↑) 랩 EIS와
  직접 대응.  → backlog B6(operating-pressure σ-degradation)에 *사이클-Warburg* 축 추가.
- ⑤ **LZO/코팅 = 계면 패시베이션 ↔ 우리 coverage·계면 모델 (A4 인접, 단 종류 다름)**:
  LZO는 *화학* 패시베이션(XPS 부산물 억제)이지 우리 coverage(*기계* 접촉면적)가 아니다.  하지만 "**계면 분해가
  Li-구배를 만들고 → 균열**"이라는 인과는 우리가 *전혀* 모델 안 하는 축(계면 화학열화).  → 당장 흡수는 아니나,
  **interfacial degradation → 균열 → R_int/R_w↑** 체인을 우리 future "계면" 축의 실험 근거로 기록(A4 carbon
  coating과는 다른 *화학* 코팅).
- ⑥ **그들 FEM ↔ 우리 MPM 모델링 패럴렐 (방법론)**:
  그들 cohesive-zone **damage scalar D(0→1)** = 우리 MPM **누적 소성변형 Σdg**의 *취성 박리* 대응물.  둘 다
  연속체 역학 + 손상/소성 변수.  → 우리 MPM 문서에 "사이클 chemo-mechanical은 cohesive-zone(Kang 2025 랩),
  압밀 plastic은 J2(우리)"로 *시간축 분업*을 명문화 → frame[5] 확장.

## 9. 인용 가능 문장 (deck/paper용)

- "Our group's experimental work on bimodal NCA/LPSCl cathodes (Kang, Shin et al., ACS AMI 2025) shows
  that the packing benefit of a 3+10 µm bimodal cathode (1.1× volumetric loading, lower electronic
  resistance) is offset by **size-dependent intergranular cracking of the large 10 µm particles**,
  driven by spatially inhomogeneous Li concentration and stress gradients (~10× larger c_Li gradient in
  10 µm vs 3 µm particles) from NCA/LPSCl interfacial decomposition — capacity retention dropping from
  67.3 % (unimodal) to 47.7 % (bimodal) at 100 cycles."
- "A 2D electrochemo-mechanical FEM with Voronoi-tessellated polycrystalline NCA and a cohesive-zone
  grain-boundary damage model (Kang 2025) quantifies that the **diffusion-induced stress reaches GPa,
  far exceeding the few-hundred-MPa stack-pressure stress** — establishing that the dominant fracture
  driver under cycling is Li inhomogeneity, not the applied pressure (a key complement to our
  compaction-stress DEM/MPM picture)."
- "E_LPSCl = 22.1 GPa adopted in our group's FEM (Kang 2025) coincides with the Bazzoun 2026 value
  (22.1) and our real-bulk anchor (≈24 GPa), confirming the SE-modulus baseline behind our softened
  E_eff = 1.35/1.53 GPa proxy."
- "A conformal 6–8 nm amorphous Li₂ZrO₃ coating passivates the NCA/LPSCl interface (XPS: suppressed
  Li₂Sₙ/P₂Sₓ/PO₄³⁻ decomposition byproducts), keeping the large particles intact to 120 cycles and the
  Warburg resistance nearly flat (R_w +1.2 Ω·cm² over cycles 50→100 vs +176.7 for bare B-NCA)."

## 10. 주의/한계 (over-claim 방지)

- **압밀 porosity 미보고** → 이 논문은 *압밀 porosity/밀도*를 직접 측정·보고하지 않는다(펠릿 *두께*만: U 0.74 /
  B 0.68 mm).  우리 압밀 앵커(Minnmann 14 %, Doux 18 %, 우리 DEM 15.6 %)와 **직접 비교 금지** — 이 논문의 정량
  앵커는 *EIS 저항·용량·E·코팅두께·FEM 구배비*다.
- **하중축이 *사이클*이지 *압밀*이 아님** → 그들 FEM의 응력·damage는 *Li deintercalation volume change*가 하중.
  우리 MPM/DEM의 압밀-응력과 *같은 현상이 아니다*.  "큰 입자 더 깨짐"은 공통이나 *driver가 다름*(사이클 Li-구배
  vs 압밀 접촉응력) — 흡수 시 반드시 분리 명시.
- **CAM이 NCA(≠NMC811)** → E=175(우리 140), σ_e·D_Li도 다름.  우리 NMC811 결과를 NCA에 *절대값* 전이 금지 —
  E·σ_e 재보정 후 *추세*만.
- **transport σ는 시뮬 아님** → σ_eff,ion/σ_e를 *풀지 않는다*(실험 EIS-TLM + FEM 입력만).  그들의 R_ion/R_int/R_w
  는 *측정값*이지 *예측 솔버* 산출이 아니다 → 우리 Kirchhoff/Holm σ와 *방법이 다름*(우리=솔버, 그들=실측+TLM 피팅).
- **FEM = cohesive-zone 입계 박리(취성)** → 우리 MPM의 *연성 소성 형상 흐름*과 *파괴 메커니즘이 다르다*.  damage
  scalar D를 우리 소성변형 Σdg와 *개념* 대응은 되나 *동일시 금지*(취성 cohesive ≠ 연성 J2).
- **stack pressure "기여 미미"는 *사이클 균열* 맥락 한정** → 우리 *압밀 porosity/Heckel*에서는 압력이 주역.
  "압력 기여 미미"를 우리 압밀 결론으로 잘못 전이 금지 — 그들 진술은 *cycling 중 균열*에 국한.
- **FEM 일부 입력은 *대표값* 가정** → Table S4 "AM 반경 5 µm"는 3/10 µm의 대표 단일값; isotropic 확산/strain 가정;
  815×100 µm는 *셀* 스케일이고 균열 해석 도메인은 12.5 µm.  정량 c_Li/σ 절대값은 *모델 가정 내* 추세로.
- **digitized 구분**: Fig S2 부피로딩(~1.87/2.02), Fig 3d/3e 컬러바 범위는 *그림에서 읽은 값*(±, 추세) — Table
  S1–S6·본문 stated 수치(저항·용량·E·두께)와 구분.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
