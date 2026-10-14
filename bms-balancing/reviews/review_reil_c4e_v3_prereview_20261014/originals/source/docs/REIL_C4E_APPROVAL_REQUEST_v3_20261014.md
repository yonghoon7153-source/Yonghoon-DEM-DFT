# REIL C4-E (E3a 66 호출) 실행 승인 요청 v3 — 사전 재검토 (v2) 정정 반영 · 2026-10-14

> **승인 요청문이다.** 사용자 결정 전에는 구현 · 자료 반입 · 자료 개봉 · 실행을 하지 않는다 (0 회).
> 앞 판들은 그대로 둔다:
> - v1 (`docs/REIL_C4E_APPROVAL_REQUEST_20261014.md` · sha256 `b1d8953a346f034a4eecbbc695198f58e1deefcb0a1ba9b00fab631b1d41aa75`)
> - v2 (`docs/REIL_C4E_APPROVAL_REQUEST_v2_20261014.md` · sha256 `a4fb202549e6f785080c0e0feab09f930a2f0afd288cb3a3e5005096dd6d8e28`)
>
> 정정의 근거는 두 사전 검토 회신이다 (판정은 둘 다 `REQUEST_REVISION_BEFORE_E0_APPROVAL`):
> - v1 회신 `reviews/review_reil_c4e_prereview_20261014/originals/` (상태 문서 §62)
> - **v2 회신 `reviews/review_reil_c4e_v2_prereview_20261014/originals/` (상태 문서 §64)** — 주요 정정 수용 · 남은 문서 경계 셋
>
> 그 밖의 근거:
> - C4 v2 요청 (`docs/REIL_C4_APPROVAL_REQUEST_v2_20261013.md`) §0 · §1 · §3 · §4-5.
> - 프로토콜 v2 §2 · **v2 §6-3** · 부속 A §3-8 · §6-1.
> - 상태 문서 §57 (7-1 · 7-2 · 7-3) · §60.
>
> 순서: **이 정정판 → 사전 재검토 → 사용자의 E0 별도 승인 → E0 결과 검토 → E1 별도 GO.** "[산술]" 은 우리 계산이고 추정이며 보증이 아니다.

## v2 와 다른 점 (v2 회신 · §64)

| 곳 | 무엇 | 근거 |
|---|---|---|
| §6-2 · §5 끝 | **실제 fork = 기존 10 + 새 5 = 15** (상한 17 그대로). v2 의 11 은 계수 오류였다 — 0a 보완 n3_a · n3_b 는 모사 Process (실제 0) · 0b2 c_8 은 두 파 (2) | C4E-N1-REMAINING |
| §6-2 | COBYQA 14 실행: **내부 목적평가 ≤ 50 (maxfev)** 과 **정상 반환 뒤 독립 재평가 ≤ 1** 을 나눈다 · 보존 util 의 "몇 회" 를 함수별 유한 상한으로 바꾼다 | C4E-N1-REMAINING |
| §3-2 · §4-1 · §4-4 · §4-7 · §4-8 | **최종 수용 = 끝 식별 재해시와 마지막 끝 기록의 저장 · 재읽기까지 포함한 `final_record` 한 번의 최종 snapshot · 같은 산출 루트 크기.** 9,900 s · 10,800 s 의 적용 경계를 고정 · snapshot 뒤 외부 반환은 별도 | C4E-N2-FINAL-BOUNDARY |
| §4-2 · §4-7 | 진행 중 초과는 **중단 요청 대상**으로 기록하고, 최종 drain 뒤 done 이 있으면 원래 COMPLETED · termination 을 보존한다 (초과 기록 · global_stop 유지) · 마지막 drain 에서 받은 행도 늦은 완료 대조 | C4E-N3-FINAL-DRAIN |
| §5 | r_6 (c) 최종 drain 경합 (순수 fixture) · s_3 (d)–(g) 실제 종결 경로의 시간 / 크기 / 쓰기 실패 · 66 returned + global_stop 만 실패 | 위 둘 |

## v1 → v2 에서 바뀐 것 (참고 · v1 회신 · §62)

| 곳 | 무엇 | 근거 |
|---|---|---|
| §0 · §6 · §10 | 새 대조 · `plan-e` 의 계산 0 과 **기존 159 회귀시험의 계산 예외표** (§6-2) 를 분리한다. 0a 보완 시험이 요구하는 env 둘 · outcome 파일을 실행기 명세에 넣는다 | C4E-N1 |
| §11 | "E0 GREEN 이면 바로 E1" 선택지를 지운다 | C4E-N1 |
| §4-7 · §5 | **E3a COMPLETE = 66 모두 `returned` + 기록 · 식별 · 운영 · 최종 기록 조건.** 지역 오류 행은 관측 행으로만 보존한다 | C4E-N2 |
| §3 · §4-2 · §4-3 · §5 | 시간 좌표 (run 원점 · 상대 시각) · 호출당 상한의 계측 구간과 늦은 완료 · 통계 입력 검증 · 비용 판정 원시 근거 · 표현 축소 · grace 뒤 정리 | C4E-N3 |
| §4-6 · §5 | 적재 대조에 **NE · reference 둘**을 더하고, 서로 다른 PE / NE 합성 대조를 둔다. 소비 digest · 선택 인자 · 입력 식별의 시작 / 끝 결속 | C4E-N4 |
| §1 · §9 | util 원바이트 관계 정정 · 원본 크기 33,754 B · 원본 선호 이유 축소 · "v2 §6-3" | M1 |
| §5 · §6 | 대조 15 → **21** (매개변수화 없음 · 21 항목) · 새 fork 세션 · 가짜 평가 수를 다시 봉인한다 | C4E-N1 4 |

## 0. 요약

| 단계 | 내용 | 계산 · 자료 · 네트워크 | 승인 |
|---|---|---|---|
| **E0** | 실행 진입점 `scripts/reil_c4e_run.py` (새) · 감시 `supervise` 의 선택 인자 `stop_rule` · 새 대조 21 · 무자료 계획 건조 | **새 대조 · 건조: 실제 optimizer (pymoo · COBYQA) · 보존 util 사본 · Sobol 생성 · 자료 · 네트워크 0.** GREEN 의 기존 159 는 §6-2 예외표의 계산만 | **이 요청의 결정 1** |
| (E0 검토) | 결과 검토 (구현 · 대조 · 기록 · 반입 방식) | — | 검토자 |
| **E1** | 고정 커밋에서 두 파일 반입 · sha 대조 → 실행 1 회 (66 호출) | 자료 개봉 · 그들 GA / NSGA 실행 · github.com 읽기 | **별도 GO** — E0 검토 수용 뒤, §4 · §7 그대로 |
| C4-A · C4-B | H 분석 | — | **이 승인 밖** (E 승인은 A / B 포괄 승인이 아니다) |

## 1. 지금 사실 (읽기만 · 실행 0)

