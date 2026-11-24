# REIL C4-A 구현 요청서 v1 — H Phase A 실자료 실행기 · 저장 · 경고 · 비용 중단 · C4-A 실행 틀 · 무자료 시험 (문서만 · 실행 0) · 2026-11-06 KST

> **구현 요청서 v1 이다 (이 문서를 쓰는 동안 구현 · 시험 · 실행 0).** 기준: C4-A 범위안 v2 (`docs/REIL_C4A_SCOPE_v2_20261106.md` · `605520b8…` · 수용 §125) ·
> 채택된 C4 요청 v2 (`docs/REIL_C4_APPROVAL_REQUEST_v2_20261013.md` · `22dcc8e5…`) · 사용자 선택 §126 (U1 분리 · U2 는 이 문서의 배분을 본 뒤 · U3 고정 자료 재사용).
> 승인되면 §6 의 절차로 **구현과 무자료 시험만** 한다. 자료 개봉 · 맞춤 · 실제 C4-A 실행은 별도의 실행 요청이다.

## 0. 요약

- **만들 것 여섯 (§2):** I1 실자료 진입점 `scripts/reil_c4a_run.py` · I2 store 저장 · I3 경고 기록 (`reil_c4_h` 최소 변경) · I4 Phase A 비용 중단 규칙 · I5 C4-A
  실행 틀 (launcher · 외곽 · 판정기 · 끝 기록 작성기) · I6 무자료 시험.
- **계약 (§3 · §4):** 신뢰 입력 · 실제 소비 바이트 · 수의 판정 (등록 / 조건 제외 / 착수 / 완료 / 중단 / 미착수) · 실행 유효성과 실험 결과의 분리.
- **시험 (§5):** C4A-T01–T15 (RED 먼저) + 기존 회귀. **구현 단계의 호출 (§6):** RED 1 회 · GREEN 1 회 · 재시도 0.
- **실행 단계 시간 배분안 (§7 · U2 입력):** 전체 10 h = 착수 창 5,400 s + 단계 28,800 s + 종결 R 1,800 s.
- **바꾸지 않는 것:** E 계열 바이트 (`reil_c4e_run.py` · launcher v6 · 외곽 / 판정기 / 끝 기록 작성기 v2) · util · C6 봉인 · 배열 · 기존 증거.

## 1. 지금 코드의 연결부와 빈 곳 (읽기만 · 줄 번호는 확인함)

| 연결부 | 위치 |
|---|---|
| Phase A 순서 · 미실행 · 완료 대조 · ρ | `reil_c4_hb.py` `stage_a` 1082 · `_not_run_a` 1010 · `phase_a_complete` 1020 · `rho_wave` 1129 · `plan_counts` 1353 |
| store · runner | `new_store` 992 (메모리만) · `direct_runner` 1056 · `supervise_runner` 1074 (wave 마다 새 원점 — `mon.supervise`) |
| 단일 실행 | `reil_c4_h.py` `run_phase_a` 896 → `run_local` 881 → `_run_local` 807 (COBYQA · 경고 포착 836–848 · 모르는 옵션 → 구조 중지 856–859) |
| 배열 · 게이트 | `load_phase_a_arrays` 679 · `phase_a_tasks` 698 · `endpoint_gate` 507 · `jd_gate` 483 · `rho_denominators` 920 |

- **G1** ctx · runner · store · arrays 를 실자료로 묶는 곳이 없다 (지금은 시험에서만 — `tests/test_reil_c4_0b2.py`).
- **G2** store 는 메모리에만 있다 — C4-B 에 넘길 저장이 없다.
- **G3** 게이트의 키 형이 다르다 — `h.dryrun` 은 `str(r)` (1044), `hb.dryrun_b` 와 `stage_a` 는 `int` (1441).
- **G4** Phase A 배열 폴더의 로컬 MANIFEST (`reil_c4_arrays_20261013/MANIFEST.json` · `861c33ac…`) 가 코드에 고정돼 있지 않다 (npy 바이트는 C6 MANIFEST 로 대조).
- **G5** 경고는 실행마다 고유 문구 20 개만 남는다 — 총수 · 고유 수 · 초과 표시가 없고, `_assess` 재평가의 경고는 포착 밖이다.
- **G6** E 실행기의 신뢰 소스 집합 · 필드 · 비용 중단 규칙 · 집계 · 완료 판정은 E3a 용이다 (Phase A 의 종료는 converged / budget / solver_error).
- **G7** launcher v6 · 외곽 / 판정기 / 끝 기록 작성기 v2 는 단계 셋 (`identity` · `fetch` · `run`) 을 고정해 둔다.

