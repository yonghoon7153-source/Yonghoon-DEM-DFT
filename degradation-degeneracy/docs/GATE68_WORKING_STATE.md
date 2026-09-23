# 68차 게이트 리뷰 작업 상태 (정본)

판정: **부분 수용 / 종결 NO-GO** — 2026-09-24 접수. 리뷰어가 고정한 HEAD
`a1979cdf5b9f04234b6a441150e161bd4f0a3ced` · 과학 정본 `743f65bead671bf353ce38027c2e8e457738ec08` ·
`source_digest e9ee7475dea7de1d` (리뷰어가 **직접 재계산**한 값과 우리 실측이 일치). 새 **P2 1건 = G68-T1**.
리뷰 플랫폼 Windows / Python 3.12.14 / pytest 9.1.1.

리뷰 패키지 원본은 `docs/22p_gap/gate68_review/` (zip 바이트 그대로 + `codex/` 풀어 둔 것, zip sha256
`6679445165c2fba82b1dacf5b3dd24228d23bbce512306e6248d8e5fd7f096eb` · `MANIFEST.json` 141 payload, 풀어서
sha 대조 141/141). 회신 원문 `codex/GATE68_REVIEW_KO.md` · 전달용 `codex/GATE68_CLAUDE_REPLY.md`.

**리뷰어가 닫혔다고 인정한 것** (되돌리지 않는다): **G67-N1** (`mutation_replay.py:6112` 의 `g != cand` 가 auto 보다
먼저 — 원래 `repro_boundaries.py` 로 OFF/ON 정직 영수증 entry 수용 · absent 위조 parent/entry 거부) ·
**G67-N2** (`:6019` archive/member 직접 읽기 — 자기 경로를 뺀 ZIP package 와 두 대조군 entry 수용, 바이트 변경·member
소멸·미지원 origin 거부 회귀 포함) · **G67-T1-b** (등록 변이 네 축의 baseline rc 0 · mutant rc 1 · 정확 실패 집합 · call ·
고정 witness 일치 — Windows 독립 국소 대조) · G67-T1 의 **usage error · collect-only · 상속 옵션 경계**.
그리고 리뷰어가 스스로 한정한 것: completeness 단독은 구조 검사 · startup 후 관측 origin 이지 로드 순간 불변 증명 아님 ·
네 축 국소 대조이지 전체 mutation replay 전수 통과가 아님 · 기존 P0-1/P0-4·등록부 격리 미착수를 새 결함으로 세지 않음.

## 발견 원장

| ID | 무엇이 틀렸나 | 자리 | 상태 |
|---|---|---|---|
| **G68-T1** (P2) | `_premise_outcomes()` 는 JUnit testcase 에 error/failure/skipped 자식이 없으면 **passed** 로 읽는다. `--setup-only` child 는 fixture 만 준비하고 **call 단계를 생략**하면서도 testcase 를 자식 없이 적는다 (pytest 문서화 동작) → rc 0 · 정확한 두 testcase · 자식 없음 — 셋 다 맞는데 시험 본문이 한 줄도 안 돈 child 가 **ACCEPTED, 미측정 []** (리뷰어 실제 child 재현, `t1_setup_only/RESULTS.json`; JSON-report plugin 없이 커밋된 `test_g66_08` 직접 호출로도 정상 반환) | `tests/test_gate66_defensive.py` `_premise_outcomes` `:284` · `assert_premise_actually_ran` | 코드 ✔ |

**문서 정정 셋** (리뷰어가 "새 코드 결함과 구분" 해 요구):

