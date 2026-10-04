# 89차 검토 자료 읽는 순서

먼저 REVIEW_KO.md 또는 전달용 CLAUDE_REPLY_KO.md를 읽는다. DECISION.json은 같은 판정의 구조화본이다. 이 묶음은 검토 자료이며 실행 지시가 아니다.

- RECEIVED_SNAPSHOT.json: 고정 GitHub ref에서 읽은 29개 파일과 비교·tree 메타데이터. 소스와 로그는 JSON 문자열로 보존했다. 요청 후 추가된 14번 로그의 ref는 별도 표시했다.
- PRIOR_RUN_SCOPE_SNAPSHOT.json 및 PRIOR_RECEIVED_SNAPSHOT.json: 이전 88차 검토 입력을 바이트 그대로 복사했다. 새 소스 digest 계산은 현행 tree의 동일 blob으로 확인된 57개 이전 파일과 새 preserve.py를 사용했다.
- STATIC_AUDIT.json 및 PRODUCTION.diff: 검토자 독립 바이트·SHA·AST·텍스트 대조 결과. YAML core hash 재계산이나 시험 실행 결과가 아니다.
- reviewer_static_audit.py: 표준 라이브러리만 쓰는 검토자 작성 정적 검사기. 수신 코드를 import/실행하지 않는다. 재현 명령 형태는 python -I -B -X utf8 reviewer_static_audit.py이다. 자동 실행하라는 지시는 아니다.
- REVIEWER_TOOL_RETURNS.json 및 REVIEWER_FINAL_STATIC_RETURN.json: 검토자 정적 도구의 출력 인코딩 실패와 이후 성공 반환. 생산 시험 로그와 구분한다.
- PACKAGE_MANIFEST.json: 위 payload의 바이트·SHA 목록. manifest와 ZIP은 자신의 payload 목록에 포함하지 않는다.

첫 정적 도구 출력은 CP949 때문에 실패했고 UTF-8 옵션으로 출력했다. 최종 재현본은 이전 입력을 같은 폴더의 보존 사본으로 읽도록 경로만 바꿨으며 결과는 동일했다. 별도 Python YAML 라이브러리를 설치하지 않았고, 영수증은 원문 차이와 보존 식별·제출 실행 로그의 범위로 확인했다.

이 자료를 작성하면서 작업 저장소의 코드·운영 원장·영수증·브랜치는 수정하지 않았다. 외부 전송도 하지 않았다. 압축 묶음 작성은 검토 산출물 포장이며 연구 프로그램 실행이 아니다.
