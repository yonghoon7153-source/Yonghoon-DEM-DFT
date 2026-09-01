# 52차 게이트 리뷰 요청 — 묶음 9 (실행 전 승인 · 보존 lifecycle)

**대상 커밋**: `9beb9649` 이후 — 이 요청문·원장 §60·변이 증거를 담은 커밋이 정본이다 (브랜치 `claude/14-gate-code-review-9qkx05`)
**직전 판정**: 51차 **NO-GO** — "이번에도 **검사 하나 뒤의 창**, **다른 lock
namespace**, **self-attested evidence** 가 반복됐다" (새 P0 뿌리 8건 · P1 2건)

---

## §0 먼저 — 이번 라운드가 **하지 않은** 것

| 조건 | 상태 |
|---|---|
| **P0-1** producer 결속 — 닫힌 typed manifest 파싱 · 두 payload 압축해제 재해시 · producer 발행 영수증 | **미착수** (49차부터 네 라운드째) |
| **P0-8** 경로 무관 typed·sealed 실행 class marker | **미착수.** 판정은 여전히 `is_inside_namespace()` 의 경로 기반 격리 |
| **P0-4** typed CAS/archive/restore/validation/retention 영수증 **소비** | **부분** |
| 발급·게시·freeze 를 **하나의 generation transaction** 으로 | **부분** — 아래 |
| baseline·sweep1d·wsweep 계획 gate · 실물 object-lock adapter · power-loss 모델 · publisher 전용 OS principal · 외적타당도 #48/#49/#50 | **미착수** |

51차 리뷰어가 권고한 순서는 ① lifecycle·freeze·publisher 를 단일 generation
transaction 으로 ② P0-8 sealed execution manifest ③ P0-1 producer receipt 였다.
이번에 한 것은 **①의 절반**이다: 발급·phase·되돌림·freeze 가 같은 배타성을
공유하도록 고쳤고, 게시는 대상 안의 marker 로 막았다. 그러나 그 둘은 **서로
다른 두 장치**이고 하나의 transaction 이 아니다. ②·③ 은 시작하지 않았다.

**남아 있는 표면**:

- 원장·journal·anchor·`.FROZEN` **전부**에 쓸 수 있는 주체는 역사를 다시 쓸 수
  있다. 52차가 좁힌 것은 "원장 한 파일" 과 "bind mount alias" 다.
- 소유 증명 token 파일(0600)은 같은 uid 의 다른 process 가 읽을 수 있다.
- `--attempt-file` 없이 `python -m src.grid` 직접 호출은 여전히 claim 을 발급한다.
- 변이 증거의 **pytest report 자체를 위조**하면 checker 를 통과한다 (§2-6).

---

## §1 51차 반례 10건 — 전부 재현한 뒤 고쳤다

| # | 51차 반례 | 재현 | 고친 자리 |
|---|---|---|---|
| P0-1a | 비교 뒤 `unlink` 사이에 새 발급이 끼어들어 B 의 token 이 지워진다 | ○ | claim 폐기와 token 삭제를 **한 임계 구역**으로 (`_abandon_claim`·`finalize_leg`) |
| P0-1b | 서로 다른 leg 가 같은 `--attempt-file` 을 쓰면 첫 credential 이 덮인다 | ○ | 소유 증명 파일이 **leg·attempt 를 담는다** + 살아 있는 남의 것은 안 덮는다 |
| P0-2 | `_plan_status()` 재독 오류를 미커밋으로 읽어 회수 불가 orphan | ○ | `PlanWriteUncertain` — 커밋 여부를 **타입으로** 알린다 (추정을 없앴다) |
| P0-3 | 발급·phase·게시·freeze 가 다른 lock namespace | ○ | freeze 가 **살아 있는 claim 을 거부**한다 |
| P0-4 | bind mount alias 로 frozen tree 에 게시 | ○ | 봉인 marker 를 **대상 안**에 (`.FROZEN`) |
| P0-5 | 승인한 cache bytes 가 runtime 불일치에서 재계산으로 넘어간다 | ○ | authoritative mode 에서는 **거부** (+ 재계산 경로 도달 자체를 거부) |
| P0-6 | `DD_SMOOTH_CACHE` 가 J 를 바꾸는데 승인·지문 밖 | ○ | `smoothing_backend` 를 승인 축과 `env_fingerprint()` **양쪽**에 |
| P0-7 | `AugAssign`·import·match capture 가 binding 인데 안 담긴다 | ○ | 이름 → **순서 있는 binding 목록** |
| P0-8 | `inspect.getsource()` 로 정규형이 버린 raw source 를 읽는다 | ○ | raw source **관찰 능력**을 닫는다 |
| P1-1 | journal→head crash 가 재시도 불가 | ○ | 한 줄 앞선 partial commit 을 인식해 anchor 를 완주 |
| P1-2 | coverage v2 도 replay 0회를 인증한다 | ○ | 조각이 **pytest report 원본**을 남기고 checker 가 거기서 판정을 다시 유도 (v3) |

