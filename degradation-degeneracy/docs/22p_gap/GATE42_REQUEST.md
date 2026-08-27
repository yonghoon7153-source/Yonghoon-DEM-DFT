# 42차 게이트 리뷰 요청 — 41차 반증 조건 9개 대응 (+ 인프라 2건 계속 신고)

```yaml
브랜치:     origin/claude/14-gate-code-review-9qkx05
대상 커밋:   c8265c4d3474f06c5a7be1e2432c01a74b9598e3
직전 대상:   283251fd…      (41차, 조건 1·2 종결 / #9 P0·retention P1 NO-GO)
source_digest: b587816c40999e27 → 3e5aa23c80d90243
원장:       docs/08_REVIEW_RESPONSE.md §50
```

41차 판정을 수용한다. 40차 P0-1(store locator) 종결 인정도 받았다 — 조건 1·2 는
다시 열지 않는다. 41차가 준 **최소 반증 조건 9개**(10번은 인프라)를 조건별로 적는다.

41차가 짚은 병은 한 문장이다: **검증이 끝난 값이 다음 단계까지 따라가지 않으면
그 단계에 대해서는 아무것도 증명하지 않는다.** 세 자리에서 같은 형태였다 —
unbound 바깥/virtual 안쪽, 검사 시점/commit 시점, 검증 phase/사용 phase.

---

## §1. 조건별 대응

### 조건 1 — exact instance 의 inner override

**41차**: `type(lock) is _PublishLock` + unbound outer call 은 넣었는데
`assert_held_for()` **안**은 `self._assert_plain_sentinel` ·
`self._reassert_kernel_lock` 이었다. 정확한 타입 인스턴스도 평범한 객체다.

**대응** (`row_projection.py` `assert_held_for` 끝):

```python
_PublishLock._assert_plain_sentinel(self.fd)
_PublishLock._reassert_kernel_lock(self)
```

**회귀** `test_an_exact_lock_cannot_blank_its_own_inner_check` — 정상 enter →
A `LOCK_UN` → B `LOCK_EX` → `a._reassert_kernel_lock = lambda: None` → raw
promotion. 거부 · B lock 생존(세 번째 fd 로 확인) · CURRENT·generation 불변.

> **신고**: same-process hostile Python 이 module 과 객체를 자유롭게 바꿀 수
> 있다는 모델에서 exact type 은 보안 경계가 아니다. raw publisher 를 아예
> 노출하지 않는 구조(취득~commit 을 하나의 신뢰 control flow 안에)는 **미착수**다.

### 조건 2 — 최종 검사 뒤 pathname 교체

**41차**: 마지막 inode 대조는 `assert_held_for()` 에서 끝나고, 그 뒤
staging scan · 자재화 · fsync · CAS · pointer 교체가 pathname 을 다시 결속하지
않는다.

**대응**: `_commit_guard()` — **pointer 를 옮기기 직전에** lock 결속과 원장을
다시 본다. `.PENDING` 게시와 `CURRENT` 게시 두 자리 모두. 실패하면 이미 굳은
generation directory 는 immutable 잔여로 남을 뿐 어떤 reader 에게도 안 보인다
(가시성 전환점은 pointer 하나다).

**회귀** `test_replacing_the_lock_pathname_after_the_check_refuses_the_commit`
— A 가 최종 assert 를 지난 뒤 sentinel 을 rename 하고 같은 pathname 에 새
inode 를 만들어 B 가 잡는다. A 거부 · CURRENT 불변.

> **신고**: 재검사는 창을 좁힐 뿐 **검사-직후 창을 없애지 못한다.** 41차가
> 말한 강한 해법(lock namespace 의 write authority 를 publisher 하나로 제한)은
> **미착수 설계 항목**이다. cooperative writer 전제를 계약에 적을지, 구조를
> 바꿀지는 리뷰 판단을 구한다 (질문 1).

### 조건 3 — single-read pointer snapshot

**41차**: `_read_pointer()` 로 parse 하고 `_pointer_fingerprint()` 가 파일을
**다시 읽어** 기대 digest 를 만든다. 그 사이 교체하면 옛 record 로 만든
generation 이 새 authority 아래 게시된다.

**대응**: pointer 를 **각각 한 번만** 읽는다.

```python
cur_raw  = _pointer_bytes(out, "CURRENT")
pend_raw = _pointer_bytes(out, ".PENDING")
...
cur    = _parse_pointer(out, base_ptr, base_raw)
expect = _sha(base_raw)                      # 같은 바이트에서 나온다
```

