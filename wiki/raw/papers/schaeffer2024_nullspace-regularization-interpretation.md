---
title: "Schaeffer et al. 2024 — Interpretation of high-dimensional linear regression: effects of nullspace and regularization (Comput. Chem. Eng. 180, 108471)"
source_url: local-upload/12._Interpretation_of_highdimensional_linear_regression_Effects_of_nullspace_and_regularization_demonstrated_on_battery_data.pdf
ingested: 2026-09-03
sha256: 6347219507178b222f3405ebed2aa16ae0526376f183db7e8ada090d33e2e3fd
---

# 수집 목적

Joachim Schaeffer, Eric Lenz, William C. Chueh, Martin Z. Bazant, Rolf Findeisen,
Richard D. Braatz, **"Interpretation of high-dimensional linear regression:
Effects of nullspace and regularization demonstrated on battery data"**,
*Computers and Chemical Engineering* **180** (2024) 108471 의 **절별 해체분석**
(본문 9쪽 + SI 4쪽 + 저자 공개 저장소 `HDRegAnalytics`).

이 문헌은 이 위키가 **두 번 지목해 둔** 것이다.
[[fused-lasso-feature-design-framework]] (Rhyu et al. 2025) 를 흡수하던
2026-09-03 (7) 라운드에서 그 논문의 참고문헌 `[13]` 제목 안에 `nullspace` 가
있는 것을 보고 "저자 그룹 자신의 nullspace 논문인데 본문에서 **긍정 근거로만**
인용한다" 고 적었다 ([[pvs-sev-lli-lampe-separability]] Gap 절, `22p` 카드
Status Log (4) 항목 2). 바로 그 `[13]` 이 이 논문이다.

그리고 직전 라운드에서 축이 옮겨졌다. [[np-lip-ocv-reparametrization]]
(Lin & Khoo 2024) 이 우리 축퇴의 **닫힌 형태 null 방향**을 인쇄했고, 그
digest 의 결론 중 하나가 이것이었다 — *"오차공분산 `C_θ` 를 계산해 놓고
`sqrt(diag)` 만 그린다. 축퇴의 **방향**을 손에 쥔 채 한 번도 표시하지 않는다.
우리가 값싸게 공급할 수 있는 것이 바로 그 그림이다."*

따라서 이 digest 의 무게중심은 "이 논문이 무엇을 발견했나" 가 **아니라**:

> **nullspace 를 다루는 이 논문의 도구가 우리 축퇴 방향에 그대로 쓰이는가.
> 특히 그 방향을 *그리는* 방법을 여기서 얻을 수 있는가.**

**표기 규칙** (이 위키 관례 3구분):
- `[인쇄]` — 논문 본문·SI·식·표·캡션·저장소 코드에 **글자로** 있는 것
- `[도표]` — 그림에서 눈으로 읽은 근사값 (원 데이터가 아니다)
- `[해석]` — 이 문서를 쓰면서 붙인 판단. **논문의 주장이 아니다**
- `[재현]` — 저자 공개 데이터·코드로 **우리가 직접 계산**한 값. 원문에 인쇄돼
  있지 않다. 방법은 §12 에 적었고 원문 인용 근거로 쓰면 안 된다.

---

## 0. 서지사항 (직접 확인)

| 항목 | 값 |
|---|---|
| 저자 | J. Schaeffer¹², E. Lenz¹, W. C. Chueh³, M. Z. Bazant², R. Findeisen¹, R. D. Braatz²(교신) |
| 소속 | ¹TU Darmstadt (Control and Cyber–Physical Systems Lab) · ²MIT · ³Stanford |
| 학술지 | *Computers and Chemical Engineering* **180** (2024) 108471 |
| DOI | 10.1016/j.compchemeng.2023.108471 |
| 접수/개정/게재 | 2023-08-31 / 2023-10-11 / 2023-10-17 · online 2023-10-20 |
| 프리프린트 | arXiv:2309.00564 (stat.ML) — 저장소 README `[인쇄]` |
| 코드·데이터 | `https://github.com/JoachimSchaeffer/HDRegAnalytics` · `https://data.matr.io/1/` |
| 라이선스 | 코드 AGPL-3.0 · LFP 데이터 CC-BY 4.0 (`data/lfpdatalicense.md`) |
| 키워드 `[인쇄]` | Interpretable machine learning · Linear regression · High dimensions · **Nullspace** · Functional data · Lithium-ion batteries |
| 자금 | DAAD (석사 해외장학·IFI 펠로우십, BMBF 재원) · **Toyota Research Institute** (D3BATT Center) |
| 본문 분량 | 9쪽 (참고문헌 제외 본문 약 44,400자) + SI 4쪽 (약 8,800자) |

**계보 위치**: 저자 6인 중 Chueh·Bazant·Braatz 는 Severson et al. 2019
(*Nat. Energy* 4, 383) 의 공저자다. 즉 이 논문은 **Severson 데이터셋을 만든
팀이 그 데이터셋 위에서 자기들 회귀 계수의 해석 가능성을 스스로 문제 삼은**
논문이다. 이 위키의 [[fused-lasso-feature-design-framework]] (Rhyu 2025,
*Joule*) 와 [[zhang2020-eis-aging-dataset]] (Zhang 2020, *Nat. Commun.*;
심사자가 Braatz) 도 같은 계보다.

---

## 1. ★ 원문에 없어서 확인이 필요한 것 (먼저 적는다)

논문을 읽기 전에 우리가 기대했던 것 중 **없는 것**들이다. 이 목록이 이
digest 의 정직성 담보다.

1. **비선형 문제로의 확장이 없다.** 전부 `y = Xβ* + ε` 선형 정적 모형이다.
   Jacobian·국소 선형화·비선형 최소제곱이라는 단어가 본문에 **없다**. 우리
   문제(모드 → 곡선)로 옮기는 다리는 **우리가 놓아야 한다** (§14.1).
2. **`identifiability`·`degeneracy`·`non-unique`·`Fisher`·`Hessian`이 전부 0회**
   (§3 전수). 같은 수학을 다루면서 그 어휘를 쓰지 않는다 — 이 계보 열한 편째의
   같은 형태다.
3. **불확실성 정량이 없다.** `uncertainty` 0 · `confidence interval` 0 ·
   `error bar` 0. `v_γ` 나 β 에 오차 막대가 붙은 그림이 하나도 없다. 베이지안
   회귀를 §2 에서 한 문단 언급하고 `[인쇄]` "we focus on analyzing linear
   regression methods that **do not model regression coefficients
   probabilistically** because chemical engineers commonly use non-probabilistic
   models" 라며 명시적으로 범위 밖에 둔다.
4. **`γ` 선택이 휴리스틱이고 일부는 손으로 골랐다.** `[인쇄]` "We hand-selected
   γ = 10 for this case study" (§4.1), "Here we hand-selected γ = 0.1, as a
   different example". 식 (23) 의 자동 선택은 `[인쇄]` "not convex for most
   practical examples". 즉 `v_γ` 그림의 진폭은 **저자의 손에 어느 정도 달려
   있다** — 이것이 이 방법의 가장 큰 약점이다 (§15).
5. **cycle life 사례에서 `β*` 가 존재한다는 근거가 없다.** §4.2.2 는 참계수를
   모르는 실측 응답인데, 그럼에도 fused lasso 계수의 봉우리에 전기화학적 의미를
   붙인다. 그 해석의 검증 절차가 없다 (§15.2 — 이 논문의 가장 날카로운 자기모순).
6. **LLI/LAM/half-cell 이 0회.** 이 논문은 **열화 모드를 재지 않는다.** 응답은
   cycle life 하나뿐이다. 모드 분해에 대한 진술은 Dubarry 2012 를 인용한 한
   문장뿐이다 (§9.3).
7. **일차 시험셋에서 셀 하나가 조용히 빠졌다.** 본문에 그 서술이 없고 Table 1
   의 `Test 1 (42)` 라는 괄호 숫자만 흔적이다. 코드에는 이유가 주석으로 적혀
   있다 (§11.4, §15.4). 이것은 원문 검토만으로는 찾을 수 없고 **저장소를 열어야**
   보인다.
8. **교차검증 fold 의 group 정의가 없다.** R 코드는 41 셀에 대한 **무작위
   10-fold** 다 (`foldid <- sample(rep(seq(nfolds), length = N))`). 충전
   프로토콜 group 이 아니다 — [[fused-lasso-feature-design-framework]] 가
   같은 그룹에서 세운 표준(프로토콜 group + 설계를 학습 fold 안에 가둠)보다
   **느슨하다.** 두 논문의 시간 순서를 보면 이 논문(2023)이 먼저다.

---

## 2. 사용자가 물은 다섯 질문에 대한 직답

근거는 아래 절에 전부 있다. 여기서는 결론만.

### Q1. nullspace 를 정확히 무엇의 nullspace 로 정의하는가

**설계행렬 `X` 의 nullspace 다. Fisher/Hessian 이 아니다.**

`[인쇄]` 초록: "The data's nullspace contains all coefficients that satisfy
**𝐗𝐰 = 𝟎**, thus allowing very different coefficients to yield identical
predictions."

`[인쇄]` §1: "We use the fact that 𝒩(𝐗) consists of all solutions to 𝐗𝐰 = 0
and thus the predictions do not change when adding a vector of the nullspace to
the regression coefficients **𝐗(𝜷 + 𝐰) = 𝐗𝜷**."

좌표: `X ∈ R^{n×p}`, `n` = 표본 수, `p` = 예측자 수, **`p ≫ n`** 를 가정한다.
따라서 `dim 𝒩(X) = p − rank(X) ≥ p − n` 이고 LFP 사례에서는
**`[재현]` 959 차원** (`p=1000`, `n=41`; 열 평균중심 후에는 rank 가 40 으로
떨어져 **960 차원**).

**★ 우리 문제와의 간극 — 좁혀지는 부분과 좁혀지지 않는 부분을 나눠 적는다:**

`[해석]` **(a) 좁혀지는 부분: `𝒩(X)` 는 이 모형에서 Hessian 의 커널과 같다.**
선형 최소제곱 `J(β) = ‖y − Xβ‖²` 의 Hessian 은 정확히 `2XᵀX` 이고,
`𝒩(X) = 𝒩(XᵀX)` 다 (`Xβ=0 ⟺ βᵀXᵀXβ=0`). 등분산 가우시안 잡음이면 Fisher
정보행렬은 `XᵀX/σ²` 다. 즉 **"설계행렬의 nullspace" 와 "Hessian/Fisher 의
영고유공간" 은 이 모형에서 같은 것의 두 이름이다.** 논문은 그 사실을 쓰지
않지만(Hessian·Fisher 0회) 수학적으로 동치다. 그러므로
[[np-lip-ocv-reparametrization]] 이 계산한 `C_θ = (Fisher)⁻¹` 의 **최소
고유벡터**와 이 논문의 `𝒩(X)` 는 **같은 대상의 정확판과 근사판**이다.

