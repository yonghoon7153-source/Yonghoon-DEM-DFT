# Lim 2025 (Small 21, 2410485) — Virtual Calendering Framework: 3D-재구성 양극으로 가상 캘린더링 검증 + 전극설계 최적화 ★★★ 우리 DEM+MPM 압축의 가장 직접적인 방법론적 형제 (reconstruct-then-compress vs 우리 predict-from-powder-then-compress)

**인용:** **Jaejin Lim**¹²†, Jihun Song³†, Kyung-Geun Kim³, Jin Kyo Koo⁴, **Hyobin Lee**², Dongyoon Kang¹²,
Young-Jun Kim⁴, Joonam Park⁵\*\*, **Yong Min Lee**¹²\*, "Validating the Virtual Calendering Process With
3D-Reconstructed Composite Electrode: An Optimization Framework for Electrode Design", *Small* **21** (2025)
2410485, DOI 10.1002/smll.202410485.  © 2025 The Authors (Wiley-VCH, **Open Access CC BY-NC**).  접수
2024-11-06, 수정 2025-01-27, 게재 2025-03-16 (정정 2026-03-31).
- ¹연세대 화학생명공학 + ²DGIST 에너지과학공학(Lim/H.Lee = **DTBL 디지털트윈 모델러**, 이용민 교신) + ³DGIST
  에너지과학공학연구센터(Song/K-G.Kim) + ⁴SKKU SAINT(Koo/Y-J.Kim) + ⁵**LG에너지솔루션** 과천 R&D(J.Park 공동교신).
  J.Lim·J.Song 공동 1저자.  지원: NRF RS-2021M3H4A1A02048529 + LG Energy Solution.

**연세대 DTBL(이용민) 그룹 논문** — `docs/literature_yonsei_dtbl_2026.md`에 추가.  이 그룹의 **"가상 캘린더링
(virtual calendering)" headline 논문**으로, **우리 DEM+MPM 압축(compaction)과 가장 직접적으로 1:1 대응**되는
방법론.  positioning(`docs/positioning_vs_geodict.md`)의 **top-down/reconstruction vs bottom-up/formation** 분류를
"같은 압축 시뮬 안에서도 출발상태가 토모그래피냐 분말이냐"로 한 단계 정밀화하는 핵심 사례.

⚠ **소재 = Li-ion NCM622 + 액체전해질(1.15 M LiPF₆ in EC/EMC) — 우리 LPSCl 황화물 ASSB가 아님.** 따라서 셀 절대값
(용량·과전압·σ_ion 절대치)은 전이 불가.  **전이되는 것은 METHOD**(가상 캘린더링 검증 + 밀도 sweep) — 우리 압축의
**직접 방법론적 형제**(method-sibling), 수송 절대값 앵커가 아님.  수치 앵커는 Bazzoun/Varkey/Minnmann/#266/#271이 담당.

---

## ★ 한 문장 결론 — 이게 무엇이고 우리에게 왜 결정적인가

**FIB-SEM 토모그래피로 압축 전(uncalendered, 2.3 g/cm³) 양극의 3D 구조를 디지털 트윈으로 재구성한 뒤, 그 구조를
탄성 대변형(elastic large-deformation, FVM) 모델로 가상 압축("virtual calendering")해 목표밀도 2.4–4.0 g/cm³(총
11개)로 만들고, porosity·ionic tortuosity·접촉면적·crack 구조의 변화를 실제 캘린더링(독립 재구성)과 직접 대조해
검증한 뒤, 어느 밀도가 최적인지를 P3D 전기화학 모델로 최적화한다.  결론: 3.4–3.6 g/cm³가 최적(전자전도·접착·적당한
응력의 균형); 과압축(3.8–4.0)은 pore/tortuosity 부족으로 rate를 오히려 악화, 균열도 급증.**

**★ 우리 hook (왜 이게 우리 압축과 가장 직접 비교되는가):**
이 논문의 **"가상 캘린더링" = 우리 DEM+MPM 압축(compaction)** 그 자체다.  출력이 1:1 대응한다:

| 그들의 "virtual calendering" 출력 | 우리 DEM+MPM 압축 출력 | 매핑 |
|---|---|---|
| porosity vs 밀도 (Fig 2b) | porosity vs P/조성 (DEM ε_sphere) | ✅ 1:1 |
| ionic tortuosity vs 밀도 (Fig 2d) | τ_Dijkstra / τ_Laplace,eff (DEM 접촉망) | ✅ 추세 1:1 (정의 다름) |
| 접촉면적(NCM-pore, NCM-CBD) vs 밀도 (Fig 2e,f) | coverage/contact-area (Stage-E Tabor) | ✅ 1:1 |
| crack 구조 (VMS>100/150 MPa, Fig 4) | Auerbach fracture (F/P_c, severe%) | ✅ 1:1 (큰 다결정 분쇄) |
| 전자전도 +130%, 접착 +199% (Fig S1) | σ_e (DEM Kirchhoff) | ✅ 추세 (절대값 X, 액체계) |

**그리고 가장 중요한 차이 — 출발상태(start state):**
- **그들 = reconstruct-then-compress (하향식 출발):** 압축 *전* 전극의 **FIB-SEM 토모그래피가 필요**.  실제
  uncalendered 전극을 측정해서 디지털 트윈을 만든 *뒤* 압축.
- **우리 = predict-from-powder-then-compress (상향식 출발):** **토모그래피 없이** DEM으로 분말을 packing해 출발
  구조를 *예측*한 뒤 MPM/DEM으로 압축.

