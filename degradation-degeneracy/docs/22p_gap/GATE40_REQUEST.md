# 40차 게이트 리뷰 요청 — 39차 P0-1 · #9 (반증 11조건)

> 자기 완결 문서다. 숫자는 옮겨 적지 않는다 — 영수증·투영·원장이 정본이다.

```yaml
브랜치:     origin/claude/14-gate-code-review-9qkx05
대상 커밋:   f0aa24f11d7aa0ce4bf339027235a96fa4422aae
직전 대상:   abd5155a…      (39차, 좁은 항목 13 종결 / P0-1·#9 NO-GO)

source_digest:
  39차:  6013cc09cebab2f5
  현재:  db34cc3d3aeca5e2

재현:      git checkout f0aa24f11d7aa0ce4bf339027235a96fa4422aae
           cd degradation-degeneracy
```

## 0. 요청 판정

| 대상 | 요청 |
|---|---|
| 반증 조건 1~11 | **전부 닫았는가** |
| 39차 수용 목록 13항 | 재검 요청하지 않는다 |
| 실제 provider adapter · power-loss fault model | **미구현으로 신고한다** |
| 묶음 9 완료 · gate 배선 · 묶음 2 동결 | **요청하지 않는다** |
| 새 Stage 3 leg · 대규모 재실행 | **요청하지 않는다** |

## 1. 검증 — 방금 실행한 출력

```
$ git rev-parse HEAD
f0aa24f11d7aa0ce4bf339027235a96fa4422aae
$ git status --short
(빈 출력 — `.publish.lock` 은 더 이상 tracked 가 아니다)

$ python3 -m pytest tests/ -q
1108 passed, 1 xfailed in 387.74s (0:06:27)

$ ./scripts/smoke_e2e.sh
✅ pipeline smoke 통과
⚠ 보존 gate 미완료 (계약 v4 묶음 9) — 새 leg 실행 금지.

$ python3 docs/22p_gap/make_receipt.py paired_fixed5_v4 --check
✅ paired_fixed5_v4: core 재생성 바이트 동일 · core_sha 03d6f842b9ca6922

$ python3 wiki/tools/lint.py
RESULT: 0 errors
```

## 2. 이번 라운드에서 배운 것 — fixture 가 축을 가리는 방식이 하나가 아니다

`_semantically_forged` fixture 를 **두 번** 다시 만들었고, 두 번 다 시험이
자기 이름의 축을 실행하지 못하고 있었다.

| 판 | 무엇이 잘못됐나 | 증상 |
|---|---|---|
| 39차 1판 | pin 미잠금 + 가짜 `object_versions` | 어느 축을 위조하든 거절 — 변이 넷 다 초록 |
| 40차 2판 | `retain()` 호출 → **진짜 lease 가 이미 pin** | ambiguity 가 먼저 물음 — 같은 변이가 **여전히** 초록 |
| 3판 | graph 만 pin·잠금, lease 없음 | 후보가 정확히 하나 |

3판에는 **`위조 없으면 통과한다` 를 전제로 명시**했다. 그 전제가 없으면 같은
실수를 또 한다.

## 3. 반증 조건별 대응

| # | 조건 | 대응 | 검사 |
|---|---|---|---|
| 1 | nonexistent/wrong locator → 상태 불변 | `_locator_holds()` 가 **읽기만** 해서 존재·bytes·mode·기한 확인 | `..._forged_candidate_axis_is_refused_without_touching_anything[10축]` — 전후 version census·잠금·pin·store bytes 동일 |
| 2 | store/content 만 Compliance, graph·lease-pin·`lock_mode` 는 Governance → 거부 | membership 을 **lease record 한 곳**에 (`lock_mode`·`store_lock_mode`) | `..._governance_graph_and_lease_pin_are_not_durable` · `..._governance_store_lock_mode_is_not_durable_even_when_consistent` |
| 3 | provider `retain_until` 이 `"zzzz"`·비-문자열 → 거부 | `_horizon_covers()` 가 문법 확인 + tz-aware 파싱 | `..._malformed_provider_horizon_is_not_a_future_proof[4축]` · `..._fake_refuses_a_malformed_retain_until` |
| 4 | `after_lease_pin` 의 **unlocked** exact v1 로 재개 · same-bytes newer Governance 가 안 가림 | `_version_for`(proof) 와 `_repair_source`(수리) 를 **가름**. `_locked_versions(modes=)` | `..._repair_recovers_from_an_unlocked_exact_version` · `..._same_bytes_governance_version_does_not_hide_the_compliance_proof` |
| 5 | `assert_held_for` no-op 객체 · 수동 unlock 된 real lock → 거부 | 구체 타입 + 활성 registry + **kernel lock 재확인** | `..._merely_has_assert_held_for_cannot_publish` · `..._fabricated_lock_instance_is_refused` · `..._manually_unlocked_real_lock_is_refused` |
| 6 | `CURRENT={a}`, roster `{a,b,c}` → complete 도달 | 호환 `.PENDING` 을 base 로 이어받는다 | `..._expanding_a_roster_over_an_active_cohort_reaches_completeness` |
| 7 | 다른 roster 의 pending 재사용 → active 안 움직임 | pending 에 `roster_digest`·`base_generation` 봉인 | `..._pending_from_a_different_roster_is_not_inherited` |
| 8 | `_WARM` alias·`joinpath`·`Path(...)` → 전부 guard 가 깨짐 | **이름을 읽는 것 자체**를 금지. predicate 를 `_warm_offenders()` 로 빼서 직접 시험 | `..._guard_catches_every_way_of_reaching_warm[4형태]` |
| 9 | 취득 뒤 실패 시 fd·flock 해제 · worktree 청결 | 실패 cleanup + **빈 sentinel** + untrack·gitignore | `..._failed_acquire_releases_the_lock[2]` · `..._lock_file_is_a_stable_empty_sentinel` · `..._repository_does_not_track_a_publish_lock` |
| 10 | 원장이 같은 dir·cohort_id 를 두 번 → 거부 | `_ledger_roster()` 가 first match 대신 거부 | `..._ledger_that_declares_one_directory_twice_is_refused` · `..._ledger_declares_each_cohort_and_directory_once` |
| 11 | unknown purpose · `purpose+cohort_id` → 거부 | selector 를 **닫힌 선택**으로 | `..._snapshot_selector_is_a_closed_choice[2]` |

