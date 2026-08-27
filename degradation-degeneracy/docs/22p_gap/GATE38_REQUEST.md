# 38차 게이트 리뷰 요청 — 37차 P0-1 · #9

> 자기 완결 문서다. 숫자는 옮겨 적지 않는다 — 영수증·투영·원장이 정본이다.

```yaml
브랜치:     origin/claude/14-gate-code-review-9qkx05
대상 커밋:   e4f516736f0b4fd0b78b1ac05d4b0f0d5f7d7e40
직전 대상:   988a5216…      (37차, 좁은 항목 11 종결 / P0-1·#9 NO-GO)

source_digest:
  37차:  ccb3e2ad0f6145c0
  현재:  59ba034148cf8a60

재현:      git checkout e4f516736f0b4fd0b78b1ac05d4b0f0d5f7d7e40
           cd degradation-degeneracy
```

## 0. 요청 판정

| 대상 | 요청 |
|---|---|
| 발견 1 (만료 갱신) | **기능을 뺐다** — 그 판단이 옳은가 |
| 발견 2 (candidate `None` 구멍 · validate-before-mutate) | 닫혔는가 |
| 발견 3·4 (store version proof · lifecycle exact version · fake 의미) | 닫혔는가 |
| #9-1 (stale lock ownership · fencing · publisher boundary) | 닫혔는가 |
| #9-2 (실제 reader · snapshot) | 닫혔는가 |
| #9-3 (roster authority) | 닫혔는가 |
| P0-3 · P2 | 33·35차 종결 — 재검 요청하지 않는다 |
| 실제 provider adapter · power-loss fault model · **lease 갱신** | **미구현으로 신고한다** |
| 묶음 9 완료 · gate 배선 · 묶음 2 동결 | **요청하지 않는다** |
| 새 Stage 3 leg · 대규모 재실행 | **요청하지 않는다** |

## 1. 검증 — 방금 실행한 출력

```
$ git rev-parse HEAD
e4f516736f0b4fd0b78b1ac05d4b0f0d5f7d7e40
$ git status --short
(빈 출력)

$ python3 -m pytest tests/ -q
1049 passed, 1 xfailed in 340.84s (0:05:40)

$ ./scripts/smoke_e2e.sh
✅ pipeline smoke 통과
⚠ 보존 gate 미완료 (계약 v4 묶음 9) — 새 leg 실행 금지.

$ python3 docs/22p_gap/make_receipt.py paired_fixed5_v4 --check
✅ paired_fixed5_v4: core 재생성 바이트 동일 · core_sha 0a6cb73b1d979d01

$ python3 wiki/tools/lint.py
RESULT: 0 errors
```

## 2. 발견 1 — 기능을 **뺐다**. 이 라운드에서 가장 중요한 항목이다

리뷰가 맞다. 그리고 지적보다 나쁘다: production 재개 경로(`finalize_only()`)로는
journal 의 만료 lease 검증에서 먼저 죽어 **갱신에 도달조차 못 했다.**

36차에 붙인 갱신 시험은 `retain()` 반환값의 digest 와 날짜만 봤다. 이 저장소
규칙("새 테스트가 처음부터 통과하면 fixture 가 진실을 가리고 있었다")에 정확히
걸리는 경우였고, 내가 그 확인을 안 했다.

리뷰가 준 세 선택지 중 셋째를 택했다:

| 선택지 | 판단 |
|---|---|
| active lease generation/pointer | 설계 항목. 365일 지평에서 실현될 일이 없는데 표면만 늘린다 |
| exact-version retirement primitive | `delete` 를 계약에 다시 들여야 한다 — 37차에 뺀 근거를 뒤집는다 |
| **미지원 선언 + fail-closed** | **택함.** 동작한 적 없는 기능을 빼는 것이다 |

거부는 **이유를 말한다** — "historical WORM pin 을 퇴역시킬 수 없어 새 lease 를
만들어도 exact pin set 이 깨진다. 사람이 판단해 새 leg 로 다시 담보하라."

