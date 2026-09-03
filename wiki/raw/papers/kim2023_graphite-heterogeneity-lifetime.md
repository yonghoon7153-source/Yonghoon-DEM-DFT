---
title: "Kim et al. 2023 — 흑연 음극 불균일성으로 수명 예측 (ACS Energy Lett. 8)"
source_url: local-upload/ACS_Energy_Lett_2023_Kim_Lifetime_Prediction_by_Heterogeneity_of_Graphite_Anodes.pdf (+ Supporting Information)
ingested: 2026-09-03
sha256: dff0405a16a9b364273e3492bbe18ffd3523b62194b3f9b2ca02fccf92760ff2
---

# 수집 목적

Minsoo Kim, Inwoo Kim (공동 1저자), Jisub Kim, Jang Wook Choi\*,
**"Lifetime Prediction of Lithium Ion Batteries by Using the Heterogeneity of
Graphite Anodes"**, *ACS Energy Letters* **2023**, 8, 2946−2953,
DOI **10.1021/acsenergylett.3c00695** — **본문(8쪽) + Supporting
Information(24쪽)** 의 절별 해체분석.

흡수 동기는 **하나의 판정**이다. 직전에 흡수한 분야 리뷰
([[interpretable-ml-battery-prognosis-taxonomy]], Wang et al. 2025) 가 이
논문을 §4.2 IC/DV feature 계열의 대표 사례로 싣고, 그 feature 를
"**DV peak intensity**", 물리 귀속을 "**흑연 음극으로의 리튬 삽입
불균일성**"(= 음극 단일)이라고 요약한다. 우리 위키는 리뷰 Fig. 5c 를 직접
보고 그 "intensity" 가 실제로는 **peak−valley 진폭**이라고 적어 두었다.

그런데 2026-09-02 BML 세미나
(`raw/papers/2026-09-02-siwon-kim-degradation-mode-ml-seminar.md` p.7) 는 같은
형태의 기하량(PVS = ICA 의 peak2−valley2 를 전압 간격으로 나눈 것)을
**"peak2 = 양극(NCM811) 상전이 vs valley2 = 음극(graphite) 단일상" 의 대비**로
읽는다. 두 해석은 같은 도형에 서로 다른 전극을 붙인다.

이 digest 의 임무는 **원전에서 직접** 다음 셋을 확정하는 것이다:

1. descriptor 의 정확한 정의 — 절대 peak 높이인가, peak−valley 진폭인가.
2. 물리 귀속의 **근거** — half-cell? 해체? 시뮬레이션? 상관관계뿐? 양극은
   검토했는가.
3. 그래서 이것이 세미나 PVS 해석과 **충돌**인가, 아니면 **다른 대상**인가.

결론을 먼저 적는다 (근거는 §9):

- **descriptor 는 두 개다.** `ΔPeak_S2` = ridge − valley (진폭) 이고,
  `Peak_S2 intensity` = **ridge 의 절대값**이다. **논문의 모든 대표 결과
  (ρ = 0.82, MAPE 13.5 %, 모듈 등급화) 는 절대값 쪽을 쓴다.** 진폭 쪽은
  valley 노이즈 때문에 **의도적으로 버려졌다** (ρ = 0.75).
  → 리뷰의 단어("peak intensity")는 **맞고**, 우리 위키가 리뷰 Fig. 5c 에서
  추론한 "intensity = peak−valley 진폭" 은 **틀렸다**. Fig. 5c 가 재수록한
  화살표는 이 논문이 **버린** 변형(ΔPeak_S2)이다.
- **셀은 LFP‖Gr 원통형(IFR18500, 1 Ah)** 이다. 세미나의 NCM811‖Si-graphite
  (MJ1) 와 **화학이 다르다**. LFP 는 2상 평탄 OCP 라 dV/dQ 에 사실상 기여하지
  않는다 → 이 논문에서 음극 단일 귀속은 **화학에 의해 강제**된 것이지, 일반
  법칙으로 주장된 것이 아니다.
- 물리 귀속의 근거는 **half-cell 도 시뮬레이션도 아니다.** 기구론적 도식
  (Fig. 1a–c) + 선행문헌(ref 14/18/19) + **n = 2 셀의 XRM 구조 상관** +
  운전조건 경향 + 해체 SEM/ToF-SIMS 다. **양극은 한 번도 검토되거나 명시적으로
  배제되지 않는다.**

**표기 규칙** (이 위키 관례 3구분):

- `[인쇄]` — 원문(본문/SI/캡션/표)에 문자로 인쇄된 것.
- `[도표]` — 잘라낸 그림을 **실제로 보고** 눈으로 읽은 것. 수치는 근사이며
  원문 도표가 정본이다.
- `[해석]` — 내(에이전트) 판단. 원문 주장이 아니다.

---

## 0. 서지 — PDF 에서 직접 재확인

`[인쇄]` (본문 p.1 헤더 / 각 페이지 footer / ASSOCIATED CONTENT)

| 항목 | 값 |
|---|---|
| 제목 | Lifetime Prediction of Lithium Ion Batteries by Using the Heterogeneity of Graphite Anodes |
| 저자 | Minsoo Kim^⊥, Inwoo Kim^⊥, Jisub Kim, Jang Wook Choi\* |
| 각주 | `⊥M.K. and I.K. contributed equally to this work.` |
| 소속 | Seoul National University — School of Chemical and Biological Engineering + Institute of Chemical Processes (전원); Choi 는 Dept. of Materials Science and Engineering 겸직 |
| 교신 | jangwookchoi@snu.ac.kr · ORCID 0000-0001-8783-0901 |
| 저널 | *ACS Energy Lett.* **2023**, 8, 2946−2953 (Letter) |
| **DOI** | **10.1021/acsenergylett.3c00695** |
| SI DOI 링크 | `https://pubs.acs.org/doi/10.1021/acsenergylett.3c00695` |
| 접수/게재 | Received April 3, 2023 · Accepted June 5, 2023 · Published June 9, 2023 |
| 자금 | MOTIE Technology Innovation Program (20011379) · NRF-2021R1A2B5B03001956 · **Hyundai Motor Company** |
| SI 구성 | Tables S1–S2, Figures S1–S16 |

`[해석]` 사용자가 1쪽에서 확인한 서지와 **완전히 일치**한다. 페이지 footer 의
문자열(`nz3c00695`)이 DOI 말미와 같아 교차확인된다.

`[해석]` **자금 출처에 Hyundai Motor Company 가 있다.** 논문의 결론
("as-manufactured 셀 등급화 → 모듈 조립")은 완성차 업체의 입고검사 관심사와
정확히 겹친다. 이해상충은 "The authors declare no competing financial
interest." 로 부인되어 있다.

---

## 원문에 없어서 확인이 필요한 것 (공백 목록)

이 절을 머리에 둔다. 아래 본문은 이 공백들을 전제로 읽어야 한다.

1. **half-cell / 3-전극 데이터가 전무하다.** `half-cell`·`half cell` 은 본문과
   SI 를 통틀어 **0회**. dV/dQ 의 ridge/valley 를 흑연 staging 에 귀속시키는
   **직접 측정**이 이 논문 안에 없다 (선행문헌 인용으로 대체).
2. **양극(LFP)의 기여를 정량한 곳이 없다.** "LFP 의 dV/dQ 기여는 무시할 수
   있다" 는 문장조차 없다 — 그냥 **논의되지 않는다**.
3. **열화 모드 분해가 전무하다.** `LLI`·`LAM` 은 약어로 0회이고,
   "loss of lithium inventory and loss of active material" 이 서론에서 DVA 의
   일반적 효용을 소개할 때 **딱 한 번** 나온다. 이 논문은 모드를 재지 않는다.
4. **descriptor 계산의 수치적 세부가 없다.** dV/dQ 를 어떤 미분·평활화·
   샘플링으로 얻었는지 (window, 다항 차수, ΔQ 간격) 본문·SI 어디에도 없다.
   `Peak_S2` 는 "ridge 의 절대값" 이라고만 정의된다 → **평활화 의존성이
   그대로 열려 있다** (그리고 저자들이 valley 노이즈 때문에 Δ 를 버렸다는
   사실이 이 민감도가 실재함을 보여 준다).
5. **DVA 측정의 C-rate 가 명시되지 않았다.** SI 는 RPT 를 "0.2C 3사이클로
   용량 평가 후 DVA 와 DCIR 측정" 이라 적고, descriptor 는 "첫 RPT 의 **세 번째
   사이클**" 데이터를 쓴다고 한다 → 0.2C 로 읽히지만 DVA 전용 rate 를 따로
   적지 않았다.
6. **불확실성 어휘 0회.** `uncertainty`·`confidence`·`identifiab`·`uniqu`·
   `degenerat`·`ill-posed`·`collinear` 전부 0회 (§8 전수 확인).
7. **n = 2 의 구조 상관.** XRM(Fig. 2c–f, S10, S11) 은 균질/비균질 셀 **각
   1개**씩이다. roundness 0.21 vs 0.64 mm 는 **표본 2개의 값**이며 분포가 없다.
8. **해체 분석의 대상이 descriptor 실험군과 다르다.** SEM/ToF-SIMS/DMC 색
   (Fig. S5–S9) 은 **1C@25 °C vs 2C@25 °C 로 사이클한 셀**을 비교한다.
   Fig. 2 의 "균질/비균질 셀"(같은 조건 1C@25 에서 첫 사이클 descriptor 로 고른
   두 셀)을 해체한 결과가 아니다.
9. **cycle life 라벨 자체가 회귀 보간값이다.** `[인쇄, SI]` "The cycle life was
   referred to as the cycle number to reach the SOH80, which was **estimated by
   polynomial regression** using for the capacity measured every 100 cycles."
   → 정답 축에 보간 오차가 실려 있으나 그 크기가 보고되지 않는다.
