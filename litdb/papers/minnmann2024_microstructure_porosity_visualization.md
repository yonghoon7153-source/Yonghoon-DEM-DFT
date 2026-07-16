# 복합 양극 미세구조·porosity → SSB 성능을 FIB-SEM 토모그래피로 *시각화* — Minnmann (J. Electrochem. Soc. 2024, Editors' Choice)

> slug `minnmann2024_microstructure_porosity_visualization` · DOI `10.1149/1945-7111/ad510e` · type `exp` (FIB-SEM 토모 + EIS-TLM + 사이클; 보조 flux/random-walk τ 시뮬) · PDF `Minnmann_2024_JES_CompositeCathodeMicrostructure_Porosity_Visualization.pdf` · digested `2026-06-26` · status ✅

## 1. 한 줄 요약
**우리 핵심 porosity 앵커 저자(Minnmann, Janek 그룹)의 2024 Editors' Choice** — SE(ISE) 입경만 바꾼 3개 복합 양극(BM10/BM03/BM01)을
**Xe-plasma FIB-SEM 토모그래피로 3D 재구성**하여 **porosity·상분율·계면면적·chord length·tortuosity를 정량화**하고,
이를 **EIS-TLM 유효전도도 + full-cell 사이클 성능**과 직접 상관시킨 *실험* 논문.  핵심 발견: **작은 SE 입자 → 더 균질한 미세구조 →
잔류 porosity↓ + CAM-ISE 계면면적↑ + ionic tortuosity↓ → CAM 이용률↑(62→77 %) + 율속↑** (BM10 92 vs BM03/BM01 156/152 mAh/g @0.1C).
★ **porosity 가 이온수송에 *주역 병목*** 임을 토모로 *시각화* — 우리 DEM(porosity·접촉망 σ)·MPM(소성 void-fill)이 *모델링하려는 바로 그 구조→성능 사슬*을 실험이 보여줌.
이 논문은 **우리가 calibrate-to-experiment(frame[4]) 하는 Minnmann 계보의 2024 버전**으로, **σ_ion 절대값·CAM-ISE 계면면적·tortuosity·CAM 이용률**을 외부 검증점으로 제공한다.

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 (SE/CAM) | 연구유형 |
|---|---|---|---|---|
| **Philip Minnmann**, Johannes Schubert, Sascha Kremer, René Rekers, Simon Burkhardt, Raffael Ruess, Anja Bielefeld, Felix H. Richter, **Jürgen Janek** (교신) (Justus-Liebig-Univ. Giessen + KIT-BELLA) | **J. Electrochem. Soc. 171 (2024) 060514** (Editors' Choice, **Open Access**, 제출 2024-03-24 / 게재 2024-06-11) | 10.1149/1945-7111/ad510e | **ISE = Li₃PS₄–0.5LiI (glassy thiophosphate, "1.5Li₃PS₄·0.5LiI")** + **CAM = LiNi₀.₈₃Mn₀.₀₆Co₀.₁₁O₂ (NCM, single-crystal D50 3–5 µm)**; **separator = Li₆PS₅Cl (LPSCl)** | **실험** (PFIB-SEM 토모 3D 재구성 + EIS-TLM 부분전도도 + galvanostatic 사이클); 보조 **flux/random-walk tortuosity 시뮬**(GeoDict ConductoDict / Pytrax) |

> ⚠ **소재 주의 — 이 논문의 *복합 양극* SE 는 LPSCl 이 아니라 Li₃PS₄–0.5LiI (glassy thiophosphate)다.**  LPSCl 은 *separator* 로만 쓰임.
> 우리(LPSCl 복합) 와 SE 가 다르므로 **절대 σ·porosity 직접 동일시 금지** — *추세·구조→성능 사슬·방법론·CAM-ISE 계면면적·이용률* 이 전이 가능한 것.
> 단 같은 **황화물(thiophosphate) 계열 + 같은 Janek 그룹 + 같은 NCM 양극** → frame[4] 외부 앵커로서 가치 높음.  (CAM 은 NCM 으로 우리 NMC811 과 가까움; Ni0.83 = 우리 Ni0.8 근방.)

> ★ **저자 계보 (왜 ANCHOR):** 이 Philip Minnmann = 우리 **Minnmann 2021 JES 040537**(NCM622+LPSCl, σ_ion,eff 0.17 / τ_ion 2.07 / 복합 porosity 13–17 % @380 MPa) 의 같은 제1저자.
> 우리 DEM·MPM 의 pure-SE porosity 앵커("~10 %@300 MPa cold-press")는 Minnmann 2021 JES/Sakuda cold-press 거동 위에서 보정된 값.  이 2024 논문은 그 계보의 **토모-시각화 버전** — porosity 가 *어디에·왜* 병목인지 3D 로 보여준다.

## 3. 핵심 물성 (수치)
> ⚠ **표기:** *segmented* = FIB-SEM 분할(실측 구조), *geometric* = 투입질량·재료밀도로 계산한 기대값(Fig 4 검은 막대).  bar 값은 digitized(±, TREND); stated = 본문/표 명시.

| 물성 | 값 | 조건 (P, 조성) | stated/digitized | 비고 |
|---|---|---|---|---|
| **σ_ion (ISE bulk, 단상)** | **BM10 2.0 / BM03 1.7 / BM01 1.6 mS/cm** | ISE 단상, **380 MPa** 가압 측정 | **stated** (본문 + Fig 1a–c) | 작은 밀링미디어 → 입경↓ → σ_ion *약간↓*(BM01 1.6) — 소입자 입자간 접촉저항 기여 |
| **복합 porosity (segmented)** | **BM10 ≈10 % / BM03 ≈7.5 % / BM01 ≈6 %** | 복합 양극, **380 MPa cold-press** | digitized (Fig 4d) | ★ **작은 SE → porosity↓**; segmented ≪ geometric (나노공극 <50 nm 미검출 + 재퇴적) |
| **복합 porosity (geometric)** | **BM10 ≈20 % / BM03 ≈16 % / BM01 ≈11 %** | 동일 | digitized (Fig 4d 검은 막대) | 질량·밀도 기대값; segmented 보다 *높음*(분할이 나노공극·계면 놓침) |
| **φ_CAM (segmented)** | **BM10 55 / BM03 ≈51 / BM01 ≈45 vol%** | 공칭 50:50 vol | stated(BM10 55) + digitized (Fig 4b) | BM10 은 +5 vol% 편차(작은 ISE·공극이 CAM 으로 오분할) |
| **φ_ISE (segmented)** | **BM10 ≈34 / BM03 ≈41 / BM01 ≈45–46 vol%** | 동일 | digitized (Fig 4c) | geometric ~40; BM10 만 과소(소입자 ISE 분할난) |
| **복합 σ_el,eff (전자)** | **BM10 ≈15 / BM03 ≈10 / BM01 ≈10 mS/cm** | 70 wt% CAM 복합, ion-blocking cell, 380 MPa | digitized (Fig 2c) | ★ **작은 SE → σ_el↓**(CAM 클러스터 분산 → 전자 highway 끊김); 불확실성 ~20 % |
| **복합 σ_ion,eff (이온)** | **BM10 ≈0.05 / BM03 ≈0.11 / BM01 ≈0.11 mS/cm** | 70 wt% CAM 복합, full-blocking cell, 380 MPa | digitized (Fig 2d) | ★ **작은 SE → σ_ion↑ ~2×**(0.05→0.11); 더 많고 짧은 이온경로 = packing |
| **S_CAM-pore (계면면적)** | **0.34 → 0.16 m²/g** (BM10→BM01) | 복합, 380 MPa | stated | 작은 SE → CAM 표면이 공극 대신 ISE 와 접촉 → 감소 |
| **S_CAM-ISE (활성 계면)** ★ | **0.11 → 0.24 m²/g** (BM10→BM01) | 복합, 380 MPa | stated | ★ **작은 SE → 활성 CAM-ISE 계면 2.2×↑** = Li 전달면적↑ = 핵심 이득 |
| **S_ISE-pore** | **0.05 → 0.09 m²/g** (BM10→BM01) | 복합, 380 MPa | stated | 작은 ISE 입자간 점접촉↑ |
| **CAM coverage by ISE** | **BM10 ≈20 % → BM03/BM01 ≈50 %** | 복합, S_CAM=0.5 m²/g 가정 | stated | 나머지: 공극이 31 %, 다른 CAM 이 19 % 덮음(BM03/01) |
| **CAM utilization (1st)** ★ | **BM10 62 % / BM03·BM01 77 %** | full-cell, OCP-기반(Ruess 법) | stated (Fig 8) | ★ **작은 SE → 전기화학 활성 CAM 비율↑** → 용량↑ |
| **κ_ion (ionic tortuosity factor)** | **exp BM10 ≈15 → 작은 SE ≈6; sim 12→4; pore-less ~동일(porosity 가 주역)** | 복합, EIS(τ²) + flux/RW 시뮬 | stated/digitized (Fig 6b) | ★ exp ≫ sim(접촉저항·나노공극 미반영); porosity 채우면 κ_ion 급감 |
| **κ_el (electronic tortuosity factor)** | **exp BM10 ≈3 → sim ~2; ISE 입경 영향 작음** | 복합, EIS + 시뮬 | digitized (Fig 6b) | 전자는 porosity 영향 작음(이온이 porosity 에 민감) |
| **방전용량 @0.1C** | **BM10 92 / BM03 156 / BM01 152 mAh/g** | full-cell, 2.62–4.32 V | stated (Fig 7a) | ★ 큰 SE(BM10) = 율속 나쁨 |
| **율속 유지 @1C** | **BM10 25 % / BM03 32 / BM01 28 %** (vs 0.1C) | full-cell | stated | 큰 SE = tortuous 경로 → 과전압↑ |
| **1st-cycle Coulombic eff.** | **BM10 58 % / BM03 73 / BM01 68 %** | full-cell @0.1C | stated (Fig S8) | 계면열화·chemo-mech 손실(첫 사이클); BM10 최저 |
| **chord length (CL)** | 작은 SE → CL 짧음·균질; BM10 ISE CL **>10 µm**(클러스터), BM03/01 CAM CL 짧음 | 복합 | stated/digitized (Fig 5a) | CL = 상의 1방향 돌출 거리; 짧을수록 균질 |
| **d50 (ISE, 레이저 회절)** | **BM10 7.41 / BM03 4.93 / BM01 5.93 µm** | ISE 단상 | stated (Fig 1d) | BM01 재응집으로 d50 *반등*(5.93>4.93); 분포는 더 좁음 |
| **E_SE / σ_y / ν** | **n/a** (실험; 모듈러스 미측정) | — | n/a | 이 논문은 E 미보고; ISE 의 *malleability* 만 정성 언급(룸템프 가압 치밀화) |
| **Heckel P_y / knee** | **n/a** (단일 압력 380 MPa, 압력 sweep 없음) | — | n/a | porosity-vs-P 곡선 없음 → 우리 Heckel(P_y 138) 직접검증엔 부적합 |
| **fab/측정/작동압 3종** | **압밀 380 MPa(cold-press, 3 min) / σ 측정 380 MPa / 사이클 stack 30 MPa** | — | **stated** | ★ 우리 "제조≠작동압" 3종 구분과 정합(제조 380 ≈ 우리 300; 작동 30) |

## 4. 실험 + 시뮬 방법 ★
> 이 논문은 *실험* 이 주(主)이고 transport tortuosity 만 보조 시뮬.  순서: 합성 → 셀 제작·사이클 → 전도도(EIS-TLM) → PFIB-SEM 토모 → 분할·3D 재구성 → 미세구조 분석(계면면적·CL·τ) → 시뮬 τ 대조.

- **소재·합성**:
  - **ISE = "1.5Li₃PS₄·0.5LiI" (= Li₃PS₄–0.5LiI), glassy.**  기계화학 합성: P₂S₅ + LiI + Li₂S(총 2 g) 를 planetary mill(Pulverisette 7), 70 mL ZrO₂ jar, 20 × 10 mm ZrO₂ 미디어, 450 rpm, 12 h(밀링미디어:분말 = 30:1).
  - **3종 입경 = 밀링미디어 직경만 변경**: **BM10**(10 mm 미디어), **BM03**(추가 3 mm, 4 h, 450 rpm), **BM01**(추가 1 mm).  분말이 미디어에 붙는 것 방지로 anhydrous heptane 첨가.  *작은 미디어 → 충돌빈도↑ → 입경↓.*
  - **CAM = LiNi₀.₈₃Mn₀.₀₆Co₀.₁₁O₂ single-crystal (D50 3–5 µm, MSE Supplies).**  **separator = Li₆PS₅Cl (LPSCl, NEI Corp).**
- **셀 제작·테스트**:
  - in-house 하우징, **10 mm dia PEEK 실린더**.  먼저 LPSCl 60 mg 를 hand-press 로 separator 펠릿 압밀.
  - 복합 = CAM:ISE 를 agate mortar 로 15 min 혼합, **12 mg 복합(= CAM 로딩 10.7 mg/cm²)** 을 separator 위에 분산 → **최종 380 MPa, 3 min** uniaxial cold-press.
  - **음극 = In foil(9 mm) + Li foil(6 mm) → In/InLi (0.62 V vs Li⁺/Li).**
  - 사이클: **25 ℃, stack pressure 30 MPa, 2.62–4.32 V vs Li⁺/Li**(= 2 V–3.7 V vs In/InLi), C-rate 0.1/0.2/0.5/1/2C(3사이클마다 증가).  1C = 200 mA/g.
- **전도도 측정(EIS-TLM)** ★:
  - **σ_ion (ISE 단상)**: ion-blocking 대칭셀(양쪽 steel piston), 100 mg ISE, **380 MPa** 가압.  σ_LPSCl separator 는 25 mg/50 mg 복합으로 **두께 ~400 µm** 형성.
  - **복합 부분전도도** = 두 셀 설정 + 두 TLM:
    - **σ_el (전자)**: ion-blocking cell(steel‖cathode‖steel) → **T-type TLM**(병렬 수송, 한 캐리어 미차단, current collector 횡단 가능).
    - **σ_ion (이온)**: **full-blocking cell**(steel‖cathode‖**ISE layer**‖cathode‖steel) → **Z-type TLM**(계면 용량성, fully-lithiated NCM 이라 Li 전달 불가 → 매우 높은 R_ct).
    - σ_cc,eff = l/(R_cc·A) (eq 2).  VMP-300, OCV, 3 MHz–10 mHz, 10 mV, **stack pressure 100 MPa** 유지하며 측정.  데이터 불확실성 ~20 %.
- **PFIB-SEM 토모그래피** ★ (핵심 시각화):
  - **Xe-plasma FIB-SEM (XEIA3, Tescan)** — 3개 복합 펠릿(ISE 입경 다름, **무탄소**) 의 3D 토모.
  - 펠릿을 sputter Pt 박막 → ROI 에 gas injection 으로 **10–15 µm Pt 코팅**, U-trench 밀링, polishing(curtaining 저감).
  - 자동 슬라이싱: **36 nA, 슬라이스 두께 100 nm**.  **SE(이차전자) + BSE(후방산란) 둘 다 100 nm 해상도** 기록 → **cubic voxel 100 nm**.
  - **상보적 분할(complementary segmentation)**: BSE = CAM 구분(원자번호 대비) 잘하나 공극·하부물질 혼동; SE = 표면지형 민감 → 공극 검출 우수.  **둘을 결합** → CAM(파랑)/ISE(노랑)/pore(검정) 3상 할당.
  - **ML 분할**: VGG16 CNN 첫 2 conv 층 feature 추출 + **random forest** pixelwise 분류(Keras/Scikit-learn).  BM01 의 mortar 불순물은 수동 분할.
- **미세구조 분석(3D)**:
  - **상분율**: voxel 카운트로 CAM/ISE/pore 부피분율.
  - **계면면적 S_a**: marching-cubes(Scikit-learn) 로 각 상 표면적 → **S_{a-b} = ½(S_a + S_b − S_c)** (eq 1, Janek/Bielefeld 관례).
  - **chord length (CLD)**: PoreSpy(Python) — 상 경계 사이 선분 길이 분포(2 voxel 이내 교차 chord 는 제외).
  - **tortuosity τ** = **flux-based(GeoDict ConductoDict)** + **random-walk(Pytrax, 2000 walkers, MSD vs timestep 의 역기울기)** 둘 다.  flux 가 dead-end 도 반영해 더 적합.  **κ_a = σ_a,bulk/σ_a,eff · φ_a** (eq 3) 으로 EIS τ 와 대조.
- **입자/구조 처리** ★ (이 논문은 *실측 재구성* — "무질서 처리"가 아예 *실제 미세구조*):
  - ★ **digital twin / 통계 배치 *아님*** — 본문 명시: "we use geometric reconstructions of *actual* cathodes and do not generate digital twins by any statistical or stochastic methods."  → **우리(압축해 예측) 와도, Bielefeld GeoDict stochastic placement 와도 다른 *ground-truth 실측 구조*.**
  - SE = glassy(비정질, LiI 불순물), CAM = single-crystal NCM.  *모델 입자형상 가정 없음* — voxel 화한 실제 입자.
  - **나노공극(<50 nm) 미해상**: 100 nm voxel 한계 → segmented porosity 가 geometric 보다 *낮게* 나오는 주원인(나노공극·입자간 접촉이 CAM 으로 오분할).
- **압력·통계**: 제조 380 MPa(단일), σ 측정 100 MPa stack, 사이클 30 MPa.  **porosity-vs-P sweep 없음**(단일 제조압).  토모는 3 펠릿(입경 3종) 각 1개.

## 5. Figure set ★
| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| 1 | (a–c) BM10/03/01 ISE SEM + **σ_ion 라벨(2.0/1.7/1.6)**, (d) **레이저회절 누적 PSD**(d50 7.41/4.93/5.93), (e) XRD(glassy + LiI 불순물) | 입경 sweep 의 기준; **σ_ion 단상 앵커**; BM01 재응집으로 d50 반등 = 우리 "응집 SE" 논의(So 2021 φc=0.13)와 연결 |
| 2 | **(a) 전자 ion-blocking EIS(T-TLM), (b) 이온 full-blocking EIS(Z-TLM), (c) σ_el vs 샘플(15/10/10), (d) σ_ion vs 샘플(0.05/0.11/0.11)** | ★ **복합 σ_ion·σ_el 절대 앵커 + 측정법(두 셀·두 TLM)**; 작은 SE → σ_ion↑·σ_el↓ trade-off = 우리 dead-AM/dead-SE 양끝 |
| 3 | **PFIB-SEM 토모 워크플로 모식**: FIB 밀링 → BSE+SE 상보분할 → 3D 재구성 → 미세구조 분석(계면면적·CL·τ) | 우리 *구조→성능* 파이프라인의 실험 카운터파트; 상보분할(BSE+SE) = 공극 검출법 |
| 4 | **(a) BM10/03/01 3D 재구성 큐브(파랑 CAM/노랑 ISE/검정 pore), (b) φ_CAM(55/51/45), (c) φ_ISE(34/41/46), (d) φ_pore(seg ~10/7.5/6 vs geo ~20/16/11)** | ★ **핵심 porosity 그림** — 작은 SE → porosity↓; segmented vs geometric 차이 = 나노공극 한계 |
| 5 | **(a) CAM·ISE chord length 분포, (b) CL 모식, (c) 비계면면적 S_spec(ISE-pore/CAM-pore/CAM-ISE) bar** | ★ **S_CAM-ISE 0.11→0.24(활성계면 2.2×↑)·S_CAM-pore 0.34→0.16**; 작은 SE → 짧은 CL = 균질 |
| 6 | **(a) ionic-flux 국소전류밀도 3D 맵(0–4.5 mA/cm², BM10 hotspot↑), (b) τ factor κ_el·κ_ion(exp/RW/flux/RW-no-porosity)** | ★ **τ_ion exp 15→6·sim 12→4; "pore-less" τ 가 실측과 큰 차 = porosity 가 이온의 주병목** = 우리 √φ_eff·porosity-중심 모델 정당화 |
| 7 | **(a) 방전 C-rate 용량(0.1–2C, BM10 92 vs 156/152), (b) dQ/dV(H1/M·H2/H3 전이), (c) 0.1C·(d) 1C 방전곡선** | ★ **율속 성능 = 미세구조의 함수**; 큰 SE → 과전압↑·용량↓; 우리 fracture/τ→성능 사슬의 실험 끝점 |
| 8 | **CAM 이용률 vs 사이클수(BM10 62 % → 작은 SE 77 %, 15 사이클 감소)** | ★ **CAM 이용률 = S_CAM-ISE 의 직접 결과**; 큰 SE 클러스터 → 이온망서 단절 → 활성질량↓ = 우리 dead-AM/f_AM^cc |

## 6. Post-processing ★
- **무엇**:
  - ① **porosity (segmented vs geometric)** — voxel 카운트 분할 vs 질량·밀도 기대값.  ★ **두 convention 차이 자체가 결과**(나노공극·계면이 분할에서 누락 → segmented < geometric).
  - ② **상분율 φ_CAM/φ_ISE/φ_pore** (3D voxel).
  - ③ **계면면적 S_{a-b}** marching-cubes + eq 1 — 특히 **활성 S_CAM-ISE** (Li 전달 면적).
  - ④ **chord length 분포(CLD)** PoreSpy — 상 균질성·클러스터링 지표.
  - ⑤ **tortuosity κ** = flux(GeoDict ConductoDict) + random-walk(Pytrax), EIS τ²(=κ_a, eq 3)와 대조.  **"pore-less" κ**(공극 채운 가상구조) 도 계산 → porosity 기여 분리.
  - ⑥ **국소전류밀도 맵**(ionic-flux 시뮬, Fig 6a) — bottleneck 시각화(hotspot).
  - ⑦ **CAM 이용률**(electrochemically active mass) — Ruess 법, OCP-vs-Li 평형(전기화학 비활성 입자는 OCP 기여 없음).
- **도구**: **Fiji ImageJ**(MultiStackReg drift 보정, Stripes Filter curtaining 제거) + **Python**(Keras VGG16 + Scikit-learn random forest 분할; marching cubes; PoreSpy CLD) + **GeoDict ConductoDict**(flux τ) + **Pytrax**(random-walk τ) + EIS-TLM 피팅(T-type/Z-type).
- **수치화·플롯·기록**: porosity·상분율·계면면적·κ 를 BM10/BM03/BM01(= ISE 입경 sweep)로 bar/곡선.  σ(EIS)·용량(사이클)을 같은 3샘플로 상관.  **raw 토모 데이터를 supplementary datafiles 로 공개**(http://dx.doi.org/10.22029/jlupub-18458).  segmented vs geometric 막대 병기로 분할 한계 명시.

## 7. 우리 DEM+MPM 대비  →  `our_dem_baseline.md`
> 이 논문은 *실험*(경쟁 시뮬 아님) → "차이"는 *우리 시뮬이 무엇을 모델링/예측하는가 vs 그들이 무엇을 실측하는가* 의 분업.

| 항목 | 이 논문 (Minnmann 2024, 실험) | 우리 (DEM+MPM) | 관계 / 분업 |
|---|---|---|---|
| **구조 획득** | **FIB-SEM 실측 재구성**(digital twin/통계 배치 *아님*, 명시) | **공정-물리로 압축해 *예측***(DEM cold-press) | **상보**: 그들 = ground-truth 측정; 우리 = 예측(측정 불요).  우리 예측을 그들 실측에 검증 가능(frame[4]) |
| **porosity** | 복합 segmented **~6–10 %**(geo ~11–20 %), Li₃PS₄–LiI SE, 380 MPa | DEM real_14 **15.6 %**, MPM scaffold **16.7 %**, LPSCl, 300 MPa | ★ **둘 다 ~10 % 권 황화물 복합** — 추세·order 정합.  ⚠ SE 다름(Li₃PS₄LiI≠LPSCl)·압력 다름(380≠300) → 절대 동일시 금지.  그들 *segmented<geometric* 교훈 = 우리 ε_sphere vs ε_union 차이와 같은 종류 |
| **porosity → σ_ion 인과** | ★ **"pore-less" τ ≈ 실측 차 → porosity 가 이온 주병목** 실증(Fig 6) | √φ_eff·porosity-중심 σ_ionic 폼 (LOOCV 0.975) | ★ **그들 실험이 우리 porosity-중심 모델링을 정당화** — 이온은 porosity 에 민감, 전자는 둔감(우리도 σ_e 는 φ_AM⁴·전자망) |
| **σ_ion (복합)** | exp **0.05→0.11 mS/cm**(작은 SE↑) | DEM σ_ionic 0.04–0.18 | ★ **그들 0.05–0.11 ⊂ 우리 범위** — frame[4] 외부 앵커(⚠ SE 다름 → 추세 검증, 절대는 LPSCl Minnmann2021/Bazzoun 소유) |
| **σ_el (복합)** | exp **15→10 mS/cm**(작은 SE↓) | σ_e 삼중항(LOOCV 0.953) | ★ **작은 SE→σ_el↓**(CAM 클러스터 분산) = 우리 σ_e 의 φ_AM⁴·f_p(percolation) 방향; 그들 실측이 외부 검증 |
| **σ_thermal** | **없음** | σ_thermal 삼중항(LOOCV 0.90) | **우리 고유** (그들 미측정) |
| **계면면적/coverage** | **S_CAM-ISE 0.11→0.24 m²/g·coverage 20→50 %**(실측 기하) | Stage-E coverage(Tabor+B3, real_14 AM_P/S 48–52 %) | ★ **둘 다 "작은 SE → CAM-ISE 계면↑"** + coverage 절대값 같은 권(~50 %).  ⚠ 그들 = *기하 계면면적/coverage*, 우리 Stage-E = *전도-가중 접촉면적*(Tabor 소성) → 종류 다름, 추세 정합 |
| **tortuosity τ** | **exp κ_ion 15→6 / flux sim 12→4** | τ_Laplace / τ_Dijkstra / R_brug | ★ **그들 flux τ = 우리 τ_Laplace 와 같은 종류**(연속체 확산); exp≫sim(접촉저항·나노공극) = 우리 Stage-E constriction 이 메우는 간극 |
| **CAM 이용률(dead-AM)** | **62→77 %**(작은 SE↑, 사이클 감소) | f_AM^cc / dead-AM 경고(<80 %) | ★ **그들 이용률 = 우리 dead-AM 의 *실험 측정*** — 큰 SE 클러스터 → CAM 이온망서 단절 = 우리 f_AM^cc<80 % 와 같은 물리 |
| **소성 morphology** | **없음**(실측 구조 정적) | **MPM J2 소성 SHAPE·void-fill** | **우리 고유** — 단 그들이 ISE *malleability*(룸템프 가압 치밀화)를 정성 언급 = 우리 MPM 소성의 *현상* 근거 |
| **fracture/degradation** | **사이클 CAM 이용률 감소·1st CE 58–73 %**(contact loss 정성) | Auerbach/fracture-Holm/f_intact | 그들 = *사이클 후* contact-loss 정성; 우리 = *압밀-시점* 균열.  시간축 분업(frame[5]) |
| **전달 솔버** | **EIS-TLM 실측 + flux/RW τ 시뮬**(GeoDict/Pytrax) | **Kirchhoff + Holm 명시 저항망** | 그들 τ→σ(연속체, constriction 없음) = 상한; 우리 Holm constriction 이 *되돌려 넣음*(Bielefeld2020→Bazzoun→우리 궤적) |
| **압력 sweep** | **단일 380 MPa**(porosity-vs-P 없음) | DEM Heckel 4압력(P_y 138) | 그들은 다중압력 없음 → 우리 Heckel 직접검증엔 부적합(σ·porosity 절대점만) |

## 8. 적용 인사이트 (내 연구에 어떻게)
- ① **porosity 가 이온 주병목 — 우리 porosity-중심 σ_ionic 모델의 *실험적 정당화*.**  Fig 6 의 **"pore-less" tortuosity 가 실측 τ 보다 훨씬 낮다**(공극 채우면 LIB 수준 τ 도달) = porosity 가 이온수송의 *지배* 저해요인이고 전자는 둔감하다는 직접 증거.  우리 σ_ionic = √φ_eff·...·porosity-중심(LOOCV 0.975), σ_e = φ_AM⁴·전자망(porosity 둔감) — **정확히 같은 비대칭**.  ⇒ 우리 모델 구조가 옳은 방향임을 *같은 그룹의 실험* 이 보증.  ★ deck 강점.
- ② **S_CAM-ISE(활성 계면면적) = 우리 Stage-E coverage 의 실험 카운터파트 + 외부 검증.**  그들 **0.11→0.24 m²/g(작은 SE → 2.2×↑) · coverage 20→50 %** = 우리 "작은 SE → CAM-SE 접촉↑" + real_14 Stage-E coverage 48–52 % 와 **같은 권·같은 추세**.  ⚠ 그들 = *기하* 계면면적, 우리 Stage-E = *Tabor 소성 전도면적* → 종류 다름.  ⇒ 우리 coverage 추세를 그들 실측 계면면적에 *cross-check*(절대 동일시 말고 추세).  **backlog B (coverage/RNM-vs-StageE 검증)** 보강.
- ③ **CAM 이용률 62→77 % = 우리 dead-AM/f_AM^cc 경고의 실험 측정값.**  큰 SE 클러스터가 CAM 을 이온 percolating 망에서 *단절* → 전기화학 비활성 → 용량↓.  우리 f_AM^cc<80 % dead-AM 경고와 **물리 동일**.  ⇒ 우리 dead-AM 메트릭을 그들 이용률에 매핑(작은 SE = 높은 이용률 = 낮은 dead-AM).  **scaling-law predictor 의 이용률/CAM-활성 타깃**(Phase 3) 외부 앵커.
- ④ **frame[4] 외부 앵커 (단 *추세*):** σ_ion 0.05→0.11 / σ_el 15→10 / τ_ion 15→6 / coverage 20→50 / 이용률 62→77 — 모두 *작은 SE → 균질 → 성능↑* 의 일관 추세.  우리 DEM·MPM 의 "작은 SE = packing 이득"(size=packing, Furnas)·"균질→σ↑"·"이용률↑" 예측을 *같은 방향* 으로 검증.  ⚠ **절대 σ·porosity 는 SE 가 Li₃PS₄–0.5LiI(≠LPSCl) 라 전이 금지** — LPSCl 절대 앵커는 Minnmann2021(0.17)·Bazzoun(0.137)·우리 DEM 소유.

## A. 우리 DEM+MPM 대비 (comparison vs ours) — 미세구조→성능 매핑
> 이 논문이 *시각화* 한 구조→성능 사슬을, 우리 DEM(porosity·접촉망 σ-삼중항)·MPM(소성 morphology·void-fill)이 *어떻게 계산하는가*.

- **(A1) porosity → 우리 DEM porosity·MPM scaffold:**  그들 복합 segmented **~6–10 %**(Li₃PS₄LiI, 380 MPa) vs 우리 DEM real_14 **15.6 %**·MPM scaffold **16.7 %**·pure-SE 앵커 **~10 %**(LPSCl, 300 MPa).
  - ★ **같은 *order*(~10 % 권 황화물 복합)** → 우리 scaffold porosity(15.6 %) 가 *실험적으로 그럴듯한 권* 임을 보강.  ⚠ 단 **SE 다름(Li₃PS₄–0.5LiI ≠ LPSCl)·압력 다름(380≠300)·CAM 다름(NCM single-crystal vs 우리 PSD)** → 절대 동일시 금지.  그들 segmented(~6–10) < geometric(~11–20) 의 ~5–10 %p 차 = 나노공극·계면 분할 누락 = 우리 **ε_sphere vs ε_union**(real_14 13.47 vs 14.98) 차이와 *같은 종류의 convention 격차*.  ⇒ "어느 porosity 가 진짜냐"는 양쪽 다 *측정/계산 방식 의존* 이라는 공통 교훈.
  - ★ **우리 scaffold 검증과의 연결:** 우리 real_14 DEM 15.6 % ↔ MPM scaffold 16.7 %(|gap| ~1.2 %p, frame[4] 교차검증).  Minnmann 토모는 *제3의 실험 점*(같은 황화물-NCM 계, ~6–10 %) → 우리 DEM↔MPM 일치가 *실험 권* 안에 있음을 보강(절대 일치 주장 아님, 추세·order).
- **(A2) 접촉망 σ-삼중항 → 그들 EIS:**  그들 복합 σ_ion 0.05→0.11·σ_el 15→10 mS/cm.  우리 DEM Kirchhoff/Holm σ_ionic(0.04–0.18)·σ_e·σ_thermal 삼중항.
  - σ_ion: 그들 0.05–0.11 ⊂ 우리 0.04–0.18 → **추세·권 정합**(frame[4]).  σ_el: 작은 SE→σ_el↓ = 우리 σ_e 의 percolation(f_p)·φ_AM⁴ 방향.  ⇒ 우리 *삼중항* 이 그들 *2채널 실측*(σ_ion+σ_el) 을 포괄·확장(σ_thermal 은 우리만).
- **(A3) 소성 morphology·void-fill → MPM:**  그들은 ISE *malleability* 로 룸템프 가압 치밀화·공극충전을 정성 언급("malleable ISE allows removal of pores between ISE particles", Fig 5 논의).  ★ **이것이 바로 우리 MPM 이 *정량* 모사하는 소성 void-fill** — 그들이 *현상* 으로 관찰한 것을 우리 MPM 이 변형장 Σdg·porosity 감소(−8.5 %p)·SEM-일치 morphology 로 *계산*.  ⇒ 그들 토모는 MPM void-fill 의 *실험 동기*; 우리 MPM 은 그 메커니즘을 예측.
- **(A4) coverage 가시화 corroboration:**  그들 **CAM-ISE coverage 20→50 %**(작은 SE) + S_CAM-ISE 0.11→0.24 m²/g 실측 ↔ 우리 Stage-E coverage real_14 AM_P/S **48–52 %**(Tabor).  ★ **그들 시각화한 pore/contact 구조가 우리 Stage-E coverage(~50 %)·scaffold porosity(15.6 %) 를 *추세·권* 으로 corroborate.**  ⚠ 종류 다름: 그들 = 기하 계면(BSE+SE 분할), 우리 = 전도-가중 소성 접촉(Tabor+B3) → "둘 다 ~50 % 권, 작은 SE↑" 까지만 일치, byte 동일 아님.

## B. 적용가능성 (applicability — *실험 앵커*: 어떤 수치를 절대 검증점으로) ★
> frame[4] = 우리 모델은 EXPERIMENT 에 calibrate, 모델끼리 cross-fit 금지.  이 논문은 *실험* → 외부 앵커 후보.
> ⚠ **SE 가 Li₃PS₄–0.5LiI(≠LPSCl)** 이므로 **절대 σ·porosity 는 "추세/order 검증" 으로만**; LPSCl 절대 앵커는 Minnmann2021·Bazzoun·우리 DEM 소유.

| 그들 수치 (조건) | 우리 어느 메트릭에 | 앵커 등급 | 매핑 주의 |
|---|---|---|---|
| **복합 porosity seg 6–10 % / geo 11–20 %** (Li₃PS₄LiI, 380 MPa, CAM:ISE 50:50 vol) | DEM/MPM scaffold porosity(15.6/16.7 %) | **추세/order 앵커**(절대 ✗) | SE·압력·CAM 다름; *segmented vs geometric* convention 교훈은 직접 적용 |
| **σ_ion,eff 0.05→0.11 mS/cm** (70 wt% CAM, 380 MPa) | σ_ionic(0.04–0.18) | **추세 앵커**(작은 SE→σ↑) | SE 다름 → 절대 ✗; 추세·권 ✓.  vol% CAM:ISE 50:50 → φ_SE 매핑 후 |
| **σ_el,eff 15→10 mS/cm** | σ_e(percolation·φ_AM⁴) | **추세 앵커**(작은 SE→σ_el↓) | CAM=NCM(우리 가까움) but σ_AM 절대 다름; 추세 ✓ |
| **S_CAM-ISE 0.11→0.24 m²/g · coverage 20→50 %** | Stage-E coverage(48–52 %) | **추세 + 권 앵커** | 기하 vs Tabor-소성 → 종류 다름; "작은 SE→계면↑·~50 % 권" ✓.  **backlog B coverage 검증 보강** |
| **κ_ion exp 15→6 / flux 12→4** | τ_Laplace / R_brug | **추세 + 방법 앵커** | flux τ = 우리 τ_Laplace 종류; exp≫sim 격차 = Stage-E constriction 대상 |
| **CAM utilization 62→77 %** | dead-AM / f_AM^cc(<80 %) | **개념 + 추세 앵커** | 큰 SE→이용률↓ = 우리 dead-AM; **Phase 3 predictor 이용률 타깃** 외부점 |
| **fab 380 / σ측정 100 / 사이클 30 MPa** | 압력 3종 구분 | **개념 앵커** | 제조 380 ≈ 우리 300; 작동 30 ≈ 우리 "수십 MPa" → Doux/Lee2025 "제조≠작동" 합류 |

- ★ **backlog B1(σ_ionic 절대 검증점) 보강:**  이 논문은 σ_ion 절대값(0.05–0.11)·복합 porosity·계면면적·이용률·τ 를 *한 논문에서 동시* 제공 → Minnmann2021(0.17/13–17 %/τ 2.07)·Bazzoun(0.137)·Lee2025(0.076)·Kim2025(R_ion) 의 LPSCl 앵커 군에 **Li₃PS₄LiI *추세* 앵커**를 추가(절대는 LPSCl 군 소유, 이건 *구조→성능 사슬 + 추세 + 방법* 앵커).  ⇒ **"우리 porosity·σ·coverage·이용률·τ 가 같은 그룹 토모 실험과 같은 방향"** 이라는 frame[4] 강점 5종 동시 확보.
- ★ **Minnmann porosity 앵커 강화:**  우리 "Minnmann ~10 % @300 MPa"(pure-SE, 2021 JES/Sakuda 보정) 의 *출처 계보* 가 2024 토모로 확장 — 같은 저자가 *복합* porosity 를 ~6–10 %(seg) 로 토모-실측 → 우리 pure-SE 10 % / 복합 15.6 % 가 *같은 그룹의 실측 권* 안.  ⚠ 단 이 2024 의 6–10 % 는 *복합·Li₃PS₄LiI·380 MPa* 이지 *pure-SE·LPSCl·300* 이 아님 → 앵커 *계보 보강* 이지 *수치 교체* 아님.

## C. frame[5] 위치 + 우리 novelty (our contribution vs this experimental study)
> 이 논문은 *실험*(DEM-SOTA 경쟁 논문 아님) → "novelty"는 *우리 시뮬이 그들 시각화 위에 무엇을 더하는가*.

- **그들 위치 = 실험 *측정/시각화*(MEASURE).**  FIB-SEM 으로 *실제* 미세구조→성능 사슬을 ground-truth 로 보여줌(porosity·계면·τ·이용률·용량).  *digital twin 도, 통계 배치도 아닌* 실측 재구성.  → frame[4] 의 **외부 EXPERIMENT 앵커** 자리(우리가 calibrate-to).
- **우리 시뮬이 *그 위에* 더하는 것 (MODEL the link they VISUALIZE):**
  - ★ **예측 transport 삼중항 σ_ionic+σ_e+σ_thermal** (Kirchhoff/Holm 접촉망) — 그들은 σ_ion+σ_el 2채널 *실측*, σ_thermal 무.  우리는 *구조에서 계산*(측정 불요) + σ_thermal 추가.  그들 토모는 *한 번 측정*; 우리 솔버는 *설계공간 전체 예측*.
  - ★ **MPM 소성 void-fill 메커니즘** — 그들이 ISE *malleability* 로 *정성* 관찰한 공극충전을, 우리 MPM 이 *정량*(변형장 Σdg·porosity −8.5 %p·SEM-일치 morphology) 으로 계산.  그들 = 결과(공극 적음); 우리 = *메커니즘*(어떻게 채워지나).
  - ★ **fracture-aware degradation** — 그들 사이클 CAM 이용률 감소·1st CE 58–73 % 는 *contact-loss 정성*; 우리 Auerbach/fracture-Holm/f_intact 는 *압밀-시점 균열 정량*(시간축은 frame[5] 분업: 사이클은 Kang FEM).
  - ★ **scaling-law 설계 predictor** — 그들 3샘플(BM10/03/01) 이산점 vs 우리 design-knob→전 메트릭 예측(σ_ionic LOOCV 0.975, σ_e 0.953, σ_thermal 0.90).  우리는 그들이 *측정한 추세* 를 *연속 설계함수* 로 일반화 + 그들 실측을 그 위에 검증.
- **요약:**  **그들 = 미세구조→성능 링크를 *시각화*(실측); 우리 = 그 링크를 *모델링/예측*(σ-삼중항+MPM-소성+fracture+predictor) 하고 *그들 실험에 calibrate*.**  frame[5] 분업 = DEM(transport 망 σ)·MPM(소성 morphology)·predictor(설계) 가 그들 토모-실측 *위에* 예측층을 얹음.  ⚠ 그들은 *실험* 이라 "우리가 능가" 가 아니라 "우리가 *모델링·예측·일반화* 로 보완 + calibrate-to" 가 정직한 framing.

## 9. 인용 가능 문장 (deck/paper용)
- "Minnmann et al. (2024, *Editors' Choice*) used Xe-plasma FIB-SEM tomography to **visualize**, in actual NCM/Li₃PS₄–LiI composite cathodes, that **residual porosity is the dominant inhibitor of *ionic* (not electronic) charge transport** — a 'pore-less' tortuosity factor reaching LIB-like values confirms that filling porosity, not changing ISE particle size per se, governs ionic transport; this directly justifies our porosity-centred σ_ionic form (√φ_eff·…) and porosity-insensitive σ_e form (φ_AM⁴·percolation)."
- "Smaller solid-electrolyte particles produced a more homogeneous microstructure with **lower segmented porosity (≈10→6 %), 2.2× higher active CAM–ISE interface area (0.11→0.24 m² g⁻¹), lower ionic tortuosity (κ_ion 15→6), and higher CAM utilization (62→77 %)** — the same 'small-SE packing benefit → higher σ_ion and utilization' trend our DEM (size = packing) and MPM predict, here measured by tomography on the same Janek-group sulfide/NCM system that anchors our porosity calibration."
- "Because our DEM compaction (porosity, contact-network σ-triad) and MPM (plastic void-fill morphology) **model** exactly the microstructure→performance chain Minnmann et al. **visualize**, their tomography-derived numbers (composite porosity ~6–10 %, σ_ion 0.05–0.11 mS cm⁻¹, CAM–ISE 0.11–0.24 m² g⁻¹, CAM utilization 62–77 %) serve as external frame[4] anchors — calibrated to, never cross-fit against, the simulation."

## 10. 주의/한계 (over-claim 방지)
- ★ **복합 양극 SE = Li₃PS₄–0.5LiI (glassy thiophosphate), *LPSCl 아님*.**  LPSCl 은 *separator* 로만.  **절대 σ·porosity·계면면적 직접 전이 금지** — *추세·order·구조→성능 사슬·방법론·CAM-ISE 계면·이용률·τ* 만.  LPSCl 절대 앵커는 Minnmann2021(0.17)·Bazzoun(0.137)·Lee2025(0.076)·우리 DEM 소유.
- **단일 제조압(380 MPa) — porosity-vs-P sweep 없음.**  우리 Heckel(P_y 138)·다중압력 압밀 직접검증엔 부적합(σ·porosity 절대점·구조만).  다중압력은 So2021·Varkey·Bazzoun(σ-vs-P)·Doux(접촉-vs-P) 소유.
- **segmented vs geometric porosity 차(~5–10 %p)** = **나노공극(<50 nm) 미해상 + 재퇴적** 한계(100 nm voxel).  본문도 명시: "segmented porosity much lower than geometric … pores falsely segmented as CAM + nanosized pores not detected."  → 그들 segmented 절대값을 *진짜 porosity* 로 과신 금지(geometric 도 같이 봐야); 우리 ε_sphere/ε_union 양면 보고와 같은 교훈.
- **tortuosity exp ≫ sim**(κ_ion exp 15 vs sim 12; 작은 SE exp 6 vs sim 4) — 본문이 3원인 명시: (I) current collector·GB 접촉저항 미반영, (II) 나노공극 미해상, (III) constriction(field 왜곡) 미반영.  ★ **바로 (III) = 우리 Stage-E/Holm constriction 이 메우는 칸** → 그들 sim(연속체 flux/RW)은 σ 상한, 우리 접촉저항이 아래로 좁힘(Bielefeld2020→Bazzoun→우리 궤적과 동일).  → 그들 sim τ 를 우리 절대 τ 와 직접 동일시 금지.
- **그림 읽은 값(digitized)은 추세만(±):** Fig 2c/d(σ), Fig 4b–d(porosity·상분율), Fig 6b(κ), Fig 7a(용량) 의 bar/곡선 수치는 근삿값.  stated(σ_ion 단상 2.0/1.7/1.6, S_CAM-ISE 0.11/0.24, 이용률 62/77, 용량 92/156/152, 1st CE 58/73/68, d50 7.41/4.93/5.93, 압력 380/100/30) 와 구분.
- **CAM = single-crystal NCM(Ni0.83)**, *우리 production NMC811 PSD 와 다름*(그들 D50 3–5 µm single-crystal; 우리 bimodal AM_P/AM_S).  Ni0.83 ≈ 우리 Ni0.8 근방이라 CAM 은 *비교적 가까움*(SE 보다)이나 단결정 vs 다결정·PSD 차 → 절대 매칭 주의.
- **사이클 1st CE·CAM 이용률 감소 = *사이클 후* contact-loss/chemo-mech 정성** — 우리 *압밀-시점* fracture(Auerbach) 와 시간축 다름(frame[5]: 사이클 chemo-mech 은 Kang FEM 영역).  "큰 입자 깨짐/단절" 계보는 공통(Lee2025 PC-NCM·Kang 큰입자 균열·우리 AM_P 파괴) 이나 *원인·시점* 구분.
- **무탄소(carbon-free) 복합** — 도전제 없는 셀(분해반응 회피 목적).  우리 production(VGCF/SuperP+PTFE) 과 다름 → CBD·바인더 효과(Lee2025/Bielefeld2020/Hong)는 이 논문에 없음.
- **시뮬은 보조(τ 만)** — 이 논문의 flux/RW τ(GeoDict/Pytrax)는 *실측 재구성 위* 의 후처리지 *예측 압밀 모델* 아님.  우리 DEM(공정-예측)·MPM(소성)과 *방법 범주가 다름*(그들 = 측정구조의 τ; 우리 = 구조 자체를 예측).

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
