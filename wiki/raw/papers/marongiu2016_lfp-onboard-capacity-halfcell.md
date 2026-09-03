---
title: "Marongiu et al. 2016 — On-board capacity estimation of LFP batteries by means of half-cell curves (JPS 324)"
source_url: local-upload/4._Onboard_capacity_estimation_of_lithium_iron_phosphate_batteries_bymeans_of_halfcell_curves.pdf
ingested: 2026-09-03
sha256: 533058bc4692f49b48faf9410ef7ba6d62aaa50a82c9294734875add429a79e0
---

# 수집 목적

A. Marongiu, N. Nlandi, Y. Rong, D.U. Sauer,
**"On-board capacity estimation of lithium iron phosphate batteries by means of
half-cell curves"**, *Journal of Power Sources* **324** (2016) 158–169 의
**절별 해체분석**.

제목에 **half-cell curves** 가 있고, 실제로 **우리 파이프라인이 α·β 로 하는 바로
그것** — 반쪽전지 곡선 두 개를 창(window)으로 붙여 full-cell 을 재구성하고 그
창의 위치·폭에서 열화 모드를 읽는 것 — 을 한다. 그래서 이 digest 의 무게중심은
"무엇을 발견했나" 가 아니라 **"우리와 같은 도구를 쓰는데 어디가 같고 어디가
다른가"** 다.

세 가지가 이 논문을 이 계보에서 특별하게 만든다:

1. **창 매개화가 식으로 인쇄돼 있다** (식 2–5). Dubarry 2012 는 2-파라미터
   `(LR, OFS)`, Birkl 2017 은 3-파라미터 `[LLI, LAM_PE, LAM_NE]` 를 쓰는데,
   이 논문은 **5개 모드 → 4개 창 좌표** 의 사상(map)을 **전부** 적어 놓았다.
   그 결과 **축퇴가 손으로 풀린다** (§5 — 이 digest 의 최대 산출물).
2. **LFP 셀**이다. OCV 가 평탄해서 전압 잔차 fitting 이 성립하지 않는 화학이고,
   저자들은 그래서 **관측을 전압 곡선이 아니라 「평탄역 길이 3개」라는 스칼라
   3개로 바꾼다**. 관측을 극단적으로 줄였을 때 무슨 일이 일어나는지의 실측이다.
3. **차량 탑재(on-board)** 제약 아래에서 돌린다. 실험실 조건과 무엇을
   맞바꾸는지가 인쇄돼 있다.

**표기 규칙** (이 위키 관례 3구분):
- `[인쇄]` — 논문 본문/표/식에 글자로 있는 것
- `[도표]` — 그림에서 눈으로 읽은 근사값 (원 데이터가 아니다)
- `[해석]` — 이 문서를 쓰면서 붙인 판단. **논문의 주장이 아니다**
- `[재현]` — 이 세션에서 원문 식을 그대로 코드로 옮겨 계산한 결과

- 원본 파일: 로컬 업로드 PDF (저장소에 바이너리를 넣지 않는다)
- 크로핑 그림: `raw/figures/marongiu2016_lfp-onboard-capacity-halfcell/`
  (fig 8장 + tab 5장, `figures.json` 에 캡션 색인)
- 페이지 참조는 **저널 페이지(158–169)**. PDF 페이지 + 157 = 저널 페이지다.

---

## 0. 서지사항 (직접 확인)

`[인쇄]` PDF 헤더/푸터 및 메타데이터:

| 항목 | 값 |
|---|---|
| 제목 | On-board capacity estimation of lithium iron phosphate batteries by means of half-cell curves |
| 저자 | Andrea Marongiu ᵃᐟᶜ (교신), Nsombo Nlandi ᵃᐟᶜ, Yao Rong ᵃᐟᶜ, Dirk Uwe Sauer ᵃᐟᵇᐟᶜ |
| 소속 | a: ISEA, RWTH Aachen · b: PGS, E.ON ERC, RWTH Aachen · c: JARA-Energy |
| 학술지 | Journal of Power Sources **324** (2016) 158–169 |
| DOI | 10.1016/j.jpowsour.2016.05.041 |
| 접수/개정/게재 | Received 6 March 2016 · Revised 17 April 2016 · Accepted 10 May 2016 · Available online 26 May 2016 |
| 저작권 | © 2016 Elsevier B.V. All rights reserved (**open access 아님**) |
| 키워드 | LiFePO4 batteries · On-board capacity estimation · Degradation modes · Half-cell curves |
| 지원 | BMBF LiMobility, grant 03X4614C |
| 분량 | 12쪽 (본문 ~50,127자, 참고문헌 제외) |

`[인쇄]` Highlights 4개 (p.158):
> - A novel approach for total capacity estimation of LFP cells in EVs is presented.
> - The method is based on the estimation of some degradation modes during lifetime.
> - The algorithm allows estimating the total capacity with **an error of approx. 1%**.
> - The obtained results allow the recalibration of a hysteresis model of the OCV.

### 0.1 ★ 이 위키에 이미 예약된 자리가 있었다

`wiki/questions/22p-physics-or-degeneracy.md` **2026-09-03 (2) 항목 3** 이
우리 legacy `LLI` 식의 출처 후보로 **"[19] Dubarry 2012, [26] Marongiu 2016"**
을 지목했다. 그 `[26]` 이 **이 논문이다** — Birkl 2017 참고문헌 [26] 을 직접
대조해 확인했다:

> `[인쇄, Birkl 2017 참고문헌]` "[26] A. Marongiu, N. Nlandi, Y. Rong, D.U.
> Sauer, On-board capacity estimation of lithium iron phosphate batteries by
> means of half-cell curves, J. Power Sources 324 (2016) 158e169."

그리고 Birkl 본문에서 `[26]` 이 인용되는 자리 **두 곳**을 찾았다:

> `[인쇄, Birkl 2017 §1]` "The assumed links between the OCV and degradation
> modes have been used for SoH estimation in the literature **[19,25,26]**."
>
> `[인쇄, Birkl 2017 §3.1]` "The theory underlying the proposed degradation
> modes and their effects on the OCV of cells and electrodes is well documented
> in the literature **[19,26,29]**."

`[해석]` 즉 **Birkl 자신이 "모드 → 전극 곡선" 이론의 출처로 Dubarry 2012 와
이 논문을 지목한다.** 우리 저장소 `docs/02_CODE_AUDIT.md` 가 2026-09-03 에
"Birkl 2017 부호 규약" 주석을 제거하며 열어 둔 계보 질문의 **남은 한 후보가
이것**이었고, 이 digest 가 그것을 닫는다 (§11.2).

---

## 1. 원문에 없어서 확인이 필요한 것 (공백 목록)

digest 를 쓰기 전에 먼저 밝힌다. 아래는 **논문이 인쇄하지 않은 것**이며, 후속
인용에서 이 자리를 메꾸는 문장을 쓰면 그것은 이 논문의 근거가 아니다.

1. **`Q_Ne,BOL` 의 수치가 없다.** 식 (2)–(5) 전체가 이 값(= 로딩비 N/P)에
   비례하는 항을 갖는데, 논문은 `[인쇄]` "in a fresh state Q_Pe,BOL is equal to
   one, while Q_Ne,BOL is **normally bigger than one**" 이라고만 쓴다. 숫자
   **n/a**. §5 의 축퇴 방향 계수가 이 값이므로 **정량 환산이 안 된다**.
2. **초기 offset 의 값이 없다.** Fig. 1a 의 `Offset`(= `Q_Pe,start` 가 0보다
   작은 양)이 BOL 에서 얼마인지 인쇄되지 않았다. 식 (4) 는 BOL 에서
   `Q_Pe,start = 0` 을 주므로 **식과 그림이 이 점에서 어긋난다** (§10 ①).
3. **추정된 모드 값의 표가 없다.** 7개 셀에 대해 알고리즘이 낸
   `(LLI, LAM_Ne,De)` 는 Fig. 6 의 예시 한 쌍(12.97 % / 19.23 %)뿐이고,
   나머지 셀의 값은 어디에도 없다. **모드는 검증되지 않았고 용량만 검증됐다.**
4. **모드 추정값의 정답(해체분석)이 없다.** post-mortem 은 §4.2.1 에서
   **다른 논문 [23,38,39,30]** 을 인용해 "LFP 는 LLI 와 LAM_Ne 로 설명된다"
   는 **가정의 근거**로만 쓰였고, 이 논문 자신의 셀은 해체되지 않았다.
5. **불확실성·신뢰구간·상관·Hessian·감도 분석이 하나도 없다.** Fig. 7 의
   오차 막대는 **7개 셀에 대한 오차의 표준편차**(Table 5 의 STD)이지 추정
   불확실성이 아니다.
6. **전압 잔차가 보고되지 않는다.** 이 방법은 전압을 적합하지 않는다 (§6.3).
   본문 전체에서 `mV` 는 **1회**뿐이고 그것도 적합 잔차가 아니라 히스테리시스
   재보정 후의 룩업테이블 오차다.
7. **다중시작·초기값 목록이 없다.** Fig. 6 에서 초기값이 `[도표]` LLI 17.5 % ·
   LAM 30 % 로 읽히지만 본문에 인쇄돼 있지 않고, 그 값을 어떻게 정하는지도
   없다. 단 **1-plateau 시나리오에서만** `LAM_start = 10 %` 와 `0 %` 두 값을
   비교한다 (§8.3 — 이 논문에서 가장 값진 실험이다).
8. **평탄역 검출 알고리즘의 세부가 참고문헌으로 넘어간다.** 선형/시그모이드
   적합의 기울기 임계값, 시그모이드의 형태, VPA 의 상세는 각각 [33],[34],[35],
   [32] 로 돌린다. 이 논문만으로는 **재현 불가**다.
9. **잡음 모형이 없다.** `noise` 2회는 둘 다 "미분이 잡음을 증폭한다" 는
   문장 하나에 있고, 측정 잡음 크기·전파 분석이 없다.
10. **평탄역 길이 측정의 반복 재현성이 없다.** Fig. 4 의 산포가 유일한 단서인데
    (§8.2), 그것은 재현성이 아니라 **조건 간 환산 회귀의 잔차**다.
11. **셀 개수 7개, 화학 1종.** 통계적 주장을 하기에는 작고, 저자들도 통계
    검정을 하지 않는다.

---

## 2. ★ 의뢰 질문 6개에 대한 직답 (근거는 아래 절)

이 절만 읽어도 되도록 쓴다. 각 항의 상세와 원문 인용은 지시된 절에.

### Q1. 창 매개화가 정확히 무엇인가 — 자유 파라미터 개수와 제약

`[인쇄]` 식 (2)–(5) 는 **전극별 시작점·끝점 4개**를 **모드 5개**의 함수로 준다.
제약(등식)은 **하나도 없다.** 즉 **5 → 4 의 사상**이고, 그 자체로
**최소 1차원의 정확한 축퇴**를 갖는다. 관측이 평탄역 **길이**(= 차이)라서
평행이동이 안 보이면 **축퇴는 2차원**이 된다 — §5 에서 손으로 풀고 수치로
확인했다.

