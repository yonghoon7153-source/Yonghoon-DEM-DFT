---
title: "Su et al. 2024 — DRT 유래 health feature 와 GPR SOH 추정 (J. Energy Storage 90)"
source_url: local-upload/7._Modeling_and_health_feature_extraction_method_for_lithiumion_batteries_state_of_health_estimation_by_distribution_of_relaxation_times.pdf
ingested: 2026-09-03
sha256: 5fab7227f0543e6548f5463179d88676ed23547d275f74a72c98174d9957044f
---

# 수집 목적

Zhipeng Su, Jidong Lai\*, Jianhui Su, Chenguang Zhou, Yong Shi, Bao Xie
(School of Electrical and Automation Engineering, Hefei University of
Technology / Research Center for Photovoltaic System Engineering of Ministry
of Education, Hefei 230009, China),
**"Modeling and health feature extraction method for lithium-ion batteries
state of health estimation by distribution of relaxation times"**,
*Journal of Energy Storage* **90** (2024) 111770,
DOI **10.1016/j.est.2024.111770** — 본문 15쪽 전문의 절별 해체분석.

흡수 동기는 **두 개의 판정**이다. 둘 다 다른 문서가 이 논문에 걸어 둔 미결
항목이며, 이 digest 의 임무는 그것을 원문으로 닫는 것이다.

**① 문헌 근거의 원전 확인.** 직전에 흡수한 분야 리뷰
([[interpretable-ml-battery-prognosis-taxonomy]], Wang et al. 2025,
*Adv. Energy Mater.* 15, e03067) 가 §4.4 에서 이 논문을 참조번호 [127] 로
인용하며 다음과 같이 인쇄한다 — `[인쇄, Wang 2025 p.10]`:

> "An example of extracting interpretable features from DRT was provided by
> Su et al., who observed that the variation trends of typical DRT peaks and
> valleys during battery aging **aligned with the increase in charge transfer
> resistance caused by LLI and LAM**. [127]"

이 진술이 사실이면 2026-09-02 세미나의 **SEV**(= R_ct,PE 의 stoichiometry
의존성을 읽는 동역학 feature, concept: [[pvs-sev-degradation-mode-features]])
로 LLI 와 LAM_PE 를 **가르려는** 설계에 직접 불리하다. 두 모드가 같은 물리량을
같은 방향으로 민다면 그 축에는 두 모드를 나누는 정보가 없기 때문이다. 우리
질문 카드 [[pvs-sev-lli-lampe-separability]] 는 이것을 **H1 지지 증거**로
잠정 등록하되 "원전 미확인 — 인용 전에 Su 2024 를 직접 봐야 한다"는 유보를
붙여 두었다. 여기서 그 유보를 푼다.

**② 우리가 지금 쓰는 데이터셋의 출처 확정.** satellite [[mode-observability]]
의 Phase 2(SEV 실측 대조)가 이 논문 SI 의 zip 을 쓰고 있다
(`mode-observability/data/su2024/EIS data/`, 176파일 90 MB). 그 데이터가 이
저자들이 **직접 측정**한 것인지 **선행 공개 데이터셋의 재사용**인지가
확정되지 않아, `mode-observability/manifests/README.md` 에 "출처 확정 전에는
'Su 2024 SI' 로만 적는다" 는 유보가 걸려 있었다. 여기서 그 유보를 푼다.

결론을 먼저 적는다 (근거는 아래 각 절).

- **② 데이터는 저자들이 잰 것이 아니다.** 원문 §2.1 과 Data availability 절이
  **공개 데이터셋의 재사용**임을 명시하며, 원 출처는 **Zhang, Tang, Zhang,
  Wang, Stimming, Lee, *Nature Communications* 11 (2020),
  DOI 10.1038/s41467-020-15235-7**, 데이터 저장소 **Zenodo
  10.5281/zenodo.3633835** 다. 우리 가설이 맞았다. 이제 우리 수치의 출처는
  "Su 2024 SI" 가 아니라 **"Zhang et al. 2020 (Zenodo 3633835), Su 2024 를
  거쳐 입수"** 로 적어야 한다.
- **① 그 진술은 Su 의 측정이 아니라 상속된 인용이며, 게다가 Su 자신의 그림과
  어긋난다.** Su 는 LLI 도 LAM 도 **한 번도 재지 않는다**(반정량 추정조차
  없다). 해당 문장은 자기 DRT 추세를 **다른 논문 [20] 의 진술로 해석**한
  한 문장이고, 정작 Su 가 "charge transfer" 로 이름 붙인 peak(p2)의 높이는
  5셀 중 4셀에서 **노화와 함께 감소**한다. 증거 등급: **인용 상속(3차)이며
  자체 데이터에 의해 부분 반박됨**. → Wang 리뷰의 요약은 문면상 충실하지만
  **증거 등급을 한 단계 올려 옮겼다**(상속된 해석 → Su 의 관찰).
- **그러나 이 논문은 SEV 설계에 더 무거운, 다른 종류의 불리한 증거를 준다.**
  전하전달 peak 높이 γ(lnτ_p2)의 SOH 상관은 **셀에 따라 부호가 뒤집히고**
  (cell1 −0.687 vs cell2 +0.934), 분극저항 R_pol 도 마찬가지로 뒤집힌다
  (cell1 −0.965 / cell2 +0.864 / cell3 −0.397). 두 feature 모두 저자 자신의
  0.75 문턱을 통과하지 못해 **health feature 에서 탈락**했다. 즉 "R_ct 가
  모드에 어떻게 반응하는가" 이전에 **동일 사양 셀 5개 사이에서 부호조차
  안정하지 않다**.
- **전극 귀속은 이 논문에 없다.** `positive electrode`/`negative electrode`
  가 본문 방법·결과부에 0회다(서론에서 남의 논문 [25] 를 요약할 때 1회).
  R_ct,PE 라는 양은 등장하지 않는다. SEV 의 "양극 전하전달 저항" 귀속에
  대해 이 논문은 **찬성도 반대도 하지 않는다** — 다룬 적이 없다.

---

# 원문에 없어서 확인이 필요한 것 (Gap)

이 논문이 **말하지 않는 것**을 먼저 못박는다. 아래는 전부 원문 부재이며,
digest 본문에서 다시 "n/a" 로 표시된다.

| 항목 | 원문 상태 |
|---|---|
| 셀 **형태** (코인셀/파우치/원통형) | **n/a** — "12 LiCoO₂/graphite aging data with a 45mAh capacity" 라고만 쓴다. 형태를 한 번도 적지 않는다. 코인셀 여부는 원 출처(Zhang 2020)에서 확인해야 한다 |
| 셀 제조사·모델명 | **n/a** |
| 사이클링 프로토콜 (충방전 전류·전압창) | **n/a** — Su 는 EIS 조건만 옮겨 적고 노화 프로토콜을 적지 않는다 |
| **state I~IX 각각이 무엇인가** | **부분** — "Nine different states form a charge-discharge cycle" 과 "State V = 100 %SOC, after 15-min rest" 만 인쇄. 나머지 8개 state 의 SOC/시점은 **n/a** |
| LLI·LAM 의 **정량값** | **n/a** — 이 논문은 열화 모드를 재지 않는다. half-cell OCP fitting·ICA/DVA 분해·해체분석 전부 없음 |
| DRT peak 의 **전극 귀속 근거** | **n/a** — 대칭셀·기준전극·half-cell·온도/SOC 스윕 어느 것도 없다. p1/p2/p3 ↔ SEI/전하전달/확산 대응은 **선언**이다 |
| 정규화 파라미터 λ = 1E-3 의 **선택 근거** | **부분** — "Based on a large number of tests and relevant literature" 라고만 쓴다. GCV·L-curve·discrepancy principle 등 **원리적 기준 없음** |
| DRT 의 **불확실성** (신뢰구간·해상도 한계) | **n/a** — DRTtools 는 credible interval 을 낼 수 있으나 쓰지 않았다 |
| 셀 간 일반화 (**cross-cell** 학습/시험) | **없음, 그리고 저자가 인정한다** — §5 limitations 참조 |
| 3개 온도(25/35/45 °C) 중 실제 사용 | **25 °C 만** 사용. 35/45 °C 데이터는 언급만 되고 쓰이지 않는다 |
| 12셀 중 실제 사용 | **5셀** (25C01/02/03/05/06). 25C04·25C07·25C08 과 35 °C·45 °C 전부 제외 |

---

# 서지 (PDF 에서 직접 재확인)

`[인쇄, p.1]`

- 제목: *Modeling and health feature extraction method for lithium-ion
  batteries state of health estimation by distribution of relaxation times*
- 저자: Zhipeng Su, **Jidong Lai\*** (교신), Jianhui Su, Chenguang Zhou,
  Yong Shi, Bao Xie
- 소속: School of Electrical and Automation Engineering, Hefei University of
  Technology, Hefei 230009, China / Research Center for Photovoltaic System
  Engineering of Ministry of Education (Hefei University of Technology)
- 교신 이메일: 2013800004@hfut.edu.cn
- 저널: *Journal of Energy Storage* **90** (2024) **111770**, Research Papers
- DOI: **https://doi.org/10.1016/j.est.2024.111770**
- 투고 이력: **Received 4 December 2023 · Revised 26 February 2024 ·
  Accepted 17 April 2024 · Available online 4 May 2024**
- ISSN 2352-152X, © 2024 Elsevier Ltd.
- Keywords: Lithium-ion batteries · State of health · Electrochemical
  impedance spectroscopy · Distribution of relaxation times · Health
  features · Regression model
- 자금: The University Synergy Innovation Program of Anhui Province
  [GXXT-2021-025]
- 참고문헌 54편, 본문 그림 12 + 표 4

