# Song 2025 (Energy & Environmental Science 18, 3129-3147) — 미세전극(microelectrode) electrochemo-mechanical 디지털트윈: FIB-SEM 재구성 + 전성분 고유물성 → 셀전압 >98% 검증 + 입자↔셀 괴리 3메커니즘 + 폴리머 바인더 VISCOPLASTICITY ★★★ 우리 Phase-4(미세구조→PyBaMM) sibling + 바인더 점탄성(E3 --coh / #285 spring-back gap)에 직결

> slug `song2025_electrochemo_mechanical_microelectrode_ees` · DOI `10.1039/d4ee04856c` · type `FEM·electrochemo-mechanical` · PDF `Song_2025_EES_Microelectrode_ElectrochemoMechanical.pdf` · digested `2026-07-28` · status ✅
>
> ⓘ **정본 승격 2026-07-28** — 원본은 작업 브랜치 `claude/solid-state-cathode-improvement-hevry0` 의
> `docs/lit_song2025_electrochemo_mechanical_microelectrode_ees.md` 에서 논문 에이전트가 작성. 단일-서랍 규칙(CLAUDE.md)에 따라 이관.


**인용:** Jihun Song,ᵃ Royal C. Ihuaenyi,ᵃ **Jaejin Lim**,ᵇ Zihan Wang,ᵃ Wei Li,ᵃ Ruqing Fang,ᵃ
Amin Kazem Ghamsari,ᵃ Hongyi Xu,ᶜ **Yong Min Lee\***,ᵇ **Juner Zhu\***,ᵃ "A microstructural
electrochemo-mechanical model of high-nickel composite electrodes towards digital twins to bridge
the particle and electrode-level characterizations", *Energy & Environmental Science* **18** (2025)
3129-3147, DOI **10.1039/d4ee04856c**.  © 2025 The Authors (RSC, **Open Access CC BY-NC 3.0**).
접수 2024-10-21, 게재확정 2025-02-04.  **ᵃNortheastern Univ.**(Mechanical & Industrial Eng., Boston —
**Juner Zhu** 교신, j.zhu@northeastern.edu) + **ᵇYonsei Univ.**(Chemical & Biomolecular Eng., Seoul —
**Yong Min Lee** 교신, yongmin@yonsei.ac.kr = **DTBL**) + **ᶜUniv. of Connecticut**(Mechanical Eng.,
Storrs).  ★ **Cover-featured**(표지 논문).  지원: Center for Battery Sustainability (Hyundai Motor,
Shell, SES.AI, Saint-Gobain, Siemens) + NSF CMMI-2142290.