회귀 둘: `..._is_refused_and_says_why` (재진입점) ·
`..._fails_closed_in_the_production_path` (실제 `finalize_only()`).

## 3. 발견별 대응

### 3.1 발견 2 — `None` 구멍과 mutation 순서

| 축 | 대응 | 검사 |
|---|---|---|
| 정책 강화가 두 번째 lease 를 만듦 | metadata mismatch → **fail-closed** | `test_a_stronger_policy_request_does_not_mint_a_second_lease` |
| 검증보다 앞선 WORM mutation | 순수 validator 가 **전부** 먼저 | `test_a_forged_candidate_is_refused_before_anything_is_made_worm` (version census 로 "아무것도 안 바꿨다" 확인) |
| orphan 입양이 느슨함 | 같은 validator 를 지난다 | `..._from_a_foreign_store_is_not_adopted` · `..._with_a_forged_pin_set_digest_is_not_adopted` |

`_matches_lease()` 가 보는 것: exact key set · schema · leg · graph ·
정책일수 · `pin_set_digest` · store ID · URI · enforcement · 만료.
**순수 함수다** — provider 를 읽기만 한다.

### 3.2 발견 3·4 — exact version 을 lifecycle 전체로

| 자리 | 37차 | 38차 | 검사 |
|---|---|---|---|
| `read_lease()` | version 없이 읽고 나중에 lock 조회 | 봉인 version 으로 읽는다 | `..._reads_the_lease_at_its_sealed_version` |
| `verify_pins()` | lease 의 version map 버림 | `versions=` 로 받는다 | `..._uses_the_sealed_graph_versions` |
| lease content version | 봉인 없음 | journal `lease_content_version` | `..._the_lease_content_version_is_sealed_too` |
| store identity | live-lock census | lease `store_version_id`·`store_lock_mode` | `..._is_sealed_in_the_lease` · `..._tampered_store_version_seal_is_refused` |
| canonical selector | `LOCK_MODES` | `DURABLE_MODES` (Compliance 만) | `..._governance_store_version_is_not_a_canonical_candidate` |
| fake lock | until 대입 · mode 미저장 | **version 별 mode 봉인 · Compliance 단조** | `..._enforces_per_version_mode_and_monotonic_compliance` |

### 3.3 #9-1 — 시간 기반 lease 를 **버렸다**

`fcntl.flock` 은 process 가 죽으면 kernel 이 자동으로 푼다. owner
liveness·heartbeat·stale 판정·fencing 이 **전부 필요 없어진다** — 있어야 할
것을 더 만드는 대신 필요 없게 만드는 쪽이다.

| 검사 | 축 |
|---|---|
| `..._blocks_a_second_writer_and_dies_with_its_owner` | 배타 + crash 잔여 파일이 영구히 막지 않음 |
| `..._live_owner_is_not_evicted_however_long_it_holds` | 하루 늙혀도 못 빼앗는다 |
| `..._old_owner_cannot_delete_the_new_owners_lock` | release 의 token 대조 (독립 불변식) |
| `..._internal_publisher_cannot_move_the_pointer_without_the_lock` | `_promote_generation(lock=)` 필수 |

### 3.4 #9-2 — 가드를 이름에서 **namespace** 로

리뷰가 지목한 line 1260 을 고치려고 가드를 넓혔더니 **네 곳이 더** 나왔다:
`_projection` · `_projection_rows` · `_restart_rows` · warm pair 시험. 전부
`_snapshot_for_leg()` 로 옮겼다. `_sealed_projections()` 의 이중 snapshot 도
하나로 합쳤다 (이름과 내용이 서로 다른 `CURRENT` 읽기에서 오던 것).

가드 규칙 둘: cohort record 의 `dir` 은 snapshot 생성자에서만 · `_WARM` 은
generation 세 suffix 에 닿을 수 없다.

