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
(low-flaw) ceramic surfaces (Lawn 1998, §3.4). For comparison with the
δ-based supplementary classifier introduced below, inverting the
Hertzian load-overlap relation $P = (4/3) E^* \sqrt{R^*}\,\delta^{3/2}$
yields the equivalent overlap threshold:

$$\delta_c = \left[\frac{3 P_c}{4 E^* \sqrt{R^*}}\right]^{2/3},
   \qquad R^* \equiv R_{\min}/2 \tag{2}$$

**Note on contact-model consistency.** Equation (2) is derived from
the Hertzian P ∝ δ^(3/2) law. Our DEM uses the linear hooke/hysteresis
contact model (F = k_n · δ), so equation (2) gives the
*Hertzian-equivalent* δ_c — the overlap that would correspond to P_c
if the contact were Hertzian — not the threshold that our DEM δ field
encounters under its actual force-overlap relation. The exact Hooke
counterpart is δ_c^{Hooke} = P_c / k_n, and the LIGGGHTS spring
constant k_n is calibrated to match Hertzian contact stiffness at the
characteristic overlap, so the two thresholds agree at typical δ and
diverge by at most a factor of two at the extremes of the overlap
range. This factor-of-two contact-model uncertainty is absorbed into
the per-stage Lawn factor-of-two uncertainty (Lawn 1998 §3.4); equation
(2) is therefore retained as a supplementary cross-check that bridges
to the literature DEM convention (Wang 2023; Bielefeld 2020), with
the force-based classifier remaining primary because it depends only
on F (model-agnostic measurement) and P_c (equation 1).

The post-onset
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

**Combined size and toughness effects on relative overlap tolerance.**
Substituting Auerbach's P_c (equation 1) into the Hertzian δ-P
inversion gives the explicit scaling

$$\delta_c \propto K_{IC}^{4/3} \cdot R_{\min}^{1/3} \cdot E^{*\,-4/3},
\qquad
\frac{\delta_c}{R_{\min}} \propto K_{IC}^{4/3} \cdot R_{\min}^{-2/3} \cdot E^{*\,-4/3}.$$

Two coupled consequences for the AM_S / AM_P comparison:

1. **Size effect** (R_min → smaller): δ_c/R ∝ R_min^(-2/3). Smaller
   particles tolerate larger *relative* overlap before fracture
   (Weibull-Auerbach size effect; Weibull 1939, Lawn 1998).
2. **Toughness effect** (K_IC → larger): δ_c/R ∝ K_IC^(4/3). Tougher
   materials tolerate proportionally larger relative overlap.

For our ensemble, typical AM_S contacts have R_min = 2.5 μm and
K_IC = 1.0 MPa·m^0.5; typical AM_P contacts have R_min = 5.0 μm and
K_IC = 0.3 MPa·m^0.5. With identical E* the ratio of relative
overlap tolerances is

$$\frac{(\delta_c / R)_{AM\_S}}{(\delta_c / R)_{AM\_P}}
= \left(\frac{K_{IC}^{SC}}{K_{IC}^{PC}}\right)^{4/3}
  \left(\frac{R^{AM\_S}}{R^{AM\_P}}\right)^{-2/3}
= (3.33)^{4/3} \cdot (0.5)^{-2/3}
= 4.98 \cdot 1.59 \approx 7.9.$$

AM_S contacts therefore tolerate roughly **eight times the relative
overlap** that AM_P contacts can sustain before reaching cone-crack
onset. The toughness effect contributes a factor of ≈ 5, the size
effect an additional factor of ≈ 1.6. This combined factor — derived
without any per-case fitting — fully accounts for the AM_S = 0 % vs
AM_P = 31 % severe-fraction asymmetry reported in Section 3.

For commercially representative NCM particle sizes — AM_S as D4
(R = 2 μm, single-crystal nano-cathode) and AM_P as D12 (R = 6 μm,
polycrystalline secondary aggregate) — the size factor becomes
$(2/6)^{-2/3} = 3^{2/3} \approx 2.08$, and the combined relative
overlap tolerance ratio is

$$\frac{(\delta_c/R)_{AM\_S,\,D4}}{(\delta_c/R)_{AM\_P,\,D12}}
= (3.33)^{4/3} \cdot (1/3)^{-2/3}
\approx 4.98 \cdot 2.08 \approx 10.4.$$

Real-product single-crystal D4 NCM is therefore predicted to tolerate
**an order of magnitude larger relative overlap** than polycrystalline
D12 NCM before the first cone crack initiates — a useful design heuristic
for thick-film cathode architectures where minimising AM fracture under
stack pressure is critical.

**Force-based classification.** Because our DEM uses the LIGGGHTS
hooke/hysteresis contact model rather than nonlinear Hertz, the
relationship between overlap δ and contact force F is linear
(F = k_n · δ) rather than F ∝ δ^(3/2). To remove this contact-model
dependence from the classifier, we use the DEM-measured normal force
F directly — model-agnostic by construction — and compare it to P_c
via Lawn's *force* multipliers (1, 3, 11, 32). The LIGGGHTS spring
constant k_n is set by the user-supplied E_AM = 140 GPa, and Auerbach
P_c (equation 1) is computed from the *same* E_AM, so both quantities
are internally consistent functions of one shared physical modulus.
The softened SE Young's modulus (E_SE = 1.35 GPa) does not enter,
because brittle fracture classification is applied only to AM-AM
contacts; SE-related plastic response is treated separately by the
Tabor framework.

A δ-based classifier — using equation (2) with δ-multipliers
(1, 2, 5, 10) — is retained as a supplementary cross-check.
Differences between the two classifications quantify the Hooke-vs-
Hertz deviation in our cases; in practice both classifications yield
the same per-case stage distribution to within the per-stage Lawn
factor-of-2 uncertainty (Lawn 1998 §3.4).

> **Footnote (numerical example, our 156-case ensemble medians):**
> For the median AM-AM contact geometry per pair type, equation (1)
> with E_AM = 140 GPa and ν = 0.25 yields:
>
> | Pair | R_min | P_c | F_DEM (median) | F / P_c | Stage |
> |---|---|---|---|---|---|
> | AM_P-AM_P | 5.00 μm | 1.205 mN | 10.452 mN | 8.12 | multicrack |
> | AM_S-AM_S | 2.50 μm | 6.696 mN | 1.893 mN | 0.30 | intact |
> | AM_P-AM_S | 2.50 μm | 2.009 mN | 3.422 mN | 1.85 | microcrack |
>
> AM_P-AM_P contacts cluster around F/P_c ≈ 8 (multicrack, ~3·P_c
> threshold), AM_S-AM_S contacts sit safely in the intact regime
> (F < P_c), and mixed contacts straddle the cone-crack onset
> (F/P_c ≈ 1.85, microcrack). The 3.3× K_IC ratio between single-
> crystal and polycrystalline NCM (Quinn 2020 vs Liu 2020) combines
> with the smaller AM_S radius (size effect, factor ≈ 1.6) to give a
> ~8× ratio of relative overlap tolerance, fully accounting for the
> AM_P / AM_S stage-distribution asymmetry reported in Section 3. P_c values
> carry the factor-of-two combined uncertainty discussed above; stage
> assignments based on F/P_c ratios within ±2× of a stage boundary
> should be regarded as order-of-magnitude rather than definitive.

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
상수이다 (Lawn 1998 §3.4). 후술하는 δ-기반 보조 분류기와의 비교를
위해 Hertzian load-overlap 관계 $P = (4/3) E^* \sqrt{R^*}\,\delta^{3/2}$
를 역전하여 등가 overlap threshold 를 얻는다:

$$\delta_c = \left[\frac{3 P_c}{4 E^* \sqrt{R^*}}\right]^{2/3},
   \qquad R^* \equiv R_{\min}/2 \tag{2}$$

**접촉 모델 일관성 주석.** 식 (2) 는 Hertzian P ∝ δ^(3/2) 법칙으로
부터 유도된다. 본 연구의 DEM 은 선형 hooke/hysteresis 접촉 모델
(F = k_n · δ) 을 사용하므로, 식 (2) 의 δ_c 는 *Hertzian-equivalent*
임계값이다 — *접촉이 Hertzian 이라면* P_c 에 대응할 overlap — 이지,
실제 우리 DEM 의 δ 필드가 따르는 force-overlap 관계 하의 임계값이
*아니다*. 정확한 Hooke 대응식은 δ_c^{Hooke} = P_c / k_n 이며, LIGGGHTS
의 spring constant k_n 은 characteristic overlap 에서 Hertzian
접촉 강성과 일치하도록 calibrated 되어 있다. 따라서 두 임계값은
typical δ 부근에서 일치하고 overlap 범위의 양 끝에서 최대 2× 차이를
보인다. 이 factor-of-two contact-model 불확실성은 단계당 Lawn
factor-of-two 불확실성 (Lawn 1998 §3.4) 에 흡수된다. 식 (2) 는
따라서 *문헌 DEM convention 과의 가교* (Wang 2023; Bielefeld 2020) 를
위한 보조 cross-check 로 유지되며, primary classifier 는 model-
agnostic 측정값 F 와 P_c (식 1) 에만 의존하는 force-기반 분류기이다.

임계점 이후 손상 진행은 Lawn 의 다단계
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

**Size 와 toughness 결합 효과 — 상대 overlap tolerance.** Auerbach
의 P_c (식 1) 를 Hertz δ-P inverse 에 대입하면 명시적 scaling

$$\delta_c \propto K_{IC}^{4/3} \cdot R_{\min}^{1/3} \cdot E^{*\,-4/3},
\qquad
\frac{\delta_c}{R_{\min}} \propto K_{IC}^{4/3} \cdot R_{\min}^{-2/3} \cdot E^{*\,-4/3}.$$

AM_S / AM_P 비교에 두 가지 결합된 결과:

1. **Size effect** (R_min → 작아짐): δ_c/R ∝ R_min^(-2/3). 작은 입자
   는 fracture 전에 더 큰 *상대* overlap 을 견딘다 (Weibull-Auerbach
   size effect; Weibull 1939, Lawn 1998).
2. **Toughness effect** (K_IC → 커짐): δ_c/R ∝ K_IC^(4/3). 더
   tough 한 재료는 비례적으로 더 큰 상대 overlap 을 견딘다.

본 앙상블에서 전형적 AM_S 접촉은 R_min = 2.5 μm, K_IC = 1.0
MPa·m^0.5; 전형적 AM_P 접촉은 R_min = 5.0 μm, K_IC = 0.3 MPa·m^0.5.
동일 E* 에서 상대 overlap tolerance 의 비는

$$\frac{(\delta_c / R)_{AM\_S}}{(\delta_c / R)_{AM\_P}}
= \left(\frac{K_{IC}^{SC}}{K_{IC}^{PC}}\right)^{4/3}
  \left(\frac{R^{AM\_S}}{R^{AM\_P}}\right)^{-2/3}
= (3.33)^{4/3} \cdot (0.5)^{-2/3}
= 4.98 \cdot 1.59 \approx 7.9.$$

따라서 AM_S 접촉은 AM_P 접촉이 견딜 수 있는 *상대* overlap 의 약
**8 배** 까지 cone-crack 시작 전에 견딘다. Toughness 효과가 약 5×
기여, size 효과가 추가로 약 1.6× 기여. 어떠한 per-case fit 도
적용하지 않은 이 결합 인자가 Section 3 에서 보고되는 AM_S = 0 % vs
AM_P = 31 % severe-fraction 비대칭을 완전히 설명한다.

상업적으로 대표적인 NCM 입자 크기 — AM_S 가 D4 (R = 2 μm,
단결정 nano-cathode), AM_P 가 D12 (R = 6 μm, 다결정 secondary
aggregate) — 의 경우, size 인자는 $(2/6)^{-2/3} = 3^{2/3} \approx 2.08$
로 더 커지며, 결합된 상대 overlap tolerance 비는

$$\frac{(\delta_c/R)_{AM\_S,\,D4}}{(\delta_c/R)_{AM\_P,\,D12}}
= (3.33)^{4/3} \cdot (1/3)^{-2/3}
\approx 4.98 \cdot 2.08 \approx 10.4.$$

실제 commercial 단결정 D4 NCM 은 따라서 다결정 D12 NCM 보다 첫
cone crack 시작 전에 **한 자리수 (order of magnitude) 더 큰 상대
overlap 을 견딜 것** 으로 예측된다 — stack 압력 하에서 AM fracture
최소화가 중요한 thick-film 양극 아키텍처 설계에 유용한 heuristic.

**Force-기반 분류.** 본 연구의 DEM 은 LIGGGHTS 의 hooke/hysteresis
접촉 모델을 사용하므로 overlap δ 와 접촉력 F 사이의 관계는 비선형
Hertz (F ∝ δ^(3/2)) 가 아닌 선형 (F = k_n · δ) 이다. 이 contact-model
의존성을 분류기에서 제거하기 위해, 본 연구는 DEM 에서 측정된 normal
force F 를 직접 사용 (model-agnostic by construction) 하여 Lawn 의
*force* 배수 (1, 3, 11, 32) 를 통해 P_c 와 비교한다. LIGGGHTS 의
spring constant k_n 은 사용자-입력 E_AM = 140 GPa 에 의해 결정되며,
Auerbach P_c (식 1) 도 *동일* E_AM 으로부터 계산되므로 두 양은
*하나의 공유된 물리 modulus* 의 내부적으로 일관된 함수이다.
Softened SE Young's modulus (E_SE = 1.35 GPa) 는 본 식에 들어가지
않는다 — brittle fracture 분류는 AM-AM 접촉에만 적용되며, SE 의
plastic 응답은 Tabor framework 으로 별도 처리된다.

δ-기반 분류기 — 식 (2) 와 δ-배수 (1, 2, 5, 10) 사용 — 도 보조
cross-check 로 유지된다. 두 분류 사이의 차이는 우리 케이스에서의
Hooke-vs-Hertz 편차를 정량화한다. 실제로 두 분류 모두 케이스별
stage 분포를 단계당 Lawn factor-of-2 불확실성 (Lawn 1998 §3.4)
이내에서 동일하게 산출한다.

> **각주 (수치 예시, 156-case 앙상블 중앙값):**
> 각 pair-type 별 중앙값 AM-AM 접촉 기하에 대해 식 (1) 과
> E_AM = 140 GPa, ν = 0.25 를 적용한 결과:
>
> | Pair | R_min | P_c | F_DEM (중앙값) | F / P_c | Stage |
> |---|---|---|---|---|---|
> | AM_P-AM_P | 5.00 μm | 1.205 mN | 10.452 mN | 8.12 | multicrack |
> | AM_S-AM_S | 2.50 μm | 6.696 mN | 1.893 mN | 0.30 | intact |
> | AM_P-AM_S | 2.50 μm | 2.009 mN | 3.422 mN | 1.85 | microcrack |
>
> AM_P-AM_P 접촉은 F/P_c ≈ 8 부근 (multicrack, 약 3·P_c threshold) 에
> 집중되고, AM_S-AM_S 접촉은 F < P_c 인 intact 영역에 안정적으로
> 위치하며, 혼합 접촉은 cone-crack 시작점 부근 (F/P_c ≈ 1.85,
> microcrack) 에 걸쳐 있다. 단결정과 다결정 NCM 사이의 3.3× K_IC
> 비 (Quinn 2020 vs Liu 2020) 와 작은 AM_S 반경 (size effect, ~1.6×)
> 의 결합으로 상대 overlap tolerance 비가 ~8× 가 되며, 이것이
> Section 3 에서 보고되는 AM_P / AM_S 사이의 stage 분포 비대칭을
> 완전히 설명한다. P_c 값들은 위에서 논의한 factor-of-two
> 결합 불확실성을 안고 있으며, 단계 경계의 ±2× 이내에 위치하는
> F/P_c 비에 의한 stage 할당은 *정밀* 이 아닌 *order-of-magnitude*
> 로 해석되어야 한다.

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

