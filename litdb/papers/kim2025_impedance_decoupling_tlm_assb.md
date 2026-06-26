# ⭐필독 / 우리-랩 — Multiple-reaction kinetics of composite electrodes for sulfide-based ASSBs: Impedance decoupling (modified TLM) — Kim, Kang, Park, Lee (Electrochimica Acta 2025)

> slug `kim2025_impedance_decoupling_tlm_assb` · DOI `10.1016/j.electacta.2025.147413` · type `exp + equivalent-circuit modeling (modified TLM)` · PDF `Kim_2025_ElectrochimActa_ImpedanceDecoupling_TLM_main.pdf` (+ `_SI.docx`) · digested `2026-06-26` · status ✅
>
> ## ★★★ 우리 랩(Hanyang, **Jong-Won Lee** 그룹) 자체 논문 — EIS-TLM 임피던스 *분해*의 방법론 기준점 ★★★
> 저자 = **Siwon Kim, Junhee Kang, Jae Hyun Park, Jong-Won Lee\*** (Division of Materials Science and
> Engineering + Department of Battery Engineering, **Hanyang University**).  **Junhee Kang 이 우리 랩의
> 다른 필독 논문 Kang & Shin 2025**(`papers/kang2025_toughened_bimodal_nca_lzo.md`)**과 공통 저자** →
> 같은 그룹·같은 NCM/LPSCl 계면을 **다른 렌즈로 본 자매 논문**.  Kang 2025 = *역학/균열*(FEM cohesive-zone,
> bimodal 패킹 대가), 이 논문 = *임피던스/반응속도*(modified TLM 으로 R_ion / R_ct / C_dl / 확산을 *분해*).
> **두 논문이 NCA/NCM–LPSCl 계면을 mechanics(Kang) ↔ kinetics(Kim) 로 함께 묶는다.**
>
> ★ **우리에게 왜 중요한가 (3줄):** (1) **modified TLM 임피던스 분해 = 우리 네트워크 솔버(Kirchhoff+Holm)의
> 실험 카운터파트** — 그들이 *측정/분해*하는 R_ion / R_int(=R_ct) / C_dl / 확산(Warburg)을 우리는 *구조적으로
> 계산*(σ_ionic 파이프라인).  **Bazzoun 2026·Minnmann 2021 에 이은 세 번째 TLM 앵커이자 SAME LAB**. (2)
> **NCM811 + LPSCl = 우리 정확한 production 소재계** → 그들 R_ion/τ 가 우리 σ_ionic 직접 실험 앵커(조성 wt%
> 62:37/72:27/82:17 ↔ 우리 φ_SE 매핑). (3) **활성화에너지(온도 스윕 30/45/60 °C)·전하전달 R_ct·이중층 C_dl =
> 우리가 *전혀* 안 갖는 축** → T-의존 σ + R_ct 가 우리 *constriction-only* 솔버가 못 잡는 실험 과정임을 명시.

---

## §0. ★ 이 논문의 위치 — TLM 세 번째 앵커 + 자매 논문 링크 (이 절이 digest의 핵심 framing)

### 0.1 TLM 앵커 3종 (우리가 가진 EIS-TLM 실험 근거의 전체 지도)
| 논문 | 그룹 | 소재 | TLM 이 *분해*하는 것 | 우리에게 |
|---|---|---|---|---|
| **Minnmann 2021 JES** | Janek (Giessen) | NCM-622 + LPSCl | σ_ion,eff / σ_el,eff / **τ²** (T-type TLM, 이온·전자 차단 셀) | porosity 14 %·σ_ion 0.17·τ_ion 2.07 앵커 출처 |
| **Bazzoun 2026 JPS** | Mercedes/Stuttgart | NMC811 + LPSCl | R_ion → σ_eff,ion (Z-type TLM, full-blocking) + DEM→RNM 솔버 | σ_eff,ion 0.137/0.101/0.065 절대 앵커 + 같은 Holm/Kirchhoff |
| **★ Kim 2025 (이 논문)** | **Lee (Hanyang, 우리 랩)** | **NCM811 + LPSCl** + 할라이드 LZC | **R_ion / R_int(=R_ct) / C_dl(CPE_int) / 고상확산(Warburg) 을 *동시* 분해** | ★ **R_ion+R_ct+C_dl+확산 *동시* 분해 + T-의존 E_a** — 가장 완전한 kinetic 분해 + SAME LAB |
> ★ Minnmann/Bazzoun 은 주로 **이온/전자 *수송* σ** 를 줌.  이 논문은 거기에 **계면 *전하전달* R_int(=R_ct),
> *이중층* C_dl, *고상확산* Warburg 까지 한 회로에서 분해** + **활성화에너지(온도 스윕)** 까지 줘서,
> EIS-TLM 분해의 가장 완전한 버전이다 (그래서 "multiple-reaction kinetics" 제목).  우리 솔버는 σ_ionic 의
> *수송* 부분만 계산 → **R_ct·C_dl·확산은 우리 미보유 칸**임을 이 논문이 정확히 짚어 준다.

### 0.2 자매 논문 (Kang 2025) ↔ 이 논문 — 같은 NCM/NCA–LPSCl 계면, 두 렌즈
| | **Kang & Shin 2025** (역학) | **Kim 2025** (이 논문, kinetics) |
|---|---|---|
| 본다 | 사이클 중 *입계 균열* (NCA 다결정) | 정상상태 *임피던스 분해* (NCM811) |
| 방법 | 실험 + **2D FEM** (Voronoi + cohesive-zone damage) | 실험 + **modified TLM** (분포 임피던스 회로) |
| 계면 | NCA/LPSCl 분해 → Li-구배 → **균열** | NCM811/LPSCl 분해 → **R_ct(전하전달저항) 급증** |
| 코팅 | **LZO 6–8 nm**(화학 패시베이션) | **LNO**(LiNbO₃) 코팅 vs **uncoated** 비교 |
| 같은 계면의 결론 | 분해가 *역학적* 손상(균열)을 만든다 | 분해가 *전기화학적* 손상(R_ct↑)을 만든다 |
> ★ **핵심 연결:** Kang 2025 가 **"NCA/LPSCl 계면분해 → Li 농도·응력 구배 → 큰 입자 균열"**(역학)이라면,
> 이 논문은 **"NCM811/LPSCl 계면분해 → 전하전달저항 R_int 급증(uncoated 가 LNO-coated 의 수 배)"**(kinetics)이다.
> **둘은 같은 황화물-계면 산화분해의 mechanics-side(Kang) 와 kinetics-side(Kim)** — 한 논문은 그게 *깨짐*으로,
> 다른 논문은 그게 *느린 반응(R_ct↑)* 으로 나타남을 보인다.  랩이 이 계면을 *입체적*으로 공략 중임을 보여줌.

---

## 1. 한 줄 요약
ASSB 복합 양극의 임피던스를 **분포 임피던스 요소들로 짠 modified TLM(transmission line model)**으로
모델링해 — 두 레일(이온/전자)이 crossrail(계면)에서 결합하는 사다리 회로 — **Li⁺/전자 수송, 계면 전하전달
R_int(=R_ct), 이중층 충전 C_dl, 활물질 내 고상확산(Warburg)을 *한 번에 분해(decouple)*** 한다.  **두 경계조건
(ion-blocking/ion-blocking 과 electron-blocking/ion-blocking)** 으로 각 회로요소가 어느 전기화학 과정에
대응하는지를 model simulation 으로 보인 뒤, **대칭셀 + 3-전극 풀셀**(Ag–Li 합금 기준전극)의 EIS 를
**조성(62/72/82 wt% NCM811) 과 온도(30/45/60 °C)** 함수로 측정해 R_ion·R_int·C_dl·D_s 를 추출하고, **이온수송
vs 계면반응의 활성화에너지**를 분리하며, **할라이드(LZC) vs 황화물(LPSCl)** 의 계면 안정성 차이까지 정량화한다.
→ "**복합 양극에서 여러 반응속도를 임피던스로 분해하는 정량 가이드라인**".

---

## 2. 메타
| 항목 | 값 |
|---|---|
| 저자 | **Siwon Kim**ᵃ, **Junhee Kang**ᵃ, **Jae Hyun Park**ᵇ, **Jong-Won Lee**\*ᵃ,ᵇ |
| 소속 | ᵃ Division of Materials Science and Engineering, Hanyang University · ᵇ Department of Battery Engineering, Hanyang University (Seoul 04763, Korea) |
| 저널/년 | **Electrochimica Acta 542 (2025) 147413** |
| DOI | **10.1016/j.electacta.2025.147413** (Received 2025-08-18, revised/accepted 2025-09-17, online 2025-09-17) |
| Keywords | Solid electrolyte · **Transmission line model** · EIS · Composite electrode · Equivalent circuit modeling |
| 소재 (CAM/SE/도전제) | **CAM = NCM811 LiNi₀.₈Co₀.₁Mn₀.₁O₂** (COSMO AM&T) · **SE = LPSCl Li₆PS₅Cl** (POSCO-JK Solid Solution) · 도전제 = **Super P** (기본) / **VGCF** (1D 대안 비교, Fig S1) |
| 추가 SE (할라이드) | **LZC = Li₂ZrCl₆** (LiCl + ZrCl₄ 를 700 rpm 12 h ball-mill 합성) |
| 조성 (복합 양극 wt%) | NCM811 : LPSCl : Super P = **62:37:1 / 72:27:1 / 82:17:1** (황화물); **NCM811 : LZC : Super P = 72:27:1** (할라이드); NCM811:LPSCl:VGCF = 62:27:1 (VGCF) |
| CAM 코팅 | **LNO (LiNbO₃) coated NCM811** (대칭셀·full cell 기본) vs **uncoated NCM811** (§3.3 계면 R_ct 분리용) |
| 셀 | (a) **대칭셀** SUS\|복합양극\|SUS (이온 차단); (b) **3-전극 풀셀** WE=복합양극, CE=In/Li, **RE = Ag–Li 합금**(Teflon-coated Ag wire) |
| 압력 | **대칭셀 cold-press 250 MPa, 90 s** · separator LPSCl **433 MPa** · full cell SUS 삽입 후 **250 MPa, 3 min** · separator 위 양극 **100 MPa** 적층 |
| 측정 | EIS: Biologic SP-300, **7 MHz–50 mHz**, 5 mV, 온도 **30/45/60 °C** (constant-T chamber). Cycling: 3-전극 풀셀 **2.5–4.3 V vs Li/Li⁺, 30 °C, 1st 0.05C (CC-CV charge / CC discharge, CV cutoff = 1/5 의 applied current), 이후 0.5C** |
| 연구유형 | **실험**(EIS-TLM 측정·피팅 + cycling) **+ equivalent-circuit *model simulation***(2 BC × 각 요소 파라메트릭) |

