# DEM 파라미터 보정(calibration) 방법론 리뷰 — 두 학파(직접측정 vs 벌크 역보정)·해의 비유일성·접촉강성(contact stiffness) 감소 — Coetzee (Powder Technology 2017)

> slug `coetzee2017_dem_calibration_review` · DOI `10.1016/j.powtec.2017.01.015` · type `DEM (review — 보정 방법론)` · PDF `2563cb58-Review_Calibration_of_the_discrete_element_method.pdf` · digested `2026-08-25` · status ✅

## 1. 한 줄 요약 (TL;DR)

**DEM 입력 파라미터를 "어떻게 정하는가"만을 25년치 문헌(238편)으로 훑은 유일한 종합 리뷰.**
두 학파를 명명하고 — **Direct Measuring Approach**(입자/접촉 수준 직접 측정) vs
**Bulk Calibration Approach**(벌크 거동 측정 후 파라미터를 반복 조정하는 **역보정**) — 후자를
*"a calibration approach in the true sense of the word"* (p.106) 라 부르며 **가장 널리 쓰이는 접근**
(p.138)으로 인정한다.  동시에 그 대가를 정확히 적는다: **해가 유일하지 않다**(§2 p.106, §5 p.123),
파라미터의 **물리적 의미가 일부 상실**되며, 값이 **코드·접촉모델 의존**이다(§1 p.105, §9 p.138).
처방은 두 줄 — ① **각 실험이 하나의 파라미터를 고립**시키거나 ② **둘 이상 실험의 교집합**으로
유일해를 만들 것, 그리고 ③ **보정에 쓴 시험과 *다른* 시험으로 검증**할 것(§2 p.106).
★ 우리에게 결정적인 문장 하나: **보정값은 형상·크기·접촉모델 단순화의 결손을 *대신 보상*한다**
(§5 p.123, §9 p.138) — 이것이 우리 `E_eff = 1.35 GPa` 18× 연화를 방법론적으로 정당화하는
가장 가까운 문헌 근거다.  ⚠ 단, 이 리뷰는 **저응력 벌크 핸들링**(호퍼·사일로·컨베이어·토양-공구·
드럼) 문헌이고 **소성 접촉법칙을 사실상 다루지 않는다**("plastic" 이 본문 전체에 **1회**, 그것도
rolling 에너지 손실 열거에서) — **방법론은 전이되지만 파라미터·가드레일은 전이되지 않는다.**

---

## 2. 메타

| 항목 | 값 |
|---|---|
| 저자 | **C.J. Coetzee** (단독) |
| 소속 | Department of Mechanical and Mechatronic Engineering, **Stellenbosch University**, South Africa |
| 저널/년 | **Powder Technology 310 (2017) 104–142** (39 pp) |
| DOI | 10.1016/j.powtec.2017.01.015 |
| 유형 | **Review** (자체 시뮬레이션·실험 **0** — 전 수치가 1차 출처 소환값) |
| 이력 | 접수 2016-11-04 / 개정 2016-12-13 / 수락 2017-01-05 / 온라인 2017-01-09 |
| 규모 | 본문 34 pp + 참고문헌 5 pp · **Fig 1–34**(전부 타 논문 "adopted from") · **Table 1–4** · **refs 238** |
| 소재 | ⚠ **배터리 아님**. 파쇄암·자갈·철도 밸러스트·모래·토양·옥수수/쌀/밀 곡물·유리구슬·석탄·철광석 펠릿·목재칩·정제(tablet)·폴리에틸렌 펠릿 |
| 저자 자신의 위치 | Coetzee 는 §5.5 "Comprehensive approach" 의 **1차 출처 저자**([25,26,28,62,201,202]) — 즉 이 리뷰는 중립 서베이인 동시에 **자기 방법론의 자리매김 문서**이기도 하다 (§13 주의 참조) |

**명시적 제외 범위**(§1 p.105): *"in this paper we focus on the calibration of materials **without strong
inter-particle bonds**"* — 본드(cohesive/bonded) 모델 보정은 [20,44–60] 로 넘긴다.
분쇄·파쇄·암석역학처럼 "강한 본드"가 필요한 응용은 언급만 하고 다루지 않는다.

---

## 3. 이 리뷰가 다루는 것 / 다루지 않는 것 (범위 상자 — 인용 전 반드시 확인)

| 축 | 다룬다 | 다루지 않는다 (= 우리가 채우는 칸) |
|---|---|---|
| 응용 | 호퍼·사일로 배출, 컨베이어/슈트, 토양-공구, 회전드럼/믹서, 밀, 밸러스트, 사면/애벌런치 | **냉간 고압 압밀**, 전극 제조, 배터리 |
| 응력 | **명시 수치 사실상 없음** — 중력·핸들링 규모 (삼축 구속압·전단상자 수직응력은 "범위를 맞춰라"는 규칙만) | **300 MPa 냉간압축** (§5-Q6) |
| 접촉법칙 | 선형 spring-dashpot, **Hertz–Mindlin**, rolling resistance, (본드 모델은 배제) | **소성 캡**(Thornton–Ning p_y, EEPA, Storåkers), 다중접촉 mean-field |
| 소성 | ❌ 사실상 없음 — `plastic` 이 본문에 **1회**(Wensrich & Katterfeld 의 rolling 손실 열거, p.106) | 접촉 소성(δ 프록시) · **입자 형상 소성**(우리 MPM) |
| 치밀화 | ❌ Heckel **0회**, `porosity` 9회이나 전부 **전단/삼축의 dilatancy 대리**로만 | Heckel·porosity floor·Furnas dip |
| 형상 | ✅ 매우 상세 (§3.1, 전체의 1/4) — clump / polyhedra / superquadric / superellipsoid | — |
| 크기 스케일업 | ✅ (§3.2) 스케일링 법칙·한계 | 우리는 **스케일업 안 함**(실측 µm PSD 그대로) |
| 전달(σ) | ❌ 전혀 없음 | σ_ionic/σ_e/σ_thermal 전부 우리 |
| 파라미터 분포 | 🔶 §8 "future work" 로만 (Van Lew, Molenda, Wang, Hastie) | — |

---

## 4. 두 학파 — 정의와 원문 (§2, p.105–106)

### 4.1 용어 정의 (리뷰가 §1 p.105에서 세운 구분 — 우리 보고 규약의 근거)

> *"We have to distinguish between **material properties** and **numerical model parameters**.
> Material properties are the properties of the physical material and can be measured at either
> particle/contact level (**micro** properties) or at bulk level (**macro** properties). … **Macro
> properties cannot be specified as input parameters in a DEM model**, the micro parameter values
> need to be determined so that an assembly of numerical particles will exhibit the same bulk
> behaviour as the physical material."* (§1, p.105)

⇒ **DEM 입력 E 는 "물성"이 아니라 "모델 파라미터"** 라는 것이 리뷰의 출발점이다.
이어서: *"Different DEM models might include different parameters and the same parameter
(rolling resistance and contact damping for example) might be implemented differently in various
DEM codes, i.e., **the calibrated parameter values might be code dependent** [66]."* (§1, p.105)

### 4.2 Bulk Calibration Approach (역보정)

> *"The first approach is to make use of a procedure where either in-situ measurements or laboratory
> experiments are performed to measure a specific material bulk property. The experiment is then
> numerically replicated by following the laboratory or field setup and procedures as closely as
> possible. **The DEM parameter values are then changed iteratively until the predicted bulk response
> matches the measured result.**"* (§2, p.106)

> *"**The first approach is a calibration approach in the true sense of the word** since an iterative
> procedure is normally used and the bulk response of the material is matched to measured results by
> changing the parameter values."* (§2, p.106)

§5 서두의 성격 규정(p.123):
> *"The Bulk Calibration Approach **does not necessarily assume a strong link between the DEM
> parameters and physical material properties. The parameters are rather treated as adjustment
> parameters** even though the models were developed by giving the parameters a distinct physical
> meaning [61]."*

### 4.3 Direct Measuring Approach (직접측정)

> *"The second approach … is to directly measure the property values on particle or contact level.
> Some of the properties are easy to measure while others are very difficult, depending on the
> particle scale. Several attempts were made, but **they were all applied to particles in the
> millimetre and above size range** [61]."* (§2, p.106)

> *"**Even if the property values can be directly and accurately measured, it does not necessarily
> mean that the DEM model would show the same level of accuracy on a bulk level** [67,68]. This
> approach would only be accurate if the shape and size of the particles are modelled accurately and
> **if the contact model is an accurate representation of the physical contact behaviour** [69]."* (§2, p.106)

> *"The advantage of this direct measurement approach is that the resulting properties are **not
> dependent on the contact model or the specific DEM code used** [74]."* (§2, p.106)

### 4.4 리뷰의 최종 판정 (§9 결론, p.137–138)

> *"**The bulk calibration approach is by far the most popular approach** and specifically angle of
> repose and hopper discharge tests."* (p.138)

> *"The advantage of the bulk calibration approach is that sophisticated instruments are not needed to
> measure properties at particle or contact level, but any field or laboratory experiment can be
> performed that measures one or more bulk property. **The disadvantage, however, is that it can be
> time consuming to repeat the experiments numerically and the parameter values obtained in this way
> might be software and contact model dependent. Also, more than one experiment might be needed to
> obtain a unique set of parameter values.** Another advantage of this approach is that **the particle
> size can be scaled up, the particle shape can be simplified and assumptions in terms of the contact
> model can be made. The calibration process will then reduce the effect that these simplifications
> and assumptions might have on the bulk behaviour since the other parameters will compensate for
> it.**"* (§9, p.138)  ★★★ **우리 §12 인용 1순위**

직접측정에 대한 결론(§9, p.137):
> *"A major disadvantage, however, is that **it is very difficult to measure the properties at particle
> or contact level if the particles are relatively small and irregular in shape.** Researchers obtained
> **mixed results** following this approach and **in some cases further adjustment of parameter values
> were needed following the bulk calibration approach** to achieve more accurate results."*

---

## 5. ★★ 지도교수 질문 7개 — 직답 (근거 문장 + 쪽수)

### Q1. 벌크 역보정은 DEM 의 정당한 표준 방법론인가?  → **YES. 리뷰는 이를 "진짜 의미의 보정"이라 부르고, "단연 가장 널리 쓰이는 접근"이라 판정한다.**

| 판정 축 | 리뷰의 서술 | 위치 |
|---|---|---|
| **명명** | 두 학파 중 하나로 **정식 명명**: *Bulk Calibration Approach* | 초록 p.104 · §2 p.106 |
| **정당성** | *"a calibration approach in the true sense of the word"* | §2 p.106 |
| **보급도** | *"by far the most popular approach"* | §9 p.138 |
| **권장 조건** | 입자 크기를 **스케일업해야 한다면 벌크 보정을 쓰라**: *"It is suggested that if the particle size has to be scaled up that the **Bulk Calibration Approach should be used** [13,37,136]."* | §3.2 p.115 |
| **효용의 핵심** | *"the calibrated parameter values will **compensate for other aspects such as the particle size and shape not being modelled accurately or the chosen contact model not describing the physical mechanisms very accurately** [95]"* | §5 p.123 |
| **대가(명시)** | 비유일성 · 물리적 의미 일부 상실 · 코드/접촉모델 의존 · 응용 전이 무보장 | §2 p.106 · §5 p.123 · §9 p.138 |

**왜 직접측정이 전이되지 않는가 — 리뷰가 드는 5개 논거**

1. **입경 하한**(가장 강한 논거, 우리에게 결정적): 직접측정 시도는 전부 **밀리미터 이상** 입자에
   적용됐다(§2 p.106).  §6.1이 인용하는 최소 사례가 **500 µm 입자의 접촉 마찰 측정**[218](p.134).
   ⇒ **우리 LPSCl SE(D50 ~1–3 µm 지름)는 이 문헌이 보고하는 직접측정 하한보다 2–3 자릿수 작다.**
2. **형상·크기가 정확해야만 성립**: 직접측정값이 옳아도 모델 입자가 구·클럼프 근사면 벌크가 안 맞는다
   (§2 p.106).  대규모 계에서는 크기 스케일업이 불가피하고 형상은 계산비용 때문에 못 맞춘다.
3. **실측값이 실제로 실패한 사례 2건**(1차 출처):
   · **Just et al. [169]**(정제 코팅, p.135): 측정한 particle–wall 마찰 **0.15 → 최소 0.45로 올려야** cascading
     flow 가 나왔고, 코팅 정제의 측정 particle–particle 마찰 **0.5 → 0.14로 내려야** 동적 안식각이 맞았다.
     저자들 결론 *"the experimental methods used to model the friction coefficients were inadequate."*
   · **Barrios et al. [69]**(철광석 펠릿, p.135): 모든 값을 입자 수준에서 측정했는데도 **구 입자는 안식각
     28.9° 예측 vs 실측 15.3°**, 텀블링 동력 오차 30 %(클럼프 6 %).  마찰을 낮춰야 맞았다.  클럼프의 COR 은
     측정값을 못 쓰고 **역보정**이 필요했다.
