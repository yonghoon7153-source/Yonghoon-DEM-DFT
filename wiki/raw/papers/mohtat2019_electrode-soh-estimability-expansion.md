---
title: "Mohtat et al. 2019 — Towards better estimability of electrode-specific state of health: Decoding the cell expansion (JPS 427, 101–111)"
source_url: local-upload/978ee242-Towards_better_estimability_of_electrodespecific_state_of_health_Decoding_the_cell_expansion.pdf
ingested: 2026-09-04
sha256: 76c2c68ac2e388eca90cc2c444b04ea0e77224aba5429cdf4c361764d2be0d0c
---

# 수집 목적

Peyman Mohtat, Suhak Lee, Jason B. Siegel, Anna G. Stefanopoulou,
**"Towards better estimability of electrode-specific state of health:
Decoding the cell expansion"**, *Journal of Power Sources* **427** (2019)
101–111 의 **절별 해체분석**.

이 논문은 [[np-lip-ocv-reparametrization]] (Lin & Khoo 2024) 가 자기 참고문헌
`[11]` 로 지목하며 `[인쇄, Lin p.2]` "They also derive the gradient … and **use
Fisher information to quantify the parametric identifiability**" 라고 **선행자로
인정**한 문헌이다. 우리 위키는 2026-09-03 에 이 편을 "다음 흡수 1순위" 로
예약해 두었고 (`log.md` 2026-09-03 (10) 항목), 2026-09-04 에는 원전을 못 구해
**PyBaMM 구현본**(`_ElectrodeSOH`) 만 읽고 대리 흡수했다.
이 digest 가 그 대리를 **원전으로 대체**한다.

따라서 무게중심은 "이 논문이 무엇을 발견했나" 가 아니라 다음 세 가지다:

1. **Fisher 정보행렬을 정확히 무엇에 대해 세웠나** (파라미터·관측·스칼라 지표)
2. **그 분석이 내린 판정이 어디까지 인쇄돼 있나** (전압만 vs 전압+팽창)
3. **매개화 장부** — 자유 파라미터 몇 개, 등식 제약 몇 개가 **Mohtat 자신의 표기**인가

**표기 규칙** (이 위키 관례 3구분):
- `[인쇄]` — 논문 본문/표/식/캡션에 글자로 있는 것
- `[도표]` — 그림에서 눈으로 읽은 근사값 (원 데이터가 아니다)
- `[해석]` — 이 문서를 쓰면서 붙인 판단. **논문의 주장이 아니다**

**쪽 인용 규약 (중요)**: 이 PDF 는 Elsevier **조판본(published version)이며
11쪽**이다. 인쇄된 러닝 푸터가 `Journal of Power Sources 427 (2019) 101–111` 과
쪽번호 `102`…`111` 을 달고 있어 **PDF 쪽 인덱스 i ↔ 인쇄 쪽번호 100+i** 로
정확히 대응한다. **이 digest 의 모든 쪽 인용은 PDF 인덱스 1–11 기준**이며,
출판본 쪽으로 바꾸려면 100 을 더하면 된다 (예: 이 digest 의 `p.7` = 출판본 107쪽).
흡수 요청서에 있던 "57쪽 accepted manuscript" 는 **사실이 아니다** — 조판본이다
(요청자도 같은 세션에서 스스로 정정했다).

- 원본 파일: 로컬 업로드 PDF 11쪽 (본문 + 참고문헌. **Supporting Information 없음**)
- 크로핑 그림: `raw/figures/mohtat2019_electrode-soh-estimability-expansion/`
  (fig 8장 + tab 1장, `figures.json` 에 캡션 색인). 실제로 본 그림은 §11 에 명시.

---

## 0. 서지사항 (직접 확인)

`[인쇄]` PDF 1쪽 헤더·푸터 + PDF 임베디드 메타데이터에서 확인한 것:

| 항목 | 값 | 확인처 |
|---|---|---|
| 저자 | Peyman Mohtat (교신), Suhak Lee, Jason B. Siegel, Anna G. Stefanopoulou | p.1 |
| 소속 | Mechanical Engineering Department, The University of Michigan, Ann Arbor, MI 48109-2125, USA | p.1 |
| 학술지 | *Journal of Power Sources* **427** (2019) 101–111 | p.1 푸터 (2–11쪽 러닝 푸터에도 반복) |
| DOI | `10.1016/j.jpowsour.2019.03.104` | **p.1 좌하단에 인쇄됨** — `https://doi.org/10.1016/j.jpowsour.2019.03.104`. PDF 메타데이터 `subject` 필드도 동일 |
| 접수 / 개정 / 게재 | 2019-01-10 / 2019-02-22 / 2019-03-25 (online 2019-04-24) | p.1 |
| 키워드 | Li-ion batteries · Electrode state of health · Mechanical response · **Identifiability analysis** | p.1 |
| 자금 | Automotive Research Center, Cooperative Agreement **W56HZV-14-2-0001**, U.S. Army TARDEC (Warren, MI) | p.10 Acknowledgment |
| 배포 | `[인쇄]` "DISTRIBUTION A. Approved for public release; distribution unlimited." | p.10 |
| 데이터 가용성 선언 | **없음** (2019년 논문이라 Elsevier 의 data availability 절이 아직 없다) | 전수 |

`[해석]` **서지 대조 결과: 요청서에 적힌 서지는 DOI·권·쪽수 모두 원전에서
확인된다.** "미대조" 를 해제한다. 유일하게 틀린 것은 쪽수 총량(57 vs 11)이다.

`[인쇄]` **Highlights 3줄 (p.1)** — 논문 자신이 요약한 기여. 전사:

> • Monitoring the graphite lithiation state is essential for reducing lithium plating.
> • **Expansion improves the identifiability of graphite lithiation state.**
> • **With expansion measurement, DOD required for observability is reduced to 30%.**

`[인쇄]` **Abstract 전문 (p.1)** — 판정문이 여기 다 들어 있으므로 전사한다:

> Li-ion batteries are prone to adverse physical and chemical mechanisms that can
> degrade their performance over time. For this reason, identifying each electrode's
> capacity and utilization window is important for the safe operation of the battery,
> unfortunately the standard capacity estimation method cannot provide this. In this
> work, we introduce electrode-specific State of Health (eSOH) related parameters,
> including individual electrode capacity and utilization window. **We explore the
> identifiability of the parameters using terminal voltage alone and voltage plus cell
> expansion measurements. The analysis here is based on the constrained Cramer-Rao
> Bound (CRB) formulation, which provides the error bounds for the parameters.** The
> model utilizes the voltage/expansion functions of lithium stoichiometry for the
> individual electrodes based on the underlying physics of phase transitions. It is
> shown that slope changes in voltage and expansion that correspond to phase
> transitions in the electrodes enhance the estimation. As a result, **with the
> addition of the expansion, the parameters are estimable without the need to
> discharge the battery to a high Depth of Discharge (>70%)**, which rarely happens in
> automotive applications. This makes eSOH estimation feasible for a wider range of
> real-world driving scenarios.

---

## 1. ★ 원문에 없어서 확인이 필요한 것 (먼저 적는다)

이 절은 논문이 **비워 둔 자리**의 목록이다. 우리 프로젝트가 무엇을 공급할 수
있는지가 여기서 나온다.

