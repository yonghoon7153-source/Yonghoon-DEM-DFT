---
title: "Lee et al. 2020 — Estimation Error Bound of Battery Electrode Parameters With Limited Data Window (IEEE TII 16(5), 3376-3386)"
source_url: local-upload/55c52065-Estimation_Error_Bound_of_Battery_Electrode_Parameters_With_Limited_Data_Window.pdf
ingested: 2026-09-04
sha256: c97eb857507889b4d8ad821f506e8363f22a448bf8501a32fde73e0d8b3c8ead
---

# 수집 목적

Suhak Lee, Peyman Mohtat, Jason B. Siegel, Anna G. Stefanopoulou, Jang-Woo Lee,
Tae-Kyung Lee, **"Estimation Error Bound of Battery Electrode Parameters With
Limited Data Window"**, *IEEE Transactions on Industrial Informatics* **16**(5),
May 2020, 3376–3386 의 **절별 해체분석**.

이 편은 [[np-lip-ocv-reparametrization]] (Lin & Khoo 2024) 가 자기 참고문헌
`[15]` 로 지목하며 Mohtat 2019 `[11]` 과 함께 **"Fisher 로 식별 가능성을 정량한
선행자"** 로 인정한 문헌이다. Mohtat 2019 는 2026-09-04 에
`raw/papers/mohtat2019_electrode-soh-estimability-expansion.md` 로 흡수했고,
**Mohtat 은 이 편의 제2저자**이며 이 편은 Mohtat 2019 를 `[16]` 으로 인용한다.
즉 같은 UMich 그룹의 **같은 4-파라미터 좌표를 쓰는 자매편**이다.

이 digest 의 무게중심은 "이 논문이 무엇을 발견했나" 가 아니라 흡수 요청서가
지정한 **다섯 판정**이다:

1. 오차막대를 **어떤 좌표**에서 냈나 (파라미터 벡터가 무엇인가)
2. **비대각(상관)** 을 보고하는가
3. "limited data window" 가 정확히 **무엇의 구간**인가
4. 어휘 전수 (조판 함정 포함)
5. `LLI`·`LAM` 이 **몇 쪽·어느 절**에 나오는가

**표기 규칙** (이 위키 관례 3구분):
- `[인쇄]` — 논문 본문/표/식/캡션에 **글자로** 있는 것. 그림 **안에 조판된
  숫자 라벨**은 `[인쇄, Fig. N 라벨]` 로 따로 적는다 (눈대중이 아니다).
- `[도표]` — 그림에서 **눈으로 읽은** 근사값·곡선 모양 (원 데이터가 아니다)
- `[해석]` — 이 문서를 쓰면서 붙인 판단. **논문의 주장이 아니다**

**쪽 인용 규약 (중요)**: 이 PDF 는 IEEE 조판본이며 **11쪽**이다. 인쇄된
러닝 헤더가 `3376`…`3386` 을 달고 있어 **PDF 인덱스 i ↔ 인쇄 쪽번호 3375+i**
로 정확히 대응한다 (PDF p.1 = 인쇄 3376, PDF p.11 = 인쇄 3386).
**이 digest 의 모든 쪽 인용은 PDF 인덱스 1–11 기준**이며, 필요하면 3375 를
더해 인쇄 쪽으로 바꾼다. 본문은 PDF p.1–10(인쇄 3376–3385), 참고문헌은 p.10
하단–p.11, 저자 약력은 p.11 이다. **Supporting Information 없음.**

- 원본 파일: 로컬 업로드 PDF 11쪽
- 크로핑 그림: `raw/figures/lee2020_estimation-error-bound-limited-data-window/`
  (Fig. 1–10, 10장, `figures.json` 에 캡션 색인). Table I–IV 는 캡션 기반
  추출기에 안 잡히므로 **쪽 렌더로 따로 읽었다** (§4 에 무엇을 봤는지 명시).

---

## 0. 서지사항 (직접 확인)

`[인쇄]` PDF p.1 헤더·각주 + p.10–11 에서 확인:

| 항목 | 값 | 확인처 |
|---|---|---|
| 저자 | Suhak Lee (교신), Peyman Mohtat, Jason B. Siegel (Member, IEEE), Anna G. Stefanopoulou (Fellow, IEEE), Jang-Woo Lee, Tae-Kyung Lee | p.1 |
| 소속 | Department of Mechanical Engineering, University of Michigan, Ann Arbor, MI 48109 USA / **System Development Team, Samsung SDI Co., Ltd., Yongin-si 17084, South Korea** (J.-W. Lee, T.-K. Lee) | p.1 |
| 학술지 | *IEEE Transactions on Industrial Informatics* **16**(5), May 2020, pp. 3376–3386 | p.1 헤더 |
| DOI | `10.1109/TII.2019.2952066` | p.1 좌하단 |
| 접수 / 게재확정 / 온라인 / 현판 | 2019-09-30 / 2019-10-20 / 2019-11-18 / 2020-02-06 | p.1 각주 |
| Paper no. | TII-19-4479 | p.1 각주 |
| 자금 | **Samsung SDI Company, Ltd.** 지원 | p.1 각주 |
| 라이선스 | Creative Commons Attribution 4.0 | p.1 하단 |
| Index Terms | Estimation error bound · battery electrode parameters · **Cramer-Rao bound** · confidence interval · **data window** | p.1 |

`[해석]` 자금 출처가 Mohtat 2019(미 육군 TARDEC)와 다르고 **Samsung SDI** 이며
공저자 2인이 SDI 소속이다. Mohtat 2019 가 셀 팽창 센서(연구실 장비)로 관측을
늘리는 쪽이었다면, 이 편은 **BMS 가 실제로 얻을 수 있는 데이터 구간**을 묻는
산업 쪽 질문이다.

---

## 1. 요청된 다섯 판정 — 결론 먼저

| # | 질문 | 판정 | 핵심 근거 |
|---|---|---|---|
| 1 | 오차막대의 좌표 | **전극 파라미터 좌표. 모드 좌표 아님.** `θ = [y₁₀₀, C_p, x₁₀₀, C_n]` (식 7 아래, p.2) | Table II·III·IV 의 열 머리가 `θ₁ = y₁₀₀, θ₂ = C_p, θ₃ = x₁₀₀, θ₄ = C_n`. **`LLI`·`LAM` 에 대한 오차막대는 논문 전체에 없다** |
| 2 | 비대각(상관) 보고 | **부분적으로 예 — 이 계보에서 처음.** 다만 (a) 헤드라인 수치는 전부 `sqrt(diag)`, (b) 그림 하나(Fig. 7)에만, (c) 한 데이터 창(DW-deep)에서만, (d) **수치 ρ 는 0회**, (e) **모드 좌표로 전파 안 함** | 식 (19) `SE = [sqrt(Σ)]_kk` ↔ **Fig. 7 은 6개 쌍 전부에 95 % 오차 타원**(제약 유/무 2종)을 그린다. p.8 `[인쇄]` "a **strong correlation** has been observed among the parameters from the same electrode … However, the parameters from the **different electrodes do not show any correlation**." + 식 (26) `σ_y·α = σ_x·β` |
| 3 | "limited data window" 의 정체 | **DOD 구간** (전압 구간도 SOC 구간도 아님). `DW = [Q_s, Q_e]`, `Q` = 완충에서의 방전 Ah, `DOD = Q/C` | p.4 §IV-A + Fig. 2. Table IV 에 네 창의 범위가 **인쇄돼 있다**: shallow `[0.0, 0.2]` · medium `[0.3, 0.7]` · non-full `[0.1, 0.5]` · deep `[0.0, 0.9]`. 처방 예시: `[인쇄, p.10]` σ̂ = 10 mV, 목표 10 %, 95 % → **DOD = [0.35, 0.73]** |
| 4 | 어휘 전수 | §5 표. **`identifiab*` 16회 (본문)**, `Fisher` 3, `Cramer` 3, `covarianc*` 2, **`correlat*` 3**, `estimab*` 0, `degenerac*` 0, `global` 0, `condition number` 0 | §5. **조판 함정**: `ﬁ` 합자 때문에 순진하게 세면 `identifiab*` 이 **0회로 나온다** (§5 경고) |
| 5 | `LLI`·`LAM` 위치 | **p.1(인쇄 3376) 서론 각 1회 + p.3(인쇄 3378) §III-A 에 LLI 5회·LAM 7회. 그 외 0회** — §IV 결과·§V 검증·§VI 지침·§VII 결론에 **한 번도 안 나온다** | §5 쪽별 분포표 |

