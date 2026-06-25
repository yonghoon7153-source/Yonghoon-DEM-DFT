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

### #281 — Microstructure-Guided Reactant Transport, 3D Air Electrodes (Li-O₂)  ★★
Journal of Power Sources 686 (2026) 240471 (IF 8.4).
- **핵심:** architected 3D air electrode 미세구조 → reactant 수송 엔지니어링 (다른 화학계지만 동일 원리:
  미세구조 설계 → 수송 최적).
- **매핑:** 미세구조→수송 설계 원리 공유; 우리 transport triad와 같은 사고.  주변부(다른 시스템).

---

## ★★ TIER-2 — Dry-processed electrode / ASSB / CBD / 압축 (강하게 관련)

### #285 — Modulating CBD Viscoelasticity Suppresses Time-Dependent Spring-Back (Single-Crystal Cathodes)  ★★★
Energy Storage Materials, Accepted 2026 (IF 19.3).  Rakhwi Hong†, Jingyu Choi† … Yong Min Lee.
- **핵심(제목):** **CBD 점탄성**을 조절해 단결정 cathode의 **시간의존 spring-back(압축 후 되튐) 억제**.
- **우리 모델 매핑:**
  - **spring-back = 우리 MPM springback/relaxation** (CLAUDE.md "springback validation pending"; MPM
    `--protocol hold` = 변위정지 후 relax = spring-back 모델링).  이 논문이 **CBD 점탄성 메커니즘** 제공.
  - 단결정 = 우리 **AM_S**.  CBD 점탄성 → 우리 CBD 상(additives.py)의 기계 물성에 점탄성 추가 후보.
  - **ACTION:** PDF로 spring-back 정량(시간상수, 압력) 추출 → 우리 MPM hold-relax 검증 앵커.

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

### #284 — Optimized Carbon Coating on SiOx, Balanced Ion/Electron Transport + Uniform Dispersion  ★★
Journal of Power Sources 689(15) (2026) 240698 (IF 8.4).  Jihwan Oh†, Seungyeop Choi† … Yong Min Lee.
- **핵심(제목):** carbon coating이 **이온/전자 수송 균형 + 균일 분산**.
- **매핑:** ion vs electron 수송 **trade-off** = 우리 σ_ionic↔σ_electronic; **균일 분산** = 우리 CBD seeding
  형태(SuperP 분산 vs VGCF 응집).  우리 CBD ionic-blocking vs electronic-bridging trade-off와 동일 긴장.

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
- **#282** Charge-Engineered Cellulose Nanofibril Binders, PFAS-free High-Loading — *Nature Communications* (IF 18.1).  binder(주변부).

---

## · TIER-4 — 타 화학계 (카탈로그만; 우리 모델 직접 관련 낮음)

| # | 제목(요약) | 저널 | 비고 |
|---|---|---|---|
| 280 | Elastomeric Li metal anode, nano-crumpled architecture | Adv. Energy Mater. (25.5) | Li metal anode |
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
| 3 | #271 | PTFE void↓ vs NBR void↑ (digital-twin) | binder→void→σ 축; PTFE additive 검증 | litdb 풀 디제스트(PDF) |
| 4 | #285 | CBD 점탄성 → spring-back 억제 | **MPM hold-relax springback** 메커니즘 | PDF로 시간상수 |
| 5 | #286 | porosity 구배(z) + 토모 정량(τ/PNM) + 전기화학시뮬 | **Phase 5 z-layer + 토모 방법 이식 + Phase 4 workflow** | ✅ 풀 디제스트 (`lit_yoo2026_...md`); ⚠흑연/액체→방법·개념만, 수치앵커 아님 |
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
