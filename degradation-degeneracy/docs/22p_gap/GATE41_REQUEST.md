# 41차 게이트 리뷰 요청 — 40차 반증 조건 10개 대응

> **대상 커밋**: `283251fd279f5251813fac0d9dd07ef4145a4ff5`
> **직전 대상**: `f0aa24f11d7aa0ce4bf339027235a96fa4422aae`
> **브랜치**: `claude/14-gate-code-review-9qkx05`
> **source_digest**: `db34cc3d3aeca5e2` → `b587816c40999e27`
> **원장**: `docs/08_REVIEW_RESPONSE.md` §49

40차 판정은 NO-GO 였고, "반증 조건 1~11 전부 종결" 이라는 내 주장을 기각했다.
그 기각을 수용한다. 40차가 준 **최소 반증 조건 10개**를 조건별로 아래에 적는다.

---

## §1. 조건별 대응

### 조건 1 — store locator 가 exact store record 를 증명해야 한다

**40차**: `_locator_holds("store.json", v, None, mode, rec)` — `dg is not None`
일 때만 bytes 를 본다. store 는 존재·mode·기한만 보고 record 의미를 안 봤다.

**대응**: `_locator_holds()` 를 **typed 둘**로 가른다. `dg=None` 분기가 없다.

| 함수 | `tools/preserve.py` | 무엇을 결속하는가 |
|---|---|---|
| `_locator_state()` | L947 | 존재 · mode 동등 · 기한 덮음 (**여기서 끝내면 안 된다**) |
| `_object_locator_holds()` | L968 | 위 + `_bytes_match(key, version, dg)` |
| `_store_locator_holds()` | L975 | 위 + `_is_store_record(got)` + `got["store_id"] == rec["store_id"]` |

**반례 회귀** (`tests/test_preserve.py`, 위조 축 12개 parametrize):

| 축 | provider 상태 |
|---|---|
| `store_version_other_store` | canonical v1 = record(A) Compliance / v2 = **record(B)** Compliance, 기한 충분 · candidate = `store_id=A, store_version_id=v2` |
| `store_version_not_a_record` | v2 = `b"not-a-store-record-at-all"`, Compliance, 기한 충분 |

두 축 모두 candidate 단계에서 `PreserveError`, 그리고 시험이 **거부 전후**를
대조한다: version census · `store._lock` 전체 · `pinned(leg)` · `store.json`
head bytes 가 모두 동일해야 한다.

### 조건 2 — base local backend 의 candidate validation·strict mismatch 가 read-only

**40차**: `CasBackend.inspect_store_id()` 가 `return self.store_id` (없으면 만들고
CAS root 를 굳힌다). strict verifier 는 불일치를 inspect 로 찾고 **오류 문자열**
에서 `self.store_id` 를 다시 평가했다.

**대응**: `inspect_store_id()` 가 `store.json` 을 읽기만 한다 (없으면 `None`,
형식이 이상하면 `None` — fail-closed). `verify_retention()` 은 읽은 값을
`live_sid` 에 담고 메시지도 그것만 쓴다 (`tools/preserve.py` L1030).

**회귀**: `test_the_local_backend_inspect_never_creates_or_extends_the_store` —
`store.json` 을 지운 뒤 ① `inspect_store_id()` ② `_matches_lease()`
③ `verify_retention()` 셋을 부르고, `store.json` 이 **끝까지 없어야** 한다.

### 조건 3 — unlocked v1 + same-bytes Governance v2 에서 재개

**40차**: repair **source** 와 repair **target** 이 같은 selector 였다.
`_existing_version()` 은 최신 same-bytes 를 고르므로 Governance head 를 잠갔고,
Governance 는 Compliance 로 승격되지 않아 재개가 영영 실패했다.

**대응 — 네 phase 로 가른다**:

| phase | 함수 | 묻는 것 |
|---|---|---|
| proof lookup | `_version_for()` L1594 | 잠긴 담보 + exact bytes |
| repair byte source | `_repair_source()` L1611 | 바이트를 **읽을** 수 있는가 (잠금 안 묻는다) |
| repair target | `_repair_target()` L1625 | 담보로 **만들** 수 있는가 (unlocked 또는 이미 담보) |
| journal verify | `recover_lease_version()` · `recover_content_version()` | 봉인된 exact ID 만 |

`_lock_to_proof()` (L1664) 가 target 선택 → `lock()` → **proof selector 재실행**
을 한 자리에 묶는다. proof 가 없으면 `PreserveError`. `retain()` 은 더 이상
`pv`(repair source) 를 `lease_version` proof 로 넘기지 않는다 (L855).

**회귀 둘**:
- `test_a_same_bytes_governance_head_does_not_block_repair` — `after_lease_pin`
  crash + unlocked exact v1 + same-bytes Governance v2. `finalize_only()` 가
  같은 lease 로 재개하고, 돌려준 proof version 의 mode 가 `COMPLIANCE` 여야 한다.
- `test_a_lock_that_does_not_produce_a_durable_version_fails_closed` —
  `lock()` 이 Governance 로 봉인하는 provider. `lock_content_object()` 가
  bogus proof 를 돌려주지 않고 거부해야 한다.

### 조건 4 — 위조 lock (instance attribute · subclass override)

**40차**: `isinstance(lock, _PublishLock)` + **virtual** `lock.assert_held_for(out)`.
`isinstance` 는 subclass 를 통과시키고 속성 조회는 instance 속성이 이긴다.

**대응** (`docs/22p_gap/row_projection.py` L940):

```python
if type(lock) is not _PublishLock: raise SystemExit(...)
_PublishLock.assert_held_for(lock, out)
```

**회귀 셋**:
- `..._lock_whose_assert_is_overridden_cannot_publish[instance_attribute]`
  — `object.__new__(_PublishLock)` + `fake.assert_held_for = lambda out: None`
- `..._lock_whose_assert_is_overridden_cannot_publish[subclass_override]`
- `..._subclass_holding_a_real_lock_cannot_weaken_its_own_checks` — **진짜
  `__enter__` 를 지난** subclass 가 `_reassert_kernel_lock` 을 override 한 뒤
  실제로 lock 을 놓고 B 가 가져간 상태. unbound 호출만으로는 못 막는 축이다
  (내부 검사가 `self.` 로 불리기 때문). 정확한 타입 검사가 이것을 막는다.

셋 다 `CURRENT` 와 `gen/` 목록이 전후 동일함을 확인한다.

### 조건 5 — A unlock / B lock / A publish

**40차**: `_holds_kernel_lock()` 은 두 번째 fd 로 `LOCK_EX|LOCK_NB` 를 시도해
실패하면 "내가 들고 있다" 고 결론냈다. 그 실패는 *누군가* 잠갔다는 뜻일 뿐이고,
아무도 안 잠근 상태에서는 probe 가 **실제로** lock 을 잠깐 취득했다 놓았다.

**대응**: 그 함수를 **삭제**하고 `_reassert_kernel_lock()` 을 둔다 (L808) —
게시 직전 **원래 fd** 에 `LOCK_EX|LOCK_NB` 를 다시 적용한다. 관측이 아니라
강제다. 남이 들고 있으면 실패하고, 남의 lock 은 건드리지 않는다.

**회귀**:
- `..._lock_another_writer_stole_is_refused_without_touching_it` — A enter →
  A `LOCK_UN` → B `LOCK_EX` → A publish 시도. A 거부 · **세 번째 fd 로 B 의
  lock 이 여전히 살아 있음을 확인** · `CURRENT` 불변.
- `..._reapplying_flock_to_an_fd_that_already_holds_it_succeeds` — 이 수정이
  기대는 플랫폼 성질을 별도 회귀로 고정한다 (40차 리뷰가 요구한 항목).

