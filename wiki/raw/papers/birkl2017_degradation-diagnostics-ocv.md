---
source_url: local-upload/Birkl2017_Degradation_diagnostics_for_lithium_ion_cells.pdf
ingested: 2026-09-03
sha256: 8c32a65c108687ad376bad32ff0096dddb4dc0c675f0bf46f447234b84a09146
---

# 수집 목적

C.R. Birkl, M.R. Roberts, E. McTurk, P.G. Bruce, D.A. Howey,
**"Degradation diagnostics for lithium ion cells"**, *Journal of Power Sources*
**341** (2017) 373–386 의 **절별 해체분석**.

이 논문은 우리 satellite `degradation-degeneracy` 가 판정 대상으로 삼고 있는
바로 그 절차 — **half-cell OCP 를 full-cell pseudo-OCV 에 fitting 해서
LLI/LAM_PE/LAM_NE 를 뽑는 것** — 의 원전 중 하나다.
2026-09-02 BML 세미나(김시원) p.3 이 "정량화 방법: half-cell OCP 를 측정된
full-cell OCV 에 fitting" 이라 적으면서 인용한 출처가
`J. Power Sources, 2017, 341, 373–386` 이며, 이 PDF 의 서지사항과 일치한다
(`raw/papers/2026-09-02-siwon-kim-degradation-mode-ml-seminar.md` p.3 참조).

따라서 이 digest 는 "이 논문이 무엇을 말했나" 보다 **"이 논문이 식별 가능성에
대해 정확히 무엇을 말하고 무엇을 말하지 않았나"** 에 무게를 둔다.

**표기 규칙** (이 위키 관례 3구분):
- `[인쇄]` — 논문 본문/표/식에 글자로 있는 것
- `[도표]` — 그림에서 눈으로 읽은 근사값 (원 데이터가 아니다)
- `[해석]` — 이 문서를 쓰면서 붙인 판단. **논문의 주장이 아니다**

- 원본 파일: 로컬 업로드 PDF (저장소에 바이너리를 넣지 않는다)
- 크로핑 그림: `raw/figures/birkl2017_degradation-diagnostics-ocv/`
  (fig 8장 + tab 6장, `figures.json` 에 캡션 색인)

---

## 0. 서지사항 (직접 확인)

`[인쇄]` PDF 1쪽 헤더 및 메타데이터에서 확인한 것:

| 항목 | 값 |
|---|---|
| 제목 | Degradation diagnostics for lithium ion cells |
| 저자 | Christoph R. Birkl ᵃ, Matthew R. Roberts ᵇ, Euan McTurk ᵇᐟᶜ, Peter G. Bruce ᵇ, David A. Howey ᵃ (교신) |
| 소속 | a: Dept. of Engineering Science, University of Oxford, OX1 3PJ · b: Dept. of Materials, University of Oxford, OX1 3PH · c: Warwick Manufacturing Group, University of Warwick, CV4 7AL |
| 학술지 | Journal of Power Sources **341** (2017) 373–386 |
| DOI | 10.1016/j.jpowsour.2016.12.011 |
| 접수/개정/게재 | Received 12 July 2016 · Revised 15 November 2016 · Accepted 4 December 2016 · Available online 12 December 2016 |
| 라이선스 | © 2016 The Authors, Elsevier B.V., **CC BY 4.0** (open access) |
| 교신저자 메일 | david.howey@eng.ox.ac.uk |
| 키워드 | Lithium ion · Degradation · State of health · Diagnostic · Open circuit voltage · Battery management system |

**의뢰인 추정과의 차이**: 의뢰 메모는 "33쪽 accepted manuscript 판으로 보인다"
고 했으나, 실제 파일은 **14쪽 게재본(typeset, Elsevier 조판)** 이다. 페이지
번호가 373–386 으로 찍혀 있고 Table/Figure 가 조판된 상태다. 이 digest 의
페이지 참조는 **저널 페이지 번호(373–386)** 를 쓴다.

---

## 1. 원문에 없어서 확인이 필요한 것 (공백 목록)

digest 를 쓰기 전에 먼저 밝힌다. 아래는 **논문이 인쇄하지 않은 것**이며,
후속 인용에서 이 자리를 메꾸는 문장을 쓰면 그것은 이 논문의 근거가 아니다.

1. **열화 모델 최적화의 경계(bounds)와 초기값 목록이 없다.** MATLAB
   `fmincon` + `MultiStart`(100회) 만 인쇄돼 있고, `lb`/`ub` 가 무엇인지,
   100개의 시작점이 어떻게 뽑혔는지(랜덤/격자/사용자 지정)는 없다.
2. **추정값에 대한 신뢰구간·표준오차가 없다.** Fig. 8 의 오차 막대는 fitting
   불확실성이 아니라 **코인셀 제작 재현성(기준셀 5개 용량의 표준편차 5.4%)**
   이다 — 논문이 §4.3 에서 명시한다. 즉 **적합의 불확실성은 한 번도 정량화되지
   않는다**.
3. **추정 파라미터 간 상관(correlation)·Hessian·Fisher 정보 분석이 없다.**
   본문 전체에서 "correlation" 은 참고문헌 [6] 제목에만 나온다.
4. **국소최소에 대한 진단이 없다.** multistart 100회가 "global minimum 으로의
   수렴을 보장하기 위해" 있다고만 하고, 100개 해가 몇 개의 서로 다른 최소로
   갈렸는지, 목적함수 값이 비슷한 다른 해가 있었는지는 인쇄되지 않았다.
5. **노이즈 하에서의 검증이 없다.** 합성 데이터 검증(§4.2)은 노이즈를 넣지
   않았고(Fig. 7 의 RMSE 가 셋 다 0.0 mV), 노이즈 민감도 스윕이 없다.
6. **해체(post-mortem) 기반 독립 검증이 없다.** 해체는 §1 에서 *다른 목적*
   (전극 sheet 리튬화 균일성 육안 확인)으로만 쓰였고, 진단 알고리즘의 정답
   대조에는 쓰이지 않았다. 정답은 **제작 설계값**(디스크 지름 · 조립 SoC)이다.
7. **측정 소요시간이 인쇄되지 않았다.** C/25 라는 전류율만 있고 "몇 시간"
   이라는 숫자는 없다.
8. **LAM 의 정규화 기준이 두 곳에서 다르게 읽힌다** (§4 아래 상세). "이용된
   용량 범위 대비" 인지 "전극 전체 대비" 인지가 식과 문장에서 일치하지 않는다.
9. **다른 화학종에 대한 검증이 없다.** LCO/NCO–graphite 한 종뿐이며, 저자
   스스로 결론에서 "future work" 로 남긴다.
10. **상용 노화셀에 적용한 결과가 없다.** 모든 검증셀은 열화를 **공학적으로
    모사한** 코인셀이며, 실제로 사이클링해서 늙힌 셀이 아니다. 이것도 저자가
    결론에서 future work 로 명시한다.

---

## 2. 논문의 질문과 답 (Abstract · §1 Introduction, p.373–376)

### 2.1 문제 설정

`[인쇄]` 초록:

> "Degradation in lithium ion (Li-ion) battery cells is the result of a complex
> interplay of a host of different physical and chemical mechanisms. The
> measurable, physical effects of these degradation mechanisms on the cell can
> be summarised in terms of three degradation modes, namely loss of lithium
> inventory, loss of active positive electrode material and loss of active
> negative electrode material. The different degradation modes are assumed to
> have unique and measurable effects on the open circuit voltage (OCV) of Li-ion
> cells and electrodes. **The presumptive nature and extent of these effects has
> so far been based on logical arguments rather than experimental proof.**"

`[인쇄]` §1 (p.375) 에서 같은 공백을 더 날카롭게 적는다:

> "However, to the best of our knowledge, **the existence of the proposed
> degradation modes has never been proven experimentally and unambiguously but
> only in simulation.**"

`[해석]` 즉 2016년 시점에서 저자들이 지목한 공백은 **"모드가 OCV 에 남기는
효과가 실험으로 증명된 적이 없다"** 이지, **"그 역문제가 유일해를 갖는가"** 가
아니다. 이 구분이 이 digest 의 핵심이다 — 논문의 목표는 *forward* 주장의 실험적
확립이었고, *inverse* 의 식별 가능성은 부산물로만 다뤄진다.

