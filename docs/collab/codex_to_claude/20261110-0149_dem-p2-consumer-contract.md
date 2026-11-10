# D-3/P2 — native 소비 선언과 판 분리 진단

| 1저자 결정 칸 | 권고 한 줄 | 준비 중 적용 |
|---|---|---|
| Q-P2-1: 소비 사상 | 원 S0 입력을 재검증한 native P2 header·params, h0 비례·명시 중력·같은 물리시간을 결속 | **권고안 전제(Q-P2-1)**; 실제 규약/정량값/출처 인증 아님 |
| Q-P2-2: 분리 관측 | 두 연속 유효 무접촉 창 뒤 MOVE_CLEAR 진단 사건, 그 뒤 네 완전한 창; primary는 미선정 | **권고안 전제(Q-P2-2)**; 실제 판 이동·실행 권한0 |

## 1. 바탕·변경

| 항목 | 상태 | 근거 | 다음 |
|---|---|---|---|
| 새 가지 | `codex/dem-p2-consumer-1110`, 바탕 S0 `f4647f2b7c218a6df7def3292c092273f9d4e35f` | 상시 요청 D-3 | 앞 판정 대기 중 후속 준비 |
| API | native 검증·분리 진단2개 | `scripts/dem_gen2_p2_contract.py`; `docs/reviews/dem_p2_consumer_contract_20261110/README.md` | 독립 검토 PENDING |
| 사건 | 언로딩 첫 유효 교차·둘째0창끝·clear·post끝4개 분리 | 같은 폴더 `contract_draft.json`·`review_request.md` | primary SELECTION_UNRESOLVED |
| 실제 자격·권한 | actual T0/T11/T12 NOT_RUN, actual S0/언로딩 선택 null, 운영 권한 false | 순수 합성 선언과 step 창만 처리 | 전체 HOLD |

## 2. 시험·작성 순서

| 관측 | 수 | 한계 |
|---|---|---|
| 시험 준비 첫 red | 28메서드·실패15·오류1 | tuple fixture 수정 오류, 원본 보존; 구현은 아직 없었음 |
| fixture 한 줄 정정 후 red2 | 28메서드·실패16·오류0 | 이 관측 뒤 구현 시작 |
| 첫 구현 green | 28/28·오류0 | red2와 동일 시험 |
| post 교차 추가 반례 | 29메서드·실패1·오류0 → 29/29·오류0 | 같은29메서드, 언로딩 phase 조건 한 줄 추가 |
| 보호 조건 약화 | 7/7 검출·각 오류0 | S0 원입력/plan digest/시간/매 step 접촉/재고/post예산/native profile, suite 반복을 새 시험수로 더하지 않음 |

최종 source SHA256=`cb5b3b66bbb89c39d2faf843c68f1b04853e28d9bcddc69de458f4aa2c194899`, test SHA256=`0aa20e8128a1e1d9ed0b03e0c61e93c200466562d797df6d5371f0a4a21babe3`. 원 영수증은 `verification_summary.json`과 하루 묶음에 결속한다. 기존 q/T0/T11/LIVE/S0·봉인32·Rint·원장·공용 gate 수정0. 전체 gate/CI NOT_RUN. 이번 합성 호출의 실제 연구 결과·엔진·현장 접근0. 전체 턴 문서 노출 예외는 `20261110-0121_dem-t5-contract.md` §3 그대로다.

P2는 입력 선언/바이트/step 순서를 대조한다. 물리 압력·접촉을 원자로부터 다시 산출하거나 source/hidden history를 인증하지 않는다. 실제 P1 소비자 연결·운영 재봉인·실행 GO는 별도다.

## 3. 반입·다음

반입 커밋=`<<sha:Prepare synthetic P2 consumer and separation contract>>`. 고정 핀·원시 증거는11-10 하루 반박 묶음 ZIP에 포함하며 발송=1저자, cherry-pick -x·원장 처분=Claude다.

다음은 D-3 T12·binary/history/resume/dt/2·등록/통합의 필수 사례와 영수증 상태 계약이다. 실제 자격의 빈칸을 합성 통과로 채우지 않고 누락·실패·부분·다른 attempt/원천의 혼입부터 시험한다. 이어 DEMP-01/02와 두 입경의 같은 정적 상태 비교 요구 계약을 준비한다.
