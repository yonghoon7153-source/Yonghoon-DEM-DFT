---
title: "MD 생산길이 표준 — `MDadaptive-v2` (200 ps 고정을 순차 연장으로 바꾼다)"
date: 2026-08-27
updated: 2026-08-27
tags: [methodology, md, protocol, uncertainty]
status: 채택
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: medium
claimType: prescriptive
evidenceScope: multi-source-primary
---

# `MDadaptive-v2` — 고정 200 ps 를 **순차 연장**으로 바꾼다

> 채택 근거: 교차리뷰 H Q12 (2026-08-27). *"`200→800 ps` 고정 교체보다는 순차 연장
> 표준이 낫다."* 고정 교체는 기존 자료와 프로토콜을 갈라 비교를 깨뜨린다.

## 1. 왜 바꾸나 — 200 ps 는 block CI 를 못 낸다

block 하한은 `b ≥ max(t₂_max, g·Δo)` 이고 유효 block 수는 **`(T − t₂_max)/b`** 다
(⚠ `T/b` 가 아니다 — `q_o` 를 만들 수 있는 마지막 시간원점이 `T − t₂_max` 에서 끝난다).
발행 하한은 **8–10 개**:

| T | τ_int 10 ps | 25 ps | 50 ps |
|---|---:|---:|---:|
| 100 ps | 1.0 | 1.0 | 0.5 |
| **200 ps** ← 옛 표준 | **3.0** | **3.0** | **1.5** |
| 800 ps | 15.0 | 15.0 | **7.5 ← 경계** |
| 1600 ps | 31.0 | 31.0 | 15.5 |

**800 ps 도 자동 합격이 아니다.** τ≈50 ps 면 하한 아래다 — 그래서 **고정 길이가 아니라
사전 종료기준으로** 끊는 게 맞다.

⚠ **8–10 blocks 는 발행 기준이지 점추정치를 무효화하는 정리가 아니다.**
기존 200 ps 결과는 **조건부 유지**다 (§4).

## 2. 프로토콜

| 판 | 무엇 |
|---|---|
| `MD200-v1` | 기존 고정 200 ps. **폐기하지 않는다** — 이미 나간 값들의 프로토콜 이름이다 |
| **`MDadaptive-v2`** | **200 → 400 → 800 → 1600 ps checkpoint**. 사전 기준을 만족하면 종료 |

### 사전 종료기준 (전부 만족해야 끝낸다)

1. **primary `D_inc` plateau** — 연속된 후기 두 구간에서
   `CI₉₅{log(D_j / D_{j+1})} ⊂ [−log(1+ε), +log(1+ε)]`, ε 는 사전 등록.
   ⛔ "CI 가 0 을 포함한다" 가 아니라 **사전 허용폭 등가성 검정**이다.
2. **ACF/창 및 block-SE 안정** — block 크기를 `b · 1.5b · 2b` 로 바꿔 SE 가 평평한가.
3. **충분한 block-equivalent 와 사건수** — `(T − t₂max)/b ≥ 8`, 그리고 committed 사건수.
4. **느린 상태 혼합 확인** — PS₄ 회전 등. 궤적에서 상태전이가 0–1회뿐이면
   block 을 늘릴 문제가 아니라 **equilibrium 이 미표집**된 것이다 ⇒ `unresolved`.
5. **목표 상대오차 충족**.

⛔ CI 가 넓거나 `D_inc` 가 음수면 `PASS` 가 아니라 **`UNRESOLVED`** 다.

### 저장 규약 — **200 ps prefix 를 반드시 같이 남긴다**

모든 v2 런은 `traj.xyz` 를 **증분 기록**하므로(2026-08-27 드라이버 수정) prefix 분석이
공짜다. 비교 규칙:

- **기존 자료와 비교**: 200 ps prefix 끼리
- **장시간 주장**: v2 최종값 끼리
- ⛔ **분자와 분모의 궤적 길이가 다르면 안 된다** — 유한크기와 유한시간이 섞인다
  (회신 H 1-b). 지금 lpsocl 큰 셀·작은 셀을 **둘 다 800 ps** 로 도는 이유가 이것이다.

### 소급 보정은 하지 않는다

저·중·고 이동도 조건을 골라 **같은 궤적의 200/400/800 ps prefix 를 paired bridge** 로 쓴다.
⛔ **하나의 보정계수를 전 캠페인에 소급 적용하지 않는다.**

## 3. 관련 도구

| 무엇 | 어디 |
|---|---|
| `D_inc` (절편 없는 축) | `msd_diffusive_check.py --scan` 의 `★D_inc` 행 |
| 창 등급 (primary/sensitivity/exploratory) | 같은 도구, `~`·`!` 표시 |
| 방향별 확산텐서 | `msd_diffusive_check.py --directional` |
| 누적 prefix | 같은 도구, `--prefixes 100,200,400` |
| `τ_int` · block 하한 | `tau_int_geyer()` — ⚠ `block_min_ps` 가 **이미 `2·τ_int`** 다 |
| 증분 궤적 | `disorder_ensemble_diffusion.py` (스냅샷마다 append) |

## 4. 기존 `MD200-v1` 값의 지위 — **조건부 유지**

교차리뷰 H Q12 판정 그대로:

> 이 값은 동일한 200 ps 프로토콜의 독립 초기화 3–4개에서 얻은 **finite-duration 추정치**다.
> 제시한 산포는 200 ps run 간 변동이며 **단일궤적 block CI 도, 장시간 극한의 수렴도
> 뜻하지 않는다.** 유한시간 편향·느린 basin 혼합·무질서 realization 불확실도는
> 분리되지 않았다.

**표기 규약**

| 양 | 표기 |
|---|---|
| 활성화에너지 | **`Ea_200, provisional`** — 유한시간 편향이 온도별로 다르면 기울기도 편향된다. 각 온도의 **seed-level `log D`** 를 직접 쓴다 |
| Nernst–Einstein 전도도 | **`σ_NE,200`** — 실제 collective conductivity 로 **확대 금지** |
| 불확실도 | `mean ± SD_seed` 는 **run-to-run 산포**이지 평균의 CI 가 아니다. `SD/√n` 은 n=3–4 라 매우 불안정 |

원고에는 **평균·SD 만 두지 말고 각 seed 값을 함께** 보인다. 95 % CI 가 꼭 필요하면
`log D` 에서 small-sample t 구간을 쓰되 **"200 ps 프로토콜 평균의 조건부 CI"** 라고 명시한다
(`D∞` 가 아니다).

**반영 위치**: `db/properties/canonical_registry.json` 의 MD 항목 8건에
`finite_duration` 블록과 `prohibitions: [single_trajectory_CI, long_time_convergence]` 를 넣었다.
`li_transport.json` · `md_run_ledger.json` 도 같은 단서를 달았다.

## 5. ⛔ 이 표준이 못 하는 것

- **소급 보정을 주지 않는다.** 기존 값을 새 값으로 바꾸는 계수는 없다.
- **τ_int 를 자동으로 정해주지 않는다.** `tau_int_geyer()` 는 후보를 줄 뿐이고,
  SE plateau 확인은 사람이 해야 한다. back-jump 반상관이면 `g` 만 보면 놓친다 —
  `memory_horizon_ps` 를 같이 본다.
- **무질서 realization 불확실도를 다루지 않는다.** 그건 독립 disorder 시드의 몫이고,
  원셀 타일링은 **세 무질서 시드가 아니다**.
