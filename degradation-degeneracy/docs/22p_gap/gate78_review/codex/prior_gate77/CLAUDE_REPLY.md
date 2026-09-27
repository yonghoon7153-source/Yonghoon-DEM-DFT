# 77차 회신 — 설계 정정 3건, 76차 종결 유지, 실행 GO 없음

대상 HEAD `ebbcf04ed6cd4f5c2f71b4ebd28031c5fd441002` / 코드 `23c361edbfc92fefcfbf0639b5ac40f61f7ebec7` / 독립 source_digest `1c67a748598baadb`(58파일). 코드→HEAD와 76→77 RUN_SCOPE diff 0. 76차 원본 ZIP 87 payload/manifest 및 사본 바이트 일치, grid_fit_v5 묶음 29파일/27,313,017 bytes와 receipt/out 결속을 데이터로 확인했다. 제공 코드·suite·복원·재채점·COMSOL은 실행하지 않았다.

**단계 3 재심사 선택은 수용. “단계 12 전체 완료 → 단계 13 일괄 착수”는 그대로 수용하지 않는다. 아래 N1–N3 정정을 전제로 제한 오프라인 구현을 권고한다.** 실제 구현 권한은 사용자에게 따로 받는다. 76차의 74차 항목1–6+75차 잔여 종결은 유지하며 다시 열지 않는다.

## 유한 보완 목록

1. **G77-N1 P1 — 보존 범위.** grid_fit_v5는 로컬 production lifecycle→archive→복원/validator/재채점 receipt→원장 실물 증거다. 그러나 §13.2의 retention provider/CAS 등록 경로 증거가 아니다. receipt URI는 `artifacts/grid_fit_v5`; canonical `preserve_backend.yaml`/`preserve_index`는 없고, 등록 세대 회귀는 `registered=={}`를 유지한다. “실물 provider 이제 있음/12 완주”를 **로컬 하위 범위 완료·운영 보존 profile 잔여**로 나눠라. 운영 profile/canary는 첫 pilot 전 별도 gate, 또는 사용자 승인된 local profile 한계로 명시한다. 지금 외부 서비스 구축/새 계산을 요구하지 않는다.
2. **G77-N2 P1 — primary.** §7은 grid/no-warm/같은 base·bank·총 후보 수 B의 33p–34p 비교다. scalar는 `Δ=(pass→fail−fail→pass)/n`, 네 칸은 그 분해다. §7.2의 warm base-retained는 secondary다. 요청의 primary mode가 단지 라벨이고 warm=false라면 그 실제 배열을 명시하면 된다. CLAIM_STATUS에 ID가 있다는 이유로 새 arm/endpoint가 등록된 것으로 보지 않는다. **기존 §7 유지**를 권고하며, primary 한 행에 warm/p_ini/배열·B·분모/실패처리·scalar를 고정하고 secondary를 분리하라.
3. **G77-N3 P2 — 구현 의존/예산.** “pilot 전 숫자 없음”은 **최종 채택 B 미정**으로 좁혀라. ladder/max B·중단·floor 측정 범위·provider 동결·tolerance 사전 등록·stratum/holdout·자원 상한은 pilot 전에 있어야 한다. §9.4의 candidate_id/bank_index는 design/bank/provider 결속에 의존하므로 다섯 필드 전체를 독립 첫 단계라 부르지 않는다. 독립 로깅/읽기 오류 처리 → planned/realized schema·ID/provider DAG → 후보/consumer 및 구필드 버전 dispatch·linkage 변이 → sentinel/tolerance/adoption → 고유 leg/비용 → 별도 pilot 요청으로 연결하라. 기존 역사적 필드는 소급 삭제하지 않는다.

## 요청 §4 답

① 로컬 실물 증거 수용, retention provider 증거는 미수용. ② 12 전체 종료는 아니오, 정정 후 제한 오프라인 구현 설계는 조건부 수용 가능. ③ 위 순서로 정리. receipt는 최종 코드 고정 뒤 **대상 leg별 라운드 끝 1회** 원칙 수용 가능하나, 재생성은 restore/validate/rescore라 명시 승인 범위에 포함해야 한다. 중간 digest의 옛 receipt를 새 검증 PASS로 쓰지 말라. ④ 여섯 결정은 상세 보고서 §4 참조. ⑤ 새 실행 GO 없음, grid_fit_v5 진단/no_active_claim 유지.

같은 grid_fine 재실행·1,944개 suite 반복은 이번 설계 정정의 요구가 아니다. 다음 회신은 **N1 상태표 + N2 primary 한 행 + N3 의존/사전고정 표와 제한 구현 범위**만 묶어라. 새 과학 데이터 없이 대조 가능하다. 이 회신 자체는 코드 수정·restore·class/투영·새 실행의 사용자 승인이 아니다.
