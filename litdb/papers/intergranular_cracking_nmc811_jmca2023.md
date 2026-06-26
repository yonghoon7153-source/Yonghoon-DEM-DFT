# Direct observations of electrochemically induced intergranular cracking in polycrystalline NMC811 particles — Parks et al. (J. Mater. Chem. A 2023)

> slug `intergranular_cracking_nmc811_jmca2023` · DOI `10.1039/d3ta03057a` · type `exp (operando-style ex-situ X-ray nano-CT) + phase-field FEM` · PDF `IntergranularCracking_NMC811_2023_JMCA_d3ta03057a.pdf` · digested `2026-06-26` · status ✅
>
> ## ★★★ 우리 랩 degradation-map의 *결정성(crystallinity) 축*에 대한 — *직접 실험 증거* (DIRECT OBSERVATION) ★★★
> 저자 = **Huw C. W. Parks, Adam M. Boyce, Aaron Wade, Thomas M. M. Heenan, Chun Tan, Emilio Martínez-Pañeda,
> Paul R. Shearing, Dan J. L. Brett, Rhodri Jervis\*** (UCL Electrochemical Innovation Lab + The Faraday
> Institution + UCD + Univ. of Oxford).  **J. Mater. Chem. A, 2023, 11, 21322–21332** (Received 2023-05-23,
> Accepted 2023-09-11; Open Access, CC-BY).
>
> > ★ **우리에게 왜 중요한가 (3줄):** (1) **다결정 NMC811 2차입자가 사이클(충전 4.5 V) 중 *입계 균열(intergranular
> > cracking)*을 일으킨다는 것을 같은 입자의 *pristine→charged* 직접 비교로 못 박은 논문** — 우리 랩 degradation-map의
> > "**다결정은 깨지고 단결정은 견딘다**" 결정성 축(Jung2023 SC vs PC)의 *직접 실험 anchor*. (2) **균열 driver =
> > 양극활물질 *내부* (intercalation 변형 + c-격자 collapse) 의 *비등방 격자변형*** (random orientation의 1차입자가
> > 비대칭 팽창/수축 → 입계에 인장응력) → 우리 **압밀 Auerbach(접촉응력 driver)와 *다른 driver*** 인 *사이클* 파괴를
> > 명확히 분리해주는 표준 케이스. (3) 균열이 **입자 *중심*에서 시작해 *반경방향*으로 전파**(separator 쪽이 더 심함) →
> > 우리 fracture→tortuosity↑→transport↓(B6) 의 *공간 패턴* 실험 근거이자, 우리 σ_e Trevisanello NCM(r) GB-밀도
> > 보정항이 *전제하는 입계 약점*의 미세구조 증거.
>
> > ⚠ **이 논문은 *우리 랩(Hanyang Lee 그룹) 논문이 아니다*** — UCL Shearing/Brett/Jervis 그룹 (+ Martínez-Pañeda
> > phase-field).  하지만 **frame[4] 외부 실험 anchor**로서 우리 랩 자체논문(Jung2023 SC-vs-PC, Kang2025 size-crack)이
> > *정성적*으로 보인 "다결정 입계균열"을 *정량·직접관찰*(X-ray nano-CT, 같은 입자 before/after)로 확정한다.  소재는
> > **NMC811 (= 우리 production CAM)** 로 정확히 일치(단 *cell* 은 LIB 액체전해질 — ASSB 아님, §10 주의).

---

## 1. 한 줄 요약
**상용 NMC811 전극(NMC811:carbon:PVDF=90:5:5, 액체전해질 LIB)을 4.5 V까지 충전**한 뒤, **lab X-ray nano-CT로
*같은* 다결정 NMC811 2차입자를 pristine→charged 두 번 비파괴 영상화**하여, **제조-유발 균열과 *전기화학-유발* 균열을
처음으로 분리**해 관찰했다.  결과: **충전(delithiation) 중 2차입자는 평균 +19 %(최대 +28 %) *부피팽창* 하고, 입자
*중심*에서 시작해 *반경방향*으로 전파되는 *입계 균열(intergranular cracking)* 이 발생** — 균열은 입자 *중심*에 집중(반경
바깥으로 갈수록 약해짐)하며 separator 쪽 입자가 current-collector 쪽보다 더 심하다.  ★ **이 부피팽창(+19 %)이
*결정학적 단위격자 부피변화(−5 %, a-격자 수축)와 정반대*** 라는 점이 핵심 발견 — 팽창은 단위격자가 아니라 *입계가 벌어져
생긴 공극(crack void)* 때문이며, 평균적으로 부피증가의 ~92 %(분할가능 균열 기준 best-case ~70 %)가 균열로 설명된다.
동반한 **chemo-mechanical phase-field FEM**(COMSOL, AT2, Voronoi 400 1차입자, E_p=150 GPa)은 **균열이 ~4 V·c-격자
변형 0.015 에서 입자 *중심*에 발생** → c-격자가 ~0.55 lithiation 에서 최대 → **4.1 V 이상에서 c-격자 collapse(단위격자
수축) → 입계 인장응력 급증 → damage 급상승**이라는 메커니즘을 재현한다.  driver = **random하게 배향된 1차결정의
*비등방(transversely isotropic) 격자변형* → 입계에서 응력 집중**.

> ★ **주의 — 이 논문은 압밀 porosity·전달 σ·Heckel·배위수를 측정하지 않는다** (X-ray CT 균열정량 + 부피팽창 +
> phase-field 응력/damage 가 정량 앵커).  porosity·σ_ionic 칸은 n/a.  우리 압밀/전달 앵커(Minnmann 10/14 %, Bazzoun
> σ 등)와 직접 수치 비교 금지.  이 논문이 우리에게 주는 것은 **(i) 다결정 NMC811 *사이클 입계균열*의 직접 증거,
> (ii) 그 driver(intercalation 변형·c-collapse)가 우리 압밀 Auerbach 와 *다른 축*임의 명확한 분리, (iii) 균열의
> 공간 패턴(중심→반경, separator-편향)** 이다.

