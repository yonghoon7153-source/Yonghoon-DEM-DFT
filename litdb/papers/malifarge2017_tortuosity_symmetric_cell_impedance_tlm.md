<!-- digest 표준 양식 확장 (paper-level STANDALONE).  ★ = 사용자가 특히 원한 항목.  깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md ·
     τ 묶음 형식 기준 = tjaden2018_… · taufactor_… · landesfeind2016_… + 같은 날 앞 묶음 (siroma2015_… · kaiser2018_… · landesfeind2018_… · pouraghajan2018_…).
     이 논문은 실험 (차단 대칭셀 EIS) + 1D 회로 모형 (두 레일 전송선 모델 TLM) + Newman P2D 주파수영역 검증 논문이다 — DEM · MPM · FEM 미세구조
     시뮬레이션은 없다.  그래서 §4 = 식의 사슬 (원문 번호 그대로) + 측정 · 적합 사슬이고, §8 맨 앞 = "전자 저항 임의값 대칭셀 TLM" (이 카드를 연 이유).
     쪽 표기 = 학술지 인쇄 쪽 E3329–E3334.  PDF n 쪽 = 인쇄 E(3327 + n)  (PDF 1 = 출판사 내려받기 표지 · 논문 아님 · PDF 2 = E3329 … PDF 7 = E3334).
     식 · 표 · 그림 번호 = 원문 번호.  SI 없음 (원문에 Supplementary 언급 없음).
     수식 · 표 · 그림은 원문 PDF 를 고배율 (4–7×) 로 렌더해 읽었다 (텍스트 추출은 τ · ε · κ · 물결표 · 첨자를 깨뜨린다).
     값 표지: stated = 본문 · 캡션 · 표 원문 / 판독 = 그림에서 읽은 값 (≈, 추세 전용) / 카드 산술 = 원문 수치로 계산 (식 명시) /
     우리 유도 = 원문 식에서 카드 작성자가 끌어낸 극한 · 관계 (원문에 그 문장은 없다) / 우리 재계산 = 원문 식을 수치로 검산 ("원문 대조 기록" 절). -->
# 차단 대칭셀 임피던스의 두 레일 전송선 모델 (TLM) 로 기공 tortuosity τ₂ 추출 — 고상 전자 레일 포함 Z형 open–open 해 (Tröltzsch–Kanoun 해석식 = Siroma 표 2 · Landesfeind 2018 Eq 1 · Pouraghajan Eq 5 극한과 같은 함수) · Newman P2D 와 일치 검증 · 판상 흑연 16 전극 τ₂ 5–9 (Bruggeman 의 약 2.3–3.7 배) — Malifarge (J. Electrochem. Soc. 2017)

> slug `malifarge2017_tortuosity_symmetric_cell_impedance_tlm` · DOI `10.1149/2.0331711jes` · type `exp+theory (차단 대칭셀 EIS + 두 레일 TLM 전 스펙트럼 적합 · Newman P2D 주파수영역 검증; 액체 LIB 흑연 음극 기공 τ₂)` · PDF `24. Determination of tortuosity using impedance spectra analysis of symmetric cell.pdf` · digested `2026-10-03` · status ✅
>
> inbox τ 문헌 묶음 tortuosity_3 #24 · 본문 6 쪽 (E3329–E3334) 전부 렌더로 읽음 (식 1–13 · 그림 1–6 · Table I · 참고문헌 51) · SI 없음 · 그림 크롭은 메인 몫 (§5 에 권고).
> ★ **정의 판정** — 이 논문의 τ₂ 는 **τ₂ = ε₂·κ/κ_eff** (Eq 8 의 κ_eff = (ε₂/τ₂)·κ, E3330) 이다.  원문 이름은 *"electrolyte tortuosity"* (E3330) · *"pore tortuosity"* (그림 6 축 · E3332–E3333)
> 이고 **"tortuosity factor" · "MacMullin" 낱말은 한 번도 나오지 않는다** — 그러나 값의 꼴은 **tortuosity factor = 우리 `tau2`** (Bruggeman 을 τ₂ = ε₂^−0.5 로 그린다, 그림 6).
> σ₀ = **벌크 액체 전해질 κ 0.792 S/m** (LP40 계열, Lundgren [28] 문헌값, 25 °C) · ε₂ = 무게 · 조성에서 낸 **전극 기공률**.  측정법은 **차단 대칭셀 + TLM 전 스펙트럼 적합** → Nguyen 분류 **eSCM = τ_e 계열**.
> ★ **닫는 항목 판정 (§8-1)** — "전자 저항 임의값 대칭셀 TLM" 의 **식은 원문에 있다** (Eq 7 의 σ_eff = (ε₁/τ₁)σ · Eq 11).  그러나 ① 해석식 Eq 11 은 **Tröltzsch–Kanoun [37] 의 것**이고
> (같은 함수 = Siroma 표 2 Z형 "open–open" · Landesfeind 2018 Eq 1 · Pouraghajan Eq 5 의 Z₀ → ∞ · Z_cc → 0 판 — 우리 재계산 상대차 ≤ 4·10⁻¹⁶) ② 자료는 흑연 (σ 2203.8 S/m) 뿐이라
> 전자 저항이 의미 있는 영역을 **시험하지 않았고** (원문: *"No influence of the solid phase conductivity … (2000 S.m⁻¹ or more)"*, E3331) ③ **무시 오차의 원문 수치는 없다** ④ Eq 11 은
> **R_e ↔ R_i 교환에 불변** (우리 유도) — "r_el ≪ r_ion 이 안 설 때" 스펙트럼 하나로는 어느 레일이 이온인지 못 가른다 → 독립 전자 측정으로 R_e 를 고정해야 한다.
> 형제 카드: `siroma2015_transmission_line_model_porous_electrode_impedance` (TLM 해 전집 — 위상 이름표) · `landesfeind2018_tortuosity_impedance_vs_tomography` (같은 함수의 β 오차 지도) ·
> `pouraghajan2018_tortuosity_polarization_interrupt_vs_blocking_electrolyte` (일반 TLM — 이 논문을 ref 15 로 인용) · `nguyen2020_electrode_tortuosity_factor` (eSCM · τ_e — 이 논문을 ref 18 로 인용) ·
> `landesfeind2016_tortuosity_eis_electrodes_separators` (차단 대칭셀 TLM-Q · 분리막 실측) · `kaiser2018_ion_transport_limitations_assb_sulfide_electrodes` (ASSB TLM, z_C = 0) · `minnmann2021_jes_charge_transport_bottlenecks` (ASSB σ_el,eff · σ_ion,eff 실측 — §8-1 β 의 원천).

---

## 0. 결론 먼저 (정의 판정 + 닫는 항목)

| 질문 | 답 | 근거 (식 · 쪽) |
|---|---|---|
| τ₂ 는 어떤 양인가 | **ε₂·κ/κ_eff** — tortuosity factor 꼴 = 우리 `tau2`.  원문 이름 "electrolyte tortuosity" · "pore tortuosity".  "tortuosity factor" · "MacMullin" 낱말 0 회 (원문 전수).  Bruggeman = τ₂ = ε₂^−0.5 (T 지수 0.5 관례 = Landesfeind 관례) | Eq 7–8 (E3330) · 그림 6 범례 (E3333) |
| σ₀ 기준 | **벌크 액체 κ = 0.792 S/m** (Table I "Li⁺ conductivity", Lundgren [28], 25 °C) — 배치 실측 아님 · "벌크 = 1" 부류 (펠릿 기준 상태 문제 없음) | Table I (E3332) |
| ε 기준 | ε₂ = 전극 기공 부피분율 — *"Mean electrode porosity is evaluated from weight and composition"* · 같은 설계의 **평균값**을 그 설계의 모든 전극 적합에 쓴다 | E3330 · E3332–E3333 |
| 측정법 계열 | 차단 대칭셀 EIS + TLM **전 스펙트럼** 적합 (자유 매개변수 셋: Q₀ · α · τ₂).  그래프법 (R/3) 을 쓰지 않는다 → Nguyen **eSCM (τ_e 계열)**.  균질 1D 가정 안에서만 관통 tau2 와 같은 수 (siroma 카드 §0) | E3331 · nguyen 카드 §4-A |
| TLM 의 위상 | 두 레일 (위 = 고상 전자 Z̃_e · 아래 = 액상 이온 Z̃_i · 가로대 = CPE Z̃_t) · 전자 단자 = 집전체 쪽 (k = 1) · 이온 단자 = 분리막 쪽 (k = n, Z_sep 직렬) · 반대 끝 둘 다 열림 = **Siroma 표 2 Z형 "open–open" (z_C ≠ 0)** | 그림 1 · Eq 2–6 (E3330) |
| 해석식은 누구의 것인가 | Eq 11 = Tröltzsch–Kanoun [37] (원문: *"Alternately, an analytic solution developed by Tröltzsch and Kanoun"*).  이 논문 고유 = 행렬 Kirchhoff 판 (Eq 2–10) · P2D 물성 매개변수화 (Eq 7–9 · 12–13) · P2D 일치 (그림 2) · 흑연 적용 | E3330 |
| 같은 함수인가 (앞 묶음 대조) | **같다** — Siroma 표 2 Z형 open–open · Landesfeind 2018 Eq 1 (Göhr) · Pouraghajan Eq 5 (Z₀ → ∞ · Z_cc → 0 · 차단).  대수 전개가 같은 세 항이고 수치 상대차 ≤ 4·10⁻¹⁶ (우리 재계산).  **다른 꼴은 Minnmann 식 [1] (= Siroma 표 3 T형, 관통형)** | §4-3 |
| 전자 저항을 실제로 다뤘나 | 식에는 있다 (Eq 7).  자료는 흑연 σ **2203.8 S/m** (Table I, Ender [47]) 뿐이고 *"No influence of the solid phase conductivity on this domain is observed in the typical range of electronic conductivity reported for graphite electrodes (2000 S.m⁻¹ or more)"*.  τ₁ · ε₁ 값 미보고.  β = R_e/R_i ≈ 10⁻⁵–10⁻⁴ (카드 산술) | E3331 · Table I · §3-5 |
| 전자 저항 무시 오차 (원문 수치) | **원문에 없다.**  같은 함수의 수치 = Landesfeind 2018: R_El/R_Ion < 10⁻² 정확 · 10⁻²–10⁻¹ 이면 R_Ion 오차 최대 ~20 % (그 카드 A470–A471).  우리 유도 (Eq 11 극한): 그래프법 겉보기 R_ion = R_ion·[(1+β) − 3β/(1+β)] — β 0.01 → 0.980 · 0.1 → 0.827 · 최소 0.464 (β 0.732) · β 2 → 1.000 (우연 상쇄) · β 10 → 8.27 | §4-4 |
| 레일 배정 | Eq 11 은 **R_e ↔ R_i 교환에 불변** (식이 R_e + R_i · R_eR_i · R_e/R_i + R_i/R_e 로만 들어간다 — 우리 유도 · 수치 확인) → 스펙트럼 하나로는 레일을 못 가른다.  원문은 σ 를 문헌값으로 **고정**해 이 문제를 피했다 | §4-4 |
| 결과 (흑연) | τ₂ **5–9** (기공률 45 → 10 %, E3333; E3332 는 "5.5 to about 9") · 멱법칙 τ₂ = **3.19ε₂^−0.46 · 4.29ε₂^−0.23 · 3.88ε₂^−0.43 · 3.42ε₂^−0.50** (적재 4.8 · 8.8 · 11.9 · 15.7 mg/cm²) · 8.8 제외 시 전인자 3–4 · 지수 ≈ 0.46 · Bruggeman 의 **2.3–3.7 배** (ε₂ 0.10–0.45, 카드 산술) | 그림 6 · E3332–E3333 |
| 원인 해석 (원문) | 판상 흑연이 Cu 집전체와 **평행 정렬** — 같은 배치에서 평행에 가까운 입자가 압연압에 따라 **30–60 %** ([21]) · 평행 입자 몫이 클수록 τ₂ ↑ · 지수 < 0.5 = 기공 영향 완만 · 큰 전인자 = 형상 · 크기 · 방향 | E3332 |
| 감도 | 기공률 < 15 % 에서 **기공 1 % 입력 차 → τ₂ 약 0.75** (stated) = R_ion 고정 시 τ₂ ∝ ε₂ 로 재현 (ε₂ 0.12 · τ₂ 9 → 0.75, 카드 산술) | E3332 |
| 우리 ASSB 에서 이 해가 필요한 조건 | **탄소 없는 NCM 복합 양극 · 0 % SoC · Z형 차단 셀** — β = σ_ion,eff/σ_el,eff 가 Minnmann stated 값으로 **≈ 20 (25 vol% CAM) · 1.1 (33) · 0.30 (42) · 0.031 (53) · 0.002 (61)** (카드 산술).  질량비 70:30 에서 de Levie 형 (z_C = 0) 그래프법이 R_ion 을 × 0.61 로 · 33 vol% 이하에서는 레일 배정 자체가 모호 | §8-1 (e) |