실제 실행에서는 **5개 중 3개를 0으로 못박아** 자유 파라미터를 **2개**
(`LLI`, `LAM_Ne,De`) 로 줄인다. 그 근거는 데이터가 아니라 **다른 논문의
해체분석 문헌**이다.

**⚠ 논문 안에서 파라미터 개수가 세 번 다르게 쓰인다** (§10 ②):
모델(식 2–5) **5개** · 알고리즘 서술(§3, Fig. 2, Fig. 3) **3개**
(`P_i = [LLI; LAM_Pe; LAM_Ne]`) · 실제 실행(§4.2.1) **2개**.

계보 비교표 (의뢰가 요청한 것):

| 문헌 | 자유 파라미터 | 개수 | 등식 제약 | 관측 | 창 좌표로 사상 |
|---|---|---|---|---|---|
| **Dubarry 2012** | `LR`, `OFS` | **2** | 0 | full-cell 곡선 · ICA | 2 → 2 (전단사) |
| **Marongiu 2016 (모델)** | `LLI, LAM_Pe,Li, LAM_Pe,De, LAM_Ne,Li, LAM_Ne,De` | **5** | **0** | 평탄역 길이 3개 | **5 → 4** (또는 관측상 **5 → 3**) ⇒ **null 2차원** |
| **Marongiu 2016 (실행)** | `LLI, LAM_Ne,De` | **2** | 나머지 3개 **= 0 하드 고정** | 평탄역 길이 1~3개 | 2 → 3 (관측) |
| **Birkl 2017** | `LLI, LAM_PE, LAM_NE` (+ `Δx_EoC, Δx_EoD`) | **3** | **2** (컷오프 전압 등식 11·12) | full-cell 전압 곡선 | 5 → 4, 제약 2로 소거 |
| **Lin & Khoo 2024** | `r_N/P`, `z₀⁺` | **2** | 0 | SOC 정규화 OCV **형상** | 정의상 2 (형상 자유도) |
| **Navidi 2024** | `m_p, δ_p, m_n, δ_n` | **4** | **0** | full-cell 전압 곡선 | 전단사 |
| **우리** | `α_PE, β_PE, α_NE, β_NE` | **4** | **0** | full-cell 전압 곡선 (+옵션 dQ/dV) | 전단사 |

`[해석]` **이 표에서 읽을 것.** 창 좌표는 어디서나 4개다. 갈리는 것은
**그 4개를 무엇으로 매개화하느냐**다.
- **Birkl** — 5개로 매개화하고 **등식 2개로** 여분을 죽인다.
- **Marongiu** — 5개로 매개화하고 **3개를 0으로 놓아** 여분을 죽인다
  (등식이 아니라 **사전 믿음**이다).
- **우리·Navidi** — 4개를 **직접** 자유 파라미터로 쓴다. 모드 층을 만들지
  않으므로 **이 두 논문의 null 을 물려받지 않는다.** 대신 모드 이름도 공짜로
  얻지 못하고, 사후 변환(`LAM_PE = 1 − α_PE·r` 등)이 **몫공간으로의 사영**이
  된다 — Birkl 이 설계로 한 것을 우리는 변환으로 한다.

### Q2. LFP 의 평탄한 OCV 를 어떻게 다루는가

**미분을 쓰지 않는다.** ICA/DVA 를 명시적으로 배제한다:

> `[인쇄, p.159]` "Unfortunately **the derivative operation in signals with
> superimposed noise can lead to the amplification of this noise**, and, in some
> cases, to the misinterpretation of the processed information."

> `[인쇄, p.163]` "The detection of the plateaus on the collected data during
> the online and the offline procedure takes place **without the need of any
> differentiation**."

대신 **평탄역(two-phase transition plateau) 세 개의 길이를 Ah 단위로 잰다.**
LFP‖Gr 은 캐소드가 전 구간 평탄역 하나(A), 애노드가 평탄역 셋(I, II, V) 이므로
full-cell 에 **IA · IIA · VA** 세 평탄역이 생긴다 (Fig. 1a).

즉 **평탄함을 문제로 보지 않고 관측으로 바꾼다** — 평탄역의 *전압*은 정보가
없지만 그 *길이*에는 정보가 있다. 이것이 이 논문의 핵심 발상이고, NMC 계열의
전압 잔차 fitting 과 **관측 공간 자체가 다르다.**

**평탄해서 못 하는 것을 논문이 인정하는가 — 인정한다, 두 곳에서:**

> `[인쇄, p.159]` "The use of the OCV-SoC relation of equation (1) for capacity
> estimation becomes more complicated or not feasible in case of lithium iron
> phosphate (LFP) cells. In fact, **the flatness of the OCV curve and its
> remarkable hysteresis behavior make the diagnostic of this cell particularly
> difficult.**"

> `[인쇄, p.167]` "The error is significant especially in the low and high SoC
> range. **In the middle SoC range it remains limited, due to the flat
> characteristics of the OCV curve of LFP cells.**"

`[해석]` 두 번째 문장이 우리에게 중요하다 — 그 "limited" 는 좋은 뜻이 아니다.
**신선셀과 노화셀(SoH 77~89 %)의 OCV 차이가 중간 SoC 대역에서 사실상 0이라는
뜻**이고, 그건 곧 그 대역에 열화 정보가 없다는 뜻이다. `[도표, Fig. 8c]`
SoC 45–65 % 에서 `|ΔOCV|` 막대가 **≈ 0.001~0.003 V** 다. 상세는 §8.5.

### Q3. onboard 제약이 방법을 어떻게 바꾸는가

`[인쇄]` 바뀌는 것 다섯:

1. **관측이 곡선에서 스칼라 3개로 줄어든다.** 실험실이면 quasi-OCV 곡선 전체를
   쓰겠지만, 차량에서는 완전 방전을 못 하므로 부분 구간에서 잡히는 **평탄역
   길이**만 쓴다. `[인쇄, p.168]` "In order to calculate the battery capacity,
   **it is not necessary to discharge the cell completely.** The information
   contained in the plateaus is adequate. In particular, **only the length of
   the plateau represents sufficient information**."
2. **전류율 상한.** `[인쇄, p.161]` "currents smaller than **0.3C** are
   sufficient" (충전 중 관측), `[인쇄, p.163]` "**current rates above 0.3C are
   not sufficient to clearly distinguish the plateaus**".
3. **조건 환산 회귀가 하나 더 붙는다.** 실제 주행/충전은 표준(0.1C, 23 °C)이
   아니므로 Fig. 4 의 선형 회귀로 표준 조건 길이로 되돌린다. **이 회귀의 잔차가
   관측 오차의 바닥**이 되는데 논문은 그것을 오차예산에 넣지 않는다 (§8.2).
4. **OCV 를 직접 못 재므로 EECM 으로 추정한다** (Waag [32]). Fig. 5 가 FTP75
   주행 중의 결과다. `[인쇄, p.164]` "it is possible to correctly estimate the
   length of the single plateaus … **without precisely tracking the OCV**."
5. **계산을 real-time 에서 뺀다.** `[인쇄, p.161]` "not real-time/offline
   calculation is referred to the possibility for the microcontroller in the BMS
   to **not carry out the requested operation in real time**. This allows the
   distribution of the computational effort over a longer time period, thus
   reducing the load of the BMS microcontroller." 반복 예산은
   `[인쇄, Table 2]` **`It_max = 100`** 이다.

**맞바꾼 것**: `[인쇄, p.168]` 저자들이 스스로 적은 유일한 단점 —
> "The main drawback of this method is that the most needed information resides
> in the plateaus' lengths. Therefore **it is necessary to measure a plateau
> without interruption.** This means that **occasionally it is necessary to
> discharge the battery during normal driving operation until 30%–40% SoC.**"

### Q4. 비유일성을 다루는가

**어휘로는 전혀 다루지 않는다.** 어휘 전수 (§9): `identifiab*` **0** ·
`degenerac*` **0** · `non-unique`/`uniqueness`/`uniqu` **0** · `nullspace` **0** ·
`collinear*` **0** · `ill-posed` **0** · `uncertaint*` **0** · `error bar` **0** ·
`cross-valid*` **0** · `Fisher`/`Hessian`/`condition number`/`singular value`
**각 0** · `sensitivit*` **0** · `confidence` **0**.

**그러나 세 곳에서 실질을 건드린다.** 이것이 이 digest 의 발견 중 하나다:

**(a) 모드 축퇴를 한 문장으로 인정하고, 그것을 근거로 파라미터를 줄인다.**
> `[인쇄, p.164]` "In particular, considering the two possible different types of
> LAM on the negative electrode (lithiated and delithiated), and observing
> singularly their impact on the plateaus' lengths, **the obtained results are
> completely comparable**, as also exemplary discussed in Ref. [17]. Therefore,
> in this work, between the two possible LAM_Ne, **only the LAM_Ne,De is used**
> for the estimation of the battery capacity."

`[해석]` 이것은 Birkl §4.2 의 `pure-LLI + LAM_de ↔ LAM_li` 와 **같은 축퇴**이고,
Dubarry 2012 의 `{LAM_liNE = x} ≡ {LAM_deNE = x, LLI = LR·x}` 와 **같은
축퇴**다. 세 번째 독립 확인이며, 이 논문만이 **그것을 식으로 쓰고 그 식을 쓴다**.

**(b) 모드의 물리적 정확성을 명시적으로 범위 밖에 둔다.**
> `[인쇄, p.165]` "Moreover, all these hypotheses are based on the fact that the
> main goal of the presented method is the estimation of the total battery
> capacity. **The correct determination of all the degradation mechanisms which
> physically perfectly mirror the actual battery aging state is out of the goal
> of this work.**"

`[해석]` 이 계보 열세 편 중 **가장 정직한 문장**이다. 22p 카드가 다른 논문들에
대해 반복해서 지적해 온 것("적합값을 물리처럼 읽는다")을 이 논문은 **먼저
포기한다.** 인용할 때 이 문장을 빼면 안 된다.

**(c) 국소최소를 이름으로 언급한다 — 딱 한 번.**
> `[인쇄, p.164]` "As the method is approaching the found minima (**global or
> local**), the generation of the new parameter set P_i occurs with smaller
> interval in respect to the first step."

그리고 **수렴 실패의 메커니즘을 서술한다** (다중시작이 아니라 관측 충돌로):
> `[인쇄, p.166]` "it can happen that **the change of one of the degradation
> modes can generate a reduction of the error related to a single plateau but
> the increase of the other ones.** Therefore following this process **the
> algorithm can enter a closed loop and converge to an imprecise solution.**"

