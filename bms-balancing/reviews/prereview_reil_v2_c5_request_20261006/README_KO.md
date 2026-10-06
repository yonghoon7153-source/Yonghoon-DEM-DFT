# REIL C5 승인 요청문 사전 검토 전달본

2026-10-06. 고정 커밋 `7def9238c8fdac605decc5bf17c1428a93faad1d`에 대한 문서 검토다.

**판정:** 설계 방향 수용, 승인문 정정 필요. C5 구현·시험·비용 측정은 승인하지 않았다.

- REVIEW_KO.md: 근거, 5개 지적, 질문별 답, 원문 좌표.
- DOCUMENT_CORRECTIONS_KO.md: 작성자가 반영할 정정 문안 제안. 원문을 수정한 파일이 아니다.
- CLAUDE_REPLY_KO.md: 그대로 전달 가능한 짧은 회신.
- DECISION.json: 기계가 읽을 수 있는 판정과 권한 경계.
- READ_SNAPSHOT.json: 고정 커밋의 관련 문장, 허용된 P0 JSON의 선택 기록, 기존 옵션 JSON, 허용 util 157–236행. 실행용 소스가 아니다.
- PACKAGE_MANIFEST.json: 위 6개 payload의 크기와 SHA-256. manifest는 자기 자신을 해시하지 않는다.

승인 요청문 첨부와 고정 커밋의 원문은 전체 바이트 일치(15,765 bytes, SHA-256 `2656ab2bf142ea1ea64245f816cc8c7c4f5b6ac086d1ad28a50961d68bf85cc6`)를 확인했다. 나머지 저장소 근거는 READ_SNAPSHOT에 고정 커밋과 Git blob 식별을 연결했다. 발췌문 SHA와 원 파일 전체 SHA를 혼동하지 않는다.

REIL xlsx·pickle·노트북은 읽지 않았고, 맞춤·시험·Sobol 생성·설치·환경 재구축·COMSOL·Java를 실행하지 않았다. 기존 요청문·코드·자료·봉인·P0 기록을 수정하지 않았다. 새 검토 파일만 작성했다.

다음은 C5-N1–N5의 문서 정정이다. 사용자는 정정된 §10 (1)을 별도로 승인해야 하며, 구현 결과 제출 뒤 비용 측정은 다시 별도 승인한다. 자동 발송은 하지 않았다.