## 1. 한 줄 요약
집전체 붙은 흑연 전극 두 장의 **차단 대칭셀** (LP40 · 개방회로 · 원상태 흑연) EIS 를, 고상 전자 레일까지 넣은 **두 레일 전송선 모델** (원소를 Newman 다공 전극 이론과 같은
κ_eff = (ε/τ)κ 꼴로 매개변수화 · 이중층 = CPE) 로 **전 스펙트럼 적합**해 기공 tortuosity τ₂ 를 직접 뽑는 방법을 내고 (P2D 주파수영역 모의와 α = 1 에서 겹침 확인),
판상 흑연 16 전극 (적재 4 × 기공 4) 에서 **τ₂ 5–9 (Bruggeman 의 약 3 배)** 와 "평행 이동한 Bruggeman" 꼴 멱법칙 (지수 ≈ 0.46) 을 얻은 논문 — 우리에게는 전자 레일을
가진 **Z형 TLM 해의 τ 추출 원문 사례**이자, 그 해가 **R_e ↔ R_i 대칭**이라 저 σ_e ASSB 양극에서는 독립 전자 측정 없이는 쓸 수 없다는 한계 (우리 유도) 의 출발점이다.

## 2. 메타

| 저자 | 저널/년 | DOI | 소속 | 연구유형 |
|---|---|---|---|---|
| **Simon Malifarge**, Bruno Delobel, **Charles Delacourt** (교신) | **J. Electrochem. Soc. 164 (11) E3329–E3334 (2017)** | **10.1149/2.0331711jes** | Laboratoire de Réactivité et Chimie des Solides, CNRS UMR 7314, Université de Picardie Jules Verne, Amiens · Renault Technocentre, Guyancourt (E3329) | 실험 (EIS) + 1D TLM + P2D 검증 — 미세구조 시뮬레이션 없음 |

