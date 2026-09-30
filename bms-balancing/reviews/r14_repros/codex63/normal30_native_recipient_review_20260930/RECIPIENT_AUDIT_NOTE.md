# 수신 검산 도구 수정 기록

수신자가 새로 작성한 audit_numeric.py의 첫 실행(chunk 0d7c10, rc1)은 로그 완료 표식을 줄 전체 `PREFLIGHT_SOLVER_RETURNED=true`로 잘못 가정해서 중지했다. 실제 원문은 `PREFLIGHT_SOLVER_RETURNED=true; physical checks separate`였다. 원문을 확인한 뒤 정확한 전체 줄을 비교하도록 수신 검산기 한 줄만 정정했다. 최초 비교식은 `console_markers.count('PREFLIGHT_SOLVER_RETURNED=true')==1`, 정정 비교식은 `console_markers.count('PREFLIGHT_SOLVER_RETURNED=true; physical checks separate')==1`이다.

이는 수신 독립 검산기의 문자열 가정 오류이며 생산 코드·COMSOL 계산·송신 시험 실패가 아니다. ZIP/수신 원자료는 수정하지 않았다. CSV 검산을 포함한 수신 자체 도구를 다시 실행했으며, 받은 시험/소스/COMSOL을 실행한 것은 아니다.

초기 파일 목록 조회에서 존재하지 않는 units_point1.csv 및 run/PRESERVATION_AFTER.json 경로를 읽으려 한 오류도 있었다. 실제 단위 자료는 units_point1_configured/evaluated.csv이고 전달 보존 자료는 supplement/PRESERVATION_AFTER.json이다. 없는 자료를 생성하거나 추정으로 채우지 않았다.

기록 검사기의 첫 시도(chunk c8f4e9, rc1)는 validation release의 참조 17개가 모두 이전 수신 디렉터리에 들어 있다고 잘못 가정했다. 실제 검사 결과 핵심 검증 기록 외 사전 실행 경로/승인 문서 일부는 참조만 있고 이 수신본에는 없었다. 이를 누락을 무시한 전체 검증 PASS로 바꾸지 않고, 참조별 실제 바이트 대조 여부를 RECORDS_AUDIT.json에 남기고 핵심 검증 기록 대조와 미포함 참조를 분리했다. 이전 수신 보고서 및 명시된 Downloads 원본 ZIP도 동일 SHA 여부만 확인한다. 수신 검토 중 UTF-8 인코딩을 생략한 일회성 JSON 조회는 cp949 오류로 종료됐고, read_bytes/명시 UTF-8으로 정정했다. 생산 산출물에는 변경이 없다.