존재 판정 · parse · 기대 digest 가 전부 그 한 번의 반환값에서 나온다.
(중간에 만들었던 `_pointer_snapshot()` 은 쓰이지 않게 되어 **삭제**했다.)

**회귀** `test_the_base_pointer_record_and_its_fingerprint_come_from_one_read`
— `.PENDING` 이 첫 read 뒤 한 번 바뀌고 그대로 있는 파일을 주입한다. 한 번
읽는 구현은 commit 의 live read 와 어긋나 거부하고, 두 번 읽는 구현은
parse 만 옛 것으로 하고 기대 digest 를 새 것으로 만들어 **CAS 를 통과한다**.

### 조건 4 — stale bootstrap pending

**41차**: `CURRENT` 가 없으면 `base_ptr = ".PENDING"` 으로 시작하고,
`base_generation` 불일치는 조건만 false 가 될 뿐 **거부하지도 base 를 비우지도
않는다**. key 가 빠지면 `None == None` 이라 fresh bootstrap 으로 받아들인다.

**대응**:
- `_PENDING_KEYS = {schema, generation_id, files, roster_digest, base_generation}`
  — `.PENDING` 을 **닫힌 schema** 로 읽는다 (`_parse_pointer(..., pending=True)`).
- `pend["base_generation"] != cur_gid` → **명시적 거부** (`.PENDING` 을 지우고
  지금의 base 에서 다시 쌓으라는 메시지). "base 가 다르다" 와 "CURRENT 가
  없다" 를 같은 분기로 다루지 않는다.

**회귀** `test_a_stale_bootstrap_pending_is_refused_not_inherited[wrong_base|missing_base_key]`.

### 조건 5 — orphan hostile head

**41차**: `_orphan_lease()` 는 exact `(key, version)` 을 읽어 판정하고 digest
문자열만 반환한다. 호출자의 `pin()` 이 `read_back(digest)` 로 namespace 를
다시 읽어 hostile locked head 에 막힌다.

**대응**: `VerifiedBytes(key, version, digest, data)` 를 돌려주고
`adopt_orphan()` 이 **그 bytes** 로 pin 한다. locator 자체의 digest 일관성도
locator 를 만들기 전에 못 박는다.

**회귀 둘**: `..._orphan_lease_is_adopted_by_its_exact_version` (correct
unlocked v1 + wrong-bytes locked v2 → 같은 lease 로 재개) ·
`..._orphan_locator_never_carries_bytes_from_another_key` (유효한 lease record
바이트를 **다른 digest 의 key** 에 올려 두면 locator 를 안 만든다).

### 조건 6 — pin-source / content hostile head 결합

**41차**: `repair_lease_locks()` 는 pin 의 exact source 에서 올바른 bytes 를
읽어 놓고 content 존재를 **bytes-blind `has()`** 에 묻는다. `has()` 만 고쳐도
뒤이은 `put_if_absent()` 가 같은 protected read 로 collision 을 낸다.

**대응**: `has()`/`put_if_absent()` 왕복을 **삭제**하고
`lock_content_object(lease_digest, until, data=data)` 로 **검증된 bytes 를
직접 넘긴다.** exact bytes version 이 없으면 그것으로 새 version 을 만든다.

**회귀** `..._content_repair_uses_the_bytes_it_already_verified` — correct pin
bytes + correct content v1 **exact-version 삭제** + wrong locked head. 재개
성공, content proof 가 검증된 바이트를 담아야 한다.

### 조건 7 — proof-first 멱등성

**41차**: `_lock_to_proof()` 가 무조건
`repair target → lock → proof 재탐색` 이라, 충분한 Compliance v1 위의
same-bytes unlocked v2 를 새로 WORM-lock 했다.

**대응 — 41차가 준 순서 그대로**:

```
proof lookup(요청 기한을 덮는가) → 없을 때만 repair source/target
→ 없으면 검증된 bytes 로 새 version → lock → proof 재유도(같은 기한)
```

`_version_for(key, dg, until=)` · `_locked_versions(key, modes=, until=)` 에
요청 기한을 계약으로 넣었다.

**회귀 둘**: `..._locking_an_already_durable_object_adds_no_version`
(version census·lock state 전후 동일) ·
`..._short_horizon_proof_is_not_accepted_and_gets_extended` (짧은 기한
version 을 proof 로 받지 않고 **연장**한다 — 새 version 을 만들지 않고).