`[해석]` **(b) 좁혀지지 않는 부분 1 — 우리 문제는 비선형이다.** 우리의
모드 → 곡선 사상 `f: θ ↦ U(z; θ)` 는 비선형이므로 `X` 자리에 들어갈 것은
**Jacobian `J(θ) = ∂f/∂θ`** 이고, 그때 `𝒩(J)` 는 **`θ` 에서만 성립하는
국소** 개념이다. 논문의 `𝒩(X)` 는 전역이다. 이 차이는 Lin & Khoo 가 자기
감도 분석에 붙인 한계와 정확히 같다 (`[인쇄, Lin]` "any statements based on
sensitivity gradients are **only valid locally**").

`[해석]` **(c) 좁혀지지 않는 부분 2 — 차원이 반대다. 그리고 이것이 우리에게
유리하다.** 논문은 `p ≫ n` 이라 nullspace 가 **959 차원**이고, 그래서 저자
자신이 저장소에서 그 기저를 그려 보다 포기한다 (§11.3 — 저자 주석 인용).
우리는 미지수가 3~4 개이고 관측이 곡선 전체이므로 `J` 는 **키가 큰** 행렬이고
`𝒩(J)` 는 일반적으로 `{0}` 이다. 즉 **우리 축퇴는 정확한 null 이 아니라
근사 null**(작은 특이값)이다. 따라서:

> **우리가 써야 하는 것은 논문의 식 (14)(정확 사영)이 아니라 식 (19)
> (`γ`-완화판)이다.** 식 (19) 는 `JᵀJ` 가 정칙이어도 정의되고, 특이값 크기에
> 따라 "데이터가 말이 없는 방향" 을 **연속적으로** 골라낸다. 논문은 이것을
> 수치 안정성 때문에 도입했지만(§5.3), 우리에게는 **본질적인 도구**다.

동시에 이 차원 역전은 좋은 소식이다 — **1차원 null 방향은 그릴 수 있다.**
저자가 포기한 이유(959개의 임의 정규직교 기저는 해석 불가)가 우리에게는
없다.

### Q2. 정칙화가 계수 해석에 무엇을 하는가

**세 단계로 인쇄돼 있다.**

**(1) 데이터는 nullspace 성분을 정하지 않는다. 정칙화만이 정한다.**
`[인쇄]` §3: "The vectors in the nullspace **affect only the regularization
term** in the objective function."
`[인쇄]` §2: "The nullspace and its interplay with regularization
**significantly influence the shape** of the regression coefficients."

**(2) 어떤 기준으로 고르는가 — 방법마다 다르고, 두 부류로 갈린다.**

| 부류 | 방법 | nullspace 성분 | 근거 |
|---|---|---|---|
| **직교** (성분 = 0) | RR, PCR, PLS, 최소노름해 | 정확히 `0` | SI §S2 증명 3건 |
| **비직교** (성분 ≠ 0) | lasso, Elastic Net, **fused lasso** | 일반적으로 `≠ 0` | `[인쇄]` "not orthogonal to 𝒩(𝐗) **because of the L1-norm**" |

`[인쇄]` RR 의 이유: "the regularization term in (3) is always smaller for
coefficients orthogonal to 𝒩(𝐗)". PCR·PLS 는 구성상 `V₁` 이 치는 공간 안에
있어서 자동으로 직교 (SI (S8), (S13)).

`[해석]` 이 표가 이 논문의 실질적 알맹이다. **RR/PCR/PLS 를 쓰는 순간
"null 방향 성분은 0" 이라는 답을 데이터가 아니라 **패널티 함수가** 이미
정해 버린다.** 그 0 은 물리적 선택이 아니라 L2 노름의 편의다.

**(3) 그 선택이 물리적 의미를 갖는다고 주장하는가 — 조건부로만 그렇다고
한다. 이것이 이 논문의 가장 정확한 문장이다.**

`[인쇄]` 초록: "regularization and z-scoring are design choices that,
**if chosen corresponding to prior physical knowledge**, lead to interpretable
regression results. **Otherwise**, the combination of the nullspace and
regularization **hinders interpretability and can make it impossible to obtain
regression coefficients close to the true coefficients** when there is a true
underlying linear model."

`[인쇄]` §4.1: "**From the data alone, it is not possible to state whether 𝐲 was
constructed from constant or parabolic coefficients.**"

`[해석]` 즉 **"정칙화가 고른 값에 물리적 의미가 있다" 도 "없다" 도 아니다.
넣은 사전지식만큼만 나온다는 항등식**이고, 그 사전지식이 맞는지는 **데이터로
확인할 수 없다**고 못 박는다. 우리 문제에 그대로 옮기면:

> 축퇴 방향 위에서 fitting 이 내놓는 값은 **암묵적 정칙화**(초기값·경계·
> optimizer 경로·정규화 축 선택)가 정한 것이고, 목적함수 값은 그것을
> 구별하지 못한다.

### Q3. 해석 가능성에 대해 무엇을 금지하는가

**금지 문장 3개가 인쇄돼 있다. 다만 "계수 크기를 중요도로 읽지 말라" 는
정확한 형태로는 없고, 그것의 그림판 반례가 있다.**

- `[인쇄]` §1: "regression coefficients for a linear model can be analyzed and
  compared to engineering or scientific expectations **in terms of shape
  (e.g., peaks, plateaus, slopes)**, which is often done implicitly by engineers
  when looking at regression coefficients. However, as shown in this article,
  **such an interpretation can lead to misleading conclusions**."
  → **금지 대상이 "봉우리·평탄·기울기를 읽는 것" 자체다.** 우리가 다른
  논문들에서 본 함정(ARD 가중치, permutation importance, SAGE 점유율)과
  **같은 계열이되 더 근본적**이다: 저것들은 적합된 모형에 대한 **사후 귀속**의
  신뢰도 문제인데, 이것은 **모형 자신의 계수 벡터**가 데이터에 의해
  959 차원만큼 자유롭다는 진술이다.
- `[인쇄]` §4.2.2: "The component of the regression coefficients orthogonal to
  the nullspace (cf. red coefficients in Fig. 8ab) are **less interpretable
  while making identical predictions on the training data**."
- `[인쇄]` 결론: "Regression methods which yield coefficients orthogonal to the
  nullspace, such as RR, PCR, and PLS, **can be challenging to interpret**."

**★ 크기=중요도 함정의 그림판 반례 (Fig. 4a — 직접 봄):** 합성 응답의 참계수는
전 구간 **상수 `β* = 0.001`** 인데, PLS 계수는 `[도표]` **3.2 V 위에서 ≈ 0 으로
붕괴**한다. 그 계수만 보면 "3.2–3.5 V 는 무의미한 구간" 이라고 읽게 되지만
**참계수는 그 구간에서도 다른 곳과 똑같이 중요하다.** 그리고 nullspace 로 보정한
계수(magenta)는 그 구간에서 `[도표]` **≈ 0.0009 로 되돌아온다.** 논문의 서술도
같다: `[인쇄]` "the differences in the region 3.2 to 3.5 V **do not change the
prediction results on the training data significantly** and arise due to the
interplay of the regularization objective with the nullspace."

`[해석]` **이것이 "계수가 작다 ⇒ 그 변수는 중요하지 않다" 의 반례이고, 이
논문이 우리에게 주는 가장 이식성 높은 경고다.**

`[해석]` 한편 논문이 **금지하지 않는** 것도 정확히 적어야 한다: 이 논문은
"해석하지 말라" 고 말하지 않는다. 오히려 §4.2.2 에서 **직접 해석한다**
(§9.3). 논문의 처방은 "해석을 포기하라" 가 아니라 **"사전지식과 맞는
정칙화를 골라라, 그리고 nullspace 로 그 차이가 데이터 탓인지 정칙화 탓인지
분리해 보아라"** 다.

### Q4. 우리가 그대로 쓸 수 있는 진단 도구 (파일·함수 이름까지)

**있다. 그리고 우리 `C_θ`/Jacobian 에 바로 붙는다.** 저장소
`HDRegAnalytics` (읽기만 함, 이 저장소에 복사하지 않음) 기준:

| 우선 | 파일:줄 | 이름 | 무엇이고 우리에게 무엇인가 |
|---|---|---|---|
| **★★★** | `src/nullspace.py:390` | `Nullspace.nullspace_calc` | 식 (19) 구현. 핵심 한 줄이 `:429` — `v_[i,:] = -linalg.inv(g*self.XtX + I_) @ self.w`. **`X` → Jacobian `J`, `w` → `θ_A − θ_B` 로 바꾸면 그대로 우리 것.** `g` 배열을 주면 `γ` 경로 전체를 한 번에 낸다. |
| **★★★** | `src/plotting_utils.py:298` | `plot_nullspace_analysis` | **null 방향을 그리는 그림 그 자체.** 세 곡선(β_A / β_A+v_γ / β_B)을 한 축에 얹고 NRMSE 를 범례에 박는다. 논문 Fig. 1b·2·4·5 가 전부 이 함수의 출력. |
| **★★★** | `src/nullspace.py:199` | `Nullspace.objective_function_trajectory` | `γ` 를 `logspace(5,-5,40)` 로 쓸어 **ΔNRMSE 와 ‖Xv‖ 를 로그-로그 이중축**으로 그린다. `[해석]` **이것이 "축퇴 방향을 따라 얼마나 멀리 가야 목적함수가 얼마나 나빠지는가" 의 곡선**이고, 우리 flat valley 진단의 정확한 정량판이다. 논문 본문에는 이 그림이 **없다** — 코드에만 있다. |
| ★★ | `src/utils.py:517` | `project_reg_coeff_onto_nulls` | 정확 사영자 `I − Xᵀ(XXᵀ)⁻¹X` (식 14). `XXᵀ` 역행렬을 쓰므로 조건수에 취약 — 저자 자신이 노트북에서 아래 것을 권한다. |
| ★★ | `src/utils.py:523` | `project_reg_coeff_onto_space_by_basis` | 정규직교 기저 `SX` 로 사영. 노트북 주석 `[인쇄]` "The scipy implementation is better". `SX = scipy.linalg.null_space(X)`. |
| ★★ | `src/nullspace.py:354` | `Nullspace.eval_constraint` | `γ` 를 고르는 **세 가지 판정 지표** (`MSE`, `NRMSE`, `Xv`). `Xv` 는 `100·RMS(Xv)/range(ŷ)` — 예측 공간에서 잰 이탈량이다. |
| ★★ | `src/nullspace.py:239/273/321` | `optimize_gamma` / `naive_opt_gamma` / `scipy_opt_gamma` | 식 (23) 의 "허용 손실 변화 `c` 안에서 `γ` 최대화". 기본값은 naive(격자 탐색). |
| ★ | `src/hd_data.py:144, 234` | `analyze_snr_by_splines`, `calc_snr` | 스플라인 적합 잔차로 **좌표별 SNR** 를 낸다 (SI Fig. S2 생성기). `[해석]` "우리 OCV 곡선의 어느 전압 구간이 정보를 싣는가" 에 그대로 쓸 수 있다. |
| ★ | `Nullspace_LFP_examples.ipynb` cell 36–37 | `scipy.linalg.null_space` + 기저 벡터 플롯 | **저자가 null 방향을 직접 그려 본 유일한 자리.** 결론은 실패다 — §11.3 의 주석 인용. |
| ★ | `regression_in_R/regression_lfp.R`, `utils.R` | `genlasso` + `cv_genlasso` | fused lasso (D1/D2) 와 그 CV. Fig. 6b·7b·8 의 계수 출처. |

**★ null 방향을 그리는 그림**에 대한 정직한 답은 두 갈래다:

- **논문 안에는 "축퇴 방향 자체" 를 그린 그림이 없다.** Fig. 1b·2·4·5 는
  `β_A` 와 `β_A + v_γ` 를 함께 그려 **차이로** 보여 주고, Fig. 8 은 `β_FL` 과
  그 **직교 성분** `β_FL⊥` 를 겹쳐 그린다. 방향 벡터 `v` 를 독립적으로 그린
  패널은 없다.
- **저장소에는 있고, 저자가 실패라고 적어 두었다** (§11.3). 실패 사유는
  차원(959)이지 발상이 아니다. **우리 문제에서는 같은 코드가 작동한다.**

### Q5. 데이터 — 저장소에 실제로 있는가

**있다. 그리고 완전히 재현·재사용 가능하다.**

`data/lfp_slim.csv` — **124 행 × 1004 열**:
- 열 `1..1000`: `ΔQ_{100−10}(V)` (Ah), 전압 격자 **2.0–3.5 V, 1000점**
- 열 `1001`: `cycle life (cycles)` — `[재현]` 148 ~ 2237, 평균 802
- 열 `1002`: `charging protocol class` — `[재현]` 68개 고유값
- 열 `1003`: `nature energy publication split` — `[재현]` 0 = train **41**,
  1 = test **43**, 2 = secondary test **40** (Severson 2019 의 원 분할)

`[인쇄]` 논문 §4.2: "𝛥𝐐₁₀₀₋₁₀ ∈ R^{41×1000}", 셀 124개, 방전은 전 셀 동일
(4C CC), 충전 프로토콜만 다르다. 예측 대상은 **cycle life 의 로그**.

`[해석]` **"a small subset of the LFP data set" 이라는 표현의 뜻을 정확히
해 둔다** — 셀 수를 줄인 것이 **아니다** (124셀 전부 있다). 줄인 것은
**셀당 데이터**다. 원 데이터셋의 전체 사이클링 이력 대신 **사이클 100 과
10 의 방전용량 차 곡선 한 개**만 남겼다. 우리 목적에는 충분하다.

**우리가 쓸 수 있는가**: 쓸 수 있다. CC-BY 4.0 이고, 3 MB 이고,
§12 에서 실제로 돌려 봤다. **단 LLI/LAM 라벨은 없다** — 이 데이터로 우리
축퇴 질문에 직접 답할 수는 없다. 쓸 자리는 **방법론 검증**이다
(우리 진단 코드가 남의 공개 데이터에서 같은 숫자를 내는지).

**★ 재사용 시 반드시 알아야 할 함정 두 개** (`[재현]`, §11.5 에 근거):
1. **CSV 열 라벨과 데이터 순서가 반대다.** 헤더는 `2.0 V … 3.5 V` 인데
   실제 열 0 은 3.5 V 쪽이다 (열 0 의 평균 −9.3e−6 ≈ 0, 열 999 의 평균
   −9.3e−3). 노트북은 `X_lfp[:, ::-1]` 로 조용히 뒤집는다. **그 한 줄을
   빠뜨리면 모든 전압 해석이 좌우로 뒤집힌다.**
2. **노트북 안에서 축 방향이 일관되지 않다.** cell 37 은 nullspace 기저를
   `np.linspace(3.5, 2.0, 1000)` 에 대해 그리는데, 같은 노트북 cell 38·40 은
   `np.linspace(2.0, 3.5, 1000)` 을 쓴다. 뒤집힌 배열에 뒤집힌 축을 다시
   쓰면 두 번 뒤집는 셈이다. `[해석]` cell 37 쪽이 틀린 것으로 보이나
   그 그림은 논문에 실리지 않았으므로 논문 그림에는 영향이 없다.

---

## 3. 어휘 전수 (이 계보 **열한 편째**) ★

합자·붙임표 정규화 후, **본문 44,379자**(참고문헌 제외) + **SI 8,826자** 전수.

| 어휘 | 본문 | SI | 참고문헌 |
|---|---|---|---|
| `nullspace` | **69** | **9** | 0 |
| `orthogonal*` | 19 | 10 | 1 |
| `regulariz*` | 30 | 6 | 2 |
| `interpretab*` | 13 | 0 | 2 |
| `true coefficient*` | **25** | 0 | 0 |
| `noise` | 19 | 8 | 0 |
| `prior` | 9 | 0 | 0 |
| `engineering` | 16 | 0 | 1 |
| `physic*` | 7 | 0 | 0 |
| `shape*` | 7 | 0 | 0 |
| `importan*` | 9 | 0 | 0 |
| `cross-validat*` / `CV` | 9 | 0 | 0 |
| `singular value` | 2 | 1 | 0 |
| `condition number` | 1 | 1 | 0 |
| `ill-conditioned` | 1 | 0 | 0 |
| `collinear*` | **1** | 0 | 0 |
| **`identifiab*`** | **0** | **0** | **0** |
| **`degenerac*` / `degenerate`** | **0** | **0** | **0** |
| **`non-unique` / `uniqueness` / `unique`** | **0** | **0** | **0** |
| **`ill-posed`** | **0** | **0** | **0** |
| **`Hessian`** | **0** | **0** | **0** |
| **`Fisher`** | **0** | **0** | **0** |
| **`uncertaint*`** | **0** | **0** | **0** |
| **`confidence`** | **0** | **0** | **0** |
| **`error bar`** | **0** | **0** | **0** |
| **`LLI` / `LAM` / `half-cell`** | **0** | **0** | 0 |
| `degradation mode` | 1 | 0 | 1 |
| `incremental capacity` | 2 | 0 | 0 |
| `Severson` | 12 | 0 | 3 |
| `Dubarry` | 1 | 0 | 1 |

### 3.1 `[해석]` 열한 편째의 새 형태 — **"개념을 자기 어휘로 새로 만든다"**

지금까지 아홉 편은 "그 어휘가 아예 없다" 였고, 열 편째(Lin & Khoo)는
"절반만 자기 쪽으로 돌린다"(추정 정밀도는 재고 비유일성은 `redundancy` 라
부르고 지나감) 였다. 이 논문은 **또 다른 형태**다:

> **비유일성을 정면으로, 69회, 논문 전체의 주제로 다룬다. 그런데 그것을
> 부르는 이름이 `nullspace` 뿐이고, 통계·시스템동정 문헌의 표준 어휘
> (`identifiability`, `non-uniqueness`, `ill-posedness`)를 한 번도 쓰지
> 않는다.**

`collinear*` 1회는 §2 의 `[인쇄]` "the high **multicollinearity** of columns
that arises from functional data" 로, 문제의 **원인**을 부르는 데만 쓰인다.
`condition number` 1회는 OLS 분산 설명, `ill-conditioned` 1회는 `XXᵀ` 의
수치 문제.

`[해석]` 이것이 왜 중요한가: **어휘가 다르면 두 문헌이 서로를 못 찾는다.**
Lin & Khoo(전기화학, `identifiability` 26회, `nullspace` 0회)와
Schaeffer(화학공학/ML, `nullspace` 69회, `identifiability` 0회)는 **같은
수학적 대상**을 다루면서 서로를 인용하지 않는다. 우리 프로젝트는 두 어휘를
동시에 쓰는 자리에 있고, 그 자체가 기여 지점이다.

### 3.2 `unique` 계열이 **0회**라는 사실의 무게

이 논문의 중심 주장은 `[인쇄]` "allowing **very different coefficients to
yield identical predictions**" 다. 그것은 **해의 비유일성 진술 그 자체**인데
`unique` 라는 단어를 한 번도 쓰지 않는다. 대신 쓰는 표현이:
- "identical predictions" (2회)
- "the predictions do not change"
- "unchanged predictions"

`[해석]` 즉 **예측의 동일성**으로만 말하고 **계수의 비유일성**으로는 말하지
않는다. 이 서술 습관이 §15.2 의 자기모순(경고해 놓고 해석함)과 무관하지
않을 것이다.

---

## 4. §1 Introduction — 문제 설정

`[인쇄]` 첫 문장: "Many important regression problems have the dimensionality
of the data 𝑝 much larger than the sample size 𝑛". 예시로 분광학, **리튬이온
배터리**, 뇌영상, 계산생물학을 든다.

방법별 위치:
- **OLS** — `p > n` 에서 `XᵀX` 가 특이해 정의되지 않는다. 대신 **최소노름해**.
- **RR / lasso / EN** — 패널티가 `XᵀX` 의 주대각에 더해져 가역이 된다.
- **fused lasso** — `[인쇄]` "adds an L1-norm penalty of adjacent regression
  coefficient differences … encourages **piecewise constant** regression
  coefficients … **it is required that the predictors can be ordered in some
  meaningful way**."
- **PLS / PCR** — `[인쇄]` "popular choices for high-dimensional regression in
  the chemometrics community."

핵심 물음 `[인쇄]`: "A key question is **how to interpret** high-dimensional
linear regression results and the corresponding regression coefficients. In
particular, how to reason about an underlying (linear) model for scientific
insights and system optimization?"

`[인쇄]` 각주 1 — "functional data" 의 정의: "data in which neighboring values
are linked to each other to some extent, are not too different from one
another, and there exists an underlying function that is **differentiable once
or multiple times**."

`[해석]` **우리 OCV 곡선은 정확히 이 정의의 functional data 다.** 인접 전압
격자점의 `dQ/dV` 값이 서로 묶여 있고 미분 가능한 바탕 함수가 있다. 즉 우리가
곡선을 격자점 벡터로 다루는 순간 이 논문의 가정이 전부 성립한다.

---

## 5. §2–3 방법 — 식을 전부 옮긴다

### 5.1 모형과 목표의 구분 (§2)

```
(1)  y = Xβ* + ε,        X ∈ R^{n×p},  p ≫ n
(2)  y = ŷ + ε̂ = Xβ̂ + ε̂
```

`[인쇄]` 목표가 **둘**이고 다르다는 것을 명시한다: "The objective of regression
methods is to find a β̂ that yields predictions that are reasonably close to the
predictions of β* **when applied to independent data**. … interpretation and
scientific insights would be supported by achieving **a different goal**, which
is to **reconstruct the true coefficients**, i.e., β̂ = β*."

`[해석]` **이 구분이 이 논문 전체의 축이고 우리 프로젝트의 축과 같다.**
"예측이 맞는가" 와 "파라미터를 되찾았는가" 는 다른 질문이다. 우리 파이프라인이
`|err|` 로 재는 것은 후자이고, 세미나 계열이 MAE 로 재는 것은 전자다.

### 5.2 최소노름해와 직교성 (§2, 식 4–7)

```
(4)  β₀ = lim_{λ→0} β_λ = X† y
(5)  β₀ = Xᵀ (X Xᵀ)⁻¹ y                       (p > n)
(6)  β₀ = argmin_β { ‖β‖₂² | ‖y − Xβ‖₂² = 0 }
(7)  (β̃ − β₀)ᵀ β₀ = 0  ⟹  (β̃ − β₀) ⟂ β₀  ⟺  𝒩(X) ⟂ β₀
```

`[인쇄]` 결론: "Thus there exists a **set** of regression coefficients that all
fulfill 𝐗β̃ = 𝐲 with β̃ ∈ ℬ."

### 5.3 정칙화된 문제와 D-일반화 (식 8–10)

```
(8)  min_β ‖y − Xβ‖₂² + F(β)
(9)  min_β ½‖y − Xβ‖₂² + λ‖Dβ‖₁          (generalized lasso)
(10) D₁ = 1차 차분행렬 (인접 계수 차의 L1)
```

`[인쇄]` "The orthogonality of the regression coefficients to 𝒩(𝐗) **does not
hold for arbitrary regularization terms** 𝐹(𝜷)." 그리고
`[인쇄]` "The choice of 𝐃 **can incorporate expectations about the underlying
model structure**".

### 5.4 ★ nullspace method (§3, 식 11–23) — 이 논문의 기여

**정확판**:
```
(13a) min_v ‖β_Δ + v‖₂²        β_Δ = β_A − β_B
(13b) s.t.  X v = 0
(14)  v* = ( Xᵀ (X Xᵀ)⁻¹ X − I ) β_Δ
(17)  v* = − V [ 0 0 ; 0 I_{p−n} ] Vᵀ β_Δ        (SVD 형태)
```

**완화판** (수치 안정성 + 개념적 이유):
```
(18)  min_v ‖β_Δ + v‖₂² + γ‖X v‖₂²
(19)  v_γ = − ( γ XᵀX + I )⁻¹ β_Δ
(20)  γ → ∞ 면 (17) 로 수렴 ; γ = 0 이면 v₀ = −β_Δ (nullspace 무시)
```

`[인쇄]` 완화의 이유 두 가지: "The projection onto the nullspace can be a hard
requirement that might yield a vector 𝐯* that is **dominated by noise** and
difficult to interpret, in particular, if 𝐗𝐗ᵀ is **ill-conditioned**" +
"regularized regression coefficients usually differ from the true coefficients
(if they exist), and their difference is **not expected to lie exactly within
the nullspace but might be close to it**".

**`γ` 선택 휴리스틱**:
```
(21) s = max_i{y_i} − min_i{y_i}
(22) L(ŷ, y) = (1/(s√n)) ‖ŷ − y‖₂                (NRMSE)
(23) max_γ γ   s.t.  | L(X(β_A + v_γ), y) − L(Xβ_A, y) | ≤ c
```

`[인쇄]` "The optimization (23) is **not convex** for most practical examples
but is easy to solve because it only has **one degree of freedom**, γ."

**해석 규약** `[인쇄]`: "Analyzing the nullspace … allows us to identify **which
differences can be removed with a vector that is close to the nullspace** and
which differences **would require significant deviations from the nullspace**
and are thus mainly responsible for the differences of the associated
predictions."

`[해석]` **이 한 문장이 이식 대상의 전부다.** 두 파라미터 벡터의 차이를
"데이터가 구별하지 못하는 몫" 과 "데이터가 구별하는 몫" 으로 **정량 분해**
한다. 우리 문제로 옮기면: 두 열화 조합의 차이 중 얼마가 곡선에 흔적을
남기고 얼마가 안 남기는가 — 그것이 이 프로젝트가 재는 것 그 자체다.

---

## 6. §4.1 합성 포물선 사례 (Fig. 1, 2) — 논문에서 가장 중요한 그림

### 6.1 데이터 생성 `[인쇄]`

```
(24) x_i = a_i (d ⊙ d),      i = 1…50
(25) d = [1.00, 1.01, …, 3.00]        (간격 0.01, p = 201)
     a_i ~ N(μ=0.3, σ=0.3)            ⟹ X ∈ R^{50×201}
(26) y* = X* β*,   β* = (1/p) I       ⟹ 참계수는 전 구간 상수
(27)(28) X, y 에 백색잡음 추가, 각각 SNR = 50
```

즉 **데이터는 포물선, 참계수는 상수**다.

### 6.2 Fig. 1 (직접 봄)

`[도표]` 1a: 평균중심 데이터 50줄이 `d=1` 근처에서 모여 `d=3` 에서 −5 ~ +7 로
부채꼴로 벌어진다.

`[도표]` 1b — **범례에 인쇄된 NRMSE 3개가 이 논문의 핵심 수치다**:

| 곡선 | 형상 | NRMSE |
|---|---|---|
| `β₁^PLS` (녹색) | **포물선**, 0.0009(d=1) → 0.0080(d=3) — **9배 단조 증가** | **0.105 %** |
| `β₁^PLS + v_γ`, γ ≈ 10.0 (자홍) | **평탄**, 0.005 근방에서 ±0.0002 잔물결 | **0.104 %** |
| `β*` (검정) | **정확히 평탄** 0.005 (= 1/201) | **0.105 %** |

`[해석]` **모양이 9배 다른 두 계수 벡터의 예측 오차가 소수 셋째 자리에서
같다.** 이것이 축퇴의 교과서적 시연이고, 우리 flat valley 의 선형 판이다.
논문 본문의 서술도 같다: `[인쇄]` "the true coefficients and the PLS
coefficients have **very different shapes**. However, their predictions and
prediction accuracies are **almost identical**." 그리고
`[인쇄]` "The noise leads to a prediction error **even when the true
coefficients are used** (i.e., 0.105% NRMSE)."

`[인쇄]` 잔물결의 해석: "The **wrinkles indicate independent identically
distributed noise**, in line with the data generation." — `v_γ` 가 잡음을
싣는다는 자백이기도 하다.

`[인쇄]` 왜 PLS 가 포물선을 고르는가: "the PLS coefficients have a **smaller
L2-norm**, i.e., ‖β₁^PLS‖² < ‖β*‖², due to the **implicit regularization** of
PLS." → 정칙화가 고른 것이지 데이터가 고른 것이 아니다.

### 6.3 Fig. 2 (직접 봄) — 정칙화 선택이 답을 바꾼다

`[도표]` 같은 데이터, 다른 방법:

| 곡선 | 형상 | NRMSE |
|---|---|---|
| `β_CV1SE^RR` (녹색) | **포물선** 0.0009 → 0.0080 (PLS 와 사실상 동일) | **0.117 %** |
| `β_CV1SE^RR + v_γ`, γ ≈ 0.1 (자홍) | **평탄** 0.005 (Fig. 1 의 `v₁₀` 보다 매끄럽다) | **0.116 %** |
| `β_CV1SE^FL` (검정, fused lasso) | **평탄** 0.005 — 참계수와 육안 구별 불가 | **0.104 %** |

확대 삽입도가 자홍과 검정 사이의 **미세한 간격**을 보여 준다 (`[도표]`
0.005 근방에서 자홍이 아주 약간 아래).

`[인쇄]` "The fused lasso coefficients are **nearly identical to the true
coefficients**, and the ridge coefficients are similar to the PLS coefficients
with one component but slightly noisier." + `γ=0.1` 은
`[인쇄]` "only changing the associated NRMSE prediction error by **0.001%**".

### 6.4 이 절의 결론 `[인쇄]` — 두 문장을 그대로 옮긴다

> "**From the data alone, it is not possible to state whether 𝐲 was constructed
> from constant or parabolic coefficients.** Furthermore, regression
> coefficients obtained from methods that are orthogonal to the nullspace can
> yield coefficients that **appear to disagree with prior knowledge at first
> sight**. As this example shows, methods that are not orthogonal to the
> nullspace, such as the fused lasso, **can be advantageous for interpretation
> and conclusions if selected based on prior knowledge**."

`[해석]` 마지막 조건절("**if selected based on prior knowledge**")이 결정적이다.
fused lasso 가 이겼다는 것이 아니라, **이 예제에서는 참계수가 실제로
조각상수였기 때문에** 조각상수를 선호하는 패널티가 이겼다는 것이다. 참계수가
포물선이었다면 정반대 결론이 나왔을 것이고, 논문은 그 사실을 **데이터로 알 수
없다**고 이미 말했다.

---

## 7. §4.2 LFP 데이터셋 (Fig. 3, SI §S5)

### 7.1 데이터 `[인쇄]`

- Severson et al. 2019 의 **LFP 124셀**. 충전 프로토콜만 다르고 방전은 전 셀
  동일.
- 특징량 `ΔQ_{100−10}(V)` — 사이클 100 과 10 의 방전용량-전압 곡선 차.
  `[인쇄]` "shown to **linearly correlate well with the logarithm of the cycle
  life**".
- `ΔQ_{100−10} ∈ R^{41×1000}` (학습 분할), 전압 2.0–3.5 V.
- 분할은 Severson 원안 그대로 (train / primary test / secondary test).

### 7.2 Fig. 3 (직접 봄)

`[도표]` 3a — 124셀의 `ΔQ` 곡선. 전 곡선이 **음수**로, 3.2–3.5 V 에서 ≈ 0,
2.0 V 에서 0 ~ −0.14 Ah 로 벌어진다. 최단수명 셀 한 줄이 −0.135 Ah 로 **뚜렷이
떨어져** 있다. 학습(실선 파랑) / 시험(점선 빨강) / 이차시험(점쇄선 노랑)이
서로 섞여 있다.
`[도표]` 3b — 평균중심 학습 데이터. 한 줄이 −0.09 Ah 로 홀로 내려가 있고
나머지는 ±0.04 Ah 안이다.
`[도표]` 3c — z-scored 학습 데이터. **3.15 V 위에서 곡선들이 폭발**해
−5 ~ +2.5 사이를 고주파로 진동한다. 2.0–3.0 V 구간은 ±1.5 로 조용하다.

`[인쇄]` 저자 판단: 최단수명 셀에 대해 "we **keep this battery** in the data
set, as its influence on the training is **benign**."
(★ 이 문장은 **학습셋**에 대한 것이다. 시험셋에서는 셀 하나를 제거한다 —
본문에 안 적혀 있다. §11.4·§15.4.)

`[인쇄]` z-scoring 에 대한 경고: "for functional high-dimensional data, **the
unit of all columns is the same** … Fig. 3c shows that the noise in the voltage
region **3.2–3.5 V is amplified** by rescaling because of a lower SNR in this
voltage region."

### 7.3 SI §S5 / Fig. S2 (직접 봄) — SNR 지도

방법 `[인쇄]`: "The signal is estimated by fitting a spline, using
`scipy.interpolate.splrep` with a smoothing parameter **s = 10⁻⁶** and the
polynomial degree **k = 3** … The deviation to the spline is considered noise."
(★ 저장소 노트북은 `s=1e-5` 를 쓴다 — SI 인쇄값과 다르다. `[해석]` 사소하나
재현 시 주의.)

`[도표]` S2a — SNR[dB] 가 2.0 V 에서 ≈ 46 dB, 2.85 V 에서 **최대 ≈ 57 dB**,
이후 급락해 3.35 V 에서 ≈ 18 dB, 3.5 V 에서 ≈ −5 dB. 잡음 전력(주황)은
3.1–3.2 V 에서 뾰족하게 치솟는다.
`[도표]` S2b — 평균 `X̄` 가 0.011(2.0 V) → 0.046(2.9 V) → 3.2 V 위에서 ≈ 0.
표준편차 σ 는 0.010 → 0.020 → ≈ 0.
(`[재현]` 학습셋 실제값: 2.0 V 에서 mean −0.0111 / std 0.0100, 2.9 V 에서
mean −0.0467 / std 0.0180, 3.2 V 에서 mean −0.0035 / std 0.0014 — **크기가
정확히 일치**하고 **부호만 반대**다. `[해석]` S2b 는 절댓값 또는 부호 반전을
그린 것으로 보인다. 논문에 그 언급은 없다.)

`[인쇄]` 결론: "The SNR decreases strongly in the region 3.2–3.5 V; however, in
this region, **the standard deviation of the data is also very low**. Rescaling
the data matrix columns to unit variance thus **amplifies the noise** in this
section." + 대안 제시 `[인쇄]`: "rescale the data such that the **variance of
the column matches the normalized SNR ratio**."

`[해석]` **이 SNR 지도가 우리에게 직접 쓸모 있다.** 우리도 OCV/dQ-dV 곡선의
어느 구간이 정보를 싣는지를 같은 방법(스플라인 잔차)으로 낼 수 있고, 그것은
"PVS 를 어느 창에서 재야 하는가" 에 대한 데이터 기반 답이 된다.
[[pvs-sev-degradation-mode-features]] 의 valley 정의 민감도와 같은 축이다.
---

## 8. §4.2.1 합성 응답 두 개 (Fig. 4, 5) — 참계수를 아는 실측 데이터

`[해석]` **이 절의 설계가 우리 파이프라인의 설계와 같다**: 실측 `X` 를 쓰되
응답 `y` 는 알려진 `β*` 로 만들어 **복원 여부를 판정 가능**하게 한다. 우리가
PyBaMM 합성 truth 로 하는 것과 같은 논리이고, 우리 쪽이 한 단계 더 나아간
것(생성 모델도 물리 모델)이다.

### 8.1 참계수 = 상수 (Fig. 4, 직접 봄)

`β* = (1/p)·1`, `p = 1000`, SNR 50 의 백색잡음 추가.

`[도표]` **4a (원 스케일)** — PLS 성분 수는 CV + 1-SE 규칙으로 **2개**:

| 곡선 | 3.2 V **아래** | 3.2 V **위** | NRMSE |
|---|---|---|---|
| `β*` (검정) | 0.0010 상수 | **0.0010 상수** | 0.127 % |
| `β₂^PLS` (녹색) | 0.00093 ~ 0.00108 로 완만히 흔들림 | **≈ 0.00002 로 붕괴** | 0.159 % |
| `β₂^PLS + v_γ`, γ ≈ 1.45e3 (자홍) | 검정 근처에서 ±0.00015 잔물결 | **≈ 0.0009 로 회복** | 0.149 % |

★ 3.1 V 부근에서 자홍이 **0.00141 까지 치솟는 뾰족한 스파이크**를 보인다
(`[도표]`) — `v_γ` 가 저SNR 구간에서 잡음을 싣는다는 시각적 증거.

`[인쇄]` 저자 서술: "Most of the difference between the regression coefficients
in this area is **associated with the nullspace** … Thus, the differences in the
region 3.2 to 3.5 V **do not change the prediction results on the training data
significantly** and arise due to the interplay of the regularization objective
with the nullspace."

`[도표]` **4b (z-scored)** — PLS 성분 **4개**. `β*` 는 z-scoring 후 좌표에서
1.0e−5(2.0 V) → 2.0e−5(3.1 V) → 3.2 V 위에서 ≈ 0 인 **봉우리 모양**이 된다.
녹색 PLS 는 2.0–2.4 V 에서 검정보다 낮고(0.86e−5 vs 0.98e−5) 2.4 V 에 없는
어깨를 만들며 3.2 V 위에서 **±0.3e−5 로 진동**한다. 자홍은 검정과 **거의 완전히
겹친다** (확대 삽입도에서만 미세 차이).

**NRMSE 3개 (`[도표]`, 범례 인쇄값): PLS 0.108 % · PLS+v_γ 0.118 % ·
β\* 0.127 %.**

`[해석]` **★ 이 세 숫자의 순서가 중요하다 — 참계수가 가장 나쁘다.** 학습
데이터에서 적합 모형이 참계수보다 낮은 오차를 내는 것은 잡음을 먹었다는
뜻이므로 그 자체는 정상이다. 그러나 함의가 있다: **"학습 오차가 낮은 계수가
참에 가깝다" 는 추론이 여기서 명백히 깨진다.** 우리 문제에서 목적함수 값이
낮은 해가 참 열화 조합에 가깝다고 말할 수 없는 것과 정확히 같은 구조다.
논문은 이 순서를 표로 강조하지 않는다 (범례에 인쇄만 한다).

`[인쇄]` z-scoring 판정: "in case the true coefficients are constant (i.e., all
columns are equally important), **z-scoring can help** regression to yield
coefficients that are more similar to the true coefficients."

