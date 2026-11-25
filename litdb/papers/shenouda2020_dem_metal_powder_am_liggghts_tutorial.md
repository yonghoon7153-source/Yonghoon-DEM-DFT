<!-- digest 표준 양식. ★ = 사용자가 특히 원한 항목. COMPREHENSIVE / paper-level STANDALONE. -->
# 금속분말 AM을 위한 DEM 해석 + LIGGGHTS-PUBLIC 시뮬레이션 튜토리얼 — Shenouda & Hoff (LLNL 기술보고서 2020)

> slug `shenouda2020_dem_metal_powder_am_liggghts_tutorial` · report `LLNL-TR-813736` (DOI 없음, LLNL OSTI 기술보고서) · type `DEM (LIGGGHTS-PUBLIC; AM 분말 흐름/안식각 + 단계별 튜토리얼)` · PDF `Shenouda_Hoff_2020_LLNL_DEM_MetalPowder_AM_LIGGGHTS_Tutorial.pdf` · digested `2026-06-26` · status ✅
> ★ **이 문서 = 우리 DEM 엔진(LIGGGHTS)의 *공개 입문 레퍼런스/튜토리얼* + AM 금속분말 응용**. **경쟁 물리모델이 아니라** (a) LIGGGHTS 명령어·워크플로의 깨끗한 입문서 + (b) AM 분말의 흐름·안식각·feed-rate DEM 응용. 우리에게 가치는 **§B 적용가능성**(우리 input 스크립트와 명령어 1:1 대조)에 집중되며, **§C 우리 novelty 간극이 매우 큼**(전달 σ·소성 morphology·Stage-E·scaffold 전부 없음 — 이건 freefall/안식각 검증 + 튜토리얼이지 ASSB 압밀-전달 모델이 아님).
> ★ **공개성/인용**: LLNL-TR-813736 = U.S. DOE 후원 *Unclassified* 기술보고서(NNSA, Contract DE-AC52-07NA27344). 저자: **Safwat Shenouda**(North Carolina A&T State University 학부 인턴) · 멘토 **Andrew Hoff**(LLNL). 발표일 deck 2020-06-24, 보고서 2020-07-27 / 2020-08-19. **84쪽**: 앞부분(p.1–20)=PowerPoint 슬라이드 캡처, 뒷부분(p.21–84)=서술형 튜토리얼 + 부록(단위표·결과·전체 input 스크립트 3종). **학부 인턴 산출물**이라 깊이는 입문 수준(일부 오타·비정밀 표현 존재 — §10에 명시).

---

## 0. 왜 이 문서가 우리에게 의미 있나 (먼저 읽을 것)

우리 DEM 전체(압밀·porosity·전달 네트워크·Stage-E·f_AM)는 **LIGGGHTS** 위에서 돈다. 이 문서는 그 LIGGGHTS의 **공개판(LIGGGHTS-PUBLIC)을 처음 배우는 사람을 위한 가장 깨끗한 단계별 튜토리얼** + **금속 AM 분말 응용 사례**다. 따라서 이 digest의 핵심 가치는 두 가지로 갈린다:

1. **§B 적용가능성(THE 핵심)**: 이 튜토리얼이 가르치는 모든 명령어(`atom_style`/`boundary`/`pair_style`/`fix wall/gran`/`fix move/mesh`/`particletemplate`/`insert/*`/`dump`/`fix massflow/mesh`/`fix check/timestep/gran`)를 **우리 실제 input 스크립트**(`dem_scripts/thin9_seed.liggghts`, `heckel/input_SE_heckel_300.liggghts`)와 1:1 대조 → 우리가 *빌릴 수 있는* 것(예: `fix check/timestep/gran` 자동 안정성 점검, `fix massflow/mesh` 유량, Rayleigh-timestep 공식)을 정확히 식별.

2. **§C 우리 novelty(매우 큰 간극)**: 이 문서는 **금속 AM 분말의 *흐름/패킹/안식각/feed-rate*** (DEM 역학 절반)만 다루고, **전달 σ(이온/전자/열)·소성 SHAPE morphology·Stage-E 소성접촉면적·DEM↔MPM scaffold·fracture·scaling-law predictor 전부 없다**. 게다가 검증 케이스가 **자유낙하 공 1개**(MATLAB Simulink 대조)와 **안식각**이라 — 우리 ASSB 압밀-전달 파이프라인과는 *연구 깊이의 차원이 다르다*. 이건 약점이 아니라 **이 문서의 정체성(입문 튜토리얼 + AM 응용)**이며, 정직히 그렇게 기록한다.

★ **소재 주의**: 이 문서는 **금속 AM 분말**(DED, direct energy deposition; 강철 공 freefall; 안식각용 ρ=2.5–7.8 g/cm³ 일반 분말). **LPSCl/NMC811 소재 데이터·porosity·σ 절대값은 전혀 없다** → 절대값 전이 금지, **명령어/워크플로/방법론**만 가치.

---

## 1. 한 줄 요약

LLNL의 학부 인턴 프로젝트로, **금속 AM(특히 DED) 분말의 동적 거동**(진동 feeder를 통한 흐름·feed-rate, 안식각 = flowability 지표)을 **DEM(LIGGGHTS-PUBLIC)**으로 해석하고, 동시에 **LIGGGHTS-PUBLIC 입력 스크립트 작성·접촉모델 선택·메시/벽 임포트·입자 삽입·실행·ParaView 후처리**까지를 단계별로 가르치는 **튜토리얼**이다. 물리 검증은 (i) **자유낙하 공의 bounce**를 MATLAB Simulink ode45와 대조(반발계수 일치), (ii) **점착에너지밀도(CED)를 0→9.5×10⁵ erg/cc 스윕하며 안식각이 ~24.7°→73°로 증가**하고 **유량은 반대로 감소**(R²=0.98·0.90)함을 보임. **= LIGGGHTS의 공개 입문 레퍼런스 + AM 분말 흐름 응용**(전달·소성 morphology·ASSB 압밀은 다루지 않음).

## 2. 메타

| 저자 | 보고서/년 | 식별자 | 소재 (SE/CAM) | 연구유형 |
|---|---|---|---|---|
| **Safwat Shenouda** (North Carolina A&T State University, 학부 인턴) · 멘토 **Andrew (A.) Hoff** (Lawrence Livermore National Laboratory) | **LLNL-TR-813736**, Lawrence Livermore National Laboratory, technical report. deck 2020-06-24 / report 2020-07-27 / cover 2020-08-19 | **LLNL-TR-813736** (DOI 없음; DOE/NNSA Contract **DE-AC52-07NA27344**, *Unclassified*) | **금속 AM 분말** (DED 공정; 강철 공 freefall; 안식각용 일반 분말 ρ 2.5 / 7.8 g/cm³). **LPSCl·NMC811 직접 소재 데이터 없음** | **DEM**(LIGGGHTS-PUBLIC) 응용(분말 흐름/feed-rate/안식각) **+ 단계별 튜토리얼**. 검증: 자유낙하 공(MATLAB Simulink ode45) + 안식각 vs CED |

> ★ **위치**: 우리 wishlist의 **#20 (★ DEM / LIGGGHTS — 직접 우리 코드)**. **frame[5] 분류**: 이 문서 = **역학/흐름 측 + 튜토리얼**(분말 안식각·feed-rate). 전달 σ·소성 morphology 없음 → 우리 MPM(형상)·네트워크 솔버(전달)가 메우는 절반이 통째로 빠짐 + 애초에 *압밀*이 아니라 *흐름/안식각*이 주제(다른 응용).

## 3. 핵심 물성 (수치)

> ⚠ **이 문서는 소재 측정값 논문이 아니라 *튜토리얼 + AM 흐름 데모*다**. 아래 "수치"는 (a) 안식각-vs-CED 데모 결과, (b) 튜토리얼 예제 파라미터, (c) freefall 검증이다. **LPSCl·NMC811 물성 전이는 불가**(porosity·σ·E_SE·Heckel 절대값 전혀 없음). 우리에게 가치는 **명령어·워크플로·방법론**이다.