4. **원리적으로 측정 불가능한 파라미터가 있다**: rolling friction.  Benvenuti et al. [158]:
   *"it is impossible to link the rolling friction parameter to the non-sphericity of the particles and
   therefore this is a **purely empirical parameter that cannot be determined by direct measurement**"*
   (§5 p.123).  Wensrich & Katterfeld [84]: *"there is **no physical reasoning for choosing a value for
   rolling friction other than tuning the bulk behaviour** to be more realistic"* (§3 p.106).
5. **자유도 논거**: Roessler & Katterfeld [133] — 입자를 키우면 계의 총 자유도가 줄고 벌크 거동은
   상호작용의 **합**이므로 원래 입자의 파라미터값을 그대로 쓸 수 없다(§3.2 p.115).

---

### Q2. 영률/입자 강성은 흔한 보정 대상인가?  → **YES, 표준 목록의 첫 열이다. 단 "왜 낮추는가"가 두 갈래이고 절대 섞으면 안 된다.**

#### (a) 보정 대상으로서의 강성 — Table 1 (p.124) 의 **첫 번째 파라미터 열**이 `Particle/Contact Stiffness`

| 벌크 시험 | 강성을 보정하는 데 쓴 문헌 (리뷰 Table 1) |
|---|---|
| Penetration test | [22,161] |
| Direct/ring shear test (bulk friction angle) | [25,68,108,137,197,200] |
| **Uniaxial compression test (bulk stiffness)** | **[25,26,28,62,201,202]** |
| Static angle of repose / slump / pile | [139,213] |
| Hopper/silo discharge time·rate·velocity | [180,232] |
| Triaxial/Biaxial | [35,76,83,188–190,193–195,238] |
| Soil-tool interaction (draught force) | [38,164,166] |
| In-situ ring shear & vane tester | [163] |
| ANN (AoR + shear test) | [158] |

Table 3 (p.137, "micro-macro relations investigated") 에는 **`Confined bulk stiffness (oedometer)` [25,81,125,205]**
행이 따로 있고, 그 행에서 유일하게 관계가 조사된 파라미터가 **contact stiffness** 다.
⇒ **구속 단축압축(오이도미터)으로 접촉강성을 보정하는 것은 리뷰가 표로 정리한 표준 경로다.**

★ **왜 이 시험인가 — 고립성**(§5.5 p.131, 1차 출처 Coetzee & Els [25], [205]):
> *"the direct shear test results were influenced by **both** the particle-particle friction coefficient
> and the particle stiffness … On the other hand, **the confined uniaxial compression test was only
> influenced by the particle stiffness while the particle-particle friction coefficient had no
> significant effect** [25,205]. For this reason, it was important to **first** perform the uniaxial
> compression test for a range of particle stiffness values. **The relation between the particle
> stiffness and the bulk stiffness was found to be linear**, and using interpolation, the particle
> stiffness that resulted in a bulk stiffness equal to the measured value could be determined."*

강성-우선 보정 순서를 쓴 다른 1차 출처:
- **Belheine et al. [194]**(삼축, p.130): ① 법선강성 + 강성비 ← 초기 영률·푸아송비 정합 → ② 슬라이딩 마찰
  ← dilatancy 곡선 → ③ rolling 마찰 ← 응력-변형 곡선.
- **Salot et al. [195]**(삼축+클럼프, p.130): ① 입자 각형성 ← 잔류 벌크 마찰각 → ② 강성비 ← 푸아송비 →
  ③ *"the material Young's modulus (in effect the contact normal stiffness) was set by matching the
  initial bulk elastic modulus"* → ④ 접촉마찰 ← 최대 벌크 마찰각.
- **Lee et al. [188]**: 마찰 → 법선강성 → 전단강성.
- **Asaf et al. [22]**(관입시험, p.123): *particle–particle 마찰과 particle stiffness 를 **유일한 두 중요 파라미터**로 간주*,
  세 관입공구의 하중-변위 곡선 면적차를 최적화로 최소화.
- **Mak et al. [38]** / **Li et al. [166]** / **Milkevych et al. [163]**: **입자 강성만** 보정(나머지는 문헌값).
- **Sadek et al. [200]**: 전단 응력-변위 곡선의 **항복점**으로 입자 강성을 보정.

#### (b) 계산속도용 강성 감소 — **§7 "Reduction in contact stiffness" (p.135–136), 목적이 다르다**

리뷰 자신의 프레이밍(§7 첫 문단, p.135):
> *"**In order to reduce computation time** … Another method often employed by analysts is to reduce
> the contact stiffness [3]. **The size of the stable time step used for time integration is proportional
> to the square root of the density and inversely proportional to the square root of the contact
> stiffness.**"*

즉 §7 은 **타임스텝을 키우려는 수치 편법**이고, 그 정당성 기준은 **"벌크 거동이 안 변할 것"** 이다.
증거표(전부 1차 출처 stated 값):

| 1차 출처 | 계/시험 | 감소 폭 | 결과 | 쪽 |
|---|---|---|---|---|
| Hart et al. [126,198] | 유리구슬 직접전단 | **전단강성 ÷100** (÷1000까지 시험) | 전단력에 유의 영향 없음 | 135 |
| Chung & Ooi [161] | 구형 캡 로드 관입 | **÷10⁴** | 평균 관입력 둔감, 단 **힘 요동 크기 감소** | 125 |
| Goetsch & Regele [232] | 호퍼 파티클 커튼 | k_n **2.1×10⁶ → 1×10⁵ N/m (÷21)** | 여기까지 OK, **더 줄이면 질량유량·속도장 유의 변화** | 135 |
| Yan et al. [180] | 평저 원통 호퍼 배출 | **E 0.02 GPa → 200 GPa (×10⁴ 범위)** | 거시량(유량·안식각·속도) 유의 영향 **없음**, 계산시간엔 *"enormous effect"* | 127·135 |
| Höhner et al. [72,73] | 호퍼 배출(주사위·구) | **최대 오버랩 0.5 % → 4 %** | 질량유량 유의 변화 없음 → *"max contact overlap ≤ **4 %** is sufficient for the specific system"* | 135–136 |
| Cleary [233] | 다수 산업 응용 | — | 권고 **최대 오버랩 0.1–0.5 %** (Höhner 와 상충, 리뷰가 명시) | 136 |
| Xu et al. [234] | 2D 사일로 배출 | **E 70 MPa vs 70 GPa (÷1000)** | 유동패턴·속도장 차이 없음, **배출률 편차 2.7 %**, 경질 계산시간 **31.6×** | 136 |
| Lommen et al. [81] | ①구속압축 ②쐐기 관입 ③안식각 | — | ① **벌크강성 = 접촉강성의 선형함수** ② G > 1×10⁸ Pa(오버랩 ≤0.3 %) 이면 저항 포화 ③ G ≥ 1×10⁷ Pa 또는 오버랩 <0.3 % 면 안식각 무영향.  *"users should be **cautious** when reducing the contact stiffness and should **verify their approach**"* | 136 |
| **Paulick et al. [235]** (그 자체가 리뷰) | 종합 | — | **선형 접촉강성↔벌크강성** · ***"the denser the system, the more important the stiffness value becomes"*** · 총괄 권고 **최대 오버랩 ≤ 입자 반지름의 1 %** | 136 |

⚠ **(a)와 (b)를 섞으면 안 되는 이유 — 우리 인용 규율**
- (a)는 **데이터가 값을 정한다**(측정된 벌크강성/벌크응답에 맞춤). 재료 E 와 크게 달라도 정당.
- (b)는 **속도가 값을 정한다**. 정당성 조건이 **"벌크가 안 변함"** 이므로, 벌크를 *바꾸려고* 낮추는 것은
  (b)의 논리로 방어할 수 없다.  Franco et al. [196](p.130)이 (b)의 전형: *"choose the particle stiffness
  **as low as possible to reduce computational time** but still prevent excessive particle-particle
  overlap"*; Simons et al. [68](p.130)도 *"the value for the stiffness should simply be **selected to
  minimise computation time**"*.
- ⇒ **우리 18× 연화는 (a)다.** (b)의 가드레일(오버랩 0.1–4 %)을 인용해 우리를 방어하면 **잘못된 인용**이고,
  거꾸로 그 가드레일로 우리를 공격당하면 "우리는 (b)를 하고 있지 않다"가 정답이다.  단 §13-W3 참조 —
  우리 오버랩은 그 창 밖 20–100× 다.

#### (c) 리뷰가 **주지 않는** 것 (정직 고지)
- **"실제 물성보다 낮춘 유효 E 를 거시 치밀화 목표에 맞춘다"는 사례는 이 리뷰에 없다.** §7 은 전부 속도용,
  Table 1 은 전부 **측정된 벌크강성/전단/관입/삼축** 목표.  Heckel·porosity floor 를 목표로 강성을 맞춘
  사례 **0건** (Heckel 0회, porosity 는 dilatancy 대리로만).
- 다만 **크기**로 보면 문헌의 감소폭(×21 ~ ×10⁴)이 우리 18× 를 훨씬 넘고, **인식론**으로 보면 리뷰가
  마찰에 대해 정확히 같은 럼핑을 승인한다: Li et al. [189](p.129) 2D 디스크 보정 마찰이 0.92–1.04 로
  *"relatively high"* 인데, 리뷰의 해설이 *"To account for the particle shape, the sliding friction coefficient
  would have to be increased and would most probably be **higher than the value measured between two
  physical particles** [139]"* — **보정값이 실측 물성에서 벗어나는 것을 형상 결손 보상으로 정당화**하는 논리.
- 🔑 **강성에 대한 유일한 물리 기전 단서**(§8 future work, p.136): **Van Lew et al. [236]** —
  세라믹 펠릿 42개의 영률을 개별 측정(Hertz 가정 하중-변위 피팅)해 **Weibull 분포**를 얻고 DEM 단축압축에
  투입: *"the sample with a distribution in Young's modulus showed a **softer response** compared to the
  sample with a constant Young's modulus"* (+ meso 스케일에서 파단 입자 비율이 **더 낮았다**).
  같은 방향의 두 번째 사례가 **Molenda et al. [230]**(p.136): 마찰계수에 분포를 주면 응력-변형 응답이
  **더 무르고**(asymptote 도달 변형 0.003 → 0.03) 평균은 같다.
  ⇒ **"불균질성 → 거시적으로 더 무름"** 은 리뷰가 두 독립 사례로 기록한 방향이다.  단일 유효 E 로 럼핑하면
  그 유효값은 재료 E 보다 **낮아야** 한다는 *방향*의 문헌 근거.  ⚠ **크기(배수)는 n/a** — 두 논문 모두 배수 미보고.
  ⚠⚠ **2026-08-25 — Van Lew [236] 1차 출처 대조 완료.  위 요약(= 리뷰가 전한 그대로)에 4건의 드리프트가 있다.**
  정본 = **`vanlew2015_modifying_youngs_modulus_distribution.md` §9-c**.  요지만:
  ① 인용문은 **Van Lew 원문에 없다**(Coetzee 의 패러프레이즈) → **Van Lew 직접인용 금지**, 원문 대응은
     *"beds with **smaller** Young's modulus … are more compliant"* = **평균** 얘기.
  ② **"불균질 → 무름" 을 Van Lew 는 지지하지 않는다** — 그의 분포 침대는 **평균도 1.84× 낮고
     상수-Ē 통제군이 없다** ⇒ 분포 효과와 평균 효과 **분리 불가**.
  ③ **"세라믹 펠릿 42개"** → **pebble(구)** 이고 **pellet 은 기준값의 형태**(뒤바뀜); 42 = **Li₂TiO₃** 배치이며
     **DEM 에 들어간 것은 Li₄SiO₄ 31개**(그 분포는 논문에 **미게재**).
  ④ **"Weibull"** 은 사실이나 **Fig 2b 부캡션 1회·모수 0개**이고 본문은 "discrete/experimental",
     Fig 4 캡션은 "Gaussian" = **한 논문이 세 이름**.
  ⑤ **"파단 입자 비율이 더 낮았다"** 는 **원문 자신의 과장** — Table 1 의 짝 3쌍 중 **1쌍이 반대**다.
  ★ 반대로 **"배수 n/a" 는 상향 정정**된다: Van Lew 는 90 GPa 와 49 GPa 를 **둘 다 stated** 로 주므로
     **평균 연화 1.84×** 가 산술로 나온다 — 그리고 그것이 **우리 18× 의 1/10** 임을 정량한다.
  ⚠ **Molenda [230] 은 여전히 배수 미보고**이므로 그쪽에 대한 "n/a" 는 유효하다.
  ⚠ 이 리뷰 자체의 책임은 아니다 — §13 이 이미 *"절대값을 원고에 쓰려면 **1차 출처 확인이 필수**"* 라고
     적어 두었고, 이 대조가 정확히 그 규율의 실행 결과다.