10. **Fig. 2b 의 수평 점선(0.80 Ah)과 본문의 373/193 cycles 가 맞지 않는다**
    (§4 참조). SOH80 의 기준 용량이 공칭 1 Ah 인지 Q_BOL(≈0.93 Ah)인지가
    도표에서 재구성되지 않는다.
11. **`Peak_S4` 와 `ΔPeak_S4` 의 표기가 원문 안에서 서로 어긋난다** (§7.3).

---

## 1. Abstract + 서론 (p.2946)

### 1.1 Abstract

`[인쇄]` 전문 요지:

> "Here, we introduce the **lithiation heterogeneity** as a key descriptor for
> inspecting and grading as-manufactured cylindrical cells. Specifically, the
> **peak intensity of the differential voltage (DV) profile during charge**
> provides a quantitative indication of the heterogeneity of lithium ion
> intercalation into graphite, **in relation to the staging effect of the
> graphite anode**."

`[해석]` 초록의 이 한 문장이 리뷰(Wang 2025)의 요약이 온 자리다. 단어는
"peak intensity" 이고 귀속은 "intercalation into graphite" — 리뷰의 요약은
**초록에 충실**하다.

### 1.2 문제 설정

`[인쇄]` 현행 셀 메이커의 입고검사: 용량, DCIR, OCV drop 등 →
"provide **superficial** information regarding the SOH". 비파괴 대안(음향
분광, X-ray CT, fiber Bragg grating)은 파괴적이거나 장비가 더 든다. 그래서
포메이션 사이클에서의 전기화학적 방법으로 "go or no go" 를 결정한다.

`[인쇄]` DVA 를 고른 이유:

> "although the differential voltage (DV) can be simply calculated from the
> normal potential vs the capacity profile, it offers useful information
> related to the state of the electrode such as the **loss of lithium inventory
> and loss of active material**."

`[해석]` **본문에서 LLI/LAM 이 언급되는 유일한 문장이다.** 그리고 이 논문은
그 뒤로 LLI/LAM 을 한 번도 재지 않는다 — DVA 의 관례적 효용을 소개하는
수사일 뿐이다.

### 1.3 선행연구 — 물리 귀속의 계보 (★ 중요)

`[인쇄]` 세 편이 "DV peak 형상 ↔ 흑연 리튬화 균질성" 을 이 논문에 물려준다:

| ref | 내용 (인쇄된 요약) |
|---|---|
| **14** Lewerenz, Marongiu, Warnecke, **Sauer**, *J. Power Sources* 2017, 368, 57 (LiFePO₄\|Graphite **원통형**) | "DVA can inform the **homogeneity of a graphite (Gr) anode** in a LiFePO₄(LFP)/Gr cell, in such a way that **the sharpness of the peak on the DV profile reflects the homogeneity of lithium (Li) ion intercalation behavior in the Gr anode**" |
| **18** Senyshyn et al., *Sci. Rep.* 2016 (중성자 회절) | "the **inhomogeneous distribution of Li in the Gr anodes** in 18650-type cylindrical cells resulted from the geometrical dimensions of the cylinder in use" |
| **19** Sieg, …, **Sauer**, *J. Energy Storage* 2020 (NMC/Gr **파우치**) | "Sauer's group also **experimentally verified** that the spatially inhomogeneous degradation of the Gr anode in a Li[Ni_xMn_yCo_z]O₂/Gr pouch cell could be **reflected in its DV profiles**" |

`[인쇄]` 그리고 이 논문이 주장하는 novelty:

> "However, to the best of our knowledge, **the cell-to-cell variation at the
> postmanufacturing stage and the resulting differences in the lifetime have
> not yet been quantitatively evaluated** using any chemical descriptor
> including the reaction homogeneity."

`[해석]` **물리 귀속(peak 형상 ↔ 흑연 리튬화 균질성)은 이 논문이 세운 것이
아니라 ref 14 에서 물려받은 것이다.** 이 논문의 novelty 주장은 귀속이 아니라
"**셀 간 변동과 수명의 정량적 연결**" 이다. 판정에 중요하다 — 귀속의 근거를
찾으려면 최종적으로 Lewerenz 2017 (ref 14, 역시 **LFP\|Gr 원통형**) 로
가야 한다.

### 1.4 경쟁 방법에 대한 위치 설정

`[인쇄]`

- **Stefanopoulou 그룹(ref 25, Weng et al., *Joule* 2021)**: 저 SOC 저항 →
  SEI 상태 → 수명. 비판: "not usually applicable to cells that undergo the same
  or similar formation cycles but **cycle under different conditions**."
- **Chueh & Braatz(ref 24, Severson et al., *Nat. Energy* 2019)**: 10–100
  사이클 전압 프로파일 변화. 비판: "relies on the electrochemical data from a
  certain number of **initial cycles** and is therefore **not applicable to
  cells at an early stage of cycling**."
- 이 논문: "**valid throughout the entire duration of cycling, even including
  the formation cycle**, without the need to implement additional analytical or
  mathematical processing."

`[인쇄]` 헤드라인 통계: "Pearson correlation coefficient (ρ) of **0.82**"
between descriptor and cycle life for **77 LFP/Gr cells**.

---

## 2. §"Heterogeneity of Gr Anodes" (p.2947–2948) — 기구론과 descriptor 정의

### 2.1 불균일성의 기원 (인쇄된 인과 사슬)

`[인쇄]` 사슬:

1. 이상적 균질 반응에서 Li 는 **고정된 에너지 준위(= 고정된 전위)** 로
   흑연에 삽입된다.
2. 계면·결정격자의 **국소적으로 불규칙한 환경**이 그 삽입 에너지 준위를
   **분산**시킨다.
3. 그 불규칙성의 제조 기원: "**aggregation of binder during the electrode
   drying process**" 와 "**irregular morphology during the electrode coating
   process**" — 국소 전기장·압력을 교란한다 (ref 26, 27).
4. 결과: 비균일 Li flux·저장 → 불규칙한 계면 열화 → 용량 감소 가속 (ref 28).

### 2.2 Fig. 1 — descriptor 의 정의 그림 (**직접 봄**)

`[도표]` `fig_1.png` 4패널.

- **(a) Homogeneous cell / (b) Heterogeneous cell**: 좌측에 젤리롤 단면(나선)
  도식, 우측 회색 영역이 `Gr anode`. 전극의 **두 지점**을 확대해 흑연 층간에
  Li(초록 구)가 들어간 그림을 그린다. (a) 는 두 지점의 Li 점유가 **같고**,
  (b) 는 한 지점이 성기고 다른 지점이 조밀하다. 각 지점에서 나오는 초록 점선
  종 모양(=국소 DV peak 을 암시)이 (a) 에서는 **동일**, (b) 에서는 **높이와
  위치가 다르게** 그려진다. 하단에 각각 `Voltage` vs `Capacity` 곡선 —
  (a) 는 두 국소 곡선이 겹쳐 하나의 **급한 계단**, (b) 는 두 곡선이 **어긋나
  겹쳐** 완만한 계단.
- **(c)**: 축 눈금 없는 개념도. `Homogeneous Gr cell`(남색)은 **가파른** S자,
  `Heterogeneous Gr cell`(빨강)은 **완만한** S자. 전이 구간에 회색 양방향
  가로 화살표(= 전이가 용량축으로 넓어짐).
- **(d)** ★ 정의 그림. 상단: `Voltage (V)` 3.2–3.5 vs `Capacity (Ah)`
  0.0–1.0 (상단 축). 세로 점선으로 **`Stage IL`(≈0.05) · `Stage IV`(≈0.15) ·
  `Stage III`(≈0.22) · `Stage II`(≈0.58)** 표시. 하단: `dV dQ⁻¹ (V Ah⁻¹)`
  0.0–1.0 vs `Capacity (Ah)` 0.0–1.0.
  - `[도표]` DV 곡선 형상 (눈으로 읽은 근사): 0.06 에서 >1.0 → **국소최소
    ≈0.30 @ 0.085** → **ridge ≈0.55 @ 0.15** → 어깨 ≈0.44 @ 0.20 →
    **valley ≈0.05 @ 0.33–0.45** → **ridge ≈0.28 @ 0.59** → ≈0.10 @ 0.70 →
    0.93 에서 급상승.
  - **초록 양방향 세로 화살표 + `ΔPeak_S2` 라벨**: 화살표는 x ≈ 0.33 위치에
    그려지고, 위 끝은 0.59 의 ridge 높이(≈0.28)에서 왼쪽으로 뻗은 초록
    점쇄선, 아래 끝은 valley 높이(≈0.05)의 초록 실선에 닿는다.
    → **ΔPeak_S2 = (ridge @≈0.6 Ah) − (valley @≈0.4 Ah) ≈ 0.23 V Ah⁻¹.**

`[인쇄]` 본문의 정의 문장 (본문 p.2948):

> "Based on the rationale that the slope of the voltage profile near a stage
> transition reflects the spatial heterogeneity of lithiation, **the gap
> between the valley and the peak in stage II on the dV dQ⁻¹ profile, denoted
> ΔPeak_S2 (green arrow), was established as a descriptor** to represent the
> heterogeneity of lithiation in the Gr anode.^14,19,29"

`[해석]` **주목**: 본문에서 처음 정의되는 descriptor 는 **ΔPeak_S2 (진폭)**
이고, 절대 peak 높이(`Peak_S2 intensity`)는 여기서 정의되지 않는다. 절대값은
p.2949(§5)에서 **교체용으로 갑자기 도입**된다. 정의의 정본은 SI (§7.1) 다.

`[해석]` **Fig. 1d 의 stage 라벨은 full-cell 전압곡선 위에 직접 붙어 있다.**
LFP 양극의 OCP 기여를 분리해 보인 패널은 없다. 즉 "이 ridge 는 흑연 stage II
전이다" 는 **저자의 지정**이며, 그 지정의 근거는 §1.3 의 선행문헌이다.
`[해석]` 다만 LFP 는 2상 반응이라 OCP 가 3.42 V 부근에서 거의 평탄하고
dV/dQ ≈ 0 이므로, **LFP‖Gr 셀에서 full-cell dV/dQ 의 구조가 사실상 흑연의
것이라는 지정은 물리적으로 안전하다.** (이 논거는 원문에 인쇄돼 있지 않다 —
내 판단이다.)