| 물성 | 값 | 조건 | stated/digitized | 비고 |
|---|---|---|---|---|
| porosity / 상대밀도 | **n/a (전혀 없음)** | — | — | 이 문서는 *압밀/porosity*가 아니라 *흐름/안식각*이 주제 |
| σ_ionic / σ_e / σ_thermal | **n/a (전혀 없음)** | — | — | **전달 솔버 없음** — 순수 역학/흐름. frame[5] 역학 절반 |
| coverage / 접촉면적% | n/a | — | — | Hertz 접촉면적 식 `A₀=2πRδ`만 *교육용*으로 제시(측정 출력은 안 함) |
| coordination Z | n/a | — | — | 안식각·유량만 출력; 배위수 분석 없음 |
| E_SE / σ_y / ν | **금속분말 예시값만**: E=200 GPa(강철 공, `200.e9`)·5e7 barye(안식각 분말, CGS)·ν=0.3 | 튜토리얼 예제 | stated | LPSCl/NMC811 E·σ_y·ν **없음**. 소성·항복 모델 없음(Hertz 탄성만) |
| Heckel P_y / knee | **n/a (없음)** | — | — | Heckel 분석 안 함(압밀 아님) |
| **안식각 (angle of repose) vs CED** | **24.7° → 73.08°** (CED 4.0×10⁵ → 9.0×10⁵ erg/cc) | Hertz+SJKR, 안식각 데모 | stated (Fig 7–18 캡션) | 피팅 **θ=0.0079·CED²−0.209·CED+20**, R²=**0.9776** (CED 단위 ×10⁵) |
| **유량 (flow rate) vs 안식각** | **~36 → ~29 g/cc** (안식각 ~20°→75°) | massflow/mesh 데모 | stated (Appendix B) | 피팅 **flow=0.0018·angle²−0.2917·angle+41.141**, R²=**0.9005** — 안식각↑(=점착↑) → 유량↓ |
| 자유낙하 검증 | LIGGGHTS bounce ↔ MATLAB ode45 일치(반발계수 0.9, 국소 max/min err 분석) | h=1.5/3.0/6.0 m, 강철 공 | stated (Fig 17–20 슬라이드) | DEM 반발모델 검증(국소 극값 오차 peak ~0.3% 부근) |
| PSD (튜토리얼 예제) | radius 0.0025 / 0.0035 / 0.005 (frac 0.5/0.25/0.25) — 또는 mono 0.0025 | CGS(cm) 예제 | stated | **임의 교육용 PSD**(소재 무관). bi/poly-PSD 사용법은 가르침 |
| 진동 feeder | **113–120 Hz** 입력 주파수, wiggle period **0.0088496 s**(≈113 Hz), 진폭 (0, 0.0025, 0.0025) cm | 진동 feeder 데모 | stated | 실제 feeder = TEKNA **PFV100-VM-NO**(0.4 L bowl, 200 kPa) |

## 4. 시뮬레이션 방법 ★

> ★ 이 문서의 방법론은 **(A) LIGGGHTS 입력 스크립트 작성법** + **(B) 세 가지 데모**(자유낙하 공 / 안식각 / 진동 feeder)다. 우리에게 중요한 건 **명령어·워크플로**(§B에서 우리 input과 대조). 아래는 그 *교육적 정의*를 우리 관점에서 정리.

- **code / version**: **LIGGGHTS-PUBLIC** (= "LAMMPS Improved General Granular and Granular Heat Transfer Simulator", 공개 오픈소스, Linux). 실행: `liggghts -echo both < INPUT_FILE.txt` (단일코어) 또는 `mpirun -np 4 lmp_auto < INPUT_FILE.txt` (멀티코어; `lmp_auto`는 `home/LIGGGHTS-PUBLIC/src`에서 복사). 전처리=Notepad++/텍스트 에디터, 후처리=**ParaView 5.4.1 권장**(.liggghts 플러그인 + 실반경 스케일링; 5.8.0은 .vtk만) 또는 Blender. ⚠ **공개판(PUBLIC) — 상용 LIGGGHTS와 다름**(§아래 박스).

- **DEM 접촉법칙** ★ (이 문서가 가르치는 *3종 접촉모델* — 모두 **Hertz 기반 탄성**, 소성 항복 분기 없음):
  - **(2.4.1) Hertz (`hertz`)**: 두 입자 overlap δ의 함수로 접촉면적·압력 산출. 피타고라스로 유도: a²=2Rδ−δ²≈2Rδ → **접촉면적 A₀=πa²=2πRδ** (δ² 무시). "이 모델은 두 표면 사이 접촉면 *변형*을 무시한다"(=순수 Hertz, 소성 없음). 사용: `pair_style gran model hertz tangential history rolling_friction epsd2`.
  - **(2.4.2) Hooke (`hooke`)**: 선형 스프링. Hertz와 문법 동일하나 **characteristicVelocity(특성속도) 추가 필요** — "실험/수치/Hertz 시뮬에서 추정한 속도"를 Hooke에 입력. (Hertz는 이 값 *무시* — 부록 스크립트 주석 "this property is only used with the hooke model, it does nothing in the hertz model".)
  - **(2.4.1, sic 번호중복) Simplified JKR (`cohesion sjkr` / `sjkr2`)**: 입자 *점착*용. **cohesionEnergyDensity (CED)** 재료속성 필요. `pair_style ... cohesion sjkr` + `fix m6 ... cohesionEnergyDensity peratomtypepair ...`. **안식각 데모의 핵심 lever**(CED↑ → 안식각↑). 슬라이드에선 JKR 접촉반경식 `a³=(R/E)[fₙ+3γ_surπR+√(6γ_surπRfₙ+(3γ_surπR)²)]`, 분리 최대인력 `f_JKR=−(3/2)πγ_surR`, 점착포함 총법선력 `fₙ=(4a³E/3R)−√(8πEγ_sur·a³)` 을 *교육용*으로 보임.
  - **(슬라이드) DMT**: "작고 약한 점착 입자의 허용 근사", 인력 `f_DMT=−2πγ_surR`, Hertz 기반(접촉 변형 무시). ★ 우리 `dmt1975` digest와 동일 — SE 같은 작고 단단한 입자에 적합(DMT 체제).
  - **⚠ 핵심**: **이 문서의 모든 데모는 `hertz`(+`cohesion sjkr`)를 씀** — **선형 hooke/hysteresis(우리 모델)나 소성 항복 분기(Thornton–Ning/EEPA)는 데모에 *안 씀***. 즉 **순수 Hertz 탄성 + SJKR 점착**. (Hooke는 "문법만 같다"고 설명할 뿐 실제 데모는 Hertz.)
  - **whitelist (Fig 2, 중요한 실무 팁)**: `src/style_contact_model.whitelist`(예: `trough_hertz.txt`)에 *허용된 모델 조합*이 나열됨. 잘못된 조합이면 `ERROR: Contact model not found in any whitelist`. → **우리도 새 모델 조합 쓸 때 whitelist 확인 필요**(실무 디버깅 팁).

- **재료 파라미터** (튜토리얼 예제, **소재 무관 임의값**):
  - 강철 공 freefall: E=`200.e9`(SI), ν=0.3, CoR=0.9, 마찰=0 (이상화된 탄성 bounce).
  - 안식각 분말: E=`5e7` barye(CGS=Ba=dyne/cm², ≈5 GPa), ν=0.3, CoR=0.2, sliding friction=0.75, rolling friction 0.2(p-p)/0.7(p-geom), **CED 4×10⁵–9.5×10⁵ erg/cc 스윕**(이게 lever), ρ=2.5 g/cm³, radius 0.0025–0.003 cm.
  - 진동 feeder: E=`5e7` barye, ν=0.3, 동일 접촉파라미터.
  - **항복응력 σ_y·경화 없음**(Hertz는 무한탄성). **이것이 ASSB 압밀과 가장 큰 물리 차이** — 우리는 hooke/hysteresis 소성분기 + 18× 연화로 압밀을 잡는데, 이 문서는 *흐름*만 보므로 탄성 Hertz로 충분.

