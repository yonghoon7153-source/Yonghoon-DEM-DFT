# 50차 게이트 리뷰 요청 — 묶음 9 (실행 전 승인 · 보존 lifecycle)

**대상 커밋**: `71919ce7` 이후 (브랜치 `claude/14-gate-code-review-9qkx05`)
**직전 판정**: 49차 **NO-GO** — "정상 전달 자체는 닫혔지만 권한·원자성·입력
결속·동결·producer identity 가 우회됩니다" (반례 8건)

---

## §0 먼저 — 이번 라운드가 **하지 않은** 것

| 조건 | 상태 |
|---|---|
| **P0-1** producer 결속 — 닫힌 typed manifest 파싱 · 두 payload 압축해제 재해시 · producer 발행 영수증 | **미착수** (49차에 이어 두 라운드째) |
| **P0-8** 경로 무관 typed·sealed 실행 class marker | **미착수.** 판정은 여전히 `is_inside_namespace()` 의 정규 격리(경로 기반) |
| **P0-4** typed CAS/archive/restore/validation/retention 영수증 **소비** | **부분** |
| baseline·sweep1d·wsweep 계획 gate · 실물 object-lock adapter · power-loss 모델 · publisher 전용 OS principal · 외적타당도 #48/#49/#50 | **미착수** |

**남아 있는 표면** (49차 §0 에 적은 것 + 이번 것):

- 원장·journal·anchor **세 파일 모두**에 쓸 수 있는 주체는 역사를 다시 쓸 수
  있다. 막는 것은 "조용한" 되돌림이고 그 밖은 tracked diff 가 바깥 통제다.
- 소유 증명 token 파일(0600)은 같은 uid 의 다른 process 가 읽을 수 있다.
  argv 노출은 막았고(`ps`·`/proc`), 그 밖은 §13.3.1 과 같은 경계다.
- `--attempt-file` 없이 `python -m src.grid` 를 직접 부르면 여전히 claim 을
  발급한다 (token 파일을 안 남기므로 그 실행은 스스로 fit 을 이어갈 수 없고,
  `run.sh` 는 언제나 경로를 넘긴다).

---

## §1 49차 반례 8건 — 전부 재현한 뒤 고쳤다

| # | 49차 반례 | 재현 | 고친 자리 |
|---|---|---|---|
| 1 | 임의 token 으로 만든 `LegClaim` 이 live verifier 확인 없이 phase 기록 | ○ | `LegClaim.phase_done()` 이 **쓰기 지점에서** verifier 대조 |
| 2 | claim 저장 뒤 token 저장 전 `os._exit` → 정상 경로도 회수 불가 | ○ | `open_leg_run()` 이 **token 을 먼저** 굳힌다 |
| 3 | finalize/release 와 늦은 phase 가 모두 성공하고 claim 부활 | ○ | 삭제를 claim 임계 구역 안으로 + 쓰기 지점이 존재 확인 |
| 4 | subset·base-config 가 결과를 바꿔도 승인 digest 동일 | ○ | `row_selection.subset_sha256` · `base_config_digest` 추가 |
| 5 | 승인한 A 대신 교체된 유효 package B 를 계산·게시 | ○ | `halfcell_cache_sha256` 추가 + 입력 결속을 묶음 전체로 |
| 6 | frozen 원장 수정 + journal 삭제만으로 `.head` 를 남긴 채 재게시 | ○ | anchor 가 있으면 journal 도 있어야 한다 (fail-closed) |
| 7 | tuple/docstring/reflection 이 producer digest 밖 · 3.12 golden 실패 | ○ | tuple target · `__doc__` fail-closed · PEP 701 빈 조각 흡수 |
| 8 | 변이 checker 가 replay 0회와 no-op mutant 를 전수 인증 | ○ | `old==new` 거부 · 빈 기대 집합 거부 · 실패 조각은 coverage 미기록 |

**세 축이 반복해서 같은 형태였다**: 검사가 있는 자리와 **쓰는 자리**가 달랐다.
49차는 자격을 `resume_claim()` 에, 결속을 파일 하나에, 순서를 나중에 두었다.

### 특히 짚어 둘 둘

**#2 는 예외가 아니라 순서로 닫았다.** token 이 먼저 있으면 "claim 은 있는데
소유 증명이 없다" 가 **표현 불가능**해진다. 반대로 token 만 남는 것은 무해하다
(가리키는 claim 이 없으므로 권한이 아니고 다음 발급이 덮는다). 실패 시
되돌림도 같은 불변식을 지킨다 — claim 이 남았으면 token 도 남긴다.

**#7 의 3.12 는 실제 원인을 찾았다.** PEP 701 파서가 중첩 format spec 끝에 빈
`Constant('')` 를 붙인다. 정규형이 그것을 흡수한 뒤 3.11·3.12·3.13 이 정규형
digest `ae7a48bde6eb8f9d` 로 일치한다. 회귀가 **실제로 세 인터프리터를 띄워**
대조한다 — 49차는 선언만 하고 확인하지 않았다.

---

## §2 리뷰어가 환경 한계로 분류한 것 중 하나는 **결함**이었다

> "1건은 clean checkout 에서 frozen guard 보다 gitignored 원자료 누락에 먼저
> 걸림"

`results/` 를 통째로 감춰 재현했더니, 원자료가 **있는** 기계에서는 frozen
목적지를 향해 읽기·계산을 먼저 하게 되는 것이 드러났다. 거절은 아무 일도 하기
전에 나야 한다. `_assert_writable()` 을 `build()` 맨 앞으로 옮겼고, 회귀는
**존재하지 않는 다리로도** 물어 그 순서를 고정한다.

