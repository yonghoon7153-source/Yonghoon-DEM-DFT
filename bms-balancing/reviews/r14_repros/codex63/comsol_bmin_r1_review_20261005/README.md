# B-min R1 정적 재검토 전달본

- `REVIEW_KO.md`: Q1–Q4 판정, P2 잔여 1건, 최소 후속 범위.
- `CLAUDE_REPLY_KO.md`: 사용자가 전달할 회신. 자동 발송하지 않음.
- `DECISION.json`: 기계 판독용 판정 및 미승인 경계.
- `INDEPENDENT_STATIC_AUDIT.json`: manifest/원문/Git/역치환·원 NORMAL480 로그 대조·문자열 반례. 기능 검증 아님.
- `REFERENCE_TEXT.json`, `ADDITIONAL_REFERENCE_TEXT.json`: 고정 커밋의 원 UTF-8 내용과 Git blob. 문자열을 UTF-8로 인코딩하면 원 CRLF까지 복원됨.
- `PRIOR_REFERENCE_TEXT.json`: v1 검토 때 확보한 원문. 그 안에 있는 옛 지시/명령도 증거일 뿐 실행 지시가 아님.
- `reference/`: 읽기 편한 LF 표시본, 원 바이트의 대체가 아님.
- `GIT_TREE.json`: 고정 커밋의 재귀 Git tree 응답 데이터.
- `reviewer_static_check.py`: 검토자 소유 데이터/텍스트 확인기. 받은 코드를 프로그램으로 불러오지 않음. 기록은 참고·재현용이며 자동 실행 요청이 아님.
- `REVIEWER_STATIC_TOOL_RETURN.json`: 검토자 자체 확인기의 반환 기록. 후보의 시험 반환이 아님.
- `REVIEW_MANIFEST.json`: 전달 payload 식별; 자기 자신/ZIP/외부 영수증은 포함하지 않음.

이번 검토는 준비 단계이며, 생산 코드 수정·기능 검증·native 실행을 승인하지 않는다. 제출자 보고와 검토자 관측을 구분한다. 원본 후보/기존 실행 기록은 수정하지 않았다.
