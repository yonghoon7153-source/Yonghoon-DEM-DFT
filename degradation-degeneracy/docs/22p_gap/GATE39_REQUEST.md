# 39차 게이트 리뷰 요청 — 38차 P0-1 · #9 (반증 13조건)

> 자기 완결 문서다. 숫자는 옮겨 적지 않는다 — 영수증·투영·원장이 정본이다.

```yaml
브랜치:     origin/claude/14-gate-code-review-9qkx05
대상 커밋:   abd5155ad7d69f43aee64ed3c358519b5781ef6c
직전 대상:   e4f51673…      (38차, 좁은 항목 14 종결 / P0-1·#9 NO-GO)

source_digest:
  38차:  59ba034148cf8a60
  현재:  6013cc09cebab2f5

재현:      git checkout abd5155ad7d69f43aee64ed3c358519b5781ef6c
           cd degradation-degeneracy
```

## 0. 요청 판정

| 대상 | 요청 |
|---|---|
| 반증 조건 1~13 | **전부 닫았는가** |
| P0-3 · P2 · 만료 갱신 제거 | 종결 유지 — 재검 요청하지 않는다 |
| 실제 provider adapter · power-loss fault model | **미구현으로 신고한다** |
| 묶음 9 완료 · gate 배선 · 묶음 2 동결 | **요청하지 않는다** |
| 새 Stage 3 leg · 대규모 재실행 | **요청하지 않는다** |

## 1. 검증 — 방금 실행한 출력

```
$ git rev-parse HEAD
abd5155ad7d69f43aee64ed3c358519b5781ef6c
$ git status --short
(빈 출력)

$ python3 -m pytest tests/ -q
1075 passed, 1 xfailed in 567.49s (0:09:27)

$ ./scripts/smoke_e2e.sh
✅ pipeline smoke 통과
⚠ 보존 gate 미완료 (계약 v4 묶음 9) — 새 leg 실행 금지.

$ python3 docs/22p_gap/make_receipt.py paired_fixed5_v4 --check
✅ paired_fixed5_v4: core 재생성 바이트 동일 · core_sha 0ea53d3b88bf1740

$ python3 wiki/tools/lint.py
RESULT: 0 errors
```

## 2. 리뷰의 결론 한 줄이 이번 라운드의 전부다

> "시험의 이름이 실제 predicate 보다 강하다."

모든 수정의 규칙을 하나로 삼았다 — **predicate 를 이름만큼 강하게 만들거나,
이름을 바꾼다.**

## 3. 반증 조건별 대응

| # | 조건 | 대응 | 검사 |
|---|---|---|---|
| 1 | exact key 유지하며 5축 forged → 상태 불변 | `_matches_lease()` 가 `store_version_id`·`store_lock_mode`·`lock_mode`·`object_versions`·timestamp **문법**까지 본다. `_is_utc_stamp()` 추가 | `..._semantically_forged_candidate_changes_nothing_before_refusal[6축]` — 전후 **version census · pin 집합 · store bytes** 동일 확인 |
| 2 | Governance-only store + Compliance default → 거부 | `store_id` 의 `_read_protected()` fallback 을 막았다 | `..._governance_only_store_cannot_reach_durable` |
| 3 | `store_version_id == ""` · `lease_content_version == ""` → 거부 | object-lock 이면 **둘 다 필수**. journal parser 는 두 locator type 을 본다 | `..._without_a_store_version_proof_is_refused` · `..._without_a_content_proof_is_refused` · `..._locator_that_is_not_a_string[4종]` |
| 4 | store version 기한이 graph 보다 짧으면 거부 | `retain_until >= lease.retain_until_utc` | `..._store_version_that_expires_before_the_graph_is_refused` |
| 5 | content version mode 만 Governance → 거부 | `cst.mode in DURABLE_MODES` | `..._governance_locked_lease_content_is_not_a_compliance_proof` |
| 6 | journal 전 crash + wrong-bytes newer version → 같은 lease 로 재개 | `_version_for()` 하나로 pin·content·수리가 **바이트 대조** | `..._hostile_newer_lease_pin_version_does_not_block_resume` |
| 7 | Compliance version 을 global mode flip 뒤 bypass delete → 거부 | fake `delete()` 가 **봉인 mode** 와 **그 version 의 기한**을 본다 | `..._refuses_a_bypass_delete_of_a_compliance_version` + 반대 축 `..._lets_an_expired_lock_be_deleted` |
| 8 | forged `held()` · `outA` 실제 lock → `outB` 못 움직임 | `assert_held_for(out)` 이 대상·process·fd inode 대조 | `..._forged_held_object_cannot_publish` · `..._lock_for_another_cohort_cannot_publish_here` |
| 9 | inode/pathname 교체 후 old owner release | **파일을 안 지운다** (persistent inode) + inode 대조 | `..._lock_path_survives_release...` · `..._replaced_lock_pathname_invalidates_the_capability` |
| 10 | 원장 `{a}` 인데 caller 가 `{a,b}` 신고 → 거부 | publisher 가 `out` 을 원장 cohort 로 resolve 해 **직접 읽고** 신고와 대조 | `..._reads_the_roster_from_the_ledger_not_the_caller` |
| 11 | bootstrap 중 crash → active 없음 or 이전 complete | 명부가 찰 때까지 비활성 `.PENDING` 에만 적는다 | `..._bootstrap_partial_cohort_never_becomes_the_active_pointer` |
| 12 | g1/g2 bytes 다름 → active 는 g2, historical 은 명시, 무목적은 거부 | `_snapshot_for_leg(purpose=/cohort_id=)`, 아니면 **ambiguity 거부** | `..._leg_in_two_cohorts_refuses_to_be_resolved_by_order` · `..._active_purpose_reads_the_active_cohort_not_the_frozen_one` |
| 13 | line 1260 을 옛 코드로 되돌리면 guard 가 빨개짐 | guard 를 상수 접속사에서 **경로 조립 연산 금지**로 | 실제 source replacement 로 확인 (빨개짐) |

