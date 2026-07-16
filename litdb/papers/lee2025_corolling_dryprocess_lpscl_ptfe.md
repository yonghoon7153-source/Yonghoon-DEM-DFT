# Co-rolling dry-process로 만든 박막 LPSCl SSE — robust 계면 + 저압(2 MPa) 작동 — Lee (Nat. Commun. 2025)

> slug `lee2025_corolling_dryprocess_lpscl_ptfe` · DOI `10.1038/s41467-025-59363-4` · type `exp` (실험, no DEM/MPM) · PDF `Lee_2025_NatCommun_corolling_dryprocess_LPSCl_PTFE.pdf` (main) + `..._Sup.pdf` (SI 40 p) · digested `2026-06-24` · status ✅ · Open Access CC-BY

## 1. 한 줄 요약
**우리와 정확히 같은 소재(LPSCl <1 µm SE + NCM811 PC-NCM/NCM82 SC-NCM CAM)·같은 두 도전첨가제(VGCF + PTFE)**로
건식 co-rolling 박막 양극을 만든 **순수 실험** 논문 — DEM/MPM 시뮬은 없지만 (a) **PTFE wt%가 σ_ionic·σ_e를 둘 다
죽이는 직접 정량곡선**(Supp Fig 5: 0.5/2/5 wt% → σ_e 34/4.5/0.011 mS/cm), (b) **fibrillated binder-VGCF 네트워크의
실험적 SEM 증거**(Fig 3h,i + Supp Fig 17/18 = 우리 PTFE CBD curl/carbon-nucleation 모델의 검증), (c) **PC-NCM 균열
vs SC-NCM 무손상**(우리 DEM AM_P 파괴 관찰의 실험 대응)을 제공 → 우리 전달/CBD/파괴 모델의 **frame[4] 외부
실험 앵커**.  (Bazzoun처럼 경쟁 모델이 아니라 *실험 측 검증*.)

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 (SE/CAM/도전제/바인더) | 연구유형 |
|---|---|---|---|---|
| Dong Ju Lee, Yuju Jeon, Jung-Pil Lee, …, Jiyoung Kim, **Zheng Chen** (UC San Diego + **LG Energy Solution**) | Nat. Commun. **16**, 4200 (2025) | 10.1038/s41467-025-59363-4 | **Li₆PS₅Cl (LPSCl, <1 µm)** + **NCM811 (PC-NCM, polycrystalline 5–15 µm) / NCM82 (SC-NCM, single-crystal 3–5 µm)** + **VGCF** + **PTFE (<300 nm)** | **실험** (건식 co-rolling 막 제조 + EIS/DCP 전달 + cell cycling); **시뮬레이션 없음** |

핵심 레시피(우리와 거의 동일, Supp Table 1 "This work" 열):
- **양극** CAM:SSE:VGCF:PTFE = **80:17:3:0.5 wt%** (우리: 80:18:1:1 → 그들 VGCF↑·PTFE↓), areal 5 mAh cm⁻², 두께 120 µm, areal mass 31.4 mg cm⁻².
- **SSE 층** LPSCl:PTFE = **100:0.1 wt%**, 두께 **50 µm**, areal mass 8.2 mg cm⁻².
- 음극 Si:LPSCl:VGCF:PVDF (full-cell, NCM82, N/P 1.4). 셀 nominal 3.35 V, 총 두께 205 µm.

## 3. 핵심 물성 (수치)  ★
> ⚠ 모두 **실험 측정값 (stated)**, digitized 아님.  σ는 EIS(Li⁺)·DCP(e⁻)로 셀 형상에서 추출.