---

## 3. 핵심 물성 (수치)

> ⚠ 이 논문은 *압밀 porosity*·*상대밀도*·*coordination*·*coverage* 를 측정·보고하지 **않는다**(EIS-TLM 임피던스
> 논문).  porosity/Z/coverage 칸은 n/a — 우리 압밀 앵커(Minnmann 14 %, Doux 18 %)와 직접 비교 금지.  대신
> **EIS-TLM 으로 분해한 R_ion / R_int(=R_ct) / C_dl(CPE) / Warburg(R_w, T_w, α) / 두께 L / bulk σ / 활성화경향**
> 이 이 논문의 정량 앵커.  ★ **모든 fitted 값은 SI Table S1–S7 verbatim**(§6.4); 본문 Fig 4f/5f/6b/6d 막대는
> 그 시각화(읽은 막대값은 digitized 로 구분).

| 물성 | 값 | 조건 | stated/digitized | 비고 |
|---|---|---|---|---|
| **bulk σ_ion (LPSCl)** | **1.6 mS/cm** | 황화물 SE | stated (본문 §3.3) | = Minnmann 1.6 과 일치; 우리 bulk 앵커 스프레드 |
| **bulk σ_ion (LZC 할라이드)** | **0.51 mS/cm** | 할라이드 SE | stated | LPSCl 의 ~1/3 (할라이드 = 낮은 σ, 높은 산화안정성) |
| **R_ion (symmetric, LNO-coated, R_i,bulk)** | 62: **9.3** / 72: **18.7** / 82: **12.8** Ω·cm² | 250 MPa 펠릿 대칭셀, 30 °C | stated (Table S3) | bulk 부분 |
| **R_ion,gb (symmetric, LNO-coated)** | 62: **25.6** / 72: **29.4** / 82: **6.2** Ω·cm² | 〃 | stated (Table S3) | ★ GB 기여가 bulk 와 *동급 크기* (sulfide GB 특성) |
| **R_e (symmetric, LNO-coated)** | 62: **4.8** / 72: **53.1** / 82: **262.7** Ω·cm² | 〃 | stated (Table S3) | ⚠ 비단조 (62 작음·82 큼은 *전자 차단셀 아님* 맥락, 아래 §5.3 주의) |
| **R_ion (3-electrode full cell, LNO-coated)** | 62: **7.5** / 72: **12.0** / 82: **4.7** Ω·cm² | 풀셀, 30 °C | stated (Table S4) | ★ **82 wt% 가 최저 R_ion** (densification↑) |
| **R_int (=R_ct, full cell, LNO-coated)** | 62: **22.4** / 72: **18.2** / 82: **17.2** Ω·cm² | 〃 | stated (Table S4) | ★ **82 wt% 최저 R_ct** (electroactive area↑) |
| **R_w (Warburg, full cell, LNO-coated)** | 62: **215.5** / 72: **40.6** / 82: **37.2** Ω·cm² | 〃 | stated (Table S4) | 62 wt% 가 압도적 큼 (저-CAM 확산 병목) |
| **T_w (Warburg time const)** | 62: **2929.3** / 72: **614.6** / 82: **676.0** s | 〃 | stated (Table S4) | 확산 시상수 |
| **α (Warburg 지수)** | 0.24–0.36 | full cell | stated (Table S4) | 0.5 = 이상 확산; <0.5 = frequency dispersion |
| **CPE_int C (full cell)** | 62: **84.2** / 72: **1.9** / 82: **0.9** µF·sᵑ⁻¹ | 〃 | stated (Table S4) | C_dl 상수위상요소; η 0.80–0.97 |
| **R_int (=R_ct, UNCOATED NCM811, full cell)** | 62: **453.4** / 72: **289.9** / 82: **382.4** Ω·cm² | uncoated, 30 °C | stated (Table S6) | ★ **uncoated R_ct 가 LNO-coated 의 ~20× (62: 453 vs 22)** = 황화물 산화분해 |
| **R_int (UNCOATED) vs T** | 30°C **289.9** → 45°C **139.6** → 60°C **67.8** | uncoated 72 wt% | stated (Table S6) | ★ R_ct 가 온도↑ → 급감 (Arrhenius, 큰 E_a) |
| **R_int (UNCOATED) symmetric** | 62: **127.2** / 72: **10.4** / 82: **6.2** Ω·cm² | uncoated 대칭셀 (Fig 6b 막대) | digitized (Fig 6b) | 대칭셀 막대; Table S5 와 대응 |
| **R_w (UNCOATED) symmetric** | 62: **127.2 / 336.8?** | 62/72/82 | digitized (Fig 6b) | (Fig 6b 막대 — 절대값은 Table S5 우선) |
| **LZC(할라이드) σ_eff,ion** | LPSCl 대비 낮음 (정성) | 72:27:1 | stated | 할라이드 = 낮은 σ_ion |
| **LZC R_int (=R_ct)** | LPSCl-system 보다 **유의하게 낮음** | 72:27:1 | stated (Fig 6 결론) | ★ 할라이드 = 낮은 산화분해 → 낮은 R_ct (계면 안정) |
| **두께 L (대칭셀)** | LNO 62/72/82 = **190/180/160 µm**; uncoated = 210/230/210 µm; **LZC = 170 µm** | 펠릿 | stated (Table S3/S5 + 본문) | ★ CAM↑ → 두께↓ (densification, 같은 분말질량) |
| **두께 L (full cell)** | LNO 62/72/82 = **47.5/45/40 µm** | 풀셀 | stated (Table S4) | 대칭셀 질량비로 환산 |
| porosity / 상대밀도 | **n/a** (미측정) | — | — | EIS 논문 |
| coverage / coordination Z | **n/a** | — | — | — |
| E_SE / σ_y / ν | **n/a** (역학 미모델) | — | — | (E_LPSCl 은 자매 Kang 2025 = 22.1 GPa) |
| Heckel / P_y | **n/a** | — | — | 압밀곡선 없음 |
| PSD (D10/D50/D90) | **n/a** (미보고) | — | — | NCM811·LPSCl 입경 명시 안 함 |

> ★ **bulk σ 앵커 정리:** LPSCl **1.6 mS/cm** (= Minnmann 1.6 과 정확히 일치) / 할라이드 LZC **0.51 mS/cm**.
> → 우리 LPSCl bulk 스프레드 {Cronau 단결정 3.0, Lee pristine 2.19, **이 논문 1.6 = Minnmann 1.6**, Bazzoun
> pellet 1.02} 에 *Hanyang 랩 자체 측정 1.6* 추가 (Minnmann 과 동일값 = 신뢰 보강).  ⚠ 절대 직접대조 금지, 범위로만.

---

## 4. 시뮬레이션 방법 ★ — modified TLM (equivalent-circuit *model simulation*; 우리 솔버의 실험 카운터파트)

> ★ 이 논문의 "시뮬레이션"은 DEM/MPM/FEM 이 아니라 **분포 임피던스 등가회로(modified TLM)의 해석해 + 파라메트릭
> model simulation** 이다.  우리 Kirchhoff/Holm σ-솔버와 **목적은 같고(전달·계면 분해) 형식이 다르다**(그들=주파수
> 영역 임피던스 회로, 우리=공간 저항망 DC 풀이).  Supplementary Note 1 의 해석해 + Tables S1–S7 을 정리.

### 4.1 TLM 토폴로지 (Fig 1, 2a, 3a) — 두 레일 + crossrail
복합 양극 = **혼합 전도체**(이온은 SE 입자망, 전자는 CAM+도전제망을 따로 흐름).  이를 **무한개의 미소
임피던스 요소가 두께 방향으로 분포된 사다리(ladder) 네트워크**로 모델 (Fig 2a/3a 의 회로 그림):
- **상단 레일 = 이온 임피던스 z₁** (SE 상; 단위 표면적당 [Ω·cm]).
- **하단 레일 = 전자 임피던스 z₃** (CAM + 도전제 상; [Ω·cm]).
- **crossrail = 계면 임피던스 z₂** (SE/CAM 계면; 단위 *부피*당 [Ω·cm³]) — **이온↔전자 가 만나는 곳 = 전기화학
  계면 = 전하전달**.  ★ "crossrail = electrochemical interface" 가 이 모델의 핵심 (Li⁺ 가 전자와 만나 반응).
- 각 레일은 **r_bulk + (r_gb ∥ CPE_gb)** 직렬로 구성 가능 — bulk *입내* 전도 + **grain-boundary *입계*** 전도를
  분리 (Fig 2d–g).  ★ **GB(입계) 항이 이 논문의 강조점** — 황화물 SE 는 cold-press 로 입계가 형성돼 GB 저항이
  bulk 와 *동급*(아래 §5).

