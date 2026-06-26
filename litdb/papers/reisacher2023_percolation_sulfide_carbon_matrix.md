# ⭐ #27 (★ 우리 EXACT SE) — Percolation Behavior of a Sulfide Electrolyte–Carbon Additive Matrix for Composite Cathodes in All-Solid-State Batteries — Reisacher, Kaya, Knoblauch (Batteries 2023)

> slug `reisacher2023_percolation_sulfide_carbon_matrix` · DOI `10.3390/batteries9120595` · type `exp` (실험 EIS + DC-polarization, no DEM/MPM) · PDF `Reisacher_2023_Batteries_Percolation_SulfideElectrolyte_CarbonAdditive.pdf` · OPEN ACCESS (CC BY 4.0) · digested `2026-06-26` · status ✅
>
> ## ★★★ 왜 중요한가 (3줄) ★★★
> (1) **우리 EXACT SE(Li₆PS₅Cl = LPSCl) + C65 카본**의 **전자 percolation 임계 p_c ≈ 4 wt% C65 를 *실험으로 직접 측정*** — 우리 σ_e
> 도전제 percolation(backlog **A4** se_coating/carbon)의 **literature-grounded 절대 앵커**(할라이드 논문과 달리 **소재 전이 보정 불필요**, 직접 매핑).
> (2) **p_c 아래 = 이온 지배(σ_eff ≈ pure-SE, 온도의존·저주파 blocked) / p_c 위 = 전자 ohmic(주파수 무관)** = 우리 삼중항이 잡아야 할 **σ_ionic ↔ σ_e 크로스오버**를
> *carbon wt% 축*에서 정량한 σ_eff(C65) 곡선(0→100 wt%, 7점, **4 orders of magnitude step**).
> (3) **자매 carbon 논문 3종**과 짝: **Reisacher(이 논문) = carbon 전자망의 *percolation 임계 위치*(언제 켜지나)** ↔ **Kim 2024(AcceleDomain) = carbon의 *부피 점유*(SE를 밀어냄)** ↔
> **Cho 2024(Hanyang Lee group) = carbon의 *양면성*(σ_e↑ vs σ_ion↓·분해 가속)**.  → 셋 합치면 "도전제 = 양날의 검 + *최소량으로 percolate* 시켜야"라는 우리 CBD/Stage-2 테제의 *완전한 실험 골격*.

---

## §0. ★ 이 논문의 위치 — "최소 carbon 으로 전자 percolate" + 자매 carbon 논문 지도 (이 절이 digest 의 framing)

### 0.1 한 줄 테제
**"황화물 ASSB 복합 양극의 *도전 매트릭스*(LPSCl + C65)는 *전자 percolation 임계* p_c ≈ 4 wt% C65 를 가지며 — 그 아래는 이온전도 지배, 그 위는 전자 ohmic
지배 — 따라서 분해/부반응을 줄이려면 *최소 C65* 로 전자망을 percolate 시켜야 한다."**
- **p < p_c (< 4 wt% C65):** C65 가 **고립 섬(isolated islands)** → 전자망 미형성 → σ_eff ≈ pure-SE(이온전도), **온도의존**(Arrhenius, ↑T → σ↑)·**저주파 blocked
  charge transport**(In 블로킹 전극에서 허수부 폭증) = **이온전도체 거동**.
- **p ≈ p_c (≈ 4 wt%):** σ_eff 가 **step-like 급상승**(3 wt% 1.66×10⁻⁴ → 4 wt% 1.36×10⁻³ → 5 wt% 1.02×10⁻¹ S/cm, **~3 orders**) → C65 가 **연결 cluster** 형성.
- **p > p_c (≥ 4–5 wt%):** 임피던스 **주파수 무관 + 용량(capacitance) 없음 = pure ohmic resistor** → C65 percolating network 가 σ_eff 를 지배(이온전도의 *수백 배*).
- **설계 가이드라인:** 양극 70 wt% AM 기준 → 도전매트릭스의 4 wt% C65 = **양극 전체로는 1.2 wt% C65** 면 전자 percolate → CAM 패시베이션 코팅(전자전도 저하)을 보상하면서 *최소 carbon*.

### 0.2 ★ 우리 모델축과의 1:1 대응 (이 논문이 채우는 칸)
| 이 논문이 보이는 것 | 우리 모델축 | 비고 |
|---|---|---|
| **p_c ≈ 4 wt% C65** (전자 percolation 임계) | ★ **우리 σ_e percolation 게이트 / f_p³ isotropy** (backlog A4) | ★ carbon 전자망이 *언제 켜지나*의 절대 앵커 (LPSCl = 우리 SE → 직접) |
| **σ_eff(C65 wt%) 곡선** (0→100 wt%, step at p_c) | ★ **우리 σ_e vs 도전제 함량** (additives.py SuperP/VGCF) | ★ carbon wt% → σ_e 검증 곡선 |
| **p < p_c 이온 지배 / p > p_c 전자 ohmic** | ★ **우리 σ_ionic ↔ σ_e 크로스오버**(삼중항) | ★ 두 채널의 부호 전환을 *carbon 축*에서 봄 |
| **C65 BET 62 m²/g → 저-함량서 3D 망** | 우리 carbon morphology(분기 fractal aggregate, additives.py `seed_carbon_black`) | ★ 高비표면적 = 저 p_c (입자 형상·표면적이 p_c 낮춤) |
| **smaller AM → earlier p_c** (Bielefeld 인용) | ★ Bielefeld 2019 p_c=7.83·ln(d_AM)+36.67 (우리 litdb) | 우리가 *이미 보유한* peer 식과 직접 연결 |
| **LPSCl σ_ion 0.43 mS/cm @ RT, E_a 0.41 eV** | 우리 LPSCl bulk σ 앵커 스프레드 + Bielefeld E_a 0.41 | ★ **E_a 0.41 eV = Bielefeld 2019 β=0.41 와 무관 우연**(혼동 금지); σ_ion = bulk 앵커 |
| **separator 375 MPa / matrix 2.07 MPa** | 우리 제조압(300) vs 작동압 구분 | ★ separator 압밀압 ≈ Doux 370·Minnmann 380 계열; matrix in-cell 2.07 MPa = 매우 저압(접촉만) |
| 압밀 porosity·Heckel·coordination·coverage | (이 논문 *미보유* — 순수 전달/percolation) | frame[5] 빈 칸 → 우리가 채움 |

### 0.3 자매 carbon 논문 3종 — 도전제(carbon)의 세 렌즈 (우리 CBD/Stage-2 골격)
| | **★ Reisacher 2023 (이 논문)** | **Kim 2024 (AcceleDomain/AFM)** | **Cho 2024 (Hanyang Lee group)** |
|---|---|---|---|
| 그룹 | **Aalen Univ. (IMFAA, 독일)** | **KETI + Hanyang (Sun·Lee·Cho)** | **Hanyang (Jong-Won Lee group)** |
| 소재 | **LPSCl + C65** (도전매트릭스, *AM 없음*) | NCM811 + LPSCl(+Br) + SC/CF carbon | NCM811 + LPSCl + **VGCF**(+할라이드 LZC) |
| 본다 | ★ **carbon 전자망의 *percolation 임계*(p_c≈4 wt%)** | carbon 의 **부피 점유**(SE 도메인 빼앗음, ρ 0.67≪1.86) | carbon 의 **양면성**(σ_e↑ vs σ_ion↓·삼상계면 분해) |
| 방법 | **EIS(7 MHz–1 Hz, T-sweep) + DC-polarization + σ_eff(C65)** | DC-polarization σ + CC-pulse + XPS/HR-TEM | modified-TLM(R_ion/R_int 분해) + DC + XPS/CV |
| 핵심 수치 | **p_c≈4 wt%; σ_eff 6.6e-5→0.2 S/cm; LPSCl σ 0.43 mS/cm** | σ_ion AM 80/85/90 = 0.125/0.046/0.014; SC vs CF +22% | r_ele 245→102; R_ion high-f_AM 318→402(→cycled 781) |
| 처방 | ★ **최소 C65(4 wt% matrix = 1.2 wt% cathode)로 percolate** | 구형 SC → 1D 섬유 CF (SE 도메인 덜 점유) | 산화안정 할라이드 LZC(분해 억제) |
| 우리 매핑 | ★ **σ_e percolation 게이트/f_p³ 절대 앵커 (A4)** | carbon = SE 점유체 (A4 부피항) | σ_e↔σ_ion trade-off (A3/A4) |
> ★ **세 논문의 통합 결론(우리 CBD/Stage-2 테제):** carbon 은 (i) **p_c≈4 wt% 에서 전자망을 percolate**시키되(Reisacher) (ii) 그 이상 넣으면 **SE 부피를 점유**(Kim 2024)하고
> (iii) **σ_ion 을 떨어뜨리며 황화물 SE 분해를 가속**(Cho 2024)한다 → 따라서 **"p_c 직상(just above)에서 *최소량*"**이 최적.  우리 σ_e percolation 폼은 p_c 를 잡고, σ_ion 폼은
> carbon 부피·blocking 페널티를 잡고, MPM 은 carbon 부피점유 morphology 를 잡아야 — 세 논문이 그 세 조각의 실험 근거.

