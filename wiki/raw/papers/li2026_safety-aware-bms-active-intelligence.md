---
title: "Li, Li, Wu, Qiao, Jiang 2026 — From state estimation to active intelligence: safety-aware battery management for electric vehicles (Front. Chem. 14, 1960882) [Mini Review]"
source_url: local-upload/08._From_state_estimation_to_active_intelligence_safety-aware_battery_management_for_electric_vehicles.pdf
source_url_note: "본문 12쪽, SI 없음. TYPE: Mini Review — 1차 측정이 0이고 모든 수치가 재인용이다. 이 digest 의 `[인쇄]` 는 '이 리뷰의 지면에 이렇게 적혀 있다' 는 뜻이지 '그 수치가 맞다' 는 뜻이 아니다."
source_doi: 10.3389/fchem.2026.1960882
pdf_sha256_main: a54b551671eea230ef6a4c787b3347f8386667c0370e5f215382f889557534d9
ingested: 2026-09-22
sha256: 3714c77c82f41948c8d1266fedcbeb2d01fce91e80fd90b1914adc5edaaf8d8c
---

# 수집 목적

Feng Li^1(교신), Yuan Li^1, Wenqi Wu^2, Huaying Qiao^1, Lihua Jiang^1
— **"From state estimation to active intelligence: safety-aware battery management for
electric vehicles"**, *Frontiers in Chemistry* **14** (2026) 1960882,
doi `10.3389/fchem.2026.1960882`, **TYPE: Mini Review**, CC BY
(Received 2026-08-07 / Revised 2026-08-29 / Accepted 2026-09-04 / Published 2026-09-15)
의 **절별 해체분석** — 본문 PDF **12 쪽**, SI 없음.

^1 College of Mechanical Engineering, Shandong Huayu University of Technology, Dezhou,
Shandong, China
^2 Office of Scientific Research, 같은 대학
`[인쇄]` 교신 `jxgcxy@huayu.edu.cn` · `[인쇄]` Conflict of interest: 없음 선언.
`[인쇄]` 자금: New Energy Vehicle Intelligent Network Technology Shandong Province Higher
Education Institutions Future Industry Engineering Research Centre Project (No.
PT2025KJS003) · Shandong Province Higher Education Institutions Marine Vessel Special
Motor Key Technology Development and Component Manufacturing University-Enterprise
Collaborative Innovation Center (PT2025KJS005).

**이 위키 `assb` 섹션의 8호 자료이고, 앞 7 편과 성격이 다르다.**
1–7 호는 전부 ASSB 의 **미세구조·계면·전극** 논문(시뮬레이션 3 + 실험 4)이었다.
8 호는 **BMS·진단 종설**이고, **ASSB 는 12 쪽 중 한 문단(§6.1)에만 나온다.**

> ⚠⚠ **이것은 Mini Review 다. 1 차 측정이 하나도 없다.**
> 이 digest 에 나오는 모든 수치는 **재인용**이며, 우리 위키에서 근거로 쓰려면
> **원 논문을 따로 받아야 한다.** 그 후보 목록이 이 digest 의 §15 이고,
> **이 편을 읽은 실익의 대부분이 거기 있다.**
> 아래에서 `[인쇄]` 는 "이 리뷰의 지면에 이렇게 적혀 있다" 는 뜻이지
> "그 수치가 맞다" 는 뜻이 **아니다.**

**표기 규칙** (이 위키 관례 3구분 + 1):
- `[인쇄]` — 이 리뷰 본문/표에 글자로 있는 것
- `[도표]` — 그림에서 눈으로 읽은 것 (figure-read; 원 데이터가 아니다)
- `[해석]` — 이 digest 를 쓰면서 붙인 판단. **논문의 주장이 아니다**
- `[재현]` — 이 digest 가 논문의 값들로 직접 계산한 것 (계산 과정을 같이 적는다)

- 원본 파일: 로컬 업로드 PDF (저장소에 바이너리를 넣지 않는다)
  `sha256 = a54b551671eea230ef6a4c787b3347f8386667c0370e5f215382f889557534d9`
- 크로핑 그림: `raw/figures/li2026_safety-aware-bms-active-intelligence/`
  (fig 2 장 + tab 4 장, `figures.json` 에 캡션 색인)

---

# 0. 이 digest 를 쓰기 전에 실제로 본 것

| 무엇 | 어떻게 | 봤나 |
|---|---|---|
| 본문 12 쪽 전문 | `pymupdf` `get_text()` | ✅ 전수 |
| **Figure 1** (p.2, 통합 프레임워크) | `fig_1.png` 를 **Read 로 열람** | ✅ |
| **Figure 2** (p.7, 저온 급속충전 결정 흐름) | `fig_2.png` 를 **Read 로 열람** | ✅ |
| **Table 3** (p.7) | fig_2 크롭에 **같이 들어와 있어 이미지로도 봤다** + PDF 텍스트 | ✅ 이중 확인 |
| Table 1 · 2 · 4 | PDF 텍스트 (도구 권고: 표는 텍스트가 정확) | ✅ |

**크로핑 장수 대조 (06번에서 물린 항목)**: 크로퍼가 **6 장**(fig 2 + tab 4)을 뽑았고,
`pymupdf` 로 센 PDF **내장 이미지 개수는 2 개**(p.2 · p.7)다. 논문의 Figure 는
본문 인용 기준으로도 **Figure 1·2 둘뿐**이고 Table 은 1–4 넷이다.
→ **빠진 그림 0 장. 이번에는 크로퍼 사고가 없다.**

**단위 µ 탈락 검사 (07번에서 물린 항목)**: 이 PDF 의 텍스트층에는 `µ` 가 필요한
수치가 **하나도 없다.** 단위가 붙은 값은 `1 MPa`(1 회) · `−20 °C to 60 °C` ·
`0 °C–45 °C` · `70 °C` · `50 °C` · `6 A` · `3.5 Ah` · `20 min` · `5 min` · `1 min`
뿐이고, 그중 `−20 °C to 60 °C` 와 `>120 titration points` 는 **fig_2 크롭(Table 3)
에서 눈으로 다시 확인**했다. → **추출 불확실 항목 없음.**

**안 본 것**: 없다. 다만 **인용된 48 편의 원 논문은 이 digest 의 근거가 아니다** —
예외는 우리 위키가 이미 원전 digest 를 갖고 있는 **Su et al. 2024** 와
**Birkl et al. 2017** 둘뿐이고, 그 둘은 §7·§13 에서 대조에 썼다.

---

# 0.5 원문에 없어서 확인이 필요한 것 (공백 원장)

| # | 무엇이 없나 | 왜 걸리나 |
|---|---|---|
| **G1** | ★★★ **`I_uncertainty` 를 어떻게 계산하는지** — Figure 2 의 여섯 전류 상한 중 하나인데 정의·식·근거가 **본문에도 그림에도 없다** | 우리 폭 측정기가 정확히 그 자리에 들어간다 (§16) |
| **G2** | **재인용 수치의 원 논문** — Table 2 8 행 중 우리가 원전을 가진 것은 0 행, §3.1 의 DRT 두 편 중 1 편(Su 2024)만 | 이 리뷰의 숫자를 그대로 옮기면 안 된다 (§13 D1 이 그 실례) |
| **G3** | **`<1 MPa` 산업 요구치의 근거** — Xu et al. 2024 를 가리킬 뿐, 그 값이 어떤 셀·어떤 제조사·어떤 조건인지 없다 | 우리 압력 창 페이지의 아래 벽에 직결 (§14 Q6) |
| **G4** | **`Computational burden` 열의 척도** — 논문이 `[인쇄]` "relative deployment burden" 이라 적지만 **무엇 대비 relative 인지** 없다 | 비교표의 한 열이 비교 불가다 (§13 D9) |
| **G5** | **Table 4 TRL 의 근거** — 논문 스스로 `[인쇄]` "TRL ranges are **proposed targets** rather than ratings of the cited literature" | 로드맵을 근거로 쓸 수 없다 |
| **G6** | **선별 기준의 분모** — `[인쇄]` "representative studies are used as evidence rather than as an exhaustive bibliography" 라고만. **몇 편을 보고 몇 편을 걸렀는지 없다** | 이 리뷰 스스로 `[인쇄]` "Selective reporting" 을 실패 모드로 꼽는다 (Table 4) |
| **G7** | **`Liu et al. (2025)` 가 두 편인데 a/b 가 없다** | §13 D7 |
| **G8** | **ASSB 파트의 1 차 근거** — §6.1 의 ASSB 한 문단이 매단 인용 3 편이 **전부 종설**(Xu 2024 · Zhang 2025 · Biçer 2025) | 우리 축에 닿는 유일한 문단인데 **종설이 종설을 인용한다** |

---

# 1. 초록과 성격 — 논문이 스스로 말하는 것

`[인쇄]` 초록 전문의 논지 다섯:

1. "Battery management systems (BMSs) are increasingly required to **convert incomplete
   electrical and thermal measurements into safe control actions rather than merely
   report battery states**."
2. 두 개의 배치(deployment) 질문 — "how electrochemical states can be made **observable**
   with affordable diagnostics, and how charging, thermal, balancing, and health
   objectives **can be arbitrated when their constraints conflict**."
3. "we … show why **cross-dataset accuracy alone is insufficient evidence of
   deployability**."
4. "A **layered vehicle–edge–cloud architecture** is proposed in which a **deterministic
   safety supervisor enforces voltage, temperature, lithium-plating, power, imbalance,
   and uncertainty limits before performance optimization**."
5. "The same framework is then examined for **solid-state, lithium–sulfur, and
   sodium-ion batteries**, where **pressure, observability, and chemistry-specific
   calibration** introduce new constraints."

`[인쇄]` 키워드: battery management system, digital twin, electric vehicle, fast
charging, state estimation, state of health, thermal management.
→ `[해석]` **키워드에 `identifiability`·`degradation mode`·`solid-state` 가 없다.**

## 1.1 이 리뷰가 어떻게 만들어졌는지에 대한 신호 셋