**`[해석]` 한 줄 판정**: 이 편은 Mohtat 2019 와 **같은 좌표에서 같은 종류의
막대**를 세운다. 다만 **비대각을 그림 한 장에서 실제로 그린다** — 우리 위키가
"이 계보는 `Σ` 를 구해 놓고 대각선만 인쇄한다" 고 적어 둔 문장은 **이 편
앞에서 예외를 하나 인정해야 한다.** 그러나 그 타원은 **전극 파라미터
좌표**에 있고, **수치가 없고**, **모드로 전파되지 않는다.**

---

## 2. 절별 해체분석

### §I. Introduction (p.1–2, 인쇄 3376–3377)

**문제 설정**: 셀 단위 lumped SOH(용량 감소·저항 증가)는 "열화 상태의 상세를
주지 못한다" 며 전극별 SOH(eSOH)로 간다. OCV 를 쓰는 이유는
`[인쇄, p.1]` "the OCV is simply the voltage difference between the half-cell
potential of positive and negative electrodes … it provides a **thermodynamic
fingerprint** of each electrode without complex electrochemical dynamics such as
diffusion and lithium intercalation."

**선행 계보를 스스로 정리한 문단** (p.1) — 우리 위키가 이미 흡수한 문헌들이다:
- `[3]` **Dubarry 2012** — "explained the electrode contributions to the cell OCV
  curve for various degradation modes" ([[dubarry-mechanistic-mode-synthesis]])
- `[4]` **Birkl 2017** — "showed excellent diagnostic results with multiple
  coin-cells representing different levels of degradation modes, namely, LAM and
  LLI" ([[birkl-ocv-degradation-diagnostic]])
- `[5]` Han 2014, `[6]` Lee 2018 (ASME DSCC) — "characterized the cell OCV model
  with specific electrode SOH (eSOH) parameters, **electrode capacity and
  utilization range**"
- `[7]` Dey 2019 — 실시간 전극 단위 추정

**측정 현실 논변** (p.1 하단): 정확한 OCV 측정은 비실용적이므로 C/20 정도의
느린 CC 측정을 pseudo-OCV 로 쓴다. `[인쇄]` 28 kWh 이상 팩을 1.4 kW level-1
충전기로 완충하려면 "at least 20 h" 이므로 그 자체가 C/20 급이다 → BMS 가
가끔 느린 충전 프로토콜을 요청하는 시나리오, 또는 key-ON 휴지 전압 수집.

**공백 선언** (p.2, 인쇄 3377) — 이 논문의 존재 이유:
`[인쇄]` "In literature, prior work used the **Fisher information matrix-based
Cramer–Rao bound (CRB)** to evaluate the parameters' identifiability. Cell-level
lumped parameters … are investigated using an equivalent circuit model
`[10]`–`[13]`. … Edouard et al. `[14]` presented a sensitivity analysis …
Forman et al. `[15]` proposed a multiobjective genetic algorithm associated with
the **Fisher identifiability analysis** … **However, the estimation uncertainty
of the eSOH-related parameters has not yet been studied.**"

`[해석]` 즉 저자들이 스스로 잡은 빈칸은 "**eSOH 파라미터**의 추정 불확실성"
이다 — **"열화 모드의 추정 불확실성" 이 아니다.** 이 한 줄이 판정 1을 이미
확정한다. 참고로 `[11]`–`[13]` 은 Xinfan Lin 계열의 등가회로 CRB 이고,
Mohtat 2019 는 여기가 아니라 §III-A 에서 `[16]` 으로 인용된다.

### §II. Parameterization of Open-Circuit Voltage (p.2, 인쇄 3377)

Mohtat 2019 §2 와 **동일한 창 매개화**다. 순서대로 인쇄된 식:

```
V_oc(z) = U_p(y) − U_n(x)                                        (1)
z = Q/C = (y − y₁₀₀)/(y₀ − y₁₀₀) = (x₁₀₀ − x)/(x₁₀₀ − x₀)        (2)
V_max = U_p(y₁₀₀) − U_n(x₁₀₀)                                    (3)
V_min = U_p(y₀)   − U_n(x₀)                                      (4)
C = C_p (y₀ − y₁₀₀) = C_n (x₁₀₀ − x₀)                            (5)
y = y₁₀₀ + Q/C_p ,   x = x₁₀₀ − Q/C_n                            (6)
V_oc(Q; θ) = U_p(y₁₀₀ + Q/C_p) − U_n(x₁₀₀ − Q/C_n)               (7)
```

- `z` = DOD (`[인쇄]` "z is the DOD of the cell (i.e., DOD = 1−SOC)")
- `Q` = `[인쇄]` "the discharge Amp-hours from fully charged state obtained by
  **coulomb counting**"
- `C` = `[인쇄]` "the cell capacity defined by upper `V_max` and lower `V_min`
  voltage limits"
- 창 범위 `x ∈ [x₀, x₁₀₀] ⊂ [0,1]`, `y ∈ [y₁₀₀, y₀] ⊂ [0,1]`
- `[인쇄]` "the battery manufacturer specifies the voltage limits to prevent the
  overcharge or over-discharge, and thus **the individual electrodes are not
  fully utilized**"
- `[인쇄]` "Note that the upper voltage limit `V_max` is **often expected in
  practice** through typical CCCV charging protocol rather than the lower voltage
  limit `V_min`." ← §III 의 등식 제약이 `V_max` 만 쓰는 이유

**매개화 장부** `[해석]`: 창 좌표 4개(`x₀, x₁₀₀, y₀, y₁₀₀`) + 전극 용량
2개(`C_p, C_n`) + 셀 용량 `C` 중, 식 (5) 두 개가 `C` 와 창 폭을 묶으므로
자유 파라미터는 **4개**: `θ = [y₁₀₀, C_p, x₁₀₀, C_n]` (식 7). `y₀`·`x₀` 는
식 (5)로 결정된다. 이는 Mohtat 2019 의 `θ = [x₁₀₀, y₁₀₀, C_n, C_p]` 와
**같은 집합, 다른 순서**다.

### §III-A. Parameter Estimation and Degradation Diagnosis (p.3, 인쇄 3378)

**추정 문제** — 비선형 최소자승 + 등식 제약:

```
minimize_θ  Σᵢ ( V_oc(Qᵢ; θ) − V^data_oc,i )²                    (8a)
subject to  V_max = U_p(y₁₀₀) − U_n(x₁₀₀)                        (8b)
```

`[인쇄]` "The cell operates between the predefined voltage limits, and thus
`V_max` is used as an **equality constraint** in (8b), which provides
**additional information** to find the unknown parameters."

**★ 다봉성(multimodality)에 대한 인쇄된 실측 — 우리에게 매우 중요**:
`[인쇄, p.3]` "Due to the nonlinearity of the OCV model, the estimation problem
becomes a **nonconvex optimization problem** with respect to the electrode
parameters, and thus **local minima could exist**. To find an optimum solution,
multiple initial guesses are generated within feasible bounds … For instance,
**out of 100 randomly generated start points, we have observed that 55 start
points converged to the same solution** providing the minimum function value."

`[해석]` **45 %가 다른 곳으로 갔다.** 이것은 [[fitting-degeneracy]] 가 구분하는
두 얼굴 중 **multimodal(최적화 난이도)** 쪽의 야생 실측이며, 저자들은 이것을
"multi-start 로 처리했다" 로 넘긴다 — CRB 는 **국소** 도구이므로 이 45 %는
오차막대에 **전혀 반영되지 않는다**. Marongiu 2016 의 "초기값만 바꿔 오차
6.38 → 14.46 %" 와 같은 계열의 증거다.

**타당성 경계** `[인쇄]`: `x, y ∈ [0,1]`, `C_p, C_n ∈ [C, 2C]`
("electrode capacity is typically larger than cell capacity").

**반쪽전지 OCP 가정과 그 한계** `[인쇄]`: "This approach requires **accurate
knowledge of the half-cell OCPs of both electrodes** … In case the half-cell
potentials are not accurate (e.g., cell-to-cell variance, aging), the model will
cause additional error … Our preliminary work shows that, in an NMC chemistry,
**the PE upper utilization `y₁₀₀` has the highest sensitivity to model
mismatch**. However, the propagation of the model mismatch to the parameter
estimation is **not in the scope of this article**."

`[해석]` 이 한정은 결과 해석에 직접 걸린다 — 뒤에서 제약 CRB 가 `y₁₀₀` 의
막대를 **80배** 줄이는데(2.5 % → 0.03 %), 바로 그 `y₁₀₀` 가 모델 불일치에
가장 민감한 파라미터라고 스스로 적어 놓았다. **막대가 작아진 것과 값이 맞는
것은 다른 이야기**이며 논문은 그 차이를 scope 밖으로 밀어 둔다.

