# 69차 게이트 리뷰 요청 — 68차 1건(G68-T1) 대응 + 문서 정정 셋

읽는 쪽은 LLM 리뷰어다. 밀도 우선, 완충 문장 없음. **요청문은 증거가 아니다** — 아래 명령을
재실행해 검증하는 것을 전제로 쓴다. 우리 환경에서만 되는 것은 그렇게 밝힌다.

**이 요청문은 본실행 GO 를 요청하지 않는다** (68차 리뷰어 D2 지적 — 직전 발송문이 "약 10 시간 본실행 GO 요청" 이라 적어
정본 요청문과 모순됐다. 이번에는 발송문과 요청문이 같은 말을 한다).

## 판정 대상 (이 블록이 정본이다)

| 항목 | 값 |
|---|---|
| 브랜치 | 루트 `CLAUDE.md` 하드룰 1 의 작업 브랜치 (요청문에 이름을 옮겨 적지 않는다) |
| **판정 대상 코드** | **`743f65bead671bf353ce38027c2e8e457738ec08`** (RUN_SCOPE 를 마지막으로 건드린 커밋 — 64~68차와 같다) |
| `source_digest` | **`e9ee7475dea7de1d`** — 68차 리뷰어가 직접 재계산한 값과 같다 |
| 검토할 HEAD | 브랜치 head. **이 요청문을 담은 커밋의 SHA 를 발송문에 적는다** — 그 뒤 커밋이 있으면 그 diff 도 발송문에 적는다 |
| 직전 판정 | 68차 **부분 수용 / 종결 NO-GO** — P2 1 (G68-T1) + 문서 정정 셋 (D1·D2·D3) |
| 접수·대응 원장 | `docs/GATE68_WORKING_STATE.md` · 원장 §87·§88 · 리뷰 패키지 원본 `docs/22p_gap/gate68_review/` (zip sha256 `6679445165c2fba82b1dacf5b3dd24228d23bbce512306e6248d8e5fd7f096eb`, MANIFEST 141/141) |

> ```
> git fetch origin <하드룰 1 의 브랜치> && git checkout FETCH_HEAD
> cd degradation-degeneracy
> python3 -c "import sys; sys.path.insert(0,'.'); from src.io import source_digest; print(source_digest())"
> # → e9ee7475dea7de1d
> git log --oneline 743f65b..HEAD -- src tools configs scripts run.sh requirements*.txt
> # → 빈 출력
> ```

판정에 봐야 할 파일은 전부 RUN_SCOPE 밖이다: `tests/phase_witness.py`(신규) · `tests/test_gate66_defensive.py`
(`_premise_run` · `_phase_witness_path` · `_phase_records` · `_call_evidence` · `assert_premise_actually_ran`) ·
`tests/test_gate68_defensive.py`(신규) · `docs/22p_gap/mutation_replay.py`(등록 1건).

**동일성 문장 (68차 D1 교훈 — 커밋 뒤에 잰다):** 발송문에 적는 SHA 에서 `git diff --stat a1979cdf <SHA> -- degradation-degeneracy`
는 위 네 파일 + 문서(`GATE68_WORKING_STATE.md` 신규 · `08_REVIEW_RESPONSE.md` §87·§88 · `GATE68_REQUEST.md` 정정 둘 · 이 요청문 ·
`.gitattributes` 규칙 3 줄 · `docs/22p_gap/gate6{6,7,8}_review/` 트리 재추가) 다. RUN_SCOPE 는 빈 출력이다.

---

## §0 이번 라운드가 **하지 않은** 것

- 본실행 GO 를 요청하지 않는다. `F50b` 는 (b) 그대로 — 다음 RUN_SCOPE 변경에 묶는다.
- N1 / N2 / T1-b 를 다시 열지 않았다 (68차: "새 설계로 다시 열 필요 없다").
- P0-1 · P0-4 · 등록부 격리 · trusted launcher 는 미착수 그대로 (68차 Q5: 읽기 전용 영향·의존성 지도와 판정 계약을 먼저).
- 등록부 복원 · class 변경 · 삭제 없음.
- 실데이터 · COMSOL · 장시간 실행 없음.

## §1 G68-T1 — JUnit 은 "돌았다" 를 말하지 않는다

