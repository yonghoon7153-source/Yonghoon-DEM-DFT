---
title: "Lin & Khoo 2024 — Identifiability study of Li-ion capacity fade using degradation mode sensitivity (JPS 605, 234446)"
source_url: local-upload/11._Identifiability_study_of_lithiumion_battery_capacity_fade_using_degradation_mode_sensitivity.pdf
ingested: 2026-09-03
sha256: 271c09ad9d025bf8ec0a003c9cfc04f249480fd26028eaca9500b14df893b947
---

# 수집 목적

Jing Lin, Edwin Khoo, **"Identifiability study of lithium-ion battery capacity
fade using degradation mode sensitivity for a minimally and intuitively
parametrized electrode-specific cell open-circuit voltage model"**,
*Journal of Power Sources* **605** (2024) 234446 의 **절별 해체분석**.

이 논문은 이 위키가 **직접 지목해서 예약해 둔** 문헌이다.
[[fused-lasso-feature-design-framework]] 를 흡수하던 2026-09-03 (7) 라운드에서
Rhyu et al. 2025 의 참고문헌 [30] 제목 안에 `identifiability` 가 있는 것을 보고
"이 계보에서 제목에 identifiability 가 있는 **유일한** 문헌이고 우리 프로젝트의
정확한 선행 연구" 라고 적으며 다음 흡수 1순위로 확정했다
([[22p-physics-or-degeneracy]] Status Log 2026-09-03 (4) 항목 3,
[[pvs-sev-lli-lampe-separability]] Status Log (7) 마지막 줄).

따라서 이 digest 의 무게중심은 "이 논문이 무엇을 발견했나" 가 아니라
**"우리가 하려는 판정을 이 논문이 이미 했는가, 했다면 어디까지인가"** 다.

**표기 규칙** (이 위키 관례 3구분):
- `[인쇄]` — 논문 본문/표/식/캡션에 글자로 있는 것
- `[도표]` — 그림에서 눈으로 읽은 근사값 (원 데이터가 아니다)
- `[해석]` — 이 문서를 쓰면서 붙인 판단. **논문의 주장이 아니다**

- 원본 파일: 로컬 업로드 PDF 18쪽 (본문만, **Supporting Information 은 없다**)
- 크로핑 그림: `raw/figures/lin2024_ocv-degradation-mode-identifiability/`
  (fig 9장 + tab 5장, `figures.json` 에 캡션 색인). 실제로 본 그림은 §13 에 명시.

---

## 0. 서지사항 (직접 확인)

`[인쇄]` PDF 1쪽 헤더에서 확인한 것:

| 항목 | 값 |
|---|---|
| 저자 | Jing Lin, Edwin Khoo (교신) |
| 소속 | Institute for Infocomm Research (I2R), A*STAR, Singapore |
| 학술지 | *Journal of Power Sources* **605** (2024) 234446 |
| DOI | 10.1016/j.jpowsour.2024.234446 |
| 접수 / 개정 / 게재 | 2023-09-29 / 2024-03-12 / 2024-03-26 (online 2024-04-11) |
| 키워드 | Lithium-ion battery · Loss of active materials · Loss of lithium inventory · Open-circuit voltage · **Parametric identifiability** · **Sensitivity gradient** |
| 자금 | A*STAR Career Development Fund C210112037 |
| 데이터 | `[인쇄]` "Data will be made available on request." (공개 저장소 **없음**) |
| 감사 | `[인쇄]` "the four anonymous reviewers" |

`[인쇄]` Highlights 5줄 (1쪽) — 논문 자신이 요약한 기여:
1. An electrode-specific OCV model parametrized by N/P and Li/P ratio.
2. Degradation modes and electrode SOC based on material-specific usable
   stoichiometry range.
3. Electrode differential voltage fractions indicating the limiting electrode.
4. **Four regimes of degradation identifiability characterized by Li/N and Li/P ratio.**
5. **Informative SOC windows for degradation mode estimation by Fisher information.**

---

## 1. ★ 원문에 없어서 확인이 필요한 것 (먼저 적는다)

이 절은 논문이 **비워 둔 자리**의 목록이다. 우리 프로젝트가 무엇을 공급할 수
있는지가 여기서 나온다.

| # | 공백 | 근거 (전수/직접 확인) |
|---|---|---|
| G1 | **파라미터 간 상관을 계산해 놓고 버린다.** 오차공분산 `C_θ` 전체를 구한 뒤 **대각선의 제곱근만** 그린다. Fig. 8·9 는 전부 `sqrt(diag(C_θ))` 다. 축퇴의 **방향**(비대각 성분·최소 고유값의 고유벡터)은 손에 쥔 채로 한 번도 표시되지 않는다 | `[인쇄, p.15]` "the standard estimation errors of 𝑟_N/P and 𝑧₀⁺ for each SOC window obtained as the **square root of diag(𝑪_𝜽)**" |
| G2 | **추정기를 한 번도 돌리지 않는다.** NLS 를 식 (50) 으로 정의하고 최적해 `θ*` 에서 Fisher 를 평가한다고 쓰지만, 실제로 최적화를 수행한 결과가 논문에 **하나도 없다**. 복원 오차·수렴·국소최소 분포가 전부 없다 | 본문·그림 전수. Fig. 8·9 는 **참값에서 평가한 CRLB** 지 추정 결과가 아니다 |
| G3 | **노이즈를 한 번도 뽑지 않는다.** `σ_U = 5 mV` 를 **가정**해 Fisher 에 넣을 뿐 난수 실현·반복 실험이 없다. `noise` 라는 단어가 본문에 **0회** | 어휘 전수 §3 |
| G4 | **노이즈 수준 스윕이 없다.** σ_U 는 Fig. 8·9 양쪽에서 5 mV 로 고정. Fisher 가 1/σ² 스케일이므로 `σ_θ ∝ σ_U` 로 자명하지만, 그렇다면 논문이 제시한 판정선(0.2 / 0.01)도 **5 mV 에 붙어 있는 값**이다 | `[인쇄, p.15·Fig.9 캡션]` 두 곳 모두 "assumed to be 𝜎_U = 5 mV" |
| G5 | **전역(global) 식별 가능성을 명시적으로 미룬다.** | `[인쇄, p.13]` "To quantify **global identifiability**, more sophisticated techniques such as those based on Bayesian inversion are needed [26]." / `[인쇄, p.17]` "More empirical tools from statistical inference will be needed to discern global sensitivity, and **we will report our findings in future work**." |
| G6 | **모델 오차를 정성으로만 인정한다.** 크기를 재지 않는다 | `[인쇄, p.15]` "the OCV model is not perfect in practice, and **model errors will limit the estimation accuracy in the first place**, so we consider an estimation error of under 0.01 in this ideal setup as more than enough." |
| G7 | **실측 데이터가 없다.** 전부 Plett 교재의 OCP 적합식으로 만든 합성 계산이다. 셀 하나도 측정하지 않았다 | §5. `[인쇄, p.4]` "the electrode OCP relations are from the LFP, NMC-111 and MCMB … OCP fits provided in Plett [4, sec. 3.11.1], with temperature set to 25 °C" |
| G8 | **복합전극(Si/Gr)을 명시적으로 범위 밖에 둔다.** 그 파라미터 유형을 §2.4 에서 이름 붙여 정의한 뒤 곧바로 버린다 | `[인쇄, p.8]` "parameters governing the component changes in composite electrode active materials [24] … **We will not look into this type of parameters in this work.**" |
| G9 | **동역학이 없다.** OCV 만 다루며 유한 전류는 향후 과제 | `[인쇄, p.18]` "we have only discussed inferring degradation modes from OCV measurements, which has a relatively restricted scope of application in practice" |
| G10 | **Cramér–Rao 의 전제(불편성)가 성립하지 않음을 인정하고 그냥 쓴다** | `[인쇄, p.15]` "Although we do not know 𝜃_tr in practice, and the maximum likelihood estimator 𝜽*(ŷ) is **not necessarily unbiased**, we can still use the inverse of (51) as a **semi-heuristic** error covariance" |
| G11 | **Fig. 9 의 세 파라미터 오차가 서로 다른 참값 크기(700–1400 mAh)에 대해 같은 절대 컬러바(0–100 mAh)를 쓴다.** 상대오차로 환산하면 패널마다 기준이 다르다 | Fig. 9 패널 제목과 컬러바 (직접 봄) |
| G12 | **네 평가점 중 셋을 논문 스스로 "비전형" 이라 부른다.** 그런데 Fig. 8·9 는 그 넷을 동등하게 나열한다 | `[인쇄, p.5·p.13]` "we should expect the Li/P ratio to be less than 1" / "we typically design the N/P ratio to be slightly larger than 1" / "a normal cell **rarely falls into this regime** [Li 과잉]" |
| G13 | **표 4 캡션과 본문 §2.7 이 같은 문장을 "only identifiable" 과 "highly identifiable" 로 다르게 인쇄한다** (§9.3) | 두 곳 대조 |

---

## 2. 다섯 개 최우선 질문에 대한 직답 (근거는 아래 절)

### Q1. identifiability 를 어떤 의미로 쓰는가

**국소(local) · 실용(practical) 식별 가능성이다.** 도구는 **Fisher 정보행렬**이고,
Fisher 는 **해석적으로 유도한 감도 gradient**(Jacobian)에서 만든다.
프로파일 우도·Hessian·특이값분해·조건수는 **쓰지 않는다** (§3 어휘 전수: `hessian`
0회, `singular value` 0회, `condition number` 0회, `profile likelihood` 0회).

논문 자신이 세 문장으로 못 박는다:

- `[인쇄, p.13]` "To study only the identifiability **intrinsic to a problem**, one
  simple approach is based on the sensitivity gradients, as we shall adopt here.
  However, this approach **only concerns how the measurements vary with the
  parameters locally**. To quantify **global identifiability**, more sophisticated
  techniques such as those based on Bayesian inversion are needed [26]."
- `[인쇄, p.14–15]` "such gradient-based identifiability results are **only valid
  locally** and are based on the premise that 𝜽* is near the ground truth 𝜽_tr …
  If the nonlinear optimization does not ever get close to 𝜽_tr, **the above
  results are irrelevant to how close 𝜽* is to 𝜽_tr**."
- `[인쇄, p.17]` "We want to emphasize that any statements based on sensitivity
  gradients are **only valid locally**."

`[해석]` 즉 이 논문은 우리가 [[fitting-degeneracy]] 에서 **flat valley** 라 부르는
것 중 **동작점 근방의 국소 flatness** 만 잰다. **멀리 떨어진 두 해가 같은 곡선을
낸다**는 전역 축퇴, 그리고 **multimodal**(최적화 난이도)은 이 논문의 도구로는
잡히지 않으며, 저자들도 그렇게 적는다.

**단, 예외가 하나 있다** — §2.3 의 자유도 논증은 국소가 아니라 **구조적**
(structural, 전역) 이다. Q3 에서 다룬다. 이것이 이 논문의 가장 값진 부분이다.