나머지 둘(3.12 golden · 두 번째 Python 부재)은 §1 #7 로 닫혔다.

---

## §3 증거

### 3-1 전체 회귀 — **1326 passed · 1 xfailed · 0 failed**

```
tests/test_docs_lint.py       289 passed
나머지                        1037 passed · 1 xfailed
```

clean checkout 흉내(`results/` 감춤): 49차에 보고된 frozen-guard 실패가 사라졌고
남는 것은 gitignored 원자료가 없어 계산할 수 없는 artifact 대조 2건뿐이다.

### 3-2 strict smoke — **rc 0 · 52 ✅ · 0 ❌**

### 3-3 변이 전수 — 99 scenario

```
slice 1..9 (--slice I/9)  : rc 0 · 물었다 93 · 신고 6 · ★ 0
--check-coverage s1..s9   : 등록부 scenario 99 (executable 93 · declared 6) · 관측 99
                            조각 합집합이 등록부 전체를 정확히 덮었다
```

이번 라운드 방어 10개를 등록했고 전부 물었다. 증거는
`docs/22p_gap/mutation_coverage/s1..s9.json`.

**강화된 checker 가 스스로를 잡았다**: slice 7 이 낡은 증인으로 실패했을 때
coverage 가 **안 써졌고**, 합집합 검사가 그 조각의 scenario 넷을 "어느 조각에도
나타나지 않았다" 로 잡았다. 실패한 조각이 증거를 남기지 않는다는 것이 실측됐다.

### 3-4 lifecycle e2e — 3 process · 난입 여섯을 막는다

| 단계 | 확인 |
|---|---|
| grid | 새 발급 · token 0600 · 계획 `running` |
| 난입 a | 모듈 직접 호출 (shell 우회) → `이미 실행 중` |
| 난입 b | 위조 token → `소유 증명이 맞지 않는다` |
| 난입 c | 없는 token 파일 → `소유 증명 파일이 없다` |
| 난입 d~f | `curves.parquet` · `curves_manifest.yaml` · `curves_manifest_start.yaml` 을 **하나씩** 갈아 끼움 → 셋 다 `grid 가 만든 것이 아니다` |
| fit | `소유한 재개` |
| finalize | `executed` · roster 이동 · phase receipt 둘 · `preservation_pending`/`unvalidated` |
| release | 되돌린 뒤 같은 다리를 다시 시작할 수 있다 |

### 3-5 이번에도 fixture 가 진실을 가렸다

`test_the_grid_receipt_binds_every_curve_input...` 이 기대값을
`PHASE_INPUT_KEYS` **에서 유도**했다. 그래서 그 상수를 좁히는 변이에 시험이
함께 좁아져 초록으로 남았다 (변이가 안 물었다 — 실측). 시험이 대상 상수를
읽으면 그 상수를 고정하지 못한다.

---

## §4 산출물 — g4 를 얼리고 g5 로

| 값 | 49차 (g4) | 50차 (g5) |
|---|---|---|
| `producer_semantic_sha256` | `b4701aa33264a753` | `0217b906f6b8bf42` |
| `compute_sha256` | `fa21e7a3eae8e2ca` | `ac6ff10f3f1aaab9` |
| `row_projection_py_sha256` | `cfa0009662c88ede` | `0ee9b706436236c3` |
| 영수증 core_sha | `04048de301732ef5…` | `b691dd8f9e466431…` (검사 34건) |
| validator identity | `0a3095ec77da2920` | `c2abd52735ca73d6` |
| 투영 | `proj_g4` | `proj_g5` (6138행 · restart 30690행) |

**행 바이트는 안 움직였다** — `proj ad598fe77e75afec` 로 g4 와 동일하다. 움직인
것은 identity 의 정의다. freeze 는 `freeze_cohort()` 가 원장과 전이 journal
양쪽에 기록했다 (`COHORT_LIFECYCLE.jsonl` seq 3).

---

## §5 무엇을 반증해 주기 바라는가

우선순위 순. **§0 에 신고한 것을 다시 적는 것은 이미 아는 사실의 재확인이다.**

1. **자격 검사와 쓰기 사이의 남은 틈.** `phase_done()` 말고 claim 상태를
   바꾸는 다른 경로. `LegClaim` 을 직접 만들어 우회할 수 있는 자리.
2. **발급·닫기의 crash 창.** token→claim 순서로 표현 불가능해졌다고 주장하는
   상태를 만드는 sequence. `_already_finalized()` 가 거짓으로 답하는 상태.
3. **승인 축의 남은 구멍.** `LEG_SPEC_FIT_KEYS`·`LEG_SPEC_GRID_KEYS` 밖이면서
   **행 바이트를 바꾸는** 축. 입력 결속(`PHASE_INPUT_KEYS`)이 안 덮는 입력.
4. **해동.** 세 파일을 일관되게 고치지 **않고** frozen cohort 에 게시하는 경로.
5. **닫힘·정규형.** tuple/Attribute/ImportFrom 말고 producer 계산을 identity
   밖으로 빼는 문법. 세 인터프리터에서 정규형이 갈리는 구문.
6. **변이 증거의 거짓.** 조각이 덮었다고 적혔는데 실제로는 안 돈 scenario 를
   만들 수 있는가. 강화된 checker 를 통과하는 no-op 변이.
7. **순서 결함.** 부작용이 판정보다 먼저 일어나는 다른 자리 (`build()` 는
   고쳤다).
