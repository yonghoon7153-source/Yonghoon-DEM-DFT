# Stabilizing the interface between high-Ni oxide cathode and Li₆PS₅Cl for all-solid-state batteries via dual-compatible halides — Cha et al. (J. Power Sources 2024) — **[우리 그룹]**

> slug `cha2024_dualcompatible_halide_ncm_lpscl_interface` · DOI `10.1016/j.jpowsour.2024.235157` · type `exp (계산 無)` · PDF `a0db35d2-05._Stabilalides.pdf` · digested `2026-06-26` · status ✅
> **저자**: Hyohyun Cha†ᵃ, Jonghyeok Yun†ᵇ, Siwon Kimᵇ, Junhee Kangᵇ, Minhyeong Choᵇ, Woosuk Choᶜ (corresponding, cho4153@keti.re.kr), **Jong-Won Lee**ᵇ (corresponding, jongwonlee@hanyang.ac.kr). †H. Cha and J. Yun contributed equally.
> ᵃ DGIST (Daegu Gyeongbuk Institute of Science and Technology), Dept. of Energy Science & Eng. · ᵇ **Hanyang University, Division of Materials Science & Engineering** · ᶜ KETI (Korea Electronics Technology Institute), Advanced Batteries Research Center.
> **J. Power Sources 617 (2024) 235157**. Received 21 Feb 2024, revised 24 Jun 2024, accepted 29 Jul 2024, online 31 Jul 2024.
> **[우리 그룹]** = 안용훈 그룹 계보 (한양대 **Jong-Won Lee** 교신). kang2025(기생반응)·kang2026(intertwined 리뷰)와 **동일 교신저자·동일 그룹**. Junhee Kang은 이 논문 공저 = kang2025/kang2026 제1·공저자와 동일 인물 → **우리 그룹 cathode-interface 라인의 초기(2024) 논문**.

---

## 0. 이 digest를 읽는 법 (먼저 읽으세요 — 핵심 개념 "dual compatibility")

이 논문은 **조성을 바꾸는 게 아니라**(Zuo의 Cl 함량 비교, kang2025의 SE-코팅 비교와는 다른 레버), **NCM 양극 입자 표면에 *별도의 할라이드 SE*를 나노층으로 코팅**해 NCM–LPSCl 계면을 안정화한다. 비교하는 것은 **세 종류의 Li⁺-전도성 할라이드**다:

- **LIC = Li₃InCl₆** (monoclinic, In 기반)
- **LYC = Li₃YCl₆** (trigonal, Y 기반)
- **LZC = Li₂ZrCl₆** (Zr 기반)

핵심 통찰은 **"dual compatibility(이중 호환성)"** 라는 개념이다. 양극 복합체(composite cathode)에서 할라이드 코팅층은 **두 개의 다른 상**과 동시에 접촉한다:

1. **NCM 양극활물질**(산화물, 고전압서 산소 방출) — 한쪽 면
2. **LPSCl 황화물 SE**(matrix) — 다른 쪽 면

좋은 계면 수식제(interfacial modifier)가 되려면 이 **두 상 모두와 부반응을 일으키지 않아야** 한다(=dual compatible). 이 논문의 발견:

- **LIC(In)**: NCM과도, LPSCl과도 **둘 다 분해**(In→In₂S₃ 환원, LiCl 등 생성) → **나쁨**.
- **LYC(Y)**: NCM과는 OK지만 **LPSCl과 분해**(Y₂S₃ 생성) → **반쪽만 호환**.
- **LZC(Zr)**: NCM과도 LPSCl과도 **안정**(Zr⁴⁺가 황화물 형성을 견딤, 7일 후에도 무분해) → **dual compatible = 최고**.

> 🔑 **한 문장**: 할라이드를 양극 계면 수식제로 쓸 때, 단순히 σ(이온전도도)가 높은 게 아니라 **NCM과 LPSCl *둘 다*와 화학적으로 호환되는 것**이 결정적 설계 인자이며, **Li₂ZrCl₆(LZC)이 그 dual compatibility를 만족**해 NCM@LZC가 가장 낮은 계면저항·최고의 율속·수명을 준다.

> ⚠ **흔한 오해 방지**: "σ가 높은 할라이드가 좋다"가 **아니다**. 실제로 σ는 **LIC(1.12 mS/cm) > LZC(0.51) > LYC(0.37)** 순인데, 성능(낮은 계면저항·수명)은 **LZC > LYC > LIC** 순으로 σ와 **반대 경향에 가깝다**(특히 LIC는 σ 1등인데 성능은 꼴찌). 결정 변수는 **σ가 아니라 화학적 호환성(dual compatibility)**. 논문이 명시: "interfacial resistance ... cannot be explained in terms of ionic conductivity."