**초기값·경계·multi-start**: 경계 없음(인쇄 없음), multi-start 없음.
갱신은 **블록 교대 규칙**이다 (§6.4). 초기값 의존성은 **1-plateau 시나리오에서만
두 값으로 시험**되고 결과는 극적이다 (§8.3) — `LAM_start` 를 10 % → 0 % 로
바꾸면 용량 오차가 **6.38 % → 14.46 %** (충전), **4.33 % → 12.51 %** (방전).

### Q5. 잡음·정확도 수치

**용량 추정 오차** — `[인쇄, Table 5, p.166]`:

| | 3 평탄역 | 2 평탄역 | 1 평탄역 (LAM_start=10 %) | 1 평탄역 (LAM_start=0 %) |
|---|---|---|---|---|
| 충전 평균 / % | **0.98** | **0.78** | 6.38 | 14.46 |
| 충전 STD / % | 0.72 | 0.50 | 2.83 | 5.28 |
| 방전 평균 / % | **1.10** | **0.70** | 4.33 | 12.51 |
| 방전 STD / % | 0.71 | 0.54 | 2.11 | 5.05 |

**전압 잔차는 인쇄돼 있지 않다 — 이 방법은 전압을 적합하지 않기 때문이다.**
적합 잔차는 **Ah 단위의 평탄역 길이 오차**다:
`[도표, Fig. 6d]` 수렴 후 `ΔL1 = 0.0531 Ah`, `ΔL2 = 0.0517 Ah`,
`ΔL3 = 0.0206 Ah` (8 Ah 공칭의 **0.26 ~ 0.66 %**).
`[인쇄, Table 2]` 정지 임계 `ε_total = 0.1 Ah`(충전) / **0.01 Ah**(방전),
`ε_threshold = 0.3 Ah`.

**우리 1 mV / 5 mV 문턱, Cui 의 < 6 mV 와 비교 가능한가 — 직접적으로는
불가능하다.** 관측 공간이 다르다(V vs Ah). 그러나 **간접 비교가 하나 가능하고,
그것이 이 논문이 우리에게 주는 가장 값진 수치다** (§8.5):

`[도표, Fig. 8c]` **신선셀 vs 노화셀**의 OCV 차이가
- SoC 20–30 % 에서 최대 ≈ **32 mV**
- SoC 75–85 % 에서 최대 ≈ **38 mV**
- **SoC 45–65 % 에서 ≈ 1–3 mV**

`[인쇄, p.167]` 재보정 후 "**reduces the error to 20 mV** for almost the entire
SoC range" — `[도표, Fig. 8d]` 실제 최대는 ≈ **22 mV** (SoC 10 %, 방전).

`[해석]` **LFP 에서는 SoH 100 % → 77~89 % 의 열화 전체가 중간 SoC 대역에서
1–3 mV 의 전압 신호밖에 남기지 않는다.** 우리 격자의 σ = 5 mV 층은 그 신호를
통째로 묻고, σ = 1 mV 층에서도 1σ 수준이다. **이것이 "LFP 에서 전압 잔차
fitting 을 하지 않는다" 의 정량적 이유**이며, 우리 Phase 1c 의 문턱 논의를
다른 화학으로 확장할 때 쓸 수 있는 첫 실측 정박점이다. (⚠ 이 값은 **모드 분해의
감도가 아니라 전체 열화의 전압 흔적**이다 — 상한으로만 쓴다.)

### Q6. 우리가 채택할 것과 반증해야 할 것 → §11 에 표로

한 문장 요약: **채택은 「축퇴 방향의 닫힌 형태」와 「초기값 스윕이라는 값싼
식별 가능성 시험」이고, 반증(=경계 확정)해야 할 것은 「관측을 늘렸더니 나빠졌다」
가 우리 dQ/dV 결과와 같은 원인인가**다. 그리고 **Phase 1d 에 대해서는**:
Marongiu 는 σ3·σ4 에 해당하는 약한 방향을 **재보고 죽인 것이 아니라 사전 믿음으로
죽였다** — 우리 실측(σ3/σ1 ≈ 0.05 ≠ 0)은 그 사전 믿음이 **데이터에 의해 요구되지
않는다**는 반대 증거를 준다.

---

## 3. 논문의 질문과 답 (§1, p.158–159)

### 3.1 문제 설정

`[인쇄]` 초록:
> "This paper presents a novel methodology for the on-board estimation of the
> actual battery capacity of lithium iron phosphate batteries. The approach is
> based on the detection of the actual degradation mechanisms by collecting
> plateau information. **The tracked degradation modes are employed to change the
> characteristics of the fresh electrode voltage curves (mutual position and
> dimension), to reconstruct the full voltage curve and therefore to obtain the
> total capacity.**"

`[해석]` "mutual position and dimension" 이 곧 우리 `(β, α)` 다. 문장 하나가
창 모델의 정의다.

`[인쇄]` §1 이 나열하는 기존 방법과 그 기각 사유:

| 방법 | 참고문헌 | 기각 사유 (`[인쇄]`) |
|---|---|---|
| Coulomb counting + OCV-SoC | [2,3] | "the issue regarding the change of the OCV curve due to aging **is not handled** by the authors" |
| 완화 중 EMF 추정 | [5] | "**not feasible for LFP cells**, due to the mentioned features" |
| 필터(EKF 등) | [6–8] | "**can be hardly implemented in cheap microcontrollers**" |
| ICA / DVA 온보드 | [13–15] | "the derivative operation … **amplification of this noise** … misinterpretation" |
| 반쪽전지 기반 용량 추정 | **[22] Wang 2014** | "applied on **nickel manganese cobalt** cells and is based on the assumption that **the electrode characteristics do not change during battery lifetime, an assumption which cannot be made for LFP cells** [17]" |

`[해석]` **마지막 줄이 우리와 직결된다.** [22] Wang et al. 2014 (*JES* 161,
A1788) 는 NMC 셀에서 반쪽전지 곡선으로 용량을 추정한 논문이고, 이 논문은 그
가정 — **반쪽전지 OCP 가 노화에 불변** — 이 LFP 에서는 못 쓴다고 적는다.
**그 가정은 우리 파이프라인의 가정이기도 하다** (`degradation-degeneracy` 는
pristine half-cell 곡선을 고정하고 창만 움직인다). Lin & Khoo 2024 도 같은
가정을 명시적 한계로 적는다. 즉 **이 계보 전체가 같은 가정 위에 있고, 이 논문은
그 가정이 화학에 따라 깨진다고 지목하는 자리**다. 다만 이 논문 자신도 §3 에서
**신선셀 반쪽전지 곡선을 그대로 고정해 쓴다** — 자기 비판을 자기가 지키지 않는다
(§10 ④).

### 3.2 답 (결론, p.168)

`[인쇄]` 다섯 개 bullet 중 핵심 셋:
> - "**Not all the plateaus are needed**: the knowledge of three or two plateaus'
>   lengths is necessary and sufficient to correctly calculate the battery
>   capacity. An average error of 0.98% (charge) and 1.10% (discharge) is
>   obtained when three plateaus are known, and of 0.78% (charge) and 0.70%
>   (discharge) when two plateaus are known. **The knowledge of only one plateau
>   does not assure the correct tracking of the degradation modes** and therefore
>   the proper estimation of the battery capacity."
> - "The algorithm is easy to parametrize: **only the characteristics of the cell
>   in a fresh state are needed**, in terms of stoichiometry and half-cell voltage
>   curve."
> - "The method presented in this paper is **valid for LFP/G cells**, mainly due
>   to the need of collecting information of plateaus … Nevertheless, the proposed
>   model and the approach shown in the literature **are general approaches**,
>   which can also be used for other lithium-ion chemistries."

`[해석]` 첫 bullet 의 "**three or two**" 라는 표현은 조심해서 읽어야 한다.
Table 5 를 보면 **2개가 3개보다 좋다** (0.78 < 0.98, 0.70 < 1.10) — 즉 "3개도
2개도 충분하다" 가 아니라 **"3개는 2개보다 나빴다"** 가 데이터가 말하는 것이고,
저자들도 §4.2.1 에서 그 이유를 설명한다 (§8.4). 결론 bullet 은 그 방향을
중립화해서 적는다.

---

## 4. LFP 열화 모델 — 창 매개화의 정확한 정의 (§2, p.159–161) ★★ 의뢰 1항

### 4.1 관측의 구조 (Fig. 1a)

`[인쇄, p.159]` LFP‖Gr 의 전압 곡선 구조:
> "The cathode presents a flat voltage characteristic, or a so called plateau,
> for the entire SoC range. This flat region is indicated with the letter **A**.
> … In case the anode is composed of graphite, the anode voltage profile presents
> **three flat regions indicated as I, II and V** … Accordingly, the full voltage
> curve of an LFP cell with graphite electrode is characterized by **three
> plateaus**, which are indicated … as **IA, IIA and VA**."

`[인쇄, p.159]` 신선셀의 두 비대칭:
> "the lengths of the cathode and anode curves … **are not equal, since generally
> the anode is slightly oversized to avoid lithium plating** [23]. Moreover, in
> the fresh state, **the starting point of the anode and cathode curves are
> slightly shifted by an offset**, which means that during the operation of the
> cell the two electrodes are not used entirely."

`[해석]` 앞 문장이 **N/P > 1**, 뒷 문장이 **Li/P 절편** 이다 —
[[np-lip-ocv-reparametrization]] 의 두 비(比)를 말로 쓴 것이다.

`[도표, Fig. 1a]` **가로축이 `Ah relative` 인 하나의 공통 축**이고, 그 위에
왼쪽부터 `Q_Pe,start` (0보다 왼쪽) → `Q_Ne,start` → `Q_Pe,end` → `Q_Ne,end` 네
점이 찍혀 있다. `Offset` 은 앞 두 점 사이의 간격으로 표시된다. 즉 **창 좌표는
「전극별 (시작점, 끝점)」이고, 우리 `(β, β+α)` 와 좌표계가 같다.**
`[도표]` 그림 안 마커: 자물쇠 = 그 끝이 고정되는 지점, 화살표 = 움직이는 방향.
b) LLI 에서는 **캐소드 곡선 전체가 왼쪽으로** 이동한다.

`[인쇄, p.159]` LLI 의 효과:
> "The effect of the LLI on the full voltage curve is depicted in Fig. 1b), and
> **can be represented by a left shift of the cathode curve in respect to the
> anode curve** [17]. As a consequence, **the length of plateau IA is reduced**
> together with a decrease of the battery capacity."

`[인쇄, p.160]` LAM 의 효과와 li/de 구분:
> "The effect of the LAM on the full voltage curve can be distinguished referring
> to the cases in which this mechanism take places in a lithiated or in a
> delithiated phase. Therefore **four different cases** can be identified, as
> depicted in Fig. 1c–f). For all of them **LAM can be represented as the
> shrinkage of the considered electrode curve maintaining it fixed in the point
> relative to the lithiated/delithiated phase.**"

