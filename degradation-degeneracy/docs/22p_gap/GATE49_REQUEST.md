# 49차 게이트 리뷰 요청 — 묶음 9 (실행 전 승인 · 보존 lifecycle)

**대상 커밋**: `e42405f7` (브랜치 `claude/14-gate-code-review-9qkx05`)
**직전 판정**: 48차 **NO-GO** — "정상 lifecycle 은 실행 불가능하고 우회·자기신고
경로는 열려 있다"

---

## §0 먼저 — 이번 라운드가 **하지 않은** 것

리뷰 시간을 아끼기 위해 먼저 적는다. 아래는 48차 조건 중 이번에 손대지 않은
것이고, 여기에 반례를 쓰는 것은 이미 아는 사실의 재확인이다.

| 48차 조건 | 상태 |
|---|---|
| **P0-1** producer 결속 — 닫힌 typed manifest 파싱 · 두 payload 압축해제 재해시 · `(leg, producer identity, manifest digest, projection digest, restart digest)` 를 묶는 producer 발행 영수증 | **미착수** |
| **P0-8** 경로 무관 typed·sealed **실행 class marker** (primary·compare·nested·archive-external·전이 report source) | **미착수.** 판정은 여전히 `is_inside_namespace()` 의 정규 격리(경로 기반)다. 49-9 로 sink 두 곳의 **방향** 판정만 고쳤다 |
| **P0-4** typed CAS/archive/restore/validation/retention 영수증 **소비** | **부분.** `preservation_pending` 중간 상태와 계약 §8 완전 튜플은 넣었고, 영수증 소비는 미착수 |
| baseline·sweep1d·wsweep 의 계획 gate | **미착수** (grid·fit·finalize·release 만 배선) |
| 실물 object-lock provider adapter · power-loss ordering fault model · publisher 전용 OS principal | **미구현** (별도 acceptance) |
| 외적타당도 #48/#49/#50 | **미착수** |

**이번 라운드에 새로 열린 표면**도 먼저 적는다.

- `COHORT_LIFECYCLE.jsonl` / `.head` — 원장·journal·anchor **세 파일 모두**에
  쓸 수 있는 주체는 역사를 다시 쓸 수 있다. 막는 것은 "조용한" 되돌림이고,
  그 밖은 tracked diff 를 사람이 보는 것이 바깥 통제다 (§13.3.1 의 `flock` 이
  같은 기계만 가정하는 것과 같은 종류의 경계).
- 소유 증명 token 파일(0600) — 같은 uid 의 다른 process 는 읽을 수 있다.
  argv 노출(`ps`·`/proc/<pid>/cmdline`)은 막았고, 파일 권한 밖은 §13.3.1 과
  같은 경계다.
- `--attempt-file` 없이 grid 를 부르면 여전히 claim 을 발급한다 (token 파일을
  안 남기므로 그 실행은 스스로 fit 을 이어갈 수 없다). `run.sh` 는 언제나
  경로를 넘기므로 production 경로에는 그 상태가 없다.

---

## §1 이번 라운드가 닫은 것

### 1-1 P0-3/P0-4 — 정상 lifecycle 이 완주하지 못했다 (48차 판정의 첫 문장)

48차의 두 규칙은 각각 옳았고 단위 시험도 다 통과했다. 깨진 것은 **그 사이의
전달**이고, 그것은 한 process 안에서 도는 시험에는 보이지 않는다.

| 자리 | 무엇 |
|---|---|
| `tools/preserve.py::open_leg_run` | coordinator 가 실행권을 **한 번** 발급하고 소유 증명을 0600 파일로 내놓는다 |
| `::attach_leg_run` | phase process 가 그 파일로 **같은 실행**에 붙는다 |
| `::precheck_leg_run` | 사전검사가 **새 발급**과 **소유한 재개**를 구분한다 |
| `::release_leg_run` | 되돌림 (dry-run · 중단된 실행권 정리) |
| `::finalize_leg(token=/token_file=)` | 소유 증명 **필수** (48차 기본값 `None` 은 이름만 알면 남의 실행을 닫을 수 있었다) |
| `::inspect_leg_run` | 진단은 공개 필드만 (`attempt_id`) |
| `run.sh --attempt-file` / `--mode finalize` / `--mode release` | coordinator 가 grid·fit 에 **경로**를 넘기고 끝에서 닫는다 |
| `src/grid.py --attempt-file` · `src/fitting.py --attempt-file` | token 자체는 argv 에 싣지 않는다 |