### 8.2 참계수 = 열 평균 (Fig. 5, 직접 봄)

```
(29) β*_j = (1/n) Σ_i x_{i,j}          ⟹ β* 가 데이터의 스케일을 따라간다
```

`[도표]` **5a (원 스케일, PLS 3성분)** — `β*` 는 −0.012(2.0 V) → **최소
≈ −0.046(2.95 V)** → 3.2 V 위에서 0 으로 급상승하는 곡선. 녹색 PLS-3 이 이를
**전 구간에서 잘 따라간다**. 확대 삽입도(2.0–2.6 V)에서 녹색만 −0.040 근처에서
두꺼운 잔물결을 갖고, 자홍은 검정 위에 얹혀 있다.
**NRMSE: PLS-3 0.101 % · +v_γ(γ≈8.4) 0.106 % · β\* 0.112 %.**

`[도표]` **5b (z-scored, PLS 6성분)** — 2.0–3.15 V 는 세 곡선이 겹치지만
**3.2 V 위에서 녹색이 ±1e−4 규모로 격렬하게 진동**한다 (확대 삽입도가 그
진동만 따로 보여 준다). 검정·자홍은 그 구간에서 평평하게 0.
**NRMSE: PLS-6 0.101 % · +v_γ 0.106 % · β\* 0.112 %** — 4b 와 같은 순서.

