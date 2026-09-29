# 정상30초 한정 검증 — 독립 수신 검토

2026-09-30. **N30-N1·N30-N2 종결 수용 / 제출된 변경부 한정 검증 수용 / native30 별도 승인 대기.**

수용 범위는 고정 후보의 오프라인 변경부와 그 검증 증거다. 현재 30초 계산, 실제 PowerShell 시작, COMSOL API 호환성, 전체 모델 컴파일, 수치 결과, 장기 수렴을 PASS로 판정하지 않는다. 검토자는 받은 Python/PowerShell/Java를 import·실행하지 않았고, COMSOL/JVM/시험/입력 gate를 재실행하지 않았다. 자체 ZIP·JSON·해시·텍스트/AST 대조만 수행했다.

## 1. 수신 식별

| 자료 | bytes | SHA-256 |
|---|---:|---|
| 통합 ZIP | 322,912 | `0854dbd1db8433c4d22def4984af7b535c36c3e7ab6c65b6b9d013d1ab0f29ea` |
| 통합 PACKAGE_MANIFEST | 17,389 | `ff7075a3d0e1a10279b80ffaba29e11520dda0a737529f66d9925d87e4e1c7b8` |
| 전달 보충 ZIP | 7,597 | `5f5b4dfe47eec3a4a6d94dac72f08f03716b0de2ab15ea8aff95409d2414ba22` |
| 최종 후보 CODE_MANIFEST | 1,080 | `6b9ae2a75a2035d0cc80359f5d83cc3ca5dc5aa744b68255d219ce8a55feb603` |

통합 102 payload+manifest, 내부 attempt02 ZIP의 66 payload+manifest, 보충 5 payload+manifest를 각각 재읽어 정확 집합·고유 이름/대소문자·크기·SHA·CRC·경로/링크를 확인했다. 기존 생성 영수증의 recipient=null은 수정하지 않았다.

후보 manifest의 5개 파일은 포함된 실제 바이트와 일치한다. 이전 정상30초 준비본과 비교하면 Java와 candidate_entry.py는 바이트 동일하다. 소비자 변경은 초기 Li 계산·결과 필드, 부모 변경은 그 필드 소비·최종 예산 확인 및 새 root, 계약 변경은 root/파생 경로·초기 Li 한도다. LF/CRLF를 정규화한 텍스트 diff와 원시 바이트 동일성 검사를 구분했다.

## 2. N30-N1 — 종결 수용

`candidate_snapshot/src/diagnostic_consumer.py:183` 이후에서 각 초기 Li 값의 `abs(current-reference)`를 계산하고, 계약 한도가 정확히 `1e-9 mol/m²`인지 확인한다. 총량의 시간별 상대 변화 `1e-6` 검사는 별도로 유지한다. 결과에는 current/baseline/absolute_delta/unit/absolute_limit을 남기고 상대값은 참고용으로만 표시한다.

`candidate_snapshot/PARENT_COMMAND.ps1:105` 이후는 각 항의 PASS·단위·정확 한도·absolute_delta 존재·유한/비음수/한도 이내를 소비한다. 부모가 원 CSV의 수치를 다시 계산하는 별도 분석기라는 뜻은 아니다.

PY06의 동일값·정확 경계·경계 초과·N/P 상쇄·상대통과/절대실패 결과와 PS03의 경계·NaN/Infinity/음수/초과·필드 누락·위조 PASS/단위/한도 거부 기록을 대조했다. 기존 상대오차로 초기 항의 불일치를 놓치던 잔여는 닫는다.

## 3. N30-N2 — 종결 수용

부모 `PARENT_COMMAND.ps1:163–185`의 실제 outer finally는 PRE_WRITE 기록을 쓴 뒤 read-back과 boundary 식별을 완료하고, POST_WRITE 시각으로 전체5100초·전달300초를 다시 확인한다. 초과 시 limited=INCOMPLETE 및 FINAL_POST_WRITE_BUDGET을 최종 반환에 남긴다. PRE_WRITE 파일을 사후 성공 기록으로 덮어쓰지 않는다.