### Q2. 미지수가 정확히 몇 개이고 무엇인가

**곡선 좌표에 따라 2개 또는 3개다.**

| 관측 | 미지수 | 개수 | 우리 축과의 대응 |
|---|---|---|---|
| **SOC 기반** `U_OCV(z)`, `z∈[0,1]` (컷오프로 정규화된 곡선 **형상**) | `r_N/P = Q̂⁻_max/Q̂⁺_max`, `z₀⁺ = Q̂^Li_max/Q̂⁺_max` | **2** | `r_N/P = r_N/P,ini·(1−LAM_NE)/(1−LAM_PE)`, `z₀⁺ = z₀⁺,ini·(1−LLI)/(1−LAM_PE)` (식 16) |
| **전하량 기반** `U_OCV(Q̂)` (Ah 축, 완방 기준) | `Q̂^Li_max`, `Q̂⁻_max`, `Q̂⁺_max` (또는 `r_N/P, z₀⁺, Q̂⁺_max`) | **3** | LLI, LAM_NE, LAM_PE 와 식 (15) 로 1:1 |
| **부분 곡선** + 시작전압 `U_ini` 미지 | 위 3개 + `z⁻_ini` | **4** | — |

`[인쇄, p.3]` "the SOC-based OCV 𝑈_OCV(𝑧) **only depends on two independent
dimensionless parameters** of Li/P and N/P ratio."

**"minimally and intuitively parametrized" 가 정확히 줄인 것**: 반쪽전지 OCP 자체는
전혀 매개화하지 않는다 (측정된 `U±_OCP(z±)` 를 **불변으로 가정**하고 그대로 쓴다).
줄인 것은 **두 OCP 를 붙이는 방식**이다.

- **줄이기 전 (Birkl 2017, 식 3)**: 네 개의 전극 SOC 한계
  `z⁺_max, z⁺_min, z⁻_max, z⁻_min` + 컷오프 전압 **제약 2개**.
- **줄이기 전 (Mohtat 2019, 식 4)**: `z⁺_min, z⁻_max, Q̂⁺_max, Q̂⁻_max` **4개**
  + 제약 `U⁺(z⁺_min) − U⁻(z⁻_max) = U_max` **1개**.
- **줄인 뒤 (이 논문, 식 7·9)**: `z⁺(z⁻) = z₀⁺ − r_N/P·z⁻` 라는 **직선 하나의
  기울기와 절편**. 제약 **0개**, 컷오프 전압 **무관**, pristine 값 **무관**.

`[인쇄, p.2]` 줄인 이유: "the parametrization (3) or (4) based on electrode SOC at
a certain cutoff voltage involves **non-independent parameters, of which the
redundancy complicates their estimation**. Moreover, the cutoff voltage is an
operational parameter that is not intrinsic to the aging state of a cell, so a
parametrization that depends on it **blurs the intrinsic degradation trend**."

`[인쇄, p.2]` 그리고 **우리 축(퍼센트)을 쓰지 말라고 명시적으로 말한다**:
"We also argue **not to parametrize the OCV by the LLI, LAMn and LAMp
percentage**, as these quantities rely on specifying the pristine-cell SOH
parameters, which are **irrelevant to the current SOH and could be arbitrary**.
Instead, these percentage losses **should be defined in terms of the SOH
parameters … and only calculated as derived quantities** when needed and
available."

### Q3. degeneracy 를 발견했는가

**어휘로는 0회. 그러나 실질적으로 두 종류를 모두 인쇄한다 — 하나는 구조적
축퇴이고, 하나는 국소 flat valley 다.**

#### (a) 구조적 축퇴 — 닫힌 형태로 인쇄돼 있다 (§2.3, p.7)

`[인쇄, p.7]` "the shape of an OCV curve, or the SOC-based OCV, is **only governed
by two degrees of freedom**, i.e., the N/P and Li/P ratio. The issue here is that
a certain ratio LLI ∶ LAM⁻ ∶ LAM⁺ **does not correspond to a unique shape of
OCV**, which gives the **false impression that the OCV variation has more than two
degrees of freedom**. Indeed, it is the ratio (1−LLI) ∶ (1−LAM⁻) ∶ (1−LAM⁺) …
which will **uniquely determine** the OCV shape."

`[해석]` 이 문장은 **우리 프로젝트가 재려는 축퇴를 닫힌 형태로 예측한 것**이다.
식 (16) 을 그대로 읽으면 다음이 나온다 — 세 모드의 **1 마이너스 값이 공통 인자
`c` 로 스케일되는 방향**은 SOC 기반 OCV 곡선을 **정확히 불변**으로 둔다:

```
(1−LLI, 1−LAM_NE, 1−LAM_PE)  →  c·(1−LLI, 1−LAM_NE, 1−LAM_PE)
   ⟹  r_N/P 불변,  z₀⁺ 불변  ⟹  U_OCV(z) 완전 동일
```

pristine (`r_ini = z₀,ini = 1`) 에서 출발하면 이 방향은 특히 단순해진다:

> **LLI = LAM_PE = LAM_NE = x 인 모든 x 에 대해, SOC 정규화 full-cell OCV 곡선은
> pristine 곡선과 글자 그대로 같다.** 달라지는 것은 총용량 `Q̂max` 하나뿐이다
> (배율 `1−x`).

이것은 노이즈·최적화와 무관한 **모델 자체의 성질**이므로 국소가 아니라 전역이며,
[[dubarry-mechanistic-mode-synthesis]] 에서 확인한 "2012년 식 (5)+(8') 안에 이미
들어 있던 축퇴" 와 같은 계보의, 그러나 **더 일반적인** 형태다.

**하지만 저자들은 이것을 축퇴라고 부르지 않는다.** 이 문단의 목적은 "논문들이
LLI/LAM 퍼센트 세 개를 스윕하는 것은 **중복(redundancy)** 이니 그러지 말라" 는
**표기법 권고**다. `[인쇄, p.7]` "this has the caveat of **redundancy**".
`[해석]` 같은 사실을 "추정 문제의 축퇴" 로 읽는 문장은 논문에 **없다**.

#### (b) 국소 flat valley — 그림에 있고 본문이 이름을 붙이지 않는다

`[도표]` **Fig. 2(b) (LFP, p.6, 직접 봄)**: `‖U_OCV(z; r,z₀) − U_OCV(z; 1,1)‖`
지도의 MaxE·RMSE 패널에 **Li/P ≈ 1.0 을 따라 N/P 0.7→1.5 전 구간을 가로지르는
거의 흰(≈0) 수평 능선**이 있다. 즉 **LFP 에서는 N/P 를 0.7 에서 1.5 로 두 배 넘게
바꿔도 전체 OCV 곡선이 사실상 같다.** 이것이 우리가 [[fitting-degeneracy]] 에서
flat valley 라 부르는 것의 교과서적 그림이며, **논문은 이것을 "sensitivity" 라고만
부른다.**

`[도표]` **Fig. 5(b) (LFP, p.11, 직접 봄)**: `N/P = 0.6, 0.8, 1.0, 1.2, 1.4` 다섯
곡선이 SOC 축에서 **육안으로 거의 겹친다**. 같은 다섯을 `z⁻` 축에 그린 5(a) 에서는
끝점이 0.6→1.0 으로 확연히 갈린다 — **정규화가 정보를 지운다**는 것을 한 쌍의
그림이 보여 준다.

`[도표]` **Fig. 1(d) (LFP, p.5, 직접 봄)**: `(N/P, Li/P)` = (1,1), (1,1.2),
(1.4,1.2), (0.7,0.8), (1,0.8) 다섯 셀의 SOC 기반 OCV 가 **거의 구별되지 않는다**.
`[인쇄, p.4]` 저자들도 "The **flatness** of the LFP and MCMB OCP makes the
variation in 𝑈_OCV(𝑧) rather **mild visually**" 라고 적는다.

#### (c) 어느 조건에서 갈리고 어느 조건에서 안 갈리는가 (표)

논문이 제시하는 갈림 조건은 **네 축**이다: ① 화학, ② `(r_N/P, z₀⁺)` 이 속한
4-regime, ③ SOC 창, ④ 어느 파라미터인가. 노이즈는 5 mV 고정, C-rate·온도는
**변수가 아니다**(25 °C 고정, 전류 없음).

**표 A — 화학 (가장 큰 효과)**

| | LFP/MCMB | NMC111/MCMB |
|---|---|---|
| `[인쇄, p.5]` 전체 곡선 변동폭 (`z`=20~80 %) | **60–100 mV** | **200–400 mV** |
| `[도표]` Fig. 8 어두운(=식별 가능) 면적 | 좁다. 판넬에 따라 거의 전무 | 넓다. (g),(h) 는 거의 전면 |
| `[인쇄, p.15]` | "the SOH parameter identifiability is **significantly higher for NMC than for LFP**" | |
| `[인쇄, p.17]` | "the active material of **LFP tends to be hard to identify**, likely due to the **flatness and lack of features in its OCP**. In contrast, the active material of **NMC is much more identifiable**." | |
| `[인쇄, p.17]` 흑연 | "the identifiability of **graphite shares a rather similar pattern** whether it is matched with LFP or NMC" | |
| `[도표]` Fig. 3(c),(d) PE DV fraction `λ⁺` | 0 과 1 사이를 **구형파처럼** 왕복 (0.00 과 1.00 에 포화하는 구간이 여럿) | **0.4 아래로 내려가지 않는다** — PE 가 항상 최소 40 % 기여 |

**표 B — 4-regime (`Li/P` 와 `Li/N` 의 1 대비 위치)**. 이것이 논문 Highlight 4다.
아래는 `[인쇄]` Table 4 (이상적 총용량) + Table 5 (컷오프 기반 총용량 감도) 를
합친 것이다.

| regime | 조건 | 이상 총용량 `Q_max` | `∂Q̂max/∂Q̂^Li` | `∂Q̂max/∂Q̂⁻` | `∂Q̂max/∂Q̂⁺` | Fig.8·9 의 대응 패널 |
|---|---|---|---|---|---|---|
| **Ⅰ Li 과잉** | Li > N, Li > P | `N + P − Li` | **→ −1** | → 1 | → 1 | (a),(e): `r=1, z₀=1.2` |
| **Ⅱ NE 과잉** | N > Li > P | `P` | → 0 | → 0 | → 1 | (b),(f): `r=1.4, z₀=1.2` |
| **Ⅲ PE 과잉** | P > Li > N | `N` | → 0 | → 1 | → 0 | (c),(g): `r=0.7, z₀=0.8` |
| **Ⅳ Li 부족 (전형)** | Li < N, Li < P | `Li` | **→ 1** | → 0 | → 0 | (d),(h): `r=1, z₀=0.8` |

