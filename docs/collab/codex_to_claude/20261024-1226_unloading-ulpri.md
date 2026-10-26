# ULPRI-01·02 외부 반박 재현과 후속 수정 인계

사용자가 외부 판정문과 ZIP을 전달했다. [수령 판정](../../reviews/codex_review_unloading_ulpr_integer_20261024/codex_review_unloading_ulpr_integer_20261024.md)은 **정수 반올림 교정 수용 / Q2·Q3 무결성 종결 HOLD / 새 P2 두 건**이다. 새 P1이나 정상 물리량 오류를 발견했다는 판정이 아니다. 보고서 내용은 바꾸지 않았고, 저장소의 LF 사본과 CRLF 원문·원 ZIP의 관계를 같은 디렉터리 PROVENANCE에 남겼다.

## 가지와 수정 범위

- 원 검토 핀 `01c1aaf5be8acdf7d1716f34cc86fc77d8e27362`와 제출 ZIP은 그대로다. 새 가지 `codex/unloading-ulpri`를 그 핀에서 만들었다. 중심 `claude/stoic-knuth-NObVQ` 반입은 사용자가 나중으로 미뤘으며 여기서 수행하지 않는다.
- 후보 자리: `<<sha:Reject ambiguous unloading resume markers and separators>>`. 실제 최종 리뷰 핀은 외부 PIN.txt와 원격 가지로 전달한다.
- ULPRI-01은 RESUME와 앞뒤 공백만 다른 원문 표지를 거부한다. 공용 CSV의 줄 분리 전에 원 event 셀을 검사하여 선행 줄 구분자가 사라지는 같은 경계도 막는다. 변형된 표지를 정상 RESUME로 바꾸어 수용하지 않는다.
- ULPRI-02는 manifest 키를 선별하기 전에 LF/CRLF/CR 밖의 명시된 줄 구분자를 거부한다. 다른 글 뒤에 숨은 잘못된 resume_from과 정상 기록이 공존해도 정상 기록만 골라 인증하지 않는다.
- 공용 숫자/CSV 파서와 정수 파서, 물리 문턱·params·생산 덱·history·공유 코드·봉인 32파일은 변경 대상이 아니다. 사전등록 보충은 기존 승인 무결성의 좁은 경계를 명시하며 새 실행 승인이 아니다.

[후속 요청서](../../reviews/codex_dem_unloading_ulpri_recheck_request_20261024.md)에 수정 전후 반례, 정상 대조, 독립 검토와 정확한 실행 범위를 기록한다. root는 고정 01c1 체크아웃에서 외부 집중 반례 6개를 먼저 실행해 외부의 인증·행 제외·주 값·순위·CSV 불변 관측과 모두 일치함을 확인했다.

## 판정과 검사 해석

내부 수정·검사 통과는 **claimed_fixed와 외부 재확인 대기**를 뜻한다. 외부 HOLD를 내부 결과만으로 닫거나 실제 언로딩 발사 GO로 쓰지 않는다. 공유 원장의 ULPRI 두 항목 반영·종결 상태는 받는 쪽이 실제 판정과 SHA 대응을 확인하여 처리한다. 이번 가지는 공유 원장·CLAUDE를 직접 고치지 않는다.

키트 13개 직접 명령과 그 안의 reader/R40 시험은 공유 155개 검사·CI에 자동 포함되지 않는다. 각각의 실제 실행 로그와 사례 수를 구분한다. 전체 저장소 게이트는 별도 코드 후보에서 실행하고 후속 증거 쪽지로 기록한다. 합친 트리는 Claude 반입 때 다시 검사해야 한다.

## T12 연결

기존 T12 로컬 후보 `<<sha:Add pinned T12 consumer contract and synthetic boundary probes>>`의 41개 직접 시험은 당시 고정 01c1 소비자의 한정된 경계를 검사했다. 외부 반례가 도착한 뒤 그 후보의 전체 게이트는 의도적으로 중단했고, 부분 로그와 종료 코드를 보존했다. 이를 최종 전체 통과나 코드 결함에 의한 실패로 기록하지 않는다.

후속 T12는 실제 게시된 새 ULPRI 핀으로 소스 manifest와 계약을 갱신하고, 새 표지·줄 구분자 반례가 포함된 직접 시험과 전체 게이트를 다시 수행한다. 그 결과가 새 P2 생산기·등록·실제 R-a 끝 S0·외부 GO를 만들지는 않는다. `physical_ready=false`, 실물 T12 `NOT_RUN`을 유지한다. 실제 WSL·연구 런·스케줄러·Claude 중심 가지 반입은 이번 수정 범위 밖이다.
