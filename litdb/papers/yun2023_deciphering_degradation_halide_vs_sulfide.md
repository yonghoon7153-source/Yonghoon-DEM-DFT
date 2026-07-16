# ⭐필독 / 우리-랩 / ★최애 — Deciphering the critical degradation factors of solid composite electrodes with halide electrolytes: Interfacial reaction versus ionic transport — Yun, Shin, Hoang, Kim, Choi, Kim, Jung, Moon, Lee (Energy Storage Materials 2023)

> slug `yun2023_deciphering_degradation_halide_vs_sulfide` · DOI `10.1016/j.ensm.2023.102787` · type `exp (impedance decoupling, SSRM/FS local mapping) + FEM (volume-change stress + SE crack propagation)` · PDF `Yun_2023_EnergyStorageMater_DecipheringDegradation_HalideVsSulfide_main.pdf` (+ `_SI.docx`) · digested `2026-06-26` · status ✅
>
> ## ★★★ 우리 랩(Hanyang, **Jong-Won Lee** 공동교신)의 **마지막 + 최애** 논문 — 6편 랩 시리즈의 *캡스톤* ★★★
> 저자 = **Jonghyeok Yun**ᵃ, **Hong Rim Shin**ᵇ (equal contribution), **Trung Dinh Hoang**ᶜ, **Siwon Kim**ᵃ,
> **Jae Hyuk Choi**ᵃ, **Beomsu Kim**ᵃ, **Hyuck Jung**ᵈ, **Janghyuk Moon**\*ᶜ (Chung-Ang Univ.), **Jong-Won Lee**\*ᵃ (Hanyang Univ.).
> 소속 = ᵃ Division of Materials Science and Engineering, Hanyang University · ᵇ Department of Energy Science and
> Engineering, DGIST · ᶜ Department of Energy Systems Engineering, Chung-Ang University · ᵈ COSMO AM&T.
> **Energy Storage Materials 59 (2023) 102787** (NRF-2018R1A5A1025594 + KEIT 20014581).
>
> ★ **이 논문이 왜 *캡스톤*인가 — 우리 랩 시리즈 6편을 *하나의 degradation map* 으로 묶는다:**
> 우리 랩(Lee 그룹)의 다른 5편이 각각 *한 축*을 봤다면, 이 논문은 그 축들을 **"interfacial-reaction × ionic-transport,
> material-dependent" 라는 2-축 열화 지도** 위에 통합한다.  공통 저자 사슬:
> - **Jonghyeok Yun** (이 논문 제1저자) ↔ Kang 2025·Cho 2024·Kim 2023(anode) 공저 → 랩 시리즈 *허브 인물*.
> - **Hong Rim Shin** (이 논문 공동1저) ↔ Kang 2025(공동1저)·Kim 2023(공저) → mechanics 라인 공통.
> - **Siwon Kim** ↔ Kim 2025(제1저자)·Cho 2024 → impedance-decoupling 라인 공통.
> - **Beomsu Kim** ↔ 본 논문 + (다른 랩 논문 공저).
> ⇒ 이 한 편이 **(1) 계면반응 R_int**(↔ Kim 2025 TLM·Cho 2024 CA 양면성), **(2) 역학 균열**(↔ Kang 2025 입자균열·Kim
> 2023 anode-strain), **(3) 단결정 NCM**(↔ Jung 2023 SC/PC morphology)을 *한 실험-FEM 프레임*에 모은다.
>
> ★ **우리에게 왜 중요한가 (3줄):** (1) **열화 인자가 *소재 의존*임을 임피던스 분해로 증명** — 황화물 LPSCl = *계면반응*(R_int↑,
> 저항성 interphase), 할라이드 LIC = *이온수송*(R_ion↑, **SE 자체의 가압 균열**).  → 우리 transport-σ 가 채우는 *구조→수송*
> 외에, **소재별로 *어느* 열화가 지배하는가**의 실험 지도. (2) **할라이드(LIC) = 우리 Varkey 2026 cross-check** — 거기선
> 할라이드가 *압밀/σ* 로 봤고, 여기선 *가압 균열*(LIC 가 압력으로 깨짐)로 본다; **할라이드 SE 가 깨지는 건 우리 모델에 *없는*
> 메커니즘**(우리 MPM SE 는 연성-소성, 취성-균열 아님). (3) **SSRM/FS = 우리 네트워크-σ + 접촉역학의 *실험 카운터파트*** —
> 그들은 국소 저항·모듈러스를 *측정*, 우리는 구조에서 *계산*.

---

## §0. ★ 이 논문의 위치 — 6편 랩 시리즈를 *2-축 열화 지도*로 통합하는 캡스톤 (이 절이 digest의 핵심 framing)

### 0.1 ★★ 랩 시리즈 6편 통합 — "interfacial-reaction × ionic-transport, material-dependent" 지도
이 논문의 두 결론(LPSCl=계면, LIC=이온수송)을 두 직교 축으로 보면, 우리 랩 6편이 모두 이 지도 위 한 점/한 축이 된다:

```
                        ↑ 계면반응(interfacial reaction) 축 (R_int↑)
                        |
   Kim 2025 (TLM)  ─────●  ★ 본 논문: NCM-LPSCl 여기 (계면, R_int 341.7→982.3)
   R_ct ~20× (uncoated) |     = 황화물 산화분해 → 저항성 interphase (P2Sx/Li2S)
   Cho 2024 (CA 양면성) |
   계면 부반응 ↔ σ_e     |
                        |
   ────────────────────●────────────────────→ 이온수송(ionic transport) 축 (R_ion↑)
                        |     ★ 본 논문: NCM-LIC 여기 (이온수송, R_ion 302.5→595.6)
   Kang 2025 (입자균열) |        = 할라이드 LIC 가압 *균열* → 이온경로 단절
   Kim 2023 (anode 변형)|     Varkey 2026 (할라이드 압밀, 외부)
   역학 균열 ↔ 응력      |
                        |
   Jung 2023 (SC/PC NCM): 양 축의 *입자 수준 토대* — 단결정 NCM 채택이 본 논문의 출발점
```

| 랩 논문 (slug) | 축 / 렌즈 | 본 논문과의 연결 |
|---|---|---|
| **★ 본 논문 (Yun 2023)** | **양 축 통합** + 소재 의존성 | LPSCl→계면, LIC→이온수송 을 *임피던스 분해*로 deciphering |
| `kim2025_impedance_decoupling_tlm_assb` | 계면 *kinetics* (modified TLM, R_ct) | 같은 *modified TLM 분해* 방법론; Kim 2025 가 R_ct↑(uncoated 20×)을 정량 → 본 논문 LPSCl *계면반응* 축의 정밀판 |
| `cho2024_conflicting_roles_conductive_additive` | 도전제(CA) 양면성 (σ_e↑ vs 계면부반응) | CA-SE 계면 산화부반응 ↔ 본 논문 NCM-SE 계면반응; 둘 다 *계면* 축 |
| `kang2025_toughened_bimodal_nca_lzo` | 역학 *균열* (입자균열, FEM cohesive) | 같은 *FEM cohesive-zone* 방법; Kang=*CAM 입자* 균열, 본 논문=*SE(할라이드)* 균열 → **균열 위치가 다름** |
| `kim2023_chemomech_failure_highstrain_anode` | 역학 (anode-strain → cathode 균열) | anode 고변형 → 복합양극 응력 균열 ↔ 본 논문 NCM 부피변화 → SE 응력 균열; 둘 다 *역학 균열* 축 |
| `jung2023_single_crystal_ncm_morphology` | 단결정(SC) vs 다결정(PC) NCM | 본 논문이 **단결정 NCM** 을 *일부러* 채택(NCM 균열 배제 → SE 열화만 깨끗이 관찰) → Jung 2023 의 SC 채택 논리의 *응용* |
> ★ **핵심 통찰:** 우리 랩은 *같은 황화물-계면*을 **mechanics(Kang/Kim2023) ↔ kinetics(Kim2025/Cho) ↔ 소재의존
> 열화지도(본 논문)** 세 렌즈로 입체 공략 중이고, **본 논문이 그 세 렌즈를 한 프레임(impedance decoupling + SSRM/FS +
> FEM)에 모은 *종합편*** 이다.  우리 DEM+MPM 은 이 지도에서 **"제조-순간의 구조→수송 σ"(이온수송 축의 *압밀 origin*)**
> 를 채운다 (frame[5]).

### 0.2 ★ 같은 *modified TLM 분해* 3-앵커 (Kim 2025 와 동일 방법, 같은 랩) + 본 논문의 추가
| 논문 | 그룹 | 소재 | TLM 이 *분해*하는 것 | 본 논문 대비 |
|---|---|---|---|---|
| Kim 2025 EA | Lee (Hanyang, 우리 랩) | NCM811+LPSCl(+LZC) | R_ion / R_int(R_ct) / C_dl / Warburg / E_a | 계면 *kinetics* 정밀판 (코팅·온도·조성) |
| Cho 2024 EA | Lee (Hanyang, 우리 랩) | NCM811+LPSCl, CA=VGCF | σ_e ↔ σ_ion 양면성 + 계면부반응 | 도전제 축 |
| **★ Yun 2023 (본 논문, *시간상 가장 이른* 2023)** | **Lee+Moon (Hanyang+CAU)** | **SC-NCM811 + LPSCl *vs* LIC(할라이드)** | **R_ion vs R_int 을 *두 SE 비교*로 분해 → 소재별 지배 열화 인자** | ★ **본 논문이 이 분해법의 *원조/씨앗*** — 2023 에 R_ion/R_int 분해로 *소재 의존 열화*를 처음 deciphering, Kim 2025(2025)·Cho 2024(2024)가 이를 정밀화/확장 |
> ★ **시간 순서 주의:** Yun 2023 이 *가장 이른* 논문(2023) → 이 논문의 R_ion/R_int 임피던스 분해가 **랩 TLM 라인의
> 출발점**이고, Cho 2024·Kim 2025 가 그것을 이어받아 정밀화한 셈.  (그래서 "마지막 + 캡스톤"은 *digest 순서/사용자
> 선호*상 마지막이지, *발표 연대*상으로는 시리즈의 *첫* 통합 논문이다 — 이 nuance 를 정직히 기록.)

