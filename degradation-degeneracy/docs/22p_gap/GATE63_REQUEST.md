# 63차 게이트 리뷰 요청 — 묶음 5 (실행 전 승인 · 보존 lifecycle)

## 판정 대상 (이 블록이 정본이다)

| 항목 | 값 |
|---|---|
| 브랜치 | `claude/14-gate-code-review-9qkx05` |
| **판정 대상 코드** | **`743f65bead671bf353ce38027c2e8e457738ec08`** (RUN_SCOPE 를 마지막으로 건드린 커밋) |
| `source_digest` (RUN_SCOPE `src/ tools/ configs/ scripts/ run.sh requirements*.txt`) | **`e9ee7475dea7de1d`** (직전 `fd7c90edbc56ff1f`) |
| 직전 판정 | 63차 **NO-GO** — P1 3건 · P2 1건 · 증거 공백 2 (리뷰어 제목은 "62차 묶음 5 — 방어적 코드·회귀 검토", 우리 원장 번호 63차) |
| 이번 라운드 | 접수 4건 + 공백 2건 **전부 코드에서 닫음** + 신고 **8건** (직전 라운드의 ①–⑦ 유지 + ⑧) |

> **fetch 는 브랜치 head 로 해 주기 바란다.** 요청문은 자기가 담길 커밋 SHA 를
> 적을 수 없다. 그래서 둘을 나눈다:
>
> - **판정 대상 코드** = `743f65b` — `source_digest e9ee7475dea7de1d` 이것을 가리킨다.
> - **이 문서** = 브랜치 head. `743f65b` 이후 커밋은 RUN_SCOPE 를 **한 바이트도**
>   안 건드렸다 (아래 재현).
>
> ```
> git fetch origin claude/14-gate-code-review-9qkx05 && git checkout FETCH_HEAD
> cd degradation-degeneracy
> python3 -c "import sys; sys.path.insert(0,'.'); from src.io import source_digest; print(source_digest())"
> # → e9ee7475dea7de1d 이어야 한다. 아니면 그 자체가 발견이다.
> git log --oneline 743f65b..HEAD -- src tools configs scripts run.sh requirements*.txt
> # → 출력이 비어야 한다.
> ```

**RUN_SCOPE 안에서 이번 라운드가 고친 것은 하나다** — `tools/archive_bundle.py` (F1).
그래서 `source_digest` 가 움직였다. **RUN_SCOPE 밖이지만 판정에 봐야 할 파일 둘** —
`docs/22p_gap/mutation_replay.py` (F2·F3·F4 증거층 + 변이 등록부) 와
`docs/22p_gap/row_projection.py` (E1 producer identity). 둘 다 `source_digest` 에
안 들어가지만 **cohort pin 과 변이 등록부의 정본**이므로 브랜치 head 의 그 두
파일을 봐 주기 바란다.

**환경 안내.** 전체 회귀는 `pybamm`·`tqdm`·`pyarrow` 를 요구한다 (`requirements.txt`).
`tests/test_docs_lint.py::test_a_smoke_run_cannot_be_promoted_to_a_canonical_report`
는 **작업 트리에 `results/grid_fit_v4` 가 있어야** 초록이다 (gitignored 실물 산출;
fresh clone 에는 없다 → 환경 실패이지 코드 발견이 아니다. 62·63차 리뷰어 환경에서도
같은 이유로 빨갰다). 그리고 이번에 새로 하나 — E2 의 실제 planned lifecycle 시험
`test_fit_phase_receipt_is_written_while_the_kernel_lock_is_held` 는 **clean 커밋에서만**
돈다 (dirty 면 skip, 사유를 출력한다): 진짜 producer 가 git 상태를 적고 fit 의
producer 검증(F74/F85)이 dirty worktree 곡선을 거부하기 때문이다 — smoke 와 같은
규칙이고 위조하지 않는다. detached clean worktree 에서는 돈다.

---

## §0 먼저 — 이번 라운드가 **하지 않은** 것

