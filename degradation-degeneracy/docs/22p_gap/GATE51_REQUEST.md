# 51차 게이트 리뷰 요청 — 묶음 9 (실행 전 승인 · 보존 lifecycle)

**대상 커밋**: `1ca133ae` 이후 (브랜치 `claude/14-gate-code-review-9qkx05`)
**직전 판정**: 50차 **NO-GO** — "49차의 입력 key 와 쓰기 지점 검사를 늘렸지만,
그 검사가 lifecycle generation 또는 계산이 실제 소비한 immutable bytes 와
**구조적으로 묶이지 않았다**" (새 P0 9건 · P1 5건)

---

## §0 먼저 — 이번 라운드가 **하지 않은** 것

| 조건 | 상태 |
|---|---|
| **P0-1** producer 결속 — 닫힌 typed manifest 파싱 · 두 payload 압축해제 재해시 · producer 발행 영수증 | **미착수** (49차부터 세 라운드째) |
| **P0-8** 경로 무관 typed·sealed 실행 class marker | **미착수.** 판정은 여전히 `is_inside_namespace()` 의 정규 격리(경로 기반) |
| **P0-4** typed CAS/archive/restore/validation/retention 영수증 **소비** | **부분** |
| baseline·sweep1d·wsweep 계획 gate · 실물 object-lock adapter · power-loss 모델 · publisher 전용 OS principal · 외적타당도 #48/#49/#50 | **미착수** |

**남아 있는 표면** (앞 라운드에 적은 것 + 이번 것):

- 원장·journal·anchor **세 파일 모두**에 쓸 수 있는 주체는 역사를 다시 쓸 수
  있다. 막는 것은 "조용한" 되돌림이고 그 밖은 tracked diff 가 바깥 통제다.
  51차가 좁힌 것은 **한 파일**(원장의 cohort ID)만으로 되던 경로다.
- 소유 증명 token 파일(0600)은 같은 uid 의 다른 process 가 읽을 수 있다.
  argv 노출은 막았고(`ps`·`/proc`), 그 밖은 §13.3.1 과 같은 경계다.
- `--attempt-file` 없이 `python -m src.grid` 를 직접 부르면 여전히 claim 을
  발급한다 (token 파일을 안 남기므로 그 실행은 스스로 fit 을 이어갈 수 없고,
  `run.sh` 는 언제나 경로를 넘긴다).
- lifecycle journal 의 schema 를 옮기면서 사슬을 **다시 계산했다**. 그 재계산이
  역사를 안 고쳤다는 것은 회귀가 재계산 전 파일의 digest 와 그때의 네 줄을
  고정해 확인한다 (§3-6). 재계산 자체를 없앨 수는 없다.

---

## §1 50차 반례 14건 — 전부 재현한 뒤 고쳤다

| # | 50차 반례 | 재현 | 고친 자리 |
|---|---|---|---|
| P0-L1 | 두 번째 정상 `open_leg_run()` 이 살아 있는 owner token 을 먼저 덮는다 | ○ | 발급 전체가 claim 임계 구역 안. 살아 있는 claim 을 **먼저** 판정 |
| P0-L2a | 옛 release 의 늦은 cleanup 이 새 attempt 의 token 을 지운다 | ○ | `_unlink_token_generation()` — 내가 쓴 token 일 때만 |
| P0-L2b | stale `LegClaim(A)` 가 B 의 claim 을 지운다 | ○ | `_assert_live_attempt()` 를 `_abandon_claim()` 쓰기 지점에 |
| P0-L2c | `LegClaim(..., token=None)` 로 owner 취소 | ○ | 같은 검사 (타입 이름이 아니라 verifier 대조가 authority) |
| P0-L3a | release crash → 회수 불가능한 `running` orphan (`child_rc=50`) | ○ | 원장 전이 **먼저**, claim 삭제 나중 |
| P0-L3b | `os.replace` 뒤 fsync 오류를 미커밋으로 보고 claim·token 삭제 | ○ | `_plan_status()` 로 살아 있는 원장을 다시 읽고 rollback 결정 |
| P0-A1 | objective weight payload 가 승인 밖 (J 0.0114 ≠ 0.1329) | ○ | `objectives_digest` |
| P0-A2 | `extends` 부모가 승인 밖 (lli_hat 0.017343 ≠ 0.017400) | ○ | `base_config_digest` 를 dependency **closure 전체**로 |
| P0-A3 | 세 파일 대조 뒤 snapshot 전에 package 전체 교체 | ○ | `_stage_fit_inputs()` — gate **앞에서** immutable 사본 |
| P0-A4 | discharged-state cache 가 grid 승인 밖 (q_mah 5621.148 ≠ 5540.777) | ○ | `discharged_cache_sha256` + 본체가 **승인한 바이트만** 파싱 |
| P0-F | 원장 한 파일만 고쳐 frozen 디렉터리에 재게시 | ○ | journal 이 **목적지(`dir`)** 를 봉인 |
| P0-I a | module-level `for` binding 이 identity 밖 | ○ | 복합문 안으로 · 모르는 문에서 멈춘다 |
| P0-I b | aliased `getattr` 로 stripped docstring 을 읽는다 | ○ | 정규형이 docstring 을 **버리지 않는다** |
| P1-E1 | external `in_digest` 가 두 manifest digest 를 버린다 | ○ | `in_digest` 를 **묶음 package digest** 로 |
| P1-E2 | coverage 가 semantic no-op·replay 0회를 인증 | ○ | 정규형 부등식 + artifact 결속 (schema v2) |
| P1-O | freeze 가 fail-closed 인데 재시도 불가 | ○ | 남은 원장 전이를 완주 |
| P1-C | 계약 §13.4 와 executable schema 불일치 | ○ | 계약 갱신 + 두 곳 일치를 강제하는 회귀 |
| P1-P | caller token 경로가 claim authority 와 alias | ○ | `_assert_token_path_disjoint()` + 기본 자리 이동 |

