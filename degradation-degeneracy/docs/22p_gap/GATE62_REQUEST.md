# 62차 게이트 리뷰 요청 — 묶음 5 (실행 전 승인 · 보존 lifecycle)

## 판정 대상 (이 블록이 정본이다)

| 항목 | 값 |
|---|---|
| 브랜치 | `claude/14-gate-code-review-9qkx05` |
| **판정 대상 코드** | **`0dcbc17aa73ef1fc8ac681e2b0617da68a86ceb4`** (RUN_SCOPE 를 마지막으로 건드린 커밋) |
| `source_digest` (RUN_SCOPE `src/ tools/ configs/ scripts/ run.sh requirements*.txt`) | **`fd7c90edbc56ff1f`** (직전 `4227b40871fa0c10`) |
| 직전 판정 | 62차 **NO-GO** — P0 8건 · P1 6건 · P2 2건 (리뷰어 제목은 "61차 묶음 5", 우리 원장 번호 62차) |
| 이번 라운드 | 접수 16건 **전부 코드에서 닫음** + 자체 리뷰 4 렌즈가 잡은 10건 코드로 닫음 + 신고 5건 |

> **fetch 는 브랜치 head 로 해 주기 바란다.** 요청문은 자기가 담길 커밋 SHA 를
> 적을 수 없다. 그래서 둘을 나눈다:
>
> - **판정 대상 코드** = `0dcbc17` — `source_digest fd7c90edbc56ff1f` 이것을 가리킨다.
> - **이 문서** = 브랜치 head. `0dcbc17` 이후 커밋은 RUN_SCOPE 를 **한 바이트도**
>   안 건드렸다 (아래 재현).
>
> ```
> git fetch origin claude/14-gate-code-review-9qkx05 && git checkout FETCH_HEAD
> cd degradation-degeneracy
> python3 -c "import sys; sys.path.insert(0,'.'); from src.io import source_digest; print(source_digest())"
> # → fd7c90edbc56ff1f 이어야 한다. 아니면 그 자체가 발견이다.
> git log --oneline 0dcbc17..HEAD -- src tools configs scripts run.sh requirements*.txt
> # → 출력이 비어야 한다.
> ```

**RUN_SCOPE 밖이지만 이번 라운드가 크게 고친 파일 둘** —
`docs/22p_gap/row_projection.py` (producer identity · δ′ + 자체 리뷰 sig 렌즈) 와
`docs/22p_gap/mutation_replay.py` (변이 재생·증거층 · ε′ + 자체 리뷰 영수증
렌즈). 둘 다 `source_digest` 에 안 들어가지만 **cohort pin 과 변이 등록부의
정본**이므로 판정에는 브랜치 head 의 그 두 파일을 봐 주기 바란다.

**환경 안내.** 전체 회귀는 `pybamm`·`tqdm`·`pyarrow` 를 요구한다 (`requirements.txt`).
그리고 `tests/test_docs_lint.py::test_a_smoke_run_cannot_be_promoted_to_a_canonical_report`
는 **작업 트리에 `results/grid_fit_v4` 가 있어야** 초록이다 (gitignored 실물 산출;
fresh clone 에는 없다 → 환경 실패이지 코드 발견이 아니다. 61차 리뷰어 환경에서도
같은 이유로 빨갰다).

---

## §0 먼저 — 이번 라운드가 **하지 않은** 것

| 조건 | 상태 |
|---|---|
| **P0-1** producer 결속 — 닫힌 typed manifest 파싱 · 두 payload 압축해제 재해시 · producer 발행 영수증 | **미착수** (49차부터 **열네 라운드째**) |
| trusted launcher 의 source 측정 | **미착수** |
| **P0-4** typed 보존 영수증 **소비** | **부분** |
| 변이 증거의 **독립 replay** | **미착수** — ε′ 는 영수증의 위조 면을 좁혔을 뿐 checker 가 스스로 재생하지는 않는다 |
| 묶음을 **immutable content-addressed object** 로 먼저 게시 | **미착수** |
| 실행 class 5종 중 3종 미구현 · 등록부 삭제 절차 | **미착수** |
| baseline·sweep1d·wsweep 계획 gate · 실물 object-lock adapter · power-loss 모델 · publisher 전용 OS principal | **미착수** |
| 외적타당도 **#50** (`truth_provenance` 를 기계 계약에) | **미착수** |

### 이번 라운드가 스스로 신고하는 것 (자체 리뷰 4 렌즈의 실측 포함)