| 저장된 실제 시험 분기 | PRE_WRITE | POST_WRITE | 최종 의미 |
|---|---|---|---|
| 전체5099→5100.01초 | 예산 내 | 초과 | INCOMPLETE |
| 전달299→300.01초 | 예산 내 | 초과 | INCOMPLETE |
| 전체 정확5100초 | 예산 내 | 예산 내 | 외부 수용 대기 |
| 전달 정확300초 | 예산 내 | 예산 내 | 외부 수용 대기 |
| 본문 오류 유지 | 예산 내 | 예산 내 | INCOMPLETE 유지 |
| writer/transcript/마지막 반환 오류 | 성공 반환 없음 | 완료 증거 미완 | 이전 파일만으로 수용하지 않음 |

이 표는 PS fixture의 원 기록을 직접 읽은 결과다. clock/transcript/reference는 inert이며, BSave는 주입 writer 오류를 제외하고 실제 본문이다. 실제 native 실행의 시간 보증은 아니다. 마지막 stdout 자체가 끝난 뒤까지의 시간을 소급 측정했다고 보지 않는다. `-NoExit` 부모의 OS 종료코드는 null 유지가 맞다.

## 4. 111개 기능 사례와 코드 결속

| 엔진 | 제출된 사례 | 이번 수신 확인 |
|---|---:|---|
| Python | 47 | 기존 attempt02 결과, 고유 ID·PASS·실행 소스 seal·raw stdout/rc 연결 |
| Java helper | 8 | 기존 attempt02 helper 소스·stdout8건·javac/JVM rc0 연결 |
| Windows PowerShell5.1 | 56 | 이번 단일 fixture 결과, 고유 ID·CASE_MAP·raw stdout/rc 연결 |
| 정적 데이터 대조 | 2 | 정확 helper 본문 및 Java437시각/threshold0/runAll lexical1 |

합계는 **기능 사례111 + 정적 대조2, 논리군17**이다. 113회 기능 실행 또는 113개 독립 assertion으로 바꾸어 부르지 않는다. 통합 CASE_MAP에 중복 (group,case)는 없고 실제 결과 집합과 일치한다.

이전·현재 PRE_TEST_SEAL의 후보5파일+manifest 식별이 모두 동일한 현재 사본에 연결된다. 현재 normal/protected JSON 두 개는 내부 attempt02 원 ZIP의 바이트와 동일하다. Java checkShape는 후보/시험 harness에 같은 본문으로 들어 있으며 helper SHA도 재계산했다. Java 전체 모델 컴파일이나 COMSOL API 시험으로 확대하지 않는다.

PS의 BSave/BInvoke/GDecision/outer_finally 추출문은 원 부모의 명시한 행과 정규화 텍스트가 일치한다. BInvoke는 추출·보존 대조일 뿐 이번에 새 자식 프로세스를 발생시켜 시험한 함수가 아니다. rc 분기는 typed inert 반환으로 시험했다. Python 양성/보호 결과를 실제 GDecision 입력으로 소비한 경로는 확인된다.

## 5. 시작 환경의 남은 조건 — 새 기능 결함으로 재분류하지 않음

과거 attempt02의 Get-FileHash 미인식 stderr를 보존하고 있다. 이번 PS 시험은 PSHOME의 Utility 모듈 manifest를 명시적으로 Import-Module한 뒤 56개를 통과했다. 생산 부모에는 그 import가 없다. 따라서 **시험 환경의 성공을 생산 부모 startup 성공으로 확장할 수 없다.** 과거 자동 로딩 실패의 근본 원인도 미확정이다.

현재 부모는 첫 BHash를 native 위임보다 먼저 수행한다(16,125행; 위임145행). 고정 코드 그대로 실행하는 경우 모듈/해시 오류가 나면 그 자리에서 중지하는 경로다. 이 미확인 조건은 native 승인에 명시하고, 오류 후 대체 해시·다른 셸·권한/정책 변경·자동 재시도를 하지 않아야 한다. 기존 입력 진단이나 전체111개 재시험을 별도 선행 요구로 만들지 않는다.

