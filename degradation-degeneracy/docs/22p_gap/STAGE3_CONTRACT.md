# 단계 3 계약 v2 — protocol 축 분해와 고정 restart bank

> 21차 실행 순서 4 로 v1 을 썼고, **22차 리뷰가 v1 의 출발 전제를 뒤집었다.**
> 이 문서는 그 뒤 판이다. 구현 전에 다시 심사받는다.
>
> `source_digest` 를 바꾸지 않는다 (`docs/` 는 RUN_SCOPE 밖). 여기 적힌 것을
> `src/` 에 넣는 순간 **기존 산출물 전부가 재실행 대상**이 된다.

## 0. v1 이 무엇을 틀렸나 — 후보는 늘지 않았다, 교체됐다

v1 은 21차 warm 실험을 "같은 random 4개에 warm 후보 하나를 더한 union" 으로
분류했다. **틀렸다** (22차 발견 1, 철회[WARM_UNION]).

```python
# src/fitting.py — restart 루프는 정확히 n_restarts 번 돈다
n_max = max(1, n_restarts)
for k in range(n_max):
    x0 = init if k == 0 else rng.uniform(lb, ub)
    src = ("warm" if warm_init else "base_init") if k == 0 else "random"
```

커밋된 투영의 `restart_sources` (3,069조건 전부 동일):

| arm · 목적함수 | 후보 구성 | 총 후보 |
|---|---|---:|
| no-warm 33p / 34p | `base_init=1;random=4` | 5 |
| warm 33p | `base_init=1;random=4` | 5 |
| **warm 34p** | **`random=4;warm=1`** | **5** |

`base_init` 이 **사라졌다.** 실험이 잰 것은 "warm 후보를 더하면" 이 아니라
**"slot 0 의 결정론적 후보가 `base_init` 이냐 `warm` 이냐"** 다.

**함의**: 34p 개선을 "warm 이 좋다" 로만 읽을 수 없다. **`base_init` 이 34p 에서
나쁜 후보였다**는 해석과 구별되지 않는다. v1 의 후보 수 정의·비용 추정·
"equal-cost" 명명이 전부 이 오류 위에 있었다.

회귀 `test_warm_replaces_the_deterministic_slot_it_does_not_add_one` 이 문장이
아니라 **실제 후보 배열**을 고정한다.

## 1. 실측된 교란 — 이제 다섯 가지

전부 코드·투영에서 확인한 것이지 가정이 아니다.

| # | 교란 | 근거 |
|---|---|---|
| 1 | `warm_start` 하나가 **원점과 조건 fitting 을 동시에** 바꾼다 | `src/fitting.py:862` 가 조건 task 를 그대로 물려받는다. 404 half-cell `p_ini(34p)` `[1.509716,…] → [1.518503,…]` |
| 2 | `--n-restarts` 는 실행 횟수가 아니라 **예산 상한** | adaptive 조기 종료. 2회 종료 행 223 → 238 |
| 3 | **noise 층을 바꾸면 restart 난수가 통째로 갈린다** | `cond_id = sha1(asdict(Condition))[:12]` 가 `noise`·`seed` 포함 (`src/grid.py:99`) → `task["seed"] = int(sha1(cond_id)[:8],16)` (`src/fitting.py:817`) |
| 4 | **warm 은 slot 을 교체한다** (§0) | 투영 `restart_sources` |
| 5 | **예산을 바꾸면 warm 후보 자체가 바뀐다** | 연쇄 구조 (`src/fitting.py:392-406`) — 33p 예산 ↑ → 33p 해 변화 → 34p 가 받는 warm 좌표 변화. 22차 발견 2 |

5번이 v1 의 "중첩 보장" 을 부분적으로 무효화한다. 중첩은 **random bank 접두사
에만** 성립하고, 34p 의 **전체 후보집합**은 앞 목적함수 해가 바뀌면 중첩되지
않는다.

## 2. protocol 축 — 목적함수별로 쪼갠다

