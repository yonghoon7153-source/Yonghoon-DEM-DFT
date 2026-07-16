# ⭐필독 / 우리-랩 — Conflicting roles of conductive additives in controlling cathode performance in ASSBs — Cho, Yun, Kang, Kim, Lee (Electrochimica Acta 2024)

> slug `cho2024_conflicting_roles_conductive_additive` · DOI `10.1016/j.electacta.2024.143990` · type `exp + AC-impedance decoupling (modified TLM) + DC-polarization + XPS/CV` · PDF `Cho_2024_ElectrochimActa_ConflictingRoles_ConductiveAdditive_main.pdf` (+ `_SI.docx`) · digested `2026-06-26` · status ✅
>
> ## ★★★ 우리 랩(Hanyang, **Jong-Won Lee** 그룹) 자체 논문 — Kang 2025 의 reference [13] ★★★
> 저자 = **Minhyeong Cho, Jonghyeok Yun, Junhee Kang, Siwon Kim, Jong-Won Lee\*** (Division of Materials Science and
> Engineering, **Hanyang University**).  ★ **Junhee Kang, Siwon Kim 이 우리 랩의 다른 두 필독 논문과 공통 저자**:
> Junhee Kang ↔ `papers/kang2025_toughened_bimodal_nca_lzo.md`(역학/균열) + `papers/kim2025_impedance_decoupling_tlm_assb.md`(임피던스 분해);
> Siwon Kim ↔ Kim 2025(임피던스 분해)의 *제1저자*.  → 같은 그룹·같은 NCM811/LPSCl 계면을 **세 번째 렌즈로 본
> 자매 논문**(이번엔 *도전제(CA)의 양면성*).  이 논문은 **Kang & Shin 2025 의 reference [13]** 으로 인용됨.
>
> ★ **우리에게 왜 중요한가 (3줄):** (1) **CA(VGCF)의 σ_e↑(전자에 유익) vs σ_ion↓(이온망 차단·tortuous)의
> TRADE-OFF 를 AC-임피던스 *분해*로 정량** — 이게 정확히 우리 **σ_e ↔ σ_ion 경쟁** + Stage-2(VGCF) CBD 백로그
> A3/A4 의 실험 근거.  (2) **High-f_AM(88 wt%) = 우리 SE-poor 레짐**(mono-large/SE-poor porosity + wallP-conditional
> 작업) → 거기서 CA 가 *해롭다*(SE 망을 끊어 percolation 차단) = 우리 percolation/네트워크 솔버에서 CA = *이온망
> 장애물*.  (3) **같은 modified-TLM 분해 = Kim 2025 의 자매 방법론** + **Bielefeld 2020(바인더가 SE 망 차단)의
> 실험 카운터파트** + **AcceleDomain(Kim 2024 AFM, 카본 부피점유)와 짝** → 랩의 "**도전제는 양날의 검**" 테제.

---

## §0. ★ 이 논문의 위치 — "도전제 양면성" 테제 + 랩 자매 논문 지도 (이 절이 digest 의 핵심 framing)

### 0.1 한 줄 테제
**"1D 도전제(VGCF)는 f_AM(활물질 분율)에 따라 *상반된(conflicting)* 역할을 한다."**
- **Low-f_AM (72 wt%, SE-rich):** CA = **유익** → 전자저항(r_ele) ↓ → AM 이용률↑ → rate·용량 *향상*.
- **High-f_AM (88 wt%, SE-poor):** CA = **유해** → 전자는 잘 흐르나(r_ele 여전히 ↓), CA 가 *희박한 SE 망을
  끊어* 이온경로를 **tortuous** 하게 만들고 **AM/CA/SE 삼상 계면에서 SE 유래 저항성 상(PS₄³⁻ 분해산물)의 생성을
  가속** → 전자 유익이 **상쇄(nullify)** → rate-capability *열화* + 용량감쇠 *가속*.
→ **해결책:** 산화안정성이 높은 **할라이드 LZC(Li₂ZrCl₆)** SE 를 쓰면 high-f_AM 의 분해가 억제되어 CA 가 다시
  유익해진다 → "**CA-SE 호환성(compatibility)**이 핵심" (제목의 결론).

### 0.2 ★ 우리 모델축과의 1:1 대응 (이 논문이 채우는 칸)
| 이 논문이 보이는 것 | 우리 모델축 | 비고 |
|---|---|---|
| CA → r_ele 급감 (245→102, 166→51 Ω·cm) | **σ_electronic** (Stage 22.5) | CA = 전자 percolation 골격 (우리 σ_e 도전제 항) |
| CA → R_ion↑·tortuosity↑ (high-f_AM서 심함) | **σ_ionic** (Cronau·√φ·CN²·…) + **tortuosity** | ★ **CA = SE 이온망 장애물**(percolation 차단) |
| σ_e↑ vs σ_ion↓ **trade-off** | ★ **우리 σ_e ↔ σ_ion 경쟁** = backlog A3/A4 | 정확히 우리가 모델로 다투는 경쟁 |
| high-f_AM (88 wt%) = SE 희박 | ★ **우리 SE-poor 레짐**(mono-large/wallP-conditional) | CA 가 SE-poor 에서만 해롭다 = 레짐 의존 |
| 삼상(AM/CA/SE) 계면 분해 가속 | (우리 *미보유* — 화학 분해 kinetics) | frame[5] 빈 칸; Kim 2025·Kang 2025 의 분해 스토리 |
| tortuosity 6.47→18.34 (CA·high-f_AM) | **우리 tortuosity(τ) — σ_ionic C(τ) 항** | ★ 실험 τ 가 우리 τ-항 직접 앵커 |
| 할라이드 LZC 가 분해 완화 | (할라이드 = Varkey 2026 cross-check) | 안정하나 σ 낮음(0.6 vs 4.8) |

### 0.3 자매 논문 3종 — 같은 NCM811/LPSCl 계면, 세 렌즈 (랩 trend 지도)
| | **Kang & Shin 2025**(역학) | **Kim 2025**(kinetics) | **★ Cho 2024 (이 논문)**(도전제 양면성) |
|---|---|---|---|
| 공통저자 | Junhee Kang | Siwon Kim(1저), Junhee Kang | **Minhyeong Cho(1저), Junhee Kang, Siwon Kim** |
| 본다 | 사이클 중 *입계 균열*(NCA 다결정) | 정상상태 *임피던스 분해*(NCM811) | **도전제(CA)의 *조성 의존 양면성*(NCM811)** |
| 방법 | 실험 + 2D FEM(Voronoi+cohesive-zone) | 실험 + modified TLM(2 BC) | **실험 + modified TLM(Z-type) + DC-polarization + XPS/CV** |
| 계면분해 결과 | Li-구배 → **균열** | NCM811/LPSCl 분해 → **R_ct↑(uncoated ~20×)** | **삼상 계면 SE 분해 → R_ion↑·R_int↑(high-f_AM·CA)** |
| 처방 | LZO 6–8 nm 코팅 | LNO 코팅 / 할라이드 LZC | **할라이드 LZC(산화안정 SE)** |
| 도전제 | (안 다룸) | Super P(기본) vs VGCF(비교) | ★ **VGCF(1D) 가 주인공** |
> ★ **세 논문의 결론 통합:** 같은 황화물(LPSCl)/CAM 산화분해가 — Kang 에선 *역학*(균열), Kim 에선 *kinetics*(R_ct↑),
> Cho(이 논문)에선 *도전제 양면성*(삼상 계면에서 CA 가 분해를 가속 → R_ion·R_int↑) — **세 가지 손상 모드**로
> 나타난다.  우리 DEM+MPM 은 그 *구조→수송 σ* 를 채운다(structure-σ / mechanics=Kang / kinetics=Kim·Cho).