| 조건 | 상태 |
|---|---|
| **P0-1** producer 결속 — 닫힌 typed manifest 파싱 · 두 payload 압축해제 재해시 · producer 발행 영수증 | **미착수** (49차부터 **열다섯 라운드째**) |
| trusted launcher 의 source 측정 | **미착수** |
| **P0-4** typed 보존 영수증 **소비** | **부분** |
| 변이 증거의 **독립 replay** | **미착수** — 이번에도 checker 가 스스로 재생하지는 않는다. 리뷰어가 정적 대조로 확인한 것은 목록 정합성뿐이다 |
| 묶음을 **immutable content-addressed object** 로 먼저 게시 | **미착수** |
| 실행 class 5종 중 3종 미구현 · 등록부 삭제 절차 | **미착수** |
| baseline·sweep1d·wsweep 계획 gate · 실물 object-lock adapter · power-loss 모델 · publisher 전용 OS principal | **미착수** |
| 외적타당도 **#50** (`truth_provenance` 를 기계 계약에) | **미착수** |

리뷰어 재심 조건 6("§0 독립 GO 전제를 구현·입증")은 **이번 묶음이 닫지 않는다.**
위 표의 "미착수" 는 신고이지 종결이 아니다 — 그것을 안다.

### 이번 라운드가 스스로 신고하는 것 (**8건** — 직전 요청문 머리의 "5건" 은 본문 ①–⑦ 과 달랐다, 정정)

**①** 영수증 frame 의 한계 — child 의 startup 코드 전부는 못 막는다 (62차 §0-① 그대로).
부모 대조 층은 이번에 F3 로 **정상 package 까지** Python resolver 와 같은 규칙이 됐지만,
위조자가 자기 해시를 정직하게 적으면 여전히 못 막는다. 종결은 §0 표의 독립 replay 다.

**②** 승격이 막는 것은 "등록되지 않은 상태" 이지 "과거 상태로의 되돌림" 이 아니다 (62차 그대로).

**③** F68 이전 manifest(`fits_seal` 없음)는 direct bundle 창이 남는다 (62차 그대로).

**④** 보고서 sink 의 freshness 정책은 archive 와 다르다 (의도, 명시 — 62차 그대로).

**⑤** nested `wsweep/` 은 등록 자체가 없다 (62차 그대로).

**⑥** 시험이 공유 실행 class 등록부에 레코드를 남긴다 (61차부터 — 62차 그대로).
이번 E2 시험은 **임시 원장을 monkeypatch** 해 등록부가 그 원장 아래로 가게 했다 —
그 시험은 오염을 안 남긴다 (실측 `git status docs/22p_gap/_exec_class` 빈 출력).
다른 시험의 오염은 그대로다.

**⑦** `_stage_fit_inputs` 는 저장소 밖 절대 경로 입력을 staging 하지 못한다 —
**이번에 실측으로 재현됐다.** E2 의 첫 판을 저장소 밖 tempdir 에 뒀더니
`canonical_input_key` 가 절대 경로를 그대로 돌려줘 `stage / 절대경로` 가 원본
자신이 되고 `shutil.SameFileError` 로 죽었다. **고치지 않았다** — strict xfail
(`test_staging_an_input_outside_the_repo_is_still_unsupported`) 로 고정해, 고쳐지면
XPASS 로 빨개져 이 신고를 내리게 만든다. production 입력은 `results/` 안이라
지금 경로에서는 안 걸린다.

**⑧ (새)** E2 의 진짜 planned lifecycle 시험은 **PyBaMM 을 실제로 돈다** (조건 1개,
이 기계 2.6 s + 완방상태 3.8 s). solver 가 없는 환경에서는 그 시험이 error 다 —
환경 실패이지 코드 발견이 아니다. 그리고 `-X importtime -v` 의 `-v` 출력은
stderr 로 크다 — 손자 timeout 은 120 s 그대로다.

---

## §1 발견별 — 무엇이 틀렸고 무엇을 바꿨나

