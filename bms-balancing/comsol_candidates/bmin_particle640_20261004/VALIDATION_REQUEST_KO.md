# 다음 한 건 제안 — B-min 후보 변경부 한정 검증 (비활성 초안)

**상태: 계획만.** 시험 권한도 실행 결과도 아니다. 이 초안을 제출한 것만으로 통과로 취급하지 않는다 (B-min v2 §8-3). 대상은 후보 manifest
`3722a51fb1caeddd72fca3751f2ed78ed3e05d5f1938fa452503b3fa5c421a03` 의 **변경부만**이고, 목록 · 기대 이유 · 도달 단계는 `LIMITED_VALIDATION_PLAN.json`
(9 논리군 · 41 사례) 에 고정했다. 논리군 · 사례 · assertion 수는 서로 다른 단위다.

## 사용자 채택용 문구 (초안 — 채택 전에는 실행하지 않는다)

> 위 고정 B-min 후보 (manifest `3722a51f…`) 의 변경부 9 군 41 사례 한정 오프라인 검증 1 건을 승인합니다. 실제 consumer → entry, Java `checkShape`
> 추출 helper, Windows PowerShell 5.1 의 `GDecision` · `GFields` 를 검사하고 첫 실패를 보존한 뒤 중지하세요. COMSOL 전체 모델 compile / JVM 모델 실행 /
> batch / solve · 실제 입력 · 정책 변경 · native 승인 생성은 포함하지 않습니다.

## 반드시 들어가는 항목 (B-min v2 §8-3 의 목록 → 사례)

| 항목 | 사례 |
|---|---|
| 입자 축 밖 변이 거부 (물리 메시 · 실행 설정) | PY03-02 · PY03-03 · PY03-04 |
| 기준 위조 거부 | PY04-01 · PY04-02 · PY04-03 |
| 필수 끝점 누락 (150 · 149.9 · 120) | PY02-01 · PY05-01 · PY05-02 |
| 같은 개수의 잘못된 시각 / 좌표 | PY05-03 · PY05-04 · PY05-06 |
| **한도와 정확히 같은 값 → 허용 (≤ · `WITHIN_LIMITS_THIS_WINDOW`)** | PY01-02 · PS01-04 |
| 한도 초과 → `EXCEEDS_LIMITS` (오류가 아니다) | PY01-03 · PY01-04 · PS01-02 |
| NaN | PY06-01 |
| 정상 / 보호 / 오류 분리 | PY01-01 · PY02-04 · PY02-05 · PY03-01 · PY07-01 · PS01-07 |
| 부모 판정의 예산 | PY07-02 · PS01-05 · PS01-06 |
| 종료코드 연결 | PY01-01 · PY01-03 · PY02-04 · PS01-08 |

판정 문장 (SPEC §44-2 그대로): 한도와 같으면 허용한다 (≤). 모든 유효 조건이 성립할 때 max |ΔV| ≤ 0.001 V **그리고** 두 전극 max |Δx_surface| ≤ 1e−4 이면
`WITHIN_LIMITS_THIS_WINDOW`, 어느 하나라도 **엄격히 크면** `EXCEEDS_LIMITS` 다.

## 엔진 · 횟수 · 한도 (제안)

| 범위 | 제안 | 실제 대상 |
|---|---|---|
| harness · 엔진 / 소스 · fixture · 호출 봉인 | 600 s | 실제 함수 추출 SHA 와 기대값. harness 는 아직 없고 SHA 도 만들지 않았다 |
| 고정 격리 Python | 1 세션 180 s | consumer `window_coverage` · `extreme` · `numeric` · `three_fields` · `runtime_evidence` · `mesh_evidence` · `analyze` 와 entry 의 새 결과 · 승인 필드 소비. native / process / gate 진입은 import 전에 inert adapter 로 막는다 |
| Java | helper compile 1 회 90 s · stub JVM 1 세션 60 s | `checkShape` 와 `TIMES` 만 추출 — COMSOL jar · 전체 모델 로드 없음 |
| Windows PowerShell 5.1 | fixture 1 세션 120 s | 봉인된 `PARENT_COMMAND.ps1` 에서 `GDecision` · `GFields` 를 그대로 추출해 Python 이 만든 결과 JSON 을 먹인다. 새 `BInvoke` / native 프로세스 시험 없음 |
| 보존 · 포장 | 300 s | source · engine · harness · result · 반환 결속, 원본 보존 |
| 미완 정리 | 120 s | 최초 오류 · 미실행 목록 · 시간 기록 |
| **전체** | **1,470 s** | 새 원점 · 미사용분 재시험 전용 없음 |

엔진: Python = `CONTRACT.python` (고정 해시) · PowerShell = `PARENT_COMMAND.ps1` 이 고정한 `powershell.exe` 해시 · Java helper 의 compiler / JVM = 수용된 정상
30 s 검증 `COMMANDS.json` 의 후보 (첫 시험 전 실제 식별 확인). 다른 엔진 · 권한 · ExecutionPolicy fallback 없음. **실행 주체는 사용자 결정**이다 (정상
30 · 60 s 변경부 검증은 CX 가 Windows 에서 했다 — 이 저장소의 리눅스 컨테이너에는 PowerShell 5.1 · 고정 Python · COMSOL 이 없다).

fixture 는 시험 임시 위치에만 둔다. 실제 `future_run_001` · `future_parent_001` · `future_authorizations` 와 사용자 승인 / release / runtime token 을 만들지 않는다.
PowerShell 판정을 Python 으로 흉내 내 통과시키지 않는다. 첫 실패에서 해당 source · harness · seal · 원 출력 · 외부 rc · 시간을 보존하고 남은 엔진을 멈춘다 —
자동 수정 · 부분 재시험 · 추가 probe 없음. 이 검증이 끝나도 native 를 자동으로 이어서 실행하지 않는다.

## 다시 시험하지 않는 것

`BSave` · `BInvoke` · C2 · 소유 Job · post-write 예산 본문은 NORMAL480 과 바이트가 같다 (`STATIC_AUDIT.json` — `parent BSave byte-identical` 등) — 과거 수용을
재사용한다. 기존 111 · 78 · 1198 · 30 s 시험은 반복하지 않는다. 검증 대상은 새 비교 · 상태 · 세 필드 · 예산 분기뿐이다.