---

## 3. 4가지 사이클 조건 실험과 해체 검증 (p.2948, Fig. S1–S9)

### 3.1 조건과 분류

`[인쇄]` 4조건 (SOH 80 % 까지): **1C@25 °C, 2C@25 °C, 1C@45 °C, 1C@10 °C**.
`[인쇄, SI]` "only the **charging** rate and temperature were varied while the
discharging rate was fixed at 1C."

`[인쇄]` SOH 정의:

> SOH(n) = Q(n) / Q_BOL × 100 — "the SOH in this study was **solely used to
> represent the capacity retention**"

`[인쇄]` 분류 결과:

- **"homogeneous" degradation**: 1C@45 °C, 1C@25 °C
- **"heterogeneous" degradation**: 1C@10 °C, 2C@25 °C
- 해석: "a **low temperature and high C-rate** tend to more significantly
  induce heterogeneity of the Gr electrode and **increase the chance of Li
  plating**."

### 3.2 Fig. S2a — ★ 우리 축에 가장 중요한 SI 도표 (**직접 봄**)

`[도표]` `fig_S2.png` (a): y = `ΔPeak_S2 (V Ah⁻¹)` 0.04–0.24+, x = `SOH (%)`
100 → 80 (**왼쪽이 100, 오른쪽이 80** — 축이 뒤집혀 있다). 4개 조건 곡선:

| 조건 | SOH 100 % | SOH ≈80 % | 방향 |
|---|---|---|---|
| **1C@45 °C** (빨강) | ≈0.225 | **≈0.253** | **증가** |
| **1C@25 °C** (검정) | ≈0.21 | ≈0.20 | 거의 평탄 |
| **1C@10 °C** (파랑) | ≈0.20 | **≈0.11** | 감소 |
| **2C@25 °C** (주황) | ≈0.225 | **≈0.083** | **가장 큰 감소** |

우측에 `Homogeneous degradation ↑` / `Heterogeneous degradation ↓` 화살표
라벨.

`[해석]` **★ 이 도표가 이 논문에서 우리 프로젝트에 가장 값어치 있는 것이다.**
**같은 SOH 80 % 에서 ΔPeak_S2 가 0.083 ~ 0.253 으로 3배 차이 난다.** 즉
DV 극값의 진폭은 **용량 손실량의 함수가 아니다** — 손실이 **어떻게 분포하는가**
(그리고/또는 어떤 모드 조합으로 일어났는가)에 강하게 의존한다.

`[인쇄]` 저자들도 이 함의를 명시한다:

> "the series of results in Figure S2a convey an important message that **even
> at the same SOH (the same capacity retained), the heterogeneity of the
> electrode could differ such that the degradation trend in subsequent cycles
> could be different**."

`[해석]` **경고 — 이 도표는 두 가지로 읽힌다.** 저자는 "공간적 불균일성이
달라서" 라고 읽는다. 그러나 2C@25 와 1C@10 은 **Li plating** 을 유발하고
(저자 자신이 그렇게 적는다), plating 은 LLI 와 국소 LAM_NE 를 만든다.
1C@45 는 SEI 성장(LLI 위주)을 유발한다. **즉 네 곡선은 "불균일성의 정도" 가
다른 것일 수도 있고 "열화 모드 조합" 이 다른 것일 수도 있다. 이 논문은 모드를
재지 않으므로 둘을 구분할 수 없다.** 이것이 이 논문의 가장 큰 방법론적 공백이다.

`[도표]` (b) `ΔPeak_S4` 도 같은 정성적 갈림: 45 °C(빨강) 0.29→0.29 유지,
1C@25(검정) 0.27→0.26, 2C@25(주황) 0.27→**0.123**, 1C@10(파랑) 0.275→0.173.
`[인쇄]` 본문: "ΔPeak_S4 … **also varied consistently** among the cells that
underwent homogeneous and heterogeneous degradation (Figure S3)."

### 3.3 Fig. S1 — DV 곡선의 실제 진화 (**직접 봄**)

`[도표]` `fig_S1.png` 4패널, 각각 `dV dQ⁻¹` 0–1.0 vs `Capacity (Ah)` 0–1.0,
범례 = SOH(%).

- (a) **1C@25 °C** (SOH 100.0 → 81.0): 0.6 Ah 의 ridge 가 **높이를 대체로
  유지하면서 좌로 이동** (0.60 → ≈0.50), 오른쪽 급상승 구간이 0.93 → 0.72 로
  당겨진다. valley 는 ≈0.05 유지.
- (b) **2C@25 °C** (100.0 → 81.6): ridge 가 **뭉개진다** — SOH 81.6 에서
  0.6 Ah 근방의 봉우리가 거의 **어깨 수준(≈0.17)** 으로 낮아지고 valley 는
  ≈0.12 로 **올라온다**. 즉 진폭이 양쪽에서 압축된다.
- (c) **1C@45 °C** (100.0 → 80.7; 범례에 **101.4, 100.2** 가 있다 = 초기
  용량 상승): ridge 가 오히려 **날카로워지며** 좌로 이동 (≈0.28 유지).
- (d) **1C@10 °C** (100.0 → 79.2): (b) 와 같은 뭉개짐, SOH 79.2 에서 봉우리가
  ≈0.19 로 낮고 넓다.

`[해석]` **(b)·(d) 에서 valley 가 올라오고 peak 이 내려온다** — 진폭
(ΔPeak_S2)은 두 방향에서 함께 줄고, **절대 peak 값**만 보면 그 절반만 본다.
저자들이 §5 에서 절대값으로 갈아탄 것은 **노이즈 때문**이지 물리 때문이 아니다
(그리고 그 대가로 ρ 는 0.75 → 0.82 로 **올랐다** — §9.4).

### 3.4 방전 프로파일은 왜 안 쓰는가

`[인쇄]`

> "the discharge profiles are **not as suitable as their charge counterparts**
> in diagnosing the state of a cell because **the amount of Li ions
> intercalated in the Gr could affect the ΔPeak_S2 intensity**.^31"

`[해석]` 즉 방전 시작 시점의 흑연 리튬화 정도(= 직전 충전 이력)가 descriptor
를 오염시킨다는 뜻이다. **descriptor 가 이력 의존적**이라는 자백이며, 충전
쪽에서도 컷오프·rate 가 바뀌면 같은 문제가 생길 수 있다 (원문은 그 확장을
논하지 않는다). 안 봄: `fig_S4.png`.

### 3.5 해체 분석 (Fig. S5–S9) — 안 봄, 본문 서술만

`[인쇄]` 요지:

- **S5 (fresh)**: "clean, Li-free surface and intact Gr particles".
- **S6 (1C@25, SOH80)**: "overall clean surface, but **intensive Li plating was
  observed near spot 4**".
- **S7 (2C@25, SOH80)**: "**more extensive surface damage across the entire
  electrode**"; 고배율에서 "surface to be covered with **reaction
  byproducts**".
- **S8 (ToF-SIMS)**: 2C@25 쪽에서 `LiF₂⁻²`(원문 표기 그대로; LiPF₆ 분해물)와
  `C₂HO⁻`(용매 분해물)가 더 많이 검출.
- **S9 (DMC 세척액 색)**: fresh·1C@25 는 투명, **2C@25 는 노랗게** 변함 →
  "more unstable SEI formation, which is rooted in its more heterogeneous
  (dis)charging reaction."

`[인쇄]` 젤리롤 기하에 대한 설명: "the **outside of the anode** is known to be
more vulnerable to Li plating. This is because **the area of the facing cathode
is larger than that of the anode owing to the curvature of the jellyroll**,
providing a higher likelihood for Li ions to be locally concentrated.^32"

`[해석]` **이 해체 증거들은 조건 비교(1C vs 2C)에 붙어 있지, descriptor
값에는 붙어 있지 않다.** "낮은 Peak_S2 를 가진 셀을 해체했더니 흑연 리튬화가
공간적으로 불균일하더라" 는 실험은 이 논문에 **없다**. 있는 것은 "가혹 조건에서
사이클한 셀의 흑연이 더 상했다" 이며, 이는 descriptor 의 물리 귀속을 직접
증명하지 않는다.

---

## 4. §"ΔPeak_S2 as a Key Descriptor" (p.2948–2949, Fig. 2) — n=2 사례연구

### 4.1 설계

`[인쇄]` "multiple LFP/Gr commercial cells were operated for **one cycle**, and
their **first charging profiles** were analyzed by focusing on ΔPeak_S2. …
two cells were identified as homogeneous and heterogeneous cells based on their
**large and small values of ΔPeak_S2**".

`[인쇄]` 결과: 80 % 용량 유지까지 **373 사이클**(균질) vs **193 사이클**
(비균질).

### 4.2 Fig. 2 (**직접 봄**)

`[도표]` `fig_2.png` 6패널.

- **(a)** y = `dV dQ⁻¹ (V Ah⁻¹)` 0.0–0.6, x = `Capacity (Ah)` 0.0–1.0.
  하늘색 = `Homogeneous cell`, 분홍 = `Heterogeneous cell`.
  **초록 굵은 점선 사각형**이 x ≈ 0.28–0.68 을 감싼다.
  왼쪽에 **두 개의 세로 양방향 화살표**(하늘색·분홍)가 x ≈ 0.24, 0.28 위치에
  나란히 그려지고, 각각 자기 색의 valley 수준 점선과 ridge 수준 점선 사이를
  잇는다 (= ΔPeak_S2 두 개의 시각 비교).
  `[도표]` 눈으로 읽은 값: 하늘색 ridge ≈0.24 @ 0.585, valley ≈0.045;
  분홍 ridge ≈0.20 @ 0.575, valley ≈0.062.
  → ΔPeak_S2 ≈ **0.195** vs **0.138**; Peak_S2 ≈ **0.24** vs **0.20**.
  두 곡선은 0.15 Ah 의 S4 ridge(≈0.51 둘 다)와 그 왼쪽에서는 **거의 겹친다**.
