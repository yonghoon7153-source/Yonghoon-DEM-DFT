# 다음 한 건 제안 — B-min 후보 r2 변경부 한정 검증 (비활성 초안)

**상태: 계획만.** 시험 권한도 실행 결과도 아니다. 이 초안을 낸 것만으로 통과로 취급하지 않는다 (B-min v2 §8-3). 대상은 r2 manifest
`4cdca2e6bf7d073f813d97be73825b8cd2043c2fc44e285f4a190bc6fb97cf25` 의 **변경부만** (v1 의 변경부 + r1 보완 + r2 보완) 이고, 목록 · 기대 이유 · 도달
단계는 `LIMITED_VALIDATION_PLAN.json` (9 논리군 · 고유 ID 62 · 입력 77) 에 고정했다.

## 사용자 채택용 문구 (초안 — 채택 전에는 실행하지 않는다)

> 위 고정 B-min 후보 r2 (manifest `4cdca2e6…`) 의 변경부 9 군 · 고유 ID 62 · 입력 77 한정 오프라인 검증 1 건을 승인합니다. 실제 consumer → entry, Java
> `checkShape` 추출 helper, Windows PowerShell 5.1 의 `GDecision` · `GNativeAxis` · `GFields` 를 검사하고 첫 실패를 보존한 뒤 중지하세요. COMSOL
> 전체 모델 compile / JVM 모델 실행 / batch / solve · 실제 입력 · 정책 변경 · native 승인 생성은 포함하지 않습니다.

## r2 에서 새로 들어간 사례

| 발견 | 사례 |
|---|---|
| BMIN-R1-N1 — transient DOF 줄의 전체 줄 문법 | PY03-11 (한 줄에 서로 다른 두 문장 → `TRANSIENT_DOF_READBACK_FORMAT`) · PY03-12 (정상 문장 + 불완전 문장 · 정상 문장 + 꼬리 문자 → `_FORMAT` 둘) · PY03-13 (양성 대조: 공백 둘린 단일 줄 → PASS · NORMAL480 131행 원문 79485+12 → PASS 기록만) |
| consumer 의 값 경로 (재검토 Q4-2) | PY03-14 (solved 0 → consumer 의 `TRANSIENT_DOF_READBACK_VALUE`) |
| `GNativeAxis` 실패 원인별 (재검토 Q4-3) | PS01-18 (자식 반환 누락 · returned false · 예외 · 새 오류 · rc 가 정수 아님 → `NATIVE_CHILD_RETURN_MISSING_OR_ERROR`) · PS01-19 (다른 run_id · 다른 manifest → `RESULT_IDENTITY`) · PS01-20 (정상 상태 + guard · 끝 시각 ≠ 마지막 저장 시각 · step 수 불일치 · 어느 guard 와도 맞지 않는 보호 정지 사유 → `TERMINATION_EVIDENCE_INVALID`) · PS01-21 (축 계산 전 정지 → `NATIVE_AXIS_NOT_EVALUATED`) |
| C1 — 정밀도 문구 · 분류 | PS01-16 은 소수점 아래 30 자리 · 유효숫자 28 자리 문자열 → INCOMPLETE (불일치 = 미완 원칙 · 정밀도 보증 아님 · 정확 등호 사례 아님 — 정확 등호는 PY01-02 / PS01-04) · `precision_mismatch_items` 로 분류 · 실제 경로는 목표 엔진에서 확인 |

r1 의 사례 54 는 문구 그대로 유지한다 (PS01-16 의 C1 정정만 예외). 여러 입력을 가진 ID (PY05-06 · PY03-12 · PY03-13 · PS01-07 · 08 · 13 · 17 · 18 · 19 ·
20) 는 입력마다 기대 이유를 `input_expectations` 로 적었다.

판정 문장 (SPEC §44-2 그대로): 한도와 같으면 허용한다 (≤). 모든 유효 조건이 성립할 때 max |ΔV| ≤ 0.001 V **그리고** 두 전극 max |Δx_surface| ≤ 1e−4 이면
`WITHIN_LIMITS_THIS_WINDOW`, 어느 하나라도 **엄격히 크면** `EXCEEDS_LIMITS` 다.

## 엔진 · 횟수 · 한도 (제안 — r1 대비 증액은 사용자 승인 사항)

| 범위 | 제안 (r1) | 실제 대상 |
|---|---|---|
| harness · 엔진 / 소스 · fixture · 호출 봉인 | 600 s (600) | 실제 함수 추출 위치 · SHA 와 입력별 기대 이유 (harness 는 아직 없다) |
| 고정 격리 Python | 1 세션 **250 s** (210) | consumer 의 새 분기 (창 비교 · 세 필드 · I-2 · I-3 `mesh_evidence` 의 전체 줄 문법) 와 entry 의 새 결과 · 승인 필드 소비 — native / process / gate 진입은 import 전에 inert adapter 로 막는다 |
| Java | helper compile 1 회 90 s · stub JVM 1 세션 60 s (같음) | `checkShape` · `TIMES` 만 추출 |
| Windows PowerShell 5.1 | fixture 1 세션 **240 s** (150) | 봉인된 r2 `PARENT_COMMAND.ps1` (r1 과 바이트 동일) 에서 `GDecision` · `GNativeAxis` · `GFields` 를 그대로 추출 — 새 `BInvoke` / native 프로세스 시험 없음 |
| 보존 · 포장 | 300 s (300) | source · engine · harness · result · 반환 결속 |
| 미완 정리 | 120 s (120) | 최초 오류 · 미실행 목록 · 시간 |
| **전체** | **1,660 s** (1,530) | 새 원점 · 미사용분 재시험 전용 없음 |

증액분 (Python +40 s · PowerShell +90 s) 은 r1 의 입력당 시간 (Python 210 s ÷ 36 ≈ 5.8 s · PowerShell 150 s ÷ 21 ≈ 7.1 s) 에 새 입력 수 (6 · 12) 를 곱해 올린 **제안**이다 —
충분성 실측이 아니다. 별도 승인 없이 횟수 · 예산을 늘리지 않는다.

엔진: Python = `CONTRACT.python` (고정 해시) · PowerShell = `PARENT_COMMAND.ps1` 의 고정 `powershell.exe` 해시 · Java helper = 수용된 정상 30 s 검증
`COMMANDS.json` 의 후보 (첫 시험 전 식별 확인). 다른 엔진 · 권한 · ExecutionPolicy fallback 없음. 실행 주체는 사용자 결정. fixture 는 시험 임시
위치에만 두고, PowerShell 판정을 Python 으로 흉내 내지 않는다. 첫 실패에서 멈추고 보존한다 — 자동 수정 · 부분 재시험 · 추가 probe 없음. 이 검증이
끝나도 native 를 자동으로 이어서 실행하지 않는다.

시험 전 봉인 (`preseal_before_first_test`): 봉인 소스 = r2 manifest (바이트가 바뀌면 새 manifest · 새 검증안) · harness 는 별도 승인 뒤에만 쓰고 그
SHA-256 · 각 생산 함수의 봉인 바이트 추출 위치 · 입력 파일과 기대 이유를 첫 시험 전에 고정해 사용자에게 보인다 · 엔진 식별 · 최종 수 62 / 77 · 전체
1,660 s 는 제안.

## 다시 시험하지 않는 것

`BSave` · `BInvoke` · C2 · 소유 Job · post-write 예산 본문은 NORMAL480 · v1 · r1 과 바이트가 같다 (`STATIC_AUDIT.json` 사슬). 기존 111 · 78 · 1198 · 30 s
시험 · NORMAL480 · rtol30 은 반복하지 않는다.