- **E3a 정의** (v2 §2 · v2 §6-3 · A §6-1 · A §3-8):
  - 노트북 case 표 `{0:[1], 1:[0,1], 2:[2,3], 3:[0,1,2], 4:[0,1,3], 5:[0,1,2,3]}` × 분석 11 행 = 66 최상위 `run_optimization(…, pop_size=50)`.
  - GA 20 seed · NSGA2 · NSGA3 (165 방향).
  - 성공 = 66 완료 + 기록 완비. 수렴 · 실현 가능해 · 참값 일치 · 출판 재현이 아니다.
  - GA 20 seed 의 X · F · G 전부와 NSGA 의 Pareto 집합 전부를 기록하고, 요약 방식은 정하지 않는다 (E3b 미등록).
  - optimizer 호출 275 · 기대 평가 1,501,500 은 계획 산술이다. **현 E3a 는 objective 평가 수를 세고, 내부 optimizer 호출 수는 따로 세지 않는다.**
- **이미 있는 것 (C4-0a · 닫힘):**
  - `scripts/reil_c4_e3a.py` — `run_e3a_call` (지역 오류 → `termination=error` · X / F / G None · `state=COMPLETED` 행 · 286–305 행) · `plan_calls(4)`
    (작업자별 기대 평가 404,500 / 404,500 / 388,000 / 304,500) · `identity` · `notebook_case_table` · `dryrun`.
  - `scripts/reil_c4_monitor.py` — `supervise`:
    - 단계 마감 · RSS · 디스크 표본 · freshness · 구조 중지.
    - done 행 → COMPLETED (194–195 행).
    - 반환에 `global_stop` · `structural` · `owned_alive_after` · `drain_ok` · `exitcodes` · `worker_end` · `worker_deadline` (332–336 행).
    - `final_record` → `record_state` ∈ {COMPLETE · RECORD_INCOMPLETE · OUTPUT_LIMIT_EXCEEDED} · `limit_violations` (344–379 행).
- **없는 것:** 66 호출 실행 진입점 · 호출당 상한 / 비용 규칙을 걸 자리 (감시 252–311 행) · **원자료** (P0 · C5 의 `scratchpad/reil_p0/data_dl/` 이 이
  컨테이너에 없다 — 2026-10-14 제출자 읽기).
- **원자료 식별 (P0 고정 · 상태 문서 §20 · `REIL_P0_APPROVAL_REQUEST_20261006.md` §3):**
  - 출처: `REIL-UConn/Multi-Objective-Optimization-for-Lithium-Ion-Battery-Degradation-Diagnostics` @ `1188c371e5836df4a7e5f5acf336a34ffd4027e6`.
  - `LFP_Data.xlsx`: 10,841,377 B · `fd50e09542be7adb2270963d65a6e7b5ccae1473a512f68462c2dd419d620ee1`.
  - `util_LFP.py` 원본: **33,754 B** · `3c19e45ef8a64ce67cda1f623551e758d4c0f67086bbae02b978428d78de1c76` (CRLF 846 · 끝 줄바꿈 없음).
    - 보존 사본 (`reviews/prereview_pybamm_reil_20261003/external/util_LFP.py.txt`): 32,909 B · `bdf78273…`.
    - **관계 (M1 · 검토자 직접 대조 + 이 저장소에서 메모리 변환으로 재확인):** 원바이트는 줄바꿈 정규화와 끝 LF 차이다. 원본의 CRLF 를 LF 로 바꾸고 끝 LF 하나를
      더하면 사본과 전체 바이트가 같다.
    - 원본 텍스트 사본은 검토 회신 묶음 (`reviews/review_reil_c4e_prereview_20261014/originals/source/original_util/`) 에 보존돼 있다 (MIT · §62).
  - P0 결과 `evidence/reil_p0_20261006/P0_RESULT.json` (`3875e650…`) 에 있는 대조 기준:
    - 분석 11 행: `n_points` · `V_first` · `V_last` · `Q_first` · `Q_exp_max`.
    - **reference 둘** (1087–1110 행): `12-LFP C_20 Updated` · `12-Graphite Half-cell @ C_20` 각각의 sheet · step 6 · cell 1 · `n_points` (1314 · 212) ·
      `V_first` · `V_last` · `Q_first` · `Q_last`.
    - PE: max_q 3.149013767655145 · `n_q_PE_hc` 1313.
    - **NE: `q_NE_hc_max_record_only` 3.6685628130367562.**
- **환경 (2026-10-14 제출자 관측 — 검토자 직접 관측 아님):**
  - C4 봉인 `reil_c6_rebuild_20261013/` · MANIFEST `4f120948…` — identity 통과 (`evidence/reil_c4_0b2_fix_20261014/01`).
  - venv python 3.11.17 · pymoo 0.6.2 · pandas 3.0.5 · openpyxl 3.1.5.
  - 기계: CPU 4 · 메모리 15.7 GiB · 디스크 여유 26.26 GB.
- **선행:** C1-core 충족 (A §6-2) · C4-0a · 0b1 · 0b2 한정 종결 (§60).

## 2. 범위 경계

- **E3a 만 한다.** H (C4-A · C4-B) · E3b · H4 대조 / ray 는 없다.
- pickle (`results/*.pkl`) · 노트북 실행은 없다. 노트북 case 표는 sha 대조한 발췌 (`95cca5f3…`) 에서 읽는다.
- 출판 수치와 비교하지 않는다. 해 선택 (`find_balanced_solution` 등) · 결과 요약도 없다.
- **커밋하지 않는 것:** `LFP_Data.xlsx` (v2 §6-4 — 원자료는 저장소에 넣지 않는다). E1 에서 반입한 util 원본 파일도 다시 커밋하지 않는다 — sha · bytes 만 남긴다
  (원본 텍스트는 이미 검토 증거로 보존돼 있다).
- 실제 H 과학 분석 (C4-A · B) 과, E0 GREEN 안의 기존 H / H4 **합성** 회귀시험 (0b1 · 0b2 계열 — 자료 0) 은 다른 것이다.

## 3. E0 — 바뀌는 파일 (자료 0)

1. **`scripts/reil_c4_monitor.py`** (C4-0a 에서 닫힘) — `supervise(…, stop_rule=None)` 선택 인자 하나:
   - **좌표 계약 (C4E-N3 2):**
     - run 원점은 `supervise` 의 기존 인자 `t0` 다 — 실행기가 run 시작의 monotonic 값을 넘긴다.
     - snapshot = `{now_rel: clock() − t0, started: {task_id: start 사건 t − t0}, done: {task_id: {wall, n_eval, termination}}, progress: {task_id: int}, planned: [task_id…]}`.
     - 모든 시각은 초 · 같은 CLOCK_MONOTONIC (fork 작업자와 공유) 이다.
     - start 사건의 t 는 작업자가 task 를 시작하기 직전의 값이다 (`worker_loop` 167 행). **X · F · G 는 넣지 않는다.**
   - 매 tick (RSS 표본 뒤) 에 `stop_rule(snapshot)` 을 부른다. 문자열을 돌려주면 전역 중지 사유로 쓴다 — `stop.set()` → 신규 시작 0 → 진행 중 작업 종료.
   - `stop_rule` 의 예외는 우리 구조 오류다 (사유 원문 기록).
   - 기본값 None 이면 지금과 같은 동작이다. 근거는 기존 감시 시험 (0a · 0a 보완 · 0b1 보완 · 0b2 c_8) 이다.