### 4.2 ★ 분해되는 4가지 과정 (제목의 "multiple reactions") — 각 회로요소 ↔ 전기화학 과정
| 회로 요소 | 물리적 의미 | 우리 솔버 대응 |
|---|---|---|
| **z₁ = r_i,bulk + (r_i,gb ∥ cpe_i,gb)** | Li⁺ *이온수송* (SE 입내 + 입계) | ★ **우리 σ_ionic** (Kirchhoff/Holm); GB = 우리 Cronau(r_SE) GB 인자 |
| **z₃ = r_e,bulk + (r_e,gb ∥ cpe_e,gb)** | 전자 수송 (CAM/도전제 입내 + 입계) | 우리 σ_electronic |
| **r_int (in z₂) = R_ct** | **계면 전하전달저항** (Li⁺ + e⁻ → 활물질 격자 반응) | ★ **우리 미보유** (constriction-only 솔버) |
| **cpe_int (in z₂) = C_dl** | **이중층 충전** (계면 비-faradaic 용량) | ★ **우리 미보유** |
| **z_w (generalized finite-length Warburg, in z₂)** | **활물질 내 고상 Li 확산** | ★ **우리 미보유** (우리 D_Li 모델 없음) |
> ⇒ ★ **우리 σ_ionic 솔버는 z₁(이온수송)만 계산한다.**  z₂ 의 R_ct·C_dl·Warburg 세 과정은 우리가 *전혀*
> 모델하지 않는 *계면/확산 kinetics* — 이 논문이 그 빈 칸을 정확히 짚어 준다 (frame[5] 의 새 축).

### 4.3 ★ 두 경계조건 (BC) — 어느 BC 가 어느 과정을 고립시키나
이 논문의 *방법론적* 핵심.  복합 양극을 **어떤 전극으로 양 끝을 막느냐**에 따라 다른 과정이 활성화:

**(A) Ion-blocking / Ion-blocking (Fig 2)** — 양 끝 SUS(이온 차단), **전하전달 없음(no charge transfer)**:
- 구성 = 대칭셀 [집전체 | 복합양극 | 집전체].  이온이 양 끝에서 막힘 → crossrail 에 **전하전달 r_int 가 사라지고
  *이중층 cpe_int* 만 남는다**.  z₂ = 순수 용량(cpe_int).
- **해석해 (Supplementary Note 1):**
  `Z_total = z₁z₃/(z₁+z₃)·L + [2z₃²·√(z₂)/(z₁+z₃)^(3/2)]·{cosh[L·√((z₁+z₃)/z₂)]−1}/sinh[L·√((z₁+z₃)/z₂)]`
- **Nyquist 결과(Fig 2b):** 고주파 **45° 직선**(이온수송 = Gerischer-유사 거동) + 저주파 **반원**(계면 r_e).
  - r_i 크기 = Gerischer 임피던스 호의 *전체 크기* 결정 (Fig 2c 상: r_i 500→1500 Ω·cm 로 호 확대).
  - r_e 변화 = 저주파 끝점 위치 이동 (Fig 2c 하: r_e 800→1200).
  - **GB 추가(Fig 2d–g):** r_gb ∥ cpe_gb 를 z₁/z₃ 에 직렬로 → **고주파에 추가 반원** 출현.
    r_i,gb↑ → 고주파 반원↑ (Fig 2e); c_i,gb↑ → 두 반원 사이 local minimum 이 저주파로 이동.
    전자 GB(r_e,gb, c_e,gb)도 동일 거동 (Fig 2f,g).
  - ★ **CPE 지수 = 1 로 고정**(시뮬레이션).  전극 두께 **L = 200 µm 고정**.

**(B) Electron-blocking / Ion-blocking (Fig 3)** — 한 끝 전자 차단, **전하전달 발생(charge transfer occurs)**:
- 구성 = [In/Li | LPSCl | 복합양극 | LPSCl | In/Li] 류 — LPSCl 층이 전자를 막아 **이온이 계면을 건너 전하전달**.
  crossrail 에 **r_int(=R_ct) 가 살아난다** → cpe_int ∥ r_int 병렬 (Fig 3c).
- **해석해 (Supplementary Note 1):**
  `Z_total = z₁z₃/(z₁+z₃)·L + [z₂/(z₁+z₃)^(3/2)]·{(z₁²+z₃²)·cosh[L·√((z₁+z₃)/z₂)] + 2z₁z₃}/sinh[L·√((z₁+z₃)/z₂)]`
- **Nyquist 결과(Fig 3):**
  - Fig 3b (cpe_int 만): 고주파 45° + 거의 수직선(순수 용량 차단).
  - Fig 3c (+r_int): **저주파 반원 = 계면 전하전달** 출현 (r_int = 반원 지름).
  - Fig 3d (+z_w Warburg): 저주파에 **45° 직선(Warburg)→수직선** 전이 = **고상확산** (Warburg-to-capacitive).
  - Fig 3e (+r_e): r_e 추가 → 실수축 전체 우측 이동.
  - 파라메트릭(Fig 3f,g): r_i 500→1500 → 대각 영역 확대; r_int 0.3→0.8 → 반원 확대.
- ★ **Warburg = generalized finite-length** (해석해):
  `z_w = r_w·coth[(jωT_w)^α] / (jωT_w)^α`, r_w = 고상확산 저항, T_w = 확산 시상수, **α = frequency-dispersion
  지수**(0.5 = 이상 확산).  ⇒ ★ **이 한 식이 우리가 안 갖는 "활물질 내 Li 고상확산"을 임피던스로 표현.**

### 4.4 입자 처리 ★ (DEM판 "무질서 처리"의 *부재* — 이건 회로 모델)
- ★ **입자 형상·PSD·rigid/plastic 개념이 *없다*.**  이 논문은 미세구조를 *명시적으로 생성하지 않는다* —
  복합 양극을 **분포 임피던스의 *연속 사다리***로 추상화(L, z₁, z₂, z₃ 파라미터만).  ⇒ 우리 DEM(구·접촉망)·
  MPM(소성 형상)·Bazzoun(구 DEM)·Bielefeld(voxel) 의 *구조* 차원이 **이 논문엔 통째로 없다** — 구조는
  R_ion/R_int 라는 *측정된 lumped 파라미터*로만 들어온다.  ⇒ **frame[5]:** 그들 = *측정/회로*, 우리 = *구조→σ*.

### 4.5 도메인 / 압력 / seeds
- model simulation: L=200 µm 고정 (Table S1/S2/S7), 단일 실현(파라메트릭 스윕).
- 실험 셀: 대칭셀 ⌀10 mm × 0.2 mm (40 mg 분말, **250 MPa 90 s**); separator LPSCl 100 mg **433 MPa**;
  full cell 양극 10 mg **100 MPa** 적층 + In(100 µm)/Li(200 µm) + SUS **250 MPa 3 min**.
- ★ **압력 3종 구분 (우리 인식과 합류):** 제조/압밀 = **250–433 MPa** (cold-press) ≠ 측정/작동압(EIS 는 셀
  조립 상태). 우리 "제조 300 MPa ≠ 작동 수~수십 MPa"·Doux·Lee2025·Minnmann 380 과 같은 계열 (separator 433 은
  Minnmann 380·Doux 370 보다 약간 높은 고압 압밀).

---

## 5. 결과 상세 — Section-by-section (모든 수치)

### 5.1 §3.1 Model simulation (Fig 1–3) — 회로요소별 Nyquist 시그니처
**목적:** 각 회로요소가 Nyquist 의 *어느 영역*을 바꾸는지를 미리 못박아, 실험 스펙트럼 해석의 *문법*을 세움.
- **Fig 1:** ASSB 복합 양극의 전기화학 과정 모식 — ion transport / electron transport / charge transfer /
  grain boundary / solid-state diffusion 다섯을 그림으로 분류.  composite electrode = mixed conductor.
- **Fig 2 (ion-blocking/ion-blocking, no charge transfer):** 위 §4.3(A).  핵심 학습:
  - 고주파 45° = 이온수송(Gerischer); 저주파 반원 = r_e 계면.
  - r_i = 호 *크기*; r_e = 저주파 *위치*.  **GB 추가 → 고주파 추가 반원**(r_gb↑→크기↑, c_gb↑→minimum 저주파).
- **Fig 3 (electron-blocking/ion-blocking, charge transfer 발생):** 위 §4.3(B).  핵심 학습:
  - 고주파 45° 직선 = 이온수송; **중주파 반원 = 계면 전하전달 r_int(=R_ct)**; 저주파 45°→수직 = Warburg 고상확산.
  - ⇒ ★ **이 BC 가 R_ct 를 *분리해서 보이게* 하는 BC.**  실험 풀셀이 이 회로로 피팅됨.

### 5.2 §3.2 대칭셀 (Fig 4) — 조성·온도 스윕, LNO-coated NCM811
**셀:** SUS\|LNO-coated NCM811:LPSCl:SuperP\|SUS, 250 MPa.  ion-blocking → 이온 GB 회로(Fig 2d/f)로 피팅.
- **Fig 4a (Nyquist, 62/72/82 wt%):** **두 개의 눌린 반원**(depressed semicircle) — 시뮬 Fig 2d/f 와 동형.
  ★ **NCM811↑ → 스펙트럼 크기↓ + 저주파 실수축 절편↓** = 더 densify → 이온 percolation↑.
- **Fig 4b (DRT, distribution of relaxation time):** **다섯 개 polarization peak** — DRT 로 시상수 deconvolute.
  ★ **NCM811↑ → 모든 peak 강도 급감** (전반적 저항↓).