- ★ 반대 방향 경고 1건 — **Ng & Asce [193]**(삼축, p.130): 입자 강성을 아주 넓게 바꿔도 **초기 벌크 영률과
  체적변형이 유의하게 안 변했다**.  기전: *"**Decreasing the particle stiffness resulted in a higher coordination
  number** and these two effects balanced each other in such a way that the bulk elastic modulus remained
  mostly unchanged."*  ⇒ **강성을 낮추면 배위수가 올라간다** = 역학은 상쇄될 수 있어도 **접촉망은 바뀐다**
  (우리 전달 σ 에 직결 — §13-W4).

---

### Q3. 보정된 값을 논문에 어떻게 표기·출처 표시하라고 하는가?

**⚠ 리뷰는 "표를 이렇게 나눠라"는 명시적 서식 처방을 주지 않는다 → 그 부분은 `n/a`.**
대신 **결손을 결함으로 지적**하는 형태로 규범을 세운다(§1, p.105):

> *"In the literature, **parameters are often not measured and the values are assumed without
> justification** [22]. **How the parameter values were obtained is often not mentioned and whether they
> were measured or calibrated is not clear.** Together with this, **the final simulation is often not
> validated** [61]."*

여기서 도출되는(리뷰가 실제로 요구하는) 보고 규약 4가지:

| # | 요구 | 근거 |
|---|---|---|
| ①| **각 값이 measured / calibrated / assumed-from-literature 중 무엇인지 명시** | §1 p.105 (위 인용) |
| ②| **물성(material property) 과 모델 파라미터(model parameter) 를 분리 표기** — 특히 macro 는 입력이 될 수 없음 | §1 p.105 |
| ③| **코드와 접촉모델을 함께 명시** (값이 그것에 종속) | §1 p.105 *"code dependent"* · §4 p.121 *"one should take care when a set of parameter values used in one code is used in another"* · §9 p.138 *"software and contact model dependent"* |
| ④| **검증(validation) 을 따로 보고** — 보정과 검증을 구분 | §1 p.105 · §8 p.136 |

★ **리뷰 자신의 실천 = 사실상의 서식 제안**: 파라미터를 **provenance(출처 방식) 별로 두 표로 나눈다** —
**Table 1 = "Bulk calibration approach for each DEM parameter"**(p.124), **Table 2 = "Direct measuring
approach for each DEM parameter"**(p.134).  즉 *같은 파라미터라도 어떻게 얻었느냐로 표를 가른다*.
⇒ 우리 원고 SI 에 **"source: calibrated / measured / literature"** 열을 붙이는 것은 리뷰 명문 처방은
아니지만 **리뷰의 자기 실천과 §1 비판에 정확히 부합**한다.  "리뷰가 그렇게 하라고 했다"고 쓰지 말고
**"리뷰가 그 정보의 부재를 문헌의 결함으로 지목한다"**고 쓰는 것이 정확하다.

또한 §4 (p.122) 의 **네이밍 경고**는 우리 표에 그대로 적용된다:
> *"In some codes the particle (and wall) stiffness is specified while in other codes the **contact
> stiffness** is specified. If the particle stiffness is specified, the contact stiffness is calculated
> (at run time) as **two springs in series**, i.e., if the two particles in contact have the same
> stiffness, the contact stiffness would be **half** of that."*
⇒ `E_eff = 1.35 GPa` 이 **입자(재료) 입력값**인지 **접촉 유효값**인지 표에 못 박아야 한다.
(우리 LIGGGHTS 입력은 재료 `youngsModulus` = 입자값이고, 접촉 E* 는 런타임 조합값.)

---

### Q4. ★★ 비유일성(non-uniqueness) — 리뷰가 다루는가?  → **정면으로, 두 번, 그리고 처방까지.**

**진술 ①** (§2, p.106):
> *"A potential problem with this approach is that **the bulk response of the numerical experiment can be
> influenced by more than one parameter. This means that there is no unique solution since more than one
> combination of the parameter values will result in the same bulk behaviour.** If this is the case,
> **there is no guarantee that once the material is calibrated for one application it will be accurate for
> another.** Also, the DEM models were developed by giving physical meaning to the parameters, but if this
> approach is followed, **the physical meaning of the parameters might be lost to some degree** [61]."*

**진술 ② + 처방** (§5, p.123):
> *"The disadvantage of this method is that it is possible that more than one set of parameter values
> will produce the same bulk response for a given experiment [156]. **To prevent this, more than one
> experiment should be conducted and each experiment should isolate a single parameter for which the
> value can then be determined [68,157], or the combined results from more than one experiment should
> provide a unique set of parameter values.**"*
> *"It is also possible that when the parameters are calibrated using a specific experiment that the same
> parameter set used to model another experiment or application might not result in the correct bulk
> behaviour [158], i.e. **the experiment was calibrated and not the material**."*  ★

#### 처방 A — "실험마다 파라미터 하나를 고립"  (순차 보정)
- **Coetzee et al. [25,26,28,62,201,202]** (§5.5 p.131, 리뷰 저자 본인):
  형상·크기(클럼프) 확정 → particle–wall 마찰 **직접측정**(경사판) → 입자 밀도 ← 박스충전 벌크밀도
  (선형관계, 3–4회 반복이면 수렴) → **입자 강성 ← 구속 단축압축**(마찰 무영향 = 고립) →
  particle–particle 마찰 ← 직접전단 벌크마찰각(비선형·고마찰서 포화, Fig 32).
  ⚠ 리뷰가 스스로 단 단서: 마찰계수는 벌크밀도에도 영향을 주므로 [203,187] **마찰 보정 후 밀도를 재보정**해야 한다.
- **Belheine [194] / Salot [195] / Lee [188]**: 위 Q2(a) 의 순서들.

#### 처방 B — "여러 실험의 교집합"  (등고선 교차)
- **Combarros et al. [156]** (§5.2 p.125): 동적 안식각(회전드럼)만으로는 (슬라이딩, rolling) 쌍이 **유일하지
  않다** → 정적 안식각도 모델링 → 두 다항식 = 미지수 2개 방정식 2개 → **유일해**.  분리(segregation) 모델로 검증 성공.
- **Derakhshani et al. [171]** (§5.2 p.125, **Fig 24·25**): 모래시계 실험 하나에서 **두 관측량**(정적 안식각
  **41.57°**, 배출시간 **6.56 s**) → 각각 (μ_slide, μ_roll) 평면의 등고선 → **두 등고선의 교점 = 유일한 파라미터 쌍**.
  후속 [174]에서 공기(CFD-DEM)를 넣으면 μ_slide 0.52 → **0.49**(μ_roll 0.3 불변) = 공기 무시 오차는 작다.
- **Li et al. [175]** (§5.2 p.126, **Fig 26·27**): 안식각 vs 슬라이딩마찰 곡선에 실험값을 수평선으로 그으면
  **여러 조합이 교차** → 배출시간 곡선을 겹쳐 공통 집합을 취함.  고로 장입 공정으로 검증.
- **Markauskas & Kacianauskas [95]**: 같은 절차, rolling 은 {0.0, 0.3} 두 값만.

#### 실패 사례 — 리뷰가 드는 반례
- **Marigo et al. [61]** (§5.2 p.126): 모래파일 시험의 **두 측정량(파일 높이·각도)** 으로 **6개 파라미터**를
  최적화 → *"an **inherently ill-posed problem** with multiple combinations of parameter values providing an
  equally good fit"*.  세 개의 파라미터 집합이 모두 허용범위였고, 그중 하나로 회전드럼을 예측하니 정성적으로만
  맞았다 ⇒ *"the sand pile test was **not adequate** for rotating drum parameter calibration"*.
- **Simons et al. [68]** (§5.4 p.130): Schulze 링전단 결과가 **여러 파라미터에 동시 의존** →
  *"can therefore **not be used as a stand-alone calibration test**"*.  강성은 다른 시험으로 정하거나
  계산시간 최소화로 고르라고 제안.
- **Huang & Tutumluer [108]** (§5.4 p.130): 전단상자로 마찰·강성 **둘을** trial-and-error 로 맞췄다는데
  방법이 불명 — 리뷰의 비판: *"several authors [62,145,156,171,175] found that **a single experiment was not
  sufficient to find a unique set of values for two or more parameters**."*
- **Coetzee [62]** (§5.5 p.131): **전단시험과 안식각시험이 서로 다른 μ_pp 를 준다.** 안식각은 더 낮은
  마찰에서 이미 포화(Fig 33)하므로 마찰이 큰 재료에서는 **직접전단을 쓰라**(안식각으로 보정하면 μ 가 너무 낮게 나옴).
  **Härtl & Ooi [198]** 도 같은 것을 관측(Fig 34, p.132): μ > 0.3 에서 직접전단이 안식각·회전드럼보다 **높은**
  벌크마찰을 준다(강체 전단상자의 구속효과 추정).
  ⇒ **"어느 시험으로 보정했는가"가 값을 바꾼다** = 비유일성의 실험적 얼굴.

#### 처방 C — 계산 비용을 줄이는 탐색 기법 (§5.6, p.132–133)
- **Benvenuti et al. [158,212]**: 안식각 + 직접전단 DEM 결과로 **ANN**(feed-forward, backprop) 학습 →
  파라미터↔벌크 응답의 일반 사상 → DEM 실행 횟수 감소.  리뷰의 문제 규정: 순수 forward 반복은
  *"limited by the **multi-dimensionality of the parameter space**"*.
- **Rackl et al. [139,213]**: **Latin hypercube sampling + Kriging(DACE)** → 다목적 최적화 → 실제 DEM 재최적화 →
  실험 대조 정련.  **안정 타임스텝을 비용 기준으로 최적화에 포함** ⇒ 정확한 파라미터 **동시에 최대 타임스텝**.
  실측: 밀도 + μ_pp **2개 보정에 DEM 38회**.
- **Wilkinson et al. [214]**: Freeman 레오미터 5개 파라미터(E, COR, 슬라이딩·rolling 마찰, cohesion energy
  density) × 3수준의 **부분요인설계** — full **35**회 vs half **18**회 vs quarter **10**회
  (⚠ 본문 표기 그대로 옮김; "35"는 3⁵=243 의 조판 손실 가능성이 있으나 원문 확인 불가 → **as printed**).
  결론: 축소설계도 주효과는 잡으나 **2차 효과 해석에 주의**.
- **Yan et al. [180]**: *"a parametric study without using a **robust statistical approach** could result in
  major complications."*

---

### Q5. 검증 규약 — 보정에 쓴 시험과 *다른* 시험으로 검증하라는 권고가 있는가?  → **있다. 두 겹으로.**

**규약 ① — 검증시험은 보정시험과 달라야 한다** (§2, p.106):
> *"**It is also important that the calibration experiment is different from the final experiment or
> application being modelled. If the final application is used to calibrate the parameter values, the
> exercise is nothing more than a parameter sensitivity study** and would not help the engineer in
> designing a new system for which the material behaviour should be predicted."*

**규약 ②(더 강함) — 검증시험은 그 파라미터에 *민감*해야 한다** (§5.2, p.125, Derakhshani 비판):
> *"However, **the validation experiment was very similar to the calibration experiment.** In both
> experiments an angle of repose was measured. **It would be better to perform a validation experiment
> totally different from the calibration experiment** because if it is very similar, the mechanisms
> involved would be similar and one would expect good results. Also, **a parameter sensitivity study was
> not performed on the validation experiment** to determine exactly how sensitive it was to the parameters
> under investigation. … **This would indicate that the validation experiment was not suitable to
> determine the accuracy with which the parameter values were calibrated.**"*
> 대비 사례: *"Coetzee [62] for example indicated that **the discharge rate of a hopper used for validation
> was sensitive to the particle-particle friction coefficient and therefore a good validation** of the
> calibration process."*

**규약 ③ — 검증 채널의 허용 범위** (§8, p.136):
> *"In general, **all calibration methods should be thoroughly validated by comparing the results to either
> experimental measurements and observations, analytical results, or results from other numerical
> analyses.**"*
⇒ **"다른 수치해석과의 대조"도 리뷰가 인정하는 검증 채널**이다 (우리 DEM↔MPM 교차검증이 여기 해당).
⚠ 단 우리 frame[4] 는 이보다 **엄격**하다 — 서로에게 맞추는 것(cross-fit)은 금지하고, 각자 실험에 보정한
뒤의 **일치만** 증거로 센다.  리뷰의 §8 문장을 "MPM 이 검증이다"로 쓰되, **cross-fit 금지 조건**을 반드시 병기할 것.