이것을 앞에 적는 이유: **이 digest 의 모든 수치가 재인용**이므로, 인용 공정의
품질이 곧 자료의 품질이다.

- `[인쇄]` **Generative AI statement**: "generative AI was used in the creation of this
  manuscript. Generative AI was used to **assist in the preparation of Figure 1**. The
  authors designed the scientific content, reviewed the output, and revised the final
  figure." → **Figure 1 은 AI 가 그린 도식이다** (저자 검토 선언 있음).
- `[인쇄]` §1: "**The uploaded** 2023 review usefully organized this broad field around
  battery models, SOC and SOH estimation, charging, cell balancing, and thermal
  management (Ranjith Kumar et al., 2023)." → "the **uploaded** review" 라는 표현이
  게재본에 남아 있다.
- `[인쇄]` 심사 응답 문장 둘이 본문에 남아 있다: §2 "Table 2 addresses **the reviewers'
  request** for quantitative comparison." · §4 "This resolves **the reviewer's example**
  directly." (→ §13 D5)

`[해석]` 셋을 합치면 **원고와 심사 응답서가 섞인 채로 게재됐다.**
접수(08-07) → 게재(09-15) 가 **39 일**이다.

---

# 2. §1 서론 — 리뷰가 세운 두 질문

`[인쇄]` "The pressing question is no longer whether model-based or data-driven methods
are preferable in isolation, but **how they can be combined without sacrificing
real-time feasibility, physical credibility, or safety**."

**질문 1 — 차 안에서 실제로 관측 가능한 정보는 무엇인가.**
`[인쇄]` "Voltage-only estimators can be accurate on familiar cells but may become
**poorly identifiable** when temperature, aging mechanism, or chemistry changes
(Liu et al., 2026)."
→ ★ **이 리뷰에서 우리 Q4 에 가장 가까운 문장이다.** ⚠ 그런데 그 문장이 매단 인용이
**주제가 다른 논문**이다 (§13 D2).

**질문 2 — 목적이 충돌할 때 누가 권한을 갖는가.**
`[인쇄]` "A request for maximum charging power at low temperature … should not compete
**symmetrically** with lithium-plating or voltage constraints. Safety-critical
coordination requires an **explicit hierarchy in which hard constraints veto the
performance optimizer**."

`[인쇄]` 층 구조(초록의 vehicle–edge–cloud 를 본문이 푼 것):
- **차량층** — 밀리초~서브초, **결정론적 보호를 유지**
- **에지층** — 초~분, 파라미터·불확실성·진단 갱신
- **클라우드/플릿층** — 느린 모집단 학습, 모형 검증, 버전 관리된 갱신
- `[인쇄]` 위로 가는 정보 = telemetry, health features, residuals, uncertainty /
  아래로 가는 정보는 **validated priors, limits, policy updates 로 제한**
- `[인쇄]` "**Hard safety constraints remain local even when connectivity is lost.**"

`[인쇄]` 선별 기준(evidence hierarchy): "We prioritize work that contributes at least one
deployment-relevant element: mechanistic electrochemical information, **a quantitative
metric reported with a defined dataset**, validation across temperatures/chemistries/
domains, module/pack/field evidence, or **an explicit statement of computational and
sensing limitations**." (⚠ 분모 없음 — G6)

---

# 3. Figure 1 — 통합 프레임워크 (`[도표]`, 실제로 열람)

`[인쇄]` 캡션: "Integrated framework for safety-aware battery management in electric
vehicles. Battery representation, state intelligence, fast-charging control, thermal
safety and fault diagnosis, cell balancing and pack coordination, and digital twins with
active sensing are coupled through the BMS core. Robust validation, uncertainty
quantification, multiscale integration, and standardized benchmarks are identified as
key priorities."

## 3.1 `[도표]` 그림에 실제로 있는 것

가운데 **"BMS Core"** 원(배터리 팩 아이소메트릭 일러스트) 둘레에 상자 여섯,
아래에 "Future priorities" 띠 하나.

| # | 상자 | 항목 (`[도표]` 그대로) |
|---|---|---|
| 1 | Battery representation | Electrochemical models `∂c_s/∂t = D_s ∇²c_s` · Equivalent-circuit models `V = OCV − IR₀ − Σᵢ Vᵢ` · Data-driven models (산점 + S 자 곡선) · Hybrid models (`RC + ML`) |
| 2 | State intelligence | SOC · SOH · SOP · RUL · **Uncertainty-aware estimation** · **Domain adaptation** |
| 3 | Fast charging control | CC–CV · Health-constrained charging · **Lithium plating risk** · Charging-time optimization |
| 4 | Thermal safety & fault diagnosis | Heat generation · Temperature uniformity · Thermal runaway warning · Fault detection |
| 5 | Cell balancing & pack coordination | Passive balancing · Active balancing · Consistency · Pack-level control |
| 6 | Digital twins & active sensing | Cloud-edge collaboration · Fleet learning · **Active pulse diagnostics** · Closed-loop update |

`[도표]` 아래 띠: **Future priorities → Robust validation → Uncertainty quantification
→ Multi-scale integration → Standardized benchmarks → Safer, longer-life EV batteries.**

## 3.2 `[해석]` 그림에 **없는** 것 — 그리고 본문이 있다고 말하는 것

- **`safety supervisor` 상자가 없다.** 그런데 `[인쇄]` §6.2 는 "The deterministic safety
  supervisor **in Figure 1** provides a stable boundary around adaptive functions" 라고
  적는다. 그 상자는 **Figure 2** 에 있다. (→ D4)
- **층(layer)이 없다.** 초록이 `[인쇄]` "A **layered** vehicle–edge–cloud architecture is
  proposed" 라고 하지만 `[도표]` 여섯 상자와 BMS Core 는 **전부 양방향 대칭 화살표**로
  이어져 있다. `[해석]` 이것은 본문이 `[인쇄]` "should not compete **symmetrically**"
  라고 반대한 바로 그 그림이다. (→ D4)
- **압력·고체전해질 요소가 없다.** §6.1 이 `[인쇄]` "stack pressure becomes a **coupled
  state/control variable**" 이라고 주장하는데 프레임워크 그림에 그 축이 없다.
- **수치가 하나도 없다.** 데이터 그림이 아니라 개념도다.

---

# 4. Table 1 — 여섯 기능층과 그 한계 (`[인쇄]`, 전수)

`[인쇄]` 캡션: "Functional layers of a safety-aware BMS, with explicit information
exchange, evidence, and deployment limitations."

| 층 | 입출력 | 방법 | 결정 역할 | **남은 한계 (`[인쇄]` 그대로)** |
|---|---|---|---|---|
| Battery representation | V, I, T, 이력 → 내부 상태/한계 | DFN/축소 전기화학 · ECM · hybrid physics–ML | 전압/발열 예측 + 안전 관련 잠재변수 | "DFN preserves electrochemical causality but is **parameter-intensive**; ECMs are embedded-friendly but **can lose physical uniqueness**; model validity shifts with T and aging" (Chen 2020; Doyle 1993; Hu 2012; Sulzer 2021) |
| State and health intelligence | 측정 + 파라미터 → SOC, SOH, SOP, RUL, **uncertainty** | 적응 관측기 · 베이즈 필터 · GPR/NN · 전이학습 | 희소 신호 → 운용 상태 + **신뢰도** | "**Field labels are limited and domain shift is a dominant failure mode**; partial-charge and transfer-learning methods improve practicality but require **out-of-domain detection**" (Deng 2022; Lu 2023; Thelen 2024) |
| Electrochemical diagnostics | 소섭동/임피던스/이완 → 동역학·계면 feature | EIS · DRT · GITT · active pulse | 저항 성장·반응/수송 시간척도·모형 파라미터의 **관측성** 개선 | "EIS/DRT can provide low-error SOH features, but hardware, excitation design, **identifiability**, and measurement time constrain on-board use; GITT is mainly calibration/service oriented" (Khan 2024; LeBel 2022; Su 2024; Zhang 2026) |
| Fast-charging control | 상태 + 제약 + 요구 → 전류/열 명령 | CC–CV · MPC · 적응/ML | "Optimizes charging **only inside an admissible safety set**" | "Fixed protocols are robust but non-adaptive; aggressive optimization is **unsafe if plating, temperature, cell spread, or uncertainty is poorly estimated**" (Attia 2020; Sun 2024) |
| Thermal safety and fault diagnosis | T, dT/dt, 전기 잔차, (가능하면) 가스/압력 → 위험 확률 | 전기-열 모형 · 다중모드 잔차 · 예측 냉각 | 최고 온도·비균일 제한, 조기 경보 | "Surface sensing can **miss internal hot spots**; warning must **combine weak signals** rather than wait for a single threshold" (Bandhauer 2011; Finegan 2015; Gharehghani 2024; Heenan 2023) |
| Balancing and pack coordination | 셀 상태 + 산포 → 재분배·팩 한계 | 수동/능동 밸런싱 · 팩 관리 | "Prevents **weakest-cell constraints from being hidden by pack averages**" | "**Voltage equality is not always the correct target** when capacity/resistance differ" (인용 없음) |
| Digital twins and active sensing | 이력 + 모형 버전 + 플릿 사전 ↔ 검증된 갱신 | 클라우드–에지 · 디지털 트윈 · 표적 펄스 | 종단 추적 + 정보 획득 진단 | "Cybersecurity, data ownership, version control, and safe fallback are prerequisites; **learning updates cannot bypass the certified local safety envelope**" (Dubarry 2023; Liang 2026; Wu 2020) |

★ **우리 축에 걸리는 두 칸**:
- `[인쇄]` "ECMs … **can lose physical uniqueness**" — `uniqueness` 는 12 쪽 전체에서
  **이 한 번**이다. 그리고 그 근거로 매단 4 편은 **전부 모형/매개화 논문**이며
  **유일성을 잰 편이 하나도 없다** (§14 Q4).
- `[인쇄]` "**Field labels are limited**" — 라벨 층위를 **표의 칸으로** 인정한다.

---

# 5. §2 배터리 표현 — 그리고 PyBaMM