⇒ **둘 다 "압축을 시뮬"하지만, 그들은 출발구조를 측정(reconstruct)하고 우리는 예측(predict)한다.** 이것이
`positioning_vs_geodict.md`의 top-down/bottom-up 분류를 **"압축 시뮬 안에서도" 한 단계 정밀화**: 같은 가상-캘린더링
패밀리 안에서 **우리가 더 상향식**(출발상태에 토모그래피 불필요).  그들이 LIGGGHTS·GeoDict·MPSP-DEM·Ngandjong DEM을
명시 인용 → **우리가 필드 표준 도구를 쓴다는 강력한 근거**(우리 도구 = 그들이 거명한 바로 그 도구군).

---

## 1. 배경 / 동기 (Introduction, p.1–2)

- **캘린더링(calendering, 압연 압축)은 LIB 전극 제조의 필수 단계** — 목표밀도 달성을 위한 기계적 압축.  슬러리
  코팅·건조 파라미터가 고정되면 **캘린더링이 체적에너지밀도(VED)와 전기화학 성능을 결정하는 가장 중요한 공정**.
- **밀도↑의 이중성:**
  - **이득:** 전극 구성요소(AM·도전재·바인더) 간 접촉면적↑ → bulk 비저항↓(전자전도 경로↑), 바인더 접촉↑ → 기계적
    강건성·장기신뢰성↑.
  - **폐해:** pore 부피분율↓ → Li⁺ 확산·이동 방해; pore 연결성↓ → **tortuosity↑ → rate 급락**; 국소응력이 AM의
    압축강도를 초과 → **균열(crack) 형성** → 전기화학 비활성 입자 + 표면적↑(전해질 분해) → 용량↓·계면저항↑.
  - ⇒ **밀도는 rate뿐 아니라 장기신뢰성을 위해 신중히 최적화**해야 함.
- **선행 연구의 한계:** 밀도↔성능을 *실험적 상관*으로만 보거나(porosity·pore size·tortuosity·접촉면적·crack을
  실험으로 정량하기 어려움), 또는 시뮬을 쓰되 **완전 구형 입자 가정**으로 표면 형상의 영향을 반영 못 함.  핵심 주장:
  **신뢰할 수 있는 모델링 프레임워크 — 실제 미세구조 변화를 반영하고 견고한 검증 방법을 확립 — 이 최우선**이다.
  그런 프레임 없이는 계산 예측이 실험과 어긋난다.
- **선행 도구 거명(★ 우리 도구군):** 가상 전극 생성·압축을 위해 **LAMMPS, LIGGGHTS, MATBOX, GeoDict, EDEM**이
  보고됨.  **Nikpour et al. = MPSP**(multiphase smoothed-particle DEM, 비구형 입자분포 + 압축 전후 입자 상호작용);
  **Ngandjong et al. = CGMD**(coarse-grain MD, 전기화학 임피던스·방전용량·lithiation 시뮬); **Lenze et al. = P2D**
  (계산효율적, 단 형상 파라미터를 전기화학 데이터에만 피팅 → over/under-estimation 위험).  → **본 연구는 형상·
  전기화학을 둘 다 반영하는 검증된 프레임을 목표.**
- **본 연구(명시):** **bimodal NCM622** 양극(loading 19.8 mg/cm², AM **96 wt%**)의 압축 전/후 고해상 FIB-SEM
  토모그래피 → 디지털 트윈 재구성 → **가상 캘린더링으로 다양한 밀도(2.4–4.0) 시뮬** → 실제 캘린더링(3.6 g/cm³
  독립 재구성)과 대조 검증 → porosity·tortuosity·접촉면적·crack 분석 → P3D 전기화학 모델로 최적 밀도 도출.

---

## 2. 소재 & 전극 제작 (Experimental Section, p.9–10)

### 2.1 양극(cathode)
- **AM = bimodal LiNi₀.₆Co₀.₂Mn₀.₂O₂ (NCM622)**, 순도 99.9% (L&F, Korea).  **두 입경 혼합:**
  - **큰 입자(large) = 평균 14 µm** (= 우리 **AM_P** 대응, 큰 다결정 2차입자)
  - **작은 입자(small) = 3 µm** (= 우리 **AM_S** 대응)
  - **혼합비 large:small = 8:2 (wt)** — ★ 우리 a9_50 P:S와 같은 변수 축(큰:작은 = poly:single).
- **도전재/바인더:** Super P (Imerys) + PVDF (KF1300, Kureha) → NCM622 : Super P : PVDF = **96 : 2 : 2 wt%**,
  NMP 용매.  → CBD(carbon binder domain) = Super P + PVDF.
- **제작:** 알루미늄 호일(15 µm) 위 닥터블레이드 코팅 → 120 °C 2 h 건조 → **목표밀도 11개로 캘린더링**(2.3 g/cm³
  uncalendered 출발 → 2.4/2.5/2.7/2.8/3.0/3.3/3.4/3.5/3.6/3.8/4.0).  **mass loading = 19.8 mg/cm² 고정**
  (= 면적용량 **3.42 mAh/cm²**).  캘린더링 제외 전 공정은 **드라이룸(dew point ≤ −60 °C)**.

### 2.2 음극·셀
- **음극 = 인조흑연(SCMR-AR, Showa Denko)** + Super P + Na-CMC + SBR (96.9:0.5:2.6 wt%), Cu 호일(10 µm).  음극
  loading 10.46 mg/cm² (4.26 mAh/cm²) → **N/P ≈ 1.1**.
- **셀 = 2032 코인셀(Gr‖NCM622 풀셀)**, PE 분리막(18 mm, 20 µm), **액체전해질 1.15 M LiPF₆ in EC/EMC(3:7 v/v)
  + 2 wt% FEC**, 120 µL.  Ar 글러브박스 조립.

### 2.3 측정
- **전자전도(σ_e):** 전극저항측정기(RM2610, HIOKI), 0–1 mA / 0–0.5 V.
- **접착(adhesion/peel):** SAICAS(표면계면절삭), BN 블레이드(폭 1 mm), 수평속도 2 µm/s, 5회 측정.
- **전기화학:** 형성 1사이클 + 안정화 3사이클(0.1C CC, 4.3 V 컷오프).  Rate: 0.1C→10C(0.1/0.2/0.5/1/2/3/5/7/10C,
  복귀 0.1C), 충전 0.2C 고정.  Cycle: 0.5C CC/CV 충전 + 0.5C CC 방전, 3.0–4.3 V, 25 °C.

