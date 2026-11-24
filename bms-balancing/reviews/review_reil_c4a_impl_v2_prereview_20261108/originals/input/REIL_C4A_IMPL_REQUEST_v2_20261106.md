# REIL C4-A 구현 요청서 v2 — H Phase A 실자료 실행기 · 상한 있는 경고 기록 · runner 어댑터 · 비용 규칙 · 소스 / 승인 결속 · 행 무결성 (문서만 · 실행 0) · 2026-11-06 KST

> **구현 요청서 v2 다 (이 문서를 쓰는 동안 구현 · 시험 · 실행 0).** v1 (`docs/REIL_C4A_IMPL_REQUEST_20261106.md` · `86f2d631…` · 15,873 B) 은 그대로 두고 이 문서가 대체한다.
> 기준: 범위안 v2 (`docs/REIL_C4A_SCOPE_v2_20261106.md` · `605520b8…` · 수용 §125) · 채택된 C4 요청 v2 (`docs/REIL_C4_APPROVAL_REQUEST_v2_20261013.md` · `22dcc8e5…`) ·
> 사용자 선택 §126 (U1 분리 · U3 고정 자료 재사용 · U2 미선택) · §129 (C4A-IMPL-N1 의 회귀 범위 = **(가) 전체 회귀 + 합성 실제 호출 허용표**).
> v1 사전 검토 회신 (§128 · `reviews/review_reil_c4a_impl_prereview_20261106/` · C4A-IMPL-N1–N7 · 문구 C1) 을 반영했다. 행 번호는 검토 고정 커밋 `86cab053` 의 소스다.
> 승인되면 §7 의 절차로 **구현과 무자료 시험만** 한다. 자료 개봉 · 맞춤 · 실제 C4-A 단계 실행은 별도의 실행 요청이다.

## 0. v1 → v2 대응표

| ID | 검토 지적 (요지) | v2 의 대응 | 위치 |
|---|---|---|---|
| C4A-IMPL-N1 (P1) | 전체 회귀 GREEN 과 "실제 실행 0" 을 같이 요구할 수 없다 — 회귀 안에 실제 NSGA2 · `scipy.minimize` · COBYQA · 자식 프로세스 · SIGKILL · /proc · 로컬 Git 이 있다 | 사용자 선택 (가): 전체 회귀를 유지하고 **파일별 허용 호출 종류 · 시험당 상한 · 환경**을 고정한다. RED 전에 nodeid 목록을 수집만으로 고정 (b0) · 새 계수기 플러그인이 실제 호출을 nodeid 별로 세고 허용표 밖이면 실패. 주장은 "실자료 · 생산 단계 실행 0 · 합성 실제 호출은 허용표 안에서만" 으로 좁힌다 | §6-2 · §7 |
| C4A-IMPL-N2 (P2) | 새 경고 필드 ↔ `test_reil_c4_0b2.py` 의 exact-row 기대값 (205 · 217 · 228) 충돌 | 새 필드 다섯의 정상 · 오류 · partial 의미를 고정하고, 그 세 기대 dict 에 **키만 더하는** 제한적 정정을 허용 파일 · RED 전 봉인에 넣는다 (기존 단언 삭제 · 완화 없음) | §3 I3 · §6-3 |
| C4A-IMPL-N3 (P1) | 최종 20 / 50 자름은 실행 중 저장 상한이 아니다 (`catch_warnings(record=True)` 가 전부 저장 · 조기 구조 오류 · `_partial` 도 같음) | 수집 시점부터 상한이 있는 기록기 (`showwarning` 갈고리 · 키 ≤ 20 · 키 바이트 ≤ 240 · 정확한 총수 · overflow 수 · 고유 수의 정확 / 하한 구분 · 잘림 수). 모르는 옵션 판정은 상한과 무관한 별도 표지로 (늦게 와도 구조 중지). 정상 · 오류 · partial 이 같은 필드. `_assess` 재평가 경고는 행 포착 밖 — stderr 의 상한 · 실패 처리를 적고 무경고로 세지 않는다 | §3 I3 |
| C4A-IMPL-N4 (P1) | I1 runner 식이 중지 규칙 · 자원 · 시간 · 증거를 잇지 않는다 (wave 마다 새 t0 · `stop_rule` None · `out_roots` () · supervisor 원근거 미보존) | runner 어댑터 `runner_a`: wave 신원 · task→unit · **모든 wave 공통의 불변 절대 측정 마감** (잔여 = 마감 − 지금) · `StopRule_A` · 실제 출력 루트 · 여유 공간 대상 · supervisor 반환 전부 보존 (`SUPERVISOR_A.jsonl`). unit 900 s 의 책임자 = `StopRule_A`. 정리 20 s 의 뜻과 최악 40 s · 마감 연결표 | §3 I1 · I4 · §8 |
| C4A-IMPL-N5 (P2) | 비용식 표본 자격 미정의 (0 평가 지역 오류 → 0 나누기 → 규칙 구조 오류로 오분류) | 적격 = H termination `converged` · `budget` · 유한 비음수 wall · bool 제외 양의 정수 n_eval · 적격 ≥ 8. `solver_error` (0 평가 포함) 는 원기록 보존 · 표본 제외. 정상 반환인데 형식이 틀린 행은 규칙이 이유를 돌려 전역 중지 (예외로 흘리지 않음). E 의 `returned` 열거를 쓰지 않는다 | §3 I4 |
| C4A-IMPL-N6 (P2) | SOURCES_A 자체의 외부 승인 sha 결속 없음 · 실행 틀 소스 결속 없음 · `REQUEST=` 이 요청서가 실행 `--approval` 로 들어감 | 목록 둘 (`SOURCES_A` 실행 소스 · `SOURCES_A_FRAME` launcher · 외곽 · 판정기 · 끝 기록 작성기) 의 **목록 자체 sha 를 인자로 먼저 대조** (E `load_sources` 504–531 방식). `implementation_basis` (이 문서 + 구현 결과 봉인) 와 `execution_request` (이후 실행 요청서 · 그 승인 §) 를 분리 — 실행 승인 결속이 없거나 다르면 run-a · launcher_a 거부 | §4 · §3 I5 |
| C4A-IMPL-N7 (P2) | 세 집계 조건 0 이 행 신원 무결성을 보장하지 않는다 (중복 대체 · 127 / 129 상쇄) | unit 별 행 무결성 (`ROW_INTEGRITY_A`) — 계획 task 집합과 정확히 한 번씩 · unit · run_id · x0 · 상태별 필수 필드. 구조적 행 오류 → 실행 유효성 false (정당한 미완과 구분) · C4-B 가 쓸 수 있는 unit = 무결성 통과 + 완료 | §5-1 · §3 I1 |
| C1 (문구) | STORE_A 를 두 번 배타 생성하는 것으로 읽힌다 | **한 번의 공통 최종 게시** (정상 끝 · 전역 중지 모두 같은 `finally`) · 실패 시 덮어쓰기 · 재시도 없음 · END_RECORD 에 결과 · sha | §3 I2 |

