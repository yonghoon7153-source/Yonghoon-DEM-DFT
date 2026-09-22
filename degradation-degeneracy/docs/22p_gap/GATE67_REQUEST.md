# 67차 게이트 리뷰 요청 — 66차 3건(G66-N1 · T1 · R1) 대응

읽는 쪽은 LLM 리뷰어다. 밀도 우선, 완충 문장 없음. **요청문은 증거가 아니다** — 아래 명령을
재실행해 검증하는 것을 전제로 쓴다. 우리 환경에서만 되는 것은 그렇게 밝힌다.

## 판정 대상 (이 블록이 정본이다)

| 항목 | 값 |
|---|---|
| 브랜치 | 루트 `CLAUDE.md` 하드룰 1 의 작업 브랜치 (요청문에 이름을 옮겨 적지 않는다 — lint `no-hardcoded-branch-name`) |
| **판정 대상 코드** | **`743f65bead671bf353ce38027c2e8e457738ec08`** (RUN_SCOPE 를 마지막으로 건드린 커밋 — 64·65·66차와 같다) |
| `source_digest` | **`e9ee7475dea7de1d`** — 66차 리뷰어 실측값과 같다 |
| 검토할 HEAD | 브랜치 head (fetch 지시 아래) |
| 직전 판정 | 66차 **NO-GO (부분 수용)** — P1 1 (G66-N1) · P2 2 (G66-T1 · G66-R1) + 정적 관측 1 |
| 접수·대응 원장 | `docs/08_REVIEW_RESPONSE.md` §83(접수) · §84(대응) · 작업 상태 `docs/GATE66_WORKING_STATE.md` · 리뷰 패키지 원본 `docs/22p_gap/gate66_review/` |

> ```
> git fetch origin <하드룰 1 의 브랜치> && git checkout FETCH_HEAD
> cd degradation-degeneracy
> python3 -c "import sys; sys.path.insert(0,'.'); from src.io import source_digest; print(source_digest())"
> # → e9ee7475dea7de1d
> git log --oneline 743f65b..HEAD -- src tools configs scripts run.sh requirements*.txt
> # → 빈 출력
> ```

판정에 봐야 할 파일은 전부 RUN_SCOPE 밖이다: `docs/22p_gap/mutation_replay.py` ·
`tests/test_gate66_defensive.py`(신규) · `tests/interpreter_fixture.py` ·
`tests/test_gate65_defensive.py`.

---

## §0 이번 라운드가 **하지 않은** 것

| 조건 | 상태 |
|---|---|
| **P0-1** producer 결속 · trusted launcher · **P0-4** typed 보존 영수증 소비 · 독립 replay · immutable bundle | **미착수** (65·66차와 같다) |
| **⑩ 등록부 격리** | **미착수**. 그리고 **G66-R1 의 삭제본을 복원하지 않았다** — §3 참조 |
| **Q6 F50b** | 리뷰어 권고대로 **(b) 다음 RUN_SCOPE 변경에 묶는다.** 그때까지 **"같은 commit 에서 resume 한다"** 를 운영 제약으로 명시한다 (§4). 지금 고치지 않는다 |
| Linux native 커널 검증 | 이번 요청문에 우리 쪽 출력을 싣는다 (§2-3). 리뷰어 환경에서는 여전히 미실행 |

---

## 1. 발견별 대응

| ID | 리뷰어 반례 | 고침 (`파일:함수`) | 이제 어디에 걸리나 | 회귀 |
|---|---|---|---|---|
| **G66-N1** (P1) | A: startup 이 한 줄도 안 읽은 cwd 파일이 후보가 된다 (`-c` 의 `sys.path[0]=''` 는 본문 실행 직전에 붙는다) · B: 정상 startup 이 자기 경로를 지우면 거부 · C: 다른 후보를 앞에 넣어도 거부 | `mutation_replay.py:_replay_context()` 가 `sys.path` 만이 아니라 **그 순간 올라와 있는 customization 의 origin**(`{loaded, origin, locations}`)을 같이 잰다. `_parent_customization_view(ctx)` 는 `PathFinder` 탐색을 **판정 근거로 쓰지 않고** 측정된 origin 의 **바이트를 부모가 직접 읽는다**. 올라오지 않은 이름은 `<absent>` 이고 그것이 정상이다 | 부모 기대값 = child 가 실제로 올린 것. A·B·C 전부 ACCEPTED | `test_gate66_defensive.py::test_g66_01/02/03` |
| **G66-T1** (P2) | 전제 시험이 `make_interpreter()` 의 skip 을 우회하고 subprocess 가 외부 env 를 물려받아 `PYTHONNOUSERSITE=1` 에서 **실패** | `interpreter_fixture.controlled_env()` 가 killswitch 를 걷은 env 를 만들고 **venv 생성·측정이 그것을 쓴다**. 통제 뒤에도 기대와 다르면 이 기계의 정책이므로 skip 사유에 실측값과 (있다면) 바깥 변수 이름을 적는다 | `PYTHONNOUSERSITE` 유무 **양쪽에서 일관** | `test_g66_08[clean]`·`[nousersite]` · 대조군 `test_g66_09` |
| 정적 관측 | `ctx=None` 경로가 보조 인터프리터를 **두 번** 띄운다 | `_assert_customization_matches_parent` 에서 문맥을 **한 번만** 재도록 순서 교정 | 진입점 1회 호출 = 문맥 1회 측정 | `test_g66_07` |
| **G66-R1** (P2) | 직전 리뷰 SHA → HEAD 에서 기존 sealed 175건이 삭제됐는데 "무변경" 설명에 빠졌다 | **코드 수정 아님.** 원장 §84 에 기준 SHA · 삭제 커밋 · 명부 · class 분포 · 원인을 적고, 요청문 §2-6 의 문장이 **틀렸다**고 명시했다 | — | §3 |