## 2. 메타
| 항목 | 값 |
|---|---|
| 저자 | **Huw C. W. Parks**ᵃᵇ, **Adam M. Boyce**ᵃᶜ, **Aaron Wade**ᵃᵇ, **Thomas M. M. Heenan**ᵃᵇ, **Chun Tan**ᵃᵇ, **Emilio Martínez-Pañeda**ᵈ, **Paul R. Shearing**ᵃᵇᵈᵉ, **Dan J. L. Brett**ᵃᵇ, **Rhodri Jervis**\*ᵃᵇ |
| 소속 | ᵃUCL **Electrochemical Innovation Lab**, Dept. Chemical Engineering · ᵇ**The Faraday Institution** (Harwell) · ᶜUniv. College Dublin, School of Mechanical & Materials Eng. · ᵈ**Univ. of Oxford**, Dept. Engineering Science · ᵉZeiss Institute Energy Research, Oxford |
| 저널/년 | **Journal of Materials Chemistry A, 2023, 11, 21322–21332** (Royal Society of Chemistry, PAPER) |
| DOI | 10.1039/d3ta03057a (Received 2023-05-23, Accepted 2023-09-11; Open Access CC-BY; Data DOI 10.5522/04/22120061) |
| 소재 (CAM) | **CAM = 다결정(polycrystalline) Ni-rich layered NMC811 LiNi₀.₈Co₀.₁Mn₀.₁O₂** (NEI Corp, Targray); 14 µm 2차입자 = ~400 submicron 1차입자 응집체 |
| 전극 조성 | **NMC811 : conductive carbon : PVDF = 90 : 5 : 5 wt%** (CBD = carbon-binder domain) |
| 셀 (★주의) | **LIB 액체전해질 half-cell** — 2032 coin cell, **Li metal** 대극, 1 M LiPF₆ in EC:EMC 3:7 + 2 wt% VC, tri-polymer separator(Celgard 2320) + glass-fibre spacer. ★ **ASSB 아님 / SE 없음** |
| 압력 | n/a (액체전해질 coin cell — *압밀-압력 없음*; 전극은 calendared porosity ~30 %) |
| 시험 조건 | **CCCV C/50, RT, → 4.5 V vs Li/Li⁺**, CV until current < C/100; 이론용량 0.5 mA cm⁻² 기준. 1회 충전(half-charge state 비교) — *사이클링 반복 아님*, pristine vs *single charge* |
| 연구유형 | **실험** (lab X-ray nano-CT 같은-입자 ex-situ before/after; "operational-style") **+ chemo-mechanical phase-field FEM**(COMSOL, AT2 phase-field fracture, Voronoi 다결정) |
| 비교군 | **같은 입자**의 pristine(lithiated) vs charged-4.5V(delithiated) 두 상태 (입자 #1–8 + 총 15개 정량); 제조-유발 균열(없음) vs 전기화학-유발 균열(생김) |

> ★ **이 논문의 *방법론적* 1st**: "같은 *2차입자 전체*"를 (FIB-SEM처럼 *반으로 잘라* residual stress 를 풀어버리지
> 않고) **비파괴 X-ray nano-CT로 charging 전·후 두 번 영상화** → 제조 균열과 전기화학 균열을 *명확히 분리* 한 첫 상용
> 전극 사례.  laser-milled tab geometry(80×250 µm 돌출부)로 limited-FoV nano-CT 의 *같은 RoI* 재추적.

## 3. 핵심 물성 (수치)

> 데이터 CSV → `docs/data/intergranular_cracking_nmc811_2023.csv` (crack onset·c-strain·부피팽창·8입자 per-particle
> 표·crack volume/area·제조균열 baseline 전부).

| 물성 | 값 | 조건 | stated/digitized | 비고 |
|---|---|---|---|---|
| **균열 개시 전압** | **~4.0 V** | phase-field FEM, C/50 (Fig 5e-i) | stated | ★ 대부분 균열이 입자 *중심*에서 ~4 V 에 *개시* |
| **균열 개시 c-격자 변형** | **0.015** | c-strain at crack initiation (Fig 5d) | stated | ★ Griffith 균열 시작점 = c-strain 0.015 |
| **c-격자 변형 최대** | **~0.55 lithiation** 에서 peak | 충전 진행 (Fig 5e-ii) | stated | c-strain 최대 → 이후 collapse |
| **c-격자 collapse 개시** | **>4.1 V** | drastic c-격자 수축 (intro) | stated | collapse → bulk 수축 → damage 급상승(Fig 5e-iii) |
| **delithiation 임계** | **4.5 V → >85 % delithiation** | CCCV C/50 (Märker ref) | stated | "significant cracking 보장" |
| **균열 유형** | **intergranular (입계)** | X-ray CT + phase-field | stated | ★ 입계 따라; *transgranular(결정 관통)은 거의 없음* |
| **균열 위치** | **중심 집중 → 반경방향 약화** | Fig 3m, Fig 4 GREAT | stated | ★ separator 쪽 입자 = 큰 중심 void; CC 쪽 = 작고 분산 |
| **2차입자 부피팽창 (평균)** | **+19 %** | pristine→4.5V, 15 입자 | stated | ★★ *단위격자 −5 %와 정반대* |
| **2차입자 부피팽창 (최대)** | **+28 %** (입자 #5) | pristine→4.5V | stated | |
| **단위격자 부피변화** | **−5 %** (a-격자 수축) | 4.4 V (문헌 ref 2) | stated | ★ 결정학과 *모순* → 팽창은 균열 void 탓 |
| **균열 부피분율 (평균)** | **~9 %** of 입자부피 | greyscale-분할 균열 (Fig 3l) | stated | |
| **균열 부피분율 (최대)** | **16 %** of 입자부피 | (Fig 3l) | stated | |
| **부피증가 중 균열 설명비** | best-case **~70 %** (분할가능); 평균 **92.0 %** | Fig 3k/2 | stated | 나머지 = <124 nm unresolvable 균열 |
| **제조-유발 균열 (사이클 前)** | 전체 입자의 **~1/3** | 문헌 (intro ref 10) | stated | ★ *charging 前 측정입자엔 균열 없음* → 균열은 전기화학 단독 |
| **E_p (1차입자, FEM)** | **150 GPa** (등방 선형탄성, ν=0.3) | phase-field FEM | stated | ★ 우리 E_CAM 140·Kang E_NCA 175 와 같은 계열 |
| **E_c (CBD, FEM)** | **0.3 GPa** (ν=0.3, nano-porous soft) | phase-field FEM | stated | carbon-binder = 매우 연질 |
| **2차입자 직경** | **14 µm** (= ~400 1차입자) | X-ray CT 추출, FEM | stated | per-particle 표 10.2–17.8 µm |
| **pixel size** | **~124 nm** | Zeiss Xradia 810 Ultra, Cr 5.4 keV | stated | <124 nm 균열은 unresolvable |
| **σ_ionic / σ_e / σ_thermal / porosity / Z / Heckel** | **n/a** | — | — | ★ 이 논문은 전도도·압밀-porosity·배위수·Heckel 미측정 |

### per-particle 정량 (Fig 2 + Fig 3, 8 highlighted) — CSV에 전부
| 입자 | D pristine→charged (µm) | V pristine→charged (µm³) | %ΔV | dist. from CC (µm) | crack V (µm³) | crack SA (µm²) | %ΔV due to crack |
|---|---|---|---|---|---|---|---|
| #1 | 17.8→19.4 | 2935→3822 | **+23.2** | 64.4 | 641 | 2723 | 72 |
| #2 | 13.8→15.2 | 1365→1820 | +25.0 | 63.5 | 247 | 1115 | 54 |
| #3 | 16.0→17.1 | 2135→2600 | +17.9 | 56.5 | 262 | 1313 | 56 |
| #4 | 16.1→17.0 | 2185→2565 | +14.8 | 55.6 | 144 | 697 | 38 |
| #5 | 12.6→14.0 | 1040→1450 | **+28.3** (max) | 58.0 | 170 | 864 | 41 |
| #6 | 12.1→13.0 | 927→1132 | +18.1 | 48.0 | 63 | 363 | 30 |
| #7 | 12.3→12.9 | 978→1132 | +13.3 | 31.6 | 106 | 615 | 71 |
| #8 | 10.2→10.9 | 558→669 | +16.6 | 38.8 | 80 | 473 | 72 |
> ★ Fig 3k 헤더 = "Mean = 92.0 %" (15 입자 평균 %ΔV-due-to-crack).  Fig 3l = 균열 부피분율 평균 ~9 %, 최대 16 %.
> per-particle %ΔV-due-to-crack 은 30–72 %로 분산(분할가능 segment 기준; 나머지 = sub-124 nm) → "평균 92 %"는
> *segmentable + line-thickness 추정* 합산.  ⚠ **distance-from-CC vs %ΔV 상관 = R²=0.49 (Fig S2), *통계적 유의
> 아님*** (15 입자, 매우 느린 C/50 + 낮은 loading 탓) → "separator 편향"은 *경향(trend)*으로만, 강한 정량법칙 아님.

## 4. 시뮬레이션 방법 ★

> ★ 이 논문은 *실험(X-ray nano-CT)이 주(主)*, **phase-field FEM 이 해석 보조**.  우리 DEM/MPM 과 대응되는 부분은
> §4-B 의 phase-field 다.  DEM/RNM/Kirchhoff/Holm 전달솔버·MPM-J2·압밀 cap 어느 것도 없음 — 이 모델은 *사이클
> chemo-mechanical 취성 파괴* 다 (우리 압밀 소성과 frame[5] *상보*, *시간축* 다름).

### 4-A. 실험 (핵심) — lab X-ray nano-CT 같은-입자 ex-situ before/after
- **장비 / 영상**: **Zeiss Xradia 810 Ultra** lab nano-CT, 회전 **Cr source, quasi-monochromatic 5.4 keV**,
  **parallel-beam + Fresnel zone plate** 집속.  2× binning, **~124 nm pixel**, FoV **64×64 µm**.  radiograph
  15–30 s (검출기 카운트 ~2500), 한 스캔 **1601 projection**, 총 ~24 h(이동 포함).
- **limited-FoV → 전극 두께 전체 stitch**: 한 SoC 스캔 = 2개 FoV(current-collector 계면 1 + separator 계면 1,
  중간 ~50 % overlap) 를 수평 stitch → 전극 두께 전체.  laser-milled **tab geometry(80 µm×250 µm 돌출부)** 로
  limited-FoV 에서 *같은 RoI* 재추적 가능 (Tan 2020 / Heenan 의 rapid nano-CT 시료법).
- **프로토콜**: pristine 영상 → 건조(100 ℃ vacuum) → 2032 coin cell 조립(Li 대극, LiPF₆ EC:EMC + VC) →
  **CCCV C/50 → 4.5 V**(>85 % delithiation, Märker) → 분해 → **같은 RoI 재영상** (charged-4.5V).  → 같은 입자
  *before/after* 직접 비교.
- **입자 분할**: Avizo V2020.2, **Otsu thresholding** + 수동 보정으로 입자별 segment(particle boundary 내 voxel만);
  pristine·charged 둘 다 label.  균열상은 NMC상에서 **별도 thresholding 으로 분리** → binarise → label analysis →
  **Auto-Skeleton**(edge-erosion centreline) → spatial graph(거리맵, segment별 부피·path radius).
- **GREAT 알고리즘**: GReyscale Erosion Algorithm for Tomography (Wade) — 균열 빠른 검출/heterogeneity 정량.

### 4-B. phase-field chemo-mechanical fracture FEM (해석 보조) — ★ 우리 MPM/FEM 대응부
- **code**: **COMSOL Multiphysics v6.0**, 3D tomography-기반 메시.  **~4 M elements, 13 M DOF**, MUMPS 직접해.
  2nd-order backward Euler 시간적분 + time-step sensitivity.
- **기하 / 입자 처리** ★:
  - **14 µm 2차입자를 X-ray CT 에서 추출 → Rhino Grasshopper 로 randomised Voronoi 400 1차입자** tessellation
    (다결정 골격).  carbon-binder 표현 위해 **직경 20 µm shell** 을 입자 주변에 배치.
  - ⇒ **진짜 SHAPE 변형(소성 흐름)이 아니라** — **1차입자는 *고정 형상*의 등방 선형탄성(E_p=150 GPa, ν=0.3)**,
    변형의 본질은 **(i) 비등방 intercalation 변형 + (ii) 입계 phase-field damage(취성 파괴, φ=0 uncracked→1 cracked)**.
    우리 MPM(연속체 *소성 형상* J2 흐름, 연성)과 *다른 종류*: **그들 = 취성 균열(Griffith/AT2 phase-field)** ↔
    우리 = 연성 소성 void-fill.  Kang2025 의 cohesive-zone 과도 다름: **Kang = cohesive-zone(traction-separation
    bilinear) damage**, **이 논문 = phase-field(연속 damage variable φ, mesh-objective AT2)** — 둘 다 *사이클 취성*
    이지만 *수치 표현*이 다르다(phase-field 가 임의 균열 패턴·branching 을 mesh 의존성 없이 표현).
  - 1차입자는 **transversely isotropic**(ε_a ≠ ε_c, Xu et al. 의 격자상수 측정에서) 으로 lithiation 변형 인가;
    그 방향을 **random angle 로 회전**(realistic 다결정 표현) → 인접 결정과 *비대칭* 팽창/수축 → 입계 응력.
- **지배방정식 (ESI)**:
  - **Butler-Volmer** 계면 kinetics (single-particle 모델; 전해질 미고려 = C/50 느린 충전이라 적절).
  - **고상 확산**(intraparticle Li) + **확산-유발 변형**(intercalation strain; transversely isotropic ε_a/ε_c).
  - **Griffith 변분(variational) 파괴 (AT2)**: 총에너지 변분 → phase-field **φ**(1=완전균열·0=무손상),
    damage degradation 함수 **g = (1−φ)²** (E′ = g·E, nominal→effective 강성 감소).  phase-field length scale
    **l** = fracture process zone 크기 → AT2 재료강도 관계.
  - **입계 vs bulk 파괴 toughness 구분**: 보조변수 **γ**(γ=1 입계 *fracture toughness*, γ=0 1차입자 *bond*)
    + 보조 미분방정식으로 γ 분포 → **h=(1−γ)²** diffuse transition 으로 입계와 bulk 의 *다른 파괴에너지* 표현.
    ⇒ **입계가 bulk 보다 약하게(낮은 toughness) 설정** → 균열이 입계를 따라가도록(intergranular) 물리적으로 유도.
  - damage **irreversibility**(history field) 강제 (균열 비가역).
- **하중**: **충전(delithiation) volume change** (사이클 driver). ★ **압밀-press 하중 아님** — Kang2025 의
  `n·σ=−P_app` 같은 *외부 가압* 항이 *없다*(액체전해질 single-particle, 자유 표면).  driver 는 *순수 intercalation
  변형*.  → 우리 압밀-응력(제조 press) 관점과 *완전히 다른 하중축*.
- **MPM/DPC/cap / 전달솔버 / RNM**: **없음** (사이클 chemo-mech 취성파괴 only; 압밀 소성·전달 σ 미산출).
- **특이사항**:
  - **단일 입자(single particle) 모델** — 전극 스케일 농도구배(separator vs CC) 미포함 → C/50 느린 충전에서
    intraparticle delithiation 이 *균일*하다고 가정 (그래서 모델은 균열이 *더 균질하게* 발생 → 실험의 강한 *중심
    집중*을 부분만 재현, §아래 한계).
  - **모델이 *재현 못 하는* 2현상**(본문 명시): (i) 입자 *중심*의 큰 void, (ii) 13–25 % 부피팽창 — 둘 다
    **제조시 주입된 잔류응력(고온 sintering 중)** 탓으로 추정(future work: thermally-induced residual stress 포함).
  - **CBD/입자 계면 박리(delamination)** 는 모델에 *미포함*(가능하나 adsorption CT 로 CBD 분해 어려움; Singh-Pal
    2022 처럼 가능은 함).

## 5. Figure set ★
| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| **1** | (a,b) **같은 RoI 전극 volume rendering: pristine(파랑) vs charged-4.5V(빨강)** — current collector/separator 양 계면. (c) **충전 프로파일(C/50 → 4.5 V, ~54 h, nano-CT 두 시점 표시)**. (d,e) separator/CC 쪽 대표 ortho-slice (pristine vs charged) | ★★ "**같은 입자 before/after**" 직접관찰의 핵심 그림 = 우리 fracture 검증의 *gold-standard* 영상. charged 에서 균열 = X-ray 저감쇠(저밀도) |
| **2** | (a) merged 전극 rendering(분석입자 주황·기타 파랑·CC 흰색). (b–i) 입자 #1–8 위치. (j–q) **charged 입자 *균열 surface rendering*(노랑)**. (i–vii)+(1–8) pristine/charged ortho-slice. **표: D·dist-from-CC·V·%ΔV (8입자)** | ★ per-particle 정량 표(우리 CSV). #5 +28.3 % 최대. **부피팽창과 균열의 직접 연결** |
| **3** | (a,b) 입자1 ortho(pristine vs charged). (c–j) **8입자 skeletonised 균열망**(색=mean path radius, 선두께=부피). **표: crack volume/SA/%ΔV-due-to-crack**. (k) **%ΔV-due-to-crack 막대(Mean=92.0 %)**. (l) **균열 부피분율(평균 9 %·최대 16 %)**. (m) **입자1 split rendering: 균열(빨강)이 *중심*에 집중** | ★★ **균열이 입자 *중심*에 산다**(Fig 3m) = 우리 fracture→tortuosity 의 공간패턴. skeleton 정량(부피·SA·path radius) = 우리 균열 metric 대응 |
| **4** | **GREAT 분석**: (a) 다른 cracking 프로파일 입자 ortho(P3 vs P11). (b) **through-thickness 최소-정규화-강도 vs dist-from-CC**(separator=least cracked, CC쪽 most? — 실제는 그래프상 *분산*, R²=0.49). (c) **반경분포 pixel-강도 plot(균열=빨강·무균열=파랑, pristine vs charged-4.5V; P3 vs P11)** | ★ 균열의 *반경* 분포 정량(중심=빨강 균열). through-thickness 경향 = separator-편향이나 *약한 상관* |
| **5** | **phase-field FEM**: (a) X-ray CT 추출 단일입자 기하. (b) 400-1차입자 Voronoi mesh(cutout). (c) **모델 vs 실험 전압프로파일 일치**(delithiation). (d) **c/a 격자변형 vs lithiation-state(Xu et al.) + 균열개시(i)/전파(ii)/collapse(iii) 표시**. (e) **damage variable φ 맵(4/4.2/4.5 V): 균열이 중심→입계**. (f) **최대 주응력 맵(GPa): 입계 인장**. | ★★ **메커니즘 그림**: c-strain 0.015 @4 V 개시 → 0.55 peak → 4.1 V collapse → damage 급상승. 입계 인장응력 = 우리 GB-약점 전제의 *FEM 증거* |

> ★ **figure 핵심 정리(우리 입장)**: Fig 1·2·3 = *직접 실험관찰*(같은 입자 before/after, 입계균열·중심집중·
> 부피팽창 정량) → 우리 랩 degradation-map 결정성 축의 anchor; Fig 5 = *phase-field 메커니즘*(intercalation
> 변형·c-collapse 가 입계 인장응력 → 균열) → 우리 *압밀* Auerbach 와 *다른 driver* 임을 분명히.

## 6. Post-processing ★
- **무엇**:
  - **X-ray CT 분할 → 균열 정량**: Otsu thresholding 입자 segment → NMC상에서 **균열상 별도 thresholding 분리** →
    binarise → **label analysis(부피·#)** → **Auto-Skeleton(edge-erosion centreline) → spatial graph**(segment별
    부피·path radius·거리맵).  ⇒ **crack volume / crack surface area / mean path radius / %ΔV-due-to-crack** 산출.
  - **부피팽창 정량**: pristine vs charged 입자 부피(균열 voxel *포함*) → %ΔV; 균열상을 *별도 상(phase)* 으로
    재분할 → "균열로 설명되는 부피증가 비율"(best ~70 %, 평균 92 %).  **<124 nm 균열은 partial-volume(두 상 혼합
    voxel 강도저하)** 로 *간접* 보정 → 잔여 부피증가에 귀속.
  - **GREAT (GReyscale Erosion Algorithm for Tomography)**: 균열을 빠르게 검출 + **through-thickness 최소-강도**
    (dist-from-CC) + **반경 pixel-강도 분포**(중심=균열) heterogeneity 정량.
  - **phase-field 후처리**: damage φ 맵, 최대 주응력(GPa) 맵, c/a 격자변형 vs lithiation, 모델-실험 전압 일치.
- **도구**: **Avizo V2020.2**(segment·label·skeleton), **GREAT**(자체, Wade), **Rhino Grasshopper**(Voronoi),
  **COMSOL v6.0**(phase-field FEM).
- **수치화·기록**: per-particle 표(D·V·dist·crack V/SA/%due-to-crack, 8입자) + 15-입자 평균(부피팽창 19 %·균열분율
  9 %·%due-to-crack 92 %) + phase-field 임계(c-strain 0.015 @~4 V).  ⚠ **정량값 = 본문/표 stated**; through-thickness
  상관 R²=0.49 = *유의 아님*(통계오차, 15 입자) → *경향만*.

## 7. 우리 DEM+MPM 대비  →  `our_dem_baseline.md`

> ★ 이 절은 §A(우리 DEM+MPM 대비)에서 상세히.  요약: 이 논문은 **사이클(전기화학) intergranular 균열의 직접 실험
> 증거** 이고, 우리 DEM Auerbach 는 **압밀(제조 press) 접촉응력 균열** — **driver·시간축이 다르다**.

| 항목 | 이 논문 (Parks 2023) | 우리 DEM+MPM | 차이 / 이유 |
|---|---|---|---|
| **현상** | **사이클 입계균열**(직접관찰, 같은입자 before/after) | 압밀 Auerbach 균열(f_intact, frac_severe) | ★ **driver 다름**: 그들=intercalation 변형·c-collapse / 우리=press 접촉응력 |
| **소재** | **NMC811 다결정** (= 우리 production CAM) | NMC811 (AM_P 다결정·AM_S 단결정) | ★ **정확히 같은 CAM** — 단 cell 은 LIB 액체전해질(ASSB 아님) |
| **균열 driver** | **비등방 격자변형 + c-collapse → 입계 인장** | 접촉응력 집중(Auerbach P_c ∝ K_IC²/E) | ★ *다른 물리* — 사이클 vs 압밀 |
| **모델 종류** | phase-field FEM(취성, AT2, Voronoi) | DEM(Auerbach 강체-구) + MPM(J2 소성) | ★ 그들=취성 phase-field / 우리=강체-구 DEM + 연성 MPM |
| **공간패턴** | **중심→반경, separator 편향**(약상관) | 접촉점 응력 집중(force chain) | ★ 그들 패턴 = *intraparticle* / 우리 = *interparticle 접촉* |
| **transport 연결** | 부피팽창·균열 → (암시적) tortuosity↑ | σ 삼중항(Kirchhoff)·f_intact→σ↓ | ★ 그들 σ 미산출; 우리가 *수치 연결* |
| **결정성** | **다결정만**(SC 미비교; "SC는 future work") | AM_P(다결정 균열↑)/AM_S(단결정 견딤) | ★ 그들=다결정 직접증거; SC 대비는 Jung2023 |

## 8. 적용 인사이트 (내 연구에 어떻게)
- ① **우리 랩 degradation-map *결정성 축*의 직접 실험 anchor 로 인용**: "다결정 NMC811 2차입자가 사이클 중 *입계
  균열* 한다"를 *같은 입자 before/after* 로 못 박음 → Jung2023(SC vs PC 정성) + Kang2025(size-crack) 의 "다결정이
  깨진다" 를 *직접관찰·정량*(부피 +19 %, 균열분율 9 %, 입계형)으로 보강. → §A·§적용가능성 참조.
- ② **fracture *driver 분리*를 명문화**: 우리 DEM Auerbach = *압밀 접촉응력*; 이 논문 = *사이클 intercalation 변형·
  c-collapse*. → 우리 문서에 "compaction fracture(우리 DEM) vs cycling intergranular(이 실험)" 두 driver 를 명시
  분리(over-claim 방지) → §C frame[5] 위치.
- ③ **σ_e Trevisanello NCM(r) GB-밀도 항의 *미세구조* 근거**: 입계가 *물리적 약점*(낮은 toughness, 인장응력 집중)
  이라는 phase-field 증거 + 입계균열이 실제로 발생 → 우리 σ_e 의 "다결정 내부-GB = 전달병목·균열시드" 전제의 anchor.
- ④ **fracture→tortuosity↑→transport↓(B6) 의 *공간패턴* 근거**: 균열이 입자 *중심*에 집중·반경전파(Fig 3m) →
  중심 void 가 Li 확산경로를 끊음 → tortuosity↑ → R_w↑(Kang2025 EIS 시그니처와 연결). → B6 의 실험 근거.
- ⑤ **size-effect 정렬(Kang2025 짝, 약함)**: 이 논문은 입자크기 vs %ΔV *유의 상관 없음*(R²=0.49, 매우 느린 C/50
  탓; faster C-rate 면 상관 강해질 것으로 *예상*만) → Kang2025 의 "큰 입자 더 깨짐"을 *C/50 에선 약하게* 본 것.
  → 우리 size-dependent Auerbach(σ_crit ∝ 1/√d) 는 *압밀* 축이고, 이 논문의 size-약상관은 *사이클·저율* 한정 — 직접
  전이 금지, "C-rate 의존"으로 분리(backlog A9).

## 9. 인용 가능 문장 (deck/paper용)
- "Direct, non-destructive X-ray nano-CT imaging of the *same* polycrystalline NMC811 secondary particles
  before and after charging to 4.5 V (Parks et al., J. Mater. Chem. A 2023) attributes the observed
  *intergranular cracking entirely to electrochemical delithiation*, with cracks nucleating in the particle
  centre and propagating radially — providing the direct experimental evidence for the *crystallinity axis*
  of our degradation map (polycrystalline cracks, single-crystal resists), complementing our own group's
  Jung 2023 SC-vs-PC contrast."
- "The secondary particles expand on average +19 % (up to +28 %) on delithiation — *opposite* to the −5 %
  unit-cell volume change — because the expansion is dominated by crack-void opening at grain boundaries
  (crack volume ~9 %, up to 16 %), driven by the anisotropic lattice strain of randomly oriented primary
  crystals (c-strain crack onset 0.015 at ~4 V, c-lattice collapse above 4.1 V)."
- "This *cycling-driven* intergranular cracking (intercalation strain + c-lattice collapse) is the
  experimental counterpart, on a different load axis, to our *compaction-driven* Auerbach fracture
  (press contact stress) — they share the 'polycrystalline secondary particle cracks' phenomenology but
  not the driver."

## 10. 주의/한계 (over-claim 방지)
- **소재는 NMC811(= 우리 CAM) ✓ 이지만 *cell 은 LIB 액체전해질(ASSB 아님, SE 없음)*** → 이 논문에 LPSCl·SE·
  복합양극·압밀-압력·porosity·σ 가 **전혀 없다**.  우리 ASSB 압밀/전달 앵커(Minnmann·Doux·Bazzoun)와 **직접 비교
  금지**.  가져가는 것은 *NMC811 다결정 자체* 의 *사이클 입계균열 거동*뿐.  ⚠ 액체전해질이라 균열면이 *LE 에 노출*
  (gas/금속용출) — ASSB 에선 균열면이 *SE 접촉손실·dead-AM* 로 작동(다른 결과) → 메커니즘 결과를 ASSB 로 *그대로*
  전이 금지(Jung2023 의 LIB↔ASSB 반전 교훈).
- **하중축이 *사이클(delithiation)* 이지 *압밀(press)* 아님** → 그들 phase-field 응력·damage 는 *intercalation
  변형* 하중.  우리 DEM/MPM 의 *압밀 접촉응력* 과 *같은 현상이 아니다*.  "다결정 깨짐"은 공통이나 *driver 가 다름*
  (사이클 격자변형 vs 압밀 접촉응력) — 흡수 시 반드시 분리 명시.  특히 **stack-pressure 항이 *모델에 없다*** (Kang2025
  와 달리 `n·σ=−P_app` 없음) → "압밀 압력"과 무관.
- **phase-field = 취성 균열(AT2)**, Kang2025 = cohesive-zone, 우리 MPM = 연성 J2 소성 — **세 모델 모두 다른
  파괴/변형 표현**.  phase-field φ ↔ 우리 Σdg(소성변형)·Kang damage D 는 *개념* 대응이나 *동일시 금지*(취성 phase-
  field ≠ 연성 J2).
- **single-particle FEM 한계(본문 자인)**: (i) 입자 *중심 큰 void* 와 (ii) 13–25 % 부피팽창을 모델이 *재현 못 함*
  → **제조시 잔류응력(고온 sintering)** 탓으로 *추정*(future work).  ⇒ 부피팽창 +19 % 의 *일부* 는 전기화학이 아니라
  *제조 잔류응력 해방* 일 수 있음 → "전기화학이 +19 % 전부 만든다"고 과대해석 금지(논문도 "matter for future work").
- **separator-편향은 *약상관*(R²=0.49, 유의 아님)** → 15 입자 + 매우 느린 C/50 + 낮은 loading 탓.  "separator 쪽이
  더 깨진다"는 *경향(trend)* 으로만, 강한 정량법칙 아님(논문 명시: "no statistically significant correlation";
  faster C-rate 면 더 뚜렷할 것으로 *예상*).
- **<124 nm 균열 unresolvable** → 균열분율 9 %·%due-to-crack 92 %는 *부분*(segmentable + partial-volume 추정)
  → 절대값 아니라 *하한+추정*.  per-particle %due-to-crack 30–72 % 분산 큼.
- **단결정(SC) 직접 비교 *없음*** → 이 논문은 *다결정만* 관찰.  "SC 는 안 깨진다"의 직접증거는 *이 논문이 아니라*
  Jung2023(SC vs PC) — 이 논문은 결정성 축의 *다결정 절반* 만 채움.  본문 conclusion 도 "SC·SSE 로 확장 = future work".
- **digitized 구분**: 본 digest 수치는 전부 본문/표/Fig 컬러바 *stated* 값(부피·균열·c-strain·전압·E).  through-
  thickness 그래프(Fig 4b) 의 점 분포는 *경향*으로만 읽음(개별 digitized 좌표 사용 안 함).

---

## A. 우리 DEM+MPM 대비 (comparison vs ours)

> ★ **핵심 대비**: 이 논문의 *사이클 intergranular(입계) 균열* (다결정 NMC811, intercalation strain driver) ↔
> 우리 *압밀 Auerbach AM 파괴* (press 접촉응력, σ_crit ∝ 1/√d size scaling) ↔ Jung2023 *단결정-resists / 다결정-
> cracks* (결정성 driver).  세 가지가 우리 랩 degradation-map 의 **결정성 × 크기 × driver(압밀/사이클)** 축을 구성.

### A-1. ★★ 결정성(crystallinity) 축 — 이 논문이 *다결정 절반*의 직접 증거
| 축 | 이 논문 (Parks 2023, 실험·직접관찰) | 우리 모델 / Jung2023 | 연결 |
|---|---|---|---|
| **다결정(PC) 균열** | **NMC811 다결정 2차입자 = 사이클 중 *입계 균열*** (X-ray CT 같은입자 before/after; 부피 +19 %, 균열분율 9 %, 입계형, 중심집중) | 우리 **AM_P(다결정)** = 낮은 P_c·높은 frac_severe; Jung2023 PC = 입계+공극 균열시드 | ★★ **다결정이 깨진다**의 *직접관찰* anchor (Jung/Kang 정성 → 이 논문 정량·직접) |
| **단결정(SC) 대비** | **없음** (다결정만; "SC 확장 = future work") | 우리 **AM_S(단결정)** = 높은 P_c; Jung2023 SC = monolith·무균열 | ★ SC 대비는 *Jung2023*; 이 논문은 결정성 축의 *PC 절반* 만 |
| **균열 = 입계(GB)** | **intergranular**(입계 따라); transgranular 거의 없음 | σ_e Trevisanello NCM(r) = 입자 *내부 GB* 병목·균열시드 전제 | ★★ "입계가 약점"의 *미세구조+phase-field 증거*(γ=입계 toughness 낮춤 → 균열이 GB 따라감) |

→ **결론**: 우리 랩 degradation-map 의 "**다결정 cracks / 단결정 resists**" 결정성 축에서, 이 논문은 **다결정 절반의
*직접관찰 정량 증거*** (FIB-SEM 처럼 *반으로 잘라 잔류응력 풀어버리는* 인공물 없이, *같은 입자* before/after 비파괴).
Jung2023(SC vs PC 대비) + 이 논문(PC 직접관찰) → 결정성 축이 *양쪽* 다 anchor 됨.

### A-2. ★★ driver 분리 — 압밀 Auerbach(우리) vs 사이클 intergranular(이 논문)
| 항목 | 이 논문 (사이클 driver) | 우리 DEM (압밀 driver) | 차이 / 왜 분리해야 |
|---|---|---|---|
| **균열 driver** | **intercalation 변형 + c-격자 collapse** (random 배향 1차결정 비대칭 팽창/수축 → 입계 인장) | **press 접촉응력 집중** (제조 300 MPa, Hertz/Tabor 접촉점) | ★ *완전히 다른 물리* — 하나는 화학(Li 삽입), 하나는 역학(가압) |
| **시간/공정 시점** | **작동(사이클)** 중, 충전 4.5 V | **제조(압밀)** 순간, cold-press | ★ frame[5] *시간축* 분업 (Kang2025 와 같은 구분) |
| **공간 패턴** | 입자 *중심*→반경(intraparticle) | 접촉점·force chain(interparticle) | ★ intra vs inter — *다른 위치* |
| **압력 역할** | ★ **압력 항 *모델에 없음*** (single-particle, 자유표면) | ★ **압력이 주역** (Heckel P_y 138) | ★ 우리 압밀-압력과 *무관* → 전이 금지 |
| **size 의존** | %ΔV vs 크기 *유의 상관 없음*(R²=0.49, C/50 탓) | σ_crit ∝ 1/√d (Auerbach size scaling) | ★ 그들 size-약상관 = *사이클·저율* 한정; 우리 = *압밀* |

→ **결론**: "다결정 2차입자가 깨진다"는 *현상*은 공통이지만, **driver(압밀 접촉응력 vs 사이클 intercalation 변형)·
시간축(제조 vs 작동)·위치(inter vs intra)·압력역할(주역 vs 부재)** 가 모두 다르다.  우리 DEM Auerbach 는 *압밀-시점*
파괴만; 이 논문의 *사이클* 입계균열은 frame[5] *우리 미보유* 영역(§C).  흡수 시 **두 driver 를 절대 섞지 말 것**.

### A-3. 모델링 패럴렐 — phase-field(그들) ↔ MPM-J2(우리) ↔ cohesive-zone(Kang)
| 모델 | 파괴/변형 표현 | 하중 | 소재 |
|---|---|---|---|
| **이 논문 (Parks/Martínez-Pañeda)** | **phase-field AT2**(연속 damage φ, mesh-objective, branching 자유), γ로 입계/bulk toughness 분리, **취성** | 사이클 intercalation 변형 | NMC811 (LIB) |
| **Kang2025 (우리 랩)** | **cohesive-zone**(traction-separation bilinear, damage D 0→1), **취성** 입계 박리 | 사이클 Li deintercalation volume change | NCA (ASSB) |
| **우리 MPM** | **J2 연속체 소성**(누적변형 Σdg), **연성** void-fill 흐름 | **압밀** press | LPSCl SE (CAM rigid) |
→ ★ **셋 다 연속체 + damage/소성 변수** 지만 **(i) 파괴 메커니즘(취성 phase-field/cohesive vs 연성 J2), (ii) 하중축
(사이클 vs 압밀), (iii) 소재(CAM vs SE)** 가 다름.  우리 MPM 은 *SE 압밀 소성 morphology* 를, 이 논문/Kang 은 *CAM 사이클
취성 균열* 을 담당 → frame[5] 분업의 *방법론* 대응.  **phase-field 는 임의 균열 패턴·branching 을 mesh 의존 없이 표현**
(cohesive 의 미리-삽입 0-두께 요소 불필요) → 우리가 *사이클 CAM 균열* 을 미래에 모델한다면 phase-field 가 후보(현재 미보유).

### A-4. E_p = 150 GPa — 우리 E_CAM 앵커 교차확인
- 이 논문 phase-field **1차입자 E_p = 150 GPa**(등방, ν=0.3) → 우리 **E_CAM = 140 GPa**·Kang2025 **E_NCA = 175 GPa**·
  Bazzoun **E_CAM = 161.5 GPa** 와 같은 계열(140–175 GPa).  ⇒ **NMC/NCA CAM 모듈러스 ~140–175 GPa** 가 4편 독립
  cross-check.  우리 DEM 의 rigid-CAM(E 140) 가정은 이 범위 안 — 정당.  ⚠ 단 이건 *1차입자* E(다결정 2차입자의
  *유효* E 는 입계·내부공극으로 더 낮음 — Jung2023 PC 경도 113 MPa 가 그 *bulk* 약화) → 우리 DEM 의 CAM E 는 *2차입자
  유효값* 으로 해석(rigid 가정은 SE 대비 상대적).
- **CBD E_c = 0.3 GPa**(nano-porous soft) → 우리 CBD/binder 모델(매우 연질)·Kang LZO·Lee2025 PTFE 연화와 같은 방향
  (CBD 가 역학적으로 무시할만큼 연질) → 우리 DEM 이 CBD 를 mass-correction 으로 빼는 것(Bazzoun eq2 식) 정당.

---

## B. 적용가능성 (applicability to our model)

> ★ 이 논문은 **실험 anchor** 다 (시뮬 경쟁 아님).  우리 모델에 *직접 코드 변경*보다 **(i) 우리 crystallinity-의존
> σ_e GB 보정과 size-fracture 의 실험 정당화, (ii) fracture→tortuosity→transport 링크(B6)의 anchor, (iii) driver
> 분리의 명문화** 로 적용.

### B-1. ★ crystallinity-의존 σ_e GB 보정(Trevisanello NCM(r)) 의 실험 grounding
- 우리 σ_e 폼은 **NCM(r) = 1/(1+(r_AM/2)^1.5)** (Trevisanello) 로 *입자 내부 GB 밀도*를 보정한다 (다결정=GB 多→σ_e↓,
  단결정=GB-less→σ_e↑).  이 논문은 **입계가 *물리적 약점*** (phase-field γ 로 입계 toughness 를 bulk 보다 낮춰야
  균열이 GB 따라감 + 실제 *intergranular* 균열 관찰) 임을 **직접 보인다** → 우리 NCM(r) 항이 전제하는 "다결정 내부-GB =
  약점·병목" 의 *미세구조+phase-field 증거*.
- ⚠ **단 이 논문은 σ(전도도)를 측정 안 함** → NCM(r) 의 *정량값*(exponent 1.5)을 이 논문으로 fit 금지.  이 논문은
  *정성 방향*(GB 가 약점) anchor 만; 정량은 Trevisanello(원전) + Kim2025(GB 분리측정 R_i,gb≈R_i,bulk).  **포지셔닝**:
  Trevisanello(σ-GB 정량) + Kim2025(σ-GB 분리측정) + **이 논문(GB 균열 직접관찰)** = NCM(r) 항의 3중 grounding.

### B-2. ★ size-dependent fracture(backlog A9) — *압밀* 버전과 *사이클* 버전 분리
- 우리 backlog **A9 = size-dependent Auerbach**(σ_crit ∝ 1/√d; AM_P 큰 다결정일수록 fracture↑).  이 논문은 **사이클**
  맥락에서 size-fracture 를 본다 — 단 **%ΔV vs 입자크기 *유의 상관 없음*(R²=0.49)**, *매우 느린 C/50 + 낮은 loading*
  탓으로 자인하며 "faster C-rate 면 상관 강해질 것"으로 *예상*.  Kang2025 는 (FEM·다른 C-rate) "큰 입자 더 깨짐(c_Li
  구배 10×)" 을 *강하게* 본다.
