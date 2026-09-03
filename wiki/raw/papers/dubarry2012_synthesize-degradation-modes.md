---
source_url: local-upload/3._Synthesize_battery_degradation_modes_via_a_diagnostic_and_prognostic_model.pdf
ingested: 2026-09-03
sha256: 4d9e43e82cc104ce50aff64bd40df19678d8c8d293ead14e85e53897ed042f76
---

# 수집 목적

M. Dubarry, C. Truchot, B.Y. Liaw, **"Synthesize battery degradation modes via a
diagnostic and prognostic model"**, *Journal of Power Sources* **219** (2012)
204–216 의 **절별 해체분석**.

`[인쇄]` PDF 1쪽에서 직접 재확인한 서지 (Birkl 2017 참고문헌 [19] 로 지목된 것):

> Journal of Power Sources 219 (2012) 204e216
> http://dx.doi.org/10.1016/j.jpowsour.2012.07.016
> 0378-7753/$ e see front matter (c) 2012 Elsevier B.V. All rights reserved.
> Received 29 May 2012 / Received in revised form 6 July 2012 / Accepted 7 July 2012 / Available online 24 July 2012
> Hawaii Natural Energy Institute, SOEST, University of Hawaii at Manoa, 1680 East-West Road, POST 109, Honolulu, HI 96822, USA

즉 요청받은 서지 (저자 3인 · JPS 219 (2012) 204–216 · DOI 10.1016/j.jpowsour.2012.07.016)
는 **전부 1쪽에서 확인**된다. `e` 는 PDF 텍스트층이 en-dash 를 치환한 것이고
`1⁄4` 는 `=` 의 치환이다 (이하 인용에서 `=` 로 정규화해 표기하며, 그 사실을
매번 밝힌다).

**흡수의 첫째 이유**: 우리 저장소 `degradation-degeneracy` 의
`docs/02_CODE_AUDIT.md` 와 `docs/04_PROMPTS.md` 가
`LLI = (1−α_PE) + (β_PE − β_NE)` 에 **"Birkl 2017 부호 규약"** 이라는 주석을
단다. 직전 흡수에서 **Birkl 2017 본문에는 α·β 창 파라미터도 그 식도 없다**는
것이 확인됐다 (`raw/papers/birkl2017_degradation-diagnostics-ocv.md` §11.2).
이 논문이 그 진짜 출처인지 판정하는 것이 §10 이다.

---

# 원문에 없어서 확인이 필요한 것 (공백 목록)

이 절을 먼저 둔다. 아래는 **논문이 말하지 않은 것**이며, 이 digest 어디에서도
채우지 않는다.

1. **역문제(fitting)가 없다.** 이 논문은 **정방향 전용**이다. 모드 → 곡선을
   합성할 뿐, 곡선 → 모드를 푸는 알고리즘·목적함수·최적화기·경계값이 **본문에
   전혀 없다**. "diagnostic" 은 사람이 IC/DV 서명을 눈으로 대조하는 것을 뜻한다.
2. **식별 가능성 진단이 없다.** 파라미터 상관·공분산·Hessian·신뢰구간·유일성
   증명·노이즈 스윕이 **하나도 없다** (전수 확인은 §11).
3. **격자(grid)가 없다.** 모드를 조합해 돌린 스윕의 **점 개수**가 인쇄되지
   않는다. 제시된 것은 단독 모드 스윕(모드당 6단계)과 **조합 시나리오 2건**뿐이다.
4. **실측 대조가 이 논문 안에 없다.** Fig. 3 의 half-cell C/2·2C 검증을 빼면,
   모든 그림이 시뮬레이션이다. 셀 실측과의 비교는 전부 참고문헌 [4],[6],[27] 로
   넘긴다. [27] 은 `J. Power Sources (in preparation)` — 이 논문 시점에 **미출간**.
5. **LR·OFS 의 역산 공식이 없다.** Eq. (5),(8') 은 모드 → (LR, OFS) 방향이다.
   그 역(관측된 LR·OFS → 모드)은 **쓰여 있지 않다**.
6. **파라미터 수치표가 없다.** ECM 의 R1/R2 값, 반쪽셀 OCP 원자료 수치는
   인쇄되지 않았다 (LFP·graphite 데이터는 Hydro-Quebec·Timcal 제공이라고만 적음).
7. **Fig. 12 와 Fig. 3 은 캡션 기반 크로핑에서 영역이 잡히지 않았다** (본문에
   직접 삽입된 인라인 플롯). 두 그림은 **보지 않았다** — 아래 서술은 본문
   텍스트에만 근거한다.
8. **NE 가 graphite, PE 가 LFP 인 단일 화학종**이다. 저자 스스로 결론에서 LFP 의
   평탄 plateau 때문에 두 모드가 안 갈린다고 적는다 (§11). 다른 화학종에서의
   재현은 이 논문에 없다.

---

# 1. 논문이 묻는 것과 답 (Abstract · §1 Introduction, p.204–205)

`[인쇄]` Abstract:

> "Here we present a novel mechanistic model that can enable battery diagnosis and
> prognosis. The model can simulate various "what-if" scenarios of battery
> degradation modes via a synthetic approach based on specific electrode behavior
> with proper adjustment of the loading ratio and the extent of degradation in and
> between the two electrodes."

`[인쇄]` Highlights 4줄:

> < A unique and novel inference technique for battery diagnosis and prognosis.
> < A mechanistic model creates "what if" scenarios from degradation modes or their combinations.
> < A physicochemical model based on electrode degradation mode, cell design and operating condition.
> < Versatile for various chemistries, designs, sizes, geometries, operating or aging conditions.

`[인쇄]` 문제 제기 (§1, p.205):

> "since both electrodes in the cell contribute to the features (peaks and their
> shape) in the IC and DV curves, it is difficult to separate the electrode behavior
> and its contribution to the cell degradation. A technique that can resolve this
> issue would be highly desirable"

`[해석]` **이것이 우리 질문과 같은 문장이다.** 다만 답의 방향이 반대다 —
Dubarry 는 "곡선에서 전극 기여를 분리하는 역문제를 풀자" 가 아니라 **"모드를
가정해 곡선을 합성해 놓고 실측 서명과 대조하자"** 로 간다. 역문제를 우회한다.

`[인쇄]` 계보 (§1):

> "This approach conceptually follows the one described by Christensen and Newman
> in the early 2000s [13,14] and used by others such as Zhang et al. [15,16] and
> Delacourt et al. [17,18] to simulate cell degradation."

`[인쇄]` 기존 fitting 계열에 대한 저자들의 비판 (§1) — **우리 절차가 속한 계열이다**:

> "some groups used experimental half-cell data and fitting techniques to compose
> dV/dQ curves [7,8,11,19e21] for some specific studies. These experimental
> approaches may provide the benefits for case study and analysis; however, the
> applicability of the knowledge to other chemistries, cell designs, or operating
> conditions is limited, since they are after all empirical ones."

`[해석]` 저자들은 half-cell fitting 을 **"결국 경험적"** 이라고 격하한다. 즉 이
논문은 우리가 판정하는 절차(Birkl 계열 fitting)의 **원전이 아니라 그 대안**으로
자기를 위치시킨다. 이 구도는 §10 판정에서 중요하다.

---

# 2. 모델 구조 — 2층 (§2, p.205)

`[인쇄]`

> "The mechanistic model proposed in this work is composed of two layers: a top
> layer with cell configuration and inputs from cell operating and degradation modes
> and a sub-layer with half-cell modules that describe the electrode behavior."

`[인쇄]` **핵심 방향 선언** (§2, p.205) — 제목의 "synthesize" 의 정의:

> "In contrast to conventional electrochemical or electrical models, in which the
> degradation results are outputs of the simulation, ours is a "backward looking"
> approach — the "what if" scenarios of degradation are the inputs to the simulation
> of the cell behavior in aging."

`[해석]` **"synthesize" = 모드를 입력으로 넣어 곡선을 정방향 합성한다**는 뜻이
맞다. 저자들이 "backward looking" 이라 부르는 것은 **인과의 방향**(결과가 아니라
원인을 입력으로 둔다)이지 수치적 역문제가 아니다. 용어에 속지 않아야 한다.

`[인쇄]` 구현: "The model is written in MATLAB".