`[인쇄]` 판정: "**z-scoring amplifies and feeds noise into the model**,
manifesting as the spiky regression coefficients … Still, the PLS model
associated with the z-scored data has **approximately the same prediction
accuracy** as the PLS model associated with the original data."

`[인쇄]` 규칙으로 정리한 문장: "if the coefficients are expected to **vary by an
order of magnitude** …, then **not z-scoring** the data accounts for the
assumption that the scale of the columns is correlated with the assumed
underlying true coefficients."

`[해석]` **§8.1 과 §8.2 는 정반대 결론을 낸다.** 참계수가 상수면 z-scoring 이
돕고, 참계수가 데이터 스케일을 따라가면 z-scoring 이 해친다. 그리고 어느
쪽인지는 **데이터가 말해 주지 않는다.** 이것이 이 논문의 두 번째 축(첫째는
정칙화 선택)이고, 우리에게는 **좌표 선택(Ah 축 vs SOC 정규화 축)** 문제로
번역된다 — [[pvs-sev-lli-lampe-separability]] 의 미결 Gap 과 같은 것이다.

---

## 9. §4.2.2 실측 cycle life 응답 (Fig. 6, 7, 8, Table 1) — 참계수를 모르는 경우

### 9.1 설계 `[인쇄]`

- 응답: cycle life 의 **로그**. 분할은 Severson 원안.
- `[인쇄]` "based on **only discharge data from two cycles**, which is a strategy
  to **reduce the risk of data leakage** (Geslin et al., 2023)."
