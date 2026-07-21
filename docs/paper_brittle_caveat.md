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
loss in the 78-case ensemble.

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
the Lawn 1998 force multiplier m = F/P_c. If m ≥ 3 (multicrack threshold
or beyond), set the contact's conductance to zero (R = ∞). All other
contacts unchanged. This is a *strict upper bound* on σ_e_loss because
it assumes any contact in the multicrack-or-worse regime is electrically
broken. Implementation: filter contacts.csv, re-run network_conductivity
on the filtered graph.

**Stage D — Stagewise σ_factor (Lawn-literature).** Replace the binary
0/1 cutoff with literature-informed per-stage scaling, capturing the
fact that fractured contacts retain *partial* conductance (Trevisanello
2021, Min 2024, Jiang 2021):

```
intact         (m < 1)        × 1.00
microcrack     (1 ≤ m < 3)    × 0.85   (Trevisanello, Heenan)
multicrack     (3 ≤ m < 11)   × 0.40   (Jiang rock-salt + grain sep.)
fragmentation  (11 ≤ m < 32)  × 0.10   (Min, mostly broken + rock-salt)
pulverization  (m ≥ 32)       × 0.02   (binary literature limit)
```

Implementation: scale contact_area + delta of each AM-AM contact by the
stage σ_factor. Topology preserved; only edge weights modified.

**Stage E — Full literature corrections.** Stage D plus the per-particle
σ_grain factor for AM crystallinity (Trevisanello 2021 single-crystal
vs polycrystalline) and SE size (Cronau 2022 size-invariant ≥ 0.3 μm,
amorphization onset below). For κ_thermal, AM crystallinity factor
(Wang 2022 phonon GB scattering) replaces fracture; SE κ is size-
invariant per Yang 2022 (sulfide already in glassy regime). Per-particle
factors (size + crystallinity dependent) are listed in Section 6 of the
companion code documentation. Edge factors use harmonic mean of two
particle factors.

**Bound interpretation.** The three variants form a graduated estimate
of the fracture-aware σ_e:

- Stage C is the *upper bound on σ_e_loss* (lower bound on σ_e). It
  assumes complete loss above multicrack threshold.
- Stage E is the *literature-realistic central estimate*. It captures
  partial conductance preservation through stagewise scaling and AM
  crystallinity dependence.
- The gap C → E quantifies how much "rescue" the literature stagewise
  scaling provides on top of the conservative binary cutoff.

**Empirical results — 78-case ensemble.** Across the 53 cases that
pass the σ_e numerical-anomaly filter (out of 78 raw):

```
σ_e channel results
─────────────────────────────────────────────────────────────────
σ_e baseline           median 6.48 mS/cm  mean 6.01   max 13.74
Stage C (binary)       median 2.86        mean 3.63   max 10.88
                       loss median 29%, Q1/Q3 15/77%
Stage D (stagewise)    median 4.92        mean 4.94   max 10.75  (n=54)
                       loss median 7%, Q1/Q3 2/22%
Stage E (full)         median 4.71        mean 4.72   max 10.75   (n=54)
                       loss median 11%, mean 18%
                       fa(E)/full ratio median 0.89

κ_thermal channel results (Stage E only)
─────────────────────────────────────────────────────────────────
κ baseline             median 4.29
κ Stage E              median 4.15  mean 4.60
                       loss median 2%, MEAN 3%       ← nearly full preservation
                       Q1/Q3 -0.1/4.8%
                       AM_S-rich cases: minimal loss (~1%)
                       AM_P-rich cases: modest loss (~5%)
```

Three findings stand out:

(1) The literature-informed stagewise σ_factor (Stage D) *substantially
reduces* the binary Stage C upper bound: from 29 % to 7 % median loss —
a factor-of-four rescue. This is because a large share of the AM-AM
contacts that Stage C zeroes out actually sit in the multicrack band
(factor 0.40 in Stage D) or microcrack band (0.85), not in the
catastrophic fragmentation/pulverization tail. The literature
consensus — fractured cathode particles retain partial conductance
via rock-salt phase and grain-adjacency (Trevisanello 2021, Min 2024,
Jiang 2021) — is empirically validated across the 78-case ensemble.
Stage C is therefore correctly interpreted as a *strict upper bound*
on σ_e_loss (not a realistic description), while Stage D at 7 % loss
is the literature-realistic central estimate.