| # | 공백 | 근거 (전수/직접 확인) |
|---|---|---|
| **G1** | **★★ 식별 가능성을 `LLI`·`LAM` 에 대해 재지 **않는다**.** LLI/LAM 을 식 (16)·(20) 으로 정의해 놓고, 식별 가능성 분석(§5–§7)에서는 **한 번도 다시 등장시키지 않는다.** CRB 는 오직 `θ = [x₁₀₀, y₁₀₀, C_n, C_p]` 에 대해서만 계산·보고된다 | 어휘 전수 §3: `LLI` 7회는 전부 **p.2·3·5·6**, `LAM` 13회는 전부 **p.3·4·5**. §5(p.7–8) · §6(p.9–10) · §7(p.10) 에 **둘 다 0회** |
| **G2** | **오차공분산 Σ 를 다 구해 놓고 대각선만 쓴다.** 식 (32) 가 완전한 Σ 를 주는데 식 (33) 이 `σ_θ = sqrt(diag[Σ])` 로 즉시 대각화하고, 이후 보고되는 것은 Fig. 8 의 4개 스칼라뿐이다. 파라미터 간 **상관·축퇴 방향**(비대각 성분, Σ 의 최소 고유벡터)은 손에 쥔 채 한 번도 표시되지 않는다 | `[인쇄, p.8, 식 33]` `σ_θ = sqrt(diag[Σ])`. 어휘 전수: 파라미터 상관을 뜻하는 `correlat*` **0회** (유일한 1회는 p.3 "inter-correlations of these degradation **mechanisms**" — 물리 기작 얘기) |
| **G3** | **추정기를 노이즈 아래서 한 번도 돌리지 않는다.** 최적화 문제 (P) 를 정의하고 **참값 θ\* 에서 평가한 CRB** 만 보고한다. Fig. 8 은 추정 결과가 아니라 하한이다. 복원 오차·수렴·국소최소 분포·반복 실현이 전부 없다 | 본문·그림 전수. `[인쇄, p.7, 식 29 뒤]` "S = ∂Y/∂θ is the local sensitivity matrix calculated **at true θ = θ\***" |
| **G4** | **노이즈를 뽑지 않는다.** `σ_V = 10 mV`, `σ_t = 5 μm` 를 **가정**해 E 에 넣을 뿐 난수 실현이 없고, **노이즈 수준 스윕도 없다** (한 조합 고정) | `[인쇄, p.9]` "This result is obtained using σ_V = 10 mV and σ_t = 5 μm measurement error." — 논문 전체에서 이 값이 나오는 유일한 문장 |
| **G5** | **전역(global) 식별 가능성을 언급조차 하지 않는다.** Lin 2024 는 자기 결과가 "only valid locally" 임을 세 번 못 박고 Bayesian inversion 을 미룬다고 인쇄하는데, **Mohtat 은 그 한정을 인쇄하지 않는다** | 어휘 전수: `global` **0회**, `Bayes*` **0회**, `local` **2회뿐**이고 둘 다 한정이 아니라 정의문 ("f is **locally** differentiable" p.7, "the **local** sensitivity matrix" p.7) |
| **G6** | **열화 상태를 스윕하지 않는다.** CRB 는 **fresh 셀 1점**(Table 3 의 적합값)에서만 평가된다. 스윕하는 축은 오직 **데이터 창(DOD)** 하나다. Fig. 2·3 이 보여 준 aged 상태(LAM_deNE 28 %)에서 CRB 를 다시 계산하지 않는다 | `[인쇄, p.9]` "a virtual model is constructed to study the identifiability of the parameters under a variety of **data availability scenarios**, such as a limited number of measurements, and identifiability under voltage and voltage plus expansion measurements" — 열거된 시나리오에 열화 상태가 없다 |
| **G7** | **`n_c` (직렬 적층 수) 의 값이 어디에도 인쇄되지 않는다.** 그런데 팽창 감도의 스케일 `w_n = n_c t_n0 ξ_n`, `w_p = n_c t_p0 ξ_p` (식 39) 가 그 값에 **선형 비례**한다. `n_c` 없이는 `σ_t = 5 μm` 가 신호 대비 얼마나 큰 노이즈인지 알 수 없고 **Fig. 8 을 재현할 수 없다** | Table 3 전수 (`t_i0`, `ξ_i`, `U_i`, `ΔV_i`, 적합값 4개만 있고 `n_c` 없음). `[인쇄, p.4]` "`n_c` is the number of parallel cells stacked on top of each other in the battery" — 정의만 있고 값 없음 |
| **G8** | **5 % 라는 판정선의 근거가 없다.** 한 문장으로 선언된다 | `[인쇄, p.10]` "Finally, **a threshold of 5% is selected** as an acceptable amount of estimation error for the parameters." (왜 5 % 인지 없음) |
| **G9** | **aged 셀을 측정하지 않았다.** 실측은 **fresh 셀 1개**(A123 20.5 Ah graphite/LFP)의 C/20 곡선 하나뿐이고, 열화 시나리오(Fig. 2·3)는 Dubarry 2012 방법으로 만든 **시뮬레이션**이다 | `[인쇄, p.3]` "using a **simulated** aging scenario for a graphite/LFP cell … the methodology presented in Ref. [3] is followed". `[인쇄, p.10]` 향후 과제: "the estimation of eSOH parameters with data collected from **fresh and aged cells**" |
| **G10** | **화학이 하나(graphite/LFP)뿐이고, 그 화학이 결론을 만든다.** 팽창의 이득이 큰 이유가 "LFP 전압이 평탄해서" 인데, 그 조건을 벗어난 화학(NMC 등)에서 같은 결론이 나오는지 검증이 없다 | `[인쇄, p.10]` "for material **like LFP with flat voltage response** at middle SOC regions the estimation of the individual electrode parameters is feasible by including the expansion measurements" |
| **G11** | **복합전극(Si/Gr)이 범위 밖이다.** 음극은 순수 graphite 이고 상전이 격자 데이터(Table 2)도 graphite 뿐 | 전수. `silicon` 은 p.6 에서 "300 % 팽창의 예" 로 한 번 언급될 뿐 모델에 없음 |
| **G12** | **동역학·온도·이력이 없다.** 저자들이 명시적으로 뺐다고 인쇄한다 | `[인쇄, p.2]` "the model is developed using several simplifying assumptions; namely, that the effects of **temperature and hysteresis** on voltage and expansion are **omitted**" |
| **G13** | **CRB 의 전제(불편성)를 검토하지 않는다.** Lin 2024 는 "not necessarily unbiased … semi-heuristic" 이라고 자기 한계를 인쇄하는데, Mohtat 은 "unbiased estimate of a nonrandom parameter vector" 라는 교과서 정의만 쓰고 자기 문제에서 그것이 성립하는지 묻지 않는다 | `[인쇄, p.7]` §5.2 첫 문장 |
| **G14** | **Fig. 8 의 판정선 5 % 를 네 파라미터에 **엄격히** 적용하면 인쇄된 두 숫자(30 % / >70 %)가 `C_p` 에서 성립하지 않는다** — 아래 §9.3. 논문 자신이 `C_p` 의 98 % 를 §6.1 에 인쇄해 놓고 Abstract·Highlights 에서는 반영하지 않는다 | `[인쇄, p.9]` + `[도표]` Fig. 8(d) |

---

## 2. 세 개 최우선 질문에 대한 직답 (근거는 아래 절)

### Q1. Fisher 정보행렬을 정확히 무엇에 대해 세웠나

**파라미터 벡터** `[인쇄, p.7, §5.1]`:

```
θ = [ x₁₀₀ , y₁₀₀ , C_n , C_p ]
```

- `x₁₀₀` = 만충 상태에서 **음극(graphite)** 의 화학량론 (lithiation state)
- `y₁₀₀` = 만충 상태에서 **양극(LFP)** 의 화학량론
- `C_n`, `C_p` = 각 전극의 **개별 용량** (Ah) — `[인쇄, p.4]` "These capacities
  correspond to the amount of **active material** in each electrode."

**관측 벡터** `[인쇄, p.7, 문제 (P)]`:

```
Y(θ, Q_i) = [ OCV(θ, Q_i) ,  Δt_c(θ, Q_i) ]ᵀ ,   Ŷ_i = [ OCV_i , Δt_ci ]ᵀ
```

즉 **전압만이 아니다 — 셀 팽창(Δt_c, 두께 변화, μm)이 두 번째 관측 채널**이다.
논문의 두 시나리오는 이 벡터의 **두 번째 성분을 켜고 끄는 것**이다
(`Voltage` vs `Voltage+expansion`).

**FIM** `[인쇄, p.7, 식 (29)]`:

```
𝓘_f = Sᵀ E⁻¹ S                                   (29)
```
`[인쇄, 식 29 뒤]` "where **S = ∂Y/∂θ is the local sensitivity matrix calculated
at true θ = θ\***. If FIM is nonsingular, the 𝓘_f⁻¹ is the *unconstrained* CRB
for the error covariance matrix of θ."

노이즈 공분산 `[인쇄, 식 (35)]`: `E = blkdiag(E_V, E_t)`, `E_V = diag[σ_V²]`,
`E_t = diag[σ_t²]` — **전압 노이즈와 팽창 노이즈는 독립·등분산 가정**.
감도행렬 `[인쇄, 식 (36)]`: `S(θ*) = [S_V(θ*) ; S_t(θ*)]`,
`S_V = ∂OCV/∂θ|_θ*`, `S_t = ∂Δt_c/∂θ|_θ*`.

**제약 처리 (이 논문의 방법론적 핵심)** `[인쇄, p.7–8, 식 (30)–(32)]` — Stoica &
Ng 1998 (참고문헌 [27]) 의 **constrained CRB**:

```
f(θ*) = 0                                        (30)
(∂f(θ)/∂θ)|_θ*  𝒪 = 0                            (31)      ← 𝒪 는 제약 gradient 의
                                                              nullspace 정규직교기저
                                                              (𝒪ᵀ𝒪 = I)
Σ ≥ 𝒪 (𝒪ᵀ 𝓘_f 𝒪)⁻¹ 𝒪ᵀ                            (32)
```

`[인쇄, 식 31 뒤]` **"If 𝒪ᵀ 𝓘_f 𝒪 is nonsingular, then the constrained problem is
identifiable, moreover, the error covariance, Σ matrix i.e. constrained CRB is (32)."**

**스칼라 지표** `[인쇄, p.8, 식 (33)·(34)]`:

```
σ_θ = sqrt( diag[Σ] )                            (33)
Error(%) = (σ_θi / θi) × 100                     (34)
```

→ **D-최적성도, trace 도, 조건수도, 고유값도 아니다.** 지표는
**파라미터별 표준오차의 참값 대비 백분율**, 즉 **제약 CRB 의 대각선 4개**다.
어휘 전수로 뒷받침된다: `condition number` 0회, `singular value` 0회,
`eigen*` 0회, `trace` 0회, `D-optimal` 0회, `Hessian` 0회.

**★ 다만 이 논문에는 스칼라 지표가 아닌 판정 기준이 하나 더 있고, 그것이
우리 축에 더 가깝다** — **rank deficiency** (§8.2):

`[인쇄, p.8, 식 (38) 뒤]` "For the case of voltage only measurements, **if all the
measurements are from a single slope the first and second columns in the
sensitivity matrix in Eq. (38) become linearly dependent** due to the same values
of entries for all measurements. Thus, **the sensitivity matrix is rank deficient
and the problem is unidentifiable.** Hence, at minimum the measurements have to
be taken from regions with different slopes."

`[해석]` 이것은 CRB 의 대각선이 아니라 **감도행렬의 열 사이 선형종속**을 말한
문장이다 — 즉 이 논문에는 **축퇴의 방향을 지목한 문장이 정확히 한 개 있다**
(`x₁₀₀` 열 ↔ `y₁₀₀` 열). 논문은 이것을 일반화하지도, 수치로 재지도 않는다.

### Q2. 그 분석의 결론이 무엇인가 — 인쇄된 것과 우리 해석의 경계

**인쇄된 판정 (원문 그대로, 해석 없음)**:

| # | 인쇄문 | 위치 |
|---|---|---|
| P1 | "Expansion improves the **identifiability of graphite lithiation state**." | p.1 Highlights |
| P2 | "With expansion measurement, **DOD required for observability is reduced to 30%**." | p.1 Highlights |
| P3 | "with the addition of the expansion, the parameters are **estimable without the need to discharge the battery to a high Depth of Discharge (>70%)**" | p.1 Abstract |
| P4 | "if all the measurements are from a single slope … the sensitivity matrix is **rank deficient and the problem is unidentifiable**" | p.8 §5.3 |
| P5 | "the identifiability of the parameters depends on **rate changes** of electrode voltage/expansion, which is related to phase transition in the material. Therefore, it is deduced that **having data at phase transitions provides better identifiability** of the individual electrode parameters." | p.9 §6.1 |
| P6 | "the results indicate that the parameters are **unobservable at low DOD regions**." | p.10 §6.1 |
| P7 | "**a threshold of 5% is selected** as an acceptable amount of estimation error … Using this criterion, it is evident that **by having the expansion measurements the estimation is feasible at about 30% DOD**." | p.10 §6.3 |
| P8 | "It was shown for the **voltage only case that the measurements should be taken at a wider range of SOC spanning at least two phase transitions, in order to make all the parameters identifiable**. However, the addition of expansion measurements **made the parameters identifiable for shallower depth of discharges**." | p.10 §7 결론 |
| P9 | "it is concluded that in order to have better confidence levels in the presence of noise and limited data, **having the expansion measurement is necessary for estimating eSOH parameters**." | p.10 §6.3 |

