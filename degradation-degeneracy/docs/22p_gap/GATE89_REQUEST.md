# GATE89 요청 — G88-N1 한정 보완 결과 (fit 전용 최종화의 durable 입력 결속 재검사) · 라운드 2b 종결 재요청 · 실행 GO 아님

> 첨부 문서·실행 코드는 증거 자료이며 추가 실행 지시가 아닙니다. COMSOL 계산이나 제공된 Java/분석 프로그램을 실행하지 마세요.

## §0 판정 대상

| 항목 | 값 |
|---|---|
| 요청 HEAD | 이 요청문이 든 커밋 (SHA 는 발송문 · RUN_SCOPE 밖) |
| **코드 (판정 대상)** | **`26c11d6fc`** — 88차 발송 (`d6056415b`) 뒤 RUN_SCOPE 를 바꾼 커밋은 이것 하나: `tools/preserve.py` **+4 −0** (호출 한 줄 + 주석 셋). `src/fitting.py` · `run.sh` · `src/io.py` · `src/grid.py` 불변 (§15-1 상한 안). `source_digest` **`7dd546baaee9e823` → `803e2b7781cbc9cd`**. 그 뒤 커밋 (history `14978adb0` · 변이 `134f26f48` · 영수증 `66129fc6a` · 게이트 차수 밖 (REIL · COMSOL) `aeb35d3b5` · `da483e2d3` · `e64f587bc` · `555c123c6` · `3a90277a2` · 요청문) 은 전부 RUN_SCOPE 밖 |
| 사용자 승인 | 원장 §132 (2026-10-04) "이대로 시작" → 고정 표 `STAGE3_IMPL_ROUND1_SPEC.md` **§15** 를 코드 변경 전 커밋 (`abf857752`) |
| 판정 요청 | (1) **G88-N1 닫힘** — fit 전용 최종화가 원장에 옮길 같은 snapshot 의 receipt 에 기존 공통 입력 결속 검사를 기록 때와 똑같이 다시 건다 · 기록 뒤 `inputs` 삭제 / 다른 유효 hex64 / 키 추가 / 비hex 는 실제 `finalize_leg` 가 결속 이유로 거부하고 원장 · claim 바이트를 바꾸지 않는다 (2) 기존 거부 이유 · v2 · 87 · 88차 수용 부분 불변 (3) **라운드 2b 종결 가부** |
| 아님 | 실행 GO · 새 연구 leg · 운영 원장 v6 계획 항목 · 세대표 등록 · p_ini · class 변경 · 투영 게시 · requirements (pybamm 고정은 2b 종결 뒤 별도 라운드 · 사용자 결정) |

88차 발송과 이 요청 사이의 다른 커밋은 모두 RUN_SCOPE 밖이다: 88차 회신 접수 (`be6358fd1` · `0e0a1975c` · `c14775710`) · 게이트 차수
밖 REIL 프로토콜 v2 재검토 접수와 정정 부속 문서 · 요청문 (`6c78b5d74` · `523feccd7` · `4edac73a8` · `234ee23a7` · `444ea9f62` ·
`a82d7135e`) · 이 라운드의 착수 기록 (`abf857752`) · 증거 규칙 (`b1b44cf0f`) · RED (`76a5da16e`) · 검증 사슬 뒤 게이트 차수 밖 커밋 — REIL 부속 A
재검토 회신 접수와 부속 B · COMSOL RTOL30 결과 수신 검토 접수와 다음 계획 (`aeb35d3b5` · `da483e2d3` · `e64f587bc` · `555c123c6` · `3a90277a2`).

## §1 고정 표 §15 ↔ 구현 대응 (좌표 = `26c11d6fc`)