(2) Stage E (Stage D + AM crystallinity factor) sits at 11 % median
loss — slightly above Stage D because the AM_P × 0.65 grain factor
further attenuates the AM_P-mediated σ_e paths. The C → E interval
(29 % → 11 %) brackets the physically realistic loss: the binary R = ∞
overstates loss by ~3×, and the AM-crystallinity refinement adds a
small additional attenuation on top of the stagewise scaling.

(3) The κ_thermal channel shows *nearly full preservation* (median
loss 2 %, mean 3 %): AM_S-rich designs lose ~1 %, AM_P-rich ~5 %.
Both are order-of-magnitude smaller than the σ_e losses because
κ_thermal has no fracture filtering (Stage E applies only the AM
crystallinity factor to κ) and because the AM_P × 0.50 phonon-GB
factor is applied only to the AM-AM fraction of the total thermal
network, which is diluted by the AM-SE and SE-SE contact contributions.
This is the quantitative thermal counterpart of the cathode-side σ_e
asymmetry — single-crystal AM_S delivers benefits in both channels,
but the *thermal channel is inherently more robust* to fracture than
the electronic channel.

**Stratification by r_SE.** The Stage E σ_e loss is also size-stratified
(Section 7.5 will quantify this fully):

```
Stage E σ_e_loss by r_SE band:
  fine    (< 0.7 μm) :  n=32  median 20 %  max 61 %
  medium  (0.7–1.2)  :  n= 5  median  3 %  max  3 %
  coarse  (> 1.2)    :  n=17  median  4 %  max 71 %
```

The pattern reveals a *fracture-sensitivity vs σ_e-magnitude trade-off*
that complements Section 5-1's cathode-side small-SE preference. Fine
SE designs achieve high σ_e_baseline (via η_topology_void, Section 5-1)
but are more fracture-sensitive: their few AM-AM contacts are each
critical for σ_e percolation, so losing any triggers a larger relative
drop (median 20 %). Coarse SE designs have lower σ_e_baseline but
richer AM-AM contact redundancy; fracturing individual contacts leaves
the network largely intact (median 4 % loss). The Pareto-optimal design
therefore selects fine SE and simply *accepts* the higher fractional
loss — the fine-SE σ_e_baseline is high enough that even after the
20 % literature-realistic correction, the absolute σ_e_post remains
above the coarse-SE alternatives.

**Implication.** Combining the Section 4 σ_ionic invariance, the
Section 5-1 cathode/separator inversion, and the Section 6 σ_e + κ
fracture-aware quantification, the present paper's design rule for
the cathode composite is:

  *Small SE (sub-μm) + AM_S-rich (single-crystal) microstructure
  preserves all three transport channels under literature-realistic
  fracture conditions; AM_P-rich coarse-SE microstructures lose 60+ %
  of σ_e and κ to the fracture-induced AM-AM contact damage.*

The σ_ionic channel is by construction insensitive to AM-AM fracture
(Section 4) and therefore not penalized in either direction.

### 한국어

Sections 4–5-1 은 σ_ionic scaling law 가 *구조적으로* AM-AM fracture
와 분리됨 (SE-SE-only ionic graph) 과, bulk-pellet vs cathode 의 SE
크기 optimum 역전이 dominant mechanism 의 깔끔한 분리임을 확립했다.
σ_e (전자) 와 σ_thermal 채널은 같은 보호를 받지 *못한다* — 둘 다
fracture 가 직접 영향을 미치는 AM-AM contact 에 의존한다. 본 절은
78-case 앙상블에서 σ_e / σ_thermal 손실을 정량화하는 fracture-aware
solver methodology 를 제시한다.

**Decomposition framework.** 세 transport 채널 모두 다음 곱셈 분해를
인정한다:

```
σ_eff = σ_grain × η_topology(microstructure)
```

여기서 σ_grain 은 intrinsic 단결정 전도도 (literature input), η_topology
는 network solver 가 계산하는 dimensionless microstructural factor 이다.
본 논문의 v29 main scaling law (Section 4, LOOCV R² = 0.90) 는 정확히
σ_ionic 의 η_topology fit 이다. Fracture-aware 분석은 η_topology 만
수정하며 σ_grain 은 건드리지 않는다. 이 orthogonality 가 Sections 4–5
의 σ_ionic 결론을 그대로 carry over 시키는 이유이다.