**★ 정확히 말하면 판정은 "전압만으로는 못 가른다" 가 아니다.**
`[해석]` 인쇄문 P8 이 결정적이다 — 전압만으로도 **충분히 넓은 SOC 창(상전이
2개 이상)을 쓰면 네 파라미터가 identifiable 하다**. 못 하는 것은 **얕은 DOD** 다.
즉 이 논문의 판정 변수는 **관측 종류가 아니라 데이터 창의 폭**이고, 팽창은
**같은 정밀도를 더 얕은 창에서 사게 해 주는 수단**이다.
"전압만으로는 원리적으로 불가능" 이라는 문장은 **원문 어디에도 없다.**

**★ 그리고 그 판정의 대상은 `[x₁₀₀, y₁₀₀, C_n, C_p]` 이지 `LLI/LAM` 이 아니다** (G1).
Highlights P1 이 그 대상을 스스로 좁혀 말한다 — "identifiability of **graphite
lithiation state**", 즉 `x₁₀₀` 하나다.

### Q3. 매개화 장부 — Mohtat 자신의 표기는 무엇인가

**판정: "자유 파라미터 4개 + 등식 제약 1개" 가 Mohtat 자신의 표기다.**
Lin 이 전한 쪽이 맞다.

`[인쇄, p.7, §5.1]` 문제 (P) 전문 (렌더링해서 눈으로 대조함):

> The parameters, **θ = [x₁₀₀, y₁₀₀, C_n, C_p]**, related to electrode specific SOH
> can be estimated by solving the following problem using measurements at coulomb
> counting Q_i, terminal voltage at rest OCV_i, and cell expansion at rest Δt_ci
>
> **min_θ Σ_{i=1}^{N} ‖ Y(θ, Q_i) − Ŷ_i ‖²    (P)**
>
> **subject to,  U_p(y₁₀₀) − U_n(x₁₀₀) = V_max ,**

**등식은 (P) 안에 정확히 하나다** — 최대 전압 컷오프 하나뿐. 최소 전압 컷오프는
제약으로 들어가지 않고, **추정이 끝난 뒤 셀 용량 C 를 푸는 식**으로 따로 쓰인다:

`[인쇄, p.7]` "With a partial discharge scenario, the capacity of the cell is also
unknown. Therefore, to focus the estimation on the eSOH parameters, **the capacity
is not included in the above formulation. Hence, only the maximum voltage limit is
used in the estimation problem.** Nevertheless, after finding θ, the capacity of
the cell, C, can be estimated by solving the minimum voltage constraint equation
given by"

```
V_min = U_p( y₁₀₀ + C/C_p ) − U_n( x₁₀₀ − C/C_n )        (27)
```

**두 장부의 대사 (모두 Ah 축 자유도 3 으로 귀착)**:

| 표기 | 미지수 | 등식 | 자유도 | 이 위키의 기존 행 |
|---|---:|---:|---:|---|
| **Mohtat 자신 (식 (P))** | `x₁₀₀, y₁₀₀, C_n, C_p` = **4** | **1** (`V_max`) | **3** | `comparisons/…-lineage.md` 의 "Lin 이 전하는 표기" 행 |
| Mohtat 자신 + 식 (27) | 위 4개 **+ C** = 5 | 2 (`V_max`, `V_min`) | 3 | — (같은 문제를 한 덩어리로 본 것) |
| PyBaMM `_ElectrodeSOH` 구현본 | `x₁₀₀, y₁₀₀, x₀, y₀` (+`Q`) = **5** | **2** | **3** | `comparisons/…-lineage.md` 의 "구현본" 행 |

`[해석]` **세 줄은 같은 문제의 세 장부다.** 차이는 (a) Mohtat 은 `C` 를 θ 밖으로
빼내 사후에 풀고, PyBaMM 은 안에 넣어 동시에 푼다, (b) Mohtat 은 `(C_n, C_p)`
= 전극 **용량**을 좌표로 쓰고 PyBaMM 은 `(x₀, y₀)` = 전극 **SOC 하한**을 쓴다
(식 (6)–(7) 로 상호 변환된다: `x₀ = x₁₀₀ − C/C_n`, `y₀ = y₁₀₀ + C/C_p`).

`[해석]` **다만 위키의 "Lin 이 전하는 표기" 행에는 부정확한 곳이 한 군데
있다** — 그 행의 자유 파라미터를 "전극 SOC 한계 **4개**" 로 적어 두었는데,
Mohtat 의 4개는 SOC 한계 **2개**(`x₁₀₀, y₁₀₀`) + 전극 **용량 2개**(`C_n, C_p`)
다. 개수와 자유도는 맞고 **구성이 다르다**. (이 위키의 비교표는 이 digest 의
범위 밖이라 여기 기록만 남긴다.)

---

## 3. 어휘 전수 ★ (이 계보 열네 편째)

**셈 방법**: PyMuPDF 로 11쪽 전문 추출 → 합자 정규화(`ﬁ`→`fi`, `ﬂ`→`fl`) →
**줄바꿈 하이픈 결합**(`un-\nobservable` → `unobservable`) → 소문자화 →
부분문자열 셈. 그림 안의 글자는 래스터라 **세어지지 않는다** (Fig. 8(a) 의
`Unobservable` 라벨이 그 예 — 아래 주 참조).

| 패턴 | 본문(p.1–10) | 참고문헌(p.11) | 합 | 비고 |
|---|---:|---:|---:|---|
| `identifiab*` | **22** | 1 | **23** | 제목·키워드·절 제목까지 포함. 참고문헌 1회는 [5] Lee 2018 ACC 제목 |
| `unidentifiab*` | **1** | 0 | 1 | p.8 — **"the problem is unidentifiable"** (rank deficiency) |
| `observab*` | 9 | 2 | **11** | 절 제목 2개(§6.2·§6.3) 포함 |
| `unobservab*` | **1** | 0 | 1 | p.10 "the parameters are **unobservable** at low DOD regions" |
| `estimab*` | **2** | 0 | 2 | **둘 다 p.1** — 제목("estimability") + Abstract("estimable"). 본문에는 **0회** |
| `sensitivit*` | 13 | 0 | 13 | p.8 에 7회 집중 (§5.3) |
| `Fisher` / `information matrix` | 2 | 1 | **3** | 아래 §3.1 에 위치 전부 |
| `Cramer` (무악센트) | 4 | 0 | 4 | p.1·2·7·10 |
| `Cramér` (악센트) | 0 | **1** | 1 | 참고문헌 [27] Stoica & Ng 제목 안 |
| `CRB` | 7 | 0 | 7 | p.1(1) · p.7(5) · p.10(1) |
| `covarianc*` | 4 | 0 | 4 | **전부 p.7** (§5.2) |
| `rank` / `rank deficient` | **1** | 0 | 1 | p.8, 단 1회 |
| `nullspace` | **1** | 0 | 1 | p.7, 식 (31) 설명 |
| `nonsingular` | 2 | 0 | 2 | p.7 — 식별 가능성 판정 기준 |
| `linearly dependent` | **1** | 0 | 1 | p.8 |
| `noise` | 6 | 0 | 6 | |
| `better-conditioned` | **1** | 0 | 1 | p.10 — 조건수 어휘가 나오는 **유일한 곳** |
| `couple`(파라미터 결합) | **1** | 0 | 1 | p.10 §6.2 (p.2 의 1회는 `thermocouple` — 오탐, 제외함) |
| `correlat*` | 1 | 0 | 1 | p.3 "inter-**correlations** of these degradation **mechanisms**" — **물리 기작**이지 파라미터 상관이 아니다 |
| `expansion` | **87** | 0 | 87 | 이 논문의 주인공 |
| `LLI` | 7 | 0 | 7 | **전부 p.2·3·5·6** — §5 이후 0회 |
| `LAM` | 13 | 0 | 13 | **전부 p.3·4·5** — §5 이후 0회 |
| `half-cell` | 4 | 0 | 4 | p.3(3) · p.4(1) |
| `local` | **2** | 0 | 2 | 둘 다 정의문. **한정 문장이 아니다** |
| **`global`** | **0** | 0 | 0 | ★ |
| **`degenerac*`** | **0** | 0 | 0 | |
| **`uniqu*` / `non-unique`** | **0** | 0 | 0 | ★ |
| **`redundan*`** | **0** | 0 | 0 | |
| **`collinear*`** | **0** | 0 | 0 | |
| **`confound*`** | **0** | 0 | 0 | |
| **`ill-condition*` / `condition number`** | **0** | 0 | 0 | (`better-conditioned` 1회는 위 별항) |
| **`Hessian`** | **0** | 0 | 0 | |
| **`singular value` / `eigen*`** | **0** | 0 | 0 | |
| **`profile likelihood`** | **0** | 0 | 0 | |
| **`Bayes*`** | **0** | 0 | 0 | |
| **`uncertaint*`** | **0** | 0 | 0 | |
| **`ambigu*`** | **0** | 0 | 0 | |
| **`error bar` / `confidence interval`** | **0** | 0 | 0 | |
| **`cross-valid*`** | **0** | 0 | 0 | |
| **`trade-off`** | **0** | 0 | 0 | |

### 3.0 추출 방식 차이 검증 (독립 셈과의 대조)

같은 PDF 를 **pypdf** 로 독립적으로 센 결과와 대조했다. **하이픈 결합 전** 값은
아홉 항목에서 정확히 일치했다 (`identifiab* 22 · observab* 10 · sensitivit* 13 ·
Cramer 4 · Cramér 1 · covarianc* 4 · Fisher 3 · estimab* 2 · degenerac*·uniqu*·
redundan*·ill-condition*·condition number·collinear = 0`).

**어긋난 곳은 하이픈 결합 여부에서만 나오며, 넷이다**:

| 패턴 | 결합 전 | 결합 후 | 잃어버린 실체 |
|---|---:|---:|---|
| `identifiab*` | 22 | **23** | p.7 `identifi-\nable` (식 (31) 뒤) |
| `observab*` | 10 | **11** | p.3 Fig. 3 캡션 `ob-\nservable` |
| **`unobservab*`** | **0** | **1** | p.10 `un-\nobservable` ← **가장 중요한 손실** |
| `expansion` | 81 | **87** | `ex-\npansion` 6회 |

`[해석]` **"unobservab\* 0회" 는 추출 손실이었다.** 조판 줄바꿈 하이픈 때문에
원문의 유일한 "unobservable" 이 문자열 검사에서 사라진다. 이 위키의 어휘 전수는
앞으로 **하이픈 결합을 전처리에 넣어야 한다** — 앞선 열세 편의 0회 판정 중
줄바꿈 하이픈에 걸린 것이 있는지는 미확인이다.

