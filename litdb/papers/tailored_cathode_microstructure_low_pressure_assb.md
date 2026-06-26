<!-- COMPREHENSIVE / paper-level STANDALONE digest. 읽으면 논문 읽은 것과 등가가 목표. 길이 제한 없음. -->
# Tailored Cathode Composite Microstructure Enables Long Cycle Life at Low Pressure for ASSBs — Zhou et al. (ACS Energy Lett. 2025)

> slug `tailored_cathode_microstructure_low_pressure_assb` · DOI `10.1021/acsenergylett.4c03256` · type **mixed (exp + LAMMPS granular DEM + FIB-SEM tortuosity)** · PDF `TailoredCathodeMicrostructure_LowPressure_LongCycleLife_ASSB.pdf` · digested `2026-06-26` · status ✅
> ACS Energy Lett. **2025**, *10*, 966–974. Received 2024-11-24 / Accepted 2025-01-22 / Published 2025-01-25.

---

## 1. 한 줄 요약 (One-line summary)

**우리와 정확히 같은 소재계(Li₆PS₅Cl LPSCl SE + NCM811 CAM)에서, "SE 입자를 잘게(fine-LPSC, ~1 µm) 만들면 CAM 표면을 더 균일·치밀하게 덮어(=coverage↑) 이온 percolation·tortuosity가 개선되고, 그 결과 *낮은 stack pressure(2 MPa)*에서도 장수명(85.6 % retention @100 cyc)을 얻는다"**를 **실험 + LAMMPS granular DEM(CAM utilization vs 입자 overlap) + FIB-SEM tortuosity**로 보인 논문.
EN: Engineering the SE particle size (coarse ~20 µm → fine ~1 µm LPSC by wet roll-mixing) yields a **denser, more uniform SE-on-CAM distribution** → higher CAM utilization, lower tortuosity (1.84 → 1.21), lower charge-transfer resistance (R_ct 17.3 → 9.9 Ω) → **stable cycling even at 2 MPa** (vs coarse 63.3 %), whereas at high pressure (30 MPa) the microstructure advantage nearly vanishes (90.3 vs 84.0 %).
★ **우리에게 frame[4] 외부 앵커가 3중으로 겹친다:** (a) **DEM(LAMMPS granular) "CAM utilization vs minimum overlap" = 우리 coverage/contact-network의 직접 대응**(같은 코드계열·같은 소재), (b) **FIB-SEM porosity(coarse 11.3 % / fine 4.4 %)·tortuosity(1.84/1.21)·BET = 우리 압밀/τ의 실측**, (c) **fab(제조)압 vs operating(작동 2/10/30 MPa) 분리 + "microstructure가 저압에서만 차이를 만든다"**는 backlog **B6(operating-pressure 축)**의 핵심 메커니즘. — Bazzoun/Lee처럼 *경쟁 모델이 아니라 실험+같은-DEM 측 검증*.

---

## 2. 메타 (Metadata)

| 저자 | 저널/년 | DOI | 소재 (SE/CAM/도전제) | 연구유형 |
|---|---|---|---|---|
| **Ke Zhou, Sijian Lu, Charles Mish, Yu-Ting Chen, Shijie Feng, Jiyoung Kim, Min-Sang Song, Hyunsun Alicia Kim\*, Ping Liu\*** (UC San Diego, Aiiso Yufeng Li Family Dept. of Chemical & Nano Eng. + **LG Energy Solution**, Seoul) | ACS Energy Lett. **2025**, *10*, 966–974 | 10.1021/acsenergylett.4c03256 | **Li₆PS₅Cl (LPSC/LPSCl)** SE (coarse ~20 µm vs **fine ~1 µm**) + **NCM811 (LiNi₀.₈Co₀.₁Mn₀.₁O₂, ~1–5 µm)** CAM + (도전제 명시 안 됨 — Methods/SI) + **Li-metal 음극** | **mixed**: 실험(합성·EIS·GITT·cycling·FIB-SEM·XRD·XPS) + **LAMMPS granular DEM**(CAM utilization·calendaring) + **FIB-SEM 3D tortuosity** |

- ★ **소재가 우리 production과 정확히 일치** (LPSCl + NCM811). Bazzoun(LPSCl+NMC811)·Lee(LPSCl+NCM811/82)와 같은 *우리 소재계* 실험-앵커 클러스터. 같은 UCSD(Ping Liu) 그룹 — Doux 2020(Meng, UCSD)와 같은 기관 계보·**같은 LPSCl 작동압 주제의 양극-microstructure 버전**.
- ★ **저자에 H. Alicia Kim**(구조최적화·계산역학) + **Ping Liu**(실험) 공동교신 → 실험과 시뮬(LAMMPS DEM)을 한 논문에서 결합. **LG Energy Solution 공저** = 산업 ASSB.
- 동반 데이터 파일: `docs/data/tailored_cathode_low_pressure.csv` — CAM utilization vs overlap(Table 1), porosity/τ/BET, σ(EIS R_b/R_SEI/R_ct), capacity·retention vs 3압력(2/10/30 MPa), fab-vs-operating.

---

## 3. 핵심 물성 (수치) ★ — stated/digitized 명시

> ⚠ 본문 텍스트에 stated 된 값과 그림에서 읽은(digitized) 값을 칸마다 구분. SI(Figure S1–S21, Table 등)는 main text가 인용한 stated 값만 신뢰로 기록.

