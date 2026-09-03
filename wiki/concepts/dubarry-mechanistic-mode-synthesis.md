---
title: Dubarry 정방향 모드 합성 모델 (2012) — α·β 창 좌표계의 출처
description: "(LR, OFS) 창 파라미터화와 li/de 4분류 LAM 분류법의 출처는 Birkl 2017 이 아니라 여기다 — 우리 코드 주석의 인용 판정"
created: 2026-09-03
updated: 2026-09-03
type: concept
tags: [battery, degradation, research]
sources: [raw/papers/dubarry2012_synthesize-degradation-modes.md, raw/papers/birkl2017_degradation-diagnostics-ocv.md]
confidence: medium
explored: false
verificationStatus: unverified
claimType: historical
evidenceScope: multi-source-primary
---

# Dubarry 정방향 모드 합성 모델 (2012) — α·β 창 좌표계의 출처

## 정의

M. Dubarry, C. Truchot, B.Y. Liaw, *J. Power Sources* **219** (2012) 204–216
(doi:10.1016/j.jpowsour.2012.07.016) 의 **정방향(모드 → 곡선) 합성 모델**.
반쪽셀 실측 곡선 2개를 **2층 구조**로 조립하고, 열화 모드를 **입력**으로 넣어
full-cell 곡선·IC·DV·ps-OCV 를 합성한다. 저자들은 이것을 "backward looking"
이라 부르는데, 이는 **인과의 방향**(결과가 아니라 원인을 입력으로 둔다)을 뜻하지
수치적 역문제가 아니다 — **이 논문에는 fitting 이 없다**.

핵심은 top layer 의 **파라미터 2개**다 (raw digest §4):

| 기호 | 정의 | 우리 창 모델의 대응 |
|---|---|---|
| `LR = Q_NE/Q_PE` | loading ratio = NE 곡선의 **폭** | `α` (scaling) |
| `OFS` | SOC_PE 축 위 NE 곡선의 **왼쪽 끝** | `β` (offset) |

