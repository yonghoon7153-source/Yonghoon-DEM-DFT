# 68차 게이트 리뷰 요청 — 67차 3건(G67-N1 · N2 · T1/T1-b) 대응

읽는 쪽은 LLM 리뷰어다. 밀도 우선, 완충 문장 없음. **요청문은 증거가 아니다** — 아래 명령을
재실행해 검증하는 것을 전제로 쓴다. 우리 환경에서만 되는 것은 그렇게 밝힌다.

## 판정 대상 (이 블록이 정본이다)

| 항목 | 값 |
|---|---|
| 브랜치 | 루트 `CLAUDE.md` 하드룰 1 의 작업 브랜치 (요청문에 이름을 옮겨 적지 않는다 — lint `no-hardcoded-branch-name`) |
| **판정 대상 코드** | **`743f65bead671bf353ce38027c2e8e457738ec08`** (RUN_SCOPE 를 마지막으로 건드린 커밋 — 64·65·66·67차와 같다) |
| `source_digest` | **`e9ee7475dea7de1d`** — 67차 리뷰어가 직접 실행한 값과 같다 |
| 검토할 HEAD | 브랜치 head (fetch 지시 아래) |
| 직전 판정 | 67차 **부분 수용 / 종결 NO-GO** — P1 2 (G67-N1 · N2) · P2 1 (G67-T1, T1-b 보완 조건 포함) |
| 접수·대응 원장 | `docs/GATE67_WORKING_STATE.md` · 리뷰 패키지 원본 `docs/22p_gap/gate67_review/` (zip sha256 `3ab027349935843f8a2404a87b988b3e7264fa0a9d3266f2e3f20a757bd10220`) |

> ```
> git fetch origin <하드룰 1 의 브랜치> && git checkout FETCH_HEAD
> cd degradation-degeneracy
> python3 -c "import sys; sys.path.insert(0,'.'); from src.io import source_digest; print(source_digest())"
> # → e9ee7475dea7de1d
> git log --oneline 743f65b..HEAD -- src tools configs scripts run.sh requirements*.txt
> # → 빈 출력
> ```

판정에 봐야 할 파일은 전부 RUN_SCOPE 밖이다: `docs/22p_gap/mutation_replay.py` ·
`tests/test_gate67_defensive.py`(신규) · `tests/test_gate66_defensive.py`.

**리뷰어가 고정한 대상과 우리 트리의 동일성**: 67차 리뷰어는 `cdc49e91` 을 고정했고,
`git diff cdc49e91..HEAD -- degradation-degeneracy` 는 이번 대응 **직전에 비어 있었다**(실측).
그 사이 커밋 둘은 `wiki/`·큐 문서뿐이다.

### 발송 전 재확인 (2026-09-23 — 이 요청문은 2026-09-22 `a31be7a9` 에서 쓰고 보류했다)

보류하는 동안 브랜치에 커밋이 쌓였다(`bms-balancing/` MSC 작업 · `wiki/` · 문헌 원장). **degradation-degeneracy 는
움직이지 않았다.** 아래는 발송 직전에 다시 잰 것이다.

| 검사 | 명령 | 실측 |
|---|---|---|
| 요청문 커밋 이후 dd 변경 | `git diff --quiet a31be7a9 HEAD -- degradation-degeneracy` | **rc 0 (차이 없음)** |
| dd·bms·wiki 밖 변경 | `git diff --stat a31be7a9..HEAD -- . ':!bms-balancing' ':!wiki'` | **빈 출력** |
| RUN_SCOPE 마지막 커밋 | `git log -1 --format=%H -- src tools configs scripts run.sh requirements*.txt` | `743f65bead671bf353ce38027c2e8e457738ec08` (위 표와 같음) |
| `source_digest` | 위 fetch 블록의 명령 | **`e9ee7475dea7de1d`** (위 표와 같음) |
| 게이트 회귀 묶음 | `pytest tests/test_gate6{7,6,5,4,3}_defensive.py -q -p no:cacheprovider` | **77 passed · 1 xfailed** (23.06 s) EXIT=0 |

