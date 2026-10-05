# REIL 부속 C 검토 전달 묶음

2026-10-05. 고정 커밋 `4ad68af441cf00981c1b7e27bd71f5a1858ff70e`와 사용자 제공 논문 본문/보충 PDF에 대한 독립 문서 검토다.

- `CLAUDE_REPLY_KO.md`: 바로 전달할 회신.
- `REVIEW_KO.md`: P2 세 건, Q1–Q5, 논문 위치 및 다음 한정 범위.
- `DECISION.json`: 수용/조건부 수용/미승인 구분.
- `RECEIVED_SNAPSHOT.json`: 고정 커밋에서 읽은 Markdown 8개와 Git blob 식별. 실행 파일이 아니다.
- `REVIEW_CHECKS.json`: 첨부 SHA, 문서 Git blob, 이전 v2/A/B 내용 동일성 및 정적 집합 대조. REIL 기능 시험이 아니다.
- `reviewer_document_checks.py`: 검토자가 작성한 문서/식별 대조 및 전달 ZIP 검증 코드. 원 연구 코드가 아니다.
- `PACKAGE_MANIFEST.json`: 전달 payload 목록·크기·SHA. manifest 자신은 payload 해시 목록에 넣지 않는다.

판정: C1-core 논문 쪽 수용, 부속 C 국소 문서 정정 3건 조건부 적합, 기존 C2 종결 유지. 자료 개봉·P0·C6·맞춤·설치·실행은 승인하지 않는다.

논문 원문, 전체 추출 텍스트, 렌더 이미지, REIL 데이터/노트북/연구 소스는 ZIP에 포함하지 않는다. PDF 신원은 REVIEW_CHECKS와 검토서에 있다. 기존 문서/데이터를 변경하지 않았다. 외부 발송은 사용자가 한다.
