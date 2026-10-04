# 다음 한 건 제안 — B-min 후보 r1 변경부 한정 검증 (비활성 초안)

**상태: 계획만.** 시험 권한도 실행 결과도 아니다. 이 초안을 낸 것만으로 통과로 취급하지 않는다 (B-min v2 §8-3). 대상은 r1 manifest
`9dcb47f0ec3ec346b491d90c2836e3b30f54eb88fd5e4fbd216fc34782275cdb` 의 **변경부만** (v1 의 변경부 + r1 보완) 이고, 목록 · 기대 이유 · 도달 단계는
`LIMITED_VALIDATION_PLAN.json` (9 논리군 · 54 사례) 에 고정했다.

## 사용자 채택용 문구 (초안 — 채택 전에는 실행하지 않는다)

> 위 고정 B-min 후보 r1 (manifest `9dcb47f0…`) 의 변경부 9 군 54 사례 한정 오프라인 검증 1 건을 승인합니다. 실제 consumer → entry, Java
> `checkShape` 추출 helper, Windows PowerShell 5.1 의 `GDecision` · `GNativeAxis` · `GFields` 를 검사하고 첫 실패를 보존한 뒤 중지하세요. COMSOL
> 전체 모델 compile / JVM 모델 실행 / batch / solve · 실제 입력 · 정책 변경 · native 승인 생성은 포함하지 않습니다.

## r1 에서 새로 들어간 사례

| 발견 | 사례 |
|---|---|
| BMIN-N1 — native 종료 축의 분리 | PS01-09 (기대값 변경: 정상 종료 + 구성 실패 → NORMAL / INVALID / INCONCLUSIVE) · PS01-05 · PS01-07 (기대값 갱신) · PS01-10 (정상 종료 + 분석 예산 초과) · PS01-11 (정상 종료 + 최종 전달 예산 초과) · PS01-12 (native 실패 rc 1) · PS01-13 (종료 근거 누락 둘) · PS01-14 (consumer 라벨 위조 → 불일치) · PS01-15 (보호 중단 + 구성 실패) |
| BMIN-N2 — transient DOF 관측 필수 | PY03-05 (예상과 같은 값) · PY03-06 (다른 유효값 → 기록만) · PY03-07 (transient 줄 삭제 · 초기화 줄만) · PY03-08 (DOF 줄 없음) · PY03-09 (구간 안 둘 — 모호) · PY03-10 (형식 불일치) · PS01-17 (부모의 구조 검사) |
| C1 — 정밀도 문구 | PS01-03 / 04 는 **한도 부근 값 · 라벨 일치 검사**다 (자릿수 반올림 시험이 아니다) · PS01-16 명시 사례 (소수 30 자리 → INCOMPLETE · 불일치 = 미완 원칙) |

판정 문장 (SPEC §44-2 그대로): 한도와 같으면 허용한다 (≤). 모든 유효 조건이 성립할 때 max |ΔV| ≤ 0.001 V **그리고** 두 전극 max |Δx_surface| ≤ 1e−4 이면
`WITHIN_LIMITS_THIS_WINDOW`, 어느 하나라도 **엄격히 크면** `EXCEEDS_LIMITS` 다.

## 엔진 · 횟수 · 한도 (제안)

| 범위 | 제안 | 실제 대상 |
|---|---|---|
| harness · 엔진 / 소스 · fixture · 호출 봉인 | 600 s | 실제 함수 추출 SHA 와 기대값 (harness 는 아직 없다) |
| 고정 격리 Python | 1 세션 210 s | consumer 의 새 분기 (창 비교 · 세 필드 · I-2 · I-3 `mesh_evidence`) 와 entry 의 새 결과 · 승인 필드 소비 — native / process / gate 진입은 import 전에 inert adapter 로 막는다 |
| Java | helper compile 1 회 90 s · stub JVM 1 세션 60 s | `checkShape` · `TIMES` 만 추출 |
| Windows PowerShell 5.1 | fixture 1 세션 150 s | 봉인된 r1 `PARENT_COMMAND.ps1` 에서 `GDecision` · `GNativeAxis` · `GFields` 를 그대로 추출 — 새 `BInvoke` / native 프로세스 시험 없음 |
| 보존 · 포장 | 300 s | source · engine · harness · result · 반환 결속 |
| 미완 정리 | 120 s | 최초 오류 · 미실행 목록 · 시간 |
| **전체** | **1,530 s** | 새 원점 · 미사용분 재시험 전용 없음 |

엔진: Python = `CONTRACT.python` (고정 해시) · PowerShell = `PARENT_COMMAND.ps1` 의 고정 `powershell.exe` 해시 · Java helper = 수용된 정상 30 s 검증
`COMMANDS.json` 의 후보 (첫 시험 전 식별 확인). 다른 엔진 · 권한 · ExecutionPolicy fallback 없음. 실행 주체는 사용자 결정. fixture 는 시험 임시
위치에만 두고, PowerShell 판정을 Python 으로 흉내 내지 않는다. 첫 실패에서 멈추고 보존한다 — 자동 수정 · 부분 재시험 · 추가 probe 없음. 이 검증이
끝나도 native 를 자동으로 이어서 실행하지 않는다.

## 다시 시험하지 않는 것

`BSave` · `BInvoke` · C2 · 소유 Job · post-write 예산 본문은 NORMAL480 · v1 과 바이트가 같다 (`STATIC_AUDIT.json`). 기존 111 · 78 · 1198 · 30 s 시험 ·
NORMAL480 · rtol30 은 반복하지 않는다.