`[인쇄, p.13, Table 5 본문]` 규칙: "The **Li/N ratio** determines whether the
end-of-charge is limited by NE filling up or PE being emptied, and `Q̂⁻_max` is
highly identifiable when NE is limiting end-of-charge. Likewise, the **Li/P
ratio** determines whether the end-of-discharge is limited by PE filling up or NE
being emptied, and `Q̂⁺_max` is highly identifiable when PE is limiting
end-of-discharge. In contrast, `Q̂^Li_max` is highly identifiable when the two
ratio are **both larger or smaller than 1**."

`[인쇄, p.13]` regime Ⅰ 의 반직관적 결과에 저자들이 문단을 할애한다: "**loss of
lithium inventory in such scenarios will boost the total capacity**" — Li⁺ 가 너무
많으면 움직일 자리가 없어 양 전극이 쉽게 다 차기 때문. 다만 `[인쇄]` "a normal
cell **rarely falls into this regime**" (사전리튬화한 셀에서만).

**표 C — SOC 창 (Fig. 8·9, σ_U = 5 mV 고정). 전부 `[도표]` 직접 판독**

Fig. 8 은 2-파라미터(`r_N/P`, `z₀⁺`) 표준오차, 컬러바 `[0, 0.2]`, 어두울수록 좋다.
`[인쇄, p.15]` 판정선: "a standard error larger than **0.2** … means the estimation
is almost useless" / "an estimation error of under **0.01** in this ideal setup as
more than enough".

| 패널 | 셀 | `r_N/P` 가 갈리는 창 | `z₀⁺` 가 갈리는 창 |
|---|---|---|---|
| (a) LFP Ⅰ | `r=1, z₀=1.2` | 하한 SOC ≲ 12 % **필수**, 상한 ≳ 20 % | 하한 ≲ 25 %, 상한 ≳ 30 % |
| (b) LFP Ⅱ | `r=1.4, z₀=1.2` | 하한 ≲ 10 %, 상한 ≳ 55 % (중간창은 밝다) | 하한 ≲ 20 %, 상한 ≳ 45 % |
| (c) LFP Ⅲ | `r=0.7, z₀=0.8` | **거의 전면 밝음** — 하한 ≲ 25 % **이면서** 상한 ≳ 85 % 인 좁은 모서리만 어둡다 | 같은 모서리만 |
| (d) LFP Ⅳ **(전형)** | `r=1, z₀=0.8` | 하한 ≲ 45 %, 상한 ≳ 55 % 에서 어둡다 (넷 중 가장 낫다) | 하한 ≲ 50 %, 상한 ≳ 40 % |
| (e)(f) NMC Ⅰ,Ⅱ | | 하한 ≲ 50 % 면 대체로 어둡다 | 같음, (f) 는 하한 ≲ 25 % 로 더 빡빡 |
| (g)(h) NMC Ⅲ,Ⅳ | | **거의 전면 어둡다** (대각선 근방 얇은 띠만 밝음) | 같음 |

`[인쇄, p.15]` 저자들이 명시하는 규칙성 세 가지:
- "the estimation error is **monotonically decreasing vertically and increasing
  horizontally**" (창이 포함관계면 넓은 쪽이 항상 낫다)
- "we see the errors having a **sharp change in certain SOC**" — 정보가 좁은
  SOC 대역에 몰려 있다
- "**estimating 𝑟_N/P is harder than estimating 𝑧₀⁺** in most cases here" 그리고
  "**OCV values at lower SOC are overall more informative** than those at high SOC"

Fig. 9 는 3-파라미터(`Q̂^Li`, `Q̂⁻`, `Q̂⁺`) 표준오차 (mAh), 컬러바 `[0, 100]`,
참값은 700–1400 mAh. `[도표]` 직접 판독:

| 패널 | 셀 | `Q̂^Li` (LLI) | `Q̂⁻` (LAM_NE) | `Q̂⁺` (LAM_PE) |
|---|---|---|---|---|
| (a) LFP Ⅰ | `r=1,z₀=1.2` | **전면 밝음 = 불가** | 하한 ≲ 25 %, 상한 ≳ 55 % 에서 가능 | 하한 ≲ 10 % 좁은 띠만 |
| (c) LFP Ⅲ | `r=0.7,z₀=0.8` | **전면 밝음 = 불가** | 넓게 어둡다 (유일하게 가능) | **전면 밝음 = 불가** |
| (d) LFP Ⅳ **(전형)** | `r=1,z₀=0.8` | 상한 ≳ 90 % 인 얇은 띠만 | 하한 ≲ 35 %, 상한 ≳ 75 % | 상한 ≳ 90 % 얇은 띠만 |
| (e)–(h) NMC | | 셋 다 상당한 어두운 영역 | 같음 | (h) 에서 가장 넓다 |

`[해석]` **표 C 의 두 표를 겹쳐 읽으면 이 논문의 실질 결론이 나온다**:
"LFP‖graphite 셀에서 full-cell OCV 만으로 LLI·LAM_PE·LAM_NE 세 개를 동시에 가르는
것은, 이상적 5 mV 노이즈·완전한 모델·국소 선형화라는 최상의 조건에서도, 대부분의
SOC 창과 대부분의 regime 에서 **불가능하다**."
논문은 이 문장을 쓰지 않는다.

### Q4. truth 를 무엇으로 삼았는가

**실측이 전혀 없다. 100 % 해석적 계산 + 결정론적 시뮬레이션이다.**

| 항목 | 이 논문 | 우리 `degradation-degeneracy` |
|---|---|---|
| 정방향 모델 | `U_OCV = U⁺_OCP(z⁺) − U⁻_OCP(z⁻)` — **순수 열역학**, 전류·확산·저항 없음 | **PyBaMM DFN**, `Chen2020_composite`, 유한 전류 |
| OCP 출처 | `[인쇄]` Plett 교재 [4, sec. 3.11.1] 의 LFP·NMC111·MCMB 적합식, 25 °C | PyBaMM 파라미터셋의 OCP, 방전 시뮬레이션에서 산출 |
| 화학 | LFP‖MCMB, NMC111‖MCMB (**두 개**) | NMC811‖(Graphite + Si) **복합 음극 2상** |
| 전극 컷오프 (Table 1) | MCMB 1.5/0.0 V · LFP 4.0/2.5 V · NMC111 4.4/2.8 V | — |
| 셀 컷오프 (Table 2) | LFP/MCMB 3.6/2.0 V · NMC/MCMB 4.2/2.8 V | 4.2 / 2.5 V |
| 노이즈 | **가정만** (σ_U = 5 mV, 등분산·독립·불편) | 실제 난수 노이즈 층 |
| truth 격자 | `(r_N/P, z₀⁺)` **4점** (Fig. 8·9) + 연속 지도 (Fig. 2·4·7) | 모드 3축 격자 |
| 검증 방식 | **CRLB (하한)** — 추정기를 안 돌린다 | 실제 NLS 복원 오차 + multi-start |
| inverse crime | 해당 없음 (추정을 안 하므로) | 생성=적합 모델. 별도로 관리 |

`[인쇄, p.4]` "perform simulations coded in Python to concretely illustrate our
results" — 코드도 데이터도 공개되지 않았다 (`[인쇄]` "Data will be made available
on request").

`[해석]` **가장 큰 차이는 "동역학의 유무" 가 아니라 "추정기를 돌렸는가" 다.**
Lin & Khoo 는 문제의 **하한**을 계산했고 우리는 절차의 **실측 성능**을 잰다.
그리고 논문이 §3 첫 문단에서 우리 방식의 약점을 정확히 지목한다:

`[인쇄, p.13]` "A straightforward approach is to devise an estimator and calibrate
the estimation error by feeding measurements coming from a known ground truth
**[3,19]**. The drawback of this approach is that it **entangles the
identifiability intrinsic to the problem with the error incurred by the estimator
itself**. If real data are used, the imperfectness of the model used will further
complicate the apparent identifiability."

여기 `[3]` 이 **Birkl 2017** ([[birkl-ocv-degradation-diagnostic]]) 이고 `[19]` 가
Dubarry 2017 이다. 우리 파이프라인은 정확히 그 계열이다.
`[해석]` **다만 우리 프로젝트는 이 얽힘을 이미 알고 설계했다** — flat valley 대
multimodal 의 구분([[fitting-degeneracy]])이 바로 "문제 고유의 식별 불가능성" 과
"추정기의 오차" 를 갈라내려는 장치이고, 무작위 restart 끼리만 비교하는 multi-start
진단이 그 실행이다. Lin & Khoo 는 이 얽힘을 **회피**했고 우리는 **분해**하려 한다.
서로의 결함을 정확히 메우는 관계다.

### Q5. 우리가 채택할 것과 반증해야 할 것

§14 에 전부 적었다. 요지만:

- **채택 (즉시)**: (1) `(r_N/P, z₀⁺)` 재매개화 — 우리 α·β 4개보다 자유도가 적고
  컷오프 무관. (2) `C_θ` 의 **비대각**을 보는 것 (논문이 버린 G1). (3) SOC 창을
  2차원 격자(`z_lower × z_upper`)로 스캔하는 표현 방식.
- **반증해야 할 것**: 논문의 4-regime 표는 **총용량 감도**에 대한 것이지 곡선
  형상에 대한 것이 아니다. 이것을 "식별 가능성 지도" 로 일반화해 읽으면 안 된다
  (§9.3).
- **직접 충돌**: 없다. 그러나 **정면으로 겹치는 주장이 하나** 있다 — §15.

---

## 3. 어휘 전수 (이 계보 열 편째) ★

합자 정규화(`ﬁ`→`fi`, `ﬂ`→`fl`) 후 **본문 1–18쪽 중 참고문헌 목록 앞까지**
(77,217자) 를 센 것. 참고문헌 목록은 따로 셌다.

| 패턴 | 본문 | 참고문헌 | 비고 |
|---|---:|---:|---|
| `identifiab*` | **26** | 1 | **이 계보 열 편 중 처음으로 0이 아니다** |
| `sensitivit*` | 46 | 0 | 논문의 주 도구 |
| `Fisher` | 12 | 1 | |
| `LAM` | 33 | 1 | |
| `LLI` | 22 | 2 | |
| `local` | 6 | 0 | 전부 "국소적으로만 유효" 라는 한정 |
| `global` | 2 | 0 | 둘 다 **"우리는 안 했다"** 는 문장 |
| `error covariance` | 4 | 0 | |
| `correlat*` | 6 | 0 | **전부 물리량 간 부호 상관** — 파라미터 상관은 **0회** |
| `uniqu*` | 4 | 0 | 아래 §3.1 |
| `ambigu*` | 3 | 0 | 아래 §3.2 |
| `redundan*` | 2 | 0 | 아래 §3.3 |
| `Cramér` | 1 | 0 | CRLB 인용 1회 |
| `Bayes*` | 1 | 0 | "우리는 안 했다" |
| `calibrat*` | 1 | 0 | 타 방법(우리 방법) 기각 문맥 |
| `uncertaint*` | 1 | 0 | 측정 불확실성 언급 1회 |
| `misconcep*` | 1 | 0 | |
| `PyBaMM` | 1 | 1 | |
| **`degenerac*` / `degenerat*`** | **0** | 0 | |
| **`non-unique` / `nonunique`** | **0** | 0 | |
| **`collinear*`** | **0** | 0 | |
| **`confound*`** | **0** | 0 | |
| **`ill-posed`** | **0** | 0 | |
| **`nullspace` / `null space`** | **0** | 0 | |
| **`noise`** | **0** | 0 | ★ σ_U 를 "standard error" 로만 부른다 |
| **`error bar` / `confidence interval`** | **0** | 0 | |
| **`cross-valid*`** | **0** | 0 | |
| **`Hessian`** | **0** | 0 | |
| **`singular value` / `condition number`** | **0** | 0 | |
| **`profile likelihood`** | **0** | 0 | |
| **`observab*` / `estimab*`** | **0** | 1 | 참고문헌 [11] 제목 안 ("estimability") |
| **`half-cell`** | 0 (`half cell` 1) | 1 | |

