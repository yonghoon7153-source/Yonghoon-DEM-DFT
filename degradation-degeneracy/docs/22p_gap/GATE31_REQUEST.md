# 31차 게이트 리뷰 요청 — 30차 P0 셋 · P1 넷 · P2

> 자기 완결 문서다. 숫자는 옮겨 적지 않는다 — 영수증·투영·원장이 정본이다.

```yaml
브랜치:     origin/claude/14-gate-code-review-9qkx05
대상 커밋:   799687b207415e88dc06e3b0b81abd7e288d5ed9
코드 커밋:   f325f511…      # RUN_SCOPE 변경이 들어간 커밋
직전 대상:   c6a65fab…      (30차, NO-GO)

source_digest:
  30차:  35907dff97b67dc5
  현재:  d0a0904b339554cd

재현:      git checkout 799687b207415e88dc06e3b0b81abd7e288d5ed9
           cd degradation-degeneracy
```

## 0. 요청 판정

| 대상 | 요청 |
|---|---|
| P0-1 (마지막 창 · retention primitive) | 방향이 맞는가 — §2 는 **부분 종결**을 주장한다 |
| P0-2 (backend 필수 · store identity) | 닫혔는가 |
| P0-3 (fsync fail-closed · parent edge · crash drill) | 닫혔는가 |
| P1 1~4 | 어디까지인가 |
| P2 (세대 chain) | **부분** — 닫지 못한 축을 §6 에 적었다 |
| 「최소 증거」 1~8 | 대응표 §7 |
| 9 (immutable generation directory) | **미착수로 신고한다** |
| 묶음 9 완료 · gate 배선 · 묶음 2 동결 | **요청하지 않는다** |
| 새 Stage 3 leg · 대규모 재실행 | **요청하지 않는다** |

## 1. 검증 — 방금 실행한 출력

```
$ git rev-parse HEAD
799687b207415e88dc06e3b0b81abd7e288d5ed9
$ git status --short
(빈 출력)

$ python3 -m pytest tests/ -q
925 passed, 1 xfailed in 366.90s (0:06:06)

$ ./scripts/smoke_e2e.sh          # 2c949a20 (clean) 에서
✅ pipeline smoke 통과
⚠ 보존 gate 미완료 (계약 v4 묶음 9) — 새 leg 실행 금지.

$ python3 -c "…source_digest()"
d0a0904b339554cd

$ python3 docs/22p_gap/make_receipt.py paired_fixed5_v4 --check
✅ paired_fixed5_v4: core 재생성 바이트 동일 · core_sha 43386a98163b3781

$ python3 wiki/tools/lint.py
RESULT: 0 errors
```

## 2. P0-1 — 창을 하나 닫고, 남은 창은 **타입으로** 신고한다

리뷰가 지목한 창을 재현했다. 29차의 `_DropAfterRead` 로는 안 잡힌다는 지적도
맞았다 — 그것은 `read_back()` 의 `objects/` 만 건드린다. member pin 은 전수
읽기에서 **딱 한 번** 읽히므로 그것을 겨냥한 backend 를 새로 만들었다
(`_DropPinAfterRead`). 회귀:
`test_registration_fails_when_pins_vanish_during_the_final_sweep`.

요구한 세 primitive 를 만들었다:

```text
retain(graph, min_retention_days) -> lease
verify_retention(lease, actual_backend)
retrieve_retained(lease, digest)
```

lease 는 그 자체가 CAS object 이고 pin 된다 — graph 의 일부라서 위조하면
graph digest 가 어긋난다. 검증의 **마지막 단계가 바이트 읽기가 아니라 lease
상태 확인**이므로 전수 읽기 도중의 삭제가 잡힌다.

### 2.1 그 뒤의 창은 닫지 않았다 — 이유와 대안

local filesystem 에서 마지막 검사와 반환 사이는 닫을 수 없다. 이 실행 환경은
**uid 0** 이라 directory mode bit 도 잠금이 아니다 (실측: `chmod 0o500` 뒤에도
unlink 성공). 검사를 하나 더 두면 창이 한 칸 뒤로 갈 뿐이고 그것이 28·29·30차가
같은 자리에 선 이유다.

그래서 검사를 늘리는 대신 **`ok=True` 의 뜻을 좁혔다**:

| lease 의 `enforcement` | 뜻 |
|---|---|
| `advisory_local` | pin 은 붙들지만 강제하지 못한다. local 이 여기다 |
| `object_lock` | backend 가 강제한다 |