- 이력 (E3329): submitted 4 April 2017 · revised 19 May 2017 · published 3 June 2017.  *"JES Focus Issue on Mathematical Modeling of Electrochemical Systems at Multiple Scales in Honor of John Newman"*.
- **OA**: © The Author(s) 2017, Published by ECS — **CC BY-NC-ND 4.0** (E3329).
- 사사 (E3333): ANRT (Malifarge 부분 지원) · ZEON Corporation · B. Fleutot (LRCS, EIS 측정 도움) · D. Gruet (두께 측정).
- 구성: 6 쪽 · 그림 6 · 표 1 · 식 (1)–(13) · 참고문헌 51.  **SI 없음.**
- 같은 저자의 선행 [21] (흑연 전극 입자 방향 XRD 정량, J. Power Sources 343, 338 (2017)) 이 이 논문의 이방성 해석 근거다.
- 원문의 새로움 주장 (E3329): *"to the best of the authors' knowledge, no tortuosity value was extracted from the TLM analysis"* — ⚠ Landesfeind 2016 (차단 대칭셀 TLM τ) 을 인용하지 않았다 (§10-3 #10).

## 3. 핵심 수치

### 3-1. 재료 · 셀 · 측정 조건 (stated)

| 항목 | 값 | 쪽 |
|---|---|---|
| 전극 조성 | 산업용 흑연 전극: **흑연 97 wt% · CMC 1 % · SBR 1 % · 도전 탄소 1 %** | E3329–E3330 |
| 입경 | 레이저 회절 **d50 19.5 µm** · 평균 흑연 입자 반지름 **9.7 µm** (Table I, measured) | E3330 · Table I |
| 두께 | 에폭시 함침 · 연마 단면의 **광학 현미경** 관찰 | E3330 |
| 기공률 | **무게 · 조성**에서 평균 (*"Mean electrode porosity is evaluated from weight and composition"*) | E3330 |
| 전극 수 | **16** = 적재 4 (**4.8 · 8.8 · 11.9 · 15.7 mg/cm²**) × 기공 4 (본문 "between 10 and 40%") | E3330 |
| 셀 | 아르곤 글러브박스 · **대칭 코인셀** · 같은 배치에서 뚫은 **14 mm** 원판 두 장 · 분리막 **Celgard 2500 (25 µm)** | E3330 |
| 전해질 | **EC:DEC (1:1 wt%) + 1 M LiPF₆ (LP40)** — *"conveniently selected because its transport properties were reported in different publications"* [27, 28] | E3330 |
| 차단 실현 | 비삽입 염이 아니다 — **원상태 (pristine) 흑연 + 개방회로**: *"blocking electrodes, i.e., Li insertion/de-insertion does not occur"* | E3330 |
| EIS | 개방회로 · **1 MHz–1 mHz** · 진폭 **5 mV** · VMP3 (Bio-logic) · *"Impedance data are repeatable for all electrode designs"* | E3330 |
| 대칭셀의 장점 (원문) | 기준전극을 피한다 — 기준전극의 크기 · 위치가 임피던스를 왜곡할 수 있어서 [29, 30] | E3330 |
| 온도 | Table I "at 25 °C" (측정 온도를 따로 적지 않는다) | Table I (E3332) |

### 3-2. 고정 매개변수 — Table I (E3332, stated; 표지 a = assumed · m = measured · s = set · dj = Djian [51] · e = Ender [47] · lu = Lundgren [28])

| 매개변수 | 값 | 표지 | 카드 메모 |
|---|---|---|---|
| Separator thickness | 25 × 10⁻⁶ m | m | — |
| Separator porosity | 0.55 | dj | ⚠ landesfeind2016 카드 기록: Djian 의 Celgard 2500 은 **23 µm · 0.47** (§10-3) |
| Separator tortuosity | **6.25** | dj | Z_sep = L_sep·τ_sep/(ε_sep·κ) = **3.59 × 10⁻⁴ Ω m²** · N_M 11.4 (카드 산술).  ⚠ landesfeind2016 카드: Celgard 2500 실측 τ **2.5 ± 0.2** (N_M 4.5) → 그 값이면 1.43 × 10⁻⁴ (카드 산술) |
| Initial salt concentration | 1000 mol m⁻³ | s | — |
| Solid phase conductivity | **2203.8 S m⁻¹** | e | ⚠ Eq 7 의 σ (고유) 인지 σ_eff (유효) 인지 표기 없음 — 출처 [47] 은 *"measuring the effective conductivity … of porous electrodes"* |
| Mean graphite particle radius | 9.7 × 10⁻⁶ m | m | Eq 13 의 ⟨R⟩ |
| Li⁺ conductivity | **0.792 S m⁻¹** | lu | Eq 8 의 κ = **σ₀** |
| Li⁺ molar diffusion coefficient (P2D only) | 2.68 × 10⁻¹⁰ m² s⁻¹ | lu | — |
| Li⁺ transference number (P2D only) | 0.162 | lu | — |
| Thermodynamic factor (P2D only) | 1.63 | lu | — |
| Initial state of charge (P2D only) | 0 | s | — |

- **표에 없는 것**: τ₁ · ε₁ (고상 레일) · n (사다리 노드 수) · 적합 주파수 창 · 그림 2 모의의 전극 매개변수 · 오차 막대 정의.

### 3-3. 적합 결과 (stated)

| 양 | 값 | 쪽 |
|---|---|---|
| τ₂ 범위 | *"Tortuosity ranges from 5.5 to about 9"* (E3332) · *"pore tortuosity values lie between 5 and 9 for porosities ranging from 45 to 10%"* (E3333) | E3332 · E3333 |
| 멱법칙 (그림 6 범례) | 4.8 mg/cm²: **τ₂ = 3.19 ε₂^−0.46** · 8.8: **4.29 ε₂^−0.23** · 11.9: **3.88 ε₂^−0.43** · 15.7: **3.42 ε₂^−0.50** | 그림 6 (E3333) |
| 8.8 제외 요약 | *"the pre-exponential coefficient varies between 3 and 4 while the porosity exponent is around 0.46"* — *"a translated Bruggeman relation"* | E3332 |
| 8.8 의 이상 (원문 해석) | 멱법칙이 최저 기공 점에 민감 · 이 적재가 **가장 낮은 기공 설계**를 가진다 · 그 점의 τ₂ 가 크게 흩어진다 → 나쁜 젖음 또는 원판 간 국소 기공 비균질 | E3332 |
| Q₀ | 16 전극 평균 **0.93 F m⁻²_ASA s^−(1−α)** — HOPG edge plane 문헌 **0.6–1.5 F m⁻²_ASA** [48, 49] 와 맞음 · edge/basal 분리는 불가 | E3331 |
| Q₀ 추세 | 네 적재 모두 **기공이 줄수록 Q₀ ↑** (그림 5) → 저기공 전극의 a 를 과소 추정했을 가능성 — *"pseudo-capacitance and specific interfacial area cannot be determined unequivocally"* | E3331–E3332 |
| α | 평균 **0.95** — *"which validates the use of a CPE in the TLM"* | E3332 |
| 감도 | *"As the porosity reaches values below 15%, the model becomes more sensitive to the input porosity value. Variation of 1% of porosity can lead to fitted pore tortuosity variation of about 0.75."* | E3332 |
| 적재 간 흩어짐의 원인 (원문) | ① 두께 · 기공 결정 오차 (그림 6 세로 오차막대에 **미포함**) — 설계별 평균 기공을 쓰는데 전극마다 두께가 조금씩 다르다 · 적재가 클수록 기공 오차가 줄어 **고적재 τ₂ 가 더 믿을 만** ② 모형이 기술하지 않는 국소 비균질 | E3332–E3333 |
| 문헌 비교 (원문 재인용 — 원 논문 대조 안 함) | Wood 그룹 [20] 판상 흑연 3D 재구성 수치 확산 관통 τ **≈ 6 @ 40 %** · Wheeler 그룹 [22, 23] SFG 흑연 restricted-diffusion (Li/Li 대칭셀) **7.5 @ 35 %** (E3329) · Wheeler 등 *"4.8 ε^−0.53"* 다른 흑연 (E3332, 문장에 번호 없음 — 바로 앞 문장 = Thorat [23]) | E3329 · E3332 |

### 3-4. 그림 6 점 판독 (≈ · 추세 전용 · 가로 ±1 %p · 세로 ±0.2)

| 적재 (mg/cm²) | (기공률 %, τ₂) 네 점 — 판독 |
|---|---|
| 4.8 | (≈ 12, ≈ 9.0) · (≈ 18, ≈ 6.1) · (≈ 32, ≈ 5.7) · (≈ 40, ≈ 5.0) |
| 8.8 | (≈ 10, ≈ 7.2) · (≈ 21, ≈ 5.9) · (≈ 38, ≈ 5.5) · (≈ 43, ≈ 5.0) |
| 11.9 | (≈ 18, ≈ 8.0) · (≈ 29, ≈ 6.3) · (≈ 37, ≈ 6.2) · (≈ 44, ≈ 5.4) |
| 15.7 | (≈ 14, ≈ 9.2) · (≈ 25, ≈ 6.7) · (≈ 38, ≈ 5.8) · (≈ 41, ≈ 5.2) |

- 판독 최저 ≈ 5.0 · 최고 ≈ 9.2, 기공 ≈ 10–44 % → 결론 문장 "5 and 9 · 45 to 10%" 와 맞고, "5.5 to about 9" (E3332) · "between 10 and 40%" (E3330) 와는 끝이 조금 어긋난다 (§10-3).
- Bruggeman 곡선 검산: 그림의 검은 점선이 ε 0.05 에서 ≈ 4.5 · 0.40 에서 ≈ 1.6 = ε^−0.5 (4.47 · 1.58, 카드 산술) — **τ₂ 축 = tau2 척도** (√ 아님) 확인.

### 3-5. 카드 산술 (원문 수치로 계산 — 측정 아님)

| 양 | 식 | 값 |
|---|---|---|
| Bruggeman 배수 | τ₂ ÷ ε₂^−0.5 = A·ε₂^(0.5 − b), ε₂ 0.10 → 0.45 | 4.8: 2.91 → 3.09 · 8.8: 2.30 → 3.46 · 11.9: 3.30 → 3.67 · 15.7: 3.42 (일정) ⇒ **2.3–3.7** |
| MacMullin 수 (원문에 없는 이름) | N_M = κ/κ_eff = τ₂/ε₂ | τ₂ 5.0 @ 0.40 → 12.5 · τ₂ 9.0 @ 0.12 → 75 (판독 점) |
| f (= κ_eff/κ) | ε₂/τ₂ | 0.080 (5.0 @ 0.40) · 0.013 (9.0 @ 0.12) |
| 분리막 직렬 | Z_sep = L_sep·τ_sep/(ε_sep·κ) | **3.59 × 10⁻⁴ Ω m²** (Table I) · 1.43 × 10⁻⁴ (landesfeind2016 τ 2.5 대입) |
| β = R_e/R_i (흑연) | R_i = L·τ₂/(ε₂κ) · R_e = L/σ_eff | L 65 µm · ε₂ 0.37 · τ₂ 5–9 → R_i 1.1–2.0 × 10⁻³ Ω m² · 2203.8 를 σ_eff 로 → R_e 2.9 × 10⁻⁸ → **β 1.5–2.7 × 10⁻⁵**.  2203.8 을 고유 σ 로, ε₁/τ₁ = 0.6/10 (가정) → β 2.5–4.4 × 10⁻⁴ |
| 감도 재현 | R_ion 고정이면 Δτ₂/τ₂ = Δε₂/ε₂ | ε₂ 0.12 · τ₂ 9 · Δε₂ 0.01 → **Δτ₂ 0.75** (원문 수치와 일치) |

## 4. ★ 방법 — 식의 사슬 (원문 번호 그대로) + 측정 · 적합

### 4-1. 정의식 (E3330–E3331, 렌더 판독)

| 식 | 원문 형태 | 뜻 · 비고 |
|---|---|---|
| **Eq 1** | F_obj = (F^Re_obj ; F^Im_obj) · F^Re_obj = ((Z^exp_Re,i − Z^sim_Re,i)/Z^exp_Re,i)_{i∈f} · F^Im_obj 같은 꼴 (Im) | **상대 잔차** 목적함수 — Matlab `lsqnonlin` · f = 실험 주파수 영역 |
| Eq 2 | Z̃_e ĩ_e,k + Z̃_t ĩ_t,k+1 = Z̃_t ĩ_t,k + Z̃_i ĩ_i,k (k = 1 … n−1) | 고리 전압 (Kirchhoff 전압 법칙) |
| Eq 3 | ĩ_e,k−1 = ĩ_e,k + ĩ_t,k (k = 2 … n) | 전자 레일 마디 |
| Eq 4 | ĩ_i,k + ĩ_t,k+1 = ĩ_i,k+1 (k = 1 … n−1) | 이온 레일 마디 |
| **Eq 5** | k = 1: ĩ_e,1 + ĩ_t,1 = 1 | **집전체 쪽**: 전류 전부가 전자로 들어온다 (이온 레일 왼끝은 열림) |
| **Eq 6** | k = n: ĩ_i,n = 1 · ĩ_e,n = 0 | **분리막 쪽**: 전류 전부가 이온으로 나간다 (전자 레일 오른끝은 열림) |
| **Eq 7** | Z̃_e = L_el/((n − 1)σ_eff) · **σ_eff = (ε₁/τ₁)σ** | 고상 전자 레일 — σ = *"electronic conductivity of the electrode matrix"* · ε₁ = *"solid-phase volume fraction"* · τ₁ = *"solid-phase tortuosity"* |
| **Eq 8** | Z̃_i = L_el/((n − 1)κ_eff) · **κ_eff = (ε₂/τ₂)κ** | 액상 이온 레일 — κ = 전해질 전도도 · ε₂ = 전해질 부피분율 · τ₂ = *"electrolyte tortuosity"* |
| **Eq 9** | Z̃_t = 1/((jω)^α Q) · Q = Q₀ L_el a/(n − 1) | 가로대 = **CPE 만** (전하이동 가지 없음 = 차단) · a = ASA/전극 부피 [m²_ASA m⁻³] · Q₀ [F m⁻²_ASA s^−(1−α)] · Q [F m⁻²_SA s^−(1−α)] |
| Eq 10 | Z̃_el = Z̃_e Σ_{k=1}^{n−1} ĩ_e,k + Z_t ĩ_t,n | 전극 임피던스 (행렬 해에서) — 인쇄본 둘째 항 Z_t 에 물결표 없음 (§10-3) |
| **Eq 11** | Z̃_el = [1/(1/Z̃′_e + 1/Z̃′_i)] · [1 + (2 + (Z̃′_e/Z̃′_i + Z̃′_i/Z̃′_e)·cosh √((Z̃′_e + Z̃′_i)/Z̃′_t)) / (√((Z̃′_e + Z̃′_i)/Z̃′_t)·sinh √((Z̃′_e + Z̃′_i)/Z̃′_t))] · Z̃′_e = (n−1)Z̃_e · Z̃′_i = (n−1)Z̃_i · Z̃′_t = Z̃_t/(n−1) | **해석해 (Tröltzsch–Kanoun [37])** — n 이 약분된다 |
| **Eq 12** | Z̃_cell = Z̃_sep + 2Z̃_el · Z̃_sep = L_sep/((ε_sep/τ_sep)κ) | 대칭셀 = 분리막 + 전극 둘 · 분리막도 같은 (ε/τ) 꼴 |
| **Eq 13** | a = 3ε_AM/⟨R⟩ | 구형 가정의 비표면적 — *"the same as that used for intercalation"* → 도전 탄소 위 이중층 충방전 없다는 가정을 품는다 |

- 원소의 뜻 (우리 유도 — 원문은 정의만): Z̃′_e = L_el/σ_eff = **전자 레일 총저항 R_e** · Z̃′_i = L_el/κ_eff = **이온 레일 총저항 R_i** · Z̃′_t = 1/((jω)^α Q₀ a L_el) = **계면 총임피던스 Z_t** (모두 전극 기하 면적당, Ω m²_SA).
  ⇒ Eq 11 = R_eR_i/(R_e+R_i) · [1 + (2 + (R_e/R_i + R_i/R_e) cosh ν)/(ν sinh ν)], **ν = √((R_e + R_i)/Z_t)**.

### 4-2. 회로 위상과 경계조건 (그림 1 · E3330)
- 3n 미지수 (마디마다 ĩ_e,k · ĩ_i,k · ĩ_t,k) 와 3n 식 (Eq 2–6) · 전류는 총전류 Ĩ 로 무차원화 (*"all currents are dimensionless quantities"*).  ĩ_i,1 = ĩ_t,1 은 따로 적히지 않았지만 Eq 3–5 에서 나온다 (우리 유도).
- *"The above system of equations is implemented in a Matlab script and all normalized current variables are readily solved for by matrix inversion"* → Eq 10.  *"Alternately"* Eq 11.  **적합에 어느 쪽을 썼는지 · n 값은 원문에 없다.**
- 차단: *"Because electrodes are in blocking condition, liquid-phase diffusion is neglected"* (E3330) — 가로대에 전하이동 저항이 없고, 확산 무시는 P2D 비교로 확인 (그림 2).
- **Siroma 표 2 위상 매핑** (siroma 카드 §4-2 · 표 2 전사 기준): 단자가 서로 다른 레일의 반대 끝 = **Z형** · 양 끝 외부 요소 없음 = **"open–open"** ·
  z_A (이온 레일 비저항) = 1/κ_eff · z_C (전자 레일 비저항) = 1/σ_eff · z_B = 1/((jω)^α Q₀ a) · Siroma 의 β (= √((z_A + z_C)/z_B)·L) = 위 ν.
  Siroma 는 위 레일 = 이온 · 단자 + 를 이온 레일 x = 0 에 둔다 — Malifarge 그림은 위 레일 = 전자 · 전자 단자를 왼끝에 둔다.  거울상 (x → L − x) 이고 식이 레일 교환에 대칭이라 같은 답이다.

### 4-3. 같은 함수 대조 — 앞 묶음 카드 (우리 유도 + 우리 재계산)

| 출처 (카드) | 그 카드의 식 | Malifarge Eq 11 과 같아지는 조건 | 확인 |
|---|---|---|---|
| Siroma 2015 표 2 Z형 **open–open** (`siroma2015_…` §4-3) | Z = z_A z_C L/(z_A + z_C) + √z_B/(z_A + z_C)^(3/2) · [(z_A² + z_C²) cosh β + 2 z_A z_C]/sinh β | 조건 없음 (위 매핑) | 대수 전개 = 같은 세 항 (병렬 항 · (R_e²+R_i²)/(R_e+R_i) · coth ν/ν · 2R_eR_i/(R_e+R_i) · 1/(ν sinh ν)) · **수치 상대차 ≤ 4·10⁻¹⁶** (β = 10⁻⁴ … 10, 5 주파수, α 0.95) |
| Siroma 원문 문장 | *"the 'open–open' condition in Table 2 is identical to Eq. (12) in Ref. [16]"* ([16] = Tröltzsch & Kanoun 2012) | — | **같은 출처** = Malifarge [37] |
| Landesfeind 2018 **Eq 1** (Göhr [7], `landesfeind2018_…` §4-1) | Z_El = Z_∥ + Z*·{1 + 2ps[√(1 − tanh²ν) − 1]}/tanh ν · Z* = √((Z₁+Z₂)Z_S) · p = Z₂/(Z₁+Z₂) · s = Z₁/(Z₁+Z₂) | R_CT → ∞ (Eq 8 차단판) | √(1 − tanh²ν) = sech ν 로 펼치면 같은 세 항 (우리 유도) |
| Pouraghajan 2018 **Eq 5** (`pouraghajan2018_…` §8-0 ⑤ 의 축약식) | Z_EL = R_ion·[β/(1+β) + (1 + 2β·sech λL + β²)/((1+β)·λL·tanh λL)] (Z₀ → ∞) · β_P = k_eff/σ_eff | Z₀ → ∞ (전해질–집전체 차단) · Z_cc → 0 (고상–집전체 접촉 0) · z_s = CPE (R_ct → ∞) | β_P = R_e/R_i · λL = ν 로 대수 일치 (우리 유도) |
| Kaiser 2018 Eq 4–5 · Nguyen Eq 4 · Landesfeind 2016 TLM-Q | √(R_i Z_t)·coth √(R_i/Z_t) (+ 직렬) | **R_e → 0** = Siroma 표 2 "open–open (z_C = 0)" (de Levie) | Eq 11 의 R_e → 0 극한 (우리 유도) |
| **Minnmann 2021 식 [1]** (= Siroma 표 3 T형 open–open) | z_A z_C L/(z_A+z_C) + 2 z_A² √z_B/(z_A+z_C)^(3/2) · (cosh β − 1)/sinh β | — | **다른 꼴** — 관통형 (단자가 같은 레일 양 끝; DC → 단자 레일 저항 전부, siroma 카드 §0 ②) |

- ⇒ **한 함수, 네 표기**.  Malifarge 의 고유 기여는 해석식이 아니라 ① 행렬 Kirchhoff 판 (Eq 2–10) ② 원소를 P2D 물성 (L · σ · ε · τ · κ · a · Q₀) 으로 쓴 매개변수화 (Eq 7–9 · 12–13)
  ③ P2D 주파수영역 모의와의 일치 (그림 2) ④ 흑연 16 전극 적용이다.
- 사다리 판 (Eq 2–10) 은 노드 n 개에 가로대 n 개 (각 Q/(n−1)) 라 끝점 가중이 없어 **O(1/n)** 로 Eq 11 에 수렴한다 — n·상대차 ≈ 0.89 (β 0.1 · ω 1 · α 0.95; n = 101 · 401 · 1601 에서 같은 값, 우리 재계산) → n ≥ 100 이면 < 1 %.  원문 n 미기재.

### 4-4. 극한 · 대칭 · 오차 지도 (우리 유도 · 수치 확인 — 원문에 이 문장들은 없다)

| 양 | 식 | 비고 |
|---|---|---|
| 고주파 (Z_t → 0) | Z_el → **R_eR_i/(R_e + R_i)** (두 레일 병렬) | 흑연 (β ~10⁻⁵) 에선 ≈ R_e ≈ 0 |
| 저주파 (Z_t 용량성 → ∞) | Re Z_el → **(R_e + R_i)/3** · Im → CPE 항 1/((jω)^α Q₀ a L) | R_e = 0 이면 de Levie 의 R_i/3 |
| 셀 (Eq 12) | Z_cell(ω→∞) → Z_sep + 2R_eR_i/(R_e+R_i) · Re Z_cell(ω→0) → Z_sep + 2(R_e+R_i)/3 | 전극 둘 |
| **대칭** | Eq 11 은 **R_e ↔ R_i 교환에 불변** — R_e + R_i · R_eR_i · (R_e/R_i + R_i/R_e) 로만 들어간다 | 예: (R_e, R_i) = (0.2, 1) ↔ (1, 0.2) 에서 Z 가 같다 (수치) |
| **그래프법 오차** | 겉보기 R_ion = 3·(R_lo − R_hi) = **R_i·[(1+β) − 3β/(1+β)]**, β = R_e/R_i | 아래 표 |

| β = R_e/R_i | 0.005 | 0.01 | 0.025 | 0.05 | 0.1 | 0.3 | 0.5 | 0.732 | 1 | 2 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 겉보기/참 R_ion | 0.990 | 0.980 | 0.952 | 0.907 | 0.827 | 0.608 | 0.500 | **0.464 (최소)** | 0.500 | **1.000** | 8.27 |

- 같은 식이 `landesfeind2018_…` §4-3 ("카드 유도", 원문 Fig 2 의 최저 ≈ 0.46 과 일치) · `pouraghajan2018_…` §8-0 ⑤ ("우리 유도") 에도 있다 — **세 카드가 독립으로 같은 식**에 닿았다.
  ⚠ 그래프법 기준이다.  R_e = 0 모형으로 전 스펙트럼을 맞추면 편향 모양이 다르다 (재계산 안 함).
- **부호**: β < 2 → 과소 · β = 2 → 우연 일치 · β > 2 → 과대.  β ≫ 1 이면 그래프법은 **R_e 를 R_ion 으로 읽는다** (8.27 @ β 10).

### 4-5. τ₂ 추출 절차 (원문 순서 · E3330–E3332)
1. 전극마다 L_el (광학 단면) · ε₂ (무게 · 조성; **설계별 평균**) 를 잰다.
2. 고정: κ 0.792 S/m (문헌) · σ 2203.8 S/m (문헌) · 분리막 25 µm / 0.55 / 6.25 (측정 · 문헌) · ⟨R⟩ 9.7 µm → a = 3ε_AM/⟨R⟩ (Eq 13).
3. Z_cell = Z_sep + 2Z_el (Eq 12) 을 측정 셀 임피던스에 **전 스펙트럼** 적합 — *"Only three parameters, namely the pseudo double-layer capacitance Q₀, the CPE α exponent, and the pore tortuosity across the electrode τ₂, are fitted"* (E3331) · 목적함수 Eq 1 · `lsqnonlin`.
4. 영역 역할 (원문, E3331): *"the pore tortuosity affects the impedance extent of the second domain while the capacitance only produces a shift of the characteristic frequencies"*.
5. 출력 = τ₂ (κ_eff = (ε₂/τ₂)κ).  **R_ion 을 먼저 뽑지 않는다** (τ₂ 가 직접 매개변수 — R_ion = L_el·τ₂/(ε₂κ) 는 우리 환산) · **MacMullin 수를 쓰지 않는다** (N_M = τ₂/ε₂ 는 카드 산술).
- Eq 12 가 2Z_el 을 명시하므로 τ₂ 는 **전극 하나당** 값이다 — landesfeind2018 카드가 지적한 "R_Ion 전극 수 규약" 혼란이 이 논문에는 없다.

### 4-6. P2D 검증 (그림 2 · E3331)
- *"Prior to analyze data with the TLM model, it is validated against Newman's P2D model for the limiting case where the CPE exponent α is 1, see Fig. 2. This result also confirms that electrolyte diffusion can be safely neglected with the present experimental setup (blocking electrodes)."*
- P2D = 주파수영역 해 [31–34] · Table I 의 "P2D model only" 행 (확산계수 · 수송수 · 열역학 인자 · SOC 0) 이 P2D 에만 들어간다.  그림 2 의 전극 매개변수는 *"identical parameters"* 뿐 — 값 미기재.
- 판독: α = 1 TLM (파란 실선) 이 P2D (검은 ×) 와 영역 I–III 전부에서 겹치고, α = 0.95 (점선) 은 영역 III 에서 기운다.  HF 절편 ≈ **0.36 × 10⁻³ Ω m²** (판독) = Z_sep 3.59 × 10⁻⁴ (카드 산술) — 모의 셀에 Table I 분리막이 들어갔다.
- 의미 (우리 해석): P2D 와 TLM 이 **같은 κ_eff = (ε₂/τ₂)κ 의 같은 τ₂** 를 공유한다는 주파수영역 실증 → τ₂ (tau2 꼴) 가 그대로 P2D 입력 칸이다 (nguyen 카드: 전하이동을 막은 P2D 는 TLM 으로 줄어든다).

### 4-7. Nyquist 세 영역 해석 (E3331)
- **I** (고주파): 케이블 유도 · 전해질 저항 · 저항성 접촉 · **II** (중주파, ~45°): 기공 안 분포 저항 — 전해질 전도도 · 두께 · τ₂ · 전해질 부피분율 (기공 길이 · 반지름) 에 민감 · 신호 침투 깊이는 주파수와 기공 크기에 달림 (큰 기공에 더 깊이) ·
  **III** (용량성): 흑연 표면 이중층 · 이론 기울기 90°.
- 두 기울기 모두 de Levie · Newman 예측보다 낮다 [41, 42]: II 의 45° 이탈 = **기공 모양** (Keiser 병목 기공 [43] · Itagaki 3 척도 프랙탈 [42]) · III 의 이탈 = **전극 성질 비균일** [44, 45] (입자 표면 거칠기 · 쌓임 → 기공 모양 · PoSD [40, 46]).
  Song [40] 은 PoSD 를 de Levie TLM 에 넣어 III 을 맞췄고, 이 논문은 **CPE 로 뭉친다** — *"An α exponent that strongly deviates from one would suggest that the physics-based model is not appropriate"*.
- 그림 3: **두께↑ 또는 기공률↓ → 영역 II 확장**.

### 4-8. 시뮬레이션 · 입자 처리 ★
- **DEM · MPM · FEM 미세구조 없음.**  1D 균질 두 레일 TLM (회로) + 1D Newman P2D (주파수영역, 검증용) — 입자 형상 · 방향은 매개변수 τ₂ · a 안에만 들어간다.
- 입자: 실물 판상 흑연 (d50 19.5 µm) · 집전체와 평행 정렬 (같은 배치 30–60 % [21]) — 모형의 구 가정은 a (Eq 13) 하나 · 이방성은 **관통 방향 τ₂ 하나**로 뭉쳐진다.
- 접촉 · 소성 · 형상 변화: 해당 없음 (액체 전해질의 연속 기공상 — 입자 간 이온 접촉 저항이 없다).
- 고상 레일: 균질 σ_eff (τ₁) — 입자 간 전자 접촉 저항 · 집전체 접촉 요소 없음 (Pouraghajan 의 Z_cc · Z₀ 에 해당하는 것 없음).

### 4-9. 기법 미니 용어집

| 용어 | 뜻 |
|---|---|
| 차단 (blocking) 대칭셀 | 같은 전극 둘 + 분리막 · 전하이동 없이 이중층 충방전만 — 여기서는 원상태 흑연의 개방회로 |
| TLM (transmission-line model) | 고상 · 액상 두 레일과 계면 가로대의 분포 회로 (그림 1) |
| Z형 open–open | 단자가 다른 레일의 반대 끝 · 양 끝 외부 요소 없음 (Siroma 명명) — de Levie R/3 계열 |
| CPE (Q₀, α) | 상수위상요소 — α = 1 이면 순수 축전.  ⚠ **α 는 Bruggeman 지수가 아니다** |
| ASA / SA | active surface area (실제 계면) / surface area of the electrode (기하 면적) |
| P2D | Newman pseudo-2D 다공 전극 모형 — 여기서는 주파수영역 해 |
| β (이 카드) | R_e/R_i = σ_ion,eff/σ_el,eff (같은 L · A) — Pouraghajan 의 β (k_eff/σ_eff) 와 같다.  ⚠ Siroma 의 β 는 다른 양 (= ν = √((z_A+z_C)/z_B)·L) |
| PoSD / PaSD | pore size distribution / particle size distribution |
| `lsqnonlin` | Matlab 비선형 최소제곱 |

## 5. Figure set ★

| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 | 크롭 권고 |
|---|---|---|---|
| 1 (E3330) | 두 레일 이산 사다리 — 위 = 고상 전자 Z̃_e · 아래 = 액상 이온 Z̃_i · 가로대 Z̃_t · 노드 1 … n · 오른끝 Z_sep · L_el | **Z형 open–open 위상**이 그림으로 보인다 (전자 단자 왼끝 · 이온 단자 오른끝 Z_sep) — Siroma 이름표 · Minnmann T형과 가르는 근거 | **1 순위** |
| 2 (E3331) | 모의 Nyquist: P2D (검은 ×) vs TLM α = 1 (실선) · α = 0.95 (점선) · 영역 I / II / III · 250 Hz 표지 | TLM ≡ P2D (α = 1) → τ₂ 가 P2D 입력 τ 와 같은 양 · HF 절편 ≈ Z_sep (판독 ≈ 0.36 × 10⁻³) | **2 순위** |
| 3 (E3331) | 실측 셀 Nyquist 세 설계 — 65 µm / 37 % (검정) · 87 µm / 36 % (빨강) · 67 µm / 19 % (파랑) · 10 / 100 / 1000 / 10000 Hz 표지 | 두께 · 기공이 영역 II 길이를 바꾼다.  ⚠ 시작점 Re ≈ (0.2–0.3) × 10⁻³ (판독) < Table I Z_sep (§10) | 3 순위 |
| 4 (E3332) | 적합 예: 얇은 4.8 (○) vs 두꺼운 15.7 mg/cm² (◇), 기공 ~40 % — Nyquist · 위상 · \|Z\| | 적합 품질 — 위상 고주파 평탄 ≈ −42° (판독, 영역 II) · 저주파 ≈ −84 ~ −85° (판독; CPE α 0.95 의 −90α = −85.5°, 카드 산술) · ⚠ 시작점 ≈ 0 · \|Z\|(10 kHz) ≈ 1.1–1.3 × 10⁻⁴ (판독) | 2–3 순위 |
| 5 (E3332) | Q₀ vs 활물질 분율 ε₁ (0.53–0.85, 판독) · 네 적재 · Q₀ ≈ 0.66–1.29 (판독) | Q₀ 가 ε₁ 과 함께 오른다 → Eq 13 (구형 a) 의 한계 신호 — 우리 AM–SE sink 면적 문제 (LHS-25) 의 액체판 유비 | 4 순위 |
| 6 (E3333) | τ₂ vs 기공률 (0–50 %) · 네 적재 패널 · 멱법칙 맞춤 (색 점선) · Bruggeman τ₂ = ε₂^−0.5 (검은 점선) | **핵심 결과** — Bruggeman 의 2.3–3.7 배 (카드 산술) · τ₂ 축 = tau2 척도 (§3-4 검산) | **1 순위** |
| Table I (E3332) | 고정 매개변수 11 행 + 출처 표지 | 분리막 0.55 / 6.25 (Djian) · σ 2203.8 (Ender) · κ 0.792 (Lundgren) — **고정값이 τ₂ 에 들어가는 자리** | **1–2 순위** |

- (선택) Eq 7–11 블록 (E3330 오른쪽 단) 을 식 크롭으로 — §4-3 대조의 원문 근거.

## 6. Post-processing ★
- **무엇**: 전 스펙트럼 비선형 적합 (Eq 1 상대 잔차 — Re · Im 을 각자 실측 성분으로 나눔) → τ₂ · Q₀ · α · 설계별 τ₂(ε₂) 멱법칙 맞춤 (Thorat [23] 이 도입한 전인자 붙은 멱법칙) · Q₀ 의 16 전극 평균 · α 평균.
- **도구**: Matlab 스크립트 (TLM 행렬 해 / 해석식) · `lsqnonlin` (E3330).  P2D 주파수영역 해 (도구 이름 미기재).
- **수치화 · 플롯**: 그림 6 = 설계별 4 점 + 오차막대 (세로 = 정의 미기재 · 두께 · 기공 오차 **미포함**, E3333; 가로 = 정의 미기재) + 멱법칙 + Bruggeman.  그림 5 = Q₀ vs ε₁.
- 멱법칙 맞춤 방법 (가중 · 오차) 미기재.  적합 주파수 창 미기재 (측정 1 MHz–1 mHz · 그림 4 축 10⁻²–10⁴ Hz).
- ⚠ (우리 판단) 상대 잔차 Eq 1 의 Im 성분은 |Z_Im| 이 작은 고주파 점을 크게 가중한다 — 고정된 Z_sep 와 모형 밖 고주파 요소 (케이블 · 접촉) 가 영향을 주는 바로 그 구간이다 (§10).

## § τ 정의 대조 — 우리 규약 매핑

> 우리 규약 = CLAUDE.md ★★ τ 명명 규약 (1저자 비준 10-03).  'tortuosity factor' 는 τ² (`tau2`) 에만 쓴다.

| 원문 기호 (쪽) | 원문 정의식 | 원문 이름 | 정규화 (어느 부피 · 어느 단면 · 어느 σ₀) | 우리 다섯 양 중 | 환산 · 비고 |
|---|---|---|---|---|---|
| κ_eff/κ (Eq 8, E3330) | ε₂/τ₂ | (이름 없음) | σ₀ = 벌크 κ | **f** (`f_ion_<mode>` 꼴) | 0.080 (τ₂ 5.0 @ 0.40) · 0.013 (9.0 @ 0.12) — 판독 점 · 카드 산술 |
| **τ₂** (Eq 8, E3330 · 그림 6) | ε₂·κ/κ_eff | "electrolyte tortuosity" (E3330) · "pore tortuosity" (그림 6 · E3332 · E3333) | **ε₂ = 전극 기공 부피분율** (무게 · 조성, 전극 전체 부피 분모) · 전극 **전체 기하 단면** (Ω m²_SA) · 두께 L_el (광학 단면) · **σ₀ = 벌크 액체 κ 0.792 S/m** (문헌, 25 °C) | **tau2 꼴** (`tau2_ion_<mode>`) — 측정은 차단 Z형 → **τ_e 계열** (Nguyen eSCM) | 균질 1D 에선 관통 tau2 와 같은 수 (siroma 카드).  √τ₂ 는 원문에 없다 |
| **τ₁** (Eq 7, E3330) | ε₁·σ/σ_eff | "solid-phase tortuosity" | ε₁ = "solid-phase volume fraction" (Eq 7) — 그림 5 캡션은 *"active material fraction ε₁"* · σ₀ = σ "electronic conductivity of the electrode matrix" (Table I 2203.8 S/m — σ/σ_eff 구분 없음) | **전자 tau2 꼴** (미래 `tau2_el_<mode>`, 결정 14) | **값 미보고** |
| τ_sep (Eq 12 · Table I) | ε_sep·κ·L_sep/Z_sep | "separator tortuosity" | 분리막 기공 0.55 · 같은 κ | 관통 tau2 (분리막엔 계면이 없다) | 6.25 (Djian [51] 고정) ↔ landesfeind2016 카드 Celgard 2500 실측 2.5 ± 0.2 |
| Bruggeman (그림 6) | τ₂ = ε₂^−0.5 | "Bruggeman relation" [17] | — | T_B = φ^−½ | **T 지수 0.5 (Landesfeind 관례)** ⇔ f = ε^1.5 (Tjaden · COMSOL 의 f 지수 1.5) |
| 멱법칙 (그림 6) | τ₂ = A·ε₂^−b | "Power Law Fit" (Thorat [23] 꼴) | — | tau2 의 경험식 | A 3.19–4.29 · b 0.23–0.50 — 전인자 ≠ 1 (Landesfeind 2016 Eq 7 τ = f·ε^−α 꼴) |
| (√τ₂) | 보고 없음 | — | — | **tau** (`tau_ion_<mode>`) — 파생만 | √5 = 2.24 · √9 = 3.00 (카드 산술) |
| τ_geo | 없음 | — | — | **τ_geo** — 해당 없음 | 서론의 Wood/Ebner [20] 값은 3D 재구성 위 **수치 확산** 관통 τ (기하 τ 아님, 원문 서술 E3329) |
| N_M | 낱말 없음 | — | — | 1/f | N_M = τ₂/ε₂ (카드 산술) |
| α (Eq 9) | CPE 지수 | "exponent in the constant-phase element" | — | **기호 충돌** | Bruggeman α 와 다른 양 — 키 · 표에 옮길 때 꼬리표 필수 |

**σ₀ 기준**: 벌크 액체 전해질 (1 M LiPF₆ EC:DEC) 의 **문헌 전도도** 0.792 S/m @ 25 °C (Lundgren [28]) — 배치 실측이 아니고, 액체는 연속상이라 "순수 상 = 1" 의 기준이 모호하지 않다
(부록 결론 ② 의 셋 중 **"벌크/치밀 고유 = 1"** 부류).  우리 망 σ₀ 3.0 mS/cm (LPSCl 펠릿값, `CL-91`) 는 망 안에서 약분되지만 (메모 v2 §3-1), 실험 τ₂ 는 **가정한 κ 에 정비례**한다 — 이 논문에서는 κ 가 문헌값이라 배치 κ 의 차이가 τ₂ 에 그대로 들어간다.

**환산 사슬 (한 줄로)**:
```
f      = κ_eff/κ        = ε₂/τ₂                         (Eq 8)
τ₂     = ε₂·κ/κ_eff     ↔ tau2 (꼴) ;  N_M = τ₂/ε₂ ;  tau = √τ₂ (원문에 없음)
R_i    = L_el·τ₂/(ε₂·κ) ;  R_e = L_el·τ₁/(ε₁·σ)          (Eq 7–8 의 Z̃′ — 우리 표기)
Z_cell = Z_sep + 2·Z_el(R_e, R_i, Z_t)                   (Eq 11–12 — Z_el 은 R_e ↔ R_i 대칭)
Bruggeman: τ₂ = ε₂^−0.5  ⇔  f = ε₂^1.5                  (T 지수 0.5 관례)
```

**판정**:
1. τ₂ 는 **우리 tau2 와 같은 꼴**이다 (전체 단면 · 전극 두께 · 상 부피분율 정규화).  다른 것은 **경계조건** (차단 Z형 = τ_e 계열 ↔ 우리 두 띠 Dirichlet 관통) · **σ₀** (벌크 액체 ↔ 펠릿 위 Holm) · **수송 상** (연속 액체 ↔ 접촉망) 이다.
2. τ₁ (고상) 은 같은 꼴의 **전자 tau2** 정의가 P2D 표준이라는 원문 사례다 — 단 값이 없고 σ 가 고유인지 유효인지 표기가 없다 (결정 14 의 σ₀ 짝 문제).
3. 원문은 "tortuosity factor" 라는 이름을 쓰지 않고 "tortuosity" 로 τ² 꼴 양을 부른다 → **이름이 아니라 식으로 판정** (결정 15) 의 또 한 사례.
4. Eq 8 = COMSOL f_e = ε/τ_F 꼴 → τ₂ 숫자가 들어갈 자리는 τ_F 칸이고 σ₀ 짝은 κ 다 (결정 5 와 정합) — 그림 2 가 P2D ↔ TLM 의 τ 공유를 직접 보인다.

## 7. 우리 DEM+MPM 대비  →  `our_dem_baseline.md` (⚠ 이 브랜치에서는 값 자리표시 상태 — 우리 수치는 메모 v2 `docs/reviews/tau_conventions_judgment_v2_20261003.md` 의 유도값으로 적는다)

| 항목 | 이 논문 | 우리 | 같음 / 다름 · 이유 |
|---|---|---|---|
| 역할 (frame[5]) | 수송 절반의 **실험 + 1D 모형** (EIS τ₂) — 압밀 · 기계 · 미세구조 없음 | DEM 접촉망 tau2 (conventional) · STEP3 복셀 (CONTACT_FREE 가지) | 이 논문은 수송 쪽 반쪽만 가진다 |
| frame[4] | 실험 — 원칙적으로 독립 앵커 후보 | 각 모델을 실험에 따로 보정 | ⛔ 액체 LIB 흑연 → 우리 모델을 이 값에 맞추지 않는다 |
| 수송 상 | **액체 전해질 연속 기공상** (접촉 저항 없음) | LPSCl 입자 접촉망 (접촉마다 Holm R_c = 1/(2σa)) | **다른 물리** — 우리 T 의 큰 몫인 SE–SE 협착이 이 계에는 없다 |
| τ 정의 | τ₂ = ε₂κ/κ_eff | T = φ·σ₀/σ_full (`tau2`) | **같은 꼴** |
| 경계조건 | Z형 차단 TLM (τ_e 계열, 균질 1D) | 두 띠 Dirichlet 관통 (conventional) | 균질이면 같은 수 · 비균질 · dead-end 에서 갈림 (nguyen 카드) |
| σ₀ | 벌크 액체 κ (문헌) — 기준 모호성 없음 | 간선 σ₀ 3.0 (펠릿값) + SE–SE Holm 직렬 = 모델 T | 기준 상태 부류가 다르다 (결정 4) |
| φ | ε₂ = 무게 · 조성 기공률 (설계 평균) | φ_SE = 구 부피 합 / 상자 (결정 1 의 φ_mc 로 정리 중) | 정의 다름 · 이 논문은 ε 1 % 가 τ₂ 0.75 를 바꾼다 (ε < 15 %) |
| 입자 | **판상 흑연** 평행 정렬 (d50 19.5 µm) | 강체구 (NMC bimodal + SE) | ⚠ 우리 DEM 은 판상 정렬 이방성을 **표현할 수 없다** — Bruggeman 배수의 형상 기여를 우리 침대가 재현할 이유가 없다 |
| 전자 레일 | TLM 안 (Eq 7) · 흑연이라 무시 가능 | AM 전자망을 **따로** 푼다 (σ_e Stage 22.5) | 우리는 σ_e 를 얻으려고 TLM 이 필요 없다 — TLM 은 **실험 앵커를 읽을 때** 필요 |
| 값 (판정 없이) | τ₂ 5–9 (ε₂ 0.45 → 0.10) | T_H 중앙 6.21 (코퍼스) · φ_SE 띠별 2.65 @ 0.613 … 13.5 @ 0.248 (메모 v2 §3-3 · 1세대 협착식 · 기준 상태 미보정) | **비율을 내지 않는다** — 상 · 재료 · 경계조건 · σ₀ 가 모두 다르다 |
| Bruggeman 배수 | **2.3–3.7** (멱법칙 · 카드 산술) | H 중앙 3.40 (IQR 2.54–6.71) · P 5.42 (메모 v2 §3-5) | 축은 같다 (T ÷ φ^−½) — 숫자가 비슷해 보여도 **같은 원인 (협착 · 형상) 이 아니다**.  "정합" 으로 읽지 말 것 |

- **방법 artifact 와 실제 차이의 구분**: ① 액체 연속상 vs 고체 접촉망 (Holm 협착 유무) ② 판상 흑연 vs 강체구 ③ Z형 차단 (τ_e) vs 관통 ④ σ₀ 부류 (벌크 vs 펠릿 + Holm) ⑤ 판독 vs stated — 다섯이 겹친다.  이 표의 어느 행도 "모델 오차 배수" 를 주지 않는다.
- **frame[5]** — 이 논문이 가진 반쪽 = 수송 (액체 기공 τ₂, 측정 + 1D 해석).  없는 반쪽 = 미세구조 (실제 기공망 · 방향 분포는 [21] 로만) · 기계 (압연 · 정렬 형성).  우리 DEM 은 강체구라 그 반쪽 (판상 정렬) 을 줄 수 없다.

## 8. 적용 인사이트 (내 연구에 어떻게) — 이 묶음이 닫으려는 것

### 8-1. 전자 저항 임의값 대칭셀 TLM (판단 메모 v2 §7 τ_e · §8-2: "ASSB 에서 r_el ≪ r_ion 이 안 설 때")

**(a) 해의 식 — 차단 · 전하전달 없음 · 경계조건**

| 요소 | 원문 | 쪽 |
|---|---|---|
| 차단 | 가로대 = CPE 만 Z̃_t = 1/((jω)^α Q) (Eq 9) · *"Li insertion/de-insertion does not occur"* · 액상 확산 무시 (P2D 로 확인) | E3330 · E3331 |
| 레일 | 고상 전자 Z̃_e = L_el/((n−1)σ_eff), σ_eff = (ε₁/τ₁)σ (Eq 7) · 액상 이온 Z̃_i = L_el/((n−1)κ_eff), κ_eff = (ε₂/τ₂)κ (Eq 8) | E3330 |
| 경계조건 | 집전체 쪽 k = 1: ĩ_e,1 + ĩ_t,1 = 1 (전류는 전자로 들어옴 · 이온 레일 끝 열림, Eq 5) · 분리막 쪽 k = n: ĩ_i,n = 1 · ĩ_e,n = 0 (이온으로 나감 · 전자 레일 끝 열림, Eq 6) | E3330 |
| 해 | 행렬 Kirchhoff (Eq 2–6 → Eq 10) 또는 해석식 Eq 11 (Tröltzsch–Kanoun [37]) = R_eR_i/(R_e+R_i)·[1 + (2 + (R_e/R_i + R_i/R_e) cosh ν)/(ν sinh ν)], ν = √((R_e+R_i)/Z_t) | E3330 |
| 셀 | Z_cell = Z_sep + 2Z_el (Eq 12) | E3331 |
| 위상 | Siroma 표 2 **Z형 open–open (z_C ≠ 0)** = Landesfeind 2018 Eq 1 = Pouraghajan Eq 5 (Z₀ → ∞ · Z_cc → 0) — 같은 함수 (§4-3) | — |

**(b) τ 추출 절차 — MacMullin 수 · ε**
- τ₂ 는 Eq 8 의 **직접 적합 매개변수**다 (자유 셋 = Q₀ · α · τ₂) — R_ion 을 먼저 내거나 MacMullin 수를 거치지 않는다.  ε₂ (설계 평균 기공률) · L_el · κ · σ · 분리막 · ⟨R⟩ 는 고정 (§4-5).
- MacMullin 수는 원문에 없다 — N_M = κ/κ_eff = τ₂/ε₂ (카드 산술; 예 12.5 @ τ₂ 5.0 · ε₂ 0.40).
- ε 이 τ₂ 에 들어가는 길: R_ion 이 스펙트럼으로 정해지면 τ₂ = R_ion·ε₂·κ/L_el 이라 **ε₂ 에 정비례** → 기공률 < 15 % 에서 1 % 입력 차가 τ₂ 0.75 (원문 · 카드 산술 재현).  ⇒ ASSB 판에서는 φ_SE 장부 (기공 포함 · 고체 기준 · 수지) 가 같은 크기로 τ 에 들어간다 (부록 결정 4 ⓑ ε 장부).

**(c) 흑연 비등방 입자 자료와 결과**
- 산업용 흑연 97 % · d50 19.5 µm · 적재 4.8 / 8.8 / 11.9 / 15.7 mg/cm² × 기공 ≈ 10–44 % (판독) · 16 전극 (E3330 · 그림 6).
- τ₂ 5–9 · 멱법칙 A 3.19–4.29 · b 0.23–0.50 · 8.8 제외 A 3–4 · b ≈ 0.46 · Bruggeman 의 2.3–3.7 배 (카드 산술) — 원문: *"It appears like a translated Bruggeman relation which would account for a peculiar electrode microstructure resulting from the anisotropic shape of graphite particles"* (E3332).
- 원인: 판상 입자가 집전체와 평행 정렬 — 평행에 가까운 입자가 압연압에 따라 전체의 30–60 % (같은 배치, [21]) · *"The tortuosity values increase as the amount of graphite particles parallel to the current collector increases"* (E3332).  ⚠ 이 논문 안에서 방향 분율과 τ₂ 를 **전극별로 짝지은 표나 그림은 없다** — 연결은 문장뿐이다.
- 적재 무관이어야 할 τ₂ 가 적재마다 흩어진 원인 = 두께 · 기공 결정 오차 (고적재가 더 믿을 만) + 모형 밖 국소 비균질 (E3332–E3333).

**(d) 전자 저항을 무시했을 때의 오차 크기 — 원문 수치**
- **원문 수치 없음.**  원문 문장은 하나뿐이다: *"No influence of the solid phase conductivity on this domain is observed in the typical range of electronic conductivity reported for graphite electrodes (2000 S.m⁻¹ or more)"* (E3331).  비교한 σ 값들 · 스펙트럼 · 오차는 보이지 않는다.
- 흑연의 β ≈ 1.5–2.7 × 10⁻⁵ (σ = σ_eff 로 읽을 때) ~ 2.5–4.4 × 10⁻⁴ (고유 σ · ε₁/τ₁ = 0.6/10 가정) (카드 산술, §3-5) — 오차 표 (§4-4) 에서 < 0.1 % 구간이다.  이 논문은 **전자 레일이 문제가 되는 영역을 시험하지 않았다.**
- 수치가 필요하면 같은 함수의 다른 출처: **Landesfeind 2018** (일반 TLM 모의 — R_El/R_Ion < 10⁻² 정확 · 10⁻²–10⁻¹ 이면 R_Ion 오차 최대 ~20 %, `landesfeind2018_…` §4-2 · A470–A471) · **우리 유도** 그래프법 R_i·[(1+β) − 3β/(1+β)] (§4-4 표 — 세 카드 독립 일치).

**(e) 우리 ASSB 양극에서 이 해가 필요한 조건**

| 조건 | 판정 | 근거 |
|---|---|---|
| 셀 위상 | **Z형 차단 대칭셀** (Bazzoun 형 full-blocking · Kaiser Type-A) 에서만 문제 — 두 레일이 다 열려 있다.  Minnmann 형 (반대 운반체를 막은 T형) 은 DC 극한이 단자 레일 저항뿐이라 β 가 DC 값에 안 들어간다 (고주파 부분만) | siroma 카드 §0 ② · §3-5 |
| β 의 크기 (탄소 없는 NCM–LPSCl · **0 % SoC**) | Minnmann SI Table S2 stated σ_el,eff · σ_ion,eff 로 β = σ_ion,eff/σ_el,eff: **25 vol% CAM 19.8 · 33 vol% 1.13 · 42 vol% 0.299 · 53 vol% 0.0311 · 61 vol% 0.00214** (fine SE 61 vol% 0.0168) (카드 산술) → 그래프법 계수 17.9 · 0.537 · 0.609 · 0.941 · 0.996 (0.967) | `minnmann2021_…` §5.0 (SI Table S2) |
| 우리 생산 조성으로 옮기면 | 우리 AM 70–85 wt% ↔ Minnmann 질량비 m_NCM : m_SE 70:30 (42 vol%) · 80:20 (53) · 86:14 (61) → **β ≈ 0.30 → 0.002** · 그래프법 R_ion **× 0.61 → × 0.996** | 같은 표 (질량비 열) — ⚠ NCM622 · Minnmann 미세구조 · 추세 전용 |
| 차단과 저 σ_e 가 겹친다 | ASSB 의 차단은 원상태 (완전 리튬화, 0 % SoC) NCM 으로 얻는데, 그 상태가 σ_e 가 **가장 낮은** 상태다 — Minnmann σ_el,0 = 10 mS/cm 가 *"fully lithiated NCM"* 값이고 탈리튬화되면 오른다 | `minnmann2021_…` 메타 표 (p.6 · ref [46]) |
| 레일 배정 | β ≳ 1 (≤ 33 vol% CAM) 이면 Eq 11 의 대칭 때문에 스펙트럼만으로 R_ion · R_el 을 가를 수 없다 → **이온 차단 (steel) 셀로 σ_el,eff 를 먼저 재서 R_e 를 고정**하고 R_i 만 맞춘다 (Malifarge 가 σ 를 문헌값으로 고정한 것과 같은 처방) | §4-4 (우리 유도) |
| 탄소 첨가 | VGCF · CNF · 카본블랙이 있으면 σ_el,eff ↑ → β ↓ (크기 [미확인] — 우리 침대별 σ_e 출력으로 계산 가능) | 판단 |
| 우리 모델의 β | 망 출력 σ_ion,eff/σ_e,eff 로 침대마다 계산 가능 — 단 σ_AM 50 mS/cm 는 측정값의 약 10 배인 **모델 기준값** (`CL-92`) 이라 모델 β 는 같은 구조의 실제보다 작게 나온다 | `pouraghajan2018_…` §8-0 ⑦ 과 같은 지적 |
| Bazzoun 앵커 | 카드 기록: *"Z-type TLM EIS 피팅 (R_ion/R_elec/CPE)"* — 두 레일 함수 (Siroma 명명과 같다면 Eq 11 과 같은 함수).  **R_elec 값 · 레일 배정 규칙은 카드에 없다 [미확인]** — CNF 함유라 β 가 작을 가능성 (판단 · 미검증) | `bazzoun2026_dem_fem_rnm_ionic` §5 Fig 4 |

**(f) 판정 한 줄** — 이 논문은 "전자 저항 임의값 대칭셀 TLM" 의 **식 (Eq 7 · 11) 과 P2D 일치 (그림 2)** 를 닫는다.  **오차 크기는 닫지 못한다** (원문 수치 없음 — Landesfeind 2018 · 우리 유도로 메운다).
그리고 메모가 상정한 "r_el ≪ r_ion 이 안 설 때" 에는 이 해만으로 부족하다 — **R_e ↔ R_i 대칭** 때문에 독립 전자 측정이 함께 있어야 R_ion 이 정해진다.

### 8-2. 결정별 인사이트 (메모 v2 §0-2 결정 번호)
- ① **결정 13 (τ_e)** — 권고 **불변** (P2D 열 보류 · "부호 불정" · ML 기술자 문장으로만).  한정어 · 진단 보강 제안:
  ⓐ 실험 τ_e 앵커마다 **TLM 에 전자 레일이 들어갔는지 · R_e 를 고정했는지 맞췄는지 · β** 를 기록한다 (Malifarge = 두 레일 · R_e 고정 (문헌 σ) · β ~10⁻⁵).
  ⓑ **Eq 11 의 R_e ↔ R_i 대칭** → 두 레일 적합은 독립 σ_el,eff 없이는 레일 배정이 정해지지 않는다 (우리 유도).
  ⓒ β-무시 그래프법의 편향 **부호가 β = 2 에서 뒤집힌다** (과소 → 과대) — "부호 불정" 에 실험 쪽 기전이 하나 더 붙는다.
  ⓓ 메모 §7 최소안의 "AM 등전위" 가정은 Minnmann 실측 β 로 **질량비 80:20 이상 (β ≲ 0.03)** 에서만 그래프법 6 % 안이다 — 70:30 (β 0.30) 이면 × 0.61 (카드 산술).
- ② **결정 14 (전자 · 열 T)** — 권고 **불변**.  보강: Eq 7 의 σ_eff = (ε₁/τ₁)σ 는 "단일 σ₀ 기준 전자 tau2" 의 **P2D 표준 꼴**이라는 원문 사례다.  그러나 이 논문 자신이 함정을 보인다 — Table I "Solid phase conductivity 2203.8" 이 유효값 측정법 [47] 에서 왔는데 σ 인지 σ_eff 인지 적지 않았고, ε₁ 은 Eq 7 에서 "고상", 그림 5 에서 "활물질" 분율이다.
  ⇒ 전자 tau2 를 실을 때 **σ₀ 종류 (고유 / 유효) 와 φ 기준 (AM 만 / 탄소 포함 전 고체)** 을 메타 (`phi_basis` · `*_sigma0_*`, 결정 15) 로 둔다.  전자 T 의 실험 앵커는 **이온 차단 관통형** (Minnmann steel 셀) 이 깨끗하다 — Z형 차단 셀의 R_e 는 R_i 와 **순서 없는 짝**이다.
- ③ **결정 5 (COMSOL 표기)** — 권고 **불변**.  지지: P2D 와 TLM 이 같은 κ_eff = (ε₂/τ₂)κ 의 같은 τ₂ 를 공유함을 주파수영역 모의로 확인한 사례 (그림 2, α = 1) → τ₂ (tau2 꼴, √ 아님) 가 P2D/COMSOL τ 칸의 양이다.  "EIS" 표지에는 연결형 (Z형 = τ_e 계열) 을 병기한다 (부록 결정 5 한정어와 같은 방향).
- ④ **결정 15 (키 이름)** — 권고 **불변**.  "pore tortuosity" 라는 이름의 tau2 — 이름이 아니라 식으로 판정하는 원칙의 또 한 사례.
- ⑤ 결정 4 · 9 · 11 — **해당 없음** (액체 연속상 · 접촉 면적 없음 · 협착 없음).  σ₀ 부류만 기록: "벌크 = 1" (부록 결론 ② 의 첫 부류).

## 9. 인용 가능 문장 (deck/paper용)
- "Malifarge et al. extracted the pore tortuosity τ₂ by fitting the full impedance spectrum of blocking-electrode symmetric cells with a two-rail transmission-line model parameterized as in Newman's porous-electrode theory, κ_eff = (ε₂/τ₂)κ (J. Electrochem. Soc. 164 (2017) E3329, Eqs. 7–12); τ₂ is therefore a tortuosity-factor (τ²-type) quantity referenced to the bulk electrolyte conductivity."
- "For industrial graphite electrodes made of platelet-shaped particles, τ₂ ranged from about 5 to 9 for porosities between about 45 % and 10 %, roughly three times the Bruggeman value ε^−0.5, and followed power laws τ₂ = A·ε₂^−b with A ≈ 3–4 and b ≈ 0.46 when one loading was excluded."
- "Their analytic electrode impedance (Eq. 11, after Tröltzsch and Kanoun) is the Z-type 'open–open' transmission-line solution with a finite electronic rail; because it is symmetric in the electronic and ionic rail resistances, one blocking spectrum cannot assign the two resistances without independent knowledge of the electronic conductivity (our derivation)."
- "The electronic rail was negligible for graphite (σ ≈ 2.2 × 10³ S m⁻¹), so the paper does not quantify the error of neglecting it; that error has to be taken from the general transmission-line analysis (e.g. Landesfeind et al., J. Electrochem. Soc. 165 (2018) A469)."

## 10. 주의/한계 (over-claim 방지)
- ⚠ **재료 전이 없음**: 액체 LP40 + 판상 흑연 음극 ↔ LPSCl + NMC811 고체 복합 양극.  τ₂ 의 숫자 · 멱법칙 계수를 우리 계로 옮기지 않는다 (정의 · 방법만 전이).
- ⚠ **전자 레일은 식에만 있다** — 이 논문의 자료는 β ~10⁻⁵ 영역뿐이라 Eq 11 의 전자 레일 기능을 **검증하지 않는다**.  "전자 저항 임의값 TLM 을 실험으로 확인한 논문" 으로 인용하지 말 것.
- ⚠ **고정 매개변수가 τ₂ 를 정한다** — 분리막 (Djian 0.55 / 6.25) · σ (Ender) · κ (Lundgren) 를 고정했고 맞춘 것은 셋뿐이다.  Z_sep 를 Table I 로 계산하면 3.59 × 10⁻⁴ Ω m² 인데 같은 분리막의 다른 실측 (landesfeind2016 카드 τ 2.5) 이면 1.43 × 10⁻⁴ 로 2.5 배 작다 (카드 산술) → τ₂ 편향 크기 · 방향은 원 자료 없이 판정 불가.
- ⚠ **고주파 처리 미설명 (판독)** — 그림 3 의 셀 스펙트럼은 Re ≈ (0.2–0.3) × 10⁻³ Ω m² 에서 시작해 Table I Z_sep (3.59 × 10⁻⁴) 보다 작고, 그림 4 는 시작점 ≈ 0 · |Z|(10 kHz) ≈ 1.1–1.3 × 10⁻⁴ 다.  그림 4 가 고주파 직렬 성분을 뺀 전극 임피던스인지, 적합의 Z_sep 가 Table I 값 그대로인지 원문에 없다.  판독 정밀도가 낮아 결함 판정은 아니고 **원 자료 확인 과제**다.
- ⚠ **상대 잔차 가중 (우리 판단)** — Eq 1 의 Im 성분이 |Z_Im| 작은 고주파 점을 크게 가중한다 → 위 고주파 처리 문제가 τ₂ 에 들어갈 통로가 된다.
- ⚠ **a 의 구형 가정 (Eq 13)** — Q₀ 가 기공에 따라 오르는 것 (그림 5) 을 원문이 a 과소 추정 가능성으로 읽고, Q₀ 와 a 를 *"unequivocally"* 정할 수 없다고 인정한다 (E3332).  τ₂ 는 영역 II 길이로 정해져 Q₀ 와 상관이 약하다는 원문 서술 (E3331) 은 있지만 상관 계수 · 신뢰구간은 없다.
- ⚠ **설계 평균 기공** — 전극별 기공을 쓰지 않았다 (원문 인정).  ε < 15 % 에서 1 % 차 → τ₂ 0.75.  오차 막대 정의 미기재 (세로는 두께 · 기공 오차 미포함).
- ⚠ **8.8 mg/cm² 의 지수 −0.23** 은 원문이 최저 기공 점 민감 · 젖음 · 비균질로 설명할 뿐 재측정하지 않았다.
- ⚠ **이방성 연결은 문장뿐** — 방향 분율 30–60 % ([21]) 과 τ₂ 를 전극별로 짝지은 자료가 이 논문에 없다.
- ⚠ **균질 1D TLM** — dead-end 기공 · 방향성 · 두께 방향 구배를 못 본다 (τ_e 계열의 한계, nguyen 카드).  τ₂ 는 그 가정 아래의 유효값이다.
- ⚠ 문헌 비교값 (Wood ≈ 6 @ 40 % · Wheeler 7.5 @ 35 % · 4.8 ε^−0.53) 은 **원문 재인용** — 원 논문과 대조하지 않았다.
- ⚠ 원문이 적은 후속 계획 (Wheeler 법과 비교 · 다른 입자 형상 · *"lithiated electrodes (positive electrode materials)"* 로 확장, E3333) 은 이 논문에서 수행되지 않았다.
- ⚠ 시뮬레이션 없음 — DEM · MPM 어느 쪽의 검증도 아니다 (frame[4]: 액체 LIB 실험이라 우리 앵커 후보도 아니다).

### 10-1. 메모 v2 정정 후보 (`docs/reviews/tau_conventions_judgment_v2_20261003.md` · 부록 `…_addendum_lit10_20261003.md`)
1. **§8-2 Malifarge 행** — *"전자 저항 임의값 대칭셀 TLM — ASSB 에서 r_el ≪ r_ion 이 안 설 때 | §7"*.
   원문 (E3330–E3331) 으로는: 식은 맞다 (Eq 7 · 11) — 단 ① 해석식은 Tröltzsch–Kanoun [37] 의 것 ② 자료는 흑연 σ 2203.8 S/m 뿐이고 *"No influence"* (E3331) — **전자 저항 영역은 시험되지 않았다** ③ 무시 오차 수치 없음 ④ **ASSB 언급 없음** (원문 전수) ⑤ Eq 11 이 R_e ↔ R_i 대칭이라 "r_el ≪ r_ion 이 안 설 때" 는 **독립 전자 측정이 함께 있어야** 쓸 수 있다 (우리 유도).
   → *"두 레일 Z형 TLM 해 (Eq 11 · Tröltzsch–Kanoun) + P2D 일치 (그림 2) · 실측은 R_e 무시 영역 · 오차 크기는 Landesfeind 2018 Fig 1–2 · 레일 배정엔 독립 σ_el,eff 필요"* 로 정밀화 제안.
2. (보강) **§3-5 Bruggeman 배수** 문헌 칸 *"액체 전극 ≈ 1.5–3× (Landesfeind A1386)"* — 판상 흑연 (액체) **2.3–3.7×** (Malifarge 멱법칙 · ε₂ 0.10–0.45 · 카드 산술, 그림 6 E3333) 가 위 끝을 넘는다.  부록 §2 의 Landesfeind 2018 1.96–3.56× · Holzer 1.8–3.1× 와 같은 쪽.
3. (보강) **§7 최소안** *"AM 등전위 (σ_e ≫ σ_ion 가정 — 저 CAM 에서 깨짐, Minnmann τ_el² 120 @25 vol%)"* — 깨지는 경계를 β 로: Minnmann stated σ 로 β ≈ 19.8 (25) · 1.13 (33) · 0.30 (42) · 0.031 (53) · 0.0021 (61 vol%) (카드 산술, minnmann 카드 §5.0) → 그래프법 6 % 안은 **53 vol% (질량비 80:20) 이상**.
4. (보강) **§1 τ_e 행** — Landesfeind Eq 13 옆에 Malifarge τ₂ (Eq 8 · 전 스펙트럼 적합 · 전극 하나당 · E3330–E3331) 를 eSCM 사례로 더할 수 있다.
5. (출처 표지) **부록 §1 결정 13 ⓒ** *"실험 앵커엔 고상 저항 β 보정 (무시하면 R_ion 을 [(1+β) − 3β/(1+β)] 배)"* — 식은 맞다 (Eq 11 로 재현).  다만 **원문 식이 아니라 카드 유도**다 (pouraghajan 카드 §8-0 ⑤ "우리 유도" · landesfeind2018 카드 §4-3 "카드 유도" · 이 카드 §4-4) · **그래프법 기준** · 부호가 β = 2 에서 뒤집힌다 — 이 셋을 한정어로 붙이는 것을 제안.  Malifarge 원문에도 이 식은 없다.

### 10-2. 이 논문을 인용하는 카드의 서술 ↔ 원문 대조 (그 카드는 고치지 않는다 — 메인 판단)

| 카드 · 자리 | 카드 서술 | 원문 대조 | 판정 |
|---|---|---|---|
| `nguyen2020_…` §1 · §4-A 표 · 용어집 | eSCM = *"차단 조건 대칭셀 EIS + TLM 적합"* (Landesfeind 2016 · Malifarge 2017) · *"같은 전극 두 장 (집전체 붙은 채) + 분리막"* · *"차단 대칭셀 + TLM 으로 전극 R_ion"* | 초록 *"transmission-line-model analysis of the electrochemical impedance diagram of symmetric cells containing porous electrodes in blocking condition"* (E3329) · 코인셀 · Celgard 2500 · Cu 집전체 (E3330 · E3333) | **같음**.  보탤 점: Malifarge 는 R_ion 을 먼저 뽑지 않고 **τ₂ 를 직접 맞춘다** · 차단은 비삽입 염이 아니라 **원상태 흑연 + LP40 개방회로** (Landesfeind 2016 의 TBAClO₄ 와 다름) |
| `nguyen2020_…` §4-B | *"확장: Malifarge (ref 18) — 고상 전자저항 임의값 포함 해석식"* | Eq 7 · Eq 11 (E3330) | **같음** — 단 해석식 Eq 11 은 **Tröltzsch–Kanoun [37]** 의 것 (*"Alternately, an analytic solution developed by Tröltzsch and Kanoun"*) · Malifarge 고유는 행렬 판 Eq 2–10 |
| `nguyen2020_…` §11 ref 18 행 | *"고상 전자저항 임의값을 포함한 대칭셀 해석식 — ASSB 처럼 r_el ≪ r_ion 이 안 설 때 필요"* | 앞 절 = Eq 7 · 11.  뒤 절: 원문에 **ASSB 언급 없음** · 자료는 흑연 (β ~10⁻⁵) 이고 *"No influence"* (E3331) | 앞 절 **같음** · 뒤 절은 **카드 작성자의 동기** (원문 주장 아님) — 그리고 그 영역에서는 Eq 11 의 R_e ↔ R_i 대칭 때문에 독립 전자 측정이 함께 필요하다 (우리 유도) |
| `nguyen2020_…` §7 표 | *"실험 앵커 τ — Thorat / Landesfeind / Malifarge 법"* | — | 같음 |
| `pouraghajan2018_…` §11 ref 15 행 | *"고상 전자저항 임의값 포함 대칭셀 TLM (nguyen 카드 ref 18) — β 보정의 독립 출처"* | Malifarge 원문에 **β 보정이 없다** — 극한 (HF R_e∥R_i · LF (R_e+R_i)/3) · 그래프법 겉보기 R_ion · 오차 어느 문장도 없다 (원문 전수).  Eq 11 은 Pouraghajan Eq 5 의 Z₀ → ∞ · Z_cc → 0 · 차단 판과 **같은 함수**이고, 그 해석식의 출처 (Tröltzsch–Kanoun) 는 Pouraghajan 이 비교 대상으로 인용한 [25] 와 **같다** | 앞 절 **같음** · 뒤 절 **어긋남** — "β 보정의 출처" 가 아니다.  쓸 수 있는 것 = **같은 함수의 독립 표기 · 행렬 Kirchhoff 판 (Eq 2–10) 이 식 검산의 독립 경로**.  β 보정식은 pouraghajan · landesfeind2018 카드가 각자 유도한 것 |

### 10-3. 원문 내부 불일치 · 오식 · 미기재 (그대로 두고 표지만)
1. τ₂ 범위: *"5.5 to about 9"* (E3332) ↔ *"between 5 and 9"* (E3333) — 그림 6 판독 최저 ≈ 5.0.
2. 기공 범위: *"between 10 and 40%"* (E3330) ↔ *"ranging from 45 to 10%"* (E3333) — 그림 6 판독 ≈ 10–44 %.
3. ε₁: Eq 7 *"solid-phase volume fraction"* ↔ 그림 5 캡션 *"active material fraction ε₁"* ↔ Eq 13 의 ε_AM (세 이름이 섞인다).
4. Eq 10 둘째 항 Z_t 에 물결표 없음 (인쇄본 표기).
5. Table I "Solid phase conductivity" 가 σ 인지 σ_eff 인지 미기재 (§3-2).
6. **분리막 출처 (교차 카드)**: Table I 은 ε_sep 0.55 · τ_sep 6.25 를 Djian [51] 로 표지 ↔ landesfeind2016 카드 기록: Djian 의 Celgard 2500 = **N_M 13 ± 1.5 · 23 µm · ε 0.47** (그 값이면 τ = N_M·ε ≈ 6.1) · Landesfeind 실측 τ **2.5 ± 0.2** (사양 25 µm · 0.55).  Djian 원문 없이 판정 불가.
7. 미기재: n · 적합에 쓴 해 (행렬 / 해석식) · 적합 주파수 창 · 그림 2 전극 매개변수 · 오차막대 정의 · 멱법칙 맞춤 방법 · 조성당 셀 수.
8. 그림 3 · 4 의 고주파 시작점이 Table I Z_sep 와 맞지 않는다 (판독, §10 본문).
9. 표기: 서론의 *"Wood et al."* 은 [20] (제1저자 Ebner, 교신 Wood) · *"Wheeler and coworkers"* [22, 23] — 그룹 이름 표기 (오류 아님).
10. **선행 연구 누락 (교차 카드)**: 원문 *"to the best of the authors' knowledge, no tortuosity value was extracted from the TLM analysis"* (E3329) ↔ Landesfeind 2016 (J. Electrochem. Soc. 163, A1373, 2016 — 정본 카드 `landesfeind2016_…`) 이 이미 **차단 대칭셀 + TLM 으로 전극 τ** 를 냈다.  Malifarge 참고문헌 51 편에 Landesfeind 2016 이 없다 (원문 목록 전수 · "Landesfeind" · "Gasteiger" 0 회).  ⇒ "TLM 으로 τ 를 낸 첫 논문" 으로 인용하지 말 것 — nguyen 카드처럼 **eSCM 의 두 원전 중 하나**로 쓴다.

## 11. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)

| 서지 (원문 목록 그대로 · 발음 기호만 복원) | 왜 | 정본 카드 |
|---|---|---|
| 37. U. Tröltzsch and O. Kanoun, Generalization of transmission line models for deriving the impedance of diffusion and porous media, Electrochim. Acta., 75, 347 (2012). | Eq 11 의 원전 = Siroma [16] · Pouraghajan [25] 와 같은 논문 — 세 카드의 같은 함수를 원전에서 닫기 · Pouraghajan 유한 Z₀ 가지 판별 | 없음 |
| 26. N. Ogihara, S. Kawauchi, C. Okuda, Y. Itou, Y. Takeuchi, and Y. Ukyo, Theoretical and Experimental Analysis of Porous Electrodes for Lithium-Ion Batteries by Electrochemical Impedance Spectroscopy Using a Symmetric Cell, J. Electrochem. Soc., 159, A1034 (2012). | 대칭셀 TLM 원법 (Li 염 + SOC 0/100 % 차단 — Malifarge 와 같은 차단 실현 방식) | 없음 |
| 23. I. V. Thorat, D. E. Stephenson, N. A. Zacharias, K. Zaghib, J. N. Harb, and D. R. Wheeler, Quantifying tortuosity in porous Li-ion battery materials, J. Power Sources, 188, 592 (2009). | 전인자 붙은 멱법칙의 출처 · eRDM 원조 · "4.8 ε^−0.53" 의 후보 출처 | 같은 묶음 #26 (작성 중 · 그림 폴더 이름으로 보아 예정 slug `thorat2009_quantifying_tortuosity_porous_liion` — 메인 확정) |
| 21. S. Malifarge, B. Delobel, and C. Delacourt, Quantification of preferred orientation in graphite electrodes for Li-ion batteries with a novel X-ray-diffraction-based method, J. Power Sources, 343, 338 (2017). | 이방성 해석의 근거 (평행 입자 30–60 %) — 방향 분율 ↔ τ₂ 짝짓기 자료가 있는지 | 없음 |
| 47. M. Ender, A. Weber, and E. Ivers-Tiffée, A novel method for measuring the effective conductivity and the contact resistance of porous electrodes for lithium-ion batteries, Electrochem. Commun., 34, 130 (2013). | σ 2203.8 S/m 의 출처 — σ 인지 σ_eff 인지 · 전자 tau2 실험 앵커 (결정 14) | 없음 (`ender2011_…` 는 다른 논문) |
| 51. D. Djian, F. Alloin, S. Martinet, H. Lignier, and J. Y. Sanchez, Lithium-ion batteries with high charge rate capacity: Influence of the porous separator, J. Power Sources., 172, 416 (2007). | 분리막 0.55 / 6.25 의 출처 — landesfeind2016 카드 기록 (23 µm · 0.47 · N_M 13) 과의 어긋남 판별 | 없음 |
| 20. M. Ebner, D. -W. Chung, R. E. García, and V. Wood, Tortuosity Anisotropy in Lithium-Ion Battery Electrodes, Adv. Energy Mater,. 4, 1 (2014). | 판상 흑연 단층촬영 관통 τ ≈ 6 @ 40 % — 같은 계열 재료의 영상 기반 값 | 없음 |
| 22. N. A. Zacharias, D. R. Nevers, C. Skelton, K. Knackstedt, D. E. Stephenson, and D. R. Wheeler, Direct Measurements of Effective Ionic Transport in Porous Li-Ion Electrodes, J. Electrochem. Soc., 160, A306 (2013). | SFG 흑연 7.5 @ 35 % (restricted diffusion) 의 출처 | 없음 |
| 28. H. Lundgren, M. Behm, and G. Lindbergh, Electrochemical Characterization and Temperature Dependency of Mass-Transport Properties of LiPF6 in EC:DEC, J. Electrochem. Soc., 162, A413 (2014). | σ₀ = κ 0.792 S/m 와 P2D 물성의 출처 | 없음 |
| 33. J. P. Meyers, M. Doyle, R. M. Darling, and J. Newman, The Impedance Response of a Porous Electrode Composed of Intercalation Particles, J. Electrochem. Soc., 147, 2930 (2000). | P2D 주파수영역 임피던스 — 그림 2 검증의 모형 계열 | 없음 |
| 40. H. -K. Song, H.-Y. Hwang, K.-H. Lee, and L. H. Dao, The effect of pore size distribution on the frequency dispersion of porous electrodes, Electrochim. Acta., 45, 2241 (2000). | PoSD 를 넣은 de Levie TLM — CPE 대신 물리 분포를 쓰는 선택지 (z 비균질 진단, 결정 13) | 없음 |
| 17. B. Tjaden, S. J. Cooper, D. J. Brett, D. Kramer, and P. R. Shearing, On the origin and application of the Bruggeman correlation for analysing transport phenomena in electrochemical systems, Curr. Opin. Chem. Eng., 12, 44 (2016). | 원문 Bruggeman 비교의 근거 · α 관례 | 없음 (`tjaden2018_…` 는 다른 논문) |
| 16. D. -W. Chung, M. Ebner, D. R. Ely, V. Wood, and R. Edwin, García, Validity of the Bruggeman relation for porous electrodes, Model. Simul. Mater. Sci. Eng., 21, 74009 (2013). | 구형 입자에서 Bruggeman 의 타당성 — 비구형 이탈의 기준선 | 없음 |

- 정본 카드 유무 = `litdb/papers/` 파일 목록 (365 항목) + 낱말 grep 으로 확인 (2026-10-03).

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 — 스크립트는 카드 밖 작업 공간, 값만 기록)
- 본문 6 쪽 전부 렌더로 읽었다 (식 1–13 · 그림 1–6 · Table I · 참고문헌 51).  식 블록 (E3330 · E3331) 과 Table I · 그림 2–6 은 4–7× 확대 렌더로 다시 읽었다.
- 원문 전수 낱말 확인: "MacMullin" 0 · "tortuosity factor" 0 · "solid-state" / "all-solid" 0 · 노드 수 n 의 값 0.
- **Eq 11 ↔ Siroma 표 2 Z형 open–open**: 대수 전개 일치 + 수치 상대차 ≤ 4·10⁻¹⁶ (β = R_e/R_i = 10⁻⁴ · 0.01 · 0.1 · 1 · 10 × ω = 10⁻³ … 10³, α 0.95).
- **Eq 2–10 (사다리) ↔ Eq 11**: O(1/n) 수렴 — n = 101 · 401 · 1601 에서 n·상대차 0.888 일정 (β 0.1 · ω 1).
- **극한**: 고주파 R_e∥R_i · 저주파 실수부 (R_e+R_i)/3 를 β 5 점에서 수치 재현 · 그래프법 계수 (1+β) − 3β/(1+β) 재현 (최소 0.4641 @ β 0.7320) · R_e ↔ R_i 대칭 수치 확인.
- **Landesfeind 2018 Eq 1** (그 카드 전사) 을 sech 로 펼쳐 Eq 11 과 같은 세 항임을 대수로 확인 · **Pouraghajan Eq 5** 의 Z₀ → ∞ 축약식 (그 카드 §8-0 ⑤) 도 대수로 일치.
- Bruggeman 곡선 (그림 6 검은 점선) = ε^−0.5 (판독 4.5 @ 0.05 · 1.6 @ 0.40) · 멱법칙 범례값으로 τ₂(0.40) = 4.86 / 5.30 / 5.75 / 5.41 (카드 산술) — 판독 점과 정합.
- 그림 2 HF 절편 ≈ 0.36 × 10⁻³ (판독) ↔ Table I Z_sep 3.59 × 10⁻⁴ (카드 산술) 일치.  그림 3 · 4 의 시작점은 맞지 않는다 (§10).
- 감도 문장 (0.75) 을 τ₂ ∝ ε₂ (R_ion 고정) 로 재현.
- β 수치 (§8-1 (e)) 는 `minnmann2021_…` §5.0 의 SI Table S2 stated σ 를 그대로 나눈 것 (σ_ion,eff/σ_el,eff) — Minnmann 원문은 이 카드에서 다시 보지 않았다.

## 🔗 이 논문을 인용하는 corpus 카드
- `nguyen2020_electrode_tortuosity_factor` — ref 18 (eSCM 의 한 갈래 · "고상 전자저항 임의값 포함 해석식") — 서술 대조는 §10-2.
- `pouraghajan2018_tortuosity_polarization_interrupt_vs_blocking_electrolyte` — ref 15 ("β 보정의 독립 출처" — §10-2 에서 어긋남 기록).
- 함께 읽을 카드: `siroma2015_…` (위상 이름표 · 같은 함수) · `landesfeind2018_…` (β 오차 지도) · `landesfeind2016_…` (분리막 실측 · TLM-Q) · `kaiser2018_…` (ASSB TLM, z_C = 0) · `minnmann2021_…` (ASSB σ_el,eff · σ_ion,eff → β) · `bazzoun2026_dem_fem_rnm_ionic` (ASSB Z-type TLM 앵커 · R_elec) · `tjaden2018_…` (명명 정본).

## 🗨️ Q&A 로그
- (아직 없음)