U2 (전체 10 h 배분) 는 여전히 미선택 제안이다. 이 문서의 숫자는 실행 요청에서 확정한다.

## 1. 요약

- **만들 것 일곱 (§3):** I1 진입점 `scripts/reil_c4a_run.py` (runner 어댑터 · 행 무결성 포함) · I2 STORE_A 한 번 게시 · I3 상한 있는 경고 기록 (`reil_c4_h.py` 변경) ·
  I4 `StopRule_A` · I5 실행 틀 (launcher_a · 외곽 · 판정기 · 끝 기록 작성기 v3) · I6 무자료 시험 C4A-T01–T16 · I7 호출 계수기 플러그인.
- **계약 (§4 · §5):** 신뢰 입력 · 소스 목록 둘의 외부 sha 결속 · 구현 기준 ↔ 실행 승인 분리 · 수의 판정 · 행 무결성 · 실행 유효성과 실험 결과의 분리.
- **시험 (§6):** RED 는 새 시험만 (전부 가짜 · 실제 호출 0 을 계수기로 확인) · GREEN 은 고정한 nodeid 전체 (허용표 안의 합성 실제 호출만).
- **바꾸지 않는 것:** E 계열 바이트 · util · C6 봉인 · 배열 · 기존 증거 · `reil_c4_hb.py` · `reil_c4_monitor.py` (과학적 실행 순서와 감시 동작을 그대로 쓴다).

## 2. 연결부와 빈 곳 (읽기만)

| 연결부 | 위치 (고정 소스) |
|---|---|
| Phase A 순서 · 미실행 · 완료 대조 · ρ · 집계 | `reil_c4_hb.py` `_not_run_a` 1010 · `phase_a_complete` 1020–1045 · `stage_a` 1082–1126 · `rho_wave` 1129–1175 · `plan_counts` 1353–1388 |
| runner | `direct_runner` 1056 · `supervise_runner` 1074–1079 (wave 마다 `t0 = time.monotonic()` · 고정 limits) |
| 감시 | `reil_c4_monitor.py` `apply_rule` 224–234 · `supervise` 237–367 (`stop_rule` 기본 None · `out_roots` 기본 () · 정리 344–359 · 반환 363–367) |
| 단일 실행 | `reil_c4_h.py` `_partial` 737–748 · `_assess` 773–804 · `_run_local` 807–878 (n_eval 0 시작 822 · 경고 포착 836–848 · 모르는 옵션 856–859 · solver_error 860–865) |
| 소스 목록 | `reil_c4e_run.py` `load_sources` 504–532 (목록 바이트 sha 를 먼저) |
| launcher 의 승인 문자열 | `reil_c4e1_launch.py` 385 (`--approval … {REQUEST}`) · 831 (meta `request`) |

- v1 의 G1–G7 은 그대로이고 넷을 더한다 — **G8** runner 가 규칙 · 출력 루트 · 공통 마감 · 원근거를 잇지 않는다 · **G9** 비용 표본의 자격이 없다 · **G10** 소스 목록 자체와
  실행 승인의 외부 결속이 없다 · **G11** 집계 세 수로는 행 신원을 판정할 수 없다.

## 3. 만들 것

### I1. 진입점 `scripts/reil_c4a_run.py` (새 파일)

- **명령:** `plan-a` (자료 없이 수 · 계획만) · `seal-sources-a` (구현 끝에 SOURCES_A · SOURCES_A_FRAME 을 봉인 — §4) · `run-a` (실자료 — 실행 요청 승인에서만).
- **`run-a` 준비:** 실행 승인 결속 (§4-2 — 없거나 다르면 시작 전 거부) · 소스 목록 대조 (§4-1) · 환경 identity · 입력 결속 (§4-3) · util 적재 · 행별 Model · halfcell ·
  옵션 (C6 `COBYQA_OPTIONS.json` 바이트) · 게이트 (int 키) · 배열 (고정 MANIFEST).
