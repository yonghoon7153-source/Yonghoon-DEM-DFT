# NSB 기존 독립 판정 수령 + DEM·믹서·LHS 오프라인 준비

## 1. 반입 순서

가지 codex/nonrint-casebooks-1114, 바탕2a19696767c08c83a57814252151c3b004c93f4e. 반입 대상은 <<sha:Receive recovered NSB verdict and prepare offline casebooks>> 한 커밋. 기존 대기열 뒤 cherry-pick -x, Claude 복귀·1저자 반입 지시 뒤. 기존 가지 재작성0.

## 2. 내용·검증

| 항목 | 상태 | 근거 |
|---|---|---|
| NSB-F01/C01/C02 | 11-10 독립 판정 한정 종결 가능 수령; 새 시험0 | docs/reviews/nsb_recovered_verdict_receipt_20261114/README.md §1–4 |
| NSB 무결성 | 528파일/527외부·254독립·268후보 해시, 원269바이트·snapshot24 Git blob 일치 | 같은 폴더 intake_verification.json |
| DEM 수영 | 손 계산12관측 일치; 생산 red/green 아님 | docs/reviews/nonrint_offline_casebooks_20261114/dem_worked_examples.md §2–3 |
| 믹서 | 전체 소스 고정시계 사본2개, 원바이트/AST 복원2/2·clock3관측; Linux 전체0 | 같은 폴더 mixer_fixed_clock_copies.md §1–3 |
| LHS | O1 명령 원문 사본·11키 수령 대조표/빈 양식; 실행0 | 같은 폴더 lhs_o1_receipt_plan.md §1–3 |

NSB 원문은 역사 수령 사본 .md.txt로 원바이트 보존. 과거 NOT_RECEIVED를 덮지 않고 후속 수령을 붙였다. 원 ZIP/원로그 통째는 반입하지 않는다. 새 실제 값·연구·현장·봉인·공유 원장 변경0, 전체 HOLD. 공유 점검은 check_results.json과 scope_check.json 그대로이며 Windows native rc1을 PASS로 쓰지 않는다.

## 3. 공유 기록 제안

NSB 원장: 별도 ledger_proposal.json의 수령 메모만 현행 상태와 규약에 맞춰 적용. verified/closed 자동 승격을 제안하지 않는다.
진행 기록 제안 문장: ‘11-14 NSB 고정 후보의 11-10 독립 한정 수용 판정 회수·동일성 확인. DEM 설계 산술12, 믹서 고정 시각 전체 사본 준비, LHS O1 수령 양식 추가. 실제 자격/현장/값열람/운영 봉인0, 전체 HOLD.’
게이트 추가 제안0. 지금 새 1저자 질문0; 미정 수치·현장 GO를 대신 결정하지 않았다. 실제 반박이 필요한 solver/운영 묶음 검토는 해당 구현/고정 핀 뒤 별도로 낸다.
