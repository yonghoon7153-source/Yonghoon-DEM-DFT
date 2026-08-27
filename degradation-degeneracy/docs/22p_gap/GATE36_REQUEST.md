# 36차 게이트 리뷰 요청 — 35차 P0-1 · #9

> 자기 완결 문서다. 숫자는 옮겨 적지 않는다 — 영수증·투영·원장이 정본이다.

```yaml
브랜치:     origin/claude/14-gate-code-review-9qkx05
대상 커밋:   6c11cf6c0c8c6323bf587ccc2e8026e46030037b
직전 대상:   3698be72…      (35차, P2 종결 / P0-1·#9 NO-GO)

source_digest:
  35차:  b79b0019d69a6fcf
  현재:  4f4756746bd63496

재현:      git checkout 6c11cf6c0c8c6323bf587ccc2e8026e46030037b
           cd degradation-degeneracy
```

## 0. 요청 판정

| 대상 | 요청 |
|---|---|
| P0-1 (retain 내부 crash · store.json · adapter 계약/의미) | 닫혔는가 |
| #9 (실제 reader 고정경로 · public publish 경계) | 닫혔는가 |
| P0-3 · P2 | 33·35차 종결 — 재검 요청하지 않는다 |
| 실제 provider adapter · power-loss fault model · delete-marker | **미구현으로 신고한다** |
| 묶음 9 완료 · gate 배선 · 묶음 2 동결 | **요청하지 않는다** |
| 새 Stage 3 leg · 대규모 재실행 | **요청하지 않는다** |

## 1. 검증 — 방금 실행한 출력

```
$ git rev-parse HEAD
6c11cf6c0c8c6323bf587ccc2e8026e46030037b
$ git status --short
(빈 출력)

$ python3 -m pytest tests/ -q
1011 passed, 1 xfailed in 339.36s (0:05:39)

$ ./scripts/smoke_e2e.sh
✅ pipeline smoke 통과
⚠ 보존 gate 미완료 (계약 v4 묶음 9) — 새 leg 실행 금지.

$ python3 docs/22p_gap/make_receipt.py paired_fixed5_v4 --check
✅ paired_fixed5_v4: core 재생성 바이트 동일 · core_sha ddb3ac0b38b6c2e5

$ python3 wiki/tools/lint.py
RESULT: 0 errors
```

## 2. 35차 진단 — 한 덩어리라고 부른 것이 여러 단계였다

| 자리 | 한 덩어리라고 불렀다 | 실제 단계 |
|---|---|---|
| `retain()` | lease 하나 | put → pin → lock_objects → lock_content (4) |
| `store.json` | 생성하면 잠긴다 | put → lock (2) · 기한이 lease 와 무관 |
| `_materialize()` | 승격의 일부 | 파일 수만큼 `os.replace` (n) |
| provider 계약 | 산문 7연산 | 코드가 부르는 것 9개 |

33차 "고친 것 ≠ 쓰이는 것" · 34차 "최초 경로 이후 상태 없음" 에 이은 세 번째
변형이다.

## 3. 발견별 대응

### 3.1 P0-1a — `retain()` 네 단계 crash

| 항 | 값 |
|---|---|
| 회귀 | `test_a_crash_inside_retain_leaves_exactly_one_repairable_lease[after_lease_put\|after_lease_pin\|after_pin_lock]` |
| 코드 | `tools/preserve.py` `repair_lease_locks()` · `_existing_lease()` |
| 겨냥 방식 | **호출 서수** — lease digest 는 store 마다 다르다 (`store_id`·`backend_uri` 가 lease 안) |
| 불변식 | 재개가 lease 를 **하나만** 남긴다 · 두 잠금(pin·content) 모두 생존 |

### 3.2 P0-1b — `store.json` pre-lock 잔여 + 기한 결속

| 항 | 값 |
|---|---|
| 회귀 | `test_an_unlocked_store_record_is_repaired_or_refused` · `test_the_store_lock_horizon_covers_every_lease` |
| 코드 | `ensure_store_lock()` · `_store_horizon()` · `retain()` 이 `ensure_store_lock(until_s)` |
| 변이 3종 | `ensure_store_lock` no-op · 생성시 미잠금 · retain 쪽 연장 제거 — **전부 물었다** |

> 첫 판은 변이가 안 물었다: 시험 lease(365일)가 store 기본 지평(3650일)에 이미
> 덮였다. lease 를 지평보다 **길게**(`MIN_RETENTION_DAYS*20`) 만들고 backend
> `retention_days` 를 함께 열어야 축이 실행된다. §44.2 에 기록.

### 3.3 P0-1c — 계약 authority · per-version · GOVERNANCE

| 축 | 대응 | 검사 |
|---|---|---|
| 계약이 두 곳 | `PROVIDER_CONTRACT` 상수가 정본 (9연산) | `test_the_provider_contract_is_the_only_authority` — **AST 로 `self.provider.*` 호출 집합과 정확히 일치** |
| 계약 미충족 provider | `probe_enforcement()` → advisory | `test_a_provider_missing_a_contract_op_cannot_claim_durable` (연산마다 parametrize, **실제 판정 경로**로 확인) |
| per-version 의미 | `protected_version()` · 모든 durable 읽기가 경유 | `test_the_provider_actually_refuses_to_delete_a_locked_object` 등 3 canary **불변식 교체** |
| GOVERNANCE 우회 | `probe_bypass()` 가 잠긴 canary 에 **우회 삭제를 시도** | `test_governance_mode_alone_is_not_durable` + **반대 축** `..._that_refuses_bypass_is_durable` + `..._not_a_self_report` |

