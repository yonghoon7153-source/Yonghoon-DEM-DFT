# 55차 게이트 리뷰 요청 — 묶음 9 (실행 전 승인 · 보존 lifecycle)

**대상 커밋**: `TBD` (브랜치 `claude/14-gate-code-review-9qkx05`)
**직전 판정**: 54차 **NO-GO** — P0 5묶음 · P1 2건

---

## §0 먼저 — 이번 라운드가 **하지 않은** 것

| 조건 | 상태 |
|---|---|
| 54차 조건 — 실행되는 source bytes 를 **trusted launcher** 가 측정 | **미착수** (54차에도 신고했다) |
| **P0-1** producer 결속 — 닫힌 typed manifest 파싱 · 두 payload 압축해제 재해시 · producer 발행 영수증 | **미착수** (49차부터 **일곱 라운드째**) |
| **P0-8** 경로 무관 typed·sealed 실행 class marker | **미착수.** 판정은 여전히 경로 기반 격리 |
| **P0-4** typed CAS/archive/restore/validation/retention 영수증 **소비** | **부분** |
| 변이 증거의 **독립 replay** | **미착수** — 55차는 증거를 시험한 트리에 묶었을 뿐, checker 가 스스로 재생하지는 않는다 |
| baseline·sweep1d·wsweep 계획 gate · 실물 object-lock adapter · power-loss 모델 · publisher 전용 OS principal · 외적타당도 #48/#49/#50 | **미착수** |

54차 GO 최소 조건 7개 중 이번에 한 것은 1~7 **전부**(즉 반례 전부)이지만,
위 표의 항목들은 그와 **별개의 독립 전제**로 남아 있다는 54차 판정문의 마지막
문단에 동의한다.

**남아 있는 표면** (54차 신고분 + 이번 라운드에 새로 확인한 것):

- 원장·journal·anchor·`.FROZEN` **전부**에 쓸 수 있는 주체는 역사를 다시 쓸 수 있다.
- 소유 증명 token 파일(0600)은 같은 uid 의 다른 process 가 읽을 수 있다.
- 변이 증거의 **pytest report 자체를 손으로 위조**하면 checker 를 통과한다.
- `_through_bind_mounts()` 는 `/proc/self/mountinfo` 를 읽는다 — 그 파일을 못 읽는
  환경(비 Linux · 제한된 컨테이너)에서는 **푸는 것이 없다**. 그때는 54차 상태와
  같아진다 (fail-open 이다 — 아래 §3-2 에서 반증해 주기 바란다).
- symlink 원장을 **재지정**하면 claims root 는 여전히 움직인다. 55차가 닫은 것은
  원장이 **자기 쓰기로** 그것을 움직이던 경로다.
- lock 은 여전히 같은 파일시스템의 `flock` 이다.

---

## §1 54차 반례 7건 — 전부 재현한 뒤 고쳤다

| # | 54차 반례 | 재현 | 고친 자리 |
|---|---|---|---|
| P0-1 | 정상 finalize 가 공용 token 경로의 **새** 소유 증명을 지운다 | ○ | 정상 경로도 `_lifecycle_locks()` — `attempt_path → claim → ledger` 를 검증·commit·삭제가 끝날 때까지 유지 |
| P0-2 | 같은 `ledger` 인자가 **자기 쓰기 뒤** 다른 claims root | ○ | `canonical_ledger()` 신설 — 원장 해석 7자리를 1자리로 (그 1은 함수 자신) |
| P0-3 | stale anchor repair 가 `.head` 를 과거로 되돌린다 | ○ | `_lifecycle_lock()` 신설 — journal·`.head` 에 lock 이 **하나도** 없었다. 읽기와 쓰기가 같은 임계 구역 |
| P0-4 | frozen tree 의 **자식**을 bind mount 하면 새 이름으로 게시된다 | ○ | `_through_bind_mounts()` — 목적지를 mount 관계로 풀고 **조상까지** marker 를 본다 |
| P0-5① | 역방향 alias(`ALIAS = BOX`)가 producer 닫힘에서 빠진다 | ○ | module-level `Expr` 를 예약 이름 `MODULE_EFFECTS` 에 묶어 두 닫힘 walk 의 seed 에 **무조건** 넣는다 |
| P0-5② | `getattr(f, *[...])` · `[...][0]` · 변수 가 dunder 검사를 우회 | ○ | 이름 인자 식에서 **정적으로 읽히는 문자열**(중첩 리터럴·module 상수 경유)을 모아 같은 규칙 |
| P1-1 | freeze 가 거부하기 **전에** 부작용을 남긴다 | ○ | `_assert_dest_inside_repo()` 를 첫 쓰기 앞 + ledger lock 안에서 재확인 |
| P1-2 | coverage 의 `head` 결속이 "실재하는 commit" 이면 통과 | ○ | `_tested_tree_digest()` — checker 가 **지금 트리**와 대조 |