`[인쇄]` 식 (2') — "generally true, including situations with degradation as well":

> SOC_NE = (100% − SOC_NE)·LR_ini + OFS_ini

모드는 이 둘로만 들어간다 (LAM·LLI 는 전극 곡선 자체를 바꾸지 않는다):

> LR = LR_ini · (100% − %LAM_deNE − %LAM_liNE)/(100% − %LAM_dePE − %LAM_liPE)  … (5)
>
> OFS = OFS_ini + LR·%LAM_liNE + (LR/LR_ini)·%LAM_dePE + %LLI_ch − %LLI_dis   … (8')

Fig. 4 는 이 기하를 **치수선으로 직접 인쇄**한다 (`OFS_ini`, `100%SOC_NE × LR_ini`).
Fig. 6/7 은 모드별 창 변화를 그린다 — **LLI = NE 창의 순수 평행이동**(폭 불변,
양 끝이 함께 이동), **LAM = 창 폭 축소**(li/de 에 따라 어느 쪽 끝이 움직이는지가
갈린다).

## ★ 판정 — 우리 코드 주석의 출처가 여기인가: **(c) 부분적으로 맞다**

이 페이지가 존재하는 첫째 이유. `degradation-degeneracy/docs/02_CODE_AUDIT.md:84`
와 `docs/04_PROMPTS.md:329` 가 `LLI = (1−α_PE) + (β_PE − β_NE)` 에
**"Birkl 2017 부호 규약"** 주석을 단다.
[[birkl-ocv-degradation-diagnostic]] 흡수에서 **Birkl 본문에 α·β 도 그 식도
없음**이 확인됐고, 후보로 지목된 것이 Birkl 참고문헌 [19] 인 이 논문이다.
전문 대조는 raw digest §10.

**여기가 출처인 것** (판정 a 에 해당):

1. **α·β 창 파라미터화 자체** — scaling(`LR`) + offset(`OFS`) 로 반쪽셀 곡선을
   full-cell 축에 얹는 좌표계. 식 (2'),(3) 과 **Fig. 4 의 치수선**이 정본이다.
   Birkl 에는 이 기하가 없다 (Birkl 은 `x_EoC`/`x_EoD` 4개 중 둘을 컷오프
   등식으로 소거한다).
2. **LAM ↔ scaling 관계가 대수적으로 동일하다.** 우리 `α_PE=(1−LAM_PE)/r`,
   `α_NE=(1−LAM_NE)/r` 에서 `r` 을 소거하면
   `α_NE/α_PE = (1−LAM_NE)/(1−LAM_PE)` = Dubarry 식 (5) 의
   `LR/LR_ini`. **같은 식이다.**
3. **LLI 가 offset 에 들어간다는 구조** — 식 (8') 의 `+%LLI_ch`, Fig. 7 의 평행이동.
4. **`LAM_liPE`/`LAM_dePE`/`LAM_liNE`/`LAM_deNE` 4분류와 명명 규칙** —
   §3.1 이 정의문의 출처("li" for lithiated, "de" for delithiated, 전극은
   아래첨자). **Birkl 의 4종 구분은 여기서 왔다** (Birkl 이 [19] 로 인용).

**여기도 아닌 것** (판정 b 에 해당):

5. **`LLI = (1−α_PE) + (β_PE − β_NE)` 라는 식은 이 논문에 없다.** 더구나 식 (8')
   과 **세 군데가 어긋난다**: (i) offset 항 부호가 반대다 — Dubarry 의 `OFS` 는
   `β_NE − β_PE` 에 대응하고 LLI 는 거기에 **+** 로 들어간다, (ii) Dubarry 는
   LAM 항을 **뺀다**, (iii) 그 LAM 항은 `LAM_liNE` 와 `LAM_dePE` 뿐이다 —
   `LAM_liPE` 는 OFS 에 **들어가지 않는다**(Fig. 6(a) 가 그것을 그린다).
6. **전극당 창 2개**(α_PE, β_PE, α_NE, β_NE)가 없다. Dubarry 의 자유도는
   `(LR, OFS)` **2개**이고 PE 는 축 자체로 고정된다.
7. **역문제·목적함수·경계값·역환산 공식**이 전부 없다 — 정방향 전용이다.

**결론 문장**: 우리 코드 주석이 붙여야 할 이름은 **"Birkl 2017 부호 규약" 이
아니라 "Dubarry 2012 (LR·OFS) 창 파라미터화"** 다. 단, 그 이름으로도 legacy 식
자체는 정당화되지 않는다 — **그 식은 두 원전 어디에도 없다.** 가장 정확한 서술은
**"좌표계의 계보는 Dubarry 2012, legacy LLI 식은 문서화되지 않은 우리 쪽
(재)유도"** 다. 현행 `degradation-degeneracy/src/fitting.py:23` 의
`κ·(β_NE − β_PE)` 는 **최소한 offset 부호가 Dubarry 와 일치**한다 —
legacy 문서 쪽이 어긋난 것이다.

### 자유도 계보

| | Dubarry 2012 | Birkl 2017 | 우리 창 모델 |
|---|---|---|---|
| 자유 파라미터 | `(LR, OFS)` = **2** | `[LLI, LAM_PE, LAM_NE]` = **3** | α_PE,β_PE,α_NE,β_NE = **4** |
| 역문제를 푸는가 | **아니다** | 그렇다 | 그렇다 |
| PE 창 | 축으로 고정 | 컷오프 등식으로 구속 | **자유** |

`[해석]` 우리가 관측하는 degeneracy 의 일부가 **원전들에 없는 자유도**에서
온다는 가설이 이 표로 선명해진다 (2 → 3 → 4). 미실측.

## ★ 축퇴가 이미 2012년 식 안에 있다

식 (8') 은 **세 모드(`LAM_liNE`, `LAM_dePE`, `LLI`)를 단 하나의 스칼라 `OFS` 에
덧셈으로** 넣는다. 여기서 식 (5) 와 함께 곧바로 나온다 (raw digest §5.4, 우리 유도):

    {LAM_liNE = x}  ≡  {LAM_deNE = x, LLI = LR·x}

두 시나리오는 `LR` 도 `OFS` 도 동일하게 만든다. 이것은 [[birkl-ocv-degradation-diagnostic]]
이 5년 뒤 §4.2 에서 명시한 축퇴("a combination of e.g. LLI and LAM_NE,de creates
the same OCV signature as an equal amount of LAM_NE,li")와 **정확히 같은
명제**이며, **이미 2012년 이 논문의 식에 대수적으로 들어 있다.**
Dubarry 는 그것을 쓰지 않았다 — 대신 §5.3 에서 같은 사실을 **물리 언어**로
바꿔 읽는다: "LLI shifts the NE-to-PE loading correspondence **in the same
direction as** LAM_dePE" → 그래서 LAM 이 "masked" 된다. **같은 대수적 사실의 두
해석**(축퇴 vs masking)이다.

또한 식 (5) 는 li/de 를 **합으로만** 받는다 — 저자 스스로
"Disregarding if the AM is lithiated or not" 이라 적는다. **scaling 축에서 li/de 는
원리적으로 축퇴**다.

## 저자들이 인정한 구별 불가 (정성적)

`[인쇄]` §4.2 결론:

> "in the case of graphite||LFP chemistry, the derivation of signature for various
> cell degradation modes is rather feasible, but **it is difficult to distinguish
> between LAM_liPE and LLI unambiguously.** This is due to the fact that the LFP used
> in the example has a flat potential plateau and good rate capability."

- 구별 불가 쌍: **LAM_liPE ↔ LLI** (DV 로는 "almost impossible", IC 로는 peak ⑤
  이동 속도로만 가능, 용량손실 <5% 면 그것도 어려움).
- 유일 식별 가능: **LAM_deNE** (모든 peak 이 처음부터 감소).
- 두 번째 축퇴 (§5.2): **LAM ↔ ORI/FRD** — LAM 이 전극 실효 rate 를 올려
  "polarization resistance increase 로 오독된다". ORI 없이 LAM_liPE 만으로
  IC peak 이 저전압으로 이동한다.

`[해석]` 단, 같은 절 서두에는 "we can identify which mode might occur … **without
any ambiguity**" 도 있다. 4종 LAM 끼리로 한정하면 참에 가깝고 LLI 를 넣으면
깨진다. **앞 문장만 떼어 인용하면 논문을 왜곡한다.**

## 정량 진단은 0 — 전수 확인

합자(`ﬁ ﬂ ﬀ`) 정규화 후 본문 전체(61,578자, 13쪽) 검색 (raw digest §11):

`identifiab` **0** · `degenerat` **0** · `non-unique` **0** · `ill-posed` **0** ·
`collinear` **0** · `confidence` **0** · `inverse` **0** · `fitted`/`best fit` **0**.
`uniqu` 7회는 **전부 "unique/novel technique"** 의 자화자찬 어휘이며 수학적
유일성 주장이 아니다. 축퇴는 `ambigu` **3회**에만 살고, 전부 정성적이다.
`fitting` 2회는 **타 연구 비판 맥락**이다 (자기 방법에 fitting 이 없다).

## 왜 중요한가

- **[[fitting-degeneracy]] 의 축퇴가 2012년 식으로 예측된다.** 지금까지 우리가
  본 축퇴는 수치적으로 발견된 것이고, 식 (5)+(8') 이 주는 것은 **해석적으로
  예측된 축퇴 방향**이다 — 검증력이 다르다.
- **"정방향 합성" 은 [[degradation-degeneracy]] 방법론의 선행이다.** 다만
  범위가 다르다 — 이 논문은 **역방향 fitting 을 하지 않으므로 truth 대비 복원
  오차를 잴 수 없고, 격자(다차원 스윕)도 없다** (단독 축 스윕 + 조합 2건, noise
  층 없음). **"합성 truth 를 만든다" 는 선행이고, "합성 truth 로 식별 가능성을
  판정한다" 는 이 논문에 없다.**
- **prognosis 전체가 우리 질문에 의존한다.** `[인쇄]` "It could also be used for
  prognostics by extrapolation from previous RPTs, **if the degradation modes were
  identified** from the test data and the results quantified to feed the model."
  논문은 그 식별을 하지 않는다. 우리가 묻는 것이 바로 그 "if" 다.

## 이 위키에서의 적용

- **용어 계보의 정본**: `LAM_*,li`/`LAM_*,de` 4분류의 출처는
  **Birkl 2017 이 아니라 이 논문 §3.1** 이다. [[birkl-ocv-degradation-diagnostic]]
  의 해당 서술을 이 페이지로 넘긴다.
- **IC peak 의 물리 귀속 주의** `[해석]`: 이 논문에서 IC 5개 peak 은 **전부
  graphite(NE) staging** 에 귀속되고 LFP 는 전압 좌표만 제공한다. 이는
  [[pvs-sev-degradation-mode-features]] 의 PVS 귀속(peak2 = PE)과 **화학종이
  달라서** 직접 충돌하지는 않지만, **LFP‖graphite 에서는 IC peak 의 PE 귀속이
  성립하지 않는다.** 두 진술을 같은 근거로 나란히 인용하면 안 된다.
- **가져올 수 있는 실험 3개** (미실행):
  1. **해석적 축퇴 방향의 직접 시험** — `{LAM_liNE=x}` vs `{LAM_deNE=x, LLI=LR·x}`
     쌍을 격자에 심고 fitting 이 가르는지 본다.
  2. **설계(LR) 축.** 같은 %LLI 가 HP 설계에서는 즉시, HE 설계에서는 **13% 까지
     용량에 전혀 나타나지 않는다** (Fig. 11). 단일 LR 격자는 이 비관측성 축을
     못 잰다.
  3. **LAM ↔ ORI/FRD 오염.** LAM 이 전극 실효 rate 를 올린다 (식 6,7). C-rate 를
     올린 프로토콜을 쓰면 이 오염이 들어온다.
- **인용 금지 문장**:
  - "이 모델은 열화 모드를 곡선에서 식별한다" → **정방향 전용, 역문제 없음**
  - "IC/DV 로 모드를 모호함 없이 가른다" → 4종 LAM 끼리로 한정된 문장
  - "이 방법은 화학종에 제약이 없다" (결론 bullet 4) → §4.2 가 결과를 LFP 평탄
    plateau 탓으로 돌린다. **결론이 본문의 유보를 지운다.**
  - "Dubarry 2012 가 우리 LLI 식의 출처다" → 인용 가능한 것은 **(LR, OFS) 창
    파라미터화와 li/de 4분류까지**다.

## 한계 (raw digest §16, 공백 목록 요약)

- **역문제·목적함수·최적화기·경계값이 전부 없다.** "diagnostic" 은 사람이 IC/DV
  서명을 눈으로 대조하는 것을 뜻한다.
- **실측 대조가 이 논문 안에 없다** (Fig. 3 의 half-cell leave-one-rate-out 제외).
  셀 실측 비교는 [4],[6],[27] 로 넘기고 **[27] 은 이 시점에 미출간**이다.
- **격자가 없다** — 조합 실행은 Fig. 10, Fig. 17 **2건뿐**.
- 외삽 함수형(선형 LLI, 지수 LAM)의 근거는 **"our experience"** 다.
- 결론 bullet 이 §4.2 의 유보를 지운다 (위 인용 금지).
- 그림/범례 불일치 1건: **Fig. 17 의 `Calculated capacity loss` 는 실제로는
  유지율 곡선**이다 (100 에서 시작해 감소).

## 관련
- [[birkl-ocv-degradation-diagnostic]] — 5년 뒤 이 좌표계를 역문제로 만든 절차. 4분류를 여기서 물려받았다
- [[fitting-degeneracy]] — 식 (5)+(8') 이 해석적으로 예측하는 바로 그 축퇴
- [[degradation-degeneracy]] — 정방향 합성의 후손이자, 이 논문이 안 한 역방향 판정을 하는 satellite
- [[22p-physics-or-degeneracy]] — "식별 가능성 진단이 있는가" 에 이 논문의 답은 "없다"
- [[pvs-sev-degradation-mode-features]] — IC peak 물리 귀속의 화학종 의존성 주의