- `[인쇄]` 정칙화 파라미터는 **최소 CV 오차**로, **1-SE 규칙을 쓰지 않는다.**
  각주 3 이 이유를 적는다: "The standard deviation of the CV error is large due
  to the **long-living cells** that heavily influence the prediction
  performance, which would lead to **overly conservative** regularization
  estimates."

`[해석]` 이 각주는 정직하지만 대가가 있다 — 1-SE 를 버리면 정칙화가 약해지고,
계수의 고주파 성분(= nullspace 쪽으로 흐르기 쉬운 성분)이 커진다. §4.1·§4.2.1
에서는 1-SE 를 쓰고 여기서만 버린 것이므로 **절 사이에 절차가 다르다.**

### 9.2 Fig. 6·7 (직접 봄) — 계수의 모양

`[도표]` **6a `β₅^PLS` (원 스케일)**: 2.0 V 에서 약간 음, 2.8–2.95 V 에서
완만한 양의 봉우리, **3.0–3.2 V 에서 고주파로 심하게 진동**(양·음 왕복),
3.25 V 위에서 ≈ 0. 전 구간에 잔물결이 얹혀 있다.
`[도표]` **6b `β_{D1}^{FL}` (fused lasso)**: 완전한 **조각상수 계단**.
2.0–2.1 음 → 2.1–2.35 약양 → **2.35–2.45 뚜렷한 음의 골** → 2.46–2.9 약양
평탄 → **2.93–3.0 큰 양의 계단** → 3.0–3.07 음 → 3.07–3.12 양 → 3.12–3.18
음 → **3.18–3.22 가장 깊은 음의 골** → 3.22–3.5 계단식 회복.
(★ 우리 크롭에서 6a 의 `a)` 라벨과 y축 눈금값 일부가 잘렸다. y축 값은
읽지 않았다.)

`[도표]` **7a `β₉^PLS` z-scored**: 3.0 V 위에서 **6a 보다 더 격렬하게** 진동
하며 3.15·3.35·3.45 V 에 큰 봉우리가 선다. 2.4 V 부근 음의 골은 유지.
`[도표]` **7b `β_{D1}^{FL}` z-scored**: 다시 조각상수. 6b 와 봉우리 위치가
대체로 같고, **3.13–3.19 V 에 좁고 높은 양의 스파이크**가 추가로 생겼으며
3.33–3.35 V 에도 작은 계단이 하나 더 있다.

`[인쇄]` 저자 서술: PLS 는 "high-frequency perturbations, in particular, in the
voltage range **3 2.9–3.2 V**, which is likely due to noise, making the PLS
coefficients **harder to interpret**." fused lasso 는 "clearly indicate **three
regions of importance**, enabling a physical interpretation." z-scored FL 의
추가 봉우리에 대해서는 "an additional peak appears around **3.35 V**, which
**could not be learned from the original data** because of the very small
variance of the data prior to rescaling in combination with regularization."

### 9.3 ★ 저자들이 붙인 물리 해석 (전문) — 우리 계보와 닿는 유일한 자리

`[인쇄]` §4.2.2, fused lasso 계수의 세 구간:

1. **2.0–2.1 V**: "associated with the **capacity change of the cell between
   cycles 10 and 100**."
2. **≈ 2.4 V (음의 봉우리)**: "**may correspond to LFP cathode degradation
   associated with iron anti-site defects**, as the free energy of reaction
   (overpotential times charge) exceeds their formation energy **∼0.55 eV**
   (Malik et al., 2010). This interpretation is also consistent with experiments
   showing that chemical reduction of LFP by citric acid is able to heal iron
   anti-site defects with a similar free energy of reaction of **0.58 eV**
   (Xu et al., 2020)."
3. **2.9–3.3 V**: "contains **most of the regression coefficient peaks**. The two
   dominant plateaus of the Open-Circuit Voltage (OCV), which result from the
   single broad plateau of LFP superimposed with two more narrow plateaus of
   graphite, are located here … These voltage plateaus correspond to **phase
   transformations of the porous electrodes** …, specifically between the low
   and high-density stable phases of LFP, as well as between **stages 1, 2, and
   3 of lithiated graphite**."