**① 영수증 frame 의 한계 — child 의 startup 코드 전부는 못 막는다.**
ε′ 가 닫은 것은 "stdout 에 **덧붙이기**"(atexit · `os.write` 앞뒤) 뿐이다. 자체
리뷰가 실측했다: `sys.stdout` 교체 · fd 층(`dup2` 로 1 을 돌리고 원본에 write) ·
`builtins.print` 교체 — 셋 다 진짜 frame 을 삼키고 세탁본을 내며 **ACCEPTED**.
child 는 `sys.orig_argv` 로 자기 `-c` 소스를 읽어 frame 도 안다. 둘째 층을
뒀다 — 부모가 **자기 프로세스에서** `customization`(site · sitecustomize ·
usercustomize 바이트)을 같은 검색 순서로 재서 child 와 대조한다
(`_assert_customization_matches_parent`). 위조 파일을 `<absent>` 로 세탁하면 거기서
걸린다. **위조자가 자기 해시를 정직하게 적으면 여전히 못 막는다** — 환경을 그
환경 안에서 재는 층의 한계이고, 종결은 §0 표의 독립 replay 다.

**② 승격이 막는 것은 "등록되지 않은 상태" 이지 "과거 상태로의 되돌림" 이 아니다.**
봉인에는 서명이 없다. fit member 를 지우고 grid 시점의 봉인을 복원하면 grid 의
등록된 canonical 상태로 승격된다 — 그것은 grid commit 이 실제로 봉인·등록한
상태이므로 세탁이 아니지만, "승격은 지금 있는 것으로 되돌아가지 않는다" 는
문장의 정확한 범위는 **원장에 봉인·등록된 상태 사이**다 (`_promotion_content_id`
docstring 에 적었다). 방어선은 봉인이 아니라 원장 등록이다.

**③ F68 이전 manifest(`fits_seal` 없음)는 direct bundle 창이 남는다.**
identity 는 manifest 바이트만 담는다. manifest(+봉인)만 복사하고 `fits.parquet`
을 바꾸면 identity 층은 통과하고, `archive_bundle.bundle()` 의 `_seal_conflicts`
(`manifest.fits_seal.file_sha256` ↔ 실물)가 거부한다. production fit 은 언제나
`fits_seal` 을 넣으므로(`src/fitting.py`) 실물 artifact 셋은 닫혀 있지만,
`fits_seal` 없는 옛 manifest 를 직접 `bundle` 하면 통과한다. legacy roster 4개
dir 는 이 clone 에 없어 미확인.

**④ 보고서 sink 의 freshness 정책은 archive 와 다르다 (의도, 명시).**
`tools/make_results.py` 의 보고서 sink 는 `assert_not_smoke_provenance` 를 직접
부른다 (승격 판정은 `for_promotion=True` 로 내부에서 지난다). 파생 freshness 는
거부가 아니라 **재계산 렌더 + 인용 금지 배너**(F77)다. `assert_promotable` 에
셋째 검사가 붙으면 보고서 sink 가 또 빠질 수 있다 — 구조 시험
(`test_the_promotion_primitive_is_one_function`)은 `archive_bundle.main` 만 고정한다.

**⑤ nested `wsweep/` 은 등록 자체가 없다.** `src/weight_sweep.py` 는
issue/commit 을 안 부르므로 부모 승격이 nested 를 판정하지 않는다 (결속은
`_seal_conflicts` 의 자기일관성 + `make_results` 의 `sweep_vs_main` 뿐). 외부
wsweep 디렉터리를 갈아 끼워도 `archive_bundle bundle` 이 안 거부한다.

**⑥ (61차부터 이어짐) 시험이 공유 실행 class 등록부에 레코드를 남긴다.**
이번 라운드도 고치지 않았다 — `_complete_artifact` 등 fixture 가 `ledger=None`
으로 실물 `docs/22p_gap/_exec_class/` 에 쓴다. session fixture 가 끝에서 지우지만
중단된 실행은 남긴다 (이번 마감에서 두 번 `git clean` 했다).

**⑦ `_stage_fit_inputs` 는 저장소 밖 절대 경로 입력을 staging 하지 못한다**
(`SameFileError`, diff 이전부터). 이번엔 안 고쳤다.

---

## §1 발견별 — 무엇이 틀렸고 무엇을 바꿨나

판정문의 **세 문장**으로 묶는다.

