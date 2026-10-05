---
title: ampworks (dQdV · dVdQ 피팅으로 LAM · LLI — watch)
description: "저율 반쪽전지 · 전지 곡선의 전압 · ICA · DVA 를 맞춰 전극 창 (xn0 · xn1 · xp0 · xp1) 을 찾고 LAM · LLI 와 그 불확도를 내는 Python 도구 (BSD-3 · Python ≥3.11). 우리에게는 경쟁 · 비교 도구이자 판정 대상. 2026-10-05 실측 (버리는 venv · 우리 합성 truth): 점 추정은 비용 항 · 시작점에 민감하고 (dQdV 만이 가장 안정 · 기본값은 LLI 단독 조건에서 국소 최소), 보고 불확도는 틀린 적합에서 참 오차를 덮지 못하며 Hessian 이 대부분 양정치가 아니다. watch 유지 · 불확도 출력은 채택하지 않는다. upstream 결함 둘 (LLI_std 변수 혼동 · constrained_fit 의 x0 덮어쓰기) 은 초안만 — 발송은 사용자."
created: 2026-10-05
updated: 2026-10-05
type: entity
tags: [degradation, tooling, research]
sources: [raw/articles/2026-10-05-github-research-briefing.md, raw/repositories/2026-10-05-ampworks-on-synthetic-truth.md]
confidence: medium
explored: false
verificationStatus: unverified
claimType: mixed
evidenceScope: multi-source-mixed
---

# ampworks (dQdV · dVdQ 피팅으로 LAM · LLI — watch)

## 개요