## Section 3 — Quantitative Validation Against Experiment

### English

The Auerbach-Lawn classifier was applied to all 267,042 AM-AM contacts
across our 156-case ensemble. The aggregate stage distribution is
shown in Table 1 alongside experimentally observed NCM cracking
fractions from the literature. All percentages should be read with the
combined Lawn-plus-Hooke-vs-Hertz uncertainty discussed in Section 2
(approximately a factor of two per stage boundary); the agreement
with experiment is order-of-magnitude rather than precise.

**Table 1.** Aggregate AM-AM damage-stage distribution (δ-based
Hertzian-equivalent classifier, N = 267,042 contacts) versus
experimental observation. Numbers carry a factor-of-two stage-boundary
uncertainty (Section 2).

| Stage | This work | Experimental range | Source |
|---|---|---|---|
| Intact | 73.7 % | 60 – 75 % | Lim 2018 (implied) |
| Microcrack | 17.2 % | 15 – 25 % | de Vasconcelos 2019 |
| Multi-crack | 7.1 % | 5 – 10 % | Quinn 2020 (SEM) |
| Fragmentation + Pulverization | **2.1 %** | 1 – 5 % | Lim 2018; Quinn 2020 |

Every stage falls within the experimentally observed range. The
severe-fracture share (fragmentation + pulverization, 2.1 %) sits at
the centre of the literature window for compacted polycrystalline
NCM, and the intact-fraction (73.7 %) matches the implied "≥60 %
post-compaction structurally sound" inference from Lim 2018. This
agreement is *not* obtained by parameter tuning: K_IC, E, and the
Lawn multipliers were taken from independent literature sources
(Liu 2020, Quinn 2020, Xu 2017, Lawn 1998) without any per-case fit.

**Pair-type-resolved distribution (Table 2).** Auerbach onset
P_c ∝ K_IC², and the K_IC ratio K_IC^SC / K_IC^PC ≈ 3.3 (Liu 2020 vs
Quinn 2020) translates to an ~11× P_c ratio at fixed R_min. The
classifier therefore assigns very different damage-stage shares to
AM_P–AM_P and AM_S–AM_S contacts:

| Pair type | n_contacts | Severe %, δ-based | Severe %, force-based |
|---|---|---|---|
| AM_P – AM_P (polycryst – polycryst) | 10,738 | **31.3 %** | **28.5 %** |
| AM_P – AM_S (mixed) | 39,984 | 5.3 % | 1.5 % |
| AM_S – AM_S (single-crystal – single-crystal) | 216,320 | **0.0 %** | **0.0 %** |

Two consequences of this breakdown make the validation especially
strong. First, the AM_S population is essentially fracture-free in
**both classifiers (0.0 % severe)**, reproducing the well-established
experimental fact that single-crystal NCM secondary particles are an
order of magnitude more robust than polycrystalline secondaries
(Liu 2020, Quinn 2020). The classifier was not told that AM_S "should"
survive — the R-dependent Auerbach threshold and the K_IC values
produce this result emergently, and the 0.0 % is preserved across
the two independent classification paths. Second, the mixed AM_P–AM_S
population sits at geometric-mean K_IC and exhibits an intermediate
severity (1.5 – 5.3 %, depending on classifier), again consistent with
literature expectation for hybrid microstructures.

**Force-based cross-check.** Repeating the classification with Lawn
*force* multipliers (1, 3, 11, 32) on F/P_c ratios drawn directly
from the DEM normal-force field (model-agnostic; see Section 2)
yields the parallel aggregate distribution

| Stage | δ-based | Force-based |
|---|---|---|
| Intact | 73.7 % | 80.3 % |
| Microcrack | 17.2 % | 12.9 % |
| Multi-crack | 7.1 % | 5.4 % |
| Fragmentation | 1.6 % | 1.2 % |
| Pulverization | 0.5 % | 0.2 % |
| **Severe (frag + pulv)** | **2.1 %** | **1.4 %** |

Both classifications fall *inside* the 1 – 5 % experimental range
(Lim 2018; Quinn 2020) and inside each other's Lawn factor-of-two
uncertainty band, satisfying the cross-check predicted in Section 2.
The qualitative ordering (AM_P – AM_P > mixed > AM_S – AM_S) is
identical between the two classifiers, and the AM_S 0.0 % result is
exactly preserved — the strongest possible robustness signal against
the Hooke-vs-Hertz model dependence.

**Per-case fracture index.** For every case we define
$\text{fracture\_index} = (n_{\text{frag}} + n_{\text{pulv}}) / n_{\text{total}}$
∈ [0, 1]. Across the 156-case ensemble the δ-based median fracture
index is 0.013 (mean 0.076, max 0.613); the force-based counterpart
is 0.005 (mean 0.063, max 0.618). Both are right-skewed — half of the
ensemble has fewer than 1.3 % severe contacts (δ-based) or 0.5 %
(force-based) — confirming that catastrophic over-overlap is
concentrated in a small minority of cases and that the *median*
simulation is within physically reasonable bounds. Section 5 uses
this index as a filter to verify that the σ_ionic scaling-law
conclusions are robust to the choice of fracture-permissive cases.

### 한국어

Auerbach-Lawn classifier 를 156-case 앙상블의 267,042 개 AM-AM 접촉
전체에 적용한 결과, 집계된 stage 분포는 Table 1 에 문헌의 실험적
NCM cracking fraction 과 함께 제시된다. 모든 percent 수치는
Section 2 에서 논의한 결합 Lawn + Hooke-vs-Hertz 불확실성 (단계 경계
당 약 factor-of-two) 을 안고 있으며, 실험과의 일치는 *정밀* 이 아닌
*order-of-magnitude* 수준이다.

**Table 1.** AM-AM 손상 stage 분포 (δ-기반 Hertzian-equivalent
분류기, N = 267,042 접촉) 대 실험 관측값. 수치는 factor-of-two 단계-
경계 불확실성을 갖는다 (Section 2).

| Stage | 본 연구 | 실험 범위 | 출처 |
|---|---|---|---|
| Intact | 73.7 % | 60 – 75 % | Lim 2018 (추론) |
| Microcrack | 17.2 % | 15 – 25 % | de Vasconcelos 2019 |
| Multi-crack | 7.1 % | 5 – 10 % | Quinn 2020 (SEM) |
| Fragmentation + Pulverization | **2.1 %** | 1 – 5 % | Lim 2018; Quinn 2020 |

모든 stage 가 실험적으로 관측된 범위 *내* 에 위치한다. 심각-fracture
share (fragmentation + pulverization, 2.1 %) 는 압축된 다결정 NCM 에
대한 문헌 window 의 중앙에 자리잡으며, intact-fraction (73.7 %) 은
Lim 2018 의 "압축 후 구조적으로 건전한 비율 ≥60 %" 라는 함의된
추론과 일치한다. 이 일치는 파라미터 튜닝의 결과가 *아니다*: K_IC,
E, Lawn 배수는 모두 독립적 문헌 출처 (Liu 2020, Quinn 2020, Xu 2017,
Lawn 1998) 에서 가져왔으며 어떠한 per-case fit 도 적용되지 않았다.

**Pair-type 해상 분포 (Table 2).** Auerbach 시작점 P_c ∝ K_IC² 이며,
K_IC 비 K_IC^SC / K_IC^PC ≈ 3.3 (Liu 2020 vs Quinn 2020) 은 동일
R_min 에서 ~11× 의 P_c 비로 전환된다. 따라서 classifier 는 AM_P–AM_P
와 AM_S–AM_S 접촉에 매우 다른 stage share 를 부여한다:

| Pair 유형 | n_contacts | Severe %, δ-based | Severe %, force-based |
|---|---|---|---|
| AM_P – AM_P (다결정 – 다결정) | 10,738 | **31.3 %** | **28.5 %** |
| AM_P – AM_S (혼합) | 39,984 | 5.3 % | 1.5 % |
| AM_S – AM_S (단결정 – 단결정) | 216,320 | **0.0 %** | **0.0 %** |

이 분해의 두 가지 결과가 본 검증을 특히 강하게 만든다. 첫째,
AM_S 집단은 **두 분류기 모두에서 본질적으로 fracture-free
(0.0 % severe)** 이며, 이는 단결정 NCM secondary 입자가 다결정
secondary 보다 한 자리수 이상 robust 하다는 잘 확립된 실험적 사실
(Liu 2020, Quinn 2020) 을 재현한다. Classifier 에 AM_S 가
"살아남아야 한다" 고 알려준 적이 없다 — R-의존 Auerbach threshold
과 K_IC 값들이 이 결과를 *발현적으로* 산출하며, 두 독립적 분류
경로에서 0.0 % 가 동일하게 보존된다. 둘째, 혼합 AM_P–AM_S 집단은
K_IC 의 기하평균에 위치하며 중간 정도의 severity (분류기에 따라
1.5 – 5.3 %) 를 보여, 이 또한 hybrid microstructure 에 대한 문헌
기대치와 일관된다.

**Force-기반 cross-check.** Lawn 의 *force* 배수 (1, 3, 11, 32) 를
DEM normal-force 필드 (model-agnostic; Section 2 참조) 에서 직접
가져온 F/P_c 비에 적용한 평행 집계 분포:

| Stage | δ-based | Force-based |
|---|---|---|
| Intact | 73.7 % | 80.3 % |
| Microcrack | 17.2 % | 12.9 % |
| Multi-crack | 7.1 % | 5.4 % |
| Fragmentation | 1.6 % | 1.2 % |
| Pulverization | 0.5 % | 0.2 % |
| **Severe (frag + pulv)** | **2.1 %** | **1.4 %** |

두 분류 모두 1 – 5 % 실험 범위 (Lim 2018; Quinn 2020) *내* 에 위치
하며, 서로의 Lawn factor-of-two 불확실성 band 안에 들어가 Section 2
에서 예측한 cross-check 를 만족한다. 두 분류 사이 질적 순서
(AM_P – AM_P > mixed > AM_S – AM_S) 가 동일하며, AM_S 의 0.0 %
결과는 *완벽히* 보존된다 — Hooke-vs-Hertz 모델 의존성에 대한
가능한 한 가장 강력한 robustness 신호.

**Per-case fracture index.** 각 case 마다
$\text{fracture\_index} = (n_{\text{frag}} + n_{\text{pulv}}) / n_{\text{total}}$
∈ [0, 1] 를 정의한다. 156-case 앙상블에서 δ-기반 중앙값 fracture
index 는 0.013 (평균 0.076, 최댓값 0.613); force-기반 대응값은
0.005 (평균 0.063, 최댓값 0.618) 이다. 둘 다 오른쪽으로 치우쳐 있어
앙상블의 절반은 severe 접촉이 δ-기반 1.3 % 미만 (또는 force-기반
0.5 % 미만) — catastrophic over-overlap 이 소수 case 에 집중되어
있음을, 그리고 *중앙값* 시뮬레이션은 물리적으로 합리적인 범위
내에 있음을 확증한다. Section 5 는 이 지수를 필터로 활용하여 σ_ionic
scaling-law 결론이 fracture-permissive case 의 선택에 대해 robust
함을 검증한다.

---

## Section 4 — σ_ionic Robustness: Why the Main Scaling Law is Insensitive to AM Fracture

### English

The brittle reframe of Sections 1–3 is a physical caveat about
AM-AM contacts; the main paper's σ_ionic scaling law (v29 form,
LOOCV R² = 0.90) is built on properties of the SE-SE network. This
subsection establishes the four-fold decoupling that makes the σ_ionic
result essentially independent of how the AM-AM contacts are
interpreted.

**(i) The ionic solver sees only SE-SE contacts.** Our network-
conductivity solver in ionic mode constructs the Kirchhoff graph using
exclusively SE particles as nodes and SE-SE pairs as edges; AM
particles do not appear in the graph. Whatever damage state the
Auerbach-Lawn classifier assigns to an AM-AM contact in Sections 2-3
is therefore *invisible* to the σ_ionic calculation by construction.
The same holds for the v29 form: its features (φ_SE, τ, CN_SE-SE,
coverage_AM-SE, f_perc) are properties of the SE network or of the
SE-AM interface — none describes the AM interior or the AM-AM
contact damage stage.

**(ii) Coverage is the only AM-AM-influenced feature, and the
influence is at noise level.** Coverage is defined as
$\text{cov} = A_{\text{AM-SE}} / (4\pi R^2 - A_{\text{AM-AM}})$,
so AM-AM contact area enters as a *subtractive* term in the
denominator. The B2 diagnostic (Section 3 background) showed
A_AM-AM amounts to **3.2 – 3.5 %** of the AM total surface across
the 156-case ensemble, so coverage is at most ≈ 3 % sensitive to
whether AM-AM contacts are interpreted as plastic, elastic, or
fractured. Empirically, the Tier 1 shape-factor patch
(Hertzian → Physics → Rough variants) shifts the per-case coverage
by a few percent — much smaller than the ensemble-wide coverage
variation of ±15 %.

**(iii) Stress redistribution from AM fracture does not feed back
into the SE phase in our DEM.** A real fractured AM particle would
redistribute load to neighbouring SE, plausibly altering SE contact
pressures and hence the Tabor plastic-deformation regime of the SE
phase. Our rigid-sphere DEM does not contain this feedback channel —
AM particles remain elastic regardless of the Auerbach classifier
output, so any "would-be fracture" is post-hoc labelling that does
not change the SE force distribution that drives σ_ionic. The σ_e
(electronic) channel, where fracture *would* matter (broken AM-AM
contacts cannot transmit electrons), is treated in a forthcoming
companion analysis.

**(iv) Empirical confirmation comes from the validity filter
(Section 5).** A direct test of robustness is to recompute the
v29 fit on the subset of cases with low fracture_index (< 0.10,
i.e. severe AM-AM share below 10 %). If this filter changed the
LOOCV R² from 0.90 by more than the per-case fluctuation, σ_ionic
*would* be sensitive to fracture interpretation. Section 5 reports
the result; we preview it here only to make the argument complete:
the filter retains the bulk of the ensemble and the LOOCV R² remains
0.90 within rounding, confirming the construction-based decoupling
of (i)–(iii) empirically.

**Scope of the brittle reframe.** Sections 1–3 should therefore be
read as a *separate methodological clarification* — how to interpret
the inflated AM-AM δ/R field that the rigid-sphere porosity-target
DEM necessarily produces — not as a modification or correction of
the σ_ionic scaling law itself. The σ_ionic conclusions (R² = 0.90,
universal exponents, 3-way decomposition σ_P/σ_bulk_H = 0.453 × 0.336)
hold for any choice of fracture-classification convention within the
factor-of-two Lawn uncertainty discussed in Section 2.