### 0.4 ★ AcceleDomain / Kim 2024 AFM(카본 부피점유)와의 짝
> 사용자 지시 — 이 논문은 **AcceleDomain 의 carbon 논문(Kim 2024, *Adv. Funct. Mater.*, "carbon volumetric
> occupation")과 짝**을 이룬다.  Kim 2024 = 카본이 *부피를 차지*해 활물질/SE 공간을 밀어내는 *기하/부피* 측면;
> 이 논문 Cho 2024 = 카본(CA)이 *이온망을 끊고 분해를 가속*하는 *전달/화학* 측면.  → 둘을 합치면 랩의
> **"conductive additive is a double-edged sword(양날의 검)"** 테제: 카본은 전자엔 좋지만 (i) *부피를 점유*하고
> (Kim 2024) (ii) *SE 이온망을 disconnect + 분해 촉진*한다(Cho 2024).  우리 σ_e/σ_ion 트레이드오프 + CBD 모델에
> 둘 다 반영해야 함(backlog A4 se_coating carbon).  ⚠ AcceleDomain/Kim 2024 AFM 은 *본 litdb 에 아직 미digest*
> (WISHLIST 후보) — 여기선 *짝 관계*만 명시.

---

## 1. 한 줄 요약
황화물 ASSB 복합 양극에서 **1D 도전제 VGCF 가 활물질 분율 f_AM 에 따라 상반된 역할**을 함을 **AC-임피던스 분해(modified
TLM 으로 R_ion / R_int 분리) + DC-polarization(r_ele) + XPS/CV**로 정량: **Low-f_AM(72 wt%)에서는 CA 가 전자저항을
낮춰 *유익***, **High-f_AM(88 wt%)에서는 CA 가 희박한 SE 이온망을 끊어 *이온경로를 tortuous* 하게 만들고 *삼상(AM/CA/SE)
계면에서 SE 분해를 가속* → 전자 유익을 *상쇄*하여 rate-capability 열화 + 용량감쇠 가속** → **할라이드 LZC(산화안정 SE)로
high-f_AM 의 분해를 억제하면 CA 가 다시 유익** → "**최적 전하경로 구축뿐 아니라 CA-SE *호환성*이 양극 성능을 좌우**".

---

## 2. 메타
| 항목 | 값 |
|---|---|
| 저자 | **Minhyeong Cho, Jonghyeok Yun, Junhee Kang, Siwon Kim, Jong-Won Lee\*** |
| 소속 | Division of Materials Science and Engineering, Hanyang University, 222 Wangsimni-ro, Seongdong-gu, Seoul 04763, Korea |
| 저널/년 | **Electrochimica Acta 481 (2024) 143990** |
| DOI | **10.1016/j.electacta.2024.143990** (Received 2023-12-10, revised 2024-02-13, accepted 2024-02-18, online 2024-02-19) |
| Keywords | All-solid-state battery · **Conductive additive** · Sulfide electrolyte · Composite electrode · Impedance |
| 소재 (CAM/SE/CA) | **CAM = NCM811 LiNi₀.₈Co₀.₁Mn₀.₁O₂** (polycrystalline, COSMO AM&T) · **SE = LPSCl Li₆PS₅Cl** (COSMO AM&T) · **CA = VGCF**(vapor-grown carbon fiber, 1D 미세 카본섬유, 高 aspect ratio, 低 비표면적 12.3 m²/g) |
| 추가 SE (할라이드) | **LZC = Li₂ZrCl₆** (LiCl + ZrCl₄ 를 600 rpm 3 h high-energy ball-mill → 260 °C 12 h annealing) |
| 활물질 분율 f_AM | **72 wt%(Low-f_AM, SE-rich)** 또는 **88 wt%(High-f_AM, SE-poor)** + **VGCF 2 wt%** 고정 |
| σ_ion (RT) | **LPSCl = 4.8 mS/cm**(Fig S1) · **LZC = 0.6 mS/cm**(Fig S2) |
| CA 비표면적 / 형상 | **12.3 m²/g**(N₂ 흡탈착, Fig S4) · 1D 고-aspect-ratio 섬유(SEM Fig S3) |
| 셀 | (a) **DC-polarization**: 이온차단 [SUS \| 복합양극 \| SUS] (전자저항 r_ele 측정); (b) **AC-impedance + cycling**: [In/Li \| LPSCl \| 복합양극], WE=복합양극, CE=In/Li |
| 압력 | separator LPSCl 100 mg **first poured/pressed**; 복합양극 10 mg(⌀10 mm) **433 MPa** 적층; 셀 작동 **stack pressure 250 MPa** |
| 측정 | EIS: Biologic SP-300, **7 MHz–30 mHz**, 5 mV.  CV: 2.5–4.3 V vs Li/Li⁺, 10 mV/s.  Cycling: 2.5–4.25 V, 30 °C, 1st 0.1C(CC-CV/CC, CV cutoff=1/5 적용전류), 이후 0.33C; rate 0.1–1.0C.  특성: FE-SEM(Verios G4UC), N₂ 흡탈착(AutoChem 2950), Raman(Almega XR), XPS(Al Kα 1486.6 eV, K-Alpha⁺) |
| 연구유형 | **실험**(DC-polarization r_ele + AC-impedance TLM 피팅 R_ion/R_int + rate/cycling + XPS/CV post-mortem) — *시뮬레이션 없음* |

---

## 3. 핵심 물성 (수치)

> ⚠ 이 논문은 *압밀 porosity 절대값*·*상대밀도*·*coordination*·*coverage*·*Heckel* 을 측정 목적이 아니다(임피던스·성능
> 논문).  단 ★ **porosity 와 tortuosity 는 Table S2 에 보고**(아래) — EIS 의 R_ion 을 SE 부피·경로로 해석하기 위한
> 값.  E_SE·σ_y·PSD 는 n/a.  ★ 모든 fitted 임피던스 값은 **SI Table S1 verbatim**; 본문 Fig 2d/3c 막대는 그
> 시각화, r_ele 는 Fig 2a/b 의 *기울기 라벨*(stated).

| 물성 | 값 | 조건 | stated/digitized | 비고 |
|---|---|---|---|---|
| **σ_ion (LPSCl)** | **4.8 mS/cm** | 황화물 SE, RT | stated (Fig S1) | ★ 우리 bulk 앵커 스프레드 *상단*(Cronau 단결정 3.0 보다 높음 — 측정·압력차) |
| **σ_ion (LZC 할라이드)** | **0.6 mS/cm** | 할라이드 SE, RT | stated (Fig S2) | LPSCl 의 ~1/8 (할라이드 = 낮은 σ, 높은 산화안정성) |
| **r_ele (전자저항/길이, Low-f_AM)** | w/o CA **245.0** Ω·cm → with CA **102.3** Ω·cm | DC-polarization, Ohm 법칙 | stated (Fig 2a) | ★ CA 가 r_ele **2.4× ↓**(전자 percolation 형성) |
| **r_ele (High-f_AM)** | w/o CA **166.2** Ω·cm → with CA **51.0** Ω·cm | 〃 | stated (Fig 2b) | ★ CA 가 r_ele **3.3× ↓** — high-f_AM 서 *전자에는* 더 효과적 |
| **R_ion (pristine, Low-f_AM)** | w/o CA **64.8** → with CA **80.9** Ω·cm² | AC-impedance TLM, pristine | stated (Table S1) | CA 추가 시 약간↑(+25 %) |
| **R_int (pristine, Low-f_AM)** | w/o CA **145.0** → with CA **175.2** Ω·cm² | 〃 | stated (Table S1) | 약간↑(+21 %) |
| **R_ion (pristine, High-f_AM)** | w/o CA **318.8** → with CA **402.5** Ω·cm² | 〃 | stated (Table S1) | ★ CA 가 R_ion **+26 %**(이온경로 차단) |
| **R_int (pristine, High-f_AM)** | w/o CA **241.1** → with CA **278.0** Ω·cm² | 〃 | stated (Table S1) | ★ CA 가 R_int **+15 %** — 둘 다↑ |
| **R_ion (cycled, High-f_AM)** | w/o CA **416.9** → with CA **780.9** Ω·cm² | AC-impedance, 100 cyc 후 | stated (Table S1, 본문) | ★★ **CA·high-f_AM: 402→781 (R_ion ~2× 폭증)** = 분해 누적 |
| **R_int (cycled, High-f_AM)** | w/o CA **490.3** → with CA **591.4** Ω·cm² | 〃 | stated (Table S1, 본문) | ★ 278→591 (R_int 2× 이상↑) |
| **R_ion (cycled, Low-f_AM)** | w/o CA **108.2** → with CA **140.1** Ω·cm² | 〃 | stated (Table S1) | low-f_AM 은 cycled 도 완만 |
| **R_int (cycled, Low-f_AM)** | w/o CA **285.1** → with CA **381.0** Ω·cm² | 〃 | stated (Table S1) | 〃 |
| **porosity (Low-f_AM)** | w/o CA **0.14** / with CA **0.15** | 복합양극 | stated (Table S2) | ★ CA 가 porosity 거의 안 바꿈(+0.01) |
| **porosity (High-f_AM)** | w/o CA **0.18** / with CA **0.19** | 〃 | stated (Table S2) | ★ **high-f_AM 이 더 porous**(SE 적어 충전율↓) = 우리 SE-poor floor↑ |
| **tortuosity (Low-f_AM)** | w/o CA **6.47** / with CA **7.56** | 〃 | stated (Table S2) | ★ CA 가 τ **+17 %**(이온경로 우회) |
| **tortuosity (High-f_AM)** | w/o CA **17.41** / with CA **18.34** | 〃 | stated (Table S2) | ★★ **high-f_AM τ 가 ~2.7× 큼**(17–18 vs 6–8) = 희박 SE 망 → 극도로 우회 |
| **Cap@1C / Low-f_AM** | CA-free **84.2** → with CA **119.5** mAh/g | rate, 1C | stated (본문) | ★ CA 가 용량 +42 %(유익) |
| **Normalized Cap (Cap_1C/Cap_0.1C), Low-f_AM** | w/o CA **~49 %** → with CA **~59 %** | Fig 1e | digitized (Fig 1e) | ★ CA 가 retention↑ |
| **Normalized Cap, High-f_AM** | w/o CA **~40 %** → with CA **~24 %** | Fig 1e | digitized (Fig 1e) | ★★ **CA 가 retention *반감*(유해)** |
| **초기 CE (High-f_AM, with CA)** | **72.4 %** (낮음) | 1st cycle | stated (본문) | ★ CA·high-f_AM 초기효율 저하 |
| **ΔV @ SOC50 %, Low-f_AM (1C)** | CA-free **0.88 V** → CA **0.73 V** | Fig 1f | stated (본문) | ★ CA 가 분극 ↓(유익) |
| **ΔV @ SOC50 %, High-f_AM (1C)** | CA-free **1.09 V** → CA **1.29 V** | Fig 1f | stated (본문) | ★★ **CA 가 분극 *증가*(유해)** |
| **AM loading** | f_AM 72 → **9.17 mg/cm²** · f_AM 88 → **11.21 mg/cm²** | 복합양극 | stated | — |
| **CV vol ratio (LPSCl:CA)** | **94:6**(low-f_AM 대응) · **79:21**(high-f_AM 대응) | CV/XPS 모델 | stated | XPS 분해 비교용 |
| E_SE / σ_y / ν | **n/a** (역학 미모델) | — | — | (E_LPSCl = 자매 Kang/Bazzoun 22.1 GPa) |
| coverage / coordination Z | **n/a** | — | — | 임피던스 논문 |
| Heckel / P_y | **n/a** | — | — | 압밀곡선 없음 |
| PSD (D10/D50/D90) | **n/a** (미보고) | — | — | NCM811·LPSCl 입경 명시 안 함 |

> ★ **bulk σ_ion(LPSCl) = 4.8 mS/cm** — 우리 LPSCl bulk 스프레드 {Cronau 단결정 3.0, Lee pristine 2.19, Kim2025/
> Minnmann 1.6, Bazzoun pellet 1.02} 의 *상단 이상*(4.8).  ⚠ 측정법·압력·셀 차로 절대 직접대조 금지, *범위*로만.
> 같은 랩 Kim 2025 는 1.6 이라 *동일 랩 내에서도 1.6↔4.8 의 스프레드* — 측정 셀/압력·SE 로트 차 (절대값 신뢰 말 것).

---

## 4. 시뮬레이션 방법 ★ — *없음* (이 논문은 순수 실험 + 등가회로 *피팅*)

> ★ 이 논문에는 **DEM / MPM / FEM / 입자 시뮬레이션이 없다.**  "모델"은 **AC-impedance 를 *modified TLM 등가회로*로
> 피팅**(Fig 2c 회로)하여 R_ion / R_int 를 분해하는 것뿐 — 자매 Kim 2025 의 TLM 분해와 *같은 방법론, 더 단순한 버전*
> (Kim 2025 = 2 BC × R_ion/R_int/C_dl/Warburg/온도; 이 논문 = 1 회로로 R_ion/R_int 분리 + r_ele 는 DC 로 별도).

### 4.1 modified TLM 등가회로 (Fig 2c) — 우리 Kirchhoff/Holm 솔버의 *실험 카운터파트*
복합 양극을 **분포 임피던스 요소의 네트워크**로 모델 (Fig 2c 회로 그림):
- **이온수송**: SE 상의 *분포 저항* `r_ion`(단위 길이당 [Ω·cm]) — 두께 방향 사다리.
- **계면 임피던스**: SE/NCM 계면의 **`r_int`(전하전달 R_int) + `cpe_int`(이중층 상수위상요소) + `z_w`(Warburg
  고상확산)** 병렬 — 세 과정(전하전달 / 이중층 충전 / NCM 입자 내 고상확산)을 표현.
- ★ **가정: 복합 양극의 *전자전도도는 충분히 높다*고 가정** → 회로엔 전자레일을 명시 안 넣고, **전자저항 r_ele 는
  DC-polarization 으로 *별도* 측정**(Fig 2a/b).  ⇒ 이 논문의 전략 = "**전자(DC r_ele) + 이온/계면(AC R_ion/R_int)을
  나눠 측정**" → CA 의 *전자 유익*과 *이온 유해*를 *분리*해서 보이는 핵심 트릭.
- 피팅 데이터: Fig 2d(pristine) / Fig 3c(cycled) 의 Nyquist → 회로 피팅 → **Table S1**(R₁/R_ion/R_int/R_w/CPE_int C/η).

### 4.2 DC-polarization 으로 r_ele 추출 (Fig 2a/b) — 전자저항만 고립
- **이온차단 셀** [SUS \| 복합양극 \| SUS] 에 여러 DC 전압(−0.5 ~ +0.5 V) 인가 → 정상상태 전류 측정 →
  **Ohm 법칙 기울기 = 단위 길이당 전자저항 r_ele [Ω·cm]**.
- 이온이 SUS 에서 차단되므로 전류는 *전자만* 흐름 → **순수 전자전도** 분리.
- 결과: CA 가 *low·high 양쪽 모두* r_ele 를 크게 낮춤(245→102, 166→51) → "**CA 는 전자수송에는 항상 효과적**"을 못박음
  → 따라서 high-f_AM 의 열화는 *전자 kinetics 탓이 아님*(본문 명시) → *이온·계면* 쪽 문제임을 논리적으로 좁힘.

### 4.3 입자 처리 ★ — *없음* (회로/실험 모델)
- ★ **입자 형상·PSD·rigid/plastic 개념이 없다.**  미세구조를 *명시적으로 생성하지 않고* 복합 양극을 **분포 임피던스
  사다리 + lumped r_ele** 로 추상화.  구조는 R_ion/R_int/r_ele/porosity/tortuosity 라는 *측정된 lumped 파라미터*로만
  들어온다.  ⇒ 우리 DEM(구·접촉망)·MPM(소성 형상)·Bazzoun(구 DEM)·Bielefeld(voxel)의 *구조* 차원이 이 논문엔
  없다 → **frame[5]:** 그들 = *측정/회로*, 우리 = *구조→σ*.

### 4.4 압력 구분
- separator LPSCl + 복합양극 적층 **433 MPa**(제조/압밀) ≠ 셀 작동 **stack pressure 250 MPa**.  우리 "제조 300 MPa ≠
  작동압" 인식과 합류(Minnmann 380·Doux 370·Kim2025 separator 433 와 같은 고압 압밀 계열).

---

## 5. 결과 상세 — Section-by-section (모든 수치)

### 5.1 §3 도입 — CA 의 양면 가능성 (Fig 1 SEM + rate)
**목적:** f_AM 72/88 wt% 두 전극 × CA 유무 4종을 만들어 CA 역할을 비교.
- **Fig 1a,b (SEM, CA 포함 low-/high-f_AM):** 두 조성 모두 NCM 균일 분포; 화살표가 VGCF(1D 섬유)를 표시.  high-f_AM 은
  NCM 입자가 더 빽빽 + SE 가 적어 *입자 간 SE 충전이 성김*(시각적).  Fig S5 = CA 없는 low/high-f_AM SEM(비교).
- **Fig 1c (Low-f_AM voltage profiles, 0.1–1C):** ★ **CA-incorporated(파랑) 가 CA-free(빨강)보다 *모든 rate 에서
  높은 용량***.  1C: CA-free **84.2** → CA **119.5 mAh/g**(+42 %).  → "**CA 가 AM 이용률을 높여 성능 향상**"(유익).
- **Fig 1d (High-f_AM voltage profiles):** ★ **CA-incorporated 가 *초기효율 낮고*(CE 72.4 %) *rate 증가 시 용량 급감***
  → CA-free 보다 *나쁨*.  CA-incorporated high-f_AM = 큰 분극.
- **Fig 1e (Normalized Cap = Cap_1C/Cap_0.1C):** ★★ **핵심 대조** —
  - Low-f_AM: w/o CA **~49 %** → with CA **~59 %** (CA 가 retention↑, *유익*).
  - High-f_AM: w/o CA **~40 %** → with CA **~24 %** (CA 가 retention *반감*, *유해*).
  ⇒ **CA 의 부호가 f_AM 으로 *뒤집힘*** = 제목의 "conflicting roles"의 직접 증거.
- **Fig 1f (ΔV @ SOC50 %, 0.1–1C):** ★ 분극 전압갭 —
  - Low-f_AM (1C): CA-free **0.88 V** → CA **0.73 V** (CA 가 분극 ↓, *유익*).
  - High-f_AM (1C): CA-free **1.09 V** → CA **1.29 V** (CA 가 분극 ↑, *유해*).
  ⇒ ΔV 도 f_AM 으로 부호 반전.

### 5.2 §3 DC-polarization (Fig 2a/b) — 전자는 *양쪽 다* CA 가 유익
- ★ **r_ele (Ohm 기울기):** Low-f_AM 245.0→102.3 Ω·cm; High-f_AM 166.2→51.0 Ω·cm.
- ⇒ **CA 가 low·high *모두* 전자저항을 크게 낮춤** → "**전자수송은 CA 가 항상 효과적; high-f_AM 열화는 전자 kinetics
  탓이 *아님***"(본문 명시).  → 논리적으로 high-f_AM 문제를 *이온·계면*으로 좁힘.
- (주: high-f_AM 의 r_ele 절대값(166)이 low-f_AM(245)보다 *낮은* 이유 = high-f_AM 은 NCM(전자전도 활물질)이 많아
  전자 percolation 이 본래 더 좋음 → CA 가 거기에 더해져 51 까지 떨어짐.)

### 5.3 §3 AC-impedance 분해 (Fig 2c–e) — 이온·계면은 high-f_AM·CA 에서 *동반 악화*
- **Fig 2c:** modified TLM 등가회로(§4.1).  **Fig 2d:** pristine Nyquist(low/high × CA).  **Fig 2e:** 피팅된
  R_int(Interfacial, 검정 막대) / R_ion(Ionic, 빗금 막대)를 4종에 대해 비교.
- ★ **pristine 추세 (Table S1):**
  - **Low-f_AM:** R_ion 64.8→80.9, R_int 145.0→175.2 (CA 가 *약간*↑, +21–25 %).
  - **High-f_AM:** R_ion 318.8→402.5, R_int 241.1→278.0 (CA 가 *둘 다 크게*↑).
  - ★ **본문 진술:** "high-f_AM 전극은 R_ion > R_int(이온저항이 계면보다 큼); CA 도입이 high-f_AM 의 *이온·계면
    저항을 모두 상당히 증가* → Fig 1d 의 rate-capability 열화를 설명"; low-f_AM 은 반대(R_int > R_ion, CA 영향 작음).
- ★ **tortuosity (Table S2):** Low 6.47→7.56, **High 17.41→18.34**.  → "**high-f_AM 의 tortuosity 가 훨씬 크고
  (~2.7×) CA 가 더 키운다**" = 희박한 SE 망에서 CA 가 *이온경로를 우회*시킴(percolation 차단).  porosity 는 거의
  불변(0.18→0.19) → **변한 건 *연결성(tortuosity)*이지 *공극량*이 아님** → CA 가 SE 망을 *끊는* 효과의 직접 지표.

### 5.4 §3 장기 cycling (Fig 3a/b) + cycled 임피던스 (Fig 3c) — 분해 누적
- **Fig 3a (Low-f_AM, 100 cyc, 0.33C):** ★ CA-incorporated 가 *높은 방전용량 + 유사한 retention 유지* → CA 유익 확인.
- **Fig 3b (High-f_AM, 100 cyc):** ★ CA-incorporated 가 *초기용량은 높으나 더 빠른 용량감쇠* → CA 유해 확인.
- **Fig 3c (cycled Nyquist + R_ion/R_int 막대):** ★★ **CA·high-f_AM 의 저항 폭증** (Table S1, 본문):
  - **R_ion 402.5 → 780.9 Ω·cm²** (100 cyc 후 ~2× 폭증).
  - **R_int 278.0 → 591.4 Ω·cm²** (~2.1× ↑).
  - ⇒ "**관측된 용량손실은 *주로 *열화된 이온경로·계면*에서 기인**"(본문) — 사이클 중 *이온·계면 저항이 누적 증가*.
  - (대조: low-f_AM cycled R_ion 108→140, R_int 285→381 = 완만; high-f_AM 만 폭증.)

### 5.5 §3 분해 화학 — CV + XPS (Fig 4) ★ 삼상 계면 SE 분해의 직접 증거
**목적:** high-f_AM·CA 의 저항 폭증의 *화학적 원인* = **CA 가 LPSCl 의 산화분해를 가속** 함을 CV·XPS 로 입증.
- **CV (Fig 4a, LPSCl:CA 부피비 94:6 vs 79:21):** ★ **CA 가 많은 79:21(=high-f_AM 대응)이 *전 전압영역에서 더 큰
  산화전류*** → "**CA-NCM 접촉↑ → LPSCl 분해↑**".  특히 79:21 은 *1st 사이클*에 큰 산화전류(분해) → 이후 감소(분해
  산물이 더 이상 분해 안 됨) = 비가역 계면분해.  94:6 은 분해 작음.
- **XPS (Fig 4b, S 2p / P 2p, CV 전후):**
  - pristine LPSCl: **S 2p PS₄³⁻ = 161.7 / 163.0 eV** (argyrodite 특성 peak).
  - **CV 후 새 signal:** **P₂Sₓ = 163.7 / 164.2 eV** + **Li₂Sₙ** + **PO₄³⁻ = 134.1 eV**(–OH/탄산염/수분 잔류와의
    부반응 산화종).  → **SE 가 PS₄³⁻ → P₂Sₓ + Li₂Sₙ + POₓ 로 분해**.
  - ★ **79:21(CA 多) 이 94:6 보다 *분해산물이 훨씬 많음*** → "**CA 가 high-f_AM 에서 LPSCl 의 *현저한 분해*를
    유발 → SE 유래 *저항성 상*이 이온수송·계면반응을 sluggish 하게 → 큰 R_ion·R_int 설명**"(본문).
- ⇒ ★ **메커니즘 확정:** CA(전자전도) 표면이 LPSCl(산화 한계 ~2.5 V 이하) 을 *전자적으로 산화 분해* → 분해산물(POₓ,
  P₂Sₓ, Li₂Sₙ)이 **AM/CA/SE 삼상 계면**에 저항성 층 형성 → 이온경로 막힘(R_ion↑) + 전하전달 방해(R_int↑).
  high-f_AM 은 SE 가 적어 이 분해층이 *희박한 이온망에 치명적*(percolation 끊김) → low-f_AM 은 SE 여유가 있어 완충.

### 5.6 §3 할라이드 LZC 해결책 (Fig 5) ★ Varkey 할라이드 cross-check
**목적:** 산화안정성 높은 **할라이드 LZC(Li₂ZrCl₆, > 4 V vs Li/Li⁺ 안정)** 로 LPSCl 을 대체 → high-f_AM·CA 의
분해/열화가 해소되는지 검증.
- **Fig 5a (High-f_AM + LZC, rate 0.1–1C, CA 유무):** ★ **CA-incorporated 가 *전 C-rate 에서 더 높은 용량*** →
  **LPSCl 일 때(Fig 1d)와 *반대*** = LZC 에서는 CA 가 다시 *유익*(전자 kinetics 향상이 살아남).
- **Fig 5b (High-f_AM + LZC, 100 cyc):** ★ CA 유무의 cycling 거동이 *거의 동일* → **CA 가 더 이상 용량감쇠를
  가속하지 않음**(LPSCl 의 빠른 감쇠가 사라짐).
- **Fig 5c (XPS Zr 3d / Cl 2p, CV 전후):** ★ **CV 후에도 Zr 3d(184/186 eV)·Cl 2p(198/200 eV) peak 이 *변화 없음***
  → "**LZC-CA 간 *유의한 부반응 없음***" = 할라이드는 CA 와 접촉해도 분해 안 됨.
- **Fig S8 (DC-polarization, high-f_AM + LZC):** CA 가 전자저항을 낮춤(LPSCl 과 동일한 전자 유익).
- ⇒ ★ **결론:** high-f_AM 의 CA 유해성은 *LPSCl 의 산화 불안정성* 탓 → **산화안정 SE(할라이드 LZC)로 바꾸면
  CA 가 다시 유익** → "**CA-SE 호환성이 핵심; CA 는 *전기화학적으로 안정한 SE* 와 짝지어야 high-f_AM 에서도
  전자·이온 둘 다 개선**"(제목 결론).  ⚠ 단 **LZC σ_ion 0.6 « LPSCl 4.8** → 할라이드는 *낮은 σ* 라는 대가
  (Fig 5a 절대용량은 LPSCl-low-f_AM 만큼 높진 않음).

### 5.7 §3 메커니즘 종합 (Fig 6 모식)
- **Fig 6 schematic:** CA 의 두 역할을 그림으로 —
  - **Low-f_AM:** SE 풍부 → CA 추가 = 전자망 형성 → AM 이용률↑ (이온망은 SE 여유로 무사) = **유익**.
  - **High-f_AM:** SE 희박 → CA 가 (i) **SE 이온망을 *disconnect*** + (ii) **SE 분해를 *촉진*** → 이온경로 tortuous +
    저항성 상 → 전하전달 방해 → 전자 유익을 **nullify** = **유해**.
- ★ 본문 마지막: "**고전도 + 전기화학적 안정성을 *둘 다* 갖춘 SE 와 CA 를 함께 쓰는 것이 전자/이온 수송·계면 kinetics
  를 모두 향상시키는 효과적 접근**".

---

## 6. Figure / Table set ★ (모든 그림·표 + 우리가 쓸 점)

### 6.1 본문 Figures
| Fig | 내용 (무엇을 보여주나) | 핵심 수치 | 우리가 참고할 점 |
|---|---|---|---|
| **1a,b** | CA 포함 low-/high-f_AM SEM (화살표=VGCF) | — | 미세구조 직관 (high-f_AM = NCM 빽빽·SE 성김) |
| **1c** | Low-f_AM voltage profile (0.1–1C, CA 유무) | 1C: 84.2→119.5 mAh/g | ★ CA 가 용량↑(유익) |
| **1d** | High-f_AM voltage profile | CE 72.4 %; 큰 분극 | ★ CA 가 rate·CE 저하(유해) |
| **1e** | Normalized Cap (Cap_1C/Cap_0.1C) 막대 | Low 49→59 %; High 40→24 % | ★★ **CA 부호 반전**(conflicting) |
| **1f** | ΔV @ SOC50 % (0.1–1C) 막대 | Low 1C 0.88→0.73; High 1C 1.09→1.29 V | ★ 분극갭 부호 반전 |
| **2a** | Low-f_AM DC-polarization (전류 vs 전압) | r_ele 245.0→102.3 Ω·cm | ★ CA 전자저항 2.4× ↓ |
| **2b** | High-f_AM DC-polarization | r_ele 166.2→51.0 Ω·cm | ★ CA 전자저항 3.3× ↓ (전자엔 항상 유익) |
| **2c** | modified TLM 등가회로 (r_ion, cpe_int, z_w) | — | ★ 우리 Kirchhoff/Holm 솔버의 임피던스판 |
| **2d** | pristine Nyquist (low/high × CA) | 1 kHz–1 Hz | 피팅 입력 |
| **2e** | pristine R_int/R_ion 막대 (4종) | High: R_ion 318.8→402.5; R_int 241.1→278.0 | ★ high-f_AM·CA 이온·계면 동반↑ |
| **3a** | Low-f_AM 100-cyc 용량/CE | CA 유익(용량↑ retention 유사) | ★ CA 유익 확인 |
| **3b** | High-f_AM 100-cyc 용량/CE | CA 유해(빠른 감쇠) | ★ CA 유해 확인 |
| **3c** | cycled Nyquist + R_ion/R_int 막대 | High·CA: R_ion 402→781; R_int 278→591 | ★★ 분해 누적 → 저항 폭증 |
| **4a** | CV (LPSCl:CA = 94:6 vs 79:21) | 79:21 이 큰 산화전류 | ★ CA 多 → LPSCl 분해↑ |
| **4b** | XPS S 2p / P 2p (CV 전후) | PS₄³⁻ 161.7/163.0 → +P₂Sₓ 163.7/164.2 +Li₂Sₙ +PO₄³⁻ 134.1 | ★ SE 분해 화학 증거 |
| **5a** | High-f_AM + LZC rate (CA 유무) | CA 가 *유익*(LPSCl 과 반대) | ★ 할라이드가 CA 유해성 해소 |
| **5b** | High-f_AM + LZC 100-cyc | CA 유무 거동 동일 | ★ 분해 가속 사라짐 |
| **5c** | XPS Zr 3d / Cl 2p (CV 전후) | 변화 없음 | ★ LZC-CA 부반응 없음 |
| **6** | CA 두 역할 모식 (low=유익/high=유해) | — | ★ 메커니즘 요약도 |

### 6.2 SI Figures & Tables
| 항목 | 내용 | 우리가 참고할 점 |
|---|---|---|
| **Fig S1** | LPSCl AC-impedance Nyquist | σ_ion 4.8 mS/cm 추출 |
| **Fig S2** | LZC AC-impedance Nyquist | σ_ion 0.6 mS/cm 추출 |
| **Fig S3** | VGCF SEM | 1D 고-aspect 섬유 형상 |
| **Fig S4** | VGCF N₂ 흡탈착 등온선 | 비표면적 12.3 m²/g (低 표면적 = 부반응↓) |
| **Fig S5** | CA 없는 low/high-f_AM SEM | CA 유무 미세구조 비교 |
| **Fig S6/S7** | low/high-f_AM voltage profile @0.33C (CA 유무) | cycling 전압거동 |
| **Fig S8** | High-f_AM + LZC DC-polarization | LZC 도 CA 전자저항↓ |
| **Fig S9** | High-f_AM + LZC voltage profile (CA 유무) | LZC cycling |
| **★ Table S1** | pristine·cycled fitted 임피던스 (R₁/R_ion/R_int/R_w/CPE_int/η) | ★ 우리 σ_ionic 앵커(아래 §6.3) |
| **★ Table S2** | porosity / tortuosity (4종) | ★ 우리 tortuosity τ-항 앵커 |

### 6.3 ★ SI Table S1 (fitted 임피던스 verbatim — 우리 정량 앵커) [Ω·cm² 단, R₁ 은 Ω·cm]
**Pristine**
| 조건 | R₁ (Ω·cm) | R_ion (Ω·cm²) | R_int (Ω·cm²) | R_w (Ω·cm²) | CPE_int C (mF·sᵑ⁻¹) | η |
|---|---|---|---|---|---|---|
| Low-f_AM w/o CA | 891.1 | **64.8** | **145.0** | 22.1 | 0.7 | 0.7 |
| Low-f_AM with CA | 926.0 | **80.9** | **175.2** | 18.3 | 1.1 | 0.5 |
| High-f_AM w/o CA | 1742.3 | **318.8** | **241.1** | 86.7 | 1.4 | 0.4 |
| High-f_AM with CA | 1747.6 | **402.5** | **278.0** | 64.5 | 4.8 | 0.7 |

**Cycled (100 cyc)**
| 조건 | R₁ (Ω·cm) | R_ion (Ω·cm²) | R_int (Ω·cm²) | R_w (Ω·cm²) | CPE_int C (mF·sᵑ⁻¹) | η |
|---|---|---|---|---|---|---|
| Low-f_AM w/o CA | 1244.8 | **108.2** | **285.1** | 28.7 | 0.7 | 0.7 |
| Low-f_AM with CA | 1370.2 | **140.1** | **381.0** | 27.6 | 1.2 | 0.4 |
| High-f_AM w/o CA | 2227.0 | **416.9** | **490.3** | 105.3 | 1.2 | 0.9 |
| High-f_AM with CA | 2013.5 | **780.9** | **591.4** | 41.9 | 3.6 | 0.7 |
> ★ 읽기: (1) **High-f_AM 이 모든 R 이 ~5× 큼** (R_ion 318.8 vs 64.8 = SE 적어 이온저항 큼).  (2) **CA 가 high-f_AM
> 에서 R_ion·R_int 둘 다↑**(pristine +26 %/+15 %; cycled 에선 R_ion 402→781 폭증).  (3) **R₁(직렬, separator+접촉)
> 도 high-f_AM 이 ~2× 큼**.  (4) **CPE_int C(이중층 용량) 가 high-f_AM·CA 에서 큼**(4.8 mF) = 분해층의 큰 계면 면적.
> ⇒ 이 표가 "CA 의 이온·계면 유해성"의 정량 결정체.

### 6.4 ★ SI Table S2 (porosity / tortuosity verbatim) — 우리 τ-항 직접 앵커
| 조건 | Porosity | Tortuosity |
|---|---|---|
| Low-f_AM w/o CA | **0.14** | **6.47** |
| Low-f_AM with CA | **0.15** | **7.56** |
| High-f_AM w/o CA | **0.18** | **17.41** |
| High-f_AM with CA | **0.19** | **18.34** |
> ★★ **핵심 해석:** CA 추가가 **porosity 는 +0.01 만**(거의 불변) 바꾸지만 **tortuosity 는 크게↑**(low +17 %,
> high +5 %; 그리고 high-f_AM 자체가 low 의 ~2.7×).  → "**CA 가 *공극량*이 아니라 *이온경로 연결성(τ)*을 악화*** =
> CA 가 SE percolation 망을 *끊는다*는 직접 증거".  ⚠ τ 산출법은 본문/SI 에 *명시 안 됨*(아마 R_ion·porosity·σ_bulk
> 로 역산한 *전기화학적 tortuosity* τ = σ_bulk·porosity·A/(R_ion·L) 류 — Bruggeman/Tortuosity-from-EIS).  절대값보다
> *추세*(CA·high-f_AM → τ↑)가 우리에게 유효.