`[해석]` **그림 속 글자는 세어지지 않는다.** Fig. 8(a) 에는 화살표와 함께
`Unobservable` 이라는 **라벨이 그려져** 있는데(직접 봄), 이 논문의 그림은
래스터 이미지라 텍스트 층에 없다. 즉 실제로 저자가 "unobservable" 이라고 쓴
자리는 최소 **2곳**(본문 1 + 그림 1)이다.

### 3.1 `Fisher` 3회의 위치 (요청 항목)

| # | 쪽 | 절 | 문장 |
|---|---|---|---|
| 1 | p.2 | §1 Introduction 끝 | `[인쇄]` "The methodology for identifiability analysis is based on the **Fisher information matrix** that yields the Cramer-Rao bound for the estimation of eSOH parameters." |
| 2 | p.7 | §5.2 첫 문장 | `[인쇄]` "The identifiability analysis can be explored by means of **Fisher Information Matrix (FIM)**, and the Cramer-Rao bound (CRB) matrix, which gives the lower bound on the error covariance matrix of an unbiased estimate of a nonrandom parameter vector." |
| 3 | p.11 | 참고문헌 [28] | C. Jauffret, "Observability and **Fisher information matrix** in nonlinear regression", *IEEE Trans. Aerosp. Electron. Syst.* 43(2) (2007) 756–759 |

**즉 `Fisher` 라는 낱말이 붙은 식은 (29) 단 하나다.** 나머지 논의는 전부 CRB
(식 32–34) 로 진행된다.

### 3.2 `Cramer/Cramér` 5회의 위치 (요청 항목)

| # | 쪽 | 위치 | 문장 |
|---|---|---|---|
| 1 | p.1 | Abstract | "The analysis here is based on the **constrained Cramer-Rao Bound (CRB)** formulation, which provides the error bounds for the parameters." |
| 2 | p.2 | §1 | "…that yields the **Cramer-Rao bound** for the estimation of eSOH parameters." |
| 3 | p.7 | §5.2 | "…and the **Cramer-Rao bound (CRB) matrix**, which gives the lower bound on the error covariance matrix…" |
| 4 | p.10 | §7 결론 | "…the standard error of the parameters was calculated by the **constrained Cramer-Rao Bound**." |
| 5 | p.11 | 참고문헌 [27] | P. Stoica, B.C. Ng, "On the **cramér-rao** bound under parametric constraints", *IEEE Signal Process. Lett.* 5(7) (1998) 177–179 |

`[해석]` **어휘 표의 요지**: 이 논문은 `identifiab*` 23회 · `observab*` 11회 ·
`CRB` 7회로 **추정 정밀도의 어휘를 완비**했다. 그러나 `uniqu*` 0 · `degenerac*` 0
· `redundan*` 0 · `collinear*` 0 · `confound*` 0 이다 — **"서로 다른 파라미터
조합이 같은 관측을 낸다" 는 비유일성의 어휘는 여전히 0회**다. Lin 2024 와
정확히 같은 패턴이며, 차이는 Mohtat 이 그 비유일성을 **한 문장으로 지목한다**는
것뿐이다: "linearly dependent … rank deficient … unidentifiable" (p.8, 각 1회).

---

## 4. §1 Introduction (p.1–2) — 이 논문이 세운 질문

`[인쇄, p.2]` 이 논문이 인쇄한 **문제 제기 두 문장** (이 위키의 축과 정확히
겹치므로 전사):

> There are a number of studies that identify aging mechanisms using an underlying
> model with voltage and current measurements [4–7]. However, **it has been shown
> that these aging mechanisms are only weakly detectable using terminal
> voltage-based estimation [8,9].**

`[인쇄, p.2]` 그리고 팽창 관측의 유용성을 **의심하는 형태**로 묻는다:

> Although the idea of using stress/strain measurements to identify aging
> mechanisms, such as lithium plating [12], has been proposed, **questions remain on
> the usefulness of this measurement.** For example, given the fundamental
> relationship between voltage and strain [13], **does this stress/strain give
> additional information about the battery's state of health that is not available
> in voltage?**. Furthermore, **is using stress/strain beneficial, given limits on
> data availability and sensor noise, for observability of the aging mechanisms?**

`[해석]` **이 두 물음이 이 논문의 실제 질문이며, 우리 축과 같은 종류다** —
"관측을 하나 더 넣으면 정보가 실제로 늘어나는가, 아니면 이미 들어 있던 것인가".
Mohtat 의 답은 CRB 로 계산한 "늘어난다" 이고, 그 반대 방향의 사례가 우리 위키에
이미 있다 (Marongiu 2016 — 상관된 관측을 더하면 **나빠진다**,
[[pvs-sev-lli-lampe-separability]] Evidence For 2026-09-03 (12)).