```yaml
protocol:
  objective_order: [pocv_dvdq, pocv_dvdq_dqdv]

  # 예산은 목적함수별이다 (22차 발견 2). 축 하나로는 33p 예산 변화가
  # 34p 후보까지 끌고 간다.
  p_ini_budget_by_objective:      {pocv_dvdq: 20, pocv_dvdq_dqdv: 20}
  condition_budget_by_objective:  {pocv_dvdq: 20, pocv_dvdq_dqdv: 20}

  p_ini_warm_start:      false
  condition_warm_start:  false
  p_ini_candidate_mode:      union          # §3 의 세 값 중 하나
  condition_candidate_mode:  union

  adaptive: false
  p_ini_bank_sha256:       <64 hex>
  condition_bank_sha256:   <64 hex>
  bank_version:            1

  # 앞 목적함수 → 뒤 목적함수 warm 공급 관계. 암묵 규칙(`w_dqdv != 0`)에
  # 의존하지 않고 명시한다.
  warm_provider_map: {pocv_dvdq_dqdv: pocv_dvdq}

  # 실제로 쓴 후보 집합(조건 × 목적함수 × restart 의 source·bank index)의 digest.
  # 계획이 아니라 **실현값**이라 사후 검산의 앵커다.
  realized_candidate_map_sha256: <64 hex>
```

**`N` 의 정의를 한 번만 한다**: `*_budget_by_objective` 의 값 `N` 은
**random bank 에서 뽑는 점의 수**다. `base`·`warm` 은 별도이며 §3 의 mode 가
정한다. 총 시작점 수는 mode 에 따라 `N+1` 또는 `N+2` 다.

### 2.1 하위호환 — version-dispatched read-only (22차 Q3)

v1 은 "옛 필드를 아예 읽지 않는다" 였다. 22차가 **과하다**고 판정했다. 수정:

| 대상 | 규칙 |
|---|---|
| v6 writer / resume / canonical validator | 새 필수축이 하나라도 없으면 **실패** |
| v5 historical validator | 당시 v5 schema 로만 읽고 `historical_valid` 또는 `recorded_only` 로 표시 |
| v5 → v6 필드 추론 | **금지** (Q4 의 포괄적 동등 선언 통로) |
| v5 chunk 를 v6 resume 에 사용 | **금지** |
| v5 artifact 를 v6 canonical 로 승격 | **금지** |

즉 shim 이 아니라 **버전별 읽기 전용 검증기**다.

### 2.2 adaptive diagnostic arm 의 schema

v1 은 `adaptive=true` 와 bank digest 를 동시 지정하면 실패시키면서, 바로 다음
문장에서 adaptive 탐색을 `diagnostic_only` 로 허용했다 — 표현 불가능한 상태다
(22차 발견 2). 수정:

```yaml
adaptive: true
condition_bank_sha256: <64 hex>          # 필수 — 어느 bank 에서 뽑았는가
realized_candidate_map_sha256: <64 hex>  # 필수 — 실제로 **쓴** prefix
inference_status: diagnostic_only        # 강제. 다른 값 금지
```

adaptive arm 도 bank 를 기록하되 **실현 prefix 를 따로 봉인**하고 상태를
`diagnostic_only` 로 고정한다. bank digest 를 비우는 길은 두지 않는다 —
비우면 옛 난수 경로로 조용히 돌아간다.

## 3. 후보 정책 — 세 가지를 이름으로 구분한다

`M` = random bank 에서 쓰는 점의 수(= `*_budget_by_objective`).
아래는 **앞 목적함수의 warm provider 가 실제로 있는** 목적함수에 대한 정의다.
provider 가 없는 연쇄 1번째는 어느 mode 에서도 `[base] + bank[:M]` 이다.

| mode | no-warm arm | warm arm | 총 시작점 |
|---|---|---|---|
| `legacy_slot_replace` | `[base] + bank[:M]` | `[warm] + bank[:M]` | 양쪽 `M+1` |
| `equal_start_count_base_retained` | `[base] + bank[:M]` | `[base, warm] + bank[:M-1]` | 양쪽 `M+1` |
| `union` | `[base] + bank[:M]` | `[base, warm] + bank[:M]` | `M+1` vs `M+2` |

