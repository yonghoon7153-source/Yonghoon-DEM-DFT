# Q12 수집 중 객체 소유권 — 선택표 초안

바탕97fee6ebbcece686285c869316d22a918408accd, codex/rint-capture-ownership-1114. docs/reviews/rint2_q12_capture_preparation_20261114/capture_contract.md §2–4의 다음 연결. source64e4d213e8267bafaf3ae5af00a42996cefd3f33·기존블록 불변, 새구현/조립/기존시험 재실행0·전체 HOLD.

## 1. 권고안 전제 OWN-Q1

조립 완료 객체가 기록 구간 동안 바뀌지 않을 소유권을 먼저 선택한다. 실제 불변 객체 근거가 있으면 그 구간을 유지하고, 없으면 같은 일관 시점의 독립 사본 비용을 검토한다. 실제 방식 비준·thread/lock/copy 구현은 아직 없다.

| 선택 | 필요한 증거 | 비용/한계 |
|---|---|---|
| O1 원객체 단일소유 구간 | graph/CSR/RHS/DOF의 모든 writer를 막는 구간·예외 경로 | 원객체+hash/직렬화 임시·writer 대기; 일부 배열만 잠그면 불충분 |
| O2 일관 사본 | 전 배열이 같은 논리 시점인 사본·원본참조 | 원객체+사본+직렬화의 동시 peak·복사시간; 배열별 복사 중 변경되면 시점 혼합 |
| O3 입증된 불변 구조 | 생산자 불변 소유권/수명의 고정 코드 | 공유payload+descriptor/alias metadata; 새 구조면 sourcepin/재확인 범위 변경 |

원객체를 먼저 지워 peak를 줄인다고 가정하지 않는다. record 완결/출처 결속 전에 필요한 데이터·실패 원인을 잃지 않아야 한다. view 중복을 빼더라도 실제 별도복사이면 별도 할당이다. host/device/unified memory를 같은 pool로 임의 합치지 않는다.

## 2. 사본이 보존할 것

입력/source/환경/attempt/모드·원DOF 순서·CSR/RHS/판 결합 dtype/shape/내용은 기존 assembly_record 규약대로 남긴다. 수치 정규화·정렬·재합산으로 환경 간 차이를 없애는 것은 수집 방법이 아니다. ID의 int64 표현과 원 ID배열dtype 구분, Q-A 독립 건설과 저장본 재읽기 구분도 유지한다.

## 3. 다음 확인

CAP03 수집 중 RHS 변경은 O1=변경 시도 거부/수집 보류, O2=일관 사본 실패/전체 보류, O3=불변 소유권 위반 거부로 구현해야 한다. 부분descriptor COMPLETE 금지. CAP01/02/04/10의 시도/출처/완료/옛기록 분리도 필요하다. 실제10사례 시험은 미실행.

콜사이트·수명·환경·필드별byte/비용·예외 원본보존 규칙은 미정. 다음 고정 연결 후보에서 비용표를 채워 1저자에게 올린다. 지금 선택 승인·새질문·실행GO 없음.