`run_transaction` 은 `durable: False` 를 함께 돌려주고
`assert_durable_retention()` 은 `object_lock` 이 아니면 거부한다. 비싼 본
실행을 승인하는 gate 가 그 자리다.

**이 판단을 리뷰가 확인해 주기 바란다** — "local 에서 durable retention 을
주장하지 않는다" 를 종결로 볼지, 아니면 object-lock backend 구현까지를
P0-1 의 조건으로 볼지.

## 3. P0-2 — backend 필수 · store identity

| 축 | 반례 | 지금 |
|---|---|---|
| backend 없는 판정 | 정상 등록 뒤 `pins/`·`objects/` 를 다 지워도 참 | `is_registered` 가 backend **필수**. 주장 확인은 `has_registration_journal()` |
| 상대 root · cwd 변경 | 다른 store 를 가리키며 URI 가 같다 | URI 를 절대 경로로 정규화 |
| store 재생성 | 같은 경로 = 같은 store 로 봤다 | 생성 시각에 고정되는 store UUID 를 receipt·lease 에 결속 |

세 축을 **각각** 물리는 시험을 따로 뒀다. 한 시험에 몰면 한 축을 지워도
초록이라는 것을 변이로 확인했고, 그래서 URI 축 시험은 `store.json` 째 복사해
UUID 축을 일부러 무력화한다.

## 4. P0-3 — fsync 와 crash drill

| 무엇 | 지금 |
|---|---|
| 실패를 `False` 로 돌리고 무시 | `_fsync_dir_strict()` 가 오류로 전파 |
| `objects/<prefix>`·`pins/<leg>` 자기만 flush | `_mkdir_durable()` 이 새로 만든 모든 층의 **부모 edge** 를 flush |
| 캐시 키가 `resolve().anchor` | `st_dev` |
| crash/reopen drill 부재 | 자식 프로세스를 `os._exit(9)` 로 죽이고 부모가 재개방 |

drill 은 두 지점에서 죽인다 (`after_pin`, `after_publish`) 그리고
`journal visible ⇒ full graph retrievable` 을 확인한다. commit 순서를
뒤집는 변이로 물리는 것을 봤다.

## 5. P1 넷

| # | 고침 | 대표 회귀 |
|---|---|---|
| 1 | journal 닫힌 키 집합 · unique 정렬 64-hex · **유도한 graph 로** 재계산한 `pin_set_digest` · journal 없으면 fail-closed · 등록 전 검증은 `verify_graph_before_registration()` 로 이름 분리 | `..._journal_is_an_exact_typed_graph` (duplicate·surplus·거짓 digest·역순·lease 누락 다섯) |
| 2 | `check_envelope()` 값 domain · hook 결과 exact bool + 상호 모순 · output role 별 tagged union · manifest path domain | `..._value_domains_not_just_keys` (16) · `..._validator_hook_result_has_a_domain` (7) · `..._tagged_union_not_a_bag_of_nonempty` (10) · `..._member_paths_have_a_domain_at_seal_time` (8) |
| 3 | `min_retention_days` 를 envelope 에 봉인 · lease 검증이 **지금 backend** 재조회 | `..._lease_below_the_policy_floor_is_refused` |
| 4 | `design_binding()` 이 봉인 design 에서 chain 을 유도, `candidate_id` 는 그것만 받는다 | `..._cannot_name_an_objective_from_a_free_argument` · `..._bank_from_another_design_is_refused` |

P1-2 에서 하나 더 나왔다 — `envelope()` 이 `int(...)` 로 강제 변환해 `True` 가
`1` 이 되어 domain 검사에 도달하지 못했다. 변환을 없앴다.

P1-4 의 golden vector 는 **바이트 동일**이다. ID domain 은 안 움직였고 움직인
것은 plan 의 권위 위치다.

## 6. P2 — 닫은 것과 닫지 못한 것

닫은 것: 투영의 `manifest_sha256` 을 봉인 manifest **바이트에서 재해시** ·
투영의 `source_digest` 를 그 manifest 의 `run_spec.source_digest` 와 대조 ·
cohort 가 갈리면 실패하고 active 우선 · 세대표 **값**에 근거표
(`source_digest_evidence`) · `STAGE3_CONTRACT.md` §8 에 leg-level 과 per-claim
두 층 명시.