**credential 을 평문으로 저장하지 않는다.** claim 파일은 `attempt_id`(공개)와
`attempt_verifier`(`sha256(token)`)만 담는다.

### 1-2 P0-5 — 승인이 fit 의 실행 정책과 입력 바이트를 덮지 않았다

```
LEG_SPEC_FIT_KEYS = ("config_digest", "objective_order", "reference",
                     "halfcell_recipe", "bounds_preset", "bounds_digest",
                     "optimizer", "use_noisy", "row_selection",
                     "in", "in_digest", "out")
```

`objective_order` 는 **순서**다 (warm 연쇄가 그 순서를 따른다). 중첩 dict
(`optimizer`·`halfcell_recipe`·`row_selection`)도 닫힌 집합이다. production 과
시험이 **같은 함수**(`src/fitting.py::live_fit_axis`)로 축을 만든다.

`in_digest` 가 입력의 내용 identity 를 두 경우로 가른다:

| 값 | 뜻 | 런타임 대조 |
|---|---|---|
| hex64 | 이 다리 **밖**에서 온 입력 (F70 분리 producer) | fit 이 읽은 바이트와 직접 |
| `null` | 이 다리의 grid 가 만든다 | grid **phase receipt** 의 `curves_sha256` (`assert_phase_input_binding`) |

### 1-3 P0-6 — 정본 lock 순서 · finalize 임계 구역 · 복구

`LOCK_ORDER = ("claim", "ledger")`. finalize 는 claim lock 을 **쥐고** 내려가고,
snapshot 을 한 번만 읽어 검사와 기록 모두의 근거로 쓰며, 원장 lock **안에서**
전체 authority 를 다시 본다. 원장 write 뒤 claim 삭제 전 crash 는
`_already_finalized()` 가 **원장에서** 알아내 idempotent 하게 닫는다.

> **리뷰어 조건과 다르게 한 것**: "idempotent recovery journal" 을 요구했지만
> **별도 journal 파일을 두지 않았다.** 근거는 원장 자신이다 (계획이 executed
> 이고 실행 기록의 `attempt_id` 가 살아남은 claim 의 것과 같다). 파일을 하나 더
> 두면 "닫혔다" 의 정본이 둘이 되고, 이 저장소가 반복해서 고쳐 온 실패 형태가
> 바로 그것이다. 원장 write 는 `os.replace` 로 원자적이므로 옛 상태 아니면 새
> 상태이고, 옛 상태면 그냥 다시 닫으면 된다.

### 1-4 P0 — 해동(frozen → active)

`docs/22p_gap/COHORT_LIFECYCLE.jsonl` — append-only · 해시 사슬 ·
`frozen → active` 는 `_LIFECYCLE_MOVES` 에 없어 **표현할 수 없다**. 게시 경로는
첫 write 전에 `assert_not_thawed()` 를 지나고 임계 구역 안에서 다시 지난다.
`frozen_reason` 이 남은 cohort 도 status 와 무관하게 거부한다. frozen cohort 의
`CURRENT` 는 계속 읽힌다. 사슬의 끝은 `.head` anchor 가 고정한다.

### 1-5 P0-2 — 닫힘이 import 문법 하나만 따라갔다

`Import + Attribute`(`import src.scoring as sc` → `sc.foo`)를 따라간다. 풀리지
않는 참조는 fail-closed. `globals()`·`getattr(module, …)`·`eval`·`exec`·
`__import__` 는 거부한다 (경계는 좁게 — `getattr(node, f, None)` 은 그대로).
**이 검사가 실물 위반 하나를 찾았다**: `_analyzer_provenance()` 의
`__import__(mod).__version__`. `SUPPORTED_PYTHON` 과 `AST_CANON_GOLDEN` 으로
인터프리터 집합을 고정했다.

### 1-6 P1 둘

- **변이 재생이 0건 실행을 성공으로 셌다** — declared MULTI 하나만 고르면
  `scenario_declared 0 · ran 0 · rc 0` 에 성공 문장 (실측). 분류를 `_select()`
  한 곳으로 모으고, 실행 가능 수 ≠ 실행 수면 실패한다.
- **원장 명부가 multiset 이었다** — `legs: ["a","a"]` 가 그대로 봉인됐다.