### 2.2 두 개의 명시된 목표

`[인쇄]` §1 말미:

> 1. The design and execution of experiments to verify the manifestations of
>    LLI, LAM_NE and LAM_PE on the OCV of Li-ion cells.
> 2. The creation of a diagnostic algorithm capable of identifying and
>    quantifying the nature and extent of degradation modes present in a Li-ion
>    cell **based exclusively on the cell's OCV without performing derivative
>    operations on the measurements.**

`[인쇄]` 미분을 피하는 이유:

> "Differentiating measurements amplifies the noise in the signal and makes it
> more difficult to use the resulting data for processing. This is especially
> problematic in practical applications where voltage measurements may be
> noisier than in a laboratory environment."

`[해석]` 이것이 ICA(incremental capacity analysis)/DVA(differential voltage
analysis)와 이 논문이 갈라지는 지점이다. 우리 프로젝트가 목적함수에 dQ/dV 항을
더했을 때의 전례([[22p-physics-or-degeneracy]] Evidence Against)는 이 논문의
설계 철학과 **정반대 방향의 실험**이었던 셈이다.

### 2.3 답 (결론, p.385)

`[인쇄]` 저자들이 스스로 정리한 세 가지 key finding:

> - Experimental proof of the effects of LLI, LAM_PE and LAM_NE on the cell's OCV.
> - A diagnostic algorithm has been demonstrated to successfully identify and
>   quantify LLI, LAM_PE and LAM_NE.
> - The diagnostic algorithm can identify the onset of potentially dangerous
>   processes such as excessively high voltages on the PE and lithium plating on
>   the NE.

`[인쇄]` 그리고:

> "Experimental evidence has been presented to prove, for the first time, that
> the OCV of Li-ion cells can be used to provide accurate estimates of LLI,
> LAM_PE and LAM_NE."

---

## 3. 열화 모드 분류 체계 (§1, §3.1, p.375 / p.378–379) ★ 의뢰 4항

### 3.1 세 모드의 정의 (§1, p.375, 그대로)

`[인쇄]`

1. **Loss of lithium inventory (LLI)**: "lithium ions are consumed by parasitic
   reactions, such as surface film formation (e.g. SEI growth), decomposition
   reactions, lithium plating, etc. and are no longer available for cycling
   between the positive and negative electrode, leading to capacity fade.
   Surface films may also cause power fade. **Lithium ions can also be lost if
   they are trapped inside electrically isolated particles of the active
   materials.**"
2. **Loss of active material of the NE (LAM_NE)**: "active mass of the NE (or
   anode) is no longer available for the insertion of lithium due to particle
   cracking and loss of electrical contact or blocking of active sites by
   resistive surface layers."
3. **Loss of active material of the PE (LAM_PE)**: "active mass of the PE (or
   cathode) is no longer available for the insertion of lithium due to
   structural disordering, particle cracking or loss of electrical contact."

`[해석]` LLI 정의의 마지막 문장(전기적으로 고립된 입자 안에 갇힌 리튬도 LLI)이
뒤에서 li/de 축퇴 논의의 씨앗이 된다 — LAM_li 은 정의상 LLI 를 **동반**한다.

### 3.2 li/de 하위 구분 — 우리 격자 `lam_pe_type="de"` 의 어원 ★

`[인쇄]` §2.1 (p.376):

> "**Theoretically, active electrode material can be lost in lithiated,
> delithiated and partially lithiated states.** Loss of lithiated NE material
> (LAM_NE,li) was emulated by combining a 12 mm NE disk with a 15 mm PE disk,
> both harvested from a fully charged pouch cell (SoC = 100%). Equivalently,
> loss of delithiated NE material LAM_NE,de was emulated by combining a 12 mm NE
> disk with a 15 mm PE disk, both harvested from a fully discharged pouch cell
> (SoC = 0%). The same principle was used to create loss of lithiated PE
> material (LAM_PE,li)."

즉 논문이 쓰는 아래첨자는 정확히 네 가지다: **LAM_NE,li · LAM_NE,de ·
LAM_PE,li · LAM_PE,de**. 정의는 *잃은 활물질이 그 순간 리튬을 갖고 있었는가*다.

`[인쇄]` 각 하위모드의 OCV 결과 (§3.1, Fig. 5 c)–f) 서술):
- **LAM_NE,li** — 잃은 흑연 입자 안에 리튬이 갇힘 → 용량 손실 직결. NE 의
  **EoC 전압은 그대로**(Fig. 5 c 의 자물쇠 기호), EoD 쪽 전압은 LLI 때와 같은
  방식으로 움직인다.
- **LAM_NE,de** — 초기에는 용량 영향이 작다 (NE 여유분이 흡수). NE 의 **EoD
  전압이 그대로**이고 EoC 전압이 점점 내려간다. 30% LAM_NE,de → 용량 손실
  **12%**.
- **LAM_PE,li** — LAM_NE,li 의 대칭. PE OCV 곡선이 수축, EoC 에서 NE 에 들어가는
  리튬이 줄어 NE 가 더 높은 OCV 에 남고 → PE 를 더 높은 전압으로 밀어야 4.2 V
  에 닿는다.
- **LAM_PE,de** — 초기부터 용량에 영향 가능 (PE 여유분이 NE 보다 작다). 양 전극
  **EoC OCV 는 그대로**, PE 의 EoD OCV 가 내려간다. LCO/NCO 는 약 3.4 V 아래에서
  OCV 가 급락하므로 30% LAM_PE,de → 용량 손실 **24%**.

`[도표]` Fig. 5 (왼쪽 막대 도식의 SoC_cell 눈금에서 직접 읽음):
- b) 30% LLI → `2% stoich. offs.` 라벨이 인쇄돼 있고 EoD 쪽 30% 손실
- d) 30% LAM_NE,de → `88% SoC_cell` (= 12% 손실, 본문과 일치 ✓)
- e) 30% LAM_PE,li → `72% SoC_cell` (= 28% 손실)
- f) 30% LAM_PE,de → `24% SoC_cell` (= 24% 손실, 본문과 일치 ✓)

`[해석]` **우리 격자의 `lam_pe_type`/`lam_ne_type` ∈ {"de","li"} 는 이 축과
의미가 정확히 일치한다.** `degradation-degeneracy/src/modes.py` 의 구현
(read-only 확인) 에서 `lam_*_type == "de"` 일 때만 잔여 전극 초기농도를
`c/(1-lam)` 으로 되올리며, 주석이 "죽은 PE 는 비어 있었음 → 남은 PE 가 재고
전량 보유" 라고 적는다 — 이는 Birkl 의 "delithiated 상태로 잃었다" 와 같은
물리다. 다만 **이 논문이 그 이름의 직접 출처라는 문장은 저장소 어디에도 인쇄돼
있지 않다.** 의미 일치는 확인했고, 명명의 계보는 미확인이다.

### 3.3 메커니즘 → 모드 매핑 (Fig. 1, Fig. 3)

`[도표]` Fig. 3 (본 그림, 오른쪽 "Effect" 열은 크로핑에서 잘림) 의 좌측 2열:

| Degradation mechanism (11종) | → Degradation mode |
|---|---|
| SEI growth · SEI decomposition · Electrolyte decomposition | → **LLI** |
| Lithium plating / dendrite formation | → **LLI** |
| Binder decomposition · Graphite exfoliation · Structural disordering · Loss of electric contact · Electrode particle cracking · Transition metal dissolution · Corrosion of current collectors | → **LAM_NE / LAM_PE** (다대다 연결) |

`[인쇄]` §1 중요 단서:

> "Note that Fig. 3 only lists the effects of degradation mechanisms and modes
> on the cell's **thermodynamic** (i.e. its OCV), **not its kinetic** behaviour.
> The primary effect of degradation on the cell's kinetics is an increase in
> internal resistance or cell impedance … Methods to estimate internal cell
> resistance are widely reported [22–24] and not the subject of the presented
> work."

