---
title: ASSB 에서 OCV 적합이 LAM_PE 와 접촉 손실을 가를 수 있는가
description: "In solid-state cells (Li-In / Li metal / anode-free), does OCV fitting separate true positive-electrode active material loss from contact/percolation loss"
created: 2026-09-16
updated: 2026-09-16
type: research-question
tags: [battery, degradation, research, assb]
sources: [raw/papers/cui2026_direct-diagnosis-lfp-degradation-modes.md, raw/papers/bielefeld2019_microstructural-modeling-assb-composite-cathode.md, raw/papers/clausnitzer2023_optimizing-composite-cathode-structure-resolved.md, raw/papers/liu2024_grain-level-chemo-mechanics-composite-cathode-degradation.md]
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
   → **세 편의 공백은 같은 한 조각이다: cohesive zone / phase-field damage.**
2. **Li-In 기준 전위가 얼마나 안정한가.** 평탄한 것은 두 상 공존 영역 안에서만이다.
   벗어나면 기준이 이동하고 그것은 전체 곡선의 **밀기** — **`LLI` 와 같은 모양**이다.
3. **무음극의 dead Li 와 SEI Li** 는 OCV 에 똑같이 들어온다. 가르는 관측이 있나.
4. **압력**이 상태변수다 (액체셀에 없던 것). 열화 모드가 압력 의존이면 "상태" 의
   정의부터 다시 해야 한다.
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

**1호 단독 1.5 → 2편 누적 ≈2.5 → 3편 누적 ≈3.0 칸이다.**
3호가 **새로 채운 칸은 Q8 하나**(2호가 남긴 "OCV 곡선 0 편" 단서를 닫았다)이고,
**Q3 에 새 층위("fitted 문턱")를 열었다.** 남은 5 칸 중:

- **Q4(유일성)는 `assb` 3/3 편이 안 쟀다** — 전부 forward 전용이라 **원리적으로**
  못 채운다. → **역문제를 다루는 논문이 이 축에 반드시 한 편 들어와야 한다.**
- **Q5·Q6·Q7 은 여전히 0 편.** 특히 **Q6(압력)은 `assb` 3/3 편이 `pressure` 0 회**다.
  (2호의 `sinter density`·FAST/SPS 는 **제조 압력의 간접 대리**일 뿐이고, 3호는
  **계면 접촉 역학을 정면으로 다루면서도** 스택 압력을 한 번도 쓰지 않는다 —
  이 축의 공백이 3호에서 가장 두드러진다.)
- **Q1 은 세 편이 세 개의 다른 양을 "접촉 손실" 이라 부른다**: 기하 분율(1호) ·
  연결성(2호) · **계면 인장응력**(3호). **앞의 둘은 같은 양이고 셋째는 다른 차원**이다.
- ✅ **Q8 의 단서가 닫혔다**: 3호 SI Fig. S2 가 **OCV 곡선**을 준다. ⚠ 단 그 OCV 는
  **액체 반쪽전지 GITT 측정**(ref 18)에서 온 것이고 ASSB 셀의 것이 아니다.

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

## 이 페이지가 주장하지 않는 것

- ASSB 실셀 자료를 **본 적이 없다.**
- "OCV 로 못 가른다" 를 **결론으로 적지 않았다** — 그것이 이 물음이다.
- 액체셀 결론(`LAM_NE 최광 · LLI 최협`)을 ASSB 로 **옮기지 않는다.** 음극 축이
  아예 다르므로 모집단이 다르다.