### 0.4 ★ 이 논문이 인용하는, *우리가 이미 보유한* peer 4종 (frame[4] 그룹-내부 연결)
이 논문은 우리 litdb 의 다음 digest 들을 **직접 인용**한다 → 우리 비교의 *문헌-내부 일관성* 확인:
- **ref [10] Bielefeld 2020** (GeoDict flux-PDE σ_eff + 바인더, `docs/lit_bielefeld2020_effective_ionic_conductivity_binder.md`) — σ-모델링 peer.
- **ref [11] Bielefeld 2022** (J. Electrochem. Soc. 169, 20539 — Li kinetics/morphology/voids) — Bielefeld 시리즈 3편째.
- **ref [37] Minnmann 2021 JES** (NCM622+LPSCl, 우리 porosity/σ_ion/τ 앵커 1차 출처, `docs/lit_minnmann2021_jes_charge_transport_bottlenecks.md`) — "NCM622 σ_e 충분" 논쟁 인용.
- **ref [12] Doux 2020** (LPSCl 압력-역학, `docs/lit_doux2020_stack_pressure_assb.md`) — 황화물 압력민감성 인용.
- **ref [45] Bielefeld 2019** (GeoDict percolation, `docs/lit_bielefeld2019_microstructural_modeling_composite_cathodes.md`) — **"smaller AM → earlier p_c" 직접 인용** (= 우리 보유 p_c=7.83·ln(d_AM)+36.67).
- **ref [46] Guzman 2017** (LiFePO₄+C65 p_c ≈ 7 wt%) — 다른 소재계 p_c 비교점.
> ⇒ 이 논문은 **Bielefeld(percolation/σ-모델링) + Minnmann(σ_e 충분?) + Doux(압력) 라인의 *실험 percolation* 짝**.  우리는 Bielefeld 의 *전자 p_c 식*(이론/모델)을 **이 논문의 *실측 p_c=4 wt%*(LPSCl+C65)** 로 검증할 수 있다.

---

## 1. 한 줄 요약
황화물 ASSB 양극의 **도전 매트릭스 = Li₆PS₅Cl(LPSCl) + C65 카본** 의 **전자 percolation 임계 p_c 를 ≈ 4 wt% C65 로 *실험 측정***(EIS T-sweep + DC-polarization +
σ_eff vs C65 wt%): **p_c 아래는 이온전도 지배**(σ_eff ≈ pure-SE, 온도의존 Arrhenius·In 블로킹 전극서 저주파 blocked charge transport), **p_c 위는 전자 ohmic 지배**(임피던스
주파수 무관·용량 없음·step-like 급상승 3 wt% 1.66×10⁻⁴ → 5 wt% 1.02×10⁻¹ S/cm) → **도전매트릭스는 AM 입자 사이의 *이온·전자 동시전도 상*** 으로 볼 수 있고 → **양극 70 wt% AM
기준 1.2 wt% C65** 면 전자 percolate → "**최소 C65 로 전자전도를 켜는 설계 가이드라인**"(CAM 패시베이션 코팅의 전자전도 저하 보상).

---

## 2. 메타
| 항목 | 값 |
|---|---|
| 저자 | **Elias Reisacher\*, Pinar Kaya, Volker Knoblauch** |
| 소속 | **Materials Research Institute Aalen (IMFAA), Aalen University of Applied Sciences**, Beethovenstraße 1, 73430 Aalen, Germany (corr. elias.reisacher@hs-aalen.de) |
| 저널/년 | **Batteries 2023, 9(12), 595** (MDPI) |
| DOI | **10.3390/batteries9120595** (Received 2023-11-09, revised 2023-12-09, accepted 2023-12-13, published 2023-12-15) |
| 라이선스 | **OPEN ACCESS (CC BY 4.0)** |
| Keywords | all-solid-state batteries · composite cathode · solid electrolyte · sulfides · carbon · additives · **percolation** · ionic conductivity |
| 소재 (SE/CA) | **SE = LPSCl Li₆PS₅Cl** (자체 합성, Li₂S+P₂S₅+LiCl 볼밀 30:1 ratio·100 rpm·1 h → 550 °C 6 h, ramp 1.5 °C/min, 석영관 진공) · **CA = C65** (Super C65, MTI/Imerys, Bironico, Switzerland — 도전성 카본블랙) · **★ AM(활물질) 없음** — *도전 매트릭스만* 연구 |
| 조성 (도전매트릭스) | **Wt-ratio LPSCl:C65 = 100:0 / 99:1 / 97:3 / 96:4 / 95:5 / 90:10 / 0:100** (C65 = **1.00–10.00 wt%** 스윕 + 순수 양 끝) |
| ρ (밀도) | **LPSCl 1.83 g/cm³** · **C65 1.60 g/cm³** (유사 밀도 — p_c 가 낮은 건 밀도 아닌 *비표면적* 탓) |
| C65 비표면적 | **62 m²/g** (高비표면적 → 적은 양으로 3D 망 형성 → 낮은 p_c) |
| σ_ion (LPSCl) | **0.12 mS/cm @ 5 °C · 0.43 mS/cm @ RT · 2.02 mS/cm @ 65 °C** (Fig 2); **E_a(Li⁺) = 0.41 eV** (Arrhenius, Fig 2b) |
| 셀 | (a) **EIS**: 대칭 [In \| 도전매트릭스 \| In] (블로킹 전극, TSC rhd instruments); (b) **DC**: 전자전도 거동 확인용 직류측정 |
| 압력 | **separator(분리막) 100 mg LPSCl → 375 MPa 단축 압밀** ≠ **도전매트릭스 40 mg → 셀 내 163.2 N = 2.07 MPa in-situ 압축** (펠릿이 안 만들어져 *셀 안에서 직접* 압축; 측정 후 caliper 로 ⌀10.12 mm·두께 400 µm 측정) |
| 측정 | EIS: VSP-300 Bio-Logic, **7 MHz–1 Hz**, AC 10 mV, **5–65 °C 10 °C 스텝**(120 min 안정화), Z-View 4.0d 피팅. DC: 거동 확인. XRD: Seifert Sun 3003 Cu-Kα 15–80° 0.026°/min. SEM: Zeiss Sigma 300VP |
| 연구유형 | **실험**(EIS T-sweep σ_eff + DC-polarization + σ_eff vs C65 wt% percolation 곡선 + XRD/SEM 미세구조) — *시뮬레이션 없음* |

---

## 3. 핵심 물성 (수치)

> ⚠ 이 논문은 **percolation 임계 + σ_eff(C65 wt%, T)** 가 목적이다.  ★ **porosity·Heckel·coordination·coverage·E_SE·σ_y·PSD 는 측정 안 함**(전부 n/a — 도전매트릭스 percolation
> 논문).  σ_eff 절대값은 **Fig 5 막대(stated 본문에 4종 명시) + Fig 4 Arrhenius(digitized)**.  도전매트릭스는 **AM 없이 LPSCl+C65 만** → 우리 *복합 양극* φ_SE 케이스와 직접
> 동일시 금지(이건 *SE-카본 2상 매트릭스*); 매핑은 "carbon wt% → 전자 percolation 게이트" 축으로만.

