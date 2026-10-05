# GATE91 검토 인계

판정: ACCEPTED — G90-N1·C1 및 환경 프로필 C 기록 대조 라운드 종결. 실행 GO 아님.

- `CLAUDE_REPLY_KO.md`: 제출자에게 전달할 회신.
- `REVIEW_KO.md`: 근거·수용 범위·시험/영수증/자체 신고의 상세 판정.
- `DECISION.json`: 기계 판독용 판정.
- `STATIC_AUDIT.json`: 검토자 소스·AST·digest·로그/영수증 대조 결과.
- `REFERENCE_TEXT.json`: 고정 커밋에서 읽은 원문, 참조 및 식별.
- `REQUEST_TREE.json`, `GIT_COMPARISONS.json`, `FIXED_TABLE_AND_CODE_COMMIT.json`: 고정 트리/변경 범위/코드 변경 전 표 대조.
- `SOURCE_DIFF.txt`, `TEST90_DIFF.txt`, `MUTATION_DIFF.txt`, `*_RECEIPT_DIFF.txt`: 읽기용 변경 대조.
- `EXPECTED_LOG_HASHES.json`: 제출 README의 로그 식별 목록.
- `RECEIVED_REQUEST.md`: 수신 첨부 원문 사본.
- `prior_review_data/`: 현재 tree/blob에 결속해 재사용한 이전 검토 사본.
- `REVIEWER_TOOL_RETURNS.json`: 검토자 참조 목록 오류 두 건과 수정 후 정적 대조 반환. 제출 시험 실패와 별개다.
- `reviewer_static_audit.py`: 검토자가 작성한 데이터 점검 코드. 수신자에게 실행을 지시하는 파일이 아니다.
- `PACKAGE_MANIFEST.json`: 자신을 제외한 payload의 크기/SHA. 전달 ZIP 및 외부 영수증은 이 디렉터리 밖에 둔다.

제출 프로그램·pytest·smoke·변이·COMSOL·PyBaMM·JVM·설치·복원은 이번 검토에서 실행하지 않았다. 기록된 시험 결과는 제출자 원문 확인이며 독립 재실행이 아니다. 저장소/원장 변경이나 외부 자동 발송도 하지 않았다.