**반례(전이 실패) 2건** — 검증이 왜 필요한지:
- **Marigo [61]**: 모래파일로 보정 → 회전드럼 예측 실패(정성적만).
- **Santos et al. [170]** (§5.2 p.125): 유리구슬·쌀알을 회전드럼 동적 안식각으로 보정하고 **다른 드럼 직경·
  길이·충전율·회전속도**로 검증 → 쌀알은 성공, **유리구슬(구형)은 실패**.
  결론: *"for **spherical** particles, in contrast to irregular shaped particles, **the parameter values should
  be calibrated to specific conditions and cannot be generalised. This will however make it very difficult
  to use DEM as a predictive tool.**"*  ★★ **우리는 구를 쓴다 — §13-W5 참조.**
- ⚠ 반대 의견도 기록됨: *"In general **Marigo et al. [61] question the appropriateness of using a calibration
  experiment which is different from the final application**"* (§5.2 p.126).  즉 "달라야 한다"가 **만장일치는 아니다**.

---

### Q6. ⚠ 압력 범위 — 이 리뷰의 응력영역과 우리 300 MPa 의 거리

**(a) 리뷰는 응력 크기를 거의 명시하지 않는다.**
본문 전체에서 벌크 시험의 적용 응력을 수치로 준 곳은 **사실상 없다**
(`kPa` 0회 — 유일한 매치는 오탐, 응용 응력의 `MPa` 표기도 없음; 검색된 "MPa" 는 대부분 "co**mpa**red" 오탐이고,
실제 물리량은 **Xu et al. [234] 의 E = 70 MPa vs 70 GPa** 하나뿐인데 그것은 **응력이 아니라 강성**이다).
⇒ **"<10 kPa 수준"은 이 논문의 stated 수치가 아니다.** 응용 목록(중력 배출 호퍼·사일로, 컨베이어 낙하,
토양-공구 견인, 회전드럼, 밀, 애벌런치)에서 **추론**되는 규모일 뿐이므로, 인용할 때는
**"리뷰가 다루는 응용은 중력·핸들링 스케일이며 응력 크기는 명시되지 않았다"**로 쓸 것.
(정량 앵커가 필요하면 리뷰가 아니라 1차 출처의 삼축 구속압·전단 수직응력을 직접 인용해야 한다.)

**(b) 그러나 리뷰는 "파라미터가 응력 의존이다"를 두 번, 명시적으로 규정한다** — 이것이 Q6 의 진짜 답이다.

> **Li et al. [189]** (§5.3, p.129): *"The results also indicated an **increase in contact stiffness and
> friction coefficient with an increase in the confining pressure**. This again emphasises the fact that
> **the parameter and property values are stress dependent and the stress levels used in the calibration
> experiment should be carefully selected.**"*

> **Franco et al. [196]** (§5.4, p.130): *"They showed that **the bulk friction was a function of the applied
> normal stress** on the specimen. **This makes it important to perform the shear tests (both experimentally
> and numerically) in the range of normal stresses expected in the final application being analysed** [189]."*

> **Suhr & Six [237]** (§8, p.136): 접촉 법선응력에 **의존하는** 접선 마찰계수를 구현 — 한 쌍 구(paired
> spheres)에서는 **상수 마찰 모델이 나쁘고 응력의존 모델이 좋았다**.

**(c) 결론 — 우리에게 갖는 함의 (양날)**

| | 판정 |
|---|---|
| **방법론 전이** | ✅ 가능.  "역보정은 정당하다", "실험을 두 개 이상 써라", "다른 시험으로 검증하라", "provenance 를 적어라" 는 **응력영역과 무관한 인식론**이다. |
| **파라미터 전이** | ⛔ **금지.**  리뷰가 스스로 응력의존을 규정하므로, 이 리뷰 안의 어떤 μ·E·COR 값도 300 MPa 냉간압축에 옮길 수 없다. |
| **가드레일 전이** | ⛔ 오버랩 0.1–4 % 규칙(§7)은 **저응력·자유유동** 계에서 "강성을 낮춰도 벌크가 안 변한다"를 보장하려는 기준.  고압 치밀화에는 그대로 안 걸린다.  ★ 오히려 **Paulick [235]** 가 *"the **denser** the system, the **more important** the stiffness value becomes"* 라고 적었으므로, **300 MPa 로 잼된 침대에서 E 는 최대 민감 파라미터**라는 방향만 전이된다 (= 우리 MPM 의 *"E 가 지배 레버, σ_y 아님"* 관측과 부호 일치). |
| **우리 실천 점수** | ✅ 우리는 **300 MPa 에서 보정하고 300 MPa 에서 쓴다** = Li[189]/Franco[196] 요구를 정확히 충족.  ⚠ 단 다압력(100/200/300/600)으로 확장하는 순간 같은 규칙이 우리를 문다 (§13-W7). |

---

### Q7. 표준 벌크 시험 목록 — 그리고 우리가 이미 하는 것

**Table 1 (p.124) 의 행 = 리뷰가 인정한 벌크 보정 시험 카탈로그**

| # | 시험 | 주로 보정하는 파라미터 | 우리 보유? |
|---|---|---|---|
| 1 | **Penetration test** (평판·30°/90° 쐐기·원판·원뿔·로드) | 강성, μ_pp, μ_roll | ❌ (MPM 관입은 미보유) |
| 2 | **Direct / ring shear test** (벌크 마찰각) | **강성**, μ_pp, μ_pw, μ_roll | ❌ 실험 미보유 · 🔶 시뮬 측 force-chain/전단 정보는 있음 |
| 3 | Direct shear (**angle of dilatancy**) | μ_pp | ❌ |
| 4 | **Uniaxial compression test (bulk stiffness)** = Table 3 의 `Confined bulk stiffness (oedometer)` | **접촉강성 단독** | ✅✅ **우리 냉간압축이 정확히 이것** (목표만 벌크강성이 아니라 **porosity**) |
| 5 | Static angle of repose / slump / swing-arm slump / pile formation | 밀도, μ_pp, μ_pw, μ_roll | ❌ |
| 6 | Dynamic angle of repose (rotating drum) | μ_pp, μ_pw, damping | ❌ |
| 7 | Hopper / silo discharge time·rate | 강성, μ_pp, μ_pw, μ_roll | ❌ |
| 8 | Hopper / silo discharge **velocity profile** | 강성, μ_pp, μ_pw | ❌ |
| 9 | **Box fill (bulk density)** | **입자 밀도** | ✅ (우리는 ρ 를 재료 실측값으로 고정 = 보정 안 함) |
| 10 | **Triaxial / biaxial** (하중-변위, 체적변형) | 강성, 강성비, μ_pp, μ_roll, damping, cohesion | ❌ |
| 11 | Soil-tool interaction (draught force) | 강성, μ, bond | ❌ |
| 12 | In-situ ring shear & vane tester | μ_pp, bond 강도, 강성 | ❌ |
| 13 | ANN(안식각+전단) | 다수 동시 | ❌ (우리는 대신 **스케일링법칙 + LOOCV** 를 별도 축에서 운용) |
| + | (§5.6) **Freeman FT4 레오미터** [214,215] | 슬라이딩·rolling 마찰 | ❌ |
| + | (§5.5) **Drop test of a whole assembly** [211] | **접촉 damping(COR)** — 6000구 낙하 후 최종 높이 정합 | ❌ |
| + | (§5.2) **Quist & Evertsson 장치** [67] (Fig 30) | 다목적 최적화용 통합 장치 | ❌ |
| + | (§5.2) **Roessler & Katterfeld "shear box"/slope-angle** [133] (Fig 28) | 안식각 — **크기 스케일 불변**이 검증된 유일 변형 | ❌ |

⚠ **Heckel 은 이 리뷰에 없다** (`Heckel` 0회).  압밀 곡선을 통한 강성/항복 보정은 **금속·의약 분말압축
문헌의 관행이지 이 리뷰의 카탈로그에는 부재**하다.  ⇒ 우리의 Heckel 선형성 R²=0.965 / P_y=138 MPa 은
**이 리뷰가 승인하는 표준 시험이 아니라 우리가 추가로 가져온 축**이다.  "Coetzee 리뷰가 Heckel 을
표준으로 든다"고 쓰면 **날조**다.

**우리가 이미 하고 있는 것 = 4번(구속 단축압축) 하나 + 9번을 보정 없이 고정.**
나머지 12개 시험은 전부 미보유 ⇒ **리뷰 기준 "여러 실험의 교집합"(처방 B)을 만들 재료가 현재 없다.**

---

## 6. 섹션별 상세 (읽은 그대로)

### §1 Introduction (p.105)
- DEM 은 벌크재 취급 설계의 주력 도구; FEM/메쉬프리는 대변형·혼합·분리에 약함; CFD·LBM 과 결합해 유체-입자.
- **Marigo et al. [61]**: *"the main difficulty for the industrial application of DEM is related to the
  **calibration of the input parameters**."*
- *"In some cases **the calibration of the bulk material can be the largest component of a DEM simulation
  project**."*
- 물성 vs 모델 파라미터 구분(§4.1 위 인용), macro 는 입력 불가, 코드 의존성.

### §2 Overview of calibration approaches (p.105–106)
위 §4 전문.  두 접근의 명명·장단점·비유일성·"보정시험은 응용과 달라야 함"이 전부 여기.

### §3.1 Particle shape (p.106–114) — 전체의 1/4
- **구 입자의 근본 결함**: *"when using spherical particles, **the bulk (internal) friction or shear strength
  of the assembly is usually too low** when compared to real granular material [76]."*
  대책 = 비구형 입자 **또는** rolling friction.  둘은 **등가가 아니다**:
  **Zhou et al. [79]** — 원판+rolling 과 클럼프(무rolling)는 벌크 전단강도·dilatancy 를 둘 다 올리지만
  **국소화 패턴이 근본적으로 다르다**(원판은 뚜렷한 전단띠, 클럼프는 균일 국소화) ⇒
  *"circular particles with rolling friction **could not replace the particle shape effects** as modelled
  by the clumps."*
- **회전 완전 봉쇄**(rotational freedom fixed) [80,81] 도 쓰이나, 순수전단 대변형에선 무리이고
  **dilatancy 를 제어할 파라미터가 사라진다** [76]; Obermayr [83] 은 미시적 충실도(전단띠)는 잃되
  벌크는 현실적일 수 있다고 봄.
- **비용**: 비구형 2–3× (최대 10×) [4]; 타원체 클럼프 4.1× [86].
- **Stahl & Konietzky [87]**: *입자 크기·형상·상대밀도를 현실적으로 모델링하면* 조립 비점착재의 보정은
  **법선강성·전단강성·마찰계수 3개**로 줄어든다.
- 형상 모델: clump(다구), polyhedra, ellipsoid, superquadric, superellipsoid.  clump 가 최다.
  클럼프 단점 — 필요한 구 개수의 지식 부재 [95], 겹치면 질량·관성 오류 [96](질량은 밀도로 보정 가능 [97],
  관성은 코드가 허용해야 — PFC3D v5 는 가능), 다중접촉 발생 [93,94].
- **Höhner et al. [72,73,113,114]** 계열: 각형성↑ → 질량유량↓; polyhedra 는 funnel flow, clump·구는 mass flow;
  구형도 x = π^(1/3)(6V_p)^(2/3)/A_p (eq 1); 종횡비↑ → 배출률↓, 전단강도↑ (DEM 이 약간 과소).
  형상 근사 **방식**보다 **거시 형상지표(구형도·종횡비)**가 지배.
- **Zhao et al. [118]**(삼축, 무보정): IQ = 36πV²/S²; 내부마찰각 peak **30.8/39/42.6/44.7°** (C-1/2/3/4 클럼프),
  residual **22.7/28/33.6/34.3°** ⇒ *"the internal friction angle of an assembly of clumps is roughly **10°
  higher** than that of spheres."*  ⚠ 리뷰 주석: **같은 파라미터를 모든 형상에 썼으므로 형상 단독 효과가 아님.**
- **§3.1.11 (p.113) 규범 2줄**:
  *"**It is important to include the modelled particle shape in the calibration process** since it will
  influence most of the bulk material properties. Also, during the calibration process **the particle shape
  (together with the size) needs to be determined first because, if it is changed later the model parameters
  will have to be re-calibrated** to take the change in shape into account."*
  실증: **Markauskas et al. [77]** 클럼프 구 개수를 바꿀 때마다 μ_pp 재보정 필요;
  **Grima & Wypych [129]** Particle B→C 로 바꾸니 rolling friction 을 0.2→0.01 로 재조정해야 함.
- ★ **Coetzee [62]** (p.113): 클럼프 2·4·8구를 **각각 독립 보정**하니 셋 다 앵커 인발력·호퍼 배출을 정확히 예측.
  그러나 *"**Spherical particles without rolling friction** were also used, but **could not be calibrated**
  due to the low level of interlocking and hence shear resistance, **even when high particle friction
  coefficients were used.**"*  ★★ **구+무rolling 의 원리적 한계 — 우리 §13-W5.**

