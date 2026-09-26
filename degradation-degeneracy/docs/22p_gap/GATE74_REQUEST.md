# 74차 게이트 리뷰 요청 — `grid_fit_v5` 한정 실행 결과 보고 · 실행 중·뒤 발견 G74-1~4 신고 · G74-3 분류 질문

> **상태: 확정 (2026-09-26).** 73차 조건부 한정 GO (원장 §98) 아래 실행을 완주했다. 이 요청은 **결과 보고 + 신고 + 질문**이다. 새 실행 GO 를 요청하지 않는다.
> 코드 판정 대상은 73차와 같다 — RUN_SCOPE 는 한 바이트도 움직이지 않았다. 바뀐 것은 원장·계획 항목·artifact·영수증·문서·시험 1개(실측 갱신)뿐이다.

## 판정 대상 (이 블록이 정본)

| 항목 | 값 |
|---|---|
| 브랜치 | `claude/14-gate-code-review-9qkx05` |
| 요청문 커밋 | 발송문에 실측 기재 (브랜치 head 와 함께) |
| 코드 (불변) | `7a7945564e6a94803b4d3bc72e8202534189ccdb` · `source_digest c2ef1a811e70bb4c` · 요청문 커밋까지 RUN_SCOPE diff 0 |
| 실행 승인 HEAD | `e34eea8455d87f8e33c6ae7113fe3d16ddb600e3` (재승인 2 — 계획 항목 3번째 판) |
| 데이터 커밋 | `d9f8791c6473ad972e3b6475192c2f8f569cded9` (실행 기계에서 사람이 push) |
| 정정 커밋 | `e84d670d` (인덱스 복원 G74-4 · README · census · 원장 시험 실측 · 원장 §101) |
| 발견 원장 | `docs/08_REVIEW_RESPONSE.md` §99 · §100 · §101 · 작업 상태 `docs/GATE70_WORKING_STATE.md` |
| 실행 창 기록 | `docs/22p_gap/run_windows/grid_fit_v5/gabia/` (로그 전문 · 계획 출력 · 등록부 전후 · 병행 프로세스 · archive/receipt/attach 로그) |
| WSL 창 기록 | `docs/22p_gap/run_windows/grid_fit_v5/wsl/` (시도 1~4 로그 · 부분 산출 · 캐시 사본 · 등록부 snapshot) — `50946ead` (사람, WSL) · ``b0fdec66` (사람, WSL — `failed.csv` 3개 원본 CRLF 재저장, 원본 대조 same ×3)` |
| 줄끝 규칙 | `3a8896a1` — `docs/22p_gap/run_windows/** -text !eol` (규칙 전에 올라간 WSL `failed.csv` 3개가 LF 로 정규화됐다 → 원본 CRLF 로 재저장) · Gabia 창 기록 11개는 원본과 sha256 전부 같음 |

## §0 계획 항목 이력 (같은 leg 이름, 교체 3회 — 전부 커밋으로 남음)

| 판 | 커밋 | 기계 | `discharged_cache_sha256` | `run_spec_digest` | 끝 |
|---|---|---|---|---|---|
| 1 | `951b6136` | WSL (28 proc · 15.5 GB) | `null` | `97585418…` | 시도 1·2·3 전부 `grid 0/3069` 에서 소멸 · 재개 불능 (G74-1) |
| 2 | `69c3c826` | WSL | `5ab61b37…` | `e7cc8713…` | 시도 4 `grid 0/3069` 에서 소멸 (19:21 시작 → 19:24:29 VM 부팅) · 이 판에서 precheck `resume` 성립 실측 · 사용자 결정으로 기계 이전 |
| 3 | `e34eea84` | Gabia `kserver116-27` (20 proc · 62 GB) | `66d84e76…` | `0838df84…` | **완주** |