**의미가 바뀐 시험 하나 — 숨기지 않는다.** 40차의
`test_a_manually_unlocked_real_lock_is_refused` 는
`..._is_retaken_before_publishing` 이 됐다. 아무도 안 들고 있는데 내 fd 만
풀린 경우는 이제 **되찾는다** (상호배제는 유지된다). 리뷰가 그 판정 predicate
자체가 틀렸다고 했으므로, 관측을 버리고 강제로 옮긴 결과다.

### 조건 6 — sentinel symlink / hardlink (파괴적)

**40차**: `O_NOFOLLOW` 없이 열고 flock 뒤 `ftruncate(fd, 0)`.
`.publish.lock -> CURRENT` 면 lock 취득이 권위 파일을 비웠다.

**대응** (`__enter__`, L761):
1. `os.open(path, O_CREAT|O_RDWR|O_NOFOLLOW, 0o644)` — symlink 는 열리지 않는다
2. `_assert_plain_sentinel(fd)` — `S_ISREG` + `st_nlink == 1` (**flock 전에**)
3. flock
4. `_assert_plain_sentinel(fd)` **다시** — 검사와 잠금 사이 교체 감지, 실패하면 unlock+close
5. `ftruncate` **삭제**

`assert_held_for()` 의 `Path.stat()` 도 `os.stat(..., follow_symlinks=False)` 로.

**회귀**: `..._lock_sentinel_cannot_be_aimed_at_another_file[symlink|hardlink]`
— 취득이 **거부되고**(`SystemExit`), `CURRENT` 와 `gen/` 전체가 byte-for-byte
동일해야 한다.

### 조건 7 — module scope `_WARM_ALIAS = _WARM`

**40차**: `_warm_offenders()` 가 `FunctionDef` 를 찾아 그 **안**만 돌았다.

**대응**: 전체 AST 를 **scope 를 들고** 순회한다 (`tests/test_docs_lint.py`
`_warm_offenders`). `fn` 은 가장 안쪽 함수 이름이고 module scope 는 `None` 이라
allowlist 에 없다. decorator·기본값·annotation 은 **바깥** scope 로 판정한다.
허용 accessor 안의 nested function 도 각자 자기 이름으로 판정된다 (40차 리뷰가
경고한 자리).

**회귀 둘**: `..._warm_guard_catches_a_module_scope_alias` (반례 그대로) ·
`..._an_allowed_accessor_may_still_read_warm` (전제 — guard 가 전부를 빨갛게
만들면 앞 시험이 공허참이 된다).

### 조건 8 — 같은 cohort ID · 다른 디렉터리

**40차**: 소비자 넷이 원장을 각자 파싱했다. `_ledger_roster()` 에만 디렉터리
중복 검사가 있었고 `_cohort_dir()` 은 첫 ID 를, `_frozen_cohort_dirs()` 는
dict comprehension 으로 조용히 덮었다.

**대응**: `_ledger_cohorts()` (L1292) — **중앙 parser 하나**가 조회 **전에**
`cohort_id` 와 resolved directory 의 유일성을 강제한다.
`_ledger_roster`·`_cohort_dir`·`_frozen_cohort_dirs` 가 전부 그것만 쓴다.
시험 쪽 selector 가 읽는 `_cohorts()` 에도 같은 규칙을 넣었다.

**회귀**: `..._ledger_that_declares_one_cohort_id_twice_is_refused[order 0|1]`
— **원장 항목 순서를 뒤집어** 두 번 돌리고, 세 소비자가 전부 거부하며
메시지에 중복 ID 가 나와야 한다. `..._snapshot_selector_refuses_a_ledger_with_a_duplicate_cohort_id`.

### 조건 9 — unknown purpose (40차 회귀는 false-green 이었다)

