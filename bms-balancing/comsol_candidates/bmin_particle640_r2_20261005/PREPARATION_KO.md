# B-min 오프라인 후보 r2 — 재검토의 국소 보완 (BMIN-R1-N1 · C1 문구 · 검증안 보강)

상태: **r2 작성 · 정적 대조만 함 · 변경부 기능 검증 미실행 · native 미승인.** 후보 코드의 import · 구문 해석 · 컴파일 · 실행, JVM · COMSOL 호출은 0 회다.
모든 승인 플래그는 false.

근거: r1 (`../bmin_particle640_r1_20261005/` · manifest `9dcb47f0…` · 고정 커밋 `741dde19b`) 의 재검토 회신 `LOCAL_CORRECTION_REQUIRED`
(`reviews/r14_repros/codex63/comsol_bmin_r1_review_20261005/` · SPEC §54) 와 사용자의 국소 보완 지시 (§54-3 — §45 범위 안). 검토자가 정한 범위 그대로
DOF 한 줄 파싱 · 해당 검증안 · C1 문구 / 분류 · 변경표 · manifest · 참조 결속만 고쳤다. Java · entry · 부모 · CONTRACT · 물리 · 수치 허용치 · 시간 /
좌표 · 기준 파일은 r1 그대로다 (바이트 동일).

## 1. 식별

| 항목 | 값 |
|---|---|
| r2 CODE_MANIFEST SHA-256 | **`4cdca2e6bf7d073f813d97be73825b8cd2043c2fc44e285f4a190bc6fb97cf25`** (이전 = r1 `9dcb47f0…`) |
| run_id · 실행 기계 root | r1 · v1 과 같다 — `bmin_particle640_candidate_001` · `outputs/bmin_particle640_offline_preparation_20261004/` (r1 도 배치 · 승인된 적이 없다 · 승인은 manifest SHA 에 결속) |
| 바뀐 파일 | `src/diagnostic_consumer.py` (CRLF · 26,065 → 26,394 B · `mesh_evidence` 안 두 자리) · 봉인 셋 (`CODE_MANIFEST` · `COMMAND_MAP` · `NATIVE_APPROVAL_FIELD_SPEC` — manifest SHA) |
| 그대로 | `src/Bmin640Candidate.java` · `src/candidate_entry.py` · `PARENT_COMMAND.ps1` · `CONTRACT.json` (r1 과 바이트 동일) |
| r1 · v1 문서 중 그대로 유효 | v1 `BASELINE_IDENTITIES.json` · `RESOURCE_BUDGET_KO.md` · `LITERAL_CHANGE_MAP.json` · `CHANGE_BOUNDARIES.json` (NORMAL480 → v1) · r1 `R1_CHANGE_BOUNDARIES.json` · `R1_LITERAL_CHANGES.json` (v1 → r1) — r2 는 그 위의 국소 변경이다. r1 의 C1 문구 (`c1_wording` · 검증안 PS01-16) 는 아래 §2 로 정정한다 |

## 2. 무엇을 고쳤나

