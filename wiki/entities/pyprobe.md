---
title: PyProBE (OCV/DVA 피팅 도구)
description: "Imperial College 의 배터리 데이터 처리 도구 — 전극 OCP 로 셀 OCV·ICA·DVA 를 맞춰 전극 용량과 리튬 재고를 추정한다. 우리에게는 경쟁 도구이자, 우리 degeneracy 질문을 적용할 '판정 대상' 후보"
created: 2026-10-01
updated: 2026-10-01
type: entity
tags: [degradation, tooling, research]
sources: [raw/articles/2026-10-01-github-research-briefing.md, raw/repositories/2026-10-01-pyprobe-dma-on-synthetic-truth.md, raw/repositories/2026-10-01-pyprobe-shape-only-on-synthetic-truth.md]
confidence: medium
explored: false
verificationStatus: unverified
model: claude-opus-5-5
effort: medium
claimType: mixed
evidenceScope: multi-source-mixed
---

# PyProBE (OCV/DVA 피팅 도구)

## 개요

- 저장소: `https://github.com/ImperialCollegeLondon/PyProBE` · 예제: `https://pyprobe.readthedocs.io/en/latest/examples/ocv-fitting.html`
- 브리핑 요약 (2026-10-01 · 단일 출처): 전극 OCP 와 셀 OCV · ICA · DVA 를 맞춰 **전극 용량과 리튬 재고**를 추정한다.
  예제와 합성 데이터 복원 시험이 있다. 허용적 라이선스.
- **2026-10-01 실측 (아래):** 2.6.0 을 별도 venv 에 깔아 공개 API 를 읽고 우리 합성 truth 로 돌렸다. 자유 파라미터는
  **4** (`x_pe_lo · x_pe_hi · x_ne_lo · x_ne_hi`), 용량은 `ptp(Capacity)/ptp(SOC)` 로 **절대 용량을 그대로 쓴다**
  (전극 용량 = 셀 용량 / 창 폭 · Li 재고 = Q_pe·x_pe_lo + Q_ne·x_ne_lo), 불확실성 · 식별성 진단은 **없다**. LLI · LAM
  정의는 비율 (`1 − Q/Q₀` · `1 − Li/Li₀`) 로 우리 Birkl 정의와 같다. `confidence: medium` 으로 올린 근거가 이 실측이다.

## 핵심 사실 — 우리 질문과의 관계

이 도구는 [[birkl-ocv-degradation-diagnostic]] 계열의 **electrode balancing 피팅**을 구현한 것으로 보인다. 우리
연구는 바로 그 피팅이 **유일한 답을 주는가**를 묻는다 ([[fitting-degeneracy]] · [[22p-physics-or-degeneracy]]).
그래서 두 갈래로 쓸 수 있다.

| 쓰임 | 내용 | 주의 |
|---|---|---|
| 경쟁 · 비교 도구 | 같은 곡선에 PyProBE 와 우리 파이프라인을 각각 적용해 LLI · LAM 추정을 비교 | 둘 다 같은 형상 정보를 쓰면 같은 축퇴를 공유할 수 있다 — 일치가 정답의 증거는 아니다 |
| **판정 대상** | 우리 PyBaMM 합성 truth (참값을 아는 곡선) 를 PyProBE 에 넣어 참값을 되찾는지, 초기값 · 피팅 범위에 따라 답이 갈리는지 본다 | [[np-lip-ocv-reparametrization]] 의 2 자유도 정리 — SOC 정규화 OCV **형상**만으로는 세 모드 비율이 다 정해지지 않는다. PyProBE 가 절대 용량을 함께 쓰는지 먼저 확인해야 한다 |

- **미세단락:** 브리핑도 "적합도가 좋다고 미세단락까지 입증되는 건 아니다" 라고 적었다. ISC 판별 도구가 아니다 —
  [[isc-detection-vs-balancing-masking]] 의 근거로 쓰지 않는다.

