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
| `inference_role` | 그것을 **현행 세대에서** 어디에 쓸 수 있는가 |

**★ 30차 P2 — leg-level `inference_role` 은 "현행 세대에 대한" 판정이다.**
초판은 이 칸을 "어디에 쓸 수 있는가" 라고만 적었고, 아래 제약이
`canonical` 에 `full_bundle + current_validated` 를 요구한다. 그런데
`paired_fixed5_v4` 는 leg-level 이 `diagnostic` 이면서 옛 세대 주장
`LEGACY_PAIRED_FIXED5` 의 `canonical` 이다 — 24차 보충 리뷰가 "legacy claim
scope 와 당시 protocol 을 명시한 채" 허용한 것이다. 두 진술이 모순처럼 읽혔고,
30차 리뷰가 "새 helper 의 재해석이 authority 문서에 반영되지 않았다" 고 지적했다.

두 층을 이름으로 가른다:

| 층 | 무엇 | 정본 |
|---|---|---|
| leg-level `inference_role` | **현행 세대**에 대한 다리의 역할. 아래 제약이 그대로 적용된다 | 이 문서 |
| per-claim `claim_roles[].inference_role` | 그 다리를 **특정 주장**에 쓸 때의 역할. 세대가 다르면 `role_compatibility` 표가 관장한다 | `CLAIM_STATUS.yaml` |

leg-level 보다 **센** per-claim role 은 그 주장의 세대가 **현행이 아닐 때만**
성립한다. 현행 세대 주장에는 leg-level 이 상한이다
(`tests/test_docs_lint.py::_claim_role_problems`). "현행" 은 선언이 아니라
산출물이 도달한 가장 새로운 세대로 도출한다 — `v6` 는 산출물이 없으므로
현행이 될 수 없다.

**raw bundle 이 없는 다리를 선택만으로 `historical_validated` 라고 부를 수
없다** — 검증은 실제 보존·검증 증거가 있을 때만 붙는다.

```yaml
# 허용 조합은 **열거하지 않고 제약에서 생성**한다. ★ v4 묶음 7 / 25차 발견 5
#
#   열거표였던 초판은 정상 상태를 빠뜨렸다 — 현행 코드로 보존·검증에 성공했지만
#   설계가 교란된 arm(`full_bundle / current_validated / confounded`)을 사실대로
#   적을 수 없었다. 세 축이 직교한다고 적어 놓고 표는 직교하지 않았던 것이다.
#
#   제약만 적고 조합은 회귀가 생성한다. 세 축의 곱에서 아래 함의를 어기는 것만
#   빼면 그것이 허용 집합이다.
allowed_status_constraints:
  - if:   {validation_status: [current_validated, historical_validated]}
    then: {preservation_status: [full_bundle]}
    왜:   원자료 없이 "검증됐다" 고 말할 수 없다
  - if:   {preservation_status: [recorded_projection, missing]}
    then: {validation_status: [unvalidated]}
    왜:   같은 함의의 대우 — 투영만 남은 다리는 검증 대상이 없다
  - if:   {inference_role: [canonical]}
    then: {preservation_status: [full_bundle], validation_status: [current_validated]}
    왜:   정본은 현행 검증기로 통과한 완전 묶음에서만 나온다
```

`diagnostic`·`confounded`·`superseded`·`excluded` 는 보존·검증 축과 **독립**이다
— 교란은 설계의 성질이지 보존의 성질이 아니다.

**계획 다리는 여기 오지 않는다.** 아직 실행하지 않은 다리를 `missing` 으로
적으면 "원자료를 잃었다" 와 "아직 안 돌렸다" 를 한 필드가 동시에 말하고,
`excluded` 를 붙이면 과학적으로 폐기된 것처럼 읽힌다. 계획 lifecycle 은 별도
**planned leg index** 에 적으며 그것이 **묶음 9** 다 (§13.4). 그때까지
`LEG_PRESERVATION.yaml` 은 **이미 실행된 다리만** 담는다.

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

> **★ 25차 리뷰 정정 — "닫음" 판정을 전부 철회한다.** v4 초판은 묶음 7·10 을
> "이번 라운드에서 닫았다" 고 적었다. 리뷰가 둘 다 반례를 냈다 (허용표가 정상
> 상태를 빠뜨림 · 세대 pin 이 여전히 전역). **이 절은 이제 "닫음" 을 쓰지
> 않는다** — 미착수 / 부분 둘뿐이고, 닫힘 판정은 리뷰가 한다.

