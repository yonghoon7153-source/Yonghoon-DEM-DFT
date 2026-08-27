# 32차 게이트 리뷰 요청 — 31차 P0 둘 · P1 넷 · P2

> 자기 완결 문서다. 숫자는 옮겨 적지 않는다 — 영수증·투영·원장이 정본이다.

```yaml
브랜치:     origin/claude/14-gate-code-review-9qkx05
대상 커밋:   44d6efdb260a2f8e9f4ee708191489c102cc4c43
코드 커밋:   209fd63e…      # RUN_SCOPE 변경이 들어간 커밋
직전 대상:   799687b2…      (31차, NO-GO)

source_digest:
  31차:  d0a0904b339554cd
  현재:  d85449e57d74fdfb

재현:      git checkout 44d6efdb260a2f8e9f4ee708191489c102cc4c43
           cd degradation-degeneracy
```

## 0. 요청 판정

| 대상 | 요청 |
|---|---|
| P0-1 (enforcement 를 capability 로) | **타입 경계만** 종결 주장 — actual adapter 는 미구현으로 신고 (§2) |
| P0-3 (index edge · capability · retry · crash 양성) | 닫혔는가 |
| P1-1 (checks 값) · P1-2 (output union·path) · P1-3 (mode enum) · P1-4 (chain 내부 유도) | 닫혔는가 |
| P2 (registry 발견) | 닫혔는가 — **30차 주장 하나를 철회했다** (§6) |
| 「최소 증거」 1~8 | 대응표 §7 |
| 2 (object-lock adapter canary) · 9 (immutable generation) | **미구현/미착수로 신고한다** |
| 묶음 9 완료 · gate 배선 · 묶음 2 동결 | **요청하지 않는다** |
| 새 Stage 3 leg · 대규모 재실행 | **요청하지 않는다** |

## 1. 검증 — 방금 실행한 출력

```
$ git rev-parse HEAD
44d6efdb260a2f8e9f4ee708191489c102cc4c43
$ git status --short
(빈 출력)

$ python3 -m pytest tests/ -q
954 passed, 1 xfailed in 277.35s (0:04:37)

$ ./scripts/smoke_e2e.sh          # d3e3d776 (clean) 에서
✅ pipeline smoke 통과
⚠ 보존 gate 미완료 (계약 v4 묶음 9) — 새 leg 실행 금지.

$ python3 -c "…source_digest()"
d85449e57d74fdfb

$ python3 docs/22p_gap/make_receipt.py paired_fixed5_v4 --check
✅ paired_fixed5_v4: core 재생성 바이트 동일 · core_sha bf3d0b7b020f54f1

$ python3 wiki/tools/lint.py
RESULT: 0 errors

```

전체 suite 는 영수증·원장 pin 을 갱신한 **뒤** 다시 돌린 결과다.

## 2. P0-1 — 리뷰가 준 정적 반례를 그대로 돌렸다

```python
CasBackend(root=cas, enforcement="object_lock")   # → TypeError
b.enforcement = "object_lock"                      # → PreserveError [capability]
```

| 축 | 지금 |
|---|---|
| 생성자 지정 | `ENFORCEMENT` 는 `ClassVar` — 인자가 아니다 |
| 사후 대입 | `__setattr__` 이 막는다 |
| lease 의 값 | 신고값이 아니라 `probe_enforcement()` **조회 결과** |
| lease ↔ 실물 | `verify_retention()` 이 대조한다 (권위는 여기 **한 곳**) |
| lock 증거 | provider 의 `lock_mode` + immutable `object_versions`, 검증 때 **재조회** |
| `finalize_only()` | 두 경로 모두 typed 결과 (`retention`·`durable`) |

`ObjectLockBackend` 로 adapter 자리를 만들었다. 경계가 한쪽으로만 닫히면
시험이 아니므로 강제가 **있는** 쪽도 canary 로 고정했다:

| canary | 무엇을 고정 |
|---|---|
| `..._can_claim_durable_retention` | provider 가 version·mode 를 주면 `durable=True` |
| `..._stops_enforcing_loses_durable_retention` | 정책 하한이 내려가면 그 자리에서 잃는다 |
| `..._forgets_a_version_loses_durable_retention` | version 이 사라지면 잃는다 |
| `..._without_a_provider_is_advisory` | 클래스 이름만으로는 강제가 아니다 |

**미구현으로 신고한다**: 실제 provider(S3 Object Lock 등) adapter 는 없다.
리뷰가 "이것 전에는 durable gate 를 닫지 말 것" 이라고 했고, 닫지 않았다.
남은 일은 세 메서드 구현이다 — `query_object_lock` · `lock_objects` ·
`query_object_versions`.

## 3. P0-3 — CAS 쪽만 닫혀 있었다

| # | 무엇 | 회귀 |
|---|---|---|
| 1 | `index/`·`index/legs`·`index/registered` 새 edge 를 안 굳혔다 | `..._index_and_journal_levels_flush_their_parent_entry` |
| 2 | capability 없으면 조용히 `return` | `..._without_directory_fsync_cannot_publish_a_graph` |
| 3 | 재시도가 `EEXIST` 로 fsync 를 건너뛰고 성공 | `..._retry_after_a_failed_directory_fsync_must_fsync_again` |
| 4 | crash drill 두 지점이 모두 `_register()` 앞 | `after_register`·`during_journal_fsync` 추가 |

2번은 주석까지 틀렸었다 — "publish 가 이미 막는다" 는 CAS 와 index 가 같은
filesystem 일 때만 참이다. 갈라 주입하니 `put_if_absent()` 가 그냥 성공했다.

4번은 이번 라운드 자기기만의 대표다. 시험 이름은
`journal visible ⇒ full graph retrievable` 인데 **전건이 한 번도 참이 되지
않았다**. 이제 양성/음성 도달을 별도 시험이 강제한다:

```
{'after_pin': False, 'after_publish': False,
 'after_register': True, 'during_journal_fsync': True}
```

## 4. P1 넷

| # | 고침 | 대표 회귀 |
|---|---|---|
| 1 | `checks` 값이 전부 참이어야 하고, 검사 **이름 집합**을 receipt 에 봉인 | `..._false_subcheck_cannot_hide_inside_a_successful_receipt` · `..._seals_the_check_names_not_just_a_count` |
| 2 | role 별 **exact** key set · `relative_path` 를 manifest 와 같은 `_safe_member_path()` 로 | `..._output_variants_reject_fields_from_another_variant` · `..._output_paths_use_the_same_validator_as_manifest_members` (6) |
| 3 | mode enum 을 계약 §3 에서 **파싱** | `..._candidate_mode_enum_comes_from_the_contract_not_a_second_list` |
| 4 | `binding` 인자를 **없앴다** — 봉인물만 받고 chain 을 유도 | `..._forged_binding_has_nowhere_to_go` · `..._binding_derives_order_and_bank_version_from_the_design` |

P1-4 는 두 회차 연속 같은 형태다. 30차에 "plan 을 인자로 받을 수 있다는 것
자체가 결함" 이라고 적어 놓고 plan 을 담은 dict 를 인자로 만들었다.
golden vector 는 **바이트 동일**이다 — ID domain 은 안 움직였다.

## 5. P0-2 hardening

`root` 를 `__post_init__` 에서 고정했다. 30차 반례는 backend **객체 두 개**를
만들었으므로, 같은 객체가 cwd 변경만으로 다른 store 를 가리키는 축은 보지
못했다. URI 는 `Path.as_uri()` 로 만든다.

## 6. P2 — 30차 주장을 철회한다

30차 요청문과 원장 §39.5 에 "등록이 생기는 순간 fail-closed 로 켜진다" 고
적었다. **거짓이었다.** 검사 대상을 가변 원장의 optional
`evidence.registered_receipt` 로 골랐으므로, 실제 등록이 생겨도 그 필드를 안
적으면 검사가 잠들었다.

이제 실제 index 의 journal 을 읽고 **양방향**으로 본다:

| 방향 | 실패 조건 |
|---|---|
| index → 원장 | 등록됐는데 원장에 없다 · receipt 의 `source_digest`/`protocol_generation` 이 원장·세대표와 다르다 |
| 원장 → index | 원장이 등록을 주장하는데 index 에 없다 |

실물 index 가 아직 없어 결과는 여전히 비어 있지만 **이유가 다르다** — 원장이
고른 것이 아니라 실물이 없다. 규칙이 무는지는 합성 index 시험
(`..._generation_binding_bites_on_a_synthetic_registry`, 다섯 방향)과 reader
자체 시험(`..._registry_reader_finds_a_real_registration`)이 보인다.

`digest → generation` 화살표는 **여전히 선언**이다 — 실행 산출물에 그 필드가
없다. 30차와 같은 신고이며 바뀌지 않았다.

## 7. 「최소 증거」 대응표

| 항 | 요구 | 상태 |
|---|---|---|
| 1 | local enforcement 를 생성자에서 못 바꾸게 · fake label 로 durable 불가 | 닫음 (§2) |
| 2 | actual object-lock adapter + live canary | **타입 경계·canary 종결 / adapter 미구현** — §2 |
| 3 | `run_transaction`·`finalize_only` 의 모든 성공 경로가 같은 typed 결과 | 닫음 (§2) |
| 4 | CAS/index 다른 capability · 모든 새 parent edge · retry 재-fsync | 닫음 (§3) |
| 5 | journal commit 직전/직후 kill 에서 **양성** 전건 | 닫음 (§3). power-loss ordering 은 별도 fault model 필요 — 미착수 |
| 6 | `checks` 값 · output role 별 exact key · 공유 path validator · 계약과 같은 mode enum | 닫음 (§4) |
| 7 | forged binding · order/version 불일치 거부 · sealed preimage 에서 재유도 | 닫음 (§4) |
| 8 | actual registry 에서 등록 leg 발견해 결속 | 닫음 (§6). generation value 는 선언 |
| 9 | immutable cohort generation + single `CURRENT` | **미착수** |

## 8. 변이로 확인했고, 물지 않은 것 다섯

| 물지 않은 변이 | 왜 | 처리 |
|---|---|---|
| `assert_durable_retention` 의 재조회 삭제 | `verify_retention` 이 이미 대조 | 중복이라 **삭제** — 권위를 한 곳으로 |
| output exact key set → subset | 시험이 **남는** 키만 넣고 **모자란** 경우를 안 봤다 | 누락 축 추가 |
| capability fail-closed 삭제 | 시험이 `store.json` 쓰기에 업혀 통과 | store 를 먼저 만들고 CAS 쓰기만 보게 분리 |
| `bank_version` 유도 삭제 | design digest 에 이미 들어 있어 `bank_id` 가 어차피 달라진다 | 유도값 자체를 보는 시험으로 |
| crash drill 양성 상태 | 전건이 거짓이라 공허하게 참 | 양성/음성 도달을 강제하는 시험 추가 |

## 9. 산출물

영수증을 clean tree 에서 다시 만들었다 (`validator_tree_dirty: false`,
commit `209fd63e`). 원장 pin:

```text
verification_receipt_core_sha256  43386a98… → bf3d0b7b…
validator_identity.source_digest  d0a0904b339554cd → d85449e57d74fdfb
```

g2 투영은 재생성해도 **바이트 동일**이다. `g1_2026_08_20` 은 frozen — 손대지
않았다. `tools/design_golden.yaml` 도 바이트 동일이다.
