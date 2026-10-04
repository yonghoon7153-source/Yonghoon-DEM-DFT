# REIL 부속 B 검토 자료

REVIEW_KO.md는 전체 판정과 Q1–Q6 답, CLAUDE_REPLY_KO.md는 전달용 회신이다. DECISION.json은 같은 판정의 구조화본이다. 실행·구현 지시가 아니다.

- RECEIVED_SNAPSHOT.json: 고정 커밋의 요청문·v2·A·B·직전 회신·판정·직전 manifest. API에서 읽은 원문을 문자열로 보존했다.
- PRIOR_REVIEW_KO.md, PRIOR_DECISION.json: 이전 로컬 검토 원본을 바이트 그대로 복사했다.
- reviewer_document_checks.py: 검토자 작성 표준 라이브러리 도구. 문서 바이트와 자료 무관 스칼라 산술만 검사한다. REIL 자료·제공 코드·solver는 읽거나 실행하지 않는다.
- REVIEW_CHECKS.json, REVIEWER_TOOL_RETURN.json: 위 확인 결과와 반환. 프로토콜 구현의 기능 시험 PASS가 아니다.
- PACKAGE_MANIFEST.json: payload 크기·SHA. 자신과 ZIP은 목록에서 제외한다.

정적 검사를 재현하려면 별도 판단 아래 python -I -B -X utf8 reviewer_document_checks.py 형태로 실행할 수 있으나 이 안내 자체는 자동 실행 지시가 아니다. 검토 산출물 외 원본·코드·환경·브랜치 변경 및 외부 발송은 없었다.