| 물성 | 값 | 조건 (P, 조성) | stated/digit | 비고 |
|---|---|---|---|---|
| **porosity (FIB-SEM)** | **coarse 11.3 % / fine 4.4 %** | 펠릿(전해질), 제조압(SI) | **stated** (본문 p968) | ★ fine이 ~2.6× 더 치밀; SE 미세화→packing↑ |
| **relative density** | **fine ~90 %** (Figure S8) | 펠릿 | stated | porosity 4.4 %와 정합(≈95.6 %는 SEM-pore, S8은 rel.dens) |
| **tortuosity (FIB-SEM, LPSC 상)** | **coarse 1.84 / fine 1.21 (median)** | 3D 재구성, LPSC 경로 | **stated** (본문 p968) | ★ fine이 덜 우회 → 이온수송↑ |
| **BET 비표면적** | **coarse 6.02 / fine 9.24 m²/g** | 전해질 분말 | **stated** | roll-mixing이 표면적↑(=계면접촉↑ 간접) |
| **CAM utilization (DEM)** | coarse **94/83/56/20 %**, fine **100/100/94/28 %** | minimum overlap **0/2/5/10 %** | **stated** (Table 1) | ★★ **coverage/contact 직접 대응** — fine@2 % overlap **≈100 %** vs coarse 83 % |
| **R_b (SSE bulk/GB, EIS)** | coarse vs fine (Fig 1e) | full cell, 제조 후 | digitized (TREND) | DRT P1(GB)에서 분리 |
| **R_ct (charge transfer)** | **17.3 (coarse) → 9.9 Ω (fine)** | full cell, 제조 후 | **stated** (본문 p968) | ★ fine이 charge-transfer 저항 ~43 %↓ (핵심 결과) |
| **σ_ionic (LPSC@To rolling)** | "fine 샘플 중 최고" (정성) | EIS, 펠릿 | stated(정성) | roll-mixing이 LPSC 원물성 보존(ball-mill은 Li₂S 불순물↑) |
| **1st-cycle 용량 우위(fine−coarse)** | **+18 / +20 / +22 mAh/g** | **30 / 10 / 2 MPa** | **stated** (본문 p969) | ★ 저압일수록 fine 우위↑ (압력↓→microstructure 중요↑) |
| **capacity retention @100 cyc** | coarse **84.0 / 74.3 / 63.3 %** vs fine **90.3 / 88.9 / 85.6 %** | **30 / 10 / 2 MPa** | **stated** (Fig 2c) | ★★ **저압 retention 격차 = +7.5 / +19.7 / +35.2 %p** (압력↓→격차↑) |
| **R_SSE/NCM 증가 @100cyc, 2 MPa** | coarse **+545 Ω** vs fine **+34 Ω** | full cell EIS, 2 MPa | **stated** (본문 p971) | ★ 저압서 coarse 계면 급열화 (16× 더 증가) |
| **DRT(R_ct) 면적 증가 @100cyc** | 30 MPa +8 % / 10 MPa +26 % / 2 MPa **+115 %** (coarse 대비 fine) | full cell | **stated** | 저압서 coarse charge-transfer kinetics 급저하 |
| **TGA 분해온도** | **~365 °C** (both, no new peak) | 잔류 toluene 확인 | stated | fine-LPSC에 toluene 잔류 無 |
| **PSD (fine LPSC)** | 대부분 **1–3 µm**, 일부 <1 µm; ball-mill은 <0.25 µm 多 | wet roll-mix(@To) | stated | roll@To가 <0.25 µm 적고 >3 µm 보존 → 균일 |
| **PSD (CAM)** | **NCM811 ~1–5 µm** | | stated | SE(fine)≈CAM ⇒ 우리 12:4:1 ≠ (여긴 SE≈CAM) |
| **Heckel P_y / coordination Z / E_SE / σ_y / ν** | **n/a** | | | 압밀 모델(Heckel)·배위수·탄성계수·항복강도 측정/계산 **없음** (§10) |

**porosity convention 주의**: 11.3/4.4 %는 **FIB-SEM 단면 pore-segmentation**(Figure S7 pore-size 분석 + S8 relative density). 우리 ε_sphere(material-conserving 압밀 porosity)와 **방법이 다름**(실측 SEM void) → 추세(fine<coarse)는 우리 "미세 SE→packing↑"와 정합하나 절대값 직접대조는 주의.

---

## 4. 시뮬레이션 방법 ★ (Simulation method)

- **code / version**: **LAMMPS** — **"granular package"** (Plimpton 2024, ref 21) 사용한 **DEM**. ★ **우리 LIGGGHTS(=LAMMPS 기반 granular)와 같은 코드 계열**. + **FIB-SEM 3D 재구성 tortuosity**(Tjaden 2016 Bruggeman 맥락, ref 22).
- **DEM 접촉법칙**: **"interparticle forces were simulated using Hertzian contact within the granular package of LAMMPS"** (본문 p968). ⇒ **Hertzian(탄성) 접촉** — **항복·소성 접촉법칙 명시 안 됨**(Thornton–Ning·EEPA·H-cap 등 없음). 우리 hooke/hysteresis와 같은 *탄성 계열* 강체-구 DEM.
- **calendaring(압연/캘린더링) 모델**: **velocity-Verlet, microsecond 단위 explicit time step**으로 calendaring(다지기) 과정을 모사 (수치 안정성 확보 목적 명시).
- **재료 파라미터 (E_SE, E_CAM, ν, μ, COR, σ_y)**: **n/a — 본문/표에 수치 미기재**. Hertzian 접촉이라 E·ν가 들어가야 하나 main text는 값을 안 줌(SI Simulation method에 있을 수 있으나 본문 인용 없음 → 기록 n/a). ⇒ **E_SE 강성·항복 파라미터 미공개 = 우리 E_eff 1.35/항복캡과 직접 비교 불가**.
- **bond/binder 모델**: **없음**(binder 입자·SBR/CB/PTFE bond 모델 미사용; 도전제도 시뮬에 미포함). 순수 AM+SE 구 패킹.
- **MPM/continuum**: **없음**. 소성 SHAPE 변형·void-fill flow·변형장 일절 없음 (= rigid-sphere DEM의 본질 한계 — 우리 MPM이 메우는 칸).
- **전달 솔버 (RNM/Kirchhoff)**: **없음**. ★ 중요 — 이 논문 DEM은 **σ(전도도)를 풀지 않는다.** σ_ionic은 **실험 EIS**로 측정. DEM은 오직 **CAM utilization(= AM이 SE와 접촉한 비율)** 과 **tortuosity 맥락의 입자 패킹**만 산출. (tortuosity 1.84/1.21은 **FIB-SEM 실측 3D**이지 DEM 산출 아님 — Figure S15.)
- **입자 처리** ★ (DEM판 "무질서 처리"): **완벽 구(discrete spherical particles)** 명시 ("Li ion transport tortuosity ... modeled using **discrete spherical particles**"). **rigid sphere + Hertzian CONTACT**(δ-overlap) — **진짜 SHAPE 소성 없음**. PSD: **bimodal/poly 가능**(AM ~1–5 µm, SE coarse~20 / fine~1 µm를 실제 입경분포로 넣어 calendaring). ⇒ 우리와 **같은 부류**: rigid-sphere + 탄성접촉 + δ-overlap을 접촉지표로 사용. **"minimum overlap" criterion**으로 CAM utilization을 정의 = 우리 contact/coverage의 overlap-임계 정의와 *직접 대응*.
- **도메인/RVE / servo / seeds / 압력범위**: 구체적 box 크기·seed·servo/PID **미기재**(본문). calendaring = 변위-기반 다지기(우리 hold-protocol 계열). **제조압 수치 미기재**(작동압 2/10/30 MPa는 *cycling* 압력 — DEM 입력 아님).
- **특이사항/튜닝**: ★ **CAM utilization 정의(ref 14, Shi 2020)** — "AM 입자가 SE와 **접촉(overlap ≥ 임계)** 한 비율"을 minimum overlap **0/2/5/10 %**(두 입자 반경합 대비 overlap)로 스캔. **fine@2 %=~100 %**, **coarse@2 %=83 %** → "fine이 더 많은 AM에 SE 접촉을 공급 → 더 높은 활용용량". ⇒ **이게 우리 coverage(AM_*_by_SE)·contact-network·dead-AM의 직접 실험-시뮬 대응** (overlap 임계 = 우리 Hertz/Tabor 접촉 임계와 같은 개념틀).

---

## 5. 섹션별 결과 — 전수 (Section-by-section, ALL numbers)

