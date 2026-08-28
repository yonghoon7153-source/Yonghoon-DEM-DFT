# 45차 게이트 리뷰 요청 — 44차 P0 넷 + 조건 5~10 (인프라 2건 계속 신고)

```yaml
브랜치:     origin/claude/14-gate-code-review-9qkx05
대상 커밋:   2a696eac25df3a2b230326b0917b2d93468d366d
직전 대상:   8549d259…      (44차, 조건 1·2·5·6·7·8 좁게 인정 / P0 넷 NO-GO)
source_digest: 1d0b9bde8e09792a → ae4d82faf6c2281f
원장:       docs/08_REVIEW_RESPONSE.md §53
변이 재생:   python3 docs/22p_gap/mutation_replay.py  (--list · -k)
```

44차 판정을 수용한다. 11개 최소 조건 중 1~10 을 아래에 적고 11(인프라)은 계속
신고한다. **10번(roster immutable + pointer 의 원장 결속)까지 했다** — 44차
리뷰가 그것을 묶음 9 종결 조건이라고 했기 때문이다.

44차가 짚은 병은 하나다: **막았다고 부른 것의 가장자리.** 동결은 재대입만,
alias 는 `is_file()` 만, seal 은 date 만 봤다.

---

## §1. 조건별 대응

### 조건 1 — deep immutable authority

**44차**: `__setattr__` 동결은 **얕다**. `auth.roster` 가 mutable `set` 이라
`roster.clear(); roster.add("evil")` 는 동결을 아예 지나지 않는다.

**대응**: 담기는 값 자체를 immutable 로 — `roster` 는 `frozenset`,
pointer snapshot 은 `bytes`, 나머지는 `str`. sink 가 쓰지 않던 mutable
`cohort` snapshot 은 **제거**했다 (근거는 `seal` 이다).
`auth.frozen_values()` 가 그 성질을 스스로 확인한다.

**회귀** `..._frozen_authority_holds_only_immutable_values` — genuine
authority 로 `roster.add()` 를 시도하고(`AttributeError`), `evil` 세 파일
stage 를 sink 에 넘겨 거부·pointer 불변을 본다.

### 조건 2 — `seen <= roster` 를 모든 경로에서

**44차**: sink 는 `seen == roster` 일 때만 명부를 대조했다. complete 한
**undeclared** leg(`evil.*` 세 파일)가 `.PENDING` 으로 게시돼 다음 publisher
를 막았다.

**대응**: 부분집합 검사를 **모든 경로**에서. equality 는 active/pending
**선택**에만 쓴다.

**회귀** `..._complete_undeclared_leg_never_reaches_pending`.

### 조건 3 — stage/gdir alias

**44차**: 현재 active `gen/<gid>` 를 stage 로 주면 idempotent 분기가 그것을
자기 자신과 비교한 뒤 `rmtree` 로 **지우고**, 같은 gid 를 다시 게시했다.
public API 만으로 성립했다.

**대응**: `_staging_entries()` 가 `resolve()` 로 staging 이 generation
namespace 안(또는 목적지 자신)인지 보고 거부한다.

**회귀** `..._current_generation_cannot_be_used_as_its_own_staging`.

### 조건 4 — owned files 로 자재화

**44차**: `is_file()` 이 symlink 를 따라가고, staging 디렉터리를 통째로
`shutil.move` 했다. 게시 뒤 바깥 target 을 고치면 "immutable" generation
바이트가 바뀐다. directory·FIFO·broken link 도 이동에 딸려갔다.

**대응** — 44차 리뷰가 준 다섯 단계 그대로:

1. `lstat` 으로 **따라가지 않고** 열거하고 regular·`st_nlink == 1` 만 허용
2. `O_NOFOLLOW` 로 열어 바이트를 읽는다
3. caller 디렉터리를 **옮기지 않고** `O_CREAT|O_EXCL|O_NOFOLLOW` 로 **새
   inode** 에 쓴다 (`_write_owned`)
4. 만든 것을 **되읽어** 이름·바이트가 staging 과 같은지 확인
5. directory fsync → generation commit → pointer

**회귀 둘**: `..._staging_aliases_never_become_an_immutable_generation[symlink·hardlink·extra_dir]`
(거부 · CURRENT 없음) · `..._a_published_generation_owns_its_bytes`
(게시된 파일이 regular·nlink==1 이고 **staging 과 다른 inode**).

### 조건 5 — exact JSON domain

**44차**: `isinstance(node, (list, tuple))` 이 tuple 을 허용했다. PyYAML 의
표준 `!!omap` 은 list[tuple] 이고 `json.dumps` 는 tuple 과 list 를 같은
JSON array 로 접는다 — 서로 다른 typed record 가 같은 seal 이 된다. NaN·
Infinity 도 통과했다.

**대응**: `isinstance` → **`type(...) is`**. tuple·subclass·비유한수 거부,
`json.dumps(..., allow_nan=False)`.