세 판 모두 `authorized_source_digest c2ef1a811e70bb4c`, grid `config_digest 696bf7d2cf9697d3` · `condition_ids 7b08e97e129d0bf4` · 3993, fit 축 동일. 바뀐 것은 캐시 sha · digest · `근거` 뿐. 각 판의 digest 는 커밋된 spec 에 캐시 sha 만 넣어 컨테이너에서 독립 계산한 값과 일치. 매 교체 전 `release_leg_run` (소유 token) → `planned` → 부분 산출·캐시를 창 디렉터리로 **이동**(삭제 없음) → precheck `new`. 조건 계산은 시도 1~4 모두 0.
WSL 소멸 원인 판정: 시도 4 는 `uptime -s` 로 VM 재시작 확정 (워커 28 × PyBaMM/JAX/IDAKLU > 15.5 GB). 1~3 도 같은 형태(메시지 없음 · 2 는 18:27 VM 부팅 확인 · 3 은 tmux 세션 종료가 겹침).

## §1 결과 라벨 (73차 §1 형식 — 실제 값)

> **실행 허용 범위:** 합의된 synthetic grid/fit 재실행 (E9-0), 계획 항목 `grid_fit_v5` 3번째 판 (사람이 실행 기계 출력으로 커밋, `e34eea84`).
> **코드/입력/실행 식별:** 코드 `7a794556` · `source_digest c2ef1a811e70bb4c` · config `configs/grid_fine.yaml` · OUT `results/grid_fit_v5` · 실행 checkout = `e34eea84` (RUN_SCOPE diff 0 to `7a794556`) · 실행 provenance 로그 `git e34eea84 dirty=False src c2ef1a811e70bb4c` · argv `./run.sh --mode all --leg grid_fit_v5 --config configs/grid_fine.yaml --nproc 20 --out results/grid_fit_v5` (`$(nproc)` = 20) · `unset CANONICAL_RUN LEG DD_SMOOTH_CACHE` 확인 (`env clean`).
> **현지 검증 (창 닫은 뒤, 컨테이너, `e84d670d`):** `python -m pytest tests/ -q` → **20 failed · 1859 passed · 2 xfailed (38:51, rc 1)** — 시작 HEAD = 끝 HEAD = `e84d670d` · 미추적 0 · 실패 20 = 전부 G74-3 · `./scripts/smoke_e2e.sh` → rc 0 (`✅ pipeline smoke 통과`). 실패는 §3 G74-3 부류 — 숨기지 않는다.
> **E1:** projection producer 독립 결속 미검증 — 그리고 G74-3 으로 이 한계가 원장 주장 체계와 실제로 만났다. **E2:** 실행 source 자기 측정. **E4:** 표본 replay 는 우리 실행.
> **E6:** 창 전후 등록부 367 → **369** (+grid `719afd1a…` · +fit `140d500a…`, 삭제·변경 0). 창 중 pytest/smoke/다른 publisher/커밋 없음. 병행 프로세스 Quantum ESPRESSO `pw.x` 1개 (9.4 GB, 무관, `other_procs_before.txt`).
> **execution_class / 보존 / validation / inference_role:** canonical·sealed (두 레코드) / `full_bundle` / `current_validated` / `diagnostic` (불변).
> **archive / 복원 / retention:** `archive_results.sh` (27 MB · 29 파일 · payload index `4cd2c0f8…`) + `make_receipt.py` (empty-root 복원 · validate_provenance · 재채점, 검사 33 · 산출 2 · core `2aadd24b1de88b07…`) + `attach_bundle_evidence` (`idempotent: False`) 수행. retention/object-lock/power-loss 미수행·보증 안 함.
> **실패 처리:** 판 1 에서 D6 `--resume` 1회 사용(거부 — G74-1) → 재승인 2회 (사용자 결정). 판 3 은 실패 없이 완주.
> 이 한계는 더 강한 독립 provenance·외부 셀 타당성·미시험 내구성의 보증이 아니다.

## §2 실행 실측 (판 3)