- → **A9 적용 시 분리**: (i) *압밀* size-fracture(우리 DEM Auerbach, σ_crit ∝ 1/√d, 접촉응력 ∝ 입경) = 우리 주영역;
  (ii) *사이클* size-fracture 는 **C-rate 의존** (저율 C/50: 약상관[이 논문] / 고율·FEM: 강상관[Kang2025]) → 우리 DEM
  *압밀-시점* 모델에는 (i)만, (ii)는 frame[5] 미보유로 명시.  이 논문은 (ii)가 *C-rate 에 민감*하다는 *caveat* 을 준다
  (저율에선 균열이 *더 균질*·size-무관) → A9 의 "size 가 항상 지배" 가정에 brake.

### B-3. ★ fracture → tortuosity↑ → transport↓ (backlog B6) 의 공간패턴 anchor
- B6 = fracture 가 transport 를 깎는 링크.  이 논문은 **균열이 입자 *중심*에 집중·반경전파**(Fig 3m) → 중심 void 가
  Li 확산경로를 *끊는다* → **diffusion path tortuosity↑**.  이는 Kang2025 EIS 의 **R_w(Warburg, ∝ δ_s 확산거리)
  급등**(70→353 Ω·cm², 균열→tortuosity↑) 시그니처와 *직접 연결*된다 (Kang 이 *거시* EIS 로 본 것을 이 논문이 *미세*
  CT 로 본 것).