- **runner 어댑터 `runner_a` (N4):** `stage_a` 가 부르는 runner 계약 (`runner(tasks, ctx, task_fn) → {states, global_stop}`) 을 지키면서 —
  - run-a 원점에서 **불변 절대 측정 마감** `D_meas = t_run0 + MEASURE_A` 를 한 번 정한다. wave 를 부를 때마다 `remaining = D_meas − now` · `limits = LIMITS_A ⊕ {measure: remaining}` ·
    `t0 = now` 로 `mon.supervise` 를 부른다 → 모든 wave 의 `t0 + measure = D_meas` (같은 절대 마감 · 새 예산이 생기지 않는다). `remaining ≤ 60 s` 면 시작하지 않고 모든 task 를
    `NOT_STARTED` · 사유 "단계 경계 — 남은 측정 시간" 으로 돌린다.
  - `stop_rule = StopRule_A(wave_id, task_unit, maxfev, n_workers=4, unit_limit_s=900, deadline_rel=remaining)` (I4) · `out_roots = (run-a 출력 폴더, 증거 폴더)` · `free_path = 출력 폴더`.
  - wave 신원: 순번 · 첫 unit · task_id 범위 · task→unit · task→(run_id, x0) · 작업자 배정 · 원점 (monotonic · UTC) · remaining.
  - supervisor 반환 **전부** (`samples` · `structural` · `owned_alive_after` · `drain_ok` · `exitcodes` · `workers` · `worker_end` · `worker_deadline` · `t_stop` · `deadline_rel` ·
    `global_stop`) 를 wave 마다 `SUPERVISOR_A.jsonl` 에 한 줄로 붙인다 (states 는 STORE_A 에). HB 의 과학적 실행 순서 (wave 1 → ρ) 는 바꾸지 않는다.
- **행 무결성 (N7):** 각 run unit 에 대해 `ROW_INTEGRITY_A.json` (§5-1).
- **기록 (`<out>/`):** `HEADER` · `IDENTITY` · `ROWS_A` · `STORE_A` (I2) · `COUNTS` · `ROW_INTEGRITY_A` · `WARNINGS` · `RULE_A` · `SUPERVISOR_A.jsonl` · `RESOURCES` ·
  `OPERATION` · `END_RECORD`. 정확한 이름 집합은 c 에서 고정한다. `HStop` 은 기록하고 끝낸다 — 재시도 0.

### I2. STORE_A — 한 번의 공통 최종 게시 (C1)

- `STORE_A.json` = store 의 JSON 사본 (`planned_units` · `phase_a` · `not_run` · `summaries` · `rho_denominators` · `events` · `next_task_id` · `seq` · 행 무결성 결과).
- **게시는 run-a 의 `finally` 에서 한 번** (정상 끝 · 전역 중지 · 예외 모두 같은 경로) — 임시 파일에 쓰고 sha 를 잰 뒤 배타 이름 바꾸기 (대상이 있으면 실패). 실패하면 덮어쓰기 ·
  재시도 없이 `END_RECORD.store_publish` 에 오류를 적고 실행 유효성 false. 성공하면 게시한 바이트의 sha 를 END_RECORD 에 넣는다. 읽기 함수 `load_store_a` 는 sha 를 받아 대조한다.

### I3. 상한 있는 경고 기록 (N3 · N2 · `reil_c4_h.py` 변경)

- **기록기 `_WarnBox`:** `_run_local` 의 `warnings.catch_warnings(record=True)` 를 `warnings.catch_warnings()` + `simplefilter("always")` + `warnings.showwarning = box.show` 로
  바꾼다 (블록을 나가면 원래 갈고리로 돌아간다). `show` 는 경고 하나마다:
  - `n_total += 1` (정확한 정수 · 상한 없음).
  - 원문 `text = f"{category.__name__}: {message}"` 에 `"Unknown solver options"` 가 있으면 `unknown_option = True` — **키 저장 여부와 무관한 별도 표지**.
  - 키 = `text` 를 UTF-8 **240 바이트**로 자른 것 (잘리면 `n_truncated += 1`). 이미 있는 키면 그 수 + 1 · 없고 저장 키가 **20 개 미만**이면 새 키 · 아니면 `n_overflow += 1`.
  - 저장량 상한 = 키 20 × 240 B + 정수 다섯 — 경고가 몇 개 나와도 이 이상 저장하지 않는다.
- **행 필드 (정상 · solver_error · partial 공통):** `warnings` = 저장 키 정렬 (≤ 20 · 기존 필드와 같은 이름 · 같은 형식) · `warnings_n_total` · `warnings_n_distinct` ·
  `warnings_distinct_exact` (= `n_overflow == 0`) · `warnings_n_overflow` · `warnings_n_truncated`. `warnings_distinct_exact` 가 false 면 `warnings_n_distinct` = 저장 키 수 + 1 =
  **하한**이다 (정확한 고유 수가 아님을 필드로 표시).
- **구조 중지:** 모르는 옵션 판정은 `box.unknown_option` 으로 한다 (856–859 의 문구 대조 대신) — 키 상한 뒤에 와도 구조 중지는 그대로다. 조기 구조 오류 (842–845) 와 모든
  `_partial` 은 `acc["wbox"]` 에서 같은 여섯 필드를 그 시점 값으로 남긴다 (0 으로 채우지 않음 — 기록기가 아직 없으면 필드를 넣지 않는다).