**회귀 둘**: `..._seal_domain_is_exact_not_isinstance[omap·nonfinite·date_key]` ·
`..._an_omap_and_a_list_of_lists_do_not_share_a_seal` (한쪽이 fail-closed).

### 조건 6 — 계약 문구 정정

44차가 지적한 과장 둘을 **걷어냈다** (계약 §13.3.1 · 코드 `_TRUST_BOUNDARY`):

| 44차 문구 | 45차 정정 |
|---|---|
| "전제가 깨져도 **탐지**는 된다" | 마지막 창은 **탐지되지도 않는다** |
| "generation 이 immutable 하므로 잃은 pointer 는 복구 가능" | **바이트 보존**은 되고 **정본 pointer 복구는 안 된다** — durable commit journal 도 기대 pointer digest 도 없다 |

그리고 §13.3.1.1 을 새로 두어 **배포 점검이 증명하는 것과 못 하는 것**을
적었다: 소유자·퍼미션 점검은 **cooperative-local 설정 점검**이며 cooperative
behavior 를 증명하지 못한다 (같은 principal 의 코드는 퍼미션을 지나가고
uid 0 에서는 mode bit 가 잠금이 아니다). 강한 enforcement 는 publisher 전용
service principal 과 negative canary 가 필요하고 **미착수**다.

**회귀** `..._publisher_declares_its_trust_boundary` 가 문구별로 확인한다.

### 조건 7 — strict mutation runner

**44차**: 모든 nonzero pytest 종료를 "물었다" 로 셌고 scenario 수도 단위를
섞었다.

**대응** — runner 가 node 단위로 다음을 전부 확인한다:

| 축 | 확인 |
|---|---|
| 선택 | `--collect-only` 로 **정확한 node ID 목록** (없으면 실패) |
| baseline | 그 node 들이 **전원 PASS** |
| 변이 뒤 | 실패가 **call 단계**여야 한다 |
| 오류 | setup/teardown/collection·internal 오류가 있으면 **실패** |
| 원복 | 복원 뒤 **바이트 해시 동일** |
| 의존 | `pytest-json-report` 가 없으면 조용히 넘어가지 않고 **실패** |

**이번 집계**: `scenario 31 · 실행 28 · 신고 3 · site 29`.
(44차의 `19/17/2` 는 단위를 섞은 숫자였다 — 리뷰 지적 수용.)

이번에 다섯이 걸렸다: **지점 불량 셋**(내가 코드를 고치고 mutant 를 안 고쳤다
— 44차 runner 였다면 조용히 통과했을 것이다), `pointer-binds-the-cohort-id`
는 seal 이 이미 덮는 **중복**이라 그 코드를 지웠고, `guard-before-commit` 은
`-k` 가 좁았다.

### 조건 8 — public-lifecycle · warm wiring 증거

- **두 publisher**: child 가 `promote_cohort_generation` 을 지날 때 **marker
  파일**을 남기고, 시험이 A·B 둘의 marker 와 **최종 exact bytes** 여섯 개를
  확인한다.
- **warm**: 44차는 accessor 이름이 파일 어딘가에서 불리는지만 봤다. 이제
  **소비자별로 매핑**하고, 선언된 소비자를 **실행하면서 accessor spy** 가
  실제로 불리는지 본다.
- mutant `warm-consumer-uses-accessor` 가 소비자 하나를 direct path 로
  되돌리면 그 시험이 빨개진다.

### 조건 9 — falsy/비문자열 VersionId

**44차**: `get(key, version)` 은 version 이 falsy 면 **head lookup** 이 된다.
그러면 read-back 이 head 를 읽어 통과하고, 그 사이 head 가 바뀌면 남의
version 을 잠근다.

**대응**: `put` 반환이 nonempty `str` 이 아니면 **read-back 전에** 거부.

**회귀** `..._a_falsy_version_id_from_put_is_refused[None·""·0]`.

### 조건 10 — roster immutable + pointer 의 원장 결속

44차 리뷰 Q3 답변대로 **묶음 9 종결 조건으로 넣었다.**

- `CURRENT`·`.PENDING` 이 게시 당시의 **게시 authority** 를 봉인한다:
  `_LEDGER_AUTHORITY = ("cohort_id", "dir", "status", "legs")`
- **reader(`read_current()`)도** 그 봉인값을 지금의 원장과 대조한다
- 넷 중 하나라도 바뀌면 그 cohort 의 기존 pointer 는 authority 가 아니다 →
  **새 cohort ID 와 새 출력 디렉터리**로 간다 (계약 §13.3.2)

**봉인 범위를 record 전체가 아니라 authority 네 필드로 좁힌 이유**: 이
저장소의 원장 record 는 `pin`·`runtime` 같은 **기록용 bookkeeping** 을 함께
담고 그것은 라운드마다 바뀐다. 전체를 봉인하면 pin 을 갱신하는 순간 이미
게시된 pointer 가 전부 무효가 된다 — **실측했다.** 44차 리뷰가 예고한
"비권위 필드로 축소하려면 먼저 closed authoritative field schema 와 계약
문구를 바꾸라" 를 그대로 했다.

