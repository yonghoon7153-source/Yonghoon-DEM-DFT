# Transport and mechanical aspects of all-solid-state lithium batteries — Deysher & Ridley, Meng (Materials Today Physics 2022) [REVIEW]

> slug `deysher2022_transport_mechanical_aspects_assb_review` · DOI `10.1016/j.mtphys.2022.100679` · type `REVIEW (전달 + 역학, 실험 특성화 중심 — 자체 시뮬레이션 없음)` · PDF `Deysher_Meng_2022_MaterTodayPhys_TransportMechanical_ASSB_Review.pdf` · digested `2026-06-26` · status ✅
>
> ## ★★★ 이 논문이 우리에게 무엇인가 (review = positioning, not a competitor) ★★★
> Materials Today Physics 24 (2022) 100679. **Grayson Deysher & Phillip Ridley 공동 1저자**, 교신
> **Y. Shirley Meng** (UC San Diego + Univ. of Chicago).  소재 = **NMC | Li₆PS₅Cl (LPSCl = 우리 SE) | Si/Li**.
> 이것은 **리뷰**다 — 자체 DEM/MPM/FEM 시뮬레이션이 없고, ASSB 복합 양극의 **이온·전자 *전달* 한계**와
> **부피변화에서 오는 *역학* 한계**(void formation, contact loss, stack pressure, Li-metal/anode-less
> 부피팽창)를 *현상 + 실험 특성화 방법* 으로 종합하고 **향후 방향**을 제시한다.
>
> ★ **우리에게 왜 중요한가 (3줄):**
> (1) 이 리뷰의 **중심 프레임 = "전달(transport)이 입자 부피변화 + void formation 때문에 *역학적으로*
> 저해된다"** — 이것이 **정확히 우리 DEM(porosity·접촉망 σ 삼중항)↔MPM(소성 void-fill·변형장) 분업이
> *계산으로 구현* 하는 그 transport↔mechanics 결합**이다.  즉 우리 모델은 이 리뷰가 *말로* 요구하는
> 결합 현상의 **predictive 미세구조→전달+역학 시뮬레이션** 이다.
> (2) **소재계가 우리와 같다**(LPSCl + NMC811) → 리뷰가 인용하는 정량 앵커(areal capacity, current
> density, ASR, stack pressure, 부피변화 %)를 **frame[4] 외부 컨텍스트/검증점**으로 채택 가능 (단 거의
> 모두 *원전 인용* → per-anchor 원 출처를 반드시 병기).
> (3) 리뷰가 명시한 **gap = "복합 양극의 전달을 정량·심층 이해하려면 적절한 echem 측정이 필요"**(Abstract)
> + "양극 미세구조·형상 설계로 전달 최적화" + "역학 물성의 지식 공백" — 이 중 **transport 삼중항·미세구조
> 설계는 우리가 이미 채우고**, **cycling/operando 시간축은 우리도 공유하는 gap** 이다 (frame[5]: 정직한
> 분업 + 우리 contribution 위치).

---

## §0. 이 리뷰의 위치 — 다른 우리 litdb 논문과의 관계 (framing 지도)

이 리뷰는 우리 litdb 의 여러 실험·모델 앵커들이 *왜 중요한지* 를 위에서 묶어 주는 **상위 프레임**이다.
같은 UCSD/Meng 그룹의 두 핵심 논문(Doux 2020, Lee 2025)이 이 리뷰의 *현상* 을 *정량 실험* 으로 뒷받침한다.

| 우리 litdb 항목 | 이 리뷰와의 관계 |
|---|---|
| **Bazzoun 2026** (DEM+RNM σ_ionic, LPSCl+NMC811) | 이 리뷰가 *요구* 하는 "복합 양극 전달의 정량 이해"의 **계산 구현**.  리뷰 §2(전달 한계) ↔ Bazzoun σ_eff,ion 솔버 |
| **Minnmann 2021 JES** (EIS-TLM, NCM622+LPSCl) | 리뷰 §4(echem 특성화 — EIS/TLM)가 *말하는* 측정을 *실제로 수행*; porosity·σ_ion·τ 앵커 |
| **★ Doux 2020** (LPSCl+Li, 같은 그룹) | 리뷰 §3.2(Li-metal 부피변화·creep·stack pressure)의 **1차 실험 데이터**.  리뷰가 ref [37] 등으로 *자기 논문 인용* |
| **★ Lee 2025** (LPSCl+NMC811+VGCF+PTFE, 같은 그룹) | 리뷰 §2.1–2.2(carbon morphology·co-rolling 막)·§3(역학)의 후속 실험 |
| **Kim 2025 / Kang 2025** (Hanyang) | 리뷰가 "future work"로 남긴 *cycling kinetics(R_ct)* + *입계 균열(chemo-mech)* 을 채우는 자매 논문 |
| **우리 DEM+MPM** | 리뷰가 명시 요청한 "transport↔mechanics 정량 모델" 의 **predictive 미세구조 시뮬레이션** (§A·§B·§C) |

