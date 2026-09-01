# 54차 게이트 리뷰 요청 — 묶음 9 (실행 전 승인 · 보존 lifecycle)

**대상 커밋**: `TBD` (브랜치 `claude/14-gate-code-review-9qkx05`)
**직전 판정**: 53차 **NO-GO** — P0 6묶음 · P1 4건

---

## §0 먼저 — 이번 라운드가 **하지 않은** 것

| 조건 | 상태 |
|---|---|
| 53차 조건 5 — 실행되는 source bytes 를 **trusted launcher** 가 측정 | **미착수.** P0-5③ 의 decoy 반례는 절단면을 좁혀 닫았지만 경계 자체는 P0-8 과 같은 자리다 |
| **P0-1** producer 결속 — 닫힌 typed manifest 파싱 · 두 payload 압축해제 재해시 · producer 발행 영수증 | **미착수** (49차부터 **여섯 라운드째**) |
| **P0-8** 경로 무관 typed·sealed 실행 class marker | **미착수.** 판정은 여전히 `is_inside_namespace()` 의 경로 기반 격리 |
| **P0-4** typed CAS/archive/restore/validation/retention 영수증 **소비** | **부분** |
| 변이 증거의 **독립 replay** | **미착수** — 표식(§2-4)은 donor relabel 을 막을 뿐, checker 가 스스로 재생하지는 않는다 |
| baseline·sweep1d·wsweep 계획 gate · 실물 object-lock adapter · power-loss 모델 · publisher 전용 OS principal · 외적타당도 #48/#49/#50 | **미착수** |

53차 리뷰어의 GO 최소 조건 7개 중 이번에 한 것은 1~4·6·7 이다 (즉 반례 전부).
5(trusted launcher)는 시작하지 않았다. 51·52·53차가 세 번 권고한 순서
(① 단일 transaction ② P0-8 sealed execution manifest ③ P0-1 producer receipt)
에서 이번 라운드는 ①을 **원장 하나가 정하는 authority** 수준까지 밀었고 ②·③ 은
그대로다 — 그리고 그것이 **GO 를 막는 축**이라는 판단에 계속 동의한다.

**남아 있는 표면** (53차 신고분 + 이번 라운드에 새로 확인한 것):

- 원장·journal·anchor·`.FROZEN` **전부**에 쓸 수 있는 주체는 역사를 다시 쓸 수 있다.
- 소유 증명 token 파일(0600)은 같은 uid 의 다른 process 가 읽을 수 있다.
- 변이 증거의 **pytest report 자체를 손으로 위조**하면 checker 를 통과한다 (§2-4).
- `freezing` 은 원장 한 필드다 — 원장에 쓸 수 있는 주체는 그 상태를 되돌릴 수 있다.
- lock 은 여전히 같은 파일시스템의 `flock` 이다. NFS·컨테이너 경계 밖의 두
  발급자는 서로를 못 본다.

---

## §1 53차 반례 10건 — 전부 재현한 뒤 고쳤다