### 실측 (2026-10-01 · `raw/repositories/2026-10-01-pyprobe-dma-on-synthetic-truth.md` · 결과 JSON 동봉)

우리 PyBaMM 합성 truth (grid_curves_v4 · 0.05 C DFN 곡선 · 300 점) 를 우리 전 범위 OCP 표와 함께 PyProBE 에 넣었다.
첫 표는 **절대 용량을 참값으로 알려 준 조건**이고, 형상만 조건은 표의 끝에서 두 번째 행 (같은 날 추가 실측). 전체 8.5 s · 운영 환경 불변.

| 물음 | 결과 | 읽는 법 |
|---|---|---|
| 참값 복원 (기본 시작점 `[0.9, 0.1, 0.1, 0.9]` · 전 범위 · OCV target) | LLI 0.10 → **0.101** · LAM_NE 0.10 → **0.102** · 혼합 (0.1/0.1/0.1) → **0.101 / 0.101 / 0.096** · LAM_PE 단독 0.06 → **0.044** (−27 % 상대) · SOH 는 정확 | 좋은 시작점 + 전 범위 + 참값 용량이면 ±1–2 %p 안. LAM_PE 만 체계적으로 작다 (LLI 단독에서도 LAM_NE −0.018 가짜) |
| 초기값 다중 시작 (8) | 전 범위 OCV: 먼 골에 떨어진 답이 LAM_pe **−0.47 … −0.64**, LAM_ne **−2.2 … −2.7** — 전압 RMSE 는 최적의 **2–4 배** (10.7 → 39.5 mV) | multimodal 은 분명하다. 다만 먼 골은 RMSE 로 걸러진다 — [[fitting-degeneracy]] 의 "multimodal (최적화 난이도)" 쪽 |
| SOC 범위 자르기 (5–95 % · 10–90 %) | 최소 RMSE 는 **내려가는데** (10.7 → 8.7 mV) best-RMSE 답이 **움직인다**: 혼합 LAM_pe 0.101 → 0.094 → 0.083 · LAM_NE 단독의 LAM_pe 0.007 → −0.016 → −0.026 · LLI 0.004 → −0.006 → −0.010 | **컷오프 끝이 정보를 들고 있다** ([[birkl-ocv-degradation-diagnostic]] 의 컷오프 등식). 범위를 조금 자르면 더 잘 맞으면서 답이 1–2 %p 이동 — flat valley 의 모양 |
| target OCV ↔ dVdQ | dVdQ 는 **불안정**: 전압 RMSE 18–283 mV · LLI −14 … +0.13 · best-RMSE 답도 OCV 와 다르다 (혼합 LAM_pe 0.011 ~ 0.130) | 브리핑의 "OCV 와 DVA 결론이 유지되는가" 시험은 **완벽한 합성 데이터에서도 실패**한다 — 300 점 0.05 C 동적 곡선의 수치 미분이 운동 잔차를 증폭. DVA 는 더 촘촘한 평형 곡선이 있어야 한다 |
| 노이즈 1 · 5 mV × Savitzky–Golay 0 / 11 / 31 | OCV target: LLI **0.100–0.101** 전부 유지 · 평활화 무관. dVdQ: 평활화와 무관하게 틀림 (LAM_pe −0.24 … −0.31 · LAM_ne +0.21 — 가짜 신호) | 평활화 민감도는 target 선택에 종속 — OCV target 이면 묻지 않아도 되는 축 |
| 적합 창 ↔ truth 창 | PE 창 0.937 / 0.277 ↔ truth 0.929 / 0.281 (가깝다) · **NE 충전 끝 0.894 ↔ truth 0.978** (−0.085) · pristine RMSE 10 mV | 0.05 C 과전압 (평형 OCP 표 대비) + 복합 음극 OCP 가 완전 리튬화 근처에서 평탄 → 창은 틀려도 **비율 (LAM · LLI) 은 보상**된다 — [[halfcell-ocp-shape-invariance]] 의 아핀 전제가 여기서는 성립 |
| **형상만 (용량 비제공)** — 용량 열을 pristine 값 또는 1 Ah 로 통일 (`raw/repositories/2026-10-01-pyprobe-shape-only-on-synthetic-truth.md`) | 적합 창 4 개는 **용량과 무관하게 같다** (RMSE 동일) · 모드는 `1 − (1 − mode_true)/SOH_true` 로 되감긴다: LLI 0.10 단독 → LLI −0.025 · LAM_pe −0.137 · LAM_ne −0.161 · **세 모드 똑같이 0.10 인 조건 → 0.000 / 0.001 / −0.006** · LAM_NE 0.20 → LLI −0.188 · LAM_pe −0.189 · LAM_ne +0.023 | [[np-lip-ocv-reparametrization]] 2 자유도 정리의 **수치 확인**: SOC 정규화 형상은 공통 인수 (1−LLI):(1−LAM_NE):(1−LAM_PE) 의 비만 정하고, 세 모드가 같은 비율로 줄어든 방향은 **완전히 보이지 않는다**. 용량 (SOH) 한 숫자가 그 자유도를 닫는다 — 그래서 첫 실측의 "복원" 은 용량을 알려 준 덕이다 |
| `differential_evolution` | PyProBE 가 bounds 를 **[(0.75,0.95),(0.2,0.3),(0,0.05),(0.85,0.95)] 로 하드코딩** — truth x_ne_hi 0.978 은 **밖**. 결과는 `minimize` 국소해와 일치 | 화학 사전 지식이 코드에 박혀 있다. 다른 화학에는 그대로 못 쓴다 |