### §3.2 Particle size (p.114–121)
- 실제 입자 수는 10⁹–10¹² 규모 → 크기 스케일업이 불가피.  **크기 스케일업 시 벌크 보정을 쓰라**(p.115).
- **§3.2.2 스케일링 법칙**:
  - **Feng et al. [125]**: F_n = k r^a δ^b 형태에서 스케일 불변 조건 **a + b = n_d − 1** (2D: n_d=2, 3D: n_d=3).
    ⇒ **선형 접촉법칙은 2D 에서만 스케일 불변, 3D 에선 아니다.**
    ⚠ **리뷰 본문의 내부 모순 1건**: 바로 다음 문장이 *"In 3D, the particle or contact stiffness should be
    scaled with a factor **inversely proportional** to the particle size scaling factor"* 라고 적는데,
    두 문단 뒤 **Thakur et al. [135]** 요약은 *"the contact normal stiffness should **scale linearly with
    the particle radius**"* 다.  선형법칙(a=0,b=1)에서 a+b=2 를 만들려면 k ∝ r 이어야 하므로 **Thakur 판
    ("비례")이 자기일관적**이고 "inversely" 는 오기로 보인다.  **인용 시 Thakur 판을 쓸 것.**
  - 기하·역학·동역학 **3 상사** 중, 스케일 불변 접촉법칙을 쓰면 역학·동역학은 유지되나 **기하 상사는
    입자 수를 같게 유지할 때만** 성립.  도메인을 안 줄이고 입자만 키우면 기하 상사가 깨져 오차 유입.
  - **Obermayr et al. [35]**: Hertz(a=1/2, b=3/2 → a+b=2)는 **3D 스케일 불변** — r 3→30 mm 삼축으로 확인.
  - **Thakur et al. [135]**: 접선강성도 법선과 같은 방식으로; **공극률을 같게 유지하면 입자 밀도는 스케일하지 말 것**
    (중력 위치에너지 밀도 보존).
- **스케일업 한계 실측**(1차 출처 stated):
  | 출처 | 계 | 결과 |
  |---|---|---|
  | Shigeto [141] | 스크류 컨베이어 | ×4 스케일업이 유량에 영향 없음 (유동이 강제되는 계) |
  | Grima & Wypych [13,37] | 컨베이어 충돌판 | 구 vs 2구 클럼프 충돌력 차 **3.1 %**; **×1.23 무해**, **×2–3 부터 결과 달라짐** |
  | Xie et al. [143] | 슈트 마모 | 4 mm 정확 · **8 mm(×2) 는 최대 충돌력 2배**, 구조설계·마모 예측엔 부적합 |
  | Grima & Wypych [145] | 세탄 배출 호퍼 | ×4 + 클럼프 + rolling → **배출시간 10 % 이내** ✅ |
  | Combarros Garcia [146] | 분리(2종 모래) | 둘 다 ×5(크기비 6 유지) → 분리 소폭 과소(형상·PSD 미반영) |
  | Ucgul et al. [136] | 경운 공구 | 입자 반지름↑ 시 **rolling·sliding 마찰을 2차식(quadratic)으로 올려야** 같은 벌크 |
  | Salazar [147] | 직접전단(모래, parallel gradation) | ×2 = 응력·체적 거의 동일, **20× 빠름** ✅ / ×4 = 응력 다소 높고 요동 큼, 200× 빠르나 **비권장** |
  | Cleary et al. [31] | Isamill | 9·15 mm 유동 유사, **25 mm 는 과대** |
  | Mollon et al. [34] | 암석 애벌런치 | 평면 사면은 크기 무관, **굴곡 사면은 크기 강한 영향** |
- **비용 절감 기법**: Servin & Wang [148] 강체 집합체 치환(**5–50×**), Cleary [30] 멀티스케일(거시 밀 + 국소
  전단셀, 1-way), McDowell [96] 입자 리파인먼트(6/9/12 mm 3층, 90°→30° 섹터), [150] **모든 입자에 같은 질량**
  부여(준정적) → **2.3×**.

### §4 Contact models and naming convention (p.121–123)
- 선형 spring-dashpot: F_n = k_n δ_n (절대), F_t 는 **증분** 갱신, Coulomb 절단 F_t ≤ μF_n,
  c_n = 2β_n√(m_c k_n), m_c = m₁m₂/(m₁+m₂).  ⚠ *"The tangential contact model is implemented differently
  in different codes. Some codes include only the linear spring force to determine the limiting sliding
  force, while others use the combination of spring force and damper force [92,135]."*
- Hertz–Mindlin: F_n = k_n δ_n^{3/2}, **k_n = (4/3)E*√R***, **k_t = 8G*√(R*δ_n)**,
  E* = [(1−ν_i²)/E_i + (1−ν_j²)/E_j]⁻¹, 감쇠 F_d = c δ̇ δ^{1/4},
  c = ln e/√(ln²e + π²) · √(m*k).
- **접촉모델 간 비교는 매우 드물다** — 리뷰가 든 전부:
  - **Ucgul et al. [136]**: Hertz vs **Walton & Braun 이력(hysteretic) spring 모델** [154] →
    **이력 모델이 토양-공구에서 더 정확**.  ★ 리뷰 전체에서 이력 모델이 등장하는 **유일한** 자리이고,
    그 한 번의 대결에서 **이력 모델이 이겼다** (우리 LIGGGHTS `hooke/hysteresis` 와 같은 계열).
  - **Grima & Wypych [37]**: 선형 vs Hertz–Mindlin → **거시/벌크 수준 유의차 없음**.
  - **Gröger & Katterfeld [3]**: 실물도 모델도 구면 → Hertz 적절; 복잡 형상(클럼프 포함)이면 **접촉 파라미터를 보정해야**.
  - **Boac et al. [19]**: 곡물 취급에서 선형·비선형 둘 다 효과적으로 사용됨.
- **네이밍 규약**(우리 표기에 직결): 이 문서에서 *Young's modulus / modulus of elasticity / shear modulus /
  particle stiffness / wall stiffness* 는 **전부 접촉강성과 관련된 것**으로 취급; rolling resistance =
  rolling friction; COR ↔ 감쇠계수는 서로 직결; sliding 을 생략하면 sliding friction 을 뜻함;
  bulk friction = internal friction (angle) = shear strength.
  **입자강성 지정 코드 vs 접촉강성 지정 코드**의 차이(직렬 두 스프링 → 절반) 는 §5-Q3 참조.

### §5 Bulk calibration approaches (p.123–133)
- 5.1 In-situ·토양-공구: Asaf [22](3 관입공구 면적차 최소화 + 초기추정용 에너지법, grouser 전단으로 검증),
  Ucgul [136,162](안식각으로 정성 보정 + 원판·30°원뿔 관입의 누적에너지-깊이 곡선으로 정량 보정),
  Milkevych [163](비틀림 전단상자 + 베인, 민감도 미제시), Mak [38]/Li [166](**강성만** 보정, McKyes 식과 대조),
  Hess [167](입자군집최적화 PSO, 세부 미공개).
- 5.2 안식각·호퍼: 위 Q4·Q5 전문.  추가로 —
  **Yan et al. [180]** 대규모 민감도(순수 수치): **E 0.02→200 GPa 거시량 무영향**; COR 0–0.45 무영향,
  0.85까지 소폭; 마찰이 낮으면 rolling 효과 미미, 높으면 유의 ⇒ **rolling 은 sliding 에 대해 2차**;
  유량은 sliding 에 더 민감.
  **Wensrich & Katterfeld [84]**: 낮은 sliding 에서 안식각은 rolling 변화에 둔감, 역도 성립
  (⚠ Yan 과 한 지점에서 **불일치** — 리뷰가 명시).
  **Roessler & Katterfeld [133]**: 안식각이 **용기 인양속도의 함수**(빨라지면 감소, 100 mm/s 이상 포화);
  실린더 인양식 안식각은 **저속(2 mm/s, 준정적)에서만 크기 불변**, 16 mm/s 동적조건에선 아님;
  **shear-box(벽 제거) 슬로프각 시험은 크기 독립**(Fig 28).
  **Grima·Wypych·Hastie [181,182]**: 세 가지 파일형성(인양 슬럼프 / 부어내림 / **swing-arm slump**, Fig 29)이
  **서로 다른 파일 프로필**을 준다(상대 입자속도가 달라서) ⇒ *"the parameter values were application and
  conditions dependent"*.  **파일 높이는 rolling 에, 안식각은 sliding 에 가장 민감**; **COR 은 파일 프로필에
  유의 영향 없음** ⇒ 이 시험으로 COR 보정 불가.
  **입자 개수 영향**: Coetzee [62] 1500 vs 3000 무차; Stahl & Konietzky [87] 4 kg→3 kg 에서 안식각 **2° 감소**(실험 확인).
- 5.3 삼축·이축: **Plassiard & Belheine [76]** 강성↑ → 벌크 E ↑(멱법칙), ν 는 어느 지점까지 감소 후 불변;
  전단강성만 ↑ → E 거의 선형↑, ν 거의 선형↓.
  **Marczewska et al. [190]**(Fig 31): 낮은 강성 구간에서만 E ↑, 높은 강성에선 포화; 강성↑ → **수축(contraction)
  단계가 짧아짐**; 강성비(t/n)↑ → E ↑, ν ↓; μ ↑ → E ↑ (μ>0.4 에서 포화), ν ↓ (0.4 이후 불변).
  ⚠ ν 방향이 [76] 과 **상충**(리뷰 명시).
  **Ng & Asce [193]**: 강성·감쇠 **둘 다 무영향**(배위수 상쇄) — 위 Q2(c).
  **Mohammed et al. [192]**: rolling 은 초기 E·ν 에 무영향이나 **벌크 마찰각·dilation 각을 올리고** 전단띠 형성 촉진.
- 5.4 직접전단: 위 Q4 실패사례.  추가 —
  **Franco [196]**: 벌크마찰이 μ_pp 뿐 아니라 **강성 증가로도 증가**(2D).
  **Keppler et al. [197]**: **강성↑ → 벌크마찰·응집 둘 다 감소** (⚠ [25],[196] 과 **정반대**),
  μ_pp 는 응집에 강한 영향(선형 감소)이나 **벌크마찰엔 거의 무영향** (⚠ [3,25,62,101] 과 정반대).
  **Simons [68]**: E↑ → 전단저항 **선형 증가**; COR 무영향; μ_pp 0.7 까지 증가 후 포화; μ_pw < 0.25 에서만 유효;
  μ_roll(pp) 선형 증가, μ_roll(pw) 무영향.
  **Hart/Härtl & Ooi [126,198]**: μ↑ → 벌크마찰 비선형 증가, μ>1.0 에서 포화; **μ↑ → 배위수 감소**(저마찰서 더 급함);
  **공극률/공극비는 μ↑ 에 따라 증가**하고 초기·최종 모두 점근값에 접근.
  **본드가 있으면 마찰이 무력화**: Sadek [200]·Landry [155] — 결합이 깨져야 마찰이 작동하므로 μ 영향이 사라진다.
- 5.5 Comprehensive: 위 Q4 처방 A.
- 5.6 기타: ANN·Kriging·DoS — 위 Q4 처방 C.

### §6 Direct measuring approaches (p.133–135)
- **Cole et al. [216,217]**: 자연 소립자(파쇄 gneiss·풍화 자갈·석영사·마그네사이트) 접촉 실측 —
  *"the load-displacement behaviour in the contact normal direction was **linear with the onset of loading**
  and exhibited a **transition to the Hertzian 3/2 power law above a threshold normal force**. **The ratio of
  the shear stiffness to the normal stiffness varied from 0.3 to approximately 1.**"*
  ★ 실제 접촉은 저하중에서 **선형**, 고하중에서 Hertz — 교과서 기대와 반대 순서.
- **Senetakis et al. [220]**: 석영사 입자 간 마찰 전용 장치, 변위 1–300 µm, 법선하중 1–15 N →
  **법선력·전단속도가 마찰계수에 유의 영향 없음**.
- **Paulick et al. [219]**: 시험기·압반의 강성/변형을 배제하고 두 구 사이 **접촉강성만** 측정하는 방법.
- 밀도 = **피크노미터**(수중), E = **압축/압입 시험 + Hertz 가정**(ν 는 가정), COR = **낙하시험 + 고속카메라**,
  particle–particle COR = **이중진자**, 마찰 = **경사판**·**전단상자 반쪽을 벽재료로 교체**·**핀-온-디스크 트라이보미터**.
- **Lim [224]**: 무차원 COR ↔ [kg/s] 감쇠계수를 잇는 **master curve** (선형 spring-dashpot + Buckingham Π).
- **Barrios [69]·Just [169]·Ucgul [136,162]**: 위 Q1 논거 3.
  Ucgul 의 rolling 측정법은 리뷰가 *"seems counter-intuitive"* 라 평함(모래 위에서 **강구**를 굴려 얻은 0.05 를
  모래-강철 rolling 으로 사용).

### §7 Reduction in contact stiffness (p.135–136)
위 Q2(b) 표 전문.  밀도 스케일링(density scaling)은 **정적 해에만** 유효하고 동적·중력 하중엔 부정확 [58,92].