- **21차 실험 = `legacy_slot_replace`** (§0).
- v1 의 "equal-cost" 라는 이름은 쓰지 않는다 (22차 발견 1). 시작점 수가 같아도
  각 시작점의 `n_eval` 이 달라 계산비용은 같지 않다. **`equal_start_count`** 로
  부르고 `n_eval` 합과 wall time 을 **따로 기록**한다.
- 세 mode 를 섞어 하나의 결론에 쓰지 않는다.

회귀는 문장이 아니라 다음을 고정한다: 후보 ID 목록 · 각 후보의 `source`·bank
index·초기 좌표 digest · 총 후보 수 · 총 `n_eval`.

## 4. restart bank — 행 단위로, unit cube 에서

### 4.1 지금 구조의 문제 (교란 3)

같은 물리 조건이라도 noise 층이 다르면 다른 난수 초기값을 받는다. noise 를
재려는 모든 비교가 optimizer draw 효과와 섞인다.

### 4.2 ID 설계 (22차 발견 3 · Q1)

v1 은 물리좌표 hash 하나였다. 부족하다.

```text
latent_pair_id = H( pairing_design_id,
                    canonical(lli, lam_pe, lam_ne, lam_pe_type, lam_ne_type),
                    parameter_order_sha256 )

bank_id = H( latent_pair_id, bank_version, unit_cube_bank_sha256 )

mapped_candidate_id = H( bank_id, exact_bounds_sha256, mapped_parameter_bytes )
```

- **treatment·noise·noise_seed·objective 를 제외**한다 — 같은 paired family
  안에서 arm 들이 같은 latent draw 를 받아야 하기 때문이다.
- 다만 "같은 좌표면 무조건 같은 그룹" 은 과하다. **`pairing_design_id`** 아래
  에서만 묶는다. 짝지을 의도가 없는 실험은 여기서 갈린다.
- **`bounds_preset` 이름이 아니라 실제 ordered `lb/ub` 의 digest** 를 쓴다.
  난수가 `rng.uniform(lb, ub)` 라 bound 가 바뀌면 같은 난수도 다른 점이다.
- bank 는 **unit cube 에서 먼저 생성**하고 bounds mapping 을 별도 digest 로
  남긴다. 그래야 bound 가 다른 arm 사이에서도 "같은 latent draw" 를 말할 수 있다.
- float canonicalization 규칙과 **truncated-ID 충돌 검사**를 구현에 포함한다.
- treatment 별 reference/cache digest 는 pair ID 가 아니라 **각 leg identity** 에
  기록한다.

### 4.3 저장 단위 — leg scalar 가 아니라 행 (22차 발견 3)

다리 하나에 수백 개 물리 조건이 있다. v1 의 leg 수준 `pair_group_id` 는
표현 자체가 틀렸다.

| 어디에 | 무엇 |
|---|---|
| fits / restart 행마다 | `pair_group_id`, `candidate_id`, bank index, latent 좌표 digest |
| leg manifest | `n_pair_groups`, `cond_id → pair_group_id` mapping digest |
| arm 간 검사 | pair-group 집합과 중복도가 **정확히 같은가** |

### 4.4 중첩 접두사 — 어디까지 보장되나

`bank[0:5] ⊂ bank[0:10] ⊂ bank[0:20] ⊂ bank[0:40]` 은 **random bank 에만**
성립한다. 34p 의 전체 후보집합은 앞 목적함수 해가 예산과 함께 바뀌므로
중첩되지 않는다 (교란 5). 그래서 예산 실험은 다음 중 하나로만 한다.

1. `*_budget_by_objective` 로 목적함수별 예산을 따로 움직인다, 또는
2. **provider 예산과 조건별 provider-solution map 을 먼저 고정·봉인**하고,
   그 고정 seed 위에서 34p 예산만 비교한다.

warm seed 가 예산과 함께 바뀌는 실험을 "nested candidate set" 이라고 부르지
않는다.