### 특히 짚어 둘 셋

**순서는 CAS 가 아니었다.** 50차는 자격 검사를 쓰기 지점으로 옮겼다고 했지만
옮긴 것은 `phase_done()` **하나뿐**이었다. 읽고 나서 쓰는 모든 자리가 같은
질문을 해야 한다 — "지금 디스크에 있는 것이 내가 읽은 그것인가". 51차는 그
질문을 네 자리에 넣었다: 발급 · phase 기록 · 되돌림 · token 삭제.

**회수 가능성이 순서를 정한다.** release 의 두 쓰기를 claim→원장으로 두면 그
사이 crash 의 중간 상태가 어떤 공개 API 로도 회수 불가다. 뒤집으면 "claim 은
있고 계획은 `planned`" 이고 같은 소유 증명으로 그냥 다시 되돌리면 된다.
freeze 도 같은 형태였다 — 안전한 중간 상태를 만드는 것과 **거기서 나갈 길을
두는 것**은 다른 일이다.

**철자 목록은 종결 조건이 아니다.** 49차가 `import ... as`, 50차가 tuple
target 을 더했고 51차 반례는 module-level `for` 였다. 그리고 50차가 막은
`.__doc__` 철자는 `read = getattr` 한 줄로 피해 갔다. 형태 열거를 그만두고
(a) 모르는 module-scope 문에서 멈추고 (b) 정규형이 **아무 것도 안 버리게** 했다.

---

## §2 증거

### 2-1 전체 회귀 — **1348 passed · 1 xfailed · 0 failed**

### 2-2 strict smoke — **rc 0 · 52 ✅ · 0 ❌**

### 2-3 변이 전수 — 114 scenario

```
slice 1..11 (--slice I/11) : rc 0 · executable 108 · 신고 6 · ★ 0
--check-coverage s1..s11   : 등록부 114 (executable 108 · declared 6) · 관측 114
                             조각 합집합이 등록부 전체를 정확히 덮었다
```

이번 라운드 방어 16개를 등록했고 전부 물었다. artifact 는 schema **v2** 이며
등록부·EXPECT·runner·HEAD·실행 transcript digest 를 담고, checker 가 그 다섯을
살아 있는 값과 대조한다 — 50차 반례(`replay_calls=0` 으로 전수 인증)가 닫힌다.

### 2-4 lifecycle e2e — 3 process · 난입 여섯

| 단계 | 확인 |
|---|---|
| grid | 새 발급 · token 0600 · 계획 `running` |
| 난입 a~c | 모듈 직접 호출 · 위조 token · 없는 token 파일 |
| 난입 d~f | 세 곡선 파일을 **하나씩** 갈아 끼움 → 셋 다 거부 |
| fit → finalize → release | 소유한 재개 · `executed` · 되돌린 뒤 재시작 |

### 2-5 산출물 — g5 를 얼리고 g6 로

| 값 | 50차 (g5) | 51차 (g6) |
|---|---|---|
| `producer_semantic_sha256` | `0217b906f6b8bf42` | `632232332b015def` |
| `compute_sha256` | `ac6ff10f3f1aaab9` | `730e673e74edb8ae` |
| `row_projection_py_sha256` | `0ee9b706436236c3` | `06e8dcfe58946e9e` |
| 영수증 core_sha | `b691dd8f9e466431…` | `a54c2b0af8905508…` (검사 34건) |
| validator identity | `c2abd52735ca73d6` | `c9cd0b2955956e77` |
| 투영 | `proj_g5` | `proj_g6` (6138행 · restart 30690행) |

