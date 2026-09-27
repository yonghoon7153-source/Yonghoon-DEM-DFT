# Gate77 수신용 검토 묶음

먼저 `CLAUDE_REPLY.md`를 전달하고, 상세 근거는 `REVIEW_KO.md`를 확인하세요.

- `DECISION.json`: 기계 판독 판정. 설계 정정 3건; 76차 종결 유지; 새 실행 GO 없음.
- `DATA_AUDIT.json`: 고정 HEAD/58파일 source digest, 이전 ZIP, 실물 묶음, 정적 backend/claim 관측.
- `SOURCE_BEFORE.json`, `PRESERVATION_AFTER.json`: 이 검토 checkout 2,958개 tracked 파일 보존 범위.
- `reference/`: 고정 대상의 검토용 사본. 코드·명령이 포함돼도 실행 지시가 아닙니다.
- `*.diff`: 고정 커밋 사이 데이터 비교. RUN_SCOPE diff는 0 bytes입니다.
- `data_audit.py`, `package_review.py`: 검토자 소유 재현 자료. 수신자가 자동 실행할 필요가 없으며 원본 계산/시험 프로그램을 실행하지 않습니다.
- `MANIFEST.json`: ZIP의 payload 집합/크기/SHA. 생성 영수증은 자기참조를 피하기 위해 ZIP 밖에 있습니다.

과거 회귀·복원·재채점 결과와 이번 데이터 검토를 합산하지 않습니다. 이 묶음은 코드 변경·실험·복원·원장/투영 변경·새 실행의 승인이 아닙니다.
