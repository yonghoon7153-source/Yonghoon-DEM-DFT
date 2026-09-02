# 56차 게이트 리뷰 요청 — 묶음 9 (실행 전 승인 · 보존 lifecycle)

**대상 커밋**: `168f0071` (브랜치 `claude/14-gate-code-review-9qkx05`) — 코드·시험·산출물(g11)·변이 전수 증거를 전부 담은 커밋이다. 이 줄을 고치는 커밋만 그 뒤에 하나 더 있다 (내용 동일).
**직전 판정**: 55차 **NO-GO** — P0 9건 · P1 2건

---

## §0 먼저 — 이번 라운드가 **하지 않은** 것

| 조건 | 상태 |
|---|---|
| **P0-1** producer 결속 — 닫힌 typed manifest 파싱 · 두 payload 압축해제 재해시 · producer 발행 영수증 | **미착수** (49차부터 **여덟 라운드째**) |
| **P0-8** 경로 무관 typed·sealed 실행 class marker | **미착수** |
| trusted launcher 의 source 측정 | **미착수** |
| **P0-4** typed 보존 영수증 **소비** | **부분** |
| 변이 증거의 **독립 replay** | **미착수** — 56차는 증거의 결속을 넓혔을 뿐, checker 가 스스로 재생하지는 않는다 |
| baseline·sweep1d·wsweep 계획 gate · 실물 object-lock adapter · power-loss 모델 · publisher 전용 OS principal · 외적타당도 #48/#49/#50 | **미착수** |

55차 판정문의 마지막 문단에 동의한다 — 위 항목들은 반례와 **별개의 독립 GO
전제**로 그대로 남는다.

**남아 있는 표면** (55차 신고분 + 이번에 새로 확인한 것):

- 원장·journal·anchor·`.FROZEN` 전부에 쓸 수 있는 주체는 역사를 다시 쓸 수 있다.
- 소유 증명 token(0600)은 같은 uid 의 다른 process 가 읽는다.
- 변이 증거의 **pytest report 자체를 손으로 위조**하면 checker 를 통과한다.
- lock 은 여전히 같은 파일시스템의 `flock` 이다.
- `_execution_receipt()` 의 `BOUND_ENV`·`BOUND_INPUT_GLOBS` 는 **손으로 적은
  목록**이다. 새 환경변수·설정 파일을 도입하면서 여기 안 적으면 증거 밖이
  된다 (§3-6 에서 반증해 주기 바란다).
- mountinfo 를 못 읽으면 이제 **거부**한다 (55차의 fail-open 을 닫았다). 대신
  mountinfo 를 읽을 수 있는 Linux 를 전제한다.

---

## §1 55차 반례 11건 — 전부 재현한 뒤 고쳤다

| # | 55차 반례 | 재현 | 고친 자리 |
|---|---|---|---|
| P0-1 | token symlink 가 **자기 첫 쓰기로** attempt lock identity 를 바꾼다 | ○ | 해석을 공개 진입에서 한 번만 하고 그 값을 돌려준다 · symlink·hardlink token 경로는 첫 부작용 앞에서 거부 |
| P0-2 | hardlink ledger alias 가 하나의 승인 원장을 두 authority 로 가른다 | ○ | `canonical_ledger()` 가 `st_nlink != 1` 원장을 거부 — `resolve()` 는 hardlink 를 합치지 못한다 |
| P0-3 | 원장 commit 뒤 claim 삭제에서 죽으면 재시도 불가 | ○ | `attempt_verifier` 를 **원장에** 봉인하고, claim 이 없을 때 원장으로 소유자를 인증해 완주 |
| P0-4 | 연속 partial append 로 journal 이 anchor 보다 두 줄 앞서면 복구 불능 | ○ | append 가 새 줄을 붙이기 **전에** 미완을 완주(`_finish_pending_anchor`) · repair 도 같은 몸통 |
| P0-5 | mountinfo 의 `\040` 미해제로 공백 alias 게시 성공 | ○ | `proc_pid_mountinfo(5)` 대로 octal unescape |
| P0-6 | 중첩 bind 에서 **바깥** mount 를 먼저 선택 | ○ | 매 단계 **가장 깊은** mountpoint 선택 |
| P0-7 | `root=/child` 를 namespace 경로로 오해 | ○ | major:minor 로 **같은 filesystem 을 보여 주는 창**을 찾아 해석 · 못 찾으면 게시 거부 |
| P0-8 | crossed `src.scoring` 의 `MODULE_EFFECTS` 가 closure 밖 | ○ | 닫힘에 들어오는 **모든** module 에 seed |
| P0-9 | `"__" + "globals__"` 조립 이름이 digest 를 안 움직인다 | ○ | 조각 수집 대신 **exact 상수 평가**(`_exact_const`) · 계산 못 하면 멈춘다 |
| P1-1 | tree digest 에 checkout 절대경로가 들어가 clean checkout 에서 rc 1 | ○ | 저장소 상대 POSIX 경로로 해시 |
| P1-2 | dependency·환경변수·비-Python 설정이 증거 밖 | ○ | `_execution_receipt()` — interpreter · 설치 패키지 · `BOUND_ENV` · requirements/configs/scripts |