| 물성 | 값 | 조건 | stated/digitized | 비고 |
|---|---|---|---|---|
| **★ p_c (전자 percolation 임계)** | **≈ 4 wt% C65** (범위 **3 < p_c < 5 wt%**) | 도전매트릭스 LPSCl+C65, 25 °C | **stated** (Abstract, Fig 5, Conclusions) | ★★ **우리 σ_e carbon percolation 의 절대 앵커**. vol% 로는 ≈ **4.62 vol% C65** |
| **★ σ_eff @ 25 °C, 0 wt% C65** | **≈ 6.6 × 10⁻⁵ S/cm** | pure SE(셀내 압축), p<p_c | digitized (Fig 5) | = pure-SE 이온전도 수준(셀내 미압밀 → separator 0.43 mS/cm 보다 낮음) |
| **★ σ_eff @ 25 °C, 1 wt% (CM-1)** | **≈ 9.5 × 10⁻⁵ S/cm** | p<p_c | digitized (Fig 5) | C65 고립섬 → 여전히 이온 지배 |
| **★ σ_eff @ 25 °C, 3 wt% (CM-3)** | **1.66 × 10⁻⁴ S/cm** | p≈p_c 직하 | **stated** (본문) | CM-1 대비 +1.20×10⁻⁴ (이온~전자 전이 시작) |
| **★ σ_eff @ 25 °C, 4 wt% (CM-4)** | **1.36 × 10⁻³ S/cm** | p≈p_c | **stated** (본문) | ★ **CM-3 대비 ~1 order ↑** (1.66e-4 → 1.36e-3) = percolation 무릎 |
| **★ σ_eff @ 25 °C, 5 wt% (CM-5)** | **1.02 × 10⁻¹ S/cm** | p>p_c | **stated** (본문) | ★★ **CM-3 대비 ~3 orders ↑** = 전자망 완성 |
| **★ σ_eff @ 25 °C, 10 wt% (CM-10)** | **≈ 1.1 × 10⁻¹ S/cm** | p>p_c | digitized (Fig 5) | CM-5 대비 *미미한* 증가(수확체감 — 망 이미 형성) |
| **★ σ_eff @ 25 °C, 100 wt% (pure C65)** | **≈ 0.2 S/cm** (저항 ≈ 0.25 Ω) | pure C65, p≫p_c | **stated** (본문) | 순수 카본 상한 |
| **★ σ_ion (LPSCl separator)** | **0.12 (5 °C) / 0.43 (RT) / 2.02 (65 °C) mS/cm** | LPSCl, 375 MPa separator | **stated** (Fig 2) | ★ bulk 앵커. RT 0.43 « Cronau 3.0·우리 채택 — *셀 형상·압밀·측정온도* 차 (스프레드로만) |
| **★ E_a (Li⁺ in LPSCl)** | **0.41 eV** | Arrhenius slope (Fig 2b) | **stated** | ★ 문헌 일치(Yu/Zhang). ⚠ **Bielefeld 2019 β=0.41 (percolation 지수)와 *우연 일치*, 물리 무관 — 혼동 금지** |
| **R_total(LPSCl separator)** | 354.40 Ω (25 °C) → 58.79 Ω (65 °C) | separator | stated | T↑ → R↓ |
| **R_total(CM-1, 1 wt%)** | 522 Ω (RT) → 247.67 Ω (65 °C); R_pure SE 102.10 Ω (65 °C) | 도전매트릭스 | stated | CM-1 이 pure SE 보다 high-T 저항 *높음*(섞임) |
| **R_total(CM-3, 3 wt%)** | 302.43 Ω (65 °C) → 288.03 Ω (15 °C) → 272.17 Ω (5 °C) | 도전매트릭스 | stated | ★ **T↓ → R↓** (전자전도 지배 시그니처 — 이온과 *반대*) |
| **R_total(CM-4, 4 wt%)** | 33.50 Ω (25 °C) / 43.89 Ω (65 °C), T-무상관 | 도전매트릭스 | stated | ★ 주파수·온도 무관 = pure ohmic |
| **vol% C65 (조성별)** | 99:1→**1.16** / 97:3→**3.47** / 96:4→**4.62** / 95:5→**5.77** / 90:10→**11.44** vol% | Table 1 | stated | wt%→vol% (ρ 1.83/1.60) |
| **★ 설계 가이드라인** | 70 wt% AM 양극 → 도전매트릭스 4 wt% C65 = **양극 전체 1.2 wt% C65** | Conclusions | stated | ★ 최소 carbon percolate 처방 |
| **다른 소재계 p_c (비교)** | LiFePO₄+C65 ≈ **7 wt%** (Guzman, ref [46]) | 비교 | stated(인용) | 황화물 p_c(4) < LFP(7) |
| porosity / 상대밀도 | **n/a** (미측정) | — | — | percolation 논문 |
| E_SE / σ_y / ν | **n/a** (역학 미모델) | — | — | (E_LPSCl = 자매 22.1 GPa) |
| coverage / coordination Z / Heckel | **n/a** | — | — | — |
| PSD (D10/D50/D90) | **n/a** (SE 입경 "submicrometer, agglomerate >10 µm" 정성만, Fig 1b) | — | — | C65 nano(primaries), 수치 미보고 |

> ★ **bulk σ_ion(LPSCl) = 0.43 mS/cm @ RT** — 우리 LPSCl bulk 스프레드 {Cronau 단결정 3.0, Lee pristine 2.19, Doux pellet 2–2.5, Kim2025/Minnmann **1.6**, Bazzoun pellet 1.02,
> **이 논문 0.43**} 의 *하단*.  ⚠ **이 0.43 은 셀-내 직접압축이 아니라 separator(375 MPa)** 값이고 측정 RT·셀 형상 차 → **절대 직접대조 절대 금지, *범위/추세*로만**.  황화물 LPSCl bulk σ 는
> 측정 셀·압력·로트·온도·GB 포함 여부에 따라 0.43↔3.0 의 ~7× 스프레드 → *절대값 신뢰 말 것*, 우리 σ_grain prefactor 는 Cronau 3.0(단결정-라벨) 유지.

---

## 4. 시뮬레이션 방법 ★ — *없음* (순수 실험 + 등가회로 *피팅*)

> ★ 이 논문에는 **DEM / MPM / FEM / 입자 시뮬레이션이 없다.**  "모델"은 (i) **percolation *이론*** (Newman-Ziff Monte-Carlo·연속체 percolation 인용, ref [34–36]) 을
> *해석 프레임*으로 쓰고, (ii) **EIS Nyquist 를 등가회로로 피팅**(Z-View)하여 R 을 추출, (iii) **σ_eff = (d/A)·R⁻¹** (Eq 1) 로 환산하는 것뿐.  입자 시뮬레이션·접촉망·구조생성 *없음*.

### 4.1 percolation 이론 프레임 (해석만, 시뮬 아님)
- **percolation theory**(ref [34] Newman-Ziff Monte-Carlo, [35] 연속체 spherocylinder percolation, [36] McLachlan 복합저항)을 *해석 틀*로 인용:
  C65 입자가 randomly distributed → 임계 함량서 cluster 가 *유한 공간 전체를 가로질러 연결* = percolating.
- ★ **단 percolation 을 *시뮬레이션하지 않음*** — p_c 를 *실험 σ_eff(C65) step* 으로 측정.  Bielefeld 2019(ref [45], 우리 보유)의 "smaller AM → earlier p_c (高표면적)"를 *인용*하여
  C65 의 高비표면적(62 m²/g)이 *낮은 p_c(4 wt%)* 를 설명.

### 4.2 EIS 등가회로 피팅 (Z-View) — 우리 Kirchhoff/Holm 솔버의 *실험 카운터파트*
- **RT 이상 (p<p_c·이온전도):** 블로킹 전극 tail 의 **linear intercept** 로 R 추출.
- **RT 미만·1 wt%:** **R₀ 직렬 + (R₁ ∥ CPE) + 추가 CPE** 피팅(separator 의 evolved semicircle).
- **3 wt%:** **R + 2 Randles circuit** 직렬.
- **★ 4 wt% 이상 (p≥p_c·percolation 도달):** **단일 저항 R** 만으로 피팅(주파수 무관·용량 없음 = pure ohmic) → percolation 의 *임피던스 시그니처*.
- σ_eff = (d/A)·R⁻¹ (Eq 1), d=두께(~400 µm), A=면적(⌀10.12 mm).  **DC-polarization 으로 전자전도 거동 교차확인**(Fig S3/S4).