`[해석]` 이 논문의 관측은 **순수 열역학**이다. 2026-09-02 세미나의 SEV 는
동역학(charge-transfer 저항) 축이므로, 두 자료는 **직교하는 관측 공간**을 본다
([[pvs-sev-degradation-mode-features]] 참조).

---

## 4. 측정 조건 (§2, p.376–377) ★ 의뢰 5항

### 4.1 셀과 재료

`[인쇄]`
- 원 셀: 상용 **Kokam 740 mAh 파우치셀**. NE = **graphite**, PE = **LCO/NCO
  blend**(lithium cobalt oxide + lithium nickel cobalt oxide).
- 셀당 전극 sheet 20장(PE, NE 각각). 총 전극 표면적 **600 cm²**, C/25 실측
  평균 용량 **759 mAh** (표준편차 < 0.2%).
- 파우치셀을 Ar 글로브박스에서 세라믹 메스로 개봉 → sheet 추출 → DMC 세척 →
  진공 20분 건조 → 한쪽 면 활물질을 NMP 로 제거(집전체 접촉 개선) → 펀치로
  디스크 절단.
- Celgard 세퍼레이터 + **LP30 전해액** (1.0 M LiPF₆ in EC:DMC = 50:50).

`[인쇄]` 코인셀 구성 (Table 1, Table 2, Fig. 4):

| 셀 ID | 모사 모드 | SoC PE | SoC NE | ⌀PE | ⌀NE |
|---|---|---|---|---|---|
| Ref 1–3 | 기준 | 100% | 0% | 15 mm | 15 mm |
| Ref 4–5 | 기준 | 0% | 100% | 15 mm | 15 mm |
| HC_PE | PE 반쪽셀 (Li foil 대극) | 100% | — | 15 mm | — |
| HC_NE | NE 반쪽셀 (Li foil 대극) | — | 0% | — | 15 mm |
| LLI25 | 25% LLI | 75% | 0% | **20 mm** | **20 mm** |
| LLI50 | 50% LLI | 50% | 0% | **20 mm** | **20 mm** |
| LAM_NE,li | 36% LAM_NE,li | 0% | 100% | 15 mm | 12 mm |
| LAM_NE,de | 36% LAM_NE,de | 100% | 0% | 15 mm | 12 mm |
| LAM_PE,li | 36% LAM_PE,li | 100% | 0% | 12 mm | 15 mm |
| LLI+LAM_PE | 25% LLI + 13% LAM_PE,li | 75% | 0% | 14 mm | 15 mm |

`[도표]` **원문 내부 모순 하나 (조판본 Table 2 이미지에서 직접 확인)**: Table 2
는 LLI25/LLI50 의 전극 지름을 **20 mm** 로 인쇄한다. 그런데 §2.1 본문은 "In
coin cells with emulated LLI, **both electrode disks were 15 mm** in diameter"
라 하고, §2.2 는 "Given a surface area of 1.767 cm² **in all coin cells with
electrode diameters of 1.5 cm**" 라 한다 (1.767 cm² = π·(0.75 cm)² → 15 mm 가
맞다). Fig. 4 a) 도 Anode ⌀15 / Separator ⌀20 / Cathode ⌀15 이다.
`[해석]` Table 2 의 20 mm 는 세퍼레이터 지름이 전극 열에 잘못 들어간 **오식**일
가능성이 높다. 어느 쪽이든 이 논문을 인용해 "LLI 셀은 20 mm 전극" 이라고 쓰면
안 된다.

### 4.2 LLI / LAM 을 물리적으로 "만든" 방법

`[인쇄]`
- **LLI**: SoC 가 높은 상태로 방전된 파우치셀의 **PE** 와, SoC 가 낮은 상태의
  파우치셀의 **NE** 를 조합. 예 — PE(25% SoC) + NE(0% SoC) = **25% LLI**.
  근거: "the NE is the limiting electrode during discharge and once it has
  reached its upper voltage limit … no more lithium can be extracted."
- **LAM**: 해당 전극 디스크의 **지름을 줄인다**. "The commercial electrodes …
  were very uniformly coated with active material, so the useful capacity of
  the electrodes was assumed to be proportional to their surface area."
  12 mm vs 15 mm → 면적비 (12/15)² = 0.64 → **36% LAM**.

`[인쇄]` **이 방법의 한계를 저자가 직접 적는다**:

> "A limitation of this experimental approach to simulate the loss of active
> material is the fact that lithium insertion/extraction in the overhang region
> of the larger electrode is limited by the lateral diffusion of lithium in the
> active material. **The simulation of LAM using this method is therefore only
> valid for very slow C-rates. For this reason, a very low pseudo-OCV C-rate of
> C/25 is used in this work.**"

`[해석]` 즉 **C/25 라는 선택은 "OCV 에 가깝기 위해서"만이 아니라 "이 LAM 모사
기법이 성립하기 위해서"** 이기도 하다. 이 논문의 C-rate 는 진단법의 요구가
아니라 검증 장치의 요구에서도 나온 값이다 — 인용할 때 구분해야 한다.

### 4.3 시험 조건 ★ "20시간 이상" 의 근거

`[인쇄]`
- 항온조 **30 °C**, BioLogic MPG-205 / SP-150 포텐시오스탯, 시험 전 3시간 열평형.
- 코인셀 공칭 용량 계산: 표면적 1.767 cm² × (759 mAh / 600 cm²) = **2.236 mAh**
  → **C/25 = 0.089 mA**, **C/2 = 1.118 mA**.
- 시험 순서(Table 4, full cell): 부분충전 → **C/2 사이클**(성능 선별, 불량 셀
  폐기) → 부분방전(3.75 V) → 부분충전 → **C/25 사이클 = pseudo-OCV 측정**.
  전압창 2.7–4.2 V.
- 반쪽셀 전압창: PE 3.5–4.5 V, NE 0.001–1.3 V.
- 파우치셀 전처리(Table 3): C/25 = 29.6 mA, 목표 SoC 는 초기 실측 용량 Q_meas
  대비 쿨롱 계수로 맞춤 (50% → Q_dch > 0.5·Q_meas, 25% → Q_dch > 0.75·Q_meas).

`[인쇄]` pseudo-OCV 로 취급한 근거:

> "At a current rate of C/25, the voltage drop in the coin cells was measured to
> be on the order of 9 × 10⁻⁴ mV, which was considered negligible and any
> voltage measurements recorded at a current rate of C/25 were treated as
> pseudo-OCV."

`[해석]` **소요시간은 논문에 인쇄되지 않았다.** C/25 정전류라는 정의에서 한
방향 만방전/만충전이 명목상 **25시간**, 방전+충전 한 사이클이 **~50시간**이며,
여기에 C/2 사이클과 부분 충·방전, 3시간 열평형이 앞에 붙는다. 세미나의
"20시간 이상" 은 이 자리수와 모순되지 않지만 (오히려 보수적이다), **이 논문에서
그 숫자를 직접 인용할 수는 없다**.

`[해석]` 불확실성 표기에 대해: 5.4% 라는 유일한 오차 수치는 **기준 코인셀 5개를
C/2 로 잰 용량의 표준편차**다. 이것은 (a) 제작 재현성이고, (b) C/2 측정이며,
(c) 진단 알고리즘의 출력 분산이 **아니다**. 논문은 (b)(c)를 명시적으로 구분하지
않은 채 이 값을 Fig. 8 의 오차 막대로 쓴다.

---

## 5. 이론 — 전압 한계가 만드는 stoichiometric offset (§3.1, p.377–379)

`[인쇄]` 기본 구도:

> "In Li-ion cells, the end of charge (EoC; 100% SoC) and the end of discharge
> (EoD; 0% SoC) are defined by a corresponding maximum and minimum cell voltage
> … During charge, **the PE is limiting**, since its rising voltage, resulting
> from delithiation, triggers the cell's EoC voltage limit (in this case 4.2 V).
> Analogously, **the NE is limiting during discharge**, triggering the EoD
> voltage limit (in this case 2.7 V)."

`[인쇄]` **이 논문이 문헌에 더했다고 주장하는 것** (§3.1):