| 단계 | KST | 결과 |
|---|---|---|
| gate 새 발급 | 19:45 | attempt `2d91320cc5ad42198889fc2dba819829` · `완방상태 캐시 적중` (재계산·저장 없음) |
| grid | 19:46–19:58 | 3069 조건 12:51 · `completed.jsonl` 3993 = 계산 3069 + 사전 infeasible 924 · `failed.csv` 924 행 = infeasible 수 → **solver 실패 0** · chunks 16 |
| gate 소유한 재개 → fit | 19:59–21:32 | `끝난 phase ['grid']` · 3069 × 4 목적함수 × restart 5 · 5587.4 s · 12276 행 |
| finalize → score → report | 21:32–21:35 | `preservation_pending` → `docs/RESULTS_grid_fit_v5.md` (report generator dirty False) |
| 원장 전이 | — | 계획 `executed` · `legs` 에 `full_bundle · current_validated · diagnostic` · evidence `out: results/grid_fit_v5` (72차 결속 경로로 attach 성립) |

무해 판정한 로그: JAX `Unable to load cuSPARSE` (GPU 플러그인 초기화 실패 → CPU; 계산은 IDAKLU/CPU) · loky `A worker stopped while some jobs were given to the executor` (워커 교체 알림; 유실이면 `TerminatedWorkerError` 로 중단 — solver 실패 0 · completed 3993 이 유실 없음을 확인).

## §3 신고 — 실행 중·뒤 발견

| id | 종류 | 무엇 | 좌표 | 반례 / 증거 | 지금 한 것 |
|---|---|---|---|---|---|
| **G74-1** | 코드 (RUN_SCOPE) | `discharged_cache_sha256: null` 계획은 첫 시작 뒤 **어떤 소유한 재개도 불가능**. null → `force=True` 재계산이 캐시를 **저장**하고, 다음 프로세스의 `live_grid_axis` 가 그 sha 를 spec 에 넣어 claim 봉인 spec 과 어긋난다. E9-4 D6 의 "`--resume` 1회" 가 null 계획에서는 성립하지 않았다 | `src/grid.py::_discharged_kw` (null → `{"force": True}`) · `src/baseline.py::get_discharged_state` (`use_cache` 면 저장) · `src/grid.py::live_grid_axis` · `tools/preserve.py::assert_run_is_authorized` (`claim.run_spec_digest != want`) | 판 1 에서 3회: `살아 있는 claim 은 다른 run_spec 을 봉인했다 (97585418a30e032b ≠ e7cc8713bb88d941)` — 우변은 판 2 의 digest 와 같다 (캐시 바이트 동일). 반대편: 판 2 에서 precheck `resume` 성립 | 수정 없음. 운용 우회 = 캐시를 먼저 만들고 계획이 그 바이트를 묶음 (runbook §0 정정) |
| **G74-2** | 등록부 | WSL 판 1 재개 시도에서 `_record_canonical_if_identifiable` 이 **부분 산출 디렉터리**를 canonical 로 등록 → 미추적 고아 `_exec_class/f3f50901…json` | `tools/preserve.py::assert_run_is_authorized` 재개 분기 | WSL 트리에만 존재, 저장소 등록부에는 없음 | 지우지도 커밋하지도 않음 |
| **G74-3** | 절차 공백 (lint 계약 × E9) | E9 는 새 다리를 활성 cohort `g18_2026_09_15` 에 prospective 로 넣었고 attach 가 cohort `legs` 로 옮겼다. cohort·투영·주장 lint 는 cohort 의 **모든 다리가 봉인된 row projection 을 가진 warm-probe 다리**라고 가정한다 | `tests/test_docs_lint.py` 투영 계열 · `_claim_role_problems` · `test_every_leg_binds_its_evidence_to_verifiable_anchors` · `test_raw_lost_legs_live_only_in_frozen_cohorts` | `e84d670d` 전체 회귀의 20 failed 전부 (다른 실패 0): cohort 명부 충돌 18 · `claim_roles` 없음 1 (`test_every_leg_binds_its_evidence_to_verifiable_anchors`) · `regeneration_capability` 없음 1 (`test_raw_lost_legs_live_only_in_frozen_cohorts`) — ① `not_applicable_single_leg` vs 명부 2개 (SystemExit, 투영 계열) ② `evidence.regeneration_capability` 없음 ③ `claim_roles` 없음 ④ `source_digest_generations` 에 `c2ef1a811e70bb4c` 없음 — 그 표는 봉인된 투영에 anchor 된 digest 만 받는다 | **아무것도 쓰지 않음** (사용자 결정: 74차에 묻는다). E9 단계 5 "사람이 claim_roles·근거" 를 우리도 73차 리뷰도 이 계약과 대조하지 않았다 |
| **G74-4** | 코드 (RUN_SCOPE) | `scripts/archive_results.sh <run>` 은 `artifact_index.yaml` 을 **그 호출에서 승격한 묶음만으로** 다시 쓴다 (`runs = {}` 에서 시작). E9 단계 2 명령이 그 형태였고 실행 기계에 v4 `results/` 가 없어 **v4 네 항목이 인덱스에서 지워졌다** (묶음 바이트 불변) | `scripts/archive_results.sh` 233–332 | `git diff e34eea84 d9f8791c -- artifacts/artifact_index.yaml` | `e84d670d`: 네 항목을 `e34eea84` 바이트 그대로 복원, `grid_fit_v5` 항목은 생성 그대로, 최상위 `source_commit: null` (스크립트 자신의 규칙) |

