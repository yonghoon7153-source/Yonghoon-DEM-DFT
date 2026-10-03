# 두 사전 검토의 전달 자료

고정 커밋 00ed85b4402169bae788b7269ffe69d76a0c40aa를 대상으로 한 2026-10-03 읽기 전용 검토다. PyBaMM 환경 고정과 REIL 외부 검증 프로토콜을 별도 판정했다. 실행 승인이나 G87-N1/GATE88 판정이 아니다.

- CLAUDE_REPLY_KO.md: 전달용 통합 회신.
- PYBAMM_REVIEW_KO.md: 근거 정정 3건, Q1–Q6, 목적별 환경/guard 권고.
- REIL_PROTOCOL_REVIEW_KO.md: 프로토콜 정정 R1–R6, Q1–Q8. 특히 외부 부등식이 명목값을 배제하는 문제.
- DECISION.json: 판정과 금지 범위.
- SOURCE_INDEX.json 및 reference/: 고정 커밋의 UTF-8 텍스트 사본. Python 사본은 .txt이며 실행하지 않았다.
- external/: 공식 PR/외부 소스/노트북 선택 셀. 노트북은 JSON 데이터로 읽었고 코드 셀·pickle은 실행하지 않았다.
- REVIEW_CHECKS.json: 문서 구조·참조·해시 확인. 연구 시험 결과가 아니다.
- PACKAGE_MANIFEST.json: 전달 payload 크기/SHA. ZIP 자체 식별은 ZIP 밖 DELIVERY_RECEIPT.json에 둔다.

검토 근거는 출처별로 구분했다. GitHub blob SHA는 원본 식별이고 로컬 텍스트는 LF·마지막 개행 정규화가 있을 수 있다. 원문 로그에 실린 수치는 제출자의 관측이며 이번 재실행 실측이 아니다. util_LFP.py는 CRLF/무개행 EOF를 복원한 메모리 바이트의 크기·SHA256·Git blob을 출처와 대조했다.

문서 작성 스킬은 결론·근거·권고·미확인 항목을 분리하고 원문 주장을 과장하지 않는 형식에 적용했다. 자료를 외부로 자동 전송하거나 cloud Page를 만들지 않았다.

확인 범위 밖: PyBaMM 새 설치/실행, 26.7.1↔26.8 비교, REIL xlsx 셀 내용 및 실제 fit, 논문 전문, 전체 저장소/운영 환경 보존 증명. 생산 소스·requirements·원장·영수증은 수정하지 않았다. 생성한 것은 이 별도 로컬 검토 폴더와 전달 ZIP뿐이다.