2. **`scripts/reil_c4e_run.py`** (새):
   - **`fetch` (E1 전용 · E0 에서는 가짜 로컬 git 저장소로만 시험):**
     1. 저장소 밖의 새 scratch 폴더에서 `git init`.
     2. `git fetch --depth 1 --filter=blob:none <공개 URL> 1188c371…` — 전체 clone · checkout 없음.
     3. `git show 1188c371…:<경로>` 를 **두 경로 (`LFP_Data.xlsx` · `util_LFP.py`) 에만** 쓴다.
     4. 이미 있는 목적지 파일은 거부한다. sha · bytes 를 대조한다.
     5. 정확 argv · cwd · 시각 · 커밋 · 경로 · sha · bytes 를 기록하고, 파일 바이트는 기록하지 않는다.
   - **`plan-e` (E0 건조):** identity · 원천 sha · P0 · 발췌 · 계획 · 규칙 매개변수 · 기대 자료 식별 (두 파일 크기 · sha) → `PLAN_E.json`. util import · 자료 ·
     optimizer · 네트워크 0.
   - **`run` (E1):** 순서가 고정이다.
     1. 원점 t0.
     2. identity · 원천 sha · 두 파일 / P0 / 발췌 / 봉인 MANIFEST 의 **시작 sha**.
     3. 경로 경계: 자료 파일은 저장소 밖이어야 하고, `.pkl` · `.ipynb` 는 거부하고, 출력 폴더는 새로 만든다.
     4. util import → 적재 (11 행 + 반쪽전지 PE / NE).
     5. P0 기록과 정확 대조 (§4-6).
     6. 소비 digest 기록.
     7. 계획 (`e3a.plan_calls(4)`).
     8. `supervise` (stop_rule = §4-2 + §4-3) — 반환 상태는 감시의 마지막 drain 뒤 상태다 (done 우선 · `_states` 194–205 행).
     9. 호출 행 · 운영 필드 · 비용 판정 기록 · 초과 대조 (진행 중 초과 기록 + 모든 COMPLETED 행의 wall · §4-2).
     10. **끝 식별 재해시** (두 파일 · P0 · 발췌 · MANIFEST · 모듈).
     11. 사전 판정 (§4-7 의 조건 1–4 · 6).
     12. **`final_record` 한 번 — 단계 안의 마지막 기록이다** (C4E-N2-FINAL-BOUNDARY):
         - 모든 기록 파일을 쓰고 · 다시 읽고 · 해시한다 — 호출 행 · 상태 · 운영 · 비용 판정 · 식별 표 (기대 · 시작 · 끝) · 끝 기록 (사전 판정과 근거).
         - 그 뒤 같은 산출 루트의 크기와 최종 monotonic snapshot 을 한 번 잰다 (`reil_c4_monitor.py:365–377`).
     13. **최종 판정** = 사전 판정 AND `record_state = COMPLETE` AND `limit_violations` 비어 있음 → stdout.
         - stdout 은 snapshot 뒤의 외부 반환이다. 단계 실행기가 산출 루트 밖의 `<단계>.stdout.log` 로 받는다.
         - 이 반환은 snapshot 에 포함됐다고 하지 않는다. 산출 루트 안에는 새로 쓰지 않는다 (재귀 측정 없음).
   - `e3a.run_e3a_call` · `plan_calls` · `identity` · `notebook_case_table` 를 그대로 쓴다 (`reil_c4_e3a.py` 는 고치지 않는다).
   - 적재는 P0 (`scripts/reil_p0.py:341–380`) 와 C5 (`scripts/reil_c5_pilot.py:871–885`) 의 같은 그들 함수 · 같은 인자다:
     - 11 행: `visualize_LFP_data(sheet = SHEETS_ANALYSIS[i], step_idx = STEP_IDX[i], visualize=False)` → `extract_battery_data(idx = CELL_IDX[i])`.
     - reference: `SHEETS_REF[0 | 1]` · `REF_STEP` 6 · `REF_CELL` 1.
     - halfcell = `[q_PE, v_PE, q_NE, v_NE]`:
       - slice `[argmin(Q) : argmax(Q)]`.
       - 질량 `area = 0.25 π 1.2²` · `LFP_mass_12 = 13.5 area` · `Gr_mass_12 = 5.77 area` · 배율 PE 20.16 · NE 11.4.
3. **`tests/test_reil_c4e.py`** (새) — 대조 원문은 E0 승인 뒤 RED 전에 커밋한다. 목록은 §5.

**바꾸지 않는 것:** `reil_c4_e3a.py` · `reil_c4_h.py` · `reil_c4_hb.py` · `reil_c5_pilot.py` · `reil_p0.py` · `reil_c6_profile.py` · 기존 시험 일곱 · 배열 · 봉인 · 기존 증거.

## 4. E1 의 규칙 — 결과를 보기 전에 지금 고정 (실행 중 바꾸지 않는다)

### 4-1. 단일 원점 · 단계 예산 (C4-E 단계 3 h = 10,800 s)

| 경계 (원점 t0 = `run` 시작 · monotonic · 모든 상대 시각의 원점) | 값 | 넘으면 |
|---|---|---|
| prep (identity · sha · 적재 · 대조 · digest · 계획 — 작업자 시작 전) | t0 + 900 s | 작업자를 시작하지 않고 멈춘다 |
| 측정 마감 (`supervise` 의 measure) | t0 + 9,000 s | 신규 시작 중지 · 진행 중 호출 중단 |
| 정리 (terminate → grace 60 s → kill → join 5 s · 잔존 확인 — 감시 318–325 행) | 측정 마감 뒤 | 잔존 > 0 이면 INCOMPLETE |
| **기록 마감** — `final_record` 의 최종 snapshot (§3-2 의 12: 끝 재해시 · 끝 기록을 포함한 마지막 쓰기 · 재읽기 · 해시 · 용량 조회 **뒤**) | t0 + 9,900 s | RECORD_INCOMPLETE → E3a INCOMPLETE |
| **단계 끝** — run 프로세스의 종료 (최종 판정 stdout 반환 포함) · 단계 실행기의 run timeout | 단계 실행기 시작 + 10,800 s | timed_out → E3a INCOMPLETE |

- 단계 실행기의 원점은 run t0 보다 조금 앞이다 (프로세스 시작 · import). 그래서 10,800 s 판정은 단계 실행기 meta 의 경과 · `timed_out` 으로 하고, run t0 기준
  상대 시각과 더하지 않는다.
- reserve = 10,800 − 9,000 = **1,800 s**:
  - 9,000 → 9,900 s: 중단 · 정리 (grace 뒤 kill / join · 잔존 확인 포함) · 기록 · 끝 재해시 · `final_record`.
  - 9,900 → 10,800 s: 최종 판정 반환 · 프로세스 종료.
  - **grace 60 s 는 모든 정리 완료의 보증이 아니다.**
