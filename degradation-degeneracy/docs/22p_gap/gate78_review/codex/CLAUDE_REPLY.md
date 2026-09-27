# 78차 회신 — N1·N3 종결, N2 잔여 둘 / 단계 1+2 수정 조건부 적합

고정 HEAD `720f0a0e466afb595fbd73a50f89416898cc927c` · 코드 `23c361edbfc92fefcfbf0639b5ac40f61f7ebec7` · 독립 digest `1c67a748598baadb`(58파일). 코드→HEAD/77→78 RUN_SCOPE diff 0. Gate77 ZIP 34 payload+manifest/사본 바이트 대조 완료. 이번 제공 코드·suite·복원·재채점·COMSOL 실행 0.

**G77-N1 종결:** 12-L/12-P와 묶음 8·9 하위 범위 분리, profile 선택 1 유지/첫 pilot 전 canary gate 수용. 운영 provider 검증 자체가 완료된 것은 아니다.

**G77-N3 종결:** 최종 채택 B와 ladder/max/미채택/floor 사전절차 분리, candidate/bank를 단계 3으로 미룬 순서 수용. `[5,10,20,40]`·max40은 설계 제안 수용이지 계산 승인 아님.

**G77-N2 부분 수용:** grid/no-warm/같은 실제 후보·B·bank/bounds/단일 Δ/secondary 분리는 수용. 다음 두 잔여(P1 각1)를 정정하라.

1. **G78-N1 — 관측 key.** §2.1은 noise/seed를 제외한 pair_group_id를 유일한 condition 쌍으로 쓴다. 동일 물리조건의 두 seed가 있으면 그룹 join은 2쌍 대신 4행을 만든다. bank 공유용 그룹은 유지하고 `비교-family + pair_group_id + treatment/noise/실현seed/반복 식별` 또는 이에 일대일 결속한 cond_id로 **objective별 정확히 한 행**을 짝지어라. planned roster·중복/교차 seed 거부를 명시한다. 실제 ID 코드는 이번 단계 2에 추가하지 않는다.
2. **G78-N2 — 누락과 분모.** missing-as-fail은 raw-degeneracy Δ의 worst-case가 아니다. 계획40/complete38에서 D=+1, 누락2쌍이 모두 “33 누락·34 pass”면 Δ_cc=+1/38이지만 fail 대입은 −1/40이다. 전체 집합의 가능한 상한은 +1/40인데 요청 방식은 하한을 worst라 부른다. 계획 대상 N/complete n/missing m을 고정하고 Δ_cc와 `[(D+Σl_i)/N,(D+Σu_i)/N]`를 구별하라. 각 l/u는 관측된 쪽을 유지한 d=y34−y33의 최소/최대다. 양쪽 누락·N/n=0도 정의한다. primary의 geometry/recoverable inclusion mask를 먼저 고정하고 solver 누락과 구조적 제외를 섞지 않는다. 5%가 별도 reporting 정책이면 그렇게 명시하며 §6.2 실패·비유한 0건 gate의 완화로 쓰지 않는다. 조건부 complete-pair 결과를 전체 planned set의 완료로 승격하지 않는다.

§5 답: ① 예 ② 위 두 잔여 ③ 설계 제안 예 ④ **단계1+2는 수정 조건부 적합** ⑤ 실행 GO 없음/grid_fit_v5 진단 전용 유지.

사용자가 이미 승인한 단계1+2를 동일 계획으로 다시 승인받는 절차는 요구하지 않는다. 위 문서 정정을 단계1에 반영하고 로깅·parquet 오류 처리만 구현한 뒤 **기존 예정 GATE79에 함께 제출**하면 된다. 미확정 primary를 등록 완료로 쓰지 말고, missing 처리 분석기·ID/provider·adoption 구현은 이번에 하지 않는다. 기존 수치 동작 변경이 필요하면 별도로 회신한다.

구현 경계: restart별 종료 기록은 native/바깥 반복과 반환 best 결과의 의미를 구분; 옛 필드 부재를 false/0 관측으로 소급 채우지 않음. §4의 “복원 금지”는 명시 승인된 기존 leg의 receipt용 격리 복원만 예외로 정리. 최종 digest 고정 후 leg별 1회, 원문 history 보존. strict smoke 자체는 작은 계산/복원 경로이므로 “연구용 새 실행0”과 “solver 총호출0”을 혼동하지 않는다. 대상 leg·시험 범위를 고정하고 다른 운영 복원/class/투영 작업을 추가하지 않는다.

**76차 종결은 그대로다.** 본 리뷰는 미래 한정 구현의 설계 판정이며 검토자가 구현을 실행하거나 새 권한을 발급한 것이 아니다. 새 과학 계산·provider canary·floor·pilot·COMSOL/Java·class/투영 승격은 승인하지 않는다.