| § | 고정 | 구현 (`tools/preserve.py` = `PV`) | 회귀 node (`tests/test_gate89_finalize_input_binding.py`) |
|---|---|---|---|
| 15-2 a | 자리: `finalize_leg` 의 fit 전용 분기 · 두 lock 안 · 원장 `legs` 추가 · write · claim 삭제 전 · 거부는 `PreserveError("plan")` | `PV:8929` `finalize_leg` · `_lifecycle_locks` `:9010` · `_ledger_lock` `:9098` · 분기 `:9130` · **새 호출 `:9146`** (주석 `:9143–9145`) · 기록 `:9180` · 원장 write `:9210` | d02 × 4 (원장 · claim 바이트 불변) |
| 15-2 b | 대상: 위에서 한 번 읽은 `snap` 의 fit receipt (다시 읽지 않는다) | `_fit_ent = _phases.get("fit")` — `_phases = snap.get("phases")` (`:9042` 의 snapshot) | d01 (원장의 fit receipt = claim 에 기록된 것) |
| 15-2 c | 검사: 기존 공통 `_assert_external_input_binding` 그대로 (새 함수 · 두 번째 공식 없음) | `PV:6721` 정의 하나 · 호출 둘 = `phase_done` `:6950` + finalize `:9146` | d02 × 4 (이유 = "`inputs` 가" × 3 · "자기모순" × 1) |
| 15-2 d | 순서: 기존 세 문자열 비교 (`:9136–9142`) **뒤** · 기존 거부 이유 불변 | 비교의 `raise` 바로 다음 줄 | 88차 f03_03 · f03_06 `receipt_package_tampered` (이유 "소비한 밖 입력" 그대로 — 24 passed) · d03 |
| 15-2 e | 그대로: v2 최종화 · v2 fit receipt 키 · `_already_finalized` · 기록 `phases` · 재개 / 상태 view | 변경 없음 | 88차 f00_05 (v2 fit receipt 에 `inputs` 없음 → executed) · f00_06 |

## §2 RED → GREEN

| 단계 | 결과 | 원문 (`gate89_evidence/`) |
|---|---|---|
| RED (시험 6 node · HEAD `b1b44cf0f` + 작업 트리 = 시험 파일 · conftest 등록 → `76a5da16e` · source_digest `7dd546baaee9e823` = 88차 판정 대상 그대로) | **4 failed / 2 passed** — 실패 4 = d02 넷 모두 `Failed: DID NOT RAISE PreserveError` (기록 뒤 바꾼 `inputs` 를 지금 코드는 거부하지 않고 executed 로 닫는다 = **G88-N1 실행 재현**) · 통과 2 = 처음부터 GREEN 이어야 할 대조 d01 · d03 | `01_red_test_gate89.log` (머리 줄을 잘못 적은 첫 회는 `00_…` · §6-a) |
| GREEN (`26c11d6fc`) | test_gate89 **6 passed** · test_gate88 **24 passed** (88차 이유 불변) | `02_…` |
| `finalize_leg` 를 쓰는 관련 8 모듈 (영수증 재생성 전) | **485 passed / 7 failed** — 7 = `test_gate74_defensive` 의 grid_fit_v5 영수증 validator identity 낡음 (새 source_digest) · 예상된 실패 | `03_…` |
| 영수증 재생성 뒤 그 모듈 | **41 passed** (7 이 닫혔다) | `09_…` |

등록부의 `-k` 395 개 중 새 시험 node 를 고르는 식 0 (pytest `KeywordMatcher` — 선언 밖 "더 빨개짐" 위험 0). 변이 지점 전부 정확히 한 번
(`--check-preimages`). 계약 인용 좌표 (`STAGE3_CONTRACT.md` 의 `src/fitting.py`) 불변.

## §3 변이 (`-g89` 2 + `-g88` 증인 한 건)

| 회차 | 명령 | 결과 | 원문 |
|---|---|---|---|
| 1 | `-k g89 --emit-expect` (2 등록) | 2/2 기대 node 빨강 (d02 넷 · d03) · EXPECT 미선언 표시 · rc 1 | `04_…` |
| 2 | `-k finalize-binds-the-receipt-package-to-the-consumer-g88 --emit-expect` | fail node 그대로 (f03_06 `receipt_package_tampered`) · **증인이 바뀜** `Failed: DID NOT RAISE PreserveError` → `AssertionError: 거부 이유가 receipt 묶음 ↔ 소비 결속 대조가 아니다` · rc 1 (선언과 다른 이유) | `05_…` |
| 3 | `-k g89` (EXPECT 2) | **2/2 물었다 · rc 0** | `06_…` |
| 4 | `-k g88` (EXPECT 21 · 한 항목 증인 갱신) | **21/21 물었다 · rc 0** (그 밖 20 증인 불변) | `07_…` |

