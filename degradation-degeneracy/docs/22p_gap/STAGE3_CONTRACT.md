# 단계 3 계약 v4 — protocol 축 분해, 고정 restart bank, 보존 트랜잭션

> v1(21차 순서 4) → **22차가 출발 전제를 뒤집어** v2 → **23차가 v2 의 자기모순
> 여섯 개를 찾아** v3 → **24차 + 24차 보충이 보존 축을 요구해** v4.
> 구현 전에 다시 심사받는다.
>
> **v4 가 더한 것**: 24차가 남긴 묶음 1~6 은 그대로 미결로 유지하고, 24차
> 보충이 P0 로 추가한 보존 묶음 7~10 을 §13 에 적는다. 상태 3축의 **허용
> 조합표**(묶음 7)는 §8 에 들어갔다 — 축별 membership 만으로는
> `missing / unvalidated / canonical` 같은 불가능한 튜플이 통과했다.
>
> v3 가 고친 것: 후보 예산 `N` 의 이중 의미(P0-1) · `pair_group_id` 이름과
> 후보 ID 범위, `n_pair_groups` 640→320(P0-2) · provider freeze 미봉인(P0-3) ·
> tolerance 가 수치가 아님(P0-4) · sentinel 목록 부재(P0-5) · primary 표가
> warm arm 이었고 status 축이 뒤섞임(P0-6) · 소급 재실행 문구와 비용 모델(P0-7).
>
> `source_digest` 를 바꾸지 않는다 (`docs/` 는 RUN_SCOPE 밖).
>
> **★ 23차 P0-7 정정** — v2 는 여기 "기존 산출물 **전부**가 재실행 대상" 이라고
> 썼는데 §2.1 의 historical read-only 정책과 모순이다. 정확한 문장:
>
> > Stage 3 구현 뒤 **v6 canonical claim 을 지지하거나 v6 resume 에 쓰는**
> > 산출물은 새 source digest 로 다시 생성한다. 기존 artifact 는 당시
> > source·protocol 아래의 historical/recorded status 를 유지하며 **소급
> > 무효화하지 않는다.**

## 0. v1 이 무엇을 틀렸나 — 후보는 늘지 않았다, 교체됐다

<!-- QUARANTINE:WARM_UNION -->
> **⛔ 철회[WARM_UNION]** — v1 은 21차 warm 실험을 "같은 random 4개에 warm
> 후보 하나를 더한 union" 으로 분류했다. **틀렸다** (22차 발견 1).
<!-- /QUARANTINE -->

실제로는 slot 0 의 결정론적 후보가 **교체**됐다. 양 arm 의 후보 수는 5로 같다.

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

  # 앞 목적함수 → 뒤 목적함수 warm 공급 **관계**. 암묵 규칙(`w_dqdv != 0`)에
  # 의존하지 않고 명시한다.
  warm_provider_map: {pocv_dvdq_dqdv: pocv_dvdq}

  # ★ 23차 P0-3 — 관계 이름만으로는 **값이 고정되지 않는다.** provider 예산이
  #   바뀌면 warm 좌표가 통째로 바뀐다 (교란 5). 실제 해를 봉인한다.
  p_ini_provider_artifact_sha256:      <64 hex>
  p_ini_provider_solution_map_sha256:  <64 hex>
  p_ini_values_sha256:                 <64 hex>
  condition_provider_artifact_sha256:      <64 hex>
  condition_provider_solution_map_sha256:  <64 hex>
  provider_protocol_sha256:            <64 hex>

  # 실제로 쓴 후보 집합(조건 × 목적함수 × restart 의 source·bank index)의 digest.
  # 계획이 아니라 **실현값**이라 사후 검산의 앵커다.
  realized_candidate_map_sha256: <64 hex>
```

**★ 23차 P0-1 정정 — `N` 하나로 두 뜻을 겸하면 안 된다.**

v2 는 `N` 을 "random bank 점 수" 로 정의했다. 그런데 §3 의
`equal_start_count_base_retained` warm arm 은 `bank[:M-1]` 을 쓴다 — 같은
budget 필드가 mode 에 따라 **다른 random 수**를 뜻한다. 예산을 축으로 쓰는
실험에서 이것은 치명적이다.

기준을 **총 시작점 예산 `B`** 로 바꾼다. random prefix 길이는 mode 가 정하는
파생값이고, 필요하면 `random_bank_prefix_len` 으로 **따로** 적는다.

```yaml
protocol:
  total_start_budget_by_objective: {pocv_dvdq: 20, pocv_dvdq_dqdv: 20}   # B
  # 아래는 계획·실현을 모두 남긴다 — 계획만 적으면 사후 검산이 안 된다
  planned_counts:  {base: 1, warm: 0, random: 19}
  realized_counts: {base: 1, warm: 0, random: 19}
  random_bank_prefix_len: 19
  total_n_eval: <int>
  wall_time_s: <float>