> "Imposing these voltage limits can lead to a **stoichiometric offset between
> the electrodes, which has not been addressed in the literature but is an
> important addition of this work.**"

`[인쇄]` 30% LLI 예시에서의 결과:

> "In the case of 30% LLI, this stoichiometric offset causes a noticeable
> **increase in cell capacity, on the order of 2%**, as indicated by the green
> area in the OCV plot of Fig. 5 b)."

`[해석]` **이 항이 왜 우리에게 중요한가.** 순진한 α/β 창 모델(전극 곡선을
늘이고 밀어 full-cell 을 재구성)에서는 EoC/EoD 지점이 파라미터의 함수로 자유롭게
따라 움직인다. Birkl 은 그렇게 두지 않는다 — **컷오프 전압 2개가 두 개의
방정식(Eq. 11, 12)을 강제**하고, 그것이 Δx_EoC · Δx_EoD 두 자유도를 **소거**한다
(§6.3). 다시 말해 Birkl 의 역문제는 **자유 파라미터 3개**짜리이고, 컷오프
제약이 없는 4-파라미터 창 모델보다 **구조적으로 덜 축퇴적**이다. 대신 그 대가로
반쪽셀 OCP 모델의 **절대 전압 정확도**에 훨씬 민감해진다 (Eq. 11–12 가 절대
전압값 4.2 / 2.7 V 를 등식으로 쓰기 때문이다).

`[인쇄]` 안전 관련 부산물 두 가지:
- LLI 나 LAM_PE,li 가 커지면 PE 가 점점 높은 전압으로 밀린다 → 구조 불안정,
  최악의 경우 탈리튬화된 캐소드가 전해질과 발열 반응 → **thermal runaway** [30].
- LAM_NE,de 가 NE 여유분을 다 먹으면 NE 가 음전압으로 밀린다 → **리튬 도금**
  개시 → 덴드라이트 → 내부단락 [31,32].

---

## 6. 분해 절차의 정확한 정의 (§3.2–3.3, p.379–381) ★ 의뢰 1항

**이 절이 이 digest 의 핵심이다.** 절차는 **3단계**이고, 자유 파라미터의 개수가
단계마다 다르다.

### 6.1 단계 1 — 반쪽셀로 OCP 모델 파라미터화 (전극당 15개)

`[인쇄]` 전극의 정규화 용량 x 를 OCV 의 함수로 쓰는 다상(multi-phase) 모델
(선행연구 [33] = Birkl et al., *J. Electrochem. Soc.* **162**(12) (2015)
A2271–A2280):

> x(E^OC) = Σᵢ₌₁ᴺ Δxᵢ / (1 + exp[(E^OC − E₀,ᵢ)·aᵢ·e / kT])   … (1)

- N = 상(phase) 개수, Δxᵢ = 상 i 에 귀속된 물질 분율, E₀,ᵢ = 상 i 의 격자자리
  에너지, aᵢ = 삽입 이온 간 상호작용 에너지의 근사, e = 전하량, k = 볼츠만 상수,
  T = 절대온도.

`[인쇄]` **상 개수를 4 → 5 로 늘린 이유가 명시돼 있다**:

> "In previous work, a minimum of four phases were identified in both the PE and
> NE material for this particular cell chemistry [33]. In this work, **high
> qualities of fit of electrode OCVs are paramount in order to achieve accurate
> estimates of degradation modes.** For this reason, an additional phase was
> added to the OCV model in order to improve the fit qualities from a root mean
> squared error (RMSE) of 7 mV for the PE and 12 mV for the NE [33] to < 3 mV
> for both electrodes in this work."

`[인쇄]` 목적함수 (Eq. 2) — **전압 잔차의 RMSE**, 가중치 없음:

> arg_θ min RMSE = √( Σᵢⁿ (Ê^OC_i(θ) − E^OC_i)² / n )

`[인쇄]` 자유 파라미터 (Eq. 3): 전극 하나당 **θ = 5행 × 3열 = 15개**
(E₀,₁…E₀,₅, Δx₁…Δx₅, a₁…a₅).

`[인쇄]` Eq. (1) 은 N>1 에서 E^OC(x) 로 명시적으로 뒤집을 수 없어 **최적화 중
반복법으로 푼다**.

### 6.2 단계 2 — 전극 + 셀 동시 재적합 (30개)

`[인쇄]` 2단계에서는 단계 1 의 θ 를 **초기 추정값으로** 삼아, 기준(pristine)
full-cell pseudo-OCV 와 두 반쪽셀 OCV 를 **동시에** 맞춘다.

- 셀 OCV 정의 (Eq. 4): **E^OC_Cell = E^OC_PE − E^OC_NE**
- 목적함수 (Eq. 5) = **세 개의 RMSE 의 단순 합** (셀 + PE + NE), 가중치 없음:
  RMSE_cell(θ_Cell) + RMSE_PE(θ_Cell,PE) + RMSE_NE(θ_Cell,NE)
- 자유 파라미터 (Eq. 6): **θ_Cell = 30개** (PE 15 + NE 15)

`[인쇄]` 그리고 결정적인 한 문장:

> "**It is important to emphasize that the OCV model is only parameterized in
> this fashion once for the base case.** Fitting the OCV of degraded cells, thus
> identifying the degradation modes, is achieved using the degradation model
> described below. This is based on the assumption that **the degradation does
> not impact the individual phases of the electrode materials in different
> ways.**"

`[해석]` 이 가정이 무너지면(예: 특정 상만 우선적으로 죽는 구조 열화) 진단
알고리즘 전체가 무효다. 논문은 이 가정을 시험하지 않는다 — 코인셀 검증에서 잃은
활물질은 **가위로 잘라낸 균일한 조각**이라 정의상 이 가정을 만족한다.

### 6.3 단계 3 — 열화 모델: 자유 파라미터 **3개뿐** ★

`[인쇄]`

> "The degradation model is designed to estimate **three parameters only**; the
> degradation modes LLI, LAM_NE and LAM_PE. … **Only the full cell's OCV
> measurement is required for this. The parameters of the OCV model described in
> Section 3.2 remain unaltered.**"

`[인쇄]` 세 모드가 전극 용량 범위에 작용하는 방식 — 논문이 직접 3분한다:

> "The degradation modes affect the electrodes' capacity ranges in terms of
> (i) **their offset, increased by LLI**, (ii) **their scaling, affected by
> LAM_NE and LAM_PE** and (iii) **the stoichiometric offset, at EoC (Δx_EoC) and
> EoD (Δx_EoD) due to the constant upper and lower cell voltage limits.**"

`[인쇄]` 식 (7)–(10) (조판본 이미지에서 부호까지 직접 확인):

> x_PE,EoC = Δx_EoC / (1 − LAM_PE)                          … (7)
> x_PE,EoD = (Δx_EoD + 1 − LLI + LAM_PE) / (1 − LAM_PE)      … (8)
> x_NE,EoC = (Δx_EoC + LLI − LAM_NE) / (1 − LAM_NE)          … (9)
> x_NE,EoD = Δx_EoD / (1 − LAM_NE)                           … (10)

`[인쇄]` 정규화 규약:

> "LLI, LAM_PE and LAM_NE in Equations (7)–(10) range from 0 to 1, where 1 is
> equivalent to the cell's original capacity; e.g. LLI = 0.1 means that the loss
> of lithium inventory is equivalent to 10% of the cell's original capacity.
> **LAM_PE and LAM_NE refer to the loss of active material as a fraction of the
> active material originally utilised within the capacity range of the full
> cell.**"

`[인쇄]` **Δx_EoC 와 Δx_EoD 는 자유 변수가 아니다.** 셀 전압 한계 2개가 등식을
준다:

> E^OC_Cell,high − Ê^OC_PE,EoC(x_PE,EoC) + Ê^OC_NE,EoC(x_NE,EoC) = 0   … (11)
> E^OC_Cell,low  − Ê^OC_PE,EoD(x_PE,EoD) + Ê^OC_NE,EoD(x_NE,EoD) = 0   … (12)