| 물성 | 값 | 조건 (P, 조성) | stated/digit | 비고 |
|---|---|---|---|---|
| **σ_ionic (양극)** | **0.069 / 0.024 / 0.007 mS/cm** | PTFE **0.5 / 2 / 5 wt%**, CAM:SSE:VGCF=80:17:3 고정, 75 MPa | stated (Supp Fig 5) | ★ **바인더가 σ_ionic을 죽인다** |
| **σ_e (양극, VGCF망)** | **34 / 4.5 / 0.011 mS/cm** | PTFE **0.5 / 2 / 5 wt%** 동일 | stated (Supp Fig 5) | ★ **바인더가 σ_e를 3,000× 죽인다** (0.5→5 wt%) |
| σ_ionic (양극, co/free) | **0.076 / 0.069 mS/cm** | 0.5 wt% PTFE, co-rolled / freestanding | stated (Fig 4e) | 거의 동일(조성 동일) → 잘 분산된 SSE |
| σ_e (양극, co/free) | **33 / 34 mS/cm** | 0.5 wt% PTFE | stated (Fig 4f) | VGCF 전자망 잘 형성, co/free 무관 |
| **σ_ionic (SSE 층)** | **1.04 (co-rolled) / 1.29 (freestanding) mS/cm** | SSE 100:0.1 PTFE | stated (Fig 4c) | co-rolled가 **얇은 SSE 덕에 conductance↑** (1.04는 *intrinsic* 전도도; conductance 164 vs 20 mS는 두께차) |
| σ_e (SSE 층, 절연) | **1.4×10⁻⁷ / 2.6×10⁻⁷ mS/cm** | co / free | stated (Fig 4d) | SSE는 전자절연 ✓ (전자누설 적음) |
| σ_ionic (bulk LPSCl) | pristine **2.19** / ball-mill **1.64 mS/cm** | pellet | stated (Supp Fig 4e) | 볼밀(입자↓) 후 σ 유지(소폭↓) |
| σ_e (bulk LPSCl) | pristine **5.0×10⁻⁴** / ball-mill **3.3×10⁻⁴ mS/cm** | pellet DCP | stated (Supp Fig 4f) | |
| **PSD** | SSE **<1 µm** (볼밀); PC-NCM **5–15 µm**, SC-NCM **3–5 µm** | | stated (Methods) | SE≪CAM = 우리 12:4:1 동기 |
| PTFE 초기 입자 | **<300 nm** (Chemours) | | stated (Methods) | = 우리 CBD 초기 노드 크기 분포 입력 |
| **PTFE 모듈러스** | storage modulus **30→120 °C서 67% 감소** (≈150→50 MPa) | DMA 1 Hz | stated (Supp Fig 10) | ★ 온도↑→바인더 연화→균일 층 (우리 E_eff 연화 정당화의 *바인더판*) |
| 인장강도 | SSE **0.049** / 전극 **0.441** / co-rolled **0.510 N cm⁻¹** | n=5 | stated (Fig 3b) | co-rolled ≈ 두 막의 합 → 둘 다 하중분담 |
| 적층비중 specific energy | **310 Wh kg⁻¹ (stack)** / **805 Wh L⁻¹** ; CAM-level 660 Wh kg⁻¹ | pouch, 5 mAh cm⁻², 30 °C, 5 MPa | stated (Fig 6c,f, Supp Note 1) | |
| 저압 작동 | **2 MPa서 >80% 유지 500 cyc** (0.5 C); 75 MPa서 >95% | LiIn‖LPSCl‖NCM | stated (Fig 5a,b) | ★ 저압(2 MPa ≪ 통상 75 MPa) 작동 |
| 균열(Fig 2b,c) | **PC-NCM 균열(debris)** / **SC-NCM 무손상** | press 후 | stated (SEM) | ★ = 우리 DEM AM_P(다결정) 파괴 |

**Heckel / porosity / coordination Z / coverage% / E_SE / σ_y**: **n/a** — 압밀 모델·정량 porosity·접촉면적·배위수·탄성계수 측정 **없음** (실험 막, void 정성 segmentation만; §10 참조).

## 4. 시뮬레이션 방법 ★
- **code / version**: **없음** — 순수 실험.  DEM·MPM·FEM·RNM 일절 없음.
- **DEM 접촉법칙 / 재료 파라미터 (E,ν,μ,COR,σ_y)**: **n/a** (시뮬 없음 → E_SE, σ_y, ν, 마찰 측정 안 함).
- **bond/binder 모델**: 모델은 없으나 **PTFE 섬유화 메커니즘을 실험·모식도로 제시**(Supp Fig 18a, §5) —
  우리 CBD 시드 모델의 물리 그림과 1:1: (i) 계면 접촉 형성, (ii) shear로 입자 이동+바인더 응력,
  (iii) 바인더 **stretched & fibrillated across interface**, (iv) 새 접촉 형성, (v) 두께감소 step마다 반복.