- **Fig 4c,d (온도 30/45/60 °C, 62 wt% 고정):** 온도↑ → **고주파 반원↓ + 고주파 DRT peak↓**.  ★ **고주파 두
  DRT peak = 이온수송**(입내 + 입계)으로 귀속(온도 의존성으로 확인) → **고주파 반원 = 이온 GB 임피던스**.
- ★ **GB 기여가 bulk 와 *동급 크기*** (Table S3): 62 wt% R_i,bulk 9.3 vs R_i,gb 25.6 (GB 가 *더 큼!*);
  72 wt% 18.7 vs 29.4.  → **"sulfide SE 의 입계가 이온수송의 주 병목"** (cold-press 로 형성된 GB) — 우리
  Cronau(r_SE) GB 인자·grain-boundary density 항의 실험 근거.
- ★ **R_ion 추세 (Table S3, R_i,bulk+R_i,gb):** 62 wt% **34.9** / 72 wt% **48.1** / 82 wt% **19.0** Ω·cm² →
  **82 wt% 가 최저 이온저항** (본문 명시: "82 wt% NCM811 exhibited the lowest ionic resistance").  ⚠ 통념
  ("SE↑ → 이온 좋음")과 *반대* — 이유: 같은 분말질량이라 **CAM↑ → 부피↓ → 더 thin·compact → 이온 percolation↑**.
  (★ 단 72 wt% 가 62 보다 약간 높은 건 비단조 — 압밀/패킹 변동.)

### 5.3 §3.2 풀셀 (Fig 5) — 3-전극, 전하전달 분리, LNO-coated
**셀:** 3-전극 풀셀(WE 복합양극, CE In/Li, **RE Ag–Li 합금**), electron-blocking → charge transfer 회로(Fig 3)로 피팅.
- ★ **3-전극의 이유:** **양극 임피던스만** 고립(음극 In/Li 신호 제거).  RE = Teflon-coated Ag wire(⌀0.16 mm,
  끝 1 mm 노출)를 separator 중앙에 삽입 → 양극 신호를 RE 기준으로 측정.  → ★ **우리는 이런 *실험적* 전극 분리가
  불가**(우리는 구조에서 σ 를 *계산*) — 그들의 3-전극 = 실험으로 양극만 보는 트릭.
