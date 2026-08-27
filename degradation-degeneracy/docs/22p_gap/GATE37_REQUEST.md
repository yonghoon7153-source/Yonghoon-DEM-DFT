# 37차 게이트 리뷰 요청 — 36차 P0-1 · #9

> 자기 완결 문서다. 숫자는 옮겨 적지 않는다 — 영수증·투영·원장이 정본이다.

```yaml
브랜치:     origin/claude/14-gate-code-review-9qkx05
대상 커밋:   988a5216bd042c003d9a8c5ae7b34eaecf3e606d
직전 대상:   6c11cf6c…      (36차, 좁은 항목 9 종결 / P0-1·#9 NO-GO)

source_digest:
  36차:  4f4756746bd63496
  현재:  ccb3e2ad0f6145c0

재현:      git checkout 988a5216bd042c003d9a8c5ae7b34eaecf3e606d
           cd degradation-degeneracy
```

## 0. 요청 판정

| 대상 | 요청 |
|---|---|
| P0-1 발견 1 (삭제 포함 lease crash recovery) | 닫혔는가 |
| P0-1 발견 2 (canonical store identity 의 immutable version authority) | 닫혔는가 |
| P0-1 발견 3 (exact per-version 의미 · Governance · fake semantics) | 닫혔는가 |
| #9 발견 1 (`expected_current` 가 실제 atomic 인가) | 닫혔는가 |
| #9 발견 2 (실제 reader · snapshot roster) | 닫혔는가 |
| P0-3 · P2 | 33·35차 종결 — 재검 요청하지 않는다 |
| 실제 provider adapter · power-loss fault model | **미구현으로 신고한다** |
| 묶음 9 완료 · gate 배선 · 묶음 2 동결 | **요청하지 않는다** |
| 새 Stage 3 leg · 대규모 재실행 | **요청하지 않는다** |

## 1. 검증 — 방금 실행한 출력

```
$ git rev-parse HEAD
988a5216bd042c003d9a8c5ae7b34eaecf3e606d
$ git status --short
(빈 출력)

$ python3 -m pytest tests/ -q
1031 passed, 1 xfailed in 489.37s (0:08:09)

$ ./scripts/smoke_e2e.sh
✅ pipeline smoke 통과
⚠ 보존 gate 미완료 (계약 v4 묶음 9) — 새 leg 실행 금지.

$ python3 docs/22p_gap/make_receipt.py paired_fixed5_v4 --check
✅ paired_fixed5_v4: core 재생성 바이트 동일 · core_sha c80b580a8647dfde

$ python3 wiki/tools/lint.py
RESULT: 0 errors
```

## 2. 출발점 — fake 를 실물에 맞추자 **여덟이 빨개졌다**

리뷰 §3-3 을 먼저 처리했다. 그것이 나머지를 가리고 있었기 때문이다.

| fake 의 거짓 | 실물 |
|---|---|
| 잠긴 head 에 같은 바이트 put → 같은 version 재사용 | `PutObject` 는 **요청마다** version |
| version 없는 delete → head 삭제 | **delete marker** 를 얹고 보호 version 은 남는다 |

fake 를 고치자 durable canary·phase drill·lease 재사용 등 **8개가 즉시**
빨개졌다. 32차 "canary 가 강제하는 쪽이 아니었다" 의 재발이다 — 이번 canary 는
바이트를 들고 있었지만 **의미**를 거꾸로 들고 있었다.

| 드러난 결함 | 수정 |
|---|---|
| `lock_objects`·`lock_content_object` 무조건 `put` → 재시도마다 WORM version 누적 | `_existing_version()` 재사용 |
| `pinned()` 이 delete marker 뒤 담보를 못 봄 | 열거를 `list_versions`(ListObjectVersions)로 |
| "lease 가 하나다" 가 key 만 셈 | **version cardinality** 를 센다 (`_version_census`) |

계약 정리: `keys_under`(ListObjectsV2) **제거** — marker 뒤를 못 본다.
`delete` **제거** — 우리는 어떤 경로로도 지우지 않으므로 adapter 에게 요구할
근거가 없다. 남은 8연산은 `PROVIDER_CONTRACT` 가 authority 이고 AST 가 대조한다.

## 3. 발견별 대응