> ⚠ **이 논문엔 DFT/계산이 전혀 없다.** 전부 실험(XRD·STEM·SEM-EDS·XPS·EIS+TLM·충방전). 우리 DFT 수치와의 직접 비교는 부적절하며, **개념(전자절연·dual-compatible interphase, 분해산물 화학)·우리 그룹 trend 정렬** 용도로만 연결한다. 호환성의 근거로 든 것은 **금속이온 표준 환원전위 trend(In vs Y vs Zr)**(정성)이지 계산이 아니다.

---

## 1. 한 줄 요약

Ni-rich NCM(LiNi₀.₈₃Co₀.₁₁Mn₀.₀₆O₂) 입자에 **Li⁺-전도성 할라이드(LIC/LYC/LZC)를 RAM(resonant acoustic mixing) 공정으로 8–10 nm conformal 나노층 코팅**하면, NCM–LPSCl 계면의 전기화학 부반응이 억제되어 **계면저항이 bare NCM 74.4 → LZC 20.1 Ω·cm²로 ~3.7배 감소**하고 율속·수명이 향상된다. 세 할라이드 중 **Li₂ZrCl₆(LZC)이 NCM과 LPSCl *양쪽 모두*와 화학적으로 호환(dual compatibility)** — LIC는 양쪽 다 분해, LYC는 LPSCl과 분해 — 하여 **7일 무분해, 100 cyc 후 용량유지율 91.2 %**(LIC 80.8 %, LYC 87.3 %)로 최고 성능을 준다. **dual compatibility가 양극 복합체 설계의 결정적 인자**.

## 2. 메타 / 동기

| 항목 | 내용 |
|---|---|
| 비교 | **bare NCM** vs **NCM@LIC** vs **NCM@LYC** vs **NCM@LZC** (할라이드 *종류* 비교; 조성·Cl함량 아님) |
| 양극활물질(CAM) | **LiNi₀.₈₃Co₀.₁₁Mn₀.₀₆O₂** (POSCO-JK, 단결정 single-crystalline, 입자 ~3 µm) — 고-Ni layered oxide |
| 황화물 SE (matrix) | **Li₆PS₅Cl (LPSCl = 우리 comp1)** (POSCO-JK) |
| 계면 수식제(할라이드) | **LIC=Li₃InCl₆ / LYC=Li₃YCl₆ / LZC=Li₂ZrCl₆** (입자 ~5 µm, 직접 합성) |
| 음극 | **Li–In** (areal cap 3.2 mAh/cm², N/P=1.74) |
| 핵심 질문 | NCM–LPSCl 계면 부반응(고전압 LPSCl 산화분해)을 할라이드 나노층으로 어떻게 억제하나? 어떤 할라이드가 최적이고 *왜*? |
| 답 | **dual compatibility** — NCM·LPSCl 양쪽과 호환되는 **Li₂ZrCl₆(LZC)**이 최적. In(LIC)·Y(LYC)는 부분/완전 비호환 |
| 갭/동기 | 기존 oxide 코팅(LiNbO₃·Li₂ZrO₃)은 σ가 10⁻⁶–10⁻⁹ S/cm로 낮고 절연성 → 율속 손해. 할라이드는 σ 높고 고전압 안정 → 더 나은 계면 수식제 후보. 단 **계면 호환성이 조성 의존**임이 미지 |
| 선행맥락 | Asano(ref 27): Li₃YCl₆(LYC) σ 0.51 mS/cm + LiCoO₂ 양극서 우수 사이클. 이후 LIC·LZC·LSC(Li₃ScCl₆) 보고. 본 논문 = **세 할라이드를 *동일 조건*서 NCM-LPSCl 양극 복합체에 적용·정량 비교** |
| 공정 강점 | **RAM (Resonant Acoustic Mixing, Resodyn)** = 공명 가속(50G)으로 무용매 균일 코팅, 짧은 시간 (ref 38,39) |

## 3. 핵심 물성 (수치 총정리)

> ⚠ 전압 기준: 셀은 **Li–In 대극**이나, 충방전 곡선은 **V vs Li/Li⁺**로 표기(2.5–4.3 V). σ는 RT 측정.

### 3.1 할라이드 자체 물성

| 할라이드 | 결정구조 | σ (RT, mS/cm) | 입자 크기 | 비고 |
|---|---|---|---|---|
| **LIC = Li₃InCl₆** | monoclinic | **1.12** | ~5 µm | σ 최고 |
| **LYC = Li₃YCl₆** | trigonal | **0.37** | ~5 µm | σ 최저 |
| **LZC = Li₂ZrCl₆** | (trigonal-계) | **0.51** | ~5 µm | σ 중간; **dual compatible** |
| (참고) LPSCl | cubic | ~2.9–7 (문헌) | (POSCO-JK) | matrix SE |

