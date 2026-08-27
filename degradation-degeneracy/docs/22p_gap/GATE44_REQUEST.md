# 44차 게이트 리뷰 요청 — 43차 P0 셋 + 증거·계약 넷 (인프라 2건 계속 신고)

```yaml
브랜치:     origin/claude/14-gate-code-review-9qkx05
대상 커밋:   8549d2596f41eee7aa1fd2affd5b558fd1ac7608
직전 대상:   09317986…      (43차, 조건 3·6·7·9 종결 / P0 셋 NO-GO)
source_digest: 9a18ed9776de34f3 → 1d0b9bde8e09792a
원장:       docs/08_REVIEW_RESPONSE.md §52
변이 재생:   python3 docs/22p_gap/mutation_replay.py  (--list · -k)
```

43차 판정을 수용한다. 조건 3·6·7·9 종결과 5·8 한정 통과 인정도 받았다.
43차가 준 **최소 조건 9개** 중 1~4(P0)와 5~8(증거·계약)을 아래에 적는다.
9(인프라 2건)는 계속 신고한다.

**P0-3 은 구현으로 닫지 않고 보장을 철회했다.** 그 판단의 근거를 §1 조건 4 에
적었고, 그것이 이번 라운드에서 가장 중요한 항목이다.

---

## §1. 조건별 대응

### 조건 1 — genuine authority + incomplete stage

**43차**: `_authority()` 가 genuine `_Authority` 를 caller 에게 그대로
`yield` 하므로, 위조도 registry 편집도 없이 이렇게 부를 수 있었다:

```python
with _PublishLock(out) as lock, _authority(lock, out) as auth:
    _promote_generation(incomplete_stage, auth)
```

exact suffix 와 `assert_cohort_complete()` 는 wrapper 에만 있었고 sink 는
leg **이름 집합**만 roster 와 대조했다. roster {a,b} 에
`{a.projection.yaml, b.projection.yaml}` 이면 seen legs 는 {a,b} 라 통과 —
publisher 가 reader 가 못 읽는 active state 를 만들 수 있었다.

**대응**: 되돌릴 수 없는 sink 가 **자기 불변식을 스스로** 본다.

```python
seen = {_leg_of(n) for n in files}
assert_cohort_complete(files, gid,
                       expect_legs=auth.roster if seen == auth.roster else None)
```

**자재화보다 먼저** 부른다 — 거부가 아무것도 남기지 않아야 하기 때문이다.
reader 와 **같은 validator** 하나를 쓴다 (36차에 이 사본을 "중복" 이라며
지웠던 것이 37차에 오판으로 판명된 그 자리다).

`_Authority` 는 `__setattr__` 로 고정 뒤 수정을 거부한다 (43차가 지적한
mutable slot).

**회귀**: `..._sink_refuses_an_incomplete_generation_with_a_genuine_authority`
— genuine `_authority()` + 두 축(active 경로: leg 집합은 맞고 suffix 가 깨짐 /
bootstrap 경로: leg 집합이 부분집합이고 suffix 도 깨짐). 둘 다 거부 ·
`CURRENT`·`.PENDING`·`gen/` 전부 불변. 그리고
`..._frozen_authority_cannot_be_edited_by_its_holder`.

> **신고 유지**: same-process hostile Python 에 대해 Python 객체·registry 는
> 보안 경계가 아니다. 이 수정이 닫는 것은 **불변식이 sink 밖에 있던 것**이다.

### 조건 2 — non-injective seal

**43차**: 원장은 `yaml.safe_load()`, seal 은 `json.dumps(..., default=str)`.
`legs: ["2026-08-28"]`(str) 과 `legs: [2026-08-28]`(date) 가 같은 seal 로
접혀 최종 guard 가 변경을 놓친다.

**대응**: `_assert_sealable()` — str/int/float/bool/None/list/dict 밖의 값은
**거부**한다 (`default=str` 삭제). 흡수하지 않는다.

**회귀**: `..._ledger_whose_types_differ_is_not_folded_into_one_seal[date_leg·date_scalar]`
— `legs` 안의 date 와 record scalar 의 date 를 각각 본다.

### 조건 3 · 4 — post-guard 창: **보장을 철회한다**

**43차**: guard 가 두 pointer 를 비교한 뒤 반환하고, 그 다음
`_publish_pointer()` 가 temp write·fsync·`os.replace` 를 한다. 그 사이에
다른 valid `CURRENT` 가 생기면 덮는다.

**할 수 있는 것은 했다**: `_write_pointer_tmp()` 로 temp write 를 분리하고,
대조를 **`os.replace` 직전**으로 내렸다. 남은 것은 마지막 syscall 앞 창이다.

**할 수 없는 것을 인정한다**: 43차 리뷰 Q1 답변대로, 이 창을 없애려면
별도 OS principal 이 `CURRENT`·`.PENDING`·`gen/`·`.publish.lock`·원장
namespace 의 create/rename/link/write 를 독점하거나 provider 의 원자적
conditional write 가 있어야 한다. 둘 다 이 저장소의 배포 형태 밖이다.

