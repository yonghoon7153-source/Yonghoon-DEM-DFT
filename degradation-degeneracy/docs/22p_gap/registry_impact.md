# 실행 class 등록부 영향 지도 (읽기 전용) — 70차 E6

> **이 문서는 등록부를 바꾸지 않는다.** 무엇이 들어 있고, 무엇이 그것을 읽고 쓰며, 새 본 실행이 어디에
> 무엇을 남기는지를 적는다. 과거 레코드의 정리·복원·class 변경은 **별도 승인 사항**이다 (70차 리뷰 §4 E6:
> "이 조건으로 새 실행의 안전성을 확보하면 과거 등록부 전체 정리·복원·class 변경은 별도 작업으로 남길 수
> 있다"). 아래 수는 `git ls-files docs/22p_gap/_exec_class` 와 각 레코드의 `evidence` 문장을 기계가 센 것이고
> `tests/test_gate70_defensive.py::test_g70_e6_03_*` 가 이 문서의 수와 실물을 대조한다 — 수치의 정본은 실물이다
> (CLAUDE.md 하드룰 4).

## 1. 무엇이 들어 있나 — tracked 최상위 `docs/22p_gap/_exec_class/*.json`

<!-- census:tracked_total=369 -->
<!-- census:legacy=4 -->
<!-- census:rekey=12 -->
<!-- census:fixture=174 -->
<!-- census:leg_L=177 -->
<!-- census:other=2 -->

| 부류 | 건수 | `evidence` 문장 (시작) | 무엇인가 | class |
|---|---:|---|---|---|
| legacy 분류 | 4 | `legacy 분류 (58차 P0-8): 분류 시점 경로 results/<run> 가 … 밖이었다` | 58차 P0-8 이 배선 이전의 실제 산출 4개(`grid_curves_v4`·`grid_fit_v4`·`halfcell_fit_v4`·`paired_fixed5_v4` = `LEGACY_EXEC_CLASS_ROSTER`)를 **한 번** 분류한 것. 2026-09-04. 유일하게 **실제 과학 실행**을 가리키는 레코드 | canonical |
| re-key | 12 | `58차 L2 re-key …` · `59차 M2 re-key …` · `61차 P0-1 re-key …` | 위 4개의 content id 형식이 v1→v2→v3→v4 로 바뀔 때마다 키만 옮긴 것 (4×3). "판단은 새로 하지 않았고 v1 레코드 … 를 옮겼다" 가 본문에 있다 | canonical |
| 시험 fixture | 174 | `` 시험 fixture `_complete_artifact` 가 정본 산출로 합성했다 `` | `tests/test_compare.py::_complete_artifact` 가 `ledger=None` 으로 등록한 것. 58차가 등록부를 만든 직후 전체 회귀 한 번에 93건이 쌓여 커밋됐고(58차 conftest 주석 실측), 그 뒤에도 더 커밋됐다 | canonical |
| 시험 leg `L` | 177 | `산출 완료 시점 등록 · leg=L phase=grid class=canonical` | production `commit_run_outputs()` 가 시험이 발급한 leg `L` 의 권한으로 등록한 것 — 시험(`test_exec_class_*`·`test_issuance_*`·`test_temporal_seal_*` 등)이 기본 원장으로 돈 흔적 | canonical |
| 그 밖 — 한정 실행 `grid_fit_v5` | 2 | `산출 완료 시점 등록 · leg=grid_fit_v5 phase={grid,fit} class=canonical` | 73차 조건부 한정 실행(2026-09-26, Gabia)이 production `commit_run_outputs()` 로 남긴 grid `719afd1a…` · fit `140d500a…`. E6 창 전후 snapshot: 367 → 369, 삭제·변경 0 (`docs/22p_gap/run_windows/grid_fit_v5/gabia/registry_{before,after}.txt`) | canonical · sealed |

~~**요지:** tracked 367 건 중 실제 과학 실행을 가리키는 것은 legacy 4 + 그 re-key 12 = **16** 이고, **351 건은 시험이 남긴 synthetic canonical** 이다.~~
**요지 (2026-09-26 갱신):** tracked 369 건 중 실제 과학 실행을 가리키는 것은 legacy 4 + 그 re-key 12 + 한정 실행 `grid_fit_v5` 2 = **18** 이고, **351 건은 시험이
남긴 synthetic canonical** 이다. 리뷰어 문장 그대로 — "현재 367개 기록의 문구를 읽는 것만으로 '실제 과학 실행의
canonical 367개' 라고 확인할 수는 없다." 이 문서는 그것을 **확인해 주는** 것이지 지우는 것이 아니다.

가리키는 바이트가 저장소에 있는가: `artifacts/{grid_curves_v4,grid_fit_v4,halfcell_fit_v4,paired_fixed5_v4}` 는 tracked 묶음이고
`results/` 는 gitignored 라 checkout 마다 다르다. 351 건의 시험 레코드는 pytest tmp 아래 산출을 가리켰고 그 바이트는 이미 없다
(죽은 무게 — `local_exec_class_root_for_ledger` docstring 이 smoke 에 대해 적은 것과 같은 성질).

`_exec_class/local/` (gitignored) — smoke class 만 산다. checkout 지역 운용 상태. 여기는 세지 않는다.

## 2. 누가 읽고 누가 쓰나

| 경로 | 함수 | 읽기/쓰기 | 언제 |
|---|---|---|---|
| 발급 | `issue_execution_class()` | 읽기(충돌 확인) | grid/fit 이 계산 **전** gate 를 지날 때 |
| 등록 | `commit_run_outputs()` → `_record_execution_class()` → `_record_execution_class_locked()` | **쓰기** (create-if-absent · 내용당 lock · 같은 class 멱등) | 산출이 굳는 순간 (`write_curves_manifest` · fit commit) |
| legacy 분류 | `classify_legacy_run()` | **쓰기** (roster 4 경로만, 한 번) | 사람이 부를 때만 |
| 승격 판정 | `assert_not_smoke_provenance()` → `resolve_execution_class(for_promotion=True)` → `read_execution_class()` → `_read_exec_class_at()` | 읽기 | `archive_bundle bundle` · `make_results` · `archive_results.sh` — 인용 자리로 **나가는** 모든 길 |
| 전이 조회 | `resolve_execution_class()` (기본) | 읽기 | phase 사이 |
| 시험 | 위 전부 (`ledger=None` 이면 기본 원장) | 읽기·쓰기 | **70차 E6 부터 시험 authority 사본으로 격리** (`tests/conftest.py::_isolate_test_authority`) |

읽는 쪽의 규칙 (70차 E5 로 닫힘): 레코드는 modern 5키 / legacy 4키 두 variant 만 authority 다 (`_typed_exec_class_record`).
공유·국소 두 자리를 다 읽고 class 가 갈리면 멈춘다 (59차 M4). 이름이 둘이면 멈춘다 (60차 P1-1).

## 3. 새 본 실행이 남기는 것 (delta 의 형태)

계획된 다리 `<leg>` 를 `run.sh --mode all --out results/<leg>` 로 돌리면:

1. grid 가 굳는 순간 — `_exec_class/<cid_grid>.json` **1 건** (`evidence: 산출 완료 시점 등록 · leg=<leg> phase=grid class=canonical`, `sealed: true`)
2. fit 이 굳는 순간 — 봉인이 다시 만들어지고 identity 가 바뀌므로 `_exec_class/<cid_fit>.json` **1 건** 더 (같은 evidence 형식, `phase=fit`)
3. `_frozen_coords/` — 건드리지 않는다 (동결은 사람이 따로 한다)
4. `_claims/<leg>.claim` · `_attempts/<leg>.token` — 실행 중에만 있고 finalize 가 지운다

즉 정상 완주의 delta 는 **등록부 +2 (둘 다 canonical · sealed)** 이고 그 밖은 0 이다. 그 이상이 생기면 다른 writer 가 겹쳤다는 뜻이다.

## 4. 격리 / 배타 운영 창 (리뷰어 E6 의 두 대안을 둘 다 쓴다)

**(a) 시험의 권한 쓰기를 격리한다 — 코드 (70차):** `tests/conftest.py` 가 세션 시작에 `LEG_PRESERVATION.yaml` 의 바이트 복사본을
tempdir 에 세우고 `tools.preserve.DEFAULT_LEDGER` 를 거기로 돌린다. 기본 인자로 가는 모든 파생 root(`_exec_class`·`_frozen_coords`·
`_claims`·`_attempts`)가 그 옆으로 간다. 세션 끝에 운영 최상위 `_exec_class/*.json`·`_frozen_coords/*.json` 의 **이름과 sha 가 시작과
같은지 확인**하고, 다르면 지우지 않고 빨갛게 이름을 적는다 (`_the_real_authority_is_untouched`). 58차의 "새 JSON 을 전부 지운다" 는 없어졌다.
한계: 시험이 띄우는 자식 프로세스는 운영 authority 를 본다 — 그것들은 smoke namespace 안에서 돌아 `_exec_class/local/` 에만 쓴다. 불변 검사가 그것을 세션마다 확인한다.

**(b) 본 실행의 배타 운영 창 — 절차 (E9 명세에 그대로 들어간다):**

| 단계 | 무엇 | 증거 |
|---|---|---|
| 창 열기 | 전용 checkout(실행 전용 clone, 시험·wiki 작업 없음) · 실행 시작 HEAD 고정 · **실행 중 pytest·smoke·commit 금지** · 다른 `run.sh` 없음 | `git rev-parse HEAD` · `ps` 스냅샷 |
| 시작 snapshot | `_exec_class/*.json` 이름+sha 목록 · `_frozen_coords/*.json` 목록 · 원장 sha | `registry_before.txt` |
| 실행 | `run.sh --mode all …` 하나 | 로그 전문 |
| 종료 snapshot | 같은 목록 | `registry_after.txt` |
| delta | 새 이름 정확히 2 (grid·fit content id) · 둘 다 `execution_class: canonical`·`sealed: true`·`evidence` 에 `leg=<leg>` · 사라짐 0 · 바뀜 0 | `registry_delta.txt` + 두 레코드 바이트 |
| 창 닫기 | archive → 영수증 → `attach_bundle_evidence` → (사람) `claim_roles`·`근거` → 그 다음에야 pytest/smoke 재개 | 커밋 SHA |

smoke/후속 검증의 권한 목적지: strict smoke 는 `results/_smoke/` 안에서 돌아 `_exec_class/local/` 에만 쓴다 — 창을 닫은 **뒤에** 돈다.

## 5. 하지 않는 것

- 351 건의 시험 레코드를 지우거나 class 를 바꾸지 않는다 (별도 승인 사항 — GATE66 "리뷰어가 삭제본을 자동 복원하거나 class 를 바꾸라고 승인하지 않는다" 와 같은 축).
- `LEGACY_EXEC_CLASS_ROSTER` 를 늘리지 않는다 — 새 산출은 gate 가 발행한 권한으로만 등록된다 (59차 M1).
- 이 문서의 수를 손으로 고치지 않는다 — 실물이 바뀌면 `test_g70_e6_03` 이 빨개지고, 그때 **실물을 보고** 고친다.