**닫지 못한 것**: 실행이 남긴 어떤 산출물에도 "protocol generation" 필드가
없다 — 그 이름은 이 원장의 분류다. 그러므로 `digest → generation` 화살표는
도출이 아니라 **선언**이고, 할 수 있는 것은 봉인물이 지지하는 digest 에 그
선언을 묶는 것까지다. 묶음 9 등록이 생기는 순간 registered receipt 의
`planned_envelope` 이 정본이 되도록 fail-closed 검사를 미리 켜 뒀고, 지금은
그 검사가 "등록된 다리 없음" 을 고정하고 있다
(`test_a_registered_leg_binds_its_generation_to_the_receipt`).

리뷰가 요구한 chain 중 `restored manifest/run_spec` 축은 **원자료가 남은 한
다리에서만** 가능하다. 나머지 일곱은 영구히 불가능하며, 그 사실 자체를
`test_a_projection_manifest_digest_is_rehashed_from_actual_bytes` 가
`anchored == ["paired_fixed5_v4"]` 로 고정한다.

## 7. 「최소 증거」 대응표

| 항 | 요구 | 상태 |
|---|---|---|
| 1 | read-then-delete backend 에서 `_commit_registration` 이 성공하지 않을 것. 검사 추가가 아니라 retention primitive/lease | **구현 종결 · 판단 요청** — §2.1 |
| 2 | backend 없는 `is_registered` 제거 · 상대 root/cwd · store ID mismatch | 닫음 (§3, 축별 시험 셋) |
| 3 | journal exact schema · 재계산 `pin_set_digest` · missing journal fail-closed | 닫음 (§5 #1) |
| 4 | fsync 실패 전파 · 모든 새 directory 의 parent edge · crash/reopen | 닫음 (§4) |
| 5 | planned/validation/output/manifest path 를 생성·복구가 같은 validator 로 | 닫음 (§5 #2) |
| 6 | 숫자가 아니라 actual backend 의 retention 재조회 · 원래 하한을 sealed receipt 에서 복원 | 닫음 (§5 #3) |
| 7 | warm objective 를 sealed design hash chain 에 결속 | 닫음 (§5 #4) |
| 8 | registered receipt 의 `{source_digest, protocol_generation}` 을 manifest/projection 과 결속 | **부분** — §6 |
| 9 | immutable cohort generation + single `CURRENT` + crash/reopen | **미착수** |

## 8. 변이로 확인했고, 물지 않은 것 셋

이번에 넣은 규칙을 전부 지워 봤다. **물지 않은 변이가 셋** 있었고 전부 시험이
다른 축에 업혀 통과하던 자리였다:

| 물지 않은 변이 | 왜 | 처리 |
|---|---|---|
| URI 정규화 삭제 | 시험이 lease 의 store UUID 축으로 통과 | UUID 축을 무력화한 시험으로 고침 |
| receipt 의 `backend_store_id` 결속 삭제 | end-to-end 로는 lease 검사가 먼저 걸린다 | validator 직접 시험을 따로 |
| journal 자기 `pin_set_digest` 재계산 삭제 | 강한 쪽(유도 graph 로 재계산)이 이미 있다 | 실제 중복이라 **약한 쪽을 지웠다** |

## 9. 자체 발견 둘

**lease 가 재실행마다 늘었다.** `retain_until_utc` 때문에 재실행이 초 경계를
넘으면 lease 가 하나 더 pin 됐다. 전체 시험 열두 번 중 두 번 빨갰고 원인이
시계라 재현이 확률적이었다. 시계를 강제로 전진시키는 결정적 회귀로 고정하고
`retain()` 을 멱등으로 만들었다.

**요청문 lint 가 archive 를 거짓으로 만들었다.** 모든 요청문의 인용을
**오늘의** 영수증과 대조하고 있었다. 요청문은 그 회차의 기록이므로 다음 회차에
영수증이 바뀌면 지나간 요청문이 전부 거짓이 된다. **그 요청문이 이름한 대상
커밋의 영수증**과 대조하도록 바꿨다 — 그것이 자기완결의 뜻이기도 하다.

## 10. 산출물

영수증을 clean tree 에서 다시 만들었다 (`validator_tree_dirty: false`,
commit `f325f511`). 원장 pin:

```text
verification_receipt_core_sha256  2c36f26a… → 43386a98…
validator_identity.source_digest  35907dff97b67dc5 → d0a0904b339554cd
```

g2 투영은 재생성해도 **바이트 동일**이다 — 이번 라운드는 `row_projection.py`
와 `ANALYSIS_SPEC` 을 건드리지 않았다. `g1_2026_08_20` 은 frozen, 손대지 않았다.