### 1-7 P0-4 — `no_bundle` 이 계약 §8 enum 밖이었다

production finalize 가 쓰는 값을 이 저장소 자신의 lint 가 거부하는 상태였다.
계약에 `preservation_pending` 을 추가하고 (`missing` 과 뜻이 다르다), finalize
는 세 축의 완전한 튜플을 쓴다.

---

## §2 증거

### 2-1 end-to-end lifecycle — **세 process 를 건너**

`tests/test_lifecycle_e2e.py`. RUN_SCOPE 를 바이트 그대로 복사한 격리 tree 에
계획 원장을 심고 진짜 `run.sh` 를 따로 띄운다. 원장 우회 환경변수를 새로 만들지
않았다 — `DEFAULT_LEDGER` 가 `tools/preserve.py` 의 위치에서 유도되므로 tree
복사 자체가 격리다. PyBaMM 2조건 실측 **~46s**.

| 단계 | 확인 |
|---|---|
| ① grid | `새 발급` · token 파일 0600 · 계획 `planned → running` |
| ②-a 모듈 직접 호출 (shell 우회) | `이미 실행 중` 으로 거부 |
| ②-b 위조 token | `소유 증명이 맞지 않는다` |
| ②-c 없는 token 파일 | `소유 증명 파일이 없다` |
| ②-d 곡선 한 바이트 변조 | `grid 가 만든 것이 아니다` (P0-5 입력 결속) |
| ③ fit | `소유한 재개` — **48차가 거부하던 지점** |
| ④ finalize | `executed` · roster 이동 · phase receipt 둘 · `preservation_pending`/`unvalidated` · token 파일 삭제 |
| 별도 | `--mode release` 뒤 같은 다리를 **다시 시작**할 수 있다 |

### 2-2 전체 회귀

```
tests/                    1313 passed · 1 xfailed · 0 failed
  test_docs_lint.py        284 passed          (48차부터 끌던 artifact staleness 3건 닫힘)
  test_preserve.py         370 passed
  나머지                    659 passed · 1 xfailed
```

### 2-3 strict smoke — **rc 0 · 52 ✅ · 0 ❌**

48차 §0 에 "6단계 이후 미완" 이라고 적었던 자리를 실제로 돌렸다. 처음에는
**실패 11건**이었고 원인은 48차 P0-8 이 심은 결함이었다 (§1-9 / 아래 2-5).

### 2-4 변이 전수 재생 — 89 scenario

```
slice 1..8 (--slice I/8)  : rc 0 · 물었다 83 · 신고 6 · ★ 0
--check-coverage s1..s8   : 등록부 scenario 89 (executable 83 · declared 6) · 관측 89
                            조각 합집합이 등록부 전체를 정확히 덮었다
```

증거 파일: `docs/22p_gap/mutation_coverage/s1..s8.json` (RUN_SCOPE 밖 — code
identity 를 움직이지 않는다). 이번 라운드가 붙인 방어 24개가 전부 등록돼 있다.

**동치 변이 1건을 신고한다**: `finalize` 의 receipt snapshot 을 lock 안에서
다시 읽도록 되돌려도 아무 시험이 빨개지지 않는다. claim lock 을 쥐고 있으므로
두 읽기가 같은 값임이 보장되기 때문이다 (48차에는 lock 이 없어 달랐다). 시험이
약한 것이 아니라 새 불변식 아래 두 코드가 같아진 것이다.

**신고(declared) 6건**: `generation-owns-its-bytes` ·
`idempotent-shares-the-validator` · `public-lifecycle-in-two-publisher-fixture` ·
`proof-until-equals-lease` · `warm-consumer-wiring` · (신규)
`interpreter-set-is-pinned` — 지원 집합 밖 인터프리터가 이 기계에 없어 관측할
수 없다. 대신 회귀가 (a) 지금 인터프리터가 선언 집합 안이고 (b) 대표 구문 넷의
정규형이 golden 과 같음을 매번 확인한다.

### 2-5 이번 라운드가 **스스로 찾은** 결함 넷

기전을 만드는 것과 **쓰는 것**은 다른 검사다. 넷 다 후자에서 나왔다.