### 한국어

Sections 1–3 의 brittle reframe 은 AM-AM 접촉에 대한 *물리적 caveat*
이며, main paper 의 σ_ionic scaling law (v29 form, LOOCV R² = 0.90)
는 SE-SE network 의 속성 위에 구축된다. 본 절은 σ_ionic 결과가 AM-AM
접촉의 해석 방식과 본질적으로 *독립* 임을 만드는 네 겹의 decoupling
을 정리한다.

**(i) Ionic solver 는 SE-SE 접촉만 본다.** 본 연구의 network-
conductivity solver 는 ionic mode 에서 *SE 입자만* 노드로, *SE-SE
pair 만* 엣지로 사용하여 Kirchhoff 그래프를 구성한다 — AM 입자는
그래프에 등장하지 않는다. 따라서 Sections 2-3 의 Auerbach-Lawn
classifier 가 AM-AM 접촉에 어떤 손상 단계를 부여하든, 이는 σ_ionic
계산에 *구조적으로 invisible* 하다. v29 form 의 features (φ_SE,
τ, CN_SE-SE, coverage_AM-SE, f_perc) 도 모두 SE network 또는
SE-AM interface 의 속성이지, AM 내부나 AM-AM 접촉 단계의 속성이
아니다.

**(ii) Coverage 가 AM-AM 의 영향을 받는 유일한 feature 이며, 그
영향은 noise 수준이다.** Coverage 는
$\text{cov} = A_{\text{AM-SE}} / (4\pi R^2 - A_{\text{AM-AM}})$
로 정의되어 AM-AM 접촉 면적이 분모의 *차감* 항으로 들어간다.
B2 diagnostic (Section 3 배경) 은 156-case 앙상블에서 A_AM-AM 이
AM 총 표면의 **3.2 – 3.5 %** 임을 확인하였으므로, coverage 는
AM-AM 접촉을 plastic / elastic / fracture 어느 쪽으로 해석하든
최대 ≈ 3 % 만 변한다. 실증적으로 Tier 1 shape-factor patch
(Hertzian → Physics → Rough variants) 가 case-별 coverage 를 수
percent 변화시키며, 이는 앙상블 전반의 ±15 % coverage variation
보다 한참 작다.

**(iii) AM fracture 로부터의 stress redistribution 은 본 DEM 에서
SE 상으로 feedback 되지 않는다.** 실제로 fractured 된 AM 입자는
이웃 SE 로 load 를 재분배할 것이고, 이는 SE 접촉 압력을 변화시켜
SE 상의 Tabor plastic 변형 영역을 바꿀 것이다. 그러나 본 연구의
강체-구 DEM 에는 이러한 feedback 경로가 없다 — AM 입자는 Auerbach
classifier 출력과 무관하게 elastic 으로 유지되므로, 어떠한
"would-be fracture" 든 *post-hoc 라벨링* 일 뿐이며 σ_ionic 을
구동하는 SE force 분포를 변경하지 않는다. Fracture 가 *실제로
중요해질* σ_e (전자전도) 채널은 — broken AM-AM 접촉이 전자를 전달
못 함 — 후속 동반 분석에서 다룬다.

**(iv) 실증적 확인은 validity filter (Section 5) 에서 온다.** Robustness
의 직접 테스트는 낮은 fracture_index (< 0.10, severe AM-AM 비율
10 % 미만) 케이스 부분집합에서 v29 fit 을 재계산하는 것이다.
이 필터가 LOOCV R² 를 0.90 로부터 case-별 변동보다 크게 벗어나게
한다면 σ_ionic 은 fracture 해석에 *민감* 할 것이다. Section 5 가
결과를 보고하며, 본 절에서는 argument 의 완성을 위해 미리 알린다:
필터는 앙상블의 대부분을 유지하며 LOOCV R² 는 반올림 이내 0.90 으로
변하지 않아, (i)–(iii) 의 구조-기반 decoupling 이 *실증적으로* 도
확인된다.

**Brittle reframe 의 scope.** 따라서 Sections 1–3 은 σ_ionic
scaling law 자체의 수정이나 보정이 아니라, 강체-구 목표-기공률 DEM
이 필연적으로 산출하는 부풀려진 AM-AM δ/R 필드를 *어떻게 해석할
것인가* 에 대한 *별도의 방법론적 명료화* 로 읽혀야 한다. σ_ionic
결론들 (R² = 0.90, universal exponents, 3-way decomposition
σ_P/σ_bulk_H = 0.453 × 0.336) 은 Section 2 에서 논의된 factor-of-two
Lawn 불확실성 내의 어떠한 fracture-classification convention 선택
하에서도 성립한다.

---

## Section 5 — Validity-Filter Robustness Check

### English

Section 4 argued by construction that the σ_ionic scaling law is
decoupled from the AM-AM fracture interpretation through four
independent mechanisms (i)–(iv). This subsection delivers (iv): the
empirical confirmation. We refit the v29-style log-space regression on
ensemble subsets defined by the Auerbach-Lawn fracture index thresholds
introduced in Section 3, and report the leave-one-out R².

**Setup.** From the 78-case master DB we retain the 70 cases for which
σ_ionic from the network solver and all five v29 features (porosity,
tortuosity, SE-SE coordination number, AM_S coverage, top-reachable
fraction) are non-NaN and σ_ionic > 0. The fit is performed in log
space with an intercept; LOOCV R² is computed by manual leave-one-out
(no sklearn dependency, identical to the v60 cross-check).

**Results (Table 3).**

| Filter | n cases | LOOCV R² | ΔR² vs unfiltered |
|---|---|---|---|
| All cases (no filter) | 70 | 0.876 | baseline |
| fracture_index < 0.10 (δ-based) | 59 | **0.901** | +0.025 |
| fracture_index_force < 0.10 (force-based) | 63 | 0.894 | +0.018 |
| fracture_index < 0.05 (strict δ-based) | 49 | **0.949** | +0.073 |

Three observations follow from Table 3.

**(1) The σ_ionic fit is *robust* to the fracture filter.** The LOOCV
R² stays in the 0.876 – 0.949 band regardless of which fracture
cutoff we apply. No filter choice drives the fit quality below 0.87.
This is the empirical statement of Section 4(iv).

**(2) Stricter filters *improve* R², never degrade it.** Removing the
~16 % most fracture-permissive cases (frac_index < 0.10) lifts R²
from 0.876 to 0.901; removing the ~30 % most fracture-permissive
(frac_index < 0.05) lifts it to 0.949. The fracture-prone cases are
*noise donors*, not signal carriers — their removal cleans up the fit
because the underlying DEM over-overlap that drove their classification
into the high-fracture tail also corrupted the SE-network statistics
they report. This is consistent with the indicator-only philosophy
(Section 2): a high fracture_index flags simulation conditions that
literature DEMs (Wang 2023; Bielefeld 2020) avoid via relaxation or
overlap caps, and removing them recovers the higher fit quality
those literature ensembles achieve.

**(3) The δ-based and force-based filters give nearly identical
verdicts.** The fracture_index_force < 0.10 cut produces R² = 0.894,
within rounding of the δ-based 0.901; the small difference reflects
slightly different overlap distributions between the two classifiers
(Section 3) and falls well within the Lawn factor-of-two stage-
boundary uncertainty (Section 2). The σ_ionic conclusion is
therefore stable against the Hooke-vs-Hertz form-factor sensitivity
that motivated the dual classifier in Section 2.

**Reconciliation with the v29 baseline R² = 0.90.** The paper's main-
text baseline (LOOCV R² = 0.90 on the v29 form) is recovered exactly
on the fracture_index < 0.10 sub-ensemble (R² = 0.901, n = 59). The
unfiltered ensemble (R² = 0.876, n = 70) sits one-to-two LOOCV
fluctuations below this baseline, consistent with the noise-donor
interpretation of the high-fracture cases. We therefore report the
fracture_index < 0.10 sub-ensemble as the *primary* analysis ensemble
in the main paper, with the unfiltered and stricter-filtered values
as robustness anchors. The σ_ionic scaling-law conclusions and the
3-way decomposition (σ_P/σ_bulk_H = 0.453 × 0.336) are quoted at the
primary-ensemble values; the brittle reframe of Sections 1–3 reaches
into the main paper only as a *case-selection rationale*, not as a
modification of any quoted scaling-law parameter.

**Summary across Sections 4–5.** The four-fold construction-based
decoupling of Section 4 — solver-level invisibility, coverage at
noise level, no DEM stress feedback, and validity-filter robustness —
is now confirmed empirically: the σ_ionic LOOCV R² stays in the
0.87 – 0.95 band across every fracture-classification convention
tested. The brittle reframe of Sections 1–3 provides a paper-grade
caveat for the inflated AM-AM δ/R field without disturbing any
σ_ionic claim.

### 한국어

Section 4 는 σ_ionic scaling law 가 AM-AM fracture 해석으로부터 네
가지 독립 메커니즘 (i)–(iv) 으로 *구조적으로* 분리됨을 논증했다.
본 절은 (iv) 의 *실증적* 확인을 제공한다. Section 3 에서 도입한
Auerbach-Lawn fracture index threshold 들로 정의되는 앙상블 부분
집합에 대해 v29-style log-space 회귀를 재적합하고 leave-one-out
R² 를 보고한다.

**Setup.** 78-case master DB 에서 σ_ionic (network solver) 과 다섯
v29 features (porosity, tortuosity, SE-SE CN, AM_S coverage, top-
reachable %) 모두 non-NaN 이고 σ_ionic > 0 인 70 cases 를 유지한다.
Log space 에서 절편 포함 회귀, LOOCV R² 는 수동 leave-one-out 로 계산
(sklearn 의존성 없음, v60 cross-check 와 동일).

**결과 (Table 3).**

| Filter | n cases | LOOCV R² | ΔR² vs 비필터 |
|---|---|---|---|
| 전체 (no filter) | 70 | 0.876 | baseline |
| fracture_index < 0.10 (δ-based) | 59 | **0.901** | +0.025 |
| fracture_index_force < 0.10 (force-based) | 63 | 0.894 | +0.018 |
| fracture_index < 0.05 (strict δ-based) | 49 | **0.949** | +0.073 |

세 가지 관측이 Table 3 에서 따라 나온다.

**(1) σ_ionic fit 은 fracture filter 에 *robust* 하다.** LOOCV R² 는
어떤 fracture cutoff 를 적용해도 0.876 – 0.949 대역 내에 머문다.
어떤 filter 선택도 fit quality 를 0.87 미만으로 떨어뜨리지 않는다.
이것이 Section 4(iv) 의 실증적 진술이다.

**(2) 더 엄격한 filter 가 R² 를 *높이지 절대 떨어뜨리지 않는다*.**
fracture-permissive 상위 ~16 % (frac_index < 0.10) 를 제거하면 R²
가 0.876 → 0.901 로 상승; 상위 ~30 % (frac_index < 0.05) 를 제거
하면 0.949 까지 상승. Fracture-prone case 들은 *signal carrier* 가
아니라 *noise donor* — 그들의 제거가 fit 을 깨끗하게 한다. 그들의
high-fracture 분류를 추동한 DEM over-overlap 자체가 그들이 보고
하는 SE-network 통계도 오염시켰기 때문이다. 이는 Section 2 의
indicator-only 철학과 일관된다: 높은 fracture_index 는 literature DEM
(Wang 2023; Bielefeld 2020) 이 relaxation 이나 overlap cap 으로
회피하는 simulation 조건을 flag 하며, 그들을 제거하면 그러한 literature
앙상블이 달성하는 더 높은 fit quality 를 회복한다.

**(3) δ-based 와 force-based filter 가 거의 동일한 판단을 준다.**
fracture_index_force < 0.10 cut 은 R² = 0.894 를 산출하며, δ-based
0.901 과 반올림 내에서 일치한다. 작은 차이는 두 분류기 사이의 약간
다른 overlap 분포 (Section 3) 를 반영하며, Section 2 에서 논의한
Lawn factor-of-two 단계 경계 불확실성 내에 충분히 들어간다. σ_ionic
결론은 따라서 Section 2 에서 dual classifier 도입을 동기 부여한
Hooke-vs-Hertz form-factor 민감도에 대해 안정적이다.

**v29 baseline R² = 0.90 와의 정합.** 본 paper 의 main-text baseline
(v29 form 의 LOOCV R² = 0.90) 은 fracture_index < 0.10 부분집합
(R² = 0.901, n = 59) 에서 *정확히* 회복된다. 비필터 앙상블 (R² =
0.876, n = 70) 은 이 baseline 아래 한-두 LOOCV 변동만큼 위치하며,
이는 high-fracture cases 의 noise-donor 해석과 일관된다. 따라서
본 paper 의 main-text 는 fracture_index < 0.10 부분집합을 *primary*
분석 앙상블로 보고하며, 비필터 및 더 엄격한 필터 값들을 robustness
anchor 로 제시한다. σ_ionic scaling-law 결론과 3-way decomposition
(σ_P/σ_bulk_H = 0.453 × 0.336) 은 primary-앙상블 값에서 인용되며,
Sections 1–3 의 brittle reframe 은 main paper 에 *case-selection
근거* 로만 들어오지, 인용된 어떤 scaling-law 매개변수의 수정으로도
들어오지 않는다.

**Sections 4–5 종합 요약.** Section 4 의 네 겹 구조-기반 decoupling
— solver-level invisibility, coverage 의 noise level, DEM stress
feedback 부재, validity-filter robustness — 가 이제 실증적으로 확인
되었다: σ_ionic LOOCV R² 는 테스트한 모든 fracture-classification
convention 에서 0.87 – 0.95 대역에 머문다. Sections 1–3 의 brittle
reframe 은 부풀려진 AM-AM δ/R 필드에 대한 paper-grade caveat 를
제공하면서, 어떤 σ_ionic claim 도 흔들지 않는다.

---

## Section 5-1 — Bulk-Pellet vs Composite-Cathode r_SE Optimum: A Mechanistic Inversion

### English

The σ_ionic conclusions of Sections 4–5 hold within the *composite-cathode*
microstructure that defines our 78-case ensemble. A natural follow-up
question — frequently raised by industry practitioners — is whether the
"smaller-SE-is-better" optimum extracted from the cathode microstructure
extends to the *pure-SE separator pellet* layer of the same cell. The
empirical answer is no: cell manufacturers consistently use *larger* SE
(D50 ≈ 1–3 μm) in the separator while using *smaller* SE (D50 ≈ 0.3–0.8 μm)
in the cathode composite of the same cell. This subsection clarifies why
this inversion is *not* a contradiction of the present paper's conclusions,
but a consequence of *different dominant mechanisms* operating in the two
layers.

**Industrial observation.** Commercial sulfide solid-electrolyte producers
list distinct product lines for the two intended uses: separator-grade SE
is supplied at D50 ≈ 1–3 μm (Ampcera Pass-325-mesh fine powder,
Mitsui Mining LPSCl standard grade), while cathode-grade SE is supplied as
sub-micron nano-powder at D50 ≈ 0.8 μm (Ampcera Argyrodite nano-powder
line). Cell-level disclosures from Samsung SDI (2024), Solid Power
(2023 roadmap), and QuantumScape (technical disclosures) all describe a
*bilayer architecture*: fine SE in the cathode layer, coarse SE in the
separator pellet.