- **`_assess` 재평가 경고:** 행 포착 밖이다 (재평가는 포착 블록 뒤). 프로세스 stderr 로 가며, launcher_a 가 자식 stderr 를 증거 폴더의 파일로 받는다. 그 파일은 `out_roots` 에
  들어가므로 감시의 새 산출 상한 (1 GiB) 이 저장 한도이고, 넘으면 그 wave 가 전역 중지된다 (실패 처리 = 기존 감시 사유 · 기록). END_RECORD 에 stderr 바이트 수를 적는다.
  `WARNINGS.json` 과 판정기는 재평가 경고를 **"미집계 (stderr)"** 로 적고, 무경고로 세지 않는다.
- **run-a 의 집계 `WARNINGS.json`:** 범위를 **"행마다 저장된 키 (≤ 20) 에서 관측한 키"** 로 한정한다. (키별 그 키가 나온 실행 수 · 전체 고유 키 ≤ 50 · 넘으면 overflow 수) ·
  `warnings_distinct_exact` false 인 행 수 · `n_truncated` 합 · `n_total` 합 · "재평가 경고 미집계" 문구를 함께 적는다. 이 집계를 전체 경고의 유형 · 문구별 실행 수로 쓰지 않는다.
- **이 변경은 C4-0b1 / 0b2 에서 수용된 `reil_c4_h.py` 의 바이트를 바꾼다** — 새 식별값은 구현 결과 봉인 (§4-1) 에 들어가고 실행 요청에서 묶는다.

### I4. 비용 · unit 규칙 `StopRule_A` (N5 · N4 · C4 v2 131 행의 네 요소)

- **적격 표본 (N5):** 그 wave 의 완료 행 가운데 H termination ∈ {`converged`, `budget`} · `wall` 이 유한한 비음수 · `n_eval` 이 bool 이 아닌 양의 정수인 것. c = wall / n_eval.
  `solver_error` 행 (목적함수 첫 호출 전 지역 오류의 0 평가 포함) 은 원기록 그대로 두고 표본에서 뺀다 (`excluded: solver_error`). E 의 `returned` 열거는 쓰지 않는다.
- **정상 반환인데 형식이 틀린 행** (termination 은 converged / budget 인데 wall 이 비유한 · 음수거나 n_eval 이 0 · 음수 · bool · 비정수): 규칙이 **문자열 사유**
  ("비용 표본 형식 오류 — task …") 를 돌려 전역 중지한다 — 예외를 던지지 않으므로 `apply_rule` 의 구조 오류 분류 (224–234) 와 섞이지 않는다.
- **최소 표본:** 적격 8 (wave 안 누적 · tick 마다 다시). **기준 통계:** 적격 c 의 위쪽 중앙 (0-기반 index ⌊n/2⌋).
- **중지 경계 (엄격한 >):** `now_rel + (n_remaining × maxfev × c) / n_workers > deadline_rel` 이면 사유를 돌린다. `n_remaining` = 그 wave 계획 task − 완료 (착수 뒤 미완은 남은 것으로 센다).
  `deadline_rel` = runner_a 가 준 잔여 (= 공통 절대 마감까지).
- **unit 900 s (N4):** unit 마다 첫 task 시작 (snapshot `started`) 에서 잰다 — 아직 모든 task 가 끝나지 않았고 `now_rel − 첫 시작 > 900` 이면 사유 "unit … 900 s 초과" (대기 ·
  병렬 포함 경과). unit 의 마지막 task 가 끝나면 그 unit 을 닫고 더 보지 않는다. **책임자 = `StopRule_A`** (감시가 tick 마다 부른다).
- **자원:** 표본 RSS 합 ≤ 4 GiB · 새 산출 ≤ 1 GiB · 디스크 여유 ≥ 5 GiB (LIMITS_A · 감시의 기존 판정). v1 의 "중앙 3 배" 예시는 채택하지 않는다.
- 규칙의 모든 판정 입력 · 사유는 `RULE_A.json` 에 남긴다.

### I5. C4-A 실행 틀 (새 파일 · E 계열 바이트는 그대로)

- **launcher `scripts/reil_c4a_launch.py`** — v6 의 형식을 따른다 · 단계 하나 `phase_a` · 고정 argv · 작업 폴더 `SP/c4a` · 자료 `SP/c4e1/data` 읽기만 (U3) · 새 pycache 폴더 ·
  사전 / 사후 검사. **승인 문자열과 메타의 `request` 는 `execution_request` (§4-2) 다 — 이 구현 요청서가 아니다.** 실행 승인 결속 · `SOURCES_A_FRAME` 대조가 없으면 자식을
  띄우지 않는다. 자식 stderr 는 증거 폴더 파일로 (I3).
- **외곽 · 판정기 · 끝 기록 작성기 v3 초안** (`docs/*_v3_*.py.txt`) — 단계 `phase_a` 를 더한다 (감시 여유 · 조각은 §8 의 표) · phase_a 판정 항목 (§5-2) · E 단계 동작 불변.

### I6. 무자료 시험 C4A-T01–T16 — §6-1.

### I7. 호출 계수기 플러그인 `tests/c4a_callcount.py` (N1 · 새 파일)

- pytest `-p` 로만 켠다 (기존 conftest · 시험 파일은 건드리지 않음). 세는 것: **K1** `scipy.optimize.minimize` (COBYQA 포함) · **K2** `pymoo.optimize.minimize` (util NSGA2) ·
  **K3** `subprocess.Popen` 생성 · **K4** `os.kill` · `os.killpg` · **K5** `multiprocessing` `Process.start` · **K6** argv[0] 이 git 인 K3 · **K7** xlsx 읽기 (`openpyxl.load_workbook` ·
  `pandas.read_excel`). 감싸기만 하고 동작을 바꾸지 않는다 (원 함수를 그대로 부른다).