이어지는 문장들 `[인쇄]`:
- "The fused-lasso coefficients showcase three distinct negative and positive
  peaks, corresponding to changes in the **rate-dependent tilt of the voltage
  plateaus**, which may result from changes in particle-size-dependent
  nucleation barriers and population dynamics of reaction-controlled phase
  transformations."
- "The peak width and height can be interpreted as a **weighted sum of the
  average slopes of the data between the respective peaks**."
- **★ 우리 계보와 닿는 한 문장**: "On low-rate data, the position and magnitude
  of peaks in the **incremental capacity analysis correspond to different
  degradation modes (Dubarry et al., 2012)**. The peaks and peak shifts of the
  incremental capacity analysis **blur out at higher C-rates**, as expected from
  the suppression of phase separation by driven auto-inhibitory reactions
  (Bazant, 2017)."
- "the obtained regression coefficients indicate that there is **degradation
  information in this region even in 𝜟𝐐₁₀₀₋₁₀** (i.e., … both at **4C**) that is
  important for capturing past degradation and forecasting future degradation."
- "if the 4C current is well into the regime of suppressed phase separation, then
  we would expect a **negative correlation between lifetime and internal
  resistance** of the intercalation reaction, which in turn is correlated with
  larger 𝜟𝐐₁₀₀₋₁₀."

`[해석]` **이 문단이 이 논문에서 [[dubarry-mechanistic-mode-synthesis]] 계보와
만나는 유일한 지점이고, 만나자마자 갈라진다.** 저자들 자신이 "IC 봉우리 ↔
열화 모드" 대응은 **저율 데이터에서만** 성립하고 4C 에서는 뭉개진다고 적는다.
즉 **이 논문의 봉우리들은 열화 모드가 아니다** — 저자들도 그렇게 주장하지
않는다. 우리 축(LLI/LAM 분해)과 이 논문은 **데이터가 겹치되 미지수가 다르다.**

### 9.4 Table 1 (RMSE, 원문 인쇄값 그대로)

`[인쇄]` 캡션: "Low Cycle Life (CL): y_i ≤ 1200 cycles; high CL: y_i > 1200.
All models were trained on the entire training data."

| Set | FL D1 (원 스케일) | PLS 5 (원 스케일) | FL D1 (z-scored) | PLS 9 (z-scored) | Variance model (Severson) |
|---|---|---|---|---|---|
| Training (41) | 68 | 83 | 62 | **57** | 104 |
| Test 1 (**42**) | 115 | 116 | 105 | **102** | 138 |
| Test 2 (40) | 198 | 217 | 192 | **174** | 196 |
| Training low CL (39) | 62 | 82 | 53 | **50** | 103 |
| Test 1 low CL (39) | 96 | 101 | **76** | 80 | 96 |
| Test 2 low CL (34) | 135 | 202 | **115** | 132 | 119 |
| Training high CL (2) | 138 | **106** | 150 | 139 | 115 |
| Test 1 high CL (3) | 258 | **231** | 280 | 252 | 385 |
| Test 2 high CL (6) | 395 | **285** | 412 | 322 | 419 |

`[인쇄]` 판정: "both models on the z-scored data **outperform the variance
model** suggested by Severson et al. (2019). While being interpretable, fused
lasso provides comparable prediction accuracy than PLS. The PLS model with nine
components … **slightly outperforms** the fused lasso model when all cells are
considered. However, the fused lasso yields the **lowest RMSE for both test sets
when only evaluated on the shorter-lived cells**."

`[인쇄]` PLS 우세에 대한 자기 방어 셋: (a) 장수명 셀 때문 —
"mainly associated with the longest-living cells that are more difficult to
predict"; (b) `[인쇄]` "the coefficients associated with the PLS model are
**challenging to interpret because their sign changes frequently**";
(c) `[인쇄]` "the secondary test set was impacted by a **longer calendar aging**
due to an extended storing period before the cycling started …, making it tough
to understand the higher prediction accuracy of the PLS model on the secondary
test set."

`[해석]` **high CL 행의 표본 수가 2·3·6 이다.** 저 세 행의 숫자는 사실상
개별 셀 이야기이고, 그 위에 "장수명 셀 때문" 이라는 설명을 얹는 것은
과해석에 가깝다. 표에 표본 수를 적어 둔 것은 정직하다.

### 9.5 ★★ Fig. 8 (직접 봄) — 이 논문에서 축퇴 방향에 가장 가까운 그림

`[인쇄]` 캡션: "Comparison of fused lasso coefficients (blue) and **their
component orthogonal to the nullspace** (red): (a) Original data, (b) z-scored
data."

`[도표]` 8a: 파랑 `β_{D1}^{FL}` 은 조각상수 계단 (−3.2 ~ +1.7 범위). 빨강
`β_{D1⊥}^{FL}` 은 같은 큰 구조를 따라가되 **전 구간에 잔물결**이 얹히고,
**3.0–3.2 V 에서 −2.3 ~ +3.0 사이를 격렬하게 왕복**한다. 2.45–2.9 V 의 조용한
평탄 구간에서도 빨강은 ±0.3 규모로 흔들린다.
`[도표]` 8b (z-scored): 같은 구조. 파랑은 −0.013 ~ +0.023 의 계단, 빨강은
3.0–3.25 V 에서 −0.015 ~ +0.032 로 진동.

`[인쇄]` 이 그림의 요점: "The component of the regression coefficients
orthogonal to the nullspace … are **less interpretable while making identical
predictions on the training data**. … **Not requiring the coefficients
orthogonal to the nullspace improves interpretability**."

`[해석]` **이 그림이 "축퇴 방향을 그린 그림" 에 가장 가깝다** — 파랑과 빨강의
**차이**가 곧 nullspace 벡터이고, 그 차이가 큰 전압 구간이 곧 "데이터가
말이 없는 구간" 이다. 다만 **차이 자체를 따로 그리지는 않는다.** 우리가
그것을 그리면 곧바로 새 그림이 된다 (§12 에서 그 크기를 수치로 냈다).

**★ 그리고 이 그림이 §9.3 의 물리 해석과 정면으로 만난다**: 빨강과 파랑이 가장
크게 갈리는 구간이 **3.0–3.2 V** 인데, 그곳은 §9.3 이 "LFP 와 흑연의 상전이
평탄" 이라고 물리적으로 해석한 바로 그 구간이다. `[해석]` 즉 **가장 물리적으로
해석된 구간이 동시에 nullspace 자유도가 가장 큰 구간**이다. 논문은 이 두
사실을 같은 쪽(7–8쪽)에 인쇄해 놓고 **연결하지 않는다.** 우리가 §12 에서 이
관찰을 수치로 확인했다.

---

## 10. §5 결론 (원문 요지)

`[인쇄]` 네 문단으로 정리된다:
1. "The nullspace allows **different-looking regression coefficients to yield
   similar predictions** (Fig. 1)."
2. "While z-scoring for high-dimensional functional data can be beneficial, it
   should be an **active design choice** because it can increase noise by
   scaling up columns with low SNR (Fig. 5)."
3. "regularization and z-scoring must be carefully considered and **correspond to
   prior physical knowledge** … Otherwise, the combination of the nullspace and
   regularization can hinder interpretability and **potentially make it
   impossible to obtain regression coefficients close to the true
   coefficients**."
4. "Regression methods which yield coefficients orthogonal to the nullspace, such
   as RR, PCR, and PLS, **can be challenging to interpret**. Methods that yield
   regression coefficients **not orthogonal** to the nullspace, such as the fused
   lasso, can be advantageous for interpretability (Fig. 8)."

---

## 11. 저자 공개 저장소 해부 (`HDRegAnalytics`)

읽기만 했고 이 저장소에 복사하지 않았다. 파일 목록·행 수·핵심 코드만 옮긴다.

### 11.1 구조

```
src/nullspace.py            567줄   ★ Nullspace 클래스 (핵심)
src/plotting_utils.py       863줄   ★ plot_nullspace_analysis 등
src/utils.py                528줄   ★ 사영자 2종 + CV 최적화 + RMSE
src/hd_data.py              253줄   HD_Data (z-scoring, 잡음 주입, SNR)
src/basis_function_data.py  206줄   합성 데이터 생성 (다항/RBF/푸리에 기저)
Nullspace_Parabola_Examples.ipynb   312줄   → Fig. 1, 2, S1
Nullspace_LFP_examples.ipynb       1214줄   → Fig. 3–8, S2, S3, Table 1
regression_in_R/regression_lfp.R    274줄   fused lasso (genlasso) + CV
regression_in_R/utils.R             267줄   cv_genlasso 등
data/lfp_slim.csv                   124×1004
results/Nullspace/*.pdf             논문 그림 원본 20여 개
```

### 11.2 ★ 핵심 한 줄 (`src/nullspace.py:429`)

```python
v_[i, :] = -linalg.inv(g * self.XtX + I_) @ self.w
```

`self.w = self.w_alpha - self.w_beta` (`:128`) 이고 `g` 가 `γ` 다. 즉
**식 (19) 그대로**이며, `self.XtX` 자리에 우리 `JᵀJ` 를 넣으면 끝이다.
`XXᵀ` 역행렬이 필요 없다 — 조건수 문제를 우회한다.

