# DEM 결과에 대한 입자 **탄성 물성**(Young's modulus E · shear modulus G · 접촉강성 contact stiffness)의 영향 리뷰 — 조밀계 vs 희박계 · 오버랩 1 % 규칙 · "밀할수록 강성이 중요해진다" — Paulick, Morgeneyer, Kwade (Powder Technology 2015)

> slug `paulick2015_elastic_particle_properties_dem_review` · DOI `10.1016/j.powtec.2015.03.040` · type `DEM (review — 탄성 파라미터 민감도)` · PDF `df4b5cdd-Review_on_the_influence_of_elastic_particle_properties_on_DEM_simulation_results.pdf` · digested `2026-08-25` · status ✅

---

## 1. 한 줄 요약 (TL;DR)

**"DEM 에서 E(또는 G, 또는 k_n)를 바꾸면 무엇이 바뀌고 무엇이 안 바뀌는가"만을 30+ 편으로 훑은
유일한 전용 리뷰.**  결론은 세 줄이다 —
① **탄성 파라미터는 계산속도를 위해 관행적으로 낮춰지며**, 리뷰의 표현으로 *"in pure numerical
studies the elasticity is often reduced, **neglecting any probable change of numerical response**"*
(Abstract, p.66).
② 낮춰도 되는 한계선으로 리뷰가 제시하는 것은 **오버랩 ≤ 입자 *지름*의 1 %** 이고 (§4 p.75, §5 p.75),
그 목적은 *"for **elastic deformation as foreseen by Hertz**"* — 즉 **속도용 감소의 무해성 + 헤르츠
탄성접촉 가정의 유효성**이지 수치안정성(그건 별도의 Rayleigh Δt, Eq. 2)이 아니다.
③ 총평은 **regime 판정**이다: ***"The denser the system, the more important is the stiffness value"***
(§5 p.75) — 희박·CFD-DEM 에서는 무시할 만하고, **조밀·구속계에서는 신중히 골라야 한다**.

★ **우리에게 결정적인 두 문장** (둘 다 §2.2 p.71 의 같은 문단, 서로 짝):
- **허용** — *"All authors found a **linear relationship** between the applied elastic parameter
  (contact stiffness, particle stiffness or shear modulus) and the bulk modulus which **enables the
  DEM user to scale down the stiffness parameter** for this specific application and for determining
  the bulk modulus."*
- **대가** — *"**However, a scale down in stiffness leads to a different compression behaviour** and,
  thus, **different force chains and distributions of normal force values may develop** [33,35]."*

⇒ 즉 이 리뷰는 **"벌크 *탄성계수* 를 맞추려고 강성을 낮추는 것"은 선형관계가 보장한다고 명시적으로
허용**하고, 동시에 **"그 대가는 힘사슬과 수직력 *분포* 가 달라지는 것"** 이라고 못 박는다.
우리 Kirchhoff/Holm 전달망은 **접촉당 힘·면적**을 먹는다 ⇒ **허용은 우리 porosity 보정에, 대가는 우리
σ 계산에** 정확히 떨어진다.  이 짝이 이 카드의 최대 소득이다.

⚠ **범위 경고 (읽기 전에)**: 이 리뷰 전체에서 언급된 **최대 구속응력은 ≈ 96 kPa**(Thakur 무구속압축)
이고 오이도미터는 **0–80 kPa** 이다.  우리 **300 MPa 는 그보다 3,000 배 이상**이다.
**고압 치밀 압밀은 이 리뷰에 없다.**  §5-Q7 참조.

---

## 2. 메타

| 항목 | 값 |
|---|---|
| 저자 | **M. Paulick** ^a,b · **M. Morgeneyer** ^a · **A. Kwade** ^b |
| 소속 | ^a GPI, Université de Technologie de Compiègne, B.P. 20.529, 60200 Compiègne, France · ^b **Institut für Partikeltechnik, TU Braunschweig**, Volkmaroderstr. 4-5, 38104 Braunschweig, Germany |
| 저널 | **Powder Technology 283 (2015) 66–76** (11 pp) |
| DOI | `10.1016/j.powtec.2015.03.040` |
| 이력 | Received **2014-06-23** · revised **2015-03-19** · accepted **2015-03-28** · online **2015-04-03** |
| 유형 | **Review** (논문 유형 자체가 "Review" 로 표기됨) |
| 키워드 | DEM simulation · Young's modulus · Shear modulus · Stiffness · Sensitivity analysis · Industrial processes · Laboratory tests · Calibration |
| 소속 네트워크 | **PARDEM** (EU Marie Curie ITN, www.pardem.eu) + Deutsch-Französische Hochschule |
| 참고문헌 | **72 편** |
| 리뷰 규모 | 저자 표현 *"more than 30 researches"* (§5 p.75) |
| 재료계 | **없음 — 소재 무관 방법론 리뷰** (유리구슬 · 옥수수 · 분뇨 · 암석 · 세제분말 · 나노실리카 · 유동층 분체) |
| 우리 소재계와의 거리 | **LPSCl/NMC 언급 0회.  배터리 언급 0회.**  전이되는 것은 *방법론과 regime 판정*뿐 |

**계보 메모** — A. Kwade(TU Braunschweig, iPAT)는 정본의 **`giannis2021_stress_based_multicontact_dem`**
공저자이기도 하다.  같은 그룹의 계보이므로 cross-reference 만 남긴다.
Giannis 내용은 **이 카드에서 추측하지 않는다** (그 카드가 정본).
또 **[29] Combarros et al.** 도 Kwade 공저이며 **LIGGGHTS 1.5.3** 을 쓴다 = 이 리뷰 안에서
**우리와 같은 코드**를 쓴 유일한 항목이다 (§5-Q5 표 참조).

---

## 3. 범위 상자 — 이 리뷰가 다루는 것 / **다루지 않는 것** (인용 전 필독)

| 다룬다 ✅ | 다루지 않는다 ⛔ |
|---|---|
| E · G · k_n(선형) · k_n(Hertz) · bond stiffness · 강성비 K=k_t/k_n 가 **거시응답을 바꾸는가** | **입자 탄성물성 *측정법*** — 리뷰 장(章)이 없다 (§5-Q6) |
| **process regime 분류** (조밀/희박 × 정적/동적, Table 1) | **재료별 E 값 표** — 없다.  재료명↔E 대응이 산발적 |
| 오버랩 가드레일 (1 %, 0.5 %, 0.6 %-of-radius, 1–10 %) | **고압 압밀 (≥ 1 MPa)** — 최고 96 kPa (§5-Q7) |
| **Δt ↔ G** (Rayleigh, Eq. 2) 와 속도 동기 | **소성 접촉법칙** — 리뷰 대상 중 소성 LAW 는 Thakur [32] **1 편**뿐이고 그마저 E 가 아니라 λ_p 를 스윕 |
| **코드마다 다른 탄성 입력** (E / G / k_n) 의 지도 (Table 4, 6) | **입자 형상·크기·마찰·COR 의 독립 보정** (그건 Coetzee 2017 소관) |
| bonded-particle 파괴 (agglomerate) 에서의 bond stiffness | **coarse-graining/upscaling** — *"should be investigated"* 라고 **미해결로 지목**만 (§4 p.75) |
| 파라미터 **교차상관** 경고 (마찰×강성, COR←강성비) | **전달 물성(σ, κ)** — 전무 |

⚠ **결정적 한 줄**: 리뷰가 자기 입으로 지목한 미해결 영역이 **하필 우리 자리**다 —
*"we notice that **only little research on the influence of contact stiffness on bulk behaviour of
powders** has been conducted.  Due to high computational efforts in case of numerically describing
**fine powders**, also the influence of contact stiffness during **particle upscaling** should be
investigated."* (§4 p.75).  우리는 Ø 1 µm 급 **fine powder** 를 다루고 **강성을 바꾼다**.
⇒ 이 리뷰 기준으로 우리 문제는 **"아직 연구되지 않은 영역"** 이다.  방어 논거이자 정직한 상태서술.

---

## 4. 핵심 수식 3개 (§1, p.66–67) — 지도교수 질문의 산술적 뼈대

### (1) 탄성 파라미터는 코드마다 **다른 이름으로** 들어간다 (p.66–67, 원문 그대로)
> *"For instance, to consider the elastic part of a contact, either **the contact stiffness [17]**,
> **the Young's modulus [9]** or **shear modulus [8]** is introduced."*

| 코드 | 입력 | 참조 |
|---|---|---|
| Luding 계열 (선형 이력 LAW) | **k_n** (접촉강성) | [17] Luding 2004 |
| **LIGGGHTS®** | **Young's modulus E** | [9] Kloss et al. 2012 |
| **EDEM®** | **Shear modulus G** | [8] DEM Solutions 2010 |
| PFC2D/3D | k_n (선형) 또는 E/G (Hertz–Mindlin) | [10],[58] |

**k_n 의 정의**: *"The contact stiffness k_n links the particle overlap δ_n and the resulting normal
forces F_n in the particle contact area [19]."*

### (2) **Eq. (1)** — E ↔ G 는 ν 로 **선형** 연결 (p.67)
```
E = 2 G (1 + ν)
```
> *"Young's modulus E and shear modulus G are **linearly dependent by each other through Poisson's
> ratio ν**"*

⇒ **등방 선형탄성에서 (E, G, ν) 는 자유도가 2 이다.** 둘을 주면 셋째는 **선택이 아니라 산술로
강제**된다.  "G 의 출처가 어디냐"는 질문은 형식적으로 **"(E, ν) 쌍이 물리적이냐"** 로 환원된다
(§10-(c) 판정).

### (3) **Eq. (2)** — 시간간격은 **G^(−1/2)** (p.67, EDEM 규약 [8])
```
Δt = 0.2 · π · R_p · (ρ / G)^0.5 / (0.1631 ν + 0.8766)
```
> *"The time step must be sufficiently smaller than the particles' contact duration… **However, the
> time step size is increased if the elasticity parameter decreases which results into a faster
> simulation time.**"*

이 한 줄이 **"왜 다들 E 를 낮추는가"** 의 전부다 (= 아래 (a) 동기).
- **Δt ∝ G^(−1/2)** — G 를 f 배 낮추면 Δt 는 **√f 배**.
- **ν 는 거의 안 먹는다** — 분모 (0.1631ν + 0.8766) 은 ν 0.30 → 0.9255, ν 0.49 → 0.9565 = **+3.3 %** 뿐.

★ **우리 수치로 환산** (DERIVED-BY-US, 논문에 없음 — 이 식에 우리 값을 대입한 것):
| | 원 값 | 우리 값 | 배수 | Δt 이득 (√f) |
|---|---|---|---|---|
| DEM E_SE | 24 GPa | **1.35 GPa** | ÷17.78 | **×4.22** |
| MPM 유효 G (E 1.53 / ν 0.49) | DFT 쌍 (B₀ 26.23, E_VRH 22.06) ⇒ ν 0.360, **G 8.11 GPa** | **G = 0.5134 GPa** | ÷15.80 | (MPM 은 CFL, Eq.2 비적용) |
⇒ **우리 18× 연화는 부수적으로 Δt 를 ~4.2 배 벌어준다.**  그러나 그것은 **동기가 아니라 배당금**이다.
동기를 (a)로 적으면 §10-(a) 판정이 뒤집히므로 **원고에 절대 (a)로 쓰지 말 것**.

---

## 5. ★★★ 지도교수 질문 8개 — 직답 (근거 문장 + 쪽수)

### Q1. ★★★ **E 를 낮추는 두 갈래를 이 리뷰가 어떻게 가르는가?  (b) 사례가 있는가?**

**라벨 정의** (이 카드 안에서 고정; Coetzee 카드의 (a)/(b)와 **반대 번호**이니 주의):
- **(a) 속도용 감소** — 목적 = 큰 Δt.  **정당성 조건 = "벌크가 안 변할 것"**.
- **(b) 벌크-맞춤 보정** — 목적 = 실측 벌크 거동 재현.  값은 **데이터가 정한다**.
  *(Coetzee 카드에서는 이 둘이 각각 (b)/(a)로 번호가 반대다 — 인용 시 라벨 명시 필수.)*

**판정 — 이 리뷰의 압도적 다수는 (a)도 (b)도 아닌 *제3의 것*, 즉 순수 *민감도 스윕* 이다.**

리뷰가 모은 30+ 편을 동기로 분류하면:

| 동기 | 편수(내 분류) | 대표 | 근거 |
|---|---|---|---|
| **민감도 스윕** (E 를 훑고 응답을 보고함, 값을 고르지 않음) | **압도적 다수** (Table 4·6 의 거의 전부) | [21][23][24][28][29][34][35][62][63][66] | 각 항목의 "Elasticity value = 범위" 열 |
| **(a) 속도용 감소** | 명시 4편 | [64] Tsuji · [65] Mikami · [66] Nakamura · [27] Liyan | Abstract p.66 *"the elasticity is often reduced to lower the running time"*; [66] p.73 *"a **decrease in simulation time by a factor of 10 is worth the loss of accuracy**"* |
| **직접측정(= 연화 아님)** | 3편 | [62] k_n 1.72×10⁷ N/m = *"identical to the physically measured value"* · [67] Hertz 로 입자/벽 실험 환산 2×10⁷ · [54] 템퍼링 실측 강성을 DEM 에 이식 | p.73, p.74 |
| **(b) 벌크-맞춤 보정 — *명시적 사례*** | ⛔ **0 편** | — | — |

⇒ **답: 이 리뷰 안에 "실험 벌크 곡선에 맞추려고 E 를 N 배 낮췄다" 고 명시한 사례 논문은 없다.**
배수도 당연히 없다.  ⚠ 이것은 **없다고 명확히 써야 하는 항목**이다 (§F1).

**그러나 리뷰는 (b)를 *원리적으로 허가* 한다.**  §2.2 p.71 종합 문단:
> *"All authors found a **linear relationship** between the applied elastic parameter (contact
> stiffness, particle stiffness or shear modulus) **and the bulk modulus** which **enables the DEM
> user to scale down the stiffness parameter** for this specific application and for determining the
> bulk modulus."*

