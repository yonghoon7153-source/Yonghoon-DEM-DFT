# 35차 게이트 리뷰 요청 — 34차 P0-1 · P2 · #9

> 자기 완결 문서다. 숫자는 옮겨 적지 않는다 — 영수증·투영·원장이 정본이다.

```yaml
브랜치:     origin/claude/14-gate-code-review-9qkx05
대상 커밋:   3698be729283f55a866e916ddbe261786a98a866
직전 대상:   76759f9f…      (34차, P0-3 종결 유지 / 나머지 NO-GO)

source_digest:
  34차:  71321d826194f75a
  현재:  b79b0019d69a6fcf

재현:      git checkout 3698be729283f55a866e916ddbe261786a98a866
           cd degradation-degeneracy
```

## 0. 요청 판정

| 대상 | 요청 |
|---|---|
| P0-1 (lease proof 재발견 · control-plane 잠금) | 닫혔는가 |
| P2 (raw journal 열거 · 사본 필수) | 닫혔는가 |
| #9 (실제 reader authority · snapshot 완전성) | 닫혔는가 |
| P0-3 | 33차 종결 · 34차 유지 — 재검 요청하지 않는다 |
| 실제 provider adapter · power-loss fault model | **미구현으로 신고한다** |
| 묶음 9 완료 · gate 배선 · 묶음 2 동결 | **요청하지 않는다** |
| 새 Stage 3 leg · 대규모 재실행 | **요청하지 않는다** |

## 1. 검증 — 방금 실행한 출력

```
$ git rev-parse HEAD
3698be729283f55a866e916ddbe261786a98a866
$ git status --short
(빈 출력)

$ python3 -m pytest tests/ -q
994 passed, 1 xfailed in 314.78s (0:05:14)

$ ./scripts/smoke_e2e.sh
✅ pipeline smoke 통과
⚠ 보존 gate 미완료 (계약 v4 묶음 9) — 새 leg 실행 금지.

$ python3 -c "…source_digest()"
b79b0019d69a6fcf

$ python3 docs/22p_gap/make_receipt.py paired_fixed5_v4 --check
✅ paired_fixed5_v4: core 재생성 바이트 동일 · core_sha 6fe1137f79e0a226

$ python3 wiki/tools/lint.py
RESULT: 0 errors
```

## 2. 세 발견이 같은 형태였다 — 시제만 달랐다

| 회차 | 형태 |
|---|---|
| 33차 | 고친 것과 **실제로 쓰이는 것**이 다르다 |
| 34차 | 최초 정상 경로는 맞는데 **그 다음 상태**가 빠졌다 |

| 발견 | 최초 경로 | 빠진 다음 상태 |
|---|---|---|
| P0-1 | lease 를 잠근다 | 재개가 그 proof 를 **재발견**하지 못한다 |
| P2 | 후보의 graph 실패를 보고한다 | 후보를 **고르는 술어**가 깨진 journal 을 앞에서 숨긴다 |
| #9 | writer 가 CURRENT 로 게시한다 | 실제 reader 가 fixed 사본을 **읽는다** |

## 3. P0-1 — proof 재발견

| 반례 | 회귀 |
|---|---|
| 완료 뒤 같은 트랜잭션 재실행 | `..._rerunning_an_object_lock_transaction_reuses_the_same_lease` |
| lease lock 뒤 journal 전 crash → 새 provider/backend 로 재개 | `..._crash_between_lease_lock_and_journal_can_be_finalized` |
| `store.json` control-plane 보존 | `..._provider_control_plane_is_locked_too` |

두 반례 모두 **시계를 전진**시켰다. 같은 초 안에서는 lease 바이트가 같아
우연히 재사용되므로, 그러면 시험이 아무 것도 시험하지 않는다.

불변식: **lease 가 한 번 잠겼다면 어느 후속 지점에서 죽어도 reopen 이 같은
lease digest 와 같은 provider version 을 재발견하고 재사용한다.**

adapter 계약을 정정한다 — 7연산이 아니라 **9연산**이다:
`put` · `get` · `delete` · `lock` · `describe` · `describe_object` ·
`keys_under` · `store_uri` · `head_version`.

## 4. P2 — raw namespace 에서 발견한다

`registered/*.json` 과 `legs/*.json` 을 직접 열거하고 **parse → index 대응 →
receipt 일치 → graph** 순으로 본다.

| 손상 | 회귀 |
|---|---|
| truncated · `{}` · foreign receipt · orphan · missing index | `..._damaged_raw_journal_is_an_error_not_an_absence` (5) |
| raw journal 있는데 backend 없음 | `..._raw_journals_without_a_backend_are_an_error` |
| index 사본 **누락** | `..._generation_binding_bites_on_a_synthetic_registry` 3b |

## 5. #9 — reader authority 와 snapshot 완전성

| 축 | 회귀 |
|---|---|
| active reader 가 CURRENT 를 따른다 (fixed 사본을 흔들어도) | `..._lint_readers_follow_current_not_the_fixed_copies` |
| `_materialize` 중 crash 에서 실제 reader 가 G1 만 본다 | `..._real_readers_see_only_the_new_generation_after_a_materialize_crash` |
| leg 당 세 suffix exact set | `..._partial_leg_stage_cannot_be_promoted` (4) |
| 불완전 base 를 물려받지 않는다 | `..._incomplete_base_generation_cannot_be_carried_forward` |

frozen g1 은 원자료를 잃어 migration 불가이므로 fixed fallback 을 **명시적
예외**로 유지한다 — 같은 시험이 그 예외를 함께 고정한다.

## 6. 변이 — 셋, 전부 "시험이 그 축을 안 보던" 자리

| 물지 않은 변이 | 처리 |
|---|---|
| base 완전성 검사 삭제 | 검사를 우회해 불완전 base 를 만든 뒤 물리는 시험 추가 |
| active reader **이름**을 fixed glob 으로 | **lint 가 쓰는 함수**를 직접 부르는 시험 추가 |
| active reader **바이트**를 fixed 사본으로 | 같은 시험에서 함께 |

helper 가 맞는 것과 실제 소비자가 그것을 쓰는 것은 다른 축이다 — 34차 발견
셋이 전부 이 구분이었고, 변이에서 나온 셋도 같았다.

## 7. 남은 것 — 인프라

| 항 | 상태 |
|---|---|
| 실제 object-lock provider adapter | **미구현**. 계약 9연산과 canary 는 고정 |
| power-loss ordering fault model | **미착수**. fault-injecting filesystem 필요 |
| `digest → generation` value | **선언** — 실행 산출물에 그 필드가 없다 |

## 8. 산출물

투영과 영수증을 clean tree 에서 다시 만들었다 (`validator_tree_dirty: false`).
g2 는 `CURRENT` generation 으로 게시된다. 원장 pin:

```text
compute_sha256                    fa05b081fbca25ef → d56cb009767844c9
row_projection_py_sha256          e876bd425400143b → f4e2da04c8bcf2e2
verification_receipt_core_sha256  ec5ec0fa… → 6fe1137f…
validator_identity.source_digest  71321d826194f75a → b79b0019d69a6fcf
```

행 바이트는 안 움직였다. `g1_2026_08_20` 은 frozen — 손대지 않았다.
