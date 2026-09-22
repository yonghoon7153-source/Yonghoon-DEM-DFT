# 66차 게이트 리뷰 요청 — 65차 4건(G65-N1a · N1b · N2b · T1) + E2-R 후속 대응

읽는 쪽은 LLM 리뷰어다. 밀도 우선, 완충 문장 없음. **요청문은 증거가 아니다** — 아래
명령을 재실행해 검증하는 것을 전제로 쓴다. 우리 환경에서만 되는 것은 그렇게 밝힌다.

## 판정 대상 (이 블록이 정본이다)

| 항목 | 값 |
|---|---|
| 브랜치 | 루트 `CLAUDE.md` 하드룰 1 의 작업 브랜치 (요청문에 이름을 옮겨 적지 않는다 — lint `no-hardcoded-branch-name`) |
| **판정 대상 코드** | **`743f65bead671bf353ce38027c2e8e457738ec08`** (RUN_SCOPE 를 마지막으로 건드린 커밋 — **64·65차와 같다**) |
| `source_digest` | **`e9ee7475dea7de1d`** — 65차 리뷰어 실측값과 같다 |
| 검토할 HEAD | 브랜치 head (fetch 지시 아래). 이 묶음의 커밋은 `docs/22p_gap/mutation_replay.py` · `tests/` · `docs/` 만 만진다 |
| 직전 판정 | 65차 **NO-GO (부분 수용)** — "64차 접수 셋 전부 종결" 불수용. 새 P1 3 (G65-N1a · N1b · N2b) · P2 1 (G65-T1) · E2-R 보류 1 |
| 이번 라운드 | 접수 4건 + 보류 1건 **전부 코드/시험에서 닫음**. 리뷰어 재현기 셋을 Linux 에서 먼저 실행 |
| 접수·대응 원장 | `docs/08_REVIEW_RESPONSE.md` §81(접수) · §82(대응) · 작업 상태 `docs/GATE65_WORKING_STATE.md` · 리뷰 패키지 원본 `docs/22p_gap/gate65_review/` |

> ```
> git fetch origin <하드룰 1 의 브랜치> && git checkout FETCH_HEAD
> cd degradation-degeneracy
> python3 -c "import sys; sys.path.insert(0,'.'); from src.io import source_digest; print(source_digest())"
> # → e9ee7475dea7de1d 이어야 한다. 아니면 그 자체가 발견이다.
> git log --oneline 743f65b..HEAD -- src tools configs scripts run.sh requirements*.txt
> # → 출력이 비어야 한다.
> ```

**과학 코드 identity 는 이번에도 안 움직였다.** 판정에 봐야 할 파일은 전부 RUN_SCOPE 밖이다:
`docs/22p_gap/mutation_replay.py` · `tests/test_gate65_defensive.py`(신규) ·
`tests/interpreter_fixture.py`(신규) · `tests/test_gate64_defensive.py` ·
`tests/test_gate63_defensive.py` · `tests/receipt_fixture.py`.

---

## §0 먼저 — 이번 라운드가 **하지 않은** 것

65차 리뷰어: "본 실행 GO 는 별도이며 이번에 승인한 것은 아니다." 그대로 받는다. **본 실행 GO 를
요청하지 않는다.**

| 조건 | 상태 |
|---|---|
| **P0-1** producer 결속 · trusted launcher · **P0-4** typed 보존 영수증 소비 · 독립 replay · immutable bundle | **미착수** (65차 요청문 §0 과 같다) |
| **⑩ 등록부 격리** (tracked root JSON 541 = 261 synthetic · 264 real canonical · 16 re-key) | **미착수** — 별도 계약. 리뷰어 권고 "둘 다"(임시 등록부 주입 + 운영 등록부 불변 확인 · synthetic 을 canonical 권한으로 유입시키지 않기 · reader 가 읽는지/authority 를 주는지 같이 고정 · 기존 기록은 append-only supersession) 을 §81 에 적었다. 기존 class/삭제 계약 변경은 **별도 승인 대상**이라 손대지 않았다 |
| **Q4 권고** (고정 `error_code`·검사 단계 구조화, 문맥 매트릭스) | **미착수**. 이번 증인 문구는 전부 시험의 고정 문구 (production reason · digest · 경로 없음) |
| 보조 인터프리터의 신뢰 경계 | **64차와 같다** — `_replay_context` 가 띄우는 인터프리터도 같은 startup 코드를 실행한다. 부모가 독립적으로 믿는 것은 그 경로 위의 **바이트를 부모가 직접 읽은 값**이다 (docstring 에 명시). 이것을 신고로 유지한다 |

---

## 1. 발견별 대응