`[인쇄, p.2]` 참고문헌 [8,9] 는 각각 Zhou 2017 (*Contr. Eng. Pract.* 66, 51–63,
"Battery state of health monitoring by estimation of the number of cyclable
li-ions") 과 Hatzell 2012 (ACC survey) 다. **"weakly detectable" 의 근거가 이
둘**이고, 우리 위키에는 아직 없다.

---

## 5. §2 실험 (p.2) — 실측은 fresh 셀 하나뿐

| 항목 | 값 `[인쇄]` |
|---|---|
| 셀 | A123 파우치, **graphite/LFP**, 공칭 **20.5 Ah**, 2.5–3.6 V (Table 3) |
| 지그 | 상·하판 고정, **중간판 자유**, 압축 스프링으로 약 **1 psi** 예압. "the spring constants were much lower than the modulus of the cell [14]" → 자유 팽창에 가깝게 |
| 팽창 센서 | 변위 센서 (Keyence, Japan), 상판 장착 |
| 사이클러 | Biologic (France) · 열전대 K형 (Omega) |
| 온도 | 항온챔버 **25 °C** |
| 프로토콜 | C/3 로 2.5–3.6 V 10 사이클 (반복성 확인) → **CC C/20 충전** to 3.6 V → CV until < C/40 → **3 h 휴지** → 같은 전류로 2.5 V 까지 방전. 3회 반복, **마지막 사이클만 보고** |

`[해석]` **셀 1개, 상태 1개(fresh), 온도 1개.** aged 셀 측정은 없다 (G9).
C/20 이므로 "OCV" 는 준정적 근사이고, 이력(hysteresis)은 명시적으로 무시된다.

---

## 6. §3 모델 개발 (p.3–5) — eSOH 정의와 LLI/LAM 식

### 6.1 §3.2 열화 기작 → 두 모드 (p.3)

`[인쇄]` "it is possible to separate the effects of the mechanisms into two general
modes of Loss of Lithium Inventory (LLI) and Loss of Active Material (LAM) at the
positive and negative electrodes. **Dubarry et al. [3]**, further categorized LAM
under the consideration of the lithiated or delithiated state of LAM i.e.
**LAM_liPE, LAM_dePE, LAM_liNE, and LAM_deNE**. Furthermore, LLI is also divided
into two subcategories during; (1) charging in the negative electrode, and (2)
discharging in the positive electrode."

`[해석]` **이 논문의 모드 어휘는 통째로 [[dubarry-mechanistic-mode-synthesis]]
(Dubarry 2012) 에서 온다.** 우리 위키가 이미 흡수한 계보 안이다.

### 6.2 §3.2.1 OCV 모델 (p.4) — 매개화의 뼈대

`[인쇄]` 식 (1)–(9). 요지:

```
OCV(z) = U_p(y) − U_n(x)                                      (1)
U_p(y₀) − U_n(x₀)     = V_min                                 (2)
U_p(y₁₀₀) − U_n(x₁₀₀) = V_max                                 (3)
z = Q/C = (y − y₁₀₀)/(y₀ − y₁₀₀) = (x₁₀₀ − x)/(x₁₀₀ − x₀)      (4)
C = C_p (y₀ − y₁₀₀) = C_n (x₁₀₀ − x₀)                          (5)
z = Q/C = (C_p/C)(y − y₁₀₀) = (C_n/C)(x₁₀₀ − x)                (6)
y = y₁₀₀ + Q/C_p ,   x = x₁₀₀ − Q/C_n                          (7)
OCV = U_p(y₁₀₀ + Q/C_p) − U_n(x₁₀₀ − Q/C_n)                    (9)
```

`[인쇄, 식 9 뒤]` "The eSOH parameters are utilization window at charged state and
capacity, **(x₁₀₀, C_n)** and **(y₁₀₀, C_p)**, for negative and positive electrode,
respectively."

`[인쇄, p.4]` z 의 정의: "z is the **depth of discharge (DOD)** of the cell
(z = 1 − SOC)". **이 논문에서 DOD 는 방전 심도이고 Fig. 8 의 x축이다.**

`[해석]` 우리 프로젝트의 `windowed_curve` 좌표와의 사전(dictionary): 식 (7) 은
전극 화학량론을 **Ah 축에서 아핀**으로 놓는 것이며, 우리 `(α, β)` 매개화와
1:1 이다 (`α ↔ 1/C_i`, `β ↔ x₁₀₀` 또는 `y₁₀₀`). 정본 대사는
`comparisons/halfcell-window-parametrization-lineage.md` 에 이미 기록돼 있다.

### 6.3 §3.2.2 팽창 모델 (p.4) — 두 번째 관측의 정의

```
t_c   = n_c [ t_p(y) + t_n(x) ] + t_ic⁰                        (10)
Δt_i  = ξ_i ΔV_i t_i⁰                                          (11)   ← 입자 부피변형 → 전극 두께
t_c   = n_c [ (1+ΔV_p(y)) t_p⁰ + (1+ΔV_n(x)) t_n⁰ ] + t_ic⁰    (12)
Δt_c  = t_c − t_c¹⁰⁰                                           (14)   ← 만충 기준 상대 팽창
Δt_c  = n_c [ (ΔV_p(y₁₀₀+Q/C_p) − ΔV_p(y₁₀₀)) ξ_p t_p⁰
            + (ΔV_n(x₁₀₀−Q/C_n) − ΔV_n(x₁₀₀)) ξ_n t_n⁰ ]       (15)
```

`[인쇄, 식 11]` 가정 두 개: "the electrode **only expands in the through-plane
direction**" 과 "the changes in electrode thickness come **only from the active
material** and contribution of binder and other add-ons are not considered".

`[인쇄, 식 14 앞]` 기준점 선택 이유: "In application, **batteries rarely go to the
fully discharged state**, hence for convenience the expansion is assumed to be
measured **with respect to the fully charged state**."

`[해석]` **이 기준점 선택이 §6 의 실험 설계를 강제한다** — 팽창이 만충 기준이라
데이터 창이 반드시 만충에서 시작해야 하고, 논문도 그렇게 인쇄한다 (§9.0).

### 6.4 §3.2.3 LLI/LAM 정의식 (p.5) — ★ 정의만 하고 버려진다

```
LAM_pe% = (1 − C_pa/C_pf) × 100 ,   LAM_ne% = (1 − C_na/C_nf) × 100     (16)
n_Li = (3600/F) ( y C_p + x C_n )                                        (17)
n_Li = (3600/F) ( y₁₀₀ C_p + x₁₀₀ C_n )                                  (19)   ← 만충 기준, SOC 무관
LLI% = (1 − n_Li^a / n_Li^f) × 100                                       (20)
```

`[인쇄, 식 16 뒤]` "Note that the LAM here is the **overall amount of LAM of
lithiation and delitiation**." → 즉 `LAM_liPE`/`LAM_dePE` 를 다시 합친 굵은 모드다.
`[인쇄, 식 20 뒤]` "**LLI here denotes the total loss of lithium.**"

`[해석] ★★ 이것이 이 흡수의 결정적 지점이다.` 식 (16)·(20) 은 CRB 로 잰
`θ` 를 **모드로 바꾸는 결정론적 사상**이다. 그러므로 논문은 원하기만 하면
`Σ` (식 32) 를 그 사상으로 전파해 **LLI·LAM 의 오차막대를 인쇄할 수 있었다**:

- `LAM_ne` 는 `C_n` 만의 단조함수 → `σ(LAM_ne)` 는 `Σ` 의 **대각선 하나**로 끝난다
- `LAM_pe` 는 `C_p` 만의 단조함수 → 마찬가지
- **`LLI` 는 `y₁₀₀C_p + x₁₀₀C_n` 의 조합이라 `Σ` 의 비대각 성분이 필요하다**
  — 논문은 그 `Σ` 를 이미 갖고 있다 (식 32)

**그런데 하지 않는다.** §5 이후 `LLI`·`LAM` 은 어휘 전수 기준 **0회**다 (G1).
`[해석]` 이 논문은 **모드 좌표의 오차공분산을 계산할 재료를 전부 손에 쥔 채
전극 좌표에서 멈춘다.** 우리 프로젝트가 서 있는 자리가 바로 그 다음 칸이다.

---

## 7. §4 상전이 물질 모델 (p.5–7) — 왜 "기울기 변화" 가 정보인가

`[인쇄, p.5 §4 도입]` "In section 5, it will be shown that **the sensitivity matrix
of OCV and expansion to the parameters is related to the slope of each electrode
potential and expansion.** In the following, the connection between these slopes
and the phase transitions of electrode material is explained."

### 7.1 전위 (p.5–6)

- LFP: 정규용액(regular solution) 모형 식 (21)–(22) 로 **평탄역이 생기는 이유**를
  세우고, 그로부터 **구간선형 근사** 식 (23) 을 만든다. 평탄역 경계
  `[인쇄]` `(y⁻, y⁺) = (0.05, 0.97)`, 중점 전위 `V⁰ = 3.45 V`, 범위 2.5–4.5 V.
- Graphite: 스테이지 상전이 4개를 Table 1 로 정리하고 구간선형 식 (24).
  `[인쇄, Table 1]`:

| 물질 | 상 공존 | `x, y` 범위 | 평탄역 전위 `V⁰` (V) |
|---|---|---|---|
| LFP | FePO₄ & LiFePO₄ | `y` 0–1.0 | 3.45 |
| Graphite | Dilute 1 & Stage 4 | `x` 0–0.13 | 0.2 |
| Graphite | Stage 4 & Stage 3 | `x` 0.13–0.24 | – (**평탄역 없음**) |
| Graphite | Stage 3 & Stage 2 | `x` 0.24–0.5 | 0.12 |
| Graphite | Stage 2 & Stage 1 | `x` 0.5–1.0 | 0.09 |

`[인쇄]` "the stage 4 to 3 transition **does not produce a plateau** [19], therefore,
is approximated with a line."

### 7.2 격자 부피 변화 (p.6–7)

`[인쇄, Table 2]` 격자 상수에서 계산한 상별 부피 변화:

| 물질 | 상 | `x, y` | 단위격자 부피 (Å³) | ΔV (%) |
|---|---|---|---|---|
| LFP | LiFePO₄ | 1.00 | 291.2 | 0 |
| LFP | FePO₄ | 0.00 | 271.5 | **−6.76** |
| Graphite | C | 0 | 52.13 | 0 |
| Graphite | Stage 4 | 0.13 | 53.28 | 2.20 |
| Graphite | Stage 3 | 0.24 | 54.25 | 4.06 |
| Graphite | Stage 2 | 0.50 | 55.35 | 6.18 |
| Graphite | Stage 1 | 1.00 | 58.94 | **13.06** |

구간선형 팽창 함수 `[인쇄, 식 (25)·(26)]`:

```
ΔV_n(x) [%] = 16.96x                       x < 0.13
              16.91(x−0.3) + 2.20          0.13 ≤ x < 0.24     ← 텍스트 추출 기준. 이 구간의
              8.13(x−0.2) + 4.06           0.24 ≤ x < 0.50        계수 표기는 그림 6 과
              13.76(x−0.5) + 6.18          0.5 ≤ x               대조하면 오식 가능성 있음 (§7.3)
ΔV_p(y) [%] = −6.76 (1 − y)                                     (26)
```

`[해석] ★ 이것이 팽창이 이기는 물리적 이유다.` graphite 는 **전위가 평탄한
구간에서도 부피가 계속 커진다** (13.06 % 를 4개 기울기로 나눠 쓴다). LFP 는
전위도 평탄하고 팽창도 **단일 기울기**(식 26, 선형)다. 그래서 §10.3 의
"팽창은 음극에 훨씬 이롭다" 가 나온다 — 논문 자신의 설명과 일치한다.

### 7.3 식 (25) 두 번째 줄의 표기 의심 `[해석]`

텍스트 추출에서 두 번째 구간이 `16.91(x−0.3) + 2.20` 으로 나오는데, `x=0.13`
에서 이 값은 `16.91×(−0.17)+2.20 = −0.67 %` 로 **첫 구간의 끝값(2.20 %)과
불연속**이다. 세 번째·네 번째 구간은 연속이다 (`x=0.24`: `8.13×0.04+4.06=4.39`
vs 앞 구간 예상 4.06 — 여기도 미세 불일치). Fig. 6(b) 를 보면 곡선은 **연속**
이다. `[해석]` 조판 또는 추출 과정의 오식으로 보이며, **인용할 때는 식 (25)
자체가 아니라 Table 2 의 격자 데이터를 근거로 삼는 것이 안전하다.** 원 PDF 를
확대 대조하지는 않았다 — **미확인 항목으로 남긴다.**

---

## 8. §5 파라미터 식별 (p.7–8) ★★ — 이 논문의 심장

### 8.1 §5.1 추정 문제 (p.7)

Q3 (§2) 에 전문을 옮겼다. 요점 재확인:
- `θ = [x₁₀₀, y₁₀₀, C_n, C_p]` (4개)
- 목적함수는 **비가중 L² 잔차합** (`‖Y − Ŷ‖²`) — **전압과 팽창을 단위 없이 그냥
  더한다.** `[해석]` 가중치가 없다는 것은 문제 (P) 자체가 mV 와 μm 를 같은 무게로
  본다는 뜻인데, CRB 쪽(식 29·35)에서는 `E⁻¹` 로 정확히 가중한다. **(P) 와 CRB 의
  가중이 서로 다르다** — 논문은 이 불일치를 언급하지 않는다. 실제 추정을 돌리지
  않으므로(G3) 드러나지 않는다.
- 등식 제약 **1개**: `U_p(y₁₀₀) − U_n(x₁₀₀) = V_max`
- `C` 는 θ 밖 → 사후에 식 (27) 로 푼다

### 8.2 §5.2 식별 가능성 방법론 (p.7–8)

식 (28)–(34). Q1 (§2) 에 전사했다. 여기서는 **인쇄된 판정 기준**만 다시 못 박는다:

> `[인쇄, p.7]` **If 𝒪ᵀ 𝓘_f 𝒪 is nonsingular, then the constrained problem is
> identifiable**, moreover, the error covariance, Σ matrix i.e. constrained CRB is (32)

`[해석]` 이것은 **이분법(binary) 판정**이다 — 특이하면 식별 불가, 아니면 식별 가능.
정도(degree)는 식 (33)·(34) 의 표준오차가 맡는다. 조건수 같은 **연속 지표는 없다**.

`[인쇄, p.7, 식 28 뒤]` ε 의 정체: "an additive measurement error, which **can
include measurement noise and model mismatch**." `[해석]` 모델 오차를 ε 안에
넣는다고 선언해 놓고 §6 에서는 `σ_V=10 mV, σ_t=5 μm` 를 **센서 노이즈 수준으로**
쓴다. 구간선형 OCP 근사의 오차(Fig. 4 에서 데이터-모델 편차가 눈에 보인다)는
10 mV 를 넘는 곳이 있으므로, 이 σ 는 **낙관적**이다 `[해석]`.

### 8.3 §5.3 감도행렬과 rank ★ (p.8)

**전압 감도** `[인쇄, 식 (37)]`:

```
∂OCV_i/∂x₁₀₀ = (∂OCV_i/∂x_i)(∂x_i/∂x₁₀₀) = − ∂U_n/∂x_i        (37)
∂OCV_i/∂y₁₀₀ = ∂U_p/∂y_i
```

`[인쇄, 식 (38)]` — 4열 감도행렬 (전압만):

```
             ⎡ −∂U_n/∂x₁   ∂U_p/∂y₁   (Q₁/C_n²)(∂U_n/∂x₁)   −(Q₁/C_p²)(∂U_p/∂y₁) ⎤
S_V(θ*)  =   ⎢     ⋮           ⋮              ⋮                      ⋮            ⎥
             ⎣ −∂U_n/∂x_N   ∂U_p/∂y_N  (Q_N/C_n²)(∂U_n/∂x_N)  −(Q_N/C_p²)(∂U_p/∂y_N)⎦
```
(부호·인수 배치는 조판 수식을 재구성한 것이며 **텍스트 추출이 심하게 깨져 있어
행렬 전체를 글자 단위로 대조하지는 못했다** — 열의 **의미**는 §5.3 본문이
글자로 확인해 준다: 1열 = 음극 전위 기울기, 2열 = 양극 전위 기울기, 3·4열은
"calculated similarly".)

**★ rank 판정문** `[인쇄, p.8]`:

> For the case of voltage only measurements, **if all the measurements are from a
> single slope the first and second columns in the sensitivity matrix in Eq. (38)
> become linearly dependent** due to the same values of entries for all
> measurements. Thus, **the sensitivity matrix is rank deficient and the problem is
> unidentifiable.** Hence, at minimum the measurements have to be taken from
> regions with different slopes.

`[해석]` **이 문단이 이 논문에서 우리 축(비유일성)에 가장 가까운 자리다.**
말하는 바: 모든 측정점이 같은 평탄역 안에 있으면 `∂U_n/∂x` 와 `∂U_p/∂y` 가 각각
상수라, `S_V` 의 1열과 2열이 **상수 벡터의 배수**가 되어 서로 비례한다 →
`(x₁₀₀, y₁₀₀)` 방향으로 **완전 축퇴**. 이것은 근사가 아니라 **구조적(전역)
진술**이다 — 구간선형 모형 안에서는 정확하다.

**팽창 감도** `[인쇄, 식 (39)]`:

```
∂Δt_ci/∂x₁₀₀ = n_c ξ_n t_n⁰ [ ∂ΔV_n/∂x |_{x_i} − ∂ΔV_n/∂x |_{x₁₀₀} ]
             ≡ w_n [ ΔV_n'(x_i) − ΔV_n'(x₁₀₀) ]                        (39)
   where  w_n = n_c t_n⁰ ξ_n ,   w_p = n_c t_p⁰ ξ_p
```
`[인쇄, 식 39 뒤]` 두 번째 열: `∂Δt_ci/∂y₁₀₀ = w_p [ ΔV_p'(y_i) − ΔV_p'(y₁₀₀) ]`.

`[해석] ★ 이 식 하나가 팽창 관측의 성격을 다 말한다.` 팽창 감도는 **기울기의
절대값이 아니라 두 지점 기울기의 차**다. 그러므로:
- LFP 처럼 `ΔV_p` 가 **선형**이면 `ΔV_p'` 가 상수 → **2열이 통째로 0**
  (`ΔV_p'(y_i) − ΔV_p'(y₁₀₀) = 0`). 즉 **팽창은 `y₁₀₀` 에 대해 정보를 전혀
  주지 않는다.** 이것이 Fig. 8(b) 에서 두 곡선의 차이가 작은 이유이고,
  논문의 "팽창은 음극에 더 이롭다" 의 정확한 기전이다. **논문은 이 0을 명시하지
  않는다** — "LFP expands at a constant rate" 라고만 쓴다 (p.10).
- graphite 는 `ΔV_n'` 이 4구간 계단이므로 `x₁₀₀` 이 어느 구간에 있느냐에 따라
  1열이 살아난다.

`[인쇄, 식 40 뒤 결론]` "Therefore **the identifiability of the parameters in the
estimation problem depends on the number of rate changes** in electrode
potential/expansion included in the measurement."

### 8.4 §5.4 가상 셀 모델 (p.8) — 유일한 실제 적합

`[인쇄]` "The eSOH parameters are **fitted to the full range** of voltage and
expansion data. The fitting results are reported in Table 3."

`[인쇄, Table 3]` 가상 모델의 파라미터:

| 항목 | Graphite | LFP |
|---|---|---|
| 전극 두께 `t_i⁰` (μm) | **43** [29] | **70** [30] |
| 활물질 부피분율 `ξ_i` | **0.63** [29] | **0.42** [30] |
| 전극 전위 `U_i` | 식 (24) | 식 (23) |
| 입자 부피팽창 `ΔV_i` (%) | 식 (25) | 식 (26) |

| 적합값 | `x₁₀₀` | `y₁₀₀` | `C_n` (Ah) | `C_p` (Ah) |
|---|---|---|---|---|
| | **0.741** | **0.038** | **27.85** | **21.65** |

`[해석]` **이 4개가 CRB 를 평가하는 유일한 동작점 θ\* 다** (G6).
파생값: `C_n/C_p = 1.286` (N/P 용량비), 그리고 식 (27) 로 풀리는 셀 용량은
`[도표]` Fig. 7 에서 `y₀ ≈ 0.93` → `C ≈ (0.93−0.038)×21.65 ≈ 19.3 Ah`
(공칭 20.5 Ah 보다 작다). `[해석]` 이 값은 논문이 인쇄하지 않았고 위 대사는
우리 계산이다.

**`n_c` 는 표에 없다** (G7). 그러므로 `w_n = n_c × 43 × 0.63`,
`w_p = n_c × 70 × 0.42` 의 절대 크기를 알 수 없고, Fig. 8 은 재현 불가다.
`[도표]` 참고로 Fig. 1(c) 의 **실측** 팽창 전폭은 SOC 100 %→0 % 에서
**≈ 54 μm** (오른쪽 축 0–60 μm, 단조가 아니라 SOC 65 % 부근 ≈31 μm 로 내려갔다
SOC 35 % 부근 ≈38 μm 로 다시 올라온 뒤 0 으로 떨어진다). 한편 Fig. 3(b) 의
**모형** 셀 팽창은 전폭 **≈ 0.8 μm** 다 — `n_c = 1`(단층) 계산으로 보인다
`[해석]`. 두 그림의 스케일이 **70배 가까이 다르므로**, `σ_t = 5 μm` 가
Fig. 8 에서 어느 쪽 스케일에 대해 걸린 값인지 논문만으로는 확정할 수 없다.

---

## 9. §6 결과 (p.9–10) ★ — Fig. 8 정독

### 9.0 실험 설계 (p.9)

`[인쇄]` "The data window is defined as follows: it is assumed that there is **one
measurement opportunity at every 1 % change in SOC**, starting from the **fully
charged state**. With each addition of the measurements, the standard error of the
parameters is calculated. The size of the data window is denoted by the **depth of
discharge (DOD)**."

`[인쇄]` "This result is obtained using **σ_V = 10 mV** and **σ_t = 5 μm**
measurement error."

`[인쇄]` 창을 만충에서만 시작하는 이유: "since the expansion is defined **with
respect to the fully charged state** (see Eq. (14)) and to be able to compare the
two scenarios, only the data windows starting from the fully charged state are
considered."

`[해석]` **이 제약은 팽창 시나리오 때문에 생긴 것이고, 전압 시나리오를 불리하게
만들 수 있다.** 논문 스스로 "It is straight-forward to apply the same analysis for
a data window starting at a lower SOC for voltage" 라고 인정하면서 하지 않는다.
전압만 시나리오는 **중간 SOC 창**에서 훨씬 유리할 수 있다 (graphite 기울기 변화가
그쪽에 있다). **미검증 — 이 논문이 안 한 대조군이다.**

`[인쇄]` 응용 맥락: "for transportation applications, the data can accumulate every
time there is an open circuit opportunity, for instance, **at every key-on with
ample rest time** before it. Also, at very low c-rate such as **level 1 charging**."

### 9.1 §6.1 상전이와의 연결 (p.9–10)

`[인쇄]` "as the measurements move to a higher DOD, the estimation error decreases
for all the parameters. **This reduction happens in stages, which corresponds to
the phase transitions in the material.**"

`[인쇄]` "for the parameter **C_p**, in case of voltage alone measurement, the
estimation error **remains at a constant value until almost 98 % DOD**, which
corresponds to the stoichiometric state (y⁺) bounding the plateau in LFP."

`[인쇄]` DVA 와의 정합: "the results agree with the long-established method,
**Differential Voltage Analysis (DVA)**, which depends on terminal voltage data
across phase transitions to compute the shifts of the peak locations in the
dV/dQ curve [31]."

`[인쇄]` **자기 완화 문장** (중요): "the results indicate that the parameters are
unobservable at low DOD regions. However, **in practice, compared to the simple
model used in this study, there are more non-linearities near the low DODs which
results in better-conditioned sensitivity matrices.** Hence, **the observability of
the parameters should enhance in practice**."

`[해석]` 이 한 문장이 논문의 정량 결론(30 % / 70 %)을 **모형 의존적**으로
못 박는다 — 구간선형 근사가 평탄역을 **완전 평탄**으로 만들었기 때문에 rank
결손이 그렇게 깨끗하게 나온 것이고, 실제 OCP 의 미세 곡률은 그 결손을 메운다.
**즉 이 논문의 "unidentifiable" 은 실제 셀의 성질이 아니라 구간선형 모형의
성질일 수 있다**, 그리고 저자들도 그렇게 적는다.

### 9.2 §6.2 파라미터 사이의 결합 (p.10) — 유일한 비대각 진술

`[인쇄]` "Recall that the problem (P) includes an equality constraint (maximum
voltage limit) which **intrinsically couples the error estimates of parameters
x₁₀₀ and y₁₀₀**. Using the Taylor series expansion of the voltage constraint about
the true solution the following equation is obtained"