---

## 1. 한 줄 요약
단결정(SC) NCM811 복합 양극을 **황화물 LPSCl** 과 **할라이드 LIC(Li₃InCl₆)** 두 SE 로 각각 만들어 사이클 열화를 비교하고,
**modified TLM 임피던스 분해**(이온수송 vs 계면반응) + **SSRM(국소 저항 3D 맵)** + **FS(국소 모듈러스 맵)** + **FEM(부피변화
응력 + SE 내 균열전파)** 로, **"열화의 *임계 인자*가 SE 소재에 따라 *다르다*"** 를 deciphering 한다:
- **NCM–LPSCl(황화물) → *계면반응* 으로 열화**: 황화물 산화분해 → NCM/LPSCl 계면에 **저항성 interphase(P₂Sₓ, Li₂S)** 형성 →
  **계면(전하전달) 임피던스 R_int 급증** (341.7 → 982.3 Ω·cm², +187%).
- **NCM–LIC(할라이드) → *이온수송* 으로 열화**: **LIC SE 자체가 가압 하에서 *균열/역학변형*** (NCM 반복 부피변화가 elastic-only
  LIC 계면에 응력 집중 → 균열) → **이온경로 단절 → Li⁺-수송 임피던스 R_ion 급증** (302.5 → 595.6 Ω·cm², ~2배).
→ "**할라이드 양극의 빠른 성능감쇠는 황화물의 통념(계면반응)과 *다른 인자*(SE 가압 균열에 의한 이온수송 손실)이다**" 가 결론.

---

## 2. 메타
| 항목 | 값 |
|---|---|
| 저자 | **Jonghyeok Yun**ᵃ, **Hong Rim Shin**ᵇ (equal), Trung Dinh Hoangᶜ, **Siwon Kim**ᵃ, Jae Hyuk Choiᵃ, **Beomsu Kim**ᵃ, Hyuck Jungᵈ, **Janghyuk Moon**\*ᶜ, **Jong-Won Lee**\*ᵃ |
| 소속 | ᵃ Materials Sci. & Eng., **Hanyang Univ.** · ᵇ Energy Sci. & Eng., **DGIST** · ᶜ Energy Systems Eng., **Chung-Ang Univ.** · ᵈ **COSMO AM&T** |
| 교신 | **jhmoon84@cau.ac.kr** (J. Moon, FEM) · **jongwonlee@hanyang.ac.kr** (J.-W. Lee) |
| 저널/년 | **Energy Storage Materials 59 (2023) 102787** (Received 2023-03-22, accepted 2023-04-21, online 2023-04-23) |
| DOI | **10.1016/j.ensm.2023.102787** |
| Keywords | All-solid-state battery · **Halide electrolyte** · **Interfacial impedance** · **Charge transport** · **Degradation** |
| CAM | **단결정(single-particle) NCM811 LiNi₀.₈Co₀.₁Mn₀.₁O₂** (size ~1–5 µm, smooth surface; COSMO AM&T) |
| SE (비교 2종) | **황화물 LPSCl = Li₆PS₅Cl** (mechanochem, Li₂S+P₂S₅+LiCl, 600 rpm 10 h ZrO₂) **vs 할라이드 LIC = Li₃InCl₆** (LiCl+InCl₃ 600 rpm 3 h → 260 °C 진공 12 h anneal) |
| 도전제 | **Super P** |
| 복합 양극 | **NCM : SE : Super P = 72 : 27 : 1 wt%** (ball-mill 250 rpm 48 h, ZrO₂) |
| 셀 | (a) **이온차단 대칭셀** [SUS \| 복합양극 \| SUS]; (b) **풀셀** [SUS \| 복합양극 \| LPSCl separator \| In/Li \| SUS] |
| 압력 | SE separator(LPSCl 100 mg) **433 MPa** · 분말혼합층 한쪽에 가압 · In(100 µm)/Li(200 µm) 적층 후 SUS(10 µm Cu) 삽입 → **250 MPa** |
| 두께 | SE separator **~200 µm**; ⌀10 mm PEEK mold, SUS current collectors |
| 측정 | 갈바노 사이클 **2.5–4.3 V vs Li/Li⁺, 30 °C**; formation **0.05C×2**(CC-CV charge to 4.3 V, CV cutoff 0.01C) → cycling **0.33C**; rate **0.1–2C**. EIS: Biologic SP-300, **7 MHz–1 mHz**, 5 mV amplitude |
| 분석 | XRD(Cu Kα), XPS(Al Kα ESCALAB 250Xi), SEM/EDS(Hitachi S-4800), 단면 BSE-SEM(Ar cross-section polish, Hitachi ArBlade5000), GITT |
| 국소 맵 | **SSRM**(AFM, Park NX-10, log amp, +2.5 V DC, Pt-coated CONTSCPt tip, dry room, 2×2 µm) + **FS**(tapping-mode AFM, PPP-NCHR Si probe, 5×5 µm, 256×256, 0.2 Hz, DMT fit) |
| 계산 | **FEM**(부피변화 응력 + SE 균열전파; Voronoi SE 10 µm 유효, 도메인 12.55 µm, cohesive-zone bilinear traction-separation, B-K criterion) |
| 연구유형 | **실험**(전기화학 + SSRM/FS 국소 맵 + XRD/XPS) **+ FEM**(응력·균열) |

---

## 3. 핵심 물성 (수치)

> ⚠ 이 논문은 *압밀 porosity*·*상대밀도*·*coordination*·*coverage*·*Heckel*·*PSD* 를 측정·보고하지 **않는다**(열화-메커니즘
> 논문).  그 칸은 n/a — 우리 압밀 앵커(Minnmann 14 %, Doux 18 %, 우리 15.6 %)와 *직접 비교 금지*.  이 논문의 정량 앵커는
> **분해된 임피던스 R_ion/R_int(Table S1) · 두 SE bulk σ · FS 국소 모듈러스 E · FEM σ_Mises/균열 · rate/cycling 용량** 이다.
> ★ 모든 fitted 임피던스는 **SI Table S1 verbatim**; 본문 Fig 2 막대는 그 시각화(읽은 막대값은 digitized 로 구분).

### 3.1 ★★ 분해된 임피던스 (modified TLM, Table S1) — 이 논문의 *심장*
| 시스템 | 상태 | **R_ion** (Ω·cm²) | **R_int** (Ω·cm²) | 지배 열화 |
|---|---|---|---|---|
| **NCM–LPSCl** | before cycling | 126.1 | 341.7 | — |
| **NCM–LPSCl** | **after cycling** | 155.6 (+23 %) | **982.3 (+187 %)** | ★ **계면반응** (R_int 폭증) |
| **NCM–LIC** | before cycling | 302.5 | 65.2 | — |
| **NCM–LIC** | **after cycling** | **595.6 (+97 %, ~2×)** | 113.8 (+75 %) | ★ **이온수송** (R_ion 2배) |
> ★★ **이 4×2 표가 논문 전체의 결론을 한 눈에 담는다:**
> - **LPSCl**: 사이클 후 **R_int 가 R_ion 의 *6배 이상*** (982 vs 156) + R_int 증가폭(+641)이 R_ion 증가폭(+30)의 *20배* →
>   **계면(전하전달)이 열화 지배 인자** = 저항성 interphase 형성.
> - **LIC**: 사이클 후 **R_ion 이 R_int 의 *5배*** (596 vs 114) + R_ion 증가폭(+293)이 R_int 증가폭(+49)의 *6배* →
>   **이온수송이 열화 지배 인자** = SE 가압 균열로 이온경로 단절.
> - **대칭(symmetry):** LPSCl 은 R_int↑·R_ion 안정 / LIC 는 R_ion↑·R_int 안정 — *정확히 반대* 시그니처 → "소재 의존".
> - **pristine 도 정보:** LIC 는 pristine R_int 가 낮음(65.2 ≪ LPSCl 341.7) = *처음부터* 계면이 안정(할라이드 산화안정성);
>   LIC pristine R_ion 이 높음(302.5 ≫ LPSCl 126.1) = 할라이드의 *낮은 bulk σ*(1.2 vs 1.6) 반영.

### 3.2 SE 이온전도도 + 가압 거동 (Fig 4a,b)
| 물성 | 값 | 조건 | src | 비고 |
|---|---|---|---|---|
| **bulk σ_ion (LPSCl)** | **1.6 mS/cm** | 25 °C | stated | = Minnmann 1.6 / Kim2025 1.6 (랩 자체 측정 일치) |
| **bulk σ_ion (LIC)** | **1.2 mS/cm** | 25 °C | stated | 할라이드; LPSCl 의 ~0.75× |
| ★ **σ_ion(LIC) under pressure** | **1.2 → 0.6 mS/cm** (over 240 h) | 250 MPa 펠릿 | stated (Fig 4b) | ★★ **가압 하 *시간에 따라 반감*** — 균열-유발 |
| ★ **σ_ion(LPSCl) under pressure** | **1.6 (변화 없음)** | 250 MPa 펠릿 | stated (Fig 4b) | ★ **안정** — 대조군 |
| σ_ion(LIC) **무가압** Ar 보관 | **손실 없음** | 동일 기간, 무가압 | stated (Fig S9) | ★ **손실 = *압력* 때문**(역학) ≠ 화학/상전이 |
> ★ **핵심 실험 논리(Fig 4a,b + S8,S9):** LIC σ_ion 감소가 (i) 구조/상전이? → XRD(Fig S8) *변화 없음* → 배제; (ii) 조성변화? →
> 배제; (iii) 무가압 보관? → *손실 없음*(S9) → **남는 원인 = 가압 하 역학(균열)** → "LIC 의 σ 손실은 *기계적 특성*에서 온다".

