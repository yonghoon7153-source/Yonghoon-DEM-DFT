---
source_url: local-upload/Advanced_Energy_Materials_2025_Wang_Interpretable_Machine_Learning_for_Battery_Prognosis.pdf
ingested: 2026-09-03
sha256: aa4b36a6005bc5986fe66da9fb4efb277d18dcd697ba2fa89ed6d38a1c648d7d
---

# 수집 목적

Ting-Ting Wang, Kun-Yu Liu, Hong-Jie Peng, Xinyan Liu,
**"Interpretable Machine Learning for Battery Prognosis: Retrospect and
Prospect"**, *Advanced Energy Materials* **15**, e03067 (2025) 의 **절별
해체분석**.

이 자료는 **리뷰(REVIEW)** 다. 1차 연구가 아니라 분야의 자기 서술이며, 따라서
이 digest 의 무게중심은 "무엇을 발견했나" 가 아니라 **"이 분야가 무엇을
문제로 인식하고 무엇을 인식하지 않는가"** 에 있다.

흡수 동기는 두 가지다.

1. 2026-09-02 BML 세미나(김시원) **p.4** 가 physics-inspired feature
   engineering 을 도입하면서 근거로 `Adv. Energy Mater., 2025, 15, e03067` 을
   인용했다 (`raw/papers/2026-09-02-siwon-kim-degradation-mode-ml-seminar.md`
   p.4). **이 PDF 가 그것인지 article number 로 확인**하는 것이 첫 과제였다 —
   §0 에서 확인했다 (일치).
2. 직전에 흡수한 [[birkl-ocv-degradation-diagnostic]] (Birkl 2017) 이 라벨
   **생성 절차**의 원전이었다면, 이 리뷰는 그 라벨을 소비하는 **ML 쪽 분야
   서술**이다. 두 층 모두에서 "식별 가능성·라벨 불확실성" 이 어떻게 다뤄지는지
   (혹은 다뤄지지 않는지)를 확인하는 것이 이번 흡수의 최우선 목표였다.

**표기 규칙** (이 위키 관례 3구분):
- `[인쇄]` — 논문 본문/표/캡션/식에 글자로 있는 것
- `[도표]` — 그림에서 눈으로 읽은 근사값 (원 데이터가 아니다)
- `[해석]` — 이 문서를 쓰면서 붙인 판단. **리뷰의 주장이 아니다**

- 원본 파일: 로컬 업로드 PDF (저장소에 바이너리를 넣지 않는다)
- 크로핑 그림: `raw/figures/wang2025_interpretable-ml-battery-prognosis/`
  (fig 8장 + tab 1장, `figures.json` 에 캡션 색인)

---

## 0. 서지사항 (직접 확인) — 세미나 인용과의 대조

`[인쇄]` PDF 1쪽 헤더·각주 및 파일 메타데이터에서 확인한 것:

| 항목 | 값 |
|---|---|
| 문서 종류 | **REVIEW** (표지 좌상단 인쇄) |
| 제목 | Interpretable Machine Learning for Battery Prognosis: Retrospect and Prospect |
| 저자 | Ting-Ting Wang, Kun-Yu Liu, Hong-Jie Peng\*, Xinyan Liu\* (\* 교신) |
| 기여 | "T.-T.W. and K.-Y.L. contributed equally to this work." (Acknowledgements) |
| 소속 | Institute of Fundamental and Frontier Sciences (IFFS), University of Electronic Science and Technology of China (UESTC), Chengdu, Sichuan 611731, China · X. Liu 는 Key Laboratory of Quantum Physics and Photonic Quantum Information, Ministry of Education, UESTC 겸직 |
| 교신 메일 | hjpeng@uestc.edu.cn · xinyanl@uestc.edu.cn |
| 학술지 | *Advanced Energy Materials* **2025**, **15**, **e03067** |
| DOI | **10.1002/aenm.202503067** |
| 접수/개정/온라인 | Received: June 5, 2025 · Revised: July 10, 2025 · Published online: **October 22, 2025** |
| 쪽수 | 20쪽 (본문 e03067 (1 of 20) – (16 of 20), 참고문헌 포함 20) |
| 키워드 | battery prognosis, energy storage, interpretability, machine learning |
| 저작권 | © 2025 Wiley-VCH GmbH, 페이지 각주에 Creative Commons License 문구 |
| 연구비 | National Natural Science Foundation of China (Nos. 22379021, 22479021) |
| 이해충돌 | "The authors declare no conflict of interest." |
| Data Availability | "This is a review article, all the data presented in this article were cited from the original papers." |

**세미나 인용과의 일치 여부 — 일치한다.** 세미나 p.4 가 적은
`Adv. Energy Mater., 2025, 15, e03067` 는 권(15)·article number(e03067)·연도
(2025)가 이 PDF 와 정확히 같다. 페이지 하단 러닝 헤더가 매 쪽
`Adv. Energy Mater. 2025, 15, e03067` 로 인쇄돼 있고, PDF 메타데이터의
Subject 필드도 `Advanced Energy Materials 2025.15:e03067` 이다. **추정이 아니라
확인이다.**

`[해석]` 부수적 확인 하나: 세미나 p.4 는 같은 줄에 **두 번째 출처**로
`Joule, 2025, 9, 101884` 도 적는다. 그것은 이 리뷰의 **참고문헌 [113]**
(J. Rhyu, J. Schaeffer, M. L. Li, X. Cui, W. C. Chueh, M. Z. Bazant,
R. D. Braatz, *Joule* **2025**, 9, 101884) 와 일치한다. 즉 세미나 p.4 의 두
인용은 **리뷰 + 그 리뷰가 인용하는 원전 하나**의 조합이다.

---

## 1. 원문에 없어서 확인이 필요한 것 (공백 목록) ★

digest 를 쓰기 전에 먼저 밝힌다. 아래는 **리뷰가 인쇄하지 않은 것**이며, 이
리뷰를 근거로 이 자리를 메꾸는 문장을 쓰면 그것은 이 리뷰의 근거가 아니다.
근거는 §9 의 전수 확인이다.

1. **"identifiability(식별 가능성)" 이라는 단어가 본문에 한 번도 없다.**
2. **"uncertainty(불확실성)" 이라는 단어가 본문에 한 번도 없다.** UQ·신뢰구간·
   오차 막대·사후분포 논의가 전혀 없다.
3. **"noise" 가 한 번도 없다.** 측정 잡음이 feature 나 해석에 미치는 영향을
   다루는 문단이 없다.
4. **역문제의 유일성·축퇴(degeneracy)·ill-posedness 를 다루는 절이 없다.**
5. **교차검증 설계(cross-validation, train/test split, group 정의)에 대한
   서술이 없다.** 인용된 연구들의 성능 수치(MAPE/RMSE)는 나열되지만 그 수치가
   어떤 분할에서 나온 것인지 리뷰는 적지 않는다.
6. **정답 라벨의 출처를 묻는 문단이 없다.** 인용 연구의 target 이 측정값인지
   fitting 산물인지 리뷰는 구분하지 않는다 (유일한 예외적 언급은 §5.1.1 의
   "feature importance 에는 보편적 ground truth 가 없다" 인데, 이는 **라벨**이
   아니라 **해석의 정답**에 대한 진술이다).
7. **full-cell OCV·pseudo-OCV·half-cell 이라는 단어가 본문에 없다** (전수
   확인: `OCV` 0회, `open circuit` 0회, `half-cell` 0회). 즉 Birkl 계열의
   전극 수준 분해 절차는 이 리뷰의 서술 범위 안에 **없다**.
8. **해체(post-mortem/teardown/disassembly) 검증에 대한 언급이 없다** (0회).
9. **feature 간 공선성은 딱 두 곳에서만, 그것도 post-hoc 도구의 한계로만
   나온다** (§9.2). feature **설계** 단계의 공선성 논의는 없다.
10. **전극 수준(LLI/LAM) 을 예측 target 으로 삼는 절이 없다** (§10 상세).
11. **정량적 비교표가 없다.** Table 1 은 4종 방법의 정성 요약이며, 인용된
    연구들의 성능을 같은 축에서 비교하는 표·그림이 없다.
12. **리뷰의 문헌 선정 기준(검색어·기간·포함/배제 규칙)이 인쇄되지 않았다.**
    체계적 문헌고찰(systematic review) 이 아니라 서술형 리뷰다.

---

## 2. 리뷰의 질문과 답 (Abstract · §1 Introduction, p.1–2)

### 2.1 문제 설정

`[인쇄]` 초록 (전문에 가깝게):

> "The multidimensional parameter space resulting from the interplay of complex
> physicochemical mechanisms and dynamic operating conditions renders
> traditional trial-and-error methods increasingly inadequate for advanced
> battery research. Although data-driven approaches have demonstrated
> considerable potential for accurate battery prognosis, **their inherently
> opaque architectures often hinder the extraction of mechanistic insights**,
> thereby limiting their applicability in guiding the refinement of operating
> strategies and the design of next-generation battery systems. In response to
> this limitation, interpretable machine learning frameworks that balance
> predictive fidelity with physicochemical relevance have emerged as a
> compelling alternative. Building on this paradigm shift, this review
> systematically examines state-of-the-art interpretable battery lifetime
> prediction techniques, **focusing on four critical dimensions: white-box
> model, physics-informed machine learning, physics-inspired feature
> engineering, and post-hoc analysis techniques.** Emerging challenges and
> strategic research directions are analyzed to guide the next-generation
> battery innovation …"

`[인쇄]` §1 이 지목하는 공백:

> "While success in leveraging ML to make accurate predictions has been widely
> reported and demonstrated, **adopting ML to deepen mechanistic understanding
> and to obtain physically meaningful insights, however, is rarely explored.**
> The main reason is that traditional ML frameworks for battery prognosis
> prioritize performance accuracy over model interpretability (Figure 1a)."

`[해석]` 이 리뷰가 세운 문제는 **"예측은 되는데 왜 되는지 모른다"** 이지,
**"예측 대상(라벨) 자체가 잘 정의돼 있는가"** 가 아니다. 이 구분이 이 digest
의 축이다 — 리뷰 전체가 *모델의 투명성* 축에 서 있고, *역문제의 적절성
(well-posedness)* 축은 시야에 들어오지 않는다.

### 2.2 용어 정리 — interpretable vs explainable

`[인쇄]` §1:

> "It is worth noting that a distinction is sometimes made between interpretable
> and explainable ML in computer science. Specifically, **interpretable ML
> generally refers to models that are inherently transparent, while explainable
> ML often involves post-hoc methods** that aim to uncover the reasoning behind
> the predictions of complex models. **In this review, however, we use these
> terms interchangeably** to offer battery researchers a comprehensive guide …"

`[해석]` 두 용어를 합친 결과, 리뷰의 4분류는 서로 다른 **층위**의 것을 한
평면에 놓게 된다 (모델 구조 2종 + feature 1종 + 사후 분석 1종). 저자들도
§6 에서 "Rather than forming a hierarchy, they constitute an integrative and
flexible toolbox" 라고 명시하므로 이것은 숨겨진 결함이 아니라 선언된 설계다.

### 2.3 답 (§6 Summary, p.14)

`[인쇄]`

> "Among these methods, white-box models offer inherent interpretability and are
> well-suited for small datasets or scenarios focused on transparency, but
> struggle with complex patterns. PIML embeds physics into model structure or
> objectives, enhancing physical consistency and predictive performance, albeit
> at the cost of increased model complexity and reliance on prior domain
> knowledge. Physics-inspired feature engineering ensures interpretability
> through meaningful inputs, aiding dimensionality reduction and cross-domain
> transferability, though it requires careful, domain-informed design. Post-hoc
> analysis is broadly applicable for extracting physical insights from trained
> models, **but its explanations may lack robustness and causal reliability.**"