| 결함 | 어떻게 드러났나 |
|---|---|
| `assert_not_smoke_provenance` 가 목적지를 안 봐 smoke 뒷절반(보관→복원→검증→재채점)이 통째로 죽어 있었다 | strict smoke 를 실제로 돌렸다 (실패 11건) |
| `make_results.py` 도 같은 형태 — smoke 안 보고서를 못 만들어 `score→hessian→report` 회귀가 죽어 있었다 | 같은 smoke |
| `freeze_cohort()` 가 출발점을 `"active"` 로 못 박아, 기록 없는 cohort(= 정상)를 영영 못 얼렸다 | g3 을 실제로 얼리려다 거부됐다 |
| `_analyzer_provenance()` 의 `__import__(mod)` | 새 동적-해석 검사가 잡았다 |

### 2-6 fixture 가 진실을 가리고 있었다 (세 번)

새 변이 24개 중 셋이 안 물었고, 전부 시험 쪽 문제였다.

| 변이 | 왜 | 고침 |
|---|---|---|
| `finalize-requires-the-credential` | `raises(TypeError)` 가 **다른 이유의** TypeError(`Path(None)`)로 초록 | `match="소유 증명"` |
| `diagnostic-hides-the-credential` | 진단 claim 의 `.token` 을 아무도 안 읽어 guard 가 도달 불가 | readonly claim 에서 직접 확인 |
| `lifecycle-chain-is-verified` | 끝 anchor 가 tip 위조를 먼저 잡아 `prev` 사슬의 고유 증인 없음 | **중간** 줄 위조 사례 추가 |

---

## §3 산출물 — g3 을 얼리고 g4 로

P0-2 를 고치면서 `producer_semantic_sha256` 이 움직였다. 계약 §13.3.2 대로 pin 은
cohort lifetime 동안 고정이므로 g3 을 얼리고 새 cohort 로 갔다. **행 바이트는 안
움직였다** — 움직인 것은 identity 의 정의다.

| 값 | 48차 (g3) | 49차 (g4) |
|---|---|---|
| `producer_semantic_sha256` | `bbb1c4d6fc982610` | `b4701aa33264a753` |
| `compute_sha256` | `6f44ae4a3ce50d4d` | `fa21e7a3eae8e2ca` |
| `row_projection_py_sha256` | `6f4d9d21d38947b9` | `cfa0009662c88ede` |
| RUN_SCOPE `source_digest` | `e77598f97c40e809` | `0a3095ec77da2920` |
| 영수증 core_sha | `b9322e4495d976a4…` | `04048de301732ef5…` (검사 34건) |
| 투영 | `docs/22p_gap/proj_g3` | `docs/22p_gap/proj_g4` (6138행 · restart 30690행) |

freeze 는 이번 라운드에 만든 `freeze_cohort()` 의 첫 실사용이고 원장과 전이
journal 양쪽에 기록했다 (`COHORT_LIFECYCLE.jsonl` seq 2).

---

## §4 무엇을 반증해 주기 바라는가

우선순위 순.

1. **전달 경로에 남은 우회.** coordinator 를 지나지 않고 `grid → fit →
   finalize` 를 완주시킬 수 있는가. 특히 `--attempt-file` 을 주지 않은 grid 가
   남긴 claim 을 다른 주체가 이어받을 수 있는 경로.
2. **소유 증명의 실효성.** `attempt_verifier` 대조를 우회해 phase 를 기록하거나
   원장을 닫을 수 있는가. `inspect_leg_run()`·`LegClaim` 에서 credential 이
   새는 자리.
3. **승인 축의 구멍.** `LEG_SPEC_FIT_KEYS` 밖에 있으면서 **행 바이트를 바꾸는**
   축. `in_digest: null` 결속을 우회해 다른 곡선으로 fit 을 돌리는 경로.
4. **해동.** 원장·journal·anchor 셋을 일관되게 고치지 **않고** frozen cohort 에
   게시하는 경로. §0 에 적은 한계 밖의 것.
5. **finalize 임계 구역.** 두 lock 사이에서 authority 가 바뀌는 창, 또는
   `_already_finalized()` 가 거짓으로 "닫혔다" 를 답하는 상태.
6. **닫힘.** `Import + Attribute` 와 `ImportFrom` 말고 producer 계산을 identity
   밖으로 빼는 문법. 좁게 잡은 동적-해석 경계를 빠져나가는 용법.
7. **변이 coverage artifact 가 거짓 증명인 경우** — 조각이 덮었다고 적었는데
   실제로는 돌지 않은 scenario를 만들 수 있는가.