---

## 7. ★ 메커니즘 — f_AM 의존 "상반된 역할"의 인과 사슬 (한눈에)

```
                    ┌─────────────── CA(VGCF) 추가 ───────────────┐
                    │                                              │
            [전자 효과: 항상 유익]                        [이온·계면 효과: f_AM 의존]
            r_ele ↓ (245→102, 166→51)                            │
                    │                            ┌────────────────┴────────────────┐
                    │                      Low-f_AM (SE 풍부)            High-f_AM (SE 희박)
                    │                      = SE 여유로 완충             = SE 망이 빈약
                    │                            │                         │
                    │                      R_ion·R_int 약간↑          (i) CA 가 SE 망 disconnect → τ↑(우회)
                    │                      τ 6.47→7.56               (ii) CA 가 LPSCl 산화분해 가속(삼상계면)
                    │                            │                        → POₓ/P₂Sₓ/Li₂Sₙ 저항성 상
                    │                            │                         │
                    │                            │                      R_ion·R_int 크게↑(402/278→cycled 781/591)
                    ▼                            ▼                         ▼
            전자 percolation↑              순효과: 유익                 순효과: 전자 유익이 *상쇄(nullify)*
                                          (용량↑, ΔV↓, retention↑)     (rate 열화, ΔV↑, 용량감쇠 가속)
                                                                          │
                                                                   해결: 산화안정 할라이드 LZC SE
                                                                   → 분해 사라짐 → CA 다시 유익
                                                                   (단 σ_ion 0.6 « 4.8 의 대가)
```
★ **요지:** CA 의 *전자 유익*은 f_AM 무관 상수, *이온·계면 유해*는 f_AM 과 SE 산화안정성에 의존 → **두 효과의
부호 합이 f_AM 으로 뒤집힌다**.  High-f_AM = 우리 **SE-poor 레짐**에서 이온망이 본래 빈약하므로 CA 의 망-차단 +
분해-가속이 *치명적*.