> ① temporal seal 이 "등록된 실행의 고정 identity" 가 아니라 **우연히 남은, 과거에 등록된 prefix** 로 되돌아간다
> ② run lock 은 발급이 원자적이지 않고, 정상 fit/grid 는 **봉인·class 등록 전에** lock 을 놓는다
> ③ producer scope 모델이 아직 Python 과 다르다 — 셋 다 **digest 같고 계산은 1→9**

| ID | 무엇이 틀렸나 | 무엇을 바꿨나 | 증인 (시험) | 변이 축 |
|---|---|---|---|---|
| P0-1 | stale/subset seal 이 과거 canonical prefix 로 fallback — 진행 중 fit · fit member 삭제 상태가 승격 | **승격 판정과 전이 조회를 갈랐다.** `_promotion_content_id()`: 봉인 낡음 → 거부, 지금 있는 identity member 를 다 안 담음 → 거부, 봉인 없음은 현재 목록이되 레코드가 `sealed` 면 거부. commit 레코드에 `sealed: true`. 전이(`run_content_id`·`issue_execution_class`)는 60·61차 관용 그대로 | `test_promotion_seal_62.py` 7건 (+ 61차 temporal 7건 그대로) | `promotion-refuses-a-stale-seal-g62` · `promotion-refuses-a-subset-seal-g62` · `sealed-records-need-their-seal-g62` |
| P0-2 | lock 이 `exists()`→`write_text()` — 두 contender 동시 성공 | `O_CREAT` + `flock(LOCK_EX\|LOCK_NB)` + (dev,ino) 재확인 → `RunLock` token | `test_run_lock_62.py` 10건 (barrier 2-contender · 8 프로세스 peak 1) | `run-lock-exclusivity-is-a-kernel-op-g62` |
| P0-3 | fit/grid 가 봉인·commit 전에 lock 을 놓음 → 첫 실행이 둘째 bytes 봉인 | token 이 dir_fd 를 들고 있어 commit 이 handle 을 닫은 뒤에도 놓는다 → compute → commit → receipt → release. grid 는 merge·manifest·`write_curves_manifest`·`phase_done` 까지 lock 안 | `test_lock_lifetime_62.py` (fit 순서 spy · grid AST `min(release)`) · smoke 7b (resume 뒤 lock 정리) | `fit-commits-inside-the-lock-g62` · `grid-merges-inside-the-lock-g62` |
| P0-4 | grid `manifest.yaml` 의 `curves_parquet=/proc/self/fd/N/…` 이 fit 에 봉인됨 | `_grid_manifest_payload(named_out, merged, …)` — 이름 기준 | 같은 파일 2건 · smoke 8b (굳은 기록 scan) | `grid-manifest-locator-is-the-name-g62` |
| P0-5 | random `fit-stage-*` 가 run_spec 에 → run_sig 매번 변경, resume 무효 | `"base_config": _ck(...)` — staging 뿌리 기준 논리 key (`base_config_sha` 와 같은 key) | 같은 파일 2건 (resume → journal 1개 · manifest 에 `fit-stage-` 없음) · smoke 7b | `run-sig-has-no-staging-pathname-g62` |
| P0-6 | class local 을 method 에, parameter 를 definition head 에 적용 | `_definition_head()` 는 바깥 집합, class 는 자식 scope 에 `inherited`. **자체 리뷰가 하나 더**: class 본문·module 문장의 결속은 `LOAD_NAME` 이라 위치 의존 → 함수·lambda 만 결속 shadow (fail-closed) | `test_scope_model_62.py` 27건 (Python 진실 exec + 분석기 + guard e2e) | `definition-head-is-the-enclosing-scope-g62` · `class-body-bindings-are-not-shadows-g62` · (declared) `class-locals-stay-in-the-class-body-g62` — F3 가 class 의 `here == inherited` 로 만들어 의미를 못 바꾼다, 사유는 `DECLARED_MASKED` |
| P0-7 | crossed scoring 을 primary 의 symbol table 로 분석 | `_producer_closure` 가 module 별 table (`tables["rp"|"sc"]`). **자체 리뷰가 둘 더**: 건너간 module 의 자기 이름 공간 접근을 walk 가 따라감 · `from src import scoring as me` 수집, `import src as S` 는 fail-closed 거부 | 같은 파일 | `crossed-module-uses-its-own-symbol-table-g62` · `crossed-module-self-alias-is-followed-g62` · `from-imports-are-namespace-targets-g62` · `parent-package-import-is-refused-g62` · (재조준) `closure-follows-module-aliases` |
| P0-8 | direct `archive_bundle bundle` 이 derived freshness 우회 | `assert_promotable()` = smoke·등록·봉인 + freshness, `archive_bundle.main` 이 지난다. **자체 리뷰가 하나 더**: 검사↔복사 사이 writer 를 막으려고 `.fit.lock`·`.run.lock` 을 든 채 검사+복사 | `test_archive_freshness_62.py` 5건 | `promotion-checks-derived-freshness-g62` · `promotion-holds-the-run-locks-g62` |
| P1-1 | own lock 의 malformed/unreadable 을 release 가 삼킴 | release 는 token 만 받고 inode 로 판정 — 사라짐/바뀜은 올리고, 경로 인자는 `TypeError` | `test_run_lock_62.py` · 61차 `test_logical_paths_61.py` 2건 정정 | `release-consumes-a-token-not-a-path-g62` · `release-refuses-a-replaced-inode-g62` · `release-refuses-a-vanished-lock-g62` · (재조준) g61 2개 |
| P1-2 | dry-run · pre-commit 실패가 capability/fd 를 폐기 안 함 | `discard_capability_on_abort` (fit·grid 공용). **자체 리뷰가 잡은 것**: capability 는 lock 앞에서 발행되므로 lock 거부·발행↔lock 사이 예외가 빠져 있었다 → try 를 발행 직후로 | `test_lock_lifetime_62.py` 7건 (dry-run · 계산 실패 · 보유자 거부 ×2 · lock 앞 예외 ×3) | `fit-failure-discards-the-capability-g62` · `grid-dry-run-discards-the-capability-g62` · `capability-discarded-before-the-lock-g62` · `grid-discards-before-the-lock-g62` |
| P1-3 | startup 코드가 stdout 마지막 줄로 영수증 위조 | frame — 정확히 한 frame 일 때만 받는다 (§0-①: 한계와 둘째 층) | `test_evidence_receipt_62.py` (atexit 실제 재현 · parser 5 형태 · 부모 대조) | `receipt-is-framed-g62` · `parent-cross-checks-customization-g62` |
| P1-4 | `<unreadable>`·zipimport→unfiled 가 measured 로 세탁 | `_Unreadable` → 섹션 `failed`; zip origin 은 `loader.get_data`; `find_spec→None` 은 `failed` (헤더 줄 파싱 버그가 그 경로의 정상 사례였다) | 같은 파일 (zip 실제 · `.pth` 디렉터리 · 올렸다 지운 module) | `unreadable-bytes-fail-the-section-g62` · `zip-origins-are-hashed-g62` · `history-refuses-a-vanished-module-g62` |
| P1-5 | duplicate distribution 을 뒤 root 로 덮음 | `sys.path` 순서 첫 것, `shadowed` 에 위치와 함께, Name 없는 dist 는 stem 키; dist-info 파일 바이트도 `importable_roots` 에 | 같은 파일 (Python 진실 대조 포함) | `packages-keep-the-first-distribution-g62` · `dist-info-bytes-are-in-the-receipt-g62` |
| P1-6 | 한 receipt 를 여러 번 측정 | `ReceiptSnapshot` — 재생·checker 가 한 번 재서 tag·본문·digest 를 같은 바이트에서 | 같은 파일 (AST 구조 + 스냅샷) | `coverage-records-the-snapshot-it-was-given-g62` |
| P2-1 | completeness 가 `status` 만 검사 | `_RECEIPT_SCHEMA` 재귀 exact + 교차 필드 (빈 값 · `startup.env==env` · `version==interpreter` · 음수) | 같은 파일 · fixture `tests/receipt_fixture.py` (61차 최소 dict 는 깨졌다) | `receipt-schema-is-exact-g62` · `schema-refuses-empty-receipts-g62` |
| P2-2 | 없는 `_canon_*` 인용 · docstring 이 `ast.unparse` | 정정 + 인용 lint | `test_contract_citations_62.py` 2건 | — (문서) |