- **Fig 5a (Nyquist):** 고주파 45° 직선(이온수송) + 중주파 눌린 반원(R_int=R_ct) + 저주파 45° 직선(Warburg 확산).
- **Fig 5b (DRT):** 다섯 peak; **0.1–1 kHz 의 second-largest peak = R_int(전하전달)** 로 귀속 (온도↑·CAM↑ → 강도↓).
- **Fig 5c,d (온도):** 온도↑ → 중주파 반원(R_int)↓ = kinetics 가속.
- ★ **핵심 fitted 추세 (Table S4, LNO-coated full cell):**
  - **R_int(=R_ct):** 62 **22.4** / 72 **18.2** / 82 **17.2** Ω·cm² → **82 wt% 최저 R_ct** (본문: "the cell with
    82 wt% NCM811 exhibited the lowest charge transfer resistance").  이유 = **CAM↑ → electroactive surface
    area↑** (활물질-SE 접촉면적↑).  ★ 우리 coverage(A_AM-SE)·active-interface 와 같은 물리.
  - **R_w(Warburg):** 62 **215.5** ≫ 72 **40.6** ≈ 82 **37.2** → **저-CAM(62)이 확산 병목 압도적**.
  - **R_ion:** 62 7.5 / 72 12.0 / 82 4.7 → 82 최저 (대칭셀과 일치).
  - ⇒ ★ **CAM↑(82 wt%) 이 R_ion·R_ct·R_w *세 저항 모두* 최저** → 고-CAM 이 (이 LNO-coated·이 압력에서는)
    수송·계면·확산 모두 유리.  단 이는 *전기화학 저항*만; 사이클 안정성/균열은 자매 Kang 2025 가 다룸(고-CAM·큰
    입자 = 균열 리스크) → **두 논문이 trade-off 의 양면**.

### 5.4 §3.3 계면 kinetics — uncoated vs LNO-coated (Fig 6) ★ 자매 논문 연결의 핵심
**목적:** LNO 코팅을 *벗겨* uncoated NCM811 로 가면 **계면 전하전달 R_ct 가 *극적으로 커진다*** — 황화물/CAM
산화분해가 R_ct 를 키움을 분리 입증.
- **Fig 6a,b (uncoated 대칭셀):** **명확히 분리된 두 반원**(coated 보다 GB 기여 큼) — uncoated 표면의 sluggish
  이온수송(계면 분해층).  Table S5: 82 wt% R_i,gb = **209.5 Ω·cm²**(!) = uncoated 고-CAM 의 GB 가 폭증.
- **Fig 6c,d (uncoated 풀셀):** **중주파 R_int 반원이 압도적으로 큼.**  ★ Table S6:
  - **R_int(=R_ct) uncoated:** 62 **453.4** / 72 **289.9** / 82 **382.4** Ω·cm² → **LNO-coated 의 ~13–20×**
    (coated 62: 22.4 → uncoated 62: 453.4 = **20×**).  ★★ **"oxidative degradation of uncoated NCM811 with
    LPSCl → large interfacial charge transfer resistance (sluggish kinetics); LNO protective layer suppressed
    side reactions"** — 본문 명시.
  - **온도 의존 (uncoated 72 wt%):** R_int 30°C **289.9** → 45°C **139.6** → 60°C **67.8** = 온도↑ → R_ct 반감×2
    → **큰 활성화에너지**(계면반응이 열적으로 강하게 활성화 = 느린 kinetics 의 전형).
  - ⇒ ★ **uncoated NCM811/LPSCl 계면 = 우리 production 소재의 *맨* 계면** → 분해로 R_ct 가 수백 Ω·cm² 까지 큼.
    LNO 코팅이 이를 ~20× 낮춤.  ★ **이게 Kang 2025 의 "계면분해→균열"의 *kinetics 버전*** (분해가 한쪽에선
    R_ct↑, 다른 쪽에선 Li-구배→균열).
- ★ **uncoated 가 임피던스 *분해*에 유리한 역설:** 본문 — coated NCM811 은 이온수송(고주파 45°)과 전하전달(중주파
  반원)이 거의 *구분 안 됨*(R_ct 가 작아서); **uncoated 는 R_ct 가 커서 두 영역이 *명확히 분리*** → "**추가
  분석 없이 이온수송과 전하전달을 직접 decouple 가능**".  ⇒ ★ 방법론 교훈: *R_int/R_i 비*가 클 때만 임피던스가
  깨끗이 분해됨.

### 5.5 §3.3 R_int/R_i 비의 파라메트릭 (Fig 6e–g, Table S7) ★ 임피던스 분해 가능성의 조건
**Morasch et al. 의 접근**(전하전달/pore-ionic 비가 다공전극 임피던스 형태를 좌우)을 TLM 으로 재현:
- R_int/R_i = **3, 1, 1/4, 1/16** 스윕 (Table S7: r_i 1000→10000 Ω·cm, r_int 1.2→0.25):
  - **R_int/R_i 높음(3, 1):** 이온수송 영역과 전하전달 영역이 **명확히 분리** (uncoated 처럼).
  - **R_int/R_i 낮음(1/4, 1/16):** 두 영역 **겹쳐 구분 불가** → **저주파 확산만 다름**.
- ★ **결론:** "**charge transfer kinetics 가 ionic transport 보다 느리지(R_ct 큼) 않으면, full-cell 단독 임피던스
  분석은 오해를 부른다 → 정확한 전하수송저항 정량엔 *대칭셀 보완 분석이 필수***" (full cell + symmetric cell 병용).
- ⇒ ★ **우리 σ_ionic 검증에의 함의:** 우리가 R_ion 을 *구조에서 계산*할 때, 실험 EIS 의 R_ion 을 앵커로 쓰려면
  **R_ct 가 충분히 커서 R_ion 이 깨끗이 분리된 셀**(uncoated, 또는 대칭셀)의 값을 써야 한다 — coated full-cell 의
  lumped 값은 R_ct 와 섞여 부정확.  Bazzoun/Minnmann 이 *대칭셀/full-blocking* 을 쓴 이유와 동일.

### 5.6 §3.3 할라이드(LZC) vs 황화물(LPSCl) (Fig 6 후반) ★ Varkey 할라이드 cross-check
**셀:** uncoated NCM811 : **LZC(Li₂ZrCl₆)** : SuperP = 72:27:1, 대칭셀+풀셀.
- **bulk σ:** LZC **0.51 mS/cm** < LPSCl **1.6 mS/cm** (할라이드 = 낮은 이온전도).
- **대칭셀(Fig 6f):** LZC 가 **유의한 GB 기여** → 이온수송저항이 LPSCl 보다 *높음* (예상대로, 낮은 σ_ion).
- **풀셀(Fig 6g):** ★ **LZC 의 R_int(=R_ct) 가 LPSCl-system 보다 *유의하게 낮음***.  → "**reduced interfacial
  oxidative degradation**" — 할라이드는 황화물보다 **산화 안정성↑** → 계면분해↓ → R_ct↓.
- ★ **핵심 trade-off:** 할라이드 = **낮은 σ_ion(0.51) BUT 안정한 계면(낮은 R_ct)**; 황화물 = **높은 σ_ion(1.6)
  BUT 불안정 계면(높은 R_ct, 특히 uncoated)**.  ⇒ "**낮은 σ + 높은 R_ct 인 시스템(할라이드/uncoated)에서는
  이온수송·전하전달 영역이 *분리*되어 신뢰성 있는 임피던스 분해 가능**" (Fig 6e 의 R_int/R_i 논리와 합치).
- ⇒ ★ **Varkey 2026(할라이드 Li₃YBrCl₆ + NMC811) cross-check**: Varkey = 할라이드 *압밀/σ* (E=10.58, floor 21/37%);
  이 논문 = 할라이드 *계면 kinetics*(낮은 R_ct).  **둘 다 "할라이드 = 안정하나 σ 낮음"** 의 다른 측면.

### 5.7 §3.3 Super P vs VGCF (Fig S1) — 도전제 형상 효과
- **Super P(0D 카본):** 일반 도전제이나 **금속 불순물**(제조 중 도입) → 사이클 안정성 저하; SE/카본 계면 분해 위험.
- **VGCF(1D vapor-grown carbon fiber):** ★ **대칭셀 전자저항이 Super P 보다 *상당히 낮음***(1D 망 = 효율적 전자
  percolation); **풀셀 R_int(계면저항)도 낮음**(SE-카본 계면면적↓ → 산화분해↓).  → "**1D VGCF 가 전자 percolation↑
  + SE 산화분해 완화**".
- ⇒ ★ **우리 σ_e 도전제 항·Lee 2025 VGCF 데이터와 합치**(VGCF = 효율적 전자망).  단 우리는 도전제 형상(0D/1D)
  구분이 약함 → 흡수 후보.

### 5.8 §4 결론 (저자 요약)
- modified TLM(2 BC) + 대칭셀·풀셀 EIS 로 **이온수송·전자수송·전하전달·이중층·고상확산을 체계적 분해**.
- 고주파 반원 = **이온 GB 임피던스**(온도 스윕으로 확인); 조성이 electroactive area·R_ct 를 좌우.
- ★ **full cell 단독 분석은 오해 소지 → 대칭셀 병용 필수** (R_int/R_i 비가 작으면 영역 겹침).
- → "**ASSB 복합 양극의 다중 반응속도 정량분석을 위한 robust 전략**".

---

## 6. Figure / Table set ★ (모든 그림·표 + 우리가 쓸 점)

### 6.1 본문 Figures
| Fig | 내용 (무엇을 보여주나) | 핵심 수치 | 우리가 참고할 점 |
|---|---|---|---|
| **1** | ASSB 복합 양극 전기화학 과정 모식 (ion/electron transport·charge transfer·GB·diffusion) | — | 5과정 분류 = 우리가 *어느 칸*을 갖고/못 갖는지 지도 |
| **2a** | ion-blocking TLM 회로 + 요소 (z₁/z₂/z₃, r_gb∥cpe_gb) | L=200 µm | ★ 사다리 회로 토폴로지 = 우리 저항망의 임피던스판 |
| **2b** | 순수 저항 TLM Nyquist (45°+반원) | — | r_i=호크기, r_e=저주파위치 |
| **2c** | r_i(500/1500)·r_e(800/1200) 파라메트릭 | — | 요소→Nyquist 문법 |
| **2d–g** | 이온 GB·전자 GB 요소 + 파라메트릭 | r_gb 250/750, c_gb 0.001/0.1 | ★ **GB 추가 → 고주파 추가 반원**(우리 GB 인자) |
| **3a** | electron-blocking TLM 회로 (r_int 살아남) | — | ★ **R_ct 분리 BC** |
| **3b–e** | cpe_int→r_int→z_w(Warburg)→r_e 누적 Nyquist | r_int 0.5, r_w 1, T_w 10 | ★ 중주파 반원=R_ct, 저주파=확산 |
| **3f,g** | r_i(500/1500)·r_int(0.3/0.8) 파라메트릭 | — | R_ct→반원크기 |
| **4a** | 대칭셀 Nyquist (62/72/82 wt%, LNO-coated) | 두 눌린 반원; CAM↑→크기↓ | ★ CAM↑→densify→이온↑ |
| **4b** | 대칭셀 DRT (62/72/82) | 5 peak; CAM↑→강도↓ | DRT 시상수 분해 |
| **4c,d** | 대칭셀 온도(30/45/60, 62 wt%) Nyquist+DRT | 온도↑→고주파↓ | ★ 고주파=이온 GB(온도확인) |
| **4e** | 대칭셀 TLM 회로 (r_i,bulk+r_i,gb∥cpe_i,gb + r_e, cpe_int) | — | 피팅 회로 |
| **4f** | 대칭셀 정량 막대 R_i,bulk/R_i,gb/R_e (조성·온도) | 62: 35.0/336.8/…; 82: 19.0/3.7 (digitized) | ★ 정량값(Table S3 우선) |
| **5a** | 풀셀 Nyquist (62/72/82, LNO) | 45°+반원+45° | 이온/R_ct/확산 분리 |
| **5b** | 풀셀 DRT | 0.1–1 kHz peak=R_ct | R_ct DRT 귀속 |
| **5c,d** | 풀셀 온도 Nyquist+DRT | 온도↑→R_ct↓ | kinetics 가속 |
| **5e** | 풀셀 TLM 회로 (r_i, r_int∥(z_w), cpe_int, r_e) | — | charge-transfer 회로 |
| **5f** | 풀셀 정량 막대 R_int/R_w (조성·온도) | 62: 22.4/215.5; 82: 17.2/37.2 (digitized) | ★ R_ct·R_w 추세(Table S4) |
| **6a** | uncoated 대칭셀 Nyquist (62/72/82) | 분리된 두 반원 | uncoated GB↑ |
| **6b** | uncoated 대칭셀 정량 막대 (R_i,bulk/R_i,gb/R_e) | 62: 62.7/127.2; 82: 10.4/6.2 (digitized) | Table S5 우선 |
| **6c** | uncoated 풀셀 Nyquist | 압도적 큰 R_int 반원 | ★ uncoated R_ct 폭증 |
| **6d** | uncoated 풀셀 정량 막대 (R_int/R_e) | 62: 453.4; 72: 289.9; 82: 382.4 | ★ **uncoated R_ct = coated 의 ~20×** |
| **6e** | R_int/R_i (3/1/1/4/1/16) 파라메트릭 Nyquist | r_i 1000–10000, r_int 0.25–1.2 | ★ 분해 가능성 조건 |
| **6f** | 할라이드(LZC) 대칭셀 (vs LPSCl) | GB 기여 큼; σ 낮음 | ★ 할라이드 이온저항↑ |
| **6g** | 할라이드(LZC) 풀셀 | R_int *낮음* (안정 계면) | ★ **할라이드=낮은 R_ct** |

### 6.2 SI Figures
| Fig | 내용 | 우리가 참고할 점 |
|---|---|---|
| **S1a–d** | VGCF 대칭셀·풀셀 온도(30/45/60) Nyquist + 정량 | ★ VGCF 전자저항·R_int < Super P (1D 망) |

### 6.3 본문 Fig 4f/5f/6b/6d 막대 ↔ Table 대응 주의 (digitized 구분)
> ⚠ Fig 4f/5f/6b/6d 의 막대 *라벨 숫자*(35.0, 336.8, 48.1, 7.4, 19.0, 3.7, 215.5 등)는 그림에서 읽은 값으로,
> 일부는 **DRT-적분 R 또는 bulk+gb 합** 등 Table 의 개별 fitted 파라미터와 *정규화가 다를 수 있다*.  **절대값은
> 항상 아래 §6.4 Table S3–S6 의 verbatim fitted 값을 우선**한다 (336.8 은 Table S3 의 62 wt% **CPE C=336.8 µF**
> 값이 막대로도 나타난 것 — R 이 아니라 *용량* 라벨일 수 있음).  본문 추세 진술(82 최저 R_ion·R_ct 등)은 stated.

### 6.4 ★ SI Tables S1–S7 (fitted 파라미터 verbatim — 우리 정량 앵커)

**Table S3 — 대칭셀 (LNO-coated NCM811) [Ω·cm²]** ★ 이온 GB 회로
| 조건 | L(µm) | R_i,bulk | R_i,gb | CPE_i,gb C(µF·sᵑ⁻¹) | η | R_e | CPE_int C(mF) | η |
|---|---|---|---|---|---|---|---|---|
| 62 wt% | 190 | 9.3 | 25.6 | 4.8 | 0.69 | **336.8** | 6.3 | 0.78 |
| 72 wt% | 180 | 18.7 | 29.4 | 53.1 | 0.60 | 7.4 | 14.9 | 0.63 |
| 82 wt% | 160 | 12.8 | 6.2 | 262.7 | 0.61 | 3.7 | 18.3 | 0.60 |
| 45 °C (62) | 190 | 8.0 | 12.4 | 5.2 | 0.72 | 256.8 | 7.2 | 0.80 |
| 60 °C (62) | 190 | 6.0 | 3.1 | 5.7 | 0.81 | 181.2 | 9.6 | 0.83 |
> R_ion(=bulk+gb): 62 **34.9** / 72 **48.1** / 82 **19.0** → 82 최저.  온도↑(62): R_i,gb 25.6→12.4→3.1 (이온 GB 가
> 온도로 급감 = 큰 E_a) · R_i,bulk 9.3→8.0→6.0 (bulk 는 완만).  ★ **GB 가 bulk 와 동급/더 큼** + **GB 가 온도에
> 더 민감** → 황화물 이온수송의 주 병목 = *입계*.  ⚠ R_e 막대(62: 336.8)는 Table 의 R_e 4.8 과 다름 → Fig 4f
> "336.8" 은 **CPE_int C 값**이 막대로 표시된 것(R 아님).  Table 의 R_e(4.8/53.1/262.7)가 fitted 전자저항.

**Table S4 — 3-전극 풀셀 (LNO-coated NCM811) [Ω·cm²]** ★ charge-transfer 회로
| 조건 | L(µm) | R_i | R_int(=R_ct) | CPE_int C(µF·sᵑ⁻¹) | η | R_e | R_w | T_w(s) | α |
|---|---|---|---|---|---|---|---|---|---|
| 62 wt% | 47.5 | 8.7 | **22.4** | 84.2 | 0.97 | 34.5 | **215.5** | 2929.3 | 0.31 |
| 72 wt% | 45 | 12.0 | **18.2** | 1.9 | 0.89 | 27.1 | **40.6** | 614.6 | 0.24 |
| 82 wt% | 40 | 4.7 | **17.2** | 0.9 | 0.80 | 58.8 | **37.2** | 676.0 | 0.30 |
| 45 °C | 47.5 | 5.1 | 8.7 | 64.2 | 0.97 | 64.7 | 106.4 | 1207.5 | 0.36 |
| 60 °C | 47.5 | 2.3 | 7.6 | 45.3 | 0.94 | 53.9 | 81.0 | 2350.0 | 0.27 |
> ★ **R_int(R_ct): 82 최저(17.2) — CAM↑→electroactive area↑.  온도↑(62 base? 사실 45/60 은 별도): R_int 22.4(?)
> → 45°C 8.7 → 60°C 7.6** = 온도로 R_ct 급감(kinetics 가속).  R_w(62=215.5) 저-CAM 확산병목.  α 0.24–0.36 (≪0.5,
> 강한 frequency dispersion = 비이상 확산/계면).  ★ **이 표가 R_ion+R_ct+C_dl+확산 *동시 분해*의 결정체** —
> 우리가 갖는 건 R_i 칸뿐, R_int·CPE_int·R_w·T_w·α 는 전부 우리 미보유.

**Table S5 — uncoated NCM811 대칭셀 [Ω·cm²]**
| 조건 | L(µm) | R_i,bulk | R_i,gb | CPE_i,gb C(µF) | η | R_e | CPE_int C(mF) | η |
|---|---|---|---|---|---|---|---|---|
| 62 wt% | 210 | 12.2 | 50.5 | 4.6 | 0.69 | 127.2 | 1.6 | 0.84 |
| 72 wt% | 230 | 12.9 | 80.3 | 14.2 | 0.65 | 10.4 | 1.1 | 0.87 |
| 82 wt% | 210 | 59.7 | **209.5** | 9.7 | 0.63 | 6.2 | 2.3 | 0.83 |
| 45 °C | 230 | 14.3 | 37.0 | 16.7 | 0.67 | 7.3 | 2.2 | 0.82 |
| 60 °C | 230 | 10.8 | 8.3 | 55.4 | 0.64 | 4.7 | 3.2 | 0.81 |
> ★ uncoated 의 **R_i,gb 가 coated 대비 *훨씬 큼*** (82 wt%: coated 6.2 → uncoated **209.5**, ~34×) = 분해층이
> 입계 이온수송을 막음.  온도↑ → R_i,gb 급감(37→8.3).

**Table S6 — uncoated NCM811 3-전극 풀셀 [Ω·cm²]** ★ 계면 R_ct 폭증
| 조건 | L(µm) | R_i | R_e | R_int(=R_ct) | CPE_int C(µF) | η |
|---|---|---|---|---|---|---|
| 62 wt% | 52.5 | 15.7 | 31.8 | **453.4** | 42.8 | 0.90 |
| 72 wt% | 57.5 | 23.3 | 2.6 | **289.9** | 31.0 | 0.91 |
| 82 wt% | 52.5 | 67.3 | 1.5 | **382.4** | 41.6 | 0.93 |
| 45 °C | 57.5 | 12.8 | 1.8 | **139.6** | 27.2 | 0.93 |
| 60 °C | 57.5 | 4.8 | 1.2 | **67.8** | 31.6 | 0.92 |
> ★★ **uncoated R_int(R_ct) = coated 의 ~13–20×** (62: coated 22.4 → uncoated 453.4 = 20×; 72: 18.2 → 289.9 =
> 16×) = **NCM811/LPSCl 산화분해가 전하전달을 ~20× 느리게**.  온도(72 wt%): 289.9→139.6→67.8 = ~2×/15°C 감소 →
> **큰 활성화에너지**(아래 §7 Arrhenius).  ★ **이게 우리 production *맨* 계면의 kinetics + Kang 2025 분해→균열의
> kinetics 짝.**

**Table S1 (ion-block 시뮬), S2 (e-block 시뮬), S7 (R_int/R_i 시뮬)** — model simulation 입력값(§4.3, Fig 2/3/6e).
L=200 µm 고정.  S7: R_int/R_i = 3/1/1/4/1/16 (r_i 1000/2500/5000/10000, r_int 1.2/1/0.5/0.25).

---

## 7. ★ 활성화에너지 (온도 스윕 30/45/60 °C) — 우리가 *전혀* 안 갖는 축

> ★ 이 논문이 우리에게 주는 **가장 새로운 축**: 온도 스윕으로 **이온수송 vs 계면반응의 활성화에너지를 분리**.
> 우리 σ-솔버는 *상온 단일온도* 만 — T-의존 σ 가 없다.  ⚠ 논문은 명시적 E_a 수치(eV/kJ)를 *본문 표로 주지는
> 않으나*, **Arrhenius 거동을 정성+준정량적으로 보인다** (저항의 온도 의존성 = E_a 의 직접 proxy).

| 과정 | 온도 의존 (Table 값) | E_a 정성 | 우리 대응 |
|---|---|---|---|
| **이온수송 bulk (R_i,bulk)** | 62 대칭셀: 9.3→8.0→6.0 (30→45→60°C) | **작은 E_a** (완만) | 우리 σ_ionic bulk (Cronau σ_grain) |
| **이온수송 GB (R_i,gb)** | 62 대칭셀: 25.6→12.4→3.1 | **큰 E_a** (급감, ~8× over 30°C) | ★ 우리 GB 인자 — GB 가 *열적으로 강하게 활성화* |
| **계면 전하전달 (R_int=R_ct)** | uncoated 72 풀셀: 289.9→139.6→67.8 | **매우 큰 E_a** (~4.3× over 30°C) | ★ **우리 미보유** — R_ct 가 가장 강한 T-의존 |
| **고상확산 (R_w)** | 62 풀셀: 215.5→106.4→81.0 | 중간 E_a | ★ 우리 미보유 (D_Li 모델 없음) |
> ★ **물리적 서열:** E_a(R_ct) > E_a(R_i,gb) > E_a(R_w) > E_a(R_i,bulk).  **계면반응(R_ct)이 가장 thermally-
> activated** = 가장 느린 kinetics = 율속(rate-limiting).  ⇒ 이게 "**계면이 ASSB 의 병목**"의 정량 근거이자,
> **우리 constriction-only σ-솔버가 못 잡는 부분**(우리는 GB·계면반응의 *온도* 활성화를 모델 안 함).
>
> ★ **준정량 E_a 추정 (Arrhenius ln(1/R)=ln A − E_a/RT; 30/45/60 °C = 303/318/333 K):**
> R_ct(uncoated 72): 289.9→67.8 over 303→333 K → **E_a ≈ R·ln(289.9/67.8)/(1/303−1/333) ≈ 40 kJ/mol ≈ 0.42 eV**
> (TREND-only, 3점 추정).  R_i,gb(62): 25.6→3.1 → **E_a ≈ 0.6 eV** (입계 이온수송도 큰 활성화).
> ⚠ **digitized/계산 추정**(논문이 명시 표로 안 줌) — 절대값 신뢰 말고 *서열·크기대*만.

---

## 8. Post-processing ★
- **무엇:**
  - **modified TLM 등가회로 피팅** (2 BC) → R_i,bulk / R_i,gb / R_e / R_int(=R_ct) / CPE_int(=C_dl) /
    R_w·T_w·α(Warburg 고상확산) 분해.  해석해 = Supplementary Note 1 (ion-block, e-block, generalized FLW).
  - **DRT(Distribution of Relaxation Time)** 분석 → 시상수별 polarization peak deconvolution (Fig 4b/5b 등 5 peak),
    피팅 전 *적절한 등가회로 결정* + 고주파 peak 의 이온-GB 귀속(온도 스윕으로 확인).
  - **온도 스윕 Arrhenius** → R 의 온도 의존 → 활성화에너지 서열 (이온 GB ≫ bulk; R_ct 가 최대).
  - **3-전극 분리** → 양극 임피던스만 (Ag–Li RE 로 음극 제거).
  - **Morasch R_int/R_i 비 분석** → 임피던스 분해 가능성 조건 (비 작으면 영역 겹침 → 대칭셀 병용 필수).
- **도구:** **Biologic SP-300**(EIS, 7 MHz–50 mHz, 5 mV); TLM 등가회로 피팅(소프트 미명시 — RELAXIS 류 추정);
  DRT 소프트(미명시).  cycling = (장비 미명시).
- **수치화·기록:** 조성(62/72/82)·온도(30/45/60)·코팅(LNO/uncoated)·SE(LPSCl/LZC)·도전제(SuperP/VGCF)별
  R_i,bulk/R_i,gb/R_e/R_int/CPE/R_w/T_w/α + 두께 L 을 Table S1–S7 로.

---

## 9. 우리 DEM+MPM + 전달 파이프라인 대비  →  `our_dem_baseline.md`

| 항목 | 이 논문 (Kim 2025) | 우리 | 차이 / 이유 |
|---|---|---|---|
| **방법** | **실험 EIS + modified TLM 피팅** (주파수 영역 임피던스 회로) | **DEM Kirchhoff/Holm σ-솔버** (공간 저항망 DC 풀이) + Stage-E | ★ **목적 같음(전달·계면 분해), 형식 다름** — 그들=측정/회로, 우리=구조→σ.  frame[4] 외부 검증 |
| **σ_ionic / R_ion** | **R_ion 측정·분해** (대칭셀 34.9/48.1/19.0 Ω·cm²; bulk σ 1.6) | σ_ionic *계산* (LOOCV 0.975); bulk σ_grain 3.0×Cronau | ★ **같은 NCM811+LPSCl** → 그들 R_ion 이 우리 σ_ionic 직접 앵커 (wt%→φ_SE 매핑 후); bulk 1.6=Minnmann 1.6 |
| **GB(입계) 저항** | ★ **R_i,gb 가 R_i,bulk 와 동급/더 큼** (62: 9.3 vs 25.6) + 온도에 더 민감 | Cronau(r_SE) sub-µm GB 인자 (σ_grain prefactor) | ★ **그들이 GB 를 *분리 측정*** → 우리 GB 인자의 실험적 정당화 (입계가 주 병목); 우리는 GB 를 σ_grain 에 럼핑 |
| **R_int (=R_ct, 전하전달)** | ★ **분해·측정** (coated 17–22, uncoated 290–453 Ω·cm²) | ★ **우리 미보유** (constriction-only) | ★ **우리 σ-솔버가 *전혀* 안 잡는 계면반응** — frame[5] 의 새 빈 칸 |
| **C_dl (이중층)** | ★ **CPE_int 분해** (84.2 µF 등, η 0.6–0.97) | ★ **우리 미보유** | 〃 |
| **고상확산 (Warburg)** | ★ **R_w/T_w/α 분해** (62: 215.5 Ω·cm², α 0.24–0.36) | ★ **우리 미보유** (D_Li 모델 없음) | ★ 활물질 내 Li 확산 = 우리 transport 솔버 밖; 자매 Kang FEM 은 D=3e-14 입력 |
| **활성화에너지 (T-의존)** | ★ **온도 스윕 → E_a 서열** (R_ct ≫ GB > 확산 > bulk) | ★ **우리 단일온도** (T-의존 σ 없음) | ★ **새 축** — T-dependent σ 가 우리 model extension 후보 |
| **소재** | **NCM811 + LPSCl** (= 우리 production 소재계 정확히) + 할라이드 LZC | NMC811 + LPSCl | ★ **동일** (Kang 2025 는 NCA, 이 논문은 NCM811 = 우리와 더 정확) → 추세 직접 비교 |
| **할라이드(LZC)** | bulk σ 0.51 (낮음) BUT R_ct 낮음 (안정 계면) | (할라이드 미모델; Varkey 2026 cross-ref) | ★ Varkey 할라이드(압밀/σ) ↔ 이 논문 할라이드(kinetics) = 같은 "안정하나 σ 낮음" |
| **CAM 코팅** | **LNO(LiNbO₃) vs uncoated** → R_ct ~20× 차 | coverage(Tabor/Hertz) = *기계* 접촉면적 | ★ LNO=*화학* 코팅(R_ct↓) ≠ 우리 coverage(기계); Kang LZO 와 같은 *화학* 패시베이션 계열 |
| **압밀 porosity** | **미측정** (펠릿 두께 L 만: 160–230 µm) | DEM 15.6 % / MPM 16.7 % | ★ **직접 비교 금지** (이 논문 정량 앵커 = 저항·두께·σ, porosity 아님) |
| **소성/morphology** | 없음 (회로 모델) | MPM 진짜 SHAPE 소성 | 우리 MPM 고유 (frame[5]) |
| **transport 채널** | σ_ion + σ_e + **R_ct + C_dl + 확산** (계면까지) | σ_ion + σ_e + σ_thermal (수송 삼중항) | ★ **상보**: 우리=수송 3채널 깊이, 그들=수송+계면+확산 폭 (우리 σ_thermal 그들엔 없음) |

**핵심 정합/상보 3가지:**
1. **bulk σ_ion(LPSCl) = 1.6 mS/cm = Minnmann 1.6** — 같은 소재 두 독립 측정 일치 → 우리 bulk 앵커 신뢰 보강.
2. **GB 가 bulk 와 동급 병목** — 그들이 *분리 측정*으로 우리 Cronau(r_SE) GB 인자를 정당화 (입계가 이온수송 주병목).
3. **R_ct·C_dl·확산·E_a 는 우리가 *전혀* 안 갖는 계면/확산 kinetics** — frame[5] 의 *새 빈 칸*(우리=수송 σ,
   그들=수송+계면반응+확산을 임피던스로 분해).

---

## 10. 적용 인사이트 (내 연구에 어떻게) — ★ 우리 랩 trend 정렬

- ① **TLM R_ion 을 우리 σ_ionic 의 *세 번째* 실험 앵커로 (직접, Bazzoun/Minnmann 와 합류)**:
  같은 NCM811+LPSCl 의 R_ion(대칭셀 bulk+gb: 62 **34.9** / 72 **48.1** / 82 **19.0** Ω·cm²) + bulk σ 1.6 mS/cm
  → 우리 σ_ionic 외부 검증점.  ⚠ **조성 매핑 필수**: 그들 wt%(62:37/72:27/82:17 = NCM811:LPSCl:SuperP) → vol%
  (density NCM811 ~4.77, LPSCl ~1.64) → 우리 φ_SE.  대략 62 wt% ≈ φ_SE 0.45–0.50, 82 wt% ≈ φ_SE 0.25 수준.
  ★ **단 "R_ion 이 깨끗이 분리된 셀"(대칭셀 또는 uncoated)의 값만** 쓸 것 (coated full-cell 은 R_ct 와 섞임 —
  §5.5 의 R_int/R_i 교훈).  → `docs/data/kim2025_tlm_kinetics_anchors.csv`.

- ② **GB 항을 우리 σ_ionic 에 *명시적*으로 (Cronau 인자 정당화 + 강화)**:
  그들이 **R_i,gb ≈ R_i,bulk 또는 더 큼**(62: 9.3 vs 25.6; uncoated 82: 59.7 vs 209.5)을 *분리 측정* → 우리
  Cronau(r_SE) GB 인자(현재 σ_grain prefactor 에 럼핑)가 옳은 방향임을 실험으로 확증.  ★ **흡수 후보**: GB 저항이
  *입경 의존*(작은 SE → GB 면적↑ → R_gb↑?)·*온도 의존*(GB 가 bulk 보다 큰 E_a)임을 우리 σ_grain 에 반영.  특히
  우리 grain-boundary-density 지표(σ_thermal Ridge feature 로 이미 사용)를 σ_ionic 으로도 끌어올 근거.

- ③ **R_ct(계면 전하전달) = 우리 *미보유* 칸 → frame[5] 의 새 축 명문화 (정직 목록)**:
  우리 σ-솔버는 **z₁(이온수송)만** 계산.  R_int(=R_ct)·C_dl·Warburg 는 우리가 *전혀* 안 다룬다.  → `our_dem_
  baseline.md §4` 와 `comparison_vs_ours.md F` 에 "**계면 전하전달·이중층·고상확산 kinetics = 우리 transport
  솔버 밖, EIS-TLM(Kim 2025) 영역**" 명시.  ★ **Kang 2025 의 D_Li=3e-14·LZO 패시베이션과 합쳐, "계면" 을 우리
  랩의 *공동 future 축*으로** (mechanics=Kang, kinetics=Kim, structure-σ=우리).

- ④ **T-dependent σ (활성화에너지) = 우리 model extension 후보 (신규 action)**:
  그들 온도 스윕 → **E_a(R_ct) > E_a(R_i,gb) > E_a(R_w) > E_a(R_i,bulk)** 서열.  우리 σ-솔버는 *상온 단일*.
  → ★ **σ_ionic(T) = σ_ionic(300K)·exp[−E_a/k(1/T−1/300)]** 형태로 T-축 추가 가능 (E_a 는 그들 GB ~0.6 eV·
  bulk 작음 추정값 — TREND-only).  우리 σ_thermal 은 *열전도*지 *전도도의 온도의존*이 아님 → **다른 축**.
  ⚠ E_a 절대값은 그들이 명시 표로 안 줌 → 우리가 쓰려면 *그들 R(T) 로 우리가 재-fit* 하거나 추세로만.

- ⑤ **자매 Kang 2025 와 *계면* 스토리 통합 (랩 trend 정렬)**:
  Kang = "NCA/LPSCl 분해 → Li-구배 → **균열**"(mechanics); 이 논문 = "NCM811/LPSCl 분해 → **R_ct↑ ~20×**"(kinetics).
  → **우리 deck/paper 에 "같은 황화물-계면 산화분해가 *역학*(균열, Kang)과 *kinetics*(R_ct↑, Kim) 양쪽으로
  나타나며, 우리 DEM+MPM 은 그 *구조→수송 σ* 를 채운다"** 는 3자 분업(structure-σ / mechanics / kinetics)을
  랩 trend 로 명문화.  LNO(Kim)·LZO(Kang) 둘 다 *화학* 코팅 → 우리 coverage(*기계*)와 종류 다름을 일관 유지.

- ⑥ **할라이드(LZC) kinetics ↔ Varkey 할라이드 압밀 통합 (cross-ref)**:
  이 논문 LZC = "낮은 σ(0.51) BUT 안정 계면(낮은 R_ct)"; Varkey 할라이드 = "stiffer E(10.58) → 높은 porosity floor".
  → **할라이드 = 압밀(Varkey) 도 kinetics(Kim) 도 황화물과 다른 trade-off** 를 한 줄로 (만약 우리가 할라이드로
  확장하면 E·σ·R_ct 셋 다 재보정 필요).

- ⑦ **도전제 형상(0D Super P vs 1D VGCF) → 우리 σ_e 도전제 항 (Lee 2025 와 합류)**:
  VGCF(1D) 가 전자저항·R_int 둘 다 낮춤 → 우리 σ_e 의 도전제 형상 구분 약함을 보강 (Lee 2025 VGCF σ_e 34 mS/cm
  과 같은 결).  단 우리 production 은 Super P(0D) 가정.

---

## 11. 인용 가능 문장 (deck/paper용)

- "Our group's modified transmission-line-model study (Kim, Kang, Park, Lee, Electrochim. Acta 2025) decouples
  the impedance of an NCM811/Li₆PS₅Cl composite cathode into **Li⁺/electron transport, interfacial charge
  transfer (R_ct), double-layer charging (C_dl) and solid-state Li diffusion (Warburg)** within a single
  ladder network, using two boundary conditions (ion-blocking and electron-blocking) to isolate each process —
  the experimental counterpart of our structural Kirchhoff/Holm σ_ionic solver, which captures only the ionic-
  transport rail."

- "The same EIS-TLM analysis shows that the **grain-boundary ionic resistance of cold-pressed LPSCl is
  comparable to or larger than the bulk** (e.g. R_i,bulk 9.3 vs R_i,gb 25.6 Ω·cm² at 62 wt% NCM811) and is
  more strongly thermally activated — providing direct experimental support for the Cronau(r_SE) grain-boundary
  factor in our σ_ionic prefactor."

- "Removing the LiNbO₃ coating raises the interfacial charge-transfer resistance of NCM811/LPSCl by **≈20×**
  (R_int 22→453 Ω·cm² at 62 wt%), attributed to oxidative interfacial decomposition — the kinetics-side
  signature of the very same sulfide-interface degradation that, in our group's companion paper (Kang & Shin
  2025), drives Li-gradient-induced intergranular cracking of the large cathode particles."