| ID | 무엇이 틀렸나 | 무엇을 바꿨나 | 증인 (시험) | 변이 축 |
|---|---|---|---|---|
| F1 (P1) | `archive_bundle bundle` 의 두 lock — list comprehension 뒤 try · finally 의 단순 for → 둘째 acquire 실패 시 첫 lock 미해제 · 첫 release 예외 시 둘째 미해제 | `_bundle_under_run_locks(run_dir, names, acquire, body)`: 하나씩 잡으며 목록에 넣고 전부 놓는다. 부분 취득 실패 → 얻은 것 놓고 그 오류 · 정리 예외 → 나머지도 시도, **첫** 정리 오류 · 본문 예외 → 원래 오류 보존 (정리 오류는 `add_note`). 해제 순서 = 취득 순서 | `test_gate63_defensive.py` F1 3건 (리뷰어 원문 2 + 본문 오류 보존 1) | `archive-releases-the-first-lock-when-the-second-fails-g63` · `archive-cleanup-tries-every-lock-g63` · (재조준) `promotion-checks-derived-freshness-g62` · `promotion-holds-the-run-locks-g62` |
| F2 (P1) | `-X importtime` 의 이름을 성공한 import 로 취급 → `site` 의 실패한 선택적 import 를 "올렸다 지운 module" 로 오분류 → 기본 Ubuntu 가 failed | 손자를 `-X importtime -v` 로. importtime = **시도** 전부, `-v` 의 `import 'X' # <loader>` = **성공한 로드만** (이 저장소 실측). 이름마다: 로드 → 지금 해시, 못 찾으면 failed(올렸다 지움) · 시도만 → `attempted_not_loaded` 에 기록하고 measured · `-v` 는 로드인데 customization 은 `<absent>` → failed. 이름 예외 목록이 아니다. schema 에 `attempted_not_loaded: [str]` | 같은 파일 F2 4건 (정상 선택적 import → measured · `sys.modules` 에서만 지움 → measured · 파일까지 지움 → failed · schema) + 62차 `test_evidence_receipt_62.py` 그대로 | `startup-history-runs-verbose-imports-g63` · `attempted-only-names-are-not-loaded-modules-g63` · `attempted-list-is-inside-the-receipt-g63` |
| F3 (P1) | 부모 customization 탐색이 `이름.py` 만 보고 package 를 안 봄 → 정상 환경 거부 | `importlib.machinery.PathFinder.find_spec(name, dirs)` — `.py` · package · 앞/뒤 root 가 child 와 같은 규칙. namespace package → `<absent>`, 파일 아닌 origin → loader 에게 묻고 못 주면 거부 | 같은 파일 F3 2건 (리뷰어 원문 + 앞 root `.py` vs 뒤 root package 대조군) · 62차 `the_real_probe_agrees_with_the_parent_view` | `parent-customization-uses-the-path-finder-g63` |
| F4 (P2) | `_HEX16` 을 `re.match` + `$` 로 → 후행 LF 17자 통과 | `fullmatch` | 같은 파일 F4 8건 (리뷰어 원문 2 + CRLF·공백·대문자·15/17자) | `hex16-is-a-fullmatch-g63` |
| E1 (공백) | 3.12 `type_params` 의 bound 를 scoped walker 가 방문 안 함 | `_definition_head` 가 bound(3.12)·default_value(3.13) 를 head 로 연다 — annotation scope 는 매개변수를 못 보므로 `inherited` 로 걷는다. type parameter 이름 자체는 shadow 로 안 센다 (거부 쪽). 첫 판의 `getattr(tp, attr)` 가 분석기 자신의 "계산된 이름 금지" 규칙에 걸려 `test_scope_model_62` 6건이 빨개졌다 → 리터럴 이름 둘 | 같은 파일 E1 3건 (리뷰어 원문 2 + bound 는 매개변수를 못 본다) — 3.11 컨테이너라 합성 AST 와 3.12 실제 파싱 두 경로 | `type-params-bounds-are-definition-head-g63` |
| E2 (공백) | lock-lifetime 시험이 경로 exists · smoke namespace(claim=None) 위의 관측 | smoke 밖·저장소 안 실제 planned lifecycle: 계획 원장 → grid 가 `may_open` 으로 발급받아 **진짜 solver** 로 조건 1개 → phase 닫음 → fit 이 token 으로 같은 claim 을 이어받아 commit → `claim.phase_done("fit")` durable 기록 → release. 기록이 쓰이는 순간 `.fit.lock` 을 **따로 열어 flock** → BlockingIOError (커널의 답) · 기록 직후와 release 시점에 claim 파일에 `phases.fit`. 탐침 대조군 별도 | 같은 파일 E2 2건 (clean 커밋 `743f65b` 에서 2 passed — §2.2) | — (production 순서는 62차 축 `fit-commits-inside-the-lock-g62` 가 이미 문다; 이 시험은 그 축의 증거를 planned claim 으로 넓힌 것) |