### 4.3 입자 처리 ★ — *없음* (실험)
- ★ **입자 형상·PSD·rigid/plastic 개념이 없다.**  미세구조를 *명시적으로 생성하지 않고* 도전매트릭스를 **σ_eff + R(T) + percolation 임계** 라는 *측정 lumped 파라미터*로만 봄.
  C65 분포는 SEM(Fig 6b-e)으로 *정성* 관찰(고립섬 → 가교 → SE 표면 완전피복)만.  ⇒ 우리 DEM(구·접촉망)·MPM(소성)·Bazzoun(구 DEM)·Bielefeld(voxel)의 *구조* 차원이 이 논문엔 없다 →
  **frame[5]:** 그들 = *측정/percolation 이론*, 우리 = *구조 → σ(명시적 carbon 3D 망 + 삼중항)*.

### 4.4 압력 구분
- **separator 375 MPa**(LPSCl 단축 압밀) = 우리 제조압 300·Doux 370·Minnmann 380 계열의 "수백 MPa 냉간가압".  **≠ 도전매트릭스 셀-내 2.07 MPa**(163.2 N) — 펠릿이 안 만들어져
  *셀 안에서 직접* 저압 압축(접촉만).  ⚠ 이 **2.07 MPa = 매우 저압** → 도전매트릭스 σ_eff 절대값이 낮은(0 wt% 6.6e-5 « separator 0.43 mS/cm) 한 원인 = *미압밀*.  우리 압밀 케이스(300 MPa)와
  **절대 σ 동일시 절대 금지** — percolation *추세/임계*만 전이.

---

## 5. 결과 상세 — Section-by-section (모든 수치)

### 5.1 §3 LPSCl 합성·미세구조 (Fig 1 XRD+SEM)
**목적:** 도전매트릭스의 SE 상이 순수 결정질 LPSCl 임을 확인.
- **Fig 1a (XRD):** 볼밀 전구체(검정) → 550 °C 열처리 후 **순수 결정질 Li-argyrodite LPSCl(빨강)** 형성(ICSD 418490 reference 일치).  P₂S₅ peak 은 triclinic·저강도라 안 보임.
- **Fig 1b (SEM, LPSCl 분말):** **submicrometer 구형 grain** 이 응집해 **>10 µm 2차입자** 형성.  ⚠ 우리가 쓸 PSD 수치는 *없음*(정성).
- **Fig 1c (SEM, 압밀 separator 표면, 375 MPa):** **plastic compaction(소성 압밀) 거동** 가시화 — "LPSCl 은 *soft nature* 로 알려짐" 명시.  ★ = 우리 **MPM 소성 void-fill·SEM-like 코어보존+경계평탄화**가 모사하려는 바로 그 현상(Sakuda·Doux 와 같은 "황화물 = 냉간 소성압밀" 계보).
- **Fig 1d (사진):** 압밀 separator 를 셀 하부 집전체에 놓은 모습.

### 5.2 §3 LPSCl 이온전도 (Fig 2 Nyquist + Arrhenius) — p<p_c 의 *기준선*
- **Fig 2a (Nyquist, 5–65 °C):** 중-고주파 반원(bulk+GB) 이 T↑ 에서 *사라짐*(high-T 서 bulk 지배) → RT 서 bulk·GB *분리 불가*.
- ★ **σ_ion: 0.12 mS/cm (5 °C) → 0.43 mS/cm (RT) → 2.02 mS/cm (65 °C)**.  **R_total: 354.40 Ω (25 °C) → 58.79 Ω (65 °C)** (T↑→R↓).  Yu/Zhang 문헌 일치.
- ★ **Fig 2b (Arrhenius):** linear → **E_a(Li⁺) = 0.41 eV** (문헌 일치).  선형성 = 측정 T 범위서 LPSCl 열적 안정.
- ⚠ **이 0.41 eV 는 *이온전도 활성화에너지*** — Bielefeld 2019 의 *percolation 임계지수* β=0.41 과 숫자만 같고 물리 완전 무관(절대 혼동 금지).

### 5.3 §3 도전매트릭스 임피던스 (Fig 3) — C65 wt% 별 거동 전환 ★
**표기:** "CM-A" (CM=conducting matrix, A=C65 wt%).
- **Fig 3a (pure SE, 셀-내 압축):** RT~65 °C 까지 *linear*(블로킹), 15 °C 이하 evolved semicircle; **R 1628.50 Ω (15 °C) → 3098.60 Ω (5 °C)** (T↓→R↑, 이온전도).  저주파 허수부 폭증 = **SE/In 계면 blocked charge transport**.  (separator 보다 R 높음 = *셀-내 미압밀*.)
- **Fig 3b (CM-1, 1 wt%):** T-의존은 pure SE 와 유사하나 **R_total 65 °C = 247.67 Ω(> pure SE 102.10), RT = 522 Ω**.  RT 미만 mid-f stretched semicircle + 저주파 blocking 허수부 → **여전히 이온 지배(p<p_c)**.
- **Fig 3c (CM-3, 3 wt%):** ★ **거동 전환 시작** — **R_total 302.43 Ω (65 °C) → 288.03 Ω (15 °C) → 272.17 Ω (5 °C)** (★ **T↓→R↓**, 이온과 *반대* = 전자전도 기여 출현).  저주파 **blocking 사라짐**(전하수송 *완전 차단 안 됨*) → 부분 전자경로.  45 °C 이하 R < pure SE.
- **Fig 3d (CM-4, 4 wt%):** ★★ **완전 전환** — **ohmic R 이 전 T 범위 거의 불변(33.50 Ω 25 °C / 43.89 Ω 65 °C, T-무상관)**, **주파수 무관**, 용량 없음.  고주파 inductive(셀 와이어 artifact).  = **pure ohmic resistor = percolation 도달**.  (R 이 T 와 *무상관*이나 측정시간 따라 약간↑ = SE-카본 계면반응 hint, ref [22] Oh LGPS+AB 계면반응.)
- **Fig S2 (CM-5·CM-10, ≥5 wt%):** CM-4 와 동일(주파수 무관·용량 없음).  **5 wt%→pure C65 사이 평균 R 0.50→0.24 Ω 만** 변화(거의 포화).  ⇒ **C65 가 σ_eff 를 지배하는 *전자 ohmic 망* 완성**.

### 5.4 §3 온도의존 σ_eff (Fig 4) — 이온 vs 전자 지배의 *부호* 구분
- **Fig 4 (ln(T·σ_eff) vs 1000/T, C65 0/1/3/4/5/10/100 wt%):** pure SE 와 *동일 가정*(SE=pure 이온전도체, C65=pure 전자전도체) 하에:
  - **pure SE·CM-1 (≤1 wt%):** T↑ → σ_eff↑ (**이온전도 Arrhenius 지배**).
  - ★ **≥3 wt%:** T↑ → σ_eff *↓* (**전자전도 지배** — 전자는 보통 T↑서 약간↓; 이온의 강한 ↑가 사라짐).
  - ⇒ **σ_eff 의 *온도 부호*가 3 wt% 부근서 뒤집힘** = 이온→전자 지배 전환의 직접 지표.
- **RT (25 °C):** C65↑ → σ_eff *체계적 상승*; pure SE·CM-1·CM-3 는 같은 order, **CM-4 서 ~1 order 도약(3 wt% 1.66×10⁻⁴ vs 4 wt% 1.36×10⁻³)**.

### 5.5 §3 ★ percolation 곡선 (Fig 5) — p_c ≈ 4 wt% 의 핵심 그림
- **Fig 5 (σ_eff @ 25 °C vs C65 wt%, log-y, x = 0/1/3/4/5/10/100 비스케일):** ★★ **step-like progression** —
  - **p < p_c (0,1,3 wt%):** σ_eff ≈ pure SE 수준(6.6e-5 → 9.5e-5 → 1.66e-4) — 회색영역 "p<p_c" 라벨.
  - **p_c (4 wt%):** 1.36×10⁻³ — 회색영역 "p_c" 라벨(전이).
  - **p > p_c (5,10,100 wt%):** 1.02×10⁻¹ → ~1.1×10⁻¹ → ~0.2 — "p>p_c" 라벨, 포화.
  - ★ **3→5 wt% 사이 ~3 orders 급상승** = **typical percolation threshold 현상**(sintering ceramics·fuel cell·carbon-nanotube polymer 와 같은, ref [41–43]).
- ★ **본문 해석:** "p<p_c 면 σ_eff ≈ pure SE; p>p_c 면 C65 가 percolating network 형성 → C65 ≥ 4 wt% 면 전하수송이 *거의 전적으로 C65 나노입자 망의 전자전류*로 진행(σ_eff ≫ pure SE 이온전도)".