### 13.1 묶음별 상태

| # | 묶음 | 상태 | 있는 것 / 없는 것 |
|---|---|---|---|
| 1 | `planned_protocol` ↔ `execution_receipt` 분리 | **부분** | `tools/preserve.py::PlannedLeg` 가 최소 envelope 과 `planned_id`(내용 주소)를 갖고, 트랜잭션이 `execution_receipt` 를 따로 낸다. **없는 것**: stage×objective×arm 별 예산/실현 count, 실제 leg index 결속 |
| 2 | canonical design wire schema · arm registry · hash domain · golden vectors | **부분** | arm registry ↔ 계약 §5 2×2 결속 · 이진 float 금지(**재귀**) · 십진 정규화 · **source 별 닫힌 candidate payload schema** · `src.grid.Condition` 결속(왕복 검증 실패 시 거부) · label 을 hash **밖**으로. **없는 것**: 실제 v6 격자 실행과의 end-to-end 결속, Unicode 정규화 실측 |
| 3 | provider materialize→seal→consumer DAG · `p_ini` arm 별 solution map | **미착수** | |
| 4 | `mono_tol` / `material_tol` 분리 · stratum · budget adoption · max-failure | **미착수** | |
| 5 | 실제 `sentinel_panel.yaml` | **미착수** | |
| 6 | 구 `pairing_design_id`·`inference_status` 제거 · per-key linkage mutation test | **미착수** | 묶음 9 의 final gate 는 이것 없이 닫을 수 없다 (25차 Q3) |
| 7 | 상태 schema 단일 authority | **부분** | §8 이 **제약**을 적고 회귀가 조합을 생성한다 (열거표가 아니다). `claim_roles` 는 `CLAIM_STATUS.yaml` 의 claim ID 와 role enum·protocol generation 에 묶였고, 중복·철회주장·원자료 없는 canonical 을 거부한다. **없는 것**: planned lifecycle (묶음 9) |
| 8 | immutable bundle index · receipt schema | **부분** | member 전수 재해시 → 빈 root 복원 → **`repo_root` 로 검증기를 그 root 에 결속**(26차 P1-5 정정) → 복원본만으로 재채점 → file·semantic 두 digest → **봉인본과 semantic equality 강제**(26차 P1-6 정정). core/stamp 분리로 core 가 바이트 동일 재생성. **없는 것**: 비-git backend URI 형식, legacy 다리의 외부 store 사본 |
| 9 | 트랜잭션 보존 gate | **부분** | §13.2 · §13.4 — 26차 P0 둘(CAS 복원·영수증 저장)을 고쳤고 46차에 planned leg index 를 실행 전 gate 로 배선했다. **실물 provider 어댑터**가 남았다 |
| 10 | historical projection version dispatch | **부분** | §13.3 — 26차 P1-9·P1-10 으로 전역 회귀 둘을 cohort 화하고 frozen 목적지 쓰기를 코드가 거부하게 했다 |

### 13.2 묶음 9 — two-phase 보존 트랜잭션

구현: `tools/preserve.py` · 회귀: `tests/test_preserve.py` (hermetic).

> **★ 26차 리뷰가 초판을 P0 둘로 반려했다. 둘 다 false-green 이었다.**
>
> **P0-1** 복원이 CAS 가 아니라 **원본 `run_dir` 를 복사**했다. member 와
> manifest 를 backend 에 넣고 되읽기까지 했지만 되읽은 bytes 는 해시만 확인하고
> 버렸다. 리뷰가 read-back 직후 CAS 를 통째로 비우자 그대로 publish 까지
> 성공했다. "빈 root 로 복원해 검증했다" 는 주장이 거짓이었다.
>
> **P0-2** receipt 를 메모리에서 만들고 **digest 만** index 에 적었다. 그
> digest 로 아무 것도 회수할 수 없었고, "등록" 은 상태 변경이 아니라 단순
> `return` 이었다. crash 뒤 "재시도" 는 계산 전체를 다시 도는 것이었다 —
> 실제 사고에서 원본 계산은 12시간짜리다.

고친 순서:

```text
planned_leg seal            내용 주소. run_spec 이 **없으면 시작하지 않는다**
→ private temp 로 실행 (호출자)
→ payload seal              exact member manifest + root digest
→ CAS staging put-if-absent staging → os.replace 로만 objects/ 승격
→ read-back                 backend 에서 되읽어 다시 해시
→ **CAS 에서만** 빈 root 복원  `restore_from_cas(backend, manifest_digest, root)`
                            — 함수가 원본 경로를 **받지 않는다**
→ validate + rescore        복원본만으로. expected_semantic 이 없으면 거부
→ receipt 를 CAS 에 저장     + read-back 대조
→ per-leg **배타 생성** publish  O_EXCL. read-modify-write 가 아니다
→ durable registration      journal 파일. `return` 이 아니다
```

**두 단계 불변식** — 초판의 "어느 단계에서 멈추든 index 가 깨끗하다" 는
틀렸다. publish 뒤 crash 는 durable 한 중간 상태를 남긴다. 숨기지 않고 적는다:

| 언제 실패 | 남는 상태 | 닫는 법 |
|---|---|---|
| publish **전** | public index 에 항목 없음 | 처음부터 다시 |
| publish **후** | 항목은 durable, **등록 안 됨** | `finalize_only()` — **재계산 없이** CAS 만으로 |

주입 가능한 실패 21종이 `FAULTS` 에 있고,
`test_every_declared_fault_has_a_regression` 이 목록만 늘고 검사가 안 늘어나는
것을 막는다.

| 실패 | 멈추는 단계 |
|---|---|
| member 1비트 변경 · 누락 · 추가 · stale index | `payload_seal` |
| 끊긴 업로드 | `cas_put` |
| 되읽기 손상 · 읽기 권한 없음 | `read_back` |
| **CAS 에서 member·manifest 삭제 · 전체 삭제 · 바이트 변조** | `cas_restore` |
| 복원 누락 | `empty_root_restore` |
| 검증기 예외 · 검증 실패 | `validate` |
| 재채점 예외 · semantic 불일치 · 산출 schema 위반 | `rescore` |
| `run_spec` 없음 · 다른 계획 · 다른 code identity | `planned_seal` |
| `expected_semantic` 없음 | `hooks` |
| 보존 기간 부족 | `capability` |
| publish 직전 crash | `publish` |
| publish 직후 crash | `register` → `finalize_only` 로만 닫힌다 |

**증명 장치**: `run_transaction(..., drop_source_after_seal=True)` 는 업로드
직후 원본을 지운다. 그러고도 끝까지 간다면 복원이 backend 에서 나온 것이
확실하다. 회귀가 그 경로를 돈다.

**아직 아닌 것** (그래서 "닫음" 이 아니다):

1. `run.sh` · smoke 의 **필수 gate 로 배선되지 않았다.**
2. 실제 운영 backend canary 가 없다 (25차 Q1 대로 local `file+cas://` 로
   트랜잭션 **의미**만 검증했다).
3. `planned_leg_index` 가 실제 leg 원장과 결속되지 않았다 — 묶음 1·6 필요.

### 13.3 묶음 10 — cohort 기반 세대 dispatch

전역 pin 하나를 cohort 로 나눴다 (`LEG_PRESERVATION.yaml` 의 `cohorts`).

| 규칙 | 회귀 |
|---|---|
| 모든 투영이 **자기 cohort 의 pin** 과 같다 | `test_every_projection_matches_its_own_cohort_pin` |
| 활성 cohort 는 **정확히 하나**, 현행 트리를 따른다 | `test_exactly_one_cohort_is_active_and_it_tracks_the_current_tree` |
| 원자료를 잃은 다리는 활성 cohort 에 들어갈 수 없다 | `test_raw_lost_legs_live_only_in_frozen_cohorts` |
| 교차-다리 비교는 cohort 안에서만 | `test_projections_share_one_compute_provenance_within_each_cohort` |
| 새 세대는 **새 경로**에 쓴다 (옛 바이트를 덮지 않는다) | `row_projection.py --out` + `test_cohort_membership_is_consistent_in_both_directions` |

실측으로 확인한 것: analyzer 를 g1→g2 로 올리고 `paired_fixed5_v4` 를 새
cohort 에 재생성했더니 `projection_sha256`·`restart_projection_sha256`·
`fits_sha256` 이 **g1 과 바이트 동일**했다. 계산 의미는 안 바뀌었고 identity
회계만 엄격해졌다는 뜻이다 (25차 발견 2 의 수정이 정확히 그 목적이었다).