## 2. 만들 것

### I1. 실자료 진입점 `scripts/reil_c4a_run.py` (새 파일 · E 실행기 바이트는 그대로)

- **명령:** `plan-a` (자료 없이 수 · 계획만) · `seal-sources-a` (신뢰 소스 목록 봉인) · `run-a` (실자료 — 실행 요청에서만 쓴다).
- **`run-a` 의 준비:** 환경 identity (`e3a.identity` → `c5.env_identity` 재사용) · 신뢰 소스 집합 대조 (I1 의 `SOURCES_A.json` — §3) · 입력 결속 (§3) · util 적재
  (`c5.load_util`) · 행별 Model · halfcell · 옵션 (C6 `COBYQA_OPTIONS.json` 바이트) · 게이트 (`h.endpoint_gate` · **int 키** — G3) · 배열 (`h.load_phase_a_arrays` +
  고정한 MANIFEST — G4).
- **실행:** `store = hb.new_store()` · `runner = hb.supervise_runner(limits=LIMITS_A, n_workers=4)` · `hb.stage_a(h.units() 의 77 unit 이름, ctx, runner, store, arrays,
  n_workers=4)`. `HStop` (전역 중지) 은 기록하고 끝낸다 — 재시도 0.
- **기록 (`<out>/`):** `HEADER` · `IDENTITY` (시작 · 끝의 소스 · 입력 표) · `ROWS_A` (Phase A 행) · `STORE_A` (I2) · `COUNTS` (§4-1) · `WARNINGS` (I3) · `RULE_A` (I4) ·
  `RESOURCES` · `OPERATION` · `END_RECORD` 의 `.json`. 정확한 이름 집합은 GREEN 에서 고정한다.
- **판정:** 실행 유효성과 실험 결과를 따로 적는다 (§4-1).

### I2. store 저장

- `STORE_A.json` — store 의 JSON 사본 (`planned_units` · `phase_a` · `not_run` · `summaries` · `rho_denominators` · `events` · `next_task_id` · `seq`). 끝 기록 직전과
  전역 중지 때 배타 생성 (임시 → 이름 바꾸기) · sha 를 끝 기록에 넣는다. 읽기 함수 `load_store_a` 를 함께 둔다 (C4-B 에 넘기는 형식 · C4-B 의 사용은 범위 밖).

### I3. 경고 기록 (범위안 v2 §2 의 정책 · `reil_c4_h.py` 최소 변경)

- `_run_local` 의 836–848 행에서 `warnings = msgs[:20]` 는 그대로 두고 두 필드를 더한다: `warnings_n_total = len(caught)` · `warnings_n_distinct = len(msgs)`
  (20 초과면 초과가 보인다). 모르는 옵션 경고 → 구조 중지 (856–859 행) 는 그대로다.
- `run-a` 는 실행들을 가로질러 (형 · 문구) 별 실행 수를 세되 고유 키 50 개까지 · 넘는 것은 `overflow` 수로 남긴다 (`WARNINGS.json`).
- `_assess` 재평가의 경고는 포착 밖으로 둔다 (밝힘). 경고에서 수렴 · 적합성 · 무경고를 주장하지 않는다.
- **이 변경은 C4-0b1 / 0b2 에서 수용된 `reil_c4_h.py` 의 바이트를 바꾼다** — 기존 0b1 / 0b2 시험이 GREEN 이어야 하고, 새 식별값은 실행 요청에서 묶는다.

### I4. Phase A 비용 중단 규칙 `StopRule_A` (C4 v2 131 행의 네 요소)