### 5.1 동기 (Intro, p966–967)
ASSB 양극은 CAM이 SE에 *직접 둘러싸여* 있어 **(1) 불완전 고체-고체 접촉, (2) SE가 gap/void를 못 메움, (3) (de)lithiation 부피변화로 구조 불안정, (4) CAM-SE 계면 박리** 4문제 → 균질 percolation 망 형성 실패·이온수송 저하. ⇒ 통상 **고 stack pressure 필요**. Sakka(Sakuda) et al.(ref 12)이 X선 CT로 **50 MPa에서 SE가 내부 cavity를 채워 접촉면적↑·R_ct↓**(12 MPa 이하 대비)를 보였으나 고압은 **생산비↑·에너지밀도↓**. **모델 연구는 25 MPa면 안정 계면접촉에 충분**(ref 12 모델)하나 산업은 **≤5 MPa** 지향. ⇒ **저압에서 최적 접촉·낮은 tortuosity를 *microstructure 설계*로 확보**가 핵심전략. 선행: 작은 SE(~4 µm)가 charge transport↑(ref 13), SE 크기↓→CAM utilization↑(Tan, ref 14), 작은 CAM도 접촉점↑(ref 14), hierarchical(작은 ~300 nm + 큰 ~20 µm Li₆₋ₓPS₅₋ₓCl₁.₅) → tortuosity↓·이온수송↑(ref 16), CAM에 SE층 코팅 → 저압서도 친밀접촉(ref 17–19). **본 연구 = wet roll-mixing으로 fine-LPSC 제조 → 저압 고성능 양극 architecture.**

### 5.2 fine-LPSC 합성·특성화 (p967–968, Fig 1 + S1–S9)
- **합성법 4종**(Figure S1): ball-milling without solvent (LPSC ball-milling), roll-milling without solvent (LPSC rolling), ball-milling with toluene (LPSC@To ball-milling), **roll-milling with toluene (LPSC@To rolling, 채택)**. Figure S2: 4종 모두 입경 ~1 µm로 감소. Figure S3: ball-mill이 roll-mill보다 더 작음(고에너지).
- ★ **roll@To의 우월성**: ball-mill은 **<0.25 µm 미세분 多**(불균일), roll@To는 **<0.25 µm 적고 >3 µm 보존** → 균일 PSD → 낮은 tortuosity의 양극 구조(ref 16). **XRD(Figure S4)**: LPSC **ball-milling은 Li₂S 불순물** 출현(분해) vs LPSC@To rolling은 coarse와 동일(원구조 보존). **EIS(Figure S5)**: LPSC@To rolling이 **fine 샘플 중 σ_ionic 최고** → roll-mixing+toluene이 LPSC 손상 최소·원물성 보존. **TGA(Figure S6)**: 분해온도 ~365 °C, 신규 peak 없음 → **잔류 toluene 無**.
- **FIB-SEM pore(Figure S7)**: coarse **11.3 % porosity** vs fine **4.4 %** → fine이 더 치밀. **상대밀도(Figure S8)**: fine ~**90 %**. **BET(Figure S9)**: coarse **6.02** / fine **9.24 m²/g** → roll-mixing이 표면적↑(SEM 관찰과 정합) → 계면접촉↑ 기대.
- **분포 균일성(Fig 1a,b + S10–S13, EDX Ni·P 맵)**: **coarse-LPSC = LPSC 심한 응집·NCM811 주위 불균일 분포**(Fig 1a,S12) vs **fine-LPSC = LPSC가 NCM811 주위 균일 분포 → 균질 microstructure**(Fig 1b,S13). ⇒ ★ **"fine SE가 CAM을 더 고르게·치밀하게 덮는다"** = 우리 coverage↑의 실험 SEM 증거.

### 5.3 ★ DEM CAM utilization (p968, Table 1, Fig 1c,d + S14)
- **방법**: AM+SE를 **discrete spherical particles**로, **Hertzian 접촉(LAMMPS granular)**, **velocity-Verlet calendaring**. **CAM utilization = NCM811 입자가 LPSC와 접촉한 비율**(ref 14), 접촉 criterion = **minimum overlap(두 입자 반경합 대비 overlap %)**.
- **Table 1 (핵심 표)**:

  | Configuration | Min overlap | CAM utilization |
  |---|---|---|
  | **Coarse-LPSC** | 0 % | **94 %** |
  | | 2 % | **83 %** |
  | | 5 % | **56 %** |
  | | 10 % | **20 %** |
  | **Fine-LPSC** | 0 % | **100 %** |
  | | 2 % | **100 %** |
  | | 5 % | **94 %** |
  | | 10 % | **28 %** |

- ★★ **해석**: 더 엄격한 접촉기준(높은 overlap 요구)일수록 utilization↓ — 하지만 **모든 기준에서 fine ≫ coarse**. **2 % overlap에서 fine=~100 % vs coarse=83 %** → fine이 **거의 모든 CAM에 SE 접촉을 공급**(Fig 1c,d: coarse는 **미접촉 CAM = 빨간 atom** Fig 1c/S14e 다수; fine은 거의 없음). ⇒ "fine-LPSC가 우월한 interparticle contact 덕에 더 높은 활용용량 전달". **시뮬 예측이 실험 1st-cycle 용량(fine +18~22 mAh/g)과 정량 상관** — "utilization↑ → capacity↑". (단 §5.6 슬라이트 불일치: 실험 coarse가 fine의 ~85 % 용량 → "특정 C-rate에 맞춘 overlap 추가 보정 필요" 인정.)
- **Fig 1c,d 우측 = Li⁺ ion paths**(FIB-SEM 3D): coarse는 구불구불(높은 tortuosity), fine은 직선적(낮은 tortuosity) — §5.4와 연결.

### 5.4 ★ tortuosity (p968, Fig 1c,d + S15)
- **FIB-SEM 3D 재구성**(Tjaden Bruggeman 맥락, ref 22)으로 **LPSC 상 tortuosity** 분석: **fine median 1.21 vs coarse 1.84**. ⇒ ★ **fine이 더 직접적 이온경로 → (de)lithiation 중 Li 수송↑**. (이건 DEM이 아니라 **실측 3D 형상**의 tortuosity — 우리 τ_Laplace/τ_Dijkstra와 같은 *구조적 우회도*.)

### 5.5 ★ EIS·DRT — charge-transfer (p968–969, Fig 1e,f + S16)
- **등가회로(Fig 1e)**: **R_b(SSE bulk+GB)** — **R_SEI∥CPE_SEI** — **R_CT∥CPE_NCM** — W(Warburg). **R_ct이 핵심 변화점**: **coarse 17.3 Ω → fine 9.9 Ω**(43 %↓). ⇒ fine이 charge-transfer kinetics 개선.
- **DRT(Fig 1f, peaks P1–P7, Figure S16)**: **P1 = grain-boundary 저항** — fine에서 R↓하나 **time constant τ가 0.5 → 1.4 µs로 증가**. τ=R·C이므로 τ↑ = **GB capacitance↑** → (조성 불변이므로) **계면면적↑**(작은 입자 → 표면적↑, BET 9.24와 정합). **P4 = cathode 계면 charge-transfer** — fine에서 R↓(Fig S16) → fine이 양극 내 Li 수송·charge-transfer 촉진. ⇒ "fine-LPSC가 양극 내 이온수송·charge-transfer를 효과적으로 향상".

