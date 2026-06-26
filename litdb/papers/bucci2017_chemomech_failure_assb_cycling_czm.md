# ⭐frame[5] 시간축 / 사이클-균열 — Modeling of internal mechanical failure of all-solid-state batteries during electrochemical cycling, and implications for battery design — Bucci, Swamy, Chiang, Carter (J. Mater. Chem. A 2017)

> slug `bucci2017_chemomech_failure_assb_cycling_czm` · DOI `10.1039/c7ta03199h` · type `FEM (coupled electro-chemo-mechanical) + CZM (cohesive-zone damage)` · PDF `Bucci_2017_JMCA_InternalMechanicalFailure_ASSB_Cycling_CZM.pdf` · digested `2026-06-26` · status ✅ · WISHLIST #25 (fracture / frame[5])
>
> ## ★★★ 이 논문의 위치 — 우리 *압밀* 파괴(Auerbach/Lawn, DEM)의 *사이클* 짝, 그리고 우리 frame[5]의 *시간축* 공백 ★★★
> MIT (Yet-Ming Chiang 그룹 + W. Craig Carter) — **ASSB 역학신뢰성의 *최초* 정량 해석**(저자 자체 주장: "to our knowledge,
> ours is the first model to quantitatively assess mechanical reliability of all-solid-state batteries, and predict the
> extension of fracture caused by electrochemical cycling").  **coupled electro-chemo-mechanical FEM + cohesive-zone model
> (CZM)** 로 *사이클 중* SE 균열을 모사.  ★ 우리 Auerbach/Lawn 균열은 **AM-AM 접촉의 *압밀-시점* 균열**(접촉응력 driver)이고,
> 우리 MPM J2 는 **연성 소성**이라 *SE 취성균열* 을 못 한다 → **이 논문이 정확히 우리가 *없는* 두 칸(사이클-시점 + SE-취성)을
> 채운다** (frame[5] 시간축 + 취성 메커니즘 공백).  backlog **A10**(사이클 chemo-mechanics future) + **B6**(operating-pressure
> 시간축) + **D6**(SE 취성균열 = de Vaucorbeil continuous-damage/cohesive MPM 경로)의 **literature 레퍼런스**.
>
> ★ **세 핵심 결과(외우기):**
> 1. **균열 *방지* 조건 = 전극입자 팽창 < 7.5 % AND G_c ≥ 4 J/m²** (대부분 Li-삽입화합물 < 7.5 % → 만족 가능).
> 2. **★ 반직관: *compliant*(말랑한) SE — Young's modulus ~E_SE = 15 GPa 정도 — 가 *더* micro-cracking 에 취약** →
>    "황화물(말랑) SE 가 bulk 전지에 산화물(딱딱)보다 유리하다"는 *통념을 반박*.  (단 이건 *비선형 운동학*이 잡아내고
>    *선형 탄성*은 못 잡는 효과.)
> 3. **무차원 설계 규칙: 𝒢 = 0.5·k_SE·(3β_AM·A_AM)²/(H·G_c) < 1000** 이면 elastic-brittle SE integrity 보존.
>
> ⚠ **우리 압밀과 *축이 다름*(절대 혼동 금지):** 이 논문 E_SE=15 GPa 는 **real 재료 모듈러스**(사이클 균열 입력)이고,
> 우리 E_eff=1.35(DEM)/1.53(MPM) 은 **압밀-bed 유효 모듈러스**(granular 럼핑 프록시).  "compliant SE 가 더 깨진다"(real-15)와
> 우리 "softened E_eff=1.35"(effective) 는 **다른 층위** — §우리-대비에서 정밀 구분.

---

## 1. 한 줄 요약
ASSB 복합전극에서 **전극입자(AM)의 *Li-삽입 유발 부피팽창*(Vegard strain)이 주변 *치밀한* SE 매질에 응력을 만들고, 그
응력이 SE 상(phase) *내부*에 micro-crack 을 만든다** — 이를 **fully-coupled electro-chemo-mechanical FEM**(전기·화학·역학
세 장 연성, Newton–Raphson) + **cohesive-zone model(CZM, intrinsic history-dependent, traction-separation)** 으로 *정량화*.
핵심 결론: **(a)** 균열은 **전극팽창 < 7.5 %** 이고 **SE fracture energy G_c ≥ 4 J/m²** 면 *방지*되며 (대부분 Li-삽입화합물이
< 7.5 % → 달성 가능); **(b) 반직관적으로 *compliant*(E_SE ~15 GPa) SE 가 *더* 취약** — 비선형 운동학(큰 변형 → 인장·전단)이
잡아내는 효과로, "sulfide(말랑) > oxide(딱딱) for bulk batteries" 라는 *speculation 을 반박*; **(c)** Li-전도체 안의 균열은
**Li-수송의 장벽 → rate performance(출력) 감쇠 가속**.  설계 규칙으로 **무차원수 𝒢 < 1000** 제시.

---

## 2. 메타
| 항목 | 값 |
|---|---|
| 저자 | **Giovanna Bucci**, **Tushar Swamy**, **Yet-Ming Chiang**, **W. Craig Carter\*** |
| 소속 | **Massachusetts Institute of Technology**, Dept. of Materials Science and Engineering, 77 Massachusetts Ave., Cambridge, MA 02139-4307, USA |
| 교신 | **W. Craig Carter** (ccarter@mit.edu — 본문 bucci@mit.edu 표기) |
| 저널/년 | **J. Mater. Chem. A, 2017, 5, 19422–19430** (Received 12 April 2017, Accepted 18 August 2017) |
| DOI | **10.1039/c7ta03199h** |
| 자금 | **DOE Office of Science, grant DE-SC0002633** (감사: Brian W. Sheldon, Frank McGrogan) |
| 연구유형 | **이론/시뮬레이션** — coupled electro-chemo-mechanical **FEM** (deal.II) + **CZM**(cohesive-zone fracture).  실험 없음 |
| 모델 시스템 | **복합 *음극*(negative electrode)** — AM 입자(delithiated 상태로 제조, *charge* 시 팽창) 가 **SE + 전자도전제 혼합 매질**에 박힘.  ⚠ Bucci 의 모델은 *negative electrode*(Si/Sn/Al/graphite 류 삽입음극)를 명시 — *cathode* 가 아님 (단 메커니즘=전극입자 팽창 vs SE → cathode 에도 일반화 가능) |
| AM (전극입자) | **Li-삽입 전극화합물**(특정 소재 미지정; Vegard 팽창 0–30 % 파라미터 스윕; 대표 baseline 3 %; "typical Li-intercalation < 7.5 %") |
| SE (고체전해질) | **bulk SE**(특정 소재 미지정 — *대표값* E_SE=15 GPa, G_c=1 J/m² baseline = **sulfide SE 대표값**); Table 1 에 LiPON/Perovskite/Garnet(LLZO)/Sulfide(Li₂S-P₂S₅)/Li₁₀GeP₂S₁₂ 모듈러스 *survey* |
| 도전제 | SE 와 혼합된 **전자도전제(carbon)** — "SE mixed with carbon"(Fig 1) → 매질을 *ionic+electronic 혼합도체*로 homogenize |
| 도메인 | **11 µm × 11 µm 정사각**(plane strain 2D), **36 randomly-oriented square 입자**, centroidal **Voronoi tessellation**, 평균 입경 **1 µm**, AM area ratio **~50 %**(=부피로딩 50–60 %) |
| 입자형상 | ★ **square(모서리 sharp)** — circle 보다 *현실적*이라 주장(Sakuda Fig 6 SEM + Harris LiCoO₂ 3D 재구성 근거); **flaw·응력이 sharp corner 에 집적** |
| 하중 | **galvanostatic** — separator 계면에 일정·균일 Li flux(=정전류 i=1 mA/cm²) → AM 입자가 *charge* 시 팽창; 시간 = SOC |
| FEM 라이브러리 | **deal.II**(linear quadrilateral, Newton–Raphson; ref 61,62) |
| 균열모델 | **CZM** — intrinsic history-dependent; flux across 균열면 = 균열개시 시 *비가역적으로 0*; pre-inserted cohesive elements (potential crack paths 따라, 입자 사이 + *입자 내부*); bilinear-ish traction-separation; Griffith(순간방출) 와 달리 **gradual** 방출 |

---

## 3. 핵심 물성 (수치)

> ⚠ 이 논문은 *압밀 porosity*·*상대밀도*·*coordination*·*coverage*·*Heckel*·*PSD*·*σ_ionic 절대값*·*σ_y(항복강도)*·
> *σ_thermal* 를 측정·보고하지 **않는다**(사이클-역학 시뮬 논문, AM 은 elastic, SE 도 elastic/diffusively-isotropic).
> 그 칸은 **n/a — 우리 압밀 앵커(Minnmann 14 %, Doux 18 %, 우리 15.6 %)와 *직접 비교 금지*.**  이 논문의 정량 앵커는
> **(i) 균열 임계: 팽창 7.5 % + G_c 4 J/m²**, **(ii) compliant-SE 취약(E_SE=15 GPa)**, **(iii) Table 1 SE 모듈러스 survey**,
> **(iv) FEM 입력 Table 2**, **(v) 무차원 𝒢 < 1000** 이다.

### 3.1 ★★ 균열 임계/방지 조건 (이 논문의 *심장*)
| 양 | 값 | src | 비고 |
|---|---|---|---|
| **균열 방지 ① AM 팽창 임계** | **ΔV ≤ 7.5 %** (volumetric) | stated | "fracture prevented when electrode-particle's expansion < 7.5 % (typical for most Li-intercalating compounds)" |
| **균열 방지 ② SE fracture energy** | **G_c ≥ 4 J/m²** | stated | "and the solid-electrolyte's fracture energy higher than G_c = 4 J m⁻²" — 두 조건 *동시* 만족 시 균열 억제 |
| baseline G_c (대표 sulfide) | **1.0 J/m²** | stated (Table 2, §3) | "representative value for a sulfide SE"; G_c 스윕 0.25–4.0 J/m² |
| **균열 개시 임계 (시뮬에서)** | 입자 부피 **3 % 변화** 시 | stated (§3) | baseline 시뮬은 ΔV=3 % 에서 균열 *시작*(= 많은 삽입화합물 거동) |
| 사이클 응력 = AM 팽창의 *기하 구속* | "stress-free strain ↑ → **compressive stress** 발생" | stated | 전체계가 구속 → AM 팽창이 대부분 *압축*, **sharp corner 근처에만 *인장/전단*** → 거기서 균열 핵생성 |
| **무차원 설계수** 𝒢 | **𝒢 = 0.5·k_SE·(3β_AM·A_AM)² / (H·G_c)** | stated (eq, §3) | k_SE=SE bulk modulus, β_AM=AM Vegard 파라미터(3β_AM=체적팽창율), H=전극두께, A_AM=AM 면적, G_c=SE fracture energy |
| **integrity 보존 규칙** | **𝒢 < 1000** | stated | "We predict the integrity of elastic-brittle solid-state electrolytes to be preserved when the condition 𝒢 < 1000 is met" |
> ★★ **읽는 법:** AM 팽창(β_AM)·SE 강성(k_SE)이 *클수록*, G_c·두께(H)가 *작을수록* 𝒢↑ → 균열↑.  팽창이 2× 되면
> elastic 에너지 4× (∝ 팽창²) → 균열 열기 위한 fracture energy 도 4× 커야 동률 → **𝒢 가 "저장된 탄성에너지 / 파괴에너지"
> 비율**.  두 곡선(Fig 5 의 case a/b)이 *같은 𝒢* 면 같은 균열거동 → 𝒢 로 결과를 일반화.

### 3.2 ★★ Table 1 — SE 재료 Young's modulus + fracture toughness *survey* (이 논문의 literature 앵커)
> ★ 이 표가 **"sulfide SE 가 *말랑*하다(14–25 GPa) → bulk 전지에 유리하다는 *speculation* 의 출처"** 이고, 본문이 그
> speculation 을 *반박*.  ★ 우리 E_SE 앵커 corpus 와 *교차*: 우리 real-bulk ~24, Sakuda 24, Bazzoun/Kang/Kim 22.1.
> 이 표의 **sulfide 14–25 GPa = Sakuda 18–25 와 일치**(같은 Li₂S-P₂S₅).  ⚠ **단 baseline 에 쓴 E_SE=15 GPa 는 그 *하단*** —
> "compliant SE" 라벨이 거기서 옴.

| 분류 | 화합물 | 처리 | **Young's modulus** | Fracture toughness K_IC | 시험법 | σ_ion (RT) | ref |
|---|---|---|---|---|---|---|---|
| LiPON | Li₃PO₄Nₓ | amorphous LiPON 스퍼터막 | **77 GPa** | — | nanoindentation | 2×10⁻⁶ S/cm | 12 |
| Perovskite | Li₀.₃₃La₀.₅₇TiO₃ (solid state) | — | **186 ± 4 GPa** | 0.890–1.34 MPa·m^0.5 | nanoindentation | bulk ~10⁻³ | 13 |
| Perovskite | Li₀.₃₃La₀.₅₇TiO₃ (sol-gel) | — | **200 ± 3 GPa** | 0.890–1.31 MPa·m^0.5 | nanoindentation | total ~10⁻⁵ | 13 |
| **Garnet** | Li₆.₂₄La₃Zr₂Al₀.₂₄O₁₁.₉₈ (**LLZO**) | hot-pressed | **150 GPa** (porosity 0.03 → 132.5 GPa @porosity 0.06) | — | resonant ultrasound | ~0.2×10⁻³ | 14 |
| Garnet | cubic Li₇La₃Zr₂O₁₂ | rel.density ~99 % | **150 GPa** | — | resonant ultrasound | 3×10⁻⁴ | 14 |
| **Sulfide** | **Li₂S–P₂S₅ (hot-pressed)** | sinter 360 MPa, 20–190 °C | **★ 18–25 GPa** | — | ultrasound velocity + compression | 3×10⁻⁴ (조밀재) | 15 |
| Sulfide | Li₂S–P₂S₅ (cold-pressed) | sinter 180–360 MPa, RT | **★ 14–17 GPa** | — | (위와 동) | | 15 |
| Sulfide | Li₆PS₅ (= **argyrodite류**) | — | **18.5 ± 0.9 GPa** | 0.23 ± 0.04 MPa·m^0.5 | nanoindentation | | 16 |
| Sulfide | **Li₁₀GeP₂S₁₂ (LGPS)** | — | **37.19 GPa** | — | atomistic simulation | 1.2×10⁻² S/cm | 17 |
> ★ **핵심 narrative(본문):** "sulfide SEs tend to be much more *compliant* than oxide electrolytes. The Young's modulus
> of Li₂S–P₂S₅ sulfide SEs has been estimated to be in the range of **14–25 GPa**. Such a low stiffness has been regarded
> as *favorable* for the design of bulk-type batteries. **However, we show that compliant solid electrolytes (E_SE ~15 GPa)
> are more prone to micro-cracking.**"  → Table 1 의 sulfide 하단(14 GPa)·argyrodite(18.5)가 우리 LPSCl 계열, oxide(LLZO
> 150, perovskite 186–200)는 *딱딱한* 대조군.