| ID | 리뷰어 반례 | 고침 (`파일:함수`) | 이제 어디에 걸리나 | 회귀 |
|---|---|---|---|---|
| **G65-N1a** (P1) | 비활성 인터프리터 + `sitecustomize.py: import usercustomize` → child `1cfeb13a…` · parent `<absent>` → REJECTED | `mutation_replay.py:_parent_customization_view(ctx)` 는 **후보**만 (조건으로 `<absent>` 를 미리 넣지 않는다) · `_assert_customization_matches_parent(receipt, ctx)` 가 **조건 · 후보 · 이력** 셋으로 판정 | child hex16 = 후보 **and** `startup_history.modules` 에 있음 → 수용. 후보 ≠ → `child=… parent=…` 로 거부. 이력에 없음 → `child 가 바이트를 냈는데 startup 이력에 없다` 로 거부. child `<absent>` 인데 이력에 있음 → `child=<absent> 인데 startup 이력은 올렸다고 한다` 로 거부 | `test_gate65_defensive.py::test_a_disabled_interpreter_with_an_explicit_import_is_accepted` · `…_with_changed_bytes_is_rejected` · `…_that_did_not_load_usercustomize_stays_absent` · `…_claiming_absent_while_history_loaded_it_is_rejected` |
| **G65-N1b** (P1) | `PYTHONPATH=startup`(상대) + 호출 cwd ≠ 재생 cwd → child `<absent>`/`0638e450…` · parent `2e252a13…`/`0c47a41c…` → REJECTED. 실제 sandbox 재사용 판도 REJECTED | `mutation_replay.py:_replay_context(cwd)` 신설 — 같은 실행 파일 · `-c` · `replay_env()` · **cwd=`_sandboxed(ROOT)`** 로 인터프리터를 띄워 `ENABLE_USER_SITE`·`sys.path`·`getcwd`·`site.__file__` 을 받고 `sys.path` 를 child cwd 기준 절대 경로로 정규화. `_parent_customization_view` 의 `dirs = list(ctx["search_path"])` — 부모 `sys.path` 사용 제거. `_parent_user_site_enabled()` 는 `ctx["user_site"]` 의 wrapper | 부모가 child 와 **같은 검색 경로**에서 resolver 를 돌린다 → 후보 = child 가 올린 것 → 수용 | `…::test_a_relative_pythonpath_is_resolved_in_the_replay_cwd` · `…::test_the_real_entry_point_accepts_a_relative_pythonpath_from_another_cwd` (실제 `_execution_receipt()`) · `…::test_the_parents_sys_path_is_not_the_childs_search_path` |
| **G65-N2b** (P1) | 빈 `sitecustomize/` (namespace) → child `<absent>` → 이력 검사 "올렸다는데 `<absent>`" → `failed` → 완전성 거부 | `mutation_replay.py:_ENV_PROBE_BODY` cust 를 **상태 넷**으로: `<absent>` · hex16(`_hash_origin`) · `<namespace>:hex16`(`__file__ None` ∧ `submodule_search_locations`) · `_Unreadable`→`failed`(origin 도 검색 위치도 없음). identity = 종류 + 검색 위치(절대 경로 정규화, sha256[:16]) — child·부모가 **같은 문자열** `_NAMESPACE_IDENTITY_SRC` 실행. schema `_NAMESPACE_ID` · `_UNSUPPORTED_ORIGIN` 추가 | namespace 는 더 이상 `<absent>` 가 아니다 → 이력 검사 통과 → 완전성 통과 → 부모 후보(`PathFinder` namespace spec)와 일치 → 수용. 다른 위치 → 다른 값. `sys.modules` 에 심은 빈 ModuleType → `failed` | `…::test_a_namespace_usercustomize_is_measured_and_accepted` · `…::test_a_namespace_identity_is_bound_to_its_search_locations` · `…::test_a_loaded_customization_without_any_origin_is_failed_not_absent` · `…::test_a_zip_customization_and_an_unreadable_one_keep_their_own_reasons` |
| **G65-T1** (P2) | `test_an_enabled_user_site_still_compares_the_bytes` 가 일반 venv 에서 `assert child != '<absent>'` 로 죽음 (1 failed) | `tests/interpreter_fixture.py` 신설 — `build_interpreter` (`python -m venv --without-pip [--system-site-packages]`) → `make_interpreter` 가 **실측** `site.ENABLE_USER_SITE` 후 기대와 다르면 `pytest.skip` (기대값·실측값 명시). `test_gate64_defensive.py` 의 활성 대조군을 이 fixture 위로 (활성 확인 assertion 유지), 비활성 판은 venv 판 + env 변수 판 둘 다 | 전제를 못 만들면 **skip 이유에 실측값** — 실패도 통과도 아니다 | `…::test_the_interpreter_fixture_measures_its_own_premise[True/False]` · `…::test_an_enabled_interpreter_compares_usercustomize_bytes` · `test_gate64_defensive.py::test_an_enabled_user_site_still_compares_the_bytes` |
| **E2-R 후속** (보류) | 실제 lifecycle 이 쓰는 `_kernel_lock_held(tok)` 은 True 쪽만. `repro_e2_linux_NOT_RUN.py`: 상수 True 로 바꿔도 커밋된 대조군 둘 PASS (**이 Linux 실측**) | `tests/test_gate63_defensive.py:_flock_reports_held(fd)` 하나를 token 판·경로 판이 공유. 커밋된 대조군에 **같은 token · 같은 inode** 에서 `LOCK_UN`→`is False`→재획득→`is True`. g64 AST 대조군은 **탐침별로** True·False 를 센다 | token 탐침을 상수 True 로 바꾸면 `test_the_kernel_lock_probe_itself_is_not_vacuous` 가 빨개진다 (`pytest.raises(AssertionError)` 로 고정) | `…::test_the_token_probe_goes_false_on_the_same_live_token` · `…::test_a_constant_true_token_probe_is_caught_by_the_committed_control` · `…::test_the_committed_control_asserts_the_token_probe_negative` |