### 3.3 국소 모듈러스 (FS force-spectroscopy, Fig 4c–f) — ★ 균열의 *직접* 역학 증거
| 물성 | 값 | 조건 | src | 비고 |
|---|---|---|---|---|
| **E_mean (LPSCl, pristine)** | **~32.8 GPa** | FS, DMT fit | stated (Fig 4e) | FEM 입력과 일치 |
| **E_mean (LIC, pristine)** | **~41.1 GPa** | FS | stated (Fig 4d) | ★ LIC 가 LPSCl 보다 *더 단단* |
| **E_mean (LPSCl, 가압 후)** | **~29.3 GPa** | FS, after pressure | stated (Fig 4f) | ★ **거의 변화 없음**(32.8→29.3) |
| **E_mean (LIC, 가압 후)** | **~19.8 GPa** | FS, after pressure | stated (Fig 4d) | ★★ **−52 % 급락**(41.1→19.8) = 균열/역학손상 |
> ★ FS 가 **국소 nanoindentation**(intrinsic 모듈러스, 적용 힘·면적이 macro 보다 훨씬 작음) → bulk macro 시험보다 큰 E 측정.
> **LIC 가 *처음엔 더 단단*(41.1)했는데 가압 후 *반토막*(19.8)** = LIC 가 가압으로 *깨졌다*는 직접 증거.  LPSCl 은 가압에도
> 모듈러스 유지(plastic 으로 흐를 뿐 안 깨짐).  SEM(Fig S10)이 가압 LIC 의 microscale crack 을 추가로 보여줌.

### 3.4 FEM 입력 모듈러스 / 부피변화 / 균열 파라미터
| 물성 | 값 | src | 비고 |
|---|---|---|---|
| **E_NCM** | **175 GPa** | stated (FEM) | = Kang 2025 E_NCA 175; 우리 NMC811 가정 140 과 다름 |
| **E_LPSCl** | **32.8 GPa** | stated (FEM) | ★ **within-corpus 불일치**: 32.8 *vs* Bazzoun/Kang2025/Kim2025 의 22.1 *vs* 우리 real ~24 (§10 플래그) |
| **E_LIC** | **41.1 GPa** | stated (FEM) | 할라이드; LPSCl 보다 stiffer |
| NCM 부피변화 | **5.9 %** | stated (ref 38) | full delitiation/lithiation |
| 부분몰부피 Ω | **1.338×10⁻⁶ m³/mol** | stated | ε = Ω/3 · Δc (확산유발 strain, thermal-strain 유추) |
| **LPSCl 항복강도** | "**200 GPa**" (본문 그대로) | stated_text ⚠ | ★★ **물리적 오타로 강하게 의심 → 200 MPa** (항복강도 200 GPa > 모듈러스 32.8 GPa 는 불가능; §10) |
| G_c (crack-tip opening) | **0.5–3 J/m²** (parameterized) | stated | sulfide SE known **2.93 J/m²** (ref 40 Smith) |
| GB 계면강도 | **grain 내부보다 30 % 약함** | stated | (Kang 2025 의 "100 MPa 고정"과 다름 — 여기는 *30 % 감쇠 규칙*) |
| 도메인 / Voronoi NCM | **12.55 µm / 10 µm** | stated | 부피분율 매칭; Voronoi tessellation SE grain |

### 3.5 미측정/n/a (우리 압밀 앵커와 직접대조 금지)
| 항목 | 상태 |
|---|---|
| porosity / 상대밀도 / coordination Z / coverage | **n/a** (열화 논문, 미측정) |
| Heckel / P_y / 압밀곡선 | **n/a** |
| σ_y(정량, MPa) / 경화 | **n/a** (LPSCl "200 GPa" 오타만) |
| PSD (D10/D50/D90) | **n/a** (SE ~5 µm, NCM ~1–5 µm 정성만) |
| σ_thermal / σ_electronic 절대값 | **n/a** (SSRM 은 *상대* 저항맵) |

---

## 4. 시뮬레이션 방법 ★ — FEM(부피변화 응력 + SE 균열전파) + 임피던스 등가회로(modified TLM)

> ★ 이 논문엔 **두 종류의 "계산"** 이 있다: (A) **FEM** — NCM 부피변화가 만드는 응력 + **SE *내부* 균열전파**(cohesive-zone);
> (B) **modified TLM 등가회로 피팅** — 임피던스를 R_ion/R_int 로 분해(Kim 2025·Cho 2024 와 같은 방법).  DEM/MPM 은 없다.
> ⇒ frame[5]: 그들 FEM = *사이클 중 균열 역학*(우리 Auerbach 와 유사하나 *SE* 균열), 그들 TLM = *임피던스 측정 분해*(우리
> Kirchhoff/Holm σ-솔버의 실험 카운터파트).  우리 DEM+MPM 은 *제조-순간 구조→수송*(이온수송 축의 *압밀 origin*).

### 4.1 ★ FEM — 부피변화 응력 + SE 균열전파 (Supplementary Note 2,3; Fig 5, S2, S11, S12)
이 논문 FEM 의 핵심은 **균열이 *SE 상(phase)* 안에서 전파**한다는 점 — Kang 2025(CAM 입자 균열)와 **균열 위치가 다르다**.

- **기하 (Fig S2):** **Voronoi tessellation** 으로 SE grain 생성, 그 사이에 NCM 입자를 부피분율(72:27 → vol% 환산) 맞춰 패킹.
  NCM 유효크기 **10 µm**(단결정 ~1–5 µm 이나 패킹 매칭용), 도메인 **12.55 µm 정사각**.  각 grain 을 submicron 으로 discretize,
  **2차 Voronoi tessellation 의 edge(=grain boundary)에 cohesive-zone 요소** 삽입 → *grain 내부* 균열경로까지 표현.
- **하중 = NCM 부피변화 (thermal-strain 유추):** NCM 의 Li 삽입/탈리 → 부피 5.9 % 변화 → 확산유발 strain
  **ε = Ω/3 · Δc** (Ω = 1.338×10⁻⁶ m³/mol).  순수 *역학* 변형만 고려(delitiation by NCM).
- **모듈러스:** E_NCM 175, E_LPSCl **32.8**, E_LIC **41.1** GPa.  **LPSCl = elastic-plastic**(점탄성/소성, ref 54 Papakyriakou,
  항복강도 "200 GPa"=오타→200 MPa), **LIC = elastic-only**(소성 없음 가정).  ★ 이 *변형 모드 차이*가 결과를 가른다.
- **균열모델 = cohesive-zone (CZM), bilinear traction-separation (Supplementary Note 3):**
  - **(damage 개시)** quadratic nominal stress: `⟨σ_n⟩/σ_n^c + σ_s/σ_s^c = 1` (⟨⟩=Macauley, 압축 σ_n≤0 은 0).
  - **(혼합모드 변위)** `d_m = √(d_n² + d_s²)`; 개시 변위 `d_m0` (mode-mixing 식).
  - **(손상 후 traction)** `σ_i = (1−d)·K_i·d_i`, d = debonding index 0→1.
  - **(최종 파괴)** **Benzeggagh–Kenane (B-K) criterion**: `G_c = G_n^c + (G_s^c − G_n^c)·{G_s/(G_n+G_s)}^η`.
  - 입력: **G_c parameterized 0.5–3 J/m²**(sulfide 알려진 값 2.93), **GB 계면강도 = grain 내부의 70 %**(30 % 약화).
- ⇒ ★ **우리 Auerbach(접촉응력→AM 균열) 와의 차이:** (1) **균열 위치** — 우리=*AM 입자*, 그들=*SE grain/GB*.
  (2) **모델** — 우리=Auerbach 통계적 임계응력(파편 개수), 그들=cohesive-zone 결정론적 traction-separation(균열경로 추적).
  (3) **하중** — 우리=*접촉/가압* 응력, 그들=*Li 부피변화* 응력(사이클).

### 4.2 ★ FEM 결과 (Fig 5) — *왜* 소성이 균열을 줄이나 (이 논문 역학 결론의 핵심)
- **Fig 5a (NCM-LPSCl, full lithiation):** σ_Mises 가 **넓은 영역에 *재분포*, 값이 낮음(<0.2 GPa)** → **plastic LPSCl 이
  응력을 흩뿌림** → 균열 driving force↓ → **균열 *적음*** (Fig 5a 우: gray GB 에 빨강 균열 *소수*).
- **Fig 5b (NCM-LIC, full lithiation):** elastic-only LIC 는 **응력 재분포 불가 → NCM/LIC 계면에 *집중*, 값 큼(>0.5 GPa)** →
  균열 driving force↑ → **균열 *많음*** (Fig 5b 우: 빨강 균열 *다수*, intergranular).
- **Fig 5c (모식):** LPSCl 측 = Li⁺/e⁻ 경로 + 얇은 *저항성 interphase*(연두, P₂Sₓ/Li₂S); LIC 측 = grain 사이 *균열*(검정 선)이
  Li⁺ 경로를 끊음.  ⇒ **두 열화의 *공간적* 그림**: LPSCl=계면 *층*, LIC=SE *균열*.
- **SI Fig S11 (elastic-only 가정만):** LPSCl·LIC *둘 다 elastic* 으로 두면 균열 패턴·총 균열길이가 *비슷* → **차이는 *재료 elastic
  모듈러스* 가 아니라 *소성 유무*에서 온다**는 결정적 통제실험.