### 5.6 ★ 전기화학 성능 vs 3압력 (p969–970, Fig 2)
- **셀**: NCM811 양극 + LPSC + **Li-metal 음극**, **0.1 C, 30 °C**, **30 / 10 / 2 MPa**.
- **1st-cycle 용량 우위(fine − coarse)**: **+18 (30 MPa) / +20 (10 MPa) / +22 mAh/g (2 MPa)** → ★ **저압일수록 fine 우위↑**(utilization 시뮬과 정합). coarse는 fine의 **~85 % 용량**. (이론 utilization 100/83 = fine 1.20× → 실험 ~1.18×, 약간의 슬라이트 차 = C-rate별 overlap 보정 필요 인정.)
- **★★ Cycling retention @100 cyc(Fig 2c)**:
  - **30 MPa**: coarse **84.0 %** / fine **90.3 %** → **+7.5 %p** (격차 작음)
  - **10 MPa**: coarse **74.3 %** / fine **88.9 %** → **+19.7 %p**
  - **2 MPa**: coarse **63.3 %** / fine **85.6 %** → **+35.2 %p** (격차 최대)
  - ⇒ ★ **"압력↓ → microstructure(fine) 우위↑"**가 본 논문의 정량 핵심. 고압에선 둘 다 잘 됨(SE가 어차피 cavity 채움), **저압에선 fine만 살아남음**.
- **Rate capability(Figure S18, 0.1–0.5 C)**: fine이 **0.3 C +40 % / 0.5 C +50 %** 더 높은 용량.

### 5.7 ★ GITT 분극 + EIS 사이클 열화 (p970–971, Fig 3)
- **GITT(Fig 3a–c)**: fine이 **30·10 MPa에서 더 낮은 분극, 2 MPa에서 특히 현저**. 분극 = 불완전 고체접촉(uneven contact·microvoid·NCM811 내부 균열)의 지표.
- **EIS @1·100 cyc(Fig 3d–f) + DRT(Fig 3g–i)**: **R_SSE/NCM** 100cyc 후 양쪽 다 증가(=R_ct↑·CEI 저항↑·bulk NCM811·계면 열화). ★ **압력↓일수록 coarse의 R_SSE/NCM ≫ fine**:
  - **2 MPa, 100cyc**: **coarse R_SSE/NCM +545 Ω vs fine +34 Ω** (16× 차) — "coarse 결정구조·계면 심한 decay".
  - **DRT(R_ct, 10⁻⁴–10⁻¹ s) 면적 증가**: 30 MPa **+8 %**, 10 MPa **+26 %**, **2 MPa +115 %**(coarse vs fine) → 저압서 coarse charge-transfer kinetics 급저하.
- ⇒ "**고압에선 microstructure가 Li 수송에 영향 적음**(SE가 어차피 채움), **저압에선 microstructure가 결정적**" — fine이 친밀접촉·낮은 tortuosity로 저압 장기안정.

### 5.8 ★ 구조 안정성 — 균열·분해 (p971–972, Fig 4)
- **FIB-SEM 사이클후(Fig 4a–f)**: **coarse-LPSC = NCM811 microcrack**(10 MPa부터, 2 MPa 더 심함 Fig 4c) — SE 불완전접촉→불균일 전류→국소 과충/과방→Li⁺/Ni²⁺ mixing·격자뒤틀림·입자 strain→균열(ref 29). **fine = 균열 현저히 적음**(Fig 4d–f) → 저압서도 안정.
- **XRD(Fig 4g–i)**: 둘 다 α-NaFeO₂(R3̄m, NCM811) + argyrodite(F4̄3m, LPSC). ★ **coarse @2 MPa = polysulfide Li₂Sₓ 불순물 peak**(ref 30) = SE 분해. **I(003)/I(104) 비**(Li/Ni mixing 지표): 10·2 MPa에서 coarse 1.121/1.011 vs fine **1.388/1.204** → **fine이 Li/Ni mixing 적음**(더 균일 Li 수송·안정 결정구조).
- **XPS(Figure S20)**: 압력 30→2 MPa로 갈수록 분해산물(P₂Sₓ polysulfide·Li₂Sₓ)↑; **161.7 eV(PS₄³⁻ SSE) peak 감소**. **fine이 계면 부반응 훨씬 적음** — 균일 전류·전위분포가 국소 열화 억제. **STEM(Figure S21)**: coarse 100cyc 후 표면 rock-salt(Fm3̄m) 층(심한 Li/Ni mixing·상전이) vs **fine = 비가역 상전이 無** → 우월한 구조안정성.

### 5.9 결론 (p972)
**wet roll-mixing fine-LPSC → CAM 주위 SE 균일분포·낮은 tortuosity·R_ct↓ → 저압(2 MPa) 장수명(85.6 % @100cyc vs coarse 63.3 %)·균열↓·분해↓.** microstructure 품질이 **저압 ASSB 성능의 결정인자**. "고압에선 microstructure 영향 적고, **압력↓일수록 microstructure가 결정적**" → 산업 저압 ASSB 상용화 가속.

---

## 6. Figure / SI 전수 (각 그림이 무엇을·우리가 뭘 쓰나) ★