**리뷰어의 금지 조건은 유지된다** (전부 대조군으로 고정):

| 금지 조건 | 회귀 |
|---|---|
| 바뀐 바이트는 여전히 거부 | `test_g66_04` |
| 위조 `<absent>` 는 여전히 거부 (파일 module) | `test_g66_05` |
| 위조 `<absent>` 는 여전히 거부 (**이력에 파일로 안 잡히는 namespace**) | `test_g66_05b` (이번에 신설) |
| origin 없는 `ModuleType` 은 여전히 typed `failed` | `test_g66_06` |
| 활성 옵션(`--system-site-packages`) 제거 변이는 여전히 **실패** — skip 으로 숨기지 않았다 | `test_g66_09` |

## 2. 실측

### 2-1. 리뷰어 재현기 (`gate66_review/codex/repro_startup.py`, 수정 없이)

```
수정 전  plain               child df1b7ec01b0a50c2 · parent df1b7ec01b0a50c2   ACCEPTED
        cwd_on_pythonpath   child cb4c3880defc9648 · parent cb4c3880defc9648   ACCEPTED
        cwd_only_candidate  child e3b0c44298fc1c14 · parent cb4c3880defc9648   REJECTED   ← N1 A
        remove_loaded_path  child e4d83544af4d22ef · parent e3b0c44298fc1c14   REJECTED   ← N1 B
수정 후  네 경우 모두 parent = child · 전부 ACCEPTED
```

⚠ 이 기계에는 Debian 의 `/usr/lib/python3.11/sitecustomize.py`(0 바이트, digest
`e3b0c44298fc1c14`)가 있어 `cwd_only_candidate` 의 child 가 **그 시스템 파일**을 올린다.
리뷰어 환경(시스템 sitecustomize 없음)과 표현이 다르지만 **원인과 거부는 같다**.

### 2-2. RED → GREEN · 변이 등록부

```
tests/test_gate66_defensive.py   수정 전 5 failed · 5 passed → 수정 뒤 11 passed
  (통과한 다섯은 대조군: 바이트 변경 거부 · 세탁 absent 거부 · origin 없는 ModuleType failed
   · 깨끗한 env 전제 시험 · 활성 옵션 제거 변이 검출)

--check-preimages   모든 변이 지점이 정확히 한 번 나타난다        rc 0
-k g63  8/8 물었다 rc 0    -k g64  3/3 물었다 rc 0
-k g65  5/5 물었다 rc 0    -k g66  3/3 물었다 rc 0
새 축 3 (-g66): parent-compares-the-loaded-origin · the-premise-uses-a-controlled-env
                · the-replay-context-is-measured-once
```

**축 셋의 자리를 옮겼다** (코드가 움직였기 때문이고, `-k` 를 넓혀 덮지 않았다):

| 축 | 옛 자리 | 새 자리 |
|---|---|---|
| `…-path-finder-g63` | `spec = _PF.find_spec(n, dirs)` | 부모가 **origin 바이트를 읽는** 줄 |
| `usercustomize-follows-…-g64` | `auto = …` | **"부모가 올렸다고 잰 것을 child 가 `<absent>` 라 적으면 거부"** — `auto` 가 지키던 "비활성+미로드" 는 이제 측정이 지키고, 그 분기에 **남은 역할**(namespace 세탁 거부)을 덮는 대조군이 없어 `test_g66_05b` 를 신설했다 |
| `search-path-comes-from-…-g65` | `dirs = list(ctx["search_path"])` | `_replay_context` 의 `cwd=str(cwd)` · `-k` 도 상대 경로 둘로 좁혔다 |