> **요청문 표 정정** (41차 지적 수용): `recover_lease_version()` ·
> `recover_content_version()` 은 sealed exact ID 를 verify 하는 함수가 아니라
> `_version_for()` 를 다시 도는 **live proof search** 다. 실제 journal
> exact-ID 경로는 `verify_registered_graph()` 가 journal ID 를
> `verify_retention()` 에 넘기는 자리다. 41차 요청문의 phase 표가 구현보다
> 강했다 — 원장 §50 에 고쳐 적었다.

### 조건 8 — warm structural bypass

**41차**: guard 가 "`_WARM` 이라는 **이름**을 읽는다" 만 본다. `_this()._WARM`
은 `Attribute` 라 통과하고, 허용 accessor 안의 `lambda` 는 바깥 함수 이름을
물려받아 allowlist 에 얹힌다.

**대응**: `ast.Attribute(attr="_WARM")` 도 위반. `Lambda` 를 **새 scope**
(`<lambda>`, allowlist 밖) 로 다룬다.

**회귀** `..._warm_guard_catches_attribute_and_lambda_bypasses`
— `some_reader` 안의 `_this()._WARM` · `_warm_summary` 안의 lambda 둘 다.

### 조건 9 — one-cohort unknown purpose / selector 소비자

조건 9 자체는 41차에 종결됐다. 41차가 남긴 **P2 증거** 를 여기서 닫는다:
duplicate-ID 회귀가 `_cohorts()` 를 직접 불렀다 → 소비자를 부른다.

**회귀** `..._snapshot_selector_itself_refuses_a_duplicate_cohort_id`
(`_snapshot_for_leg("L", cohort_id="gDUP")`).

### 조건 10 — 두 subprocess schedule + 원장 전환

**41차가 지정한 형태 그대로.** `fork` 도 in-process fd 두 개도 쓰지 않는다.

1. `..._second_process_holding_the_lock_blocks_and_loses_nothing`
   — 독립 `subprocess` A 가 lock 을 잡고 barrier 에서 멈춘다. B(이 process)
   게시 시도 → 실패 · **pointer·generation 무변이**. A 종료 후 B 재시도 →
   성공 · **아무 leg 도 잃지 않는다**.
2. `..._ledger_change_during_publication_is_refused`
   — 임계 구역 초입의 원장과 게시 직전 원장이 다르면 거부
   (`_assert_ledger_unchanged()`).

> **신고**: 두 번째는 **재확인**이지 단일 승인 전환이 아니다. 원장 세대와
> cohort 세대를 하나의 authority transition 으로 묶는 설계는 **미착수**다
> (질문 2).

### Q4 대응 — `no-truncate` 를 관측 가능하게

41차가 "삭제할 코드가 아니라 관측 가능한 시험으로 바꿔라. 이름도
`stable opaque sentinel` 이 맞다" 고 했다. 그대로 했다:
marker 바이트를 담은 평범한 nlink=1 sentinel 을 미리 두고 acquire/release 뒤
**같은 inode·같은 바이트**인지 본다 (`..._lock_sentinel_is_a_stable_opaque_inode`).
`ftruncate(0)` 을 되살리는 변이가 이제 **문다.**

---

## §2. 변이 시험 — 17축, 처음에 안 문 셋

전부 물었다:
`orphan-exact-locator` · `orphan-locator-digest-check` ·
`content-repair-verified-bytes` · `proof-first-lookup` ·
`proof-horizon-in-lookup` · `proof-horizon-filter` · `inner-unbound-sentinel` ·
`commit-guard-lock` · `commit-guard-ledger` · `single-read-base-fingerprint` ·
`pending-closed-schema` · `pending-base-generation` · `no-truncate-observable` ·
`warm-attribute` · `warm-lambda-scope` · `cohorts-dup-id-consumer` ·
`flock-two-process`(2-site).

| 처음에 안 문 변이 | 왜 가려졌나 | 처리 |
|---|---|---|
| `orphan-locator-digest-check` | 반례에 "key 가 말하는 digest ≠ bytes" 인 version 이 없었다 | **시험 추가** |
| `single-read-snapshot` | pointer 를 세 번 읽고 있어 주입 시점이 흐려졌다 | **코드 수정** — 각각 한 번만 읽게 바꾸자 변이가 물었다 |
| `flock-refuses-second-writer` | 취득 거부와 `_reassert_kernel_lock` 이 서로를 가린다 (심층 방어) | **2-site 변이** |