`[해석]` 이것이 우리 격자 `lam_pe_type`/`lam_ne_type ∈ {li, de}` 와 같은 축이고,
Birkl §2.1 과도 같다. **세 논문이 같은 정의를 쓴다.**

### 4.2 ★ 식 (2)–(5) — 원문 이미지에서 부호까지 직접 확인

텍스트 추출이 마이너스 기호를 잃어버려서, 저널 조판본 p.160 우측 단을
**400 dpi 로 재렌더링해 눈으로 확인**했다. 그대로 옮기면:

```
Q_Ne,start = − LAM_Pe,De · Q_Pe,BOL                                   … (2)

Q_Ne,end   = Q_Ne,BOL − LAM_Ne,De · Q_Ne,BOL − LAM_Ne,Li · Q_Ne,BOL
                      − LAM_Pe,De · Q_Pe,BOL                          … (3)

Q_Pe,start = − LAM_Ne,Li · Q_Ne,BOL − LLI · Q_Pe,BOL                  … (4)

Q_Pe,end   = Q_Pe,BOL − LAM_Pe,Li · Q_Pe,BOL − LAM_Pe,De · Q_Pe,BOL
                      − LAM_Ne,Li · Q_Ne,BOL − LLI · Q_Pe,BOL         … (5)
```

`[인쇄, p.160–161]` 정규화 규약:
> "The Ah scale is normalized in respect to the total capacity of the positive
> electrode in a fresh state. This means that **in a fresh state Q_Pe,BOL is
> equal to one, while Q_Ne,BOL is normally bigger than one.** … considering the
> cell in a fresh state (case of Fig. 1a), **the value of Q_Ne,start is zero**,
> which corresponds also to the fully discharged state of the full cell;
> **Q_Pe,start is smaller than zero**, with a value depending on the initial
> offset. The value of the Q_Pe,end is then smaller than one. The resulting full
> voltage range, which goes from Q_Ne,start to Q_Pe,end **is considered as the
> reference value for a cell in a fresh state**, i.e. in the normalized reference
> system the fresh cell has a full capacity equal to one."

`[인쇄, p.161]` 파생량 (Groot [18] 인용):
```
Q_Ne,EOL = Q_Ne,BOL · (1 − LAM_Ne)                                    … (6)
Q_Pe,EOL = Q_Pe,BOL · (1 − LAM_Pe)                                    … (7)
Q_full cell,EOL = min(Q_Ne,end, Q_Pe,end) − max(Q_Ne,start, Q_Pe,start)  … (8)
```

`[해석]` **우리 좌표와의 대응이 정확히 성립한다** (`[재현]` 아래에서 확인):
```
α_PE ↔ Q_Pe,end − Q_Pe,start = Q_Pe,BOL·(1 − LAM_Pe)     ← 식 (7) 과 일치
β_PE ↔ Q_Pe,start
α_NE ↔ Q_Ne,end − Q_Ne,start = Q_Ne,BOL·(1 − LAM_Ne)     ← 식 (6) 과 일치
β_NE ↔ Q_Ne,start
β_NE − β_PE = LLI·Q_Pe,BOL + LAM_Ne,Li·Q_Ne,BOL − LAM_Pe,De·Q_Pe,BOL
```
마지막 줄이 **우리 `src/fitting.py` 의 `κ·(β_NE − β_PE)` 항의 부호와 일치**한다
(§11.2). 다만 그 항 앞에 붙는 `w_PE·α_PE + w_NE·α_NE` 가중 부분은 이 논문에
**없다** — 대응은 부호 규약까지이고 식 전체가 아니다.

### 4.3 식 (8) 이 하는 일 — 왜 min/max 인가

`[해석]` 식 (8) 은 "두 전극 창의 **교집합** 길이" 다. `min` 은 충전 종료를
먼저 걸리는 전극이, `max` 는 방전 종료를 먼저 걸리는 전극이 정한다. **컷오프
전압이 아니라 전극 창의 끝이 한계를 정한다** — Birkl 이 컷오프 **전압**
등식(4.2 V / 2.7 V)으로 하는 일을, 이 논문은 **용량 창의 끝**으로 한다.

`[해석]` **왜 이 차이가 LFP 에서 필연인가**: LFP 의 full-cell 전압은 평탄해서
"전압이 2.7 V 에 닿는 지점" 이 곡선 위에서 잘 정의되지 않는다 (기울기가 거의
0인 구간에서 전압 등식은 조건수가 폭발한다). 그래서 컷오프 전압 제약이라는
Birkl 의 장치가 **이 화학에서는 쓸 수 없고**, 대신 창의 기하로 대체된다.
이것은 이 논문이 명시적으로 적는 것은 아니다.

---

## 5. ★★ 이 매개화의 축퇴를 손으로 풀었다 (이 digest 의 최대 산출물)

`[해석]` **아래 계산은 논문에 없다.** 재료는 전부 `[인쇄]` (식 2–5, 식 8) 이고,
계산은 이 세션에서 했다. 논문 자신은 §4.2.1 에서 그 결론의 **일부**만 말로 적는다.

### 5.1 관찰 — 5개 모드가 4개 창 좌표로 들어간다

식 (2)–(5) 를 `P = Q_Pe,BOL = 1`, `N = Q_Ne,BOL`,
`(l, a, b, c, d) = (LLI, LAM_Pe,Li, LAM_Pe,De, LAM_Ne,Li, LAM_Ne,De)` 로 쓰면:

```
Q_Ne,start = −b
Q_Ne,end   = N(1 − c − d) − b
Q_Pe,start = −cN − l
Q_Pe,end   = 1 − a − b − cN − l
```

**5개 미지수 → 4개 좌표.** 등식 제약이 하나도 없으므로 **최소 1차원의 정확한
null 이 구조적으로 존재한다.**

### 5.2 관측이 「길이」라서 null 이 하나 더 늘어난다

평탄역 길이는 Ah 축 위의 **차이**다. 즉 네 좌표를 통째로 평행이동해도 관측은
변하지 않는다. 관측 가능한 것은 (평행이동 불변량)

```
D1 = Q_Ne,end − Q_Ne,start = N(1 − c − d)
D2 = Q_Pe,start − Q_Ne,start = −cN − l + b
D3 = Q_Pe,end − Q_Ne,start = 1 − a − cN − l
```

**3개 관측, 5개 미지수 → null 2차원.** `[재현]` 수치로 Jacobian rank 를 확인했다:
평행이동 불변 관측 `(D1,D2,D3)` 에 대해 **rank 3**, 원 창 좌표 4개에 대해
**rank 4**.

### 5.3 두 null 방향 (닫힌 형태)

`(ΔLLI, ΔLAM_Pe,Li, ΔLAM_Pe,De, ΔLAM_Ne,Li, ΔLAM_Ne,De)` 좌표에서:

```
n₁ = ( −N ,  0 ,  0 , +1 , −1 )
n₂ = ( +1 , −1 , +1 ,  0 ,  0 )
```

말로 옮기면:

> **n₁** — 음극 활물질 손실을 `리튬화 상태` 에서 `탈리튬화 상태` 로 δ 만큼
> 옮기고 동시에 `LLI` 를 `N·δ` 만큼 늘리면, **네 창 좌표와 총용량이 전부
> 그대로다.** 즉 `{LAM_Ne,Li = δ, LLI = l}` ≡ `{LAM_Ne,De = δ, LLI = l + N·δ}`.
>
> **n₂** — 양극 활물질 손실을 `리튬화` 에서 `탈리튬화` 로 ε 만큼 옮기고 동시에
> `LLI` 를 ε 만큼 **줄이면** 마찬가지로 전부 그대로다.

`[재현]` 수치 검증 (`N = 1.15`, 기준점 `(l,a,b,c,d) = (0.10, 0.02, 0.03, 0.04,
0.05)`, `δ = ε = 0.017`): 두 방향 모두 `(D1,D2,D3)` 변화 **정확히 0**,
식 (8) 의 총용량 변화 **정확히 0**.

### 5.4 ★ 이것이 Birkl 의 몫공간과 **같은 것**임을 확인했다

Birkl 2017 §4.2 는 축퇴를 말로 진술하고 **`[total-LLI, LAM_PE, LAM_NE]`** 라는
3-파라미터 좌표로 옮겨 우회한다. 그 좌표는

```
total-LLI = LLI + LAM_Ne,Li·N + LAM_Pe,Li·1     (잃은 리튬화 활물질 속 리튬 포함)
LAM_PE    = LAM_Pe,Li + LAM_Pe,De
LAM_NE    = LAM_Ne,Li + LAM_Ne,De
```

`[재현]` 위 두 null 방향을 이 세 좌표에 넣으면:
- `n₁`: Δtotal-LLI = −N + N·1 + 0 = **0**, ΔLAM_PE = **0**, ΔLAM_NE = 1−1 = **0**
- `n₂`: Δtotal-LLI = +1 + 0 + 1·(−1) = **0**, ΔLAM_PE = −1+1 = **0**, ΔLAM_NE = **0**

> **`[해석]` Birkl 의 3-파라미터 좌표는 정확히 Marongiu 식 (2)–(5) 의 몫공간
> `ℝ⁵ / span{n₁, n₂}` 다.** 5 − 2 = 3 이 맞고, 두 논문(같은 해, 서로 인용 관계
> 있음)이 **같은 대상의 두 표현**임이 이제 확인됐다. Birkl 은 그것을 산문으로
> 진술했고, Marongiu 는 식으로 인쇄했으며, **어느 쪽도 그 방향을 계산해 보이지
> 않았다.**

### 5.5 왜 이것이 우리에게 값진가

`[해석]` 세 가지다.

1. **닫힌 형태 축퇴가 하나 더 확보됐다.** 지금까지 이 위키가 쥐고 있던 것은
   Lin & Khoo 의 `(1−LLI, 1−LAM_NE, 1−LAM_PE)` 스칼라배 방향 하나와
   Dubarry 의 `{LAM_liNE = x} ≡ {LAM_deNE = x, LLI = LR·x}` 였다. **후자가
   여기 `n₁` 이고, `n₂` 는 그 양극 판이며, 위키가 아직 등록하지 않은 것이다.**
   둘 다 **격자에 truth 쌍으로 심어 직접 시험할 수 있다** (수치로 찾은 방향과
   검증력이 다르다).
2. **"용량은 맞는데 모드는 모른다" 가 정리로 증명된다.** 식 (8) 의 총용량이
   `n₁, n₂` 를 따라 **정확히 불변**이므로, 이 논문의 헤드라인(용량 오차 ≈ 1 %)은
   **모드 식별 가능성에 대해 원리적으로 아무 말도 하지 않는다.** 저자들이
   "out of the goal of this work" 라고 적은 것이 **수학적으로 옳다.**
   `[해석]` 이 계보에서 처음으로 **성공 지표와 우리 질문이 직교한다는 것이
   증명 가능한 사례**다. 후속 인용자가 "Marongiu 가 half-cell 로 모드를 뽑았다"
   고 쓰면 안 되는 이유이기도 하다.