---

## 8. Post-processing ★
- **무엇:**
  - **DC-polarization → r_ele**: 이온차단 셀의 I-V 기울기(Ohm 법칙) → 단위길이 전자저항 [Ω·cm].
  - **modified TLM 등가회로 피팅 → R_ion / R_int 분해**: AC-impedance Nyquist(Fig 2d/3c)를 분포 임피던스 회로
    (r_ion + (r_int ∥ cpe_int ∥ z_w))로 피팅 → Table S1.  전자레일은 "전자전도 충분히 높다" 가정으로 생략(r_ele 는
    DC 로 별도) → **CA 의 전자 유익과 이온 유해를 *분리***.
  - **tortuosity / porosity (Table S2)**: 복합양극의 이온경로 우회도 τ + 공극률 φ (τ 산출법 미명시 — EIS-역산 추정).
  - **CV (2.5–4.3 V, 10 mV/s)**: LPSCl:CA 부피비(94:6, 79:21)별 산화전류 → CA 가 SE 분해를 얼마나 가속하는지.
  - **XPS (S 2p / P 2p / Zr 3d / Cl 2p, CV 전후)**: 분해산물(P₂Sₓ/Li₂Sₙ/POₓ) 동정 → LPSCl 분해 vs LZC 안정성.
  - **Raman / N₂ 흡탈착(BET)**: VGCF 표면적(12.3 m²/g) + 상 동정.