- §2-3 의 "76 passed · 1 skipped" 에서 skip 1 은 `test_gate63_defensive.py:426` 이었다(dirty worktree 면 건너뛴다).
  이번에는 **clean worktree 에서 돌아 통과했다** → 77 passed. 새로 고친 것이 아니라 실행 조건이 달라진 것이다.
- **전체 pytest(41 분)와 strict smoke 는 다시 돌리지 않았다.** 대상 바이트가 같아서 §2-3 의 수치(`e834b01e` 에서 잰 것)를 그대로 쓴다.
  리뷰어가 HEAD 에서 전체를 돌리면 그 수치와 비교할 수 있다.
- 재실행 뒤 `git status --short` 는 빈 출력이다(미추적 0).
- **검토할 HEAD** 는 이 블록을 담은 커밋이다. 발송 메시지에 SHA 를 적는다.

---

## §0 이번 라운드가 **하지 않은** 것

| 조건 | 상태 |
|---|---|
| **P0-1** producer 결속 · trusted launcher · **P0-4** typed 보존 영수증 소비 · 독립 replay · immutable bundle | **미착수** (65·66·67차와 같다. 67차 리뷰어도 새 발견으로 세지 않았다) |
| **⑩ 등록부 격리** | **미착수**. 67차 Q5 의 답을 받아 순서를 **읽기 전용 영향 확인 → 그 다음 복원/삭제/class 변경/격리 migration 의 별도 승인** 으로 적었다. 이번에도 복원·class 변경 없음 |
| **Q6 F50b** | 여전히 **(b)**: 다음 RUN_SCOPE 변경에 묶고 그때까지 "같은 commit 에서 resume" 을 운영 제약으로 둔다 |
| Linux native 검증 | 우리 쪽 출력을 §2-3 에 싣는다. 67차 리뷰어 환경(Windows)에서는 `fcntl`·`/proc` 제약으로 미실행이었고 그것을 통과로 세지 않은 것을 그대로 받는다 |

**본 실행 GO 를 요청하지 않는다.**

---

## §1 발견별 대응표

| ID | 리뷰어가 잰 것 | 우리 원인 | 고침 | 지금 관측 |
|---|---|---|---|---|
| **G67-N1** (P1) | OFF + 명시 import namespace 에서 `startup.customization.usercustomize` **한 칸**을 `<absent>` 로 바꾼 영수증이 completeness·parent 비교·실제 `_execution_receipt()` **전부 ACCEPTED**. ON 대조는 REJECTED | 부재 위조의 마지막 방어가 `elif auto and cand != "<absent>":` 였다. OFF 면 `auto=False`, 표준 namespace 는 origin 이 없어 startup 이력의 **파일 목록**에도 안 잡힌다 → 두 방어를 다 빠져나갔다 | **판정의 기준을 `cand`(부모가 잰 것) 하나로** 했다. `if g != cand:` 를 앞세워 세 종류를 한 줄로 대조하고, 이력 교차 확인은 그 뒤에 남긴다. `auto` 는 **사유 문장에만** 쓴다 | forged **REJECTED** (OFF·ON 둘 다) · 정직한 namespace 영수증 ACCEPTED · 정말로 미로드인 `<absent>` ACCEPTED |
| **G67-N2** (P1) | 표준 ZIP **package** 가 자기 archive 를 `sys.path` 에서 빼면 native 로드·completeness 는 성공인데 parent/entry 가 unsupported-loader `_ReplayError` | `dirname(origin)` 이 archive root 가 아니라 `archive.zip/sitecustomize` 이고, root 는 이미 final path 에서 빠졌다. **66차에 일반 파일 분기에서 걷어낸 사후 재탐색이 ZIP 분기에 남아 있었다** | `_archive_member_digest()` 신설 — origin 경로를 조상 쪽으로 걸어 **실재하는 archive 파일**을 찾고 남은 부분을 member 로 써서 `zipfile` 로 바이트를 읽는다. 사후 검색 경로도, 임의 loader 실행도 없다 | `zip_package_remove_path` entry **ACCEPTED** · 경로 유지 package·단일 module 대조군 ACCEPTED 유지 · 바이트 변경·member 소멸·표준 archive 아님은 **거부** |
| **G67-T1** (P2) | 상속 `PYTEST_ADDOPTS` 로 child pytest 가 rc 4(사용법 오류) 또는 수집만(call 0건)인데 커밋된 전제 회귀가 **정상 반환** | 실제 assertion 이 `"failed" not in stdout` 하나. 그리고 child env 를 `dict(os.environ)` 으로 그대로 물려줬다 | 둘을 갈랐다 — ① **입력 경계**: pytest env 손잡이 넷(`PYTEST_ADDOPTS`·`PYTEST_PLUGINS`·`PYTEST_DISABLE_PLUGIN_AUTOLOAD`·`PYTEST_CURRENT_TEST`)을 걷는다 ② **실행 증거**: `--junitxml`(내장)로 **정확히 그 두 node** 가 `passed`/`skipped` 인지 본다. `skipped` 는 **미측정**으로 따로 찍는다 | 바깥 env 통로: child rc **4 → 0** (옵션이 child 에 닿지 않는다) · 허용 통로(`env_extra`): 커밋된 시험이 **진짜 `AssertionError`** 로 거부 |
| **G67-T1-b** (P2) | 등록 witness 에 `stdout[-600:]` 에서 잘린 `도 기대와 다르면 그때는` 이 있어 그 기계에서 `call_witness_matches=false` | 증인을 관측값 그대로 붙여 넣었다 | 사유 문장까지만 남겼고, **재발 방지 정적 회귀**(`test_g67_14`)를 두었다: 닫히지 않은 따옴표 **뒤에 글자가 남으면** 실패 | `-k g66` 3/3 물었다 · witness 일치 · `test_g67_14` 통과 |