**fake 를 실물에 맞추자 durable canary 셋이 먼저 빨개졌다.** 그 셋은 "적대적
put 이 실패한다" 를 보고 있었는데, 실물 Object Lock 에서 그 put 은 **성공한다**
— retention 은 key 가 아니라 version 을 지킨다. 35차 fake 가 그 창을 가리고
있었다 (32차 "canary 가 강제하는 쪽이 아니었다" 의 재발). 불변식을 옳은 것으로
바꿨다: **담보한 바이트를 그래도 회수할 수 있다.**

`head_version` 은 계약에서 **제거**했다 — 담보 version 을 못 가리킨다.

### 3.4 #9a — 판정이 고정 경로를 읽었다

| 항 | 값 |
|---|---|
| 우회로 | `_cohort_projections(c)` — docstring 에 "판정에는 쓰지 않는다" 만 적혀 있었다 |
| 대응 | 함수를 **삭제**. `_cohort_manifests()` 는 경로를 주지 않고 읽힌 내용을 준다 |
| 재발 방지 | `test_no_cohort_assertion_reads_a_fixed_path` (AST — 정의·호출 둘 다) |
| 고친 판정 5 | cohort analyzer 단일성 · active 현행성 · schema/pin · 전 투영 pin · cohort 구성원 |
| 추가 회귀 | `test_a_crash_midway_through_materialize_never_moves_the_authority[0\|1\|2]` |

`_materialize` 중간 crash 불변식 셋: 권위 읽기 무영향 · `check_materialized()`
가 섞였다고 **말한다** · 재실행이 복구한다. 변이 2종(`cohort_bytes` 가 fixed
사본 읽기 · `check_materialized` 무검사) 모두 3 parametrize 전부에서 물었다.

### 3.5 #9b — 불완전 generation 의 public publisher

| 축 | 대응 | 검사 |
|---|---|---|
| 검사를 건너뛰는 공개 이름 | `promote_generation` → `_promote_generation` (비공개) | `test_the_incomplete_publisher_is_not_public` |
| 완전성이 쓰는 쪽에만 | `read_current()` 가 leg 3-suffix 완전성을 본다 | `test_reading_current_refuses_an_incomplete_cohort` (fixture 를 **바이트에서** 생성) |
| CURRENT lost-update | `_promote_generation(..., expect=)` compare-and-swap | `test_a_lost_update_cannot_silently_drop_another_legs_generation` |

34차 불완전-base fixture 는 **살아 있는 publisher** 로 만들어져 있었다 —
publisher 를 비공개로 만들자 fixture 가 먼저 깨졌고, 그것이 fixture 가 무엇을
보는지 알 수 없게 만들고 있었다는 증거다. `_handmade_generation()` 이 generation
디렉터리와 CURRENT 를 바이트에서 만든다.

## 4. 변이 시험 — 물지 않은 둘

| 물지 않은 변이 | 진단 | 처리 |
|---|---|---|
| `retain` 이 store 기한 미연장 | 시험이 축을 안 봤다 (지평에 덮임) | **시험을 고쳤다** (§3.2) |
| cohort publisher 의 base 완전성 loop 삭제 | `read_current()` 가 같은 것을 본다 | **코드를 지웠다** — 불변식은 한 곳에 |

두 번째는 지운 쪽이 맞다: `read_current()` 는 publisher 만이 아니라 **모든
독자**를 덮으므로 publisher 안의 사본은 검사를 하나 더 두는 것일 뿐이었다.

## 5. 산출물 재생성

`tools/preserve.py`(RUN_SCOPE) 와 `row_projection.py`(analyzer pin) 가 바뀌어
g2 투영·영수증을 다시 만들고 `LEG_PRESERVATION.yaml` pin 을 갱신했다.

| 항 | 이전 → 현재 |
|---|---|
| `source_digest` | `b79b0019d69a6fcf` → `4f4756746bd63496` |
| `compute_sha256` | `d56cb009767844c9` → `ab8aadbf521943fd` |
| `row_projection_py_sha256` | `f4e2da04c8bcf2e2` → `b00ec1c367532c5d` |
| receipt `core_sha256` | `6fe1137f79e0a226…` → `ddb3ac0b38b6c2e5…` |

행 바이트는 안 움직였다 (`proj ad598fe77e75afec` · 봉인일치 True).

## 6. 이 환경에서 닫히지 않는 것 — 신고

| 항 | 상태 | 왜 |
|---|---|---|
| 실제 object-lock provider adapter | **미구현** | 자격증명·네트워크 없음. 계약(9연산)·per-version 의미·bypass probe 는 고정 |
| power-loss ordering fault model | **미착수** | `os._exit` 는 fsync 안 된 항목을 잃지 않는다. fault-injecting filesystem 필요 |
| delete-marker 공격면 | **미모형** | fake 는 version 삭제만 모형한다. head 를 가리는 delete marker 는 별도 축 |

## 7. 리뷰 요청 사항

1. §3.3 의 **per-version 불변식 교체**가 옳은 축인가 — "적대적 put 이
   실패한다" 를 버리고 "담보 바이트를 회수할 수 있다" 로 옮긴 것.
2. §3.3 의 **GOVERNANCE 실측**이 충분한가 — canary 우회 삭제 시도로 답하는 것이
   실물 IAM 조건을 대표하는가, 아니면 GOVERNANCE 를 아예 거부해야 하는가.
3. §3.5 의 **compare-and-swap** 이 lost-update 를 실제로 닫는가 — `read_current`
   와 게시 사이가 아니라 게시 자체가 원자적이어야 하는 축이 남아 있는가.
4. §4 의 **중복 제거 판단** — `read_current()` 한 곳으로 모은 것이 맞는가.
5. §6 의 세 항을 미구현으로 신고한 것이 이 게이트에서 받아들여지는가.