---

## §2 증거 — 전부 이 브랜치 head 에서 실행한 출력이다

### 2.1 판정 좌표

```
판정 대상 코드          0dcbc17aa73ef1fc8ac681e2b0617da68a86ceb4
source_digest          fd7c90edbc56ff1f          (직전 4227b40871fa0c10)
그 뒤 RUN_SCOPE diff    없음
    git log --oneline 0dcbc17..HEAD -- src tools configs scripts run.sh requirements*.txt
    → 빈 출력
```

### 2.2 회귀

```
python -m pytest tests/ -q      1713 passed, 1 failed, 1 xfailed   (26분 22초)
    실패 1 = tests/test_docs_lint.py::test_a_smoke_run_cannot_be_promoted_to_a_canonical_report
             — 작업 트리에 results/grid_fit_v4 (gitignored 실물) 가 없는 환경 결손.
             61차 리뷰어 환경에서도 같은 이유로 빨갰다. 코드 발견이 아니다.
./scripts/smoke_e2e.sh          pipeline smoke 통과 (✅ 54건, exit 0) — 0dcbc17, RUN_SCOPE clean
                                새 단계 7b (resume → journal 1 · lock 정리 · 봉인/승격 판정 · 보고서 갱신)
                                · 8b (굳은 기록 58개 scan: handle·staging·없는 경로 0) 포함
wiki/tools/lint.py              0 errors
```