**40차 리뷰가 맞다.** 그 회귀는 두-cohort fixture 라, unknown-purpose guard 를
지워도 `purpose="compare"` 가 뒤의 "두 cohort 에 모두 있다" 분기에서 같은
`AssertionError` 를 냈다. 변이로 확인했다.

**대응**: `..._unknown_purpose_is_refused_even_with_one_cohort` — cohort 를
**하나만** 둔다. guard 가 없으면 selector 는 조용히 그 하나를 돌려주므로,
거부는 guard 때문일 수밖에 없다. 전제(`_snapshot_for_leg("L")` 는 그냥 고른다)
를 시험 안에서 assert 한다. 변이(`if purpose not in (...)` → `if False`)가
이제 **문다**.

### 조건 10 — 두 writer + 원장 전환

**부분 대응이다. 종결을 주장하지 않는다.**

닫은 둘:
- 원장 조회를 **임계 구역 안**으로 (`promote_cohort_generation` L1181).
  회귀 `..._roster_is_read_from_the_ledger_inside_the_publish_lock` 는
  `_ledger_roster` 호출 시점마다 `_PublishLock._ACTIVE` 가 비어 있지 않은지 본다.
- pointer CAS 를 `generation_id` 가 아니라 **base pointer 의 바이트 전체
  digest** 로 (`_pointer_fingerprint()` L981). `roster_digest` 와
  `base_generation` 은 generation ID 밖이라 gid CAS 로는 안 보였다.
  회귀 `..._pointer_cas_compares_the_whole_record_not_just_the_generation` —
  base 를 읽은 뒤 게시 전에 `.PENDING` 을 **같은 gid · 다른 명부 digest** 로
  갈아 끼운다.

**아직 아닌 것**: 두 process 동시 게시 회귀, roster generation 과 cohort
generation 의 단일 승인 전환. 후자는 설계 항목으로 신고한다.

---

## §2. 변이 시험 — 16축, 그리고 처음에 안 문 여섯

전부 물었다:
`store-locator-record-binding` · `inspect-store-id-pure` ·
`verify-error-string-pure` · `repair-target-mode-filter` ·
`lock-to-proof-rederive` · `retain-proof-not-repair-source` ·
`exact-type-check` · `unbound-assert-call` · `reassert-kernel-lock` ·
`o-nofollow` · `nlink-check` · `roster-inside-lock` ·
`full-pointer-cas`(2-site) · `ledger-dup-id` · `cohorts-dup-id` ·
`unknown-purpose-guard`.

**처음에 여섯이 안 물었다. triage 를 그대로 적는다** — 40차 리뷰가 요구한
"masked mutation 을 목록으로 관리하라" 에 해당한다.

| 안 문 변이 | 왜 가려졌나 | 처리 |
|---|---|---|
| `exact-type-check` | unbound 호출이 위조 둘을 이미 잡았다. 그러나 **진짜 lock 을 든 subclass 가 내부를 override** 하면 unbound 호출도 뚫린다 | 시험 보강 (`..._subclass_holding_a_real_lock_...`) |
| `lock-to-proof-rederive` | 그 반례에서는 target 과 proof 가 같은 version 이었다 | 시험 보강 (Governance-only provider) |
| `o-nofollow` · `nlink-check` | 시험이 **바이트 불변**만 봐서 `ftruncate` 제거만으로 초록이 됐다 | 시험 보강 — **거부까지** 요구 |
| `full-pointer-cas` | 변이 설계 오류 (한쪽만 gid 로 되돌려 언제나 불일치) | 2-site 변이로 재실행 |
| `no-truncate` | 소유권 검사가 앞서므로 truncate 가 남의 inode 에 닿을 수 없다 | **코드를 남긴다** — 파괴적 축의 심층 방어이고 애초에 불필요한 연산의 제거다. **독립 관측되지 않는다는 것을 여기 신고한다** |

---

## §3. 실측 증거 (커밋 `283251fd` 에서 방금)