- **bond/binder 모델**: **없음**(점착은 SJKR CED로만 통합 표현; 명시 바인더 입자상·bond 없음).

- **MPM/continuum**: **없음**(순수 이산 DEM). 입자 **형상 안 변함**.

- **전달 솔버**: **없음**(σ_ionic/e/thermal 전혀 안 다룸). 슬라이드 첫 장에서 "FEM=연속체 / DEM=이산"이라고 *대조*만 함(FEM 자체는 안 씀). → frame[5]에서 **역학/흐름 절반만** 소유.

- **입자 처리** ★ (DEM판 "무질서 처리"):
  - **구(sphere)만** (`atom_style granular`; integrator `fix nve/sphere`; "multisphere·superquadratic이 다른 옵션"이라고 *언급만* 함).
  - **mono 또는 임의 bi/tri-PSD** (`particledistribution/discrete`로 frac 지정 — 사용법은 가르치나 데모는 대개 mono 또는 50/25/25). **소재-특이 bimodal(우리 12:4:1) 아님**.
  - **rigid sphere + 순수 Hertz 탄성 접촉**(소성 분기 *없음*; SJKR 점착만). → **CONTACT-소성조차 아님**(우리 hooke/hysteresis는 소성분기 있음, 이 문서 Hertz는 그것도 없음). **진짜 SHAPE 소성은 당연히 없음**. ⇒ `elasto_plastic_feasibility.md §0` 층위에서 **층위(0) 순수탄성 Hertz**(우리 층위(1) CONTACT-소성보다도 아래; 층위(3) SHAPE는 우리 MPM).
  - **흐름/안식각이 주제라 소성 불필요**: 분말이 *흐르고 쌓이는* 거동(안식각)은 마찰·점착·중력 균형이 지배 → Hertz 탄성으로 충분(압밀 고압이 아니므로). 이것이 *틀린* 게 아니라 *응용이 다름*.

- **도메인/RVE / servo / seeds / 압력범위**:
  - **자유낙하 공**: 단일 강철 공, z=1.5 m에서 낙하 → 바닥 평면 벽(`fix wall/gran ... primitive type 1 zplane 0.0`)에 bounce. `xcm(all,z)` 로 질량중심 z 추적, MATLAB ode45 대조. **압력 없음**(중력 동역학).
  - **안식각**: 실린더 영역(`region factory cylinder z 0 0 0.0125 0. 0.25`)에서 분말을 `insert/rate/region`으로 흘려, 기울인 중력(또는 평면)에 쌓아 **pile 경사각** 측정. CED 스윕. **압력 없음**(자유 적층).
  - **진동 feeder**: SolidWorks STL trough(`fix mesh/surface file Wiggle.stl`)를 `fix move/mesh ... wiggle`로 113 Hz 진동시켜 분말 흐름·**massflow/mesh로 유량** 측정. **압력 없음**(진동 수송).
  - **seeds**: 삽입 시드 = **10000 초과 소수**(prime)여야 함 (`primes(20000)` 로 MATLAB에서 생성; 예 10487/11887/11897/32452867/86028157). 시드 바꾸면 "통계적으로 유사한 varying 결과"(우리 seed-variance와 동일 철학).
  - **timestep**: **Rayleigh timestep의 ~20%**(또는 Hertz timestep, hooke 쓸 때) — §아래 공식.

- **특이사항/튜닝**:
  - **단위계 두 종**: SI(kg·m·s·Pa) 또는 CGS(g·cm·s·**barye**=dyne/cm²). 부록 A에 SI↔CGS 단위 환산표. **안식각/feeder 데모는 CGS, freefall은 SI**. ⚠ "Barye = 1.6e-6 bars"는 *오타*(정확히는 1 barye = 1 dyne/cm² = 0.1 Pa = 1e-6 bar).
  - **2단계 워크플로 철학**: ① .txt input 생성(입자/단위/변수 → 도메인/경계 → 접촉모델/이웃/timestep → 삽입) → ② **모델 calibrate + 파라미터 조정**(변수로 재실행 쉽게) → ③ ParaView 후처리 → ④ Excel/MATLAB 분석. = 우리 webapp/calibration 루프의 *입문판*.
  - **안정성 진단**: KE(운동에너지)가 "wildly varying"이면 불안정 → 입자 적게/천천히 삽입하거나 강성 낮춤. `fix check/timestep/gran`으로 자동 점검(§아래).

> ### 📦 LIGGGHTS-PUBLIC vs 상용 LIGGGHTS (우리가 쓰는 것과의 차이)
> 이 튜토리얼은 **LIGGGHTS-PUBLIC**(완전 오픈소스, DCS Computing 공개판)을 가르친다. **상용 LIGGGHTS(LIGGGHTS-WITH-BONDS / Aspherix 등)**는 추가 기능(고급 bond, 멀티스피어 최적화, 일부 접촉모델, 상용 지원)을 갖는다. **우리 input(`thin9_seed.liggghts` 등)이 쓰는 `hooke/hysteresis`·`coefficientMaxElasticStiffness`·`coefficientAdhesionStiffness`·`coefficientPlasticityDepth`·`mesh/surface/stress`·`move/mesh`는 PUBLIC에도 대부분 존재**(우리 스크립트가 PUBLIC 호환으로 보임). ⚠ 단 **이 튜토리얼은 그 hooke/hysteresis 소성모델을 *데모에 쓰지 않음*** — Hertz+SJKR만 가르침 → **우리 핵심 모델(hooke/hysteresis 소성분기)의 사용법은 이 문서에 *없다***(Luding 2008 digest가 그 정의서). 이 문서는 *기초 명령어·워크플로* 레퍼런스이지 우리 소성 접촉모델 가이드는 아님.

---

## 4.5. 튜토리얼이 가르치는 핵심 공식·명령어 (우리가 빌릴 후보) ★

> 이 절은 §B 적용가능성의 근거. **우리 input에 *없거나 다른* 유용한 것**을 굵게.

### (a) Rayleigh / Hertz timestep 공식 — **우리가 명시적으로 안 쓰는 안정성 기준**
- **Rayleigh timestep**: `dt_R = πR√(ρ/G) / (0.1631ν + 0.8766)`, G=E/(2(1+ν)) (전단탄성률), 다입자면 1/R=Σ1/Rᵢ, 1/E=Σ1/Eᵢ.
  - 실무: **timestep = Rayleigh의 ~20%** (hooke 쓸 땐 Hertz timestep도 고려).
- **Hertz timestep**: `dt_H = 2.87·(m²/(R·V_max·E²))^0.2` (m=질량, V_max=최대속도). ⚠ V_max를 사전에 알아야 해서 까다로움.
- **★ 자동 점검**: **`fix ts_check all check/timestep/gran 1000 0.2 0.2`** — 1000스텝마다 timestep이 Rayleigh·Hertz의 20%를 넘으면 *경고 출력*. → **우리 input엔 이 fix가 없다**(우리는 dt=1e-6을 고정). **빌릴 가치 있음**: 압밀 중 강성이 변하면(소성·overlap) 안정 timestep도 변하므로, `check/timestep/gran`을 넣으면 자동 안전 점검. (우리 `dem_scripts/*.liggghts`에 추가 검토 — backlog 후보.)