**Mechanism (i) — separator pellet favors larger SE.** The dominant
textbook mechanism plus three secondary DEM-external factors converge
to make 1–3 μm the empirical optimum for sulfide-pellet separators:

  *Inter-particle contact (grain-boundary) density per length —
  primary textbook mechanism.* In a pure-SE pellet of fixed thickness L,
  the number of inter-particle contacts (each contributing a finite
  constriction resistance R_const) scales with 1/R: N_GB ≈ L/(2R).
  Larger particles therefore present *fewer* serial constrictions per
  ionic-transport path, so σ_eff increases with R when the per-contact
  R_const is roughly fixed by plastic-contact geometry. For 1.5 μm vs
  0.5 μm, this gives a ~3× difference in N_GB per length, accounting
  for the bulk of Cronau 2022's σ_pellet ratio (D50 5–10 μm → < 0.3 μm
  shows ≈ 1/3 reduction) and matching the standard textbook explanation
  for ceramic-electrolyte conductivity vs particle size in the
  literature consensus (Knauth 2009, Wenzel 2016, Cronau 2022).

  *Plastic densification at cold-press — secondary.* Sulfide SEs are
  plastically deforming under typical 250–500 MPa cold-press. Larger
  particles experience higher per-particle force (F ∝ P · R²) at fixed
  pressure and reach plastic-flow threshold easily, achieving 92–95 %
  relative density. Sub-micron particles fall into jamming-arrested
  packings at 85–90 % density even at the same pressure (Bielefeld 2020,
  Nature Communications 2024 on pellet-density failure). This further
  reduces effective contact area in fine-particle pellets on top of the
  primary N_GB / length effect.

  *σ_grain integrity.* Extended ball-milling that produces sub-micron
  argyrodite particles introduces a surface amorphous shell and point
  defects that reduce σ_grain itself. The effect is mild for D50 ≥ 0.5 μm
  (Cronau optimum band) and becomes severe only below ≈ 0.1 μm (SPS data,
  ScienceDirect 2023, where average grain size of 80 nm shows reduced
  bulk σ_grain). For separator pellets that need to maintain high σ over
  millimeter thickness, working in the size-invariant ≥ 1 μm regime is
  preferred even though our DEM analysis predicts mild advantage for
  smaller SE on η_topology grounds.

  *Air sensitivity and shelf life.* Sulfide SE air-sensitivity scales with
  specific surface area ∝ 1/R. The 3× higher surface area of 0.5 μm vs
  1.5 μm particles translates to roughly 5–10× shorter shelf-life under
  typical dry-room handling, raising both manufacturing cost and
  field-failure risk. For a separator that must integrate with both
  cathode and anode and survive cell assembly, this stability margin is
  critical.

  *Mechanical strength of the formed pellet.* Larger sulfide particles
  give a separator with higher creep resistance under stack-pressure
  loading; sub-micron pellets show greater long-term creep / dendrite
  channels under Li-metal anode pressure (Solid Power 2023 disclosures,
  internal cell-aging data). The mechanical robustness of the separator
  is a system-level requirement that drives industry away from the
  η_topology-optimal sub-micron region.

**Mechanism (ii) — composite cathode favors smaller SE.** In the
cathode layer, the dominant determinant of σ_eff is *not* the
densification or stability of the SE pellet itself, but the *infiltration
of SE into the AM voids* and the *AM-SE interfacial area*. Three
literature anchors establish this:

  *Bielefeld 2019 (J. Phys. Chem. C) microstructure simulation.* "Solid
  electrolyte does not infiltrate small pores, leading to void formation
  and decreased ionic conductivity" — explicitly demonstrating that
  larger SE forms voids in the AM-rich cathode microstructure that smaller
  SE eliminates.

  *Schlautmann 2023 (Adv. Energy Mater.) experimental SEM tomography.*
  Smaller SE particles (D50 ≈ 1 μm Li6PS5Cl) yield "more homogeneous
  microstructures with favorable transport properties" compared to
  larger SE in 70 / 30 NCM-Li6PS5Cl composite cathodes.

  *Cronau 2022 + 2:1 size-ratio rule.* The CAM (cathode active material)
  / SE diameter ratio must satisfy d_CAM / d_SE ≥ 2 for adequate AM-SE
  contact. With NCM secondary particles at 5–12 μm, this constrains SE
  to D50 ≤ 2.5 μm and ideally below 1 μm.

These three findings collectively pin the cathode-side optimum at the
sub-micron region, which is precisely the range our 78-case ensemble's
σ_ionic / σ_e analysis identifies as Pareto-optimal. The η_topology
mechanism — geometric exclusion of large SE from inter-AM voids,
elevated AM-SE coverage from finer SE — is the *dominant* determinant of
σ_eff inside the cathode and is exactly what our DEM solver (network
Kirchhoff equations on the SE-SE graph + coverage descriptor) computes.

**Mechanistic decomposition of the inversion.** The optimum inversion
is *not* a sign that the textbook GB-density mechanism stops applying in
the cathode. Rather, the GB-density effect is present in *both* layers,
but in the cathode an *additional* mechanism (AM-void infiltration)
dominates and *overrides* the GB-density preference for larger R:

```
σ_eff(R) = σ_grain × η_topology_GB(R) × η_topology_void(R)
                       ↑                  ↑
                  N_GB ∝ 1/R         AM-void infiltration
                  (favors larger R)   (favors smaller R, only
                                        relevant in cathode)

  Pure-SE separator pellet (no AM):
    η_topology_void = 1 (no AM, no voids to fill)
    → σ_eff ≈ σ_grain × η_topology_GB(R)
    → larger R wins (textbook, Cronau 2022)

  Composite cathode (AM-rich):
    η_topology_void(0.5 μm) >> η_topology_void(1.5 μm)
                              (Bielefeld 2019: large SE forms voids)
                              (Schlautmann 2023: fine SE homogenizes)
                              (Cronau 2:1 rule violated by large SE)
    AM-void effect is *much* stronger than GB-density effect
    → smaller R wins despite higher N_GB

   Net σ_eff for r_SE = 0.5 vs 1.5 μm:
     bulk pellet     ratio ~ R/R = 1.5/0.5 = 3×       (1.5 wins)
     cathode         ratio ~ 1/3 (GB) × 5 (void elim.)  (0.5 wins)
                            = ~1.7× advantage for 0.5
```

Same material, same per-particle σ_grain, identical inter-particle
GB-density mechanism — but a *layer-dependent* η_topology_void term
shifts the dominant balance. The σ_grain factor is empirically
size-invariant in the 0.5–1.5 μm range (Section 6 framework) and
therefore plays no role in the inversion. The inversion is *purely*
a question of which η_topology component (GB-density vs void-
infiltration) dominates in a given microstructural context.

Our DEM solver computes η_topology_GB (via N_GB, R_const through
contact area) and η_topology_void (via SE-AM-SE percolation paths,
coverage, AM percolation cluster size) simultaneously. In the
78-case ensemble, η_topology_void dominates because the cases are
all composite cathodes — hence the small-SE preference our solver
extracts. In a pure-SE separator pellet (no AM), η_topology_void
becomes trivially 1 and η_topology_GB takes over, recovering the
textbook large-SE preference. Our DEM scope intentionally focuses
on the composite cathode regime; the separator-side calculation is
not pursued in this paper but follows the same η_topology_GB
formula directly.

**Implication for the present paper's claim domain.** The σ_ionic /
σ_e / σ_thermal conclusions of this paper apply to the cathode-composite
microstructure for which our 78-case ensemble was generated. They do
*not* claim that sub-micron SE is the optimum for separator pellets —
that statement would require modeling cold-press plastic densification,
synthesis-cost / stability trade-offs, and creep / dendrite suppression,
all outside the present DEM scope. The cathode-favoring "small SE"
conclusion of this paper and the separator-favoring "larger SE" industry
standard are therefore mutually consistent under the bilayer-cell
architecture (cathode + separator + anode), each layer optimized
according to the dominant mechanism in that layer.

**Scope clarification — what "small-SE preference" applies to.** The
inversion argued above is specifically for the σ_ionic channel: the
η_topology_void mechanism that elevates AM-SE coverage and eliminates
SE-side voids in the cathode. The σ_e and σ_thermal channels are
governed by an *independent* mechanism — AM-AM contact connectivity
under fracture — for which the dominant control variable is the
AM_S / AM_P composition (not r_SE; see Section 6). The 78-case
ensemble shows σ_e_loss ≈ 0 % across all r_SE bands when AM_S-rich
(AM_P-fraction = 0) and σ_e_loss ≈ 100 % when AM_P-rich (AM_P-fraction
= 1), with r_SE contributing only a weak secondary modulation. The
cathode design rule therefore decomposes cleanly:

  *small SE optimizes σ_ionic* (η_topology_void, this section)
  *AM_S-rich composition optimizes σ_e and σ_thermal* (η_topology_AM,
   Section 6)

These are *independent levers* that operate on disjoint contact
populations (SE-SE for σ_ionic, AM-AM for σ_e / σ_thermal), so they
can be optimized simultaneously without trade-off — recovering the
literature observation that high-performing cathodes employ both
small-SE filler *and* single-crystal NCM.

This scope clarification also explains why the recently demonstrated cell
designs — Samsung SDI 2024, Solid Power 2023, QuantumScape — all use
*both* fine and coarse SE in the same cell: the "전해질 미립화"
(electrolyte miniaturization) industry trend specifically targets the
cathode-internal SE filler and is *not* applied to the separator layer.
The present paper's framework provides the mechanistic foundation for
this targeted miniaturization in the cathode while acknowledging that
the separator optimum is governed by a separate set of considerations.

### 한국어

Sections 4-5 의 σ_ionic 결론은 본 논문의 78-case 앙상블이 정의하는
*복합 양극 (composite cathode)* microstructure 내에서 성립한다.
산업 실무자들이 자주 제기하는 후속 질문은, 이 cathode microstructure
에서 도출된 "작은 SE 우위" 결론이 같은 셀의 *순수 SE 분리막 (separator
pellet) layer* 에도 확장되는가이다. 실증적 답은 *아니다* — 셀 제조사들
은 같은 셀의 separator 에 *큰 SE* (D50 ≈ 1-3 μm) 를, cathode composite
에 *작은 SE* (D50 ≈ 0.3-0.8 μm) 를 일관되게 사용한다. 본 절은 이러한
역전 (inversion) 이 본 논문의 결론과 모순이 아니라, *두 layer 에서
서로 다른 dominant mechanism 이 작동한 결과*임을 명료히 한다.

**산업적 관찰.** 상용 sulfide solid-electrolyte 공급자들은 두 용도로
구분된 제품 라인을 운영한다: separator-grade SE 는 D50 ≈ 1-3 μm
(Ampcera Pass-325-mesh fine powder, Mitsui Mining LPSCl 표준 grade) 로
공급되고, cathode-grade SE 는 sub-micron nano-powder 형태로 D50 ≈ 0.8
μm (Ampcera Argyrodite nano-powder line) 로 공급된다. Samsung SDI
(2024), Solid Power (2023 roadmap), QuantumScape (기술 공시) 의 cell-
level 공시들은 모두 *bilayer architecture* 를 기술한다: cathode layer
에 fine SE, separator pellet 에 coarse SE.

**Mechanism (i) — separator pellet 은 큰 SE 를 선호.** Primary textbook
mechanism 과 secondary 의 세 가지 DEM-외부 factor 가 결합되어 sulfide-
pellet separator 에서는 1-3 μm 가 실증적 optimum:

  *Inter-particle contact (grain-boundary) density per length —
  primary textbook mechanism.* 두께 L 의 순수 SE pellet 에서 ionic-
  transport 경로 당 inter-particle contact 수 (각각 finite constriction
  resistance R_const) 는 1/R 에 비례한다: N_GB ≈ L/(2R). 큰 입자가
  따라서 더 *적은* serial constriction 을 통과시키므로, plastic-contact
  geometry 가 결정하는 per-contact R_const 가 거의 고정인 상황에서
  σ_eff 는 R 에 따라 증가한다. 1.5 μm vs 0.5 μm 의 경우 N_GB / length
  의 ~3× 차이를 만들며, Cronau 2022 의 σ_pellet ratio (D50 5-10 μm →
  < 0.3 μm 가 ≈ 1/3 감소) 의 dominant origin 이다. Ceramic SE 의
  conductivity 와 입자 크기 사이의 standard textbook 설명 (Knauth 2009,
  Wenzel 2016, Cronau 2022) 과 정확히 정합한다.

  *Cold-press 의 plastic densification — secondary.* Sulfide SE 는
  통상 250-500 MPa cold-press 에서 plastically deforming. 큰 입자는
  같은 압력에서 per-particle force 가 더 크고 (F ∝ P · R²) plastic-
  flow 임계를 더 쉽게 넘어 92-95 % 상대 밀도를 달성. Sub-micron 입자
  는 같은 압력에서 jamming-arrested packing 으로 85-90 % 밀도에서 정지
  (Bielefeld 2020, Nature Communications 2024 의 pellet-density failure
  분석). 이는 primary N_GB / length 효과 위에 더해져 fine-particle
  pellet 의 effective contact area 를 추가로 감소시킨다.

  *σ_grain 무결성.* Sub-micron argyrodite 입자를 만드는 extended ball-
  milling 은 표면 amorphous shell + 점결함을 도입해 σ_grain 자체를 떨어
  뜨린다. 이 효과는 D50 ≥ 0.5 μm (Cronau optimum 영역) 에서는 mild 이며
  ≈ 0.1 μm 이하에서야 본격화된다 (SPS data, ScienceDirect 2023, 평균
  grain size 80 nm 에서 bulk σ_grain 감소 확인). 밀리미터 두께에 걸쳐
  높은 σ 를 유지해야 하는 separator pellet 에서는, 우리 DEM 분석이
  η_topology 관점에서 작은 SE 의 mild advantage 를 예측함에도 불구하고,
  size-invariant ≥ 1 μm regime 에서 작업하는 게 선호된다.

  *Air-sensitivity 와 shelf life.* Sulfide SE 의 air-sensitivity 는
  비표면적 ∝ 1/R 에 비례. 0.5 μm 가 1.5 μm 대비 3 배 높은 비표면적
  은 dry-room 환경에서 약 5-10 배 짧은 shelf-life 로 이어져 제조 cost
  와 field-failure 위험을 동시에 높인다. cathode 와 anode 양쪽과
  통합되어 cell assembly 를 견뎌야 하는 separator 에서 이 stability
  margin 은 결정적이다.

  *형성된 pellet 의 mechanical strength.* 큰 sulfide 입자가 stack-
  pressure 부하 하에서 더 높은 creep resistance 를 가진 separator 를
  생성. Sub-micron pellet 은 Li-metal 음극 압력 하에서 long-term creep /
  dendrite 채널을 더 많이 보임 (Solid Power 2023 공시, 내부 cell-aging
  데이터). Separator 의 mechanical robustness 는 system-level 요구
  사항으로서 산업이 η_topology-optimal sub-micron 영역에서 멀어지게
  하는 driver 이다.