| # | 틀린 문장 | 정정 | 자리 |
|---|---|---|---|
| D1 | "`git diff --quiet a31be7a9 HEAD -- degradation-degeneracy` rc 0 · 한 바이트도 불변" | 고정 HEAD 에서는 **rc 1** — 변경은 `GATE68_REQUEST.md` 머리 20 줄이고 그 파일을 빼면 rc 0. **"실행 코드 불변 · 요청문 머리 추가"** 로 좁힌다. 블록을 쓰기 전 tree 의 측정을 최종 HEAD 의 값으로 쓰지 않는다 | `GATE68_REQUEST.md` 발송 전 재확인 표 ✔ |
| D2 | 발송문의 "본 실행(~10 시간) 전 GO 를 받는 요청" | 정본 요청문 §0/§5 는 본실행 GO 를 **두 번 부인**한다. 발송문이 틀렸고 정본이 맞다. 이번 결과를 본실행 승인으로 읽지 않는다 | 발송문(스크래치패드) — 저장소 밖. 이 원장과 §88 에 기록 ✔ |
| D3 | "지운 고아 175 건은 같은 회귀를 다시 돌리면 되돌릴 수 있다" | 재실행은 **새 시각·ID·실행 이력**을 만든다 — 바이트/역사의 복원이 아니다. 삭제 원자료나 당시 inventory 없이는 옛 175 건을 독립 재구성했다고 할 수 없다. "같은 종류가 다시 생긴다" 로 좁힌다 | `GATE68_REQUEST.md` §2-4 ✔ |

**RED 관측**: `tests/test_gate68_defensive.py` (13 node) 첫 실행 — `g68_01`(실제 `--setup-only` child) ·
`g68_03[setup_only]` · `g68_04`(call 줄 제거) **실패**, 합성 사례들도 새 API 부재로 실패. 수정 뒤 gate66 + 67 + 68
**41 passed** (10.02 s).

## 한 줄 요약

**JUnit 은 "돌았다" 를 말하지 않는다** — testcase 가 있고 자식이 없다는 것과 call 단계를 지났다는 것은 다른 명제다.
67차가 "stdout 문자열 → 기계 판독" 으로 옮겼지만, 옮긴 자리(JUnit)도 **단계**를 모른다는 것을 이번에 배웠다.

## 리뷰어 재현기 — 수정 없이 먼저, 그리고 다시

```
                                   수정 전 (a1979cdf)              수정 후
premise control (clean)            ACCEPTED, 미측정 []          →  ACCEPTED, 미측정 []      (대조군 유지)
premise --collect-only             AssertionError (G67-T1)      →  AssertionError (G67-T1)  (유지)
premise --g68-option-does-not-exist AssertionError (G67-T1)     →  AssertionError (G67-T1)  (유지)
premise --setup-only               ACCEPTED, 미측정 []  ✗       →  AssertionError (G68-T1)  ← T1
```

같은 통로다 — 원본 `_premise_run` 의 명시 `env_extra` (리뷰어 `repro_gate68_t1.py` 와 같다). `subprocess` 를 가짜로
만들지 않았고 서명도 그대로다 (`_premise_run(python, env, junit)` · `assert_premise_actually_ran(r, junit)`) — 67차 교훈:
서명 `TypeError` 는 수정의 증거가 아니다.

## 고침

### T1 — 단계 증거를 **exact full node id** 로 소비한다

- `tests/phase_witness.py` (신규): pytest **내장 hook** `pytest_runtest_logreport` 만 쓰는 작은 plugin. 보고서마다
  `{nodeid, when, outcome}` 한 줄을 **즉시 append** 한다 (child 가 도중에 죽어도 그때까지의 단계가 남는다). 외부 plugin 을
  필수화하지 않는다 (리뷰어 조건).
- `_premise_run`: `-p tests.phase_witness --phase-witness=<junit>.phases.jsonl --rootdir=REPO`. 증거 파일 경로는 JUnit 경로에서
  **유도**한다 — 인자를 늘리면 리뷰어 통로가 `TypeError` 로 깨진다. `--rootdir` 고정은 nodeid 의 뿌리를 같게 하기 위해서다.