- nodeid 별 계수를 `CALLS_A.json` 에 쓰고, 세션 끝에 §6-2 의 허용표와 대조한다 — 허용 밖 종류 1 회 · 상한 초과 · K7 > 0 이면 세션을 실패로 끝낸다 (이유와 nodeid 를 적는다).

## 4. 입력 · 소스 · 승인 계약 (N6)

### 4-1. 소스 목록 둘 — 목록 자체의 sha 를 먼저

| 목록 | 정확한 경로 집합 | 결속 |
|---|---|---|
| `SOURCES_A.json` | run-a 가 import 하는 것: `reil_c4a_run.py` · `reil_c4_h.py` · `reil_c4_hb.py` · `reil_c4_monitor.py` · `reil_c5_pilot.py` · `reil_p0.py` · `reil_c4_e3a.py` (+ import 하면 `reil_c4e_run.py`) — 구현 c 에서 import 그래프로 확정 | run-a `--sources … --sources-sha256 <hex>` — 목록 바이트 sha = 인자 (E `load_sources` 504–532 와 같은 순서) → 경로 집합 정확 → 항목별 sha · bytes |
| `SOURCES_A_FRAME.json` | `reil_c4a_launch.py` · 외곽 · 판정기 · 끝 기록 작성기 v3 · wrapper | launcher_a `--frame-sources … --frame-sources-sha256 <hex>` — 같은 순서로 대조 · 외곽은 launcher 를 띄우기 전에 같은 대조 |

- 소스와 목록을 **함께** 바꾸면 내부 상호 대조는 통과하지만 목록 sha 가 인자와 달라 거부된다 (T05).
- 두 목록은 구현 단계 d 에서 `seal-sources-a` 로 만든다 (= **구현 결과 봉인**). 그 sha 는 결과 검토를 거쳐 실행 요청서에 적힌다 — 이 요청서는 아직 없는 구현의 sha 를 요구하지 않는다.

### 4-2. 구현 기준 ↔ 실행 승인 분리

| 이름 | 무엇 | 어디에 쓰나 |
|---|---|---|
| `implementation_basis` | 이 구현 요청서 v2 (경로 · sha) + 구현 결과 봉인 (SOURCES_A · FRAME 의 sha) + 구현 승인 § | 구현 단계의 기록 · 결과 검토 |
| `execution_request` | 이후의 별도 실행 요청서 (경로 · sha) · 그 승인 § (원장) · 그 요청서에 적힌 SOURCES_A · FRAME sha · 입력 sha · LIMITS_A · 시간 배분 | run-a · launcher_a 의 인자와 메타 · `--approval` 문자열 |

- run-a · launcher_a 는 `--execution-request <path> --execution-request-sha256 <hex> --approval-section §N` 을 받는다. 요청서 바이트 sha = 인자 · 요청서 본문의 SOURCES_A ·
  FRAME sha = 받은 목록 인자 · 승인 § 가 원장에 있다 — 셋 중 하나라도 없거나 다르면 **시작 전 거부** (fail-closed · T14). `implementation_basis` 를 실행 승인으로 받지 않는다.

### 4-3. 입력 (v1 §3 그대로)

`LFP_Data.xlsx` (10,841,377 B · `fd50e095…`) · `util_LFP.py` (33,754 B · `3c19e45e…`) · `P0_RESULT.json` (`reil_c4e_run.py` 63–64 의 고정 sha) · C6 봉인 (`4f120948…`) ·
Phase A 배열 MANIFEST (`861c33ac…` · 정확한 파일 집합) · E3a 완료 근거 (`evidence/reil_c4e1_20261106/run/` · §122 의 수용 범위) · 시작 · 끝의 실제 소비 바이트 · 행마다 `options_received`.
H 배열 (`d122117f…`) 은 C4-A 가 읽지 않는다 ("소비 안 함" 으로 기록 · C4-B 입력).

## 5. 판정 계약

### 5-1. run-a 의 판정 — 수 · 행 무결성 · 유효성

- **수 (범위안 v2 §3-2 · `plan_counts`):** 등록 9,856 · 조건 제외 (ENDPOINT_GATE · JD_EMPTY_MASK · RHO_PRECONDITION — unit 수와 실행 수 · 이유) · 상태별 행 · `unaccounted_units` ·
  `unaccounted_runs` · `row_count_mismatch`. 9,856 · 7,040 을 "반환해야 정상" 으로 쓰지 않는다.
- **행 무결성 `ROW_INTEGRITY_A` (N7) — 세 집계 수와 따로:** run unit 마다 계획 task 집합 (task_id → run_id · unit · x0 · 작업자) 을 기준으로
  - 행의 task_id 집합 = 계획 집합 · 각각 정확히 한 번 (누락 · 중복 · 계획 밖 task 를 따로 적는다) · 행 수 128.
  - 모든 행의 unit = 그 unit · COMPLETED 행의 run_id · x0 = 계획 task 의 값 (x0 는 봉인 배열과 같은 값 — `phase_a_complete` 와 같은 비교).
  - 상태별 필수 필드 — COMPLETED: run_id · unit · x0 · n_eval (bool 제외 정수 ≥ 0) · termination ∈ {converged, budget, solver_error} · witness · 경고 여섯 필드. STARTED_INTERRUPTED:
    task_id · interrupt_reason (+ 있으면 structural_partial). NOT_STARTED: task_id · interrupt_reason.
  - 결과: unit 별 `integrity_ok` 와 오류 목록. **구조적 행 오류** (누락 · 중복 · 계획 밖 · unit / run_id / x0 불일치 · 필수 필드 오류) 는 정당한 미완 (필드가 바른 NOT_STARTED ·
    STARTED_INTERRUPTED) 과 다른 범주로 적는다. `phase_a_complete` 의 false 나 그 사유 문자열 (예: 정상 중단의 "run 번호 누락") 만으로 구조 오류를 판정하지 않는다.