### §1-1 리뷰어가 닫혔다고 인정한 축 — 되돌리지 않았다

기존 재현기 `repro_startup_gate66.py --full-sandbox` 5조건(`plain` · `cwd_only_candidate` ·
`cwd_on_pythonpath` · `remove_loaded_path` · `reorder_loaded_path`)을 다시 돌려 **전부
comparison·entry ACCEPTED** 를 확인했다. `PYTHONNOUSERSITE=1` 직접 전제 시험도 2 passed.

---

## §2 실행 출력 (전부 이 커밋 직전 실측)

### 2-1. 리뷰어 재현기 — **한 줄도 고치지 않고** 수정 전/후

```
repro_boundaries.py --repo <dd> --out <새경로>
                                        수정 전            수정 후
  namespace_explicit_off   forged entry  ACCEPTED     →    REJECTED      ← N1 닫힘
  namespace_explicit_on    forged        REJECTED     →    REJECTED      (대조군 유지)
  zip_package_remove_path  entry         REJECTED     →    ACCEPTED      ← N2 닫힘
  zip_package_plain        entry         ACCEPTED     →    ACCEPTED      (대조군 유지)
  zip_module_remove_path   entry         ACCEPTED     →    ACCEPTED      (대조군 유지)
  premise_pytest_usage_error   committed ACCEPTED     →    REJECTED      ← T1 닫힘
      사유 AssertionError('child pytest 가 결과 파일을 남기지 않았다 … (G67-T1)', …)
  premise_collection_only      committed ACCEPTED     →    REJECTED      ← T1 닫힘
      사유 AssertionError('기대한 두 전제 node 가 실제로 돌지 않았다 … (G67-T1)', [], […])

repro_premise_no_execution.py --repo <dd> --out <새경로>
  네 case 모두  child_rc 4 또는 call 0건  →  **child_rc 0**
  `committed_test_returned_normally` 는 전후 모두 true 인데 **뜻이 바뀌었다**:
  전에는 "안 돌았는데 안 봤다", 지금은 "바깥 옵션이 child 에 닿지 못해 실제로 돌았다".
  두 스크립트가 서로 보완적으로 닫힘을 보인다 — 한쪽은 **경계**, 한쪽은 **증거 요구**다.

repro_startup_gate66.py --full-sandbox (5 case)   전부 comparison·entry ACCEPTED
```