`[인쇄]` DFN: "resolves lithium transport and reaction processes through coupled partial
differential equations and remains the physical reference for many reduced models
(Doyle et al., 1993). Such models can expose internal concentration gradients and
overpotentials that are **directly related to power limitation and lithium-plating
risk**."

★★ `[인쇄]` **그 다음 문장이 이 리뷰에서 우리에게 가장 값나가는 한 줄이다**:

> "Their disadvantage is not simply computational cost. **Parameter identifiability,
> cell-to-cell variability, and uncertain aging mechanisms can make a detailed model
> appear more precise than the available measurements justify.**"

`[해석]` **이것이 `degradation-degeneracy` 의 논지다** — 문헌에서 인용 가능한 형태로
적혀 있다. ⚠ **단 이 문장에 데이터가 붙어 있지 않다.** 바로 뒤 문장이
`[인쇄]` "Parameterization studies and open modeling platforms such as **PyBaMM** have
improved reproducibility, but they also highlight **how strongly predictions depend on
experimental design and parameter quality**" (Chen 2020; Sulzer 2021) 인데, 이 두 편은
**파라미터화 방법론과 소프트웨어 논문**이지 식별 가능성 측정 논문이 아니다.
→ `[해석]` **주장은 우리 쪽, 근거는 0.**

`[인쇄]` ECM: "model order should be chosen for the **duty cycle** rather than by
complexity alone (Hu et al., 2012)." · "The important deployment issue is **parameter
drift**: an ECM calibrated at one temperature and age can **fit voltage well while
misrepresenting the internal electrochemical margin**."
→ `[해석]` **"잘 맞는데 내부가 틀렸다" 를 리뷰가 배치 문제로 명명한다.** 우리 위키의
[[halfcell-ocp-shape-invariance]] 가 액체셀에서 잰 것(곡선만 바꿔도 OCV RMSE 는 9.9 →
8.2 mV 로 좋아지는데 `LAM_an` 은 2.4 %p 움직인다)과 **같은 형태의 주장**이다. ⚠ 이
리뷰는 그 크기를 재지 않는다.

`[인쇄]` GITT: "reported **pulse durations of roughly 10 s to 30 min** and **rest periods
of about 8 min to 4 h** make full characterization unsuitable for continuous on-board
operation (LeBel et al., 2022). Thus, **high-resolution GITT is best treated as offline
or service-level calibration**."

`[인쇄]` 데이터 주도: "their strongest reported accuracy is often obtained under
**carefully defined datasets** (Severson et al., 2019). This distinction matters because
**a BMS model is not a leaderboard entry**: it must **declare its validity domain** and
provide a safe action when the input leaves that domain."

`[인쇄]` PIML: "Physics-informed approaches are most useful when the roles are
explicit—**conservation laws and feasible states are imposed by physics, while learning
estimates uncertain parameters or residual effects**" (Wang et al., 2024).
→ `[해석]` 우리 [[piml-physics-injection-points]] 의 여섯 자리 중 ①(손실항)·③(구조)만
언급하고 **⑥(라벨 그 자체가 물리 모형의 적합값)은 말하지 않는다.**

`[인쇄]` 권고 위계: "high-fidelity electrochemistry **offline** for safety maps and
**synthetic experiments**; reduced electrochemical/ECM models **on-board**; and learned
residuals or parameter adapters for systematic mismatch."
→ `[해석]` **"합성 실험" 이 오프라인 고충실도 모형의 정당한 용도로 명시돼 있다** —
우리 PyBaMM 합성 truth 접근이 리뷰의 권고 위계 안에 들어간다.

`[인쇄]` 비교 규율: "**accuracy, acquisition latency, inference burden, validity-domain
coverage, uncertainty output, and validation level** as **co-equal** performance
dimensions rather than ranking methods by a single error metric." · "an RMSE below 1% on
a cell-level laboratory dataset **does not imply pack-level accuracy** under sensor drift
or a new chemistry."

---

# 6. §3 + Table 2 — 상태 지능, 그리고 **라벨·불확실성 원장**

## 6.1 `[인쇄]` SOC 의 구조적 문제

"Coulomb counting accumulates sensor bias, open-circuit-voltage methods require
sufficient rest, and model-based observers inherit errors in capacity, resistance, and
temperature dependence." · "**capacity should not remain fixed while SOC is estimated**.
As the battery ages, an unchanged coulomb-counting denominator produces a **systematic
SOC bias, particularly near the upper and lower operating limits**."

## 6.2 Table 2 전수 (`[인쇄]`) — 이 리뷰의 유일한 정량 자산

`[인쇄]` 캡션: "Representative quantitative benchmarks … Reported metrics come from the
cited studies and **should not be compared without considering dataset, target, and
validation conditions**."

| 연구 | 방법/대상 | **보고된 정확도** | 계산 부담* | 입력 | 학습/화학 경계 | 검증 수준 | **Uncertainty output** | 실시간성 |
|---|---|---|---|---|---|---|---|---|
| Roman 2021 | SOH ML 파이프라인 | **RMSE 0.45 %** (best fast-charge deployment) | Low–medium online | V/I 충전 구간 | **179 Li-ion cells** | Cell | ★ **Confidence interval reported** | 가능 |
| Deng 2022 | 무작위 부분충전 sparse GPR | **평균 최대절대오차 2.88 / 2.52 / 1.51 %** (3 셀종) | Medium | V/I 부분충전 | 3 종 · 다중 T/전류 | Cell | "Predictive variance possible; **safety calibration not demonstrated**" | feature 창 있으면 |
| Zhu 2022 | 전압이완 ML + 전이 | **RMSE 1.1 %** (source) · **<1.7 %** (transfer) | Low–medium | 운전 후 전압이완 | **130 cells**; NCA·NMC·blend | Cell | **Not primary output** | 간헐 (이완 필요) |
| Ma 2022 | 심층 전이학습 | **평균 오차 0.176 %** 용량 · **8.72 %** RUL · 교차 데이터셋 **0.193–0.328 %** | Medium–high 학습 | 사이클 센서 | **77 cells; >140,000 cycles** | Cell | **Not primary output** | 개념적 시연 |
| Lu 2023 | 도메인 적응 심층 SOH | **MAE ≤1.43 %**; **89.4 % 표본이 절대오차 <3 %** (대상 열화 라벨 없이) | Medium | 충전/사이클 신호 | **65 cells; 71,588 samples**; 복수 제조사 | Cell | **No calibrated uncertainty reported** | 가능 |
| Wang 2024 | PINN | **MAPE 0.87 %** | Medium–high 학습 | V/I/T + 물리 제약 | **387 batteries; 310,705 samples** | Cell | **No calibrated uncertainty reported** | 차량 검증 안 됨 |
| Khan 2024 | EIS→DRT→LSTM SOH | **평균 RMSPE 1.69 %** (10 개 테스트셋) | **Higher acquisition burden** | EIS 스펙트럼 | **5 calendar-aged + 17 cycling-aged** | Cell | **No calibrated uncertainty reported** | 주기적 진단, 연속 불가 |
| Liu 2025 | NODE–CNN, **나트륨이온** SOC/SOH | **R² = 0.998 (SOC) · 0.997 (SOH)** | Medium–high 학습 | 부분충전 + 온도 | **53 Na-ion cells, 2 packs, 0–45 °C** | ★ **Cell + pack** | **No calibrated uncertainty reported** | "pack validation still limited" |

\* `[인쇄]` "Computational cost is … expressed as a **relative deployment burden** when the
original paper does not report standardized microcontroller timing" (⚠ 기준 없음 — G4).

## 6.3 ★★★ 이 표에서 우리가 직접 셀 수 있는 것 (`[재현]`)

**Uncertainty output 열을 세면**:

| 층위 | 편수 |
|---|---:|
| **보정된(calibrated) 불확실성을 보고** | **0 / 8** |
| 신뢰구간 보고 (보정 여부 불명) | 1 / 8 (Roman 2021) |
| "가능하지만 안전 보정은 시연 안 됨" | 1 / 8 (Deng 2022) |
| "주 산출이 아님" | 2 / 8 (Zhu 2022, Ma 2022) |
| "보정된 불확실성 보고 없음" | 4 / 8 (Lu, Wang, Khan, Liu) |

**Validation level 열을 세면**: **7 / 8 이 `Cell`**, 1 편만 `Cell + pack`(그것도
"pack validation still limited").

`[해석]` ★★ **이것이 이 리뷰가 우리에게 준 가장 단단한 것이다** — 액체셀 17 편에서
"유일성을 잰 편 0" 이었고 `assb` 7 편에서 "오차막대 0" 이었던 원장에,
**BMS/SOH 추정 쪽 대표 8 편에서 "보정된 불확실성 0"** 이 붙는다.
세 계보가 **같은 방향**으로 비어 있다.
⚠ **단 이것은 리뷰의 분류를 우리가 센 것**이고, 8 편은 리뷰가 고른 표본이다 (G6).

## 6.4 `[인쇄]` 현장 데이터 — 가용성과 정보량은 다르다

"Real vehicles provide large volumes of voltage/current records but often contain
**narrow SOC windows, uncertain calibration, firmware changes, missing rest periods, and
no direct capacity labels**."

★ `[인쇄]` **생산용 추정기가 내야 할 세 가지**: "an **estimate**, **calibrated
uncertainty**, and a **validity flag linked to domain coverage**."

`[인쇄]` 검증 처방: "Validation should **deliberately inject** current/voltage bias,
missing sensors, ambient-temperature shifts, replacement modules, and abnormal but
non-fault conditions **rather than relying only on random train–test partitions**"
(Thelen et al., 2024).
→ `[해석]` 우리 [[fused-lasso-feature-design-framework]] 가 Rhyu 2025 에서 본
**프로토콜 group CV** 와 같은 축의 요구이고, 여기서는 **결함 주입**까지 간다.

---

# 7. §3.1 + Table 3 — 전기화학 진단 네 채널

## 7.1 `[인쇄]` 네 채널의 역할 분담 (Table 3, 이미지로도 확인)