## 5. half-cell 2×2

`p_ini` 가 있는 것은 half-cell 기준뿐이다.

| arm | `p_ini_warm_start` | `condition_warm_start` | 분리하는 것 |
|---|---|---|---|
| A | off | off | 기준선 |
| B | on | off | 원점 이동 단독 |
| C | off | on | 조건 warm 단독 |
| D | on | on | 상호작용 (현재 기본값) |

- 네 arm 이 같은 bank·같은 목적함수별 예산·`adaptive=false`·같은
  `candidate_mode` 를 쓴다.
- 격자 기준은 `p_ini = null` → **C vs A** 한 축만 필요하다.
- **사전 예측(기록)**: B·D 에서 원점이 같은 값으로 이동하고, **C 의 원점은 A 와
  자리별로 동일**해야 한다. C 의 원점이 움직이면 축 분리 구현이 틀린 것이다.

## 6. plateau — truth 를 쓰지 않는다 (22차 발견 4 · Q2)

v1 은 "truth-free" 라고 선언하면서 `degenerate` 전이율을 hard gate 로 썼다.
이 저장소의 `degenerate` 는 `|추정 − truth| > tol` 이므로 **truth 를 쓴다.**
모순이었다.

### 6.1 절차

1. `p_ini` 와 조건별 **warm-provider solution map** 및 그 digest 를 먼저 고정.
2. 각 condition/objective 에서 **nested random-bank prefix 만** 늘린다.
3. `J_N − J_2N` 을 절대+상대 tolerance 로 비교한다. nested 이면 비증가여야 한다
   (증가하면 구현 오류).
4. material 개선이 남은 조건 비율과 개선량 분포를 본다.
5. solver 실패·비유한값·**실제 `n_eval`** 을 따로 기록한다.

### 6.2 예산 선택 hard gate — 넷으로 좁힌다

| gate | 기준 |
|---|---|
| nested 단조성 | `J_2N ≤ J_N` (위반 = 구현 오류) |
| material `ΔJ` | `J_N − J_2N > max(abs_tol, rel_tol·max(1,\|J_2N\|))` 인 조건 비율 ≤ 1% |
| solver 건전성 | 실패·비유한 0건 |
| sentinel 안정성 | 아래 panel 전체에서 **연속 두 번의 doubling** 이 위 셋을 통과 |

`abs_tol`·`rel_tol` 은 구현 시 사전 등록한다. v1 이 `agree_tol` 과 같다고 쓴
것은 부정확했다 — 코드의 비교식은 `1e-3 * max(1, |min(J0,J1)|)` 이라 작은 `J`
에서는 사실상 절대 `1e-3` 이다.

### 6.3 gate 에서 **뺀** 것 (결과 민감도 표로만 보고)

- 추정 파라미터 `p` 의 이동 — 좌표 scale 의존적이고, flat valley 는
  **과학적 결과**이지 예산 부족이 아니다. gate 로 두면 진짜 non-identifiability
  때문에 예산을 끝없이 늘린다.
- truth 기반 `degenerate` 전이 — §6 의 전제 위반.
- restart-source 승자 구성 — v1 의 `≤2%p` 는 **근거 없는 임의값**이었고,
  bank 점이 전부 `random` 라벨이라 "bank 후반부 승리" 를 측정하지도 못한다.
  bank index 를 행에 남기면(§4.3) 그때 별도 지표로 다시 볼 수 있다.

### 6.4 sentinel panel — 하나로 정하지 않는다

v1 은 무왜곡 dense half-cell 하나로 전체 예산을 정하려 했다. §12 의
"이 격자·화학·bound 에만 해당" 한계와 정면으로 충돌한다.

panel 에 반드시 포함: **half-cell / grid** 두 reference · **clean / noisy** ·
**smooth(33p) / dQdV(34p)** · 대표 **hard·boundary** 조건. 각각에서 필요한 `N`
을 구하고 **가장 큰 값을 채택**한다.