`[인쇄]` 그리고 자기 평가:

> "Nevertheless, **while still at its infancy**, interpretable ML has already
> started to demonstrate its attractive potential in assisting and accelerating
> battery research."

---

## 3. 4종 분류 체계 ★ 의뢰 1항 (Fig. 1, Fig. 2, Table 1)

### 3.1 분류의 기준 — 해석 가능성이 **어디서** 들어오는가

`[인쇄]` §1 말미:

> "**Based on whether the interpretability is introduced by the model, the
> feature or the post-training analysis**, the discussion is divided into four
> sections: white box model, physics-informed ML (PIML), physics-inspired
> feature engineering, and post-hoc analysis (Figure 2)."

`[해석]` 기준은 하나의 축(해석 가능성의 **주입 지점**)이고, 그 축 위에 네 개가
놓인다: 모델 자체(2종: 구조가 단순해서 / 물리를 심어서) → 입력(feature) →
사후. 경계가 겹치는 지점은 §3.4 에 정리했다.

### 3.2 Fig. 1 — conventional vs interpretable 워크플로 (**본 그림**)

`[도표]` `fig_1.png` 를 실제로 보고 읽은 것:

**(a) Conventional ML framework** — 한 줄 파이프라인:
`Battery datasets` (배터리 아이콘) → `Feature engineering` (톱니바퀴) →
**`Black-box`** (검은 정육면체) → `Targets (SOH, RUL, SOC…)` (배터리 아이콘) →
`Domain experts` / `Users` (사람 아이콘 2개). 화살표는 **전부 왼→오 단방향**.

**(b) Interpretable ML framework** — 같은 검은 상자가 **반투명 회색 상자(안에
톱니가 보이는)** 로 바뀌고, 두 계열의 화살표가 추가된다:
- **파란 화살표(물리 지식 주입)**: 중앙 상단의 원자 기호 `Physical knowledge`
  에서 **세 갈래**가 각각 `Battery datasets`, `Feature engineering`,
  그리고 모델 상자로 들어간다.
- **파란 화살표(해석 산출)**: 모델 상자 → `Decision-making process /
  physical insights` → 사람 아이콘. 모델 상자 아래의 **`Explainable tools`**
  (스패너·드라이버 아이콘) 에서도 같은 라벨의 화살표가 사람 쪽으로 나간다.
- **초록 화살표(되먹임)**: 사람 → `Validation & Optimize ML` → 모델 상자,
  그리고 모델 상자 → `Validation & design battery` → `Battery datasets`.

`[해석]` **그림에서만 읽히고 본문에는 없는 것**: (b) 의 `Physical knowledge`
화살표가 **데이터셋에도** 꽂힌다는 점이다. 이는 §3.1 의 physics-informed data
augmentation(합성 데이터 생성)에 해당하며, 본문의 4분류 서술만 읽으면
"physical knowledge → feature 또는 model" 두 갈래로만 이해하기 쉽다.

`[해석]` **★ 이 그림에서 우리에게 가장 중요한 것**: (a)와 (b)의 `Targets` 이
**동일하게 `SOH, RUL, SOC…`** 다. 즉 리뷰가 그리는 "해석 가능성" 은
**출력을 바꾸는 것이 아니라 경로를 투명하게 만드는 것**이다. 2026-09-02
세미나가 하는 일 — target 자체를 macro(SOH)에서 **전극 수준(LLI/LAM)**으로
내리는 것 — 은 이 그림의 어느 화살표에도 그려져 있지 않다.

### 3.3 Fig. 2 — 4종 분류 도식 (**본 그림**)

`[도표]` `fig_2.png` 를 실제로 보고 읽은 것. 네 개의 색 테두리 상자가 위→아래로
쌓여 있고, 각 상자는 [아이콘 + 특징 2개 + 예시 그림 2개] 구조다.

| # | 상자 (테두리색) | 아이콘 | 인쇄된 특징 2줄 | 예시 그림 2개 |
|---|---|---|---|---|
| 1 | **White box model** (초록) | 반투명 상자 안 톱니 | `intrisic interpretability`(원문 오식, = intrinsic) · `computational simplicity` | **Linear regression** `f(x) = ax + b` (산점도 + 점선 직선) · **Symbolic regression** `f(x) = ax^b + ce^{dx} + …` (산점도, 적합선 없음) |
| 2 | **Physics-informed machine learning** (파랑) | 스패너 | `physical law alignment` · `prior knowledge Integration` | **Data augmentation** (여러 개의 단조 증가 곡선 다발) · **PINN** (신경망 도식 + `argmin 𝓛_data + 𝓛_mono + 𝓛_PDE`) |
| 3 | **Physics-inspired feature engineering** (금색) | 초록 원통 배터리 | `domain knowledge` · `model sanity` | **dQ/dV** (봉우리 3개짜리 곡선) · **Impedence**(원문 오식, = Impedance) (반원 + 우상향 직선 = Nyquist 개형) |
| 4 | **Post-hoc analysis** (빨강) | 전구 | `feature importance ranking` · `prediction rationalization` | **SHAP analysis** (beeswarm 3행) · **Importance ranking** (가로 막대 4개) |

`[해석]` 이 그림이 본문보다 더 정확하게 말해 주는 것 두 가지:
1. **3번 상자의 두 예시가 정확히 `dQ/dV` 와 `Impedance` 다.** 즉 리뷰가 생각
   하는 physics-inspired feature 의 표준형은 **ICA/DVA 계열 + 임피던스 계열**
   이며, 이는 세미나의 PVS(ICA 유래)·SEV(CI/저항 유래) 조합과 **같은 두 축**
   이다. 세미나의 feature 선택은 이 리뷰의 분류에서 정확히 3번 상자의
   전형이다.
2. **2번 상자의 PINN 손실식 `𝓛_data + 𝓛_mono + 𝓛_PDE` 가 그림에만 있다.**
   본문 §3.2 는 이 세 항을 문장으로 서술하지만 식으로 인쇄하지 않는다
   (Fig. 4c 에는 각 항의 전개식이 있다 — §5.3).

`[해석]` 오식 2건(`intrisic`, `Impedence`)은 그림 안 라벨이며 의미에 영향은
없다. 인용 시 원문 철자를 그대로 옮기지 않도록 여기 기록해 둔다.

### 3.4 Table 1 — 4종의 장점·한계·적용처 (p.15, 인쇄 텍스트)

`[인쇄]` 표 전체를 그대로 옮긴다 (PDF 텍스트에서 추출, 도구 권고에 따라
이미지 판독은 하지 않았다).

| 축 | White-box Models | PIML | Physics-inspired feature engineering | Post-hoc analysis |
|---|---|---|---|---|
| **Description** | Transparent models with simple logic | Models embedding physics into training | Physically meaningful feature construction | Interpretation tools applied after model training |
| **Tools** | Linear regression; symbolic regression | PINN; physics-guided loss functions | **IC/DV peaks; ECM parameters** | SHAP; PDP; ALE; LPR; saliency map; attention mechanism |
| **Advantages** | Easy to debug and validate; Data-efficient; Inherent interpretable | Promotes consistency with physical laws; Enables extrapolation; Reduces overfitting | Reduces dimensionality; Supports transferability; Aids hypothesis testing | Compatible with any model; Useful for debugging and insight generation |
| **Limitations** | Poor at modeling complex or nonlinear tasks; Needs manual feature design | Requires strong priors; Complex architecture; Limited to known physics | **Relies on expert knowledge; Limited novelty discovery** | Sensitive to data bias; Method-dependent outputs; **Limited causal understanding** |
| **Applications** | Small datasets; Simple systems; Baseline modeling | Electrochemical dynamics; Aging simulation | High-dimensional input; Cross-chemistry prediction; Expert-driven feature filtering | Fault detection; Model debugging; Hypothesis generation |

`[해석]` **★ 의뢰 1항의 핵심 답**: 저자들이 각 방법의 한계로 드는 것은
전부 **모델링 실무의 한계**(비선형성, 사전지식 요구, 전문가 의존, 데이터 편향,
방법 의존성)이며, **어느 칸에도 "feature 가 target 을 유일하게 결정하는가"
류의 한계는 없다.** physics-inspired feature engineering 의 한계는 "전문가
지식에 의존한다 / 새로운 발견을 하기 어렵다" 두 가지뿐이고, **"물리 feature
들이 서로 같은 방향을 잴 수 있다"** 는 종류의 한계는 표에도 본문에도 없다.

### 3.5 본문에 흩어진 각 분류의 한계 (Table 1 보다 상세)

`[인쇄]` **White box** (§2 말미, p.5):

> "it is often difficult to achieve extremely high prediction power while
> maintaining model transparency. They generally struggle with highly nonlinear
> tasks and complex interactions … Additionally, they typically rely on manual
> feature engineering, which can be time-consuming and **may introduce bias if
> domain knowledge is incomplete or inaccurate.**"

`[인쇄]` **PIML** (§3 말미, p.8):

> "PIML typically requires well-defined physical priors, and its model
> architecture can be complex and difficult to design. Moreover, **its strong
> reliance on embedded knowledge may hinder generalizability across varying
> operating conditions and limit the discovery of novel physical insights.**
> As a result, PIML is best suited for tasks where physical mechanisms are
> well-understood and can be mathematically formulated …"

`[인쇄]` **Physics-inspired feature engineering** (§4 말미, p.11):

> "By formulating and adopting features with physical meanings, **the validity
> of the model can be ensured and its prediction results can be rationalized.**
> Nevertheless, this approach often relies heavily on expert knowledge and may
> struggle to uncover novel mechanistic insights to advance further research.
> Despite these limitations, physics-inspired feature engineering is widely
> adopted, particularly for reducing complexity in high-dimensional spaces,
> enabling transferability across cells or chemistries, and supporting
> hypothesis validation through interpretable models."

`[해석]` **이 문단이 이 리뷰에서 가장 위험한 문장을 담고 있다**: "features with
physical meanings … **the validity of the model can be ensured**". 물리적
의미를 가진 feature 를 쓰면 모델의 타당성이 *보장된다*는 것은 논리적으로
성립하지 않는다 — 물리적으로 해석 가능한 feature 도 (a) 서로 공선일 수 있고,
(b) target 과 교란요인을 통해 상관될 수 있으며, (c) 여러 모드에 대해 같은
방향으로 움직여 모드를 못 가를 수 있다. 리뷰는 이 세 가지 중 어느 것도 §4
어디에서도 다루지 않는다. **세미나 p.4 가 이 리뷰를 근거로 삼을 때 실제로
빌려오는 것이 바로 이 문장의 논리다.**

`[인쇄]` **Post-hoc** (§5 말미, p.14):

> "However, one needs to be careful as the results are typically drawn from the
> data itself. **The conclusions can therefore be distorted if bias exists in
> the training data.** Moreover, several post-hoc analysis methods are still
> subject to ongoing debate regarding their interpretability, such as attention
> mechanism. In addition, **their feature importance may not stay consistent
> across different analysis methods.** Solely depending on such methods may be
> not adequate for achieving comprehensive model understanding."

---

## 4. §2 White Box Model (p.3–5)

### 4.1 선형회귀 계열

`[인쇄]` 정의:

> "White box models normally refer to models that are intrinsically
> interpretable. These models are often simple in structure, and reasonable
> understandings can be obtained from the models or model parameters. The
> well-known white box models include linear regression, logical regression,
> simple decision tree, and so on."