### 이번 라운드의 형태 둘

**① 검사를 좁히게 만든 것이 다음 반례의 통로였다.** 55차에 P0-5②(동적 dunder)
규칙을 걸었더니 producer **자신의** 동적 `getattr` 두 자리가 먼저 걸렸고
(`_ast_canon` 의 `node._fields` 루프, `_module_defs` 의 `attr` 루프) 그래서
규칙을 좁혔다. 리뷰어는 정확히 그 틈으로 들어왔다(P0-9). 이번엔 **내 코드를
먼저 고쳐서**(`ast.iter_fields`·명시 접근) 규칙을 완전히 닫았다.

**② 모델이 틀리면 파싱을 고쳐도 안 닫힌다.** P0-5·6·7 은 세 개의 버그가 아니라
`(mountpoint, root)` 문자열 치환이라는 **한 모델의 세 얼굴**이다. octal unescape
만 고치면 P0-6·7 이 남고, 깊이 선택만 고치면 P0-5·7 이 남는다. mount ID ·
parent ID · major:minor 를 들고 다니는 mount 그래프로 갈아엎어야 셋이 함께
닫힌다.

---

## §2 증거

### 2-1 전체 회귀 — **1410 passed · 1 xfailed · 0 failed** (803s)

### 2-2 strict smoke — **rc 0 · 52 ✅ · 0 ❌**

### 2-3 변이 전수 — 등록부 **176 scenario** (executable 168 · declared 8 · site 197)

165 → 176. 56차 방어 11건을 등록했고, 56차 수정으로 원문이 움직인 낡은
preimage 4건을 갱신했다 (`--check-preimages` 가 그것을 먼저 잡았다).

12조각을 **HEAD 를 고정한 채**(`b91e49c0`) 끝까지 돌렸고 조각별 문제는 0건이다.
`--check-coverage` 는 `등록부 scenario 176 (executable 168 · declared 8) ·
조각 12개에서 관측 176 · 조각 합집합이 등록부 전체를 정확히 덮었다` (rc 0).

**정본은 커밋된 증거 파일이다** — `docs/22p_gap/mutation_coverage/s1..s12.json`
과 그 옆의 `reports/`.

### 2-4 증거 층이 잡은 것 넷

**① 새 방어가 옛 변이 둘을 가렸다.** P0-8(건너간 module 의 `MODULE_EFFECTS`
무조건 seed)이 들어가자 `producer-crosses-into-scoring` 과
`closure-follows-module-aliases` 가 안 물었다 — seed 가 scoring 의 내용을 여전히
닫힘에 넣으므로 건너기만 끊어서는 digest 가 움직인다. 54차
`receipt-verdict-is-fail-closed` 와 같은 형태이고, 답은 방어를 지우는 것이
아니라 **함께 되돌리는** 것이라 둘 다 2-site MULTI 로 옮겼다.

**② 변이가 여전히 "거부" 로 끝나면 안 문다.** `mount-root-is-filesystem-relative`
와 `assembled-names-are-exactly-evaluated` 는 처음 등록한 지점을 꺼도 다른
fail-closed 가 잡아 시험이 초록이었다. 지점을 실제 **fail-open 자리**로 옮겼다
(전자는 55차의 순진한 치환으로 되돌리는 자리, 후자는 평가 세 갈래 + fail-closed
자체를 함께 되돌리는 4-site MULTI).