**★ 26차 P1-9·P1-10 으로 더 고친 것:**

| 무엇이 남아 있었나 | 고침 |
|---|---|
| 투영 자기정합 회귀가 frozen g1 과 **현행 spec** 을 박아 뒀다 | cohort 를 순회하고 **그 cohort 의 pin** 과 대조한다 |
| 보존 원장 coverage 가 g1 디렉터리 하나와 정확히 같기를 요구했다 | cohort 전체의 투영 집합과 대조한다 |
| 활성 cohort 의 gzip payload 를 **아무도 열지 않았다** | 같은 순회가 g2 의 payload 도 압축 해제·재해시한다 (삭제 변이로 확인) |
| `--out` 을 생략하면 frozen g1 을 **직접 덮었다** | `--cohort` 로 고르고, frozen 목적지는 코드가 거부한다 |
| 검증 **전에** gzip 부터 목적지에 썼다 | staging 에 쓰고 전 검증 통과 뒤 원자적으로 승격한다 |
| `evidence.cohorts` 가 nonempty 인지만 봤다 | cohort registry 와 **양방향** 대조 |

**아직 아닌 것**: v6 투영을 새 schema 로 만들 때 새 디렉터리·새 cohort 로
가야 한다는 규칙은 적었지만, v6 투영 자체가 없어 실측되지 않았다.

### 13.3.1 cohort 게시의 신뢰 경계 (44차 — **보장 철회**)

39~43차 게이트 리뷰에서 cohort 게시 경로는 "적대적 same-process/namespace
writer" 를 위협 모델에 두고 검사를 계속 늘렸다. 44차에 그 중 하나가 **검사
횟수로 닫히지 않는다**는 것이 확정됐다:

> `_commit_guard()` 가 원장 seal 과 두 pointer 를 재확인하고 통과한 뒤,
> `os.replace` 가 실행되기 전에 다른 writer 가 valid `CURRENT` 를 게시하면
> 그것을 덮는다.

이 창을 없애려면 둘 중 하나가 필요하다.

1. 별도 OS principal/service 가 `CURRENT`·`.PENDING`·`gen/`·`.publish.lock`
   과 보존 원장 namespace 의 create/rename/link/write 를 **독점**한다.
2. provider 가 원자적 conditional write(compare-and-swap)를 제공한다.

둘 다 이 저장소의 현재 배포 형태 밖이다. 그러므로 **보장을 철회하고 전제를
계약에 적는다.**

> **전제**: cohort 출력 디렉터리와 보존 원장은 **하나의 OS principal 이
> 소유**하고, 그 안에 쓰는 모든 writer 는 `promote_cohort_generation()` 을
> 지나 같은 게시 lock 을 따른다. 비협조적 writer — 같은 principal 로 lock
> 없이 pointer 를 바꾸는 코드, pathname 을 교체하는 코드 — 는 지원 범위
> **밖**이다.

정본은 `docs/22p_gap/row_projection.py` 의 `_TRUST_BOUNDARY` 문자열이고,
이 절은 그것을 가리킨다 (`test_the_publisher_declares_its_trust_boundary`
가 둘이 함께 있는지 본다).

남는 것은 다음 셋이다. **44차 리뷰 지적을 받아 과장을 걷어낸다** — 45차 정정:

| 축 | 상태 |
|---|---|
| lock 취득~`os.replace` 직전의 pointer/원장 변경 | 검사한다 (`_commit_guard` + `os.replace` 직전 pointer 재확인) |
| `os.replace` 직전~직후의 마지막 창 | **전제로 배제** — 검사로 못 닫고 **탐지되지도 않는다** |
| 그 창에서 덮인 pointer | **복구되지 않는다** (아래) |

44차판은 "전제가 깨져도 탐지는 된다" 고 적었는데 **틀렸다.** 마지막 창에서
덮인 pointer 는 아무도 못 본다 — 그것이 그 창의 정의다.

generation directory 가 immutable 이라는 것은 **바이트가 남는다**는 뜻이지
"어느 pointer 가 정본이었는지 회수된다" 는 뜻이 아니다. 여러 valid generation
중 무엇이 active authority 였는지는 durable commit journal 이나 기대 pointer
digest 없이는 정할 수 없고, 그런 것은 **없다**. 둘을 구분해 적는다:

- **바이트 보존**: 된다 (generation 은 immutable 하게 굳어 있다)
- **정본 pointer 복구**: 안 된다 (사람이 원장·수령증으로 재판단해야 한다)

### 13.3.1.1 배포 점검이 증명하는 것과 못 하는 것

디렉터리 소유자·퍼미션 점검은 **cooperative-local 설정 점검**이다. gross
misconfiguration(group/other write, 남의 소유, symlink 경유)은 잡지만
**cooperative behavior 를 증명하지 못한다** — 같은 principal 의 코드는
퍼미션을 그대로 지나가고, uid 0 에서는 mode bit 가 잠금이 아니다.

강한 enforcement 를 주장하려면 publisher 전용 service principal 과, worker
principal 의 create/rename/link/write 가 **실제로 거부되는** negative canary 가
필요하다. 그것은 미착수다.

### 13.3.2 cohort 게시 authority 는 무엇인가 (46차)

`CURRENT` 와 `.PENDING` 은 게시 당시의 **원장 authority** 를 봉인한다:

```
_LEDGER_AUTHORITY = ("cohort_id", "dir", "status", "legs",
                     "pin", "cross_leg_comparison")
_PIN_SEALED       = ("schema_version", "analysis_spec_sha256",
                     "producer_semantic_sha256")
```

reader(`read_current()`)도 그 봉인값을 지금의 원장과 대조한다. 따라서 이 중
하나라도 바뀌면 그 cohort 의 기존 pointer 는 **더 이상 authority 가 아니다**
(게시도 읽기도 거부된다). 바꾸려면 **새 cohort ID 와 새 출력 디렉터리**로 간다.

**45차의 좁히기가 지나쳤다.** 45차는 `pin` 을 통째로 authority 밖에 뒀는데,
`pin` 에는 두 종류가 섞여 있다:

| 필드 | 성격 | 봉인 | 어디서 강제되나 |
|---|---|---|---|
| `schema_version` | 산출 schema | **○** | 봉인 대조 (`_parse_pointer`) |
| `analysis_spec_sha256` | 비교 규칙 | **○** | 봉인 대조 |
| `producer_semantic_sha256` | **누가 만들었는가** (47차 추가) | **○** | 봉인 대조 |
| `compute_sha256` | 계산 dependency closure digest | × | `..._digests_recompute_from_the_current_tree` |
| `row_projection_py_sha256` | producer 파일 digest | × | 같은 회귀 |
| `src_scoring_py_sha256` | 채점기 파일 digest | × | 같은 회귀 |
| `runtime`·산문 | 관측 기록 | × | — |

**46차의 두 필드 선택은 틀렸다 (47차 정정).** 46차는 producer 축 전체를
봉인 밖에 두고 "active cohort 의 manifest 는 현행 트리와 같아야 한다"는
**나중에 채점하는** 회귀에 맡겼다. 그 회귀는 publisher 불변식도 reader
불변식도 아니므로 그 사이로 빠지는 상태가 있었고, 47차 리뷰가 실제 schedule 을
보였다:

> roster {a,b} · pin A 로 a 만 게시(`.PENDING`) → schema/spec 는 그대로 두고
> producer 만 B 로 → 원장 pin 을 B 로 → b 를 게시
> ⇒ **a(A)+b(B) 를 담은 active CURRENT** 가 만들어지고 reader 가 승인한다.

그래서 producer identity 를 봉인에 넣되, **주석에 흔들리지 않는 형태**로
정의한다. `producer_semantic_sha256` 은