- `assert_premise_actually_ran`: JUnit 검사(67차) **뒤에** 단계 증거를 본다. node id 집합이 `_PREMISE_NODE_IDS` 와 정확히 같아야
  하고, node 마다 `when=call` 이 **정확히 하나**여야 한다. 사유를 가른다 — **unrun**(call 없음, `--setup-only` 모양) ·
  **duplicate** · **error**(setup/teardown 실패) · failed · skipped(미측정, 목록으로 반환). 그리고 JUnit 결말과 단계 결말이
  **같아야** 한다 (어긋나면 어느 쪽이 child 의 진실인지 모른다). `rc 0` · testcase 수 · 요약 passed 수로 **대체하지 않고**,
  옵션 문자열을 차단하지도 않는다.
- 회귀 `tests/test_gate68_defensive.py`: 실제 child 셋(setup-only · collect-only · usage error) + clean 대조군 둘 + **실제 clean
  child 의 산출을 고쳐서** 묻는 합성 여섯(call 줄 제거 · call 중복 · setup 실패 · call skipped=미측정 · 다른 파일 node ·
  JUnit↔단계 불일치) + 내장 hook 확인.

### 변이 등록부 (68차)

| 이름 | 자리 | 되돌리는 것 | 기대 실패 (관측 = 선언) | 증인 |
|---|---|---|---|---|
| `the-premise-checks-the-call-phase-g68` | `test_gate66_defensive.py` `_call_evidence` | call 기록 없는 node 를 `"unrun"` 대신 `"passed"` 로 (JUnit 만 보던 전 판의 뜻) | `g68_01` · `g68_03[setup_only]` · `g68_04` (3 node, call 단계) | `Failed: DID NOT RAISE AssertionError` |

`--check-preimages` 모든 지점 1회 · `-k premise` 재생(g66 controlled-env · g67 actually-ran · g68 call-phase) 통과.

## 우리가 스스로 찾은 것 — 리뷰 패키지 보존의 줄끝 정규화

68차 패키지를 `docs/22p_gap/gate68_review/codex/` 에 풀어 커밋하자 git 이 **CRLF→LF 정규화**를 걸었다 (dd `.gitattributes` 의
`* text=auto eol=lf`). 커밋된 파일 141 개 중 **64 개가 MANIFEST 의 sha256 과 어긋났다** (zip 바이트는 온전). 같은 방법으로
확인하니 **67차 패키지도 350 중 174 개**, 66차도 같은 문제였다 — 이전 두 라운드의 "패키지 원본 보존" 은 zip 은 맞고 풀어 둔
트리는 줄끝이 바뀐 사본이었다. 고침: `docs/22p_gap/gate6{6,7,8}_review/** -text !eol` 규칙을 **먼저** 커밋하고, 세 트리를
index 에서 빼고 원본 바이트로 다시 넣었다 (68차는 working tree, 66·67차는 커밋된 zip 에서 재추출). 커밋 뒤 `git show HEAD:`
재대조 **141/141 · 350/350 · 107/107**. bms 쪽 `preserve_handoff.sh` 가 r320_timecap 에서 배운 순서 그대로다 —
dd 쪽은 그 규칙이 없었다.

## 이 라운드가 하지 않은 것

- **본 실행** — 리뷰어가 승인하지 않았고 요청문도 요청하지 않는다. `F50b (b)` 그대로.
- N1/N2/T1-b 를 새 설계로 다시 열지 않았다 (리뷰어: "필요 없다").
- 기존 P0-1/P0-4·등록부 격리·trusted launcher 미착수 그대로 (리뷰어 Q5 답: 읽기 전용 영향·의존성 지도와 판정 계약을 먼저).
- Linux native locking · `/proc` 경로는 이 컨테이너 실측이고 리뷰어는 Windows 라 그쪽에서 미실행 — 우리 숫자를 수신 측 수치로 바꾸지 않는다.

## 등록부 delta

69차 요청문 커밋 직전 실측: tracked **367** · 디스크 **367** · `git status` 미추적 **0** · 삭제 **0**.