그래서 **강한 hostile-namespace 보장을 철회하고 전제를 계약에 적었다**:

- 계약: `STAGE3_CONTRACT.md` §13.3.1 (무엇을 철회했는지 · 무엇이 필요한지)
- 코드: `row_projection.py` 의 `_TRUST_BOUNDARY` (정본)

> **전제**: cohort 출력 디렉터리와 보존 원장은 **하나의 OS principal 이
> 소유**하고, 그 안에 쓰는 모든 writer 는 `promote_cohort_generation()` 을
> 지나 같은 게시 lock 을 따른다. 비협조적 writer 는 지원 범위 **밖**이다.

**이것은 구현 종결이 아니라 위협 모델 축소다.** 그렇게 부른다.

**회귀 둘**: `..._pointer_is_rechecked_immediately_before_the_rename`
(temp write 뒤·replace 앞 주입 → 거부) ·
`..._publisher_declares_its_trust_boundary` (코드 선언과 계약서가 함께
있는지 — 산문과 코드가 갈라지지 않게).

### 조건 5 — 두 publisher 모두 public lifecycle

**43차**: A 가 `_authority()`·`_promote_cohort_locked()` 를 직접 불렀다.

**대응 — 43차 Q3 답변 그대로**: production signature 에 hook 을 달지 않는다.
child process 에서 내부 임계 단계 하나를 **시험 전용 wrapper** 로 감싸
barrier 만 넣고, A·B **둘 다** `promote_cohort_generation()` 을 부른다.

### 조건 6 — `RetentionProof.until` 과 content/journal 결속

**43차**: `until` 이 반환만 되고 아무도 안 본다. content exact-ID 와 journal
field 를 직접 assert 하지 않는다.

**대응**: orchestration 경계에서 `proof.until == lease["retain_until_utc"]`
를 못 박는다. 그리고 `..._journal_seals_the_content_proof_the_repair_produced`
— `after_pin_lock` 창에서 재개해 journal 의 `lease_content_version` 이
수리가 만든 exact ID 와 같고, 그 ID 가 실제 Compliance·기한 충족인지 본다.

### 조건 7 — per-candidate 로 범위를 좁힌다

**43차 지적을 수용한다.** "실패 시 transaction 전체 irreversible mutation 0"
은 거짓이다 — orchestration 이 lease pin 을 먼저 잠그므로 content 단계에서
실패해도 valid pin lock 은 남는다 (복구 가능한 중간 상태다).

조건 7 의 범위를 **candidate version 단위**로 못 박는다: *검증되지 않은
candidate version 을 WORM-lock 하지 않는다.* 원장 §52 와 요청문에서 그렇게만
주장한다.

### 조건 8 — warm: **blacklist 를 지웠다**

**43차**: `DOCS / "22p_gap" / "warm_probe"` 재구성과 closure introspection 이
남는다. AST blacklist 를 structural confinement 의 증명으로 세면 안 된다.

**대응 — 43차 Q4 답변 그대로 삭제했다.** `_warm_offenders()` 와 그
parametrize 시험 넷을 지웠다. 39~43차에 걸쳐 `BinOp` → 이름 load → module
scope → attribute·lambda → 문자열 상수로 네 번 넓혔고 매번 새 철자가 나왔다.

남기는 회귀 둘:

1. `..._warm_root_is_not_a_module_global` — 그 global 이 없다
2. `..._warm_consumers_go_through_the_accessors` — 현행 소비자가 accessor
   셋을 부르고, `"warm_probe"` 문자열이 accessor factory 밖에 없다

이름을 **"현행 소비자 API hardening"** 으로 정확히 붙였다. structural
confinement 의 증명이 아니다.

### 조건 9 — 인프라 2건

실제 object-lock provider adapter · power-loss ordering fault model 은
**미구현·미착수**다. 43차 Q5 답변대로 별도 acceptance gate 로 두되 묶음 9
최종 완료 조건에는 포함된다고 이해한다.

---

## §2. 변이 재생 artifact (43차 요구)

`docs/22p_gap/mutation_replay.py` — mutant **19개**를 저장소에 둔다.
RUN_SCOPE 밖(`docs/`)이라 code identity 를 움직이지 않는다.

```
python3 docs/22p_gap/mutation_replay.py --list   # 목록
python3 docs/22p_gap/mutation_replay.py -k warm  # 이름으로
python3 docs/22p_gap/mutation_replay.py          # 전부
```

각 항목은 (불변식 이름, 파일, 되돌릴 조각, 되돌린 값, 빨개져야 하는 `-k`) 이고
실행은 원본을 `finally` 로 복원한다. 2-site 변이(심층 방어라 하나만 지우면
다른 하나가 가리는 축)는 따로 둔다.