- **기준 통계:** 그 wave 의 COMPLETED 실행의 c = wall / n_eval 을 오름차순으로 놓은 위쪽 중앙 (0-기반 index ⌊n/2⌋).
- **최소 표본:** 8. **판정 창:** wave 안에서 누적 (완료된 실행 전부 · tick 마다 다시).
- **중지 경계:** `now_rel + (남은 실행 수 × maxfev × c) / 작업자 수 > 그 wave 의 measure 기한` 이면 전역 중지 (엄격한 > · 기록 · 재시도 0). maxfev 는 C6 옵션 값.
- **자원:** 표본 RSS 합 ≤ 4 GiB · 새 산출 ≤ 1 GiB · 디스크 여유 ≥ 5 GiB (C4 v2 §3 공통). v1 의 "중앙 3 배" 예시는 채택하지 않는다.

### I5. C4-A 실행 틀 (새 파일 · E 계열 바이트는 그대로)

- **launcher `scripts/reil_c4a_launch.py`** — v6 의 형식을 따르는 새 파일 · 단계 하나 `phase_a` · 고정 argv (`reil_c4a_run.py run-a …`) · 작업 폴더 `SP/c4a` ·
  자료는 `SP/c4e1/data` 를 읽기만 (U3 · fetch 없음) · `REQUEST` = 이 요청서의 경로 · 새 pycache 폴더 · 사전 / 사후 검사.
- **외곽 · 판정기 · 끝 기록 작성기 v3 초안** (`docs/*_v3_*.py.txt`) — 단계 `phase_a` 를 더한다: 감시 여유 28,800 s · 감시 호출 ≤ 5 (조각 6,600 s) · phase_a 판정
  항목 (§4-2). v2 의 E 단계 동작은 바꾸지 않는다.

### I6. 무자료 시험 — §5.

## 3. 입력 계약 (신뢰 입력 · 실제 소비 바이트 · 옵션 결속)

| 입력 | 식별 | 대조 |
|---|---|---|
| `LFP_Data.xlsx` | 10,841,377 B · `fd50e095…` | 적재 전 크기 · sha (U3 — `SP/c4e1/data` 읽기만) |
| `util_LFP.py` | 33,754 B · `3c19e45e…` | 같음 · `p0.util_static_check` |
| `P0_RESULT.json` | `reil_c4e_run.py` 63–64 행의 고정 sha | sha |
| C6 봉인 | `reil_c6_rebuild_20261013/MANIFEST.json` `4f120948…` | 환경 identity · `COBYQA_OPTIONS.json` · Phase A npy 바이트 (`e3a.check_arrays`) |
| Phase A 배열 | `reil_c4_arrays_20261013/MANIFEST.json` `861c33ac…` (새로 고정) | 정확한 파일 집합 (ARRAYS · MANIFEST · npy 넷) · 파일별 sha |
| E3a 완료 근거 | `evidence/reil_c4e1_20261106/run/` 의 `END_RECORD` · `IDENTITY` · `AGGREGATE` sha · `05_run.judge.json` MATCH | sha · §122 의 수용 범위를 기록에 적는다 |
| 신뢰 소스 | `SOURCES_A.json` — `reil_c4a_run.py` · `reil_c4_h.py` · `reil_c4_hb.py` · `reil_c4_monitor.py` · `reil_c5_pilot.py` · `reil_p0.py` · `reil_c4_e3a.py` (+ import 하면 `reil_c4e_run.py`) | 정확한 집합 · 파일별 sha · bytes |

- H 배열 (`reil_c4_arrays_0b1_20261013` · `d122117f…`) 은 `stage_a` 가 읽지 않으므로 C4-A 의 입력이 아니다 (기록에 "소비 안 함" 으로 적는다 · C4-B 의 입력).
- 시작과 끝에 실제 소비 바이트를 적는다 (E 의 `consumed` 방식). 행마다 받은 옵션 (`options_received`) 이 C6 옵션 바이트와 같은지 대조한다.

## 4. 판정 계약

### 4-1. `run-a` 의 판정

- **수 (범위안 v2 §3-2):** 등록 9,856 (77 × 128) · 조건 제외 (ENDPOINT_GATE · JD_EMPTY_MASK · RHO_PRECONDITION — unit 수와 실행 수 · 이유) · 착수 · COMPLETED ·
  STARTED_INTERRUPTED · NOT_STARTED · `unaccounted_units` 0 · `unaccounted_runs` 0 · `row_count_mismatch` 0 (`plan_counts`). 9,856 이나 7,040 을 "반환해야 정상" 으로
  쓰지 않는다 — H4 22 unit 은 실행 시점의 P0 게이트로 판정한다.