- **(b)** y = `Capacity (Ah)` 0.7–1.0, x = `Cycle` 0–500. 산점.
  하늘색은 ≈0.93 에서 시작해 완만히 감소, **100·200·300 사이클마다 RPT 로 인한
  불연속 점프**가 보인다. 분홍은 100 사이클 이후 급격히 꺾여 ≈190 에서 0.7 을
  통과. 검은 수평 점선이 **0.80 Ah** 에 있다.
- **(c)** 측면 단면 XRM. 상: `Homogeneous cell`, 하: `Heterogeneous cell`.
  `Cu`(주황 화살표, 얇고 밝은 선) 와 `Gr | Cu | Gr`, `LFP | Al | LFP` 라벨.
  각 이미지 아래에 전극 가장자리를 이은 **주황(Cu/anode)·하늘색(Al/cathode)
  선**이 그려져 있는데, 균질 셀은 **거의 직선**, 비균질 셀은 **뚜렷하게
  물결친다**. 우측 확대 4장 중 아래 2장에 **빨간 화살표 + `cathode overhang`**
  라벨.
- **(d)/(f)** 상면 단면 XRM (균질/비균질). 밝은 원형 캔 안에 나선 젤리롤.
  scale bar 1 mm.
- **(e)** 두 젤리롤의 **중심 공동(core void)** 을 색으로 채운 비교: 하늘색
  (균질)은 거의 완전한 원, 분홍(비균질)은 회색 배경 안에서 **한쪽이 찌그러진**
  원. 각각 검은 점선 원(외접원)이 겹쳐 있다.

`[해석]` **★ Fig. 2a 가 리뷰(Wang 2025) Fig. 5c 의 원본이다.** 축·색·초록
사각형·화살표가 일치한다. 따라서 우리가 리뷰 Fig. 5c 에서 읽은 값
(peak≈0.24/valley≈0.05, peak≈0.19/valley≈0.07) 은 **정확했다** — 그림 판독은
맞았고, 틀린 것은 **그 화살표가 논문의 대표 descriptor 라는 추론**이다
(§9.1).

`[해석]` **★ Fig. 2b 와 본문 수치가 어긋난다.** 본문은 "retained 80 % of their
initial capacities for **373** and **193** cycles" 라 하는데, 도표에서 두 곡선이
**0.80 Ah 수평 점선**을 지나는 지점은 각각 ≈240 과 ≈125 사이클이다.
Q_BOL ≈ 0.93 Ah 로 두면 SOH80 = 0.744 Ah 이고, 그 높이를 지나는 지점은
≈340–350 과 ≈185 로 본문 수치에 가깝다. **즉 0.80 Ah 점선은 SOH80 기준선이
아니다** (아마 공칭 1 Ah 대비 0.8). 캡션·본문 어디에도 이 점선의 정의가 없다.

### 4.3 구조적 상관 (XRM)

`[인쇄]`

- 균질 셀: "an **even alignment with a uniform anode overhang**".
- 비균질 셀: "the anodes and cathodes … were **misaligned** such that the edges
  of some cathodes extended beyond the upper ends of the surrounding anodes
  (**"cathode overhang,"** the opposite of anode overhang)". 위험: "Li can be
  plated on the upper edge area of the Gr anode due to **oversupply of Li from
  the protruding cathode**, giving rise to **short circuits**."
- 젤리롤 진원도: 균질 = 원형, 비균질 = **타원형**. MCC(maximum circumscribed
  circle) 법으로 코어 공동의 roundness error (R_out − R_in):
  **균질 0.21 mm, 비균질 0.64 mm (3배)**.

`[해석]` **이것이 이 논문에서 물리 귀속에 가장 가까운 실측이다.** 그러나
(i) **n = 2**, (ii) 재는 것은 흑연의 리튬화 균질성이 아니라 **전극 정렬과
젤리롤 진원도**(제조 기하), (iii) descriptor 와 기하 사이의 인과 방향이
"기하 결함 → 국소 전류 집중 → 리튬화 분산 → DV peak 완화" 라는 **가정된 사슬**
이며 중간 항이 측정되지 않았다. 강한 정황이지만 귀속의 증명은 아니다.

---

## 5. §"Lifetime Prediction … by Correlating with ΔPeak_S2" (p.2949–2950) — 77셀 본실험

### 5.1 데이터셋 (정본은 SI)

`[인쇄, SI]`

| 항목 | 값 |
|---|---|
| 셀 | **상용 LFP/Gr, IFR18500 (China)**, 77개 |
| 공칭 | **1 Ah**, **3.2 V** |
| 사이클 프로토콜 | **1C CC 충·방전, 2.5–3.9 V, 25 °C** (전 셀 동일) |
| 장비 | WBCS 3000 (WonATech) · 챔버 IL-11 (JEIO TECH) |
| RPT | **100 사이클마다**. 0.2C 3연속 사이클(용량) → DVA → DCIR |
| DCIR | 0.2C 로 3.35 V(= SOC50)까지 올린 뒤 0.1C/0.5C/1C 펄스 충·방전 **10 s 폭, 10 min 간격**; I–V 기울기 = 저항 |
| descriptor 추출 시점 | **첫 RPT 의 세 번째 사이클** dV/dQ (SI 명시) |
| cycle life | SOH80 도달 사이클 수; **100 사이클 간격 용량점을 다항 회귀로 보간** |

`[인쇄]` 관측된 수명 범위: "**from 151 to 567 cycles**", 동일 조건에서 —
"revealing the variation in the quality of the manufactured cells."

`[인쇄, Table S2]` 77셀 변수 통계:

| 변수 | 평균 | 표준편차 |
|---|---|---|
| Cycle life | 295.4 | 92.0 |
| **Peak_S2 intensity (V Ah⁻¹)** | **0.211** | **0.014** |
| Peak_S4 intensity (V Ah⁻¹) | 0.310 | 0.033 |
| 1st DCIR (Ω) | 0.169 | 0.010 |
| 1st capacity (Ah) | 0.989 | 0.008 |
| Var(ΔQ₁₀₀₋₁₀(V)) | 0.0005 | 0.0003 |

### 5.2 ★ 절대값으로의 교체 — 인쇄된 그대로

`[인쇄]` (p.2949, 이 논문에서 가장 중요한 방법론 문장):

> "Note that **the Peak_S2 intensity was used in this analysis instead of the
> ΔPeak_S2 intensity because of the fluctuation in the valley near 0.4 Ah,
> which is attributed to the limited resolution of voltage detection when the
> voltage plateaued at the transition from stage III to stage II.**
> The Pearson correlation coefficient of the ΔPeak_S2 intensity was **0.75**
> (Figure S12)."

`[해석]` 세 가지가 여기서 확정된다.

1. **대표 descriptor 는 절대 ridge 값이다.** 진폭이 아니다.
2. **버린 이유는 물리가 아니라 측정 노이즈다** — LFP 의 전압 플래토
   (stage III → II 전이 구간)에서 전압 분해능이 valley 를 흔든다.
3. **성능은 절대값 쪽이 더 좋다** (0.82 > 0.75). 즉 valley 를 빼는 것이
   **정보를 더하지 않고 노이즈만 더했다**.

`[해석]` **★ 세미나의 PVS 에 대한 직접적 함의**: PVS 는 peak−valley 를 쓰고
**추가로 valley 위치의 전압까지** 분모에 넣는다. LFP 만큼은 아니어도
NCM‖Gr 의 mid-SOC valley 역시 평탄한 구간이며, 우리 [[mode-observability]]
Phase 1 이 이미 "PVS 값이 valley 정의(인접 최소 vs 창내 전역 최소)에 민감"
하다고 실측했다. **이 논문은 같은 병을 만나 valley 를 버리는 쪽을 택했다.**

### 5.3 Fig. 3 (**직접 봄**)

`[도표]` `fig_3.png` 3패널. 컬러바 = `Cycle life` 100(진분홍) → 500(진청).

- **(a)** y = `Capacity (Ah)` 0.7–1.0, x = `Cycle` 0–700. 77개 셀의 용량
  궤적이 겹쳐 있고 색이 수명 순. **100 사이클마다 세로로 튀는 점 뭉치**(RPT
  0.2C 용량점)가 뚜렷하다. 수평 검은 점선이 0.80 Ah. 가장 오래 간 진청 곡선이
  ≈605 사이클에서 0.705 Ah 로 끝난다.
  `[해석]` 진청(수명 500+) 셀조차 0.80 Ah 점선을 ≈410 에서 통과한다 → **(a)
  에서도 0.80 Ah 점선은 SOH80 기준선이 아니다** (Fig. 2b 와 같은 문제).
- **(b)** y = `dV dQ⁻¹` 0.0–0.6, x = `Capacity (Ah)` 0.0–1.0. 77셀의 **첫 RPT**
  DV 곡선. **분홍(단명) 군이 0.57 Ah 근방에서 ridge ≈0.19, 진청(장수) 군은
  0.59 Ah 근방에서 ridge ≈0.25**. valley 는 분홍 ≈0.065, 청 ≈0.05.
  0.15 Ah 의 S4 ridge 는 두 군이 ≈0.51–0.55 로 **거의 겹친다**.
  `[해석]` **분리가 Peak_S2 에만 나타나고 Peak_S4 에는 거의 없다** — Table 1
  에서 PeakS4 모델이 dummy 수준인 것과 일관된다.