```
$ python -m pytest tests/ -q
1127 passed, 1 xfailed in 327.14s (0:05:27)

$ ./scripts/smoke_e2e.sh
✅ pipeline smoke 통과
⚠ 보존 gate 미완료 (계약 v4 묶음 9) — 새 leg 실행 금지.

$ python3 docs/22p_gap/row_projection.py paired_fixed5_v4 --cohort g2_2026_08_25
✅ paired_fixed5_v4: 6138행 · restart 30690행 · proj ad598fe77e75afec ·
   전체 True · by_obj True · fits삼중 True · 봉인일치 True

$ python3 docs/22p_gap/make_receipt.py paired_fixed5_v4 --check
✅ paired_fixed5_v4: core 재생성 바이트 동일 · core_sha cb18faff43432bad

$ python wiki/tools/lint.py
RESULT: 0 errors

$ git status --short
(비어 있음)
```

| 축 | 40차 | 41차 |
|---|---|---|
| `source_digest` | `db34cc3d3aeca5e2` | `b587816c40999e27` |
| g2 `compute_sha256` | `28c5151d788f7ec0` | `18a994ac9f9c27c4` |
| g2 `row_projection_py_sha256` | `3b54fe35d80f4eb3` | `114de75d462957a7` |
| receipt `core_sha256` | `03d6f842b9ca6922…` | `cb18faff43432bad…` |
| **투영 행 바이트** | `ad598fe77e75afec` | **`ad598fe77e75afec`** (불변) |

---

## §4. 스스로 신고하는 것

1. **조건 10 을 종결로 주장하지 않는다.** 두 process 동시 게시 회귀와
   roster/cohort generation 의 단일 승인 전환은 미착수다.
2. **`no-truncate` 변이는 독립 관측되지 않는다** (§2 표 마지막 줄).
3. **시험 하나의 의미를 바꿨다** (§1 조건 5) — 40차가 요구했던 "manual unlock
   은 거부" 를 "되찾는다" 로 바꿨다. 리뷰가 그 판정 방식을 기각했기 때문이고,
   그 사실을 시험 docstring 과 원장 §49 에 적었다.
4. 실제 object-lock provider adapter · power-loss ordering fault model 은
   여전히 미구현·미착수다.

---

## §5. 질문

1. **조건 1** — `_store_locator_holds()` 를 `_locator_state()` 위에 얹는 형태로
   두었다. 40차 리뷰는 `VerifiedStoreLocator`/`VerifiedObjectLocator` **타입**을
   제안했는데, 지금 형태(공유 prelude + typed predicate 둘, `dg=None` 분기 없음)로
   재발 방지가 충분한가, 아니면 반환 타입 자체를 갈라야 하는가?
2. **조건 3** — 네 phase 를 함수 이름으로 갈랐다. `_lock_to_proof()` 가
   target→lock→proof 재유도를 한 자리에 묶는 것이 맞는가, 아니면 호출자가
   각 phase 를 명시적으로 밟아야 하는가?
3. **조건 5** — `_reassert_kernel_lock()` 은 "아무도 안 들고 있으면 되찾는다".
   이것이 상호배제 관점에서 받아들일 만한가, 아니면 "내 fd 가 한 번이라도
   풀렸다" 를 별도로 탐지해 거부해야 하는가 (그럴 수단이 flock 에 있는가)?
4. **`no-truncate`** — 소유권 검사에 가려져 독립 관측되지 않는다. 이런 항목을
   앞으로 어떻게 다뤄야 하는가: 코드 삭제 / 관측 가능하게 시험 재설계 /
   "masked but retained" 목록으로 명시 관리?
5. **조건 10** — 두 process 동시 게시 회귀를 이 저장소 시험 환경에서 어떤
   형태로 요구하는가 (`fork` + pipe 동기화? `subprocess` 두 개? 아니면
   `_PublishLock` 의 fd 를 두 개 잡아 in-process 로 흉내내도 되는가)?