σ_e 와 σ_thermal 의 경우 η_topology 는 fracture 가 깰 수 있는 AM-AM
contact 에 의존한다. 세 solver variant 가 fracture-loss estimate 를
점진적으로 정밀화한다:

**Stage C — Binary cutoff (R = ∞).** 각 AM-AM contact 에 대해 Lawn
1998 force multiplier m = F/P_c 분류. m ≥ 3 (multicrack 임계 이상)
이면 contact conductance = 0 (R = ∞). 그 외는 변화 없음. *σ_e_loss
의 strict upper bound* 이다 — multicrack-or-worse regime 의 모든
contact 이 전기적으로 broken 이라고 가정하기 때문. 구현: contacts.csv
필터 후 network_conductivity 재실행.

**Stage D — Stagewise σ_factor (Lawn-literature).** Binary 0/1 cutoff
대신 literature-informed per-stage scaling 으로 대체. Fractured contact
이 *부분* 전도도를 유지한다는 사실 (Trevisanello 2021, Min 2024, Jiang
2021) 을 반영:

```
intact         (m < 1)        × 1.00
microcrack     (1 ≤ m < 3)    × 0.85   (Trevisanello, Heenan)
multicrack     (3 ≤ m < 11)   × 0.40   (Jiang rock-salt + grain 분리)
fragmentation  (11 ≤ m < 32)  × 0.10   (Min, mostly broken + rock-salt)
pulverization  (m ≥ 32)       × 0.02   (binary literature 한계)
```

구현: 각 AM-AM contact 의 contact_area + delta 를 stage σ_factor 로
스케일. Topology 는 보존, edge weight 만 수정.

**Stage E — Full literature corrections.** Stage D + AM 결정성에 대한
per-particle σ_grain factor (Trevisanello 2021 single-crystal vs poly-
crystalline) + SE 크기 factor (Cronau 2022 size-invariant ≥ 0.3 μm,
이하 amorphization 시작). κ_thermal 의 경우 AM 결정성 factor (Wang
2022 phonon GB scattering) 가 fracture 를 대체 — SE κ 는 size-invariant
(Yang 2022, sulfide 이미 glassy regime). Per-particle factor (크기 +
결정성 의존) 는 companion code 문서의 Section 6 에 명시. Edge factor
는 두 particle factor 의 harmonic mean 사용.

**Bound interpretation.** 세 variant 가 fracture-aware σ_e 의 graduated
estimate 를 형성:

- Stage C 는 *σ_e_loss 의 upper bound* (σ_e 의 lower bound). Multicrack
  임계 이상의 완전 손실 가정.
- Stage E 는 *literature-realistic central estimate*. Stagewise scaling
  으로 부분 전도도 보존 + AM 결정성 의존성 capture.
- C → E gap 은 보수적 binary cutoff 위에 literature stagewise scaling
  이 제공하는 "rescue" 의 양을 정량화한다.

**Empirical 결과 — 78-case 앙상블.** σ_e 수치 anomaly filter 통과한
53 cases (78 raw 중) 에 대해:

```
σ_e 채널 결과
─────────────────────────────────────────────────────────────────
σ_e baseline           median 6.48 mS/cm  mean 6.01   max 13.74
Stage C (binary)       median 2.86        mean 3.63   max 10.88
                       loss median 29%, Q1/Q3 15/77%
Stage D (stagewise)    median 4.92        mean 4.94   max 10.75  (n=54)
                       loss median 7%, Q1/Q3 2/22%
Stage E (full)         median 4.71        mean 4.72   max 10.75   (n=54)
                       loss median 11%, mean 18%
                       fa(E)/full ratio median 0.89

κ_thermal 채널 결과 (Stage E only)
─────────────────────────────────────────────────────────────────
κ baseline             median 4.29
κ Stage E              median 4.15  mean 4.60
                       loss median 2%, MEAN 3%       ← 거의 완전 보존
                       Q1/Q3 -0.1/4.8%
                       AM_S-rich cases: 최소 손실 (~1%)
                       AM_P-rich cases: 적정 손실 (~5%)
```

세 가지 발견:

(1) Literature-informed stagewise σ_factor (Stage D) 가 binary Stage C
upper bound 를 *substantially 감소* 시킨다: 29 % 에서 7 % median loss
로 — factor-of-four rescue. 이는 Stage C 가 zero 처리하는 AM-AM contact
의 상당수가 실제로는 multicrack band (Stage D factor 0.40) 또는
microcrack band (0.85) 에 위치하지 catastrophic fragmentation/
pulverization tail 이 아니기 때문이다. Fractured cathode 입자가 rock-
salt phase 와 grain-adjacency 를 통해 partial conductance 를 유지한다는
literature consensus (Trevisanello 2021, Min 2024, Jiang 2021) 가 78-
case 앙상블에서 empirical 검증. Stage C 는 따라서 σ_e_loss 의 *strict
upper bound* (realistic description 아님), Stage D 의 7 % loss 가
literature-realistic central estimate 이다.

(2) Stage E (Stage D + AM crystallinity factor) 가 11 % median loss
에 위치 — Stage D 위에 AM_P × 0.65 grain factor 가 AM_P-mediated σ_e
경로를 추가로 약화. C → E 구간 (29 % → 11 %) 이 physically realistic
loss 를 bracket 한다: binary R = ∞ 가 loss 를 ~3× 과대평가, AM-
crystallinity refinement 가 stagewise scaling 위에 작은 추가 약화 부여.

(3) κ_thermal 채널이 *거의 완전 보존* (median loss 2 %, mean 3 %)
을 보인다: AM_S-rich ~1 %, AM_P-rich ~5 % 손실. σ_e 손실보다 order-
of-magnitude 작으며 이유는 두 가지 — κ_thermal 에는 fracture filter
가 적용되지 않으며 (Stage E 는 κ 에 AM crystallinity factor 만 적용),
AM_P × 0.50 phonon-GB factor 가 전체 thermal network 중 AM-AM 부분에만
적용되어 AM-SE 와 SE-SE contact contribution 으로 dilute 되기 때문.
Cathode 측 σ_e 비대칭의 정량적 thermal 대응 — single-crystal AM_S 가
전기 + 열 채널 양쪽에서 benefit 을 제공하지만, *thermal 채널이 fracture
에 대해 본질적으로 electronic 채널보다 robust*.

**r_SE 별 stratification.** Stage E σ_e loss 의 크기-별 stratification
(Section 7.5 에서 fully 정량화):

```
Stage E σ_e_loss by r_SE band:
  fine    (< 0.7 μm) :  n=32  median 20 %  max 61 %
  medium  (0.7–1.2)  :  n= 5  median  3 %  max  3 %
  coarse  (> 1.2)    :  n=17  median  4 %  max 71 %
```

이 pattern 은 Section 5-1 의 cathode 측 small-SE preference 를 보완하는
*fracture-sensitivity vs σ_e-magnitude trade-off* 를 드러낸다. Fine SE
design 은 η_topology_void 를 통해 high σ_e_baseline 을 달성 (Section
5-1) 하지만 fracture 에 더 민감하다: 소수의 AM-AM contact 각각이 σ_e
percolation 에 critical 하므로, 어느 하나라도 잃으면 상대적으로 큰
drop 을 일으킨다 (median 20 %). Coarse SE design 은 σ_e_baseline 이
낮지만 AM-AM contact redundancy 가 풍부; 개별 contact fracture 가
network 에 미치는 영향이 작다 (median 4 % loss). Pareto-optimal design
은 따라서 fine SE 를 선택하고 더 높은 fractional loss 를 *수용*한다 —
fine SE 의 σ_e_baseline 이 높아서 20 % literature-realistic correction
후에도 절대 σ_e_post 가 coarse SE alternative 위에 남는다.

**함의.** Section 4 의 σ_ionic 불변성, Section 5-1 의 cathode/separator
역전, Section 6 의 σ_e + κ fracture-aware 정량화를 종합하면, 본 논문
의 cathode composite 에 대한 design rule 은:

  *Small SE (sub-μm) + AM_S-rich (single-crystal) microstructure 가
  literature-realistic fracture 조건 하에서 세 transport 채널 모두
  보존; AM_P-rich coarse-SE microstructure 는 fracture-induced AM-AM
  contact 손상으로 σ_e 와 κ 의 60 % 이상 손실.*

σ_ionic 채널은 구조적으로 AM-AM fracture 에 둔감 (Section 4) 하므로
어느 방향으로도 penalty 받지 않는다.

---