- **(c)** ★ y = `Cycle life` 0–600, x = `Peak_S2 intensity (V Ah⁻¹)`
  **0.18–0.24**. 77점 산점 + 검은 점선 회귀선. 좌하(0.178, ≈160)에서
  우상(0.237, ≈565)으로 상승. `ρ = 0.82` 인쇄. 색이 y 와 동조 (같은 양을
  색으로도 인코딩).
  `[도표]` **x 범위 0.18–0.24 는 Table S2 의 평균 0.211 ± 0.014 와 맞고,
  Fig. 2a 에서 눈으로 읽은 ridge 절대값(0.20, 0.24)과도 맞는다** → `Peak_S2
  intensity` 가 **절대 ridge 높이**임을 도표로 재확인.

`[도표]` `fig_S12.png`: y = `Cycle life` 0–600, x = **`ΔPeak_S2 intensity`
0.10–0.20**, `ρ = 0.75`. **x 범위가 Fig. 3c 와 완전히 다르다** (0.10–0.20 vs
0.18–0.24) → 두 descriptor 가 **서로 다른 양**임이 축만으로 확정된다.
산점의 흩어짐이 Fig. 3c 보다 눈에 띄게 크다.

### 5.4 예측 모델 (SI 가 정본)

`[인쇄, SI]`

- 모델: **ridge regression, univariate** (특징 1개). λ 는 각 CV 반복에서
  `GridSearchCV` 로 최적화.
- 분할: **테스트 20 % 홀드아웃** → 나머지에 **K = 5** CV → **1000회 무작위
  분할(shuffling)** 반복.
- 지표: RMSE, **MAPE** (SI 의 수식은 절대값을 포함한 정통 MAPE).
- 구현: Python + pandas, NumPy, scikit-learn.

`[인쇄, Table 1]` (본문은 열 이름을 `MPE` 로, SI 수식은 `MAPE` 로 적는다.
괄호 안은 표준편차):

| 모델 | RMSE train | RMSE test | MPE train (%) | **MPE test (%)** |
|---|---|---|---|---|
| Dummy regressor | 92 | 93 | 28.2 (5.5) | **28.5 (4.8)** |
| **Peak_S2 intensity** | **52** | **51** | **13.6 (0.7)** | **13.5 (2.4)** |
| Peak_S4 intensity | 81 | 81 | 22.8 (1.1) | 22.8 (3.9) |
| first IR | 93 | 94 | 28.3 (1.2) | 28.5 (4.7) |
| first Q | 94 | 94 | 28.4 (1.3) | 28.6 (4.9) |
| **Var(ΔQ₁₀₀₋₁₀(V))** (Severson) | 60 | 60 | 15.6 (1.0) | **15.6 (2.8)** |

`[인쇄]` 본문의 주장:

> "it produced a **significantly smaller** prediction error than the dummy
> regressor **but larger than the one based on the Peak_S2 intensity**. From a
> practical viewpoint, our method based on the Peak_S2 intensity is attractive,
> as it **requires only the voltage profile in the first cycle**."

`[해석]` **★ "significantly smaller" 는 보고된 산포로 지지되지 않는다.**
13.5 (2.4) vs 15.6 (2.8) — 차이 2.1 %p 는 **각각의 표준편차보다 작다.**
1000회 반복의 분포가 크게 겹친다는 뜻이며, 유의성 검정은 제시되지 않는다.
`[도표]` `fig_S13.png` 를 직접 보면 이 판단이 확인된다: (a) Peak_S2(초록,
RMSE ≈35–70)는 dummy(회색, ≈70–135)와 거의 겹치지 않지만, (e) Var(ΔQ)(황토,
≈30–80)의 구름도 dummy 와 분리되어 있고 **(a) 와 (e) 의 구름은 서로 상당히
겹친다.** 즉 **dummy 대비 우위는 확고하고, Severson descriptor 대비 우위는
확고하지 않다.**

`[해석]` 다만 **실용적 우위는 실재한다**: Var(ΔQ₁₀₀₋₁₀) 는 정의상 **100
사이클**이 필요하고 Peak_S2 는 **첫 RPT 3번째 사이클** 하나면 된다. 논문의
주장을 "정확도가 더 좋다" 가 아니라 "**같은 정확도를 100배 적은 데이터로**"
로 읽으면 방어된다.

`[도표]` `fig_S14.png` (4패널, y = `Cycle life` 0–600): (a) x =
**`ΔPeak_S4 intensity` 0.24–0.40**, `ρ = 0.51`; (b) x = `DCIR (Ω)` 0.15–0.20,
`ρ = 0.01` (회귀선이 **수평**); (c) x = `Capacity (Ah)` 0.97–1.01, `ρ = 0.14`;
(d) x = `Var(ΔQ₁₀₀₋₁₀(V)) (×10⁻⁴)` 0–16, `ρ = −0.73`.

`[해석]` **(b)(c) 가 이 논문의 가장 좋은 대조군이다.** 첫 사이클 용량과 DCIR
은 수명과 **사실상 무상관**인데(ρ = 0.14, 0.01) Peak_S2 는 0.82 다. 따라서
Peak_S2 의 예측력은 "용량이 큰 셀이 오래 산다" 같은 자명한 경로가 아니다.
`[해석]` 특히 1st capacity 의 산포가 0.989 ± 0.008 Ah (0.8 %) 로 매우
좁은 데 반해 Peak_S2 산포는 0.211 ± 0.014 (6.6 %) 다 — **dV/dQ 의 전체
스케일이 용량에 반비례한다는 자명한 커플링으로는 설명되지 않는 크기**다.

---

## 6. §"Peak_S2 as a Tool for Cell Inspection" (p.2950–2952, Fig. 4·5)

### 6.1 등급화와 모듈 구성

`[인쇄]` 3군: **low (0.18−0.20), middle (0.20−0.22), high (0.22−0.24)**.
5개 모듈 × **6셀 병렬(니켈 판 용접)**:

| 모듈 | 선별 기준 |
|---|---|
| 1 | low Peak_S2 |
| 2 | middle Peak_S2 |
| 3 | high Peak_S2 |
| 4 | **controlled first-cycle capacity (1st Q)** — 1st Q 는 모듈 2 와 비슷하되 Peak_S2 는 전 범위에 걸침 |
| 5 | **controlled first-cycle IR** — 동일 논리 |

`[인쇄, SI]` 모듈은 **1C (6 A)** 로 사이클, 100 사이클마다 **0.2C (1.2 A)**
용량 확인. 모듈 수명 정의는 셀과 동일(SOH80).

`[인쇄, Table S1]` 모듈 4·5 의 대조가 성립함을 보이는 표:
middle Peak_S2 모듈 Q 평균 0.987 (std 0.0102) vs controlled 1st Q 모듈 0.987
(std 0.0105); IR 평균 0.162 (std 0.0051) vs controlled 1st IR 0.162
(std 0.0049).

### 6.2 Fig. 5 (**직접 봄**)

`[도표]` `fig_5.png` 3패널.

- **(a)** 박스플롯. y = `Cycle life` 0–600, x = 3군(`0.18~0.2` 빨강,
  `0.2~0.22` 보라, `0.22~0.24` 파랑). 검은 점 = Mean, 빨간 점 = Outliers.
  `[도표]` 평균 ≈**185 → 310 → 378**. IQR: 빨강 ≈170–200(매우 좁음),
  보라 ≈265–335, 파랑 ≈320–405. 빨간 이상치는 보라군에 1개(≈478), 파랑군에
  2개(≈530, ≈565).
  `[해석]` **저(低)군의 산포가 극히 좁고 고(高)군이 넓다** — 등급화는 "낮은
  Peak_S2 = 확실히 단명" 을 잘 잡고, "높은 Peak_S2 = 오래 산다" 는 덜 확실하다.
  불량품 스크리닝이라는 논문의 용도에는 오히려 유리한 비대칭이다.
- **(b)** x = `Peak_S2 intensity` 0.18–0.24, y 축은 3행(`Peak_S2 control`,
  `Q control`, `IR control`). 세로 회색 점선 2개가 0.20·0.22 에 있어 3군을
  나눈다. 1행: 빨강/보라/파랑 사각형이 각자 자기 구간 안에 촘촘히 모여 있다.
  2행(주황 원)·3행(초록 삼각형)은 **세 구간에 흩어져 있다** — 설계 의도대로.
- **(c)** y = `SOH (%)` 70–100+, x = `Cycle` 0–430. 5모듈 궤적. 모든 모듈이
  **첫 사이클에 100 → ≈91 %** 로 급락한 뒤 완만히 감소. 100 사이클마다 RPT
  점프. `[도표]` SOH 70 % 도달: 빨강(module 1, low) ≈190, 초록(module 5,
  IR) ≈250, 주황(module 4, Q) ≈258, 보라(module 2, middle) ≈282,
  파랑(module 3, high) ≈340 (그리고 파랑 점 하나가 ≈415, 74 %).

`[인쇄]` 순서: "module 3 (high) > module 2 (middle) > module 4 (controlled 1st
Q) > module 5 (controlled 1st IR) > module 1 (low)".

`[인쇄]` 핵심 주장:

> "**the cycle life of modules 4 and 5 was inferior to that of module 2 even
> though their average Peak_S2 intensities, thus their average expected cycle
> life, were almost the same as that of module 2**, which reconfirms the
> importance of the **consistent performance** of individual cells in a module."

`[인쇄]` 그리고 Fig. S16: SOH70 까지 갔을 때 개별 셀 용량 감소의 **편차**가
모듈 4·5 에서 모듈 1–3 보다 크다.

`[해석]` **이것이 이 논문에서 유일하게 "개입(intervention)" 에 해당하는
실험이다** — descriptor 를 관측이 아니라 **조작 변수**로 써서 모듈을 짓고
결과를 봤다. 상관연구에서 한 발 나아간 설계이며, n = 5 모듈(각 6셀)로 작지만
방향은 옳다. 다만 모듈 4·5 가 모듈 2 보다 나쁜 것은 "**분산이 크면 병렬 모듈이
나쁘다**" 는 일반 명제이지 Peak_S2 의 물리를 증명하지 않는다 — 어떤 수명
예측 변수든 그 분산을 좁히면 같은 결과가 나온다. 안 봄: `fig_4.png`(개념
도식), `fig_S15.png`, `fig_S16.png`.

