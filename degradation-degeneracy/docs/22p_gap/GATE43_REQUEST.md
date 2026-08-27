# 43차 게이트 리뷰 요청 — 42차 반증 조건 9개 대응 (인프라 2건 계속 신고)

```yaml
브랜치:     origin/claude/14-gate-code-review-9qkx05
대상 커밋:   093179863768048f7b7880d1a2feff4be3c0b401
직전 대상:   c8265c4d…      (42차, 조건 1·3·4·5·6·9 종결 / #9 P0 NO-GO)
source_digest: 3e5aa23c80d90243 → 9a18ed9776de34f3
원장:       docs/08_REVIEW_RESPONSE.md §51
```

42차 판정을 수용한다. 조건 1·3·4·5·6·9 와 stable-sentinel 종결 인정도 받았다 —
다시 열지 않는다. 42차가 준 **최소 반증 조건 9개**(10번은 인프라)를 조건별로 적는다.

42차가 짚은 병은 한 문장이다: **검사를 늘려도, 그 검사가 근거의 일부만 보거나
근거를 인자로 받을 수 있으면 불변식이 아니다.**

---

## §1. 조건별 대응

### 조건 1 — raw-entry rejection

**42차**: 유효한 exact lock 만 있으면 caller 가 `roster` 를 고르고
`recheck=None` 으로 원장을 통째로 우회할 수 있었다.

**대응**: 근거를 **한 객체**로 모은다.

| 이름 | 무엇 |
|---|---|
| `_Authority` | lock · 원장 cohort record 전체 · seal · roster · `CURRENT` bytes · `.PENDING` bytes · base 선택 |
| `_authority(lock, out)` | 그 snapshot 을 **만드는 유일한 자리** (contextmanager). 만든 것만 `_ACTIVE` 에 등록한다 |
| `_promote_generation(stage, auth)` | 인자가 **둘뿐**이다. `type(auth) is _Authority` + registry 확인 |

caller 가 넘길 수 있는 authority 인자가 **없다**. base 선택·pending 호환성
판정도 `_authority()` 안으로 옮겼다.

**회귀** `test_the_raw_publisher_takes_no_caller_authority` — ① signature 가
`{stage, auth}` 인지 (구조) ② `object.__new__(_Authority)` 로 조립한
authority + **진짜 lock** 으로 게시 시도 → 거부 · pointer·generation 불변.

> **신고**: same-process hostile Python 에 대해 Python 객체·이름은 보안 경계가
> 아니다 (42차 리뷰가 맞다). 이 수정이 닫는 것은 **우연한 우회 경로**다.
> process·권한 경계는 미착수 설계 항목이다 (질문 1).

### 조건 2 — same-roster ledger mutation

**42차**: `_assert_ledger_unchanged()` 가 `_ledger_roster()` 를 다시 부르는데
그 반환값이 `set(legs)` 뿐이라, `active → frozen` (legs 동일) 이 통과했다.

**대응**: `_ledger_cohort(out)` 가 **record 전체**를 돌려주고
`_ledger_seal(cohort)` 가 정규 digest 를 만든다. `_ledger_roster()` 는 그
위의 얇은 사본으로 남는다. commit guard 가 **seal** 을 대조한다.

**회귀** `test_a_same_roster_ledger_change_is_refused` — 게시 직전 재확인에서
`status` 만 `active → frozen` 으로 바꾼다 (legs 동일). 거부 · CURRENT 없음.

### 조건 3 — two-pointer interleaving

**42차**: `CURRENT` 와 `.PENDING` 을 각각 한 번 읽지만 **고른 한 쪽만** CAS 했다.

**대응**: `_commit_guard()` 가 `auth.pointers_now()` 로 **두 pointer 를 다**
읽어 snapshot 과 대조한다.

### 조건 4 — post-CAS mutation

**42차**: pointer 비교가 `_commit_guard()` **보다 먼저** 끝나므로, 그 사이에
바꾸면 그대로 `os.replace` 했다.

**대응**: 별도 `expect` 비교를 **없애고** 대조를 전부 guard 안으로 옮겼다.
guard 는 `_publish_pointer()` 직전에만 불린다.

**회귀 (조건 3·4 공용)** `test_a_pointer_moved_by_another_writer_is_never_overwritten`
— 다른 writer 가 올린 **유효한** CURRENT 를 두 시점에 끼워 넣는다:
`writable`(자재화 전) · `ledger_seal`(guard 의 **원장 검사 뒤 · pointer 검사
앞**). 둘 다 거부하고, 남의 CURRENT 가 그대로 남아야 한다.

### 조건 5 — real two-publisher lifecycle

**42차**: subprocess A 가 lock 만 잡고 기다린 **idle holder** 였고, B 도 같은
leg `a` 를 재시도했다.