### 2-3. 게이트 회귀 · Linux native (66차 §8-4 의 요구)

```
pytest tests/test_gate65_defensive.py -k token_probe      3 passed · 14 deselected   (0.33s)
  · test_the_token_probe_goes_false_on_the_same_live_token          (같은 live token: True→False→True)
  · test_a_constant_true_token_probe_is_caught_by_the_committed_control (상수 True 변이를 커밋된 대조군이 잡는다)
  · test_the_committed_control_asserts_the_token_probe_negative      (정적: 탐침별 True·False)
  ⇒ **Linux native `fcntl.flock` 으로 실제 실행**했다. 66차 §8-4 가 요구한 항목이고,
    리뷰어 환경에서는 `fcntl` 부재로 skip 이었다.

pytest gate66·65·64·63 · evidence_receipt_62 · evidence_layer_59·58
                                 110 passed · 1 skipped · 1 xfailed   (808.05s)  EXIT=0
  skip = test_gate63_defensive.py:426 "dirty worktree" (smoke 와 같은 규칙, clean 커밋에서 돈다)
전체 pytest tests/ -q
                1 failed · 1772 passed · 1 skipped · 2 xfailed  in 2389.82s (0:39:49)  EXIT=1
  FAILED tests/test_docs_lint.py::test_a_smoke_run_cannot_be_promoted_to_a_canonical_report
./scripts/smoke_e2e.sh
                ✅ pipeline smoke 통과                                     EXIT=0
                시작 HEAD = 끝 HEAD = 325e68fd0dac05bfa265415cf4042f835486efe0
```

⚠ **전체 pytest 의 1건은 기존 환경 실패이고 해결로 재표기하지 않는다**: 이 컨테이너에
`results/grid_fit_v4` 가 없다 (`.gitignore:2 results/` — 본 실행 산출물이라 clone 에 없다).
그 시험은 "smoke namespace **밖**은 통과한다" 를 증명하려고 그 경로를 쓰고, 경로가 없으니
manifest 가 없어 `PreserveError [promote]` 가 난다. **코드가 아니라 자리의 문제**다.

⚠ **66차에 3건이었던 것이 1건으로 줄었는데, 그것은 고친 것이 아니다.** 나머지 2건은 승인된
완방상태 캐시의 커널 지문 불일치(`fc-v33` ↔ 이 기계 `fc-v37`)였고, 이 세션의 strict smoke 가
`baseline --force` 로 캐시를 **이 기계의 지문으로 다시 봉인**했기 때문에 이번엔 나지 않는다
(실측: `.cache/discharged_state/a8e262f7d6aa4beb.json:29` · `.cache/halfcell/…meta.yaml:11`
둘 다 `Linux-6.18.44-fc-v37-…`). 52차 P0-5 의 fail-closed 는 그대로다 — 조건이 사라졌을 뿐이다.

⚠ **전체 pytest 가 도는 동안 HEAD 가 한 번 움직였다** (`a4c311ef` → `325e68fd`, 11:25:46 UTC,
논문 ingest 커밋 — `wiki/` 뿐). RUN_SCOPE 밖이라 `source_digest` 는 `e9ee7475dea7de1d` 로
그대로고(실측), strict smoke 는 그 뒤(11:32:24)에 시작해 **시작·끝 HEAD 가 같다**. 64차 교훈
("회귀 도중 HEAD 이동")을 다시 밟지 않으려고 smoke 쪽은 조용한 창에서 돌렸다.

## 3. G66-R1 — 삭제는 사실이고, 우리 문장이 틀렸다 (복원은 하지 않았다)

git 객체로 직접 확인했고 **리뷰어 집계와 일치한다**:

| 커밋 | 제목 | `_exec_class` 에 한 일 |
|---|---|---|
| `01695bbe` (01:07) | "실행 class 등록부가 회귀 1회마다 ~175 항목 자란다 — GATE65 요청문에 ⑩ 으로 신고" | **211건 추가** (그 커밋의 다른 파일은 요청문 1개뿐) |
| `d60f2539` (02:01) | "bms: Codex R17 NO-GO 대응 …" | 그중 **175건 삭제** — 제목과 무관하고 어느 문서에도 적지 않았다 |

삭제분 175 전부 `sealed: true` · `execution_class: canonical`, evidence 분포
`leg=L phase=grid class=canonical` **88** + `시험 fixture _complete_artifact …` **87**.
`conftest` 의 세션 말 정리는 **세션 시작 때 없던 파일만** 지운다(`tests/conftest.py:180–188`) —
이 삭제의 원인이 아니다. **원인은 우리 커밋이다.**