---

## §2 증거 — 전부 이 브랜치 head 에서 실행한 출력이다

### 2.1 판정 좌표

```
판정 대상 코드          743f65bead671bf353ce38027c2e8e457738ec08
source_digest          e9ee7475dea7de1d          (직전 fd7c90edbc56ff1f)
그 뒤 RUN_SCOPE diff    없음
    git log --oneline 743f65b..HEAD -- src tools configs scripts run.sh requirements*.txt
    → 빈 출력
```

### 2.2 회귀

```
python -m pytest tests/ -q      1 failed · 1735 passed · 2 xfailed (43분 22초)
    실패 = tests/test_docs_lint.py::test_a_smoke_run_cannot_be_promoted_to_a_canonical_report
             — 작업 트리에 results/grid_fit_v4 (gitignored 실물) 가 없는 환경 결손 (62·63차 리뷰어 환경 동일).
               PreserveError: [promote] … 에 manifest 가 없어 내용 identity 를 만들 수 없다 → 승격 거부 (fail-closed 가 도는 증거다)
    skipped 0 — E2 의 planned lifecycle 시험이 이 실행에서 **건너뛰지 않고 돌았다** (clean 커밋이라).
    이 실행 한 번 전(`743f65b` 트리)에는 docs_lint 가 9건 빨갰다. 8건은 이번 라운드가 닫았다:
      pin 검사 2 → g17→g18 세대 전환(`0254027`) · full_bundle_claims 1 → 원장의 영수증 core/validator 갱신 ·
      committed_gate_requests 1 → 62차 요청문이 `대상 커밋:` 줄을 빠뜨린 것(추가) ·
      coverage 3 + recorded_head 1 → 등록부가 274 로 늘어 커밋된 조각(266)과 어긋난 것 → 12조각 재생으로 닫음.
tests/test_gate63_defensive.py  22 passed · 1 xfailed (41.28s, 단독 실행)
    RED 첫 실행 10 failed · 12 passed (F1×3 · F3 · F4 · F2×2 · E1×2 · E2) → GREEN
    xfail(strict) 1 = §0 ⑦ 재현 — 저장소 밖 입력의 staging 이 SameFileError 로 죽는다 (고치지 않고 고정)
./scripts/smoke_e2e.sh          rc 0 — pipeline smoke 통과
    9절(보관 → 격리 복원 → 검증 → 재채점) 전부 초록 · 복원본 재채점 digest b69dd52d1ec4
    남은 경고는 62차와 같다: 실물 provider 어댑터 없음 (보존 회귀는 hermetic fake)
wiki/tools/lint.py              0 errors · 0 warnings
```

### 2.3 변이 등록부와 전수 재생

