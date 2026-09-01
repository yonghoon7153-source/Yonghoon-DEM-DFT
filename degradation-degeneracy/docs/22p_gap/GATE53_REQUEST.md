# 53차 게이트 리뷰 요청 — 묶음 9 (실행 전 승인 · 보존 lifecycle)

**대상 커밋**: `5ecfdb50` (브랜치 `claude/14-gate-code-review-9qkx05`) — 코드(`b667e025`)·산출물(`c4c1a380`)·요청문·원장 §61·변이 전수 증거를 전부 담은 커밋이다. 이 줄을 고치는 커밋만 그 뒤에 하나 더 있다 (내용 동일).
**직전 판정**: 52차 **NO-GO** — P0 7건 · P1 1건

---

## §0 먼저 — 이번 라운드가 **하지 않은** 것

| 조건 | 상태 |
|---|---|
| **P0-1** producer 결속 — 닫힌 typed manifest 파싱 · 두 payload 압축해제 재해시 · producer 발행 영수증 | **미착수** (49차부터 다섯 라운드째) |
| **P0-8** 경로 무관 typed·sealed 실행 class marker | **미착수.** 판정은 여전히 `is_inside_namespace()` 의 경로 기반 격리 |
| **P0-4** typed CAS/archive/restore/validation/retention 영수증 **소비** | **부분** |
| 발급·finalize·freeze·publish 를 **하나의 generation transaction** 으로 | **부분** — 아래 |
| baseline·sweep1d·wsweep 계획 gate · 실물 object-lock adapter · power-loss 모델 · publisher 전용 OS principal · 외적타당도 #48/#49/#50 | **미착수** |