| 방법 | 전기화학 정보 | 대표 증거 | 획득/해석 부담 | 권고 BMS 역할 |
|---|---|---|---|---|
| **EIS** | 주파수 의존 임피던스; ohmic · charge-transfer · diffusion · 열/노화 서명 | 소형화 온보드 임피던스 하드웨어 (Wen 2025; Zhang 2026) | "Full spectra require perturbation design and are **vulnerable to DC bias, ripple, wiring and converter noise**" | 주기적 온보드/서비스 진단; **sparse-frequency 구현이 가장 실용적** |
| **DRT (EIS 에 적용)** | "Characteristic time-scale distribution **without fixing a single ECM topology**" | "**SOH RMSE ≤0.873 % in Su et al. (2024)**; average RMSPE 1.69 % in Khan et al. (2024)" | ★ "**Ill-posed inversion needs regularization**; peak interpretation and uncertainty **can change with temperature/chemistry**" | EIS 로부터 feature 추출 + 기구 인식 건강 지표 |
| **GITT/펄스 매개화** | OCV + 동적 응답 vs SOC/T; 확산/동역학 파라미터 | "LeBel et al. (2022) used **>120 titration points over −20 °C to 60 °C**" | "Typical pulse/rest protocols are long (seconds–minutes pulses; minutes–hours rest)" | 오프라인 특성화·교정·서비스 진단 |
| **Active bounded pulses** | 의도적으로 고른 여기 아래의 짧은 동적 응답 | "Active BMS uses **information-seeking pulses to improve observability**" (Liang 2026) | "Pulse must be safe, imperceptible, and **identifiable from inverter/charger disturbances**" | **높은 불확실성 또는 약한 관측성에 의해 촉발되는** 온보드 표적 진단 |

## 7.2 ★★★ 이 표의 DRT 칸이 원전을 넘어선다 (→ D1)

리뷰 `[인쇄]` §3.1 본문: "Su et al. (2024) developed DRT-based features and reported
**SOH RMSE within 0.873 %**."
리뷰 `[인쇄]` Table 3: "**SOH RMSE ≤0.873 %** in Su et al. (2024)."

**우리 위키가 이 원전의 digest 를 이미 갖고 있다** —
`raw/papers/su2024_drt-soh-health-features.md` (2026-09-03 흡수). 거기에 적힌 것:

| 원전이 실제로 말하는 것 | 근거 (우리 digest 좌표) |
|---|---|
| 0.873 % 는 **5 셀 평균**이고 **cell5 는 1.607 %** | 원전 Table 4, 셀별 값 0.727 / 0.512 / 0.655 / **1.607** / 0.865 |
| **제안 feature 가 자기 대조군에 진다** — 원시 EIS 120-D(Feature2) **0.573 %**, 8-D(Feature3) **0.672 %** 가 제안 feature(Feature1, 0.873 %)보다 **모든 지표에서 우세** | 원전 Table 3 (R² 99.362 vs 98.446, MaxAE 0.0135 vs 0.0222) |
| **보간 성능**이다 (새 셀 일반화가 아니다) | 원전 §5, 저자 스스로 인정 |
| 원전 결론절이 `[인쇄]` "0.873 %, which is only slightly **lower** than Feature3's RMSE of 0.672 %" 라고 **부등호를 뒤집어** 적는다 | 원전 p.12 |

`[해석]` ★★★ **리뷰는 원전의 과장(`within`)을 받아 `≤` 라는 부등호로 한 단계 더
굳힌다.** 0.873 % 는 **상한이 아니고**(cell5 = 1.607 %), **그 논문의 최고 성적도
아니다**(0.573 %). 그리고 리뷰는 "제안 방법이 자기 대조군에 졌다" 는 사실을
전달하지 않는다 — 전달했다면 이 표의 결론("DRT feature 가 정량적으로 경쟁력 있다")이
**원시 스펙트럼을 그냥 쓰는 쪽**을 가리켰어야 한다.

→ ★ **이것이 우리 위키가 `[인쇄]` 를 `[재인용]` 과 구분해야 하는 이유의 실측 사례다.**
같은 일이 Table 2 의 나머지 7 행에서도 일어나고 있는지는 **우리가 모른다** (G2).

## 7.3 `[인쇄]` 설계 질문 — 식별 가능성을 실험 설계로 다시 쓴 것

"The central electrochemical design question is thus **not which diagnostic is
universally best, but what minimum excitation can resolve the safety-relevant process of
interest** within the available time, power-electronics noise, and aging budget."

`[해석]` **이것은 우리 [[near-optimal-set-width-measurement]] 의 역문제다.**
우리는 "주어진 관측으로 답이 하나로 정해지는가(폭)" 를 재고,
이 문장은 "원하는 폭을 얻으려면 최소 어떤 여기가 필요한가" 를 묻는다.
**같은 기계의 양 끝**이고, 리뷰는 그 기계를 갖고 있지 않다.

## 7.4 ⚠ Birkl 2017 이 붙은 자리

`[인쇄]` §3.1 마지막 문장: "As summarized in **Table 3**, electrochemical diagnostic
methods provide complementary information on battery health, internal kinetics, and
degradation, supporting accurate state estimation and safety-aware decision-making in a
deployable BMS **(Birkl et al., 2017)**."

`[해석]` Table 3 은 **EIS · DRT · GITT · active pulse** 넷의 표다. Birkl et al. 2017
(*JPS* 341, 373–386)은 **OCV/DV 기반 열화 모드(LLI · LAM_PE · LAM_NE) 진단** 논문이고
(우리 원전 digest: `raw/papers/birkl2017_degradation-diagnostics-ocv.md`),
그 넷 중 어느 것도 다루지 않는다. → **인용이 내용과 연결되지 않는다** (D8).

★★ 그리고 더 중요한 것: **이 리뷰는 열화 모드라는 개념을 한 번도 쓰지 않는다.**
`[재현]` 12 쪽 전수 검색 — `LLI` **0 회** · `LAM` **0 회** · `degradation mode` **0 회** ·
`incremental capacity` **0 회** · `differential voltage` **0 회** · `half-cell` **0 회**.
→ `[해석]` **이 리뷰의 SOH 는 끝까지 스칼라(용량 또는 %)다.** 우리 축(모드 분해)이
이 리뷰에 **아예 없다**, 열화 모드 진단의 원전을 인용해 놓고도.

---

# 8. §4 + Figure 2 — 급속충전을 제약 중재로 다시 쓴다

## 8.1 `[인쇄]` 본문의 위계

"A practical arbitration rule is to compute **independent admissible current limits for
terminal voltage, temperature, plating risk, pack power, cell imbalance, and
uncertainty**. The performance optimizer—whether MPC, dynamic programming, or a learned
policy—**operates only inside this feasible set**. This creates a **lexicographic
priority**:

> (1) hard safety and isolation, (2) lithium-plating and cell-voltage margin,
> (3) thermal envelope, (4) degradation and balancing objectives, and only then
> (5) charging-time demand."

`[인쇄]` "If sensor validity or uncertainty fails a threshold, the supervisor **derates
current or returns to a validated conservative profile** rather than extrapolating the
optimizer."

## 8.2 Figure 2 (`[도표]`, 실제로 열람) — 흐름도에 실제로 있는 것

`[도표]` 제목: "Example decision flow: low-temperature fast charging"

```
Plug-in / fast-charge request
        ↓
Update state vector: SOC, SOH, cell temperatures,
cell spread, model uncertainty, recent history
        ↓ (셋으로 갈라짐)
 [Thermal gate]        [Electrochemical gate]      [Pack gate]
 Tcell < preheat?      plating / voltage margin    imbalance / power limit
        ↓ yes                    ↓                      ↓
 Preheat + current                                      │
 derating until      ──then──>  Compute admissible current limits
 thermal margin                 IV, IT, Iplate, Ipower, Iimbalance, Iuncertainty
 is restored                             ↓
                        Safety supervisor sets
                        Icmd = min(IV, IT, Iplate, Ipower, Iimbalance, Iuncertainty)
                         ↓ invalid / high uncertainty        ↓
        If uncertainty / sensor validity fails:     Optimize within safe set:
        conservative fallback profile               charge time + aging + thermal uniformity
                                                             ↓
                                            Apply current / cooling / balancing
                                            and monitor residuals
                                                  └─ repeat every control interval ─┘
```

`[도표]` 하단 이탤릭: "*Priority is **lexicographic**: hard safety constraints veto the
optimizer; performance is optimized only inside the feasible safe set.*"

## 8.3 ★★ `[해석]` 그림이 계산하는 것은 lexicographic 이 아니다 (→ D3)

`min(I_V, I_T, I_plate, I_power, I_imbalance, I_uncertainty)` 는 **인수의 순서에
불변**이다. 여섯 제약의 우선순위를 어떻게 뒤섞어도 **같은 `I_cmd` 가 나온다.**
즉 그림은 **연언(conjunction, 가장 빡빡한 제약이 이긴다)** 을 구현했고,
사전식(lexicographic) 순서는 **구현돼 있지 않다.**

`[해석]` 사전식 순서가 실제로 다른 답을 내는 경우는 **제약들이 동시에 만족 불가능할
때**다(그때 어느 것을 먼저 포기하는가). 그 경우가 흐름도에 없다 —
유일한 비상구는 `[도표]` "invalid / high uncertainty → conservative fallback" 하나이고,
그것은 순서가 아니라 **이분 분기**다.
→ **이 논문의 중심 구조 주장(초록 4번 · §1 질문 2 · §4 · §6.2)이 자기 그림에서
구현되지 않는다.**

## 8.4 ★★★ `I_uncertainty` — 이 리뷰가 낸 빈칸 (G1)

`[도표]` 그림이 **여섯 번째 전류 상한을 "불확실성" 에서 뽑는다.**
그런데 **계산법이 본문에도 그림에도 없다.** `[인쇄]` 본문은 "compute independent
admissible current limits for … **and uncertainty**" 라고만 적는다.

`[해석]` ★★★ **이것이 이 논문이 우리 프로젝트에 낸 가장 직접적인 접점이다** —
§16 에서 다시.