**관측되지 않는 둘을 신고한다** (`DECLARED_MASKED`):

| mutant | 왜 안 물리나 |
|---|---|
| `proof-until-equals-lease` | horizon 정본은 lease record 이고 verifier 가 exact ID 로 다시 확인한다. 이 assert 는 필드가 이름만 갖지 않게 하는 계약이며 현재 production 경로에 갈라지는 반례가 없다 |
| `warm-consumer-wiring` | positive wiring 회귀는 **배선이 끊길 때** 빨개진다. 그 assert 를 지우는 변이는 자기 시험만 무력화한다 — 회귀의 성질이지 결함이 아니다 |

**이번에 합친 것**: `sink-exact-suffix` 와 `sink-completeness` 를 따로
두었더니 서로를 가려 둘 다 안 물었다. 두 검사가 같은 것을 말하고 있었으므로
`assert_cohort_complete()` 한 번으로 합쳤다 — 합친 뒤 `sink-validates-itself`
가 문다.

---

## §3. 실측 증거 (대상 커밋에서 방금)

```
$ python -m pytest tests/ -q
1155 passed, 1 xfailed in 316.08s (0:05:16)

$ ./scripts/smoke_e2e.sh
✅ pipeline smoke 통과
⚠ 보존 gate 미완료 (계약 v4 묶음 9) — 새 leg 실행 금지.

$ python3 docs/22p_gap/mutation_replay.py
(19 mutant · 17 물었다 · 2 신고)

$ python3 docs/22p_gap/row_projection.py paired_fixed5_v4 --cohort g2_2026_08_25
✅ paired_fixed5_v4: 6138행 · restart 30690행 · proj ad598fe77e75afec ·
   전체 True · by_obj True · fits삼중 True · 봉인일치 True

$ python3 docs/22p_gap/make_receipt.py paired_fixed5_v4 --check
✅ paired_fixed5_v4: core 재생성 바이트 동일 · core_sha 01c241a5b77766de

$ python wiki/tools/lint.py
RESULT: 0 errors

$ git status --short
(비어 있음)
```

| 축 | 43차 | 44차 |
|---|---|---|
| `source_digest` | `9a18ed9776de34f3` | `1d0b9bde8e09792a` |
| g2 `compute_sha256` | `94c5e825cdce8fc7` | `4217202487faf775` |
| g2 `row_projection_py_sha256` | `934fda4a9c4e74a3` | `510738beea9729ab` |
| receipt `core_sha256` | `f22116328335d8c7…` | `01c241a5b77766de…` |
| **투영 행 바이트** | `ad598fe77e75afec` | **`ad598fe77e75afec`** (불변) |

---

## §4. 스스로 신고하는 것

1. **P0-3 은 구현으로 닫지 않았다.** 보장을 철회하고 전제를 계약에 적었다
   (§1 조건 3·4). 위협 모델 축소이지 구현 종결이 아니다.
2. **조건 7 의 범위를 좁혔다** — per-candidate 보장이지 transaction 전체
   zero-side-effect 가 아니다 (43차 지적 수용).
3. **조건 8 은 현행 소비자 API hardening 이다** — structural confinement 의
   증명이 아니다 (43차 지적 수용).
4. **변이 둘은 관측되지 않는다** (§2 표).
5. roster immutable + `CURRENT` 에 cohort ID·원장 record digest 봉인
   (43차 Q2 답변의 설계) 은 **미착수**다.
6. 실제 provider adapter · power-loss fault model 은 여전히 미구현·미착수다.

---

## §5. 질문

1. **조건 3·4** — 보장 철회를 택했다. 계약 §13.3.1 의 전제 문구와 그 범위가
   충분한가? 배포 acceptance 에서 무엇을 더 확인해야 하는가 (디렉터리 소유자·
   퍼미션 검사를 smoke 에 넣는 것이 맞는가)?
2. **조건 1** — sink 가 reader 와 같은 validator 를 부르는 형태로 닫았다.
   `_authority()` 를 caller 에게 노출하지 않는 구조(closure 소유)까지
   가야 하는가, 아니면 "sink 가 스스로 검증한다" 로 충분한가?
3. **43차 Q2 설계** — roster immutable + `CURRENT` 에 cohort ID·원장 digest
   봉인. 이것을 묶음 9 종결 조건에 넣는가, 아니면 묶음 10(cohort dispatch)
   으로 옮기는가?
4. **변이 artifact** — `mutation_replay.py` 의 형태가 요구를 만족하는가?
   실패 log 를 저장소에 함께 커밋해야 하는가 (재생 가능하면 불필요하다고
   보는데, 판단을 구한다)?
5. **인프라 gate** — 실제 provider adapter acceptance 를 시작할 때 무엇이
   먼저 필요한가: adapter 구현 → fake 와 같은 계약 시험 → 실물 bucket?
   아니면 계약 시험을 먼저 쓰고 adapter 를 그것에 맞추는가?