**대응**: A 를 진짜 publisher 로 만든다 — **임계 구역 안에서** barrier 를 친다
(`_PublishLock` + `_authority` 를 들고 원장·base 를 읽은 뒤 멈췄다가 그대로
`_promote_cohort_locked()`). 두 process 다 독립 `subprocess` 이고 각자
**진짜 원장**(임시 repo root)을 읽는다.

**회귀** `test_two_independent_publishers_lose_no_leg`:

1. A 가 lock·authority 를 들고 barrier
2. B 가 **다른 leg** 게시 시도 → exit≠0 · CURRENT/.PENDING/gen 모두 없음
3. A 를 풀어 commit (exit 0) → B 재시도 (exit 0)
4. 최종 `read_current(out, expect_legs={a,b})` 에 **두 leg 가 모두** 남는다

### 조건 6 — proof handoff

**42차**: `repair_lease_locks()` 가 wrapper 가 돌려준 proof ID 둘을 버리고
`None` 을 반환했고, 호출자가 **기한 인자 없는** `recover_*()` 로 다시 찾았다.

**대응**: `RetentionProof(lease_version, content_version, until)` 를 돌려주고
`_existing_lease()` 가 그대로 verify 에 넘긴다. `recover_*()` 에 `until` 을
넣었다 (advisory backend 는 빈 proof — `None` 분기를 남기지 않는다).

**회귀 둘**: `..._repaired_proof_is_handed_to_verify_not_researched[pin·content]`
(wrapper 가 v1 을 돌려주고, **기한 없는 재탐색은 실제로 v2 를 고른다**는 전제도
함께 assert) · `..._pre_journal_finalize_uses_the_repaired_pin_proof`
(`after_pin_lock` crash = journal 이전 창에서 end-to-end).

### 조건 7 — pre-lock validation

**42차**: 새-version 경로가 `put` 뒤 곧바로 `lock` 했다.

**대응**: `put` **전** digest 확인 + `put` **뒤** 그 exact version read-back
확인 → 그 다음에 lock.

**회귀 둘**: `..._wrong_bytes_are_never_locked` (잠금뿐 아니라 **version 이
생기지 않는 것**도 본다) · `..._a_provider_that_returns_the_wrong_version_locks_nothing`.

### 조건 8 — warm structural bypass

**42차**: guard 가 syntax blacklist 다. `getattr` · mapping lookup · lambda
default capture 가 통과한다.

**대응 — 42차 리뷰가 권한 구조적 수정을 했다**: `_WARM` **global 을 없앴다.**
`_warm_accessors()` 의 closure 지역변수가 경로를 갖고 accessor 셋
(`summary`·`manifest`·`has_summary`)만 밖으로 나온다. **이름이 없으면
`getattr` 도 `globals()` 도 찾을 것이 없다.**

guard 는 지우지 않고 **재발 방지 회귀**로 남긴다 (문자열 상수 `"_WARM"` 과
lambda default capture 축 추가).

**회귀** `..._warm_root_is_not_a_module_global` ·
`..._warm_guard_catches_indirect_namespace_lookups[getattr·globals·lambda default]`.

### 조건 9 — inner sentinel mutation

**42차 지적을 수용한다.** 42차 요청문의 "17축 전부 물었다" 는 과장이었다:
`_assert_plain_sentinel` 을 virtual 로 되돌려도 kernel 검사가 B 때문에
거부해 시험이 초록이었다.

**회귀** `test_an_exact_lock_cannot_blank_its_sentinel_check` — kernel lock 은
**정상인 채로** 두고, 취득 뒤 sentinel 에 hardlink 를 걸어 `st_nlink` 를 2로
만든 다음 exact 인스턴스의 `_assert_plain_sentinel` 만 no-op 으로 덮는다.
`inner-unbound-sentinel` 변이가 이제 이 시험만 빨갛게 만든다.

---

## §2. 변이 시험 — 14축, 처음에 안 문 둘

전부 물었다:
`proof-handoff-to-verify` · `prelock-digest-check` · `prelock-readback-check` ·
`authority-registry` · `ledger-seal-record` · `both-pointers-in-guard` ·
`guard-before-commit` · `inner-unbound-sentinel` · `inner-unbound-kernel` ·
`pending-base-generation` · `pending-closed-schema` · `warm-string-constant` ·
`warm-lambda-default-scope` · `flock-two-publisher`(2-site).

| 처음에 안 문 변이 | 왜 가려졌나 | 처리 |
|---|---|---|
| `proof-handoff-to-verify` | 시험이 journal **이후** 상태를 썼다 — 그때는 runtime verifier 가 봉인 exact ID 를 쓰므로 handoff 축이 안 보인다 (42차 리뷰가 지적한 그 배선이 맞다는 뜻이기도 하다) | **시험을 pre-journal 창으로 옮겼다** |
| `prelock-digest-check` | read-back 검사가 가렸다 (잠그지는 않았다) | **시험 보강** — version census 도 본다 |