`[해석]` **이 표가 이 흡수의 가장 중요한 산출물 중 하나다.** 앞 아홉 편에서
`identifiab*` 는 본문 서술 기준 **전부 0회**였고, 유일한 예외인 Rhyu 2025 의 1회도
**참고문헌 제목 안**(그것이 바로 이 논문이다)이었다. 열 편째에서 **26회**가 나온
것이므로 "연속 0회" 는 형식·실질 모두 깨졌다.

**그러나 깨진 방식이 중요하다**: 26회 전부가 `identifiab*` 계열이고,
`degenerac*`·`non-unique`·`collinear*`·`ill-posed`·`nullspace` 는 **여전히 0회**다.
즉 이 저자들은 **"파라미터를 얼마나 정확히 잴 수 있나"(추정 정밀도)** 의 어휘는
갖추었지만 **"서로 다른 파라미터 조합이 같은 관측을 내는가"(비유일성)** 의 어휘는
쓰지 않는다. §2.3 에서 그 비유일성을 **닫힌 형태로 인쇄해 놓고도** 그것을
"redundancy" 라고 부른다 (§3.3). `[해석]` 개념이 없는 것이 아니라 **문제로 보지
않는다** — Zhang 2020 에서 관찰한 "자기 쪽으로 돌리지 않는다" 의 변주이되, 이번에는
자기 쪽으로 **절반만** 돌렸다.

### 3.1 `uniqu*` 4회 — 전부 "유일하게 결정된다" 는 **긍정** 진술

1. `[인쇄, p.7]` "the initial electrode SOC 𝑧±_ini are **uniquely determined** by
   𝑈_ini and any three-SOH-parameter tuple above"
2. `[인쇄, p.7]` "a certain ratio LLI ∶ LAM⁻ ∶ LAM⁺ **does not correspond to a
   unique shape of OCV**" ← **유일하게 부정형이며, 우리 축의 축퇴다**
3. `[인쇄, p.7]` "it is the ratio (1−LLI) ∶ (1−LAM⁻) ∶ (1−LAM⁺) … which will
   **uniquely determine** the OCV shape"
4. `[인쇄, p.7]` "the same N/P and Li/P ratio will still **uniquely determine**
   𝑈_OCV(𝑧)"

`[해석]` 2번이 이 논문 전체에서 **비유일성을 말하는 유일한 문장**이고, 그 문장이
가리키는 대상이 정확히 **우리의 (LLI, LAM_PE, LAM_NE) 좌표**다.

### 3.2 `ambigu*` 3회 — 축퇴가 아니라 **표기법의 모호성**

전부 "무엇을 고정한 편미분인지 밝히지 않으면 애매하다" 는 뜻이다:
`[인쇄, p.9]` "A partial derivative with respect to a particular parameter 𝛼
itself is **ambiguous**, because it also depends on the complete
parametrization." (Birkl/Dubarry 의 `ambigu` 3회가 **축퇴 논의**였던 것과 대비된다
— [[dubarry-mechanistic-mode-synthesis]].)

### 3.3 `redundan*` 2회 — 이 논문이 축퇴를 부르는 이름

1. `[인쇄, p.2]` "(3) or (4) … involves non-independent parameters, of which the
   **redundancy** complicates their estimation"
2. `[인쇄, p.7]` "parametric study of an OCV model by varying the above three loss
   percentages … has the caveat of **redundancy**"

---

## 4. §1 Introduction — 이 논문이 정리한 계보와 우리 좌표

### 4.1 저자들이 먼저 세운 구분 (우리에게 직접 걸린다)

`[인쇄, p.2]` **총용량 `Q̂max` 과 충·방전 용량은 다르다**:
"under finite-current operation, the observed terminal voltage shall reach a
cutoff voltage before the underlying OCV does due to polarization in
non-equilibrium, so the commonly reported charge/discharge capacity during
cycling **can be significantly smaller than the total capacity**, unless both
charging and discharging have a trailing CV (constant-voltage) phase with a small
enough cutoff current. … The total capacity depends **only on the thermodynamic
properties** of the cell, while the charge/discharge capacity **also depends on
the kinetic characteristics and operation protocols**. … It is not uncommon to see
a charge/discharge capacity being **confused** with the total capacity in
literature, but the distinction is important for the various modes of capacity
fade."

`[해석]` **이것은 우리 파이프라인에 대한 점검 항목이다.** 우리는 모드 역환산에
`r = Q_degraded/Q_reference` 를 쓴다 (`src/fitting.py` 헤더, `src/inventory.py`).
그 `r` 이 **총용량 비**인지 **어떤 프로토콜의 방전용량 비**인지에 따라 Lin 의
식 (16)·(47) 과의 대응이 달라진다. 우리 `configs/base.yaml` 의 완방 프로토콜은
`Discharge at 0.05C until 2.5V` 뒤에 `Discharge at 2.5 V until 0.02 C` 라는 **CV
꼬리를 포함**하므로 Lin 이 요구한 조건을 형식적으로는 만족한다 —
`[해석]` 그러나 **확인한 적은 없다.** 값싼 점검 항목으로 §14 에 올린다.

### 4.2 계보 정리 (논문이 인용한 순서 그대로)

| 세대 | 매개화 | 자유도 | 이 위키의 페이지 |
|---|---|---|---|
| Dubarry 2012 [8] (식 2) | `U_OCV(z⁻) = U⁺(1−(b_OFS + a_LR z⁻)) − U⁻(z⁻)` | **2** (`a_LR`, `b_OFS`) | [[dubarry-mechanistic-mode-synthesis]] |
| Birkl 2017 [3] (식 3) | 전극 SOC 한계 4개 + 컷오프 제약 2개 | **3** (실질) | [[birkl-ocv-degradation-diagnostic]] |
| Mohtat 2019 [11] (식 4) | `z⁺_min, z⁻_max, Q̂±_max` + 컷오프 제약 1개 | **4→3** | — |
| **Lin & Khoo 2024 (식 7·9·14)** | `r_N/P`, `z₀⁺` (+ `Q̂⁺_max`) | **2 (+1)** | 이 문서 |
| 우리 창 모델 | `α_PE, β_PE, α_NE, β_NE` | **4** | [[fitting-degeneracy]] |

`[인쇄, p.4]` 대응 관계가 명시된다: "our N/P ratio 𝑟_N/P and Li/P ratio 𝑧₀⁺
essentially correspond to the '**loading ratio**' and '**offset**' in (2) used in
[8,9] by `𝑟_N/P = 𝑎_LR` and `𝑧₀⁺ = 1 − 𝑏_OFS`."

`[해석]` 이것으로 [[22p-physics-or-degeneracy]] Status Log (3) 의 "자유도 계보"
표가 완성된다: Dubarry **2** → Birkl **3** → 우리 **4** 사이에 Lin & Khoo 가
**2 (+1)** 로 들어가고, 그들은 **2 가 옳은 숫자이며 3 이상은 중복** 이라고
주장한다. 우리 4는 그 주장의 정반대편 끝에 있다.

`[인쇄, p.2]` Mohtat 2019 에 대한 평가가 특히 중요하다: "They also derive the
gradient of 𝑈_OCV(𝑄_d) with respect to the four parameters and **use Fisher
information to quantify the parametric identifiability**. This OCV model **has
been incorporated in PyBaMM** [12] … and much subsequent work on model-based
degradation mode estimation has used different variants of this four-parameter
formulation [13,14]."
`[해석]` **즉 Fisher 로 이 문제의 식별 가능성을 잰 것은 Lin & Khoo 가 처음이
아니다** — Mohtat 2019 [11] 과 Lee 2020 [15] 가 먼저다. 이 논문의 기여는
"Fisher 를 처음 썼다" 가 아니라 "**제약이 없는 매개화로 옮겨서 Fisher 평가를 쉽게
만들었다**" 이다. `[인쇄, p.15]` "Due to the cutoff-voltage constraint between the
two electrode SOC limits in their parameters, **extra treatments are needed** to
evaluate the Fisher information matrix. The independent and cutoff-voltage-agnostic
parametrization introduced in this work allows this to be done with more ease."
→ **[11] Mohtat 2019 와 [15] Lee 2020 이 다음 흡수 후보다.**

### 4.3 저자들이 스스로 정한 범위 밖

`[인쇄, p.3]` "**this work is not related to DV analysis**" (DV fraction 이라는
이름을 쓰지만 DV/IC 분석 기법과는 별개라고 못 박는다).
`[인쇄, p.3]` "This work is **not about a more advanced estimation algorithm**, but
presents a more compact and intuitive parametrization that **can be substituted
into any such algorithm**."

---

## 5. §2.1 — 화학량론 `x±` 과 전극 SOC `z±` 의 구분

`[인쇄, p.3]` 핵심 주장: 활물질 질량을 모르면 `x±` 에 접근할 수 없고, 우리가 실제로
가진 것은 **사용 가능한 전위창 안의 Coulomb counting** 뿐이다. 그래서
`z± ∈ [0,1]` 을 그 창의 양 끝으로 정의하고 `Q̂±_max` 를 그 창의 전하량으로 쓴다.

식 (5): `Q̂±_max = (x±_max − x±_min)·Q±_max` — 이론 용량보다 훨씬 작을 수 있다.
식 (6): `z± = (x± − x±_min)/(x±_max − x±_min)`.

`[인쇄, p.3]` 저자들의 권고: "We advocate that researchers **do not use the term
stoichiometry and electrode SOC interchangeably** and should **report the upper and
lower cutoff potential** when presenting an OCP curve `U±_OCP(z±)`."
→ Table 1 이 그 실천이다 (MCMB 1.5/0.0 V · LFP 4.0/2.5 V · NMC111 4.4/2.8 V).

