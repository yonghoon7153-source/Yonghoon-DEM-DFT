# Hong 2026 (Energy Storage Materials 86, 104930) — 황화물 복합양극 열화 메커니즘 (디지털트윈): Dry(PTFE) vs Wet(NBR) 바인더 ★우리 소재계(LPSCl+NCM)

> slug `hong2026_sulfide_cathode_binder_digitaltwin` · DOI `10.1016/j.ensm.2026.104930` · type `FEM·digital-twin` · digested `2026-07-28` · status ✅
>
> ⓘ **정본 승격 2026-07-28** — 원본 `claude/stoic-knuth-NObVQ:docs/lit_hong2026_sulfide_cathode_binder_digitaltwin.md`.
> 단일-서랍 규칙(CLAUDE.md)에 따라 이관 — 그전까지 DFT webapp 목록에 안 떴다.


**인용:** Seung-Bo Hong, Hyobin Lee, Young-Jun Lee, Choyeon Kim, Yong Min Lee\*, Un-Hyuck Kim\*,
Dong-Won Kim\*, "Unveiling degradation mechanisms of sulfide-based composite cathodes supported by
digital-twin modeling: Dry binder versus wet binder", *Energy Storage Materials* **86** (2026) 104930,
DOI 10.1016/j.ensm.2026.104930. © 2026 Elsevier. 접수 2025-12-01, 수정 2026-01-15, 게재확정 2026-01-26,
online 2026-01-27. Hanyang Univ.(Chemical Eng. + Battery Eng.) + DGIST(Energy Science) + Yonsei Univ.
(Chemical & Biomolecular Eng.). 교신 yongmin@yonsei.ac.kr(Y.M.Lee) · unhyuck.kim@dgist.ac.kr(U-H.Kim)
· dongwonkim@hanyang.ac.kr(D-W.Kim). 지원: NRF Korea(RS-2024-00454354, RS-2025-18072968). 이해상충 없음.
**연세대 DTBL(이용민) 그룹 #271** — `docs/literature_yonsei_dtbl_2026.md` TIER-1 항목 갱신본.
디지털트윈 모델러 = **Hyobin Lee**(공동 1저자, #262/#285도 참여).

**소재계:** ★★ **Li₆PS₅Cl (LPSCl) 황화물 SE + NCM 활물질(NCM, L&F Co.) 복합양극(ASSLB)**.
**우리와 정확히 같은 소재계** (Bazzoun #와 동일, Varkey 할라이드와 다름). 바인더 = **PTFE(Solvay,
dry process)** vs **NBR(Kumho Petrochemical, wet process)**. SE = **두 종 LPSCl(d₅₀ = 1 µm AND 3 µm,
Jeong Kwan Co.)**. 도전재 = **Super C(Timcal)**. 음극 = **Li-In**(pressiometry는 zero-strain **LTO**).
용매 = **butyl butyrate**(약극성, NBR 용해 + LPSCl 부반응 최소화).

DB 동반: 이 논문의 LPSCl 양극 데이터는 **우리 소재계라 σ_ionic·porosity 절대 앵커 후보** —
`docs/data/densification_porosity_db.csv`(porosity@P) + `docs/data/bazzoun2026_sigma_ionic.csv` 동급
σ_ionic 앵커. 후보 행은 §11에 나열(직접 추가하지 않음, 유저 결정). 머신판독불가 자료(동영상 등) 없음.

---

## ★ 한 문장 결론 — 이게 무엇이고 우리에게 왜 결정적인가

**바인더의 공간분포·계면접착이 황화물 ASSB 복합양극의 열화경로를 지배한다.** **PTFE(dry)**는 섬유상
망(fibrillar network)이 **좁은 계면영역에 confined(국소·최소 coverage)** → 연속 Li⁺ 경로 보존 +
void 형성 최소 → 우수 cycling. **NBR(wet)**은 **깊이 침투·광범위 3D coverage** → Li⁺ 차단 + 계면 void
성장 가속 + LPSCl 산화분해(rock-salt 전환) 가속 → 급속 열화. **3D 디지털트윈**(GeoDict GrainGeo로 측정
파라미터→가상 미세구조 재구성 → ConductoDict FV로 이온 current density·SE coverage 시뮬)으로 메커니즘
정량화.

**★ 우리 hook(가장 중요 — 이건 #284/#285처럼 "개념만 전이"가 아니다):**
이 논문은 **우리 정확한 소재계(LPSCl SE + NCM CAM, ASSB)**이므로 **σ_ionic·porosity·retention 절대값이
전이 가능** → **검증 앵커**가 된다(반면 #284 SiOx·#285 단결정NCMA·#286 흑연은 액체 LIB라 절대값 비전이).
구체적으로:
- **(A) σ_ionic 절대 앵커 추가:** LPSCl 양극의 σ_ionic = **Pwd 0.087 / S-Pwd 0.079 / PTFE 0.064 /
  NBR 0.042 mS/cm** (Table S2). 이건 **Bazzoun(0.137/0.101/0.065 @ f_CAM 70/75/80)** 에 이은 **2번째
  LPSCl+NCM 실측 σ_ionic 데이터셋** → 우리 audit #1(현재 Bazzoun 1점 외삽만)을 **다점화**한다.
- **(B) PTFE의 void-최소화 = 우리 audit #5가 놓치는 양(陽)의 역학효과:** 우리는 PTFE를 **σ=0 obstacle**
  로만 모델 → PTFE의 **기계적 void-억제(densification 도움) 역할이 빠져 있다**. 이 논문은 PTFE가 pore
  volume을 **28.7→22.3 vol%**로 낮추고(Pwd→PTFE) NBR은 29.4 vol%로 키운다는 **정량 증거**를 준다.
- **(C) NBR은 우리 모델에 없음:** 우리는 wet/NBR 공정을 안 다룬다 → NBR 관련은 process-specific(비전이).
- **(D) 디지털트윈 = GeoDict 기반 reconstruct-from-measurement(출력단):** 우리 DEM+MPM은 **공정→구조 예측
  (입력단)**. `docs/positioning_vs_geodict.md`의 superset 논지를 **이 그룹의 또 다른 GeoDict 사례**로 재확인.

---

## 1. 배경 / 동기 (Introduction, p.1–2)

- EV 전환 → 고에너지·고안전 전지 필요. LIB는 액체전해질의 인화성·고로딩 한계 → **황화물 ASSLB**가 차세대.
  복합양극이 에너지밀도·cycling을 좌우 → **양극 제조법**이 핵심.
- 두 주류 제조법:
  - **Dry process(무용매 건식):** PTFE 바인더. 용매노출 회피 → **LPSCl 고유 이온전도도 보존**. PTFE는
    전단력 하 **선형 섬유망(fibrillar)** 형성 + 화학 불활성.
  - **Wet process(슬러리 습식):** NBR 바인더. 기존 LIB 인프라·노하우 활용. **그러나 LPSCl가 유기용매에
    분해되기 쉬움** → 약극성 용매(butyl butyrate)로 바인더 용해성 ↔ 부반응 억제 균형.
- ❗ **미해결 질문:** wet 공정 양극의 열화가 **(1) 용매유발 분해**(solvent-induced decomposition)인지
  **(2) 바인더 고유의 공간·화학적 거동**(deep infiltration, spatial heterogeneity)인지 불명확.
- **본 연구(명시):** PTFE/NBR을 대표 바인더로, **전기화학 측정 + 형태 분석 + 디지털트윈**을 결합해
  바인더 특성·용매상호작용·양극열화의 복합 상호관계 해명. ★ **4개 구성(2 reference + 2 binder)으로 용매효과
  와 바인더효과를 decouple.**

---

## 2. 소재 & 4개 양극 구성 (Experimental, §4, p.10 + Fig S2)

### 2.1 ★ 4개 양극 구성 (Fig 1a, Fig S2) — 용매↔바인더 decouple 설계
| 구성 | 조성 | 용매노출 | 바인더 | 역할 |
|---|---|---|---|---|
| **Pwd** (pristine powder) | NCM + **pristine LPSCl** + Super C | ✗ | 없음 | baseline (무용매·무바인더) |
| **S-Pwd** (solvent-exposed powder) | NCM + **S-LPSCl**(butyl butyrate 노출) + Super C | ✓ | 없음 | **용매효과만** 분리 |
| **NBR** (wet process) | NCM + **S-LPSCl** + Super C + **NBR** | ✓ | NBR | wet 공정 (용매+바인더) |
| **PTFE** (dry process) | NCM + **pristine LPSCl** + Super C + **PTFE** | ✗ | PTFE | dry 공정 (바인더만) |

→ **S-Pwd vs Pwd = 순수 용매효과**; **NBR vs S-Pwd = NBR 바인더효과**; **PTFE vs Pwd = PTFE 바인더효과**.
이 분리설계가 "용매 vs 바인더 중 무엇이 지배하는가"를 답하는 핵심.

### 2.2 제작 (§4.2, p.10)
- **PTFE 양극(dry):** NCM : LPSCl : Super C : PTFE = **75 : 22.5 : 1.5 : 1** wt%. 막자사발 혼합 30 min →
  roll-press(WCRP-1015HG)로 PTFE **피브릴화** → cohesive sheet. **활물질 mass loading = 30 mg/cm²**.
- **NBR 양극(wet):** NBR 용액(butyl butyrate 중 5 wt% NBR) 준비 → 양극 슬러리(NCM : LPSCl : Super C =
  **75 : 22.5 : 1.5**, wt 기준) cast(carbon-coated Al, 70°C 12h) → NBR 첨가. PTFE와 동일 loading.
- **Pwd / S-Pwd(binder-less):** Pwd = NCM : LPSCl : Super C = **75 : 23.5 : 1.5**. S-Pwd = LPSCl를
  butyl butyrate에 **overnight 사전노출 후 건조**한 S-LPSCl 사용.
- **셀 조립(ASSLB):** LPSCl(d₅₀=3 µm) 분말을 **80 MPa**로 펠릿화 → 양극 3종을 펠릿 위에, **350 MPa**로 압착
  → Li-In 음극(반대편) + Ni foil 집전체 → **30 MPa 토크 고정**. 글러브박스(MBRAUN, O₂·H₂O < 0.1 ppm).
- **Pressiometry용 LTO:** LTO : LPSCl : Super C = **60 : 39 : 1** wt%, N/P = 1.3.

### 2.3 측정 (§4.3–4.4, p.10)
- **σ_ionic:** Li/LPSCl/cathode/LPSCl/Li 셀, **AC 임피던스, 10 mHz–1 MHz** (full-blocking).
- **σ_electronic:** SUS/cathode/SUS 셀, **DC법**(전류 점증).
- **Pressiometry(operando):** LTO 음극 + SE 펠릿 + 양극, 압력센서 실시간 + battery cycler. **Δ(ΔP)_Q =
  Δ(ΔP)/Q_Discharge** [MPa·g·(A·h)⁻¹] = 단위용량당 압력변화 = 부피팽창 지표.
- **EIS(potential-dependent):** 1st formation cycle 중 충전 3.1/3.5/3.7 V, 방전 3.5/3.1/2.7/2.4 V에서
  5-min rest 후 측정. **등가회로 = Fig S9** (아래 §6).
- **GITT(cycle-resolved):** 특정 사이클(10/20/50/100th)에서 적용 → D_Li(NCM) 계산(식 §4.4).
- **Cycling:** formation 2 cycle @0.05C(1C = 4.5 mA/cm²), 3.7 V CC → 0.05C cutoff, **0.33C** retention test.
- **분석:** SEM(Verios G4) + cross-section polisher(ArBlade 5000) / ToF-SIMS(IONTOF, Bi³⁺/Bi³⁺⁺) /
  SAICAS(Daipla Wintes, 다이아블레이드) / XPS(Thermo, S 2p 분해상태) / HR-TEM+FIB+SAED(rock-salt 진단).

### 2.4 ★ 디지털트윈 (§4.5, p.10) — GeoDict 기반, reconstruct-from-measurement
**전부 GrainGeo 모듈(GeoDict 2024)의 object-based stochastic generation으로 가상 생성.** 핵심 디테일:
- **NCM:** convex spherical, **5 g/cm³**, **표면적을 실측 BET와 매칭**, 3D 도메인에 **random 분포**,
  voxel **0.2 µm**.
- **LPSCl:** polyhedron-shaped, **1.86 g/cm³**, **잔여 pore 공간에 채움**.
- **Super C(CBD):** spherical, **1.6 g/cm³**, 잔여 pore에 채움.
- 생성 미세구조 → uniform voxel grid 이산화.
- ★ **이온 current density 시뮬 = ConductoDict 모듈, Finite Volume Method**(지배 transport eq를 격자에서
  풀이). 상·하면 **전위차 1 V** 인가 → 구조 전체 이온 current density.
- ★★ **각 모델의 내부 형태(coverage)는 실측 σ_ionic로 calibration** → "시뮬과 실제 양극성능의 일관성 확보".
  즉 **σ_ionic는 입력**(Table S2 실측값을 모델에 주입), coverage·current density 분포가 출력.
- 같은 방법론 = 그들 선행 ref [13,56](= #266/digital-twin 계열) 답습. **= 이 그룹의 GeoDict 활용**(Bazzoun
  RNM과 다름; #281 ConductoDict/DiffuDict, #286 τ/PNM, #284 W_adh, #275 PNM과 동일 GeoDict 라인).

---

## 3. 핵심 메커니즘 — PTFE confined-minimal vs NBR extensive-deep (Fig 1a, Fig 6a)

**(1) PTFE(dry) = 좁고 confined한 섬유망 → 연속 Li⁺ 경로 보존.** PTFE는 전단력 하 **선형 fibrillar
network**로 변형, **상대적으로 좁은 계면영역에 confined**(Fig 1a 우측 "Minimal coverage"). LPSCl
입자를 거의 방해 안 함 → Li⁺ 전도경로 연속성 유지 + interparticle 접착으로 구조 무결성.

**(2) NBR(wet) = 깊이 침투·광범위 coverage → Li⁺ 차단.** NBR은 복합양극 안에 **균일·광범위 분산**되어
**활물질–SE 계면에 깊이 침투**(Fig 1a 좌측 "Extensive coverage"). 비전도성 폴리머가 큰 부피분율을 차지 →
**Li⁺ percolation 차단** + 직접 Li⁺ flux 형성 방해 → σ_ionic 최저(0.042 mS/cm).

**(3) ❗ 핵심 통찰 — 용매효과는 minor, 바인더 공간분포가 dominant.** S-Pwd(용매만)는 Pwd 대비 **moderate
한 손실만**(retention 92.0→87.1%, σ_ionic 0.087→0.079) — XRD 결정구조 변화 없음(Fig S6), AC 임피던스로
LPSCl σ가 **1.87 → 0.53 mS/cm**(28% 잔존)로 **moderate 감소**(Fig S7). 반면 NBR(바인더+용매)는 **severe
한 열화**(retention 85.4%, σ_ionic 0.042). ⇒ **"NBR 양극의 급속 열화는 주로 비전도성 바인더의 광범위
공간분포 탓이지 용매노출 탓이 아니다."**

**(4) NBR의 자기가속 열화 cascade(Fig 6a):** NBR coverage → 계면 void 형성 → **비균일 계면접촉** →
국소 응력집중 → **LPSCl 산화분해**(brittle byproducts, Young's modulus↑) → 추가 균열·void → 더 많은
산화분해 → **self-accelerating cascade**. PTFE는 confined fibril → void 최소 → 이 cascade 차단.

**(5) 향후 wet-bias 설계지침(2가지):** ① **spatial confinement**(이온차단 최소화), ② **충분한 계면접착**
(void 형성 억제). 그들 선행 **EMG 바인더**[ref 17, S6]가 이 두 조건을 만족(NBR보다 confined + 강접착) →
PTFE급 성능 접근(Fig 6b, Fig S25).

---

## 4. 섹션별 결과 — 모든 수치 (Results & Discussion, §2, p.2–9)

### 4.1 초기 cycling·rate·전도도 (Fig 1, Table S1, Table S2)

**초기 충방전(Fig 1b, 0.05C formation):** PTFE가 가장 높은 방전용량. NBR이 가장 낮음. (전압곡선 Fig S4.)

**★ Cycling retention(Fig 1c, 100 cyc @0.33C; Table S1):**
| 구성 | 1st formation(0.05C) 방전용량 (mAh/g) / Eff. | 1st(0.33C) 방전 / Eff. | 100th 방전 / Eff. | **Retention(%)** |
|---|---|---|---|---|
| **Pwd** | 211.7 / 92.1% | 182.9 / 89.3% | 168.3 / 99.8% | **92.0** |
| **S-Pwd** | 210.7 / 91.5% | 179.6 / 88.4% | 156.5 / 99.8% | **87.1** |
| **NBR** | 199.4 / 87.4% | 147.3 / 82.3% | 125.8 / 99.8% | **85.4** |
| **PTFE** | 212.8 / 91.6% | 175.1 / 87.4% | 165.7 / 100.0% | **94.6** |
- ★ **순위: PTFE 94.6 > Pwd 92.0 > S-Pwd 87.1 > NBR 85.4%**. PTFE가 **무바인더 Pwd보다도 높음**(접착으로
  구조무결성↑). NBR이 최악(초기 0.05C 용량부터 Pwd 대비 12 mAh/g 낮고, 0.33C 용량·retention 모두 최저).
- S-Pwd(용매만) = 87.1% → Pwd 대비 4.9%p만 감소(**moderate** = 용매효과 작음). NBR이 그보다 더 낮음 →
  추가 손실은 바인더 공간분포 탓.

**★ Rate capability(Fig 1d, 0.1→2C):** **PTFE > Pwd > S-Pwd > NBR**. NBR이 PTFE는 물론 S-Pwd보다도 낮은
rate → 바인더 형태·분포가 이온수송에 큰 음의 영향. S-Pwd는 cycling은 나쁘나 rate는 PTFE 다음 정도(용매효과
는 rate보다 cycling에 더 타격). (전압곡선 Fig S5.)

**★★ σ_ionic / σ_electronic(Fig 1e, **Table S2**) — ★우리 절대 앵커:**
| 구성 | **Li⁺ σ_ionic (mS/cm)** | σ_electronic (mS/cm) |
|---|---|---|
| **Pwd** | **0.087** | **1.11** |
| **S-Pwd** | **0.079** | **1.07** |
| **NBR** | **0.042** | **0.85** |
| **PTFE** | **0.064** | **1.10** |
- ★ **σ_ionic 순위: Pwd 0.087 > S-Pwd 0.079 > PTFE 0.064 > NBR 0.042 mS/cm**. NBR이 압도적 최저(Pwd의
  48%). PTFE는 무바인더 대비 ~26% 손실(0.087→0.064)이나 NBR(52% 손실)보다 훨씬 양호.
- σ_electronic은 모두 ~0.85–1.11 mS/cm로 **이온보다 변화 작음**(NBR만 0.85로 약간↓). → **바인더 효과는
  주로 이온 차단**(전자는 Super C 망이 지배, 바인더 영향 작음). NBR·PTFE 둘 다 전자절연·이온무시 폴리머
  (Fig S10 주석 [S3]) → 이들 영향은 직접 전하수송이 아닌 **공간분포·미세구조 역할**에서 옴.

**★ LPSCl 고유 σ_ionic — 용매노출 효과(Fig S7, S6):**
- **pristine LPSCl σ = 1.87 mS/cm → butyl butyrate 노출 후 0.53 mS/cm (28% 잔존)**. ❗ **moderate 감소**
  (NBR 양극의 severe 열화를 설명하기엔 부족 → 바인더 공간분포가 추가 주범).
- XRD(Fig S6): pristine vs BB-exposed LPSCl **결정구조 변화 없음**(argyrite peak 유지) → 용매가 결정을
  파괴하진 않음(표면 σ만 moderate 저하).
- XPS S 2p(Fig S23): pristine·BB-exposed 둘 다 argyrodite PS₄³⁻ 우세, **노출만으로는 sulfate(SO₄²⁻)
  미생성**(아래 §4.4 사이클 후와 대비 — 분해는 cycling이 trigger).

### 4.2 ★ 디지털트윈 — coverage·current density·porosity (Fig 2, Fig S11–S15)

★ 핵심 — **GeoDict GrainGeo 재구성 + ConductoDict FV로 coverage·이온 current density·pore volume 정량.**

**3D 디지털트윈 구조(Fig 2a, Fig S11 for S-Pwd):** AM(회색) + LPSCl(노랑) + S-LPSCl + CBD(파랑)을
실측 조성·BET·porosity 매칭으로 재구성.

**★ 활물질 표면 coverage(Fig 2b 2D 단면 + Fig 2c 막대) — LPSCl vs CBD:**
| 구성 | **LPSCl coverage of AM (%)** | **CBD coverage of AM (%)** |
|---|---|---|
| **Pwd** | **35** | **5** |
| **NBR** | **26** | **27** |
| **PTFE** | **36** | **9** |
- ★ **PTFE: LPSCl coverage 35→36%(↑), CBD 5→9%(소폭↑)** → LPSCl·CBD가 AM을 더 조밀·균일 packing(강접착
  cohesion → 더 효과적 이온접촉). PTFE의 confined fibril이 LPSCl 방해 안 함(negligible interference).
- ❗ **NBR: LPSCl coverage 35→26%(급감), CBD 27%(불균형 급증)** → NBR이 이온·전자 전도상을 **활물질 주위
  에서 재배치(displace)** → **활물질 표면의 부분 절연(partial insulation)** → 활성계면 disruption.
- ⇒ **NBR이 LPSCl(이온경로)을 AM 표면에서 밀어내고 비전도 CBD/바인더가 그 자리 차지** = σ_ionic 0.042의
  미세구조적 원인. PTFE는 반대로 LPSCl coverage 유지.
- (※ Fig 2 시뮬 LPSCl coverage 추세는 **실험 GITT(Fig S13)와 일치** = 모델 신뢰도 검증.)

**★ 이온 current density 분포(Fig 2d 3D + Fig 2e 2D, range 30–40 mA/cm²; Fig S14):**
- **NBR:** 연속 고-current density(>30 mA/cm²) 경로가 **형성 안 됨**(3D·2D 모두) → 바인더 분포가 만든
  이온수송 한계(LPSCl 화학분해가 아니라 **분포** 탓 — Fig S14b가 입증).
- **PTFE:** 좁은 바인더 분포 + 낮은 pore volume → **연속·robust 고-current 경로 형성**(Fig 2f, Fig S15).
- **S-Pwd:** NBR과 달리 **안정적 고-current 영역 유지** → S-Pwd의 이온수송 한계는 (NBR식 바인더분포가 아닌)
  용매유발이지만 그조차 minor → "NBR 열화는 바인더분포 탓"을 재확인.

**★★ Pore volume(Fig 2f 막대, Fig S15) — ★우리 audit #5 핵심:**
| 구성 | **Pore volume (vol%)** |
|---|---|
| **Pwd** | **28.7** |
| **NBR** | **29.4** |
| **PTFE** | **22.3** |
- ★ **PTFE 22.3% ≪ Pwd 28.7% < NBR 29.4%**. PTFE가 pore를 **6.4%p 낮춤**(densification 도움), NBR은
  **0.7%p 키움**. → PTFE의 좁은 바인더분포 + 높은 전극밀도 → **연속·robust 이온경로**; NBR의 광범위 occupation
  → 계면 void·disruption.
- **Fig S15b(target vs digital-twin 부피분율 검증):** AM/LPSCl/CBD 부피분율이 target과 거의 일치
  (Pwd AM 36.8/36.2, LPSCl 30.8/30.8, CBD 2.3/2.3; NBR AM 36.3/36.3, LPSCl 29.1/29.1, CBD 4.9/5.2;
  PTFE AM 40.9/40.8, LPSCl 32.8/33, CBD 3.7/3.9 — target/digital-twin) → 재구성 충실도 확인.

### 4.3 ★ Pressiometry·potential-EIS — void 형성과 계면저항 (Fig 3, Fig S16–S18, Table S3)

★ 핵심 — **PTFE가 부피팽창·계면저항을 정량적으로 억제**(operando 압력 + EIS).

**Operando pressiometry(Fig 3a, Fig S16 셋업, Fig S17 Pwd/S-Pwd):**
- **Δ(ΔP)_Q [MPa·g·(A·h)⁻¹] = 단위용량당 압력변화**(부피팽창 지표; LTO zero-strain 음극으로 양극만 분리).
- ★ **NBR = 1.99 vs PTFE = 1.74** → **PTFE가 부피팽창을 약 14% 더 효과적으로 억제**(1.99→1.74).
- **Pwd = 1.88, S-Pwd = 1.89**(Fig S17) → PTFE(1.74)는 무바인더 Pwd(1.88)보다도 ~8% 낮은 부피변화 →
  **PTFE 자체의 void-억제 능력**(접착이 입자연결 유지 → 팽창 흡수).

**Potential-dependent EIS — 계면저항 R₁(Fig 3b 2.7V·3c 2.4V Nyquist, Fig 3d 모식 + R₁; Fig S18, Table S3):**
- R₁ = **계면저항**(void 형성 + AM↔SE 계면 부산물; 등가회로 Fig S9 §6). Low-voltage(<3.0 V)에서 NBR/PTFE
  차이 뚜렷.
- ★ **R₁ @2.7 V: NBR 19.2 Ω vs PTFE 17.5 Ω**; **R₁ @2.4 V(완전방전): NBR 17.4 Ω vs PTFE 12.8 Ω**.
  → 방전 깊을수록 NBR R₁ ≫ PTFE. (Table S3 전체: charge 3.1/3.5/3.7 V = NBR 2.2/3.0/5.2, PTFE 1.4/2.9/5.2 Ω;
  discharge 3.5/3.1/2.7/2.4 V = NBR 3.4/3.2/19.2/17.4, PTFE 3.8/2.2/17.5/12.8 Ω.)
- ⇒ **NBR의 깊은 침투형태 → 계면 void → 계면접촉 불량 → R₁↑**; PTFE confined fibril → 연속 채널 보존 →
  R₁↓. (전기화학 부산물 차이가 아닌 **바인더 접착 차이**가 void 형성을 좌우.)

### 4.4 ★ 장기 열화 — void/crack·rock-salt·R₂(Fig 4, Fig 5, Fig S19–S24)

★ 핵심 — **NBR은 100사이클 후 광범위 void/crack + LPSCl 산화분해(rock-salt) + R₂(charge-transfer) 급증;
PTFE는 연속 채널·layered 구조 보존.**

**Cycling 중 EIS — R₂ charge-transfer 발산(Fig 4a 100cyc Nyquist, Fig 4b R₂; Fig S20 R₁):**
- R₂ = **charge-transfer resistance**(양극내 전하전달; 균열·rock-salt 생성으로 전자전도 저해·분극; Fig S9).
- ★ **R₂(NBR)는 10→100사이클 계속 급증**(Fig 4b 빨강, ~60→110 Ω), **R₂(PTFE)는 완만 증가 후 포화**
  (~25→40 Ω). NBR은 R₁·R₂ 둘 다 50사이클까지 증가 후 R₁ 포화·**R₂ 급발산** → "후반 transport 한계가
  활물질 안에서 출현 → NBR의 dominant 열화 메커니즘".
- **R₁(Fig S20):** NBR 10→100cyc 20→33 Ω(증가), PTFE 5–6 Ω 일정 → NBR 계면저항도 누적 증가.

**단면 SEM — void/crack(Fig 4c NBR / 4d PTFE, 100cyc; Fig S21 이진화):**
- ★ **NBR: 광범위 계면 void + crack**(Fig 4c 노란 점선 void + 빨간 화살표 crack, 5 µm scale) →
  solid-electrolyte 접촉 단절. **PTFE: 훨씬 적은 void, 연속 접촉 보존**(Fig 4d).
- Fig S21(Fig 4c/d 이진화): 검은 영역(void+crack)이 NBR(a)에서 압도적, PTFE(b)는 minimal.

**ToF-SIMS ⁷Li 분포(Fig 4e NBR / 4f PTFE, 100cyc 충전상태):**
- ★ **NBR 활물질 내부에 substantial ⁷Li 잔존**(높은 intensity) = **과도한 계면 void가 Li⁺ de-intercalation
  방해 → 활물질 내 Li trap → 비가역 용량손실**. **PTFE는 활물질 내 ⁷Li signal 거의 없음** = 효율적
  de-intercalation·계면무결성 보존.

**GITT D_Li(Fig 4g, Fig S22; 식 §4.4):**
- ★ **PTFE: D_Li 완만·점진 감소**(전 사이클 ~10⁻¹⁰ cm²/s 유지). **NBR: 50사이클 후 급가속 감소**
  (~10⁻¹² cm²/s까지 하락) → R₂ 급증과 직접 상관(계면열화↔이온수송 저하 연결).

**★ XPS S 2p — LPSCl 산화분해(Fig 5a NBR / 5b PTFE / 5c ratio; Fig S23):**
- as-prepared·1st cycle: 둘 다 argyrodite PS₄³⁻ + P-[S]ₙ-P(polysulfide) 우세, **sulfate(SO₄²⁻) 미검출**.
- ★ **100사이클 후 — NBR에만 SO₄²⁻(sulfate) 출현**(Fig 5a·5c). **Fig 5c 정량 비율(S 2p):**
  - **NBR:** 1st = P-[S]ₙ-P 16.4% → 100th = SO₄²⁻ **4.4%** + P-[S]ₙ-P **31.7%**.
  - **PTFE:** 1st = 12.2% → 100th = **17.1%** (SO₄²⁻ 없음).
  → **NBR에서만 LPSCl 산화분해(sulfate 생성)**. 이 분해 부산물은 pristine LPSCl보다 **σ↓·brittle·E↑** →
  추가 균열·void 전파 가속.

**ToF-SIMS SO⁻ 3D(Fig 5d):** NBR cathode에서 **SO⁻ signal intensity↑**(sulfate 축적) — XPS 확증.

**★ HR-TEM + SAED rock-salt 전환(Fig 5e–j NBR / PTFE, 100cyc; Fig S24 target area):**
- ★ **NBR(Fig 5e–g):** NCM 표면 lattice fringe **심하게 disrupted**, SAED에 **rock-salt 상 회절점** →
  표면 **17–22 nm** 깊이까지 구조 disorder(layered → rock-salt 전환). LPSCl 산화분해 부산물의
  inferior 전기화학·기계물성 → 인접 LPSCl 분해 가속.
- ★ **PTFE(Fig 5h–j):** lattice fringe 비교적 보존, **8–10 nm**의 얇은 재구성 층만, FFT는 bulk layered와
  epitaxial 연결 → **layered 골격 부분 보존**. ⇒ **PTFE confined fibril이 국소 strain 축적 완화 + 상전이
  전선(phase-transformation front) 내향 전파 지연**.

### 4.5 종합 메커니즘 (Fig 6)
- **Fig 6a 모식:** **NBR** = early cycle "Noticeable Void Formation" → long-term "Severe Interfacial
  Degradation + Pronounced Internal Crack". **PTFE** = "Minimal Void Formation" → "Preserved Interfacial
  Integrity + Slight Internal Crack".
- **Fig 6b(retention):** NBR < EMG[ref17] < Pwd < PTFE (PTFE 최고). EMG(distribution-controlled
  high-adhesion 바인더)가 NBR과 PTFE 사이 → 설계지침 검증.
- **Fig 6c(roadmap):** 차세대 wet-process 바인더 = **(1) spatial confinement(이온차단 최소) + (2) 강한
  계면접착(void 억제)** → "Robust Interfacial Adhesion + Surface Area Activation" → "Target"(PTFE급).
- **결론:** **바인더 형태·공간분포·계면접착이 황화물 ASSLB cathode 열화경로를 결정**한다. 용매노출이 아닌
  **바인더 유발 구조불안정**이 dominant cause.

---

## 5. 그림 한 장씩 — 무엇을 보이고 우리가 쓸 것

### 본문 Figures
- **Fig 1 (p.2):** (a) NBR(extensive) vs PTFE(minimal) coverage 모식. (b) 0.05C 초기 충방전. (c) ★
  **100cyc retention**(PTFE 94.6 > Pwd 92.0 > S-Pwd 87.1 > NBR 85.4%). (d) rate(0.1–2C; PTFE>Pwd>S-Pwd>NBR).
  (e) ★★ **σ_ionic·σ_electronic 막대**(Pwd 0.087/PTFE 0.064/NBR 0.042 mS/cm) → **우리 σ_ionic 절대 앵커**.
- **Fig 2 (p.4):** ★ 디지털트윈 핵심 — (a) 3D 디지털트윈 구조. (b) 2D 단면(AM 표면 LPSCl/CBD coverage).
  (c) ★ **AM coverage 막대**(Pwd LPSCl35/CBD5, NBR 26/27, PTFE 36/9 %). (d) 3D 이온 current density(NBR
  연속경로 無 vs PTFE 有). (e) 2D current density. (f) ★ **pore volume**(Pwd 28.7/NBR 29.4/PTFE 22.3 vol%)
  → **우리 audit #5(PTFE void-억제) 핵심 정량**.
- **Fig 3 (p.5):** ★ void·계면저항 — (a) **pressiometry Δ(ΔP)_Q**(NBR 1.99 vs PTFE 1.74). (b)(c)
  potential-EIS Nyquist(2.7/2.4 V). (d) R₁ 모식 + 전압별 R₁(NBR>PTFE, 깊은방전서 격차). → PTFE 부피·계면
  억제 정량.
- **Fig 4 (p.6):** ★ 장기열화 — (a) 100cyc EIS. (b) **R₂(charge-transfer)**(NBR 급발산 vs PTFE 포화).
  (c)(d) 단면 SEM(NBR void+crack vs PTFE clean). (e)(f) ToF-SIMS ⁷Li(NBR Li-trap vs PTFE 효율 deintercalation).
  (g) GITT D_Li(NBR 50cyc후 급감 vs PTFE 완만). → 열화 메커니즘 전모.
- **Fig 5 (p.8):** ★ LPSCl 분해·rock-salt — (a)(b) XPS S 2p(NBR sulfate 생성 vs PTFE 무). (c) **S 2p ratio**
  (NBR 100th SO₄²⁻ 4.4%+P-S 31.7% vs PTFE 17.1%). (d) ToF-SIMS SO⁻ 3D. (e–g) NBR TEM+SAED(rock-salt,
  17–22 nm). (h–j) PTFE TEM+SAED(layered 보존, 8–10 nm). → NBR의 화학분해 cascade 증거.
- **Fig 6 (p.9):** ★ 종합 — (a) NBR/PTFE 열화 모식. (b) retention(PTFE>Pwd>EMG>NBR). (c) 바인더 설계
  roadmap(confinement + adhesion → Target). → 1장 요약 + 설계지침.

### SI Figures (S1–S25) + Tables S1–S3
- **Fig S1:** NBR(a) vs PTFE(b) 양극 SEM(2 µm) — NBR 매끈한 입자, PTFE 섬유상(fibril) 존재.
- **Fig S2:** ★ **4개 구성 제작·조성 모식**(Pwd/S-Pwd/NBR/PTFE의 용매·바인더 decouple 설계).
- **Fig S3:** 0.33C normalized 방전용량(Fig 1c 무차원판). **Fig S4:** 4구성 충방전 곡선(1/5/10/20/50/100th).
  **Fig S5:** 4구성 rate 방전 곡선(0.1–2C).
- **Fig S6:** ★ **XRD**(pristine vs BB-exposed LPSCl) — 결정구조 변화 없음(argyrite 유지).
- **Fig S7:** ★★ **AC 임피던스**(pristine vs BB-exposed LPSCl) — **σ 1.87 → 0.53 mS/cm(28% 잔존)**.
- **Fig S8:** Pwd·S-Pwd cycling 중 EIS(10/20/50/100cyc). **Fig S9:** ★ **등가회로**(Rbulk + R₁ + R₂ + R₃, §6).
- **Fig S10:** ★ electron-blocking 대칭셀 Nyquist(a,c) + ion-blocking V-I(b,d) → σ_e/σ_ion(Table S2);
  주석: NBR·PTFE 둘 다 전자절연·이온무시 폴리머[S3].
- **Fig S11:** S-Pwd 3D 디지털트윈 + 2D 단면. **Fig S12:** Pwd vs PTFE 단면 EDS(Ni/S) mapping.
- **Fig S13:** ★ GITT 전압곡선(Pwd/NBR/PTFE) — 시뮬 LPSCl coverage 추세를 실험으로 검증.
- **Fig S14:** 4구성 3D(a)+2D(b) 이온 current density(NBR 연속경로 無; S-Pwd 안정 고-current 유지 →
  "NBR 열화는 LPSCl 화학분해 아닌 바인더분포" 입증).
- **Fig S15:** ★ (a) 3D pore phase(Pwd 28.7/NBR 29.4/PTFE 22.3 vol%) + (b) **target vs digital-twin 부피분율
  검증**(거의 일치 = 재구성 충실도).
- **Fig S16:** operando pressiometry 셋업(LTO/SE/cathode 펠릿 + 압력센서). **Fig S17:** Pwd 1.88 vs
  S-Pwd 1.89 Δ(ΔP)_Q(둘 다 비슷 → PTFE 1.74가 진짜 바인더효과). **Fig S18:** potential-EIS 측정점 + 각
  전압 Nyquist(NBR vs PTFE).
- **Fig S19:** ★ **SAICAS**(NBR vs PTFE 접착·응집) — **PTFE가 NBR의 약 2배 결합강도**(f_coh = F_H/w).
- **Fig S20:** R₁ vs cycle(NBR 20→33 vs PTFE ~5–6 Ω). **Fig S21:** Fig 4c/d 이진화 void/crack(NBR≫PTFE).
- **Fig S22:** NBR/PTFE GITT 전압프로파일(1/10/20/50/100cyc). **Fig S23:** XPS S 2p(pristine vs BB-exposed
  LPSCl, 둘 다 argyrodite — 노출만으론 분해 無). **Fig S24:** Fig 5e/h SAED target area TEM.
- **Fig S25:** EMG 바인더 비교 cycling(Pwd/NBR/PTFE/EMG; EMG가 NBR과 PTFE 사이).
- **Table S1:** ★ cycling(위 §4.1 표 — formation/1st/100th 용량·Eff·retention). **활물질 loading 30 mg/cm² 고정.**
- **Table S2:** ★★ **σ_ionic·σ_electronic**(Pwd 0.087/1.11, S-Pwd 0.079/1.07, NBR 0.042/0.85, PTFE 0.064/1.10 mS/cm).
- **Table S3:** ★ potential-EIS R₁(charge 3.1/3.5/3.7 V + discharge 3.5/3.1/2.7/2.4 V; NBR vs PTFE).

---

## 6. 기술 미니용어집 (우리 맥락)

- **Pwd / S-Pwd / NBR / PTFE:** 4개 양극 구성(§2.1). Pwd=무용매·무바인더 baseline; S-Pwd=용매만(바인더無)
  → **용매효과 분리**; NBR=wet(용매+NBR); PTFE=dry(PTFE만). **S-Pwd가 decouple의 핵심**(용매 vs 바인더).
- **Dry process(PTFE) vs Wet process(NBR):** dry=무용매 건식, PTFE 전단 피브릴화 → confined fibril망. wet=
  슬러리, NBR 깊이침투 광범위 coverage. ASSB 양극 제조 두 주류.
- **σ_ionic (Li⁺ ionic conductivity, mS/cm):** full-blocking AC 임피던스(10 mHz–1 MHz). ★ 우리 DEM
  Kirchhoff/Holm σ_ionic의 **실험 대응**(우리 소재계라 절대값 비교 가능). NBR이 LPSCl 차단 → 0.042로 최저.
- **σ_electronic:** SUS/cathode/SUS DC법. 바인더 영향 작음(Super C 망 지배). 우리 σ_e 대응이나 그들은
  triad 중 이온·전자만(열 없음).
- **Pore volume / Δ(ΔP)_Q:** pore volume(vol%) = 디지털트윈 기공분율(PTFE 22.3 ≪ NBR 29.4). Δ(ΔP)_Q =
  operando 단위용량당 압력변화(부피팽창; PTFE 1.74 < NBR 1.99). ★ **우리 porosity + MPM void-fill 대응** +
  audit #5(PTFE void-억제) 정량.
- **AM coverage (LPSCl/CBD %):** 디지털트윈에서 활물질 표면을 LPSCl/CBD가 덮는 비율. ★ **우리 Stage-E
  coverage(Tabor/Hertz)의 출력단 대응**. NBR이 LPSCl coverage 35→26% 급감 = σ_ionic 저하의 미세구조 원인.
- **R₁ / R₂ / R₃ (등가회로, Fig S9):** Rbulk(SE bulk) + **R₁ = AM↔SE 계면저항**(고주파, contact+계면부산물,
  ion-transfer 계면) + **R₂ = charge-transfer resistance**(중주파, 균열·rock-salt로 전자전도 저해·분극) +
  **R₃ = 음극(Li-In)↔SE 계면**(저주파). ★ **우리 transport(저항=1/σ)에 시간상수 분해는 없음** — R₁/R₂ 분리는
  EIS 고유(우리 모델 대응 없음). NBR R₂ 급발산 = dominant 열화 지표.
- **rock-salt 전환(SAED):** Ni-rich NCM 표면 layered → 비전기화학활성 rock-salt 상전이(전자전도↓·분극↑).
  NBR 17–22 nm vs PTFE 8–10 nm. LPSCl 산화분해 부산물(brittle, E↑)이 가속. 우리 모델엔 상전이 축 없음.
- **LPSCl 산화분해(sulfate, XPS S 2p):** PS₄³⁻(argyrodite) → SO₄²⁻(sulfate) + polysulfide. brittle·σ↓·E↑
  부산물 → 균열·void 전파. cycling이 trigger(노출만으론 無). 우리 fracture(Auerbach/Holm)의 화학 trigger 대응.
- **ToF-SIMS ⁷Li / SO⁻:** 사이클 후 ⁷Li 잔존(Li-trap, NBR) + SO⁻(sulfate, NBR) 공간 mapping. 우리 모델엔
  화학 species mapping 없음(transport σ만).
- **디지털트윈(GeoDict GrainGeo + ConductoDict FV):** 측정 파라미터(BET·조성·porosity·σ_ionic)→가상 미세구조
  **재구성**→FV로 이온 current density·coverage 출력. ★ **GeoDict 기반 reconstruct-from-measurement(출력단)**.
  우리 DEM+MPM은 **공정→구조 예측(입력단)** + Kirchhoff/Holm 접촉망(연속체 FV가 놓치는 점접촉 constriction).
- **SAICAS (Fig S19):** V형 마이크로블레이드 절삭 → 접착(adhesive)·응집(cohesive) 강도(f_coh=F_H/w).
  PTFE ≈ 2× NBR. 우리 `--coh`(SE cohesion) 측정법 대응.
- **EMG 바인더[ref17,S6]:** poly(ethylene-co-methyl acrylate-co-glycidyl methacrylate). distribution-controlled
  + high-adhesion wet 바인더 → NBR보다 confined + 강접착 → PTFE급. 이 그룹(Kim) 선행연구(= 설계지침 검증).

---

## ★ 7. 우리 DEM+MPM 검증/비교 (OUR SYSTEM — TIER-1 앵커) [frame [1]–[5]]

⚠ **대전제(★ #284/#285/#286과 결정적으로 다름):** 이 논문은 **우리 정확한 소재계 = LPSCl Li₆PS₅Cl 황화물 SE
+ NCM CAM, ASSB(solid-state, contact-network transport)**다. 따라서 **#284(SiOx 음극·액체)·#285(단결정 NCMA·
액체)·#286(흑연·액체)과 달리, σ_ionic·porosity·retention 절대값이 (조건 매핑 후) 전이 가능 → 검증 앵커**가
된다. Bazzoun(같은 LPSCl+NCM, EIS)에 이은 **2번째 같은-소재계 transport 실측 데이터셋**이다.

아래 (a)~(d)를 유저 요청 순서대로 — **(a) σ_ionic 절대값 in-range 검증, (b) 디지털트윈 vs 우리 DEM+MPM,
(c) PTFE void-최소화 ↔ audit #5, (d) NBR 비전이** — 명확히.

### (a) ★★ σ_ionic 절대값 — 우리 DEM σ_ionic 범위 + Bazzoun과 대조 → in-range인가?

**그들 실측 LPSCl 양극 σ_ionic(Table S2, full-blocking EIS):**
| 구성 | σ_ionic (mS/cm) | 비고 |
|---|---|---|
| **Pwd** (무바인더, pristine LPSCl) | **0.087** | 가장 깨끗한 LPSCl 양극 |
| **S-Pwd** (용매노출) | **0.079** | 용매 moderate 손실 |
| **PTFE** (dry) | **0.064** | confined 바인더 |
| **NBR** (wet) | **0.042** | 광범위 바인더 차단 |

**Bazzoun(같은 LPSCl+NCM, 400 MPa EIS):** σ_eff,ion = **0.137 / 0.101 / 0.065 mS/cm** @ f_CAM = 70/75/80 wt%
(vol% CAM:SE 45/53 → 60/38).

**우리 DEM σ_ionic(Kirchhoff/Holm + Stage-E, 132 케이스):** 생산 범위 **~0.04–0.18 mS/cm**(케이스별; 예
2mAh_real_9 σ_ionic_P 0.108/0.114/0.127 @ ε 13.47/13.19/12.47%; CBD 작업 SuperP 0.0168 / VGCF 0.0298).

**✅ 판정 — 우리 절대 σ_ionic은 in-range(검증됨):**
- 그들 LPSCl 양극 σ_ionic **0.042–0.087 mS/cm**는 **우리 DEM 생산범위(~0.04–0.18) 하단~중단에 정확히 들어감**.
  Bazzoun **0.065–0.137**과 합치면 **LPSCl+NCM 복합양극 σ_ionic의 실측 envelope ≈ 0.04–0.14 mS/cm**가
  형성된다 → **우리 DEM σ_ionic가 이 실측 envelope 안에 있다** = 절대값 cross-validation(frame[4]).
- **2개 독립 실측(Bazzoun EIS + Hong EIS)이 같은 자릿수(10⁻¹–10⁻² mS/cm)로 수렴** → 우리 절대 σ_ionic가
  "외삽 1점(Bazzoun)에만 의존"하던 audit #1 상태를 **다점 실측으로 격상**. ★ **이게 이 논문의 가장 큰 가치.**
- 조성 추세도 일치: Bazzoun은 **f_CAM↑(SE↓) → σ_ionic↓**(0.137→0.065). Hong은 조성을 고정(75 wt% NCM)하고
  **바인더로 σ를 변조** → 같은 조성에서도 **LPSCl coverage(AM 표면)↓ → σ_ionic↓**(Pwd 35%/0.087 → NBR 26%/
  0.042). 둘 다 **"SE 침투·접촉이 σ_ionic을 지배"**라는 우리 φ_SE/coverage 물리와 합치.

**⚠ 매핑 주의(in-range지만 정밀 1:1은 아님):**
- Hong σ_ionic는 **양극을 SE 펠릿 사이에 끼운 full-blocking 셀**의 양극-한정 이온전도(우리 σ_ionic 정의와
  같은 "복합양극의 유효 σ_ionic")라 Bazzoun보다 **우리 정의에 더 가깝다**(Bazzoun도 동일 셀). 단 **압력이
  다름**: Hong = 350 MPa 조립 + 30 MPa 측정, Bazzoun = 400 MPa 조립 + 25 MPa 측정, 우리 DEM = 300 MPa 표적.
  압력↑ → σ↑(Bazzoun이 ~400 MPa에서 포화)이므로 **Hong(350 MPa)이 Bazzoun(400 MPa)보다 약간 낮은 것은
  일관**(0.064 PTFE vs 0.065 @80%은 우연히 비슷; Pwd 0.087은 Bazzoun 75%의 0.101보다 낮음 — 압력·바인더 無·
  조성 차).
- **조성 매핑 필요:** Hong은 NCM 75 wt% 고정(vol% 미명시; 디지털트윈 AM ~36–41 vol%). Bazzoun vol% CAM:SE
  (45/53–60/38)와 우리 φ_SE 정의로 **셋을 같은 축에 올려야** 정밀 비교 가능(현재는 자릿수·추세 수준 일치).
- **σ_grain 앵커 정합:** Hong **pristine LPSCl bulk σ = 1.87 mS/cm**(Fig S7). Bazzoun pellet 1.02, Cronau
  단결정 3.0. → **1.87(Hong) 은 1.02(Bazzoun pellet)와 3.0(Cronau 단결정) 사이** = GB-포함 다결정 LPSCl의
  전형적 범위(셋 다 일관: 단결정 > 다결정 pellet, 측정셀·입경 차로 1.02~1.87 분산). 우리 σ_grain=3.0(단결정)
  + Cronau(r_SE) GB인자가 이 범위를 포괄하는지 점검 가치(이중계상 주의 — Bazzoun digest의 σ_grain 재검토
  항목과 동일).

### (b) ★ 디지털트윈 vs 우리 DEM+MPM — predict vs reconstruct, GeoDict 축, frame[4]/[5]

**그들 디지털트윈 = GeoDict 기반 reconstruct-from-measurement(출력단 특성화):**
- §4.5가 명시: **GrainGeo(GeoDict 2024) object-based stochastic generation**으로 NCM(BET 매칭)·LPSCl·Super C를
  **측정 조성·porosity에 맞춰 가상 재구성** → **ConductoDict FV(Finite Volume Method)**로 이온 current density·
  coverage 출력. **σ_ionic는 입력**(Table S2 실측값을 모델에 calibration으로 주입).
- ⇒ **구조를 측정/조성에서 재구성(reconstruct)하고, 그 위에서 유효물성을 FV로 푼다.** 압력·공정에서 구조가
  **어떻게 나오는지는 예측하지 않는다**(주어진 조성·BET·porosity가 입력). = **GeoDict 출력단 특성화** —
  `docs/positioning_vs_geodict.md`의 정확히 그 패턴(#281/#284/#286/#275와 같은 GeoDict 라인의 또 다른 사례).

**우리 DEM+MPM = predict-from-process(입력단 예측):**
- DEM(LIGGGHTS hooke/hysteresis) + MPM(Taichi J2): **압력·조성·입경·첨가제 → 미세구조**를 예측(GrainGeo가
  못 하는 입력단). 그 위에 voxel FV(= 그들 ConductoDict 대응, 무료) + **Kirchhoff/Holm 접촉망**(연속체 FV가
  놓치는 점접촉 constriction σ_ionic) + Stage-E 소성 접촉면적 + MPM 소성 morphology/void-fill + fracture.

**판정표:**
| 축 | Hong 디지털트윈 (GeoDict) | 우리 DEM+MPM |
|---|---|---|
| 미세구조 출처 | **측정 조성·BET·porosity로 재구성** | **압력·조성에서 예측** ★(GeoDict 불가) |
| 솔버 | ConductoDict FV(연속체) | voxel FV(연속체, 복제) **+ Kirchhoff/Holm 접촉망** ★ |
| σ_ionic | **입력**(실측 주입·calibration) | **출력**(접촉망 + Stage-E에서 계산) |
| coverage | 출력(LPSCl/CBD AM coverage %) | 출력(Stage-E Tabor/Hertz coverage) — **대응** ✓ |
| pore volume | 출력(porosity, 측정 매칭) | 출력(ε_sphere; DEM 예측) — **대응** ✓ |
| 소성 morphology·void-fill | ✗(고정 형상 입자) | ✅ MPM ★ |
| 입자 파괴·force chain | ✗ | ✅ DEM ★ |
| 시간 진화(degradation) | ✗(단일 스냅샷) | ✗(우리도 없음 — §(d)) |

- **frame[4](독립 교차검증):** 그들은 **σ_ionic를 입력**으로 넣고 coverage·current density를 출력 → "구조→
  물성" 방향. 우리는 **구조를 예측**하고 σ_ionic를 출력 → "공정→구조→물성" 방향. **둘은 반대 방향**이라
  직접 cross-fit은 아니나, **같은 LPSCl 양극의 σ_ionic 절대값(그들 실측 = 우리 출력)이 같은 envelope에
  들어가면**(§(a) ✅) 두 접근이 같은 물리를 가리킨다 = 교차검증.
- **frame[5](분업):** 그들 디지털트윈은 **이온 transport 출력단**(coverage·current density)에 머물고
  **압력→구조 예측·접촉망 constriction·소성·파괴가 없다**(GrainGeo 고정형상). 우리는 입력단 예측 + 접촉망 +
  MPM/fracture가 더 넓다. **그들의 출력단 coverage/current-density 시각화는 우리 Stage-E coverage 출력에
  검증 reference**(우리 coverage가 그들식 AM-coverage %로 환산되는지).
- ★ **positioning 강화:** Bazzoun이 RNM(접촉망, = 우리 솔버 평행구현)이었던 것과 달리, **Hong은 GeoDict
  연속체 FV** → `positioning_vs_geodict.md`의 "GeoDict는 구조를 줘야 한다(reconstruct), 우리는 예측한다
  (predict)"를 이 그룹의 **양극(ASSB) 사례로** 직접 재확인. 즉 **이 그룹조차 ASSB 양극에서 GeoDict로 출력단
  특성화만** 한다 → 우리 입력단 예측 superset 논지의 강한 외부증거.

### (c) ★★ PTFE void-최소화 = 우리 audit #5가 놓치는 양(陽)의 역학효과 (가장 실행가능한 발견)

**그들이 정량한 PTFE의 void-억제(우리가 σ=0 모델로 빠뜨린 것):**
- **pore volume:** PTFE **22.3 vol%** ≪ Pwd 28.7% < NBR 29.4% (Fig 2f) → PTFE가 **−6.4%p densification**.
- **operando 부피팽창:** PTFE Δ(ΔP)_Q **1.74** < Pwd 1.88 < S-Pwd 1.89 < NBR 1.99 (Fig 3a/S17) → PTFE가
  **무바인더 Pwd보다도 ~8% 작은 팽창**(접착으로 입자연결 유지 → 사이클 팽창 흡수).
- **SAICAS:** PTFE ≈ **2× NBR** 결합강도(Fig S19) → 구조무결성.
- → PTFE는 **이온차단(σ_ionic 0.087→0.064, −26%)이라는 음(陰)의 효과**와 **void-억제·densification·접착이라는
  양(陽)의 역학효과**를 동시에 가지며, **net으로 retention 최고(94.6%)** = 양효과가 음효과 압도.

**우리 audit #5 현황:** 우리는 **PTFE를 σ=0 obstacle**로만 모델(transport mask에서 PTFE 셀=비전도). #285/#286은
"PTFE 탈불소화는 액체-LIB ICE 손실 → ASSB 무관"이라 했고, 우리는 **PTFE를 이온차단(음)만 반영**한다.
❗ **이 논문은 ASSB에서 PTFE의 양(陽)의 역학효과(void-억제·densification·접착)가 실재하고 retention을
지배함을 보인다** → **우리 σ=0 모델은 PTFE의 절반(음의 차단)만 잡고 절반(양의 void-억제)을 놓친다.**

**★ 우리가 누락하는 것 정량 + 이식 후보:**
- **(i) PTFE의 densification(−6.4%p pore):** 우리 `additives.py`의 PTFE는 **기하 obstacle**(부피 차지 +
  σ=0)이고 **MPM에서 PTFE를 능동 결합상으로 안 다룬다**. → PTFE를 **MPM에서 cohesion-부여 상**(`--coh`에
  PTFE-fibril 항)으로 넣으면 **void-억제(porosity↓)를 재현** 가능. 현재 우리 MPM은 PTFE를 압축에 안 넣음 →
  PTFE-포함 케이스의 porosity를 **과대평가**할 위험(그들 PTFE 22.3% vs Pwd 28.7%처럼 PTFE가 더 조밀해야).
- **(ii) net 효과 정량 틀:** PTFE = σ_ionic −26%(차단) BUT porosity −6.4%p(void-fill). **우리 σ_ionic은
  porosity↓ → σ↑이므로**, PTFE의 void-억제가 σ_ionic을 **부분 회복**시킬 수 있다(차단으로 잃은 σ를 densification
  으로 일부 되찾음). 현재 우리는 차단(−)만 모델 → **PTFE σ_ionic을 과소평가**할 수 있다. 그들 실측 PTFE
  0.064(Pwd 0.087의 74%)는 "net 26% 손실"이 **차단·densification 상쇄 후 값**이다 → 우리 모델이 PTFE를
  σ=0 차단만으로 26%보다 더 깎으면 과소. **양 효과를 둘 다 넣어야 0.064에 맞는다.**
- **(iii) audit #5 진전:** audit #5는 "PTFE를 σ=0 obstacle로 모델 — defluorination은 ASSB 무관"이었다.
  ★ 이 논문은 **defluorination이 아닌 새 축(PTFE 기계적 void-억제)**이 ASSB에서 중요함을 추가 → audit #5에
  **"PTFE 양의 역학효과(void-억제·접착) 미반영" 항목을 신설**할 근거(유저가 audit 직접 편집).

### (d) NBR은 우리 모델에 없음(process-specific, 비전이) + 시간진화 GAP

- **우리는 wet/NBR 공정을 안 다룬다.** 우리 DEM+MPM은 **dry-process(무용매) 압축**만 모델(LPSCl + AM + (PTFE)).
  NBR의 **깊은 침투·광범위 coverage·용매유발 LPSCl 분해(sulfate·rock-salt)**는 **wet 공정 특이현상** →
  우리 입력에 NBR 항 없음 → **비전이**(process-specific). NBR 수치(retention 85.4, σ_ionic 0.042, R₂ 발산,
  rock-salt 17–22 nm)는 우리 검증 앵커가 **아니다**(PTFE·Pwd·S-Pwd만 우리 dry-side에 대응).
- ❗ **공통 GAP — 시간진화(degradation):** 그들의 **100사이클 void 성장·rock-salt 전환·R₂ 발산·D_Li 급감**은
  **시간(사이클) 축 화학-기계 열화**다. 우리 DEM+MPM은 **단일 압축 스냅샷**(시간 진화 없음; #285 spring-back
  미구현과 같은 정체). → **우리도 그들도(그들 디지털트윈도 단일 스냅샷) cycling 열화를 직접 예측 못 한다.**
  단 그들은 **실측(SEM/EIS/XPS/GITT)으로** 열화를 관측, 우리는 **압축 종점만** → 이건 우리 transport 모델의
  scope 밖(Phase 4 chemo-mechanical 확장 시 후보). 우리 fracture(Auerbach/Holm)가 **균열→σ↓**의 첫 조각이나,
  rock-salt 상전이·sulfate 생성 같은 **화학 trigger는 없음**.

### 비교 요약표
| 축 | Hong 2026 (LPSCl+NCM ASSB, dry/wet) | 우리 (LPSCl ASSB, DEM+MPM) | 전이/판정 |
|---|---|---|---|
| 소재 | **LPSCl SE + NCM CAM** | **동일 ✓** | ★ 절대값 전이 가능(검증 앵커) |
| σ_ionic 절대 | Pwd 0.087 / PTFE 0.064 / NBR 0.042 mS/cm | DEM ~0.04–0.18 | ✅ **in-range**(+ Bazzoun 0.065–0.137 → envelope 0.04–0.14) |
| σ_ionic 추세 | coverage↓(LPSCl AM 35→26%) → σ↓ | φ_SE/coverage↓ → σ↓ | ✅ 일치(우리 coverage 물리 확증) |
| bulk LPSCl σ | **1.87 mS/cm**(pristine) | Cronau 단결정 3.0 / Bazzoun pellet 1.02 | ✅ 1.02 < 1.87 < 3.0 일관(GB) |
| pore volume | PTFE 22.3 / Pwd 28.7 / NBR 29.4 vol% | DEM ε_sphere 예측 | ★ PTFE densification = audit #5 신규 |
| PTFE 역할 | **void-억제(−6.4%p)·접착·팽창↓(1.74)** | **σ=0 obstacle(차단만)** | ❗ **양의 역학효과 누락**(audit #5) |
| NBR(wet) | 광범위 coverage·sulfate·rock-salt | **모델 없음** | ⚠ process-specific(비전이) |
| 디지털트윈 | **GeoDict reconstruct(출력단), σ 입력** | **DEM+MPM predict(입력단), σ 출력** | frame[5] 분업; positioning 재확인 |
| 시간 열화 | 실측(void/rock-salt/R₂, 100cyc) | 단일 스냅샷(없음) | ❗ 공통 GAP(Phase 4 후보) |
| 우리 고유 | (디지털트윈 출력단만) | 접촉망 σ triad + 소성 morphology + fracture + 예측 | frame[5] 우리 우위 |

---

## ★ 8. 우리 작업에 넣을 가장 날카로운 인사이트 3가지

1) ✅✅ **우리 σ_ionic 절대값이 검증된다 — Bazzoun에 이은 2번째 같은-소재계 실측 앵커.**
   Hong LPSCl 양극 σ_ionic **0.042–0.087 mS/cm**가 **우리 DEM 생산범위(~0.04–0.18) 안**에 들고, Bazzoun
   (0.065–0.137)과 합쳐 **LPSCl+NCM σ_ionic 실측 envelope ≈ 0.04–0.14 mS/cm**를 만든다 → **우리 절대 σ_ionic이
   "외삽 1점(Bazzoun)" 상태(audit #1)에서 "2개 독립 EIS 실측에 둘러싸인" 상태로 격상**. 자릿수·조성추세
   (coverage/φ_SE↓→σ↓) 모두 일치 = frame[4] 절대값 cross-validation. ★ **이게 이 논문의 최대 가치 — TIER-1
   인 이유.** (단 압력 350 vs 400 vs 300 MPa + vol% 매핑은 정밀 1:1 전 보정 필요.)

2) ★★ **PTFE의 양(陽)의 역학효과(void-억제) — 우리 σ=0 모델이 놓치는 절반 (audit #5 진전).**
   우리는 PTFE를 **σ=0 obstacle(이온차단=음효과)**로만 모델하나, 이 논문은 ASSB에서 PTFE가 **pore를
   28.7→22.3 vol%(−6.4%p) 낮추고 팽창을 1.74로 억제(Pwd 1.88보다도 낮음)·접착 2×**라는 **양효과**가 retention
   최고(94.6%)를 만듦을 보인다. → ❗ **우리 모델은 PTFE의 음(차단)만 잡고 양(void-억제·densification)을 빠뜨려
   PTFE-케이스 porosity 과대·σ_ionic 과소** 위험. 이식: **MPM에서 PTFE를 cohesion-부여 결합상(`--coh` PTFE항)
   으로 → void-억제 재현**; net σ_ionic은 "차단 − densification 회복"으로 계산해야 그들 0.064에 맞음. audit #5에
   **"PTFE 기계적 void-억제 미반영"** 신규 항목 근거(defluorination과 별개 축).

3) ★ **디지털트윈 = GeoDict reconstruct(출력단) → 우리 predict(입력단) superset 재확인 + 시간열화 공통 GAP.**
   그들 디지털트윈은 **GeoDict GrainGeo로 측정 조성·BET·porosity에서 구조를 재구성** + ConductoDict FV로
   coverage·current density 출력(**σ_ionic는 입력**). = `positioning_vs_geodict.md`의 "GeoDict는 구조를 줘야
   함"을 이 그룹의 **ASSB 양극** 사례로 직접 재확인 → 우리 **공정→구조 예측 + 접촉망 constriction** superset
   논지 강화. 그들의 **AM-coverage %(LPSCl 35→26%)·current-density 맵은 우리 Stage-E coverage 출력의 검증
   reference**(우리 coverage가 그들식 %로 환산되는지 비교 후보). ❗ 단 **시간(cycling) 열화는 둘 다 단일
   스냅샷이라 예측 불가** = 공통 GAP(우리 fracture가 균열→σ↓ 첫 조각이나 rock-salt/sulfate 화학 trigger는
   없음 → Phase 4 chemo-mechanical 확장 후보).

### 보너스 실행 항목
- **#271 인덱스 갱신**(아래 완료): web-abstract → 검증 수치(σ_ionic Pwd 0.087/S-Pwd 0.079/PTFE 0.064/NBR
  0.042, retention 92.0/87.1/85.4/94.6%, pore 28.7/29.4/22.3 vol%, AM-coverage LPSCl 35/26/36 · CBD 5/27/9%,
  Δ(ΔP)_Q 1.74 vs 1.99, LPSCl σ 1.87→0.53, R₁/R₂, rock-salt 17–22 vs 8–10 nm, 디지털트윈=GeoDict GrainGeo+
  ConductoDict FV)로 교체.
- ⚠ **혼동 금지(역할 구분):**
  - **#271(이 논문, LPSCl+NCM ASSB):** ★ **σ_ionic·porosity 절대 검증 앵커(Bazzoun에 이은 2번째 같은-소재계)
    + PTFE void-억제(audit #5) + GeoDict reconstruct positioning**. 우리 소재계라 **수치 전이됨**.
  - **#284(Oh, SiOx·액체):** CBD ion/electron trade-off 개념 + 분산 측정법. **수치 비전이.**
  - **#285(Hong R., 단결정 NCMA·액체):** rigid-AM 검증 + spring-back 미구현. **수치 비전이.**(이름이 같은
    "Hong"이나 **다른 논문·다른 소재** — 혼동 금지: #271=Seung-Bo Hong/ASSB, #285=Rakhwi Hong/액체.)
  - **σ/porosity 절대앵커 = Bazzoun(LPSCl) + #271(LPSCl) + Varkey(halide, 비교용) + Minnmann(LPSCl cold-press)**
    — #271이 **LPSCl σ_ionic 앵커군에 합류**(Bazzoun과 짝).
- **σ_grain 재검토(선택):** Hong bulk LPSCl 1.87 + Bazzoun pellet 1.02 + Cronau 단결정 3.0 → 우리 σ_grain=3.0
  + Cronau(r_SE) GB인자가 1.02–1.87 다결정 범위를 포괄하는지 (이중계상 주의; Bazzoun digest 동일 항목과 통합).

---

## 9. comparison_vs_ours / properties 반영 메모

- **축 B(transport triad):** #271 σ_ionic(Pwd 0.087/PTFE 0.064/NBR 0.042 mS/cm) → **우리 DEM σ_ionic
  절대 검증점**(Bazzoun 0.065–0.137과 함께 LPSCl+NCM envelope 0.04–0.14). σ_electronic(0.85–1.11)은 우리
  σ_e와 자릿수 비교 가능하나 그들은 양극 DC법(Super C 망 지배) → 우리 AM-network σ_e와 정의 다름(참고만).
- **축 A(compaction/porosity):** #271 pore volume(PTFE 22.3/Pwd 28.7/NBR 29.4 vol%) → 우리 ε 예측의
  바인더-효과 reference(특히 PTFE densification = audit #5).
- **축 C(mechanics/morphology):** PTFE void-억제·Δ(ΔP)_Q·SAICAS 2× = 우리 MPM void-fill + `--coh` 대응
  (PTFE를 능동 결합상으로 넣는 근거).
- **축 E(where-we-validate-lit):** σ_ionic 절대값 in-range = 우리 DEM이 #271 실측을 **검증**(frame[4]).
- **축 F(what-we-can't-do-yet):** (i) wet/NBR 공정, (ii) 시간(cycling) 화학-기계 열화(void 성장·rock-salt·
  sulfate), (iii) PTFE 양의 역학효과 = 현재 미모델 → Phase 4/audit #5 후보.

---

## ★ 10. 비판적 한계 (over-claim 금지)

- **σ_ionic in-range ≠ 정밀 검증:** 우리 DEM 범위(0.04–0.18)가 넓어 그들 값(0.042–0.087)이 "들어간다"는
  건 **envelope 합치**지 **점대점 검증이 아니다**. 압력(350/400/300 MPa)·조성(vol% 미명시)·셀구성 차를
  보정해 **같은 (φ_SE, P)에서 비교**해야 진짜 검증. 현재는 "자릿수·추세 일치" 수준(그래도 audit #1 1점→다점은
  실질 진전).
- **디지털트윈 σ는 입력(자기참조 주의):** 그들 디지털트윈은 **실측 σ_ionic를 calibration 입력으로 주입** →
  current density·coverage 출력. 즉 **σ_ionic 자체는 모델이 예측한 게 아니라 측정값**이다. 그들 coverage/
  current-density는 "σ_ionic를 재현하도록 fit된" 구조의 결과 → **우리 DEM이 σ_ionic를 from-scratch 예측**하는
  것과 정보론적 위상이 다름(그들=실측 σ로 morphology 역추론, 우리=구조로 σ 순추론).
- **GeoDict 연속체 한계 공유:** 그들 ConductoDict FV는 **점접촉 sub-voxel constriction을 못 잡는 σ_contact-free
  상한**(우리 voxel FV와 동일 한계, `voxel_conductivity_crossvalidation.md`). granular SE의 진짜 σ_ionic은
  Kirchhoff/Holm 접촉망이 필요(그들엔 없음, 우리엔 있음) → 그들 current-density 절대값은 constriction 미반영
  상한일 수 있음.
- **PTFE void-억제 = 정성·단일조건:** −6.4%p pore·1.74 Δ(ΔP)_Q는 **75 wt% NCM·350 MPa 단일 조건**. 우리
  모델에 넣을 PTFE cohesion 강도는 **이 1점에 fit**할 수밖에 없어 다압력·다조성 일반화는 미검증(그들 데이터
  부족). "PTFE가 densify시킨다"는 방향은 확실하나 **얼마나(정량)는 1점 외삽**.
- **bulk LPSCl 1.87 mS/cm vs 우리 1.35 GPa E_eff는 무관 축:** 1.87은 σ(전도), 1.35는 E(역학) — 같은 LPSCl이나
  다른 물성. σ_grain 정합 논의(§(a))는 σ축만; E_eff softening 논의(real 22–24 GPa → 1.35 proxy)와 섞지 말 것.
- **rigid-sphere/연속체 공통 한계:** 우리 DEM(강체구+overlap-proxy)도 그들 GeoDict(고정형상)도 **소성 입자
  형상변화가 없다**(우리 MPM만 있음). 그들 디지털트윈은 형상 고정 + σ 입력이라 **소성·압축역학·접촉망이 전무**
  → frame[5]에서 우리(특히 MPM+접촉망)가 더 넓음은 분명하나, **그들의 강점(실측 EIS·XPS·SEM 열화 관측 +
  GeoDict robust 연속체)**은 우리에게 없음(정직하게).