동봉된 주석에서 저자 자신이 SVD 블록 방식을 시도했다가 접었다고 적는다
(`:446` `[인쇄]` "Working with block matrices. **This doesnt solve the issue of
poor conditioned X**....").

### 11.3 ★★ 저자가 null 방향을 그려 보고 포기한 자리 (notebook cell 36–37)

```python
NX = scipy.linalg.null_space(X_lfp_train)
...
ax[0].plot(np.linspace(3.5, 2.0, 1000), NX)      # 959개 기저 벡터를 한꺼번에
```

바로 아래 저자 주석 `[인쇄]`:

> "It's **difficult to interpret when visualized this way**. Scipy constructs the
> nullspace basis vectors in a particular way such that they are **orthogonal
> unit vectors which can be difficult to visualize (and interpret)**. Consider
> plotting the diagonal z-scoring matrix."

`[해석]` **이것이 이번 흡수에서 가장 중요한 발견 중 하나다.** "null 방향을
그린다" 는 시도는 **이미 있었고, 차원 때문에 실패했으며, 논문에 싣지
않았다.** 실패 원인은 `dim 𝒩(X) = 959` 이고 정규직교 기저의 개별 벡터가
물리적 의미를 갖지 않는다는 것이다.

**우리에게는 그 장애가 없다.** [[np-lip-ocv-reparametrization]] 이 준
null 방향은 **1차원이고 닫힌 형태로 알려져 있다**
(`(1−LLI, 1−LAM_NE, 1−LAM_PE)` 의 스칼라배). 3~4차원 파라미터 공간에서
`JᵀJ` 의 최소 고유벡터는 **유일하게 결정되고 그릴 수 있다.** 즉:

> **저자가 못 그린 이유는 우리에게 해당하지 않는다. 그 그림은 우리가
> 그릴 수 있고, 이 계보에서 아무도 그리지 않았다.**

### 11.4 ★ 본문에 없는 데이터 조작 (notebook cell 4 / R 스크립트 :44)

Python `[인쇄]`:
```python
# Remove single outlier in the test set.
# Reason: Very different shape and a lot lower cycle life than all other cells.
# Degradation is not linear.
id_outlier_test = np.where(np.mean(X_lfp_test, axis=1)==np.min(np.mean(X_lfp_test, axis=1)))
X_lfp_test = np.delete(X_lfp_test, id_outlier_test, axis=0)
```
R `[인쇄]`: `test1_id[43] <- F # Removing the shortest lived outlier battery!`

`[재현]` 제거된 셀: 일차 시험셋 내 21번, **cycle life 148**, 충전 프로토콜
class 23. 제거 후 일차 시험셋의 수명 범위는 335 ~ 2237.

`[해석]` 본문은 **학습셋의** 최단수명 셀을 남긴다고만 적고 **시험셋에서 셀을
뺐다는 말은 없다.** 유일한 흔적은 Table 1 의 `Test 1 (42)` 이다 (원 분할은
43). 제거 사유가 `[인쇄]` "Degradation is not linear" 인데, 이것은 **선형
모형이 못 맞히는 셀이라서 뺐다**는 뜻으로 읽힌다 — 시험셋 조작으로는 가장
피해야 할 종류다. §15.4 에서 다시 다룬다.

### 11.5 교차검증 설계 (R `regression_lfp.R`)

```R
nfolds <- 10
N <- nrow(X_train_)                       # 41
foldid <- sample(rep(seq(nfolds), length = N))
cv_list = cv_genlasso(X_train_, y_train_, D1, foldid, y_train_list)
```

`[해석]` **무작위 10-fold**이고 group 이 없다. `[재현]` 학습 41셀의 충전
프로토콜 class 는 40종(중복 1쌍)이므로 학습 fold 내부의 프로토콜 누수는
사실상 없다. 다만 `[재현]` **일차 시험셋 43셀 중 22셀이 학습셋과 같은 프로토콜
class 를 공유**한다 (Severson 원 분할의 성질이며 이 논문이 만든 것이 아니다).
`[해석]` 이 논문의 입력은 프로토콜 식별자가 아니라 **측정 곡선**이므로
[[fused-lasso-feature-design-framework]] 가 지적한 형성-프로토콜 누수와
같은 문제는 아니다. 그러나 "시험셋 성능" 을 셀-대-셀 일반화의 증거로 읽을
때는 이 사실을 알고 읽어야 한다.

---

## 12. `[재현]` 우리가 직접 돌린 것 (원문에 인쇄돼 있지 않은 수치)

저자 공개 데이터 `data/lfp_slim.csv` + 저장소가 배포한 fused lasso 계수
`regression_in_R/lfp_cl_D1_cv_reg_coeff.csv` (두 번째 열 = `coef_D1_cv`) 로
계산했다. 스크래치패드에서만 돌렸고 이 저장소에 코드를 남기지 않았다.
**인용 근거로 쓰면 안 된다 — 원문 수치가 아니다.**

### 12.1 nullspace 의 크기와 조건수

| 양 | 값 |
|---|---|
| `X_train` 모양 | 41 × 1000 |
| `dim 𝒩(X_train)` (원 데이터) | **959** |
| `dim 𝒩(X_train)` (열 평균중심 후) | **960** (rank 41 → 40) |
| `dim 𝒩(X_train)` (z-scored) | **960** |
| `cond(X_train)` 원 데이터 | 3.31e3 |
| `cond(X_trainᵀX_train)` | 1.09e7 |
| `cond(X_train Xᵀ)` 평균중심 후 | **2.13e17** |

`[해석]` **평균중심을 하는 순간 `XXᵀ` 가 특이해진다** (행이 하나 종속). 논문
식 (14) 는 `[인쇄]` "where 𝐗𝐗ᵀ **is assumed to be invertible**" 라고 전제하는데
논문 자신의 전처리(평균중심)가 그 전제를 깬다. 실제 코드는 식 (19) 를 쓰므로
문제가 드러나지 않고, 노트북도 `scipy.linalg.null_space` (SVD 기반) 를 쓴다.
`[해석]` **식 (14) 를 그대로 옮겨 쓰면 안 된다는 뜻이고, 우리에게는 애초에
식 (19) 가 맞는 도구다.**

### 12.2 fused lasso 계수 중 데이터가 정하지 않는 몫

```
‖β_FL‖              = 28.35
‖β_FL 의 nullspace 성분‖ = 10.34   →  노름의 36.5 %
‖β_FL⊥‖             = 26.40   →  노름의 93.1 %
학습 데이터 예측 차이 max|X(β_FL⊥ − β_FL)| = 1.3e−15   (기계 정밀도)
점별 최대 변화 max|β_FL − β_FL⊥| = 2.09   (max|β_FL| = 3.18)
```

`[해석]` **논문 Fig. 8 의 정량판이다.** 계수 벡터 노름의 **36.5 %** 가 학습
데이터에 대해 **완전히 자유**하고, 어떤 전압점에서는 계수가 **2.09 만큼**
움직여도 예측이 기계 정밀도 수준에서 변하지 않는다 (그 지점 최대 계수가
3.18 이므로 **크기의 3분의 2**).

### 12.3 ★ 그 자유도가 어느 전압 구간에 있는가 (논문이 하지 않은 계산)

전압을 0.1 V 구간으로 나누어 `‖β_FL 의 nullspace 성분‖` 을 잰 것:

| 전압 구간 | nullspace 성분 노름 | `β_FL` 노름 | 비 |
|---|---|---|---|
| 2.0–2.1 | 1.81 | 4.32 | 0.42 |
| 2.1–2.2 | 1.43 | 0.60 | **2.38** |
| 2.2–2.3 | 2.29 | 1.52 | **1.51** |
| 2.3–2.4 | 2.29 | 5.74 | 0.40 |
| 2.4–2.5 | 1.15 | 4.57 | 0.25 |
| 2.5–2.6 | 1.78 | 1.60 | 1.11 |
| 2.6–2.7 | 1.81 | 1.40 | 1.29 |
| 2.7–2.8 | 2.14 | 0.98 | **2.20** |
| 2.8–2.9 | 1.57 | 1.05 | 1.50 |
| 2.9–3.0 | 2.45 | 8.75 | 0.28 |
| **3.0–3.1** | **5.14** | 8.01 | 0.64 |
| **3.1–3.2** | **5.16** | 16.07 | 0.32 |
| **3.2–3.3** | **4.07** | 16.92 | 0.24 |
| 3.3–3.4 | 0.44 | 5.43 | 0.08 |
| 3.4–3.5 | 0.76 | 2.74 | 0.28 |

`[해석]` 두 가지가 보인다:
1. **절대 크기로는 3.0–3.3 V 가 압도적**이다 (다른 구간의 2~4배). 그 구간이
   §9.3 에서 "LFP·흑연 상전이 평탄" 으로 물리 해석된 바로 그 구간이고,
   Fig. 8 에서 빨강이 가장 크게 요동친 구간이다. **세 관찰이 일치한다.**
2. **상대 비로는 2.1–2.2 와 2.7–2.8 이 최악**(2.2~2.4배)이다. 그 구간은
   계수가 작아 논문이 아무 해석도 붙이지 않은 곳이다 — 즉 "해석 안 한 곳" 이
   "정보가 없는 곳" 과 일치한다는 점에서는 다행이지만, **계수가 작다는
   이유로 무시한 것이 우연히 맞았을 뿐**이다 (§8.1 Fig. 4a 가 그 추론이
   틀릴 수 있음을 보인다).

**주의**: 이 표는 "`β_FL` 이 실제로 가진 nullspace 성분" 이지 "그 구간에서
계수가 변할 수 있는 최대치" 가 아니다. 후자는 무한대다 (nullspace 는
부분공간이므로 스케일이 자유롭다). 이 표가 재는 것은 **fused lasso 라는
특정 정칙화가 그 구간에서 얼마나 큰 자유도를 소비했는가**다.

---

## 13. 그림 — 본 것과 안 본 것 (정직하게)

크로핑 결과 `wiki/raw/figures/schaeffer2024_nullspace-regularization-interpretation/`
에 **본문 8장 + SI 2장 + 표 1장 = 11장**.

**직접 열어 본 것 (9장 — 본문 8장 전부 + SI 1장)**:
- `fig_1.png` — 포물선 데이터 + nullspace 관점 ★ 핵심
- `fig_2.png` — RR vs fused lasso ★ 핵심
- `fig_3.png` — LFP 데이터 3패널 (원/평균중심/z-scored)
- `fig_4.png` — 상수 참계수, 원 스케일 vs z-scored ★ 핵심 (크기=중요도 반례)
- `fig_5.png` — 열평균 참계수, 원 스케일 vs z-scored
- `fig_6.png` — cycle life 계수 (PLS-5 / FL D1, 원 스케일) ★ 물리 해석 대상
- `fig_7.png` — cycle life 계수 (PLS-9 / FL D1, z-scored)
- `fig_8.png` — **fused lasso vs 그 직교 성분** ★★ 축퇴에 가장 가까운 그림
- `fig_S2.png` — SNR 지도 (SI §S5)

**안 본 것 (2장)**:
- `fig_S1.png` (SI Fig. S1) — 포물선 예제의 예측 산점도. **안 봤다.** 본문
  §4.1 이 그 내용(NRMSE 0.104/0.105%)을 이미 인쇄하고 SI 텍스트도 같은 값을
  적으므로 그림에서 새로 얻을 것이 없다고 판단했다.
- `tab_1.png` (Table 1) — **이미지로 읽지 않았다.** PDF 텍스트에서 숫자를
  그대로 옮겼다 (§9.4). 추출기 안내대로다.
- SI Fig. S3 (cycle life 예측 산점도) — **추출기가 영역을 찾지 못해 크롭이
  없다** (`제외 1건: fS3 p4 영역 없음`). SI 텍스트에 인쇄된 RMSE 값
  (FL z-scored: train 61.6 / test1 105.1 / test2 191.6, `<1200`: 53.3 / 76.5 /
  115.0 · PLS-9 z-scored: 57.5 / 102.0 / 174.5, `<1200`: 49.8 / 79.5 / 132.3)
  은 Table 1 의 반올림 전 값과 일치한다.

**본문 서술과 어긋난 그림이 있었는가 — 하나 있다 (사소)**:
- SI Fig. S2b 의 평균 `X̄` 가 **양수**로 그려져 있는데 `[재현]` 실제 데이터의
  평균은 같은 크기의 **음수**다 (2.0 V: −0.0111, 2.9 V: −0.0467). 크기는
  소수 넷째 자리까지 일치한다. `[해석]` 절댓값 또는 부호 반전을 그린 것으로
  보이며 논문에 그 언급이 없다. Fig. 3a 는 음수로 올바르게 그려져 있다.
- 그 밖에 본문 서술과 그림이 어긋난 곳은 **찾지 못했다.** Fig. 4a 의
  "3.2–3.5 V 차이가 nullspace 에 있다", Fig. 5b 의 "z-scoring 이 잡음을
  키운다", Fig. 8 의 "직교 성분이 덜 해석 가능하다" 는 전부 그림과 맞는다.
- **크롭 품질 주의**: `fig_6.png`·`fig_7.png` 는 왼쪽 y축 눈금값과 `a)` 라벨
  일부가 잘렸다. 그래서 §9.2 에서 y축 **수치는 읽지 않고** 모양만 기술했다.

---

## 14. 우리 프로젝트와의 접점

### 14.1 ★ 즉시 채택할 것 — 축퇴 방향을 그리는 절차

우리 문제로의 사전(辭典):