| # | 53차 반례 | 재현 | 고친 자리 |
|---|---|---|---|
| P0-1① | 발급자가 사전검사를 지난 뒤 대기하는 동안 freeze 완주 → `cohort=frozen · plan=running · release 불가` | ○ | 승인 **commit 시점**에 cohort authority 재검사 (`_assert_cohort_admits`, 원장 lock 안) |
| P0-1② | freeze 가 journal·marker 만 쓰고 죽으면 발급 gate 가 원장만 보고 통과 | ○ | 원장에 durable **`freezing`** 을 먼저 선형화 (`COHORT_STATUS = active·freezing·frozen`) |
| P0-1③ | 발급 API 가 여전히 임의 `claims_root` 를 받는다 | ○ | `claims_root_for_ledger()` — 동결도 발급도 **원장에서** 유도. 공개 API 8개에서 인자 제거 |
| P0-2① | L 의 release 가 자기 token 을 확인한 뒤 멈춘 사이 M 이 발급 → L 이 **M 의** token 을 지운다 | ○ | `_lifecycle_locks()` — `attempt_path → claim → ledger` 를 **모든 mutator** 가 공유 |
| P0-2② | finalize 복구가 lock 없이 지운 뒤 늦은 `phase_done()` 이 claim 을 부활 | ○ | 복구도 같은 임계 구역 안 |
| P0-3 | `_write_ledger_doc()` 의 제자리 `write_text()` → ENOSPC 하나로 원장이 반쪽 | ○ | 발급자와 같은 원자적 쓰기 (temp + write-all + read-back + `os.replace`) |
| P0-4 | 같은 `dir` 에 새 이름의 허용 전이 `None → active` 를 넣으면 frozen 목적지가 사라진다 | ○ | 목적지 frozen 은 **단조**(`frozen_dirs`) · 다른 이름의 재개방은 읽기가 거부 |
| P0-5① | module scope `BOX.update(...)` 가 `Expr` 이라 통째로 무시 | ○ | 값을 버리는 표현식을 **대상 뿌리 이름에 결속**(`_expr_root_name`) · 뿌리 없으면 fail-closed |
| P0-5② | `getattr(f, "__globals__")` 가 dunder allowlist 우회 | ○ | 인자로 건네는 **dunder 문자열 상수**도 같은 규칙 |
| P0-5③ | 절단된 `_producer_source_files()` 가 pristine decoy 를 줘도 두 identity 동일 | ○ | 그 함수를 `_PRODUCER_CUT` 에서 뺀다 — 무엇을 재는지 고르는 것도 주장이다 |
| P0-6 | 직접 발급이 token 을 지역변수로만 만들어 `PlanWriteUncertain` 뒤 회수 불가 | ○ | 발급이 소유 증명을 **인자로** 요구 · gate 는 `--attempt-file` 없으면 거부 |
| P1 | donor report 를 이름만 바꿔 붙이면 통과 (`new_pytest_runs=0`) | ○ | runner 가 **변이별 표식 node**(`test_mutant_<sha12>`)를 sandbox 에 놓고 checker 가 report 바이트에서 찾는다 |
| P1 | `head` 결속이 죽어 있다 (40개의 `0` 으로도 rc 0) | ○ | 조각들이 **한** HEAD 를 적었고 그것이 이 저장소에 **실재**하는지 본다 |
| P1 | journal 의 절대 경로 `dir` 이 저장소 밖에 `.FROZEN` 을 만든다 | ○ | 저장소 상대 canonical 만 (쓰는 쪽·읽는 쪽 같은 규칙) |
| P1 | `_live_claims_for(cohort_id)` 가 인자를 안 쓴다 | ○ | claim record 의 cohort 로 거른다 (읽을 수 없으면 여전히 막는다) |

### 이번 라운드의 형태: **authority 가 둘이면 그 사이가 구멍이다**

여섯 P0 중 넷이 같은 모양이었다.

- 동결은 `claims_root` 인자를 없앴는데 **발급은 안 없앴다** → 두 쪽이 다른 곳을 본다.
- 동결은 journal 을 먼저 쓰고 원장을 나중에 쓰는데 **발급은 원장만 본다** → 그 사이가 창이다.
- 발급은 `attempt_path → claim → ledger` 를 잡는데 **정리 경로는 안 잡는다** → 같은 순서를 안 쓰는 경로가 곧 반례다.
- 발급은 원자적으로 쓰는데 **동결은 제자리에서 자른다** → 약한 쪽이 실효 규칙이다.

고친 방식도 하나다: **규칙을 한 함수에 두고 두 쪽이 그것을 부른다.**
`claims_root_for_ledger()` · `_lifecycle_locks()` · `_atomic_write_text()` 가
그것이고, 동결의 시작은 `freezing` 이라는 **원장 한 필드**로 발급자에게 보인다.