### 3.3 FEM 입력 (Table 2 — Section 2 문제) ★ 우리 MPM/FEM 이 미러할 값
| 입력 | 값 | 설명 |
|---|---|---|
| F | 96 485.3365 C/mol | Faraday 상수 |
| R | 8.314 J/K/mol | 기체 상수 |
| T | **298 K** | 온도 |
| M_el | **10⁻¹⁵ m²/s** | AM(전극재) 내 Li 이동도 |
| M_SE | **10⁻¹³ m²/s** | SE 내 Li 이동도 (★ SE 가 AM 보다 100× 빠른 Li 수송) |
| c_max,AM | 1 | AM 화합물 mol 당 Li 최대 상대몰수 |
| c_max,SE | 0.25 | SE mol 당 Li 최대 상대몰수 |
| i | **10 A/m²** (= 1 mA/cm²) | separator 계면 정전류밀도 (commercial Li-ion 대표) |
| γ_Li | 1 | activity coefficient |
| **ν (Poisson)** | **0.3** (두 재료 *공통*) | ★ Poisson's ratio for *both* materials |
| **β_AM** | **0.1** | AM 내 Li 의 relative lattice constant (Vegard 파라미터) |
| **β_SE** | **0** | ★ SE 는 Vegard strain *zero*(팽창 안 함) — SE 응력은 *순전히* AM 팽창의 구속에서 옴 |
| **E_AM** | **100 GPa** | ★ AM(전극재) Young's modulus |
| **E_SE** | **15 GPa** | ★★ SE Young's modulus (baseline = **compliant sulfide 대표**) |
| **G_c** | **1.0 J/m²** | bulk SE fracture energy (baseline) |
| **δ₀** | **5 nm** | 손상 개시 opening displacement |
| **δ_cr** | **20·δ₀ = 100 nm** | 완전 계면분리(complete separation) critical opening |
> ★ E_AM/E_SE = **100/15 ≈ 6.7×** — AM 이 SE 보다 훨씬 딱딱.  **β_SE=0** 이 결정적: SE 는 스스로 안 팽창,
> *AM 팽창을 구속*하며 응력 받음 → "compliant SE 가 변형으로 흡수 못 하면 인장 쌓여 균열".

