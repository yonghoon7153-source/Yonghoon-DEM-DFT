# NEXT_RUN_PLAN — B 물리축 5초 계산1회 후 정지

**전체 수렴 미완·장시간 운전 보류.** 승인된 B 한 건을 완료하고 추가 실행은0회다. 권장/승인된 Astra High·16코어·1800초 예산을 사용했다. 기준 해는 재실행하지 않았다.

기준: Caps300R320H0125C16 / 5d1a87652ed54e6a945d4f2af4aeda70 / source SHA 4db47e27dcf0d8d2977dc786dab2c3ba40e98a6adf42d7201bf1c66ab802537e.
새 B: Caps600R320H0125C16 / 56975e4d24054b23bcec87553875f729 / source SHA f230dcc0ccc2bb88c73b978ad9ebc564eb5e1c72cd328f24802d3f4435623906.

물리 메시만300(120/60/120)→600(240/120/240)으로 변경했다. 입자320/320·16코어·원래 cap `if(t<0.1[s],0.000125[s],0.1[s])`·초기화·물성·OCP·Li·0.1C·sigma·허용오차·scale·보호·187요청시각·전극별241좌표를 유지했다. 후기 cap A를 혼합하지 않았다.

판정: **지정 표본의 물리축 300→600 세분 민감도 기준 충족**. 0–5초 요청187시각 최대 전압 차 1.06511000E-8mV @0.001s, 최대 pointwise x 차 5.2300400E-9 @5s/P/121.000000µm. 공통 저장 교집합은987시각이며 별도로 채점했다. 전체8창·동시 성분·actual step은 [결과 보고서](physical600_b/PHYSICAL600_B_RESULTS_KO.md)에 있다.

같은 시간상한이 같은 accepted 이력이나 새600 메시의 시간 정확도를 뜻하지 않는다. 표본 기준을 충족해도 참값 오차·전체 수렴·장시간GO로 확대하지 않는다. 실패 또는 기준 초과가 있으면 해당 상태를 유지하며 맞추기 위한 보정/자동재시도를 하지 않는다.

다음 실행 승인횟수는0이다. 추가 메시·시간조건 시험, 전체 프로토콜·12시간 휴지·유한sigma·sweep은 별도 승인 대상이다. 다음 계산 전에 추론 수준·이유·실행 조건과 횟수·자원·중단 예산을 먼저 제시하고 사용자 승인을 기다린다.

OCP 외삽 none, StopCondition 노드1개/활성 조건2개, 기존 failed/INCOMPLETE_RANGE_STOP을 보존한다. 전해질 양수는 **후처리 검사**다. 초기 전압을 맞추거나 OCP·초기 조성·Li를 변경하지 않는다.

CORE16_CONTROL 수신 확인은 별도 [수신 기록](physical600_b/RECEIPT_CONFIRMATION.json)으로 추가했다. 당시 현지1,247개 중 직접93개(92불변+계획서 변경 전 사본1개)의 외부 확인이며 전체 현지 파일 검증이 아니다. 역사333개는 별도 보관 범위다. 이전 A 결합 비교와 원본 영수증을 유지하며, TIME_CAPS 두 raw ZIP 차이 원인은 미확인이다.

[변경 전 계획](physical600_b/NEXT_RUN_PLAN_before_physical600_b.md), [계약](physical600_b/comparison_contract.json), [원시 재검산](physical600_b/results/raw_arithmetic_recheck.json), [COMSOL Time API](https://doc.comsol.com/6.3/doc/com.comsol.help.comsol/comsol_api_solver.51.50.html).
