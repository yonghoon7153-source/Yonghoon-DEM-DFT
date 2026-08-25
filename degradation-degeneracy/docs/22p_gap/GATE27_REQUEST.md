# 27차 게이트 리뷰 요청 — 26차 P0 둘 + P1 여덟 + P2 둘

> 자기 완결 문서다. 옛 왕복은 `GATE24_REQUEST.md`·`GATE26_REQUEST.md` 와
> 원장 §29~§35 에 있다. 이 문서는 숫자를 옮겨 적지 않는다 — 영수증·투영·
> 원장이 정본이고, 두 곳에 두면 26차 P2-12 처럼 한쪽이 낡는다.

```yaml
브랜치:     origin/claude/14-gate-code-review-9qkx05
대상 커밋:   92ba0b109d105d636bc0e181da1a3cae89d12e7e
코드 커밋:   f8ee62bfb7e2…      # RUN_SCOPE 변경이 들어간 커밋
직전 대상:   e1ec91d11222a0d0d756c523fd4469c984653b4e   (26차, NO-GO)

source_digest:
  26차:  0b9fb0d4519d34ae
  현재:  d3b1644f7ebe5bda      # 묶음 9 재작성 · 묶음 2 typed payload

재현:      git checkout 92ba0b109d105d636bc0e181da1a3cae89d12e7e
           cd degradation-degeneracy
```

## 0. 요청 판정

| 대상 | 요청 |
|---|---|
| 26차 P0 둘 (CAS 복원 · 영수증 저장) | 닫혔는가 |
| P1 3~10 · P2 11~12 | 어디까지인가 |
| 「다음 회신에 필요한 최소 증거」 12항목 | 대응표 §3 |
| 묶음 9 **완료 선언** · gate 배선 | **요청하지 않는다** — §5 |
| 묶음 2 **동결** | **요청하지 않는다** — §6 의 둘이 남았다 |
| 새 Stage 3 leg · 대규모 재실행 | **요청하지 않는다** |

## 1. 검증 — 방금 실행한 출력

```
$ git rev-parse HEAD
92ba0b109d105d636bc0e181da1a3cae89d12e7e
$ git status --short
(빈 출력)

$ python3 -m pytest tests/ -q
771 passed, 1 xfailed in 292.16s (0:04:52)

$ ./scripts/smoke_e2e.sh          # f8ee62bf (clean) 에서
✅ pipeline smoke 통과
⚠ 보존 gate 미완료 (계약 v4 묶음 9) — 새 leg 실행 금지.

$ python3 -c "…source_digest()"
d3b1644f7ebe5bda

$ python3 docs/22p_gap/make_receipt.py paired_fixed5_v4 --check
✅ paired_fixed5_v4: core 재생성 바이트 동일

$ python3 wiki/tools/lint.py
RESULT: 0 errors
```

## 2. 리뷰가 옳았다 — 내가 "확인했다" 고 적은 둘이 false-green 이었다

### 2.1 복원이 CAS 를 전혀 안 봤다 (P0-1)

member 와 manifest 를 넣고 `read_back()` 까지 했지만 **되읽은 bytes 를 해시만
확인하고 버렸다.** 실제 복원은 `hooks.restore(man, run_dir, root)` — 보존 전
원본이다. read-back 직후 CAS 를 비워도 publish 까지 성공한다는 리뷰의 반례를
그대로 재현했다.

고친 방식은 **구조**다:

```python
restore_from_cas(backend, manifest_digest, root)   # 원본 경로를 받지 않는다
```

인자에 없으면 재발이 불가능하다. 증명 장치도 넣었다 —
`run_transaction(..., drop_source_after_seal=True)` 는 업로드 직후 원본을
지운다. 그러고도 끝까지 가면 복원이 backend 에서 나온 것이 확실하다.

### 2.2 영수증이 회수 불가능했다 (P0-2)