인용된 사례 (수치는 전부 `[인쇄]`):

| 문헌 | 무엇을 했나 | 성능 |
|---|---|---|
| **Severson et al. [77]** (*Nat. Energy* 2019, 4, 383) | 100번째–10번째 사이클의 방전 용량차 ΔQ₁₀₀₋₁₀(V) 의 **분산**을 cycle life 조기예측 feature 로. 정규화 선형모델, LFP\|Gr 상용셀 **124개**, 급속충전 (MIT 데이터셋) | test **MAPE 9.1%** |
| **Weng et al. [78]** (*Joule* 2021, 5, 2971) | 저 SOC 에서 잰 셀 저항 **R_LS** 를 진단 feature 로, 정규화 선형회귀 | MAPE **8%** (실온) / **7.4%** (45 °C) |
| **Guo et al. [81]** (*Joule* 2024, 8, 1820) | 도메인 지식 기반 feature **20개**의 중요도를 200 trial 의 선형회귀 계수 절대값 가중합으로 정량화 | ΔQ₁₀₀₋₁₀ 의 최소·평균·표준편차가 최상위 |
| **Liu et al. [79]** (*J. Energy Chem.* 2022, 68, 548) | 방전곡선을 **STL**(seasonal-trend decomposition using loess) 로 분해 → `trend mean`(분극·내부저항) + `seasonality area`(전압 프로파일 형상 변화) → ARIMA 로 외삽 → MLR 로 용량 매핑 | (수치 미인쇄) |
| **Liu et al. [80]** (*J. Energy Chem.* 2025, 106, 1) | 위를 3종 화학계로 확장, feature 기여도로 기구 해석 | (수치 미인쇄) |
| **Zhang et al. [82]** | **GEP**(Gene Expression Programming) 기반 기호회귀로 SOH 식 유도 | (수치 미인쇄) |
| **Schofer et al. [83]** (*Adv. Sci.* 2022, 9, 2200630) | 자동차용 파우치셀 **104개**의 cycle+calendar 노화 데이터에 기호회귀 | 외삽 정확도 **+38%**(저장시간) / **+13%**(에너지 처리량) / **+77%**(기타 stress factor) |

`[인쇄]` Severson feature 의 물리 근거로 리뷰가 드는 설명:

> "the authors demonstrated that **the loss of active material (LAM) of the
> delithiated negative electrode can result in a shift in discharge voltage
> while exhibiting no obvious change in the current capacity at early cycles.**
> As the cycling proceeds, however, the LAM eventually induces lithium plating,
> which irreversibly accelerates capacity loss."

`[해석]` **이것이 리뷰 전체에서 열화 모드가 등장하는 첫 번째 자리이며, 그
용법이 이 리뷰의 전형이다** — 모드는 *예측 대상*이 아니라 *feature 가 왜
작동하는지에 대한 사후 이야기*로 쓰인다. `LAM_NE,de` 가 "용량은 그대로인데
전압만 민다" 는 진술은 [[birkl-ocv-degradation-diagnostic]] §3.2 의
LAM_NE,de 서술(초기 용량 영향 작음, EoC 전압 하강)과 물리적으로 같은 내용
이지만, 이 리뷰는 그 연결을 하지 않는다 (Birkl 을 인용하지 않는다).

`[인쇄]` 기호회귀의 한계 (저자들이 인용 원문에서 가져온 것):

> "the authors also pointed out that **most of the equations generated by
> symbolic regression were relatively complex, which mitigated their local
> interpretability.** In this case, the incorporation of domain knowledge still
> remains necessary."

### 4.2 Fig. 3 (**본 그림**) — 및 캡션/그림 불일치 1건

`[도표]` `fig_3.png` 를 실제로 보고 읽은 것:
- **(a)** 대표 셀의 10번째·100번째 방전 곡선. x = Discharge capacity 0–1.1 Ah,
  y = Voltage 2.0–3.5 V. 두 곡선 사이 회색 음영. LFP 특유의 평탄역.
- **(b)** ΔQ₁₀₀₋₁₀(V) 를 전압축(2.0–3.5 V)에 대해 124셀 전부 겹쳐 그림.
  x = `Q100 − Q10` (Ah), 범위 대략 **−0.15 ~ 0**. 수명이 짧은 셀(붉은색)이
  왼쪽(더 큰 음의 값)으로 크게 벌어지고, 긴 셀(파란색)은 0 근처에 몰려 있다.
- **(c)** log–log 산점도: x = `Var(ΔQ₁₀₀₋₁₀(V))` 10⁻⁶–10⁻², y = Cycle life
  10²–10³ 대. 뚜렷한 우하향 직선. 패널 안에 **`ρ = −0.92`** 라고 인쇄돼 있다.
  컬러바 = Cycle life, 눈금 100 / 540 / 980 / 1,420 / 1,860 / 2,300.
- **(d)** STL 분해 도식: 위 = 사이클별 방전 곡선(cycle 1 → cycle i),
  아래 좌 = `Trend` → `trend_mean`(사이클수에 대해 단조 하강하는 점열),
  아래 우 = `Seasonality` → `seasonality_area`(사이클이 갈수록 커지는 음영 면적).
- **(e)(f)(g)** 누적 막대 3장. 패널 제목은 각각 **`NMC|Li`**, **`NMC|Gr`**,
  **`LFP|Gr (fast-charging)`**. x = `Training data` 에 F₁…F₆, y = `Counts`
  (e,f 는 0–45, g 는 0–180). 색: 아래(파랑)=seasonality area 지배,
  가운데(연회색)=혼합, 위(황갈색)=trend 지배 — 캡션의 색 정의와 대조하면
  캡션은 "Blue = seasonal area dominance, yellow = trend dominance, green =
  mixed" 라 적는다.
  `[도표]` 대략 읽은 값: (e) NMC\|Li 는 F₄–F₆ 로 갈수록 파랑 막대가 8→5 수준
  으로 줄고 황갈색이 커진다 (본문의 "후기에 trend mean 이 지배" 와 방향 일치).
  (f) NMC\|Gr 은 F₁–F₃ 에서 파랑이 34–38 로 압도적이고 F₄–F₅ 에서 15 로
  급감했다가 F₆ 에서 23 으로 회복. (g) LFP\|Gr 은 F₂ 에서 파랑 ~115 로 최대,
  F₄–F₅ 에서 ~60 으로 감소.

**★ 본문·캡션과 그림이 어긋나는 지점 (1)**: 캡션은
> "(c) Cycle life plotted as a function of the variance of ΔQ100–10 (V) on a
> log–log axis, **with a correlation coefficient of −0.93**."

라고 인쇄하는데, **재수록된 그림 패널 안에는 `ρ = −0.92` 가 인쇄돼 있다.**
(400 dpi 로 다시 잘라 확대해 확인했다.) 0.01 차이이며 결론에 영향은 없지만,
**이 리뷰를 인용해 "−0.93" 을 적으면 리뷰 자신의 그림과 어긋난다.** 원전
Severson 2019 를 직접 확인하기 전에는 어느 쪽도 확정하지 말아야 한다.

`[해석]` 사소한 어긋남 (2): 캡션은 (g)를 "MIT batteries" 라 부르는데 그림의
패널 제목은 `LFP|Gr (fast-charging)` 이다. 본문이 MIT 데이터셋 = LFP\|Gr
급속충전이라고 정의했으므로 모순은 아니고 표기 불일치다.
(3) 캡션은 "F1–F6 represent six stages of battery capacity degradation divided
according to different percentages" 라 하지만 그림의 x축 라벨은
`Training data` 다. 축 라벨만 보면 F 가 무엇인지 알 수 없다.

---

## 5. §3 Physics-Informed Machine Learning (p.5–8)

### 5.1 두 갈래

`[인쇄]`

> "This is achieved through two primary strategies: **the sequential integration
> of independent models, and hybridized physics-based (PB) ML models.**
> Sequential approaches leverage synthetic data or parameterized features
> derived from physical models, or adopt residual learning frameworks to ensure
> that inputs conform to physical laws. Hybrid approaches, on the other hand,
> directly embed physical constraints into model architecture and/or loss
> function."

### 5.2 §3.1 Sequential — 물리모델로 데이터를 **만든다**

`[인쇄]` 인용 사례:

| 문헌 | 방법 | 성능 |
|---|---|---|
| **Li et al. [92]** | **P2D** + 열모델(electrochemical-thermal)로 온도·부하 프로파일별 대규모 데이터 생성 → DNN 상태추정 | (미인쇄) |
| **Tian et al. [93]** (*Energy Stor. Mater.* 2024, 67, 103270) | 경량 **V-Q(voltage-capacity) 모델**로 충전곡선 모사. 곡선을 **IC peak 개수 + 각 peak 의 면적·위치·폭** 4종 파라미터로 변환 → 보간으로 합성 데이터 → DNN + transfer learning | 용량 추정 **RMSE < 12.42 mAh** |
| **Tian et al. [94]** | 같은 V-Q 저차원 파라미터를 **RUL 예측의 해석 가능 feature** 로 직접 사용, 단일 사이클 데이터 | **RMSE 11.42 mAh** |
| **Lin et al. [96]** | EIS → **ECM** 에서 R_ohm, R_SEI, R_CT 추출 → 용량추정 모델의 추가 입력. physical regularization + multi-task learning | (미인쇄) |

`[인쇄]` sequential 의 한계:

> "Although physics-informed data augmentation and parameter learning methods
> provide strong support for the physical consistency of models, **the
> dependence on the physical model accuracy makes it difficult to correct for
> the model's systematic biases.**"

→ 그 대응이 **residual modeling**: Feng et al. [97] (간이 electrochemical-thermal
+ NN 잔차 보정 + unscented Kalman filter), Cui et al. [98] (thermoelectric
모델 + attention + DNN, 사이클 스케일 오차와 전압 수준 오차를 나눠 보정).

### 5.3 §3.2 Hybrid — 구조에 심거나 손실에 심는다

`[인쇄]` 사례:
- **Nascimento et al. [99]**: 축소차수 물리모델을 **RNN 셀 안에** 심는다.
- **Huang et al. [100]**: **physics-informed autoencoder** — 디코더에 도메인
  지식으로 만든 feature term layer 를 두어 잠재변수가 물리적 의미를 갖는
  health indicator 가 되게 한다.
- **Navidi et al. [102]** (*Energy Stor. Mater.* 2024, 68, 103343): 손실함수에
  물리 항 2개 추가 — "to minimize the discrepancies between the predicted and
  **true values of battery capacity, lithium inventory, and dQ/dV curves**".
- **Tang et al. [103]**: V-Q 곡선 예측용 physics-informed loss.
- **Ye et al. [104]**: **IC 곡선 peak 과 SOH 의 단조 관계**를 물리 제약으로
  손실에 넣는다.
- **Wang et al. [95]** (*Nat. Commun.* 2024, 15, 4332): PINN. 손실 =
  data loss + monotonicity loss + degradation-equation constraint loss.

`[해석]` **★ [102] 는 이 리뷰에서 전극 수준 양(lithium inventory)이 "true
value" 를 갖는 것으로 등장하는 유일한 자리다.** 그런데 리뷰는 그 "true value"
가 어디서 오는지 (측정인가, half-cell fitting 인가, 물리모델 시뮬레이션인가)
한 마디도 적지 않는다. 우리 축에서 이 문장은 **가장 날카로운 후속 확인
지점**이다 — 손실함수에 "참 리튬 재고" 와의 불일치를 넣는다는 것은, 그 참값이
식별 가능해야 성립하는 설계이기 때문이다 (§14 후속 후보 1번).