| 논문 | 우리 |
|---|---|
| `X ∈ R^{n×p}` 설계행렬 | `J(θ) = ∂(모델 곡선)/∂θ ∈ R^{n_점 × 3}` Jacobian |
| `𝒩(X)` (959차원, 전역) | `J` 의 **최소 특이값 방향** (1차원, `θ` 국소) |
| `XᵀX` | `JᵀJ` = Gauss–Newton Hessian ≈ Fisher (Lin 의 `C_θ⁻¹`) |
| `β_A − β_B = β_Δ` | 두 열화 조합의 차 `θ_A − θ_B` |
| 식 (19) `v_γ = −(γXᵀX+I)⁻¹β_Δ` | **그대로** |
| NRMSE 제약 (23) | 우리 목적함수 `J(θ)` 의 허용 증가폭 |

**절차 (미실행, 값이 싸다)**:
1. 22p 동작점 `θ₀` 에서 `J` 를 수치 미분으로 구한다 (곡선 격자점 × 3 모드).
2. `JᵀJ` 의 고유분해 → **최소 고유벡터 `u_min`** 과 고유값 스펙트럼.
   `[해석]` 예측: `u_min` 이 [[np-lip-ocv-reparametrization]] 의 닫힌 형태
   방향 `(1−LLI, 1−LAM_NE, 1−LAM_PE)` 스칼라배와 정렬해야 한다. **이 정렬
   여부가 해석해의 수치 검증이 된다** — 이 위키가 그 방향을 인쇄만 하고
   확인한 적이 없다.
3. `θ₀ ± t·u_min` 을 따라 곡선을 그려 **눈으로 겹쳐 보인다** (논문 Fig. 1b 의
   우리 판). 동시에 `θ₀ ± t·u_max` 도 그려 대조군으로 둔다.
4. `objective_function_trajectory` 의 우리 판: `t` 를 로그 스케일로 쓸며
   목적함수 증가량을 그린다 → **flat valley 의 폭을 물리 단위로** 준다.
5. 논문 식 (23) 의 `c` 를 우리 노이즈 수준으로 잡으면
   **"측정 잡음 안에서 구별 불가능한 열화 조합의 집합"** 이 그대로 나온다.
   그것이 이 프로젝트가 지금까지 격자 스캔으로 근사하던 것의 **직접 계산판**
   이다.

### 14.2 ★ 두 번째 채택 — "직교 성분" 대조 그림 (Fig. 8 의 우리 판)

우리 fitting 이 낸 `θ̂` 를 `J` 의 행공간에 사영한 `θ̂_⊥` 와 겹쳐 그린다.
차이가 크면 **fitting 이 낸 값의 그만큼이 데이터가 아니라 optimizer·초기값·
경계가 정한 것**이라는 시각적 증거가 된다. `[해석]` 이것은
[[22p-physics-or-degeneracy]] Status Log 2026-08-20 의 관찰("좌표 원점이
격자마다 다른 국소해로 수렴")에 **정량 형태**를 준다.

### 14.3 우리가 이 논문에 공급할 수 있는 것

1. **저자가 못 그린 그림.** §11.3 의 실패는 차원 문제이고 우리에게는 없다.
   "1차원 null 방향을 물리 좌표에서 그리고, 그 방향을 따라 관측이 얼마나
   변하는지 보인다" 는 그림은 이 계보 열한 편 어디에도 없다.
2. **비선형 확장.** 이 논문의 전 결과가 선형이다. 우리 Jacobian 판정은
   "국소 nullspace 는 동작점에 따라 회전한다" 는 것을 보일 수 있고,
   그것은 논문의 전역 결론이 갖지 못하는 정보다.
3. **`γ` 를 손으로 고르지 않는 방법.** 우리는 잡음 수준을 안다(합성 truth).
   식 (23) 의 `c` 를 잡음에서 유도할 수 있다.

### 14.4 채택하지 **않을** 것 — 경계를 분명히

- **z-scoring 논쟁은 우리 문제에 그대로 오지 않는다.** 우리 미지수는 3개이고
  단위가 같은 비율이다. 대응물은 오히려 **"어느 축에서 곡선을 볼 것인가"**
  (Ah 축 vs SOC 정규화) 이고, 그것은 [[np-lip-ocv-reparametrization]] 의
  2 자유도 정리가 지배한다.
- **fused lasso 를 우리 fitting 에 도입할 이유는 없다.** 우리 파라미터는
  순서가 없고 3개뿐이다 (fused lasso 는 `[인쇄]` "requires predictors that can
  be ordered"). 단 우리가 **곡선을 회귀 입력으로 쓰는 별도 분석**(예: 곡선 →
  모드 회귀)을 한다면 그때는 전부 적용된다.
- **이 논문의 LFP 결과는 우리 축의 근거가 아니다.** LLI/LAM 0회, half-cell
  0회, 응답이 cycle life 하나. §9.3 이 유일한 접점이고 거기서도 저자들이
  "4C 에서는 IC ↔ 모드 대응이 뭉개진다" 고 스스로 적는다.

---

## 15. 비판 — 이 논문의 약한 곳

### 15.1 `γ` 가 결론의 진폭을 정하는데 선택이 임의적이다

`[인쇄]` "We **hand-selected** γ = 10", "Here we **hand-selected** γ = 0.1, as a
different example". 자동 선택(식 23)은 비볼록이라 `[인쇄]` "solved by plotting
the left-hand side of the inequality with respect to γ" 라고 각주에 적는다.
`v_γ` 의 진폭이 곧 "차이의 얼마가 nullspace 탓인가" 의 답이므로 **결론의
크기가 저자의 선택에 의존한다.** 논문은 `γ` 민감도 분석을 하지 않는다
(코드에는 `objective_function_trajectory` 가 있는데 논문에 안 실렸다).

### 15.2 ★ 경고해 놓고 스스로 그 함정에 들어간다

논문은 §1 에서 "계수의 봉우리·평탄·기울기를 물리적 기대와 대조하는 것이
**오도할 수 있다**" 고 적고, §4.1 에서 "**데이터만으로는 참계수의 모양을 말할
수 없다**" 고 못 박는다. 그런데 §4.2.2 에서는 **참계수를 모르는 실측 응답**의
fused lasso 계수 봉우리에 **철 반사이트 결함 형성에너지 0.55 eV** 까지 붙여
해석한다. 방어 장치는 두 가지뿐이다:
- 조동사 헤지 ("**may** correspond", "**could** be interpreted"),
- fused lasso 를 골랐다는 것 자체가 사전지식 반영이라는 논리.

`[해석]` 두 번째 방어는 순환적이다. 논문의 명제는 "**정칙화가 사전지식과
맞으면** 해석 가능하다" 인데, 사전지식이 맞는지는 데이터로 확인 불가라고
스스로 적었다. 그러면 §4.2.2 의 해석은 **검증 불가능한 전제 위의 해석**이다.
그리고 §12.3 이 보인 대로, 물리 해석이 가장 조밀하게 붙은 3.0–3.3 V 가
**nullspace 자유도가 가장 큰 구간**이다.

**우리 쪽 함의**: 이 자기모순은 우리에게도 그대로 온다. 우리가 축퇴 방향을
그린 뒤에도 "그 방향 위 어디에 참값이 있는가" 는 여전히 사전지식이 정한다.
우리가 할 수 있는 정직한 주장은 **"어디까지가 데이터인지 선을 긋는 것"**
까지다.

### 15.3 비교 기준이 불공평하게 설정돼 있다

PLS 는 CV **최소** 오차로 성분 수를 골라 9성분까지 가고(=정칙화 약함), fused
lasso 도 최소 CV 로 골랐지만 **구조적 패널티**가 별도로 걸린다. 그런 뒤
"PLS 계수는 부호가 자주 바뀌어 해석하기 어렵다" 고 결론짓는다. `[해석]` 부호가
자주 바뀌는 것은 **PLS 의 성질이 아니라 이 정칙화 설정의 결과**일 수 있다.
§4.1·§4.2.1 처럼 1-SE 규칙을 썼다면 PLS 계수도 훨씬 매끄러웠을 것이고,
논문은 그 비교를 보여 주지 않는다.

### 15.4 시험셋에서 셀을 빼고 본문에 적지 않았다

§11.4. 사유가 `[인쇄]` "Degradation is **not linear**" 이라 더 나쁘다 —
**모형 가정에 맞지 않아서 시험 표본을 뺀 것**이다. 영향 크기는 작을 수 있으나
(그 셀 하나가 42개 중 하나) `Test 1` 행 전체가 그 조작 위에 있다.
**이 논문의 결론(해석 가능성)에는 영향이 없지만 Table 1 의 비교에는 영향이
있다** — Severson 의 variance model 과 나란히 놓인 열이기 때문이다.

### 15.5 어휘 고립 (§3.1)

`identifiability`·`non-uniqueness` 를 한 번도 쓰지 않아, 같은 문제를 다루는
시스템동정·전기화학 문헌과 **검색으로 만나지 않는다.** 실제로 이 논문은
Lin & Khoo 2024 를 인용하지 않고, Lin & Khoo 도 이 논문을 인용하지 않는다
(`nullspace` 0회). `[해석]` 이 위키가 두 편을 나란히 놓은 것 자체가 작은
기여다.

### 15.6 잘한 점도 적는다 (공정하게)

- **코드와 데이터를 전부 공개했고 실제로 돌아간다.** §12 의 재현이 30분 안에
  됐다. 이 계보 열한 편 중 재현성이 가장 좋다.
- **자기 방법의 한계를 코드 주석에 남긴다** (§11.2, §11.3). 논문에 못 실은
  실패를 지우지 않았다.
- **합성 응답으로 참계수를 아는 실험을 설계했다** (§8). "예측이 맞는가" 와
  "계수를 되찾았는가" 를 분리한 것은 이 계보에서 드물다.
- **Table 1 에 표본 수를 괄호로 전부 적었다** (high CL 이 2·3·6 이라는 것을
  숨기지 않는다).

---

## 16. 한 줄 결론

**이 논문은 우리 축퇴의 *증거* 를 주지 않는다 (LLI/LAM 을 재지 않는다).
주는 것은 *도구* 다 — 식 (19) 의 `γ`-완화 사영과 "직교 성분 대조" 그림이,
Lin & Khoo 가 닫힌 형태로 인쇄만 해 놓은 우리 null 방향을 *그리는* 방법이다.
그리고 저자 자신이 그 그림을 시도했다가 차원(959) 때문에 포기했다는 사실이
저장소 주석에 남아 있다 — 우리 null 방향은 1차원이므로 그 장애가 없다.**

---

## 관련 위키 페이지

- [[nullspace-coefficient-interpretation]] — 이 digest 에서 컴파일된 개념 페이지
- [[fitting-degeneracy]] — 우리 축퇴의 본진. §14.1 의 절차가 여기로 들어간다
- [[np-lip-ocv-reparametrization]] — 그릴 대상(닫힌 형태 null 방향)을 준 문헌
- [[22p-physics-or-degeneracy]] · [[pvs-sev-lli-lampe-separability]] — 열린 질문 2종
- [[fused-lasso-feature-design-framework]] — 이 논문을 `[13]` 으로 인용한 후속 논문
- [[zhang2020-eis-aging-dataset]] — 같은 계보의 관측 선택 비식별성 사례
- [[dubarry-mechanistic-mode-synthesis]] — §9.3 이 인용한 모드 계보
