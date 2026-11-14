# DEM — 메모리 수명 산술 준비

## 1. 범위와 근거

바탕3456af3e00b4836eda561c40ee6941233de49c27, codex/dem-memory-prep-1114. 단계1 설계 db5abe6b359abdc44b3c17bb91d984a5fee3a567의 docs/reviews/dem_suyoung_stage01_20261113/stage1_census_design.md §3–4와 docs/reviews/nonrint_contract_preparation_20261114/dem_p2g_transaction_contract.md §2–3의 old/new 동시 생존을 합성 정수 산술로 구체화했다.

새 도구는 선언한 예약/수명 명부의 pool별 peak만 계산한다. 실제 배열/좌표/원로그·시스템 메모리 조회·solver·GPU·MPI·네트워크 기능이 없다. 운영 실행기/게이트/봉인에 연결하지 않았다. 실제 구현/자원/연구 GO가 아닌 준비용 산술이다. 전체 HOLD.

## 2. 계약

| 항목 | 계산 규칙 | 실제 적용 전 남는 것 |
|---|---|---|
| 단위/숫자 | B 단위 정확한 내장 정수, float/bool/문자열 변환 전 거부 | 항목 크기 출처·allocator 비용 |
| 수명 | 정수 사건 번호의 반열린 [start,end), end에는 해제된 것으로 계산 | 실제 해제 완료와 순서/소유권 근거 |
| 예약 | used보다 reserved 계상, 사용량≤예약량 | 예약 성장·arena 캐시·파편화·runtime 여분 |
| view | 알려진 owner의 연속 바이트 범위·수명 안, payload 중복 가산 없음 | view 객체 metadata는 별도 할당, strided/distributed view 범위 밖 |
| 자원군 | host/device 같은 pool을 각각 계산 | 실제 용량·통합메모리 의미, pool끼리 합쳐 한 한도로 비교 금지 |
| 결과 | peak/budget/headroom/over_budget/timeline | 산술상 한도 안이어도 명부 완전성·현장 자격·실행 GO 없음 |

같은 사건 번호의 해제/새 할당은 먼저 해제됐다는 선언의 결과다. 실제 새 할당 뒤 해제라면 다른 사건 번호로 겹침을 명시한다. 선언되지 않은 동시 생존을 자동 추론하지 않는다. 실제 물리 상태/통신/정렬/검증/입출력/runtime 전체 명부는 아직 없다. 큰 정수 정확성이 입력 진위를 보증하지 않는다.

## 3. 시험

시험 파일부터 작성하고 새 모듈을 작성했다. 역사 생산 소스 수정/구본 red→green 주장은 없다. Python3.12.14, 고정20메서드 실패0/오류0.

| 검사 | 직접 결과 | 의미 |
|---|---|---|
| 정상/음성20메서드 | 20/20 | old3+new4+rollback2 peak9, 반열린 경계 peak5, alias·예약·pool·형식·수명·owner·범위 |
| float 누적 변이 | 같은20 중1실패/0오류 | 2**53+1을2**53으로 줄이면 한도1 B 초과 누락 |
| 최대 단일 할당만 peak | 2실패/0오류 | 동시 합 누락 |
| used로 reserved 대체 | 7실패/0오류 | 예약량 누락 |
| view 중복 가산 | 1실패/0오류 | alias payload 중복 |

4변이는 새 모듈의 임시 사본을 의도적으로 약화한 음성 대조이며 과거 결함4건/독립 반박4건이 아니다. 반복20과 subtest를 더해100고유 시험으로 세지 않는다. 원 모듈/시험 바이트 보존, test_results.json에 소스/시험/원출력SHA와 반환값을 보존했다.

## 4. 다음

권고안 전제 MEM-Q1: 실제 적용 전 예약항목/수명/별칭 근거를 완결한다. 실제 budget/사건/사용가능 자원·구현 핀은 null. runtime guard로 연결하려면 고정핀·완전성/수명 검증·독립 반박 별도. P1 A/B 판정 대기·NSB 앞 한정 수용·T0/T5/T11/T12·DEMP·U자격은 그대로다.

재현: python -I -X utf8 -B test_memory_liveness.py. 표준 라이브러리와 같은 폴더 모듈만 쓰며 실제 설정 실행 CLI는 없다. 현장·연구·값열람·운영재봉인0.