⚠ **한 번은 거부가 증거가 아니었다.** 첫 재실행에서 `repro_boundaries.py` 의 T1 칸이 REJECTED 로
나왔지만 사유가 `TypeError: … missing 1 required positional argument: 'tmp_path'` 였다 —
내가 시험 함수에 fixture 를 더해 **리뷰어의 호출 서명을 깼기** 때문이고, 그 거부는 우리 수정의
증거가 아니다. 서명을 되돌린(함수 안에서 `tempfile.TemporaryDirectory()` 로 정리) 뒤 다시
돌려 `AssertionError` 인 것을 확인하고서야 닫혔다고 적었다. `tmp_path` 에 **기본값을 주는**
우회도 재 보고 버렸다 — pytest 가 기본값 있는 인자에 fixture 를 넣지 않아(`--setup-show` 실측)
임시 디렉터리가 새어 나간다.

### 2-2. 변이 등록부

`auto` 가 판정에서 빠지면서 preimage 둘이 또 죽어 **자리를 옮겼다** (`-k` 를 넓히지 않았다):

| 축 | 옛 자리 | 새 자리 |
|---|---|---|
| `usercustomize-follows-the-startup-activation-g64` | `elif auto and cand != "<absent>":` | `if g != cand:` — 위조 대조군 **셋**(g66_05b · g67_01 · g67_04)이 한꺼번에 빨개진다 |
| `explicit-import-is-an-ordinary-import-g65` | `elif not loaded_file:` | `if not loaded_file:` (동일성 검사가 앞에서 `continue` 하므로 `elif` → `if`) |

새 축 2 (`-g67`):

```
zip-bytes-come-from-the-archive-member-g67     MR     G67-N2  (사후 재탐색으로 되돌림)
the-premise-checks-the-child-actually-ran-g67  G66T   G67-T1  (전 판 증거 한 줄로 되돌림)

--check-preimages   모든 변이 지점이 정확히 한 번 나타난다 (rc 0)
-k g63   8/8 물었다 · rc 0      -k g64   3/3 물었다 · rc 0
-k g65   5/5 물었다 · rc 0      -k g66   3/3 물었다 · rc 0
-k g67   2/2 물었다 · rc 0
```

⚠ g67 T1 축의 preimage 를 **두 번** 고쳤다. 처음엔 주석 한 줄을 겨냥했는데 그 주석이 같은
줄에서 이어져 치환이 문장을 잘라 **변이가 수집을 깼다**(runner 진단 `변이가 수집을 깼다`).
완전한 줄로 옮기고 **변이본이 컴파일되는 것을 따로 확인**한 다음 다시 돌렸다. 67차 리뷰어의
"setup 오류를 mutant kill 로 세지 않는다" 와 같은 규율이다.

### 2-3. 회귀

```
pytest gate67·66·65·64·63                 76 passed · 1 skipped · 1 xfailed  (15.41s)  EXIT=0
  skip = tests/test_gate63_defensive.py:426 "dirty worktree — 진짜 grid 의 곡선을 fit 이
         거부한다 (F74/F85). clean 커밋에서 돈다 (smoke 와 같은 규칙)"
pytest tests/test_gate67_defensive.py     17 passed
  첫 실행 7 failed · 11 passed (RED). 초판 8 failed 중 둘은 **내 시험 버그**였다 —
  `EXPECT` 를 `MUTANTS` 로 썼고 `site_file=None` 이 다른 예외를 냈다. 고친 뒤 7 이 진짜 RED.
전체 pytest tests/ -q
        1 failed · 1789 passed · 1 skipped · 2 xfailed  in 2472.82s (0:41:12)   EXIT=1
  FAILED tests/test_docs_lint.py::test_a_smoke_run_cannot_be_promoted_to_a_canonical_report
./scripts/smoke_e2e.sh
        ✅ pipeline smoke 통과                                                   EXIT=0
        시작 HEAD = 끝 HEAD = e834b01e4066c5e78c06b6ed1f77878e5a27a481
```