- **실행 유효성:** 사전 대조 모두 통과 · 모든 run unit 의 `integrity_ok` · `unaccounted_*` 0 · `row_count_mismatch` 0 · STORE_A 게시 성공 · 기록 집합 정확 · 모든 wave 의
  `owned_alive_after` 0 · `drain_ok` true · supervisor 원근거 저장 (wave 수 = SUPERVISOR_A 줄 수). 하나라도 아니면 false 와 이유.
- **실험 결과 (유효성과 따로):** 범주별 수 · unit 별 완료 / 미완 · 전역 중지 이유 · UNFIT 은 완료 unit 에만 (원장 1406–1414).
- **Parent 소비 · C4-B 인계:** C4-B 가 Phase A 결과로 쓸 수 있는 unit = `integrity_ok` + `phase_a_complete` true. 무결성 오류 unit 은 인계 목록에서 빠지고 이유가 남는다.
  모든 unit 의 완료나 9,856 회 반환을 요구하지 않는다.

### 5-2. 판정기의 `phase_a` 항목 (E 단계 공통 항목 + 아래)

`run/` 파일 집합 정확 · COUNTS 정합 (두 항등식) · ROW_INTEGRITY_A 의 오류 0 (아니면 유효성 false) · STORE_A sha 가 END_RECORD 에 있고 게시 성공 · WARNINGS 의 상한 준수와
"재평가 경고 미집계" 문구 · SUPERVISOR_A 줄 수 = wave 수 · 정리 증거 · 실행 승인 결속 (§4-2) · 유효성과 실험 결과를 따로 적음.

## 6. 시험

### 6-1. 새 시험 C4A-T01–T16 (`tests/test_reil_c4a.py` · 전부 가짜 · 실제 호출 0)

가짜 util · 가짜 minimize · 가짜 시계 · 합성 입력 · 봉인 배열 (읽기만). RED 의 기대 원인 = 골격 (NotImplementedError · 없는 이름).

| ID | 대조 |
|---|---|
| T01 | `plan-a` — 등록 9,856 · 끝점 게이트 22 unit · 계획 7,040 (실제 P0 · 봉인 배열 · util import 없음) |
| T02 | 게이트 키 int · `stage_a` 와 맞음 (str 키 거부) |
| T03 | 입력 sha 불일치 (xlsx · util · P0 · C6 · 배열 MANIFEST · E3a 근거) → 시작 전 거부 |
| T04 | 배열 npy 와 로컬 MANIFEST 를 함께 바꿔도 잡힌다 |
| T05 | SOURCES_A · FRAME — 항목 추가 · 누락 · 변경 → 거부 · **소스와 목록을 함께 바꾸면 목록 sha 인자로 거부** (N6) |
| T06 | 행 무결성 — 128 행 중 하나를 다른 run_id 의 중복으로 대체: `plan_counts` 세 수는 0 / 빈 목록인데 `ROW_INTEGRITY_A` 는 구조 오류 · 유효성 false (N7) |
| T07 | 한 unit 127 행 · 다른 unit 129 행 (합계 상쇄) → 두 unit 모두 무결성 오류 · x0 / run_id 불일치 → 오류 · 정당한 NOT_STARTED / STARTED_INTERRUPTED 는 오류 아님 (N7) |
| T08 | 정당한 미실행 (ENDPOINT_GATE · JD_EMPTY_MASK · RHO_PRECONDITION) 은 이유와 함께 세고 오류가 아니다 |
| T09 | wave 1 전역 중지 → STORE_A 가 `finally` 에서 **한 번** 게시 · ρ 진입 없음 · SUPERVISOR_A 1 줄 · 수 정합 (C1 · N4) |
| T10 | ρ wave 안 중지 → 뒤 ρ 는 NOT_RUN:RHO_PRECONDITION · **둘째 wave 의 measure = 같은 절대 마감까지의 잔여** (새 예산 아님) · 잔여 ≤ 60 s 면 시작 안 함 (N4) |
| T11 | 경고 기록기 — 키 20 상한 · overflow 수 · `distinct_exact` false 와 하한 · 240 B 잘림 수 · 저장량 상한 · **키 상한 뒤의 늦은 Unknown solver options → 구조 중지** · 조기 구조 오류 partial 에 그 시점 계수 · 집계 50 상한 · "재평가 경고 미집계" (N3) |
| T12 | `StopRule_A` — 0 평가 solver_error 는 표본 제외 · 비유한 / 음수 wall · bool n_eval · 적격 7 / 8 경계 · 위쪽 중앙 · 엄격한 > · 형식 틀린 정상 행 → 문자열 사유 (구조 오류 아님) · unit 900 s 초과 → 사유 · 닫힌 unit 은 다시 보지 않음 (N5 · N4) |
| T13 | STORE_A — 왕복 일치 · 배타 게시 · 쓰기 실패 → 덮어쓰기 · 재시도 없음 · 유효성 false · END_RECORD 의 sha (C1) |
| T14 | launcher_a — argv 고정 · 자료 sha 사전 검사 · 새 pycache · **실행 승인 없음 · 요청서 sha 불일치 · 본문 sha 불일치 → 자식 안 띄움** · FRAME 대조 · 정리 미완 (`owned_alive_after` > 0) · supervisor 원근거 누락 → 유효성 false (N6 · N4) |
| T15 | 외곽 / 판정기 / 끝 기록 작성기 v3 — §8 의 감시 여유 · 조각 · phase_a 항목 (fixture) · E 단계 동작 불변 |
| T16 | 계수기 플러그인 자체 — 가짜 함수 호출이 nodeid 별로 세어짐 · 허용 밖 종류 · 상한 초과 · K7 → 세션 실패 표시 (N1) |

