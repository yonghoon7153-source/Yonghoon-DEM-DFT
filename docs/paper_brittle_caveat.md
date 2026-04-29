# Paper Caveat — Brittle Reframe Framework

> Working draft. Each section has English + Korean parallel versions.
> File saved locally; will be committed once all sections are reviewed.

---

## Section 1 — DEM Rigid-Sphere Limitation: Honest Acknowledgment

### English

Discrete-element-method (DEM) ensembles in this work were generated in
LIGGGHTS using a **Hooke linear-spring contact model with hysteretic
energy dissipation** (LIGGGHTS `gran model hooke/hysteresis`) and a
porosity-target compaction protocol that drove the cathode mixture to
a prescribed solid fraction φ ∈ [0.62, 0.82]. Two non-trivial design
choices were made up front to incorporate plastic-flow physics within
the rigid-sphere paradigm:

**(i) Hysteretic contact model.** Unlike a pure Hertz-Mindlin elastic
contact, the hooke/hysteresis model dissipates loading-unloading
energy, partially encoding the irreversible work that plastic flow
would absorb in a real ceramic-glass system. Within the elastic-sphere
framework this is the closest available proxy for plastic dissipation.

**(ii) Softened SE Young's modulus.** The solid-electrolyte stiffness
in the simulation is reduced from its single-crystal reference value
(E_SE ≈ 24 GPa, Sakuda 2013) to **E_SE = 1.35 GPa** (≈ 18× softening).
This explicitly mimics the plastic compliance of cold-pressed
Li₆PS₅Cl — which yields under stack pressure rather than deforming
elastically — and is calibrated against experimental porosity-vs-
pressure curves.

Together these two devices capture the SE-side plastic response with
reasonable fidelity. The active-material side, however, retains its
near-rigid elastic stiffness because brittle ceramics dissipate stress
through *fracture*, not through plastic flow, and no rigid-sphere DEM
contact model — hysteretic or otherwise — can represent fracture by
construction. Consequently the AM-AM overlap field encodes the
fracture work that real NCM particles would perform as additional
elastic interpenetration, driving δ/R values well beyond any
realisable deformation: per-case median maximum overlap reaches
δ/R = 0.23 and the global maximum is 0.52, against typical literature
DEM values of 0.05–0.15 (Wang 2023; Minnmann 2021) and an explicit cap
of 0.05 in Bielefeld 2020.

A literal interpretation of the AM-AM overlap field is therefore
physically untenable. The next subsection formalises the *correct*
interpretation: this field is a relative stress-concentration
indicator, not an absolute deformation measurement, and is mapped
through an Auerbach-Lawn brittle-fracture classifier into damage-
stage statistics that recover experimental NCM cracking observations
quantitatively.

### 한국어

본 연구의 DEM 앙상블은 LIGGGHTS 의 **Hooke 선형-스프링 + 이력
(hysteresis) 에너지 소산 접촉 모델** (`gran model hooke/hysteresis`)
과 목표-기공률 압축 프로토콜로 생성되었으며, 양극 혼합물을 지정된
고체 분율 φ ∈ [0.62, 0.82] 까지 압축한다. 강체-구 패러다임 내에서
*가능한 한 plasticity 를 반영* 하기 위해 두 가지 비자명한 설계
결정이 사전에 적용되었다:

**(i) 이력 (hysteretic) 접촉 모델.** 순수 Hertz-Mindlin 탄성 접촉과
달리, hooke/hysteresis 모델은 loading-unloading 사이클의 에너지를
소산시키며, 실제 ceramic-glass 계가 plastic flow 로 흡수하는 비가역
일을 부분적으로 encode 한다. 강체-구 프레임워크 내에서 plastic
소산을 근사할 수 있는 가장 실용적인 대안이다.

**(ii) 고체 전해질 Young's modulus 의 의도적 softening.** 시뮬레이션
내 SE 의 강성은 단결정 reference 값 (E_SE ≈ 24 GPa, Sakuda 2013)
으로부터 **E_SE = 1.35 GPa** (약 18× softening) 으로 의도적으로
낮춰져 있다. 이는 cold-pressed Li₆PS₅Cl 이 stack 압력 하에서 탄성
변형이 아닌 *항복으로* 응답하는 plastic compliance 를 명시적으로
모방하며, 실험적 porosity-vs-pressure 곡선에 대해 calibrated 되어
있다.

이 두 장치를 통해 *SE 측 plastic 응답* 은 합리적 충실도로 capture
된다. 그러나 활물질 측은 거의 강체 탄성을 유지하는데, 이는 brittle
ceramic 의 응력 소산이 plastic flow 가 아닌 *fracture* 를 통해
일어나기 때문이며, 강체-구 DEM 접촉 모델은 — 이력항 유무와 무관하게
— 본질적으로 fracture 를 표현할 수 없다. 결과적으로 AM-AM overlap
필드는 실제 NCM 입자가 fracture 를 통해 수행했어야 할 일을 *추가
탄성 침투* 로 encode 하며, δ/R 값을 어떤 실현 가능한 변형보다 훨씬
큰 영역으로 끌어올린다: 케이스별 최대 overlap 의 중앙값은
δ/R = 0.23, 전체 최대값은 0.52 에 달하며, 이는 문헌의 전형적 DEM 값
0.05–0.15 (Wang 2023; Minnmann 2021) 와 Bielefeld 2020 의 명시적
cap 0.05 를 한참 상회한다.

따라서 AM-AM overlap 필드를 문자 그대로 해석하는 것은 물리적으로
불가능하다. 다음 절은 *올바른* 해석을 정형화한다: 이 필드는
절대적 변형 측정이 아닌 *상대적 응력-집중 indicator* 이며,
Auerbach-Lawn brittle-fracture classifier 를 통해 damage-stage
통계로 mapping 되어 NCM cracking 의 실험적 관측을 정량적으로
재현한다.

---

<!-- Section 2 will be appended below after review. -->