### 이번 라운드의 형태 둘

**① 규칙을 한 자리에 두지 않으면 남은 중복 구현이 곧 반례다.** 54차는
"authority 가 둘이면 그 사이가 구멍이다" 를 배우고 네 곳을 합쳤는데, **합치다
만 곳**이 이번 P0-1 이다 (복구 분기만 옮기고 정상 경로를 남겼다). P0-2 도 같다 —
"자리는 원장이 정한다" 로 모았으면서 **그 원장을 무엇으로 해석하는가** 는 두
벌이었다.

**② 이름 계층에 없는 것은 이름으로 못 잡는다.** P0-4 에서 실측했다:

```
os.path.ismount(alias) = False    (같은 파일시스템 bind 는 안 잡힌다)
os.path.realpath(alias) = alias   (bind 는 안 풀린다)
alias 의 st_ino == 원본의 st_ino  (같은 tree 다)
```

52차가 marker 를 tree **안**에 둔 것은 옳았지만, 리뷰어는 marker 가 **없는
자식**을 bind 했다. 이름을 몇 겹 만들든 mount 관계는 커널이 알고 있으므로 그것을
읽는다. P0-5① 도 같은 형태다 — 별칭 겹수는 이름 추적으로 못 이기므로 방향을
뒤집어 **무조건 포함**으로 갔다.

---

## §2 증거

### 2-1 전체 회귀 — `TBD`

### 2-2 strict smoke — `TBD`

### 2-3 변이 전수 — 등록부 **165 scenario** (executable 157 · declared 8)

157 → 165. 55차 방어 8건을 등록했고, 55차 수정으로 원문이 움직인 낡은 preimage
4건을 갱신했다 (`--check-preimages` 가 그것을 먼저 잡았다).

**전수 재생 결과의 정본은 커밋된 증거 파일이다** —
`docs/22p_gap/mutation_coverage/s1..s12.json` 과 그 옆의 `reports/`.

### 2-4 이번 라운드에 변이가 잡은 것 셋 — **하나는 내가 조용히 약화시킨 자리였다**

**① P0-1 의 첫 재현 시험이 거짓 초록이었다.** hook 을
`_unlink_token_generation()` 에 걸었더니 그 함수의 generation 검사가 먼저 막았다.
창은 그 함수 **안**(비교 → `unlink` 사이)이므로 `Path.unlink` 를 hook 해야 진짜
RED 가 났다.

**② `ledger-is-resolved-once` 가 약한 시험이었다.** `.resolve()` 를 지우는 변이를
걸면 전후가 똑같이 *틀린* 곳을 가리켜 "안정적" 이 되고, 무는 것은 곁가지
단언뿐이었다. 반례의 본질인 **"같은 실제 원장을 가리키는 서로 다른 이름이 다른
claims root 를 준다"** 를 못 박아 그 축에서 물게 했다.

**③ P0-5① 을 고치면서 `raise SystemExit` fail-closed 분기 하나를 지웠는데 아무
시험도 빨개지지 않았다.** 54차 시험은 같은 fixture 의 `_f()['tol'] = 1` 이 **53차
컨테이너-대입 분기**에서 대신 걸려 계속 초록이었다 — 옛 규칙이 대신 잡으면 그
시험은 아무 것도 증명하지 않는다. 변이 재생이
`module-expr-binds-its-target` 이 안 문다고 알려주면서 드러났다.