> ★ **핵심 포지셔닝:** 이 리뷰는 **현상을 *나열* 하고 *측정* 을 처방** 한다.  우리 모델은 그 현상들을
> **하나의 미세구조에서 *동시에 예측*** 한다 — porosity(압밀), σ_ionic/σ_e/σ_thermal(전달 삼중항),
> coverage(접촉), void-fill flow + 변형장(MPM 역학), fracture(균열).  ⇒ 리뷰 = *지도*, 우리 = *예측 엔진*.

---

## 1. 한 줄 요약
ASSB 의 두 **율속 병목 — (i) 복합 양극의 이온·전자 *전달*, (ii) 부피변화에서 오는 *역학*(void 형성·접촉
손실·stack pressure·Li-metal 팽창) — 을 종합하고, 이를 풀려면 *올바른 echem 특성화*(EIS·CV·DC 분극)가
필수임을 강조하는 리뷰**.  핵심 메시지: SE 의 *벌크* 이온전도도는 이미 충분히 높아졌으니(LGPS 12 mS/cm 등)
**연구 초점은 *복합 양극 내부* 의 전달·역학·계면으로 이동해야 한다**.

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 (SE/CAM/Anode) | 연구유형 |
|---|---|---|---|---|
| **G. Deysher, P. Ridley** (공동 1저자), So-Yeon Ham, J.-M. Doux, Y.-T. Chen, E.A. Wu, D.H.S. Tan, A. Cronk, J. Jang, **Y.S. Meng** (교신; UCSD + Univ. Chicago) | Materials Today Physics **24** (2022) 100679 | 10.1016/j.mtphys.2022.100679 | **NMC** (NCM811 포함) / **Li₆PS₅Cl (LPSCl)** / **Si·Li-metal** | **리뷰** (전달+역학, 실험 특성화 중심) |

- 접수 2022-02-09, 게재 2022-04-04.  Keywords: Characterization, Batteries, Solid-state, Transport, Composites.
- Funding: **LG Energy Solution** (Battery Innovation Contest) + NSF PFI 2044465.  (Meng 그룹 ↔ LGES — 우리 산업 맥락과 동일 계열.)
- 121개 참고문헌.  **자체 데이터/시뮬레이션 없음 — 모든 수치는 인용** (per-anchor 원전 병기 필수, 아래 §3·CSV).

## 3. 핵심 물성 (수치 — *전부 인용값*, 원전 병기)
> ⚠ **이 리뷰는 자체 측정/시뮬이 없다.** 아래 수치는 본문이 *다른 논문에서 인용* 한 값이다.
> cite 시 **반드시 원 출처(ref 번호)** 를 함께 적을 것.  digitized(Fig 곡선 추세) 는 별도 표기.