```

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

**`B`** = 총 시작점 예산 (= `total_start_budget_by_objective`, §2).
아래는 **앞 목적함수의 warm provider 가 실제로 있는** 목적함수에 대한 정의다.
provider 가 없는 연쇄 1번째는 어느 mode 에서도 `[base] + bank[:B-1]` 이다.

| mode | no-warm arm | warm arm | 총 시작점 |
|---|---|---|---|
| `legacy_slot_replace` | `[base] + bank[:B-1]` | `[warm] + bank[:B-1]` | 양쪽 `B` |
| `equal_start_count_base_retained` | `[base] + bank[:B-1]` | `[base, warm] + bank[:B-2]` | 양쪽 `B` |
| `union` | `[base] + bank[:B-1]` | `[base, warm] + bank[:B-1]` | `B` vs `B+1` |

`B` 를 기준으로 하면 mode 를 바꿔도 **총 시작점 수의 뜻이 안 변한다.**
random prefix 길이(`B-1` 또는 `B-2`)는 파생값이며 manifest 의
`random_bank_prefix_len` 에 실현값으로 적는다.

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
pair_group_id = H( pairing_design_sha256,
                   canonical(lli, lam_pe, lam_ne, lam_pe_type, lam_ne_type),
                   parameter_order_sha256 )

bank_id       = H( pair_group_id, bank_version, unit_cube_bank_sha256 )

candidate_id  = H( bank_id, exact_bounds_sha256, source, source_payload )
```

**★ 23차 P0-2 — 이름을 하나로 통일한다.** v2 는 `latent_pair_id` 와
`pair_group_id` 를 섞어 썼다. 정본은 **`pair_group_id`** 하나다.

**`pairing_design_id` 를 사람이 쓰는 자유문자로 두지 않는다.** 오타 하나로
조용히 merge/split 된다. label 과 canonical digest 를 분리한다:

```yaml
pairing_design_label:  p22_grid_primary        # 사람용 별칭
pairing_design_sha256: H(canonical_design_spec) # 정본
```

`canonical_design_spec` 최소 구성:

| 항목 | 왜 |
|---|---|
| schema/version, 물리좌표 canonicalization·단위 | float 표현이 갈리면 같은 조건이 다른 ID 가 된다 |
| varied treatment axis 의 **종류**와 arm 역할 | 값 자체는 pair ID 에서 제외 — 값을 넣으면 arm 이 갈린다 |
| pair ID 에서 제외하는 축과 **이유** | 제외 결정 자체가 설계다 |
| parameter order, bounds-equivalence policy | 실제 ordered bounds 값은 candidate/leg identity 에 |
| objective plan, parameter-coordinate schema | treatment 별 reference/cache bytes 는 leg identity 에 |
| bank generator/version/seed derivation, dtype·endian·serialization | 재현의 전제 |

**`candidate_id` 는 random 만 다루면 안 된다** (23차 P0-2). 세 source 전부:

| source | `source_payload` |
|---|---|
| `base_init` | base 좌표의 exact bytes digest |
| `warm` | provider objective · provider artifact sha · solution-map sha |
| `random` | bank index + unit-cube bytes digest |

arm 간 검사는 pair-group 집합·중복도뿐 아니라 **normalized candidate_id 와
실제 mapped 좌표 digest** 까지 비교한다.

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

**★ 23차 P0-4 — `≤1%`·`abs_tol`·`rel_tol` 이 아직 수치가 아니다.** 실행 가능한
계약이 되려면 값이 있어야 하고, 그 값은 **추측이 아니라 실측**에서 나와야 한다.

**tolerance 를 정하는 절차** (truth 미사용):

1. **objective 별 numerical floor 를 먼저 잰다** — 같은 입력을 반복하거나
   같은 max-bank prefix 를 재평가해서 `J` 의 재현 산포를 본다. 이것이 그
   objective 에서 "차이 없음" 의 바닥이다.
