# Nam 2026 (Materials Horizons REVIEW, 13, 3149-3177) — 건식전극(DPE) 미세구조 엔지니어링 리뷰 ★ 우리 DEM+MPM 프로젝트의 FRAMEWORK/POSITIONING 논문

**인용:** Gwonsik Nam†, Jaejin Lim†, Seungyeop Choi†, Sang Cheol Nam, Kijoo Hong, Jisung Lee,
**Yong Min Lee\*** — "Materials- and process-driven microstructural engineering for scalable
dry-processed electrode manufacturing", *Materials Horizons* **13** (2026) 3149-3177,
DOI 10.1039/d5mh02484f. **Open Access (CC-BY 3.0).** 접수 2025-12-31, 게재확정 2026-02-20.
**Back-cover featured** (Showcasing a review from Prof. Yong Min Lee's laboratory). †G. Nam,
J. Lim, S. Choi 동등기여.

**소속:** Yonsei University — (a) Dept. of Battery Engineering + (b) Dept. of Chemical &
Biomolecular Engineering (= **Digital Twin Battery Lab, 이용민 LEAD**); (c) POSCO Future M; (d)
LIB Materials Research Center, POSCO N.EX.T Hub, POSCO Holdings. 교신 yongmin@yonsei.ac.kr.
지원: KIAT(MOTIE) + POSCO Holdings. **ChatGPT v5.2는 언어편집에만 사용(저자 명시).** 이해상충 없음.

**★ 이 논문의 위상 (다른 디제스트와의 차이):** 이건 이 연구실(이용민 DTBL)의 **#276 — 우리 정확한
도메인(건식전극 미세구조)의 자기 그룹 리뷰**다. **수치 앵커 논문이 아니라 FRAMEWORK/POSITIONING
논문**이다. Bazzoun(#, LPSCl σ 앵커)·Varkey(halide DEM)·Minnmann(LPSCl porosity 앵커)·#266(P:S 7:3
bimodal 앵커)이 **수치**를 담당하면, 이 리뷰는 우리 DEM+MPM 전체가 **무슨 문제를 푸는 도구인지를 정의하는
어휘·4단계 공정 분류·미세구조-특징→성능 지도**를 공급한다. → 논문 intro/significance에서 우리 작업을
**"바로 이 리뷰가 정의한 미세구조 엔지니어링을 정량·예측하는 엔진"**으로 자리매김하는 데 최강의 근거.

**소재계 ⚠ CRITICAL CAVEAT:** 이건 **일반 Li-ion(LIB) 건식전극(DPE) 리뷰**다 — 우리 **LPSCl sulfide
ASSB가 specifically 아니다**. 따라서:
- **정량 셀 절대값(용량 mAh/g, ICE %, retention %, areal mAh/cm²)은 Li-ion 맥락** → LPSCl ASSB로 직접
  전이 금지(수치 앵커는 위 4개 논문이 담당).
- **그러나 (a) 미세구조 엔지니어링 FRAMEWORK, (b) 4단계 공정(혼합/kneading/lamination/calendering),
  (c) PTFE 피브릴화(Maxwell), (d) 미세구조-특징 어휘(AM–CBD contact / ASA / ion-percolation tortuosity /
  electron-conduction continuity)는 DIRECTLY 전이된다** — DPE는 ASSB 양극의 선도 공정 경로이기도 하고
  (리뷰가 직접 LPSCl 사례를 다룸: ref 57·123·148), 미세구조 물리는 화학계 무관하다.
- ⇒ **framework/positioning + 정성 DPE 사실 = 강하게 전이; 특정 Li-ion 셀 절대값 = 맥락(앵커 아님).**

DB 동반 파일: 없음(생성 안 함 — 리뷰는 수치 corpus가 아니라 framework). 주요 수치는 본 MD 본문 표에 정리.
SI: 없음(리뷰, SI 없음).

---

## ★ 한 문장 결론 — 이게 무엇이고 우리에게 왜 중요한가

**건식전극(DPE)의 성능은 소재만으로도 공정만으로도 결정되지 않고 둘의 결합(coupled interplay)이 빚는
미세구조가 결정한다**는 명제 아래, DPE 제조를 **4단계(powder mixing · kneading · laminating ·
calendering)**로 해부하고, 각 단계가 만드는 **3대 결함(non-uniformity · delamination · heterogeneous
densification/cracking)**의 기원을 정리하며, 소재(AM/도전재/binder-PTFE&대안/집전체) 혁신과 공정 기술을
**미세구조 최적화 관점**으로 종합한 리뷰다. 미세구조 핵심특징으로 **각 성분의 공간분포·형태, AM–CBD
계면접촉, effective active surface area(ASA), ion-percolation 경로의 tortuosity, electron-conduction
경로의 continuity**를 지목하고 이들이 **rate/cycle/energy-density/safety**를 가른다고 본다.

**우리 hook(가장 중요):** 이 리뷰의 어휘가 곧 **우리 DEM+MPM의 출력**이다. 그들의 공정단계 **calendering =
우리 압축(porosity, contact area, σ@300MPa)**, 그들의 미세구조 특징 **AM–CBD contact / ASA /
ion-percolation τ / electron-conduction continuity = 우리 coverage(cov_AM,Tabor) / ASA / τ_Laplace,eff·
τ_Dijkstra / σ_e 접촉망·CN**, 그들의 **PTFE 피브릴망 = 우리 `additives.py` PTFE fibril 모델**, 그들의 결함
**heterogeneous densification = 우리 porosity(z) 구배(#286/Phase 5)**. **1:1 매핑**이다. 결정적 차이:
**리뷰는 DESCRIPTIVE(필드를 정성 서술)**, **우리는 PREDICTIVE(압력→미세구조→σ triad, explicit 접촉망 +
소성 morphology + fracture)**. ⇒ **우리 작업은 이 리뷰가 깔아둔 framework를 정량·예측하는 엔진**이다.

---

## 0. 약어·핵심개념 (우리 맥락)

- **DPE / WPE:** dry-processed electrode(건식, 무용매, PTFE 피브릴화) / wet-processed electrode(습식,
  슬러리 코팅). 이 리뷰 전체의 대비축.
- **CBD (Carbon-Binder Domain):** 도전재(carbon)+binder가 함께 만드는 도메인. WPE에서는 건조 중
  **CBD migration**으로 비균일 응집체 형성; DPE에서는 PTFE 피브릴이 연속망을 만들어 더 균일.
- **PTFE fibrillation (Maxwell technology):** PTFE가 전단응력 하에 **피브릴화**(섬유화)하여 AM+도전재를
  물리적으로 그물처럼 묶는 무용매 결합 메커니즘. DPE의 지배적 제조법. Maxwell(Tesla 인수)가 상용화.
- **ASA (effective active surface area):** 전기화학 반응이 실제 일어날 수 있는 유효 활성표면적. 미세구조
  특징의 하나. 우리 coverage/ASA에 대응.
- **Ion-percolation tortuosity / electron-conduction continuity:** 이온경로 우회도 / 전자경로 연결성 —
  이 리뷰가 미세구조→성능을 가르는 핵심으로 꼽는 두 수송 특징. 우리 σ_ionic의 τ·percolation / σ_e의
  contact-network·CN에 직접 대응.
- **Thick / high-loading electrode:** 후막·고로딩 전극(~200 µm, 20→70 mg/cm²). 비활성 성분 비율↓ →
  에너지밀도↑. DPE가 특히 유리. 우리 real_14 708-cell thick 전극 맥락.
- **PFAS / PFOA:** per-/polyfluoroalkyl substances / perfluorooctanoic acid. PTFE가 속한 규제대상
  불소화합물군 → beyond-PTFE binder 동기.

---

## 1. 배경 / 동기 (Introduction §1, p.3149-3150)

- EV 보급(>24% 성장) → LIB가 **에너지밀도·가격·안전**의 상충 trade-off를 동시 충족해야. 내연기관 완전대체
  목표: **에너지밀도 >350 Wh/kg_cell, 제조비 <100 USD/kWh_cell, 수명 >15년, 실사용조건 안전**.
- 전통적으로 LIB 개발은 **chemistry-driven(소재 고유 물성)**에 집중 → specific capacity·안정성·수명 향상.
  그러나 **cell-level 성능은 chemistry만으로 안 됨** — 전극의 **architecture(조성·loading·밀도·미세구조
  특징: 성분분포·ASA·이온/전자 경로)**가 소재물성을 실제 성능으로 번역한다. → 최근 **electrode-/cell-level
  engineering**으로 이동(ref 13-17).
- ★ **이 리뷰의 thesis:** DPE의 미세구조가 **소재·공정의 결합(co-shaped, bi-directional interplay)**으로
  형성된다는 점을 비판적으로 검토. 타깃 소재설계가 공정한계를 완화하고, 반대로 진보된 공정전략이 소재제약을
  수용하는 **양방향** 관계를 강조. → "unified, microstructure-driven perspective bridging materials
  chemistry with process design."
- **Wider impact 박스:** 기가팩토리 스케일·지속가능 제조 관심↑ → DPE가 유망 플랫폼(독성용매 제거 +
  에너지집약적 건조 제거). DPE는 WPE와 달리 **소재·공정만으로 결정되지 않는, 둘의 결합 interplay가 빚는
  distinctive 미세구조**를 가짐 → **후막 전극에서 특히 성능·신뢰성에 critical**. DPE 제조를 **4단계(mixing,
  kneading, laminating, calendering)**로 분류하여 **주요 결함(non-uniformity, delamination,
  heterogeneous densification)의 기원**을 규명하고 완화전략 제안. → **materials chemistry ↔ process
  engineering ↔ microstructure ↔ performance를 잇는 practical framework.**

---

## 2. DPE의 장점과 제조법 (§2, p.3150-3153)

### 2.1 건식공정의 장점 vs 습식 (§2.1)

**(A) 환경 지속가능성 & 비용 — ★ 핵심 정량 DPE 사실 (positioning에 직접 인용):**
- **습식(WPE)** 4단계: (1) slurry mixing → (2) slurry coating → (3) **drying** → (4) calendering. +
  NMP 같은 독성 유기용매 회수공정 필수.
- ★ **drying + solvent recovery가 full-cell 제조 총에너지의 46.84%** 차지(가장 에너지집약). 상업
  스케일에서 **multi-zone 건조시스템(>100 m, 수십 개 convection oven, 수십~수백 ℃)** 사용.
- ★ **NMP 1 kg 회수에 최대 ~10 kWh** — 순수 NMP 잠열의 **약 45배**(폭발 방지 위해 대량 공기 가열·순환
  필요). 다단 증류탑 회수시스템은 blower·exhaust fan에 **최대 230 kW** 소비.
- ★ **건식공정(DPE)으로 전환 시:** 용매·건조·회수 제거 → (i) **장비 수 최대 30% 감소**, (ii) **CAPEX·OPEX
  각 약 20% 감소**, (iii) **전극 코팅속도 최대 20% 향상**, (iv) **CO₂ 배출: WPE ≈ 2.3 kg CO₂/kWh_전극용량,
  DPE는 이를 최대 60% 감소**(ref 30, 32-36). (Fig 1c·d 레이더 + Fig 1c/d 본문.)

**(B) 전극 미세구조 — ★ 미세구조 특징 어휘의 정의 (우리 출력과 1:1):**
- LIB 전기화학 성능은 **소재 고유물성뿐 아니라 전극 미세구조**가 지배. ★ **Critical 미세구조 특징:**
  1. **각 성분의 spatial distribution & morphology**(공간분포·형태),
  2. **AM과 CBD 사이의 interfacial contact**(계면접촉),
  3. **effective surface area for interfacial electrochemical reactions** (= ASA, 유효 활성표면적),
  4. **tortuosity of ion percolation pathways**(이온 퍼콜레이션 경로 우회도),
  5. **continuity of electronic conduction networks**(전자 전도망 연결성).
  → 이 5개가 **rate capability, cycle life, energy density, safety**를 집합적으로 결정(ref 16,22,37-39).
  **★★ 이 5개 항목이 우리 DEM+MPM 출력과 정확히 1:1 (positioning §의 심장 — 아래 §8 표).**
- WPE는 건조 중 **CBD migration → 비균일 CBD**(특히 두께방향). 이 부피큰 CBD 응집체가 **Li⁺ 경로 차단 +
  tortuosity↑ → rate↓**(ref 40-42). DPE는 PTFE 피브릴화 → **연속 fibrillar network → pore-blockage↓ +
  well-connected Li⁺ 전도경로 + rate↑**. ★ **이 fibril 망 덕에 binder 함량 <1 wt%에서도 self-standing
  전극 가능** → 비활성 성분 비율↓ → 에너지밀도↑ (ref 15,57).
- 후막에서 WPE는 **edge elevation(in-plane 비균일), through-plane CBD migration, 건조 crack/delamination**에
  취약 → DPE는 무용매라 본질적으로 완화 → **후막·고로딩 전극에 DPE가 적합**(ref 20). (Fig 1e: WPE vs DPE의
  seamless ion percolation/larger ASA, less inactive comp, thick-electrode 적합성 3-패널.)

**(C) 후막·고로딩 동기 — ★ 정량 DPE 사실:**
- ★ **양극 mass loading 20 mg/cm²(전극밀도 3.5 g/cm³에서 ~75 µm) → 70 mg/cm²(~200 µm)로 증가** 시:
  - **비활성 성분(집전체+separator) 비율 약 21% → 6%로 감소**,
  - **gravimetric energy density 475 → 541 Wh/kg로 증가**(양극+집전체만 고려한 추정).
  → 후막 전극이 kWh당 제조비↓ + 에너지밀도↑의 유망 경로. 단 WPE로는 위 결함들 때문에 후막 구현 어려움
  → **DPE가 후막의 enabler**(ref 18-20).

### 2.2 DPE 대표 제조법 (§2.2, Fig 1f)

세 가지 대표법 + 역사적 발전(Fig 1f 타임라인):
1. **★ Maxwell/PTFE fibrillation (가장 널리 구현):** PTFE의 전단-피브릴화로 **무용매 연속 fibrous binder
   망** 형성 → AM+도전재를 물리적으로 entangle/bind. 단계: (1) powder mixing(planetary/ball/high-energy
   shear mixer로 PTFE+AM+도전재 dry mixing) → (2) **kneading(PTFE 피브릴화)**, key params = shear rate·
   temperature·kneading time → robust 3D PTFE fibrillar network → (3) dough-like composite/partial dry
   sheet를 집전체(보통 primer-coated Cu/Al)에 laminate → (4) roll pressing + calendering으로 최종
   densification(두께·밀도·loading 정밀제어). ★ **binder <1 wt%에서도 free-standing/ultra-thick 전극 +
   고에너지밀도**(ref 15,57). 역사: 1970 porous membrane via PTFE fibrillation 개념(Gore) → 1997 LiFePO₄
   DPE with PTFE → 2008 Maxwell Technologies 특허출원 → 2022 **Tesla Model Y용 PTFE DPE 대량생산** → 2023
   R2R. **R2R 호환성·산업 적용성 최강.**
2. **Melting extrusion:** 열가소성 binder(PVdF, PVdF-HFP, PEO, PP, paraffin wax, polyaniline) + AM +
   도전재를 가열 압출기에서 용융·혼합·전단균질화 → 시트성형 → laminate → calender. 높은 binder 함량
   응용(기계적 유연 architecture)에 적합. **단 저 binder(<2 wt%)에서 균일분포·기계접착 어려움** → binder
   입경·shear rate·압출온도·체류시간 정밀제어 필수(ref 62). 역사: 2008 LiFePO₄ hot pressing → 2017
   Li₄Ti₅O₁₂ → 2022 R2R melting extrusion platform.
3. **Spray deposition:** 과립화 dry powder를 air/gas-driven nozzle로 집전체에 분사 → calender로 binder
   용융/fuse → 접착. electrostatic spraying으로 균일도·접착 개선; post-curing(thermal annealing/UV
   crosslinking) 가능. R2R 적합하나 **powder-granule morphology·flow·spray uniformity·layer thickness
   제어 어려움 → 비균일 mass loading/poor adhesion/inconsistent porosity** 위험(ref 31,50,51). 역사: 2004
   LiCoO₂ electrostatic spraying → 2020 NCM811 → 2023 R2R spray.

→ Fig 1f 레이더(scalability·tech maturity·electrode thickness·electrode density): **Maxwell/PTFE
fibrillation이 4축 모두 최고권**. melting extrusion은 ED·thickness 중간, spray는 maturity 낮음.

---

## 3. 확장형 DPE 제조의 도전과 전략 (§3) — ★ 4단계 공정 분류의 본체

> ★ **이 §3가 리뷰의 핵심 = 4단계(mixing → kneading → laminating → calendering) 공정 taxonomy.**
> 각 단계마다 **(미세구조 역할) + (발생 결함) + (완화전략: 소재-level + 공정-level)**을 정리.
> **Fig 2가 이 전체를 한 장에 요약**: 좌(Processes: mixing/kneading/laminating/calendering) ↔
> 중(Microstructural defects: non-uniformity / delamination / heterogeneous densification & crack) ↔
> 우(Materials: conductive additives / binders / active materials / current collectors).

### 3.0 3대 미세구조 결함 (Fig 2 중앙 패널)
1. **Non-uniformity(비균일):** 부적절한 mixing/kneading 전단 + 입경·형태·표면화학·열역학 차이 → 성분
   분포 비균일(특히 도전재·binder 응집). → 국소 전류밀도 불균일 → 전자/이온 병목.
2. **Delamination(박리):** 전극↔집전체 계면 접착 부족(PTFE는 화학결합 없이 mechanical interlocking만) →
   박리 → 접촉저항↑.
3. **Heterogeneous densification / crack(비균일 치밀화·균열):** calendering 중 응력 비균일 전달 → 국소
   과압축·void 잔류 → 입자균열(특히 다결정 secondary particle) + 밀도구배.

### 3.1 Powder mixing process (§3.1) — 미세구조 역할: 성분 균일분산
- **역할:** dispersant-assisted 분산 불가(무용매) → **mechanical mixing만으로 AM·도전재·binder 균일분산.**
  carbon은 van der Waals·π-π·고표면에너지로 본질적 응집 경향 → 분산 challenge.
- **결함:** carbon 비균일 분산(특히 CNT re-bundling — capillary force로 건조 중 재번들). PTFE 전단-피브릴화는
  기계강건성↑이나 process param 세심한 최적화 필요(PTFE 소수성).
- **핵심 사례 수치(Fig 3):**
  - **carbon nanotube(CNT) 고유 전기전도도 ~200 S/cm** ≈ **conventional carbon black(Super P ~29.6,
    Ketjen black ~23.2 S/cm)의 약 100배**(ref 36). 그러나 분산 불량 시 전극-level 이점 상쇄.
  - ★ **ozone-treated CNT(O-SWCNT) 사례(Fig 3a, ref 72):** ozone가 sp² 골격 손상 없이 **OH/carbonyl/
    carboxyl 작용기** 도입 → 분산 개선. **O-SWCNT-NCM 전극 압연 후 porosity 13.89% vs Super P-NCM
    20.90%**(Super P 부분응집 → porosity↑). **CNT-DPE σ_s,eff ≈ CB-WPE의 3.1배, tortuosity 36% 감소.**
    pre-dispersion(MWCNT를 CAM에 먼저 코팅, salt-out)으로 CNT 응집 완화 → AM fraction **최대 99.6 wt% +
    전극밀도 4.0 g/cm³**(ref 73, SC-NCA).
  - **PVP-MWCNT 사례(Fig 3c, ref 74):** PVP 고분자 사슬이 MWCNT 표면 흡착 → 응집 방지 → 균일 도전망.
    **areal capacity 8·10 mAh/cm² PCDPE가 MWCNT-only 능가.**
  - **binder-carbon composite(rGO@PTFE, Fig 3d, ref 79):** thioglycolic acid로 PTFE 나노입자를 rGO에
    anchoring → restacking 억제 + 피브릴화 촉진. **G@P_TC t_Li+ = 0.73(vs Super P-PTFE 0.43), areal
    15.2 mAh/cm² + volumetric 563 mAh/cm³.**
  - ★ **핵심 명제:** 도전재·binder 둘 다 균일분산 필수 — **CBD의 spatial distribution이 전자 퍼콜레이션망 +
    기계강건성을 동시에 결정**(ref 21-23,75-78). (Table 1: 도전재·binder 균일분산 전략 종합.)

### 3.2 Kneading process (§3.2) — 미세구조 역할: PTFE 피브릴화 정도 제어
- **역할:** PTFE 피브릴화 유도. **피브릴화 정도(degree of fibrillation)**가 미세구조·기계물성·이온/전자
  경로를 좌우. 피브릴화는 **PTFE 고유물성(M_W·입경·결정성) + kneading 조건(time·temp·feeding)**에 의존.
- **PTFE 고유물성 영향(Fig 4a-b):**
  - **입경(Fig 4a, ref 76):** pristine PTFE(L) 평균 492.31 µm → cryo-freezer milling 8 cycles
    87.73 µm(M) → 16 cycles 6.44 µm(S). ★ **작은 PTFE → 전하수송 저항↓ → 이온/전자 전도↑**(절연
    PTFE의 접촉면적 최소화). SAICAS로 PTFE(L)/(S) 접착거동 차이(75% depth).
  - **M_W(Fig 4b, ref 85):** high-M_W PTFE(H) → 응집↓ + 균일 섬유형태(긴 사슬이 fibril 형성·전파 지속).
    PTFE(H) 복합 cathode → 전자저항↓ + 접착↑. ★ **all-solid-state Li-In/LPSCl/NCM with PTFE(H):
    209.7 mAh/g + 97.4% retention @300cyc, high mass loading 22.5 mg/cm²** (← ★ ASSB+LPSCl+PTFE 직접
    사례! 우리 소재계와 일치).
  - **결정성(ref 86):** PTFE 가열 200℃ + 냉각속도 제어 → A-PTFE(amorphous)/SC-PTFE/C-PTFE(crystalline).
    XRD 확인. **A-PTFE → 기계강도↑ → interparticle contact loss 완화.** C-PTFE-NCM cathode: 171 mAh/g +
    84.1% @200cyc.
- **kneading 조건 영향(Fig 4c-e):**
  - **kneading time(Fig 4c, ref 55):** 5 min 피브릴화 시작 → 20 min 거의 완전 → **60 min over-kneading은
    fibril 파괴 → 기계무결성 손실.** F-104/F-208 binder는 고유물성 유사하나 extrusion ratio(36~1500)
    상이 → kneading torque 다름.
  - **temperature(Fig 4d, ref 77):** 30℃ 피브릴화 부족(virgin-like, 인장강도 0.43 MPa) → **80℃
    완전섬유화(인장강도 ~0.85 MPa)** → 135℃(>T_g) fibril이 film형으로 coalesce(과연화). ★ **80℃ 최적 =
    균일 PTFE/도전재 분포 → 연속 이온/전자 경로.** (Fig 4d: PTFE storage modulus vs T — virgin/fiber/film
    3영역.)
  - **multi-step fibrillation(Fig 4e, ref 88):** dual-fibrous(multistep grinding-kneading) → yarn-like
    thin + rope-like thick 2종 fibril 균일분포 → 거시·미시 균일 + 전기화학 성능↑. rope-like가 edge
    roughness↓ + cohesion/adhesion↑.
- **요약:** PTFE 고유물성 + 피브릴화 공정조건이 함께 **기계무결성 + 이온/전자 경로**를 지배. → beyond-PTFE
  binder 선택 + 피브릴화 공정 최적화 필수.

### 3.3 Laminating process (§3.3) — 미세구조 역할: 전극↔집전체 접착·기계무결성
- **역할:** 전극층과 금속집전체 사이 충분한 접착 → 기계무결성. **PTFE는 집전체와 화학결합 약함 →
  mechanical interlocking(피브릴화) 지배** → 본질적 저접착 → **현 collector 설계·표면개질 필요.**
- **PTFE 접착 한계 정량:** PTFE 표면에너지 ~18 mN/m vs **Al 집전체 ~40 mN/m** → 큰 차이 → 접착일↓ → 계면
  접착↓(ref 91,92). PTFE는 point-to-point contact만 → 접착면적 severely limited.
- **3.3.1 Current collectors(집전체, Fig 5a-d) — ★ 우리가 모델 안 하는 결함(delamination/adhesion)의 본체:**
  - **표면거칠기 효과(Fig 5a, ref 100):** TACC(traditional smooth Al, peel ~0.28 N) < EACC(etched
    honeycomb, ~6.88 N) < **PACC(porous-carbon-coated Al, 25.42 N).** ★ **PACC σ_s = 0.83 S/m(vs TACC
    0.25) + Li⁺ 확산계수↑ → 우수 전기화학.** (강한 계면접착 → 균일 전자경로.)
  - **anodization(Fig 5b, ref 101):** Al을 Al₂O₃ nanotube로 양극산화 후 top층 제거 → nano-embossed porous
    표면(NSA). XPS로 Al₂O₃ 제거 확인(순수 Al peak). **NSA peel 1.44 N/cm vs bare Al 0.30**(mechanical
    interlocking). AFM unbinding force 3.06e-9 → 6.79e-9 N, 접착에너지 2.18e-17 → 8.21e-17 J.
  - **plasma 표면활성화(Fig 5c, ref 108):** plasma로 PTFE에 OH 도입 → 비극성 PTFE를 극성으로 → 접착↑.
    AM(LFP/NCM) 결정구조 손상 없이 PTFE만 선택적 작용기화.
  - **in-situ crosslinking 계면결합(Fig 5d, ref 15):** graphite를 polydopamine(PD)+PAA로 코팅 → 건식
    80℃에서 **amide(-RNCO-) 결합** 형성 → 3D 상호연결망. DP-PD@Gr 87.1% / DP-xPDAA@Gr 84% @500cyc
    (vs DP-bGr 77.9%).
- **요약:** carbon coating·etching·plasma·crosslinking 전략으로 접착 개선 가능하나 **계면 접착·집전체 설계가
  후막 DPE의 critical factor.** ★ **이 절 전체가 우리 모델이 다루지 않는 "delamination/adhesion" 갭의
  literature 본체** (아래 §8 honest-gap).

### 3.4 Calendering process (§3.4) — ★★ 우리 압축(DEM/MPM)에 정확히 대응하는 단계
> **이 절이 우리 DEM+MPM 압축역학과 1:1 대응하는 핵심.** calendering = 우리 300 MPa 압축.

- **역할(다기능):** calendering은 (i) 전극밀도↑ → 전자연결↑·접촉저항↓, (ii) **AM 입자-입자 contact +
  집전체 접착 + 전자/이온 수송특성을 동시 결정**, (iii) **polymeric binder(PTFE) 피브릴화 continuation**
  (rolling/pressing의 전단응력이 PTFE fibril을 추가로 extend·align·redistribute → mechanically
  interlocking binder망 강화 + 입자안정화)(ref 32,111-113). → **calender 설계·운전 파라미터가 densification
  품질·기계 cohesion·전기화학 성능을 직접 연결.**

- **3.4.1 Densification(치밀화, Fig 6a-c):**
  - **두 mechanical regime(Fig 6a, ref 112):** **feed zone**(roll gap 진입, frictional force + 내부
    입자-입자 마찰 지배, roll 표면에 ~평행한 전단장 → 도전재·binder 재분배 + 피브릴화 촉진) → **nip zone**
    (전단 감소, 수직 압축응력 급증 → densification + consolidation). ★ **Gyulai et al.(ref 112): 효과적
    전극형성 = feed zone 전단 최대화 + nip zone 과압축 최소화**(전통 WPE calendering은 nip 전단 회피 →
    반대). **shear-dominant calendering이 binder 균일재분배 + 연속 fibril망 + 균일 밀도프로파일.**
  - ★ **bimodal AM packing(Fig 6b, ref 116, Hong et al.) — ★ 우리 Furnas dip + #266 직접 대응:**
    **큰 polycrystalline(PC) + 작은 single-crystalline(SC) 입자 블렌드 → interstitial void를 효율적으로
    채움 → 목표밀도 도달에 필요한 calendering pass 수↓.** ★ **이 치밀화는 입자균열이 아니라 geometric
    rearrangement로 진행 → unimodal PC 대비 기계손상 입자 비율↓.** bimodal 고유 packing density↑ →
    사이클 중 elastic spring-back 억제 → 입자-입자 contact + 전자 퍼콜레이션 보존 → 전자안정성·cycling↑.
    **★★ 이게 우리 Furnas dip(AM 70-85wt% porosity 최소) + #266(P:S 7:3 bimodal → tortuosity↓) +
    우리 12:4:1 size-ratio void-filling과 정확히 동일 물리.**
  - **LPSCl 사례(Fig 6c, ref 119, Kim et al.) — ★ ASSB+LPSCl 직접:** 기존 DPE는 calendering 전 mixed
    powder에 void가 널리 퍼져 sparse bulk → 외부압력이 heterogeneous powder bed를 통해 불균일 전달 →
    residual porosity + microcrack. ★ **Li₆PS₅Cl(LPSCl) + LiPO₂F₂ 첨가제 bi-functionalized 전극:
    bimodal 입경 + 전략적 void-fill로 균일 압력분포 → packing↑ + void/crack↓.** + LiPO₂F₂가 AM 표면에
    conformal LiF/Li_xPF_y 보호층 → chemo-mechanical 안정 + SE 분해 억제. ★ **"균일 densification이
    void 형성 억제 + 균일 응력전달 + DPE 전기화학 무결성의 prerequisite."**
- **3.4.2 Particle cracking(입자균열, Fig 6d-e):**
  - **calendering-induced cracking ≠ cycling-induced fracture**(별개). WPE는 슬러리건조 연속 binder가
    완충 → DPE는 solid-solid 직접접촉(AM·도전재·PTFE) → calendering 응력이 입자에 직접 전달.
  - **PTFE 점탄성 3-regime(Fig 6d, ref 122, Matthews et al.):** 초기 elastic → ductile flow(PTFE fibril
    network) → high-stress compaction(입자 재배열 제한 → AM 입자에 응력집중) → 국소 응력집중 + 밀집
    클러스터 내 입자균열 driving force. **binder 함량↑(0.5→4 wt% PTFE) → Young's modulus·yield stress
    비선형↑ → 소성변형능↓ → 다결정 secondary 입자 균열↑(입계 따라 전파).** (Fig 6d: 0.5 vs 4 wt% PTFE,
    energy-selective BSE + 입경분포 + 압축 중 normalized volume evolution + low/high yield strength
    소성거동 모식.)
  - ★ **균열은 dry processing의 불가피한 결과가 아니라 calendering 경로 수정으로 완화 가능**(ref 123,
    Embleton et al.): **저비점 무독성 용매(ethanol <3 wt%)를 PTFE binder에 미량 도입(SaB, solvent-assisted
    binder)** → 초기 PTFE/도전재 분산 개선 + transient lubricant → 외부 압축응력을 shear-dominant 변형으로
    재분배 → 입자 응력집중 억제. Cross-section SEM: 표준 DPE는 전 두께 균열, **SaB-DPE는 고로딩에서도
    다결정 NCM622 구형 형태 보존**(Fig 6e). → "particle fracture는 dry processing의 본질이 아니다."

---

## 4. 차세대 DPE용 advanced binder (§4) — beyond-PTFE

### 4.1 기존 PTFE binder의 도전(Fig 7a) — ★ 5대 한계
1. **Poor interfacial adhesion(저접착):** C-F 비극성 → 기계 interlocking만 → 박리.
2. **Poor electrolyte wettability(전해질 젖음성 부족):** 후막에서 전해질 침투↓ → tortuosity 이점 상쇄.
3. **Poor electrochemical stability(전기화학 불안정):** 저전위에서 PTFE **reductive defluorination**(낮은
   LUMO) → LiF + 사슬절단 → 음극 사용 시 **ICE↓**. (해법: FEC additive로 SEI, PEO 코팅으로 binder 전기적
   decouple — ref 127-129.)
4. **Non-uniform dispersion:** PTFE 응집 → 국소 이온/전자 병목.
5. **PFAS 규제:** PTFE는 PFAS군 → "forever chemical" → 환경 잔류·PFOA 우려 → 규제 강화 + EOL 재활용 어려움.
   → **beyond-PTFE 동기.**
- **functionalization(Fig 7c, ref 134, Won et al.):** post-fabrication electron-beam(EB) irradiation으로
  fibrillated PTFE에 -COOH/C=O 도입 → 소수성→전해질친화 → 젖음성↑ + 이온저항↓. mass loading 100 mg/cm²
  hyper-thick에서도 Li⁺ migration enabled. (Fig 7c: 6/10/48/90 kDy FT-IR + 접촉각 + 저항.)

### 4.2 Dual-binder & beyond-PTFE (PFAS-free) (Fig 8, Table 2)
- **Dual-binder:** PTFE(피브릴화 scaffold) + 보조 co-binder(기능 부여).
  - **PTFE/PAA(Fig 8a, ref 90):** PAA의 -COOH가 Al 집전체 native Al₂O₃의 -OH와 **수소결합** → 접착↑(순수
    기계 anchoring과 대비) + 젖음성↑ → 고밀도 후막(90 mg/cm², 15.6 mAh/cm²) 가능.
  - **PTFE/PVP(Fig 8b, ref 142):** PVP가 PTFE↔음극 직접접촉 억제 → PTFE 분해 완화 + inorganic-rich SEI →
    ultrahigh 10 mAh/cm² + ICE↑.
  - **PAA-g-CMC bollard-anchored(Fig 8c, ref 145):** multivalent 수소결합으로 PTFE fibril 고정 → binder
    응집 억제 → 90 mg/cm²·15.6 mAh/cm²에서 균일 응력·전하수송.
- **PFAS-free(beyond-PTFE):**
  - **Sericin(ref 148):** 재생가능 단백질 binder, 전단유도 fibril(거미줄형) → solvent-free fibrillation.
    Li-S cathode, PTFE 동등 성능.
  - **Parafilm(Paraffin+PE, ref 146, Kim et al.):** 열가소성, **피브릴화 없이** 저T_g flow로 mild pressure
    activation → primer-free 집전체 접착 + 균일 binder분포. 5-9 mAh/cm² 후막. 불소 없음 → wider stability
    window + PFAS 회피.
  - **SBR(ref 132):** sticky adhesive, high-pressure calendering 시 SEI(LiF-rich) → 10.6 mAh/cm² ultrahigh.
- (Fig 8d: PTFE/PVDF/Parafilm 구조·비용·환경(GWP)·공정 비교. **PTFE GWP 12,200·PVDF 9,420 vs Parafilm
  매우 낮음; 비용 PTFE 2,805 vs Parafilm 123 USD/kg.**)
- **Table 1(도전재·binder 균일분산 전략) + Table 2(dual-binder & PFAS-free 전략):** 조성·접근법·기능·셀구성·
  loading·areal·retention 종합. (대표: NCM811/NCM622/graphite/LFP/sulfur cathode 다수 — 대부분 Li-ion, 일부
  ASSB(ref 57·148).)

---

## 5. 요약·전망 (§5, Fig 9)

- **공정 관점:** mixing/kneading/sheet forming/calendering 각각이 미세구조를 결정. 비균일 mixing → 도전재·
  binder 분포 비균일 → 전자전도·기계강도 공간변동; 불충분 피브릴화 → 연속 fibrous망 실패 → cohesion↓ +
  계면접착↓; lamination/calendering → 치밀화·계면접촉이나 crack·밀도구배 유발(기계 compliance 부정합 시).
- **소재 관점:** PTFE 피브릴화는 M_W·입경·결정성에 본질적으로 의존; 도전재 dimension/표면에너지가 퍼콜레이션·
  접촉저항을 좌우; AM/binder 선택이 lamination/calendering 중 전기화학 안정·응력수용을 결정.
- ★ **결론 명제:** **"확장형·기계강건 DPE 제조는 통합된 material-process-microstructure engineering 문제다.
  공정경로와 소재설계를 동시에 최적화하고 전기화학 성능·제조성·지속가능성을 함께 고려해야만 DPE가 차세대
  배터리 제조의 cornerstone 기술이 된다."** (Fig 9: material innovations ↔ process innovations의 양방향
  interplay가 scalable robust DPE를 만든다는 통합 개념도 — 자동차+mixing/kneading/laminating/calendering/
  grinding 공정라인 + 도전재/AM/binder/집전체 소재.)
- **전망:** 후막·고로딩 DPE는 더 높은 binder 함량을 요구 → PFAS 부담↑ → dual-binder + PFAS-free(CNF,
  fibroin, non-fibrillating thermoplastic)로 전환.

---

## 6. 그림 한 장씩 — 무엇을 보이고 우리가 쓸 것

### 본문 Figures
- **Fig 1 (p.3152):** (a) 습식 WPE 4단계(slurry mixing/coating/drying/calendering) + multi-zone 건조시스템
  (>100 m) + solvent recovery. (b) 건식 DPE(powder mixing/kneading → laminating/calendering → sheet
  forming) + mixing/kneading 모식. (c,d) **레이더: WPE vs DPE의 carbon emission/OPEX/CAPEX/coating speed/
  required equipment**(각 metric WPE 100% 정규화 → DPE가 모두 안쪽=우수). (e) ★ **DPE vs WPE 미세구조
  이점 3-패널: seamless ion percolation/larger ASA · less inactive comp(WPE >3wt% vs DPE <1wt%) ·
  thick 전극 적합(WPE edge elevation/non-uniform CBD/delamination vs DPE flat edge/uniform CBD/robust).**
  (f) 3대 제조법 레이더 + 역사 타임라인(1970 Gore → 2022 Tesla Model Y). → ★ **DPE 공정·이점·미세구조특징
  전체 개념도(우리 positioning의 1차 근거).**
- **Fig 2 (p.3153):** ★★ **리뷰의 중심도 — Processes(mixing/kneading/laminating/calendering) ↔
  Microstructural defects(non-uniformity / delamination / heterogeneous densification & crack) ↔
  Materials(conductive additives 0D/1D/2D+functionalization / binders PVdF·PTFE+PVP/CMC/PAA/Gluten /
  active materials bimodal·crystalline·surface engineering / current collectors primer layer·surface
  etching).** → ★ **이 한 장이 우리 DEM(transport 결함)·MPM(densification 결함)·CBD additive·bimodal이
  덮는 영역 전체를 지도화. 우리 작업의 "어디에 꽂히는지" 시각 근거.**
- **Fig 3 (p.3155):** 도전재 분산 4-패널 — (a) **ozone CNT 표면개질**(O-SWCNT, porosity 13.89 vs 20.90%).
  (b) MWCNT를 SC-NCA에 salt-out wrapping(AM 99.6wt%·4.0 g/cm³). (c) PVP-MWCNT 분산. (d) rGO@PTFE
  binder-carbon 복합(t_Li+ 0.73). → 도전재 균일분산 전략(우리 CBD seeding 맥락).
- **Fig 4 (p.3159):** ★ PTFE 피브릴화 — (a) cryo-milled PTFE 입경(L 492→M 87.7→S 6.44 µm). (b) 시트형성
  + M_W별 피브릴화 모식·SEM(aggregated/initiated/fully fibrillated). (c) kneading time 형태변화(5/10/20/60
  min). (d) **PTFE storage modulus vs T(virgin/fiber/film 3영역)** + SEM. (e) multi-step fibrillation(yarn/
  rope fibril). → ★ **PTFE 피브릴 형태·공정의존(우리 `additives.py` PTFE fibril 모델 검증·확장).**
- **Fig 5 (p.3161):** 집전체·계면 — (a) carbon-coated Al(PACC peel 25.42 N·σ 0.83 S/m). (b) anodization
  NSA(peel 1.44 N/cm). (c) plasma 활성화. (d) crosslinking(PD/PDAA@Gr amide 결합). → ★ **delamination/
  adhesion 결함의 본체(우리 모델 갭).**
- **Fig 6 (p.3163):** ★★ **calendering = 우리 압축 — (a) feed/nip zone 모식(u₁≥u₂). (b) PC vs bimodal
  치밀화(bimodal이 적은 pass로 고밀도 + CB 균일분포). (c) LPSCl+LiPO₂F₂ bimodal void-fill(thick resistive
  vs dense dry; LiF/Li_xPF_y XPS). (d) 0.5 vs 4 wt% PTFE 입자균열(BSE+입경분포+압축 normalized volume
  evolution + low/high yield strength 소성거동). (e) 표준 DPE(전두께 균열) vs SaB-DPE(구형 보존).** → ★★
  **densification(MPM) + bimodal packing(Furnas dip/#266) + 입자균열(우리 fracture) 전부 직접 대응.**
- **Fig 7 (p.3165):** PTFE 한계 — (a) 5대 한계(저접착/젖음성/전기화학불안정/비균일/PFAS). (b) PEO 코팅으로
  PTFE 분해 억제(258.7 Wh/kg pouch). (c) EB irradiation functionalization(-COOH/C=O, 젖음성↑). → beyond-PTFE
  동기.
- **Fig 8 (p.3168):** dual-binder & PFAS-free — (a) PTFE/PAA(수소결합 접착). (b) PTFE/PVP(SEI 안정). (c)
  bollard-anchored dual-binder(분산). (d) **PTFE/PVDF/Parafilm 구조·비용·GWP 비교(PTFE GWP 12,200·비용
  2,805 vs Parafilm 123).** → beyond-PTFE 소재전략.
- **Fig 9 (p.3172):** ★ **통합 개념도 — material innovations(도전재/AM/binder/집전체) ↔ process
  innovations(mixing/kneading/laminating/calendering/grinding)의 양방향 interplay → scalable robust DPE.**
  → ★ **리뷰의 thesis 1장 요약(우리 작업이 채우는 "정량·예측" 자리).**

### Tables
- **Table 1 (p.3157-3158):** 도전재·binder 균일분산 전략 — 소재·surface modifier·접근법·기능·조성·loading·
  areal·voltage·C-rate·retention. (SC-NCA+MWCNT salt-out, NCM811+MWCNT Pickering, NCM811+SWCNT spray-dry,
  NCM+rGO@PTFE, LCO+MWCNT freeze-dry, NCMA+CB, NCM811+O-SWCNT ozone, NCM811+PVP-MWCNT 등 — Li-ion 다수.)
- **Table 2 (p.3169-3170):** dual-binder & PFAS-free — PTFE/PAA·PTFE/gluten-flour·PTFE/PAA-g-CMC·PTFE/PVdF·
  PTFE/PVP·PTFE/CMC + PFAS-free(Phenoxy resin·Parafilm·SBR·Sericin). 시스템·기능·접근·areal·retention.

---

## 7. 기술 미니용어집 (우리 맥락)

- **DPE / WPE:** 건식(PTFE 피브릴화, 무용매) / 습식(슬러리 코팅). 리뷰 전체 대비축.
- **PTFE fibrillation (Maxwell):** PTFE가 전단으로 섬유화 → AM+도전재 그물 결합. 우리 `additives.py` PTFE
  fibril(roll-shear-drawn 1D web, vol_conserve d∝√(V/L))이 이 메커니즘의 기하 모델.
- **CBD migration:** WPE 건조 중 carbon-binder가 두께방향 이동 → 비균일 응집(DPE에 없는 결함).
- **ASA (active surface area):** 유효 활성표면적. 우리 coverage/ASA에 대응.
- **Ion-percolation tortuosity:** 이온경로 우회도(낮을수록 좋음). 우리 τ_Laplace,eff/τ_Dijkstra + σ_ionic의
  C(τ) 항에 대응.
- **Electron-conduction continuity:** 전자경로 연결성. 우리 σ_e 접촉망(Kirchhoff) + CN(Z_AM-AM) + percolation에
  대응.
- **Feed zone / nip zone:** calendering의 전단지배(roll gap 진입) / 압축지배(densification) 영역. 우리 압축의
  rearrangement(전단) vs consolidation(수직압축)에 개념 대응. ★ **shear-dominant calendering = void-fill
  flow를 전단으로 유도 → 우리 MPM void-fill의 공정 해석.**
- **Bimodal packing (PC+SC):** 큰 polycrystalline + 작은 single-crystalline AM → void-fill → 적은 pass로
  고밀도 + geometric rearrangement(균열 없이). ★ 우리 Furnas dip + #266 P:S 7:3 + 12:4:1 size-ratio와 동일.
- **Calendering-induced particle cracking:** 압축 응력집중 → 다결정 secondary 입자균열(입계 전파). cycling
  fracture와 별개. 우리 fracture(Auerbach/Holm)·MPM 응력집중에 대응. SaB(ethanol lubricant)로 완화 가능.
- **Heterogeneous densification:** 불균일 압력전달 → residual void + 밀도구배. 우리 porosity(z) 구배(#286/
  Phase 5)에 대응.
- **Primer layer (PL):** 집전체↔전극 conductive-carbon+binder 박막(접착·도전). #286의 주인공; 이 리뷰는
  집전체 절(§3.3.1)에서 다룸. 우리 미모델(adhesion 갭).
- **beyond-PTFE / PFAS-free:** PTFE(불소·PFAS) 대안 binder(CNF/fibroin/Parafilm/SBR/sericin). 우리
  `additives.py`가 기하로만 모델하는 PTFE의 대안 맥락(binder 화학 미모델).
- **Defluorination:** Li⁺이 PTFE 환원 → LiF + 비정질탄소 → ICE↓(저전위). 우리 PTFE 상은 기계/부피만 모델 →
  이 전기화학 부반응 미반영(일반 LIB ICE 예측 시에만 관련; ASSB는 관련 낮음).

---

## ★ 8. 우리 DEM+MPM의 positioning vs 이 framework (이 리뷰의 핵심 활용)

> ⚠ **대전제:** 이건 **일반 Li-ion DPE 리뷰**다. 정량 셀 절대값(mAh/g·ICE·retention)은 Li-ion 맥락 →
> LPSCl ASSB 수치 앵커는 Bazzoun(#)/Varkey/Minnmann/#266이 담당. **이 리뷰에서 가져오는 것은 (a) 미세구조
> 엔지니어링 framework, (b) 4단계 공정 taxonomy, (c) 미세구조-특징 어휘, (d) 정성 DPE 사실/에너지%** — 이건
> **화학계 무관하게 DIRECTLY 전이**(DPE는 ASSB 양극 선도경로이기도 하고, 미세구조 물리는 공통). 우리 작업을
> **이 framework를 정량·예측하는 엔진**으로 자리매김하는 게 본 §의 목표.

### (A) ★★ THE KEY MAPPING — 그들 어휘 = 우리 출력 (1:1, positioning의 심장)

| 그들 (리뷰 어휘) | 우리 (DEM+MPM metric/도구) | DEM/MPM | 관계 |
|---|---|---|---|
| **공정: calendering** (densification) | **압축**: porosity, σ@300 MPa, contact area | DEM+MPM | **= 같은 물리** (calendering = 우리 300 MPa 압축) |
| **공정: powder mixing / dispersion** | **CBD seeding**: `additives.py` (SuperP 분산 vs VGCF 응집), dispersion CV | DEM(voxel) | **= 같은 단계** (분산 균일도) |
| 미세구조: **각 성분 spatial distribution/morphology** | particle 위치(scaffold), CBD morphology, MPM 소성 shape | DEM+MPM | 우리가 **예측·생성** |
| 미세구조: **AM–CBD interfacial contact** | **coverage** (cov_AM, Tabor 0.26µm / Hertz 0.13µm), AM-CBD contact | DEM(StageE) | **1:1** |
| 미세구조: **effective active surface area (ASA)** | coverage·접촉면적 + ASA, B3 표면거칠기 | DEM(StageE) | **1:1** |
| 미세구조: **ion-percolation tortuosity** | **τ_Laplace,eff / τ_Dijkstra** + σ_ionic의 C(τ) | DEM | **1:1** (단 그들 pore-τ, 우리 contact-τ — 쌍대) |
| 미세구조: **electron-conduction continuity** | **σ_e 접촉망**(Kirchhoff/Holm) + **CN**(Z_AM-AM) + **f_p/percolation** | DEM | **1:1** |
| 소재: **PTFE fibrillar network** | **`additives.py` PTFE fibril** (curl/vol_conserve/nucleate/branch/bridge) | MPM-seed | **1:1** (형태/기하) |
| 결함: **heterogeneous densification** | **porosity(z) 구배** (#286, Phase 5 z-band K=8) | MPM | **대응** (우리가 생성) |
| 결함: **non-uniformity** (분산) | **dispersion 균일도** (SuperP CV↓ vs VGCF CV↑, voxel carbon occupancy CV) | DEM(voxel) | **대응** |
| 결함: **particle cracking** (calendering) | **fracture** (Auerbach/Holm, σ_e/σ 감소) + MPM 응력집중 | DEM | **대응** (transport-side) |
| 소재: **bimodal AM (PC+SC) packing** | **Furnas dip** + P:S 7:3 + 12:4:1 size-ratio void-filling | DEM+MPM | **= 동일 물리** (#266·Fig 6b·ref 116) |
| 결함: **delamination / adhesion** | **(없음 — honest gap)** | — | ✗ 우리 미모델 |

→ ★★ **이 표 = 우리 DEM+MPM 전체가 정확히 이 리뷰가 정의한 미세구조 특징들을 출력한다는 증명.**
**리뷰는 이 특징들이 rate/cycle/energy/safety를 가른다고 정성 서술하고, 우리는 그 특징들을 압력·조성에서
정량·예측한다.** 논문 intro에서 "Nam et al. (2026)이 DPE 미세구조 엔지니어링의 5대 핵심특징(성분분포·AM-CBD
contact·ASA·ion-percolation τ·electron continuity)을 정의했고, 본 연구의 DEM+MPM은 이 5대 특징을 압축
압력·조성의 함수로 예측하는 정량 엔진을 제공한다"로 직접 인용 가능.

### (B) ★ WHERE WE ADD VALUE — DESCRIPTIVE 리뷰 ↔ PREDICTIVE 엔진

- **리뷰 = DESCRIPTIVE:** 필드를 surveys, 미세구조→성능을 **정성**으로 연결("작은 PTFE → 저항↓", "bimodal →
  적은 pass로 고밀도", "구배 → tortuosity↓"). 인과 메커니즘을 서술하나 **압력→미세구조→σ를 수치로 예측하는
  모델은 없음**(리뷰는 문헌 종합이지 솔버가 아님).
- **우리 DEM+MPM = PREDICTIVE:** **압력→미세구조→σ triad(ionic/electronic/thermal)**를 explicit 접촉망
  (Kirchhoff/Holm) + 소성 morphology(MPM J2 void-fill) + fracture(Auerbach)로 **정량·예측**. + scaling-law
  (σ_ionic LOOCV 0.975, σ_e 0.953, σ_thermal 0.90)로 design-knob→metric 압축.
- ⇒ ★ **우리 작업 = 이 리뷰의 framework를 위한 quantitative microstructure-engineering ENGINE.** 논문
  significance에 강력: "이 리뷰(Nam 2026)가 정의한 material-process-microstructure-performance 사슬에서,
  본 연구는 process(calendering=압축)→microstructure(porosity·coverage·τ·CN)→property(σ triad)의 정량
  예측 고리를 완성한다."

### (C) ★ frame[5] 분업 재확인 (DEM=transport / MPM=mechanics) — 리뷰가 두 반쪽을 모두 명명

이 리뷰는 우리 DEM·MPM 두 반쪽을 모두 어휘로 호명한다 → frame[5] 분업이 임의가 아니라 **필드가 인정한
미세구조 축**임을 입증:
- **DEM이 소유(transport):** ion-percolation τ, electron-conduction continuity, AM-CBD contact, ASA,
  CBD 분산 → 리뷰의 미세구조 특징 1·2·3·4·5 + 결함 non-uniformity. 우리 σ_ionic/σ_e/σ_thermal + coverage +
  CN + percolation이 정량.
- **MPM이 소유(mechanics):** densification(calendering), 소성 morphology(입자 shape change), void-fill flow,
  heterogeneous densification(porosity 구배) → 리뷰의 calendering §3.4 + heterogeneous densification 결함.
  우리 MPM J2 소성 + scaffold가 정량.
- **둘 다(cross-validate):** porosity, bimodal packing(Furnas dip), 입자균열(transport-side DEM + 응력장
  MPM). 리뷰의 bimodal(Fig 6b) + cracking(Fig 6d)이 양쪽.
- → ★ "DEM=transport, MPM=mechanics" 분업이 이 리뷰의 미세구조-특징 분류와 정확히 겹침 = **frame[5]의
  독립 framework 근거**(Varkey/Bazzoun이 frame[1]/[2]/[4]를 줬다면, 이 리뷰는 frame[5] 분업의 어휘적 정당화).

### (D) ★ honest GAPS — 우리가 안 하는 것 (리뷰가 강조하나 우리 미모델)

1. **Delamination / 전극↔집전체 adhesion (§3.3 전체):** ★ 리뷰가 **3대 결함의 하나**로 강조(PTFE point-
   contact·저표면에너지·집전체 표면개질). **우리 DEM+MPM은 전극 내부만 — 집전체 계면 접착·박리 미모델.**
   - 정직하게: 우리 `--coh`(SE cohesion)는 SE-SE 결합이지 전극-집전체 접착이 아님. → **delamination은 우리
     framework 밖**(향후 집전체 BC + 계면 접착에너지 항 추가 시에만). ASSB도 집전체 접착은 실재 문제이나
     우리 RVE는 bulk만. → 논문에서 **"본 연구는 bulk 미세구조에 집중, 집전체 계면 접착은 future work"**로
     명시(이 리뷰가 그 갭의 literature 근거).
2. **Kneading rheology / PTFE 피브릴화 동역학 (§3.2):** 리뷰는 피브릴화 정도를 M_W·입경·결정성·kneading
   time/temp의 함수로 다룸. **우리 `additives.py`는 피브릴화 결과(fibril web 형태)를 기하로 seeding할 뿐,
   피브릴화 과정(전단→섬유화 rheology)을 시뮬하지 않음.** (Lee 2025 디제스트에도 동일 caveat — 우리 RVE는
   film-roll-shear 단계 미재현.) → **PTFE 형태는 검증, 피브릴화 rheology는 갭.**
3. **Calendering 온도축 (feed/nip zone shear, §3.4.1):** 리뷰의 shear-dominant calendering(feed zone 전단
   최대화)은 **온도·roll-gap·전단장**의 함수. 우리 MPM은 압력/변위만(온도·점성·전단장 분리 없음). #285
   디제스트의 점탄성/온도 갭과 동일. → ASSB는 cold-press 표준이라 우선순위 낮으나, 후막 DPE calendering
   최적화엔 점탄성+온도 필요.
4. **PTFE defluorination ICE 손실 (§4.1):** 리뷰의 PTFE 전기화학 부반응(LiF·ICE↓)은 우리 PTFE 상이
   기계/부피만 모델하므로 미반영(일반 LIB 확장 시 ICE 항 후보; ASSB는 관련 낮음). #286 디제스트와 동일.

### (E) ★ ACTION items (이 리뷰가 직접 유도하는 우리 작업)

1. **positioning 인용 확정:** 논문 intro/significance에서 이 리뷰(Nam 2026, #276)를 **우리 DEM+MPM이 푸는
   미세구조 엔지니어링 framework의 정의**로 인용. 5대 미세구조 특징 ↔ 우리 5대 출력 1:1 표(위 (A))를
   significance 그림/표로.
2. **4단계 공정 어휘 채택:** 우리 문서/논문에서 압축을 **"calendering(densification)"**, CBD seeding을
   **"powder mixing/dispersion"**으로 명명 → 필드 표준 어휘와 정렬(reviewer 친화). 우리 dispersion 균일도
   metric(carbon occupancy CV)을 **"non-uniformity 결함 정량"**으로 프레이밍.
3. **bimodal/Furnas dip 서사 강화:** Fig 6b(ref 116, Hong) + Fig 6c(ref 119, Kim, **LPSCl+LiPO₂F₂**)를
   우리 Furnas dip + #266 P:S 7:3의 **공정-level(calendering void-fill) 근거**로 인용 — "bimodal packing이
   적은 calendering pass로 고밀도 + geometric rearrangement(균열 없이)"가 우리 dip의 calendering 해석.
4. **shear-dominant calendering ↔ 우리 MPM void-fill:** feed/nip zone(Fig 6a, Gyulai ref 112)의
   "shear-dominant densification"이 우리 MPM의 전단유도 void-fill flow의 공정 해석 → MPM 압축을 "nip-zone
   수직압축 + feed-zone 전단 재배열"로 서술.
5. **에너지% positioning 사실 채택:** drying 46.84% / NMP ~10 kWh/kg(45×) / CAPEX·OPEX −20% / 장비 −30% /
   coating speed +20% / CO₂ −60% / loading 20→70 mg/cm²(비활성 21→6%, 475→541 Wh/kg) — 논문 intro의 "왜
   DPE인가" 동기에 직접 인용(우리 작업이 DPE 미세구조를 정량하는 가치 강조). ⚠ Li-ion 맥락이나 DPE 일반
   사실이라 ASSB 양극 DPE에도 적용.

### 비교 요약표
| 축 | Nam 2026 리뷰 (Li-ion DPE) | 우리 (LPSCl ASSB DEM+MPM) | 이식/교훈 |
|---|---|---|---|
| 성격 | **DESCRIPTIVE** (필드 종합, 정성) | **PREDICTIVE** (압력→미세구조→σ) | ★ 우리 = framework의 정량 엔진 |
| 미세구조 특징 | 5대(분포·AM-CBD·ASA·τ·전자continuity) 정의 | 5대 = 우리 출력 1:1 | ★ positioning 심장 |
| calendering | 공정 서술(feed/nip, bimodal, crack) | 압축 정량(porosity·σ·coverage) | = 같은 물리 |
| mixing/분산 | non-uniformity 결함 서술 | dispersion CV (SuperP vs VGCF) | non-uniformity 정량 |
| PTFE | 피브릴화 메커니즘·M_W·결정성 | additives.py fibril 기하 | 형태 검증(rheology 갭) |
| bimodal | PC+SC void-fill(Fig 6b/c) | Furnas dip·P:S 7:3·12:4:1 | = 동일 물리 |
| delamination | ★ 3대 결함의 하나(집전체) | **(없음)** | ✗ honest gap |
| 우리 고유 | (없음 — 리뷰) | σ triad 예측 + 소성 morphology + fracture | 그들엔 정량·예측 없음 |

---

## ★ 9. 우리 작업에 넣을 가장 날카로운 인사이트 3가지

1) **이 리뷰는 우리 DEM+MPM의 "왜 이게 의미 있는가"를 통째로 정의한다 — significance의 backbone.**
   리뷰가 명시한 5대 미세구조 특징(성분분포·AM-CBD contact·ASA·ion-percolation τ·electron continuity)이
   **우리 출력과 1:1**이고, 리뷰는 이들이 rate/cycle/energy/safety를 가른다고 **정성** 서술한다. ⇒ 우리
   작업은 **"바로 이 리뷰가 정의한 미세구조 특징을 압력·조성에서 정량·예측하는 PREDICTIVE 엔진"**으로
   포지셔닝하면 된다(리뷰=descriptive, 우리=predictive). 논문 intro 한 문단 + significance 표(위 §8(A))로 직결.

2) **"calendering = 우리 압축"이 어휘적으로 확정 — 우리 압축역학을 필드 표준 용어로 재명명.**
   리뷰의 §3.4 calendering(feed/nip zone, shear-dominant densification, bimodal void-fill, 입자균열)이
   **우리 DEM+MPM 압축의 공정 해석 전체**다. 특히 **(a) shear-dominant feed-zone 전단 → 우리 MPM void-fill
   flow**, **(b) bimodal PC+SC void-fill(Fig 6b/c, ref 116/119, ref 119는 LPSCl!) → 우리 Furnas dip +
   P:S 7:3**, **(c) calendering-induced cracking → 우리 fracture**. ⇒ 우리 압축을 "calendering(densification)"
   으로 명명하고 dip을 "bimodal calendering void-fill의 geometric rearrangement"로 서술하면 필드 정렬 +
   reviewer 친화. (Fig 6 전체가 우리 압축 §의 literature 근거.)

3) **frame[5] 분업이 이 리뷰의 미세구조-특징 분류와 정확히 겹친다 — 분업의 독립 framework 정당화 + honest
   gap(delamination) 명시.** 리뷰가 transport 특징(τ·전자continuity·AM-CBD·ASA = DEM)과 mechanics 특징
   (densification·morphology·heterogeneous densification = MPM)을 **둘 다 핵심으로 명명** → 우리 "DEM=transport,
   MPM=mechanics" 분업이 임의 분할이 아니라 **필드가 인정한 축**임을 입증(Varkey/Bazzoun이 frame[1]/[2]/[4]를
   줬다면 이 리뷰는 frame[5]의 어휘적 근거). 동시에 리뷰가 강조하는 **delamination/집전체 adhesion**은 우리가
   **명백히 안 하는 갭** → 논문에서 "bulk 미세구조에 집중, 집전체 계면은 future work"로 정직히 한정(이 리뷰가
   그 갭의 literature 본체 §3.3).

### 보너스 실행 항목
- **#276 인덱스 갱신**(아래 완료): 6줄 스텁 → framework anchor 본문(4단계 taxonomy·에너지%·미세구조 5특징·
  positioning 매핑·honest gap)으로 대폭 확장. TIER-2 내에서 **positioning 최우선**으로 격상(우리 도메인 리뷰).
- ⚠ **혼동 금지:** 이 리뷰(#276)는 **framework/positioning** 공급원 — **수치 앵커가 아니다**. LPSCl σ/porosity
  수치 앵커는 Bazzoun(#)/Varkey/Minnmann/#266; z-구배 측정방법은 #286; CBD ion/electron trade-off는 #284;
  점탄성 spring-back은 #285. 이 리뷰는 그 모든 조각을 **하나의 미세구조 엔지니어링 framework**로 묶는 상위
  지도다.
- **에너지% 사실 인용 준비:** drying 46.84% · NMP 10 kWh/kg(45×) · CAPEX/OPEX −20% · 장비 −30% · coating
  +20% · CO₂ −60% · loading 20→70 mg/cm²(비활성 21→6%, GED 475→541 Wh/kg) — 논문 intro "왜 DPE/우리 작업이
  중요한가"에 직접.