실측해 확인했다: 뿌리를 정할 수 없는 표현식(`_f().update(tol=0.02)`)이 이제
digest 를 움직인다 (`d43c0e39…` → `3f0e1af2…`). `MODULE_EFFECTS` 가 그 문을
무조건 담으므로 **멈추는 대신 담는** 더 강한 상태다. 다만 그것은 *확인한 뒤에*
할 말이지 그냥 지나갈 일이 아니었다. 시험을 새 보장에 맞추고
(`module_scope_expression_statement_is_fail_closed` 가 이제 "뿌리를 정할 수 없는
표현식도 digest 를 움직이는가" 를 본다), scenario 를 **declared** 로 옮겨
사유를 적었다.

### 2-5 산출물 — g9 을 얼리고 g10 으로

| 값 | 54차 (g9) | 55차 (g10) |
|---|---|---|
| `producer_semantic_sha256` | `d4c3dc8ff856d31a` | `effc3eef2e23fabd` |
| `compute_sha256` | `b12e9ff10385169e` | `0f59ad72af31703e` |
| `row_projection_py_sha256` | `b99dee231d0f170e` | `969916b10e845036` |
| 영수증 core_sha | `77235418c8f3e8e8…` | `2fd81e7015a279bb…` |
| validator identity | `7b968b9bf0965402` | `82aeae57631f6c0c` |
| 투영 | `proj_g9` | `proj_g10` |

**행 바이트는 안 움직였다** — 재생성 출력이 `proj ad598fe77e75afec` 로 g4~g9 과
동일하다 (6138행 · restart 30690행 · 전체 True · 봉인일치 True). 움직인 것은
identity 의 **정의**다. 그래도 cross-cohort 비교는 금지다.

---

## §3 무엇을 반증해 주기 바라는가

우선순위 순. **§0 에 신고한 것을 다시 적는 것은 이미 아는 사실의 재확인이다.**

1. **합치다 만 자리.** `_lifecycle_locks()` 를 **안 지나는** lifecycle mutator,
   또는 셋 중 일부만 잡는 경로가 또 있는가. 같은 물음을 `canonical_ledger()` 와
   `_lifecycle_lock()` 에도 — 해석·잠금이 두 벌인 자리가 남았는가.
2. **mount 해석의 fail-open.** `/proc/self/mountinfo` 를 못 읽으면
   `_through_bind_mounts()` 는 아무 것도 풀지 않고 그대로 돌려준다. 그 상태에서
   P0-4 반례가 되살아나는가. 겹친 mount·`--rbind`·mount namespace 분리로 해석을
   어긋나게 만들 수 있는가 (반복 상한 16회를 넘기는 구성 포함).
3. **producer 닫힘.** `_static_strings()` 가 못 보는 경로로 dunder 이름을
   건네는 자리 (dict 값·클래스 속성·f-string 조립·`chr()` 연결 등). 반대로
   너무 넓어 producer 자신의 정규형 코드를 막는 자리.
4. **`MODULE_EFFECTS`.** 예약 이름과 실제 소스의 이름이 충돌할 수 있는가.
   module-level 표현식이 닫힘에 들어오면서 게시 코드가 producer identity 로
   끌려 들어온 곳은 없는가 (절단면이 조용히 넓어졌는가).
5. **lifecycle lock.** `_lifecycle_lock()` 과 원장 lock·게시 lock 사이의 순서에
   순환이 있는가. 수리와 동결이 겹치는 다른 schedule.
6. **증거.** `_tested_tree_digest()` 가 세는 파일 집합이 실제로 시험한 코드와
   다른 경우 (변이 대상 3파일 + 기대 실패 시험 파일 밖에서 결과가 바뀌는 경로).
7. **거부하면서 남기는 기록.** freeze 말고 다른 경로에도 같은 형태가 있는가.
8. **순서 결함.** 부작용·판정 순서가 뒤바뀐 다른 자리.

---

## §4 검증 명령

```
python -m pytest tests/ -q
./scripts/smoke_e2e.sh
python3 docs/22p_gap/mutation_replay.py --check-preimages
python3 docs/22p_gap/mutation_replay.py --slice I/12 --emit-coverage docs/22p_gap/mutation_coverage/sI.json
python3 docs/22p_gap/mutation_replay.py --check-coverage docs/22p_gap/mutation_coverage/s*.json
python -m pytest tests/test_lifecycle_e2e.py -q
```

원자료(`results/`)는 gitignored 이므로 clean checkout 에서는 artifact 대조가
계산 불가로 실패할 수 있다. 지원 인터프리터가 하나뿐인 환경에서는 정규형 일치
회귀 2건이 `len(seen) >= 2` 로 실패한다. P0-4 회귀는 bind mount 를 만들 수 없는
환경에서 skip 한다. 셋 다 알려진 환경 한계다 — 다만 **환경 한계로 보이는 실패가
사실은 순서·fail-open 결함**일 수 있다는 것이 50차에 실측됐으니 한 번은 의심해
주기 바란다.
