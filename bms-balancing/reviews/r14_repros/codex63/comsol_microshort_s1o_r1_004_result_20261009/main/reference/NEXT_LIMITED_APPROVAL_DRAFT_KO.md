# 비활성 승인 초안 S1O R1 검증 잔여 보완

2026-10-08. **미승인 초안. 사용자 명시 채택 전 수정·시험을 시작하지 않는다.** native 승인은 포함하지 않는다.

## 사용자 채택 문안

> R1_003 원본·실패·127개 PASS와 생산 코드를 그대로 보존하고, 검토 회신 S1O003-N1/N2의 하네스 및 동일 기본 입력 양성 보완을 승인합니다. 새 원점1200초 안에서 Python 양성4개1세션, Windows PowerShell5.1 미완3개1세션만 수행하세요. 기존99개/28개와 실패한 세션을 통째로 다시 돌리지 마세요. 사전 봉인 또는 기존 결과 재사용 조건을 충족하지 못하면 시험 전에 중지하고, 최초 예상 밖 실패 뒤 수정·재시도·부분probe는 하지 마세요. COMSOL/JVM/Java컴파일/native/실제입력·Job·정책 변경 및 실제 approval/release/runtime/token 생성은 승인하지 않습니다. 결과와 원문을 제출한 뒤 멈추세요.

## 경로와 불변

새 위치 제안: `C:/Users/BML/Documents/Codex/2026-09-13/files-mentioned-by-the-user-comsol63/outputs/microshort_s1o_r1_20261008/future_validation_fixture_R1_004/`. 이 이름도 사용자 채택에 포함된다. 이미 있으면 생성/덮어쓰기/삭제/재사용/다른 이름fallback 없이 중지한다. 이전001/002/003은 변경하지 않는다.

수용 source CODE_MANIFEST SHA `4ce5c08dbde5153027819b5a651e3995ec82417b4429b9bb0f789082b440f5da`; Parent SHA `e9f8d366ca9931b84ded5753a560369b72fea8737a77075bc2b80ec771bc56ff`. 나머지 생산파일도 원manifest21개로 대조한다. 원R1_003 ZIP SHA `11a27f3034fed763442ccce9730f7e008058b819bfbffd9d58a5d2994b875d4b`와 원 FIRST_SEAL·하네스·results·producer seal을 새 증거의 재사용 출처로 연결한다. 원 승인/원패키지/원상태를 수정하지 않는다.

새 쓰기는 이 폴더의 좁은 subset하네스·정정계획·fixture·reuse map·봉인·기록·전달 자료뿐이다. 일반 파서나 생산 방어를 변경하지 않는다. 엔진과 의존origin은 이전 고정값과 읽기전용 대조하며 설치·환경 재구축·엔진 fallback은 없다.

## 사전 고정할 새 입력7개

| 엔진 | ID와 목표 | 기대 |
|---|---|---|
| Python | READ_CTRL_CSV, read_csv_bytes | 같은 정상2열 CSV의 정확2행/값 반환 |
| Python | READ_CTRL_TIME, timed_rows | time_s만 가진Decimal0/1행·end문자열1의 정확 시간집합 |
| Python | READ_CTRL_COVERAGE, coverage | 양쪽Decimal[0,1], 세 요청문자열[0,1], safe문자열1 → 비교[0,1]·누락0 |
| Python | READ_CTRL_PROFILE, profile_rows | 원규칙 t0 N241점/원좌표/domain1 →1시각241점 |
| PS5.1 | PARENT_R115, 동일POLICY02 문자열값 | 실제정상분기·WITHIN_LIMITS_THIS_WINDOW |
| PS5.1 | 개정PARENT_R113, 동일leaf 명시Double | DECIMAL_TRANSPORT_PRECISION·stage=comparison_numerics |
| PS5.1 | PARENT_R114, POLICY03 summary2leaf만위조 | COMPARISON_SUMMARY_CONTRADICTION·stage=fields |

원래 130 ID를 재번호 매기지 않는다. Python 4개는 새 보조 양성이며 원래 130개 외에 따로 집계한다. PS 3개는 원 미완 ID다. Python 4개가 모두 기대대로 끝난 뒤 PS를 한 번 수행한다. 함수 내부 호출은 봉인한 경로로만 허용하며 숨은 추가 입력/대조 호출은 없다.

Python fixture 상세:

- CSV 원바이트는 `time_s,value\n0,1\n1,2\n`; expected_header는time_s/value, 두 단위사전은s/1. expected_identity는 이전 generator가 사용한 **정확 path·크기·SHA**로 만든다. 경로도 임의로 바꾸지 않는다.
- timed_rows는 `[{time_s:Decimal(0)},{time_s:Decimal(1)}]`, end=`"1"`; value필드를 새로 더하지 않는다.
- coverage의 양쪽시간은Decimal 목록, 세요청은문자열목록이며 다른 컨테이너로 대체하지 않는다.
- profile은 봉인된 원 `shared_fixture.data([Decimal(0)])` 생성규칙과50자리Decimal 조건·원241좌표·domain1의 실제 데이터를 준비한다. 입력 준비에 production 함수를 호출하지 않는다.
- 각 새 양성의 canonical bytes/해시와 기존 READ02–12 recipe를 대조해, 선언된 변이만으로 기존 실패 입력이 유도되는지 **데이터로** 확인한다. READ05–07의 raw변경/identity재계산, READ10의다섯벡터1제거를 복수변이로 명시한다. 기존 음성함수를 다시 부르지 않는다.

## R113 하네스 정정과 결과 재사용

원 POLICY02 producer/context를 바이트 그대로 읽고, 지정 문자열0.001 token의 따옴표 두 개만 제거한 JSON 숫자 변이를 기록한다. **타입 assertion 전에** raw 변이 bytes/SHA·token offset·parse 직후 실제 CLR 타입/값을 남긴다. 유한한 해당 숫자인지 확인한 뒤 승인된 fixture 단계에서 단일 leaf만 명시적으로 Double로 변환한다. 전후 type/value·Double 64비트·나머지 leaf 불변을 기록한다. null/string/비숫자/값 불일치는 cast로 숨기지 않는다. JSON parser 자체가 Double을 만든 것으로 쓰지 않는다.

입력 준비 전에 ID·빈 reach·target_entered=false를 설정한다. 준비 실패에도 현재 진단을 보존한다. R113은 실제 S1Decision→S1Fields→S1ComparisonNumerics 도달과 정확 이유/단계를, R114는 실제 S1Decision→S1Fields 도달과 정확 이유/단계를 확인한다. 다른 조기 오류는 PASS가 아니다.

기존 PARENT02 양성은 동일 Parent/함수·PS 엔진·POLICY03 JSON/context·원 raw 반환/도달을 연결한 재사용 표로 결속한다. 새 공통 loading/producer parsing/판정 의미가 달라지면 이번 3개 범위에서 그 결과를 재사용하지 말고 시험 전에 중지한다. PARENT02를 네 번째로 몰래 호출하지 않는다. 기존 PARENT01 등 참조도 동일 원칙을 따른다.

새 하네스 SHA를 새 봉인에 담는다. 원 PS_PRODUCER_SEAL의 옛 하네스 SHA를 새 하네스 검증에 재사용하지 않는다. 원 Python producer는 재생성하지 않으며 모든 결과/context의 원 SHA를 다시 대조한다. 이전 127개 중 READ 11개는 새 양성/변이 결속이 성공한 뒤 종결 근거로 함께 사용한다.

## 예산과 중단 및 제출

| 단계 | 새 제안 상한 |
|---|---:|
| 계획·하네스정정·입력/재사용봉인 |600초|
| Python 양성4개1세션 |120초|
| PS5.1 미완3개1세션 |180초|
| 보존·포장·전달 |240초|
| 미완정리 |60초|
| 전체 |1200초|

이는 새 제안이지 기존 남은 예산의 전용이나 완료 보장이 아니다. 시작 디스크≥2GiB, 새 fixture≤1GiB, 전달≤50MiB의 기존 자원 조건을 유지한다. 새 원점·단계 시각·엔진 외부 rc·원문·시작/종료 식별·원본 전후 SHA를 기록한다. 포장 내부 snapshot과 도구 wall time을 합산하지 않는다.

사전 조건/봉인 불일치, 기존 대조 재사용 불가, 예상 밖 실패, 예산 초과, 추가 입력·세션·생산 수정이 필요하면 중지한다. 실패를 고쳐 같은 승인으로 다시 돌리지 않는다. 권한/정책/다른 shell로 우회하지 않는다.

최종 제출은 최소 diff, 7개 입력 정의·양성 연결표, 소스/엔진/하네스 봉인, raw stdout/stderr/rc/첫 실패, 원 봉인123개 보존 및 재사용 범위, 새 포장 manifest/receipt/최종 반환이다. 원003의 INCOMPLETE·하네스 실패는 그대로 두고 새 결과를 별도 기록한다. 성공 시 집계는 **원127 재사용+원 미완3 신규 충족, 보조 양성4 별도**다. 전체130을 한 번에 통과했다고 쓰지 않는다.

native_ready=false, 설치본 t0/계수/native/raw/OS 어댑터 OPEN, 전체/정상 gate INCOMPLETE를 유지하고 멈춘다. 실제 S1-P·COMSOL·microshort 계산은 여전히 별도 승인 대상이다.