- 기대 경과 ≈ 35–45 분 [산술 · C5 단가 5.113 ms × 최대 작업자 404,500 평가 ≈ 2,068 s + 초기화 · 기록 · v2 §3 의 추정 · 보증 아님].
- fetch 는 원점 전 별도 단계다 (§7 · 300 s).

### 4-2. 호출당 상한 1,800 s — 계측 구간 · 늦은 완료 (C4E-N3 1)

| 호출 상태 | 계측 | 넘으면 |
|---|---|---|
| 진행 중 (started − done) | `now_rel − started[tid]` (부모 tick 의 clock − 작업자 start 사건 t · 같은 CLOCK_MONOTONIC) | 전역 중지 "호출당 상한 (진행 중 · tid)". 그 호출은 **중단 요청 대상**으로 기록한다 (감지 상대 시각 · 관측 경과). **최종 상태는 감시의 마지막 drain 뒤에 정한다** — done 이 없으면 STARTED_INTERRUPTED · done 이 있으면 원래 COMPLETED 와 termination (returned · error) 을 보존한다. 어느 쪽이든 진행 중 초과 기록과 global_stop 은 취소하지 않는다 |
| 완료 (done) — **늦은 완료** | 그 행의 `wall` (작업자가 `run_e3a_call` 안에서 잰 호출 시간 · 사본 · 계수 준비 포함) | 다음 tick 에서 전역 중지 "호출당 상한 (늦은 완료 · tid)". **반환 행은 그대로 보존한다** (COMPLETED · 원래 termination) · 늦은 완료 목록에 따로 적는다 · 단계 판정 INCOMPLETE |
| **마지막 drain 에서 받은 완료** (C4E-N3-FINAL-DRAIN) | 그 행의 `wall` | 감시가 돌려준 **모든** COMPLETED 행 (마지막 drain 에서 처음 받은 행 포함) 의 wall 을 상한과 대조해 늦은 완료 목록을 완성한다. 이미 걸린 중지 사유는 그대로다 |

- 상태 분류는 감시의 기존 규칙 (done 이 있으면 COMPLETED) 을 그대로 따른다. 규칙 (`stop_rule`) 은 상태를 바꾸지 않고 중지 사유와 초과 기록만 남긴다.
- 이 경합에서도 global_stop 이 남으므로 판정은 INCOMPLETE 다 — 성공 우회가 아니라 원행과 초과 증거를 보존하는 것이다.

- 비교는 엄격한 `>` 다 (1,800 이면 넘지 않음). 중지 신호 뒤에는 새 호출을 시작하지 않는다 (작업자가 시작 직전마다 `stop` 을 본다 · 기존 동작).
- 검사는 tick (1 s) 표본이다 — **1,800.000 s 의 OS 강제 차단 보증이 아니다.** 기록에는 감지 tick 의 상대 시각과 관측 경과를 남긴다.
- 늦은 완료와 진행 중 초과가 같은 tick 에 함께 보이면 사유에 둘 다 적는다 (늦은 완료를 먼저).

### 4-3. 비용 중단 규칙 (비용만 · 결과값 0)

| 항목 | 정의 |
|---|---|
| 집합 | planned = 계획 66 · active = started − done · not-started = planned − started · 작업자 배정 고정 (번호 mod 4) |
| 입력 검증 (C4E-N3 3) | 계산 전에 확인한다: `returned` 행의 wall 은 유한 · ≥ 0, n_eval 은 정수 ≥ 1 · progress 는 정수 ≥ 0 · done ⊆ started ⊆ planned. **하나라도 어긋나면 규칙이 예외를 내고 구조 중지다** — 표본을 임의로 빼거나 0 으로 채우지 않는다 |
| 기준 통계 | 완료 `returned` 호출마다 c_i = wall_i / n_eval_i · 기준 m = **위쪽 중앙 순서통계** (오름차순 정렬 뒤 0-기반 index ⌊n/2⌋ — C5 표기와 같다) |
| 최소 표본 | **8** — 그 전에는 판정하지 않는다 |
| 판정 창 | 누적 (완료된 `returned` 호출 전부) · tick 마다 다시 계산 |
| 투영 | 작업자 w 마다 R_w = (not-started 배정 호출의 기대 평가 합 + active 호출의 max(기대 평가 − progress, 0)) × m |
| 경계 | now_rel + max_w R_w > **9,000 s** 이면 전역 중지 "비용 중단 — 고정 비용 투영 모형에서 측정 마감 초과로 추정" |

- progress 는 평가 **진입** 때 올라가는 관측 진행 proxy 다 (예외로 끝난 평가 포함 · `e3a.py:247–249`). 완료 평가 수가 아니다.
- 기대 평가는 C4-0a 계획의 산술 (pop × 세대 × seed) 이고 한도가 아니다. 실측과의 차이는 호출 행의 `n_eval_minus_expected` 에 남는다.
- [산술] 첫 판정 무렵이라면 m 이 C5 단가의 약 4 배 (≈ 20–22 ms · 판정 시각에 따라) 를 넘어야 걸린다.
- **판정 원시 근거 (C4E-N3 4):** 중지한 판정과 마지막 판정 (정상 종료 때) 마다 기록한다.
  - 상대 시각 · 포함한 `returned` task ID · 표본 수 · 각 wall / n_eval · m.
  - 작업자별 남은 기대 평가 · R_w · 판정값 (now_rel + max R_w) · 경계 · 사유.
  - X · F · G 는 넣지 않는다.
- 이 규칙은 과학 결과를 고르는 데 쓰지 않는다.

### 4-4. 자원 (감시 표본 · C5 · C4 v2 §3 계승)

- RSS 표본 합 ≤ 4 GiB.
- 새 산출 ≤ 1 GiB — run 의 산출 루트 하나 (`evidence/reil_c4e1_<날짜>/run/`).
  - 실행 중에는 감시 (`out_roots`) 가 잰다.
  - 최종 수용은 `final_record` 가 끝 기록까지 쓴 **뒤** 같은 루트를 다시 잰 값이다 (§3-2 의 12).
  - 단계 실행기의 로그 (meta · stdout · stderr · porcelain) 는 이 루트 밖이고 snapshot 뒤에 쓰인다 — 크기는 끝 보고에 따로 적는다.
- 디스크 여유 ≥ 5 GiB (실행 직전 다시 잼) · 두 감시기 freshness (C4-0A-N3).
- 동시 실행 금지 (CPU 4 독점) · 작업자 4 · BLAS 스레드 1.

### 4-5. 중지 조건 — 하나라도 걸리면 그 자리에서 멈추고 미완 기록을 보존한다 (재시도 0)

- 대조 실패: identity · sha · 경로 · 적재 대조 불일치.
- 시간: prep 초과 · 측정 마감 · 호출당 상한 (진행 중 · 늦은 완료).
- 규칙: 비용 중단 · 규칙 입력 검증 실패.
- 실행: 구조 오류 (우리 코드 · 구조 목록) · 작업자 비정상 종료 · Model / halfcell 격리 실패 (호출 뒤 digest 변화).
- 감시: RSS · 디스크 · freshness.