## 4. 스스로 신고 — `.publish.lock` 을 저장소에 커밋했다

39차에 persistent inode 로 바꾸면서 `proj_g2/.publish.lock` 이 **tracked 로
들어갔다.** tracked 이면 worktree 가 더러워지고 checkout·배포가 그 pathname 의
inode 를 갈아 끼울 수 있다 — 39차에 inode 대조를 넣은 **바로 그 조건**이다.

untrack·gitignore 하고 파일을 **빈 sentinel** 로 바꿨다 (PID·token 은 어떤
판정에도 안 쓰였다). 회귀도 뒀다: `..._repository_does_not_track_a_publish_lock`.

## 5. 변이 — 물지 않은 다섯

| 물지 않은 변이 | 진단 | 처리 |
|---|---|---|
| locator 실존·bytes·기한·mode | fixture 가 축을 가림 (§2) | fixture 재작성 ×2 |
| per-version mode membership | lease 쪽 membership 과 서로 가림 | **중복 삭제** |
| 활성 registry | `fd is None` 에 업힘 | **인스턴스 위조** 시험 추가 |
| `_WARM` guard | 현재 코드에 우회 형태가 없음 | predicate 를 빼서 직접 시험 |
| 원장 dir 중복 거부 | 실제 원장이 유일함 | 임시 원장으로 함수를 직접 시험 |

그리고 도달 불가능한 옛 selector(`recover_lease_version` 의 `return` 뒤)와,
구현보다 강하던 `list_versions` 계약 주석을 정리했다.

## 6. 산출물 재생성

| 항 | 이전 → 현재 |
|---|---|
| `source_digest` | `6013cc09cebab2f5` → `db34cc3d3aeca5e2` |
| `compute_sha256` (g2) | `251bfe34f4af65a7` → `28c5151d788f7ec0` |
| `row_projection_py_sha256` (g2) | `6d3a32783203e16e` → `3b54fe35d80f4eb3` |
| receipt `core_sha256` | `0ea53d3b88bf1740…` → `03d6f842b9ca6922…` |

행 바이트는 안 움직였다 (`proj ad598fe77e75afec` · 봉인일치 True).

## 7. 이 환경에서 닫히지 않는 것 — 신고

| 항 | 상태 |
|---|---|
| 실제 object-lock provider adapter | **미구현** |
| power-loss ordering fault model | **미착수** |

## 8. 리뷰 요청 사항

1. §2 의 **fixture 전제 명시**(위조 없으면 통과한다)가 이 종류의 실수를 막는
   옳은 형태인가 — 더 나은 구조가 있는가.
2. 조건 2 의 **membership 을 lease record 한 곳에** 둔 판단 — per-version
   membership 을 중복으로 지운 것이 맞는가.
3. 조건 4 의 **phase 분리**가 충분한가 — proof lookup · repair source 둘로
   갈랐는데, journal verification(exact ID 만 조회)이 별도 축으로 남아야 하는가.
4. 조건 5 의 **kernel lock 재확인**(다른 fd 로 `LOCK_EX|LOCK_NB` 시도)이
   부작용 없는 방법인가.
5. 조건 6·7 의 **pending 승계 규칙**(같은 명부 + 지금의 CURRENT 를 base) 이
   충분한가 — 동시 writer 가 서로 다른 pending 을 남기는 경우 포함.
