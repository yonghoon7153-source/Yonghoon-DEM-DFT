# D-3/P2 native 선언·판 분리 진단 — 한정 독립 검토 요청

바탕은 S0 `f4647f2b7c218a6df7def3292c092273f9d4e35f`. 고정 후보는 하루 묶음 PIN_MANIFEST에 결속한다. 발송은 1저자, 반입·원장 처분은 Claude다. 본 문서는 작성측 요청이며 반박 판정이 아니다.

## 1. 이번에 닫으려는 범위

**권고안 전제(Q-P2-1/2)** 아래 pure-data native P2 header/params, 원 S0/LIVE 입력 재검증, h0·물리시간·명시 중력 사상, 두 유효 무접촉 창 → MOVE_CLEAR 진단 사건 → 분리 뒤 네 창의 결속만 검토한다. 일반 P1/r8 이름 교체는 지원하지 않는다. 실제 소비자나 판 이동 기능을 추가한 것이 아니다.

| 질문 | 고정 검토 대상 | 필요한 구분 |
|---|---|---|
| Q1 native 신원 | `validate_p2_contract`와 원 S0 decoder 입력, plan/S0 digest·active definitions | caller가 계획·자료를 함께 바꾸는 것을 실제 생성 출처 인증으로 세지 않는다 |
| Q2 시간·h0 | dt/2와 같은 물리 창, S0 판 위치에서 선언 bottom을 뺀 h0·A/B 비례/상한, 명시 중력 | TOY 단위·등록 미정값과 실제 규약/자격은 별도 |
| Q3 분리 순서 | 모든 step의 접촉/재고·같은 attempt/history, 두 연속 유효0창 뒤 MOVE_CLEAR, 네 post 창 | None/누락/부분을0·완료로 승격하지 않는가 |
| Q4 사건 | 언로딩 구간 첫 유효 압력 교차, 둘째0창 끝, clear, post 끝을 별도 기록 | post 압력 교차가 언로딩 사건으로 채택되지 않는가; primary는 항상 SELECTION_UNRESOLVED인가 |
| Q5 보존·권한 | 기존 q/T0/T11/LIVE/S0 불변, source/test hashes, red→green 원기록 | 구조 통과가 실제 T12·숨은 이력·PBC·source 인증·운영 봉인/GO를 만들지 않는가 |

## 2. 작성 순서와 증거

이번 신규 구현은 시험·fail-closed 스텁 red를 먼저 실행한 뒤 작성했다. 첫 준비 시험에는 tuple fixture 수정 오류1이 있어 원기록을 보존했다. 한 줄 수정 후 고정28메서드 red2는 실패16·오류0, 구현 첫 green은28/28이다. 이후 post-only crossing 반례를 추가한29메서드는 기존 후보에서 실패1·오류0, phase 제한 뒤29/29이다. 최종 고정시험으로 가드 약화7/7을 검출했다. 서로 다른 suite·반복·내부 관측을 합산하지 않는다.

source SHA256=`cb5b3b66bbb89c39d2faf843c68f1b04853e28d9bcddc69de458f4aa2c194899`; test SHA256=`0aa20e8128a1e1d9ed0b03e0c61e93c200466562d797df6d5371f0a4a21babe3`. 세부 수·버전·원시 manifest는 `verification_summary.json`과 하루 ZIP에 둔다. 이전 T11/LIVE/S0의 선작성 순서 예외가 이번 P2의 순서로 소급 해소되지는 않는다.

## 3. 닫지 않는 것

실제 ULPR/P1 소비자 연결, primary 선택, 원자·접촉에서 힘/압력/운동 재계산, 실제 gravity/PBC/재개·숨은 이력·binary 자격, 정량값 등록, source 인증, 운영 source seal, gate/CI 및 실행 GO는 포함하지 않는다. S0의 pair/wall·atom 의미/동시성 한계도 그대로다. 실제 엔진·호스트·자료 접근과 연구 결과는0이며 전체 HOLD다. 반례가 있으면 이 범위의 판정을 먼저 받고 다음 연결의 근거도 함께 수정한다.
