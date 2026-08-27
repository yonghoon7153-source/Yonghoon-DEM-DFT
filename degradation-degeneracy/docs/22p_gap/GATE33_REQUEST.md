# 33차 게이트 리뷰 요청 — 32차 P0 둘 · P2 · 최소 증거 #9

> 자기 완결 문서다. 숫자는 옮겨 적지 않는다 — 영수증·투영·원장이 정본이다.

```yaml
브랜치:     origin/claude/14-gate-code-review-9qkx05
대상 커밋:   6a656b88b99ad66598215688e20ade5b6f59f8d4
코드 커밋:   f7c0aee3…      # RUN_SCOPE 변경이 들어간 커밋
직전 대상:   44d6efdb…      (32차, NO-GO)

source_digest:
  32차:  d85449e57d74fdfb
  현재:  09d9caae89285f31

재현:      git checkout 6a656b88b99ad66598215688e20ade5b6f59f8d4
           cd degradation-degeneracy
```

## 0. 요청 판정

| 대상 | 요청 |
|---|---|
| P0-1 (provider 가 바이트를 소유 · verifier 세 구멍) | 닫혔는가 |
| P0-3 (object/pin retry · CAS root edge · journal 복구 · exact vector) | 닫혔는가 |
| P2 (verified receipt 회수) | 닫혔는가 |
| #9 (immutable generation + 단일 CURRENT) | 닫혔는가 |
| 실제 provider adapter | **미구현으로 신고한다** — 붙일 provider 가 없다 |
| power-loss ordering fault model | **미착수로 신고한다** |
| 묶음 9 완료 · gate 배선 · 묶음 2 동결 | **요청하지 않는다** |
| 새 Stage 3 leg · 대규모 재실행 | **요청하지 않는다** |

## 1. 검증 — 방금 실행한 출력

```
$ git rev-parse HEAD
6a656b88b99ad66598215688e20ade5b6f59f8d4
$ git status --short
(빈 출력)

$ python3 -m pytest tests/ -q
970 passed, 1 xfailed in 282.48s (0:04:42)

$ ./scripts/smoke_e2e.sh          # 215bd4c4 (clean) 에서
✅ pipeline smoke 통과
⚠ 보존 gate 미완료 (계약 v4 묶음 9) — 새 leg 실행 금지.

$ python3 -c "…source_digest()"
09d9caae89285f31

$ python3 docs/22p_gap/make_receipt.py paired_fixed5_v4 --check
✅ paired_fixed5_v4: core 재생성 바이트 동일 · core_sha 919e61bb120e131a

$ python3 wiki/tools/lint.py
RESULT: 0 errors
```

## 2. P0-1 — 지적이 정확했다

리뷰의 문장을 그대로 인정한다: 31차 canary 는 "강제가 있는 쪽이 아니라
**local bytes 와 독립된 metadata 장부가 있는 쪽**" 이었다.

| 연산 | 31차 | 지금 |
|---|---|---|
| `put_if_absent`·`read_back`·`has` | local `objects/` | provider |
| `pin`·`pinned`·`read_pinned` | local `pins/` | provider |
| `store_id`·`uri` | local | provider |

canary 두 개가 리뷰가 요구한 형태다:

| 회귀 | 무엇을 보인다 |
|---|---|
| `..._locked_graph_survives_wiping_the_local_root` | local root 를 **통째로 지운 뒤** graph 전부 회수 |
| `..._provider_actually_refuses_to_delete_a_locked_object` | `retain_until` 전 delete/overwrite 를 provider 가 **실제로 거부** |

verifier 의 세 구멍도 번호대로 닫았다. 다섯 축을 각각 물린다:

```
empty_version · foreign_version · mode_changed · until_shortened · lock_released
```

**미구현으로 신고한다**: 실제 provider(S3 Object Lock 등) adapter 는 없다.
이 환경에 붙일 provider 가 없어서다. 여기 있는 것은 계약을 만족하는
in-process store 이며, adapter 는 같은 일곱 연산(`put`·`get`·`delete`·`lock`·
`describe`·`describe_object`·`keys_under`)을 구현하면 된다.

## 3. P0-3 — 네 곳에 같은 형태가 남아 있었다

31차에 "이름이 있는 한 항상 굳힌다" 고 적고 `_exclusive_write()` 에만
적용했다.

| 곳 | 회귀 |
|---|---|
| `put_if_absent` 기존-name branch | `..._cas_object_retry_must_fsync_the_prefix_again` |
| `pin` 기존-pin branch | `..._pin_retry_must_fsync_the_pin_directory_again` |
| `_mkdir_durable` 의 조기 return | `..._directory_that_exists_is_still_re_fsynced_on_retry` |
| `store_id` 의 CAS root 이름 | `..._fresh_store_root_flushes_its_own_parent_entry` |

