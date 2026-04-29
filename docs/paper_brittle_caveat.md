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
> | AM_P-AM_P | 5.0 μm | 1.21 mN | 10.4 mN | 8.7 | multicrack |
> | AM_S-AM_S | 2.5 μm | 6.70 mN | 1.9 mN | 0.28 | intact |
> | AM_P-AM_S | 2.5 μm | 2.01 mN | 3.4 mN | 1.7 | microcrack |
>
> AM_P-AM_P contacts cluster around F/P_c ≈ 9 (multicrack, ~3·P_c
> threshold), AM_S-AM_S contacts sit safely in the intact regime
> (F < P_c), and mixed contacts straddle the cone-crack onset
> (F/P_c ≈ 1.7, microcrack). The 3.3× K_IC ratio between single-
> crystal and polycrystalline NCM (Quinn 2020 vs Liu 2020) gives a
> ~11× P_c ratio at fixed R, fully accounting for the AM_P / AM_S
> stage-distribution asymmetry reported in Section 3.

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
> | AM_P-AM_P | 5.0 μm | 1.21 mN | 10.4 mN | 8.7 | multicrack |
> | AM_S-AM_S | 2.5 μm | 6.70 mN | 1.9 mN | 0.28 | intact |
> | AM_P-AM_S | 2.5 μm | 2.01 mN | 3.4 mN | 1.7 | microcrack |
>
> AM_P-AM_P 접촉은 F/P_c ≈ 9 부근 (multicrack, 약 3·P_c threshold) 에
> 집중되고, AM_S-AM_S 접촉은 F < P_c 인 intact 영역에 안정적으로
> 위치하며, 혼합 접촉은 cone-crack 시작점 부근 (F/P_c ≈ 1.7,
> microcrack) 에 걸쳐 있다. 단결정과 다결정 NCM 사이의 3.3× K_IC
> 비 (Quinn 2020 vs Liu 2020) 가 동일 R 에서 ~11× P_c 비를 부여하며,
> 이것이 Section 3 에서 보고되는 AM_P / AM_S 사이의 stage 분포
> 비대칭을 완전히 설명한다.

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
fractions from the literature.

**Table 1.** Aggregate AM-AM damage-stage distribution (δ-based
classifier, N = 267,042 contacts) versus experimental observation.

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

| Pair type | n_contacts | Severe (frag+pulv) % |
|---|---|---|
| AM_P – AM_P (polycryst – polycryst) | 10,738 | **31.3 %** |
| AM_P – AM_S (mixed) | 39,984 | 5.3 % |
| AM_S – AM_S (single-crystal – single-crystal) | 216,320 | **0.0 %** |

Two consequences of this breakdown make the validation especially
strong. First, the AM_S population is essentially fracture-free
(0.0 % severe), reproducing the well-established experimental fact
that single-crystal NCM secondary particles are an order of magnitude
more robust than polycrystalline secondaries (Liu 2020, Quinn 2020).
The classifier was not told that AM_S "should" survive — the
R-dependent Auerbach threshold and the K_IC values produce this
result emergently. Second, the mixed AM_P–AM_S population sits at
geometric-mean K_IC and exhibits an intermediate severity (5.3 %),
again consistent with literature expectation for hybrid
microstructures.

**Force-based cross-check.** The same data classified via Lawn force
multipliers (1, 3, 11, 32) on F/P_c with F drawn directly from the
DEM normal-force field reproduces the same qualitative ordering
(AM_P – AM_P > mixed > AM_S – AM_S) and the same severe-fraction
range (a few percent overall). Quantitative agreement between the
δ-based and force-based classifiers — within the per-stage Lawn
factor-of-2 uncertainty — provides a robustness check against the
Hooke-vs-Hertz form-factor sensitivity discussed in Section 2.

**Per-case fracture index.** For every case we define
$\text{fracture\_index} = (n_{\text{frag}} + n_{\text{pulv}}) / n_{\text{total}}$
∈ [0, 1]. Across the 156-case ensemble the median fracture index is
0.013, the mean is 0.076, and the maximum is 0.613. The right-skewed
distribution — half of the ensemble has fewer than 1.3 % severe
contacts — confirms that catastrophic over-overlap is concentrated
in a small minority of cases and that the *median* simulation is
within physically reasonable bounds. Section 5 uses this index as a
filter to verify that the σ_ionic scaling-law conclusions are robust
to the choice of fracture-permissive cases.

### 한국어

Auerbach-Lawn classifier 를 156-case 앙상블의 267,042 개 AM-AM 접촉
전체에 적용한 결과, 집계된 stage 분포는 Table 1 에 문헌의 실험적
NCM cracking fraction 과 함께 제시된다.

**Table 1.** AM-AM 손상 stage 분포 (δ-기반 분류기, N = 267,042 접촉)
대 실험 관측값.

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

| Pair 유형 | n_contacts | Severe (frag+pulv) % |
|---|---|---|
| AM_P – AM_P (다결정 – 다결정) | 10,738 | **31.3 %** |
| AM_P – AM_S (혼합) | 39,984 | 5.3 % |
| AM_S – AM_S (단결정 – 단결정) | 216,320 | **0.0 %** |

이 분해의 두 가지 결과가 본 검증을 특히 강하게 만든다. 첫째,
AM_S 집단은 본질적으로 fracture-free (0.0 % severe) 이며, 이는
단결정 NCM secondary 입자가 다결정 secondary 보다 한 자리수
이상 robust 하다는 잘 확립된 실험적 사실 (Liu 2020, Quinn 2020) 을
재현한다. Classifier 에 AM_S 가 "살아남아야 한다" 고 알려준 적이
없다 — R-의존 Auerbach threshold 과 K_IC 값들이 이 결과를 *발현적
으로* 산출한다. 둘째, 혼합 AM_P–AM_S 집단은 K_IC 의 기하평균에
위치하며 중간 정도의 severity (5.3 %) 를 보여, 이 또한 hybrid
microstructure 에 대한 문헌 기대치와 일관된다.

**Force-기반 cross-check.** DEM 의 normal-force 필드에서 직접 가져온
F 에 Lawn force 배수 (1, 3, 11, 32) 를 적용한 force-기반 분류는
같은 질적 순서 (AM_P – AM_P > mixed > AM_S – AM_S) 와 같은 severe-
fraction 범위 (전체적으로 수 percent) 를 재현한다. δ-기반 분류기와
force-기반 분류기 사이의 정량적 일치 — 단계당 Lawn factor-of-2
불확실성 이내 — 는 Section 2 에서 논의한 Hooke-vs-Hertz form-factor
민감도에 대한 robustness check 를 제공한다.

**Per-case fracture index.** 각 case 마다
$\text{fracture\_index} = (n_{\text{frag}} + n_{\text{pulv}}) / n_{\text{total}}$
∈ [0, 1] 를 정의한다. 156-case 앙상블에서 중앙값 fracture index 는
0.013, 평균은 0.076, 최댓값은 0.613 이다. 오른쪽으로 치우친 분포 —
앙상블의 절반은 severe 접촉이 1.3 % 미만 — 는 catastrophic over-
overlap 이 소수 case 에 집중되어 있음을, 그리고 *중앙값* 시뮬레이션은
물리적으로 합리적인 범위 내에 있음을 확증한다. Section 5 는 이
지수를 필터로 활용하여 σ_ionic scaling-law 결론이 fracture-permissive
case 의 선택에 대해 robust 함을 검증한다.

---

<!-- Section 4 will be appended below after review. -->