### 6.3 결론절

`[인쇄]` "the **Peak_S2 intensity** was identified as the descriptor that
reflects the **lithiation heterogeneity of the Gr anode**." 그리고 BMS 에
"various chemical descriptors" 를 심는 미래상.

---

## 7. SI 에만 있는 것 (본문에 없는 정본 정보)

### 7.1 ★ descriptor 정의의 정본 (SI p.2–3)

`[인쇄, SI]` 전문:

> "All parameters except for ΔQ₁₀₀₋₁₀(V) were **evaluated from the initial
> three cycles in the first RPT protocol before cycling**. The parameters
> (Peak_S2 and Peak_S4 intensity) related to dV dQ⁻¹ profile used the data in
> the **third cycle of the first RPT**. **The ΔPeak_S2 intensity corresponds to
> the difference between the ridge near 0.6 Ah and the valley near 0.4 Ah in
> the transition to stage Ⅱ. The Peak_S2 intensity is the absolute value at the
> ridge.** The ΔpeakS4 intensity corresponds to the difference between the
> ridge near 0.1 Ah and the valley near 0.15 Ah in the stage Ⅳ."

`[해석]` **이것이 §9.1 판정의 정본이다.** 두 문장이 두 descriptor 를 명확히
가른다:

```
ΔPeak_S2 = dV/dQ|ridge≈0.6Ah  −  dV/dQ|valley≈0.4Ah      (진폭, 사용 안 함)
Peak_S2  = dV/dQ|ridge≈0.6Ah                              (절대값, ★ 사용)
```

`[해석]` **정의에 없는 것**: 미분 방법, 평활화, 전압/용량 격자, ridge 를 찾는
알고리즘(국소 최대? 창내 전역 최대?), 창의 정확한 경계. "near 0.6 Ah" 이
전부다.

### 7.2 프로토콜·장비 세부 (§5.1 표에 이미 반영)

본문에는 없고 SI 에만 있는 것: 셀 모델명 **IFR18500**, 공칭 1 Ah/3.2 V,
전압 창 **2.5–3.9 V**, 사이클러/챔버 모델, DCIR 펄스 사양(10 s / 10 min,
SOC50 = 3.35 V), 모듈 6셀 **병렬** 니켈 판 용접, cycle life 의 **다항 회귀
보간**, ridge regression·K=5·1000회 반복·GridSearchCV.

`[인쇄, SI]` 통계 관례: "|ρ| > 0.8 was usually considered to have a **strong
correlation**^3. ρ is statistically significant **when both variables follow a
normal distribution**^4." 박스플롯 whisker = 1.5 × IQR.

`[해석]` "두 변수가 정규분포일 때 유의" 라고 적어 두었지만 **정규성 검정
결과는 없다**. Fig. 3c 의 y(cycle life) 분포는 151–567 로 오른쪽 꼬리가 길다.

### 7.3 ★ 원문 내부의 표기 불일치 세 건

`[해석]` SI 를 본문·도표와 대조하면 라벨링이 어긋나는 곳이 셋 있다. 인용할 때
주의해야 한다.

1. **`Peak_S4` vs `ΔPeak_S4`.** Table 1 과 SI Fig. S14 **캡션**은
   "Peak_S4 intensity" 라고 쓰는데, **Fig. S14a 의 x축 라벨은
   `ΔPeak_S4 intensity` (0.24–0.40)** 이다. 그리고 Table S2 의
   "Peak_S4 intensity = 0.310 ± 0.033" 은 **Fig. S14a 의 Δ 범위와 일치**한다
   (절대 ridge 는 `fig_S3.png` 에서 ≈0.55). → **S4 계열은 사실상 Δ 값을 쓰면서
   이름만 `Peak_S4` 로 적은 것으로 보인다.** S2 계열은 반대로 절대값이다
   (Table S2 0.211 = Fig. 3c 축 범위와 일치).
2. **ΔPeak_S4 의 ridge/valley 위치가 SI 본문과 그림에서 뒤바뀌어 있다.**
   SI 는 "ridge near **0.1** Ah and the valley near **0.15** Ah" 라 적는데,
   `[도표]` `fig_S3.png` 의 주황 화살표는 **valley ≈0.29 @ ≈0.09 Ah** 에서
   **ridge ≈0.55 @ ≈0.15 Ah** 로 그어져 있다 — 위치가 서로 바뀌었다.
3. **`MPE` vs `MAPE`.** 본문과 Table 1 은 "mean percent error (MPE)",
   SI 수식은 절대값을 포함한 **MAPE** 다. 리뷰(Wang 2025)가 "MAPE 13.5 %" 로
   적은 것은 **SI 수식 기준으로 옳다**.

### 7.4 SI 에 **없는** 것

`[해석]` descriptor 계산의 수치적 세부, 추가 셀군, 재현성(같은 셀 재측정)
데이터, 불확실성 정량 — **없다**. SI 는 프로토콜·통계 절차·보조 도표로만
구성되어 있고, 1·2항(정의·귀속)에 대해 SI 가 추가로 주는 것은 **§7.1 의 두
문장뿐**이다. 그 두 문장이 결정적이었다.

---

## 8. 식별 가능성·불확실성 어휘 전수 확인

`[방법]` 본문·SI PDF 를 pymupdf 로 텍스트 추출한 뒤 합자 `ﬁ ﬂ ﬀ ﬃ ﬄ` 를
정규화하고 대소문자 무시로 세었다 (참고문헌 목록 포함).

| 어휘 | 본문 (8쪽) | SI (24쪽) |
|---|---|---|
| `identifiab` | **0** | **0** |
| `uniqu` | **0** | **0** |
| `degenerat` | **0** | **0** |
| `non-unique` | **0** | **0** |
| `ill-posed` | **0** | **0** |
| `collinear` | **0** | **0** |
| `uncertain` | **0** | **0** |
| `confidence` | **0** | **0** |
| `correlat` | 17 | 5 |
| `heterogen` | **58** | 3 |
| `homogen` | 24 | 2 |
| `half-cell` / `half cell` | **0** | **0** |
| `simulat` | **0** | **0** |
| `LLI` (약어) | **0** | **0** |
| `LAM` (약어) | **0** | **0** |
| "lithium inventory" | 1 (서론) | 0 |
| "active material" | 1 (서론) | 0 |
| `OCV` | 2 (둘 다 "OCV drop" = 입고검사 항목) | 0 |

`[해석]` 패턴은 [[birkl-ocv-degradation-diagnostic]]·
[[interpretable-ml-battery-prognosis-taxonomy]] 때와 **동일**하다: 식별
가능성·불확실성 어휘가 **전부 0회**. 이 계보에서 네 편 연속이다.

`[해석]` 특기할 것은 `correlat` 22회 vs `simulat` 0회 다. **이 논문은 순수하게
상관 기반이며 물리 모델(P2D/SPM)을 한 번도 돌리지 않는다.** 세미나 p.8 이
PVS 의 모드 의존성을 P2D 단독 스윕으로 보인 것과 대비된다 — 두 문헌은
**증거의 종류가 다르다**.

`[해석]` `heterogen` 58회 vs `LLI/LAM` 0회 는 이 논문의 좌표계를 그대로
보여 준다. **이 논문의 축은 "공간적 불균일성"이지 "열화 모드"가 아니다.**

---

## 9. ★ 판정 — 리뷰의 요약은 옳았는가

### 9.1 descriptor 정의: 리뷰의 **단어는 옳고**, 우리 위키의 **추론은 틀렸다**

| 주장 | 판정 | 근거 |
|---|---|---|
| 리뷰(Wang 2025): "DV 프로파일의 **peak intensity**" | **옳다** | 초록·Table 1·Fig. 3c·SI 가 모두 `Peak_S2 intensity` 를 대표 descriptor 로 쓴다 |
| 우리 위키: "그 intensity 는 실제로는 **peak−valley 진폭**" | **틀렸다** | SI: "**The Peak_S2 intensity is the absolute value at the ridge.**" 진폭은 `ΔPeak_S2` 라는 **다른 이름의 다른 변수**이고, valley 노이즈 때문에 **버려졌다** |
| 리뷰: "cycle life, 첫 사이클 전압 프로파일만으로 MAPE 13.5 %" | **거의 옳다** | 13.5 % 는 Table 1 test MPE(=SI 정의상 MAPE) 그대로. 다만 정확히는 "**첫 RPT 의 3번째 0.2C 사이클**" 이다 (본문은 "first cycle" 이라 쓰지만 SI 가 더 정확하다) |

`[해석]` **우리 위키의 오류가 어디서 났는지가 중요하다.** 리뷰 Fig. 5c 는
이 논문 **Fig. 2a 의 재수록**이고, Fig. 2a 에는 ΔPeak_S2 화살표가 그려져 있다.
그림 판독 자체는 정확했다. 틀린 것은 "**그림에 그려진 화살표 = 논문이 쓴
descriptor**" 라는 **한 단계의 추론**이다. 이 논문은 **정의 그림(Fig. 1d,
2a)에는 진폭을 그리고, 실제 분석(Fig. 3, Table 1, Fig. 5)에는 절대값을 쓴다.**
그림만 보고는 알 수 없고 SI 를 읽어야 알 수 있었다.
`[해석]` 이것은 "그림을 봐라" 규칙의 **역방향 교훈**이다 — 그림은 본문
서술을 교정하지만, 그림이 본문·SI 를 이기지는 않는다.

### 9.2 물리 귀속의 근거: **half-cell 없음, 시뮬레이션 없음, 양극 검토 없음**