**셀 용량도 추정 가능** `[인쇄]` 식 (9): `V_min = U_p(ŷ₁₀₀ + C/Ĉ_p) −
U_n(x̂₁₀₀ − C/Ĉ_n)` 를 만족하는 `Q = C` 를 찾으면 된다. (단 `V_min` 제약은
추정 문제 (8) 에는 **넣지 않는다**.)

**★ 열화 모드 정의 (이 논문에서 `LLI`·`LAM` 이 등장하는 유일한 절)**:

`[인쇄]` "Identification of electrode SOH and corresponding degradation modes is
done by **tracking the changes of the electrode parameters** `θ = [y₁₀₀, C_p,
x₁₀₀, C_n]` **as a cell ages** `[16]`." (`[16]` = Mohtat 2019)

`[인쇄]` "For aging diagnosis, we refer to commonly defined degradation modes:
**LLI** in a cell and **LAM** for each electrode `[3]`, `[4]`." (Dubarry, Birkl)

```
LLI     = 1 − (y^a₁₀₀ C^a_p + x^a₁₀₀ C^a_n) / (y^f₁₀₀ C^f_p + x^f₁₀₀ C^f_n)   (10)
LAM_PE  = 1 − C^a_p / C^f_p                                                   (11)
LAM_NE  = 1 − C^a_n / C^f_n                                                   (12)
```

`f` = fresh cell 추정치, `a` = aged cell 추정치. 리튬 재고는
`[인쇄]` "the lithium content in one electrode can be calculated by multiplying
the stoichiometric state to the capacity of the electrode (e.g., `Li_PE = y·C_p`)"
로 정의하고, **완충 상태의 화학량론 `y₁₀₀`, `x₁₀₀`** 로 총 재고를 잡는다.

`[해석]` **여기가 판정 1·2의 급소다.** 식 (10)–(12) 는 `θ → (LLI, LAM_PE,
LAM_NE)` 사상을 **명시적으로 인쇄**한다. `LAM_PE`·`LAM_NE` 는 한 성분만 쓰지만
**`LLI` 는 네 성분을 전부 섞으므로 그 분산은 `Σ` 의 비대각 성분을 요구한다.**
논문은 `Σ` 를 손에 쥐고 있고(식 16·24), 상관이 있다는 것도 알고 있는데
(p.8), **식 (10) 로 전파하는 계산을 하지 않는다.** 이 사상은 §III-A 이후
논문에서 **다시 등장하지 않는다.**

### §III-B. Error Bound of Parameter Estimation (p.3–4, 인쇄 3378–3379)

**식별 가능성 분석의 목표를 두 층으로 인쇄한다** — Mohtat 2019 와 같은 이분법:
`[인쇄]` "The goal of the identifiability analysis is **twofold**. One is to
address if the unknown parameters are **uniquely identified** and, if it is
uniquely determined, the second goal is to provide a **measure of the
reliability** of the estimates out of the noisy output measurements."

**CRB 의 성격을 스스로 한정한다** `[인쇄]`: "Note that the CRB is the lower bound
of the variance for **any unbiased estimator**, and thus the error bound in this
article is the **best case scenario**."

식 전개 (p.3–4):

```
y_j = f_j(θ₀) + ε_j ,  ε_j i.i.d., E[ε]=0, var[ε_j]=σ₀²           (13)
θ̂_LS ~ N_m(θ₀, σ₀²(χᵀ(θ₀)χ(θ₀))⁻¹) = N_m(θ₀, Σ₀)                  (14)
χ_ij(θ) = ∂f_i(θ)/∂θ_j              (n×m 감도행렬)                 (15)
Σ₀ = F⁻¹ ≈ Σ(θ̂) = σ̂²(χᵀ(θ̂)χ(θ̂))⁻¹   ← F = Fisher 정보행렬        (16)
σ̂² = 1/(n−m) Σ_j (f_j(θ̂) − y_j)²                                  (17)
θ̂_LS ~ N_m(θ₀, Σ₀) ≈ N_m(θ̂, Σ(θ̂))                                (18)
SE(θ̂_k) = [sqrt(Σ(θ̂))]_kk                                         (19)
θ̂_k − t_{1−α} SE ≤ θ_k ≤ θ̂_k + t_{1−α} SE                         (20)
e_θk(%) = t_{1−α} · SE(θ̂_k)/θ̂_k × 100                             (21)
```

- `[인쇄]` `t_{1−α} = 2` for 95 % (α = 0.05)
- `[인쇄]` 식 (21) 정규화 이유: "the SE term is divided by the least square
  estimate `θ̂_k` for normalization, which enables the evaluation of the
  **relative identifiability among all four electrode parameters**"
- 근거는 `[17]` Seber & Wild *Nonlinear Regression*, `[18]` Banks 2007,
  `[19]` Chen 2013

**제약 CRB (Stoica & Ng `[20]`)** — Mohtat 2019 식 28–34 와 같은 기계:

```
h(θ) = 0 ,   H(θ) = ∂h(θ)/∂θᵀ                                     (22)
H(θ) U = 0            (U: H 의 nullspace 정규직교기저, UᵀU = I)     (23)
Σ'(θ̂) = U (Uᵀ Σ⁻¹(θ̂) U)⁻¹ Uᵀ                                     (24)
H(θ) = [ ∂U_p/∂y · ∂y/∂y₁₀₀ , 0 , −∂U_n/∂x · ∂x/∂x₁₀₀ , 0 ]
     = [ α|_{y₁₀₀} , 0 , −β|_{x₁₀₀} , 0 ]                          (25)
```

`[인쇄]` "The CRB under the parametric constraints can be found by a
**reparameterization** of the original problem to **remove redundancies in the
parameter vector** `[20]`. … If `UᵀΣ⁻¹U` is **nonsingular**, then the parameters
are **identifiable** and the constrained CRB (i.e., **the error covariance
matrix**) can be obtained …"

`[해석]` 두 가지가 여기서 확정된다. (a) 판정의 **이분법 층**은 Mohtat 과 글자
그대로 같다(`UᵀΣ⁻¹U` 특이 여부). (b) 저자들은 `Σ'` 를 명시적으로 **"the error
**covariance** matrix"** 라 부른다 — **행렬 전체를 계산한다는 자각이 있다.**
그리고 식 (19)에서 `[·]_kk` 로 **대각만 뽑아** SE 를 만든다. 즉 이 계보의
"대각선 관습" 은 여기서도 유지되지만, Fig. 7 이 그 관습의 **유일한 예외**다.

**제약의 구조** `[해석]`: `H` 는 1×4 이고 2·4열이 0 이다 → 제약은 `y₁₀₀`,
`x₁₀₀` **두 창 끝점만** 묶고 `C_p`, `C_n` 은 **직접 건드리지 않는다**.
자유도는 4 → 3 으로 준다.

### §IV-A. Data Window (p.4–5, 인쇄 3379–3380)

`[인쇄]` "Two points determine the location and size of the DW; starting-point
`Q_s`; and end-point `Q_e` of the window, i.e., **`DW = [Q_s, Q_e]`**."

`[인쇄]` dV/dQ 곡선의 두 봉우리 `P1`, `P2` 는 "**the phase transitions of the
graphite NE**" 를 나타낸다. `[인쇄]` "In `[21]`, `[22]`, it is shown that data
taken from regions that include **phase transitions** of the electrode material
**improve the identifiability** of the corresponding electrode parameters."
(`[21]` = Lee et al. ACC 2018, `[22]` = Dahn 2012 DVA freeware)

**네 창의 정의** `[인쇄, p.5]`:
- **DW-shallow** — "the battery is used down to **80 % SOC**"
- **DW-medium**, **DW-non-full** — 둘 다 "40 % of the battery capacity usages
  but utilized at **different locations** in the OCV curve, where the non-full
  represents **not fully charged**"
- **DW-deep** — "almost full range of the OCV curve is available"

동기도 인쇄돼 있다: `[인쇄]` "range anxiety tends to make BEV drivers stay away
from low SOC. Typical lower bound for the **PHEV is designed to be around 30 %
SOC**."

수치 범위는 **Table IV 에 인쇄**돼 있다(§3): `[0.0,0.2]`, `[0.3,0.7]`,
`[0.1,0.5]`, `[0.0,0.9]`.

### §IV-B. Analytic Error Bounds (p.5–6, 인쇄 3380–3381)

**계산 조건** `[인쇄]`: 삼각형 plot 은 `Q_s`(y축) × `Q_e`(x축), "Data points are
evenly distributed with **0.5 % DOD intervals**", 관측 잡음은
"**Gaussian white noise with a standard deviation of 10 mV**", 색은 log scale.
`[인쇄]` "the error bound is **proportional to the observation error** as shown
in (16)–(21)."

