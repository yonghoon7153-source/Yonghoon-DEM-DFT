# 연세대 Digital Twin Battery Lab (Yong Min Lee 그룹) — 2026 논문 트리아지 + 우리 모델 매핑

**출처:** 연구실 Publication 리스트 2026 (논문 #260–286, 총 27편).  이 그룹은 우리 DEM+MPM
프로젝트와 **같은 도메인**(digital-twin 미세구조 모델링 + dry-processed electrode + sulfide ASSB +
2D→3D 합성 + CBD/transport)에서 활동 → 직접 인사이트 소스.

**이 문서의 역할:** 27편을 (1) 우리 프로젝트 관련도로 등급화, (2) 테마로 묶고, (3) 각 논문의 핵심
인사이트 → **우리 DEM/MPM/transport/Phase1-5 로드맵 어디에 꽂히는지** 매핑.  ★★★=직접 우리 도메인
(PDF 받아 litdb 풀 디제스트 필수), ★★=강하게 관련, ★=주변부, ·=타 화학계(카탈로그만).

⚠ 웹 초록·검색으로 확인한 내용 기반 — 풀 디제스트(수치/그림/방법 전체)는 PDF 필요.  상위 논문은
PDF 받으면 `docs/lit_<author>2026_<topic>.md`로 litdb-curator 풀 디제스트 예정.

---

## ★★★ TIER-1 — 우리 방법론 그 자체 (digital-twin / 2D→3D / bimodal)

### #266 — Bimodal Composite Cathodes, Chemo-Mechanical Integrity & Kinetics for ASSB  ⭐최우선
ACS Energy Letters 11(2) (2026) 2103-2114 (Open Access, IF 17.5).  Hyeonseong Oh†, Uigyeong Jeong† … Yong Min Lee, … Yoon Seok Jung 공저.
DOI 10.1021/acsenergylett.5c03923.
- **핵심:** bimodal = **큰 polycrystalline + 작은 single-crystalline CAM** 블렌드 → 입자 패킹·porosity
  최적화 → **ionic tortuosity↓ → Li⁺ 전달↑**.  CAM 90 wt%에서 **P:S = 7:3** (poly:single) 조성이
  87.8% retention @200 cyc, unimodal 능가.
- **우리 모델 매핑 (DIRECT 실험 검증):**
  - **P:S 7:3 = 우리 production calibration point 그 자체** (CLAUDE.md "Production calibration (2D)…
    P:S 7:3").  이 논문이 7:3을 실험 최적으로 보고 → 우리 7:3 선택의 **독립 실험 앵커**.
  - **bimodal packing → tortuosity↓ → σ_ionic↑** = 우리 **Furnas dip** (frame[3], porosity-vs-AM% dip @
    AM 70-85wt%) + 우리 σ_ionic의 τ·CN 항을 **실험으로 직접 확증**.  "큰poly+작은single이 더 조밀"이
    우리 12:4:1 size ratio bimodal void-filling과 동일 물리.
  - large-poly = 우리 **AM_P**, small-single = 우리 **AM_S** (라벨 정의 일치).
  - **ACTION:** 우리 bimodal/dip/P:S-7:3 서사의 headline 실험 검증으로 인용.  87.8%@200cyc +
    tortuosity 데이터를 validation corpus에 추가 (PDF에서 수치 추출).

### #263 — Stochastic 3D Microstructures from 2D Images (polymeric separators)  ⭐Phase 4 청사진
Advanced Energy Materials 16(10) (2026) e70730 (Back Cover, IF 25.5).  Youyeong Shin†, Suhwan Kim† … Yong Min Lee.  DOI 10.1002/aenm.70730.
- **핵심:** 2D 이미지에서 구조 파라미터 추출 → **stochastic하게 3D 가상 미세구조 생성** → 전기화학
  성능 예측.  separator digital-twin.  핵심 구조 파라미터를 **독립적으로 변화** → 미세구조↔이온수송
  관계 규명 → 합리적 설계.  (phase-contrast nano-CT로 lamellae + 2D SEM로 sub-100nm fibril을
  stochastic 재구성 → 3D 통합.)
- **우리 모델 매핑 (= 우리 Phase 4-5 그 자체):**
  - **"예측 수치 → 2D 이미지 → 3D 미세구조"가 정확히 우리 Phase 4** (`scripts/extract_2d_microstructure.py
    synthesize_microstructure`의 targets-only 진입점).  이 논문이 **published blueprint**.
  - "구조 파라미터 독립 변화 → 수송 예측" = 우리 predictor(design knobs → metrics) + 합성 파이프라인.
  - 2D→3D stochastic 재구성 = 우리 z-stacking/layered 합성(Phase 5)에 직접 이식할 방법.
  - **ACTION:** 이들의 2D-param-추출 → stochastic-3D-생성 방법을 우리 synth와 비교; 우리 합성이 같은
    구조 파라미터(porosity, tortuosity, 입경분포)를 보존하는지 검증 프레임으로 채택.

### #271 — Unveiling Degradation of Sulfide Composite Cathodes, Digital-Twin: Dry vs Wet Binder  ⭐우리 도메인
Energy Storage Materials 86 (2026) 104930 (IF 19.3).  Seung-Bo Hong†, Hyobin Lee† … Yong Min Lee, Dong-Won Kim.
- **핵심:** sulfide ASSLB 복합 cathode를 dry(PTFE) vs wet(NBR) 공정으로 제작.  digital-twin 모델링 +
  전기화학 + 형태 분석.  **PTFE는 긴밀한 접촉 유지 + void 형성 최소화 → 계면 열화 억제**; NBR은
  사이클 중 **계면 열화 + void 성장** 가속.
- **우리 모델 매핑:**
  - 우리 `additives.py`가 **PTFE 피브릴**을 모델링 → 이 논문이 "PTFE → void↓" 실험 확증 = 우리 MPM
    void-fill + coverage 유지와 직결.
  - **binder type(PTFE/NBR) → void → σ** 축은 우리 porosity/coverage 관계식에 **binder 항 추가** 후보.
  - "사이클 중 void 성장" = 우리가 아직 안 다루는 **degradation(시간 진화) 축** → 향후 porosity/coverage
    시간 변화 metric.
  - 그들의 digital-twin(전기-화학-기계 결합) = 우리 **DEM(transport)+MPM(mechanics)** 분업.  그들의
    binder-void 모델 vs 우리 coverage/Stage-E 비교 연구 가치.
  - **ACTION:** litdb 풀 디제스트(PDF) — 우리 LPSCl sulfide ASSB + PTFE additive와 1:1 비교.

### #262 — Digital Twin Mechanical Degradation Diagnostics, Si Anode Microstructure  ★★★
Small 22(3) (2026) e07883 (IF 11.8).  Jaejin Lim†, Junhyeok Choi† … Hyobin Lee, Yong Min Lee.  DOI 10.1002/smll.202507883.
- **핵심:** Si 부피변화 >300% → 접촉손실/박리/균열.  **FIB-SEM 토모그래피 3D 재구성** + Li⁺확산·계면
  반응·농도의존 기계변형 **결합 시뮬**.  충전율 0.5C→4C이 SoC 제한으로 응력↓ → 기계 열화 완화.
  응력기반 파괴 진단 digital-twin.
- **우리 모델 매핑:**
  - FIB-SEM 3D 재구성 = 우리 미세구조; **결합 전기-화학-기계** = 우리 MPM(mechanics)+DEM(transport).
  - "응력기반 파괴" ~ 우리 **fracture(Auerbach/Holm)** + MPM 응력장.  C-rate→응력→열화는 응력장
    degradation metric 아이디어.
  - digital-twin이 우리 프레임과 동일 → 그들의 결합 방식(Phase 4 PyBaMM과 연결될) 참고.

### #281 — Microstructure-Guided Reactant Transport, Architected 3D Air Electrodes (Li-O₂)  ★★ (→ Phase 4 blueprint급)  ✅ 풀 디제스트 완료
Journal of Power Sources **686** (2026) 240471 (IF 8.4), DOI 10.1016/j.jpowsour.2026.240471.  Suhwan Kim†,
Seungwon Jung† … Seokwoo Jeon\*(KU), Yong-Mook Kang\*(KU/UCSD), Yong Min Lee\*(Yonsei DTBL).  접수
2026-04-16 / 게재확정 2026-05-19.  MDB 2025 특별호.  ★ **풀 디제스트:**
`docs/lit_kim2026_a3d_air_electrode_microstructure_transport.md`.
⚠ **소재 = Li–O₂ 전지(금속-공기) 공기극** — Li metal 음극, **O₂ 가스**(주변 공기) + 액체전해질
(**1 M LiCF₃SO₃ in TEGDME**) 중 Li⁺, 방전생성물 **Li₂O₂**, 양극 골격 **Ni**(A3D BCT/diamond 또는 foam).
**우리 LPSCl sulfide ASSB가 전혀 아님** → **모든 전기화학·구조 절대값(용량·과전압·SSA·D_O₂·σ) 전이불가**.
가져올 것은 **METHODOLOGY 3종**(아래) — 수치 σ/porosity 앵커 아님(Bazzoun/Varkey/Minnmann/#266이 담당).
- **핵심:** **3D 디지털트윈 구조분석(GeoDict) + 1D 전기화학 모델(COMSOL) 결합**으로 architected-3D(A3D)
  공기극 미세구조 → reactant(O₂·Li⁺) 수송 엔지니어링. **구조변수(SSA·porosity·유효 D_O₂·유효 σ_e/σ_ion)를
  독립 변화시켜 산소수송·반응국소화·방전용량·과전압을 분리(decouple)**. ★ **단위셀 주기↓ → SSA↑(반응
  site↑) but pore 좁아짐 → 유효 D_O₂↓ → 고율 용량 제한(trade-off)** → **diamond 단위셀(잘 연결된 pore
  network) + electropolishing 표면공학(D300EP)**으로 SSA↑를 산소수송 보존과 양립 → **+37% 용량**.
- **방법:** **GeoDict 2025**(STL→voxel **0.01 µm**; ProcessGeo 'Repeat'·GrainGeo 'Roughen Surface'·
  FoamGeo·**MatDict**=SSA·**ConductoDict**=유효 σ_e/σ_ion·**DiffuDict**=유효 D_O₂) + **COMSOL 6.3 1D
  전기화학**(방전 ORR만; separator|air electrode|GDL 3도메인; 'Lithium-Ion Battery'+'Transport of Diluted
  Species in Porous Media'+'Domain ODEs and DAEs'; Li₂O₂ **film형 성장**(50 Ω·m²) → SSA·porosity↓·기공막힘).
  = 이 그룹 **3번째 GeoDict 활용**(#286 τ/PNM, #284 W_adh 다음).
- **핵심 수치:** A3D vs foam — 유효 **σ_e 2.51×10⁵ vs 0.40×10⁴ S/cm**(6배↑), **SSA 1.02×10⁷ vs 0.88×10⁵
  m²/m³**(~116배↑), porosity 45.6 vs 80.2 %; BCT B600/B500/B400/B300(Table S3) **SSA 1.02/1.69/2.10/2.88
  ×10⁷**(period↓ 단조↑), **유효 D_O₂ 0.92/1.67/1.29/1.46 ×10⁻⁸ cm²/s**(비단조, B500 최대), porosity
  45.6/56.9/51.1/54.3 %; 고율 용량 **B500 최대**(SSA 최고 B300 아님 — D_O₂가 지배), 과전압 B300 최소;
  decouple — **0.01 mA/cm²(저율): porosity가 용량 지배**(±15%p→±~30% 용량), **0.05(고율): SSA가 지배**
  (절반→−34.6%, 2배→+37.9%), **D_O₂ 비단조**(고율 1.5×에서 anomalous 열화→국소집중·기공막힘); 전자/이온
  전도도 변화는 무영향(rate-limiting 아님); **D300EP areal capacity B500/D400 대비 +37%**(고율). 1D 모델
  Table S2 전체셋(공기극 8/GDL 192/separator 420 µm; t₊ 0.92; D_O₂ 4.17e-8; O₂농도 9.46 mol/m³; 전류
  0.01/0.05/0.10 mA/cm²).
- **우리 모델 매핑 (★ METHODOLOGY 3종 — 수치 앵커는 Bazzoun/Varkey/Minnmann/#266):**
  - **(a) ✅ GeoDict ConductoDict/DiffuDict ↔ 우리 `voxel_conductivity.py` FV:** 둘 다 voxel에 ∇·(σ∇φ)=0
    (전도)/정상상태 Fick(확산) → 균질화 유효물성. **수학적으로 동일**(상용판). ✅ 우리 voxel FV 접근 확증.
    우리가 이미 정리한 한계(점접촉 sub-voxel→constriction 못 잡음, `voxel_conductivity_crossvalidation.md`)
    동일 적용 — 정렬골격(A3D/AM)엔 맞고 granular SE엔 DEM Holm 필요(frame[5]). ★ **DiffuDict(유효 D_eff/τ)는
    우리에게 없음** → voxel FV에 확산모드 추가 → contact-network τ와 frame[4] 교차검증 이식 후보.
  - **(b) ★★ 미세구조→effective→COMSOL 1D ↔ 우리 미세구조→effective→PyBaMM Phase 4 = published blueprint:**
    그들 COMSOL 1D(effective ε/τ/σ/D 주입→방전곡선, Table S2) = 우리 PyBaMM DFN
    (`{"transport efficiency":"tortuosity factor"}`로 τ 주입 + σ 주입). 결합 디테일 3종 직접채택:
    (i)핵심전극=측정 effective·보조도메인=Bruggeman ε^1.5 혼용, (ii)동역학 파라미터는 문헌+실험fit 후 고정·
    구조변수만 변화, (iii)방전부터·충전은 추가물리로 분리. ⚠ 방정식/물성은 Li-O₂ 특유→ASSB로 교체
    (단일이온 t₊≈1·접촉저항·무O₂).
  - **(c) ★ 구조변수 decouple→성능 귀속 ↔ 우리 predictor(knobs→metrics→성능):** 사고 동형(그들=물리모델
    1변수 sweep, 우리=ML 다변수). ★ **DOD colormap(작동조건이 어느 변수 지배) + 5축 레이더(다목적 구조-물성
    균형)** 시각화를 우리 predictor 출력에 이식 후보.
  - **우리 우위:** 그들은 **고정 미세구조(CAD/리소그래피) + GeoDict + 1D 전기화학(출력단)**; 우리 DEM+MPM은
    **압력→미세구조 예측(입력단) + 소성 morphology + 접촉 σ triad + granular constriction + fracture**. ⇒
    이상 워크플로 = 우리가 미세구조 생성/예측 → GeoDict식 effective(우리 voxel FV) → 그들식 1D 전기화학
    (우리 Phase 4). frame[5] 분업 재확인(그들엔 입자스케일 압축예측·접촉 σ triad 없음 — 논문도 자인:
    "1D framework relies on volume-averaged effective properties... cannot capture pore-scale
    heterogeneities"). ⚠ Stage-2 audit 영향 없음(Li-O₂ 외래 + Phase-4 결합 방법론 → transport 판정에 새
    벤치 없음); Phase 4 결합 프로토콜은 `stage4_electrochem_research.md` 반영 가치.

---

## ★★ TIER-2 — Dry-processed electrode / ASSB / CBD / 압축 (강하게 관련)

### #285 — Modulating CBD Viscoelasticity Suppresses Time-Dependent Spring-Back (Single-Crystal Cathodes)  ★★★  ✅ 풀 디제스트 완료
Energy Storage Materials (2026), DOI 10.1016/j.ensm.2026.105321 (PII S2405-8297(26)00453-8, ENSM 105321,
IF 19.3).  Rakhwi Hong†, Jingyu Choi† … Yong Min Lee\* (Yonsei DTBL).  접수 2026-04-03 / 게재확정 2026-06-20.
★ **풀 디제스트:** `docs/lit_hong2026_cbd_viscoelasticity_springback.md`.
⚠ **소재 = 단결정 NCMA(LiNi₀.₈₆₅Co₀.₀₅₄Mn₀.₀₇₅Al₀.₀₀₇O₂) 양극 + CBD(Super P+PVDF) + 액체전해질
(1.15 M LiPF₆ EC/EMC 3:7) 일반 LIB** — **우리 LPSCl sulfide ASSB가 아님** → 전기화학 절대값 전이불가.
**단 #286(흑연 pore 수송, 무관)과 달리 이 논문은 입자/CBD 역학(단결정 견고성·균열·압축·spring-back·CBD
점탄성)이 주제 → 역학은 (주의해서) 전이됨.**
- **핵심:** **단결정 CAM은 견고 → 균열·변형으로 에너지 못 빼므로 압축응력이 무른 점탄성 CBD로 몰림.**
  CBD 점탄성은 온도의존: **RT(25°C) → 탄성 CBD → 응력저장 → 시간의존 spring-back**(3주 **58→61.7 µm,
  +4 µm**); **HT(80°C) → 사슬이동도↑ → 점성/compliant CBD → 응력소산 → spring-back 억제**(3주 **+1 µm**).
  다결정은 입계균열로 소산 → spring-back 무(Table S1: 66 µm 유지). 코드 **RC-P/RC-S/HC-P/HC-S**(RT/HT ×
  pristine/3주stored).
- **핵심 수치:** spring-back RC-S +4 µm vs HC-S +1 µm; **500사이클 retention HC-P 69.9% / HC-S 67.2% /
  RC-P 62.6% / RC-S 32.4%(최악)**; bulk 전자저항 pristine 0.50 → stored 0.56 Ω·cm; **nanoindentation h_max
  RT 1193 → HT 1948 nm**, **dissipation ratio 0.62 → 0.67**; **DMA E′ HT −41.2%**(tan δ는 온도↑→↑);
  치밀화효율 RT는 roll gap 60 µm·HT는 70 µm에서 목표밀도; **CAM–CBD 계면접촉 HC-S +25%**, **유효 σ_e
  +50%**(RC-S 0.19 → HC-S 0.32); CAM/CBD σ_e = **0.7 / 500 S/m**(Table S2). 검증 = 2D SEM 재구성 +
  GeoDict(MatDict/PoreDict/ConductoDict) + DMA + nanoindentation + HPPC/EIS.
- **우리 모델 매핑 (★ 역학 검증 + spring-back 한계 지목 — 수치 σ/porosity 앵커는 Bazzoun/Varkey/Minnmann):**
  - **(a) ✅ 검증:** "단결정=견고 → 압축이 무른 상으로 몰림" = **우리 MPM rigid-AM scaffold + soft-plastic
    SE 분담의 실험 정당화**(우리 AM_S=single-crystal을 `--am-scaffold` 고정 obstacle로 둔 게 옳음).
    Stage-2 audit #7의 단결정 견고성 측면을 **검증**으로 굳힘.
  - **(b) ❗ 균열 GAP:** 다결정 입계균열→에너지소산→spring-back억제는 **역학 균열 역할**. 우리 DEM 균열은
    **transport(σ↓, Auerbach/Holm)만**, MPM은 균열 자체 없음(AM=rigid). (i)균열→두께 연결 + (ii)poly>single
    균열경향 **둘 다 없음** → chemo-mechanical(Phase 4) 한계.
  - **(c) ❗ 시간의존 spring-back 재현 불가(핵심):** 그들 spring-back = **점탄성=시간의존(3주)+온도의존**.
    우리 MPM = **rate-independent J2**(시간·점성·온도 전무), hold-relax는 ~40 substep **순간 settling**
    (`mpm3d_compaction.py:636-642`). ⇒ **구조적으로 시간의존 spring-back 재현 불가** = CLAUDE.md "springback
    validation pending"의 **정체**. **하자 아닌 미구현 물리**(정적 압축 종점은 옳게 줌). 해결 = MPM에
    **점탄성 요소(SLS=Maxwell+병렬스프링) + η(T)/E(T) DMA 캘리브** 추가. 이 논문이 검증데이터 제공.
  - **(d) ❗ CBD 역학 활성화:** 그들 **CBD 점탄성 = THE 설계변수**(spring-back 지배). 우리 `additives.py`
    CBD = 기하/부피/전자블로킹만(역학 없음). spring-back 다루려면 **CBD를 능동 점탄성 역학체로**(MPM에 CBD
    material point + 점탄성 + σ_e). transport-only Stage-2엔 불필요.
  - **(e) ❗ Calendering 온도축 GAP:** RT/HT가 그들 핵심 dial. 우리는 압력/변위만(온도·roll gap 없음). η(T)/
    E(T) 넣어야 온도효과 예측가능. ⚠ ASSB는 cold-press가 표준 → 온도축은 일반 LIB 확장/ASSB 고온공정 시만 우선.
  - **★ 워크플로 이식:** 2D SEM 재구성→GeoDict(계면접촉면적·pore size·**전류밀도 국소화/분산 맵**·유효 σ_e)
    = 우리 `voxel_conductivity`/`viz_mpm_continuum` 출력 추가 후보(#286과 동일 도구 — 전류밀도 localization
    맵은 우리 StageE coverage/force-chain 대응 시각지표).
  - **우리 우위:** 그들은 **post-mortem 2D 재구성 + 연속체 전자전도**; 우리 DEM+MPM은 **압력→미세구조→σ
    triad 예측 + 소성 morphology + 압축역학**. frame[5] 분업 재확인(그들엔 입자스케일 예측 없음).

### #276 — Materials/Process-Driven Microstructural Engineering for Dry-Processed Electrode (리뷰)  ★★
Materials Horizons 13 (2026) 3149-3177 (Back Cover, IF 11.4).  DOI 10.1039/d5mh02484f.
- **핵심:** DPE의 재료(AM/도전재/binder/CC) + 공정(혼합/kneading/lamination/**calendering**)을
  **미세구조 최적화 관점**으로 정리한 리뷰.
- **매핑:** 우리 DEM+MPM은 DPE 미세구조 도구 그 자체.  calendering→우리 압축, 혼합/분산→CBD seeding.
  우리 작업의 **positioning/framework 인용**.  (리뷰라 디제스트보다 맥락 참고.)

### #275 — Continuous Carbon Nanotube Sheath, Dry-Processed Thick Electrodes  ★★
Joule 10 (2026) 102392 (IF 37.1).  Jin Kyo Koo†, Jaejin Lim† … Yong Min Lee.
- **핵심(제목):** **연속 CNT sheath**로 dry-processed **두꺼운 전극**에서 초고에너지밀도 + 급속충전.
- **우리 모델 매핑 (방금 끝낸 SuperP-vs-VGCF와 직결):**
  - "연속 1D CNT 망" = 우리 **VGCF/fibre additive + `--fibre` densification(연속 thread)**.  우리가 방금
    VGCF 섬유를 연속 thread로 잇는 게 정확히 이 "continuous sheath" 개념.
  - **두꺼운 전극** = 우리 real_10 708-cell thick.  연속 1D 도전망이 두꺼운 전극에 유리 → 우리 AM-poor
    crossover 논의(연속 VGCF망 vs 분산 SuperP)의 문헌 근거.

### #286 — Porosity-Gradient Dry-Processed Graphite + Deformable Primer Layer  ★★  ✅ 풀 디제스트 완료
Energy Storage Materials (2026), DOI 10.1016/j.ensm.2026.105331 (ENSM 105331, IF 19.3).  Hyundong Yoo†,
Jaejin Lim† … Yong Min Lee\*, Hansu Kim\* (Hanyang+Yonsei).  ★ **풀 디제스트:**
`docs/lit_yoo2026_porosity_gradient_dry_electrode.md`.
⚠ **소재 = 천연흑연 음극 + 액체전해질(1M LiPF₆ EC/EMC 3:7 +10% FEC) 일반 LIB** — **우리 LPSCl sulfide
ASSB가 아님** → 절대 transport 값 전이불가. 가져올 것은 **설계개념·측정방법·정성추세**(수치 앵커 아님).
- **핵심:** **PL(primer layer) binder 변형성**(PVDF가 가장 무름, 압축/탄성계수 **6.31/15.99 MPa** vs
  PAA·CMC 약 2배)을 선택하면 라미네이션 **비대칭응력 → 자발적 z-porosity 구배**(위 다공·아래 치밀).
  전체 porosity는 같아도(MIP **32.2–33.3%**) z-분포만 다름. **DPE@PVDF-PL = 가장 가파른 구배(top↔bottom
  Δ24.5%p vs WPE 5.6%p)**.
- **검증:** 3D XCT(250 nm) + FIB-SEM 토모(46.52 nm, 800장, CNN 분할) + GeoDict 확산-τ + PNM(MATLAB) +
  BESTmicro 3D 전기화학시뮬.
- **핵심 수치:** tortuosity **PVDF 1.86 < PAA 1.98 < WPE 3.09**(확산시뮬, EIS도 같은 순서); PNM
  coordination number **PVDF 4.20 / PAA 4.44 ≫ WPE 2.94**; connectivity bandwidth 표준편차
  0.1581/0.1309/0.0976(PVDF 장거리연결 최고); **3C 방전 305 vs WPE 258 mAh/g**, 3C CC용량 **80.2 vs 23.3**;
  full-cell 3C CC-SOC **PVDF 27.89% vs WPE 14.31%**; AM↔PL 접촉면적 PVDF +45%(표면높이차 12.1 µm);
  ICE DPE 85–87% < WPE 92.7%(**PTFE 탈불소화** → LiF+비정질탄소, dQ/dV 0.2–0.8 V·XPS).
- **우리 모델 매핑 (★ 방법/설계 청사진 — 수치 앵커는 Bazzoun#가 담당):**
  - **(a) Phase 5 z-layer:** porosity-gradient = 우리 **z-band 합성**(`extract_2d_microstructure.py`
    K=8 stratified, line 668) + tortuosity pore elongation(line 826)의 **published 실증** → Phase 5를
    **band별 다른 porosity 구배**로; 출력에 **"두께방향 porosity(z) 프로파일" + top↔bottom Δ** metric 추가.
  - **(b) tortuosity:** 그들 **EIS 식(1) ↔ 확산시뮬 식(2, ε/τ²·D_e)** 2-방법 교차검증 = 우리 σ_ionic
    C(τ)의 τ(Laplace/Dijkstra) 선택 템플릿(우리는 실측 τ 없음). ⚠ pore-도메인 Bruggeman형 → 폼 차용 금지.
  - **(c) PTFE:** 그들 1D피브릴 pore↑ = 우리 `additives.py` PTFE fibril 형태 반영됨; **탈불소화 ICE손실은
    우리 미모델**(일반 LIB 확장시 ICE 항 후보; ASSB는 관련 낮음).
  - **(d) 토모그래피:** FIB-SEM→GeoDict-τ + PNM(coordination·connectivity matrix)을 우리
    `voxel_conductivity`/`mpm3d`에 이식 — 특히 **pore-side 지표**(우리는 particle-contact CN만) +
    확산-τ↔contact-σ frame[4] 교차검증.
  - **(e) 농도분극:** BESTmicro 3D FVM(BV+Fick, 3C CC-CV 0.005 V cutoff) = 우리 **Phase 4(PyBaMM) 흑연계
    reference workflow**. ⚠ ASSB는 전해질농도분극 대신 SE-network σ가 지배 → 적응 필요.
  - **우리 우위:** 그들은 **post-mortem 고정 미세구조 + 연속체 확산**; 우리 DEM+MPM은 **압력→미세구조→σ
    예측 + 소성 morphology + 접촉 σ triad + fracture**. ⇒ 이상 워크플로 = 우리가 미세구조 생성/예측 →
    그들식 토모-정량 검증 → 그들식 전기화학시뮬로 농도분극 닫기. frame[5] 분업 재확인.

### #284 — Optimized Carbon Coating on SiOx, Balanced Ion/Electron Transport + Uniform Dispersion  ★★  ✅ 풀 디제스트 완료
Journal of Power Sources **689** (2026) 240698 (IF 8.4), DOI 10.1016/j.jpowsour.2026.240698.  Jihwan Oh†,
Seungyeop Choi† … Yong Min Lee\* (Yonsei DTBL + ActRO Corp.).  접수 2026-04-04 / 게재확정 2026-06-10.
MDB 2025 특별호.  ★ **풀 디제스트:** `docs/lit_oh2026_carbon_coating_siox_ion_electron_balance.md`.
⚠ **소재 = SiOx(0<x<2) + 인조흑연 음극 + 액체전해질(1.15 M LiPF₆ EC/EMC 3:7 + 10% FEC) 일반 LIB**,
full-cell 양극 NCM622 — **우리 LPSCl sulfide ASSB가 아님** → 전기화학 절대값(용량·ICE·Rct·rate) 전이불가.
가져올 것은 **이온/전자 trade-off 개념 + 분산 측정법(SSRM/W_adh) + 정성추세**(수치 σ/porosity 앵커 아님 —
Bazzoun/Varkey/Minnmann이 담당).
- **핵심:** **CVD 아세틸렌 탄소코팅 두께(thin/moderate/thick = TGA 0.95/2.91/4.18 wt%)가 이온↔전자 수송
  BALANCE를 지배.** **두꺼운 코팅 → 전자전도↑(연속 도전망) BUT Li⁺ 수송 차단 → Rct↑·분극↑**; **얇은 코팅 →
  전자경로 불충분**; ★ **moderate(~2.91 wt%) = 균형 → 최저 임피던스·최고 rate·최고 cycling.** 또 탄소코팅이
  SiOx **표면에너지를 CBD에 가깝게** 바꿔(γᵖ 21.6→11–14) **SiOx–CBD 상호작용↑ → CBD 균일분산**(bare는 응집).
- **검증:** TEM(코팅두께) + TGA(C wt%) + **SSRM 저항맵(분산)** + OWRK 표면에너지/work-of-adhesion + 유변학 +
  EIS/DCIR/GITT/CV/DRT + SiOx/graphite‖NCM622 full-cell + 48 mAh pouch + SAICAS + post-mortem SEM/XPS.
- **핵심 수치:** TEM thin **~4–5 nm conformal**, thick **조밀**; bulk 전기저항률 bare **0.033 → thin 0.018 →
  moderate 0.013 → thick 0.012 Ω·cm**(moderate≈thick saturate); 계면 전기저항 **1.7→1.0→0.6→0.5 mΩ·cm²**;
  **ICE half 73.6/80.0/81.6/81.5%, full 58.7/69.1/73.1/71.8%**(moderate≈thick saturate); **work-of-adhesion
  (SiOx↔CBD) bare 99.9 → thin 107.3 / moderate 108.6 / thick 107.9 mN/m**(moderate 최고); DCIR·DRT(Z_W·Rct·
  R_SEI) **moderate 최소**(thick은 Rct↑=Li⁺ 차단); 70사이클 후 단면 두께 **bare ~93 vs moderate ~70 µm**;
  **SAICAS cohesive 112.3/129.0/147.0/134.6 N/m, adhesive 120.2/138.5/196.5/149.9 N/m**(moderate 최고).
  조성: SiOx/graphite 음극 80:9:1:5:1.5:5(SiOx:흑연:Super C65T:MWCNT:Na-CMC:SBR), NCM622 양극 96:2:2.
- **우리 모델 매핑 (★ CBD ion/electron trade-off 독립확증 + 분산 측정법 — 수치 σ 앵커는 Bazzoun/Varkey/Minnmann):**
  - **(a) ✅ 이온/전자 trade-off 독립확증:** 그들 "탄소↑→전자↑·이온↓, moderate 균형" = 우리 CBD
    **"SuperP 전자 1.3× win BUT 이온 1.8× blocking(σ_ionic 0.0168 < VGCF 0.0298)"**(`docs/cbd_morphology_roadmap.md`)와
    **동일 ion/electron 긴장**(그들=탄소 양/두께 축, 우리=도전재 종류/분산 축). → 우리 CBD blocking이
    **시뮬 artifact 아닌 일반 trade-off**임을 강화(모델 신뢰도↑, flaw 아님 = trade-off 그림 enrich).
  - **(b) ★ balance point 개념:** 우리 CBD는 **채널별 승자**(SuperP=전자, VGCF=이온)만 보고, **종합 최적
    탄소량(balance optimum)은 미정량**. 그들 **moderate-C 명시적 최적**이 동기 → ★ **탄소 wt% 0.5→4 sweep
    하며 voxel σ_e gain vs σ_ionic loss 동시 plot → 우리 balance curve**(roadmap PENDING 4 wt% 테스트가 시작점).
  - **(c) ★ 분산 측정법 이식:** 그들 **SSRM 저항맵 공간균질도 + W_adh(표면에너지 매칭) + 유변학**. 우리는
    분산을 morphology 근접도로만 봄(균일도 스칼라 無) → **voxel carbon occupancy 변동계수(CV) / nearest-carbon
    거리분포**로 SuperP(분산=낮은 CV) vs VGCF(응집=높은 CV) 단일수치화; **carbon↔SE/AM W_adh**로 우리
    `nucleate_frac`/`surface_frac` 경험치 물리근거화(단 LPSCl 표면에너지 우리 측정 필요).
  - **(d) thick-C 이온차단 = 우리 blocking 방향일치(다른 주체):** 그들 thick=**연속 코팅층 barrier(Rct↑,
    전해질-매개)**, 우리 SuperP=**분산 입자 SE-packing 교란(σ_ionic↓)** → 방향 동일, 주체 다름.
  - **우리 우위:** 그들은 **post-mortem 측정(고정 구조)**; 우리 DEM+MPM은 **압력→미세구조→σ triad 예측 +
    소성 morphology + voxel FV(carbon σ_e gain·σ_ionic blocking mechanistic 정량 = 그들 SSRM의 인과버전)**.
    frame[5] 분업 재확인(그들엔 입자스케일 예측·접촉 σ 없음). ⚠ 절대 전기화학값(Rct·ICE) 전이불가(액체/음극).

### #264 — Multi-Faceted Binder via Thiol-Ene Click, Low-Pressure-Operable ASSB  ★★
Advanced Functional Materials 36(15) (2026) e16017 (IF 19.9).  Young Jun Park … Yong Min Lee, Yoon Seok Jung.  DOI 10.1002/adfm.202516017.
- **핵심:** SBR binder를 thiol-ene click으로 개질(COOH 접착 + TMPT 가교).  **저압 작동** ASSB.
  가교가 접착보다 저압 성능에 더 중요.  전기-화학-기계 안정성.
- **매핑:** **저압 ASSB = 우리 압축 압력 축**; binder 가교 → strain 저항 → 우리 MPM 기계/coverage 유지.
  binder 기계물성이 압축에 영향 → --coh(cohesion)와 연결.

### #270 — Ion-Conducting Cavity Filler, In-Situ SEI in Sulfide SE Sheets (ASSB)  ★★
Chemical Engineering Journal 529 (2026) 173036 (IF 12.5).  Minjae Kim†, Yongjun Kwon† … Yong Min Lee.
- **핵심(제목):** sulfide SE sheet의 cavity를 이온전도성 filler로 채워 in-situ SEI.
- **매핑:** sulfide SE sheet + cavity 충전 = 우리 **SE void-fill(MPM)** + SE 퍼콜레이션.  filler가 cavity
  메움 = 우리 SE 조밀화.

### #268 — Calendering-Induced Interfacial Reconfiguration, Li Metal Powder Electrodes  ★★
EES Batteries 2 (2026) 464-474 (Front Inside Cover).  Dongyoon Kang†, Sun Hyu Kim†, Jaejin Lim† … Yong Min Lee.
- **핵심(제목):** **calendering(압연)**이 Li metal powder 전극 계면 재구성 → 전기화학 활성화.
- **매핑:** **calendering = 압축**(우리 MPM/DEM).  압력하 계면 재구성 = 우리 contact-area 진화(Stage-E).

---

## ★ TIER-3 — 주변부 (transport / 기계 / binder)

- **#260** Regularly Arranged Micropore, Li-Ion Transport in SiOx/Graphite — *Nano-Micro Letters* 18(75) (IF 38.5).
  정렬된 micropore → 효율 수송 = 우리 porosity/tortuosity → σ_ionic; ordered vs random pore = 패킹.
- **#283** Primer Layer Design, Dry Electrode-CC Interfaces — *ACS Energy Letters* (IF 17.5).  dry 전극 접착/계면(주변부).
- **#267** Surface/Interfacial Cutting, Adhesive Strength Measurement — *J. Energy Storage* 150 (IF 10.7).
  접착강도 = 우리 binder/cohesion(--coh) 측정법.
- **#282** Charge-Engineered Cellulose Nanofibril Binders, PFAS-free High-Loading — *Nature Communications* (2026),
  DOI 10.1038/s41467-026-73909-0 (Open Access).  Sang-Woo Kim†, Nag-Young Kim† … **Yong Min Lee(공저)** …
  Won Bo Lee\*(SNU), Sang-Young Lee\*(Yonsei) + UNIST.  ✅ **풀 디제스트:** `docs/lit_kim2026_charge_engineered_cnf_binder.md`.
  ⚠ **LEAD = Sang-Young Lee + Won Bo Lee + UNIST; Yong Min Lee는 공저자(주도 아님)** → DTBL 핵심(#266/#285/#286)보다 협업·주변부.
  - **핵심:** 목재 유래 셀룰로오스 나노피브릴을 **4급 암모늄(−N(CH₃)₃⁺)으로 양이온화(c-CNF, ζ +31.9 mV·DS 0.39·직경 38 nm)** →
    슬러리에서 **정전기 반발로 분산 안정화** + 건조 후 **강한 수소결합으로 접착·구조 무결성** → **PFAS(PVDF)·NMP 없이**
    초고로딩 **113 mg/cm²·밀도 3.65 g/cm³·면적용량 22.5 mAh/cm²·1781.5 Wh/L·431.8 Wh/kg**(바인더 1 wt%) NCM811 양극.
    PVDF 대비: t_Li+ **0.83 vs 0.54**, 토르투오시티 **3.6 vs 6.8**, 접착일(Fowkes) 활물질/도전재 **107.1/103.6 vs 78.40/77.56 mN/m**,
    peel 접착 **157.3 vs 14.2 N/m**, 전극전도도 0.23 vs 0.16 S/cm, 흑연‖NCM811 300cyc **88% vs 80%**.
  - **DFT:** **VASP GGA-PBE PAW(cutoff 450 eV)** — MEP/ESP 맵(c-CNF 양전하) + 결합에너지(−OH···−OH **−0.64 eV** ≈ 10× PVDF −F···H− −0.07;
    MD Al₂O₃ 슬랩 c-CNF **−1204.8 vs** PVDF **−530.26 kJ/mol**) + 음이온 교환(TFSI⁻ MEP −0.025 Ha/e·ΔG −46.7 kJ/mol → PF6⁻ 자발 치환).
    보충데이터 16종 = Gaussian-cube SCF density/ESP(PVDF/b-CNF/c-CNF/TFSI/PF6/Cl).
  - **우리 모델 매핑 (★ TIER-3 / 주변부 — 모델 영향 0):** ⚠ **분자스케일 바인더 화학 + 액체전해질 NCM811 LIB** —
    우리 LPSCl sulfide ASSB의 연속체/접촉망 DEM+MPM과 소재·스케일·물리 모두 다름.  접점은 **맥락 3가지뿐**:
    (a) **PFAS-free 바인더 = 우리 additives.py가 기하로만 모델하는 PTFE(역시 PFAS)의 대안 맥락**(바인더 화학 미모델);
    (b) **전하→분산 개념이 우리 CBD 분산균일도(E2)에 개념적 인접**하나 메커니즘 다름(분자 표면전하/DLVO vs 기하 seeding) → 수치 전이 無;
    (c) **고로딩 양극 맥락**(단 그들 한계=Peclet 수직분리·전해질 침투는 ASSB엔 없음).  ✗ **transport/압축/σ 앵커 아님**(Bazzoun/Varkey/Minnmann/#266 담당).
    ✗ **#284와 혼동 금지** — 이건 바인더 교체(c-CNF가 분산·접착·t_Li+·전도 all-win)이라 우리 SuperP-vs-VGCF **ion/electron trade-off와 대응 안 됨**
    (그 trade-off 확증·분산정량법은 #284가 공급).  ✗ 그들 DFT=분자 MEP, 우리 DFT-DEM=입자스케일 → 스케일 달라 상보 아님.  **TIER-3 유지.**

---

## · TIER-4 — 타 화학계 (카탈로그만; 우리 모델 직접 관련 낮음)

| # | 제목(요약) | 저널 | 비고 |
|---|---|---|---|
| 280 | 탄성 Li metal anode — 나노-크럼플+마이크로-오목 PDMS 집전체 + 친리튬 TREN SAM (LEAD=Cho/Ko/Back, **Y.M.Lee 공저**). E_host 31.4 MPa·핵생성 124.5→11.0 mV·대칭 ~2,600 h@1/1·~2,100 h@3/3·LFP 90.2%@1,000(1C). 음극 도금 계면공학+액체 LFP → 모델 영향 0; 응력완화 테마만 MPM/#285에 먼 인접. 디제스트 `docs/lit_choi2026_elastomeric_li_metal_anode.md` | Adv. Energy Mater. (25.5) | Li metal anode |
| 279 | Electronic-ionic polymer, PCET, aqueous Zn-ion | Energy Storage Mater. (19.3) | Zn-ion |
| 278 | Na 층상 cathode, Bi 치환 공기·수분 안정화 | Chem. Eng. J. (12.5) | Na cathode |
| 277 | Dual-layer anode 보호, lean-electrolyte Li-S | J. Energy Storage (10.7) | Li-S |
| 274 | High-Ni cathode, 수분응답 dehumidifying separator | ACS Nano (17.3) | separator/High-Ni |
| 273 | Ultra-thin ceramic-coated dry-stretched PP separator | Chem. Eng. J. (12.5) | separator |
| 272 | Passivation 불균일 제거, Li/Zn/Mg 도금 | Chem (19.1) | metal plating |
| 269 | Stepwise activation Zn 증착, flowless Zn-Br | Small (11.8) | Zn-Br |
| 265 | Nb-doped Ni-rich multiphase cathode 소재 | Nature Nanotech. (37.5) | cathode 소재 |
| 261 | 2D polymeric metal phthalocyanine, Li metal full cell | eScience (52.9) | 2D 소재 |

---

## ⇒ 우리 모델에 넣을 인사이트 — 실행 우선순위

| 순위 | 논문 | 인사이트 | 우리 모델 hook | 상태 |
|---|---|---|---|---|
| 1 | #266 | bimodal P:S 7:3 → tortuosity↓ → σ↑, 87.8%@200cyc | **P:S 7:3 production + Furnas dip 실험 앵커** | PDF로 수치 추출 → validation corpus |
| 2 | #263 | 2D param → stochastic 3D → transport 예측 | **Phase 4-5 합성 published blueprint** | 방법 비교/이식 |
| 2.5 | #281 | 미세구조→GeoDict effective→1D 전기화학(COMSOL)→방전; 구조변수 decouple | **★ Phase 4 결합 blueprint(=우리 voxel FV→PyBaMM) + DiffuDict(유효 D_eff/τ) 이식 + predictor decouple** | ✅ 풀 디제스트 (`lit_kim2026_...md`); ⚠Li-O₂ 외래→METHODOLOGY만, 수치앵커 아님 |
| 3 | #271 | PTFE void↓ vs NBR void↑ (digital-twin) | binder→void→σ 축; PTFE additive 검증 | litdb 풀 디제스트(PDF) |
| 4 | #285 | 단결정=견고→압축이 CBD로; CBD 점탄성→시간의존 spring-back; HT 억제 | **(✅)rigid-AM 검증 + (❗)점탄성 spring-back 미구현 한계** | ✅ 풀 디제스트 (`lit_hong2026_...md`); ⚠단결정NCMA/액체→역학만 전이 |
| 5 | #286 | porosity 구배(z) + 토모 정량(τ/PNM) + 전기화학시뮬 | **Phase 5 z-layer + 토모 방법 이식 + Phase 4 workflow** | ✅ 풀 디제스트 (`lit_yoo2026_...md`); ⚠흑연/액체→방법·개념만, 수치앵커 아님 |
| 5.5 | #284 | 탄소코팅↑→전자↑·이온↓, moderate 균형; SSRM/W_adh 분산정량 | **CBD ion/electron trade-off 독립확증 + balance curve sweep + 분산 균일도 metric** | ✅ 풀 디제스트 (`lit_oh2026_...md`); ⚠SiOx흑연/액체→개념·방법만, 수치앵커 아님 |
| 6 | #275 | 연속 CNT sheath, thick 전극 | **--fibre 연속 thread / VGCF 검증** | 이미 정합(방금 작업) |
| 7 | #262 | FIB-SEM 3D + 결합 chemo-mech, 응력 파괴 | digital-twin 프레임 + fracture | Phase 4 연결 |
| 8 | #264/#268/#270 | 저압 ASSB / calendering / SE cavity-fill | 압축·압력 축 + SE void-fill | 맥락 인용 |

**다음 단계:** 위 #266/#263/#271/#285/#262 PDF를 받으면 각각 `docs/lit_<author>2026_<topic>.md`로
litdb-curator 풀 디제스트(수치·그림·방법 전체) → comparison_vs_ours에 우리 DEM+MPM과 1:1 비교 추가.
PDF 없이도 위 인덱스·매핑은 즉시 우리 로드맵(Phase 1-5)·CLAUDE.md 서사에 반영 가능.

**출처(검증):** [#271 Yonsei Pure](https://yonsei.elsevierpure.com/en/publications/unveiling-degradation-mechanisms-of-sulfide-based-composite-catho/) ·
[#263 AEM](https://advanced.onlinelibrary.wiley.com/doi/10.1002/aenm.70730) ·
[#266 ACS EL](https://pubs.acs.org/doi/10.1021/acsenergylett.5c03923) ·
[#262 Small](https://onlinelibrary.wiley.com/doi/10.1002/smll.202507883) ·
[#276 Mater. Horiz.](https://pubs.rsc.org/en/content/articlelanding/2026/mh/d5mh02484f) ·
[#264 AFM](https://advanced.onlinelibrary.wiley.com/doi/10.1002/adfm.202516017)