### 5.4 Fig. 4 (**본 그림**)

`[도표]` `fig_4.png` 를 실제로 보고 읽은 것:
- **(a)** IC 곡선(파란 실선)을 세 개의 색칠된 peak(`peak-1` 청록, `peak-2`
  주황, `peak-3` 분홍)으로 분해한 도식. 확대 삽입창에 **peak 하나당 세 개의
  파라미터**가 화살표로 표시돼 있다: **`ω_i`**(폭, 좌우 화살표),
  **`A_i`**(면적), **`V_0,i`**(위치, 세로 점선). x = Voltage, y = Incremental
  capacity (눈금 없음 — 개념도).
- **(b)** 흐름도: `Realistic charging curves` → **`Voltage-capacity model`** →
  `Parameter identification` → `Parameter interpolation` → 다시
  `Voltage-capacity model` → `Synthetic charging curves`.
- **(c)** PINN 구조: 상단에 지배식 `∂f(t,x)/∂t = g(t,x,u;θ)`. 좌측
  **`𝓕(·): maps features to SOH`** (입력 x₁…xₙ, t → 은닉층 → 출력 `û`),
  우측 **`𝓖(·): models battery degradation dynamics`** (입력 x, û, û_x, û_t →
  `𝓖(t,x,û,û_t,û_x;Θ)` = `SOH decay rate`). 하단에 세 손실의 전개식이
  인쇄돼 있다:
  - `𝓛_data = Σ_{i=1}^{N} |u^i − û^i|²` (← `True SOH` 로 들어오는 점선 화살표)
  - `𝓛_mono = Σ_{j=1}^{M} Σ_{k=1}^{N_j} ReLU(û^{k+1} − û^k)`
  - `𝓛_PDE = Σ_{i=1}^{N} |û_t^i − 𝓖(t^i, x^i, û^i, û_t^i, û_x^i; Θ)|²`

`[해석]` **(b) 의 상자 하나가 문자 그대로 `Parameter identification` 이다.**
즉 이 분야는 "파라미터 식별" 이라는 **말**은 쓰지만, 그 식별이 유일한지를
묻는 절차(`identifiability`)는 리뷰 전체에 없다 (§9). 그리고 (a) 의
파라미터화 — peak 당 (면적, 위치, 폭) 3개 × peak 개수 — 는
[[birkl-ocv-degradation-diagnostic]] §6.1 의 5상 OCV 모델(상당 (E₀, Δx, a)
3개 × 5상 = 15개) 과 **구조가 놀랍도록 같다**. 두 문헌 모두 다중 peak/상
분해를 쓰고, 두 문헌 모두 그 파라미터들 사이의 상관을 보고하지 않는다.

`[해석]` `𝓛_mono` 의 `ReLU(û^{k+1} − û^k)` 는 SOH 가 증가하는 것만 벌하는
**단조 감소 제약**이다. 이는 우리 쪽 관심사인 "제약을 더해 자유도를 줄이는"
접근의 ML 판본이며, Birkl 의 컷오프 등식(Eq. 11–12)이 하는 일과 **철학이
같다** — 다만 여기서는 제약이 *해의 유일성*이 아니라 *궤적의 물리적 타당성*
을 위해 도입된다.

---

## 6. §4 Physics-Inspired Feature Engineering ★★ 의뢰 3항 (p.8–11)

**우리 축에서 가장 중요한 절이다.** 세미나 p.4 가 인용한 개념이 여기 있다.

### 6.0 정의

`[인쇄]`

> "Besides embedding physics constraints into the ML models, integrating
> physical knowledge into the feature design process, known as physics-inspired
> feature engineering, offers another effective pathway to enhance
> interpretability and predictive performance. With the inclusion of domain
> knowledge or insights inspired from experiments, these features not only
> ensure the predictive power of the model, but also **allow for indirect
> understanding of the connection between the battery behaviors and specific
> internal processes.** In practice, physics-informed features are often
> extracted from **charge/discharge curves, IC/differential voltage (DV)
> curves, relaxation behavior, and EIS data.**"

→ 하위 4절이 정확히 그 네 가지다.

### 6.1 §4.1 충·방전 곡선 유래

| 문헌 | feature (정의된 대로) | 물리 귀속 (리뷰가 적은 대로) | 예측 대상 / 성능 |
|---|---|---|---|
| **Lin et al. [105]** | 단시간 충전 구간에서 HI 3종: ① **충전 시간** ② 전압 분포의 **편차** ③ 전압 분포의 **왜도(skewness)** | ① 용량 및 **LAM** 같은 내부 열화 기구 ②③ 내부저항의 누적 효과 | 용량, 반지도학습, 평균 **RMSE 0.55%** |
| **Tao et al. [106]** (*EES* 2025, 18, 1544) | **9-step 충전 프로토콜**에서 prior-cycling feature(초기 제조 편차) + in-cycling **열역학·동역학 파라미터** | 전압 손실을 **열역학 유래 ΔE** 와 **동역학 유래 η** 로 분해 (Fig. 5a) | 열화 예측 평균 정확도 **95.1%**, 이력 데이터의 **첫 4%** 만 사용, 다양한 온도에서 material-agnostic |
| **Liu et al. [107]** (*Angew.* 2022, 61, 202214037) | **Li–S** 방전곡선을 폴리설파이드 상전이에 맞춰 **3구간**으로 자르고 각 구간에 STL → 동적 feature 3종. 정적 feature 로 **N/P ratio** | 구간 = 리튬 폴리설파이드 상 진화 | 수명, LSTM(고/저 N/P 별도 학습), 저 N/P 셀 test **MAPE 8.9%** |

`[인쇄]` [107] 의 흥미로운 관찰:

> "they … found that **batteries with different N/P ratios exhibit disparity in
> correlation behaviors. It is therefore hypothesized that distinctive
> degradation mechanisms dominated in batteries with different N/P ratios.**"

`[해석]` 이것은 리뷰 전체에서 **"같은 feature 가 조건에 따라 다른 방향/세기로
움직인다"** 를 인정한 거의 유일한 자리다. 대응은 **셀을 두 군으로 나눠 각각
모델을 학습**하는 것 — 즉 feature 의 조건 의존성을 *진단*하지 않고 *분할*로
우회한다. `[해석]` 우리 [[mode-observability]] Phase 1 이 관측한 "PVS 의
부호 구조가 동작점(pristine vs 22p)에 따라 달라진다" 와 형태가 같은 문제이며,
문헌의 표준 대응이 "군을 나눈다" 라는 것을 알아 둘 만하다.

### 6.2 §4.2 IC / DV 곡선 유래 ★ PVS 의 가족

`[인쇄]` 왜 IC/DV 인가:

> "IC and DV are widely recognized as powerful, **non-destructive diagnostic
> tools for probing internal battery mechanisms, since they convert voltage
> plateaus into distinct peaks and valleys that reflect electrochemical
> signatures related to cell aging, such as phase transitions and lithium
> inventory loss.**"

| 문헌 | feature | 물리 귀속 | 예측 대상 / 성능 |
|---|---|---|---|
| **Kim et al. [108]** (*ACS Energy Lett.* 2023, 8, 2946) | **DV 프로파일의 peak intensity** (단일 변수!) | **흑연 음극으로의 리튬 삽입 불균일성(heterogeneity)** | cycle life, **첫 사이클 전압 프로파일만**으로 **MAPE 13.5%** |
| **Wei et al. [112]** | 약간의 **과충전** 조건에서 측정한 IC 곡선의 **두 주요 peak 의 면적·높이·위치** | 한 peak → **LAM**, 다른 peak → **LLI**(과충전 사이클링 중) | 용량 추정, 최대 상대오차 **< 2%** |
| **Rhyu et al. [113]** (*Joule* 2025, 9, 101884) | **형성(formation) 공정** 중의 dQ/dV, d²Q/dV² 관련 feature 를 **자동 생성** (`Q(V)`) | 온도 민감도, 미시적 입자 저항 **불균일성** | cycle life, **MAPE 9.2%** |
| **Lin et al. [109]** | IC 주 peak 근처 **0.1 V 부분충전 구간**의 두 시퀀스: 등간격 전압-시간, 등간격 시간-전압 | IC·DV 곡선 아래 단위 면적의 국소 변화 | LSTM, **MAPE 0.91%** |
| **Wang et al. [116]** | 지배적 IC peak 주변의 **무작위 100초 전압 구간** | (물리 귀속 서술 없음) | 용량, transfer learning DNN |

`[해석]` **★ 세미나의 PVS 가 앉는 자리**: PVS(= ICA 2번 peak 과 2번 valley 를
잇는 **할선의 기울기**)는 이 표의 **[108] 과 [112] 사이**에 정확히 들어간다 —
[108] 은 DV peak 의 **높이 하나**, [112] 는 IC peak 의 **면적·높이·위치**,
PVS 는 **peak 과 valley 를 함께 쓰는 2점 기울기**다. 즉 PVS 는 이 리뷰의
분류에서 새로운 종류가 아니라 **§4.2 의 표준 계보 안에 있는 변형**이다.
다만 **peak 과 valley 를 **서로 다른 전극**에 귀속시키고 그 대비를 재는**
설계(PVS: peak2 = PE 상전이, valley2 = NE stage-2)는 이 표의 어느 사례에도
없다 — 리뷰의 사례들은 모두 **하나의 형상 특징을 하나의 기구**에 귀속시킨다.
`[해석]` 이것은 세미나 feature 의 **독창적인 부분**이지만, 동시에 §9 에서
보듯 리뷰가 그런 "두 전극의 대비" feature 의 식별력에 대해 아무 지침도 주지
않는다는 뜻이기도 하다.

`[해석]` **SEV 는 이 리뷰의 어느 절에도 딱 맞지 않는다.** SEV(전류 차단 후
1초 시점의 전압 강하를 SOC 마다 재고 EOC 값을 min–max 스케일)는 §4.3
(relaxation curves) 의 측정 방식과 §4.4 (EIS/DRT 의 R_ct 귀속) 의 물리 해석을
**절반씩** 쓴다. 리뷰에 "current interruption" 이라는 범주는 없다.

### 6.3 §4.3 완화(relaxation) 곡선 유래 ★ SEV 의 이웃

`[인쇄]` 이 절의 전제:

> "Other than formulating features from the readily available data such as
> charging or discharging voltage curves, **supplementary experiments can also
> be conducted** to provide extra data for engineering features that contain
> additional information of the battery internal processes."

| 문헌 | feature | 물리 귀속 | 성능 |
|---|---|---|---|
| **Zhu et al. [118]** (*Nat. Commun.* 2022, 13, 2261) | 완화 전압 곡선의 형상·위치를 나타내는 **통계 feature 6종**; 최적 조합은 **분산 + 왜도 + 최대 완화전압** | (형상 통계 — 개별 기구 귀속 없음) | XGBoost, 단일 데이터셋 **RMSE 1.1%** |
| **Fan et al. [119]** | **10초** 완화 전압만 | 열화가 이온·전자 수송 특성에 미치는 영향이 완화 전압에 나타난다 | CNN, test **MAPE 1.8%** |
| **Tong et al. [120]** | **P2D** 로 분극 회복 중 전해질 농도 분포 모사 → 완화 시간·상태 등 stress factor | 완화 시간이 길수록 입자 분포가 균일해져 유리. **micro-Raman + rate 시험**으로 교차확인 | 하이브리드 앙상블, 용량 추정 **MAE < 1%** |