### 6-2. 회귀와 합성 실제 호출 허용표 (N1 · 사용자 선택 가)

- **회귀 파일:** `tests/test_reil_c4_0a.py` · `_0a_fix` · `_0b1` · `_0b1_fix` · `_0b1_fix2` · `_0b2` · `_0b2_fix` · `test_reil_c4e.py` · `test_reil_c4e_fix.py` ·
  `test_reil_c4e1_launch.py` · `test_reil_c4e1_runner.py` (환경 변수가 없으면 건너뜀 — 건너뜀은 이 파일만 허용).
- **nodeid 고정 (b0 · RED 전):** 위 파일 + `test_reil_c4a.py` 를 `pytest --collect-only -q` 로 **수집만** 해 `NODEIDS_A.txt` 로 커밋한다. GREEN 은 이 목록 전체를 같은 순서로 부른다.
- **허용표 (계수기 I7 이 강제 · 시험당 상한):**

| 파일 | 허용 종류 | 시험당 상한 | 근거 (검토 인용) |
|---|---|---|---|
| `test_reil_c4_0a.py` · `_0a_fix` | K2 (보존 util 의 합성 NSGA2) · K5 | K2 ≤ 2 · K5 ≤ 16 | `test_reil_c4_0a.py:349–364` |
| `test_reil_c4_0b1*.py` · `test_reil_c4_0b2*.py` | K1 (합성 문제의 실제 `scipy.minimize` · COBYQA) | K1 ≤ 2,000 | `test_reil_c4_0b1.py:396–415` · `test_reil_c4_0b2.py:307–321 · 446–456` |
| `test_reil_c4e.py` · `_fix` | K2 · K3 · K5 · K6 (임시 로컬 저장소) | K2 ≤ 2 · K3 ≤ 200 · K5 ≤ 16 | — |
| `test_reil_c4e1_launch.py` · `_runner` | K3 · K4 · K6 (합성 자식 · 손주 · SIGKILL · /proc · 임시 로컬 Git) | K3 ≤ 200 · K4 ≤ 200 | `test_reil_c4e1_launch.py:203–208 · 386–419` |
| `test_reil_c4a.py` (새) | 없음 | 0 | — |
| 모든 파일 | K7 (xlsx 읽기) 금지 | 0 | — |

- **환경:** 봉인된 venv (C4-ENV identity) · cwd `bms-balancing` · `tmp_path` · 네트워크 불요 (Git 은 로컬만) · 실자료 경로 없음.
  `test_reil_c4_0a_fix.py::test_out_the_synthetic_nsga2_outcome_is_kept_as_evidence` 는 기록 위치를 요구한다 (390 행) — GREEN 에서 `REIL_C4_FIX_EVIDENCE` =
  `evidence/reil_c4a_impl_<D>/fix_outcome/` · `REIL_C4_FIX_STEP` = `c4a_green` 을 준다. `test_reil_c4e1_runner.py` 는 `REIL_C4E1_RUNNER_UNDER_TEST` 를 주지 않아 모듈 단위로
  건너뛴다 (36–38 행 · 허용된 건너뜀은 이것뿐).
- **주장의 범위:** "실자료 개봉 · 생산 단계 (launcher_a 의 실제 phase_a) 실행 0 · 합성 실제 호출은 위 허용표 안에서만 · 계수는 `CALLS_A.json`". 시간 상한만으로 실제 호출 0 을
  주장하지 않는다.

### 6-3. 기존 시험의 제한적 정정 (N2 — 허용 파일 하나)

- `tests/test_reil_c4_0b2.py` 의 세 기대 dict 에 **새 경고 다섯 키만 더한다** (기존 키 · 단언 삭제 · 부분 비교로 완화 없음):
  - 205–208 행 `want` (정상): `warnings_n_total` 0 · `warnings_n_distinct` 0 · `warnings_distinct_exact` true · `warnings_n_overflow` 0 · `warnings_n_truncated` 0.
  - 217–219 행 (util 오류 · solver_error): 위와 같은 값.
  - 228 행 `part` (모르는 옵션 구조 중지 partial): `warnings_n_total` 1 · `warnings_n_distinct` 1 · `warnings_distinct_exact` true · `warnings_n_overflow` 0 · `warnings_n_truncated` 0.
- 다른 회귀 파일은 행 전체 비교가 없다 (키별 단언만 — 0b1_fix 122 · 0b1_fix2 92 · 0b2 242). 이 정정은 b 에서 새 시험과 함께 RED 전에 커밋 · sha 를 봉인한다.

## 7. 구현 절차 (승인 뒤 · 단계마다 첫 예상 밖 결과에서 멈춤 · 재시도 0)

