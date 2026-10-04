# RTOL30 독립 검토 전달 자료

고정 rtol30_candidate_001의 30초 rtol 민감도 결과를 한정 수용한 검토 자료입니다. COMSOL 실행·제출 분석기 호출·새 시험·정책 변경은 하지 않았습니다.

- REVIEW_KO.md: 수용 범위, 독립 수치, 실행·보존·전달 경계와 다음 행동.
- CLAUDE_REPLY_KO.md: 그대로 전달할 회신. 자동 발송하지 않았습니다.
- DECISION.json: 원 상태와 분리한 독립 수용. 새 실행 승인 아님.
- ARCHIVE_AUDIT.json, NUMERIC_AUDIT.json, EVIDENCE_AUDIT.json: 수신자 검산·증거 대조.
- USER_PROVIDED_FINAL_RETURN_FIELDS.json: 사용자 메시지의 선택 필드 정규화. 원 sidecar 바이트 복사본 아님.
- REVIEWER_METHOD_NOTES.json: 수신자 보조 스크립트 정정과 수행 범위.
- reviewer_audit.py: 수신자 자체 대조 코드. 연구 실행·승인·생산 분석기가 아님.

대형 원 CSV/ZIP/MPH는 이 검토 묶음에 다시 넣지 않습니다. 원 ZIP 두 개는 ARCHIVE_AUDIT의 정확 식별로 연결합니다. 원본 영수증의 recipient=null, 실패·state·승인은 수정하지 않았습니다. 전체/정상 gate는 INCOMPLETE이며, 같은 rtol30 반복이나 다음 계산을 승인하는 문서가 아닙니다.