### 3.4 균열-vs-모듈러스 / 균열-vs-G_c / 균열-vs-팽창 (Fig 3–5, 정성+상대)
| 관계 | 거동 | src | 비고 |
|---|---|---|---|
| **G_c ↑ → 균열전파속도 ↓** | G_c 0.25→4.0 J/m² 스윕: G_c↓ 일수록 stage-b 전파율(곡선 기울기)↑, 균열핵생성 빠름 | Fig 3 stated | 모든 case 가 *안정* 전파(급격파괴 아님); plateau=성장포화 |
| **E_SE ↓(compliant) → 균열전파속도 ↑** | E_AM/E_SE = 100/15·100/25·100/50·100/150 스윕: **E_SE 작을수록 더 빨리·더 많이 균열** | Fig 4 stated | ★★ 반직관 핵심; E_SE=150(garnet급)이 가장 안 깨짐 |
| **AM 팽창 ↑ → 균열 ↑** | ΔV 7.5/15/30 % 스윕 | Fig 5 stated | ΔV<7.5 % + G_c≥4 면 균열 *억제* |
| **균열 후 σ_Mises** | 압축 < 200 MPa(대부분), sharp corner 근처만 인장 | Fig 2 stated | "compressive stress in electrolyte within linear elastic range 0–200 MPa, similar to Sakuda" |
| **응력 범위(AM 입자)** | charge 진행 시 입자 압력 **> 1 GPa**(50 % 용량 저장 입자) | Fig 2c stated | AM 응력은 GPa, SE 응력은 ~수백 MPa |
| 3-stage 균열성장 | (a) 핵생성 지연 → (b) ~일정 전파율 → (c) 감속·포화 | Fig 3 stated | 모든 곡선 공통 패턴 |

### 3.5 미측정/n/a (우리 압밀·전달 앵커와 직접대조 금지)
| 항목 | 상태 |
|---|---|
| porosity / 상대밀도 / coordination Z / coverage | **n/a** (사이클-역학 시뮬, 미측정·압밀 모델 아님) |
| Heckel / P_y / 압밀곡선 | **n/a** |
| **σ_y(항복강도) / 소성경화** | **n/a** — ★ **AM·SE 둘 다 *linear elastic* 가정**(SE 는 elastic + diffusively-isotropic; AM 도 linear elastic) → 우리 MPM J2 *소성*·우리 DEM hooke/hysteresis 와 **구성식 자체가 다름**(elastic-brittle vs ductile-plastic) |
| PSD (D10/D50/D90) | **n/a** (평균 1 µm, square 입자, Voronoi — 분포는 tessellation) |
| σ_ionic / σ_e / σ_thermal **절대값** | **n/a** (M_el/M_SE 이동도 *입력*만; σ_eff 를 풀지 *않음* — 균열이 Li-flux 를 *끊는* 효과만 정성 언급) |
| 압밀 압력(MPa) | **n/a** — ★ 하중이 *Li flux(정전류)* 지 *기계 가압* 아님 (Table 1 sulfide 처리압 180–360 MPa 는 *문헌 인용*) |

---

## 4. 시뮬레이션 방법 ★ — coupled electro-chemo-mechanical FEM + cohesive-zone CZM

> ★ 이 논문은 **하중이 *기계 가압*이 아니라 *Li 삽입(정전류)*** 이고, **AM 입자가 *팽창*하며 SE 를 깨는** 모델 —
> 즉 ***사이클* 역학**이다 (우리 *압밀* 역학과 시간축이 다름).  세 물리장(전기 φ / 화학 c-diffusion / 역학 u)을 *fully
> coupled* Newton–Raphson 으로 동시에 풀고, **SE 상 내부 균열을 cohesive-zone(CZM)** 으로 추적.  DEM/MPM 은 없다(연속체 FEM).
> ⇒ frame[5]: 그들 FEM = *사이클 중 SE 취성균열*(우리 미보유 시간축 + 취성 메커니즘); 우리 = *제조-순간 압밀 구조→수송 σ*
> (DEM) + *압밀 소성 morphology*(MPM, 연성).

### 4.1 ★ 지배방정식 — coupled electro-chemo-mechanical (Bucci et al. 2016 Acta Mater. 62, 33; ref 10)
**세 미지장:** displacement **u**, Li concentration **c**, diffusion potential **φ**(전기화학 퍼텐셜).  각 time step 에서
Newton–Raphson 으로 세 방정식 동시해 (전기·화학·역학 장 coupling).

- **(역학) 평형 + 비선형 운동학:** "The *nonlinear formulation* of the mechanical equilibrium quantifies the difference
  in deformation/stress associated with varying SE stiffness. A *linear model* would predict that stress scales with E_SE
  and would *not* capture the microstructural effects." → ★ **비선형(large-strain) 운동학이 핵심** — *선형 탄성*은 compliant-
  SE 효과(stretching/shearing)를 못 잡음.  AM·SE 둘 다 **linear elastic constitutive**(σ=C:ε^e), 단 *기하*는 비선형.