`J` 비교는 **같은 condition · 같은 objective · 같은 reference** 의 `N ↔ 2N`
안에서만 한다. 목적함수 사이의 `J` 는 비교 대상이 아니다.

두 번의 연속 doubling 도 수학적 보장이 아니라 engineering heuristic 이다.
사전 최대 `N` 까지 전부 보고한다.

## 7. estimand — primary 를 하나 고른다 (22차 Q4)

연구 질문은 "dQ/dV 정보가 복원을 개선하는가" 다. 그렇다면 primary 는:

> **같은 reference · 같은 exact bounds · 같은 `p_ini` protocol 아래,
> warm 없이 같은 `base` 와 같은 고정 random bank·같은 후보 수로
> 33p 와 34p 를 비교한 optimizer-controlled paired contrast**

- reference 는 **grid** (`p_ini = null`) 를 쓴다 — half-cell 은 목적함수별
  `p_ini` 가 따로 계산돼, 순수한 "dQ/dV 항 하나" 가 아니라 **objective-specific
  calibration 을 포함한 pipeline contrast** 가 된다.
- primary endpoint 는 aggregate 차이 **와** condition-level **transition table**
  둘 다다 (§7.1).

### 7.1 transition table 이 primary 인 이유 (실측)

`paired_fixed5_v4_warm` 안에서 33p ↔ 34p (recoverable 1,476조건):

| | 34p pass | 34p fail |
|---|---:|---:|
| **33p pass** | 381 | **186** |
| **33p fail** | **167** | 742 |

aggregate 는 `909 → 928`, +19 다. 그런데 **불일치가 353/1476 = 23.9%** 다.
두 목적함수는 "거의 같은 답" 을 내는 것이 아니라 **네 조건 중 하나에서 서로
다르게 판정**하면서 총량만 비슷하다. aggregate 하나로 보고하면 이것이 사라진다.

**통계 한정**: 이 격자는 확률표본이 아니라 결정론적 조건집합이므로 전이 건수는
**기술통계**다. McNemar p-value 나 모집단 확률로 옮기려면 조건 표집 모형과
독립 반복을 먼저 정의해야 한다.

### 7.2 secondary

| arm | 무엇을 재나 |
|---|---|
| `legacy_slot_replace` | 21차 실험 재현 — optimizer 초기화 민감도 ablation |
| `equal_start_count_base_retained` | warm 을 넣는 대신 random 하나를 빼는 ablation |
| `union` | 추가 후보까지 허용한 **운영 cascade** 성능 |

운영 성능을 주 질문으로 바꾸면 `union` 이 primary 가 될 수 있다. 다만 그
결론은 "dQ/dV 정보 자체" 가 아니라 **warm 을 포함한 알고리즘 bundle** 의
성능이다. co-primary 로 두려면 두 가설·판정 규칙·다중성 처리를 **사전에**
적는다. 결과를 보고 유리한 쪽을 정본으로 고르지 않는다.

## 8. leg 상태와 index

| `inference_status` | 뜻 | 인용 |
|---|---|---|
| `canonical` | 새 protocol 정본 | ✅ |
| `historical_valid` | 옛 source commit 의 완전 bundle 로 재검증 가능 | 조건부 (regime 병기) |
| `recorded_only` | summary/manifest/투영만 남아 원자료 독립 재계산 불가 | ❌ 진단만 |
| `diagnostic_only` | 교란·교차-digest·adaptive → 인과 결론 부적합 | ❌ 진단만 |
| `superseded` | 새 protocol 정본으로 대체됨 | ❌ |
| `excluded` | 원점 오염 등으로 폐기 | ❌ |

정확히 하나여야 한다. 현재 warm-probe 8다리는 `recorded_only`.

### 8.1 `leg_index.yaml`