3. **우리 좌표는 이 null 을 물려받지 않는다.** 우리는 4개 창 좌표를 직접
   맞추고 모드 층을 만들지 않으므로 `ℝ⁵ → ℝ⁴` 사상 자체가 없다. 대신 사후
   변환(`LAM_PE = 1 − α_PE·r` 등)이 **몫공간으로의 사영**이다. **즉 우리 출력도
   Birkl/Marongiu 와 같은 몫공간의 값이며, 그 위에서 다시 축퇴가 있느냐가
   22p 카드의 질문이다.** 두 층을 섞으면 안 된다.

### 5.6 ⚠ 범위 한정

- 이 계산은 **모델(식 2–5)의 성질**이지 데이터의 성질이 아니다. 관측이
  평탄역 길이라는 가정과 반쪽전지 곡선이 노화 불변이라는 가정 위에 있다.
- **`N` 의 값이 논문에 없으므로** `n₁` 의 계수는 기호로만 안다 (§1 ①).
- 이 논문의 실제 실행은 `a = b = c = 0` 이므로 **두 null 이 모두 잘려 있다.**
  즉 이 축퇴는 **논문의 결과를 무효화하지 않는다** — 논문의 결과가 무엇에
  대한 것인지를 정확히 한정할 뿐이다.

---

## 6. 알고리즘 (§3, p.161–163)

### 6.1 BMS 구조 — 온라인/오프라인 분할 (Fig. 2)

`[도표, Fig. 2]` 왼쪽 파란 블록 **Online Estimation**: (a) 충전 중 평탄역 추정,
(b) 주행 중 평탄역 추정 (EECM 으로 OCV 추적) → **Information Pre-processing**
(표준 조건으로 환산) → **Save**.
오른쪽 초록 블록 **Not Real-time Calculation**: 상단에
`Q_cath = f(LLI, LAM_Ne, LAM_Pe)`, `Q_anod = f(LLI, LAM_Ne, LAM_Pe)`,
`Q_full = f(Q_cath, Q_anod)` 세 식이 박스로 들어가 있고, 그 아래
**Offline plateaus detection** ↔ **DMs detection** 루프, 그리고 결과를 받는
**Hysteresis Recalibration**.

`[해석]` **이 그림의 식 표기가 파라미터 3개** (`LLI, LAM_Ne, LAM_Pe`) 다 —
모델의 5개도, 실행의 2개도 아니다 (§10 ②).

### 6.2 반복 루프 (Fig. 3)

`[도표, Fig. 3]` 순서도를 그대로 옮기면:
```
Start
 → a) Generation of P_i = [LLI; LAM_Pe; LAM_Ne]
 → b) Modification of anode/cathode curve   ← c) Electrode curve fresh cell
 → Calculation of V_cell = V_cathode − V_anode
 → e) Detection of plateaus in V_cell
 → f) Err = Σᵢ₌₁ⁿ ΔL_i                      ← g) Plateau characteristics detected online
 → h) Err ≤ ε ?   아니오 → a) 로 복귀 / 예 → i) Calculate battery capacity → End
```

`[인쇄, p.161]` 같은 절차의 산문판이 §3 에 있고 단계 라벨이 일치한다.

**★ 여기서 목적함수가 본문과 어긋난다** (§10 ③): 순서도 f) 는 **합(Σ)** 인데
본문 식 (9) 는 **최대(max)** 다.

### 6.3 목적함수 — 식 (9)

`[인쇄, p.163]`
```
Error_actual = max( L_Pi,measured − L_Pi,fitted ) ,   i = 1, 2, 3           … (9)
```
> "where L_Pi represents **the length of the ith plateau expressed in Ah**. In
> this way it is not necessary to gather the information relative to all the
> existing plateaus online. The algorithm will proceed in order to minimize the
> single error related to the available plateaus (the one measured online)."

`[해석]` **관측 공간이 우리와 근본적으로 다르다.**
- 우리 / Birkl / Navidi: 전압 잔차 (곡선 위 수백 점) → `L²`
- Marongiu: 평탄역 길이 **최대 3개 스칼라**, 단위는 **Ah**, 노름은 **`L^∞`**

`[해석]` `L^∞` 노름은 미분 불가능한 점이 많아 좌표 하강류 알고리즘이 잘
멈춘다. §4.2.1 이 서술하는 "closed loop" 현상(§8.4)이 정확히 그 증상으로 읽힌다
— 논문은 이 연결을 하지 않는다.

`[인쇄, p.163]` 평탄역 길이 자체의 검출 방법:
> "The lengths of plateaus **VA and IIA** are estimated by saving the data in a
> vector of limited length and **fitting the data with linear function with
> constrained dependency**, as explained in Ref. [33]. The beginning and end of a
> plateau is determined by fixing the pendency of the respective fitting linear
> function during the recalibration process of the algorithm. The length of the
> plateau **IA**, however, is estimated by **fitting of the data with a so called
> sigmoid function** [34], by using the **Nelder-Mead** method [35]. This allows
> the correct identification of the precise point where the single phase region
> is placed. In fact, in this region **the growth of the battery's internal
> resistance can create some difficulties**, and can deliver imprecise
> information in terms of plateaus lengths."

`[해석]` **관측 자체가 이미 하나의 적합 결과다.** 평탄역 길이는 측정값이 아니라
"직선/시그모이드를 맞춰 얻은 끝점" 이며, 그 적합의 불확실성은 어디에도 없다.
그리고 **IA 는 내부저항 성장에 오염된다**고 저자가 적는다 — 즉 이 관측은
순수 열역학이 아니라 **동역학이 섞인 관측**이다.

### 6.4 최적화 — VPA 와 블록 교대 규칙

`[인쇄, p.162]` 알고리즘 이름: **varied parameter approach (VPA)**, Waag [31,32]
에서 가져와 수정.

`[인쇄, p.164]` **갱신 규칙이 좌표 블록 교대다**:
> "The fitting algorithm proceeds **tracking only one of the degradation
> mechanisms per time** based on the actual error. In detail, **if the actual
> error is relative to the plateaus VA or IIA, then only the LAM_Ne,De is
> changed, while in case of plateau IA only the LLI is changed.**"

`[인쇄, p.164]` 2단계 구조 + 강제 수렴:
> "the tracking process takes place in two steps. In the first step the two modes
> are adjusted following the aforementioned rule … The second step takes place
> when the sum of the actual single plateau errors is below a defined threshold.
> As the method is approaching the found minima (global or local), the generation
> of the new parameter set P_i occurs with **smaller interval** … Moreover, once
> the stop criteria is not yet satisfied and the error is still considerable but
> constant for a certain number of iterations, **to force the convergence the
> single degradation mechanisms are forced to change with a value proportional
> to the actual error.**"

`[인쇄, Table 2, p.165]` VPA 파라미터:

| 이름 | 값 | 뜻 |
|---|---|---|
| `k_var(LLI)` 1단계 | **0.4** | `LLI·(1 ± k_var)` 로 새 파라미터 집합 생성 |
| `k_var(LAM)` 1단계 | **0.5** | `LAM·(1 ± k_var)` |
| `ε_threshold` | **0.3 Ah** | 이 값 아래여야 2단계 진입 |
| `k_var(LLI)` 2단계 | **0.1** | |
| `k_var(LAM)` 2단계 | **0.1** | |
| `ε_total` | **0.1 Ah** (충전) / **0.01 Ah** (방전) | 종료 임계 |
| `It_max` | **100** | 최대 반복 |
| `It_same` | **20** | `ε_total` 이 변하지 않는 최대 반복 |

`[해석]` 이 표가 이 논문에서 우리 절차와 가장 직접 비교되는 자리다:
- **경계(lb/ub) 가 없다.** `LLI·(1 ± k_var)` 라는 **곱셈 갱신**이라 `LLI = 0`
  에서 출발하면 영원히 0 이다 — 그래서 `LAM_start = 0 %` 시나리오가 실패한다
  (§8.3). `[해석]` 이 인과는 논문이 명시하지 않지만 갱신식에서 바로 따라온다.
- **multi-start 가 없다.** 시작점 1개, 예산 100 반복. Birkl 은 `fmincon` +
  MultiStart 100회, Navidi 는 서로 다른 초기값 5회. **이 논문이 가장 적다.**
- **블록 교대**는 Navidi 부록 A1 의 수동 절차(`(m_n,δ_n)` → `(m_p,δ_p)`) 와
  **같은 발상**이다. 두 논문이 서로 독립적으로 같은 처방에 도달했다.
  `[해석]` 22p 카드 2026-09-03 (14) 항목이 "블록 교대 최적화" 를 후속 실험으로
  올려 뒀는데, **그 실험에 선례가 둘이 됐다.**

### 6.5 반쪽전지 곡선의 출처

`[인쇄, p.162]`
> "The two electrode voltage curves available at step c) have to be measured on a
> sample **at the beginning of life**. … a pristine cell was disassembled in a
> glove box under argon atmosphere and **16 mm diameter samples** of cathode and
> anode electrodes were collected. Then coin cells were built and the single
> anode and cathode voltages were measured **relative to a lithium reference
> electrode** during charge and discharge. **The current used in the coin cell
> was scaled to the full cell's total electrode surface in order to get the same
> overvoltage effect.** Moreover, this process allows finding the offset relative
> to a cell in a fresh state indicated in Fig. 1a)."

`[해석]` Cui 2024 와 같은 계열(해체 전극 실측 반쪽전지)이고 Rhyu 2025 의
범용 OCV 다항식보다 직접적이다. **다만 pristine 1개 셀뿐이고 반복 측정이 없다**
— Cui 의 SI Table S3 같은 재현성 자료가 없다. 그리고 `[해석]` "같은 과전압
효과를 얻기 위해 전류를 면적으로 스케일" 은 곧 **이 반쪽전지 곡선이 OCP 가
아니라 유한 전류 곡선**이라는 뜻이다.

---

## 7. 데이터셋 (§4, p.163)

`[인쇄]` 셀: **원통형 고출력 LFP/graphite, 공칭 8 Ah.** 표준 용량 정의는
**0.1C 정전류, 23 °C**.

`[인쇄, Table 1]` 검증에 쓴 **7개 노화셀 + 신선셀 1개**:

| 셀 이름 | 노화 조건 | 실제 SoH / % |
|---|---|---|
| Fresh | 신선 | 100 |
| L40C50 | 달력노화, 40 °C, SoC 50 % | **85.78** |
| L50C20 | 달력노화, 50 °C, SoC 20 % | **82.30** |
| L50C50 | 달력노화, 50 °C, SoC 50 % | **76.77** |
| Z01C10 | 사이클, 1C, SoC 45–55 % (span 10 %), 30 °C | **81.53** |
| Z01C50 | 사이클, 1C, SoC 25–75 % (span 50 %), 30 °C | **88.91** |
| Z01C80 | 사이클, 1C, SoC 10–90 % (span 80 %), 30 °C | **84.15** |
| Z06C10 | 사이클, **6C**, SoC 45–55 % (span 10 %), 30 °C | **83.47** |