**연세대 DTBL(이용민) 그룹 + Juner Zhu(Northeastern) 공동** — `docs/literature_yonsei_dtbl_2026.md`
**TIER-1 신규**.  ⚠ **#266/#271(우리 LPSCl ASSB)과 결정적으로 다름: 이건 NMC + 액체전해질 일반 LIB**
→ **셀 절대값(전압·용량·과전압·σ) 전이 ✗**.  ★ **METHODOLOGY 3종이 핵심 가치**(수치앵커 아님 —
앵커는 Bazzoun/Varkey/Minnmann/#266/#271):
**(a)** 미세구조(FIB-SEM 재구성) → **full electrochemo-mechanical** → **셀전압 검증**(우리 Phase-4 sibling),
**(b)** 입자↔셀 괴리 **3메커니즘**(반응면적↓ / 확산길이↑ / 전해질부족 = 우리 coverage·ASA / τ / porosity·SE-vol),
**(c)** ★★ **폴리머 바인더 VISCOPLASTICITY**(Perzyna 시간/속도의존 + Ludwick 경화) — **우리 MPM이 없는 물리**
(E3 `--coh` cohesion 레버 + #285 점탄성 spring-back gap의 직접 후보).

**소재계 (★ NMC + 액체 — 우리 LPSCl 아님, 주의):**
- **AM(활물질) = LiNi₀.₇Mn₀.₁₅Co₀.₁₅O₂ (NMC711)**, high-nickel layered oxide.  단결정 입자 측정(single
  particle).  **1차입자 직경 0.5–1.5 µm**, 밀도 4.77 g/cm³, 비용량 183.5 mAh/g.  ⚠ **NMC711 = 액체 LIB
  표준 양극**(우리 LPSCl ASSB의 NMC811과 화학 유사하나 셀계가 다름).
- **CBM(conductive & binder materials, 도전재+바인더 통합상) = PVDF(KF-1300, M_w 350k, Kureha) 바인더 +
  Super P(Imerys) 도전재**.  ⚠ **둘을 통합(combined) CBM 단일상으로 모델**(sub-µm carbon은 voxel보다 작아
  개별 입자화 불가 → 목표 부피분율 채우는 연속상; 우리 `additives.py` CBD continuum과 동형).
- **전해질 = 1 M LiPF₆ in EC:EMC = 3:7 (vol)** (Enchem).  ⚠ **액체전해질** — 우리 sulfide SE 아님(t₊≈0.38,
  대류·농도분극 있음 = 단일이온 SE와 근본 다름).
- **집전체 = Al(15 µm, Sam-A)**; **음극 = Li metal**(반쪽셀, Li 과전압 일정 가정 → 양극에 분석 집중).
- **조성 = NMC711 : PVDF : Super P = 96 : 2 : 2 wt%**, Al 집전체에 코팅, 160°C 1 h 건조, **roll-press →
  두께 70 µm, 밀도 3.3 g/cm³**.  분리막 20 µm(Tonen).  ⚠ **셀 = coin cell(half), 양극에 집중**.

---

## ★ 한 문장 결론 — 이게 무엇이고 우리에게 왜 중요한가

**FIB-SEM으로 NMC711 복합양극의 실제 3D 미세구조(AM·CBM·pore·집전체)를 재구성하고, 모든 성분에 각자의
고유 전기화학·기계 물성(단일입자 측정 + nanoindentation + 바인더 인장시험)을 직접 부여한 "미세전극
electrochemo-mechanical 모델"이 coin-cell 전압곡선을 >98% 정확도로 재현한다.  이 모델은 입자수준에서는
빠른 충전이 가능해 보이지만 셀수준에서 안 되는 괴리를 3가지 메커니즘 — (1) 반응면적 감소(particle-vs-cell
30.52% specific-surface 차 + CBM/집전체에 가려진 비반응 계면 → 유효 ASA의 61.76%만 활성), (2) 확산길이
증가, (3) 전해질 부족 — 으로 정량 분해한다.  과량전해질 설계로 4C에서 94% 용량유지를 달성.  더 나아가 도전재·
바인더의 역할과 **폴리머 바인더의 점소성(viscoplasticity, Perzyna+Ludwick)**을 모델에 넣어, cycling 중
바인더-입자 연결의 기계열화(5 cycle에서 yield stress 42.10 MPa로 포화)를 시뮬레이션한다.**

**★ 우리 hook (왜 이게 Phase-4·MPM에 결정적인가):**
이 논문은 **우리 Phase-4 파이프라인의 sibling published 버전 + 우리 MPM이 없는 한 조각(시간의존 바인더
점탄성)을 정확히 채운 모델**이다:
- **(A) Phase-4 결합 청사진(#281 NEXT 단계):** #281(Li-O₂)이 "미세구조→GeoDict effective→1D 전기화학(COMSOL)
  →방전곡선"의 effective-property(균질화) 버전이었다면, **이 #17은 미세구조를 voxel mesh로 직접 풀어
  (homogenization 없이) 전성분 PDE를 격자에서 푼다**(reaction-area·tortuosity·porosity를 effective 평균값으로
  근사하지 않고 실구조에서 직접) → **우리 Phase-4의 "structure-resolved" 끝판**.  논문이 명시:
  "directly defining the governing equations on each component … avoiding homogenization and
  approximations" — 우리 PyBaMM-DFN(effective τ/σ 주입)보다 한 단계 더 미세.
- **(B) 입자↔셀 3메커니즘 = 우리 transport triad 출력 1:1:** **반응면적↓ = 우리 coverage(Tabor/StageE)·ASA**,
  **확산길이↑ = 우리 tortuosity(τ_Laplace,eff/τ_Dijkstra)**, **전해질부족 = 우리 porosity·SE 부피분율**.
  세 메커니즘 모두 우리가 이미 출력하는 양 → **우리 미세구조 metric이 셀 괴리를 설명하는 published proof**.
- **(C) ★★ 바인더 VISCOPLASTICITY = 우리 MPM이 구조적으로 없는 물리:** Perzyna **점소성(rate-dependent, 변형률
  속도 의존)** + Ludwick **경화법칙**으로 PVDF 바인더의 시간·속도 의존 변형을 모델 → **우리 MPM의 rate-independent
  J2 한계(#285 점탄성 spring-back 재현불가)를 정확히 메우는 후보 모델**, 그리고 **E3 `--coh` cohesion 레버에
  점성 요소를 부여**할 수 있는 published 정식.  ⚠ 단 바인더 **인장시험은 dried film**(전해질 swelling 미반영,
  논문 자인) — 우리도 같은 한계(전해질-impregnated 물성 미측정).

⚠ **전이 경계(CRITICAL):** **NMC711 + 액체 LiPF₆ LIB ≠ 우리 LPSCl sulfide ASSB.**  셀 전기화학 절대값
(전압·과전압·용량·σ_e·D)은 **전이 ✗** — 액체전해질(t₊≈0.38, 대류, 농도분극) vs 단일이온 SE(t₊≈1, 무대류,
접촉저항), 반쪽셀 Li-metal 음극, NMC711 비용량.  **σ_ionic/porosity 절대앵커는 Bazzoun/#271/#266(LPSCl)·
Varkey(halide)·Minnmann이 담당** — 이 논문은 **방법론 + 바인더 역학 모델**만 가져온다.

---

## 1. 배경 / 동기 (Introduction, p.3129–3131)

- LIB의 성능(고에너지밀도·빠른 충전·장수명)은 복합전극 내 **전자·Li⁺의 효율적 이동성**에 좌우 → 미세구조
  특성이 지배.  LFP가 입자수준 구조설계(입경↓·탄소코팅)로 저전도/저확산 한계를 극복해 상용화한 사례가 동기.
- **입자수준 모델(particle-level):** single particle measurement, STXM, BCDI, nanoindentation, phase-field,
  3D-reconstruction operando 모델 → **활물질 고유특성·빠른충전·균열을 잘 기술**하나 **복합전극 전체구조(입자
  너머)는 무시** → 셀거동 정확예측 한계.
- **셀수준 모델(cell-level):** **P2D(Doyle-Fuller-Newman)** + 3D 열모델 결합(thermal-electrochemical).
  셀성능은 직접 측정하나 **너무 큰 스케일(coin ~1 Ah = 수백만 입자, EV pouch ~100 Ah = 수십억)** → **각
  성분의 개별 특성을 정확 반영 못 함** — homogenization·effective 물성에 의존.
- **★ 바인더의 누락:** 바인더는 cell-level 모델에서 자주 무시 → 그러나 활물질을 묶고(delamination 방지)
  도전재와 결합해 전극 전기전도 향상.  **cycling 중 활물질 팽창/수축의 반복 기계하중 → 바인더 피로 → 바인더-
  입자 계면 파괴 → 수명 급감.**  ⇒ 바인더 역학을 넣어야 함(이 논문의 차별점).
- **기존 입자수준 모델의 한계(명시):** 대부분 **small-deformation·elastic**만 가정 → cycling 중 활물질의
  큰 수축/팽창과 **CBM의 소성변형(plastic deformation)을 무시** → 예측 정확도↓.
- **본 연구(명시):** **NMC711 복합양극의 FIB-SEM 이미지 수백 장 → 미세전극(microelectrode) 수준
  electrochemo-mechanical 모델** → 충전 중 구조변화가 전기화학·기계 특성에 미치는 영향을 정밀 분석 + **CBM의
  비탄성(inelastic) 변형 + 점소성 기반 기계열화 예측**.

---

## 2. ★ 미세전극 모델 개발 — 구조 재구성 + 전성분 고유물성 (Results, Development, p.3130–3132)

### 2.1 입자/셀 이중 특성화 (Fig 1A/B)
- **입자수준(Fig 1A):** **단일입자 측정**(Au filament에 단일 NMC711 입자를 micromanipulator로 접촉 → Li metal
  대극, 부반응 차단 봉인) + **nanoindentation**(수십 µm 평면 압자로 단일입자 압축 → 기계물성).  → 활물질의
  electrochemo-mechanical **고유물성**.
- **셀수준(Fig 1B):** **coin cell rate capability(1/2/4/8C) + GITT** 측정 → 셀 전기화학 검증 reference.

### 2.2 ★ 3D 미세구조 재구성 (Fig 1C, Table 1) — FIB-SEM (top-down reconstruction)
★ 핵심 — **측정 미세구조를 voxel mesh로 직접 변환**(GeoDict식 effective가 아니라 실구조 PDE 풀이).
- **장비:** **FIB/SEM (NB 5000, Hitachi)** → NMC711 양극을 **65 nm 간격**으로 절삭, **540장** tomography,
  **pixel 43.78 nm, 해상도 2048×1536**.
- **세그멘테이션:** ★ **SAM(Segment Anything Model, deep-learning) meta-segment**로 활물질·CBM·pore·집전체의
  전체 면적과 배경 제거 → median filter → greyscale로 3상(활물질/CBM/pore) 분류 → 3D voxel mesh로 적층.
- **★ 검증(frame[4] 그들 내부판):** 재구성 구조의 각 상 부피분율을 원본 tomography(30×70.8×30 µm³ crop)와 비교
  → **good match**(Table 1): NMC711 0.68355(재구성) vs 0.68335(실측), CBD 0.08067 vs 0.08062, porosity 0.23582
  vs 0.23583.  → "재구성 ≈ 실구조" 확인.
- ⚠ **해상도 다운샘플:** 계산비용 때문에 **시뮬 voxel = 600 nm/voxel**(원본 43.78 nm에서 다운) → **8-node solid
  element**로 변환.  도메인 = **30×70.8×30 µm³**(Table 1) — 그러나 Fig 1E의 모델 도메인은 **90×90×90 µm³**로
  표기(전극 두께축 90 µm).  ⚠ **도전재(CBM)는 sub-nano~수십 nm라 정확 형상 포착 불가** → **목표 부피분율을 채우는
  연속 CBD 도메인**으로 통합(우리 voxel CBD와 동형).

### 2.3 ★★ 전성분 고유물성 (Table 2/3/4/5) — homogenization 회피의 핵심
★ **각 성분에 cell-level effective가 아닌 측정/문헌 고유물성을 직접 부여** — 이게 정확도의 원천(논문 명시:
"directly defining the governing equations on each component (Fig 1E), avoiding homogenization").

**★★ Table 2 — NMC711 활물질 electrochemo-mechanical 파라미터:**
| 파라미터 | 값 | 단위 | ★우리 대응 |
|---|---|---|---|
| 초기온도 | 303.15 | K | |
| 복합전극 용량 | 0.2294 | nA·h | (미세전극 도메인 스케일) |
| 비용량 | 183.5 | mAh/g | NMC811 ~200 (우리계) |
| 밀도 | 4.77 | g/cm³ | 우리 AM 4.77 (NCWA/NCM 동일) |
| Solid volume | 4.4312×10⁻¹⁴ | m³ | (도메인) |
| **Porosity** | **0.0455** | (%, 표기상 4.55%) | ⚠ 활물질 내부 porosity |
| **1차입자 직경** | **0.5–1.5** | µm | 우리 r_AM (단결정 NMC) |
| 최대 Li 농도 c_s,max | 49122 | mol/m³ | |
| **초기 교환전류밀도 i₀,init** | **2.6×10⁻³ → 26** | A/m² | ★ BV 핵심(식13: i₀=26 A/m²) |
| 초기 cathodic 확산계수 D_s,init | **3×10⁻¹¹** | cm²/s (=3×10⁻¹⁵ m²/s) | ★ 고체확산(식3) |
| 최소/최대 lithiation | 0.242 / 0.91 | | (x in LiₓNMC) |
| cathodic/anodic transfer | 0.5 / 0.5 | | BV 대칭 |
| **전자전도도 σ_AM** | **SOC 함수(Fig)** | S/m | ★ **lithiation 0.2→1.0서 ~0→1.7 S/m 급증**(0.135–17 mS/cm) = 우리 σ_AM(e) |
| **★ Young's modulus E_AM** | **2.611** | **GPa** | ⚠ **활물질 측정 modulus(nanoindentation)** |
| **★ Yield stress σ_y,AM** | **0.1534** | **GPa** | ★ **우리 SE σ_y 0.15와 우연 동급**(소재 다름) |
| Isotropic tangent modulus | 1.3055 | GPa | |
| **Poisson ν_AM** | **0.25** | | 우리 AM rigid·#266 ν_AM 0.25 일치 |

⚠ **주의:** E_AM=2.611 GPa는 **활물질 NMC711**의 nanoindentation 값(우리 AM=rigid 가정과 다름; 우리 22 GPa
SE-modulus 앵커와 무관 — 이건 oxide AM이지 sulfide SE가 아님).  NMC811 oxide 실측 modulus는 ~140–200 GPa
(#266 Fig S14)인데 **2.611 GPa는 단일입자 nanoindentation의 effective(균열·기공 포함) 값** → 활물질 자체의
softened modulus.  ★ **우리계 매핑 시 이 modulus는 AM(oxide)용이지 SE용 아님 — 혼동 금지.**

**★★ Table 3 — CBM(conductive & binder, 통합상) 파라미터 ★ 바인더 역학의 핵심:**
| 파라미터 | 값 | 단위 | ★우리 대응 |
|---|---|---|---|
| **전자전도도 σ_CBM** | **375** | S/m (=3750 mS/cm) | ★ 우리 CBD(SuperP) σ_e; #266 σ_CB 1000 mS/cm와 동급 자릿수 |
| 밀도 | 1.76 | g/cm³ | PVDF+SuperP 통합 |
| Volume | 0.0809 | m³(도메인) | |
| **Poisson ν_CBM** | **0.326** | | ★ 바인더 점탄성상 |
| **★ Young's modulus E_CBM** | **1.05** | **GPa** | ★★ **바인더 film 인장시험(Fig 1D)에서 도출** |
| **★ Yield strength σ_y,CBM** | **19.36** | **MPa** | ★★ **바인더 항복(저속 인장)** |
| **Isotropic tangent modulus** | **284.90** | **MPa** | ★ 바인더 경화 |
| Resistivity | 2×10¹² | Ω·m | (비전도 한계) |
| **Electrolyte fraction in CBM** | **0.16** | | ⚠ **CBM에 전해질 16% 침투**(swelling, eqn 6) |
| **★ Stress exponent (Perzyna b)** | **1** | | ★★ Perzyna 응력지수(점소성) |
| **★ Viscoplastic rate coeff. (Perzyna A)** | **변형률속도 함수(Fig)** | s⁻¹ | ★★ **0→3×10⁻³ s⁻¹**(strain-rate 0→300×10⁻⁵) |
| **★ Hardening exponent (Ludwick n)** | **2** | | ★★ Ludwick 경화지수 |
| **★ Strength coeff. (Ludwick k)** | **변형률속도 함수(Fig)** | MPa | ★★ **~1100→1200 MPa**(strain-rate 0→300×10⁻⁵) |

★★ **이 CBM 블록이 우리 MPM에 없는 바인더 점탄성 모델의 전부** — E_CBM=1.05 GPa, σ_y=19.36 MPa, Perzyna
A(변형률속도)·b=1, Ludwick k(변형률속도)·n=2.  (§3 바인더 viscoplasticity 상세 참조.)

**Table 4 — 전해질(1 M LiPF₆ EC:EMC 3:7) 파라미터:**
- 초기온도 303.15 K, **초기 Li 농도 c_e = 1000 mol/m³**.  **σ_e(전해질전도) / D_e(확산) / t₊(transport number)
  / activity dependence는 모두 c_e 함수**(Fig 곡선): σ_e ~0.5–0.82 S/m(c_e 400–1600), D_e ~1.2–2.7×10⁻¹⁰ m²/s,
  **t₊ ~0.10–0.30**(c_e↑→t₊↓), activity ~−0.1→0.7.  ⚠ **t₊≈0.38(1 M 기준)·대류·농도분극 = 액체전해질 = 단일이온
  SE(t₊≈1)와 근본 다름** → 셀 absolute 전이불가의 핵심 이유.

**Table 5 — Al 집전체(CC) 파라미터:**
- σ_e 3.58×10⁷ S/m, 밀도 2.70 g/cm³, **E_CC 6.88 GPa**(또는 2.611 표기), σ_y 276 MPa, ν 0.3314.

---

## 3. ★★ Modeling methodology — 지배방정식 (전기화학 + 기계 + 바인더 점소성) (p.3142–3145)

★ **우리 Phase-4(PyBaMM-DFN) + MPM(J2) 대응의 published full set.**  COMSOL Multiphysics 6.0
(Lithium-Ion Battery + Transport of Diluted Species + Solid Mechanics + Deformed Geometry 모듈,
AMD Threadripper PRO 64-core, 단일 방전곡선 ~2주 계산).

### 3.1 전기화학 — 질량보존 + 전하보존 + BV (Fig 1E)

**(1) 활물질 Li 질량보존 (Fick, 식1–3):**
∂c_s/∂t = ∇·(D_s,eff ∇c_s);  BC: ∇c_s|_surface = −j/(D_s,eff·F), c_s|_center = c_s,init.
★ **실구조 재구성이라 D_s,eff = D_s 그대로**(셀설계로 안 변함 = homogenization 회피) → 식2 단순화
∂c_s/∂t = ∇·(D_s ∇c_s).  **★ 농도의존 확산(식3):**
**D_s = D_s,init · exp[−6·(c_s/c_s,max − 0.1)⁵]**,  D_s,init = 3×10⁻¹⁴ m²/s.
⚠ ⇒ 우리 stage4 §1의 Fick 구방정식(식3)과 동형, 단 **D_s가 SOC 강의존**(고Ni 특유).

**(2) 전해질 질량보존 (concentrated-solution, 식4–6):**
ε_e ∂c_e/∂t = ∇·[−D_e,eff ∇c_e + t₊·(−σ_e,eff∇φ_e + (2σ_e,eff RT/F)(1−t₊)∇ln c_e)/F].
★ **실구조라 전해질 전부 포착 → ε_e=1, D_e,eff=D_e, σ_e,eff=σ_e**(식4 → 5, effective 불요).
⚠ **단 CBM 내부는 전해질 16% 침투(ε_e=0.16) → Bruggeman**: D_e,eff=ε_e^1.5·D_e, σ_e,eff=ε_e^1.5·σ_e (식6).
⇒ **핵심전극(pore)은 실구조 직접, 보조도메인(CBM침투)은 Bruggeman** = #281 채택디테일 ①과 동일 패턴.

**(3) 전하보존 (Ohm, 식7–11):**
∇·(σ_s,eff ∇φ_s) = a_s·j (고체);  BC: ∇·(σ_s,eff∇φ_s)|_currentflow = I/A, |_AM surface = 0.
★ 실구조라 σ_s,eff=σ_s (식7→8).  전해질·CBM 액상 전하보존(식9–10):
∇·[−σ_e,eff∇φ_e + (2σ_e,eff RT/F)(1+∂lnf/∂lnc_e)(1−t₊)∇ln c_e] = a_s·j.
⚠ CBM은 전해질-혼합이라 σ_e,eff=ε_e^1.5·σ_e Bruggeman (식11).

**(4) 반응속도 — Butler-Volmer (식12–14):**
**j = i₀·[exp(α_a Fη/RT) − exp(−α_c Fη/RT)]**.  ★ **농도의존 교환전류(Arrhenius형, 식13):**
**i₀ = i₀,init · exp[−7·(c_s/c_s,max − 0.1)²]**,  i₀,init = 26 A/m².
과전압 **η = φ_s − φ_e − U_eq (식14)**.  ⇒ 우리 stage4 §1의 BV(식5)와 동형, i₀ 형태만 고Ni 특화.

### 3.2 ★ 기계 — elastic + hygroscopic(Li-induced) strain + CBM 점소성 (식15–31)

**(1) 운동학·평형 (식15–18):**
변형률 ε(u) = ½(∇u + (∇u)ᵀ) (식15);  Dirichlet BC u=û (식16);  운동량보존 ∇·σ + b = 0 (식17);
Neumann BC σ·n = t̂ (식18).

**(2) ★ 활물질(NMC711) — Li-induced strain(hygroscopic) + elastic(소성 NO):**
구성식 σ=σ(ε, ε̇) (식19) → small-deformation 가산분해 **ε = ε_e + ε_vp + ε_s (식20)**.
Cauchy 응력 **σ = ℂ:ε_e (식21)**.  ★ **NMC711은 brittle(취성)** → "strain tensor formulation excludes
viscoplastic strains" → **ε = ε_e + ε_s (식22)**(활물질엔 점소성 없음 = elastic + Li-strain만).
★ **Li-induced strain(hygroscopic theory, 등방체적변화, 식23):**
**ε_s = β_L·M_m·(c_s − c_s,init)**,  β_L = Li-induced strain coefficient(Fig S32D), M_m = molar mass.
⚠ ⇒ **활물질의 충방전 부피변화를 "흡습 팽창(hygroscopic swelling)"으로 모델** — Li 농도변화 → 등방
strain → 응력.  우리 Stage-3 H2→H3 ~8% 부피변화의 연속체 버전(우리는 DEM fracture로 처리).

**(3) ★★ CBM(PVDF+SuperP) — elastic + VISCOPLASTIC (점소성) — 이 논문의 차별점:**
CBM은 **elastic + viscoplastic 둘 다** → **ε = ε_e + ε_vp (식24)**.
★ **Perzyna 점소성 모델(rate-dependent, 변형률속도 의존, 식25):**
**ε̇_vp = λ̇·∂f(σ,ε̄_vp)/∂σ**  (associated flow rule).
**항복함수 (식26): f(σ,ε̄_vp) = σ̄ − σ_y**,  등가응력 **σ̄ = √(3/2 s:s) (식27)**(s = deviatoric stress).
★ **Ludwick 등방경화 (식28): σ_y = σ_y0 + k·(ε̄_vp)ⁿ**  (k = strength coefficient, n = hardening exponent=2).
누적 등가 점소성변형 **ε̄_vp = ∫₀ᵗ √(2/3 ε̇_vp:ε̇_vp) ds (식29)**.
★ **Perzyna viscoplastic multiplier (식30): λ̇ = A·⟨f(σ,ε̄_vp)/σ_y⟩ᵇ**  (A=viscoplastic rate coeff,
b=stress exponent=1, ⟨·⟩=Macaulay bracket).  **⟨f/σ_y⟩ = f/σ_y if f≥0, else 0 (식31).**

★★★ **이 식25–31이 우리 MPM이 구조적으로 없는 "시간/속도 의존 소성"** — Perzyna 모델은 항복 초과량
(f/σ_y)의 b제곱에 비례하는 **속도(λ̇)**로 점소성이 흐른다 → **변형률속도가 빠를수록 더 단단(rate-stiffening),
느릴수록 흐름(creep/relaxation)** = **시간의존**.  우리 MPM의 rate-independent J2(λ̇가 정의 안 됨, 즉시 항복면
복귀)와 근본 다름.  → **#285의 시간의존 spring-back(점탄성)·E3 `--coh` 점성요소의 직접 published 정식.**

### 3.3 도구
COMSOL Multiphysics 6.0 (Li-Ion Battery + Diluted Species + Solid Mechanics + Deformed Geometry).
**deformed geometry가 핵심** — Li-strain으로 변형된 구조가 다시 전기화학(반응면적·확산경로)에 피드백
(electrochemo-mechanical 양방향 결합).

---

## 4. 섹션별 결과 — 모든 수치

### 4.1 ★ 입자 vs 셀 전압 괴리 — rate별 과전압 (Fig 2, p.3133)

**Fig 2 (A)1C (B)2C (C)4C (D)8C 방전전압(equilibrium·particle·coin cell) + (E)particle-eq 전압차 +
(F)cell-eq 전압차.**

- **★ 1C(60 min), x=0.24 (방전 시작):** **particle 과전압 0.0089 V** vs **coin cell 0.1383 V** = **15배↑**.
  전압곡선 기울기는 x=0.8까지 유사 → 차이는 주로 **초기 생성 과전압**.  cutoff(3 V) 도달 시 x = particle 0.3577
  / coin cell 0.6169.
- **★ 2C/4C/8C, x=0.24:** particle 과전압 0.0142/0.0244/0.0405 V vs coin cell 0.2538/0.4505/0.8234 V =
  **18–20배↑**.  coin cell 용량 감소(eq 대비) 2C/4C/8C = **23.89% / 89.23% / 96.95%**.
- ⇒ **입자수준은 빠른충전 가능(과전압 작음)하나 셀수준은 15분(8C) 충전이 사실상 불가**(과전압 폭증) →
  **입자↔셀 괴리를 분석·해소해야 빠른충전 달성** = 논문의 핵심 동기.  셀 과전압은 양극·음극 둘 다 영향받으나
  Li metal 음극 과전압 일정 가정 → **양극(NMC711 복합)에 집중 분석**.

### 4.2 ★★ 3가지 괴리 메커니즘 — 정량 분해 (p.3134) ★ 우리 transport metric과 1:1

**메커니즘 1 — 반응면적 감소(reduced reaction area):**
- **★ 비표면적(SSA, surface/volume) — particle vs microelectrode:** **particle 2,476,784 m²/m³** vs
  **microelectrode 1,720,752 m²/m³** = **30.52% 차이**.  ⇒ 셀에서는 입자가 서로 접촉·CBM·집전체에 가려져
  전해질과 닿는 면적이 줄어듦.
- **★ 비반응 계면 차감(coin cell 실제 활성면적):**
  - CBM 12% 전해질 함유 가정 → 활물질-CBM 계면의 **12%만 반응**, 나머지 88%(**8.30×10⁻⁹ m²**) = 비반응.
  - 활물질-집전체 계면(**7.71×10⁻¹⁰ m²**) = 비반응.
  - 차감 후 활물질 활성면적 = **1,538,340 m²/m³** = particle 비표면적의 **62.11%**.
  - 측면 비접촉 보정 후 = **1,529,744 m²/m³ = particle의 61.76%**.
- ⇒ ★★ **유효 반응면적은 입자 고유 비표면적의 ~62%만** — **나머지 38%는 입자접촉·CBM·집전체에 가려져 죽은
  면적(dead area)**.  ⭐ **= 우리 coverage(Tabor/StageE) + dead-AM/active-fraction 출력 1:1**(우리는 AM이 SE에
  덮인 비율·ionic/electronic active fraction을 직접 계산).

**메커니즘 2 — 확산길이 증가(increased diffusion length):**
- ★ **입경이 fast-charging 좌우** — 큰 입자 = 긴 확산경로 → rate↓; 작은 입자 = 짧은 경로 → rate↑ BUT
  기계강건성 저하(균열↑).  Fig 3C/G(25% 충전 4C): 큰 입자에서 delithiation 불균일.  ⇒ **입경 최적화 = rate ↔
  기계 trade-off**.  ⭐ **= 우리 tortuosity(τ_Laplace,eff) + 입경(r_AM) → σ_ionic C(τ)** 물리.

**메커니즘 3 — 전해질 부족(insufficient electrolyte volume):**
- ★ **realistic(전해질이 전극 표면만 덮음) vs excessive(전해질이 전극 전체를 감쌈)** 비교.  realistic에서
  **전해질이 부족 → Li⁺ 농도구배 심화 → 과전압↑.**  Fig 3 (4C, 25% 충전):
  - **realistic:** Li⁺ 농도가 전극표면 근처 높고 집전체 근처 낮음(구배 큼, Fig 3C–F) → 집전체 근처 과전압↑.
  - **excessive:** 잉여 전해질이 충분한 Li⁺ 공급 → CBM·전해질 내 균일 농도(Fig 3G–J) → 낮은 과전압.
  - **★ 용량유지(과량전해질): 1C/2C/4C = 100% / 96.72% / 94.01%**(realistic는 90.5/81.58/26.5%) → ★
    **4C에서 94% 용량유지**(realistic 26.5%의 3.5배) = 논문 headline 설계.
- ⇒ ⭐ **= 우리 porosity·SE 부피분율**(전해질 부피 = ASSB에선 SE 부피)·percolation.  ⚠ **단 ASSB는 SE가
  고정 부피(액체처럼 "더 부을" 수 없음) → "과량전해질" 설계는 ASSB에 직접 안 통함**(SE 부피분율↑로 대응).

### 4.3 ★ 구조분석 — 전류밀도 + CBM 지배 (Fig 4, p.3136–3137)

**Fig 4 (A)부피변화 (B)비표면적 (C)활물질/유효 전류밀도 (D)CBM 전류밀도 (E–J)3D/2D 전류밀도맵(4C, 25%).**
- **★ 충전완료(4.3 V) 부피변화:** 1C/2C/4C = **2.37% / 1.71% / 0.34%**(rate↑→충전 덜 됨→변화↓).  비표면적
  증가 0.81% / 0.57% / 0.08%.  ⚠ ⇒ **NMC711 부피변화 ~2.4%@1C**(저Ni 수준; 고Ni 8%는 더 깊은 충전서).
- **★ 전류밀도(4C 평균):** 활물질 **16.29/35.20/96.60 A/m²**(1/2/4C) vs **CBM 222.10/431.01/1012.92 A/m²** =
  ★ **CBM 전류밀도가 활물질보다 1000%+ 높음** → 유효 전류밀도(활물질+CBM) **38.78/78.39/196.40 A/m² = 활물질
  대비 ~200% 높음**.  ⇒ ★★ **전류는 집전체에서 주로 CBM을 통해 흐른다(활물질 아님)** — CBM 4 wt%에 불과하나
  지배.  ⭐ **= 우리 σ_e 접촉망에서 CBD(SuperP)가 전자전도를 carry하는 물리**(우리 carbon-network 발견과 정합).
- **★ CBM 연결성 결함:** 슬러리 건조(130°C) 중 **바인더 boiling → void 형성 → 전극표면 근처 CBM 연결 끊김**
  (Fig 4G/J) → 표면 근처 전류밀도↓.  ⇒ **불균일 CBM 분포가 전류분포를 좌우** = #275(연속 sheath)·우리 CBD
  분산균일도(E2)와 정합.

### 4.4 ★ 기계분석 — von Mises 응력·strain + CBM 소성 (Fig 5, p.3137–3140)

**Fig 5 (A)평균 (B)최대 von Mises 응력 + (C–N)3D 응력/strain맵(realistic vs excessive, 4C 25%).**
- **★ 충전완료(94%, excessive 4C) 집전체 근처 최대응력 314 MPa** → 활물질 고응력 → CBM 응력·strain 전달
  (Fig 5M/N) → **CBM 소성변형(plastic deformation)**.
- **realistic:** 응력·변형이 **전극표면·집전체 근처 집중**(Fig 5C–F).  **excessive:** 더 균일 분포(Fig 5I/J).
  ⚠ 단 excessive가 더 깊이 충전(94%)되므로 **충전말기 평균·최대 응력은 오히려 더 큼**(Fig 5A/B) — trade-off.
- ⭐ **= 우리 MPM von Mises 응력장 + 소성변형**(우리는 SE 소성, 그들은 CBM 소성 — 소성 주체가 다름; 우리 AM은
  rigid, 그들 활물질은 brittle-elastic).

### 4.5 ★★★ 바인더(CBM) VISCOPLASTICITY — 5 cycle 기계열화 (Fig 6, p.3139–3140) ★ 우리 MPM이 없는 물리

**Fig 6 (A)Perzyna 파라미터(strength coeff·viscoplastic rate coeff vs strain-rate) (B)응력-변형 실험vs시뮬
(3종 strain-rate) (C)5cycle 평균strain (D)yield stress 진화 (E)최대strain (F)응력-변형 + yield 포화.**

- **★ 바인더 film 인장시험(Fig 1D / 6B) — 3종 변형률속도:** **0.00003 / 0.0003 / 0.003 s⁻¹**.  실험↔시뮬
  정확도 **89.21% / 93.75% / 97.11%**.  ⇒ ★ **Young's modulus 1.05 GPa, yield 19.36 MPa**(Table 3) 도출.
  ⚠ **dried binder film 측정 → 전해질 swelling 미반영**(논문 명시: 실제는 전해질 함침으로 물성 변함, 제조 후
  수십 시간 내 swelling 관찰) — **우리도 동일 한계**(전해질-impregnated 바인더 물성 미측정).
- **★ Perzyna 파라미터(Fig 6A) — 변형률속도 의존:** **strength coeff(Ludwick k) ~1100→1200 MPa**, **viscoplastic
  rate coeff(Perzyna A) 0→3×10⁻³ s⁻¹**(strain-rate 0→300×10⁻⁵ s⁻¹ 범위).  ★ **rate↑ → k↑·A↑ = rate-stiffening**.
- **★ 5 cycle 기계열화(1C, realistic, Fig 6C–F) — 활물질 부피변화 일정 가정:**
  - **평균 strain: 0→0.00316**(cycle 내), 5 cycle 동안 **거의 일정**(Fig 6C).
  - **★ 평균 yield stress: 5 cycle에서 0.01%만 증가**(19.3600→19.3625 MPa, Fig 6D) = **경화 미미**.
  - **★ 최대 strain(집전체 근처): cycle마다 감소**(Fig 6E) — 평균과 반대 → **CBM 소성변형 발생**.
  - **★★ 최대 strain 영역 yield stress 진화(Fig 6F): 24→29→33→36→40 MPa → 포화 42.10 MPa**(5 cycle, 선형
    외삽).  ⇒ ★ **PVDF 파괴강도 45 MPa(저속 0.00003 s⁻¹)** > 포화 42.10 MPa → **PVDF는 견딤(파괴 안 함)** =
    "PVDF가 NMC 복합양극에 널리 쓰이는 이유"(기계무결성 유지).
- **★ 한계(논문 명시):** 이 모델은 **소성변형(plastic) 기반 기계열화만** 예측 → **입자균열·CC분리·SEI·Li
  plating·gas 등 장기열화는 미반영**(계산비용 + fracture 모델 부재).  정밀 CBM 파괴 모델·전극분리는 future work.
- ⇒ ★★★ **= 우리 MPM이 구조적으로 없는 "시간/속도 의존 + cycle 누적 경화" 바인더 역학** — Perzyna A·Ludwick
  k가 변형률속도 함수 + 5 cycle yield 진화(24→42.10) = **rate-independent J2로는 불가능**(우리 MPM은 단일 압축
  스냅샷, cycle·시간축 없음).  → **#285 점탄성 spring-back + E3 `--coh`의 published 구현 정식**(§6 상세).

---

## 5. 그림 한 장씩 — 무엇을 보이고 우리가 쓸 것

### 본문 Figures
- **Fig 1 (p.3132):** ★★ **모델 개발 전체** — (A) 단일입자 측정 + nanoindentation, (B) coin cell rate+GITT,
  (C) ★ **FIB-SEM 540장 → 3D 재구성**(활물질/pore/CBM/집전체), (D) ★ **바인더 film 인장 S-S 곡선**(실험vs시뮬,
  3 strain-rate → E 1.05 GPa, σ_y 19.36 MPa), (E) ★★ **미세전극 electrochemo-mechanical 결합 도식**(전기화학
  방정식 + 기계 + Perzyna/Ludwick).  → **우리 Phase-4 파이프라인 + MPM 결합의 1장 청사진**.
- **Fig 2 (p.3133):** ★ **입자 vs 셀 전압괴리** — (A–D) 1/2/4/8C 방전(equilibrium·particle·coin cell), (E)(F)
  전압차.  particle 과전압 ≪ coin cell(15–20배) → 빠른충전 입자가능·셀불가.  → **3메커니즘 분해의 동기**.
- **Fig 3 (p.3135):** ★★ **realistic vs excessive 전해질** — (A) 전압(1/2/4C 두 조건), (B) 과전압, (C–F)
  realistic 4C 25% Li농도(활물질/CBM/전해질) + 과전압맵(농도구배 큼), (G–J) excessive(균일).  → **메커니즘 3
  (전해질부족) + 94%@4C headline**.  ⚠ ASSB엔 직접 안 통함(SE 고정부피).
- **Fig 4 (p.3137):** ★ **구조·전류밀도** — (A) 부피변화(2.37/1.71/0.34%), (B) 비표면적증가, (C)(D) 전류밀도
  (CBM ≫ 활물질 1000%+), (E–J) 3D/2D 전류맵(CBM에 집중, 표면 근처 CBM연결끊김).  → **CBM이 전자전도 지배 +
  분포불균일** = 우리 carbon-network·CBD 분산.
- **Fig 5 (p.3138):** ★ **기계 von Mises 응력·strain** — (A)(B) 평균/최대 응력(realistic vs excessive),
  (C–N) 3D 응력/strain맵(집전체 근처 314 MPa 집중, CBM 소성).  → **우리 MPM 응력장 대응**(소성주체: 그들 CBM).
- **Fig 6 (p.3139):** ★★★ **바인더 점소성 + 5cycle 열화** — (A) Perzyna k·A vs strain-rate, (B) S-S
  실험vs시뮬(3 rate, 89–97%), (C) 평균strain(일정), (D) yield 0.01%↑, (E) 최대strain(감소=소성), (F)
  yield 진화 24→42.10 MPa 포화(PVDF 45 견딤).  → **우리 MPM이 없는 시간/속도/cycle 의존 바인더 역학**.

### 표 (본문 — SI는 제공 안 됨)
- **Table 1:** ★ 재구성↔실측 부피분율(NMC711 0.684, CBD 0.081, porosity 0.236) 검증.
- **Table 2:** ★★ NMC711 활물질 파라미터(E 2.611 GPa, σ_y 0.1534 GPa, ν 0.25, i₀ 26, D_s 3×10⁻¹⁴, SOC-σ).
- **Table 3:** ★★ **CBM 파라미터**(E 1.05 GPa, σ_y 19.36 MPa, Perzyna A·b=1, Ludwick k·n=2, σ_e 375 S/m,
  ε_e 0.16) = 바인더 점소성의 전부.
- **Table 4:** 전해질(c_e 1000, σ_e/D_e/t₊/activity = c_e 함수).
- **Table 5:** Al CC(σ_e 3.58×10⁷, E 6.88 GPa).
- **Table 6:** 파라미터 기호 정의.
- ⚠ **ESI(SI) 제공 안 됨**(DOI 10.1039/d4ee04856c) — Fig S1–S32(excessive 도식 S1A/D, Li-strain coeff β_L
  S32D, 등)·Video S1–S4(구조변형 동영상)는 본문에서 참조만.  본 디제스트는 본문 PDF 기준.

---

## 6. ★★ 비교 vs 우리 DEM+MPM + Phase 4 (핵심 섹션)

### 6.1 ★ Phase-4 sibling: 미세구조 → electrochemo-mechanical → 셀전압 (frame[5] 출력단)

| 축 | Song 2025 (#17) | 우리 Phase-4 (stage4 §6, PyBaMM) | 관계 |
|---|---|---|---|
| 미세구조 출처 | **FIB-SEM 재구성**(top-down) | DEM+MPM 압축예측(bottom-up) | ⚠ **그들=재구성(출력단), 우리=예측(입력단)** = #281/positioning_vs_geodict 패턴 |
| 미세구조 처리 | **voxel mesh 직접 PDE**(homogenization 회피) | **effective τ/σ 주입**(PyBaMM `tortuosity factor`) | ★ 그들이 한 단계 더 미세(structure-resolved); 우리는 effective 주입 |
| 전기화학 | **COMSOL full**(Fick+Ohm+BV, 식1–14) | **PyBaMM DFN**(같은 Fick+Ohm+BV) | ✅ 동형 방정식 |
| 기계결합 | ★ **deformed geometry 양방향**(Li-strain→반응면적 피드백) | Stage-3 H2→H3→DEM/MPM fracture loop | ★ 그들=연속체 양방향, 우리=DEM fracture 단방향 |
| 검증 | **coin-cell 전압 >98%** | (Phase-4 미구현 — 검증 reference 필요) | ★ 그들 워크플로 = 우리 Phase-4 published 검증 템플릿 |
| 셀계 | **NMC+액체 LIB** | **LPSCl sulfide ASSB** | ⚠ 절대값 전이 ✗ |

★ **채택할 것:** (1) **핵심전극=실구조 직접, 보조도메인(CBM침투)=Bruggeman** = #281 채택디테일 ①의 재확인 →
우리 PyBaMM에서 **양극만 우리 τ/σ 주입, 분리막=default Bruggeman**.  (2) **비구조 동역학(i₀=26, D_s=3×10⁻¹⁴)은
단일입자 측정/문헌에서 고정 → 구조변수만 변화**(structure-attribution) = #281 채택디테일 ②.  (3) **단일
방전곡선부터 검증 → cycling/degradation 분리**(그들도 5 cycle만, 장기열화 future work) = #281 채택디테일 ③.

### 6.2 ★★★ 3메커니즘 → 우리 transport triad 1:1 매핑 (Phase-4 핵심)

| Song 2025 메커니즘 (입자↔셀 괴리) | 정량값 | ⭐ 우리 DEM 출력 | Phase-4 hook |
|---|---|---|---|
| **① 반응면적 감소** (reaction area↓) | 유효 ASA = particle의 **61.76%**(38% dead: 입자접촉·CBM·집전체에 가림) | **coverage(Tabor/StageE) + ionic/electronic active fraction + dead-AM map** | PyBaMM 비표면적 a = 3ε_s/R_p를 우리 **유효 coverage로 보정** (전체 ASA 아님) |
| **② 확산길이 증가** (diffusion length↑) | 입경↑→경로↑→rate↓ (입경 최적화 = rate↔기계 trade-off) | **tortuosity(τ_Laplace,eff/τ_Dijkstra) + r_AM** | PyBaMM `tortuosity factor`에 우리 τ 주입 (#281 채택①) + 입경 → D_s,eff |
| **③ 전해질 부족** (electrolyte vol↓) | realistic 26.5% vs excessive 94% @4C (전해질부피 = 농도구배 지배) | **porosity + SE 부피분율 + percolation(f_p)** | ⚠ ASSB는 SE 고정부피 → "과량" 대신 **SE 부피분율↑ + σ_ionic 망** |

⭐ **= 이 3메커니즘은 정확히 우리가 이미 출력하는 3가지 미세구조 metric** → **우리 transport triad가 셀 괴리를
설명하는 published proof**.  특히 **① 유효 ASA 61.76%(38% dead)는 우리 coverage·active-fraction의 셀-수준
의미를 정량 부여** — 우리는 "AM이 SE에 덮인 %"를 계산하나, 이 논문은 "그 미덮인/가린 면적이 셀 과전압을
얼마나 키우는지"를 전기화학으로 닫는다.  ⇒ **우리 coverage → PyBaMM 반응면적 보정 → 셀전압**이 Phase-4의
구체적 결합 경로.

⚠ **③ 전해질부족의 ASSB 적응:** 액체 LIB는 "전해질을 더 부어(excessive)" 농도구배를 없앤다.  ASSB는 SE가
**고정 부피 고체**라 더 부을 수 없음 → 대신 **SE 부피분율↑(porosity↓) + SE percolation 망 보강**으로 대응.
즉 우리계에서 "전해질부족 = SE 부피분율·연결성 부족" → **우리 porosity·f_perc·σ_ionic 망이 바로 이 메커니즘**.

### 6.3 ★★★ 바인더 VISCOPLASTICITY → 우리 E3 `--coh` + #285 점탄성 spring-back gap (이 논문 THE 가치)

**우리 MPM의 한계(audit ⚠#10 / #285 (c) / `mpm3d_compaction.py:636-642`):**
- 우리 MPM = **rate-independent von Mises J2** → **시간축·점성·속도의존 전무**.  `--protocol hold`의 relax는
  ~40 substep **순간 settling** → **구조적으로 시간의존 spring-back 재현 불가**(#285의 RT 3주 +4µm vs HT +1µm).
- 우리 `--coh`(binder cohesion, E3) = **시간무관 정적 cohesion**(끌림력) — 점성/속도/cycle 의존 없음.
- 우리 `additives.py` CBD = **기하/부피/전자블로킹만**(역학 없음).

**Song 2025가 제공하는 published 정식(우리가 가져올 것):**
- ★ **Perzyna 점소성(식25,30): ε̇_vp = A·⟨f/σ_y⟩ᵇ·∂f/∂σ** — **시간의존 점소성 흐름**(λ̇가 항복초과량 함수).
  ⇒ 우리 MPM에 **점탄성/점소성 요소**를 넣는 정확한 정식: **A(변형률속도)·b=1 → rate-stiffening**.
- ★ **Ludwick 경화(식28): σ_y = σ_y0 + k·(ε̄_vp)ⁿ**(n=2) + **cycle 누적 경화**(5 cycle yield 24→42.10 MPa).
  ⇒ 우리 `--coh`를 **단조 정적값이 아니라 누적 점소성변형의 함수(경화)**로.
- ★ **바인더 측정 파라미터(Table 3):** E 1.05 GPa, σ_y 19.36 MPa, Perzyna A 0–3×10⁻³ s⁻¹, Ludwick k 1100–1200
  MPa, n=2, b=1 → **우리 MPM 바인더 점탄성 요소의 직접 캘리브 후보**(단 PVDF, 액체 LIB — 값 자체는 우리 ASSB
  바인더와 다를 수 있음, **정식·구조만 전이**).

**구현 경로(향후, DISCUSS — solo 결정 금지):**
1. ⚠ **Stage-2(transport)엔 불필요** — spring-back·점소성은 **as-compacted 정적 종점 transport에 영향 없음**
   (audit #10 판정: 범위 밖, Phase-4+).  우리 정적 압축 종점은 옳게 줌.
2. **Phase-4/장기거동에서 후보:** MPM에 **점탄성 요소(SLS = Maxwell+병렬스프링, 또는 Perzyna 점소성)** + **A(T)·
   E(T) DMA 캘리브** 추가 → #285의 DMA tan δ·3주 두께회복 + 이 논문의 Perzyna A·5cycle yield 진화가 **이중
   검증 앵커**.  → CLAUDE.md "springback validation pending"의 해소 경로.
3. **E3 `--coh` 점성화:** `--coh`를 **(i) 누적변형 의존 경화(Ludwick) + (ii) 변형률속도 의존(Perzyna A)**으로
   확장 → #264(SBR 가교 modulus, 비단조 cap) + #271(PTFE void억제) + **이 논문(Perzyna+Ludwick 정식)**의 3입력원
   수렴.  ⚠ **바인더 modulus(MPa) ≠ SE E_eff(1.53 GPa)** 별개 항(#264 (B) 일관).

⭐ **이 논문이 #285보다 가치 있는 점:** #285는 점탄성 spring-back을 **현상(DMA tan δ·두께회복)으로 측정**만
하고 정식을 안 줌.  이 논문은 **Perzyna+Ludwick 완전 정식 + 측정 파라미터 + 검증(89–97%)**을 줌 → **#285의
"무엇을(현상)"에 이 논문이 "어떻게(정식)"를 더함** → 우리 MPM 점탄성 요소의 **직접 구현 가능 published 레시피**.

### 6.4 frame[5] — 우리 edge (over-claim 금지)

| 그들 우위 | 우리 우위 |
|---|---|
| ★ **structure-resolved 전기화학**(voxel PDE, homogenization 회피) — 우리 PyBaMM은 effective 주입 | ★ **공정→미세구조 예측**(압력·조성→구조; 그들은 FIB-SEM 재구성 = 줘야 함) |
| ★ **electrochemo-mechanical 양방향 결합**(Li-strain→반응면적 피드백) | ★ **granular 점접촉 constriction σ**(Kirchhoff/Holm; 연속체 voxel은 σ_contact-free 상한만) |
| ★ **바인더 점소성**(Perzyna+Ludwick, 시간/속도/cycle) — 우리 MPM 없음 | ★ **σ triad**(ionic+electronic+thermal; 그들 전자/이온만, 열 없음) |
| ★ **셀전압 >98% 검증**(experimental anchor) | ★ **소성 SHAPE morphology + void-fill**(그들 활물질=brittle-elastic, CBM=소성; 입자형상 고정) |
| ★ **단일입자 측정 동역학**(i₀/D_s) | ★ **fracture**(Auerbach/Holm; 그들 균열 future work) |
| | ★ **scaling law 예측**(design knobs → σ 직접, Phase-1 완료) |

⇒ **이상 워크플로 = 우리 DEM+MPM이 미세구조 생성/예측 → voxel effective(우리 voxel FV) → 이들식
structure-resolved electrochemo-mechanical(우리 Phase-4 + 바인더 점소성 요소) → 셀전압 검증**.  논문도 자인:
"these models only consider elastic deformation when analyzing CBM … neglecting the plastic deformation"
(기존 한계) → 이 논문이 CBM 소성을 넣음 → **우리는 SE 소성(MPM) + 그들의 CBM 점소성을 합쳐야 완성**.

### 6.5 ⚠ 정직한 전이 경계 (CRITICAL)

- ❌ **셀 전기화학 절대값 전이 ✗:** NMC711 + 액체 LiPF₆ EC:EMC ≠ LPSCl sulfide ASSB.
  - 액체전해질 **t₊≈0.38·대류·농도분극** vs 단일이온 SE **t₊≈1·무대류·접촉저항** → 전해질 방정식(식4–6) 자체가
    다름(우리 ASSB는 SE-network σ_ionic이 지배, 농도분극 minor).
  - 반쪽셀 **Li metal 음극**(과전압 일정 가정) vs 우리 복합양극 전체.
  - **NMC711 비용량 183.5 mAh/g·부피변화 2.4%@1C** ≠ 고Ni NMC811(8% H2→H3).
- ❌ **"과량전해질(excessive)" 설계 = ASSB 직접 안 통함**(SE 고정부피) → SE 부피분율↑로 번역 필요.
- ❌ **E_AM 2.611 GPa·E_CBM 1.05 GPa·바인더 파라미터 = 액체 LIB 측정값** — 우리 LPSCl 22 GPa SE-modulus 앵커와
  **무관**(이건 oxide AM·PVDF 바인더, sulfide SE 아님).  **정식(Perzyna/Ludwick/Fick/Ohm/BV)만 전이, 수치 ✗.**
- ✅ **전이 가능:** **(a) 방법론**(미세구조→structure-resolved electrochemo-mechanical→셀전압 검증 워크플로),
  **(b) 3메커니즘 분해 프레임**(반응면적/확산길이/전해질부피 → 우리 coverage/τ/porosity), **(c) 바인더 점소성
  정식**(Perzyna+Ludwick 구조 — E3/#285 gap 후보).  **수치 σ/porosity 앵커는 Bazzoun/Varkey/Minnmann/#266/#271.**

---

## 7. 우리 모델에 넣을 인사이트 — 실행 우선순위

| 순위 | 인사이트 | 우리 hook | 상태 |
|---|---|---|---|
| 1 | ★★★ **3메커니즘(반응면적↓/확산길이↑/전해질↓) = 우리 coverage/τ/porosity** | **Phase-4: 우리 미세구조 metric → PyBaMM 반응면적·τ 보정 → 셀전압**(published 분해 프레임) | 📋 Phase-4 결합 프레임 채택 (stage4 §7 #281과 병기) |
| 2 | ★★★ **바인더 Perzyna+Ludwick 점소성 정식** | **MPM 점탄성/점소성 요소 + E3 `--coh` 점성화**(시간/속도/cycle) → #285 spring-back gap 해소 정식 | 📋 Phase-4+ (DISCUSS, solo 금지; Stage-2 무영향) |
| 3 | ★★ **structure-resolved(voxel PDE, homogenization 회피)** | 우리 PyBaMM effective 주입의 한 단계 미세 버전 — 핵심전극 실구조·보조 Bruggeman(#281 ①) | 📋 Phase-4 정밀도 옵션 |
| 4 | ★ **유효 ASA 61.76%(38% dead)** | 우리 coverage·active-fraction의 셀-수준 의미 정량 — PyBaMM `a=3ε_s/R_p`를 우리 유효 coverage로 보정 | 📋 Phase-4 반응면적 보정 |
| 5 | ★ **CBM 전류밀도 ≫ 활물질 1000%+** | 우리 carbon-network σ_e(CBD가 전자전도 carry) 정합 — frame 무영향, 확증 | ✅ 정합 확인 |
| 6 | ⚠ **바인더 dried-film 측정(swelling 미반영)** | 우리도 동일 한계(전해질-impregnated 바인더 물성 미측정) — 공통 GAP 명시 | 📋 honest gap |

---

## 8. 한 줄 verdict

> **Song 2025(EES, Yonsei DTBL + Juner Zhu)는 우리 Phase-4의 sibling published 버전이자 우리 MPM이
> 구조적으로 없는 한 조각을 채운 모델 — FIB-SEM 재구성 미세구조에 전성분 고유물성을 직접 부여해
> homogenization 없이 셀전압을 >98% 재현하고, 입자↔셀 괴리를 우리 transport triad와 1:1 대응하는
> 3메커니즘(반응면적↓=coverage/ASA, 확산길이↑=tortuosity, 전해질↓=porosity/SE-vol)으로 분해하며, 우리
> rate-independent J2 MPM이 못 하는 시간/속도/cycle 의존 바인더 점소성을 Perzyna+Ludwick 완전 정식으로
> 제공한다(E3 `--coh` 점성화 + #285 spring-back gap의 직접 구현 레시피).  ⚠ NMC+액체 LIB라 셀 절대값은
> 전이 ✗ — 가져오는 건 방법론·3메커니즘 프레임·바인더 점소성 정식뿐이며 σ/porosity 수치앵커는
> Bazzoun/Varkey/Minnmann/#266/#271이 유지한다.**

---

## 9. cross-ref
- **Phase-4 결합:** `docs/stage4_electrochem_research.md` §6(plan)·§7(#281 결합 레시피) — 이 #17은 #281의 **structure-resolved
  NEXT 단계** + 3메커니즘 분해 프레임.
- **바인더 점소성 / spring-back:** `docs/stage2_model_audit_vs_literature.md` ⚠#10(rate-indep J2 spring-back 범위밖)·
  #7(#285 점탄성)·E3(`--coh`) — **읽기만, 편집 금지**.  이 논문 = #285("무엇을") + Perzyna/Ludwick("어떻게").
- **positioning:** `docs/positioning_vs_geodict.md` — 그들 미세구조 = **FIB-SEM 재구성(top-down/reconstruction)** 또;
  가치는 구조생성이 아니라 **electrochemo-MECHANICAL 결합 + 바인더 점소성**.  우리 = bottom-up/formation(공정예측) + 접촉망 σ.
- **DTBL 리스트:** `docs/literature_yonsei_dtbl_2026.md` TIER-1 신규(#17, 2025 EES).
- **sibling 디제스트:** `docs/lit_kim2026_a3d_air_electrode_microstructure_transport.md`(#281, Phase-4 결합)·
  `docs/lit_hong2026_cbd_viscoelasticity_springback.md`(#285, spring-back gap)·`docs/lit_park2026_thiolene_sbr_binder_assb.md`
  (#264, E3 cohesion)·`docs/lit_oh2026_bimodal_composite_cathode.md`(#266, 우리 LPSCl 소재계 σ 앵커).
- **앵커(절대 σ/porosity, 이 논문 아님):** Bazzoun + #271 + #266(LPSCl EIS) · Varkey(halide) · Minnmann(pure-SE 10%@300MPa).