### 3.5 #9-3 — roster authority, 그리고 **exact 를 요구할 수 없는 이유**

`_ledger_roster()` 가 보존 원장에서 읽고, `promote_cohort_generation(..., roster=)`
는 **기본값이 없다** (`..._roster_is_mandatory_for_the_publisher` 가 signature 를
본다).

다만 publisher 에 exact roster 를 요구할 수는 **없다**: roster={a,b} 인 cohort 에
a 를 처음 게시할 때 b 는 존재할 수 없다. 의무를 나눴다.

| 주체 | 의무 |
|---|---|
| publisher | 명부에 없는 leg 를 만들지 않는다 (**base 에서 물려받는 것 포함**) |
| reader | exact roster 를 요구한다 (`_Snapshot`) |

검사: `..._refuses_a_leg_the_roster_does_not_declare` ·
`..._base_leg_the_roster_dropped_blocks_the_next_publish` ·
`..._whole_leg_missing_from_the_roster_is_not_complete`.

## 4. 변이 — 여섯이 물지 않았고 **셋은 코드를 지웠다**

| 물지 않은 변이 | 진단 | 처리 |
|---|---|---|
| content lock 의 바이트 대조 | 후보 filter 가 이미 한다 | **삭제** |
| `undeclared` / `leg not in roster` / `not roster` | 셋이 서로 가림 | **둘 삭제** + base drift 시험 |
| shrink 검사 | `keep` 복사가 구조로 막아 도달 불가 | **삭제** |
| store selector 의 Compliance 제한 | 두 mode 를 갈라 놓은 시험 없음 | 시험 보강 |
| 봉인 store version 검증 | 변조 시험 없음 | 추가 |
| 만료 판정 | 갱신 축 미검사 | §2 에서 기능 자체를 뺐다 |

## 5. 산출물 재생성

| 항 | 이전 → 현재 |
|---|---|
| `source_digest` | `ccb3e2ad0f6145c0` → `59ba034148cf8a60` |
| `compute_sha256` (g2) | `4d948d46f4123ce4` → `f4602a9b7aae8e1b` |
| `row_projection_py_sha256` (g2) | `c08b6309e6c79a7d` → `c6db39d9319a4f86` |
| receipt `core_sha256` | `c80b580a8647dfde…` → `0a6cb73b1d979d01…` |

행 바이트는 안 움직였다 (`proj ad598fe77e75afec` · 봉인일치 True).

## 6. 이 환경에서 닫히지 않는 것 — 신고

| 항 | 상태 | 왜 |
|---|---|---|
| 실제 object-lock provider adapter | **미구현** | 자격증명·네트워크 없음. 계약 8연산·per-version·delete-marker·Compliance 단조성은 고정 |
| power-loss ordering fault model | **미착수** | `os._exit` 는 fsync 안 된 항목을 잃지 않는다 |
| **lease 갱신** | **미지원으로 신고** (신규) | §2. active lease pointer 또는 retirement primitive 설계가 선행 |

## 7. 리뷰 요청 사항

1. §2 의 **기능 제거**가 옳은 판단인가 — 동작한 적 없는 갱신을 빼고 fail-closed
   로 좁힌 것. (리뷰가 준 세 선택지 중 셋째)
2. §3.5 의 **의무 분할**이 옳은가 — publisher 에 exact roster 를 요구할 수 없는
   이유(bootstrap)와, 그 대신 reader 가 exact 를 지는 구조.
3. §3.3 의 **`flock`** 이 이 저장소의 배치(단일 호스트 로컬 filesystem)에서
   충분한가 — 시간 기반 lease 를 버린 판단 포함.
4. §4 의 **셋을 지운 판단** — 중복이라 지운 것이 맞는가, 특히 도달 불가능한
   shrink 검사.
5. §3.2 의 봉인 축 넷(store version · lease pin · lease content · graph pin)이
   충분한가 — 더 봉인해야 할 locator 가 남아 있는가.