⚠ **전체 pytest 의 1건은 기존 환경 실패이고 해결로 재표기하지 않는다** (67차 요청문과 같다):
이 컨테이너에 `results/grid_fit_v4` 가 없다 (`.gitignore:2 results/` — 본 실행 산출물이라
clone 에 없다). 그 시험은 "smoke namespace **밖**은 통과한다" 를 증명하려고 그 경로를 쓰고,
경로가 없으니 manifest 가 없어 `PreserveError [promote]` 가 난다. **코드가 아니라 자리의
문제**다. 실측 문구: `… /results/grid_fit_v4 에 manifest 가 없어 내용 identity 를 만들 수 없다`.

⚠ **전체 회귀·smoke 가 도는 동안 HEAD 는 움직이지 않았다** (시작·끝 모두 `e834b01e`, 실측).
64차 교훈("회귀 도중 HEAD 이동")을 다시 밟지 않으려고 조용한 창에서 돌렸다. 도중에 Q1 문장
좁히기(주석·문서)를 넣어야 해서 **먼저 돌던 전체 회귀는 4% 에서 끊고 최종 트리에서 한 번만**
돌렸다 — 끊은 회귀의 숫자는 쓰지 않는다.

### 2-4. 등록부 delta — **추가 0 · 삭제 0** (그리고 지운 고아 175건의 사실)

커밋 직전 실측: tracked **367** · 디스크 **367** · `git status` 미추적 **0** · **삭제 0**.
67차 리뷰어가 직접 확인한 366→367 에서 **더 움직이지 않았다.**

⚠ 그 사이에 실제로 있었던 일을 그대로 적는다. 전체 회귀를 한 번 시작했다가 **4% 에서 끊었고**
(Q1 문장 좁히기를 넣어야 해서), 끊은 탓에 `conftest` 의 세션 말 정리(`tests/conftest.py:180–188`,
*세션 시작 때 없던 파일만* 지운다)가 **돌지 못했다.** 그 결과 미추적 `_exec_class` **175건**이
남았다 — `recorded_at` 13:43:57Z–13:46:31Z, 전부 `sealed: true` · `canonical`, 분포
`leg=L phase=grid class=canonical` **88** + `시험 fixture _complete_artifact …` **87**
(G66-R1 에서 리뷰어가 집계한 그 분포와 같은 모양이다). 최종 체인은 13:49:32Z 에 시작했으므로
이 175건은 **최종 트리의 산물이 아니다.**

그래서 **끊긴 세션의 정리를 대신 수행했다** — 그 175건을 지웠다. 이것은 G66-R1 이 지적한 삭제와
**다른 종류**임을 분명히 해 둔다: R1 은 *이미 커밋된 sealed 기록*을 라운드 간에 지운 것이고,
이번 것은 *한 번도 명부에 들어간 적 없는, 중단된 실행의 고아*다. 커밋된 기록은 **하나도 건드리지
않았다** (tracked 367 그대로, `git status` 에 `D` 없음 — 위 실측). 판단이 틀렸다면 되돌릴 수
있다: 같은 회귀를 한 번 더 돌리면 같은 종류가 다시 생긴다 (그것이 ⑩ 이 열려 있다는 뜻이다).

---

## §3 리뷰어 질문 다섯에 대한 우리 쪽 조치

1. **Q1 — helper 신뢰 경계.** 지적을 받아 **문서 문장을 좁혔다**: 탐침이 주는 것은
   *"startup 후 관측한 module origin"* 이고 **로드 순간의 불변 기록이 아니다**
   (`__file__`/`__spec__.origin` 은 런타임에 바뀔 수 있다). 그 이상의 주장은 trusted
   launcher/immutable input bundle 이 필요하고 그것은 §0 의 미착수 항목이다. **그 경계 안에서도
   모순인 N1 을 먼저 거부하라** 는 지시를 그대로 이행했다.