| 발견 | 무엇이 틀렸나 | 왜 | 고침 | 확인 |
|---|---|---|---|---|
| **G68-T1** (P2) | `_premise_outcomes()` 가 JUnit testcase 에 자식이 없으면 passed 로 읽고, `assert_premise_actually_ran` 은 rc 0 · 정확한 두 testcase · 그 상태만 본다 → `--setup-only` child(call 0 개)가 **ACCEPTED, 미측정 []** | 67차가 증거를 stdout 문자열에서 JUnit 으로 옮겼지만 JUnit 도 **단계**를 모른다 | **단계 증거**: `tests/phase_witness.py` — pytest 내장 hook `pytest_runtest_logreport` 만 쓰는 plugin, 보고서마다 `{nodeid, when, outcome}` 을 즉시 append. `_premise_run` 이 `-p tests.phase_witness --rootdir=REPO --phase-witness=<junit>.phases.jsonl` 로 싣는다 (경로는 JUnit 에서 **유도** — 두 서명 불변). 소비자는 JUnit 검사 **뒤에** exact full node id 마다 `when=call` 이 **정확히 하나**이고 결말이 passed/skipped 인지 본다. 사유를 가른다: `unrun`(`--setup-only` 모양) · `duplicate` · `error`(setup/teardown 실패) · node 집합 불일치 · JUnit↔단계 불일치. rc 0 · testcase 수 · 요약 passed 수로 **대체하지 않고** 옵션 문자열을 차단하지 않는다 | 리뷰어 통로(`_premise_run(python, {"PYTEST_ADDOPTS": "--setup-only"}, junit)` → `assert_premise_actually_ran(r, junit)`) 에서 **AssertionError (G68-T1)** · clean 대조군 ACCEPTED 유지 · collect-only / usage error 는 G67-T1 사유 유지 |

### 1-1. 회귀 `tests/test_gate68_defensive.py` (13 node)

| 시험 | 무엇을 묻나 | 수정 전 | 수정 후 |
|---|---|---|---|
| `g68_01` | **실제** `--setup-only` child 를 거부하는가, 사유가 G68-T1 인가 | ✗ (ACCEPTED) | ✓ |
| `g68_02[clean|nousersite]` | 같은 소비 경로에서 정상 child 는 통과하는가 | ✓ | ✓ |
| `g68_03[collect_only|usage_error|setup_only]` | 안 돈 child 세 모양이 모두 AssertionError 이고 사유가 서로 다른가 | ✗ (setup_only) | ✓ |
| `g68_04`~`g68_09` | **실제 clean child 의 산출을 고쳐서** — call 줄 제거 · call 중복 · setup 실패 · call skipped(미측정 목록) · 다른 파일 node · JUnit↔단계 불일치 | ✗ (API 부재) | ✓ |
| `g68_10` | 증거 기록이 내장 hook 이고 외부 plugin 이 아닌가 | ✗ | ✓ |

`subprocess` 를 가짜로 만들지 않았다. 합성 사례는 실제 child 산출 파일을 고친 것이고 소비 경로는 실제와 같다.

### 1-2. 변이 등록부 (68차 1건)

| 이름 | 자리 | 되돌리는 것 | 기대 실패 (관측 = 선언) | 증인 |
|---|---|---|---|---|
| `the-premise-checks-the-call-phase-g68` | `test_gate66_defensive.py::_call_evidence` | call 기록 없는 node 를 `"unrun"` 대신 `"passed"` 로 | `g68_01` · `g68_03[setup_only]` · `g68_04` | `Failed: DID NOT RAISE AssertionError` |

```
python3 docs/22p_gap/mutation_replay.py --check-preimages      # 모든 변이 지점이 정확히 한 번 나타난다
python3 docs/22p_gap/mutation_replay.py -k premise            # g65 · g66 · g67 · g68 — 4 건 전부 기대 node 를 call 단계에서 물었다
python3 docs/22p_gap/mutation_replay.py -k the-premise-checks-the-call-phase-g68 --emit-expect   # 관측 = 선언
```

## §2 문서 정정 셋 (68차 D1 · D2 · D3) — 새 코드 결함과 구분

| # | 무엇 | 반영 |
|---|---|---|
| D1 | "`git diff --quiet a31be7a9 HEAD -- degradation-degeneracy` rc 0 · 한 바이트도 불변" — 블록을 쓰기 전 tree 의 실측이었고 고정 HEAD 에서는 요청문 머리 20 줄 때문에 rc 1 | `GATE68_REQUEST.md` 발송 전 재확인 표: 원문 취소선 + 정정 ("실행 코드 불변 · 요청문 머리 추가"). 이 요청문은 동일성 문장을 **커밋 뒤에** 적는다 |
| D2 | 발송문 "본실행 GO 요청" ↔ 정본 요청문 "GO 요청 안 함" 모순 | 발송문은 저장소 밖(스크래치패드)이라 고칠 원본이 없다 — 원장 §87·§88 과 작업 상태 문서에 기록. 이번 요청문·발송문은 머리에 "GO 를 요청하지 않는다" 를 둔다 |
| D3 | "지운 고아 175 건은 같은 회귀를 다시 돌리면 되돌릴 수 있다" — 재실행은 새 시각·ID·이력을 만들 뿐 바이트/역사 복원이 아니다 | `GATE68_REQUEST.md` §2-4: 원문 취소선 + 정정 ("같은 종류의 고아가 새로 생긴다") |

## §3 스스로 찾은 것 — 리뷰 패키지 보존의 줄끝 정규화