### 3.1 P0-1 발견 1 — 삭제 포함 crash recovery

| 항 | 값 |
|---|---|
| 반례 재현 | `test_a_deletion_inside_the_unlocked_window_never_mints_a_second_lease[3 phase]` — **재현했다**: `after_pin_lock` 에서 lease pin 이 2개 |
| 순서 뒤집기 | `repair_lease_locks()` 가 `read_pinned()` 로 **살아남은 pin 바이트**를 먼저 읽고, content 가 없으면 그것으로 되살린 뒤 잠근다 |
| fail-closed | 모호(≥2) · 손상 · 수리 실패 · **만료 전** 검증 실패 → `None` 이 아니라 `PreserveError` |
| orphan 입양 | `_orphan_lease()` — `after_lease_put` 잔여를 새 lease 대신 **입양**한다 |
| 누적 금지 | `test_repeated_repair_never_inflates_locked_versions` (version 을 센다) |
| 갱신 축 | `test_an_expired_lease_is_renewed_not_refused` — 만료는 갱신이 맞다 |

> `after_lease_put` 은 pin 이 없으므로(그리고 시험이 content 도 지우므로) 새
> lease 가 유일한 정답이고, 그때는 지울 수 없는 WORM 잔여가 없다. pin 이
> 살아남은 두 phase 에서는 **성공**을 요구한다 — 거부도 허용하면 "복원 안 하고
> 그냥 거부" 변이가 초록이다 (실측했다).

### 3.2 P0-1 발견 2 — canonical store version

| 축 | 대응 | 검사 |
|---|---|---|
| latest-locked 가 authority | `_canonical_store_version()` = **가장 오래된** 유효 잠금 | `test_a_newer_locked_store_record_cannot_switch_the_identity` (A·B 둘 다 valid·locked) |
| exact schema | `_is_store_record()` — 닫힌 key set + `schema` 값 | `test_the_store_record_must_be_an_exact_schema_not_just_a_uuid` |
| 계약 아닌 담보 record | **거부** (재발급 금지 — 잠긴 쓰레기는 못 지운다) | `test_a_locked_non_contract_store_record_is_refused_not_reissued` |

### 3.3 P0-1 발견 3 — 의미

**Governance (Q2 답 수용).** `probe_bypass()` 를 **삭제**하고 GOVERNANCE 를
durable 에서 뺐다. `DURABLE_MODES = {COMPLIANCE}`. 근거는 리뷰 그대로다 —
delete 한 경로의 거부는 retention 단축·제거 권한·다른 principal·이후 IAM
변경을 증명하지 못한다. 31차에 local mode bit 를 uid 0 이 우회할 수 있다는
이유로 뺐으니 같은 잣대다. 시험은 `bypass=True/False` **양쪽**에서 advisory 를
요구한다 — 어떤 probe 결과로도 승격되지 않는다는 뜻이다.

**exact version 회수.** `retrieve_retained()` → `read_pinned(..., version=)` →
`provider.get(key, version)`. lease 의 `object_versions[dg]` 를 그대로 넘긴다.
회귀는 다른 바이트의 v2 를 올리고 **잠근다** (36차 회귀는 안 잠가서 fallback 만
봤다).

### 3.4 #9 발견 1 — 진짜 임계 구역

| 항 | 값 |
|---|---|
| 반례 재현 | `test_a_publish_between_compare_and_replace_cannot_be_lost` — A 의 **비교 read 가 G0 를 반환한 뒤** B 를 게시. 재현했다 |
| 구조 | `_PublishLock` (`O_CREAT\|O_EXCL`) 이 base 읽기·완전성 판정·자재화·pointer 전환을 **함께** 덮는다 |
| stale 회수 | `test_a_live_publish_lock_blocks_and_a_stale_one_is_reclaimed` |
| 불변식 변경 | "A 가 거부된다" → **"성공을 반환했으면 남아 있어야 한다"**. 앞의 것은 구현을 하나로 못 박는 과잉 규정이다 |

### 3.5 #9 발견 2 — snapshot handle + 명부

