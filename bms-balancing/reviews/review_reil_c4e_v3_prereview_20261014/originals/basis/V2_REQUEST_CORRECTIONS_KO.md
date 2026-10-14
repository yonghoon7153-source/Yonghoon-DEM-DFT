# REIL C4E v2 승인 전 최소 정정

고정 HEAD `dc6e5b7e043ff11b73095ddb9d60db7837e665c7`의 요청문에 대한 문서 정정 제안이다. 구현·시험·자료 반입 승인이 아니다. 원문은 보존하고 다음 revision에 반영한다.

## 1 회귀시험 예외표

요청문 289–293행 및 발송문 대응표.

- COBYQA: “14실행 · 실행당 내부 목적평가 ≤50 · 정상 반환 뒤 독립 재평가 ≤1”. 내부/독립 계수를 섞지 않는다.
- 비최적화 보존 util: “test_06은 extract_battery_data≤5, objective_fun≤3, dVdQ_hc≤9. 0b2 h_1–h_4는 extract_battery_data≤4, objective_fun=0, dVdQ_hc≤48의 보수 상한. 중첩 API 진입을 각각 센 정적 상한이며 optimizer는 0.” 기존 ≤120을 유지하면 해당 계수 단위를 함께 적고 “몇 회”를 없앤다.
- 실제 fork: “기존 10 + 새 5 = GREEN 15, 상한 17”. n3_a/n3_b는 대본 Process이고 실제 fork 0, c_8은 실제 두 파로 2다. 새 경합 대조를 추가 fork로 선택하면 새 6/합계16으로 갱신하되 상한을 늘리지 않는다.
- 가짜 minimize≤995, Sobol 관련 15시험, 기존159+새21=180의 구분은 유지한다. Sobol 시험 수를 생성 호출 수로 바꾸지 않는다.

## 2 최종 기록과 예산

요청문 111–112, 133–136, 174, 214–215, 251행. 아래 의미를 포함한다.

> E3a의 최종 기록 수용은 끝 식별 재해시와 단계 내 마지막 끝 기록의 저장·재읽기까지 끝난 뒤 확정한다. 같은 산출 루트 전체 크기와 최종 monotonic snapshot을 사용한다. 9,900초 기록 마감과 10,800초 단계 한도가 각각 어느 마지막 작업을 포함하는지 고정하며, 끝 기록 뒤 크기·시간 초과나 쓰기·재읽기·식별 실패를 앞선 final_record의 COMPLETE로 가리지 않는다. 실패 시 E3a INCOMPLETE/C4-A=false를 유지하고 이미 받은 행·파일·오류는 보존한다. 마지막 유한한 확인 snapshot 뒤 외부 도구 반환 및 후속 전사 시간은 별도이며 snapshot에 포함됐다고 하지 않는다.

순서는 끝 sha와 끝 기록을 마지막 final_record 안으로 이동하거나, 같은 조건을 검사하는 후속 종결 단계로 명시할 수 있다. 구현을 여기서 수행하지 않는다.

s_3에 끝 재해시 지연, 마지막 기록에 의한 크기/시간 초과, 66 returned+global_stop/freshness 실패를 각각 명시한다. 단순 record_state 입력만으로 마지막 종결 경로를 대조했다고 하지 않는다.

## 3 active 중지와 최종 drain

요청문 144–145, 216, 241행.

> active 초과는 중단 요청 대상으로 기록한다. 최종 drain 이후 done이 없으면 STARTED_INTERRUPTED, done이 있으면 원래 COMPLETED와 termination을 보존한다. returned/error 모두 보존하고 감지 당시 active 초과 기록 및 global_stop을 취소하지 않는다. 마지막 drain에서 추가된 완료 행의 wall도 상한과 대조하여 늦은 완료 초과 목록을 완성한다. 따라서 전체 판정은 INCOMPLETE다.

r_6에 “active 초과 감지 → 중지 요청 → 마지막 drain에서만 done 수신”을 명시한다. 실제 반환을 보존하는 순수 집계 fixture 또는 추가 fork 중 어느 방식을 쓸지 사전에 정하고 세션 표와 연결한다.

## 유지할 정정

지역 오류와 E3a 성공의 구분, 66 returned의 AND 조건, NE/reference 둘/실제 소비 배열 결속, 공통 원점과 비용 입력 검증, M1 바이트 관계·인용, E0 뒤 별도 E1 GO는 되돌리지 않는다. 과거 실패·누락·승인 이탈 기록과 H 배열/H4 의무의 유보를 유지한다.