### (b) 입자 삽입 3종 — 우리는 `insert/pack`만, 이 문서는 셋 다
| 방법 | 명령 | 특징 | 우리 사용? |
|---|---|---|---|
| **insert/pack** | `fix ins all insert/pack ... volumefraction_region X` | 영역을 목표 부피분율로 채움. **"가장 비효율, 필요할 때만"** | ★ **우리가 쓰는 것**(`thin9_seed.liggghts:80`, `volumefraction_region 0.148`) |
| **insert/stream** | `fix ins all insert/stream seed ... insertion_face ins_mesh extrude_length 0.1` | STL 평면에서 입자 스트림 삽입. mass+massrate 또는 nparticles+particlerate | 우리 미사용 |
| **insert/rate/region** | `fix ins all insert/rate/region seed ... region factory nparticles INF particlerate 1000 insert_every 100` | 영역에서 *속도 제어* 삽입(가장 편리, STL 불필요). **안식각/feeder 데모가 이걸 씀** | 우리 미사용 |
- **삽입면(insertion face)**: STL 평면(`mesh/surface/planar`) 또는 region(`cylinder z x y r zlo zhi`). 도메인보다 크면 `scale`로 축소.
- ★ **우리 대비**: 우리는 settling 후 `insert/pack`(부피분율)으로 한 번에 채우고 plate로 압축. 이 문서의 **`insert/rate/region`(속도 제어 연속 삽입)**은 *흐름/feed* 모사용 — 우리 ASSB 압밀엔 불필요하나, 혹시 *충전(filling)* 거동을 보고 싶을 때 참고.

### (c) 메시/벽 임포트 & 이동 — **우리 plate STL과 직접 대응**
- **STL 임포트**: `fix cad1 all mesh/surface file Wiggle.stl type 2 scale 0.01` (⚠ Windows=.STL, Linux=.stl). 벽 접촉: `fix walls all wall/gran model hertz tangential no_history rolling_friction cdt mesh n_meshes 1 meshes cad1`.
  - ★ **우리 대응**: 우리는 동적 plate STL을 *런타임 생성*(`thin9_seed.liggghts:117–132` `print "..." file plate.stl`) 후 `fix top_mesh all mesh/surface/stress file plate.stl ...` + `fix zwall_top all wall/gran model hooke/hysteresis ... mesh meshes top_mesh`. **방법 동일**(STL→mesh/surface→wall/gran). 차이: 우리는 `mesh/surface/**stress**`(반력 측정용) + `hooke/hysteresis`, 이 문서는 `mesh/surface`(stress 없음) + `hertz`.
- **★ 이동(`fix move/mesh`)**: 
  - **진동**: `fix move all move/mesh mesh cad1 wiggle amplitude 0.0 0.0025 0.0025 period 0.0088496` (진폭벡터 + 주기 → 113 Hz 진동).
  - ★ **우리 대응**: 우리는 `fix move_press all move/mesh mesh top_mesh linear 0.0 0.0 -${press_speed}` (plate를 *선형 하강* = 압축). **같은 `move/mesh` 명령, 모드만 다름**(우리=linear 압축, 이 문서=wiggle 진동). → **`wiggle`로 plate를 진동시켜 *tapping/vibration densification*을 모사할 수 있다**(우리가 안 해본 것 — backlog 후보: 진동-보조 압밀).
- **반력(stress)**: 우리는 `mesh/surface/stress` + `f_top_mesh[3]`(z방향 반력)으로 압력 산출(`pressMPa equal abs(f_top_mesh[3])/0.0025/1e6`). 이 문서는 *벽 반력*을 안 씀(흐름이라 불필요) — 대신 **`fix massflow/mesh`로 유량** 측정.

### (d) **`fix massflow/mesh`** — 유량 측정 (우리에게 없는 출력)
- `fix plane1 all mesh/surface/planar file massface.stl type 2 scale 0.01` + `fix mass all massflow/mesh mesh plane1 count once delete_atoms no vec_side 0. 0.625 0. file massflow.txt`.
- → `massflow.txt`: (1열) 통과 입자 ID, (2열) 입자 직경, (7열) **유량(g/s)**. ParaView/Excel로 분석.
- ★ **우리 대비**: 우리는 *압밀*이라 유량 불필요. 하지만 **개념적으로 "면을 통과하는 입자/플럭스를 센다"**는 건 우리 transport 솔버의 *입자 단위* 버전과 다른 축(이건 *질량* 플럭스, 우리는 *전하/열* 플럭스를 네트워크로). 직접 차용은 아니나, *충전 균질도*나 *segregation* 진단엔 쓸 수 있음.

### (e) dump / run / 단위
- **dump**: `dump dmpparticle all custom/vtk 1000 post/particles_*.vtk id type x y z vx vy vz fx fy fz radius mass` (.vtk=bounding box 포함, 모든 ParaView 버전) 또는 `custom ... *.liggghts`(.liggghts=입자/기하만, ParaView 5.1 필요). 메시 dump: `dump dmpWiggle all mesh/stl 1000 post/Wiggle*.stl`.
  - ★ **우리 대응**: 우리도 `dump dmp_atom all custom 5000 post/atom_*.liggghts id type x y z radius vx vy vz c_strs[1..3] c_ke` + `dump dmp_mesh all mesh/stl ...` + **`dump dmp_contact all local ... c_cpl[1..26]`**(접촉망 — *이 문서에 없는 우리 고유 출력*, 전달 솔버 입력). 이 문서는 **접촉 단위 dump(`pair/gran/local`)를 안 함** → 우리 네트워크 솔버의 입력 자체가 없음(= 우리 transport novelty의 데이터 기원).
- **run**: `run N` (N timesteps). 파일 수 = (run/dump)×(입자그룹+기하). `unfix`로 객체 제거.
- **단위표**(부록 A): SI(Pa·N·m·kg·s) / CGS(barye·dyne·cm·g·s). **압력 SI=Pa, CGS=barye(=0.1 Pa)**.

## 5. Figure set ★

> 84쪽 = 슬라이드(p.1–20) + 튜토리얼/부록(p.21–84). 주요 그림만.

| Fig/슬라이드 | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| **슬라이드 Background** | FEM(연속체) vs DEM(이산) 충돌 시뮬 나란히 | "FEM=continuum, DEM=discrete" 대조 — 우리 DEM↔MPM 분업 그림의 입문판(단 그들은 FEM 안 씀) |
| **슬라이드 DEM Contact Models** | Hertz(`A₀=2πRδ`) / JKR(점착반경·인력식) / DMT(`f=−2πγR`) 교육 슬라이드 | **접촉모델 정의 슬라이드** — DMT(작고 단단=SE) 우리 `dmt1975`와 일치. 단 *Hertz 탄성*만(우리 hooke/hysteresis 소성 아님) |
| **슬라이드 Methodology / Input Script (p.10–15)** | Notepad++→LIGGGHTS→ParaView 워크플로 + input .txt 스크린샷(부분): `atom_style granular`/`boundary f f f`/`pair_style gran model hertz ...`/`fix wall/gran`/`fix gravity` | **워크플로 한 컷** + 명령어 미리보기(저해상도). 실제 풀 스크립트는 부록에 |
| **슬라이드 Raw Data / Error Analysis (p.17–20)** | 자유낙하 공: Height/Velocity/Accel vs Time (LIGGGHTS vs MATLAB), 국소 max/min 오차 분석(peak error ~0.3% 부근) | **DEM 반발모델 검증 방법**(해석해 대조) — 우리 Minnmann/Cronau 앵커의 *toy* 버전. bounce가 잘 맞음 = DEM 동역학 sanity |
| **슬라이드 Vibratory Feeder (p.21–32)** | TEKNA PFV100-VM-NO feeder + trough slice 모델 + "No vibration/With vibration" troubleshooting 스냅샷("poor adhesion & contact" / "poor stability due to high amplitude") | **진동 수송 DEM 셋업** + 흔한 실패(점착부족/진폭과대) 진단 — 진동-보조 거동 참고 |
| **슬라이드 Velocity Trend (p.23)** | 경사각 0→15°에 따른 입자 속도 분포(히스토그램) 감소 추세 | feed-rate가 경사각에 민감 — AM feeder 설계 변수 |
| **슬라이드 Relevant DEM Parameters (p.33)** | 안식각·Hausner ratio·sphericity·CoR·마찰·구름마찰 정의 모음 | **flowability 지표 용어집**(안식각·Hausner=ρ_tap/ρ_bulk·구형도 ω) — 분말 특성화 |
| **Fig 1 (튜토리얼)** | 입자 삽입용 실린더 region 모식 | `region cylinder` 삽입영역 정의 |
| **Fig 2 (튜토리얼, 중요)** | **whitelist**(`style_contact_model.whitelist`) 스크린샷 — 허용 모델 조합 목록 | ★ **새 접촉모델 조합 쓸 때 whitelist 확인**(우리 실무 디버깅 팁) |
| **Fig 3–4 (튜토리얼)** | ParaView .vtk 임포트 + Point Gaussian(실반경) 렌더 | ParaView 5.4.1 후처리 절차 |
| **Fig 5 (튜토리얼)** | Plot Matrix View 속도분포 | ParaView 통계 플롯 |
| **Fig 6 (튜토리얼)** | massflow.txt raw 데이터(Excel) | 유량 후처리 형식 |
| **★ Appendix B 안식각 그래프** | **안식각 vs CED**(θ=0.0079·CED²−0.209·CED+20, R²=0.9776) + **유량 vs 안식각**(0.0018x²−0.2917x+41.141, R²=0.9005) | **점착(CED)↑ → 안식각↑·유량↓** 정량화. 우리 SE-SE adhesion이 압밀-후 결합에 주는 효과의 *흐름* 짝(단 흐름이지 압밀 아님) |
| **★ Fig 7–18 (안식각 갤러리)** | CED 9.5e5→4.0e5 erg/cc 스윕 ParaView 단면: pile이 **73°(가파른 기둥) → 24.7°(평평한 더미)** 로 전이. 색=입자 ID/높이 | **점착이 분말 적층 형상을 지배** 시각 증거. CED↑ → 입자가 *안 흐르고 쌓임*(높은 안식각). 우리 SJKR/`--coh` 정성거동의 흐름판 |