---

## 3. 가상 캘린더링 METHOD — 핵심 (Experimental Section, p.10–11 + SI Table S1/S3)

★ **이 절이 우리 압축과의 비교 핵심.** 3단계: (a) 재구성 → (b) 가상 압축 → (c) 검증.

### 3.1 (a) FIB-SEM 토모그래피 → 3D 디지털 트윈 재구성
- **장비:** FIB-SEM (Crossbeam 550, ZEISS).
- **uncalendered(2.3 g/cm³):** voxel/pixel 37.22 nm, FIB milling 간격 32.5 nm, image 2048×1536×1080, 도메인
  ≈ **30 × 90 × 40 µm³** (= a×b×c).  단면 수: SI Table S1 **1,080** / 본문 Experimental **1,500** (출처별 상이 — 표기 그대로).
- **calendered(3.6 g/cm³):** voxel 42.94 nm, 동일 milling 간격, image 2048×1536×1080.  도메인: SI Table S1
  **30 × 60 × 40 µm³** / 본문 **≈ 33 × 60 × 56 µm³** (출처별 상이).  단면 수 SI **932** / 본문 **1,160**.
- **이미지 처리(GeoDict, Math2Market):** FFT 필터 + nonlocal means 필터 → trilinear scaling으로 z방향 보정 →
  **gray-value threshold + watershed** 분할 → 3상(pore / NCM622 / CBD) segmentation → 3D 디지털 트윈.
- **결과(★ digital twin 검증):** **부피분율 디지털트윈 vs 이론계산 편차 모두 <2%p**(Fig 1d,e):
  - **uncalendered(Fig 1d):** NCM622 이론 46.2 / 트윈 45.8(편차 0.4), CBD 5.0/5.1(−0.1), pore 48.8/49.0(−0.3).
  - **calendered 3.6(Fig 1e):** NCM622 69.0/69.8(편차 −0.8), CBD 7.8/8.4(−0.6), pore 23.3/21.8(+1.5).
  - **REV(대표체적, representative element volume) = 14.1(uncal) / 13.9(cal)** ≫ 신뢰분석 최소권장 5 → 견고.
    (도메인 두께 85 µm uncal → 55 µm cal 3.6.)

### 3.2 (b) 가상 캘린더링 = 탄성 대변형 압축 시뮬 (GeoDict ElastoDict, FVM)
- **방법(명시):** 재구성한 **uncalendered 구조를 출발점**으로 → **ElastoDict 모듈(GeoDict 2023) = 유한체적법(FVM)
  기반 strain-controlled 압축 시뮬**.  **모든 상을 선형 탄성(linearly elastic)으로 가정** + **두께(y)방향 단축압축
  (uniaxial compression)**.  대칭 경계조건, 기계하중은 strain-controlled(목표밀도까지 변형 후 변형률/두께 기준 종료).
- **체적보존 리샘플링:** 목표 strain에서 선형탄성 모델로 변위장/요소장 계산 → voxel 재배치 → **총부피 유지 +
  고체부피 손실 없음**(SI ref 58, Kabel resampling).  → 작은 mechanical property를 가진 이웃 voxel을 강한 voxel이
  밀어내거나 차지(실제 캘린더링과 유사).
- **재료 물성(SI Table S4):** **E_NCM622 = 2.61 GPa**(ref 4 = Song 2023, AEM = 같은 그룹) / E_CBD = 1.55 / E_Al
  = 68.96; ν 모두 0.30(Al 0.33).  ⚠ **E_NCM622 = 2.61 GPa는 "전극 effective" 또는 2차입자 유효값** — 우리 NCM
  bulk(~140 GPa rigid AM)과 다른 scale(2차입자 다공·결합 포함 유효탄성).