fixture 가 먼저 깨진 것 (규율 2): `tests/receipt_fixture.py` — 완전한 영수증의 이력은 customization
과 양립해야 한다(바이트를 낸 이름은 `startup_history.modules` 에). `test_gate64_defensive.py::
test_a_child_with_user_site_disabled_matches_the_parent` 의 `want["usercustomize"] == "<absent>"`
는 틀린 등식을 적은 assertion 이었다 → 판정 함수로.

## 2. 실측

### 2-1. 리뷰어 재현기 (Linux, CPython 3.11.15, `/usr/local/bin/python3`)

```
repro_imports.py  (수정 전 HEAD 5e4cf103)
  plain_control              ACCEPTED
  zip_control                ACCEPTED
  disabled_but_explicit_import   REJECTED  usercustomize: child='42bd17d9d1bd1516' parent='<absent>'   ← N1a
  normal_namespace_package   ACCEPTED   (⚠ 아래)
  relative_pythonpath        REJECTED  sitecustomize: child='0638e4509624a19b' parent='0c47a41c3ddec65b'   ← N1b
  enabled_control            ACCEPTED
repro_namespace.py           startup measured · history measured · completeness ACCEPTED   (⚠ 아래)
repro_e2_linux_NOT_RUN.py    same_token_baseline [true, false]
                             baseline  : 두 대조군 PASS
                             mutated   : 두 대조군 PASS   ← 리뷰어 보류 사항 확정 (상수 True token 탐침을 못 잡는다)
```

⚠ namespace 두 건이 이 기계에서 ACCEPTED 인 이유: Debian 의 `/usr/lib/python3.11/sitecustomize.py`
(0 바이트, 실측 `wc -c`) 가 이 인터프리터의 검색 경로에 있어 namespace `sitecustomize/` 를
가린다 (Python 은 정규 module 을 먼저 찾는다). 그래서 N2b 회귀는 자유로운 이름 `usercustomize`
+ 활성 인터프리터로 만들었다 — `usercustomize/` 빈 디렉터리가 실제로 namespace 로 올라오는 것을
확인했다 (`__file__ None`, `submodule_search_locations` 2 항목). 리뷰어 환경(Windows, 시스템
sitecustomize 없음)에서는 원래 이름으로 재현된다.

### 2-2. RED → GREEN

```
tests/test_gate65_defensive.py  수정 전 첫 실행:  10 failed · 7 passed   (통과 7 = 대조군)
  실패 이유: N1a 2 · N1b 3 (그중 1 은 _replay_context AttributeError — 새 API) · N2b 3 · E2-R 2
  (E2-R 하나는 tmp_path/"a" 미생성으로 이유가 틀린 빨강 → 시험만 고쳐 다시 빨갛게 한 뒤 production 수정)
수정 뒤 (gate65·64·63 · evidence_receipt_62 · evidence_layer_59·58):
  96 passed · 3 failed · 1 skipped · 1 xfailed  — 3 failed 는 전부 test_evidence_layer_58 의
  check_coverage 가 g64 변이 preimage 0회 (코드 이동) 를 막은 것 → 등록부 갱신 뒤:
최종 (같은 6 파일):        99 passed · 1 skipped · 1 xfailed  in 850.70s   EXIT=0
  skip = test_gate63_defensive.py:426 "dirty worktree" (smoke 와 같은 규칙, clean 커밋에서 돈다)
tests/test_docs_lint.py:  355 passed · 1 failed  in 1198.11s   EXIT=1
  1 failed = test_a_smoke_run_cannot_be_promoted_to_a_canonical_report
    tools/preserve.py:4647 PreserveError "[promote] results/grid_fit_v4 에 manifest 가 없어
    내용 identity 를 만들 수 없다" — `results/grid_fit_v4` 가 **이 기계에 없다**
    (`ls` → No such file; `git ls-files` → 빈 출력, 미추적 실행 산출물).
    65차 요청문 §2 에 이미 같은 환경 실패로 적혀 있었고, 이번 diff 에 RUN_SCOPE 파일은 0건이다.
```