```yaml
schema_version: 2
legs:
  - leg_id: hc22p_v6_armC_b20
    pairing_design_id: p22_halfcell_2x2_v6
    n_pair_groups: 640                    # ★ leg scalar pair_group_id 는 없다
    cond_to_pair_sha256: <64 hex>         #   행 단위 mapping 의 digest
    treatment: null                       # ★ 무왜곡이면 null (v1 예시가 틀렸다)
    source_commit: <40 hex>
    producer_source_digest: <16 hex>
    fit_source_digest: <16 hex>
    analyzer_source_digest: <16 hex>
    inputs_sha256: {curves: <64 hex>, fits: <64 hex>}
    reference: halfcell
    target_column: v_full_noisy
    exact_bounds_sha256: <64 hex>         # ★ preset 이름이 아니라 ordered lb/ub
    parameter_order_sha256: <64 hex>
    condition_ids_sha256: <64 hex>
    protocol: {...}                       # §2 를 그대로
    p_ini_cond: <12 hex>
    projection_sha256: <64 hex>
    restart_projection_sha256: <64 hex>
    analysis_spec_sha256: <64 hex>
    inference_status: canonical
    canonical_output: docs/22p_gap/<file>
    claim_ids: [P22_DQDV_PAIRED]
```

`producer`/`fit`/`analyzer` digest 를 따로 적는 이유: 곡선 생성기가 불변이면
`curves.parquet` 을 새 fitting 의 입력으로 재사용할 수 있다.

**단, 조건이 있다** (22차 Q5): `pair_group_id` 를 **봉인된 curves 의 기존 좌표
열에서 결정론적으로 유도**해야 한다. 새 producer column 을 필수화하면 기존
curves 가 새 schema 를 못 만족해 재생성이 필요해진다.

## 9. 재실행 목록 — v1 은 불완전했다 (22차 Q5)

### 9.1 v1 에 없었는데 필요한 것

| # | 무엇 | 왜 |
|---|---|---|
| 1 | **seed/grid 별 0 mV matched control** | 6격자 × PE 2/5/10 mV 를 돌리려면 seed 마다 같은 protocol 의 무왜곡 대조가 필요하다. seed 404 하나가 나머지 다섯의 control 이 될 수 없다. dense PE 1/1.5 mV·`bias_ne2mv`·`bias_both2mv`·`bias_pest095` 도 같은 protocol 의 dense 0 mV control 이 필요하다 |
| 2 | **grid-reference plateau sentinel** | half-cell pilot 하나로 grid 예산을 정할 수 없다 |
| 3 | **비-PE 다리 재실행 또는 격하** | `bias_ne2mv`·`bias_both2mv`·`bias_pest095` 를 계속 해석에 쓸 것이면 새 protocol 로 다시 돌린다. 아니면 그 claim 을 `historical_valid`/`diagnostic_only` 로 격하한다 |
| 4 | **hard/noisy/boundary sentinel** | clean dense half-cell 만으로 예산을 고르면 가장 어려운 지형을 놓친다 |
| 5 | **후보 정책별 arm** | §3 의 세 mode 중 무엇을 돌릴지 사전 확정. 다 돌리면 arm 수가 v1 표보다 늘어난다 |
| 6 | **고유 leg 목록** | "새 5 mV matched 짝" 과 6격자 5 mV 행이 중복인지 leg ID 단위로 풀어 쓴다 |

plateau pilot 출력이 **동일 curves/reference/bounds/bank/protocol** 의 control
이면 1번과 공유해 중복 실행을 피한다.

### 9.2 산출물 이름

기존 `*_v4` 이름을 **재사용하지 않는다.** v6/protocol 을 드러내는 새 디렉터리에
쓴다 (예: `results/p22_v6_gridC_b20/`). 같은 이름에 다른 protocol 을 쓰면
투영·index 대조가 무의미해진다.

### 9.3 비용 — v1 의 12시간 추정은 폐기

v1 추정은 (a) 후보 수 의미가 틀렸고 (b) 목적함수별 예산이 없었고 (c) §9.1 의
arm 이 빠졌다. **재산정 전까지 실행 승인을 요청하지 않는다.**

재산정에 필요한 것: §9.1 을 반영한 **고유 leg 목록**과 leg 마다
reference·treatment·curves digest·objective order·목적함수별 예산·두 warm
축·candidate mode·exact bounds digest·bank digest. 그것이 있어야 중복 제거와
비용 검산이 된다.

