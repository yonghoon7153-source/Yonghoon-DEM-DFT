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

## Section 2 — Auerbach-Lawn Reframe Framework

### English

The reframe converts the inflated AM-AM contact field into a physically
meaningful damage-stage map by adopting Auerbach's force-based criterion
for cone-crack initiation. For a Hertzian point-contact between two
brittle elastic spheres, Auerbach (1891) established that the load
required to initiate the first cone crack scales linearly with particle
radius:

$$P_c = A \cdot \frac{K_{IC}^2 \cdot R_{\min}}{E^*}, \qquad
  E^* \equiv \frac{E}{2(1-\nu^2)} \tag{1}$$

with A ≈ 200 a dimensionless geometric constant for as-prepared
(low-flaw) ceramic surfaces (Lawn 1998, §3.4). The post-onset
progression of damage is parameterised through Lawn's multi-stage
classification (Lawn 1998, Table 3.4), in which successive damage
modes appear at increasing fractions of P_c:

| Stage | Force range | Physics |
|---|---|---|
| Intact | F < P_c | No crack |
| Microcrack | P_c ≤ F < 3·P_c | First cone crack initiates |
| Multi-crack | 3·P_c ≤ F < 11·P_c | Multiple cone/radial cracks |
| Fragmentation | 11·P_c ≤ F < 32·P_c | Surface chunks separate |
| Pulverization | F ≥ 32·P_c | Particle disintegrates |

Two consequences of equation (1) are central to the reinterpretation.
First, P_c depends linearly on R_min, so smaller particles fracture
under proportionally smaller loads — but tolerate larger *relative*
overlap δ/R, the well-known "size-effect" of brittle solids. Second,
P_c depends quadratically on K_IC, so the polycrystalline (PC) and
single-crystal (SC) NCM populations have intrinsically different
fracture thresholds. We adopt the central-value pair
(K_IC^PC, K_IC^SC) = (0.3, 1.0) MPa·m^0.5 (Quinn 2020; Liu 2020),
giving a ~11× P_c ratio between AM_P-AM_P and AM_S-AM_S contacts at
fixed R. For mixed AM_P-AM_S contacts we use the geometric mean
K_IC = 0.55 MPa·m^0.5. The Young's modulus is fixed at E_AM = 140 GPa
(Xu 2017, NCM811 nanoindentation; consistent with the project-wide DEM
input value), and Poisson's ratio at ν = 0.25 (typical ceramic).

**Force-based classification.** Because our DEM uses the LIGGGHTS
hooke/hysteresis contact model rather than nonlinear Hertz, the
overlap δ does not stand in a simple δ ∝ F^(2/3) relationship to the
contact force; the linear hooke relation F = k_n · δ — with k_n
calibrated to E_AM = 140 GPa — applies instead. We therefore use the
DEM-measured normal force F directly, comparing it against P_c via
Lawn's *force* multipliers (1, 3, 11, 32). This route is internally
consistent for AM-AM contacts: both the DEM force F and the Auerbach
P_c are computed from the same physical E_AM, so the Hooke-vs-Hertz
form-factor mismatch cancels in the ratio F/P_c. The softened SE
Young's modulus (E_SE = 1.35 GPa) does not enter, because brittle
fracture classification is applied only to AM-AM contacts; SE-related
plastic response is treated separately by the Tabor framework.

A δ-based classifier (using equation (2): δ_c = (3 P_c / 4 E* √R*)^(2/3)
with δ-multipliers 1, 2, 5, 10) is also retained as a supplementary
cross-check. Differences between the two classifications quantify the
Hooke-Hertz deviation in our cases; in practice both classifications
yield the same per-case stage distribution to within the per-stage
Lawn ±50 % uncertainty (Lawn 1998 §3.4).

**The indicator-only philosophy.** Equations (1) and the Lawn
thresholds are applied to the DEM contact field *not to claim that any
particular contact represents that level of physical penetration or
load*, but to translate each contact into the damage stage that *would*
be observed if a brittle-fracture mechanism were physically active.
The classifier output is therefore a **stress-concentration indicator**
— a per-contact label drawn from a fixed five-element vocabulary —
and the meaningful quantity is its statistical distribution across an
ensemble. The next subsection demonstrates that this distribution
recovers experimental NCM cracking observations quantitatively,
validating the indicator-only interpretation.

### 한국어

본 reframe 은 부풀려진 AM-AM 접촉 필드를 *Auerbach 의 force-기반
cone-crack initiation 기준* 으로 mapping 함으로써 물리적으로 의미
있는 damage-stage map 으로 변환한다. 두 brittle 탄성 구의 Hertzian
점접촉에 대해 Auerbach (1891) 은 첫 cone crack 을 시작시키는 load 가
입자 반경에 선형 비례함을 확립하였다:

$$P_c = A \cdot \frac{K_{IC}^2 \cdot R_{\min}}{E^*}, \qquad
  E^* \equiv \frac{E}{2(1-\nu^2)} \tag{1}$$

여기서 A ≈ 200 은 as-prepared (low-flaw) ceramic 표면의 무차원 기하
상수이다 (Lawn 1998 §3.4). 임계점 이후 손상 진행은 Lawn 의 다단계
분류 (Lawn 1998 Table 3.4) 로 parameterise 되며, 연속된 손상 모드가
P_c 의 점진적 배수에서 출현한다:

| 단계 | Force 범위 | 물리 |
|---|---|---|
| Intact | F < P_c | Crack 없음 |
| Microcrack | P_c ≤ F < 3·P_c | 첫 cone crack 시작 |
| Multi-crack | 3·P_c ≤ F < 11·P_c | 다수 cone/radial cracks |
| Fragmentation | 11·P_c ≤ F < 32·P_c | 표면 chunk 분리 |
| Pulverization | F ≥ 32·P_c | 입자 분해 |

식 (1) 에서 두 가지 결과가 재해석의 중심이다. 첫째, P_c 가 R_min 에
선형 비례하므로 작은 입자는 비례적으로 작은 load 에서 깨지지만 더
큰 *상대* overlap δ/R 을 견딘다 — brittle solid 의 잘 알려진 "크기
효과". 둘째, P_c 가 K_IC 에 제곱 비례하므로 다결정 (PC) NCM 과
단결정 (SC) NCM 은 본질적으로 다른 fracture threshold 를 갖는다. 본
연구는 중심값 쌍 (K_IC^PC, K_IC^SC) = (0.3, 1.0) MPa·m^0.5 를 채택
하며 (Quinn 2020; Liu 2020), 이는 동일 R 에서 AM_P-AM_P 와 AM_S-AM_S
접촉 사이에 약 11× 의 P_c 비를 부여한다. 혼합 AM_P-AM_S 접촉에는
기하평균 K_IC = 0.55 MPa·m^0.5 를 적용한다. Young's modulus 는
E_AM = 140 GPa (Xu 2017, NCM811 nanoindentation; project-wide DEM
입력값과 일관) 로, Poisson 비는 ν = 0.25 (전형적 ceramic) 로 고정한다.

**Force-기반 분류.** 본 연구의 DEM 은 LIGGGHTS 의 hooke/hysteresis
접촉 모델을 사용하며 비선형 Hertz 가 아니다. 따라서 overlap δ 와
접촉력 F 사이에 단순한 δ ∝ F^(2/3) 관계가 성립하지 않고, 대신
선형 Hooke 관계 F = k_n · δ 가 적용된다 (k_n 은 E_AM = 140 GPa 에
calibrated). 본 연구는 DEM 에서 직접 측정된 normal force F 를 Lawn
의 *force* 배수 (1, 3, 11, 32) 를 통해 P_c 와 비교한다. 이 경로는
AM-AM 접촉에 대해 *내부적으로 일관* 하다: DEM force F 와 Auerbach
P_c 가 모두 동일한 물리 E_AM 으로부터 계산되므로 Hooke-vs-Hertz
form-factor 불일치가 비율 F/P_c 에서 상쇄된다. Softened SE Young's
modulus (E_SE = 1.35 GPa) 는 본 식에 들어가지 않는다 — 본 brittle
fracture 분류는 AM-AM 접촉에만 적용되며, SE 의 plastic 응답은 별도의
Tabor framework 으로 처리된다.

δ-기반 분류기 (식 (2): δ_c = (3 P_c / 4 E^* √R^*)^(2/3) 와 δ-배수
1, 2, 5, 10 사용) 도 보조 cross-check 로 유지된다. 두 분류 사이의
차이는 우리 케이스에서의 Hooke-Hertz 편차를 정량화한다. 실제로 두
분류 모두 케이스별 stage 분포를 단계당 Lawn ±50 % 불확실성 (Lawn
1998 §3.4) 이내에서 동일하게 산출한다.

**Indicator-only 철학.** 식 (1) 과 Lawn threshold 들은 DEM 접촉 필드에
적용되지만, 어떤 특정 접촉이 *그 수준의 물리적 침투나 load 를
나타낸다고 주장하기 위함이 아니다*. 오히려 각 접촉을, *만약 brittle-
fracture 메커니즘이 물리적으로 활성화되어 있었다면* 관측되었을
damage stage 로 번역하기 위함이다. 따라서 classifier 출력은
**응력-집중 indicator** — 고정된 다섯-원소 어휘에서 추출된 per-
contact 라벨 — 이며, 의미 있는 양은 앙상블에서의 통계적 분포이다.
다음 절은 이 분포가 실험적 NCM cracking 관측을 정량적으로 재현함을
보여 indicator-only 해석을 검증한다.

---

<!-- Section 3 will be appended below after review. -->