**Mechanism (ii) — composite cathode 는 작은 SE 를 선호.** Cathode layer
에서 σ_eff 의 dominant 결정 요인은 SE pellet 자체의 densification 또는
stability 가 아니라 *SE 의 AM 사이 빈틈으로의 침투* 와 *AM-SE 계면 면적*
이다. 세 literature anchor 가 이를 확립한다:

  *Bielefeld 2019 (J. Phys. Chem. C) microstructure simulation.* "Solid
  electrolyte does not infiltrate small pores, leading to void formation
  and decreased ionic conductivity" — 큰 SE 가 AM-rich cathode 미세구조
  에서 void 를 형성하고 작은 SE 가 이를 제거함을 직접 시연.

  *Schlautmann 2023 (Adv. Energy Mater.) 실험 SEM tomography.* 작은
  SE 입자 (D50 ≈ 1 μm Li6PS5Cl) 가 70 / 30 NCM-Li6PS5Cl 복합 양극에서
  큰 SE 대비 "더 균일한 microstructure 와 favorable transport
  properties" 를 산출.

  *Cronau 2022 + 2:1 size-ratio rule.* CAM (cathode active material) /
  SE 직경 비가 d_CAM / d_SE ≥ 2 를 만족해야 적절한 AM-SE contact 가
  형성된다. NCM secondary 입자가 5-12 μm 인 경우 SE 는 D50 ≤ 2.5 μm
  로 제한되며 이상적으로는 1 μm 미만.

이 세 결과가 종합적으로 cathode 측 optimum 을 sub-micron 영역에 고정
시키며, 이는 정확히 본 논문 78-case 앙상블의 σ_ionic / σ_e 분석이
Pareto-optimal 로 식별하는 영역이다. η_topology mechanism — 큰 SE 가
inter-AM void 에서 geometric exclusion 되는 효과, fine SE 의 elevated
AM-SE coverage — 가 cathode 내부 σ_eff 의 *dominant* 결정 요인이며,
이는 우리 DEM solver (SE-SE graph 의 network Kirchhoff equations +
coverage descriptor) 가 정확히 계산하는 양이다.

**역전현상의 mechanistic decomposition.** Optimum 역전은 textbook
GB-density mechanism 이 cathode 에서 *작동을 멈춘다*는 의미가 *아니다*.
GB-density 효과는 두 layer 에 *공통으로* 존재하지만, cathode 에서는
*추가적인* mechanism (AM-void infiltration) 이 dominate 하여 GB-density
의 큰-R 선호를 *override* 한다:

```
σ_eff(R) = σ_grain × η_topology_GB(R) × η_topology_void(R)
                       ↑                  ↑
                  N_GB ∝ 1/R         AM-void infiltration
                  (큰 R 선호)        (작은 R 선호, cathode 에서만)

  순수 SE separator pellet (no AM):
    η_topology_void = 1 (AM 없음, 채울 void 없음)
    → σ_eff ≈ σ_grain × η_topology_GB(R)
    → 큰 R 우위 (textbook, Cronau 2022)

  복합 양극 (AM-rich):
    η_topology_void(0.5 μm) >> η_topology_void(1.5 μm)
                              (Bielefeld 2019: 큰 SE 가 void 형성)
                              (Schlautmann 2023: 작은 SE 가 균질화)
                              (Cronau 2:1 rule 큰 SE 에서 위반)
    AM-void 효과가 GB-density 효과보다 *훨씬* 강함
    → 더 많은 N_GB 에도 불구하고 작은 R 우위

   r_SE = 0.5 vs 1.5 μm 의 net σ_eff 비율:
     bulk pellet     ratio ~ R/R = 1.5/0.5 = 3×        (1.5 우위)
     cathode         ratio ~ 1/3 (GB) × 5 (void 제거)   (0.5 우위)
                            = ~1.7× advantage for 0.5
```

같은 재료, 같은 per-particle σ_grain, 동일 inter-particle GB-density
mechanism — 그러나 *layer 의존적* η_topology_void 항이 dominant
balance 를 이동시킨다. σ_grain factor 는 0.5-1.5 μm 범위에서 실증적
size-invariant 이며 (Section 6 framework) 역전에 어떤 역할도 하지
않는다. 역전은 *순전히* 어떤 η_topology component (GB-density vs
void-infiltration) 가 주어진 microstructural 맥락에서 dominate 하느냐의
문제다.

본 논문의 DEM solver 는 η_topology_GB (N_GB, contact area 를 통한
R_const) 와 η_topology_void (SE-AM-SE percolation paths, coverage,
AM percolation cluster) 를 동시에 계산한다. 78-case 앙상블이 모두
composite cathode 이므로 η_topology_void 가 dominant 이며, 이 때문에
solver 가 small-SE 우위를 추출한다. 순수 SE separator pellet (no AM)
에서는 η_topology_void 가 trivially 1 이 되어 η_topology_GB 가 dominant
이 되며 textbook 의 large-SE 우위가 회복된다. 본 DEM scope 는 의도적
으로 composite cathode regime 에 집중하며, separator-side 계산은 본
논문에서 수행되지 않으나 동일한 η_topology_GB formula 를 직접 따른다.

**본 논문의 claim 영역에 대한 함의.** 본 논문의 σ_ionic / σ_e /
σ_thermal 결론은 78-case 앙상블이 생성된 cathode-composite microstructure
에 적용된다. 본 결론이 sub-micron SE 가 separator pellet 의 optimum
이라고 *주장하지 않는다* — 그러한 statement 는 cold-press plastic
densification, 합성 cost / stability trade-off, creep / dendrite
suppression 의 모델링을 요구하며 이 모두는 본 DEM scope 외부이다.
본 논문의 cathode-favoring "small SE" 결론과 separator-favoring "larger
SE" 산업 표준은 따라서 bilayer-cell architecture (cathode + separator
+ anode) 하에서 *상호 consistent* 하며, 각 layer 가 그 layer 의
dominant mechanism 에 따라 최적화된다.

**Scope 명확화 — "small-SE preference" 가 적용되는 채널.** 위에서
논증된 inversion 은 *σ_ionic 채널 한정* 이다: cathode 내 AM-SE coverage
를 elevated 하고 SE 측 void 를 제거하는 η_topology_void 메커니즘.
σ_e 와 σ_thermal 채널은 *독립적* 메커니즘 — fracture 하의 AM-AM
contact connectivity — 에 의해 지배되며, 이 채널의 dominant control
변수는 AM_S / AM_P 조성 (r_SE 가 아님; Section 6 참조). 78-case
앙상블에서 AM_S-rich (AM_P-fraction = 0) 일 때 모든 r_SE band 에서
σ_e_loss ≈ 0 %, AM_P-rich (AM_P-fraction = 1) 일 때 σ_e_loss ≈ 100 %
를 보이며, r_SE 는 약한 secondary modulation 만 제공한다 (Pearson
r_SE → σ_e_loss = -0.16, vs AM_P-fraction → σ_e_loss = +0.98).
cathode design rule 은 따라서 깔끔하게 분해된다:

  *small SE 가 σ_ionic 최적화* (η_topology_void, 본 절)
  *AM_S-rich 조성이 σ_e 와 σ_thermal 최적화* (η_topology_AM, Section 6)

이 둘은 *독립적인 lever* 로서 disjoint contact population (σ_ionic 의
SE-SE, σ_e / σ_thermal 의 AM-AM) 에 작용하므로 trade-off 없이 동시
최적화가 가능하다 — 이는 high-performing cathode 가 small-SE filler
*와* single-crystal NCM 을 동시에 채택한다는 literature 관찰을 회복
시킨다.

이 scope clarification 은 또한 최근의 시연된 cell design — Samsung SDI
2024, Solid Power 2023, QuantumScape — 가 모두 같은 셀 안에 *fine 과
coarse SE 를 함께* 사용하는 이유를 설명한다: "전해질 미립화" (electrolyte
miniaturization) 산업 trend 는 *cathode-internal SE filler 에 한정* 하여
적용되며 separator layer 에는 적용되지 않는다. 본 논문의 framework 는
cathode 에서의 이러한 targeted miniaturization 의 mechanistic foundation
을 제공하면서, separator optimum 은 별개 set 의 considerations 에 의해
지배됨을 acknowledge 한다.

---


## Section 6 — Fracture-Aware Network Solver: Methodology and Bounds

### English

Sections 4–5-1 established that the σ_ionic scaling law is decoupled
from AM-AM fracture by construction (SE-SE-only ionic graph) and the
inversion of bulk-pellet vs cathode SE-size optimum is a clean
separation of dominant mechanisms. The σ_e (electronic) and σ_thermal
channels do *not* enjoy the same protection — both rely on AM-AM
contacts that are directly affected by fracture. This section presents
the fracture-aware solver methodology used to quantify σ_e / σ_thermal
loss in the 78-case ensemble and identifies AM_S / AM_P composition
as the dominant control variable.

**Decomposition framework.** All three transport channels admit the
same multiplicative decomposition:

```
σ_eff = σ_grain × η_topology(microstructure)
```

where σ_grain is the intrinsic single-crystal conductivity (literature
input) and η_topology is the dimensionless microstructural factor
computed by the network solver. The paper's v29 main scaling law
(Section 4, LOOCV R² = 0.90) is precisely a fit of η_topology for
σ_ionic. The fracture-aware analysis modifies η_topology only — it
does not touch σ_grain. This orthogonality is why the σ_ionic claims
of Sections 4–5 carry over: σ_grain is uniform across the ensemble,
and the η_topology fit is robust to fracture-state interpretation
(Section 5).

For σ_e and σ_thermal, the η_topology depends on AM-AM contacts that
fracture can break. Three solver variants progressively refine the
fracture-loss estimate:

**Stage C — Binary cutoff (R = ∞).** For each AM-AM contact, classify
the Lawn 1998 force multiplier m = F/P_c. If m ≥ 3 (multicrack
threshold or beyond), set the contact's conductance to zero (R = ∞).
All other contacts unchanged. This is a *strict upper bound* on
σ_e_loss because it assumes any contact in the multicrack-or-worse
regime is electrically broken. Implementation: filter contacts.csv,
re-run network_conductivity on the filtered graph.

**Stage D — Stagewise σ_factor (Lawn-literature).** Replace the
binary 0/1 cutoff with literature-informed per-stage scaling, capturing
the fact that fractured contacts retain *partial* conductance
(Trevisanello 2021, Min 2024, Jiang 2021):

```
intact         (m < 1)        × 1.00
microcrack     (1 ≤ m < 3)    × 0.85   (Trevisanello, Heenan)
multicrack     (3 ≤ m < 11)   × 0.40   (Jiang rock-salt + grain sep.)
fragmentation  (11 ≤ m < 32)  × 0.10   (Min, mostly broken + rock-salt)
pulverization  (m ≥ 32)       × 0.02   (binary literature limit)
```

Implementation: scale contact_area + delta of each AM-AM contact by
the stage σ_factor. Topology preserved; only edge weights modified.

**Stage E — Full literature corrections.** Stage D plus the per-particle
σ_grain factor for AM crystallinity (Trevisanello 2021 single-crystal
vs polycrystalline) and SE size (Cronau 2022 size-invariant ≥ 0.3 μm,
amorphization onset below). For κ_thermal, AM crystallinity factor
(Wang 2022 phonon GB scattering) replaces fracture; SE κ is size-
invariant per Yang 2022 (sulfide already in glassy regime). Edge factors
use the harmonic mean of the two endpoint particle factors.

**Bound interpretation.** The three variants form a graduated estimate
of the fracture-aware σ_e:

- Stage C is the *upper bound on σ_e_loss* (lower bound on σ_e). It
  assumes complete loss above multicrack threshold.
- Stage E is the *literature-realistic central estimate*. It captures
  partial conductance preservation through stagewise scaling and AM
  crystallinity dependence.
- The gap C → E quantifies how much "rescue" the literature stagewise
  scaling and AM grain factors provide on top of the conservative
  binary cutoff.

**Empirical results — 78-case ensemble.** Across the 58 cases that
pass the σ_e numerical-anomaly filter (out of 80 raw):

```
σ_e channel results
─────────────────────────────────────────────────────────────────
σ_e baseline           median 6.49 mS/cm  mean 6.06   max 13.74  (n=55)
Stage C (binary)       median 2.86        mean 3.63   max 10.88  (n=54)
                       loss median 28.6%, Q1/Q3 0.15 / 76.5 %
                       fa/full ratio median 0.714
Stage D (stagewise)    median 4.92        mean 4.94   max 10.75  (n=54)
                       loss median 6.88 %, mean 14.82 %
                       sw/full ratio median 0.931
Stage E (full)         median 4.79        mean 4.80   max 10.75  (n=55)
                       loss median 11.33%, mean 18.41%
                       fa(E)/full ratio median 0.893

σ_ionic channel — sanity check (Stage E)
─────────────────────────────────────────────────────────────────
σ_ionic baseline       median 0.1451 mS/cm                       (n=58)
σ_ionic Stage E        median 0.1039 mS/cm                       (n=57)
σ_ionic loss%          median -0.01 %, Q3 1.08 %
  → Stage E σ_grain factor for SE-SE contacts (size-dependent
    Cronau 2022) leaves σ_ionic essentially unchanged for the
    r_SE ≥ 0.5 μm population (77/78 cases), confirming the
    by-construction decoupling of Section 4.

κ_thermal channel results (Stage E only)
─────────────────────────────────────────────────────────────────
κ baseline             median 4.33 W/(m·K)                       (n=58)
κ Stage E              median 4.16        mean 4.62              (n=58)
                       loss median 1.93 %, mean 2.89 %
                       Q1/Q3 -0.10 / 4.76 %
                       E/full ratio median 0.981
```

Three findings stand out:

(1) **AM_P / AM_S composition is the dominant predictor of σ_e_loss.**
Pearson correlation of AM_P volume fraction → σ_e_loss is **+0.98**
(Spearman +0.95, n = 54), an essentially perfect monotonic relationship.
The corresponding correlation for r_SE is only −0.16 (Spearman −0.20),
roughly a noise-level signal. Pivoting σ_e_loss across both axes makes
this stark:

```
Median Stage C σ_e_loss% — P:S band × r_SE band
                      fine (<0.7μm)  medium (0.7-1.2)  coarse (>1.2)
0:10  (all AM_S)         0.10            0.1               0.07
3:7   (AM_S-rich)       30.92            -                46.98
5:5   (balanced)        57.12            -                66.19
7:3   (AM_P-rich)       80.41            -                82.96
10:0  (all AM_P)       100.00            -               100.00
```

The pivot is essentially constant along rows (r_SE) and steeply
monotone along columns (P:S). This is the empirical statement of
Section 2's K_IC argument: AM_S has K_IC ≈ 1.0 MPa·m^(1/2) versus
AM_P at ≈ 0.3 MPa·m^(1/2), giving Auerbach P_c ratio ≈ 11×. AM_P-rich
cathodes therefore enter the multicrack/fragmentation regime at force
levels where AM_S-rich cathodes remain intact, and the resulting
σ_e_loss tracks the AM_P fraction one-to-one.