| 축 | 대응 |
|---|---|
| 고정 namespace read | `_Snapshot` 이 **경로를 밖으로 내보내지 않는다** — 이름과 이미 읽힌 바이트만 |
| mixed generation | reader operation 당 `CURRENT` **한 번**. 이름과 내용이 같은 generation |
| AST 금지 | 이름이 아니라 **namespace**: cohort record 의 `dir` 을 꺼내는 곳은 snapshot 생성자뿐 (`test_no_reader_touches_the_cohort_fixed_namespace`) |
| 옮긴 실제 reader | cohort self-consistency(대형) · 보존 원장 대조 · `recorded_projection` 판정 |
| completeness | nonempty + **기대 명부** 대조. 명부는 원장에서 온다 (고정 파일 목록에서 유도하면 자기 자신이 근거다) |
| 공유 validator | `assert_cohort_complete()` 를 publish·read **양쪽**에서 호출 (`test_the_publisher_and_the_reader_share_one_validator` 가 AST 로 확인) |

> **Q4 답 수용.** 36차에 publisher 쪽 검사를 지운 것은 오판이었다. 변이가 안
> 문 이유는 중복이어서가 아니라 **validator 가 약해서**였다.

## 4. 변이 — 여섯이 물지 않았고, 그것이 이번 라운드의 수확이다

| 물지 않은 변이 | 진단 | 처리 |
|---|---|---|
| repair 가 pin 바이트로 복원 안 함 | 시험이 fail-closed 도 허용 | pin 생존 시 **성공** 요구로 조임 |
| 수리 실패를 `None` 으로 | `finalize_only()` 가 journal 검증에서 먼저 죽어 분기 미도달 | 재진입점 `retain()` 을 직접 호출 |
| 만료 아닌 검증 실패를 `None` 으로 | 같은 이유 | 같은 처리 |
| 모호 후보를 `None` 으로 | 후보 2개 상태를 만드는 시험 없음 | 추가 |
| 계약 아닌 담보 record 재발급 | schema 시험이 **잠기지 않은** record 만 씀 | 잠긴 쓰레기 시험 추가 |
| 만료 판정 뒤집기 | 갱신 축 미검사 — "언제나 거부" 로도 초록 | 갱신 시험 추가 |

## 5. 산출물 재생성

| 항 | 이전 → 현재 |
|---|---|
| `source_digest` | `4f4756746bd63496` → `ccb3e2ad0f6145c0` |
| `compute_sha256` | `ab8aadbf521943fd` → `4d948d46f4123ce4` |
| `row_projection_py_sha256` | `b00ec1c367532c5d` → `c08b6309e6c79a7d` |
| receipt `core_sha256` | `ddb3ac0b38b6c2e5…` → `c80b580a8647dfde…` |

행 바이트는 안 움직였다 (`proj ad598fe77e75afec` · 봉인일치 True).

## 6. 이 환경에서 닫히지 않는 것 — 신고

| 항 | 상태 | 왜 |
|---|---|---|
| 실제 object-lock provider adapter | **미구현** | 자격증명·네트워크 없음. 계약 8연산 · per-version · delete-marker 의미는 고정 |
| power-loss ordering fault model | **미착수** | `os._exit` 는 fsync 안 된 항목을 잃지 않는다 |

delete-marker 는 이번에 **계약 안으로 들였다** (§2) — 더 이상 신고 항목이 아니다.

## 7. 리뷰 요청 사항

1. §3.1 의 **fail-closed 경계**가 옳은가 — "후보가 하나라도 있으면 새 state 를
   만들지 않는다" 가 너무 넓어 정당한 진행까지 막는 경우가 있는가.
   (`after_lease_put` 을 예외로 둔 판단 포함)
2. §3.2 의 **가장 오래된 유효 잠금**이 옳은 authority 인가 — receipt 에 store
   version proof 를 봉인하는 쪽이 더 나은가.
3. §3.4 의 **lock file** 이 이 저장소에서 충분한 primitive 인가 — 임계 구역이
   덮어야 할 범위에 빠진 것이 있는가.
4. §3.5 의 **명부 출처**(원장)가 순환이 아닌가 — 원장이 곧 승격 대상일 때
   무엇이 근거가 되는가.
5. §2 의 계약 축소(`keys_under`·`delete` 제거)가 옳은가 — 안 부르는 연산을
   계약에서 빼는 원칙이 adapter 작성자에게 위험을 만드는가.