```
MUTANTS 243 · MULTI 31 · EXPECT 264 · DECLARED_MASKED 11
63차 축 8 (-g63) — 실행 8 · declared 0 · g62 재조준 2 (F1 refactor 로 preimage 가 죽은 archive 축 둘)
증인 문구는 기계 독립 (개수 · repr · 기계별 digest 를 뺐다 — 62차 ① 회차의 교훈)

--check-preimages               모든 변이 지점이 정확히 한 번 나타난다
-k g63                          8/8 물었다 (call 단계) · EXPECT 일치
slice 1..12 (HEAD 104448e, 순차)  12/12 rc 0 (2026-09-15 02:25Z → 03:54Z)
--check-coverage s*.json        모든 변이 지점이 정확히 한 번 나타난다
                                등록부 scenario 274 (executable 263 · declared 11) · 조각 12개에서 관측 274
                                조각 합집합이 등록부 전체를 정확히 덮었다

한 HEAD 규칙: 조각 12개가 전부 `104448e078208fb1cf288527f563a617f5bb3452` 에서
나왔다 — 재생 중에는 커밋하지 않았다. 조각 산출물은 `dcd4839` 에 있다.
① 회차(`526784a`)는 조각 9 에서 멈췄다: 62차 축
`history-refuses-a-vanished-module-g62` 의 증인 문구가 기계별 개수
(`unfiled=22`)를 담고 있었고 F2 의 `-v` 모델에서 이 기계는 26 이다. 문구에서
개수를 빼고 EXPECT 를 재관측한 것이 `104448e` 이고, ② 회차가 그 위에서 돌았다.
```

### 2.4 cohort 세대 전환 (g17 → g18) · `0254027`

대상 커밋: `0254027bf58de1cedc148a998a87395bbe44448f`
— 아래 `core_sha256` 은 이 커밋의
`docs/22p_gap/receipts/paired_fixed5_v4.validate.yaml` 을 가리킨다 (세대를 넘긴
커밋이고, 그 뒤로 영수증은 안 바뀌었다). 요청문이 인용한 값은 **그것이 이름한
커밋**에 대고 대조하는 것이 자기완결의 뜻이다.

```
g17_2026_09_14  active → frozen  (journal seq 16)
g18_2026_09_15  새 active · docs/22p_gap/proj_g18

pin  compute            14ff767d5fbd0d9d → 150416386d3c0b93
     row_projection     f85fc2b39e15d3d0 → b8eae978b9525c3e
     producer_semantic  814278bfcb82fa2f → 1d6c0e76f18d63ed
     src_scoring        69e69cb046f4b4ae (변동 없음)
     analysis_spec      43d74dd385b1f66d… (변동 없음)
영수증 core_sha256       3714cbbf3687a2ebffd81413f617b71f63705e0962e4745c6dc036cd01b81c01
validator                e9ee7475dea7de1d (검사 34건)
행 바이트                 ad598fe77e75afec — **열네 세대째 같다**
```

`row_projection.py paired_fixed5_v4 --cohort g18_2026_09_15` → 6138행 · restart
30690행 · 전체 True · by_obj True · fits삼중 True · 봉인일치 True. pin 을 움직인
것은 E1 하나 — producer analyzer 의 definition head 규칙이다. `src_scoring` 과
analysis spec 이 그대로이고 행 바이트가 안 움직인 것이 "이번 라운드는 증거·경계층만
건드렸고 계산식은 안 건드렸다" 를 실물로 말한다.

---

## §3 자체 리뷰

이번 라운드는 `/self-review` 를 **돌리지 않았다** (비용이 큰 subagent 절차라
사용자 요청이 있을 때만 돈다 — CLAUDE.md). 대신 고치는 중에 드러난 것을 적는다:
분석기가 자기 producer 닫힘을 분석하다 E1 첫 수정판의 계산된 이름을 스스로
거부한 것 (규칙이 자기 자신에게도 걸린다), F1 refactor 가 62차 변이 축 둘의
preimage 를 죽인 것을 `--check-preimages` 가 잡은 것, E2 첫 판이 §0 ⑦ 을 실측으로
재현한 것. 셋 다 `docs/GATE63_WORKING_STATE.md` "고치며 드러난 것".

---

## §4 판정 대상이 아닌 것 (혼동 방지)

이 라운드는 **계산식을 안 건드렸다.** `src.scoring` 과 analysis spec 은 그대로다
(세대 전환 표 §2.4). cross-cohort 비교는 금지다. 연구 수치의 정본은 artifact 와
`docs/RESULTS*.md` 이고, 이 문서의 숫자는 **게이트 판정용 좌표**다. pyDMA·BML·
COMSOL(§19 물리축 B 는 수신 측 검토값·원문 보존 전) 은 62차와 같이 판정 범위 밖이다.