- **MPM/continuum / 전달 솔버**: **n/a**.  전달은 **실험 EIS(Li⁺) + DCP(e⁻)** 로 측정 (솔버 아님).
- **입자 처리** ★ (DEM판 "무질서 처리"): 실험이라 입자 모델 없음.  **그러나** 이 논문이 보여주는 실제 입자 거동이
  우리가 모델로 흉내내는 두 가지를 **실험으로 확인**: (a) PC-NCM은 **진짜로 깨진다**(rigid sphere가 아님 — 우리 DEM
  AM_P 파괴/Auerbach가 맞는 방향), (b) PTFE는 **진짜로 소성 draw·fibrillate**(우리 CBD vol-conserve draw d∝√(V/L)).
  SC-NCM은 안 깨짐 → AM_S는 rigid에 가깝다는 우리 가정 지지.
- **도메인/RVE / servo / seeds / 압력범위**: **n/a** (셀 제조 압력 500 MPa fabrication, 작동 stack pressure 2/5/75 MPa).
- **특이사항/공정 레버 (P1–P3, 우리 시뮬 입력에 시사점)**:
  - **P1 CAM 입자**: large PC-NCM(5–15 µm) vs small SC-NCM(3–5 µm) → SC-NCM이 압밀 전부터 dense·intimate
    contact, PC-NCM은 거친 표면 + 큰 CAM/작은 SE 사이 큰 void → press시 심한 균열 (= 우리 12:4:1 packing + AM_P 파괴).
  - **P2 co-rolling 온도**: 30 °C → 비균일 층, 120 °C → 균일 층 (바인더 모듈러스 67%↓; Supp Fig 10).
  - **P3 reduction 두께**: 20 µm → distinct SSE/cathode 층, 100 µm → 전극이 SSE로 **침투**(과변형) → 120 °C/20 µm 채택.