명시적 모듈 초기화를 실제 시작 명령에 추가하려면 **추가 운영 명령 변경**이다. 숨겨 넣지 말고 정확 명령·출처·오류 중단을 제시하여 그 좁은 범위만 따로 승인받는다. 현재 코드가 잘못됐다고 단정하거나 이번 검토에서 생산 코드를 수정하지 않는다.

## 6. 전달 보충과 시간 경계

보충 영수증은 실제 수신 통합 ZIP/manifest와 일치하며, c0126c의 후속 전사 output을 JSON으로 읽으면 영수증 값과 같다. 전사된 바깥 exit_code=0을 확인했다. 이는 수신자가 과거 원격 프로세스를 직접 관측한 기록이나 원시 OS 감사가 아니다.

전체237.264968초는 START→성공 closeout의 ZIP 검증 후 영수증 객체 구성 시점이다. 포장1.0886146000120789초는 성공한 closeout 호출 안의 시점이며 앞선 포장 실패/수정 구간까지 포함한 단계 누적이 아니다. 영수증 쓰기·최종 stdout·도구 반환까지의 정확 종료시간은 미측정이다. 따라서 **ZIP 무결성 및 성공 반환은 수용하되, 전 전달 lifecycle의 마지막 시점까지 정밀한 예산 준수를 독립 확인했다고 쓰지 않는다.**

이번 누락은 새 native 후보 N30-N2의 기능 시험 실패가 아니다. 과거 시간을 재실행으로 만들거나 영수증을 고치지 않는다. 같은 시험·포장을 반복할 사유로 삼지 않고 기록 한계로 남긴다.

## 7. 보존과 검토 한계

송신 측 PRESERVATION_BEFORE/AFTER의 선택28개 기록은 동일하다. 그 중24개는 실제 수신 바이트(내부 ZIP 포함)와 SHA/크기로 연결된다. python/javac/java/powershell 실행파일4개는 식별 기록만 있고 바이너리가 없어 원격 현재 파일까지 직접 검증한 것이 아니다. MPH·현지 전체 prefs·전역 프로세스 상태는 이번 검토 대상에 없다.

이전 attempt02 실패, 포장 검사 문자열30/숫자30 오류, 성공 후속 기록은 함께 보존된다. 수신 검토자의 첫 데이터 감사에도 외부 영수증을 내부 파일로 기대한 오류와 helper CRLF/LF 비교 오류2개가 있었다. 최초 감사 기록을 남기고 감사기만 정정했다. 후보/기능시험 실패가 아니다. 최종 자체 데이터·정적 대조109항목은 모두 일치했으며 이를 기능 사례 수에 합산하지 않는다.

## 8. 다음 결정

**같은 수정·전체 시험·1198 재시험을 반복하지 않는다.** 다음은 최종 manifest/run/argv/cwd, 현재 기본 prefs 식별과 정책 무변경 경로, 시작 환경 미확인 조건, 실행 자원·예산을 정리한 **fresh0→30초 최대1회 별도 사용자 승인**이다. 승인 전 실제 approval/release/runtime/token/USER_DECISION을 만들지 않는다.

정상30초 도달과 보호중단/오류를 구분하고, 결과 수용 전 다음 연장을 실행하지 않는다. 30초가 완료돼도 전체 수렴·장기 운전·실험 타당도·1198 재시험·후보C·12시간/CDC/sweep 승인은 아니다. 전체/정상 gate INCOMPLETE, 내부 실효정책 UNVERIFIED, OCP 외삽 금지, TIME_CAPS 원인 미확인, 기존 failed/pending/원복 기록을 유지한다.

판정 데이터: DECISION.json. 상세 독립 대조: PACKAGE_AUDIT.json, EVIDENCE_AUDIT.json, SUPPLEMENT_AUDIT.json, INDEPENDENT_SOURCE_DIFF.patch.