| 발견 | r2 의 변경 | 자리 |
|---|---|---|
| **BMIN-R1-N1** (P2) — `mesh_evidence` 가 DOF 문구를 포함한 **줄** 수만 세고 `re.search` 로 그 줄의 첫 부분 일치를 받아, 한 줄에 서로 다른 두 문장 (79485 · 156925) 이나 정상 문장 + 불완전 꼬리가 붙어도 첫 값을 채택했다 | 단일 후보 줄을 **전체 줄**로 대조한다: `re.fullmatch(r'\s*'+pattern+r'\s*', 줄)` — 앞뒤 공백은 허용하고, 같은 줄의 두 번째 문장 · 불완전 문장 · 그 밖의 꼬리 문자는 `TRANSIENT_DOF_READBACK_FORMAT` (I-3 미완) 이다. 줄 수 (`_COUNT`) · 구간 표식 · solved > 0 (`_VALUE`) · 구간 밖 기록 · **예상 156,925+12 와 다른 유효값은 기록만** (값 · 차이 · `review_note`) 은 그대로다. 결과의 `dof_policy` 문구도 같은 규칙으로 고쳤다 | consumer `mesh_evidence` 의 두 줄 (`R2_LITERAL_CHANGES.json`) |
| **C1** (비차단) — "31 significant digits" | `0.001000000000000000000000000001` 은 **소수점 아래 30 자리 · 유효숫자 28 자리**다. r1 의 "31 significant digits" (검증안 PS01-16 · `R1_CHANGE_BOUNDARIES.json` `c1_wording`) 를 r2 검증안 · `R2_CHANGE_BOUNDARIES.json` 에서 정정했다. r1 PREPARATION 의 "(.NET decimal 의 28 자리를 넘는다)" 는 유효숫자가 아니라 **소수 자리 (scale) 상한 28** 을 넘는다는 뜻이다. PS01-16 은 정확한 등호 사례가 아니므로 `value exactly equal to a limit` 목록에서 빼고 `precision_mismatch_items` (긴 소수의 부모 / consumer 불일치 → INCOMPLETE) 로 분류했다 — 정확 등호는 PY01-02 · PS01-04 가 맡는다. 실제 경로 (반올림인가 해석 실패인가) 는 목표 엔진에서 확인한다 · 임의 정밀도 십진 비교 보증이 아니다 | 검증안 · 변경 경계 · 이 문서 |
| 검증안 보강 (재검토 Q4) | 아래 §5 — 같은 줄 두 문장 / 정상 + 불완전 꼬리 · 공백 허용 양성 · consumer solved = 0 · `GNativeAxis` 실패 원인별 사례 · 총수 · 예산 · 봉인 항목 | `LIMITED_VALIDATION_PLAN.json` |

**재검토가 수용한 것 (바꾸지 않음):** BMIN-N1 의 종료 축 분리 (준비 수준 수용 — "독립" 은 같은 consumer 의 구조화된 종료 증거를 부모가 별도 조건으로
소비한다는 뜻이고 원시 native 로그의 독립 측정이 아니다) · entry rc 1 → `NOT_ESTABLISHED` / `NATIVE_CHILD_RC` 의 보수적 한계 (entry 변경 요구 없음 ·
"solver 실패 확인" 으로 쓰지 않는다 · 원래 오류는 `NATIVE_STATE.json` 에 남는다).

**알려 둔 한계 (r2 에서 새로):** 전체 줄 문법은 batch 로그가 DOF 문장을 줄 전체로 (앞뒤 공백만 허용) 쓴다고 본다 — 재검토가 인용한 NORMAL480
`batch.log` 131행이 그렇다. 시각 같은 접두어가 붙는 로그라면 정상 실행이 I-3 미완이 된다 (거짓 음성 · fail-closed 쪽). 우리는 원 로그가 없어
재검토 요청문 Q1 에서 그 줄의 원문 확인을 부탁한다.

## 3. 정적 대조 (`STATIC_AUDIT.json` · `tools/static_audit_r2.py`)

- r1 꾸러미 = 검토받은 커밋 `741dde19b` 의 바이트 · r1 의 정적 대조 (42 항목 — 그 안에서 v1 의 81 항목도 다시 돈다) 를 다시 돌려 r1 → v1 → NORMAL480
  사슬이 그대로임 · 두 결과 파일도 바이트 그대로.
- **r2 → r1 역재구성:** `R2_CHANGE_BOUNDARIES.json` 의 선언 변경 (consumer 의 두 문자열) 만 되돌리면 consumer 가 r1 바이트와 정확히 같다 · Java · entry ·
  부모 · CONTRACT 는 바이트 동일 · consumer 는 `mesh_evidence` 외 모든 함수가 r1 과 바이트 동일 · COMMAND_MAP · FIELD_SPEC 은 manifest SHA 만 다르다.
- **문자열 모형** (감사 도구 자신의 정규식 — 후보 소스의 다섯 문장과 글자가 같은지만 본다 · 후보 실행 아님): 재검토의 여섯 사례 (`valid` · `two_lines` ·
  `two_same_line` · `valid_then_malformed_same_line` · `zero` · `missing_internal`) 와 r2 사례 셋 (공백 둘린 줄 · 꼬리 문자 · NORMAL480 131행 원문) 의
  r2 규칙 이유가 기대와 같다 · r1 규칙에서는 같은 줄 두 사례가 첫 값 79485 를 받았음을 다시 보인다 (재검토 지적의 재현).
- 검증안 · 문서가 r2 manifest 에 결속 · 수 · 예산 · 원인별 사례 · C1 문구.

재현: r2 꾸러미 루트에서 `python3 tools/build_candidate_r2.py --check` · `python3 tools/static_audit_r2.py`.