`[인쇄, Table 1 각주]` SoH 정의:
> "The value of the SoH is defined as the ratio between the value of the total
> actual capacity measured with **0.1C constant current discharge** and the value
> of the same capacity for the fresh cell in the same condition."

`[인쇄, p.163]` 검증 목표:
> "The main goal is to test if the algorithm is able to detect the battery
> capacity **even though the aging conditions (and therefore the different aging
> mechanisms) may be different and unknown**."

`[해석]` **정답 축이 용량 하나뿐이다.** SoH 는 0.1C 방전 용량비이므로
**독립적으로 측정된 것**이고 (그 점은 Birkl 의 제작 설계값보다 낫다), 대신
**모드의 정답은 없다.** 열화 조건이 달력/사이클/고율로 갈리므로 모드 조성이
셀마다 다를 것이라는 기대는 있지만 확인되지 않는다.

`[해석]` 셀 수 7개, 모두 SoH 77–89 % 구간. **저열화 영역(SoH 95 % 이상)의
셀이 하나도 없다** — 신호가 작을 때 어떻게 되는지 알 수 없다.

---

## 8. 결과 — 그림별 (§4, p.163–167)

### 8.1 Fig. 5 — 주행 중 평탄역 검출 (내가 본 그림)

`[도표, Fig. 5]`
- a) FTP75 반복 주행의 전류 프로파일, **±15 A** 범위, 3.1 시간. 8 Ah 셀이므로
  피크가 ≈ **1.9C**.
- b) y축이 **3.15 – 3.35 V** 다 — **LFP 전 사용구간의 전압 폭이 200 mV 밖에
  안 된다** (x축 0–7 Ah). 곡선 넷: quasi-OCV 0.1C(적, 실선), Tracked OCV(청,
  점선, EECM 추정), Tracked and filtered OCV(녹, 일점쇄선), Measured OCV(갈색
  ×, GITT).
- `[도표]` **추적 OCV(청)가 quasi-OCV 대비 ±20~30 mV 로 흔들린다.**
- `[도표]` **GITT 측정 OCV(갈색 ×)가 quasi-OCV 보다 중간 구간에서 30~40 mV
  높다** — 히스테리시스 + 과전압. 본문은 이 격차를 논하지 않는다.
- `[도표]` 평탄역 끝점 마커: quasi-OCV 기준(적 사각) ≈ **1.65 Ah, 3.95 Ah**;
  추적 OCV 기준(녹 원) ≈ **1.55 Ah, 3.8 Ah**. **차이 ≈ 0.10–0.15 Ah.**

`[인쇄, p.164]`
> "it is possible to correctly estimate the length of the single plateaus … 
> **without precisely tracking the OCV**. … Nevertheless, even if affected by
> negligible errors, the different two-phase transitions, and therefore the
> plateaus' lengths can still be clearly identified."

`[해석]` **본문 서술과 그림이 어긋나는 첫 지점.** 그림에서 읽은 평탄역 끝점
차이 0.10–0.15 Ah 는 Fig. 6d 의 수렴 잔차(0.02–0.05 Ah)의 **2~7배**이고,
방전 종료 임계 `ε_total = 0.01 Ah` 의 **10~15배**다. "negligible errors" 라는
표현이 자기 임계값과 맞지 않는다. 저자는 이 문제를 **평균화로 넘긴다**:
`[인쇄]` "can be limited by collecting plateaus' information in subsequent
driving cycles and **averaging them**, together with a plausibility analysis" —
그 평균화가 실제로 얼마나 줄이는지는 인쇄되지 않았다.

### 8.2 Fig. 4 — 조건 환산 회귀 (내가 본 그림)

`[도표, Fig. 4]` 두 패널 모두 x축이 표준 조건, y축이 다른 조건에서 잰 같은
평탄역 길이. **각 회귀에 점이 4개뿐**이다.

| 패널 | 평탄역 | 조건 | 회귀식 (`[도표]` 그림 안 인쇄) | R² |
|---|---|---|---|---|
| a | IIA | 0.05C vs 0.1C | `y = 0.865x + 0.5536` | **0.9454** |
| a | IIA | 0.2C vs 0.1C | `y = 0.9945x − 0.1697` | **0.9285** |
| b | IA | 10 °C vs 23 °C | `y = 0.8113x + 0.5212` | **0.9643** |
| b | IA | 40 °C vs 23 °C | `y = 0.9529x − 0.0471` | **0.9485** |

`[해석]` **이 그림이 오차예산의 숨은 바닥이다.** 패널 a 에서 x ≈ 2.57 Ah 인
두 셀의 0.05C 값이 **2.69 Ah 와 2.77 Ah** 로 갈린다 — 같은 x 에 대해
**0.08 Ah 의 산포**. 그런데 Fig. 6d 의 수렴 잔차는 0.02–0.05 Ah 다. 즉
**적합 잔차가 관측 환산의 산포보다 작다** — 적합이 관측 정밀도 이하로 내려간
상태이고, 그 아래에서 얻은 모드 값에는 의미를 붙일 수 없다.
`[해석]` 이것은 Schaeffer 2024 의 "낮은 잔차 ⇒ 참에 가깝다 는 거짓" 과 같은
계열의 논증이며, 이 논문에서 **관측 쪽에서** 성립하는 형태다. 논문은 이 대조를
하지 않는다.

`[인쇄, p.163]` 저자의 결론은 관대하다:
> "in both cases it is possible to find a **nearly linear relationship** between
> the plateaus measured in standard conditions and the plateaus measured in
> different conditions."

### 8.3 Fig. 7 + Table 3–5 — 용량 추정 오차 (내가 본 그림)

`[도표, Fig. 7]` 두 패널(a 충전, b 방전) 각각 막대 4개. 막대 = Table 5 의
평균, **점선 수염 = ±STD** (예: 충전 3평탄역 막대 0.98 에 수염이 ≈0.26–1.70 →
±0.72 = Table 5 의 STD 와 일치).

`[인쇄, Table 3, p.166]` 셀별 충전 오차 / %:

| 셀 | 3 평탄역 | 2 평탄역 | 1 평탄역 (LAM_start=10 %) | 1 평탄역 (LAM_start=0 %) |
|---|---|---|---|---|
| L40C50 | 0.76 | 1.01 | 6.28 | 16.49 |
| L50C20 | 1.10 | 0.74 | 10.85 | 21.50 |
| L50C50 | **2.66** | **0.39** | 1.70 | 10.90 |
| Z01C10 | 0.61 | 1.64 | 6.29 | 14.83 |
| Z01C50 | 0.51 | 0.34 | 5.06 | 4.06 |
| Z01C80 | 0.77 | 0.13 | 4.89 | 14.44 |
| Z06C10 | 0.42 | 1.20 | 9.59 | 19.02 |

`[인쇄, Table 4, p.166]` 셀별 방전 오차 / %:

| 셀 | 3 평탄역 | 2 평탄역 | 1 평탄역 (10 %) | 1 평탄역 (0 %) |
|---|---|---|---|---|
| L40C50 | 0.93 | 0.70 | 5.74 | 15.76 |
| L50C20 | 0.23 | 0.06 | 6.41 | 19.11 |
| L50C50 | 1.26 | 1.26 | 3.86 | 14.15 |
| Z01C10 | 0.82 | 0.25 | 0.22 | 9.70 |
| Z01C50 | 0.87 | 0.32 | 6.74 | 1.96 |
| Z01C80 | **2.71** | 0.64 | 2.95 | 12.72 |
| Z06C10 | 0.91 | 1.69 | 4.39 | 14.17 |

`[인쇄, 식 10, p.166]` 오차 정의: `Error_capacity = (Q_real − Q_calc)/Q_real`.

**★★ 초기값 의존성 — 이 논문에서 우리에게 가장 값진 실험.**
`[인쇄, p.166]`
> "if only one of the plateaus is known (namely IA), the error in the estimation
> of the capacity increases dramatically reaching a value of 6.38% (charge) and
> 4.33% (discharge) **when LAM_Ne has a starting value of 10%**, and a value of
> 14.46% (charge) and 12.51% (discharge) **when LAM_Ne has a starting value of
> 0%**. … **The evident highest error in the second case is related to the
> smaller initial value of the LAM_Ne which is kept for the final calculation of
> the battery capacity due to the lack of information to track this mechanism.**"

`[해석]` **관측을 줄이자 초기값이 답을 지배한다.** 같은 데이터·같은 알고리즘에서
초기값 하나를 10 % → 0 % 로 바꾸면 **용량 오차가 2.3~2.9배**가 된다. 그리고
저자 자신의 설명이 정확히 우리 어휘로 번역된다 — "데이터가 그 방향을 말하지
않으므로(`lack of information to track this mechanism`) 초기값이 그대로 남는다".
이것은 [[nullspace-coefficient-interpretation]] 의 **"축퇴 방향 위의 값은
데이터가 아니라 정칙화(여기서는 초기값)가 정한다"** 의 **야생 실측**이며,
이 계보에서 그 명제가 **관측 개수를 통제한 대조군과 함께** 나타난 첫 사례다.

`[해석]` 그리고 §6.4 의 곱셈 갱신 `LAM·(1 ± k_var)` 때문에 `LAM_start = 0 %`
는 **수학적으로 갇힌 초기값**이다 (0에서 못 벗어난다). 논문은 이 인과를 적지
않는다.

### 8.4 ★ 정보를 늘렸더니 나빠졌다 (§4.2.1, p.166)

`[인쇄]`
> "one would expect that the knowledge of more information (namely all three
> plateaus' lengths) would deliver a more precise value of the battery capacity.
> This is valid as a general rule … However, **in two cases the error for the
> first scenario rises to 2.66% for the charge process and 2.71% for the
> discharge process**, generating therefore a higher standard deviation. This
> trend can be explained with the fact that **the knowledge of all three plateaus
> can create some problems in the algorithm's convergence.** … it can happen that
> **the change of one of the degradation modes can generate a reduction of the
> error related to a single plateau but the increase of the other ones.**
> Therefore following this process **the algorithm can enter a closed loop and
> converge to an imprecise solution.** On the contrary, the knowledge of only two
> plateaus assures the reduction of the global error in a more efficient manner
> and **guarantees a faster convergence to more precise solutions.**"

그 원인의 물리적 근거로 **관측 중복**을 든다:
> `[인쇄, p.166]` "These result from the characteristics of the anode curve. So it
> happens that **if during the battery lifetime the length of one of the two
> plateaus decreases, the other one will decrease proportionally.¹** Therefore
> **the knowledge of only plateau IIA is sufficient** to correctly estimate and
> track the degradation modes."
>
> `[인쇄, 각주 1]` "This assumption is valid in case LAM_Pe does not take place
> during the battery lifetime, therefore LLI and LAM_Ne can be considered as the
> dominant mechanisms."