- **도구:** Biologic SP-300(EIS 7 MHz–30 mHz); FE-SEM Verios G4UC; AutoChem 2950(N₂); Nicolet Almega XR(Raman);
  K-Alpha⁺ XPS(Al Kα 1486.6 eV).  TLM 피팅 소프트 미명시(RELAXIS 류 추정).
- **수치화·기록:** 4종(f_AM 72/88 × CA 유무) + LZC 변형에 대해 r_ele / R_ion / R_int / R_w / CPE / porosity / τ +
  rate(Cap_1C/Cap_0.1C) + ΔV(SOC50 %) + cycling(100 cyc) 을 본문 Fig + Table S1/S2 로.

---

## 9. ★ 우리 DEM+MPM + 전달 파이프라인 대비  →  `our_dem_baseline.md`

> ⚠ **동시성 주의:** 본 절은 digest *안*에 작성 (INDEX.md/comparison_vs_ours.md 는 다른 에이전트가 편집 중 →
> 건드리지 않음).  메인 세션이 이 절을 보고 INDEX/comparison 에 반영.

| 항목 | 이 논문 (Cho 2024) | 우리 | 차이 / 이유 |
|---|---|---|---|
| **방법** | **실험 EIS(modified TLM) + DC-polarization + XPS/CV** | **DEM Kirchhoff/Holm σ-솔버** + Stage-E + MPM | ★ 목적 일부 같음(전달 σ 분해), 형식 다름 — 그들=측정/회로, 우리=구조→σ.  frame[4] 외부 검증 |
| **σ_electronic / r_ele** | ★ **CA → r_ele 급감 측정**(245→102, 166→51 Ω·cm) | σ_electronic *계산*(Stage 22.5, LOOCV 0.953); 도전제 항 | ★ **CA = 전자 percolation 골격** = 우리 σ_e 도전제 항의 실험 근거(backlog A4) |
| **σ_ionic / R_ion** | ★ **CA → R_ion↑ 측정**(high-f_AM 318.8→402.5; cycled 402→781) | σ_ionic *계산*(LOOCV 0.975) | ★ **같은 NCM811+LPSCl** → R_ion 이 우리 σ_ionic 앵커(wt%→φ_SE 매핑 후); ★ **CA = 이온망 장애물** |
| **tortuosity τ** | ★ **측정**(6.47/7.56/17.41/18.34) — CA·high-f_AM 서 ↑ | **우리 τ — σ_ionic C(τ) 항·percolation** | ★ **실험 τ 가 우리 C(τ) 항 직접 앵커**; CA → τ↑ = SE 망 disconnect(우리 percolation 차단) |
| **porosity** | 0.14/0.15/0.18/0.19 (high-f_AM 더 porous) | DEM 15.6 %·MPM 16.7 % (real_14) | ★ **high-f_AM(0.18–0.19) = 우리 SE-poor floor↑**(SE 적어 충전율↓); low-f_AM(0.14–0.15) ≈ 우리 15.6 % |
| **σ_e ↔ σ_ion trade-off** | ★ **CA 가 σ_e↑ BUT σ_ion↓**(high-f_AM) | ★ **우리 σ_e ↔ σ_ion 경쟁**(backlog A3/A4) | ★★ **정확히 우리가 모델로 다투는 경쟁** — CA = 전자 유익/이온 유해의 정량 실험 |
| **SE-poor 레짐** | **high-f_AM 88 wt% = SE 희박** → CA 유해 | **mono-large/SE-poor + wallP-conditional** 작업 | ★ **레짐 의존**: CA 가 SE-poor 에서만 해롭다 = 우리 SE-poor 코너의 물리(희박 이온망 민감) |
| **삼상 계면 분해** | ★ **CV/XPS 로 LPSCl 분해 가속 입증**(POₓ/P₂Sₓ/Li₂Sₙ) | (우리 *미보유* — 화학 분해 kinetics) | ★ frame[5] 빈 칸; Kim 2025 R_ct↑·Kang 2025 균열의 *도전제* 버전 |
| **R_int (=R_ct)** | ★ **분해·측정**(pristine 175–278, cycled 381–591) | ★ **우리 미보유**(constriction-only) | ★ 계면 전하전달 = 우리 σ-솔버 밖(Kim 2025 와 같은 빈 칸) |
| **할라이드(LZC)** | σ_ion 0.6(낮음) BUT 분해 없음(CA 와 호환) | (할라이드 미모델; Varkey 2026 cross-ref) | ★ Varkey 할라이드(압밀/σ) ↔ 이 논문 할라이드(CA 호환성) = 같은 "안정하나 σ 낮음" |
| **도전제 형상** | **1D VGCF**(고-aspect, 低 표면적 12.3 m²/g) | 우리 production = Super P(0D) 가정; σ_e 형상 구분 약함 | ★ Lee 2025·Kim 2025 VGCF 와 합류; 1D = 효율적 전자망 + 低 표면적(부반응↓) |
| **소성/morphology** | 없음(회로/실험) | MPM 진짜 SHAPE 소성 | 우리 MPM 고유(frame[5]) |