- **11개 밀도 모두**(2.4/2.5/2.7/2.8/3.0/3.3/3.4/3.5/3.6/3.8/4.0) 가상 압축.
- ⚠ **한계(명시):** strain-controlled 탄성압축이라 **spring-back(스프링백) 미반영** → 가상 압축한 3.6 표면이 실제
  재구성 3.6보다 "더 평평"(top surface too flat).  실제 캘린더링의 spring-back은 못 잡음.  → **우리 MPM도 같은
  gap**(`positioning_vs_geodict.md` #285 spring-back 미구현).

### 3.3 (c) 검증 — 가상 3.6 vs 실제 재구성 3.6 (Fig 1d,e / Fig 2 / Fig S5)
- **uncalendered(2.3)를 가상 압축해 3.6으로 만든 구조 ↔ 실제 3.6 캘린더링을 독립 FIB-SEM 재구성한 구조**를 대조.
- **핵심 형상 파라미터 일치(p.4):**
  - **porosity:** 가상 vs 실제 **<10% 오차**(Fig 2b — 이론값과도 <10%).
  - **전자전도(effective electronic conductivity):** 가상 **17.9% vs 실제 18.7%**(상대오차 ~4%) → 1.8 S/m vs
    1.9 S/m (Fig S5; 본문은 가상 17.9%·실제 18.7%로 표기 = 어떤 기준 백분율).  실험 대조 평균 상대오차 **≈3.5%**(Fig 2c).
  - **ionic tortuosity:** 가상 **2.5 vs 실제 2.6**.
  - **NCM 비표면적:** 가상 **7.04×10⁵ vs 실제 6.98×10⁵ m²/m³**.
  - **NCM-CBD 비접촉면적:** 가상 **8.74×10⁵ vs 실제 8.63×10⁵ m²/m³**.
  - ⇒ **세 파라미터 모두 가상≈실제** → 가상 캘린더링이 신뢰할 수 있음을 입증(frame[4] 식 검증).

### 3.4 분석 도구(SI)
- **유효확산/tortuosity:** GeoDict **DiffuDict** — D_e,eff 계산(Dirichlet, ΔC=1 mol/m³, x–z 법선면), 전해질
  intrinsic D_e(1.15 M LiPF₆ in EC/EMC) 입력.  **식(1) τ_e = ε_e·D_e/D_e,eff** = MacMullin-type(우리 측지 τ와 정의 다름).
- **유효전자전도:** GeoDict **ConductoDict**(ΔV=1 V, Ohm 법칙, FVM).
- **PNM(pore network model):** MATLAB + MathWorks watershed → pore를 ball, 연결을 stick으로 → 등가 pore 반경,
  pore 배위수(coordination number), pore connectivity matrix(대역폭 bandwidth) 정량(SI Fig S9/S10).
- **crack 추출:** 이미지 처리 프로토콜(SI Fig S11)로 실제 캘린더링 3.6 구조에서 cracked volume 추출.
- **P3D 전기화학 모델:** COMSOL 6.1, Doyle-Newman, **pseudo-3D**(x·y 실제 차원 + r 1D)로 Al/cathode/separator/
  anode/Cu 5층(SI Fig S12, Table S2/S3/S4).  MUMPS 직접솔버, 5C 방전, time step 5 s.

---

## 4. 결과 — 미세구조 변화 vs 밀도 (Fig 2, p.4–6)

### 4.1 porosity vs 밀도 (Fig 2b)
- **밀도↑ → porosity↓ 단조:** 2.3 g/cm³ ≈ **49%**(=초기) → 4.0 g/cm³ ≈ **9–10%**.  가상(시뮬) vs 이론값 매우
  근접(<10% 오차) → 검증.  (디지털화: 2.3→49, 2.4→46, 2.5→44, 2.7→39, 2.8→35, 3.0→31, 3.3→25, 3.4→23, 3.5→20,
  3.6→19, 3.8→14, 4.0→10 % 정도; TREND only.)

### 4.2 전자전도 vs 밀도 (Fig 2c / Fig S1a)
- **밀도↑ → σ_e↑ 단조:** uncalendered 2.3 → 4.0 g/cm³에서 **약 +130%**.  가상 시뮬 ↔ 실측 평균 상대오차 **≈3.5%**.
  고밀도일수록 고체가 조밀 접촉 → 전자경로↑.  (Fig 2c: ~0.9 → ~2.2 S/m.)

### 4.3 접착(adhesion) vs 밀도 (Fig S1b)
- **밀도↑ → 접착강도↑, σ_e보다 더 크게:** 2.3 → 4.0에서 **약 +199%**.  바인더 접촉↑ → 기계적 강건성·장기신뢰성↑.

### 4.4 ionic tortuosity vs 밀도 (Fig 2d)
- **밀도↑ → tortuosity↑:** 특히 **3.5 → 3.6 g/cm³를 넘어 급증**(Fig 2d, 가상 ↔ 실제 거의 동일).  pore가 작아지고
  연결 끊김 → Li⁺ 경로 우회.  ⇒ **3.8/4.0의 rate 저하 원인 = 이온수송 한계(tortuosity↑), 전자전도 부족이 아님.**

### 4.5 비표면적(NCM-pore 접촉) vs 밀도 (Fig 2e)
- **밀도↑ → NCM 비표면적↓**, 단 **3.3 g/cm³ 이상에서 ≈6.90×10⁵ m²/m³로 포화(거의 일정)** — pore가 일정점 이후
  downsizing되면서도 AM-pore 접촉 유지.

### 4.6 비접촉면적(NCM-CBD) vs 밀도 (Fig 2f)
- **밀도↑ → NCM-CBD 접촉면적↑**, 단 **복잡 거동:** 3.3–3.6은 거의 일정 → **3.8에서 급증(sharp)**.  3.8 이상에서
  AM-CBD 신접촉 형성 + pore 부피↓ + AM 재배열(Fig S6) = 중간조밀(≤3.3) → 고밀집(>3.8) 구조전이.

---

## 5. 결과 — pore 구조 정량(PNM) (Fig 3, p.6–7)

- **등가 pore 반경↓ + 연결 stick↓:** 밀도↑ → 붉은 ball(큰 pore)↓.  평균 등가반경 **3.8 g/cm³가 3.4 g/cm³보다
  25% 작음**(Fig 3b: 3.4→0.84 / 3.6→0.67 / 3.8→0.62 µm 정도).
- **pore 배위수↓:** 밀도 0.2 g/cm³↑마다 평균 배위수 0.5↓(Fig 3c: 3.4→4.1 / 3.6→3.5 / 3.8→3.1 정도).
- **connectivity matrix 대역폭(bandwidth)↑(narrower diagonal):** 밀도↑ → pore 수·최대 인덱스↑(큰 pore가 작은
  것으로 쪼개짐) → 대각선 좁아짐 = **마이크로 pore가 나노 pore로 쪼개져 이온경로 더 우회·차단**(Fig 3d, S10).
  높은 밀도 = pore connectivity 표준편차 작음(narrower) = 연결 좁음.

---

## 6. 결과 — 응력·crack 분석 (Fig 4, p.6, 8)

★ **이 절 = 우리 Auerbach fracture와 직접 대응.**

### 6.1 von Mises stress(VMS) 분포 (Fig 4a)
- **밀도↑ → AM 내부 VMS↑**, 특히 입자끼리 압축되는 접촉점 + 입자 *표면뿐 아니라 내부*에서도 고VMS → **harsh
  캘린더링 조건에서 입자 내부 균열 가능**.
- **NCM 2차입자 최대항복강도 = 100–150 MPa**(보고값, ref 25/52) → **VMS>100–150 MPa 영역 = crackable volume**으로
  정의해 균열 잠재성 정량.

### 6.2 crackable volume vs 밀도 (Fig 4b)
- **VMS>100 MPa 체적%:** 저밀도(2.8/3.0)는 ~**1.5–5.0 vol%** → **3.4/3.6에서 ~10 vol%로 지수적 증가** → 4.0에서
  ~14%.  VMS>150 MPa도 동반 상승(~8% @4.0).
- ⇒ **균열은 3.4–3.6 g/cm³ 넘어 지수 급증** → 시뮬이 실험(>3.5 g/cm³ cycle 성능 악화, Fig 1b)을 뒷받침.

### 6.3 crackable(가상) vs cracked(실제) 대조 (Fig 4c,d)
- **실제 3.6 캘린더링 구조에서 추출한 cracked volume**(SI Fig S11 프로토콜) ↔ **가상 압축 3.6의 crackable
  volume(VMS>150 MPa)**.  두 3D 렌더링의 **크기·분포가 매우 유사**(Fig 4c) + 두께방향 normalized 체적% 곡선도
  유사 변동(Fig 4d).  ⇒ **VMS 기반 분석이 신뢰할 수 있음** + 균열 진단에 유용.
- ⚠ **정밀 주의(명시):** crackable(잠재) ≠ cracked(실제) — 같은 물리량이 아님.  정확한 cracked 검출은 **failure/
  interface 물성을 포함하는 고급 모델**(요소가 어디서 fracture point 도달 후 응력 drop되는지 식별)이 필요 →
  **future work**.  → **우리 Auerbach(F/P_c 임계 + severe%)는 바로 이 "criterion-based fracture"** = 그들이
  future work로 남긴 부분을 우리는 이미 보유(frame[5] 우리 강점).

---

## 7. 결과 — 전기화학 검증 + 최적 밀도 (Fig 1 / Fig 5, p.3–4, 7–8)

### 7.1 rate / cycle 실험 (Fig 1a,b)
- **rate(Fig 1a):** **저밀도(<3.0 g/cm³)는 1C에서 용량 나쁨** — uncalendered 전극은 전자접촉 불충분(특히 고율).
  **고밀도 3.8/4.0은 5C에서 3.6보다 오히려 낮음** — 전자전도 향상으로 설명 안 됨 → **pore 부피·연결 부족 = 이온수송
  한계**.
- **cycle(Fig 1b):** **2.8 g/cm³는 초기용량 절반 이하로 급락, 300사이클 못 버팀**(접착 부족 → 접촉손실).  **3.0
  g/cm³ = 400사이클 80%↑ 벤치마크**.  **3.4 g/cm³ = 400사이클 91.9% 최고 retention**, 단 **3.4 넘으면 retention↓**
  (균열↑ → 유기용매·Li 소모 → cathode-전해질 계면상 → 용량↓).
- ⇒ **3.0 = cycle 최소 기준, 3.4–3.6 = 최적**(접착·전자전도·적당한 VMS 균형).

### 7.2 P3D 전기화학 모델 검증 (Fig 5)
- **5C 방전용량 시뮬 ↔ 실험 상대오차 6.1%**(Fig 5a) — 가상 캘린더링이 뽑은 형상·전기화학 파라미터(tortuosity·
  porosity·σ_e·σ_ion·D_e,eff)가 신뢰할 수 있음.
- **방전말 lithiation 상태(SOL, Fig 5b/S14/S15):** **3.6 g/cm³ = 전 두께에서 SOL 27%↑ 유지**(균일); **3.4는 27%
  미달**(σ_e 부족); **3.8은 SOL 급변**(두께방향 심한 분극 = tortuosity↑·pore↓·연결끊김).
- **과전압/전해질 Li⁺ 농도구배/전위(Fig 5c):** 저밀도(<2.8)는 과전압 0.9 V↑(저σ_e ohmic), 밀도↑로 3.5까지 감소 →
  **3.6 넘으면 다시 증가**(고밀도 전해질 농도구배↑).  → 실험(Fig 1a)과 정합.

---

## 8. 결론 + future work (Conclusion + Fig 6, p.9)

- **밀도↔성능을 디지털트윈 가상 캘린더링으로 규명** — 2.4–4.0 g/cm³에서 실험+시뮬.  **최적 = 3.4–3.6 g/cm³**
  (고전자전도·고접착·충분한 이온수송·적당한 VMS).  ★ 이것이 **명시적 "최적 밀도 최적화 프레임워크"**.
- **future work(Fig 6 schematic):** 디지털트윈을 조성·분포·바인더 형상·표면개질·기능성 집전체·전극변형(crack
  전파·부피팽창)에 확장.  특히 **fracture point 식별 + 응력 drop 모델**(criterion-based) 개발 예정.
- **방법론적 의의:** 실제 FIB-SEM 재구성 구조 + 가상 캘린더링(실험 검증됨)으로 미세구조를 정량 → 신뢰성 높은
  시뮬 데이터 생성 패러다임.

---

## ★★★ 9. 우리 DEM+MPM 압축과 비교 (CENTERPIECE)

이 논문은 **우리 압축 모델과 가장 직접적으로 1:1 대응**되는 논문이다.  아래를 (A) 출력 1:1 → (B) 출발상태 distinction
→ (C) 검증방법론 평행 → (D) bimodal/crack → (E) 도구 → (F) 정직한 경계로 체계화.

### (A) "가상 캘린더링" = 우리 DEM+MPM 압축 — 출력 1:1 대응

| 그들 (Lim 2025, 가상 캘린더링, FVM 탄성압축) | 우리 (DEM+MPM 압축) | frame | 판정 |
|---|---|---|---|
| porosity vs 밀도 (49%→10%, Fig 2b) | porosity vs P/조성 (DEM ε_sphere, MPM 소성) | [5] 둘 다 | ✅ 1:1 (밀도축 ↔ 압력축) |
| ionic tortuosity vs 밀도 (Fig 2d, 3.5→3.6 급증) | τ_Dijkstra/τ_Laplace,eff (DEM 접촉망) | [5] DEM | ✅ 추세 1:1 (정의 다름) |
| 접촉면적 NCM-pore/NCM-CBD (Fig 2e,f) | coverage/contact-area (Stage-E Tabor+B3) | [5] DEM | ✅ 1:1 |
| crack: VMS>100/150 MPa crackable% (Fig 4) | Auerbach fracture (F/P_c, severe%) | [5] DEM | ✅ 1:1 (큰 다결정 분쇄) |
| von Mises stress 장 (Fig 4a) | MPM 응력장 (von Mises J2) | [5] MPM | ✅ 1:1 (MPM이 정확히 이걸 출력) |
| 전자전도 +130% vs 밀도 (Fig 2c) | σ_e (DEM Kirchhoff) | [5] DEM | ⚠ 추세만 (액체계 절대값 X) |
| pore 등가반경·배위수·connectivity (PNM, Fig 3) | pore network(우리 미구현) / porosity·τ | — | ⚠ 부분 (PNM은 우리 미보유 분석) |

**⇒ 그들의 "virtual calendering 출력 5종(porosity/τ/접촉면적/crack/응력)"이 우리 DEM+MPM 압축 출력과 거의 완전
1:1.** 특히 **VMS 응력장 = 우리 MPM이 출력하는 바로 그것**, **crack = 우리 Auerbach**, **τ/접촉면적/porosity = 우리
DEM**.  frame[5] 분업(DEM=transport, MPM=mechanics)이 이 논문 한 편에 그대로 들어있다(그들은 한 도구 GeoDict로,
우리는 DEM+MPM 둘로).

### (B) ★ 출발상태 distinction — reconstruct-then-compress vs predict-from-powder-then-compress

`positioning_vs_geodict.md`의 top-down/bottom-up 분류를 **"같은 압축 시뮬 안에서도" 한 단계 정밀화**하는 핵심.

| | Lim 2025 (그들) | 우리 DEM+MPM |
|---|---|---|
| **출발구조 생성** | **FIB-SEM 토모그래피 재구성** (실제 uncalendered 2.3 측정) | **DEM packing 예측** (분말→구조, 토모그래피 불요) |
| 분류 (Choi 2024 E.Chem) | **top-down / reconstruction** | **bottom-up / formation** |
| 압축 시뮬 | ElastoDict FVM 탄성 대변형 | MPM(소성 J2) + DEM(hooke/hysteresis) |
| 압축 후 출력 | porosity/τ/접촉/crack/VMS | porosity/τ/coverage/Auerbach/응력 (= 동일) |
| 출발상태에 필요한 것 | **실제 전극의 FIB-SEM** (1,500단면, 장비) | **설계 입력만**(압력·조성·입경) |

**★ 정밀한 한 문장:** 둘 다 "압축을 시뮬"한다.  그러나 **그들은 출발구조를 측정(reconstruct)하고, 우리는 예측
(predict)한다.** 같은 가상-캘린더링 패밀리 안에서 **우리가 더 상향식** — 출발상태에 토모그래피가 불필요하므로
**아직 만들지 않은(미측정) 설계점도** 압축 시뮬 가능(predictive, design-side).  그들의 프레임은 *측정된 전극이
이미 있어야* 가상 압축이 가능(reconstruct가 선행).

→ 이것은 `positioning_vs_geodict.md`의 "GeoDict=구조-given 특성화 ↔ 우리=공정에서 구조-예측"을 **"가상 캘린더링"
이라는 가장 직접적인 비교대상에서 재확인**: 그들의 가상 캘린더링조차 **출발구조는 GeoDict가 만들지 못해 FIB-SEM으로
넣어줘야** 하고(top-down 출발), 압축만 ElastoDict로 시뮬한다.  우리는 출발구조(DEM packing)부터 압축(MPM/DEM)까지
**전부 bottom-up**.  ⇒ positioning의 "even within simulate-compaction, we are more bottom-up"의 **교과서적 사례**.

### (C) 검증 방법론 평행 — 같은 frame[4] 철학

| | Lim 2025 | 우리 |
|---|---|---|
| 가상 압축 ↔ 실제 대조 | 가상 3.6 vs 실제 재구성 3.6 (porosity/σ_e/τ/접촉 <10%·~3.5% 오차) | DEM/MPM porosity·thickness·coverage vs LIGGGHTS·실험 (real_14 15.6/30.28; Minnmann 10%) |
| 검증 앵커 | 실험(FIB-SEM 재구성 + 전기화학) | 실험(Minnmann/Cronau/#266 He) — **모델끼리 교차피팅 금지(frame[4])** |
| 밀도/압력 sweep 검증 | 11개 밀도(2.4–4.0) | 다압력 Heckel(100/300/600) + 조성 sweep |
| 과압축 caveat | **3.8–4.0 rate 악화(tortuosity↑·pore↓)** | **우리 over-compression caveat**(ε_sphere 음수 cap, Stage-E min-cap) |

**⇒ 검증 철학이 동일:** 시뮬을 실험으로 검증하고, 밀도/압력 sweep으로 추세를 잡고, **과압축의 성능역전을 명시**.
그들의 "3.8–4.0 과캘린더링 rate-loss(이온수송 한계)" = 우리 "과압축 caveat"(ε_sphere over-compression cap + 고밀도
constriction).  우리 a9_50 sweep에서 **P:S 6:4 넘어 σ_ionic 붕괴(0.0506→0.0066, 7.7×↓)** = 그들의 "최적 밀도
넘으면 tortuosity↑로 rate 악화"의 조성판(packing이 한계 넘으면 SE 경로 압박).

### (D) bimodal + crack ↔ 우리 AM_P/AM_S + Auerbach

- **bimodal NCM622(large 14 µm : small 3 µm = 8:2) ↔ 우리 AM_P(6 µm) : AM_S(2 µm).** 같은 "큰:작은 입자 혼합"
  변수.  우리 a9_50 P:S sweep이 *이 변수를 직접 변화*시킨 것(그들은 8:2 고정이지만 입자 bimodal성은 동일).
- **crack(VMS>100–150 MPa, 큰 입자 내부 균열) ↔ 우리 Auerbach fracture(큰 다결정 AM_P 분쇄).** 우리 a9_50에서
  **severe fracture 63% @p10**(전부 큰 AM_P → 하중 독점 → 분쇄), 작은 AM_S는 내내 intact(#285 단결정 균열억제).
  그들도 **고밀도서 큰 입자 내부 VMS 초과 → 균열 → cycle 악화**.  **둘 다 "큰 다결정이 압축에서 깨진다"는 동일 물리.**
- **NCM 항복강도 100–150 MPa** = crackable 임계 → 우리 Tabor/Stage-E의 **경도 H·항복 기반 접촉area cap**과 같은
  재료상수 축(우리는 H로 contact-area cap, 그들은 VMS>H_y로 crackable).

### (E) 도구(toolchain) — "우리는 필드 표준 도구를 쓴다"

- 그들이 **명시 인용**: **LAMMPS, LIGGGHTS, MATBOX, GeoDict, EDEM, MPSP-DEM(Nikpour), Ngandjong CGMD, Lenze P2D.**
- **우리 도구 = LIGGGHTS(DEM) + Taichi/scipy(MPM·Kirchhoff)** → **그들이 거명한 바로 그 가상-전극 도구군에 우리가
  속함**.  특히 **LIGGGHTS는 그들 인용 리스트의 핵심 DEM 엔진 = 우리 DEM 엔진과 동일** → "우리가 비표준 도구를
  쓴다"는 reviewer 반론에 직접 반박.  MPSP-DEM(비구형 입자)·Ngandjong(전기화학 결합)은 우리가 향후 비교/벤치마크할
  레퍼런스.

### (F) 정직하게 — 전이 경계 (over-claim 금지)

- ⚠ **Li-ion NCM622 + 액체전해질 ≠ 우리 LPSCl 황화물 ASSB.** 셀 절대값(용량·과전압·σ_ion 절대치·tortuosity τ
  MacMullin)은 **전이 불가**.  이 논문은 **방법론적 형제(method-sibling)**이지 수송 절대값 앵커가 아니다(앵커는
  Bazzoun/Varkey/Minnmann/#266/#271).
- ⚠ **모든 상 선형 탄성 가정(ElastoDict) — 소성 SHAPE 변화 없음.** 입자 형상은 voxel resampling(체적보존)으로
  재배치되지만 **진짜 소성흐름(plastic flow)이 아님** → **우리 DEM(rigid sphere+overlap)과 같은 한계**.  우리
  **MPM(소성 J2)이 바로 이 gap을 메움**(void-fill 소성흐름·morphology).  즉 그들의 압축 시뮬은 우리 DEM-side에
  가깝고(탄성/체적보존), **소성 morphology는 우리 MPM이 더 물리적**.
- ⚠ **τ(ionic tortuosity)는 MacMullin-type(식 1 ε_e·D_e/D_e,eff) — 우리 측지 τ_Dijkstra(~1.2–2)와 정의 다름.**
  추세(밀도↑→τ↑, 3.5→3.6 급증)만 비교, 절대값 비교 불가.  (그들 가상 2.5 / 실제 2.6은 그들 정의 내 값.)
- ⚠ **spring-back 미반영(둘 다).** 그들 ElastoDict strain-controlled = spring-back 없음(가상 3.6 표면 too flat).
  우리 MPM도 spring-back 미구현(#285 future-work).  → **공통 gap**, 우리만의 약점 아님.
- ⚠ **digital twin REV 14 ≫ 5 = 견고 / 부피분율 편차 <2%p** — 그들의 재구성 품질이 매우 높음(우리는 토모그래피
  재구성을 안 하므로 이 검증은 그들 강점, 우리는 packing-predict로 우회).
- ✅ **그러나 METHOD는 직접 전이:** 가상 캘린더링(압축 시뮬) + 밀도 sweep + 실험 검증 + 과압축 caveat + bimodal +
  crack = **우리 DEM+MPM 압축의 직접 방법론적 형제.** 우리가 "압축을 시뮬해 미세구조/수송/역학/파괴를 뽑고 실험으로
  검증한다"는 워크플로 전체가 이 논문에 (다른 화학계로) 그대로 있음 → **우리 방법론의 published precedent + frame[5]
  분업의 단일 논문 시연.**

### ★ 종합 한 줄 verdict

> **이 논문의 "가상 캘린더링"은 우리 DEM+MPM 압축 그 자체(출력 porosity/τ/접촉면적/crack/응력이 1:1)이며, 차이는
> 단 하나 — 그들은 출발구조를 FIB-SEM으로 측정(reconstruct-then-compress, top-down 출발)하고 우리는 분말에서
> 예측(predict-from-powder-then-compress, bottom-up 출발)한다.  Li-ion 액체계라 셀 절대값은 전이 불가하나, 가상
> 캘린더링 검증 방법론·밀도 sweep·과압축 caveat·bimodal·crack은 우리 압축의 직접 형제이고, 그들이 명시 인용한
> LIGGGHTS/GeoDict/MPSP-DEM = 우리 도구군 → 우리가 필드 표준 압축-시뮬을 하되 출발측에서 더 상향식(토모그래피 불요)
> 임을 입증하는 가장 직접적인 positioning 근거.**

---

## 10. 주요 figure 요약 (우리가 재사용할 것 중심)

| Figure | 내용 | 우리 재사용 |
|---|---|---|
| **Fig 1a,b** | rate(0.1–10C)·cycle(400) vs 밀도 11종 | 과압축 rate-loss(3.8/4.0<3.6) = 우리 over-compression caveat |
| **Fig 1c** | 캘린더링 schematic + uncal(2.3, 85µm)/cal(3.6, 55µm) 디지털트윈 + REV 14 | 압축 전후 구조 = 우리 압축 전후 |
| **Fig 1d,e** | 부피분율 트윈 vs 이론 (편차 <2%p) | digital twin 검증 품질(그들 강점, 우리는 packing-predict 우회) |
| **★ Fig 2** | porosity(b)/σ_e(c)/τ(d)/NCM-pore면적(e)/NCM-CBD면적(f) vs 밀도, 가상↔실제 | **출력 1:1 핵심** — porosity/τ/접촉면적 = 우리 DEM 출력 |
| **★ Fig 2a** | 가상 캘린더링 schematic (2.3→4.0 구조 9컷, reconstructed 3.6 강조) | reconstruct-then-compress 시각화 |
| **Fig 3** | PNM: pore 등가반경/배위수/connectivity matrix (3.4/3.6/3.8) | pore 정량(우리 미보유 PNM 분석 — 향후 후보) |
| **★ Fig 4a** | von Mises stress 장 (2.8→4.0) | **우리 MPM 응력장과 직접 대응** |
| **★ Fig 4b** | crackable volume%(VMS>100/150 MPa) vs 밀도 (3.4–3.6 지수급증) | **우리 Auerbach severe% vs 압축** |
| **Fig 4c,d** | crackable(가상) vs cracked(실제) 3D + 두께방향 % | criterion-based fracture = 우리 Auerbach(그들 future-work) |
| **Fig 5** | P3D 5C 방전 검증(오차 6.1%) + SOL/과전압/농도구배 vs 밀도 | 형상파라미터→전기화학 검증(우리 Phase 4 PyBaMM 연결 아이디어) |
| **Fig 6** | future-work schematic(crack전파·부피팽창·조성·바인더·표면개질…) | 디지털트윈 확장 로드맵(우리 Phase 2–5와 정합) |
| **SI Fig S1** | σ_e(+130%)/peel(+199%) vs 밀도 | σ_e 추세(절대값 X) |
| **SI Fig S5** | 가상 vs 재구성 porosity·σ_e 비교 | 검증 정량 |
| **SI Fig S6** | 밀도별 top-view 미세구조(3.3–4.0) | 3.8 구조전이(중간조밀→고밀집) |
| **SI Fig S7/S8** | 배위수 분포·평균 등가반경·pore 배위수 vs 밀도 | pore 정량 추세 |
| **SI Fig S11** | crack 추출 이미지 프로토콜 | 실제 cracked volume 추출법 |
| **SI Table S1** | FIB-SEM 조건(uncal 30×90×40µm/1500단면; cal 33×60×40µm/1160) | 재구성 메타 |
| **SI Table S4** | 모델물성(E_NCM 2.61 / E_CBD 1.55 / E_Al 68.96 GPa, ν 0.30) | 그들 탄성 입력(우리 E_eff와 scale 비교) |

---

## 11. 기술 미니용어 (이 논문 맥락)

- **Virtual calendering(가상 캘린더링):** 재구성한 압축-전 전극 구조를 압축 시뮬해 목표밀도 구조를 만드는 것.
  = 우리 "압축(compaction) 시뮬".  단 출발구조가 **토모그래피 재구성**(우리는 DEM packing).
- **Digital twin(디지털 트윈):** 실제 전극의 3D 구조를 토모그래피로 복제한 가상 구조.  (Choi 2024 E.Chem 분류로
  **top-down/reconstruction**; 설계-side 미연결이면 DTP, 연결이면 DTI.)
- **ElastoDict(GeoDict):** FVM 기반 선형탄성 대변형 압축 모듈.  strain-controlled, 체적보존 resampling.
- **DiffuDict/ConductoDict(GeoDict):** 유효확산/유효전자전도 FVM 솔버 = 우리 voxel_conductivity 상응(연속체).
- **PNM(pore network model):** pore=ball, 연결=stick.  등가반경·배위수·connectivity matrix(대역폭)로 pore구조 정량.
- **VMS(von Mises stress) crackable volume:** VMS가 NCM 항복강도(100–150 MPa) 초과하는 체적% = 균열 잠재.
  ≠ cracked(실제) — failure 물성 모델 필요.  우리 **Auerbach F/P_c**는 criterion-based 실파괴 분류(그들 future-work).
- **MacMullin-type tortuosity(식 1):** τ_e = ε_e·D_e/D_e,eff.  우리 측지 τ(경로 우회 비율)와 정의 다름 → 추세만 비교.
- **REV(representative element volume):** 도메인이 전체를 대표하기에 충분한 단위셀 배수.  14 ≫ 권장 5 = 견고.
- **P3D(pseudo-3D):** x·y는 실제 차원 + r은 1D 입자내 확산 → 계산효율 + 공간분해 전기화학.

---

## 12. DB / 데이터 노트

- **수치 앵커 추가 안 함(method-sibling):** Li-ion 액체 NCM622라 σ/porosity 절대값을 우리 LPSCl 앵커 CSV
  (`densification_porosity_db.csv`, `*_sigma_ionic.csv`)에 넣지 않음 — 화학계가 달라 **추세만** 유효.
- (필요시 별도 후보) porosity-vs-밀도 추세(49→10%, 11점, digitized TREND)나 crackable%-vs-밀도는 **method 검증
  레퍼런스**로만 인용; 우리 transport 회귀에는 미투입(유저 결정).
- **positioning 강화:** `positioning_vs_geodict.md`의 reconstruct vs predict distinction의 **가장 직접적 사례**로
  본 디제스트를 cross-link(단, 지시대로 positioning_vs_geodict.md 파일 자체는 수정하지 않음).
