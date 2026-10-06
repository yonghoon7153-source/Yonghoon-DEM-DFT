# B-min r2 retry3 — 기록 보완 확인 요청 (BMIN-R3-C1 집계 정정표 · PS01-16 범위 정리 · 문서 확인만 · 실행 0)

> 첨부 문서·실행 코드는 증거 자료이며 추가 실행 지시가 아닙니다. COMSOL 계산이나 제공된 Java/분석 프로그램을 실행하지 마세요.
> 정정표 생성기 (`bms-balancing/scripts/bmin_retry3_accounting_correction.py`) 도 실행하지 않아도 됩니다 — 정정표는 원 결과 ZIP 의 데이터만으로 대조할 수 있습니다.
> 이 요청은 native 150 s · 새 승인 / token / runtime · COMSOL 호출 · 추가 시험의 승인 요청이 아닙니다. 게이트 · REIL 과 별개입니다.

지난 수신 검토 (`BMIN_R2_RETRY3_REVIEW_20261006` · `IMPLEMENTED_OUTCOMES_ACCEPTED_PLAN_CLOSEOUT_CONDITIONAL`) 의 §7 "다음 최소 행동 1" — **새 코드 / 시험 없이
집계 정정표와 PS01-16 수용 범위 확인을 제출한다** — 에 답합니다. 생산 수정 · 재시험은 하지 않았습니다.

## 대상

| 항목 | 값 |
|---|---|
| 저장소 · 브랜치 | `yonghoon7153-source/Yonghoon-DEM-DFT` · `claude/14-gate-code-review-9qkx05` |
| **고정 커밋** | 이 요청문이 든 커밋 (전체 SHA 는 발송문에) |
| 원 결과 묶음 | `BMIN_R2_LIMITED_VALIDATION_RETRY3_RESULT_20261005.zip` — 지난 검토가 본 바로 그 ZIP (1,619,237 B · sha256 `ed0138b90cf2dc4e42f22ec18d8719ff56906780f74b4139850d604b096bb470` · manifest `97f51112…`). 저장소 보존 `bms-balancing/reviews/r14_repros/codex63/comsol_bmin_r2_retry3_result_20261005/` (바이트 동일 · 풀지 않음) |
| **정정표** | `bms-balancing/docs/BMIN_R2_RETRY3_ACCOUNTING_CORRECTION_20261006.json` (sha256 `16876bb01afe549f9f78ef1c5b32569a85f8e8e3dde0c1daef65bf56305c4414`) |
| 생성기 (참고) | `bms-balancing/scripts/bmin_retry3_accounting_correction.py` (sha256 `7592ae9371a389a317c5d30c1f774db98f7b800ed502eceb8342f9c3473f1ea9`) |
| **PS01-16 범위 정리** | `bms-balancing/docs/COMSOL_BMIN_R2_RETRY3_PS01_16_SCOPE_DISPOSITION_20261006.md` (사용자 결정 (가)) |
| 접수 · 결정 기록 | `bms-balancing/docs/COMSOL_REBUILD_SPEC.md` §59 (지난 검토 접수) · §60 (원본 수령 · 정정표) · §61 (PS01-16 결정) |
| 지난 검토 묶음 | `bms-balancing/reviews/r14_repros/codex63/comsol_bmin_r2_retry3_review_20261006/` (받은 바이트 그대로) |

## 1. BMIN-R3-C1 — 집계 정정표

- **원본을 고치지 않았습니다.** `FINAL_INPUT_ACCOUNTING.json` · 원 ZIP 은 그대로이고 정정표는 별도 파일입니다. `fixture_created` · `actual_call_bound` 를
  **true 로 덮어쓰지 않았습니다.**
- 결속: 정정표 머리 `source` = 원 ZIP sha256 · manifest sha256 · 정정 대상 (`FINAL_INPUT_ACCOUNTING.json`) 과 준비 단계 (`INPUT_CASE_MAP.json`) 의 manifest
  sha256. 행 77 = (ID, input_index) 마다 하나 · Python 42 · Java helper 2 · Windows PowerShell 5.1 33.