그들 util 의 **지역 오류**는 중지 조건이 아니다. 행으로 남기고 나머지 호출을 계속 관측하되, 판정은 INCOMPLETE 다 (§4-7).

### 4-6. 자료 결속 — 실제 소비 입력 (C4E-N4 · 7-1 의 정신)

- **시작 / 끝 식별:** 두 파일 (xlsx 10,841,377 B · util 33,754 B) · P0 결과 (`3875e650…`) · 노트북 발췌 (`95cca5f3…`) · 봉인 MANIFEST (`4f120948…`) ·
  실행 모듈 · e3a · monitor · c5 · p0.
  - 신뢰 기대 sha 와, 시작 때 실제로 읽은 sha 와, 끝에 다시 해시한 sha 를 한 표에 둔다.
  - 시작과 끝이 다르면 INCOMPLETE 다.
- **적재 정확 대조 (float 동일 · 조정 · 재추출 경로 없음):**
  - 분석 11 행의 `len(Q_exp)` · `V_exp[0]` · `V_exp[-1]` · `Q_exp[0]` · `Q_exp_max`.
  - **reference 둘**의 sheet · step · cell · `n_points` · `V_first` · `V_last` · `Q_first` · `Q_last`.
  - PE: max_q · `n_q_PE_hc`.
  - **NE: q_NE_hc 의 최대 = `q_NE_hc_max_record_only`.**
  - 하나라도 다르면 optimizer 를 부르기 전에 멈춘다.
  - P0 는 3.11.15 venv, C4 는 3.11.17 venv (같은 lock 판) 다.
- **소비 digest · 선택 인자:** 실제로 넘긴 Model 11 개 · halfcell 의 `c5.model_digest` · 시트 · step · cell · 질량 · 배율 · slice 규칙을 기록한다.
  - digest 기록만으로 잘못된 적재가 교정되지는 않는다 — 그래서 E0 의 합성 PE / NE 대조 (d_3) 가 함께 필요하다.
  - P0 에 없던 전체 배열 digest 가 과거에 있었다고 주장하지 않는다.
- **7-1:** E3a 는 우리 Sobol 배열을 쓰지 않는다 (그들 GA / NSGA 의 seed). H 배열의 MANIFEST · NPY + INDEX 동시 변경 의무는 C4-A · C4-B 승인 요청에 남는다 —
  **C4 전체의 7-1 을 닫은 것이 아니다.**

### 4-7. 판정 — 관측 집계와 E3a COMPLETE 를 분리한다 (C4E-N2)

- **관측 집계:** 계획 66 = COMPLETED (`returned` · `error` 따로) + STARTED_INTERRUPTED + NOT_STARTED. 칸이 겹치지 않고, "작업 생성 ≠ 완료" 정의를 이어 쓴다.
- **E3a COMPLETE** = 아래를 **모두** 만족할 때다.
  1. 66 호출 모두 COMPLETED 이고 **`termination = returned`** 다 (지역 오류 0).
  2. C4-0a 의 기록 필드가 모두 있다.
  3. `global_stop` 이 없고 `structural` 이 비어 있다 (호출당 상한 · 비용 중단 · 마감 · 감시 중지 포함).
  4. 작업자 넷 모두 `worker_end` 가 있고, `worker_deadline` 이 없고, `exitcodes` 가 0 이고, `owned_alive_after` 가 0 이고, `drain_ok` 가 참이다.
  5. **최종 기록 수용:** §3-2 의 12 의 `final_record` 가 `record_state = COMPLETE` 이고 `limit_violations` 가 비어 있다. 이 `final_record` 는 끝 식별 재해시와 끝 기록을
     포함한 단계 안의 마지막 쓰기다.
     - 모든 파일의 재읽기 바이트가 같다.
     - 최종 snapshot ≤ 9,900 s.
     - 같은 산출 루트 ≤ 1 GiB.
  6. 시작 / 끝 식별이 같다 (§4-6). 늦은 완료 목록과 진행 중 초과 기록이 비어 있다.
  7. run 프로세스가 단계 끝 (단계 실행기 시작 + 10,800 s) 안에 rc 0 으로 끝나고, 최종 판정을 stdout 으로 돌려준다 (단계 실행기 meta · `timed_out` 거짓).
     - 이 조건은 run 자신이 아니라 단계 실행기 meta 로 판정한다.
     - **단계 판정 = run 의 최종 판정 (1–6) AND 이 조건.** 결과 기록 (§) 에 둘을 함께 적는다.
- 하나라도 어긋나면 **E3a INCOMPLETE** 이고 **C4-A 관문은 false** 다. 완료된 행 · 파일 · 오류는 지우지 않는다 — 단계 판정만 INCOMPLETE 로 둔다.
- **앞선 판정으로 뒤의 실패를 가리지 않는다.** `final_record` 전의 사전 판정은 "사전" 으로만 기록한다. 끝 기록 뒤의 크기 · 시간 초과나 쓰기 · 재읽기 · 식별 실패가 있으면
  E3a COMPLETE 를 확정하지 않는다.
- 수렴 · feasible 해 · `success=True` 는 조건이 아니다. 반환된 X / F / G 의 없음 · 비유한 · G 위반은 기존대로 구분해 기록하고, 성공 기준으로 바꾸지 않는다.
- 지역 오류 행을 H 선행 완료로 인정하는 것은 이 요청의 해석 범위 밖이다 (프로토콜 변경이 필요하다).

### 4-8. 기록 (E1 · `evidence/reil_c4e1_<날짜>/`)

- 착수 기록 · porcelain 시작 / 끝 · 단계 실행기 사본 · identity.
- fetch 기록: argv · cwd · 시각 · 커밋 · 경로 · 목적지 · sha · bytes (파일 자체는 아님).
- 식별 표 (기대 · 시작 · 끝) · 적재 대조 표 · 소비 digest · 선택 인자.
- 호출 행 66: X · F · G 원형 · 계수 · 오류 · 추출 기록 · digest · 경고 계수 · wall · cpu.
- 관측 집계 · 운영 필드 (§4-7 의 3–5) · 비용 판정 원시 근거 · 늦은 완료 목록 · 진행 중 초과 기록 (중단 요청 대상 · 최종 상태) · 중지 원문 · 감시 표본 ·
  시작 / 끝 HEAD · 원천 sha.
- run 산출 루트 안 (모두 `final_record` 로 · §3-2 의 12): 위 기록 파일 · 끝 기록 (사전 판정과 근거).
- run 산출 루트 밖 (snapshot 뒤 외부 반환 · snapshot 에 포함됐다고 하지 않음): 최종 판정 (stdout → `<단계>.stdout.log`) · 단계 실행기 meta · 끝 보고.
- 끝 보고에는 커밋 · push · 문서 전 snapshot 이라고 표시한다.
- 결과 요약 · 출판 비교 · 해 선택은 하지 않는다.

## 5. E0 대조 목록 — 21 ID (매개변수화 없음 · 21 항목 · 원문은 E0 승인 뒤 RED 전에 커밋)