**핵심 물리 설명 — 반쪽전지 국소 기울기가 식별 가능성을 정한다** `[인쇄]`:
"It is found that **the half-cell potential slopes (α and β in Fig. 1) drive the
identifiability of the electrode parameters**. For NMC/graphite cell, the NMC PE
potential has a relatively **steeper slope** than that of the graphite NE
potential. This steeper slope provide **better identifiability of the PE
parameters (y₁₀₀, C_p) than that of the NE parameters (x₁₀₀, C_n)**."

**LFP 에 대한 (실험 없는) 확장 주장** `[인쇄]`: "For the chemistry of LFP, it has
a flat half-cell potential in the middle, and thus when only the flat voltage
portion is utilized in a certain DW, **the PE parameters are not observable**.
Meanwhile, when it is utilized over the range … that includes the very top charge
level or deep discharge level, also known as **knee or shoulder** of the
potential, the abrupt slope change provides ample information and makes the
parameter estimation feasible `[16]`, `[21]`."

`[해석]` 이 문장이 논문에서 `observab*` 이 쓰인 **유일한** 자리이고, 대상은
**시뮬레이션도 안 한 LFP** 다. NMC/graphite 결과에 대해서는 "not identifiable"
이라는 표현을 쓴다(아래).

**DW-shallow 판정** `[인쇄]`: "When only the upper 20 % range of battery capacity
is used, **all electrode parameters are not identifiable** because of a lack of
information. Large errors (**above 30 % break line**) are obtained, except for
the PE upper utilization range `y₁₀₀` … Even more so, the **NE parameters are
almost not identifiable** due to large errors for the DW-shallow and non-full
cases."

**DW-deep 판정** `[인쇄]`: "for the DW-deep case, the utilized graphite anode
potential **rises significantly** when the battery is almost fully depleted,
making the estimation error of **all electrode parameters less than 5 %**."

**위치 효과 (medium vs non-full, 같은 폭 40 %)** `[인쇄, p.6–7]`: "The non-full
operates around a **higher SOC** region … where the PE potential has a relatively
steeper slope, and hence it provides better identifiability of the **PE**
parameters … Similarly, when the relatively **low SOC** region is utilized as in
the medium case, the relatively steeper slope of the graphite NE provides better
identifiability of the **NE** parameters in the medium."

`[해석]` **같은 폭이어도 어디에 놓느냐가 어느 전극이 보이는지를 바꾼다.** 이
문장이 이 논문의 실질적 기여이며, 우리의 "관측 창을 어디에 두면 어느 모드가
갈리는가" 와 정확히 같은 형태의 질문이다 — 다만 **모드가 아니라 전극
파라미터**에 대해 답한다.

### §IV-C. Impact of Voltage Constraint (p.7, 인쇄 3382)

`[인쇄]` "The voltage constraint **ties the upper utilization ranges of each
electrode (`y₁₀₀` and `x₁₀₀`)**, which provides the **parameter dependency
between the positive and negative electrodes**, which in turn **reduces the
number of unknown parameters** and consequently improves the estimation accuracy
(see Fig. 5; the error bounds of the PE parameters become significantly improved,
especially the utilization range **`y₁₀₀` becomes less than 0.3 % for all the DWs
except the DW-shallow case**)."

**제약이 만든 결합의 닫힌 형태** — Taylor 전개로 얻은 관계식:

```
σ_y · ∂U_p/∂y|_{y₁₀₀}  =  σ_x · ∂U_n/∂x|_{x₁₀₀}        (26)
즉  σ_y · α = σ_x · β
```

`[인쇄]` "Comparing local slope of the half-cell potentials (`α = ∂U_p/∂y|y₁₀₀`
and `β = ∂U_n/∂x|x₁₀₀` in Fig. 1), **β is smaller than α** due to the flat
voltage curve of the graphite NE. Hence, **the error bound `σ_x` is larger than
`σ_y`**. Furthermore, since **the parameters from the same electrode are
correlated**, the improvement in the estimation accuracy of `y₁₀₀` is beneficial
to the estimation accuracy of `C_p` as well."

`[해석]` 식 (26) 은 **비대각을 인쇄한 것에 가장 가까운 것**이다: 두 파라미터의
불확실성 **비(比)** 를 반쪽전지 기울기 비 `β/α` 로 못 박는다. 이것은 "축퇴
방향" 을 한 쌍에 대해 닫힌 형태로 쓴 것이지만, 저자들은 이를 **정확도 개선의
설명**으로만 쓰고 **방향 자체를 결과로 제시하지 않는다.**

**봉우리 효과** `[인쇄]`: "the estimation error bounds of the PE parameters show
a **sharp transition at P1 location, DOD = 0.4**. Similarly, the transitions
occur at both peak points for the NE parameters. Since the slope of the graphite
NE potential starts to change before P2 location, the transitions of the error
bound in the NE parameters occur **around DOD = 0.7**."

### §V-A. Numerical Validation — Monte-Carlo (p.7–8, 인쇄 3382–3383)

**설정** `[인쇄]`: 1000회 반복, 제약 유/무 두 경우, 데이터는 식 (7) + Table I
공칭값 + 가산 zero-mean Gaussian `σ = 10 mV`, **DW-deep 한 경우만**
("utilizes 90 % of the battery capacity from the fully charged state").

**결과** `[인쇄]`: 추정 오차 분포가 근사 Gaussian, "centered at near zero
indicating the **estimates are unbiased**. Since the estimator is unbiased, the
error bound obtained from the CRB can be considered as a proper metric." 해석적
막대와 MC 결과가 Table II·III 에서 일치.

**★ 상관에 대한 유일한 문장** `[인쇄, p.8]`:
"for the unconstrained case, **a strong correlation has been observed among the
parameters from the same electrode**, either from the PE or NE, as shown in the
**top left (`e_y₁₀₀` vs. `e_Cp`)** and **bottom right (`e_x₁₀₀` vs. `e_Cn`)**
plots in Fig. 7. However, **the parameters from the different electrodes do not
show any correlation.**"

`[해석]` 이 문장 + Fig. 7 의 타원이 판정 2의 전부다. **수치는 없다**
(`ρ = …` 형태가 논문에 0회). 그리고 §4 에서 적듯 **그림은 이 문장보다 조금
더 말한다** — `(e_Cp, e_x₁₀₀)` 패널의 타원은 눈에 띄게 기울어 있다.

### §V-B. Experimental Validation (p.8–9, 인쇄 3383–3384)

`[인쇄]`: 5 Ah NMC/graphite 셀. pseudo-OCV 는 **C/20 정전류, 완충에서 방전**.
반쪽전지 전위는 **리튬 금속 상대전극 코인셀에서 개별 측정**. 추정은 식 (8)
**등식 제약 포함**. 기준선(baseline)은 **full-range 데이터의 추정치**이고,
각 DW 의 추정치를 그것과 비교해 "estimation error" 를 만든다.

`[인쇄]` "Fig. 9 shows that **most of the errors are inside the error bounds
except `e_y₁₀₀` for the DW-shallow case**. Note that **the error bounds do not
necessarily predict exact error values** for a given DW, but describe a boundary
for error statistics."

`[해석]` 두 가지 유보가 필요하다. (a) "참값" 이 **full-range 적합값**이다 —
파괴분석도 아니고 독립 측정도 아니다. 즉 이 검증은 "좁은 창의 적합이 넓은
창의 적합과 얼마나 다른가" 를 재며, **넓은 창의 적합이 옳다는 가정** 위에
있다. (b) 셀은 **1개**로 읽히고(단수 표현), 반복·셀간 산포는 없다.

### §VI. Guideline for Selecting Data Window (p.9–10, 인쇄 3384–3385)

`[인쇄]` 4단계 흐름도(Fig. 10): ① 부분 OCV 측정 확보 → ② `θ̂` 와 관측 오차
분산 `σ̂` 추정(식 8, 17) → ③ 목표 오차 막대 `e_θ` 선택(식 21) → ④ 요건을
만족하는 후보 DW 찾기.

`[인쇄]` "if the given voltage error variance **σ̂ = 10 mV** and the target error
bound is **within 10 % at a 95 % confidence level**, the OCV range of
**DOD = [0.35, 0.73]** can be one possible DW satisfying the requirement."