`[해석]` **세 사례 모두 target 이 용량/SOH 이고, 완화 feature 를 특정 전극의
저항에 귀속시키지 않는다.** 세미나의 SEV 는 DRT 로 **R_ct,PE** 에 귀속시키는데
(concept: [[pvs-sev-degradation-mode-features]]), 그런 **전극 특정 귀속**을
가진 완화 feature 는 이 리뷰에 없다. [120] 만이 P2D 시뮬레이션으로 물리를
확인하며, 이는 세미나 p.8 의 P2D 단독 모드 스윕과 방법론적으로 같은 종류다.

### 6.4 §4.4 EIS 유래

| 문헌 | feature | 물리 귀속 | 성능 |
|---|---|---|---|
| **Su et al. [123]** | 저주파 EIS 에서 HI 3종: **Warburg factor**, **pseudo-Li⁺ 확산계수**, **pseudo-Li⁺ 확산 상태** | 내부 전기화학 동역학 ↔ 외부 노화 특성의 연결 | GPR, **R² = 0.95** |
| **Li et al. [125]** | 전체 EIS 를 ECM 에 fitting 해 파라미터 추출. 저주파에서 SEI 양면의 전하 축적을 발견 → **커패시터 성분 추가** | SEI 계면 축전 | (미인쇄) |
| **Zhang et al. [110]** | **저·중주파만** 쓰는 간이 ECM → HI 3종 | 저주파 = **전하전달 저항** 변화, 중주파 = 계면 반응·확산 | GRU, 예측오차 **< 2%** |
| **Su et al. [127]** | **DRT** peak/valley 의 변화 추세 → 비분극 과정 파라미터 · 분극 과정 파라미터 · DRT 곡선 파라미터 **3군**. **weighted PCA** 로 대표 feature 선별 | "**DRT peak/valley 의 변화가 LLI 와 LAM 이 야기한 전하전달 저항 증가와 나란하다**" | SOH, **RMSE < 0.873%** |

`[해석]` **[127] 이 리뷰에서 LLI·LAM 이 feature 물리 귀속에 쓰인 두 번째이자
마지막 자리다.** 그런데 문장 구조를 보면 "LLI 와 LAM 이 R_ct 를 올린다" 는
**한 방향**만 말한다 — 두 모드가 R_ct 를 **같은 방향**으로 민다는 서술이며,
따라서 그것만으로는 두 모드를 **가를 수 없다**. `[해석]` 이것은 우리
[[pvs-sev-lli-lampe-separability]] 의 H1(두 feature 가 같은 하나의 대비만
잰다)과 **정확히 같은 형태의 문제**가 문헌 안에 이미 인쇄돼 있다는 뜻이다.
리뷰는 이 함의를 언급하지 않는다.

### 6.5 Fig. 5 (**본 그림**) ★ 이번 흡수에서 가장 값어치 있는 그림

`[도표]` `fig_5.png` 를 실제로 보고 읽은 것:

- **(a)** [106] 의 개념도. y = `Applied current (I)`, x = `Electrode voltage
  offset` (`0 Theoretical` → `Actual`). 배경이 좌측 **연청색 = Thermodynamics**
  / 우측 **연분홍 = Kinetics** 로 나뉜다. 세로 점선 `I = 0`. 검은 곡선(초기)과
  회색 곡선(노화 후)이 그려지고 상단에 `Aging` 진행 방향 화살표(검정→흰색
  그라데이션). **좌측 양방향 화살표 = `ΔE`** (열역학 유래 전압손실, "Intrinsic
  properties" 라벨이 세로로 붙어 있다), **우측 양방향 화살표 = `η`** (동역학
  유래). 삽화로 좌측에 층상 결정구조(적/녹/청 구), 우측에 Li⁺ 이온이 표면에
  붙는 그림.
- **(b)** [107] 의 Li–S. 좌: 방전곡선 (y = Voltage 1.6–2.4 V, x = Normalized
  capacity 0–1) 을 **I / II / III** 세 구간으로 색칠(연녹/노랑/연분홍).
  우: 각 구간 feature 대 capacity retention 산점도 3개, 각각
  **Correlation: −0.94 (Feature_TS1, 0.4–0.8 V) / −0.95 (Feature_TS2,
  0.22–0.26 V) / −0.96 (Feature_TS3, 0.04–0.08 V)**. y = Capacity retention
  0.8–1.0, 회색 점선 = 0.8 기준선.
- **(c)** [108] 의 DV 곡선. y = **`dV dQ⁻¹ (V Ah⁻¹)`** 0–0.6, x = `Capacity
  (Ah)` 0–1.0. **파란 곡선 = Homogeneous cell**, **분홍 곡선 = Heterogeneous
  cell**. 초록 점선 사각형이 0.28–0.68 Ah 구간을 감싸고, 그 안에서 **peak
  꼭대기와 인접 valley 바닥 사이를 잇는 세로 양방향 화살표 2개**(파랑·분홍)가
  각각의 셀에 대해 그려져 있다. `[도표]` 눈으로 읽으면 파란(균질) 셀의
  peak≈0.24, valley≈0.05 → 높이 ≈0.19; 분홍(비균질) 셀의 peak≈0.19,
  valley≈0.07 → 높이 ≈0.12. **즉 "peak intensity" 는 사실상 peak−valley 진폭
  으로 측정된다.**
- **(d)** [109]. y = `dQ/dV (Ah/V)` 0–4 남짓, x = `Voltage (V)` 3.0–4.2.
  여러 사이클의 IC 곡선이 짙은 남색→하늘색→붉은색으로 겹쳐 있고 (노화 진행),
  주 peak(≈3.7 V, 높이 ≈4.2 → ≈3.1 로 감소)의 오른쪽 어깨에 **3.7–3.8 V
  세로 띠**가 음영으로 표시돼 있다 (= 선택된 0.1 V 구간). 두 번째 peak 는
  ≈4.0 V.
- **(e)** [110]. Nyquist. x = `Z_Re (mΩ)` 0–2.5, y = `Z_Im (mΩ)` −0.1–0.7.
  **Cycle 1(주황)→Cycle 350(파랑)** 컬러바. 빨간 화살표 3개로
  `High frequency impedance variation amplitude`(좌하, 짧은 가로 화살표),
  `Medium frequency impedance variation amplitude`(중앙, 우상향),
  `Low frequency impedance variation amplitude`(우상, 우상향)를 표시.
  노화가 진행되며 반원이 우측으로 밀리고 커진다.