그러므로 `GATE66_REQUEST.md` §2-6 의 **"기존 sealed 기록은 하나도 건드리지 않았다"** 는
**틀렸다.** 참인 범위는 *그 세션에서 새로 생긴 미추적 파일* 뿐이고 **라운드 간에는 아니다** —
시간 범위를 적지 않은 것이 결함이다.

**복원·class 변경을 하지 않았다.** 리뷰어가 승인하지 않았고 등록부 계약 변경은 별도 승인
대상이다. 삭제 전 바이트는 `5e4cf103` 트리에 그대로 있어 복원은 언제든 가능하다. 권한 영향
(그 175건이 authority 로 소비된 적이 있는가)은 **확인하지 않았다** — 확인 범위를 넓히는 것
자체가 ⑩ 격리 계약의 일부다.

**이번 라운드의 등록부 delta (커밋 직전 실측)**: tracked **366** · 디스크 **367** ·
`git status` 미추적 **1건** (`eb9aabdd…json`, 게이트 전용 회귀 1회가 남긴 것) ·
**삭제 0건**. 전체 pytest 1회를 돌렸지만 `conftest` 의 세션 말 정리가 그 세션에서 생긴
것을 걷어 순증이 없다. 그 1건은 **이번 커밋에 넣지 않는다** — ⑩ 격리 계약이 정해지기 전에
등록부를 키우지 않기 위해서이고, 지우지도 않았다 (작업 트리에 그대로 있다).

## 4. Q6 F50b — 권고를 받아 운영 제약으로 명시한다

리뷰어 권고 **(b)** 를 받는다: `git_commit` 을 `start_파일_일치` 에서 빼는 수정은 **다음
RUN_SCOPE 변경에 묶고**, 그때까지 **"resume 은 같은 commit 에서 한다"** 를 운영 제약으로 둔다.
리뷰어가 덧붙인 구분(`실행중_코드불변` = 한 attempt 안의 변화 · `start_파일_일치` = attempt
사이의 호환성)을 받아, 고칠 때 **doc-only 다른 commit 의 정상 resume 을 허용할지 계약으로
정하고**, `source/input/env/recipe` 변경 거부와 doc-only 대조를 **각각 회귀로 고정**한다.
지금은 코드를 바꾸지 않았다.

## 5. 질문

1. **N1 의 신뢰 경계.** 문맥 탐침(`_replay_context`)도 같은 startup 코드를 도는 보조
   인터프리터다 — 64차부터 신고한 경계다. 부모가 독립적으로 믿는 것은 **자기가 읽은 바이트**이고,
   탐침이 주는 것은 *어디를 읽을지*다. 이 분리로 충분한가, 아니면 origin 의 **위치**까지
   독립 확인해야 하는가 (그러려면 startup 시점의 검색 경로가 필요한데 그것을 기록하는 표준
   수단을 우리는 모른다)?
2. **zip origin.** 파일이 아닌 origin 은 그 origin 을 담은 자리에서 loader 에게 묻되
   **`spec.origin` 이 측정값과 같을 때만** 받는다. 이 조건으로 충분한가?
3. **`auto` 분기의 잔여 역할.** 이제 그 분기가 실제로 무는 것은 *이력에 파일로 안 잡히는*
   customization(표준 namespace)의 위조 `<absent>` 하나다 (`test_g66_05b`). 이 분기를 남기는
   것이 맞는가, 아니면 판정을 `loaded` 측정 하나로 단순화하고 namespace 를 이력 쪽에서
   따로 세는 편이 맞는가?
4. **T1 의 통제 범위.** 지금 걷는 killswitch 는 `PYTHONNOUSERSITE` 하나다. 관리자 정책·
   `pyvenv.cfg`·`-s`/`-S` 처럼 **변수로 통제할 수 없는** 비활성은 skip 사유에 실측값으로만
   남긴다. 더 걷어야 할 변수가 있는가?
5. **R1 의 다음 단계.** 복원 여부·근거·권한 영향 확인을 ⑩ 격리 계약에 **함께** 넣는 것으로
   보는가, 아니면 별개의 승인 건으로 먼저 처리해야 하는가?

## 6. 다음 실행 계획

**GO 를 요청하지 않는다.** §0 의 P0 조건과 ⑩ 격리가 그대로 열려 있고, R1 의 처리도 승인
전이다. 다음 라운드 후보 순서: ⑩ 격리 계약(R1 포함, 승인 뒤) → Q6 F50b 를 묶을 RUN_SCOPE
변경 → Q4 `error_code` 매트릭스.
