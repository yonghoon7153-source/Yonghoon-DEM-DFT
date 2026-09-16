---
title: ASSB 에서 OCV 적합이 LAM_PE 와 접촉 손실을 가를 수 있는가
description: "In solid-state cells (Li-In / Li metal / anode-free), does OCV fitting separate true positive-electrode active material loss from contact/percolation loss"
created: 2026-09-16
updated: 2026-09-16
type: research-question
tags: [battery, degradation, research, assb]
sources: [raw/papers/cui2026_direct-diagnosis-lfp-degradation-modes.md, raw/papers/bielefeld2019_microstructural-modeling-assb-composite-cathode.md, raw/papers/clausnitzer2023_optimizing-composite-cathode-structure-resolved.md, raw/papers/liu2024_grain-level-chemo-mechanics-composite-cathode-degradation.md, raw/papers/shi2020_mechanical-degradation-assb-cathode.md]
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

**1호 단독 1.5 → 2편 ≈2.5 → 3편 ≈3.0 → 4편 누적 ≈5.5 칸이다.**
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

### Against / 단서 — "독립 관측이 존재할 수 있다" 쪽

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

## 이 페이지가 주장하지 않는 것

- ASSB 실셀 자료를 **본 적이 없다.**
  → ⚠ **2026-09-16 정정**: `assb` 4호(Shi 2020)가 **ASSB 실셀 실험 자료**다
  (FIB-SEM 토모그래피 + EIS + 용량곡선). 다만 **원자료(raw data)** 를 받은 것은
  아니고 **논문에 인쇄된 값과 그림을 읽은 것**이다.
- "OCV 로 못 가른다" 를 **결론으로 적지 않았다** — 그것이 이 물음이다.
- 액체셀 결론(`LAM_NE 최광 · LLI 최협`)을 ASSB 로 **옮기지 않는다.** 음극 축이
  아예 다르므로 모집단이 다르다.