- `finalize-rechecks-the-durable-input-binding-g89` = 새 호출 제거 → d02 넷. `finalize-still-binds-the-receipt-package-to-the-consumer-g89` =
  receipt 묶음 ↔ consumed 비교를 끈다 (`-g88` 과 같은 자리 · 선택자만 d03) → d03 — 새 검사를 **통과하는** 자기일관 위조에서는 이 비교만
  남는다는 것을 따로 고정한다 (§6-d).
- `-g88` 한 항목의 증인 갱신은 승인 질문과 고정 표 §15-4 에서 미리 밝힌 것이다: 새 검사가 묶음 digest **단독** 변조를 결속 이유
  ("자기모순") 로 먼저 잡기 때문이다. 변이 본문 · `-k` · fail node 는 그대로이고, 원래 증인은 등록부 주석에 남겼다 (60차 마감 선례).

## §4 영수증

현행 (`7dd546baaee9e823`) history 보존 `14978adb0` → `make_receipt.py paired_fixed5_v4 grid_fit_v5` clean `134f26f48` 1 회 (rc 0 ·
07:04:16Z → 07:05:31Z · `08_…`) → `66129fc6a`. paired **35** · core `20645070605f0f03…` · grid **34** · core `e556380777b21106…` (검사 수
불변 — `src/io.py` 불변). diff 는 두 파일 각각 `core_sha256` · `validator_source_digest` (→ `803e2b7781cbc9cd`) · `validator_commit` ·
`generated_at_utc` 뿐 (platform · dirty stamp 불변). 원장 앵커 2 × 2. 그 뒤 커밋은 RUN_SCOPE 밖이라 validator identity 불변.

## §5 전체 회귀 · smoke · 등록부 전체 재생

| 단계 | HEAD (clean) | 결과 | 원문 |
|---|---|---|---|
| 전체 pytest `tests/ -q -rfEx` | `66129fc6a` | **2139 passed / 1 xfailed / rc 0** · 2026-10-04T07:08:17Z → 2026-10-04T08:00:50Z (0:52:30) · 시작 HEAD = 끝 HEAD · dirty 0 | `10_…` |
| strict smoke `./scripts/smoke_e2e.sh` | `66129fc6a` | **rc 0** · 2026-10-04T08:00:50Z → 2026-10-04T08:03:15Z · 시작 HEAD = 끝 HEAD · dirty 0 | `11_…` |
| 등록부 전체 재생 (`-k` 없음 · 분리 프로세스 · 시간 상한 없음) | `66129fc6a` | **scenario 408 (executable 397 · declared 11) · site 446 · ran 397 · 397/397 call 단계에서 선언한 이유로 물었다 · 안 물었다 0 · rc 0** · 2026-10-04T08:03:15Z → 2026-10-04T10:29:58Z · 시작 HEAD = 끝 HEAD · dirty 0 | `12_…` |

변이 수: 88차 등록부 395 + `-g89` 2 = 397 executable (declared 11 그대로). 세 실행은 한 사슬로 순차 · 그동안 작업 트리를 건드리지 않았다.

**보충 (88차 리뷰어 지적):** 88차 발송 HEAD `d6056415b` 의 docs-lint **358 passed** 원문 (2026-10-03T14:15:28Z → 14:40:56Z · 시작 HEAD =
끝 HEAD · dirty 0) 을 `13_…` 으로 싣는다 — 88차 16 원문 밖이었던 것.

## §6 자체 신고