> ★ **안식각 갤러리 = SJKR CED→안식각 transfer function**(데이터로 추출 가능):
> | CED (erg/cc) | 안식각 (°) | | CED | 안식각 |
> |---|---|---|---|---|
> | 9.5×10⁵ | 72.54 | | 6.5×10⁵ | 38.55 |
> | 9.0×10⁵ | 73.08 | | 6.0×10⁵ | 31.83 |
> | 8.5×10⁵ | 58.7 | | 5.5×10⁵ | 30.22 |
> | 8.0×10⁵ | 55.79 | | 5.0×10⁵ | 26.45 |
> | 7.5×10⁵ | 51.29 | | 4.5×10⁵ | 25.59 |
> | 7.0×10⁵ | 44.26 | | 4.0×10⁵ | 24.7 |
> (Fig 7–18 캡션, stated. CED↑ → 안식각↑, 단조; 9.0e5 부근 포화/노이즈. **소재 무관 일반분말** → 절대값 전이 금지, *점착→유동성* 정성관계만.)

## 6. Post-processing ★

- **무엇**:
  - **안식각(angle of repose)**: 적층 pile의 경사각을 ParaView 단면에서 측정 → flowability 지표(낮을수록 잘 흐름). CED의 함수로 회귀(R²=0.98).
  - **유량(flow rate)**: `fix massflow/mesh`로 면 통과 질량/시간(g/s) → 안식각의 함수로 회귀(R²=0.90).
  - **자유낙하 검증**: `xcm(all,z)`(질량중심 z) 시계열을 MATLAB ode45(2차 ODE + 반발계수) 와 대조, 국소 max/min 오차 정량.
  - **Heckel/percolation/coordination/coverage/tortuosity/porosity convention/EIS-TLM**: **전부 안 함**(이 문서 범위 밖 — 흐름/안식각 전용).
- **도구**: **ParaView 5.4.1**(.liggghts 플러그인, Point Gaussian 실반경, Plot Matrix View 통계, .csv export) / **Blender**(시각화) / **Excel·MATLAB**(회귀·오차분석) / **MATLAB Simulink ode45**(freefall 해석해 baseline) / **MATLAB `primes(n)`**(삽입 시드 소수 생성) / **SolidWorks 2019**(trough/plate STL CAD).
- **수치화·플롯·기록 방식**: dump(.vtk/.liggghts) → ParaView 임포트 → Point Gaussian 렌더(실반경) → Plot Matrix(속도분포) 또는 .csv export → Excel/MATLAB 회귀. **로그파일(log)**: 1부=input 스크립트 echo, 2부=계산 데이터(입자수·timestep·KE). 100스텝마다 thermo 출력.

---

## 7. 우리 DEM+MPM 대비  →  `our_dem_baseline.md`

> ★ 이 문서는 **튜토리얼 + AM 흐름 응용**이라, "대비"는 *물리모델 경쟁*이 아니라 **(a) 명령어/워크플로 대조**(§B) + **(b) 응용·깊이의 차원 차이**다.

| 항목 | 이 문서 (Shenouda 2020) | 우리 (ASSB DEM+MPM) | 차이 / 이유 |
|---|---|---|---|
| **목적** | LIGGGHTS 입문 튜토리얼 + AM 분말 *흐름/안식각/feed-rate* | ASSB *압밀→전달(σ 삼중항)→grade* + MPM morphology + scaling-law predictor | **응용·깊이 차원 다름** — 입문/흐름 vs 연구급 압밀-전달 파이프라인 |
| **code** | LIGGGHTS-**PUBLIC**(공개판) | LIGGGHTS (hooke/hysteresis·mesh/surface/stress 사용) | **같은 코드 계열** ✓ — 우리 input이 PUBLIC 명령어와 대부분 호환 |
| **접촉 LAW** | **Hertz**(`A₀=2πRδ`, 순수탄성) + **SJKR 점착**(CED). 소성분기 **없음** | **hooke/hysteresis**(Luding eq6, 소성분기 k₁→k₂·δ₀ + adhesion k_c) + **18× 연화** + **Stage-E**(Tabor+volume 소성접촉면적) | **우리가 훨씬 정교**: 우리는 소성분기·항복깊이·최대강성cap·소성접촉면적까지. 이 문서 Hertz는 *흐름*엔 충분하나 *압밀*엔 부족 |
| **항복/소성** | **없음**(Hertz 무한탄성) | hooke/hysteresis 소성 잔류겹침 δ₀ + ε_sphere "displaced material" + MPM 진짜 SHAPE 소성(J2) | **우리만 소성**. 이 문서는 *흐름*이라 소성 불필요(응용 차이) |
| **전달 σ** | **없음**(역학/흐름 전용) | **σ_ionic + σ_e + σ_thermal 삼중항**(Kirchhoff + Holm R=1/(2σr_c) + Stage-E) | ★★ **우리 핵심 novelty 통째로 부재**. 이 문서는 접촉망 dump(`pair/gran/local`)조차 안 함 |
| **morphology/변형장** | **없음**(rigid 구) | MPM 진짜 형상변화(SEM 일치)·void-fill·Σdg 변형장·scaffold 커플링 | **우리 MPM 고유**(frame[5]) |
| **압밀 모드** | **없음** (흐름: freefall·안식각·진동수송) | cold-press(단축, plate linear 하강, 300 MPa hold) | **다른 응용** — 이 문서는 압밀 자체를 안 함 |
| **plate/mesh 이동** | `move/mesh ... **wiggle**`(진동) | `move/mesh ... **linear**`(압축 하강) | **같은 명령, 모드만 다름** — wiggle은 우리가 진동압밀에 빌릴 수 있음 |
| **삽입** | insert/pack·**insert/stream·insert/rate/region** (셋 다) | **insert/pack**(부피분율)만 | 우리는 한 방식; 이 문서가 셋 다 가르침(흐름 모사용 rate/region) |
| **안정성 점검** | **`fix check/timestep/gran`**(자동) + Rayleigh/Hertz timestep 공식 | dt=1e-6 고정(자동 점검 fix 없음) | ★ **빌릴 가치**: 우리도 `check/timestep/gran` 추가 검토 |
| **검증** | 자유낙하 공(MATLAB ode45) + 안식각-vs-CED 회귀 | Minnmann·Cronau·Bazzoun·SEM 등 *소재* 외부 앵커 + scaling-law LOOCV 0.90–0.98 | **우리 검증이 훨씬 깊음**(연구급 vs toy). 이 문서 검증은 *동역학 sanity*(공 bounce) 수준 |
| **소재** | 금속 AM 분말(소재 무관 예시) | LPSCl SE + NMC811 | **절대값 전이 불가**(porosity·σ·E 전혀 없음) — 명령어/방법만 |
| **PSD** | mono 또는 임의 50/25/25 | **소재-특이 bimodal 12:4:1**(AM_P/AM_S/SE) + Furnas dip | 우리만 소재-실측 PSD + dip |
| **predictor** | 없음 | 솔버→스케일링법칙(σ_ionic 0.975·σ_e 0.953·σ_thermal 0.90 LOOCV) → 2D synth → layered | **우리만**(이 문서엔 ML 없음) |