- → **B6 적용**: 우리 fracture-aware σ(f_intact, frac_severe)가 σ 를 깎을 때, 이 논문이 *균열의 공간패턴*(중심 void)
  을 anchor → "균열 → 중심 void → 확산경로 단절 → R_w↑/σ↓" 인과의 미세구조 근거.  ⚠ 단 이 논문은 *액체전해질·CAM
  내부* 확산; 우리 ASSB σ 는 *SE-SE 접촉망 + AM-SE 계면* → 균열의 transport 영향이 *다른 경로*(ASSB 에선 균열면 SE
  접촉손실 = dead-AM, Jung2023) → *경로* 는 다르되 "균열→transport↓" 방향은 공통(흡수 시 경로 분리).

### B-4. driver 분리의 명문화 (over-claim 방지)
- 우리 문서/deck 에서 fracture 를 다룰 때 **두 driver 를 명시 분리**:
  - **compaction fracture (우리 DEM Auerbach)**: 제조 press 접촉응력, σ_crit ∝ 1/√d, *interparticle* 접촉점, 압력 주역.
  - **cycling intergranular (이 논문 + Kang2025)**: intercalation 변형·c-collapse, *intraparticle* 입계, 압력 부재.
  → "우리가 다결정 균열을 모델한다"고 *뭉뚱그리지* 말 것 — 우리는 *압밀* 버전만; *사이클* 버전은 이 논문/Kang(실험·
  FEM)의 영역 = frame[5] 미보유(§C).