| 물성 | 값 | 조건 | stated/digitized | 원 출처 (ref) |
|---|---|---|---|---|
| **areal capacity (현 문헌 한계)** | 대부분 **< 2 mAh/cm²** | RT, 다양 | stated (survey) | Fig 1 = refs [1,6,9–28] 종합 |
| **areal capacity (best-case)** | **6.8 mAh/cm²** @ 3.2 mA/cm² | 60 ℃, Ag–C pouch, LiNi₀.₉Mn₀.₀₅Co₀.₀₅O₂(NMC)+LPSCl | stated | Yong-Gun **Lee et al.** [24] |
| **current density (best, full cell)** | **5 mA/cm²**, 80 % 유지 @500 cyc | NCM811+LPSCl μSi full cell, areal **2 mAh/cm²**, 양극 이용률 <50 % | stated | **Tan et al.** [25] |
| **current density (RT Li-metal 한계)** | **< 2 mA/cm²** | RT 대칭셀↔full cell 격차 | stated | Fig 1 / [28,30,32–62] |
| **ARPA-E IONICS 목표** | **3 mA/cm²** (2016) | — | stated (기준선) | Fig 1 녹색 점선 |
| **SE 벌크 σ_ionic (대표 high)** | LGPS **12 mS/cm** (RT) | — | stated | Kamaya [1] (Li₁₀GeP₂S₁₂) |
| **NMC 부피변화** | **1–3 %** (de/lithiation) | layered oxide | stated | [86] |
| **CEI band gaps (LGPS 분해산물)** | GeS₂ **2.3** / P₂S₅ **2.6** / S **2.7** eV | 1st cycle | stated | [89,90] Materials Project |
| **void-fill 회복 압력** | **370 MPa** re-press → lost capacity 상당 회복 | Li₃PS₄+NMC, 첫 수십 cyc 후 | stated | [121] Koerver |
| **양극 이용률 vs porosity** | **< 20 % porosity** 필요 (고-CAM wt%서 full 이용률) | 미세구조 모델링 | stated | [66] **Bielefeld** |
| **유틸 vs porosity (2nd 인용)** | **> 55 %** porosity → 이용률 ↓ | — | stated | [66] Bielefeld |
| **SE 코팅 두께** | **수백 nm** (양극 입자 표면) | solution-precip | stated | [3] |
| **SE 용해-침투 후 SE 감량** | 양극 **~10 vol%**, anode **~20 vol%** 까지 감량(이용률↑) | LPSCl, LiCoO₂/graphite | stated | [78] |
| **이론용량 근접** | LiCoO₂ **141**, graphite **364** mAh/g (SE 침투 후) | — | stated | [78] |
| **SE separator 두께(현 펠릿)** | **~0.5 mm** (감량 대상) | — | stated | [25,67,68,82–85] |
| **얇은 SE 막** | **< 50 µm** cast | LPSCl casting | stated | [23,24,79,80] |
| **Li-metal 부피팽창(anode-less)** | **~5 µm / 1 mAh·cm⁻²** plated Li | NMC811 anode-less | stated | Fig 4b / [25] |
| **Na vs Li 부피팽창** | Na = Li 대비 **~60 % 더** 팽창 (8 µm vs 5 µm per mAh/cm²) | — | stated | 결론 |
| **multilayer 팽창** | 10층 **0.18** / 20층 **0.35** / 30층 **0.53 mm** | NMC anode-less, 4 mAh/cm² | stated (digit. Fig 5) | Fig 5 |
| **critical stack pressure (Li/LLZO)** | Li 수송 위해 임계 stack pressure 필요 (없으면 분극) | Li/LLZO/Li 대칭 | stated | **Wang et al.** [105] |
| **critical stripping/plating 전류** | strip **0.2** (3 MPa) / **1.0** mA/cm² (7 MPa); plate **2.0** (저·고압 공통) | Li/Li₆PS₅Cl/Li | stated | **Kasemchainan et al.** [106] |
| **Li creep yield** | **~0.8 MPa** (1–7 MPa stack서 소성+creep) | Li metal | stated | [107] Masias |
| **Li-alloy 부피팽창** | **> 300 %** (lithiation) | (Li)Si, (Li)Sb | stated | [25] |
| **Li-alloy stack pressure** | **5–150 MPa**(Li-In) / **50 MPa**(Li-Si) | — | stated | [104] / [25] |
| **연료전지차 압력 비교** | passenger car **70 MPa** (H₂ 탱크) | (맥락) | stated | [109] DOE |
| **Li 융점 / Li-alloy 융점** | Li **180.6 ℃**; (Li)Si > **592** / (Li)Sb > **466 ℃** | — | stated | [102]/[103] |
| **LGPS 안정성창(겉보기 vs 실제)** | 겉보기 **0–5 V** vs 실제 환원 **1.71** / 산화 **2.15 V** (vs Li/Li⁺) | — | stated | [110] |
| **LPSCl 산화 한계** | **2.1 V** vs Li/Li⁺ (4.25 V 충전 시 산화) | carbon 효과 실험 | stated | [69] |
| **carbon-composite 셀 bias** | DC 분극 ~**50 mV–** | echem 분리 | stated | Fig 6e / [120] |

> **PSD / coverage / coordination Z / Heckel P_y / σ_thermal:** **n/a** — 리뷰가 이 정량값을 다루지 않음
> (미세구조 *시뮬* 이 아니라 *현상+측정* 리뷰).  형상/크기 효과는 *정성* 으로만(Fig 2a,b SSE:CAM 크기비).

## 4. 시뮬레이션 방법 ★
- **code / version**: **없음 — 리뷰**.  자체 DEM/MPM/FEM/RNM 구현이 없다.
- **DEM/MPM/continuum/전달 솔버**: **n/a** (자체 모델 없음).  단 리뷰가 *인용* 하는 모델링은:
  - **Bielefeld [66]** (= 우리 litdb `bielefeld2019/2020`): 미세구조 모델링 → "porosity < 20 % 면 고-CAM서
    full 이용률" — **우리 porosity↔이용률 결합의 권위 인용** (리뷰가 이 결론을 핵심으로 인용).
  - **Shi et al. [67]**: 3D 복합 양극 이온수송 네트워크 모델 (SSE:CAM 비, SSE 입경 vs CAM 로딩의 이용률)
    — Fig 2a,b.  **= 우리 DEM 접촉망 σ 의 *질적* 선행** (작은 SSE·낮은 CAM:SSE → 이용률↑ = 우리 size=packing).
- **전달 지배식 (인용, Eq 1–3)** ★:
  - σ = n·q·μ (Eq 1, 캐리어 밀도×전하×이동도) — n·μ 둘 다 Li⁺ 위해 최대화.
  - σ = t/(R·A) (Eq 2, 측정저항→σ; **t = SE 두께 → SE 코팅으로 t↓ = σ↑** 가 리뷰 핵심 논리).
  - σ = σ₀·exp(−E_a/RT) (Eq 3, Arrhenius — 고온이 areal capacity 돕는 이유).