회귀는 12조각 증거 커밋(`2a4ca8a`) 트리에서 받았다. 그 뒤 커밋은 `docs/` 만
건드렸다 — RUN_SCOPE 의 dirty 판정은 `src/ tools/ configs/ scripts/ run.sh
requirements*.txt` 만 보므로 smoke 의 전제는 그대로다.

### 2.3 변이 등록부와 전수 재생

```
MUTANTS 235 · MULTI 31 · EXPECT 256 · DECLARED_MASKED 11
62차 축 33 (접수 16건에 22 · 자체 리뷰 11) — 실행 32 · declared 1
g61 재조준 4 (lock 2 · closure 2)

--check-preimages               모든 변이 지점이 정확히 한 번 나타난다
slice 1..12 (HEAD 1b4a837, 순차)  전부 rc=0
--check-coverage s*.json        등록부 scenario 266 (executable 255 · declared 11)
                                조각 12개에서 관측 266
                                조각 합집합이 등록부 전체를 정확히 덮었다
```

**전수 재생을 세 번 돌렸다.** ① `6c54429` 4조각 빨강 — 증인 문구에 journal
이름·token repr·PID 로그가 들어가 조각마다 달라졌고(증인은 접두 대조), ε′ 의
schema·교차 층이 옛 축 2개의 실패 이유를 바꿨고, 61차 최소 dict fixture 가 부모
대조 층에 먼저 거부돼 `incomplete_receipt_is_refused-g61` 이 안 물었다.
② `dbfbbf8` 1조각 빨강 — 8 프로세스 경쟁의 동시 보유자 수가 변이 아래서 7/8 로
흔들렸다. ③ `1b4a837` 12/12. 그리고 EXPECT 관측 자체가 셋을 잡았다 (§3).

### 2.4 cohort 세대 전환 (g16 → g17) · `d145790`

```
g16_2026_09_09  active → frozen  (journal seq 15)
g17_2026_09_14  새 active · docs/22p_gap/proj_g17

pin  compute            fa5b9324c01ab7f0 → 14ff767d5fbd0d9d
     row_projection     0e22767966646d49 → f85fc2b39e15d3d0
     producer_semantic  2e2ddce417ecf0db → 814278bfcb82fa2f
     src_scoring        69e69cb046f4b4ae (변동 없음)
     analysis_spec      43d74dd385b1f66d… (변동 없음)
영수증 core_sha256       d6ae274f6e06d95a9028cebd6a7551f2d23e5fb74367576c57afab22b178ca7d
validator                fd7c90edbc56ff1f (검사 34건)
행 바이트                 ad598fe77e75afec — **열세 세대째 같다**
```

대상 커밋: `d1457901d35a18747d8ab7cb085251135871e2ad`
— 위 `core_sha256` 은 이 커밋의
`docs/22p_gap/receipts/paired_fixed5_v4.validate.yaml` 을 가리킨다 (세대를 넘긴
커밋이고, 판정 대상 `0dcbc17` 까지 영수증은 안 바뀌었다). 요청문이 인용한 값은
**그것이 이름한 커밋**에 대고 대조하는 것이 자기완결의 뜻이다. *(63차 마감에 추가 —
62차 판은 이 줄이 빠져 `test_committed_gate_requests_are_self_contained` 가 63차
세대 전환 뒤 빨개졌다.)*

원자료는 이 컨테이너에 없어 `tools.archive_bundle restore artifacts/paired_fixed5_v4`
로 복원한 뒤 돌렸다 (bundle `check` 가 member 를 재해시하므로 바이트는 같다).
`row_projection.py paired_fixed5_v4 --cohort g17_2026_09_14` → 6138행 · restart
30690행 · 전체 True · by_obj True · fits삼중 True · 봉인일치 True.