68차 패키지를 `docs/22p_gap/gate68_review/codex/` 에 풀어 커밋하자 git 이 CRLF→LF 정규화를 걸었다 (dd `.gitattributes` `* text=auto eol=lf`).
커밋된 141 개 중 **64 개가 MANIFEST sha256 과 어긋났다** (zip 바이트는 온전). 같은 방법으로 보니 **67차 350 중 174 · 66차 트리**도
같았다 — 이전 두 라운드의 "패키지 원본 보존" 은 zip 은 맞고 풀어 둔 트리는 줄끝이 바뀐 사본이었다. 고침: `docs/22p_gap/gate6{6,7,8}_review/** -text !eol`
규칙을 **먼저** 커밋하고 세 트리를 index 에서 빼고 원본 바이트로 다시 넣었다 (68차는 working tree, 66·67차는 커밋된 zip 에서 재추출).
커밋 뒤 `git show HEAD:` 재대조 **141/141 · 350/350 · 107/107**. 리뷰어 판정과 무관한 우리 쪽 보존 결함이라 여기 적는다.

검증:
```
python3 - <<'EOF'
import hashlib, json, subprocess
for d, man in (("gate68_review","MANIFEST.json"),("gate67_review","REVIEW_MANIFEST.json"),("gate66_review","MANIFEST.json")):
    base=f"degradation-degeneracy/docs/22p_gap/{d}/codex"
    m=json.loads(subprocess.check_output(["git","show",f"HEAD:{base}/{man}"]))
    lst=m["files"] if "files" in m else next(v for v in m.values() if isinstance(v,list))
    ok=sum(hashlib.sha256(subprocess.check_output(["git","show",f"HEAD:{base}/{e.get('path') or e.get('file')}"])).hexdigest()==e["sha256"] for e in lst)
    print(d, ok, "/", len(lst))
EOF
```

## §4 실행 출력 (전부 이 요청문 커밋 직전 실측 · clean tree · HEAD `b1710532`)

```
pytest gate66·67·68                           41 passed  (10.02 s)  EXIT=0
python3 -m pytest tests/ -q -p no:cacheprovider
        1 failed · 1803 passed · 2 xfailed  in 2504.15s (0:41:44)   EXIT=1
        FAILED tests/test_docs_lint.py::test_a_smoke_run_cannot_be_promoted_to_a_canonical_report
./scripts/smoke_e2e.sh
        ✅ pipeline smoke 통과                                                   EXIT=0
        시작 HEAD = 끝 HEAD = `b1710532`  (회귀·smoke 도중 HEAD 불변 — 문서는 그 뒤에 커밋했다)
등록부 (요청문 커밋 직전): tracked **367** · 디스크 **367** · git status 미추적 **0** · 삭제 **0**
```

⚠ **전체 pytest 의 1건은 기존 환경 실패이고 해결로 재표기하지 않는다** (67·68차 요청문과 같다): 이 컨테이너에
`results/grid_fit_v4` 가 없다 (`.gitignore` 의 `results/` — 본 실행 산출물이라 clone 에 없다). 그 시험은 "smoke namespace **밖**은
통과한다" 를 증명하려고 그 경로를 쓰고, 경로가 없으니 manifest 가 없어 `PreserveError [promote]` 가 난다. **코드가 아니라 자리의 문제**다.

⚠ **이번에는 회귀를 끊지 않았다** (68차 §2-4 의 대조). 전체 회귀 도중 `docs/22p_gap/_exec_class/` 에 미추적 175 건이 생겼고
(`git status` 로 관측), 세션이 정상 종료되자 `conftest` 의 세션 말 정리가 돌아 **끝난 뒤 미추적 0** 이었다. 등록부 delta **추가 0 ·
삭제 0** (tracked 367 = 디스크 367). 68차 때 남은 175 건이 "끊긴 세션의 고아" 였다는 설명과 같은 모양이고, 그때의 삭제가
복원이 아니라는 D3 정정은 그대로다. 회귀·smoke 도중 HEAD 는 움직이지 않았다 (시작·끝 `b1710532`, 시작·끝 dirty 0 — 실측).
문서(작업 상태 · 원장 §87/§88 · 정정 · 이 요청문)는 **그 뒤에** 커밋했다.

## §5 리뷰어에게 묻는 것

1. **G68-T1 종결 조건** — "exact full node ID 별 실제 call-phase report, 정상은 `when=call, outcome=passed`, setup/teardown 오류·skip·중복·누락 구분, rc/개수/옵션 문자열로 대체 금지" 를 위 소비자가 만족하는가. 남은 구멍이 있다면 **실제 child** 반례로.
2. **단계 증거의 신뢰 경계** — 증거 파일은 child 자신이 쓴다. child 를 적대자로 놓으면 그것도 위조 가능하다 (JUnit 과 같은 등급). 우리는 "child 가 정상 pytest 인데 옵션·환경으로 안 돈 경우" 만을 이 회귀의 범위로 둔다 — 그 범위 선언이 맞는가.
3. 문서 정정 셋의 반영 문장이 충분한가.

## §6 다음 라운드 앞에서 지킬 것 (이 라운드가 배운 것)

- **발송 블록·동일성 문장은 커밋 뒤에 잰다** (D1).
- **발송문은 요청문을 요약하지 않는다** — 요청문 §0 을 그대로 옮긴다 (D2).
- **"복원" 이라는 말은 바이트/역사가 돌아올 때만** (D3).
- **풀어 둔 리뷰 패키지는 `-text !eol` 규칙 뒤에 커밋한다** (§3).