### B-5. ⚠ 직접 코드 적용은 *제한적* — anchor 가 본질
- 이 논문은 σ·porosity·압밀 수치가 *없고* cell 이 LIB 라, 우리 모델 *파라미터 fit* 에 직접 쓸 데이터는 없다.  적용 =
  **(i) 정성 방향 grounding**(GB 약점·다결정 균열·중심void), **(ii) driver 분리 caveat**, **(iii) E_p 150 cross-check**.
  *정량 fit* 은 우리 ASSB 소재계 앵커(Minnmann·Bazzoun·Kim2025·Jung2023)로.

---

## C. frame[5] 위치 (our division)

> ★ 이 논문 = **실험 anchor** (DEM 경쟁자 아님).  frame[5] 분업에서, 이 논문은 우리가 *안 하는* 영역(*사이클*
> chemo-mech 취성 균열)을 *직접관찰*로 드러내며, 우리가 *하는* 영역(*압밀* 구조·전달·접촉응력 파괴)의 경계를 명확히 한다.

### C-1. 우리 시뮬이 *소유*하는 것 (이 논문이 *안 하는* 것)
| 축 | 우리 DEM+MPM | 이 논문 |
|---|---|---|
| **압밀-순간 구조** | ★ P/S 패킹·porosity·Furnas-dip·접촉망 | 안 함(LIB, 압밀-압력 없음) |
| **전달 σ 삼중항** | ★ σ_ionic/e/thermal 정량(Kirchhoff/Holm) | σ 미산출(전도도 측정·해석 없음) |
| **압밀 파괴 역치** | ★ Auerbach P_c·f_intact 정량(*접촉응력* driver) | 안 함(사이클 driver 만) |
| **SE 소성 morphology** | ★ MPM J2 연성 void-fill·Σdg 변형장 | 안 함(CAM 취성, SE 없음) |
| **packing/조성→porosity** | ★ DEM·de Larrard dip | 안 함 |