> 🔑 **σ 순서 = LIC(1.12) > LZC(0.51) > LYC(0.37)** — 성능 순서(LZC>LYC>LIC)와 **불일치**. σ는 결정 변수가 아님.

### 3.2 코팅·구조

| 항목 | 값 | 출처 |
|---|---|---|
| NCM : 할라이드 코팅 비율 | **97 : 3 wt%** | 본문(RAM, 50G) |
| 코팅 두께 (conformal) | **8–10 nm** (LIC; LZC·LYC도 유사) | STEM-HAADF (Fig 1d), EDS (Fig 1e,f) |
| 합성: LIC | LiCl+InCl₃ 화학량론, ball-mill 700 rpm 4 h(지르코니아), **260 °C 3 h** anneal | §2.1 |
| 합성: LYC/LZC | LiCl+YCl₃(LYC) / LiCl+ZrCl₄(LZC), 700 rpm 56 h or 12 h | §2.1 |
| 상순도 | LIC·LYC·LZC **phase-pure** (XRD·SEM, Fig S1) | §3 |
| NCM@halide XRD | NCM 패턴과 일치, 할라이드 peak은 3 wt% 너무 적어 미검출 (Fig S3); 양 늘리면 출현 (Fig S4) | §3 |

### 3.3 전기화학 성능 (Fig 2: 율속, Table S1: 임피던스)

| 항목 | bare NCM | NCM@LIC | NCM@LYC | NCM@LZC | 출처 |
|---|---|---|---|---|---|
| 방전용량 @0.1C | 더 낮음 | **206.6** | **200.8** | **206.8** mAh/g | Fig 2a–d |
| 방전용량 @2C | 더 낮음 | — | — | **141.3** (vs bare 198.6 @0.1C 기준 큰 향상) | Fig 2e |
| 1차 충전 전압 sagging | **있음**(낮은 셀전압=부반응) | 없음 | 없음 | **없음**(부반응 억제) | Fig 2a–d, Fig S7 |
| **이온저항 r_ion** (Ω·cm²) | **70** (가장 낮음) | 78 | **99** (가장 높음) | 84 | Fig 3f, Table S1 |
| **계면저항 (interfacial)** | **74.4** | 55 | 30 | **20.1** (가장 낮음, bare의 ~1/3.7) | Fig 3f, 본문 |
| 전자저항 (electronic) | — | — | — | **더 낮음**(LIC/LYC보다) | Fig S10–S11 |

> 🔑 **이온저항 순서 = NCM@LIC(78) < NCM@LZC(84) < NCM@LYC(99)** — σ trend와 일치(LIC σ 최고→r_ion 최저). **할라이드 나노층은 r_ion을 *약간* 올림**(절연 아님, 얇아서 영향 작음). 핵심 향상은 **계면저항**에서 온다.

### 3.4 7일 호환성 시험 (Fig 4: 할라이드–LPSCl 복합체 EIS+XRD+XPS)

| 복합체 | 7일 EIS | 분해산물 (XRD) | XPS 증거 | 호환성 |
|---|---|---|---|---|
| **LIC–LPSCl** | 임피던스 **증가** | **In₂S₃, P₄S₃, LiCl, InCl₆** | In 3d: In₂S₃ peak(445.1 eV), InCl₆(446.4 eV) | **비호환** |
| **LYC–LPSCl** | 임피던스 **증가** | **Y₂S₃, LiCl, Li₂S** | Y 3d: Y₂S₃ peak(157.3, 159.3 eV) | **비호환** |
| **LZC–LPSCl** | **변화 없음(7일)** | **분해 무**(Li₂S 미량만) | Zr 3d: **불변**(분해산물 無) | **호환 ✓** |

### 3.5 100 사이클 수명 (Fig 5: NCM vs NCM@LZC @0.33C, 2.5–4.3 V)

| 항목 | bare NCM | NCM@LZC | NCM@LIC | NCM@LYC | 출처 |
|---|---|---|---|---|---|
| 100 cyc 후 방전용량 | **140 mAh/g** (급감) | 더 높음 | — | — | Fig 5b |
| **100 cyc 용량유지율** | **83.1 %** | **91.2 %** | 80.8 % | 87.3 % | Fig 5b, S12, 본문 |
| cycling 후 단면 SEM | 균열 無 (단결정) | 균열 無 | — | — | Fig 5c,d, S13 |
| cycling 후 XPS (P 2p) | **phosphate·P₂Sₓ·Li₂S 분해 출현** | **거의 불변** | — | — | Fig 5e,f |
| cycling 후 XPS (S 2p) | Li₂S 출현 | PS₄³⁻ 유지 | — | — | Fig 5e,f |
| cycling 후 XPS (Zr 3d) | — | **불변**(LZC 안정) | — | — | Fig 5f |