## 5. Figure set ★
| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| **M1** | conventional vs co-rolling 모식 + SSE두께↔균열위험 | 우리 박막 SSE 맥락 (우리 모델은 RVE — 막 제조 단계는 다룸 안 함) |
| **M2 a** | P1–P3 공정 모식 | CAM 크기·온도·두께 레버 |
| **M2 b,c** | ★ **large PC-NCM = "Cracked CAM"(debris) / small SC-NCM = "Intact CAM"** (press 후 SEM) | ★ **우리 DEM AM_P 다결정 파괴(37–40% in 92:8 8mAh)의 실험 증거** + AM_S rigid 지지 |
| **M2 d,e** | 30 °C 비균일 / 120 °C 균일 층 (단면) | 바인더 연화 = 우리 E_eff 연화의 바인더판 정당화 |
| **M2 f,g** | 100 µm 전극침투 / 20 µm distinct 층 | 과변형 vs 적정 — 우리 over-compression 캡과 같은 맥락 |
| **M2 h,i** | ★ as-fab vs **pressed** SEM + EDS(S/Cl on SSE side, S/Ni on electrode side) | press가 SSE 입자 접촉 형성 (우리 DEM 접촉망 형성의 실험 대응) |
| **M3 b** | 인장강도 SSE 0.049 / 전극 0.441 / co-rolled 0.510 N cm⁻¹ | co-rolled ≈ 합 → 두 막 하중분담 (우리 AM-shielding과 결 같음) |
| **M3 d–i** | peel-off (freestanding 1회만에 분리 vs co-rolled 10회도 안 떨어짐) + ★ **Fig 3h side-view SEM + Fig 3i 모식: "binder-VGCF network" (꼬불꼬불 squiggle 선으로 그림)** | ★★ **우리 PTFE CBD curl + carbon-nucleation 모델의 실험 SEM + 개념도** |
| **M3 j–l** | shear가 (i) 바인더 fibrillation (ii) 접촉 형성 → freestanding=heterogeneous, co-rolled=fused 계면 | shear→fibril = 우리 fibril-by-shear 시드 가정 |
| **M4 a–f** | Li⁺/e⁻ 전달 (SSE·전극) EIS/DCP: σ_ionic 1.04/1.29(SSE), 0.076/0.069(전극); σ_e 33/34(전극, VGCF) | **전달 절대 앵커** (조성별·co/free) |
| **M4 g–i** | 내부저항(분극), shelf-life(전자누설), stack pressure DRT (2 vs 75 MPa) | 저압 작동시 void 형성 ↔ 분극 |
| **M5 a,b** | ★ **2 MPa서 >80% / 75 MPa서 >95% 유지 (500 cyc)** | 저압 작동 = 우리 σ-vs-P·void 동기 |
| **M5 e,f** | cycling 후 단면 void: co-rolled 계면 intact / freestanding 심한 **interfacial voids** (75→2 MPa서 free void ratio 4.0→15.5, co 1.9→3.5) | void 정성 정량 (우리 porosity와 다른 축 — 사이클 후 계면) |
| **M6** | high-energy Si full-cell + pouch (310 Wh kg⁻¹, 805 Wh L⁻¹) | 실용 셀 데모 (우리 모델 범위 밖) |
| **SI Fig 4** | pristine vs ball-mill LPSCl: σ_ion 2.19→1.64, σ_e 5e-4→3.3e-4 | bulk LPSCl σ 앵커 (Bazzoun pellet 1.02·Cronau 단결정 3.0과 비교) |
| **★ SI Fig 5** | ★★ **PTFE 0.5/2/5 wt% → σ_ionic 0.069/0.024/0.007 · σ_e 34/4.5/0.011 mS/cm** (CAM:SSE:VGCF 80:17:3 고정) | ★★★ **우리 Stage-2 "carbon+binder→σ_e" 직접 보정/검증 곡선 + "PTFE가 σ 죽인다" 경고** |
| **SI Fig 6** | PC-NCM 표면: as-fab "Void" 多 → pressed "Microvoids" → BSE "**Cracked particles with debris**" | AM_P 파괴 정성 |
| **SI Fig 7** | SC-NCM: "Smooth surface" → "Intimate contacts" → "**Intact particles**" | AM_S 무손상 |
| **SI Fig 8** | PC/SC-NCM @300 vs 500 MPa: PC 500서 균열↑(debris), SC 균열 없음·접촉↑ | 압력↑→PC 더 깨짐 (압력의존 파괴) |
| **SI Fig 10** | ★ **PTFE storage modulus 30→120 °C서 67%↓** | 바인더 연화 정량 (우리 E_eff 연화 바인더판) |
| **★ SI Fig 17** | ★★ **"Fibrillated network of binder-VGCF at the interface"** (SE/BSE mode, 계면 곡선 섬유망) | ★★★ **우리 CBD fibril web의 실험 SEM** |
| **★ SI Fig 18** | ★★ **(a) 바인더 fibrillation 메커니즘 5단계 모식 (CAM·SSE·VGCF·꼬불꼬불 binder), (b) 초기/최종 co-rolling 단면 — "Binder fibrillation across interface" 화살표** | ★★★ **우리 curl + nucleate-on-carbon + draw 모델의 메커니즘 그림 그대로** |
| **SI Table 1** | dry-process SSE 문헌 비교 (Ref 35/46/47/48/49/50 vs This work) — 레시피·두께·성능 | 우리 레시피 출처 + 문헌 정합 |

## 6. Post-processing ★
- **무엇**:
  - 전달: **EIS** (7 MHz–0.1 Hz, full-blocking/non-blocking 셀) → **Z-type 등가회로 피팅** (SSE: R1-CPE1; 전극: R1-(R2‖CPE2)-(R3‖CPE3)-CPE4, Supp Fig 20) → R 추출 → **σ = l/(R·A)** (eq 1).  e⁻는 **DCP**(직류분극, R=V/I, eq 2).
  - void 분석: 단면 SEM → **ImageJ threshold(하위 5%) segmentation** → void area fraction (Electrode/Interface(10 µm 고정)/SSE 3영역, Supp Fig 27–29).  **이건 우리 porosity와 다른 축**: 사이클 후 *계면 void* 비율(상대), DEM 압밀 porosity 아님.
  - 역학: 인장(MARK-10), **DMA**(PTFE 모듈러스 vs 온도), peel-off, micro-CT (Zeiss Xradia, Amira-Avizo).
  - DRT(분포완화시간, DRTtools/RBF)로 SSE-양극 저항 진화 분리.
- **도구**: ZView/RELAXIS류 EIS 피팅, **ImageJ**(void), Amira-Avizo(CT), CasaXPS(XPS), DRTtools.
- **수치화·플롯·기록**: σ는 모두 셀에서 측정→eq1/2로 환산 (시뮬 정규화 아님 = **절대값**).  void는 상대비(SSE 대비).