### 2-3. 변이 등록부

```
--check-preimages   모든 변이 지점이 정확히 한 번 나타난다   rc 0
-k g64              3/3 물었다 (call 단계) · EXPECT 일치      rc 0
-k g65              5/5 물었다 (call 단계) · EXPECT 일치      rc 0
새 축 5:  explicit-import-is-an-ordinary-import-g65 (MR)      search-path-comes-from-the-replay-context-g65 (MR)
          namespace-is-loaded-code-free-not-absent-g65 (MR)   the-fixture-measures-its-premise-g65 (tests/interpreter_fixture.py)
          the-token-probe-negative-is-asserted-g65 (tests/test_gate63_defensive.py — g64 AST 대조군도 같이 빨개짐, 선언에 포함)
g64 N1·N2 preimage 이동 (N1: 판정 함수의 `auto = …` → `auto = True`; N2: 새 `elif f:` 분기)
첫 재생에서 안 문 둘: g64 E2-R (AST 대조군이 탐침을 구분 안 함 → 탐침별로) · T1 (실측 함수 상수화는 skip 을 낳음 → 변이를 "활성 조건을 안 만든다" 로)
```

### 2-4. 전체 pytest · strict smoke

```
python -m pytest tests/ -q          <FULL_PYTEST>
./scripts/smoke_e2e.sh (clean 커밋) <SMOKE>
```

### 2-5. 두 환경 결과 (T1 최소 종결 조건 4)

```
이 기계: venv --system-site-packages → site.ENABLE_USER_SITE True  ·  일반 venv → False  (둘 다 실측, fixture 가 만든 것)
test_the_interpreter_fixture_measures_its_own_premise[True]  passed
test_the_interpreter_fixture_measures_its_own_premise[False] passed
활성 판 시험(on fixture) · 비활성 판 시험(off fixture) 전부 같은 실행에서 통과 — skip 0
```

## 3. 질문 (판단이 갈릴 수 있는 곳 — 되돌릴 수 있다)

1. **N1a 의 "세 상태" 를 조건·후보·이력으로 읽었다.** 부모가 `<absent>` 를 받는 조건은 "이력에
   없음 ∧ (자동 import 대상이 아니거나 후보가 없음)" 이다. 이력(`-X importtime -v` 손자)을 로드
   증인으로 쓰는 것이 의도와 다르면 대안은 부모가 자기 손자에서 `sys.modules` 를 직접 묻는 것인데,
   그것도 같은 startup 코드를 실행한다. 어느 쪽이 요구인가?
2. **`<built-in>`·`<frozen>` customization 은 명시 거부**한다 (대조할 바이트가 없다). 표준
   CPython 에서 `sitecustomize`/`usercustomize` 가 frozen 인 경우는 모른다 — 이 거부가 정상
   입력을 막을 수 있다고 보면 알려 달라.
3. **namespace identity = 종류 + `submodule_search_locations` 정규화 digest.** 리뷰어가 요구한
   "필요한 구조" 가 이것으로 충분한가, 아니면 각 위치의 디렉터리 목록(안의 파일 이름)까지 결속해야
   하는가? (코드가 없으므로 실행에 영향을 주는 바이트는 없다고 봤다.)
4. **T1 의 fixture 는 venv 로 전제를 만든다.** venv 를 못 만들거나 실측이 기대와 다르면 skip
   (이유에 실측값). CI 의 고정 환경에서 활성·비활성 둘 다 돈다는 증거는 이번엔 이 기계의 실행
   출력뿐이다 — "적어도 한 고정 환경" 요구를 이것으로 볼 수 있는가?
5. **E2-R 후속** — 공유 판정 함수 + 같은-token 음성 + 상수-True 회귀로 보류를 닫은 것으로
   봐도 되는가, 아니면 planned lifecycle 시험(`test_gate63_defensive.py` 479·487 줄의 token
   관측)에도 음성 관측을 넣어야 하는가? (후자는 lifecycle 중간에 lock 을 풀어야 해서 관측이
   상태를 바꾼다 — 그래서 안 넣었다.)

## 4. 다음 실행 계획

**GO 를 요청하지 않는다.** 이 라운드가 GO 로 판정돼도 본 실행은 별도 승인이고, ⑩ 등록부 격리와
§0 의 P0 조건이 그대로 열려 있다. 다음 라운드 후보 순서: ⑩ 격리 계약(별도 승인 뒤) → Q4
`error_code` 매트릭스.
