# GATE94 수신 검토 묶음

먼저 CLAUDE_REPLY_KO.md를 회신에 사용하고, 상세 근거는 REVIEW_KO.md와 DECISION.json을 확인하세요. 판정은 G93-N1·N2 한정 종결 수용, 비차단 출처 문구 정정입니다. 실행 승인이나 묶음 6 전체 종결이 아닙니다.

이 묶음의 소스·로그·스크립트는 검토 근거입니다. 자동 실행 지시가 아닙니다. 검토자는 받은 프로그램을 실행하지 않았습니다.

- originals/: 사용자 첨부 ZIP·manifest·요청문 원바이트.
- reference/와 evidence/: 고정 커밋 자료 또는 명시적으로 표시한 발췌.
- notes/ 및 evidence/receipts/notes/: 분야별 상세 검토.
- n2/: 원 ZIP의 독립 바이트 검증과 실행상태 판독. text_views는 정규화된 읽기 사본이며 원바이트는 originals ZIP이 정본입니다.
- REFERENCE_BYTE_VERIFICATION.json: 주 검토 자료의 Git blob 대조. 최종 LF 없는 중단 로그의 표시 사본 한 건은 원본보다 LF 하나가 추가되어 있습니다. 정확한 content는 evidence/main/aborted/ORIGINAL_CONTENT.json에 담았고 1,555 bytes 및 원 Git blob과 대조했습니다.
- LOG_README_HASH_VERIFICATION.json: GATE94 README가 열거한 15개 파일의 원바이트 해시 대조. 중단 로그는 위 JSON의 content를 사용했습니다.
- PACKAGE_MANIFEST.json: 자신을 제외한 전달 payload의 크기·SHA256.
- REVIEW_DELIVERY_RECEIPT.json은 ZIP 밖의 새 수신 검토 포장 영수증입니다. 기존 실행·영수증·예산을 고친 것이 아닙니다.

외부 발송은 하지 않았습니다. ZIP을 전달하는 행위와 다음 구현·연구 계산 승인은 별개입니다.