| 단계 | 내용 | 호출 · 상한 |
|---|---|---|
| a | 승인 기록 § · 보존 규칙 (`evidence/reil_c4a_impl_<D>/**`) | 문서 · Git |
| b0 | `NODEIDS_A.txt` 고정 — 수집만 (`--collect-only`) · 허용표 (§6-2) 를 기계 형식 `ALLOW_A.json` 으로 · 커밋 | pytest 수집 1 회 · ≤ 120 s |
| b | T01–T16 원문 · 골격 · I7 계수기 · §6-3 의 정정 커밋 → **RED 1 회 (새 시험만 · 계수기 켬)** — 기대: T01–T16 실패 (골격) · 실제 호출 0 · 예상 밖 통과는 fixture 가 진실을 가린다는 뜻이므로 멈춤 | pytest 1 회 · ≤ 600 s |
| c | I1–I5 · I7 구현 → 정적 자체 검토 → **GREEN 1 회 (`NODEIDS_A` 전체 · 계수기 켬)** — 허용 실패 0 · 건너뜀은 runner 파일만 · 계수는 허용표 안 | pytest 1 회 · ≤ 1,800 s |
| d | `seal-sources-a` (구현 결과 봉인 — SOURCES_A · FRAME) · 끝 기록 (`CALLS_A.json` 포함) · 비밀 검사 · 커밋 · push · 결과 § · 결과 검토 발송문 → 멈춤 | 문서 · Git |

- 실패하면 그 자리의 기록을 커밋하고 결과 §에 적고 멈춘다. 자료 개봉 · 생산 단계 실행은 0 이다.

## 8. 실행 단계의 마감 연결표 (U2 의 입력 · 숫자는 실행 요청에서 확정)

| 구간 | 값 (제안) | 원점 → 닫힘 | 책임 |
|---|---|---|---|
| 전체 | ≤ 36,000 s (10 h · U2 미선택) | T_a (a0) → g3 의 push 반환 | wrapper |
| 착수 창 | ≤ 5,400 s | T_a → phase_a 단계 시작 (wrapper 는 `시작 + 28,800 ≤ T_end − R` 일 때만 launcher 를 띄운다) | wrapper |
| 단계 (외곽 감시 여유) | 28,800 s | 단계 시작 기록 → 감시 기한 · 아래 여섯 줄이 모두 이 안 | 외곽 |
| ├ run-a 준비 | ≤ 900 s | run-a 시작 → `t_run0` (원점) | run-a |
| ├ 측정 (모든 wave 공통 절대 마감) | `MEASURE_A` = 25,800 s | `t_run0` → `D_meas = t_run0 + MEASURE_A` · wave 마다 measure = `D_meas − now` | runner_a + 감시 |
| ├ unit | 900 s | unit 의 첫 task 시작 → 마지막 task 끝 (대기 · 병렬 포함) | `StopRule_A` |
| ├ wave 정리 | "정리 20 s" = terminate 뒤 **공통 join 마감** (`limits.grace` 20) · 그 뒤 살아 있는 작업자마다 kill + join 5 s → 최악 20 + 5 × 4 = 40 s / wave · 단계 안 정리 여유 600 s | 중지 사유 → 마지막 join | 감시 (기존 344–359) · 증거 = `owned_alive_after` · `drain_ok` · `exitcodes` |
| ├ run-a 기록 · STORE_A 게시 · run-a 의 END_RECORD | ≤ 900 s | `D_meas` (또는 중지) → run-a 반환 | run-a |
| └ launcher_a 사후 검사 · 반환 · 외부 관측 | ≤ 300 s (+ 여유 300 s) | 자식 반환 → launcher 반환 | launcher_a · 외곽 |
| 종결 reserve R | 1,800 s | 감시 기한 → T_end: 판정기 · **전체 끝 기록** (단계 안 END_RECORD 와 다른 파일) · 커밋 · push 반환 | wrapper / g |

- 900 + 25,800 + 600 + 900 + 300 + 300 = 28,800 — 단계 안의 준비 · 정리 · 기록을 착수 창이나 R 에서 다시 세지 않는다. run-a 의 END_RECORD 는 단계 안 · 전체 끝 기록은 R 안이다 (이중 계산 없음).
- 감시 조각 · 호출 수 (E1 의 6,600 s · ≤ 5) 는 외곽 v3 에서 28,800 s 에 맞춰 정하고 T15 로 대조한다.

## 9. 밝힐 것

1. I3 은 수용된 `reil_c4_h.py` 바이트를 바꾼다 (기록기 · 필드 다섯 · 모르는 옵션 표지). `reil_c4_hb.py` · `reil_c4_monitor.py` 는 바꾸지 않는다 — 어댑터 · 규칙은 새 파일에 둔다.
2. `_assess` 재평가 경고는 행 포착 밖이다 (stderr · 감시 상한 · 미집계 표시).
3. 허용표의 상한은 정적 읽기로 정한 넉넉한 값이다. GREEN 에서 넘으면 실패로 멈추고 결과 §에 적는다 (상한을 사후에 올리지 않는다).
4. 9,856 · 7,040 은 기대 반환 수가 아니다. `MEASURE_A` 등 §8 의 숫자는 제안이다.
5. 줄 번호는 고정 커밋 `86cab053` 의 소스다. 시험 함수 · 기록 파일의 정확한 이름은 b · c 에서 고정해 결과 §에 적는다.

## 10. 하지 않는 것

자료 개봉 · 맞춤 · 실제 C4-A 단계 실행 (별도 실행 요청) · C4-B · COMSOL · util · C6 봉인 · 배열 · 기존 증거 · E 계열 · `reil_c4_hb.py` · `reil_c4_monitor.py` 의 변경 · 재봉인 ·
설치 · 환경 재구축 · 기존 시험의 단언 삭제나 완화.