이번에는 "masked but retained" 로 남긴 항목이 **없다**.

---

## §3. 실측 증거 (커밋 `c8265c4d` 에서 방금)

```
$ python -m pytest tests/ -q
1143 passed, 1 xfailed in 320.20s (0:05:20)

$ ./scripts/smoke_e2e.sh
✅ pipeline smoke 통과
⚠ 보존 gate 미완료 (계약 v4 묶음 9) — 새 leg 실행 금지.

$ python3 docs/22p_gap/row_projection.py paired_fixed5_v4 --cohort g2_2026_08_25
✅ paired_fixed5_v4: 6138행 · restart 30690행 · proj ad598fe77e75afec ·
   전체 True · by_obj True · fits삼중 True · 봉인일치 True

$ python3 docs/22p_gap/make_receipt.py paired_fixed5_v4 --check
✅ paired_fixed5_v4: core 재생성 바이트 동일 · core_sha ce51f000a0d98691

$ python wiki/tools/lint.py
RESULT: 0 errors

$ git status --short
(비어 있음)
```

| 축 | 41차 | 42차 |
|---|---|---|
| `source_digest` | `b587816c40999e27` | `3e5aa23c80d90243` |
| g2 `compute_sha256` | `18a994ac9f9c27c4` | `e1111da301055fea` |
| g2 `row_projection_py_sha256` | `114de75d462957a7` | `0c9ef899ee405507` |
| receipt `core_sha256` | `cb18faff43432bad…` | `ce51f000a0d98691…` |
| **투영 행 바이트** | `ad598fe77e75afec` | **`ad598fe77e75afec`** (불변) |

---

## §4. 스스로 신고하는 것

1. **`_commit_guard()` 는 검사-직후 창을 없애지 못한다.** lock namespace 의
   write authority 를 publisher 하나로 제한하는 구조는 미착수다.
2. **원장 재확인은 단일 승인 전환이 아니다.** 원장 세대와 cohort 세대를 한
   transition 으로 묶는 설계는 미착수다.
3. **same-process hostile Python 에 대해 exact type 은 보안 경계가 아니다.**
   raw publisher 를 노출하지 않는 구조는 미착수다.
4. 41차 요청문의 phase 표가 구현보다 강했다 (`recover_*` 는 journal
   verification 이 아니라 live search). §1 조건 7 에 정정을 적었다.
5. 실제 object-lock provider adapter · power-loss ordering fault model 은
   여전히 미구현·미착수다. 위 1~3 과 **섞지 않는다** — 1~3 은 fake/local 에서
   닫을 수 있는 설계 항목이고, 이 둘은 인프라다.

---

## §5. 질문

1. **조건 2** — `_commit_guard()` 로 창을 좁혔지만 TOCTOU 는 남는다. 다음 중
   무엇을 요구하는가: (a) cooperative single-publisher 를 계약에 명시하고
   여기서 닫는다, (b) sentinel directory 를 권한 경계로 만든다, (c) 취득~commit
   을 fd 를 노출하지 않는 내부 critical section 으로 재구성한다?
2. **조건 10** — 원장 세대 ↔ cohort 세대의 단일 승인 전환을 어떤 형태로
   요구하는가: 원장에 `generation` 을 두고 pointer 가 그것을 봉인 / cohort
   lifetime 동안 roster immutable + 변경은 새 cohort ID 로만 / 다른 형태?
3. **조건 5·6** — `VerifiedBytes` 를 NamedTuple 로 두었다. 41차가 말한
   "opaque locator" 로 충분한가, 아니면 backend 만 만들 수 있게 생성자를
   닫아야 하는가 (그러면 시험이 위조 locator 를 만들 수 없게 된다)?
4. **조건 7** — `_lock_to_proof()` 가 proof-first 순서를 소유하게 했다.
   `until` 을 계약에 넣었는데, `verify_retention()` 이 쓰는 기한과 이 wrapper
   가 받는 기한이 **같은 값**이어야 한다는 것을 어디서 강제해야 하는가?
5. **인프라 2건** — 실제 provider adapter 를 언제 요구하는가: 묶음 9 종결
   조건인가, 아니면 fake/local 반례가 다 닫힌 뒤 별도 게이트인가?
