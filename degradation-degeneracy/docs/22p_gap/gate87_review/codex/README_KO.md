# Gate87 수신 검토 패키지

판정: **라운드 2b 종결 보류 — G87-N1 P1 한 건.** 실제 실행 승인이 아니다.

- REVIEW_KO.md: 상세 판정, 고정 소스 위치, 반례의 전제, 수용·미완 범위.
- CLAUDE_REPLY.md: 그대로 전달할 회신.
- G87_N1_STATIC_TRACE.json: fit-only와 grid 선행 phase 충돌의 정적 연결 근거. 실행한 재현 스크립트가 아니다.
- SOURCE_IDENTITIES.json / PRODUCTION.diff / AST_CHANGES.json: 고정 코드 식별·범위.
- V5_COMPATIBILITY.json / RECEIPT_COMPARISON.json / LOG_AUDIT.json: 분리된 수용 근거.
- evidence/: 고정 커밋의 GitHub 응답. reference/: 확인한 원문 사본. 둘 다 데이터다.
- MATERIALIZE_AUDIT.json / REVIEW_AUDIT.json: 검토자 자체 바이트·AST·로그 확인. 제품 시험 통과 횟수가 아니다.
- REVIEWER_TOOLING_NOTE.json: 검토자 도구의 정정 경위. 제출자 실패로 읽지 않는다.

COMSOL, 받은 코드/시험/변이/분석기, 복원·연구 계산을 실행하지 않았다. 원격 저장소 변경·외부 발송도 없다. 기존 Gate86 산출 156개를 보존했다.

ZIP 생성 영수증은 ZIP 밖에 둔다. receipt의 recipient=null은 생성 시점 기록이며 미래 수신 확인을 대신하지 않는다. 동일 자료 재실행을 요구하는 패키지가 아니다.