2. 그 floor 위에서 `abs_tol`·`rel_tol` 을 **사전 등록**한다. 33p 와 34p 는
   `J` scale 이 다르므로 **같은 값을 쓰지 않는다**.
3. `max(1, |J|)` 를 쓰면 `|J| < 1` 구간이 전부 공통 절대오차가 된다. 코드의
   `agree_tol` 비교식(`1e-3 * max(1, |min(J0,J1)|)`)이 이미 그렇고, v1 이
   그것을 상대 tolerance 라고 부른 것은 부정확했다.
4. 가능하면 **max-N 을 한 번 돌리고 prefix minima 를 offline 계산**한다.
   그러면 nested 비증가가 구조적으로 보장된다. 별도 N/2N 실행이라면 exact
   `J_2N ≤ J_N` 대신 `mono_tol` 을 둔다 (부동소수·비결정 경로 때문).

**작은 panel 에서 `≤1%` 는 의미가 없다.** n=60 이면 1% 는 0.6건이라 사실상
"0건" 규칙인데 계약이 분모·반올림을 안 정했다. 규칙을 나눈다:

| stratum 크기 | 규칙 |
|---|---|
| n < 100 | material 개선 **0건** |
| n ≥ 100 | 비율 ≤ 1% (반올림 없이 `count * 100 <= n`) |

1% 규칙을 쓰고 싶으면 panel 을 100 단위 이상으로 키운다 (§6.4).

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

**★ 23차 P0-5 — 조건 목록이 없으면 계약이 아니다.** panel 을 `sentinel_panel.yaml`
로 **파일에 고정**한다. 그리고 구현 smoke 와 budget pilot 을 분리한다.

**구현 smoke** (wiring 확인만 — 예산을 정하지 않는다):
reference 2 × noise {0, 0.005 한 seed} × objective 2 × condition {interior 1,
boundary 1}.

**budget sentinel pilot** — reference 마다 다음 archetype 을 사전 지정한다:

| # | archetype | 선택 시점 |
|---|---|---|
| 1 | pristine / interior easy | 결과 전 (geometry) |
| 2 | 22p 근방 scientific target | 결과 전 |
| 3 | α-window / feasibility edge 이지만 생성 가능 | 결과 전 (geometry) |
| 4 | parameter·bounds boundary face | 결과 전 (geometry) |
| 5 | recorded-only 투영에서 **결정론적 rule** 로 고른 hard 조건 | 결과 후 (empirical) |

noise 는 clean + **독립 noisy seed 2개**, objective 는 둘 다.
최소 구성은 `5 archetype × 2 reference × 3 noise × 2 objective = 60`
condition-objective 비교다 → n<100 이므로 위 표에 따라 **material 개선 0건**
을 요구한다. 1% 규칙을 쓰려면 panel 을 키운다.

**hard 의 정의를 둘로 나눈다** (이것이 P0-5 의 핵심이다):

- **geometry hard** — α wall, feasibility edge, 알려진 물리·bounds face.
  **결과를 보기 전에** 고를 수 있다.
- **empirical hard** — recorded-only 의 `J`·수렴 진단으로 고른 development set.
  선택 script 와 투영 SHA 를 봉인하고, **별도 holdout 또는 full-grid 확인**을
  반드시 붙인다.

새 결과의 truth error 가 큰 조건을 사후에 hard 로 고르면 **같은 자료로 예산을
튜닝**하는 것이다 (22차 발견 4 와 같은 오류).

계속 인용할 treatment claim 이 있으면 PE 5/10 mV · PE stretch 0.95 ·
NE +2 mV · both +2 mV 를 **treatment sentinel** 로 따로 넣거나, 해당 claim 을
`diagnostic` 으로 격하한다. exact 22p 는 계획한 seed 전부를 넣는다.

```yaml
# docs/22p_gap/sentinel_panel.yaml  (구현 시 생성)
schema_version: 1
selection_rule: <geometry rule / empirical script sha>
conditions: [<exact cond id 또는 물리좌표>]
reference_and_recipe_sha256: ...
treatment_and_curves_sha256: ...
exact_bounds_sha256: ...
objectives: [pocv_dvdq, pocv_dvdq_dqdv]
noise_levels_and_seeds: {0.0: [~], 0.005: [s1, s2]}
candidate_mode: equal_start_count_base_retained
provider_map_sha256: ...
budget_ladder: [5, 10, 20, 40]
max_budget: 40
tolerances_by_objective: {pocv_dvdq: {abs: ..., rel: ...}, pocv_dvdq_dqdv: {...}}
material_count_rule: {lt_100: zero, ge_100: pct_1}
holdout_rule: <empirical hard 를 썼다면 필수>
```