`[해석]` **이것이 관측 공간의 축퇴다.** 평탄역 VA 와 IIA 가 비례하므로
**관측 3개의 유효 rank 는 2**이고, 미지수도 2개다. 남는 3번째 관측은 정보가
아니라 **잡음 채널**이며, `L^∞` 목적함수 아래에서는 그 잡음이 최대값을 지배해
수렴을 방해한다.

`[해석]` **우리 dQ/dV 결과와의 관계 — 조심해서 읽어야 한다.**
2026-08-20 실측에서 dQ/dV 항을 더한 목적함수가 더 나빴다(protocol 조건부).
[[np-lip-ocv-reparametrization]] 의 점검 B2 는 그것을 "dQ/dV 는 같은 곡선의
함수이므로 자유도를 못 늘린다" 로 설명한다. **이 논문은 다른 메커니즘을 준다**:
중복 관측이 자유도를 못 늘리는 데 그치지 않고 **최적화를 적극적으로 방해한다**.
두 설명은 배타적이지 않고, **구별 가능하다** — 전자는 정보 상한(잔차 지형),
후자는 수렴 경로다. 우리는 참값을 알고 목적함수 값을 저장하므로
[[fitting-degeneracy]] 의 flat valley ↔ multimodal 구분으로 **갈라낼 수 있다.**
⚠ 다만 이 논문의 목적함수는 `L^∞` 이고 우리는 `L²` 이므로, **메커니즘을 그대로
옮길 수 없다.** 가설로만 등재한다.

### 8.5 Fig. 8 — 히스테리시스 재보정 (내가 본 그림) ★ mV 수치가 나오는 유일한 곳

`[도표, Fig. 8]` 네 패널:
- a) 신선셀(청 원, 점선) vs 노화셀(적 마름모, 실선)의 OCV 히스테리시스
  (충전 상단 / 방전 하단 두 가지 branch). **y축 3.15–3.34 V, x축 SoC 10–90 %.**
- b) 재보정 후: 노화셀 실측(적) vs 재보정된 곡선(녹 사각). 두 곡선이 거의 겹친다.
- c) 재보정 **전** 신선-노화 전압차, 충전(청)/방전(적갈) 막대, y축 0–0.04 V.
- d) 재보정 **후** 같은 막대.

`[도표]` c) 에서 읽은 값:
- SoC 20–30 %: 최대 ≈ **0.032 V** (충전, SoC 25 %), ≈ 0.025 V (방전)
- SoC 75–85 %: 최대 ≈ **0.038 V** (방전, SoC 75 %), ≈ 0.034 V (충전)
- **SoC 45–65 %: ≈ 0.001–0.003 V** — 사실상 0

`[도표]` d) 에서 읽은 값: 최대 ≈ **0.022 V** (SoC 10 %, 방전), 그다음
≈ 0.017 V (SoC 20 %, 충전); **나머지 대부분 ≲ 0.012 V**, 중간 구간 ≲ 0.005 V.

`[인쇄, p.167]`
> "the recalibration process **reduces the error to 20 mV** for almost the entire
> SoC range, especially in the high and low SoC range, for both charge and
> discharge. **This again validates the presented method and assures correctness
> of the tracked aging mechanisms.**"

`[해석]` 두 가지를 적어야 한다.
1. **"assures correctness of the tracked aging mechanisms" 는 과한 주장이다.**
   재보정은 §5 에서 보인 몫공간 위의 양(창 좌표)만 쓰므로, 두 null 방향 위의
   어떤 값을 골랐든 **똑같은 재보정 결과를 낸다.** 즉 이 검증은 모드의
   correctness 에 대해 원리적으로 무감하다. 저자 자신이 §4.2.1 에서 "out of the
   goal" 이라고 적은 것과 **모순되는 문장**이다 (§10 ⑤).
2. **그러나 그림 c) 는 우리에게 매우 값진 수치를 준다** — Q5 참조. LFP 에서
   SoH 100 → 77~89 % 의 열화가 **중간 SoC 대역에 1–3 mV 밖에 남기지 않는다.**

### 8.6 Fig. 6 — 반복 궤적 (내가 본 그림)

`[도표, Fig. 6]` 4단 패널, x축 `N iterations` 0–100.
- a) `LLI / %`: **17.5 % 에서 출발** → 반복 22 근처에서 9.6 % 까지 급락 후 진동
  → 12 % 부근 → 반복 ~47 에서 13.2 로 올랐다가 → **최종 12.97 %** (범례 인쇄).
- b) `LAM_Ne,De / %`: **30 % 에서 출발** → 반복 3에서 15 % 로 급락 → 16.5 %
  →  18.5 → 17.7 → **최종 19.23 %** (범례 인쇄).
- c) `Error / Ah`: 0.88 → 0.57 → 0.66 → 반복 21 에서 0.25 로 → 0.1 부근에서
  진동 → **최종 0.1255 Ah** (범례 인쇄).
- d) `Δ_L / Ah` 셋: **Δ_L1 = 0.0531 · Δ_L2 = 0.0517 · Δ_L3 = 0.0206 Ah**
  (범례 인쇄). 캡션: `[인쇄]` "where L1/VA and L3/IA".

`[해석]` **이 그림에서 읽히는 것 넷:**

1. **c) 의 "총 오차" 는 식 (9) 의 max 가 아니라 합이다.**
   `0.0531 + 0.0517 + 0.0206 = 0.1254 ≈ 0.1255`. max 라면 0.0531 이어야 한다.
   → Fig. 3 의 `Err = Σ ΔL_i` 와 일치하고 **식 (9) 와 어긋난다** (§10 ③).
2. **이 예시 실행은 정지 임계를 만족하지 못했다.** 최종 0.1255 Ah >
   `ε_total = 0.1 Ah`(충전). 즉 `It_max = 100` 으로 **소진 종료**했다.
   그런데 c) 를 보면 오차가 반복 **62 부터 100 까지 평평**하다 — 38 반복 동안
   변화가 없으므로 `It_same = 20` 규칙이면 **반복 ~82 에서 멈췄어야** 한다.
   `[해석]` 규칙과 그림이 맞지 않는다. 그림이 100까지 그린 것뿐일 수도 있으나,
   **어느 쪽이든 이 예시는 "수렴했다" 가 아니라 "예산을 다 썼다" 이다.**
3. **파라미터 궤적이 매끄럽지 않다.** LLI 가 9.6 → 13.4 → 11.9 → 13.2 → 12.97
   로 왕복하고, LAM 도 30 → 15 → 18.5 → 16.5 → 19.23 으로 왕복한다.
   `[해석]` 블록 교대 + `L^∞`/합 목적함수의 전형적 지그재그이며, §8.4 의
   "closed loop" 서술과 같은 현상으로 읽힌다.
4. **초기값이 그림에서만 읽힌다** (LLI 17.5 %, LAM 30 %). 본문에 없다.
   `[해석]` 그 초기값 자체가 이미 최종값(12.97/19.23) 근처이므로, 이 예시는
   **warm start** 에 가깝다. 초기값을 어떻게 얻는지가 인쇄되지 않았으므로
   재현 불가다.

### 8.7 안 본 그림

- `fig_2.png` (BMS 구조도) — **봤다** (§6.1). 수치가 없는 블록도지만
  파라미터 개수 표기(3개)를 확인하려고 열었다.
- 표 5장(`tab_*.png`) — **이미지로는 안 봤다.** PDF 텍스트 추출이 완전하고
  숫자가 정확히 나왔으므로 (Table 1–5 전부 위에 옮겼다) 이미지 판독이 불필요.
  단 Table 3·4 는 `[인쇄]` "The maximum and minimum errors are **highlighted in
  red and green**" 이라 하는데 **텍스트에는 색 정보가 없다** — 어느 셀이
  최대/최소인지는 숫자에서 직접 판정했다(굵게 표시).

---

## 9. 어휘 전수 (이 계보 열세 편째)

본문 **50,127자** (참고문헌 제외, 합자 `ﬁ`/`ﬂ` 정규화 후):

| 용어 | 횟수 |
|---|---|
| `identifiab*` | **0** |
| `degenerac*` | **0** |
| `non-unique` / `uniqueness` / `uniqu*` | **0 / 0 / 0** |
| `nullspace` / `null space` | **0 / 0** |
| `collinear*` | **0** |
| `ill-posed` / `ill-conditioned` | **0 / 0** |
| `cross-valid*` | **0** |
| `uncertaint*` | **0** |
| `error bar` | **0** |
| `confidence` | **0** |
| `Fisher` / `Hessian` / `condition number` / `singular value` | **0 / 0 / 0 / 0** |
| `sensitivit*` | **0** |
| `half-cell` | **5** (제목·키워드·본문) |
| `LLI` | **23** |
| `LAM` | **47** |
| `plateau` | **97** |
| `noise` | **2** (둘 다 "미분이 잡음을 증폭한다" 한 문장) |
| `mV` | **1** (히스테리시스 재보정 결과) |
| `minima` | **1** ("global or local") |
| `converg*` | **7** |
| `standard deviation` | **5** |
| `correlation` | **3** (전부 Fig. 4 의 조건 환산) |
| `post-mortem` | **1** (남의 문헌을 가정의 근거로) |
| `assumption` | **5** |