- **바이트를 만드는 코드의 닫힘**만 담는다. 게시·원장 authority 는
  `_PRODUCER_CUT` 에서 잘라 낸다 — 그 코드는 바이트를 만들지 않는다.
  (46차 `compute_sha256` 은 `build()` 가 뿌리라 publisher 전체를 빨아들였고,
  그래서 게시 코드를 고칠 때마다 움직였다. 그것이 "봉인하면 라운드마다 새
  cohort" 의 진짜 원인이었다.)
- 각 정의를 **AST 정규형**으로 접는다 (주석·docstring·서식이 사라진다).
- 절단면 이름이 사라지면 fail-closed 로 거부한다 — 닫힘이 조용히 넓어지거나
  좁아질 수 없다.

실측: 47차에 publisher·원장 authority·계획 lifecycle 을 크게 고쳤는데
`producer_semantic_sha256` 은 `908503e65162e7d9` 그대로였고 (그래서 이미 게시된
pointer 가 유효했다) `compute_sha256` 은 세 번 움직였다.

나머지 셋은 여전히 기록이며, `..._digests_recompute_from_the_current_tree` 가
그 축을 본다.

`cross_leg_comparison` 은 소비자가 **지켜야 하는 사용 정책**이므로 같은 이유로
authority 다.

**원장 위생** (production parser 가 fail-closed 로 강제한다):

- `status` 는 정확한 enum `("active", "frozen")` — 자유 문자열이면 frozen 도
  active 도 아닌 cohort 가 조용히 생긴다.
- `cross_leg_comparison` 도 정확한 enum이다.
- `dir` 은 **정규 · 저장소-상대 · 격리** 경로여야 한다. `pathlib` 의 `/` 는
  오른쪽이 절대 경로면 왼쪽을 버리므로, 45차까지 `dir: /etc` 인 항목은 `/etc`
  를 cohort 디렉터리로 만들었다 (중복 검사도 조회도 저장소 밖에서 돌았다).
- `pin` 은 닫힌 5필드 schema 다.

**pointer 는 봉인 하나만 싣는다.** 45차는 `cohort_id` 를 echo 로 함께 실었지만
비교하지 않았다 (봉인이 이미 덮으므로 중복이라고 판단했고, 실제로 그 대조
변이가 안 물었다). 그러면 그 필드는 seal 과 어긋날 수 있는 **진단 문자열**로
남아 오류 메시지가 거짓말을 한다. 대조를 더하는 대신 필드를 없앴다. 진단용
ID 는 살아 있는 원장에서 그때 읽는다. 이미 커밋된 pointer 는
`docs/22p_gap/migrate_pointer.py` 가 **같은 generation 을 가리킨 채** 한 번
옮긴다 (`schema` 문자열은 `generation_id()` 의 preimage 라서 올리지 않는다).

**pointer 소실은 terminal 이다.** `CURRENT` 도 `.PENDING` 도 없는데 `gen/` 에
generation 이 있으면 그것은 bootstrap 이 아니라 pointer 소실이다. 45차는 그
상태에서 한 leg 만 담은 새 계보를 조용히 시작했고, 그 순간 명부 불변식이
깨졌다 — 무엇이 있었는지 알 방법이 없다 (durable commit history 를 두지 않기로
했으므로 복구할 근거가 없다). 그래서 **fail-closed 로 끝낸다**: 사람이 새
cohort ID 로 가야 한다.

### 13.3.3 caller staging 은 읽기 전용 입력이다 (46차)

`promote_cohort_generation(stage, out, leg, roster=...)` 의 `stage` 는
publisher 가 **읽기만** 하는 입력이다. 성공하든 실패하든 그 디렉터리에
write·copy·unlink·rmtree 를 하지 않는다. 치우는 것은 만든 쪽의 일이다.

45차까지는 아니었다. `stage` 를 merge workspace 로 써서 base generation 의
파일을 `shutil.copyfile` 로 복사해 넣었고, 성공 경로에서 `rmtree` 했다.
결과로 public API 만으로 다음이 성립했다:

> `stage` 에 `b.projection.yaml -> ../victim` 인 **dangling symlink** 를 두면
> `Path.is_file()` 이 그것을 걸러 exact-set 검사를 통과시키고, 이어지는 base
> 복사가 목적지 symlink 를 **따라가** cohort 디렉터리 **밖**에 파일을 만든다.

이제 순서가 이렇다:

1. `stage` 를 `_staging_entries()` 로 **처음부터** no-follow exact read
   (regular · `st_nlink == 1` · 정확한 entry 집합)
2. base generation 도 **같은 validator**(`_generation_entries()`)로 읽는다
3. 병합은 **메모리에서** 한다
4. publisher 소유 private temp(`out/.merge.<uuid>.tmp`)에만 `_write_owned` 로
   자재화하고, 실패하면 그 temp 만 지운다

생성·멱등 재게시·독자 셋이 **같은** generation validator 를 지난다. 45차에는
자재화 경로에만 no-follow·`nlink` 검사가 있어서, generation 안의 파일에 바깥
hardlink 를 걸면 "immutable generation" 의 바이트를 바깥 이름으로 바꿀 수
있는데도 독자와 멱등 분기가 통과했다.

alias 판정은 **`(st_dev, st_ino)`** 로 한다. `Path.resolve()` 는 symlink 만
펴므로 bind mount(다른 pathname·같은 inode)를 못 본다.

**디렉터리 root 자신도 따라가지 않는다 (47차).** 46차는 child entry 만
`lstat`/`O_NOFOLLOW` 로 열고 root 는 `exists()`·`is_dir()`·`os.listdir(path)`
로 봤다. 그래서 `gen/<gid>` 를 바깥 디렉터리 symlink 로 바꾸면 immutable
generation 의 바이트가 namespace **밖**에 있게 되고, 나중에 그 target 을 고치면
immutable 이 아니다. child hardlink 는 막으면서 root alias 는 허용하는 경계는
성립하지 않는다 — 46차가 조건 3 의 증거로 든 것이 바로 child hardlink 였다.

이제 root 는 `O_DIRECTORY | O_NOFOLLOW` 로 열고 (실물 디렉터리이고 alias 가
아니라는 판정을 **커널이** 한다 — 검사와 사용 사이에 창이 없다) child 는 그
**붙잡은 dirfd** 에 대한 `openat`/`fstatat` 으로만 읽는다. root 를 검사한 뒤
pathname 으로 child 를 다시 열면 그 사이의 root 교체를 못 본다.

### 13.4 planned leg index — 실행 **전** gate (46차에 배선)

45차까지 보존 원장의 coverage 기준은 **커밋된 투영**이었다. 그래서 새 다리를
돌려도 투영을 만들기 전에는 아무 회귀도 깨지지 않았고, 2026-08-20 에 warm
7다리를 그렇게 돌렸다가 보존 없이 잃었다. 이것이 "묶음 9 의 남은 절반" 이라고
스스로 신고하던 자리다.

`LEG_PRESERVATION.yaml` 에 `planned:` 가 생겼다. 항목은 닫힌 schema 다:

```
PLANNED_KEYS   = ("leg_id", "cohort_id", "status",
                  "authorized_source_digest", "recorded_on", "근거")
PLANNED_STATUS = ("planned", "executed")
```

강제하는 것은 `tools/preserve.py` 의 두 함수다.

| 함수 | 무엇을 막나 |
|---|---|
| `assert_planned_leg(leg, source_digest)` | 계획에 없는 다리 · `executed` 를 승인으로 재사용 · frozen cohort 로 새 다리 · **승인 뒤 RUN_SCOPE 가 바뀐 경우** |
| `assert_planned_index_consistent()` | `legs:` 에만 있고 계획에 없는 다리 · 계획 digest ≠ `evidence.leg_source_digest` · 계획 cohort ∉ 실행 기록의 cohort |

두 방향이 다 필요하다. 앞의 것만 있으면 gate 를 안 부르고 돌린 다리가 나중에
`legs:` 에만 나타나도 아무 검사가 안 깨진다. 뒤의 것만 있으면 계획 index 가
자기 자신만 참조하는 목록이 된다 (아무 digest 나 적어도 일관되다).

**46차의 gate 는 lifecycle 이 아니었다 (47차 정정).** 47차 리뷰가 보인 것:
정상적인 prospective leg 가 gate·원장 lint·publisher 를 **동시에 통과할 상태가
없었다.**

| L 의 배치 | 실행 전 gate | publisher / lint |
|---|---|---|
| roster 밖 · `planned` | 통과 | publisher 가 undeclared 로 거부 |
| roster 에만 추가 · `planned` | 통과 | roster ↔ 실행 legs exact 불변식 실패 |
| 실행 legs 에도 추가 · `planned` | 통과 | planned-index consistency 실패 |
| `executed` 로 변경 | 거부 | 실행 전에 이미 실행됨으로 기록 |

그래서 47차는 **계획 roster 와 실행 roster 를 분리**하고(`prospective_legs` ↔
`legs`) read-only predicate 를 **상태 전이**로 바꿨다.

```
prospective 승인(사람이 원장에 적는다)
→ claim_planned_leg()      원자적 claim (O_EXCL) · run_spec digest 대조
→ phase_done("grid", …)    durable phase receipt
→ phase_done("fit", …)
→ finalize_leg()           executed 전이 + roster 이동 + 실행 기록
```

중단되면 `resume_claim()` 이 **같은 attempt 로** 이어받아 남은 phase 만 하고
닫는다 (재계산 없음). `claim` 은 실행 계획의 **내용 주소**(`run_spec_digest`)를
봉인하므로, 같은 이름으로 다른 실행을 승인할 수 없다 — 46차 planned row 는
`--objective A --n-restarts 1` 과 `--objective B --n-restarts 999` 를 똑같이
승인하는 allowlist 였다.

**승인의 종류를 기계가 구분한다.** `authorization_kind: prospective |
retrospective`. 소급 항목은 `run_spec_digest: "retrospective:no-preauthorization"`
이고 claim 대상이 아니다. `planned_coverage()` 가 종류별로 세므로 "실행 전
gate 가 실제로 몇 번 작동했는가" 를 자유문자 근거를 읽지 않고 답할 수 있다.
**현재 값은 prospective 0 · retrospective 8 · gate_backed_executions 0 이다.**

**배선** (건너뛰는 환경변수·flag 는 두지 않는다 — 그런 문이 있으면 gate 가
아니다):

- `run.sh` 의 `grid`·`fit` 은 `plan_gate` 를 지난다. `all` 은 `--leg` 를 하위
  단계로 전파한다. **`--dry-run` 면제는 47차에 없앴다** — `run_grid(dry_run=True)`
  는 출력 디렉터리를 만들고 완방상태·baseline 을 계산한 뒤 최대 세 조건에
  solver 를 실제로 부른다. 계산이 있으면 gate 도 있다.
- **모듈 자신이 gate 를 지난다.** 46차 gate 는 `run.sh` 안에만 있었고 `--leg`
  는 shell 이 소비했으므로 `python -m src.grid` 직접 호출은 계획을 전혀 보지
  않았다. gate 가 wrapper 에 있으면 wrapper 를 안 쓰면 그만이다.
  `src/grid.py` 는 **첫 부작용(`mkdir`) 보다 먼저** 공유 gate 를 부른다.
- `scripts/smoke_e2e.sh` 는 (a) 계획 index 가 일관하고 (b) 계획 밖 다리를
  gate 가 **실제로 거부**하며 (`--out` 이 smoke namespace 밖인 실제 호출로
  확인한다 — grep 만 보면 함수가 빈 껍데기여도 초록이다) (c) `run.sh` 에
  배선이 남아 있는지 본다.

**면제는 산출 namespace 하나뿐이고, 판정은 정규 격리다 (47차).**
`results/_smoke/` **안으로만** 읽고 쓰는 실행은 gate 를 지나지 않는다 (smoke
자신이 pipeline 을 돌려야 하기 때문이다). 경로가 하나라도 그 밖이면 gate 를
지난다.

46차 판정은 shell `case` **문자열 prefix** 였고 그래서 다음이 면제를 받았다:

```
--out results/_smoke/../grid_fit_v4    # 문자열은 안, 실물은 results/grid_fit_v4
--out results/_smoke/link/x            # link 가 밖을 가리킨다
```

`is_inside_namespace()` 하나가 판정한다: `..` 성분 금지 · namespace 부터 마지막
존재 성분까지 어느 것도 symlink 가 아님 · 실물 경로가 namespace 아래. `run.sh`
와 모듈 gate 가 **같은 함수**를 쓴다.

> **여전히 남는 한계**: 같은 principal 이 비싼 실행을 `results/_smoke/` 로 밀어
> 넣으면 gate 를 피할 수 있다. 47차 리뷰가 지적한 대로 "그 산출은 정본이 될 수
> 없다" 는 **아직 코드로 강제되지 않는다** — `archive_results.sh` 와 report 는
> source namespace 를 거부하지 않는다. typed smoke provenance 를 모든 sink 가
> 거부하게 하는 것은 **다음 라운드로 신고한다** (§13.5).

**아직 남은 것**: 실물 provider 어댑터. 지금 보존 회귀는 hermetic fake
provider 로만 돈다. 그래서 smoke 통과는 "pipeline 이 온전하고 계획 gate 가
배선돼 있다" 는 뜻이며 실물 WORM 보관에 대한 승인이 아니다 (§13.5).

현재 `planned:` 의 8건은 46차에 index 를 도입하면서 **소급 기록**한 것이다 —
그때는 실행 전 gate 가 없었다. 소급이라는 사실을 지우지 않는다. digest 는
새로 만든 값이 아니라 원장의 `evidence.leg_source_digest` 를 그대로 옮겼고,
`assert_planned_index_consistent()` 가 그 일치를 강제한다.