이번에도 "masked but retained" 로 남긴 항목은 **없다**.

> **RED 순서 신고**: 조건 1~4 는 production 을 먼저 고치고 시험을 뒤에 썼다
> (한 구조 변경이 네 조건을 함께 닫기 때문이다). 그 축들의 RED 증거는 위
> 변이 시험이다 — 각 수정을 되돌리면 해당 시험이 정확히 빨개진다. 조건 6·7·9
> 는 시험을 먼저 써서 실패를 보고 고쳤다.

---

## §3. 실측 증거 (대상 커밋에서 방금)

```
$ python -m pytest tests/ -q
1158 passed, 1 xfailed in 317.78s (0:05:17)

$ ./scripts/smoke_e2e.sh
✅ pipeline smoke 통과
⚠ 보존 gate 미완료 (계약 v4 묶음 9) — 새 leg 실행 금지.

$ python3 docs/22p_gap/row_projection.py paired_fixed5_v4 --cohort g2_2026_08_25
✅ paired_fixed5_v4: 6138행 · restart 30690행 · proj ad598fe77e75afec ·
   전체 True · by_obj True · fits삼중 True · 봉인일치 True

$ python3 docs/22p_gap/make_receipt.py paired_fixed5_v4 --check
✅ paired_fixed5_v4: core 재생성 바이트 동일 · core_sha f22116328335d8c7

$ python wiki/tools/lint.py
RESULT: 0 errors

$ git status --short
(비어 있음)
```

| 축 | 42차 | 43차 |
|---|---|---|
| `source_digest` | `3e5aa23c80d90243` | `9a18ed9776de34f3` |
| g2 `compute_sha256` | `e1111da301055fea` | `94c5e825cdce8fc7` |
| g2 `row_projection_py_sha256` | `0c9ef899ee405507` | `934fda4a9c4e74a3` |
| receipt `core_sha256` | `ce51f000a0d98691…` | `f22116328335d8c7…` |
| **투영 행 바이트** | `ad598fe77e75afec` | **`ad598fe77e75afec`** (불변) |

---

## §4. 스스로 신고하는 것

1. **`_Authority` 는 보안 경계가 아니다.** same-process hostile Python 은
   registry 도 타입도 바꿀 수 있다. 이 수정이 닫는 것은 우연한 우회다.
2. **lock pathname TOCTOU 는 남는다.** `_commit_guard()` 는 창을 좁힐 뿐이다.
   lock namespace 의 write authority 를 publisher 하나로 제한하는 구조는 미착수.
3. **roster 를 cohort lifetime 동안 immutable 로 만들지 않았다.** 지금은
   record seal 대조다. 42차 리뷰가 권한 "변경은 새 cohort ID 로만" 은 미착수.
4. **조건 1~4 의 RED 증거는 변이 시험이다** (§2 신고).
5. 실제 object-lock provider adapter · power-loss ordering fault model 은
   여전히 미구현·미착수다. 42차 Q5 답변대로 **별도 acceptance gate** 로 두되
   묶음 9 최종 완료 조건에는 포함된다고 이해했다.

---

## §5. 질문

1. **조건 1** — 42차 Q1 답변의 (b)+(c) 중 (c)를 했다 (취득~commit 을 한
   control flow 로, capability 를 인자로 안 받게). (b)(sentinel directory 를
   권한 경계로)는 이 저장소의 배포 형태에서 무엇을 뜻하는가 — 별도 uid/디렉터리
   권한을 요구하는가, 아니면 계약 문서에 신뢰 경계를 적는 것으로 충분한가?
2. **조건 2** — `_ledger_seal()` 은 cohort record 전체의 digest 다. 42차가
   권한 "roster immutable + 변경은 새 cohort ID" 로 가면 seal 대조는 중복이
   되는가, 아니면 둘 다 두는 것이 맞는가?
3. **조건 5** — A 가 임계 구역 **안**에서 barrier 를 치도록 내부 API
   (`_authority` + `_promote_cohort_locked`)를 subprocess 에서 직접 부른다.
   이것이 "production 경로를 지나지 않는 시험" 으로 보이는가, 아니면
   `promote_cohort_generation` 에 시험용 barrier hook 을 다는 편이 나은가?
4. **조건 8** — global 을 없앴으므로 guard 는 이제 **재발 방지**만 한다.
   이런 guard 를 계속 유지하는 것이 맞는가, 아니면 구조가 닫힌 뒤에는
   삭제하는 것이 최소주의에 맞는가?
5. **§4-4** — 한 구조 변경이 여러 조건을 함께 닫을 때, RED 증거를 변이로
   대체하는 것을 허용하는가? 아니면 조건마다 먼저 실패하는 시험을 요구하는가?
