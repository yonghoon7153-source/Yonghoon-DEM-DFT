# NEXT_RUN_PLAN — 전해질 guard 제한 시험 후 정지

**필수 검사 미완/실패 — 추가 실행 중지. 전체 수렴 미완·장시간 운전 보류.**

사용자가 선택한 목적은 provisional 기능 진단이다. 승인된 정상/발동 최대2회 중 1개 job을 제출했고, 기준 해는 재실행하지 않았다. Astra High,16코어,각 물리5초 이하/worker1800초 범위다. 추가 실행 승인0회, 자동 재시도 없음.

원래 Caps300R320H0125C16과 정상 guard 복제본,1198 시험 fixture를 구분한다. 시험 fixture는 정상 기준으로 승격하지 않는다. 이번 기능 결과는 [결과 보고서](electrolyte_guard/ELECTROLYTE_GUARD_RESULTS_KO.md)와 [계약](electrolyte_guard/comparison_contract.json)에 있다.

현행 원본의 전해질 양수는 후처리 검사다. 별도 새 복제본에 solver Minimum 기반 step후 중단을 추가했다. 모든 순간/공간의 양수성, 실제cl=0접근시 안정성, 모든domain 개별발동을 보장하지 않는다. 입자 내부 보호, 고해상도 모델의CDC/장기시간제어 통합, 원본6.4/실험 대응은 별도 미완이다.

기존 CDC 시작·짧은 전이 시험은 재사용할 근거이며 현행 고정전류 모델에 장기 프로토콜이 통합됐다는 뜻은 아니다. 과거 반경80→160 기준 초과는 보존하고 후속 표본 충족을 전체 수렴으로 확대하지 않는다. OCP 외삽금지·초기조성/Li/물성·원본·failed/INCOMPLETE_RANGE_STOP을 유지하며3.0524V로 맞추지 않는다. TIME_CAPS raw ZIP 차이 원인은 미확인이다.

후보C·추가 보호/시간/메시 solve·전체 프로토콜·12시간휴지·유한sigma·sweep은 모두 별도 승인이다. 이번 전달 후 정지한다. 다음 작업이 필요하면 목적·단일 변경축·기준·횟수·성공/실패 기준·자원·추론수준을 먼저 제시하고 승인을 기다린다.

[변경 전 계획](electrolyte_guard/NEXT_RUN_PLAN_before_guard.md), [기존 목적/준비도 문서](NEXT_MODEL_READINESS_DECISION.md). 기존 문서/영수증/ZIP은 당시 기록으로 보존한다.