> 🔑 **수명 순서 = LZC(91.2 %) > LYC(87.3 %) > bare(83.1 %) > LIC(80.8 %)**. **LIC는 bare보다도 나쁨** — In의 비호환 분해가 코팅 안 한 것보다 해롭다는 강력한 증거. dual-compatible LZC만 확실한 이득.

## 4. 재료 & 방법 (실험 전용)

- **할라이드 합성**: 화학량론 LiCl + (InCl₃ / YCl₃ / ZrCl₄), planetary micro-mill(Pulverisette 7) 700 rpm, 지르코니아 vial/ball, vacuum 밀봉. LIC만 260 °C 3 h anneal.
- **NCM@halide 코팅**: **RAM(Resonant Acoustic Mixer, Resodyn)**, NCM:halide = **97:3 wt%**, 가속도 **50G**(G=9.81 m/s²). 무용매. → 8–10 nm conformal 나노층.
- **양극 복합체**: NCM@halide : LPSCl : Super-P = **72:27:1 wt%**, ball-mill 48 h. 100 MPa pelletize → 433 MPa 압연. 전극 직경 1 cm, 활물질 로딩 9.2 mg/cm², areal cap 1.84 mAh/cm², apparent electrode density 3.18 g/cm³.
- **셀**: 복합양극 / LPSCl 분리막(127 mg/cm², 600 µm, 433 MPa) / **Li–In**(areal cap 3.2 mAh/cm², N/P 1.74) / SUS foil(100 µm) 집전체. 운전압력 **250 MPa**.
- **σ 측정**: 할라이드 분말 ion-blocking symmetric cell(SS|SE|SS), 433 MPa pelletize, 측정 시 250 MPa, Bio-Logic VSP-300, 7 MHz–5 mHz, 5 mV, 25 °C.
- **충방전**: 2.5–4.3 V vs Li/Li⁺. 율속 0.05–2C (1C=200 mAh/g). 사이클 0.33C CC-CV(충전)/CC(방전).
- **임피던스 디커플링**: **TLM(transmission-line model) 기반 등가회로**(ref 28,40)로 양극 복합체 임피던스를 **r_ion(이온)·r_int+cpe_int(계면)·z_w(Warburg)** 로 분해. 7 MHz–5 mHz.
- **특성**: XRD(Cu Kα, dry room, Rigaku MiniFlex 600) · FE-SEM(S-4800, BSE mode) · STEM-HAADF+EDS(Tecnai G2 F20) · **XPS**(monochromatic Al Kα 1486.6 eV, ESCALAB 250Xi, Thermo).
- **이론/계산**: **없음**. 호환성 근거 = **금속이온 표준 환원전위 trend**(In vs Y vs Zr, 정성 인용 ref 37,46,47).

## 5. 결과 — 섹션별 상세

### 5.1 할라이드 합성·σ·구조 (Fig 1, S1)
- 세 할라이드 모두 phase-pure(monoclinic LIC, trigonal LYC/LZC; Fig 1b 결정구조 도식), 입자 ~5 µm.
- **σ: LIC 1.12 > LZC 0.51 > LYC 0.37 mS/cm** (RT, ion-blocking cell).
- RAM으로 NCM에 **8–10 nm conformal 코팅**(STEM-HAADF Fig 1d: NCM|LZC 경계 선명; EDS Fig 1e,f: Ni/In/Y/Zr/Cl 분포로 conformal 확인). XPS(Fig S6)·SEM-EDS(Fig 1f)로 코팅 균일성 재확인.
- XRD(Fig S3): 3 wt% 할라이드 너무 적어 미검출; 양 늘리면 peak 출현(Fig S4).

### 5.2 율속·충방전 (Fig 2)
- **bare NCM은 1차 충전서 전압 sagging**(낮은 셀전압) = NCM-LPSCl 부반응(저항성 interphase) → Fig S7. **NCM@halide는 sagging 없음** = 부반응 억제 → 전기화학 안정성 향상.
- 방전용량(0.1C): LIC 206.6 / LYC 200.8 / LZC 206.8 (bare보다 높음).
- **2C서 NCM@LZC 141.3 mAh/g로 율속 가장 우수**.
- 율속 성능이 **할라이드 종류에 전적으로 의존** → "efficacy is exclusively determined by the halide constituents".

### 5.3 임피던스 디커플링 (Fig 3, Table S1)
- TLM 등가회로(Fig 3a): r_ion(Li⁺ 수송)·r_int·cpe_int(계면반응)·z_w(확산). Nyquist(Fig 3b–e) 피팅.
- **이온저항 r_ion**: NCM@LIC(78) < NCM@LZC(84) < NCM@LYC(99) — bare(70)보다 약간↑(할라이드 나노층 존재). σ trend와 일치.
- **계면저항**: **NCM@LZC 20.1 Ω·cm² = bare 74.4의 1/3.7**. 할라이드 나노층이 계면반응을 크게 줄임.
- → 율속 향상의 주원인 = **계면 kinetics 개선**(이온전도가 아니라).
- 🔑 **결정적 문장**: "interfacial resistance of NCM@halide depends strongly on the composition of the halide nanolayer, which **cannot be explained in terms of ionic conductivity**." → 호환성(화학)이 변수.