> "Δx_EoC and Δx_EoD can be calculated by substituting Equations (7)–(10) into
> Equations (11) and (12) and **solving the linear system of equations.**"

여기서 E^OC_Cell,high = **4.2 V**, E^OC_Cell,low = **2.7 V** (고정 상수).

`[인쇄]` 전극 창의 이산화 (Eq. 13–14):

> x̂_PE = {x_PE,EoC, … x_PE,EoD} ,  x̂_NE = {x_NE,EoC, … x_NE,EoD}
> "The number of elements in the vectors depends on the number of sampling
> points obtained for the pseudo-OCV measurements."

`[인쇄]` 셀 수준 (Eq. 15–17):

> x_Cell,EoC = Δx_EoC             … (15)
> x_Cell,EoD = 1 − LLI + Δx_EoD   … (16)
> x̂_Cell = {x_Cell,EoC, … x_Cell,EoD}   … (17)
> "In a pristine cell 100% SoC is equivalent to x_Cell,EoC = 0 and 0% SoC to
> x_Cell,EoD = 1. … x_Cell,EoD − x_Cell,EoC = 0.9 means that the cell has lost
> 10% of its original capacity."

`[인쇄]` **목적함수 (Eq. 18)** — full-cell 전압 잔차의 RMSE **하나뿐**. dQ/dV
항 없음, 가중치 없음:

> arg_θdeg min RMSE = √( Σᵢⁿ (Ê^OC_Cell,deg(θ_deg) − E^OC_Cell,deg)² / n )

`[인쇄]` **θ_deg = [LLI, LAM_PE, LAM_NE]** (Eq. 19). 끝. 세 개다.

### 6.4 최적화 알고리즘·초기값·경계 (§3.3 말미)

`[인쇄]` 그대로:

> "The fitting procedure is carried out in **Matlab**, using the **active-set
> algorithm in Matlab's fmincon** optimisation function. **In order to ensure
> convergence to the global minimum, the optimisation is run repeatedly (100
> times) from different starting points using Matlab's global optimisation
> function multistart.**"

`[해석]` 여기서 읽을 것 둘:
1. `fmincon` 을 쓴다는 것은 **경계(lb/ub)와 제약이 있다는 뜻**이지만 그 값은
   인쇄되지 않았다. 물리적으로는 [0, 1] 이 자연스럽다 (Eq. 7–10 의 정의역).
2. **multistart 100회는 국소최소가 실재한다는 저자들의 인정**이다. 다만 논문은
   그 100개 해의 분포·목적함수 값의 평탄도를 보고하지 않는다 — 우리가 재는
   flat valley 가 있었는지 없었는지는 이 논문에서 알 수 없다.

### 6.5 가중치 대신 쓴 것 — 구간 제한

`[인쇄]`

> "Since the cell's OCV drops off rapidly near the EoD, errors calculated at low
> OCV are generally greater than errors at higher OCV where the OCV curve is
> flat. **In order to avoid a bias of the fit toward the lower end of the OCV
> curve, the calculation of the RMSE as described in Equation (18) was confined
> to the part of the OCV curve with a gradient of ΔE^OC_Cell,deg / ΔSoC < 0.1.**"

`[해석]` 즉 가중치 함수 대신 **하드 마스크**를 썼다. 이것은 축퇴 구조에 직접
영향을 준다 — 급경사 구간(EoD 근처)은 세 모드를 가장 잘 구분해 주는 구간인데,
그 구간을 목적함수에서 **빼 버린 것**이다. 저자의 동기(저전압 쪽 편향 방지)는
이해되지만, 식별 가능성 관점에서는 **정보를 버리는 선택**이다. 0.1 이라는
임계값의 근거는 인쇄되지 않았고 민감도 분석도 없다.

`[인쇄]` 그리고 §4.3 에서:

> "The RMSE values displayed in the OCV plots were calculated from the measured
> and the fitted cell voltages **for the entire cell voltage window of 2.7 V–4.2
> V.**"

`[해석]` **보고된 RMSE ≠ 최적화된 RMSE.** Fig. 8 의 숫자는 전 구간 기준이고,
최소화된 것은 마스크 구간 기준이다. 두 값의 차이는 논문에 없다.

### 6.6 조판 오식 하나

`[인쇄]` p.381: "the OCV of the degraded cell, Ê^OC_Cell,deg, is calculated for
capacity range x̂_Cell, by **solving Equation (2)** using Ê^OC_PE and Ê^OC_NE."
`[해석]` Eq. (2) 는 반쪽셀 적합의 목적함수이고, 여기서 필요한 것은 **Eq. (4)**
(E_Cell = E_PE − E_NE) 다. 명백한 오식이며 의미에는 영향이 없다.

---

## 7. 식별 가능성에 대해 저자들이 실제로 한 말 ★★ 의뢰 2항 — 이 digest 의 최중요 산출물

**결론부터: 저자들은 침묵하지 않는다. 명시적으로 한 종류의 축퇴를 진술하고,
그것을 "제거하지 않고 파라미터화를 바꿔 우회한다."** 아래는 §4.2 (p.382) 의
해당 문단 **전문 인용**이다.

`[인쇄]`

> "It is important to point out that the model estimates the **total** amounts of
> lost active materials LAM_PE and LAM_NE, both lithiated and delithiated. Any
> lithium contained in lost active electrode material is included in the estimate
> of the **total LLI**; i.e. the total estimated LLI includes both the lithium
> lost through pure LLI (e.g. by SEI build up) and the lithium lost in lithiated
> active material (LAM_PE,li and LAM_NE,li). For example, 10% of pure LLI and 5%
> of LAM_NE,li gives a total of 15% LLI.
>
> **The reason for the diagnostic algorithm to be designed in this manner is that
> a combination of e.g. LLI and LAM_NE,de creates the same OCV signature as an
> equal amount of LAM_NE,li. The same holds true for combinations of LLI and
> LAM_PE. The fractions of lithiated and delithiated LAM can therefore not be
> uniquely identified if the assumption is that LLI can occur simultaneously,
> resulting from a different mechanism.**
>
> An exceptional case would be one where LAM is detected but no LLI. In such a
> case, the respective LAM could be uniquely identified as loss of delithiated
> active material.
>
> In real-world scenarios of Li-ion cell degradation, there is no reason to
> assume that the loss of active electrode material occurs exclusively in
> lithiated or delithiated states - it is likely to occur over a range of
> different stages of lithiation. The approach to separate the loss of lithium
> contained in lost active electrode material from the loss of the active
> electrode material itself allows to account for these more realistic
> scenarios."

`[해석]` 이 문단을 정확히 읽으면:

1. **5-파라미터 문제 {pure-LLI, LAM_NE,li, LAM_NE,de, LAM_PE,li, LAM_PE,de} 는
   전역적으로 축퇴다.** 저자들이 그 축퇴 방향을 구체적으로 지목한다:
   `pure-LLI + LAM_NE,de ↔ LAM_NE,li` 가 같은 OCV 시그니처를 만든다.
2. **저자들의 대응은 축퇴를 푸는 것이 아니라 몫공간(quotient)으로 옮기는
   것이다.** 3-파라미터 {total-LLI, LAM_PE, LAM_NE} 는 그 축퇴의 동치류에
   붙인 좌표다. "설계 이유(reason for the diagnostic algorithm to be designed
   in this manner)" 라는 표현이 그것을 명시한다.
3. **따라서 이 방법으로 얻은 LAM_PE 는 "PE 활물질을 잃었다"만 말하고, 그것이
   리튬을 갖고 있었는지는 말하지 않는다.** 하위 귀속을 주장하는 후속 인용은
   원전이 허용하지 않는 주장이다.
4. **예외조항이 조건부 식별성을 준다**: LAM 이 검출되고 LLI 가 0 이면, 그 LAM 은
   delithiated 로 유일하게 식별된다. 이것은 "축퇴가 상태공간 전체에서 균일하지
   않다"는 진술이며, 우리 프로젝트의 격자 스캔 논리와 같은 형태다.

**반대쪽 문장** — 같은 §4.2 마지막에 저자들이 쓰는 강한 주장:

`[인쇄]`