- **SI Fig S12 (elastic-plastic LPSCl vs elastic-only LIC):** 실제 가정(LPSCl 소성, LIC 탄성)으로 가면 **LPSCl 균열 ≪ LIC 균열** →
  소성이 균열을 줄인다는 결론.
- ⇒ ★★ **결론:** "**LPSCl 의 *소성*이 응력을 재분포시켜 균열을 줄이는 반면, LIC 의 *탄성-only* 거동은 계면에 응력을 쌓아
  균열을 키운다**" → **할라이드는 ESW(전기화학 안정창)뿐 아니라 *역학적 가소성*도 개선해야** (저자 제언: dopant/구조변형으로
  가압 하 *intimate contact* 유지하면서 산화안정성 보존).

### 4.3 ★ modified TLM 임피던스 분해 (Fig 2a) — Kim 2025·Cho 2024 와 같은 방법
- **회로 (Fig 2a):** 복합 양극 = 분포 임피던스 사다리.  **r_ion**(이온 레일, SE 상) + **r_ele**(전자 레일, CAM/도전제) 두 레일을
  **crossrail z_int** 로 결합; z_int = **r_int(전하전달) ∥ cpe_int(이중층)** + **z_w(Warburg, NCM 고상확산)** (Fig 2a inset).
  - = Kim 2025 의 z₁/z₂/z₃ 토폴로지와 동일(같은 랩 같은 방법).  단 본 논문은 **두 SE(LPSCl/LIC)** 를 비교하는 데 초점.
- **두 셀 BC:** (a) **이온차단 대칭셀**[SUS\|양극\|SUS] → 전자/이온 *수송* 고립; (b) **풀셀**[SUS\|양극\|LPSCl\|In/Li\|SUS] →
  전하전달(R_int) 발생.  → 측정 스펙트럼을 TLM 등가회로에 피팅해 **R_ion / R_int / CPE_int / Warburg 를 분해**(Table S1).
- ⇒ ★ **우리 σ_ionic 솔버는 r_ion(이온수송)만 계산** — r_int(전하전달)·cpe_int(이중층)·z_w(고상확산)는 *우리 미보유*
  (frame[5]).  본 논문 R_ion = 우리 σ_ionic 의 실험 카운터파트(소재 같음).

### 4.4 입자 처리 ★ (DEM판 "무질서 처리" 관점)
- **FEM 측:** SE = **Voronoi 다결정 grain 집합** + **cohesive-zone GB 분리** — *입자 형상은 고정*, **GB 가 *균열*로 갈라짐**
  (Kang 2025 와 동형: 진짜 SHAPE 변형 아님, *취성 박리/균열*).  NCM = rigid-ish elastic 입자.  ⇒ **우리 MPM 의 *연성 J2
  소성 형상흐름*과 정반대 파괴양식**: 그들=*취성 cohesive 균열*, 우리=*연성 소성 void-fill*.  ★ 단 LPSCl 은 *elastic-plastic*
  으로 둬서 "소성 재분포"를 표현 → 우리 MPM 소성과 *개념적으로 가장 가까운* 랩 모델(연속체 소성).
- **TLM 측:** 입자 형상·PSD·rigid/plastic 개념 *없음* — 복합양극을 분포 임피던스 *연속 사다리*로 추상화(L, r_ion, r_int 만).
  구조는 *측정된 lumped R* 로만 들어옴(Kim 2025 와 동일).
- ⇒ ★ **우리 DEM(구·접촉망)·MPM(소성 형상)의 *명시적 미세구조*가 이 논문엔 두 형태 모두 *없다*** — FEM 은 Voronoi
  연속체, TLM 은 lumped 회로.  frame[5]: 우리 = 구조→σ; 그들 = 균열역학(FEM) + 측정분해(TLM).

### 4.5 도메인 / 압력 / seeds
- FEM: 12.55 µm 정사각 도메인, Voronoi SE(submicron discretize) + 10 µm NCM, 단일 실현(lithiation degree sweep).
- 실험: ⌀10 mm PEEK mold; SE separator 100 mg **433 MPa**; full cell **250 MPa**; In(100 µm)/Li(200 µm); SUS(Cu 10 µm).
- ★ **압력 구분(우리 인식과 합류):** 제조/압밀 = **250–433 MPa**(separator 433 = Minnmann 380·Doux 370 보다 약간 높은 고압) ≠
  *측정/aging* 압(LIC σ 측정은 250 MPa 펠릿을 *유지*한 상태에서 240 h) ≠ 작동압.  ★ **단 본 논문의 핵심은 *작동/aging 중에도
  유지되는 가압*(250 MPa)이 LIC 를 *서서히* 깬다는 점** — "제조 순간 가압"만이 아니라 *지속 가압*이 할라이드엔 치명적.

---

## 5. 결과 상세 — Section-by-section (모든 수치)

### 5.1 §3 도입부 — 재료/셀 + 단결정 NCM 채택 이유 (Fig 1a, S3–S7)
- **두 SE (Fig S3,S4,S5):** LPSCl·LIC 둘 다 mechanochem, 입경 ~5 µm(SEM).  bulk σ: LIC **1.2**, LPSCl **1.6** mS/cm(Fig S4 Nyquist).
  XRD(Fig S5): LIC=monoclinic(ICSD 418,490), LPSCl=cubic(ICSD 04-009-9027), 불순물 없음.
- **단결정 NCM (Fig S6):** size ~1–5 µm, smooth surface.  ★ **일부러 *기계적으로 robust 한 단결정* 채택** → 사이클 중 NCM
  *균열/pulverization* 을 배제 → **SE 가 만드는 열화만 깨끗이 관찰** (= Jung 2023 SC 채택 논리의 응용).
- **초기 충방전(Fig S7,1a):** NCM-LPSCl 은 첫 충전 시 *낮은 전압*(sagging) — **NCM/LPSCl 계면 부반응** 흔적(ref 44,45);
  NCM-LIC 은 sagging *없음* → **NCM/LIC 계면 *전기화학 안정***.

### 5.2 §3 rate capability + cycling (Fig 1b,c,d) — 두 열화의 *거시* 시그니처
- **Fig 1b,c (rate 0.1–2C):**
  - **저율(0.1–1C):** ★ **NCM-LIC 가 더 큰 용량** (초기 방전 **197.7** vs LPSCl **186.4** mAh/g; ICE **89.5** vs **84.5 %**) —
    안정한 NCM/LIC 계면.
  - **고율(2C):** ★ **NCM-LPSCl 이 *역전* 우세** — LIC 은 큰 분극(charge-discharge gap)·작은 용량.  이유 = **고율에선 *이온수송*이
    율속** → LIC 의 낮은 Li⁺ 전도가 병목; LPSCl 은 *큰 과전압*이 계면 전하전달을 밀어붙여 극복(kinetics of interfacial charge
    transfer enhanced by large driving force).  → **rate 거동이 이미 "LIC=이온수송 한계 / LPSCl=계면 한계"를 예고**.
- **Fig 1d (cycling 0.33C, 100 cyc):**
  - **NCM-LIC:** 초기 용량 *높으나*(파랑) **더 빠른 감쇠** → 100 cyc 후 **140.4 mAh/g, 유지율 75.7 %**.
  - **NCM-LPSCl:** 초기 낮으나(빨강) **더 안정** → 100 cyc 후 **138.5 mAh/g, 유지율 84.7 %**.
  - ⇒ ★ "**할라이드 양극이 *빠르게* 감쇠**" 가 본 논문이 푸는 현상.  CE: LIC 가 약간 높은 ICE 였으나 cycling 감쇠는 더 빠름.

### 5.3 §3 ★★ 임피던스 분해 (Fig 2) — 핵심 결론의 정량 근거
- **Fig 2a:** TLM 등가회로(r_ion / r_ele / z_int = r_int∥cpe_int + z_w).  §4.3.
- **Fig 2b (Nyquist, before/after, 두 시스템 + 막대):**
  - **NCM-LPSCl:** before 작은 호 → **after *크게 확대*** (특히 *계면* 반원) → **R_int 341.7 → 982.3** (Ionic/Interfacial 막대).
  - **NCM-LIC:** before 작은 호 → **after *이온수송* 영역(고주파 45°+) 확대** → **R_ion 302.5 → 595.6**.
  - **막대(Fig 2b 우):** "Ionic"·"Interfacial" 두 패널 — LPSCl=Interfacial 막대가 after 에 폭증(빨강), LIC=Ionic 막대가 after 에
    2배(파랑).  → **시각적으로 *정확히 반대* 패턴**.
- ★ **본문 3 포인트(저자 정리):**
  1. **pristine:** NCM-LIC 가 더 낮은 r_int(1.3 Ω·cm³) — 안정 계면; 그러나 더 높은 r_ion(15125 Ω·cm³, LPSCl 6.8) — 낮은 σ.
  2. **r_ion 사이클 후:** NCM-LIC **15125 → 29780 Ω·cm³ (~2배)**; r_int 도 약간↑(6305→? — LPSCl 측 6.8→19.6).
  3. **r_int 사이클 후:** NCM-LPSCl **6.8 → 19.6 Ω·cm³ 로 크게↑** (본문, 단위/스케일은 본문 서술 기준).
  - ⇒ ★ "**degradation behaviors are governed by *different* critical factors: Li⁺ transport for NCM-LIC versus interfacial
    reactions for NCM-LPSCl**" (본문 명시 = 논문의 thesis 문장).

### 5.4 §3 SSRM + XPS (Fig 3) — *국소 저항맵* 으로 interphase 유무 확인
- **Fig 3a (NCM-LPSCl, after cycling):** 2D/3D SSRM 맵 — NCM 상(녹-청, <10 kΩ·cm) + SE 상(빨강, 극히 높음).
  **line scan(A–A'):** ★ **interfacial region(~50 nm) 에서 resistivity *연속 변화*** → **저항성 interphase 존재**(NCM↔SE 사이에
  중간 저항층).