2. **Q2 — ZIP.** "origin 일치만으로는 부족" 을 받았다. 이제 archive·member **identity 로 읽고**
   사후 `sys.path` 의존을 없앴다. 원래 바이트 비교는 유지했다.
3. **Q3 — `auto`.** "부재 위조를 거부하는 근거로 쓰면 안 된다" 를 그대로 이행했다. `auto` 는
   판정에서 빠지고 사유 문장에만 남는다. namespace 의 **이름별 이력**을 더하는 방향은 하지
   않았다 — 지금은 measured `loaded`/kind/locations 와의 동일성이 그 몫을 한다.
4. **Q4 — env.** env 이름을 지우는 것만으로 닫히지 않는다는 지적을 받아 **두 축을 따로** 두었다:
   입력 경계(pytest 손잡이 넷)와 실행 증거(정확한 두 node 의 call 결과). 통제 불가 정책 skip 은
   **미측정**으로 PASS 와 구분해 찍는다.
5. **Q5 — R1.** 순서를 받아들였다: **읽기 전용 영향 확인을 먼저**, 복원/삭제/class 변경/격리
   migration 은 **별도 승인**. 이번 라운드에 등록부 복원·class 변경은 하지 않았다.

## §4 질문

1. **N2 의 읽기 경로.** 부모가 origin 경로를 조상 쪽으로 걸어 archive 를 찾고 `zipfile` 로
   member 를 읽는다 — loader 를 실행하지 않는다는 점은 의도한 강화인데, 그러면 **표준 ZIP 외의
   지원 loader**(예: 다른 archive 형식)는 원리적으로 거부된다. 지금은 그것이 맞는 경계라고 보고
   거부 문구에 적었다. 더 넓혀야 하는 형식이 있는가?
2. **N1 의 남은 비대칭.** 이제 `<absent>`·hex16·namespace 셋을 같은 한 줄로 대조한다. 이력
   교차 확인(`loaded_file`)은 그 뒤에 남아 있는데, 표준 namespace 는 이력에 파일로 안 잡히므로
   그 축에서는 여전히 **한 방향**(파일로 잡혔다고 하면 거부)만 본다. 이름별 이력을 만들지 않고
   닫을 수 있는 축이 더 있는가?
3. **T1 의 skip 처리.** 정책상 skip 을 **미측정**으로 찍고 PASS 로 세지 않되 실패로도 세지
   않는다. 이 기계에서는 둘 다 실제로 돌아 skip 이 0 이다. "전부 skip" 이 되는 환경에서 그것을
   **실패로 승격**해야 하는가, 아니면 미측정 보고로 충분한가?
4. **T1-b 의 규칙 폭.** witness 검사를 "닫히지 않은 따옴표 뒤에 글자가 남으면 실패" 로 좁혔다.
   더 넓은 규칙("닫힌 조각은 시험 소스에 있어야 한다")은 `'NoneType'`·`'ok:canonical'` 같은
   **결정적** repr 19건이 걸려 버렸다. 이 좁힘이 맞는가, 아니면 결정적 repr 을 따로 선언하게
   하고 넓은 규칙을 쓰는 편이 맞는가?
5. **Q1 의 다음 단계.** "로드 순간의 불변 기록" 을 실제로 만들려면 trusted launcher 쪽 설계가
   필요하다고 적었다. 그것을 ⑩ 격리·P0-1 과 **묶어서** 한 라운드로 여는 것이 맞는가, 아니면
   읽기 전용 영향 확인(Q5)처럼 **먼저 관측만** 하는 단계를 따로 두는 편이 맞는가?

## §5 다음 실행 계획

**GO 를 요청하지 않는다.** §0 의 미착수가 그대로 열려 있다. 다음 라운드 후보 순서:
⑩ 등록부 **읽기 전용 영향 확인**(승인 불필요한 범위) → 그 결과를 근거로 격리 계약 승인 요청 →
Q6 F50b 를 묶을 RUN_SCOPE 변경 → Q4 `error_code` 매트릭스.