## 8.5 `[인쇄]` 클라우드는 안전 루프 밖

"Li et al. (2025) trained a model on **909,135 real-world direct-current charging
sessions** and reported **90 % charging-duration accuracy from one observation** and
**95 % accuracy with absolute error below 1 min using six observations within 5 min**.
… They **should not directly override** cell-level voltage, temperature, plating, or
uncertainty limits because **prediction of user-visible charging duration is a different
task from certifiable safety control**."

---

# 9. §5 — 열·고장·밸런싱

`[인쇄]` Heenan et al. 2023 재인용: "a **20 min high-rate discharge of an
energy-optimized 3.5 Ah cell** produced internal temperatures **above 70 °C**, whereas a
**power-optimized design** under a shorter high-rate condition remained **below about
50 °C**; **even under the same 6 A current**, internal thermal responses differed
substantially." · "pack-average surface temperature can **hide chemistry- and
design-dependent internal hot spots**."

`[인쇄]` 경보 설계: "A practical warning layer should **fuse weak evidence**—voltage
divergence, dT/dt, impedance change, gas/pressure where available, and **residual
inconsistency between electrical and thermal models**—into a **calibrated hazard
probability**. A single high-temperature threshold is simple to certify but **often too
late**; an opaque classifier with no uncertainty is earlier but **difficult to trust**."

`[인쇄]` 밸런싱: "**Equal terminal voltage is not necessarily the correct target** when
cells have different capacities and resistances. Depending on the operating objective,
the pack may instead minimize **predicted end-of-charge margin, SOC spread,
heat-generation spread, or future power limitation**."
→ `[해석]` **밸런싱 목표가 셀 파라미터(용량·저항)의 함수**라는 것은 곧
**밸런싱이 추정 오차를 증폭한다**는 뜻이다. 리뷰는 그 증폭을 재지 않는다.
(`bms-balancing/` 갈래와 같은 축이다 — 그쪽 수치의 정본은 그 폴더다.)

---

# 10. §6 + §6.1 — 디지털 트윈, 그리고 **ASSB 한 문단**

## 10.1 `[인쇄]` 디지털 트윈과 능동 감지

"A battery digital twin is most useful when it maintains **identity, parameter history,
uncertainty, and traceable links** among cell, module, pack, vehicle, and fleet
information **rather than serving as a dashboard or duplicate neural network**."
"each update needs **model identity, training-data lineage, validation results, and
rollback capability**."
→ `[해석]` **우리 `provenance` 축과 같은 요구다** (서명·계보·롤백).

`[인쇄]` 능동 감지: "the BMS can **schedule a bounded pulse, altered charging segment, or
short rest when uncertainty becomes high**. … This is a genuine transition from passive
estimation to active intelligence because **the controller chooses not only an action but
also an information-gathering experiment.** The safety condition is that **the experiment
itself remains inside a validated electrochemical and thermal envelope**."

## 10.2 ★ §6.1 — ASSB 가 나오는 유일한 자리 (`[인쇄]` 전문에 가깝게)

> "The architecture can be **chemistry-agnostic at the level of information flow** —
> sensing, estimation, uncertainty, constraint supervision, actuation, and
> version-controlled learning — but its **state definitions, constraints, and diagnostic
> maps are chemistry-specific**. **For all-solid-state batteries, stack pressure becomes
> a coupled state/control variable because contact loss, interfacial impedance, cracking,
> and short-circuit risk depend on electro-chemo-mechanical conditions.** Reviews
> emphasize that many laboratory solid-state cells still rely on high external pressure,
> whereas practical targets are moving toward much lower operating pressure; **Xu et al.
> (2024) note industrial requirements below approximately 1 MPa**, and recent low-pressure
> reviews identify pressure reduction as a central commercialization problem (Zhang et al.,
> 2025). **A solid-state BMS may therefore need pressure or force sensing,
> pressure-dependent impedance models, and diagnostics capable of distinguishing contact
> loss from ordinary electrochemical aging (Biçer et al., 2025).**"

★★★ `[해석]` **마지막 문장이 우리 닻 질문이다.**
"**contact loss 를 보통의 전기화학적 노화와 가르는 진단**" — `questions/
assb-contact-loss-vs-lampe.md` 가 묻는 것이 문헌에서 **요구 사항으로** 적혀 있다.
⚠ **그리고 그 요구가 매단 인용 1 편(Biçer 2025)도 종설이다** (G8).
⚠⚠ **정량은 0 이다** — `θ`·면적분율·퍼콜레이션·모형 형태 어느 것도 없다.

★ `[재현]` **`MPa` 는 12 쪽 전체에 딱 한 번 나오고 그 값이 `1` 이다.**
우리 [[assb-stack-pressure-operating-window]] 가 가진 실측과 나란히 놓으면:

| 출처 | 압력 | 역할 |
|---|---|---|
| `assb` 6호 Lee 2020 (제작) | **490 MPa** (WIP, 등방) | 계면을 만든다 (비가역) |
| `assb` 7호 Spencer-Jolly 2023 (제작) | 400 MPa (일축) | 〃 |
| `assb` 4호 Shi 2020 (개입) | **300 MPa** 재가압 | `θ_AM` 을 되돌린다 |
| `assb` 5호 Doux 2020 (상한) | **75 MPa** 에서 도금 전 기계적 단락 | Li 금속 셀의 위 벽 |
| `assb` 5호 (운전 권고) | 5 MPa (>1000 h 무단락) | |
| `assb` 6호·7호 (운전) | **2–4 MPa** | 무음극 파우치 / 반쪽전지 |
| **8호 (재인용 산업 요구치)** | **< ≈1 MPa** | **위 전부보다 아래다** |

`[해석]` **우리가 문헌에서 읽어 온 압력 창 전체가 산업 요구치 위에 있다.**
→ [[assb-pressure-reapplication-separation-test]] 의 `P↑` 연산자는 **산업 셀에서는
더더욱 쓸 수 없고**, 거꾸로 **`θ_AM` 의 시간 변화가 산업 조건에서 더 클 것**이라는
방향이 생긴다. ⚠ **재인용이다. Xu 2024 를 받아야 한다** (G3, §15 1순위).

## 10.3 `[인쇄]` Li–S 와 나트륨이온 — 우리 축의 **다른 화학 판본**

Li–S: "Their voltage behavior contains **regions in which conventional OCV and
Coulomb-counting assumptions are less informative**, and state estimation often requires
chemistry-specific dynamic or electrochemical models. Reviews of Li–S BMS methods
therefore emphasize Bayesian filtering and data-driven alternatives **rather than direct
reuse of lithium-ion observers** (Ayadi et al., 2022)."
→ ★ `[해석]` **"OCV 가 정보를 안 주는 구간" 이 상태 추정을 깬다는 것**이 또 다른
화학에서 반복된다. 우리 LFP 의 `(X1, X3)` 축퇴
([[ic-peak-area-direct-mode-readout-lfp]])·ASSB 의 평탄 상대극과 **같은 형태의 문제**다.
⚠ 리뷰는 셋을 연결하지 않는다 (LFP 도 ASSB 평탄 상대극도 언급 없다).

나트륨이온: "much of the BMS architecture is transferable, but **OCV–SOC relations,
thermal behavior, aging signatures, and safety limits require recalibration**." +
"Liu et al. (2025) reported **R² = 0.998 for SOC and 0.997 for SOH** using partial
charging data across 53 sodium-ion cells and two packs at 0 °C–45 °C. This result
supports **transfer of methodology, not transfer of parameters**."

## 10.4 `[인쇄]` 이식 가능/불가능의 경계 — 이 리뷰의 가장 깔끔한 문단

> **이식 가능**: "sensing → estimation → uncertainty assessment → constraint supervision
> → actuation → version-controlled learning" 의 **구조**.
> **재교정 필수**: "the **latent states** to be estimated, the **electrochemical features
> that are observable**, the safe **voltage/temperature/pressure envelope**, **degradation
> signatures**, and **the mapping from diagnostic features to failure modes**."
> "a common software architecture can reduce development burden, but **common numerical
> parameters or diagnostic thresholds should not be assumed** across lithium-ion,
> solid-state, lithium–sulfur, and sodium-ion systems."

`[해석]` ★ **"어느 잠재 상태가 관측 가능한가" 와 "feature → 고장 모드 사상" 이
화학마다 다시 정해져야 한다**는 것은, 우리가 액체셀 결론을 ASSB 로 옮기지 않는다고
적어 둔 규율([[assb-contact-loss-vs-lampe]] "주장하지 않는 것")과 **같은 말**이다.
문헌에서 인용 가능한 형태로 적혀 있다.

## 10.5 `[인쇄]` 팩 수준 검증이 보고해야 할 것 (그대로 옮긴다)

"a stress test should record the **maximum cell temperature**, **cell-to-cell temperature
spread**, **voltage/SOC spread**, **minimum electrochemical safety margin**, **false-alarm
and missed-detection rates** for fault logic, **95th-percentile or worst-case
state-estimation error near operating limits**, and **end-to-end control latency**. The
same protocol should be repeated under **sensor bias, missing measurements, cooling
degradation, aged-cell mismatch, and communication loss**."

→ ★★ `[해석]` **"운전 한계 근방의 95 분위/최악 오차"** 가 검증 항목으로 명시돼 있다.
이것이 이 리뷰에서 **점추정 금지 규율에 가장 가까운 문장**이다.

---

# 11. §6.2 — 학습형 BMS 의 안전 보증 (우리 provenance 축)

`[인쇄]` 표준의 범위를 **정직하게** 적는다:
- "**ISO 26262** … It **does not provide a ready-made certification recipe for every ML
  estimator**, but it motivates traceable requirements, hazard analysis, verification
  evidence, and controlled change."
- "**UL 4600** is an **autonomous-products** safety standard **rather than a
  battery-specific BMS standard**."
- "These standards should therefore be **cited with their actual scope** rather than
  presented as direct certification standards for battery algorithms."
→ `[해석]` **이 리뷰에서 인용 규율이 가장 잘 지켜진 문단이다** (D1·D2 와 대조된다).