- **Fig 3b (NCM-LIC, after cycling):** line scan(B–B'): ★ **resistivity *불연속*(discontinuity), 유한거리 연속변화 *없음*** →
  **interphase *없음*** (NCM/LIC 계면이 깨끗) — SSRM 이 *공간적으로* "LIC 계면 안정"을 확인.
- **Fig 3c (XPS, NCM-LPSCl):** P 2p — pristine 131.9/132.7 eV(argyrodite+phosphate); **after: P₂Sₓ(132.8)+phosphate(133.7)
  *새 peak*** = LPSCl 산화분해; S 2p — **Li₂S, P₂Sₓ** 생성 → ★ **저항성 interphase 의 화학 정체 = P₂Sₓ + Li₂S**.
- **Fig 3d (XPS, NCM-LIC):** In 3d·Cl 2p — ★ **사이클 후에도 *변화 없음*** → LIC *전기화학 안정*(분해 없음) → SSRM 의
  "interphase 없음"과 일치.
- ⇒ ★ **SSRM(저항맵) + XPS(화학) 가 *서로*, 그리고 *임피던스 분해*와 일치**: LPSCl=interphase 형성(R_int↑) / LIC=계면 안정 →
  **"LPSCl 열화=계면반응" 을 세 독립 방법(임피던스·SSRM·XPS)이 교차확인**.  여기서 *역설*이 남음: "그럼 *왜* LIC 의 Li⁺ 수송이
  나빠지나?" → §5.5 (가압 균열)로 답.

### 5.5 §3 ★★ 가압-유발 LIC σ 손실 → 균열 (Fig 4) — LIC 열화의 *기전* 규명
- **Fig 4a,b (SE-only 펠릿, 250 MPa, 240 h):** ★ **LIC σ_ion 1.2 → 0.6 mS/cm (반감)** over 240 h; **LPSCl 1.6 *유지***.
  → "**r_ion 증가의 원인 = 가압 하 σ 손실**".
- **원인 배제 (S8,S9):** (i) 구조/상전이? XRD(S8) *불변* → 배제; (ii) 조성변화? 배제; (iii) **무가압 Ar 보관(S9)? *손실 없음*** →
  ⇒ **남는 원인 = 가압 하 *역학*(deteriorated solid-solid contacts = 균열)**.
- **Fig 4c–f (FS 모듈러스 맵):** §3.3.  ★ **LIC E 41.1 → 19.8 GPa(−52 %, 가압 후)**; LPSCl 32.8 → 29.3(거의 불변).
  + **SEM(S10):** 가압 LIC 의 microscale crack *직접 관찰*.
- ⇒ ★★ **"LIC 의 *기계적 취약성*(가압 균열) → solid-solid contact 악화 → 이온경로 단절 → r_ion↑"** — LIC 열화의 *역학적*
  기전.  이게 **임피던스 분해(R_ion↑)의 *물리적 원인*** 이고, **할라이드 특유의 새 열화축**(황화물엔 없음).

### 5.6 §3 FEM (Fig 5) — *왜* LPSCl 소성이 균열을 막나
- §4.2 전체.  요지: **LPSCl 소성 → 응력 재분포(<0.2 GPa) → 균열 적음**; **LIC 탄성-only → 계면 응력 집중(>0.5 GPa) → 균열
  많음**.  통제실험 S11(둘 다 elastic → 비슷) / S12(LPSCl 소성 vs LIC 탄성 → LPSCl 균열 ≪) 가 "차이=소성 유무"를 못박음.
- ⇒ ★ **FEM 이 §5.5 의 실험(LIC 균열)을 *기전*으로 설명**: NCM 반복 부피변화 → elastic LIC 계면 응력축적 → cohesive 균열 →
  이온경로 단절.  → "**SE 의 *변형거동*(소성 vs 탄성)이 복합양극 균열을 좌우**".

### 5.7 §4 결론 (저자 요약)
- 임피던스 분해 + SSRM + FS + FEM 로 **할라이드/황화물 양극의 *임계 열화 인자*가 다름** 을 demonstrate:
  - **NCM-LPSCl** → **저항성 interphase 형성**(계면반응) → R_int↑.
  - **NCM-LIC** → **가압 하 LIC 의 *cracking-유발 역학변형*** → 이온경로 단절 → R_ion↑.
- FEM: **SE 변형거동이 균열 형성/전파를 좌우** — LIC 의 *탄성* 거동이 NCM 부피변화로 인한 균열에 취약.
- → "**고출력·장수명 ASSB 를 위한 *소재·전극 설계* 통찰**" (할라이드는 ESW + *역학가소성* 둘 다 개선 필요).

---

## 6. Figure / Table set ★ (모든 그림·표 + 우리가 쓸 점)

### 6.1 본문 Figures
| Fig | 내용 (무엇을 보여주나) | 핵심 수치 | 우리가 참고할 점 |
|---|---|---|---|
| **1a** | ASSB 모식 (NCM-LPSCl vs NCM-LIC 복합양극 + Li⁺/e⁻ 경로) | 72:27:1 | 두 SE 비교 셋업 |
| **1b** | NCM-LPSCl rate (0.1–2C) 전압프로파일 | 0.1C 186.4; 2C 우세 | ★ 고율=LPSCl 우세(계면 driving force) |
| **1c** | NCM-LIC rate | 0.1C 197.7; 2C 열위 | ★ 고율=LIC 열위(이온수송 병목) |
| **1d** | cycling 100 cyc 0.33C (용량유지+CE) | LPSCl 84.7 %·LIC 75.7 % | ★ LIC 더 빠른 감쇠(푸는 현상) |
| **2a** | modified TLM 등가회로 (r_ion/r_ele/z_int) | — | ★ Kim 2025 토폴로지; 우리 솔버 임피던스판 |
| **2b** | Nyquist before/after (두 시스템) + Ionic/Interfacial 막대 | ★ R_int(LPSCl)·R_ion(LIC) 폭증 | ★★ **핵심 결과 — 정확히 반대 패턴** |
| **3a** | SSRM 2D/3D + line scan (NCM-LPSCl after) | ~50 nm 연속변화 | ★ **interphase 존재(저항맵)** |
| **3b** | SSRM (NCM-LIC after) | 불연속 | ★ **interphase 없음** |
| **3c** | XPS P2p/S2p (NCM-LPSCl) | P₂Sₓ·Li₂S 생성 | ★ interphase 화학정체 |
| **3d** | XPS In3d/Cl2p (NCM-LIC) | *불변* | ★ LIC 전기화학 안정 |
| **4a** | LPSCl SE-only Nyquist + σ(t) (240 h, 250 MPa) | σ 1.6 유지 | 대조군(안정) |
| **4b** | LIC SE-only Nyquist + σ(t) | ★ σ 1.2→0.6 | ★ **가압 하 반감(균열)** |
| **4c,e** | LPSCl FS 모듈러스 맵 (pristine/가압) | 32.8 → 29.3 GPa | ★ LPSCl E 거의 불변 |
| **4d,f** | LIC FS 모듈러스 맵 (pristine/가압) | ★ 41.1 → 19.8 GPa | ★★ **LIC E 반토막(균열)** |
| **5a** | FEM σ_Mises + 균열 (NCM-LPSCl, full lith.) | <0.2 GPa, 균열 적음 | ★ 소성 재분포→균열↓ |
| **5b** | FEM σ_Mises + 균열 (NCM-LIC) | >0.5 GPa 계면집중, 균열 많음 | ★ 탄성 집중→균열↑ |
| **5c** | 열화 기전 모식 (interphase vs 균열) | — | ★ 두 열화의 공간 그림 |

### 6.2 SI Figures / Tables
| 항목 | 내용 | 우리가 참고할 점 |
|---|---|---|
| **S1** | SSRM 실험 셋업 모식 (ρ_e = 4·r·R_e, +2.5 V) | SSRM 정량식 |
| **S2** | FEM 기하 (Voronoi SE + NCM + virtual crack path) | ★ cohesive-zone 위치(2차 Voronoi edge) |
| **S3** | LPSCl·LIC 입자 SEM | ~5 µm |
| **S4** | 두 SE Nyquist (σ 측정) | σ_ion 1.2/1.6 |
| **S5** | XRD (LPSCl cubic / LIC monoclinic) | 상순도 |
| **S6** | 단결정 NCM SEM/EDS | ~1–5 µm smooth |
| **S7** | 초기 충방전(0.05C) + cycling 프로파일 | LPSCl sagging(계면부반응) |
| **S8** | LIC XRD (240 h 가압 후) | ★ *불변* → 상전이 배제 |
| **S9** | LIC Nyquist (무가압 aging) | ★ 손실 *없음* → 압력이 원인 |
| **S10** | 가압(433 MPa) LIC SEM | ★ **microscale crack 직접 관찰** |
| **S11** | 균열 evolution vs 리튬화도 (elastic-only 둘 다) | ★ 통제: 둘 다 탄성 → 비슷(차이=소성유무) |
| **S12** | 균열 evolution (LPSCl 소성 vs LIC 탄성) | ★ LPSCl 균열 ≪ LIC |
| **Table S1** | TML fitted (R1/R2/CPE + R_ion/R_int/CPE_int/Zw) | ★★ **핵심 정량 앵커** (§3.1) |

### 6.3 ★ Table S1 (fitted 임피던스 verbatim — 우리 정량 앵커)
**상단(unit-cell TML, R1/R2/CPE2):**
| | R1(Ω·cm²) | R2(Ω·cm²) | CPE2 C(µF·sᵑ⁻¹·cm⁻²) | η |
|---|---|---|---|---|
| NCM-LPSCl | 21.7 | 2.6 | 189.6 | 0.5 |
| NCM-LIC | 17.8 | 0.007 | 24.2 | 0.9 |
| NCM-LPSCl (after) | 19.7 | 0.5 | 0.07 | 0.5 |
| NCM-LIC (after) | 19.0 | 24.9 | 16.5 | 0.8 |

**하단(분해 — R_ion/R_int/CPE_int/Warburg):** ★ 이 표가 thesis 의 결정체
| | **R_ion** | **R_int** | CPE_int C(µF·sᵑ⁻¹·cm⁻²) | η | **R_w** | T(s) | f |
|---|---|---|---|---|---|---|---|
| NCM-LPSCl | 126.1 | **341.7** | 96.8 | 0.8 | 14.7 | 5.1 | 0.2 |
| NCM-LIC | **302.5** | 65.2 | 257.6 | 0.9 | 30.7 | 22.5 | 0.4 |
| NCM-LPSCl (after) | 155.6 | **982.3** | 98.6 | 0.8 | 11.8 | 3002.6 | 0.2 |
| NCM-LIC (after) | **595.6** | 113.8 | 368.9 | 0.7 | 1017.9 | 0.5 | 0.6 |
> ★ **읽는 법:** LPSCl 행 = R_int(굵게) 가 사이클로 341.7→982.3 폭증(R_ion 은 126→156 만) = *계면*; LIC 행 = R_ion(굵게)
> 302.5→595.6 폭증(R_int 은 65→114 만) = *이온수송*.  → **한 표에서 두 열화가 *반대 칸*에 나타남**.

---

## 7. Post-processing ★
- **무엇:**
  - **modified TLM 등가회로 피팅**(2 BC: 이온차단 대칭셀 + 풀셀) → **R_ion / R_int(=R_ct) / CPE_int(=C_dl) / Warburg(R_w,T,f)**
    분해 (Table S1).  = Kim 2025·Cho 2024 와 같은 분해법(같은 랩).
  - **SSRM 3D 저항-topology 맵핑** → ρ_e = 4·r·R_e (r=probe radius) 픽셀별 → **interface line scan** 으로 interphase 유무 판정
    (연속변화=interphase / 불연속=없음).
  - **FS(force spectroscopy) 모듈러스 맵핑** → **DMT(Derjaguin-Muller-Toporov) 모델**로 retraction curve 피팅:
    `F − F_adh = (4/3)·E*·√R·(d−d₀)^(3/2)`, `1/E* = (1−ν²)/E + (1−ν_tip²)/E_tip` → **국소 E 맵** (pristine vs 가압).
  - **FEM cohesive-zone 균열전파** → bilinear traction-separation + quadratic 개시 + B-K 파괴 → **균열경로·총 균열길이 vs 리튬화도**.
  - **XRD/XPS** → 상순도·산화분해 화학종(P₂Sₓ/Li₂S vs In/Cl 불변).
  - **GITT / rate** → 분극·확산.
- **도구:** Biologic SP-300(EIS, 7 MHz–1 mHz, 5 mV); AFM Park NX-10(SSRM, log amp, CONTSCPt) + PPP-NCHR(FS); FEM(상용 솔버,
  COMSOL/Abaqus류 — 명시 안 함, cohesive-zone CZM); XPS ESCALAB 250Xi; SEM Hitachi S-4800 + ArBlade5000(cross-section).
- **수치화·기록:** 두 SE(LPSCl/LIC) × 상태(before/after) 별 R_ion/R_int/CPE/R_w (Table S1); FS E (pristine/가압); FEM σ_Mises·균열.

---

## 8. ★ 두 열화 기전의 *물리적 사슬* (논문의 논증 흐름 한 눈에)

```
[NCM-LPSCl = 계면반응 축]
 황화물 LPSCl 산화분해(고전압) ──> NCM/LPSCl 계면에 저항성 interphase(P2Sx, Li2S)
   └ 증거: XPS P2Sx/Li2S 새 peak(Fig3c) + SSRM ~50nm 연속 저항변화(Fig3a) + 첫충전 sagging(S7)
                                   │
                                   ▼
         계면 전하전달 임피던스 R_int 급증 (341.7 ──> 982.3, +187%)
                                   │
                                   ▼
              용량감쇠(유지율 84.7%) — 단, 고율선 계면 driving force 로 극복(2C 우세)

[NCM-LIC = 이온수송 축]
 NCM 반복 부피변화(5.9%) + 지속 가압(250 MPa) ──> elastic-only LIC 계면 *응력 집중*(>0.5 GPa)
   └ FEM(Fig5b): 탄성 LIC 는 응력 재분포 불가 ──> NCM/LIC 계면 cohesive 균열
                                   │
                                   ▼
         LIC SE *균열/역학변형* (FS E 41.1 ──> 19.8 GPa; SEM crack S10; XRD 불변 S8)
   └ 증거: 가압 σ 1.2 ──> 0.6 (Fig4b); 무가압은 손실 없음(S9) ──> 원인=*역학*
                                   │
                                   ▼
         solid-solid contact 악화 ──> 이온경로 단절 ──> R_ion 급증 (302.5 ──> 595.6, ~2배)
                                   │
                                   ▼
              용량감쇠(유지율 75.7%, 더 빠름) — 고율선 이온수송 병목(2C 열위)

[대조의 핵심]  LPSCl: R_int↑·R_ion 안정 (계면) │ LIC: R_ion↑·R_int 안정 (이온수송)
              = 정확히 *반대* 시그니처 ──> "열화 임계인자는 *소재 의존*" (논문 thesis)
```

---

## 9. 미니 용어집 (technique glossary)
- **SSRM (Scanning Spreading Resistance Microscopy)** — AFM 기반 *국소 spreading resistance* 3D 맵.  Pt-코팅 tip 에 DC bias(+2.5 V)
  → 시료 통과 전류 → 픽셀별 저항 → ρ_e = 4·r·R_e.  ★ *어디서* 저항이 국소화하는지(interphase 층)를 *공간적*으로 본다.
- **FS (Force Spectroscopy)** — tapping-mode AFM 의 force-distance curve 로 *국소 영률 E*·접착력·소성변형 에너지 맵.
  **DMT 모델**(접착 고려)로 retraction 피팅 → E.  국소 nanoindentation → intrinsic(작은 면적) 모듈러스 → macro 보다 큰 값.
- **modified TLM (Transmission Line Model)** — 복합 양극의 *분포* 임피던스를 이온/전자 두 레일 + 계면 crossrail 사다리로 모델.
  "modified" = GB·Warburg·charge-transfer 요소 추가.  R_ion(이온수송) / R_int(전하전달) / CPE_int(이중층) / Warburg(고상확산) 분해.
- **R_ion (Li⁺-transport impedance)** — SE 상의 이온수송 저항.  ★ **NCM-LIC 열화의 지배 인자**(가압 균열로 급증).
- **R_int (interfacial / charge-transfer impedance)** — NCM/SE 계면 전하전달 저항.  ★ **NCM-LPSCl 열화의 지배 인자**(interphase).
- **cohesive-zone model (CZM)** — 균열을 *traction-separation* 법칙(두께 0 cohesive 요소)으로 모델.  **bilinear** = 선형 상승→damage
  하강; **quadratic** 개시 + **B-K(Benzeggagh-Kenane)** 혼합모드 파괴.  ★ 균열 *경로*를 결정론적으로 추적(우리 Auerbach 통계와 다름).
- **resistive interphase (P₂Sₓ / Li₂S)** — 황화물 SE 의 *산화분해* 산물층.  계면에 형성돼 R_int↑.  XPS(화학)+SSRM(저항)으로 확인.
- **elastic-plastic vs elastic-only** — LPSCl=*소성 가능*(응력 재분포→균열↓), LIC=*탄성만*(응력 집중→균열↑).  ★ 이 *변형모드 차이*가
  두 SE 의 균열 거동을 가르는 FEM 의 핵심.
- **Warburg (generalized FLW) z_w** — NCM *고상 Li 확산* 임피던스.  T = 확산 시상수, f = frequency-dispersion.
- **halide (LIC = Li₃InCl₆)** — 할라이드 SE.  높은 산화안정성(>4 V, 계면 안정) BUT 낮은 σ_ion(1.2) + **가압 *취약*(균열)**.
- **단결정(single-particle) NCM** — 1차입자 단결정 NCM(다결정 2차입자 아님).  기계적 robust → 사이클 균열 배제 → *SE 열화만* 관찰.

---

## 10. ★ 우리 DEM+MPM 대비 — 캡스톤 통합 + transfer/non-transfer + action items

> ★ 이 절이 capstone digest 의 핵심.  (A) 6편 랩 통합 재진술, (B) 무엇이 우리 모델로 *transfer* 되고 무엇이 *안* 되는지,
> (C) 신규 action item(SE 균열 / E_LPSCl 불일치 / SSRM-FS 카운터파트).  frame[4](교차검증 ≠ cross-fit)·frame[5](분업) 준수.

### 10.1 대비 표
| 항목 | 이 논문 (Yun 2023) | 우리 (DEM+MPM) | 차이 / 이유 (frame) |
|---|---|---|---|
| **방법** | 실험(EIS-TLM 분해 + SSRM/FS) + **FEM**(부피변화 응력 + SE cohesive 균열) | **DEM** Kirchhoff/Holm σ-솔버 + Stage-E + **MPM** J2 소성 형상 | ★ frame[5] 분업: 우리=*제조-순간 구조→수송*; 그들=*사이클 열화 기전*(균열+측정분해) |
| **이온수송 R_ion** | **측정·분해** (LPSCl 126→156; LIC 302→596 Ω·cm²) | σ_ionic *계산* (LOOCV 0.975; bulk σ_grain 3.0×Cronau) | ★ **같은 LPSCl** → 그들 R_ion 이 우리 σ_ionic 의 실험 카운터파트(LPSCl); **LIC 는 우리 미모델** |
| **계면반응 R_int(R_ct)** | ★ **측정·분해** (LPSCl 342→982 Ω·cm²) | ★ **우리 미보유**(constriction-only) | ★ frame[5] 빈 칸 — Kim 2025 와 동일(계면 전하전달은 우리 솔버 밖) |
| **고상확산 Warburg** | ★ R_w/T/f 분해 | ★ **우리 미보유**(D_Li 모델 없음) | 활물질 내 Li 확산 = 우리 transport 밖 |
| **SE 균열** | ★ **할라이드 LIC 가 가압으로 *균열*** (FEM cohesive + FS E 반감 + SEM) | ★ **우리 Auerbach = *AM* 균열만**; MPM SE = *연성 소성*(취성 아님) | ★★ **SE *취성 균열* = 우리 모델에 *없는* 새 메커니즘**(§10.3 action) |
| **CAM 균열** | *배제*(일부러 단결정 NCM 채택) | Auerbach(AM 균열, fracture-aware Holm f_intact) | ★ 우리 AM-균열은 Kang 2025(다결정 입자균열)와 짝; 본 논문은 *SE* 균열 |
| **소성 vs 취성** | LPSCl=*elastic-plastic*(재분포→균열↓), LIC=*elastic-only*(집중→균열↑) | MPM=J2 *연성 소성* 형상흐름(void-fill) | ★ **LPSCl elastic-plastic = 우리 MPM 소성과 *개념적으로 가장 가까운* 랩 모델**; LIC 탄성-취성은 우리에 없음 |
| **모듈러스 E_LPSCl** | ★ **32.8 GPa**(FEM+FS) | real ~24 / E_eff 1.35(연화) / MPM 1.53 | ★ **within-corpus 불일치**: 32.8 *vs* 22.1(Bazzoun/Kang2025/Kim2025) *vs* 24 (§10.4) |
| **E_NCM** | **175 GPa** | NMC811 140 (우리 가정) | = Kang 2025 E_NCA 175; CAM E 재고(A1) |
| **E_LIC(할라이드)** | **41.1 GPa** | (할라이드 미모델; Varkey E 10.58) | ⚠ 본 논문 E_LIC 41.1 ≫ Varkey 할라이드 10.58 — *다른 할라이드*(Li₃InCl₆ vs Li₃YBrCl₆) → 직접대조 금지 |
| **소재** | **SC-NCM811 + LPSCl** (= 우리 production) + **할라이드 LIC** | NMC811 + LPSCl | ★ **황화물 측은 우리와 동일**; 할라이드는 우리 밖(Varkey cross-ref) |
| **국소 저항맵** | ★ **SSRM 측정**(interphase 위치) | σ-솔버가 *구조에서 σ 계산* | ★ frame[4]: 그들=*측정* 국소저항, 우리=*계산* — 카운터파트(§10.5) |
| **국소 모듈러스맵** | ★ **FS 측정**(국소 E 이질성) | Hertz/Tabor coverage = *기계 접촉면적* | ★ 그들 FS=*측정* 국소 E, 우리 coverage=*계산* 접촉 — 다른 양 |
| **압밀 porosity** | **미측정**(펠릿 두께만) | DEM 15.6 % / MPM 16.7 % | ★ **직접 비교 금지** (열화 논문) |
| **transport 채널** | R_ion + R_int + Warburg(계면+확산) | σ_ion + σ_e + σ_thermal(수송 삼중항) | ★ **상보**: 우리=수송 3채널 깊이, 그들=수송+계면+확산 폭 |

### 10.2 ★ 무엇이 *transfer* 되나 (우리 모델/논증에 쓸 수 있는 것)
1. **"계면반응(interfacial reaction)" 개념 + R_int 앵커(LPSCl)** — 황화물 LPSCl 의 *계면 열화*는 우리 production 소재의 실제
   문제.  R_int(342→982)는 *우리 미보유 칸*(frame[5])이지만, **Kim 2025·Cho 2024 와 합쳐 "계면 = 우리 랩 공동 future 축"**.
   우리 σ_ionic 검증 시 R_ion(이온수송 *분리*된 값)만 앵커로 쓸 것(R_int 섞이면 부정확 — Kim 2025 교훈과 동일).
2. **할라이드 vs 황화물 *대조* = Varkey 2026 cross-check 의 *kinetics/열화* 짝** — Varkey=할라이드 *압밀/σ*(E=10.58, floor
   21/37 %); 본 논문=할라이드 *가압 균열 → 이온수송 손실*.  **둘 다 "할라이드 = 안정하나(산화) 취약하다(역학/σ)"** 의
   다른 측면 → 우리가 할라이드로 확장 시 *압밀(Varkey) + 균열(Yun) + 낮은 σ* 셋 다 재보정 필요.
3. **bulk σ_ion(LPSCl) = 1.6 mS/cm** — = Minnmann 1.6 = Kim 2025 1.6 → 랩 자체 *세 번째* 1.6 측정 → 우리 bulk σ 스프레드
   {Cronau 3.0, Lee 2.19, **1.6(Minnmann=Kim2025=본 논문)**, Bazzoun 1.02} 신뢰 보강.
4. **단결정 NCM 채택 논리** — "기계적 robust 단결정 → CAM 균열 배제 → *SE/계면* 열화만 깨끗이 관찰" = Jung 2023 SC 논리 →
   우리 AM_S(단결정)/AM_P(다결정) 구분의 *왜 단결정이 깨끗한가*의 실험 근거.
5. **FEM "소성이 균열을 줄인다"(재분포)** — LPSCl elastic-plastic 이 응력을 흩뿌려 균열↓ = **우리 MPM 소성 void-fill 의
   *균열관점* 버전**(우리 MPM 은 소성이 *void 를 채운다*; 그들 FEM 은 소성이 *균열 driving force 를 낮춘다*) → 같은 "소성=
   완충" 물리.

### 10.3 ★★ 무엇이 *transfer 안* 되나 (frame[5] 빈 칸 — 정직 목록)
1. **SE *취성 균열*(할라이드 LIC)** — ★ **우리 모델에 *없는* 메커니즘**.  우리 Auerbach 균열은 *AM 입자*만; SE 는 우리 DEM 에서
   *영원한 강체구*, 우리 MPM 에서 *연성 J2 소성*(취성 균열 아님).  LIC 가 가압으로 *깨지는*(cohesive crack) 건 우리 두 모델
   *모두* 못 한다.  → `our_dem_baseline.md`·`comparison_vs_ours.md F` 에 "**SE 취성-균열(특히 할라이드) = 우리 transport
   모델 밖, FEM cohesive-zone(Yun 2023) 영역**" 명시.  ⚠ *황화물 LPSCl 은 소성*이라 우리 MPM 연성과 그나마 맞지만, *할라이드는
   취성* → 우리 MPM 으로도 표현 불가.
2. **계면 전하전달 R_int·이중층·고상확산 Warburg** — Kim 2025 와 동일하게 우리 *미보유*(constriction-only σ-솔버).
3. **사이클(cycling) 열화 자체** — 우리 DEM+MPM 은 *제조-순간*(t=0) 구조/수송; *100 사이클 후* interphase 성장·균열 진행은
   우리 모델의 *시간축 밖*.  본 논문 before/after 의 *after* 는 우리가 못 만든다.
4. **할라이드 SE 일반** — 압밀(Varkey)·균열(Yun)·낮은 σ 모두 우리 production(LPSCl 황화물) 밖.

### 10.4 ★ E_LPSCl within-corpus 불일치 (신규 action — 우리 SE-모듈러스 앵커)
| 출처 | E_LPSCl | 맥락 |
|---|---|---|
| **본 논문 (Yun 2023)** | **32.8 GPa** | FEM 입력 + FS 국소 측정(둘 다 32.8) |
| Bazzoun 2026 | 22.1 GPa | DEM 입력 |
| Kang 2025 (랩) | 22.1 GPa | FEM 입력 |
| Kim 2025 (랩) | (22.1 계열) | (자매 언급) |
| 우리 real bulk | ~24 GPa | 단결정/벌크 lit |
| 우리 E_eff(DEM) / MPM | 1.35 / 1.53 GPa | *연화 프록시*(압밀-rearrangement 럼핑) |
> ★ **불일치 정리:** LPSCl E 문헌 스프레드가 **22.1 ↔ 24 ↔ 32.8 GPa** 로 *1.5배* 벌어짐.  본 논문 32.8 은 **FS *국소
> nanoindentation* 값**(intrinsic, 작은 면적 → macro·DEM-input 보다 *크게* 나옴 — §3.3 의 "FS > macro" 논리와 일관) →
> 32.8 이 *틀린 게 아니라* **측정 스케일이 다른 값**(국소 intrinsic vs bulk).  ⇒ **우리 SE-modulus 앵커 노트에 "real E_SE
> 스프레드 = 22.1(DEM/FEM-input)–24(bulk lit)–32.8(FS 국소)" 로 *범위* 기록**; 우리 E_eff 1.35–1.53 은 이 *어느 값도* 아닌
> *압밀-프록시*(연화)임을 재확인.  ⚠ **절대 직접대조 금지** — 32.8(국소) ≠ 22.1(bulk-input) 은 *방법 차이*, 모순 아님.
> ★ **E_LIC 주의:** 본 논문 E_LIC 41.1 GPa(Li₃InCl₆) ≫ Varkey 할라이드 E 10.58 GPa(Li₃YBrCl₆) — **다른 할라이드**(In vs Y/Br)
> → 두 할라이드 E 직접대조 금지(할라이드도 조성마다 E 다름).

### 10.5 ★ SSRM/FS = 우리 네트워크-σ + 접촉역학의 *실험 카운터파트* (frame[4])
- **SSRM(국소 저항 3D 맵)** = 우리 **네트워크 솔버의 σ-맵**(Kirchhoff Holm constriction)의 *실험* 짝.  그들은 단면에서 *국소
  저항*을 *측정*(interphase 층 ~50 nm 까지 분해), 우리는 구조(접촉망)에서 *국소 전도경로*를 *계산*.  → ★ **frame[4] 외부
  검증**: 우리 σ-맵이 *interphase 같은 국소 고저항*을 (만약 우리가 모델하면) 어디에 두는지 SSRM 이 *실측*으로 비교점 제공.
  단 ⚠ 우리는 *interphase 를 모델 안 함* → SSRM 의 interphase 신호는 우리가 *재현 못 하는* 것(frame[5]).
- **FS(국소 모듈러스 맵)** = 우리 **접촉역학(Hertz/Tabor coverage, Stage-E)** 의 *실험* 짝 — 단 *다른 양*: FS=*국소 E 이질성*
  (intrinsic 모듈러스 맵), 우리 coverage=*기계 접촉면적*(σ-라우팅용).  ★ FS 의 "LIC E 41.1→19.8(가압 균열)" = 우리 모델이
  *못 잡는* SE 역학손상 → 우리 E_SE *단일값* 가정의 한계를 실측으로 보여줌(SE E 가 가압으로 *국소 변함*).

### 10.6 ★ Action items (우리 모델·문서에 반영)
- **A. SE 취성-균열 = frame[5] 새 빈 칸 명문화** → `our_dem_baseline.md` LIMITS + `comparison_vs_ours.md F`(못 하는 것)에
  "**SE 취성균열(할라이드 LIC 가압 균열, Yun 2023 FEM cohesive-zone) = 우리 AM-only Auerbach 밖; MPM SE 는 연성소성 →
  취성균열 미표현**" 추가.  (메인 세션이 INDEX/comparison 편집 — 이 digest 가 그 내용을 *제안*만.)
- **B. E_LPSCl 스프레드 노트** → SE-modulus 앵커에 "22.1(DEM/FEM-input)–24(bulk)–**32.8(FS 국소, Yun 2023)**" 범위 기록;
  E_LIC 41.1(Li₃InCl₆) ≠ Varkey 10.58(Li₃YBrCl₆) 별개.
- **C. 할라이드 통합 노트(Varkey ↔ Yun)** → "할라이드 = 압밀(Varkey E10.58→floor 21/37 %) + 가압균열(Yun, σ 1.2→0.6) +
  낮은 σ(1.2) — 우리가 할라이드 확장 시 E·σ·균열·압밀 *전부* 재보정" 한 줄.
- **D. 계면축 랩-통합(이미 Kim2025 digest 에 있음, 본 논문이 *원조*)** → "계면반응 R_int↑ = LPSCl 황화물 열화(Yun 2023 원조,
  Kim 2025 정밀화, Cho 2024 CA축) = 우리 미보유 → 랩 공동 future 축(mechanics=Kang/Kim2023, kinetics=Kim2025/Cho, 소재지도=
  Yun2023, structure-σ=우리)".