**회귀 둘**: `..._expanding_a_roster_over_an_active_cohort_requires_a_new_cohort`
(명부를 넓힌 뒤의 게시는 거부) · `..._a_fixed_roster_still_accumulates_to_completeness`
(40차가 고친 **같은 명부 안에서의 누적**은 그대로 동작한다).

40차 시험 `..._reaches_completeness` 는 이 규칙 아래 **의미가 뒤집혔으므로**
이름과 내용을 바꿨다 (숨기지 않는다).

### 조건 11 — 인프라 2건

실제 object-lock provider adapter · power-loss ordering fault model 은
**미구현·미착수**. 44차 Q5 답변의 순서(계약 시험 → fake 검증 → adapter →
실물 acceptance)를 받아들인다.

---

## §2. 실측 증거 (대상 커밋에서 방금)

```
$ python -m pytest tests/ -q
1170 passed, 1 xfailed in 299.25s (0:04:59)

$ python3 docs/22p_gap/mutation_replay.py
scenario 31 · 실행 28 · 신고 3 · site 29
실행한 변이가 전부 기대 node 를 call 단계에서 물었다

$ ./scripts/smoke_e2e.sh
✅ pipeline smoke 통과
⚠ 보존 gate 미완료 (계약 v4 묶음 9) — 새 leg 실행 금지.

$ python3 docs/22p_gap/row_projection.py paired_fixed5_v4 --cohort g2_2026_08_25
✅ paired_fixed5_v4: 6138행 · restart 30690행 · proj ad598fe77e75afec ·
   전체 True · by_obj True · fits삼중 True · 봉인일치 True

$ python3 docs/22p_gap/make_receipt.py paired_fixed5_v4 --check
✅ paired_fixed5_v4: core 재생성 바이트 동일 · core_sha bff345f6b2f1a12b

$ python wiki/tools/lint.py
RESULT: 0 errors

$ git status --short
(비어 있음)
```

| 축 | 44차 | 45차 |
|---|---|---|
| `source_digest` | `1d0b9bde8e09792a` | `ae4d82faf6c2281f` |
| g2 `compute_sha256` | `4217202487faf775` | `ea7a0c1964eb4c3f` |
| g2 `row_projection_py_sha256` | `510738beea9729ab` | `38749bd2def6f98e` |
| receipt `core_sha256` | `01c241a5b77766de…` | `bff345f6b2f1a12b…` |
| `CURRENT` schema | `projection-current/v1` | `projection-current/v2` (cohort·원장 결속) |
| **투영 행 바이트** | `ad598fe77e75afec` | **`ad598fe77e75afec`** (불변) |

`proj_g2/CURRENT` 는 새 schema 로 **재게시**했다 (옛 v1 pointer 는 새 계약을
만족할 수 없다). generation directory 는 건드리지 않았다.

---

## §3. 스스로 신고하는 것

1. **`os.replace` 직전~직후 창**은 전제로 배제한다. 탐지도 복구도 안 된다
   (계약 §13.3.1 — 44차의 과장 둘을 걷어냈다).
2. **publisher 전용 principal · negative canary** 는 미착수다. 배포 점검은
   `cooperative-local 설정 점검` 이며 enforcement 증명이 아니다.
3. **변이 셋은 관측되지 않는다** (`mutation_replay.py` 의 `DECLARED_MASKED`).
4. **40차 시험 하나의 의미가 뒤집혔다** — roster 확장이 이제 거부다.
   이름과 내용을 바꿔 적었다 (§1 조건 10).
5. 실제 provider adapter · power-loss fault model 은 여전히 미구현·미착수다.

---

## §4. 질문

1. **조건 10** — 봉인 범위를 authority 네 필드로 좁혔다. 이 schema 가
   충분한가? `dir` 을 넣었는데 원장의 `dir` 은 repo 상대 경로다 —
   resolved path 로 봉인해야 하는가?
2. **조건 4** — generation 을 owned files 로 만들면서 caller staging 을
   `rmtree` 로 지운다. staging 소유권이 caller 에게 있다고 보고 **지우지
   않는** 편이 나은가 (지금은 44차 이전 동작을 유지했다)?
3. **조건 7** — runner 가 `pytest-json-report` 에 의존한다.
   `requirements*.txt` 에 넣어야 하는가? (RUN_SCOPE 안이라 code identity 가
   움직인다 — 그래서 아직 안 넣었다.)
4. **조건 6** — 배포 점검을 smoke 에 넣을지 여부는 아직 안 정했다. 넣는다면
   무엇을 확인하는 것으로 이름 붙여야 하는가?
5. **묶음 9** — 조건 10 까지 닫혔다면, 남은 것은 §3 의 1~2(설계·운영)와
   인프라 2건인가? 아니면 아직 publication 축에 더 있는가?