### 이번 라운드의 형태: **철자에서 능력으로**

세 자리에서 같은 결론에 도달했다.

- 51차: `.__doc__` 철자를 막았더니 `read = getattr` 이 피해 갔다 → 버리는 것을
  없앴다.
- 52차: `getsource` 철자를 막았더니 `from inspect import getsource as _gs` 가
  피해 갔다 → `inspect`·`linecache`·`dis`·`traceback` 에 묶이는 이름을 닫힘
  안에서 금지했다 (**지역 import 포함**).
- 이름 → 단일 node 는 `TOL = 1` · `TOL += 9` 를 구별하지 못했다 → **순서 있는
  목록**.

blacklist 는 언제나 다음 철자를 남긴다. 닫는 것은 **그 능력을 쓸 수 있는가** 다.

### 추정을 없앴다

51차 `_plan_status()` 는 "쓰기가 실패했는데 커밋됐나" 를 재독으로 **추정**했다.
리뷰어가 재독까지 실패시키자 그 추정이 `None` 을 냈고, `None != "running"` 이
회수 불가능한 orphan 을 만들었다. `_mark_plan_running()` 은 자기가 **쓰기 전에**
실패했는지(원장을 안 건드렸다 → 확정 미커밋) 아니면 쓰는 도중·이후인지를 알고
있다. 그것을 예외 타입으로 내보내면 caller 는 추정할 필요가 없다.

### 이름은 대상이 아니다

49차는 cohort ID 를, 51차는 `dir` 을 봉인했다 — 둘 다 **이름**이고 bind mount 는
이름을 또 만든다. 봉인을 대상 **안**에 둔다 (`.FROZEN`). 어느 이름으로 열든 같은
tree 를 열면 같은 marker 를 본다.

---

## §2 증거

### 2-1 전체 회귀 — **1360 passed · 1 xfailed · 0 failed**

### 2-2 strict smoke — **rc 0 · 52 ✅ · 0 ❌**

### 2-3 변이 전수 — 127 scenario

등록부는 127 scenario (executable 121 · declared 6) 이고 이번 라운드 방어 13개를
등록했다. artifact 는 schema **v3** 이며 scenario 마다 **pytest report 원본**을
`mutation_coverage/reports/sI/` 에 남긴다.

**전수 재생 결과의 정본은 커밋된 증거 파일이다** —
`docs/22p_gap/mutation_coverage/s1..s12.json` 과 그 옆의 `reports/`. 이 문서에
숫자를 옮겨 적지 않는다 (사본은 인용 근거가 아니다).

### 2-4 lifecycle e2e — 3 process · 난입 여섯

### 2-5 산출물 — g6 을 얼리고 g7 로