각 archetype 에서 필요한 `N` 을 구하고 **가장 큰 값을 채택**한다.

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

**★ 23차 P0-6 정정 — v2 는 여기 `warm` arm 표를 실었다.** primary 는 no-warm
인데 근거 표가 warm 이면 estimand 가 어긋난다. primary 와 **같은 arm** 인
`paired_fixed5_v4_nowarm_now` 의 33p ↔ 34p (recoverable 1,476조건):

| | 34p pass | 34p fail |
|---|---:|---:|
| **33p pass** | 131 | **436** |
| **33p fail** | **55** | 854 |

불일치 `491/1476 = 33.27%`, 34p 순증 실패 `436 − 55 = 381`.

**primary scalar 는 하나로 정의한다** — paired raw-degeneracy risk difference:

```text
Δ = (pass→fail − fail→pass) / n = (436 − 55) / 1476 = 0.2581
```

네 칸 전이표는 **같은 estimand 의 필수 분해**이지 두 번째 endpoint 가 아니다.
endpoint 를 둘로 늘리면 다중성 처리가 필요해진다.

참고로 warm arm 의 같은 표는 `381 / 186 / 167 / 742` (불일치 23.9%, 순증 19)
다. **둘 다 `recorded_only` 설계 prior 일 뿐 새 primary 결과가 아니다** — 이
수치로 threshold 나 endpoint 를 고르면 22차 Q4 가 금지한 자기선택이 된다.

두 arm 을 나란히 놓으면 aggregate 가 무엇을 숨기는지 보인다: no-warm 에서는
34p 가 33p 보다 **훨씬** 나쁘고(순증 381), warm 에서는 거의 비슷하다(순증 19).
aggregate 하나로 보고하면 이 protocol 의존성이 사라진다.

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

**★ 23차 P0-6 — 단일 `inference_status` 는 직교하는 축 셋을 섞었다.**
`recorded_only` 는 **보존** 상태, `diagnostic_only` 는 **과학적 용도**,
`historical_valid` 는 **검증 세대**다. 한 다리가 동시에 recorded-only 이면서
confounded 일 수 있는데 단일 필드로는 표현이 안 된다. 셋으로 나눈다:

```yaml
preservation_status: full_bundle | recorded_projection | missing
validation_status:   current_validated | historical_validated | unvalidated
inference_role:      canonical | diagnostic | confounded | superseded | excluded
```

| 축 | 답하는 질문 |
|---|---|
| `preservation_status` | 원자료가 **있는가** |
| `validation_status` | 그것이 **검증됐는가**, 어느 세대 검증기로 |
| `inference_role` | 그것을 **어디에 쓸 수 있는가** |

**raw bundle 이 없는 다리를 선택만으로 `historical_validated` 라고 부를 수
없다** — 검증은 실제 보존·검증 증거가 있을 때만 붙는다.

```yaml
# 허용 조합 (allowed cross-product) — 이 표 밖의 튜플은 거부한다. ★ v4 묶음 7
#   규칙:  canonical            은 full_bundle + current_validated 에서만
#          historical_validated 는 full_bundle 에서만 (원자료 없이 검증 못 한다)
#          recorded_projection · missing 은 언제나 unvalidated
allowed_status_combinations:
  - [full_bundle, current_validated, canonical]
  - [full_bundle, current_validated, diagnostic]
  - [full_bundle, current_validated, superseded]
  - [full_bundle, historical_validated, diagnostic]
  - [full_bundle, historical_validated, confounded]
  - [full_bundle, historical_validated, superseded]
  - [full_bundle, unvalidated, diagnostic]
  - [full_bundle, unvalidated, excluded]
  - [recorded_projection, unvalidated, diagnostic]
  - [recorded_projection, unvalidated, confounded]
  - [recorded_projection, unvalidated, superseded]
  - [recorded_projection, unvalidated, excluded]
  - [missing, unvalidated, excluded]
```