| ID | 단언 |
|---|---|
| m_1 | `stop_rule=None` → 기존 동작 (기존 감시 시험이 근거) · 규칙이 사유를 돌려주면 전역 중지 · 세 상태 · 사유 원문 (fork 세션 1) |
| m_2 | snapshot 좌표: 0 이 아닌 t0 와 가짜 clock 에서 now_rel = clock − t0 · started = start.t − t0 · 내용은 §3-1 의 키뿐 (X · F · G 없음) · 규칙 예외 → 우리 구조 오류 |
| r_1 | 호출당 상한 (순수 함수): 진행 중 초과 · **표본 사이 늦은 완료** (직전 1,799.5 → wall 1,800.2) · 같음 (1,800.0) 은 넘지 않음 · 사유 문구 |
| r_2 | 비용 규칙 (순수 함수): 위쪽 중앙 순서통계 · `returned` 만 · 7 이면 판정 없음 · 8 번째부터 · 작업자별 투영 (active 의 progress 반영) · 경계 같음 / 넘음 |
| r_3 | 비용 규칙이 결과값을 읽지 않는다 — 접근하면 예외인 X · F · G 를 넣어도 판정이 같다 |
| r_4 | 입력 검증: wall NaN · 음수 · n_eval 0 · 정수 아님 · progress 음수 · 계획 밖 ID · done ⊄ started → 예외 (빼기 · 0 채우기 없음) |
| r_5 | 판정 원시 근거: 중지 판정과 마지막 판정의 기록 키 (§4-3) 가 모두 있고 X · F · G 키가 없다 |
| r_6 | 상한의 세 경로. (a) **fork:** 진행 중 초과 → 중단 요청 대상 기록 → 최종 drain 에 done 없음 → STARTED_INTERRUPTED. (b) **fork:** tick 사이 늦은 완료 → 다음 tick 전역 중지 · 반환 행 보존 (COMPLETED · returned) · 늦은 완료 목록 · INCOMPLETE. (c) **순수 집계 fixture (fork 없음 · C4E-N3-FINAL-DRAIN):** 진행 중 초과 감지 → 중지 요청 → **마지막 drain 에서만** done 수신 (returned 변형 · error 변형) → 원래 COMPLETED · termination 보존 · 진행 중 초과 기록 · global_stop 유지 · 그 행의 wall 이 상한을 넘으면 늦은 완료 목록에도 들어감 · INCOMPLETE (fork 세션 2) |
| t_1 | 0 이 아닌 run 원점 (가짜 clock): prep 초과 → 작업자 시작 0 · 측정 마감 상대 계산 · 중지 신호 뒤 신규 시작 0 |
| d_1 | 순서: identity → 원천 sha → 두 파일 · P0 · 발췌 · MANIFEST sha → 경로 → util import → 적재. 앞에서 어긋나면 뒤 (가짜 util 의 적재 함수) 는 불리지 않는다 |
| d_2 | 적재 대조: 11 행 · reference 둘 · PE max_q / 길이 · **NE 최대** 가 정확 일치면 통과. 어느 한 값 (NE 포함) 이 1 ulp 달라도 optimizer 0 으로 멈춘다 |
| d_3 | **PE / NE 합성 대조:** 시트마다 다른 곡선을 주는 가짜 util → halfcell 이 정확히 `[q_PE, v_PE, q_NE, v_NE]` (slice · 질량 · 배율 20.16 / 11.4 를 시험이 따로 계산해 대조) · PE 를 NE 자리에 둔 적재는 실패 |
| d_4 | 경로: 저장소 안 자료 · `.pkl` · `.ipynb` · 이미 있는 출력 폴더 · 이미 있는 fetch 목적지 거부 |
| d_5 | fetch: 가짜 로컬 git 저장소 (tmp) 의 고정 커밋에서 두 경로만 · 다른 경로 요청 거부 · sha / bytes 불일치 → 멈춤 · 기록에 argv · cwd · 시각 · sha · bytes (파일 바이트 없음) · 네트워크 0 |
| d_6 | 식별 결속: 시작 / 끝 sha 표 (두 파일 · P0 · 발췌 · MANIFEST · 모듈) · 시작과 끝이 다르면 INCOMPLETE · 소비 digest · 선택 인자 기록 |
| s_1 | 계획 = C4-0a `plan_calls(4)` (66 · 번호 · 작업자 · 알고리즘 · 기대 평가) |
| s_2 | 판정: 66 `returned` + 필드 + 운영 + 최종 기록 + 식별 → COMPLETE · **지역 오류 1** → INCOMPLETE (관측 집계에는 COMPLETED · error) · C4-A 관문 false |
| s_3 | 운영 · 최종 기록 — 66 returned 뒤 각각 INCOMPLETE · 행 · 파일 보존. 운영 (합성 supervise 반환 · 순수 판정): (a) 작업자 exitcode ≠ 0 (b) `owned_alive_after` > 0 (c) `drain_ok` 거짓 (f) global_stop (freshness) 만 실패. **실제 종결 경로** (실행기의 종결 함수 · 가짜 clock · 작은 크기 한도 — `record_state` 를 직접 넣지 않는다): (d) 끝 식별 재해시가 늦어 최종 snapshot 이 기록 마감을 넘음 → RECORD_INCOMPLETE (e) 마지막 끝 기록이 같은 산출 루트를 크기 한도 위로 올림 → OUTPUT_LIMIT_EXCEEDED (g) 끝 기록 쓰기 · 재읽기 실패 → RECORD_INCOMPLETE. 어느 경우도 앞선 사전 판정이 COMPLETE 를 확정하지 않는다 |
| s_4 | 끝-끝 합성: 가짜 util (GA / NSGA2 / NSGA3 꼴의 반환 · 최적화 없음) · 가짜 xlsx 경로 · fork 작업자 → 66 returned COMPLETE · 지역 오류 하나 섞인 변형 → INCOMPLETE (fork 세션 2) |
| s_5 | `plan-e` 건조: `PLAN_E.json` 하나 · util import · 자료 · optimizer · 네트워크 0 · 규칙 매개변수 (§4) · 기대 자료 식별 (두 파일 크기 · sha) |
| s_6 | 관측 집계: 66 = COMPLETED (returned · error) + STARTED_INTERRUPTED + NOT_STARTED · 칸이 겹치지 않음 · 합 = 66 |

- 새 실제 fork 세션 = m_1 1 + r_6 (a)(b) 2 + s_4 2 = **5** (세션 공유 없음 · 상한 6). r_6 (c) 와 s_3 은 fork 가 없다 (순수 fixture · 가짜 clock).
- 21 ID · 21 항목은 그대로다 (r_6 · s_3 의 하위 사례는 같은 시험 안에서 단언한다).
- 새 가짜 util 평가 ≤ 2,000 (s_4 두 변형 · r_6 · m_1 포함).
- 실제 pymoo · 실제 COBYQA · 보존 util 사본 · Sobol 생성 · 자료 · 네트워크는 새 대조에서 0 이다.

## 6. E0 — 실행 순서 · 배정 (승인하면)

### 6-1. 순서

