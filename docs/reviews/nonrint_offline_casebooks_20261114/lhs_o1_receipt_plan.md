# LHS O1 — 현재 덱 신원 수령 대조표

## 1. 기존 초안 보존

source_reference_map.json의 고정 O1 문서 §4 ASCII 블록을 원문 그대로 별도 전달 사본으로 준비했다. 원 명령·시간/크기 placeholder·기본 NO를 바꾸지 않았다. 실행0, 구문/합성 실행0. WSL 접근·현재 덱/원 로그 내용 열람0. 명령은 현재 한 파일을 두 번 해시하지만 내용을 출력/해석하지 않는다는 기존 범위다.

이 표는 새 수집기나 실행 승인 토큰이 아니다. 현재 덱 신원 O1 선택은 이미 비준됐으며 다시 묻지 않는다. 실제 대상·예산·운영 시점을 1저자가 확인한 뒤 실행한다. Q2–Q4는 이번에 묻거나 승인하지 않는다.

## 2. 완전 출력11키 + 별도 실제 rc

| 키 | 수령 조건 | 의미 |
|---|---|---|
| alias | current_deck_lhs00_100–129 중 선언 별칭 | 파일과 case 대응은 1저자 선언; 실행 입증 아님 |
| kind | deck | 역할 선언 |
| bytes | ASCII 비음수 정수, 임의 float 변환 없음 | 관측 길이; 0도 문법상 가능하나 유효 덱 인증 아님 |
| sha256 | 소문자16진64자 | 현재 바이트 지문 |
| observed_utc | 실제 달력에 맞는 YYYY-MM-DDTHH:MM:SSZ | WSL 시계 관측; 실행 시각 인증 아님 |
| record_type | CURRENT_IDENTITY_ONLY | 현재 신원 한정 |
| execution_identity_status | NOT_ESTABLISHED | 실행 당시 신원 미확정 유지 |
| origin_execution_proven | false | 과거 사용 증명 아님 |
| value_access_go | NONE | 값 열람 승인 아님 |
| whole_gate | HOLD | 전체 HOLD |
| command_rc | 0 + 전달자가 확인한 실제 프로세스 rc0 | 출력 문자열만으로 성공 인증 안 함 |

누락·중복키·추가키·잘린 출력은 완전 수령으로 세지 않는다. 원 출력은 비공개 보존하고, 추가 데이터가 실제 값/원문이면 확대 열람 없이 범위 위반으로 보류한다. 달력·hash 형식 검사는 내용/시간의 진위 인증이 아니다. 실제 parser 구현/검증은 이번 범위가 아니다.

## 3. 수령 분기와 보존

| 상황 | 대조 결과 | 다음 |
|---|---|---|
| 아직 출력 없음 | NOT_RECEIVED | 양식 null 유지 |
| 정상11키·실제rc0·별칭 선언 일치 | CURRENT_IDENTITY_RECEIVED_ONLY | 실행 신원 NOT_ESTABLISHED·동결 미승인·값GO NONE 유지 |
| command_rc=0이나 실제rc 비0/미수령 | INCOMPLETE | rc를 추정하거나 자동 재시도하지 않음 |
| 동일 별칭·다른SHA/길이/시각 | MULTIPLE_OBSERVATIONS | 새 관측을 추가, 이전 것 보존; 실행 당시 것 선택 안 함 |
| 다른 별칭·같은SHA | DISTINCT_DECLARED_ALIASES | 같은 run/계보/입력 사용으로 합치지 않음 |
| 실행 신원 ESTABLISHED·값 GO true로 바뀜 | SCOPE_CONTRADICTION | 현재 hash로 과거 실행/값 승인 대체 불가 |
| 빈 파일 bytes0 | CURRENT_BYTES_ONLY_IF_OTHER_FIELDS_COMPLETE | 적격 덱/정본/실행 성공으로 승격 안 함 |
| 크기/시각은 같지만SHA 다름 | CHANGED_CURRENT_BYTES | 변경 사실만 기록; 원인 추정 안 함 |

같은 SHA라도 과거 실행 당시 사용·include 폐쇄·재개 사슬은 증명되지 않는다. 실제 정본/구간·A/C·명부/쌍·종점/필드·담당/범위·노출·동결 승인·값 GO는 별도 칸으로 계속 남긴다. 초안의 stat·두 번 hash는 원자 snapshot/적대적 경합 방어가 아니라는 한정도 유지한다.