**★ 이 두 fenced 블록(enum + 허용 조합표)이 3축의 유일한 정본이다.** 원장도 회귀도 값을
옮겨 적지 않는다 — 회귀는 여기서 파싱한다
(`test_status_axis_enums_have_exactly_one_authority`). 24차 보충 리뷰가 반려한
것이 정확히 이 규칙의 위반이었다: 계약에 없는 `canonical_candidate` 를 원장과
회귀가 만들어 **두 번째 authority** 가 생겼다.

현재 warm-probe 8다리의 실측 상태는 이 문서가 아니라
`docs/22p_gap/LEG_PRESERVATION.yaml` 이 정본이다 (기계가 읽는다). 요약하면
`paired_fixed5_v4` 하나가 `full_bundle` · `historical_validated` ·
`diagnostic`, 나머지 7다리가 `recorded_projection` · `unvalidated` ·
`diagnostic`/`confounded` 다. 숫자·digest 는 여기 옮기지 않는다.

참고로 v2 의 단일 축은 다음과 같았다 (이제 쓰지 않는다):

| `inference_status` (v2) | 뜻 | 인용 |
|---|---|---|
| `canonical` | 새 protocol 정본 | ✅ |
| `historical_valid` | 옛 source commit 의 완전 bundle 로 재검증 가능 | 조건부 (regime 병기) |
| `recorded_only` | summary/manifest/투영만 남아 원자료 독립 재계산 불가 | ❌ 진단만 |
| `diagnostic_only` | 교란·교차-digest·adaptive → 인과 결론 부적합 | ❌ 진단만 |
| `superseded` | 새 protocol 정본으로 대체됨 | ❌ |
| `excluded` | 원점 오염 등으로 폐기 | ❌ |

정확히 하나여야 한다 — **v2 를 쓰던 때의 규칙이다.** v3 부터는 위 3축을
쓰므로 이 표는 옛 원장을 읽을 때의 대조용으로만 남긴다.

### 8.1 `leg_index.yaml`