**행 바이트는 안 움직였다** — `proj ad598fe77e75afec` 로 g4·g5 와 동일하다.
움직인 것은 identity 의 정의다.

### 2-6 lifecycle journal schema 이동을 증명한다

`dir` 을 더하려면 append-only 사슬을 다시 계산해야 하고, 그 쓰기는 정확히
"조용한 되돌림" 과 같은 모양이다.
`test_the_lifecycle_schema_migration_did_not_rewrite_history` 가 재계산 **전**
파일의 digest(`a3b2dbed…`)와 그때의 네 줄 `(cohort_id, from, to, at)` 을
고정하고, 지금 journal 의 앞 네 줄이 그 값을 그대로 담고 `dir` 만 더해졌는지
본다.

### 2-7 이번에도 시험이 **쓰는 자리**를 안 봤다

`fit-stages-its-inputs-before-the-gate` 변이가 처음에 안 물었다 — 시험이
`_stage_fit_inputs()` 를 직접 불러 사본의 성질만 봤기 때문이다. 그 함수가
아무리 옳아도 `run_fit()` 이 원본 경로를 넘기면 아무 것도 닫히지 않는다.
`run_fit()` 이 본체에 무엇을 넘기는지 보는 시험으로 바꾸니 물었다 (50차의
`PHASE_INPUT_KEYS` 자기참조와 같은 축).

---

## §3 무엇을 반증해 주기 바라는가

우선순위 순. **§0 에 신고한 것을 다시 적는 것은 이미 아는 사실의 재확인이다.**

1. **generation 이 안 닿는 자리.** 읽고 나서 쓰는데 live attempt 를 다시 안
   보는 lifecycle 경로. `finalize_leg()` 의 두 lock 사이. `resume_claim()` 이
   돌려준 handle 이 오래 사는 경로.
2. **crash 창.** 51차가 "회수 가능" 이라고 주장하는 중간 상태 중 실제로는
   막힌 것. 두 lock 을 중첩해 쥔 구간에서 죽었을 때. `_plan_status()` 재독이
   거짓을 답하는 상태.
3. **승인 축의 남은 구멍.** `LEG_SPEC_FIT_KEYS`·`LEG_SPEC_GRID_KEYS` 밖이면서
   **행 바이트를 바꾸는** 축. staging 이 안 뜨는 입력. `objectives_digest` 나
   `_config_closure_digest()` 가 접는 값.
4. **검증한 bytes ≠ 소비한 bytes 의 남은 자리.** staging 사본을 뜬 뒤에도
   원본 pathname 을 다시 여는 경로. grid 쪽(`cache_bytes` 밖)의 같은 형태.
5. **동결.** journal 의 `dir` 봉인을 우회해 frozen 목적지에 게시하는 경로.
   symlink·bind mount·대소문자로 같은 디렉터리를 다른 canonical 경로로 보이게
   하기.
6. **닫힘·정규형.** `_MODULE_COMPOUND`/`_MODULE_NONBINDING` 이 잘못 분류한 문.
   docstring 을 남긴 뒤에도 정규형이 **여전히 버리는** 것 중 계산이 읽을 수
   있는 것. 세 인터프리터에서 정규형이 갈리는 구문.
7. **증거의 거짓.** v2 결속을 통과하면서 실제로는 안 돈 조각. 정규형 부등식을
   통과하는 semantic no-op.
8. **순서 결함.** 부작용·판정 순서가 뒤바뀐 다른 자리 (`build()` 는 50차에,
   fit gate 는 51차에 고쳤다).

---

## §4 검증 명령

```
python -m pytest tests/ -q
./scripts/smoke_e2e.sh
python3 docs/22p_gap/mutation_replay.py --check-preimages
python3 docs/22p_gap/mutation_replay.py --slice I/11 --emit-coverage docs/22p_gap/mutation_coverage/sI.json
python3 docs/22p_gap/mutation_replay.py --check-coverage docs/22p_gap/mutation_coverage/s*.json
python -m pytest tests/test_lifecycle_e2e.py -q
```

원자료(`results/`)는 gitignored 이므로 clean checkout 에서는 artifact 대조가
계산 불가로 실패할 수 있다 — 알려진 환경 한계다. 다만 **환경 한계로 보이는
실패가 사실은 순서·fail-open 결함**일 수 있다는 것이 50차에 실측됐으니
(`build()` 건) 한 번은 의심해 주기 바란다.