- **입자 처리** ★: **n/a (자체 모델 없음)** — 단 리뷰가 *인용* 하는 미세구조 모델([66,67])은 강체-구 + voxel
  기반.  리뷰가 **명시적으로 *역학* 모델 공백을 지적**("significant knowledge gap in the understanding of
  the **mechanical properties** of solid electrolyte materials and their composites") → ★ **이것이 우리 MPM
  (소성 SHAPE 변화)·DEM(역학 압밀)이 채우는 칸**임을 리뷰가 *스스로* 인정.

## 5. Figure set ★
| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| **1** | **문헌 survey: current density vs 발표연도, 점 크기=areal loading, 색=온도·anode 종류.** 대부분 <2 mA/cm²·<0.1 mAh/cm²; ARPA-E 3 mA/cm² 점선; Tan(5 mA/cm²)·Lee(6.8 mAh/cm²) 상단 | **우리 모델의 *목표 좌표*** — current density·areal capacity 가 ASSB 의 율속 지표.  우리 σ 삼중항·porosity 가 이 두 축을 *결정* 하는 미세구조 변수.  Tan/Lee = 우리 소재계 best-case 앵커 |
| **2a,b** | **Li⁺ 네트워크 모식 + SSE-to-CAM 크기비 → 이용률 맵** (CAM loading vol% × SSE size).  작은 SSE·낮은 CAM 로딩 = high utilization | **= 우리 DEM 접촉망 + size=packing의 정성 원형**.  "작은 SSE → 연속 이온망 → 이용률↑" = 우리 작은 SE→σ↑.  단 *정성* (우리는 정량 σ) |
| **2c** | **이용률 vs SSE:carbon 비 — *최적점* 존재** (insulating sulfur cathode) | **= 우리 Furnas-dip / σ trade-off 의 친척** (이온·전자 둘 다 필요 → 중간 최적).  carbon 축이 추가된 형태 |
| **2d** | carbon 유무 → 전압 plateau (carbon 없으면 이용률↓) | 전자 percolation 필요성 = 우리 σ_e f_p 항 |
| **2e** | carbon black / Ketjen / CNT / VGCF **SEM morphology** (비표면적 차이) | **= 우리 CBD morphology 모델 (Super P 0D vs VGCF 1D)** 의 실험 형상 근거 (Lee 2025 와 연결) |
| **2f** | carbon 종류별 분해 kinetics (고비표면 carbon black = 분해↑; VGCF = reduced decomposition) | 우리 σ_e 도전제 형상·산화분해 — VGCF 우수 (Lee 2025 일치) |
| **2g** | **여러 SE 클래스 전기화학적 안정성창** (V vs Li/Li⁺) — sulfide/oxide/halide | 소재 선택 맥락; halide = 더 넓은 산화창 (우리 Varkey/Kim halide 와 연결) |
| **2h** | SE × CAM **반응 에너지** (음수 = 불안정) — sulfide 가장 반응성 | 계면 화학열화 맥락 (우리 미모델 — Kang/Kim 화학 코팅과 연결) |
| **3a** | **★ cathode\|SSE 계면 void formation SEM (pristine vs cycled)** — 부피변화 반복 → 접촉 손실 void | **★ 우리 핵심 그림** — "부피변화 → void → 접촉손실 → 이온수송 제한"의 *실측*.  = 우리 DEM porosity·coverage 손실 + MPM void-fill 이 모델링하는 *그 현상* |
| **3b** | **radially-designed microstructure** (방사상 결정립 → 반경수축 완화) | 미세구조 설계로 부피변화 제어 = 우리 미세구조→역학 예측의 설계 응용 |
| **3c** | LiCoO₂ vs NMC **부피변화 *반대 추세*** (Δ vol < 0 / > 0) → 혼합으로 net-zero | **= 우리 복합 양극 부피변화 설계** (역학 항).  composite-level 부피변화 상쇄 |
| **3d,e** | 부피변화 다른 CAM 혼합 → stack pressure 변화 모니터(Li₄Ti₅O₁₂ zero-strain anode 기준) | stack pressure ↔ 부피변화 결합 = 우리 MPM servo/hold protocol 맥락 |
| **4a** | **Li-metal dense plating SEM** (pristine/charged/discharged) — solid-state Li 는 dense morphology | Li-metal 부피변화(우리 SE 모델 밖 — 전사 금지, 맥락만) |
| **4b** | **cell 부피변화 vs areal capacity** (anode·cathode 기여 분리; Li reservoir ↑면 팽창↑) | anode-less 팽창 정량 (우리 SE/양극 모델과 분리; ⚠ Li-metal) |
| **5** | **multilayer 팽창 ∝ 층 수** (10/20/30층 = 0.18/0.35/0.53 mm) | 스택 설계 맥락 (우리 미세구조 RVE 와 다른 스케일) |
| **6a** | CV: LGPS/LLZO planar electrode (semi-blocking) — 분해 전류 불명확 | echem 특성화 *방법* (우리 σ 의 실험 카운터파트) |
| **6b** | CV: carbon-composite electrode → 분해 전류 증폭 (정확 측정) | "carbon 섞어야 SE 안정성창 제대로 측정" = 측정 방법론 교훈 |
| **6c,d,e** | **MIEC echem 모식 + EIS(2 semicircle) + DC 분극** — 이온·전자 분리 측정 | **= 우리 σ_ionic vs σ_e 분리의 실험 근거** (EIS Nyquist + DC 분극 = Minnmann/Bazzoun TLM 의 개념 기초) |

## 6. Post-processing ★ (리뷰가 *처방* 하는 특성화 — 우리 σ 의 실험 카운터파트)
이 리뷰의 **§4(Electrochemical characterization tools)** 가 핵심 — *우리 σ 삼중항을 실험으로 검증하는 방법론* 의 교과서.
- **무엇 (리뷰가 처방):**
  - **AC 임피던스(EIS)**: 이온/전자 분리.  MIEC(혼합전도체)는 전자 누설 → capacitive tail 사라짐 → **electron-blocking
    layer + composite carbon electrode** 필요 (Fig 6c–e).  **2 연속 semicircle** = 이온·전자 둘 다 기여.
  - **DC 분극**: EIS(이온) + DC(전자 분리, 저bias ~50 mV) **병용** 필수 → 전하전달의 이온/전자 기여 정확 분리.
  - **CV (voltammetry)**: SE 안정성창.  ⚠ **semi-blocking planar 전극은 분해전류 과소** → **carbon-composite
    전극** 으로 측정해야 정확 (Fig 6a vs 6b) — 많은 문헌이 이걸 틀려서 *겉보기* 안정성창을 과대보고 ([110] LGPS 0–5 V 겉보기 vs 실제 1.71–2.15 V).
  - **FIB milling + paired reconstruction** (stack pressure 하에서) → void formation·morphology 변화 정량 ([121]).
- **도구 (인용)**: EIS/DC = 표준; FIB-SEM 재구성 = void 정량.  **자체 도구·코드 없음** (리뷰).
- **수치화·기록:** 리뷰이므로 *현상 종합* + 향후 방향만.  정량 수치는 §3(전부 인용).

---

## A. ★ 우리 DEM+MPM 대비 (comparison vs ours) → `our_dem_baseline.md`

> ★ **이 리뷰의 transport↔mechanics 프레임을 우리 모델에 1:1 매핑.**  리뷰는 *현상 + 측정처방*,
> 우리는 *예측 시뮬* — 리뷰가 *말하는* 결합을 우리가 *수치로 구현* 한다.

### A.1 리뷰의 두 병목 ↔ 우리 두 모델
| 리뷰가 말하는 율속 병목 | 리뷰의 표현 | **우리 모델에서** |
|---|---|---|
| **(i) 복합 양극 전달** | "Li⁺·e⁻ 수송이 양극 composite 에서 *저해*; 양극 입자 부피변화 + void 형성 때문" | **DEM 접촉망 → σ_ionic / σ_e / σ_thermal 삼중항** (Kirchhoff+Holm).  porosity·coverage·coordination·percolation = 전달의 *구조적* 결정변수 |
| **(ii) 부피변화 역학** | "부피변화(NMC 1–3 %)·void formation·contact loss·stack pressure·Li 팽창; 역학 물성 *지식 공백*" | **MPM 소성 void-fill flow + 변형장 Σdg** (압밀 시점) + **DEM fracture** (Auerbach/fracture-Holm) + **porosity/Heckel** (압밀) |
| **(i)↔(ii) *결합*** | "부피변화 → void → **접촉 손실** → 이온수송 제한 → 이용률↓" (Fig 3a) | **이것이 우리 DEM↔MPM 분업의 핵심** — MPM 이 void/소성을, DEM 이 *그 결과 구조의* σ 를 푼다.  ⇒ 우리 = 리뷰 결합의 *계산 실현* |

> ★ **가장 강한 매핑:** 리뷰 **Fig 3a** ("repeated expansion/contraction → interparticle void → loss of
> contact → restriction of ion transport across void") = **우리 DEM porosity·coverage 손실 (전달 저하) +
> MPM void-fill (역학 채움) 가 *정확히* 모델링하는 메커니즘**.  리뷰가 SEM 으로 *보여주고*, 우리가 *예측* 한다.

### A.2 리뷰가 *인용* 한 모델 ↔ 우리
| 항목 | 리뷰 인용 | 우리 | 차이 / 위치 |
|---|---|---|---|
| porosity↔이용률 | Bielefeld [66]: "<20 % porosity 면 고-CAM full 이용률" | 우리 DEM porosity(real_14 15.6 %, pure-SE ~10 %) + σ_ionic 폼 | **우리 porosity 가 그 <20 % 영역** → 리뷰 인용 결론을 *우리 값으로 충족*.  단 그들=stochastic placement(입력 porosity), 우리=압밀(예측 porosity) — 절대 동일시 금지, 결론 방향만 |
| 이온수송망 모델 | Shi [67]: 작은 SSE·낮은 CAM:SSE → 이용률↑ (정성) | 우리 σ_ionic 정량 솔버 (작은 SE→σ↑, size=packing) | **우리가 *정량 σ* 로 그 정성 결론을 수치화** (Bazzoun RNM 도 같은 방향) |
| 전달 σ = t/(R·A) | Eq 2: SE 코팅으로 t↓ → σ↑ | 우리 σ_ionic = f(구조) | 리뷰 = *벌크 두께* 논리; 우리 = *미세구조 접촉망* (더 미시) |
| 역학 모델 | **"mechanical model 지식 공백"** 명시 | **우리 MPM(소성 SHAPE)+DEM(압밀·fracture)** | ★ **리뷰가 *비운 칸* 을 우리가 채움** — 리뷰가 *요청* 한 바로 그 mechanical model |

### A.3 우리만 갖는 것 (리뷰에 없음)
- **정량 σ 삼중항** (σ_ionic LOOCV 0.975 / σ_e 0.953 / σ_thermal 0.90) — 리뷰는 σ 측정 *방법* 만 처방, 예측 솔버 없음.
- **정량 porosity·Heckel·coordination·coverage** — 리뷰는 porosity *임계*(<20 %)만 인용, 우리는 압밀 곡선·Heckel P_y 138.
- **MPM 소성 *형상* 변화·void-fill·변형장** — 리뷰는 void 를 *SEM 으로 관찰*(Fig 3a)만, 우리는 *예측·메커니즘 시각화*.
- **frame[4] 독립 교차검증** (DEM↔MPM 각각 실험 보정) — 리뷰는 단일 관점 종합.

---

## B. ★ 적용가능성 (applicability to our model)

### B.1 채택 가능한 정량 앵커 (frame[4] 외부 컨텍스트/검증점)
> ⚠ **거의 모두 *원전 인용값* + 일부는 Li-metal/스택 스케일 → 우리 SE/양극 미세구조 모델로 *직접 전사 금지*,
> *컨텍스트/목표 좌표* 로만.**  per-anchor 원 출처는 §3·CSV 에.

| 앵커 | 값 | 우리 채널에서 쓰임 | 전사 가능성 |
|---|---|---|---|
| **areal capacity 목표** | best 6.8 mAh/cm² (Lee), 통상 <2 | 우리 모델 *목표 좌표* (porosity·σ 가 결정) | 컨텍스트 (직접 검증 아님) |
| **current density** | best 5 mA/cm² (Tan, NCM811+LPSCl, 우리 소재계!), 통상 <2 | σ 삼중항이 *지지* 하는 상한 맥락 | 컨텍스트 — Tan = 우리 소재계 best-case |
| **양극 이용률 vs porosity** | **<20 % porosity → full 이용률** (Bielefeld [66]) | ★ **우리 porosity 결과(~10–15.6 %)가 이 임계를 *충족*** → "우리 미세구조는 full 이용률 영역" 논증 | **직접 사용 가능** (frame[4]) — 단 placement vs 압밀 porosity 구분 |
| **NMC 부피변화** | 1–3 % | 우리 MPM/DEM *사이클* 부피변화 (현재 *압밀* 만) → 흡수 후보 | 컨텍스트 (우리 미보유 시간축) |
| **void-fill 회복 압력** | 370 MPa re-press → 용량 회복 (Koerver [121]) | ★ **= 우리 MPM void-fill + Doux 비가역 압밀의 거시 증거** | 추세 (우리 압밀압 300 ≈ 370 계열) |
| **stack pressure (작동)** | Li creep yield ~0.8 MPa; 작동 1–7 MPa; critical strip 0.2–1.0 mA/cm² | 우리 압력 *구분*(제조 300 ≠ 작동 수 MPa)의 추가 근거 | 컨텍스트 (Doux 와 합류) |
| **SE 벌크 σ** | LGPS 12 mS/cm (high), LPSCl 산화 2.1 V | 우리 σ_grain 앵커 맥락 (LPSCl 쪽은 Minnmann/Cronau 가 직접) | 컨텍스트 (LGPS≠LPSCl) |
| **CEI band gap** | 2.3–2.7 eV (LGPS 분해) | 우리 미모델 (계면 화학) | 컨텍스트만 |

### B.2 리뷰가 명시한 future-direction ↔ 우리가 *이미 채운* vs *공유 gap*
| 리뷰 future-direction (결론 §5) | 우리 상태 |
|---|---|
| "**복합 양극을 입자크기·조성비로 *체계적으로 설계*** → 고 areal capacity·current density" | ★ **우리가 *이미* 함** — DEM bimodal 12:4:1 + Furnas-dip + 조성 스윕 + 예측 (Phase 1–5 로드맵) |
| "**balancing CAM·SSE 입경** (SSE < CAM 로 최고 이용률 + SE 로딩↓)" | ★ **우리 size=packing·dip 작업이 정량화** (Bazzoun/Minnmann 일치) |
| "**carbon additive 로 전자수송·SE 산화 최소화 동시**" | 우리 σ_e (VGCF/Super P) + Lee/Hong CBD cross-check (부분 — 바인더 페널티는 Stage-2 흡수 backlog) |
| "**전달·전하전달 측정(특히 MIEC) 의 *proper* 특성화**" | ★ **우리 σ_ionic/σ_e 분리 = 그 측정의 *계산* 짝** (Minnmann/Bazzoun EIS 가 실험 짝) |
| "**ML 과 ASSB 모델링이 점점 중요** — 전통 Li-ion 처럼" | ★ **우리 predictor(설계→전 metric 예측) 가 *정확히* 그것** (Phase 3) |
| "**cycling 성능 예측 + 장기 역학 안정성**" | ⚠ **공유 gap** — 우리도 *압밀* 시점만, *사이클* 부피변화·열화는 미보유 (Kang/Kim 자매 논문이 일부, backlog B6) |
| "**operando / paired reconstruction (FIB, stack pressure 하)**" | ⚠ **공유 gap** — 우리는 정적 RVE; operando 시간축 미보유 |

> ★ **핵심:** 리뷰가 *call* 하는 6개 방향 중 **4개(미세구조 설계·입경 balancing·전달 특성화·ML 모델링)를
> 우리가 이미 채우고**, **2개(cycling·operando)는 우리도 공유하는 정직한 gap** 이다.

---

## C. ★ frame[5] 위치 — review = positioning, not a competitor

> 이것은 *리뷰* 다 → 경쟁 시뮬이 아니라 **우리 contribution 을 *위치 지어주는* 프레임**.
> frame[5](분업)·frame[4](교차검증) 관점에서 부드럽게, 그러나 *명확히* 우리 우위를 진술.

### C.1 리뷰가 *비운 칸* = 우리가 채우는 칸
- 리뷰는 **"복합 양극 전달의 *정량·심층* 이해가 필요"**(Abstract) 라고 *요청* 하지만, 자체적으로는 *현상 종합 +
  측정 처방* 까지만 간다.  **우리 DEM 접촉망 σ 삼중항 = 그 정량 이해의 *예측 모델 구현*.**
- 리뷰는 **"역학 물성의 *지식 공백*"**(§1 끝)을 *명시* 한다.  **우리 MPM(소성 SHAPE)+DEM(압밀·fracture) = 그 공백
  을 메우는 mechanical model.**
- 리뷰는 transport↔mechanics 결합을 *말로* 묶지만(Fig 3a 메커니즘), **한 미세구조에서 *동시 예측* 하는 도구는 없다.**
  우리 DEM↔MPM 분업이 그 *동시 예측* 이다.

### C.2 우리 contribution 의 위치 (positioning 문장 후보)
> "This review (Deysher, Ridley & Meng 2022) frames the two coupled bottlenecks of ASSB cathode
> composites — *transport* hindered by particle volume change + void formation, and the *mechanical*
> aspects driving that contact loss — and explicitly calls for the quantitative, in-depth understanding
> and the mechanical models the field lacks.  Our independently-calibrated **DEM (contact-network
> σ_ionic/σ_e/σ_thermal triad) ↔ MPM (plastic shape-change, void-fill flow, strain field)** framework is
> a *predictive microstructure→transport+mechanics realization* of exactly that coupling, on the same
> LPSCl/NMC811 system, providing a more complete computational treatment than the review surveys."

### C.3 정직한 한계 (우리도 공유 / 우리가 더 나음 *둘 다* 명시)
- ★ **우리가 더 완전한 곳 (명확히):** (i) 전달 *삼중항*(리뷰는 이온·전자 *측정 방법* 만; σ_thermal·예측 솔버 없음);
  (ii) *정량* porosity·coverage·coordination·Heckel(리뷰는 porosity *임계*만 인용); (iii) *소성 형상* void-fill +
  변형장(리뷰는 void *SEM 관찰* 만); (iv) frame[4] DEM↔MPM 독립 교차검증.
- ⚠ **공유 gap (정직):** (i) **cycling/operando 시간축** — 우리도 *압밀* 정적 RVE 만 (사이클 부피변화·열화 미보유);
  (ii) **계면 화학열화**(CEI·산화분해) — 우리 *전혀* 미모델 (리뷰 §2.2·Fig 2h 가 다루는 칸, Kang/Kim 화학 코팅이 일부).
- ⚠ **over-claim 금지:** 리뷰의 Li-metal/anode-less 부피팽창(Fig 4–5)은 *Li 상* 의 물리 → 우리 *SE/양극* 모델과
  **상이 다름** → 부피변화 % 절대값 전사 금지, *맥락(셀 스택 설계)* 으로만.

---

## 7. 우리 DEM+MPM 대비 (요약표 — §A 의 압축)
| 항목 | 이 리뷰 | 우리 | 차이 / 위치 |
|---|---|---|---|
| 전달 이해 | *현상 종합 + 측정 처방* (자체 솔버 없음) | σ_ionic/σ_e/σ_thermal *예측* 삼중항 (Kirchhoff/Holm) | ★ **우리 = 리뷰가 요청한 *정량 모델*** |
| 역학 | "지식 공백" 명시 (void *SEM 관찰* 만) | MPM 소성 void-fill·변형장 + DEM fracture | ★ **우리 = 리뷰가 비운 mechanical model** |
| transport↔mechanics 결합 | *말/그림* 으로 묶음 (Fig 3a) | DEM↔MPM 분업이 *동시 예측* | ★ **우리 = 결합의 계산 실현** |
| porosity↔이용률 | <20 % 임계 *인용* (Bielefeld) | 우리 porosity ~10–15.6 % = 그 영역 *충족* | frame[4] — placement≠압밀 구분 |
| 정량값 출처 | *전부 인용* (자체 측정 0) | 자체 시뮬+실험 앵커 | 리뷰 = 지도, 우리 = 엔진 |
| cycling/operando | future-direction 으로 *요청* | ⚠ 우리도 미보유 (정적 RVE) | **공유 gap** (정직) |

## 8. 적용 인사이트 (내 연구에 어떻게)
- ① **리뷰를 우리 *프레임 인용* 으로**: 논문/deck 서론에서 "ASSB 의 transport↔mechanics 결합이 율속(Deysher 2022) →
  우리 DEM↔MPM 이 그 결합의 predictive 미세구조 시뮬" 로 위치.  **same-material(LPSCl+NMC811) 권위 리뷰.**
- ② **Fig 3a void→contact loss = 우리 핵심 그림의 *실험 짝***: 우리 DEM porosity/coverage 손실 + MPM void-fill 의
  *현상* 을 리뷰 SEM 으로 정당화.  "리뷰가 관찰, 우리가 예측."
- ③ **<20 % porosity 임계(Bielefeld [66], 리뷰 인용) 채택**: 우리 porosity(~10–15.6 %)가 *full 이용률 영역* 에
  있음을 frame[4] 로 진술 (placement vs 압밀 porosity 구분 명시).
- ④ **future-direction 4/6 우리가 채움 (강점 진술)**: 미세구조 설계·입경 balancing·전달 특성화·ML — 리뷰 §5 가
  *call* 한 방향을 우리가 *이미 구현* (Phase 1–5).  cycling/operando 2개는 정직 gap.
- ⑤ **echem 특성화 §4 = 우리 σ 의 실험 검증 *방법론***: EIS(이온)+DC 분극(전자) 분리 = 우리 σ_ionic/σ_e 분리의
  실험 짝 → Minnmann/Bazzoun TLM 앵커와 연결.  CV semi-blocking 함정(겉보기 안정성창 과대) = 측정 주의 인용.

## 9. 인용 가능 문장 (deck/paper용)
- "Deysher, Ridley & Meng (Mater. Today Phys. 2022) review the two coupled bottlenecks of ASSB cathode
  composites — ionic/electronic *transport* hindered by particle volume change and void formation, and the
  *mechanical* aspects driving that contact loss — on the same Li₆PS₅Cl/NMC system, and explicitly call for
  the quantitative understanding and mechanical models the field lacks."
- "Our DEM contact-network σ-triad (σ_ionic/σ_e/σ_thermal) and MPM plastic-shape/void-fill model provide a
  predictive microstructure→transport+mechanics realization of the transport↔mechanics coupling this review
  frames qualitatively (e.g. its Fig 3a void-formation/contact-loss mechanism)."
- "The review's adopted criterion — *< 20 % cathode porosity is needed for full active-material utilization
  at high CAM weight fractions* (Bielefeld) — places our computed composite porosities (~10–15.6 %, LPSCl)
  squarely in the full-utilization regime."

## 10. 주의/한계 (over-claim 방지)
- **리뷰 = 자체 측정/시뮬 0**: §3 의 *모든* 수치는 인용값.  cite 시 **반드시 원전(ref 번호)** 병기 — 리뷰를
  1차 출처로 인용하면 안 됨 (예: porosity<20 % → Bielefeld [66]; 6.8 mAh/cm² → Lee [24]; void-fill 370 MPa → Koerver [121]).
- **Li-metal/anode-less 부피팽창(Fig 4–5)**: *Li 상* 물리 → 우리 *SE/양극* 미세구조 모델과 **상이 다름** → 부피변화 %·
  팽창 µm 절대값 *전사 금지*, 셀-스택 설계 *맥락* 으로만.
- **LGPS 12 mS/cm 등 *벌크 SE σ*** : 우리 σ_grain 앵커와 *소재 다름*(LGPS≠LPSCl) → LPSCl 쪽은 Minnmann 1.6/Cronau 3.0
  이 직접 앵커 (이 리뷰는 σ *맥락* 만).
- **porosity↔이용률 <20 %** (Bielefeld 인용): 그들 = *입력* porosity(stochastic placement); 우리 = *압밀* porosity
  (예측) → 절대 동일시 금지, *임계 영역 충족* 논증만.
- **전달·역학 결합을 우리가 *모두* 푼다고 과장 금지**: cycling 부피변화·계면 화학열화·operando 는 우리도 *미보유*
  (리뷰가 future-direction 으로 남긴, 우리도 공유하는 gap) — frame[5] 정직.
- digitized 값(Fig 5 multilayer 팽창 0.18/0.35/0.53 mm 등)은 곡선 추세 — 정밀값 아님.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