`[인쇄]` 핵심 난점: "**the deployed function changes after validation**."
`[인쇄]` 처방 체인: "offline training with traceable data and fixed preprocessing;
**shadow-mode evaluation without control authority**; regression, fault-injection, and
domain-shift testing; hardware-in-the-loop verification of timing and fallback behavior;
limited vehicle validation; **signed release with a unique model version**; and
**rollback** if post-deployment monitoring detects performance outside the approved
envelope." · "a safety-critical on-board estimator or controller **should not change
autonomously between validated releases**."

→ ★ `[해석]` **우리 게이트 리뷰 루프·`source_digest` 서명·fail-closed 검사와 같은
구조다** (`wiki/guides/gate-review-loop.md` ·
[[provenance-fail-closed-verification]]). 다른 분야에서 독립적으로 같은 결론에
도달한 외부 사례로 인용할 수 있다.

---

# 12. §7 + Table 4 — 로드맵

`[인쇄]` 캡션: "Proposed testable roadmap … **TRL ranges are proposed targets rather than
ratings of the cited literature**." (G5)

| 기간 | 목표 | 측정 가능한 산출 | 데이터 요구 | 검증/TRL | **주요 실패 모드** |
|---|---|---|---|---|---|
| 단기 1–3 y | **전기화학 관측성 + 불확실성** | "Report **boundary-case error**, **calibration curves**, runtime/memory; compare **sparse EIS/DRT, relaxation and pulse features under common protocols**" | 다중 온도 셀 데이터 + **센서 바이어스·결측·복수 노화 모드·raw 진단 메타데이터** | Cell + HIL; TRL 4–5 | "Domain shift; **false confidence**; diagnostic noise" |
| 단기 1–3 y | **재현 가능한 model cards** | "Record chemistry, format, current/T range, sampling, preprocessing, target labels, compute platform and **known invalid regions**" | 공개 벤치마크 분할 + 독립 hold-out 셀 | Cell/module 반복; TRL 4–5 | "**Selective reporting; hidden leakage; incomparable metrics**" |
| 중기 3–5 y | **폐루프 충돌 중재** | "Demonstrate **hard-constraint veto and graceful derating** during cold fast charge, imbalance, cooling limits and sensor faults" | 동기화 전기/열 신호 팩 데이터 + **통제된 결함 주입** | Module/pack HIL + vehicle; TRL 5–6 | "**Weakest-cell violation**; unstable optimizer; sensor drift" |
| 중기 3–5 y | **팩 수준 능동 진단** | "Trigger information-seeking pulses **only when expected information gain justifies electrochemical/comfort cost**" | 변환기 잡음 포함 팩 임피던스/동적 데이터 | Pack/vehicle; TRL 5–6 | ★ "**Unidentifiable pulse response**; extra aging; EMI contamination" |
| 장기 5+ y | **화학 적응형 디지털 트윈** | "Transfer architecture while recalibrating chemistry-specific observability and constraints; **include pressure for solid state**" | 교차 화학 플릿 데이터 + 추적 가능한 버전 | Fleet/vehicle; TRL 6–8 | ★ "**Negative transfer; pressure/contact failure**; new aging modes" |
| 장기 5+ y | **학습 갱신의 safety case** | "Signed frozen releases, shadow-mode evaluation, rollback, cybersecurity and evidence-based approval gates" | 종단 현장 증거 + 회귀/결함/적대적 테스트 스위트 | Vehicle/fleet safety case; TRL 6–8 | "Unsafe update; corrupted data; connectivity loss; certification drift" |

★★ `[해석]` **우리 축이 실패 모드 열에 두 번 들어 있다**:
"**Unidentifiable pulse response**"(중기) · "**pressure/contact failure**"(장기).
**측정 방법은 어디에도 없다** — 이름만 올라가 있다.

`[인쇄]` 표준화 요구: "Future publications should state **whether target-battery
calibration data were used**, **whether uncertainty was calibrated rather than merely
produced**, and **whether reported latency includes feature acquisition**. For
electrochemical diagnostics, the acquisition protocol—**frequency set, perturbation
amplitude, SOC, temperature, and validation criteria**—should be reported together with
the state-estimation metric."

`[인쇄]` 성숙 판정 규칙: "A research priority is considered mature **only when its claimed
benefit remains valid under the failure mode that is most likely to invalidate it**."
→ `[해석]` **적대적 게이트 리뷰의 정의를 한 문장으로 적은 것이다.**

`[인쇄]` 결론 마지막 문장: "a layered BMS in which **uncertainty-aware estimation and
electrochemical diagnostics define what is known, a deterministic supervisor defines what
is allowed, and adaptive optimization determines what is preferred only inside that safe
set**."

---

# 13. 어긋남 원장

> 규율: **개수를 목표로 세우지 않았다.** 아래는 실제로 대조해서 어긋난 것만이고,
> 원문을 두 번 이상 읽고도 어긋나지 않는 항목은 적지 않았다.
> ★ 이 논문은 **자기 실험이 0** 이므로, 4–7 호에서 지배적이던 형태
> ("결론을 떠받치는 문장이 자기 그림과 충돌") 대신 **인용 어긋남**이 주종이다.

## D1 ★★★ 재인용이 원전을 넘어선다 (우리 위키로 검증됨)

리뷰 `[인쇄]` Table 3 "SOH RMSE **≤0.873 %** in Su et al. (2024)" · §3.1 "reported SOH
RMSE **within** 0.873 %".
원전(`raw/papers/su2024_drt-soh-health-features.md`): 0.873 % 는 **5 셀 평균**,
**cell5 = 1.607 %** → **상한이 아니다**. 그리고 같은 논문의 **Feature2(원시 EIS)
0.573 %**, Feature3 **0.672 %** 가 제안 feature 를 **모든 지표에서 이긴다**.
`[해석]` **리뷰는 원전의 과장을 부등호로 굳히고, 원전이 자기 대조군에 졌다는 사실을
전달하지 않는다.** → §7.2.
⚠ Table 2 의 나머지 7 행에도 같은 일이 있는지는 **우리가 확인하지 못했다** (G2).

## D2 ★★ 이 리뷰의 유일한 "식별 가능성" 인용이 **주제가 다른 논문**이다

`[인쇄]` p.2: "Voltage-only estimators … may become **poorly identifiable** when
temperature, aging mechanism, or chemistry changes **(Liu et al., 2026)**."
참고문헌의 유일한 Liu et al. 2026: `[인쇄]` "Liu, X., Wang, G., Du, W., Jin, C., and Liu,
X. (2026). **Silicon-carbon composite anodes for lithium-ion batteries: synthesis,
architecture, interfacial regulation, and practical prospects**. *Front. Mech. Eng.* 12,
1860708."
`[해석]` **Si–C 음극 소재 종설**이다. 추정기 식별 가능성과 관계가 없고, 같은 Frontiers
계열 자매지다. → **리뷰의 Q4 관련 주장에 붙은 근거가 사실상 0** (§14 Q4).

## D3 ★★ Figure 2 가 "lexicographic" 이라 적고 `min()` 을 계산한다

`[도표]` 그림 하단: "Priority is **lexicographic**". `[도표]` 그림 상자:
`Icmd = min(IV, IT, Iplate, Ipower, Iimbalance, Iuncertainty)`.
`[해석]` **min 은 인수 순서에 불변**이므로 §4 의 5 단계 우선순위
(`[인쇄]` "(1) hard safety and isolation … (5) charging-time demand")는 **결과에 영향이
없다**. 사전식 순서가 의미를 갖는 경우(동시 만족 불가)가 흐름도에 없다.
→ **논문의 중심 구조 주장이 자기 그림에서 구현되지 않는다.** → §8.3.

## D4 ★★ 본문이 Figure 1 에 없는 요소를 Figure 1 의 것이라 부른다

`[인쇄]` §6.2: "The deterministic safety supervisor **in Figure 1**".
`[도표]` Figure 1 에는 safety supervisor 상자가 **없다**(여섯 상자 + BMS Core +
Future priorities 띠뿐). safety supervisor 는 **Figure 2** 에 있다.
⚠ 더해서: 초록의 `[인쇄]` "**layered** vehicle–edge–cloud architecture" 가 Figure 1 에
**층으로 그려져 있지 않고**, 여섯 상자가 BMS Core 와 **전부 대칭 양방향 화살표**다 —
본문이 `[인쇄]` "should not compete **symmetrically**" 라고 반대한 구조다. → §3.2.

## D5 ★ 심사 응답 문장이 게재본에 남아 있다

`[인쇄]` §2 "Table 2 addresses **the reviewers' request** for quantitative comparison." ·
`[인쇄]` §4 "This resolves **the reviewer's example** directly." ·
`[인쇄]` §1 "**The uploaded** 2023 review usefully organized …".
`[해석]` 원고와 심사 응답서가 섞였다. `[인쇄]` Generative AI statement(Figure 1 제작에
생성형 AI 사용)와 접수→게재 **39 일**과 같이 놓으면 **편집 공정의 품질 신호**다.
⚠ 내용의 오류는 아니다 — 그러나 **재인용을 그대로 믿으면 안 되는 이유**에 무게를 더한다.

## D6 ★ PyBaMM 인용의 서지가 DOI 와 다른 곳을 가리킨다

`[인쇄]` "Sulzer, V., Marquis, S. G., Timms, R., Robinson, M., and Chapman, S. J. (2021).
Python battery mathematical modelling (PyBaMM). ***J. Open Source Softw.* 6, 3080**.
doi: **10.5334/jors.309**."
`[해석]` DOI 접두 `10.5334` 는 Ubiquity Press(= *Journal of Open Research Software*)이고
*Journal of Open Source Software* 는 `10.21105` 를 쓴다 → **학술지명·권·쪽과 DOI 가
서로 다른 출판물을 가리킨다.**
⚠ **원 논문을 열어 확인한 것이 아니라 DOI 접두로 판단했다.** 우리가 쓰는 도구의
인용이라 적어 둔다.