- **E. SSRM/FS 카운터파트** → "SSRM(국소 저항)=우리 σ-맵 실험짝; FS(국소 E)=우리 coverage 와 *다른* 양(국소 모듈러스)" 노트.

---

## 11. 인용 가능 문장 (deck/paper용)
- "Our group's capstone study (Yun, Shin, … Moon, Lee, Energy Storage Mater. 2023) **deciphers that the critical
  degradation factor is material-dependent**: by impedance decoupling (modified TLM, the same method as our Kim 2025 /
  Cho 2024 papers) it shows that an **NCM811/Li₆PS₅Cl (sulfide) composite degrades by *interfacial reaction*** (charge-
  transfer resistance R_int 342 → 982 Ω·cm² from a resistive P₂Sₓ/Li₂S interphase) whereas an **NCM811/Li₃InCl₆ (halide)
  composite degrades by *ionic transport*** (Li⁺-transport resistance R_ion 303 → 596 Ω·cm² from cracking-induced
  mechanical deformation of the halide SE under pressure)."
- "This single paper **unifies our six-paper lab series into a two-axis degradation map** (interfacial-reaction ×
  ionic-transport): it joins the *interfacial-reaction* axis (Kim 2025 R_ct, Cho 2024 conductive-additive side
  reactions) with the *mechanical-cracking* axis (Kang 2025 particle cracking, Kim 2023 anode-strain), on the
  single-crystal NCM foundation of Jung 2023."
