# S1O-R1 R1_003 한정 검증 중지 결과

이번 결과는 **INCOMPLETE**입니다. Python 99사례는 전부 통과했고, PowerShell은 앞선 28사례 통과 후 PARENT_R113의 시험 입력 형식 확인에서 멈췄습니다. 127 PASS / 1 하네스 실패 / 2 미실행이며 전체 130사례 통과가 아닙니다.

첫 오류는 `HARNESS_FIXTURE_OR_ASSERTION:R113_DOUBLE_AFTER_JSON_PARSE`입니다. PowerShell 하네스 133행의 JSON 파싱 후 Double 형식 assertion에서 중단됐습니다. 해당 사례의 목표 생산 판정 함수에 도달하기 전이므로 생산 코드 결함이나 해당 음성 사례 PASS로 분류하지 않습니다. 실제 파싱 형식은 실패 기록에 없으므로 추측해 확정하지 않습니다. PARENT_R114·PARENT_R115는 실행하지 않았습니다.

사전 봉인 390.058414/720초, Python 실제 세션 169.274139/420초·rc0, PowerShell 실제 세션 30.308574/300초·rc1입니다. PowerShell 반환의 within_limits=false는 성공/예산 결합 판정이며 시간 상한 초과라는 뜻이 아닙니다. 최종 전달 시간은 ZIP 밖 DELIVERY_RECEIPT와 반환 후속 전사를 함께 확인해야 합니다.

사용자가 R1_003 새 위치를 승인한 뒤 새 원점으로 수행했습니다. 앞선 R1_001/R1_002 중지 기록은 보존했으며 재사용한 준비 자료를 이번에 새 기능 시험한 것으로 부풀리지 않았습니다. 이번 첫 시험 전에 INIT02 경계 입력을 target0.001/observed0.001000001로 정리하여 절대1e-9·상대1e-6 허용치를 유지했습니다. 생산 파일은 변경하지 않았습니다.

FIRST_SEAL은 생산 소스·엔진·130 입력 명세·하네스·추출 범위·명령을 결속합니다. Python 실제 분석 결과 및 context 10개를 PS_PRODUCER_SEAL로 추가 봉인한 뒤 PS가 읽었습니다. 원문 stdout/stderr, 외부 rc, 실패 스택, 사례별 이유·도달·미실행 목록과 선택 파일 전후 해시를 동봉합니다. 정적 N4 확인 1개는 기능 사례 수에 포함하지 않습니다.

최초 실패 후 수정·부분 재시험·추가 probe는 없었습니다. COMSOL/JVM/Java 컴파일/native/실제 입력·Job·정책 변경과 실제 승인 활성화도 없습니다. native_ready=false, 전체/정상 gate INCOMPLETE 및 기존 미확인 상태를 유지합니다.

다음 판단 대상은 PARENT_R113의 시험 입력 JSON 전달과 형식 assertion 한 곳입니다. 이미 통과한 결과의 재사용 여부와 이 실패 사례·후속 2개에 필요한 최소 검증 범위를 검토받을 수 있습니다. 이번 제출은 정정·재시험 또는 native 실행 승인이 아닙니다.