**초록의 수치** `[인쇄, p.1]`: "the EIS fitting accuracy R² of the developed
model is the best and the **RMSE of SOH estimation is within 0.873 %**".

`[해석]` "within 0.873 %" 는 **평균**이지 상한이 아니다. Table 4 에서 cell5 의
Feature1 RMSE 는 **1.607 %** 다. 초록의 "within" 은 과장이다.

---

# §1 Introduction — 이 논문이 스스로 세운 문제

`[인쇄, p.1–2]` 논지 사슬:

1. SOH 추정은 (i) 모델 기반, (ii) 데이터 기반 둘로 나뉜다. EIS 기반은 열화
   기구를 식별하는 수단으로 주목받는다 [12–17].
2. **기존 ECM 의 병**: Nyquist 의 반원들이 겹쳐 유한차수/분수차수 ECM 이 잘
   맞지 않고, ECM 구조 선택이 경험 의존이라 **사전 가정(a priori assumption)**
   문제가 생긴다. Shu et al. [19] 은 2–3개 RC 로 충분하다 하고, Jiang et al.
   [20] 은 SEI(R1//CPE1)·전하전달(R2//CPE2)·확산(W) 의 ECM 을 세워 GPR 로
   SOH 를 추정한다.
3. **DRT 의 약속**: 서로 다른 전기화학 과정이 서로 다른 완화시간에 대응하므로,
   DRT 는 사전 가정 없이 반응들을 분리한다 [21–24].
4. **DRT 자신의 병 (저자가 명시)** `[인쇄, p.2]`: "because distribution
   sharpness/smoothness is an unreliable indicator for the existence or
   absence of peaks (discrete relaxations), **continuous DRT estimates are
   prone to producing false peaks or omitting true relaxation processes**
   [27]." 그리고 "If the non-relaxation process is considered as the true
   relaxation process, although it may still end up with a better EIS fit,
   **it is spurious by nature** and will eventually affect the feature
   extraction of the true relaxation process."
5. 따라서 **parsimony 원칙** [27,28] 으로 역문제의 모호성을 다뤄야 한다.
6. feature 는 자동추출(ML)과 수동추출로 나뉘고, 자동추출은 "**열화 기구를
   설명하기 어렵다**"는 문제가 있어 이 논문은 수동추출을 택한다.
7. feature 분류 3종 [33]: (i) **모델 fitted feature**(저항·커패시턴스),
   (ii) **가공된 외부 feature**(IC/DV, 특정 주파수 임피던스),
   (iii) **직접 외부 feature**(단자전압·전류·온도).

`[해석]` **4번이 이 논문의 가장 정직한 대목이자 우리에게 가장 유용한 문장이다.**
저자 스스로 "DRT 는 가짜 peak 을 만들거나 진짜 완화를 빠뜨리기 쉽다"고
인쇄했다. 그런데 논문의 나머지는 그 DRT peak 을 SEI/전하전달/확산에
**이름 붙여** 물리 해석을 얹는다. 두 태도가 같은 논문 안에 공존한다.
SEV 처럼 DRT peak 을 특정 전극의 R_ct 에 귀속시키는 설계는 이 인쇄된 경고를
반드시 통과해야 한다.

`[해석]` **6번의 아이러니**: "ML 자동추출은 열화 기구 설명이 어렵다"를 이유로
수동추출을 택했으나, 이 논문의 최종 입력은 8개 feature 를 **WPCA 로 1차원으로
뭉갠 IHF** 다. 뭉개고 나면 물리 해석 가능성은 자동추출과 다를 바 없다 —
저자는 이 자기모순을 언급하지 않는다.

---

# §2.1 데이터셋 ★ (②의 답)

**원문 전문** `[인쇄, p.3]`:

> "It is common practice to evaluate SOH estimation techniques using EIS data
> from public datasets. **12 LiCoO2/graphite aging data with a 45mAh capacity
> are include in the dataset supplied in [32]** at three different
> temperatures: 25 °C (25C01-25C08), 35 °C (35C01-35C02), and 45 °C
> (45C01-45C02). **Nine different states form a charge-discharge cycle are
> chosen for the EIS test, with a sine wave current of 5 mA and 60 different
> frequencies chosen from a range of 0.02 Hz–20 kHz.**
>
> The EIS data at **25 °C and 100 %SOC (State V, after 15-min rest)** are the
> main focuses of our case. Taking into account the variability and aging
> trend of these cells, we ignored those batteries in the dataset that had
> less cycle counts and focused more on those that are relatively abundant of
> counts. The impedance spectra of **25C01, 25C02, 25C03, 25C05 and 25C06**
> recorded at different aging statuses will be used in the following model
> training and verification... referred as cell1, cell2, cell3, cell5 and
> cell6..."

**Data availability 절 전문** `[인쇄, p.14]`:

> "We used an **open dataset** at doi:**https://doi.org/10.5281/zenodo.3633835**,
> reference number [32]."

**참조 [32] 전문** `[인쇄, p.15]`:

> "[32] Y. Zhang, Q. Tang, Y. Zhang, J. Wang, U. Stimming, A.A. Lee,
> **Identifying degradation patterns of lithium ion batteries from impedance
> spectroscopy using machine learning**. Nature, Communications (2020) 11,
> https://doi.org/10.1038/s41467-020-15235-7."

## ② 판정

**저자들은 아무것도 측정하지 않았다.** 이 논문은 순수 재분석(secondary
analysis)이다. 근거는 세 겹으로 독립적이다:

1. §2.1 이 "public datasets" · "the dataset supplied in [32]" 라고 명시.
2. Data availability 가 "We used an **open dataset**" + Zenodo DOI 를 명시.
3. CRediT 저자기여 `[인쇄, p.14]` 에 **Yong Shi: Methodology, Data curation**
   은 있으나 **Investigation/실험 수행에 해당하는 측정 기여가 없다**
   (Jidong Lai: Writing–review & editing, Resources, Project administration,
   Investigation, Conceptualization — Investigation 은 있으나 §2.1·Data
   availability 와 합치면 실측이 아니라 데이터 조사로 읽는 것이 정합적이다).
   `[해석]` 3번은 보조 근거이고, 1·2번만으로 판정이 선다.

**원 출처 (이제부터 이렇게 인용한다)**:

> Y. Zhang, Q. Tang, Y. Zhang, J. Wang, U. Stimming, A. A. Lee,
> *Identifying degradation patterns of lithium ion batteries from impedance
> spectroscopy using machine learning*, **Nature Communications 11** (2020),
> DOI 10.1038/s41467-020-15235-7. 데이터: **Zenodo 10.5281/zenodo.3633835**.

## 우리 실측(`mode-observability/manifests/README.md`)과의 대조표

| 우리가 파일에서 잰 것 | Su §2.1 이 인쇄한 것 | 판정 |
|---|---|---|
| 주파수 범위 0.02 Hz ~ 20 kHz | "0.02 Hz–20 kHz" | **일치** |
| EIS 파일당 4,920행 / 82 스펙트럼 → 스펙트럼당 60점 | "**60** different frequencies" | **일치** (4920 = 60 × 82) |
| Capacity 파일 전류 45.00 mA | "**45 mAh** capacity" (→ 1C = 45 mA) | **일치** |
| 온도 25 / 35 / 45 °C | "25 °C, 35 °C, 45 °C" | **일치** |
| 파일명 `EIS_state_{I..IX}_...` | "**Nine** different states ... chosen for the EIS test" | **일치** — state I~IX = **한 충방전 사이클 안의 아홉 측정 시점**. 열화 단계도 SOH 등급도 아니다 |
| — | "State **V** = 100 %SOC, after 15-min rest" | state V 만 SOC/시점이 확정. 나머지 8개는 **n/a** |
| 셀 번호 `01..08` (온도 3종 모두?) | 25 °C 는 **01–08(8셀)**, 35 °C 는 **01–02(2셀)**, 45 °C 는 **01–02(2셀)** = **12셀** | **미확인 — 확인 필요.** Su 의 열거대로면 `35C03`~`35C08`·`45C03`~`45C08` 은 **존재하지 않아야 한다.** manifests 의 파일명 패턴이 실제 열거인지 축약 표기인지 확인할 것 |
| 진폭 (우리 실측 없음) | 정현파 **전류 5 mA** (= 45 mAh 셀 기준 **C/9**) | Su 만의 정보 |
| 파일 176개 | 12셀 × 9 state = 108 EIS + 용량 12 = **120** | **미확인** — 176 과 맞지 않는다. `__MACOSX` 그림자 파일·추가 파일 여부 확인 필요 |
| `EIS_state_VI_25C42.txt` (셀번호 42) | 25 °C 는 01–08 뿐 | **원문에 근거 없음.** Su 의 열거로는 `25C42` 가 설명되지 않는다 — 원 데이터셋(Zenodo)에서 확인할 항목 |
| 헤더 있는 파일 / 없는 파일 혼재 | (언급 없음) | **n/a** — Su 는 파일 포맷을 다루지 않는다 |
| zip 타임스탬프 2019-12 ~ 2020-02 | — | `[해석]` Zhang 2020 (Nat. Commun., 2020-03 게재)의 원 측정 시기와 정합적이다. Su(2023-12 투고)가 잰 것이라면 나올 수 없는 날짜다 — **② 판정의 독립 확인**이 된다 |

`[해석]` **Phase 2 설계에 직결되는 결론 하나**: `state` 는 **SOC/측정 시점**
축이지 열화 축이 아니다. 열화 축은 **파일 안의 `cycle number` 열**이다.
따라서 SEV 실측 대조를 하려면 (a) state 를 고정하고 cycle 을 훑거나
(b) 특정 cycle 에서 state I~IX 를 훑어 SOC 의존성을 보는, 두 개의 서로 다른
스윕이 가능하다. Su 는 (a) 중에서도 **state V 하나만** 썼다 — state 축은
**아무도 쓰지 않은 여유 차원**이며, SEV 가 stoichiometry 의존성을 읽는
feature 라는 점에서 **(b) 쪽이 우리에게 더 값어치 있을 가능성이 있다**.

---

# §2.2–2.3 developed DRT-based impedance model

## 모델 구조 `[인쇄, p.4, Fig. 2(a)]`

직렬로: **고주파 인덕턴스 L → 옴저항 R_∞ → {R₁//C₁, R₂//C₂, …, Rₙ//Cₙ}
(무한급수, DRT) → CPE**.

전체 임피던스 (식 5):

```
Z(f) = j2πfL + R_∞ + ∫ γ(ln τ) / (1 + j2πfτ) d(ln τ) + 1/(Q (j2πf)^(−α))
```

- 식 (1)–(3): 표준 DRT. γ(ln τ) = τ·g(τ), ∫g(τ)dτ = R_pol.
- 식 (4): CPE, `Z_CPE(ω) = 1/(Q(jω)^(−α))`, α ∈ [0,1].
- L 도입 근거 `[인쇄]`: 선로 인덕턴스·셀 중간체·촉매 등 비이상성 [44].
- CPE 도입 근거 `[인쇄]`: 저주파 Warburg 가 노화·편차 때문에 경험적 π/4
  에서 벗어나므로 CPE 로 보정 [47].

## split-frequency domain 계산 (이 논문의 방법론적 핵심)

`[인쇄, p.5]` 문제의식: L 과 CPE 를 DRT 정규화 알고리즘 안에 함께 넣으면
계산량이 폭증하고 **비수렴** 가능성이 있다. 그래서 주파수대를 나눠 **먼저
비분극 성분을 빼고** 나머지로만 γ(ln τ) 를 푼다.

- **HEIS (고주파)**: 커패시터·CPE 임피던스 ≈ 0 → `Z(f) ≈ j2πfL + R_∞`.
  **최고주파 5점**으로 (식 7):
  `R_∞ ≈ (1/5)Σ Z'ₙ`, `L ≈ (1/10π)Σ Z''ₙ/fₙ`.
- **LEIS (저주파)**: L ≈ 0, R//C 병렬 ≈ R_pol →
  `Z(f) ≈ R_∞ + R_pol + (1/(Q(2πf)^α))·[cos(απ/2) − j·sin(απ/2)]` (식 8).
  → `−Z''(f) = tan(απ/2)·Z'(f) − (R_∞+R_pol)·tan(απ/2)` (식 9): **Nyquist
  저주파 직선의 기울기 k 와 절편 a** 를 선형회귀로 얻어
  `α = 2·tan⁻¹(k)/π`, `R_pol = −a/k − R_∞` (식 10).
- **Table 1 (5단계)**: ① 고→저 주파수로 훑다가 인접 두 점의 기울기가
  k₀(= **0.5** 로 설정)를 넘는 첫 점을 LEIS 상한 f_set 으로 잡는다 →
  ② 구간 [f_set, f_m] 을 `−Z'' = a + kZ'` 로 선형 fitting → ③ α, R_pol
  계산 → ④ |Z_CPE(f)| = √(Z''² + (Z'−a)²) → ⑤ 선형 fitting 으로 Q.
- **③ 잔차 DRT**: 측정 임피던스에서 L·R_∞·CPE 를 뺀 나머지로 γ(ln τ) fitting.

## DRT 수치 설정 `[인쇄, p.6]` ★ (⑤의 답 일부)

> "The DRT algorithm of this paper is implemented with MATLAB's open source
> **DRTtools** [51]. Based on a large number of tests and relevant literature,
> we finally set the initial parameters for DRT calculation, we set
> **Data Used as "Combined Re-Im Data"**, **Inductance included as "Fitting
> without Inductance"**, **Regularization Parameter as "1E-3"**, and other
> parameters are set by default."

- [51] = Wan, Saccoccio, Chen, Ciucci, *Electrochim. Acta* 184 (2015) 483 —
  radial basis function 이산화 기반 DRTtools.
- 정규화: **Tikhonov (DRTtools 기본)**, λ = **1E-3**.
- **λ 선택 근거**: "based on a large number of tests and relevant literature"
  → **원리적 기준 없음**. GCV·L-curve·discrepancy·Bayesian 어느 것도 언급 없음.
- 나머지(RBF 종류·shape factor·형상 계수) 는 "default" 로만 적혀 있어
  **재현에 필요한 정보가 부족**하다.
- **Inductance 를 DRT 단계에서 끄는 것**은 이 논문 설계상 일관적이다
  (L 은 이미 HEIS 에서 빼냈다).

`[해석]` **이것이 이 논문의 진짜 기여이자 진짜 위험이다.** 저주파 CPE 를
DRT 이전에 빼내면 Fig. 4 처럼 τ ≳ 1 s 의 거대 가짜 peak 이 사라진다. 그러나
빼내는 방식이 **직선 fitting 의 기울기·절편**이므로, LEIS 직선이 실제로
CPE 하나로 설명되지 않으면 **진짜 저주파 완화까지 함께 빠져나간다** — 저자가
§1 에서 스스로 경고한 "omitting true relaxation processes" 의 정확한 형태다.
논문은 이 방향의 오류(과잉 제거)를 **한 번도 검사하지 않는다**. 검사한 것은
반대 방향(가짜 peak 제거)뿐이다.

---

# §2.4 DRT peak 의 물리 귀속과 노화 추세 ★ (①의 답)

## 귀속의 선언 `[인쇄, p.6]`

> "From Fig. 5, **three polarization processes** can be clearly represented in
> the form of peaks, which are named **p₁, p₂, p₃ from low to high of
> relaxation times**. It essentially describes **the thickness of the SEI
> film, the charge transfer processes and diffusion processes**."

→ 순서대로 **p₁ = SEI 막 두께**, **p₂ = 전하전달**, **p₃ = 확산**.

`[해석]` **귀속의 근거가 하나도 제시되지 않는다.** 대칭셀도, 기준전극도,
half-cell 도, 온도 스윕(활성화에너지)도, SOC 스윕도 없다. "낮은 τ 부터 SEI,
전하전달, 확산" 이라는 **관례적 순서를 그대로 선언**한 것이다.

`[해석, 계산]` τ ↔ f 환산 (`f = 1/(2πτ)`) 을 하면 Fig. 5 에서 읽은 위치는
대략 **p₁ ≈ 5×10⁻⁵ s → 3 kHz**, **p₂ ≈ 1–3×10⁻³ s → 50–160 Hz**,
**p₃ ≈ 1–3×10⁻² s → 5–16 Hz** 다. **p₃ 를 "확산" 이라 부르는 것은 무리한
귀속이다** — 코인셀 규모에서 5–16 Hz 대역은 통상 **전하전달 arc** 로 읽히고,
확산(Warburg)은 훨씬 낮은 주파수에 있다. 게다가 이 논문은 저주파 성분을
CPE 로 **이미 빼냈다**. 즉 **남은 γ(ln τ) 안에 확산이 있을 이유가 구조적으로
없다.** 이 재해석이 옳다면 ①의 함의가 뒤집힌다 (아래 "①의 최종 판정" 참조).

## 노화 추세의 진술 (문제의 문장) `[인쇄, p.6]`

> "With the battery aging, further analysis of p₁, p₂ and p₃ is shown as
> follows: **Except for cell1, the value of p₁ and p₂ for the other cells
> tends to decrease. On the other hand, the value of p₃ shows an increasing
> trend with aging. These trends are in line with the fact that the loss of
> stock (LLI) and loss of active material (LAM) in the electrode makes the
> charge transfer process more difficult with the battery aging [20].**
> Therefore, we can assume that the curves are regular and reliable with LIB
> aging..."

**두 번째 언급** `[인쇄, p.8, §3.2]`:

> "Fig. 8 shows that the HFs can keep the same trend of increase or decrease
> with aging in every battery, but their values and rates of change are
> distinctly different. **This further illustrates that as batteries aging,
> the loss of stock and loss of active material in the electrode are regularly
> variable**, but differences in the consistency of the cells result in
> differences in their impedance model parameters."

**세 번째 언급** `[인쇄, p.14, §5 결론]`:

> "Since the high sensitivity of EIS to the polarization process, in practical
> applications, the developed DRT-based impedance model **contributes to our
> understanding of loss of cyclable and loss of active materials lead to the
> battery capacity fade**."

`[해석]` 세 언급이 전부다. 본문 전체에서 `LLI`·`LAM` 이 등장하는 곳은 위
세 곳 + 서론 1회(`[인쇄, p.2]` "both loss of cyclable and loss of active
materials lead to the battery capacity fade") = **네 곳**이며, **어느 곳에도
LLI/LAM 의 수치가 없다.** 이 논문은 열화 모드를 재는 논문이 아니다.

## ①의 최종 판정

**(a) 출처.** 문제의 문장에 붙은 인용은 **[20] = B. Jiang, J. Zhu, X. Wang,
X. Wei, W. Shang, H. Dai, "A comparative study of different features extracted
from electrochemical impedance spectroscopy in state of health estimation for
lithium-ion batteries", *Appl. Energy* 322 (2022) 119502** 다. 즉 **"LLI 와
LAM 이 전하전달을 어렵게 한다"의 원전은 Su 2024 가 아니라 Jiang 2022** 이며,
Su 는 그것을 **자기 추세의 해석 틀로 빌려 온** 것이다.

**(b) 증거 등급: 인용 상속(3차). 실측 아님.** Su 는 LLI·LAM 을 재지 않았고,
전극별로 나누지도 않았으며, 모드를 조작한 실험도 시뮬레이션도 하지 않았다.
"in line with the fact that…" 이라는 문장 구조 자체가 **측정 결과 보고가 아니라
정합성 주장**이다.

**(c) 자체 데이터에 의한 부분 반박.** Su 자신이 "charge transfer" 로 이름 붙인
peak 은 **p₂** 인데, 그 값이 **노화와 함께 감소**한다(cell1 제외 4셀).
"전하전달이 어려워진다" 는 서술과 **부호가 반대**다. Fig. 7 이 이것을 수치로
확인해 준다 (γ(lnτ_p₂) 의 SOH 상관이 4셀에서 **양수** = SOH 가 떨어지면 값도
떨어진다). 문장이 성립하려면 "전하전달" 은 p₂ 가 아니라 **p₃** 여야 하는데,
p₃ 는 저자가 "확산" 이라고 이름 붙인 것이다. **논문 내부에서 어긋난다.**

**(d) 그러므로 Wang 2025 리뷰의 요약은?** 문면상으로는 충실하다 — Su 의 문장을
크게 왜곡하지 않았다. 그러나 **두 가지를 잃었다**:
- Su 가 그 진술을 **[20] 에서 빌려 왔다**는 사실 (리뷰는 "Su et al. …
  **observed**" 라고 써서 **Su 의 관찰**로 격상시킨다).
- Su 가 **LLI/LAM 을 재지 않았다**는 사실 (리뷰는 그 문장을 §4.4 의
  "interpretable feature 의 물리 귀속" 열에 넣어 근거처럼 배치한다).

→ **[[pvs-sev-lli-lampe-separability]] 의 Evidence For 항목은 인용 등급을
내려야 한다.** "문헌에 인쇄된 관찰" 이 아니라 "**리뷰가 한 단계 격상시켜 옮긴,
원전에서는 상속된 해석 한 문장**" 이다.

**(e) 그러나 SEV 에 대한 이 논문의 실제 함의는 더 나쁘다** — 아래 §3.2 참조.

---

# §3.1 feature 추출 (17개)

`[인쇄, p.7]` 3군으로 분류:

- **Group 1 — 비분극 과정 파라미터** (4): 옴저항 **R_∞**, 고주파 인덕턴스
  **L**, CPE 상수 **Q**, CPE 지수 **α**.
- **Group 2 — 분극 과정 파라미터** (1): 분극저항 **R_pol**.
- **Group 3 — γ(ln τ) 곡선 파라미터** (12): p₃ 의 완화시간 **ln τ_p₃**,
  peak 높이 **γ(lnτ_p₁), γ(lnτ_p₂), γ(lnτ_p₃)**, 골 높이
  **γ(lnτ_v₁), γ(lnτ_v₂)**, 상대비 **ratio_p₁, ratio_p₂, ratio_p₃**,
  반peak 면적 **S₁, S₂, S₃**.

정의 (식 12–14):

```
ratio_pi = γ(ln τ_pi) / Σ_{i=1..3} γ(ln τ_pi)
S_i = ∫_{flex_up_pi}^{flex_down_pi} γ(ln τ) d ln τ
flex_up_pi = (1/K) Σ_k flex_up_pi,k       (K = 학습 표본 수)
```

`[인쇄]` S_i 의 적분 구간은 **학습 표본 전체에 걸친 변곡점의 평균**으로
고정한다 — "In order to reduce the error from the different integration
intervals". 근거 `[인쇄, p.7]`: "From Eq. (2), the integration of γ(ln τ) can
reflect the **resistance of the polarization process at that peak**."

`[해석]` **S_i 가 물리적으로 가장 방어 가능한 feature 다** (∫γ d lnτ = 저항).
peak **높이** γ(lnτ_p) 는 저항이 아니라 저항밀도이고 peak 폭에 오염된다.
`ratio` 는 세 peak 높이의 상대비라 **더 멀다**. 그런데 최종 선택된 8개 중
**ratio 가 3개**로 최대 비중이다.

`[인쇄, p.6]` **p₁.₅ 의 처리**: cell2·cell3·cell6 에서 p₁ 과 p₂ 사이
(τ ∈ 10⁻⁴~10⁻³ s) 에 작은 peak 이 나타나지만 노화와 함께 사라지므로 "p₂ 의
분극 과정 일부" 로 보고 **연구에서 제외**한다. cell1·cell5 에는 없다.

`[해석]` **이것은 §1 이 경고한 "false peak vs true relaxation" 판정을 눈으로
하고 있는 것이다.** p₁.₅ 를 버리는 기준은 "노화하면 사라지니까" 인데, 그것은
**진짜 완화가 사라지는 경우**와 구분되지 않는다. 그리고 그 결과로 S₂ 의 적분
구간(변곡점 위치)이 셀마다 다른 것을 뭉개게 된다.

---

# §3.2 상관분석 ★ (Fig. 7 — 이번 흡수에서 가장 값어치 있는 그림)

`[인쇄, p.8]` 방법: Pearson corr(ρ) 와 Spearman corr(r) 을 SOH(= 용량비,
식 15) 에 대해 계산. **절대값**을 취해 부호를 무시하고, **문턱 0.75 를 5셀
모두에서** 넘는 feature 만 남긴다.

`[도표]` **Fig. 7 을 실제로 보고 읽은 Pearson 계수 전표** (17 feature × 5 cell,
그림에 인쇄된 숫자를 그대로 옮김):

| feature | cell1 | cell2 | cell3 | cell5 | cell6 | 채택 |
|---|---|---|---|---|---|---|
| R_∞ | −0.1175 | −0.859 | −0.8612 | −0.9866 | −0.9703 | ✗ |
| L | 0.3424 | 0.9306 | 0.8501 | 0.4269 | 0.8671 | ✗ |
| **Q** | −0.857 | −0.8566 | −0.8234 | −0.8387 | −0.7541 | **✓** |
| α | −0.04165 | 0.7436 | 0.7583 | 0.1409 | 0.4586 | ✗ |
| **R_pol** | **−0.9651** | **+0.8637** | **−0.3969** | **−0.9177** | **+0.854** | ✗ |
| **ln τ_p₃** | −0.9726 | −0.9654 | −0.8589 | −0.9456 | −0.9199 | **✓** |
| γ(lnτ_p₁) | 0.4717 | 0.8618 | 0.8455 | 0.8063 | 0.8578 | ✗ |
| **γ(lnτ_p₂)** | **−0.6874** | **+0.9341** | **+0.8437** | **+0.751** | **+0.8691** | ✗ |
| **γ(lnτ_p₃)** | −0.9818 | −0.9124 | −0.8493 | −0.9452 | −0.9112 | **✓** |
| γ(lnτ_v₁) | 0.5722 | 0.7671 | 0.6095 | 0.5171 | 0.6341 | ✗ |
| **γ(lnτ_v₂)** | 0.8129 | 0.9457 | 0.8686 | 0.8527 | 0.9097 | **✓** |
| **ratio_p₁** | 0.963 | 0.8857 | 0.8816 | 0.9478 | 0.88 | **✓** |
| **ratio_p₂** | 0.9391 | 0.936 | 0.8539 | 0.9211 | 0.9101 | **✓** |
| **ratio_p₃** | −0.9717 | −0.9387 | −0.8715 | −0.9553 | −0.9138 | **✓** |
| S₁ | 0.1886 | 0.9339 | 0.8533 | 0.7957 | 0.8739 | ✗ |
| S₂ | −0.5251 | 0.9305 | 0.8518 | 0.8218 | 0.9065 | ✗ |
| **S₃** | −0.9774 | −0.9604 | −0.8825 | −0.9787 | −0.9252 | **✓** |

(Spearman 표는 Fig. 7(b) 에 있고 부호·채택 결론이 같다. 대표적으로
γ(lnτ_p₂): cell1 **−0.6963** / cell2 +0.963 / cell3 +0.9728 / cell5 +0.7893 /
cell6 +0.9491, R_pol: cell1 −0.9793 / cell2 **+0.8955** / cell3 **−0.3726** /
cell5 −0.909 / cell6 **+0.957**.)

**채택된 8개** `[인쇄]`: **Q, ln τ_p₃, γ(lnτ_p₃), γ(lnτ_v₂), ratio_p₁,
ratio_p₂, ratio_p₃, S₃** (Fig. 7 에서 빨간 글씨로 표시된 열과 일치 —
그림과 본문이 **합치한다**).

## ★ 이 표에서 읽히는 것 (논문이 말하지 않는 것)

`[해석]` **1. 전하전달 feature 는 부호가 뒤집힌다.** γ(lnτ_p₂) 는 cell1 에서
**−0.687**, 나머지 4셀에서 **+0.75 ~ +0.93** 이다. 양수 = "SOH 가 내려가면
전하전달 peak 도 내려간다". 부호가 셀에 따라 뒤집힌다는 것은 **동일 사양·동일
온도·동일 프로토콜의 5셀 사이에서도 그 feature 의 노화 방향이 정해지지
않는다**는 뜻이다.

`[해석]` **2. 분극저항 R_pol 은 더 심하다.** cell1 −0.965, cell5 −0.918 (SOH↓
→ R_pol↑) 인데 cell2 +0.864, cell6 +0.854 (SOH↓ → R_pol**↓**) 이고 cell3 은
−0.397 로 거의 무상관이다. **"노화하면 분극저항이 오른다" 는 통념이 5셀 중
2셀에서 반대로 나온다.** 논문은 이 사실을 지적하지 않고, R_pol 을 문턱
미달로 조용히 버린다.

`[해석]` **3. 저자의 "절대값 처리" 가 이 사실을 숨긴다.** §3.2 `[인쇄]`:
"Because the results' assessment of the degree of connection is unaffected by
features' correlation coefficients' positivity or negativity. We perform
**absolute value processing** for all feature correlation coefficients,
**focusing on correlation and ignoring positive and negative correlation**."
→ 부호를 버리면 "부호가 셀마다 뒤집힌다" 는 진단이 원리적으로 불가능해진다.
채택된 8개는 다행히 5셀 모두에서 부호가 같지만, **그것은 절차가 보장한 것이
아니라 우연히 그렇게 된 것**이다. 절차 자체는 부호가 뒤집히는 feature 도
|corr| 만 높으면 통과시킨다.

`[해석]` **4. 우리 축에 대한 함의 — 이것이 이 논문이 SEV 에 주는 진짜 증거다.**
①("LLI 와 LAM 이 같은 방향으로 R_ct 를 민다")은 상속된 문장이라 무게가 없다.
대신 이 표는 **모드를 논하기 이전 단계의 문제**를 준다:

> 실측 셀에서 **전하전달 유래 임피던스 feature 의 노화 부호가 셀 간에 안정하지
> 않다.** 5셀 중 1셀에서 뒤집히고, 그 상위 집계량인 R_pol 은 2셀에서 뒤집힌다.

SEV 는 R_ct,PE 의 **부호 구조**(LLI↑, LAM_PE↑, LAM_NE↓)를 읽어 모드를 가르려
한다. 부호 구조를 쓰는 feature 는 **부호가 셀 간에 안정할 때만** 작동한다.
이 논문은 그 전제가 실측에서 성립하지 않는 사례를 준다. 이것은 H1/H2 어느
쪽 편도 아니고, **두 가설이 다투는 무대(= SEV 가 재현 가능한 축인가) 자체에
대한 경고**다.

---

# §3.3 WPCA — 가중 주성분분석

`[인쇄, p.9]` 절차: ① 8개 HF 를 m×n 행렬로 → ② Z-score 정규화 →
③ **가중치 β_i** 곱 → ④ 공분산 행렬 → ⑤ 주성분.

가중치 (식 17):

```
β_i = (2/π)·arctan[  tan(π|corr(ρ_i)|/2) / Δtan(π|corr(ρ)|/2)
                   + tan(π|corr(r_i)|/2) / Δtan(π|corr(r)|/2) ]
```

여기서 Δ(·) 는 최대−최소.

`[인쇄]` 설계 의도: tan(π·|corr|/2) 가 [0,1] 을 [0,∞] 로 늘려, |corr| → 1 인
feature 에 가중치가 몰리게 한다.

`[해석]` **이 식은 수치적으로 불안정하다.** |corr| → 1 이면 tan → ∞ 이고,
분모 Δtan 도 함께 발산한다 (저자가 `[인쇄]` "which often close to infinity"
라고 스스로 적는다). ∞/∞ 형태를 유한하게 만드는 것은 순전히 유한 정밀도
산술이며, 이 표의 몇몇 값(예: Spearman |corr| = 0.9986, 0.9964)은 tan(π·0.9986/2)
≈ 455 수준이라 **하나의 feature 가 β 를 지배**한다. 물리적 근거가 아니라
**함수 형태가 만든 가중치**다. 저자는 β_i 의 실제 수치를 **한 번도 인쇄하지
않는다** → 재현 불가.

`[인쇄, Table 2]` 첫 주성분의 누적기여율: cell1 **98.3420 %**, cell2 97.7370 %,
cell3 97.2083 %, cell5 **96.7462 %**, cell6 96.7894 % → 전부 96.7 % 초과이므로
**F₁ 하나(1차원)** 를 IHF 로 쓴다.

`[해석]` 8개 feature 의 96.7 % 이상이 **한 방향**에 실린다는 것은 그 8개가
사실상 **하나의 잠재변수(= SOH 자신)** 의 사본이라는 뜻이다. 논문은 이것을
"차원 축소가 잘 됐다" 로 읽지만, 같은 사실이 "**8개 feature 는 독립 정보를
7개만큼 더 주지 않는다**" 로도 읽힌다. 우리 관심(= 서로 다른 모드를 가르는
독립 방향이 몇 개인가)에서는 **후자가 요점**이다.

---

# §4 결과

## 4.1 성능 지표와 실험 설계 `[인쇄, p.10]`

- 지표: **R², MaxAE, RMSE** (식 22). **MaxAE 는 초기 5 사이클을 제외**한다
  ("in the hope of observing a MaxAE that is more representative of the full
  life cycle characteristics").
- 계산 환경: Intel 13400F, RTX 3060, MATLAB R2023a. ECM 파라미터 계산 시간은
  **제외**.
- **데이터 분할** `[인쇄]`: "this study **randomly disrupts the data for each
  battery and randomly selects 40 % of the data as training dataset and the
  remaining 60 % as test dataset**."

`[해석]` **이것이 이 논문 성능수치의 가장 큰 약점이다.** 한 셀 안에서 사이클을
무작위로 섞어 40/60 으로 나누면, 테스트 표본의 바로 앞뒤 사이클이 학습에
들어간다. EIS·용량 모두 사이클에 대해 매끄러우므로 이 설정의 GPR 은 사실상
**보간(interpolation)** 을 하고 있고, RMSE 0.873 % 는 "새 셀을 얼마나
예측하는가" 와 무관하다. **저자들이 이것을 스스로 인정한다** `[인쇄, p.14]`:

> "there are still some limitations, such as when dividing the dataset into
> training and test sets, **instead of splitting the dataset into training
> datasets from one or more batteries and testing datasets from other
> batteries**, we randomly disrupt the data for each battery and randomly
> selects 40 % of the data as training dataset... **This is due to the
> significant difference in battery consistency**, not only in terms of
> initial capacity and decay, but also in the EIS."

`[해석]` 즉 **cross-cell 로 나누면 안 되는 것이 아니라, 나누면 성능이 안
나온다**는 고백이다. Fig. 8 이 그 이유를 그림으로 보여 준다 (아래).

## 4.2 모델 비교 `[인쇄, p.11, Table 3]`

비교 대상: **ECM1** = 이 논문 모델, **ECM2** = R0(R1//C1)(R2//C2),
**ECM3** = R0(R1//C1)(R2//C2)W, **ECM4** = R0(R1//CPE1)(R2//CPE2)W.
ECM2–4 는 비선형 최소자승(SciPy [53]) 으로 fitting. cell1 의 3개 SOH 상태
(100 % / 85 % / EOL) 평균:

| | ECM1 RMSE / R² | ECM2 | ECM3 | ECM4 |
|---|---|---|---|---|
| **Re(Z)** | **0.441 % / 99.991 %** | 6.030 % / 98.079 % | 1.717 % / 99.845 % | 1.157 % / 99.930 % |
| **−Im(Z)** | **5.303 % / 94.385 %** | 7.757 % / 84.876 % | 5.628 % / 90.797 % | 5.468 % / 92.024 % |

`[해석]` **본문·초록·결론이 인용하는 "R² 99.994 %" 는 평균이 아니라
100 % SOH 상태 하나의 값이다** (Table 3 의 평균은 **99.991 %**). 세 곳 모두
99.994 를 쓴다 — 사소하지만 최선값을 대표값으로 쓰는 습관이다.

`[해석]` **비교가 불공정하다.** ECM1 은 사실상 **무한 차수**(DRT 는 임의 개수의
RC 를 허용) 이고 ECM2–4 는 2차다. 파라미터 수가 압도적으로 다른 모델의
fitting RMSE 를 비교해 "우리 모델이 낫다" 고 하는 것은 자명한 결과다. AIC/BIC
같은 **복잡도 벌점**도, 교차검증도 없다. 저자가 §1 에서 인용한 parsimony 원칙
[27,28] 이 정작 이 비교에는 적용되지 않았다.

`[해석]` 허수부 R² 가 **94 % 에 그친다** — 실수부 99.99 % 와 대조적이다.
Nyquist 에서 −Im 은 분극 과정을 담는 축이므로, **분극 쪽 재현이 가장 나쁜
모델로 분극 유래 feature 를 뽑고 있다**. 논문은 이 긴장을 언급하지 않는다.

## 4.3–4.4 SOH 추정 `[인쇄, p.11–12, Table 4]`

GPR: MATLAB `fitrgp()`, **zero mean + Matérn 3/2 kernel**.

4개 입력 전략:
- **Feature1** = 이 논문의 IHF (**1-D**)
- **Feature2** = 전체 임피던스 스펙트럼 (**120-D** = 60주파수 × Re/Im), 출처 [32]
- **Feature3** = 8개 HF 원본 (**8-D**)
- **Feature4** = 8개 HF 를 **일반 PCA** 로 축소 (**1-D**)

**5셀 평균**:

| | R² (%) | **RMSE (%)** | MaxAE | Train (s) | Test (s) | **Total (s)** |
|---|---|---|---|---|---|---|
| Feature1 (IHF, 1-D) | 98.446 | **0.873** | 0.0222 | 0.2287 | 0.0071 | **0.2358** |
| **Feature2 (raw EIS, 120-D)** | **99.362** | **0.573** | **0.0135** | 0.2722 | 0.0076 | 0.2798 |
| Feature3 (8 HF, 8-D) | 99.062 | 0.672 | 0.0150 | 0.2435 | 0.0074 | 0.2509 |
| Feature4 (PCA, 1-D) | 98.216 | 0.946 | 0.0228 | 0.2401 | 0.0071 | 0.2472 |

셀별 Feature1 RMSE `[인쇄]`: cell1 0.727 / cell2 **0.512** / cell3 0.655 /
cell5 **1.607** / cell6 0.865.

`[해석]` ★ **제안 방법이 정확도에서 진다.** 원시 스펙트럼을 그냥 넣은
Feature2 가 **모든 지표에서** Feature1 을 이긴다 (RMSE 0.573 vs 0.873,
R² 99.362 vs 98.446, MaxAE 0.0135 vs 0.0222). 심지어 축소 안 한 8-D
Feature3 도 Feature1 을 이긴다 (0.672 vs 0.873). 즉 **WPCA 축소는 정확도를
떨어뜨린다.** 논문의 유일한 우위는 **계산시간 0.2358 s vs 0.2798 s = 0.044 초**
다. 저자는 `[인쇄]` "It is impractical to focus only at the relative accuracy
and should be more concerned with the cost of the computational burden" 로
프레임을 정확도에서 비용으로 옮긴다.

`[해석]` **0.044 초의 차이를 근거로 "best performance" 를 주장한다.** 게다가
이 시간에는 **ECM/DRT 파라미터 계산이 제외**돼 있는데(§4.1 명시), Feature1 은
그 전처리로 split-frequency 회귀 + DRTtools 역문제를 매 스펙트럼마다 풀어야
하고 Feature2 는 **전처리가 0** 이다. **전처리를 포함하면 비교가 뒤집힐 것이
거의 확실하다.** 논문은 이 계산을 하지 않는다.

`[해석]` **결론절의 문장 오류** `[인쇄, p.12]`: "the RMSE of Feature1 is
0.873 %, which is only slightly **lower** than Feature3's RMSE of 0.672 %."
— 0.873 은 0.672 보다 **높다**(= 나쁘다). 서술이 뒤집혀 있다.

`[도표]` **Fig. 12** (직접 봄): 5셀 각각 사이클 vs SOH, 검은 실선(Real) ·
붉은 선(Estimated) · 95 % CI(연분홍 띠). 사이클 수는 cell1 ≈ 172, cell2 ≈ 245,
cell3 ≈ 225, cell5 ≈ 172, cell6 ≈ 140. **(d) cell5 와 (e) cell6 에서 사이클
0 부근의 추정이 크게 빗나간다** — 실측이 100 % 에서 시작하는데 추정은 ~90 %
에서 시작한다. MaxAE 가 초기 5 사이클을 제외하는 이유가 여기 있다
`[해석]`. (e) cell6 의 CI 폭이 눈에 띄게 넓다(≈ ±4 %p) — 본문은 CI 를 "stable"
이라고만 쓴다.

---

# 그림별 판독 (직접 본 것)

## Fig. 1 — SOH 감쇠와 EIS `[도표]`

(a) 5셀의 SOH vs cycle. y 축 50–100 %, x 축 0–~230. **EOL 70 % 수평 점선**.
초기에 급락한 뒤 선형 감소. cell3(노란 ▽)이 가장 빨리 떨어져 **첫 10사이클
만에 ≈ 78 %** 로 급락한 뒤 완만해지고, cell2(주황 \*)는 완만하지만 길어
**~245 사이클까지 ≈ 74 %** 에 머문다. cell1(파랑 △)·cell5(보라 □)·cell6(초록
◇)은 그 사이.

(b)–(f) 각 셀의 Nyquist(Z′ vs −Z″, 둘 다 Ω), 색은 **파랑=Fresh → 빨강=Aged**.

- 공통 형상: 중고주파 **눌린 반원** + 저주파 **상승 직선**.
- **(b) cell1**: 반원 정점이 fresh ≈ 0.18 → aged ≈ 0.22 Ω 로 **커지고**,
  좌측 절편(R_∞)도 ≈ 0.30 → 0.37 Ω 로 **오른쪽 이동**. 스펙트럼이 통째로
  오른쪽으로 밀린다.
- **(c) cell2**: 반원 정점 ≈ 0.27–0.28 Ω 로 **거의 변하지 않는다**. R_∞ ≈
  0.25 Ω 고정. 변하는 것은 저주파 꼬리뿐.
- **(d) cell3**: 정점이 fresh ≈ 0.28 → aged ≈ 0.38 Ω 로 **가장 크게 증가**.
  R_∞ 는 ≈ 0.25 Ω 로 거의 고정.
- **(e) cell5**: 정점 ≈ 0.17 → 0.19 Ω, 우측 이동 뚜렷.
- **(f) cell6**: 정점 ≈ 0.25 Ω 에서 **거의 변화 없음**.

`[해석]` **다섯 셀의 노화가 서로 다른 방식으로 진행된다.** cell1/cell5 는
**R_∞ 증가 주도**(스펙트럼 평행이동), cell3 는 **반원 성장 주도**(R_∞ 고정),
cell2/cell6 는 **둘 다 거의 안 변한다**. 같은 온도·같은 프로토콜인데
임피던스 열화 경로가 셋으로 갈린다. §3.2 에서 R_pol 의 부호가 셀마다 뒤집힌
이유가 **여기 그림에 이미 보인다** — 논문은 이 연결을 짓지 않고 "consistency
차이" 로만 부른다 `[인쇄, p.3]`: "cell2 and cell6 have less cell variation,
which makes it difficult to determine the ideal health profile using EIS".

## Fig. 2 — 모델과 전류 경로 (캡션만 확인, 구조는 Fig. 3 에서 봄)

(a) 개발 모델, (b) LEIS 전류 경로, (c) HEIS 전류 경로.

## Fig. 3 — split-frequency fitting 예시 `[도표]`

가운데에 회로도가 있고 (좌: **L–R_∞** 주황 상자 / 중: **R₁//C₁ … Rₙ//Cₙ**
녹색 상자 / 우: **CPE** 보라 상자), 세 상자에서 각각 위쪽 소그림으로 선이
뻗는다.

- 좌상 **"RL EIS Fitting"**(주황 \*): Nyquist 상에서 x ≈ 0.3 에 **수직선**
  (−Z″ 가 0 → −0.11, x 는 거의 고정). L·R_∞ 성분.
- 중상 **"DRT EIS Data(× 진녹) / DRT EIS Fitting(연녹)"**: L·R_∞·CPE 를 뺀
  **잔차 반원** — x 0 → ≈ 1.05, 정점 −Z″ ≈ 0.26. 데이터와 fitting 이 육안으로
  구분되지 않을 만큼 겹친다.
- 우상 **"CPE EIS Data(보라 ○) / CPE EIS Fitting(보라 선)"**: x 0.05–0.30,
  y 0.09–0.37 의 **직선**. 12점 남짓만 쓴다.
- 하단 **"EIS Data(파랑 ○) / EIS Fitting(빨강 선)"**: 최종 재구성. x 0.25–1.65.
  반원 정점 ≈ 0.26 at x ≈ 1.0, 저주파 최소 ≈ 0.095 at x ≈ 1.40, 이후 상승.
  **좌측 끝(x ≲ 0.32, 고주파)에서 빨간 fitting 선이 파란 데이터에서 크게
  벗어나 아래로 급강하한다.**

`[해석]` 마지막 항목이 중요하다 — **가장 큰 fitting 오차가 고주파 끝에 있고,
그곳이 바로 R_∞·L 을 "최고주파 5점 평균" 으로 정한 지점**이다. 5점 평균이라는
거친 추정이 그 대가를 그림에 남겼다. R_∞ 가 우리 대조에서 쓰일 값이라면
**이 편향을 감안해야 한다**.

`[해석]` CPE fitting 에 쓰인 저주파 점이 **12개 남짓**이다. 60점 중 5점은
HEIS, ~12점은 LEIS 로 소비되고 나머지 ~43점만 DRT 로 간다. 정보 예산이 이렇게
쪼개진다는 사실은 본문에 없다.

## Fig. 4 — 가짜 peak 제거 `[도표]`

(a) 전통 DRT, (b) 이 논문 방법. 둘 다 x = τ (10⁻⁶ ~ 10³ s), y = γ(ln τ) (0–1 Ω),
5셀 첫 사이클을 색으로 구분(검=cell1, 빨=cell2, 파=cell3, 청록=cell5, 주황=cell6).

- **(a)**: τ ≈ 10–10² s 에 **거대 peak** (높이 0.6–0.8 Ω) 이 점선 타원으로
  묶여 **"False-peak"** 라 표시. τ ≈ 0.1–1 s 에도 작은 봉우리(≈ 0.08)가
  두 번째 "False-peak" 로 표시. 그 왼쪽(τ < 0.1 s)에는 우리가 아는 p₁·p₂·p₃
  구조가 있다.
- **(b)**: 큰 가짜 peak 이 **사라졌다**. 남은 것은 τ ≈ 10⁻⁵ ~ 10⁻¹ s 의 구조
  (최대 ≈ 0.29, cell3 파랑). **다만 τ ≈ 10–30 s 에 높이 ≈ 0.02 의 잔여 봉우리가
  여전히 남아 있다** — 본문은 이것을 언급하지 않는다.

`[해석]` **제거는 확실히 됐다.** 그러나 이 그림은 "제거된 것이 가짜였다" 를
증명하지 않는다 — 그것을 증명하려면 독립 근거(예: 알려진 Warburg 계수, 대칭셀,
합성 데이터)가 필요하고 논문에는 없다. **"CPE 로 모델링한 것을 뺐더니 CPE 처럼
생긴 peak 이 사라졌다"** 는 동어반복에 가깝다.

## Fig. 5 — 노화 중 γ(ln τ) ★ `[도표]`

5패널 (a) cell1 (b) cell2 (c) cell3 (d) cell5 (e) cell6. x = τ (10⁻⁵ ~ 10⁰ s),
y = γ(ln τ) (0–0.6 Ω), 색 **파랑=Fresh → 진빨강=Aged**. 점선 타원으로 p₁, p₁.₅,
p₂, p₃ 를 표시.

읽은 값 (`figure-read ≈`):

| | p₁ 위치 / 높이(fresh→aged) | p₂ 위치 / 높이 | p₃ 위치 / 높이 | p₁.₅ |
|---|---|---|---|---|
| (a) cell1 | ≈ 8×10⁻⁵ s, ≈ 0.13 → 감소 | ≈ 8×10⁻⁴ s, ≈ 0.10 | ≈ 1×10⁻² s, **0.20 → 0.32** | 없음 |
| (b) cell2 | ≈ 5×10⁻⁵ s, ≈ 0.13 → 감소 | ≈ 3×10⁻³ s, **0.20 → 0.15** | ≈ 2–3×10⁻² s, **0.22 → 0.33** | 있음 |
| (c) cell3 | ≈ 4×10⁻⁵ s, ≈ 0.17 → 감소 | ≈ 2×10⁻³ s, **0.17 → 0.14** | ≈ 3–5×10⁻² s, **0.28 → 0.55** | 있음 |
| (d) cell5 | ≈ 1×10⁻⁴ s, ≈ 0.10 | ≈ 1×10⁻³ s, ≈ 0.09 | ≈ 1×10⁻² s, **0.17 → 0.25** | 없음 |
| (e) cell6 | ≈ 4×10⁻⁵ s, ≈ 0.15 → 감소 | ≈ 3×10⁻³ s, **0.20 → 0.16** | ≈ 2×10⁻² s, **0.24 → 0.30** | 있음 |

`[도표]` **본문 서술과 그림이 합치하는 부분**: p₃ 는 5셀 모두 노화와 함께
**증가**한다 (특히 cell3 는 거의 2배). p₁·p₂ 는 (a)(d) 를 빼면 **감소**한다.
p₁.₅ 는 (b)(c)(e) 에만 있고 노화하며 사라진다 — 전부 본문대로다.

`[해석]` ★ **그러나 이것이 본문의 LLI/LAM 문장을 반박한다.** 저자의 귀속에
따르면 **p₂ = 전하전달**인데 그것이 **감소**한다. "LLI 와 LAM 이 전하전달을
어렵게 만든다" 는 서술과 부호가 반대다. 증가하는 것은 **p₃ = 확산**이다.
`[해석]` 앞서 계산한 τ↔f 환산(p₃ ≈ 5–16 Hz)까지 감안하면 가장 정합적인
재해석은 **저자의 peak 귀속이 한 칸씩 밀렸다** 는 것이다 (p₂ 가 SEI/접촉,
p₃ 가 전하전달). 그렇게 읽으면 "노화하면 전하전달 저항이 증가한다" 는 서술은
살아나지만, **그 경우 논문의 인쇄된 귀속표가 틀린 것이 되고**, `ln τ_p₃`·
`γ(lnτ_p₃)`·`S₃` 라는 최상위 feature 3종의 물리적 이름이 전부 바뀐다.
어느 쪽이든 **이 논문의 peak↔과정 대응은 인용에 쓸 수 없다.**

## Fig. 6 — feature 정의 모식도 `[도표]`

단일 γ(ln τ) 곡선(파란 선, 노란 음영) 위에 p₁(≈0.13 at 7×10⁻⁵), p₁.₅(≈0.115),
p₂(≈0.155 at 2×10⁻³), p₃(≈0.48 at 3×10⁻²) 와 골 v₁(≈0.05), v₁.₅, v₂(≈0.048)
를 파란 점으로 찍고, **peak height** 는 0 에서 peak 까지의 세로 양방향 화살표,
**골 높이** 는 파란 점선, **S₁·S₂·S₃** 는 빗금친 노란 영역(변곡점 사이),
**ln τ_p₃** 는 p₃ 위치에서 오른쪽으로 뻗은 수평선으로 표시.

`[해석]` **peak height 가 0 기준 절대 높이**임이 그림으로 확정된다
(peak−valley 진폭이 아니다). 이는 [[dv-peak-heterogeneity-descriptor]]
(Kim 2023) 에서 확인한 것과 **같은 선택**이다 — 두 논문 모두 valley 를 빼는
진폭이 아니라 **절대값**을 쓴다. `[해석]` 반면 세미나의 PVS 는 peak−valley
진폭을 쓴다. **valley 를 쓰지 않는 변형을 대조군으로 넣을 근거가 하나 더
쌓였다.**

## Fig. 7 — 상관계수 히트맵 ★

위 §3.2 의 표로 전부 옮겼다. (a) Pearson, (b) Spearman. x 축은 17 feature,
y 축은 5 cell, 색 스케일 −1(파랑) ~ +1(진빨강), **채택된 8개의 축 라벨이
빨간 글씨**로 인쇄돼 있다 — 본문의 채택 목록과 **정확히 일치**한다.

## Fig. 8 — 8개 HF vs SOH ★ `[도표]`

8패널, 전부 x = SOH (%) 65–100, y = "Amplitude", 5셀을 색 사각형으로
(파랑 cell1, 노랑 cell2, 빨강 cell3, 보라 cell5, 초록 cell6).

`[도표]` **캡션과 패널 라벨이 어긋난다**: 캡션은 (a)–(h) = Q, lnτ_p₃,
γ(lnτ_p₃), γ(lnτ_v₂), ratio_p₁, ratio_p₂, ratio_p₃, S₃ 인데, **그림 안의 (f)와
(g) 가 둘 다 `ratio_p2` 로 인쇄**돼 있다. (g) 는 `ratio_p3` 여야 한다 —
(g) 의 y 범위가 0.4–0.7 이고 SOH↓ 에서 증가하는 것이 캡션의 ratio_p₃ (표에서
음의 상관) 와… `[해석]` 부호가 맞지 않는다. 표에서 ratio_p₃ 는 **음의 상관**
(SOH↓ → 값↑) 이고 (g) 는 SOH↓ 에서 값이 **증가**하므로 (g) = ratio_p₃ 가
맞다. **(f)/(g) 중 (g) 의 라벨이 오타**다.

읽은 값 (`figure-read ≈`):

- **(a) Q**: SOH 100 → 70 에서 0.11 → 0.13(cell1) … 0.125 → 0.18(cell3).
  단조 증가, 셀별 곡선이 **분리**된다.
- **(b) ln τ_p₃**: −2.2(cell1, SOH 95) → −1.35(cell3, SOH 68). 셀별 **오프셋이
  0.5 이상** — cell1 은 −2.2 대, cell3 는 −1.6 대에서 시작한다.
- **(c) γ(lnτ_p₃)**: SOH 70 에서 cell3 ≈ **0.50**, cell5 ≈ **0.25** — **2배 차이**.
- **(d) γ(lnτ_v₂)**: 0.03–0.19. cell2/cell3/cell6 는 SOH 70→100 에서 0.03 →
  0.19 로 크게 변하는데 **cell1/cell5 는 0.05 → 0.08 로 거의 안 변한다**.
- **(e) ratio_p₁**: 0.155–0.28. 다섯 셀이 비교적 겹친다.
- **(f) ratio_p₂**: 0.17–0.33.
- **(g) [실제로는 ratio_p₃]**: 0.43–0.67.
- **(h) S₃**: 0.10–0.255. SOH 70 에서 cell3 ≈ 0.25, cell6 ≈ 0.15.

`[해석]` ★ **이 그림이 §4.1 의 데이터 분할 선택을 설명한다.** 어느 패널을
보아도 **같은 feature 값이 셀마다 다른 SOH 에 대응**한다. 예: γ(lnτ_p₃) = 0.30
은 cell1 에서는 SOH ≈ 95 %, cell3 에서는 SOH ≈ 78 % 다. 즉 **feature → SOH
사상이 셀 간에 이동(shift)한다.** 셀 간 학습/시험을 하면 이 오프셋만큼
틀린다. 논문이 셀 안 무작위 분할을 쓴 것은 편의가 아니라 **필연**이다.

`[해석]` **우리 축에 대한 함의**: 임피던스 유래 feature 는 **셀 고유 오프셋**을
크게 싣는다. SEV 를 실측에 적용할 때 절대값 대비가 아니라 **같은 셀 안의
상대 변화**만 써야 할 가능성이 높다. 그런데 SEV 로 모드를 가르는 설계는
**절대적인 부호·크기 구조**에 의존한다 — 이 둘은 긴장 관계다.

## Fig. 12 — SOH 추정 결과

위 §4.4 에서 서술.

## 본 것과 안 본 것

- **본 것 (8/15)**: `fig_1`(SOH+EIS), `fig_3`(split-frequency fitting),
  `fig_4`(false peak), `fig_5`(노화 중 DRT ★), `fig_6`(feature 정의),
  `fig_7`(상관 히트맵 ★), `fig_8`(HF vs SOH ★), `fig_12`(SOH 추정).
- **안 본 것 (4)**: `fig_2`(모델 회로도 — Fig. 3 가운데에 같은 회로가 있어
  대체됨), `fig_9`(순서도), `fig_10`(4모델 EIS fitting 비교 — Table 3 이
  수치로 정본), `fig_11`(4모델 RMSE 막대 — Table 3 과 같은 내용).
- **표 3장** (`tab_1`, `tab_3`, `tab_4`) 은 이미지로 읽지 않고 **PDF 텍스트**로
  옮겼다 (도구 권고).

---

# 방법론 비판 요약 (심각도 순)

1. **★ 셀 안 무작위 40/60 분할 → 시간적 누출.** 인접 사이클이 학습·시험에
   나뉘어 들어간다. RMSE 0.873 % 는 보간 성능이다. 저자가 §5 에서 인정하고,
   그 이유(셀 간 차이가 커서)까지 밝힌다. **이 논문의 어떤 성능수치도 새 셀에
   대한 일반화 근거가 아니다.**
2. **★ 제안 방법이 baseline 에 정확도로 진다.** 원시 스펙트럼(Feature2) 이
   RMSE·R²·MaxAE 모두 우세. 우위는 0.044 초의 계산시간뿐이고, 그 비교에서
   **DRT 전처리 비용이 제외**돼 있다.
3. **★ peak↔과정 귀속에 근거가 없고, 자기 데이터와 어긋난다.** §2.4 참조.
   전극 귀속(PE/NE)은 아예 없다.
4. **불공정한 모델 비교.** 무한차수 DRT vs 2차 ECM 의 fitting 오차 비교.
   복잡도 벌점 없음.
5. **λ = 1E-3 의 근거 부재 + DRT 불확실성 미보고.** DRT 는 정규화 강도에
   peak 폭·개수가 민감한데 λ 민감도 분석이 없다. credible interval 없음.
6. **부호를 버리는 feature 선별.** |corr| 만 보는 절차가 "부호가 셀마다
   뒤집힌다" 는 진단을 원리적으로 차단한다.
7. **WPCA 가중식의 수치 불안정 + β 값 미인쇄** → 재현 불가.
8. **초록의 "RMSE within 0.873 %"** 는 평균이며 cell5 는 1.607 %.
9. **자잘한 편집 오류**: 절 번호가 깨져 있다 (§2 말미가 "Section 4 extracts…",
   §4.3 이 "From Section 4.3, we have…" 로 자기 참조, §3 이 §4.1/4.2 를 참조).
   Fig. 8 (g) 라벨 오타. p.12 의 "lower than" 방향 오류. p.3 의 EOL 설명
   ("there are only 250 cycles left until it reaches 70 %") 은 문장이 깨져
   의미가 불분명하다.

---

# 우리 프로젝트와의 접점

## A. `mode-observability` Phase 2 (데이터 층) — **가장 실질적**

1. **출처 확정 완료.** 원 출처 = Zhang et al. 2020, *Nat. Commun.* 11,
   DOI 10.1038/s41467-020-15235-7 / Zenodo 10.5281/zenodo.3633835.
   `mode-observability/manifests/README.md` 의 유보를 이 근거로 푼다.
   **인용은 Zhang 2020 을 1차로, Su 2024 를 "이 데이터로 무엇을 했는가" 의
   선행연구로 쓴다.**
2. **좌표 해독 완료.** `state I~IX` = 한 충방전 사이클 안의 아홉 측정 시점,
   **state V = 100 % SOC (15분 휴지 후)**. 열화 축은 파일 안의 `cycle number`.
   Su 는 **25 °C · state V · 5셀**만 썼다 → **온도 축과 state 축 전체가
   미사용 자원**이다.
3. **셀 사양**: LiCoO₂/graphite, 45 mAh (1C = 45 mA). **형태는 원문에 없다** —
   코인셀 여부는 Zhang 2020 에서 확인해야 한다.
4. **EIS 프로토콜**: 정현파 **전류 5 mA** (≈ C/9), 60 주파수, 0.02 Hz–20 kHz.
   우리 실측과 일치.
5. **확인해야 할 불일치 2건**: (i) Su 는 12셀(25 °C 8 + 35 °C 2 + 45 °C 2)만
   열거하는데 우리 manifests 패턴은 온도별 01–08 을 시사한다. (ii) 176 파일이
   12셀 × 9 state + 12 용량 = 120 과 맞지 않는다. (iii) `25C42` 는 Su 의
   열거로 설명되지 않는다.
6. **Su 를 재현 baseline 으로 쓸 수 있다.** 같은 5셀·같은 state 에서 DRT 를
   돌리면 우리 파이프라인이 문헌과 같은 그림을 내는지 확인 가능하다.
   (단, λ=1E-3·DRTtools RBF 기본값이라는 정보만으로는 완전 재현이 어렵다.)

## B. `pvs-sev-lli-lampe-separability` (SEV 축)

1. **기존 Evidence For 의 등급 하향.** "LLI 와 LAM 이 함께 R_ct 를 올린다" 는
   **Su 의 측정이 아니라 [20](Jiang 2022) 에서 상속된 해석 한 문장**이고,
   Su 자신의 Fig. 5·Fig. 7 과 부호가 어긋난다. → H1 의 문헌 근거로 쓸 수 없다.
   **진짜 원전은 Jiang et al., *Appl. Energy* 322 (2022) 119502 이며, 그것이
   다음 확인 대상이다.**
2. **대신 새 Evidence(양가) 1건.** 실측 5셀에서 **전하전달 peak 높이의 노화
   부호가 셀 간에 뒤집히고**(1/5), **R_pol 은 2/5 에서 뒤집힌다**. SEV 처럼
   부호 구조에 의존하는 feature 는 이 재현성 문제를 먼저 통과해야 한다.
   이것은 H1/H2 판정이 아니라 **무대 자체에 대한 경고**다.
3. **전극 귀속에 대해서는 침묵.** 이 논문은 PE/NE 를 나누지 않으므로
   SEV 의 R_ct,PE 귀속에 찬성도 반대도 하지 않는다. `[해석]` DRT 로 셀 수준
   임피던스를 풀면 전극이 자동으로 갈리지 않는다는 것을 **실물로 보여 주는
   사례**이며, SEV 가 "DRT 로 R_ct,PE 를 얻는다" 고 할 때 그 한 걸음이
   **자명하지 않다**는 근거가 된다.
4. **valley 대 절대 peak.** Fig. 6 이 확정하듯 이 논문의 peak height 는
   **0 기준 절대값**이다. Kim 2023 과 같은 선택 — PVS 의 valley 의존에 대한
   대조군 설계 근거가 하나 더 쌓였다.

## C. `22p-physics-or-degeneracy` (주 카드)

`[해석]` 직접적 증거는 없다. 다만 간접적으로: 이 논문은 **17개 feature 의
96.7 % 이상이 한 주성분에 실린다**는 것을 보였다. 임피던스 유래 feature 를
여러 개 늘려도 **독립 방향이 늘지 않는** 사례이며, 우리가 "관측을 늘리면
갈리는가" 를 물을 때 **늘린 관측이 서로 독립인지 먼저 봐야 한다**는 것의
문헌 예시다.

## D. 우리가 이 계열에 공급할 수 있는 것

1. **DRT peak↔과정 귀속의 검증 도구.** 우리는 합성 truth 에서 모드를 고정한
   채 임피던스를 낼 수 있으므로(PyBaMM), "어느 τ 대역이 어느 전극·어느
   과정인가" 를 **강제로** 알 수 있다. 이 논문이 근거 없이 선언한 것을
   판정할 수 있는 자리다.
2. **λ 민감도의 상한.** 정규화 강도가 peak 위치·높이를 얼마나 흔드는지를
   합성 데이터로 정량하면, `ln τ_p₃`·`γ(lnτ_p₃)` 류 feature 의 신뢰 구간이
   생긴다. 이 분야에는 그 수치가 없다.
3. **cross-cell 일반화 실패의 분해.** Fig. 8 의 셀별 오프셋이 (a) 초기 제조
   편차인지 (b) 열화 모드 조합 차이인지, 이 논문은 구분할 수 없다
   (모드를 재지 않으므로). 우리는 모드를 고정한 채 (b) 의 몫을 계산할 수 있다.

---

# 이 논문에서 인용 가능한 문장 (verbatim)

DRT 의 한계에 대한 **저자 자신의 경고** — 우리 논지에 가장 쓸모 있는 문장
`[인쇄, p.2]`:

> "because distribution sharpness/smoothness is an unreliable indicator for
> the existence or absence of peaks (discrete relaxations), continuous DRT
> estimates are prone to producing false peaks or omitting true relaxation
> processes [27]. If the non-relaxation process is considered as the true
> relaxation process, although it may still end up with a better EIS fit, it
> is spurious by nature and will eventually affect the feature extraction of
> the true relaxation process."

cross-cell 일반화 실패의 **자백** `[인쇄, p.14]`:

> "instead of splitting the dataset into training datasets from one or more
> batteries and testing datasets from other batteries, we randomly disrupt the
> data for each battery and randomly selects 40 % of the data as training
> dataset and the remaining 60 % as test dataset. This is due to the
> significant difference in battery consistency, not only in terms of initial
> capacity and decay, but also in the EIS."

문제의 LLI/LAM 문장 (**인용할 때 반드시 [20] 상속임을 밝힐 것**)
`[인쇄, p.6]`:

> "Except for cell1, the value of p1 and p2 for the other cells tends to
> decrease. On the other hand, the value of p3 shows an increasing trend with
> aging. These trends are in line with the fact that the loss of stock (LLI)
> and loss of active material (LAM) in the electrode makes the charge transfer
> process more difficult with the battery aging [20]."

---

# 다음 확인 대상

1. **★ Zhang et al. 2020, *Nat. Commun.* 11, 6 (DOI 10.1038/s41467-020-15235-7)**
   — 우리가 쓰는 데이터의 **원 논문**. 셀 형태·제조사·사이클링 프로토콜·
   state I~IX 의 정의·셀 목록이 전부 거기 있다. Phase 2 에 필수.
2. **Jiang et al., *Appl. Energy* 322 (2022) 119502** — "LLI/LAM 이 전하전달을
   어렵게 한다" 의 **진짜 원전**. ①의 사슬을 끝까지 따라가려면 이것을 봐야
   한다. 같은 저자군의 [40] (Zhu et al., *Energy* 284 (2023) 129283, DRT
   timescale + MRMR) 도 같은 계열.
3. **Huang et al., *Electrochim. Acta* 443 (2023) 141879** ([27], "How reliable
   is DRT analysis?") — Su 가 인용한 DRT 신뢰성 비판의 원전. λ·가짜 peak
   문제의 기준 문헌이 될 수 있다.