메모리 dict 로 만들고 digest 만 index 에 적었다. 등록은 단순 `return` 이라
프로세스가 죽으면 사라졌고, "재시도" 는 계산 전체를 다시 도는 것이었다.

→ receipt canonical bytes 를 CAS 에 넣고 되읽어 대조한다. index 가 회수 가능한
`receipt_object` 를 가리킨다. 등록은 `O_EXCL` journal 이다. crash 뒤에는
`finalize_only(leg_id, backend, index, hooks)` 가 **원본 없이** CAS 만으로
닫는다.

**불변식도 정정했다.** "어느 단계에서 멈추든 index 가 깨끗하다" 는 틀렸다:

| 언제 실패 | 남는 상태 | 닫는 법 |
|---|---|---|
| publish **전** | 항목 없음 | 처음부터 |
| publish **후** | durable, **미등록** | `finalize_only` (재계산 없이) |

## 3. 「최소 증거」 12항목

| # | 요구 | 회귀 |
|---|---|---|
| 1 | 원본 제거 뒤 **CAS 만으로** restore→validate→rescore | `test_restore_reads_the_backend_not_the_original_run_dir` (`drop_source_after_seal`) |
| 2 | CAS member/manifest/receipt 훼손 시 publish 전 실패 | `test_deleting_cas_objects_fails_before_publish[member\|manifest\|all]` · `test_mutating_a_cas_object_fails_before_publish` |
| 3 | receipt CAS digest/read-back + finalize-only resume | `test_the_receipt_itself_is_stored_and_retrievable` · `test_crash_after_publish_resumes_with_finalize_only` · `test_registration_is_a_durable_state_change_not_a_return` |
| 4 | concurrent different/same-leg publish race | `test_concurrent_publish_of_different_legs_loses_nothing` (16 thread) · `test_concurrent_publish_of_the_same_leg_admits_exactly_one` |
| 5 | missing run_spec · missing semantic · malformed output | `test_missing_run_spec_is_fail_closed` · `test_expected_semantic_is_mandatory` · `test_malformed_output_manifest_is_refused[4종]` |
| 6 | `make_receipt` 가 `repo_root=<restored root>` | `test_receipt_validation_actually_reads_the_restored_root` (복원 root 의 봉인 입력을 지우면 실패해야 한다) · `test_make_receipt_binds_the_validator_to_the_restored_root` |
| 7 | rescored vs sealed semantic equality | `test_receipt_compares_the_rescored_summary_against_the_sealed_one` — 영수증이 `outputs_agree` 를 값으로 적고, 갈리면 **생성이 멈춘다** |
| 8 | label 을 hash 밖으로 · `PlannedLeg` 가 design digest | `test_a_design_alias_change_does_not_move_any_id` · `PlannedLeg.__post_init__` 이 64-hex 를 강제 |
| 9 | typed payload golden + `src/grid` linkage | `test_candidate_payloads_follow_a_closed_per_source_schema` · `test_grid_conditions_bridge_to_wire_coordinates` |
| 10 | cohort-generic rehash · frozen 쓰기 거부 · schema bump | `test_warm_probe_row_projections_are_committed_and_self_consistent` (cohort 순회) · `test_the_projection_builder_refuses_to_write_into_a_frozen_cohort` · `test_evidence_cohorts_and_the_cohort_registry_agree_both_ways` |
| 11 | committed 요청문 placeholder 제거 + identity test | `test_committed_gate_requests_are_self_contained` — placeholder·없는 커밋·낡은 영수증 sha 를 잡는다 (실제로 GATE26 의 낡은 core sha 를 잡았다) |
| 12 | 새 Stage 3 leg 실행 금지 유지 | §0 · smoke 출력 |

## 4. P1-6 의 원인 — 왜 두 digest 가 영원히 달랐나