## D7 ★ `Liu et al. (2025)` 가 두 편인데 a/b 구분이 없다

`[인쇄]` 참고문헌: Liu, **H.** et al. (2025) *Nat. Commun.* 16, 1137 (현장 데이터
multi-modal) / Liu, **J.** et al. (2025) *J. Energy Storage* 135, 118357 (나트륨이온).
본문 §3 "multimodal field-data frameworks … (Liu et al., 2025)" = 전자,
§6.1 "Liu et al. (2025) reported R² = 0.998" 과 Table 2 = 후자.
→ **본문만 읽고는 어느 쪽인지 갈 수 없다.**

## D8 ★ Birkl 2017 이 내용과 무관한 자리에 붙어 있다

`[인쇄]` §3.1 끝: "As summarized in **Table 3** … (Birkl et al., 2017)."
Table 3 은 EIS/DRT/GITT/active pulse 표이고, Birkl 2017 은 **OCV/DV 기반 열화 모드
진단** 논문이다. `[재현]` 이 리뷰 전수 검색에서 `LLI` · `LAM` · `degradation mode` ·
`incremental capacity` · `differential voltage` · `half-cell` 이 **모두 0 회**다.
→ `[해석]` **열화 모드 진단의 원전을 인용해 놓고 그 개념을 한 번도 쓰지 않는다.**

## D9 ★ 비교표의 한 열이 비교 불가능하다

`[인쇄]` Table 2 의 `Computational burden` 값: "Low–medium online" · "Medium" ·
"Medium–high training; medium inference" · "Higher acquisition burden".
논문 스스로 `[인쇄]` "expressed as a **relative deployment burden** … this avoids
assigning artificial precision to incomparable hardware" 라고 변호하지만
`[해석]` **무엇 대비 relative 인지가 없다** → 이 열로는 어떤 순서도 나오지 않는다.
그리고 같은 논문이 `[인쇄]` "incomparable metrics" 를 단기 실패 모드로 꼽는다 (Table 4).

## D10 ⚠ (어긋남이라기보다 관측) 자기 권고를 만족하는 증거가 표 안에 1 행뿐

`[재현]` Table 2 의 `Validation level`: **7 / 8 이 `Cell`**, `Cell + pack` 1 행
(Liu 2025, 그마저 "pack validation still limited").
그런데 §6.1·§7 은 **팩 수준 검증**을 요구한다.
`[해석]` 리뷰의 권고와 리뷰가 고른 증거 사이의 거리를 **논문이 명시하지 않는다.**
`Uncertainty output` 열도 같다 — **보정된 불확실성 0 / 8** 인데
"calibrated uncertainty" 를 생산 요건으로 적는다 (§6.3).

---

# 14. 우리 축 Q1~Q8 판정

| Q | 판정 | 근거 |
|---|---|---|
| **Q1** 접촉 손실 정량 | **없다** — 정량 0. ★ **그러나 이 계보 최초로 "가르는 진단이 필요하다" 를 요구로 인쇄한다** | `[인쇄]` §6.1 "diagnostics capable of **distinguishing contact loss from ordinary electrochemical aging**" (Biçer 2025). `contact loss` **2 회**(§6.1 본문 + Table 4 "pressure/contact failure"). `θ`·면적분율·`percolat*`·`tortuos*` **0 회** |
| **Q2** 독립 관측 | **없다 — 리뷰다.** 자기 실험 0, 1 차 데이터 0. ★ 대신 **처방**: EIS/DRT/GITT/active pulse 네 채널의 역할 분담(Table 3) + ASSB 용 "**pressure or force sensing**" | Table 3 · §6.1 |
| **Q3** 라벨 층위 | **★★★ 이 계보 최초로 라벨·불확실성 층위를 표의 열로 만든다** — 단 **층위가 다르다** | Table 2 의 `Training/chemistry boundary` · `Validation level` · **`Uncertainty output`** 열. `[재현]` **보정된 불확실성 0 / 8**, `Cell` 검증 **7 / 8**. `[인쇄]` "Field labels are limited"·"**no direct capacity labels**"·생산 추정기 3 요소(estimate + calibrated uncertainty + validity flag). ⚠⚠ **열화 모드 라벨은 0** — `LLI`·`LAM`·`degradation mode` 전수 0 회. **이 리뷰의 SOH 는 끝까지 스칼라다** |
| **Q4** 유일성 | **★★ 여전히 0 (8/8 편) — 그러나 성질이 바뀐다.** 이 계보에서 처음으로 **식별 가능성을 실패 모드로 명명**한다 (`identifiab*` **5 회**; `assb` 1–7 호는 전부 0 회) | `[인쇄]` Table 1 "ECMs … can **lose physical uniqueness**" · §2 "**Parameter identifiability** … can make a detailed model **appear more precise than the available measurements justify**" · Table 1 "excitation design, **identifiability**, and measurement time constrain on-board use" · Table 3 "**Ill-posed inversion needs regularization**" · **Table 4 중기 실패 모드 "Unidentifiable pulse response"** · §3.1 "what **minimum excitation can resolve** the safety-relevant process". ⚠ **측정 0**: 조건수·프로파일 가능도·근최적 폭·Fisher/CRB **전부 없다**. `uniqueness` 1 회에 붙은 인용 4 편은 **전부 모형/매개화 논문**이고, `poorly identifiable` 문장의 인용은 **Si–C 음극 종설**이다 (D2) |
| **Q5** Li-In 기준극 | **해당 없음** — `indium` · `Li–In` **0 회** | — |
| **Q6** 압력 | **★ 부분 — 재인용 수치 1 점 + 처방 3 개** | `[인쇄]` §6.1 "stack pressure becomes a **coupled state/control variable**" · "Xu et al. (2024) note industrial requirements **below approximately 1 MPa**" · "**pressure or force sensing**, **pressure-dependent impedance models**" · Table 4 장기 "**include pressure for solid state**" / 실패 모드 "**pressure/contact failure**". `[재현]` `MPa` **전체 1 회**, 그 값이 1. ★ **우리가 읽어 온 압력 창 전체(2–490 MPa)가 이 요구치 위에 있다**. ⚠ **재인용** — Xu 2024 필요 |
| **Q7** dead Li / SEI Li | **없다.** `plating` 9 회는 전부 **액체셀 저온 급속충전의 제약(gate)** 이고, dead Li ↔ SEI Li 분해는 0. 무음극 0 회 | Fig. 2 "Electrochemical gate: plating / voltage margin" |
| **Q8** 양극 화학·OCP 기울기 | **없다** (ASSB 양극 화학 0). ★ **인접 관측 하나**: `[인쇄]` Li–S "voltage behavior contains **regions in which conventional OCV and Coulomb-counting assumptions are less informative**" · Na-ion "**OCV–SOC relations … require recalibration**" | §6.1 |

## 14.1 누적 — **칸은 늘지 않는다**

`[해석]` **8 편 누적 ≈7.0 / 8 그대로다.** Q1 은 정량이 0 이고, Q4 는 이름만 올라갔으며,
Q6 은 부분(재인용 1 점)이고, Q3 은 **다른 층위**(모드 분해가 아니라 스칼라 SOH)다.

★ **대신 세 가지가 바뀐다**:
1. **Q4 의 성질** — 1–7 호: "`identifiab*` 0 회, 아무도 안 쟀다" →
   **8 호: 로드맵 표의 실패 모드 항목으로 올라갔다.** (4호가 EIS 축퇴를 인쇄로 인정한
   것과 같은 계열이되, 이쪽은 **해야 할 일의 목록**에 들어가 있다.)
2. **Q1 의 성질** — 1–7 호: "일곱 편이 일곱 개의 다른 양을 접촉 손실이라 부른다" →
   **8 호: "접촉 손실과 보통 노화를 가르는 진단이 필요하다" 가 BMS 요구 사항으로
   인쇄됐다.** 우리 닻 질문이 문헌의 요구 목록에 있다.
3. **Q6 의 아래 벽** — 실험실 창(2–490 MPa) 전체가 **산업 요구치(<1 MPa) 위**에 있다.

---

# 15. ★★★ 우리가 추가로 받아야 할 원 논문 후보

> **이 편을 읽은 실익의 대부분이 이 표다.** Mini Review 의 수치는 전부 재인용이고
> (D1 이 그 위험의 실례), 리뷰의 진짜 가치는 **어디를 파야 하는지의 지도**다.
> 아래 서지는 **이 리뷰의 참고문헌 목록에 인쇄된 그대로** 옮긴 것이다.