1. 보존 규칙 (`evidence/reil_c4e0_20261014/** -text`) · 승인 기록 커밋 → 착수 기록 (폴더가 있으면 중지).
2. identity 1 회 (60 s).
3. 대조 원문 + 새 모듈 골격 커밋 → **RED 1 회 (600 s)** — 새 시험만.
   - RED 예상: **21 모두 실패.** 종류는 둘뿐이다 — 새 모듈 골격의 NotImplementedError, 또는 지금 감시에 `stop_rule` 인자가 없어서 나는 TypeError.
   - 다른 종류가 나오거나 무관한 하네스 실패면 원문을 보존하고 멈춘다.
   - RED 의 한계 (골격 · 인터페이스 수준) 는 0b2 와 같다. 틀린 구현을 잡는 증거는 GREEN 의 음성 대조다.
4. 구현 → 정적 검토 (ast · 이름 · 모듈 속성) → **GREEN 1 회 (600 s)**.
   - 대상: 기존 C4 시험 159 (0a 26 · 0a 보완 14 · 0b1 71 · 0b2 48) + 새 21 = **180**.
   - env: 단계 실행기가 GREEN 자식에 `REIL_C4_FIX_EVIDENCE=<E0 증거 폴더>` · `REIL_C4_FIX_STEP=03_green` 을 준다.
   - 0a 보완 시험 `test_out` (`test_reil_c4_0a_fix.py:387–405`) 이 `03_green.nsga2_synthetic_outcome.json` 을 쓴다. GREEN 전에 없어야 하고, 증거로 커밋한다.
   - 기존 시험은 고치지 않는다.
5. **`plan-e` 건조 1 회 (300 s)**.
6. 끝 기록 · 비밀 검사 · 커밋 · push · 결과 기록 · 검토 발송문을 쓰고 멈춘다.

- **배정:** 계산 1,560 s (60 + 600 + 600 + 300) · 전체 작업 4 h · 자동 재시험 0.
- **자원:** 사후 관측 (최대 단일 자식 RSS ≤ 4 GiB · 증거 ≤ 64 MiB · 착수 때 디스크 ≥ 5 GiB).
- **참고:** 직전 같은 계열 GREEN 은 0a 보완 40 시험 18.3 s · 0b2 보완 119 시험 26.8 s 였다 (기록값 · 보증 아님).

### 6-2. 기존 159 회귀시험의 계산 예외표 (이번 GREEN 1 회에만 적용 · C4E-N1)

과거 승인이 자동 재실행 권한은 아니다. 아래는 **이번 GREEN 1 회**에 대해 새로 묻는 예외다. 출처 칸은 그 계산이 처음 승인된 문서다.

| 범주 | 시험 (파일 : 행) | 이번 횟수 · 상한 | 처음 승인 |
|---|---|---|---|
| 보존 util 사본 + 실제 pymoo NSGA2 · 합성 곡선 | `test_reil_c4_0a.py:349–364` (test_07) · `test_reil_c4_0a_fix.py:387–405` (test_out) | **2 호출 · 호출당 ≤ 5,000 평가** (expected_evals · 시험 단언) · 직전 실측 6.17 s (`evidence/reil_c4_0a_fix_20261013/03_green.nsga2_synthetic_outcome.json`) | C4 v2 §4-5 (`REIL_C4_APPROVAL_REQUEST_v2_20261013.md`) · 0a 보완 요청 (`REIL_C4_0A_FIX_APPROVAL_REQUEST_20261013.md` · `11822e6f…`) |
| 실제 SciPy COBYQA · 가짜 목적 · 건조 옵션 (maxfev 50 · maxiter 100) | 0b1 test_08 (5) · 0b1 보완 n1_a · n1_b · n1_d (3) · 0b1 보완 2 r1_e (1 · 모르는 옵션 경고 경로) · 0b2 p_2 ×3 · s_3 · n_2 (5) | **14 실행 · 실행당 내부 목적평가 ≤ 50** (maxfev · `reil_c4_h.py:840–841`) **· 정상 반환 뒤 독립 재평가 ≤ 1** (`_assess` → `_evaluate` · `:781` · `:875`) — 둘을 섞지 않는다 · 14 × 50 은 내부의 보수 상한이고 전체 목적 호출 상한이 아니다 | 0b1 보완 요청 §5 (`2612086b…`) · 0b1 보완 2 요청 §4 · 0b2 확인 요청 §5 · 결과 §56 |
| 보존 util 사본 · 합성 곡선 · 최적화 없음 | 0b1 test_06 · 0b2 h_1–h_4 | **0b1 test_06:** `extract_battery_data` ≤ 5 · `objective_fun` ≤ 3 · `dVdQ_hc` ≤ 9. **0b2 h_1–h_4:** `extract_battery_data` ≤ 4 · `objective_fun` 0 · `dVdQ_hc` ≤ 48. 중첩 진입을 함수마다 따로 센 정적 상한이고 서로 더하지 않는다 · optimizer 0. 0b2 의 기존 "≤ 120" · §56 의 "22" 는 최상위 호출 단위 (extract 4 · J_V^s 6 · n_out 9 · V_full 3) 다 | 0b1 보완 요청 §5 · 0b2 확인 요청 §5 · v2 재검토 회신 (§64) |
| 가짜 minimize (최적화기 없음) · 가짜 util 평가 | 0b1 보완 8 · 0b1 보완 2 4 · 0b2 ≤ 982 (명목 격자 402 는 독립 칸) · 0b2 보완 1 | ≤ 995 호출 · 가짜 util 평가는 각 승인표대로 | 각 요청 · §57 정정 |
| Sobol 생성 · 재생성 · 임시 봉인 (**pytest 임시 폴더에만**) | 0a test_05 ×3 · test_09 · 0a 보완 n1_a–n1_c · 0b1 test_05 ×3 · test_10 ×2 · 0b1 보완 a1_a–a1_c — **15 시험** | 등록 배열 디렉터리 (`reil_c4_arrays_20261013/` · `reil_c4_arrays_0b1_20261013/`) · 봉인 · 원자료 쓰기 0 · 읽기만 | C4 v2 §4-3 · §4-5 · 0a 보완 요청 · 0b1 확인 요청 (`b769102a…`) · 0b1 보완 요청 §5 |
| **실제** fork 작업자 세션 | 0a test_02 ×3 · 0a 보완 n4_b · 0b1 보완 n1_a · n1_d · n2_d · 0b1 보완 2 r1_b · 0b2 c_8 (1 파 + ρ 파 = 2 · `reil_c4_hb.py:1105` · `:1165`) — 0a 보완 n3_a · n3_b 는 모사 Process (`_ScriptedProc` · 실제 프로세스 0) | **기존 10 세션 + 새 5 = GREEN 15 · 상한 17** | 각 요청 |
| 기록 파일 | 0a 보완 test_out → `<E0 증거>/03_green.nsga2_synthetic_outcome.json` | 1 (없어야 · 보존) | 0a 보완 요청 |
| H / H4 합성 회귀 | 0b1 · 0b1 보완 · 0b2 · 0b2 보완 전부 | 자료 0 · 합성 입력 — 실제 H 과학 분석이 아니다 | 각 요청 |

