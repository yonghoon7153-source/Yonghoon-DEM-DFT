# 62차 게이트 리뷰 작업 상태 (정본)

판정: **NO-GO** (2026-09-10 접수 · 리뷰어 제목은 "61차 적대적 게이트 리뷰 —
묶음 5" 이나 우리 원장 번호로는 **62차**다 — `GATE61_REQUEST.md` 에 대한 답).
검토 head `6ed11a152508388dce8f27fc90d111c32d5ddd3a` · 판정 대상 RUN_SCOPE
`3a08f5894e94ef246f43dfbc04c1df2cbf2e086a` · `source_digest 4227b40871fa0c10`
(리뷰어 실측 일치). 새 **P0 8 · P1 6 · P2 2 = 16건**.

리뷰어가 새 발견으로 세지 않은 것: 요청문 §0 의 미착수·신고 항목(공유
등록부 오염 · grid 콘솔 요약). 61차 전용 4파일 24 passed · `--check-preimages`
rc 0 · wiki lint 0 errors. 전체 회귀·smoke 는 리뷰어 환경 결손으로 미완주.

## 판정의 세 문장

1. temporal seal 이 "등록된 실행의 고정 identity" 가 아니라 **현재 디렉터리에
   우연히 남은, 과거에 등록된 prefix** 로 되돌아간다.
2. run lock 은 발급이 원자적이지 않고, 정상 fit/grid 는 **봉인·class 등록 전에**
   lock 을 놓는다.
3. producer scope 모델이 아직 Python 과 다르다 — class→method · definition
   head · crossed scoring module 셋 다 **digest 같고 계산은 1→9**.

## 발견 원장

| ID | 무엇이 틀렸나 | 자리 (판정 시점) | 묶음 | 상태 |
|---|---|---|---|---|
| P0-1 | stale/subset seal 이 과거 canonical prefix 로 fallback → 진행 중 fit · fit member 삭제 상태가 canonical 로 승격 | `tools/preserve.py:4433-4456` · `:4637-4643` · `:5484-5488` | α′ | 코드 ✔ |
| P0-2 | run lock 이 `exists()` → `write_text()` (check-then-overwrite) → 두 contender 동시 성공 | `src/io.py:500-514` | β′ | 코드 ✔ |
| P0-3 | fit/grid 가 **봉인·commit 전에** lock 을 놓아 첫 실행이 둘째 bytes 를 봉인 | `src/fitting.py:1026-1050` · `src/grid.py:753-801` | β′ | 코드 ✔ |
| P0-4 | grid 의 durable `manifest.yaml` 이 `curves_parquet=/proc/self/fd/N/…` 을 적고 fit 이 그것을 `manifest_grid.yaml` 로 봉인 (identity member) | `src/grid.py:587-591,756-770` · `src/io.py:593-599` | γ′ | 코드 ✔ |
| P0-5 | random `fit-stage-*` 경로가 run_spec 에 들어가 run_sig 가 매번 바뀜 → 정상 resume 무효 | `src/fitting.py:705,757,1031,1465,1491-1495` | γ′ | 코드 ✔ |
| P0-6 | class local 을 method 에, parameter 를 definition head(default) 에 적용 | `row_projection.py:1489-1509,1718-1724` | δ′ | 코드 ✔ |
| P0-7 | crossed scoring module 을 primary 의 symbol table 로 분석 | `row_projection.py:1939-1998` | δ′ | 코드 ✔ |
| P0-8 | direct `archive_bundle bundle` 이 derived freshness 를 우회 (검사가 shell wrapper 에만) | `tools/archive_bundle.py:531-545` · `scripts/archive_results.sh:124-138` | ζ′ | 코드 ✔ |
| P1-1 | own lock 의 malformed/unreadable 을 release 가 조용히 삼킴 | `src/io.py:532-540` | β′ | 코드 ✔ |
| P1-2 | grid dry-run · pre-commit 실패가 capability/fd 를 폐기 안 함 (`discard` 호출자 0) | `src/grid.py:579,630-661` · `src/fitting.py:1002-1049` | β′ | 코드 ✔ |
| P1-3 | startup code 가 stdout 마지막 줄로 영수증 위조 (`sitecustomize` atexit) | `mutation_replay.py:4639-4645` | ε′ | 코드 ✔ |
| P1-4 | zip/read 실패가 `measured` 로 세탁 (`<unreadable>` · zipimport→unfiled) | `mutation_replay.py:4405-4413,4493-4508` | ε′ | 코드 ✔ |
| P1-5 | package receipt 가 duplicate distribution 을 뒤 root 로 덮음 (Python 은 앞) | `mutation_replay.py:4582-4591` | ε′ | 코드 ✔ |
| P1-6 | 한 receipt 를 여러 번 측정 (marker/selection · body/digest 분리) | `mutation_replay.py:1933-1939,4918-4923,5053-5054,5274-5275` | ε′ | 코드 ✔ |
| P2-1 | completeness validator 가 `status` discriminator 만 검사 | `mutation_replay.py:4753-4771` | ε′ | 코드 ✔ |
| P2-2 | 계약이 없는 `_canon_*` 인용 · `_ast_normal_node` docstring 이 `ast.unparse` 라 적음 | `STAGE3_CONTRACT.md:1077` · `row_projection.py:443-454` | η′ | 코드 ✔ |

## 묶음과 순서

| 순서 | 묶음 | 축 | 발견 |
|---|---|---|---|
| 1 | β′ | **잠금** — 원자 발급 · 소유 token · 임계구역을 commit 까지 · 비-commit 종료의 capability 폐기 | P0-2 · P1-1 · P0-3 · P1-2 |
| 2 | γ′ | **논리 경로·서명** — durable locator 에 staged 경로 금지 · run_sig 에서 random pathname 제거 | P0-4 · P0-5 |
| 3 | α′ | **승격 판정과 transition 조회의 분리** — stale/subset seal 은 승격에서 거부 | P0-1 |
| 4 | ζ′ | **공통 승격 primitive** 에 derived freshness | P0-8 |
| 5 | δ′ | producer scope 를 Python lexical/definition-time 과 per-module 로 | P0-6 · P0-7 |
| 6 | ε′ | 증거 영수증 — framed single snapshot · loader 종류 · precedence · 재귀 schema | P1-3~P1-6 · P2-1 |
| 7 | η′ | 계약 문구 + identifier citation lint | P2-2 |

β′ 가 먼저인 이유: P0-3 의 "임계구역을 commit 까지" 는 61차 P1-1 의 정정
(commit 을 lock 해제 **뒤로** 옮긴 것)과 정면으로 부딪친다. 61차가 그렇게 한
이유는 lock 이 `staged_root(cap)=/proc/self/fd/N` 아래 있어 commit 이 fd 를
닫으면 release 가 죽었기 때문이다. 그러므로 lock 을 **경로가 아니라 dirfd +
inode/nonce token** 으로 들고 가면 commit 뒤에도 놓을 수 있고, 그래야 P0-3
순서(compute → merge → manifest → seal → class → receipt → release)가 성립한다.

## 이번 라운드 규율 (61차에서 이어받음 + 62차 판정문이 준 것)

- RED 먼저. 리뷰어 반례(이번엔 스크립트를 못 받았다 — 관측 표만 있다)를
  **관측 표 그대로** 회귀로 고정한다.
- **production 순서 전체**를 돈다. 61차 P0-1 이 두 라운드 연속 같은 축에서 난
  이유가 조각 시험이다 (서브 브랜치 `HANDOFF_TO_GATE.md` §2d-3 도 같은 진단).
- 방어를 심으면 축을 심고, 넓히면 다른 축이 가려지는지 마감에 센다.
- 서브 브랜치가 R6 F06 에서 세운 잠금 규율(잠금 파일 inode 결속 · `git clean`
  이 지우면 배타가 사라진다)을 β′ 의 참고로 쓴다.

## 62차 요청 전에 할 것 (서브 HANDOFF §2d, 본체 채택)

1. 정상 production 순서 **전체** e2e — grid 굳힘 → fit → commit → report →
   **resume** → report 갱신 → 승격 (이번 P0-1·P0-3·P0-4·P0-5 가 전부 이 순서
   안에서 난다).
2. `/self-review` (렌즈 `순서-TOCTOU` · `sig-완전성`).
3. 요청문에 pyDMA 외부 검증 (`bms-balancing/reviews/BML_R1_RESPONSE.md` §12)
   — 경고와 함께.

## 좌표 (판정 시점 → 지금 head 재확인)

- 잠금: `src/io.py:494 acquire_run_lock` (`exists` 502 · `write_text` 513) ·
  `:518 release_run_lock` (mine 판정 534)
- fit: `src/fitting.py:669 _stage_fit_inputs` (mkdtemp 705) · `:955-1055`
  staged 흐름 (lock 1026 · release 1042 · commit 1050 · receipt 1055) ·
  `:1440 run_spec` · `:1491 run_sig`
- grid: `src/grid.py:587-591` staged 전환 · `:630-661` dry-run 반환(폐기 없음) ·
  `:665 acquire` · `:754 release` · `:769 curves_parquet` · `:774
  write_curves_manifest(named_out…)` · `:837 phase_done out=named_out`
- 봉인: `tools/preserve.py:4394 _sealed_manifest_parts` · `:4592 run_content_id`
  · `:4969 read_execution_class` · `:5259 commit_run_outputs` · `:5333
  discard_execution_capability` · `:5436 assert_not_smoke_provenance`
- 보관: `tools/archive_bundle.py:511 main` (`:533-536` provenance 만) ·
  `scripts/archive_results.sh:127 check_derived_fresh`

## 마감 진행

### β′ — 잠금 (P0-2 · P1-1 · P0-3 · P1-2) ✔ 코드

- RED 관측: `tests/test_run_lock_62.py` 10건 중 9 failed (옛 `exists→write_text`
  구현) → `src/io.py` `RunLock` 으로 교체 후 10 passed.
- `src/io.py`: `acquire_run_lock()` = `O_CREAT` + `flock(LOCK_EX|LOCK_NB)` +
  (dev,ino) 재확인 · `RunLock(dir_fd, name, fd, dev, ino, nonce, pid, where)` ·
  `release_run_lock(token)` = 이름이 아직 내 inode 일 때만 `os.unlink(name,
  dir_fd)`; 사라짐/바뀜 → `RuntimeError`; 경로 인자 → `TypeError`.
- `src/fitting.py` `_run_fit_staged`: `tok = acquire` → `_run_fit_locked` →
  `commit_run_outputs` → `_record_phase` → (except: `discard_capability_on_abort`)
  → finally `release_run_lock(tok)`.
- `src/grid.py` `run_grid`: 같은 구조. lock 구간이 청크 루프 → merge →
  `write_manifest` → `write_curves_manifest`(commit) → `phase_done` 까지. dry-run
  반환도 `discard_capability_on_abort`. 콘솔 요약 `out_dir` 도 `named_out`
  (61차 §0 신고 항목 정리).
- `tools/preserve.py` `discard_capability_on_abort(cap, log=)` 신설 (fit·grid
  공용, 원래 예외를 가리지 않는다). `import logging` 추가.
- 옛 시험 정정: `test_io_bookkeeping.py` 잠금 3건 (실제 flock 보유자 · PID 1 ·
  token release), `test_logical_paths_61.py` 2건 (`os.unlink` patch · "조용히"
  규칙 뒤집음 — 남의 lock 은 안 지우되 올린다).
- `.gitignore`: `.run.lock` `.fit.lock` (R6 F06).
- 실측: β′·γ′·옛 잠금 4파일 + `test_pid_alive…` = **49 passed**.

### γ′ — 논리 locator · run_sig (P0-4 · P0-5) ✔ 코드

- RED 관측: `test_lock_lifetime_62.py` P0-5 2건 — journal 2개
  (`fit_completed_1380c8d85a8f` · `…69d931693a37`), manifest 에
  `/tmp/fit-stage-67o5j9qr/configs/base.yaml`.
- `src/grid.py` `_grid_manifest_payload(named_out, merged, …)` — `curves_parquet`
  = `named_out / merged.name`.
- `src/fitting.py` run_spec `"base_config": _ck(base_config or
  "configs/base.yaml")` (= `base_config_sha` 와 같은 논리 key).
- 시험 정정 (축 심다 실측): grid AST 순서는 `min(release)` 로 (조기 release
  가 finally 에 가려짐) · path-release 는 `TypeError` 만 (넓히면 isinstance
  뺀 변이가 `AttributeError` 로 통과).
- 변이 축: g61 두 개 재조준 (`the-run-lock-is-released-g61` → `release_run_lock(tok)`
  · `lock-release-failure-is-not-swallowed-g61` → `os.unlink(…dir_fd)`) + g62
  10개 신설 (`run-lock-exclusivity-is-a-kernel-op` · `release-consumes-a-token-not-a-path`
  · `release-refuses-a-replaced-inode` · `release-refuses-a-vanished-lock` ·
  `fit-commits-inside-the-lock` · `grid-merges-inside-the-lock` ·
  `fit-failure-discards-the-capability` · `grid-dry-run-discards-the-capability`
  · `grid-manifest-locator-is-the-name` · `run-sig-has-no-staging-pathname`).
  `--check-preimages` rc 0. EXPECT 는 전수 재생 때 `--emit-expect` 로 채운다.
- 부수: `STAGE3_CONTRACT.md` 줄번호 인용 2건 갱신 (1396→1412 · 1351→1367,
  `test_stage3_contract_cites_live_code_facts` 가 잡음).

### α′ — 승격 판정과 transition 조회의 분리 (P0-1) ✔ 코드

- RED 관측 (`tests/test_promotion_seal_62.py`): 진행 중 fit(subset seal) ·
  fit member 삭제(stale seal) · 봉인 파일 삭제 — 셋 다 `DID NOT RAISE`; commit
  레코드에 `sealed` 없음. 4 failed / 3 양성 대조 passed.
- `tools/preserve.py`: `_promotion_content_id(d)` (봉인 낡음 → 거부 · 봉인이
  지금 있는 identity member 를 다 안 담음 → 거부 · 봉인 없음 → 현재 목록,
  단 레코드가 `sealed` 면 거부) · `resolve_execution_class(…, for_promotion=)`
  · `assert_not_smoke_provenance` 가 `for_promotion=True` · 등록 레코드에
  `sealed: bool` (`_record_execution_class` 가 봉인 존재를 본다).
- 전이 조회(`run_content_id` · `issue_execution_class`)는 60·61차 관용 그대로
  (`test_temporal_seal_61.py` 7건 그대로 초록).
- 실측: 14 passed (62 α′ 7 + 61 temporal 7).

### ζ′ — 공통 승격 primitive 에 derived freshness (P0-8) ✔ 코드

- RED 관측 (`tests/test_archive_freshness_62.py`): stale 파생인데 `bundle` 호출
  · `main` 에 `assert_promotable` 없음. 2 failed / 2 passed.
- `tools/preserve.py`: `assert_derived_fresh(run_dir)` (`objective_comparison.yaml`
  없으면 대상 아님 · `verify_derived_freshness` 실패 → PreserveError) ·
  `assert_promotable(paths, sink, dest)` = smoke 판정 + freshness.
  `tools/archive_bundle.py main` 이 그것을 지난다. `scripts/archive_results.sh`
  의 검사는 남긴다 (사람용 진단; 경계는 primitive).
- 실측: 4 passed.

### δ′ — producer scope 를 Python 규칙과 per-module 로 (P0-6 · P0-7) ✔ 코드

- RED 관측 (`tests/test_scope_model_62.py`): method 의 load 에 class 본문
  `for getattr` 결속 · default/decorator/annotation/lambda default 에 매개변수
  결속 · scoring 의 `GET = getattr` 별칭·자기 이름 공간 별칭이 통과 (11 failed).
  두 e2e 시험은 첫 판이 **다른 층**(58차 L9-b 별칭 고정점 · 60차 P0-10 매개변수
  호출 거부)에서 걸려 shape 을 바꿨다: `[getattr][0]` 로 감싸고, head 안에서
  직접 이름 공간을 연다 — 리뷰어의 "digest 같고 1→9" 형태.
- `row_projection.py`: `_definition_head(node)` (default · kw_default ·
  annotation · returns · decorator · class bases/keywords) 는 `inherited` 로,
  본문은 `here` 로; 자식 scope 가 물려받는 집합 `nested` = class 면 `inherited`
  (comprehension 은 첫 iterable 만 class 본문). `_walk_nodes(nodes, here,
  nested)` 가 본체 (첫 판은 body 문장 자신이 scope 인 경우를 놓쳤다 — RED 로
  잡음). `_producer_closure` 가 `tables = {"rp": …, "sc": …}` 를 module 별로
  만들어 `_assert_no_dynamic_resolution(node, key, *tables[kind])`.
- 실측: 22 passed (62 δ′·η′ 17 + 61 scope 5) · docs_lint producer 55 passed.

### ε′ — 증거 영수증 (P1-3 · P1-4 · P1-5 · P1-6 · P2-1) ✔ 코드

- RED 관측 (`tests/test_evidence_receipt_62.py`): 리뷰어 조건 그대로 —
  packages `2.0`(뒤 root) · zip module 이 unfiled · `"<unreadable>"` 이 pth
  digest 자리에 · `_write_coverage` 가 `_execution_receipt` + `_digest` 를 따로
  호출 · 최소 dict 가 reader 통과. 19 failed.
- `mutation_replay.py`:
  · P1-3 `_FRAME_PREFIX` + `_FRAMED_PARSER_SRC`(한 문자열, 부모는 `exec`, 증언
    node 는 파일에 박음) · `_run_probe()` 가 frame 으로 받고 앞뒤에 무엇이든
    있으면 `_ReplayError`. **한계**: `sys.stdout` 자체를 바꿔 치우는 startup
    코드는 못 막는다 (요청문에 적는다).
  · P1-4 `_Unreadable` 예외 → `startup`·`inputs` 섹션이 `failed`;
    `_hash_origin(p, loader)` 가 zip origin 을 `loader.get_data` 로 잰다;
    `find_spec` 실패는 `failed`, builtin/frozen/namespace 만 `unfiled`.
  · P1-5 `sys.path` 순서로 `distributions(path=[entry])` — 첫 것이 `dists`,
    나머지는 `shadowed: [[name, pos, ver]]`, `positions`.
  · P1-6 `ReceiptSnapshot(json_body, digest, tag)` · `take_receipt_snapshot()`
    — `_replay` 가 한 번 재서 `_write_marker(…, tag)` · `_write_coverage(…,
    snapshot=)` · `_assert_execution_is_current` 도 한 스냅샷.
  · P2-1 `_RECEIPT_SCHEMA` 재귀 exact (키 집합 · int/str · hex16 · 고정 길이
    list) · `_assert_receipt_is_complete` = status 층 + schema 층.
- fixture: `tests/receipt_fixture.py::full_receipt()` — 61차 최소 dict 가
  schema 에서 깨졌다 (규율 2 대로). `test_evidence_receipt_61.py` 1건 정정.
- 실측: 42 passed (62 ε′ 22 + 61 receipt 12 + 60 import closure 8).

### η′ — 계약 문구 · 인용 lint (P2-2) ✔ 코드

- `STAGE3_CONTRACT.md:1077` `_canon_*` → `_keep_docstrings()` →
  `_ast_normal_node()` → `_ast_canon()`. `_ast_normal_node` docstring 의 "unparse
  로 찍는다" 정정. `tests/test_contract_citations_62.py` — `row_projection.py`
  와 같은 줄의 백틱 `_이름` 은 전부 실제 module-level 정의여야 하고 `*` 는
  인용이 아니다.

### 변이 축 (62차 전체)

g61 재조준 3 (`the-run-lock-is-released` · `lock-release-failure-is-not-swallowed`
· `closure-refuses-dynamic-resolution` · `comprehensions-are-their-own-scope`
site 1) + g62 신설 **22**: β′γ′ 10 · α′ 3 · ζ′ 1 (`ARCHIVE` 상수 신설) · δ′ 3 ·
ε′ 6. `--check-preimages` rc 0 (자기 참조 5건은 `\uXXXX` 로 escape —
도구가 JSON escape 를 먼저 풀어 두 번 실패, `chr(92)` 로 씀).

### 남은 것 (순서대로)

sealed-record scan + fit resume 단계 (smoke_e2e.sh) → 전체 회귀 결과 처리 →
커밋 → strict smoke → EXPECT(`--emit-expect`)/12조각/영수증/g17 → `/self-review`
→ 요청문 (pyDMA 증거 포함) → push.

## 자체 리뷰 (`/self-review`, 렌즈 4 — 커밋 `449fcc7` 의 diff)

### 렌즈 승격 vs 전이 — 결론이_바뀜 0 · 서술만_바뀜 2 · §0 신고 후보 2

| # | 공격 (실측) | 판정 |
|---|---|---|
| 1 | fit member 삭제 + grid 시점 봉인 복원 → grid 의 canonical id 로 승격 | 정당한 grid 상태 (원장에 `phase=grid` 로 등록된 바이트 그대로). 봉인엔 서명이 없으므로 이 층이 막는 것은 **미등록 상태**뿐 — `_promotion_content_id` docstring 에 범위를 적었다 |
| 2 | manifest(+seal)만 복사하고 `fits.parquet` 을 바꿈 → identity 층은 통과 | `archive_bundle.bundle()` 의 `_seal_conflicts` (`manifest.fits_seal.file_sha256` ↔ 실물) 가 거부. **F68 이전** manifest(`fits_seal` 없음)는 direct bundle 창이 남는다 → §0 신고 |
| 3 | sink 열거: `make_results.py:1703` 보고서 sink 는 `assert_not_smoke_provenance` 직접 (for_promotion 은 내부에서 지남) · derived freshness 는 배너 정책(F77) | 요청문에 "보고서 sink 는 배너, archive 는 거부" 를 명시 |
| 3b | nested `wsweep/` 은 등록 자체가 없다 (`weight_sweep.py` 가 issue/commit 을 안 부름) → 부모 승격이 nested 를 판정 안 함 | §0 신고 후보 |
| 4 | 봉인 형식 edge (non-JSON · 빈 목록 · 파생 이름 · 중복 항목 · 두 번 읽는 사이 삭제) | 전부 fail-closed |
| 5 | 가용성: grid commit → fit 시작만(거부 ✔) → fit commit + 파생 + nested + attempts → resume 중(거부 ✔) → resume commit + report 갱신 → 승격 | 살아 있음 |

### 렌즈 순서-TOCTOU — 결론이_바뀜 0 · 서술만_바뀜 2 (둘 다 코드로 닫음) · 사소 1

| # | 실측 | 고침 |
|---|---|---|
| F1 | capability 는 lock **앞에서** 발행된다. lock 이 살아 있는 보유자에게 거부되거나 발행↔lock 사이(입력 승인 · 완방상태 · dry-run 표본 solve)에서 죽으면 `discard` 를 못 지나 `live_caps 0→1 · open_dir_fds 0→1` — 리뷰어의 P1-2 계측이 둘째 contender 로 그대로 재현 | fit·grid 모두 `tok = None; try:` 를 **발행 직후**에 열고 `finally` 는 `tok is not None` 일 때만 release. 회귀 5건 (`test_lock_lifetime_62.py` 뒤쪽: fit 보유자 거부 · fit lock 앞 예외 · grid lock 앞 예외 ×2(dry-run 포함) · grid 보유자 거부) — RED 관측 뒤 GREEN |
| F2 | `assert_promotable` 은 검사 **시점** 문장이고 `bundle()` 은 그 뒤 바이트를 복사 — 사이에 fit 이 같은 자리에서 시작하면 묶음이 진행 중 상태를 담는다 (lock 없음 실측) | `archive_bundle.main` 이 `.fit.lock`·`.run.lock` 을 token 으로 잡고 검사+복사를 끝낸 뒤 놓는다 (살아 있는 실행이 있으면 거부). 회귀 `test_direct_bundle_holds_the_run_locks_while_copying` |
| F3 | `_run_fit_locked` docstring 이 61차 순서를 말함 | 정정 |
| 미재현 | 12 프로세스 × 150회 acquire/hold/release peak 1 · `/proc/self/fd/N` 위 lock 은 dir_fd 가 **새 fd** 라 N 이 닫히고 rename 돼도 맞는 파일을 지움 · commit 뒤 receipt 예외·commit 부분 실패 → discard 가 옳고 같은 프로세스 재시도 OK · `_promotion_content_id` 두 읽기 사이 재봉인은 양성 | — |

### 렌즈 sig-완전성 — **결론이_바뀜 3** (전부 코드로 닫음) · 사소 2

| # | 실측 (digest 같고 출력 다름) | 고침 |
|---|---|---|
| F1 | 건너간 scoring 이 `import src.scoring as me` + `me.external(...)` 로 **자기** 이름 공간을 열면 닫힘이 안 따라감 — P0-7 은 table 만 module 별로 줬고 walk 는 primary 의 `mods` 만 봤다 | Attribute 분기가 `tables[kind][0]` 을 본다. 회귀 `test_the_crossed_module_own_namespace_access_enters_the_closure` |
| F2 | `from src import scoring as me` · `import src as S; S.scoring` 두 import 형태가 `_crossed_modules` 밖 → `getattr(me, "x")` 가 "이름 공간이 아님이 증명됐다" | `ImportFrom` 도 수집, 부모 package import 는 fail-closed 거부. 회귀 2+1 |
| F3 | class 본문·module 문장의 `for`/`with as`/`except as` 결속을 scope 전체 shadow 로 봤다 — `LOAD_NAME` 은 위치 의존 (결속 앞 load · `del` 뒤 · unbind). `if True: with nullcontext(…) as getattr: EXT = getattr` 한 문장이 MODULE_EFFECTS 의 한 node 라 통째 면제 | `_own_shadows` 는 함수·lambda 에만 결속 shadow 를 준다 (fail-closed). δ′ 첫 판의 시험 2건이 반대를 고정하고 있었다 → 뒤집음 |
| F4 | P0-6 over-refusal: class 본문 안 method 의 default 가 class-local 을 못 봄 | F3 로 class 본문에 shadow 가 없어져 소멸 (실제 closure 통과 확인) |
| F5 | (diff 밖) `_stage_fit_inputs` 가 저장소 밖 절대 경로 입력을 staging 못 함 (`SameFileError`) | §0 신고 후보 — 이번엔 안 고침 |

### 렌즈 영수증 위조 — 서술만_바뀜 4 (코드로 닫음) · 사소 2

| # | 실측 | 고침 |
|---|---|---|
| F1 | frame 의 한계는 "`sys.stdout` 교체" 보다 넓다 — fd 층(`dup2`) · `builtins.print` 교체도 ACCEPTED, child 는 `sys.orig_argv` 로 frame 을 안다. 주석의 "customization 에 남는다" 는 거짓 (부모가 그 필드를 아무것과도 대조 안 함) | 주석 정정 + 둘째 층 `_parent_customization_view()`/`_assert_customization_matches_parent()` — 부모가 자기 프로세스에서 site/sitecustomize/usercustomize 를 같은 검색 순서로 찾아 해시, child 의 `<absent>` 세탁을 거부. fixture 도 부모 시야를 쓴다 |
| F2 | `find_spec → None` 을 `unfiled` 로 셈 → 올렸다 **지운** module 이 영수증 밖. 기본 환경의 None 둘은 importtime **헤더 줄** `imported package` 와 실패한 `usercustomize` 시도 | 헤더 줄 파싱 제거(자료 줄만), None 은 `<absent>` 인 customize 만 unfiled, 나머지 `failed` |
| F3 | PYTHONPATH 의 `*.dist-info/entry_points.txt` 가 영수증 밖 — digest 같고 pytest plugin 로드 다름 | `importable_roots` 가 dist-info/egg-info 아래 파일 전부를 담는다 |
| F4 | Name 없는 dist 는 건너뜀 (Python 은 stem 으로 찾음) | stem 키 |
| F5 | schema 가 전부 빈 영수증·교차 필드 불일치를 받음 | customization 키 고정 · 빈 startup_modules/env 거부 · `startup.env==env` · `startup.version==interpreter` · 음수 거부 |
| 사소 | `_observed_environment` 죽은 코드 | 삭제 |

변이 축: 재조준 4 (`dry-run-releases-the-claim` · `grid-dry-run-discards-the-capability-g62` · `promotion-checks-derived-freshness-g62` · `closure-follows-module-aliases` site 0) + 신설 11 (`capability-discarded-before-the-lock` · `grid-discards-before-the-lock` · `promotion-holds-the-run-locks` · `class-body-bindings-are-not-shadows` · `from-imports-are-namespace-targets` · `parent-package-import-is-refused` · `crossed-module-self-alias-is-followed` · `history-refuses-a-vanished-module` · `dist-info-bytes-are-in-the-receipt` · `parent-cross-checks-customization` · `schema-refuses-empty-receipts`). `--check-preimages` rc 0.