### 5.6 §3 ★ 미세구조 (Fig 6) — percolation 의 *형상* 증거
- **Fig 6a (모식):** p<p_c = C65 가 SE 안에 **isolated islands** / p_c = C65 가 **network 형성** / p>p_c = C65 가 SE grain 표면 *완전피복* + 이온전도 *불가피하게 감소*.
- **Fig 6b-e (top-view SEM, BSE, C65 1/2/5/10 wt%):** 노랑화살표=SE grain, 진파랑화살표=C65 nanoparticle —
  - **CM-1 (1 wt%):** SE grain 거의 *완전 노출*; C65 고립 분산, **망 미형성**.
  - **CM-2 (2 wt%):** C65 응집체 *약한 가교*만.
  - **CM-5 (5 wt%):** ★ **미세구조 현저히 변화 — SE grain 표면 거의 전체가 C65 로 피복**.
  - **CM-10 (10 wt%):** 10 wt% 만으로도 **C65 가 SE 상을 거의 완전 피복**(균열도 보임).
- ★ **본문:** "C65 의 *높은 비표면적(62 m²/g)* 이 SE·C65 밀도가 유사(1.83 vs 1.60)함에도 *낮은 3<p_c<5 wt%* 에서 3D 망을 쉽게 형성하게 한다" — **percolation 임계는 *밀도*가 아니라 *입자 표면적/형상*이 지배** → Bielefeld(작은 AM=高표면적=낮은 p_c) 인용.

### 5.7 §4 결론 + 설계 가이드라인
- **p_c ≈ 4 wt% C65** (도전매트릭스 기준).
- ★ **설계 가이드라인:** 황화물 양극 *전형* 70 wt% AM → 도전매트릭스(나머지 30 wt% SE 영역)의 4 wt% C65 = **양극 전체로는 ~1.2 wt% C65** 면 전자 percolate.
- **4 wt% = "최적 조성"** 후보(高 전자전도 + 低 carbon = 분해/부반응 최소).  CAM 패시베이션 코팅이 부분 전자전도를 *떨어뜨릴* 때 특히 중요(전자망 보강 필요).
- **향후:** 다양한 AM × C65/LPSCl 분율의 full-cell 사이클; **전자 블로킹 조건 EIS** 로 이온↔전자 상호작용 분리.

---

## 6. Figure / Table set ★ (모든 그림·표 + 우리가 쓸 점)

### 6.1 본문 Figures
| Fig | 내용 (무엇을 보여주나) | 핵심 수치 | 우리가 참고할 점 |
|---|---|---|---|
| **1a** | XRD (전구체 vs 열처리 LPSCl) | ICSD 418490 일치 | 순수 결정질 LPSCl 확인 |
| **1b** | SEM LPSCl 분말 | submicron grain, >10 µm 응집 | ⚠ PSD 수치 없음(정성) |
| **1c** | SEM 압밀 separator(375 MPa) | — | ★ **plastic compaction(soft LPSCl)** = 우리 MPM 소성 모사 대상 |
| **1d** | 셀 사진 | — | — |
| **2a** | LPSCl Nyquist (5–65 °C) | R 354.40→58.79 Ω | bulk+GB high-T 융합 |
| **2b** | LPSCl Arrhenius | **E_a 0.41 eV** | ★ bulk 앵커 + E_a (⚠ β=0.41 와 무관) |
| **3a** | pure SE 도전매트릭스 Nyquist | R 1628.50(15 °C)→3098.60(5 °C); 저주파 blocked | ★ p<p_c 이온 *기준선* |
| **3b** | CM-1 (1 wt%) Nyquist | R 522(RT)/247.67(65 °C) | ★ p<p_c (이온 지배) |
| **3c** | CM-3 (3 wt%) Nyquist | R 302.43→272.17 Ω (T↓→R↓) | ★ **전이 시작**(전자 기여 출현) |
| **3d** | CM-4 (4 wt%) Nyquist | R 33.50/43.89 Ω, 주파수·T 무관 | ★★ **pure ohmic = percolation 도달** |
| **★ 4** | ln(T·σ_eff) vs 1000/T (7조성) | ≤1 wt% T↑→σ↑ / ≥3 wt% T↑→σ↓ | ★ **온도 부호 반전 = 이온↔전자 지배 전환** |
| **★★ 5** | **σ_eff @25 °C vs C65 wt% (percolation 곡선)** | **p_c≈4 wt%; 1.66e-4→1.36e-3→1.02e-1 (3→4→5 wt%)** | ★★ **우리 σ_e carbon percolation 의 절대 앵커 곡선** |
| **★ 6a** | percolation 단계 모식 (island→network→피복) | — | ★ p_c 전후 carbon 망 형성 그림 |
| **★ 6b-e** | top-view SEM (C65 1/2/5/10 wt%) | 1 wt% 고립 → 5 wt% SE 완전피복 | ★ **percolation 의 형상 증거**(우리 carbon morphology seed 검증) |

### 6.2 SI Figures & Tables
| 항목 | 내용 | 우리가 참고할 점 |
|---|---|---|
| **Fig S1** | 전구체 미처리 XRD | 합성 출발물질 |
| **Fig S2** | CM-5·CM-10 Nyquist (5–65 °C) | ★ ≥5 wt% 전부 ohmic·주파수무관 = percolation 확립 |
| **Fig S3** | DC 측정 (CM-4) | 전자전도 ohmic 교차확인 |
| **Fig S4** | 추가 EIS RT (p_c 초과 조성) | percolation 이후 σ |
| **Fig S5** | C65 나노입자 SEM | C65 형상(nano primaries) |
| **★ Table 1** | 조성표 (wt%↔vol% C65, mg/pellet) | ★ wt%→vol% 환산(99:1→1.16 … 90:10→11.44 vol%) |
| **Table 2** | EIS 온도 protocol (separator/matrix) | 측정 순서 |

### 6.3 ★ σ_eff vs C65 데이터 (우리 정량 앵커) — Fig 5 + 본문 verbatim/digitized
| C65 wt% | C65 vol% | σ_eff @25 °C (S/cm) | 영역 | src |
|---|---|---|---|---|
| 0 (pure SE) | 0 | ≈ 6.6 × 10⁻⁵ | p<p_c | digitized |
| 1 (CM-1) | 1.16 | ≈ 9.5 × 10⁻⁵ | p<p_c | digitized |
| 3 (CM-3) | 3.47 | **1.66 × 10⁻⁴** | p<p_c (직하) | **stated** |
| 4 (CM-4) | 4.62 | **1.36 × 10⁻³** | **p_c** | **stated** |
| 5 (CM-5) | 5.77 | **1.02 × 10⁻¹** | p>p_c | **stated** |
| 10 (CM-10) | 11.44 | ≈ 1.1 × 10⁻¹ | p>p_c | digitized |
| 100 (pure C65) | 100 | ≈ 0.2 (R≈0.25 Ω) | p>p_c | **stated** |
> ★ **읽기:** (1) **3→5 wt% 사이 ~3 orders 급상승** = percolation step(p_c≈4); (2) **5→10→100 wt% 거의 포화**(망 형성 후 수확체감); (3) p<p_c 의 σ_eff(6.6e-5~1.66e-4) ≈ pure-SE
> *이온전도*(이 셀-내 미압밀 LPSCl 의 σ_ion 수준 — separator 0.43 mS/cm 보다 낮음 = 2.07 MPa 미압밀).  ⇒ 이 곡선이 "**carbon wt% → 전자 percolation 게이트**"의 정량 결정체.
> ⚠ **σ_eff 절대값 전이 금지**(미압밀·도전매트릭스만·AM 없음); **임계 위치(p_c≈4 wt%)와 step 형태**만 우리에게 유효.

---

## 7. ★ 메커니즘 — percolation 임계 전후 인과 사슬 (한눈에)