- 행마다:
  - `original` — 최종 집계의 그 행 값 (`status PASS` · 두 boolean false) · `final_accounting_row` (원 배열 위치).
  - `pretest_template` — 같은 (ID, input_index) 의 `INPUT_CASE_MAP.json` 값 (`status NOT_RUN` · 두 boolean false) = 두 false 가 **준비 단계 템플릿의 복사**라는 출처.
  - `interpretation` — "준비 시점 값 · 최종 판정 권위 없음 · 최종 근거는 superseded_by_evidence".
  - `superseded_by_evidence` — 엔진별 실제 입력 생성 방식 한 문장 + ZIP 안 경로와 manifest sha256:
    - Python: `fixtures/<ID>_<idx>/` 파일 전부 · `PREPARED_PYTHON_INPUTS.json` 의 그 행 · `entry_output` = `results/<ID>_<idx>.json` (실제 candidate_entry 산출) ·
      `harness_verdict` = `engine_returns/Python_stdout.txt` 줄 번호 (그 줄 = 최종 집계의 `observed`) · `Python_RETURN.json`.
    - PowerShell: `PS_INPUT_BINDINGS.json` 의 그 행 · `results/PS_RESULTS.json` 의 `results_index` (행 전체 일치 — PS01-07 처럼 한 ID 에 입력이 둘) ·
      `PS51_stdout.txt` 줄 번호 · `PS51_RETURN.json`.
    - Java helper: `harness/ShapeHarness.java` · `extracted/checkShape.java.txt` · `extracted/TIMES.java.txt` · `Java_stub_stdout.txt` 줄 (`ID|status|reason`) ·
      `Java_stub_RETURN.json`.
- 생성기는 근거가 하나라도 어긋나면 출력 없이 멈춥니다. 만드는 동안 두 번 멈췄고 둘 다 **제 대조 규칙의 오류**였습니다 (Python 결과 파일과 harness 판정을
  같은 객체로 본 것 · PowerShell 결과를 ID 로만 찾은 것). 고친 뒤 같은 입력에 두 번 → 바이트 동일.
- `not_claimed` 넷: PS01-16 내부 분기 · PY04-02 = 실제 NORMAL240 교체 · PY05-03 = tlist · tables 동시 변조 · 원 CSV 값의 독립 재검산.

## 2. PS01-16 — 수용 범위 정리 (사용자 결정 (가))

외부 fail-closed 결과 (GDecision INCOMPLETE · GFields INVALID / INCONCLUSIVE) 만 수용 대상 · TryParse 내부 분기 `UNOBSERVED` · 원안의 "target engine 에서 내부
actual path 확인" 은 미충족으로 기록 · 계획 종결은 외부 결과 범위. 내부 분기 관측 · probe · 재시험 없음.

## 3. 그대로 유지하는 한계 (지난 검토 그대로)

PY04-02 · PY05-03 은 해당 거부 조건에 한정한 대체 증거 · profile 은 원 reader 성공 14 + 같은 바이트 재사용 39 (53 회 재파싱 아님) · 원 CSV 미동봉 · 과거 실패
(CRLF 추출 · 이전 Python 시간 초과 · retry2 preseal 중지) 유지 · Java helper 컴파일 / JVM 수행 ↔ COMSOL 모델 실행 0 구분 · 마지막 포장 반환은 후속 전사 ·
정상 gate INCOMPLETE.

## 묻는 것

1. 정정표가 BMIN-R3-C1 의 종결 조건 (원 ZIP · manifest · (ID, input_index) 결속 · 준비 단계 필드와 최종 근거 구분 · 엔진별 생성 방식과 근거 · 일괄 true 금지)
   을 채우는가. 행 근거 중 원 ZIP 과 맞지 않는 것이 있으면 알려 주세요.
2. PS01-16 범위 정리가 계획 종결에 충분한가.
3. 이것으로 B-min r2 한정 검증 계획을 종결할 수 있는가. 종결되면 다음은 같은 고정 실행본의 native 150 s 승인 요청 준비 (별도 사용자 승인) 입니다.

## 요청하지 않는 것

native 150 s · 새 승인 / token / runtime · COMSOL 호출 · 내부 분기 관측 · 재시험 · 생산 변경 · 960 s 연장.