- **(화학 = Vegard/확산유발 strain):** AM 의 **stress-free(eigen) strain = β_AM·Δc** (Vegard's law / "Vegard's stress"),
  열변형과 유추.  SE 는 **β_SE=0**(팽창 없음).  → AM 이 charge 시 부풀고 SE 가 그것을 *구속* → 응력.
  - AM 부피팽창율 = **3β_AM·Δc**(체적); baseline β_AM=0.1, full charge Δc=1 → ΔV≈3·0.1·…(스윕 3–30 %).
- **(확산) Li flux:** `J = −M·c·∇φ` 류(이동도 M_el/M_SE), 매질을 **homogenized ionic+electronic 혼합도체**로(SE+carbon).
  separator 계면(Fig 1 top)에 **정전류(균일 flux)** Dirichlet, 나머지 변=zero flux.
- **(역학 BC):** 좌·우변 **zero horizontal displacement**(roller); top 변=SE 존재로 vertical 구속; bottom=packaging/이웃셀
  구속.  → "AM 부피변화는 SE 매질 변형으로 수용"(Harris graphite DIC 관찰과 유사: graphite 전극 평균 strain 0.2 %,
  화학팽창의 1/10 — 대부분 porosity 감소로 흡수).

### 4.2 ★ CZM — cohesive-zone 균열모델 (intrinsic, history-dependent; ref 11 Bucci-Carter Springer 2016)
- **intrinsic 접근:** **cohesive elements 를 잠재적 균열경로(입자 사이 + *입자 내부* 일부 interface)에 *미리* 삽입** →
  균열은 그 subset interface 만 따라 전파.  *extrinsic*(균열기준 충족 시 *그때* 삽입)은 mesh topology 변경 필요·병렬
  부적합 → intrinsic 채택("high-shear 영역의 CZ 배치는 두 접근이 다르지 않다" 가정).
- **history-dependent flux 차단:** ★ **flux across the interface is *irreversibly set to zero* at the onset of fracture**
  → **균열이 Li-수송을 *영구* 차단**(= rate performance 감쇠의 모델 메커니즘).  CZM 이 *fracture 가 Li-flux 에 주는 악영향*을
  계정에 넣음(Woodford-Chiang-Carter electrochemical-shock; ref 18).
- **gradual energy release(≠ Griffith):** "CZM differs from the Griffith model wherein energy is released *instantaneously*.
  The gradual release presumes some cohesion between separating flanks. Traction decays with increasing separation until it
  vanishes at a critical opening displacement." → **traction-separation: δ₀=5 nm 손상개시 → δ_cr=20·δ₀=100 nm 완전분리**.
  **G_c = traction-separation 곡선의 적분 = 모델 파라미터**.
- **결정적 통제:** "cracking is *prevented* in those cases for which **G_c ≥ 4 J/m²** AND total volumetric expansion
  **ΔV ≤ 7.5 %**. In all other cases the model predicts some extension of mechanical degradation."
- ⚠ **shortcoming(저자 명시):** 낮은 G_c 에서 stage-c 가 *pre-inserted* crack-path 가용성에 *bias* 될 수 있음("even if
  about 10 % of the pre-inserted cohesive interfaces remain unfractured") → intrinsic CZM 의 한계.

### 4.3 ★ 무차원 설계 규칙 도출 (Fig 5 → 𝒢)
입자팽창이 2× 면 SE 에 저장된 탄성에너지 4× (∝ 팽창²·k_SE), 균열 열 fracture energy 도 4× 면 *전파율 동일* → 두 효과를
한 무차원수로:
- **𝒢 = 0.5·k_SE·(3β_AM·A_AM)² / (H·G_c)**  (k_SE=SE bulk modulus, 3β_AM=AM 체적팽창율, A_AM=AM 면적, H=전극두께)
- Fig 5 의 두 case(30 % 팽창·G_c=1.0 / 7.5 % 팽창·G_c=0.25, 또는 15 %·1.0 / 7.5 %·0.25)가 *같은 𝒢* → *겹치는 균열곡선*
  → **𝒢 로 결과 일반화** → **𝒢 < 1000 이면 integrity 보존** (elastic-brittle SE).

### 4.4 입자 처리 ★ (DEM판 "무질서 처리" 관점)
- **AM·SE 둘 다 *연속체 linear-elastic*** (SE = elastic + diffusively isotropic; β_SE=0).  ★ **입자 *형상*은 변형
  안 함**(rigid-elastic, 작은 변형) — **SE 상은 *cohesive-zone 으로 *갈라짐*(취성 균열·박리)**.  ⇒ **우리 MPM 의 *연성 J2
  소성 형상흐름(void-fill)*과 *정반대* 파괴양식**: 그들=**취성 cohesive 균열**, 우리=**연성 소성 흐름**.
  ★ 우리 DEM 의 **Auerbach(AM-AM 접촉응력→AM 균열)**과도 위치 다름: 그들 균열=*SE 상*, 우리 Auerbach=*AM 입자*.
- **square 입자(sharp corner)** 채택 = circle 보다 *현실적*(Sakuda Fig 6 SEM, Harris LiCoO₂ 3D) — flaw·응력이 모서리에
  집적 → 입자 misalignment 가 matrix 전단·인장 만듦.  **mono-size ~1 µm(Voronoi tessellation)**, 36 입자.
- ⇒ ★ **우리 DEM(구·접촉망)·MPM(소성 형상)의 *명시적 입자-단위 미세구조*가 이 논문엔 *없다*** — Voronoi 연속체(square 셀)
  + cohesive GB.  frame[5]: 우리 = 구조→σ + 압밀 소성; 그들 = 사이클 SE 취성균열역학.

### 4.5 도메인 / 하중 / seeds
- **11 µm × 11 µm**, plane-strain 2D(thin-plate-in-thick-sample 가정; "2D model expected to correctly capture trends in
  stress and fracture" — 3D 풀 해석은 계산비용으로 보류); **36 square Voronoi 입자**, ⟨d⟩=1 µm, AM area ~50 %(=vol loading
  50–60 %).  단일 실현(lithiation degree/SOC 스윕).  deal.II linear quad, Newton–Raphson.
- **하중 = galvanostatic** i=1 mA/cm²(=10 A/m²) at separator → SOC 시간진행.  ★ **압밀 가압 *아님*** (이 점이 우리와
  근본 다름 — 우리 압밀은 300 MPa 외부 가압, 이 논문은 *내부* Li-팽창 응력).

---

## 5. 결과 상세 — Section-by-section (모든 수치)

### 5.1 §1 Introduction — 문제 제기 + frame[5] 위치
- ASSB 의 두 도전: **제조(manufacturing) + 신뢰성(reliability)**.  복합전극에서 **SE 가 (i) AM binding (ii) Li⁺ 경로**
  둘 다 담당 → **SE 내 micro-crack 이 *유효 이온전도도 감소*** 예상.  **저-porosity 시스템은 삽입변형 수용 못 하면 더
  역학손상 취약**(= 우리 압밀-porosity 논의와 *맞닿되* 그들은 *사이클*).  micro-crack 이 **Li dendrite 성장 경로 → 단락**
  (Porz et al. ref 9: dendrite 가 *조밀* ceramic SE 도 표면 flaw 따라 침투).
- "operation 중 micro-crack 형성 여부 예측이 cell shorting 방지에 critical" → **fully coupled electro-chemo-mechanical
  model + CZM** 채택.  Treatment of microstructural details + local variability(ref 10) → stress localization 연구.
- ★ **선행연구 위치:** Vegard-stress 의 AM 역학파괴는 많이 봤으나(ref 18–51), **fully coupled electro-mechanical 로 단순
  전극 미세구조 균열 모사한 건 Bower–Guduru(ref 20)뿐** → **"ours is the *first* model to *quantitatively* assess
  mechanical reliability of ASSBs, and predict fracture extension caused by electrochemical cycling"**(저자 주장).
- ★ **SE 역학물성 데이터 빈약** → Table 1 survey: **sulfide(14–25 GPa) ≪ oxide(150–200 GPa)** = compliant.  "low stiffness
  regarded as *favorable* for bulk batteries(ref 52 Sakuda) — **그러나 우리는 compliant SE 가 더 깨진다 보임**".
- **계면층(SEI/interphase) 논의:** SE-전극 계면반응층(Zhu ref 53, Wenzel ref 55 Li₇P₃S₁₁ SEI 2–3 nm)·thick interphase
  가 charge-transfer kinetics 저하; 본 연구는 **"perfectly coherent/stable interface"** 가정(범위 한정).

### 5.2 §2 Methods — 모델 정식화 (§4 전체)
- coupled electro-chemo-mechanical FEM(§4.1) + intrinsic CZM(§4.2).  homogenized ionic+electronic 매질, square Voronoi
  입자, Table 2 입력.  **AM 은 음극(delithiated 제조 → charge 시 팽창)**; SE β=0.

### 5.3 §3 Results — baseline + 스윕
- **baseline:** E_SE=15 GPa, G_c=1.0 J/m²(sulfide 대표); 팽창은 **full charge 시 최대 30 %**까지 허용(스윕)하되 baseline
  균열개시는 **ΔV=3 %**(많은 삽입화합물 거동).
- **Fig 2 (SOC 진행 3 스냅샷):** t=150 s(SOC 0.116) / 400 s(0.168) / 900 s(0.273).  **좌=Li 농도, 우=hydrostatic Cauchy
  응력.** charge↑ → AM 화학팽창 → **대부분 *압축*** 발생(전체 구속); **입자 *모서리* 근처에만 *인장*(rust-colored)** →
  거기서 **균열(검은 선) 핵생성·전파**(corner-to-corner, Li 확산경로 절단).  Fig 2c: AM 입자압력 **>1 GPa**(50 % 용량 입자);
  SE 압축응력은 **0–200 MPa 선형탄성 범위**(Sakuda 측정과 일치).
- **Fig 3 (G_c 스윕 0.25–4.0 J/m², 균열길이/두께 vs 시간):** 5 곡선; **3-stage**(핵생성 지연→일정전파→감속포화);
  **G_c↓ → 전파율↑·핵생성 빠름**; G_c≥4 J/m² 면 ΔV=30 % 에서도 균열 *억제* 가능 영역.  plateau=성장포화.  ⚠ 낮은 G_c 에서
  stage-c 가 pre-inserted path 가용성에 bias.
- **Fig 4 (E_SE 스윕, 균열/두께 vs 평균 SOC):** E_AM/E_SE = 100/15·100/25·100/50·100/150 GPa.  ★★ **E_SE↑(stiffer) →
  균열전파속도↓**(stiffer SE 가 화학팽창을 *덜* 흡수·덜 stretch → 인장·전단 덜 → 균열↓); **E_SE=150(garnet급)이 최저
  균열**.  "stiffer SE tends to *contain* the chemical expansion ... lower velocity of fracture propagation."  E_SE≈E_AM
  (100/100) 이면 압축응력 높아지나 변형 적음 — **선형탄성 관점엔 반직관**, 비선형에선 큰 변위가 인장·전단 만듦(특히 compliant).
- **Fig 5 (Vegard×G_c 조합, 𝒢 일반화):** 두 곡선 쌍(a: 30 %·G_c=1.0 / 7.5 %·G_c=0.25; b: 15 %·1.0 / 7.5 %·0.25)이
  *겹침* → **같은 𝒢 → 같은 균열거동** → 𝒢 로 일반화(§4.3).  **균열 억제 조건 = ΔV<7.5 % + G_c≥4 J/m²**(대부분 산화물
  삽입재 ΔV<7.5 %).
- ★ **fracture toughness↔G_c 환산(본문):** McGrogan(ref 16) nanoindentation **K_IC=0.23±0.04 MPa·m^0.5** (glassy Li₂S-P₂S₅,
  E_SE=18.5±0.9 GPa) → **G_c=K_IC²/E ≈ 2.8±1.8 J/m²** ("the only experimental fracture-toughness data for sulfide SE").
  → baseline G_c=1.0 은 이 범위 하단, 균열-억제 임계 4 J/m² 는 상단 근처.

### 5.4 §4 Conclusions (저자 요약)
- electro-chemo-mechanical FEM + CZM 이 ASSB 복합전극 *손상 개시·전파* 포착.  **균열 방지 = AM 팽창 < 7.5 % + G_c > 4 J/m²**
  (E_SE=15 GPa 가정 하) → **G_c 기반 SE 선택 제약**; 대부분 삽입 *산화물* 양극재 ΔV<7.5 %.
- poly-crystal Vegard 는 *비등방* 가능(graphite); 입자+SE 가 만드는 *미세구조*(입자형상·근접·misalignment)가 균열 결정.
- ★ **반직관:** "compliant SEs (E_SE ~15 GPa) are *more* prone to micro-cracking ... contradicts the speculation that
  sulfide SEs are more suitable than oxide for bulk-type batteries"(ref 52).  비선형 운동학 모델이라야 잡는 효과.
- ★ **출력 영향:** "Fracture in solid Li-ion conductors represents a *barrier* for Li transport, and accelerates the
  decay of rate performance." → 균열 = 이온수송 장벽 → power-density 감쇠.
- **설계 규칙:** **𝒢 = 0.5·k_SE·(3β_AM·A_AM)²/(H·G_c) < 1000** → elastic-brittle SE integrity 보존.

---

## 6. Figure / Table set ★ (모든 그림·표 + 우리가 쓸 점)

### 6.1 본문 Figures
| Fig | 내용 (무엇을 보여주나) | 핵심 수치 | 우리가 참고할 점 |
|---|---|---|---|
| **1** | FEM 기하/이산화/BC (복합 negative electrode: AM square 입자 in SE+carbon 매질; Li flux top; plane-strain 2D + 3D 모식) | 11×11 µm, 36 입자, ⟨d⟩=1 µm, AM ~50 % | ★ "SE mixed with carbon"=혼합도체 homogenize; square 입자 |
| **2a–c** | SOC 진행 3 스냅샷 — 좌 Li 농도 / 우 hydrostatic 응력; 균열(검은선) corner-to-corner | SOC 0.116/0.168/0.273; AM>1 GPa; SE 0–200 MPa | ★★ **압축 대부분 + 모서리만 인장→균열**; Li 경로 절단 |
| **3** | G_c 스윕(0.25–4.0 J/m²) 균열길이/두께 vs 시간 | 3-stage; G_c↓→전파↑ | ★ G_c≥4 면 억제; tougher=지연 |
| **4** | **E_SE 스윕**(E_AM/E_SE=100/15·25·50·150) 균열 vs SOC | ★★ E_SE↓→균열↑ | ★★ **반직관 핵심 — compliant SE 더 깨짐** |
| **5** | Vegard×G_c 조합 → 𝒢 일반화 (두 곡선쌍 겹침) | ΔV<7.5 %+G_c≥4=억제; 𝒢<1000 | ★ 무차원 설계수 |

### 6.2 Tables
| 항목 | 내용 | 우리가 참고할 점 |
|---|---|---|
| **Table 1** | **SE 재료 Young's modulus + K_IC + σ_ion survey** (LiPON 77 / Perovskite 186–200 / Garnet-LLZO 150 / **Sulfide 14–25** / Argyrodite 18.5 / LGPS 37.19 GPa) | ★★ **우리 E_SE 앵커 corpus 교차**(sulfide 14–25=Sakuda 18–25; argyrodite 18.5=우리 LPSCl 계열); "compliant=favorable" speculation 의 출처 |
| **Table 2** | **FEM 입력**(F/R/T, M_el 10⁻¹⁵/M_SE 10⁻¹³, c_max, i=10 A/m², ν=0.3, β_AM=0.1/β_SE=0, **E_AM=100/E_SE=15**, **G_c=1.0**, δ₀=5 nm/δ_cr=100 nm) | ★ 우리 cycling-MPM 이 미러할 입력셋; β_SE=0(SE 안 팽창)·δ₀/δ_cr cohesive 길이 |

> ⚠ **이 논문엔 SI(supplementary) 별도 표/그림이 본문에 노출 안 됨** — Table 1·2 + Fig 1–5 가 전부(reference 64개).
> Bucci 2016 Acta Mater.(ref 10, 지배방정식) + Bucci-Carter 2016 Springer(ref 11, CZM) 가 방법 원전.

---

## 7. Post-processing ★
- **무엇:**
  - **coupled electro-chemo-mechanical FEM**(deal.II, Newton–Raphson) → 세 장(u/c/φ) 동시해; AM Vegard eigenstrain
    β_AM·Δc → SE 응력장(hydrostatic Cauchy).
  - **cohesive-zone(CZM) 균열전파** → pre-inserted cohesive elements(traction-separation: δ₀=5 nm 개시 → δ_cr=100 nm
    완전분리; G_c=적분); history-dependent flux 차단(균열 시 비가역 0) → **균열길이/전극두께 vs SOC/시간** 곡선.
  - **K_IC → G_c 환산**: G_c = K_IC²/E (McGrogan 0.23 MPa·m^0.5 → ~2.8 J/m²).
  - **무차원수 𝒢 = 0.5·k_SE·(3β_AM·A_AM)²/(H·G_c)** 로 (Vegard×G_c×k_SE×H) 결과를 *한 곡선*으로 collapse → 설계규칙 𝒢<1000.
- **도구:** **deal.II**(FEM, ref 61–62; linear quad); cohesive-zone 자체구현(ref 11 Bucci-Carter Springer 2016
  "Mechanics of Materials. Micromechanics in electrochemical systems"); galvanostatic time-stepping.
- **수치화·기록:** baseline(E_SE=15, G_c=1.0) + 3 스윕(G_c 0.25–4.0 / E_SE via E_AM/E_SE 100/15–150 / ΔV 7.5–30 %) →
  균열길이/두께 vs 시간·SOC 곡선; 𝒢 collapse 로 일반화.

---

## 우리 DEM+MPM 대비 (comparison vs ours)
> ★ **이 절이 사용자 MANDATORY A.**  이 논문 = *사이클* chemo-mechanical CZM 파괴 vs 우리 *압밀* 파괴.  **driver·시간축·
> 메커니즘·구성식이 모두 다름** — "진짜 차이" vs "method-artifact" 를 명시 구분.

### 7.1 핵심 대비표
| 항목 | 이 논문 (Bucci 2017) | 우리 DEM+MPM | 차이 / 이유 (진짜 차이 vs artifact) |
|---|---|---|---|
| **파괴 시간축** | **사이클(operation) 중** — Li 삽입 팽창 | **압밀(제조) 중** — 외부 300 MPa 가압 | ★ **진짜 다른 축** (frame[5] 시간축).  우리 Auerbach/Lawn = *제조-시점* 접촉응력; 그들 = *사이클-시점* Vegard 응력 |
| **파괴 driver(하중)** | **AM 팽창의 *기하 구속*** (β_AM·Δc → SE 인장; 압밀 가압 *아님*) | **AM-AM *접촉응력*** (가압 → Hertz 접촉력) | ★ 진짜 다름.  같은 "균열"이나 *원인*이 다름 (intercalation vs compaction) |
| **균열 *위치*** | **SE 상(phase) 내부 + GB**(cohesive-zone) | **AM 입자**(Auerbach P_c, fracture-aware Holm) | ★ **반대 상** — 그들=SE 깨짐(우리 *전혀* 미보유), 우리=AM 깨짐 |
| **파괴 *모델*** | **cohesive-zone CZM**(traction-separation, 결정론적 균열경로, history flux-차단) | **Auerbach 통계 임계응력**(P_c, 파편확률) + Lawn 1998 multiplier | ★ 방법 다름 (결정론 균열추적 vs 통계 임계) |
| **구성식** | **AM·SE 둘 다 *linear elastic*** + 비선형 *기하* + **SE 취성 cohesive 균열** | DEM=hooke/hysteresis(elastic 럼핑); MPM=**von Mises J2 *연성 소성***(void-fill 흐름) | ★★ **근본 다름** — 그들 = *취성*(brittle cohesive); 우리 MPM = *연성*(ductile plastic).  **우리 MPM J2 는 SE *취성균열* 불가**(D6 공백) |
| **모듈러스 층위** | **E_SE=15 GPa = *real 재료* 모듈러스**(사이클 균열 입력) | **E_eff=1.35(DEM)/1.53(MPM) = *압밀-bed 유효* 프록시**(granular 럼핑) | ⚠ **다른 층위 — 절대 혼동 금지**(§7.3 상세) |
| **AM 모듈러스** | E_AM=100 GPa | NMC811 가정 140(또는 Kang NCA 175) | 소재·층위 다름 |
| **전달 σ** | *안 풂*(이동도 입력만; 균열→flux 차단 *정성*) | σ_ionic+σ_e+σ_thermal *명시 솔버*(Kirchhoff/Holm) | ★ **우리 우위** — 그들은 σ_eff 미산출(우리 frame[5] 전달 절반 소유) |
| **차원/규모** | 2D plane-strain, 11×11 µm, 36 입자 | DEM/MPM 2D+3D, real 12:4:1 PSD | 2D≠3D 절대규모 주의 |

### 7.2 ★★ "compliant SE 가 더 깨진다(real-15 GPa)" vs 우리 "softened E_eff=1.35" — *tension 인가?* (사용자 핵심 질문)
**답: tension 아님 — 서로 다른 *축*의 진술이라 직접 비교 불가.  conflate 하면 *오독*.**
- **Bucci 의 E_SE=15 GPa** = **real 재료 모듈러스**(Table 1 sulfide 14–25 의 하단), **사이클 중 SE 가 AM 팽창을 흡수/저항하는
  *탄성 강성***.  그의 결론 = "real-stiffness *낮은*(compliant) SE 일수록 *큰 변위* → 인장·전단 → *SE 균열* 많음"(Fig 4).
  → **변수 = SE 의 *재료* 강성**, 결과 = ***사이클 SE 취성균열* 양**.
- **우리 E_eff=1.35 GPa** = **압밀-bed *유효* 모듈러스** — real 24 GPa 를 **18× 연화**한 *프록시*(granular 재배열/GB-slide/
  micro-fracture 럼핑).  변수 = **압밀 *역학*을 맞추는 유효값**, 결과 = ***제조-시점 porosity*** (사이클 균열 *아님*).
- ⇒ **두 축이 직교:** Bucci 는 *real E_SE 를 바꿔* *사이클 균열*을 보고, 우리는 *유효 E_eff 를 골라* *압밀 porosity*를 맞춘다.
  **"compliant 가 더 깨진다"는 우리 1.35 와 무관**(우리 1.35 는 *압밀*용, 그의 15 는 *사이클*용; 우리 *real* 칸은 24,
  그의 15 와 *같은 sulfide 범위*).
- ★ **그래도 *간접* 시사점 2개(주의해서):**
  1. **우리 *real* E_SE(24)·Sakuda(18–25)·이 논문 Table 1 sulfide(14–25)·argyrodite(18.5)가 *일치*** → 우리 E_SE 앵커
     corpus 의 *4번째* 외부 확인(같은 Li₂S-P₂S₅ 계열).  단 이 논문 baseline 15 는 그 *하단* — 우리 24 보다 *말랑*(소재
     subset 차이; LPSCl argyrodite 18.5 가 우리에 더 가까움).
  2. **만약 우리가 *사이클-MPM*(미래)을 만든다면 *real* E_SE(24, *not* 1.35)를 써야** — Bucci 의 균열물리는 real 강성에
     걸려 있으므로, *압밀용 1.35* 를 사이클-균열에 쓰면 안 됨(층위 혼동).  (우리 MPM 압밀에서도 *bulk* 는 ν=0.49 로 real-24
     로 끌어올렸음 = 같은 교훈: 압밀-shear 만 연화, bulk·사이클은 real.)
- ⚠ **conflate 금지 한 줄:** "우리 1.35 가 Bucci 15 보다 *더 compliant* 니 우리가 *더* 깨지겠다" = **틀림**(층위 다름;
  우리 1.35 는 사이클 균열 입력이 아니고, 우리 DEM 은 SE 균열을 *아예* 모델 안 함).

### 7.3 frame[4]/[5] 정직 정리
- **frame[4](cross-fit 금지):** 이 논문은 우리와 *교차검증* 대상이 아니라 **frame[5] 시간축 *보완*** — DEM/MPM 을 여기에
  맞출 일 없음(둘 다 experiment 에 독립 calibrate).  단 **Table 1·G_c·7.5 % 는 *literature 값* → 인용/채택 가능**(우리가
  사이클-MPM 만들 때 입력).
- **frame[5](분업):** **압밀 파괴 = 우리(Auerbach/Lawn, DEM)**; **사이클 *취성* SE 파괴 = Bucci CZM(우리 미보유)**;
  **우리 MPM J2 = 연성 only**(SE 취성 불가).  → 이 논문은 **DEM 경쟁자 *아님*** — "novelty" framing 은 *우리가 소유한 것*
  (압밀 transport+packing+morphology) vs *그들이 소유한 것*(사이클 SE 취성균열)의 *분업*.

---

## 적용가능성 (applicability to our model)
> ★ **사용자 MANDATORY B.**  구체적으로 *어디에* 쓰나 — backlog **A10 / B6 / D6** 의 literature 레퍼런스.

### 8.1 backlog 매핑 (즉시)
| backlog | 항목 | 이 논문이 주는 것 | 적용 방법 |
|---|---|---|---|
| **A10** | 사이클 chemo-mechanics (future frame[5] 시간축) | ★ **방법 *원형*** — coupled electro-chemo-mechanical FEM + CZM (Kang 2025 와 *같은* CZM 계열; Bucci 가 *최초/원전*) | 우리 future *cycling-MPM/FEM* 의 정식화 템플릿: Vegard eigenstrain ε=β·Δc + cohesive 균열 + flux-차단.  Kang(NCA 입자균열)+Bucci(SE 균열) 둘 다 참고 |
| **B6** | operating-pressure σ-degradation (시간축) | ★ **균열→Li-flux 차단→rate 감쇠** 메커니즘 | 우리 정적 σ 에 *사이클* 시간축 추가 시 "균열 interface flux=0"(history-dependent) 채택; Kang R_w∝δ_s 시그니처와 결합 |
| **D6** | SE 취성균열 (frame[5] 공백) | ★ **G_c=2.8±1.8 J/m²(McGrogan sulfide)·7.5 % 임계·𝒢<1000** | de Vaucorbeil continuous-damage/cohesive MPM 으로 SE 취성 추가 시 *G_c 입력값* + *검증 임계*; 우리 J2(ductile)에 *별도 brittle-damage* 변수 필요 |

### 8.2 ★ 직접 채택 가능한 *literature 값*(우리가 인용/입력)
| 값 | 출처(이 논문) | 우리 용도 |
|---|---|---|
| **G_c(sulfide) = 2.8 ± 1.8 J/m²** | McGrogan K_IC=0.23 MPa·m^0.5 환산(ref 16) | ★ 우리 사이클-MPM/SE-fracture *입력 G_c*; 우리 Auerbach 의 *에너지* 대응 |
| **균열-방지 = ΔV<7.5 % + G_c≥4 J/m²** | 본 논문 핵심 임계 | ★ 우리 사이클-균열 *검증 임계*(우리가 재현해야 할 target) |
| **Table 1 SE 모듈러스**(sulfide 14–25, argyrodite 18.5, LLZO 150) | Table 1 survey | ★ 우리 E_SE *real* 앵커 corpus 보강(4번째 외부 확인); 할라이드 확장 시 oxide/sulfide 대조 |
| **무차원 𝒢 = 0.5·k_SE·(3β_AM·A_AM)²/(H·G_c) < 1000** | 본 논문 설계규칙 | ★ 우리 *입자크기·팽창·SE강성·두께* 설계 스윕의 *해석적 collapse* 후보(우리 ML 예측의 물리 prior) |
| **β_SE=0**(SE Vegard zero) + **δ₀=5 nm/δ_cr=100 nm** | Table 2 | ★ 우리 cycling 모델 cohesive 길이 스케일 기본값 |
| **AM 응력 >1 GPa / SE 응력 0–200 MPa** | Fig 2c | ★ Kang(σ_Mises GPa)·우리 So 2021(Si AM-AM 2.5–5.9 GPa) 와 *같은 계열* 응력규모 — 우리 압밀 AM-shielding 응력과 교차(단 driver 다름) |

### 8.3 ★ 우리 Auerbach 와의 *접목* (압밀-버전 → 사이클-버전 가교)
- 우리 Auerbach = **압밀 접촉응력 → AM 입자 균열**(통계 P_c).  Bucci = **사이클 Vegard 응력 → SE 균열**(결정론 CZM).
- **가교 1(크기-의존, A9 와 합류):** Kang+Bucci 둘 다 *큰 입자/큰 팽창*이 더 깨짐 → 우리 Auerbach 임계를 *입경-스케일링*
  (σ_crit∝1/√d 또는 접촉응력∝입경)으로 보강하면 *압밀-시점* 크기효과 표현(사이클-시점은 frame[5] 미보유 명시).
- **가교 2(에너지 일관):** 우리 Auerbach(임계응력)·Bucci(G_c 에너지)는 K_IC=√(E·G_c) 로 *환산 가능* → 우리 fracture
  에 *G_c(2.8 J/m²)* 를 통일 단위로 도입하면 두 모델 비교 가능.

### 8.4 한계 (적용 시 주의)
- **2D plane-strain · 11 µm · 36 입자 · mono-1 µm** → 절대규모·통계 우리 real 12:4:1 3D 와 다름(추세/임계만).
- **AM·SE linear-elastic** → 우리 압밀 *소성*(MPM J2)·*hooke/hysteresis*(DEM)와 구성식 다름 — *압밀*에 직접 못 씀(*사이클*
  전용).  **압밀 porosity·Heckel·coverage 와 *직접 비교 금지***(이 논문은 그 양을 *안* 산출).
- **소재 미지정**(E_SE=15 = sulfide *대표*, 특정 LPSCl 아님) → σ 절대전이 금지; Table 1 *범위*만.
- **intrinsic CZM bias**(pre-inserted path) — 저자 self-flag; 균열경로 절대값보다 *추세/임계* 신뢰.

---

## frame[5] 위치 (our division)
> ★ **사용자 MANDATORY C.**  이 논문이 frame[5] 어디에 들어가는가 — 명료 진술.

```
                    파괴(fracture)의 frame[5] 분업
  ┌──────────────────────────┬──────────────────────────────────────┐
  │  COMPACTION(제조) 파괴    │  CYCLING(작동) 파괴                   │
  │  = 우리 소유 (DEM)        │  = Bucci CZM 소유 (우리 미보유)        │
  ├──────────────────────────┼──────────────────────────────────────┤
  │ • driver: 접촉응력(가압)  │ • driver: Vegard 팽창(Li 삽입)         │
  │ • 위치: AM 입자           │ • 위치: SE 상/GB                       │
  │ • 모델: Auerbach P_c +    │ • 모델: cohesive-zone CZM(결정론)      │
  │   Lawn 1998 multiplier    │   + history flux-차단                  │
  │ • 우리 MPM: J2 *연성*     │ • SE *취성* — 우리 J2 불가(D6 공백)    │
  │   (void-fill, 형상흐름)   │   → de Vaucorbeil continuous-damage    │
  │                           │     /cohesive MPM 으로 넣어야          │
  └──────────────────────────┴──────────────────────────────────────┘
       ↑ 우리가 *novelty* 로 주장할 것              ↑ Bucci(+Kang) 가 소유; 우리 *미래* 확장
```
- **명료 3-진술:**
  1. **압밀 파괴 = 우리(Auerbach/Lawn, DEM)** — AM-AM 접촉응력, AM 입자 균열, *제조-시점*.
  2. **사이클 *취성* SE 파괴 = Bucci CZM(우리 lack)** — Vegard 응력, SE 상 균열, *작동-시점*, 결정론 cohesive.
  3. **우리 MPM J2 = *연성 only*** — SE *취성균열* 표현 불가 → Bucci/Kang 의 CZM(또는 de Vaucorbeil continuous-damage
     MPM)이 채우는 칸; 우리 MPM 은 *압밀 소성 morphology*(void-fill, 형상흐름)를 소유.
- ★ **"novelty" framing(정직):** 이 논문은 **DEM 경쟁자가 *아니라* frame[5] *보완***.  우리 차별점 = **우리가 *소유한*
  것**(압밀 transport σ-삼중항 + packing/Furnas-dip + 소성 morphology) — Bucci 가 *안* 하는 것; Bucci 차별점 = **사이클 SE
  취성균열역학** — 우리가 *안* 하는 것.  → **두 논문이 같은 ASSB 의 *다른 절반*을 소유**(frame[5] *시간축* + *파괴-모드*
  분업).  우리 paper 에서 "사이클 SE 균열은 Bucci 2017 이 정량화(우리 미보유 frame[5] 칸); 우리는 *압밀-시점* 구조→수송과
  소성 morphology 를 소유" 로 *정직*하게 위치.

---

## 9. 인용 가능 문장 (deck/paper용)
- "Bucci et al. (2017) provided the *first quantitative mechanical-reliability analysis of ASSBs*, coupling an electro-
  chemo-mechanical FEM with a cohesive-zone model to predict *cycling*-induced fracture of the solid electrolyte —
  the time-axis complement to our *compaction*-time Auerbach/Lawn fracture in DEM (frame[5] division)."
- "Fracture is suppressed when electrode-particle volumetric expansion < 7.5 % and SE fracture energy G_c ≥ 4 J/m²; we
  adopt the McGrogan-derived G_c ≈ 2.8 J/m² (sulfide Li₂S–P₂S₅) and the dimensionless design rule 𝒢 < 1000 as literature
  anchors for a future cycling-fracture model."
- "Counter-intuitively, Bucci et al. show *compliant* SEs (E_SE ~15 GPa) are *more* prone to micro-cracking — a real-
  modulus *cycling* result that must NOT be conflated with our *effective* compaction modulus E_eff = 1.35 GPa (a softened
  proxy for granular rearrangement; our *real* E_SE ≈ 24 GPa sits at the top of their Table 1 sulfide range 14–25 GPa)."
- "Our MPM uses ductile von Mises J2 (volume-preserving plastic flow) and therefore cannot reproduce *brittle* SE cracking;
  the de Vaucorbeil continuous-damage/cohesive-MPM route (or Bucci/Kang CZM) is required to fill this frame[5] gap."

## 10. 주의/한계 (over-claim 방지)
- ★★ **층위 혼동 금지(가장 중요):** 이 논문 **E_SE=15 GPa = *real* 모듈러스(*사이클* 균열 입력)** ≠ 우리 **E_eff=1.35 GPa
  (*압밀-bed* 유효 프록시)**.  "compliant 가 더 깨진다"를 우리 압밀-softening 과 **직접 연결 금지**(§7.2).  우리 *real* 칸
  =24(Sakuda/Table 1 sulfide 와 일치)가 비교 대상이지 1.35 아님.
- **시간축 다름:** *사이클* 파괴(Vegard 팽창 driver) ≠ 우리 *압밀* 파괴(가압 접촉응력 driver).  "큰 입자/큰 팽창 더
  깨짐"은 Kang·우리와 *방향* 같으나 *driver 다름* — 압밀 결론으로 전사 금지.
- **구성식 다름:** AM·SE 둘 다 **linear-elastic + 취성 cohesive** ≠ 우리 MPM **연성 J2** / DEM **hooke-hysteresis**.
  우리 MPM 은 SE *취성균열* 못 함(D6) — 이 논문을 *압밀*에 직접 적용 불가, *사이클* 전용.
- **압밀량 미산출:** porosity·상대밀도·coordination·coverage·Heckel·σ_eff 절대값 **전부 n/a** → 우리 압밀/전달 앵커
  (Minnmann 14 %, Doux 18 %, 우리 15.6 %; σ_ionic 0.04–0.18)와 **직접 비교 금지**.
- **소재 미지정·2D·mono-1 µm·single-realization·intrinsic-CZM bias** → 절대규모·통계·균열경로 절대값보다 *추세/임계/규칙*
  (7.5 %, 4 J/m², 𝒢<1000)만 신뢰.  Table 1 은 *문헌 survey 범위*(절대 LPSCl 값 아님).
- **negative electrode 모델**(Si/Sn/Al/graphite 류 삽입음극) — *cathode* 가 아님(메커니즘은 일반화 가능하나, 우리 NMC811
  *양극*에 절대 동일시 금지; AM 팽충 0.1·100 GPa 는 *대표* 입력).
- **fracture toughness↔G_c 환산은 본문 추정**(K_IC=0.23→G_c≈2.8 J/m²) — McGrogan *glassy* Li₂S-P₂S₅(≠ 결정질 argyrodite
  LPSCl), 불확도 ±1.8.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