```
                         ┌──────────── C65 함량 증가 (0 → 100 wt%) ────────────┐
                         │                                                     │
         [p < p_c (<4 wt%)]              [p ≈ p_c (≈4 wt%)]            [p > p_c (≥5 wt%)]
         C65 = 고립 섬                    C65 = 연결 cluster              C65 = SE 표면 완전피복
         (SEM Fig 6b CM-1)               (Fig 6a 중앙)                   (SEM Fig 6d CM-5)
                │                              │                              │
         전자망 미형성                   network 형성 (step)             percolating e⁻ network
                │                              │                              │
         σ_eff ≈ pure-SE 이온전도        σ_eff ~1 order ↑               σ_eff ~3 orders ↑ (포화)
         (6.6e-5~1.66e-4 S/cm)          (1.66e-4 → 1.36e-3)            (1.02e-1 → 0.2 S/cm)
                │                              │                              │
         임피던스: 저주파 blocked         부분 전자경로                  주파수 무관 + 용량 없음
         (In 블로킹), 온도의존(T↑→σ↑)    (blocking 사라짐, T↓→R↓)       = pure ohmic (T 무상관)
                │                              │                              │
         ★ 이온전도체 거동                전이                          ★ 전자전도체(ohmic) 거동
                                                                              │
                                                                 + 이온전도 *불가피 감소*(SE 피복)
                                                                 + SE-카본 계면 분해 hint(ref[22])
                                                                              │
                                                              설계: p_c 직상 *최소 C65*(4 wt% matrix
                                                              = 1.2 wt% cathode) = 전자 ON + carbon 최소
```
★ **요지:** 전자 percolation 은 *연속*이 아니라 *임계(p_c≈4 wt%)에서 step* 으로 켜진다(고립섬 → 연결망).  임계 위치는 **C65 의 高비표면적(62 m²/g)** 이 정한다(밀도 아님) →
作은 입자·高표면적 = 낮은 p_c (Bielefeld).  p_c 직상 *최소 carbon* 이 전자전도 ON 과 carbon-유발 부작용(SE 부피점유·분해, 자매논문) 최소를 동시 달성하는 최적.

---

## 8. Post-processing ★
- **무엇:**
  - **percolation 임계 p_c 추출**: σ_eff(C65 wt%) 곡선(Fig 5)의 *step-like 급상승* 위치 + 임피던스 *시그니처 전환*(이온 blocking → ohmic 주파수무관)으로 p_c≈4 wt% 결정.  percolation
    *이론*(Newman-Ziff/연속체)은 *해석 틀*로만(시뮬 아님).
  - **EIS 등가회로 피팅 (Z-View 4.0d) → R**: 영역별 회로(RT 이상 tail intercept / RT 미만·1 wt% R₀+(R₁∥CPE)+CPE / 3 wt% R+2 Randles / ≥4 wt% 단일 R).
  - **σ_eff = (d/A)·R⁻¹ (Eq 1)**: R → 전도도 환산(d 두께·A 면적, caliper 실측).
  - **Arrhenius (ln(T·σ) vs 1/T) → E_a**: LPSCl 0.41 eV; 도전매트릭스는 *혼합전도체*라 단순 Arrhenius 부적용(이온/전자 부호로 지배상 판별).
  - **DC-polarization**: 전자전도 ohmic 거동 교차확인(Fig S3/S4).
  - **XRD(상 동정) / SEM-BSE(C65 분포·피복 정성) / BET(C65 62 m²/g)**.
- **도구:** Bio-Logic VSP-300(EIS 7 MHz–1 Hz), **Z-View 4.0d**(피팅), Seifert Sun 3003(XRD), Zeiss Sigma 300VP(SEM-BSE).  ⚠ **porosity·접촉면적·배위수·tortuosity 같은 *구조 정량 후처리는 없음*.**
- **수치화·기록:** 7조성(C65 0–100 wt%) × T(5–65 °C) 의 R → σ_eff 막대/Arrhenius; p_c 는 σ_eff-vs-wt% step + 임피던스 시그니처; C65 분포는 SEM-BSE 정성.

---

## 9. ★ 우리 DEM+MPM + 전달 파이프라인 대비  →  `our_dem_baseline.md`

> ⚠ **동시성 주의:** 본 절은 digest *안*에 작성 (INDEX.md/comparison_vs_ours.md 는 read-only → 건드리지 않음).  메인 세션이 이 절을 보고 INDEX/comparison 에 반영.

| 항목 | 이 논문 (Reisacher 2023) | 우리 | 차이 / 이유 |
|---|---|---|---|
| **방법** | **실험 EIS(percolation) + DC-polarization + σ_eff(C65)** | **DEM Kirchhoff/Holm σ-솔버** + Stage-E + MPM | ★ 그들=측정/percolation 이론, 우리=구조→σ(명시적 carbon 3D 망).  frame[4] 외부 *앵커*(경쟁 아님) |
| **소재(SE/CA)** | ★ **LPSCl(=우리 EXACT SE) + C65 카본** | LPSCl + NMC811 + CBD(SuperP/VGCF/PTFE) | ★★ **SE 동일 → 소재 전이 보정 불필요**(할라이드 논문과 결정적 차이); 단 그들 = *AM 없는 SE-카본 매트릭스* |
| **★ 전자 percolation p_c** | ★★ **p_c ≈ 4 wt% C65 *실측*** | σ_e percolation 게이트 / **f_p³ isotropy**(Stage 22.5); Bielefeld p_c=7.83·ln(d_AM)+36.67 보유 | ★★ **carbon 전자망이 *언제 켜지나*의 절대 앵커**(backlog A4) — 우리 σ_e 폼에 carbon-wt% percolation 게이트 calibration |
| **σ_eff(C65 wt%) 곡선** | ★ **step at p_c**(1.66e-4→1.36e-3→1.02e-1, 3→4→5 wt%) | σ_e *계산*(Stage 22.5, LOOCV 0.953) | ★ carbon wt% → σ_e *검증 곡선*(절대값 아닌 *step 형태/임계* 매핑) |
| **σ_ionic ↔ σ_e 크로스오버** | ★ **p<p_c 이온 지배 / p>p_c 전자 ohmic** | ★ **우리 삼중항**(σ_ionic SE-backbone / σ_e AM+carbon-backbone) | ★★ 두 채널 부호 전환을 *carbon 축*에서 정량 = 우리 삼중항이 잡아야 할 크로스오버(backlog A3/A4) |
| **carbon morphology** | **C65 nano(62 m²/g) 분기 aggregate**, SEM 고립섬→피복 | additives.py `seed_carbon_black`(분기 fractal chain) + SuperP/VGCF | ★ **高표면적 → 낮은 p_c** = 우리 carbon seed 형상/표면적 모델 검증; Fig 6 SEM = morphology 시드 ground-truth |
| **bulk σ_ion(LPSCl)** | **0.43 mS/cm @ RT**(separator) | Cronau 3.0(채택, 단결정-라벨) | ★ bulk 앵커 *하단*(스프레드 0.43↔3.0); ⚠ 셀/압력/온도 차 → 절대 직접대조 금지 |
| **압밀 porosity** | **n/a**(미측정) | DEM 15.6 %·MPM 16.7 %(real_14) | 그들 porosity 안 줌 → **우리 강점**(정량 porosity·Heckel) |
| **압력** | separator 375 / matrix in-cell **2.07 MPa** | 제조 300 MPa(Heckel P_y 138) | ★ separator 375 ≈ 우리 제조; matrix 2.07 = 매우 저압(접촉만) → **σ 절대값 미압밀 → 전이 금지** |
| **삼중항 σ_e/σ_thermal** | **이온·전자 σ_eff 만**(thermal 없음) | ★ **σ_ionic+σ_e+σ_thermal 삼중항** | ★ 우리 삼중항 우위(frame[5]) |
| **소성/morphology** | 없음(percolation/회로) | MPM 진짜 SHAPE 소성·void-fill | 우리 MPM 고유(frame[5]); 단 Fig 1c "soft LPSCl plastic compaction" 이 우리 MPM 전제 *실험 정당화* |

**핵심 정합/상보 4가지:**
1. ★ **p_c ≈ 4 wt% C65 = 우리 σ_e carbon percolation 의 *literature-grounded 절대 앵커*(backlog A4)** — LPSCl(우리 EXACT SE) + C65 의 전자 percolation 임계를 *실측* →
   우리 σ_e percolation 게이트/f_p³ 를 carbon-wt% 축에서 calibration.  할라이드 논문과 달리 **소재 전이 보정 불필요**.