### 본문 Figure
| Fig | 내용 | 핵심 수치 | 우리가 쓸 점 |
|---|---|---|---|
| **TOC** | coarse vs fine 모식: 빈약/균일 LPSC-NCM 접촉, 불균일/균일 Li⁺ flux | — | coverage↑→균일 flux 개념도 |
| **1a,b** | FIB-SEM 단면 coarse(LPSC 응집) vs fine(균일) | scale 20 µm | ★ fine이 CAM 고르게 덮음(coverage SEM 증거) |
| **1c,d** | DEM 입자 모식(좌, 미접촉 CAM=빨강) + FIB-SEM Li⁺ paths(우) | utilization·tortuosity | ★ **CAM utilization 시각화** + 이온경로 우회도 |
| **1e** | Nyquist + 등가회로(R_b/R_SEI/R_ct/W) | **R_ct 17.3→9.9 Ω** | ★ charge-transfer 저항 앵커 |
| **1f** | DRT(P1–P7) coarse vs fine | P1(GB) τ 0.5→1.4 µs; P4(R_ct)↓ | ★ GB·계면 분해 분석법 |
| **2a,b** | 충방전 voltage profiles, 3압력(30/10/2 MPa) × coarse/fine, 100cyc | fine 더 안정 | 압력별 cycling raw |
| **2c** | ★★ **Cycling life + CE, 3압력** | retention **84.0/74.3/63.3 (coarse) vs 90.3/88.9/85.6 % (fine)**; 격차 +7.5/+19.7/+35.2 %p | ★★ **저압 retention 격차 = backlog B6 핵심 데이터** |
| **3a–c** | GITT 분극, 3압력, 100cyc 후 | fine 저분극(2 MPa 현저) | 분극=불완전접촉 지표 |
| **3d–f** | Nyquist 1·100cyc, 3압력 | **2 MPa: coarse R_SSE/NCM +545 vs fine +34 Ω** | ★ 사이클 계면열화 vs 압력 |
| **3g–i** | DRT(R_ct) 1·100cyc | R_ct 면적 +8/+26/**+115 %** | ★ charge-transfer kinetics 저압 급저하 |
| **4a–f** | FIB-SEM 100cyc 후 균열, 3압력 | coarse microcrack(2 MPa 심함) vs fine 적음 | ★ NCM811 균열 vs 압력(우리 AM 파괴 대응) |
| **4g–i** | XRD 100cyc 후, 3압력 | coarse@2MPa Li₂Sₓ; I(003)/I(104) 1.121/1.011 vs 1.388/1.204 | ★ SE 분해·Li/Ni mixing 지표 |

### SI Figure (main text 인용분만)
| SI | 내용 | 핵심 수치 | 우리가 쓸 점 |
|---|---|---|---|
| **S1** | 합성 4종 모식 | — | fine-LPSC 제법 |
| **S2** | 4종 입경(모두 ~1 µm) | ~1 µm | PSD |
| **S3** | ball-mill < roll-mill 입경 | — | 고에너지=더 미세 |
| **S4** | XRD: LPSC ball-mill = **Li₂S 불순물** / roll@To = coarse 동일 | — | ★ roll@To가 원구조 보존 |
| **S5** | EIS: **LPSC@To rolling σ 최고** | 정성 | roll-mix가 σ 보존 |
| **S6** | TGA: 분해온도 ~365 °C, 잔류 toluene 無 | 365 °C | 잔류용매 검증 |
| **S7** | FIB-SEM pore: **coarse 11.3 % / fine 4.4 %** | ★ | ★★ **porosity 앵커** |
| **S8** | relative density: **fine ~90 %** | ★ | rel.dens 앵커 |
| **S9** | BET: **6.02 / 9.24 m²/g** | ★ | 표면적(계면접촉 간접) |
| **S10–S13** | EDX Ni·P 맵 coarse(불균일)/fine(균일) | — | ★ coverage 균일성 |
| **S14** | DEM 모식 + e: 미접촉 CAM(red atom) | utilization | ★★ **CAM utilization 시각화** |
| **S15** | tortuosity 분석 | **1.84 / 1.21** | ★★ **tortuosity 앵커** |
| **S16** | DRT P1–P7 상세(P1 GB·P4 R_ct) | τ 0.5→1.4 µs | DRT peak 귀속 |
| **S17** | 추가 cycling | — | Fig 2 보강 |
| **S18** | rate capability 0.1–0.5 C | fine +40/+50 % @0.3/0.5 C | rate 우위 |
| **S19** | EIS fitting(R 값 산출) | — | R_SSE/NCM·R_ct·R_CEI 출처 |
| **S20** | XPS 분해(P₂Sₓ·Li₂Sₓ·161.7 eV PS₄³⁻↓) | — | 계면 부반응 vs 압력 |
| **S21** | STEM: coarse rock-salt 층 / fine 무전이 | — | ★ 구조안정성 |

---

## 7. Post-processing ★ (방법론)

- **무엇**:
  - **CAM utilization (DEM)**: AM-SE **접촉비율 vs minimum overlap(0/2/5/10 %)** 스캔 (ref 14 Shi 2020 방법). = 우리 **coverage/contact 임계 정의의 직접 대응**(overlap 임계 = Hertz/Tabor 접촉 임계).
  - **tortuosity**: **FIB-SEM 3D 재구성** → LPSC 상 median tortuosity (Bruggeman 맥락, Tjaden ref 22). = 우리 τ_Laplace/τ_Dijkstra와 같은 구조 우회도(단 그들=실측 3D, 우리=네트워크/Laplace).
  - **porosity**: FIB-SEM 단면 pore-segmentation(11.3/4.4 %) + relative density(~90 %). = 실측 SEM void (우리 ε_sphere 압밀 convention과 방법 다름).
  - **EIS 등가회로 피팅**: R_b—R_SEI∥CPE—R_ct∥CPE—W → R_ct·R_SSE/NCM·R_CEI 분리 추출.
  - **DRT(distribution of relaxation times)**: P1–P7 peak 귀속(P1 GB, P4 양극 R_ct), τ=R·C로 capacitance(=계면면적) 변화 추론.
  - **XRD I(003)/I(104)** = Li/Ni mixing 정량(ref 32); **XPS** 분해산물 정량; **STEM** rock-salt 상전이.
- **도구**: LAMMPS(granular, velocity-Verlet) + FIB-SEM(Tjaden Bruggeman) + EIS/DRT 피팅(상용) + BET + TGA + XRD(FullProf 류) + XPS + STEM. (구체 SW 버전은 SI.)
- **수치화·플롯·기록**: σ는 **실험 측정**(DEM은 σ 안 풂); CAM utilization은 **DEM 직접 산출(Table 1)**; tortuosity·porosity는 **FIB-SEM 실측**; retention은 셀 cycling 실측.

---

## A. 우리 DEM+MPM 대비 (comparison vs ours) → `our_dem_baseline.md`

> 핵심 원칙: 같은 소재(LPSCl+NCM811)·같은 코드계열(LAMMPS granular) → **frame[4] 외부 앵커**. 그들 DEM이 *CAM utilization(=coverage)* 을 직접 산출하나 *σ는 안 풀고*(실험 측정), *소성 SHAPE·Heckel·E_SE 값* 미공개. 우리는 그 빈 칸(σ 삼중항·Heckel·MPM morphology)을 채운다.

| 항목 | 이 논문 (Zhou 2025) | 우리 (DEM+MPM) | 차이 / 매핑 (정직) |
|---|---|---|---|
| **소재 (SE/CAM)** | **LPSCl + NCM811** | **동일** | ★ Bazzoun·Lee·Doux와 같은 *우리 소재계* — SE/CAM 물리 직접 전사 가능(halide·LIB와 다름) |
| **코드** | **LAMMPS granular (Hertzian, velocity-Verlet calendaring)** | **LIGGGHTS(=LAMMPS 기반), hooke/hysteresis** | ★ 같은 코드 계열·같은 *탄성-접촉 강체-구* DEM (Bazzoun도 LIGGGHTS) |
| **입자 처리** | **rigid sphere + Hertzian CONTACT(δ-overlap)**, bi/poly-PSD | rigid sphere + hooke/hysteresis CONTACT(δ-overlap) + E_eff 18× 연화 | ★ 둘 다 **CONTACT-탄성(δ 프록시), 진짜 SHAPE 소성 아님** — 둘 다 MPM이 메우는 한계 |
| **CAM utilization / coverage** | **DEM 직접 산출**: fine 100/100/94/28 % vs coarse 94/83/56/20 % (overlap 0/2/5/10 %) | 우리 **coverage_AM_*_by_SE**(Hertz 16–48 % / Tabor 48–52 %, real_14) + **dead-AM(f_AM^cc<80 % 경고)** | ★★ **직접 대응 축** — 그들 "minimum overlap 임계" = 우리 Hertz/Tabor 접촉 임계; 그들 "미접촉 CAM(red atom)" = 우리 dead-AM. **우리 coverage 정의의 실험-시뮬 검증점** (단 그들=*전체 CAM 접촉비율 한 수*, 우리=*표면 덮임 % + 접촉면적*; 측정량 결 다름 — 추세/개념 대응) |
| **transport σ** | **DEM은 σ 안 풂** — σ_ionic은 **실험 EIS** | **Kirchhoff/Holm σ 삼중항**(σ_i/σ_e/σ_thermal), R=1/(2σr_c), Stage-E | ★ **우리 강점** — 그들은 utilization→capacity 상관까지, 명시적 σ-network 없음. Bielefeld2019처럼 "percolation/utilization은 주되 σ는 안 풂" 부류 |
| **tortuosity** | **FIB-SEM 실측 1.84(coarse)/1.21(fine)** | τ_Laplace,eff / τ_Dijkstra (네트워크), Minnmann τ_ion 2.07 | ★ **frame[4] 실측 τ 앵커** (그들=실측 3D 형상, 우리=접촉망 우회도; 추세 "미세 SE→τ↓" 일치) |
| **porosity** | **FIB-SEM 11.3 %(coarse)/4.4 %(fine)** (펠릿) | DEM 15.6 % / MPM 16.7 %(real_14 composite); pure-SE ~10 %; rigid floor ~20 % | ⚠ 방법 다름(그들 SEM void vs 우리 ε_sphere 압밀); **추세(미세 SE→치밀)는 우리 size=packing과 정합**. ★ fine 4.4 %는 우리 pure-SE 10 %보다 *낮음* → roll-mix 미세분이 강체 floor 아래로 (단 절대값 직접대조 금지) |
| **fab vs operating 압력** | ★ **operating 2/10/30 MPa(cycling) 명시 분리**; 제조압=별도(SI) | **300 MPa = 제조(Heckel P_y 138)**; 작동 수~수십 MPa(별도 영역) | ★★ Doux/Lee/Minnmann "fab≠operating" 클러스터에 합류; ★ **"microstructure가 *저압에서만* 차이를 만든다"**는 *작동압 메커니즘* 추가(B6) |
| **AM 균열** | **coarse NCM811 microcrack(저압 심함)** vs fine 적음 | DEM AM_P 파괴 37–40 %(92:8 8mAh), Auerbach, fracture-Holm | ★ frame[4] — 단 그들 driver = *사이클 불균일전류*(Li/Ni mixing), 우리 = *압밀 접촉응력*(Auerbach) → 결 다름(Kang2025·Lee2025와 같은 "다결정 2차입자 깨짐" 계보) |
| **E_SE / σ_y / Heckel** | **n/a**(미공개) | E_eff 1.35(DEM)/1.53(MPM), Heckel P_y 138 | 그들 압밀-모델 파라미터 없음 → 우리 강점(정량 압밀·Heckel) |
| **소성 morphology / void-fill** | 없음(rigid sphere) | MPM 진짜 소성 형상변화(SEM 일치)·void-fill·Σdg | ★ 우리 MPM 고유 — 그들 rigid-sphere가 비운 칸 |

### ★ "CAM utilization vs overlap" 과 "우리 coverage" 의 정밀 대응 (over-claim 방지)
- 그들 **CAM utilization** = "AM 입자 중 SE와 (overlap≥임계) 접촉한 **개수 비율**" (한 입자가 SE에 닿으면 1, 아니면 0 → 전체 평균). minimum overlap 0/2/5/10 %는 "얼마나 깊이 눌려야 *접촉*으로 칠지" 임계.
- 우리 **coverage** = "각 AM **표면적 중 SE로 덮인 %**"(Hertz/Tabor 접촉면적 기반) + **dead-AM**(전자/이온망에서 끊긴 AM 비율 f_AM^cc).
- ⇒ **개념틀은 같다**(둘 다 *AM-SE 접촉의 충분성*을 overlap-임계로 정의), **측정량은 다르다**(그들=접촉 *입자수* 비율, 우리=표면 *덮임 면적* % + 망 연결성). ★ 그들 "fine@2 %=100 % vs coarse=83 %"는 **우리 coverage가 미세 SE에서 올라가는 방향**을 *같은 코드계열 DEM으로 독립 확인* — 단 우리 coverage **절대 %**를 그들 utilization %와 *동일시 금지*(서로 다른 분모). frame[4] *추세·개념* 교차검증.
- ★ 그들 "minimum overlap criterion"은 **우리 Hertz vs Tabor 접촉 임계 논쟁의 외부 대응**: overlap 임계를 높이면(엄격) utilization 급감(coarse 94→20 %). = 우리 Hertz(작은 접촉면적, 엄격)→Tabor(plastic-spread, 관대)에서 coverage가 16→52 %로 벌어지는 것과 같은 *임계-민감성*. ⇒ **"접촉을 어디서 끊느냐가 결과를 좌우"**의 공통 교훈.

### ★ "microstructure가 저압에서만 차이를 만든다" — 우리 fab-vs-operating 분리에 대한 직접 기여
- Doux는 "5 MPa 최적"(*현상*), Lee는 "co-rolling robust 계면→2 MPa 가능"(*공정→작동압*). **Zhou는 한 걸음 더: *같은 압력 범위(2/10/30 MPa)에서 microstructure(fine vs coarse)가 retention 격차를 +7.5→+35.2 %p로 벌린다***(압력↓→격차↑). ⇒ **작동압 성능 = f(microstructure 품질, 작동압)** 의 정량 2D 맵. "고압에선 SE가 어차피 cavity를 채워 microstructure 무관, **저압에선 microstructure가 결정**" = 우리가 σ_ionic/coverage를 *작동압*에서 논할 때의 **인과 메커니즘**.
- 우리 모델 매핑: **우리 DEM coverage/contact-network(300 MPa 제조)** 가 높으면(=fine 유사) → *작동압이 낮아도* 이온/전자 percolation 유지 → retention↑. **coverage가 낮으면(coarse 유사)** → 저압서 접촉 끊김→R_ct↑→균열→급열화. ⇒ ★ **우리 coverage·dead-AM·σ가 "저압 cyclability"의 *예측 변수*가 될 수 있다**(B6).

---

## B. 적용가능성 (applicability to our model) ★

구체적으로 **무엇이 우리 모델의 어느 칸에 frame[4] 앵커가 되나**:

- **① ★★ CAM utilization(Table 1) → 우리 coverage/contact-network 검증 (1순위)**:
  - 그들 fine 100/100/94/28 % vs coarse 94/83/56/20 % (overlap 0/2/5/10 %) = **같은 LPSCl+NCM811·같은 LAMMPS-granular DEM**의 coverage-analog. → 우리 `coverage_AM_P/S_by_SE`(Hertz/Tabor)·`f_AM^cc`(dead-AM)의 **방향·임계-민감성을 독립 검증**. 흡수: 우리 coverage를 **overlap-임계 스윕**으로도 리포트해(Hertz=엄격↔Tabor=관대) 그들 0→10 % 곡선과 *형태* 대조. `docs/data/tailored_cathode_low_pressure.csv`의 utilization 행.
  - ⚠ 절대 % 동일시 금지(분모 다름: 입자수 vs 표면면적). **개념/추세 앵커**.
- **② ★ tortuosity 실측(1.84/1.21) → 우리 τ 앵커**: Minnmann τ_ion 2.07(NCM622+LPSCl 복합)과 같은 계열의 *NCM811+LPSCl* 실측 τ. **fine 1.21 = 거의 ideal**(우리 production fine-SE 목표의 실측 하한). 우리 τ_Laplace/Dijkstra 예측이 "미세 SE→τ↓"를 내는지 cross-check. (단 그들=실측 3D, 우리=네트워크 → 추세.)
- **③ ★ porosity(11.3/4.4 %) → densification DB**: `docs/data/densification_porosity_db.csv`에 **LPSCl 펠릿 coarse 11.3 % / fine 4.4 %** 행 추가 가치 — 단 **방법(SEM void)·제조압 미공개**라 *fine<coarse 추세*와 *우리 pure-SE 10 %와의 대비*(fine이 더 낮음=미세분 packing)로만, porosity 절대칸은 "method=FIB-SEM, P=n/a" 명시.
- **④ ★★ operating-pressure 축(backlog B6) — 핵심 앵커**:
  - **retention vs (microstructure, 작동압)**: coarse 84.0/74.3/63.3 vs fine 90.3/88.9/85.6 % @30/10/2 MPa = **B6의 정량 데이터**("P sweep→void→σ↓"). + **R_SSE/NCM 사이클 증가(2 MPa coarse +545 vs fine +34 Ω)** = 저압 계면열화의 *시간축* 시그니처(Kang2025 R_int·R_w↑와 같은 계열).
  - 매핑: 우리 정적 σ/coverage(300 MPa 제조)를 **작동압 retention의 예측 변수**로 연결하는 인과("coverage↑ → 저압서도 percolation 유지 → retention↑"). B6 "void-vs-P 시간축"에 **microstructure 의존성**을 추가.
- **⑤ ★ R_ct(17.3→9.9 Ω) → 우리 ASR/계면 (Kim2025 R_ct 클러스터)**: charge-transfer 저항은 우리 σ-솔버가 *안 잡는* 칸(z₁ 이온레일만) → Kim2025 R_ct·Kang R_int와 함께 **"계면 kinetics = 우리 미보유, microstructure(coverage)가 좌우"**의 실험 근거. 우리 coverage↑가 *간접적으로* R_ct↓를 의미(접촉면적↑)함을 보강.
- **⑥ AM 균열 vs 압력(coarse 저압 심함)**: 우리 DEM AM_P 파괴·Auerbach의 frame[4] — 단 driver가 *사이클 불균일전류*(우리 *압밀응력*과 다름) → Kang/Lee와 같은 "다결정 2차입자 깨짐" 계보로 기록(직접 흡수보다 *방향 검증*).

**frame[4] 앵커가 되는 숫자(요약)**: CAM utilization 표(Table 1), tortuosity 1.84/1.21, porosity 11.3/4.4 %, BET 6.02/9.24, retention@100cyc×3압력, R_ct 17.3/9.9 Ω, R_SSE/NCM 2 MPa +545/+34 Ω, 1st-cyc 용량 우위 +18/+20/+22 mAh/g.

---

## C. frame[4] 위치 (experimental anchor) ★

> **실험(+같은-DEM) → 앵커.** 이 논문은 *경쟁 시뮬*이 아니라 **우리 transport/coverage 측의 외부 검증**(Bazzoun=σ-솔버 교차검증, Lee=실험 앵커, Bielefeld=구조-모델링 peer 와 같은 부류). DEM이 있으나 *우리 솔버(σ)를 대체하지 않음* — utilization/packing까지만(σ는 실험).

- **실험→앵커가 되는 부분**:
  - **CAM utilization(DEM)** = 우리 coverage/contact의 *같은 코드계열* 독립 산출 → frame[4] **추세·개념** 교차검증(절대 % 아님).
  - **tortuosity·porosity·BET·R_ct·retention** = **실측** → 우리 τ/coverage/σ 예측이 향하는 *방향*의 실험 앵커. 특히 **retention×3압력 = B6 작동압 축의 정량 데이터**.
- **우리 시뮬이 *추가*하는 것 (그들이 비운 칸 = 우리 novelty)**:
  - ★ **명시적 σ 삼중항**(Kirchhoff/Holm σ_i/σ_e/σ_thermal) — 그들은 σ를 *안 풀고* 실험 측정. 우리는 **microstructure→σ를 *예측***(그들이 *측정만* 한 것을). ⇒ "**우리 DEM이 그들이 tailor한 microstructure→contact→σ를 사전 예측한다**"가 정확한 positioning.
  - ★ **Heckel·E_SE·압밀 정량**(그들 미공개), **MPM 소성 SHAPE morphology·void-fill·변형장**(그들 rigid-sphere), **Stage-E 소성 접촉면적**(그들 단순 overlap 임계), **σ 스케일링 법칙**(LOOCV 0.90–0.975).
- **transferability caveat(전사 한계)**:
  - ⚠ **DEM 재료 파라미터(E_SE·ν·σ_y) 미공개** → 그들 utilization 절대값을 우리 E_eff 1.35 모델에 직접 대입 불가(추세만). 그들 Hertzian(항복 없음) = 우리 hooke/hysteresis와 같은 탄성계열이나 *연화 정도 모름*.
  - ⚠ **CAM utilization % ≠ coverage %**(분모 다름: 입자수 vs 표면면적) → 동일시 금지, 개념/추세 대응.
  - ⚠ **SE≈CAM 크기**(fine SE ~1 µm ≈ NCM811 1–5 µm) — 우리 **12:4:1**(SE≪CAM)과 *입경비 다름* → packing/Furnas 맥락 절대전이 주의(그들 fine은 SE를 CAM과 *비슷한 크기*로 만들어 *덮음*을 노린 것; 우리는 SE를 *훨씬 작게* 해 *틈을 채움*). 둘 다 "작은 SE가 좋다"지만 *기하 메커니즘이 약간 다름*(coverage vs interstice-fill).
  - ⚠ **porosity·tortuosity = FIB-SEM 실측**(우리 ε_sphere·네트워크 τ와 방법 다름) → 절대 동일시 금지, 추세.
  - ⚠ **균열 driver = 사이클 불균일전류**(우리 압밀 Auerbach과 다름) → AM_P 파괴는 *방향* 검증만.
  - ⚠ **σ_ionic 정량 미공개**(EIS R_ct/R_b는 Ω, 셀형상 σ 환산 본문 미제공) → Bazzoun/Minnmann/Lee처럼 *절대 σ 앵커*로는 약함; **utilization·τ·retention**이 주 앵커.

---

## 8. 적용 인사이트 (내 연구에 어떻게) ★

- ① **★★ CAM utilization(Table 1) = 우리 coverage의 같은-코드-계열 검증점**: 같은 LPSCl+NCM811·LAMMPS-granular DEM이 "fine@2 % overlap=100 % vs coarse=83 %"를 산출 → 우리 `coverage_AM_*_by_SE`·dead-AM이 "미세 SE→coverage↑"를 내는 방향을 독립 확인. **흡수**: 우리 coverage를 overlap-임계 스윕(Hertz↔Tabor)으로 리포트해 그들 0→10 % 곡선과 *형태* 대조. `docs/data/tailored_cathode_low_pressure.csv`.
- ② **★★ operating-pressure 메커니즘(B6) 확보**: "microstructure가 *저압에서만* 차이를 만든다"(retention 격차 +7.5→+35.2 %p, 압력↓→격차↑)는 우리가 *제조압(300 MPa)*만 갖고 부족했던 **작동압 인과**. → 우리 coverage/σ(제조)를 *작동압 retention의 예측 변수*로 연결("coverage↑→저압 percolation 유지→retention↑"). Doux 5 MPa·Lee 2 MPa·Minnmann 40 MPa 압력 클러스터에 **microstructure 의존축** 추가.
- ③ **★ tortuosity 1.84/1.21 = 우리 τ 실측 앵커**: NCM811+LPSCl *실측* τ(Minnmann NCM622 τ_ion 2.07과 같은 계열). fine 1.21=거의 ideal → 우리 fine-SE production 목표의 실측 하한.
- ④ **★ R_ct(17.3→9.9 Ω) → 계면 kinetics 칸(Kim2025·Kang2025와 합류)**: charge-transfer 저항은 우리 σ-솔버가 안 잡는 칸 → "계면 kinetics = microstructure(coverage)가 좌우"의 실험 근거(우리 coverage↑→접촉면적↑→R_ct↓ 간접). future 계면 축(structure-σ 우리 / kinetics Kim/Zhou / mechanics Kang).
- ⑤ **★ "고압=microstructure 무관, 저압=microstructure 결정" = frame[5] 분업의 응용 정당화**: 고압선 SE가 cavity를 채워(=우리 MPM void-fill가 메우는 물리) microstructure 무관, 저압선 초기 packing/coverage(=우리 DEM)가 결정 → **압력 영역에 따라 DEM(coverage)·MPM(void-fill) 기여가 갈린다**는 우리 분업의 실험적 응용 맥락.
- ⑥ **porosity 4.4 %(fine) < 우리 pure-SE 10 %**: roll-mix 미세분이 강체 floor 아래로 → 우리 "연화/소성이 floor를 깬다" 논증의 *또 다른 실측 대비*(단 방법·제조압 다름, 추세만).

---

## 9. 인용 가능 문장 (deck/paper용)

- "For our exact material system (Li₆PS₅Cl + NCM811), Zhou et al. (ACS Energy Lett. 2025) used LAMMPS granular DEM to show that fine-LPSC SE reaches ~100 % CAM utilization at a 2 % minimum-overlap criterion versus 83 % for coarse-LPSC — a direct same-code-family analog of our SE-on-CAM coverage / contact-network descriptor — and that this microstructural advantage translates into stable cycling at a low **operating** stack pressure of 2 MPa (85.6 % vs 63.3 % retention at 100 cycles)."
- "Zhou et al. quantify that the microstructure benefit grows as the operating pressure falls (capacity-retention gap +7.5 → +19.7 → +35.2 %p at 30 → 10 → 2 MPa), establishing that initial packing/coverage — the half our DEM owns — governs low-pressure cyclability, while at high pressure the SE simply fills the cavities (the void-fill flow our MPM models). This anchors our fabrication-vs-operating pressure distinction with a microstructure-dependence axis."
- "FIB-SEM gives a fine-LPSC tortuosity of 1.21 (vs 1.84 coarse) and pellet porosity of 4.4 % (vs 11.3 %) for NCM811/LPSCl composites — an experimental tortuosity/porosity anchor consistent with our 'finer SE → denser packing, lower tortuosity' modeling trend (note: their FIB-SEM convention differs from our material-conserving compaction porosity)."

---

## 10. 주의/한계 (over-claim 방지) ★ — 정직 목록

- ⚠ **DEM이 σ를 안 푼다**: 이 논문 LAMMPS DEM은 **CAM utilization + calendaring packing**만; **σ_ionic/σ_e는 실험 EIS**로 측정. tortuosity 1.84/1.21도 **FIB-SEM 실측**이지 DEM 산출 아님. ⇒ 우리 Kirchhoff/Holm σ 삼중항·Stage-E와 **σ 직접 수치비교 불가** — 비교 가능한 건 *utilization(coverage-analog)·packing·τ 추세*뿐 (Bielefeld2019와 같은 "percolation/utilization은 주되 σ는 미산출" 부류).
- ⚠ **rigid sphere + Hertzian CONTACT, 진짜 SHAPE 소성 없음**: "discrete spherical particles" 명시 + Hertzian(탄성) 접촉, 항복·소성 접촉법칙 미명시. ⇒ 우리와 **같은 강체-구 한계**(δ-overlap 프록시) — MPM이 메우는 morphology/void-fill는 그들도 없음. "그들 DEM이 소성 변형을 한다" 식 과장 금지.
- ⚠ **DEM 재료 파라미터(E_SE·ν·σ_y·μ·COR) 미공개**(본문): Hertzian이라 E·ν가 들어가나 수치 없음 → 우리 E_eff 1.35/항복캡과 **직접 비교 불가**, utilization은 *추세*로만.
- ⚠ **CAM utilization % ≠ 우리 coverage %**: 분모 다름(그들=AM *입자수* 접촉비율, 우리=AM *표면면적* 덮임 %). 개념틀(overlap-임계 접촉 충분성)은 같으나 **절대값 동일시 금지** — 추세/개념 대응.
- ⚠ **SE≈CAM 입경비**(fine SE ~1 µm ≈ NCM811 1–5 µm) ≠ 우리 **12:4:1**(SE≪CAM): 그들은 SE를 CAM과 *비슷한 크기*로 만들어 *덮음(coverage)* 노림; 우리는 SE를 *훨씬 작게* 해 *틈을 채움(interstice-fill)*. 둘 다 "작은 SE 좋다"지만 *기하 메커니즘이 다름* → Furnas/packing 절대전이 주의.
- ⚠ **porosity·tortuosity = FIB-SEM 실측**(SEM void / 3D 재구성) ≠ 우리 ε_sphere(압밀 material-conserving) / 네트워크 τ → 방법 다름, 절대 동일시 금지(추세만). **제조압 미공개**(작동 2/10/30 MPa는 *cycling* 압력) → porosity@P의 P칸 = n/a.
- ⚠ **σ_ionic 정량값 본문 미제공**: EIS는 R(Ω)·R_ct로만 제시, 셀형상 σ 환산 본문 없음 → Bazzoun(0.137 mS/cm)·Minnmann(0.17)·Lee(0.076)처럼 *절대 σ 앵커*로 쓰긴 약함. 주 앵커 = **utilization·τ·porosity·retention·R_ct**.
- ⚠ **균열 driver = 사이클 불균일전류·Li/Ni mixing**(우리 압밀 Auerbach 접촉응력과 다름) → AM_P 파괴는 *방향* 검증만(Kang2025·Lee2025와 같은 "다결정 2차입자 깨짐" 계보).
- ⚠ **Li-metal 음극**: full cell이 Li-metal — 음극 단락/Li 거동은 우리 *복합 양극* 범위 밖(Doux와 같은 주의). 가져올 것은 **양극 microstructure·utilization·τ·porosity·작동압-retention**.
- ⚠ **digitized vs stated**: porosity 11.3/4.4 %·tortuosity 1.84/1.21·BET 6.02/9.24·utilization 표·R_ct 17.3/9.9·retention·R_SSE/NCM ±545/+34·용량우위 +18/+20/+22·DRT 면적 +8/+26/+115 %는 **본문 stated**(신뢰). Nyquist R_b·voltage profile 세부는 TREND.

---

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