**③ 시험의 축을 잘못 겨누면 우연히 초록이 난다.** P0-1 을 "두 다리가 동시에
running" 으로 쓰면 순차 실행에서 **내용 검사**가 우연히 막아 통과한다 — 그건
다른 guard 다. 실제 축인 "같은 pathname 의 배타 지점이 정상 발급 하나로
움직이는가" 로 바꿔야 RED 가 났다.

**④ 증인에 휘발성 값이 섞였다** (임시 경로·digest 쌍). 의미 부분만 남겼다.

### 2-5 산출물 — g10 을 얼리고 g11 로

| 값 | 55차 (g10) | 56차 (g11) |
|---|---|---|
| `producer_semantic_sha256` | `effc3eef2e23fabd` | `eb4555abd9490dd0` |
| `compute_sha256` | `0f59ad72af31703e` | `872ca5b9046ca703` |
| `row_projection_py_sha256` | `969916b10e845036` | `b9d895261c7a9df1` |
| 영수증 core_sha | `2fd81e7015a279bb…` | `79ed20cd3fd34034…` |
| validator identity | `82aeae57631f6c0c` | `9c7e5e71cbef8f05` |
| 투영 | `proj_g10` | `proj_g11` |

**행 바이트는 안 움직였다** — 재생성 출력이 `proj ad598fe77e75afec` 로 g4~g10 과
동일하다 (6138행 · restart 30690행 · 전체 True · 봉인일치 True). 움직인 것은
identity 의 **정의**다. cross-cohort 비교는 여전히 금지다.

---

## §3 무엇을 반증해 주기 바라는가

우선순위 순. **§0 에 신고한 것을 다시 적는 것은 이미 아는 사실의 재확인이다.**

1. **mount 그래프의 남은 축.** `_through_bind_mounts()` 가 `wins` 후보 중
   `root` 가 가장 짧은 것을 고른다 — 그 선택이 틀리는 구성 (같은 dev 에 서로
   겹치지 않는 두 창, `--rbind`, mount namespace 분리, 32회 반복 상한 초과).
   후보가 없으면 거부하는데, **정상 운용에서 거부되는** 구성이 있는가.
2. **경로 고정의 남은 alias.** token·원장에서 symlink·hardlink 를 거부했다.
   그 밖의 alias 로 같은 분기를 만들 수 있는가 (bind mount 된 token 디렉터리,
   대소문자 무시 파일시스템, `//` · 유니코드 정규화 차이).
3. **원장이 봉인한 `attempt_verifier`.** 그것으로 인증되는 상태에서 두 번
   finalize 하거나, 남의 실행을 닫을 수 있는 순서. 55차 이전 기록(verifier 가
   없는 leg)이 만드는 경로.
4. **미완 완주 protocol.** `_finish_pending_anchor()` 를 지나면서도 journal 이
   anchor 를 앞서는 상태를 만들 수 있는가. 완주 자체가 죽는 경우.
5. **producer 닫힘.** `_exact_const()` 가 **계산해 버리는** 위험한 식
   (`str.format` · `%` · `bytes.decode` · 슬라이스 조합). 반대로 너무 넓어
   producer 자신의 정상 코드를 막는 자리.
6. **증거의 목록 의존.** `BOUND_ENV` 와 `BOUND_INPUT_GLOBS` 는 손으로 적었다 —
   시험 결과를 바꾸면서 그 목록 밖인 것 (환경변수 · 설정 · 설치 경로 · locale ·
   시간대 · 파일시스템 특성).
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
계산 불가로 실패할 수 있다. 지원 인터프리터가 하나뿐이면 정규형 회귀 2건이
`len(seen) >= 2` 로 실패한다. mount 회귀 넷은 bind mount 를 만들 수 없는
환경에서 skip 한다. lifecycle E2E 는 `tqdm` 이 필요하다 (55차 검토 환경에서
그것 때문에 미완이었다 — `pip install -r requirements.txt` 를 먼저 부탁한다).

**55차 P1-1 이 닫혔으므로 커밋된 coverage 는 이제 clean checkout 에서
portable 하게 검증된다** — 그것이 이번에 가장 먼저 고친 것이다.