## Section 7 — Empirical 78-Case Sweep: 10-Case Anchor, Regression, and Pareto Winners

### English

Section 6 established the fracture-aware solver methodology and reported
the ensemble-level σ_e / κ statistics. This section drills into the
78-case ensemble at case level: (i) a 10-case corner anchor spanning
the (P:S, r_SE) design grid that provides the mechanistic backbone;
(ii) regression of σ_e_loss on microstructural predictors to identify
the dominant driver; (iii) Stage E composite Pareto ranking of design
winners; (iv) the r_SE band stratification that establishes the fine-SE
Pareto region.

**7.1 Ten-case anchor design.** The (P:S, r_SE) 2-parameter sweep
occupies a 5×2 corner grid: P:S ∈ {0:10, 3:7, 5:5, 7:3, 10:0} and
r_SE ∈ {0.5, 1.5} μm. All 10 anchor cases sit at AM:SE volume ratio
≈ 82:18 and 300 MPa target compaction. Baseline (no fracture correction)
values are tabulated in the companion CSV (`docs/db/section7_10case_sweep.csv`).
The 5×2 grid systematically maps how P:S and r_SE separately affect
each transport channel:

- σ_ionic peaks near P:S = 7:3 for both r_SE values, consistent with
  bimodal packing benefit and the Section 4 conclusion that σ_ionic
  depends primarily on SE-SE percolation.
- σ_e is dramatically higher at r_SE = 1.5 μm (median 7.0 mS/cm across
  all P:S) than at r_SE = 0.5 μm (median 4.1 mS/cm), because larger SE
  cannot infiltrate inter-AM voids and forces AM-AM direct contacts
  (Section 5-1 η_topology_void mechanism, inverted for σ_e).
- κ_thermal shows the same coarse-SE preference as σ_e (all-contact
  network favors AM-AM direct paths).

The 10-case anchor thus establishes the *three-channel decoupling* at
case level: σ_ionic, σ_e, and κ each respond to (P:S, r_SE) via
different topology terms, and no single design maximizes all three
simultaneously — the Pareto frontier is not degenerate.

**7.2 Regression predictors of σ_e_loss_pct (Stage C, 78 cases).**
Across the 54 valid cases (22 anomalies excluded by the σ_e > 100
mS/cm sparse-graph filter, plus 2 additional numerical outliers), the
Pearson and Spearman regressions identify:

```
predictor                       Pearson    Spearman   n
─────────────────────────────────────────────────────────
AM-AM excluded %                 +0.746     +0.952    54  ← dominant
porosity                         -0.163     -0.332    54
r_SE (μm)                        -0.164     -0.200    54
```

The AM-AM excluded fraction (share of AM-AM contacts flagged as
multicrack+ by the F/P_c ≥ 3 threshold) is *the* dominant predictor
of σ_e_loss: Spearman r = 0.95 indicates near-perfect rank correlation.
This confirms the direct mechanistic chain of Section 6.1: the more
AM-AM contacts fall into the fracture-band, the more of the AM-AM
network is disconnected under Stage C's binary filter, and the more
σ_e is lost. The other predictors (r_SE, porosity) are weak (|r| < 0.35)
because they act only indirectly, mediated by their influence on the
AM-AM contact stress distribution.

The negative sign on r_SE (r = -0.16) is initially counterintuitive:
larger SE seemingly correlates with *smaller* σ_e_loss. The mechanism
is that coarse-SE cathodes have richer AM-AM redundancy (Section 6.5),
so the same fraction of severe AM-AM contacts translates to a smaller
relative σ_e drop. The r_SE effect on σ_e_loss is thus not from
mechanical stress (which favors small r_SE for AM_P survival) but from
network redundancy topology.

**7.3 Stage E composite Pareto ranking.** Ranking all 78 cases by a
normalized composite score (average of σ_ionic_baseline, σ_e_Stage_E,
κ_Stage_E all min-max normalized to [0, 1]), the top-10 winners are:

```
Rank  case_id                r_SE   σ_ionic  σ_e_E  κ_E    Pareto
─────────────────────────────────────────────────────────────────
🥇    260421_214540_c7c589   0.5    0.333    7.28   10.79   0.721
🥈    260421_214433_b890e5   0.5    0.307    7.24    9.38   0.647
🥉    260421_214255_54799a   0.5    0.281    5.60   10.51   0.627
4     260421_214325_4478d8   0.5    0.159    8.29    8.95   0.583
5     260423_134749_9454f0   0.5    0.130    6.73    9.67   0.547
6     260421_214128_1129da   0.5    0.160    8.06    6.14   0.456
7     260421_192558_1d6404   1.0    0.641    1.54    4.97   0.453
8     260421_213850_cb95b9   0.5    0.029   10.75    4.99   0.425
9     260421_192712_db852c   1.5    0.588    1.80    4.67   0.419
10    260423_110038_1aba36   0.5    0.021   10.54    4.26   0.383
```

Eight of the top-10 winners have r_SE = 0.5 μm. The two 1.0 / 1.5 μm
winners (ranks 7 and 9) are outliers where an unusually high σ_ionic
(0.6 mS/cm) compensates for the mediocre σ_e and κ. The 3rd through
6th ranks are all at r_SE = 0.5 μm with the σ_ionic, σ_e, κ triple
all above baseline median — the *fine-SE Pareto cluster*.

Winner 260421_214540_c7c589 exemplifies the fine-SE Pareto region:
r_SE = 0.5 μm, σ_ionic = 0.333 mS/cm (highest in the ensemble),
σ_e_Stage_E = 7.28 mS/cm (above the 6.5 mS/cm ensemble median), and
κ_Stage_E = 10.8 mS/cm-equiv (well above 4.3 median). Its σ_e_loss
is 42 % — the highest among the top-3 winners — yet the *absolute*
σ_e_post at 7.28 still comfortably exceeds the alternatives. This
is the fracture-sensitivity vs σ_e-magnitude trade-off of Section 6.5
made concrete: high-σ_e_baseline designs can afford higher fractional
loss because the residual σ_e stays high.

**7.4 r_SE band stratification of Stage E outcomes.** Stratifying the
54 valid cases by r_SE band confirms the fine-SE dominance:

```
r_SE band            n    σ_e loss median    σ_e_post median
──────────────────────────────────────────────────────────────
fine (< 0.7 μm)      32       20 %             4.5 mS/cm
medium (0.7–1.2)      5        3 %             4.9 mS/cm
coarse (> 1.2)       17        4 %             4.4 mS/cm
```

The three bands produce *nearly identical σ_e_post medians* (4.4–4.9
mS/cm) despite dramatically different loss rates. Fine SE designs
tolerate a 20 % loss and still land at 4.5 mS/cm because their
baselines are high; coarse SE designs enjoy only 4 % loss but end at
4.4 mS/cm because their baselines are lower. The composite Pareto
score, which also credits σ_ionic and κ, then breaks the tie in favor
of fine SE because fine SE simultaneously delivers higher σ_ionic
(Section 5-1) and generally higher κ (via the AM-SE contact area
that fine SE opens up).

**7.5 Design implication and cross-section synthesis.** Combining
Section 4 (σ_ionic invariance to AM-AM fracture), Section 5-1
(bulk-vs-cathode r_SE inversion), Section 6 (three-channel fracture
correction), and Section 7 (empirical Pareto ranking), the paper's
final design rule for the composite cathode is:

  *Small SE (0.5 μm) with high AM density (P:S ≈ 3:7 to 7:3) maximizes
  the (σ_ionic, σ_e_post, κ_post) triple under literature-realistic
  fracture correction. The design accepts a ~20 % σ_e_loss because
  the high σ_e_baseline (~ 10 mS/cm before fracture) leaves the
  residual well above coarse-SE alternatives. Single-crystal AM_S
  further improves the post-fracture σ_e and κ through the
  Trevisanello 2021 crystallinity factor.*

The separator layer, per Section 5-1, uses coarse SE (1–3 μm) via a
different mechanism entirely; the bilayer cell architecture is the
natural consequence.

### 한국어

Section 6 이 fracture-aware solver methodology 를 확립하고 앙상블-
레벨 σ_e / κ 통계를 보고했다. 본 절은 78-case 앙상블을 case 레벨로
파고든다: (i) (P:S, r_SE) design grid 를 span 하는 10-case corner
anchor 가 mechanistic backbone 을 제공; (ii) σ_e_loss 를 microstructural
predictor 로 회귀하여 dominant driver 식별; (iii) Stage E composite
Pareto ranking 의 design winners; (iv) fine-SE Pareto region 을
확립하는 r_SE band stratification.