**핵심 정합/상보 4가지:**
1. **σ_e↑ vs σ_ion↓ trade-off = 우리 σ_e ↔ σ_ion 경쟁(backlog A3/A4)** — CA 가 전자엔 유익(r_ele 2–3×↓)·이온엔
   유해(R_ion·τ↑, high-f_AM)인 *부호 대립*을 실험으로 정량 → 우리가 모델로 다투는 바로 그 경쟁의 실험 앵커.
2. **High-f_AM(88 wt%) = 우리 SE-poor 레짐** — porosity 0.18–0.19·τ 17–18 = SE 희박 코너; CA 유해성은 *이 레짐에서만*
   = 우리 mono-large/SE-poor·wallP-conditional 작업의 물리(희박 이온망이 disconnect 에 민감).
3. **tortuosity 실험값(6.47→18.34)이 우리 C(τ) 항·percolation 의 직접 앵커** — CA → τ↑(공극 불변, 연결성만 악화) =
   percolation 망 차단의 정량 지표.
4. **삼상 계면 SE 분해·R_int = 우리 *미보유* 칸(frame[5])** — Kim 2025 R_ct↑·Kang 2025 균열과 함께 "황화물-계면
   산화분해"의 *세 번째 손상모드*(도전제 매개).

---

## 10. 적용 인사이트 (내 연구에 어떻게) — ★ 우리 랩 trend 정렬

