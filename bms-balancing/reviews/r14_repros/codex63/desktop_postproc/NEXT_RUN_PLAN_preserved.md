# NEXT_RUN_PLAN — 전해질 후처리 복구 접근 차단 후 정지

**정상 필수 검사 미완. 후처리 복구도 INCOMPLETE_RECOVERY / BLOCKED_COMSOL_FILE_READ_SECURITY. 전체 수렴 미완·장시간 운전 보류.**

원래 정상 job `56ef13bee5a448c5a029b02656ebf6bb`의 worker failed와 INCOMPLETE_POSTPROCESSING_UNDEFINED_COORDINATE는 유지한다. 복구 job `28f40815e3a3410aab411ec93cd36fe1`는 별도 후처리 제출 1건이며 COMSOL 파일 읽기 보안 설정에서 차단됐다. 새 solve0회·발동시험0회·복구 재시도0회다. 입력 원본/복사본은 전후 SHA 동일이다. 새 수치 CSV/MPH는 없고 실제 native reopen·필수 출력·비교는 미완이다.

수신 검토가 확인한 원래 MPH의987 저장시각 메타데이터와 바이너리 리소스는 복구 가능성의 근거이며 이번 API 회수 성공은 아니다. 기존 생성영수증·ZIP·실패/audit/gate는 보존했다. [복구 결과](electrolyte_recovery/RECOVERY_RESULTS_KO.md)를 참조한다.

다음 제안 1건: COMSOL 파일 접근 정책·허용 로드 경로의 읽기 전용 검토. Astra High, 동일 입력 SHA, 새 solve0·재제출0·설정변경0. 구현/재호출 전에 최소 변경·영향·자원을 제시하고 별도 사용자 승인을 기다린다. 이번에는 그 검토나 변경을 시작하지 않는다. 기존 187시각·241좌표·1mV/1e-4 기준은 유지한다.

사용자 목적은 provisional 기능 진단이다. 기존 기준 Caps300R320H0125C16은 재실행하지 않는다. 기존 모델의 전해질 양수는 후처리 검사이고 새 정상 복제본의 solver guard는 필수 검증 미완이다. 발동 시험은 별도 승인이다. 입자 내부 보호·현행 모델 CDC/장기 제어 통합·원본6.4/실험 대응·전체 수렴도 미완이다.

OCP 외삽금지·원본/초기조성/Li·기존 failed/INCOMPLETE_RANGE_STOP 보존, TIME_CAPS raw ZIP 차이 원인 미확인을 유지한다. 후보C·추가 보호/시간/메시 solve·전체 프로토콜·12시간휴지·유한sigma·sweep은 보류한다. 연속 시공간 양수성을 주장하지 않는다. 전달 후 정지한다.

[변경 전 계획](electrolyte_recovery/NEXT_RUN_PLAN_before_recovery.md), [기존 목적·준비도](NEXT_MODEL_READINESS_DECISION.md).