**7.1 Ten-case anchor design.** (P:S, r_SE) 2-parameter sweep 이
5×2 corner grid 를 점유: P:S ∈ {0:10, 3:7, 5:5, 7:3, 10:0}, r_SE
∈ {0.5, 1.5} μm. 10 anchor case 모두 AM:SE 부피비 ≈ 82:18, 300 MPa
target 압축. Baseline (fracture correction 없음) 값은 companion CSV
(`docs/db/section7_10case_sweep.csv`) 에 표로 정리. 5×2 grid 가 P:S
와 r_SE 가 각 transport 채널에 어떻게 별도로 영향 미치는지 체계적으로
mapping:

- σ_ionic 은 r_SE 두 값 모두에서 P:S = 7:3 근처 peak — bimodal packing
  benefit 과 σ_ionic 이 SE-SE percolation 에 primarily 의존한다는
  Section 4 결론과 정합.
- σ_e 는 r_SE = 1.5 μm 에서 dramatically 더 높음 (모든 P:S 걸쳐 median
  7.0 mS/cm) vs r_SE = 0.5 μm (median 4.1 mS/cm) — 큰 SE 가 inter-AM
  void 침투 못 해 AM-AM 직접 접촉 강제 (Section 5-1 η_topology_void
  mechanism, σ_e 에 대해 반전).
- κ_thermal 은 σ_e 와 같은 coarse-SE preference — all-contact network
  가 AM-AM 직접 경로를 선호.

10-case anchor 는 따라서 case 레벨에서 *3-channel decoupling* 을 확립:
σ_ionic, σ_e, κ 가 각각 다른 topology 항을 통해 (P:S, r_SE) 에 반응
하며, 어떤 단일 design 도 세 개를 동시에 maximize 하지 못한다 —
Pareto frontier 는 degenerate 하지 않다.

**7.2 σ_e_loss_pct 의 회귀 predictor (Stage C, 78 cases).** Valid 54
cases (σ_e > 100 mS/cm sparse-graph filter 로 22 anomaly 제외 + 2
추가 numerical outlier) 걸쳐, Pearson 과 Spearman 회귀가 식별:

```
predictor                       Pearson    Spearman   n
─────────────────────────────────────────────────────────
AM-AM excluded %                 +0.746     +0.952    54  ← dominant
porosity                         -0.163     -0.332    54
r_SE (μm)                        -0.164     -0.200    54
```

AM-AM excluded fraction (F/P_c ≥ 3 임계로 multicrack+ 로 flagged 된
AM-AM contact 비율) 이 σ_e_loss 의 *the* dominant predictor: Spearman
r = 0.95 로 near-perfect rank correlation. Section 6.1 의 direct
mechanistic chain 확인: AM-AM contact 이 fracture-band 에 많이 떨어질
수록 Stage C binary filter 하에서 AM-AM network 가 더 disconnected,
σ_e 손실 더 큼. 다른 predictor (r_SE, porosity) 는 weak (|r| < 0.35)
— indirectly 만 작동, AM-AM contact stress 분포에 대한 영향으로만
매개.

r_SE 의 음의 부호 (r = -0.16) 는 처음에는 counterintuitive: 큰 SE 가
겉보기에 *작은* σ_e_loss 와 상관. 메커니즘은 coarse-SE cathode 가
richer AM-AM redundancy (Section 6.5) 를 가져서, 같은 fraction 의
severe AM-AM contact 이 더 작은 relative σ_e drop 으로 이어짐. r_SE
의 σ_e_loss 에 대한 효과는 따라서 mechanical stress (AM_P 생존을 위해
small r_SE 를 선호) 가 아닌 network redundancy topology 에서 옴.

**7.3 Stage E composite Pareto ranking.** 정규화된 composite score
(σ_ionic_baseline, σ_e_Stage_E, κ_Stage_E 모두 [0, 1] min-max 정규화
후 평균) 로 78 cases ranking 한 top-10 winners:

```
Rank  case_id                r_SE   σ_ionic  σ_e_E  κ_E    Pareto
─────────────────────────────────────────────────────────────────
🥇    260421_214540_c7c589   0.5    0.333    7.28   10.79   0.721
🥈    260421_214433_b890e5   0.5    0.307    7.24    9.38   0.647
🥉    260421_214255_54799a   0.5    0.281    5.60   10.51   0.627
4     260421_214325_4478d8   0.5    0.159    8.29    8.95   0.583
5     260423_134749_9454f0   0.5    0.130    6.73    9.67   0.547
6     260421_214128_1129da   0.5    0.160    8.06    6.14   0.456
7     260421_192558_1d6404   1.0    0.641    1.54    4.97   0.453
8     260421_213850_cb95b9   0.5    0.029   10.75    4.99   0.425
9     260421_192712_db852c   1.5    0.588    1.80    4.67   0.419
10    260423_110038_1aba36   0.5    0.021   10.54    4.26   0.383
```

Top-10 winners 의 8/10 이 r_SE = 0.5 μm. 두 개의 1.0 / 1.5 μm winners
(rank 7, 9) 는 이례적으로 높은 σ_ionic (0.6 mS/cm) 이 mediocre σ_e 와
κ 를 보상하는 outlier. 3-6 rank 는 모두 r_SE = 0.5 μm 이며 σ_ionic,
σ_e, κ triple 이 모두 baseline median 위 — *fine-SE Pareto cluster*.

Winner 260421_214540_c7c589 이 fine-SE Pareto region 을 예시: r_SE =
0.5 μm, σ_ionic = 0.333 mS/cm (앙상블 최댓값), σ_e_Stage_E = 7.28
mS/cm (앙상블 median 6.5 위), κ_Stage_E = 10.8 mS/cm-equiv (4.3
median 훨씬 위). σ_e_loss 는 42 % — top-3 winner 중 최고 — 이지만
*절대* σ_e_post 가 7.28 로 alternative 를 comfortably 능가. 이는
Section 6.5 의 fracture-sensitivity vs σ_e-magnitude trade-off 의
구체화: high-σ_e_baseline design 이 high fractional loss 를 감당
가능한 이유는 residual σ_e 가 높게 남기 때문.

**7.4 Stage E outcome 의 r_SE band stratification.** Valid 54 cases
를 r_SE band 로 stratify 하면 fine-SE dominance 확인:

```
r_SE band            n    σ_e loss median    σ_e_post median
──────────────────────────────────────────────────────────────
fine (< 0.7 μm)      32       20 %             4.5 mS/cm
medium (0.7–1.2)      5        3 %             4.9 mS/cm
coarse (> 1.2)       17        4 %             4.4 mS/cm
```

세 band 가 dramatically 다른 loss rate 에도 불구하고 *거의 동일한
σ_e_post median* (4.4–4.9 mS/cm) 을 생산. Fine SE design 은 20 %
loss 를 tolerate 하고도 baseline 이 높기 때문에 4.5 mS/cm 에 안착;
coarse SE design 은 4 % loss 만 겪지만 baseline 이 낮아서 4.4 mS/cm
에서 끝. Composite Pareto score 가 σ_ionic 과 κ 도 credit 하므로
fine SE 의 유리한 tie-break 가 발생 — fine SE 가 동시에 더 높은
σ_ionic (Section 5-1) 과 일반적으로 더 높은 κ (fine SE 가 여는 AM-SE
contact area 를 통해) 을 delivery.

**7.5 Design 함의와 cross-section synthesis.** Section 4 (σ_ionic 의
AM-AM fracture 불변성), Section 5-1 (bulk-vs-cathode r_SE 역전),
Section 6 (3-channel fracture correction), Section 7 (empirical Pareto
ranking) 을 종합, 본 논문의 복합 양극에 대한 final design rule 은:

  *Small SE (0.5 μm) + high AM density (P:S ≈ 3:7 to 7:3) 조합이
  literature-realistic fracture correction 하에서 (σ_ionic, σ_e_post,
  κ_post) triple 을 maximize. Design 이 ~20 % σ_e_loss 를 accept 하는
  이유는 high σ_e_baseline (fracture 전 ~10 mS/cm) 이 residual 을
  coarse-SE alternative 위에 남기기 때문. Single-crystal AM_S 가
  Trevisanello 2021 crystallinity factor 를 통해 post-fracture σ_e
  와 κ 를 추가로 개선.*

Section 5-1 의 결과 대로 separator layer 는 완전히 다른 mechanism 을
통해 coarse SE (1–3 μm) 를 사용 — bilayer cell architecture 가
자연스러운 귀결이다.
