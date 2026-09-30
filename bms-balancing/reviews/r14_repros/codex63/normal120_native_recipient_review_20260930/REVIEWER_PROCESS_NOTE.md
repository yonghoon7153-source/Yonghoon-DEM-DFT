# 검토자 작업 범위와 도구 정정

최종 전달 문서는 한국어다. 작업 도중 첫 안내의 언어가 잘못 나가 바로 한국어로 정정했다. 기술 판정과 무관한 안내 오류다.

이번 검토는 ZIP/JSON/로그/소스 텍스트 읽기, 안전한 별도 자료 추출, 검토자가 직접 작성한 CSV·기록 검산 및 보고서 작성이다. 받은 모듈 import·받은 시험·COMSOL/JVM/solver·정책 변경·외부 발송을 하지 않았다.

스프레드시트 읽기 전용 절차에 따라 원 CSV 바이트는 수정하지 않고 별도 Decimal 검산을 수행했다. 문서 작성 절차에 따라 기존 로컬 Markdown 검토 형식을 유지했다. 자체 검사 항목 수는 데이터 대조 횟수이며 생산 기능 시험 수가 아니다.

수신자는 보낸 측 전체 PC를 관측하지 않았다. 승인/사용자 입력·POST_WRITE·마지막 포장 도구 반환은 명시된 출처의 전사 자료로 처리했다. 현재 사용자 메시지의 ed5452를 새 JSON으로 보존했으며 보낸 측 원본 파일과 바이트 동일이라고 주장하지 않는다.

자체 작업 중 한 번의 읽기용 셸/Python 인용 구문 오류를 정정했다. 넓은 디렉터리 목록 출력도 있었으나 받은 파일 변경은 없었다. 마지막 보조 검사기의 첫 실행(chunk 7b6a8d, rc1)은 과거 검증 보충 ZIP이 현재 Downloads에 있다는 잘못된 경로 가정 때문에 FileNotFoundError로 중단됐다. 과거 ZIP을 다시 검증했다고 쓰지 않고, 이미 보존된 이전 수신 ARCHIVE_AUDIT의 식별과 비교하는 것으로 검사를 정정했다. 후속 보조 검사(chunk 949376, rc0) 44항목이 통과했다. 이는 검토자 데이터 도구의 정정이며 생산 코드/COMSOL 실행/기능 suite 실패가 아니다.

최초 오류의 대상 경로: C:/Users/Administrator/Downloads/NORMAL120_VALIDATION_DELIVERY_SUPPLEMENT_20260930.zip. 사용한 과거 대조 기록은 이전 normal120_validation_review_20260930/ARCHIVE_AUDIT.json이며 그 파일 식별과 해당 레코드는 SUPPLEMENTAL_AUDIT.json에 포함했다. 원래 과거 기록은 수정하지 않았다.

두 수신 ZIP의 최종 재해시와 검토 자료만의 봉인은 FINAL_SOURCE_CHECK.json / REVIEW_MANIFEST.json / REVIEW_DELIVERY_RECEIPT.json으로 구분한다. 이 검토 ZIP은 전체 원시 CSV/MPH의 재포장이 아니다.