- **실패 중지:** GREEN 600 s 를 넘거나, 예상 밖 실패가 나거나, 위 상한을 넘는 정적 집계가 나오면 원문을 보존하고 멈춘다 (자동 수정 · 재시험 0).
- 위 횟수는 시험 구조의 정적 집계다 (실행별 계수 로그가 아니다 — 이전과 같다).
- 기존 정식 배열 봉인 · 원자료를 바꿀 권한으로 넓히지 않는다.

## 7. E1 — 별도 GO 뒤의 순서 (지금 승인하지 않는다)

1. 승인 기록 · 보존 규칙 커밋 → 착수 기록 (증거 폴더가 있으면 중지).
2. REIL 공개 저장소의 git 읽기 경로를 확보한다 (세션에 그 저장소 읽기를 붙인다). 안 되면 멈춘다 — 다른 출처 (자료 페이지 등) 로 대신하지 않는다.
3. **fetch 1 회 (300 s)** — E0 에서 시험하고 E0 결과에 고정한 방식 · argv 그대로. 두 파일 · sha · bytes 대조. 불일치면 멈춘다.
4. identity (60 s) → **run 1 회 (단계 실행기 timeout 10,800 s · §4-1)** — 배경 실행 · 진행 감시 · 중간 개입 0.
5. 끝 기록 · 비밀 검사 · 커밋 (xlsx · util 원본 파일 제외) · push · 결과 기록 · 검토 발송문.

- 전체 작업 6 h · 재시도 0 · 예산 변경 0.
- 결과가 INCOMPLETE 여도 그대로 보고하고 멈춘다. 다시 돌리는 것은 새 승인이다.

## 8. 조건 대응 (§57 · §60 · §62) — 닫힘으로 표시하지 않는다

| 조건 | 이 요청에서 |
|---|---|
| 7-1 | E3a 는 실제 소비 입력을 결속한다 (§4-6 · d_2 · d_3 · d_6). H 배열의 MANIFEST · NPY + INDEX 동시 변경 의무는 C4-A · C4-B 승인 요청에 남는다 — C4 전체 7-1 은 열린 채다 |
| 7-2 | C4-E 에 H4 가 없다 → 의무는 C4-B 경계에 남는다 (해소 아님) |
| 7-3 | E3a 범위 (§2) · 비용 측정 용도 · 조기 중지 (§4-2 · §4-3) · reserve · 단일 원점 (§4-1) · HEAD / 파일 목록 · lock / P0 식별 (§4-6 · §4-8) · 부분 / 중단 결과 (§4-7 · §4-8) · 최종 전달 경계 (§4-8 snapshot) — 검토 판단 대상이고 이 문서가 닫았다고 표시하지 않는다 |
| C4-A / B 분리 | E 승인은 A / B 포괄 승인이 아니다. C4-A 는 E3a COMPLETE (§4-7) 기록과 입력 계약 · C4-B 는 등록 탐색 · 판독 · 배열 인증 · 중단 집계를 따로 확인 |
| 인계할 보고 정의 | 작업 생성 ≠ 완료 · 관측 COMPLETED ≠ E3a COMPLETE (이번) · UNFIT 은 완료 단위에만 (C4-A) · support ≠ grades · grid_t ≠ 실제 h_k (C4-B) |
| 유지 | ray 유보 · H4 gate · ν · seed · 기존 배열 불변 · 기존 실패 · 누락 · 승인 이탈 기록 |

## 9. 밝힐 것

1. **감시 모듈 (닫힌 파일) 을 고친다.** 선택 인자 하나이고 기본 동작은 그대로다. 작업자가 fork 프로세스라 시작 시각 · 진행 수는 부모의 감시 루프 안에서만 보인다 —
   그래서 호출당 상한과 비용 규칙을 감시 밖에서 걸 방법이 없다.
2. **원자료를 다시 반입한다.** 컨테이너가 바뀌어 사라졌다 (제출자 관측). 같은 고정 커밋 · 같은 sha · 같은 크기이고, 다른 출처는 쓰지 않는다. 전체 clone 은 하지 않는다.
3. **util 은 고정 커밋의 원본 (`3c19e45e…` · 33,754 B) 을 쓰자고 권한다.** 이유는 P0 · C5 가 쓴 것과 같은 바이트라는 것 하나다. 오류 위치 판정은 실제 로드 경로
   (`ctx.util_file`) 와 비교하므로 사본을 써도 분류에 불이익은 없다 (v1 §9-3 의 이유는 틀렸다 · M1).
4. 비용 규칙의 입력인 기대 평가는 산술이다. 비용 추정은 C5 단가 기반이고 보증이 아니다 (C5 는 3.11.15 환경).
5. 노트북과 다른 점 둘 (C4-0a §40-4) 은 그대로다 — 호출마다 깊은 사본 · case 순 실행.
6. GREEN 의 0a 계열 시험은 0a 보완 (§44) 뒤 처음 다시 돈다 — 0b1 · 0b2 GREEN 은 0a 파일을 넣지 않았다. 감시 모듈을 고치기 때문에 이번에는 넣는다.
7. v1 의 사실 오류 둘을 고쳤다: util 바이트 관계 (M1 — 위 §20 의 같은 문구도 §62 에서 정정) · "부속 A §6-3" → v2 §6-3.
   v2 의 계수 오류 하나를 고쳤다: 기존 fork 11 → **10** (모사 Process 둘을 셌고 c_8 의 두 파를 1 로 셌다 · §64).
8. RED / GREEN 은 C4-0 전체로 각 8 회가 된다 (E0 을 더해서).

## 10. 하지 않는 것

H (C4-A · C4-B) · E3b · H4 대조 / ray · pickle · 노트북 실행 · 출판 비교 · 해 선택 · 결과 요약 · 재시도 · 실행 중 예산 변경 · 설치 · 환경 재구축 · 정식 배열 재봉인 ·
원자료 커밋 · 전체 clone · COMSOL. E0 의 새 대조 · 건조에서 실제 optimizer · 보존 util 사본 · Sobol 생성 · 자료 · 네트워크 (§6-2 의 기존 회귀 예외는 따로).

## 11. 정하실 것

1. **E0 승인** (§3 · §5 · §6 — 예외표 §6-2 포함). E1 은 E0 결과 검토 뒤 별도 GO 다 (이번 요청의 고정 순서 · 선택지 없음).
2. **비용 중단 규칙 — 투영 규칙 (§4-3 · 권장)** / 측정 마감 · 호출당 상한만 (단순하지만 v2 §3 의 "기준 통계 · 최소 표본 · 판정 창" 요구를 채우지 못한다).
3. **util — 고정 커밋 원본 (권장 · P0 · C5 와 같은 바이트)** / 보존 사본.
4. **코드 위치 — 새 모듈 + 감시 선택 인자 (권장)** / `reil_c4_e3a.py` 에 진입점 추가 (닫힌 파일 둘을 고치게 된다).

(v1 §11-4 의 "COMPLETE 정의" 는 선택지에서 뺐다 — 검토 회신대로 66 `returned` 로 고정한다.)
