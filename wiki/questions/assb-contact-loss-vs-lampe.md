---
title: ASSB 에서 OCV 적합이 LAM_PE 와 접촉 손실을 가를 수 있는가
description: "In solid-state cells (Li-In / Li metal / anode-free), does OCV fitting separate true positive-electrode active material loss from contact/percolation loss"
created: 2026-09-16
updated: 2026-09-22
type: research-question
tags: [battery, degradation, research, assb]
sources: [raw/papers/cui2026_direct-diagnosis-lfp-degradation-modes.md, raw/papers/bielefeld2019_microstructural-modeling-assb-composite-cathode.md, raw/papers/clausnitzer2023_optimizing-composite-cathode-structure-resolved.md, raw/papers/liu2024_grain-level-chemo-mechanics-composite-cathode-degradation.md, raw/papers/shi2020_mechanical-degradation-assb-cathode.md, raw/papers/doux2020_stack-pressure-room-temperature-assb-li-metal.md, raw/papers/lee2020_ag-c-anode-free-assb.md, raw/papers/spencerjolly2023_ag-graphite-interlayer-structural-changes.md, raw/papers/li2026_safety-aware-bms-active-intelligence.md, raw/papers/huo2025_assb-cathode-lampe-coupled-aging-model.md, raw/papers/vadhva2021_eis-for-assb-theory-methods.md, raw/papers/yu2024_drt-time-resolved-aging-sulfide-assb-fullcell.md, raw/papers/kouhestani2022_phm-solid-state-batteries-perspective.md, raw/papers/zheng2026_assb-grid-realistic-appraisal.md, raw/papers/oh2025_maxwell-protocol-nondestructive-assb-health.md, raw/papers/rahman2024_sbms-rul-solid-state-batteries.md, raw/papers/ramanayagam2026_stack-pressure-three-electrode-assb-impedance.md]
confidence: low
explored: false
verificationStatus: unverified
claimType: empirical
evidenceScope: user-original
status: open
feedsInto: "bms-balancing/docs/ASSB_TRANSFER_NOTE.md — 그리고 그것이 새 모델 요구서의 ASSB 판으로 갈 때"
---

# ASSB 에서 OCV 적합이 LAM_PE 와 접촉 손실을 가를 수 있는가

> **ASSB 섹션의 닻이다.** 이 주제의 논문은 `assb` 태그를 달고 여기로 링크한다.
> 액체셀 계열(현재 `raw/papers/` 20 편)과 **섞지 않는다** — 음극 축이 다르다.
>
> ⚠ **보류 항목이다** (2026-09-16 사용자 결정): 지금 프로젝트가 끝난 뒤에 착수한다.
> 지금 하는 일은 **자료를 모으고 물음을 벼려 두는 것**까지다.

## 질문

전고체전지의 음극은 **Li-In 합금 · Li 금속 · 무음극**이고, 셋 다 작동 구간에서
**OCP 가 평탄**하다. 그러면 완전지 OCV 는 사실상 양극 곡선 하나가 늘어나고 밀린
것이다. 여기서:

> 복합양극의 **접촉 손실**(활물질이 고체전해질과 닿지 않게 됨)은 **용량이 준 것처럼**
> 보인다 — 물질은 그대로인데. **OCV 적합이 이것을 진짜 `LAM_PE` 와 가를 수 있는가?**

## 왜 이 물음인가 — 액체셀에서 막힌 자리가 여기서는 열릴 수 있다

액체셀 갈래(`bms-balancing/`)가 도달한 결론은 **"LAM 분할은 점추정으로 보고할 수
없고 폭과 함께 보고해야 한다"** 였고, 더 못 간 이유가 **measured 라벨이 없다**는
것이었다 (`bms-balancing/docs/NEW_MODEL_REQUIREMENTS.md` §5 · §8-6).

ASSB 의 이 물음은 다르다 — **접촉 수·퍼콜레이션은 DEM 이 독립으로 준다.**
이 모노레포에 이미 DEM/MPM 계열이 있다(타 브랜치 소유, `dem-mpm` 태그).
그것이 **OCV 적합이 못 보는 바로 그 양**이므로, 액체셀에 없던 **독립 라벨**이 될 수
있다. 이것이 이 물음을 먼저 적어 두는 이유다.

## 지금까지 아는 것 — 실측 하나

`bms-balancing/docs/ASSB_TRANSFER_NOTE.md` §1 (2026-09-16, 합성):
현행 `Objective` 에 **평탄 상대극**을 끼우고(코드 수정 0) 축별 민감도를 쟀다.

| 흔든 축 | `Δ obj` |
|---|---:|
| `a_PE` | **+2.204e-01** |
| `b_PE` | **+4.399e-01** |
| `a_NE` | **+0.000e+00** |
| `b_NE` | **+0.000e+00** |
| `γ_Si` | **+0.000e+00** |

→ **5 → 3 파라미터 붕괴.** 액체셀 최악의 축퇴([[fitting-degeneracy]] 의 `LAM_NE ↔ γ_Si`)는
ASSB 에서 **개념 자체가 없어진다.** 대신 싸움이 **`LAM_PE ↔ 접촉 손실` 한 자리로 모인다.**

폭을 재는 기계([[near-optimal-set-width-measurement]])는 **그대로 쓴다** — 화학에
무관하게 "답이 하나로 정해지는가" 를 재기 때문이다. 파라미터가 3 개로 줄면 오히려
싼 문제가 된다.

⚠ 이것은 **우리 합성 양극 곡선에 평탄 상대극을 붙인 것**이지 ASSB 실자료가 아니다.

## 아직 모르는 것

1. **접촉 손실을 모델에 어떤 형태로 넣나** — 용량 축 스케일인가, 별도 칸인가,
   유효 활물질 분율인가. **이것이 정해져야 구분 시험이 설계된다.**
   → **형태는 정해졌다** (1호: 용량 축에 곱해지는 기하 인자 `θ_AM`).
   → **항이 하나 더 있다** (2호: 율 의존 인자 `η(i)`, [[assb-apparent-capacity-decomposition]]).
   → **남은 것은 시간축** (`θ(N)`) — `assb` **3/3 편이 안 줬다**.
   ⚠ 그리고 2호의 `C_norm` 이 `θ_AM` 을 포함하는지 아닌지 **원문에 안 적혀 있다**
   (2호 digest G1) — 3항 분해를 수치로 쓰기 전에 풀어야 할 좌표.
   → **3호(Liu 2024)가 시간축 대신 준 것은 `θ` 를 떨어뜨릴 구동력**이다: 계면
   **최대주응력**(GPa). ★ **그러나 좌표 변환이 안 된다** — 응력(Pa) → 분리 분율(무차원)
   에는 파괴 판정 규칙이 필요한데 **3호에 파괴·디본딩 모형이 없다**
   (`[인쇄]` "the current model does not explicitly account for mechanical fracture").
   → **1–3 호의 공백은 같은 한 조각이다: cohesive zone / phase-field damage.**
   → ★ **4호(Shi 2020)가 모형 대신 실측으로 시간축을 줬다** — void 부피분율이 사이클
   **0/10/50** 에 **2.87 → 3.23 → 9.50 vol%**. 모양은 **부드럽지 않고 계단**이다
   (`[인쇄]` "does **not progress gradually** … the majority … occurs at **later cycles
   and over a short period**"). ⚠ 3 점 · 각 점 **다른 셀** · 반복 0 이고, 그 "계단" 이
   **검출 한계의 산물일 수 있다** (같은 논문이 `[인쇄]` "very small microfractures …
   **undetectable by the tomography**").
   ⚠⚠ **그리고 4호의 양은 `θ` 가 아니다** — **접촉 면적분율**(10.4 %)이고, 그것을
   곱셈 인자 자리에 넣으면 **자기 압력 실험과 6 배 어긋난다**(아래 Evidence).
2. **Li-In 기준 전위가 얼마나 안정한가.** 평탄한 것은 두 상 공존 영역 안에서만이다.
   벗어나면 기준이 이동하고 그것은 전체 곡선의 **밀기** — **`LLI` 와 같은 모양**이다.
   → ★ **4호가 답이 아니라 경고를 준다**: 실험 논문이 `[인쇄]` "1.4–3.7 V vs In
   (2–4.3 V vs Li/Li⁺)" 로 **오프셋 0.6 V 를 고정 가정하고 검토하지 않는다**
   (`indium` 0 회). ⚠ **그런데 같은 논문의 EIS 에서 음극 쪽 `R_LF` 가
   `[도표]` ≈0.7 → ≈110 kΩ (≈157 배)로 자라고, 50 사이클에 전체 저항의 ≈93 % 다.**
   → **기준극이 가장 크게 변하는 계면인데 기준 전위를 불변으로 놓는다.**
   완전지 OCV 를 양극 곡선으로 읽는 우리 계획이 딛는 바로 그 가정이다.
3. **무음극의 dead Li 와 SEI Li** 는 OCV 에 똑같이 들어온다. 가르는 관측이 있나.
   → ★ **5호(Doux 2020)가 절반 답했다.** 같은 셀에서 **토모그래피(형태) + XRD(화학)**
   두 채널을 돌리면 **SEI 는 상으로 잡힌다** (Li₂S · LiCl · P₄ · Li₃P₇, Mo Kα 투과).
   ⚠ **dead Li 는 잡히지 않는다** — `[인쇄]` "lithium metal dendrites are **not
   directly detected by X-ray diffraction** due to the low amounts and low scattering
   efficiency of lithium metal", 그리고 토모그래피는 **밀도 대비**뿐이라
   Li(0.534 g cm⁻³)와 균열/공극(0)이 갈리지 않는다.
   ⚠⚠ 그 결과 같은 논문이 **같은 저밀도 대비를 Fig. 5b 에서는 "dendrite", Fig. S6
   에서는 "severe cracking"** 이라고 부른다 (5호 digest D6).
   `[해석]` **SEI Li 는 정량 가능한 길이 보이고, dead Li 는 아직 관측 수단이 없다.**
   → ★★ **6호(Lee 2020)가 이 계보 첫 무음극 셀로 채널 둘을 더했다** —
   ② **EELS Li 맵**(Li 특이 채널; `[도표]` **방전 후·100 사이클 후에도 Ag–C 층 안에
   Li 망이 남는다**, pristine 엔 없다) ③ **XRD 의 Li₉Ag₄**(Li 를 담은 상을 동정한
   첫 사례, 가역). **그래도 dead Li 는 못 가른다** — EELS 가 dead Li / LiC_x / SEI /
   합금 잔여를 구분하지 않는다. 단면 SEM 은 `[재현]` **1 µm = 용량의 3.0 %** 라
   사이클당 손실(0.011 %)보다 **≈270 배 거칠다**.
   ⚠⚠ 그리고 6호는 `[인쇄]` "the discharge capacity decays due to the generation of
   **isolated lithium**" 이라고 **기구로 지목하면서 한 번도 재지 않는다.**
   → ★★★ **대신 6호가 준 것은 "무음극에서 `LLI` 를 무엇으로 세는가" 의 답이다**:
   **전하 수지 둘뿐**(첫 사이클 비가역분 · 사이클당 CE)이고 **그 둘이 10 배 어긋난다.**
   자세히는 [[anode-free-li-inventory-accounting]].
   → ★★★ **7호(Spencer-Jolly 2023)가 처음으로 dead Li 를 숫자로 만들 재료를 준다 —
   그리고 그 뺄셈을 하지 않는다.** 같은 셀의 `[도표]` **충전 67.6 h · 방전 35.0 h**
   (둘 다 30 µA cm⁻²) → `[재현]` **2.03 ↔ 1.05 mAh cm⁻², 첫 사이클 효율 ≈52 %**.
   여기서 `[도표]` 계면상(SEI) 구간 **0.19** 를 빼면 **≈0.79 mAh cm⁻² (통과 전하의
   39 %)** 가 남는다. **방전 종료 회절에 `[인쇄]` "only graphite and Ag" 만 남으므로
   층 안에 저장된 Li 는 전부 돌아왔고**, 남는 통로는 **추가 SEI 와 고립 Li 금속**뿐이다.
   ⚠ **그 둘은 여전히 안 갈린다** — 5·6호의 한계가 그대로다.
   ⚠ 모집단: **반쪽전지 · 상온 · ≈C/68 · 1 사이클 · 층 용량의 4 배 과충전**.
   `LLI(N)` 로 옮길 수 없다. 자세히는 [[anode-free-li-inventory-accounting]] ·
   [[ag-c-interlayer-lithium-phase-path]].
4. **압력**이 상태변수다 (액체셀에 없던 것). 열화 모드가 압력 의존이면 "상태" 의
   정의부터 다시 해야 한다.
   ⚠ **`assb` 1–3 호가 `pressure` 0 회였다.** 3호(Liu 2024)는 계면 접촉 역학을 **본체로**
   다루면서도 스택 압력을 쓰지 않는다 — 대신 전해질 **탄성률·항복강도**가 그 자리를
   차지한다. `[해석]` 둘은 다른 축이다(재료 물성 vs 외부 경계조건).
   → ✅ **4호가 깼다. 그리고 압력이 상태변수를 넘어 `분리 연산자`가 된다** —
   50 사이클 후 **300 MPa 재가압**으로 용량이 `[도표]` ≈2 → `[인쇄]` **80 mAh g⁻¹**.
   `[해석]` **율이 `η(i)` 를 지우듯, 압력이 `θ_AM` 을 (부분적으로) 되돌린다.**
   자세히는 [[assb-pressure-reapplication-separation-test]].
   ⚠ **남은 것**: 압력 **스윕**이 여전히 0 편이다 (4호도 각 1 점). 그리고 4호의
   사이클 압력 **~2 MPa 는 낮은 편**이라 이 셀의 급락이 저압의 산물일 가능성을
   논문이 검토하지 않는다.
   → ✅✅ **5호(Doux 2020)가 스윕을 줬다. 그리고 압력이 "좋은 방향으로만" 가는
   변수가 아니라는 것을 보인다** — [[assb-stack-pressure-operating-window]].
   `[인쇄]` **75 MPa 도금 전 기계적 단락 · 25 MPa 48 h · 20 MPa 190 h ·
   15 MPa 272 h · 10 MPa 474 h · 5 MPa >1000 h 무단락.**
   그리고 임피던스는 `[인쇄]` **1 MPa >500 Ω → 25 MPa 32 Ω**.
   ★ **세 가지가 우리 계획에 바로 걸린다**:
   ① **상한**(4호의 300 MPa 는 이 상한의 4 배) ②  **이력**(처녀 5 MPa 110 Ω ↔
   25 MPa 를 찍고 내려온 5 MPa 50 Ω → `θ(P)` 는 경로 의존 상태다)
   ③ **`η = η(i, P)`** (과전압 자체가 압력 함수 → 율 연산자와 압력 연산자가 직교하지 않는다).
   ⚠ **여전히 없는 것**: **압력 → 용량** 곡선. `assb` **5/5 편**이 안 줬다.
   → ✅✅✅ **6호(Lee 2020)가 압력 → 용량을 준다. 그리고 축이 하나가 아님을 보인다.**
   이 셀에는 압력이 **둘**이다: **제작 490 MPa (온간 등방압 WIP)** 와 **운전 2 MPa (지그)**.
   `[도표]` 운전 압력 **2/3/4 MPa** 에서 율특성이 **94.0 / 95.1 / 95.5 %** 이고
   300 사이클 유지율 곡선 셋이 **겹친다**. `[도표]` **무압 0.1 C 곡선**(SI Fig. 12,
   충전 ≈235 · 방전 ≈217 mAh g⁻¹)이 2 MPa 곡선(≈233 / ≈214)과 **구별되지 않는다**.
   `[해석]` **490 MPa WIP 가 이미 계면을 만들어 놓아서 운전 압력이 할 일이 없다** —
   5호에서 1 → 25 MPa 가 임피던스를 >15 배 움직였던 것과 정반대이고, 모순이 아니라
   **제작 압력 이력이 다르기 때문**이다. ⚠ 그리고 **운전 상한이 훨씬 낮다**:
   `[인쇄]` "the probability of short-circuiting increased upon application of high
   pressures **exceeding 4 MPa**" — **5호의 Li 금속 75 MPa 의 1/19**.
   ⚠⚠ **그 문장에 데이터가 없다** (Fig. S11 의 압력 점은 2·3·4 MPa 셋뿐).
   → [[assb-stack-pressure-operating-window]].
5. **양극이 LFP 면** 평탄해서 `(X1, X3)` 축퇴가 그대로 온다
   (`raw/papers/cui2026_direct-diagnosis-lfp-degradation-modes.md`). NMC 면 기울기가 있다.

## 들어올 논문에서 뽑을 것 (수집 지침)

`assb` 태그를 달 논문을 읽을 때 **이 축들을 먼저 찾는다.** 없으면 "없다" 고 적는다 —
없다는 사실도 이 계보의 관측이다 (액체셀 17 편 중 유일성을 잰 논문이 0 편이었던 것처럼).

| # | 뽑을 것 | 왜 |
|---|---|---|
| Q1 | **접촉 손실을 어떻게 정량했나** — 단위·측정법·모델 형태 | 위 "모르는 것 1" |
| Q2 | **접촉 손실과 LAM 을 가르는 독립 관측**을 썼나 (단면 SEM·임피던스·압력 시험 등) | 라벨 출처 |
| Q3 | **라벨 출처 층위** — measured / fitted / 가정, 오차 막대 유무 | 요구서 §5 규칙 |
| Q4 | **유일성·식별성을 쟀나** (조건수·근최적 폭·프로파일) | 액체셀 계열은 17/17 이 안 쟀다 |
| Q5 | **Li-In 기준 전위 이동**을 다뤘나 / 무시했나 | 위 "모르는 것 2" |
| Q6 | **압력**을 통제·보고했나 | 위 "모르는 것 4" |
| Q7 | **무음극이면** dead Li 와 SEI Li 를 갈랐나, 무엇으로 | 위 "모르는 것 3" |
| Q8 | 양극 화학 (NMC / LFP / 기타) 과 **OCP 기울기** | 위 "모르는 것 5" |

### 수집 현황 — Q1~Q8 채움표

| 논문 | Q1 정량 | Q2 독립관측 | Q3 라벨층위 | Q4 유일성 | Q5 Li-In | Q6 압력 | Q7 dead Li | Q8 화학·OCP |
|---|---|---|---|---|---|---|---|---|
| Bielefeld 2019 (`assb` 1호) | **부분** (`θ`) | **없다** (실험 0) | computed-geometric | **없다** | 없다 | **없다** | 없다 | 부분 (밀도·입도만) |
| Clausnitzer 2023 (`assb` 2호) | **부분** (`Connectivity` ≡ `θ` + `ρ_S` 소결밀도 + `R_GB`) | **부분** (Minnmann 2021 EIS 부분 전도도 — **타 재료계** NMC622/Li₆PS₅Cl, 자기 실험 0) | computed-geometric + computed-electrochemical, **오차막대 0 · 점당 구조 1 개** | **없다** (순수 forward) | **없다** (`indium` 0회; Li 금속·이상 접촉) | **없다** (`pressure` 0회) | **없다** (Li 금속 무열화 가정) | **★ 있다** — LCO + NMC811, `U₀ = 4.2 V` 함수형, `U_cut = 3.4 V`, `x ∈ [0.525, 1]` / `[0.231, 1]` |
| **Liu 2024 (`assb` 3호)** | **없다** — 접촉 손실의 **양을 계산하지 않는다**. 대리로 계면 **최대주응력**(평균 378 MPa 방전 → 580 MPa 충전; SE Young 률 1→150 GPa 에서 0.05→0.55 GPa). **차원이 달라 `θ` 로 변환 불가** | **없다** (자기 실험 0 — 3/3 편 공통). ★ 단 **부정적 정보**: `[인쇄]` 실험의 활물질 손실은 rock-salt + **입계 파괴로 고립된 활물질**을 **둘 다 포함**한다 | **fitted 문턱** — 활물질 손실 라벨 = `소성전단 > 12 %`, 그 12 %는 **타 화학(Li-rich, ref 5) 실험 분포에 적합**. 오차막대 0 · 문턱 민감도 0 · **구조 실현 1 개** | **없다** (순수 forward, `identifiab*` 0회) | **없다** (`indium` 0회; **음극 자체를 모델링 안 한다**) | **없다** (`pressure` 0회 — 접촉 역학 논문인데) | **없다** (음극 없음) | **★★ 있다 — 이 계보 최초의 OCV 곡선.** NMC811 + Ta-LLZO, GITT OCV `1−θ` 0→1 에서 **≈3.0 → 4.4 V vs Li/Li⁺**, 전 구간 기울기 있음, 컷오프 3.0 V |
| **★ Shi 2020 (`assb` 4호 — 첫 실험 논문)** | **★ 있다, 무차원 분율로** — void 부피분율 **2.87 / 3.23 / 9.50 vol%** (사이클 **0/10/50**) + 접촉 손실 **면적 10.4 %** (50 사이클). ⚠ `θ` 와 **같은 양이 아니다**: **면적** vs 부피, **퍼콜레이션 판정 없음**(`percolat*` 0회), 분모에 **NMC–NMC 접촉 포함**, 면적→용량 **사상 없음** | **★★ 있다 — 3/3 편 연속 0 을 깬다.** ① FIB-SEM 토모그래피(3 셀) ② EIS(사이클 1/5/10/20/50/51) ③ ★ **300 MPa 재가압 개입** — 이 계보 최초의 "접촉 손실만 되돌리는 조작". ⚠ ①이 ②③과 **다른 셀** | **measured-but-ML-thresholded** (새 층위: 실측 영상 + Weka ML 분할, **정확도 수치 0**) + fitted(EIS 등가회로, 파라미터 표 0). **오차막대 0 · 조건당 셀 1 · 반복 0** | **없다 (4/4 편 0).** ★ 단 형태가 다르다 — `[인쇄]` EIS 시간상수가 겹쳐 "**not possible to precisely assign** a single frequency region" 이라 적고도 `R_MF` 를 **점추정으로** 서사의 기둥에 쓴다 | **★ 부분 — 계보 최초 In 금속 음극 실물.** `[인쇄]` "1.4–3.7 V vs In (2–4.3 V vs Li/Li⁺)" = **오프셋 0.6 V 고정 가정**. 안정성 논의 **0**. ⚠ 그런데 `[도표]` **음극 쪽 `R_LF` 가 ≈0.7 → ≈110 kΩ (≈157 배)** | **★★ 있다 — 3/3 편 0 을 깬다.** 제작 **100/300/100 MPa** · 사이클 **~2 MPa 스프링** · **재가압 300 MPa**. ⚠ **스윕 없음**(각 1 점), 전부 **ESI 에만** | **없다 (4/4 편 0)** — In 음극이라 dead Li 축 해당 없음. 그런데 **음극 형태학 미관찰** (`[인쇄]` "requires further study of the anode morphology") | **★★ 있다 — 계보 최초의 실측 사이클별 V–Q.** NMC532(LZO 6–8 nm) / 비정질 LPS / CNF 60:35:5, 전 구간 **기울기 있음**. `[도표]` 방전 시작 전압 사이클 5→34 에 **≈−300 mV**, 사이클 39→40 에 **≈−500 mV 계단**, ★ **충전 전압 비단조 진동** |

| **★ Doux 2020 (`assb` 5호 — 압력 스윕의 첫 편)** | **부분 — 단, 축이 음극이다.** 양극 `θ`·접촉면적·퍼콜레이션 **0**. 대신 **Li\|SE 계면 접촉의 전기적 대리량을 곡선으로**: 셀 임피던스 `[인쇄]` P=1→25 MPa 에서 **>500 → 32 Ω**, DC 과전압 `[도표]` **7.0 → 4.5 mV**, `[재현]` 계면 ASR **≈25 → ≈8 Ω cm²** | **★ 있다, 네 채널** — ① in situ **X-선 토모그래피**(≈1.18 µm) ② **같은 셀 XRD**(Mo Kα 투과, FullProf) ③ EIS ④ **로드셀 압력 실계측**(0–220 MPa, Instron 교정). ⚠ 갈라 주는 것은 **덴드라이트/SEI** 이지 LAM_PE/접촉 손실이 아니다 | **measured-electrical**(임피던스·과전압·수명) + **measured-morphological 정성**(토모 수치 0) + **measured-phase 비정량**(profile matching — 상 분율 0). **적합 라벨 0**, 오차막대 0, 조건당 셀 1. ★ **예외: Table S2 가 펠릿 4 개의 상대밀도 산포**(80.2/84.9/80.3/83.0 %) — **계보 최초의 반복** | **없다 (5/5 편 0).** `identifiab*` 0 회. ★ 형태가 또 다르다 — **등가회로 적합조차 없어** 이 논문에는 역문제 자체가 없다 (Nyquist 를 날것으로만 보여준다) | **부분 — 그리고 문제로 남는다.** Li–In 셀이 **대조군의 본체**인데 전압축을 `[인쇄]` "2.5–4.3 V vs Li/Li⁺" 로 적고 **vs In → vs Li/Li⁺ 오프셋을 명시·인용·검토하지 않는다**. `[인쇄]` Li vs Li–In 의 **역학 차이는 "아직 연구되지 않았다"** 고 스스로 적는다 | **★★★ 이 논문의 본체 — 계보 최초의 압력 스윕.** P→임피던스 **6 점**(+이력 1) · P→단락시간 **6 점** · P→과전압 **5 점**(+미보고 2 MPa). 제작압 370(펠릿)/25(Li)/120(Li–In) MPa. ★ **상한이 숫자로**: **75 MPa 도금 전 기계적 단락**, 25 MPa 48 h, 5 MPa >1000 h. ⚠ **압력→용량 곡선은 여전히 없다** | **★ 부분 — 4/4 편 0 이 깨지되 절반만.** **SEI 는 상으로 검출**(Li₂S·LiCl·P₄·Li₃P₇) 이지만 **정량 0**; **dead Li 는 검출 수단 자체가 없다** — `[인쇄]` "Li metal dendrites are **not directly detected by XRD**" 이고 토모는 **밀도 대비**뿐(Li 0.534 vs 균열 0 이 안 갈린다). `dead li`·`isolated` 0 회 | **있다(CC)** — **LNO 2 wt% 코팅 NCA**(LiNi₀.₈Co₀.₁₅Al₀.₀₅O₂) : LPSCl : carbon = 11:16:1 wt, **3.55 mg cm⁻²**, 2.5–4.3 V vs Li/Li⁺, C/10, 전 구간 기울기. **OCV·GITT 없다**(`OCV` 0 회) |

| **★ Lee 2020 (`assb` 6호 — 첫 **무음극** · 첫 **산업체**(SAIT/Samsung) · 첫 **Ah 급 파우치**)** | **없다.** `contact loss` **1 회**뿐이고 그마저 **남의 논문 인용**(refs 5,37–39). `percolat*`·`tortuos*`·`inactive` **0 회**. 유일한 대리량 = Table S2 의 **셀 두께 −5.51 %**(644.5 → 609.0 µm, WIP 490 MPa). **`θ` 를 공정으로 처리하고 재지 않는다** | **많다 — 그러나 전부 음극이다.** SEM/EDS · TEM/HAADF · **EELS(Li 맵)** · SADP · **XRD(Li₉Ag₄)** · X-선 CT(820 nm) · CV(Cu↔SUS) · EIS(온도만). ⚠ **양극 사후 분석 0** (`degradation` 본문 0 회) → `LAM_PE` ↔ 접촉 손실을 가르는 관측은 **하나도 없다** | **measured-electrochemical**(용량·CE·율·온도) + **measured-morphological 정성**(수치 0, 전부 형용사) + **measured-phase 비정량**(Li₉Ag₄, Rietveld 없음). **적합 라벨 0**(`fit*`·`equivalent circuit` 0 회). ⚠ **셀 수가 어디에도 없다**(`n =`·`N =`·`error bar`·`standard deviation`·`replicate` 전부 0 회) — ★ 유일한 산포 = **Table S2 ±2.2–2.9 µm**(정의·n 없음) | **없다 (6/6 편).** `identifiab*` 0 회. **역문제를 아예 풀지 않는다**(등가회로도 곡선 적합도 없다) — 5호와 같은 형태 | **해당 없음** (`indium` 0 회, 무음극). ★ **그러나 같은 문제가 다른 옷을 입는다**: `[도표]` Fig. 4a + SI Fig. 4c 에서 **음극 전위가 앞 9.5–16.6 % 용량 동안 ≈1 → 0 V 를 훑는다** → **"무음극은 OCP 평탄" 이 그 구간에서 거짓** | **★★★ 있다 — 그리고 축을 둘로 쪼갠다.** **제작 490 MPa 등방(WIP, 계보 최고, 대기 중)** + **운전 2/3/4 MPa 스윕** + **무압 대조**. `[재현]` WIP 치밀화 −5.51 % 가 **7 일 무압에 +0.8 µm 만 복원**(비가역). `[도표]` 무압 0.1 C 곡선이 2 MPa 와 **구별 안 된다**. ⚠ `[인쇄]` **">4 MPa 단락 확률 증가" 는 데이터 0** | **★★ 부분 — 채널은 늘고 정량은 0.** ① 방전 단면 SEM(음성; `[재현]` 한계 1 µm = 용량의 **3.0 %**, 사이클당 손실의 **270 배**) ② ★ **EELS Li 맵** — `[도표]` **방전 후·100 사이클 후에도 Li 망 잔존**(pristine 엔 없음) ③ ★★ **XRD 로 Li₉Ag₄** — **Li 저장 상을 동정한 첫 사례**(가역) ④ CE. **dead Li 를 SEI·합금·LiC_x 와 가르는 수단은 없다**. `[인쇄]` "isolated lithium" 을 기구로 지목하고 **한 번도 안 잰다** | **★★ 있다 — 계보 최초로 음극 쪽 전압축.** LZO(5 nm)-**LiNi₀.₉Co₀.₀₅Mn₀.₀₅O₂** : Li₆PS₅Cl : CNF : PTFE = 85:15:3:1.5, **6.8 mAh cm⁻²**, **215 mAh g⁻¹@0.2C**, 2.5–4.25 V, 전 구간 기울기. **OCV·GITT 0 회**. ★ **Fig. 4a** = 컷오프 전압 ↔ 면적용량 **5 점 사상**(3.5/3.55/3.6/4.0/4.25 V ↔ 0.5/0.64/1.12/5.0/6.75 mAh cm⁻²), ★★ **SI Fig. 16** = 사이클 1/200/400/600/800/1000 의 **V–Q 6 곡선** |

| **★ Spencer-Jolly 2023 (`assb` 7호 — 첫 **operando 회절** · 6호의 **외부 검증** · Bruce/Oxford)** | **없다.** `contact loss`·`percolat*`·`tortuos*` **0 회**. **양극이 아예 없다** — `[인쇄]` "these performances relate **only to the anode** and do not encompass … a composite cathode". 음극 계면 분리를 서론에서 언급만 하고 재지 않는다 | **★★ 있다, 다섯 채널 — 전부 음극.** ① **operando PXRD**(반사, Cu Kα, 시간 분해) ② **operando 싱크로트론 PXRD**(Diamond I12, 56 keV 투과, 스팟 50 µm) ③ ★ **전기화학을 뺀 ex situ 화학반응 PXRD**(LiC_x + Ag 혼합 — 계보 최초의 "화학만" 대조) ④ 평면 SEM/EDX(집전체 제거) ⑤ 단면 SEM/EDX. ⚠ `LAM_PE` ↔ 접촉 손실을 가르는 관측은 **0** | **measured-structural, 정성.** 상의 **존재/부재·순서**만. **Rietveld 0 · 상 분율 0 · 격자상수 0 · Δ2θ 수치 0**. 적합 라벨 0(등가회로·곡선적합 0). **오차막대 0 · 셀 수 어디에도 없음**(`n =`·`N =`·`error bar`·`standard deviation`·`replicate`·`uncertain*` 본문 13 쪽 + SI 6 쪽 **전수 0 회**) | **없다 (7/7 편).** `identifiab*` 0 회. **역문제를 아예 풀지 않는다** — 5·6호와 같은 형태 | **해당 없음** (`indium` 0 회, 상대극이 **Li 금속 박 50 µm**). ★ **대신 이 계보 최초로 음극 전위를 Li 기준으로 직접 읽는다**(반쪽전지). 그리고 6호의 "앞 구간이 평탄하지 않다" 를 **독립 재현**: `[도표]` SI Fig. 1 흑연 단독이 0.9 → 0 V 를 훑는 데 **용량의 ≈11.5 %**, Fig. 5 의 2 mA cm⁻² 는 **≈15 %** (6호 9.5–16.6 %) | **부분 — 6호 대비 후퇴.** 제작 **일축 400 MPa** + 운전 **2 MPa(원뿔 스프링)** 두 축 구조는 6호와 같지만 **스윕 0 · 로드셀 0 · 무압 대조 0 · 압력→용량 0**. `pressure` 5 회 · `MPa` **2 회**. 도금으로 스택이 두꺼워질 때의 압력 변화 보고 없음 | **★★★ 이 계보에서 가장 가까이 갔다 — 그런데 논문은 안 잰다.** `dead`·`isolated`·`Coulombic`·`efficiency` **전수 0 회**. 그러나 ① operando XRD 가 **Li 를 담은 상 11 종**을 시간축 위에서 동정 ② **자기 Fig. 1·3 의 시간축이 전하 수지를 닫을 재료를 준다** → `[재현]` **충전 2.03 · 방전 1.05 · SEI 0.19 mAh cm⁻² ⇒ 첫 사이클 효율 ≈52 %, 설명되지 않는 비가역분 ≈0.79 mAh cm⁻² = 통과 전하의 39 %** ③ 방전 후 **잔류 Li 의 형태학 증거**(Fig. 6C·6F 탄소 음성 영역). ⚠ **dead Li ↔ SEI 는 여전히 안 갈린다** | **없다 — 양극이 없다.** `OCV`·`open circuit`·`GITT` **0 회**. 전압축은 전부 **음극 쪽 정전류 곡선**이다 |

| **★ Li et al. 2026 (`assb` 8호 — 첫 **BMS·진단 종설** · ⚠ **Mini Review, 1차 측정 0**)** | **없다 — 정량 0.** `contact loss` **2 회** · `percolat*`·`tortuos*`·`θ` **0 회**. ★ **그러나 이 계보 최초로 "가르는 진단이 필요하다" 를 요구로 인쇄한다**: `[인쇄]` §6.1 "diagnostics capable of **distinguishing contact loss from ordinary electrochemical aging**"(Biçer 2025 — ⚠ 그것도 종설) | **없다 — 리뷰다** (자기 실험 0, 1차 데이터 0). ★ 대신 **처방**: EIS/DRT/GITT/**active bounded pulse** 네 채널의 역할 분담표(Table 3) + ASSB 용 `[인쇄]` "**pressure or force sensing**" · "**pressure-dependent impedance models**" | **★★★ 이 계보 최초로 라벨·불확실성 층위를 표의 열로 만든다 — 단 층위가 다르다.** Table 2 에 `Training/chemistry boundary`·`Validation level`·**`Uncertainty output`** 열. `[재현]` **보정된 불확실성 0 / 8** (CI 1 · "가능하나 미시연" 1 · "주산출 아님" 2 · "없음" 4), **`Cell` 검증 7 / 8**. `[인쇄]` "Field labels are limited"·"**no direct capacity labels**"·생산 추정기 3 요소(estimate + **calibrated uncertainty** + **validity flag**). ⚠⚠ **열화 모드 라벨은 0** — `LLI`·`LAM`·`degradation mode`·`incremental capacity`·`differential voltage`·`half-cell` **전수 0 회**. **이 리뷰의 SOH 는 끝까지 스칼라다** | **★★ 여전히 0 (8/8 편) — 그러나 성질이 바뀐다.** 이 계보 최초로 **식별 가능성을 실패 모드로 명명**한다 (`identifiab*` **5 회**; 1–7 호는 전부 0 회): `[인쇄]` Table 1 "ECMs … can **lose physical uniqueness**" · §2 "**Parameter identifiability** … can make a detailed model **appear more precise than the available measurements justify**" · Table 3 "**Ill-posed inversion needs regularization**" · ★ **Table 4 중기 실패 모드 "Unidentifiable pulse response"** · §3.1 "what **minimum excitation can resolve** the safety-relevant process". ⚠ **측정 0** — 조건수·프로파일 가능도·근최적 폭·Fisher/CRB 전부 없다. ⚠⚠ `poorly identifiable` 문장이 매단 인용이 **Si–C 음극 소재 종설**이다(D2) | **해당 없음** — `indium`·`Li–In` **0 회** | **★ 부분 — 재인용 수치 1 점 + 처방 3 개.** `[인쇄]` "stack pressure becomes a **coupled state/control variable**" · "Xu et al. (2024) note industrial requirements **below approximately 1 MPa**" · Table 4 장기 "**include pressure for solid state**" / 실패 모드 "**pressure/contact failure**". `[재현]` `MPa` **전체 1 회**, 값이 **1**. ★ **우리가 읽어 온 실험실 압력 창(2–490 MPa) 전체가 이 요구치 위에 있다.** ⚠ **재인용** — Xu 2024 를 받아야 한다 | **없다.** `plating` 9 회는 전부 **액체셀 저온 급속충전의 제약(gate)** 이고 dead Li ↔ SEI Li 분해는 0. `anode-free`·`dead li`·`isolated li` **0 회** | **없다** (ASSB 양극 화학 0, OCV 곡선 0). ★ **인접 관측 하나**: `[인쇄]` Li–S "voltage behavior contains **regions in which conventional OCV and Coulomb-counting assumptions are less informative**" · Na-ion "**OCV–SOC relations … require recalibration**" → **평탄/비정보 OCV 가 상태 추정을 깨는 문제가 다른 화학에서 반복된다** |

| **★★ Huo et al. 2025 (`assb` 9호 — 첫 **실험 + 파라미터 식별 동시** · 첫 **결합 전기화학-노화 모델** · 상하이교통대)** | **부분 — 그리고 자기 모순이다.** `[인쇄]` `A^p_eff = 0.4938` (무차원, 양극, BV 분모에 정의) = 이 계보 최초의 **모델 파라미터로서의 양극 접촉 면적비**. ⚠ (a) **적합값**, (b) **노화 중 고정** → `θ(N)` 0, (c) `[재현]` 자기 SEM 의 입자 반경(≈1.05 µm)을 쓰면 **0.055 로 9 배 움직인다**. `contact loss` 3 회는 전부 **남의 논문 인용**(refs 17,18,21) | **부분.** SEM(표면, 정성, 노화 1 + 신품 1) · EIS(2-전극, 등가회로) · **압력 센서 연속 시계열(★ 계보 최초)**. **XRD·XPS·TEM·ICP·적정·3-전극·반쪽전지(노화품) 전부 0.** `LAM_PE` 를 **적합 밖에서** 확인한 관측 **0 건** | ★★ **새 층위: `fitted-single-parameter`.** 노화 라벨 = **1-파라미터 PSO 적합**(`ε_p`)이고 정답축이 **자기 자신의 방전곡선**이다. 오차막대 0 · 셀 **2** · 반복 0 · `n =` 0 회. ★ **Table 3 에 provenance 열이 없고 6 개 값이 비공개**(`[인쇄]` "not disclosed") | **0 (9/9 편).** `uncertaint*`·`identifiab*`·`sensitiv*`·`confidence`·`Fisher`·`condition number`·`bootstrap`·`initial guess`·`multi-start`·`error bar`·`regulariz*`·`objective function` **전수 0 회**. ★★★ **성질이 또 바뀐다** — 8호가 "이름을 실패 모드 목록에 올렸다" 였다면 **9호는 자기 표 안에 축퇴의 지문 셋을 인쇄해 놓고 다르게 부른다**: ① `R_SEI` 분해가 동일 공정 두 셀에서 **+37 % / −80 %** 인데 `[인쇄]` "장비 정확도·**적합 오차**·열평형" 탓으로 지나간다 ② `A_eff·ε_p/R_s` **곱 축퇴** ③ `k_LAM` 셀 간 **2.15 배**를 `[인쇄]` "slightly different" | **해당 없음 → 그러나 새 형태로 열린다.** `indium`·`Li-In` 0 회. ★ **계보 최초의 합금(Li-Si) 음극**이고 모델은 `U^n_ocp(θn)` 를 **비평탄 보간 함수**로 둔다. `[재현]` 모델 N/P ≈ **3.14** → 사이클당 음극 화학량론 스윙 **31.8 %**. → **이 카드의 "전고체 음극은 평탄 → 5→3 붕괴" 가 이 셀에는 성립하지 않는다.** ⚠ N/P 는 SI 가 제출 거부한 값이고 **우리가 Table 3 에서 계산했다** | ★★ **있다 — 계보 최초의 `in operando` 연속 힘 시계열.** `[도표]` Fig. 6 이 12 사이클의 힘을 `Kg` 로 기록(고점 296.6 · 저점 294.0 · 스윙 2.6). `[재현]` 면적 7.854e−5 m² 환산 → **평균 ≈36.9 MPa · 주기 변조 ≈0.32 MPa**. ⚠ **`MPa` 0 회 · 제작 압력값 0 · 교정 0 · 스윕 0 · 노화 전 구간 추세 0**. ★★ **압력이 모델에 들어가지 않는다** — Eq. (2) 는 사이클 수만의 함수다 | **해당 없음** (Li-Si 합금 음극). `dead li`·`isolated` 0 회. ⚠ 그리고 **CE 를 SI 에서 명시적으로 제출 거부**한다 → `LLI` 의 전하 수지 채널이 닫힌다 | **있다(CC).** **단결정 NCM811 + H₃BO₃ 코팅**(★ 계보 최초의 붕산 코팅) : Li₆PS₅Cl : VGCF = **56:40:4 wt%**, `[재현]` **10.7 mg cm⁻²**, `[도표]` **2.0–4.3 V**, 전 구간 기울기 있음. ★ `[도표]` Fig. A.1(a) = **NCM811 반쪽전지 dV/dQ vs SOC** (계보 최초의 양극 반쪽셀 미분곡선) ⚠ **측정조건 전무**. **OCV·GITT 0 회** — 모델의 `U_ocp` 두 곡선은 출처가 없다 |

| **★★★ Vadhva, Hu, Johnson (3인 공동 1저자), Stocker, Braglia, Brett, Rettie 2021 (`assb` 10호 — 첫 **방법론 리뷰** · UCL + **HORIBA MIRA**(기업) · ⚠ **1차 측정 0**)** | **없다 (10/10 편).** `contact loss`·`percolat*`·`θ` **0 회**. 유일한 접점 = `[인쇄]` Fig. 9 본문 "**loss of interfacial contact in the composite cathode due to volumetric expansion**" — ★★ 그런데 그 문장이 **분해층 형성과 `and` 로 한 저항(`R_MF`)에 묶여 있다**. 가장 가까운 정량 채널은 **TLM + 전자차단 대칭셀의 유효 이온 굴곡도**(ref. 57 Kaiser) — `θ_AM` 과 같은 양이 아니다 | **★★ 있다 — 그러나 "가르는 관측" 이 아니라 "가르는 절차" 다.** ① **상보 대칭셀 쌍**(차단/가역) ② **저온으로 시상수 벌리기**(ref. 82 Bron — `R_gb` 를 −130 °C 에서 동정해 **실온 적합의 구속으로 되가져온다**) ③ **가압으로 큰 시상수 제거**(ref. 28, `[도표]` 400 MPa 에서 `R_int` 가 사라지자 `GB` 가 드러난다) ④ **DRT 로 개수를 먼저 정하기**(ref. 62) ⑤ **4 단자**(ref. 21) ⑥ **K–K / Lin-KK 사전 검증**(ref. 41–43). ⚠ **전부 재인용 · ASB 복합양극에 `LAM_PE` ↔ 접촉 손실로 적용된 사례 0** | **해당 없음 — 리뷰다** (1차 측정 0, 열화 라벨 0: `LLI`·`LAM`·`degradation mode`·`half-cell` 전수 0 회). ★ **새 층위 하나**: `[인쇄]` **기관 간 라운드로빈 산포** — `>1 mS cm⁻¹` 에서 상대 중앙값 오차 **22 %**, `<1` 에서 **~10 %** (⚠ 재인용, ⚠⚠ 인용 번호가 틀렸다 — D5). **"같은 양을 여러 기관이 재면 얼마나 벌어지는가" 의 첫 숫자** + `[인쇄]` **삼중 측정 권고** | **★★★ 0 이 깨진다 — 단 "쟀다" 가 아니라 "일반 현상임을 인쇄했다".** `[인쇄]` "**As no solution to an EIS spectrum is unique**" · "**The non-uniqueness of an ECM solution**" · "**the inclusion of more elements will tend to improve the fit**" · "how many time constants … **highly subjective**" · "Physical features **may not be visible**" · **AIC 로 회로 순위 매기기**(ref. 51,52; `[인쇄]` "only recently applied to **simulated** data") · **DRT 는 `ill-posed`, `regularization` 필요**. ★★ 그리고 **"분해 가능한 RC 개수 = 실험 조건의 함수" 를 다섯 사례로 보인다**(황화물 5 중 3 만 입계 분해 · LGPS 실온 원호 0 개 · 400 MPa 에서 GB 등장 · 폴리머 60 °C 에서 상경계 소멸 · **노화가 RQ 를 3→4 로**). ⚠ **측정 0** — `identifiab*`·`uncertaint*`·`confidence`·`condition number`·`error bar` **전수 0 회** | **★★ 부분 — 새 경고 둘.** `indium` 2 · `Li-In` 2 회. ① Li 금속이 비이상적이라 **Li-In 을 기준극 대안**으로 제시 ② ★★ `[인쇄]` **방전 중 In 음극 계면 저항이 리튬화도(In-rich 화)로 크게 증가** ⇒ **`R_anode(N)` 에서 노화분과 SoC 분이 안 갈린다** (4호 `R_LF` ≈157 배 해석에 직접 걸린다) ③ ★★★ `[인쇄]` **In–Li 음극 셀은 LMA 셀과 전극↔주파수 귀속이 반대다** ⇒ **"저주파=양극" 같은 보편 규칙이 없다**. ⚠ 전위 오프셋 안정성은 여전히 0 | **부분 — 값 3 개.** `[인쇄]` **~120 MPa**(σ 포화, 단 그것이 인가 최대압) · `[인쇄]` **~400 MPa**(Li₆PS₅Cl σ 는 거기까지 계속 증가, ref. 84 = **Doux JMCA 2020**, 우리 5호의 자매) · `[도표]` **400 MPa**(Fig. 11a, Li\|LLZO\|Li). ★★ **개념 기여가 값보다 크다**: ① `[인쇄]` "**<1 Ω cm², remained after the pressure was removed**" = **5호의 이력을 산화물에서 독립 재현** ② **압력이 분해능 연산자다** ③ `[인쇄]` 제언 2 가 **다변수(온도·압력·SoC) 시험**을 ECM 구축의 표준 처방으로 올린다. ⚠ **압력→용량 곡선 0 (10/10 편)** | **없다.** `dead li`·`isolated` 0 회. ★ 인접 둘: ① `[인쇄]` **soft short**(LLZO 내부 Li 석출)를 **`R_leak` ECM 원소**로 잡고 `R_b`·`R_gb` 안정성으로 부재 확인 ② `[인쇄]` **NLEIS 가 상용 LiB 에서 Li 도금 검출**(ref. 184). 둘 다 **석출**이지 **고립**이 아니다 | **없다.** `OCV` **1 회**(⚠ 그것도 `[인쇄]` "**OCV variation due to small capacity changes can affect the low-frequency range**" — 즉 **OCV 드리프트가 EIS 저주파를 오염시킨다**는 경고다). `GITT`·`half-cell` 0 회, **V–Q 곡선 0 장**. ★ 대신 `[도표]` Fig. 9b/9c = **SoC 축 위 EIS 10+10 점**(충전 3.305–3.599 V / 방전 3.442–2.000 V, LCO) — **전압축은 있고 용량축이 없다** |

| **★★★ Yu, Choi, Dunham, …, Farahati, Kim 2024 (`assb` 11호 — 첫 **graphite 음극 완전지** · 첫 **DRT** · **Schaeffler**(산업체) + Ohio State · *J. Power Sources* 597, 234116)** | **부분 — 단위가 Ω 다.** `contact loss`·`percolat*`·`tortuos*`·`θ` **0 회**. 대리량 = **P3 DRT 봉우리 높이**(`Ω` 또는 `Ω mg⁻¹`). ★ **계보 최초로 (i) 주파수로 국소화되고 (ii) 시계열이 있고(최장 6 점) (iii) 조작(재가압)으로 되돌려지는** 접촉 손실 대리량. ⚠ 셋이 막는다 — ① 무차원 분율이 아니다(용량 사상 0) ② ★★ **전극을 가르지 않는다** (`[도표]` Fig. 8 이 P3 에 **Cathode + Anode 둘 다** 찍는다) ③ `[인쇄]` Table 1 이 P3 를 "active material/SE **and/or** electrode/current-collector" 로 둔다 — **복합양극 내부 접촉과 집전체 접촉을 안 가른다** | **★★ 있다 — 네 조작, 그러나 전부 임피던스 안이다.** ① **완전지 ↔ NMC/In–Li ↔ graphite/In–Li 반쪽전지 분해**(계보 최초) ② **SE 입도 스윕**(nano ≤1 µm vs micro ≤20 µm) ③ **코팅 유무**(LiNbO₃ vs bare) ④ **재가압**(150 / >500 MPa). ⚠⚠ **형태학·화학 관측 0** — SEM·TEM·FIB 토모·XRD·XPS·ToF-SIMS **전수 0**. **접촉 손실을 임피던스 밖에서 확인한 관측 0 건** (4호가 FIB-SEM 으로 void 를 실측한 것과 정반대) | ★★ **새 층위: `inverted-nonunique`.** 라벨이 **ill-posed 역변환의 봉우리 높이**인데 **정규화 설정이 보고되지 않았다**(`regulariz*`·`λ`·`L-curve`·`GCV`·RBF shape **전수 0 회**). 그 위에 `[인쇄]` Fig. 2 캡션 — DRT 를 **"simulated Nyquist curves" 위에서** 계산했다 ⇒ **ECM 을 입력으로 받은 DRT**(순환). 오차막대 0 · 셀 수 0(`n =` 0 회) · 반복 0. ★ `[인쇄]` **"The authors do not have permission to share data."** ⚠⚠ **파라미터 표가 아예 없다** — 9호는 6 개를 "not disclosed" 로 **찍었는데** 38호는 구멍을 셀 기준조차 없다 (**어느 셀이 Cl 이고 어느 셀이 Br 인지도 끝까지 안 밝힌다**) | **0 (11/11 편).** `identifiab*`·`uniqu*`·`ill-posed`·`regulariz*`·`uncertaint*`·`confidence`·`error bar`·`Kramers`·`Kronig`·`condition number`·`Fisher`·`Bayes*`·`posterior`·`overfit*`·`degenerac*`·`λ`·`L-curve`·`GCV`·`cross-valid*` — **본문 + SI 전수 0 회**. ★★★ **성질이 다섯 번째로 바뀐다 — "잴 재료를 SI 에 인쇄해 놓고 뺄셈을 안 했다"**: `[도표]` **Fig. S3 가 같은 셀에서 배선만 바꿔 DRT 봉우리를 −15 % ~ +69 % 움직인다**(≈3 kHz −15 % · ≈0.03 Hz **+69 %** · 분해된 어깨 **1 개 유무 차이**), 그런데 **본문의 재가압 효과는 −10 ~ −25 %** 로 **그 폭 안**이다. 논문은 둘을 나란히 놓지 않는다. ★★ 두 번째 재료: `[재현]` **P3 의 보고 위치가 논문 안에서 500 Hz–10 kHz = 1.3 자릿수**인데 **P2–P3 간격은 0.8 자릿수**(`log₁₀(6000/900)=0.82`) ⇒ **이름표의 불확정성이 이름표 간격보다 크다** = P2(화학) ↔ P3(기계) 분리 붕괴 | **부분 — 값은 들어왔고 검토는 0.** `indium` **1 회** · `In–Li` 7 회. `[인쇄]` 반쪽전지 창 **−0.595 – 0.9 V**(음극) · **2.1–3.7 V**(양극) · 완전지 **2.7–4.2 V** ⇒ `[재현]` **오프셋 ≈0.60–0.62 V vs Li/Li⁺ 가 함의된다** (계보 최초로 소수 셋째 자리까지). ⚠ **명시·인용·안정성 논의 전부 0**. ⚠⚠ 10호의 경고(방전 중 In 계면 저항이 리튬화도로 변한다)를 **검토하지 않는다** — 모든 EIS 가 `[인쇄]` **완전지 기준 50 % SOC** 이고 **반쪽전지의 In–Li 리튬화도는 통제되지 않았다** | **★★★ 이 계보에서 가장 넓다 — 그리고 `압력 → 용량` 을 처음으로 준다.** 제작 `[인쇄]` **>500 MPa** · 운전 `[인쇄]` **20 MPa** · 재가압 **150 / >500 MPa**. `MPa` **48 회**. ★ **압력→용량 반쪽 3 점**(`[인쇄]` 165.0 / 166.9 / **173.1** mAh g⁻¹) + **완전지 2 점**(169.9 / 171.7) — **10/10 편이 못 준 칸이 채워진다**. ★★ 그리고 **압력 → 봉우리별 Δ**(`[도표]` Fig. 4d · 7d). ⚠ **효과가 4호의 1/12** (`[재현]` +4.91 % vs 4호 +60.5 %p) 인데 `[인쇄]` "agree with previous report by **Ceder et al. [21]**"(= 우리 4호) 라고만 쓰고 **크기를 비교하지 않는다**. ⚠⚠ **계측 수단 0** — `[도표]` Fig. S1 은 **볼트·너트**(정변위)인데 `[인쇄]` "remained **constant at 20 MPa**". ⚠⚠⚠ ★★ **선택성이 없다** — 재가압이 `[도표]` P1 **−11 %** · P2 **−10 %** · P3 **−16 %** · P4(전하이동) **−25 %** · 무표기 0.03 Hz **−27 %** 를 **전부** 줄인다 | **해당 없음** (graphite 음극). `dead li`·`isolated`·`plating` **0 회**. ★ 인접 하나 — `[인쇄]` graphite 반쪽 CE ">99.99 %" 인데 `[도표]` Fig. 6(a) 의 CE 축은 **5 %p 눈금**이라 0.01 % 를 분해 못 하고 **사이클 ≈65 에 ≈98.5 % 로 떨어지는 점**이 있다 (`[재현]` 용량 역산 평균은 ≈99.98 %/cycle 로 정합) | **★★★ 계보 최초의 graphite 음극 ASSB 완전지.** LiNbO₃-코팅 **NMC622** + **graphite** + Li₆PS₅X, **2.7–4.2 V**, C/3, `[인쇄]` **192.4 → 179.8(200 cy) → 169.9(500 cy) mAh g⁻¹**. `OCV`·`open circuit`·`GITT` **0 회**, **V–Q 곡선 0 장**(10호와 같다). ★★★★ **그런데 이 칸이 이 카드의 전제를 깬다** — graphite 는 **스테이지 평탄역이 여럿인 구조 있는 OCP** 다 ⇒ **"전고체 음극은 평탄 → 5→3 붕괴" 가 이 셀에 성립하지 않는다** (9호 Li-Si 에 이은 **두 번째 반례**이고 이쪽은 **상용 흑연**이라 더 직접적) |

| **Sadegh Kouhestani, Yi, Qi, Liu, Wang, Gao, Yu, Liu 2022 (`assb` 12호 — 첫 **PHM 종설** · Kansas + USTB + North Minzu · *Energies* 15, 6599 · ⚠ **Review, 1차 측정 0, 그림 7 장 전부 타 논문 재수록(LIB 6 + 2009 모식도 1)**)** | **없다 (12/12 편).** `contact loss`·`θ`·`percolat*` **0 회**. `contact area` 3 회 = 전부 §3.1.1 재인용 — `[인쇄]` "Tian et al. [60] and Shao et al. [60] introduced **a parameter to describe the contact area, which adjusts the current density in the 1-D Newman model** … the capacity drop was correlated with the loss of contact area", **값 0**. ★ `[해석]` 그 형태는 9호 `A^p_eff`(BV 분모)의 **조상 후보**(Tian & Qi 2017 → Shao 2022) — 원전 미확인 | **없다 — 리뷰다.** 인용 중 실험 영상이 모델에 들어간 것은 Fathiannasab 2021 토모그래피 1 편(재인용). ★★★ 그리고 **분리 물음을 정의에서 지운다**: `[인쇄]` §2.2 "**The loss of active materials mainly stems from the electrical contact loss** that is caused by graphite spalling, adhesive decomposition, collector corrosion, and electrode particle cracking" ⇒ 이 리뷰의 어휘에서 **`LAM ⊃ 접촉 손실`** 이고, 열거된 기구는 **전부 액체셀 것**. `[도표]` Fig. 6 의 "Contact Loss" 두 자리도 **집전체**(Cu 균열·Al 부식) | **해당 없음 + 날짜 하나.** SOH = `[인쇄]` 식 (6) 스칼라 `Q_max/Q_nominal`; 열화 모드 라벨 **0**(`LLI` 2 · `LAM` 1 회는 정의 문장뿐, 정량법 0 — 모드 정량 원전 두 편 refs 57·58 은 "**CL**" 이라는 낱말의 각주로만 쓰인다); Table 1 에 검증·불확실성·화학 열 **없음**(열이 Categories·Technique 둘); `[인쇄]` "Data Availability Statement: **Not applicable**". ★ `[인쇄]` "**very few instances where a battery can be completely exhausted or fully charged at the pack level**"(재인용) + `[인쇄]` "**most PHM techniques are based on simulation results and not experimental**"(1차) ⇒ 8호(2026)의 "no direct capacity labels" 와 같은 명제가 **2022 년에** 인쇄돼 있다 | **0 (12/12 편). 성질은 8호 이전 — 계보의 출발점을 날짜로 고정한다.** `identifiab*` **0** · `uniqu*` 1(무관: "no unique technique") · `ill-posed`·`regulariz*`·`confidence`·`error bar`·`standard deviation` **0** · `uncertaint*` 3(일반론). 가장 가까운 문장 셋: ① `[인쇄]` "difficult parameter identification"(×2, 실무 곤란) ② `[인쇄]` "large number of parameters … **inevitable errors in each parameter**" ③ 재인용 `[인쇄]` "**from a single impedance arc to a double impedance arc**" (노화·온도로, [84] LIB ECM) — 그리고 ②의 **반대 명제** `[인쇄]` "the more parameters … **the higher the accuracy**"(§3.1.3)가 같은 논문에 있다. ⇒ 8호가 이름을 붙인 것(`identifiab*` 5 회)이 **2022 년 PHM 종설에는 이름조차 없었다** | **없다.** `indium`·`In-Li`·`Li-In` 0 회 | **부분 — 재인용 1 값.** `[인쇄]` "optimal charging performance … under medium compressive pressures (**0.4–1 MPa**)" — ⚠ 출처가 **중복 인용번호 [60]**(D4) 탓에 Tian & Qi 2017 / Shao 2022 중 **확정 불가**. `[인쇄]` "anisotropic displacement of AM particles can also be prevented by applying **external compressive pressure**"(Fathiannasab). `stack` 0 · `MPa` 1 회. ★ 8호의 재인용 "<≈1 MPa"(Xu 2024, 산업 요구)와 **다른 원전에서 같은 자릿수** — 실험실 창(2–490 MPa)은 둘 다의 위 | **없다.** LLI 원인 = `[인쇄]` "SEI layer, lithium dendrite, and battery self-discharge"(LIB). `anode-free`·`dead li`·`isolated` 0 회 | **없다.** LCO(식 1; `[인쇄]` "LiCoO₂ **or LTO**" — LTO 는 음극, D1) · TiS₂ · LiPON 등 **이름만**. `OCV` 2 회(PNGV 설명 · Fig. 4 회로 기호) · `IC curve` 1 회 · `GITT` 1 회(Fabre 파라미터화) · **V–Q 곡선 0 장 · OCP 곡선 0 장**. 유일한 미분곡선 = `[도표]` 재수록 Fig. 5 의 dV/dQ 삽도. ⚠ `[도표]` 같은 Fig. 5 가 **`SOH = {FOI₁ … FOIₙ}` 벡터**를 인쇄하는데 본문 식 (6) 은 **스칼라** — 논문은 언급 없음(D20) |

| **Zheng, Xie, Zhang, Yang, Zhou, Zhu 2026 (`assb` 13호 — 첫 **그리드 용도 appraisal** · Nanjing Tech + **Huadian 전력연구원 + Shuangdeng(전지 제조사)** · *Energy* 345, 140229 · ⚠ **Perspective, 1차 측정 0, `[인쇄]` "No data was used", 그림 5 장 전부 모식도/레이더**)** | **없다 (정량 0).** `contact loss` **1 회**(M³ 시뮬 대상 열거) · `interfacial contact` 6 · `θ`·`percolat*`·`tortuos*` 0 · 단위·모델 형태 0. ★ 대신 **대리량을 지목한다**: `[인쇄]` "decay of **interfacial contact pressure** — a primary driver of impedance growth" → 압력 센서 시계열 = 접촉 손실의 관측 (9호가 힘을 **재고도 모델에 안 넣은** 자리를 처방으로 채운다). 인과 방향 `압력 감쇠 → 임피던스 ↑` 명시 | **없다 — perspective.** 처방 셋: ① 압전/박막 **압력 센서**(셀 스택 내장) ② `[인쇄]` "**EIS** could be used as a **proxy for contact integrity**"(주파수·특징 0, `DRT` 0) ③ **음향/초음파**(void·crack; 인용 [41] 은 음향 논문이 아님 D9). `LAM_PE` ↔ 접촉 손실을 가르는 관측으로 제시된 것 **0** | **해당 없음 + 정의 하나.** Table 1 ASSB 열 = 투영(재인용 2 + **무인용 5**, 10000–15000 cycles 무인용 G2), LCOS 식 (1) 입력(`d`·`P_charge`·`C_deg`) **미공개**(G1) → `$0.08–0.12/kWh` 재현 불가. ★ **라벨 정의는 인쇄됐다**: `[인쇄]` SOH 는 "**true active material loss**" ↔ "**reduction in usable capacity caused by rising impedance or increasing overpotentials**" 를 갈라야 한다 — **2 항 이분법**이고 **같은 절이 지배 실패 모드 1 번으로 꼽은 접촉 손실의 소속을 말하지 않는다** (`θ_AM` 이 문장에서 사라짐). 12호 `LAM ⊃ 접촉 손실` ↔ 13호 `LAM ∣ kinetic + 접촉 손실 미배정` — **두 종설의 분류가 다르고 둘 다 우리 3 항과 다르다** | **0 (13/13 편).** `identifiab*`·`ill-posed`·`regulariz*`·`uncertaint*`·`confidence`·`error bar` 전수 0, `uniqu*` 3 무관. ★ 성질: **역추정을 워크플로로 처방한다** — `[인쇄]` "These models **inversely estimate** the current state of interfacial contact **and** material properties" — 유일성 경고 **0**. 9호의 `A_eff·ε_p/R_s` 곱 축퇴가 정확히 "접촉 상태 ↔ 재료 물성" 사이에 있는데 이 논문은 그것을 모른다. ⇒ 8호(2026, `identifiab*` 5)와 **같은 해**에 이름 없이 역문제를 처방 — "2026 년 문헌은 식별 가능성을 안다" 는 8호 한 편의 일 | **해당 없음.** `indium`·`In-Li` 0. Li 금속 음극 자체를 `[인쇄]` "may be misguided" 로 배제 | **★★ 있다 — 이 편의 본체(값은 적다).** `pressure` **24** · `stack pressure` 7 · `pressure-less` 5 · `MPa` 본문 **2**(둘 다 `<5`). ① 1 차 주장 `[인쇄]` **`<5 MPa`** ×2(Si 음극 / 저압 아키텍처 문턱; 근거 [35]·[45], "5" 의 출처 미명시 G3) ② `[도표]` **Fig. 2 클래스별 창 — 본문에 없는 다섯 값**: Oxides **≥30** · Sulfides **5–20** · Halides **2–10** · Polymers **0/compliant** · Composites **1–10 MPa** (⚠ 권장 두 클래스 상단 10 = 문턱의 2 배, D4) ③ ★★ **상한의 두 번째 형태**: `[인쇄]` 고정 고압 → "creep and stress relaxation … **fatigue-driven micro-crack initiation** … gradually degrading interfacial contact" — 5호의 단락 상한(시간 ~h)과 **다른 축**(피로, ~년) ④ ★★ **압력 = 제어변수 + 정책**: `[인쇄]` "apply higher pressure during high-rate cycling … reduce pressure during extended rest periods or as the cell ages"(8호 "coupled state/control variable" + 정책) ⑤ 요구치 계보 세 번째: 8호 `<≈1`(Xu 2024) · 12호 `0.4–1`(Tian/Shao) · **13호 `<5`** — **원전 셋 다 다르고 자릿수 같음**; 실험실 창 2–490 MPa 은 셋 다의 위. ⚠ **압력→용량 · 스윕 · 이력 · 계측 전부 0** | **해당 없음.** Si 계 음극 권장. `dead li`·`isolated` 0 · `plating` 2(그리드 주파수조정 "resistance to lithium plating" · Table 2) | **★ 부분 — 처방과 경고, 곡선 0 장.** ① 양극 권장 **LFP / LFMP**(저전압 → 계면 열화 최소) ② `[인쇄]` "**flat voltage profiles** … (e.g., LFP cathodes) exhibit minimal voltage change over large SOC ranges" ③ ★ **운전 창 절단**: `[인쇄]` "**20–80 % SOC** … **impossible to obtain a full OCV curve** for calibration" ④ `[인쇄]` "distorted by **voltage hysteresis arising from mechanical stresses**"(인용·크기·전극 0, G6) ⑤ 음극 권장 **Si 계**(비평탄·이력 OCP — 논의 0, G10). `OCV` 1 회 · `GITT`·`dV/dQ`·`half-cell` 0 · **V–Q·OCP 0 장**. ★ 닻 "모르는 것 5"(LFP 평탄 → `(X1, X3)` 축퇴)가 그리드에서 **설계 권장 + 운전 창 절단 + 응력 이력** 세 겹으로 강화되고, "전고체 음극 = 평탄" 전제는 **세 번째로**(9호 Li-Si · 11호 graphite 에 이어 **설계 처방으로서**) 깨진다 |

| **★★ Oh, Kim, Kim, An, Kwon, Choi 2025 (`assb` 14호 — 첫 **열역학 도함수 진단** · 서울대 + **HMG-SNU JBRC(현대차)** · *Angew. Chem. Int. Ed.* 64, e202514910, **Hot Paper** · 실험 논문 + **SI .docx(진짜 SI, 표 0)** · ⚠ 자기 인용 21/74)** | **★ 있다 — 두 층위.** ① XRM 공극률 `[인쇄]` **4.5 → 9.8 vol%**(10 MPa, 50 cy) · **4.4 → 5.3**(20 MPa) — 4호 Shi 의 void vol%(2.87 → 9.50 @50 cy)와 **같은 종류·같은 자릿수** ② ★ **계보 최초의 비파괴 in situ 대리량** `F(dE/dP)_T` = `[인쇄]` **42.7 → 34.7 µJ mol⁻¹ Pa⁻¹(−18 %)**, 3 셀 `[도표]` 18.1–20.3 %. ⚠ 무차원 `θ` 아님 · 공극률→`dE/dP` 사상 **2 점** · `[재현]` **`dE/dP` 가 압력 구간에 2 배 의존**(0.44 mV/MPa @5–10 ↔ 0.23 @10–20, 신품끼리; 논문 무언급) · `LAM` **0 회** → **접촉 손실 = LAM 안/밖: 미언급** | **★★ 있다, 셋 — 그러나 가르는 쌍이 다르다.** 엔트로피메트리 `ΔS = −F(dE/dT)_P` · volumetry `ΔV = F(dE/dP)_T` · XRM/SEM. 주장은 `[인쇄]` "distinguish between **mechanical and chemical** degradation" — **`LAM_PE` ↔ 접촉 손실은 물음 자체가 없다.** ★★ 그리고 `[인쇄]` ΔS 는 "local physical **contact loss** … **as well as** an increase in the **interfacial resistance**" 를 **한 신호로** 받는다고 스스로 정의 ⇒ **ΔS 채널은 우리 쌍을 합친다.** 교차 실험 0(화학 단독 대조군 0 · 20 MPa 셀 엔트로피메트리 0). ★★★ 실익 = `[인쇄]` **void +5.3 %p 인 셀(86.0 %)과 +0.9 %p 인 셀(84.0 %)의 용량이 같다(역상관)** — 접촉 손실이 이 창에서는 **겉보기 `LAM_PE` 로 나타나지 않는다** | **measured-morphological**(XRM "window leveling" 문턱, 복셀·정확도 0) + **measured-thermodynamic**(ΔS drop `[도표]` 13–15 → 5.8–8 J mol⁻¹ K⁻¹ · volumetry drop 18–20 %; n = 3, **오차 막대 0**). ★ **"health" 등급(reuse/recondition/recycle)의 문턱값 0** — `[인쇄]` "quantitative metrics … requires analyzing many cells … currently difficult". 적합 라벨 0(`fit*` 0). ⚠ `[도표]` Fig. 3c "after" 곡선이 S2 세 셀 어느 것과도 끝점이 다르다(D2) | **0 (14/14 편) — 성질이 또 다르다: 역문제가 없다.** 관측이 **직접 열역학 도함수**이고 적합이 없으므로 조건수·프로파일이 **정의될 자리가 없다**; 대신 **귀속이 가정**이다(ΔS 변화 → "비균질", `dE/dP` 감소 → "void"), 대안 원인(재료 변화 · 음극 상수항 · 이완 · 압력 비선형) 배제 시험 0. `identifiab*`·`uncertaint*`·`error bar` **0**. ★ `[재현]` **sum rule 위반 후보**: 비균질은 OCV 축을 뭉갤 뿐 SOC 축 적분을 못 바꾸는데 `[도표]` 전 곡선 평균 ≈ −3.5 ↔ 후 ≈ +1.5 — 논문은 이 뺄셈을 안 한다 | **해당 없음(Li 금속) → 그러나 남는다.** `[인쇄]` "Li metal anode, whose potential can reasonably be assumed to remain constant" → 전부 양극 귀속. `[해석]` 식 (6)·(10) 의 음극항은 **상수 ≠ 0**(S°(Li) 29 J mol⁻¹ K⁻¹ · **V_m 13.0 cm³ mol⁻¹** — `[재현]` 이 항만으로 5 MPa 에 **0.67 mV**, 실측 2.2 mV 의 30 %); "10 MPa → Li creep → pore 무시" 는 pore 항 논거이지 상수항 논거가 아니다. 100 사이클 뒤 음극 계면 기여 미검토 | **★★★ 있다 — 이 계보에서 가장 새로운 형태: 압력이 관측 변수다.** 제작 100/350 MPa · 운전 **10 / 20 MPa** · 진단 **ΔP = −5 / −10 MPa (≤0.01 MPa)** · 처방 **>300 MPa**(**미수행**, 4호 미인용, Li 금속 셀에 5호 상한의 4 배). ① ★ **압력 → OCV 기울기 = 계보 최초의 `E(P)`**: `[인쇄]` 2.2 mV/5 MPa · 2.3 mV/10 MPa(**비선형, 오목**) ② 압력 → 공극률 2 점(9.8 / 5.3 %) ③ **압력 → 용량 2 점**(86.0 / 84.0 % — 역상관) ④ `[도표]` S16 재가압 뒤 **+0.4 mV 비가역 오프셋 + 감압 중 +0.5 mV 표류** = 노화 신호와 같은 자릿수(5호 이력의 그림자) ⑤ 20 MPa Li 금속 셀 `[재현]` ≈225 h 사이클에 단락 보고 0(5호 190 h 와 대조 — 설계·전류 다름). ⚠ 로드셀 명시 0 · 스윕 0(2 구간) | **해당 없음**(Li 금속). `dead li`·`isolated`·`plating` 0. CE `[도표]` S1 첫 사이클 ≈85 %, 이후 ≈98–99 %(눈금 20 %p) | **★★★ 있다 — 계보 최초로 ASSB 실셀의 OCV 축 위에 열역학 도함수를 준다.** LiNbO₃-**NCM811** / LPSCl / Li, **2.5–4.3 V**, 기울기 있음. `[도표]` ΔS(OCV) 3.53–4.25 V ≈28 점(5 % SOC 간격) + dQ/dV(OCV) 봉우리 **3.60 / 3.73(H1→M) / 4.00 / 4.18 V** 신품 → 후 3.75 + 둔덕 4.05. ⚠ **SOC 축 없음** — `E(x)` 곡선은 여전히 0 장. 접촉 손실 = LAM 안/밖: **미언급** |

| **Rahman, Lu 2024 (`assb` 15호 — 첫 **학회 회의록** · South Dakota State Univ. (Construction and Operations Management) · *Proc. IISE Annual Conf. & Expo 2024*, Abstract ID 8085 · ⚠⚠ **6 쪽 · 1차 측정 0 · 재인용 수치도 0 · 본문 그림 1 장(타 논문 재수록) · 표 0 · 식 0**)** | **없다 — 계보에서 가장 없다.** `contact` **0 회**(낱말 자체가 논문에 없다) · `percolat*`·`θ` 0 · `capacity` **0 회** · `LAM`·`LLI` 0. ASSB 기하 어휘는 `tortuos*` **1 회**가 전부이고 그것도 ref [28](Bielefeld 2020 바인더 편) 요약 안이다 | **없다.** 1차 측정 0, 인용된 관측 수단도 0 (`EIS`·`impedance`·토모·XRD 전부 **0 회**). ⚠ **Figure 1 에는 "Impedance models" 가 있는데 본문에 0 회** — 그림이 **액체셀 종설(ref [16] Zou 2023)의 재수록**이라 본문보다 넓다 | ★ **`simulated` — 그리고 그것이 확인 가능한 유일한 라벨이다.** 이 편 전체에서 SSB + ML 인용은 ref **[22]**(Asheri 2023) 한 편이고 `[인쇄]` "data-driven multiscale **simulation** framework … focusing on **interface damage**". 자기 라벨 0 · 데이터셋 0 · `experiment*`·`measur*` **0 회** · 오차막대 0 | **없다 (0/15) — 성질이 여덟 번째다: 추정기 자체가 없다.** `identifiab*`·`uniqueness`·`condition number` **0 회**. 14호가 "역문제가 없어 조건수 자리가 없음" 이었다면 **15호는 RUL 추정기가 없어 역문제를 말할 대상이 없다.** ⚠ 그런데 `accuracy` **7 회** — **정확도 수치 0 · 불확실성 표기(`RMSE`·`MAE`·`error bar`·`uncertainty`) 0** | **없다.** `indium`·`Li-In` 0. 음극은 §4.1(나)의 "lithium-anode" 2 회뿐 | **없다 — `pressure` 0 회.** ⚠ 초록이 `[인쇄]` "sensitivity to various **operational** and environmental conditions" 를 약속하고 ASSB 운전 조건의 첫째(스택 압력)를 **낱말로도 쓰지 않는다** | **없다.** `dead`·`isolated`(본문)·`dendrit*` 0 | **없다.** `NMC`·`LFP`·`LCO` 0 · OCP 곡선 0. `OCV` **1 회**는 ref [17](Dang 2016, 액체셀)의 **SOC 대리 변수**로서 — **열화 모드와 연결되지 않는다** |

| **★★ Ramanayagam, Miß, Leier, Duncker, Kirczek, Roling 2026 (`assb` 16호 — 첫 **3전극 실측** · 첫 **압력 본체 1차 측정** · Univ. Marburg (mar.quest) · *Batteries & Supercaps* 9, e70315 · ⚠ **열화 0 — `degrad*`·`aging`·`SOH`·`LAM`·`LLI` 전수 0회, 전부 신품 2번째 사이클**)** | **없다 — 그리고 "없다" 의 형태가 계보에서 가장 날카롭다.** `contact loss`·`percolat*`·`θ`·`void` **0 회**. `contact` 8 회는 전부 정성. ★★ 그런데 **식 (4)가 접촉 면적의 자리를 만들고 값을 1 로 못 박는다**: `[인쇄]` "**The area of the CAM particles in contact with the SE** normalized to the cathode volume is given by" `a_V = 3·ε_CAM/r_CAM` — **완전구 기하 면적, 접촉 분율 인자 없음**. ⇒ `θ_AM ≡ 1` 을 **이름을 붙인 채** 가정한 첫 편 | **★★ 있다 — 이 계보 최초의 전극 분해 관측.** ① **리튬화 Au/W μ-RE 3전극**(∅25 µm, 5 µA/30 min) → 양극·음극 임피던스 분리 ② **양극 두께 5 점 스윕**(26–219 µm) = TLM 의 여기 ③ **압력 2 점**. ★ **자기 검증이 있다**(계보 최초): `[인쇄]` 2E 완전지 = 3E(양극+음극) 합이 **10 kHz 아래에서 일치**. ⚠ 단 **열화가 아니라 신품 상태의 분해**이고 `LAM_PE` ↔ 접촉 손실을 가르는 데 쓰이지 않는다 | **fitted — 층위가 하나 더 깊다.** `j₀`·`τ`·`D_CAM`·`Q_DL`·`β` 가 `[재현]` **자유 파라미터 35 개 동시 적합**(공통 5 + R‖CPE 2×3×두께 5)의 출력. 고정 가정 8 개(`a_V`·`ε_SE`=0.505·`ε_CAM`=0.495·`σ`=0.47 S/m·`r_CAM`=2.5 µm[ref 30]·`dU/dc`=−3.48e−5·T·A) 가 **두 압력에 동일**. ⚠ `σ` 는 **97 MPa 에서만** 쟀다. **오차막대 0 · 반복 0 · 조건당 셀 1 · 잔차/상관 0 · 데이터 on request** | **없다 — 0 / 16.** `identifiab*`·`uniqu*`·`uncertaint*`·`condition number`·`error bar`·`confidence` **전수 0 회**. ★★ **아홉 번째 성질이고 처음으로 "축퇴를 실제로 밟으면서 모르는" 형태다**: 식 (4)+(5)에서 `R_semicircle = R·T·r_CAM/(3·F·**j₀·ε_CAM**·d)` ⇒ 데이터가 보는 것은 **`j₀ · ε_CAM / r_CAM` 한 조합**인데 뒤 둘을 고정해 **전부 `j₀` 로 읽는다**(0.74 → 1.33 A m⁻²). **9호에서 인쇄된 식으로 보인 곱 축퇴가 여기서는 실측 논문의 배정 선택으로 나타난다** → [[assb-lampe-contact-product-degeneracy]] | **★★★ 계보에서 가장 많이 준 편 — 네 겹.** ① **기준극이 Li–In 이 아니다**: 리튬화 **Au/W μ-RE**. ② **그 전위 안정성을 재지 않는다** — `stable` 3 회 중 **2 가 남의 논문**(Zhang LTO-RE 1.57 V · Hertle μ-RE 0 V), 자기 셀 검증 0. ③ `[도표]` **Fig. S1 리튬화 곡선에 평탄부가 없다** — 2.5 µAh 동안 **560 mV 표류**. ④ ★★★ `[도표]` **Fig. S3 의 In–Li 평탄 전위가 두 셀에서 0.58 V ↔ 0.47 V, ≈0.11 V 어긋난다** (둘 다 2상역 `x_Li` 0.18/0.14, `[재현]` 과전압 ≈5 mV 로 설명 불가, **논문 무언급**). ⑤ ★★★ **그 평탄 구간 안에서 음극 DRT 봉우리가 `[도표]` 18.6 → 1.2 (≈15 배) 움직인다** — **평탄 OCP 가 숨기는 양이 여기 있다** | **★★★ 본체다 — `pressure` 49 회(계보 최대, 13호 24 를 넘는다).** 제작 **389 MPa/3 min**(분리막 선압축 97), 운전 **97 / 389 MPa** = **계보 운전 압력 최댓값**(5호 Li 금속 상한 75 MPa 의 **5.2 배**, ⚠ 화학 다름). ★ **제작 = 운전인 첫 표본** — 6호가 쪼갠 두 축을 붙인다. ① **압력 → 임피던스 1 차**: 완전지 반원합 `[인쇄]` **23 → 11**(389) / **85 → 23 Ωcm²**(97), 3E 양극 **10 ↔ 20**, 음극 **4 ↔ 9 Ωcm²** ② **압력 → 공극률** `[인쇄]` **11.2 %(389) ↔ 12.9 %(97)** — 4 배 가압에 **1.7 %p** ③ ★★ **압력 → 용량이 SI 그림에만** `[도표]` 1 사이클 방전 **+9 … +59 %**(본문 `capacity` **1 회** = 서론). ⚠⚠ **스윕 아님(2 점) · 이력 0(`hysteres*` 0회) · 같은 셀 재측정 0 · 로드셀 시계열 0**. ★ 그리고 **두 점 다 389 MPa 제작 뒤라 97 MPa 은 필연적으로 하강 분기**인데 논문이 그 사실을 말하지 않는다 | **해당 없음.** In 음극. `dead`·`isolated`·`dendrit*` 0 회 | **★★ 있다 — 계보 최초로 `dU/dc` 를 숫자로 준다.** 단결정 **NMC 83|6|11**(3–6 µm, LiNbO₃ 1 wt%) + **Li₅.₃PS₄.₃ClBr₀.₇** + **In/InLi**, 70:30. 완전지 컷오프 **2.7–3.7 V vs In/InLi**, `[도표]` 양극 **3.2 → 4.25 V vs Li/Li⁺** 전 구간 기울기 있음. **`dU/dc_Li` = −3.48·10⁻⁵ V m³ mol⁻¹** (`[도표]` c ≈16 500–42 700 중 **23 000–30 000 국소 선형화**, 충·방전 **평균**을 평형 대리로 — 0.1 C pseudo-OCV). ★ **음극 OCP 완전 평탄**(0.47–0.58 V): 닻의 "ASSB 음극 = 평탄" 전제를 **In 계에서 실측 확인한 첫 표본**이고, **동시에 그 평탄함이 15 배 임피던스 변화를 숨긴다는 것도 보인다**(Q5 ⑤) |

**1호 단독 1.5 → 2편 ≈2.5 → 3편 ≈3.0 → 4편 ≈5.5 → 5편 ≈6.5 → 6편 ≈7.0 → 7편 ≈7.0 → 8편 ≈7.0 → 9편 ≈7.5 → 10편 ≈8.0 → 11편 누적 ≈8.5 칸이다.** (12·13·14편 ≈8.5 유지 — 12·13호는 종설, 14호는 새 칸 대신 **층 셋**: Q1 "비파괴 대리량" · Q6 "압력 → OCV" · Q8 "OCV 축 열역학 도함수". **15편도 ≈8.5 유지 — 새 칸 0이고, 이 편은 Q1·Q4·Q6 에서 "안 쟀다" 가 아니라 "낱말이 없다" 여서 계보의 바닥을 찍는다.**
**→ 16편 ≈9.5 — 14편 만에 칸이 움직였다**: **Q2 +0.5**(전극 분해 관측이 처음으로 들어왔고, 2E = 3E 합으로 **자기 검증**까지 있다) ·
**Q5 +0.5**(기준극을 실제로 설치한 첫 편이고, 그 기준의 **셀 간 0.11 V 어긋남**을 지면이 인쇄한다).
**Q1·Q4 는 그대로 0** — 그리고 16호의 0 은 "낱말이 없다"(15호)도 "안 쟀다"(1–7호)도 아닌 **"밟고 지나갔다"** 다.)

## ★★★ 2026-09-22 (16호 Ramanayagam et al. 2026) — **접촉 면적의 자리를 만들고 값을 1 로 못 박는 첫 편**

`raw/papers/ramanayagam2026_stack-pressure-three-electrode-assb-impedance.md`.
NMC83|6|11(단결정) ‖ Li₅.₃PS₄.₃ClBr₀.₇ ‖ **In/InLi**, 제작·운전 **389 MPa** 또는 운전 **97 MPa**,
양극 두께 **26–219 µm 5 점**, **리튬화 Au/W μ-RE 3전극**, **SOC50 · 2 번째 사이클 · 셀 12 개 · n = 1**.
⚠ **열화가 없는 편이다** (`degrad*`·`aging`·`LAM`·`LLI`·`SOH` 전수 0 회). 그래서 이 카드에
주는 것은 **열화 라벨이 아니라 역문제의 구조**다.

1. ★★★ **식 하나가 이 카드의 물음을 그대로 담는다.** `[인쇄]` 식 (4):
   "**The area of the CAM particles in contact with the SE** normalized to the cathode volume"
   = `a_V = 3·ε_CAM / r_CAM`. **이름은 "접촉 면적" 인데 계산은 완전구 기하 면적이다** —
   접촉 분율 인자가 **없다**. 그리고 식 (5) `R_CT = RT/(F·j₀)` 와 얇은 전극 극한
   `R_semicircle = R_CT/(a_V·d)` 를 합치면 `[해석]`:
   ```
   측정량이 보는 것 = R·T·r_CAM / ( 3·F · j₀ · ε_CAM · d )   ⇒  식별되는 것은  j₀ · ε_CAM / r_CAM  한 조합
   ```
   **9호(Huo 2025)의 `A_eff·ε_p/R_s` 와 같은 자리**다. 다른 점은 9호가 **모델 논문**이었고
   16호는 **실측 논문**이며, **여기서는 저자가 실제로 한쪽 끝을 골라 잡는다** —
   `ε_CAM`·`r_CAM` 고정, 압력 차이 전부를 **`j₀` 0.74 → 1.33 A m⁻²** 로.
2. ★★★ **그리고 같은 Table 2 가 반대 배정을 품고 있다.** 이중층 CPE 계수
   `Q_DL` **0.18 → 0.54 (3.0 배)** 는 **계면 면적에 비례하는 양**이다. 접촉 분율 `θ` 를 넣으면
   `R_CT^meas = R_CT^true/θ`, `C^meas = θ·C^true` 이므로:

   | 배정 | `θ(389)/θ(97)` | `j₀^true` 비 | 논문의 **말**과 |
   |---|---:|---:|---|
   | 논문 (`θ ≡ 1`) | 1.0 | **1.80 증가** | 수치 결론 |
   | `Q_DL` 을 면적으로 읽음 | **3.0** | `[재현]` **0.60 감소** | `[인쇄]` "pressure improves the **interfacial contacts** … considerably" 와 정합 |

   `[해석]` **같은 데이터가 `j₀` 의 증가와 감소를 둘 다 허용한다.** 그리고 논문의 **문장**은
   둘째 배정을 말하고 **숫자**는 첫째 배정을 쓴다. ⚠ `β` 가 0.89 ↔ 0.81 로 달라 두 `Q` 는
   엄밀히 차원이 다르다 — `[재현]` Brug 류 유효용량으로 고치면 비가 **3.0 → ≈5.6** 으로
   **커진다**(결론 방향은 유지). 자세히는 [[assb-lampe-contact-product-degeneracy]].
3. ★★ **음극에는 면적 서사, 양극에는 동역학 서사 — 같은 논문 안에서.**
   `[도표]` Figure 5 모식도는 압력이 바꾸는 것을 **"interphase 를 통하는 칸의 개수"**
   (저압 통함 3/8 ↔ 고압 5/8)로 **그림으로 명시**한다. 그런데 §TLM 은 양극에서
   바로 그 **유효 면적을 고정**한다. `[해석]` **전극이 바뀌면 같은 현상의 이름이 바뀐다.**
4. ★★ **Q5 가 네 겹으로 채워진다** (위 표 16호 행). 요점만: 기준극이 **Li–In 이 아니라**
   리튬화 Au/W 이고 · **그 안정성을 인용으로 가정**하며 · `[도표]` **리튬화 곡선에 평탄부가 없고**
   (2.5 µAh 에 560 mV 표류) · `[도표]` **두 셀의 In–Li 평탄 전위가 0.58 ↔ 0.47 V 로 0.11 V
   어긋난 채** 같은 "vs Li/Li⁺" 축에 그려진다. `[재현]` 0.1 C 음극 과전압은 ≈5 mV 라 설명이 안 된다.
   ★ `[해석]` **완전지 OCV 를 "밀린 양극 곡선" 으로 읽는 계획에서, 밀린 양의 셀 간 재현성이
   0.1 V 자릿수라면 그것은 `LLI` 로 오독될 크기다.** 4호가 오프셋 0.6 V 를 고정 가정했던
   경고가 **기준극을 실제로 설치한 편에서도 사라지지 않는다.**
5. ★★★ **평탄 OCP 가 숨기는 양을 처음으로 숫자로 본다.** `[재현]` SI Table 의 `x_Li`
   (0.05–0.28)는 **In + InLi 2상 공존역 안**이고 `[도표]` Fig. S3 에서 음극 전위는 **완전 평탄**
   이다. **바로 그 구간에서** `[도표]` 음극 DRT 봉우리가 **18.6 → 1.2 (≈15 배)** 움직인다
   (97 MPa; 389 MPa 에서는 1.6 → 0.30, **5 배**). `[해석]` **닻의 출발 전제("ASSB 음극은 평탄이라
   완전지 OCV 는 양극 곡선 하나")가 열역학 축에서는 맞고 동역학 축에서는 완전히 틀린다.**
   OCV 적합이 `LAM_PE` 와 접촉 손실을 가르지 못하는 것과 **별개로**, 음극이 평탄하다는 사실이
   **음극이 조용하다는 뜻은 아니다.**
6. ⚠ **압력 이력에는 답하지 않는다 — 그리고 그 물음이 왜 중요한지를 보여 준다.**
   두 압력이 **다른 셀**이고, **둘 다 389 MPa 제작을 거친다.** ⇒ `[해석]` **97 MPa 데이터는
   전부 하강 분기**인데 논문은 두 압력을 **대칭적인 두 조건**처럼 비교한다 (`hysteres*` 0 회).
   5호(Doux)의 `θ(P)` 경로 의존이 참이면 이 비교의 해석이 달라진다.
7. **Q4 의 아홉 번째 성질 — "밟고 지나갔다".** 안 쟀다(1–7호) → 이름만(8호) → 지문이 자기 표
   안에(9호) → 분야가 명제로(10호) → 재료만(11호) → 0(12·13호) → 역문제가 없어 자리가 없음
   (14호) → 추정기가 없어 대상이 없음(15호) → **16호: 역문제를 풀고 축퇴한 조합 위에 서 있으면서
   `identifiab*`·`uncertaint*`·`error bar` 가 전수 0.** **여전히 0/16.**

★ **2026-09-22 (15호 Rahman & Lu 2024) — 새 칸 0. 이 편이 준 것은 근거가 아니라
**계보의 바닥 눈금**과, 이 위키 최초의 **원전 대조 실측** 둘이다.**

- ★★★ **1호(Bielefeld 2019)가 야생에서 어떻게 인용되는지를 처음 봤다 — 그리고 어긋난다.**
  15호 ref **[5]** 가 우리 1호이고, 인용된 **유일한 자리**가 `[인쇄]` "They mainly address
  key challenges such as **load balancing, state-of-charge estimation, and overall battery
  health monitoring [5, 6]**" 다. 우리 1호 digest 는 그 논문에 `[인쇄]` **"셀 실험 0,
  사이클링·전압·용량이 없다"** · `voltage` **1 회(그마저 참고문헌 제목)** · **모델에 음극이
  없다**고 전수 계수로 기록해 뒀다. **부하 균등화·SOC 추정·건전성 모니터링은 그 논문에
  없다.** ⚠ 서지도 틀렸다 — **연도 2018 (원전 2019)**, 저자 "W. Dominik A"(= Dominik A.
  **Weber**).
  `[해석]` **단순 번호 실수로 보기 어렵다** — 같은 저자의 **다른 논문 [28]**(2020 바인더
  편)이 §4.1 에 따로 있고 거기서는 내용이 대체로 맞게 요약된다. 서론의 `[5, 6]` 은
  "SSB 문헌임" 만으로 고른 **장식 인용**이다.
  ★ **이것이 우리에게 주는 것**: 1호 digest §12.4 에서 `Q_apparent = θ_AM · Q_material`
  을 **우리 해석**이라고 못 박고 "논문은 용량도 전압도 주지 않는다" 고 적었던 경고가
  **과하지 않았다는 증거**다. 바깥에서는 그 다리 없이 BMS 문장에 직결된다.
- ★★ **12호(Kouhestani 2022)와의 대조 — 어긋나지 않지만 껍데기만 간다.**
  15호 ref **[21]** 이 우리 12호이고, 쓰인 자리가 **FNN/RNN 의 교과서적 정의 한 문장**이다
  (우리 12호 digest 가 그 수준을 채록하지 않아 **어긋남은 미확인·정합 추정**).
  ★ 문제는 **12호의 자기 결론을 한 글자도 옮기지 않는다**는 것 — 우리가 Table 1 을 한 줄씩
  대조해 적은 `[재현]` **"SSB 실측 열화 데이터로 SOH/RUL 을 추정한 항목 0 / 28"** 과
  `[인쇄]` "most PHM techniques are based on **simulation** results and not experimental".
  `[해석]` **12호(2022)가 감사로 적어 둔 공백을 15호(2024)가 12호를 인용하면서 재생산한다.**
  12호 항목이 "2022 → 2026 사이 PHM 문헌은 identifiability 라는 **이름**을 얻었고 여전히
  재지 않았다" 로 끝났는데, **15호는 그 사이(2024)에서 이름조차 못 얻은 표본**이다
  (`identifiab*` **0 회**).
- ★★ **분류 체계 세 번째 표본 — "미도입" 유형.** 12호 = `LAM ⊃ 접촉 손실`(**정의로 병합**) ·
  13호 = **미배정** · **15호 = 어휘 미도입**(`contact` **0 회**). 세 편 다 **종설/전망/회의록**
  이고, **1차 측정이 있는 편(4·5·6·7·9·11·14호)은 전부 어떤 형태로든 접촉 축을 갖는다.**
  `[해석]` **접촉 손실이라는 구분은 실험 층위에서 강제되고 종합 층위에서 소실된다** —
  우리가 폭을 재서 공급하려는 대상이 **종합 층위**라는 뜻이다. ⚠ 표본 3 개, 다음 종설에서 다시 본다.
- ⚠ **Q4 의 성질 — 여덟 번째, 그리고 가장 얕다.** 안 쟀다(1–7호) → 이름만(8호) → 지문이
  자기 표 안에(9호) → 분야가 비유일성을 명제로(10호) → 재료만 인쇄(11호) → 0(12·13호) →
  역문제가 없어 조건수 자리가 없음(14호) → **15호: 추정기 자체가 없어 역문제를 말할
  대상이 없다.** 그런데 `accuracy` **7 회** : 정확도 수치 **0** : 불확실성 표기 **0**.
  **여전히 0/15.**
- ★ **후속 후보 1 순위 신설**: **Asheri et al., *Comput. Mater. Sci.* 226, 112186 (2023)**
  (이 편 ref [22]) — 이 계보에서 **ML × SSB 계면 손상**이 만나는 첫 좌표이고, **12호가
  감사한 28 슬롯에도 없던 항목**이다. 2 순위 **Bielefeld 2020 *ACS AMI* 12, 12821**
  (ref [28]) — 1호의 직계 속편, 1호 모집단 경고("탄소·바인더 없는 2 성분")의 바인더 축.

★★ **2026-09-22 (14호 Oh et al. 2025) — 새 칸 0, 그러나 이 카드의 물음에 가장 직접적인
실측 하나와 Q4 의 일곱 번째 성질이 들어왔다.**

- ★★★ **접촉 손실(void)이 겉보기 용량에 안 보인다는 실측** — `[인쇄]` void 4.5→9.8 % 셀
  86.0 % ↔ 4.4→5.3 % 셀 84.0 %. 이 카드의 물음이 "OCV 적합이 접촉 손실을 `LAM_PE` 로
  **오독**하는가" 였다면, 이 창(50 사이클, 10–20 MPa)에서는 **오독할 신호 자체가 용량에
  없다** — `θ_AM` 이 `p_c` 위에서 ≈1 로 버티는 1호 그림과 정합. `[해석]` 접촉 손실 → 용량
  사상은 **문턱형**이고, 문턱 아래에서 OCV 적합은 `LAM_PE ≈ 0` 을 정확히 보고하되 **void 가
  2 배 됐다는 사실을 놓친다** — 그것을 보는 것이 volumetry 다.
- ★★ **Q4 의 성질 — 일곱 번째: 역문제가 없어서 유일성 물음이 사라진 자리.** 8호 이름 →
  9호 지문 → 10호 명제 → 11호 재료 → 12·13호 0 → **14호: 관측이 직접 도함수라 조건수가
  정의될 자리가 없고, 그 대신 "귀속의 유일성"(ΔS 변화 = 비균질? `dE/dP` 감소 = void?)을
  아무도 묻지 않는다.** 여전히 **0/14**.
- ★★ **Q2 의 형태 — 세 번째**: 1–10호 형태학, 11호 조작, **14호 열역학 도함수**. 그리고
  이 편의 ΔS 는 스스로 우리 쌍(접촉 손실 + 계면 저항)을 **합친 신호**라고 정의한다 →
  분리 관측 후보는 **volumetry 쪽**이다 (`[해석]`, 아래 새 제약).
- ✅ **Q6 에 새 층** — 압력이 사이클 변수·개입이 아니라 **관측 변수**(소신호 ΔP = −5 MPa,
  가역). 계보 최초의 `E(P)` 두 구간과 그 **비선형**(2 배).
- ✅ **Q8 에 새 층** — OCV 축 위의 열역학 도함수 ≈28 점 × 3 셀 × 전·후. ⚠ SOC 축 없음.
- ⚠ **13호 후속 4 순위(Oh *AEM* 2025) = 이 편 ref [10], 같은 저자·연구실** → 1 순위로 승격.

★★★★ **2026-09-22 (11호 Yu et al. 2024) — 두 칸이 움직였고, Q4 의 성질이 다섯
번째로 바뀌었다.**

- ✅ **`Q1` 의 10/10 편 0 이 반쯤 깨졌다.** 여전히 **무차원 분율은 없다**(`θ` 0 회).
  그러나 이 계보 최초로 접촉 손실 대리량이 **주파수로 국소화되고 · 시계열이 있고 ·
  조작으로 되돌려진다**. ⚠ 그리고 같은 그림이 **그 대리량이 전극을 가르지 않는다**는
  것도 같이 인쇄한다 (Fig. 8 의 P3 에 Cathode + Anode).
- ✅✅ **`Q6` 의 마지막 빈칸(`압력 → 용량 곡선`)이 채워졌다** — 10/10 편이 못 주던
  것이다. 반쪽 3 점 + 완전지 2 점. ⚠ 다만 **점이 5 개이고 계측 수단이 없다**.
- ★★★ **`Q4` 의 성질 — 다섯 번째 변신**: 안 쟀다(1–7호) → 이름이 로드맵 실패 모드에
  (8호) → 지문이 자기 표 안에(9호) → 방법의 비유일성이 분야의 공식 문장(10호) →
  **11호: 축퇴의 크기를 잴 재료를 SI 에 인쇄해 놓고 본문 효과와 나란히 놓지 않는다.**
  **여전히 "쟀다" 가 아니다 — Q4 는 0/11 이다.** 7호가 `LLI` 뺄셈을 안 한 것과
  **같은 형태**이고, 축이 Q7 이 아니라 Q4 이며 재료가 **SI 에** 있다는 점이 다르다.
- ★★★ **`Q8` 이 이 카드의 출발 전제를 깼다** (위 표 끝 칸). **흑연 음극이면
  5 → 3 파라미터 붕괴가 성립하지 않는다.** 이 카드 §"지금까지 아는 것" 의 붕괴표는
  **Li-In / Li 금속 / 무음극 셀에만** 유효하다.
- ★★ **`Q2` 가 형태를 바꿨다** — 1–10 호에서 "가르는 관측" 은 **형태학**(FIB-SEM ·
  토모 · XRD)이었다. 11호는 **형태학이 0 인데 조작이 넷**이다(반쪽전지 분해 · 입도
  스윕 · 코팅 유무 · 재가압). `[해석]` **분해를 관측이 아니라 설계로 한다** —
  그래서 결론이 **설계가 통제한 것만큼만** 강하다.
- ⚠ **`Q3` 가 후퇴했다.** 9호는 표에 "not disclosed" 를 찍기라도 했는데 **11호는
  파라미터 표가 없다.** `[인쇄]` "The authors do not have permission to share data."

★★★ **10호가 `Q4` 의 0 을 처음으로 깼다 — 그리고 깬 방식을 정확히 적어야 한다.**
**"쟀다" 가 아니다**(측정 0, 10/10 편 그대로). **"축퇴가 일반 현상임을 방법론으로
인쇄했다"** 이다: `[인쇄]` "**no solution to an EIS spectrum is unique**" ·
"**the inclusion of more elements will tend to improve the fit**" ·
"how many time constants … **highly subjective**", 그리고 모델 선택을 **AIC** 라는
통계 문제로 명명한 뒤 `[인쇄]` "**thorough validation against experiment in the
context of ASBs is desirable**" 로 **열린 문제로 등록**한다.
→ **Q4 의 성질이 네 번째로 바뀌었다**: 안 쟀다(1–7호) → 이름이 로드맵 실패 모드에
올랐다(8호) → 지문이 자기 표 안에 있고 다르게 불린다(9호) →
**방법 자체가 비유일하다는 것이 분야의 공식 문장이 됐다(10호).**
⚠ **`Q1` 은 10/10 편이 여전히 0 이다.**
★ **9호가 반 칸을 늘렸다** — **Q6 이 "점·스윕" 에서 "시계열" 로** 바뀐 것과 **Q3 의 새 층위**(`fitted-single-parameter`)다.
★★★ **그리고 Q4 의 성질이 세 번째로 바뀌었다**: 1–7호 "안 쟀다" → 8호 "이름이 로드맵의
실패 모드 목록에 올랐다" → **9호 "지문이 자기 표 안에 있고 다르게 불린다".**
**Q1 과 Q4 의 0 은 9호도 채우지 못했다.** 그러나 9호는 **이 계보에서 처음으로
"열화 모드의 지분을 적합으로 정하는" 논문**이고, 그래서 **처음으로 이 카드의 Q4 가
관망이 아니라 직접 적용된다** — 자세한 것은 [[assb-lampe-contact-product-degeneracy]].
★ **8호도 칸을 늘리지 않았다** (Q1 정량 0 · Q4 이름만 · Q6 재인용 1 점 · Q3 는 다른 층위).
★★★ **대신 세 가지가 바뀌었다**:
① **Q4 의 성질** — 1–7 호 "`identifiab*` 0 회, 아무도 안 쟀다" →
**8호 "로드맵 표의 실패 모드 항목(`Unidentifiable pulse response`)으로 올라갔다"**.
4호가 EIS 축퇴를 인쇄로 인정한 것과 같은 계열이되, 이쪽은 **해야 할 일의 목록**에 있다.
② **Q1 의 성질** — 1–7 호 "일곱 편이 일곱 개의 다른 양을 접촉 손실이라 부른다" →
**8호 "접촉 손실과 보통 노화를 가르는 진단이 필요하다" 가 BMS 요구 사항으로 인쇄됐다.**
**이 카드의 질문이 문헌의 요구 목록에 올라 있다.**
③ **Q6 의 아래 벽** — 실험실 창 전체(2–490 MPa)가 **산업 요구치(<≈1 MPa) 위**에 있다.
⚠⚠ **8호는 Mini Review 다 — 1차 측정이 0 이고 위 수치는 전부 재인용이다.**
근거로 쓰려면 원 논문을 받아야 한다 (Status Log 의 후속 후보표).
★ **7호는 칸을 늘리지 않았다** (Q1·Q4 가 여전히 0, Q8 은 해당 없음, Q6 은 오히려 후퇴).
★★★ **대신 Q7 의 성질이 바뀌었다**: 5호 "수단이 없다" → 6호 "채널은 있고 정량이 0" →
**7호 "수치가 계산 가능하다"** (`[재현]` 0.79 mAh cm⁻² = 39 %). ⚠ **논문이 그 뺄셈을
하지 않는다** — 효율도 비가역분도 인쇄되지 않는다.
★★ 그리고 7호는 **6호를 외부에서 검증한 첫 편**이다 (§아래 Evidence).
★★ **5호가 Q6 을 "점" 에서 "곡선" 으로 바꿨고, Q7 의 4/4 편 0 을 절반 깼다.**
★★★ **6호는 Q6 을 "한 축" 에서 "두 축"(제작 ↔ 운전)으로 쪼갰고, Q7 에 채널 둘
(EELS Li 맵 · XRD Li₉Ag₄)을 더했다 — 정량은 여전히 0 이다.** 그리고 **Q5 를
"무음극이라 해당 없음" 으로 닫는 대신 같은 문제를 새 형태로 연다**(음극 전위가
앞 10–17 % 구간에서 평탄하지 않다). **Q1 과 Q4 는 6호도 채우지 못했다.**

- ✅✅ **Q6 이 두 축이 됐다.** 5호까지 "압력" 은 한 변수였다. 6호는 **제작 압력
  (490 MPa 등방, 비가역)** 과 **운전 압력(2 MPa)** 을 분리하고, **제작 압력이 충분하면
  운전 압력이 할 일이 없다**는 것을 무압 대조로 보인다 → [[assb-stack-pressure-operating-window]].
  ⚠ 동시에 **운전 상한이 훨씬 낮다**: `[인쇄]` **4 MPa 초과에서 단락 확률 증가**
  (5호의 Li 금속 75 MPa 의 **1/19**). ⚠⚠ **그 문장에 데이터가 없다.**
- ✅ **Q7 의 채널이 둘 늘었다 — 정량은 0 이다.** 5호가 "SEI 는 상으로 잡히고 dead Li 는
  수단이 없다" 로 남겼다. 6호는 **EELS Li 맵**(Li 특이 채널, 계보 최초)과
  **XRD 의 Li₉Ag₄**(Li 를 담은 그릇)을 더한다. **dead Li 만 여전히 수단이 없다** —
  그리고 6호는 **"isolated lithium" 을 열화 기구로 지목하고도 재지 않는다.**
  → 자세히는 [[anode-free-li-inventory-accounting]].
- ★★★ **새 축이 하나 열렸다: `LLI` 추정자의 분해능.** 6호 안에서 **20 mAh 셀은
  CE(99.97 %)와 유지율(92.5 %@300 = 99.974 %/cycle)이 맞고, 0.6 Ah 셀은 10 배
  어긋난다**(CE `[도표]` 99.89 % ⇒ 누적 결손 161 mAh g⁻¹ ↔ 실측 손실 16).
  **CE 축의 눈금조차 다르다**(95–101 vs 99.4–100.0). 논문은 두 셀을 **한 번도
  비교하지 않는다.** → **우리 폭 측정기가 바로 걸리는 자리.**
- ⚠ **Q1 은 여섯 편이 여섯 개의 다른 양을 다룬다 — 그리고 6호는 아예 안 잰다.**
  1호 기하 부피분율 · 2호 연결성 · 3호 계면 응력 · 4호 접촉 면적 + void 부피 ·
  5호 전기적 대리량(음극) · **6호 없음(공정으로 대체)**.
- **Q4(유일성)는 `assb` 6/6 편이 여전히 0.**

- ✅ **Q6 이 스윕이 됐다.** 4호는 각 1 점(2 MPa · 300 MPa)이었다. 5호는 **세 개의
  곡선**을 준다 — 그리고 **압력을 로드셀로 실제 계측한 첫 편**이다.
  ★ 가장 큰 수확은 **상한**이다: `[인쇄]` **75 MPa 는 도금 전에 이미 기계적으로
  단락한다.** → **4호의 300 MPa 재가압은 이 상한의 4 배**이고, Li 금속 셀에
  그대로 적용하면 **회복 용량을 읽기 전에 셀이 죽는다.**
  ⚠ 단 **모집단이 다르다** (4호 In 음극 vs 5호 Li 금속) — **상한은 음극 재료의 함수**다.
- ✅ **Q7 이 절반 깨졌다 (4/4 → 5호).** 이 계보 첫 **Li 금속 음극** 논문이고
  형태학을 3D in situ 로 본다. 그런데 **가른 것은 dead Li ↔ SEI Li 가 아니라
  "형태(토모) ↔ 화학(XRD)" 두 채널**이다. **SEI 는 상으로 잡히고 dead Li 는 안
  잡힌다** — Li 금속이 XRD 로 원리적으로 안 보이기 때문이다.
- ⚠ **Q1 은 다섯 편이 다섯 개의 다른 양을 "접촉 손실" 이라 부른다.** 5호의 것은
  **전기적 대리량(Ω)** 이고 **전극이 다르다(음극)**. `θ` 로 변환되지 않는다.
- **Q4(유일성)는 `assb` 5/5 편이 여전히 0.** 5호는 역문제를 **아예 풀지 않는다**
  (등가회로 0) — 4호가 "축퇴를 인쇄로 인정하고 점추정" 이었던 것과도 다른 형태다.
★★ **4호가 한 편에서 세 칸을 깼다: Q2(실험) · Q6(압력) · Q8(실측 전압곡선).**
그리고 Q1 을 **무차원 분율 + 시간축**으로 처음 채웠고, Q5 를 **부분**으로 열었으며,
Q3 에 새 층위(**measured-but-ML-thresholded**)를 추가했다.

- ✅ **Q2 가 깨졌다 (3/3 → 4호).** `assb` 1·2·3 호는 **전부 시뮬레이션**이었고 자기
  실험이 0 이었다. 4호는 **처음부터 끝까지 실험이고 시뮬레이션이 한 줄도 없다.**
  ★ 가장 큰 수확은 **개입**이다 — 50 사이클 후 **300 MPa 재가압**으로 용량이
  `[도표]` ≈2 → `[인쇄]` **80 mAh g⁻¹** 로 돌아왔다 (`[재현]` **+60.5 %p**).
  **진짜 재료 손실은 눌러도 안 돌아오고, 닿지 않던 활물질은 돌아온다** →
  [[assb-pressure-reapplication-separation-test]].
- ✅ **Q6 이 깨졌다 (3/3 → 4호).** 제작·사이클·개입 **세 역할**로 압력을 쓴다.
  ⚠ 단 **스윕이 없다**(사이클 2 MPa 1 점, 재가압 300 MPa 1 점)이고 압력값이
  **전부 ESI 에만** 있다 — 본문은 초록의 "large external pressure" 가 얼마인지도
  Fig. 1 캡션에서야 밝힌다.
- ✅ **Q8 이 실측으로 닫혔다.** 3호의 OCV 는 **액체 반쪽전지 GITT**(타 논문 입력)였다.
  4호는 **ASSB 실셀의 사이클별 V–Q** 를 준다. ⚠ 단 CC 곡선(≈C/15)이지 OCV 가 아니다
  (`OCV`·`open-circuit` 0 회).
- **Q4(유일성)는 `assb` 4/4 편이 여전히 0.** 1–3 호는 forward 전용이라 **원리적으로**
  못 쟀지만, ★ **4호는 역문제를 풀면서**(EIS 3-RC 등가회로) **축퇴를 인쇄로 인정하고도
  점추정을 보고한다.** → **이 축은 이제 "아무도 안 쟀다" 가 아니라 "재야 한다고
  문헌이 스스로 적어 놓았다" 가 됐다.**
- **Q7 은 4/4 편 0.** (4호는 In 음극이라 dead Li 축이 원래 없다 — 구조적 공백.)
- **Q1 은 네 편이 네 개의 다른 양을 "접촉 손실" 이라 부른다**: 기하 **부피**분율(1호) ·
  연결성(2호, 1호와 동일) · 계면 **인장응력**(3호, 차원 다름) ·
  **접촉 면적분율 + void 부피분율**(4호, 차원은 맞으나 **사상 미정**).
  ★ **4호의 실측이 1호의 곱셈 형태를 6 배로 배반한다** (10.4 % ↔ 60 %p, 아래 Evidence).

## Evidence For / Against

### For — "OCV 만으로는 못 가른다" 쪽 (2026-09-16, Bielefeld 2019)

- **접촉 손실이 `LAM_PE` 와 섞이는 방식이 확정됐다: 곱셈.**
  [[composite-cathode-percolation-utilization]] 의 `θ_AM` 은 재료량을 건드리지 않고
  **용량 축 스케일에 곱해진다** (`Q_apparent = θ_AM · Q_material`, 우리 해석).
  OCV 곡선은 **곱만** 본다 → 위 "모르는 것 1" 의 **형태**가 정해졌다.
- **`A_spec,a` 봉우리가 평탄하고 두께 곡선이 겹친다** — forward map 자체가 이미
  납작하다. [[fitting-degeneracy]] 가 화학 무관하게 재현될 자리.

### For 보강 (2026-09-16, Clausnitzer 2023) — **혼동원이 하나 더 있다**

- **곱셈 축퇴에 항이 하나 더 붙었다.** 같은 논문 안의 반례: `SVF_LCO = 69.4 %`,
  소결 밀도 70 %, 입계 저항 무시 → `[도표]` **CAM 연결성 ≈100 %** 인데 **정규화 용량 ≈0.10**.
  → `Q_apparent = θ_AM · **η(i)** · Q_material` ([[assb-apparent-capacity-decomposition]]).
  OCV 적합이 상대해야 할 것이 **둘이 아니라 셋**이다.
- **동역학 성분의 크기가 처음으로 숫자로 나왔다.** `[도표]` Fig. S5: 재료·기하가 전부
  동일하고 **입계 저항만** 0 → 3.6 Ω cm² 로 바꾸면 방전 용량이
  **1.37 → 0.385 mAh/cm²** — **겉보기 `LAM_PE` 72 %.** 재료 손실은 0 이다.
- **그리고 그 곡선은 아핀 스케일링이 아니다** (시작 전압 −175 mV, 기울기 다름).
  → `bms-balancing/docs/ASSB_TRANSFER_NOTE.md` §1 의 3 파라미터 창 모형으로는 **못 맞춘다.**

### For 보강 (2026-09-16, Liu 2024) — **문헌이 축퇴를 인쇄로 인정했다**

- ★★ **이 질문의 축퇴가 논문 문장으로 확인된 첫 사례.** `[인쇄]` "the experimental
  analysis of active cathode material loss generally involves the formation of **rock-salt
  phase AND isolated cathode materials induced by intergranular fracture**. Since this
  study does not explicitly consider crack formation, **only qualitative comparisons** are
  made between predictions and experimental characterisations."
  → **실험이 보고하는 "활물질 손실" 은 (진짜 재료 손실) + (기하적 고립 = 접촉 손실)의
  합이고, 그 측정으로는 안 갈라진다.** 우리가 물어 온 것이 그대로 적혀 있다.
  ⚠ 그런데 같은 논문이 **앞 항만 모델링하면서** 뒤 항까지 포함한 실험값과 Fig. 5e 에서
  겹쳐 놓는다 — 체계적으로 과소예측해야 정상인데 겹친다.
- ★ **진짜 `LAM_PE` 의 생성 기구가 처음 들어왔다.** 불균일 Li → 전위(소성전단) →
  격자변형 → 산소공공 형성에너지 하락(`[인쇄]` 10 % 인장에서 1.06 → 0.24 eV) →
  rock-salt. 즉 **`Q_material` 이 줄어드는 물리**. `[도표]` 12 µm 에서 활물질 손실이
  0.25C 0.093 → 5C **0.185**.
- ★ **그리고 그것이 율 의존이다** → 아래 "새 제약" 의 첫 항목.

### ⚠ For 에 붙는 **실측 반례** (2026-09-16, Shi 2020) — **곱셈 형태 자체가 6 배 어긋난다**

- ★★ **접촉 손실 면적 10.4 % ↔ 압력으로 되돌아온 용량 ≈60.5 %p.**
  `[인쇄]` 4호는 50 사이클 시료에서 "the estimated contact loss area is **10.4 % of the
  total cathode surface area**" 를 재고, 같은 논문에서 300 MPa 재가압으로
  `[도표]` ≈2 → `[인쇄]` **80 mAh g⁻¹** (129 기준 `[재현]` **+60.5 %p**) 를 회복한다.
  곱셈 `Q_apparent = θ_AM · Q_material` 에 면적 분율을 그대로 넣으면 손실이 **10 %**
  여야 한다. **≈6 배 어긋난다.** ⚠ **논문은 두 수를 나란히 놓고 한 번도 비교하지 않는다.**
- `[해석]` 가능한 설명 셋, 논문은 **어느 것도 검증하지 않는다**:
  ① **면적 → 부피 사상이 비선형(문턱)이다** — 4호 자신이 근거를 준다:
  `[인쇄]` 접촉 손실이 입자 **한쪽에 몰리면** "all the Li ions … have a **much larger
  distance to travel**", 균일 분산이면 "diffusion gradients … would **rapidly fade out**".
  ② **라벨과 관측이 다른 셀**이다 — **토모그래피 3 셀의 용량이 한 번도 보고되지 않는다.**
  ③ **회복분이 양극이 아니다** — 아래.
- ★★ **회복의 대부분이 음극이다.** `[도표]` Fig. 1(c) 재가압 회복률:
  **`R_LF`(음극 쪽) ≈65 %** · `R_HF` ≈46 % · **`R_MF`(양극 쪽) ≈23 %** (`[재현]`,
  `R_MF` 는 인쇄값 3283→2755 Ω). 그리고 50 사이클에 `R_LF ≈110 kΩ` 가 전체의 **≈93 %**.
  → **용량 회복률(≈61 %p)과 가장 잘 맞는 것은 양극이 아니라 음극이다.**
  ⚠ 4호의 초록·결론은 **양극 접촉 손실**로 돌린다 — **자기 그림이 다르게 말한다**
  (4호 digest D8). 본문 한 문단만 `[인쇄]` "some **anode delamination** could also exist"
  로 인정하고 만다.
- `[해석]` **우리에게 이것은 나쁜 소식이 아니라 좌표다**: `θ` 를 스칼라 곱셈 인자로
  쓰는 모형은 **실측과 6 배 틀린다.** DEM 이 싸게 주는 것도 **접촉 수·면적**이므로
  **면적 → 이용 가능 용량 사상을 우리가 만들어야 한다.**

### ⚠ For 에 붙는 **두 번째 실측 반례** (2026-09-16, Doux 2020) — **회복의 전극 귀속**

- ★★ **압력 실험은 양극 전용 조작이 아니다 — 양극이 없는 셀에서 증명된다.**
  5호의 Fig. 4c 셀은 **Li | Li₆PS₅Cl | Li 대칭셀**로 **복합양극이 아예 없다.**
  그런데 압력을 1 → 25 MPa 로 올리면 임피던스가 `[인쇄]` **>500 Ω → 32 Ω (>15 배)**
  움직이고, 25 MPa 를 찍고 5 MPa 로 내리면 `[인쇄]` **110 → ≈50 Ω** 로 **되돌아오지
  않는다**(영구 정합).
  → **압력이 되돌리는 접촉의 큰 몫이 음극/전해질 계면에 있다는 것이 독립 논문에서
  확인된다.** 4호의 `R_LF`(음극) 65 % vs `R_MF`(양극) 23 % 회복률과 **같은 방향**이다.
  `[해석]` **`ΔQ_mech` 를 통째로 양극 `θ_AM` 회복으로 읽으면 과대평가다** —
  분리 시험에 **전극 분해 관측**(3전극 또는 대칭셀 짝)이 필요하다.
- ★★ **그리고 처방에 상한이 생겼다.** `[인쇄]` Li 금속 / Li₆PS₅Cl(상대밀도 ≈82 %) /
  75 µA cm⁻² 에서 **75 MPa 는 도금 전에 이미 기계적으로 단락**한다.
  **4호가 쓴 300 MPa 는 그 4 배다.** ⚠ 모집단 차이(In 음극 vs Li 금속)를 붙여야 하지만,
  **연산자가 파괴적일 뿐 아니라 셀을 즉사시킬 수 있다**는 것이 숫자로 들어왔다.
  → [[assb-stack-pressure-operating-window]].
- ★ **율 연산자와 압력 연산자가 직교하지 않는다.** `[도표]` 5호 Fig. S4:
  같은 전류밀도(75 µA cm⁻²)에서 도금/탈리 과전압이 **5 MPa 7.0 mV ↔ 25 MPa 4.5 mV**.
  → **`η = η(i, P)`** 이고, `i→0` 으로 `η` 를 지우는 처방은 **압력을 고정한 채로만**
  성립한다. [[assb-apparent-capacity-decomposition]] 의 3 항 분해가 그만큼 좁아진다.

### ⚠ 세 번째 실측 반례 (2026-09-16, Lee 2020) — **`LLI` 쪽에서도 라벨이 안 닫힌다**

- ★★★ **같은 논문 안에서 `LLI` 의 두 추정자가 10 배 어긋난다.**
  0.6 Ah 무음극 파우치: `[도표]` CE 중앙값 **99.89 %** (사이클 0–800),
  `[인쇄]` 용량유지율 **95 % @600 · 89 % @1000**.
  `[재현]` CE 결손을 영구 Li 손실로 읽으면 누적 **161 mAh g⁻¹**, 실측 손실은
  **16 mAh g⁻¹**, 양극 전체 재고는 **215**. 89 % 를 설명하려면 CE 가 **99.988 %** 여야 한다.
  ★ **대조군이 같은 논문 안에 있다**: 20 mAh 소형 셀은 `[도표]` CE **99.97 %** ↔
  유지율 92.5 %@300 (= `[재현]` **99.974 %/cycle**) 로 **맞는다.**
  그리고 **CE 축의 눈금이 다르다** (Fig. 6g 95–101 vs SI Fig. 13c **99.4–100.0**).
  `[해석]` **셀이 커질수록 CE 의 상대 정밀도가 나빠지고, 그 순간 CE 는 `LLI` 의
  추정자가 아니라 계측 바닥이 된다.** 논문은 두 셀을 **한 번도 비교하지 않고**
  CE 계측 정밀도를 밝히지 않는다. → [[anode-free-li-inventory-accounting]].
- ★★ **그리고 `η` 가 `LLI` 도 가린다.** `[재현]` 이 셀의 0.5 C 방전 용량은
  146 mAh g⁻¹, 0.2 C 는 215 → **`η(0.5C) ≈ 0.68`**. **양극 재고의 32 % 가 운전 창
  밖에 있다** → Li 를 잃어도 양극이 쓰는 SOC 창이 이동할 뿐이다.
  `[해석]` **겉보기 용량유지율은 `LLI` 의 하한이다.** 완충 여력 `[재현]` 69 mAh g⁻¹
  으로는 위 간극(161)을 **부분적으로만** 설명한다.
  → [[assb-apparent-capacity-decomposition]] 의 `η` 가 `LAM_PE` 뿐 아니라 **`LLI` 도**
  가린다는 것이 실측으로 들어왔다.
- ★ **열화의 "계단" 이 음극에서도 나온다.** `[도표]` Lee Fig. 2d (맨 SUS 대조군,
  20 mAh, 0.1C/0.33C, 60 °C): 사이클 10 까지 ≈100 % → 15 에 ≈80 → **20 에 ≈50** →
  27 에 ≈20 → 50 에 **≈6 %**. **4호(Shi)의 양극 급락과 모양이 같은데 전극이 다르다.**
  `[해석]` → **"급락 = 양극 접촉 손실" 이라는 귀속이 위험하다.** `θ(N)` 을 계단으로
  모형화할 때 **어느 전극인지는 곡선 모양으로 정해지지 않는다.**
- ★ **1000 사이클 V–Q 는 "끝이 잘리는" 열화다.** `[도표]` SI Fig. 16 (0.5C/0.5C,
  사이클 1/200/400/600/800/1000): 충전·방전 곡선이 **0 ~ ≈110 mAh g⁻¹ 구간에서 거의
  완전히 포개지고** 방전 말단의 **무릎 하나만** 왼쪽으로 간다 (종점 146 → 131).
  `[해석]` **곡선 모양에 `LLI` 의 수평 이동 서명이 나타나지 않는다** — 움직이는
  자유도가 사실상 하나(용량 축 절단)다. **이 자료에 OCV 적합을 걸면 가를 정보가
  거의 없다.** ⚠ 단 CC 곡선이지 OCV 가 아니고, 저항 증가로도 같은 모양이 난다
  (그리고 **논문은 사이클 중 EIS 를 하지 않는다**).

### ⚠ 네 번째 실측 반례 (2026-09-16, Spencer-Jolly 2023) — **음극 OCP 가 충·방전에서 다른 곡선이다**

- ★★★ **충전 경로에 존재하지 않는 상이 방전 경로에 있다.** `[인쇄]` "The structural
  changes on discharge are **not simply the reverse** of those on charge" 이고, 구체적
  으로 `[인쇄]` "LiAg undergoes a phase transition from the **CsCl to the UPb
  structure** … more stable … when it is Li deficient … this explains why this
  structural form **only appears on discharge**."
  → **열역학적 이력이다** (동역학이 아니다). 그리고 율이 `[인쇄]` **30 µA cm⁻² ≈ C/68**,
  **상온**이다. `[해석]` **`i → 0` 으로 지울 수 없다.**
  → **[[halfcell-ocp-shape-invariance]] 의 "모양 불변" 이 ASSB 무음극 중간층에서
  깨지는 두 번째 방식**이고, 6호가 준 첫 번째(사이클에 따라 Ag 가 이동)보다
  **더 아프다** — **한 사이클 안에서** 깨지기 때문이다.
  자세히는 [[ag-c-interlayer-lithium-phase-path]].
- ★★ **`η(i)` 가 음극에서 급격히 비선형이다.** `[재현]` **2 mA cm⁻² 에서 과전압이
  ≈−0.09 V 로 3 h 내내 평평** ↔ **4 mA cm⁻² 에서 −0.16 → −1.15 V 로 자라다 ≈0.72 h
  (≈2.9 mAh cm⁻²)에 단락**. **전류 2 배에 과전압 ≈12 배.**
  그리고 **율이 상 조성 자체를 바꾼다** (`[인쇄]` 고율에서 "clear evidence of **Ag
  persisting** throughout charging") → **음극 쪽 `Q_material` 도 율 의존**이다.
  `[해석]` → [[assb-apparent-capacity-decomposition]] 의 율 스윕 분리 시험에서
  **두 율을 어디에 놓느냐가 결과를 지배한다** — 문턱 근처에서 `η` 가 사실상 발산한다.
- ★ **부분 단락 서명이 이 계보에서 세 번째로 나왔다.** `[인쇄]` 캡션은 "a sudden drop
  in cell potential to **approximately 0 V**" 라고 적지만 `[도표]` 실제로는 −1.15 V
  에서 한 번 ≈−0.1 V 로 튀었다가 **−0.5 ~ −0.9 V 로 되돌아가 톱니처럼 진동**한다
  (충전 시작점보다도 더 음이다). 4호의 **충전 전압 비단조 진동** · 5호의 **계단식
  붕괴**와 같은 계열이다. `[해석]` **`assb` 전용 판별 feature 후보에 근거가 하나 더.**
- ★ **6호가 "시료 준비 탓" 으로 돌린 자리에 첫 반례.** `[인쇄]` SI Fig. S3 (4 mA cm⁻²
  파괴 시료 단면): "Li metal nucleation and Li-Ag alloying **at the interface between
  the composite layer and Li₆PS₅Cl solid electrolyte**" — `[도표]` S 원소지도에서
  **전해질이 밀려난 자리에 5–15 µm 둥근 Li 덩어리**가 박혀 있다.
  ⚠ **파괴 조건에서만**이다 — 정상 저율에서는 도금이 층 **위**(집전체 쪽)에서 일어난다
  (SI Fig. S4). `[해석]` **6호를 반박하지는 못하고, "아티팩트로 돌리기 전에 대조를
  해야 한다" 까지가 주장 가능하다.**
- ⚠ **그리고 이 논문은 이 카드의 본체에 입력이 0 이다** — 양극이 없다.
  Q1(접촉 손실 정량)은 **7/7 편에서 비어 있다.**

### ★ 다섯 번째 — 반례가 아니라 **문헌 쪽의 요구** (2026-09-22, Li et al. 2026 · ⚠ Mini Review)

> ⚠⚠ **이 절의 모든 수치는 재인용이다.** 8호는 *Frontiers in Chemistry* 의 **Mini
> Review** 이고 1 차 측정이 0 이다. 아래 `[인쇄]` 는 "리뷰가 이렇게 적었다" 는 뜻이지
> "그 수치가 맞다" 는 뜻이 아니다.

- ★★★ **이 카드의 질문이 BMS 요구 사항으로 인쇄됐다.** `[인쇄]` §6.1: "A solid-state
  BMS may therefore need pressure or force sensing, pressure-dependent impedance models,
  and **diagnostics capable of distinguishing contact loss from ordinary electrochemical
  aging**" (Biçer et al. 2025).
  → 3호(Liu 2024)가 **축퇴가 존재한다**는 것을 인쇄로 확인했다면, 8호는
  **그것을 가르는 진단이 필요하다**는 것을 인쇄로 요구한다.
  ⚠ **정량은 0** 이고, 그 요구가 매단 인용 1 편도 **종설**이다.
- ★★ **식별 가능성이 처음으로 실패 모드 목록에 올랐다.** `[인쇄]` Table 4 중기 목표
  "Pack-level active diagnostics" 의 major failure mode = "**Unidentifiable pulse
  response**"; Table 1 "ECMs … can **lose physical uniqueness**"; Table 3 DRT
  "**Ill-posed inversion needs regularization**".
  `[인쇄]` §2 가 가장 세게 적는다: "**Parameter identifiability, cell-to-cell
  variability, and uncertain aging mechanisms can make a detailed model appear more
  precise than the available measurements justify.**"
  → `[해석]` **`degradation-degeneracy` 의 논지가 문헌 문장으로 존재한다.**
  ⚠⚠ **그러나 이 리뷰도 재지 않는다** — 조건수·프로파일 가능도·근최적 폭·Fisher/CRB
  **전부 0**. 그리고 그 문장에 붙은 인용 넷은 **전부 모형/매개화 논문**이며,
  `[인쇄]` "poorly identifiable" 문장이 매단 인용은 **Si–C 음극 소재 종설**이다
  (8호 digest D2). → **Q4 는 8/8 편 0 이다.**
- ★★ **산업 압력 요구치가 우리 압력 창 전체보다 아래다.** `[인쇄]` "Xu et al. (2024)
  note industrial requirements **below approximately 1 MPa**".
  `[재현]` `MPa` 가 12 쪽에 **1 회**뿐이고 그 값이 1 이다. 우리가 읽어 온 것:
  제작 **490**(6호)·**400**(7호) · 개입 **300**(4호) · 상한 **75**(5호) ·
  운전 **2–5**(5·6·7호). → **전부 위에 있다.**
  `[해석]` ① [[assb-pressure-reapplication-separation-test]] 의 `P↑` 연산자는
  **산업 셀에 더더욱 못 쓴다** ② 거꾸로 **`θ_AM` 의 시간 변화가 산업 조건에서 더 클
  것**이라는 방향이 생긴다. ⚠ **재인용이다 — Xu 2024 를 받아야 한다.**
- ★★ **"보정된 불확실성 0 / 8" — 세 번째 비어 있음 원장.** `[재현]` 8호 Table 2 의
  `Uncertainty output` 열을 세면 **보정된(calibrated) 불확실성을 보고한 편이 0 / 8**
  이다 (신뢰구간 1 · "가능하나 안전 보정 미시연" 1 · "주 산출 아님" 2 · "보고 없음" 4).
  `Validation level` 은 **7 / 8 이 `Cell`**.
  → 액체셀 **17/17 유일성 0** · `assb` **7/7 오차막대 0** 에 이어
  **BMS/SOH 추정 8/8 보정 불확실성 0** 이 붙는다. **세 계보가 같은 방향으로 비어 있다.**
  ⚠ 셋째 줄은 **리뷰가 고른 8 편을 리뷰의 분류대로 우리가 센 것**이고 원전 대조는 0 이다.
- ⚠ **재인용이 원전을 넘어서는 실측 사례가 잡혔다 — 우리 위키로 검증됨.**
  8호가 `[인쇄]` Table 3 에 "SOH RMSE **≤0.873 %** in Su et al. (2024)" 라고 적는다.
  우리는 그 원전의 digest 를 갖고 있다 (`raw/papers/su2024_drt-soh-health-features.md`):
  0.873 % 는 **5 셀 평균**이고 **cell5 는 1.607 %**(상한이 아니다), 게다가 같은 논문의
  **원시 EIS(0.573 %)·8-D(0.672 %) 가 제안 feature 를 모든 지표에서 이긴다.**
  → `[해석]` **리뷰가 원전의 과장을 `≤` 부등호로 한 단계 더 굳혔다.**
  **이 카드의 규율에 직결된다: 종설의 숫자를 이 위키의 근거로 삼지 않는다.**
- ⚠ **8호가 우리 축에 주는 것은 여기까지다.** ASSB 는 12 쪽 중 **한 문단(§6.1)**
  이고, `θ`·퍼콜레이션·면적분율·OCV 곡선·Li-In·dead Li 가 **전부 0** 이다.
  그리고 이 리뷰는 **열화 모드라는 개념을 한 번도 쓰지 않는다**
  (`LLI`·`LAM`·`degradation mode` 전수 0 회) — **Birkl 2017 을 인용해 놓고도**
  (8호 digest D8).

### ★★★ 여섯 번째 — **For 에 붙는 야생 실측** (2026-09-22, Huo et al. 2025)

앞의 다섯은 전부 "가르는 관측이 없다" 는 **부재**의 증거였다. 9호는 다르다 —
**가르지 않은 절차가 실제로 돌아가서 지분을 인쇄한 첫 사례**이고, 그 절차의
축퇴가 **같은 논문의 표 안에 세 개의 지문으로 남아 있다**.

| # | 지문 | 크기 | 논문이 부르는 이름 |
|---|---|---|---|
| 1 | `R_SEI` 분해가 **동일 화학·공정·프로토콜 두 셀**에서 부호까지 어긋남 (합계는 +23 %/+18 % 로 같은 방향) | **+37.1 % vs −79.7 %** | `[인쇄]` "**unexpected**" → "장비 정확도 · **적합 과정이 넣은 오차** · 열평형" |
| 2 | `A^p_eff · ε_p / R_s` **곱 축퇴** — 자기 SEM 의 입자 반경을 쓰면 `A_eff` 가 9 배 움직인다 | `A_eff ∈ [0.055, 0.494]` | 이름 없음. `[인쇄]` "retaining the **actual physical significance** of the parameters" |
| 3 | `k_LAM`(노화 속도 계수)이 **셀마다 다시 적합**되고 그 산포가 보고된 적합 오차보다 두 자릿수 크다 | **2.15 배 (≈115 %) vs "1 % 이내"** | `[인쇄]` "**slightly different**" |

★★★ **그리고 명제의 부정이 문자로 인쇄되어 있다** (`[인쇄]` 전문):

> "The values of certain parameters, such as `cp0`, `cn0`, `kp`, `kn`, `Dp` and
> `Dp_se`, **exhibit significant variations** … **To avoid potential
> misinterpretation, these values are not disclosed in this paper.** While such
> variations are expected …, **the robustness of the overall model and its
> predictive capabilities remain unaffected, as confirmed by our experimental
> results.**"

`[해석]` 세 단계다 — ① 적합 파라미터의 셀 간 산포를 **관측했다** ② 그 산포를
지면에서 **제거했다** ③ 제거의 정당화가 **적합도다**. 이것이
[[fitting-degeneracy]] 와 `degradation-degeneracy/` 가 측정으로 반박한 명제이고,
**3번 지문이 특히 인용 가치가 크다: 보고된 "정확도" 가 그 정확도를 만드는
파라미터의 셀 간 산포보다 두 자릿수 작다.**

⚠ **공정하게**: 두 셀은 **다른 노화 수준**(A 77 % · B 90 %)에서 측정됐으므로 합계
변화율의 유사성은 강하게 주장하지 않는다. **부호가 반대인 것만이 모호하지 않다.**
그리고 모집단이 **2** 뿐이라 산포의 폭 자체를 못 잰다.

★ 구조 유도는 [[assb-lampe-contact-product-degeneracy]] 에 있다.

### ★★★ 일곱 번째 — **방법론 쪽의 정식 근거** (2026-09-22, Vadhva et al. 2021 · ⚠ Review, 1차 측정 0)

9호가 **축퇴의 지문을 자기 표 안에 남기고 다르게 불렀다**면, 10호는 **그 지문이
지문이라는 것을 분야의 방법론 리뷰가 이미 인쇄해 두었다**는 것을 보인다.
⚠ **이것은 재인용 수치가 아니라 저자들의 1차 방법론적 주장이다** — 8호에서 세운
"리뷰 수치는 근거가 아니다" 규율의 **바깥에 있는 종류**다 (digest §12 참조).

**(가) 9호 §5.1 "하나의 원호에서 두 시상수" 에 대한 판정 — 다섯 문장** (전부 `[인쇄]`):

| # | 문장 | 9호에 대한 함의 |
|---|---|---|
| ① | "**As no solution to an EIS spectrum is unique**" | `R_SEI` 점추정에 근거가 없다 |
| ② | "**the inclusion of more elements will tend to improve the fit** of the equivalent circuit model" | **적합이 잘 맞는 것은 모델 선택의 증거가 아니다** |
| ③ | "using the **simplest ECM with the fewest elements possible** and ensuring that **physical and chemical meaning is maintained**" | 원호 1 개에 RQ 2 개 + W 는 이 원칙의 반대쪽 |
| ④ | "it is often challenging to **decipher how many time constants are present** in a given dataset and their assignment can be **highly subjective**" | "두 시상수" 라는 전제 자체가 주관이다 |
| ⑤ | "Physical features in the cell **may not be visible in the EIS spectra**" | 반대 방향(있는데 안 보임)도 동시에 열려 있다 |

`[재현]` 9호의 회로(`R_b` + RQ + RQ + `W`)는 자유 파라미터가 **1 + 3 + 3 + 2 = 9 개**
다(CPE 하나가 R·Q·α 셋). **원호 하나에 9 개를 맞춘 것이다** — 9호는 이 개수를 세지
않는다.

**(나) ★ 처방 — 그리고 9호는 넷 중 하나도 쓰지 않았다** (9호에 `Kramers`·`Kronig`·
`DRT`·`symmetric cell`·`AIC` **전수 0 회**):

| 처방 | 원전 사례 | 무엇을 하나 |
|---|---|---|
| **K–K / Lin-KK 사전 검증** | ref. 41–43 (Boukamp; **Schönleber Lin-KK**, KIT 2015 — 소프트웨어) | 적합 **전에** 데이터가 선형·정상·인과인지 판정 |
| **DRT 로 시상수 개수를 먼저 정한다** | ref. 62 Pang 2019 — `[인쇄]` "**unambiguously identified three semicircles**" | 개수를 **데이터가** 정하게 한다 |
| **조건을 바꿔 시상수를 벌린 뒤 구속으로 되가져온다** | ★ ref. 82 Bron (−130 °C 에서 `R_gb` 동정 → 실온 추적) · ref. 28 Krauskopf (400 MPa 로 `R_int` 제거 → `GB` 노출) | **여기(excitation)를 늘려 축퇴를 깬다** |
| **상보 대칭셀 쌍으로 전극을 귀속** | ref. 70 Iriyama · ref. 126 Ohta · ★ ref. 161 He (LFP 대칭셀 + Li 대칭셀 두 개로 **어느 계면이 변했는지 확정**) | 주파수 추론 대신 **직접 분리** |
| **AIC 로 회로를 순위 매긴다** | ref. 51,52 (Akaike 1974; **Ingdal 2019**) | 과적합을 **정보량 기준**으로 벌한다. ⚠ **실험 적용 0** |

**(다) ★★★ 새 명제 — "분해 가능한 RC 의 개수는 실험 조건의 함수다"**
리뷰가 다섯 곳에서 따로 서술하고 **한 명제로 모으지는 않는다. 우리가 모은다**:

| 사례 | 조건 | 개수 변화 |
|---|---|---|
| `[도표]` Fig. 8 (Bron, 황화물 5 종) | 동일 −130 °C | **5 중 3 만** `R_gb` 가 분해된다 — 입계는 **5 개 모두에 존재**한다 |
| `[도표]` Fig. 7 아래 인셋 (LGPS) | 27 °C | **원호 0 개** — 절편뿐인데 σ = 12 mS cm⁻¹ 가 거기서 나온다 |
| `[도표]` Fig. 11a (Krauskopf, LLZO) | 1 → 400 MPa | `R_int` 가 사라지자 **`GB` 원호가 나타난다** |
| `[인쇄]` Aziz (PEO) | 60 °C 초과 | **상경계 임피던스가 완전히 소멸** |
| ★ `[인쇄]` Larfaillou (LiPON) | **60 h / 60 °C 보관 노화** | **RQ 3 개 → 4 개**, 새 RQ 의 귀속은 `[인쇄]` "Li\|LiPON interface **and/or** in the LCO bulk" |

`[해석]` **마지막 줄이 우리 축에 가장 무겁다**: ① **모델 차수가 상태변수다** — 고정
회로로 노화 시계열을 적합하면(9호가 한 일) 모델이 틀린 구간이 생긴다 ②
**새로 생긴 저항이 음극 계면인지 양극 벌크인지 가르지 못한 채 출판된다.**

**(라) ★★ EIS 자체가 접촉 손실과 계면상 성장을 한 저항에 합친다** — 이 카드의 핵심:

> `[인쇄]` (Fig. 9 본문, In\|LGPS\|LCO): 충전 중 중주파 양극 계면 저항의 증가는
> "**loss of interfacial contact in the composite cathode due to volumetric
> expansion** **and** the **formation of a decomposition layer on exposed LCO**"
> 때문이다.

`[해석]` **두 기구가 하나의 `R_MF` 에 귀속되고, 가르는 관측은 이 논문에도 리뷰에도
없다.** [[assb-lampe-contact-product-degeneracy]] 가 **방전 V–Q 영역**에서 보인 곱
축퇴와 **같은 구조가 주파수 영역에서 반복된다** — 그리고 **두 축퇴는 독립이라 곱해진다**
(그 페이지의 처방표에서 "다중 SOC EIS" 에 ⚠ 가 붙는 이유).

**(마) ⚠ 관측의 자기 반증 사례 — 이 계보 최초**
> `[인쇄]` Itagaki 는 Li 기준극으로 in-situ EIS 를 분해해 **흑연 음극의 저주파
> 인덕턴스**를 추적했다. "**However**, a study using pulsed charge/discharge
> conditions on a similar cell set-up, concluded that this inductance feature was
> **measurement artefact, due to the violation of the QSS condition** at low
> frequencies."

`[해석]` **3 전극 · 기준극 · 전극 분해를 다 갖춘 측정에서도 저주파 특징이 물리가
아니라 아티팩트였다.** 우리 위키에 이만큼 직접적인 "관측에 붙은 물리 이름이 취소된"
사례가 없었다. **그리고 같은 논문 Table 1 은 여전히 저주파 인덕턴스를
`[인쇄]` "degradation processes" 로 적는다** (digest D6).

**(바) ⚠ 문헌의 EIS 수치가 전제 위반 상태로 쌓여 있다**
`[인쇄]` §2.1 기준은 섭동 **<50 mV**. 그런데 LGPS 를 발견한 *Nature Materials* 논문
(Kamaya 2011)에 대해 이 리뷰가 적는다 — `[인쇄]` "these EIS measurements were taken
with **large perturbation voltages of 100 to 500 mV, which may enter the non-linear
regime** and data were **not explicitly checked using K–K tests**."
`[해석]` **기준의 2–10 배**다. 분야 정초 수치가 선형성 검증 없이 인용되고 있다.

**(사) 재현성의 첫 숫자** — `[인쇄]` 5 화합물 기관 간 라운드로빈: 상대 **중앙값**
오차가 `>1 mS cm⁻¹` 재료에서 **22 %**, `<1 mS cm⁻¹` 에서 **~10 %**. 원인으로
`[인쇄]` "the **fitting of limited EIS data** and microstructural relaxation".
★ **재료가 좋을수록 산포가 커진다** — 시상수가 주파수창 밖으로 밀려 적합할 데이터가
줄기 때문이다. ⚠⚠ **재인용이고 인용 번호가 틀렸다**(본문 ref. [85] ↔ 실제 ref. [191]
Ohno *ACS Energy Lett.* 2020) — 원전을 받기 전까지 **방향만** 쓴다.
⚠⚠⚠ 그리고 이것은 **단일 파라미터 `σ_ion`** 의 산포다. `[해석]` **다중 RC 적합
파라미터의 산포는 이것보다 클 수밖에 없다** — 리뷰는 그 말을 하지 않는다.

### ★★★★ 여덟 번째 — **For 에 붙는 야생 실측, 그리고 10호의 경고가 데이터로 나타난 자리** (2026-09-22, Yu et al. 2024 · Schaeffler + Ohio State)

`raw/papers/yu2024_drt-time-resolved-aging-sulfide-assb-fullcell.md`
(*J. Power Sources* **597** (2024) 234116; 본문 8 쪽 + **SI `.docx`** 7,607 자 +
그림 S1–S5, 둘 다 sha256 봉인). **수치의 정본은 원문이고 아래는 사본이다.**

**이 편은 10호(Vadhva)가 처방한 DRT 를 실제로 돌린 첫 `assb` 논문이다.** 그리고
10호가 경고한 것들이 **데이터로 나타난다** — 논문이 알아채지 못한 채로.

**(가) ★★★ "분해 가능한 시상수 개수" 가 상태·조작·장비의 함수라는 것을 1 차
데이터로 네 번 보인다.** 10호는 이것을 **Larfaillou 2016 재인용**(신품 3 RQ →
노화 4 RQ)으로만 전했다. 11호에서는 우리가 그림을 직접 열어 셌다:

| 자리 | `[도표]` 무엇이 변하는가 |
|---|---|
| Fig. 2(a) 완전지 | 국소 극대 **2–3 (4 cy) → 5 (48 cy)**. P3 는 4 cy 에 **어깨**였다가 48 cy 에 **봉우리**가 된다 |
| Fig. 3(c) micro-SE 반쪽 | 중주파 극대 **1 개 (cy 3) → 2 개 (cy 29~)**. 그리고 cy 3 의 극대는 ≈9 × 10³ Hz 인데 이후 P2 는 ≈1.8 × 10⁴ Hz — **봉우리가 쪼개지며 자리를 옮긴다** |
| Fig. 6(c) graphite 반쪽 | **P4 가 없던 자리(평탄 ≈1.5)에 생긴다** (cy 133 에 ≈10 Hz, 5.5) |
| Fig. 7(d) 완전지 재가압 | **4 → 3** — 재가압 후 P3 의 독립 극대가 **사라진다** |

`[해석]` **노화가 개수를 올리고 개입이 개수를 내린다 ⇒ 모델 차수는 상태변수다.**
⚠ 그리고 **논문은 세 번 다 "봉우리가 커졌다" 고 적고 "봉우리가 생겼다" 고 적지
않는다** (`[인쇄]` "growth of P3 … peak intensities" · "P4 … exhibits a **gradual
increase** in peak intensity"). → **고정 회로로 노화 시계열을 적합하는 관행
(9호가 한 일) 전체에 대한 실측 반례다.**

**(나) ★★★★ 축퇴의 크기를 잴 재료가 SI 에 있고, 그 크기가 본문 효과와 같다.**
`[도표]` **Fig. S3** — 같은 셀(로 보이는 것)을 **배선만 바꿔** 잰 두 DRT:

| 봉우리 | Arbin+Gamry | Gamry 직결 | `[재현]` Δ |
|---|---:|---:|---:|
| ≈3.5 × 10⁵ Hz | 117 | 105 | −10 % |
| ★ ≈2 × 10⁴ Hz | **39 (분해된 어깨)** | **없음** | **특징 1 개 차이** |
| ≈3 × 10³ Hz (= P3 자리) | 78 | 66 | **−15 %** |
| ★ ≈3 × 10⁻² Hz | 45 | 76 | ★★ **+69 %** |

**본문이 물리로 해석한 변화**: 재가압이 P3 **−16 %** · P1 **−11 %** · P2 **−10 %** ·
P4 **−25 %**. → ★★★★★ **본문의 모든 개입 효과가 SI 의 배선 인공물 폭 안에 있다.**
논문은 이 비교를 하지 않는다 — `uncertaint*`·`error bar`·`uniqu*`·`regulariz*`
**전수 0 회**라서 **할 어휘가 없다**.
⚠ **공정하게**: 배선이 바뀌면 인덕턴스·접촉저항이 실제로 변하므로 일부는 진짜
물리이고, 두 측정의 최고 주파수가 **1 MHz ↔ 2 MHz** 로 다르며, "같은 셀" 이라는
명시가 SI 에 없다. **그러므로 69 % 는 상한이다.** 그러나 **상한조차 본문 효과보다
크다**는 것이 요점이다.

**(다) ★★★★ 이름표의 위치 불확정성이 이름표 간격보다 크다.**
`[재현]` P3 의 보고 위치: **~500 Hz**(§3.1 완전지) · **10³–10² Hz**(§3.1 NMC 반쪽) ·
**10⁴–10³ Hz**(§3.2) · **~1 kHz**(§3.3) · **~10³ Hz**(Table 1) · `[도표]` **0.9 kHz**
(Fig. 7d) · **1.3 kHz**(Fig. 4d) · **≈2.8 kHz**(Fig. 3c) ⇒ **500 Hz – 10 kHz =
1.3 자릿수**. 그런데 **P2–P3 간격은 0.8 자릿수** (`log₁₀(6000/900) = 0.82`).
★ `[인쇄]` Table 1 은 **P2 = 화학적 접촉(SEI/CEI)**, **P3 = 기계적 접촉**이다.
→ `[해석]` **화학 열화와 기계 열화의 분리가 바로 이 자리에서 무너진다.**

**(라) ★★★ 논문 자신의 결론 지도가 축퇴를 그림으로 인쇄한다.** `[도표]` **Fig. 8**:
- **P2 와 P3 에 `Cathode`(빨강)와 `Anode`(파랑)가 둘 다 찍혀 있다** ⇒
  **"P3 가 자랐다" 가 어느 전극인지 말해 주지 않는다.**
- **P4(음극 CT, 넓음)와 P5(양극 CT, 좁음)가 ≈10 Hz 에서 겹쳐 그려져 있다** ⇒
  **두 전극의 전하이동이 주파수로 분리되지 않는다.**
- **(P1′) 이 회색 점선이다** — 측정 대역(2 MHz) 위에 있어 **못 본 봉우리를 지도에
  그려 넣었다**. 그리고 `P1′` 는 본문·Table 1 에 **없다**.

**(마) ★★★ 압력 연산자가 직교하지 않는다 — 4호에 붙는 반례.**
`[도표]` Fig. 7(d): 재가압(>500 MPa)이 **P4(graphite 전하이동)를 −25 %** 줄인다.
Fig. 4(d): **P1(SE 입계/케이블) −11 %**, **P2(화학 접촉) −10 %**.
`[해석]` **기계적 조작이 "화학" 항과 "전하이동" 항도 같이 줄인다** ⇒
[[assb-pressure-reapplication-separation-test]] 의 `Q_apparent = θ_AM(P,N)·η(i)·
Q_material(N)` 에서 **`P` 가 `θ_AM` 에만 들어간다는 가정에 반례가 붙는다.**
⚠ 그리고 **회복 크기가 4호의 1/12** (`[재현]` +4.91 % vs `[재현]` +60.5 %p)인데
`[인쇄]` "agree with previous report by **Ceder et al. [21]**" 라고만 쓰고
**크기를 비교하지 않는다** — ref. [21] 이 바로 우리 **4호(Shi 2020)** 다.

**(바) ★★ 순환: DRT 가 ECM 을 입력으로 받는다.**
`[인쇄]` Fig. 2 캡션 — "The DRT peaks were computed **based on the simulated
Nyquist curves (green solid-line)** after subtracting the low-frequency data."
10호의 정답 절차(ref. 62 Pang 2019)는 **K–K → DRT 로 개수 결정 → 그 개수만큼
ECM** 인데, 11호는 **ECM 적합 → 그 곡선으로 DRT** 다. `[해석]` **DRT 가 분해할 수
있는 개수가 적합 모델의 차수에 의해 위에서 막힌다.**
⚠ SI 는 다르게 쓴다 — `[인쇄]` "the fitted model is subtracted from the
**measurement data**". **두 절차가 같은 논문 안에서 충돌한다** (digest D1).

**(사) 그리고 10호의 λ 공백(G4)은 메워지지 않았다 — 더 깊어졌다.**
`regulariz*`·`λ`·`L-curve`·`GCV`·`cross-valid*`·RBF shape factor **본문 + SI 전수
0 회**. 유일한 방법 서술이 `[인쇄]` "MATLAB-based DRT calculation code developed
by **T.H. Wan et al. [16]**" 한 줄이고, SI 는 DRT 를 **보통의 적합 문제**로
소개하며 `[인쇄]` **"The well-fitted `Z_DRT` can represent the actual physics in
the system"** 이라고 쓴다 — 10호의 `[인쇄]` "mathematically **ill-posed**,
requiring regularization" 의 **정반대 진술**이다.
`[재현]` 10호 처방 14 항목 채점: **✅ 2 · ⚠ 5 · ❌ 7** (digest §18).

### ★★ 열한 번째 — **For 에 붙는 야생 실측 + "관측 추가" 의 첫 실험 표본** (2026-09-22, Oh et al. 2025 · 실험, Hot Paper)

`raw/papers/oh2025_maxwell-protocol-nondestructive-assb-health.md` (*Angew. Chem. Int. Ed.* 64,
e202514910; 서울대 + HMG-SNU JBRC). 컴파일: [[assb-maxwell-ocv-derivative-channels]].

**이 편이 이 카드에 하는 일은 셋이다 — 실측 하나, 관측 축 하나, 경고 하나.**

1. ★★★ **실측 (For)**: `[인쇄]` 50 사이클 뒤 XRM 공극률 **4.5 → 9.8 %**(10 MPa) ↔ **4.4 →
   5.3 %**(20 MPa) 인데 용량 유지율은 **86.0 % ↔ 84.0 %** — void 가 2 배인 셀이 **더 높다**.
   논문은 "similar … internal voids may not directly affect the early-cycle performance" 로
   지나간다. `[해석]` 이 카드의 언어로: **접촉 손실이 이 창에서는 `Q_apparent` 에 전혀
   안 들어간다.** OCV 적합은 `LAM_PE ≈ 0` 을 (정확히) 보고하고 **void 2 배를 놓친다** —
   "OCV 만으로는 못 본다" 의 가장 깨끗한 형태(오독이 아니라 **무감**). 1호의 `θ_AM ≈ 1
   above p_c` 와 정합하고, 4호(면적 10.4 % ↔ 60 %p)의 반대쪽 끝이다 — **사상이 문턱형**이라는
   두 점.
2. ★★ **관측 축 (관측 추가)**: 이 편은 `E(x)` 를 적합하지 않고 같은 상태함수의 두 편미분
   `−F(∂E/∂T)_P = ΔS` · `F(∂E/∂P)_T = ΔV` 를 잰다 — [[constrained-crb-identifiability]] 의
   "관측 추가" 칸에 들어가는 **첫 ASSB 실험 표본**이다. `[해석]` 우리 쌍에 대한 새 행의
   부호: 균일 `LAM_PE`·완전 고립 접촉 손실은 둘 다 **아핀**이라 ΔS(x) 모양 불변(**새 행 = 0**);
   void 는 `dE/dP` 를 움직인다(**새 행 ≠ 0**, 이 편의 주장) ⇒ **분리 후보 행은 volumetry**이고
   **엔트로피메트리는 아니다** — 이 편은 반대로 ΔS 를 주 진단으로 둔다. ⚠ 실측 0, 우리 명제.
3. ⚠ **경고 (Against 쪽 단서)**: `[인쇄]` ΔS 는 "contact loss **as well as** … interfacial
   resistance" 를 한 신호로 받는다 — **이 편 스스로 우리 쌍을 합친 채널이라 정의한다.**
   그리고 volumetry 의 `dE/dP` 는 `[재현]` **압력 구간에 2 배 의존**(0.44 ↔ 0.23 mV/MPa,
   신품끼리)하고 **전·후 측정의 SOC 가 171 mV 다르다**(D7) — 관측 추가의 "새 행" 이
   상수가 아니라 `(P, x)` 의 함수라는 뜻. 상수 `ΔV` 로 넣으면 모델 오차가 된다.

**Q4 는 0/14 이고 성질이 일곱 번째로 바뀐다** — 역문제가 없어서 조건수가 정의될 자리가
없고, 대신 **귀속의 유일성**(ΔS 변화가 비균질인가 재료 변화인가; `[재현]` SOC 축 적분이
≈ −3.5 → ≈ +1.5 로 부호가 바뀌는 것은 비균질만으로는 안 나온다 — G8)을 아무도 묻지 않는다.

### ★ 열두 번째 — **근거가 아니라 "1호가 야생에서 어떻게 읽히는가" 의 첫 실측** (2026-09-22, Rahman & Lu 2024 · ⚠⚠ 학회 회의록 6 쪽, 1차 측정 0, **재인용 수치도 0**)

`raw/papers/rahman2024_sbms-rul-solid-state-batteries.md`
(*Proc. IISE Annual Conf. & Expo 2024*, Abstract ID 8085; 6 쪽, SI 없음, sha256 봉인).

⚠ **이 절은 이 편의 주장을 근거로 쓰지 않는다.** 쓸 수 있는 주장이 없다 —
`[재현]` 본문 2,331 단어에서 인용 괄호·절 번호를 빼면 남는 숫자가 **`2024`(회의 연도) ·
`8085`(Abstract ID) · `19`(COVID-19) · `2021`·`2026`(연구비 기간)** 뿐이다.
`capacity`·`experiment*`·`measur*`·`contact`·`pressure` 가 **전부 0 회**다.
이 절이 쓰는 것은 **인용 관계 두 개**다.

**(가) ★★★ `assb` 1호가 인용되는 방식 — 어긋난다.**
이 편 ref **[5]** = 우리 1호 (Bielefeld, Weber, Janek, *JPCC* 123, 1626−1634).
인용된 **유일한 자리**가 서론의 이 문장이다:
`[인쇄]` "These technologies [ANN, Adaptive Fuzzy Logic] … mainly address key challenges
such as **load balancing, state-of-charge estimation, and overall battery health
monitoring [5, 6]**."
우리 1호 digest 가 전수 계수로 기록한 원전의 상태: `[인쇄]` **"셀 실험 0 개이고,
사이클링·전압·용량이 없다"** · Q5 행 `voltage` **1 회 — 그마저 참고문헌 제목** ·
**"모델에 음극이 없다 — 복합양극만"** · Q8 행 **"OCP 곡선이 없다. 전압축 자체가 없다."**
그 논문이 실제로 계산하는 것은 **이용률 `θ = V_c/V_ν`(식 6)** 와 **활성 계면적**이다.
→ **판정: 어긋난다.** 그리고 서지도 틀렸다 — **연도 2018(원전 2019)**, 저자 "W. Dominik A".
`[해석]` **번호 실수로 보기 어렵다**: 같은 저자의 **다른 논문 [28]**(2020 바인더 편)이
§4.1 에 따로 있고 거기서는 내용이 대체로 맞게 요약된다. 서론의 `[5, 6]` 은 "SSB 문헌임"
만으로 고른 **장식 인용**이다([6] 도 argyrodite 합성 논문).
★★ **이 카드에 주는 함의**: 1호 digest §12.4 에서 `Q_apparent = θ_AM · Q_material` 을
**우리 해석**이라고 못 박고 "논문은 용량도 전압도 주지 않는다" 고 적은 것이
**보수적이지 않았다** — 바깥에서는 그 다리가 없는 채로 **BMS 문장에 직결된다.**

**(나) ★★ `assb` 12호가 인용되는 방식 — 어긋나지 않지만 결론이 버려진다.**
이 편 ref **[21]** = 우리 12호 (Sadegh Kouhestani et al., *Energies* 15, 6599).
쓰인 자리는 §3.1 끝의 **교과서적 ANN 정의**(세 층 · FNN 비순환 vs RNN 순환) 한 문장이다.
⚠ 우리 12호 digest 가 그 수준을 채록하지 않았으므로 **어긋남 미확인(정합 추정)**.
★ 문제는 다른 데 있다 — **12호의 자기 결론이 전달되지 않는다**:
`[재현]`(12호 digest, Table 1 해체) **"SSB 의 실측 열화 데이터로 SOH/RUL 을 추정한 항목:
0 / 28"** · `[인쇄]`(12호 §4) "most PHM techniques are based on **simulation** results and
not experimental" · `[인쇄]`(12호 결론) "very few studies … **lack of accurate data**".
15호는 이 논문을 인용하면서 **그 위에 "SBMS 로 SSB 의 RUL 을 늘린다" 를 얹는다.**
`[해석]` **12호(2022)가 감사로 적어 둔 공백을, 15호(2024)가 12호를 인용하면서
그대로 재생산한다.** 12호 항목이 "2022 → 2026 사이 PHM 문헌은 identifiability 라는
**이름**을 얻었고 여전히 재지 않았다" 로 끝났는데, **15호는 그 사이(2024)에서 이름조차
못 얻은 표본**이다 (`identifiab*` **0 회**).

**(다) 이 편이 아는 유일한 SSB-ML 라벨 = `simulated`.**
`[인쇄]` ref [22] (Asheri 2023) — "a **data-driven multiscale simulation framework**
(leveraging artificial neural networks) to predict and analyze the degradation in
solid-state batteries, focusing on **interface damage** and its impact on cell
performance." `[재현]` 이 편 참고문헌 **33 편 중 SSB 15 · 액체 LIB/EV 14 · 배터리가
아닌 것 2**([27] Cu(II) 흡착, [31] COVID-19) — **그리고 SSB 집합과 ML/BMS 집합이
교차하지 않는다**([21] 종설·[22] 시뮬 제외). **"SSB 데이터에 ML 을 돌려 RUL 을 낸"
인용은 0 편이다.**

**(라) ⚠ 인용 구조 자체의 결함 — 결론의 근거가 도메인 밖이다.**
`[인쇄]` §5 "Significant progress has been made in integrating ANN and adaptive fuzzy
logic **in SBMS**, **as evidenced by** studies by Y. J. Wongt et al. **[27]**."
ref [27] = Wong et al., *Environ. Monit. Assess.* 192 (2020) — "**Cu(II) adsorption from
aqueous solution using biochar derived from rambutan peel**". **배터리 논문이 아니다.**
(§4.2 의 [31] COVID 논문은 적어도 `[인쇄]` "**could be insightful**" 로 유추임을 밝힌다 —
이 편에서 인용 위생이 지켜진 유일한 자리다.)

**이 절이 For / Against 어느 쪽인가**: **어느 쪽도 아니다.** 이 편은 근거를 주지 않는다.
이 절이 고정하는 것은 둘이다 — ① **우리 1호의 결과가 인용 체인을 타고 나갈 때
어디서 끊어지는가**(전압·용량으로 번역되는 층이 통째로 건너뛰어진다) ②
**분류 체계 세 번째 표본 "어휘 미도입"** (12호 병합 · 13호 미배정 · 15호 미도입;
셋 다 종합 층위 문헌이고, 1차 측정이 있는 편은 전부 접촉 축을 갖는다).

### ★★★ 열세 번째 — **For 에 붙는 가장 직접적인 실측 구조** (2026-09-22, Ramanayagam et al. 2026 · 실험, 3전극)

`raw/papers/ramanayagam2026_stack-pressure-three-electrode-assb-impedance.md`.
앞선 열두 항목이 "**OCV 로는 못 가른다**" 를 **모델의 구조**(1·2·3·9호)나 **관측의 부재**
(4–7호)나 **종합 층위의 침묵**(8·10·12·13·15호)에서 끌어왔다면, **16호는 처음으로
"가르지 못하는 순간" 자체를 지면에서 보여 준다.**

**For 에 들어가는 이유 — 세 문장으로**:
1. 논문이 **접촉 면적이라는 양에 이름을 붙이고**(식 4), **값을 완전 접촉으로 고정**하고,
   **압력이 접촉을 개선했다고 말로 결론**내면서, **숫자는 전부 `j₀`(동역학)에 넣는다.**
2. 그 결과 **같은 데이터가 `j₀` 증가(1.8 배)와 감소(0.60 배)를 둘 다 허용한다**
   (배정에 따라 — 위 §16호 항목 2).
3. **논문은 두 배정 중 하나를 고른 적이 없다.** 고를 관측이 그 지면에 없기 때문이다.

★ `[해석]` **이것이 우리 물음의 EIS 판이다.** 우리 카드는 "OCV 적합이 `LAM_PE` 와 접촉 손실을
가르는가" 를 묻는데, 16호는 **EIS + TLM 도 같은 자리에서 갈라지지 않는다**는 것을 보인다 —
그리고 **EIS 는 OCV 가 못 보는 것을 본다고 여겨지던 채널**이다. 즉 **"관측을 늘리면 갈린다"
의 가장 유력한 후보 하나가, 늘린 뒤에도 같은 곱 위에 서 있다.**
⚠ **단서**: 16호의 축퇴는 **신품 셀의 압력 효과**에 대한 것이지 **열화 지분**에 대한 것이 아니다.
이 편에는 열화가 없다(`LAM`·`LLI` 0 회). **구조가 같다는 것이지 결과를 옮긴 것이 아니다.**

★★ **그리고 이 편은 Against 쪽에도 재료를 준다** — 아래 §"Against" 마지막 항목
(`R_CT·C_dl` 채널). **같은 논문이 축퇴를 밟고, 축퇴를 깰 두 숫자를 인쇄해 놓고 쓰지 않는다.**

### Against / 단서 — "독립 관측이 존재할 수 있다" 쪽

- ★★★ **`R_CT · C_dl` 채널 — 접촉 면적이 소거되는 조합** (2026-09-22, 16호에서 유도).
  계면의 실제 접촉 분율을 `θ` 라 하면, 가정 면적으로 정규화한 측정값은
  `R_CT^meas = R_CT^true/θ` 이고 `C^meas = θ·C^true` 이므로 **곱 `R_CT·C` 에서 `θ` 가 사라진다.**
  ⇒ **`R_CT·C` = 접촉-무관 고유 시상수(동역학), `C` 단독 = 접촉 면적 비례(기하).**
  **둘을 같이 보고하면 `θ` 와 `j₀` 가 갈린다.**
  ★ 16호는 **두 값을 다 갖고 있으면서**(Table 2 의 `R_CT`·`Q_DL`) **그 조합을 만들지 않는다.**
  `[재현]` 만들어 보면 두 압력에서 `R_CT·Q` 가 **1.7 배**(유효용량 변환 시 3.1 배) 달라서
  **순수 면적 효과만으로는 설명되지 않는다** — 즉 이 채널은 실제로 **정보를 가지고 있다.**
  ⚠ 단서: CPE 지수 `β` 가 다르면 변환이 모형 의존적이다(Brug 등). **우리가 아직 재지 않았다** —
  여기 적는 것은 **설계**다. → [[assb-lampe-contact-product-degeneracy]] §처방표.
- **ex situ XRD 의 inactive AM 분율** = 원리적으로 `1 − θ_AM` 의 **measured 라벨**
  (Strauss et al., ACS Energy Lett. 2018, 3, 992−996; Bielefeld 2019 ref 13).
  액체셀에서 우리를 막았던 "measured 라벨 없음" 이 여기서는 **존재할 수 있다.**
  ⚠ 단 Bielefeld 는 그 대조를 **정성적으로만** 했고 스스로 무효화했다 —
  `[인쇄]` "the total packing density of AM used by Strauss et al. is not known,
  **as the porosity was not measured**".
- ★ **율(rate)이 세 항 중 하나를 지운다** (2026-09-16, Clausnitzer 2023 에서 우리가 추론).
  논문이 인쇄한 두 문장을 붙이면 분리 시험이 나온다 —
  `[인쇄]` "At **lower current densities** … **reduced sensitivity to microstructural
  variations**" + `[인쇄]` `R_GB,3` 에서 CAM 의 큰 부분이 방전 끝에도 **초기 Li 농도 그대로**
  남는다 (Fig. 5 히스토그램: `x ≈ 0.52` 에 큰 봉우리).
  → **진짜 `LAM_PE` 와 기하 접촉 손실은 `i→0` 에서 남고, 동역학 손실은 사라진다.**
  **최소 2 개 율에서 같은 파라미터를 적합하고 `a_PE` 차이를 보고하면** 동역학 성분의
  하한이 나온다. ⚠ **그러고도 `θ_AM · Q_material` 의 곱은 안 갈라진다** — 이 물음의 본체는
  살아 있고 **범위만 좁아진다.** 자세히는 [[assb-apparent-capacity-decomposition]].
- **제안된 독립 관측 하나가 늘었다**: **복합양극 EIS 의 이온·전자 부분 전도도**
  (Minnmann et al. 2021, ref 22). Clausnitzer 가 결론에서 **자기 검증의 첫 단계**로
  지목한다 — `[인쇄]` "impedance measurements for LCO/LLZO composite cathodes could be
  conducted to determine the ionic and electronic partial conductivities".
  ⚠ 단 **LLZO 계 측정은 문헌에 없다**고 같은 문단이 적는다.
- ★★ **압력 재인가 — 이 계보 최초의 "실제로 수행된" 분리 조작** (2026-09-16, Shi 2020).
  ex situ XRD 도 EIS 도 **관측**이지만, 300 MPa 재가압은 **개입**이다:
  **진짜 재료 손실(rock-salt·구조 붕괴)은 눌러도 안 돌아오고 접촉 손실은 돌아온다.**
  → `ΔQ_mech ≡ Q(P_high) − Q(P_low)` 가 **기하 접촉 손실의 용량 등가에 대한 상한**,
  따라서 **진짜 `LAM_PE` 의 하한**을 준다. 율 연산자와 짝이 된다:

  | 조작 | 지우는 항 | 근거 | 비파괴? |
  |---|---|---|---|
  | `i → 0` | `η(i)` | 2호(추론) → 3호(율 스윕 20 곡선) | ✅ |
  | **`P ↑`** | **`θ_AM`** | **4호 (실측 1 사례)** | ❌ 되돌릴 수 없다 |
  | 둘 다 하고 남는 것 | `Q_material` = 진짜 `LAM_PE` | — | — |

  자세히와 네 개의 경고는 [[assb-pressure-reapplication-separation-test]].
  ★ `[해석]` **이것이 이 카드의 답을 바꾸지는 않지만 우회로를 연다** — OCV **모양**
  으로는 못 갈라도, **압력 축을 하나 더 걸면 같은 셀 안에서 분해가 된다.**
- ★ **율 극한 논증이 실험에서 간접 검증됐다** (2026-09-16, Shi 2020).
  4호 셀의 율은 `[재현]` **≈C/15** 로 2호(≈0.74 C)·3호(0.25–5 C)보다 한 자릿수 낮다
  → `η ≈ 1` 이어야 한다. 그런데 겉보기 용량이 **≈98 %** 날아갔고 압력으로 **60 %p** 가
  돌아왔다. `[해석]` **저율에서도 살아남는 손실 = 기하 성분**. 2호의 분리 시험이
  예측한 그대로다. ⚠ 단 4호는 **율 스윕을 하지 않았다** — 직접 증명이 아니다.
- ★ **새 관측 후보: 충전 전압의 비단조 진동** (2026-09-16, Shi 2020 ESI Fig. S1(c) 인셋).
  `[도표]` 급락 직전 사이클(38·39)의 충전 곡선이 **단조 상승이 아니라 톱니**로 흔들린다.
  ESI 캡션 `[인쇄]`: "the voltage curve becomes **unstable** … **jumping up and down** …
  can be explained by the **intermittent Li transport to and from the
  contracting/expanding cathode particles**."
  `[해석]` **곡선의 모양(용량축·전압축)이 아니라 국소 비단조성이 관측량이다.**
  OCP 적합에서는 **잔차의 고주파 성분**으로 나타나고 보통 노이즈로 버려진다.
  액체셀에는 이 서명이 없다(전해질이 늘 젖어 있다) → **`assb` 전용 판별 feature 후보.**
  ⚠ 크기가 수치로 보고되지 않았고(figure-read 로 대략 ±50–100 mV) 셀 1 개의 5 사이클
  구간에서만 보였다.

### 우리 계획에 붙은 새 제약 (2026-09-16)

- ★ **DEM 라벨 자체가 폭을 갖는다.** Bielefeld 가 인쇄한 실측: 거시 파라미터를 전부
  고정해도 무작위 충전 배열만 바꾸면 임계 근방에서 `θ_AM` 이 **≈30 % ↔ ≈70 %** 로
  이봉으로 갈린다. → **DEM 산출을 라벨로 쓰려면 반드시 폭을 붙인다**
  (`bms-balancing/docs/NEW_MODEL_REQUIREMENTS.md` §5 의 규율을 우리 자신에게).
  그리고 **임계에서 멀리**(`p − p_c ≳ 5 vol%`) 작업해야 한다.
- **DEM 도메인 크기 수렴 시험이 선행 조건**이다 — Bielefeld Fig. 10 의 유한 크기 효과가
  얇은 도메인에서 `θ` 를 낙관 방향으로 편향시킨다.
- `θ_AM` 의 **시간 변화는 아직 아무도 안 줬다.** Bielefeld 는 pristine 정적 기하만 준다.
  ⚠ **2호를 읽고도 그대로다** — Clausnitzer 도 `[인쇄]` "pore formation during cycling …
  **beyond the scope**" · "our current model **does not incorporate mechanics**", 방전
  **1 회**. **`assb` 2/2 편이 시간축을 주지 않았다.** 다만 2호의 **소결 밀도 `ρ_S` 스윕**
  (60–93.1 %)이 **후보 대리 축**이다 (Fig. 8 이 그 지도). ⚠ 제조 공극과 사이클 균열은
  **공극의 분포**가 다를 수 있다 (사이클 균열은 CAM/SE 계면에 우선).
- ★ **산포 규율이 후속 논문에서 지켜지지 않았다.** Bielefeld 는 `θ` 의 실현 간 폭을
  인쇄했는데, Clausnitzer 는 **오차 막대 0 개 · 점당 구조 1 개**이고 도메인이
  `[재현]` **1/28.7 부피**로 더 작다. → **2호 Fig. 10 의 최적 순위(0.94/0.93/0.89)는
  신뢰 근거가 그 논문 안에 없다.** 우리가 N 개 실현으로 **싸게 무효화/검증할 수 있는 자리.**
- **`θ` 는 스칼라가 아니다** (2호가 추가): `[인쇄]` "The share of unconnected clusters
  **increases with increasing distance from the separator**" — `θ_SE(z)` 가 집전체 쪽에서
  떨어지고, `[도표]` Fig. 8b 에서 `SVF 69.4 %`·밀도 70 % 는 **전극의 90 % 가 이용률 ≈0** 이다.
  → forward model 에 `θ` 를 스칼라로 넣으면 집전체 쪽 손실을 **과소평가**한다.

### 새 제약 (2026-09-16, Liu 2024)

- ★★ **율 스윕 분리 시험이 좁아졌다.** [[assb-apparent-capacity-decomposition]] 의 처방
  ("두 율에서 적합 → `a_PE` 차이 = 동역학 성분의 하한")은 **`Q_material` 이 율에
  무관하다**는 전제 위에 있었다. 3호가 그 전제를 깬다 — `[도표]` Fig. 5e: 12 µm 에서
  활물질 손실이 **0.25C 0.093 → 5C 0.185 (2 배)**. **고율 방전 자체가 진짜 재료 손실을
  더 만든다.** → 살아남는 설계는 (a) **저율 쌍만** 쓰거나 (b) **율을 바꾼 뒤 기준 율로
  돌아와 이력을 재서** 비가역분을 빼는 것. 후자가 안전하다.
- ★ **`θ` 는 양극만의 성질이 아니라 (양극 × 전해질) 쌍의 성질이다.** `[도표]` Fig. 4f·7c:
  같은 양극·같은 운전조건에서 전해질 Young 률을 1 → 150 GPa 로 바꾸면 계면 응력이
  **0.05 → 0.55 GPa (≈8 배)**, 벌크 응력은 +0.75 → −1.5 GPa 로 부호가 뒤집힌다.
  → forward model 에 접촉 손실을 넣을 때 **전해질 탄성률·항복강도가 상태변수**다.
- ★ **`η` 의 지배 인자가 두 척도에 걸쳐 있다.** 전극 척도의 입계 저항(2호 `R_GB`)과
  **이차입자 내부 입계 확산도**(3호 `D_GB`) 둘 다. `[도표]` `D_GB` 를 0.05 ↔ 20 배로
  바꾸면 1C 용량이 **0.48 ↔ 0.985** — 재료도 기하도 같은데 겉보기 용량이 두 배다.
  그리고 **OCV 로는 안 보인다.**
- ★ **산포 규율이 3/3 편에서 안 지켜졌다.** 1호만 실현 간 폭을 쟀다. 3호는 본문에
  `[인쇄]` "the **random arrangement** of primary particles … play a critical role in
  dislocation heterogeneity" 라고 적고도 **실현 1 개**다 (`seed`·`standard deviation`·
  `error bar` 각 0 회). Fig. 3j·4e 의 분포는 **한 구조 안의 공간 분포**이지 실현 분포가
  아니다. → 우리가 N 개 실현으로 싸게 검증할 수 있는 자리가 하나 더 늘었다.
- **재현 가능성 원장에 새 표본**: 3호의 Code Availability 는 공개 DAMASK v2.0.2 를
  가리키지만 **이 연구가 쓴 코드는 별 저장소의 `plasticity_chemo_mechanics` 브랜치이고
  기관 허가 + CLA 승인이 있어야 접근된다**. 공개본(2018-05-22)에는 `lithium`·`intercalat`
  이 0 건이고 논문이 "developed" 라고 적은 **독립 FEM 솔버도 없다**.
  (상세는 3호 digest §6·§13 D16.)

### 새 제약 (2026-09-16, Shi 2020 — 실험이 들어오면서 붙은 것)

- ★★ **접촉 손실 라벨을 "면적" 으로 받으면 안 된다.** 4호가 실측으로 보인 6 배 간극
  (위 For 반례). **DEM 이 주는 것도 대개 접촉 수·면적**이므로 이 제약은 우리 계획에
  직접 걸린다 → **면적 → 이용 가능 용량 사상을 우리가 세워야 하고, 그것이 비선형이다.**
- ★ **실측 라벨에도 폭이 없다 — `assb` 4/4 편 연속.** 4호는 실험인데도
  `error bar` · `standard deviation` · `uncertain*` · `replicate` · `seed` **전부 0 회**
  (본문+ESI), 조건당 **셀 1 개**. 게다가 **분할(Weka ML) 정확도 수치가 없고**
  `[도표]` Fig. S2 에서 **CNF 와 LPS 회색도가 크게 겹친다** — ESI 스스로 오분류가
  `[인쇄]` "especially within the **boundaries**" 에서 난다고 적는데,
  **접촉 손실은 정확히 그 경계에서 재는 양이다.**
- ★ **검출 한계가 결론을 만들 수 있다.** 4호의 결론 `[인쇄]` "mechanical degradation
  **does not progress gradually**" 는 사이클 10 의 void 증가가 `[도표]` **+0.36 %p**
  뿐이라는 데 기댄다. 그런데 같은 논문이 뒤에서 `[인쇄]` "very small microfractures …
  **undetectable by the tomography**" 라고 적는다. **두 문장은 같이 설 수 없다.**
  → `[해석]` **우리가 싸게 공급할 수 있는 것**: 검출 한계(50 nm 슬라이스·면내 화소
  미명시)를 넣은 전방 모형으로 **"계단" 이 실재인지 아티팩트인지** 가르기.
- ★ **`θ(N)` 을 부드러운 함수로 매개화하면 안 된다.** 4호가 준 시간축은 **계단**이다
  (void 2.87 → 3.23 → 9.50 vol%; 용량은 사이클 ≈28–45 에 붕괴). 지수·멱 감쇠로는
  원리적으로 못 맞춘다.
- ★ **셀 간 산포가 구조적으로 크다.** 4호는 `[인쇄]` "the sudden drop … could be found
  **earlier or later**" 라고 적고, `[도표]` Fig. 1(a) 셀은 ≈2 mAh g⁻¹ 까지 바닥까지
  가는데 Fig. S1(a) 셀은 **사이클 39→40 한 번에 ≈84 → ≈43** 후 ≈27 에서 안정한다.
  **붕괴의 시간 구조가 셀마다 다르다.** → `θ(N)` 은 결정론적 곡선이 아니라 **확률변수**다.
  ⚠ 그런데 논문은 산포를 **한 번도 정량하지 않는다.**
- **재가압은 일회성 조작이다.** `[도표]` 재가압 후 5–6 사이클에 80 → **≈64 mAh g⁻¹**
  (`[재현]` ≈3 mAh g⁻¹/cycle = 초기 감쇠율의 **3 배**). 원문은 이 재감쇠를 언급하지
  않는다. → 분리 시험 설계에서 **압력 조작은 맨 마지막에 한 번**이어야 한다.
- **EIS 의 식별성이 새 전선이다.** `[인쇄]` "not possible to precisely assign a single
  frequency region … because of the **overlapping time constants**" 라고 적고도
  `R_MF` 954 → 3283 Ω 를 점추정으로 쓴다. → **우리 폭 측정기
  ([[near-optimal-set-width-measurement]])를 3-RC 등가회로에 그대로 걸 수 있다** —
  "244 % 증가" 가 유의한지가 판정 가능한 질문이 된다.

### 새 제약 (2026-09-16, Doux 2020 — 압력 스윕이 들어오면서 붙은 것)

- ★★★ **`P↑` 처방에 안전 한계가 붙는다**: `P_low < P_high < P_short(음극 재료,
  전해질 공극률, 전류밀도)`. Li 금속 + 황화물에서 `P_short ≈ 75 MPa` 이하이고
  25 MPa 도 48 h 밖에 못 버틴다. → **Li 금속·무음극 셀에서는 4호식 재가압 시험을
  그대로 못 쓴다.** 자세히는 [[assb-stack-pressure-operating-window]].
- ★★ **`θ_AM(P)` 을 단일값 함수로 쓰면 안 된다 — 이력이 있다.** 처녀 5 MPa 110 Ω ↔
  25 MPa 경유 후 5 MPa ≈50 Ω, `[재현]` 계면 과잉의 **77 % 가 영구 제거**.
  → 압력 스윕 실험은 **스윕 방향과 이력을 반드시 기록**한다.
- ★ **압력 축의 정보는 저압에 있다.** `[재현]` 계면 과잉이 15 MPa 에서 8 Ω,
  20 MPa 에서 3 Ω → 20 MPa 위는 벌크가 전부다. → [[near-optimal-set-width-measurement]]
  에 압력 2 점을 넣는다면 **(5, 25) 가 아니라 (1–2, 10–15)**.
- ★ **산포를 우리가 전파할 수 있다 — 그리고 문헌에 그 입력이 있다.** 5호 Table S2 가
  **펠릿 4 개**의 상대밀도를 인쇄한다 (80.2 / 84.9 / 80.3 / 83.0 %; `[재현]` s ≈2.3 %p
  → **공극률 15.1–19.8 %**). ★ `assb` **5 편 중 첫 반복 측정**이다.
  단락 기구가 **기공 퍼콜레이션**이므로 이 폭이 `t_short(P)` 로 증폭되는데
  **논문은 전파하지 않는다** (6 점 전부 N=1). → 이 저장소의 DEM/MPM 계열(타 브랜치)로
  **싸게 공급할 수 있는 자리**다.
- ★ **진단 feature 후보 둘이 늘었다.**
  ① **단락 전조로서의 임피던스 "감소"** — `[도표]` 5호 Fig. S2(본문 미인용):
  25 MPa 셀의 고주파 절편이 0/10/20 h 에 **36.6 → 34.3 → 30.7 Ω (−16 %)**,
  **단락 28 h 전**이다. 액체셀 소프트숏은 보통 CE 하락으로 오는데 여기서는
  **저항 자체가 내려간다** → `assb` 전용 서명 후보.
  ② **충전 곡선의 계단식 붕괴** — `[도표]` 5호 Fig. 1 의 Li 금속 셀이
  3.8 → **≈1.85 V 평탄부** → **≈1.2 V 평탄부** 로 내려간다 (본문은 "plummet" 한 마디).
  4호의 **비단조 진동**과 같은 계열이고 크기가 훨씬 크다.
- ⚠ **"압력이 높으면 좋다" 는 어느 쪽으로도 단순하지 않다.** 4호는 300 MPa 로
  용량을 살렸고 5호는 75 MPa 로 셀을 죽였다. **작용 지점이 다르기 때문이다**
  (양극 복합체 vs 음극/전해질 기공). → 압력을 상태변수로 넣을 때 **전극별로 다른
  부호**를 갖는다고 적어야 한다.

### 새 제약 (2026-09-16, Lee 2020 — 무음극이 들어오면서 붙은 것)

- ★★★ **"무음극은 OCP 가 평탄하다" 에 조건이 붙는다.** Ag–C 무음극에서
  `[인쇄]`+`[도표]` **앞 9.5–16.6 % 의 용량 동안 음극 전위가 ≈1 → 0 V 를 훑는다**
  (Fig. 4a 의 컷오프 5 점 사상 + SI Fig. 4c 의 Ag–C\|Li 반쪽전지).
  → `bms-balancing/docs/ASSB_TRANSFER_NOTE.md` §1 의 **3 파라미터 창 모형**
  (`a_PE, b_PE` + 평탄 상대극)은 **전압창 전체에 걸면 안 되고 3.6 V 위에서만** 성립한다.
  ⚠ 그리고 그 구간의 **모양이 음극 조성의 함수**다 (`[인쇄]` SI Fig. 14: Ag 를 늘리면
  3.5 V 부근에 작은 평탄역이 생긴다) → **음극 조성이 완전지 곡선 모양의 상태변수**다.
- ★★★ **제작 압력과 운전 압력은 다른 연산자다.** 위 미결 항목 4 참조.
  [[assb-pressure-reapplication-separation-test]] 의 `P↑` 연산자는 **이 셀에 적용
  불가**다 — 4호가 쓴 **300 MPa 는 이 셀 운전 상한(4 MPa)의 75 배**다.
  ⚠ 모집단이 다르다(펠릿 vs Ah 급 파우치 적층). 방향은 **무음극·대면적으로 갈수록
  운전 압력 창이 좁아진다.**
- ★★ **압축의 비가역성이 기하 채널에서도 확인됐다.** `[인쇄]` Table S2:
  WIP(490 MPa) 전후 셀 두께 **644.5 ± 2.9 → 609.0 ± 2.4 µm** (`[재현]` −5.51 %),
  **7 일 무압 방치 후 609.8 ± 2.6** (복원 +0.8 µm, 산포 안).
  → 5호가 임피던스로 준 `θ(P)` 이력(경로 의존)의 **독립 확인**이다.
  `[해석]` **제작 압력은 "한 번 치르는 비용" 이고 상태에 영구히 남는다.**
- ★★ **`LLI` 추정자의 분해능이 판정 대상이다.** [[near-optimal-set-width-measurement]]
  를 그대로 건다: "CE 99.8 % 와 99.99 % 를 구분할 정보가 자료에 있는가."
  6호의 두 셀(20 mAh 맞음 ↔ 0.6 Ah 10 배 어긋남)이 **정답이 있는 시험 문제**다.
- ★ **음극이 시간에 따라 바뀌는 재료다.** `[인쇄]` Ag 가 **매 사이클 집전체 쪽으로
  이동하고 돌아오지 않는다**(Fig. 3e,f 의 Top/Middle/Bottom 분포 변화).
  → [[halfcell-ocp-shape-invariance]] 의 "모양 불변" 가정이 **ASSB 무음극에서는
  음극 쪽에서 먼저** 깨진다.
- ★ **산포 규율이 6/6 편에서 안 지켜졌다.** 6호는 **산업체 · *Nature Energy* ·
  Ah 급 파우치 스케일업**인데도 `n =`·`N =`·`error bar`·`standard deviation`·
  `replicate`·`uncertain*` 이 **본문 10 쪽 + SI 18 쪽 전수 0 회**다. 유일한 산포는
  **Table S2 의 ±2.2–2.9 µm**(정의도 n 도 없다) — 5호 Table S2 에 이어 **두 번째이고
  둘 다 전기화학이 아니라 기하다.**
  ⚠ 정성적 산포 언급 둘(`[인쇄]` ">4 MPa 에서 단락 **확률** 증가", "C 단독에서 단락이
  **쉽게** 발생")은 **분모를 밝히지 않는다.**
- ⚠ **초록의 두 수치가 같은 셀의 것이 아니다.** `[인쇄]` ">900 Wh l⁻¹" 는
  **5 Ah 10-적층셀**(0.05 C, **무압**, 942)이고 `[인쇄]` "1,000 cycles" 는
  **0.6 Ah bi-cell**(0.5 C, 2 MPa, **703** Wh l⁻¹)이다. → **문헌에서 성능 수치를
  옮길 때 셀을 확인한다.**

### 새 제약 (2026-09-16, Spencer-Jolly 2023 — operando 회절이 들어오면서 붙은 것)

- ★★★ **음극에 OCP 가 하나가 아니다.** 충전용과 방전용이 따로 있어야 한다
  (충전에 없는 상이 방전에 있고, 그것이 **열역학적**이다). → ASSB 인수인계 노트 §1
  의 3 파라미터 창 모형은 **방향별로 따로 적합**해야 하고, 그 둘의 차이를 "열화" 로
  읽으면 **없는 열화를 만든다.**
- ★★ **모집단 경계가 넷이다** — 6호와 7호는 같은 재료계가 **아니다**:
  **탄소**(카본블랙 ↔ **흑연**) · **상대극**(완전지 ↔ **반쪽전지**) ·
  **사이클 수**(1000 ↔ **1**) · **제작 압력 방식**(등방 490 MPa ↔ **일축 400 MPa**).
  → **7호의 "Ag 는 임계전류를 못 올린다"(<2.5 mA cm⁻²)는 흑연 계의 판정**이고,
  6호의 3.2 mA cm⁻² × 1000 사이클과 **모순이 아니다** — 7호 자신이 `[인쇄]`
  "the **type of carbon chosen will have a significant impact**" 라고 적는다.
  **문헌에서 재료계 결론을 옮길 때 탄소 종류를 먼저 확인한다.**
- ★★ **Ag 의 시간 도함수는 여전히 없다.** 7호가 준 것은 **칸 사이의 화살표(경로)**
  이지 **그 시간 변화율**이 아니다 — `[도표]` Fig. 6 D→E→F 가 **1 사이클**이고,
  복귀율이 `[인쇄]` "a **return to a near-pristine state**" 라는 형용사 한 마디다.
  6호의 "100 사이클에 돌아오지 않는다" 와 **모순이 아니라 시간척도가 다르다.**
  → **사이클당 Ag 잔류를 재는 것이 여전히 비어 있는 자리다.**
- ★ **인쇄된 수치도 검산해야 한다.** `[인쇄]` "maximum capacity stored by alloying
  with Ag (approx. **0.60 mA h cm⁻²**)" 를 `[재현]` 자기 조성(5 µm · 5.7 vol% Ag)과
  Li₁₀Ag₃ 화학량론으로 재계산하면 **0.25** 다 (**≈2.4 배**; Ag 당 Li 8.3 개가 필요한데
  상평형 최대가 3.33 이다). **같은 문장의 흑연 0.28 은 `[재현]` 0.33 으로 맞는다.**
  → **이 값을 그대로 인용하면 안 된다** (7호 digest D2).
- ⚠ **산포 규율이 7/7 편에서 안 지켜졌다.** 7호도 `n =`·`N =`·`error bar`·
  `standard deviation`·`replicate`·`uncertain*` 가 **본문 13 쪽 + SI 6 쪽 전수 0 회**다.
  `[인쇄]` "Graphite alone and Ag-graphite composite layers were observed to have the
  **same failure point**" 가 **각 1 셀 비교**로 보인다.
  ★ **단 하나 나아진 것**: `[인쇄]` 원자료가 **Oxford Research Archive
  (DOI 10.5287/bodleian:kKBPZ282m)** 에 공개돼 있다 — **이 계보에서 자료를 공개
  저장소에 올린 첫 편**이다. (우리가 산포·검출한계를 직접 잴 수 있는 자리.)

### ★ 아홉 번째 — **반례도 근거도 아닌, 계보의 출발점을 날짜로 찍는 표본** (2026-09-22, Sadegh Kouhestani et al. 2022 · ⚠ Review, 1차 측정 0)

`raw/papers/kouhestani2022_phm-solid-state-batteries-perspective.md`
(*Energies* **15** (2022) 6599; 본문 26 쪽, SI 없음, sha256 봉인). **수치는 전부 재인용이고
이 절에서 쓰는 것은 수치가 아니라 "2022 년 PHM 종설이 무엇을 어휘로 갖고 있었는가" 다.**

**(가) ★★★ 이 카드의 물음이 분류 차원에서 지워진 자리를 찍는다.**
`[인쇄]` §2.2 "**The loss of active materials mainly stems from the electrical contact
loss** that is caused by graphite spalling, adhesive decomposition, collector corrosion,
and electrode particle cracking." → 이 리뷰의 어휘에서 **`LAM ⊃ 접촉 손실`** 이다.
`[해석]` 3호(Liu 2024)가 `[인쇄]` "실험의 활물질 손실은 rock-salt + 파괴로 고립된 활물질을
둘 다 포함한다" 고 **실험의 한계로** 적은 병합을, 이 종설은 **정의로** 한다. 우리가 가르려는
두 양이 **PHM 문헌에서는 처음부터 한 낱말**이었다는 것 — 그리고 그 낱말의 기구 목록이
**전부 액체셀**(흑연 박리·바인더·집전체 부식·입자 균열)이고 `[도표]` Fig. 6 의 "Contact
Loss" 두 자리도 **Cu/Al 집전체**라는 것. **복합양극 AM|SE 계면은 이 리뷰에 없다.**

**(나) ★★ Q4 계보의 "1–7호 상태(안 쟀다)" 가 PHM 쪽에서도 같은 시점에 성립했음을 확인한다.**
`identifiab*` **0 회** (8호 Li 2026 은 5 회). 가장 가까운 문장이 `[인쇄]` "difficult parameter
identification" — **실무 곤란**으로만 — 과 `[인쇄]` "large number of parameters … inevitable
errors in each parameter" 이고, **같은 논문 §3.1.3 이 정반대**를 인쇄한다: `[인쇄]`
"Generally, **the more parameters** that are involved in the model, **the higher the
accuracy** of the model." → **모델 차수에 대한 두 방향 명제가 한 논문 안에서 화해되지
않은 채 있다.** 이것이 2022 년의 상태다.

**(다) ★ "모델 차수는 상태변수" 의 세 번째 독립 인쇄 — 단 액체셀 ECM, 재인용.**
`[인쇄]` §3.1.2 "the aging or temperature change of the LIB will cause the internal
impedance characteristics of the battery to change **from a single impedance arc to a
double impedance arc**, which significantly impacts the accuracy of the battery model [84]."
10호(Larfaillou 2016 재인용, LiPON RQ 3→4) · 11호(1차 DRT, 2–3→5) 에 이어 **셋째**.
⚠ ref [84](Cho 2012)가 실제로 그것을 보였는지는 원전 확인 전이다 →
[[drt-peak-count-nonidentifiability]].

**(라) ★★ `A_eff` 형 접촉 파라미터의 계보 입구.**
`[인쇄]` §3.1.1 "Tian et al. [60] and Shao et al. [60] introduced **a parameter to describe
the contact area, which adjusts the current density in the 1-D Newman model**. They found
that the capacity drop was correlated with the loss of contact area, and the optimal
charging performance could be obtained under medium compressive pressures (0.4–1 MPa)."
`[해석]` 9호(Huo 2025) Table 1 의 `A^p_eff`(BV 분모의 유효 접촉 면적비)와 **형태가
같다**. [[assb-lampe-contact-product-degeneracy]] 가 손으로 보인 `A_eff·ε_p/R_s` 곱 축퇴가
**2017 년 모델 형태에서 시작됐을 가능성**. ⚠ 두 저자에 같은 번호 [60] 이 붙어 있어
(digest D4) **`0.4–1 MPa` 의 출처는 이 지면으로 확정되지 않는다.** 원전 둘(Tian & Qi
*JES* 2017, 164, E3512 · Shao *Energy* 2022, 239, 121929)을 받아야 한다.

**(마) "라벨이 없다" 의 2022 년 판.** `[인쇄]` "very few instances where a battery can be
completely exhausted or fully charged at the pack level"(재인용, Yang 2021) ·
`[인쇄]` §4 "**most PHM techniques are based on simulation results and not
experimental**"(1차) · 결론 (1) `[인쇄]` "primarily used to estimate the **SOC** of SSBs" ·
(2) "very few studies … **lack of accurate data**". → **8호의 "no direct capacity labels"
와 같은 명제가 다른 원전에서 4 년 앞서 나온다.** 그리고 우리가 Table 1 을 한 줄씩 대조한
결과(digest §Table 1 해체) **SSB 실측 열화 데이터로 SOH/RUL 을 추정한 항목은 0 / 28** —
논문 자신의 결론과 일치한다.

**이 절이 For / Against 어느 쪽인가**: **어느 쪽도 아니다.** 이 편은 근거를 주지 않는다 —
**우리 물음이 문헌에서 어떤 어휘 상태에서 출발했는가**를 날짜와 함께 고정한다. 그것이
종설 두 편(8호·12호)을 넣고 얻은 것이다: **2022 → 2026 사이에 PHM 문헌은 "identifiability"
라는 이름을 얻었고(0 → 5 회), 여전히 재지는 않았다.**

### ★ 열 번째 — **근거가 아니라 "운전 조건이 OCV 채널을 설계상 닫는다" 는 요구 측 진술** (2026-09-22, Zheng et al. 2026 · ⚠ Perspective, 1차 측정 0, `[인쇄]` "No data was used")

`raw/papers/zheng2026_assb-grid-realistic-appraisal.md` (*Energy* 345, 140229; Nanjing Tech +
Huadian 전력연구원 + Shuangdeng 전지 제조사 — **저자 소속이 수요 측**이다).

**이 편이 이 카드에 하는 일은 근거 추가가 아니라 "물음이 놓일 운전 조건" 을 인쇄한 것이다.**
세 문장이 한 문단에 있다 (§4):

1. `[인쇄]` "grid batteries rarely perform full cycles between 0 % and 100 % SOC. Instead, they
   operate within a limited window (e.g., **20–80 % SOC**) … making it **impossible to obtain a
   full open-circuit voltage (OCV) curve** for calibration."
2. `[인쇄]` "the **flat voltage profiles** of common ASSB pairings (e.g., **LFP cathodes**) exhibit
   minimal voltage change over large SOC ranges"
3. `[인쇄]` "these profiles can be **distorted by voltage hysteresis arising from mechanical
   stresses**"

그리고 같은 절이 **SOH 가 갈라야 할 두 항**을 정의한다: `[인쇄]` "distinguish between **true
active material loss** and a reduction in 'useable capacity' caused by **rising impedance or
increasing overpotentials**".

**세 가지가 이 카드에 걸린다**:

- ★★★ **접촉 손실이 이분법에서 사라졌다.** 같은 절 첫 문단은 ASSB 의 지배 실패 모드를
  `[인쇄]` "the gradual **loss of interfacial contact**, the propagation of cracks … chemo-mechanical
  evolution" 으로 꼽는다. 그런데 SOH 정의는 `LAM` ↔ `kinetic` 둘뿐이고 **접촉 손실이 어느
  쪽인지 적지 않는다.** 12호는 `LAM ⊃ 접촉 손실` 로 **정의에 흡수**했고, 13호는 **정의에서
  누락**했다 — 두 종설이 다른 방식으로 같은 결과(분리 물음이 없는 분류)에 도달한다.
  우리 3 항(`θ_AM · Q_material · η(i)`)과는 둘 다 다르다.
- ★★ **운전 창이 OCV 채널을 설계상 닫는다.** 이 카드의 물음("OCV 적합이 가를 수 있는가")은
  **완전 OCV 곡선**을 전제한다. 그리드 ASSB 는 (i) 20–80 % 창 (ii) LFP 평탄역 (iii) 응력
  이력 — 셋이 겹쳐 **그 전제가 설계 단계에서 없어진다.** `[해석]` 이 카드의 답이 "가를 수
  있다" 로 나오더라도 **그리드 용도에는 적용 창이 없다**; 반대로 이 카드의 폭 측정기는
  "부분 창에서 폭이 얼마나 벌어지는가" 를 잴 수 있고, 그것이 13호가 요구하는
  "multi-parameter SOH model" 에 우리가 공급할 수 있는 유일한 것이다
  ([[data-window-identifiability]] 의 ASSB 판).
- ★ **음극 전제의 세 번째 반례 — 이번엔 처방으로.** 13호는 Li 금속을 `[인쇄]` "may be
  misguided" 로 배제하고 **Si 계 음극**을 권한다. Si OCP 는 비평탄 + 이력(09-21 세미나:
  8 종 전부 닫힌 이력 루프). 9호(Li-Si 셀) · 11호(graphite 셀)에 이어 **"전고체 음극 = 평탄
  → 5→3 붕괴" 가 그리드 설계 처방에서도 성립하지 않는다.** ⚠ 13호는 Si OCP 를 한 번도
  논하지 않는다 (G10) — 좁은 창에서 SOC 를 추적하라고 요구하면서.

**Q4 는 0 / 13 이고 성질이 또 바뀐다**: 8호가 `identifiab*` 5 회로 이름을 붙였다면 **같은 해
13호는 이름 없이 역문제를 처방한다** — `[인쇄]` "These models **inversely estimate** the current
state of interfacial contact **and** material properties." 9호의 곱 축퇴 `A_eff·ε_p/R_s` 가
정확히 "접촉 상태 ↔ 재료 물성" 사이에 있다 ([[assb-lampe-contact-product-degeneracy]]). ⇒
"2026 년 PHM 문헌은 식별 가능성을 안다" 는 일반화는 **8호 한 편의 일**이다.

**이 절이 For / Against 어느 쪽인가**: **어느 쪽도 아니다.** 근거 0. 얻은 것은 **(a) 분류
체계 셋(12호·13호·우리)이 서로 다르다는 실측 (b) 물음의 적용 창이 그리드에서 설계상 닫힌다는
요구 측 진술 (c) 압력 창 요구치의 세 번째 독립 인쇄** (아래 새 제약 + [[assb-stack-pressure-operating-window]]).

### 새 제약 (2026-09-22, Li et al. 2026 — 종설이 들어오면서 붙은 것)

> ⚠ 이 절의 제약은 **1 차 측정이 아니라 문헌의 요구·재인용**에서 온다. 앞 절들(1–7호)의
> 제약과 **근거 강도가 다르다**.

- ★★ **압력 창의 아래 벽에 산업 요구치가 생겼다: `<≈1 MPa`** (재인용, Xu 2024).
  → [[assb-stack-pressure-operating-window]] 의 실측 창 전체가 그 위에 있다.
  `[해석]` 우리가 설계할 분리 시험의 **운전 압력 기준점**은 실험실 값(2–5 MPa)이
  아니라 이쪽이어야 하고, 그러면 **`θ_AM` 손실이 더 크고 더 빨리** 온다고 예상해야 한다.
  ⚠ **재인용이므로 Xu 2024 를 받기 전에는 설계 입력으로 쓰지 않는다.**
- ★★★ **우리 폭 측정기의 소비처가 문헌에 그려져 있고, 그 칸이 비어 있다.**
  `[도표]` 8호 Fig. 2 의 안전 감독기가
  `I_cmd = min(I_V, I_T, I_plate, I_power, I_imbalance, **I_uncertainty**)` 를 계산한다 —
  **여섯 번째 전류 상한을 추정 불확실성에서 뽑는데 계산법이 논문에 없다**
  (8호 digest G1). → [[near-optimal-set-width-measurement]] 가 그 입력의 재료를 만든다.
  ⚠ **폭 → 허용 전류의 사상은 아직 없다** — 빈칸의 좌표가 확인된 것까지다.
- ⚠ **종설의 수치를 이 카드의 근거로 올리지 않는다.** 8호가 재인용한
  `SOH RMSE ≤0.873 %` 가 **우리가 이미 가진 원전과 어긋난다**(위 Evidence).
  → **`[인쇄]`(원전) 와 `[재인용]`(종설) 을 구분해 적는다.** Q1~Q8 채움표의 8호 행은
  전부 재인용이다.
- ⚠ **BMS 문헌은 열화 모드를 쓰지 않는다.** 8호는 SOH 를 끝까지 **스칼라**로 다루고
  `LLI`·`LAM`·`degradation mode` 가 전수 0 회다 — **Birkl 2017 을 인용하면서도.**
  `[해석]` **우리 축(모드 분해)이 BMS 배치 문헌에 아직 도착하지 않았다.**
  이것은 공백이면서 동시에 **우리가 채울 수 있는 자리**다.

### 새 제약 (2026-09-22, Huo 2025 — 적합으로 지분을 정하는 첫 편이 들어오면서 붙은 것)

1. **★ "평탄 상대극 → 5→3 붕괴" 가 모든 ASSB 에 성립하지 않는다.** 이 카드와
   `bms-balancing/docs/ASSB_TRANSFER_NOTE.md` §1 은 상대극이 평탄하다는 전제에서
   `a_NE`·`b_NE`·`γ_Si` 의 민감도가 정확히 0 이 되는 것을 실측했다. 9호는
   **Li-Si 합금 음극**이고 모델이 `U^n_ocp(θn)` 를 **비평탄 보간 함수**로 둔다 —
   `[재현]` N/P ≈ **3.14** ⇒ 사이클당 음극 화학량론 스윙 **31.8 %**.
   **⇒ 이식 전에 상대극 화학을 먼저 갈라야 한다.** Li-In·Li 금속·무음극은 평탄
   가정이 살아 있고, **합금(Li-Si) 계열은 5 파라미터가 그대로 필요하다.**
2. **`θ_AM` 과 `η(i)` 가 한 파라미터에 묶이는 실제 사례가 생겼다.**
   [[assb-apparent-capacity-decomposition]] 의 3 항 분해에서 9호는 `ε_p` **하나**만
   푸는데 `a_s = 3ε_p/R_s` 도 같이 줄어 분극이 커진다 — `[재현]` 증폭 1.60 / 1.32.
   ⇒ **2호에서 세운 율 스윕 분리 시험(`i→0`)이 이 논문에 그대로 처방이 된다.**
   그리고 **증폭이 상수가 아니므로**(동작점 의존) 사후 보정으로 뺄 수 없다.
3. **압력이 상태변수로 측정됐는데 모델에 안 들어간다.** 9호가 이 계보 최초로
   **사이클 중 힘 연속 시계열**을 기록한다 (`[재현]` 평균 ≈36.9 MPa · 주기 변조
   ≈0.32 MPa). 그런데 노화 식 Eq. (2) 는 **사이클 수만의 함수**다. ⇒ 8호가
   제안한 "압력을 BMS 상태변수로" 와 **같은 공백이 실험 논문 쪽에서도 확인된다.**
4. **`LLI` 축을 닫는 방법이 하나 더 확인됐다 — 파라미터 동결.** 리튬 재고를 정하는
   두 수(`cp0`·`cn0`)가 신품에서 한 번 적합된 뒤 **노화 전 구간 고정**이고 **값이
   비공개**인데, 그 위에서 `[인쇄]` "minimal or no loss of lithium inventory" 를
   결론한다. 그리고 SI 가 **쿨롱 효율 제출을 명시적으로 거부**한다(`[인쇄]` "our
   analysis and modeling 에 쓰이지 않는다") — 6호에서 본 대로 **CE 는 `LLI` 의
   유일한 전하 수지 채널**이다. ⇒ **"LLI 없음" 이 관측이 아니라 설계의 결과인
   경우를 라벨 출처 검사에 추가한다.**
5. ⚠ **우리가 이 논문에 공급할 수 있는 것이 있다** — `A_eff · ε_p / R_s` 의 근최적
   폭. 우리 폭 측정기는 화학 무관이다. 필요한 입력은 **반쪽전지 OCP 두 곡선**(원전이
   출처를 안 적었다)과 **비공개 6 개 파라미터**뿐이다. ⇒ 후속 후보 1 순위가
   원전의 ref [27](같은 연구실의 모델 논문)인 이유다.

### 새 제약 (2026-09-22, Vadhva 2021 — 방법론 리뷰가 들어오면서 붙은 것)

1. **★ 주파수 대역으로 전극을 지목하는 모든 문장에 화학 꼬리표를 단다.**
   `[인쇄]` "full devices using a **LMA** and an intercalation cathode typically
   assign the **SE\|cathode interface as the lowest frequency arc**, while those
   utilising an **In–Li anode assign this to the SE\|anode interface**."
   ⇒ **우리 계보 4호(In 음극)와 9호(Li-Si 합금 음극)는 서로 다른 화학인데 둘 다
   주파수로 전극을 지목했다.** 9호의 `R_SEI`(중주파) ↔ `R_ct`(저주파) 귀속은
   **Li-Si 합금 완전지의 귀속을 확립한 연구가 리뷰에 없으므로 무보증**이다.
2. **★★ `R_anode(N)` 의 증가를 노화로 읽기 전에 SoC 를 고정했는지 확인한다.**
   `[인쇄]` In 음극 계면 저항이 **한 번의 방전 안에서도** 리튬화도(In-rich 화)에
   따라 크게 증가한다. ⇒ 4호의 `[도표]` `R_LF` ≈0.7 → ≈110 kΩ(≈157 배)에서
   **노화분과 SoC 분이 갈리지 않는다** — 4호는 사이클마다 같은 SoC 에서 쟀는지
   적지 않았다. **이 카드의 "모르는 것 2" 에 붙는 경고다.**
3. **★★★ EIS 를 `θ_AM` 의 독립 관측으로 쓰려는 계획에 조건을 단다.**
   `[인쇄]` 같은 `R_MF` 에 **접촉 손실**과 **분해층 성장**이 함께 귀속된다.
   ⇒ **EIS 는 [[assb-lampe-contact-product-degeneracy]] 의 곱 축퇴를 깨는 대가로
   새 축퇴를 들여온다.** 그 페이지 처방표의 "다중 SOC EIS" 는 **단독으로는 못 쓴다** —
   **압력 되돌림 또는 대칭셀 쌍과 반드시 짝지어야 한다.**
4. **모델 차수를 시간에 대해 고정하지 않는다.** `[인쇄]` Larfaillou: 신품 **3 RQ**
   → 60 h/60 °C 노화품 **4 RQ**, 새 RQ 의 귀속은 `[인쇄]` "Li\|LiPON interface
   **and/or** in the LCO bulk". ⇒ **노화 시계열을 고정 회로로 적합하는 절차(9호)에
   구조적 결함이 있다.** 그리고 **"and/or" 는 우리가 찾던 형태의 증거다** — 저항
   하나가 어느 전극 것인지 모르는 채 열화 서사에 들어간다.
5. **역문제를 풀기 전에 데이터가 그것을 감당하는지 먼저 판정한다 (실행 가능).**
   **Lin-KK**(ref. 43, KIT 소프트웨어)는 모델 없이 선형·정상·인과를 검사한다.
   ⇒ 우리가 언젠가 ASSB EIS 를 다루면 **첫 단계**이고, 문헌 EIS 를 인용할 때
   **"K–K 검증을 했는가" 가 라벨 출처 검사의 새 항목**이 된다
   (`[인쇄]` Kamaya 2011 은 100–500 mV 섭동에 K–K 검증 0 — 기준의 2–10 배).
6. **압력이 분해능 연산자이기도 하다 (새 축).**
   `[도표]` Fig. 11a: **400 MPa 에서 `R_int` 가 사라져야 `GB` 원호가 보인다.**
   ⇒ [[assb-pressure-reapplication-separation-test]] 의 `P↑` 는 **용량을 되돌리는
   연산자**일 뿐 아니라 **관측 가능한 시상수 개수를 바꾸는 연산자**다.
   그리고 `[인쇄]` "**<1 Ω cm², which remained after the pressure was removed**" 는
   [[assb-stack-pressure-operating-window]] 가 5호에서 잡은 **이력**의 **산화물
   독립 재현**이다. ⚠ 400 MPa 는 5호의 Li\|황화물 상한(75 MPa)의 **5.3 배** —
   **창은 전해질 재료의 함수**라는 기존 단서와 일치한다.
7. **⚠ 우리 위키가 이 리뷰보다 한 칸 앞서 있는 자리가 하나 있다.**
   리뷰는 `[인쇄]` ML+EIS 의 예로 **ref. 174 = Zhang et al. *Nat. Commun.* 2020**
   을 든다. **그 논문은 우리가 이미 가지고 있다** ([[zhang2020-eis-aging-dataset]]):
   `state I~IX` 중 **넷이 DC 전류 중** 측정이라 리뷰 자신의 `stability` 요건을
   위반하고, **모드 라벨이 없으며**, ARD 가 고른 두 주파수가 **비식별**이다.
   ⇒ **리뷰의 "ASB 로 옮기자" 는 권고에 우리가 붙일 단서가 이미 검증돼 있다.**

### 새 제약 (2026-09-22, Yu 2024 — DRT 를 실제로 돌린 첫 편이 들어오면서 붙은 것)

1. ★★★★ **이 카드의 출발 전제가 음극 재료의 함수라는 것이 확정됐다.**
   §"지금까지 아는 것" 의 **5 → 3 파라미터 붕괴**는 `a_NE`·`b_NE`·`γ_Si` 의
   민감도가 **0** 이라는 것에서 나왔고, 그것은 **음극 OCP 가 평탄**할 때만 참이다.
   11호의 음극은 **graphite** — 스테이지 평탄역이 여럿인 **구조 있는 OCP** 다.
   ⇒ **붕괴표에 단서를 단다: "Li-In / Li 금속 / 무음극 셀에 한함."**
   9호(Li-Si)에 이어 **두 번째 반례**이고, 이쪽은 **액체셀과 같은 상용 흑연**이라
   `LLI ↔ LAM_NE` 축퇴가 **그대로 이식된다.** (`γ_Si` 축만 안 온다.)
2. ★★★★ **"DRT 를 쓰면 개수 문제가 풀린다" 는 기대를 접는다.**
   8호가 DRT 를 처방했고 10호가 `[인쇄]` "A powerful tool to **guide ECM
   selection**" 이라 적었다. 11호가 실제로 돌린 결과는:
   **개수가 사이클로 늘고(3 사례) · 조작으로 줄고(1 사례) · 배선으로 바뀐다(1 사례).**
   ⇒ **DRT 는 개수를 "재는" 도구가 아니라 개수가 무엇에 달려 있는지 보여 주는
   도구다.** 우리가 9호·11호에 적용할 판정은 **"몇 개가 맞는가" 가 아니라
   "개수가 정해지는가" 여야 한다.**
3. ★★★ **우리 폭 측정기가 붙을 자리가 구체적으로 특정됐다.**
   11호가 남긴 것은 **nuisance 1 점 변동**(Fig. S3, 배선 1 회 교체)이다.
   [[near-optimal-set-width-measurement]] 의 기계를 여기에 붙이면
   **`λ` 를 격자로 흔들어 봉우리 개수·위치·높이의 궤적**을 만들 수 있고,
   그것이 **"DRT 로 잰 저항 증가분" 에 폭을 붙이는 최소 절차**다.
   ⇒ **화학·방법에 무관하게 "답이 하나로 정해지는가" 를 재는 우리 논리가
   EIS·DRT 축에도 그대로 이식된다**는 것이 이 편으로 확인된다.
4. ⚠ **압력을 "θ_AM 전용 연산자" 로 쓰지 않는다.**
   [[assb-pressure-reapplication-separation-test]] 는 4호 1 편(1 셀 1 점)에
   기대어 있었다. 11호가 **5 점**을 주면서 동시에 **선택성이 없다**는 것을 보였다
   (`[도표]` 재가압이 P1·P2·P3·P4 를 **전부** 10–27 % 줄인다).
   ⇒ 그 개념 페이지의 `confidence: low` 는 **유지**하고, 반례를 본문에 적는다.
5. ⚠ **산업체 논문의 provenance 가 9호보다 뒤다.**
   9호는 Table 3 에 6 개 값을 `[인쇄]` "not disclosed" 로 **찍어 두어** 구멍을
   셀 수 있었다. 11호는 **파라미터 표가 없다** — 조성비·로딩·두께·N/P·입도·
   코팅 두께·`Ω mg⁻¹` 정규화 질량·**어느 셀이 Cl 이고 어느 셀이 Br 인지**가
   전부 없고, `[인쇄]` "The authors do not have permission to share data."
   ⇒ **`assb` 산업체 편(9·11호, 그리고 36호 예정)에는 "구멍을 찍었는가" 를
   별도 항목으로 기록한다.**

### 새 제약 (2026-09-22, Sadegh Kouhestani 2022 — PHM 종설이 들어오면서 붙은 것)

1. ★★ **`LAM` 이라는 낱말을 문헌에서 받을 때 "접촉 손실을 포함하는가" 를 먼저 묻는다.**
   12호가 `[인쇄]` "The loss of active materials **mainly stems from** the electrical
   contact loss" 로 정의했으므로, PHM 계열 논문의 `LAM` 은 **우리 `LAM_PE` 가 아니라
   `1 − θ_AM·(Q_material/Q₀)` 전체**일 수 있다. 라벨 층위 표(Q3)에 **"LAM 의 정의 범위"**
   를 적는다 — 이 칸이 없으면 액체셀 `LAM` 수치를 ASSB 로 옮길 때 두 양이 섞인다.
2. ★★ **`A_eff` 형 파라미터의 원전을 받기 전까지 9호의 곱 축퇴를 "Huo 2025 고유" 로
   적지 않는다.** 12호가 Tian & Qi 2017 · Shao 2022 를 같은 형태로 소개했으므로
   `evidenceScope: single-source` 는 유지하되 **"P2D 계열에 널리 반복될 가능성"** 을
   [[assb-lampe-contact-product-degeneracy]] 에 이미 적어 둔 그대로 두고, 원전 두 편을
   **큐 후속 1·2 순위**로 올린다.
3. ★ **종설의 "≈1 MPa" 는 두 원전에서 독립적으로 나왔으나, 둘 다 우리 근거가 아니다.**
   8호 "<≈1 MPa"(Xu 2024, 산업 요구) · 12호 "0.4–1 MPa"(Tian/Shao, 모델 최적, 출처
   미확정). [[assb-stack-pressure-operating-window]] 의 **아래 벽 후보**로만 두고 값은
   원전 확인 후 적는다.
4. ⚠ **인용 위생이 무너진 종설은 재인용 수치를 위키에 옮기지 않는다 — 방향도.**
   12호는 인용번호 오류·제목-내용 뒤바뀜이 **21 건**(digest D1–D21)이고 접수→승인이
   9 일이다. 10호(D5 인용번호 1 건)·8호(Su 2024 숫자 어긋남 1 건)에 적용한 규율을
   **더 강하게** 적용한다: 이 편에서는 **"이 지면에 이렇게 적혀 있다" 이상을 쓰지 않는다.**

### 새 제약 (2026-09-22, Zheng 2026 — 그리드 appraisal 이 들어오면서 붙은 것)

1. ★★ **적용 창을 명시한다.** 이 카드가 답을 내면 그 답에 **"완전 OCV 곡선이 있을 때"**
   라는 조건을 붙인다. 13호가 그리드 운전을 `[인쇄]` "20–80 % SOC … impossible to obtain a
   full OCV curve" 로 적었으므로, **부분 창에서의 근최적 폭**을 별도 결과로 낸다
   ([[data-window-identifiability]] · [[near-optimal-set-width-measurement]]). 창을 안 적은
   분리 진술은 그리드에는 무효다.
2. ★★ **압력 창의 위 벽을 둘로 나눠 적는다.** 5호(Doux)의 위 벽 = **단락**(Li 크리프, ~h).
   13호의 위 벽 = `[인쇄]` "creep and stress relaxation … fatigue-driven micro-crack initiation"
   (**피로**, ~년, 1 차 주장·데이터 0). 둘은 기구·시간 스케일이 다르므로
   [[assb-stack-pressure-operating-window]] 에서 **한 숫자로 합치지 않는다.**
3. ★ **압력 요구치는 세 원전이 독립 수렴한 자릿수로만 쓴다** — 8호 `<≈1`(Xu 2024) · 12호
   `0.4–1`(Tian/Shao) · 13호 `<5`(Si 근거 [35]/[45]). **세 값 모두 원전 미수령**이고 13호의
   "5" 는 인용 문장이 값을 주는지 확인되지 않았다(G3). 위키에는 "≈1–5 MPa, 종설 셋" 까지만.
4. ★ **접촉 손실의 소속을 라벨 정의에 명시하도록 요구한다.** 12호(흡수)·13호(누락)가 보여
   준 대로 종설의 `LAM` 정의가 접촉 손실을 어디 두는지 제각각이다. 앞으로 들어오는 `assb`
   논문은 Q3 판정에 **"접촉 손실 = LAM 안 / 밖 / 미언급"** 한 칸을 더 적는다.
5. ⚠ **13호의 수치를 근거로 옮기지 않는다.** Table 1 의 ASSB 열은 투영(무인용 5 항목),
   LCOS 는 입력 미공개(G1), `<5 MPa` 는 출처 미명시(G3), Fig. 2 의 다섯 창은 `[도표]` 이고
   산정 규칙 0(G8). "이 지면에 이렇게 적혀 있다" 까지만.

### 새 제약 (2026-09-22, Oh 2025 — 열역학 도함수 진단이 들어오면서 붙은 것)

1. ★★ **접촉 손실 → 용량 사상을 문턱형으로 적는다.** 4호(면적 10.4 % ↔ 60 %p)와 14호
   (void 2 배 ↔ 용량 불변)가 같은 사상의 **양 끝**이다. 우리 3 항의 `θ_AM` 은 void 분율의
   함수가 아니라 **퍼콜레이션의 함수**이고, 문턱 아래에서 OCV 적합은 `LAM_PE ≈ 0` 을
   보고하면서 void 성장을 **놓친다**(오독이 아니라 무감). 분리 시험을 설계할 때 **문턱
   위·아래 두 표본**이 필요하다.
2. ★★ **관측 추가 후보를 volumetry 로 등록한다 — 단, 상수가 아니라 곡선으로.** `dE/dP` 는
   압력 구간에 2 배(D4), SOC 에 미지(D7)로 의존한다. 근최적 폭 측정에 넣을 때는 `E(P, x)`
   면을 먼저 모델링하고, 선형 `ΔV` 상수를 쓰지 않는다. 소신호(ΔP = −5 MPa, 가역)와
   대신호(`P↑` 300 MPa, 비가역)를 **다른 연산자**로 적는다
   ([[assb-pressure-reapplication-separation-test]]).
3. ★ **엔트로피메트리를 분리 관측으로 쓰지 않는다.** 균일 `LAM_PE` 와 완전 고립 접촉
   손실은 둘 다 아핀이라 ΔS(x) 모양이 안 바뀐다(`[해석]`). 대신 **아핀 전제의 검사**로
   쓴다 — `E(x)` 와 `∂E/∂T(x)` 가 같은 (α, β) 로 재조정되는가 ([[halfcell-ocp-shape-invariance]]).
4. ★ **sum rule 을 검사 항목으로 둔다.** `∫(dS/dx)dx` 는 상태함수 차이 — 전·후가 다르면
   비균질이 아니라 재료·창·음극 변화다. 14호는 그 뺄셈을 안 했고(7호·11호와 같은 형태),
   우리가 그림에서 할 수 있다.
5. ⚠ **비파괴 진단의 라벨에도 문턱값 0 이다.** reuse/recondition/recycle 의 수치 기준이
   없고 논문 스스로 "many cells … currently difficult" 라 적는다 — 14호의 등급을 Q3 의
   measured 라벨로 옮기지 않는다.

## Status Log

- **2026-09-16 (개설)** — 카드 생성. `assb` 섹션의 닻으로 지정. 보류 항목.
- **2026-09-16 (ingest 1)** — `assb` 1호 논문 흡수:
  `raw/papers/bielefeld2019_microstructural-modeling-assb-composite-cathode.md`.
  컴파일: [[composite-cathode-percolation-utilization]].
  **미결 항목 1 의 "형태" 가 정해졌고 "동역학" 이 남았다.** Q1~Q8 채움표 개설 (1.5/8).
  후속 후보 1 순위 = Strauss et al. 2018 (ref 13, measured `1 − θ_AM`),
  2 순위 = Koerver et al. 2017 (ref 7, 접촉 손실의 실험 원전 + 용량축).
- **2026-09-16 (ingest 2)** — `assb` 2호 논문 흡수:
  `raw/papers/clausnitzer2023_optimizing-composite-cathode-structure-resolved.md`
  (Clausnitzer et al., *Batteries & Supercaps* 2023, 6, e202300167; 본문 16쪽 + SI 10쪽,
  둘 다 sha256 봉인). 컴파일: 새 개념 [[assb-apparent-capacity-decomposition]] +
  [[composite-cathode-percolation-utilization]] 갱신(좌표 변환표 · 반례 · 산포 후퇴).
  **셋 중 하나가 들어왔다**: **전압축 ★있다**(`U₀ 4.2 V`·`U_cut 3.4 V`·Fig. S5 `V`–`Q`·
  `Wh/kg_cell`) / **동역학(시간축) 없다**(방전 1회, 사이클 0, 역학 0) /
  **시드 산포 없다**(오차막대 0, 점당 구조 1개 — 1호보다 **후퇴**).
  최대 수확은 **`θ` 만으로는 겉보기 용량을 설명 못 한다는 논문 내부 반례**와,
  그로부터 나온 **율 스윕 분리 시험**. Q1~Q8 채움표에 행 추가 (누적 ≈2.5/8).
  후속 후보 1 순위 = Ren/Danner/Finsterbusch/Latz et al. *Adv. Energy Mater.* 2022, 2201939
  (ref 17 — 이 논문이 열화·최적화 양쪽에서 가장 많이 인용, `θ(N)` 시간축의 입구),
  2 순위 = Neumann et al. *ACS AEM* 2021, 4, 4786 (ref 38 — GB 모형 원전 + EIS measured 라벨).
- **2026-09-16 (ingest 3)** — `assb` 3호 논문 흡수:
  `raw/papers/liu2024_grain-level-chemo-mechanics-composite-cathode-degradation.md`
  (Liu, Roters, Raabe, *Nat. Commun.* 2024, 15, 7970; 본문 18쪽 + SI 10쪽, 둘 다 sha256 봉인).
  컴파일: 새 개념 페이지 없음(SCHEMA Page Thresholds — 이 논문의 좌표는 `θ` 로 변환되지
  않아 기존 두 개념에 **제약**으로 붙는 편이 정확하다), 대신
  [[assb-apparent-capacity-decomposition]] 과 [[composite-cathode-percolation-utilization]]
  양쪽 갱신.
  **셋 중 하나만 들어왔다**: **OCV 곡선 ★있다**(SI Fig. S2, GITT, 3.0→4.4 V) ·
  **율 스윕 ★있다**(SI Fig. S4, 0.25–5C × 4 크기 = 20 곡선 — `i→0` 에서 전 크기 ≈1 로
  수렴, 3항 분해의 `η(i)→1` 이 독립 모델에서 확인됨) /
  **`θ(N)` 시간축 없다**(방전 1 회 + 충전 1 회, 사이클 축 0 장, **파괴·디본딩 모형 없음**) /
  **실험 없다**(자기 실험 0, 3/3 편 공통; 대조 자료는 **Si 음극·황화물 셀**(Fig. 4a)과
  **액체셀**(Fig. 5e)에서 왔다) / **시드 산포 없다**(실현 1 개 — "무작위 배열이 결정적"
  이라고 적고도).
  최대 수확 둘: ① `[인쇄]` **"실험의 활물질 손실은 rock-salt + 파괴로 고립된 활물질을
  둘 다 포함한다"** — 이 카드의 축퇴가 문헌 문장으로 확인됐다. ② **`Q_material` 이 율
  의존**이라 우리 율 스윕 분리 시험이 좁아졌다.
  어긋남 원장 **18 건**(1호 8 · 2호 14 · 3호 18), 그중 무거운 묶음은
  **D3·D4·D5·D6**(초록의 접촉 손실 인과 주장 ↔ 모델에 파괴 없음 · Fig. 5 의 손실 기준이
  자기 방전곡선과 화해 안 됨 · "kinetic capacity loss" 가 세 곳에서 다른 뜻 ·
  Fig. 7 의 "≥90 % usable capacity" 라벨이 자기 Fig. 5d 와 모순) —
  **결론을 떠받치는 문장이 자기 그림과 충돌하는** 2호와 같은 형태다.
  Q1~Q8 채움표에 행 추가 (누적 ≈3.0/8).
  후속 후보 1 순위 = **Koerver et al. *Chem. Mater.* 2017, 29, 5574** (3 편이 모두 인용;
  접촉 손실의 실험 원전 + 용량축 + 사이클 — **`θ(N)` 은 실험 쪽에서만 나온다**),
  2 순위 = **Shin et al. *Adv. Energy Mater.* 2023, 13, 2301220** (저압 조건 ASSB 열화 —
  **Q6 을 채울 첫 후보**).

- **2026-09-16 (ingest 4)** — `assb` 4호 논문 흡수:
  `raw/papers/shi2020_mechanical-degradation-assb-cathode.md`
  (Shi, Zhang, Tu, Wang, Scott, Ceder, *J. Mater. Chem. A* **8** (2020) 17399–17404,
  doi `10.1039/d0ta06985j`; 본문 6쪽 + ESI 7쪽, 둘 다 sha256 봉인).
  ⚠ **업로드 파일명이 서로 바뀌어 있었다** — `Sup_` 이 붙은 쪽이 본문이다 (digest 머리).
  컴파일: **새 개념 페이지 1**([[assb-pressure-reapplication-separation-test]]) +
  [[composite-cathode-percolation-utilization]] · [[assb-apparent-capacity-decomposition]]
  양쪽 갱신.
  ★★ **이 계보 첫 실험 논문이고, 한 편에서 세 칸을 깼다**:
  **Q2(자기 실험 — 3/3 편 연속 0 이던 칸)** · **Q6(압력 — 3/3 편 `pressure` 0 회였던 칸)** ·
  **Q8(실측 사이클별 V–Q — 3호의 OCV 는 타 논문 액체 반쪽전지 GITT 였다)**.
  그리고 Q1 을 **무차원 분율 + 시간축**으로, Q5 를 **부분**으로 열었다.
  Q1~Q8 채움표에 행 추가 (**4편 누적 ≈5.5/8**). **남은 0: Q4(유일성) · Q7(dead Li).**
  최대 수확 셋:
  ① ★★ **분리 연산자가 하나 더 생겼다** — 50 사이클 후 **300 MPa 재가압**으로 용량이
  `[도표]` ≈2 → `[인쇄]` **80 mAh g⁻¹** (`[재현]` **+60.5 %p**). 율이 `η(i)` 를 지우듯
  **압력이 `θ_AM` 을 되돌린다**. **OCV 밖의 축**이 열렸다.
  ② ★★ **곱셈 형태의 실측 반례** — 같은 시점 접촉 손실 **면적 10.4 %** 인데 압력
  가역분이 **60 %p**. **≈6 배.** 논문은 두 수를 **한 번도 비교하지 않는다**(D9).
  ③ ★★ **논문의 인과가 자기 EIS 와 충돌한다** — `[도표]` 50 사이클에서
  **음극 쪽 `R_LF ≈110 kΩ` 가 전체 저항의 ≈93 %**(양극 `R_MF` ≈3.3 kΩ, **33 배**),
  재가압 회복률도 **LF 65 % vs MF 23 %**. 그런데 초록·결론은 **양극 접촉 손실**로
  돌린다(D8). → **Q5(In 기준극 안정성)가 채워지면서 동시에 문제로 드러났다.**
  어긋남 원장 **18 건**(1호 8 · 2호 14 · 3호 18 · 4호 18), 무거운 묶음은
  **D8(인과 ↔ 자기 EIS) · D9(10.4 % ↔ 60 %p 무비교) · D10(라벨과 관측이 다른 셀 —
  토모그래피 3 셀의 용량이 한 번도 없다) · D12(검출 한계가 "후기에 몰린다" 결론을
  만들었을 수 있다)**. **2·3호와 같은 형태다 — 결론을 떠받치는 문장이 자기 그림과 충돌.**
  그 밖: 전압창이 본문 `1.4–3.7 V vs In` ↔ ESI `2–3.7 V vs In` 로 다르고(D1, 그림이
  본문 편), 본문이 Fig. 1 (c)/(d) 를 바꿔 쓰고(D2), 급락 후 값을 "<20 mAh g⁻¹" 로
  적지만 `[도표]` 실제는 **≈2**(D3), 재구성 부피가 캡션의 "all 60×40×30 µm³" 와
  **하나도 안 맞고 pristine 이 0.62 배**(D4), 재가압 후 **재감쇠(80→≈64)를 언급하지
  않는다**(D17), 압력값이 **전부 ESI 에만** 있다(D16).
  그림: 크로핑 6 장 **전부 열람**. ⚠ ESI **Fig. S3** 은 캡션 줄바꿈(`Fi`/`gure S3.`)
  때문에 크로핑되지 않아 **보지 못했다** (Weka 분할 워크플로, 정확도 수치 없음).
  후속 후보: 1 순위 **Koerver 2017** (`Chem. Mater.` 29, 5574 — `assb` 1·2·3·4 호가
  모두 인용; 4호가 `θ(N)` 3 점을 줬지만 **용량과 같은 셀에서** 주지 못했다),
  2 순위 **Koerver 2018** (`EES` 11, 2142 — ASSB 화학역학 종설 + **스택 압력 스윕**,
  Q6 을 스윕으로 채울 후보), 3 순위 **Neumann/Danner/Latz 2020** (`ACS AMI` 12, 9277 —
  **4호의 실측 기하를 2호 계보 전방 모형에 꽂는 다리**),
  4 순위 **Zhang/Scott/Ceder 2020** (`AEM` 1903778 — 같은 저자의 **LZO 코팅 불안정성**,
  4호가 정량하지 않고 남긴 화학 열화 몫).

- **2026-09-16 (ingest 5)** — `assb` 5호 논문 흡수:
  `raw/papers/doux2020_stack-pressure-room-temperature-assb-li-metal.md`
  (Doux, Nguyen, Tan, Banerjee, Wang, Wu, Jo, Yang, **Meng**, *Adv. Energy Mater.*
  **10** (2020) 1903253, doi `10.1002/aenm.201903253`, UCSD; 본문 6 쪽 + SI 8 쪽,
  **둘 다 sha256 봉인**). ✅ **업로드 파일명이 이번에는 내용과 맞다** (4호의 뒤바뀜 사고
  재발 없음 — 쪽수·첫 줄로 확인).
  컴파일: **새 개념 페이지 1**([[assb-stack-pressure-operating-window]]) +
  [[assb-pressure-reapplication-separation-test]] 갱신.
  ⚠ [[composite-cathode-percolation-utilization]] 은 **일부러 건드리지 않았다** —
  이 논문은 **음극 축**이고 그 페이지는 이미 **320 줄**로 SCHEMA 200 줄 권고를 넘겼다
  (분할 제안은 사용자 판단 대기).
  ★★ **이 편의 일**: 4호가 **점**으로 준 압력을 **곡선**으로 바꿨다 —
  **P→임피던스 6 점 · P→단락시간 6 점 · P→과전압 5 점**, 그리고 압력을
  **로드셀로 실계측한 첫 편**(0–220 MPa, Instron 교정).
  Q1~Q8 채움표에 행 추가 (**5편 누적 ≈6.5/8**). **남은 0: Q4(유일성) 하나뿐.**
  최대 수확 넷:
  ① ★★★ **상한이 숫자로 들어왔다** — `[인쇄]` **75 MPa 는 도금 전에 이미 기계적으로
  단락**하고 25 MPa 는 48 h. **4호의 300 MPa 재가압은 이 상한의 4 배**다.
  ⚠ 모집단 차이(4호 In 음극 ↔ 5호 Li 금속) → **상한은 음극 재료의 함수**.
  ② ★★ **회복의 전극 귀속이 갈렸다** — 5호 Fig. 4c 셀은 **양극이 없는 대칭셀**인데
  압력이 임피던스를 **>15 배** 움직인다. 4호의 `R_LF` 65 % vs `R_MF` 23 % 와 같은 방향
  → **`ΔQ_mech` 를 양극 `θ_AM` 회복으로 읽으면 과대.**
  ③ ★★ **이력** — 처녀 5 MPa 110 Ω ↔ 25 MPa 경유 후 5 MPa ≈50 Ω (`[재현]` 계면 과잉의
  **77 % 영구 제거**) → **`θ(P)` 는 함수가 아니라 경로 의존 상태다.**
  ④ ★ **Q7 이 절반 깨졌다** — SEI 는 XRD 로 **상(相) 검출**(Li₂S·LiCl·P₄·Li₃P₇),
  **dead Li 는 검출 수단이 없다**(`[인쇄]` Li 금속은 XRD 로 안 보이고 토모는 밀도
  대비뿐). 그리고 Table S2 가 **이 계보 첫 반복 측정**(펠릿 4 개 상대밀도)이다.
  어긋남 원장 **20 건**(1호 8 · 2호 14 · 3호 18 · 4호 18 · **5호 20**), 무거운 묶음은
  **D1–D6**: `[인쇄]` "과전압이 전 과정 일정했다 → 계면이 안정하다" 가 **자기 SI
  Fig. S4 다섯 패널 전부에서 8–28 % 증가**로 반증되고(D1), 본문이 **Fig. S5 를
  "1000 h" 의 근거로 인용하는데 Fig. S5 는 92 h 다**(D2), **Fig. S2·S3·S4 를 본문이
  한 번도 인용하지 않으며**(D3) 그중 **Fig. S3 은 Methods 에도 없는 2 MPa 조건**이라
  결론의 "optimal 5 MPa" 에 **하한 탐색이 없다**(D4), **Fig. S2 는 단락 28 h 전에
  임피던스가 −16 % 떨어지는 전조**인데 해석되지 않고(D5), **"덴드라이트" 동정에
  독립 근거가 없다**(D6 — `[인쇄]` Li 는 XRD 로 안 보이고, 같은 저밀도 대비를
  Fig. S6 에서는 "severe cracking" 이라 부른다).
  → **2·3·4 호와 같은 형태이되 새 변종이다: 인용조차 되지 않은 SI 가 본문을 반증한다.**
  그림: 크로핑 13 장(그림 11 + 표 2) 중 **그림 11 장 전부 열람**, 표 2 장은
  도구 권고대로 PDF 텍스트로 읽었다.
  후속 후보: 1 순위 **Koerver 2017** (`Chem. Mater.` 29, 5574 — `assb` 1–4 호가 모두
  인용, 접촉 손실의 실험 원전 + 용량축 + 사이클),
  2 순위 **inbox 의 15번** (*Elucidating the Influence of Stack Pressure on Anode and
  Cathode Impedance of All-Solid-State Batteries via Three-Electrode Measurements* —
  ★ **이 ingest 가 남긴 정확히 그 공백**(전극 분해 + 압력)을 겨냥한다),
  3 순위 **inbox 의 24번** (*Tailored Cathode Composite Microstructure Enables Long
  Cycle Life at **Low Pressure*** — 압력 창의 아래 벽),
  4 순위 **Kasemchainan 2019** (`Nat. Mater.` 18, 1105 — 탈리 void·임계전류밀도,
  5호가 "우리는 void 가 없다" 고 반박한 상대 논문).

- **2026-09-16 (ingest 6)** — `assb` 6호 논문 흡수:
  `raw/papers/lee2020_ag-c-anode-free-assb.md`
  (Lee, Fujiki, Jung, Suzuki, Yashiro, Omoda, Ko, Shiratsuchi, Sugimoto, Ryu, Ku,
  Watanabe, Park, **Aihara**, **Im**, Han, *Nature Energy* **5** (2020) 299–308,
  doi `10.1038/s41560-020-0575-z`, **SAIT + Samsung R&D Japan**; 본문 10 쪽 + SI 18 쪽,
  **둘 다 sha256 봉인**). ✅ **업로드 파일명이 내용과 맞다** (4호의 뒤바뀜 재발 없음 —
  쪽수와 첫 쪽 텍스트로 확인; SI 1 쪽에 `SUPPLEMENTARY INFORMATION / … unedited.`).
  컴파일: **새 개념 페이지 1**([[anode-free-li-inventory-accounting]]) +
  [[assb-stack-pressure-operating-window]] · [[assb-apparent-capacity-decomposition]] ·
  [[assb-pressure-reapplication-separation-test]] 갱신.
  ⚠ [[composite-cathode-percolation-utilization]] 은 **일부러 건드리지 않았다** —
  지시이기도 하고(이미 320 줄), 내용상으로도 이 논문은 **양극 `θ` 에 대해 아무것도
  주지 않는다**(Q1 = 없다).
  ★★ **이 편이 계보에서 처음인 것 셋**: **무음극(anode-free)** · **산업체 논문**
  (저자 16 명 전원 삼성) · **Ah 급 파우치 셀**.
  Q1~Q8 채움표에 행 추가 (**6편 누적 ≈7.0/8**). **남은 0: Q1(양극 접촉 손실 정량) ·
  Q4(유일성).**
  최대 수확 넷:
  ① ★★★ **`LLI` 추정자의 분해능이 새 전선이 됐다** — 같은 논문 안에서 **20 mAh 셀은
  CE(99.97 %)와 유지율(92.5 %@300)이 맞고 0.6 Ah 셀은 10 배 어긋난다**
  (`[도표]` CE 99.89 % ⇒ 누적 결손 `[재현]` **161 mAh g⁻¹** ↔ 실측 손실 **16**,
  양극 재고 **215**). **CE 축의 눈금조차 다르다**(95–101 vs 99.4–100.0).
  논문은 두 셀을 **한 번도 비교하지 않는다.**
  ② ★★★ **압력이 두 축으로 갈렸다** — **제작 490 MPa 등방(WIP, 비가역: Table S2 에서
  7 일 무압 복원 +0.8 µm)** vs **운전 2 MPa**. `[도표]` **무압 0.1 C 가 2 MPa 와 구별
  안 된다** → 5호의 "압력이 계면을 만든다" 와 모순이 아니라 **제작 압력 이력이 다르다.**
  ⚠ 운전 상한 `[인쇄]` **">4 MPa 단락 확률 증가" 는 데이터 0**.
  ③ ★★ **Q7 에 채널 둘 추가, 정량 0** — **EELS Li 맵**(방전 후·100 사이클 후에도
  Li 망 잔존)과 **XRD 의 Li₉Ag₄**(Li 저장 상 동정, 가역). **dead Li 만 여전히 수단
  없음**이고, `[인쇄]` "isolated lithium" 을 기구로 지목하고 **안 잰다.**
  ④ ★★ **"무음극은 OCP 평탄" 이 앞 10–17 % 구간에서 거짓** (Fig. 4a + SI Fig. 4c:
  음극 전위가 ≈1 → 0 V) → ASSB 인수인계 노트 §1 의 3 파라미터 창 모형은
  **3.6 V 위에서만** 성립한다.
  어긋남 원장 **14 건**(1호 8 · 2호 14 · 3호 18 · 4호 18 · 5호 20 · **6호 14**).
  ⚠ **2–5 호보다 적고 가볍다** — *Nature Energy* 의 편집 품질이 보이고, 5호의 변종
  (**인용조차 안 된 SI 가 본문을 반증**)은 **여기 없다**(모든 SI 그림이 본문에서
  인용된다). 무거운 것은 넷: **D2**(CE ↔ 유지율 10 배, 위 ①) · **D1**(초록·라벨
  ">99.8 % CE" ↔ `[도표]` **900–1000 사이클 구간 중앙값 99.21 % · 최저 97.42 %**,
  언급 0) · **D3**(">4 MPa 단락" 에 데이터 0) · **D6**(`[인쇄]` "no residual Li
  deposits … were found" ↔ `[도표]` Fig. 5i·5l 의 **EELS Li 망 잔존**).
  그 밖: 운전 압력이 세 곳에서 2–4 / 2 / 2 MPa(D4), C 단독 율특성이 SI 안에서
  75 % ↔ ≈92 %(D5), C 의 전기화학 활성에 대한 두 문장 충돌(D5-b), 에너지밀도 두께
  예산 594 µm ↔ 실측 609.0 µm 이고 **Ag–C 층이 표에 없다**(D7), 도금 Li 두께–전하량
  수지가 **110/82/76 % 로 비단조**(D10), 초록의 ">900 Wh l⁻¹" 와 "1,000 cycles" 가
  **다른 셀**(D13).
  그림: 크로핑 **26 장**(본문 5 + SI 18 + 표 3) 중 **그림 12 장 열람**, 표 3 장은
  도구 권고대로 PDF 텍스트로 읽었다. ⚠ **Fig. 6 은 크로퍼가 "영역 없음" 으로
  제외**해서 `pymupdf` 로 8 쪽을 직접 렌더해 봤고, **Fig. S10(WIP 전후 SEM)은
  크로퍼가 "그래픽 없음" 으로 제외했고 열지 않았다** — 그래서 Q1 판정은 Table S2
  수치와 본문 서술에만 근거한다.
  ★ Fig. 6g 와 SI Fig. 16 은 **PDF 텍스트층의 축 눈금 좌표로 축을 교정한 뒤** 화소를
  읽었고, 교정을 **논문 인쇄값(600 사이클 95 % · 1000 사이클 89 %)으로 검증**했다.
  후속 후보: 1 순위 **Koerver 2017** (`Chem. Mater.` 29, 5574 — `assb` 1–5 호가 모두
  인용하고 **6호도 ref 38 로 인용**한다; Q1 의 실험 원전이고 **여섯 편이 모두 안 준
  것**이 이것 하나다), 2 순위 **inbox 의 15번** (*… Stack Pressure on Anode and
  Cathode Impedance … via Three-Electrode Measurements* — 6호가 남긴 **전극 귀속**
  공백 정조준), 3 순위 **Genovese/Louli/Weber/Hames/Dahn 2018** (`JES` 165, A3321 —
  6호 ref 23, ***무음극 셀의 CE 측정법 그 자체***; 위 ① 의 분해능 문제를 직격한다),
  4 순위 **Zhang et al. 2017** (`JMCA` 5, 9929 — 6호 ref 46, **운전 중 압력 변화
  실측**; G12(정압인가 정변위인가)의 답이 여기 있을 수 있다).

- **2026-09-16 (ingest 7)** — `assb` 7호 논문 흡수:
  `raw/papers/spencerjolly2023_ag-graphite-interlayer-structural-changes.md`
  (Spencer-Jolly, Agarwal, Doerrer, Hu, Zhang, Melvin, Gao, Gao, Adamson, Magdysyuk,
  Grant, House, **Bruce**, *Joule* **7** (2023) 503–514, doi
  `10.1016/j.joule.2023.02.001`, **University of Oxford + Diamond Light Source**;
  본문 13 쪽 + SI 6 쪽, **둘 다 sha256 봉인**).
  ✅ 업로드 파일명이 내용과 맞다 (쪽수·1 쪽 텍스트로 확인). ⚠ 같은 업로드의
  `Sup1_` (2 쪽, *Standardized data reporting for batteries* **제출 양식**)은
  사용자 지시대로 **읽지 않았고 근거에 없다.**
  컴파일: **새 개념 페이지 1**([[ag-c-interlayer-lithium-phase-path]]) +
  [[anode-free-li-inventory-accounting]] · [[assb-apparent-capacity-decomposition]] ·
  [[assb-stack-pressure-operating-window]] · [[halfcell-ocp-shape-invariance]] 갱신.
  ⚠ [[composite-cathode-percolation-utilization]] 은 **일부러 건드리지 않았다** —
  지시이기도 하고(이미 339 줄), 내용상으로도 이 논문은 **양극에 아무것도 주지 않는다**.
  ★★ **이 편이 계보에서 처음인 것 셋**: **operando 회절**(실험실 + 싱크로트론) ·
  **6호의 외부 검증**(삼성 논문을 학계가 다시 잰 첫 편) · **원자료 공개**
  (Oxford Research Archive).
  Q1~Q8 채움표에 행 추가 (**7편 누적 ≈7.0/8 — 칸은 안 늘었다**).
  **남은 0: Q1(양극 접촉 손실 정량) · Q4(유일성).** Q6 은 6호 대비 **후퇴**.
  최대 수확 넷:
  ① ★★★ **dead Li 가 처음으로 숫자가 될 수 있게 됐다** — `[도표]` 충전 67.6 h ·
  방전 35.0 h (둘 다 30 µA cm⁻²) ⇒ `[재현]` **2.03 ↔ 1.05 mAh cm⁻², 효율 ≈52 %**,
  SEI 구간 0.19 를 빼면 **≈0.79 mAh cm⁻² = 통과 전하의 39 %** 가 설명되지 않는다.
  방전 종료 회절에 `[인쇄]` "only graphite and Ag" 만 남으므로 층 내부 Li 는 전부
  돌아왔다. ⚠ **논문은 이 뺄셈을 하지 않는다** (`Coulombic`·`efficiency`·`dead`·
  `isolated` **전수 0 회**). ⚠ **SEI ↔ dead Li 는 여전히 안 갈린다.**
  ② ★★★ **음극 OCP 가 충전과 방전에서 다른 곡선이다** — `[인쇄]` 충전에 없는 상
  (LiAg 의 **UPb 다형**)이 방전에 나타나고, 논문이 그것을 **열역학적 안정성**으로
  설명한다. 율은 ≈**C/68**·상온 → **`i→0` 으로 지울 수 없는 이력**이다.
  → [[halfcell-ocp-shape-invariance]] 의 두 번째 파괴 방식이고 **한 사이클 안**이다.
  ③ ★★ **6호의 "Ag 는 돌아오지 않는다" 에 대한 답** — `[도표]` Fig. 6 D→E→F 와
  SI Fig. S4: 충전에 **Ag 가 층 밖으로 나가 집전체 계면의 균일막**이 되고 방전에
  **다시 층 안 불연속 군집**으로 돌아온다(`[인쇄]` "near-pristine").
  **모순이 아니라 시간척도가 다르다** (7호 1 사이클 ↔ 6호 100 사이클).
  ⚠ **사이클당 잔류는 여전히 아무도 안 쟀다.**
  ④ ★★ **Ag 는 임계전류를 못 올린다** — `[인쇄]` 흑연 단독과 **같은 failure point**
  (둘 다 2.0 안정 / **2.5 mA cm⁻² 단락**). ⚠ **흑연 계의 판정**이고 6호는 카본블랙
  으로 3.2 mA cm⁻² × 1000 사이클이다 → **모집단 경계 넷**(탄소·상대극·사이클 수·
  제작 압력 방식)을 digest §15 에 표로 박아 두었다.
  어긋남 원장 **13 건**(1호 8 · 2호 14 · 3호 18 · 4호 18 · 5호 20 · 6호 14 · **7호 13**).
  ★ **이 계보에서 가장 적다** — `[해석]` 1 사이클·반쪽전지라 주장 표면적이 작고,
  **초록이 자기 결과보다 세게 말하지 않는다**(2–5 호의 지배 패턴이 없다).
  무거운 넷: **D2**(`[인쇄]` Ag 합금 예산 **0.60 mAh cm⁻²** ↔ `[재현]` 자기 조성으로
  **0.25**, ≈2.4 배) · **D3**(**첫 사이클 효율을 한 번도 안 적는다**) ·
  **D4**(**비가역분 39 % 의 행방을 계산하지 않으면서** 결론에서는 "Li 가 남는다" 고
  적는다) · **D8**(Fig. 6(0.1 mA cm⁻²·60 °C)의 Ag 를 **Fig. 1(30 µA cm⁻²·상온)** 의
  상으로 귀속 — 같은 논문이 "율이 오르면 Li–Ag 반응이 뒤처진다" 를 보였는데도;
  게다가 **Fig. 6 의 조건이 Methods 두 범주 어디에도 없다**).
  그 밖: Fig. 3(방전) 캡션이 "**charging** profile"(D1), Fig. 1 의 **Li 막대 시작
  시점에 근거 없음**(D5), SI Fig. S2a 의 **Li 피크가 잡음 대비 2–3 배**(D6),
  **집전체가 실험마다 Cu ↔ SUS**(D9), `[인쇄]` "Fig. S1 에 Ag 합금 전압 특징 없음"
  ↔ `[도표]` **어깨가 있다**(D10), 캡션 "≈0 V 로 급락" ↔ `[도표]` **−0.5 ~ −0.9 V
  톱니**(D11).
  그림: 크로핑 **11 장 전부 열람** (본문 6 + SI 5). ✅ **6호에서 있었던 "크로퍼가
  핵심 그림 제외" 사고 없음** — 제외된 그림 0 장.
  ★ Fig. 1·3 의 **상 막대와 시간축**, Fig. 4 의 **전압축**은 400 dpi 재렌더 +
  **화소 좌표 판독**으로 읽었고, 시간축 교정을 **인쇄값(2 mA h cm⁻²)으로 검증**했다.
  ⚠ **Methods 는 260 dpi 로 직접 렌더해 읽었다** — 본문 PDF 폰트가 **µ 를 전부
  떨어뜨려**(`30 µA cm⁻²`→`30 mA cm⁻²`, `5 µm`→`5 mm`) 텍스트 추출값을 쓰면
  **단위를 세 자리 틀린다.**
  후속 후보: 1 순위 **Koerver 2017** (`Chem. Mater.` 29, 5574 — `assb` 1–6 호가 모두
  인용; Q1 의 실험 원전이고 **일곱 편이 모두 안 준 것**이 이것 하나다),
  2 순위 **Gao/…/Bruce 2022** (`Joule` 6, 636 — **7호 ref 44, 같은 그룹의 "저압에서
  작동하는 복합양극"**; 7호가 `[인쇄]` 스스로 "양극은 다루지 않았다" 고 가리킨 곳이고
  **Q1 과 Q6 을 동시에 칠 수 있다**),
  3 순위 **inbox 의 15번** (3전극 + 압력 — 6호·7호가 남긴 **전극 귀속** 공백),
  4 순위 **Kasemchainan 2019** (`Nat. Mater.` 18, 1105 — 7호 ref 49, **상대극 void
  형성**; 7호가 "5 mm Li 상대극으로 그 기여를 줄였다" 고 적은 근거의 원전이고,
  §7 전하 수지의 **상대극 쪽 오차원**이 거기 있다).

- **2026-09-22 (ingest 8)** — `assb` 8호 자료 흡수:
  `raw/papers/li2026_safety-aware-bms-active-intelligence.md`
  (Li F, Li Y, Wu W, Qiao H, Jiang L, *Frontiers in Chemistry* **14** (2026) 1960882,
  doi `10.3389/fchem.2026.1960882`, **TYPE: Mini Review**, Shandong Huayu University of
  Technology; 본문 **12 쪽**, SI 없음, **sha256 봉인**
  `a54b551671eea230…`). ✅ 업로드 파일이 지정과 일치 (쪽수·sha256·DOI 확인).
  ★★ **큐에서 처음으로 성격이 다른 자료다** — 1–7 호는 ASSB 미세구조·계면·전극
  논문(시뮬레이션 3 + 실험 4)이었고, 8호는 **BMS·진단 종설**이며 **ASSB 는 12 쪽 중
  한 문단(§6.1)** 에만 나온다.
  ⚠⚠ **Mini Review 다 — 1 차 측정이 0 이고 모든 수치가 재인용이다.**
  digest 머리와 채움표 행에 그 사실을 박아 두었다.
  컴파일: **새 개념 페이지 없음** (SCHEMA Page Thresholds — 1 차 근거가 없어 개념
  페이지를 세울 재료가 안 된다). 대신 **이 카드에 채움표 행 + Evidence 1 절 +
  새 제약 1 절**, 그리고 [[assb-stack-pressure-operating-window]] 에 산업 요구치
  한 줄. ⚠ [[composite-cathode-percolation-utilization]] 은 **건드리지 않았다**
  (339 줄, 분할 대기 — 지시이기도 하고 내용상으로도 8호는 `θ` 에 아무것도 안 준다).
  Q1~Q8 채움표에 행 추가 (**8편 누적 ≈7.0/8 — 칸은 안 늘었다**).
  **남은 0: Q1(양극 접촉 손실 정량) · Q4(유일성).**
  최대 수확 넷:
  ① ★★★ **이 카드의 질문이 BMS 요구 사항으로 인쇄됐다** — `[인쇄]` §6.1
  "diagnostics capable of **distinguishing contact loss from ordinary electrochemical
  aging**". 3호가 **축퇴의 존재**를 인쇄로 확인했다면 8호는 **그것을 가르는 진단의
  필요**를 인쇄로 요구한다. ⚠ 정량 0, 그 요구가 매단 인용 1 편도 종설.
  ② ★★ **Q4 의 성질이 바뀌었다** — `identifiab*` **5 회**(1–7 호는 전부 0 회)이고
  **Table 4 의 중기 실패 모드에 "Unidentifiable pulse response"** 가 항목으로 있다.
  `[인쇄]` §2 "Parameter identifiability … can make a detailed model **appear more
  precise than the available measurements justify**" 는 우리 논지 그대로다.
  ⚠⚠ **그래도 측정은 0** — 조건수·프로파일 가능도·근최적 폭·CRB 전부 없다.
  **Q4 는 8/8 편 0.**
  ③ ★★ **세 번째 "비어 있음" 원장** — `[재현]` Table 2 8 편에서 **보정된 불확실성
  0 / 8**, `Cell` 검증 **7 / 8**. 액체셀 17/17(유일성 0) · `assb` 7/7(오차막대 0) 과
  **같은 방향**이다. ⚠ 리뷰의 분류를 우리가 센 것이고 원전 대조는 0 이다.
  ④ ★★ **압력 창의 아래 벽** — `[인쇄]` "industrial requirements **below approximately
  1 MPa**"(Xu 2024 재인용). `[재현]` `MPa` 가 12 쪽에 **1 회**이고 그 값이 1 이다 —
  **우리가 읽어 온 실험실 창(2–490 MPa) 전체가 그 위에 있다.**
  ★ **그리고 우리 폭 측정기의 소비처가 그려져 있다** — `[도표]` Fig. 2 의
  `I_cmd = min(…, **I_uncertainty**)` 인데 **계산법이 논문에 없다**(G1) →
  [[near-optimal-set-width-measurement]] 가 들어갈 빈칸.
  어긋남 원장 **10 건**(1호 8 · 2호 14 · 3호 18 · 4호 18 · 5호 20 · 6호 14 · 7호 13 ·
  **8호 10**). ★ **형태가 다르다** — 자기 실험이 0 이므로 "결론이 자기 그림과 충돌"
  대신 **인용 어긋남**이 주종이다. 무거운 넷:
  **D1**(★★★ `[인쇄]` "SOH RMSE **≤0.873 %** in Su et al. (2024)" ↔ **우리가 가진
  원전**은 5 셀 **평균**이고 cell5 **1.607 %**, 게다가 같은 논문의 원시 EIS 0.573 %·
  8-D 0.672 % 가 **제안 feature 를 모든 지표에서 이긴다** — **리뷰가 과장을 `≤` 로
  굳혔다**) · **D2**(`poorly identifiable` 문장이 매단 인용이 **Si–C 음극 소재 종설**,
  *Front. Mech. Eng.* 12, 1860708 — 자매지 자기인용) ·
  **D3**(`[도표]` Fig. 2 가 "**lexicographic**" 이라 적고 **`min()`** 을 계산한다 —
  min 은 순서 불변이라 §4 의 5 단계 우선순위가 결과에 영향이 없다; **이 논문의 중심
  구조 주장이 자기 그림에 구현돼 있지 않다**) ·
  **D4**(`[인쇄]` §6.2 "safety supervisor **in Figure 1**" ↔ `[도표]` **Figure 1 에
  그 상자가 없다**; 초록의 "**layered** vehicle–edge–cloud" 도 그림엔 층이 없고
  **여섯 상자가 전부 대칭 양방향 화살표**다 — 본문이 반대한 바로 그 구조).
  그 밖: 심사 응답 문장이 게재본에 남아 있고(D5 — "the **reviewers' request**",
  "the **reviewer's example**", "**The uploaded** 2023 review"; `[인쇄]` Generative AI
  statement 로 **Figure 1 은 생성형 AI 제작**, 접수→게재 **39 일**),
  PyBaMM 인용의 학술지·권·쪽이 DOI 와 다른 출판물을 가리키고(D6, DOI 접두로 판단),
  `Liu et al. (2025)` 가 두 편인데 a/b 구분이 없으며(D7),
  **Birkl 2017 이 EIS/DRT 표에 붙어 있고 이 리뷰는 열화 모드를 한 번도 쓰지 않는다**
  (D8 — `LLI`·`LAM`·`degradation mode` 전수 0 회),
  Table 2 의 `Computational burden` 이 기준 없는 형용사이며(D9),
  자기 권고(팩 검증·보정 불확실성)를 만족하는 증거가 표 안에 **1 행 / 0 행**이다(D10).
  그림: 크로핑 **6 장**(fig 2 + tab 4) 중 **fig 2 장 전부 열람**, 표 4 장은 도구
  권고대로 PDF 텍스트로 읽었다 (Table 3 은 fig_2 크롭에 함께 들어와 **이미지로도
  이중 확인**). ✅ **크로퍼 누락 0** — `pymupdf` 로 센 PDF 내장 이미지 **2 개**와 일치.
  ✅ **µ 탈락 위험 없음** — 이 PDF 에는 `µ` 가 필요한 수치가 하나도 없고,
  `−20 °C to 60 °C`·`>120 titration points` 는 fig_2 크롭에서 눈으로 재확인했다.
  ★★★ **이 편의 실익은 수치가 아니라 원 논문 지도다** (digest §15). 후속 후보:
  1 순위 **Xu, Yang, Li 2024** (*Adv. Energy Mater.* **14**, 2303539, doi
  `10.1002/aenm.202303539` — `<1 MPa` 의 출처, **Q6**; ⚠ 그것도 종설),
  2 순위 **Zhang, Fu, Lu, Hu, Xia, Zhang et al. 2025** (*Adv. Mater.* **37**, 2413499,
  doi `10.1002/adma.202413499` — 저압 ASSB 전용, **Q6·Q1**; inbox **24번**과 짝),
  3 순위 **Biçer, Aksöz, Bakar, Odabaşı, Oyucu, Soares et al. 2025** (*Batteries*
  **11**, 212, doi `10.3390/batteries11060212` — "접촉 손실 ↔ 보통 노화 분리 진단"
  요구가 매단 **유일한** 인용, **Q1·Q2**),
  4 순위 **Liang, Tao, Shi, Lyu, Ji, Dong et al. 2026** (*npj Clean Energy* **2**, 16,
  doi `10.1038/s44406-026-00040-w` — **active pulse 원전**, 우리 폭 측정기의 역방향:
  "원하는 폭을 얻으려면 최소 어떤 여기가 필요한가", **Q4 설계 축**),
  5 순위 **LeBel, Messier, Sari, Trovão 2022** (*J. Energy Storage* **54**, 105303,
  doi `10.1016/j.est.2022.105303` — GITT OCV/동적 응답면 원전, `>120 titration
  points` × −20~60 °C, **Q3·Q8**),
  6 순위 **Roman, Saxena, Robu, Pecht, Flynn 2021** (*Nat. Mach. Intell.* **3**, 447,
  doi `10.1038/s42256-021-00312-3` — Table 2 **8 행 중 유일하게 신뢰구간을 보고**,
  **Q3**),
  7 순위 **Thelen, Huan, Paulson, Onori, Hu, Hu 2024** (*npj Mater. Sustain.* **2**, 14,
  doi `10.1038/s44296-024-00011-1` — 불확실성 **보정** 종설, **Q3·Q4**).
  ⚠ **1–3 순위가 전부 종설이다** — §6.1 은 **종설이 종설 셋을 인용한 문단**이고
  그 아래에 1 차 측정이 없다. **Q1 의 1 차 원전은 여전히 `assb` 1–7 호 쪽에 있고,
  닻의 오랜 1 순위 Koerver 2017 은 이 리뷰가 인용조차 하지 않는다**
  (참고문헌 48 편에 `Koerver` **0 회**).

- **2026-09-22 (ingest 9)** — `assb` 9호 논문 흡수:
  `raw/papers/huo2025_assb-cathode-lampe-coupled-aging-model.md`
  (Huo, Li, Fan, Zhang 외, *J. Power Sources* **627** (2025) 235830; 본문 11쪽 +
  **SI(.docx)**, sha256 봉인). 컴파일: **새 개념 페이지**
  [[assb-lampe-contact-product-degeneracy]].
  **Q1~Q8: 8편 ≈7.0 → 9편 누적 ≈7.5 칸.** 늘어난 것은 **Q6**(압력이 "점·스윕" 에서
  **연속 시계열**로) 반 칸과 **Q3 의 새 층위**(`fitted-single-parameter`)다.
  **Q1·Q4 의 0 은 9호도 못 채웠다** — 그러나 **Q4 의 성질이 세 번째로 바뀌었다**:
  안 쟀다(1–7호) → 이름이 로드맵의 실패 모드에 올랐다(8호) → **지문이 자기 표 안에
  있고 다르게 불린다(9호)**.
  ★★★ **이 편이 큐에서 우리 문제와 가장 가깝다.** 이 계보 최초로 **실험과 파라미터
  식별을 한 논문 안에서 잇고**, 그래서 처음으로 **열화 모드의 지분 자체를 적합으로
  정한다**. 그 절차를 다섯 축으로 캐물은 답: ① 식별 절차 = **1-파라미터 PSO**(`ε_p`
  하나), 정답축이 자기 방전곡선 ② 유일성 증거 **0** (`uncertaint*`·`identifiab*`·
  `sensitiv*`·`Fisher`·`condition number`·`bootstrap`·`multi-start`·`error bar`·
  `regulariz*` 전수 0회) ③ **여러 모드를 같이 놓고 지분을 비교한 적이 없다** —
  `LLI`·`LAM_NE` 는 모델에 **좌표가 없고** `ε_p` 하나만 푸므로 **잔차가 갈 곳이 하나**
  다 ④ fitting 밖의 독립 관측 **0건**(SEM 은 표면·정성, EIS 는 같은 역문제) ⑤ SOH
  "1 % 이내" 는 **훈련 잔차**이고 예측 오차가 아니다 — 대조군 **0건**, 08호의 Su 2024
  패턴과는 다르다(숫자는 정직하고 **설계**가 문제다).
  ★★ **가장 단단한 결과 둘**: (a) `A^p_eff · ε_p / R_s` **곱 축퇴를 인쇄된 식에서 손으로
  유도**했고 자기 SEM 이 `A_eff` 를 **9 배** 배반한다 (b) `[인쇄]` **"파라미터가 흔들려도
  적합이 잘 되니 괜찮다" 가 문자로 인쇄되어 있고**, 같은 논문이 그 명제의 **반례 셋**을
  자기 지면에 남긴다 (`R_SEI` **+37 %/−80 %** · 곱 축퇴 · `k_LAM` **2.15 배 vs 1 %**).
  어긋남 **9건**(D1~D9) + 공백 12건. 크로퍼가 **Fig. A.1(부록 DVA)을 빠뜨려** 수동으로
  뽑았다 (06호식 누락의 재발 — `fig_a1_manual.png`).
  후속 후보 1 순위 = 원전 **ref [27]**(같은 연구실 *eTransportation* 20, 100315 —
  모델·PSO·`A_eff` 정의를 전부 위임한 곳), 2 순위 = **ref [30] Conforto 2021**
  (9호 스스로 "정량한 몇 안 되는 문헌" 으로 지목하고 `[인쇄]` "오차가 비교적 크다" 로
  기각한다 — **그 오차의 크기를 우리가 직접 봐야 한다**, 방법이 **relaxed OCP + EIS-PSD**
  라 우리 축과 직결), 3 순위 = **ref [21] Yu 2024 DRT**(§5.1 의 병합 원호를 가르는 도구).

- **2026-09-22 (ingest 10)** — `assb` 10호 논문 흡수:
  `raw/papers/vadhva2021_eis-for-assb-theory-methods.md`
  (Vadhva, Hu, Johnson [3인 공동 1저자], Stocker, Braglia, Brett, **Rettie**(교신),
  *ChemElectroChem* **2021**, *8*, 1930–1947, doi `10.1002/celc.202100108`,
  **Reviews**, CC-BY open access; 본문 **18 쪽**, **SI 없음**(업로드 큐에 `10._Sup_*`
  부재 + 본문에 supporting/supplementary 0 회), sha256 봉인).
  소속: **UCL Electrochemical Innovation Lab** + **The Faraday Institution** +
  **HORIBA MIRA Ltd.**(기업 — Stocker·Braglia, 확인 완료).
  자금 **Faraday Institution LiSTAR** + **HORIBA-MIRA/UCL/EPSRC CASE studentship**.
  컴파일: **새 개념 페이지 없음** (이 논문의 명제는 기존 두 페이지의 같은 축이고,
  새로 만들면 "EIS 일반 설명" 으로 흐른다 — SCHEMA Page Thresholds). 대신
  [[assb-lampe-contact-product-degeneracy]] · [[fitting-degeneracy]] ·
  [[assb-stack-pressure-operating-window]] 보강.
  **Q1~Q8: 9편 ≈7.5 → 10편 누적 ≈8.0 칸.**
  ★★★ **`Q4` 의 0 이 처음으로 깨졌다 — 그리고 깬 방식이 중요하다.**
  **"우리 대신 쟀다" 가 아니다**(측정 0; `identifiab*`·`uncertaint*`·`confidence`·
  `condition number`·`error bar` **전수 0 회** — 10/10 편이 여전히 안 쟀다).
  **"축퇴가 일반 현상임을 방법론으로 인쇄했다"** 이다: `[인쇄]` "**no solution to an
  EIS spectrum is unique**" · "**the inclusion of more elements will tend to improve
  the fit**" · "how many time constants … **highly subjective**" · DRT 는
  **`ill-posed`, regularization 필요** · 모델 선택을 **AIC** 로 명명하고
  `[인쇄]` "**validation against experiment in the context of ASBs is desirable**"
  로 **열린 문제 등록**. ⇒ Q4 의 성질이 **네 번째로** 바뀌었다.
  ★★★ **9호 §5.1(하나의 원호에서 두 시상수)에 정식 근거를 준다** — 판정 5 문장 +
  처방 5 개(K–K/Lin-KK · DRT 로 개수 결정 · **저온·가압으로 시상수 벌리기** ·
  **대칭셀 쌍** · AIC). **9호는 그중 하나도 쓰지 않았다**(`Kramers`·`DRT`·
  `symmetric cell`·`AIC` 전수 0 회). `[재현]` 9호 회로의 자유 파라미터는 **9 개**
  (`R_b`1 + RQ3 + RQ3 + W2)이고 **원호는 1 개**다.
  ★★ **DRT 를 다룬다 — 그리고 비판적으로 다룬다**(`DRT` 13 회). 8호의 "ill-posed
  inversion needs regularization" 처방이 여기서 EIS 쪽 1차 진술로 확인되고,
  개선 경로 3 개(**일반화 DRT** Danzer / **Bayesian DRT** Huang / **2D DRT** Mertens)
  와 원전이 붙는다. ⚠ 자기 DRT 계산은 0(Fig. 6d 는 재인용).
  ★★ **새 명제 하나**: **"분해 가능한 RC 의 개수는 실험 조건의 함수다"** — 다섯 사례
  (황화물 5 중 3 만 입계 분해 · LGPS 실온 원호 0 개 · **400 MPa 에서 GB 등장** ·
  폴리머 60 °C 에서 상경계 소멸 · **노화가 RQ 를 3→4 로, 새 RQ 귀속은 `and/or`**).
  ★ **이 카드의 Q2 에 직격**: `[인쇄]` Fig. 9 본문이 **접촉 손실과 분해층 성장을
  한 `R_MF` 에 함께 귀속**한다 ⇒ **EIS 는 곱 축퇴를 깨는 대가로 새 축퇴를 들여온다.**
  어긋남 **6 건**(D1 위상각 식 역전 · D2 Eq.3 차원 불일치 · D3 "~10⁹ orders of
  magnitude" · D4 본문↔캡션 패널 글자 한 칸 어긋남 · D5 라운드로빈 인용 번호 오류
  [85]↔[191] · D6 저주파 인덕턴스에 두 이름) + 공백 8 건. **방법론적 주장 자체에는
  어긋남을 못 찾았다.**
  크로퍼: **15 장 = Fig. 1–14 + Table 1, 누락 0**(⚠ `fig_7.png`/`fig_8.png` 가 같은
  두 단 영역을 **중복** 크롭 — 누락은 아니다). **실제로 본 것 8 장**
  (Fig. 2·5·6·7·8·9·11·12) + 본문 4 곳 페이지 렌더(Eq. 3 · Eq. 5 · "10⁹" · `μAh`).
  ✅ **µ 탈락 없음** — 이 PDF 는 `μAh`·`μm` 를 정상 추출하고 렌더로 재확인했다.
  후속 후보 1 순위 = **ref [52] Ingdal, Johnsen, Harrington** *Electrochim. Acta*
  **2019**, *317*, 648–653 (**AIC 로 등가회로 순위 — Q4 의 계산기**),
  2 순위 = **ref [191] Ohno et al.** *ACS Energy Lett.* **2020** (라운드로빈 원전,
  **22 % / ~10 %** 의 출처 — D5 때문에 더더욱 필요, **Q3**),
  3 순위 = **ref [82] Bron, Dehnen, Roling** *J. Power Sources* **2016**, *329*, 530
  (저온으로 축퇴를 깨는 실물, **Q4·Q2**),
  4 순위 = **ref [97] Zhang, Weber, …, Zeier, Janek** *ACS AMI* **2017**, *9*, 17835
  (In\|LGPS\|LCO SoC 분해 EIS — **접촉 손실 + 분해층이 한 저항에 묶인 원전**,
  **Q1·Q2·Q5**; 4호의 `R_LF`/`R_MF` 해석을 검증할 유일한 편),
  5 순위 = **ref [28] Krauskopf et al.** *ACS AMI* **2019**, *11*, 14463 (**Q6**,
  압력 이력의 산화물 판),
  6 순위 = **ref [84] Doux et al.** *J. Mater. Chem. A* **2020**, *8*, 5049
  (우리 5호의 **자매 논문**, Li₆PS₅Cl σ 가 ~400 MPa 까지 증가, **Q6**),
  7 순위 = **ref [57] Kaiser et al.** *J. Power Sources* **2018**, *396*, 175
  (**TLM + 전자차단 대칭셀로 복합전극 이온 굴곡도 정량** — `θ_AM` 에 가장 가까운
  실측 채널, **Q1**),
  8 순위 = **ref [172] Huang, Papac, O'Hayre** *Electrochim. Acta* **2020**, *367*
  (**Bayesian DRT** — 봉우리에 사후분포를 붙이는 경로, 8호의 "calibrated
  uncertainty" 요구와 직결),
  9 순위 = **ref [73] Larfaillou et al.** *J. Power Sources* **2016**, *319*, 139
  (**노화가 RQ 를 3→4 로 바꾼다** — "모델 차수가 상태변수" 의 원전).
  도구 후보: **ref [43] Schönleber, Lin-KK**(KIT 2015).
  ⚠ **정정 하나**: ref [190] 의 **Bielefeld, Weber, Janek** *ACS AMI* **2020**, *12*,
  12821 은 우리 **1호(Bielefeld 2019, *J. Phys. Chem. C*)와 다른 논문**이다(후속).
- **2026-09-22 (ingest 11 — 큐 38번, 순서를 당겨서)** — `assb` 11호 흡수:
  `raw/papers/yu2024_drt-time-resolved-aging-sulfide-assb-fullcell.md`
  (Yu, Choi, Dunham, Ghahremani, Liu, Lindemann, Garver, Barchiesi, Farahati,
  Kim, *J. Power Sources* **597** (2024) 234116 — **Schaeffler Transmission
  Systems LLC**(산업체) + **Ohio State University**; 본문 8 쪽 + **SI `.docx`**
  7,607 자 + 그림 S1–S5, 본문·SI 둘 다 sha256 봉인).
  **10호(Vadhva) 와 짝으로 읽으려고 순서를 당겼다** — 10호가 DRT 를 `[인쇄]`
  "ill-posed … requiring regularization" 으로 판정하고 λ 선택 규칙을 공백(G4)으로
  남겼고, **11호가 그 DRT 를 실제로 돌린 첫 `assb` 논문**이기 때문이다.
  **그림 14 장 모두 등록 · 12 장 열람**(본문 Fig. 1–8 + SI Fig. S1–S5;
  Table 1 은 텍스트로). ★ **SI 가 `.docx` 라 크로퍼가 못 읽어 `zipfile` 로
  `word/media/image1–5.png` 를 직접 꺼냈다** — 텍스트만 긁었으면 §12(Fig. S2)·
  §13(Fig. S3)·§10(Fig. 1 = Fig. S3 동일 데이터)을 **통째로 놓쳤다.**
  **결과 여섯**:
  ① **`Q1` 이 반쯤 깨지고 `Q6` 의 마지막 빈칸(`압력 → 용량`)이 채워졌다**
     (누적 **≈8.5 / 8** 칸; 반쪽 3 점 165.0/166.9/**173.1**, 완전지 2 점 169.9/171.7).
  ② ★★★ **`Q4` 의 성질이 다섯 번째로 바뀌었다 — "잴 재료를 SI 에 인쇄하고
     뺄셈을 안 했다".** `[도표]` Fig. S3 가 **같은 셀에서 배선만 바꿔 DRT 봉우리를
     −15 % ~ +69 %** 움직이는데, 본문의 재가압 효과는 **−10 ~ −25 %** 로 그 폭
     **안**이다. **Q4 측정은 여전히 0 / 11.**
  ③ ★★★ **"모델 차수는 상태변수" 가 1 차 데이터로 네 번 확인됐다**
     (Fig. 2a 2–3→5 · Fig. 3c 1→2 · Fig. 6c P4 신생 · Fig. 7d 4→3 재가압).
     10호가 Larfaillou 재인용으로만 전한 것의 **직접 재현**.
  ④ ★★★ **`Q8` 이 이 카드의 출발 전제를 깼다** — **graphite 음극 완전지**라
     "전고체 음극은 평탄 → 5→3 붕괴" 가 성립하지 않는다 (9호 Li-Si 에 이은
     두 번째 반례, 이쪽은 상용 흑연).
  ⑤ ⚠ **압력 연산자가 직교하지 않는다** — 재가압이 P1·P2·P3·**P4(전하이동)** 를
     전부 10–27 % 줄인다 ⇒ [[assb-pressure-reapplication-separation-test]] 에
     반례 기록, `confidence: low` 유지.
  ⑥ **어긋남 18 건** (D1 전처리 이중 서술 · D2 P1 주파수 최대 2 자릿수 ·
     D3 "P3 만 줄었다" 가 그림에 없다 · D10 본문이 자기 Fig. 1 을 잘못 묘사 ·
     **D11 Fig. 1 은 "Illustration" 이 아니라 Fig. S3 하단의 실측** ·
     D13 DRT 봉우리가 측정 대역(0.1 Hz) 밖에 있다 …).
  컴파일: 새 개념 [[drt-peak-count-nonidentifiability]] +
  [[fitting-degeneracy]] Q4 계보 갱신 + [[assb-pressure-reapplication-separation-test]] 반례.
  후속 후보 1 순위 = **Wan, Saccoccio, Chen, Ciucci, DRTtools** (*Electrochim.
  Acta* 184 (2015) 483 — **λ 와 RBF shape factor 가 이 논문의 인터페이스**이고
  G1 을 닫는 유일한 경로), 2 순위 = **Hori, Kanno, …, Ivers-Tiffée** (*J. Power
  Sources* 556 (2023) 232450 — 같은 재료계 EIS–DRT, 봉우리 귀속의 외부 검증),
  3 순위 = **Danzer, generalized DRT** (*Batteries* 5 (2019) 53 — 10호가 지목하고
  11호가 **인용만 하고 안 쓴** 것), 4 순위 = **Illig 2012 + Schmidt 2011**
  (P3 = "solid-solid contact impedance" 귀속의 **원전**; 액체셀 LFP/Al 의
  주파수대를 황화물 복합양극에 이식한 것이 정당한지 확인해야 한다).
- **2026-09-22 (ingest 12)** — `assb` 12호 논문 흡수 (큐 11번 — 38·39 를 당겨 끝낸 뒤
  큐 순서로 복귀한 첫 편): `raw/papers/kouhestani2022_phm-solid-state-batteries-perspective.md`
  (Sadegh Kouhestani, Yi, Qi, Liu, Wang, Gao, Yu, Liu, *Energies* **15** (2022) 6599,
  doi `10.3390/en15186599`, MDPI CC BY; 본문 26 쪽, **SI 없음**, sha256 봉인).
  ⚠ **Review — 1차 측정 0. 그림 7 장 전부 타 논문 재수록**(LIB 6 + Palacín 2009 모식도 1)
  이라 **이 논문에는 SSB 데이터 그림이 0 장**이다. **그림 7 장 전부 열어 봤다**(Table 1 은
  텍스트로 전사). **결과 다섯**:
  ① **Q1~Q8 어느 칸에도 새 칸을 더하지 않는다** (누적 **≈8.5 / 8 유지**). Q4 는 **0 / 12**.
  ② ★★★ **분리 물음이 정의에서 지워진 자리를 찍었다** — `[인쇄]` "The loss of active
     materials **mainly stems from** the electrical contact loss" ⇒ PHM 어휘에서
     `LAM ⊃ 접촉 손실`. 기구 목록은 **전부 액체셀**, Fig. 6 의 "Contact Loss" 는 **집전체**.
  ③ ★★ **Q4 계보의 출발점을 날짜로 고정** — `identifiab*` **0**(8호는 5), 가장 가까운
     어휘가 "difficult parameter identification"(실무 곤란)이고, **같은 논문이 모델 차수에
     대해 정반대 두 문장**을 인쇄한다(§3.1.2 "inevitable errors in each parameter" ↔
     §3.1.3 "the more parameters … the higher the accuracy").
  ④ ★★ **`A_eff` 형 접촉 파라미터의 계보 입구** — `[인쇄]` Tian & Qi 2017 / Shao 2022
     "a parameter to describe the contact area, which adjusts the current density in the
     1-D Newman model" = 9호 `A^p_eff` 와 같은 형태. ⚠ 두 저자에 같은 번호 [60] → `0.4–1
     MPa` 출처 미확정(D4).
  ⑤ **Table 1 ("PHM techniques for SSB") 28 슬롯을 한 줄씩 대조**: SSB 실측 열화 데이터로
     SOH/RUL **0 / 28** (납축전지 ECM · 전방십자인대 예후 · 1976 kNN 이 들어 있다).
     논문 자신의 결론 (1)(2)와 일치.
  **어긋남 21 건**(D1 "LiCoO₂ or LTO" · D4 중복 [60] · D5 Deng [79] 이중 용도 · D6 "Song
  [29]" = Tian 종설 · **D7 §3.3.1/3.3.2 제목 뒤바뀜** · **D8 Table 1** · D9 ECM 식별법
  인용 4 건 전부 무관 · **D13 모델 차수 두 명제 충돌** · **D20 Fig. 5 `SOH = {FOI}` 벡터 ↔
  식 (6) 스칼라** …). 공백 10 건(G1~G10). 접수→승인 **9 일**.
  컴파일: **새 개념 페이지 없음**(이 편의 명제는 전부 기존 페이지의 같은 축이고 1차 내용이
  0 — SCHEMA Page Thresholds). 대신 이 카드(채움표 12행 + Evidence 아홉 번째 절 + 새 제약
  4 개 + 이 항목 + "주장하지 않는 것" 1 항) · [[assb-lampe-contact-product-degeneracy]]
  (`A_eff` 계보 절) · [[drt-peak-count-nonidentifiability]] ("원호 1→2" 세 번째 인쇄) ·
  [[fitting-degeneracy]] (Q4 계보에 2022 년 표본).
  8호와의 대조: **공통 원전 0 건**이라 "같은 원전을 다르게 적었는가" 는 수행 불가; 대신
  **같은 명제 둘(라벨 부재 · ≈1 MPa)이 다른 원전에서 독립적으로** 나왔다.
  후속 후보 1 순위 = **Tian & Qi, *J. Electrochem. Soc.* 2017, 164, E3512** (`A_eff` 원전
  후보), 2 순위 = **Shao et al., *Energy* 2022, 239, 121929** (접촉 면적 손실 + 압력 —
  Q1·Q6 동시, `0.4–1 MPa` 의 진짜 출처), 3 순위 = **Kim, Lin, … Chung, *Electrochim. Acta*
  2019, 317, 663** (Table 1 유일의 SSB 상태추정 — 관측 가능성을 다뤘는지; ⚠ 10호 후속
  1 순위 Ingdal 2019 와 같은 권), 4 순위 = **Schmidt, Bitzer, Imre, Guzzella, *JPS* 2010,
  195, 7634** (용량 손실 ↔ 율 특성 저하의 모델 기반 구분 — 우리 3항 분해의 액체셀 원형).

- **2026-09-22 (ingest 13)** — `assb` 13호 논문 흡수 (큐 12번):
  `raw/papers/zheng2026_assb-grid-realistic-appraisal.md` (Zheng, Xie, Zhang, Yang, Zhou, Zhu,
  *Energy* **345** (2026) 140229, doi `10.1016/j.energy.2026.140229`, Elsevier; 본문 10 쪽,
  **SI 없음**, sha256 봉인, PDF `496f3b4580a81b9b…` 실측 일치). 접수→승인 **51 일**.
  ⚠ **Perspective — 1차 측정 0, `[인쇄]` "No data was used", 그림 5 장 전부 모식도/레이더
  (데이터 그림 0 장).** **그림 5 장 전부 열어 봤다** (Table 1·2 는 텍스트 전사). 큐 등록 축은
  Q3·Q4 였으나 **실제 접점은 Q6·Q8** 로 판정. **결과 다섯**:
  ① **새 칸 0 (누적 ≈8.5 / 8 유지, Q4 0 / 13).** Q6·Q8 의 이미 채워진 칸에 **층**이 하나씩.
  ② ★★★ **접촉 손실이 SOH 정의에서 사라진 자리를 찍었다** — `[인쇄]` "distinguish between
     **true active material loss** and a reduction in 'useable capacity' caused by **rising
     impedance or increasing overpotentials**"(2 항) ↔ 같은 절 "dominant failure modes … the
     gradual **loss of interfacial contact**". 12호 `LAM ⊃ 접촉 손실`(흡수) · 13호 미배정(누락)
     · 우리 3 항 — **분류 셋이 전부 다르다.**
  ③ ★★ **운전 창이 OCV 채널을 설계상 닫는다** — `[인쇄]` "20–80 % SOC … impossible to obtain a
     full OCV curve" + LFP 평탄 + "voltage hysteresis arising from mechanical stresses"(인용 0).
     이 카드의 답에 **"완전 OCV 곡선 조건"** 을 붙이고 부분 창 폭을 별도로 낸다.
  ④ ★★ **Q6 — 요구치 세 번째 독립 인쇄 + 위 벽의 두 번째 형태**: `[인쇄]` `<5 MPa` ×2(1 차
     주장, 근거 [35]/[45], "5" 출처 미명시) · `[도표]` Fig. 2 클래스 창(Oxides ≥30 · Sulfides
     5–20 · Halides 2–10 · Polymers 0 · Composites 1–10 MPa — **본문에 없는 값**) · `[인쇄]`
     고정 고압 → creep/피로 미세균열(단락과 다른 시간 축) · `[인쇄]` 능동 응력 관리 정책
     (율↑→P↑, 휴지/노화→P↓) · 인과 `압력 감쇠 → 임피던스 ↑`.
  ⑤ ★ **Q4 성질 변화 — 이름 없이 역문제를 처방**: `[인쇄]` "inversely estimate the current
     state of interfacial contact and material properties", `identifiab*` 0. 8호와 같은 해.
  **어긋남 12 건**(D2 "45–55 %" ↔ 끝점 45.5/50 · **D3 Fig. 1 그리드 삼각 숫자 0 + EV CE
  99.98 % 는 10000 사이클에 13.5 %** · **D4 `<5 MPa` ↔ Fig. 2 권장 클래스 상단 10 MPa** ·
  **D5 Fig. 3 SSB BMS 온도 입력 없음 ↔ §4 열관리 필수** · D6 `j = 5 mA cm⁻²` ⇒ 로딩 ≈10 mAh
  cm⁻² 미기재 · D7 Table 2 열화 어휘 = 액체셀 · D8 Fig. 2 가 수명 축 제외 · D9/D10 인용 무관 ·
  D12 수명 목표 무인용). 공백 12 건(G1~G12). 자기 인용 6/56 — 권장 복합전해질의 유일한
  수치 예가 자기 논문 [29].
  컴파일: **새 개념 페이지 없음**(1 차 내용 0 · 명제 전부 기존 축 — SCHEMA Page Thresholds).
  이 카드(채움표 13행 + Evidence **열 번째** 절 + 새 제약 5 개 + 이 항목 + "주장하지 않는 것"
  1 항) · [[assb-stack-pressure-operating-window]] (요구치 계보 + 피로형 상한 + 제어 정책) ·
  [[assb-apparent-capacity-decomposition]] (2 항 이분법에서 `θ_AM` 이 빠진 자리) ·
  [[fitting-degeneracy]] (Q4 계보 2026 년 두 번째 표본 — 이름 없는 역추정 처방).
  12호와의 대조: **공통 원전 0 건**(12호의 Tian·Shao·Hu·Fathiannasab 가 13호에 없고 13호의
  Schmaltz·Albertus·Li Qianya·Gu·Pang 2021 이 12호에 없다). 10호와는 **같은 그룹(Offer/
  Marinescu)의 다른 논문**(Pang 2019 *PCCP* ↔ Pang 2021 *Mater. Today*) — 공통 원전 아님.
  ⇒ "같은 원전을 두 리뷰가 다르게 적었는가" 는 이 쌍에서도 수행 불가; 대신 **압력 요구치
  ≈1–5 MPa 가 종설 셋에서 원전 셋으로 독립 수렴**한다는 것이 실측.
  후속 후보 1 순위 = **Li Qianya et al., *Nat. Energy* 2025, 10, 1064** ("The critical importance
  of stack pressure in batteries" — 13호 [23], Q6 요구 창 정본 후보) · 2 순위 = **Zhang et al.,
  *Nat. Commun.* 2025, 16, 1013** (무외압 Si ASSB — 압력 0 에서의 접촉 손실 시계열, Q1·Q6) ·
  3 순위 = **Li Menglin et al., *AFM* 2025, 35, 2415696** (`<5 MPa` 근거 후보) · 4 순위 =
  **Gu et al., *AEM* 2023, 13, 2203153** (응력 측정 종설 — 9호 힘 시계열의 측정법 계보).
  큐 13~37 과 겹침 검색 **0 건**.

- **2026-09-22 (ingest 14)** — `assb` 14호 논문 흡수 (큐 13번 — **"OCV 경쟁 접근"** 으로
  등록된 편): `raw/papers/oh2025_maxwell-protocol-nondestructive-assb-health.md` (Oh⁺, Kim⁺,
  Kim, An, Kwon, **Choi Jang Wook**, *Angew. Chem. Int. Ed.* **64** (2025) e202514910,
  doi `10.1002/anie.202514910`, **Batteries Hot Paper**, CC BY-NC-ND; 본문 9 쪽 + **SI .docx**
  (Experimental + Note S1 + Fig. S1–S16, 표 0), PDF `fa35a5cdd5d3fcec…` · SI
  `ce0b9a35c96ef99c…` 실측 일치). 접수→승인 **35 일**. 서울대 + **HMG-SNU JBRC(현대차)**.
  자기 인용 **21/74**. ⚠ 지면은 *Angew. Chem.* 독일어판 조판이지만 **본문 영어**.
  **실험 논문** (엔트로피메트리 3 셀 · volumetry 3+1 셀 · XRM 4 · SEM). 크로핑 본문 **6 장
  전부 봄**, SI 16 장 중 **11 장 봄**(S1·S2·S3·S4·S7·S8·S9·S12·S13·S14·S16; 안 본 것 S5·S6·
  S10·S11·S15 형태학 패널). 합자 잔존 0; ⚠ 대소문자 무시 집계에서 `SOH` 5 회는 전부 저자
  "**Soh**n" — 약어 재집계.
  **판정: "OCV 경쟁" 이 아니라 "OCV 의 관측 추가"** — `E(x)` 를 적합하지 않고 같은 상태함수의
  두 편미분 `−F(∂E/∂T)_P` · `F(∂E/∂P)_T` 를 잰다. 분리 주장은 mechanical ↔ chemical 이고
  `LAM_PE` ↔ 접촉 손실은 물음 자체가 없다. **결과 다섯**:
  ① **새 칸 0 (14편 누적 ≈8.5/8 유지, Q4 0/14).** 층 셋 — Q1 비파괴 대리량 `F(dE/dP)`
     42.7 → 34.7 µJ mol⁻¹ Pa⁻¹(−18 %) · Q6 계보 최초 `E(P)`(2 구간, **비선형 2 배**) · Q8
     OCV 축 열역학 도함수 ≈28 점 × 3 셀.
  ② ★★★ **void 2 배에 용량 불변**(86.0 ↔ 84.0 %, 역상관) — 접촉 손실이 문턱 아래에서
     `Q_apparent` 에 안 들어간다 = OCV 적합의 **무감** 형태. 4호의 반대쪽 끝.
  ③ ★★ **Q4 성질 일곱 번째** — 역문제 없음 → 조건수 정의 자리 없음, 귀속 유일성 미검토.
     `[재현]` ΔS SOC 축 적분 부호 반전(≈ −3.5 → +1.5)은 비균질만으로 안 나온다(sum rule, G8).
  ④ ★★ ΔS 는 `[인쇄]` "contact loss as well as interfacial resistance" 를 **한 신호로** 받는다
     고 스스로 정의 → 분리 후보 행은 **volumetry**(우리 `[해석]`, 실측 0).
  ⑤ ⚠ Li 금속 음극항을 "constant" 로 두지만 식 (10) 의 `V_m(Li)` 13 cm³ mol⁻¹ 은 **상수 ≠ 0**
     이고 `[재현]` 실측 2.2 mV 의 30 % 크기; 실측 `dE/dP` 는 격자 몰부피로 설명되지 않는
     **유효 컴플라이언스**.
  **어긋남 15 건**(D1 Fig. 3a 이탈 ≈2–4 mV ↔ ΔS 함의 0.47 mV · **D2 Fig. 3c "after" 가 S2 세
  셀 어느 것과도 다름** · **D4 신품 volumetry 42.5 ↔ 22.2 = 압력 구간 2 배** · D6 Fig. 6 등급
  규칙 ↔ 본문 · **D7 전·후 volumetry OCV 171 mV 차** · D11 화학 단독 대조군 0 · D12 "similar"
  로 덮인 역상관 · D13 음극 상수항). 공백 14 건(G1 등급 문턱 0 · G3 `dE` 판독 규칙 0 · G7
  SOC 축 0 · G8 sum rule · G11 >300 MPa 미수행 · G12 (ΔS, ¬ΔV) 칸 없음).
  컴파일: **새 개념 페이지 1** [[assb-maxwell-ocv-derivative-channels]] (관측 축이 새롭고
  이 카드·CRB 페이지·압력 페이지 셋에서 반복 참조된다 — SCHEMA Page Thresholds 충족).
  이 카드(채움표 14행 + Evidence **열한 번째** 절 + 새 제약 5 개 + 이 항목 + "주장하지 않는
  것" 1 항) · [[assb-pressure-reapplication-separation-test]] (소신호 판) ·
  [[assb-stack-pressure-operating-window]] (`E(P)` 첫 데이터 + 20 MPa Li 금속 ≈225 h) ·
  [[assb-apparent-capacity-decomposition]] (void ≠ `Q_apparent` 실측) ·
  [[constrained-crb-identifiability]] (관측 추가의 첫 ASSB 표본) · [[fitting-degeneracy]]
  (Q4 계보 2025 표본 — 역문제 없는 형태) · [[halfcell-ocp-shape-invariance]] (두 번째 상태함수
  검사). `index.md` +1.
  13호와의 대조: **공통 원전 1 건** — **Oh *AEM* 2025**(13호 [34] = 14호 [10], 14호 저자의
  **자기 논문**) ⇒ 13호 후속 4 순위가 14호 저자 자신의 저압 실셀이므로 **1 순위로 승격**.
  우리 계보와의 인용: 5호 Doux 2020 = 14호 [35] · 4호 Shi 2020 미인용 · 1호 Bielefeld 2019
  대신 Bielefeld 2022 = [69].
  후속 후보 1 순위 = **Oh et al., *AEM* 2025, 15, 2404817**(ref [10], 저압 실셀 — Q6) · 2 순위 =
  **Bielefeld et al., *JES* 2022, 169, 020539**(ref [69], pore 문턱 → 저항 급증 = 1호 `p_c` 의
  실험판 — Q1) · 3 순위 = **Kim … Choi, *PNAS* 2022, 119, e2211436119**(ref [56], 엔트로피메트리
  원전 — SOC 축·sum rule) · 4 순위 = **Kim … Yazami, Choi, *EES* 2020, 13, 286**(ref [57]) ·
  5 순위 = **LePage 2019 *JES* 166, A89**(ref [70], "10 MPa Li creep") · 6 순위 = Lewis 2021
  *Nat. Mater.* / Lu 2022 *Sci. Adv.*(refs [73][74], "void 가 초기 성능에 안 보인다" 원전).
  큐 14~37 겹침 **0 건**(Bielefeld 는 2019 편만 큐에 있음).
- **2026-09-22 (ingest 15)** — `assb` **15호** 흡수:
  `raw/papers/rahman2024_sbms-rul-solid-state-batteries.md`
  (Rahman & Lu, *Proc. IISE Annual Conf. & Expo 2024*, Abstract ID 8085; **6 쪽**, SI 없음,
  PDF sha256 `0d99b00e…`, 본문 sha256 봉인). **첫 학회 회의록**이고 **이 계보에서 심사
  강도가 가장 낮은 표본**이다 — DOI·접수/게재 일자·심사 기록 전부 없다.
  ⚠⚠ **1차 측정 0 을 넘어 재인용 수치도 0** (12·13호보다 한 단계 아래):
  `[재현]` 본문 2,331 단어에서 인용 괄호·절 번호를 빼면 남는 숫자가 **2024 · 8085 · 19 ·
  2021 · 2026** 뿐이고, `capacity`·`experiment*`·`measur*`·`contact`·`pressure` 가 **전부 0 회**.
  본문 그림 **1 장**(액체셀 종설 ref [16] Zou 2023 의 재수록) · 표 0 · 식 0.
  컴파일: **새 개념 0** (6 쪽 회의록에 새 축이 없다). 갱신 — 닻 이 카드(채움표 15호 행 +
  Evidence 열두 번째 + 이 항목) · [[composite-cathode-percolation-utilization]]
  (1호가 야생에서 인용되는 방식 1 절 추가). `index.md` 변동 없음(새 컴파일 페이지 0).
  ★★ **최대 수확은 논문의 내용이 아니라 인용 관계 둘이다** — 이 위키 최초로
  **우리가 이미 읽은 원전을 인용하는 편**이 들어왔다:
  ① **ref [5] = 1호, 어긋난다** (기하 모형 논문이 "부하 균등화·SOC 추정·건전성 모니터링"
  의 근거 · 연도 2018 오기) ② **ref [21] = 12호, 어긋나지 않지만 12호의 결론
  (`[재현]` SSB 실측 열화 라벨 **0/28**)을 버리고 FNN/RNN 정의만 가져간다.**
  ★ **분류 체계 세 번째 표본 = "어휘 미도입"** (12호 병합 · 13호 미배정 · 15호 미도입) →
  `[해석]` **접촉 구분은 실험 층위에서 강제되고 종합 층위에서 소실된다** (표본 3, 잠정).
  Q1~Q8 채움표 행 추가 (**누적 ≈8.5/8 유지, 새 칸 0**). **Q4 여덟 번째 성질 — 가장 얕은 0**
  (추정기 자체가 없다; `accuracy` 7 회 : 수치 0 : 불확실성 0). **여전히 0/15.**
  어긋남 원장 **11 건**(원전 대조로 확인된 것 2 · 제목 기준 판단 3 · 나머지는 내부 정합).
  후속 후보 1 순위 = **Asheri et al., *Comput. Mater. Sci.* 226, 112186 (2023)**(ref [22] —
  ML × SSB **계면 손상**, 12호의 28 슬롯에도 없던 좌표) · 2 순위 = **Bielefeld et al.,
  *ACS AMI* 12, 12821 (2020)**(ref [28] — 1호의 직계 속편, 바인더·탄소 축) ·
  3 순위 = Zou et al., *JES* 73, 109069 (2023)(ref [16], Figure 1 의 원전; ⚠ 액체셀이므로
  `assb` 태그 금지) · 4 순위 = Lipu et al., *JES* 55, 105752 (2022)(ref [33] — 이 편
  참고문헌 중 **제목에 RUL 이 있는 유일한 편**인데 15호가 RUL 을 안 가져왔다; ⚠ 액체셀).
- ★★★ **2026-09-22 (ingest 16)** — `assb` 16호 흡수:
  `raw/papers/ramanayagam2026_stack-pressure-three-electrode-assb-impedance.md`
  (Ramanayagam, Miß, Leier, Duncker, Kirczek, Roling, *Batteries & Supercaps* **2026**, 9,
  e70315, doi `10.1002/batt.70315`, **CC BY**; 본문 10 쪽 + **SI 6 쪽**, 둘 다 sha256 봉인).
  **큐 15번 · 이 큐 3전극 실측 5편(15·16·18·19·20)의 첫 편.**
  크로핑 19 장 중 **11 개 파일을 실제로 봄**(본문 Fig. 1–7 전부 + SI S1·S2·S3·S4 + Fig. 3 의
  (b)(d) 확대 · S2 양 패널 확대 · S3 하단 확대). 안 본 것: SI S5·S6(Bode 적합)·S7(XRD)·
  S8(Arrhenius), 표 크롭 4 장.
  ★★★ **계보 최초 3 건**: ① **3전극 전극 분해**(리튬화 Au/W μ-RE ∅25 µm) + `[인쇄]`
  **2E = 3E 합(10 kHz 아래)** 자기 검증 ② **압력을 본체로 삼은 1차 측정**(`pressure` **49 회** —
  계보 최대) ③ **DRT 정규화 λ = 0.05 를 인쇄** ([[drt-peak-count-nonidentifiability]] 의
  **C1 최초 ✅**; C2–C5 는 전부 ❌).
  ★★★ **가장 큰 수확은 축퇴의 실측 표본**: `[인쇄]` 식 (4) 가 "접촉 면적" 이라 이름 붙인 양을
  **완전구 기하 면적**(`3ε_CAM/r_CAM`)으로 계산 ⇒ `[해석]` 측정량이 보는 것은
  **`j₀ · ε_CAM / r_CAM` 한 조합**(9호 `A_eff·ε_p/R_s` 와 같은 자리)인데 **뒤 둘을 고정해
  전부 `j₀` 로 읽는다**(0.74 → 1.33 A m⁻²). 같은 Table 2 의 `Q_DL` **0.18 → 0.54 (3 배)** 를
  면적으로 읽으면 `[재현]` **`j₀` 가 0.60 배로 감소** — **같은 데이터, 반대 결론**.
  → [[assb-lampe-contact-product-degeneracy]] (**single-source → multi-source-primary**,
  처방표에 **`R_CT·C_dl` 채널** 신설).
  ★★ **Q5 가 네 겹으로 채워졌다**: 기준극이 Li–In 이 **아니고**(Au/W) · 안정성을 **인용으로
  가정**(`stable` 3 중 2 가 남의 논문) · `[도표]` **리튬화 곡선에 평탄부 없음**(2.5 µAh 에
  560 mV 표류) · `[도표]` **두 셀의 In–Li 평탄 전위가 0.58 ↔ 0.47 V (0.11 V) 어긋남**,
  `[재현]` 과전압 ≈5 mV 로 설명 불가, **논문 무언급**.
  ★★★ **그리고 평탄 OCP 구간 안에서 음극 DRT 가 `[도표]` 18.6 → 1.2 (≈15 배)** 움직인다 —
  **"음극이 평탄하다" ≠ "음극이 조용하다".**
  **Q6**: 운전 **97 / 389 MPa** = 계보 최댓값(5호 Li 금속 상한의 5.2 배, ⚠ 화학 다름),
  **제작 = 운전인 첫 표본**, 압력 → 임피던스 1 차(완전지 반원합 `[인쇄]` 23↔85 Ωcm²),
  압력 → 공극률 `[인쇄]` **11.2 ↔ 12.9 %**, 압력 → 용량 `[도표]` **+9 … +59 %**(SI 그림에만,
  본문 `capacity` **1 회**). ⚠ **스윕 아님(2 점) · 이력 0 · 두 압력이 다른 셀 · 97 MPa 은
  필연적 하강 분기**(논문 무언급) → 5호의 `θ(P)` 이력 물음은 **여전히 미해결**.
  **어긋남 원장 12 건**(D1 본문 "In 박 두께 동일" ↔ SI 67–109 µm · D3 "2 배 넘게" ↔ `[재현]`
  1.797 · D6 완전지 DRT 의 τ≈10⁻⁴ 봉우리가 **양극·음극 어디에도 없다** · D7 **부분(4.6)이
  전체(3.1)보다 크다** …), 공백 원장 **16 건**(G3 `D_CAM` 3.1 배 무언급 · G5 분리막 저항 비공개 ·
  G9 `x_Li` 와 두께가 완전 공선 · G12 용량 미논의 …).
  **Q1~Q8 채움표 16호 행 추가 — 누적 ≈8.5 → ≈9.5** (Q2 +0.5 전극 분해 관측 · Q5 +0.5 기준극 실측).
  **Q4 아홉 번째 성질 = "밟고 지나갔다" — 여전히 0/16.**
  컴파일: [[assb-lampe-contact-product-degeneracy]] · [[assb-stack-pressure-operating-window]] ·
  [[drt-peak-count-nonidentifiability]] 갱신. **새 개념 페이지는 만들지 않았다** (세 페이지가
  이미 이 편의 세 축을 담고 있다).
  후속 후보 1 순위 = ★ **Miß, Ramanayagam, Roling, *ACS AMI* 14 (2022) 38246**(ref [30] —
  이 편 **TLM 방법의 원본**이자 `r_CAM`·초기값·비교 `j₀` 의 출처. 원본을 봐야 이 편의 고정
  가정이 어디서 왔는지 닫힌다) · 2 순위 = **König, Ramanayagam, Kraus, Roling,
  *Batteries & Supercaps* 7 (2024) e202300578**(ref [31] — 음극 heterogeneous interphase
  모형의 원본, 대칭셀 판) · 3 순위 = **Hertle et al., *JES* 170 (2023) 40519**(ref [24] —
  μ-RE 원본, "0 V vs Li⁺/Li 안정" 의 **유일한 근거**; Q5 의 G6 이 여기서 닫힌다) ·
  4 순위 = **Fukunishi et al., *J. Power Sources* 564 (2023) 232864**(ref [39] —
  ★ **큐 17번과 같은 논문**이고 이 편의 유일한 외부 실측 대조군, 그리고 **열화를 다룬다**) ·
  5 순위 = Roling et al., **chemRxiv 2025** `10.26434/chemrxiv-2025-qj66b`(ref [34] —
  공극률–압력 관계의 출처, ⚠ 심사 전 프리프린트인데 이 편의 두께 전부가 여기 걸려 있다).

## 이 페이지가 주장하지 않는 것

- ASSB 실셀 자료를 **본 적이 없다.**
  → ⚠ **2026-09-16 정정**: `assb` 4호(Shi 2020)가 **ASSB 실셀 실험 자료**다
  (FIB-SEM 토모그래피 + EIS + 용량곡선), **5호(Doux 2020)도 실험 논문이다**
  (X-선 토모그래피 + XRD + EIS + 압력 실계측). 다만 **원자료(raw data)** 를 받은 것은
  아니고 **논문에 인쇄된 값과 그림을 읽은 것**이다.
- "OCV 로 못 가른다" 를 **결론으로 적지 않았다** — 그것이 이 물음이다.
- 액체셀 결론(`LAM_NE 최광 · LLI 최협`)을 ASSB 로 **옮기지 않는다.** 음극 축이
  아예 다르므로 모집단이 다르다.
- ★ **2026-09-22 추가**: **종설(8호)의 수치를 이 카드의 근거로 삼지 않는다.**
  `<≈1 MPa`·`SOH RMSE ≤0.873 %`·Table 2 의 여덟 숫자는 전부 **재인용**이고,
  그중 하나는 **우리가 가진 원전과 이미 어긋난다**(D1). 원 논문을 받기 전까지
  "리뷰가 이렇게 적었다" 이상으로 쓰지 않는다.
- ★ **Q4 가 깨졌다고 주장하지 않는다.** 8호도 **유일성을 재지 않았다** — 이름을
  실패 모드 목록에 올렸을 뿐이다. `assb` **8 / 8 편 0** 이다.
- ★★ **2026-09-22 정정·확장 (10호)**: **Q4 의 칸은 채워졌으나 "쟀다" 는 여전히
  0 이다.** 10호가 깬 것은 **"아무도 이 문제를 이름 붙이지 않았다" 는 상태**이지
  **"아무도 재지 않았다" 는 상태**가 아니다. **유일성·식별성을 수치로 잰 `assb`
  논문은 10 / 10 편 중 0 편이다** — 조건수 · 프로파일 가능도 · 근최적 폭 ·
  Fisher/CRB 가 전부 0 이다. 이 구분을 흐리지 않는다.
- ★ **10호의 재인용 수치를 이 카드의 근거로 삼지 않는다.** `22 % / ~10 %` ·
  `~120 MPa` · `~400 MPa` · `<1 Ω cm²` 는 전부 남의 논문 값이고, 그중 하나는
  **인용 번호가 틀렸다**(digest D5). 원전을 받기 전까지 **방향만** 쓴다.
  ⚠ 단 **방법론적 주장**(비유일성 · 최소 원소 · ill-posedness · 주관적 귀속)은
  **저자들의 1차 주장**이므로 이 규율의 바깥이다 — 그렇게 구분해서 인용한다.
- ★★★ **2026-09-22 (11호 Yu 2024) — 세 가지를 주장하지 않는다.**
  ① **"Q4 가 측정됐다" 고 하지 않는다.** 11호도 재지 않았다 (**0 / 11 편**).
  우리가 한 것은 **논문이 인쇄한 두 그림(Fig. S3, Fig. 4d/7d)을 나란히 놓고
  크기를 비교한 것**이고, 그 비교는 **우리 `[재현]` 이지 논문의 주장이 아니다.**
  ② **"DRT 봉우리 높이가 배선 때문에 69 % 틀렸다" 고 하지 않는다.** 배선이
  바뀌면 인덕턴스·접촉저항이 **실제로** 바뀌고, 두 측정의 최고 주파수가
  **1 MHz ↔ 2 MHz** 로 다르며, SI 가 **"같은 셀" 이라고 명시하지 않는다.**
  우리가 말하는 것은 **"인공물의 상한이 본문 효과보다 크다"** 까지다.
  ③ **11호의 봉우리 개수(5–6)를 "정답" 으로 삼지 않는다.** 같은 논문이
  개수가 **사이클·조작·배선의 함수**라는 것을 보여 준다 —
  9호를 판정할 때 쓰는 것은 **"2 개는 모자란다"** 가 아니라
  **"개수를 고르는 규칙이 문헌에 없다"** 이다.
  ④ ⚠ **그림에서 읽은 봉우리 높이·위치는 전부 `[도표]` 다.** 세로 판독 오차
  ±1–3, 가로 ≈1/4 자릿수. 이 값들을 정본으로 인용하지 않는다.
- ★ **2026-09-22 (12호 Sadegh Kouhestani 2022) — 세 가지를 주장하지 않는다.**
  ① **이 종설의 어느 수치도 이 카드의 근거로 쓰지 않는다** — `0.4–1 MPa`·EV 판매 통계·
  `40–70 °C` 전부 재인용이고, 인용번호 오류가 21 건이라 **귀속 자체가 불확실**하다.
  ② **"PHM 분야가 LAM 과 접촉 손실을 같은 것으로 본다" 고 일반화하지 않는다.** 확인된 것은
  **이 종설 한 편의 §2.2 정의 문장**이고, 그 원전(Hu 2020 *Joule*)이 같은 정의를 쓰는지는
  원전을 받아야 안다.
  ③ **`A_eff` 가 Tian & Qi 2017 에서 왔다고 주장하지 않는다.** 12호의 한 문장에서 **형태가
  같다**는 것까지이고, 9호(Huo 2025)가 그 논문을 인용하는지는 **확인하지 않았다**.
- ★ **2026-09-22 (13호 Zheng 2026) — 세 가지를 주장하지 않는다.**
  ① **"그리드 ASSB 는 LFP + Si 다" 를 사실로 옮기지 않는다** — 13호의 **권장**이고, 저자
  소속(전력연구원 + 전지 제조사)이 수요 측이며 권장 복합전해질의 유일한 수치 예가 **자기
  논문**이다. 이 카드가 받는 것은 "그런 설계가 요구되고 있다" 는 진술까지다.
  ② **`<5 MPa` 를 압력 창의 값으로 쓰지 않는다.** 1 차 주장이지만 인용 문장이 값을 주는지
  확인되지 않았고(G3), 같은 논문의 Fig. 2 가 권장 클래스에 상단 10 MPa 를 준다(D4). Fig. 2
  의 다섯 창은 `[도표]` 이고 산정 규칙이 없다(G8).
  ③ **"접촉 손실을 임피던스 쪽에 둔다" 가 13호의 입장이라고 단정하지 않는다.** 13호는
  소속을 **적지 않았다** — 우리가 확인한 것은 **누락**이지 배정이 아니다. 12호의
  `LAM ⊃ 접촉 손실` 과 나란히 놓을 때도 "다른 방식으로 분리 물음이 없다" 까지만 말한다.
- ★ **2026-09-22 (14호 Oh 2025) — 세 가지를 주장하지 않는다.**
  ① **"volumetry 가 `LAM_PE` ↔ 접촉 손실을 가른다" 고 하지 않는다.** 새 감도 행의 부호표
  (ΔS 행 = 0 / `dE/dP` 행 ≠ 0)는 **우리 `[해석]`** 이고 실측 0 이다 — 논문은 그 물음을
  두지 않았고, 폭 측정기로 검사할 명제로만 등록한다.
  ② **42.7 µJ mol⁻¹ Pa⁻¹ 를 "ΔV" 라는 재료 상수로 옮기지 않는다.** 같은 신품에서 압력
  구간에 따라 2 배(D4), 전·후 측정의 SOC 가 171 mV 다르다(D7). `E(P, x)` 면이 모델링되기
  전까지 "이 셀에서 이 구간에 이 값" 까지만.
  ③ **"void 는 용량에 안 보인다" 를 일반화하지 않는다.** 50 사이클 · 조건당 셀 1 · 2 점 ·
  0.5C 의 것이고, 4호는 같은 자릿수의 void 에서 98 % 손실을 봤다. 우리가 받는 것은
  **사상이 문턱형이라는 두 점**까지다. 그리고 **Q4 는 0/14** — 역문제가 없다는 것은
  "유일성이 필요 없다" 가 아니라 "귀속의 유일성을 아무도 안 물었다" 이다.
- ★ **2026-09-22 (15호 Rahman & Lu 2024) — 다섯 가지를 주장하지 않는다.**
  ① **이 편의 어떤 문장도 이 카드의 근거로 쓰지 않는다.** 1차 측정 0 · **재인용 수치도 0**
  이고, 우리가 가져온 것은 **인용 관계 두 개**뿐이다.
  ② **"[5] 인용이 어긋난다" 는 우리 1호 digest 대조로 확인된 것**이고, 그 digest 자체는
  원문 PDF 의 **사본**이다 — 논문·보고서에 옮기려면 원문 두 편을 다시 편다.
  ③ **"[21](12호) 인용이 원전과 맞다" 고 단정하지 않는다.** 우리 12호 digest 가 FNN/RNN
  정의 수준을 채록하지 않아 **어긋남 미확인(정합 추정)** 이다. 우리가 말하는 것은
  "12호의 **결론**이 전달되지 않았다" 까지다.
  ④ **ref [28]·[22]·[16]·[15]·[2] 를 읽지 않았다.** 그들에 대한 판단은 **제목·서지
  수준**이고, 특히 D6(Janek & Zeier 논조 반대)은 **제목만으로 한 판단**이다.
  ⑤ **"IISE 회의록이 심사를 받지 않았다" 고 주장하지 않는다.** PDF 에 심사 기록·DOI·
  접수일이 **없다**는 것만 적었다.
- ★★ **2026-09-22 (16호 Ramanayagam et al. 2026) — 다섯 가지를 주장하지 않는다.**
  ① **논문의 결론(압력이 `j₀` 를 올린다)이 틀렸다고 주장하지 않는다.** 주장하는 것은
  **그 절차가 `j₀` 와 접촉 면적을 가른 절차가 아니라는 것**이고, 근거는 **논문 자신의
  식 (4)·(5) 와 자신의 Table 2** 다.
  ② **`j₀^true` 가 실제로 감소한다고 주장하지 않는다.** 대안 배정(0.60 배)은 `Q_DL` 을
  면적으로 읽었을 때의 **결과**이지 우리 측정이 아니다. 주장은 **"같은 데이터가 반대
  결론을 허용한다"** 까지다. ⚠ `β` 가 달라(0.89 ↔ 0.81) 두 `Q` 는 엄밀히 차원이 다르다.
  ③ **In–Li 평탄 전위의 0.11 V 차이를 압력 효과라고 하지 않는다.** 기준극 오프셋이 더
  그럴듯하고, **둘 다 논문이 검토하지 않았다**는 것이 요점이다. `[재현]` 0.38 mV MPa⁻¹ 가
  14호의 `dE/dP`(0.23–0.44)와 같은 자릿수인 것도 **우연일 수 있다** — 화학·셀·측정이 다르다.
  ④ **이 편의 압력 값을 다른 셀로 옮기지 않는다.** In 음극 · 단결정 NMC83|6|11 ·
  argyrodite · ∅12 mm · 0.1 C · **신품 2 번째 사이클**이다. 5호의 Li 금속 75 MPa 상한과
  **같은 축에서 비교할 수 없다**.
  ⑤ **이 편에서 열화에 관한 어떤 것도 가져오지 않는다.** `degrad*`·`aging`·`LAM`·`LLI`·
  `SOH` 가 **전수 0 회**다. 우리가 받는 것은 **역문제의 구조**이지 열화 지분이 아니다.