그리고 `during_journal_fsync` 복구가 완료되지 않았다 — journal 이 보이지만
durable 하지 않을 수 있는 상태에서 `already` 로 빠져나갔다. 이제 재개가
`registered/` 를 다시 굳혀 commit 을 끝낸다. drill 집계도 exact vector 다:

```
{'after_pin': False, 'after_publish': False,
 'after_register': True, 'during_journal_fsync': True}
```

## 4. P2 — reader 가 실물을 읽는다

31차판은 index entry 와 journal 의 `receipt_object` **문자열** 일치로 등록을
셌다. 이제 `verify_registered_graph()` 가 돌려준 receipt 를 쓰고, index 의
`planned_envelope` 사본은 **대조 대상**이다 (갈리면 오류).

reader 시험도 진짜 트랜잭션으로 만든 등록을 쓴다 — 31차 시험은
`planned_id="p"`·`receipt_digest="r"` 로 CAS·receipt 없이 `publish()` 와
private `_register()` 만 부르고 "real registration" 이라 불렀다. 그 지적이
맞았다.

## 5. #9 — immutable generation + 단일 CURRENT

```text
out/gen/<generation_id>/…   ← 내용 주소가 이름. 한 번 쓰고 절대 안 고친다
out/CURRENT                 ← 이 한 파일만 원자적으로 바뀐다
```

| 회귀 | 무엇을 고정 |
|---|---|
| `..._publishes_an_immutable_generation_then_one_pointer` | 멱등 · 새 내용은 **새** generation · 옛 것 보존 |
| `..._generation_directory_is_never_overwritten` | 같은 자리에 다른 바이트면 거부 |
| `..._readers_follow_current_and_a_torn_pointer_is_refused` | 없음·깨짐·없는 generation 전부 fail-closed |
| `..._torn_pointer_write_never_replaces_a_good_one` | 부분 쓰기가 옛 pointer 를 안 망가뜨린다 |
| `..._crash_between_generation_and_pointer_leaves_no_mixed_state` | pointer 직전 사망 → 옛 generation 이 그대로 |

## 6. 「최소 증거」 대응표

| 항 | 요구 | 상태 |
|---|---|---|
| 1 | provider 가 bytes 의 put/read/retrieve 와 lock/version query 를 함께 소유 | 닫음 (§2) — **실제 adapter 는 미구현** |
| 2 | local 제거 뒤 provider 에서 회수 · 기간 전 delete/overwrite 실패 | 닫음 (§2) |
| 3 | empty/None/foreign version · mode 변경 · per-version until 을 각각 | 닫음 (§2, 다섯 축) |
| 4 | object·pin 의 "final name→fsync 실패→retry" 가 다시 fsync | 닫음 (§3) |
| 5 | mkdir→parent fsync 실패→retry · fresh `store_id` · split filesystem | 닫음 (§3). **power-loss fault model 은 미착수** |
| 6 | `during_journal_fsync` reopen 이 다시 fsync 한 뒤에만 성공 · exact vector | 닫음 (§3) |
| 7 | canonical backend 에서 verified receipt 를 회수해 generation 결속 | 닫음 (§4) |
| 8 | immutable cohort generation + single `CURRENT` + promotion fsync/crash | 닫음 (§5) |

## 7. 변이로 확인했고, 물지 않은 것 셋

| 물지 않은 변이 | 왜 | 처리 |
|---|---|---|
| lease version 값 검사 삭제 | live 조회가 같은 것을 잡아 메시지가 겹쳤다 | 두 축의 메시지를 갈라 각각 고정 |
| pointer 원자성 삭제 | 단일 프로세스로는 관측 불가 | 부분 쓰기 주입으로 옛 pointer 생존을 확인 |
| "없는 generation" 검사 삭제 | 앞의 id 검사에 업혀 통과 | 자기정합 pointer 로 축 분리 |

세 라운드 연속 같은 형태다 — **시험이 다른 축에 업혀 통과하는 것**.

## 8. 산출물

영수증을 clean tree 에서 다시 만들었다 (`validator_tree_dirty: false`,
commit `f7c0aee3`). 원장 pin:

```text
compute_sha256                    3084596353e63426 → a7def130d68d79a1
row_projection_py_sha256          53ae8205d201517c → a30847533ef8fcfd
verification_receipt_core_sha256  bf3d0b7b… → 919e61bb…
validator_identity.source_digest  d85449e57d74fdfb → 09d9caae89285f31
```

행 바이트는 안 움직였다 — `projection_sha256`·`restart_projection_sha256`·
`fits_sha256` 이 g1 과 여전히 동일하다. `g1_2026_08_20` 은 frozen, 손대지
않았다. `tools/design_golden.yaml` 도 바이트 동일이다.
