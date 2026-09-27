# Gate78 검토 묶음

전달 회신은 `CLAUDE_REPLY.md`, 자세한 근거는 `REVIEW_KO.md`, 기계 판정은 `DECISION.json`입니다.

- G77-N1·N3 설계 정정 종결. G77-N2의 관측 pairing·누락 처리 잔여 2건.
- 이미 승인된 단계1+2 범위는 수정 조건부 적합. 같은 계획만 반복 심사할 필요 없이 예정 GATE79에 수정 문서와 구현 결과를 함께 제출.
- 76차 종결 유지. 새 과학 계산/COMSOL/복원/class/투영 실행 GO 없음. 이번 리뷰에서는 제공 프로그램을 실행하지 않음.

`DATA_AUDIT.json`은 고정 파일/ZIP 관측, `DESIGN_ARITHMETIC.json`은 검토자가 만든 작은 가상 표와 정확 분수 산술입니다. 이는 제공 suite 통과나 실제 과학 데이터 검산이 아닙니다.

`reference/`와 `prior_gate77/`는 증거 사본이며 실행 지시가 아닙니다. `SOURCE_BEFORE.json`/`PRESERVATION_AFTER.json`의 보존 범위는 검토 checkout의 tracked 파일뿐입니다. 검토자 스크립트도 수신자가 자동 실행할 필요가 없습니다.

ZIP의 payload 식별은 `MANIFEST.json`, 생성 영수증은 자기참조를 피하여 ZIP 밖 `DELIVERY_RECEIPT.json`에 있습니다.