`[해석]` **열세 편째의 형태 — "어휘도 없고 개념도 없는데, 결론은 정직하다".**
- 아홉 편: 어휘가 아예 없다 (Dubarry, Birkl, Tao …)
- 열 편째 Lin & Khoo: 추정 정밀도 어휘는 갖췄지만 비유일성 어휘는 없다
- 열한 편째 Schaeffer: 개념을 정면으로 다루면서 자기 어휘를 새로 만든다
- 열두 편째 Navidi: 불확실성 어휘 21회, **전부 출력 쪽**
- **열세 편째(이 논문)**: 어휘 **전무**. 그러나 **자기 방법이 모드를 물리적으로
  결정하지 못한다는 것을 명시적으로 선언하고 목표에서 뺀다** (`[인쇄]` "out of
  the goal of this work"). `[해석]` **어휘가 없는 것과 주장을 절제하는 것은
  다른 축이다.** 이 논문은 어휘가 0인데도 이 계보에서 **과대주장이 가장 적은
  축에 속한다** — Fig. 8 의 "assures correctness" 한 문장만 빼면.

---

## 10. 원문 안의 불일치 목록 (인용 전 확인 필요)

① **식 (4) 와 Fig. 1a 가 BOL 에서 어긋난다.** 식 (4) 는 모든 모드가 0일 때
`Q_Pe,start = 0` 을 주는데, 본문은 `[인쇄]` "Q_Pe,start is smaller than zero,
with a value depending on the initial offset" 이고 Fig. 1a 도 그렇게 그린다.
`[해석]` 초기 offset 을 "BOL 에 이미 존재하는 LLI" 로 흡수해 읽으면 무모순이
되지만(본문도 `[인쇄]` "The LLI is also one of the causes of the initial
offset" 라고 적는다), 그러면 **추정된 `LLI` 는 노화분이 아니라 절대 offset** 이
된다. 논문은 이 구분을 하지 않는다. **`LLI` 값을 인용할 때 기준점이 불명확하다.**

② **파라미터 개수가 세 번 다르다.** 모델 **5** (식 2–5) / 알고리즘 서술과
Fig. 2·Fig. 3 **3** (`P_i = [LLI; LAM_Pe; LAM_Ne]`) / 실제 실행 **2**
(§4.2.1: `LAM_Pe,Li = LAM_Pe,De = LAM_Ne,Li = 0`).

③ **목적함수가 본문과 그림에서 다르다.** 식 (9) = `max`, Fig. 3 f) = `Σ`.
`[재현]` Fig. 6 의 숫자(0.0531+0.0517+0.0206 = 0.1254 vs 표시된 0.1255)가
**합 쪽을 지지한다.** 즉 **식 (9) 가 실제 구현과 다를 가능성이 높다.**
어느 쪽인지는 축퇴·수렴 논의에 영향이 크므로 (§8.4), **이 논문의 목적함수를
인용할 때 반드시 이 불일치를 같이 적어야 한다.**

④ **[22] 를 기각한 근거를 자기가 지키지 않는다.** §1 에서 [22] Wang 2014 를
`[인쇄]` "based on the assumption that the electrode characteristics do not
change during battery lifetime, an assumption which **cannot be made for LFP
cells** [17]" 라고 기각하는데, §3 의 자기 절차는 **BOL 반쪽전지 곡선을 고정하고
창만 움직인다** — 같은 가정이다. `[해석]` 차이는 "곡선 형상 불변" 대신 "평탄역
길이만 쓴다" 로 의존을 줄인 것이지 가정을 버린 것이 아니다. 논문은 이 해명을
하지 않는다.

⑤ **§4.2.1 과 §4.2.2 가 서로 모순된다.** 전자는 `[인쇄]` "The correct
determination of all the degradation mechanisms … **is out of the goal of this
work**", 후자는 `[인쇄]` "This again validates the presented method and
**assures correctness of the tracked aging mechanisms**." `[해석]` §5 의 계산이
전자가 옳다는 쪽을 지지한다 — 재보정은 몫공간 위의 양만 쓰므로 모드
correctness 를 검증할 수 없다.

⑥ **절 제목과 본문의 충·방전이 어긋난다.** §4.1.1 제목은 "Estimation **during
charge**" 인데 본문 첫 문장은 `[인쇄]` "the plateau of the quasi-OCV curve can be
estimated during a constant current **discharge** process". §3 은 충전이라 한다.
`[해석]` 사소한 오식으로 읽히지만, Fig. 4a 의 데이터가 충전인지 방전인지 이
문단으로는 확정되지 않는다.

⑦ **결론의 "three or two … necessary and sufficient" 가 자기 표를 중립화한다.**
Table 5 는 **2개가 3개보다 낫다**고 말하고 §4.2.1 은 그 이유까지 설명하는데,
결론 bullet 은 두 시나리오를 동급으로 묶는다.

---

## 11. 우리 프로젝트와의 접점

### 11.1 채택할 것 / 반증할 것 (의뢰 6항)

| # | 무엇 | 근거 등급 | 우리 쪽 행동 |
|---|---|---|---|
| A1 | **null 방향 `n₁, n₂` 를 격자에 truth 쌍으로 심는다** | **A** (원문 식에서 유도, 수치 확인) | `mode-observability` Phase 1e 후보. Lin 의 `(1,1,1)` 과 **다른 방향**이므로 새 시험이다 |
| A2 | **초기값 스윕을 식별 가능성 시험으로 쓴다** | **A** (원문이 통제 대조군을 인쇄) | 우리는 참값을 알므로 그들이 못 한 "초기값 → 오차" 를 정량할 수 있다. 기존 artifact 재집계 |
| A3 | **관측 중복 진단** — 관측 feature 들의 상관/유효 rank 를 먼저 본다 | **B** (원문 서술 + 우리 재해석) | PVS/SEV 를 목적함수에 넣기 전에 필수. [[pvs-sev-lli-lampe-separability]] |
| A4 | **블록 교대 최적화** | **B** (Navidi 와 두 번째 선례) | 이미 22p 카드 후속 실험 목록에 있다. 선례가 둘로 늘었다 |
| R1 | **"관측을 늘렸더니 나빠졌다" 의 원인이 우리와 같은가** | **C** (목적함수 노름이 다름) | flat valley ↔ multimodal 로 갈라낼 수 있다. 가설로만 |
| R2 | **"용량이 1 % 로 맞으니 방법이 옳다" 는 추론** | **A** (§5 가 반증) | 우리 문서·발표에서 이 형태의 추론을 쓰지 않는다 |
| R3 | **LFP 문턱 수치를 NMC 로 옮기지 않는다** | — | Fig. 8c 의 1–3 mV 는 **LFP 고유**다. 우리 셀은 전압 폭이 한 자릿수 배 넓다 |

### 11.2 ★ 인용 계보 항목이 하나 더 닫힌다

`wiki/questions/22p-physics-or-degeneracy.md` 2026-09-03 (2) 항목 3 이 열어 둔
후보 `[26] Marongiu 2016` 을 확인했다. 결과:

- **창 기하(전극별 start/end, li/de 구분)의 계보는 Dubarry 2012 → {Marongiu
  2016, Birkl 2017} 로 확정된다.** Birkl 이 §3.1 에서 `[19,26,29]` 를 그
  이론의 출처로 명시한다.
- **우리 legacy 식 `LLI = (1−α_PE) + (β_PE − β_NE)` 는 이 논문에도 없다.**
  Marongiu 식 (4) 에서 따라오는 것은
  `β_NE − β_PE = LLI + LAM_Ne,Li·N − LAM_Pe,De` 이고, `α` 항이 없으며 부호가
  반대다. `[해석]` 따라서 **legacy 식은 여전히 두 원전 어디에도 없는 우리 쪽
  (재)유도**이고, `docs/02_CODE_AUDIT.md` 의 2026-09-03 정정이 **옳다.**
- **다만 현행 `src/fitting.py` 의 `κ·(β_NE − β_PE)` 부호 규약은 이 논문 식 (4)
  와 일치한다** (Dubarry 와 일치한다는 기존 확인에 더해 두 번째 확인).
- **이번 세션도 `degradation-degeneracy/` 를 읽기만 했고 고치지 않았다.**

### 11.3 22p 카드에 무엇을 주는가 — **Evidence 어느 쪽도 아니다. 「경계 확정」**

`[해석]` 이 논문은 22p 삼중항에 대해 찬반 어느 쪽 근거도 주지 않는다.
화학(LFP vs NMC811‖Gr+Si)·관측(평탄역 길이 vs 전압 곡선)·정답(용량만)이 전부
다르다. 주는 것은 **경계 세 개**다:

1. **성공 지표와 우리 질문이 직교할 수 있다는 것이 증명됐다** (§5.5-2).
   "half-cell 재구성이 잘 되더라"는 문장은 모드 식별 가능성의 근거가 될 수
   없다 — 총용량은 null 위에서 불변이기 때문이다.
2. **관측 개수를 통제한 초기값 대조군이 처음 등장했다** (§8.3). 축퇴 방향
   위의 값을 추정기가 정한다는 명제가, 이 계보에서 처음으로 **관측을 줄여
   축퇴를 인위적으로 키운 상태에서** 실측됐다.
3. **평탄한 화학에서 전압 관측이 얼마나 죽는지의 숫자가 처음 생겼다** (§8.5).
   Zhang 2020 digest 가 `[인쇄]` "flatness and lack of features" 라고 적은
   그것에 **1–3 mV** 라는 크기가 붙었다.

### 11.4 위키 컴파일 층에 붙는 것

- [[fitting-degeneracy]] — 닫힌 형태 null 방향 **둘** 추가 (`n₁`, `n₂`),
  그리고 "관측 중복이 최적화를 방해한다" 는 세 번째 실패 모드 후보.
- [[np-lip-ocv-reparametrization]] — 창 매개화 계보표에 이 논문의 5-모드 판이
  들어간다. Lin 이 비판한 "non-independent parameters" 의 **가장 극단적인
  사례**(제약 0, 여분 2)가 이것이다.
- [[birkl-ocv-degradation-diagnostic]] — Birkl 의 3-파라미터 좌표가 이 논문
  식 (2)–(5) 의 몫공간임이 확인됐다.
- [[22p-physics-or-degeneracy]] — 경계 확정 3건 (§11.3).
- [[pvs-sev-lli-lampe-separability]] — "관측을 늘리면 갈리는가" 에 대해
  **반례 하나**: 늘린 관측이 기존 관측과 비례하면 오히려 나빠진다 (§8.4).

---

## 12. 무엇을 보고 무엇을 안 봤나 (투명성)

- 크로핑: **fig 8장 + tab 5장 = 13장.**
- **실제로 열어 본 것: fig 1, 2, 3, 4, 5, 6, 7, 8 — 그림 8장 전부.**
  이 논문은 그림 수가 적고 8장 모두가 우리 축(창 매개화·관측 정의·수렴 거동·
  오차 수치·mV)에 직접 걸려서 전부 봤다.
- **추가로 열어 본 것**: 저널 조판본 p.160 우측 단을 400 dpi 로 재렌더링해
  **식 (2)–(5) 의 마이너스 부호를 눈으로 확인**했다 (텍스트 추출이 마이너스를
  잃어버렸고, §5 의 축퇴 계산이 부호에 전적으로 의존하기 때문).
- **안 본 것: tab_1 ~ tab_5 이미지 5장.** PDF 텍스트 추출이 완전해서 숫자를
  전부 확보했다 (Table 1–5 를 이 digest 에 옮겨 적었다). 다만 Table 3·4 의
  **색 강조(빨강=최대, 초록=최소)는 텍스트에 없으므로 판독하지 않았고**,
  최대/최소는 숫자에서 직접 판정했다.
- **본문 서술과 그림이 어긋난 지점 (내가 그림을 보고 확인한 것)**:
  §8.1 (Fig. 5 의 "negligible errors" vs 0.10–0.15 Ah 격차), §8.2 (Fig. 4 의
  환산 산포 0.08 Ah > 수렴 잔차 0.05 Ah), §8.6-1 (Fig. 6c 의 합 vs 식 9의 max),
  §8.6-2 (Fig. 6 이 정지 임계를 만족하지 못한 채 끝난다), §8.5 (Fig. 8d 의
  실제 최대 22 mV vs 본문의 "20 mV").