> "For all three scenarios, perfect fits were obtained and all degradation modes
> accurately identified, **which proves the ability of the diagnostic algorithm
> to uniquely identify the three different degradation modes by fitting the OCV
> of a degraded cell.**"

`[해석]` 이 "proves … uniquely identify" 는 **§8.1 의 검증 설계가 지지하는
범위를 넘는다**. 근거는 3개의 시나리오이고, 그 데이터는 **같은 모델을 forward
로 돌려 만든 것**이며(자기 역범죄, inverse crime), **노이즈가 없고**(Fig. 7 의
RMSE = 0.0 mV), **파라미터 상관·목적함수 곡률에 대한 진단이 없다.**
세 점에서 최적해가 참값과 일치했다는 것은 **그 세 점에서 전역 최소가 참값
근처에 있었다**는 뜻이며, "3-파라미터 문제가 유일하게 식별 가능하다"는
**전칭 명제의 증명이 아니다.**

**본문에 없는 것** (다시 명시): 파라미터 상관계수, 목적함수의 국소 곡률/Hessian,
신뢰구간, 노이즈 스윕, flat valley 탐색, 서로 다른 국소최소들의 목적함수 값 비교
— **하나도 없다.** multistart 100회가 유일한 국소최소 대응책이고 그 결과 분포도
보고되지 않는다.

---

## 8. 검증 방법 ★ 의뢰 3항

논문의 검증은 **두 층**이고, 성격이 완전히 다르다.

### 8.1 층 1 — 합성 데이터 (§4.2, Fig. 7, p.381–383)

`[인쇄]` 절차: 파라미터화된 열화 모델을 **'forward mode'** 로 돌려 알려진
(LLI, LAM_PE, LAM_NE) 을 갖는 가상 셀의 OCV 를 만들고, 같은 모델을 역으로 적합.

`[인쇄]` Table 6 — 세 시나리오 (단위: 셀 원용량 대비 %):

| 시나리오 | LLI (pure) | LAM_NE,li | LAM_NE,de | LAM_PE,li | LAM_PE,de | **LLI (total)** |
|---|---|---|---|---|---|---|
| I | 12% | 0% | 23% | 6% | 0% | **18%** |
| II | 21% | 4% | 0% | 0% | 7% | **25%** |
| III | 9% | 0% | 14% | 0% | 11% | **9%** |

`[도표]` Fig. 7 에서 직접 읽은 것:
- 세 패널(a, c, e) 모두 **RMSE = 0.0 mV** 로 인쇄돼 있다.
- 막대그래프(b, d, f)의 Real 과 Estimate 가 **육안으로 완전히 동일**하다:
  I → LLI 18 / LAM_NE 23 / LAM_PE 6, II → 25 / 4 / 7, III → 9 / 14 / 11.
  (LLI 막대는 Table 6 의 **total** 열과 일치한다 — pure 가 아니다.)

`[해석]` **이것은 inverse crime 이다.** 데이터 생성 모델 = 적합 모델 = 동일,
노이즈 0, 모델 오차 0. 이 조건에서 RMSE 0.0 mV 와 완전 복원은 **거의 자동으로
따라오는 결과**이고, 실질적으로 시험하는 것은 "구현에 버그가 없다 + 이 세 점
근처에 전역 최소가 유일하다" 정도다. **노이즈나 반쪽셀 OCP 오차가 있을 때의
식별 가능성에 대해서는 아무 말도 하지 않는다.** 우리 프로젝트가 정확히 그
빠진 축(노이즈 층 × 모델 오차)을 재고 있다.

`[해석]` 더 나아가 — §4.3 에서 논문은 이 층을 근거로 상용셀 적용을 낙관한다:
"For applications on commercial cells, **high accuracies can be expected** for
estimations of degradation modes, **as demonstrated in Section 4.2**." 무노이즈
inverse crime 을 근거로 실셀 정확도를 기대하는 것은 근거가 약한 외삽이다.

### 8.2 층 2 — 공학적으로 제작한 코인셀 (§4.3, Fig. 8, p.383–385)

정답의 출처는 **해체가 아니라 제작 설계값**이다 (디스크 지름 → LAM, 조립 시
전극 SoC → LLI). **post-mortem 대조는 없다.**

`[인쇄]` + `[도표]` Fig. 8 의 6개 셀 결과 (RMSE 는 인쇄된 숫자, 막대값은 그림
판독 근사):

| 패널 | 셀 | 설계 진값 | 추정 (figure-read ≈) | RMSE [인쇄] |
|---|---|---|---|---|
| a,b | LLI25 | LLI 25 | LLI ≈ 23, LAM_NE ≈ 1, LAM_PE ≈ 0 | **6.7 mV** |
| c,d | LLI50 | LLI 50 | LLI ≈ 50, LAM_NE ≈ 0, **LAM_PE ≈ 6.5** | **11.9 mV** |
| e,f | LAM_NE,li | LLI 36, LAM_NE 36 | LLI ≈ 32, LAM_NE ≈ 27, **LAM_PE ≈ 10** | **28.6 mV** |
| g,h | LAM_NE,de | LLI 9.6, LAM_NE 36 | LLI ≈ 11, LAM_NE ≈ 30.5, LAM_PE ≈ 7 | **5.8 mV** |
| i,j | LAM_PE,li | LLI 36, LAM_PE 36 | LLI ≈ 30, LAM_PE ≈ 30.5, LAM_NE ≈ 2.5 | **17.7 mV** |
| k,l | LLI+LAM_PE,li | LLI 38, LAM_PE 13 | LLI ≈ 33, **LAM_PE ≈ 20**, LAM_NE ≈ 7.5 | **23.2 mV** |

`[인쇄]` 오차 막대의 정체:

> "The error bars on the bar charts on the right of Fig. 8 are based on the
> standard deviation of the capacities of the reference coin cells (5.4%) … It
> should be emphasized that **the uncertainty of 5.4% reflects the
> reproducibility of the coin cell manufacturing.**"

`[인쇄]` 저자들이 스스로 보고한 오차 초과:
- **LAM_NE,li 셀**: "LAM_NE was successfully identified as a major degradation
  mode, although to a slightly smaller extent than expected, **exceeding the
  margin of error by ~4%**. Against expectations, a small amount of LAM_PE was
  detected …, **exceeding the margin of error by ~5%.**" → 원인 가설: 12 mm 펀치가
  디스크 가장자리를 눌러 0.3 mm 폭 rim 이 세퍼레이터에서 떨어졌고(≈ 전극 용량의
  5%), 리튬화 상태로 잘린 NE 의 리튬이 안 빠져 **LAM_PE 처럼 보였다.**
- **LAM_NE,de 셀**: LAM_PE 가 "exceeds the margin of error by only ~1% and is
  therefore considered negligible."
- **LLI+LAM_PE 셀**: "the LAM_PE was slightly overestimated, exceeding the margin
  of error by 1.6%", LAM_NE 는 "~1%" 초과.

`[해석]` **본문 서술과 그림이 어긋나는 지점 두 곳** (내가 그림을 보고 확인한
것):

- **패널 d (LLI50)**: 본문은 "50% LLI was accurately estimated and **other
  degradation modes were found to be negligible within the margin of error**"
  라고 한다. 그런데 그림의 LAM_PE 추정치는 ≈6.5% 이고, 논문이 스스로 정한
  margin 은 5.4% 다. 진값 0 대비 6.5% 는 **margin 안이 아니다.** 오차 막대가
  대략 2–11% 구간을 덮는 것으로 보이므로 "막대가 0을 포함하지 않는다" — 즉
  본문의 "negligible within the margin of error" 는 그림이 지지하지 않는다.
  (다른 패널에서는 이런 초과를 저자가 일일이 %로 보고하는데, 이 패널에서만
  보고하지 않는다.)
- **패널 j (LAM_PE,li)**: 본문은 "**The correct amounts of LAM_PE and LLI**
  contained in the lost electrode material **were estimated**" 라고 짧게
  끝낸다. 그림에서는 LLI 가 36 → ≈30, LAM_PE 가 36 → ≈30.5 로 **둘 다 약
  5.5–6%p (상대 ~15%) 과소추정**이며, 오차 막대 상단이 진값에 겨우 닿는다.
  "correct amounts" 는 다른 패널에 적용한 기준보다 관대한 서술이다.