그리고 P0-5① 이 같은 교훈의 다른 얼굴이다: `_MODULE_NONBINDING` 의 `Expr` 은
"그 문은 아무 것도 안 한다" 는 **주장**이었고 틀렸다. `BOX.update(tol=0.02)` 는
이름을 묶지 않지만 `BOX` 의 상태를 정한다.

---

## §2 증거

### 2-1 전체 회귀 — **1390 passed · 1 xfailed · 0 failed**

### 2-2 strict smoke — **rc 0 · 52 ✅ · 0 ❌** (clean 커밋에서)

### 2-3 변이 전수 — 등록부 **157 scenario** (executable 150 · declared 7)

145 → 157. 이번 라운드 방어 12개를 등록했고, 54차 수정으로 원문이 움직인 낡은
preimage 를 갱신했다 (`--check-preimages` 가 그것을 먼저 잡는다).

**전수 재생 결과의 정본은 커밋된 증거 파일이다** —
`docs/22p_gap/mutation_coverage/s1..s12.json` 과 그 옆의 `reports/`. 이 문서에
숫자를 옮겨 적지 않는다 (사본은 인용 근거가 아니다).

### 2-4 변이 증거의 남은 한계 — 명시한다

53차는 영수증 digest 를 exact mutant 에 결속했다. 그런데 `_receipt_digest()` 는
**공개 함수**이므로 조각을 쓰는 쪽이 다시 계산할 수 있고, 리뷰어는 다른
mutant 의 **진짜** report 를 옮기고 digest·transcript 만 재계산해 통과시켰다.

54차의 결속은 조각이 만들 수 없는 것이다 — runner 가 **그 실행에만 있는** 시험
node 를 sandbox 에 놓고 checker 가 report 바이트에서 그것을 찾는다. 그래도
**report 자체를 손으로 위조하면 통과한다.** checker 가 독립 replay 를 하는 것은
아니다 — 52·53차 리뷰어의 그 조건은 여전히 **미충족**이다.

### 2-5 증인 규칙이 **둘**이었다 — 이 라운드의 형태가 증거 층에서 한 번 더

12조각이 전부 초록으로 끝난 뒤 **합집합 검사가** `module-gate-before-side-effects`
를 거부했다. 같은 report, 같은 실행인데 판정이 갈렸다 — 규칙이 둘이었기 때문이다.
실시간 재생은 `want in longrepr`(본문 전체), 영수증 검사는 `_last_line()`(의미 줄).

pytest 는 실패 재현에 **시험 소스를 함께 찍는다.** 그래서 본문 매칭은 주석에 남은
문자열에도 걸린다. 이 scenario 의 증인 `KeyError: 'discharged_state'` 는 47차에
"gate 호출을 지웠더니 한참 뒤 엉뚱하게 죽은" 예외였고 48차가 시험을 고치면서
실패 이유가 아니게 됐는데, 48차가 그 사연을 **주석으로 남겼고** 거기 옛 문자열이
그대로 있어 여섯 라운드를 통과했다 — 48차가 고친 바로 그 결함이 증거 층에 화석으로
남아 있었다.

규칙을 한 함수(`_witness_holds()`)로 모으고 **더 엄격한 쪽**을 골랐다. 저장된
증인 176개를 새 규칙으로 전수 감사했고 어긋난 것은 이 하나뿐이다. 회귀와 변이
지점(`witness-must-be-in-the-meaning-line`)을 함께 등록했다.

### 2-5b 변이가 이번에도 **약한 시험 다섯**을 잡았다

- `frozen-destination-is-monotonic` · `admission-rechecks-the-cohort-at-commit`
  — 심층 방어라 단일 변이로 안 물었다 → **MULTI** 로 (후자는 시험이 끼어드는
  지점을 claim 파일이 생기기 **전**으로 옮겨야 했다).
- `freeze-ledger-write-is-atomic` — fixture 원장의 최상위 key 가 하나뿐이라 잘린
  YAML 도 파싱됐다 → 구조가 여럿인 원장으로 바꾸고 "구조가 그대로인가" 를 본다.
