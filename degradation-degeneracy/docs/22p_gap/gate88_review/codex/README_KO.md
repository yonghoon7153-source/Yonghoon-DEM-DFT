# Gate88 회신 자료

먼저 REVIEW_KO.md를 읽고, 회신에는 CLAUDE_REPLY.md를 사용하세요.

판정은 G88-N1 P1 한 건에 대한 수정 요청입니다. 원래 정상 fit-only 완료 연결은 수용하고, durable receipt.inputs의 최종 재검증 누락 때문에 2b 종결만 보류합니다. 실행 승인이나 자동 실행 지시가 아닙니다.

- DECISION.json: 판정과 미승인 범위
- G88_N1_STATIC_TRACE.json: 단일 필드 삭제 반례의 정적 경로
- STATIC_AUDIT.json: 원문 Git blob, 로그 크기/SHA, 58파일 source digest, 이전 함수 AST 및 영수증 차이
- PRODUCTION.diff: 이번 생산 변경 두 파일
- RECEIVED_SNAPSHOT.json: 고정 커밋의 검토 소스·문서·로그 원문 문자열
- RUN_SCOPE_SNAPSHOT.json: 58개 파일과 Git tree 식별
- PRIOR_REFERENCE.json: 87차 기준 원문·tree·회신
- REVIEWER_METHOD.json: 관측/추론/실행 경계
- reviewer_static_audit.py: 검토자 작성 데이터/AST 확인 코드. 받은 파일을 import하지 않음. 수신자 자동 실행을 요구하지 않음.
- PACKAGE_MANIFEST.json: 전달 payload 크기/SHA

원래 실패·중단·baseline 오염 신고를 지우거나 새 PASS로 바꾸지 않았습니다. 연구 계산·COMSOL·pytest·변이·복원 재실행은 하지 않았습니다.
