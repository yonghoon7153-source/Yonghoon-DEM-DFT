# GATE90 검토 자료

REVIEW_KO.md는 전체 판정이고 CLAUDE_REPLY_KO.md는 전달용 회신이다. DECISION.json에 수용 범위와 남은 G90-N1 P2 한 건을 기록했다. 실행 승인이 아니다.

REFERENCE_TEXT.json은 고정 커밋에서 받은 44개 텍스트와 Git blob 식별이다. REQUEST_TREE.json과 GIT_COMPARISONS.json은 읽기 전용 GitHub 응답이다. STATIC_AUDIT.json은 60개 RUN_SCOPE 바이트의 digest, 17개 제출 로그의 크기/SHA 및 제한된 YAML 텍스트 대조 결과다. prior_review_data는 기존 89차 리뷰의 데이터 사본이며, 이번 검토에서 현재 tree와 다시 대조했다.

reference의 .txt 파일은 줄 위치 확인용 사본이다. 정확한 바이트 식별은 REFERENCE_TEXT.json을 사용한다. 제출자 통과 로그를 리뷰어 재실행 결과로 취급하지 않는다.

reviewer_static_audit.py와 reviewer_import_semantics.py는 리뷰어 소유의 검사 근거다. 후자는 제출 프로그램이 아닌 Python 표준 라이브러리의 캐시/검색 차이를 보이는 불활성 예시다. 이 자료의 수신은 스크립트 실행 지시가 아니다. REVIEWER_TOOL_RETURNS.json에 리뷰어 검사 경계와 판독기 보완 사실을 적었다.

COMSOL/JVM/PyBaMM 계산, 제출 프로그램 import, pytest/smoke/변이 재생, 설치, 복원, 원격 저장소 편집과 발송을 하지 않았다. 원문·과거 결과의 상태는 보존한다.