- "The halide Li₃InCl₆ fails by **mechanical cracking of the SE itself under sustained pressure** — its local modulus
  drops from 41.1 to 19.8 GPa and its ionic conductivity halves (1.2 → 0.6 mS cm⁻¹ over 240 h at 250 MPa) — a failure
  mode **absent from our models**: our Auerbach fracture is cathode-particle-only and our MPM treats the SE as a
  *ductile* J2 plastic, not a *brittle*-cracking phase (frame[5] gap)."
- "FEM (cohesive-zone crack propagation in a Voronoi SE) shows that the **plasticity of LPSCl redistributes the
  volume-change stress over a large region (<0.2 GPa) and thereby suppresses cracking**, whereas the **elastic-only
  LIC concentrates stress at the NCM interface (>0.5 GPa) and cracks** — the crack-mechanics counterpart of the
  stress-buffering plastic void-fill our MPM captures on the densification side."
- "The bulk ionic conductivity of LPSCl measured here (1.6 mS cm⁻¹) coincides with Minnmann 2021 and our Kim 2025
  value, a third lab-internal confirmation of the σ_grain anchor; the FEM/FS LPSCl modulus (32.8 GPa) sits above the
  22.1 GPa DEM/FEM-input value, reflecting the higher *local* modulus that AFM nanoindentation reports versus bulk —
  widening our SE-modulus spread to 22.1–24–32.8 GPa (all real; our 1.35–1.53 GPa is a softened compaction proxy)."