`[해석]` 판정 3의 대응 수치다. Mohtat 2019 의 `[인쇄]` "DOD required for
observability is **reduced to 30 %**"(팽창 관측을 더했을 때)와 좌표계가 같은
DOD 이지만 **의미가 다르다**: Mohtat 은 *폭*(30 % 만큼이면 된다), 이 편은
*폭 + 위치*(`[0.35, 0.73]`, 폭 38 %, 저 SOC 쪽으로 치우침)를 준다.

### §VII. Conclusion (p.10, 인쇄 3385)

`[인쇄]` 핵심 3문장: (a) "the DW plays a vital role in the estimation accuracy
**associated with the local slope of the half-cell potential**", (b) "In general,
**the PE parameters have a better identifiability than the NE parameters**
because of a relatively higher local slope in an NMC/graphite chemistry cell",
(c) "the PE parameters can be even more accurately estimated by introducing a
**voltage constraint**."

**저자들이 스스로 적은 한계** `[인쇄]`: "the analysis here was based on a set of
**simplifying assumptions**, including that the half-cell potentials of both
electrodes are available and **these potentials are invariant**. **Model mismatch
due to cell-to-cell variance or aging can be a source of additional estimation
error**; hence, the propagation of the model mismatch … will be clarified in
future work."

`[해석]` **"these potentials are invariant"** 는 열화 진단에서 특히 무겁다 —
식 (10)–(12) 는 fresh 와 aged 를 **같은 OCP 로** 적합한 결과를 뺀다.

---

## 3. 표 전사 (원문 표는 래스터라 쪽 렌더로 읽었다)

### Table I — Nominal parameters for the selected NMC/graphite cell (p.4)

`[인쇄]`

| 구분 | 파라미터 | 값 |
|---|---|---|
| Full-cell | `C` | 4.95 Ah |
| Full-cell | `V_max` | 4.2 V |
| Full-cell | `V_min` | 3.0 V |
| Positive electrode | `C_p` | 5.78 Ah |
| Positive electrode | `[y₁₀₀, y₀]` | `[0.10, 0.95]` |
| Negative electrode | `C_n` | 6.24 Ah |
| Negative electrode | `[x₁₀₀, x₀]` | `[0.81, 0.02]` |

`[해석]` 정합성 확인: `C_p(y₀−y₁₀₀) = 5.78 × 0.85 = 4.913 Ah`,
`C_n(x₁₀₀−x₀) = 6.24 × 0.79 = 4.930 Ah` — 식 (5) 의 `C = 4.95 Ah` 와 각각
0.7 %·0.4 % 차이(반올림 자릿수 수준). 창 점유율: PE 85 %, NE 79 %.

### Table II — Estimation error bound for **unconstrained** case (p.7)

`[인쇄]` (DW-deep, σ = 10 mV, 95 % 신뢰수준, 단위 %)

| | `θ₁ = y₁₀₀` | `θ₂ = C_p` | `θ₃ = x₁₀₀` | `θ₄ = C_n` |
|---|---|---|---|---|
| MC simulation | 2.5 | 1.3 | 3.0 | 3.9 |
| Analytic derivation | 2.5 | 1.3 | 3.0 | 3.9 |

### Table III — Estimation error bound for **constrained** case (p.7)

`[인쇄]`

| | `θ₁ = y₁₀₀` | `θ₂ = C_p` | `θ₃ = x₁₀₀` | `θ₄ = C_n` |
|---|---|---|---|---|
| MC simulation | **3.2e-2** | 0.9 | 3.0 | 3.9 |
| Analytic derivation | **3.0e-2** | 0.9 | 3.0 | 3.9 |

`[해석]` **제약의 효과가 극도로 비대칭이다**: `y₁₀₀` 2.5 → 0.030 %(약 **83배**),
`C_p` 1.3 → 0.9 %(1.4배), **`x₁₀₀` 3.0 → 3.0, `C_n` 3.9 → 3.9 (변화 없음)**.
`V_max` 등식은 `y₁₀₀` 를 `x₁₀₀` 에 묶는데, `β ≪ α` 이므로(식 26) 그 묶음은
**평평한 쪽(NE)의 불확실성을 뾰족한 쪽(PE)으로 옮겨 담지 못한다** — 오히려
`y₁₀₀` 가 `x₁₀₀` 의 정보를 얻어 좋아지고 NE 는 그대로다. 제약은 **정보를
만들지 않는다**는 것을 보여 주는 깨끗한 수치 사례다.

### Table IV — Experimental estimation errors under different data windows (p.9)

`[인쇄]` (5 Ah NMC/graphite 실측, full-range 적합을 기준선으로, 단위 %)

| DW ID | Data window range (DOD) | `y₁₀₀` | `C_p` | `x₁₀₀` | `C_n` |
|---|---|---|---|---|---|
| Shallow | `[0.0, 0.2]` | 14.9 | 16.8 | 38.3 | 24.1 |
| Medium | `[0.3, 0.7]` | 0.1 | 0.4 | 4.9 | 14.5 |
| Non-full | `[0.1, 0.5]` | 0.2 | 0.9 | 10.0 | 24.1 |
| Deep | `[0.0, 0.9]` | 0.0 | 0.8 | 1.6 | 1.8 |

`[인쇄, p.9]` "the medium case shows relatively smaller estimation errors
especially for the negative electrode parameters (`x₁₀₀` and `C_n`) because the
utilization range of the electrode becomes more informative as the DW gets closer
to a deeper discharged area."

### Fig. 9 안에 조판된 **제약 CRB 막대** (창별)

`[인쇄, Fig. 9 라벨]` — 네 부챗살 축은 위=`e_y₁₀₀`, 오른쪽=`e_Cp`,
아래=`e_x₁₀₀`, 왼쪽=`e_Cn`. 점선 상자에 적힌 값(단위 %):

| DW | `y₁₀₀` | `C_p` | `x₁₀₀` | `C_n` |
|---|---|---|---|---|
| Shallow | 13.3 | 26.6 | **1e3** | **5e3** |
| Medium | 0.1 | 1.4 | 6.4 | 16.3 |
| Non-full | 0.2 | 1.4 | 20.5 | **53.1** |
| Deep | 3e-2 | 0.9 | 3.0 | 3.9 |

`[해석]` Deep 행이 Table III(제약 CRB) 와 **정확히 일치**하므로 이 상자들은
**제약 CRB 막대**다. 그리고 이것이 이 논문에서 가장 센 수치다:
**DW-shallow 에서 `C_n` 의 95 % 막대가 5 000 %** 다 — 음극 용량은 사실상
아무것도 결정되지 않는다. 캡션은 `[인쇄]` "graph is not to scale" 이라고
적어 둔다.

---

## 4. 그림별 기록 — 무엇을 실제로 보았나

크로핑한 그림 **10장 중 8장을 직접 열어 보았다** (Fig. 1, 2, 3, 4, 5, 6, 7, 10).
**안 본 것: Fig. 8** (실험 적합 결과 + 분해된 전극 곡선 — 본문 서술과 캡션으로만
기록), **Fig. 9 는 쪽 렌더(p.9)로 보았다**(크롭본 대신 표와 함께 읽기 위해).
Table I–IV 는 캡션 기반 추출기가 잡지 않으므로 **PDF p.4·p.7·p.9 를 260 dpi 로
렌더해 직접 읽었다.**