- ① **σ_e ↔ σ_ion trade-off 의 실험 앵커로 (backlog A3/A4 직결)**:
  CA(VGCF) 가 r_ele 를 2–3× 낮추면서(전자 유익) 동시에 R_ion·τ 를 올린다(이온 유해, high-f_AM)는 4종 데이터 →
  우리 **σ_e 도전제 항(Stage 22.5)** 과 **σ_ionic τ-항** 이 *반대 부호로 CA 에 반응*해야 함을 확증.  ★ 특히
  **high-f_AM 에서 CA 가 σ_ion 을 *악화*** = 우리가 CBD/도전제를 모델에 넣을 때 *SE-poor 에서 전자이득이 이온손실로
  상쇄됨*을 반영해야.  → `docs/data/cho2024_conflicting_roles_conductive_additive.csv`(f_AM·CA·r_ele·R_ion·R_int·τ·
  porosity·rate·σ_ion).

- ② **High-f_AM = 우리 SE-poor 코너의 실험 카운터파트 (regime-gate 정당화)**:
  porosity 0.18–0.19·τ 17–18(high) vs 0.14–0.15·τ 6–8(low) → **SE 분율이 임계 아래로 가면 이온망이 빈약·우회적**
  이 됨을 실험으로 못박음.  우리 `docs/mpm_scaffold_reliability_and_am_freeze.md` 의 **SE-poor/mono-large 코너에서
  모델 신뢰성이 갈라지는 물리**(희박 이온망)와 동일 → CA 가 그 코너를 더 악화시킴을 추가.

- ③ **tortuosity τ 를 우리 σ_ionic 에 *CA-의존*으로 (흡수 후보)**:
  실험 τ 가 CA 추가 시 ↑(porosity 불변) → 우리 C(τ) 항에 "CA(도전제 부피·망간섭) → τ↑" 경로를 넣을 근거.  특히
  **CA 가 *공극이 아니라 연결성*을 악화**시키는 건 우리 percolation/network 솔버에서 *CA 를 이온-비전도 장애물 입자로
  넣으면 τ↑·CN↓* 로 자연 재현될 것(검증 후보) → DEM 에 CA 입자(이온 비전도)를 추가하면 Bielefeld(바인더 차단)와 같은
  효과.

- ④ **삼상 계면 분해·R_int = frame[5] 의 *새 빈 칸* 명문화 (Kim 2025·Kang 2025 와 통합)**:
  우리 σ-솔버는 *수송 σ* 만; **CA 매개 SE 산화분해 → 저항성 상 → R_int↑** 은 우리가 *전혀* 안 다룬다.  → `our_dem_
  baseline.md §4` 에 "**도전제-매개 계면 분해 kinetics = 우리 transport 솔버 밖, EIS-TLM(Cho/Kim) 영역**" 추가.
  Kang(균열)·Kim(R_ct↑)·Cho(CA 분해)를 **랩의 *계면 분해 3-모드***로 묶어 deck 에.

- ⑤ **AcceleDomain(Kim 2024, 카본 부피점유)와 짝 → CBD 모델 양날 반영 (backlog A4 se_coating carbon)**:
  Kim 2024 = 카본이 *부피 점유*(기하); 이 논문 = 카본이 *이온망 disconnect + 분해 가속*(전달/화학).  → 우리 CBD/
  Stage-2 VGCF 모델은 **카본을 (i) 부피 점유체 + (ii) 이온-비전도 장애물 + (iii) (LPSCl 과) 분해 촉진체**로 *셋 다*
  취급해야 "도전제는 양날의 검"을 온전히 재현.  단순히 σ_e 만 올리는 도전제로 넣으면 *high-f_AM 의 이온 손실*을 놓침.

- ⑥ **할라이드(LZC) CA 호환성 ↔ Varkey 할라이드 압밀 통합 (cross-ref)**:
  이 논문 LZC = "낮은 σ(0.6) BUT CA 와 분해 안 함(호환)"; Varkey 할라이드 = "stiffer E(10.58) → 높은 porosity floor".
  → **할라이드 = 압밀(Varkey)·CA 호환성(Cho)·kinetics(Kim LZC) 모두 황화물과 다른 trade-off**.  우리가 할라이드로
  확장하면 E·σ·R_ct·CA호환 모두 재보정.

- ⑦ **도전제 형상(1D VGCF, 低 표면적) → 우리 σ_e 형상 항 (Lee 2025·Kim 2025 와 합류)**:
  VGCF = 1D 고-aspect(효율적 전자 percolation) + 低 비표면적 12.3 m²/g(SE 접촉면적↓ → 분해 시작점↓).  → 우리 σ_e
  도전제 항이 *형상(0D/1D)·비표면적* 의존임을 보강(Super P 0D 가정 한계).  ★ 단 이 논문은 VGCF 조차 high-f_AM 에선
  유해 → "**1D 라도 SE 가 희박하면 망 차단·분해는 못 피함**" = 형상보다 *SE 호환성·분율*이 우선.

---

## 11. 인용 가능 문장 (deck/paper용)

- "Our group's work (Cho, Yun, Kang, Kim, Lee, Electrochim. Acta 2024) shows that a 1D conductive additive (VGCF)
  plays **conflicting, AM-fraction-dependent roles** in sulfide ASSB cathodes: at low f_AM (72 wt%) it lowers the
  electronic resistance (r_ele 245→102 Ω·cm) and improves rate/capacity, but at high f_AM (88 wt%) it makes the
  ionic pathway tortuous and **accelerates the formation of SE-derived resistive phases at the three-phase
  AM/CA/SE interface**, nullifying the electronic benefit — the experimental embodiment of the σ_electronic ↔
  σ_ionic trade-off our transport solver models."

- "Impedance decoupling (DC-polarization for r_ele + modified-TLM AC fitting for R_ion/R_int) demonstrates that
  the additive's electronic benefit is f_AM-independent (r_ele drops 2–3×) whereas its ionic/interfacial penalty
  is confined to the SE-poor regime: at 88 wt% AM the CA raises R_ion (318.8→402.5 Ω·cm² pristine, 402→781 after
  100 cycles) and tortuosity (17.4→18.3) while porosity is unchanged — i.e. it disconnects the SE percolation
  network rather than reducing pore volume."

