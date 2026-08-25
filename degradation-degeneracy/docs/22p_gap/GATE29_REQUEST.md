# 29차 게이트 리뷰 요청 — 28차 P0 (등록 retention) + P1 여섯 + P2 하나

> 자기 완결 문서다. 숫자는 옮겨 적지 않는다 — 영수증·투영·원장이 정본이다.

```yaml
브랜치:     origin/claude/14-gate-code-review-9qkx05
대상 커밋:   2e50531736f3d84197c043dd42c50a8a217a45bf
코드 커밋:   16489049…      # RUN_SCOPE 변경이 들어간 커밋
직전 대상:   352f8f159b89ee41ec8c080316cc33b845516554   (28차, NO-GO)

source_digest:
  28차:  62f45be76f526ce8
  현재:  0ca9f3d13bf21a59

재현:      git checkout 2e50531736f3d84197c043dd42c50a8a217a45bf
           cd degradation-degeneracy
```

## 0. 요청 판정

| 대상 | 요청 |
|---|---|
| 28차 P0 (등록 = object graph retention) | 닫혔는가 |
| P0-2 (closed receipt validator) · P1 1~6 · P2 | 어디까지인가 |
| 「최소 증거」 1~4 · 6~7 · 10~11 | 대응표 §3 |
| 5 (durability 주입) · 8 (shared canonicalizer 전체) · 9 (generation directory) | **부분** — §5 |
| 묶음 9 완료 · gate 배선 · 묶음 2 동결 | **요청하지 않는다** |
| 새 Stage 3 leg · 대규모 재실행 | **요청하지 않는다** |

## 1. 검증 — 방금 실행한 출력

```
$ git rev-parse HEAD
2e50531736f3d84197c043dd42c50a8a217a45bf
$ git status --short
(빈 출력)

$ python3 -m pytest tests/ -q
829 passed, 1 xfailed in 508.98s (0:08:28)

$ ./scripts/smoke_e2e.sh          # 16489049 (clean) 에서
✅ pipeline smoke 통과
⚠ 보존 gate 미완료 (계약 v4 묶음 9) — 새 leg 실행 금지.

$ python3 -c "…source_digest()"
0ca9f3d13bf21a59

$ python3 docs/22p_gap/make_receipt.py paired_fixed5_v4 --check
✅ paired_fixed5_v4: core 재생성 바이트 동일

$ python3 wiki/tools/lint.py
RESULT: 0 errors
```

## 2. 리뷰의 한 문장이 이 라운드의 전부다

> **read-before-register 는 retention 구조가 아니라 또 하나의 검사 시점이다.**

반례를 직접 재현했다 — 마지막 receipt read 직후 object 를 지우는 backend 에서:

```
transaction ok     : True
is_registered      : True
receipt 회수 가능?  : False
finalize_only      : {'ok': True, 'already': True}
```

### 2.1 등록을 retention commit 으로

성공 불변식을 문장이 아니라 구조로 적는다:

```text
registered(leg) ⇒ receipt · manifest · member · 산출 전부 회수 가능
```

local 에서 object-lock 의 대응물은 **hardlink** 다. `pins/<leg>/<dg>` 가 inode
를 붙들므로 `objects/` 를 통째로 비워도 회수된다. 등록 기록이 pin 집합 digest
를 이름하고, `is_registered(index, leg, backend)` 가 pin 완전성과 **바이트**를
확인한다. `finalize_only` 는 등록된 뒤에도 graph 를 다시 본다.

같은 반례가 이제 pin 단계에서 멈춘다:

```
✓ [pin] pin 할 object 가 없다: 510f1fe46deafd1a
  is_registered(backend 포함): False
```

## 3. 「최소 증거」 대응