### 5.4 7일 호환성 시험 — **dual compatibility의 직접 증거** (Fig 4)
- **할라이드–LPSCl 복합체**(NCM 없이 SE끼리만)를 7일 방치 후 EIS·XRD·XPS:
  - **LIC–LPSCl·LYC–LPSCl**: 임피던스 **증가**(σ 저하) → 분해.
  - **LZC–LPSCl**: 7일 임피던스 **불변** → 무분해.
- **XRD 분해산물**: LIC–LPSCl → **In₂S₃, P₄S₃, LiCl, InCl₆**(Fig 4d); LYC–LPSCl → **Y₂S₃, LiCl, Li₂S**(Fig 4e); **LZC–LPSCl → 분해 무**(Li₂S 미량, Fig 4f).
- **XPS**(Fig 4g–i): LIC In 3d에 In₂S₃(445.1)·InCl₆(446.4 eV) peak 추가; LYC Y 3d에 Y₂S₃(157.3, 159.3 eV) peak; LZC Zr 3d **불변**.
- → **LZC만 LPSCl과 호환**. LIC·LYC는 LPSCl과 비호환.
- **LZC가 NCM과도 호환**: Fig S9 XPS로 LZC–NCM 호환 확인 → LZC = NCM·LPSCl **양쪽** 호환 = **dual compatible**.
- (선행 ref 37: LIC는 NCM 접촉 시 낮은 SOC서도 환원분해 → In-Li intermixing → 저항성 interphase. ↔ LYC·LZC는 금속이온 표준 환원전위가 더 안정해 NCM 호환↑.)

### 5.5 100 사이클 수명·post-mortem (Fig 5)
- NCM vs NCM@LZC @0.33C, 100 cyc:
  - bare NCM 100 cyc 후 **140 mAh/g로 급감**(retention **83.1 %**).
  - **NCM@LZC retention 91.2 %**(> NCM@LIC 80.8 %, NCM@LYC 87.3 %; Fig S12).
- **단면 SEM**(Fig 5c,d, S13): bare·NCM@LZC **둘 다 균열 無**(단결정 NCM) → 용량열화는 **NCM 입자 기계분해가 아니라 NCM-SE 계면 부반응**이 원인.
- **post-mortem XPS**(Fig 5e,f):
  - bare NCM: P 2p에 **phosphate·P₂Sₓ** 출현, S 2p에 **Li₂S** 출현 = LPSCl 분해.
  - NCM@LZC: P 2p·S 2p·Zr 3d **거의 불변** = LZC가 계면 안정화.
- → 용량유지의 화학적 근거 = **LZC 나노층이 NCM-LPSCl 분해를 억제**.

## 6. 메커니즘 종합 (Fig 6 = graphical abstract)

**Fig 6**: NCM·NCM@LIC·NCM@LYC·NCM@LZC의 계면 도식(범례: NCM / LPSCl / LIC / LYC / LZC / **Resistive interphase**).

- **bare NCM**: NCM↔LPSCl 직접접촉 → 고전압 충전 시 LPSCl **전기화학 산화분해**(좁은 ESW) → **저항성 interphase** 형성(빨강) → Li⁺·e⁻ 수송 저해 → 율속·수명 저하.
- **NCM@LIC**: LIC가 NCM·LPSCl **둘 다와 분해**(In₂S₃ 등) → 양쪽에 저항성 interphase → bare보다도 나쁨.
- **NCM@LYC**: NCM과는 OK, **LPSCl과 분해**(Y₂S₃) → LYC/LPSCl 계면에 저항성 interphase → 부분 개선.
- **NCM@LZC**: NCM·LPSCl **양쪽 모두 호환**(Zr⁴⁺가 metal-sulfide 형성 견딤·passivating) → 저항성 interphase 無 → **facile charge transport** → 최고 율속·수명.

> 🔑 **메커니즘 체인**: [할라이드 코팅이 NCM↔LPSCl 직접접촉 차단] → [그러나 할라이드 자신이 NCM/LPSCl과 분해하면 *새로운* 저항성 interphase 생성(LIC/LYC)] → [**Zr⁴⁺(LZC)만 양쪽과 안정 = dual compatible**] → [저항성 interphase 無 → 계면저항 74.4→20.1 Ω·cm²] → [율속 2C 141.3 mAh/g + 100 cyc 91.2 %]. **핵심 분기점 = 코팅 할라이드의 *양쪽-호환성*(dual compatibility)**, σ 아님.