- "The conductive additive's harm at high f_AM is an electrolyte-stability problem: replacing the sulfide LPSCl
  with the oxidation-stable halide Li₂ZrCl₆ removes the CV/XPS decomposition signatures (P₂Sₓ, Li₂Sₙ, POₓ) and
  restores the CA's beneficial role — establishing **CA–SE compatibility**, not the additive itself, as the
  controlling variable (cf. our halide cross-check with Varkey 2026)."

- "This paper pairs with our group's impedance-decoupling study (Kim 2025, same modified-TLM method) and the
  cracking study (Kang & Shin 2025): the same sulfide-interface oxidative decomposition manifests as a tortuous
  ionic path + R_int rise (Cho 2024, additive-mediated), an interfacial charge-transfer rise (Kim 2025), and
  intergranular cracking (Kang 2025) — three damage modes of one chemistry that our DEM+MPM fills on the
  structure→transport-σ side."

---

## 12. 주의/한계 (over-claim 방지)

- **순수 *실험* 논문 — 시뮬레이션 없음.**  DEM/MPM/FEM/입자 모델이 *없다*.  "모델"은 AC-impedance 의 modified-TLM
  *피팅*(R_ion/R_int 분해)뿐.  우리 구조→σ 솔버와 *방법이 다름*(그들=주파수영역 회로 피팅, 우리=공간 저항망 DC) →
  frame[4] **외부 검증**이지 *경쟁 솔버* 아님.
- **R_ion/R_int/r_ele 는 *측정+피팅* 값** → *예측 솔버* 산출 아님.  우리 σ(계산)과 비교 시 "그들=실험 진실, 우리=
  구조 예측"(frame[4]).  ⚠ **조성 wt%→φ_SE 매핑 선행**: f_AM 72 wt%(=NCM 72 : SE 26 : CA 2) / 88 wt% 를 vol%
  (NCM ~4.77, LPSCl ~1.64 g/cm³)로 환산해야 우리 φ_SE 와 비교 가능.  대략 72 wt% ≈ φ_SE 0.45 수준, 88 wt% ≈
  φ_SE 0.15–0.20(SE-poor).
- **CAM = NCM811** (= 우리 production, Kang 2025 의 NCA 와 다름) → *우리 소재와 정확히 일치*.  단 **NCM811 grade·
  입경**이 우리 시뮬 가정과 다를 수 있어 R_ion 절대값은 "같은 LPSCl + 같은 NCM811 계열" 수준 정합으로 (PSD 미보고 →
  우리 12:4:1 가정과 직접 매칭 불가).
- **porosity/tortuosity 는 보고하나 *압밀곡선·Heckel·coordination·coverage·E_SE 는 n/a*.**  porosity 0.14–0.19 는
  우리 DEM 15.6 %·MPM 16.7 %(real_14)와 *대략* 비교 가능(low-f_AM ≈ 우리)이나 **압밀 메커니즘/Heckel 직접 비교 금지**.
- **tortuosity 절대값 = 산출법 미명시** → §6.4 의 τ(6.47–18.34)는 *EIS-역산 전기화학 τ* 추정.  절대값보다 **추세**
  (CA·high-f_AM → τ↑)만 우리에게 유효.  우리 기하 τ(Dijkstra/Laplace)와 *정의가 다를 수 있음*.
- **R_int(=R_ct)·CPE_int(C_dl)·R_w(Warburg) = 우리 *미보유* 칸** → 이걸 우리 σ-솔버가 "재현/검증"한다고 말하면 *틀림*.
  우리는 이온수송 σ 만 계산 → 계면반응·확산은 우리 모델 밖(frame[5] 빈 칸).  "우리가 cross-validate"가 아니라
  "우리가 *안 갖는* 것을 실험이 보여줌"으로 정직하게.
- **σ_ion(LPSCl) = 4.8 mS/cm** 은 우리 bulk 스프레드 *상단 이상*(Cronau 3.0, 같은 랩 Kim2025 는 1.6).  ⚠ **같은 랩
  내에서도 1.6↔4.8** = 측정셀/압력/SE 로트 차 → 절대 직접대조 금지, 범위로만.
- **Fig 1e/1f 막대값(49/59/40/24 %, 0.88/0.73/1.09/1.29 V)** 중 일부는 *digitized*(그림에서 읽음) — 84.2/119.5 mAh/g·
  CE 72.4 %·r_ele·R_ion/R_int 는 stated.  digitized 는 *추세*만.
- **CV 부피비(94:6, 79:21)** 는 *순수 LPSCl:CA 모델 복합체*(NCM 없는 분해 비교용)이지 실제 전극 조성(f_AM 72/88)과
  *직접 동일은 아님* — high-f_AM 의 CA-rich 환경을 *모사*한 것.  XPS 분해 결론은 정성·상대(79:21 ≫ 94:6).
- **할라이드(LZC) 의 정량 임피던스 표는 본 추출에 없음**(Fig 5 는 rate/cycling/XPS) → "LZC 가 CA 와 호환·분해 없음"은
  XPS(Zr/Cl 불변)·rate(CA 유익 회복) 기반 *정성*.  LZC σ_ion 0.6 만 stated.

---

## 13. 미니 용어집 (technique glossary)

- **conductive additive (CA) / VGCF** — 전자전도를 위해 복합양극에 넣는 탄소.  **VGCF = vapor-grown carbon fiber**,
  1D 고-aspect-ratio 미세 탄소섬유.  카본블랙(0D)보다 *상호연결성↑·표면결함↓*(Ates et al.) → SE 와의 부반응이 적음.
- **f_AM (active-material fraction)** — 복합양극 내 활물질(NCM) 무게분율.  ★ 이 논문의 *제어변수*: 72 wt%(low, SE-rich)
  vs 88 wt%(high, SE-poor).  high-f_AM = SE 가 적어 이온망이 빈약 = 우리 **SE-poor 레짐**.
- **r_ele (electronic resistance per length)** — 이온차단(SUS) 셀의 DC I-V 기울기에서 Ohm 법칙으로 얻는 단위길이당
  전자저항 [Ω·cm].  CA 가 낮춤(전자 percolation).
- **R_ion (ionic resistance)** — modified-TLM 피팅으로 분해한 SE 상의 이온수송 저항 [Ω·cm²].  ★ 우리 σ_ionic 의
  실험 카운터파트.
- **R_int (interfacial / charge-transfer resistance, = R_ct)** — SE/NCM 계면의 전하전달 저항 [Ω·cm²].  분해층이
  두꺼우면 급증.  ★ 우리 *미보유*.
- **modified TLM (transmission line model)** — 다공·복합 매질의 *분포* 임피던스 모델.  이온 레일을 무한개 미소 RC
  요소 사다리로 짜고 계면(r_int ∥ cpe_int ∥ z_w)으로 결합.  "modified" = GB·Warburg·전하전달 요소 추가.  Kim 2025 의
  방법과 동일(이 논문은 더 단순 버전 + DC r_ele 별도).
- **CPE_int (constant-phase element)** — 계면 이중층 용량의 *비이상* 표현(지수 η<1 = 비균질 계면) [mF·sᵑ⁻¹].
- **Warburg (R_w)** — 활물질 내 *고상 Li 확산* 임피던스 [Ω·cm²].
- **tortuosity (τ)** — 이온이 SE 망을 *우회*하는 정도(직선 대비 경로 길이비).  ★ CA·high-f_AM 서 ↑ = 망 disconnect.
  porosity 불변에 τ↑ = *공극은 그대로인데 연결성만 악화* = percolation 차단의 지표.
- **three-phase interface (AM/CA/SE)** — 활물질·도전제·전해질이 만나는 삼상 접점.  ★ 여기서 CA(전자) 가 LPSCl(이온)을
  *전자적으로 산화 분해* → 저항성 상.
- **oxidative decomposition (LPSCl)** — 황화물 SE 가 고전압·전자접촉에서 PS₄³⁻ → P₂Sₓ + Li₂Sₙ + POₓ 로 분해(XPS).
  → 저항성 상 형성 → R_ion·R_int↑.
- **LZC (Li₂ZrCl₆)** — 할라이드 SE.  낮은 σ_ion(0.6) BUT 높은 산화안정성(> 4 V) → CA 와 분해 안 함(호환).
- **normalized capacity (Cap_1C/Cap_0.1C)** — rate-capability 지표.  1C/0.1C 용량비(%) = 고율 유지율.  ★ CA 부호가
  f_AM 으로 반전(low 49→59 %, high 40→24 %).
- **ΔV @ SOC50 %** — 충방전 곡선의 50 % SOC 에서의 전압갭(분극).  작을수록 좋음.  ★ CA 부호 반전(low ↓, high ↑).

---

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