pin 을 움직인 것은 δ′ + 자체 리뷰 sig 렌즈 셋이다 — 전부 producer analyzer 의
scope 규칙이다. `src_scoring` 과 analysis spec 이 그대로이고 행 바이트가 안
움직인 것이 "이번 라운드는 증거·경계층만 건드렸고 계산식은 안 건드렸다" 를
실물로 말한다.

---

## §3 자체 리뷰 (`/self-review`, 렌즈 4) — 외부 리뷰 전에 우리가 먼저 잡은 것

전부 `docs/GATE62_WORKING_STATE.md` "자체 리뷰" 절에 실측과 함께. 요약:

| 렌즈 | 결론이_바뀜 | 서술만_바뀜 | 코드로 닫음 |
|---|---|---|---|
| 승격 vs 전이 | 0 | 2 | docstring 범위 · 신고 ②③④⑤ |
| 순서-TOCTOU | 0 | 2 (+사소 1) | F1 lock 앞 폐기 · F2 승격 중 lock |
| sig-완전성 | **3** | 0 (+사소 2) | F1 자기 이름 공간 · F2 import 형태 · F3 class/module 결속 |
| 영수증 위조 | 0 | 4 (+사소 2) | F1 부모 대조 · F2 vanished module · F3 dist-info · F4 stem · F5 schema |

sig-완전성의 셋은 전부 δ′ 의 scope 축에서 났다 — 판정을 닫은 코드가 판정과
같은 형태의 구멍을 옆에 남기는 것을 외부 리뷰 전에 봤다. 셋 다 "digest 같고
출력 다름" 을 실물 module 로 재현했다.

---

## §4 외부 검증 — pyDMA (서브 브랜치 `bms-balancing/`, 경고와 함께)

이 저장소의 결론("LLI 는 좁고 LAM 분할은 축퇴한다")을 **합성 진실이 아니라
외부 공개 도구의 검증 데이터**에 걸어 본 결과가 서브 브랜치에 있다
(`bms-balancing/reviews/BML_R1_RESPONSE.md` §12, merge `cf9bad4`). 판정 대상이
아니고 이 요청문의 코드와 무관하다 — 방향의 근거로만 싣는다.

| 사이클 | 축 | pyDMA non-blend | pyDMA blend | 우리 포팅 | 폭 (%p) |
|---|---|---:|---:|---:|---:|
| CU2 | LLI | 3.04 | 3.18 | 3.00 | 0.18 |
| CU2 | LAM_PE | 0.94 | 1.55 | 1.98 | 1.04 |
| CU2 | LAM_NE | −0.58 | 0.27 | −1.26 | 1.53 (부호 갈림) |
| CU3 | LLI | 5.38 | 5.32 | 5.29 | 0.09 |
| CU3 | LAM_PE | 1.43 | 1.28 | 2.73 | 1.45 |
| CU3 | LAM_NE | 0.64 | 0.72 | 0.27 | 0.45 |

LLI 는 세 구현이 0.09–0.18 %p 안에서 붙고, LAM 두 축은 1.0–1.5 %p 로 흩어지며
CU2 의 음극은 부호까지 갈린다 — pyDMA 자신의 두 방법 사이에서도 갈린다. γ
초기값·하한을 Track C 와 맞춘 결정 실험(§12-5)에서 CU2 의 네 값이 표시 자리까지
같았으므로 차이는 **설정이 아니라 식별 가능성**이다.

**경고.** 데이터 한 세트 · 사이클 셋 · optimizer 하나(fmincon-sqp ↔ L-BFGS-B) ·
pyDMA 참조값은 `run_validation.m` 머리의 **기록**이지 우리가 pyDMA 를 돌린 것이
아니다 · 산출 CSV 는 사용자 기계에 있고 저장소에 없다 · `fit_gamma_si` 포팅이
Track C 의 γ 0.224 를 재현하지 못한다 (열린 항목, LAM 결론은 안 바꾼다).
연구 수치의 정본은 artifact + `docs/RESULTS*.md` 이고 위 표는 사본이다.

---

## §5 판정 대상이 아닌 것 (혼동 방지)

이 라운드는 **계산식을 안 건드렸다.** `src.scoring` 과 analysis spec 은
그대로다 (세대 전환 표 §2). cross-cohort 비교는 금지다 — 같은 바이트라는 사실은
회귀가 확인하는 것이지 인용의 근거가 아니다. 연구 수치의 정본은 artifact 와
`docs/RESULTS*.md` 이고, 이 문서의 숫자는 **게이트 판정용 좌표**다.