- 저장소: `https://github.com/NatLabRockies/ampworks` (BSD-3-Clause · `requires-python >=3.11,<3.16` · main `0.2.0.dev0` · 배포 태그 `v0.1.0`).
  모듈은 dQdV 외에 GITT · ICI · HPPC · OCV 처리도 있다 (`src/ampworks/`). 조직 이름 변경은 `CHANGELOG.md` 원문 "Rebrand NREL to NLR" (#15).
- dQdV 흐름 (예제 `examples/simple_dQdV_example.py` 원문 기준): 흑연 · NMC **반쪽전지 저율 곡선** + 전지 BOL (cycle 2) · EOL (cycle 3866) 충전
  곡선을 `SOC` · `Volts` (전지는 `Ah` 도) 열로 넣고, 스플라인 평활 → `DqdvFitter` 가 전압 · dQ/dV · dV/dQ 의 MAPE 로 파라미터 5 개
  (`xn0 · xn1 · xp0 · xp1 · iR`) 를 맞춘다 (`trust-constr` · 전극마다 x0 < x1 · 초기값 ± 상자 · 격자 탐색 시작점). `calc_lam_lli` 가
  `Q = Ah / (x1 − x0)` · `LAM = 1 − Q/Q[0]` · `Inv = xn0·Qn + (1 − xp0)·Qp` · `LLI = 1 − Inv/Inv[0]` 로 모드를 낸다 (문헌: Weng · Siegel ·
  Stefanopoulou 2023, Frontiers in Energy Research).
- 브리핑 (2026-10-05 · 단일 출처) 의 사실 주장 — 라이선스 · NMC/흑연 초기 · 열화 예제와 CSV · 시험 · main 9/23 — 은 **원문과 맞다**
  (`raw/articles/2026-10-05-github-research-briefing.md` 1차 대조). 같은 날 사용자 승인 ("ㄱㄱ") 으로 판정 실험 A1–A3 을 버리는 venv 에서 돌렸다 (아래).

## 핵심 사실 — 우리 질문과의 관계

| 분류 (처리 기준 [[daily-github-briefing-triage]]) | 판정 |
|---|---|
| ② 경쟁 · 비교 도구 | **예** — [[pyprobe]] 와 같은 electrode-balancing 계열 (창 4 + 전압 오프셋). 같은 곡선 정보를 쓰면 같은 축퇴를 공유할 수 있다 — 두 도구의 일치는 정답의 증거가 아니다 |
| 판정 대상 | **실측함 (2026-10-05)** — 우리 PyBaMM 합성 truth 로 참값 복원 · 불확도의 정직성을 봤다 (아래 "실측") |
| ③ 미세단락 도구 | **아니다** — 브리핑도 미세단락 판별 · ASSB 열화 원인 확정 도구가 아니라고 적었다. [[isc-detection-vs-balancing-masking]] 의 근거로 쓰지 않는다 |

`[해석]` 정보량: 피팅은 SOC 0–1 로 정규화한 형상에 창 4 + iR 을 맞추고, 절대 용량은 전지 `Ah` 로만 들어간다. [[np-lip-ocv-reparametrization]] 의
"형상 2 + 측정 총용량 1" 체제다 — 원리적으로는 세 모드가 복원 가능하지만 조건수가 문제다. PyProBE 와 달리 화학별 bounds 를 코드에 박지 않았다
(초기값 ± 상자 · [0, 1]).

## 불확도 — 정적 확인 두 가지 (2026-10-05 · 아래 실측 A2 · A3 이 실행으로 확인)

**1. LLI 불확도 식의 변수 혼동 — 브리핑 주장을 원문으로 확인했다.** `src/ampworks/dqdv/_lam_lli.py:108` (main `0f7a31c6` · 배포 `v0.1.0` 도 같은
줄) 의 "contribution from xp1" 항이 `xp1_std` 가 아니라 `xn1_std` 를 곱한다. 1차 Taylor 의 편미분을 직접 맞춰 보면
(`dQn = Ah/(xn1−xn0)²` · `dQp = Ah/(xp1−xp0)²`):

| 항 | ∂Inv/∂(·) | 코드의 계수 · 곱하는 std | 판정 |
|---|---|---|---|
| xn0 | `Qn + xn0·dQn` | 같음 · `xn0_std` | 맞다 |
| xn1 | `−xn0·dQn` | 같음 (제곱) · `xn1_std` | 맞다 |
| xp0 | `−Qp + (1−xp0)·dQp` | 같음 · `xp0_std` | 맞다 |
| xp1 | `−(1−xp0)·dQp` | 계수는 같음 (제곱) · **`xn1_std`** | **틀림 — `xp1_std` 여야 한다** |

`xp1_std` 는 84행에서 읽고 `Qp_std` (93행) 에만 쓰인다. 영향 범위는 **`LLI_std` 한 열**이다 — LLI · LAM · Q 의 점 추정과 `LAMn_std` ·
`LAMp_std` · `Qn_std` · `Qp_std` 는 이 줄을 거치지 않는다. `tests/` 에 `calc_lam_lli` · `LLI_std` 를 부르는 시험이 없다 — 시험이 이 줄을 잡을 길이 없었다.

**2. 대각만 쓰는 불확도 — 우리 주제와 직접 닿는 한계 (`[해석]`).** `_dqdv_fitter.py:588–596` 은 SSR 의 수치 Hessian 으로 5 × 5 공분산을
계산한 뒤 `std = sqrt(0.5·|diag(cov)|)` 만 남긴다. `calc_lam_lli` 는 xn0 · xn1 · xp0 · xp1 를 **서로 독립**으로 보고 전파한다. 창 파라미터가 강하게
상관된 경우 — 곧 [[fitting-degeneracy]] 가 말하는 flat valley — 가 정확히 이 근사가 깨지는 곳이다. [[np-lip-ocv-reparametrization]] 이 이미
짚은 문헌 관행 ("오차공분산 `C_θ` 를 계산해 놓고 `sqrt(diag)` 만 그린다") 과 같은 구조라, 축퇴 방향을 보여 줄 수 없다. 덧붙여 `abs()` 가 음의
대각 (Hessian 이 양정치가 아닐 때) 을 가린다 · 피팅은 MAPE, 불확도는 SSR 이라 저자 스스로 "heuristic" 이라고 적었다 · `LLI_std = inv_std /
inv[0]` 는 기준 행 (`inv[0]`) 의 불확도를 넣지 않는다.

## 실측 (2026-10-05 · `raw/repositories/2026-10-05-ampworks-on-synthetic-truth.md` · 결과 JSON 둘 동봉)

조건: ampworks 0.2.0.dev0 (main `0f7a31c6`) 를 스크래치패드의 버리는 venv 에만 설치 (운영 환경 · 저장소 설치 0). 곡선은 grid_curves_v4 (noise 0) 의
pristine + 조건 4 (LLI 단독 10 % · LAM_NE 단독 10 % · 혼합 10/10/10 · LAM_PE 단독 6 %) · 반쪽전지 OCP 는 우리 표 · 시작점 2 경로 (pristine 창
이어받기 · `grid_search(21)`) · 비용 항 4 (기본값 = 전압 + dQdV + dVdQ · 전압만 · dQdV 만 · dVdQ 만). 오차 = 추정 − 참값 (%p).

| 실험 | 결과 |
|---|---|
| **A1 점 추정** | dQdV 만: 8 적합 모두 ≤ 0.70 %p — 가장 안정 · dVdQ 만: 이어받기 ≤ 0.53 %p, 격자 경로의 LLI 단독만 다른 해 (LAM_NE −36.6 %p · 목적함수 0.181 ↔ 0.046) · **기본값: LLI 단독이 두 경로 모두 틀림** (이어받기 LLI +3.2 / LAM_PE +10.1 / LAM_NE +7.8 %p · 목적함수 0.327 · 격자 LLI −15.7 %p · 0.578), 나머지 세 조건 ≤ 0.68 %p · 전압만: LAM 오차 최대 ≈ 5 %p |
| A1 보충 (재시작 반복) | 기본값: 참값 근처로 오지만 목적함수가 반복마다 오르내린다 (0.1175–0.1228) · 전압 + dQdV: 13 번째까지 참값 근처 → 14 번째에 다른 해로 (목적함수 0.29) 빠진 뒤 돌아오지 않음. 매 호출이 iR 을 평균 잔차로 다시 잡고 ±0.1 상자를 새 시작점에 다시 두는 코드 구조가 원인 후보 (미확인) |
| **A2 108행의 크기** | 적합 32 개: 원래 / 고친 `LLI_std` = 0.24–6.7 배 (중앙 1.09) · 전압만에서 최대 6.7 배 과대 · 다른 열은 32 개 모두 같음 |
| **A3 불확도의 정직성** | 틀린 적합에서 **과소**: 기본값 · LLI 단독 — LAM_NE 오차 7.79 %p ↔ std 0.014 %p (전체 공분산으로도 0.17) · LLI 3.24 ↔ 0.54–0.90 · dVdQ 격자 — 36.6 ↔ ≈ 2.5. 맞은 적합에서는 과대 (dQdV 만: 0.22 ↔ 1.5–3.7). 전압만은 std 14–73 %p 로 정보 없음. **Hessian 이 32 중 28 에서 양정치가 아니다** — 18 은 음의 분산을 `abs()` 가 가렸고 27 은 상관계수 크기가 1 을 넘는다 (공분산이 성립하지 않음). 재구성한 공분산은 ampworks `x_std` 와 정확히 같다 (차 0) |

**판정 (2026-10-05):** watch 유지 · 우리 파이프라인의 대안 아님. 점 추정은 비용 항과 시작점에 민감하다 (이번 조건에서는 dQdV 만이 가장 좋았다).
틀린 답은 목적함수가 맞은 답의 2.8–4.9 배인 **국소 최소**라 같은 곡선을 똑같이 잘 맞추는 다른 답 (축퇴) 이 아니다 — 우리 degeneracy 질문의 직접
증거로 쓰지 않는다. 불확도 출력은 채택하지 않는다 — 108행은 고치면 되지만 Hessian 이 대부분 양정치가 아닌 것은 구조적 한계다. ampworks 예제 주석도
"국소 최소에 빠진 적합은 믿으면 안 되는 낮은 불확도를 줄 수 있다" 고 적었다 — A3 은 그 경고가 실제로 일어남을 참값으로 보인 것이다.

## upstream 알림 (초안 · 미발송 — 발송은 사용자)

재현은 ampworks 자체 예제 자료 (`examples/dqdv_data`) 와 패키지 데이터셋만 썼다 — 우리 자료 · A1–A3 결과 · 이름 · 연락처는 초안에 없다.

| # | 어디에 | 내용 | 확인 |
|---|---|---|---|
| 1 | Issue | `LLI_std` 의 xp1 항이 `xn1_std` (한 단어 수정 · 재현 · 제안 시험) — 예제 자료에서 cycle 2 `LLI_std` 0.0191 → 0.0095 · cycle 3866 0.0058 → 0.0084 | 제안 시험: 고치기 전 xn1 · xp1 실패 · 고친 뒤 통과 |
| 2 | Issue | **재현 중 새로 발견** — `constrained_fit` 이 `np.asarray(x0, dtype=float)` 뒤 `x0[-1] = iR0` 로 넘겨받은 배열 (앞 결과의 `.x`) 의 iR 을 제자리에서 덮어쓴다. 예제 순서 그대로면 cycle 2 행의 iR 이 0.0278 대신 0.0153 으로 표에 들어간다. LAM · LLI 는 영향 없음 | 제안 시험: 고치기 전 실패 · `np.array` 복사로 통과 |
| 3 | Discussion (선택) | 예제 자료에서도 SSR Hessian 이 양정치가 아니고 `abs()` 가 음의 대각을 가림 · 대각만 전파 · 기준 행 불확도 누락 | 출력만 |

검증: upstream `tests/test_dqdv` 기존 11 + 제안 5 를 네 판 (배포본 · 108행만 · x0 만 · 둘 다) 으로 돌려 3 · 1 · 2 · 0 실패 — 기존 11 은 네 판 모두 통과.
수정 diff 둘은 원본에 `git apply --check` rc 0. 중복: `refs/pull/1..39` 가 전부 PR 이라 #39 까지는 issue 가 없다 · #40 이후는 이 세션에서 볼 수 없었다
(발송 전 사용자 검색 몫).

**권고 순서 (2026-10-05 · 사용자 "1,2는 우리가 할 수 있는걸로 하자" — 우리 몫은 기록까지):** 초안을 이 기록으로 먼저 고정 → 사용자가 중복 검색 뒤
**1 · 2 를 같은 날 따로** 올림 → URL 을 받으면 이 절에 덧붙임 → **3 은 보류** (maintainer 반응을 본 뒤) → **PR 은 maintainer 가 원할 때만** (fork 필요).
초안 원문은 raw 의 마지막 절.

## 이 위키와의 관계

- 브리핑 분류 ②: [[pyprobe]] (같은 계열 · 실측 있음) 와 나란히 둔다. 우리 파이프라인의 대안이 아니라 **판정 대상**이다 — 실측은 위.
- 우리 저장소에서의 사용: 브리핑은 기본 가지만 보았다고 적었다 — 2026-10-05 로컬 원격 추적 가지 28 개를 텍스트 · 코드 파일에서 `git grep` 으로
  본 결과 **없음 (28 가지 모두 · 첫 검색에서 시간 초과한 3 가지는 재시도에서 없음)** (원문 출력은 raw 1차 대조 끝).

## 관련
- [[pyprobe]]
- [[fitting-degeneracy]]
- [[np-lip-ocv-reparametrization]]
- [[daily-github-briefing-triage]]
- [[isc-detection-vs-balancing-masking]]
- [[22p-physics-or-degeneracy]]