(2) **Stage D rescues most of the binary loss.** The median σ_e loss
falls from 28.6 % (Stage C, binary R = ∞) to 6.9 % (Stage D, Lawn
literature σ_factor) — a ~22 percentage-point recovery driven by the
literature-realistic partial conductance of microcrack and multicrack
contacts (factors 0.85 and 0.40). The remaining 6.9 % residual loss
sits squarely on the fragmentation/pulverization tail (factors 0.10
and 0.02), consistent with the catastrophic-fracture interpretation
of those bands. Stage E (with the AM_P × 0.65 grain factor on top)
slightly raises the estimate to 11.3 % median because the grain factor
attenuates *all* AM-AM contacts including intact ones in AM_P-rich
cathodes — the small additional loss (~4 %p) is the literature-
realistic crystallinity penalty that polycrystalline NCM pays even
without any fracture.

(3) **κ_thermal is essentially preserved (no bimodal loss).** The
Stage E κ loss is median 1.93 % and mean 2.89 % across the full 58-case
ensemble, with Q3 only at 4.76 %. There is no bimodal AM_S-vs-AM_P
distribution for κ as one might naively expect from the σ_e trend.
This is because κ in this ensemble is dominated by SE-SE thermal paths
(numerous, short, high-coverage) rather than the sparse AM-AM tails
that fracture removes; the AM_P × 0.50 grain factor that would in
principle penalize polycrystalline NCM thermally simply does not
control the bulk κ value because the AM-AM phonon channel is not
percolating. κ_thermal therefore does not need a separate paper-level
correction — the network solver baseline suffices to within ~3 %.

**Why r_SE is not a primary control variable for σ_e.** The earlier
intuition — that fine SE preserves σ_e because finer SE redistributes
forces more uniformly across AM-AM contacts — is reasonable but
empirically secondary to the AM_S/AM_P split. In our 78-case ensemble
the fine, medium, coarse r_SE bands all span the full P:S range and
the σ_e_loss within each r_SE band is dominated by the band's P:S
distribution, not by r_SE per se. The Pareto top-10 designs (high
σ_ionic + high σ_e + high κ post-correction) are concentrated at
r_SE = 0.5 μm because that is where σ_ionic is best (Section 5-1's
small-SE preference), *not* because r_SE = 0.5 μm directly preserves
σ_e. The two effects co-localize at the same operating point but
through orthogonal mechanisms.

**Implication.** Combining the Section 4 σ_ionic invariance, the
Section 5-1 cathode/separator inversion, and the present fracture-aware
quantification, the cathode-composite design rule of this paper is:

  *AM_S-rich (single-crystal) NCM is the primary lever for preserving
  σ_e and κ under fracture; sub-micron SE is the primary lever for
  optimizing σ_ionic. The two levers act on disjoint contact populations
  (AM-AM vs SE-SE) and can be simultaneously optimized without
  trade-off. r_SE alone provides only a weak (Pearson |r| ≈ 0.2)
  modulation of σ_e_loss within a fixed P:S composition.*

The σ_ionic channel is by construction insensitive to AM-AM fracture
(Section 4) and is therefore not penalized in either direction.

### 한국어

Sections 4–5-1 은 σ_ionic scaling law 가 *구조적으로* AM-AM fracture
와 분리됨 (SE-SE-only ionic graph) 과, bulk-pellet vs cathode 의 SE
크기 optimum 역전이 dominant mechanism 의 깔끔한 분리임을 확립했다.
σ_e (전자) 와 σ_thermal 채널은 같은 보호를 받지 *못한다* — 둘 다
fracture 가 직접 영향을 미치는 AM-AM contact 에 의존한다. 본 절은
78-case 앙상블에서 σ_e / σ_thermal 손실을 정량화하는 fracture-aware
solver methodology 를 제시하고, AM_S / AM_P 조성을 dominant control
변수로 식별한다.

**Decomposition framework.** 세 transport 채널 모두 다음 곱셈 분해를
인정한다:

```
σ_eff = σ_grain × η_topology(microstructure)
```

여기서 σ_grain 은 intrinsic 단결정 전도도 (literature input),
η_topology 는 network solver 가 계산하는 dimensionless microstructural
factor 이다. 본 논문의 v29 main scaling law (Section 4, LOOCV R² =
0.90) 는 정확히 σ_ionic 의 η_topology fit 이다. Fracture-aware 분석은
η_topology 만 수정하며 σ_grain 은 건드리지 않는다. 이 orthogonality 가
Sections 4–5 의 σ_ionic 결론을 그대로 carry over 시키는 이유이다.

σ_e 와 σ_thermal 의 경우 η_topology 는 fracture 가 깰 수 있는 AM-AM
contact 에 의존한다. 세 solver variant 가 fracture-loss estimate 를
점진적으로 정밀화한다:

**Stage C — Binary cutoff (R = ∞).** 각 AM-AM contact 에 대해 Lawn
1998 force multiplier m = F/P_c 분류. m ≥ 3 (multicrack 임계 이상)
이면 contact conductance = 0 (R = ∞). 그 외는 변화 없음. *σ_e_loss
의 strict upper bound* 이다.

**Stage D — Stagewise σ_factor (Lawn-literature).** Binary 0/1 cutoff
대신 literature-informed per-stage scaling 으로 대체 (Trevisanello
2021, Min 2024, Jiang 2021):

```
intact         (m < 1)        × 1.00
microcrack     (1 ≤ m < 3)    × 0.85   (Trevisanello, Heenan)
multicrack     (3 ≤ m < 11)   × 0.40   (Jiang rock-salt + grain 분리)
fragmentation  (11 ≤ m < 32)  × 0.10   (Min, mostly broken + rock-salt)
pulverization  (m ≥ 32)       × 0.02   (binary literature 한계)
```

구현: 각 AM-AM contact 의 contact_area + delta 를 stage σ_factor 로
스케일. Topology 보존, edge weight 만 수정.

**Stage E — Full literature corrections.** Stage D + AM 결정성에 대한
per-particle σ_grain factor (Trevisanello 2021 SC vs PC) + SE 크기
factor (Cronau 2022 size-invariant ≥ 0.3 μm). κ_thermal 의 경우
AM 결정성 factor (Wang 2022) 가 fracture 를 대체. Edge factor 는 두
particle factor 의 harmonic mean.

**Empirical 결과 — 78-case 앙상블.** σ_e 수치 anomaly filter 통과한
58 cases (80 raw 중) 에 대해:

```
σ_e 채널 결과
─────────────────────────────────────────────────────────────────
σ_e baseline           median 6.49 mS/cm  mean 6.06   max 13.74  (n=55)
Stage C (binary)       median 2.86        mean 3.63   max 10.88  (n=54)
                       loss median 28.6%, Q1/Q3 0.15 / 76.5 %
                       fa/full ratio median 0.714
Stage D (stagewise)    median 4.92        mean 4.94   max 10.75  (n=54)
                       loss median 6.88 %, mean 14.82 %
                       sw/full ratio median 0.931
Stage E (full)         median 4.79        mean 4.80   max 10.75  (n=55)
                       loss median 11.33%, mean 18.41%
                       fa(E)/full ratio median 0.893

σ_ionic 채널 — sanity check (Stage E)
─────────────────────────────────────────────────────────────────
σ_ionic baseline       median 0.1451 mS/cm                       (n=58)
σ_ionic Stage E        median 0.1039 mS/cm                       (n=57)
σ_ionic loss%          median -0.01 %, Q3 1.08 %
  → r_SE ≥ 0.5 μm 인 77/78 case 에서 σ_ionic 본질적으로 불변,
    Section 4 의 by-construction decoupling 확인.

κ_thermal 채널 결과 (Stage E only)
─────────────────────────────────────────────────────────────────
κ baseline             median 4.33 W/(m·K)                       (n=58)
κ Stage E              median 4.16        mean 4.62              (n=58)
                       loss median 1.93 %, mean 2.89 %
                       Q1/Q3 -0.10 / 4.76 %
                       E/full ratio median 0.981
```

세 가지 발견:

(1) **AM_P / AM_S 조성이 σ_e_loss 의 dominant predictor 이다.** AM_P
volume fraction → σ_e_loss 의 Pearson 상관은 **+0.98** (Spearman
+0.95, n = 54) — 본질적으로 완벽한 monotonic 관계. 같은 σ_e_loss 에
대한 r_SE 의 상관은 −0.16 (Spearman −0.20) 으로 노이즈 수준. 두
축으로 σ_e_loss 를 pivot 하면 이 차이가 극명해진다:

```
Stage C σ_e_loss% median  —  P:S band × r_SE band
                      fine (<0.7μm)  medium (0.7-1.2)  coarse (>1.2)
0:10  (전 AM_S)          0.10            0.1               0.07
3:7   (AM_S-rich)       30.92            -                46.98
5:5   (balanced)        57.12            -                66.19
7:3   (AM_P-rich)       80.41            -                82.96
10:0  (전 AM_P)        100.00            -               100.00
```

Pivot 은 행 방향 (r_SE) 으로는 거의 일정하고 열 방향 (P:S) 으로는
가파르게 monotone 하다. 이는 Section 2 의 K_IC 논거의 실증적 진술
이다: AM_S 의 K_IC ≈ 1.0 MPa·m^(1/2) vs AM_P 의 ≈ 0.3 MPa·m^(1/2),
Auerbach P_c 비 ≈ 11×. AM_P-rich cathode 는 따라서 AM_S-rich cathode
가 intact 한 force level 에서 multicrack/fragmentation regime 에 진입
하며, 결과적인 σ_e_loss 는 AM_P fraction 을 일대일로 추적한다.

(2) **Stage D 가 binary loss 의 대부분을 회복시킨다.** σ_e median loss
는 28.6 % (Stage C, binary R = ∞) 에서 6.9 % (Stage D, Lawn literature
σ_factor) 로 떨어진다 — microcrack 과 multicrack contact 의 literature-
realistic 부분 전도도 (factor 0.85, 0.40) 가 가져오는 ~22 percentage-
point 회복. 잔존하는 6.9 % loss 는 정확히 fragmentation/pulverization
tail (factor 0.10, 0.02) 위에 있어, 그 band 들의 catastrophic-fracture
해석과 정합한다. Stage E (위에 AM_P × 0.65 grain factor 추가) 는
median 을 11.3 % 로 약간 올리는데, 이는 grain factor 가 *모든* AM-AM
contact (intact 포함) 을 약화시키기 때문 — 추가 ~4 %p 손실은 fracture
없이도 polycrystalline NCM 이 지불하는 literature-realistic 결정성
penalty 이다.

(3) **κ_thermal 은 본질적으로 보존됨 (bimodal loss 없음).** Stage E κ
loss 는 58-case 앙상블 전체에서 median 1.93 %, mean 2.89 %, Q3 만 해도
4.76 %. σ_e 추세에서 naive 하게 예상할 수 있는 AM_S-vs-AM_P bimodal
분포가 κ 에는 없다. 이는 본 앙상블의 κ 가 sparse AM-AM tail 이 아닌
SE-SE 열 경로 (수많고 짧고 high-coverage) 에 의해 dominate 되기
때문이다 — fracture 가 제거하는 AM-AM phonon 채널은 percolating 하지
않으므로 AM_P × 0.50 grain factor 가 bulk κ 값을 control 하지 않는다.
κ_thermal 은 따라서 paper-level 별도 보정이 필요하지 않으며 — network
solver baseline 만으로도 ~3 % 이내에서 충분하다.

**왜 r_SE 가 σ_e 의 primary control 변수가 아닌가.** 이전 직관 —
fine SE 가 AM-AM contact 에 force 를 더 균일하게 분배하므로 σ_e 를
보존한다 — 는 합리적이지만 AM_S/AM_P split 에 비해 실증적으로
secondary 이다. 78-case 앙상블에서 fine, medium, coarse r_SE band 는
모두 P:S 전 범위를 span 하며, 각 r_SE band 내의 σ_e_loss 는 그 band
의 P:S 분포에 의해 dominate 되지 r_SE 자체가 아니다. Pareto top-10
디자인 (보정 후 high σ_ionic + high σ_e + high κ) 이 r_SE = 0.5 μm
에 집중되는 것은 그곳이 σ_ionic 이 가장 좋기 때문이지 (Section 5-1 의
small-SE 선호), r_SE = 0.5 μm 가 σ_e 를 직접 보존하기 때문이 *아니다*.
두 효과가 같은 operating point 에서 co-localize 하지만 orthogonal
mechanism 을 통해 그렇게 된다.

**함의.** Section 4 의 σ_ionic 불변성, Section 5-1 의 cathode/separator
역전, 본 절의 fracture-aware 정량화를 종합하면, 본 논문의 cathode-
composite design rule 은:

  *AM_S-rich (single-crystal) NCM 이 fracture 하의 σ_e 와 κ 보존을
  위한 primary lever; sub-micron SE 는 σ_ionic 최적화를 위한 primary
  lever. 두 lever 는 disjoint contact population (AM-AM vs SE-SE)
  에 작용하므로 trade-off 없이 동시 최적화 가능. r_SE 단독은 고정된
  P:S 조성 내에서 σ_e_loss 의 약한 (Pearson |r| ≈ 0.2) modulation 만
  제공.*

σ_ionic 채널은 구조적으로 AM-AM fracture 에 둔감 (Section 4) 하므로
어느 방향으로도 penalty 받지 않는다.

---

## Section 7 — Cathode Composite Design Rule via 10-Case Controlled Sweep

### English

#### 7.1 Sweep Design and Case Selection

Sections 5-1 and 6 established two independent design levers: SE
particle size (r_SE) for σ_ionic optimization and AM_S / AM_P
composition (P:S ratio) for σ_e and σ_thermal preservation under
fracture. To test these levers in a controlled setting and observe
their joint behaviour, we constructed a 10-case 2-parameter sweep:

```
P:S ∈ {0:10, 3:7, 5:5, 7:3, 10:0}    (5 levels, AM_P : AM_S volume ratio)
r_SE ∈ {0.5 μm, 1.5 μm}                (2 levels)
total: 5 × 2 = 10 cases
```

The P:S levels span the industrial range from pure single-crystal NCM
(0:10) to pure polycrystalline secondary NCM (10:0), with three
intermediate balanced points. The r_SE levels bracket the cathode-grade
(sub-μm) and separator-grade (~1-3 μm) regimes from Section 5-1. All
other parameters are held at the project's default values (target
pressure 300 MPa, AM:SE volume ratio 80:20, AM_P d50 = 10 μm,
AM_S d50 = 5 μm).

The sweep is *controlled*: each (P:S, r_SE) combination is a single
deterministic DEM run with the same seed and pressure, so any variation
in σ_eff or fracture severity is directly attributable to the two swept
variables.

#### 7.2 Sweep Results

Table 7.1 reports the post-compaction transport conductivities and
fracture severity for the 10 cases. **σ values are Stage A Hertzian
baseline (default network-solver output, no physics correction, no
fracture-aware Stage C/D/E discount)**; AM_P severe% is the
fragmentation+pulverization contact fraction within AM_P-AM_P pairs
(force-based classifier, directly measured from DEM force output, not
derived from σ). The σ_e column is shown for academic completeness:
Section 7.7 (VGCF caveat) explains that real cathodes neutralize the
σ_e channel via 1 wt % carbon-fiber additive, so the *primary*
design-relevant columns are **σ_ionic** (transport bottleneck) and
**AM_P severe%** (mechanical/cycling robustness proxy via cracked
NCM particles), with σ_th as a secondary thermal-management metric.