### ★ 핵심 대비 — "같은 LIGGGHTS, 입문 튜토리얼·흐름 vs 연구급 압밀-전달"
- **같은 도구**: 둘 다 **LIGGGHTS**(구 + 접촉 force-field + STL mesh wall + move/mesh + dump). 우리 input이 이 튜토리얼의 명령어 vocabulary와 거의 같다 — `atom_style granular`/`boundary`/`pair_style gran model`/`fix property/global`/`fix wall/gran ... mesh`/`fix move/mesh`/`particletemplate/sphere`/`particledistribution/discrete`/`insert/*`/`dump custom`/`region`. **즉 이 문서는 우리 input을 *읽는 법*의 입문서로 그대로 쓸 수 있다.**
- **다른 차원**: 이 문서는 **(i) 접촉모델이 Hertz 탄성**(우리 hooke/hysteresis 소성 아님), **(ii) 응용이 흐름/안식각/feed-rate**(우리 압밀-전달 아님), **(iii) 검증이 자유낙하 공 + 안식각**(우리 다중 소재 앵커 + scaling-law 아님), **(iv) 전달 σ·MPM morphology·Stage-E·scaffold·predictor 전부 없음**. ⇒ **명령어/워크플로는 1:1 대조 가능하나, 물리·검증·산출물의 깊이는 우리가 압도적**. 이건 *경쟁 모델이 아니라 입문 레퍼런스 + 다른 응용*이라 정직히 그렇게 본다.

### frame[5] 위치
- **이 문서 = 역학/흐름 측 + 튜토리얼**: rigid 구 + Hertz/SJKR → 분말 흐름·안식각·feed-rate. **압밀·전달·morphology 없음**(애초에 *흐름*이 주제). 우리 MPM(형상)·네트워크 솔버(전달)가 메우는 절반 + 우리 압밀 자체가 이 문서엔 없음.

---

## 8. 적용 인사이트 (내 연구에 어떻게)

- ① **신규 입문자/협업자용 LIGGGHTS 레퍼런스로 인용·공유**: 우리 input(`thin9_seed.liggghts`)을 처음 보는 사람에게 "이 튜토리얼(LLNL-TR-813736)의 §2가 모든 명령어를 설명한다 — `atom_style`/`pair_style gran model`/`fix wall/gran ... mesh`/`move/mesh`/`insert/*`/`dump custom`/`region`"라고 가리킬 수 있다(공개·Unclassified). **단 우리 hooke/hysteresis 소성모델은 이 문서에 없으니 Luding 2008 digest와 병용.**
- ② **★ `fix check/timestep/gran` 자동 안정성 점검 도입 검토(backlog 후보)**: 우리는 dt=1e-6을 고정하는데, 압밀 중 overlap/강성이 커지면 안정 timestep도 변한다. `fix ts_check all check/timestep/gran 1000 0.2 0.2`를 넣으면 Rayleigh/Hertz 20% 초과 시 경고 → *불안정 압밀 조기 발견*. (영향 낮으나 안전망; `dem_scripts/*.liggghts`에 추가 검토.)
- ③ **★ `move/mesh ... wiggle`로 진동-보조 압밀 실험(backlog 후보)**: 우리 plate는 `move/mesh linear`(압축)만. 이 문서의 `wiggle amplitude ... period ...`(진동)을 plate에 적용하면 *tapping/vibration densification*(진동으로 재배열 촉진 → 더 낮은 porosity)을 모사 가능 — 우리가 안 해본 압밀경로. (소재 무관 데모지만 명령 패턴은 직접 차용 가능.)
- ④ **`fix massflow/mesh` = 충전 균질도/segregation 진단 도구**: 압밀엔 불필요하나, 혹시 *충전(insert) 단계의 입자 분리/불균질*을 진단하려면 면 통과 플럭스를 셀 수 있다. (우리 transport 플럭스(전하/열)와는 다른 *질량* 플럭스.)
- ⑤ **whitelist 디버깅 팁**: 새 접촉모델 조합(예: 경로 A의 항복캡 모델, 또는 다른 cohesion/rolling 조합) 시도 시 `src/style_contact_model.whitelist` 확인 — "Contact model not found in any whitelist" 에러 회피. (`elasto_plastic_feasibility.md` 경로 A 구현 시 실무 체크.)
- ⑥ **SJKR CED↔안식각 transfer는 *흐름* 참고만**: CED↑ → 안식각↑(Fig 7–18) 는 *점착이 유동성을 줄인다*는 흐름 물리 — 우리 SE-SE adhesion(압밀-후 결합)과 *방향은 같으나 응용이 다름*(우리는 압밀, 이 문서는 적층). 우리 `--coh`/SJKR 정성검증의 *흐름판* 보조 근거로만(절대값 전이 금지).

## 적용가능성 (applicability to our LIGGGHTS DEM model) ★

> ★ **THE 핵심 절** — 이 튜토리얼의 어떤 LIGGGHTS 명령/접촉모델옵션/후처리가 *우리 input 스크립트*에 매핑되는가. (우리 기준: `dem_scripts/thin9_seed.liggghts`, `heckel/input_SE_heckel_300.liggghts`.) **명령어 단위로 구체적으로.**