52차 리뷰어의 최소 조건 7개 중 이번에 한 것은 1~6 이다. 7("§0 의 기존 미착수
항목은 그대로 남는다")은 그대로다 — 그리고 그것이 **GO 를 막는 축**이라는 판단에
동의한다. 51·52차 리뷰어가 두 번 권고한 순서(① 단일 transaction ② P0-8 sealed
execution manifest ③ P0-1 producer receipt)에서, 이번 라운드는 ①을 lock 공유
수준까지 밀었고 ②·③ 은 시작하지 않았다.

**남아 있는 표면** (52차 신고분 + 이번 라운드에 새로 확인한 것):

- 원장·journal·anchor·`.FROZEN` **전부**에 쓸 수 있는 주체는 역사를 다시 쓸 수 있다.
- 소유 증명 token 파일(0600)은 같은 uid 의 다른 process 가 읽을 수 있다.
- `--attempt-file` 없이 `python -m src.grid` 직접 호출은 여전히 claim 을 발급한다.
- 변이 증거의 **pytest report 자체를 위조**하면 checker 를 통과한다 (§2-4).
- `open(__file__).read()` 는 여전히 producer 닫힘 안에서 가능하다 — dunder
  allowlist 는 `__file__` 을 허용하지 않지만(`REPO` 는 절단면 뒤로 갔다) 경로를
  다른 방법으로 얻어 자기 소스를 읽는 경로를 **전부** 막지는 못했다.
- 동결과 게시는 같은 `_PublishLock` 을 공유하지만, 그 둘과 발급(claim lock)·
  원장(ledger lock)은 **세 개의 lock** 이지 한 transaction 이 아니다.

---

## §1 52차 반례 8건 — 전부 재현한 뒤 고쳤다

| # | 52차 반례 | 재현 | 고친 자리 |
|---|---|---|---|
| P0-1 | 커밋 뒤 lock 을 빠져나오다 실패하면 `OSError` 가 새고 rollback 이 확정 미커밋으로 오판 | ○ | 불확실 구역 = **임계 구역 전체**. `PlanNotCommitted` 를 새로 두고 **그때만** 되돌린다 |
| P0-2 | `os.write()` 반환 길이를 버려 부분 쓰기가 성공으로 통과 | ○ | `_write_all()` + `_assert_bytes_on_disk()` (claim·소유 증명 양쪽) |
| P0-3 | 서로 다른 claim lock 이라 공유 token 경로에서 두 발급이 나란히 통과 | ○ | `LOCK_ORDER = ("attempt_path", "claim", "ledger")` · `_attempt_path_lock()` |
| P0-4 | `freeze_cohort(claims_root=…)` 로 빈 디렉터리를 주면 동결 완주 | ○ | 인자를 **없앴다**. 위치의 정본은 발급자(`claims_root_for()`) · 못 물으면 얼리지 않는다 |
| P0-5 | 동결이 lock 밖 doc 을 되써 finalize 기록을 지운다 · 복구 분기가 검사보다 먼저 · 게시가 동결 뒤에 CURRENT 를 옮긴다 | ○ | 게시 lock + 원장 lock · 쓰기 직전 재독 · 검사를 맨 앞으로 |
| P0-6 | `read_lifecycle()` 이 금지된 해동을 스스로 anchor · g1..g5 에 `.FROZEN` 없음 | ○ | 허용 전이를 **읽을 때** 검사 · 읽기는 쓰지 않는다(`repair_lifecycle_anchor()`) · marker 소급 |
| P0-7 | `BOX['value']=…` 가 닫힘 밖 · `__loader__.get_source()` 가 금지 모듈 밖 | ○ | 컨테이너 변형을 뿌리 이름에 결속(뿌리 없으면 fail-closed) · dunder 를 **allowlist 로** |
| P1 | 영수증이 바이트만의 함수 · 빈 report 는 건너뛴다 | ○ | `_receipt_digest()` 가 exact mutant 에 결속 · 유도 실패도 비교에 들어간다 |

### 이번 라운드의 형태 셋

**① 경계는 호출이 아니라 임계 구역이다.** 50차 fsync · 51차 재독 · 52차 lock
exit — 세 라운드 연속 같은 자리에서, 매번 "그 호출 하나" 를 감쌌기 때문에 뚫렸다.
이제 `_mark_plan_running()` 은 `with` 문 전체를 감싸고, 결과는 두 타입 중
하나다: `PlanNotCommitted`(원장을 안 건드렸다) 또는 `PlanWriteUncertain`(모른다).

**② 기본값을 뒤집었다.** 52차의 기본값은 "모르면 되돌린다" 였고, 그러면 예상 못
한 실패 하나가 곧 회수 불가능한 orphan 이다. 53차의 기본값은 **보존**이다 —
최악의 대가가 `release_leg_run()` 한 번이기 때문이다. 대칭이 아닌 위험에는
대칭이 아닌 기본값을 준다.

**③ blacklist 를 allowlist 로 뒤집었다.** 52차의 "능력을 닫는다" 도 결국 모듈
네 개짜리 blacklist 였고, 리뷰어는 `__loader__` 로 그 밖에서 들어왔다. 정규형이
볼 수 없는 것으로 가는 문은 전부 dunder 이므로 dunder 를 allowlist 로 만들었다
(`_DUNDER_ALLOWED`). 그 규칙이 `REPO = Path(__file__)…` 을 잡았고, 그래서 `REPO`
와 provenance 파일 위치를 producer **절단면 뒤로** 옮겼다 — checkout 위치는
producer 의미가 아니다.

---

## §2 증거

### 2-1 전체 회귀 — **1375 passed · 1 xfailed · 0 failed**

### 2-2 strict smoke — rc 0 (clean 커밋 `c4c1a380` 에서)

### 2-3 변이 전수 — 등록부 **145 scenario** (executable 139 · declared 6)

127 → 145. 이번 라운드 방어 18개를 등록했고, 53차 수정으로 원문이 움직인 낡은
preimage 5건을 갱신했다 (`--check-preimages` 가 그것을 먼저 잡았다).

**전수 재생 결과의 정본은 커밋된 증거 파일이다** —
`docs/22p_gap/mutation_coverage/s1..s12.json` 과 그 옆의 `reports/`. 이 문서에
숫자를 옮겨 적지 않는다 (사본은 인용 근거가 아니다).

### 2-4 변이 증거의 남은 한계 — 명시한다

53차는 영수증을 **exact mutant** 에 결속했고(같은 바이트라도 다른 scenario 에서
다른 digest), 유도 실패를 fail-closed 로 바꿨다. 그래도 **report 자체를
위조하면 통과한다.** checker 가 독립 replay 를 하는 것은 아니다 — 52차 리뷰어의
조건 중 "checker 가 독립 replay" 는 여전히 **미충족**이다.

### 2-5 변이가 이번에도 **약한 시험** 둘을 잡았다

`producer-dunder-is-an-allowlist` 와 `receipt-verdict-is-fail-closed` 가 처음에
안 물었다. 둘 다 겨눈 축을 다른 guard 가 가리고 있었다.

- 앞의 것: dunder 규칙을 지워도 loader protocol 이름이 세 반례를 다 잡았다 →
  관찰자 이름이 아니라 dunder 문 자체가 막는 사례(`build.__globals__`)를 시험에
  더했다.
- 뒤의 것: `derived is None` 분기를 지워도 다음 비교가 잡았다 → 그 분기는
  **중복**이므로 지우고, 변이를 52차 상태(`derived is not None and`)의 복원으로
  바꿨다.

### 2-6 산출물 — g7 을 얼리고 g8 로

| 값 | 52차 (g7) | 53차 (g8) |
|---|---|---|
| `producer_semantic_sha256` | `92fa65b43a6352ce` | `d7da84a9272924dd` |
| `compute_sha256` | `fb702e8134a3cf79` | `7634dd2f0d4b4e4b` |
| `row_projection_py_sha256` | `2f01bf35a9d88af9` | `2bc69ab32c1e7a77` |
| 영수증 core_sha | `5ca1f4ecc140762b…` | `c07fc3920fabb8b7…` (검사 34건) |
| validator identity | `257c5b6d8ef8712a` | `123bcc2f6b7ea942` |
| 투영 | `proj_g7` | `proj_g8` (6138행 · restart 30690행) |

**행 바이트는 안 움직였다** — `proj ad598fe77e75afec` 로 g4~g7 과 동일하다.

봉인 marker(`.FROZEN`)를 g1..g5 에 소급해 채웠다 (`backfill_frozen_markers()` —
입력은 journal 과 원장이고 caller 가 목록을 주지 않는다).

---

## §3 무엇을 반증해 주기 바라는가

우선순위 순. **§0 에 신고한 것을 다시 적는 것은 이미 아는 사실의 재확인이다.**

1. **세 lock 사이의 창.** `attempt_path`·`claim`·`ledger`·`publish` 넷 중 둘이
   서로를 막지 않는 schedule. 특히 freeze(publish→ledger)와 finalize(claim→
   ledger)가 겹치는 순서, 그리고 `_live_claims_for()` 검사와 그 뒤 발급 사이.
2. **커밋 확실성의 남은 오판.** `PlanNotCommitted` 가 나오는데 실제로는 커밋된
   경로. 반대로 `PlanWriteUncertain` 이 반복돼 다리가 영영 회수 불가로 남는 운영
   시나리오.
3. **write-all/read-back 이 못 보는 것.** 읽기 캐시·page cache 때문에 read-back
   이 디스크가 아닌 것을 보는 경우. 부분 쓰기 뒤 `os.replace` 가 남기는 상태.
4. **동결 transaction.** `.FROZEN` marker 를 우회해 frozen tree 에 쓰는 경로.
   동결 도중 crash 의 남은 조합 (marker 는 썼는데 원장은 못 쓴 상태 등).
5. **lifecycle reader.** 허용 전이 검사를 통과하면서 역사를 다시 쓰는 journal
   편집. 한 줄 앞선 partial commit 관용을 악용하는 sequence.
6. **producer 닫힘.** dunder allowlist 의 열한 이름 중 정규형이 실제로는 못 보는
   것. `_producer_source_files()` 를 절단면에 둔 것이 만든 새 구멍
   (`open(__file__)` 계열 — §0 에 신고했다).
7. **증거.** exact-mutant 결속을 통과하면서 실제로는 안 돈 조각.
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