한계: 조건 5 (+ 형상만 시험에 LLI 0.20 · LAM_NE 0.20 추가) · LAM_PE 단독은 완방 guard 로 0.06 이 최대 · OCP 표는 우리 것 (PyProBE 데이터 파이프라인이 아니라 **피팅
층**의 시험) · 동적 곡선을 OCV 로 넣었다 (실측 저율 곡선과 같은 처지).

**우리 질문에 주는 것:** 외부 공개 도구도 같은 모양을 보인다 — 좋은 시작점 · 전 범위 · 참값 용량이면 복원되고, 범위를
조금 자르거나 시작점을 바꾸면 1–2 %p 이동하거나 먼 골로 간다. 이것은 [[22p-physics-or-degeneracy]] 의 Evidence For
(flat valley + multimodal 둘 다) 이고, 동시에 "RMSE 가 걸러 주는 먼 골" 과 "RMSE 가 못 거르는 1–2 %p 이동" 을 **갈라서**
적어야 한다는 교훈이다.

### 브리핑의 제안 실험 (→ 위 실측으로 수행)

"초기 · 열화 저율 곡선 한 쌍을 OCV 와 DVA 방식으로 각각 피팅하고, 평활화 · 피팅 범위를 바꿔도 LLI/LAM 결론이
유지되는지" — 우리 [[fitting-degeneracy]] 의 flat valley 판정과 같은 축이다. 우리 쪽에서 하면 **참값을 아는**
합성 곡선으로 할 수 있다는 점이 다르다 (실측 곡선으로는 "안정적" 이 "정확함" 을 뜻하지 않는다). 착수는 사용자
승인 뒤, 운영 환경 밖 별도 가상환경에서.

## 이 위키와의 관계

- 방법 축: [[fitting-degeneracy]] · 원전: [[birkl-ocv-degradation-diagnostic]] · 자유도: [[np-lip-ocv-reparametrization]]
- 같은 브리핑: [[pybamm]] · 처리 기준: [[daily-github-briefing-triage]]

## 관련
- [[fitting-degeneracy]]
- [[birkl-ocv-degradation-diagnostic]]
- [[22p-physics-or-degeneracy]]
- [[daily-github-briefing-triage]]
- [[pybamm]]
- [[halfcell-ocp-shape-invariance]]