### §8 Future work (p.136–137)
- 자연재의 **최소 형상 종수**: Stahl & Konietzky 6종이면 자갈 벌크밀도 양호; Coetzee 10종; 종수↑ → 오차↓.
- **PSD 선택**: Smith et al. [137] — 계산비·재현성·정확도 절충으로 **균등분포 2.5–10 mm** 가 최선,
  범위가 좁아 log-normal 보다 나았다.
- **파라미터의 분포**(위 Q2(c)): Van Lew [236] Weibull-E → 더 무른 응답 · 파단 입자 감소
  — ⚠ **리뷰의 요약이며 1차 출처와 어긋난다** (§Q2(c) 정정 배너 · 정본
  `vanlew2015_modifying_youngs_modulus_distribution.md`): 원문은 **평균 E 도 1.84× 낮춰** 분포 효과를
  분리하지 못하고, **"파단 감소"는 원문 Table 1 이 3쌍 중 1쌍에서 반증**한다;
  Molenda [230] μ 분포 → 더 무른 응답(완두 μ̄ 0.29, sd 0.09);
  Wang [221] E·COR 이 알갱이 형상별로도, **같은 알갱이의 위치별로도** 다름;
  Hastie [223] — 값 하나를 정하기보다 **변동에 대한 민감도 해석**을 하라.
- **응력의존 마찰**: Suhr & Six [237].
- 검증 규범(§8 마지막 문단, Q5 규약 ③).

### §9 Conclusions (p.137–138)
- 형상·크기 분포도 입력 파라미터이며 **모델링은 이 둘의 확정에서 시작해야 한다**.
- *"The most popular method to model particle shape is the use of **clumps** … and **there is no convincing
  evidence that other shape representations outperform clumps** in modelling natural materials."*
- 두 접근 재정의 + 각각의 장단(위 §4.4).

---

## 7. 리뷰가 기록한 "파라미터 ↔ 벌크응답" 관계 지도 (Table 3·4, p.137)