이 논문이 "Peak_S2 ↔ 흑연 리튬화 불균일성" 을 지지하는 데 쓰는 근거를 강한
순서로:

| # | 근거 | 종류 | 강도 평가 `[해석]` |
|---|---|---|---|
| 1 | **선행문헌 ref 14** (Lewerenz/Sauer 2017, **LFP\|Gr 원통형**): "the sharpness of the peak on the DV profile reflects the homogeneity of Li intercalation in the Gr anode" | 인용 | **귀속의 실질적 출처.** 이 논문이 세운 것이 아니다 → 원전 확인이 남는다 |
| 2 | **기구론 도식** Fig. 1a–c | 개념도 | 국소 SOC 분산 → 전이 폭 확장 → 기울기 완화. 물리적으로 타당하나 **데이터가 아니다** |
| 3 | **XRM 구조 상관** Fig. 2c–f (roundness 0.21 vs 0.64 mm, cathode overhang) | 실측, **n = 2** | 재는 것이 흑연 리튬화가 아니라 **조립 기하**. 중간 항 미측정 |
| 4 | **운전조건 경향** Fig. S2 (저온·고율 → descriptor 하락) | 실측, 조건당 1셀 | **모드 조합 변화와 구분 불가** (§3.2) |
| 5 | **해체** SEM/ToF-SIMS/DMC (Fig. S5–S9) | 실측 | 대상이 descriptor 실험군이 아니라 **조건 비교군** |
| 6 | 모듈 개입 실험 Fig. 5 | 실측, n = 5 모듈 | descriptor 의 **유용성**을 지지하나 **물리 귀속과 무관** |

**없는 것**: half-cell / 3-전극 / 참조전극, 전기화학 시뮬레이션, 공간분해
Li 측정(중성자·XRD 등 — ref 18 은 인용만), 양극의 dV/dQ 기여 분석.

`[해석]` **양극은 배제된 것이 아니라 논의되지 않았다.** LFP 의 평탄 OCP 를
근거로 든 문장조차 없다. 즉 이 논문이 주는 것은 "**LFP‖Gr 에서 관례적으로
흑연에 귀속되는 stage-II ridge 를 쓴다**" 이지, "양극이 아님을 보였다" 가
아니다.

### 9.3 셀·화학: **같은 계열이 아니다** — "충돌" 이 아니라 "다른 대상"

| 항목 | **Kim 2023 (이 논문)** | **2026-09-02 세미나 (PVS)** |
|---|---|---|
| 양극 | **LFP** (2상, OCP 거의 평탄) | **NCM811** (고용체 + H1→M 상전이, OCP 구조적) |
| 음극 | graphite | **Si–graphite** |
| 폼팩터 | 원통형 **IFR18500**, 공칭 **1 Ah** | 18650 **MJ1** (세미나 기준) |
| 전압창 | 2.5–3.9 V | ~2.5–4.2 V |
| 곡선 표현 | **dV/dQ vs Q** (V Ah⁻¹) | **dQ/dV vs V** (Ah V⁻¹) |
| 사용 기하량 | **ridge 의 절대 높이** (스칼라 1개) | **peak−valley 를 전압 간격으로 나눈 할선 기울기** |
| 관심 구간 | 흑연 stage III→II 전이 (≈0.6 Ah) | mid-SOC 3.55–3.9 V |
| 물리 귀속 | **흑연 음극 단일** (공간적 리튬화 불균일성) | **peak2 = PE 상전이 / valley2 = NE stage-2 의 대비** |
| 예측 대상 | **cycle life** (수명, 스칼라) | **LLI / LAM_PE / LAM_NE** (전극 수준 모드) |
| 축의 성격 | **제조 변동 → 수명** | **열화 모드 분해** |
| 증거 종류 | 상관 + 구조 관찰 (시뮬레이션 0) | P2D 단독 모드 스윕 |

`[해석]` **LFP 셀에서 full-cell dV/dQ 의 극값 구조는 사실상 흑연의 것이다** —
2상 양극의 OCP 가 평탄해 dV/dQ 기여가 미미하기 때문이다. 따라서 이 논문의
음극 단일 귀속은 **그 화학에서는 거의 강제**이고, **다른 화학으로 일반화되는
주장이 아니다.** NCM811 은 사정이 다르다 — 세미나가 peak2 를 H1→M 상전이에
붙이는 것은 NCM 의 dQ/dV 에 실제 봉우리가 있다는 사실에 기댄 것이고, 이
논문은 그것을 반박하지 않는다 (NCM 셀을 다루지 않으므로).

`[해석]` **결정적으로, 두 문헌이 재는 양이 다르다.** 이 논문의 대표
descriptor 는 **valley 를 쓰지 않는다.** "같은 기하학적 양에 두 문헌이 다른
물리 귀속을 준다" 는 우리 Gap 의 전제 자체가 성립하지 않는다 — **valley 를
쓰는 변형(ΔPeak_S2)은 이 논문이 버린 쪽**이고, 그마저도 두 전극의 대비로
해석된 적이 없다 (LFP 셀에서는 그렇게 해석할 이유도 없다).

### 9.4 그래서 판정은

`[해석]` **(ii) 두 해석은 양립한다 — 서로 다른 대상을 재고 있다.**
근거를 다시 모으면:

1. **descriptor 가 다르다**: 절대 ridge 높이(Kim) vs peak−valley 할선
   기울기(세미나). 전제였던 "같은 기하량" 이 거짓이다.
2. **화학이 다르다**: LFP(평탄 OCP, 양극 기여 무시 가능) vs NCM811(구조적
   OCP). 음극 단일 귀속은 LFP 에서 강제된 것이다.
3. **묻는 질문이 다르다**: 제조 변동 → 수명(Kim) vs 열화 모드 분해(세미나).
   Kim 은 LLI/LAM 을 재지도 언급하지도 않는다 (§8: 약어 0회).
4. 따라서 **"음극 단일 귀속이 맞으니 PVS 는 LLI↔LAM_PE 를 잴 이유가 없다"**
   는 추론은 **성립하지 않는다.** 이 논문은 그 명제에 아무 무게도 싣지 않는다.

`[해석]` **그러나 Gap 을 그냥 지우는 것은 손해다.** 이 논문은 원래 Gap 을
닫으면서 **더 날카로운 것 하나**를 남긴다:

> **DV/IC 극값의 크기는 SOH(용량 손실량)의 함수가 아니다.** 같은 SOH 80 %
> 에서 사이클 조건에 따라 ΔPeak_S2 가 0.083 ~ 0.253 (3배) 로 갈린다
> (Fig. S2a, 직접 봄). 이 변동은 열화 모드 분율만으로 설명되지 않는 성분
> (공간 불균일성 / 국소 plating / 계면 상태)을 포함한다.

`[해석]` PVS 에 대한 함의는 **귀속 논쟁보다 무겁다**: PVS 의 분자
(peak−valley)는 같은 종류의 진폭량이므로, **모드 분율이 같아도 셀의 공간
상태가 다르면 PVS 가 달라질 수 있다.** 세미나 p.8 의 P2D 단독 모드 스윕은
**균질 셀 가정** 위에서 계산된 것이고 (P2D 는 1D 이므로 전극면 방향 분산이
없다), 실측 셀의 PVS 에는 이 논문이 재는 성분이 섞여 들어온다.
**즉 PVS 를 모드 관측으로 쓸 때의 위험은 "어느 전극인가" 가 아니라 "모드
이외의 상태변수가 같은 축을 흔든다" 는 쪽이다.**

`[해석]` 추가로, **valley 의 노이즈 민감성**에 대한 독립적 확증을 얻었다.
이 논문은 LFP 플래토에서 valley 가 흔들려 **valley 를 쓰는 변형을 버렸고**,
그렇게 해서 ρ 가 0.75 → 0.82 로 올랐다. 우리 [[mode-observability]] Phase 1
이 PVS 에서 관측한 valley 정의 민감성과 **같은 병**이다.

---

## 10. DV(dV/dQ) vs IC(dQ/dV) — 대응 관계

`[인쇄]` **원문에 이 대응을 논한 곳은 없다.** 이 논문은 dV/dQ vs 용량만 쓰고
dQ/dV 를 한 번도 그리지 않는다. 아래는 전부 `[해석]` 이다.

`[해석]` 수학적으로 두 곡선은 서로 역수다: `dQ/dV = 1/(dV/dQ)`. 따라서
**같은 물리 특징이 서로 뒤바뀐 극값으로 나타난다**:

| dV/dQ (이 논문) | dQ/dV (세미나) | 물리 |
|---|---|---|
| **valley** (dV/dQ 작음) | **peak** (dQ/dV 큼) | 전압 플래토 = 2상 공존 / 상전이 |
| **ridge** (dV/dQ 큼) | **valley** (dQ/dV 작음) | 전압이 빠르게 변하는 구간 = 단일상 / stage 경계 |

`[해석]` **★ 이것이 두 문헌의 "peak" 이 서로 다른 물리를 가리키는 진짜 이유다.**

- Kim 의 `Peak_S2` = dV/dQ 의 **ridge** = dQ/dV 로 옮기면 **valley** →
  **stage 전이 사이의 가파른 구간**, 흑연 단일상 영역에 대응한다.
- 세미나의 `Valley2` = dQ/dV 의 valley = **graphite stage 2 단일상 영역**.

`[해석]` **즉 좌표를 맞추면 Kim 의 ridge 와 세미나의 valley2 가 같은 종류의
특징이다.** 둘 다 "흑연 단일상 구간의 가파름" 을 재고, 둘 다 **음극**에
귀속된다. **모순이 아니라 일치다.** 세미나가 양극에 귀속시키는 것은
`Peak2`(dQ/dV 의 peak = dV/dQ 의 valley = 상전이 플래토)이며, **Kim 의
대표 descriptor 는 바로 그 valley 를 버렸다.**