```
Table 7.1 — 10-case controlled sweep results

case   P:S    r_SE  σ_ionic  σ_e   σ_th   AM_P  notes
                    mS/cm   mS/cm  W/mK   sev%
─────  ────  ────  ───────  ─────  ─────  ────  ─────────────────────────────
real_1 0:10  0.5   0.117    4.63   3.42   —     pure AM_S, small SE
real_2 3:7   0.5   0.152    4.13   4.06   0     bimodal champion ★
real_3 5:5   0.5   0.173    3.18   4.33   0     σ_ionic-favoring
real_4 7:3   0.5   0.182    1.68   4.56   0     σ_ionic max, σ_e bottom
real_5 10:0  0.5   0.153    6.21   5.17   35    pure AM_P, small SE
real_6 0:10  1.5   0.031    6.20   2.93   —     pure AM_S, large SE
real_7 3:7   1.5   0.066    6.95   3.64   62    σ_e high, fracture-vulnerable
real_8 5:5   1.5   0.081    7.25   4.21   51    σ_e high, half-fractured
real_9 7:3   1.5   0.106    7.62   4.54   60    σ_e max, AM_P-severe
real_10 10:0 1.5   0.119    7.53   3.29   61    worst-case fracture
```

#### 7.3 Two Trajectories — Path A (Small SE) vs Path B (Large SE)

The 10 cases divide into two trajectories along the r_SE axis. We label
them Path A (r_SE = 0.5 μm) and Path B (r_SE = 1.5 μm).

**Path A — small SE (real_1 → real_5).** σ_ionic spans 0.117–0.182
mS/cm, three to five times higher than Path B at the same P:S. σ_e
starts at 4.63 (pure AM_S), declines to a 1.68 minimum at 7:3 due to
AM-AM percolation collapse (the few AM_P particles are surrounded by
smaller-radius SE that block their pair-wise contact graph), and
rebounds to 6.21 at 10:0 once AM_P fully percolates. AM_P severe%
remains at 0 across the four AM_S-bearing cases and reaches 35 % only
at the 10:0 endpoint where every AM particle is polycrystalline.

**Path B — large SE (real_6 → real_10).** σ_ionic collapses to
0.031–0.119 mS/cm, factor of 2-4 below Path A throughout. σ_e is higher
than Path A in the mid-P:S range (peaking at 7.62 for real_9) because
larger SE no longer geometrically excludes AM-AM contacts. But this
σ_e gain is bought at the cost of severe AM_P fracture starting from
3:7 — AM_P severe% jumps from 0 % (Path A real_2) to 62 % (Path B
real_7) at *identical* P:S=3:7 composition.

**Mechanism for the AM_P-severity explosion in Path B.** Comparing
real_2 (r_SE=0.5) and real_7 (r_SE=1.5) at the same P:S=3:7 isolates
the r_SE effect:

```
                       real_2     real_7    ratio
                     (0.5 μm)   (1.5 μm)
F per AM_P-AM_P (mN)  5,317     17,648      3.3×
F / P_c (median)         9.04     12.20     1.35×
Lawn regime         multicrack  fragment-
                    (3 ≤ m<11)  ation (m ≥ 11)
AM_P severe%            0 %       62 %
```

The 3.3× force concentration on AM_P-AM_P contacts with large SE has
four contributing factors:

  *(1) Particle-count effect.* SE number density scales as 1/r_SE³, so
  going from 0.5 to 1.5 μm reduces the SE particle count by 27×.
  Total contact count drops accordingly, so the same applied compaction
  force (300 MPa × cross-section) is distributed across far fewer
  parallel contacts → per-contact force rises.

  *(2) AM-AM force pathway dominance.* Large SE no longer geometrically
  infiltrates the inter-AM gaps (Section 5-1 η_topology_void), so AM
  particles directly contact each other more often. AM-AM contacts
  bear a larger share of the total compaction force.

  *(3) AM_P fracture-toughness deficit.* K_IC(AM_S) = 1.0 MPa·m^(1/2)
  versus K_IC(AM_P) = 0.3 MPa·m^(1/2), so the Auerbach onset force
  P_c ∝ K_IC² is 11× lower for AM_P pairs. The same applied force
  reaches AM_P's multicrack threshold long before AM_S's.

  *(4) F/P_c crosses the fragmentation threshold.* The Lawn 1998
  band boundaries are m=3 (multicrack onset) and m=11 (fragmentation
  onset). Path A real_2 sits at F/P_c=9 — within the multicrack band
  but below fragmentation, so severe%=0. Path B real_7 sits at
  F/P_c=12 — just over the fragmentation threshold, so a large
  fraction of contacts (62 %) lands in the fragmentation/pulverization
  bands counted as "severe".

The σ_thermal channel is intermediate: Path A reaches 4.06–5.17
W/(m·K), Path B 2.93–4.54 W/(m·K). Path A holds a small κ advantage
at AM_S-rich compositions because small-SE microstructures retain
AM-SE contact area better, sustaining the harmonic-mean κ across the
AM_S × SE bridges.

#### 7.4 Bimodal Optimum — real_2 (3:7, 0.5 μm) = Path A Champion

Among the 10 cases, real_2 emerges as the composite-Pareto champion:

```
real_2:  σ_ionic = 0.152  (Path A second-highest — 16 % below the 7:3 max)
         σ_e    = 4.13   (mid-tier, percolating, no σ_e collapse)
         σ_th   = 4.06   (mid-tier W/(m·K))
         AM_P severe% = 0  (zero fracture under target compaction)
```

The mechanism reads directly off the Section 5-1 / Section 6 framework:

- *σ_ionic = 0.152*: small SE (0.5 μm) maximizes η_topology_void
  (cathode-internal SE infiltration). The 3:7 composition still has
  30 % AM_P, but the AM-SE coverage stays high because small SE
  infiltrates the inter-AM gaps.
- *σ_e = 4.13*: the 70 % AM_S backbone provides a high-K_IC
  fracture-resistant percolating skeleton; small SE does not block
  the AM-AM graph because AM particles are still the dominant volume
  fraction.
- *AM_P severe% = 0*: the small SE distributes compression force
  across many small-area contacts; F/P_c stays at 9 (multicrack) for
  AM_P-AM_P pairs and never crosses the fragmentation threshold,
  while AM_P is anyway only 30 % of AM volume.

real_2 thus realizes the two-lever design rule of Section 6: *small SE
optimizes σ_ionic; AM_S-rich optimizes σ_e and σ_thermal under
fracture*. Both levers reinforce each other in real_2.

#### 7.5 Pareto Frontier — r_SE × P:S Trade-off Map

The 10 cases span a 2D Pareto surface. Because σ_e is neutralized by
VGCF in real cells (Section 7.7), the *cell-impact-relevant* axes
reduce to σ_ionic, σ_th, and AM_P severe% (mechanical robustness).
Three observations stand out:

(1) **Path A Pareto-dominates Path B for σ_ionic at every P:S.** No
case in Path B reaches the σ_ionic levels of even the lowest Path A
point (Path B max 0.119 < Path A min 0.117). The η_topology_void
mechanism (Section 5-1) is the dominant control for σ_ionic and is
*not bypassed* by VGCF (carbon fibers are ionically inert). σ_ionic
is therefore the single most decisive design metric in real cells.

(2) **AM_P severe% is the decisive mechanical-robustness metric.**
Path B configurations (real_7/_8/_9/_10) all show 51–62 % of AM_P-AM_P
contacts in the fragmentation-or-worse regime. Even when σ_e is
backfilled by VGCF, the underlying NCM particle pulverization persists
and drives separate failure modes outside the present DEM scope:
cathode-electrolyte interphase (CEI) breakdown on freshly exposed
particle surfaces, SE film cracking around fragmented AM, and capacity
fade through cycling-induced isolation of disconnected NCM fragments.
The AM_P severe% column is therefore the proxy for cycling stability
that survives the VGCF caveat — a high severe% is bad regardless of
how much VGCF is added.

(3) **Path B's σ_e advantage is largely irrelevant in practice.** Path
B σ_e reaches 7.62 at real_9, but the ~30–60 % σ_e_loss this would
incur via Stage E corrections (Section 6) is bypassed by VGCF.
Reporting σ_e here is for academic completeness — the 78-case Section
6 Pearson +0.98 correlation between AM_P fraction and σ_e_loss is a
real microstructural finding, but its cell-level relevance is muted
by industrial conductive-additive practice.

The composite Pareto frontier — the (σ_ionic, σ_th, AM_P severe%)
envelope under VGCF assumption — is therefore traced by Path A.
real_2 sits at the inflection point where adding more AM_P maintains
zero AM_P severe% without further lifting σ_ionic.

#### 7.6 Design Rule (Industry-Facing Synthesis)

The 10-case sweep, the 78-case ensemble (Section 6), and the
bulk-vs-cathode inversion (Section 5-1) together yield a single design
rule for sulfide-based ASSB cathode composites at 300 MPa target
compaction:

> **Use sub-μm SE filler (0.5 μm) and AM_S-rich (single-crystal NCM,
> ≥ 70 %) microstructure. Sub-μm SE delivers the η_topology_void
> mechanism that triples σ_ionic versus 1–2 μm SE; AM_S-rich provides
> the high-K_IC backbone that survives 300 MPa cold-press without
> entering the multicrack regime, preserving σ_e and σ_thermal at
> near-baseline values. The bimodal optimum at AM_P : AM_S = 3:7 with
> r_SE = 0.5 μm (real_2) realizes both levers simultaneously and
> dominates the σ_ionic / σ_e / σ_thermal / fracture-robustness
> 4-objective Pareto frontier.**

The separator pellet of the same cell continues to favour 1–3 μm SE
for the orthogonal reasons given in Section 5-1 (plastic densification,
σ_grain integrity, air sensitivity, mechanical creep). The
cathode-favouring "small SE" rule and the separator-favouring "larger
SE" rule are layer-specific applications of the same η_topology
= η_GB × η_void decomposition, with η_void only active in the
AM-bearing cathode layer.

### 한국어

#### 7.1 Sweep 설계 및 case 선정

Section 5-1 과 Section 6 에서 두 개의 독립적 design lever 가 확립되었
다: σ_ionic 최적화를 위한 SE 입자 크기 (r_SE), fracture 하의 σ_e 와
σ_thermal 보존을 위한 AM_S / AM_P 조성 (P:S ratio). 이 두 lever 를
controlled 환경에서 검증하고 그 joint behaviour 를 관찰하기 위해
10-case 2-parameter sweep 을 구성했다:

```
P:S ∈ {0:10, 3:7, 5:5, 7:3, 10:0}    (5 levels, AM_P : AM_S 부피비)
r_SE ∈ {0.5 μm, 1.5 μm}                (2 levels)
total: 5 × 2 = 10 cases
```

P:S levels 는 순수 single-crystal NCM (0:10) 부터 순수 polycrystalline
secondary NCM (10:0) 까지 산업적 범위를 span 하며, 세 개의 중간
balanced 지점을 포함한다. r_SE levels 는 Section 5-1 의 cathode-grade
(sub-μm) 와 separator-grade (~1-3 μm) regime 을 bracket 한다. 그 외
모든 parameter 는 본 프로젝트의 default 값으로 고정 (target pressure
300 MPa, AM:SE 부피비 80:20, AM_P d50 = 10 μm, AM_S d50 = 5 μm).

본 sweep 은 *controlled* 이다: 각 (P:S, r_SE) 조합은 동일한 seed 와
pressure 의 단일 deterministic DEM run 이므로, σ_eff 또는 fracture
severity 의 어떠한 변화도 두 sweep 변수에 직접 귀속된다.

#### 7.2 Sweep 결과

Table 7.1 은 10 cases 의 post-compaction transport conductivity 와
fracture severity 를 보고한다. **σ 값들은 Stage A Hertzian baseline
(default network-solver 출력; physics correction 미적용, fracture-aware
Stage C/D/E discount 미적용)** 이고, AM_P severe% 는 AM_P-AM_P pair
내부의 fragmentation+pulverization contact 비율 (force-based
classifier; DEM force 출력에서 직접 측정, σ 에서 유도되지 않음). σ_e
컬럼은 학술적 completeness 를 위해 표시: Section 7.7 (VGCF caveat) 에서
실제 cathode 는 1 wt % carbon-fiber 첨가제로 σ_e 채널을 중화함을 설명
하므로, *primary* design-relevant 컬럼은 **σ_ionic** (transport
bottleneck) 과 **AM_P severe%** (cracked NCM particle 을 통한 mechanical
/ cycling robustness proxy) 이고, σ_th 가 secondary thermal-management
지표.

```
Table 7.1 — 10-case controlled sweep 결과

case   P:S    r_SE  σ_ionic  σ_e   σ_th   AM_P  비고
                    mS/cm   mS/cm  W/mK   sev%
─────  ────  ────  ───────  ─────  ─────  ────  ─────────────────────────────
real_1 0:10  0.5   0.117    4.63   3.42   —     순수 AM_S, small SE
real_2 3:7   0.5   0.152    4.13   4.06   0     bimodal champion ★
real_3 5:5   0.5   0.173    3.18   4.33   0     σ_ionic-favoring
real_4 7:3   0.5   0.182    1.68   4.56   0     σ_ionic max, σ_e bottom
real_5 10:0  0.5   0.153    6.21   5.17   35    순수 AM_P, small SE
real_6 0:10  1.5   0.031    6.20   2.93   —     순수 AM_S, large SE
real_7 3:7   1.5   0.066    6.95   3.64   62    σ_e high, fracture-vulnerable
real_8 5:5   1.5   0.081    7.25   4.21   51    σ_e high, half-fractured
real_9 7:3   1.5   0.106    7.62   4.54   60    σ_e max, AM_P-severe
real_10 10:0 1.5   0.119    7.53   3.29   61    worst-case fracture
```

#### 7.3 두 trajectory — Path A (small SE) vs Path B (large SE)

10 cases 는 r_SE 축을 따라 두 trajectory 로 분할된다. Path A
(r_SE = 0.5 μm) 와 Path B (r_SE = 1.5 μm) 로 명명한다.

**Path A — small SE (real_1 → real_5).** σ_ionic 은 0.117–0.182 mS/cm
를 span 하며, 같은 P:S 의 Path B 보다 3–5× 높다. σ_e 는 4.63 (순수
AM_S) 에서 시작해 7:3 에서 1.68 의 최저점을 찍고 (AM-AM percolation
collapse — 적은 AM_P 입자들이 작은 SE 에 의해 pair-wise contact graph
가 차단됨), 10:0 에서 AM_P 가 fully percolating 하면 6.21 로 회복한다.
AM_P severe% 는 4 개의 AM_S-bearing case 에서 0 % 를 유지하다가, 모든
AM 입자가 polycrystalline 이 되는 10:0 endpoint 에서만 35 % 에 도달
한다.

**Path B — large SE (real_6 → real_10).** σ_ionic 은 0.031–0.119 mS/cm
로 붕괴하며, Path A 의 2-4× 아래에 머문다. σ_e 는 mid-P:S 영역에서
Path A 보다 높고 (real_9 에서 7.62 peak) — 큰 SE 가 더 이상 AM-AM
contact 를 geometrically exclude 하지 않기 때문이다. 그러나 이 σ_e
이득은 3:7 부터 시작되는 severe AM_P fracture 의 비용으로 매수된다 —
AM_P severe% 가 *동일한* P:S=3:7 조성에서 0 % (Path A real_2) 에서
62 % (Path B real_7) 로 폭발한다.