```
σ_y (∂U_p/∂y)|_{y₁₀₀}  =  σ_x (∂U_n/∂x)|_{x₁₀₀}                (41)
```

`[인쇄]` "It is apparent that ∂U_n/∂x at flat region of U_n is **smaller** than
∂U_p/∂y which is at the higher derivative region of U_p. Since the estimation error
of x₁₀₀ and y₁₀₀ are **proportional through Eq. (41)**, it stands to reason that
**x₁₀₀ has larger estimation error than y₁₀₀**."

`[해석] ★ 이것이 이 논문에서 파라미터 간 **결합**을 인쇄한 유일한 자리다.`
그런데 이 결합은 `Σ` 의 비대각 성분에서 읽은 것이 **아니라 제약식 (3) 을
1차 전개해서 얻은 것**이다. 즉 `Σ` 를 갖고 있으면서도 축퇴 방향은 **제약식
쪽에서만** 본다. 식 (41) 은 σ 사이의 **비율**을 정할 뿐 두 오차가 **어느 방향으로
같이 움직이는지**(부호·상관계수)는 말하지 않는다.

`[인쇄]` `C_n`·`C_p` 에 대한 설명: "For **C_p** to have a lower parameter error the
window should include **at least one of the asymptotes of U_p** function i.e. at
least two different slopes. Thus, the reason parameter error of C_p is small near
the edges of fully discharged states. The same analysis is also true for C_n. As
the U_n function is **almost flat until high DODs**."