`[인쇄, p.3]` 부호 규약: "we define `Q±` and the electrode SOC `z±` to count
positively in the **lithiation** direction corresponding to a **cathodic** current.
We deviate from the convention in general electrochemistry …"
`[해석]` **부호 규약이 Dubarry [8] 과 반대다** — 논문 스스로 각주로 밝힌다
("There is also work that defines electrode SOC to be **negatively correlated**
with stoichiometry … [8]"). 우리 코드의 α·β 부호 규약을 이 논문과 대조할 때
반드시 확인해야 할 지점이다.

---

## 6. §2.2 — 두 파라미터 매개화 (이 논문의 뼈대)

전하 보존만으로 두 전극 SOC 가 **직선 하나**로 묶인다 — 식 (7):

```
z⁺(z⁻) = z₀⁺ − r_N/P · z⁻ ,     r_N/P = Q̂⁻_max/Q̂⁺_max ,  z₀⁺ = Q̂^Li_max/Q̂⁺_max
```

식 (8) 이 `z₀⁺` 의 물리적 의미를 준다: `z₀⁺ = (z⁺Q̂⁺_max + z⁻Q̂⁻_max)/Q̂⁺_max`
— 즉 **두 전극에 들어 있는 리튬 총량을 PE 용량으로 잰 것**.
`[인쇄, p.4]` "The lithium inventory `Q̂^Li_max` essentially accounts for the
lithium in **both electrodes** beyond `z± = 0`."

식 (9): `U_OCV(z⁻) = U⁺_OCP(z₀⁺ − r_N/P z⁻) − U⁻_OCP(z⁻)` — **컷오프 전압이 아직
등장하지 않았다.**

식 (10)–(11): 컷오프 `[U_min, U_max]` 를 넣어 `z⁻_min, z⁻_max` 를 **음함수**로 정의하고
`z = (z⁻ − z⁻_min)/(z⁻_max − z⁻_min)` 으로 셀 SOC 를 정의. 식 (12) 가 `U_OCV(z)`.

`[인쇄, p.4]` **핵심 문장**: "𝑧⁻(𝑧) and hence 𝑈_OCV(𝑧) are parametrized by 𝑟_N/P,
𝑧₀⁺, 𝑈_min, and 𝑈_max, where **given 𝑈_min and 𝑈_max fixed, 𝑈_OCV(𝑧) is thus again
parametrized by the independent and dimensionless 𝑟_N/P and 𝑧₀⁺ only**. This is the
main difference from the parametrization of (3) based on four electrode SOC limits
and two cutoff-voltage constraints [3]."

식 (13): `Q̂max = (z⁻_max − z⁻_min)Q̂⁻_max = (z⁺_max − z⁺_min)Q̂⁺_max`.
식 (14): `U_OCV(Q̂) = U⁺_OCP(z⁺_max − Q̂/Q̂⁺_max) − U⁻_OCP(z⁻_min + Q̂/Q̂⁻_max)`
— Mohtat 의 식 (4) 와 같은 형태이되 **컷오프 무관한 3개**로 매개화된다.

`[인쇄, p.7]` 부분 곡선의 경우: 시작전압 `U_ini` 를 신뢰하면 **여전히 3개**,
`U_ini` 도 불확실하면 **`z⁻_ini` 하나가 추가되어 4개**.

### 6.1 저자들이 명시하는 가정과 그 한계

`[인쇄, p.4]` "Assuming that the PE and NE OCP **remain unchanged upon
degradation** … One caveat … is that **crystal structural transformation** undergone
by certain active materials upon aging that might affect the electrode potential is
**not captured**. Besides, the form of electrode OCP used in this work has also not
accounted for **competing reactions** … of which the most prominent example is
**lithium plating** when `U⁻_OCP(z⁻)` reaches 0 V."

`[해석]` 우리 저장소가 2026-08-20 에 관측한 **"half-cell OCP 의 PE 쪽 전압 왜곡이
수 mV 수준에서 분해를 무너뜨린다"** ([[22p-physics-or-degeneracy]] Status Log
2026-08-20 (a)) 는 정확히 이 가정이 깨질 때의 크기를 잰 것이다. **Lin & Khoo 는 그
가정을 명시했고 우리는 그것을 깼을 때의 대가를 쟀다.** 두 결과는 붙는다.

---

## 7. §2.3 — LLI/LAM 퍼센트와의 환산, 그리고 2 자유도 정리 ★★

식 (15) — **우리 저장소의 정의와 글자 그대로 같다**:

```
LLI = 1 − Q̂^Li_max/Q̂^Li_max,ini
LAM⁻ = 1 − Q̂⁻_max/Q̂⁻_max,ini
LAM⁺ = 1 − Q̂⁺_max/Q̂⁺_max,ini
```

(`degradation-degeneracy/docs/07_LAM_LLI.md` §1·§2 의 `LLI = 1 − n_Li/n_Li,ini`,
`LAM_PE = 1 − C_PE/C_PE,ini` 와 동일한 형태. **좌표계가 일치한다.**)

식 (16) — 두 표현을 잇는 다리:

```
r_N/P = r_N/P,ini · (1 − LAM⁻)/(1 − LAM⁺)
z₀⁺   = z₀⁺,ini   · (1 − LLI)/(1 − LAM⁺)
```

`[인쇄, p.7]` 저자 주석: "as similarly shown by, for example, equation (5) and (8')
in [8] and equation (48–49) in [9]." → **[[dubarry-mechanistic-mode-synthesis]] 에서
우리가 이미 해체한 그 식들**이다.

### 7.1 ★ 이 논문이 인쇄한 축퇴 (닫힌 형태)

식 (16) 에서 곧바로 나오는 것 — `[해석]` 이하 유도는 우리가 쓴 것이지만 사용한
재료는 전부 `[인쇄]` 다:

> `U_OCV(z)` 는 `(r_N/P, z₀⁺)` 만의 함수이고, 식 (16) 은 그 둘이 세 모드의
> **비(比)** 에만 의존함을 말한다. 따라서 임의의 `c > 0` 에 대해
>
> ```
> (1−LLI, 1−LAM_NE, 1−LAM_PE)  →  c · (1−LLI, 1−LAM_NE, 1−LAM_PE)
> ```
>
> 는 `r_N/P` 와 `z₀⁺` 를 **동시에 불변**으로 두므로 **SOC 기반 full-cell OCV
> 곡선을 글자 그대로 동일하게** 만든다. 이 1-모수 족이 **정확한 null 방향**이다.

**pristine 에서 출발한 특수해 (가장 중요한 계): `LLI = LAM_PE = LAM_NE = x`**
— 모든 `x` 에 대해 SOC 정규화 OCV 곡선이 **pristine 과 완전히 같다.**
달라지는 것은 총용량뿐이며, 총용량은 정확히 `1−x` 배가 된다.
(`r_N/P,ini` 와 `z₀⁺,ini` 가 1이 아니어도 성립한다 — 비가 보존되기 때문.)

`[해석]` **이것이 이 흡수의 핵심 수확이다.** 세 가지 이유에서:

1. **우리가 수치로 찾던 flat 방향의 닫힌 형태다.** [[fitting-degeneracy]] 는
   "PE·NE 가 같은 부호로 묶이는 flat 방향" 을 관측하고 그 비율을 재려 했다. 위
   결과는 그 방향의 **정확한 좌표**를 준다 — PE·NE 뿐 아니라 **LLI 까지 포함하는
   3차원 방향**이다.
2. **격자에 직접 심어 시험할 수 있다.** [[dubarry-mechanistic-mode-synthesis]] 가
   준 `{LAM_liNE = x} ≡ {LAM_deNE = x, LLI = LR·x}` 와 같은 성격의, 그러나 우리
   축(de 전용 격자)에서 **바로 실현 가능한** 방향이다.
3. **22p 결과가 이 방향 근처에 있다.** [[22p-physics-or-degeneracy]] 가 추적하는
   세미나 22p 분해(LAM_PE ≈ LAM_NE ≈ 13 %, LLI ≈ 17 %)를 식 (16) 에 넣으면
   `r_N/P/r_ini = (1−0.13)/(1−0.13) = **1.000**`,
   `z₀⁺/z₀,ini = (1−0.17)/(1−0.13) = 0.83/0.87 = **0.954**` 다.
   `[해석]` 즉 **22p 의 세 숫자가 담고 있는 곡선 형상 정보는 실질적으로 "Li/P 가
   4.6 % 줄었다" 는 스칼라 하나이고, N/P 는 pristine 값에서 정확히 한 발짝도 움직이지
   않았다.** 세 개의 독립된 물리량처럼 읽히지만 형상 자유도로는 **한 개**다.
   (세미나가 보고한 값 자체의 정본은 [[22p-physics-or-degeneracy]] 이고, 우리
   파이프라인 수치의 정본은 artifact + `degradation-degeneracy/docs/RESULTS*.md` 다.
   여기서는 **환산만** 한다.)

**하지만 축퇴가 아닌 부분도 정확히 적어야 한다**: 총용량 `Q̂max` 은 이 방향을 따라
변하므로, **곡선 형상 + 측정된 총용량**을 함께 쓰면 세 모드가 원리적으로는 복원
가능하다 (형상 2 + 용량 1 = 3). 이 논문의 §3.2 (Fig. 9) 가 하는 것이 정확히
그것이다. 문제는 **원리적 가능성이 아니라 조건수**이며, Fig. 9 가 그것이 대부분의
조건에서 매우 나쁘다는 것을 보여 준다.

### 7.2 전극 컷오프 전위 선택의 임의성

`[인쇄, p.7]` 미묘한 지점 하나: LAM 퍼센트는 전극 컷오프 전위 선택에 **불변**이지만
(분모·분자가 같은 배율로 스케일), **LLI 는 그렇지 않다**:
"changing the **upper** cutoff potential will **alter the lithium inventory** but
changing the lower one will not … since this origin only affects `Q̂^Li_max` itself
but not its change, **LLI will also depend on this choice** of lithium origin."
그러나 `U_OCV(z)` 자체와 총용량은 영향을 받지 않는다.
`[해석]` **LLI 라는 숫자는 좌표 선택에 의존하는 양이다.** 서로 다른 논문의 LLI 값을
비교할 때 곧바로 문제가 된다. 우리 저장소의 `n_Li` 정의(양극+음극 리튬 총량)가 어느
"원점" 을 쓰는지 명시적으로 대조해 볼 항목이다.

---

## 8. §2.4 — 전극 DV fraction `λ±` (이 논문의 이름 붙인 기여)

식 (29):

```
λ⁺ = (r_N/P · dU⁺/dz⁺) / (r_N/P · dU⁺/dz⁺ + dU⁻/dz⁻)
   = (dU⁺/dQ̂⁺) / (dU⁺/dQ̂⁺ + dU⁻/dQ̂⁻)  ∈ [0,1] ,      λ⁻ = 1 − λ⁺
```

`[인쇄, p.8]` 의미: "the **fraction of the PE contribution to the full-cell
differential voltage**". 두 항이 모두 음수라 비가 [0,1] 에 갇힌다.