- **unit 완료:** `phase_a_complete` (128 행 · run_id · x0 = 배열). 미완 · 중단을 UNFIT 이나 완료로 바꿔 세지 않는다. UNFIT 은 완료 unit 에만 (원장 1406–1414 행).
- **실행 유효성:** 사전 대조 모두 통과 · 위 세 0 · STORE_A 저장 · 기록 집합 정확 · 소유 정리 끝. **실험 결과:** 범주별 수 · unit 별 완료 / 미완 · 전역 중지 이유.

### 4-2. 판정기의 `phase_a` 항목 (E 단계와 같은 공통 항목 + 아래)

- `run/` 의 파일 집합 정확 · `COUNTS` 의 정합 (계획 unit = 실행 + 미실행 + 미계상 · 실행 수 = 상태별 합) · `STORE_A` sha 가 끝 기록에 있음 · `WARNINGS` 의 상한 준수 ·
  실행 유효성과 실험 결과를 따로 적음.

## 5. 무자료 시험 C4A-T01–T15 (RED 먼저 · 자료 · 실제 최적화 없이)

가짜 util · 가짜 minimize · 합성 입력 · 봉인 배열 (읽기만) 을 쓰는 기존 시험의 방식을 따른다. RED 의 기대 원인 = 골격 (NotImplementedError · 없는 이름).

| ID | 대조 |
|---|---|
| T01 | `plan-a` — 등록 9,856 · 끝점 게이트 22 unit · 계획 7,040 (실제 P0 · 봉인 배열 · util import 없음) |
| T02 | 게이트 키가 int 이고 `stage_a` 와 맞는다 (str 키는 거부) |
| T03 | 입력 sha 불일치 (xlsx · util · P0 · C6 MANIFEST · 배열 MANIFEST · E3a 근거 각각) → 실행 전 fail-closed |
| T04 | Phase A 배열의 npy 와 로컬 MANIFEST 를 함께 바꿔도 잡힌다 (C6 바이트 대조 + 고정 `861c33ac…`) |
| T05 | 신뢰 소스 집합 — 추가 · 누락 · 변경 → 실패 |
| T06 | 상태의 run_id 누락 · 중복 → unit 미완 · 미계상 계수 · 완료 아님 |
| T07 | 시작점 x0 불일치 → 미완 |
| T08 | 정당한 미실행 (ENDPOINT_GATE · JD_EMPTY_MASK · RHO_PRECONDITION) 은 이유와 함께 세고 오류로 보지 않는다 |
| T09 | wave 1 전역 중지 → 기록 · STORE_A 저장 · ρ 진입 없음 · 수 정합 |
| T10 | ρ wave 안의 중지 → 기록 · 뒤 ρ unit 은 `NOT_RUN:RHO_PRECONDITION` |
| T11 | 경고 — 총수 · 고유 수 · 20 초과 표시 · 집계 상한 50 + overflow · 모르는 옵션 → 구조 중지 (기존 동작 유지) |
| T12 | `StopRule_A` — 최소 표본 · 위쪽 중앙 · 엄격한 > 경계 · 중지 기록 (가짜 시계) |
| T13 | `STORE_A` 저장 · 읽기 왕복 일치 · 배타 생성 |
| T14 | launcher `phase_a` — argv 고정 · 자료 sha 사전 검사 (fetch 없음) · 새 pycache 폴더 · timeout · 사후 identity 결속 |
| T15 | 외곽 / 판정기 / 끝 기록 작성기 v3 — 감시 여유 28,800 · 감시 호출 ≤ 5 · phase_a 판정 항목 (fixture) · E 단계 동작 불변 |

- **회귀:** 기존 `tests/test_reil_c4_0a*` · `0b1*` · `0b2*` · `test_reil_c4e*` · `test_reil_c4e1_launch` (· `test_reil_c4e1_runner` 은 환경 변수 없으면 건너뜀) 이 GREEN.

## 6. 구현 절차 (승인 뒤 · 단계마다 첫 예상 밖 결과에서 멈춤)