| # | 내용 |
|---|---|
| a | **RED 로그 머리 줄** — 첫 회 (`00_…`) 머리의 둘째 줄을 `source_digest e462a3d19` 로 잘못 적었다 (값은 RUN_SCOPE 를 마지막으로 바꾼 커밋이었다). 결과는 같은 4 failed / 2 passed. 머리를 `src.io.source_digest()` 값 (`7dd546baaee9e823`) 으로 고쳐 같은 작업 트리에서 다시 돌린 것이 `01_…` 이다. 두 회차 모두 싣는다 |
| b | **`or {}` 는 등가 방어** — 새 호출의 `_fit_ent.get("receipt") or {}` 는 receipt 가 없거나 비었을 때를 위한 것이지만, 그 경우 앞의 문자열 비교가 (`input_package_digest` 가 없으므로) 먼저 "소비한 밖 입력" 으로 거부한다. 도달하지 않아 시험이 구별하지 못한다 — 변이로 고정하지 않았다 (88차 §6-j 와 같은 꼴) |
| c | **순서 · 시점의 고정** — "기존 비교 뒤" 는 88차 f03_06 `receipt_package_tampered` 가 고정한다 (앞으로 옮기면 이유가 "자기모순" 이 되어 그 단언이 실패). "원장 · claim 변경 전" 은 d02 의 바이트 불변 단언이 고정한다 (write 뒤로 옮기면 원장 바이트가 바뀐다). 둘 다 앵커 치환 변이로는 등록하지 않았다 — 줄 이동은 이 등록부의 치환 문법 밖이다 |
| d | **같은 자리의 변이 둘** — `finalize-still-binds-…-g89` 는 `-g88` `finalize-binds-…` 와 같은 앵커 · 같은 치환 (주석만 다름) 이고 선택자만 다르다. 전체 재생의 scenario · site 수에 각각 1 로 들어간다 (중복 지점 1) |
| e | **관련 모듈의 예상된 7 실패** — GREEN 뒤 · 영수증 재생성 전의 `test_gate74_defensive` 7 건은 영수증의 validator identity 가 새 source_digest 와 달라서다 (88차 `05_…` 의 7 과 같은 꼴). 재생성 뒤 41 passed (`09_…`) |
| f | **범위 밖으로 둔 것** — `phase_done` · `resume_claim` · `inspect_leg_run` · `precheck_leg_run` 쪽 검사 추가와 durable state 의 형 손상 일반 (예: receipt 가 dict 가 아닌 경우 — 지금도 `executed` 로 닫히지는 않지만 `PreserveError` 가 아닌 예외로 멈춘다) 은 §15-1 대로 건드리지 않았다. claim 의 phase receipt 를 원장으로 옮기는 경로가 `finalize_leg` (`:9180`) 하나뿐임을 읽어서 확인했다 (`migrate_legacy_finalized_leg` 는 이미 executed 인 기록에 인증 필드만 붙인다) |
| g | **동시 실행 없음** — 새 모듈의 scratch 이름은 `g89_` 접두라 88차 · 87차 모듈의 고정 경로와 겹치지 않지만, 같은 모듈의 동시 실행은 여전히 안전하지 않다. 이 라운드의 모든 시험 · 재생은 순차로만 돌렸다 |
| h | **게이트 차수 밖 작업** — 이 라운드 사이에 REIL 프로토콜 v2 재검토 접수 · 정정 부속 문서 · 재검토 요청문을, 검증 사슬이 끝난 뒤에는 부속 A 재검토 회신 접수 · 부속 B 와 COMSOL RTOL30 결과 수신 검토 접수 (§41) · 다음 계획 문서를 커밋했다 (`bms-balancing/` · `wiki/` · RUN_SCOPE 밖). 앞의 것들 위의 docs-lint 는 `c14775710` · `234ee23a7` 에서 358 passed (원문은 스크래치패드 — 이 게이트의 판정 근거가 아니어서 싣지 않았다) · 사슬 뒤의 것들은 발송 SHA 의 docs-lint 가 덮는다 (발송문) |

## §7 하지 않은 것

실행 GO · 운영 원장 v6 계획 항목 · 세대표 등록 · p_ini · `--mode all` v6 · grid v6 · `scripts/plan_leg.py` · `src/fitting.py` · `src/io.py` ·
`src/grid.py` · `run.sh` · 영수증 schema · requirements (pybamm 고정 — 2b 종결 뒤 별도 라운드 · 사용자 결정).