| 그림 | 무엇 | 본 것에서 얻은 것 |
|---|---|---|
| **Fig. 1** | 반쪽전지 전위 + 셀 OCV + 창 표시 | `[도표]` (a) `U_p` vs `y`: 4.5 → 2.5 V, `y₁₀₀ ≈ 0.10` 에서 `U_p ≈ 4.32 V`, `y₀ ≈ 0.95` 에서 `≈ 3.46 V`; 기울기 `α_k` 는 `y ≈ 0.30` 에 표시. (b) `V_oc` vs DOD: 4.2 → 3.0 V, 단조 감소, DOD > 0.9 에서 급락. (c) `U_n` vs `x` (**x축이 1 → 0 으로 역방향**): `x₁₀₀ ≈ 0.81` 에서 `U_n ≈ 0.09 V`, `x₀ ≈ 0.02` 에서 `≈ 0.35 V`; `β_k` 는 `x ≈ 0.65` 의 **평탄역**에 표시. **`α` 와 `β` 의 크기 차이가 그림에서 곧바로 보인다** |
| **Fig. 2** | DW 정의 + dV/dQ | `[도표]` 예시 DW 는 음영 `[0.2, 0.6]`. 오른쪽 축 `dV/dQ [V/Ah]` 0–0.6. **P1 ≈ DOD 0.38** (dV/dQ ≈ 0.235), **P2 ≈ DOD 0.82** (≈ 0.24), 그 사이 골 ≈ 0.09, DOD > 0.9 에서 급상승 |
| **Fig. 3** | 네 창의 배치 | `[도표]` 가로축 DOD 0 (Fully charged) → 1 (Fully discharged). shallow `[0, 0.2]`(P1·P2 **둘 다 밖**), medium `[0.3, 0.7]`(**P1 만 안**), non-full `[0.1, 0.5]`(**P1 만 안**), deep `[0, 0.9]`(**둘 다 안**). 경계 숫자 0.2/0.3·0.7/0.1·0.5/0.9 는 그림에 인쇄됨 |
| **Fig. 4** | 창 전수 삼각지도 (제약 **없음**) | `[도표]` 4패널(`y₁₀₀`, `C_p`, `x₁₀₀`, `C_n`), 축 `Q_e`(x) × `Q_s`(y), 컬러바 `log(e_θ)` **−4 … +2**. 빨간 점 4개 위치가 Table IV 범위와 일치. **PE 패널은 좌하단이 초록, NE 패널은 같은 자리가 노랑** — 인쇄된 "PE 가 NE 보다 낫다" 의 그림 근거. `C_n` 패널에는 `Q_e ≈ 0.8` 부근에 **수직 색 경계**가 뚜렷하다(P2 통과 효과) |
| **Fig. 5** | 창별 막대 (제약 유/무) | `[도표]` y축 `Estimation Error [%]`, **30 % 에 축 절단선**. 무제약 읽은 값: `y₁₀₀` shallow ≈ 14.2 · **medium ≈ 25.1** · non-full ≈ 6.6 · deep ≈ 2.6; `C_p` shallow > 30 · medium ≈ 6.5 · non-full ≈ 3.3 · deep ≈ 1.3; `x₁₀₀` shallow > 30 · medium ≈ 10.2 · non-full ≈ 21.9 · deep ≈ 3.0; `C_n` shallow > 30 · medium ≈ 24.4 · non-full > 30 · deep ≈ 3.9. **주목**: `y₁₀₀` 는 medium(25.1)이 shallow(14.2)보다 **나쁘다** — 완충 근처를 안 보면 PE 창 끝점이 떠 버린다. 빗금(제약) 막대는 §3 의 Fig. 9 라벨과 일치 |
| **Fig. 6** | 막대 vs DOD (창을 `[0, DOD]` 로 넓힘) | `[도표]` 4패널, y 0–30 %. 점선 수직선 **P1 ≈ 0.38**, **P2 ≈ 0.83**. `y₁₀₀`: 무제약은 DOD 0.4 이후 **≈ 2–3 % 에서 평평**하지만 제약(빨강 파선)은 **0.4 부근에서 0 으로 떨어진다**. `C_p`: 제약이 DOD < 0.4 에서 **먼저** 좋아진다(0.3 부근 ≈ 12 % vs 무제약 ≈ 19 %). `x₁₀₀`·`C_n`: **두 곡선이 사실상 겹친다** — 제약이 NE 에 아무 도움이 안 된다는 Table II↔III 대조의 곡선판. NE 는 DOD ≈ 0.6–0.7 에서 계단식으로 내려간다 |
| **Fig. 7** | **MC 산점 + 95 % 오차 타원** (DW-deep) | 아래 별도 항목 |
| Fig. 8 | 실험 적합 + 분해된 전극 곡선 | **안 봤다.** 캡션·본문만: (a) 측정 데이터와 모델 적합 + 오차 plot, (b) 분해된 전극 전압 곡선(실선=사용 구간, 파선=전극 전 범위), `[인쇄]` "the graphite NE has more total electrode capacity" |
| **Fig. 9** | 창별 오차 vs 막대 | §3 에 라벨 전사. 상자는 **축 정렬 사각형**(타원 아님) |
| **Fig. 10** | 창 선택 흐름도 | `[인쇄, 그림 내]` Step 1–4 와 예시: `e_θ = 10 %` → **후보 DW: DOD = [0.35, 0.73]** |

### ★ Fig. 7 을 자세히 (판정 2의 전부)

캡션 `[인쇄]`: "Scatter plot of the electrode parameter estimation errors from
Monte–Carlo simulation for the DW-deep case (i.e., `DW = [0, 0.9]`). Estimation
errors show approximate normal distribution. **The 95 % confidence-level error
bound (solid line) agrees with the simulation results.**"

구성 `[도표]`: 4개 파라미터의 **6개 쌍 전부**에 대한 2D 패널 (좌상 `e_y₁₀₀`–`e_Cp`,
우상 `e_y₁₀₀`–`e_x₁₀₀`, 중좌 `e_y₁₀₀`–`e_Cn`, 중우 `e_Cp`–`e_x₁₀₀`,
하좌 `e_Cp`–`e_Cn`, 하우 `e_x₁₀₀`–`e_Cn`). 각 패널에 (i) 청록 원 = 무제약 MC
1000점, (ii) **파란 실선 = 무제약 95 % 오차 타원**, (iii) 자홍 × = 제약 MC,
(iv) **노란 실선 = 제약 95 % 오차 타원**, (v) 주변부에 1D 히스토그램 2개.
축은 상대 오차이며 범위는 `±0.1` (= ±10 %) — Table II 의 2.5/1.3/3.0/3.9 %
와 타원 크기가 맞는다.

**타원의 기울기 (판정)**: 그림에서 각 타원의 주축 방향을 읽었다. 눈으로 본
뒤, 착시를 막기 위해 크롭 PNG 에서 타원 곡선 화소의 공분산 부호도 함께
계산했다(두 방법이 일치). `[도표]`

| 패널 | 전극 관계 | 타원 모양 | 상관 부호 |
|---|---|---|---|
| `e_y₁₀₀` – `e_Cp` | 같은 전극 (PE) | **매우 가늘고 길게 기운 시가형** | **강한 +** |
| `e_x₁₀₀` – `e_Cn` | 같은 전극 (NE) | **매우 가늘고 길게 기운 시가형** | **강한 −** |
| `e_y₁₀₀` – `e_x₁₀₀` | 다른 전극 | 거의 원형, 축 정렬 | ≈ 0 |
| `e_y₁₀₀` – `e_Cn` | 다른 전극 | 거의 원형, 축 정렬 | ≈ 0 |
| **`e_Cp` – `e_x₁₀₀`** | **다른 전극** | **눈에 띄게 기운 타원** (위쪽이 왼쪽으로) | **약~중간 −** |
| `e_Cp` – `e_Cn` | 다른 전극 | 세로로 길고 **약간 기움** | 약한 + |

**★ 본문과 그림의 어긋남**: 본문은 `[인쇄, p.8]` "the parameters from the
**different electrodes do not show any correlation**" 이라고 단언하지만,
**`e_Cp`–`e_x₁₀₀` 패널의 타원은 축 정렬이 아니다** — 두 축의 눈금 범위가
같은데도 주축이 기울어 있다. 본문이 근거로 든 것은 좌상·하우 두 패널뿐이고
(그 둘은 같은 전극 쌍), **중우 패널은 언급되지 않는다.** `[해석]` 즉 "다른
전극 사이 상관 0" 은 **네 개의 다른-전극 쌍 중 둘만 보고 한 진술**이며, 이
그림 자체가 반례를 담고 있다. 수치가 인쇄돼 있지 않으므로 크기는 말할 수
없고, **부호와 비영(非零)까지가 그림에서 읽히는 전부**다.

**제약이 타원에 하는 일** `[도표]`: 좌상 패널에서 노란(제약) 타원은
**`e_y₁₀₀ ≈ 0` 의 거의 수직인 얇은 조각**으로 붕괴한다 — `y₁₀₀` 은 못 박히고
`C_p` 방향으로는 여전히 무제약의 상당 부분을 남긴다(1.3 → 0.9 %). 반대로
하우(NE) 패널에서는 **노란 타원이 파란 타원과 거의 포개진다** — 제약이 NE
축퇴 방향을 **전혀 건드리지 못한다.**

`[해석]` 우리 관점에서 이 그림 한 장의 값어치: **"막대 네 개" 뒤에 가늘고 긴
타원이 있다는 것을 이 계보에서 처음으로 인쇄한 그림**이다. 다만 그 타원은
(a) `θ` 좌표에 있고, (b) 한 창(DW-deep, 가장 좋은 창)에서만 그려졌으며,
(c) **가장 나쁜 창(shallow)에서는 그리지 않았다** — 축퇴가 가장 심할 곳의
타원이 없다. (d) 어떤 수치(ρ, 고유값, 조건수)도 붙지 않는다.

---

## 5. 어휘 전수 (본문 = PDF p.1–10 중 REFERENCES 이전)

