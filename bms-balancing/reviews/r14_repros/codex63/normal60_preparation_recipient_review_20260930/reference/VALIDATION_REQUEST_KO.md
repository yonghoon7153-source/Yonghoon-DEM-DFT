# 다음 한 건 제안 — 60초 후보 변경부 한정 검증

현재는 계획만 작성했으며 시험 권한/실행 결과가 아니다. 후보 manifest `82e556243b29b10ae65b95dcdff7f854734b6f1cfffc1881327cab1939ebe5c8`의 변경부만 대상으로 **12논리군46사례**를 제안한다. 논리군/사례/assertion 수는 구분한다. 목록과 기대 이유/도달 경로는 LIMITED_VALIDATION_PLAN.json에 고정한다.

사용자 채택용 문구: “위 고정60초 후보의 변경부12군46사례 한정 오프라인 검증1건을 승인합니다. 실제 consumer→entry, Java checkShape 추출 helper, PS5.1 GDecision을 검사하고 첫 실패를 보존한 뒤 중지하세요. COMSOL 전체모델 compile/JVM/batch/solve·실제입력·정책변경·native승인 생성은 포함하지 않습니다.”

이 문구는 비활성 초안이다. 실제 사용자 채택 전에는 실행하지 않는다. 기존111개/78개/1198/30초 재시험은 포함하지 않는다.

| 범위 | 제안 횟수/한도 | 실제 대상 |
|---|---|---|
| harness·엔진/소스·fixture·호출 봉인 |600초| 실제 함수 추출 SHA 및 기대값. 아직 harness는 없으며 SHA를 만들지 않음 |
| 고정 격리 Python |1세션120초| 변경 consumer guard/coverage/numeric/late_summary/analyze 및 entry의 새 결과/승인 필드 소비. native/process/gate 진입은 import 전에 inert adapter로 차단 |
| Java |helper compile1회90초, stub JVM1세션60초| 정확 checkShape와 TIMES만 추출, COMSOL jars/전체 모델 로드 제외 |
| Windows PowerShell5.1 |fixture1세션90초| 최종 후보의 실제 GDecision 추출. Python 생성 정상/보호 결과 JSON 소비. 새 BInvoke/native 프로세스 시험 없음 |
| 보존·포장 |300초| source/engine/harness/result/반환 결속, 원본 보존 |
| 미완 정리 |120초| 최초 오류·미실행 목록/시간 기록 |
| 전체 |1380초| 새 원점, 미사용분 재시험 전용 없음 |

각 엔진의 경로/현재 바이트 SHA·정확 argv/cwd는 승인 후 시험 전 봉인한다. 고정Python은 CONTRACT.python, PS5.1은 PARENT의 고정 실행파일을 사용한다. Java helper용 compiler/JVM 경로는 기존 정상30 검증 COMMANDS.json의 후보를 재사용하되 실제 식별을 시험 전 확인한다. 버전 출력도 이번 준비에서는 실행하지 않았다. 다른 엔진/권한/ExecutionPolicy fallback은 없다.

fixture는 별도 시험 임시 위치에만 둔다. 실제 future_run/future_parent/future_authorizations와 사용자 승인/release/runtime/token을 만들지 않는다. 받은 함수 대신 Python으로 PS 판정을 모사해서 통과시키지 않는다. 봉인된 생산 함수 자체의 추출 바이트와 엔진별 결과를 연결한다.

첫 실패 시 해당 source/harness/seal/raw출력·외부rc/시간을 보존하고 남은 엔진을 중지한다. 자동 수정·부분 재시험·추가probe 없음. 이번 계획으로 기능검증 후 native60을 자동 이어서 실행하지 않는다.

이미 수용된 BSave/BInvoke·C2·owned Job·post-write 예산 본문은 이번 후보에서 바이트 불변으로 대조했고 과거 수용을 재사용한다. 신규 비교/상태/시간 분기만 실행 검증한다. 기존 전체 실패·원복 이력은 그대로 둔다.