### C-2. 이 논문이 *드러내는* frame[5] 공백 (우리 *미보유*)
| 축 | 이 논문이 직접관찰 | 우리 상태 |
|---|---|---|
| **사이클 intergranular 균열** | ★ 다결정 NMC811 입계균열(같은입자 before/after) | ⛔ **미보유** — 우리 DEM 은 *압밀* 균열만 |
| **intercalation 변형 driver** | ★ c-strain 0.015@4V·c-collapse@4.1V·비등방 격자 | ⛔ 미보유(우리는 *접촉응력* driver) |
| **사이클 부피팽창** | ★ +19 %(균열 void) | ⛔ 미보유(우리 압밀은 *수축*) |
| **CAM 내부 확산·SoC heterogeneity** | ★ 중심집중·separator 편향(약) | ⛔ 미보유(우리 DEM+MPM 은 *압밀-순간* 만) |
| **phase-field 취성 균열장** | ★ damage φ·주응력 맵 | ⛔ 미보유(우리 MPM=연성 J2; 취성 phase-field 없음) |

### C-3. ★ 분업 명제 (frame[5] 확장)
- **우리 DEM = TRANSPORT(접촉망 σ) + 압밀 packing/porosity + *압밀* 파괴(Auerbach)**.
- **우리 MPM = SE *압밀* 소성 morphology(연성 J2)**.
- **이 논문(+Kang2025) = CAM *사이클* 취성 균열(phase-field/cohesive)** = *우리 미보유* — frame[5] 의 **CAM-사이클-
  역학** 칸을 *실험·FEM* 으로 채우는 외부 anchor.
- ⇒ **이 논문은 "이겨야 할 모델"이 아니라 "우리 결정성·size 파괴 축을 *직접관찰로 정당화*하는 anchor"** 다.  우리
  DEM Auerbach(압밀)가 *interparticle 접촉응력* 파괴를 소유하고, 이 논문이 *intraparticle 사이클 격자변형* 파괴를
  드러내며 — **두 driver 가 *상보*** (frame[4] 외부 실험 + frame[5] 분업).  우리 랩 degradation-map(Yun2023 capstone)의
  "이온수송/기계 축 → 균열 3-driver" 에서 이 논문은 **다결정-CAM-사이클-입계균열** driver 의 *직접관찰 증거* 슬롯.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