## 7. 우리 DEM+MPM 대비  →  `our_dem_baseline.md`
| 항목 | 이 논문 (Lee 2025, 실험) | 우리 (DEM+MPM) | 차이 / 이유 |
|---|---|---|---|
| 성격 | **실험 막** (no model) | DEM(전달)+MPM(역학) 시뮬 | frame[4] — **그들 실험 = 우리 외부 앵커**, 경쟁 모델 아님 |
| 소재 | **LPSCl + NCM811/82 + VGCF + PTFE** | **동일** | ★ **소재·도전제 모두 동일** (Bazzoun보다 더 — 바인더·VGCF까지) |
| 레시피 | 80:17:3:0.5 (양극) / 100:0.1 (SSE) | 80:18:1:1 | 그들 **VGCF↑(3 vs 1)·PTFE↓(0.5 vs 1)** → σ_e 더 높고 바인더 손실 적음 |
| σ_ionic (전극) | **0.076 mS/cm** (0.5 wt%, 75 MPa) | 우리 σ_ionic 폼 (LOOCV 0.975) | 그들 = 절대 실측 검증점 (단 PTFE/VGCF 함량 다름 → 직접 매핑시 보정) |
| σ_e (전극) | **33–34 mS/cm** (VGCF망) | 우리 σ_e Stage 22.5 (LOOCV 0.953), σ_AM 앵커 | ★ 그들 = **VGCF 전자망 절대 앵커**; PTFE wt% 곡선 = Stage-2 보정 |
| **PTFE 영향** | ★ **0.5→5 wt%서 σ_e 34→0.011 (3,000×↓), σ_i 0.069→0.007 (10×↓)** | 우리 CBD는 σ_e *기여*만 모델, **PTFE 절연 페널티 미반영** | ★ **흡수 1순위**: PTFE wt%↑ → σ 양쪽 다 죽임 (절연+접촉차단) |
| 바인더 fibril 망 | ★ SEM+모식 실측 (Fig 3i, SI 17/18) | 우리 CBD: curl·vol-conserve·nucleate-on-carbon 시드 모델 | ★ **그들 SEM = 우리 CBD 모델의 실험 검증** (`docs/cbd_morphology_roadmap.md`) |
| AM 파괴 | ★ **PC-NCM 깨짐 / SC-NCM 무손상** (SEM) | 우리 DEM AM_P 파괴 37–40%, Auerbach | ★ **실험 검증** (AM_P 다결정 깨짐·AM_S rigid) |
| porosity 정량 | 없음 (void 상대 segmentation만) | DEM 15.6% / MPM 16.7% @300 (Minnmann 10%) | 그들은 압밀 porosity 안 줌 → **우리 강점**(정량 porosity·Heckel) |
| 전달 솔버 | 없음 (실험 EIS/DCP) | Kirchhoff/Holm + Stage-E + 삼중항 σ_i/σ_e/σ_thermal | **우리 강점**(명시적 접촉망·삼중항 스케일링) |
| morphology/변형장 | SEM 정성 (PC 깨짐) | MPM 진짜 소성 형상변화·void-fill·Σdg | **우리 강점**(MPM 정량 변형장) |

## 8. 적용 인사이트 (내 연구에 어떻게)  ★
- ① **★ PTFE wt% → σ 페널티 곡선 흡수 (Stage-2/σ_e 보정 1순위)**: Supp Fig 5의
  PTFE 0.5/2/5 wt% → **σ_e 34/4.5/0.011 · σ_ionic 0.069/0.024/0.007 mS/cm** 는 우리가 *안 갖고 있던*
  데이터 — 우리 σ_e/σ_ionic 폼은 도전제 *추가*만 반영하고 **바인더가 접촉을 막고 절연한다**는 페널티가 없다.
  → CBD가 σ_e에 *기여*(VGCF 전자망)하면서도 PTFE wt%↑면 **σ 양쪽 다 급감**하는 비단조성을 추가.  `docs/data/lee2025_transport_anchors.csv`.
- ② **★ binder-VGCF fibril 망 = 우리 CBD 모델 실험 검증**: Fig 3i 모식(꼬불꼬불 binder가 VGCF를 그물친 그림) +
  SI Fig 17/18(SEM 섬유망 + 5단계 fibrillation 모식)은 `docs/cbd_morphology_roadmap.md`의 **curl(worm-like) +
  nucleate-on-carbon + shear-draw** 그림과 *그대로 일치* → 우리 CBD 시드 모델(batch 1: curl/vol_cv/vol_conserve/
  nucleate/thickness)이 *literature-grounded*라는 직접 인용 근거 (frame[4]).