```yaml
schema_version: 2
legs:
  - leg_id: hc22p_v6_armC_b20
    pairing_design_id: p22_halfcell_2x2_v6
    n_pair_groups: 320                    # ★ leg scalar pair_group_id 는 없다
    #  ↑ 23차 P0-2 정정: v2 는 640 이라고 썼다. 그 다리는 1,280행 · cond_id
    #    640 인데, noise 0/0.005 를 pair ID 에서 빼면 물리좌표 조합은 **320**
    #    이다. 계약 자신의 §4.2 규칙과 안 맞았다 (실측 재현: 재현 명령 참조).
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
예산상한 5 → **833초** (nproc 28, `adaptive=False`).

**★ 23차 P0-7 — 이 값에서 유도한 `0.027초/restart` 는 단일 restart 시간이
아니다.** 28병렬의 **effective wall-throughput** 이다. 비용 모델은 둘을 나눠
적는다:

| 축 | 뜻 | 이 실측에서 |
|---|---|---|
| wall time | 사람이 기다리는 시간 | 833초 |
| core-time | CPU 총 사용량 | ≈ 833 × 28 = 23,324 core-초 |
| wall-throughput | 병렬 포함 처리율 | 30,690 restart / 833초 = 36.8 restart/초 |

nproc 이 다른 기계로 옮기면 wall 은 바뀌고 core-time 은 대체로 유지된다.
재산정에는 **core-time** 을 쓰고, 일정 추정에만 wall 을 쓴다.

### 9.4 단계 3 부터는 원 fits 에 더 남긴다 (23차 발견 5)

현재 `src/fitting.py` 는 restart 마다 `p` · `J` · `i` · `source` · `warm` 만
저장한다. 그래서 투영의 random-only 다봉성은 **구현대로 정확히 재현되지만**,
"수렴한 국소최소의 다봉성" 까지 증명하지는 못한다 — 유한 `J` 를 가진 미수렴
restart 도 국소최소처럼 세어진다.

단계 3 에서 restart 행에 추가한다:

| 필드 | 왜 |
|---|---|
| `converged` | 미수렴 restart 를 국소최소로 세지 않기 위해 |
| `termination_status` | 왜 멈췄나 (maxiter / xatol / 예외) |
| `n_eval` | `equal_start_count` 가 계산비용을 같게 만들지 **않는다**는 것을 재는 축 (§3) |
| `candidate_id` | §4.2 — 어느 후보였나 |
| `bank_index` | bank 후반부 승리 여부 (§6.3 이 gate 에서 뺀 지표를 여기서 다시 볼 수 있게) |

함께 고칠 것 (2026-08-24 자체 발견): `validate_provenance` 가 **깨진 parquet**
에서 `ArrowInvalid` 를 그대로 올린다 (`src/io.py:1676`). 조용한 통과는 아니지만
함수 계약이 `{"ok":…, "fail":[…]}` 라 **깨진 파일을 발견으로 보고하지 못한다.**
읽기 실패를 검사 항목으로 잡아 `fail` 에 넣는다.

이 다섯이 들어가야 §6.2 의 solver 건전성 gate 와 §3 의 비용 비교가 실측
가능해진다.

## 10. 보존 (22차 Q6) — **단계 3 실행 전에** 세운다

> **★ 2026-08-24 — 이 절을 미룬 대가를 치렀다.** 작업 기계가 교체되면서
> `results/` 가 사라져 warm 실험 **7다리의 원자료를 잃었다**
> (`08_REVIEW_RESPONSE.md` §32, `LEG_PRESERVATION.yaml`). 23차 Q6 이 권고한
> content-addressed 보존을 "단계 3 이후" 로 미룬 것이 원인이다.
>
> 그래서 §11 의 순서를 바꾼다 — **보존 체계가 서기 전에는 새 실행을 시작하지
> 않는다.** 새로 도는 다리도 같은 방식으로 잃을 수 있다.
>
> 살아남은 `paired_fixed5_v4` 는 완전 bundle 이고 `validate_provenance`
> 34검사를 전부 통과했다 — 보존이 되면 무엇이 가능한지의 실례다.


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
다리는 §8 의 `recorded_projection` 으로 남기는 것이 정직하다 (v2 는 이것을
`recorded_only` 라고 불렀다).

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
12. **보존 체계 구축** — §10. ★ 2026-08-24 에 앞으로 당겼다
13. 그 다음에만 RUN_SCOPE 변경과 pilot 실행

2~7 은 이 문서가 **정의만** 했고 구현은 없다.

**★ 24차 보충 발견 7 정정 — `source_digest` 는 13 이 아니라 12 에서 바뀐다.**
보존 구현체가 `tools/archive_bundle.py` · `scripts/archive_results.sh` 이고
`tools/`·`scripts/` 는 **RUN_SCOPE 안**이다. content-addressed backend ·
receipt · atomic promotion 을 넣으면 그 순간 digest 가 움직인다. 리뷰가 준
두 갈래 중 우리가 고르는 것은 **2번**이다:

| 갈래 | 뜻 | 채택 |
|---|---|---|
| 1 | 기존 archiver 를 그대로 쓰고 외부 store/config 만 세운다 | ✗ — 묶음 9 의 트랜잭션 강제가 코드 변경 없이는 안 된다 |
| 2 | archiver 코드를 바꾸고 **12 에서 새 digest 를 동결**한다 | **✓** — 이후 pilot 은 그 digest 를 쓴다 |

따라서 순서는 `12 (보존, digest 동결) → 13 (RUN_SCOPE 나머지, 같은 digest 세대)`
다. 12 에서 동결한 digest 를 13 이 다시 바꾸므로, **동결 지점은 12 의 끝이
아니라 13 의 끝**이다 — 12 는 "보존이 먼저 존재한다" 를 보장할 뿐 digest 를
고정하지 않는다. pilot 실행은 13 이후의 digest 로만 한다.

**12 를 13 앞에 둔 이유**: 기계 교체로 warm 실험 7다리의 원자료를 잃었다
(§10 머리, `08_REVIEW_RESPONSE.md` §32). 보존 체계 없이 새로 돌리면 **같은
방식으로 또 잃는다** — 이번엔 ~12시간짜리를. 순서를 바꾸는 것이 비용이 거의
들지 않고, 안 바꾸면 되돌릴 수 없다.

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

## 13. v4 가 닫아야 할 묶음 열 개

> 1~6 은 **24차 리뷰**가 남긴 미결이고, 7~10 은 **24차 보충 리뷰**가 원자료
> 손실 사고를 계기로 P0 로 추가한 보존 묶음이다. 이 절은 목록이지 구현이
> 아니다 — 구현은 §11 의 12·13 단계다.

### 13.1 24차가 남긴 여섯 (미결 그대로)

| # | 묶음 | 상태 |
|---|---|---|
| 1 | `planned_protocol` 과 `execution_receipt` 분리, stage×objective×arm 별 예산/실현 count | 미착수 |
| 2 | canonical pairing-design wire schema · full arm registry · serialization/hash domain · golden vectors | 미착수 |
| 3 | provider materialize→seal→consumer DAG 와 `p_ini` arm 별 solution-map schema | 미착수 |
| 4 | `mono_tol` 과 `material_tol` 분리 · stratum · budget adoption · max-failure 규칙 | 미착수 |
| 5 | placeholder 가 아닌 **실제** `sentinel_panel.yaml` | 미착수 |
| 6 | 구 `pairing_design_id`·`inference_status` 제거 · actual digest 재해시 · per-key linkage mutation test | 미착수 |

### 13.2 묶음 7 — 상태 schema 단일 authority

**이번 라운드에서 닫았다.** 근거:

| 요구 | 어디 |
|---|---|
| `recorded_projection`/`missing` 의미 | §8 (enum + 아래 조합표) |
| validation generation 의미 | §8 — `historical_validated` 는 `full_bundle` 에서만 |
| claim 별 inference role | `LEG_PRESERVATION.yaml` 의 `claim_roles` |
| allowed cross-product | §8 `allowed_status_combinations` |
| duplicate rejection | `test_registry_rejects_impossible_status_tuples` |
| **authority 가 하나인가** | `test_status_axis_enums_have_exactly_one_authority` — 회귀 파일에 계약 밖 상태 literal 이 있으면 실패 |

### 13.3 묶음 8 — immutable bundle index 와 receipt schema

부분. `paired_fixed5_v4` 한 다리에 대해서만 실물로 결속했다.

| 요구 | 지금 | 남은 것 |
|---|---|---|
| bundle URI/backend · payload SHA · byte size · exact members | ✅ `evidence.bundle_uri` 등, 회귀가 디스크에서 재계산 | 외부 backend(비-git) URI 형식 |
| producer/schema/source identity | ✅ `leg_source_digest` · `projection_generation` | v6 producer schema |
| validator commit/source digest/version/time | 부분 — `validator_identity.source_digest` · `n_checks` | validator **commit** 과 실행 시각 |
| empty-root restore + validate + **score/analyze** output digests | ✗ — validate 만 있다 | ★ 보충 발견 4: score/analyze 산출 digest 를 영수증에 결속 |

### 13.4 묶음 9 — 트랜잭션 보존 gate

**미착수. 이것이 다음 라운드의 본체다.** 강제할 순서:

```text
run complete → seal → immutable external copy → index commit
→ empty-root restore → validator + score/analyze receipt
→ 그 뒤에만 projection/status/claim 등록
```

지금 못 하는 것을 명시한다: 보존 원장의 coverage 는 **커밋된 투영**을 기준으로
한다. 그래서 새 다리를 돌려도 투영을 만들기 전에는 회귀가 깨지지 않는다.
실행 **전에** 강제하려면 planned leg index 와 실행 영수증이 있어야 하고, 그것이
**묶음 9** 다. 그때까지 사전 등록은 `preservation_status: missing` 으로만
가능하다 (`test_preservation_registry_coverage_rule_matches_its_docstring`).

### 13.5 묶음 10 — historical projection version dispatch

**이번 라운드에서 닫았다.** 원자료를 잃은 투영은 다시 만들 수 없으므로,
현행 트리 equality 를 강요하면 영구 실패한다.

| 요구 | 어디 |
|---|---|
| raw-lost v3 투영은 **기록된** analyzer/spec 에 대해 검증 | `LEG_PRESERVATION.yaml` `projection_generation_pin` + `test_projection_generation_pin_matches_every_leg` |
| current tree equality 는 현행 세대에만 | `test_projection_analyzer_digests_recompute_from_the_current_tree` 가 `regeneration_capability` 로 분기 |
| cohort 밖 비교 금지 | `comparison_set_status` + `test_analyzer_change_breaks_the_comparison_set_loudly` |
| 새 schema 는 새 경로에 | v6 투영은 `docs/22p_gap/warm_probe/` 를 덮지 않고 별도 디렉터리에 쓴다 (구현 시) |