---

## 12. 주의/한계 (over-claim 방지)
- **열화-메커니즘 논문 = 구조/압밀/역학(압밀) *미산출*.**  porosity·상대밀도·coordination·coverage·Heckel·PSD·정량 σ_y 를
  *측정하지 않는다*(펠릿 두께·국소 E·R 만).  우리 압밀 앵커(Minnmann 14 %·Doux 18 %·우리 15.6 %)·Heckel 과 **직접 비교 금지** —
  이 논문 정량 앵커 = *R_ion/R_int/Warburg(Table S1) / FS 국소 E / FEM σ_Mises·균열 / rate·cycling 용량 / bulk σ* 다.
- **"시뮬레이션"은 FEM(균열) + TLM(회로) — DEM/MPM 아님.**  FEM = Voronoi *연속체* + cohesive-zone(우리 입자 DEM 아님);
  TLM = lumped 회로(미세구조 미생성).  → frame[4] *외부 검증/보완*이지 *경쟁 DEM 솔버* 아님.
- **R_ion/R_int 은 *측정+TLM 피팅* 값** → *예측 솔버* 산출 아님.  우리 σ_ionic(계산)과 비교 시 "그들=실험 진실, 우리=구조
  예측"(frame[4]).  ⚠ **조성 매핑**: 본 논문은 *단일 조성*(72:27:1)만 → 우리 φ_SE-스윕과 *단일점* 매칭만 가능.
- **할라이드(LIC) = 우리 production(LPSCl) 밖** → LIC 의 R_ion/E/균열/σ 는 우리 모델로 *재현 안 됨*.  "우리가 LIC 를 검증"이
  아니라 "**우리가 *안 갖는* 할라이드 균열을 실험이 보여줌**"(Varkey cross-ref 와 같은 정직 프레임).
- **SE 취성균열 = 우리 모델 밖** → "우리 MPM 이 SE 균열을 재현/검증"이라 말하면 *틀림*.  우리 MPM SE=연성소성(취성 아님);
  우리 DEM SE=강체구(안 깨짐).  LIC cohesive 균열은 *둘 다* 못 함.  단 *황화물 LPSCl 소성*은 우리 MPM 연성과 개념 일치.
- **E_LPSCl 32.8 vs 22.1 = *방법 차이*(FS 국소 vs bulk-input), 모순 아님** → 직접대조 금지, *범위*(22.1–24–32.8)로만.
  E_LIC 41.1(Li₃InCl₆) ≠ Varkey 10.58(Li₃YBrCl₆) — *다른 할라이드*.
- **"LPSCl 항복강도 200 GPa"(본문) = 물리적 오타로 강하게 의심 → 200 MPa** → 항복강도(200 GPa)가 모듈러스(32.8 GPa)보다
  *클* 수 없음(불가능); 항복강도는 통상 MPa.  Kang 2025 의 cohesive 입력(GB strength 100 MPa)과도 자릿수 일관(MPa).
  ★ **우리 σ_y 앵커(0.05–0.30 GPa)에 이 "200 GPa" 를 절대 넣지 말 것** — 오타 의심값(200 MPa 라면 우리 범위보다 높은 상한).
- **사이클 열화 = 우리 시간축 밖** → before/after 의 *after* 는 우리 t=0 모델이 못 만듦.  "interphase 성장·균열 진행"은 우리 영역 아님.
- **bulk σ 1.6 vs 우리 Cronau 3.0** → 측정/입자/GB 차 → 범위로만(단 Minnmann=Kim2025=1.6 일치 = 신뢰 보강).
- **SSRM/FS = *측정* 국소값** → 우리 *계산* σ-맵/coverage 와 "종류는 같고(국소 저항/모듈러스) 출처가 다름(측정 vs 계산)".
  특히 FS E ≠ 우리 coverage(접촉면적) — *다른 물리량*(국소 모듈러스 vs 접촉면적).

---

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