### (1) 우리가 *이미 쓰는* 것 — 이 튜토리얼이 같은 명령을 가르침 (확인/검증용)
| 명령 (튜토리얼) | 우리 input | 일치 여부 / 차이 |
|---|---|---|
| `atom_style granular` | `thin9:9` 동일 | ✓ 동일 (이 문서: "granular or sphere") |
| `boundary f f f` (안식각) / `p p f`(freefall엔 f f f) | `thin9:11` **`p p f`**(x·y 주기, z 자유) | 우리=주기 RVE(압밀), 이 문서=`f f f`(이탈입자 삭제, 흐름). **응용 차이** |
| `units si` / `units cgs` | `thin9:15` `si` | 우리=SI, 이 문서=둘 다(freefall SI / 안식각·feeder CGS) |
| `newton off` · `communicate single vel yes` | `thin9:12,14` 동일 | ✓ 동일 |
| `pair_style gran model hertz tangential history rolling_friction epsd2` | `thin9:61` **`gran model hooke/hysteresis tangential history rolling_friction cdt`** | **모델·rolling 옵션 다름**: 우리=hooke/hysteresis(소성)+cdt, 이 문서=hertz(탄성)+epsd2/sjkr. **문법 골격 동일** |
| `fix m1..m5 all property/global youngsModulus/poissonsRatio/coefficientRestitution/coefficientFriction/coefficientRollingFriction` | `thin9:32–45` `m1..m5` **동일 5종** | ✓ **정확히 같은 fix 패턴**(peratomtype / peratomtypepair). 우리는 +`m6 MaxElasticStiffness`·`m7 AdhesionStiffness`·`m8 PlasticityDepth`·`m9 characteristicVelocity`(hooke/hysteresis 전용) 추가 |
| `fix ... wall/gran model ... primitive type 1 zplane 0.0` | `thin9:68` `zwall_bot ... primitive type 1 zplane 0.0` | ✓ **동일**(바닥 평면 벽) |
| `fix ... mesh/surface file X.stl` + `fix ... wall/gran ... mesh n_meshes 1 meshes X` | `thin9:135–136` `top_mesh`(`mesh/surface/stress`)+`zwall_top`(`wall/gran ... mesh meshes top_mesh`) | ✓ **동일 패턴**. 우리는 `mesh/surface/**stress**`(반력 측정), 이 문서는 `mesh/surface`(흐름이라 반력 불필요) |
| `fix ... move/mesh mesh X linear ...` / `wiggle ...` | `thin9:152` `move_press ... move/mesh mesh top_mesh **linear** 0 0 -speed` | ✓ **같은 명령**, 우리=linear(압축), 이 문서=linear(freefall 평면 고정)+**wiggle(진동)** |
| `particletemplate/sphere <prime> atom_type N density constant D radius constant R` | `thin9:72–74` `pts1/pts2/pts3` 동일 | ✓ **동일**(소수 시드 + density/radius constant) |
| `particledistribution/discrete <prime> n pts1 f1 ...` | `thin9:75` `pdd_mix ... 3 pts1 0.595 pts2 0.255 pts3 0.15` | ✓ **동일**(우리=3-type bimodal, 이 문서=1–3 type) |
| `dump ... custom N post/atom_*.liggghts id type x y z ...` + `dump ... mesh/stl` | `thin9:149,137` 동일 | ✓ **동일**(우리는 +`dump dmp_contact ... local c_cpl[1..26]` = 접촉망, **이 문서에 없음**) |
| `region ... block/cylinder ... units box` · `create_box` · `neighbor ... bin` · `neigh_modify delay 0` | `thin9:26–30` 동일 | ✓ **동일** |

### (2) 우리가 *안 쓰는* 것 — 이 튜토리얼에서 *빌릴 수 있는* 명령 (구체)
- **★ `fix ts_check all check/timestep/gran 1000 0.2 0.2`** — Rayleigh/Hertz timestep 20% 초과 시 1000스텝마다 경고. **우리 input엔 없음**(dt=1e-6 고정). → 압밀 중 강성 증가로 안정 timestep이 줄 때 *자동 안전망*. **추가 검토 1순위**(backlog).
- **★ `fix move/mesh mesh top_mesh wiggle amplitude 0 0 A period T`** — plate 진동. **우리는 linear만**. → *진동-보조 압밀*(tapping densification) 실험 명령. (예: settling 후 plate를 짧게 wiggle해 재배열 촉진 → porosity 추가 감소 시험.)
- **`fix ins all insert/rate/region seed <prime> ... region <reg> nparticles INF particlerate R insert_every K`** — *속도제어 연속 삽입*. 우리는 `insert/pack`(한 번에 부피분율). → *충전(filling) 동역학*을 보고 싶을 때.
- **`fix massflow/mesh mesh plane1 count once vec_side ... file massflow.txt`** — 면 통과 질량플럭스(g/s). → *충전 균질도/segregation* 진단(압밀엔 불필요).
- **Rayleigh timestep 공식** `dt_R=πR√(ρ/G)/(0.1631ν+0.8766)` — 우리 dt=1e-6의 *정당화/sanity* 계산. (우리 SE r=0.5µm·ρ=2000·E_eff=1.35 GPa로 dt_R 계산해 1e-6이 20% 이하인지 확인 가능.)

### (3) 금속분말 흐름 ↔ ASSB SE/AM 압밀 — 차이 (전이 주의)
- **접촉모델**: 이 문서 Hertz(탄성)+SJKR ↔ 우리 hooke/hysteresis(소성분기)+18×연화+Stage-E. *흐름*엔 Hertz면 되나 *압밀*엔 우리 소성모델 필요. **튜토리얼 명령 골격은 빌리되 접촉모델은 우리 것 유지.**
- **응용**: 흐름/안식각/feed-rate(이 문서) ≠ cold-press 압밀(우리). plate=linear 하강(우리) vs wiggle/freefall/안식각 적층(이 문서). **명령은 같아도 *물리 시나리오*가 다름** → 안식각·유량·CED 수치 전이 금지.
- **소재**: 금속(소재 무관) ≠ LPSCl/NMC811. **porosity·σ·E 절대값 0개** → 명령어/방법만.

## ★ 우리 novelty — 왜 우리가 state-of-the-art인가 (our novelty vs this work) ★

> ★ **firm·evidence-based.** 이 문서는 **LIGGGHTS 입문 튜토리얼 + 금속 AM 분말 *흐름/안식각* 응용**(학부 인턴 산출물, 검증=자유낙하 공 + 안식각 회귀)이다. **경쟁 물리모델이 아니다.** 따라서 우리 novelty 간극은 **이 corpus에서 가장 크다** — 우리 차별점 (1)–(7) 거의 전부가 이 문서에 *부재*한다. 아래는 *증거 기반*으로 못 박는다.

1. **★ 전달 TRIAD (σ_ionic + σ_e + σ_thermal) via Kirchhoff + Holm — 이 문서 完全 부재.**
   - **증거**: 이 문서는 σ를 *전혀* 다루지 않고(역학/흐름 전용), 우리 네트워크 솔버의 입력인 **접촉 단위 dump(`pair/gran/local`)조차 안 한다**(`dump custom`(입자)·`dump mesh/stl`만). FEM은 슬라이드에서 "continuum vs discrete" *대조*로만 언급(실제 안 씀).
   - **우리**: `compute cpl all pair/gran/local ... contactArea delta contactPoint` → `dump dmp_contact ... c_cpl[1..26]`(`thin9:65,166`) → Kirchhoff Σ(φi−φj)/R=0 + Holm R=1/(2σr_c) 네트워크 솔버 → σ_ionic/σ_e/σ_thermal **삼중항**. **이 문서엔 데이터 기원 자체가 없다.** = 우리 transport novelty의 가장 깨끗한 증거.

2. **★ Stage-E 소성 접촉면적(Tabor + volume) — 부재.**
   - **증거**: 이 문서 접촉면적 = **순수 Hertz `A₀=2πRδ`**(교육용 식, 측정 출력도 안 함; 소성 변형 *명시적으로 무시* — "neglects the deformation at the contact area").
   - **우리**: `network_conductivity.py:240–264` 5-regime A_physics = max(lower[Hertz·LIGGGHTS], min(caps[Tabor F/H · volume V/h · geom])). 소성 pile-up·over-compression cap까지. **이 문서 Hertz는 우리 Stage-E의 *출발점(층위0)*에도 못 미침.**

3. **★ DEM↔MPM scaffold 커플링 + J2 진짜 SHAPE morphology — 부재.**
   - **증거**: 이 문서 = rigid 구만(`fix nve/sphere`; multisphere/superquadratic "다른 옵션"이라 *언급만*). 입자 형상 안 변함, MPM 없음, void-fill 없음.
   - **우리**: MPM(Taichi, von Mises J2, ν=0.49) 진짜 SHAPE 소성(SEM 일치) + DEM AM scaffold 고정 + SE 소성 void-fill. real_14 16.7↔DEM 15.6↔Minnmann 10 % 교차검증. **이 문서엔 morphology·변형장 자체가 없음**(frame[5] 형상 절반).

4. **★ Fracture-aware (Auerbach/Lawn) — 부재.**
   - **증거**: 이 문서는 입자 파괴 없음(영구탄성 Hertz; 안식각 분말은 안 깨짐).
   - **우리**: AM_P 다결정 파괴(92:8 8mAh 37–40 % cracked) + f_intact·frac_severe + fracture-Holm partial conduction + Auerbach 임계.