이것은 (a)의 논거("벌크가 안 변한다")가 **아니다** — 정반대로 **"벌크가 선형으로 변하니까,
원하는 벌크계수를 주는 강성을 고를 수 있다"** 는 (b)의 논거다.  선형·단조 사상이면 역함수가 있다.
**리뷰가 든 선형 증거 4건** (독립 그룹·독립 코드):

| 관계 | 계 | 스윕 폭 | 코드 | 출처 |
|---|---|---|---|---|
| k_n ∝ 구속 벌크계수 | 오이도미터 2D (D 0.25 m, H 0.08 m, 0→80 kPa) | k_n 10 → 500 kN/m (**50×**) | PFC2D | [21] Coetzee & Els 2009 |
| G ∝ 벌크강성 | 단축 벌크압축, 18,000 입자, 수평 주기경계 | G 10⁴ → 10¹¹ Pa (**10⁷×**) | EDEM Hertz–Mindlin | [23] Lommen 2013 |
| E ∝ 성립 벌크계수 | 동적 콘 관입 | E 2.9 / 9 / 29 GPa (**10×**) | 자체 3D Fortran F90 | [24] Yohannes 2013 |
| 강성 = 하중–변위의 **주** 파라미터 | 오이도미터 3D **비구형** (D 0.4, H 0.25 m) | 미명시 | PFC3D | [30] Coetzee 2010 |

**그리고 리뷰는 그 대가를 같은 문단에서 즉시 청구한다** (이것이 우리에게 가장 중요한 문장):
> *"**However, a scale down in stiffness leads to a different compression behaviour** and, thus,
> **different force chains and distributions of normal force values may develop** [33,35]."*

**정량 예시가 리뷰 안에 있다** — [38] Xu et al. 2002 (§2.3 p.71), E **70 MPa vs 70 GPa (÷1000)**:

| 관측량 | 연질 E=70 MPa | 경질 E=70 GPa | 비 |
|---|---|---|---|
| 배출량·유동프로파일·동역학 | 사실상 동일 | 동일 | ≈1 |
| **평균** 압축접촉력 (배출 전) | 1.86×10⁻⁴ N | 2.04×10⁻⁴ N | 1.10 |
| **최대** 압축접촉력 (배출 전) | 17.49×10⁻⁴ N | 24.18×10⁻⁴ N | 1.38 |
| **평균** 압축력 (24 % 배출 후) | 1.97×10⁻⁴ N | 2.99×10⁻⁴ N | 1.52 |
| **최대** 압축력 (24 % 배출 후) | **40.6×10⁻⁴ N** | **364.4×10⁻⁴ N** | **8.98×** |

리뷰의 요약: *"a **minor reduced elastic parameter does not influence the discharge rate but strongly
affects the arising contact forces**."*
⇒ **평균은 전이되고 꼬리는 전이되지 않는다.**  1000× 연화가 평균힘은 1.5× 만 바꾸는데 **최대힘은 9×**
바꾼다.  우리 σ 는 **접촉당** 협착저항 R = 1/(2σr_c) 의 **직렬-병렬 망**이라 힘/면적의 **분포**에
민감하다 ⇒ **이 표가 우리 §10-(a) 판정의 "대가" 칸 그 자체다.**

---

### Q2. ★★★ **오버랩·강성 가드레일의 정확한 원문과 그 *적용 조건***

**원문 2곳 (verbatim).**

**§4 Discussion, p.75**:
> *"In a variety of numerical experiments the influence of the elastic parameter on the particle
> overlap and their effect on the simulation result have been investigated.  For different simulation
> tasks **a reduction of the elastic parameter did not show a major change in the numerical result as
> long as the particle overlap remains smaller than 1 % of the particle diameter** [26,27,70–72].
> Hereby, it depends on the dynamics of the system to apply the **maximum** overlap observed over a
> period of the simulation or the **average** overlap — the latter may be used for less energetic
> applications."*

**§5 Conclusions, p.75**:
> *"An approach to **correctly reduce** the elastic parameter would be to identify the particle
> overlap which should not be larger than 1 % **for elastic deformation as foreseen by Hertz [11]**
> and proposed by Cleary [71,72]."*

**⇒ 이 기준은 무엇을 보장하는가?  두 가지, 그리고 그 둘뿐이다.**
1. **"강성을 낮춰도 결과가 안 바뀐다"의 불변성** — 문장 자체가 *"a **reduction** of the elastic
   parameter did not show a major change"* 이다.  **(a) 전용 조항**이다.
2. **헤르츠 *탄성* 접촉 가정의 유효성** — *"for **elastic deformation as foreseen by Hertz**"*.
   즉 **접촉법칙 타당성** 기준이다.
- ⛔ **수치안정성이 아니다** — 그건 별도의 Eq. (2) Rayleigh Δt 다 (§4 위).
- ⛔ **"정확도 일반"도 아니다** — 리뷰는 정확도를 관측량별로 따로 다룬다 (Q5 표).

**⇒ 어느 계에서 도출됐나? — 인용된 5개 출처를 전부 열면 답이 나온다.**

| ref | 계 | 응력 영역 | 성격 |
|---|---|---|---|
| [26] Hanes & Walton 2000 | **경사 범프 슈트**를 굴러내리는 유리구슬 | 대기압, 중력구동 | 충돌·유동 |
| [27] Liyan 2013 | **왕복 그레이트**(reciprocating grates) 이송 | 대기압 | 동적 이송 |
| [70] Deen 2007 | **유동층** 이산입자모델 리뷰 | 대기압, 유체지배 | **희박** |
| [71] Cleary 2000 | 산업 유동 (드래그라인·텀블러·원심밀) | 대기압 | 유동 |
| [72] Cleary & Sawley 2002 | 3D 산업 과립유동, 호퍼 배출 | 대기압 | 유동 |

⇒ **5/5 전부 자유표면·유동·충돌 지배계이고 구속압은 사실상 대기압이다.
구속 고압 압밀은 단 한 건도 없다.**  이것이 §10-(b) 판정의 근거다.

**⚠ 그리고 이 "1 %" 는 같은 리뷰 안에서 *네 가지 다른 형태*로 나타난다 (10× 산포):**

| 형태 | 기준 | 통계량 | 밑변 | 보장 대상 | 출처 |
|---|---|---|---|---|---|
| ① | **1–10 %** | (미명시) | (미명시) | 유동 패턴 | [25] Walton 1993, §2.1 p.67 |
| ② | **< 1 %** | **최대**(*"during the strongest appearing collision"*) | **지름** | 운동학 | [26] Hanes & Walton 2000, §2.1 p.67 |
| ③ | **≈ 0.5 %** | **평균** | **지름** | *"numerical results are independent of E"* | [27] Liyan 2013, Table 4 p.68 |
| ④ | **≈ 0.6 %** | **평균** | **반지름** | *"qualitatively good flow patterns"* | [5] Cleary & Hoyer 2000, §2.4 p.72 |
| **⑤ 리뷰 자신의 종합** | **< 1 %** | 계의 동역학에 따라 max 또는 mean | **지름** | (위 1,2) | §4·§5 p.75 |

⇒ **"1 %" 는 예리한 문턱이 아니라 rule of thumb 이고, 밑변(반지름/지름)과 통계량(평균/최대)이
출처마다 다르다.**  ④를 ⑤와 같은 자로 재면 2× 차이가 난다.  ★ 이 사실 자체가 **재인용 오류가
생기기 쉬운 구조**임을 보여준다 (§9 참조).

---

### Q3. ★★★ **"밀할수록 강성이 중요해진다" 의 원문·근거·정량**

**원문 (§5 Conclusions, p.75, verbatim):**
> *"Considering the above mentioned process regimes, **the particle appearance probably plays the
> major role: The denser the system, the more important is the stiffness value.**  For dilute and
> coupled DEM simulations with computational fluid dynamics (CFD) a change of stiffness parameter
> gave **negligible variances** in the numerical response.  However, the bulk behaviour **did change**
> for dense particle systems such as cone penetration.  Therefore, the conclusion can be drawn that
> **the denser the system, the more carefully the elastic parameter must be chosen.**"*

**⚠ 정량은 없다.**  리뷰는 **밀도 문턱을 하나도 제시하지 않는다** — 고체분율·상대밀도·배위수 어느
것으로도 선을 긋지 않는다.  근거는 **장(章) 대조**(§2 dense vs §3 dilute)의 **정성 판정**이다.
"어느 밀도부터인가?" → **n/a (논문에 없음).**

**dense 의 정의는 있다** (§2 p.67):
> *"A dense particle system is equivalent to a particle packing in which **the particles are in
> contact with each other during almost the whole process time.**"*
⇒ **접촉 지속시간 기준**이지 밀도 수치 기준이 아니다.  우리 300 MPa 잼 침대는 이 정의를 **최대치로**
만족한다 (배위수 ~6–8, 상대밀도 ~0.85–0.90).