- ③ **★ PC-NCM 균열 / SC-NCM 무손상 = 우리 AM 파괴 모델 검증**: 우리 DEM이 AM_P(다결정)에서 37–40% 파괴를
  내고 AM_S를 rigid로 두는 것이 *실험으로 옳다* — Fig 2b,c + SI Fig 6–8 (PC debris vs SC intact, 300→500 MPa서
  PC 균열↑).  → Auerbach/fracture-Holm 검증점 + "AM_P만 깨고 AM_S는 안 깬다"의 실험 라이선스.
- ④ **바인더 연화(DMA 67%↓)** = 우리 E_eff 18× 연화의 *바인더 측* 물리 보강 (온도↑→σ_y↓→압밀↑, Bouvard 2000과 같은 결).
- ⑤ **bulk LPSCl σ_ionic 2.19 mS/cm (pellet, pristine)**: Bazzoun pellet 1.02·우리 Cronau 단결정 3.0 사이 —
  세 번째 LPSCl bulk 앵커점 (입자/GB·측정법 차이 대조).

## 9. 인용 가능 문장 (deck/paper용)
- "An industrial dry-processed LPSCl/NCM811 electrode with the identical conductive-additive pair we model
  (VGCF + PTFE; Lee et al., Nat. Commun. 2025) shows by SEM a **fibrillated binder–VGCF network bridging the
  SSE–electrode interface** — direct experimental validation of our curl + carbon-nucleated CBD seeding model."
- "Lee et al. quantify that raising the PTFE binder from 0.5 to 5 wt% collapses the composite electronic
  conductivity from 34 to 0.011 mS cm⁻¹ (≈3,000×) and the ionic from 0.069 to 0.007 mS cm⁻¹ — a binder
  insulation/contact-blocking penalty we adopt into our σ_e/σ_ionic model."
- "Polycrystalline PC-NCM cracks into debris under pressing while single-crystal SC-NCM stays intact
  (Lee 2025, SEM) — experimentally confirming our DEM treatment of AM_P fracture (37–40%) vs rigid AM_S."

## 10. 주의/한계 (over-claim 방지)
- **시뮬레이션 0** — DEM/MPM/FEM/RNM 없음.  porosity(정량)·Heckel·coordination Z·coverage%·E_SE·σ_y·접촉면적
  **전부 n/a**.  void 분석은 *사이클 후 계면 void의 상대비*(ImageJ threshold)이지 압밀 porosity 아님 → 우리 15.6%와 직접 비교 금지.
- **레시피 차이**: 그들 양극 **VGCF 3 wt%·PTFE 0.5 wt%** vs 우리 1·1 → σ_e 절대값을 우리 케이스에 그대로 옮기지 말 것
  (VGCF↑면 σ_e↑, PTFE↓면 손실↓).  σ는 *추세·페널티 형태*로 흡수, 절대 매핑은 함량 보정 후.
- **σ_ionic(SSE) 1.04 vs 1.29**: co-rolled가 *낮다* — 이건 **압밀이 더 나빠서가 아니라** freestanding이 500 µm
  두꺼운 SSE라 측정 형상이 다름(논문 명시).  conductance(164 vs 20 mS)는 두께차.  **intrinsic σ 비교는 조심**.
- **bulk LPSCl σ 2.19**(pristine pellet)는 측정·입자·GB 조건이 Bazzoun 1.02·Cronau 3.0과 달라 — 절대값 직접
  대조 말고 "세 앵커의 스프레드"로만.
- **막 제조 단계(co-rolling shear)** 는 우리 RVE 모델이 *안 다루는* 공정 영역 — fibrillation 메커니즘은 *개념적
  검증*으로 쓰되, 우리 시뮬이 그 shear 공정을 재현한다고 주장 금지.
- σ·void·강도 외 정량 표(Supp Table 2,3 EIS 피팅 R/CPE)는 회로 파라미터 — 직접 물성 아님(참고용).
- **frame[4]/[5]**: 이 논문은 *실험 절반*(transport 실측 + morphology SEM)을 줌; *모델 절반*(명시적 접촉망 σ
  삼중항·MPM 변형장·Auerbach·Heckel)은 **우리가 추가**.  수렴=교차검증, 함량차로 인한 불일치=정량화된 레시피 효과.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