리뷰의 마지막 두 표는 **어떤 미시 파라미터가 어떤 거시량과 관계있는지 조사된 문헌 맵**이다
(⚠ 리뷰 주석: *"Even though a relation might be indicated, it can be that the study found the effect to be
**negligible**."* — 즉 **관계가 조사됐다는 뜻이지 유의하다는 뜻이 아니다**).

| 거시량 | 강성 | 강성비 | μ_pp | μ_pw | rolling | damping | 밀도 |
|---|---|---|---|---|---|---|---|
| Bulk density | ✅[81] | — | ✅ | ✅ | ✅ | ✅ | ✅(다수) |
| Bulk friction (직접/링전단) | ✅(6편) | — | ✅(12편) | ✅ | ✅ | ✅ | ✅[197] |
| Bulk friction (삼축) | ✅ | ✅ | ✅(6편) | — | ✅ | — | — |
| **Bulk Young's modulus (삼축)** | ✅(8편) | ✅(6편) | ✅(5편) | — | ✅ | ✅[193] | ✅[83] |
| **Confined bulk stiffness (oedometer)** | **✅[25,81,125,205]** | — | — | — | — | — | — |
| Dilatancy / porosity (삼축·이축) | ✅(7편) | ✅ | ✅ | — | ✅ | ✅ | ✅ |
| Dilatancy / porosity (직접전단) | ✅[193,204] | — | ✅[62,126,147,198] | — | ✅ | — | — |
| Bulk Poisson's ratio | ✅ | ✅ | ✅ | — | ✅ | — | — |
| Static AoR | ✅[81,180] | — | ✅(18편) | ✅ | ✅(20편) | ✅[180] | ✅[206,213] |
| Dynamic AoR (드럼) | — | — | ✅ | ✅ | — | ✅ | ✅[169] |
| Hopper/silo 배출 | ✅[72,73,180,232] | — | ✅ | ✅ | ✅ | ✅[180] | — |
| Penetrometer 저항 | ✅[22,81,159,161] | — | ✅ | ✅ | — | — | — |
| Silo wall pressure | — | — | ✅[77,179] | — | — | — | — |
| Bulk damping | — | — | — | — | — | ✅[211] | — |

★ **우리에게 중요한 두 줄**:
① `Confined bulk stiffness (oedometer)` 행에서 **관계가 조사된 유일한 파라미터가 접촉강성**
   = **구속압축은 강성을 고립시킨다**는 Q2(a) 주장의 표 형태.
② `Dilatancy/porosity` 행이 **강성과도 관계가 조사됐다** ⇒ 공극률류 거시량으로 강성을 보정하는 것은
   리뷰의 관계 지도 **안에** 있다 (다만 **고압 치밀화가 아니라 전단 dilatancy** 맥락).

---

## 8. Figure set ★ (전 34장이 타 논문 전재 — "우리가 쓸 것"만)

| Fig | 내용 | 우리가 참고할 점 |
|---|---|---|
| 1 | 밸러스트 클럼프 자동생성(평균 8.92 / 35.92 구) [97] | 형상 근사 해상도의 대가 |
| 2 | 파단 가능 asperity 를 붙인 10구 클럼프 [98] | 축소 밸러스트의 구속압 의존 복원 |
| 3 | 종횡비·구 개수별 타원체 클럼프 [86] | **13구면 매끈 타원체에 수렴** |
| 5 | XRT 옥수수 → 5/10/15/20 구 클럼프 [111] | 실물 스캔 → 클럼프 파이프라인 |
| 7 | 실험용 폴리헤드럴 주사위 [72] | "형상을 실물로 만들어 검증"하는 설계 |
| 15·16 | ASG 자동 클럼프 vs 수동 3형상(구·긴형·피라미드) [62] | **자동 ≈ 수동** (성능 유의차 없음) |
| **17** | 세탄 실제 PSD vs DEM **×4 스케일** PSD [145] | 스케일업 보고 양식 (우리는 미해당, 대조군) |
| **18** | **parallel gradation** 스케일 PSD [147] | PSD 를 평행이동해 스케일하는 표준 도식 |
| 19 | 굴착 중 강체 집합체 치환 [148] | 모델 축약(5–50×) |
| 20·21 | 밀 멀티스케일 + 매립 전단셀 [30] | 1-way 스케일 커플링 도식 |
| 22·23 | 원뿔관입 다중 입경층(6/9/12, 2/3/4 mm) [96] | **작은 입자가 큰 입자 공극으로 이주** → 3층 필요 |
| **24** | 안식각 = f(rolling, sliding) **등고선** [171] | **비유일성의 그림 표현** |
| **25** | 안식각 등고선 ∩ 배출시간 등고선 → **교점 = 유일해** [171] | ★★ 처방 B 의 표준 그림 — 우리가 만들어야 할 그림 |
| **26·27** | 안식각·배출시간 vs μ_slide (μ_roll 별 곡선) + 실험 수평선 [175] | **수평선이 여러 곡선을 자른다** = 비유일성 |
| 28 | 벽 제거 슬로프각 시험 4단계 [133] | **크기 스케일 독립**이 검증된 안식각 변형 |
| 29 | swing-arm slump tester [182] | 벽 마찰을 배제한 파일형성 |
| 30 | Quist & Evertsson 통합 보정 장치 [67] | 다목적 최적화용 장치 설계 |
| **31** | 체적변형 vs 축변형, 법선강성별 [190] | **강성↑ → 수축단계 단축**; 포화 존재 |
| **32** | 직접전단 내부마찰각 vs μ_pp, 클럼프 종류별 + 실험 min/avg/max 수평선 [62] | ★ **보정 곡선 + 실험 밴드** 보고 양식 (우리 그림 표준으로 채택 권장) |
| **33** | 안식각 vs μ_pp, 같은 양식 [62] | 안식각은 **더 낮은 μ 에서 포화** |
| **34** | 벌크마찰 vs 입자마찰 — 직접전단(실선) vs 안식각 시험(점선) [198] | ★★ **μ>0.3 에서 두 시험이 갈린다** = "어느 시험으로 보정했나"가 값을 바꾼다 |

⚠ 이 카드의 수치는 **전부 리뷰 본문 stated**(=1차 출처 소환값)이다.  **내가 그림에서 읽은 digitized 값은 0건.**
Fig 24–27·31–34 의 축 위 값이 필요하면 **1차 출처 PDF를 직접 확보해 digitize** 해야 한다.

---

## 9. Post-processing / 방법론 도구 (리뷰가 카탈로그한 것)

- **최적화**: 곡선 간 **면적차 최소화**(Asaf [22], 초기값 민감 → 에너지법으로 초기추정),
  RMS 오차 최소화 + **응답면(response surface)** (Li [189], 7계수 7식),
  **입자군집최적화 PSO**(Hess [167]), 다목적 최적화(Quist [67], Rackl [139]).
- **대리모델**: **ANN** feed-forward/backprop (Benvenuti [158,212]), **Kriging + Latin hypercube (DACE)**
  (Rackl [139,213] — 타임스텝을 비용항으로 포함), **부분요인 DoS**(Wilkinson [214]).
- **보간**: 강성↔벌크강성 **선형 보간**, μ↔벌크마찰 **비선형(포화) 곡선 보간** (Coetzee [25,62]).
- **연립**: 정적+동적 안식각 두 다항식 → 2식 2미지수(Combarros [156]); 등고선 교차(Derakhshani [171]).
- **측정 계측**: PIV(유동장), X-ray CT(패킹), XRT(형상), 고속카메라(COR), 레이저/디지털 영상 세그멘테이션(형상 기술자),
  Fourier descriptor 3D 모래입자 생성(Mollon & Zhao [89]).

---

## 10. 우리 DEM+MPM 대비 — 리뷰 규범 적합성 판정 ★★  →  `our_dem_baseline.md`

### 10.1 우리 절차를 리뷰의 어휘로 다시 쓰면

> 우리는 **Bulk Calibration Approach** 를 쓴다.  시험은 **구속 단축압축(Table 1 #4 / Table 3 oedometer 행)**,
> 벌크 관측량은 **porosity @ 300 MPa**, 보정 파라미터는 **입자 강성 하나(E_eff)**, 실험 앵커는
> **Minnmann pure-SE ~10 %**.  나머지(μ, COR, ν, ρ)는 문헌값 고정 = 리뷰가 말하는
> *"Bulk Calibration Approach is often used in combination with the Direct Measuring Approach"* (§5 p.123).

### 10.2 규범 대조표

| 리뷰의 규범 | 근거 | 우리 현황 | 판정 |
|---|---|---|---|
| 접근을 명명하고 provenance 를 밝힐 것 | §1 p.105 | ✅ 우리는 3층 분리 보고 (real 22–24 / **DEM-eff 1.35** / MPM 1.53) | ✅ **리뷰 기준 이상** |
| 물성 vs 모델 파라미터 구분 | §1 p.105 | ✅ CLAUDE.md frame[2] 가 명시적으로 "연화는 물성이 아니라 결손 럼핑 프록시" | ✅ |
| 코드·접촉모델 명시 | §1 p.105 · §9 p.138 | ✅ LIGGGHTS `hooke/hysteresis` 명시 | ✅ |
| 크기 스케일업 금지/주의 | §3.2 p.114–120 | ✅ **스케일업 안 함** (실측 µm PSD 그대로) | ✅ **강점** — 리뷰 최대 우려원 부재 |
| 형상을 **먼저** 확정하고, 형상을 바꾸면 재보정 | §3.1.11 p.113 | ✅ 구 고정, 이후 안 바꿈 | ✅ (단 §10.3-W5) |
| **보정 응력 = 응용 응력** | §5.3 p.129 · §5.4 p.130 | ✅ 300 MPa 보정 → 300 MPa 사용 | ✅ **강점** |
| 강성은 **구속 단축압축**으로 고립해 보정 | §5.5 p.131 · Table 3 p.137 | ✅ 시험 종류 일치 | ✅ |
| ①실험마다 1 파라미터 고립 **또는** ②≥2 실험 교집합 | §5 p.123 | ⚠ ① 을 **가정**했을 뿐 우리 계에서 확인 안 함; ② 는 재료 없음 | ⚠ **약점 W1** |
| 보정과 **다른 시험**으로 검증 | §2 p.106 · §5.2 p.125 | ⚠ Heckel = 같은 시험 다른 압력; Cronau overlap = 같은 런의 다른 관측량; MPM = 다른 수치해석(§8 허용) | ⚠ **약점 W2** |
| 검증시험이 그 파라미터에 **민감**해야 | §5.2 p.125 | ⚠ 미시연.  사내 관측은 오히려 σ 가 E 에 둔감(1.35 ≡ 1.5) | ⚠ **약점 W2′** |
| 오버랩 가드레일(속도용 감소 시) | §7 p.135–136 | ⚠ 우리는 (b)가 아니라 (a) 이므로 **적용 대상 아님**; 그러나 수치상 20–100× 밖 | ⚠ **고지 필요 W3** |
| 파라미터 분포 고려 | §8 p.136 | ⚠ 단일값 럼핑 (리뷰도 "future work" 로만 다룸) | 🔶 동급 |

### 10.3 ⚠ 우리 취약점 (숨기지 않고 적음)

**W1 — 유일성을 시험한 적이 없다.**
형식적으로는 "1 미지수 = 1 방정식" 이라 유일해 보이지만, 리뷰의 비유일성은 **고정한 파라미터들이 실제로
그 관측량에 무영향인가**의 문제다.  우리가 의지하는 근거는 **Coetzee & Els [25]/[205] 의 "구속 단축압축은
마찰에 둔감"** 인데, 그것은 **파쇄암·옥수수, 저응력, 2D/클럼프** 결과이고 **300 MPa 냉간압축의 LPSCl 구 침대**
에서 재현된 적이 없다.  ⇒ **실행 항목**: E_eff 고정, μ ∈ {0.2, 0.4, 0.6} (그리고 COR ∈ {0.2, 0.4, 0.6}) 로
ε@300 을 재는 **OAT 민감도 1장**.  ∂ε/∂μ ≈ 0 이 나와야 우리 보정이 리뷰 처방 ①을 만족한다고 **주장할 자격**이 생긴다.
(현재는 그 자격이 **없다** — 인용하면 남의 계에서 온 가정이다.)

**W2 — 검증이 보정과 "충분히 다르지" 않다.**
리뷰의 Derakhshani 비판(p.125)이 우리에게 그대로 적용된다.
· **Heckel 4압력**: E_eff 를 300 에서만 맞추고 100/200/600 을 예측으로 냈다면 이는 **같은 시험의 외삽 검증**
  (리뷰 언어로 *"the mechanisms involved would be similar"*) — 없는 것보다 낫지만 "totally different" 는 아니다.
· **Cronau overlap 11–12 %**: 같은 시뮬레이션의 **다른 관측량**이지 다른 시험이 아니다.
· **독립 MPM 이 같은 18× 를 요구**: §8 이 허용하는 *"results from other numerical analyses"* 채널.  ✅ 유효하되
  **frame[4] 조건(서로에게 맞추지 않았음)** 을 문장에 반드시 붙여야 방어된다.
⇒ **가장 리뷰-정합적인 한 수**: 압밀 보정을 **전달 실험**(Bazzoun σ_eff,ion EIS / Minnmann EIS-TLM / Oh bimodal)
으로 검증하는 것 — 메커니즘이 완전히 다르다.
⚠ **그런데 W2′ 가 그걸 막을 수 있다**: 사내 실측이 *"σ_ionic 은 E 가 아니라 porosity 를 따른다"*,
*"E 1.35 ≡ 1.5 는 구조·역학·전달 전 축에서 동일 regime"* 이라고 말한다 ⇒ **σ 는 E_eff 에 둔감** →
리뷰 기준으로는 **부적합한 검증시험**일 수 있다.  먼저 **σ 의 E-민감도**를 재고, 둔감하면 다른 시험을 골라야 한다.
(둔감 자체가 나쁜 건 아니다 — porosity 만 맞으면 σ 가 따라온다는 뜻이므로 오히려 **재파라미터화**로
"E 대신 porosity 를 1차 보정변수로 선언"하는 길이 열린다.  그것이 리뷰 §1 의 "macro 는 입력이 될 수 없다"와
충돌하지 않게 쓰는 방법은 §11-③.)

**W3 — 오버랩이 리뷰의 모든 가드레일 밖이다.**
리뷰의 권고: Cleary **0.1–0.5 %**, Paulick **≤1 % of particle radius**, Höhner **≤4 %**(그 계 한정).
우리 pure-SE 하중지지 침대의 ⟨δ⟩ ≈ **직경의 11–12 %** = **반지름의 22–24 %** ⇒ Paulick 기준의 **~22×**.
· 이 가드레일들은 "**강성을 낮춰도 벌크가 안 변함**"을 보장하려는 것이므로 **우리 목적((a)형 보정)에는
  적용 조건이 아니다.**  방어 논리는 "우리는 §7 을 하고 있지 않다" 이다.
· 그러나 **정직하게 남는 두 결과**: ① 접촉법칙(Hertz/선형) 자신의 소변형 가정 밖에서 운용 중이고,
  ② 그 영역에서 **ε_sphere ↔ ε_union 규약 차이가 커진다**(우리 실측 **1.251 %p**, 렌즈 겹침 SE–SE 0.402 +
  AM–SE 0.848).  ⇒ **porosity 규약을 항상 명시**해야 한다(우리는 이미 ε_sphere 로 통일).

**W4 — 강성↔배위수 결합이 전달을 오염시킬 수 있다.**
**Ng & Asce [193]**(p.130): 강성을 낮추면 **배위수가 올라간다**.  우리는 E_eff 를 **역학(porosity)** 으로
보정한 뒤 **그 침대의 접촉망**으로 σ_ionic/σ_e/σ_thermal 을 푼다.  즉 **역학 보정이 전달 그래프를 정의한다.**
사내 검증은 **1.35 ↔ 1.5 구간**(overlap 1.75 vs 1.74 %, ⟨δ⟩ 0.0739 vs 0.0743 µm = 동일 regime)에서만 있고,
**24 → 1.35 구간의 배위수/접촉면적 변화가 σ 에 미치는 영향은 미측정**이다.
⇒ **실행 항목**: 같은 침대를 E = {24, 5, 1.35} 로 압축해 **Z(배위수)·접촉면적 분포·σ 삼중항**을 나란히.
Stage-E(Tabor+volume) 면적 재유도가 이 오염을 얼마나 흡수하는지가 그 표에서 보인다.

**W5 — 구(sphere) + rolling friction 없음의 원리적 한계.**
**Coetzee [62]**(p.113): *"Spherical particles without rolling friction … **could not be calibrated** …
**even when high particle friction coefficients were used**."*  우리 타깃은 마찰이 아니라 porosity 라
직격은 아니지만, 두 가지가 따라온다:
· 우리 침대의 **전단강도는 원리적으로 과소**다 → 재배열이 실제보다 쉽다 → 그 결손도 E_eff 에 흘러든다.
· **Santos [170]**(p.125): 구형 입자는 보정값이 **조건 특이적이고 일반화되지 않는다**.
⇒ `E_eff = 1.35 GPa` 은 "LPSCl 물성"이 아니라 **{구 근사 + hooke/hysteresis + 재배열·GB slide·미세파괴 결손}
의 합산 상수**로만 보고할 것.  (우리 frame[2] 서술이 이미 그렇게 되어 있다 — 리뷰가 그 서술을 **문헌적으로 지지**한다.)

**W6 — 코드 의존성.**
리뷰가 두 번 명시(§1 p.105 · §9 p.138).  `E_eff = 1.35` 는 **LIGGGHTS hooke/hysteresis 규약값**이며
Hertz–Mindlin·EDEM·Rocky·PFC 로 그대로 못 옮긴다.  실제 대조가 있다 — **Bazzoun**(같은 LIGGGHTS, **Hertz**)은
E_SE **20.5–22.1 GPa**(=실물값)를 쓰고 porosity **0.16–0.25** 를 낸다.  같은 코드라도 **접촉법칙이 다르면
E 의 의미가 다르다**는 실사례.  ⇒ 원고 표에 **"code: LIGGGHTS, contact law: hooke/hysteresis, value type:
particle (material) Young's modulus, source: **calibrated** (target: pure-SE porosity 10 % @ 300 MPa)"** 를
한 줄로 못 박을 것.

**W7 — 다압력으로 확장하는 순간 응력의존 규칙이 우리를 문다.**
Li [189]/Franco [196] 규칙(보정 응력 = 응용 응력)을 300 MPa 에서는 지키지만,
**100/200/600 MPa 로 쓰는 것은 리뷰 기준 외삽**이다.  이를 방어하는 유일한 길은
"E_eff 를 300 에서만 맞추고 나머지 압력은 **예측으로 보고**했다"는 프로토콜 서술 + Heckel R² 를
**적합도가 아니라 예측 정확도**로 제시하는 것.  ⇒ **원고 서술 점검 항목**(현재 CLAUDE.md 표기는
"DEM pure-SE 4압력"으로 적합만 적혀 있어 오해 소지).

### 10.4 ✅ 우리 강점 (리뷰 기준으로 방어 가능한 것)

1. **직접측정이 원리적으로 불가능한 입경대** — 리뷰가 보고하는 직접 접촉측정의 최소 입경은 **500 µm**[218]
   (일반 서술은 *"millimetre and above"*).  우리 LPSCl SE 는 **직경 ~1–3 µm** = **2–3 자릿수 아래**.
   ⇒ *"the Direct Measuring Approach is not available at our particle scale"* 는 **리뷰 인용으로 방어되는 문장**이다.
2. **보정 응력 = 응용 응력** (300 MPa).  리뷰의 명시 요구 충족.
3. **크기 스케일업 없음.**  리뷰가 §3.2 전체를 할애한 최대 오류원이 우리에겐 없다.
4. **3층 물성 보고**(real / DEM-eff / MPM) — 리뷰가 §1 에서 "문헌이 흔히 안 한다"고 지적한 바로 그 구분.
5. **연화의 *방향*에 문헌 기전이 있다** — Van Lew [236] + Molenda [230](μ 분포 → 더 무름, **배수 미보고**).
   ⚠⚠ **2026-08-25 정정 (Van Lew 1차 출처 대조 — `vanlew2015_modifying_youngs_modulus_distribution.md` §9-c)**:
   ~~"E 분포 → 더 무른 거시응답"~~ 은 **Van Lew 가 분리하지 못한 명제**다 (분포 침대의 **평균도 1.84× 낮고
   상수-Ē 통제군이 없다**).  **인용 가능한 형태로 바꿀 것** → *"단일입자 압쇄 실측에서 **개별 입자의 겉보기 E 가
   소결 벌크 문헌값보다 낮다** (κ̄ = E_peb/E_bulk ≈ 0.54, 배치 내 산포 ~7× digitized)"* — **이쪽이 더 강하다.**
   ★ **"배수 n/a" 도 Van Lew 에 한해 상향 정정**: **1.84× (90 → 49 GPa, 둘 다 stated)**.
   ⛔ 그리고 그 값이 **우리 18× 의 1/10** 이므로 **이 문헌으로 18× 를 정당화할 수 없다** —
   근거는 "미보고"가 아니라 **"보고된 값이 10배 부족"** 으로 바뀐다.
6. **접촉법칙 계열의 유일한 head-to-head 에서 이력 모델이 이겼다** — Ucgul [136]: Walton–Braun 이력 spring >
   Hertz (토양-공구).  ⚠ n=1, 토양, 저응력 → **"유리한 단일 사례"** 이상으로 쓰지 말 것.
7. **σ 삼중항·Stage-E·MPM 형상소성**은 리뷰의 지도에 **칸 자체가 없다** = 우리 고유 (frame[5]).

---

## 11. 적용 인사이트 (실행 항목)

- **① OAT 민감도표 1장을 만든다** (W1).  `ε@300 = f(μ_pp, μ_pw, COR)` at E_eff 고정.
  리뷰가 요구하는 "파라미터 고립"의 증명이며, Table 1 을 우리 계로 재작성하는 것과 같다.
  비용도 작다(기존 pure-SE 침대 재압축 6–9 런).  **이것 없이는 "우리 보정은 유일하다"고 쓸 수 없다.**
- **② 검증 시험을 하나 고르고, 먼저 그 시험의 E-민감도를 잰다** (W2/W2′).
  후보: (a) 조성 스윕의 **Furnas dip 위치**(기하 지배 → E 의존성이 porosity 와 다름),
  (b) **다압력 두께/스프링백**, (c) **전달 σ vs 실험 EIS**(Bazzoun/Minnmann).
  리뷰 규약 ②에 따라 **민감하지 않으면 검증으로 못 쓴다**.
- **③ 재파라미터화 가능성** (W2′ 의 부산물): σ 가 E 에 둔감하고 porosity 에만 민감하다면,
  우리 파이프라인의 실질 보정변수는 **porosity** 다.  리뷰 §1 은 "macro 는 입력이 될 수 없다"고 하지만,
  **macro 를 타깃으로 micro 를 정하는 것**이 정확히 벌크 보정이므로 충돌하지 않는다.
  ⇒ 원고 서술 권장형: *"E_eff is the micro parameter adjusted so that the assembly reproduces the measured
  macro porosity; it is a model parameter, not the SE Young's modulus."*
- **④ E-스윕 × 배위수/접촉면적/σ 표** (W4).  E = {24, 5, 1.35} 에서 Z·A·σ 삼중항 나란히.
  Ng & Asce 기전이 우리 계에서 얼마나 세게 작동하는지가 여기서 결정된다.
- **⑤ 보고 서식 채택**: 파라미터 표에 **`source` 열**(measured / calibrated / literature / assumed) +
  **`code` · `contact law` · `value type`(particle vs contact)** 헤더.  §5-Q3 근거.
- **⑥ 그림 양식 채택**: **Fig 32/33 스타일** — *보정 곡선 + 실험 min/avg/max 수평 밴드*.
  우리 `ε vs E_eff` 곡선에 Minnmann 밴드를 얹으면 리뷰 표준 그림이 된다.  그리고 **Fig 25 스타일**
  (두 등고선 교차)을 목표 그림으로 삼으면 W1·W2 가 한 장에 해결된다.
- **⑦ 응력 범위 문장 고정**: *"방법론은 전이되나 파라미터는 전이되지 않는다"* 를 리뷰 자신의
  Li[189]/Franco[196] 문장으로 근거화 (Q6).  리뷰의 μ·E·COR 수치를 우리 표에 **절대 옮기지 말 것**.

---

## 12. 인용 가능 문장 (deck / paper 용 — 영어 원문 + 쪽)

1. **역보정 정당화 (1순위)** — Coetzee, Powder Technol. 310 (2017) 138:
   > *"Another advantage of this approach is that the particle size can be scaled up, the particle shape can
   > be simplified and assumptions in terms of the contact model can be made. The calibration process will
   > then reduce the effect that these simplifications and assumptions might have on the bulk behaviour
   > since the other parameters will compensate for it."*
2. **역보정의 지위** — p.106 / p.138:
   > *"The first approach is a calibration approach in the true sense of the word…"* /
   > *"The bulk calibration approach is by far the most popular approach…"*
3. **직접측정 불가 (우리 입경)** — p.106 / p.134:
   > *"Several attempts were made, but they were all applied to particles in the **millimetre and above**
   > size range."*  (최소 사례: 접촉 마찰 측정 **500 µm** 입자 [218], p.134)
4. **비유일성과 그 처방** — p.123:
   > *"…more than one set of parameter values will produce the same bulk response for a given experiment.
   > To prevent this, more than one experiment should be conducted and **each experiment should isolate a
   > single parameter**…, or the combined results from more than one experiment should provide a unique set."*
5. **검증 규약** — p.106:
   > *"It is also important that the calibration experiment is different from the final experiment or
   > application being modelled. If the final application is used to calibrate the parameter values, the
   > exercise is nothing more than a parameter sensitivity study."*
6. **응력 의존 (우리 300 MPa 방어 + 문헌값 전이 금지)** — p.129:
   > *"…the parameter and property values are stress dependent and the stress levels used in the calibration
   > experiment should be carefully selected."*
7. **강성은 구속 단축압축으로 고립** — p.131:
   > *"…the confined uniaxial compression test was only influenced by the particle stiffness while the
   > particle-particle friction coefficient had no significant effect."*
8. **모델 파라미터 ≠ 물성** — p.105:
   > *"Macro properties cannot be specified as input parameters in a DEM model, the micro parameter values
   > need to be determined so that an assembly of numerical particles will exhibit the same bulk behaviour
   > as the physical material."*
9. **코드 의존성** — p.105 / p.138:
   > *"…the calibrated parameter values might be code dependent."* / *"…might be software and contact model dependent."*
10. ⚠⚠ **[사용 중지 → 대체] 불균질성 → 더 무른 거시응답** — p.136, Van Lew et al. [236] 요약:
    > *"…the sample with a distribution in Young's modulus showed a softer response compared to the sample
    > with a constant Young's modulus."*
    **2026-08-25 1차 출처 대조 결과 이 문장을 원고에 쓰지 않는다.**
    (전문 = `vanlew2015_modifying_youngs_modulus_distribution.md` §9-c)
    · 이 문장은 **Van Lew 원문에 존재하지 않는다** — Coetzee 의 패러프레이즈다.
    · Van Lew 의 "distribution" 침대는 **평균 E 도 1.84× 낮고**(90 → 49 GPa) **상수-Ē 통제군이 없어**
      *분포 효과*와 *평균 효과*를 **분리하지 못한다**.  ⇒ 원문이 지지하는 명제가 아니다.
    ✅ **대체 문장 (1차 출처 직접인용 가능, 더 강함)** — Van Lew §5:
    > *"…values of Young's modulii used in numerical models are taken from values measured for
    > **large sintered pellets** of ceramic materials."*
    + 실측 결론: **κ̄ = E_peb/E_bulk ≈ 0.54 (1.84× 연화), 배치 내 산포 ~7× (digitized)**.

⚠ 위 1–9 는 **리뷰 저자 Coetzee 자신의 서술**(인용 시 Coetzee 2017).
10 은 **리뷰가 요약한 1차 출처**(Van Lew et al., Fusion Eng. Des. 98-99 (2015) 1893) → **1차 출처 확인 완료
(2026-08-25) 결과 재인용에 드리프트가 있었다** ⇒ *"as summarised by Coetzee (2017)"* 로도 쓰지 말고
**위 대체 문장으로 교체**할 것.  ★ 이 사례가 §13 의 *"절대값을 원고에 쓰려면 1차 출처 확인이 필수"* 규율이
**추상적 원칙이 아니라 실측된 오류율**임을 보여주는 리뷰 자신의 첫 사례다.

---

## 13. 주의 / 한계 (over-claim 방지)

**리뷰 자체의 성격**
- **자체 계산·실험 0.**  모든 수치가 소환값이며, 이 카드의 표는 **리뷰가 인용한 대로**다.
  절대값을 원고에 쓰려면 **1차 출처 확인이 필수**.
- **저자 이해상충 주의**: §5.5 "Comprehensive approach" 는 Coetzee 본인의 6편([25,26,28,62,201,202])이고,
  Fig 15·16·32·33 도 본인 논문에서 가져왔다.  "순차 고립 보정"이 리뷰에서 특히 잘 정돈돼 보이는 것은
  **저자 자신의 프로그램**이기 때문일 수 있다.  중립 서베이로만 인용하지 말 것.
- **리뷰가 기록한 상충이 여러 건**: 강성↔벌크마찰 부호([196]/[25] vs [197]), 강성↔ν 부호([76] vs [190]),
  강성 민감도 자체([190] vs [193]), 오버랩 허용치([233] 0.1–0.5 % vs [72] 4 %),
  rolling↔sliding 상호작용([180] vs [84]).  ⇒ **"문헌이 X 라고 한다"로 단정 금지** — 어느 계·어느 시험인지 병기.

**전이 한계 (우리 계 기준)**
- **소재**: 배터리 무관.  파쇄암·모래·곡물·유리·철광석.  **어떤 μ·E·COR 값도 옮기지 말 것.**
- **응력**: 중력·핸들링 규모.  본문에 응용 응력의 수치 명시가 **없다**.
  ⇒ *"이 리뷰는 <10 kPa 영역이다"* 는 **논문 stated 가 아니라 우리 추론** — 그렇게 표시할 것.
- **소성 부재**: `plastic` 1회, `Heckel` 0회, Thornton–Ning/EEPA/Storåkers 부재.
  ⇒ **접촉 소성캡·형상 소성·치밀화 물리에 대해 이 리뷰는 아무 말도 하지 않는다.**
  우리 Stage-E·MPM J2 를 이 리뷰로 정당화하려 하지 말 것 (그쪽은 varkey2026 / thorntonning1998 /
  so2022 / storakers1997 카드 소관).
- **§7 가드레일 오용 금지**: 오버랩 0.1–4 % 는 **속도용 강성감소**의 무해성 기준이지,
  **보정된 강성의 타당성 기준이 아니다.**  우리를 방어하는 데 써도 안 되고, 그 기준으로 우리를 재도 안 된다
  (§10.3-W3 참조 — 다만 우리가 그 창 밖 ~22× 라는 **사실 자체는 고지**해야 한다).
- **2D/3D 혼재**: [25,26,189,190(2D 언급)] 등 다수가 2D.  리뷰가 매번 밝히지 않으므로 1차 출처 확인 필요.
- **Fig 25/26/34 는 우리가 만들어야 할 그림의 *양식*이지 데이터가 아니다.**  digitize 하려면 1차 출처 PDF 필요.

**우리 서술이 넘지 말 것**
- ❌ *"Coetzee 리뷰가 우리 18× 연화를 승인한다"* → 리뷰에 **강성을 치밀화 목표에 맞춘 사례는 없다**.
  ✅ 대신: *"리뷰는 보정값이 형상·크기·접촉모델 단순화를 보상한다고 명시하며(§5, §9), 마찰에 대해서는
  실측값에서 벗어난 보정값을 형상 결손으로 정당화하는 사례를 기록한다(Li [189], p.129).
  우리 E_eff 는 같은 인식론을 강성 축에 적용한 것이다."*
- ❌ *"리뷰가 Heckel 을 표준 보정시험으로 든다"* → **없다.**
- ❌ *"리뷰가 '<10 kPa' 라고 한다"* → **없다.**
- ❌ *"리뷰가 source: calibrated 표기를 규정한다"* → 명시 규정은 **없다**.  ✅ *"provenance 미기재를 문헌의
  결함으로 지적하고(§1), 리뷰 자신은 Table 1/2 를 provenance 로 나눈다."*

---

## 14. 기법 미니 용어집 (이 카드 안에서 쓰인 용어)

| 용어 | 뜻 (이 리뷰 맥락) |
|---|---|
| **Bulk Calibration Approach** | 벌크 거동을 재고, DEM 파라미터를 반복 조정해 그 거동을 재현시키는 **역보정** |
| **Direct Measuring Approach** | 입자/접촉 수준에서 물성을 직접 재어 그대로 입력 |
| **clump (cluster / multi-sphere)** | 여러 구를 강체로 묶어 만든 비구형 입자.  구성 구 사이 접촉력 없음, 깨지지 않음 |
| **sphericity ψ** | ψ = π^{1/3}(6V_p)^{2/3}/A_p — 같은 부피 구의 표면적 / 실제 표면적 |
| **IQ (isoperimetric quotient)** | 36πV²/S² — 구형도 지표 (구 = 1) |
| **rolling friction / resistance** | 회전에 저항하는 모멘트.  형상 결손의 **경험적 보상** 파라미터 (직접 측정 불가) |
| **angle of repose (static / dynamic)** | 정적 = 파일 형성, 동적 = 회전드럼.  최다 사용 벌크 보정량 |
| **dilatancy (angle of dilation)** | 전단 시 체적 팽창.  공극률/공극비와 연결 |
| **oedometer / confined uniaxial compression** | 측방 구속 하 단축압축 = **벌크강성 측정** = 우리 냉간압축의 리뷰 어휘 |
| **parallel gradation** | PSD 전체를 로그축에서 평행이동해 입자를 스케일하는 기법 (Fig 18) |
| **scale invariance (Feng)** | F_n = k r^a δ^b 에서 a+b = n_d−1 이면 크기 스케일에 불변 |
| **coarse graining** | 입자를 키워 개수를 줄이는 총칭 |
| **DACE / Kriging / LHS** | 계산실험 설계 — 대리모델로 DEM 실행 횟수를 줄이는 보정 가속 |
| **OAT (one-at-a-time)** | 한 번에 한 파라미터만 바꾸는 민감도 설계 |
| **stiffness ratio** | k_t/k_n (전단/법선).  삼축에서 ν 를 맞추는 데 쓰임.  실측 0.3–1 [216,217] |

---

## 15. 이 카드와 함께 볼 정본 카드

| slug | 관계 |
|---|---|
| `bazzoun2025_dem_parameter_sensitivity_assb_cathode` | **같은 문제를 우리 소재계에서** — LIGGGHTS OAT 민감도 + 실험 보정.  Coetzee 가 요구하는 §10.3-W1 표를 **그들이 이미 만들었다**(μ_CAM-SE 가 최강 민감).  우리 W1 실행 시 그 설계를 베낄 것 |
| `bazzoun2026_dem_fem_rnm_ionic` | 같은 그룹의 전달 편.  Coetzee 규범의 "다른 시험 검증"(W2) 후보 = 그들의 EIS 앵커 |
| `varkey2026_multicontact_elastoplastic_dem` | Coetzee 가 **다루지 않는** 접촉 소성(Thornton–Ning p_y)·다중접촉.  "리뷰에 소성이 없다"는 공백을 메우는 카드 |
| `thorntonning1998_adhesive_elastoplastic_contact` · `thakur2014_eepa_adhesive_elastoplastic_dem` · `storakers1997_similarity_inelastic_contact` | 소성 접촉법칙 정의서들 (Coetzee 범위 밖) |
| `so2022_dem_contact_model_assb_compaction_sintering` · `so2021_dem_mold_pressure_assb_coldpress` | 고압 냉간압축 DEM — Coetzee 의 저응력 카탈로그와 대비 |
| `boschpadros2014_dem_liggghts_msc_thesis` · `shenouda2020_dem_metal_powder_am_liggghts_tutorial` | LIGGGHTS 규약·입력값 계보 |

---

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