## 4. 스스로 발견한 것 — 검증이 반례를 고쳐 놓고 있었다

조건 1 을 고치려고 `inspect_store_id()` 를 만들자 예상 못 한 것이 드러났다:
`verify_retention()` 도 `store_id` 를 부르고 있어서, **담보 해제(조건 4 계열)와
기한 단축 반례가 둘 다 self-healing 으로 초록**이었다. 검증이 스스로 수리해
놓고 통과시킨 것이다.

거기도 inspect 로 바꾸자 두 반례가 비로소 보였다. 원칙은 조건 1 과 같다 —
**검증은 수리하지 않는다.**

조건 12 도 예상보다 나빴다. `paired_fixed5_v4` 는 g1·g2 둘 다에 있고 원장이
g1 을 먼저 적으므로, 그 helper 는 **언제나 frozen g1** 이었다. 다섯 소비자를
옮긴 것이 "active 를 읽는다" 가 아니라 g1 선택의 공통화였다는 리뷰 지적이
정확했고, 30차 P2 의 `_pick_sealed_digest()` 와 같은 실수였다.

## 5. 변이 — 여섯이 물지 않았다

| 물지 않은 변이 | 진단 | 처리 |
|---|---|---|
| `object_versions` 값 검사 | key set 검사에 업혔다 | fixture 를 갈랐다 |
| validator 의 mutating `store_id` | record 가 이미 있으면 관측 불가 | record 없는 상태로 시험 |
| store proof 필수화 | mode 검사가 먼저 물었다 | 한 축만 비우게 수정 |
| journal locator type | 빈 문자열은 `str` 이라 안 걸린다 | 비-문자열 4종 parametrize |
| `_version_for` (anchor 2×) | 같은 loop 이 **세 곳**에 있었다 | **하나로 합쳤다** |
| 38차 `..._old_owner_cannot_delete...` | 삭제를 안 하게 되어 공허참 | **시험을 지웠다** |

## 6. 산출물 재생성

| 항 | 이전 → 현재 |
|---|---|
| `source_digest` | `59ba034148cf8a60` → `6013cc09cebab2f5` |
| `compute_sha256` (g2) | `f4602a9b7aae8e1b` → `251bfe34f4af65a7` |
| `row_projection_py_sha256` (g2) | `c6db39d9319a4f86` → `6d3a32783203e16e` |
| receipt `core_sha256` | `0a6cb73b1d979d01…` → `0ea53d3b88bf1740…` |

행 바이트는 안 움직였다 (`proj ad598fe77e75afec` · 봉인일치 True).

## 7. 이 환경에서 닫히지 않는 것 — 신고

| 항 | 상태 |
|---|---|
| 실제 object-lock provider adapter | **미구현** — 계약 8연산·per-version mode·Compliance 단조·delete marker 는 고정 |
| power-loss ordering fault model | **미착수** — fault-injecting filesystem 필요 |

## 8. 리뷰 요청 사항

1. §4 의 **"검증은 수리하지 않는다"** 가 옳은 원칙인가 — `store_id` 의 자동
   수리를 검증 경로에서 뗀 것이 다른 곳(예: 정상 `retain()`)의 복구를 약화시키는가.
2. 조건 11 의 **`.PENDING` 분리**가 옳은 형태인가 — bootstrap 중 `.PENDING` 이
   가리키는 generation 이 immutable 하게 굳어 있다는 점, 그리고 그것을 base 로
   삼는 다음 publisher 가 CAS 대상을 `.PENDING` 으로 바꾸는 것 포함.
3. 조건 12 의 **세 갈래 선택**(active / cohort 명시 / 거부)에 빠진 목적이
   있는가 — 특히 "두 cohort 를 비교하는" 소비자.
4. 조건 9 의 **파일을 안 지우는 release** 가 옳은가 — lock 파일이 영구히
   남는 것의 부작용.
5. §5 에서 `_version_for` 를 하나로 합친 판단 — pin·content·수리가 같은
   규칙을 써야 하는 것이 맞는가, 아니면 축마다 달라야 하는가.
