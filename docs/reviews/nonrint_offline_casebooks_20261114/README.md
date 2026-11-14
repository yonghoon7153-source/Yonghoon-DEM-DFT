# 비 Rint — 현장 없이 이어간 준비

전체 HOLD. 바탕2a19696767c08c83a57814252151c3b004c93f4e, 새 가지 codex/nonrint-casebooks-1114. 실제 연구/현장/값열람/운영 재봉인/원장 변경0. 새 solver/수집기/소비자 구현0.

## 1. 이번 산출물

| 트랙 | 상태 | 근거 | 다음 |
|---|---|---|---|
| DEM 원 트랙 NSB | 3건 한정 수용 수령, 중복 시험0 | 별도 nsb_recovered_verdict_receipt_20261114 §1–4, 후보c5aa7bb527c5 | Claude 원장 규약에 따른 수령 반영 |
| DEM 수영 | 손 계산12관측 일치, 생산 회귀0 | dem_worked_examples.md §2; dem_example_results.json | ID/P2G rollback/메모리 계약에 연결; 실제 solver·수치 동결 별도 |
| 믹서 | 원본2/고정사본2, AST/바이트 보존2/2; clock-only3관측 | self170_copy_manifest.json; mixer_fixed_clock_copies.md §1–3 | Linux 의존/권한 확인·전체 합성0회 미수행 |
| LHS | 기존 O1 블록 원문 사본1, 완전11키·실제rc 수령 양식1 | lhs_o1_receipt_plan.md §2–3; source_reference_map.json | 1저자의 범위/예산 확인 후 실행; 현재 미수령 |

12와3은 설계/시계의 작은 관측이며 생산 시험 통과 수가 아니다. Linux 전체 selftest와 WSL 명령은 실행하지 않았다. 새 독립 판정 요청을 자동 발송하지 않는다. NSB는 기존 독립 판정 수령으로 중복 검토를 끝냈다.

## 2. 반입과 보존

새 파일만 추가. 정본 메모·DOCX·Rint source·공유 원장·게이트·봉인32·litdb·운영 seal 무변경. 타 가지의 근거는 pin/path/blob을 source_reference_map.json으로 고정했으며 소스 파일을 현재 가지에 병합하지 않았다. private 사본·원 증거 ZIP·검사 로그는 공개 반입에서 제외한다.

P1 A/B 독립 판정은 이 창에 아직 미수령이다. 들어오면 내부5회차와 합쳐 한 개정으로 처리한다. 이번 12관측을 P1 A/B·NSB의 추가 판정으로 사용하지 않는다. 숫자/환경/원자료 허용이 필요한 칸은 비워 둔다.

## 3. 확인

check_results.json은 참조/원장 점검의 실제 결과다. 기존 Windows 참조 문제는 원형대로 보고하며 검사기를 바꾸지 않는다. 전체 Linux gate는 Claude 반입 때 수행한다. 별도 scope_check.json에 새 파일 범위·금지 파일 무변경·기존 전달물 보존을 기록한다.