| 값 | 51차 (g6) | 52차 (g7) |
|---|---|---|
| `producer_semantic_sha256` | `632232332b015def` | `92fa65b43a6352ce` |
| `compute_sha256` | `730e673e74edb8ae` | `fb702e8134a3cf79` |
| `row_projection_py_sha256` | `06e8dcfe58946e9e` | `2f01bf35a9d88af9` |
| 영수증 core_sha | `646c88ce3050a3a6…` | `5ca1f4ecc140762b…` (검사 34건) |
| validator identity | `c557ae9ef3f75fa7` | `257c5b6d8ef8712a` |
| 투영 | `proj_g6` | `proj_g7` (6138행 · restart 30690행) |

**행 바이트는 안 움직였다** — `proj ad598fe77e75afec` 로 g4~g6 과 동일하다.

### 2-6 변이 증거의 남은 한계 — 명시한다

v3 는 조각이 남긴 report 에서 판정을 다시 유도한다 (`verify_receipts()`).
**report 자체를 위조하면 통과한다.** 그것은 "아무 것도 안 하고 숫자만 적는 것"
과 다른 종류의 주장이고 report 는 committed·diffable 이지만, checker 가 독립
replay 를 하는 것은 아니다. 51차 리뷰어의 조건 중 "checker 가 독립 replay" 는
**미충족**이다.

### 2-7 증인이 **선언한 이유로** 물어야 한다

`coverage-checker-derives-from-receipts` 변이가 처음에는 물었는데 증인이
"정상 조각이 거부됐다" 였다 — `check_coverage()` 가 맨 앞에서
`check_preimages()` 를 부르므로 이 파일 **자신**을 변이시키면 그 gate 가 먼저
걸린다. 물긴 하지만 다른 이유다. 영수증 검사를 `verify_receipts()` 로 떼어 내고
시험이 그것만 겨누게 했다.

### 2-8 e2e 가 캐시를 물려받지 않는다

P0-5 를 고치자 lifecycle e2e 가 깨졌다 — 그 tree 는 `configs/` 에 시험용 config
를 더하므로 `source_digest()` 가 저장소와 다르고, 저장소 `.cache` 를 symlink
하면 승인이 가리키는 바이트를 다른 코드가 만든 것이 된다. **hard error 가 옳은
동작이다.** e2e 는 이제 캐시를 복사한 뒤 `source_digest` 를 그 tree 의 값으로
다시 적는다 (준비 단계를 다시 돈 것과 같다).

---

## §3 무엇을 반증해 주기 바라는가

우선순위 순. **§0 에 신고한 것을 다시 적는 것은 이미 아는 사실의 재확인이다.**

1. **배타성이 안 닿는 자리.** 발급·phase·되돌림·finalize·freeze·게시 중 두 개가
   서로를 막지 않는 schedule. `freeze` 의 claim 검사와 발급 사이의 창.
   `promote_cohort_generation()` 과 `freeze_cohort()` 를 겹치는 순서.
2. **커밋 확실성.** `PlanWriteUncertain` 이 **안** 나오는데 실제로는 불확실한
   쓰기. 확정 미커밋이라 판단했는데 커밋된 경로.
3. **token 결속의 남은 구멍.** leg·attempt 결속을 우회해 남의 credential 을
   덮거나 남의 것으로 붙는 sequence. `_assert_token_file_free_for()` 가
   놓치는 상태 (claim 이 아직 없는 순간 등).
4. **승인 축.** `LEG_SPEC_*` 밖이면서 **행 바이트를 바꾸는** 축. 환경변수·
   import 시점 상수처럼 process 밖에서 정해지는 값 중 결과에 닿는 것.
5. **동결 대상 identity.** `.FROZEN` marker 를 우회해 frozen tree 에 쓰는 경로.
   marker 를 지우거나 marker 없이 만든 새 tree 로 옛 바이트를 대체하기.
6. **producer 닫힘.** `_MODULE_COMPOUND`/`_MODULE_NONBINDING` 이 잘못 분류한 문.
   `_SOURCE_REFLECTION_MODULES` 밖에서 raw source 에 닿는 경로 (`open(__file__)`
   같은 것 포함 — 이것은 **아직 안 막았다**).
7. **증거.** v3 결속을 통과하면서 실제로는 안 돈 조각 (§2-6 의 한계 밖에서).
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