- "The bulk ionic conductivity of LPSCl measured here (1.6 mS cm⁻¹) coincides exactly with the Minnmann 2021
  value, anchoring our σ_grain calibration; the halide Li₂ZrCl₆ shows lower σ_ion (0.51 mS cm⁻¹) but markedly
  lower R_ct, consistent with the higher oxidative stability of halides (cf. Varkey 2026)."

- "Temperature-dependent EIS resolves an activation-energy hierarchy E_a(R_ct) > E_a(grain-boundary) >
  E_a(diffusion) > E_a(bulk-ion), identifying interfacial charge transfer as the most thermally activated
  (rate-limiting) process — a temperature axis our isothermal σ-solver does not yet carry."

---

## 12. 주의/한계 (over-claim 방지)

- **EIS-TLM 임피던스 논문 = 구조/압밀/역학 *미산출*.**  porosity·상대밀도·coordination·coverage·Heckel·PSD·E_SE
  를 **측정하지 않는다** (펠릿 *두께* L 만).  우리 압밀 앵커(Minnmann 14 %·Doux 18 %·우리 15.6 %)·역학과 **직접
  비교 금지** — 이 논문 정량 앵커는 *R_ion/R_ct/C_dl/Warburg/L/bulk σ/E_a* 다.
- **"시뮬레이션"은 DEM/MPM/FEM 아님** → modified TLM 등가회로 *해석해 + 파라메트릭 model simulation*.  미세구조를
  *생성하지 않고* 분포 임피던스로 추상화(구·형상·rigid/plastic 개념 없음).  우리 구조→σ 솔버와 *방법이 다름*
  (그들=주파수 영역 회로 피팅, 우리=공간 저항망 DC).  → frame[4] **외부 검증**이지 *경쟁 솔버* 아님.