`[해석]` 두 지점의 공통 구조가 눈에 띈다: **오차가 LAM_PE 쪽으로 새는 방향으로
일관되게 나타난다** (d 에서 없는 LAM_PE 가 6.5% 생기고, f 에서 없는 LAM_PE 가
10% 생기고, h 에서 7%, l 에서 13 → 20 으로 부풀고, j 에서만 LAM_PE 가 줄어든다).
저자는 이것을 셀별로 다른 제작 아티팩트로 설명하지만, **"LAM_PE 방향이 다른
모드와 잘 안 갈린다"** 는 축퇴 해석도 같은 데이터를 설명한다. 논문은 이 대안
해석을 검토하지 않는다.

### 8.3 리튬 도금 임계의 유도 (§4.3.4)

`[인쇄]` 이 셀들의 NE 여유분은 **≈25%** 이고, 도금 개시까지 견딜 수 있는
LAM_NE,de 는

> LAM_NE,pl = 1 − x_NE,cell,pl / x_NE,Cell,max   … (20),  x_NE,max = 1.25

> "Equation (20) yields **LAM_NE,pl = 26.4%**, which means that any loss of
> delithiated NE material exceeding 26.4% causes the onset of lithium plating."

`[인쇄]` 36% LAM_NE,de 셀에서 도금으로 생긴 LLI ≈ **36 − 26.4 = 9.6%** 로 잡고
(도금된 리튬은 전부 비가역 = LLI 로 가정, 스트리핑 무시 [34]), 알고리즘이
LAM_NE 와 LLI 를 둘 다 margin 안에서 맞췄다고 보고한다.

`[해석]` 이 셀의 "정답 LLI = 9.6%" 자체가 **모델 계산으로 유도된 값**이다.
제작 설계값이 아니라 Eq. (20) + 도금 전량 비가역 가정의 산물이다. 즉 이
패널에서는 정답 축과 추정 축이 완전히 독립이 아니다.

---

## 9. 결과 — OCV 모델 적합 품질 (§4.1, Fig. 6)

`[도표]` Fig. 6 에 인쇄된 값을 그림에서 읽음: **RMSE_PE = 2.6 mV, RMSE_Cell =
2.4 mV, RMSE_NE = 2.2 mV** (본문의 "< 3 mV" 와 일치).

`[인쇄]` Table 5 — 5상 OCV 모델 파라미터 (기준셀 1회 적합, 이후 고정):

| 상 | E₀,PE,ᵢ [V] | a_PE,ᵢ [1] | Δx_PE,ᵢ [1] | E₀,NE,ᵢ [V] | a_NE,ᵢ [1] | Δx_NE,ᵢ [1] |
|---|---|---|---|---|---|---|
| P1 | 5.038 | 1.753 | 0.021 | 0.226 | 18.072 | 0.025 |
| P2 | 4.079 | 0.178 | 0.523 | 0.219 | 0.165 | 0.112 |
| P3 | 3.936 | 0.681 | 0.124 | 0.173 | 1.188 | 0.243 |
| P4 | 3.900 | 3.074 | 0.136 | 0.132 | 14.773 | 0.254 |
| P5 | 3.688 | 0.470 | 0.178 | 0.094 | 6.690 | 0.365 |

`[해석]` PE 의 P1 은 E₀ = 5.038 V 로 **측정 창(3.5–4.5 V) 밖**이고 Δx 도 0.021
로 작다 — 곡선 끝단을 맞추기 위한 사실상의 보정항으로 보인다. P3 와 P4 는 E₀ 가
3.936 / 3.900 V 로 서로 36 mV 차이이며 a 가 0.681 vs 3.074 로 크게 다르다.
`[해석]` **30개 파라미터 중 일부는 서로 강하게 상관돼 있을 개연성이 높지만
논문은 이를 보고하지 않는다.** 이 30개가 이후 전부 고정되어 3-파라미터 열화
추정의 **고정 기저**가 되므로, 기저의 불확실성이 열화 추정으로 어떻게
전파되는지는 이 논문 어디에도 없다.

---

## 10. §1 의 별개 발견 — 비균일 리튬화 (Fig. 2)

`[인쇄]` C/25 용량시험 후 파우치셀 5개를 Ar 글로브박스에서 개봉해 육안 검사.
만충전 셀에서 대부분의 NE sheet 는 균일하게 리튬화(금색)됐으나 **한 장은 명백히
비균일**했다. 다섯 셀의 용량 표준편차는 **< 0.2%** 였고, **비균일 sheet 를 가진
그 셀이 오히려 가장 높은 용량**을 보였다.

> "This illustrates that meso- and macro-scale inhomogeneities can not easily be
> identified in commercial Li-ion cells but they may have long term effects on
> degradation. Bottom-up physics-based models may not be able to capture such
> inhomogeneities on a micro-scale."

`[해석]` 이것이 §1 에서 저자들이 물리기반 모델 대신 **진단(diagnostic) 접근**을
택한 논거다. 우리 프로젝트가 PyBaMM(물리기반) 합성 truth 로 이 진단법을 평가하는
구조는, 이 논문의 논거와 방향이 반대다 — **논문은 "물리모델이 못 잡는 것이
있으니 진단으로 가자"고 하고, 우리는 "그 진단이 물리모델 truth 조차 못 되짚는
경우가 있는가"를 묻는다.** 둘은 모순이 아니라 서로의 상보적 시험이다.

---

## 11. 우리 프로젝트와의 접점 `[해석]`

### 11.1 우리가 재고 있는 절차와 이 논문의 절차는 **같지 않다**

| 축 | Birkl 2017 (이 논문) | 우리 저장소 문서가 서술하는 절차 |
|---|---|---|
| 자유 파라미터 | **3개** [LLI, LAM_PE, LAM_NE] | α_PE, β_PE, α_NE, β_NE 형태의 창 파라미터 (`docs/07_LAM_LLI.md` §5) |
| EoC/EoD 처리 | Δx_EoC, Δx_EoD 를 컷오프 등식 (11)(12)으로 **소거** | 창 파라미터가 자유롭게 움직임 |
| 목적함수 | full-cell 전압 RMSE, **기울기 마스크 적용** | 전압 잔차 (+ 조건에 따라 dQ/dV 항 실험) |
| 반쪽셀 표현 | 5상 해석 모델 (Eq. 1), 30개 파라미터 고정 | PyBaMM half-cell OCP |
| 최적화 | MATLAB `fmincon` active-set + MultiStart 100 | (저장소 정본 참조) |

`[해석]` **이 표가 이번 흡수의 가장 실용적인 산출물이다.** Birkl 의 컷오프
제약은 자유도를 4 → 3 (실질적으로는 창 파라미터 4개 중 2개 소거)으로 줄인다.
따라서:
- 우리가 관측하는 degeneracy 의 **일부는 Birkl 원안에는 없는 자유도**에서
  올 수 있다. 이것은 검증 가능한 가설이다.
- 반대로 Birkl 원안은 컷오프 전압 등식이 **반쪽셀 OCP 의 절대 전압 정확도**에
  직접 의존하므로, 우리가 이미 측정한 "PE 쪽 OCP 를 수 mV 왜곡하면 분해가
  무너진다"([[22p-physics-or-degeneracy]] Status Log 2026-08-20)는 **Birkl
  원안에서 더 나쁘게 나타날** 개연성이 있다.

### 11.2 저장소 문서의 인용 하나를 검증해야 한다

`degradation-degeneracy/docs/02_CODE_AUDIT.md` (읽기 전용 확인) 는
`LLI = ((1 - a_pe) + (b_pe - b_ne)) * 100` 에 **"Birkl 2017 부호 규약"** 이라는
주석을 달고 있고, `docs/04_PROMPTS.md` 도 같은 표현을 쓴다.