`[해석]` 이 대응은 §9.4 의 판정 (ii) 를 독립적으로 강화한다. 단, 표현 변환은
**축이 다르면 (Q 축 vs V 축) 자코비안 때문에 극값의 위치가 정확히 대응하지
않는다** — dV/dQ vs Q 와 dQ/dV vs V 는 같은 곡선의 다른 매개변수화이고, 극값의
**존재**는 대응하되 **폭·높이의 스케일링은 다르다**. 원문은 이 점을 논하지
않으며, 정량 비교를 하려면 우리가 직접 변환해 봐야 한다.

---

## 11. 우리 프로젝트와의 접점

### 11.1 이 논문이 **주는** 것

1. **★ Fig. S2a** — 같은 SOH 에서 DV 진폭이 3배 갈리는 실측. "관측을 늘리면
   갈리는가" 를 묻는 [[pvs-sev-lli-lampe-separability]] 에 **반대 방향의
   경고**를 준다: DV/IC 진폭 계열 관측은 모드 이외의 상태변수를 함께 싣는다.
2. **valley 회피의 전례** — 진폭/기울기 대신 **단일 극값의 절대값**을 쓰는
   것이 (적어도 LFP 에서) **더 잘 작동했다**. PVS 를 다룰 때 "분모를 없앤
   변형", "valley 를 쓰지 않는 변형" 을 대조군으로 넣을 근거.
3. **대조군 설계의 모범** — 1st Q, 1st DCIR 을 넣어 자명한 경로를 배제하고
   (ρ = 0.14, 0.01), dummy regressor 를 baseline 으로 명시하고, 1000회
   무작위 분할로 분산을 보고했다. 세미나 p.13 의 LOGO-CV 보고보다 이 쪽이
   **재현 가능성 서술이 낫다**. 다만 유의성 검정은 없다 (§5.4).
4. **모듈 개입 실험** — 예측 변수를 조작 변수로 써서 다운스트림 결과를 보는
   설계. 우리가 "식별 가능성 경계" 를 만들었을 때 그것을 **어떻게 써 보일지**
   의 형식적 선례.

### 11.2 우리가 이 논문에 **공급할** 수 있는 것

`[해석]`

1. **모드 대 불균일성의 분리.** 이 논문의 핵심 해석("같은 SOH 에서
   descriptor 가 다르다 = 불균일성이 다르다")은 **모드 조합이 다르다**로도
   똑같이 설명된다 (§3.2). 우리 합성 truth 파이프라인은 **모드를 고정한 채**
   DV ridge 높이가 얼마나 움직이는지 계산할 수 있고, 그러면 Fig. S2a 의 3배
   변동 중 **모드로 설명되는 몫의 상한**을 줄 수 있다. 이것은 이 논문이
   스스로 할 수 없는 계산이다 (시뮬레이션 0회).
2. **descriptor 의 평활화 민감도 경계.** 저자들이 valley 노이즈로 변형을
   포기한 것은 정성적 관찰이다. 우리 쪽 평활화 민감도 작업이 그 경계를
   정량화한다.

### 11.3 가져올 수 있는 관측

`[해석]` **`Peak_S2` 유사량 = dV/dQ ridge 의 절대 높이**는 우리 관측 후보로
값이 싸다 (기존 곡선에서 계산, 새 프로토콜 불필요). PVS 와 달리 **valley
정의에 의존하지 않으므로** [[mode-observability]] Phase 1 이 만난 NaN·민감도
문제를 우회한다. 다만 NCM 셀에서 그 ridge 가 무엇에 귀속되는지는 **이 논문이
답해 주지 않는다** — 우리가 half-cell OCP 로 직접 확인해야 한다.

### 11.4 비판 요약 (이 논문의 약점)

`[해석]`

1. **귀속이 인용에 기대어 있다.** 핵심 물리 주장의 실질적 출처는 ref 14 이며,
   이 논문 안에는 그것을 독립적으로 확립하는 측정이 없다.
2. **불균일성과 모드가 혼동되어 있다** (§3.2) — 이 논문의 가장 큰 공백.
3. **"significantly smaller" 가 산포로 지지되지 않는다** (§5.4).
   13.5 (2.4) vs 15.6 (2.8).
4. **n = 2 의 구조 상관을 서사의 중심에 놓는다** (Fig. 2 는 논문 지면의 큰
   부분을 차지한다).
5. **표기 불일치 3건** (§7.3) — 특히 S4 계열이 Δ 인지 절대값인지 원문 안에서
   확정되지 않는다.
6. **도표의 기준선이 정의되지 않는다** (0.80 Ah 점선, Fig. 2b·3a).
7. **descriptor 계산의 수치적 재현 정보가 없다** (미분·평활화 미기재).
8. **cycle life 정답 축이 다항 회귀 보간값**이고 그 오차가 보고되지 않는다.
   MAPE 13.5 % 는 **보간된 정답에 대한** 오차다.

---

## 12. 크로핑·열람 기록

`[방법]` `python3 wiki/tools/extract_figures.py --slug
kim2023_graphite-heterogeneity-lifetime --pdf <본문> <SI> --clean`
→ **24장 추출** (본문 5 + SI 16 + 표 3; SI 는 `S` 번호로 자동 부여됨).
실제로 **Read 로 본 것은 8장** (표 3장은 관례대로 PDF 텍스트로 읽음).

| 파일 | 봄 | 무엇을 얻었나 |
|---|---|---|
| `fig_1.png` | ✅ | **ΔPeak_S2 정의 그림.** stage 라벨 위치, DV 곡선 형상, 화살표가 ridge−valley 임을 확인 |
| `fig_2.png` | ✅ | **리뷰 Fig. 5c 의 원본.** 두 셀의 ridge 절대값(0.24/0.20)과 진폭(0.195/0.138)을 분리해 읽음. XRM 정렬·cathode overhang·코어 진원도. **Fig. 2b 의 0.80 Ah 점선 불일치 발견** |
| `fig_3.png` | ✅ | **x축 0.18–0.24 로 `Peak_S2` 가 절대값임을 도표로 확정.** 77셀 DV 곡선에서 S2 만 분리되고 S4 는 겹침 |
| `fig_5.png` | ✅ | 3군 박스플롯 평균(≈185/310/378), 저군의 좁은 IQR, 모듈 5종 SOH 궤적 |
| `fig_S1.png` | ✅ | 4조건 DV 진화. 비균질 조건에서 **valley 가 올라오고 peak 이 내려온다** |
| `fig_S2.png` | ✅ | **★ 최고 수확.** 같은 SOH 80 % 에서 ΔPeak_S2 가 0.083–0.253 |
| `fig_S3.png` | ✅ | ΔPeak_S4 화살표 → **SI 본문의 ridge/valley 위치 서술이 그림과 뒤바뀜** 확인 |
| `fig_S12.png` | ✅ | x축 0.10–0.20 → ΔPeak_S2 가 `Peak_S2` 와 **다른 변수**임을 축만으로 확정 |
| `fig_S13.png` | ✅ | RMSE 1000회 구름. Peak_S2 는 dummy 와 분리, **Var(ΔQ) 와는 크게 겹침** |
| `fig_S14.png` | ✅ | ρ: ΔPeak_S4 0.51 / DCIR **0.01** / capacity **0.14** / Var(ΔQ) −0.73. **축 라벨이 캡션과 불일치** |
| `fig_4.png` | ❌ | 개념 도식(입고검사 → 모듈 조립). 정보 없음으로 판단 |
| `fig_S4.png` | ❌ | 방전 DV. 본문이 "쓰지 않는다" 고 결론지은 축 |
| `fig_S5–S9.png` | ❌ | SEM 5장·ToF-SIMS·DMC 사진. **descriptor 실험군이 아닌 조건 비교군**이라 판정 무게가 낮다 (본문 서술로 대체) |
| `fig_S10.png`, `fig_S11.png` | ❌ | XRM 보조 + MCC 작도. Fig. 2c–f 로 충분 |
| `fig_S15.png`, `fig_S16.png` | ❌ | 모듈 셀 분포·편차. Table S1 텍스트로 대체 |
| `tab_1/S1/S2.png` | ❌(의도적) | 표는 PDF 텍스트가 정확 — 전부 §5.1·5.4·6.1 에 옮김 |

`[해석]` **본문 서술과 그림이 어긋난 곳 3건**을 그림을 봐서 발견했다:
(1) Fig. 2b·3a 의 0.80 Ah 점선 vs 본문 cycle-life 수치, (2) Fig. S14a 축
라벨(`ΔPeak_S4`) vs 캡션·Table 1(`Peak_S4`), (3) Fig. S3 화살표 vs SI 본문의
ridge/valley 위치 서술. 셋 다 **캡션만 읽었다면 놓쳤을 것**이다.

---

## 13. 이 digest 가 위키에 남기는 것

1. **[[pvs-sev-lli-lampe-separability]] 의 Gap "PVS 의 물리 귀속이 문헌과
   어긋난다" → 판정 (ii) 로 닫는다.** 전제("같은 기하량")가 거짓이고, 화학이
   다르며, dV/dQ↔dQ/dV 좌표를 맞추면 오히려 **둘 다 음극 단일상 구간을 음극에
   귀속시키는 일치**가 된다 (§10).
2. **대신 새 Gap 을 연다**: DV/IC 극값 진폭이 **모드 이외의 상태변수**
   (공간 불균일성·국소 plating)를 싣는다는 실측 (Fig. S2a). 이것은 PVS 를
   모드 관측으로 쓰는 설계에 대한 **더 날카로운 위협**이다.
3. **[[pvs-sev-degradation-mode-features]] 의 "문헌에서의 자리" 절 정정** —
   "선례가 같은 양을 음극 단일에 귀속시켜 충돌한다" 를 사실관계에 맞게 고친다.
4. 추가 근거: valley 를 쓰는 변형이 **노이즈 때문에 실전에서 버려진** 전례.