2. ★ **σ_ionic↔σ_e 크로스오버를 *carbon 축*에서 정량(p<p_c 이온/p>p_c 전자)** = 우리 삼중항(SE-backbone σ_ionic ↔ AM+carbon-backbone σ_e)이 잡아야 할 부호 전환의 실험 앵커(A3/A4).
3. ★ **碳 高비표면적(62 m²/g) → 낮은 p_c(4 wt%) = 우리 carbon morphology seed(분기 aggregate)·Bielefeld(작은 AM=낮은 p_c) 와 정합** — Fig 6 SEM(고립섬→망→피복)이 우리 `seed_carbon_black` 검증 ground-truth.
4. ★ **압밀 porosity·Heckel·삼중항 thermal = 우리 *추가* 칸(frame[5])** — 그들이 비운 구조/역학/thermal 을 우리 DEM+MPM 이 채움(그들 = percolation/측정 절반, 우리 = 구조→σ 절반).

---

## 10. ★ 우리 DEM+MPM 대비 (comparison vs ours) — 사용자 지정 필수 절

> 이 절은 **그들의 *실험* 전자-percolation(LPSCl+C65)** 과 **우리 *시뮬레이션* σ_e**(AM-backbone + carbon 도전제)의 정밀 대조.  핵심: 그들 p_c≈4 wt% 는 *carbon 망*의 진짜 percolation 임계 → 우리 **f_p³ isotropy / percolation 게이트**와 같은 물리.

### 10.1 그들 p_c(carbon 전자망) vs 우리 percolation 표현
- **그들:** carbon(C65) 망의 **전자 percolation 임계 p_c ≈ 4 wt%**(범위 3<p_c<5) — *site/continuum percolation* 의 step.  σ_eff(p) 는 p_c 에서 ~3 orders 도약.
- **우리 σ_e(Stage 22.5):** AM(NMC811)이 *주* 전자 backbone (φ_AM⁴ · √A_AM-AM · f_p³ isotropy); **carbon(CBD)은 σ_e *기여*로 들어가나 *명시적 percolation 게이트*는 약함**(backlog A4 미적용).
  → ★ **그들 데이터가 채우는 것:** 우리 σ_e 에 *carbon-wt% percolation 게이트*(예: g_carbon = f(wt_C65 − p_c) 류, p_c≈4 wt% LPSCl-anchored)를 추가할 절대 calibration 점.
- **우리 f_p³ 의 물리적 정당화:** 그들 step-like σ_eff(p_c) = "3D 망이 임계서 갑자기 가로지른다"는 percolation 의 본질 → 우리 **f_p³(=P(percolate x∧y∧z) 3D isotropy)** 과 **Bielefeld β=0.41(3D site-perc)** 의 같은 계보.  ⚠ 단 **그들 p_c 는 *carbon(전자상)* 의 임계**, 우리 f_p³ 는 보통 *SE/AM backbone* 에 적용 → 매핑 시 "carbon 상의 percolation"으로 *별도 게이트* 필요(SE/AM 게이트 재사용 금지).

### 10.2 그들 σ_eff(C65) step vs 우리 σ_e(carbon wt%)
- **그들:** σ_eff 3→4→5 wt% = 1.66×10⁻⁴ → 1.36×10⁻³ → 1.02×10⁻¹ S/cm (3 orders).  포화 5→100 wt% 거의 없음.
- **우리:** σ_e 는 carbon wt% 의 *완만한* 함수(현 폼) → ★ **그들 step 이 "우리 폼이 p_c 부근서 더 가팔라야 한다"는 형태 정보** 제공.  단 ⚠ **절대값 전이 금지**(그들 = AM 없는 SE-카본 매트릭스 + 셀-내 2.07 MPa 미압밀 → σ_eff 0 wt% 가 6.6e-5 로 낮음; 우리 = AM 포함 압밀 양극).  *step 위치(p_c)와 형태(급상승→포화)*만.

### 10.3 크로스오버 = 우리 삼중항이 잡아야 할 것
- 그들 **p<p_c 이온 지배(σ_eff≈σ_ion, T↑→σ↑) / p>p_c 전자 지배(ohmic, T↓→R↓)** = σ_ionic↔σ_e *지배상 전환*.
- 우리 삼중항은 σ_ionic·σ_e 를 *독립 계산* → 두 채널의 *합/min* 이 어느 게 율속인지(이온 vs 전자)를 *같은 케이스에서* 비교해야 그들 크로스오버를 재현.  → backlog A3/A4 의 σ_e↔σ_ion 경쟁이 바로 이 그림.

### 10.4 정직한 caveat (over-claim 방지)
- ⚠ **AM 없음:** 이건 *도전 매트릭스(SE+C65)* 만 — 우리 *복합 양극(AM+SE+C65)* 과 직접 동일시 금지.  p_c(4 wt% C65 *in matrix*) → 양극 환산 시 *matrix 분율*(70 wt% AM 이면 ~1.2 wt%)로 재계산.
- ⚠ **미압밀(2.07 MPa):** σ_eff 절대값이 우리 압밀(300 MPa)보다 낮음 → 절대 σ 전이 금지, percolation 임계/형태만.
- ⚠ **digitized vs stated:** 3/4/5/100 wt% σ_eff 는 stated; 0/1/10 wt% 는 Fig 5 digitized(TREND only, ±, false precision 금지).
- ⚠ **E_a 0.41 eV ≠ Bielefeld β 0.41** — 숫자 우연, 물리 무관(혼동 절대 금지).

---

## 11. 적용가능성 (applicability to our model) — 사용자 지정 필수 절

> ★ **이 논문 = 우리 CARBON 도전제 전자 percolation 의 실험 앵커(backlog A4 se_coating/carbon).  LPSCl = 우리 EXACT SE → 직접 전이.**  아래는 `scripts/additives.py` + σ_e percolation 폼에 *구체적으로* 어떻게 꽂는가.

### 11.1 ★ σ_e 폼에 carbon percolation 게이트 추가 (backlog A4 핵심)
- **현재:** 우리 σ_e(Stage 22.5)는 AM-backbone(φ_AM⁴·√A_AM-AM·f_p³) 중심; carbon 은 σ_e *기여*만, *명시적 percolation 임계 없음*.
- **이 논문이 주는 calibration:** **p_c ≈ 4 wt% C65 (in SE-carbon matrix)** = carbon 전자망이 켜지는 임계.  → σ_e 에 **carbon 게이트** g_C 추가 가능:
  `g_C = sigmoid(k·(wt_C65,matrix − p_c))` 또는 percolation power-law `σ_C ∝ ((p − p_c)/p_c)^t` (t≈2, 3D), **p_c = 4 wt% (LPSCl-anchored, 소재 보정 불필요)**.
  - ⚠ **matrix wt% 변환:** 양극 케이스의 carbon wt% 를 *SE 영역(matrix) 기준* 으로 재계산(carbon / (carbon+SE)) 후 p_c=4 wt% 와 비교 — 양극 전체 wt% 와 혼동 금지(70 wt% AM 양극 1.2 wt% carbon ≈ matrix 4 wt%).
- **검증 곡선:** §6.3 표(σ_eff vs C65 wt%, step at 4) = 우리 σ_e(carbon%) 폼의 *형태* 벤치마크(절대값 아닌 step 위치/포화).

### 11.2 ★ additives.py 매핑 — carbon seed 의 percolation 거동
- `scripts/additives.py`의 `seed_carbon_black`(SuperP 분기 fractal aggregate, surface_frac AM-coating) + `recipe_counts_real`(carbon wt% → 개수) 가 *carbon 개수/분포*를 만듦.
  → ★ **이 논문 검증점:** 우리 carbon seed 가 **matrix 4 wt% 부근서 *3D 연결(percolate)***되는지(cluster spanning) 확인 = Fig 6 SEM(1 wt% 고립 → 5 wt% 피복)의 *시뮬 재현*.
  C65 비표면적 62 m²/g·밀도 1.60(≈ 우리 SuperP 1.90 근사) → **高표면적 = 낮은 p_c** 를 우리 seed 형상(분기 chain 길이 k, surface_frac)이 반영하는지.
- ★ **MPM scaffold 에 carbon 상 추가**(additives.py 는 이미 MPM material phase 로 carbon seed): carbon vol% 가 SE 영역을 점유(Kim 2024 짝) + matrix 4 wt% 서 전자 percolate → 두 carbon 논문(Reisacher 임계 + Kim 부피점유)을 *한 scaffold* 에서 동시 표현 가능.