| 단계 | 내용 | 호출 · 상한 |
|---|---|---|
| a | 승인 기록 § · 보존 규칙 (`evidence/reil_c4a_impl_<D>/**`) | 문서 · Git |
| b | T01–T15 원문 · 골격 커밋 → **RED 1 회** (새 시험만) — 기대: 모두 실패 · 원인 = 골격. 예상 밖 통과는 fixture 가 진실을 가린다는 뜻이므로 멈춤 | pytest 1 회 · ≤ 600 s |
| c | I1–I5 구현 → 정적 자체 검토 → **GREEN 1 회** (새 + 회귀) — 허용 실패 0 | pytest 1 회 · ≤ 1,800 s |
| d | 끝 기록 · 비밀 검사 · 커밋 · push · 결과 § · 결과 검토 발송문 → 멈춤 | 문서 · Git |

- 재시도 0. 실패하면 그 자리의 기록을 커밋하고 결과 §에 적고 멈춘다. 자료 · util 실행 · 실제 최적화 · launcher 의 실제 단계 실행은 0 이다.

## 7. 실행 단계의 시간 배분안 (U2 의 입력 · 숫자는 실행 요청에서 확정)

| 구간 | 값 | 원점 → 닫힘 · 관계 |
|---|---|---|
| 전체 | ≤ 36,000 s (10 h · U2 제안 · 완료 보장 아님) | T_a (a0) → g3 의 push 반환 |
| 착수 창 | ≤ 5,400 s | T_a → phase_a 단계 시작. wrapper 는 `시작 + 28,800 ≤ T_end − R` 일 때만 launcher 를 띄운다 — 이것이 5,400 s 의 역할이다 (a · 탐침 · b · 입력 확인) |
| 단계 (외곽 감시 여유) | 28,800 s (C4 v2 의 단계 8 h) | 단계 시작 기록 → 감시 기한. 준비 · 계산 · 기록 · 소유 정리 모두 이 안 (v2 128 행). launcher 의 자식 timeout 은 탐침 · 기록 git · 정리 공통 기한을 빼서 이보다 작게 두고 같은 값을 복제하지 않는다 |
| `run-a` 안 (`LIMITS_A`) | prep ≤ 900 · 기록 ≤ 900 · 정리 20 s · wave 의 measure 기한 = 단계의 measure 끝까지 남은 시간 (wave 마다 같은 절대 기한) | run-a 원점 |
| unit | 900 s — unit 하나의 첫 실행 시작 → 마지막 실행 끝 (작업자 4 포함) · 넘으면 그 wave 전역 중지 | unit 별 · 단계 합의 상한은 28,800 s 가 묶는다 (900 s 의 합이 아니다) |
| 종결 reserve R | 1,800 s | 단계 감시 기한 → T_end (판정기 · 끝 기록 · 커밋 · push) |

- 착수 창 5,400 s + 단계 28,800 s + R 1,800 s = 36,000 s — 단계 안의 준비 · 정리를 착수 창이나 R 에서 다시 세지 않는다. 비용 중단 규칙 (I4) 은 wave 의 measure
  기한에 대해 작동한다. 외곽 구조 (시작 창 · 감시 조각 6,600 s · 끝 기록 · 반환 기록) 는 E1 과 같다.

## 8. 밝힐 것

1. I3 은 수용된 `reil_c4_h.py` 바이트를 바꾼다 (두 필드 추가). 대안 (바꾸지 않음) 은 실행마다 총수 · 초과 표시가 없어 범위안 v2 §2 의 정책을 채우지 못한다.
2. `_assess` 재평가 경고는 포착 밖이다.
3. 9,856 · 7,040 은 기대 반환 수가 아니다. 실제 수는 실행 뒤 판정한다.
4. 줄 번호는 이 커밋의 파일을 읽어 확인한 것이다. 시험의 정확한 함수 이름 · 기록 파일 이름은 b · c 에서 고정하고 결과 §에 적는다.

## 9. 하지 않는 것

자료 개봉 · 맞춤 · 실제 C4-A 실행 (별도 실행 요청) · C4-B · COMSOL · util · C6 봉인 · 배열 · 기존 증거 · E 계열 바이트의 변경 · 재봉인 · 설치 · 환경 재구축.