### 9.3 Fig. 8 — 직접 본 것 `[도표]`

**패널 4개 공통 축**: x = DOD [%] 0–100, y = Error [%] 0–10 (상한 10 에서 잘림),
5 % 에 점선 판정선. 범례 `Voltage`(파선) / `Voltage+expansion`(실선).
그림 안 라벨: (a) 에 화살표와 **`Unobservable`** 박스 (텍스트 층에는 없다, §3.0).

| 패널 | `Voltage` (파선) | `Voltage+expansion` (실선) |
|---|---|---|
| **(a) x₁₀₀** | DOD **≈ 69 %** 에서 수직 벽 (그 왼쪽은 화면 밖 = 관측 불가). 벽 직후 ≈1.9 % → 1.2 % 로 계단 하강 | DOD **≈ 29–30 %** 에서 수직 벽. 직후 ≈1.7 % → 1.2 % → (95 % 이후) ≈0.9 % |
| **(b) y₁₀₀** | DOD ≈2–3 % 에서 10 % 를 넘지만 **급격히 하강**, DOD ≈4–5 % 에서 이미 5 % 아래, 20 % 에서 ≈1 %, 28 % 이후 ≈0.05 % | DOD 2 % 에서 이미 ≈1.2 %, 28 % 이후 ≈0.03 % |
| **(c) C_n** | DOD **≈ 69–70 %** 에서 수직 벽 → 5 % 통과. 이후 ≈1.9 % 로 평탄 | DOD **≈ 11–12 %** 에서 5 % 통과. 20–40 % 에서 ≈3.5 %, 70 % 에서 ≈2.2 %, 95 % 이후 ≈1.0 % |
| **(d) C_p** | DOD ≈8 % 부터 **≈5.1 % 로 평탄** — **5 % 판정선 바로 위에 붙어서** DOD **≈98 %** 까지 유지되다 급락 | DOD 0–40 % 에서 **≈5.0 %** 평탄, 이후 하강: 68 % 에서 ≈3.4 %, 80 % 에서 ≈2.1 %, 95 % 에서 ≈1.9 %, `y⁺` 마커(≈97 %) 이후 급락 |

**(a) 의 수직 점선 마커** `[도표]`: `x₁⁻`(DOD ≈29–30 %), `x₂⁻`(≈69–71 %),
`x₃⁻`(≈93–95 %). Table 1 과 대조하면 `x₁⁻ = 0.5`(stage 2/1 평탄역 끝),
`x₂⁻ = 0.24`, `x₃⁻ = 0.04` 다 — `x = x₁₀₀ − Q/C_n` 로 환산하면 `x₂⁻ → 68 %`,
`x₃⁻ → 95 %` 로 그림과 잘 맞고, `x₁⁻ → 34 %` 로 그림 판독(≈29 %)과 **4–5 %p
어긋난다** `[해석]` (내 화소 판독 오차일 수도, 그림 쪽일 수도 있다 — 미해결).

**★ G14 의 근거** `[해석]`: 5 % 기준을 **네 파라미터 전부**에 엄격히 적용하면
- **팽창 있음**: `C_p` 가 DOD 0–40 % 구간 내내 **≈5.0 %** 로 판정선에 정확히
  얹혀 있다. 인쇄된 "about 30 % DOD" 는 `C_p` 를 **간신히** 통과시키거나
  통과시키지 못한다. 실질적으로 30 % 를 정하는 것은 `x₁₀₀` 의 벽(≈29 %) 과
  `C_n` 의 5 % 교차(≈12 %) 다.
- **팽창 없음**: `C_p` 는 DOD **≈98 %** 까지 5 % 아래로 내려오지 않는다.
  Abstract 의 ">70 %" 는 `x₁₀₀`·`C_n` 의 벽(≈69 %)이 정한 값이며,
  **`C_p` 를 포함하면 같은 기준에서 ≈98 % 를 요구한다.** 논문은 이 98 % 를
  §6.1 에 인쇄해 놓고 Abstract·Highlights 에 반영하지 않는다.

`[해석]` 즉 **인쇄된 30 % / >70 % 는 "네 파라미터 전부" 가 아니라 "음극
파라미터" 의 숫자다.** Highlights 1·2 가 "graphite lithiation state" 라고 대상을
좁혀 말한 것이 오히려 정확하고, Abstract 의 "the parameters" 가 넓다.

### 9.4 §6.3 팽창의 이득 (p.10)

`[인쇄]` "This reduction is **more significant for the negative electrode
parameters (x₁₀₀, C_n) than the positive electrode parameters (y₁₀₀, C_p)**. The
reasons are that in the case of graphite/LFP cell; first, **the slopes of ΔV_p/n
functions are a magnitude larger than the slopes of U_p/n functions**. Second,
**graphite has several rate changes while expanding, whereas LFP expands at a
constant rate.** As a result, the expansion is more sensitive to a change in
parameters compare to voltage, especially in the middle SOC region."

`[해석]` 두 번째 이유는 §8.3 에서 본 대로 **`S_t` 의 2열이 정확히 0** 이라는
뜻인데, 논문은 "constant rate" 까지만 쓰고 0 이라고 쓰지 않는다.

---

## 10. §7 결론 (p.10) — 저자들이 스스로 적은 것

`[인쇄]` 전문 중 판정 부분:

> The results of the lower bound of the estimation error of the individual electrode
> parameters using the constrained CRB formulation were compared for two scenarios of
> voltage measurement alone and voltage plus expansion measurements. **The sensitivity
> matrix depends on the slope of the OCV and expansion curves.** It was shown for the
> voltage only case that **the measurements should be taken at a wider range of SOC
> spanning at least two phase transitions, in order to make all the parameters
> identifiable.** However, the addition of expansion measurements **made the
> parameters identifiable for shallower depth of discharges.** As a result, for
> material like LFP with flat voltage response at middle SOC regions the estimation of
> the individual electrode parameters is feasible by including the expansion
> measurements.

`[인쇄]` 저자들이 적은 **한계와 향후 과제** (전문):

> The analysis here was based on a set of **simplifying assumptions**. The goal was to
> study the usefulness of the expansion measurements under limited data and the
> presence of noise. The conclusion is that having this additional information is not
> only beneficial, but it could be even **necessary** for better eSOH estimation
> techniques. In future works, **the estimation of eSOH parameters with data collected
> from fresh and aged cells, effects of temperature, hysteresis, and the dynamics of
> the battery under nonzero current profile** needs to be considered.