식 (30) 이 컷오프에서의 값 `λ⁺_l`(하한, `U_min`) 과 `λ⁺_u`(상한, `U_max`) 를 정의하고,
식 (31) 이 **모든 감도 gradient 의 공통 인자**로 그것을 넣는다:
`∂_α z⁻_min = (λ⁺_l/r_N/P)·∂_α z⁺(z⁻_min)`, `∂_α z⁻_max = (λ⁺_u/r_N/P)·∂_α z⁺(z⁻_max)`.

`[인쇄, p.8]` 왜 이것이 등장하는가에 대한 저자들의 한 줄: "the **sole reason** why
the electrode DV fractions play a role in our sensitivity analysis is the
**dependence of cell SOC 𝑧 and total capacity 𝑄̂max on the artificially specified
lower and upper cutoff voltage**."

물리적 해석 `[인쇄, p.8]`: `λ⁺_l ≈ 1` → 방전 종료가 **PE 가 리튬으로 차서** 일어남
(PE-limited discharging). `λ⁺_l ≈ 0` → NE 의 리튬 고갈로 일어남 (NE-limited).
`[인쇄, p.8]` 선행 문헌과의 대응: "the `λ` defined in [23] is just `λ⁺_l` here,
while their `ω` is essentially `(λ⁺_u − 1)`" (Rodrigues 2022, Si 음극의 SEI 성장률).

`[도표]` **Fig. 3 (p.9, 직접 봄)** — 화학 간 차이가 극적이다:
- **LFP/MCMB (3c)**: `λ⁺(z)` 가 **구형파**처럼 0 과 1 을 왕복한다. `λ⁺ = 1.00` 에
  포화하는 구간(z ≈ 0.40–0.46, 0.66–0.78, 0.83–0.93)과 `λ⁺ = 0.00` 에 포화하는
  구간(z ≈ 0.15–0.22, ~0.65, 0.79–0.83, ~0.93)이 번갈아 나온다. 즉 **어느 SOC 에서든
  한 전극이 DV 를 독점한다.**
- **NMC/MCMB (3d)**: `λ⁺(z)` 가 **0.4 아래로 내려가지 않는다** (최소 ≈ 0.39,
  최대 1.0). 즉 PE 가 어디서나 최소 40 % 를 기여한다.

`[해석]` **이것이 "NMC 가 LFP 보다 식별 가능한" 이유의 미시적 설명이다** — 논문은
이 연결을 명시적으로 쓰지 않는다. LFP 에서는 대부분의 SOC 에서 한 전극의 정보가
**정확히 0** 이므로, 그 SOC 의 측정은 그 전극에 대해 아무 말도 하지 않는다.

`[해석]` **PVS 와의 관계** ([[pvs-sev-degradation-mode-features]]):
`λ⁺` 는 `dU/dQ` 의 **전극별 분해 비율**이고, PVS 는 `dQ/dV` 곡선의 peak/valley
**진폭 비**다. 둘 다 "어느 전극이 이 SOC 를 지배하는가" 를 재려는 양이지만,
`λ⁺` 는 **반쪽전지 OCP 를 알아야 계산되고** PVS 는 full-cell 곡선만으로 계산된다.
즉 `λ⁺` 는 관측 가능한 feature 가 **아니다** — 모델의 내부량이다. 이 구분을 흐리면
안 된다.

---

## 9. §2.5–2.7 — 감도 gradient 와 네 regime

### 9.1 `U_OCV(z)` 의 감도 (§2.5)

식 (32): `∂_{r_N/P} z⁺(z⁻) = −z⁻`, `∂_{z₀⁺} z⁺(z⁻) = 1` (식 7 에서 자명).

식 (34)–(36) (N/P 에 대해), 식 (38)–(40) (Li/P 에 대해). 형태가 대칭적이다:

```
∂z⁻_min/∂r_N/P = −z⁻_min λ⁺_l / r_N/P     |   ∂z⁻_min/∂z₀⁺ = λ⁺_l / r_N/P
∂z⁻_max/∂r_N/P = −z⁻_max λ⁺_u / r_N/P     |   ∂z⁻_max/∂z₀⁺ = λ⁺_u / r_N/P
∂U_OCV(z)/∂α = (dU⁺/dz⁺)·∂z⁺(z)/∂α − (dU⁻/dz⁻)·∂z⁻(z)/∂α
```

`[인쇄, p.9]` "both `∂_{r_N/P} z±(z)` **vary linearly with 𝑧**, which is not
surprising since `z±(z)` have to remain linear by definition of 𝑧."

`[도표]` **Fig. 5 (LFP, p.11, 직접 봄)**:
- 5(c): `∂z⁻/∂r_N/P` 가 `z=0` 에서 0, `z=1` 에서 **≈ −0.88** 까지 선형 감소;
  `∂z⁺/∂r_N/P` 는 `z=1` 에서 ≈ −0.11. 즉 **N/P 는 완충 쪽 끝점만 움직인다.**
  `[인쇄, p.9]` 본문도 같은 말: "`z⁻_max` quickly decreases with increasing `r_N/P`,
  while `z⁻_min` is **insensitive** to `r_N/P` in this case".
- 5(d): `∂U_OCV/∂r_N/P` (녹색)가 **z ≈ 0.25–0.45 와 0.6–0.75 구간에서 사실상 0**
  이고, 최대 진폭 ±0.3 V 근방의 좁은 봉우리가 z ≈ 0.05·0.18·0.57·0.95 에만 있다.
  → **N/P 정보는 좁은 SOC 창에만 있다.** Fig. 8 의 "sharp change" 와 일치.

`[도표]` **Fig. 6 (LFP, p.12, 직접 봄)**:
- 6(c): `∂z⁻/∂z₀⁺` 는 z=0 에서 ≈ 0.32 → z=1 에서 ≈ 0.88 로 **증가**,
  `∂z⁺/∂z₀⁺` 는 0.68 → 0.11 로 감소. `[인쇄, p.9]` "the electrode SOC limits
  **always increase** with the lithium inventory".
- 6(d): `∂U_OCV/∂z₀⁺` (녹색)가 z ≲ 0.05 에서 **≈ −4 V** 까지 급락(PE 성분 `∂U⁺`
  는 **≈ −9.5 V**)하고, 그 밖의 거의 전 구간에서 ≈ 0, z ≈ 1 에서 다시 작은 극값.
  → **LFP 에서 Li/P 정보는 SOC 바닥(z ≲ 10 %)에 거의 전부 몰려 있다.**
  Fig. 8 의 "OCV values at **lower SOC** are overall more informative" 와 일치.

### 9.2 총용량의 감도와 네 regime (§2.6–2.7)

식 (41) (dimensionless 매개화):
`∂Q̂max/∂r_N/P = (z⁻_max λ⁻_u − z⁻_min λ⁻_l)Q̂⁺_max`,
`∂Q̂max/∂z₀⁺ = (λ⁺_u − λ⁺_l)Q̂⁺_max`,
`∂Q̂max/∂Q̂⁺_max = (z⁻_max − z⁻_min)r_N/P`.

식 (47) (all-capacity 매개화) — **가장 쓸모 있는 형태**:

```
∂Q̂max/∂Q̂^Li_max = λ⁺_u − λ⁺_l
∂Q̂max/∂Q̂⁻_max   = z⁻_max λ⁻_u − z⁻_min λ⁻_l
∂Q̂max/∂Q̂⁺_max   = z⁺_max λ⁺_l − z⁺_min λ⁺_u
```

식 (48): 셋 다 `[−1, 1]` 에 갇힌다.
`[인쇄, p.13]` 해석: "`∂_{Q̂⁻_max} Q̂max` indicates the **fraction of NE capacity
change that indeed manifests in cell total capacity** … A derivative close to 1
implies the factor being **limiting**, while a value close to 0 hints the
opposite."

`[도표]` **Fig. 7(c) (LFP) 와 7(f) (NMC), p.14, 직접 봄**:
- `dQ/dQ^Li`: **짙은 파랑 (≈ −1)** 이 좌상단(`Li/P > 1` **이면서** `Li/N > 1`),
  **짙은 빨강 (≈ +1)** 이 그 반대 구석. 경계는 `Li/P = 1` 수평선과 `Li/N = 1`
  대각선이 (1,1) 에서 만나는 꺾인 선.