**⚠ 조판 함정 두 가지 — 둘 다 이 논문에서 실측됐다**:
1. **합자(ligature)**: IEEE 조판이 `fi`·`fl` 을 U+FB01/U+FB02 합자로 넣는다.
   `identifiability` 는 실제로는 `identiﬁability` 이므로 `identifiab` 로 세면
   **16회 → 0회**가 된다. 정규화하지 않으면 이 논문의 핵심 어휘가 통째로
   사라진다. (Mohtat 흡수 때 실측된 함정은 줄바꿈 하이픈이었고, 이번 것은
   그 사촌이다. 두 정규화를 **모두** 적용해 세었다.)
2. **양쪽 정렬로 공백이 사라진 곳**: `LAMindicatesthat`, `assurfacefilm…`,
   `Consideracontinuouslydifferentiable…` 처럼 단어 경계가 붙어 나온다.
   `\bLAM\b` 같은 단어 경계 정규식은 이런 자리를 놓친다.

| 어휘 | 본문 횟수 | 쪽별 분포 (PDF 인덱스) | 비고 |
|---|---|---|---|
| `identifiab*` | **16** | p.2 ×2, p.3 ×1, p.4 ×2, **p.5 ×6**, p.6 ×2, p.7 ×2, p.10 ×1 | `identifiability` 13 + `identifiable` 3. **합자 정규화 없으면 0** |
| `estimab*` | **0** | — | Mohtat 2019 는 제목에 이 낱말을 쓴다. **같은 그룹인데 이 편은 한 번도 안 쓴다** |
| `degenerac*` | **0** | — | |
| `Fisher` | 3 | p.2 ×2, p.4 ×1 | p.2 는 선행연구 소개, p.4 는 식 (16) `F` 의 이름 |
| `observab*` | **1** | p.5 ×1 | **LFP 가정 문장 하나뿐** ("the PE parameters are not observable") |
| `unobservab*` | **0** | — | |
| `uniqu*` | 2 | p.3 ×2 | 둘 다 §III-B 첫 문단 (`uniquely identified`, `uniquely determined`) |
| `redundan*` | 1 | p.4 ×1 | 식 (22) 앞 "remove **redundancies** in the parameter vector" |
| `ill-condition*` | **0** | — | |
| `condition number` | **0** | — | 조건수 지표를 쓰지 않는다 |
| `sensitivit*` | 4 | p.2 ×1, p.3 ×1, p.4 ×2 | 감도행렬 `χ` 와 선행연구 |
| `Cramer` / `Cramér` | 3 (본문) | p.1 ×2, p.2 ×1 | 본문은 **악센트 없는 `Cramer`**, 참고문헌 `[20]`(Stoica–Ng)만 `Cramér` |
| `covarianc*` | 2 | p.4 ×2 | 식 (16) "the covariance matrix `Σ₀`", 식 (24) "the error covariance matrix" |
| **`correlat*`** | **3** | p.7 ×1, p.8 ×2 | `correlated` 1(식 26 뒤) + `correlation` 2(§V-A). **이 계보에서 0 이 아닌 첫 논문** |
| `global` | **0** | — | 전역 식별 가능성의 한정을 **인쇄하지 않는다** (Mohtat 과 동일, Lin & Khoo 와 대조) |
| **`LLI`** | **6** | **p.1 ×1, p.3 ×5** | 그 외 **0** |
| **`LAM`**(+`LAM_PE`/`LAM_NE`) | **8** | **p.1 ×1, p.3 ×7** | 그 외 **0** |
| `expansion` | 1 | p.7 ×1 | "**Taylor series expansion**" (식 26). **셀 팽창 관측은 이 논문에 없다** — Mohtat 2019 의 축이 여기서는 안 쓰인다 |
| `error bound` | 58 | 전편 | 이 논문의 중심어 |
| `confidence` | 13 | 전편 | |