`[해석]` 향후 과제 목록에 **"실제 추정기를 돌려 복원 오차를 보는 것"** 이 들어
있다 ("the estimation of eSOH parameters with data collected from fresh and aged
cells"). 즉 저자들도 G3 를 알고 있으며 다음 논문으로 미룬다.
**`global identifiability`·`비유일성`·`상관`은 향후 과제에도 없다.**

---

## 11. 그림 — 본 것과 안 본 것 (정직하게)

크로핑 결과 **9장** (`fig_1`–`fig_8`, `tab_2`).
`raw/figures/mohtat2019_electrode-soh-estimability-expansion/figures.json` 에 캡션 색인.

| 파일 | 무엇 | 봤나 | 왜 / 무엇을 얻었나 |
|---|---|---|---|
| `fig_8.png` | **★ 핵심 결과** — 파라미터 오차 vs DOD, 전압 vs 전압+팽창 | **봤다** | §9.3 전체. `Unobservable` 라벨·수직 벽 위치·`C_p` 의 5.1 % 평탄이 전부 여기서 나왔다 |
| `fig_2.png` | fresh/aged OCV + 반쪽전지 전위 (LAM_deNE 28 %) | **봤다** | 두 OCV 곡선이 거의 겹치는 것(용량 ≈20.5→19.5 Ah)과 `x₁₀₀` 이 0.741→≈0.98 로 크게 이동하는 것을 눈으로 확인 |
| `fig_3.png` | 같은 열화 시나리오의 **팽창** | **봤다** | aged(빨강) 가 fresh(파랑) 위로 **뚜렷이** 분리 (Q=0 에서 ≈1.65 vs ≈0.78 μm). 팽창 전폭이 ≈0.8 μm 인 것도 여기서 (G7 근거) |
| `fig_7.png` | Table 3 적합 결과 + 전극 전위/팽창 대응 | **봤다** | Table 3 값 대조, `y₀ ≈ 0.93`·`x₀ ≈ 0.03` 판독, **팽창이 "normalized" 라 절대 스케일이 감춰져 있음**을 확인 |
| `fig_4.png` | LFP·graphite 전위와 구간선형 근사 | **봤다** | `x₁⁻…x₃⁺`, `y⁻ y⁺` 마커 위치 확인 → Fig. 8 의 마커 해석 근거. 모델-데이터 편차가 눈에 보이는 것도 확인 (§8.2 의 σ 낙관 지적 근거) |
| `fig_1.png` | (a) 셀 모식도 (b) 지그 (c) **실측 V·팽창 vs SOC** | **봤다** | (c) 에서 실측 팽창 전폭 **≈54 μm** 판독 — G7 의 스케일 대조 |
| `fig_5.png` | LiC₆ · LiFePO₄ 결정구조 | **안 봤다** | 결정구조 삽화. 수치는 Table 2 가 정본이고 이 그림에서 새로 얻을 것이 없다 |
| `fig_6.png` | 식 (25)·(26) 구간선형 팽창 함수 + Table 2 점 | **안 봤다** | §7.3 의 식 (25) 오식 의심을 **이 그림으로 확인했어야 한다.** 안 봤으므로 그 항목은 **미확인**으로 남겼다 |
| `tab_2.png` | Table 2 이미지 | **안 봤다** | 표는 PDF 텍스트가 정확하다 (추출기 안내 규약) |

**본문 서술과 어긋난 그림**: 정면 충돌은 **없었다.** 단 두 건의 **불일치 성격의
관찰**이 있었고 위에 기록했다 —
(i) Fig. 8(d) 의 `C_p` 가 두 시나리오 모두 5 % 선 근처에 붙어 있어 Abstract 의
30 % / >70 % 를 그대로 지지하지 않는다 (§9.3, G14),
(ii) Fig. 8(a) 의 `x₁⁻` 마커 위치가 Table 1·식 (7) 환산값(≈34 %)보다
왼쪽(≈29 %)에 보인다 — 내 판독 오차 가능성을 배제하지 못했다.

---

## 12. 우리 프로젝트와의 접점

### 12.1 채택할 것

1. **제약 CRB (Stoica–Ng nullspace 사영, 식 30–32) 는 우리 Phase 1e/1h 와 같은
   기계다.** 우리는 컷오프 등식의 gradient 를 특이벡터와 대조했는데, Mohtat 은
   그 gradient 의 **nullspace 정규직교기저 `𝒪`** 로 Fisher 를 사영한다. 우리
   결과를 "제약 하 CRB" 언어로 다시 쓰면 이 계보와 직접 대화가 된다.
   개념 페이지: [[constrained-crb-identifiability]].
2. **감도행렬의 열이 "반쪽전지 OCP 의 기울기" 라는 사전 (식 37).** 우리
   `windowed_curve` 야코비안의 열이 정확히 같은 의미다. 우리 조건수·특이값을
   "몇 개의 기울기 변화가 창 안에 들어왔는가" 로 물리적으로 해석할 수 있다.
3. **팽창 감도가 "기울기의 차" 라는 구조 (식 39).** 새 관측을 추가할 때
   **관측이 파라미터에 대해 상수 기울기를 가지면 그 열은 0** 이라는 판정을
   준다. PVS·SEV 같은 후보 feature 를 목적함수에 넣기 전에 이 검사를 먼저
   할 수 있다 ([[pvs-sev-lli-lampe-separability]]).

### 12.2 점검할 것 (우리 자료로 답할 수 있는 것)

| # | 점검 | 왜 |
|---|---|---|
| C1 | **Mohtat 의 rank 판정(식 38 열 1·2 선형종속)이 우리 PyBaMM 참값에서도 성립하나** — 즉 창을 한 평탄역 안으로 좁히면 `(x₁₀₀, y₁₀₀)` 방향 σ 가 발산하나 | 그의 판정은 **구간선형 모형**의 성질이다. 실제 OCP(우리 PyBaMM OCP)에서 얼마나 완화되는지가 곧 "이 계보의 결론이 모형 인공물인가" 의 답이다. 논문 스스로 "should enhance in practice" 라고 적었으므로 **저자가 열어 둔 질문** |
| C2 | **`Σ` 를 식 (16)·(20) 으로 전파한 `σ(LLI)`·`σ(LAM_pe)`·`σ(LAM_ne)`** — Mohtat 이 재료를 다 갖고도 안 한 계산 | **우리 논지의 정확한 빈칸이자, 우리가 이 계보에 공급할 수 있는 것**. 특히 `LLI` 는 비대각 성분을 요구하므로 "대각선만 보고하는 관습" 을 정면으로 깬다 |
| C3 | **팽창(또는 그 대용 관측)을 우리 관측 벡터에 더하면 σ_min 이 얼마나 줄어드나** | Mohtat 의 판정은 "관측 추가로 식별 가능성을 산다" 인데, 우리 Phase 1e/1h 는 "등식 제약 추가는 손해" 였다. **관측 추가와 제약 추가는 다른 처방**이고, 우리는 아직 전자를 안 재 봤다 |
| C4 | **σ 수준 의존성** — Mohtat 은 `σ_V=10 mV, σ_t=5 μm` 한 점만 쓴다 (G4). CRB 가 `1/σ²` 스케일이므로 판정선(5 %)이 σ 에 **선형**으로 붙어 있다 | 우리가 σ 를 스윕하면 "30 % DOD" 가 σ 의 함수로 어떻게 움직이는지 곧바로 나온다. 논문에 없는 축 |

### 12.3 우리가 이 논문에 공급할 수 있는 것

`[해석]` 세 가지다.
1. **모드 좌표의 오차공분산** (C2) — 이 계보가 전극 좌표에서 멈춘 자리.
2. **국소 CRB 밖의 판정** — Mohtat 은 `global` 을 0회 언급한다. 우리 격자 탐색은
   **동작점에서 멀리 떨어진 해**들을 실제로 본다.
3. **추정기를 실제로 돌린 복원 오차** (G3) — CRB 하한과 실제 복원의 간극.

### 12.4 ★ 이 흡수가 우리 통합 논지에 미치는 영향 `[해석]`

`syntheses/mode-identifiability-unmeasured-lineage.md` 의 Thesis 는
"흡수한 편들 중 **분해의 유일성을 잰 편이 하나도 없다**" 였고,
그 문서의 Bias Check 1 이 이 논문을 **가장 위험한 미독 반례**로 지목해 두었다.
**원전을 읽은 결과, 그 Thesis 는 좁혀야 한다.** 정확히 어디까지인지를 아래
표로 갈라 적는다 (이 표만 그 문서로 옮기면 된다 — 이 digest 는 그 파일을
고치지 않는다).

| 논지의 성분 | 이 논문이 **깬** 것 | 이 논문이 **못 깬** 것 |
|---|---|---|
| "식별 가능성을 정량한 편이 없다" | **깨진다.** 제약 CRB 로 파라미터별 표준오차를 계산하고 판정선까지 긋는다 (식 29–34, Fig. 8) | — |
| "축퇴(비유일성)를 지목한 편이 없다" | **깨진다 (1회).** "the first and second columns … become **linearly dependent** … rank deficient … unidentifiable" (p.8) — `(x₁₀₀, y₁₀₀)` 방향의 완전 축퇴를 **구조적으로** 지목한다 | 그 축퇴를 **수치로 재지 않는다** (그 조건이 언제 얼마나 완화되는지 없음). `degenerac*`·`uniqu*`·`collinear*` 0회 |
| "**LLI/LAM 분해**의 유일성을 잰 편이 없다" | — | **못 깬다.** CRB 는 `[x₁₀₀,y₁₀₀,C_n,C_p]` 에만 걸린다. `LLI`·`LAM` 은 §5 이후 **0회** (G1). 모드 좌표의 오차·상관은 인쇄되지 않는다 |
| "축퇴의 **방향**을 보고한 편이 없다" | — | **못 깬다.** `Σ` 를 구하고 즉시 `diag` 만 취한다 (식 33). 파라미터 상관 0회. 유일한 결합 진술(식 41)은 `Σ` 가 아니라 **제약식 1차 전개**에서 나오고, 비율만 주고 방향은 안 준다 (G2) |
| "추정기를 돌려 복원을 검증한 편이 없다" | — | **못 깬다.** 노이즈 실현·복원 오차·수렴 진단이 전부 없다 (G3·G4) |
| "전역 식별 가능성을 다룬 편이 없다" | — | **못 깬다.** Lin 은 최소한 "우리는 국소만 했다" 고 인쇄하는데, Mohtat 은 그 한정조차 인쇄하지 않는다 (`global` 0회, G5) |

`[해석]` 한 문장으로: **"아무도 재지 않았다" 는 틀렸고, "아무도 모드 좌표에서,
방향까지, 추정기로 재지 않았다" 는 여전히 옳다.** 논지의 강도는 낮아지지만
좌표는 오히려 선명해진다 — 우리가 채울 칸이 위 표의 오른쪽 열 네 줄이다.

---

## 13. 비판 — 이 논문의 약한 곳

1. **판정선 5 % 가 근거 없이 선언되고, 그 선이 결론을 만든다** (G8).
   `C_p` 가 두 시나리오 모두 5 % 언저리에 붙어 있으므로(§9.3), 판정선을 4 % 나
   6 % 로 바꾸면 "30 %" 와 ">70 %" 가 크게 움직인다. 민감도 검토가 없다.
2. **헤드라인 숫자가 네 파라미터 중 둘만 반영한다** (G14). 논문 자신이 `C_p` 의
   98 % 를 §6.1 에 인쇄해 놓고 Abstract 는 ">70 %" 라고만 쓴다.
3. **비교가 공정하지 않을 수 있다** — 데이터 창을 **만충 시작**으로 못 박은 것은
   팽창 정의(식 14) 때문이고, 전압만 시나리오는 다른 창에서 더 나을 수 있다.
   논문이 그 대조군을 "straight-forward" 라고 부르면서 수행하지 않는다 (§9.0).
4. **`n_c` 미공개로 재현 불가** (G7). 팽창 감도의 절대 스케일이 미지수이고,
   `σ_t = 5 μm` 의 상대적 세기를 독자가 판단할 수 없다.
5. **목적함수 (P) 와 CRB 의 가중이 다르다** (§8.1). (P) 는 mV 와 μm 를 무가중으로
   더하고, CRB 는 `E⁻¹` 로 가중한다. 추정기를 돌리지 않아 드러나지 않는다.
6. **결론이 모형 인공물일 수 있음을 인정하면서 정량하지 않는다** (§9.1의
   "better-conditioned … should enhance in practice"). 구간선형 근사가 만든
   완전 평탄역이 rank 결손의 원인인데, 실제 OCP 로 같은 계산을 반복하지 않는다.
7. **`Σ` 를 버린다** (G2). 이 논문이 가진 정보 중 우리 축에 가장 값진 것을
   한 줄(식 33)로 폐기한다.
8. **`LLI/LAM` 을 정의만 하고 분석에 넣지 않는다** (G1). 제목이 "electrode-specific
   state of health" 이므로 저자 입장에서는 일관되지만, **열화 모드 분해의
   식별 가능성 문헌으로 이 논문을 인용할 때는 이 경계를 반드시 밝혀야 한다.**

`[해석]` 반대로 **잘한 것**도 적는다: (a) 제약을 무시하지 않고 Stoica–Ng 로
정면 처리한 것, (b) 감도행렬의 열을 물리량(반쪽전지 기울기)으로 해석해
DVA 와 연결한 것, (c) 자기 결론이 모형 의존적일 수 있다고 §6.1 에 인쇄한 것 —
셋 다 이 계보에서 흔치 않다.

---

## 14. 한 줄 결론

`[해석]` **Mohtat 2019 는 "전극 창·용량 4개 파라미터" 의 국소 추정 정밀도를
제약 Cramér–Rao 하한으로 정직하게 계산하고, 팽창이라는 두 번째 관측이 그 하한을
얕은 DOD 에서 살려낸다는 것을 보인 논문이다. 이 계보에서 처음으로 축퇴를
(rank 결손으로) 한 번 지목하지만, 그 축퇴의 방향도, 크기도, 그리고 무엇보다
LLI/LAM 모드 좌표에서의 오차도 인쇄하지 않는다 — 재료를 다 쥐고 대각선만
보고한다.**