- `dQ/dQ⁻`: **짙은 빨강 (≈ +1)** 이 대각선 `Li/N = 1` 위쪽, 아래는 거의 흰색(≈0).
- `dQ/dQ⁺`: **짙은 빨강 (≈ +1)** 이 `Li/P ≈ 1` 수평선 위쪽, 아래는 흰색(≈0).
  (LFP 는 NMC 보다 훨씬 급격한 계단, NMC 는 넓은 전이 띠 — `[인쇄, p.9]` "The NMC
  case has a **more gradual transition** across these regimes than the LFP case.")
- NMC 의 `dQ/dQ⁺` 에는 **연한 파랑 (음수) 영역**이 `Li/P ≈ 0.65–0.95, N/P ≳ 0.9`
  에 있다 — `[인쇄, p.13]` 이 논문이 예고한 "negative derivative … loss of active
  materials … will, **counterintuitively, increase the total capacity**".

`[도표]` **Fig. 4 (p.10, 직접 봄)**: 같은 4-quadrant 구조가 `z⁻_min/max`, `z⁺_min/max`,
`λ⁺_l`, `λ⁺_u` 에 먼저 나타난다. LFP 의 `λ⁺_u` 는 대각선 `Li/N = 1` 을 경계로
**0 ↔ 1 이진 전환**, `λ⁺_l` 은 `Li/P ≈ 1.03` 수평선을 경계로 이진 전환. NMC 는 같은
경계지만 0.3–0.7 의 중간값 띠가 넓다.

### 9.3 ★ 표 4 캡션과 본문의 불일치 — 그리고 그것이 왜 중요한가

**같은 세 문장이 두 곳에 다른 강도로 인쇄돼 있다.**

| 위치 | 문구 |
|---|---|
| `[인쇄]` **Table 4 캡션 (p.13)** | "`Q̂⁻_max` is **only identifiable** when NE is limiting end-of-charge … `Q̂⁺_max` is **only identifiable** when PE is limiting end-of-discharge … `Q̂^Li_max` is **only identifiable** when the two ratio are both larger or smaller than 1" |
| `[인쇄]` **본문 §2.7 (p.13)** | (같은 문장) "… is **highly identifiable** …" ×3 |

`[해석]` **"only identifiable" 은 구조적 주장이고 "highly identifiable" 은 실용적
주장이다.** 둘은 강도가 전혀 다르며, 어느 쪽도 논문의 계산이 지지하지 않는다:

- 식 (47) 의 세 미분은 **총용량 `Q̂max` 이 그 파라미터에 얼마나 민감한가**만 말한다.
  파라미터가 **곡선 형상**을 통해 식별될 수 있다는 경로를 전혀 세지 않는다.
- 실제로 Fig. 9(c) (LFP, regime Ⅲ) 를 보면 `Q̂⁻` 는 표 5 예측대로 어둡지만
  (`∂Q̂max/∂Q̂⁻ → 1`), Fig. 9(d) (regime Ⅳ) 에서는 `∂Q̂max/∂Q̂⁻ → 0` 인데도 `Q̂⁻`
  가 넓게 어둡다 — **곡선 형상이 그 정보를 준 것이다.** 즉 표 5 는 Fig. 9 의
  충분조건도 필요조건도 아니다.

→ **이 표를 "식별 가능성 지도" 로 인용하면 안 된다.** 인용 가능한 형태는
"총용량의 각 SOH 파라미터에 대한 감도가 네 regime 으로 나뉜다" 까지다.
이것이 §2 Q5 의 "반증해야 할 것" 이다.

---

## 10. §3.1 — Fisher 로 본 `(r_N/P, z₀⁺)` 식별 가능성 (Fig. 8)

절차 `[인쇄, p.13–15]`:
1. 측정 `y_i = U_OCV(z_i)` at `z = 1 %, 2 %, …, 99 %`, 오차 독립 등분산 `σ_U = 5 mV`.
2. 가능한 모든 SOC 창 `[z_lower, z_upper]` (최소 2점 포함) 를 순회.
3. `∇_θ U_OCV(z_i) = [∂_{r_N/P}U, ∂_{z₀⁺}U]` 를 식 (36)·(40) 의 **해석식**으로 계산.
4. `C_θ⁻¹ = Σ_i (1/σ_U²)·∇^T f_i ∇f_i` (식 52) — rank-1 갱신의 합.
5. `sqrt(diag(C_θ))` 를 그린다.

식 (49)·(51): `C_θ⁻¹(θ₀) = ∇_θ^T f(θ₀) C_y⁻¹ ∇_θ f(θ₀) = F_y(θ*)` — Gaussian
가능도에서 가중 NLS 의 오차공분산이 Fisher 정보행렬과 일치한다는 표준 결과.
`[인쇄, p.15]` "the inverse Fisher information matrix is the **Cramér-Rao lower
bound** of the covariance of all **unbiased** estimator".

판독은 §2 Q3 표 C 에.

`[인쇄, p.15]` 저자들이 지적하는 구조: 창이 포함관계면 오차가 단조 — "the
estimation error is monotonically **decreasing vertically** and **increasing
horizontally**" (Fig. 8 의 삼각형 지도가 그래서 계단형 등고선을 갖는다).

---

## 11. §3.2 — Fisher 로 본 `(Q̂^Li, Q̂⁻, Q̂⁺)` 식별 가능성 (Fig. 9) ★

**여기가 우리 문제와 좌표가 정확히 일치하는 유일한 절이다.**

식 (54): 부분 곡선 `U_OCV(Q_c) = U⁺(z⁺_ini(z⁻_ini(U_ini)) − Q_c/Q̂⁺_max) −
U⁻(z⁻_ini(U_ini) + Q_c/Q̂⁻_max)`.
식 (55) 가 `(r_N/P, z₀⁺)` 미분을 `(Q̂^Li, Q̂⁻, Q̂⁺)` 미분으로 바꾸는 연쇄율.
식 (56)–(58) 이 세 감도의 닫힌 형태:

```
∂U_OCV(Q_c)/∂Q̂^Li = (λ⁻_ini/Q̂⁺_max)(dU⁺/dz⁺) − (λ⁺_ini/Q̂⁻_max)(dU⁻/dz⁻)
∂U_OCV(Q_c)/∂Q̂⁻   = −(z⁻_ini λ⁻_ini/Q̂⁺_max)(dU⁺/dz⁺) + ((z⁻_ini λ⁺_ini + Q_c/Q̂⁻_max)/Q̂⁻_max)(dU⁻/dz⁻)
∂U_OCV(Q_c)/∂Q̂⁺   = ((−z⁺_ini λ⁻_ini + Q_c/Q̂⁺_max)/Q̂⁺_max)(dU⁺/dz⁺) + (z⁺_ini λ⁺_ini/Q̂⁻_max)(dU⁻/dz⁻)
```

설정 `[인쇄, p.16]`: `ΔQ_c` = 참 총용량의 1 % (= 1 % SOC), `U_ini` = 각 정수 SOC
에서의 참 OCV, `Q̂⁺_max = 1 Ah` 고정, `σ_U = 5 mV`.

판독은 §2 Q3 표 C 하단. 새 구조 하나 `[인쇄, p.16]`: Fig. 8 과 달리 하한 SOC 축을
따라 **단조가 아니다** — "some **vertical downward pointing 'fingers'**". 이유는
"the voltage measurement at a particular cell SOC 𝑧 is **interpreted differently**
when the initial voltage changes, so it is **not really the same measurement**".

`[인쇄, p.17]` 화학별 결론: "the identifiability of the **active material amount**
in an electrode **strongly depends on the intrinsic OCP relation of this particular
material**. For example, the active material of **LFP tends to be hard to
identify**, likely due to the **flatness and lack of features in its OCP**. In
contrast, the active material of **NMC is much more identifiable**. Moreover, the
identifiability of **graphite shares a rather similar pattern** whether it is
matched with LFP or NMC."

---

## 12. §4 결론 — 저자들이 스스로 적은 한계 (전문)

`[인쇄, p.17]`:
> "We want to emphasize that any statements based on sensitivity gradients are
> **only valid locally**, i.e. valid for a small range of parameters around the
> point at which the gradients are evaluated. More empirical tools from statistical
> inference will be needed to discern **global sensitivity**, and we will report our
> findings in **future work**."

`[인쇄, p.17–18]`:
> "Another limitation is that we have only discussed inferring degradation modes
> from **OCV measurements**, which has a relatively restricted scope of application
> in practice. To go beyond OCV measurements, we need to somehow estimate the cell
> SOC and OCV from terminal voltage recorded in **finite-current operation**."

`[해석]` 두 한계 모두 **우리 파이프라인이 이미 커버하는 영역**이다 (전역 격자 스캔 ·
유한 전류 DFN). 반대로 우리가 못 하는 것(해석적 gradient·CRLB·창 최적화)을 이
논문이 한다. **상보 관계가 이보다 깨끗하기 어렵다.**

---

## 13. 그림 — 본 것과 안 본 것 (정직하게)

크로핑 결과: **fig 9장 + tab 5장 = 14장**
(`raw/figures/lin2024_ocv-degradation-mode-identifiability/`, `figures.json` 색인).

| 그림 | 쪽 | 봤나 | 이 digest 에서 쓴 곳 |
|---|---|---|---|
| Fig. 1 (모델 모식도 + OCV square + `U_OCV(z)`) | 5 | **봄** | §2 Q3(b) — 다섯 셀 곡선이 겹친다 |
| Fig. 2 (OCV 값 지도 + 오차 norm 지도) | 6 | **봄** | §2 Q3(b) — **LFP 의 flat valley 능선** |
| Fig. 3 (PE DV fraction) | 9 | **봄** | §8 — LFP 구형파 vs NMC 하한 0.4 |
| Fig. 4 (전극 SOC 한계 + `λ⁺_l/u` 의 4분면) | 10 | **봄** | §9.2 |
| Fig. 5 (N/P 감도) | 11 | **봄** | §9.1 — 다섯 곡선 겹침, `∂U/∂r` 의 영구간 |
| Fig. 6 (Li/P 감도) | 12 | **봄** | §9.1 — 정보가 SOC 바닥에 몰림 |
| Fig. 7 (`Q_c` 기반 OCV + `∂Q̂max/∂Q̂(·)` 4분면) | 14 | **봄** | §9.2 — 부호 구조, NMC 의 음수 영역 |
| Fig. 8 (`(r,z₀)` 표준오차, SOC 창 지도 8패널) | 16 | **봄** | §2 Q3 표 C, §10 |
| Fig. 9 (`(Q̂^Li,Q̂⁻,Q̂⁺)` 표준오차, 8패널) | 17 | **봄** | §2 Q3 표 C, §11 — **핵심** |
| Table 1·2 (전극/셀 컷오프) | 4 | 텍스트로 읽음 | §2 Q4 |
| Table 3 (이상적 전극 SOC 한계) | 10 | 텍스트로 읽음 | §9.2 |
| Table 4·5 (네 regime) | 13 | 텍스트로 읽음 | §2 Q3 표 B, §9.3 |

**본문 그림 9장 전부를 실제로 열어 봤다.** 표 5장은 PDF 텍스트가 정확하므로
이미지로 읽지 않았다 (도구의 권고에 따름).

**본문 서술과 어긋난 그림**: 없다. Fig. 5·6 의 "해석식과 수치가 일치한다" 는 주장은
그림에서 확인되고, Fig. 7(c)/(f) 의 부호 구조는 Table 5 의 극한값과 일치한다.
다만 §9.3 의 **캡션↔본문 문구 불일치**(only / highly)는 실재하며, 그림이 아니라
글자 사이의 불일치다.

**보지 않은 것**: Supporting Information 의 figure 1–3 (화학량론↔전극 SOC 모식도,
완충·완방 상태 모식도, 관습적 선그림 OCV 조립). SI PDF 가 이번 업로드에 없다.
본문이 그 셋을 "illustration" 으로만 인용하므로 결론에 영향은 없다고 판단했다.

---

## 14. 우리 프로젝트와의 접점 — 채택 / 점검 / 공급

### 14.1 즉시 채택할 것

| # | 무엇 | 왜 | 비용 |
|---|---|---|---|
| A1 | **`C_θ` 의 비대각을 본다.** Fisher 를 쓸 때 `sqrt(diag)` 만 그리지 말고 **상관계수 `ρ(r_N/P, z₀⁺)`** 와 **최소 고유값의 고유벡터**를 함께 낸다 | 논문이 계산해 놓고 버린 것(G1)이고, **축퇴의 방향**은 거기에만 있다 | 매우 낮음 — 이미 만든 행렬의 다른 성분 |
| A2 | **SOC 창을 `(z_lower × z_upper)` 2차원 삼각 지도로 표현**한다 | 우리 저장소는 "어느 창이 정보를 갖는가" 를 지도로 낸 적이 없다. 표현 방식만 빌려도 얻는 것이 크다 | 낮음 |
| A3 | **`(r_N/P, z₀⁺, Q̂⁺_max)` 좌표를 진단용 보조 좌표로 병기**한다 (α·β 를 버리자는 것이 아니다) | 우리 4개 파라미터가 이 3개(또는 형상만 보면 2개)로 사영될 때 **무엇이 사라지는지** 가 곧 축퇴의 크기다 | 낮음 — 식 (7) 대응만 쓰면 된다: `z₀⁺ ↔ (β_NE−β_PE)/α_PE`, `r_N/P ↔ α_NE/α_PE` `[해석]` |
| A4 | **null 방향 `LLI = LAM_PE = LAM_NE = x` 를 격자에 명시적으로 심는다** | §7.1. 수치로 찾던 flat 방향의 **닫힌 형태 예측**이므로 검증력이 다르다 | 낮음 — 기존 격자에 대각선 truth 쌍 추가 |
| A5 | **Fisher/CRLB 를 우리 복원 오차의 하한 기준선으로 병기** | 우리가 재는 복원 오차가 **문제 고유의 한계**인지 **추정기 탓**인지를 가르는 직접적 도구. 논문이 §3 서두에서 우리 방식의 약점으로 지목한 바로 그 얽힘(`[인쇄]` "entangles the identifiability intrinsic to the problem with the error incurred by the estimator") | 중간 |

### 14.2 점검할 것 (우리 쪽에 열린 질문)

| # | 점검 | 근거 |
|---|---|---|
| B1 | **우리 목적함수의 x축이 "각 셀 자기 용량 정규화" 다** (`src/fitting.py` 헤더). 그렇다면 pOCV 항은 Lin 의 `U_OCV(z)` 에 해당하고 **형상 자유도는 2개뿐**인데 우리는 **4개**를 맞춘다. 재구성이 양 끝 컷오프 전압을 (근사적으로) 맞추면 제약 2개가 소모되어 유효 자유도가 2로 떨어진다 — **Lin 이 Birkl/Mohtat 매개화를 비판한 바로 그 구조** | `[인쇄, p.2]` "non-independent parameters, of which the **redundancy** complicates their estimation" + `src/fitting.py` 정규화 규약. **`[해석]`, 미검증** |
| B2 | **dQ/dV 항을 더해도 개선이 없었던 것**([[22p-physics-or-degeneracy]] 2026-08-20)이 이 논문으로 설명되는가. `dQ/dV` 는 **같은 정규화 곡선의 함수**이므로 그 곡선이 가진 자유도를 늘릴 수 없다 — 가중치만 바꾼다. 국소 null 방향은 재가중에 **불변**이다 | `[해석]`. 논문은 이 말을 하지 않는다. 그러나 §7.1 의 2-자유도 진술로부터 따라온다. **수학적으로 확인 가능하고 값싸다** |
| B3 | **`r = Q_degraded/Q_reference` 가 총용량 비인가 방전용량 비인가** | §4.1. `[인쇄, p.2]` 의 구분. 우리 완방 프로토콜에 CV 꼬리가 있어 형식적으로는 총용량이지만 확인한 적이 없다 |
| B4 | **우리 셀의 regime 이 무엇인가.** `docs/07_LAM_LLI.md` 는 이 셀을 **NE-limited**(PE 총용량이 가용용량의 1.53배, NE 는 1.04배)로 기술한다. Lin 좌표로는 `Li < P` 쪽, 즉 regime Ⅱ 또는 Ⅳ → `λ⁺_l → 0` → **`∂Q̂max/∂Q̂⁺_max → 0`** | `[해석]` 두 문서의 대조. 아래 §14.3 참조 |
| B5 | **부호 규약 대조**: Lin 은 `z±` 를 **리튬화 방향 양수**로 잡고 Dubarry [8] 과 반대라고 명시한다. 우리 α·β 규약이 어느 쪽인지 | `[인쇄, p.3]` |
| B6 | **LLI 는 전극 상한 컷오프 전위 선택에 의존하는 양이다** (§7.2). 우리 `n_Li` 정의의 "원점" 확인 | `[인쇄, p.7]` |

### 14.3 ★ 우리 저장소의 경험적 결론과 이 논문의 해석식이 만나는 지점

`degradation-degeneracy/docs/07_LAM_LLI.md` 는 이렇게 적는다 (읽기만 함, 고치지 않음):

> "**음극 제한(NE-limited) 셀**이다. 양극은 1.5배 과설계라 여유가 크다.
> → 이것이 이 프로젝트의 핵심 난점이다. **양극 활물질이 조금 줄어도 전체 용량은
> 거의 안 변하므로, LAM_PE는 full-cell 곡선에 흔적을 거의 남기지 않는다.**"

Lin & Khoo 의 식 (47) 이 **이 문장의 일반 판정식**이다:

```
∂Q̂max/∂Q̂⁺_max = z⁺_max λ⁺_l − z⁺_min λ⁺_u        (식 47)
```

`λ⁺_l ≈ 0` (= 방전 종료가 NE 고갈로 결정됨 = NE-limited discharging) 이면 이
미분은 **0 으로 간다** — Table 5 의 `Li < P` 열이 정확히 그것이다.

`[해석]` **우리가 물리적 직관으로 도달한 결론을 이 논문이 닫힌 판정식으로 준다.**
그리고 그 판정식은 우리 직관이 놓친 것을 하나 더 준다 — **`λ⁺_l` 은 SOH 에 따라
움직이는 양이다** (Fig. 4). 즉 "LAM_PE 가 안 보인다" 는 이 셀의 고정된 성질이
아니라 **`(r_N/P, z₀⁺)` 가 어디 있느냐에 따라 켜지고 꺼지는 성질**이다. 열화가
진행되어 `Li/P` 가 1 을 넘어가면 (사전리튬화·과잉 리튬 상황) `λ⁺_l → 1` 이 되고
LAM_PE 가 갑자기 보이기 시작한다. **우리 격자 안에서 이 전환이 일어나는지**는
직접 계산할 수 있고, 아직 아무도 보지 않았다.

### 14.4 우리가 이 논문에 공급할 수 있는 것

| # | 공급 | 논문의 공백 |
|---|---|---|
| S1 | **전역 축퇴 스캔**. 저자들이 `[인쇄]` "future work" 로 미룬 것 (G5) 을 우리 격자 방법론이 그대로 할 수 있다 | G5 |
| S2 | **CRLB 가 실제로 달성되는가**. 저자들은 하한만 계산하고 추정기를 안 돌린다 (G2). 우리는 NLS + multi-start 를 돌린다. **하한 대비 실제 오차의 비**가 곧 "flat valley vs multimodal" 의 정량 지표가 된다 | G2 |
| S3 | **모델 오차의 크기**. 저자들이 `[인쇄]` "model errors will limit the estimation accuracy **in the first place**" 라고만 적고 넘어간 것 (G6) 을, 우리는 이미 mV 단위로 관측했다 | G6 |
| S4 | **노이즈 스윕**. σ_U 고정(G3·G4)을 우리 노이즈 층이 대체 | G3, G4 |
| S5 | **복합전극(Si/Gr)**. 저자들이 명시적으로 범위 밖에 둔 것(G8)이 우리 셀의 기본 구성이다 | G8 |
| S6 | **파라미터 상관 지도**. G1 은 저자들이 이미 가진 것을 안 그린 것이므로, 우리가 그리면 곧바로 새 산출이 된다 | G1 |

---

## 15. 비판 — 이 논문의 약한 곳

1. **★ 축퇴를 손에 쥐고도 축퇴로 부르지 않는다.** §2.3 의 2-자유도 문단은 우리
   좌표에 대한 **정확한 비유일성 진술**인데, 논문은 그것을 "논문 저자들이 퍼센트
   세 개를 스윕하는 나쁜 습관" 을 지적하는 **표기법 조언**으로 쓴다. 그 문단에서
   "그러므로 세 모드를 곡선 형상만으로 가르는 것은 불가능하다" 로 한 걸음 더
   나아가지 않는다. 어휘 전수(§3)가 이것을 뒷받침한다: `degenerac*` 0,
   `non-unique` 0.
2. **★ 오차공분산의 비대각을 계산해 놓고 버린다** (G1). 축퇴 연구 논문이 축퇴의
   **방향**을 안 그리는 것은 방법론적 손실이다. `ρ(r_N/P, z₀⁺)` 지도는 Fig. 8 을
   만든 코드에서 한 줄 더 쓰면 나온다.
3. **추정기를 한 번도 돌리지 않는다** (G2). §3 서두에서 "추정기를 쓰면 문제 고유의
   식별 가능성과 추정기 오차가 얽힌다" 며 남의 방식을 기각하는데, 그 대가로 **자기
   결과가 실제 추정에 얼마나 옮겨지는지**를 아무도 모른다. CRLB 는 **불편 추정량의
   하한**이고 저자 스스로 MLE 가 불편이 아니라고 적는다 (G10). 하한이 느슨하면
   Fig. 8·9 의 어두운 영역도 낙관적이다.
4. **σ_U = 5 mV 라는 단일 가정**이 모든 정량 결론(0.2 / 0.01 판정선 포함)을 떠받친다
   (G3·G4). 스윕이 자명하게 가능한데 하지 않았다.
5. **네 평가점 중 셋이 논문 스스로 "비전형" 이라 부른 셀이다** (G12). 실제 노화 셀이
   가는 방향(`Li/P` ↓, `Li/N` ↓ = regime Ⅳ)은 (d)/(h) 하나뿐인데, 여덟 패널이
   동등하게 나열되어 **가장 관련 있는 패널이 눈에 띄지 않는다.**
6. **Table 4 캡션의 "only identifiable"** (§9.3) — 총용량 감도에 대한 진술을
   식별 가능성 일반으로 확대하는 문구이며, 같은 문장의 본문판은 "highly" 로
   완화돼 있다. 인용자가 캡션을 인용하면 과장이 전파된다.
7. **재현 수단이 없다.** 코드·데이터 공개가 없고 (`[인쇄]` "Data will be made
   available on request") 순수 계산 논문인데 스크립트가 없다. Fig. 8·9 를 우리가
   재현하려면 처음부터 구현해야 한다 — 다만 식 (36)·(40)·(56)–(58) 이 전부
   인쇄돼 있어 **원리적으로는 재현 가능**하다.
8. **`Q̂max` 의 두 매개화 사이 trade-off 를 "discuss" 하겠다고 예고하고 (p.6 "We
   will discuss the trade-off between these two options") 실제로는 §2.7 끝의 두
   문장으로 끝낸다.** 큰 결함은 아니지만 예고와 이행의 불일치.

`[해석]` **그럼에도 이 논문은 이 계보 열 편 중 방법론적으로 가장 정직하다.**
자기 결과의 유효 범위(국소·이상조건·OCV 한정)를 세 곳에서 반복해 명시하고,
모르는 것을 "future work" 로 남긴다. 앞의 아홉 편 중 어느 것도 이렇게 하지 않았다.

---

## 16. 한 줄 결론

**"우리가 하려는 판정을 이 논문이 이미 했는가" 에 대한 답: 절반만, 그리고 다른
질문으로.** 이 논문은 (a) 우리 좌표의 **구조적 축퇴 한 방향을 닫힌 형태로 인쇄**
했고 (§7.1), (b) **국소·이상조건에서의 창별 CRLB 지도**를 만들었다 (Fig. 8·9).
그러나 (c) **추정기를 돌리지 않았고**, (d) **전역 축퇴를 명시적으로 미뤘으며**,
(e) **파라미터 상관을 계산해 놓고 그리지 않았고**, (f) `degenerac*` 를 **한 번도
쓰지 않는다**. 우리 프로젝트가 서 있는 자리는 정확히 (c)(d)(e) 다.