| 순위 | 서지 (`[인쇄]`) | 어느 Q 축을 위해 | 주의 |
|---|---|---|---|
| **1** | **Xu, H., Yang, S., Li, B. (2024). Pressure effects and countermeasures in solid-state batteries: a comprehensive review. *Adv. Energy Mater.* 14, 2303539.** doi `10.1002/aenm.202303539` | **Q6** — 이 리뷰의 유일한 압력 수치(`<≈1 MPa` 산업 요구)의 출처. [[assb-stack-pressure-operating-window]] 의 **아래 벽을 산업 요구치와 잇는다** | ⚠ **이것도 종설이다** — 그 안의 1 차 논문을 다시 캐야 한다 |
| **2** | **Zhang, J., Fu, J., Lu, P., Hu, G., Xia, S., Zhang, S. et al. (2025). Challenges and strategies of low-pressure all-solid-state batteries. *Adv. Mater.* 37, 2413499.** doi `10.1002/adma.202413499` | **Q6 · Q1** — 저압 ASSB 전용. 우리 inbox 의 **24번**(*Tailored Cathode Composite Microstructure Enables Long Cycle Life at Low Pressure*)과 **짝을 이룬다** | 종설 |
| **3** | **Biçer, E., Aksöz, A., Bakar, R., Odabaşı, Ç., Oyucu, S., Soares, M. I. et al. (2025). Solid-state batteries: chemistry, battery, and thermal management system, battery assembly, and applications — A critical review. *Batteries* 11, 212.** doi `10.3390/batteries11060212` | **Q1 · Q2** — "**접촉 손실을 보통 전기화학적 노화와 가르는 진단**" 이라는 요구가 매단 **유일한** 인용. **우리 닻 질문이 BMS 문헌에서 어떤 이름으로 불리는지** 확인할 좌표 | 종설 (MDPI) |
| **4** | **Liang, C., Tao, S., Shi, H., Lyu, Z., Ji, J. C., Dong, D. et al. (2026). Pulse excitation for active battery management systems. *npj Clean Energy* 2, 16.** doi `10.1038/s44406-026-00040-w` | **Q4 (설계 축)** — "컨트롤러가 정보 획득 실험을 고른다" 의 원전. **우리 폭 측정기의 역방향**: 원하는 폭을 얻으려면 최소 어떤 여기가 필요한가 ([[near-optimal-set-width-measurement]] §7.3) | 1 차 논문 |
| **5** | **LeBel, F.-A., Messier, P., Sari, A., Trovão, J. P. F. (2022). Lithium-ion cell equivalent circuit model identification by galvanostatic intermittent titration technique. *J. Energy Storage* 54, 105303.** doi `10.1016/j.est.2022.105303` | **Q3 · Q8** — GITT 로 OCV/동적 응답면을 뜬 원전(`>120 titration points`, −20~60 °C). **half-cell OCP 라벨을 실제로 뜨는 비용**이 숫자로 있다 | 1 차 논문 |
| **6** | **Roman, D., Saxena, S., Robu, V., Pecht, M., Flynn, D. (2021). Machine learning pipeline for battery state-of-health estimation. *Nat. Mach. Intell.* 3, 447–456.** doi `10.1038/s42256-021-00312-3` | **Q3** — Table 2 **8 행 중 유일하게 신뢰구간을 보고한 편**(179 셀). "폭과 함께 보고" 규율의 외부 선례 | 1 차 논문 |
| **7** | **Thelen, A., Huan, X., Paulson, N., Onori, S., Hu, Z., Hu, C. (2024). Probabilistic machine learning for battery health diagnostics and prognostics — review and perspectives. *npj Mater. Sustain.* 2, 14.** doi `10.1038/s44296-024-00011-1` | **Q3 · Q4** — 불확실성 **보정**을 정면으로 다루는 종설. 리뷰의 "결함 주입 검증" 처방이 매달린 곳 | 종설이지만 우리 축 정조준 |
| **8** | **Severson, K. A., Attia, P. M., Jin, N., Perkins, N., Jiang, B., Yang, Z. et al. (2019). Data-driven prediction of battery cycle life before capacity degradation. *Nat. Energy* 4, 383–391.** doi `10.1038/s41560-019-0356-8` | **Q3** — "가장 강한 정확도는 **잘 정의된 데이터셋 아래서만** 나온다" 의 근거로 이 리뷰가 지목한 편 | 우선순위 낮음 (이미 널리 알려짐) |
| — | Heenan 2023 (*Nature* 617, 507) · Attia 2020 (*Nature* 578, 397) · Dubarry/Howey/Wu 2023 (*Joule* 7, 1134) | 온도 축 · 급속충전 프로토콜 탐색 · 디지털 트윈 | 우리 축에 간접 |

`[해석]` ★ **1–3 순위가 전부 종설이라는 것 자체가 관측이다.** §6.1 의 ASSB 문단은
**종설이 종설 셋을 인용한 문단**이고, 그 아래에 1 차 측정이 없다 (G8).
→ **ASSB 접촉 손실 정량의 1 차 원전은 여전히 `assb` 1–7 호 쪽에 있고, Q1 의 공백은
이 리뷰로 메워지지 않는다.** (닻의 1 순위 후속 후보 **Koerver 2017** 은 이 리뷰가
인용조차 하지 않는다 — 참고문헌 48 편에 `Koerver` **0 회**.)

---

# 16. 우리 프로젝트와의 접점

## 16.1 ★★★ `I_uncertainty` — 리뷰가 낸 빈칸이 우리 산출물의 소비처다

`[도표]` Figure 2 의 안전 감독기는 **여섯 개의 전류 상한 중 하나를 "불확실성" 에서**
뽑는다. **계산법이 논문에 없다** (G1).

`[해석]` 우리 [[near-optimal-set-width-measurement]] 가 만드는 것이 정확히 그 입력의
재료다 — "이 자료로 답이 하나로 정해지는가, 안 되면 폭이 얼마인가."
사슬은 이렇게 된다:

```
관측(자료·창·율·압력)  →  근최적 집합의 폭  →  상태/파라미터 추정의 폭
                                                    →  I_uncertainty  →  I_cmd
```

⚠ **이 사슬을 우리가 닫았다고 주장하지 않는다** — 폭에서 허용 전류로 가는 사상은
아직 없고, 이 리뷰도 주지 않는다. **빈칸의 좌표가 확인된 것까지가 이번 수확이다.**

## 16.2 ★★ 인용 가능한 문헌 문장 둘

우리 논지를 **외부 문헌의 문장으로** 받칠 수 있는 자리가 둘 생겼다.

1. `[인쇄]` §2: "**Parameter identifiability, cell-to-cell variability, and uncertain
   aging mechanisms can make a detailed model appear more precise than the available
   measurements justify.**"
   → `degradation-degeneracy` 의 논지 그대로다.
   ⚠ **단 이 문장에 붙은 근거는 모형 논문 넷뿐이고 측정이 0 이다** — 인용할 때
   "리뷰가 이렇게 적었다" 까지만 말할 수 있다.
2. `[인쇄]` §6.1: "the **latent states** to be estimated, the **electrochemical features
   that are observable** … must be **recalibrated for each chemistry and cell design**"
   + "**transfer of methodology, not transfer of parameters**"
   → 우리가 [[assb-contact-loss-vs-lampe]] "이 페이지가 주장하지 않는 것" 에 적어 둔
   규율(액체셀 결론을 ASSB 로 옮기지 않는다)의 **외부 진술**이다.

## 16.3 ★★ 세 번째 "비어 있음" 원장이 붙었다

| 계보 | 편수 | 비어 있는 것 |
|---|---|---|
| 액체셀 OCV 적합 | 17 / 17 | **유일성을 잰 편 0** ([[mode-identifiability-unmeasured-lineage]]) |
| `assb` 1–7 호 | 7 / 7 | **오차막대·반복 0**, `identifiab*` 0 회 |
| **BMS/SOH 추정 (이 리뷰의 Table 2)** | **8 / 8** | **보정된 불확실성 0** (§6.3) |

`[해석]` 세 계보가 **같은 방향**으로 비어 있다.
⚠ 셋째 줄은 **리뷰가 고른 8 편을 리뷰의 분류대로 우리가 센 것**이다 (원전 대조 0,
표본 선별 기준 불명 — G2·G6). **근거의 강도가 앞 두 줄과 다르다.**

## 16.4 ★ 규율 쪽에서 가져올 것 둘

- `[인쇄]` **"95th-percentile or worst-case state-estimation error near operating
  limits"** 를 팩 검증 항목으로 둔다 (§10.5). → `bms-balancing/docs/
  NEW_MODEL_REQUIREMENTS.md` §5 의 "점추정 금지, 폭과 함께" 와 **같은 축의 외부 규율**.
- `[인쇄]` **"A research priority is considered mature only when its claimed benefit
  remains valid under the failure mode that is most likely to invalidate it."**
  → 적대적 게이트 리뷰의 정의다 (`wiki/guides/gate-review-loop.md`).

## 16.5 ⚠ 가져올 feature 는 **없다**

이 리뷰는 **feature 를 하나도 정의하지 않는다.** §3.1 의 DRT·EIS·GITT·펄스는 전부
**남의 논문 이름과 성능 숫자**이고, 정의식·물리 귀속·모드별 부호 구조는 0 이다.
우리 [[pvs-sev-degradation-mode-features]] 나 [[dv-peak-heterogeneity-descriptor]] 에
붙일 새 관측은 이 편에서 나오지 않는다.

## 16.6 우리가 이 문헌에 공급할 수 있는 것

`[해석]` 셋이 보인다 — 전부 **이 리뷰가 실패 모드로 이름만 올려 둔 칸**이다.

1. **"Unidentifiable pulse response"**(Table 4 중기) — 이름만 있고 판정 기준이 없다.
   우리 폭 측정기가 **판정 가능한 형태**로 바꿀 수 있다 (4호 EIS 3-RC 에 이미
   걸어 보기로 한 것과 같은 절차).
2. **"pressure/contact failure"**(Table 4 장기) — 우리 닻 질문이고,
   DEM 이 독립 라벨을 줄 수 있는 유일한 자리다.
3. **`I_uncertainty` 의 정의** — §16.1.

⚠ **셋 다 "할 수 있다" 이지 "했다" 가 아니다.** 그리고 이 카드는
[[assb-contact-loss-vs-lampe]] 가 명시한 대로 **보류 항목**이다.

---

# 17. 이 digest 가 주장하지 않는 것

- **이 리뷰의 수치를 우리 위키의 근거로 삼지 않는다.** 전부 재인용이고, D1 이 그
  위험의 실측 사례다. §15 의 원 논문을 받기 전까지 Table 2 의 여덟 숫자는
  **"리뷰가 이렇게 적었다" 이상이 아니다.**
- **Q4 가 깨졌다고 주장하지 않는다.** 이 편도 **유일성을 재지 않았다** — 이름을
  붙였을 뿐이다. `assb` **8 / 8 편 0** 이다.
- **`<1 MPa` 를 산업 표준으로 옮기지 않는다.** 재인용이고, 어떤 셀·제조사·조건인지
  이 리뷰에 없다 (G3).
- **"리뷰가 틀렸다" 고 주장하지 않는다.** §6.2(표준의 범위)·§6.1(이식 경계)·
  §10.5(팩 검증 항목)는 이 계보에서 읽은 것 중 **가장 규율 있는 문단**들이다.
  어긋남은 **인용과 그림** 쪽에 몰려 있다.
- **Figure 1 을 근거로 쓰지 않는다** — `[인쇄]` 생성형 AI 가 만든 개념도이고 수치가 0 이다.