`[해석]` **이 논문 본문에는 α·β 형태의 창 파라미터도, 그 식도 나오지 않는다.**
본문에서 `a` 는 Eq. (1) 의 이온 상호작용 에너지이고 `Δx` 는 상 분율이다. 위
식은 Birkl 의 Eq. (7)–(10) 과 **대수적으로 관련은 있을 수 있으나 같은 식이
아니다** (Birkl 은 Δx_EoC/Δx_EoD 를 제약으로 소거한다). 저 주석의 출처는 다른
문헌(예: 참고문헌 [19] Dubarry 2012, [26] Marongiu 2016)이거나 유도 결과일 수
있다. **이 논문을 근거로는 확인되지 않는다** — 후속 확인 항목이다.
(주의: 저 문서는 RUN_SCOPE 밖 문서이므로 고쳐도 code identity 는 안 움직이지만,
이번 작업에서는 **읽기만 했고 고치지 않았다.**)

### 11.3 우리가 이 논문에 공급할 수 있는 것

`[해석]`
1. **노이즈·모델오차 하의 식별 가능성 경계.** 논문의 §4.2 는 노이즈 0 의
   inverse crime 이다. 우리 격자는 noise ∈ {0, 0.001, 0.005} 층과 OCP 왜곡
   축(`method="ocpbias"`, pe_offset_mv/ne_offset_mv/stretch)을 갖고 있다.
   Birkl 의 3-파라미터 컷오프 제약 버전을 그 격자에 얹으면 논문이 비워둔
   자리를 정확히 메운다.
2. **flat valley 의 존재 여부.** multistart 100회의 결과 분포는 논문에 없다.
   우리는 목적함수 곡률/valley 방향을 직접 잰다.
3. **오차 막대의 의미 교정.** 논문의 5.4% 는 제작 재현성이지 추정 불확실성이
   아니다. 우리가 산출하는 것은 후자다.

### 11.4 우리가 이 논문에서 가져올 수 있는 것

`[해석]`
1. **컷오프 등식 (11)(12) 자체.** 목적함수에 항을 더하는 대신 **제약을 더해
   자유도를 줄이는** 접근이며, dQ/dV 항 추가가 실패한 전례가 있는 우리에게
   값싼 대안 실험이다. (실행 주체는 satellite [[mode-observability]] 쪽이
   자연스럽다 — 본 실행이 필요 없다.)
2. **기울기 마스크의 반례로서의 가치.** Birkl 은 `|ΔE/ΔSoC| < 0.1` 구간만 쓴다.
   우리 쪽에서 **그 마스크를 켠 경우와 끈 경우**의 degeneracy 를 paired 로
   비교하면 "정보가 많은 구간을 버리는 것이 식별성에 얼마나 나쁜가"를 직접 잴
   수 있다. 논문은 이 비교를 하지 않았다.
3. **li/de 축퇴의 정확한 방향 진술.** `pure-LLI + LAM_de ↔ LAM_li`. 우리
   격자는 `lam_*_type` 을 명시적으로 갖고 있으므로 이 축퇴를 **수치로 재현**할
   수 있고, 그것은 논문의 정성 진술에 대한 정량적 확인이 된다.

---

## 12. 이 digest 를 쓰며 실제로 본 그림 (투명성)

크로핑 산출물은 **그림 8장 + 표 6장 = 14장**이다. 그중 실제로 이미지를 열어
본 것:

| 파일 | 봤나 | 무엇을 얻었나 |
|---|---|---|
| `fig_3.png` | ✅ | 메커니즘 11종 → 모드 3종 매핑 (오른쪽 "Effect" 열은 크로핑에서 잘림) |
| `fig_4.png` | ✅ | 디스크 지름 15/12/20 mm 도식 — Table 2 의 20 mm 오식 판별 근거 |
| `fig_5.png` | ✅ | 6개 모드별 OCV 모식도, 자물쇠 기호 위치, 손실률 88/72/24% |
| `fig_6.png` | ✅ | RMSE_PE 2.6 / Cell 2.4 / NE 2.2 mV |
| `fig_7.png` | ✅ | 합성 검증 3개 — RMSE 0.0 mV, Real=Estimate 완전 일치 |
| `fig_8.png` | ✅ | 코인셀 검증 6개 — RMSE 6개, 막대 12개, 오차 막대 |
| `tab_2.png` | ✅ | Table 2 의 20 mm 를 조판본에서 직접 확인 |
| `fig_1.png` | ❌ | 열화 메커니즘 셀 단면 삽화 — 우리 축(분해·식별성)에 걸리지 않아 생략 |
| `fig_2.png` | ❌ | 흑연 전극 sheet 사진(균일/비균일 리튬화) — 본문 서술로 충분 |
| `tab_1,3,4,5,6.png` | ❌ | 표는 PDF 텍스트가 정확하므로 이미지 판독 불필요 (도구 권고) |

**본문 서술과 그림이 어긋난 것**: §8.2 에 두 건 기록했다 (Fig. 8 패널 d 의
"negligible within the margin of error", 패널 j 의 "correct amounts").
그 외 확인한 그림들은 본문과 일치했다 (Fig. 5 의 12%/24% 손실, Fig. 6 의
< 3 mV, Fig. 7 의 완전 복원, Table 6 의 total LLI 열).

---

## 13. 비판적 총평 `[해석]`

**강점 (진짜로 강한 것)**
- 열화 모드를 **공학적으로 제작해서** OCV 효과를 실험으로 보인 것은, 2016년
  시점에서 문헌이 논리적 논증에만 기대던 자리를 실제로 메운다. 초록의 주장
  범위와 실제 한 일이 여기서는 일치한다.
- 컷오프 전압이 만드는 stoichiometric offset 을 모델에 넣은 것은 실질적 기여다.
  30% LLI 에서 ~2% 의 용량 "이득"이 생긴다는 것은 무시할 수 없는 크기이며,
  이를 무시하는 창 모델은 편향을 갖는다.
- **자기 방법의 축퇴를 명시적으로 진술하고 파라미터화로 대응한 점**은 이 계열
  문헌에서 드물게 정직하다. 후속 문헌이 이 문단을 인용하지 않는 것이 문제이지,
  원전이 숨긴 것이 아니다.

**약한 곳**
- "proves the ability … to **uniquely identify**" 는 근거를 넘는다. 근거는
  **노이즈 없는 3개 점의 inverse crime** 이다.
- 추정값의 불확실성이 한 번도 정량화되지 않는다. Fig. 8 의 오차 막대는 정답
  축의 제작 오차이지 추정 축의 분산이 아니며, 논문은 이 둘을 같은 그림에 겹쳐
  놓는다.
- 실험 검증 6셀 중 최소 2셀에서 **본문 서술이 그림보다 관대하다** (§8.2).
- 기울기 마스크(`< 0.1`)는 근거·민감도 없이 도입됐고, **식별에 가장 유리한
  급경사 구간을 목적함수에서 제거한다**. 저자가 피하려는 편향과, 그로 인해
  잃는 식별력의 저울질이 없다.
- 상용 노화셀 적용도, 다른 화학종 검증도 없다 (저자가 future work 로 인정).
- **모든 검증셀의 열화는 "잘라낸 균일한 조각" 이다.** §6.2 의 핵심 가정
  ("열화가 개별 상에 다르게 작용하지 않는다")을 검증 설계가 **구조적으로 시험할
  수 없게** 되어 있다. 실셀의 구조 무질서화·전이금속 용출은 정확히 그 가정을
  깨는 종류의 메커니즘이다.

**후속 인용자를 위한 경고** — 이 논문을 근거로 쓸 수 **없는** 문장:
- "OCV fitting 으로 얻은 LAM 이 리튬화/탈리튬화 중 어느 쪽인지 알 수 있다"
  → 논문이 **명시적으로 불가능하다고 적는다** (§7).
- "OCV fitting 으로 얻은 LLI 는 SEI 등 기생반응에 의한 손실이다"
  → 논문의 LLI 는 **total** 이며 lithiated LAM 안의 리튬을 포함한다.
- "이 방법은 유일해를 준다"
  → 저자의 문장은 있으나 근거는 무노이즈 3점이다.
- "LLI 셀의 전극 지름은 20 mm 였다" → Table 2 와 본문이 모순한다.