- **R_ion 은 *측정+TLM 피팅* 값** → *예측 솔버* 산출 아님.  우리 σ_ionic(계산)과 비교 시 "그들=실험 진실, 우리=
  구조 예측" 으로 (frame[4]).  ⚠ **조성 wt%→φ_SE 매핑 선행** (62:37 wt% ≠ 우리 φ_SE 직접).
- **CAM = NCM811** (= 우리 production, Kang 2025 의 NCA 와 다름) → 이 논문은 *우리 소재와 더 정확히 일치*.  단
  **NCM811 grade·코팅(LNO)·입경**이 우리 시뮬 가정과 다를 수 있어 R_ion 절대값은 "같은 LPSCl + 같은 NCM811 계열"
  수준 정합으로 (입경 PSD 미보고 → 우리 12:4:1 가정과 직접 매칭 불가).
- **R_int/R_ct/C_dl/Warburg/E_a = 우리 *미보유* 칸** → 이걸 우리 σ-솔버가 "재현/검증" 한다고 말하면 *틀림*.
  우리는 z₁(이온수송)만 계산 → 이 논문이 분해한 *계면반응·확산*은 우리 모델 밖(frame[5] 빈 칸).  "우리가 이걸
  cross-validate" 가 아니라 "우리가 *안 갖는* 것을 실험이 보여줌" 으로 정직하게.