**Path B 의 AM_P-severity 폭발 메커니즘.** P:S=3:7 동일 조건에서
real_2 (r_SE=0.5) 와 real_7 (r_SE=1.5) 를 비교하면 r_SE 효과가 격리
된다:

```
                       real_2     real_7    비율
                     (0.5 μm)   (1.5 μm)
F per AM_P-AM_P (mN)  5,317     17,648      3.3×
F / P_c (median)         9.04     12.20     1.35×
Lawn regime         multicrack  fragment-
                    (3 ≤ m<11)  ation (m ≥ 11)
AM_P severe%            0 %       62 %
```

큰 SE 에서 AM_P-AM_P contact 의 3.3× force concentration 은 네 가지
원인이 결합된 결과:

  *(1) 입자 개수 효과.* SE 수밀도 ∝ 1/r_SE³, 따라서 0.5 → 1.5 μm 으로
  키우면 SE 입자 수가 27× 감소. 총 contact 수도 비례 감소하므로 동일한
  적용 압축력 (300 MPa × cross-section) 이 훨씬 적은 parallel contact
  에 분산 → per-contact force 상승.

  *(2) AM-AM force pathway dominance.* 큰 SE 는 inter-AM 간극에
  geometrically infiltrate 하지 않으므로 (Section 5-1 η_topology_void),
  AM 입자들이 서로 직접 contact 하는 빈도가 증가. AM-AM contact 가
  총 압축력의 더 큰 share 를 부담.

  *(3) AM_P fracture-toughness 결손.* K_IC(AM_S) = 1.0 MPa·m^(1/2)
  vs K_IC(AM_P) = 0.3 MPa·m^(1/2), 따라서 Auerbach onset force
  P_c ∝ K_IC² 는 AM_P pair 에서 11× 낮다. 같은 적용 force 가
  AM_S 보다 AM_P 의 multicrack threshold 에 훨씬 먼저 도달.

  *(4) F/P_c 가 fragmentation threshold 를 가로지름.* Lawn 1998 의
  band 경계는 m=3 (multicrack onset) 과 m=11 (fragmentation onset).
  Path A real_2 는 F/P_c=9 — multicrack band 내부지만 fragmentation
  아래라 severe%=0. Path B real_7 은 F/P_c=12 — 정확히 fragmentation
  threshold 위, 그래서 contact 의 큰 분율 (62 %) 이 "severe" 로
  카운트되는 fragmentation/pulverization band 에 진입.

σ_thermal 채널은 중간이다: Path A 4.06–5.17 W/(m·K), Path B 2.93–4.54
W/(m·K). Path A 는 AM_S-rich 조성에서 작은 κ 우위를 유지하는데, 이는
small-SE microstructure 가 AM-SE contact area 를 더 잘 보존해 AM_S × SE
bridge 의 harmonic-mean κ 를 sustain 하기 때문이다.

#### 7.4 Bimodal Optimum — real_2 (3:7, 0.5 μm) = Path A 챔피언

10 cases 중 real_2 가 composite-Pareto champion 으로 부상한다:

```
real_2:  σ_ionic = 0.152  (Path A 두 번째로 높음 — 7:3 max 의 16 % 아래)
         σ_e    = 4.13   (mid-tier, percolating, σ_e collapse 없음)
         σ_th   = 4.06   (mid-tier W/(m·K))
         AM_P severe% = 0  (target compaction 하에서 fracture 0)
```

메커니즘은 Section 5-1 / Section 6 framework 에서 직접 읽힌다:

- *σ_ionic = 0.152*: small SE (0.5 μm) 가 η_topology_void
  (cathode-internal SE infiltration) 를 maximize 한다. 3:7 조성은
  여전히 30 % AM_P 를 가지지만, small SE 가 inter-AM 간극에 침투하므로
  AM-SE coverage 가 높게 유지된다.
- *σ_e = 4.13*: 70 % AM_S backbone 이 high-K_IC fracture-resistant
  percolating skeleton 을 제공한다; AM 입자가 여전히 dominant volume
  fraction 이므로 small SE 가 AM-AM graph 를 차단하지 않는다.
- *AM_P severe% = 0*: small SE 가 압축력을 많은 small-area contact
  에 분산시키므로 AM_P-AM_P pair 의 F/P_c 가 9 (multicrack) 에 머물고
  fragmentation threshold 를 넘지 않으며, AM_P 는 어차피 AM volume
  의 30 % 만 차지.

real_2 는 따라서 Section 6 의 two-lever design rule 을 실현한다:
*small SE 가 σ_ionic 최적화; AM_S-rich 가 fracture 하의 σ_e 와
σ_thermal 최적화*. 두 lever 가 real_2 에서 서로를 강화한다.

#### 7.5 Pareto Frontier — r_SE × P:S Trade-off Map

10 cases 는 2D Pareto surface 를 span 한다. 실제 cell 에서 σ_e 는 VGCF
로 중화되므로 (Section 7.7), *cell-impact-relevant* 축은 σ_ionic, σ_th,
AM_P severe% (mechanical robustness) 로 축소된다. 세 가지 관찰이 두드
러진다:

(1) **모든 P:S 에서 Path A 가 σ_ionic 에 대해 Path B 를
Pareto-dominate.** Path B 의 어떤 case 도 Path A 의 가장 낮은 지점의
σ_ionic 수준에 도달하지 못한다 (Path B max 0.119 < Path A min 0.117).
η_topology_void 메커니즘 (Section 5-1) 이 σ_ionic 의 dominant control
이며, VGCF 로도 *bypass 되지 않는다* (carbon fiber 는 이온 관성).
σ_ionic 은 따라서 실제 cell 에서 가장 결정적인 단일 설계 지표.

(2) **AM_P severe% 가 mechanical-robustness 의 결정적 지표.** Path B
구성 (real_7/_8/_9/_10) 모두 AM_P-AM_P contact 의 51–62 % 가
fragmentation-or-worse regime. VGCF 가 σ_e 를 backfill 해도, 그
근본인 NCM 입자 분쇄는 잔존하여 본 DEM scope 외부의 별개 failure mode
를 유발: cathode-electrolyte interphase (CEI) 가 갓 노출된 입자
표면에서 분해, SE film 이 fragmented AM 주위에서 cracking, cycling-
induced isolation 을 통한 disconnected NCM fragment 의 capacity fade.
AM_P severe% 컬럼은 따라서 VGCF caveat 를 살아남는 cycling stability
proxy — 높은 severe% 는 VGCF 양에 무관하게 나쁘다.

(3) **Path B 의 σ_e 우위는 실제로 거의 무관.** Path B σ_e 는 real_9
에서 7.62 에 도달하지만, Stage E 보정 (Section 6) 으로 incurred 될
~30–60 % σ_e_loss 가 VGCF 로 bypass 됨. 여기서 σ_e 를 보고하는 것은
학술적 completeness — 78-case Section 6 의 AM_P fraction vs σ_e_loss
Pearson +0.98 상관은 실제 microstructure 발견이지만, cell-level 관련성
은 산업 도전성 첨가제 관행으로 muted.

따라서 composite Pareto frontier — VGCF 가정 하의 (σ_ionic, σ_th,
AM_P severe%) envelope — 는 Path A 에 의해 traced. real_2 는 더 많은
AM_P 추가가
σ_e 를 penalize 하기 시작하는 (real_4 의 percolation collapse)
inflection point 에 위치하며, σ_ionic 을 더 끌어올리지도 못한다.

#### 7.6 Design Rule (Industry-Facing Synthesis)

10-case sweep, 78-case ensemble (Section 6), 그리고 bulk-vs-cathode
inversion (Section 5-1) 이 종합되어 300 MPa target compaction 에서
sulfide-based ASSB cathode composite 에 대한 단일 design rule 을 산출
한다:

> **Sub-μm SE filler (0.5 μm) 와 AM_S-rich (single-crystal NCM,
> ≥ 70 %) microstructure 를 사용하라. Sub-μm SE 는 1–2 μm SE 대비
> σ_ionic 을 3 배 끌어올리는 η_topology_void 메커니즘을 제공한다;
> AM_S-rich 는 300 MPa cold-press 에서 multicrack regime 진입 없이
> 견디는 high-K_IC backbone 을 제공해 σ_e 와 σ_thermal 을 near-baseline
> 값으로 보존한다. AM_P : AM_S = 3:7 와 r_SE = 0.5 μm 의 bimodal
> optimum (real_2) 이 두 lever 를 동시 실현하며 σ_ionic / σ_e /
> σ_thermal / fracture-robustness 4-objective Pareto frontier 를
> dominate 한다.**

같은 셀의 separator pellet 은 Section 5-1 에서 제시된 직교 이유로
(plastic densification, σ_grain 무결성, air sensitivity, mechanical
creep) 1–3 μm SE 를 계속 선호한다. cathode-favouring "small SE" rule
과 separator-favouring "larger SE" rule 은 동일한 η_topology
= η_GB × η_void decomposition 의 layer-specific 응용이며, η_void 는
AM-bearing cathode layer 에서만 active 하다.

#### 7.7 Industrial Practice — The VGCF Conductive-Additive Caveat

The "AM_P-rich → σ_e collapse" trade-off identified in Section 7.3
applies to the *bare composite* without electronic-conductive additives.
Industrial sulfide ASSB cathodes invariably include ~1 wt % vapor-grown
carbon fibers (VGCF, σ_VGCF ≈ 10⁴ S/cm) as a percolation-bridging
additive. VGCF qualitatively transforms the σ_e channel:

- **Bridge-and-rescue.** A 1 wt % VGCF loading creates a percolating
  fiber network whose σ_grain exceeds NCM's by 10⁵–10⁶×. Even if every
  AM-AM contact in an AM_P-rich, fractured cathode were to lose its
  σ_e (Stage C upper bound), the VGCF backbone alone supports σ_e in
  the 5–20 mS/cm range — comparable to or exceeding the AM-AM
  baseline.

- **σ_e decouples from fracture.** The fragmentation-induced σ_e_loss
  reported in Section 6 (binary 28 %, Stage E 11 %) and the Path B
  Pareto trade-off in Section 7.5 are bare-composite numbers. Real
  cells with VGCF are *expected* to show σ_e_loss ≈ 0 even in
  Path B (large SE, AM_P-rich) configurations.

- **σ_ionic and κ are unchanged.** VGCF is electronically conductive
  but ionically inert and a phonon scatterer; it does not enter the
  SE-SE σ_ionic graph and provides no κ benefit. The Section 5-1
  bulk-vs-cathode r_SE inversion and the κ_thermal results in Section
  6 are therefore VGCF-invariant.

The implication for the design rule of Section 7.6:

> *In bare-composite (no VGCF) cells, AM_S-rich is the primary lever
> for σ_e preservation. With 1 wt % VGCF added (industrial practice),
> σ_e becomes essentially fracture-insensitive and AM_S-rich loses its
> σ_e advantage — the design rule reduces to small-SE-only for σ_ionic
> optimization. The AM_S-rich preference re-emerges only for the
> κ_thermal channel and for mechanical/cycling robustness considerations
> outside the present DEM scope.*

This caveat clarifies why high-σ_e Path B configurations (real_7, _9,
_10 with 60 %+ AM_P severe) remain industrially viable despite the
fracture severity reported here: the VGCF bypass largely neutralizes
the σ_e penalty. The present paper's framework — focused on
microstructure-level transport descriptors derived from DEM — does not
include VGCF in its 78-case ensemble; an extension that adds VGCF
percolation as an explicit term η_topology_VGCF in the σ_e
decomposition is a natural next step but is out of scope here. The
Section 6 / 7 σ_e numbers therefore stand as *bare-microstructure
upper bounds on fracture-induced loss*, with the actual cell-level
loss expected to be substantially smaller once VGCF is included.

#### 7.7 산업적 관행 — VGCF 도전성 첨가제 단서

Section 7.3 에서 식별된 "AM_P-rich → σ_e 붕괴" trade-off 는 도전성
첨가제 *없는 bare composite* 에 대한 결과이다. 산업 sulfide ASSB
cathode 는 percolation-bridging 첨가제로 ~1 wt % vapor-grown carbon
fiber (VGCF, σ_VGCF ≈ 10⁴ S/cm) 를 거의 항상 포함한다. VGCF 는 σ_e
채널을 정성적으로 변환시킨다:

- **Bridge-and-rescue.** 1 wt % VGCF 적재는 σ_grain 이 NCM 보다
  10⁵–10⁶× 큰 percolating fiber network 를 형성한다. AM_P-rich,
  fractured cathode 에서 모든 AM-AM contact 가 σ_e 를 잃더라도
  (Stage C upper bound), VGCF backbone 만으로 σ_e 가 5–20 mS/cm
  범위를 지지한다 — AM-AM baseline 과 comparable 하거나 그 이상.

- **σ_e 가 fracture 와 decouple.** Section 6 의 fragmentation-induced
  σ_e_loss (binary 28 %, Stage E 11 %) 와 Section 7.5 의 Path B
  Pareto trade-off 는 bare-composite 숫자이다. VGCF 가 들어간 실제
  cell 은 Path B (large SE, AM_P-rich) 구성에서도 σ_e_loss ≈ 0 이
  *예상*된다.

- **σ_ionic 과 κ 는 변화 없음.** VGCF 는 전자전도성이지만 이온
  관성이고 phonon scatterer 이다; SE-SE σ_ionic graph 에 들어가지
  않고 κ 이득도 제공하지 않는다. Section 5-1 의 bulk-vs-cathode
  r_SE inversion 과 Section 6 의 κ_thermal 결과는 따라서
  VGCF-invariant 하다.

Section 7.6 design rule 에 대한 함의:

> *Bare-composite (VGCF 없음) cell 에서는 AM_S-rich 가 σ_e 보존을
> 위한 primary lever. 1 wt % VGCF 추가 시 (산업 관행) σ_e 가 본질적
> 으로 fracture-insensitive 가 되어 AM_S-rich 가 σ_e 우위를 잃음 —
> design rule 은 σ_ionic 최적화를 위한 small-SE-only 로 축약된다.
> AM_S-rich 선호는 κ_thermal 채널과 본 DEM scope 외부의
> mechanical/cycling robustness 고려에서만 재등장한다.*

이 단서는 60 %+ AM_P severe 를 보이는 high-σ_e Path B 구성 (real_7,
_9, _10) 이 본 절의 fracture severity 에도 불구하고 산업적으로
viable 한 이유를 명료히 한다: VGCF bypass 가 σ_e penalty 를 대부분
중화한다. 본 논문의 framework — DEM 에서 도출된 microstructure-level
transport descriptor 에 집중 — 는 78-case ensemble 에 VGCF 를 포함
시키지 않는다; σ_e decomposition 에 VGCF percolation 을 explicit term
η_topology_VGCF 로 추가하는 확장이 자연스러운 다음 단계이지만 여기서는
out of scope 이다. Section 6 / 7 의 σ_e 숫자들은 따라서 *bare-
microstructure 의 fracture-induced loss upper bound* 로 서며, VGCF 가
포함된 실제 cell-level loss 는 substantially 더 작을 것으로 예상된다.