측정 기준값(실측): `paired_fixed5_v4_warm` = 3,069조건 × 2목적함수 ×
예산상한 5 → **833초** (nproc 28, `adaptive=False`). restart 하나당 약
`0.027초` (wall, 28병렬).

## 10. 보존 (22차 Q6)

투영은 **행 비교와 recorded snapshot 에 충분하고 citation canonical 에는
불충분**하다. 지지하지 못하는 것: input snapshot 과 실행 provenance ·
restore → validate → score → analyze.

v2 투영이 부분적으로 좁혔다 — 실제 fits 바이트 SHA 를 계산해 summary·manifest
와 **삼중 대조**하고, 봉인 summary **전체**(`by_objective_noise`·
`restart_conditioned`·`multistart*` 포함)를 재계산해 대조하며, restart 수준
투영으로 random-only 다봉성을 독립 재계산할 수 있다.

| 단위 | 보존 |
|---|---|
| `canonical` 승격 leg | content-addressed `fits.parquet` · manifest · summary · 투영 + **restore 후 validate receipt** |
| 고유 input digest | `_inputs/` 를 외부 content-addressed 저장소에 **한 번만** (중복 제거) |
| 도구 경로 smoke | grid·half-cell·distortion 경로별 최소 한 번의 end-to-end restore→validate→score→analyze |
| Git | full SHA·크기·보관 위치·receipt 를 담은 index |

여덟 다리를 63 MB 씩 Git 에 중복 커밋할 필요는 없다. 그러나 **citation-ready 로
승격하려면 각 leg 의 fits 는 접근 가능해야 한다.** 원자료를 보존하지 않는
다리는 `recorded_only` 로 남기는 것이 정직하다.

## 11. 구현 순서

1. 현 warm 실험을 `legacy_slot_replace` 로 재분류 — **완료** (§0, 회귀 포함)
2. candidate mode 3종과 `N` 의 의미 확정 — **이 문서 §3**
3. 행 단위 pair mapping · exact bounds/parameter digest 스키마 — §4
4. 목적함수별 예산 또는 provider-solution map 고정 — §2·§4.4
5. truth-free plateau + sentinel panel — §6
6. primary/secondary estimand + transition endpoint 사전 등록 — §7
7. claim → leg coverage 표와 고유 재실행 목록 · 비용 재산정 — §9
8. 투영 생성기에 실제 fits SHA · validate · 전체 semantic 대조 — **완료** (v2)
9. claim registry 양방향 완전성 · fence 구조 검사 — **완료**
10. `/lean-review` detached/no-upstream — **완료**
11. **여기까지 문서·회귀 재심사** ← 지금 여기
12. 그 다음에만 RUN_SCOPE 변경과 pilot 실행

2~7 은 이 문서가 **정의만** 했고 구현은 없다. 12 를 시작하면 `source_digest`
가 바뀐다.

## 12. 이 계약이 스스로 못 하는 것

- **`pair_group_id` 로도 잡음 *지형* 축은 분리되지 않는다.** 분리되는 것은
  초기값 축뿐이다. 잡음 실현 자체가 목적함수 지형을 바꾸므로 같은 초기값에서
  출발해도 경로가 갈린다. 그 이상은 같은 잡음 실현을 여러 seed 로 반복해야
  잴 수 있고 이번 범위 밖이다.
- **plateau 는 sentinel panel 이 덮는 범위의 성질**이다. panel 밖으로
  일반화하지 않는다. 특히 **2×2** 는 half-cell 한 격자에서만 성립한다
  (격자 기준에는 `p_ini` 가 없다).
- **세 candidate mode 를 다 돌려도 "옳은 protocol" 은 정해지지 않는다.**
  정해지는 것은 세 estimand 의 값이다. 어느 것을 운영 정본으로 삼을지는
  사전 등록된 primary endpoint 가 정하는 것이지 결과가 정하지 않는다.
- **transition table 은 기술통계다.** 이 격자는 확률표본이 아니다.