**Fig. 1 (직접 봄, `figures/…/fig_1.png`)** — `[도표]` 도식은 좌상단에 PE 쪽
ECM 2개(직렬 박스, 각각 V₀·R₁·R₂//C), 좌하단에 NE 쪽 ECM 2개가 상하 대칭으로
배치되고, 각각 화살표로 `V_PE(SOC_PE)` 와 `V_NE(SOC_NE)` 를 낸다. 중앙의
`Full cell module` 로 두 전극 전위가 들어가고, **오른쪽에서 "Inputs from
degradation modes" 화살표가 full cell module 로 직접 꽂힌다.** 출력은
`V_cell = V_PE − V_NE`. 각 ECM 으로 되돌아가는 점선에 "Chemistry, rate, extent
of reaction (rxn)" 이 붙어 있다. `[해석]` 열화 모드가 **half-cell 모듈이 아니라
full-cell 모듈(top layer)로 들어간다**는 것이 도식에서 명확하다 — LAM·LLI 는
전극 곡선 자체를 바꾸지 않고 **두 곡선의 정합(LR·OFS)만 바꾼다**. 이것이 이
논문 전체의 구조이며 §10 판정의 근거다. (예외: ORI·FRD·FPP 는 sub-layer 로
들어간다 — §6.)

---

# 3. Half-cell sub-layer (§2.1, p.206)

`[인쇄]` 저항 정의, 식 (1) (`1⁄4`→`=`, `` → `−` 로 정규화):

> R_exp(C, SOC) = [V_OCP(SOC) − V_C(C, SOC)] / abs(I_C)    … (1)

> "R_exp(C,SOC) is the sum of R1 and R2, where R1 corresponds to the ohmic
> resistance calculated from the initial voltage drop after current is applied [23]
> and R2 the faradic resistance that is rate and SOC dependent in the ECMs [22,23]."

`[인쇄]` 데이터 출처와 rate 목록:

> "Hydro-Quebec and Timcal kindly provided the half-cell data for the LFP and
> graphite electrodes at different rates, respectively. For the LFP electrode, the
> parameters used to construct the sub-layer module are compiled from the discharge
> data at C/8, C/4, C/2, C/1, 2C and 4C. For the graphite electrode, the parameters
> are compiled from the charge data at C/50, C/5 and 5C."

`[해석]` NE(graphite) 는 **3개 rate** 로만 파라미터화된다 (PE 는 6개). rate 외삽
품질이 NE 쪽에서 더 낮을 수밖에 없는데, 논문은 이 비대칭을 논의하지 않는다.

`[인쇄]` 검증 (Fig. 3 — **보지 않음**, 크로핑 실패):

> "a specific rate (e.g. C/2 and 2C, respectively) is removed from the parameter
> matrix for the sub-layer module construction. The module thus constructed shall
> simulate the discharge curve for this rate and the result is compared with the
> experimental data. As shown in the figure, respectively, the simulation and
> experimental data for C/2 and 2C are in excellent agreement."

`[해석]` leave-one-rate-out 검증이다. **정량 지표(RMSE 등)는 인쇄되지 않고
"excellent agreement" 라는 말만 있다.**

`[인쇄]` 전극별 전류밀도 분리의 근거:

> "(1) the current density applied to the cell should be treated differently in the
> electrodes, depending on the apparent area used by each electrode. (2) The current
> density at each electrode may also vary, depending on the aging condition and
> degradation mode."

---

# 4. ★ Full cell model — 파라미터화의 정본 (§2.2, p.206–207)

**이 절이 §10 판정의 1차 근거다.**

`[인쇄]` 두 개의 필수 파라미터:

> "To emulate the cell behavior from the electrode sub-layers effectively, two
> parameters are essential: the loading ratio (LR) between the negative and the
> positive electrode (NE and PE); i.e. **LR = Q_NE/Q_PE**, and the initial
> irreversible capacity loss of the NE that compensates the SEI formation."

`[인쇄]` 좌표계 선택:

> "Because of the uncertainty in the initial capacity loss at the NE, it is more
> convenient and reliable to use the SOC scale at the PE (SOC_PE) as the basis for
> the calculation of cell SOC."

`[인쇄]` 식 (2) — NE 곡선을 PE 축으로 변환 (원문 표기 그대로, `` = 곱셈 기호):

> SOC_NE = (100% − SOC_NE) · LR_o      … (2)

`[해석]` 좌변과 우변에 같은 기호 `SOC_NE` 가 쓰였다 — **원문 조판이 좌변의
"PE 축으로 표현된 NE 의 SOC" 를 구분해 인쇄하지 못한 것**으로 보인다 (본문
설명은 "the V_NE = f(SOC_NE) curve can be transformed and scaled as a function of
SOC_PE, V_NE = f(SOC_PE)" 다). 즉 실질은
`(PE 축 좌표) = (100% − SOC_NE)·LR` 이다. 이 판단은 `[해석]` 이다.

`[인쇄]` 그 물리적 읽기:

> "In this representation, 100% SOC_NE (fully delithiated NE) corresponds to 0%
> SOC_PE, whereas 0% SOC_NE (fully lithiated NE) should correspond to 145% SOC_PE
> because of the LR_o = 1.45 in the capacity conversion."

`[인쇄]` SEI 형성분의 처리 — **offset 의 도입**:

> "In Fig. 4, an irreversible 8.5% active material loss on the NE is assumed, which
> is equivalent to 12% capacity loss in the full cell, based on the LR calculation
> (i.e. 8.5% × 1.45 = 12%)"

> "For convenience in the simulation, an **SOC_PE offset (OFS)** and an apparent LR
> are used in the model to calculate the full cell behavior upon initial SEI layer
> formation. This initial offset (OFS_ini) corresponds to the shift of the V_NE in
> correspondence to the V_PE on the SOC_PE scale and the amount of graphite loss in
> the first cycle."

`[인쇄]` 식 (3):

> LR_ini = [(100% − OFS_ini)/100%] · LR_o      … (3)

`[인쇄]` 수치: "an offset of OFS_ini = 12% SOC and LR_ini = 1.3 shall yield
approximately the same composition after the initial irreversible capacity loss
during cell formation (from 8.5% loss in NE and LR_o = 1.45)."

`[인쇄]` 식 (2') — **이 논문에서 가장 중요한 식**:

> SOC_NE = (100% − SOC_NE) · LR_ini + OFS_ini      … (2')
>
> "Equation (2') is generally true, including situations with degradation as well."

`[해석]` **이것이 창(window) 파라미터화다.** PE 축 위에서 NE 곡선은
**폭 = 100%·LR (scaling)**, **왼쪽 끝 = OFS (offset)** 인 창으로 놓인다. 우리
코드의 `windowed_curve` 가 `x ∈ [β, β+α]` 로 쓰는 것과 **구조가 같다**
(대응: α ↔ LR, β ↔ OFS). 다만 이 논문의 창은 **NE 하나뿐**이다 — PE 는 축 자체
(0–100% SOC_PE)로 고정된다.

**Fig. 4 (직접 봄) — 파라미터화 도식** `[도표]`:
- x축 `Initial SOC_PE (%)` 0–150, y축 `Voltage (V)` 0–4.
- 파란 실선 = Positive electrode: 약 2.2 V 에서 급상승해 3.4 V 평탄부, **0% 에서
  시작해 100% 에서 끝난다** (100% 직후 3.7 V 로 수직 상승).
- 검은 점선 = "Negative electrode as built", 검은 실선 = "Negative electrode after
  initial SEI formation". 점선은 x=0 에서, 실선은 **x≈12% 에서** 1.5 V 로 시작해
  급강하 후 0.1–0.2 V 평탄부로 간다.
- 빨간 실선 = Full cell, x≈12% 에서 1.9 V 로 시작.
- **치수선 3개가 명시적으로 그려져 있다**: 왼쪽에 `OFS_ini` (0 → ≈12%),
  그 오른쪽부터 끝까지 `100% SOC_NE × LR_ini` (≈12% → ≈145%), 그리고 그 아래
  x=0 부터 ≈143% 까지 `100% SOC_NE × LR_o`.
- 왼쪽 아래 파란 굵은 화살표 + "Initial loss" 라벨이 점선→실선의 우측 이동을 표시.

`[해석]` **α·β 창 그림 그 자체다.** "폭 = LR" 과 "시작점 = OFS" 가 치수선으로
직접 인쇄돼 있다. 우리 코드 주석이 그리는 그림과 동일한 기하다.

`[인쇄]` ps-OCV 와 SOC 환산, 식 (4):

> SOC(V_cell) = [SOC_PE(V_cell) − SOC_PE(OCV_cell^EOD)] / [SOC_PE(OCV_cell^EOC) − SOC_PE(OCV_cell^EOD)] × 100%   … (4)

> "the pseudo-OCV of the cell (ps-OCV_cell) … is obtained from averaging the charge
> and discharge curves of each electrode measured at a very slow rate (such as C/25
> or lower) [6]"

`[인쇄]` "The EOD SOC depends on the given cutoff condition used; e.g. 2.5 V in this study."

`[해석]` 컷오프가 **2.5 V 하나만** 인쇄된다. Birkl 처럼 컷오프 등식으로 자유도를
소거하는 장치는 **없다** — 여기서 컷오프는 SOC 정규화의 기준일 뿐이다.

---

# 5. ★ 열화 모드 — 분류 체계와 식 (§3, §3.1, p.207–209)

## 5.1 분류 체계의 정본

`[인쇄]` (§3, p.207) — **li/de 4분류의 정의문**:

> "Another common degradation mode is the loss of active material (LAM)
> [4,6,14,16,17,20,29,30], which can be further categorized into **four types,
> depending on the affected electrode and the degree of lithiation (i.e.
> predominantly in a lithiated or de-lithiated state) in which the LAM occurs.**"

`[인쇄]` (§3.1, p.208) — **기호 규약**:

> "Each type of LAM is noted by the electrode in which it occurs (in the subscript),
> with a prefix that specifies the state of lithiation; i.e. **"li" for lithiated and
> "de" for delithiated**."

`[해석]` **Birkl 2017 의 `LAM_liPE`/`LAM_dePE`/`LAM_liNE`/`LAM_deNE` 4종 구분은
여기서 왔다.** 명명 규칙(전극=아래첨자, 리튬화 상태=접두)까지 동일하고, Birkl 은
이 논문을 [19] 로 인용한다. **이 항목은 판정 (a) "여기가 출처다" 다.**

`[인쇄]` 전체 모드 목록 (§3, §3 마지막 문단, §5.1 제목):
- **LLI** (loss of lithium inventory) — SEI 형성 [4,6,14,16,17,20,29,30], Li plating [31] 로도 유발.
- **LAM 4종** — 원인으로 grain isolation [32], transition metal dissolution,
  electrode composition change [33,34], crystal structure change (decomposition·
  oxygen evolution) [35] 를 든다.
- **FRD** (faradic rate degradation) — charge-transfer kinetics 지연 [6,30,34,36].
- **ORI** (ohmic resistance increase) — 전극 접촉·전해질 전도 열화 [13].
- **FPP** (formation of parasitic phases) [35].

`[인쇄]` 층 배정 (§3, p.208):

> "The full cell layer can handle the four types of LAM and LLI, whereas the
> half-cell sub-layer can handle ohmic resistance increase, faradic rate
> degradation, and formation of parasitic phases that are electroactive."

## 5.2 ★ LAM → LR : 식 (5)

`[인쇄]`

> "A loss of active material (AM) will affect the LR. Disregarding if the AM is
> lithiated or not, as long as some PE AM is lost, the LR will increase. Similarly,
> the LR will decrease if NE AM is lost. Given a 50% AM loss, the LR will double if
> some PE AM is lost and reduce by half if some NE AM is lost."

> LR = LR_ini · [ (100% − %LAM_deNE − %LAM_liNE) / (100% − %LAM_dePE − %LAM_liPE) ]      … (5)

`[해석] ★★` **LR 은 li/de 를 구분하지 못한다** — 분자·분모 안에서 두 종류가
**합으로만** 들어간다. 저자 스스로 "Disregarding if the AM is lithiated or not"
이라고 적는다. 즉 scaling 축에서 li/de 는 **원리적으로 축퇴**다. 이것은 §11 의
축퇴 논의의 대수적 뿌리다.

## 5.3 전극별 실제 rate : 식 (6),(7)

`[인쇄]`

> C_PE = 100%·C_imp / (100% − %LAM_dePE − %LAM_liPE)      … (6)
> C_NE = 100%·C_imp / [ LR·(100% − %LAM_deNE − %LAM_liNE) ]      … (7)

> "The LAM will also change the rate on the affected electrode, since it decreases
> both the material content that can accept charge and the active surface area and
> thus increases the current density."

`[해석]` **LAM 이 자동으로 rate 를 올린다** — 이것이 §7 의 "LAM 이 저항 증가로
오독된다" 주장의 기계다. 우리 격자에는 없는 결합이다.

## 5.4 ★ LAM → OFS : 식 (8), 그리고 LLI → OFS : 식 (8')

`[인쇄]` 어느 LAM 이 offset 을 움직이는가:

> "In the simulation, as the condition of EOD does not change, the OFS_ini remains
> the same and a simple adjustment of the LR is sufficient to emulate both cases."
> (LAM_liPE 와 LAM_deNE 의 경우)

> "Additional adjustment to the model is needed to simulate these two cases, since
> the EOD of the affected electrode is evolving with aging; so is the LR matching
> with the opposite electrode. The simulation requires adjustments in both LR and SOC
> offset." (LAM_dePE 와 LAM_liNE 의 경우)

> OFS = OFS_ini + LR · %LAM_liNE + (LR/LR_ini) · %LAM_dePE      … (8)

`[인쇄]` LLI 를 넣은 완성형 — **이 논문에서 LLI 가 등장하는 유일한 식**:

> OFS = OFS_ini + LR·%LAM_liNE + (LR/LR_ini)·%LAM_dePE + %LLI_ch − %LLI_dis      … (8')

> "The subscripts of "ch" and "dis" are for "charge" and "discharge" regimes,
> respectively. In the follow-on discussion, only LLI_ch is considered; thus, the
> notation LLI refers to LLI_ch, unless specified."

`[인쇄]` LLI 의 물리 (p.208–209):

> "LLI occurs when reversible Li ions are partially consumed by parasitic reactions
> in the cell. LLI commonly occurs during charging when Li ions are used to grow the
> passivation layer on the NE. It may also occur during discharging if a passivation
> layer consuming Li is growing on the PE. Fig. 7 illustrates the case for a charge
> regime, where LLI does not affect the EOC SOC_PE, since the PE is releasing the
> Li-ions. The SOC_PE at EOC of the NE is however evolving with aging and becoming
> lower cycle by cycle; since less Li ions are inserting in the NE each time."

`[해석] ★★★` **식 (8') 이 이 논문의 축퇴 그 자체다.** 세 개의 서로 다른 모드
(`LAM_liNE`, `LAM_dePE`, `LLI`)가 **단 하나의 스칼라 OFS 에 덧셈으로 들어간다.**
LLI 의 계수는 1, LAM_liNE 은 LR, LAM_dePE 는 LR/LR_ini. 논문은 이 사실을 **한
번도 축퇴라고 부르지 않는다.**

**Fig. 6 (직접 봄) — 4종 LAM 의 창 변화** `[도표]`. 4패널 모두 x축
`Initial SOC_PE (%)` 0–150, y축 `Voltage (V)` 0–4. 파란=PE, 검정=NE, 빨강=full
cell, 점선=10% 증분, 실선=초기/50% 손실.
- **(a) LAM_liPE**: PE 곡선의 **오른쪽 끝**이 100% → 약 50% 로 당겨진다 (파란
  굵은 화살표가 **왼쪽**을 가리킴, ≈3.6 V 높이, x≈50–100 구간). NE 곡선은
  **전혀 움직이지 않는다**. 치수선 없음 (OFS 불변).
- **(b) LAM_dePE**: PE 곡선의 **왼쪽 끝**이 0% → 약 50% 로 밀린다 (화살표
  **오른쪽**, x≈15–50). 왼쪽 아래에 `OFS_ini` (짧음) 와 그 오른쪽에 **`OFS`
  (김, ≈12%→≈50%)** 치수선이 **둘 다** 그려져 있다.
- **(c) LAM_deNE**: NE 곡선의 **오른쪽 끝**이 ≈143% → ≈100% 로 당겨진다 (화살표
  **왼쪽**, y≈0.15 V, x≈50–100). 치수선 없음 (OFS 불변). PE·full cell 은 거의
  겹쳐 있다.
- **(d) LAM_liNE**: NE 곡선의 **왼쪽 끝**이 ≈12% → ≈78% 로 밀린다 (화살표
  **오른쪽**). `OFS_ini` 와 **`OFS` (≈12%→≈78%)** 치수선 둘 다 있음.

`[해석]` 그림이 식 (8) 을 정확히 그린다: **왼쪽 끝(=β)을 움직이는 것은 dePE 와
liNE 뿐**이고, liPE·deNE 는 **오른쪽 끝만** 줄인다(=폭 α 만 변함).

**Fig. 7 (직접 봄) — LLI** `[도표]`. x축 0–200 (다른 그림보다 넓다), y축 0–4.
NE 검은 곡선이 **폭을 유지한 채 통째로 오른쪽으로 평행이동**한다: 왼쪽 끝
≈12% → ≈62% (굵은 화살표 오른쪽, y≈1.1), **동시에 오른쪽 끝도 ≈143% → ≈190%
로 이동**한다 (x≈150 위치에 두 번째 오른쪽 화살표, y≈0.1). `OFS_ini` 와
`OFS`(≈12%→≈62%) 치수선. PE 파란 곡선은 0–100% 에 **고정**.

`[해석] ★★★` **LLI = NE 창의 순수 평행이동 (β 증가, α 불변)**. LAM = 창 폭
축소(± 한쪽 끝 이동). 이 두 그림이 우리 코드의 α·β 기하를 **1:1 로 시각화**한다.
그리고 두 번째 화살표(오른쪽 끝도 같이 이동)가 **평행이동임을 증명**한다 — 폭이
줄어드는 LAM 과 구분되는 유일한 표식이다.

`[해석] ★ 대수적 귀결 (원문에 없음, 우리가 유도)`: 식 (5)+(8') 에서
`{LAM_liNE = x}` 와 `{LAM_deNE = x, LLI = LR·x}` 는 **LR 과 OFS 를 모두 동일하게
만든다** (LR: 분자에 li/de 가 합으로만 들어가므로 동일. OFS: 전자는 `+LR·x`,
후자는 `+LR·x`). 즉 **두 시나리오는 top layer 에서 완전히 구별 불가**다.
이것은 Birkl 2017 §4.2 가 5년 뒤 명시적으로 진술한 축퇴
("a combination of e.g. LLI and LAM_NE,de creates the same OCV signature as an
equal amount of LAM_NE,li") 와 **정확히 같은 명제**이며,
**이미 2012년 이 논문의 식 (5),(8') 안에 대수적으로 들어 있다.** Dubarry 는
그것을 쓰지 않았다.

---

# 6. sub-layer 로 들어가는 모드: ORI · FRD · FPP (§3.2, p.209–210)

`[인쇄]` **ORI**, 식 (9):

> V_cell@C_imp = [V_PE@C_PE − C_PE·R_PE·(%ORI_PE/100%)] − [V_NE@C_NE + C_NE·R_NE·(%ORI_NE/100%)]   … (9)

시나리오: "ohmic resistance increase (ORI) by 100% in the PE and 66% in the NE …
on a 2C discharge curve". "the potential of each electrode is altered by the
amount of ORI with **no change in the LR or the SOC offset**."

`[인쇄]` **FRD**, 식 (10),(6'),(7'),(9'):

> RDF_PE = C_RD / C_PE      … (10)
> C_PE = 100%·RDF_PE·C_imp / (100% − %LAM_dePE − %LAM_liPE)      … (6')
> C_NE = 100%·RDF_NE·C_imp / [ LR_ini·(100% − %LAM_deNE − %LAM_liNE) ]      … (7')
> V_cell@C_imp = [V_PE@C_PE − C_PE·R_PE·(%ORI_PE/100% + RDF_PE − 1)] − [V_NE@C_NE + C_NE·R_NE·(%ORI_NE/100% + RDF_NE − 1)]   … (9')

> "the FRD is simulated by "downgrading" the reaction kinetics to a lower rate (C_RD)
> than the initial one imposed on the PE (C_PE), while maintaining the initial IR
> drop to its C_PE value"

`[해석]` 식 (7) 은 분모에 `LR`, 식 (7') 은 `LR_ini` 를 쓴다 — **원문에서 기호가
바뀐다**. 오식인지 의도인지 본문이 설명하지 않는다. 미확인 항목이다.

`[인쇄]` **FPP** (§3.2.3): 비반응성 상이면 LAM 으로 모델링. 반응성이면 composite
전극으로. LFP 예시:

> "if 30% of the hydrated phase is present, the EOD SOC should be offset by
> (1−0.8)*30% = 6%"

> "The presence of 10% hydrated phase is not going to create any noticeable changes
> in capacity with the existing cutoff, because the induced SOC offset and changes
> in the OCV = f(SOC) curve occur in the range of OFS_ini."

`[인쇄]` Li plating (§3.2.3):

> "Li plating often occurs under two conditions: (1) if the IR_NE drop of the NE
> during charging makes the NE potential goes ≤ 0 V or (2) if the LAM_deNE is
> significant to reach a condition where overcharging in NE happens (dotted line in
> Fig. 6(c)). If the plated Li is passivated progressively [42], it will result in
> additional LLI."

`[해석]` Fig. 6(c) 에서 내가 본 `x≈100%` 의 파란 수직 점선이 이 "Li plating 위험"
표시다. 본문 §3.1 도 "when 0% SOC_NE is reached earlier than 100% SOC_PE on the
PE scale (dotted line on Fig. 6(c)) the cell is at risk of Li plating" 이라 적어
그림과 일치한다.

---

# 7. ★ 모드 조합 — "격자" 에 해당하는 것 (§3.3, p.210)

`[인쇄]`

> "In the previous sections, the simulation of individual degradation mode (e.g.
> LAM, LLI, ORI, FRD and FPP) was discussed. **By combining all the equations, this
> model is capable of simulating degradation modes with multiple concurrent
> processes in an electrode or both.**"

> "Fig. 10(a) shows a scenario of degradation mode comprising a **logarithmic
> increase of LAM_liNE, an exponential increase of LAM_dePE and a linear progression
> of LLI over 100 cycles** of aging."

`[해석] ★` **조합은 가능하고 실제로 돌렸다 — 그러나 격자가 아니다.** 인쇄된
조합 실행은 **2건뿐**이다: Fig. 10 (3모드 × 100 cycle) 과 Fig. 17 (2모드 ×
500 cycle). 나머지 그림(6,7,12,13,14,15)은 **전부 단독 모드 스윕**이다
(모드당 초기 + 5증분 = 6단계, 최대 30–50%).

`[해석] ★★ 우리 프로젝트와의 관계`: **정방향 합성(모드 → 곡선)이라는 발상
자체는 우리보다 13년 앞선 선행이다.** 다만 결정적으로 다르다 —
(i) 이 논문은 **역방향 fitting 을 하지 않으므로 truth 대비 복원 오차를 잴 수
없다**, (ii) **격자(다차원 스윕)가 없다** — 단독 축 스윕 + 조합 2건, (iii)
noise 층이 없다. 즉 **"합성 truth 를 만든다" 는 우리 방법론의 선행이지만,
"합성 truth 로 식별 가능성을 판정한다" 는 이 논문에 없다.** 선행 인정은 여기까지가
정확하다.

---

# 8. 적용 1 — 셀 설계가 LLI 의 가시성을 바꾼다 (§4.1, p.211–212)

`[인쇄]` 두 설계:

> "a high power (HP) design with a high graphite content for high rate capability
> and a high energy (HE) design of a lower LR with low rate capability and high
> energy content (see details in Ref. [27])."

`[인쇄]` 동기 — 실측에서 온 수수께끼:

> "our previous study [4] of an HE cell in which the cell exhibited a unique behavior
> in its first 100 cycles of aging where capacity fading was observed at lower rates
> but not higher ones, yet the cell seemed discharged to a lower SOC progressively."

`[인쇄]` 결과:

> "In the HE design, the trend of capacity fade is different from the other two. At
> first, the capacity @2C is much lower than the other two (because of the HE design)
> but stays stable over a range of cycles, although LLI is recurring in the cell.
> **Upon reaching 15% LLI, the capacity fade begins to appear** and follows the same
> trend as the other two."

> "Fig. 11(b) shows the evolution of the EOD SOC, which tends to increase slightly
> for C/25 and HP@2C discharges but **decreased by 20% for the HE@2C discharge**
> before stabilizing"

`[인쇄]` 기계:

> "In the HP design (Fig. 11(c)), the cell can deliver capacity close to its maximum
> at 2C and the **capacity-limiting electrode is the NE**. This is not the case for
> the HE design. Because of the lower inhered rate capability, the **capacity is
> initially limited by the PE**."

> "Since the NE is the limiting electrode for the HP design, its capacity fade will be
> reflected immediately in the cell capacity loss; on the contrary in the HE design,
> as long as the PE is limiting the capacity, the NE capacity fade would not be
> detected."

**Fig. 11 (직접 봄)** `[도표]`:
- (a) x축 `% Loss of lithium inventory` 0–50, y축 `Normalized capacity (%)` 30–100.
  검정 실선 C/25 는 **직선**으로 `figure-read ≈` 98% → 41%. 파란 점선 HP-2C 는
  ≈94% → ≈39% (C/25 보다 약간 아래, 거의 평행). 빨강 점선 HE-2C 는 **0–13% LLI
  구간에서 ≈76% 로 평탄**하다가 꺾여 내려와 ≈33% LLI 부근에서 C/25 곡선과
  합류하고 이후 겹친다.
- (b) y축 `SOC_EOD (%)` 0–25. HE-2C(빨강)만 ≈21% 에서 급강하해 ≈20% LLI 에서
  ≈2% 로 바닥을 치고 이후 완만히 상승. C/25(검정)는 ≈0.2% 에서 거의 수평,
  HP-2C(파랑)는 ≈1.4% → ≈3.5% 로 완만 상승.
- (c),(d) x축 `Initial Li-ion SOC (%)` −20–160. LLI 10% 증분의 점선 다발.
  (c) HP: 빨간 full-cell 곡선들의 **왼쪽 끝이 0 → ≈35% 로 이동**, 검은 NE 곡선도
  같이 오른쪽으로 이동. (d) HE: 빨간 곡선의 왼쪽 끝이 ≈20 → ≈37% 로 이동하는데
  **초기 곡선(실선)이 이미 x≈20% 에서 시작**한다 (HP 는 x≈0).

`[해석] ★` 우리에게 직접 걸리는 것: **같은 %LLI 가 셀 설계에 따라 용량손실로
전혀 안 나타날 수 있다 (HE 에서 0–13% LLI 구간 용량 불변).** 즉 용량손실을
관측으로 쓰는 순간 LLI 는 **국소적으로 관측 불가능**해진다. 이것은 우리
degeneracy 와 다른 종류의 실패(비관측성)이며, `[해석]` 우리 격자가 단일 설계
(단일 LR)에서만 돌고 있다면 이 축은 아예 재지 못한다.

---

# 9. ★ 적용 2 — IC/DV 서명과 저자들이 인정한 구별 불가 (§4.2, p.212–214)

## 9.1 peak 의 물리 귀속

`[인쇄]`

> "The graphite staging phenomena are numbered as ① to ⑤, where ① is the reaction
> from LiC12 to LiC6 and so on, and ⑤ the last staging transition leading to the
> delithiated graphite (as shown in Fig. 12). In the dQ/dV = f(V) curve, **these five
> staging phenomena coupled with the LFP potential plateau are observed as five IC
> peaks** [4]. In the DV analysis, these five staging phenomena become valleys in the
> dV/dQ = f(Q) curve. There are **four dV/dQ peaks representing non-stoichiometry in
> the single-phase regions (solid solution), as noted by A to D.**"

`[해석] ★★ PVS 물리 귀속과의 대조`: 이 논문에서 **IC 의 5개 peak 은 전부
graphite(NE) staging 에 귀속**된다. PE(LFP) 는 평탄 plateau 로서 **전압 좌표를
제공할 뿐 peak 을 만들지 않는다.** 이는 2026-09-02 세미나의 PVS 물리 귀속
(peak2 = PE, valley2 = NE) 과 **직접 충돌하지 않는다** — 화학종이 다르다
(LFP 는 2상 평탄, NMC/NCA 는 solid-solution 이라 PE 가 자체 peak 을 만든다).
그러나 **Kim 2023 계열의 "IC peak 은 음극 귀속" 진술과는 같은 방향**이다.
`[해석]` 정확히 말하면: **LFP||graphite 에서는 IC peak 의 PE 귀속이 성립하지
않는다**는 것이 이 논문의 진술이고, 세미나의 PE 귀속은 다른 화학종을 전제한다.
두 진술을 같은 슬라이드에서 인용하면 안 된다.

**Fig. 13 (직접 봄) — IC 서명 6패널** `[도표]`. x축 `Voltage (V)` 3.1–3.35,
y축 `Incremental capacity (%Q/V)` **−6,000 – 0** (방전이라 음수). 굵은 실선=초기,
가는 실선=30% 열화 종료, 점선=1/5 증분. 패널 (a) 에 라벨: ①≈3.30 V(깊이
≈−2,400 초기 → 실선은 ≈−2,400, 점선 다발이 더 깊음), ②≈3.26 V(≈−4,300),
③≈3.225, ④≈3.195, ⑤≈3.17, 그리고 A(≈3.28), B(≈3.23), C(≈3.20), D(≈3.18).
파란 화살표는 변화 방향, **파란 "=" 기호는 불변**을 뜻한다.
- **(a) LAM_liPE**: ① 큰 위쪽 화살표(=강도 감소), ② "=" + 작은 위 화살표,
  ③④⑤ 전부 "=".
- **(b) LAM_dePE**: ⑤ 큰 위 화살표, ④·③ 위 화살표, ② "=" (깊은 peak 유지),
  ① "=" (≈3.30 에 "=" 표시).
- **(c) LAM_liNE**: ⑤④③ 위 화살표, ② 위 화살표, ① 큰 위 화살표 — **전부 감소**.
- **(d) LAM_deNE**: ⑤④③ 위 화살표, ② 위 화살표, **① 만 아래 화살표(=강도 증가)**.
- **(e) LLI**: ① 큰 위 화살표, ② "=" + 위 화살표, ④③ "=", **⑤ 에 가로(오른쪽)
  화살표** — 위치 이동.
- **(f) ORI**: 모든 peak 에 **가로(왼쪽) 화살표** — 강도 변화 없이 전압만 이동.

`[해석]` **(a) 와 (e) 의 표식이 거의 같다** — ① 감소, ② 약간 감소, ③④ 불변.
차이는 **(e) 의 ⑤ 가 오른쪽으로 이동**한다는 것 하나뿐이다. 본문 서술과 정확히
일치한다.

**Fig. 14 (직접 봄) — DV 서명 6패널** `[도표]`. x축 `Normalized capacity (%)`
0–100, y축 `Differential voltage (V/%Q)` 0–0.05. (a) 에 ①(≈88%), A(≈77%),
②(≈53%), B(≈30%), ③(≈27%), ④(≈21%), C(≈22%), D(≈17%), ⑤(≈14%) 라벨.
- (a) LAM_liPE: 오른쪽에 왼쪽 화살표 하나 + "=" 둘. 저용량쪽 peak 들은 거의 불변.
- (b) LAM_dePE: 왼쪽 끝·중앙·오른쪽에 왼쪽 화살표 다수 — peak 들이 저용량으로 이동.
- (c) LAM_liNE, (d) LAM_deNE: 둘 다 왼쪽 화살표 4개, 패턴이 서로 **매우 유사**.
- **(e) LLI: 오른쪽 peak 에 왼쪽 화살표 하나뿐이고, 나머지는 전부 "=" 3개.**
- (f) ORI: **화살표 없이 "=" 하나** — 완전 불변.

`[해석]` (a) 와 (e) 의 DV 표식이 **사실상 동일**하다 (오른쪽 이동 + 나머지 불변).
본문의 "almost impossible to distinguish … using the DV analysis" 와 일치한다.

## 9.2 ★★ 저자들이 인쇄한 구별 불가 진술 (원문 그대로)

`[인쇄]` (p.213):

> "As shown in the left column of Figs. 13 and 14, **LAM_liPE, LAM_deNE and LLI show
> similar IC and DV signatures.** They share a common theme that the graphite cannot
> be lithiated to the same level as it was initially; so, the main feature in the
> respective signatures is the loss of intensity in the first peak ① on the IC curve
> and the valley ① on the DV curve."

> "In the LAM_deNE, all ① to ⑤ peaks/valleys are fading from the beginning, thus
> **LAM_deNE can be unambiguously identified.** **It is interesting to note that it is
> almost impossible to distinguish between LAM_liPE and LLI using the DV analysis in
> this case.** It is however possible in the IC analysis, since peak ⑤ is shifting
> toward higher voltages faster for LLI than for LAM_liPE, although **it might be
> difficult to decipher between the two from the C/25 IC signature, especially for
> small capacity fade (<5%) and if the PE potential is really a constant potential
> plateau.**"

`[인쇄]` §4.2 결론 (p.213):

> "This study shows that, in the case of graphite||LFP chemistry, the derivation of
> signature for various cell degradation modes is rather feasible, but **it is
> difficult to distinguish between LAM_liPE and LLI unambiguously.** This is due to
> the fact that the LFP used in the example has a flat potential plateau and good rate
> capability. We trust that the two modes would be distinguishable in other
> chemistries, or if the LFP electrode is carefully characterized with better
> resolution in rate and temperature effects."

`[해석] ★★★` **이것이 이 논문의 유일한 축퇴 진술이며, 매우 구체적이다.**
- 구별 불가 쌍: **LAM_liPE ↔ LLI** (DV 로는 거의 불가, IC 로는 peak ⑤ 이동
  속도로만 가능, 용량손실 <5% 에서는 그것도 어려움).
- 유일 식별 가능: **LAM_deNE**.
- 원인 귀속: **PE 의 평탄 plateau**.
- 해소 전망은 **근거 없는 낙관**이다 — "We trust that the two modes **would be**
  distinguishable in other chemistries" 는 시뮬레이션도 데이터도 없이 적은 문장이다.

`[인쇄]` 방법 비교 (p.213):

> "Although capacity quantification might be easier with the DV analysis, **IC
> analysis may inhere a better sensitivity to decipher degradation modes.** It reflects
> cell degradation signature on a voltage scale, which provides a better reference to
> the state of the battery than the capacity scale that varies with aging."

`[인쇄]` 반대로 §4.2 서두의 낙관 (p.212) — **같은 절 안에서 모순적이다**:

> "since degradation results can now be simulated under various scenarios to help us
> identify the mechanisms with much less uncertainty. For instance, in the comparison
> of the four types of LAMs, **we can identify which mode might occur in the cell
> using dQ/dV or dV/dQ analysis, without any ambiguity.**"

`[해석] ★` **한 절 안에서 "without any ambiguity" 와 "difficult to distinguish
… unambiguously" 가 공존한다.** 앞 문장은 4종 LAM 끼리의 비교로 한정하면 참에
가깝고(그래도 Fig. 14 의 (c)(d) 는 매우 닮았다), 뒤 문장은 LLI 를 넣으면 깨진다는
뜻이다. **인용할 때 앞 문장만 떼면 논문을 왜곡한다.**

---

# 10. ★★★ 판정 — 우리 코드 주석의 출처가 여기인가

우리 저장소가 주장하는 것 (읽기 전용 확인, 수정하지 않음):

| 위치 | 인쇄된 것 |
|---|---|
| `degradation-degeneracy/src/fitting.py:12-23` | `U_PE(x) = f_PE_ref((x−β_PE)/α_PE)`, `α_PE = (1−LAM_PE)/r`, `LAM_PE = 1 − α_PE·r`, `LLI = 1 − r·[w_PE·α_PE + w_NE·α_NE + κ·(β_NE − β_PE)]` |
| `docs/02_CODE_AUDIT.md:84` | `LLI = ((1 - a_pe) + (b_pe - b_ne)) * 100    # Birkl 2017 부호 규약` |
| `docs/04_PROMPTS.md:329` | `LLI = (1 - a_PE) + (b_PE - b_NE)     ← 원본 부호 규약 유지 (Birkl 2017)` |
| `reference/degrade_mode_sim_original.py:414-417` | `# Birkl et al. 2017 (J. Power Sources 341, Eq.7-10) 기반: … -> LLI = (1-alpha_PE) + (beta_PE - beta_NE)  (기존 부호가 반대였음)` |

`src/fitting.py:67-78` 이 창을 `x ∈ [β, β+α]` 로 정의하므로 **β = 창의 왼쪽 끝,
α = 창의 폭**이다. 이 정의를 고정하고 대조한다.

## 10.1 항목별 대조

| 우리 코드의 요소 | 이 논문에 있는가 | 근거 |
|---|---|---|
| **scaling 파라미터** (α) | **있다** — `LR` (식 2',3,5), Fig. 4 의 치수선 `100%SOC_NE × LR` | §4 |
| **offset 파라미터** (β) | **있다** — `OFS` (식 2',8,8'), Fig. 4/6/7 의 `OFS_ini`/`OFS` 치수선 | §4, §5.4 |
| **창(window) 기하** | **있다** — NE 곡선을 폭 LR·시작점 OFS 의 창으로 PE 축에 얹는다 | Fig. 4 (직접 봄) |
| **LAM ↔ scaling 관계** | **있다, 형태 일치** — 식 (5) | 아래 10.2 |
| **LLI ↔ offset 관계** | **있다** — 식 (8') 의 `+%LLI_ch` | 아래 10.3 |
| **li/de 4분류와 기호** | **있다, 이 논문이 정의문의 출처** | §5.1 |
| **전극당 창 2개 (α_PE,β_PE,α_NE,β_NE)** | **없다** — 창은 NE 하나뿐, PE 는 축 자체로 고정 | §4 |
| **`LLI = (1−α_PE) + (β_PE − β_NE)`** | **없다** | 아래 10.4 |
| **역환산(곡선→모드) 공식** | **없다** — 이 논문은 정방향 전용 | 공백 목록 1,5 |
| **`r = Q_deg/Q_ref` 로의 정규화** | **없다** — 이 논문은 초기 PE 용량으로 정규화한다 | §4 |

## 10.2 LAM 항 — **정확히 일치한다** (비율 형태에서)

우리 코드: `α_PE = (1−LAM_PE)/r`, `α_NE = (1−LAM_NE)/r`. 두 식을 나누면 `r` 이 소거되어

    α_NE / α_PE = (1 − LAM_NE) / (1 − LAM_PE)

Dubarry 식 (5) 를 정리하면

    LR / LR_ini = (100% − %LAM_deNE − %LAM_liNE) / (100% − %LAM_dePE − %LAM_liPE)
                = (1 − LAM_NE,tot) / (1 − LAM_PE,tot)

`[해석]` **두 식은 같다.** 즉 우리 코드의 α–LAM 관계는 **Dubarry 식 (5) 의
비율을 전극별로 쪼갠 것**이다. `r` 은 우리가 "셀 자기 용량으로 정규화" 를 택했기
때문에 생긴 우리 쪽 추가이고, Dubarry 에는 없다 (그는 항상 초기 PE 축에 그린다).

## 10.3 LLI 항 — **위치와 부호는 일치, 형태는 불일치**

식 (8') 을 LLI 에 대해 풀면 (LLI_dis = 0 가정, 저자가 그렇게 한다):

    %LLI = (OFS − OFS_ini) − LR·%LAM_liNE − (LR/LR_ini)·%LAM_dePE

`OFS` = PE 축 위 NE 창의 왼쪽 끝이고, PE 창의 왼쪽 끝은 0 이다. 우리 기호로
`OFS ↔ (β_NE − β_PE)`. 따라서 Dubarry 규약에서

    LLI ∝ **+(β_NE − β_PE)**   그리고 LAM 항은 **뺀다**

대조:
- `src/fitting.py:23` 의 현행 식 `LLI = 1 − r·[w_PE·α_PE + w_NE·α_NE + κ·(β_NE − β_PE)]`
  → offset 항의 **부호가 Dubarry 와 같다** (`β_NE − β_PE`). `[해석]` 다만
  `1 − r·[...]` 라는 전체 형태(가중 재고합)는 Dubarry 에 **없다** — 이것은
  `src/inventory.py` 의 자체 유도다.
- `docs/02_CODE_AUDIT.md`·`docs/04_PROMPTS.md`·`reference/…_original.py` 의 legacy 식
  `LLI = (1−α_PE) + (β_PE − β_NE)`
  → offset 항이 **`β_PE − β_NE`**, 즉 **Dubarry 식 (8') 과 부호가 반대**다.
  → 그리고 `(1−α_PE) = LAM_PE` 를 **더한다**. Dubarry 는 LAM 항을 **빼고**,
    더구나 **`LAM_liNE` 와 `LAM_dePE` 만** 쓴다 (`LAM_PE` 전체가 아니다 —
    `LAM_liPE` 는 OFS 에 **들어가지 않는다**, Fig. 6(a) 가 그것을 그린다).

`[해석]` 즉 legacy 식은 **부호도, 관여 전극도, 부호 앞의 연산도 Dubarry 와
다르다.** 세 군데가 전부 어긋난다.

## 10.4 ★ 판정: **(c) 부분적으로 맞다** — 그러나 붙은 이름은 틀렸다

**(c) 이며, 나뉘는 지점이 분명하다.**

**여기가 출처인 것 (판정 a 에 해당하는 부분):**
1. **α·β 창 파라미터화 자체** — scaling(LR) + offset(OFS) 로 반쪽셀 곡선을
   full-cell 에 얹는 좌표계. 식 (2'),(3) 과 **Fig. 4 의 치수선**이 정본이다.
   Birkl 2017 에는 이 기하가 없다 (Birkl 은 `x_EoC`/`x_EoD` 4개를 쓰고 그중 둘을
   컷오프 등식으로 소거한다).
2. **LAM ↔ scaling 관계** — 식 (5) 가 우리 `α–LAM` 관계와 비율 형태로 **동일**.
3. **LLI 가 offset 에 들어간다는 구조** — 식 (8'), Fig. 7 의 순수 평행이동.
4. **`LAM_liPE`/`LAM_dePE`/`LAM_liNE`/`LAM_deNE` 4분류와 명명 규칙** — §3.1 이
   정의문의 출처. **Birkl 의 4종 구분은 여기서 왔다** (Birkl 이 [19] 로 인용).

**여기도 아닌 것 (판정 b 에 해당하는 부분):**
5. **`LLI = (1−α_PE) + (β_PE − β_NE)` 라는 식은 이 논문에 없다.** 그리고 §10.3
   대로 **Dubarry 식 (8') 과 부호·전극·연산이 어긋난다.** Birkl 2017 에도 없다
   (직전 흡수에서 확인). **두 논문 어디에도 없는 식이다.**
6. **전극당 창 2개(α_PE, β_PE, α_NE, β_NE)** 는 이 논문에 없다 — Dubarry 의
   자유도는 `(LR, OFS)` **2개**뿐이고 PE 는 축으로 고정된다.
7. **역문제·목적함수·경계값**은 이 논문에 없다.

**따라서 결론 문장**: 우리 코드 주석이 붙여야 할 이름은 **"Birkl 2017 부호
규약" 이 아니라 "Dubarry 2012 (LR·OFS) 창 파라미터화"** 다. 단, 그 이름으로도
legacy 식 자체는 **정당화되지 않는다** — 그 식은 Dubarry 식 (8') 의 부호와
반대이고 LAM 항의 전극 귀속이 다르다. `[해석]` 가장 정확한 서술은:
**좌표계의 계보는 Dubarry 2012 이고, legacy LLI 식은 두 원전 중 어느 것도
아닌 우리 쪽 (재)유도이며 그 유도가 문서화돼 있지 않다.** 현행 `src/fitting.py`
식은 최소한 **offset 부호가 Dubarry 와 일치**한다.

`[해석]` **자유도 개수 비교** (§10.1 표의 마지막 세 줄이 실질):

| | Dubarry 2012 | Birkl 2017 | 우리 창 모델 |
|---|---|---|---|
| 자유 파라미터 | (LR, OFS) = **2** (정방향 입력은 모드 6종) | `[LLI, LAM_PE, LAM_NE]` = **3** | α_PE,β_PE,α_NE,β_NE = **4** |
| 역문제를 푸는가 | **아니다** | 그렇다 (fmincon+MultiStart) | 그렇다 |
| PE 창 | 축으로 고정 | 컷오프 등식으로 구속 | **자유** |

`[해석]` 우리가 관측하는 degeneracy 의 일부가 **원전들에 없는 자유도**(PE 창
2개)에서 온다는 가설이 이 표로 더 선명해진다 — Dubarry 는 2, Birkl 은 3, 우리는
4다. 미실측.

---

# 11. ★ 식별 가능성 어휘 전수 확인 (본문 전체, 합자 정규화 후)

PDF 텍스트층을 `pymupdf` 로 뽑고 NFKC + `fi/fl/ff/ffi/ffl` 합자 치환을 적용한
뒤(61,578자, 13쪽) 대소문자 무시 검색한 결과:

| 검색어 | 횟수 | 비고 |
|---|---|---|
| `identifiab` | **0** | |
| `degenerat` | **0** | |
| `non-unique` / `nonunique` | **0** | |
| `ill-posed` / `ill posed` | **0** | |
| `collinear` | **0** | |
| `confidence` | **0** | |
| `deconvol` | **0** | `de-convolute` 는 하이픈형으로 1회 존재 (아래) |
| `inverse` | **0** | |
| `uniqu` | 7 | **전부 "unique" = "독창적인/특이한"** — 수학적 유일성 아님 |
| `ambigu` | 3 | **전부 축퇴 논의** (§9.2) |
| `uncertain` | 2 | 1회는 "initial capacity loss 의 불확실성", 1회는 "much less uncertainty" (§9.2 낙관 문장) |
| `correlat` | 2 | 1회는 경험적 상관법 비판, 1회는 RCV–SOC 상관 |
| `sensitivit` | 1 | "IC analysis may inhere a better sensitivity to decipher degradation modes" |
| `fitting` | 2 | **둘 다 타 연구 비판 맥락** (§1) — 자기 방법에 fitting 이 없다 |
| `fitted` / `best fit` | **0** | |

`[해석]` **`uniqu` 7회가 전부 "unique/novel technique" 의 뜻이다** — 제목·
highlights·abstract·서론·결론의 자화자찬 어휘다. **수학적 유일성 주장은 0회.**

`[해석]` **축퇴는 `ambigu` 3회에만 산다**: (i) "without any ambiguity" (4종 LAM
비교, 낙관), (ii) "LAM_deNE can be unambiguously identified", (iii) "difficult to
distinguish between LAM_liPE and LLI unambiguously". 즉 **구별 가능성을 정성적
어휘로만 다루고, 정량 진단은 하나도 없다.**

`[인쇄]` `de-convolute` 의 유일한 등장 (§5.2, p.214) — **미래 시제다**:

> "Further investigations are in progress to **de-convolute the effect of LAM on the
> FRD and ORI** using some test data from commercial cell aging experiments."

`[해석]` 즉 저자들도 **모드 간 혼동(LAM ↔ FRD/ORI)을 풀어야 할 미해결 과제로
인식**하고 있었고, 이 논문에서는 풀지 않았다.

`[해석] ★ 우리 질문 카드에 주는 답`: **[[22p-physics-or-degeneracy]] 가 묻는
"식별 가능성 진단이 있는가" 에 대해 이 논문의 답은 명확히 "없다" 다.** 그러나
Birkl 과 마찬가지로 **저자들이 구별 불가를 부정한 것은 아니다** — 오히려
LAM_liPE ↔ LLI 를 이름 붙여 인정한다. 다시 한번, 문제는 원전이 아니라
**원전의 이 문단을 인용하지 않는 후속 문헌**이다.

---

# 12. 논문이 스스로 제기한 해석 위험 3건 (§5, p.214–215)

## 12.1 LAM 이 저항 증가로 오독된다 (§5.2)

`[인쇄]`

> "Fig. 16 presents an example where the evolution of the IC signatures with 30%
> LAM_liPE are simulated. … It is clear that the IC peaks are slowly shifting toward
> lower voltages. **This would be interpreted as a polarization resistance increase,
> if a real cell were tested, whereas no ORI or FRD were included in the simulation.**
> The shift of the IC peaks is in fact related to the increase of the "actual" rate on
> the PE that goes from about 2C to 3C"

> "This observation implies that **the polarization resistance increase often reported
> in the literature upon degradation may not be entirely due to SEI layer growth or
> degradation in charge-transfer kinetics**; to the contrary, some may be imputable to
> LAM that changed the "actual" rate at the electrode that is induced by degradation."

`[해석] ★★` **모드 간 축퇴가 하나 더 있다: LAM ↔ ORI/FRD.** Fig. 13(f) 에서 ORI
의 표식은 "모든 peak 이 왼쪽으로 이동" 인데, Fig. 16 은 **ORI 없이 LAM_liPE 만으로
같은 표식이 나온다**고 말한다. 이것은 §9.2 의 LAM_liPE ↔ LLI 와 **별개의 두 번째
축퇴**이며, 열역학 축(LLI/LAM)과 동역학 축(ORI/FRD)을 가로지른다.
(**Fig. 16 은 보지 않았다** — 본문 서술에만 근거한다.)

## 12.2 SOC 추정이 열화로 무너진다 (§5.1)

`[인쇄]`

> "in Fig. 15(a), it is shown that **for a RCV = 3 V, the SOC of the cell is 7% at the
> initial state but could be in the range of 2% and 7% after aging depending on
> degradation scenarios.**"

> "the RCV of 2.9 V, which should correspond to 2.5% SOC initially, now is 5% SOC after
> aging."

> "it is essential to calibrate the ps-OCV = f(SOC) as often as possible through
> reference performance tests (RPT) at low rates upon aging [6], which is quite
> impractical."

(**Fig. 15 는 보지 않았다.**)

## 12.3 두 번째 열화 단계 = 가려져 있던 LAM 이 드러나는 것 (§5.3)

`[인쇄]`

> "Some of the LAMs may be **masked for up to 30% of capacity fade**, if they occur on
> the electrode that is not capacity limiting to the cell performance. However, such
> degradation will eventually catch up with that of the limiting electrode and shift
> the roles in the capacity limiting mechanism over aging"

> "**Since LLI shifts the NE-to-PE loading correspondence in the same direction as
> LAM_dePE** (as shown in Figs. 6 and 7), the impact on capacity fade from LAM_dePE
> might be masked until it becomes prominent."

`[해석] ★★★` **이 문장이 식 (8') 의 축퇴를 물리 언어로 다시 말한 것이다** —
"LLI 와 LAM_dePE 가 loading correspondence 를 **같은 방향으로** 민다". 두 모드가
같은 스칼라(OFS)에 같은 부호로 들어간다는 뜻이며, 저자들은 이것을 **축퇴가 아니라
"masking"(예측 현상)으로 읽는다.** 같은 대수적 사실의 두 해석이다.

---

# 13. Prognostic — 제목의 뒷 절반 (§5.1 끝, §5.3, Fig. 17)

`[인쇄]` prognostic 의 정의 (§5.1, p.214):

> "Our model could be used as a calibration tool to calculate the ps-OCV = f(SOC)
> curves evolution at any stage of degradation, which can be validated between two
> RPTs, for diagnosis. **It could also be used for prognostics by extrapolation from
> previous RPTs, if the degradation modes were identified from the test data and the
> results quantified to feed the model.**"

`[해석] ★★` **prognosis 의 실체는 "모드 궤적의 외삽" 이며, 그 전제가
"if the degradation modes were identified" 다.** 논문은 그 식별을 **하지 않는다**
(§11). 즉 **prognostic 기능 전체가 이 논문이 제공하지 않는 입력에 의존한다.**
이것이 이 논문의 가장 큰 구조적 공백이며, 우리 연구가 겨냥하는 지점과 정확히
겹친다 — 우리가 묻는 것은 바로 그 "if" 가 성립하는가다.

`[인쇄]` 외삽의 근거로 제시된 경험칙 (§5.3, p.215):

> "**Our experience suggests that LLI impacts capacity fade rather linearly in aging,
> whereas LAM may follow a power-law or exponential dependence [8].** This scenario is
> simulated in Fig. 17 where a linear 0.03%/cycle LLI is accompanied by an exponential
> LAM_dePE. **After 400 cycles, the capacity fade is still driven primarily by LLI
> despite > 25% LAM_dePE. After 500 cycles, the LAM_dePE starts to dominate** the
> capacity fade at a higher pace."

`[해석]` 궤적 함수형(선형 LLI, 지수 LAM)의 근거는 **"our experience"** 와
참고문헌 [8] (Honkura 2011) 이다. **이 논문 안에 그 함수형을 지지하는 데이터는
없다.** 외삽의 형태는 가정이다.

**Fig. 17 (직접 봄)** `[도표]`: x축 `Cycle number (#)` 0–500, y축
`Degradation or capacity loss (%)` 0–100. 범례 3개 — `LAM_dePE`(파란 파선),
`LLI`(검은 실선), `Calculated capacity loss`(동그라미 실선).
- LLI: 원점에서 직선으로 상승, 500 cycle 에서 `figure-read ≈ 15%` (0.03%/cycle ×
  500 = 15% 와 일치).
- LAM_dePE: 200 cycle 까지 거의 0, 이후 지수적으로 올라 500 cycle 에서 `≈ 64%`.
  300 cycle 에서 `≈ 8%`, 400 cycle 에서 `≈ 25%` (본문의 "> 25% at 400" 과 일치).
- 동그라미 곡선: 100% 에서 시작해 완만히 감소, **410 cycle 부근에서 ≈86% 로 무릎
  (knee)** 을 만들고 급락해 500 cycle 에서 `≈ 38%`.

`[해석] ★ 그림/범례 불일치 1건`: 범례는 `Calculated capacity **loss**` 인데
곡선은 **100 에서 시작해 감소**한다 — 실제로는 **용량 유지율(retention)** 이다.
y축 라벨 `Degradation or capacity loss (%)` 도 같은 혼동을 담는다. 같은 축에
증가하는 두 손실량(LLI·LAM)과 감소하는 유지율이 함께 그려져 있다. **본문
서술과는 모순되지 않으나 범례가 틀렸다.**

`[해석]` 이 knee 는 **어떤 새 물리도 없이** 두 모드의 합성만으로 나온다 —
"masking 이 풀리는 시점" 이다 (§12.3). 무릎(knee) 을 설명하는 초기 모델 중 하나로
읽을 수 있다.

---

# 14. 결론이 주장하는 것 (§6, p.215–216)

`[인쇄]` 4개 bullet:

> - A unique inference technique for battery diagnosis and prognosis,
> - A mechanistic model that can synthesize a variety of cell aging scenarios based on
>   degradation modes, including loss of active material, loss of lithium inventory,
>   kinetic degradation or increase of polarization resistance, formation of parasitic
>   phases, Li plating, and any combination of them,
> - A physicochemical process-based model that constitutes from electrode-specific
>   degradation modes to construct cell performance and degradation scenarios with
>   consideration of cell designs and operating conditions,
> - A versatile modeling tool without constraints on chemistry variations, cell designs,
>   battery sizes and geometries, and operating or aging conditions.

`[인쇄]` 마지막 문단 (p.216):

> "we illustrated some interesting degradation modes that were difficult to distinguish
> in the experiments but can be easily deciphered in this approach. For instance, loss
> of active materials could occur without detectable signatures in the beginning of
> aging but surface after an incubation period"

`[해석] ★ 결론이 §4.2 를 뒤집는다.** 결론은 "difficult to distinguish in the
experiments but **can be easily deciphered in this approach**" 라고 적는데,
§4.2 는 "**it is difficult to distinguish between LAM_liPE and LLI unambiguously**"
로 끝났다. **결론에는 그 유보가 사라진다.** 그리고 네 번째 bullet
("without constraints on chemistry variations")은 §4.2 가 결과를 **LFP 의 평탄
plateau 탓으로 귀속**한 것과 정면으로 어긋난다 — 화학종 의존성이 결과의 핵심인데
결론은 화학종 무제약을 주장한다. **인용 시 결론 bullet 을 근거로 쓰면 안 된다.**

`[인쇄]` 연구비: Idaho National Laboratory, Advanced Battery Research Program,
US DOE EERE (Contract No. DE-AC07-05ID14517).

---

# 15. 이 저장소와의 접점 (전부 `[해석]`)

## 15.1 가져올 수 있는 것

1. **좌표계 계보의 정정** — §10.4. 문서 주석의 출처 이름을 바꿔야 한다
   (RUN_SCOPE 밖 문서이지만 이번 세션은 **읽기만 했다**).
2. **식 (5)+(8') 의 축퇴를 우리 격자로 실측 가능하다.** §5.4 의 유도
   (`{LAM_liNE=x}` ≡ `{LAM_deNE=x, LLI=LR·x}`) 는 **닫힌 형태의 축퇴 방향**이며,
   우리 격자에 그 방향으로 truth 쌍을 심으면 fitting 이 둘을 가르는지 **직접**
   시험할 수 있다. 지금까지 우리가 본 축퇴는 수치적으로 발견된 것이고, 이것은
   **해석적으로 예측된 것**이다 — 검증력이 다르다.
3. **설계(LR) 축.** §8 은 같은 %LLI 가 HP 에서는 즉시, HE 에서는 13% 까지 용량에
   **전혀 나타나지 않음**을 보인다. 우리 격자가 단일 LR 이라면 이 비관측성 축을
   재지 못한다.
4. **LAM ↔ ORI/FRD 축퇴 (§12.1).** 우리 격자는 열역학 축(LLI/LAM)만 본다.
   Dubarry 는 LAM 이 전극 실효 rate 를 올려 **저항 증가처럼 보인다**고 적는다.
   우리가 C-rate 를 올린 프로토콜을 쓴다면 이 오염이 들어온다.

## 15.2 우리가 이 논문에 공급할 수 있는 것

1. **역방향 판정 자체.** 이 논문은 정방향만 있고 "if the degradation modes were
   identified" 를 가정한다 (§13). **그 가정이 언제 성립하는가**가 우리 산출물이다.
2. **정량 축퇴 경계.** 저자의 "small capacity fade (<5%) 에서는 어렵다" 는
   **눈대중**이다. 우리는 그 경계를 노이즈·OCP 왜곡 층과 함께 수치로 줄 수 있다.
3. **"We trust that the two modes would be distinguishable in other chemistries" 의
   시험.** 근거 없이 적힌 낙관이고, 화학종을 바꾼 합성 격자로 검증 가능하다.

## 15.3 인용 금지 문장 (이 논문을 근거로 쓸 수 없다)

- "이 모델은 열화 모드를 곡선에서 식별한다" → **정방향 전용이다. 역문제가 없다.**
- "IC/DV 로 모드를 모호함 없이 가른다" → 4종 LAM 끼리로 한정된 문장이고,
  같은 절이 LAM_liPE ↔ LLI 를 못 가른다고 적는다.
- "이 방법은 화학종에 제약이 없다" (결론 bullet 4) → §4.2 가 결과를 LFP 평탄
  plateau 탓으로 돌린다. 결론과 본문이 어긋난다.
- "Dubarry 2012 가 우리 LLI 식의 출처다" → **그 식은 이 논문에 없다** (§10.4).
  출처로 인용 가능한 것은 **(LR, OFS) 창 파라미터화와 li/de 4분류**까지다.
- "이 논문이 prognosis 를 검증했다" → 외삽 함수형은 "our experience" 이고
  이 논문 안에 지지 데이터가 없다.

---

# 16. 내가 본 그림과 안 본 그림 (정직성 기록)

크로핑 결과 **15장** (`raw/figures/dubarry2012_synthesize-degradation-modes/`,
`figures.json` 포함). Fig. 3 과 Fig. 12 는 캡션 기반 영역 검출에 실패해 크로핑
자체가 안 됐다 (본문 인라인 플롯).

**직접 Read 로 본 것 (8장)**: Fig. 1(모델 도식), **Fig. 4(파라미터화 도식 ★)**,
**Fig. 6(4종 LAM 창 변화 ★)**, **Fig. 7(LLI 창 평행이동 ★)**, Fig. 11(HP/HE
설계 의존), **Fig. 13(IC 서명 6패널 ★)**, **Fig. 14(DV 서명 6패널 ★)**,
Fig. 17(prognostic).

**보지 않은 것 (7장)**: Fig. 2(반쪽셀 rate 곡선), Fig. 5(full cell rate 곡선),
Fig. 8(ORI·FRD), Fig. 9(FPP/hydrated LFP), Fig. 10(모드 조합 100 cycle),
Fig. 15(ps-OCV 진화), Fig. 16(LAM 이 저항처럼 보이는 IC). **크로핑 실패로 아예
못 본 것: Fig. 3, Fig. 12.** 이 그림들에 관한 위 서술은 **전부 본문 텍스트에만**
근거하며 `[도표]` 표기를 쓰지 않았다.

**본문 서술과 어긋난 그림 1건**: **Fig. 17 의 범례** `Calculated capacity loss`
가 실제로는 유지율 곡선이다 (§13). 나머지 7장은 본문 서술과 일치했다 — 특히
Fig. 6/7 의 치수선과 화살표는 식 (5),(8) 을 정확히 그린다.