`[해석]` **★ (a) 는 우리 프로젝트에 직결된다.** [106] 의 ΔE/η 분해는
**"전압 손실을 열역학 성분과 동역학 성분으로 나눈다"** 는 것이고, 이는 세미나가
PVS(열역학, OCV 형상)와 SEV(동역학, R_ct)로 관측을 나눈 것과 **동일한 설계
철학**이다. 리뷰는 이 두 성분이 **서로 다른 열화 모드를 가르는가**는 묻지
않는다 — 단지 "다차원 화학 과정을 효과적으로 decouple 했다" 고만 적는다
(`[인쇄]`: "These material-agnostic features, which effectively decoupled
battery internal dynamics and thermodynamics (Figure 5a)"). **"decoupled" 는
이 리뷰가 우리 축에 가장 가까이 간 단어이지만, 그 근거로 제시된 것은 그림
5a 의 개념도 하나뿐이고 정량적 분리 가능성 진단은 없다.**

`[해석]` **★ (c) 는 PVS 의 문헌적 선례다.** [108] 의 "peak intensity" 가
실제로는 **peak−valley 진폭**이라는 것은 캡션("The proposed peak intensity of
DV curve as a descriptor")만으로는 알 수 없고 **그림을 봐야 알 수 있다**.
PVS 는 여기에 **분모(전압 간격)** 를 더해 기울기로 만든 것에 해당한다. 그리고
[108] 이 이 진폭에 귀속시키는 물리는 **"흑연 음극으로의 리튬 삽입 불균일성"**
— 즉 **음극 단일 귀속**이다. 세미나의 PVS 는 같은 형태의 양을 **양극 peak 과
음극 valley 의 대비**로 해석한다. **같은 기하학적 양에 대해 두 문헌이 다른
물리 귀속을 준다** — 이것은 PVS 의 물리 해석이 자명하지 않다는 직접 증거다.

---

## 7. §5 Post-Hoc Analysis (p.11–14)

### 7.1 분류

`[인쇄]` model-agnostic (SHAP, PDP, ALE) vs model-specific (LRP, saliency map,
attention mechanism). 리뷰는 후자를 §5.2 에서 다루며 표기가 **`LPR` 과 `LRP`
사이에서 흔들린다** (절 제목은 `5.2.1. LPR`, 본문은 `LRP`, Fig. 6 캡션은
`LPR`/`Layer-wise relevance propagation` 혼용). `[해석]` 정본은
layer-wise relevance propagation = **LRP** 다.

### 7.2 SHAP 사례

| 문헌 | 데이터·설계 | 결론 |
|---|---|---|
| **Geslin et al. [130]** (*Nat. Energy* 2025, 10, 172) | 동적 방전 프로토콜이 상용 SiOx-graphite / NCA 셀 수명을 CC 대비 **최대 38%** 연장 | SHAP: 저주파 펄스, peak 방전 전류, 시간 유발 노화가 최대 기여 |
| **Sun et al. [131]** | **열폭주** 반응의 3단계(개시·진행·peak)별 mean SHAP | 초기는 내재적 물성이, 후기는 외부 환경이 지배 |
| **Cui et al. [132]** (*Joule* 2024, 8, 3072) | LIB **186개**, 서로 다른 **formation 프로토콜 62종** | 형성 단계의 **높은 충전전류·높은 온도**가 장기 안정성의 최대 인자. 기구: 고전류 급속 형성이 **electrode-specific utilization range 를 바꾸어** PE 가 동역학적 제약 영역에 들어가는 것을 막고 NE 도금 위험을 낮춘다. 고온은 안정한 SEI 형성 경로 |
| **Xia et al. [134]** | SHAP 로 SOH 예측에 중요한 **임피던스 스펙트럼 구역**을 골라 입력을 제한 | 정확도 ↑ + EIS 측정시간 ↓ |
| **Zhao et al. [135]** | CNN-LSTM. SHAP 상 중요 feature 가 **2.9–3.2 V** 에 집중 | 입력을 그 구간으로 제한해도 정밀도 유지, 계산효율 대폭 개선 |

`[해석]` **[132] 는 이 리뷰에서 전극 수준 물리(전극별 이용 구간)가 결론으로
등장하는 유일한 사례**인데, 그것은 **예측된 것이 아니라 SHAP 결과를 보고 뒤에
추가 조사해 얻은 기구 설명**이다 (`[인쇄]`: "Guided by this SHAP-derived
insight, the study **further investigated** the mechanisms through which these
factors influence battery performance"). 즉 전극 수준 양은 이 리뷰 안에서
**한 번도 모델의 출력이 아니다**.

`[해석]` **입력이 프로토콜 식별자인 사례가 둘 있다** ([130] 방전 프로토콜
파라미터, [132] formation 프로토콜 파라미터). 리뷰는 이것을 문제로 보지 않는다
— 오히려 목표가 "어떤 프로토콜 인자가 수명을 정하는가" 이므로 그 설계에서는
정당하다. **다만 target 이 전극 수준 열화량인 경우(세미나 p.13)에는 같은
입력이 근본적으로 다른 위험을 만든다** — 이 구분을 리뷰는 하지 않는다.

### 7.3 SHAP 의 한계 — 리뷰가 공선성을 언급하는 유일한 자리 중 하나

`[인쇄]` 전문:

> "However, SHAP also exhibits several limitations that warrant careful
> consideration. First, the use of simplified methods, **combined with potential
> feature collinearity may lead to inaccurate attribution of feature
> importance.** Second, SHAP explanations heavily rely on the structure and
> behavior of the established model, therefore, the results may inherit the
> inherent model bias. **As there is no universally accepted ground truth for
> feature importance**, SHAP-based interpretations should be validated through
> experimental evidence or domain-specific physical knowledge to ensure their
> reliability."

`[인쇄]` PDP 의 한계:

> "**PDP can be unreliable when the predictors are highly correlated.** In this
> case, the ALE plot that calculates predicted differences by using the
> conditional distribution of features might be adopted. For example, **given
> the noticeable correlation between features**, ALE was adopted by Li et al.
> to investigate … driving condition parameters (DCPs) …"

`[해석]` **이것이 이 리뷰가 feature 간 상관을 문제로 인식하는 전부다.** 그리고
그 인식의 성격은 **"상관이 있으면 *해석 도구*(SHAP/PDP)의 귀속이 틀린다"**
이지, **"상관이 있으면 *feature 집합이 target 을 결정하지 못한다*"** 가
아니다. 두 진술은 다르다. 앞의 것은 사후 설명의 신뢰도 문제이고, 뒤의 것은
역문제의 적절성 문제다. **리뷰는 앞의 것만 안다.**

### 7.4 model-specific 사례와 Fig. 6·7 (**본 그림**)

`[도표]` `fig_6.png`:
- **(a)** [131] Sankey 도식. 좌→우 세 열이
  `Onset temperatrue`(원문 오식, = temperature) → `Peak temperature` →
  `Max power` 이고, 하단에 `Thermal Runaway Reaction` 진행 화살표.
  각 띠에 mean(|SHAP|) 비율이 % 로 인쇄돼 있다. `[도표]` 첫 열 위→아래:
  **14.8 / 12.5 / 10.9 / 9.1 / 8.7 / 8.7 / 5.0 / 4.1%**. 셋째 열:
  **18.1 / 15.1 / 13.0 / 7.6 / 7.1 / 6.3 / 4.2 / 3.8 / 3.4%**.
  범례 9종: Cutoff voltage · DSC scanning speed · Active substance ratio ·
  Electrolyte content · Electrolyte composition · Pristine Li content ·
  Ni content · Co content · Mn content · Radii-TM std (wt.).
- **(b)** [132] SHAP 히트맵. **행(입력) = `CC₂`, `V_transition`, `CC₁`, `T`**
  (전부 formation 프로토콜 파라미터), **열(target) = `Q_ch`, `Q_disch`,
  `RPT Q_C/20`, `Q_3C/4`, `ΔR_100%SOC,10s`, `Knee`, `Cycle life`,
  `Energy Throughput`** — 위에 `Formation` / `Cycling` / `EOL` 구간 표시.
  컬러바 `Mean |SHAP Value|` **0.00–0.12**. 마지막 두 열(Cycle life, Energy
  Throughput)이 하늘색 점선 상자로 강조돼 있다. `[도표]` 가장 진한 칸은
  `CC₂ × Q_ch` (≈0.12) 와 `CC₁` 행 전반.
- **(c)** [144] LRP 상대 중요도의 **에폭별 궤적** (x = Number of Epochs
  0–10000, y = Relative Importance 0–1). 6개 곡선이 초기 2000 에폭까지 크게
  요동하고 (빨간 곡선은 ~1400 에폭에서 0 으로 떨어져 유지), 7500–10000 구간이
  **노란 음영**으로 표시돼 있다.
- **(d)** [144] 최종 relevance score 막대. y 축 위→아래 `HI8`(≈+0.125),
  `HI7`(≈+0.22), `HI6`(≈+0.205), **`Tmax`(≈−0.065, 유일한 음수)**,
  `CT`(≈+0.115), `IR`(≈+0.07). x = Relevance Score −0.05–0.20.

`[해석]` **(c)/(d) 의 캡션 불일치 (경미)**: 캡션은 "(d) the finalized relevance
score at **Epoch 7500**" 이라 하는데, (c) 의 x축은 10000 까지 가고 강조된
노란 구간이 7500–10000 이다. 7500 이 "수렴 시작점" 인지 "판독 시점" 인지
캡션만으로는 애매하다.

`[해석]` **(d) 에서 `Tmax` 만 음의 relevance 를 갖는데 본문은 이를 언급하지
않는다.** 본문은 "impedance-related features 의 기여가 가장 컸다" 만 적는다.
그림에서 가장 큰 세 막대는 HI7 > HI6 > HI8 이고 이들이 무엇인지는 캡션에도
본문에도 없다 (원전 [144] 를 봐야 한다).

`[도표]` `fig_7.png` ([154], SELF 프레임워크):
- **(a)** 원형 개념도. 중앙 = ML(머리 아이콘). 바깥 고리 = 다양한 cathode/
  electrolyte 화학(NMC, S/Li₂S, Electrolyte, Li metal anode). 안쪽 4모듈:
  **Prognosis module**(Q–CN 곡선 + KP), **Diagnosis module**(saliency map),
  **Descriptor module**(KP 대 D 산점도, "Simplified quantification"),
  **Experimental guidance**(방전 프로토콜 개선). 하단에 `SELF: Sequential
  Explainable Learning Framework`.
- **(b)(c)** 각각 Li\|NMC 2셀, Li\|S 2셀의 **방전 전압 곡선**(cycle 1–10 컬러바)
  위에 saliency 기여도를 배경 음영(베이지→청록)으로 겹쳐 그림. y 축은
  각각 2.8–4.3 V, 1.8–2.4 V. x = Normalized capacity 0–1. **음영이 진한 곳이
  오른쪽 끝(용량 0.9–1.0)에 몰려 있다.**
- **(d)(e)** y = `KP`(20–55), x = `Normalized capacity` 0–1 인 히트맵.
  컬러바 `Normalized contribution` 0.0–1.0. 회색 점선이 "기여도가 0.2 를
  넘기 시작하는 지점" 을 표시. **(d) Li\|NMC 는 거의 전 영역이 옅고 오른쪽
  끝(≈0.97)에서만 진해진다. (e) Li\|S 는 KP 가 작을수록(≈20) 점선이 왼쪽
  (≈0.28)까지 밀리며 넓은 영역이 진해진다.**

`[해석]` 캡션은 (b)(c)를 "The saliency map of two types of batteries" 라고
부르지만, 그림이 실제로 보여 주는 것은 **방전 곡선 + 배경 음영**이다.
saliency 자체의 정량 히트맵은 (d)(e)다. 표기의 느슨함이며 내용 오류는 아니다.

`[인쇄]` [154] 의 결론 — **post-hoc 해석에서 새 descriptor 를 만드는 고리**:

> "Saliency analysis revealed that **the final 10% of the discharge curve was
> the most influential** to the model's predictions … a universal descriptor
> (**AV100**) applicable across different LMBs, obtained from areal variation of
> the last 10% discharge curves from the first 10 cycles, was proposed. This
> descriptor was shown to correlate negatively with the KP … a **voltage and
> capacity dual-cutoff discharge protocol** was developed to prevent the cell
> from entering high-DoD regions … **extending the cycle life of battery up to
> 2.8 times** compared to the conventional constant-current protocol."

`[해석]` 이 사례가 리뷰에서 가장 완결적인 고리다: 사후 해석 → 새 물리 feature
→ 프로토콜 설계 변경 → 실측 개선(2.8배). **우리 프로젝트가 참고할 만한
"해석 가능성이 실제로 값을 만든" 유일한 완전 사례**이며, 주목할 점은 그 값이
**예측 정확도가 아니라 설계 개입**에서 나왔다는 것이다.

---

## 8. §6 Summary and Outlook — 저자들의 prospect ★ 의뢰 5항 (p.14–16)

### 8.1 두 가지 이득 (opportunities)

`[인쇄]` 요약:
1. **Enhance model development** — "by analyzing how exactly certain prediction
   is made, researchers can easily debug abnormal predictions. And by
   supervising the model training process, the robustness and accuracy of the
   model can be further ensured." 실행 방안으로 **해석 도구를 개발
   워크플로에 넣기**, **공유 벤치마크 데이터셋과 도메인 특화 해석 도구 제작**.
2. **Enhance scientific discovery** — "revealing hidden correlations and
   supplying new insights … **This might be the primary motivation of leveraging
   interpretable ML for prognosing novel battery systems with internal
   mechanisms not fully understood**."

`[인쇄]` 실행 경로(roadmap) 4가지: ① 전기화학 원리를 학습모델에 심기,
② **다중모드·이종 데이터 통합**(전기화학 신호 + 이미징 + 분광 + 시뮬레이션),
③ 해석 모듈을 **실시간 digital twin** 에 결합, ④ 표준 데이터셋·벤치마킹
프로토콜·도메인 해석 지표의 확립.

### 8.2 세 가지 미해결 challenge

`[인쇄]` **(1) Limited depth and scalability of current interpretable methods**

> "Simply understanding the factor that is the most influential to prediction
> results might not be sufficient, and **how to squeeze more useful information
> from the model and from the predictions remains an open question.**
> Furthermore, **many current interpretation methods are rather local**, where
> the insights are extracted based on a single training example or from a
> limited data range. To address this, further efforts could focus on developing
> **global interpretability frameworks** that go beyond instance-level
> explanations. … Additionally, **exploring causality-based interpretability
> methods may help move beyond mere correlation** and uncover deeper,
> model-independent mechanisms."

`[인쇄]` **(2) Lack of systematic validation frameworks**

> "Proper ways to validate the interpretations are still lacking. For instance,
> **if some counterintuitive conclusion is drawn, how could one tell if this
> suggests a new finding or an artificial bias introduced by an imperfect
> model?** In this sense, incorporating domain knowledge from experts or
> designing additional experiments is still indispensable … Additionally,
> **statistical hypothesis testing can be applied to evaluate whether identified
> patterns are statistically significant or likely to arise by chance.** In the
> long term, developing a standardized and quantifiable interpretability
> validation framework will be crucial …"

`[인쇄]` **(3) Limited data quality and availability**

> "the ML model that works well on one dataset might perform poorly on another.
> To ensure model reproducibility, demonstrating model performance on a large
> public dataset might be necessary. While there exist a few public datasets
> focusing on commercial LIBs, such as those from **MIT, Oxford, and NASA**,
> establishing more datasets, especially with other novel battery systems such
> as LMBs remains essential. Additionally, **many datasets lack auxiliary
> variables such as cell temperature, impedance, pressure, or real-world cycling
> profiles, which are crucial for drawing physically meaningful
> interpretations.**"

`[도표]` **Fig. 8** (`fig_8.png`, 실제로 봄): 태극 문양(음양) 형태로 좌측
회색 반쪽에 **Opportunies**(원문 오식, = Opportunities), 우측 흰 반쪽에
**Challenges**. 좌측 아이콘 2개 = `Enhance model development`(뇌+회로),
`Enhance scientific discovery`(배터리+톱니). 우측 아이콘 3개 =
`Limited depth and scalability`(돋보기), `Lack of systematic validation
framework`(현미경), `Limited data quality and availability`(DAT 폴더).

`[해석]` **★ 의뢰 5항의 답**: 저자들이 미해결로 두는 세 축은 **해석의 깊이 ·
해석의 검증 · 데이터의 양과 질**이다. **세 축 모두 "해석(interpretation)"
쪽이며, "라벨/target 의 적절성" 축은 없다.** 특히 (2) 는 우리 관심사와
가장 가까워 보이지만, 검증 대상이 "the interpretations"(해석) 이지 "the
labels"(라벨)나 "the inverse problem"(역문제)이 아니다. (3) 이 "많은
데이터셋에 온도·임피던스·압력 같은 보조 변수가 없다" 고 말하는 것은 **관측을
늘리자**는 우리 [[mode-observability]] 의 논지와 방향이 같지만, 리뷰의 동기는
"물리적으로 의미 있는 해석을 위해" 이지 "모드를 가르기 위해" 가 아니다.

---

## 9. ★★★ 식별 가능성·축퇴·불확실성 전수 확인 (의뢰 2항 — 이 digest 의 최중요 산출물)

### 9.1 확인 방법 (재현 가능하게 기록)

PDF 20쪽 전체를 pymupdf 로 텍스트 추출한 뒤, **합자(ligature) 정규화**를 먼저
했다 — 이 PDF 는 `ﬁ ﬂ ﬀ ﬃ ﬄ` 유니코드 합자를 쓰기 때문에 정규화 없이
`identifiab`, `confiden`, `overfit` 을 검색하면 **전부 0 으로 잘못 나온다.**
(실제로 첫 시도에서 그렇게 나왔고, `identiﬁes a unique …` 가 다른 검색에
걸려 오류를 발견했다.) 정규화 후 본문(참고문헌 목록 제외)에서 대소문자 무시
검색한 결과가 아래다.

### 9.2 결과 표 — 본문(p.1–16, 참고문헌 제외) 출현 횟수

| 검색어 | 횟수 | 어디에, 무슨 뜻으로 |
|---|---|---|
| `identifiab`(identifiability/identifiable) | **0** | — |
| `degenerat`(degeneracy/degenerate) | **0** | — |
| `uncertain`(uncertainty/uncertain) | **0** | — |
| `confidence interval` | **0** | — |
| `error bar` | **0** | — |
| `Bayesian` | **0** | — |
| `noise` | **0** | — |
| `ill-posed` / `ill-conditioned` | **0** | — |
| `non-unique` / `multicollinear` | **0** | — |
| `sensitivity analysis` | **0** | — |
| `cross-valid` / `cross validation` / `train/test` / `test set` / `hold-out` | **0** | — |
| `OCV` / `open circuit` / `half-cell` | **0** | — |
| `post-mortem` / `teardown` / `disassembl` | **0** | — |
| `collinear` | **1** | §5.1.1 SHAP 한계: "potential feature collinearity may lead to inaccurate attribution of **feature importance**" |
| `highly correlated` (predictors) | **1** | §5.1.2 PDP 한계: "PDP can be unreliable when the predictors are highly correlated" |
| `ground truth` | **1** | §5.1.1: "there is no universally accepted ground truth for **feature importance**" |
| `uniqu`(unique/uniquely) | **4** | ① §2 "unique advantage of linear regression" ② §2 symbolic regression 이 "identifies a **unique mathematical formula**" ③ §5.2 "unique characteristics of the model" ④ §5.2.1 "unique role of impedance-related features" — **넷 다 역문제의 유일성과 무관하다** |
| `identifi`(identify/identified/identification) | **11** | 전부 "중요 인자를 **찾아냈다**" 또는 Fig. 4b 의 `Parameter identification` 상자. **식별 *가능성*을 논한 자리는 없다** |
| `confiden` | **2** | ① 초록의 수사("increasing confidence in the vast potential") ② §4.1 "strong correlation … **instills confidence** for the physical sanity of the model" — **통계적 신뢰가 아니라 심리적 확신** |
| `overfit` | **3** | PIML 이 과적합을 줄인다(×2), 해석도구가 과적합 위험을 줄인다(×1) |
| `validat` | **12** | 전부 **모델/해석의 타당성 검증**. 라벨 검증은 없다 |
| `causal` | **3** | ① post-hoc 이 "causal reliability" 를 결여 ② Table 1 "Limited causal understanding" ③ §6 challenge 1 "causality-based interpretability methods" |
| `robust` | **7** | 전부 "모델이 조건 변화에 강건하다" 의미 |

### 9.3 결론 — 이 리뷰는 우리 축의 질문을 **묻지 않는다**

`[해석]` 위 표에서 읽을 것은 세 가지다.

1. **"라벨의 불확실성" 은 이 리뷰에 존재하지 않는 범주다.** `uncertainty`
   `noise` `error bar` `confidence interval` `Bayesian` 이 전부 0회다.
   2025년에 나온 *Advanced Energy Materials* 리뷰가 **불확실성이라는 단어를
   단 한 번도 쓰지 않는다**는 것은, 이 분야의 자기 서술에서 UQ 가 아예
   의제가 아니라는 강한 증거다. (인용 문헌 개별에는 UQ 를 다룬 것이 있을 수
   있으나, **리뷰는 그것을 축으로 삼지 않았다.**)

2. **상관/공선성은 "해석 도구의 신뢰도" 문제로만 등장한다.** §5.1.1 과
   §5.1.2 두 곳뿐이고, 둘 다 SHAP·PDP 라는 **사후 귀속 도구**의 한계다.
   "feature 가 공선이면 **모델의 예측 자체**가 target 을 결정하지 못할 수
   있다" 는 진술은 없다. **feature 설계 단계(§4)에는 공선성 논의가 0이다.**

3. **`identification` 이라는 말은 쓰지만 `identifiability` 는 없다.** Fig. 4b
   에는 `Parameter identification` 이라는 상자가 그려져 있고 (§5.4), 본문은
   "가장 영향력 있는 인자를 identify 했다" 를 11번 말한다. **식별을 수행하는
   언어는 풍부하고, 식별이 가능한지 묻는 언어는 없다.**

`[해석]` **이 결과가 우리 질문 카드에 주는 무게**: 세미나의
Gap "라벨 불확실성" 은 (a) 원전 [[birkl-ocv-degradation-diagnostic]] 에서
상속됐고 (2026-09-03 확인), (b) 그 위에 얹히는 **ML 분야 리뷰도 그 공백을
인지하지 못한다.** 즉 이것은 한 연구자·한 발표의 누락이 아니라 **두 계보
(전기화학 진단 / ML 예후)가 만나는 지점의 구조적 공백**이다. 이 공백을 메우는
작업의 참신성은 개별 논문 대비가 아니라 **분야 리뷰 대비**로 평가된다.

---

## 10. prognosis target 의 종류 ★ 의뢰 4항

`[인쇄]` 리뷰가 열거하는 예측 대상 (§1 및 각 절):

- **매크로 상태**: SOH [27–31], **RUL** [32–35], **SOC** [36–40],
  **cycle life** [41,42], 용량(capacity), **knee point (KP)**,
  capacity retention, energy throughput
- **안전/열**: 열폭주의 onset temperature · peak temperature · max power
  ([131]), 배터리 파크의 probe temperature 변동계수 VCPT ([148])
- **제조/형성 결과**: Q_ch, Q_disch, RPT Q_C/20, Q_3C/4, ΔR_100%SOC,10s ([132],
  Fig. 6b)

`[해석]` **전극 수준(LLI / LAM_PE / LAM_NE)을 예측 target 으로 삼는 사례는 이
리뷰에 하나도 없다.** Fig. 1 의 두 패널 모두 Targets 을 `SOH, RUL, SOC…` 로만
적는다. LLI/LAM 이 본문에 등장하는 것은 **총 6회**이며 전부 아래 세 용법이다:

| 위치 | 용법 |
|---|---|
| p.3 ([77] Severson) | **feature 가 왜 작동하는지의 설명** — "LAM of the delithiated negative electrode can result in a shift in discharge voltage" |
| p.8 ([105]) | HI 의 물리 귀속 — 충전 시간이 "LAM 같은 내부 열화 기구" 와 관련 |
| p.8–9 ([112]) | IC peak 2개의 귀속 — 하나는 **LAM**, 다른 하나는 **LLI** |
| p.10 ([127]) | DRT peak/valley 변화가 "**LLI 와 LAM 이 야기한** 전하전달 저항 증가와 나란하다" |
| p.13 ([152] Grad-CAM) | 3.3 V 구역의 중요도가 "**음극의 점진적 활물질 손실**에 대응" |
| p.7 ([102] Navidi) | **유일한 예외** — 손실함수가 "predicted and **true values of** battery capacity, **lithium inventory**, and dQ/dV curves" 의 차이를 최소화 |

`[해석]` 따라서 **의뢰 4항의 답: 이 리뷰는 macro target 만 다룬다.** 전극 수준
양은 (i) 해석의 어휘로, (ii) 단 한 번 손실함수의 제약항으로만 나타나며,
**어느 경우에도 그 값이 어떻게 얻어졌는지(fitting? 해체? 시뮬레이션?)를 리뷰가
적지 않는다.** `[해석]` 2026-09-02 세미나가 하는 일 — 전극 수준 3종을 ML 의
**출력**으로 놓는 것 — 은 이 리뷰가 그리는 지형에서 **빈 칸**이다. 이는
세미나의 참신성을 높이는 동시에, **그 칸이 비어 있는 이유(라벨을 어디서
얻는가)** 가 리뷰의 도움 없이 세미나 스스로 풀어야 할 문제라는 뜻이다.

---

## 11. 우리 프로젝트와의 접점 `[해석]`

### 11.1 이 리뷰가 우리에게 주는 것

1. **좌표계**. PVS·SEV 가 문헌의 어느 칸에 앉는지 확정했다 (§6.2, §6.3):
   PVS = §4.2 IC/DV 계열의 변형([108]·[112] 사이), SEV = §4.3 relaxation 과
   §4.4 EIS/DRT 를 반씩 걸친 것. 리뷰에 **current interruption 범주는
   없다** — SEV 는 분류상 새 자리다.
2. **PVS 의 문헌적 선례와 그 물리 귀속의 불일치** (§6.5): [108] 은 같은
   기하학적 양(DV peak−valley 진폭)을 **음극 단일**(흑연 리튬화 불균일성)에
   귀속시킨다. 세미나는 **양극 peak vs 음극 valley 의 대비**로 읽는다.
   같은 양에 두 개의 다른 물리 이야기가 붙어 있다는 것은,
   [[pvs-sev-lli-lampe-separability]] 가 묻는 "PVS 가 실제로 어느 방향을
   재는가" 가 문헌 수준에서도 미결이라는 뜻이다.
3. **ΔE/η 분해라는 선행 프레임** ([106], Fig. 5a): "열역학 성분과 동역학
   성분으로 전압 손실을 나눈다" 는 설계가 이미 있다. 세미나의 PVS/SEV 조합은
   이 프레임의 특수한 구현이며, 인용할 때 이 계보를 밝히는 것이 정확하다.
4. **"관측을 늘리자" 의 문헌적 지지** (§8.2 challenge 3): 리뷰가 "많은
   데이터셋에 온도·임피던스·압력·실주행 프로파일 같은 **보조 변수가
   없다**" 고 명시한다. [[mode-observability]] 의 전제와 같은 방향이다.
5. **DRT/R_ct 의 동부호 문제** (§6.4 [127]): "LLI 와 LAM 이 **함께** R_ct 를
   올린다" 는 인쇄된 진술은, 임피던스 유래 feature 가 두 모드를 가르지
   못할 수 있다는 우리 H1 과 같은 구조다. **인용 가능한 문헌 근거**다.

### 11.2 우리가 이 리뷰(가 서술하는 분야)에 공급할 수 있는 것

1. **식별 가능성 경계 자체**. §9 가 보였듯 이 분야에는 `identifiability`
   라는 어휘가 없다. [[degradation-degeneracy]] 가 내는 것은 이 리뷰의
   Table 1 "Limitations" 열에 **새 항목을 추가하는 종류의 결과**다 —
   "physics-inspired feature 는 서로 다른 모드에 대해 같은 방향으로 움직일
   수 있고, 그러면 해석 가능성이 있어도 분해 가능성은 없다."
2. **라벨 불확실성의 정량화**. §8.2 challenge 2 가 요구하는 "systematic
   validation framework" 는 *해석*의 검증이지만, 그 앞단에 *라벨*의 검증이
   필요하다는 것을 우리가 보일 수 있다.
3. **합성 truth 기반 진단이라는 방법론**. 리뷰가 나열한 검증 수단은
   "도메인 지식 · 추가 실험 · 통계적 가설검정" 셋이다. **알려진 정답을 가진
   합성 데이터로 역문제를 시험하는 것**은 리뷰의 목록에 없다.

### 11.3 우리가 조심해야 할 것

`[해석]` 이 리뷰를 인용해 **쓸 수 없는** 문장:
- "이 리뷰는 physics-inspired feature 의 식별 가능성 한계를 지적한다" →
  **지적하지 않는다.** 지적하는 것은 전문가 지식 의존과 신규 발견의 어려움뿐.
- "이 리뷰는 라벨 불확실성을 미해결 과제로 든다" → **들지 않는다.**
  challenge 3 은 데이터의 *양과 보조변수*이지 라벨의 *정확도/유일성*이 아니다.
- "이 리뷰는 전극 수준 열화 예측을 다룬다" → **다루지 않는다** (§10).
- "이 리뷰가 ΔQ₁₀₀₋₁₀ 의 상관계수를 −0.93 이라 한다" → 캡션은 −0.93,
  **자신이 재수록한 그림은 −0.92** 다 (§4.2).

---

## 12. 이 digest 를 쓰며 실제로 본 그림 (투명성)

크로핑 산출물은 **그림 8장 + 표 1장 = 9장**이다. 그중 실제로 이미지를 열어
본 것:

| 파일 | 봤나 | 무엇을 얻었나 |
|---|---|---|
| `fig_1.png` | ✅ | 두 워크플로. **(a)(b) 모두 Targets = SOH/RUL/SOC** 확인 — §10 의 핵심 근거. physical knowledge 가 데이터셋에도 꽂힌다는 것은 그림에만 있다 |
| `fig_2.png` | ✅ | 4분류 상자. 3번 상자의 예시가 **dQ/dV + Impedance** 라는 것, PINN 손실식 `𝓛_data+𝓛_mono+𝓛_PDE`, 오식 2건(`intrisic`, `Impedence`) |
| `fig_3.png` | ✅ | Severson 3패널 + STL 도식 + 3화학계 막대. **패널 c 의 `ρ = −0.92` 가 캡션 −0.93 과 불일치** (400 dpi 재확대로 확인) |
| `fig_4.png` | ✅ | IC peak 파라미터 3종(ω, A, V₀), `Parameter identification` 상자, PINN 세 손실의 전개식 |
| `fig_5.png` | ✅ | **이번 흡수 최고 수확**. (a) ΔE/η 열역학–동역학 분해, (c) DV peak intensity 가 실제로는 **peak−valley 진폭**이며 균질/비균질 셀 비교, (b) Li–S 상관 −0.94/−0.95/−0.96, (d) 0.1 V 창의 위치, (e) Nyquist 3주파수대 |
| `fig_6.png` | ✅ | (b) 입력이 **formation 프로토콜 파라미터**(CC₁, CC₂, V_transition, T)라는 것, (d) `Tmax` 만 음의 relevance 인데 본문 미언급 |
| `fig_7.png` | ✅ | SELF 4모듈, saliency 가 **방전 마지막 10%** 에 몰린다는 것, (d)(e) 히트맵. 캡션의 "saliency map" 표기가 (b)(c)에는 느슨함 |
| `fig_8.png` | ✅ | 태극 도식. 기회 2 / 도전 3 항목명 확인, 오식 `Opportunies` |
| `tab_1.png` | ❌ | 표는 PDF 텍스트가 정확하므로 이미지 판독 불필요 (도구 권고). 대신 §3.4 에 텍스트 전문을 옮겼다 |

**본문·캡션과 그림이 어긋난 것** (전부 위 표와 본문에 기록):
1. **Fig. 3c**: 캡션 `−0.93` vs 그림 `ρ = −0.92` ← **유일하게 수치가 다른 건**
2. Fig. 3g: 캡션 "MIT batteries" vs 그림 제목 `LFP|Gr (fast-charging)` (표기)
3. Fig. 3e–g: 캡션은 F₁–F₆ 가 "열화 단계" 라는데 x축 라벨은 `Training data`
4. Fig. 6c/d: 캡션 "at Epoch 7500" vs 그림의 강조 구간 7500–10000 (모호)
5. Fig. 6d: `Tmax` 의 **음수** relevance 를 본문이 언급하지 않음
6. Fig. 7b/c: 캡션은 "saliency map" 이라 부르나 실제로는 방전곡선+음영

`[해석]` 6건 중 **결론에 영향을 주는 것은 없다.** 다만 1번은 이 리뷰를 인용해
숫자를 옮길 때 실제로 걸리는 함정이므로 §11.3 에 인용 금지 목록으로 남겼다.

---

## 13. 비판적 총평 `[해석]`

**이 리뷰가 잘한 것**
- **분류 축이 하나로 일관된다** ("해석 가능성이 어디서 주입되는가"). 4분류가
  임의적이지 않고, 저자들이 이것을 위계가 아니라 도구상자라고 명시한 것도
  정직하다.
- **각 분류의 한계를 반드시 절 말미에 적는다.** 리뷰 논문이 흔히 빠지는
  "전부 유망하다" 서술을 피한다. Table 1 의 Limitations 열도 형식적이지 않다.
- **SHAP 의 한계 서술이 특히 구체적이다** (§7.3) — 공선성, 모델 편향 상속,
  "feature importance 에는 보편적 ground truth 가 없다". 이 세 줄은 이
  리뷰에서 가장 날카로운 부분이다.
- 인용 폭이 넓고 최신이다 (2024–2025 문헌이 다수, *Nat. Energy* 2025,
  *Joule* 2025, *EES* 2025 등).

**약한 곳**
- **"물리적 의미가 있는 feature 를 쓰면 모델의 타당성이 보장된다"** (§3.5
  인용) 는 논리적 비약이며, 이 리뷰의 3번 분류 전체를 떠받치는 문장이다.
  물리적 해석 가능성 ≠ 물리적 분해 가능성이다.
- **성능 수치를 나열하지만 비교 가능성을 검토하지 않는다.** MAPE 0.91% ([109])
  와 MAPE 13.5% ([108]) 가 같은 표에 놓이는데, 전자는 LSTM 에 시퀀스 입력이고
  후자는 **첫 사이클만 쓰는 단변수** 모델이다. 데이터셋·분할·target 이 모두
  다른 수치들이며, 리뷰는 그 차이를 조정하지 않는다. (§1 공백 5·11)
- **역문제의 어휘가 통째로 없다** (§9). 특히 `uncertainty` 0회는 2025년
  리뷰로서 놀라운 수준이다. `Parameter identification` 이라는 그림 상자를
  실으면서 `identifiability` 를 한 번도 쓰지 않는다.
- **prognosis 의 정의가 넓게 열려 있다** (SOH·RUL·SOC·cycle life·knee·열폭주
  ·형성 결과). 제목의 "prognosis" 가 무엇을 포함하는지 명시적 정의가 없다.
- **체계적 문헌고찰이 아니다** — 검색 전략·포함 기준이 없어, 어떤 분야가
  빠졌는지(예: 전극 수준 진단 계열 전부) 독자가 판별할 수 없다.
- 조판·표기 오류가 눈에 띄는 편이다: `intrisic`, `Impedence`, `Opportunies`,
  `Onset temperatrue`, `Differential Volatge`(§4.2 절 제목), `LPR`↔`LRP` 혼용,
  "This integration of prior knowledge helps This integration of prior
  knowledge helps"(p.8 중복 문장), 그리고 참고문헌 [170] 의 DOI 가
  `https://doi.org/10.1002/aenm.20` 로 잘려 있다.

**후속 인용자를 위한 경고** — §11.3 에 정리했다.

---

## 14. 다음 흡수 후보 (이 리뷰가 짚어 준 원전) ★ 의뢰 6항

우리 축(전극 수준 분해 · 식별 가능성 · physics feature 정의)에 걸리는 순서로
5편. 서지사항은 이 리뷰의 참고문헌 목록에서 `[인쇄]` 그대로 옮긴 것이다.

| 우선 | 문헌 | 왜 필요한가 (한 줄) |
|---|---|---|
| **1** | **S. Navidi, A. Thelen, T. K. Li, C. Hu**, *Energy Storage Materials* **2024**, 68, 103343 (리뷰 [102]) | 손실함수에 "**true values of … lithium inventory**" 와의 차이를 넣는다 — **전극 수준 양을 정답으로 쓰는 유일한 인용 사례**이며, 그 정답을 어디서 얻는지가 우리 라벨 불확실성 질문의 정면이다 |
| **2** | **M. Kim, I. Kim, J. Kim, J. W. Choi**, *ACS Energy Lett.* **2023**, 8, 2946 (리뷰 [108]) | **DV peak intensity = PVS 의 직접 선례**. 같은 기하량을 **음극 단일**에 귀속시키므로, 세미나의 양극-음극 대비 해석과 충돌한다. 물리 귀속의 정본을 확인해야 한다 |
| **3** | **S. Y. Tao et al.** (23인), *Energy Environ. Sci.* **2025**, 18, 1544 (리뷰 [106]) | 전압 손실을 **열역학 ΔE / 동역학 η** 로 분해한 선행 프레임 — PVS·SEV 조합의 계보. "decoupled" 를 어떤 근거로 주장하는지가 우리 H1/H2 판정과 직결 |
| **4** | **J. Rhyu, J. Schaeffer, M. L. Li, X. Cui, W. C. Chueh, M. Z. Bazant, R. D. Braatz**, *Joule* **2025**, 9, 101884 (리뷰 [113]) | **세미나 p.4 가 이 리뷰와 나란히 인용한 바로 그 문헌.** dQ/dV·d²Q/dV² feature 를 **자동 생성**하는 프레임이며, 수작업 feature 설계(PVS)의 대안이자 비교 기준 |
| **5** | **Z. P. Su, J. D. Lai, J. H. Su, C. G. Zhou, Y. Shi, B. Xie**, *J. Energy Storage* **2024**, 90, 111770 (리뷰 [127]) | "**LLI 와 LAM 이 함께** R_ct 를 올린다" 는 DRT 관찰의 원전 — 임피던스 유래 feature 의 **모드 동부호 문제**를 문헌으로 고정할 수 있다 (SEV 축) |

`[해석]` 차순위 후보 (필요 시): **K. A. Severson et al.**, *Nat. Energy*
**2019**, 4, 383 (리뷰 [77] — ρ = −0.92/−0.93 불일치의 정본 확인 + LAM_NE,de
의 전압 이동 주장의 원전) · **X. Cui et al.**, *Joule* **2024**, 8, 3072
(리뷰 [132] — formation 프로토콜 62종 × 셀 186개, `electrode-specific
utilization range` 라는 표현의 출처) · **A. Weng, P. Mohtat, P. M. Attia,
V. Sulzer, S. Lee, G. Less, A. Stefanopoulou**, *Joule* **2021**, 5, 2971
(리뷰 [78] — Sulzer 는 PyBaMM 개발자이며 R_LS 라는 단일 저항 feature 로
수명을 예측한다).
