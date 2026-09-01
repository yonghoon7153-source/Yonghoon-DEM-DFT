# 55차 작업 상태 (진행 중 — 파일이 정본이다)

54차 판정 **NO-GO** (P0 5묶음 · P1 2건). 대상 커밋
`d824ecf8804a4e64c147f82e554d9ecb8a4aeef6`.

## 진행표

| # | 반례 | RED | 수정 | GREEN | 자리 |
|---|---|---|---|---|---|
| P0-1 | 정상 finalize 가 공용 token 경로의 **새** 소유 증명을 삭제 | ○ | ○ | ○ | `preserve.py` `finalize_leg` — 정상 경로도 `_lifecycle_locks()` |
| P0-2 | 같은 ledger 인자가 **자기 쓰기 뒤** 다른 claims root | ○ | ○ | ○ | `preserve.py` `canonical_ledger()` 신설 · 7자리 해석을 1자리로 |
| P0-3 | stale anchor repair 가 `.head` 를 과거로 되돌림 | ○ | ○ | ○ | `row_projection.py` `_lifecycle_lock()` 신설 · repair 를 그 안으로 |
| P0-4 | frozen root 의 **bind-mount 별칭**에 게시 가능 | ○ | ○ | ○ | `row_projection.py` `_through_bind_mounts()` — mountinfo 로 목적지를 푼다 |
| P0-5 | producer identity 가 두 문법을 놓침 (역방향 alias · 동적 dunder) | ○ | ○ | ○ | `row_projection.py` `MODULE_EFFECTS` 뿌리 · 동적 이름 풀기 fail-closed |
| P1-1 | freeze 가 잘못된 목적지를 거부하기 **전에** 부작용 | ○ | ○ | ○ | `row_projection.py` `_assert_dest_inside_repo()` 를 첫 쓰기 앞 + lock 안 재확인 |
| P1-2 | coverage HEAD 결속이 "실재하는 commit" 이면 통과 | ○ | ○ | ○ | `mutation_replay.py` `_tested_tree_digest()` — checker 가 지금 트리와 대조 |

## 닫은 것의 요지

**P0-1** — 54차는 finalize 의 **복구 분기만** `_lifecycle_locks()` 로 옮겼고
정상 경로는 claim → ledger 만 잡은 중복 구현으로 남았다. 창은
`_unlink_token_generation()` **안**(generation 비교 → `unlink` 사이)이므로
RED 재현은 `Path.unlink` 를 hook 해야 한다 — 함수 자체를 hook 하면 generation
검사가 먼저 막아 **거짓 초록**이 난다 (실제로 한 번 그렇게 통과했다).

**P0-2** — 해석이 두 벌이었다: `claims_root_for_ledger()` 는 `.resolve()` 한
경로를, 원장 쓰기는 해석 안 한 경로를 봤다. symlink 원장이면 `os.replace()`
가 symlink 를 일반 파일로 바꿔 같은 인자가 다른 곳을 가리킨다.
`canonical_ledger()` 하나로 모았다 (raw 해석 7 → 1, 그 1은 함수 자신).

**P0-3** — journal 과 `.head` 에는 lock 이 **하나도** 없었다. `_lifecycle_lock()`
을 두고 `_append_lifecycle()` 과 `repair_lifecycle_anchor()` 가 공유한다.
`freeze_cohort` 안에서 둘은 배타 분기라 중첩 없음(deadlock 없음) — 확인했다.

**P0-5①** — 54차는 `Expr` 를 **쓰여 있는 이름**에 결속했다. 별칭을 한 겹
끼우면(`ALIAS = BOX`) 계산이 읽는 이름의 닫힘에서 빠진다. 이름 추적으로는 별칭
겹수를 이길 수 없으므로 방향을 뒤집었다 — docstring 아닌 module-level `Expr`
는 예약 이름 `MODULE_EFFECTS` 에 묶이고 두 닫힘 walk 의 seed 에 **무조건**
들어간다.

**P0-5②** — dunder 검사가 직접 `Constant` 인자만 봤다. 이름 공간을 푸는
호출(`_DYNAMIC_ON_NAMESPACE`)의 이름 인자가 문자열 상수가 아니면 거부한다
(`*[...]` · `[...][0]` · 변수 전부). 시험은 **새 규칙이 물었는지**를 못 박는다
— 옛 규칙이 대신 잡으면 증명하는 것이 없다 (한 번 그렇게 될 뻔했다).

**P0-4** — 실측: `os.path.ismount(alias)=False` (같은 FS bind 는 안 잡힌다) ·
`realpath` 도 안 푼다 · **st_ino 는 원본과 같다**. 그래서 이름으로는 못 잡고
`/proc/self/mountinfo` 의 mount 관계를 읽어 목적지를 푼다. 리뷰어는 marker 가
있는 root 가 아니라 **자식**을 bind 했으므로, 푼 경로의 **조상**까지 marker 를
본다.

**P1-1** — `_PublishLock(dest)` 자체가 쓰기다. 목적지 containment 검사를 그
앞으로 옮기고 lock 안에서 한 번 더 본다.

**P1-2** — `head` 는 "실재하는가" 만 물으므로 어느 commit 이든 통과했다.
`_tested_tree_digest()` (변이 대상 3파일 + 기대 실패 시험 파일의 바이트)를
조각에 적고 checker 가 **지금 트리**와 대조한다.

## 다음 단계

1. 산출물 재생성 (RUN_SCOPE 가 움직였다 — `preserve.py` 수정) → g10.
2. 변이 등록부에 55차 방어 등록 → 12조각 전수 → 합집합.
3. 전체 회귀 + strict smoke → 요청문.

## 주의

- `preserve.py` 는 RUN_SCOPE 다 → `source_digest` 가 이미 움직였다. 산출물
  재생성이 **필수**이고 cohort 는 g9 → g10 으로 간다.
- `row_projection.py`·`mutation_replay.py` 는 `docs/` 라 RUN_SCOPE 밖이지만,
  `row_projection.py` 는 **producer semantic digest** 에 들어가므로 P0-5 를
  고치면 pin 이 또 움직인다 (53·54차와 같은 형태).