**★★ 그런데 리뷰 자신의 데이터를 읽으면 "dense" 는 *너무 거친 변수*다 — 진짜 판별자는 다른 것이다.**
조밀계 장 안에서도 결과가 갈린다:
- 조밀인데 **둔감**: 안식각 (E 10⁵→10⁸ Pa 에서 **±1°**, [28]) · 호퍼 벽응력·배출률 ([36][37][38]) ·
  볼밀 파워피크 ([44]) · 전단 정상상태 (*"the key effect during shearing is the **particle
  rearrangement** and not the elasticity"*, [33] §2.2 p.70).
- 조밀이고 **민감**: 구속압축 벌크계수 (선형, [21][23][24][30]) · 콘 관입저항 (2×, [23]) ·
  내부마찰각 (~13°, [21]) · 직접전단 응집력 (4.3×, [34]).

⇒ **내 종합(= 이 카드의 해석, 논문의 문장이 아님)**: 갈림선은 "조밀/희박"이 아니라
**① 관측량이 *강성·힘·에너지 차원* 인가 (→ 민감), 아니면 *운동학·기하 차원* 인가 (→ 둔감)**,
그리고 **② 경계조건이 *구속·하중전달* 인가, *자유표면·유체지배* 인가**이다.
반례가 규칙을 증명한다 — **안식각(기하량)조차 G < 10⁷ Pa 로 내려가면 민감해진다**
(28°→26°→23°→**12°**, [23] §2.1 p.70): 입자가 너무 물러 패킹 자체가 변형되기 시작하면
기하량이 강성을 상속한다.

**⇒ 우리 상대밀도 ~0.9 · 300 MPa 구속 · σ/E_eff ≈ 0.22 영역에 대한 함의:**
**리뷰가 정의한 "가장 강성이 중요한" 극단 그 자체다.**  방향은 우리 MPM 실측
(*"E 가 지배 레버이고 σ_y 는 아니다"*, CLAUDE.md E-sweep: E 24 → 33–38 %, E 1.35 → 8 %)과
**부호가 일치**한다 ✅.  구속압축에서 **벌크계수 ∝ 강성이 선형**이라는 4건의 독립 결과가,
"강성 하나가 도달 밀도를 정한다"는 우리 관측의 **문헌 뒷받침**이다.

⚠⚠ **그러나 우리가 지금까지 이 축에서 써 온 문장 하나는 이 리뷰 기준으로 *잘못된 증거* 다.**
사내 서술 *"E 1.35 ≡ 1.5 는 구조·역학·전달 전 축에서 동일 regime"* 은 **E 를 11 % 바꾼 실험**이다.
선형 법칙이 예측하는 응답도 **11 %** 이고, 우리 실측 ε 13.47 vs 12.77 ± 0.31 %(3 seed)는
**시드 산포 안**이다.  ⇒ 이것은 **"E 에 둔감하다"의 증거가 아니라 "11 % 변화는 우리 잡음
이하"의 증거**이며, 리뷰의 선형법칙과 **완전히 양립한다** (리뷰의 스윕은 10× ~ 10⁷×).
**F-C2′ 를 이 문장 위에 세우면 리뷰어가 먼저 무너뜨린다.**  → §11 실행항목 ①.

---

### Q4. ★★ **전단탄성률 G 를 어떻게 다루는가** (지도교수가 콕 집은 항목)

**① DEM 입력은 E 인가 G 인가? — 코드마다 다르고, 리뷰가 그 지도를 그린다.**
§4-(1) 표 참조: **LIGGGHTS = E** [9] / **EDEM = G** [8] / Luding·PFC 선형 = **k_n** [17][10].
⇒ **우리가 LIGGGHTS 에 E 를 주는 것은 그 코드의 규약 그대로다.**

**② 유도 관행은 표준인가? — 표준 이전에 *산술적으로 강제*다.**
Eq. (1) `E = 2G(1+ν)` (p.67).  등방 선형탄성의 자유도는 2 이므로 (E, ν)를 주면 G 는 **정의된다.**
리뷰는 "어느 쪽을 입력하라"고 처방하지 **않는다** — 대신 **접촉 커널을 두 형태로 병기**한다
(Table 4, p.68–69):

| 형태 | 식 | 쓰는 곳 |
|---|---|---|
| E* 형 (Hertz–Mindlin) | `E* = [ (1−ν₁²)/E₁ + (1−ν₂²)/E₂ ]⁻¹` , `k_n = (4/3) E* √R*` | EDEM [23], LIGGGHTS [29], 자체코드 [24] |
| E* 형 (동일재료 2D) | `E* = E / (2(1−ν²))` | [28,57] |
| **G 형 (Hertz–Mindlin, PFC3D)** | `k_n = 2 G_hi √(2R*) / (3(1−ν_hi)) · √δ_n`, `G_hi = ½(G₁+G₂)`, `ν_hi = ½(ν₁+ν₂)` | [34] Landry |
| 선형 | `k_n = F_n/δ_n` (또는 `k_n = k_{n,1}k_{n,2}/(k_{n,1}+k_{n,2})`, `k_n = 4E*R*`) | [21][30][34] |
| 왕복그레이트 비선형 | `k_n = √d_p · E / (3(1−ν²))`, `k_t = 2√d_p · G/(2−ν) · δ_n^{1/2}` | [27] |

**③ ★ 같은 숫자를 E 로 넣느냐 G 로 넣느냐가 결과를 바꾼다 — 리뷰의 직접 증거 [34] (§2.2 p.70, Fig 3).**
Landry et al. 이 **같은 0.15 → 2.0 MPa 범위**를 두 모델에 넣었다:

| 모델 | 파라미터 | 응집력 변화 | 전단응력 |
|---|---|---|---|
| 선형 접촉 | **E** 0.15 → 2.0 MPa | **≈18 → 78 kPa (4.3×)** | *"a four times stronger increase"* |
| Hertz–Mindlin | **G** 0.15 → 2.0 MPa | **≈25 → 35 kPa (1.4×)** | *"an equal increase"* |

리뷰의 결론: *"the numerical response does **not only depend on well-chosen contact models but also
on suitable model parameters**."*
⇒ **"1.53 GPa" 라고만 적으면 의미가 없다.  어느 모듈러스인지 + 어느 접촉모델인지 항상 병기.**
(⚠ 본문은 비선형 모델 응집력을 *"lies here between 5 and 25"* 라 적고 Table 4 는 *"25 kPa to 35 kPa"*
라 적는다 — **논문 내부 불일치**.  §9 참조.  위 표는 Table 4 값을 채택.)

**④ ★★ 전단강성 *비율* K = k_t/k_n 은 구(sphere)에서 거의 안 먹는다 — [35] Antony 2006 (§2.2 p.70–71, Table 2).**
3D 준정적 전단, K = **0.25 / 0.5 / 1** (4×):

| 관측량 | **구형** | 비구형 (stick-slip 지배) |
|---|---|---|
| Contact density | **영향 없음** | 감소 |
| Effective void ratio | 미미한 증가 | 미미한 증가 |
| Sliding fraction 진화 | **영향 없음** | 최대값 증가 + 전체 진화는 감소 |
| Sliding energy ratio | **영향 없음** | 증가 |

⇒ **구 기반 DEM 에서 전단강성은 약한 레버다.**  우리는 구를 쓰므로 "G 를 독립 입력하지 않는다"의
**위험이 낮다**는 문헌 근거가 된다.  ⚠ 단 (i) 스윕 폭이 **4× 뿐**이고 (ii) **비구형에서는 먹는다.**

**⑤ 우리 (E, ν) 쌍의 노출 — 숫자로 (DERIVED-BY-US, Eq. (1) 대입):**

| 쌍 | 출처 | ν | G = E/2(1+ν) | K = E/3(1−2ν) |
|---|---|---|---|---|
| **MPM 생산값** | 우리 champion | **0.49** | **0.5134 GPa** | **25.5 GPa** |
| **우리 DFT 쌍** | B₀ 26.23 · E_VRH 22.06 | **0.360** (유도) | **8.11 GPa** | 26.23 GPa |
| 비 | | | **÷15.80** | ×0.972 |
| DEM 접촉입력 | LIGGGHTS | 0.30 | (E 1.35 ⇒ 0.519 GPa) | — |

⇒ **우리 이야기는 Eq. (1) 로 정확히 서술된다**: *"K 는 DFT B₀ 의 97 % 로 유지하고(실물 비압축성),
G 만 15.8× 연화했다(= granular 재배열 프록시)"*.  그리고 **ν 를 0.36→0.49 로 올린 것 자체가
전단을 추가로 1.096× 더 연화**시킨다 (분모 2(1+ν): 2.72 → 2.98).  **이 두 줄이 지도교수의
"전단탄성률의 출처" 질문에 대한 우리의 정답**이다 — 출처는 **DFT (B₀, E_VRH) 쌍 + Eq. (1) 항등식**
이고, **연화의 크기와 방향을 명시적으로 선언**하는 것.

---

### Q5. ★★ **민감도 종합 — 무엇이 E 에 민감하고 무엇이 둔감한가**

이 리뷰 전체를 **관측량 기준**으로 재정렬한 표다 (모든 값 **stated**; 그림에서 읽은 값 없음).

#### 5-A. E / G / k_n 에 **민감** (거시응답이 바뀜)

| # | 관측량 | 계 · 코드 | 스윕 | 응답 | 출처·쪽 |
|---|---|---|---|---|---|
| 1 | **구속 벌크계수** | 오이도미터 2D, PFC2D, 0–80 kPa | k_n 10 → 500 kN/m | **선형 ∝ k_n** (안정 이력루프 후) | [21] p.70, Fig 1 |
| 2 | **벌크강성** | 단축 벌크압축, EDEM H–M, 18k 입자, 주기 | G 10⁴ → 10¹¹ Pa | **선형 ∝ G**; G < 10⁴ Pa 이면 *"contacts could not generate enough force to reverse the direction of the mass motion"* | [23] p.70 |
| 3 | **성립 벌크계수** | 동적 콘 관입, 자체 3D | E 2.9 / 9 / 29 GPa | **선형** (단 *변형* 자체는 둔감 — 5-B #10) | [24] p.70 |
| 4 | 하중–변위 (암석) | 오이도미터 3D 비구형, PFC3D | 미명시 | *"stiffness is major parameter"* | [30] p.70 |
| 5 | **관입저항 (에너지)** | 쐐기 8 mm/s (base 40 mm, 30°), EDEM | G 10⁴ → 10⁹ Pa | G 10⁸–10⁹: **11–14 J** / G 10⁴–10⁶: **1–6 J** = **절반으로 과소평가** | [23] p.70 |
| 6 | **내부마찰각 Φ** | 전단시험 PFC2D | k_n 10 → 500 kN/m | **임계 100 kN/m**: 이하면 낮을수록 Φ↓ (**Table 4: ~13° 감소**); 이상이면 0.1<μ<0.15 무영향, 0.2<μ<0.3 은 **5°** 차 | [21] p.70, Fig 2 |
| 7 | **응집력·전단응력** | 직접전단 PFC3D, **선형** | E 0.15 → 2.0 MPa | 응집력 **18 → 78 kPa**, 전단응력 4× 증가 | [34] p.70, Fig 3a |
| 8 | 응집력·전단응력 | 직접전단 PFC3D, **H–M** | G 0.15 → 2.0 MPa | 응집력 **25 → 35 kPa** (Table 4) | [34] p.70, Fig 3b |
| 9 | **안식각 (저강성 한정)** | EDEM, 측판 10 mm/s 하강 | **G < 10 MPa** | **28° → 26° → 23° → 12°** | [23] p.70 |
| 10 | **비출력 (원심밀)** | 자체 2D, 695 rpm | k_n 2×10⁶ → 2×10¹⁰ N/m | Table 3 참조; k=2×10⁶ 에서 **+9.0 % 과대**, 저자 판정 *"too high to be acceptable"* | [5] p.72, Table 3 |
| 11 | **최대 접촉력** | 평저 사일로 배출 | E 70 MPa vs 70 GPa | 24 % 배출 후 **40.6 vs 364.4 (×10⁻⁴ N) = 8.98×** | [38] p.71 |
| 12 | 층압력강하 | 회전 유동층, CFD–DEM | k_n 80 → 80,000 N/m | k=80 에서 *"drops remarkably"*; 800–80,000 은 무영향 | [66] p.73, Fig 6 |
| 13 | 유동화 (점착 있을 때) | CFD–DEM, 표면에너지 0.37·3.7 mJ/m² | k_n 50 vs 50,000 N/m | 저강성+고점착 = **유동화 안 됨**; 고강성 = 층 부상 후 붕괴 | [63] p.73 |
| 14 | 접촉시간·최대접촉력 | 낙하시험 (단일입자) | k_n 10³ → 1.72×10⁷ N/m | Table 5: τ_c 1.61×10⁻³ → 1.23×10⁻⁵ s; f_n 1.97 → **258 N** | [62] p.73, Table 5 |
| 15 | 응집체 강성·파단변형 | bonded PFC2D/3D 단축압축 | bond k 3×10¹⁰ → 2×10¹¹ N m⁻³ | 강성↑ → 응집체강성↑, **파단변형↓** (ANOVA 95 % 유의) | [50] p.72 |
| 16 | **취성↔연성 전이** | BPM 사각충돌판 | bond k 5×10⁷ → 1×10⁹ N m⁻³ | 너무 낮으면 결합이 극단적으로 늘어 **취성→연성** 전환 | [52] p.72, Fig 4 |
| 17 | 압축성·파단개시·전단강도 | 1 mm 응집체 등방압축 0.01 m/s, PFC3D | K 0.5 / 1 / 2 MN/m (bond 강도 2 N 고정) | 강성↑ → 압축성↑, **파단 조기 개시**, 전단강도↓ | [53] p.72 |
| 18 | 탄성/소성 변형에너지비·압입력 | 나노실리카 응집체 나노압입, EDEM | bond 강성인자 1 → 2 | 에너지비 ↓, 파단 최대압입력 ↑ | [54] p.72, Fig 5 |

#### 5-B. E / G / k_n 에 **둔감** (거시응답 불변)

| # | 관측량 | 계 | 스윕 | 결과 | 출처·쪽 |
|---|---|---|---|---|---|
| 1 | 유동 패턴 | 경사 슈트, 단분산 비탄성 마찰구 | 오버랩 **1–10 %** | 영향 없음 | [25] p.67 |
| 2 | 운동학 | 범프 경사면 (유리구슬) | 최대 오버랩 < **1 % of 지름** | *"not very sensitive"* | [26] p.67 |
| 3 | 수치결과 일반 | 왕복 그레이트 | E = 3×10⁹ N/m² (평균 오버랩 0.5 %) | *"numerical results are **independent of E**"* | [27] p.70 |
| 4 | **정적 안식각** | 상자, 단분산구 | E **10⁵ → 10⁸ Pa** (기준 2.16×10⁶) | **±1°** | [28,57] p.67·70 |
| 5 | **정적 안식각** | **LIGGGHTS 1.5.3**, 비점착 | E **72(표)/75(본문) → 125 MPa** | 증가 시 −1°, 감소 시 +0.5°.  ★ *"static and rolling friction coefficients influence **up to two times more** the angle of repose than the elasticity parameter"* | [29] p.70 |
| 6 | 안식각 (고강성 쪽) | EDEM | **G > 10 MPa** | 영향 없음 | [23] p.70 |
| 7 | 호퍼 벽응력·배출률 | 2D 호퍼, 3가지 자체 접촉법칙 | 유효 수직강성 (지수 n = 36/72/144) | *"no influence"* | [36] p.71 |
| 8 | 호퍼 배출 | 3D | k 7.0×10³ → 7.0×10⁷ N/m | *"no major change"* | [37] p.71 |
| 9 | 배출량·유동프로파일·동역학 | 평저 사일로 | E 70 MPa vs 70 GPa (**÷1000**) | 유의차 없음 (연질이 더 **빨리** 배출) | [38] p.71 |
| 10 | **변형 (콘 관입)** | 자체 3D | E 2.9 → 29 GPa | *"did not find any discrepancy for the deformation"* | [24] p.70 |
| 11 | 볼밀 파워피크 | 자체 3D, 54.5×30.4 cm | k 4×10⁵ → 1.53×10⁸ N/m **및 206 GPa**; 선형↔비선형 모델 교체 | *"no influence detected"* (⚠ 실험 검증 없음) | [44] p.72 |
| 12 | **전단 정상상태 미시역학 (구)** | 3D 준정적 전단 | **K = k_t/k_n 0.25 → 1** | 구형은 *"almost no influence"* | [35] p.70–71, Table 2 |
| 13 | 전단 (과도기 제외) | PFC2D 연질 vs Contact Dynamics **강체** | k 1 N/m vs **무한강성** | 최대 주응력 차이는 **과도기에만**; *"the key effect during shearing is the **particle rearrangement** and not the elasticity"* | [33] p.70 |
| 14 | 유동화 (점착 없을 때) | CFD–DEM | k 50 vs 50,000 N/m | 차이 없음 | [63] p.73 |
| 15 | 유동층 거동 | 2D / 습·건 | 감소된 스프링상수 | 영향 없음; *"as long as sufficient collisions take place to have a **continuum-like behaviour**, the contact stiffness is not a sensitive parameter"* | [64][65] p.73 |
| 16 | 입자속도·분산 | 원심 스프레더 (spinning disc) | 2×10⁷ ± 3×10⁶ (Hertz 계수) | *"no influence"* | [67] p.74 |

**⇒ 우리 F-C2′ 에 직결되는 판정 3줄:**
- **σ_ionic 은 "E 에 둔감"이 아니다 — *직렬 사슬* 이다**: `E → (선형) 벌크계수 → (300 MPa 정압 하) porosity → σ`.
  **정압(stress-controlled) 프로토콜에서는 E-민감**하고, **정-porosity 로 비교하면 E-둔감**하다.
  우리 런은 전부 300 MPa servo = **앞쪽**이므로 σ 는 원리상 유효한 검증시험이다.
  ⚠ 단 **이득(gain)이 낮다** — 사슬이 두 단계라 dσ/dE 가 곱으로 희석된다.
- **가장 이득이 큰 E-검증시험은 리뷰가 이미 지목했다: 구속 *벌크계수*** (5-A #1–4, **4 그룹 독립,
  선형, 10×~10⁷× 폭**).  그리고 [21] 은 그것을 ***"once a stable hysteresis loop was reached"***
  즉 **제하–재하(unload–reload) 강성**으로 잰다 — 그것이 바로 우리 `hooke/hysteresis` 의
  **k₂(제하강성)** 가 지배하는 양이다.  ⇒ **§11 실행항목 ②**.
- **E-둔감 관측량으로 E 를 검증하려 들면 안 된다**: 안식각·유동패턴·배출률 유형은 이 리뷰에서
  **1000× 연화에도 안 움직인다**.  (우리 코퍼스에는 해당 관측량이 없으므로 실무 영향은 없다.)

---

### Q6. ★★ **입자 탄성 물성 *측정법* 과 문헌 E 값 범위**

**⛔ 측정법 장(章)이 없다.**  이 리뷰는 **DEM 결과의 민감도**만 다루고 물성 측정법을 리뷰하지 않는다
(§1 p.66: *"Experimental and theoretical findings regarding particle elasticity are **only discussed
if they are important for DEM simulations**."*).  측정과 관련해 등장하는 것은 **부수적으로 3건**:

| 방법 | 내용 | 출처 |
|---|---|---|
| **나노압입** | Schilde & Kwade — 나노구조 응집체의 미시역학 물성 측정, 100–600 °C 템퍼링으로 강성·강도를 **실험적으로 변화**시키고 그 값을 DEM 에 이식 | [54][55][56] p.72 |
| **입자/벽 Hertz 실험 → 입자/입자 환산** | 원심 스프레더: 입자–강판 접촉을 Hertz 로 재고 입자–입자로 환산.  *"stiffness diminishes by a factor **2√2** for R₁=R₂ and E₁=E₂ instead of R₁→∞ and E₁≫E₂"* | [67] p.74 |
| **낙하시험 물리 측정값** | k_n = 1.72×10⁷ N/m = *"identical to the physically measured value"* | [62] p.73 |

**⛔ 재료별 E 표도 없다.**  리뷰에 흩어진 값을 모으면 **10⁴ Pa ~ 206 GPa (7 자릿수)** 이고, 그 중
**실물 재료값으로 명시된 것**은 아래뿐이다:

| 값 | 정체 | 출처 |
|---|---|---|
| 70 GPa | 사일로의 "hard particle" (유리급) | [38] |
| 206 GPa | 볼밀 접촉강성 목록의 최상단 (강철급) | [44] |
| 29 / 9 / 2.9 GPa | 미결합 과립재(도로기층) | [24] |
| 3×10⁹ N/m² | 왕복그레이트에서 **오버랩 0.5 % 를 주도록 고른** 값 | [27] |
| 2.16×10⁶ N/m² | 안식각 연구의 "standard value" — ★ 리뷰가 직접 비판: *"**a variety of materials own a higher Young's modulus than applied in this numerical study**"* | [28] p.70 |
| 0.15–2.0 MPa | 분뇨(manure) | [34] |

⇒ **우리 22–24 GPa 는 이 리뷰가 다룬 어떤 계보다도 상단**([44]의 206 GPa 강철 다음)이고,
**우리 E_eff 1.35 GPa 는 이 리뷰의 *중앙*** (10⁶–10⁹ Pa 대역이 이 리뷰의 실질 작업영역)이다.
★ 즉 **"1.35 GPa 라는 값 자체가 이상하다"는 비판은 이 문헌군에서 성립하지 않는다** — 오히려
이 리뷰가 다루는 대다수 DEM 연구가 그 대역에서 돈다.  이상한 것은 **값이 아니라 재료 대비 배수와
응력 영역**이다 (그것이 §10 의 진짜 쟁점).

**★ 우리 연화배수를 리뷰의 감소배수와 나란히 놓으면 (감소배수 기준):**

| 연구 | 실물/기준값 | 사용값 | **감소 배수** |
|---|---|---|---|
| [66] Nakamura | Hertz 이론 3.8×10⁶ N/m | 80 N/m | **÷47,500** |
| [66] (저자가 "충분"이라 판정) | 3.8×10⁶ | 800 / 8,000 | **÷4,750 / ÷475** |
| [38] Xu | 70 GPa | 70 MPa | **÷1,000** |
| [5] Cleary & Hoyer (스윕 폭) | 2×10¹⁰ | 2×10⁶ | ÷10,000 |
| [23] Lommen (스윕 폭) | 10¹¹ Pa | 10⁴ Pa | ÷10⁷ |
| **우리 DEM** | **24 GPa** | **1.35 GPa** | **÷17.8** |

⇒ **배수만 보면 우리 18× 는 이 문헌군에서 가장 *작은* 축에 속한다.**  이것은 사실이고 인용 가능하다.
⚠ 그러나 **배수는 옳은 자가 아니다** — 옳은 자는 **결과 오버랩**이고, 그것은 배수가 아니라
**σ_press/E** 가 정한다 (§10-(b)).

---

### Q7. ★ **고응력·치밀 압밀을 다루는가?  → ⛔ 다루지 않는다.**

리뷰 전체에서 **명시된 최대 응력**을 모으면:

| 시험 | 응력 | 출처 |
|---|---|---|
| 구속압축(오이도미터) | **0 → 80 kPa** | [21] Table 4 |
| 무구속 분말압축 | **16 / 36 / 56 / 76 / 96 kPa** | [32] Table 4 |
| 이축 전단시험 | **5 → 25 kPa** | [33] Table 4 |
| 직접전단 (수직응력) | Fig 3 축값 (텍스트 미기재, **digitize 안 함**) | [34] |

⇒ **최대 ≈ 96 kPa = 0.096 MPa.  우리 300 MPa 는 그 3,125 배다.**
응집체 파쇄 연구([50][52][53][54])는 국소응력이 높지만 **단일 응집체 파괴** 문제이고 탄성
파라미터가 **bond stiffness** 라 우리 계와 대응하지 않는다.

**소성 접촉법칙 커버리지도 사실상 0** — 리뷰 대상 중 소성 LAW 는 **[32] Thakur (adhesive
elasto-plastic, EDEM v2.4)** **1 편**뿐이고, 그마저 **E 가 아니라 접촉소성도 λ_p 를 스윕**한다:
```
λ_p = 1 − k_n,load / k_n,unload      (λ_p = 0 완전탄성 · λ_p = 1 완전소성)
λ_p ∈ {0, 0.2, 0.5, 0.8, 0.9, 0.99}
```
결과: λ_p ↑ → ① flow function ↑ ② **접촉이 더 많이 성립 → 응집력 ↑** ③ 벌크소성
(= 소성변형/전변형) ↑ (§2.2 p.70).
★ 이것이 리뷰 전체에서 **우리 `hooke/hysteresis` 와 같은 층(層)에 있는 유일한 항목**이며,
그 메시지는 우리에게 유리하다 — **접촉 이력(소성)을 키우면 벌크가 더 조밀·응집적이 된다**,
즉 우리 hysteresis 경로가 **강성 연화와 *별개의* 치밀화 레버**를 이미 갖고 있다는 뜻이다.
⚠ Table 4 의 *"k_n,load = 1 kN/m and k_n,unload = 1 kN/m"* 는 λ_p ≠ 0 을 만들 수 없다 =
**오식으로 보임** (§9).

---

### Q8. ★ **저자들이 권고하는 실천 (보고 규약 · 검증 · 민감도 절차)**

| # | 권고 | 원문 근거 |
|---|---|---|
| 1 | **코드 · 접촉모델 · "탄성 파라미터의 정의"를 함께 보고하라** — Table 4/6 을 그렇게 짠 이유를 명시 | §2 p.67: *"Attention was especially paid to indicate applied **codes, contact models and the definition of the elastic parameter** so that the reader can distinguish important information."* |
| 2 | **코드가 다르면 같은 접촉법칙도 다르게 구현되고 다른 물성값이 필요하다** ⇒ 시뮬레이션 간 비교는 어렵다 | §5 p.75: *"the same contact law might be implemented differently in another simulation code and thus, **different material properties are needed**"* |
| 3 | **접촉법칙이 재료 변형거동을 잘 표현해야 실측값을 쓸 수 있다** | §5 p.75: *"a contact law should well represent a material's deformation behaviour during contact and then **an experimentally measurable value can be applied**.  Otherwise, information will get lost and the computed physical response might be false or rather quantitative than qualitative."* (⚠ 마지막 절은 어순이 뒤집힌 듯 — §9) |
| 4 | **파라미터 교차상관을 확인하라** — 예: COR 이 강성비에 종속 | §4 p.75: *"the elastic parameter may **directly affect other simulation parameter** as for instance the coefficient of restitution: For the simple linear contact model [14] the coefficient of restitution in normal direction corresponds to **the square root of loading to unloading stiffness** [26]."* + *"more than one simulation parameter can be the deterministic factor"* [21,29] |
| 5 | **오버랩 기준으로 감소 한계를 정하라**; 격렬한 계는 **최대**, 덜 격렬한 계는 **평균** 오버랩 사용 | §4 p.75 (Q2 원문) |
| 6 | **밀할수록 더 신중히 고르라** | §5 p.75 (Q3 원문) |
| 7 | **단일입자 연구에는 실측값이 필수** | §3.1 p.73: *"for single particle investigations the use of the **real particle and interparticle parameters is crucial** for obtaining reliable results"* |
| 8 | 접촉모델 간 **광범위 비교연구**가 필요 (첫 시도 = [34]) | §4 p.75 |
| 9 | **미해결 지목**: 분말 벌크거동의 접촉강성 영향 · 입자 **upscaling** 시 강성 영향 | §4 p.75 (§3 범위상자) |

⚠ **권고 4번은 우리에게 즉시 감사(audit) 항목이다** — LIGGGHTS `hooke/hysteresis` 는 제하강성
비 k̂₂ = k₂/k₁ 를 갖는다(우리 `contact_models_layer_map.md` §1: *"k̂₂/k_c/φ_f = m6/m7/m8"*).
Paulick 의 관계 `e = √(k_load/k_unload) = 1/√k̂₂` 가 우리 입력덱의 **명시 COR 과 일치하는지
확인된 적이 없다.**  ⇒ **§11 실행항목 ④.**  (값은 여기서 **n/a** — 우리 덱을 안 열어봤다.)

---

## 6. 섹션별 상세 (읽은 그대로 — 카드만으로 논문을 읽은 것과 같게)

### §1 Particulate solids in contact (p.66–67)
- 목적 선언: *"this review focuses on **the effect of elasticity properties of individual particles
  and, to some extent, of a bulk of particles on DEM simulations**."*
- Cundall & Strack 1979 [1] 이후 코드 [8–10] 와 접촉모델 [11–18] 이 각 그룹별로 발전 — 목적이
  **응용 기술(記述)** 이거나 **반대로 단순화·시간단축**이었다고 명시.
- 가장 널리 쓰이는 접촉모델 = **선형 Hooke** 또는 **비선형 Hertz**.
- 탄성 파라미터의 **두 역할**: ① 접촉 변형거동 ② **시간간격의 기준** (Eq. 2).
- 리뷰의 구성 원리 = **Table 1 의 regime 분류**.

**Table 1 (p.67) — 공정공학 regime 개관** (원표 전재):

| 입자 상태 | **정적(Static)** | **동적(Dynamic)** |
|---|---|---|
| **Dense** | Storage · **Compression** · Shear cell · Angle of repose | Mixing (rotating drum) · Milling of particle beds · Silo filling and discharge · Belt or screw conveyor · Coating |
| **Dilute** | Sedimentation | Drop test · Fluidised bed · Pneumatic conveying · Spraying (jets, granulating) |
| **Agglomerates (dense)** | Silo storage · Bulk compression and shearing | Milling · Conveying (belt, screw, pneumatic) · Drop test · Fluidised bed |

★ **우리 자리** = Dense × Static × **Compression** (좌상단 칸).  리뷰가 "가장 강성이 중요하다"고
판정한 사분면이며, 동시에 리뷰가 다룬 **응력이 가장 낮은**(≤ 96 kPa) 칸이다.

### §2 Dense particle systems (p.67–72)
**dense 의 정의** = *"a particle packing in which the particles are in contact with each other
during **almost the whole process time**"* (p.67).

#### §2.1 Laboratory experiments (p.67–70)
- **[25] Walton 1993** — 경사 슈트, 단분산·비탄성·마찰구.  *"the flow pattern … is **not affected by
  a reduced elasticity as long as the overlap stays within a range of 1–10 %**"*.
  (Table 4: 코드·접촉모델·탄성정의 **전부 미명시**.)
- **[26] Hanes & Walton 2000** — 범프 경사면 유리구슬, 실험+수치.  코드 **3D SHEAR**, 선형
  `F_n = k_{n,load}·δ` (하중) / `k_{n,unload}·(δ−δ₀)` (제하), δ₀ = 완전제하 시 잔류 상대오버랩.
  *"for overlaps **smaller than 1 % of the particle diameter during the strongest appearing
  collision**, the kinematics were not very sensitive to the stiffness value."*  추가 관찰:
  **더 탄성적일수록 더 에너지 높은 유동 → 더 느린 유동.**
- **[27] Liyan 2013** — 수평 왕복 그레이트, 2D 비선형.  E = 3×10⁹ N/m² 를 **평균 오버랩 0.5 % 가
  되도록** 고름 → *"numerical results are independent of E"*.
- **[28,57] Zhou 2001** — 정적 안식각, 단분산구, Cundall–Strack + rolling friction, `E* = E/(2(1−ν²))`.
  E **10⁵ → 2.16×10⁶ → 10⁸ Pa** → **각도 변화 1° 이내**.  ★ 리뷰의 논평: *"a variety of materials
  own a **higher** Young's modulus than applied in this numerical study."*
- **[29] Combarros 2013 (Kwade 그룹, LIGGGHTS 1.5.3, Hertz–Mindlin)** — 비점착 재료.
  본문 **75 → 100 → 125 MPa** (Table 4 는 **72**, §9 참조).  증가 시 **−1°**, 감소 시 **+0.5°**.
  ★ *"the static and rolling friction coefficients influence **up to two times more** the angle of
  repose than the elasticity parameter."*
- **[23] Lommen 2013 (EDEM)** — 챔버를 채우고 측판을 내려 흘러내리게 함.
  **G < 10 MPa** 에서 **28° → 26° → 23° → 12°** 급락; **G > 10 MPa** 이면 무영향.
  리뷰 총평: *"a **very low elasticity value, e.g. below 10 MPa, highly changes** the obtained angle.
  An increase of elasticity value affects the static angle of repose **probably less** due to other,
  more influencing simulation parameters."*

#### §2.2 Bulk compression and shearing (p.70–71) ★ 우리와 가장 가까운 절
- **[21] Coetzee & Els 2009** — PFC2D 구속압축 (D 0.25 m, H 0.08 m, **0→80 kPa**), k_n 10–500 kN/m.
  **k_n ↔ 구속 벌크계수 = 선형** (**안정 이력루프 도달 후의 압축 사이클** 기준 — 이 조건이 핵심).
  **마찰 0.1–0.3 변화는 압축거동에 영향 없음** (= 압축시험이 마찰을 고립시킨다는 우리 F-C1 의 문헌근거).
  ⇒ Fig 1.
- **[30] Coetzee 2010** — PFC3D, **비구형**, 더 큰 실린더(D 0.4, H 0.25 m).  위 결과를 검증하고
  *"stiffness is major parameter to influence load–displacement behaviour of rock material"*.
- **[31] Antony 2005** — 2D vs 3D 단축압축 (구·비구, 실험 대조).  **2D 는 벌크강성을 상당히
  과소평가**하고 특히 **큰 변형에서 심함**; **3D 는 실험과 잘 일치**.
  ★ 우리 2D↔3D 규약 경고의 문헌 근거 (우리 MPM 2D σ_y 0.15 → 3D 0.30 필요와 같은 방향).
- **[23] Lommen 2013** — EDEM H–M, **18,000 입자**, 수평 주기경계, **G 10⁴ → 10¹¹ Pa**.
  **G ↔ 측정 벌크강성 = 선형** (Coetzee & Els 와 같은 결론).
  **하한 존재**: *"Below 10⁴ Pa the contacts could not generate enough force to reverse the
  direction of the mass motion."*
- **[24] Yohannes 2013** — 동적 콘 관입, resilient modulus(= 최대 편차응력/탄성변형) 도입.
  **E 2.9 / 9 / 29 GPa → *변형* 은 차이 없음**, 그러나 **E ↔ 성립 벌크계수 = 선형**.
- **[23] Lommen** 콘 관입(쐐기, base 40 mm, 30°, 8 mm/s): **G 10⁸–10⁹ → 11–14 J**,
  **G 10⁴–10⁶ → 1–6 J** = 저항을 **절반으로 과소평가**.
- **[32] Thakur 2014** — Q7 참조 (리뷰 유일의 소성 LAW).
- **[21] Coetzee & Els 전단시험** — k_n 10 → 500 kN/m, 내부마찰각 Φ.  **임계 100 kN/m.**
  교차상관: μ 0.1 → 0.3 에서 강성 100 → 520 kN/m 로 올리면 Φ **30° → ~38°**. ⇒ Fig 2.
- **[33] Kadau 2006** — PFC2D 연질 전단 vs **Contact Dynamics 강체** 전단, 약 800 원판, 정응력.
  압축 후 탄성 효과는 **과도기에만** (탄성입자의 최대 주응력 피크, 팽창 단계에서 감소).
  ★ *"the key effect during shearing is **the particle rearrangement and not the elasticity** of
  the used materials."*
- **[34] Landry 2006** — Q4-③ 참조. ⇒ Fig 3.
- **[35] Antony 2006** — Q4-④ 참조. ⇒ Table 2.

**★ 절 종합 문단 (p.71) — 이 논문에서 우리에게 가장 중요한 문단, 전문 인용:**
> *"The presented work well demonstrates the **major impact of the microscopic stiffness on the
> macroscopic bulk behaviour** of cohesionless materials.  Regarding compression behaviour the
> stiffness value has the most significant impact **as long as real particle geometries are applied
> and no ideal spherical particle shapes are used**.  For the case of spherical shapes, **the
> friction coefficient becomes more important** as it must be implemented to incorporate
> interlocking and particle sliding.  All authors found a **linear relationship** between the applied
> elastic parameter (contact stiffness, particle stiffness or shear modulus) and the bulk modulus
> which **enables the DEM user to scale down the stiffness parameter** for this specific application
> and for determining the bulk modulus.  **However, a scale down in stiffness leads to a different
> compression behaviour** and, thus, **different force chains and distributions of normal force
> values may develop** [33,35]."*

★ 이 문단에는 **우리에게 불리한 줄이 하나 더** 있다: **"구를 쓰면 강성보다 마찰이 더 중요해진다."**
우리는 구를 쓴다.  ⇒ **F-C1(마찰 민감도 미측정)의 시급성이 이 리뷰로 한 단계 올라간다.**

#### §2.3 Silo flow (p.71) — [36][37][38], Q1 표의 Xu 수치 포함
#### §2.4 Mixing and milling (p.72)
- **[44] Mishra & Murty 2001** — 볼밀.  **비선형 → 등가선형 + 강성 감소**로 바꿔도 파워피크가
  비슷 → 영향 없음.  ⚠ *"**no experimental validation was carried out**"*.
- **[5] Cleary & Hoyer 2000** — 원심밀, 695 rpm.  ★ 리뷰의 평: *"They are one of the firsts to
  recognise that **simulation may not predict the correct behaviour but that a validation between
  experiment and simulation helps to identify sensitive parameters** for specific applications."*

**Table 3 (p.67) — 스프링강성 ↔ 비출력·오버랩 (Cleary & Hoyer [5]) (원표 전재, 전부 stated):**

| k_n [N/m] | 비출력 [−] | 파워드로 과대예측 [%] | 평균 오버랩 [%] | 최대 오버랩 [%] |
|---|---|---|---|---|
| 2×10⁶ | 0.2732 | **9.0** | 3.6 | **55.0** |
| 2×10⁷ | 0.2647 | 5.6 | **0.6** | 15.0 |
| 2×10⁸ | 0.2544 | 1.5 | 0.11 | 3.5 |
| 2×10⁹ | 0.2527 | 0.8 | 0.01 | 0.9 |
| 2×10¹⁰ | 0.2507 | – | 0.003 | 0.25 |

리뷰 본문: *"a 9 % over-prediction of the specific power for k = 2×10⁶ N/m is **too high to be
acceptable** and … therefore **the elasticity parameter should not be as reduced as it is often
done** in simulations.  According to Cleary and Hoyer a **mean particle overlap of around 0.6 % of
the particle radius** is tolerable to obtain qualitatively good flow patterns."*
⚠ Table 3 은 오버랩의 밑변(반지름/지름)을 **표기하지 않는다**; 본문만 **radius** 라 말한다.
★ 이 표는 **평균 오버랩이 0.6 % 일 때 최대 오버랩이 15 %** 임을 보여준다 = **평균/최대 비 25×**.
⇒ Q2 의 "평균 쓸까 최대 쓸까"가 **25 배 차이의 선택**이라는 정량 증거.

#### §2.5 Agglomerates (p.72)
- 두 관점: ① 결합된 소입자 집합 = 하나의 **1차 입자**(파괴 연구) ② 여러 1차 입자의 **응집체**
  (정제·인스턴트커피).
- ★ 느슨한 응집체의 입자간 힘(auto-adhesion, friction, liquid binding [45–48])은
  ***"None of these interparticle forces are dependent on an elastic parameter."***
  ⇒ 탄성 영향은 **bond 강도나 입자 자체 탄성을 고려할 때만** 생긴다.
- [49] Moreno-Atanasio & Ghadiri, [50] Hanley (Taguchi+ANOVA), [51] Ergenzinger
  (*"stiff unbonded interactions lead to more brittle failure"*), [52] Metzger (Fig 4 4구역),
  [53] Nakata, [54] Schilde (Fig 5).  전부 Q5-A #15–18 에 정리.

### §3 Dilute or particle/fluid systems (p.72–74)
- **§3.1 단일입자** — [62] Di Renzo & Di Maio (Table 5), [23] Lommen.
  ★ 결론: *"for single particle investigations the use of the **real** particle and interparticle
  parameters is **crucial**"*.

**Table 5 (p.73) — 접촉강성 ↔ 접촉시간·오버랩·힘 (Di Renzo & Di Maio [62]) (원표 전재):**

| k_n [N/m] | 접촉시간 τ_c [s] | 최대 오버랩 δ_n,max [m] | 최대 접촉력 f_n,max [N] |
|---|---|---|---|
| 1×10³ | 1.61×10⁻³ | 1.79×10⁻³ | 1.97 |
| 1×10⁴ | 5.08×10⁻⁴ | 6.21×10⁻⁴ | 6.21 |
| 5×10⁴ | 2.27×10⁻⁴ | 2.78×10⁻⁴ | 13.9 |
| 1×10⁵ | 1.61×10⁻⁴ | 1.97×10⁻⁴ | 19.7 |
| 1×10⁶ | 5.08×10⁻⁵ | 6.21×10⁻⁵ | 62.1 |
| **1.72×10⁷** (= 물리 실측값) | 1.23×10⁻⁵ | 1.50×10⁻⁵ | **258** |

리뷰의 해석: *"An increase in stiffness decreases the contact duration and **since the material is
stiffer, less deformation occurs and forces are calculated more accurately, which leads to higher
force values**."*
★ **k_n 을 10⁴ 배 낮추면 최대힘이 131× 낮게 계산된다** (258 → 1.97 N).  **연화는 힘을 체계적으로
과소평가한다** — 부호가 명확하다.  (⚠ 이것은 **단일 충돌**이고, 우리는 구속 정적압축이라 힘이
플래튼 응력으로 서보된다 = 직접 전이되지 않는다.  그러나 **접촉당 힘 분포**에는 같은 방향의
압력이 있다 → Q1 의 Xu [38] 최대힘 9× 와 같은 이야기.)

- **§3.2 다수입자** — [63] Moreno-Atanasio (점착 결합 시 강성이 유동화 여부를 가름),
  [64] Tsuji, [65] Mikami (*"continuum-like behaviour"* 조건), [66] Nakamura (Fig 6),
  [67] Van Liedekerke.
  총평: *"for dilute systems with multiple particles the chosen contact model and, therefore, a
  correct stiffness value **might not be very important** if the particles can be seen as continuum
  phase and **solid–fluid interactions govern** the system's behaviour."*
  단서: 무한강성 hard-sphere [68] 로 도망가거나 과도하게 낮추기보다 [64] 의 충돌동역학 모델을
  쓰라; **표면에너지 등과의 교차관계**를 보려면 *"more reliable, realistic elasticity parameters
  are necessary"*.

### §4 Discussion (p.75) — Q2·Q8 원문 소재
### §5 Conclusions (p.75) — Q3·Q2 원문 소재
### Acknowledgements (p.75) — Marie Curie ITN · Deutsch-Französische Hochschule · PARDEM 동료

---

## 7. Figure set ★ (6장 전부 **타 논문 재현/단순화 도판**)

⚠ **이 세션에서 PDF 를 렌더할 수 없었다** (`pdftoppm`/`pdftotext` 부재; 텍스트 추출본만 사용).
따라서 **축 눈금·데이터점은 읽지 않았고 digitize 하지 않았다.**  아래는 **캡션 + 본문 서술**로만
구성한 것이며, 숫자는 전부 **본문 stated 값**이다.

| Fig | 쪽 | 내용 (캡션 그대로) | 본문이 말하는 것 | **우리가 재사용할 것** |
|---|---|---|---|---|
| **1** | 71 | *"Effect of spring stiffness and friction coefficient on the **bulk modulus** during confined compression as performed by Coetzee and Els [21]"* | k_n 10–500 kN/m ↔ 구속 벌크계수 **선형**; μ 0.1–0.3 무영향 | ★★★ **우리 E-검증 그림의 양식 원형**.  x = k_n(또는 E_eff), y = 구속 벌크계수, 계열 = μ.  여기에 **실험 밴드**를 얹으면 F-C1(마찰 고립)과 F-C2′(민감한 검증시험)를 **한 장에** 해결 |
| **2** | 71 | *"Effect of spring stiffness k_n and particle–particle friction coefficient μ on the **internal friction angle Φ** in shear simulation [21]"* | 임계 100 kN/m; μ 의존 교차상관 | ★ **파라미터 교차상관을 보이는 양식** (우리 F-C1 OAT 표의 그림판) |
| **3(a,b)** | 71 | *"Effect of **normal stress on the maximum shear stress** [34] for (a) linear contact with different **Young's moduli** and (b) Hertz–Mindlin with different **shear moduli**"* | 같은 0.15–2.0 MPa 를 E 로 넣을 때와 G 로 넣을 때 응집력 응답이 다름 (18→78 vs 25→35 kPa) | ★★ **"E 냐 G 냐"를 한 장으로 보이는 그림** — 지도교수 Q4 답변 슬라이드에 그대로 쓸 구조 |
| **4** | 72 | *"**Phase map of breakage types** for various combinations of stiffness and strength [52]"* — x=완전분해, □=파괴없음, ○=부분파괴, 무기호 하단 = 비현실 영역 | bond 강성 5×10⁷–1×10⁹ N m⁻³ × 임계 bond 강도의 4구역 | ★ **"강성-강도 상평면"** 양식 — 우리 Auerbach/fracture 게이트를 (E_eff, G_c) 평면에 그릴 때 참조 |
| **5(a,b)** | 73 | *"Effect of **solid bond stiffness and tempering temperature** on (a) the ratio of the **elastic and plastic deformation energies** and (b) on the **maximum indentation force** [54]"* | 강성 ↑ → 탄성/소성 에너지비 ↓, 파단 압입력 ↑ | ★ **탄성/소성 에너지 분해를 y축으로 쓰는 양식** (우리 Stage-E 탄성↔소성 면적 분해에 대응) |
| **6** | 75 | *"Effect of spring stiffness on the correlation between calculated **bed pressure drop and gas velocity** [66]; here **simplified presentation**"* | k=80 N/m 은 크게 어긋남; 800–80,000 은 무영향 | (희박계 — 우리 재사용 없음) |

★ **재사용 우선순위 1 = Fig 1 양식.**  우리 F-C2′ 의 답이 "구속 벌크계수(제하–재하)를 재라"이므로,
그 결과 그림은 Fig 1 과 **같은 축**을 갖는 것이 리뷰-정합적이다.

---

## 8. Post-processing / 방법론 도구 (이 리뷰가 카탈로그한 것)

| 도구 | 정의 | 출처 | 우리 대응 |
|---|---|---|---|
| **평균 / 최대 오버랩 %** | 강성 감소 허용도의 판정량; 격렬한 계는 max, 덜 격렬하면 mean | §4 p.75, Table 3, Table 5 | 우리 ⟨δ⟩/d — **이미 낸다**.  ⚠ 최대 오버랩은 **리포트한 적 없음** (실행항목 ③) |
| **구속 벌크계수 (안정 이력루프 후)** | 오이도미터 압축–제하 사이클의 기울기 | [21] p.70 | **미보유** → 실행항목 ② |
| **Resilient modulus** | 최대 편차응력 / 탄성변형 | [24] p.70 | 미보유 (동적 관입 전용) |
| **접촉소성도 λ_p = 1 − k_load/k_unload** | 0 = 완전탄성, 1 = 완전소성 | [32] p.70 | ★ 우리 `hooke/hysteresis` 의 k̂₂ 와 **같은 양의 역수 관계** — 실행항목 ④ |
| **벌크소성도** = 소성 벌크변형 / 총 변형 | | [32] p.70 | 우리 MPM Σdg 의 벌크판 — **비교 가능** |
| **스프링강성비 K = k_t / k_n** | 접선/수직 강성비 | [35] p.70 | LIGGGHTS 기본값 확인 필요 |
| **Sliding fraction / Sliding energy ratio** | 미끄럼 접촉수/총 접촉수 · 미끄럼 소산에너지/총 일 (Table 2 각주) | [35] p.67 | 미보유 (우리 force-chain 진단에 추가 가능) |
| **Flow function · 무구속강도** | 분말 유동성 지표 | [32] p.70 | 미보유 |
| **Taguchi + ANOVA marginal means** | DEM 보정의 통계적 설계 | [50] p.72 | 우리 OAT/LHS 대안 |
| **무차원군 (Weber 대체)** | 탄성계수·ν·밀도·직경·bond 강도 → 파단접촉수 | [49] p.72 | 우리 Auerbach 무차원화와 같은 계열 |
| **Rayleigh Δt (20 %)** | Eq. (2) | [8] p.67 | LIGGGHTS 도 같은 계열 — 우리 Δt 감사 근거 |

---

## 9. ⚠ 원문 내부 불일치 · 오식 목록 (재인용 점검용 — 우리가 실제로 읽고 잡은 것)

| # | 위치 | 본문 | 표 | 판정 |
|---|---|---|---|---|
| 1 | [29] Combarros E 범위 | *"changed from **75** to 100 to 125 MPa"* (p.70) | *"E-modulus: **72**, 100 and 125 MPa"* (Table 4 p.68) | **불일치.**  인용 시 *"72 또는 75 MPa (논문 내 불일치)"* 로 적을 것 |
| 2 | [34] Landry 비선형 응집력 | *"the cohesion … **lies here between 5 and 25**"* (p.70, 단위 없음) | *"cohesion from about **25 kPa to 35 kPa**"* (Table 4 p.68) | **불일치.**  이 카드는 Table 값을 채택하고 병기함 |
| 3 | [5] Cleary & Hoyer 오버랩 밑변 | *"0.6 % of the particle **radius**"* (p.72) | Table 3 열 제목 *"Mean overlap [%]"* — **밑변 미표기** | 표만 보면 지름으로 오독 가능 → **2× 오차원** |
| 4 | [32] Thakur 강성 | Table 4: *"k_n,load = **1 kN/m** and k_n,unload = **1 kN/m**"* | — | **오식으로 보임** — 둘이 같으면 λ_p ≡ 0 이라 λ_p ∈ {0…0.99} 스윕이 불가능 |
| 5 | [54] Schilde bond 강성 단위 | *"1; 1.25; 1.5 and 2 **Nm⁻³**"* | 같은 칸의 식은 `k_n,bond = N_sf·π·r_bond·E*` 로 **N_sf = 비례상수(무차원)** | 값 1–2 는 **N_sf 로 보이고 Nm⁻³ 라벨은 부정합** |
| 6 | [67] Van Liedekerke 단위 | *"2·10⁷ ± 3·10⁶ **Nm⁻³/²**"* (Table 6·본문) | Hertz 강성 차원은 **N·m^(−3/2)** 로 쓰는 것이 일반 (표기가 `N/m^{-3/2}` 로 뒤집혀 있음) | 표기 오류로 보임 |
| 7 | §5 결론 문장 | *"the computed physical response might be false or rather **quantitative than qualitative**"* | — | 어순이 뒤집힌 듯 (통상 *"qualitative rather than quantitative"*).  **원문 그대로 인용하고 해석은 붙이지 말 것** |
| 8 | [25] Walton 오버랩 범위 | *"within a range of **1–10 %**"* — **밑변 미명시** | Table 4: 탄성정의 *"Not specified"* | 최상단 허용치이므로 **반드시 "밑변 미명시" 를 병기**해야 함 |

★ **이 목록이 §10-(d) 판정의 근거이기도 하다** — 이 리뷰는 1차 자료를 옮기는 과정에서
**밑변·단위·값이 흔들린다**.  따라서 이 리뷰를 재인용할 때는 **반드시 원 표기와 밑변을 함께**
적어야 한다.

---

## 10. ★★★ 우리 DEM+MPM 대비 — **판정 4개** → `our_dem_baseline.md`

### 사전 정리 — 우리 값과 이 리뷰의 자(尺)를 같은 단위로

| 우리 항목 | 값 | 이 리뷰의 대응 자 |
|---|---|---|
| E_SE 실물 | **22–24 GPa** | 이 리뷰 최상단 [44] 206 GPa 다음 대역 |
| **E_SE,eff (DEM)** | **1.35 GPa** | 이 리뷰의 **중앙 작업대역**(10⁶–10⁹ Pa) |
| 연화 배수 | **÷17.8** | 이 리뷰의 감소 배수들(÷47.5 ~ ÷47,500) 중 **가장 작은 축** |
| MPM (E, ν, σ_y) | **1.53 GPa · 0.49 · 0.30 GPa** | E·ν 는 Eq. (1) 대상; **σ_y 는 이 리뷰의 소관 밖** (탄성 리뷰) |
| 유도 G (MPM) | **0.5134 GPa** (DFT 쌍 대비 **÷15.8**) | Eq. (1) |
| 유도 K (MPM) | **25.5 GPa** (우리 DFT B₀ 26.23 의 **97.2 %**) | — |
| pure-SE ⟨δ⟩ | **지름의 11–12 %** (= 반지름의 22–24 %) | 리뷰 종합 기준 **지름의 1 %** |
| 압밀 응력 | **300 MPa** | 리뷰 최대 **≈96 kPa** (**3,125×**) |
| 접촉법칙 | LIGGGHTS **hooke/hysteresis** (이력, **항복캡 없음**) | 리뷰의 소성 LAW 커버리지 = [32] **1 편** |

### ★ (a) **이 리뷰는 우리 18× 연화를 허용하는가, 금지하는가, 침묵하는가?**

> ## **판정: 침묵한다 (SILENT) — 단, 한 문장의 허가와 한 문장의 청구서를 남긴다.**

세 갈래로 나눠 정확히:

**① 우리 용도(= (b) 벌크-맞춤 보정)에 대한 *사례* 로는 침묵한다.**
이 리뷰 어디에도 "실험 벌크 곡선에 맞추려고 E 를 N 배 낮췄다"는 사례가 **없다** (Q1).
따라서 이 리뷰는 우리 절차의 선례를 제공하지 **못한다**.  ⇒ 선례는 **Coetzee 2017 의 Bulk
Calibration Approach 장**에서 가져와야 하고, 이 카드에서 가져올 것은 **선례가 아니라 물리**다.

**② 원리적으로는 *허가* 한다 — 그것도 명시적으로.**
§2.2 p.71: *"a **linear relationship** … **enables the DEM user to scale down the stiffness
parameter** for this specific application and for determining the bulk modulus."*
선형·단조 사상은 역함수를 갖는다 ⇒ **"원하는 벌크계수를 주는 강성을 고르는 것"이 이 리뷰의
자체 논리로 정당하다.**  독립 4 그룹·독립 4 코드·10×~10⁷× 폭에서 확인된 관계다.
⇒ **우리 porosity@300 MPa 보정은 이 문장의 사정권 안에 있다.**

**③ 동시에 *청구서* 를 붙인다 — 그리고 그 청구서가 하필 우리 전달 계산 앞으로 온다.**
같은 문단: *"a scale down in stiffness leads to a **different compression behaviour** and, thus,
**different force chains and distributions of normal force values** may develop."*
정량 예시 = Xu [38]: **÷1000 연화에서 평균힘 1.5×, 최대힘 9.0×** (Q1 표).
우리 σ_ionic/σ_e/κ 는 **접촉당 힘 → 접촉면적 A(δ) → Holm R = 1/(2σ r_c)** 로 만들어진다
⇒ **연화가 가장 많이 오염시키는 양이 하필 우리 전달망의 입력이다.**
⚠ 이것을 **완충하지 말 것**: 이 리뷰의 자로 재면 **"porosity 는 맞춰도 되고, 힘 분포는 못 믿는다"**
가 정확한 판정이다.  (우리 대응은 이미 부분적으로 존재한다 — **Stage-E 5-regime capped area**
가 과압축 접촉의 면적 과대보고를 막고, MPM 이 독립 이산화로 σ 를 두 번째로 낸다.  그러나
**힘 분포 자체를 실험과 대조한 적은 없다.**)

**④ 배수 자체는 이 문헌군에서 *작다*.**  ÷17.8 은 [66]의 ÷475–4,750(저자가 "충분"이라 판정한 값),
[38]의 ÷1,000 보다 작다.  ⇒ *"18 배가 허무맹랑하게 크다"* 는 비판은 **이 리뷰의 자로는 성립하지
않는다.**  성립하는 비판은 **"어느 응력 영역에서 그 배수를 쓰느냐"** 다 (→ (b)).

**⑤ 리뷰의 headline 은 우리에게 *경고* 이지 *금지* 가 아니다.**  *"the denser the system, the more
carefully the elastic parameter must be chosen"* — "carefully" 이지 "not at all" 이 아니다.
그리고 그 경고는 **정확히 우리가 하고 있는 것**(실험 앵커에 맞춰 신중히 고르기)을 가리킨다.

**⑥ ⚠ 우리에게 불리한 잔여 하나 — 구(sphere) 조항.**
§2.2 p.71: *"the stiffness value has the most significant impact **as long as real particle
geometries are applied and no ideal spherical particle shapes are used**.  For the case of spherical
shapes, **the friction coefficient becomes more important**."*
⇒ 구를 쓰는 우리에게는 리뷰가 **"마찰이 더 중요하다"**고 말한다.  우리는 **마찰을 문헌값으로
고정하고 한 번도 민감도를 재지 않았다** (F-C1).  ⇒ **이 카드가 F-C1 의 우선순위를 올린다.**

---

### ★ (b) **우리 오버랩 11–12 %(지름)는 이 가드레일의 *실제 위반* 인가, *범위 밖* 인가?**

> ## **판정: 규칙으로서는 범위 밖(OUT OF SCOPE).  물리로서는 실재하는 위반 — 단 그 위반은 우리 *보정 선택* 이 아니라 *탄성-구 DEM 이라는 클래스 전체* 가 300 MPa 에서 저지르는 것이다.**

**① 규칙으로서 범위 밖인 이유 — 3중.**
- **목적 불일치**: 이 기준은 *"a **reduction** of the elastic parameter did not show a major change"*
  의 조건, 즉 **(a) 속도용 감소의 무해성** 보증이다.  우리는 (b)다.  (a)의 가드레일로 (b)를
  방어하거나 재는 것은 **범주 오류**다 (Coetzee 카드 §7 의 (a)/(b) 혼용 금지와 같은 규율).
- **계 불일치**: 근거 5/5 가 **자유표면·유동·대기압** 계다 (Q2 표).  구속 300 MPa 압밀은 0 건.
- **접촉법칙 불일치**: 기준의 두 번째 목적이 *"for **elastic deformation as foreseen by Hertz**"*
  인데, 우리는 **Hertz 탄성 접촉을 주장하지 않는다** — `hooke/hysteresis` 는 **이력(비가역)
  법칙**이고, 접촉 *면적* 은 Stage-E 에서 **소성(Tabor+volume)** 으로 재유도한다.

**② 그럼에도 물리로서 실재하는 위반 — 숨기지 않고 적는다.**
δ/d = 0.115 ⇒ δ/R = 0.23.  같은 반지름 두 구의 **기하학적 렌즈 접촉반경**
`a² = Rδ − δ²/4` 로 **a/R ≈ 0.46–0.47** (δ/d 11–12 %), Hertz 정의 `a = √(R*δ)` 로는 **a/R ≈ 0.34**.
⇒ **접촉 패치가 입자 반지름의 절반**이다.  이 규모에서는
(i) 어떤 해석적 단일접촉 법칙(탄성이든 이력이든)의 **소변형 가정이 무너지고**,
(ii) 한 입자 위의 이웃 접촉들이 **더 이상 독립이 아니다** ⇒ **multi-contact 보정이 선택이 아니라
필수**가 된다 (정본 `giannis2021_stress_based_multicontact_dem` · Varkey 2026 이 그 자리).
⇒ **이 위반은 정직하게 §10-③ 한계로 적어야 하고, 우리는 이미 그 방향의 대응(Stage-E area caps,
multi-contact 검토)을 갖고 있다는 사실로 *보완* 해야 한다 — *부인* 이 아니라.**

**③ ★★ 그러나 결정적 반전 — 이 가드레일은 300 MPa 에서 *원리적으로 만족 불가능* 하다.**
간단한 유효매질 산술 (**DERIVED-BY-US, 논문에 없음, order-of-magnitude 전용**).
가정: 단분산 동일구, Hertz `F = (4/3)E*√R* δ^{3/2}`, `E* = E/(2(1−ν²))`, `R* = R/2`,
평균장 `σ = φ Z F / (3π R²)`, φ = 0.64, **Z = 6**, ν = 0.30, σ = 300 MPa:

| E_SE | 예측 δ/d | 리뷰 기준(1 %) 대비 |
|---|---|---|
| **24 GPa (실물, 연화 없음)** | **≈ 7.6 %** (Z=8 이면 ≈ 6.3 %) | **6–8× 초과** |
| 1.35 GPa (우리 유효값) | 산술적으로 δ > R (**비물리**) — 실제로는 잼/배위수 증가가 먼저 걸려 우리 실측 **11–12 %** 에서 멈춘다 | 11–12× 초과 |
| **1 % 를 만족시키려면 필요한 E** | — | **E ≈ 500 GPa** (= 실물 LPSCl 의 **~21×**, 강철 200 GPa 의 **~2.5×**) |

⇒ **결론: 300 MPa 에서는 *실물 모듈러스를 그대로 써도* 이 가드레일을 못 지킨다.**
가드레일이 지목하는 것은 **우리 보정 선택이 아니라 "탄성 구 DEM 으로 배터리 압밀 압력을
누르는 것" 자체**다.  탈출구는 두 개뿐이고 **둘 다 우리가 이미 갖고 있거나 등록해 두었다**:
- **(i) 항복캡 접촉법칙** = `contact_models_layer_map.md` §2 **경로 A** (Thornton–Ning + H-cap;
  So 2021 이 LPS 로 0.98 실증) — 오버랩을 물리적으로 **닫는** 유일한 DEM 경로.
- **(ii) 진짜 형상 소성** = 우리 **MPM** (frame [5] 의 mechanics 절반).
⇒ **이것이 지도교수 질문에 대한 가장 강한 한 수다**: *"1 % 기준은 우리가 어긴 것이 아니라,
그 압력에서는 어느 탄성-구 DEM 도 못 지킨다.  그래서 우리는 DEM 옆에 소성 MPM 을 세웠고,
항복캡 경로를 백로그에 등록했다."*

**④ ⚠ 배수 정정 — 우리 사내 문서가 위반 크기를 *2× 과장* 하고 있다.**
`comparison_vs_ours_DEM.md` §F(W3) 와 `coetzee2017_dem_calibration_review.md` 는
Paulick 권고를 **"≤ 1 % of particle radius"** 로 적고 **"우리는 22–24× 밖"** 이라 쓴다.
**1차 자료는 두 곳 모두 "1 % of the particle *diameter*"** 다 (§4 p.75, §5 p.75).
⇒ **정확한 배수는 11–12× 이지 22–24× 가 아니다.**  (radius 로 말한 것은 Paulick 의 권고가
아니라 **Cleary & Hoyer 의 평균 0.6 %-of-radius**다.)  → §11 실행항목 ⑤ (문서 정정).
★ **불리한 쪽으로도 정직하게**: 11–12× 든 22–24× 든 **가드레일 밖이라는 사실은 변하지 않는다.**
정정의 목적은 방어가 아니라 **재인용 정확성**이다.

**⑤ 참고 — 이 문헌군의 가장 느슨한 수치와 비교하면.**
[25] Walton 1993 의 **1–10 %**(밑변 미명시)가 이 리뷰 전체의 상한이고, Coetzee 카드가 전하는
Höhner 의 **4 %** 가 그 다음이다.  우리 11–12 % 는 **가장 느슨한 수치조차 약간 넘는다.**
⇒ *"문헌 상한 안에 있다"* 는 방어는 **쓰면 안 된다.**

---

### ★ (c) **전단탄성률을 E·ν 에서 유도하는 우리 관행이 표준인가?**

> ## **판정: 표준이다 — 정확히는 *표준 이전에 산술적으로 강제* 다.  질문의 진짜 대상은 G 가 아니라 (E, ν) 쌍이다.**

- **근거 ①** Eq. (1) `E = 2G(1+ν)` 가 §1 p.67 에 **정의로** 실려 있다.  등방 선형탄성 자유도 = 2.
- **근거 ②** 리뷰가 **코드별 입력이 E / G / k_n 로 갈린다**고 명시하고(§1 p.67), Hertz–Mindlin
  커널을 **E* 형과 G 형 둘 다**로 적는다(Table 4).  즉 어느 쪽을 입력해도 같은 물리라는 전제가
  이 리뷰의 서술 자체에 깔려 있다.  **LIGGGHTS 에 E 를 주는 것은 그 코드의 규약 그대로다.**
- **근거 ③** Δt 조차 G 로 쓰여 있다(Eq. 2) — 즉 **E 를 입력해도 코드는 내부적으로 G 로 환산한다.**

**⇒ 지도교수 질문에 대한 정답 형태:**
*"G 는 입력 파라미터가 아니라 (E, ν)의 항등식 산물입니다 (Paulick 2015 Eq. 1).
우리가 출처를 대야 하는 것은 G 가 아니라 (E, ν) 쌍이고, 그 쌍은 **우리 DFT (B₀ 26.23 GPa,
E_VRH 22.06 GPa)** 에서 나옵니다.  그 쌍이 함축하는 값은 ν = 0.360, G = 8.11 GPa 이고,
우리 생산값 (1.53, 0.49) 는 **K 를 DFT B₀ 의 97.2 % 로 보존한 채 G 만 15.8× 연화**한 것입니다.
연화의 대상과 크기를 우리가 명시적으로 선언합니다."*

**⚠ 그러나 이 리뷰가 우리에게 붙이는 조건 2개:**
1. **"어느 모듈러스 · 어느 접촉모델"을 반드시 병기하라** — [34] Landry 가 같은 0.15–2.0 MPa 를
   E 로 넣을 때와 G 로 넣을 때 **응집력 응답이 4.3× vs 1.4× 로 갈린다**고 실증했다.
   ⇒ **SI 물성표에 bare "1.53 GPa" 금지.**  `E (MLS-MPM, von Mises J2)` 처럼 적을 것.
2. **ν 를 바꾸면 G 가 *추가로* 움직인다** — ν 0.360 → 0.49 는 분모 2(1+ν) 를 2.72 → 2.98 로
   키워 **전단을 1.096× 더 연화**시킨다.  ⇒ *"ν=0.49 는 bulk 를 세우기 위한 것"* 이라는 우리
   서술은 맞지만, **동시에 shear 를 더 무르게 만든다는 사실을 병기**해야 완전하다.
   (⚠ CLAUDE.md 가 이미 이 정정을 담고 있다 — "μ 0.5134 는 15.8배 연화" 절.)
3. **구를 쓰면 전단강성 레버가 약하다** ([35] Antony, K 0.25–1 에서 구형 무영향) ⇒ 우리 관행의
   **위험이 낮다**는 추가 근거.  ⚠ 스윕 폭 4× 뿐, 비구형에서는 유효 — over-claim 금지.

---

### ★ (d) **이 리뷰가 Coetzee 2017 에 더해 주는 것은?  (중복이면 중복이라고)**

> ## **판정: 중복 아님.  겹치는 것은 "얼마나 낮춰도 되나" 한 장뿐이고, 그 밖에 *우리에게 필요한 것 5가지* 를 이쪽만 갖고 있다.**

**겹치는 것 (≈ Coetzee §7 "Reduction in contact stiffness" 1개 장):**
Xu 70 MPa/70 GPa · Lommen · 오버랩 1 % 규칙 · 선형 강성↔벌크계수 · *"denser ⇒ more important"*.
(⇒ Coetzee 카드가 이 리뷰를 [235] 로 **재인용**하는 부분이 정확히 이 겹침이다.)

**Paulick 만 갖고 있는 것:**

| # | 항목 | 왜 우리에게 필요한가 |
|---|---|---|
| 1 | **regime 분류표 (Table 1)** + dense/dilute 판정 | 우리 자리(Dense×Static×Compression)를 **문헌 좌표계에 찍는** 유일한 도구 |
| 2 | **Eq. (1) + Eq. (2)** — E·G·ν·Δt 의 산술 | **(c) 판정의 전부.**  Coetzee 카드에는 이 대수(代數)가 없다 |
| 3 | **코드별 탄성 입력 지도 (Table 4·6)** — E* 형 / G 형 / k_n 형 커널 병기 | 우리 `contact_models_layer_map.md` 의 **DEM 입력층** 을 문헌으로 채움 |
| 4 | **COR ← √(k_load/k_unload) 교차상관 경고** (§4 p.75) | 우리 `hooke/hysteresis` 의 **k̂₂ ↔ COR 정합 감사** 를 촉발 (실행항목 ④) |
| 5 | **힘사슬·수직력 *분포* 가 안 전이된다는 명시 caveat** + Xu 최대힘 **9×** 정량 | (a) 판정의 **청구서 조항** — 우리 전달망에 직결.  Coetzee 카드에는 이 강도로 없음 |
| 6 | **Table 3 (오버랩↔파워드로)** · **Table 5 (k_n↔접촉시간·힘)** · **Table 2 (K=k_t/k_n)** 원자료 | Coetzee 카드가 담지 않은 **정량표 3장** |
| 7 | **[32] Thakur 접촉소성도 λ_p** = 리뷰 유일의 소성 LAW | 우리 이력 LAW 와 **같은 층**의 유일한 항목 |
| 8 | **미해결 지목: fine powders + upscaling** | 우리 문제가 **field-level 미해결**임을 저자 입으로 |

⇒ **두 카드는 짝으로 읽어야 한다**: **Coetzee = "보정을 어떻게 하는가(방법론·유일성·검증)"**,
**Paulick = "탄성 파라미터를 건드리면 무엇이 움직이는가(물리·민감도·regime)"**.
지도교수 질문 *"E·ν·σ_y·G 의 출처와 타당성"* 은 **Paulick 이 (E,ν,G) 를, Coetzee 가 (보정 절차를),
`fan2026_...` 와 우리 DFT 가 (σ_y 밴드를)** 각각 맡을 때 완결된다.
⚠ **σ_y (0.30 GPa) 는 이 리뷰의 소관이 전혀 아니다** — *탄성* 리뷰다.  σ_y 출처는
정본 `fan2026_sulfide_assb_stability_review_ECERD2600097.md` §3.5 (E 10–30 GPa · K_IC 0.2–0.4)
와 LPSCl 문헌 밴드 0.05–0.30 GPa 에서 가져와야 한다.

---

## 11. 적용 인사이트 — 실행 항목 (우선순위 순)

**① ★★★ F-C2′ 의 근거 문장을 교체하라 (즉시, 문서 작업).**
현행 F-C2′ 는 *"E 1.35 ≡ 1.5 = 동일 regime"* 을 **"σ 는 E 에 둔감"의 증거**로 쓴다.
그것은 **11 % 변화**이고, Paulick 의 선형법칙이 예측하는 응답도 11 % 이며, 우리 시드 산포
(±0.31 %p) 안이다 ⇒ **둔감의 증거가 아니다.**  리뷰어가 먼저 잡는다.
→ 대체 문장: *"E-민감도는 우리 코퍼스에서 **아직 측정되지 않았다** (11 % 스윕은 시드 잡음 이하)."*

**② ★★★ E-민감 검증시험 1건을 설계하라 — 구속 *벌크계수* (제하–재하).**
리뷰가 **4 그룹 독립 · 10×~10⁷× 폭 · 선형**으로 확립한, **가장 이득이 큰** E-관측량이다.
[21] 의 규약을 그대로: *"once a **stable hysteresis loop** was reached"* = **제하–재하 강성**.
- DEM: pure-SE 침대를 300 MPa 로 누른 뒤 **제하–재하 사이클** → 구속 벌크계수 M = dσ/dε.
- 이것은 **porosity@300 과 다른 시험**(F-C2 충족)이면서 **E 에 민감**(F-C2′ 충족)하다.
  → **우리가 아는 한 F-C2 와 F-C2′ 를 동시에 만족시키는 유일한 후보다.**
- 실험 앵커: LPSCl 분말 오이도미터 제하–재하 계수.  ⚠ **리포에 없음 → 문헌 탐색 필요** (n/a).

**③ ★★ E-민감도를 *데케이드 규모* 로 재라 (사전등록 대상).**
리뷰의 스윕은 10×~10⁷× 다.  우리 11 % 는 판별력이 없다.
→ `E_eff ∈ {0.45, 1.35, 4.0} GPa`(×3 간격, ~1 decade) × 동일 시드 × 300 MPa servo,
관측 = ε_sphere · ⟨δ⟩/d · **max δ/d** · Z · σ_ionic.  **선형 벌크계수 법칙이 우리 계에서도
성립하는가**가 1차 판정이고, `dlnσ/dlnE` 가 2차 판정이다.
⚠ 사전등록 없이 돌리면 사후해석이 된다 — `docs/reviews/*_prereg_*.md` 규약대로.

**④ ★★ 감사: `hooke/hysteresis` 의 k̂₂ ↔ COR 정합.**
Paulick §4 p.75: 선형 모델에서 `e = √(k_load/k_unload)`.  우리 덱이 COR 과 k̂₂ 를 **독립적으로**
설정한다면 둘이 서로 모순일 수 있다.  → 입력덱 1회 확인 (값은 지금 **n/a**).
★ 부수: **E 를 스케일할 때 k₁ 만 스케일되고 k₂/k₁ 비가 보존된다면 COR 은 불변**이다 — 그러면
우리 연화는 COR 을 오염시키지 않는다는 **방어 문장 1줄**을 얻는다.  확인 후 기록.

**⑤ ★★ 문서 정정 — 재인용 오류 (2× 과장).**
`comparison_vs_ours_DEM.md` §F(W3) · `coetzee2017_dem_calibration_review.md` 의
*"Paulick ≤1 % of particle **radius** ⇒ 우리는 22× 밖"* → **1차 자료는 "diameter" 이고 배수는 11–12×**.
(→ 이 카드 커밋에서 comparison 쪽에 정정 항목을 추가했다; Coetzee 카드 본문은 그 카드 소관이라
**손대지 않고 교차참조만** 남긴다.)

**⑥ ★ 최대 오버랩을 리포트 항목에 추가하라 (저비용).**
리뷰가 *"maximum overlap … or the average overlap"* 을 **둘 다** 쓰라고 하고,
Table 3 은 **평균 0.6 % 일 때 최대 15 %** 임을 보인다 = **25× 차**.  우리는 ⟨δ⟩ 만 낸다.
→ 덤프에서 `max δ/d` 와 상위 분위수(p99)를 함께 출력.  **힘 분포 caveat((a)-③)에 대한 최소 대응.**

**⑦ ★ 마찰 민감도(F-C1)의 우선순위를 올려라.**
§2.2 p.71: *"For the case of **spherical shapes, the friction coefficient becomes more important**."*
우리는 구를 쓰고 마찰을 한 번도 재지 않았다.  Bazzoun 2025(같은 코드·같은 소재계)의 8입력 OAT
설계를 베낄 수 있다 (F-C1 에 이미 적힘).

**⑧ ★ 보고 서식에 3열을 추가하라 (즉시, 무비용).**
리뷰 §2 p.67 의 요구 = **코드 · 접촉모델 · "탄성 파라미터의 정의"**.
→ 우리 SI 표에 `E (Young) / ν / 유도 G / 유도 K / 접촉모델 / 코드` 6열을 명시.
Table 4 형식이 그대로 템플릿이다.

**⑨ 백로그 연결 — 경로 A 의 근거가 하나 더 생겼다.**
(b) 판정 ③이 보인 대로, **300 MPa 에서는 실물 E 로도 오버랩 가드레일을 못 지킨다**.
⇒ `contact_models_layer_map.md` §2 **경로 A(real E + 항복캡)** 는 "18× 연화를 없애는 실험"일
뿐 아니라 **"접촉법칙 소변형 가정을 되찾는 유일한 DEM 경로"** 로 재정의된다.  그 문장을
백로그 항목 설명에 추가.

---

## 12. 인용 가능 문장 (deck / paper 용 — 영어 원문 + 쪽)

1. **(a)의 동기 = 속도** — *"the elasticity is often reduced to lower the running time of a simulation"* (Abstract, p.66)
2. **(a)의 위험 = 무자각** — *"in pure numerical studies the elasticity is often reduced, **neglecting any probable change of numerical response**"* (Abstract, p.66)
3. **E↔G 항등식** — *"Young's modulus E and shear modulus G are **linearly dependent by each other through Poisson's ratio ν**"* (§1, p.67)
4. **코드별 입력 분기** — *"either the contact stiffness [17], the Young's modulus [9] or shear modulus [8] is introduced"* (§1, p.67)
5. **Δt ↔ 강성** — *"the time step size is increased if the elasticity parameter decreases which results into a faster simulation time"* (§1, p.67)
6. **★ (b) 허가** — *"All authors found a **linear relationship** between the applied elastic parameter … and the bulk modulus which **enables the DEM user to scale down the stiffness parameter** for this specific application and for determining the bulk modulus."* (§2.2, p.71)
7. **★ (b) 청구서** — *"However, a scale down in stiffness leads to a **different compression behaviour** and, thus, **different force chains and distributions of normal force values may develop**."* (§2.2, p.71)
8. **구 조항 (우리에게 불리)** — *"For the case of **spherical shapes, the friction coefficient becomes more important**"* (§2.2, p.71)
9. **재배열 지배** — *"the key effect during shearing is **the particle rearrangement and not the elasticity** of the used materials"* (§2.2, p.70, [33] 요약)
10. **평균은 전이, 꼬리는 아님** — *"a minor reduced elastic parameter **does not influence the discharge rate but strongly affects the arising contact forces**"* (§2.3, p.71)
11. **과도 감소 경고** — *"a 9 % over-prediction of the specific power … is **too high to be acceptable** and … therefore **the elasticity parameter should not be as reduced as it is often done** in simulations"* (§2.4, p.72, [5] 요약)
12. **단일입자엔 실측값** — *"for single particle investigations the use of the **real particle and interparticle parameters is crucial**"* (§3.1, p.73)
13. **희박계 면제** — *"the chosen contact model and, therefore, a correct stiffness value might **not be very important** if the particles can be seen as continuum phase and solid–fluid interactions govern the system's behaviour"* (§3.2, p.74)
14. **교차상관 (COR)** — *"the coefficient of restitution in normal direction corresponds to **the square root of loading to unloading stiffness**"* (§4, p.75)
15. **★ 가드레일 (Discussion)** — *"a reduction of the elastic parameter did not show a major change in the numerical result **as long as the particle overlap remains smaller than 1 % of the particle diameter**"* (§4, p.75)
16. **★ 가드레일 (Conclusions, 목적 명시)** — *"the particle overlap … should not be larger than 1 % **for elastic deformation as foreseen by Hertz**"* (§5, p.75)
17. **★★ headline** — *"**The denser the system, the more important is the stiffness value.**"* (§5, p.75)
18. **★★ headline 2** — *"the denser the system, **the more carefully the elastic parameter must be chosen**"* (§5, p.75)
19. **미해결 지목** — *"**only little research on the influence of contact stiffness on bulk behaviour of powders** has been conducted … also the influence of contact stiffness during **particle upscaling** should be investigated"* (§4, p.75)
20. **코드 간 비교 불가성** — *"the same contact law might be implemented differently in another simulation code and thus, **different material properties are needed**"* (§5, p.75)

⚠ 6·7 은 **반드시 붙여서** 인용할 것.  7 없이 6 만 쓰면 체리피킹이고, 리뷰어가 원문에서 바로 찾는다.

---

## 13. 주의 / 한계 (over-claim 방지 — 이 카드를 쓰는 사람에게)

1. **소재 무관 리뷰다.**  LPSCl·NMC·배터리 언급 **0회**.  전이되는 것은 **방법론·regime·산술**뿐이고,
   **어떤 E 값도 우리 재료에 전이되지 않는다.**
2. **응력 영역이 3,000× 다르다** (≤96 kPa vs 300 MPa).  *"이 리뷰가 우리를 승인했다"* 는 문장은
   어떤 형태로도 쓸 수 없다.
3. **소성 접촉법칙을 사실상 다루지 않는다** ([32] 1편, 그마저 λ_p 스윕).  Coetzee 2017 과 같은 공백.
4. **(b) 사례 0편.**  이 카드에서 (b) 를 방어할 때 쓸 수 있는 것은 **원리적 허가 문장(인용 6)** 하나이지
   **선례가 아니다.**
5. **1 % 는 예리한 문턱이 아니다** — 같은 리뷰 안에서 밑변(반지름/지름)·통계량(평균/최대)이 갈리고
   허용치가 0.5 %~10 % 로 **20× 산포**한다 (§9-#3, #8).  *"기준을 몇 배 어겼다"* 는 표현은
   **밑변을 반드시 병기**해야 의미가 있다.
6. **그림을 디지타이즈하지 않았다** (렌더 불가).  Fig 1–6 의 축값·데이터점은 이 카드에 **없다**.
   필요하면 원 PDF 를 열어 별도 작업할 것.  이 카드의 모든 수치는 **stated**.
7. **본문 vs 표 불일치 8건**을 §9 에 기록했다.  이 리뷰를 **재인용할 때 원 표기 확인 필수**.
8. **§10-(b)-③ 의 δ/d 추정은 우리 봉투계산**이다 — 단분산·Hertz·Z 고정·평균장 가정.
   실제 침대는 다분산·AM 차폐·잼이 있어 **order-of-magnitude 로만** 쓸 것.
   *"실물 E 로도 못 지킨다"* 는 **방향**은 견고하고, **숫자 7.6 %/500 GPa 는 지표값**이다.
9. **Kwade 계보 주의** — 이 리뷰([29] 포함)와 `giannis2021_...` 는 같은 그룹이다.
   두 카드를 **독립 증거로 나란히 세우면** 상관을 무시하는 것이다.  같은 그룹임을 병기할 것.
10. **σ_y·K_IC 는 이 카드의 소관이 아니다** (탄성 리뷰).  거기 인용을 붙이지 말 것.

---

## 14. 기법 미니 용어집 (이 카드 안에서 쓰인 용어)

| 용어 | 뜻 (이 카드에서의 정의) |
|---|---|
| **탄성 파라미터** | DEM 접촉의 탄성부를 정하는 입력 — 코드에 따라 **E**(LIGGGHTS) · **G**(EDEM) · **k_n**(Luding/PFC 선형) 중 하나 |
| **접촉강성 k_n** | 오버랩 δ_n 과 수직력 F_n 을 잇는 계수 (`k_n = F_n/δ_n`, 선형모델).  Hertz 계열에서는 `k_n = (4/3)E*√R*` 처럼 δ 의존 |
| **등가 영률 E\*** | `E* = [(1−ν₁²)/E₁ + (1−ν₂²)/E₂]⁻¹` (Hertz).  동일재료 두 구면 `E/(2(1−ν²))` |
| **등가 반지름 R\*** | `R* = (1/R₁ + 1/R₂)⁻¹`.  동일구 두 개면 R/2 |
| **오버랩 δ_n** | 두 입자의 수직방향 **총** 겹침 = R₁+R₂−r.  **밑변(반지름 vs 지름)을 반드시 병기해야 하는 양** |
| **Rayleigh Δt** | Rayleigh 표면파가 입자를 가로지르는 시간의 일정 비율(여기선 20 %)로 잡는 안정 시간간격.  `Δt ∝ G^(−1/2)` |
| **구속 벌크계수 (confined bulk modulus)** | 오이도미터(측방 구속) 압축에서 dσ/dε.  [21] 은 **안정 이력루프 도달 후**의 사이클로 정의 |
| **Resilient modulus** | 최대 편차응력 / 탄성변형 — 도로기층 시험의 강성 지표 [24] |
| **접촉소성도 λ_p** | `1 − k_load/k_unload`.  0 = 완전탄성, 1 = 완전소성 [32] |
| **벌크소성도** | 소성 벌크변형 / 총 벌크변형 [32] |
| **강성비 K** | 접선/수직 접촉강성 비 `k_t/k_n` [35] |
| **Sliding fraction** | 주어진 변형률에서 미끄럼 접촉수 / 총 접촉수 (Table 2 각주) |
| **Sliding energy ratio** | 접촉 미끄럼으로 소산된 에너지(단위 원부피당) / 그 변형률까지의 총 일 (Table 2 각주) |
| **Dense system (이 리뷰 정의)** | *"공정시간의 거의 전부 동안 입자들이 서로 접촉해 있는"* 패킹 — **밀도 수치 기준이 아님** |
| **BPM (bonded particle model)** | 입자들을 bond 로 묶어 1차 입자/응집체의 파괴를 모사 [60] |
| **bond stiffness [N m⁻³]** | bond 반경 배수 λ 로 정해지는 단면적에 걸쳐 작용하므로 부피강성 차원으로 표기 (Table 4 각주) |
| **(a) 속도용 감소 / (b) 벌크-맞춤 보정** | 이 카드의 라벨.  ⚠ Coetzee 카드는 **번호가 반대** — 인용 시 라벨 명시 |

---

## 15. 이 카드와 함께 볼 정본 카드

| 카드 | 관계 |
|---|---|
| `coetzee2017_dem_calibration_review` | **짝 카드.**  이쪽 = 보정 *방법론*(두 학파·유일성·검증), 저쪽 = 탄성 파라미터의 *물리·민감도*.  ⚠ 저 카드가 이 논문을 [235] 로 재인용하며 **"1 % of radius"** 로 적었다 — 1차 자료는 **diameter** (§9·§11-⑤).  또 저 카드는 **다른 Paulick 논문 [219]**(시험기 강성을 배제한 접촉강성 측정법)도 인용한다 — **미digest, WISHLIST 후보** |
| `giannis2021_stress_based_multicontact_dem` | **같은 그룹(Kwade/TU Braunschweig) 계보.**  우리 δ/d 11–12 % 에서 접촉 독립성이 깨진다는 (b)-② 판정이 가리키는 **multi-contact 보정** 의 정본.  ⚠ 내용은 그 카드 소관 — 여기서 추측 금지 |
| `bazzoun2025_dem_parameter_sensitivity_assb_cathode` | **우리 소재계·같은 LIGGGHTS 의 8입력 OAT** — §11-⑦ 마찰 민감도 설계를 그대로 베낄 대상 |
| `bazzoun2026_dem_fem_rnm_ionic` | E_SE = 22.1 GPa · ν 0.37 실측 사용례 = 우리 "실물 E" 앵커의 문헌 짝 |
| `varkey2026_multicontact_dem` / `docs/lit_varkey2026_multicontact_dem.md` | 강체구 DEM 의 ~20 % porosity floor + Thornton–Ning 항복캡 = (b)-③ 의 **탈출구 (i)** |
| `fan2026_sulfide_assb_stability_review_ECERD2600097` | **σ_y·K_IC 의 소관** (이 카드는 탄성만) — E 10–30 GPa 밴드도 여기 |
| `contact_models_layer_map.md` (litdb 루트, 동결본은 주 리포) | §2 **경로 A**(real E + 항복캡) = (b)-③ 의 탈출구 (i) 구현 스펙 |
| `our_dem_baseline.md` (주 리포) | §10 대비표의 기준값 |

---

## 🗨️ Q&A 로그

*(빈 칸 — 후속 질문·답변을 여기에 누적)*
