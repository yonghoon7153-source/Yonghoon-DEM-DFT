# 검토자 수행 범위

검토자는 두 수신 ZIP을 데이터로 해시·CRC 검사하고 새 검토 폴더에 복사/해제했다. 받은 Python/Java/PowerShell/class를 import 또는 실행하지 않았다. COMSOL/JVM/launcher·생산 분석기·기존 시험·현지 토큰/정책/프로세스 조회는 수행하지 않았다.

audit_archives.py, audit_numeric.py, audit_records.py, audit_supplemental.py, audit_additional.py는 검토자 작성/기존 검토자 코드에서 적응한 stdlib 전용 대조기다. 저장 CSV의 Decimal 계산과 JSON/로그/바이트 검사를 수행했다. 기능 시험이나 새 물리 계산으로 집계하지 않는다.

문서 작성 지침에 따라 직접 수신 바이트 대조, 보낸 측 실행 기록, 사용자 콘솔/도구 반환의 후속 전사를 분리했다. CSV 검토 지침에 따라 단위·시각·행 단위·출처·미확인 범위를 보존했다. spreadsheet나 source CSV를 수정하지 않았다.

사용자 제공 마지막 포장 반환은 USER_SUPPLIED_FINAL_RETURN.json에 의미상 필드를 전사했다. 원 도구 반환의 독립 수신 관측 또는 원래 직렬화 바이트라고 주장하지 않는다. 기존 원문과 receipt recipient=null은 변경하지 않았다.

수신 자료의 전체 보호 범위는 아니며 파일 접근이 가능한 두 ZIP의 검토 전후 식별은 FINAL_SOURCE_CHECK.json으로 확인한다. 새 검토 산출물만 포장하며 대형 원자료를 재포장하지 않는다. 외부 발송/새 실행 승인 없음.