### 11.3 ★ Bielefeld p_c 식과의 직접 연결(우리 보유 데이터)
- 우리 `docs/data/bielefeld2019_percolation_thresholds.csv`: **전자 p_c = 7.83·ln(d_AM/µm) + 36.67 vol% (AM 입자 기준)**, β=0.41.
- ★ 이 논문 **p_c≈4 wt% C65 (≈4.62 vol%, *carbon* 기준)** = Bielefeld 의 *AM-percolation* 과 *상보*(그들 = AM 전자상의 임계, 이 논문 = *carbon 첨가상*의 임계).  → 우리 모델에 **두 전자 percolation 게이트**(AM backbone + carbon additive)를 *각각* 둘 근거; carbon 게이트 임계는 이 논문(4 wt%), AM 게이트는 Bielefeld(d_AM 의존).
- ★ 그들 "smaller AM → earlier p_c (高표면적)" = 우리 σ_e *입경 의존* + Bielefeld 식의 *실험 확증*.

### 11.4 데이터/매핑 산출물
- CSV: `docs/data/reisacher2023_percolation.csv` (p_c, σ_eff vs C65 wt%/vol%, σ_ion vs T, E_a, ρ, BET).
- 매핑 순서: (carbon wt% in cathode) → (carbon wt% in SE-matrix = C/(C+SE)) → compare p_c=4 wt% → σ_e carbon 게이트.

---

## 12. ★ frame[4] 위치 (experimental anchor, not a DEM competitor) — 사용자 지정 필수 절

> ★ **이건 실험 논문 → 우리 시뮬레이션의 *경쟁자*가 아니라 *외부 앵커/검증*이다.**  frame[4]: DEM·MPM 은 각각 *실험* 에 독립 calibration → 실험과 일치 = 교차검증, 불일치 = 정량화된 모델 한계(정보).

### 12.1 이 논문이 주는 것 (앵커)
- ★ **carbon 전자 percolation 임계 p_c ≈ 4 wt% C65 (LPSCl, 실측)** = 우리 σ_e carbon-percolation 게이트의 *진짜 임계값*(우리가 *예측해야* 할 값의 ground-truth).
- ★ **σ_eff(C65 wt%) step 곡선** = 우리 σ_e(carbon%) 폼의 *형태* 벤치마크.
- ★ **이온↔전자 크로스오버(p_c 전후)** = 우리 삼중항 σ_ionic↔σ_e 경쟁의 검증.
- ★ **LPSCl bulk σ_ion 0.43 mS/cm·E_a 0.41 eV** = bulk 앵커 스프레드(하단)·E_a 참조.

### 12.2 우리 *시뮬레이션*이 *추가*하는 것 (그들이 못 주는 것)
- ★ **명시적 3D carbon 접촉망 σ_e**(Kirchhoff/Holm) — 그들은 σ_eff *측정*만, 우리는 *어느 carbon 접촉이 percolate 하는지* 명시.
- ★ **전달 삼중항**(σ_ionic + σ_e + **σ_thermal**) — 그들 thermal 없음.
- ★ **구조 정량**: porosity(15.6 %)·Heckel(P_y 138)·coordination·coverage·tortuosity — 그들 전부 n/a.
- ★ **MPM morphology**: carbon/SE 소성 형상·void-fill — 그들 SEM 정성만.  (Fig 1c "soft LPSCl plastic compaction" 이 우리 MPM 전제를 *실험 정당화*.)
- ★ **미세구조 예측**: 우리는 공정 numbers → 구조 *예측*(그들은 *측정*만).

### 12.3 softer novelty framing (정직)
- 우리 novelty 는 "전자 percolation 을 *처음 봤다*"가 아니라(이 논문이 *실측*) — **(i) 그 percolation 을 *명시적 접촉망 σ*로 풀고, (ii) 이온·전자·열 *삼중항*으로 동시에, (iii) 압밀 *구조 예측*(porosity/Heckel/morphology)과 결합**한다는 것.  이 논문은 **우리 carbon-percolation 게이트가 *맞는 임계(4 wt%)*를 내는지 검증하는 외부 시금석**(frame[4]).  수렴=교차검증, 불일치(절대 σ — 미압밀/AM-없음)=정량화된 측정-조건 차이.

---

## 13. 인용 가능 문장 (deck/paper용)
- "Reisacher et al. (Batteries 2023) experimentally locate the **electronic percolation threshold of a Li₆PS₅Cl–C65 conducting matrix at p_c ≈ 4 wt% C65** (3 < p_c < 5 wt%): below p_c the effective conductivity tracks the pure-SE ionic value (≈ 6.6×10⁻⁵ S cm⁻¹, temperature-activated, low-frequency-blocked), while above p_c the impedance is frequency-independent and ohmic (σ_eff jumps ~3 orders, 1.66×10⁻⁴ → 1.02×10⁻¹ S cm⁻¹ over 3 → 5 wt%) — the literature-grounded anchor for our σ_e carbon-percolation gate, transferable without material correction because the SE is our exact Li₆PS₅Cl."
- "Because C65's high specific surface area (62 m² g⁻¹) lets it form a 3D network at as little as 3–5 wt% despite near-equal density to the SE (1.60 vs 1.83 g cm⁻³), the percolation threshold is governed by particle surface/morphology, not density — consistent with our carbon-seed model and with Bielefeld's 'smaller AM → earlier p_c' law."
- "Translated to a 70 wt% active-material cathode, p_c = 4 wt% in the matrix corresponds to only **1.2 wt% C65 in the full cathode** — a minimal-carbon design guideline that bounds the σ_e/σ_ion trade-off our triad predicts (more carbon percolates electrons but, per the sister carbon papers, occupies SE volume and accelerates sulfide decomposition)."

---

## 14. 주의/한계 (over-claim 방지)
- **시뮬레이션 0** — DEM/MPM/FEM/RNM 없음.  porosity(정량)·Heckel·coordination Z·coverage%·tortuosity·E_SE·σ_y·PSD **전부 n/a**.  percolation 은 *이론 해석 틀*로만 인용(시뮬 아님).
- **★ AM 없는 *도전 매트릭스(SE+C65)* 만** — 우리 *복합 양극(AM+SE+C65)* 과 직접 동일시 금지.  p_c(4 wt% C65 *in matrix*)를 양극 전체 wt% 와 혼동 금지(70 wt% AM → ~1.2 wt%).
- **★ σ_eff 절대값 전이 금지** — 도전매트릭스는 **셀-내 2.07 MPa 미압밀**(separator 만 375 MPa) → σ_eff 0 wt% 6.6e-5 « separator 0.43 mS/cm = 미압밀 탓.  우리 압밀(300 MPa) 케이스와 절대 σ 비교 금지; **percolation 임계(p_c≈4)·step 형태·이온↔전자 부호**만.
- **bulk σ_ion 0.43 mS/cm @ RT** = LPSCl bulk 앵커 *하단* — 셀/압력/온도/GB·로트 차로 Cronau 3.0 과 ~7× 스프레드 → **절대 직접대조 금지**, 스프레드로만.  우리 σ_grain prefactor 는 Cronau 3.0 유지.
- **digitized vs stated** — 3/4/5/100 wt% σ_eff = **stated**; 0/1/10 wt% σ_eff·Arrhenius 점 = **digitized**(TREND only, false precision 금지).  p_c≈4 wt% = stated.
- **⚠ E_a(Li⁺) 0.41 eV ≠ Bielefeld 2019 β=0.41 (percolation 지수)** — 숫자 우연, 물리 완전 무관(혼동 절대 금지).
- **C65 ≠ SuperP/VGCF 완전동일 아님** — C65(Super C65, Imerys 도전 카본블랙, 62 m²/g) 는 우리 additives.py SuperP(1.90 g/cm³)와 *유사*하나 별개 grade; VGCF(1D 섬유)와는 형상 다름.  *형상/표면적* 차 보정 후 매핑.
- **frame[4]/[5]:** 이 논문 = *실험 절반*(전자 percolation 측정 + σ_eff + 미세구조 SEM); *모델 절반*(명시적 접촉망 σ 삼중항·MPM 변형장·정량 porosity/Heckel)은 **우리가 추가**.  수렴=교차검증, 절대 σ 불일치(미압밀·AM-없음)=정량화된 측정-조건 차.  **p_c≈4 wt%·σ_eff step·이온↔전자 크로스오버** 세 메시지가 흡수 핵심.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