- `receipt-verdict-is-fail-closed` — 53차엔 단일 변이로 물었는데 54차에 안 물었다.
  빈 report 를 **표식 검사가 먼저** 거부하기 때문이다 → 두 자리(`_report_identity_rc`
  호출 · fail-closed 비교)를 함께 되돌리는 **MULTI** 로 옮겼다.
- `coverage-checks-the-recorded-head` — 변이 sandbox 에 `.git` 이 없어 baseline
  자체가 빨갛다 (검사가 아니라 환경이 다르다) → **declared** 로 등록하고 경계와
  대체 회귀를 `DECLARED_MASKED` 에 적었다.

### 2-6 산출물 — g8 을 얼리고 g9 로

| 값 | 53차 (g8) | 54차 (g9) |
|---|---|---|
| `producer_semantic_sha256` | `d7da84a9272924dd` | `d4c3dc8ff856d31a` |
| `compute_sha256` | `7634dd2f0d4b4e4b` | `b12e9ff10385169e` |
| `row_projection_py_sha256` | `2bc69ab32c1e7a77` | `b99dee231d0f170e` |
| 영수증 core_sha | `c07fc3920fabb8b7…` | `77235418c8f3e8e8…` |
| validator identity | `123bcc2f6b7ea942` | `7b968b9bf0965402` |
| 투영 | `proj_g8` | `proj_g9` |

**행 바이트는 안 움직였다** — `proj ad598fe77e75afec` 로 g4~g8 과 동일하다.
움직인 것은 identity 의 **정의**다 (P0-5 셋). 그래도 cross-cohort 비교는
금지다 — 같은 바이트라는 사실은 회귀가 확인하는 것이지 인용의 근거가 아니다.

---

## §3 무엇을 반증해 주기 바라는가

우선순위 순. **§0 에 신고한 것을 다시 적는 것은 이미 아는 사실의 재확인이다.**

1. **`freezing` 창.** 동결이 `active → freezing` 까지만 쓰고 죽은 상태에서
   운영자가 할 수 있는 일. `freezing` 에서 `active` 로 되돌리는 경로가 원장 쓰기
   말고 또 있는가. 발급자가 `freezing` 을 보고도 통과하는 schedule.
2. **공유 lock 순서의 남은 창.** `attempt_path → claim → ledger` 를 **안 지나는**
   mutator, 또는 셋 중 일부만 잡는 경로. 특히 freeze(ledger)와 finalize
   (attempt→claim→ledger)가 겹치는 순서.
3. **원장이 정하는 claims root.** `claims_root_for_ledger()` 가 두 caller 에게
   다른 값을 주는 경우 (symlink·bind mount·상대경로·`DEFAULT_LEDGER` 재바인딩).
4. **frozen 단조.** journal 을 편집해 목적지의 frozen 을 지우는 다른 sequence.
   `.FROZEN` marker 와 원장·journal 셋이 어긋나는 조합에서 읽기가 무엇을 믿는가.
5. **producer 닫힘.** `_expr_root_name()` 이 뿌리를 못 찾아 fail-closed 로 멈추는
   대신 **잘못된 뿌리**에 결속하는 표현식. dunder 문자열 규칙이 Call 인자만 보는
   것을 우회하는 자리 (dict 값·리스트 원소 등).
6. **증거.** 변이별 표식을 통과하면서 실제로는 안 돈 조각. `_marker_id()` 충돌.
7. **커밋 확실성.** `PlanNotCommitted` 가 나오는데 실제로는 커밋된 경로. 반대로
   `PlanWriteUncertain` 이 반복돼 다리가 영영 회수 불가로 남는 운영 시나리오.
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
회귀 2건이 `len(seen) >= 2` 로 실패한다. 둘 다 알려진 환경 한계다 — 다만
**환경 한계로 보이는 실패가 사실은 순서·fail-open 결함**일 수 있다는 것이
50차에 실측됐으니 한 번은 의심해 주기 바란다.