## 4. 판정 문장 (SPEC §44-2 그대로)

한도와 같으면 허용한다 (≤). 모든 유효 조건이 성립할 때 max \|ΔV\| ≤ 0.001 V **그리고** 두 전극 max \|Δx_surface\| ≤ 1e−4 이면
`WITHIN_LIMITS_THIS_WINDOW`, 어느 하나라도 **엄격히 크면** `EXCEEDS_LIMITS` 다. 앞 두 필드 (native 종료 · 증거 유효) 중 하나라도 성립하지 않으면
`INCONCLUSIVE` 다 — native 종료가 확인됐는데 증거 · 분석 · 전달이 실패하면 `native_completion` 은 그대로 남고 비교만 `INCONCLUSIVE` 가 된다 (r1 BMIN-N1).

## 5. 변경부 검증안 · 다음

`LIMITED_VALIDATION_PLAN.json` — 9 군 · **고유 ID 62** (Python 39 + Java helper 2 + PowerShell 21) · **입력 77** · 예산 제안 **1,660 s** (r1: 54 ID ·
입력 59 · 1,530 s). ID 하나는 검증안의 한 항목, 입력 하나는 그 엔진의 단일 세션 안의 한 번의 평가다 (세션은 입력마다 열지 않는다).

| 추가 (r2) | 사례 |
|---|---|
| BMIN-R1-N1 — 전체 줄 문법 | PY03-11 (한 줄에 두 문장 → `_FORMAT`) · PY03-12 (정상 + 불완전 문장 / 정상 + 꼬리 문자 → `_FORMAT` · 입력 2) · PY03-13 (양성 대조: 공백 둘린 줄 → PASS 156925 / 12 · NORMAL480 131행 원문 → PASS 기록만 · 차이 −77,440 · 입력 2) |
| consumer 값 경로 (Q4-2) | PY03-14 (solved 0 → consumer `TRANSIENT_DOF_READBACK_VALUE` — PS01-17 의 부모 측 거부는 대체가 아니다) |
| `GNativeAxis` 원인별 (Q4-3) | PS01-18 (반환 누락 / 오류 다섯 — `NATIVE_CHILD_RETURN_MISSING_OR_ERROR`) · PS01-19 (다른 run · 다른 manifest — `RESULT_IDENTITY`) · PS01-20 (모양은 있으나 모순된 종료 근거 넷 — `TERMINATION_EVIDENCE_INVALID`) · PS01-21 (축 계산 전 정지 — `NATIVE_AXIS_NOT_EVALUATED` · 재검토가 짚지 않은 일곱째 원인 이름 · 목록을 닫으려고 더했다). 이제 부모의 원인 이름 일곱이 각각 자기 사례를 가진다 (PS01-12 · 13 · 14 · 18 · 19 · 20 · 21) |
| C1 | PS01-16 문구 (소수점 아래 30 자리 · 유효숫자 28 자리) · 분류 이동 |

예산 변경 (제안 — 사용자의 별도 승인 없이 횟수 · 예산을 늘리지 않는다): Python 210 → 250 s (입력 +6) · PowerShell 150 → 240 s (입력 +12) · 전체
1,530 → **1,660 s**. 봉인 (`preseal_before_first_test`): 봉인 소스 = r2 manifest · harness 는 별도 승인 뒤에만 쓰고 그 SHA · 각 생산 함수의 봉인 바이트
추출 위치 · 입력 파일과 기대 이유를 첫 시험 전에 고정해 사용자에게 보인다 · 엔진 식별 · 최종 수 62 / 77.

`VALIDATION_REQUEST_KO.md` · `NATIVE_BMIN640_APPROVAL_DRAFT_KO.md` 는 비활성 초안이다.

다음 (각각 별도 사용자 결정 · 자동 시작 없음): ① r2 준비 재검토 → ② 변경부 검증 승인 · 수행 · 수용 → ③ native 150 s 최대 1 회 승인 → ④ 결과 수신 검토.
하지 않은 것: 컴파일 · 기능 시험 · harness · JVM · COMSOL · native · 정책 변경 · 실제 승인 파일 생성 · 실행 기계 접근 · 유한 σ · 960 s · 다른 공간 축.
approved=false / usable=false · 전체 · 정상 gate INCOMPLETE · 실효 정책 UNVERIFIED 유지.