5. **★ 문헌-grounded σ_grain (Cronau r_SE) + 다중 실험 앵커 — 부재.**
   - **증거**: 이 문서는 σ_grain 개념 없음(전도 안 다룸); 검증 앵커 = *자유낙하 공*(MATLAB ode45) + 안식각 회귀(소재 무관).
   - **우리**: σ_grain=3.0 mS/cm × Cronau(r_SE) 입계인자 + Minnmann/Doux/Bazzoun/Lee/Sakuda 다중 LPSCl 앵커. **연구급 외부 검증 vs toy 동역학 sanity.**

6. **★ 실험-anchored 독립 calibration (frame[4]) — 깊이 차원 다름.**
   - **증거**: 이 문서 calibration = "변수로 재실행해 안식각/유량 맞춤"(입문 루프); 단일 freefall 해석해 대조.
   - **우리**: DEM(Minnmann porosity + Cronau overlap) ⟂ MPM(SEM + Minnmann pure-SE) **각각 실험에 독립 보정 → 교차검증/모델한계 정량화**. 18× 연화의 3중 독립 확증(Cronau overlap / plastic-vs-rigid / MPM). **방법론 깊이가 다름.**

7. **★ 솔버→스케일링법칙 LOOCV predictor — 부재.**
   - **증거**: 이 문서는 ML 없음(안식각·유량을 *2차 다항* 회귀 R²=0.98/0.90 — 단일 lever CED의 단순 fit; 예측모델 아님).
   - **우리**: σ_ionic(LOOCV 0.975, 5 OLS) · σ_e(0.953, 8 OLS) · σ_thermal(0.90, 14 Ridge) → 2D synth → layered composite. **설계 knob → 전 metric 예측 vs 단변수 회귀.**

### 정직한 가치 평가 (over-claim 방지)
- 이 문서는 **나쁜 논문이 아니라 *다른 종류*다**: **깨끗한 LIGGGHTS-PUBLIC 입문 튜토리얼**(워크플로·명령어·timestep·삽입·메시·후처리·ParaView를 단계별로 잘 정리) + **금속 AM 분말 흐름 응용**(안식각=flowability, feed-rate). 학부 인턴이 1여름에 만든 *교육·응용* 산출물로서 충실하다.
- **우리 novelty 간극이 큰 이유는 *경쟁이 아니기 때문***: 이 문서는 (i) *압밀*이 아니라 *흐름*, (ii) *Hertz 탄성*이지 *소성*이 아님, (iii) *전달 없음*, (iv) *입문 튜토리얼*이지 연구급 파이프라인이 아님. → 7개 차별점 거의 전부 부재는 *당연*하며, 우리가 **ASSB 압밀-전달-morphology-predictor를 통합한 SOTA**임을 *대조로* 보여준다.
- **우리가 빌리는 것(정직)**: `check/timestep/gran` 안정성 점검 · `move/mesh wiggle` 진동압밀 · Rayleigh-timestep sanity · whitelist 디버깅 팁 — **명령어/실무 수준의 차용**이지 물리 차용이 아님. **이 문서의 진짜 효용 = 우리 input을 읽고 가르치는 입문 레퍼런스.**

## 9. 인용 가능 문장 (deck/paper용)

- "Shenouda & Hoff (LLNL-TR-813736, 2020) is a publicly-released LIGGGHTS-PUBLIC tutorial that applies DEM to metal additive-manufacturing powder flow (vibratory-feeder feed-rate and angle-of-repose), validated against a MATLAB Simulink free-fall solution and an angle-of-repose vs cohesion-energy-density sweep (R²=0.98) — it is an introductory reference and a powder-flow application, not a competing ASSB compaction–transport model."
- "Unlike our DEM, the tutorial's demonstrations use a *purely elastic Hertz* contact (`A₀=2πRδ`) with optional SJKR cohesion and *no plastic branch* — it has no transport solver, no Stage-E plastic contact area, no particle-shape plasticity, and no scaling-law predictor; its contact vocabulary (`atom_style granular`, `pair_style gran model`, `fix wall/gran ... mesh`, `move/mesh`, `insert/*`, `dump custom`) maps onto our input scripts, but our hooke/hysteresis plastic model is documented elsewhere (Luding 2008), not here."
- "Two reusable items from the tutorial: the **`fix check/timestep/gran`** automatic Rayleigh/Hertz-timestep stability check (which our fixed-`dt` scripts omit), and the **`move/mesh ... wiggle`** vibration command (a path to vibration-assisted densification our linear-plate compaction has not explored)."

## 10. 주의/한계 (over-claim 방지)

- **튜토리얼/학부 인턴 산출물 — 입문 깊이.** 일부 *오타·비정밀*: 제목 "LIGGGHTS-PUBLIC"이 표지엔 "LIGGGGHTS"로 오타, "Barye = 1.6e-6 bars"(틀림, 1 barye=1e-6 bar=0.1 Pa), 접촉모델 절 번호 중복(2.4.1이 두 번), "epsd2/cdt rolling" 등 약식 표기. **정밀 레퍼런스로 인용 시 주의** — 명령어 *존재*는 신뢰하되 수치 정밀도/오타는 검증.
- **소재 데이터 없음 = 절대값 전이 불가.** 금속 AM 분말(소재 무관 예시) — **LPSCl·NMC811 porosity·σ·E_SE·Heckel 절대값 0개**. 안식각/CED/유량은 *임의 일반분말* 데모 → 우리 압밀 절대값과 직접 비교 **금지**. 가치는 *명령어·워크플로·방법론*.
- **Hertz 탄성 + SJKR만 — 소성 전무.** 데모는 순수 Hertz(`A₀=2πRδ`, 변형 무시) + SJKR 점착. **소성 항복 분기 없음**(우리 hooke/hysteresis 소성분기 < 이 문서). *흐름/안식각*엔 충분하나 *압밀*엔 부족 → 우리 18× 연화·Stage-E·MPM이 메우는 영역과 *겹치지 않음*(응용이 다름).
- **rigid 구만.** 입자 SHAPE 흐름·morphology·변형장 전무 — 우리 MPM 영역. "granular soft-particle"의 'soft'는 *overlap 허용*이지 입자 변형 아님.
- **전달 σ 전혀 없음 + 접촉망 dump조차 안 함.** σ_ionic/e/thermal 비교점 0. `pair/gran/local`(우리 네트워크 솔버 입력) 미사용 → frame[5] 역학/흐름 절반만, 그것도 *압밀* 아닌 *흐름*.
- **검증이 toy 수준.** 자유낙하 공(해석해 대조) + 안식각-CED 회귀 = *동역학 sanity*. 우리 다중 소재 외부 앵커(Minnmann·Cronau·Bazzoun·SEM) + scaling-law LOOCV 0.90–0.98 과는 *연구 깊이의 차원이 다름*. **이건 경쟁 모델이 아니라 입문 튜토리얼**임을 명시.
- **안식각 수치(Fig 7–18)는 캡션 stated이나 소재-무관** — CED→안식각 추세만, 절대 안식각·CED를 LPSCl로 전이 금지. 유량 R²=0.90·안식각 R²=0.98은 *그 데모 내부*의 적합도.
- **PUBLIC vs 상용 차이** — 이 문서는 PUBLIC. 우리 input의 일부 고급 기능이 상용/특정 빌드 의존일 수 있음(우리 스크립트는 PUBLIC 호환으로 보이나, 새 기능 추가 시 빌드 확인).

## Supplementary Information

**없음** (이 문서 자체에 SI 별도 없음; 부록 A=단위표, 부록 B=결과+전체 input 스크립트 3종이 본문에 포함). CSV 미생성 — 정량 표는 본 digest §5(CED→안식각 12점)·§3에 직접 기록(별도 소재 데이터 없어 DB 행 가치 낮음; 필요 시 안식각-CED 12점을 `densification_porosity_db.csv`가 아닌 별도 흐름-데모 노트로).

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