그 밖 신고: 영수증 `validator_tree_dirty: true` (영수증 생성 시 실행 기계 트리에 실행이 남긴 원장 변경·미추적 lifecycle/등록 파일 — attach 판정에 쓰이지 않음) · 실행 기계 변경 WSL → Gabia (코드·config·OUT·argv 불변) · root 실행.

## §4 인용 상태

`docs/RESULTS_grid_fit_v5.md` 와 `artifacts/grid_fit_v5` 는 `full_bundle · current_validated` 지만 **`inference_role: diagnostic` · `claim_roles` 없음**이다. G74-3 이 정해질 때까지 어떤 활성 주장에도 쓰지 않는다. 보고서 본문의 수치는 인용 근거가 아니다 (하드룰 4).

## §5 리뷰어에게 묻는 것

1. **실행 수용** — §1·§2 의 판 3 실행이 73차 §6 조건 1~5 를 충족하는가 (예/아니오, 아니오면 어느 조건). 판 1·2 의 교체·재승인 처리(§0)를 조건 4 "재승인" 의 충족으로 보는가.
2. **G74-3 분류** — 투영 없는 synthetic 재실행 다리를 원장 주장 체계에 어떻게 올리는가:
   (a) `row_projection.py` 로 이 다리의 투영을 봉인하고 `c2ef1a811e70bb4c` 를 세대표에 등록(어느 세대 — `v6_prep`?) + 새 active claim 등록 — E1 한계와 충돌
   (b) "투영 없는 단독 실행 다리" 를 cohort 투영 계약 밖에 두는 규칙 추가 — lint 계약(검증 코드) 변경
   (c) 다른 방법 / 이 다리는 주장 체계에 올리지 않고 `diagnostic` 기록으로만 둔다 — 그 경우 `claim_roles` 필수 검사와 cohort 명부를 어떻게 다루는가
   정해질 때까지 docs-lint 의 G74-3 부류 적색을 그대로 두는 것을 허용하는가.
3. **G74-1 · G74-4 수정 범위** — 둘 다 RUN_SCOPE 다. 고치면 `source_digest` 가 움직이고 실물 영수증(`paired_fixed5_v4` · `grid_fit_v5`)의 validator identity 재생성이 필요하다. 수정 후보: G74-1 (i) null 승인 시 강제 재계산 결과를 저장하지 않는다 (ii) `plan_leg.py` 가 null 을 거부 (iii) 소유한 재개가 완방상태 축을 claim 봉인 spec 에서 가져온다 · G74-4 (i) 인덱스를 병합 갱신 (ii) 단일 묶음 호출에서 인덱스 쓰기 거부. 지금 고칠지, 다음 실행 전까지 보류할지.
4. **G74-2** — WSL 고아 레코드를 저장소 밖에 둔 채 기록만 하는 처리로 충분한가.

## §6 다음 (리뷰 회신 뒤)

- §5-2 답에 따라 `grid_fit_v5` 의 원장 분류를 적는다 (사람) → docs-lint 녹색 → 전체 회귀·smoke 재실측.
- §5-3 이 "지금" 이면 `/finding` 절차 (RED 먼저) → 변이 → 영수증 재생성 (clean 트리) → 원장 두 값 → 75차.