## 7. 전체 논증 흐름

세 할라이드 합성·σ 측정(LIC>LZC>LYC) → RAM 8–10 nm conformal 코팅(STEM/EDS) → 율속(NCM@halide > bare, sagging 사라짐) ⟹ **코팅이 부반응 억제** → TLM 임피던스 디커플링(계면저항 LZC 20.1 ≪ bare 74.4; r_ion은 σ trend·약간↑) ⟹ **개선은 계면 kinetics, σ 무관** → 7일 호환성(LIC·LYC는 LPSCl과 분해 In₂S₃/Y₂S₃, LZC 무분해 + LZC는 NCM과도 OK) ⟹ **LZC = dual compatible** → 100 cyc(LZC 91.2 % > bare 83.1 % > LIC 80.8 %) + post-mortem XPS(bare 분해/LZC 불변) ⟹ **dual compatibility가 수명을 결정** → Fig 6 도식으로 닫음 → 결론: "compatibility of the interfacial modifier ... is a crucial design factor for solid composite cathodes."

## 8. DFT/계산 방법 ★

**없음.** 순수 실험. 호환성의 *기전*은 **금속이온 표준 환원전위 trend**(In이 가장 쉽게 환원 → LIC 비호환; Y·Zr 더 안정; Zr⁴⁺가 metal-sulfide passivation 견딤)로 **정성 설명**(ref 37,46,47 인용). → **우리 grand-potential interface reactivity가 이 화학을 voltage-resolved로 채워 검증·확장**할 수 있는 지점(§11).

## 9. Figure set ★

| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| 1a | NCM↔LPSCl 부반응(저항층) vs 할라이드 코팅 도식 | 양극 계면 부반응 프레임 |
| 1b | LIC/LYC/LZC 결정구조 | 할라이드 3종 동정 |
| 1c | RAM 코팅 공정 | 무용매 conformal 코팅법 |
| 1d | NCM@LZC STEM-HAADF (8–10 nm 층) | conformal 코팅 두께 직접증거 |
| 1e,f | EDS mapping(Ni/In/Y/Zr/Cl) | 코팅 균일성 |
| 2a–d | bare/LIC/LYC/LZC 충방전 곡선(0.05–2C) | sagging(bare만)·율속; **부반응 정성지표** |
| 2e | 율속 용량 vs C-rate | NCM@LZC 2C 141.3 우수 |
| 3a | **TLM 등가회로**(r_ion/r_int/cpe/z_w) | 양극 복합체 임피던스 디커플링 틀(차용) |
| 3b–e | Nyquist 피팅 | r_ion·r_int 추출 |
| 3f | **이온저항·계면저항 막대**(계면 LZC 20.1≪bare 74.4) | σ≠계면저항 핵심증거 |
| 4a–c | 할라이드–LPSCl 7일 EIS(LIC/LYC 증가, LZC 불변) | **호환성 정량** |
| 4d–f | 7일 후 XRD(In₂S₃·P₄S₃·LiCl / Y₂S₃·LiCl·Li₂S / 무분해) | **분해산물 동정** |
| 4g–i | 7일 후 XPS(In 3d / Y 3d / Zr 3d) | **dual compatibility XPS 증거**(우리 XPS ref와 대조) |
| 5a,b | NCM vs NCM@LZC 100 cyc(retention 83.1 vs 91.2 %) | 수명 정량 |
| 5c,d | cycling 후 단면 SEM(균열 無) | 열화=계면, 기계분해 아님 |
| 5e,f | cycling 후 XPS(P 2p/S 2p/Zr 3d; bare 분해/LZC 불변) | **계면 분해 화학**(우리 grand-potential 산물과 대조) |
| 6 | dual compatibility 도식(저항성 interphase 유무) | 메커니즘 deck 도식 |
| S1 | 할라이드 XRD·SEM(phase-pure) | 상순도 |
| S7 | 1차 충전 전압(sagging) | 부반응 정성 |
| S8 | LYC·LZC vs LIC 산화안정성 비교 | 할라이드 산화창 |
| S9 | LZC–NCM XPS 호환 | LZC NCM-side 호환 |
| S10,S11 | NCM@LZC 전자저항·LZC/카본 계면 | 전자전도 |
| S12 | NCM@LIC/LYC 사이클(80.8/87.3 %) | 3종 수명 비교 |

## 10. Post-processing ★