- **E_a 절대값은 *논문이 명시 표로 안 줌*** → §7 의 0.42 eV(R_ct)·0.6 eV(GB)는 **내가 R(T) 3점에서 Arrhenius 로
  추정한 digitized 값** (TREND-only, 3점 추정 오차 큼).  절대값 신뢰 말고 *서열·크기대*만 인용.
- **Fig 4f/5f/6b/6d 막대 라벨 ≠ 항상 Table fitted 값** → 막대 일부(예 62 wt% "336.8")는 R 이 아니라 **CPE 용량**
  값이 막대로 표시된 것.  **절대값은 Table S3–S6 verbatim 우선**, 막대 숫자는 digitized 로 구분.
- **할라이드(LZC) R_ct "낮음"은 *정성+상대*** → Fig 6g 비교(LPSCl 대비)이고 절대 fitted 값 표가 본 추출에 없음
  (LZC 두께 L=170 µm 만 stated).  "할라이드=낮은 R_ct" 는 추세로만.
- **bulk σ 1.6 vs 우리 Cronau 3.0** → 측정/입자/GB 차 → 절대 직접대조 금지, 범위로 (단 Minnmann 1.6 과 일치 = 신뢰).
- **압력 3종 구분** → 제조/압밀 250–433 MPa(porosity 결정) ≠ EIS 측정(셀 조립 상태) ≠ 작동압.  R_ion 은 *압밀된
  구조*를 측정한 값.  separator 433 MPa 는 우리 300·Minnmann 380 보다 약간 높은 고압.

---

## 13. 미니 용어집 (technique glossary)

- **TLM (Transmission Line Model)** — 다공·복합 매질의 *분포* 임피던스 모델.  이온/전자 두 레일을 무한개 미소
  RC 요소로 사다리망으로 짜고, crossrail(계면)로 결합.  단순 R∥C 병렬로 안 되는 복합 양극에 필수.  "modified" =
  GB·Warburg·charge-transfer 요소를 추가한 확장판.
- **ion-blocking / electron-blocking BC** — 셀 양 끝을 어느 전하종으로 막느냐.  ion-blocking(SUS) → 전하전달 없음
  (이중층만); electron-blocking(LPSCl 층) → 전하전달 발생(R_ct 살아남).  각 BC 가 다른 과정을 *고립*.
- **R_int = R_ct (charge-transfer resistance)** — Li⁺ + e⁻ 가 활물질 격자로 들어가는 *계면 반응*의 저항.  Nyquist
  *중주파 반원*의 지름.  계면분해층이 두꺼우면 급증(uncoated ~20×).
- **C_dl (double-layer capacitance) / CPE_int** — 계면 *비-faradaic* 전하축적.  실제론 이상 커패시터가 아니라
  **CPE**(constant-phase element, 지수 η<1 = 비균질 계면).
- **Warburg (generalized finite-length) z_w** — *고상 Li 확산* 임피던스.  Nyquist 저주파 45° 직선→수직선 전이.
  r_w=확산저항, T_w=확산 시상수, α=frequency-dispersion(0.5=이상).
- **DRT (Distribution of Relaxation Time)** — 임피던스를 시상수 τ 분포로 deconvolute → 겹친 과정을 peak 으로 분리.
  피팅 전 *등가회로 결정* + peak 의 물리 귀속(온도 스윕으로 이온-GB 확인).
- **grain boundary (GB) impedance** — cold-press 로 형성된 SE 입계의 이온수송 저항.  ★ 황화물에서 bulk 와 *동급*
  크기 + 큰 E_a → 주 병목.
- **3-electrode cell + Ag–Li RE** — WE(양극)/CE(In/Li)/RE(Ag–Li 합금) → 양극 임피던스만 고립(음극 제거).
- **Gerischer impedance** — 화학반응-coupled 확산의 임피던스 형태(45° 고주파 호) — 여기선 이온수송 영역의 거동.
- **R_int/R_i ratio** — 전하전달/이온수송 저항 비.  *클 때만* 두 영역이 Nyquist 에서 깨끗이 분리됨(Morasch);
  작으면 겹쳐서 full-cell 단독 분석이 오해를 부름 → 대칭셀 병용 필수.
- **LNO (LiNbO₃) coating** — CAM 표면 *화학* 패시베이션층(계면분해 억제 → R_ct↓).  Kang 2025 의 LZO 와 같은 계열.
- **LZC (Li₂ZrCl₆)** — 할라이드 SE.  낮은 σ_ion(0.51) BUT 높은 산화안정성(낮은 R_ct).
- **activation energy E_a** — Arrhenius ln σ = ln A − E_a/kT 의 기울기.  과정의 *온도 민감도* = 율속 진단.

---

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