| # | 요구 | 회귀 |
|---|---|---|
| 1 | final read 직후 삭제 · restore read 직후 manifest/member 삭제가 등록을 막는다 | `test_deleting_an_object_right_after_the_final_read_blocks_registration` · `_DropAfterRead` backend |
| 2 | `registered ⇒ 전체 graph 회수 가능` + pin/retention | `test_registration_requires_the_whole_graph_to_survive_deletion` — `objects/` 를 통째로 지워도 등록 유효, pin 까지 지우면 무효 |
| 3 | exact closed receipt schema · `planned_id == H(envelope)` · 실제 backend URI · output graph | `check_receipt()` · `test_a_forged_seven_key_receipt_is_refused` · `test_a_receipt_naming_another_backend_is_refused` |
| 4 | already-registered 에서 object 를 잃으면 fail-closed | `test_finalize_only_rechecks_the_graph_even_when_already_registered` |
| 6 | wrapper 가 실제 bytes 를 측정·CAS 보존 | `test_output_bytes_are_measured_by_the_wrapper_and_kept_in_cas` · `test_a_lying_output_descriptor_is_overruled_by_measurement` · `test_an_output_path_cannot_escape_the_restore_root[5종]` |
| 7 | manifest 집계 exact type · nonempty root | `test_boolean_aggregates_are_not_integers` · `test_restore_refuses_a_root_that_is_not_empty` |
| 10 | recursive closed design validator · NFC dict key/type axis · objective membership | `test_nested_design_blocks_are_validated_not_just_top_level_keys[8종]` · `test_parent_digest_domains_and_type_axis_nfc_are_checked` · `test_a_warm_candidate_must_name_an_objective_in_the_design` |
| 11 | role+generation 동시 변조가 실패 | role 행에서 세대를 없애고 봉인 digest 에서 **도출** — `test_claim_roles_are_a_machine_contract_not_free_prose` |

## 4. P1-4 — 두 감사 경로가 **또** 갈렸다

`make_receipt` 는 `_F4_주의` 를 정규 view 에 다시 넣었는데 `row_projection` 의
비교기는 계속 떼고 있었다. 봉인 summary 의 인용 금지 경고를 "안전" 으로 바꿔도
`재계산_검증.전체_일치` 에 diff 가 안 생겼다.

`SEMANTIC_SKIP` 정본을 `row_projection` 한 곳에 두고 `make_receipt` 가 import
한다. 회귀가 복제를 막는다 (`test_both_audit_paths_share_one_semantic_view`).

## 5. 부분인 것 — 스스로 적는다

| # | 무엇 | 왜 부분인가 |
|---|---|---|
| 5 | durability 주입 | capability 를 **만들기 전에** 재고 못 하면 멈추게 했고 staged object 도 fsync 한다. 다만 short write·link 직후 crash·directory-flush 실패를 **실제로 주입**하는 시험은 없다 |
| 8 | shared canonicalizer | semantic view 는 한 곳으로 모았다. 다만 `_F4_주의` 변이가 **cohort promotion 까지** 막는지는 receipt 쪽만 회귀가 있다 |
| 9 | generation directory promotion | 아직 **fixed-name 세 파일** `os.replace` 다. manifest-last 는 promotion order 이지 set atomicity 가 아니다 — 리뷰 P1-5 가 맞다. immutable generation directory + 단일 pointer 가 다음 checkpoint |

## 6. 계속 열려 있다고 적는 것

1. `run.sh`·smoke 의 **필수 gate 로 배선되지 않았다.**
2. 실제 운영 backend canary 가 없다. local hardlink pin 은 object-lock 의
   **대응물**이지 그 자체가 아니다.
3. `planned_leg_index` 가 실제 leg 원장과 결속되지 않았다.
4. 묶음 2 는 domain 을 닫았지만 실제 v6 격자 실행과의 E2E 가 없다.
5. containment E2E · analyzer canary — 27차 요청대로 계속 다음 라운드.

## 7. 질문

**Q1 — pin 의 정확한 대응물.** local 은 hardlink 로 inode 를 붙들었다. 실제
backend 에서는 (a) object-lock/retention-until, (b) 별도 immutable prefix 로의
server-side copy, (c) manifest 를 담은 단일 tar/zip object 로 pack — 셋 중
어느 쪽을 기준 의미로 볼 것인가? (c) 가 회수 단위를 하나로 만들어 가장
단순하지만 부분 회수를 잃는다.

**Q2 — generation directory 의 pointer 형태.** `cohort/generations/<digest>/`
+ 단일 pointer 로 바꾸려 한다. pointer 를 (a) `CURRENT` 파일, (b) leg 마다
`<leg>.pointer.json` 중 어느 쪽으로 둘 것인가? cohort 안에서 다리마다 세대가
갈릴 수 있으므로 (b) 로 보는데, 그러면 "cohort 전체가 한 세대" 라는 지금
불변식이 약해진다.

**Q3 — durability 주입 시험의 범위.** short write·link 직후 crash·directory
flush 실패를 실제로 주입하려면 filesystem 을 가로채야 한다. (a) `os` 함수를
monkeypatch 하는 단위 시험, (b) 별도 fault-injecting backend 클래스 중 어느
쪽을 acceptance 로 인정하는가? (a) 는 실제 syscall 경계를 흉내만 내고,
(b) 는 local backend 구현 자체는 못 건드린다.