- **TLM(transmission-line model) 임피던스 디커플링**: 양극 복합체 Nyquist를 r_ion(이온)·r_int+cpe_int(계면)·z_w(Warburg)로 분해(Fig 3a 등가회로). 기록 = r_ion/계면저항(Ω·cm²). → **kang2025·Zuo와 동일 계열 도구**(우리 그룹 cathode-interface 표준 분석).
- **XRD post-mortem**: 7일 호환성·cycling 후 분해상 동정(In₂S₃·P₄S₃·Y₂S₃·LiCl·Li₂S). 기록 = 2θ peak.
- **XPS**: In 3d/Y 3d/Zr 3d/P 2p/S 2p로 분해종 화학상태 정량. 기록 = BE(eV) + 분해 peak 출현/불변.
- **EIS aging**(7일): 호환성을 임피던스 증가율로 정량.
- **STEM-HAADF+EDS**: 코팅 두께·conformality.
> 우리 적용: **TLM 계면저항 분해 + XPS 분해종 동정**으로 "어떤 코팅이 *새* 저항층을 안 만드나" 정량 → 우리 grand-potential interface reactivity(어떤 산물이 생기나)의 **실험 카운터파트**.

## 11. 우리 DFT 대비 (comp1/modelc) → `../our_dft_baseline.md`

| 항목 | Cha 2024(exp) | 우리(DFT) | 일치/차이 + 이유 |
|---|---|---|---|
| SE = LPSCl(comp1) | matrix SE = Li₆PS₅Cl | comp1 = Li₆PS₅Cl | **동일 물질** — 우리 baseline과 직결 |
| NCM-LPSCl 고전압 분해 | bare서 phosphate·P₂Sₓ·Li₂S 생성(XPS Fig 5e) | grand-potential 산화 staircase: P₂S₇·S·폴리설파이드·LiCl (2.14–3.3 V) | **✓ 같은 화학 계열**(P-S 산화종·Li₂S). NCM 산소관여 sulfate/phosphate는 우리 6원소 hull서 부분만(Co 있는 LiCoO₂ proxy) |
| LZC=Li₂ZrCl₆ 산화안정성 | dual compatible, 7일 무분해 | (우리 hull에 Zr 無) | ✗ **범위 밖** — 우리 Cl-Li-Nd-O-P-S hull엔 Zr 없음. 별도 hull 필요 |
| 호환성 기전 | 금속 환원전위 trend(정성) | 우리 interface_reactivity(voltage-resolved, GrandPotentialInterfacialReactivity) | △ **우리 도구가 정량화 가능**(LZC-LPSCl·LZC-NCM hull 추가하면) |
| 계면저항 ↓ | 코팅 dual-compat → R_int 74.4→20.1 | 우리 onset(2.256 V)·분해 stoichiometry | △ 우리는 *어떤 산물*(thermo)만; *얼마나 저항성*(kinetic CEI)·코팅 효과는 device 스케일 |
| 할라이드 σ vs 성능 | σ(LIC 1.12) ≠ 성능(LZC 최고) | (우리 σ는 bulk AIMD) | **개념 평행**: device 성능 레버 = 계면 화학, bulk σ 아님 ([KimICCF]/[KimCA]와 동일 결) |

## 12. 적용 인사이트 (깊게)

1. **우리 그룹 cathode-interface 라인의 *기원(2024)***: 이 논문(Cha/Yun + Kang + **Jong-Won Lee** 2024) → kang2025(기생반응, 2025) → kang2026(intertwined 리뷰, 2026)으로 이어지는 **한양대 Jong-Won Lee 그룹 cathode-interface 3부작의 첫 편**. Junhee Kang이 세 논문 모두 참여. **우리 DFT가 이 라인의 atomistic 보강**.
2. **"dual compatibility" = 우리 interface_reactivity 도구의 *완벽한 적용 대상***: 우리 `GrandPotentialInterfacialReactivity`(voltage-resolved)는 **두 상의 계면 분해를 voltage별로 정량**한다. Cha의 LIC/LYC/LZC × {NCM, LPSCl} 6개 계면 호환성을 **우리 도구가 in-silico로 재현·예측 가능** → "왜 LZC만 dual compatible인가"를 grand-potential로 정량화하면 **우리 그룹 논문의 실험을 우리 DFT가 검증·확장**하는 강력한 스토리.
3. **σ≠성능 = 우리 "lever=interphase, not bulk" 결론의 *cathode-side 세 번째 증거***: [KimICCF](sheet σ=공동), [KimCA](양극 σ_e=코팅형상)에 이어 **Cha(계면저항=화학 호환성, σ 무관)** 추가. 세 우리 그룹 실험 모두 "bulk 잠재력이 아니라 계면·미세구조가 device 성능을 결정"으로 수렴.
4. **할라이드 코팅 = 우리 F-doping/oxyfluoride/Cl-rich와 *상보적인 다른 레버***: 우리 cascade(SE *bulk* 도핑으로 환원·산화 SEI 조작)와 Cha(별도 *할라이드 SE* 코팅으로 NCM-LPSCl 계면 차단)는 **다른 위치의 레버**. cascade=SE 자체, Cha=양극활물질 표면. **둘 다 "전자절연·호환 interphase가 핵심"엔 동의**(개념 정렬).
5. **분해산물 화학 대조(우리 XPS ref ↔ Cha XPS)**: Cha의 In₂S₃·Y₂S₃·LiCl·Li₂S·phosphate(P 2p 133.3 부근)·P₂Sₓ는 우리 `xps_reference_sei.csv`의 Li₂S(160.2)·LiCl(198.6)·Li₃PO₄(133.3)·thiophosphate(161.6)와 **직접 대조 가능** → 우리 XPS ref 테이블의 실험 검증.
6. **정직한 한계 = Zr hull 부재**: LZC(Li₂ZrCl₆) dual compatibility의 핵심인 Zr⁴⁺ passivation은 **우리 Cl-Li-Nd-O-P-S hull에 Zr 없어 못 봄**. 향후 Zr 포함 hull로 LZC-LPSCl·LZC-NCM interface reactivity 계산하면 정량화.