**★ 판정 5의 정밀 답**: `LLI` 와 `LAM` 은 **두 자리에만** 있다.
- **PDF p.1 (인쇄 3376) §I 서론**: Birkl `[4]` 소개 문장 안에서 각 1회
  (`[인쇄]` "different levels of degradation modes, namely, loss of active
  material (LAM) and loss of lithium inventory (LLI)")
- **PDF p.3 (인쇄 3378) §III-A 후반**: 정의 문단 + 식 (10)–(12), LLI 5회 · LAM 7회

**§IV(결과, p.4–7) · §V(검증, p.7–9) · §VI(지침, p.9–10) · §VII(결론, p.10)
에서 `LLI`·`LAM` 은 각각 0회다.** 그림·표 캡션과 축 라벨에도 없다(전부
`y₁₀₀ / C_p / x₁₀₀ / C_n`).

`[해석]` Mohtat 2019 와 **같은 구조의 침묵**이되, 이 편이 더 날카롭다:
Mohtat 은 모드 사상을 부수적으로 언급했지만, **이 편은 식 (10)–(12) 로 사상을
정식으로 인쇄해 놓고 그 뒤 7쪽 동안 한 번도 쓰지 않는다.** 제목이 곧 "전극
파라미터의 오차 한계" 이므로 이것은 누락이 아니라 **의도적 범위 설정**이다.

---

## 6. 원문에 없어서 확인이 필요한 것 (공백 목록)

1. **`Σ` 나 `Σ'` 의 성분이 하나도 인쇄되지 않는다.** 상관계수 `ρ` 수치 0회,
   고유값·고유벡터 0회, 조건수 0회. Fig. 7 의 타원이 유일한 비대각 증거다.
2. **모드 좌표의 오차막대가 없다.** 식 (10)–(12) 가 있는데도
   `σ(LLI)`·`σ(LAM_PE)`·`σ(LAM_NE)` 는 계산되지 않는다. 특히 `LLI` 는 네
   성분을 섞으므로 **비대각 없이는 계산 자체가 불가능**하다.
3. **fresh↔aged 두 추정의 결합 불확실성이 없다.** 식 (10)–(12) 는 **두 번의
   추정**(`f`, `a`)을 요구하는데, 오차 전파는 두 공분산을 모두 필요로 한다.
   논문의 모든 분석은 **fresh 공칭값 한 점**(Table I)에서만 이루어진다.
4. **열화된 셀에 대한 막대가 없다.** 창은 바꿔 보지만 `θ` 는 항상 Table I 이다.
   열화가 진행되면 `α`·`β`(반쪽전지 국소 기울기)가 놓이는 자리가 바뀌므로
   **막대도 바뀔 텐데 그 축은 스윕되지 않았다.**
5. **잡음 수준이 하나다** (`σ = 10 mV`). 막대가 `σ` 에 비례한다고 인쇄돼
   있으므로 스케일링은 자명하지만, 잡음이 백색·등분산·독립이라는 가정
   자체는 검증되지 않는다 (C/20 pseudo-OCV 의 실제 오차는 **모델 불일치가
   지배적이고 상관돼 있을** 가능성이 크다).
6. **실험 셀 수가 명시되지 않는다** — "a 5 Ah NMC/graphite cell" 단수 표현.
   반복·셀간 산포·재현성 없음.
7. **반쪽전지 OCP 데이터가 공개되지 않는다** (Fig. 1 의 곡선뿐).
8. **DW-deep 외의 창에는 MC 검증이 없다.** 가장 축퇴가 심한 shallow 창에서
   CRB 가 실제 분포를 대변하는지는 **확인되지 않았다** (그리고 그 창에서
   Fig. 9 는 `C_n` 막대를 5 000 % 로 적는다 — 선형화 가정이 성립할 리 없는
   영역이다).
9. **"참값" 의 정체** — 실험 검증의 기준은 full-range **적합값**이지 독립
   측정이 아니다.
10. **다봉성 45 %(100 start 중 55 수렴)의 나머지가 무엇인지** 기술되지 않는다:
    다른 국소해가 어디에 있고 비용이 얼마나 나쁜지, 창에 따라 그 비율이 어떻게
    변하는지 없음.

---

## 7. 비판 (`[해석]` — 논문의 주장이 아니다)

1. **오차막대와 "정확도" 를 섞어 부른다.** `e_θ` 는 잡음에 대한 **하한**이고,
   저자들도 "best case scenario" 라고 적는다. 그런데 결론은 "the PE parameters
   can be **even more accurately estimated** by introducing a voltage
   constraint" 로 넘어간다. **제약은 정보를 만들지 않는다** — 모르는 방향을
   지울 뿐이고, 제약이 참값에서 틀리면 그만큼 **편향**이 된다. 제약이 참값에서
   성립하는지는 검증되지 않는다 (그리고 §III-A 는 `y₁₀₀` 가 모델 불일치에 가장
   민감하다고 스스로 적어 놓았다 — 제약이 정확히 그 파라미터를 못 박는다).
2. **가장 축퇴가 심한 곳에서 도구가 가장 약하다.** CRB 는 국소 선형화이고
   불편 추정을 전제한다. shallow 창에서 막대가 `5e3 %` 라는 것은 "막대가 크다"
   가 아니라 **선형화가 무의미하다**는 뜻이다. 그 자리에 MC 검증이 없다.
3. **다봉성을 봤는데 결과에 반영하지 않는다.** 45 %의 start 가 다른 해로
   갔다는 관측은 CRB 프레임 밖의 사실인데, 논문의 어떤 수치도 그것을 담지
   않는다. "unbiased 이므로 CRB 가 적절하다" 는 주장은 **DW-deep 1000회
   MC 에서만** 확인됐다.
4. **본문이 그림보다 더 강하게 말한다.** "다른 전극 파라미터 사이에는 상관이
   없다" 는 단언은 자기 그림의 `(C_p, x₁₀₀)` 패널과 어긋난다(§4).
5. **모드로 가는 다리를 놓고 건너지 않는다.** 식 (10)–(12) 를 인쇄해 놓고
   그 좌표에서는 아무 불확실성도 계산하지 않는다. 제목이 "electrode
   parameters" 이므로 범위 위반은 아니지만, **"eSOH 로 열화를 진단한다" 는
   서론의 동기와 실제로 답한 질문 사이에 한 칸의 간극**이 남는다.
6. **LFP 주장은 시뮬레이션도 실험도 없다** — 반쪽전지 모양에서 유추한 산문이다.
7. **`e_θ` 의 정규화가 파라미터 간 비교를 왜곡할 수 있다.** 식 (21)은 `θ̂_k`
   로 나눈다. `y₁₀₀ = 0.10` 처럼 작은 값은 같은 절대 오차라도 상대 오차가
   커지고, `x₁₀₀ = 0.81` 은 작아진다. "relative identifiability among all four"
   를 위한 정규화라고 적혀 있지만, **분모가 물리적으로 동종이 아니다**
   (무차원 화학량론 vs Ah). 창 사이 비교에는 문제없지만 **파라미터 사이
   비교에는 이 눈금 선택이 들어 있다.**

---

## 8. 우리 프로젝트와의 접점

### 8.1 좌표 계보 대조

| | Mohtat 2019 | **Lee 2020 (이 편)** | Lin & Khoo 2024 | 우리 |
|---|---|---|---|---|
| 파라미터 | `[x₁₀₀, y₁₀₀, C_n, C_p]` | **`[y₁₀₀, C_p, x₁₀₀, C_n]`** (같은 집합) | `(N/P, Li/P)` 2 자유도 | 22p 삼중항 `(LLI, LAM_PE, LAM_NE)` |
| 등식 제약 | 컷오프 전압 | **`V_max` 1개** (`V_min` 은 안 씀) | 없음 (애초에 안 만듦) | 없음 |
| 잡음 모형 | Gaussian | Gaussian **10 mV** | Gaussian | — |
| 보고 | `sqrt(diag Σ)` | `sqrt(diag Σ')` + **95 % 타원 (Fig. 7)** | `sqrt(diag C_θ)` | **CRB 오차막대 + 상관** |
| 모드 좌표 막대 | 없음 | **없음** (식 10–12 만 인쇄) | 없음 | 있음 |
| 관측 창 | DOD 폭 (30 % 문턱) | **DOD 폭 + 위치** (창 전수 지도) | — | — |

### 8.2 우리 논지에 미치는 영향 (`[해석]`)

- **좁혀야 할 것**: "이 계보는 `Σ` 를 구해 놓고 **대각선만 인쇄한다**" 는
  일반화는 **더 이상 무조건 참이 아니다.** Lee 2020 은 (i) 6개 쌍의 95 % 오차
  타원을 그리고, (ii) 상관을 문장으로 진술하며, (iii) 식 (26) 으로 두
  파라미터의 불확실성 비를 닫힌 형태로 쓴다. 정확한 진술로 바꾸면:
  **"이 계보는 비대각을 그림으로는 한 번 보였으나, 수치로 인쇄한 적이 없고,
  모드 좌표로 전파한 적이 없다."**
- **그대로 남는 것**: **모드 좌표의 오차막대는 여전히 이 계보에 없다.**
  요청서의 판정 1은 Mohtat 과 동일한 답이며, 이 편은 사상(식 10–12)을 명시적으로
  인쇄해 놓고 안 썼다는 점에서 **공백을 더 또렷하게 만든다.**
- **우리가 공급할 수 있는 것**: 식 (10) 의 `LLI` 는 `Σ` 의 비대각을
  **요구한다**. 이 논문의 기계(식 16·24)에 우리 질문(모드 좌표 전파)을 붙이면
  곧바로 계산되는데, 아무도 하지 않았다. 이것이 우리 Phase 1i 가 서 있는 자리다.
- **가져올 수 있는 것 (도구)**:
  1. **창 전수 삼각지도** (`Q_s × Q_e`, log 컬러) — 우리도 관측 창을
     스윕한다면 이 표현이 그대로 쓸 만하다. 다만 우리는 **모드 좌표**에서,
     그리고 **상관 포함**으로 그릴 수 있다.
  2. **제약 유/무 나란히 놓기** (Table II vs III) — 제약이 무엇을 줄이고
     무엇을 안 줄이는지가 한 눈에 보인다. 우리 Phase 1e/1h 의 "제약은 손해"
     결론과 **같은 형식의 대조표**다.
  3. **식 (26)** — 등식 제약이 만드는 불확실성 비 `σ_y α = σ_x β` 는
     제약 gradient 의 nullspace 사영을 손으로 푼 특수해다. 우리 각도 대조와
     같은 대상의 다른 표기.
- **경계 (우리 수치를 여기 옮기지 않는다)**: 우리 쪽 수치의 정본은 artifact 와
  `degradation-degeneracy/docs/RESULTS*.md`, `mode-observability/results/` 다.
  이 digest 는 논문 수치만 담는다.

### 8.3 이 편이 우리 열린 질문에 주는 근거

- **[[22p-physics-or-degeneracy]] 쪽**: `[인쇄, p.3]` "out of 100 randomly
  generated start points, **55** … converged to the same solution" 은
  **다봉성의 야생 실측**이다 (flat-valley 가 아니라 multimodal 쪽).
- **[[pvs-sev-lli-lampe-separability]] 쪽**: 관측을 더하는 대신 **창을 옮기는**
  세 번째 처방이 있다는 것 — `[인쇄]` 같은 폭 40 % 라도 위치를 옮기면
  **어느 전극이 보이는지가 바뀐다** (medium ↔ non-full, Table IV: `x₁₀₀` 4.9 %
  vs 10.0 %, `C_n` 14.5 % vs 24.1 %).
- **[[constrained-crb-identifiability]] 쪽**: 제약이 **NE 막대를 전혀 못
  줄인다**는 깨끗한 수치(Table II↔III: 3.0→3.0, 3.9→3.9)가 "제약은 정보를
  만들지 않는다" 의 교과서적 예시다.

---

## 9. 이 digest 를 다시 쓸 때 필요한 좌표

- 원문 PDF: 로컬 업로드 (11쪽). 텍스트 추출은 PyMuPDF `get_text()`,
  **합자·하이픈 정규화 필수** (§5 경고).
- 표(Table I–IV)는 래스터라 `get_pixmap(dpi=260)` 로 p.4·p.7·p.9 를 렌더해야
  읽힌다.
- 크로핑 그림: `raw/figures/lee2020_estimation-error-bound-limited-data-window/`
  `fig_1.png` … `fig_10.png` + `figures.json`.
- 판정 2를 다시 검증하려면 **`fig_7.png` 를 열어 중우 패널(`e_Cp` 가로 ×
  `e_x₁₀₀` 세로)의 타원 기울기**를 보면 된다.

## 관련 위키 페이지

- [[constrained-crb-identifiability]] — 이 논문 식 (22)–(24) 와 같은 기계
- [[np-lip-ocv-reparametrization]] — 이 편을 `[15]` 로 인용한 Lin & Khoo 2024
- [[birkl-ocv-degradation-diagnostic]] — 이 논문의 `[4]`
- [[dubarry-mechanistic-mode-synthesis]] — 이 논문의 `[3]`, 식 (10)–(12) 어휘 출처
- [[fitting-degeneracy]] — 45 % 비수렴이 걸리는 개념
- [[data-window-identifiability]] — 이 논문이 만든 "창이 식별 가능성을 정한다" 축
