---
title: ASSB 에서 OCV 적합이 LAM_PE 와 접촉 손실을 가를 수 있는가
description: "In solid-state cells (Li-In / Li metal / anode-free), does OCV fitting separate true positive-electrode active material loss from contact/percolation loss"
created: 2026-09-16
updated: 2026-09-16
type: research-question
tags: [battery, degradation, research, assb]
sources: [raw/papers/cui2026_direct-diagnosis-lfp-degradation-modes.md, raw/papers/bielefeld2019_microstructural-modeling-assb-composite-cathode.md]
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

**8 칸 중 실질적으로 채워진 것은 1.5 칸이다.** 나머지 6.5 칸이 `assb` 섹션이 채워야 할
빈칸으로 확정됐다. 특히 **Q6(압력)은 아직 0 편이 다뤘다** — 액체셀에 없던 상태변수인데
미시구조 쪽 원류 논문에 `pressure` 가 **0 회**다.

## Evidence For / Against

### For — "OCV 만으로는 못 가른다" 쪽 (2026-09-16, Bielefeld 2019)

- **접촉 손실이 `LAM_PE` 와 섞이는 방식이 확정됐다: 곱셈.**
  [[composite-cathode-percolation-utilization]] 의 `θ_AM` 은 재료량을 건드리지 않고
  **용량 축 스케일에 곱해진다** (`Q_apparent = θ_AM · Q_material`, 우리 해석).
  OCV 곡선은 **곱만** 본다 → 위 "모르는 것 1" 의 **형태**가 정해졌다.
- **`A_spec,a` 봉우리가 평탄하고 두께 곡선이 겹친다** — forward map 자체가 이미
  납작하다. [[fitting-degeneracy]] 가 화학 무관하게 재현될 자리.

### Against / 단서 — "독립 관측이 존재할 수 있다" 쪽

- **ex situ XRD 의 inactive AM 분율** = 원리적으로 `1 − θ_AM` 의 **measured 라벨**
  (Strauss et al., ACS Energy Lett. 2018, 3, 992−996; Bielefeld 2019 ref 13).
  액체셀에서 우리를 막았던 "measured 라벨 없음" 이 여기서는 **존재할 수 있다.**
  ⚠ 단 Bielefeld 는 그 대조를 **정성적으로만** 했고 스스로 무효화했다 —
  `[인쇄]` "the total packing density of AM used by Strauss et al. is not known,
  **as the porosity was not measured**".

### 우리 계획에 붙은 새 제약 (2026-09-16)

- ★ **DEM 라벨 자체가 폭을 갖는다.** Bielefeld 가 인쇄한 실측: 거시 파라미터를 전부
  고정해도 무작위 충전 배열만 바꾸면 임계 근방에서 `θ_AM` 이 **≈30 % ↔ ≈70 %** 로
  이봉으로 갈린다. → **DEM 산출을 라벨로 쓰려면 반드시 폭을 붙인다**
  (`bms-balancing/docs/NEW_MODEL_REQUIREMENTS.md` §5 의 규율을 우리 자신에게).
  그리고 **임계에서 멀리**(`p − p_c ≳ 5 vol%`) 작업해야 한다.
- **DEM 도메인 크기 수렴 시험이 선행 조건**이다 — Bielefeld Fig. 10 의 유한 크기 효과가
  얇은 도메인에서 `θ` 를 낙관 방향으로 편향시킨다.
- `θ_AM` 의 **시간 변화는 아직 아무도 안 줬다.** Bielefeld 는 pristine 정적 기하만 준다.

## Status Log

- **2026-09-16 (개설)** — 카드 생성. `assb` 섹션의 닻으로 지정. 보류 항목.
- **2026-09-16 (ingest 1)** — `assb` 1호 논문 흡수:
  `raw/papers/bielefeld2019_microstructural-modeling-assb-composite-cathode.md`.
  컴파일: [[composite-cathode-percolation-utilization]].
  **미결 항목 1 의 "형태" 가 정해졌고 "동역학" 이 남았다.** Q1~Q8 채움표 개설 (1.5/8).
  후속 후보 1 순위 = Strauss et al. 2018 (ref 13, measured `1 − θ_AM`),
  2 순위 = Koerver et al. 2017 (ref 7, 접촉 손실의 실험 원전 + 용량축).

## 이 페이지가 주장하지 않는 것

- ASSB 실셀 자료를 **본 적이 없다.**
- "OCV 로 못 가른다" 를 **결론으로 적지 않았다** — 그것이 이 물음이다.
- 액체셀 결론(`LAM_NE 최광 · LLI 최협`)을 ASSB 로 **옮기지 않는다.** 음극 축이
  아예 다르므로 모집단이 다르다.