`summarize()` 는 `multistart`·`multistart_random_only` 를 만들지 않는다.
`run_scoring` 이 restart trace 에서 따로 붙인다 (22차 발견 5 가 이미 지적한
것이다). `make_receipt` 가 `row_projection._add_multistart_blocks` 를 쓰지
않았으므로 재채점본에는 그 두 블록이 통째로 없었고, 봉인본과 **영원히 다를
수밖에** 없었다. 나란히 적어 놓고 비교를 안 했으므로 아무도 몰랐다.

정규 view (`SEMANTIC_SKIP` = 재채점이 만들 수 없는 실행 메타) 를 정의하고
equality 를 강제했다. 두 digest 가 이제 같고, 갈리면 `build()` 가 멈춘다 —
`false` 를 적어 두고 통과시키면 "대조했다" 가 다시 거짓이 된다.

## 5. 묶음 9 를 완료로 선언하지 않는 이유 셋 (변함 없음)

1. **`run.sh`·smoke 의 필수 gate 로 배선되지 않았다.** Q1 답(b')을 받아들이되
   배선은 다음 라운드다 — §7 Q1.
2. **실제 운영 backend canary 가 없다.** local `file+cas://` 로 트랜잭션
   **의미**만 검증했다.
3. **`planned_leg_index` 가 실제 leg 원장과 결속되지 않았다** — 묶음 1·6 필요.

## 6. 묶음 2 동결을 요청하지 않는 이유 둘

1. `src/grid.Condition` 과의 다리는 놓았지만 **실제 v6 격자 실행**과의
   end-to-end 결속은 없다. `build_conditions` 가 만든 축 전체를 훑어 왕복
   실패가 없는지 확인한 것이 아니라, 대표 조건 3개만 golden 에 고정했다.
2. Unicode 정규화 정책을 wire 에 적었지만(`nfc_utf8_no_escape`) 실측 회귀가
   없다. 지금 좌표·type 은 ASCII 라 트리거되지 않는다.

## 7. 질문

**Q1 — 배선 시점.** Q1 답의 (b') lifecycle wrapper 를 받아들인다. 다만 그것을
지금 만들면 `run.sh` 와 `src/fitting.py` 진입점을 바꾸게 되고, 묶음 1·6 이
아직 없어 `planned_leg_index` key 가 임시가 된다. 순서를 이렇게 이해했다:

```
묶음 1 최소 lifecycle + 묶음 2 동결
→ 묶음 6 index migration
→ 그 다음에 (b') 배선
```

맞는가? 아니면 배선을 먼저 하고 planned index 를 나중에 갈아끼우는 편이
안전한가? (전자면 그동안 `results/` 는 계속 gate 밖이다.)

**Q2 — `quarantined` 상태의 소비자.** (b') 는 보존 실패 시 계산 bytes 를
`computed_unpreserved` 로 남기고 downstream reader 가 기본 거부하게 하라고
했다. 지금 downstream 은 `src/scoring.py`·`row_projection.py`·
`make_receipt.py` 셋이다. 거부를 (a) 각 reader 가 상태 파일을 확인하는 방식,
(b) `results/` 대신 `quarantine/` 로 경로를 옮겨 reader 가 애초에 못 찾게 하는
방식 중 어느 쪽으로 원하는가? (b) 가 우회하기 어렵다고 보는데, 12시간 계산의
경로가 실패로 바뀌는 것이라 되돌리기 절차가 필요하다.

**Q3 — analyzer canary registry 의 위치.** Q3 답대로 synthetic canary 를
`LEG_PRESERVATION` 의 과학 cohort 와 섞지 않고 별도 `analyzer_canary` 로
두려 한다. 그 canary 는 `src/` 실행이 필요 없는 순수 fixture 인데,
(a) `tests/fixtures/` 에 두고 회귀에서만 쓰는 것과
(b) `docs/22p_gap/canary/` 에 두고 투영 생성기를 실제로 돌리는 것 중
어느 쪽이 "계산 경로 변화 경보기" 로 유효한가? (b) 여야 `--out` 경로와
staging·승격까지 지나간다고 보는데, 그러면 canary 도 cohort 를 갖게 된다.