## 13. 인용 가능 문장 (deck/paper용)

- "Our group's earlier cathode-interface work (Cha et al., J. Power Sources 2024) shows that **a halide interfacial modifier must be *dual-compatible* — stable against both the NCM cathode and the Li₆PS₅Cl SE** — with Li₂ZrCl₆ uniquely satisfying this and lowering the interfacial resistance 74.4 → 20.1 Ω·cm²."
- "Across three of our group's experimental studies, **device performance tracks interfacial chemistry, not bulk ionic conductivity** — Cha's LIC has the highest σ (1.12 mS/cm) yet the worst cycling (80.8 %), because In is reduced by both NCM and LPSCl."
- "Cha's dual-compatibility result is the natural target for our voltage-resolved `GrandPotentialInterfacialReactivity` tool: the six halide×{NCM,LPSCl} interfaces can be screened in-silico to explain *why* only Zr⁴⁺ survives."

## 14. 주의/한계 (over-claim 방지)

- **DFT/계산 0** → 우리 DFT 수치와 직접 비교 금지. 개념·우리 그룹 trend·분해 화학 대조만.
- **Zr 우리 hull에 없음** → LZC dual compatibility는 우리 grand-potential로 *아직* 정량 못 함(향후 Zr hull).
- 호환성 기전("Zr⁴⁺ passivation", "In 환원")은 **정성적 환원전위 trend**일 뿐 — 논문 스스로 "chemical reaction ... is yet speculative" (LIC/LYC의 In-S/Y-S 형성)라고 명시. **확정 메커니즘 아님**.
- σ는 **할라이드 *분말* pellet** 측정(자체 σ), 양극 복합체 device σ 아님. r_ion(복합체)과 구분.
- NCM = LiNi₀.₈₃Co₀.₁₁Mn₀.₀₆O₂ **단결정** 특정 — 다른 NCM(다결정·조성)이면 계면화학·균열 거동 다를 수 있음.
- 100 cyc는 LZC만 full(NCM vs NCM@LZC); LIC/LYC는 retention 숫자(80.8/87.3 %)만(Fig S12).
- "interfacial modifier compatibility = crucial design factor"는 **이 NCM-LPSCl-할라이드 조합** 한정 결론.

## 15. 기법 용어 미니사전

- **dual compatibility(이중 호환성)**: 양극 복합체서 할라이드 코팅이 **NCM·LPSCl 두 상 모두**와 부반응 안 함. 이 논문의 핵심 설계 개념.
- **interfacial modifier(계면 수식제)**: 양극활물질 표면에 얇게 코팅해 SE와의 직접접촉·부반응을 막는 물질(여기선 할라이드 SE).
- **RAM (Resonant Acoustic Mixing)**: 공명 음향 가속(50G)으로 무용매 균일 코팅하는 공정(Resodyn).
- **TLM (transmission-line model)**: 다공성 복합전극 임피던스를 이온(r_ion)·계면(r_int)·확산(z_w) 저항으로 분해하는 등가회로.
- **할라이드 SE**: Li₃MCl₆ 류(M=In,Y,Zr…). 높은 σ(0.4–1.1 mS/cm) + 고전압 산화안정(>4 V) but Li 금속·환원에 약함·금속이온 비쌈.
- **LIC/LYC/LZC**: Li₃InCl₆ / Li₃YCl₆ / Li₂ZrCl₆.
- **single-crystalline NCM**: 단결정 양극(다결정 대비 입계 균열 적음) → 본 논문 열화원인을 "입자 균열 아닌 계면반응"으로 분리.
- **voltage sagging**: 1차 충전 시 부반응으로 셀전압이 처지는 현상(저항성 interphase 지표).
