# 비활성 승인 초안 — S1O-R1 검증안 정정·봉인 및 한정 검증

2026-10-08. **미승인 초안. 문서 생성·수신은 승인이 아니다.** 사용자가 아래 범위를 별도 채택할 때만 유효하다. 현재 기능 검증 승인=false, native 승인=false다.

## 채택할 문안

> S1O-R1의 생산 소스는 바꾸지 않고, 독립 검토 R1-V1–V3의 검증안 정정과 사전 봉인 명확화를 포함한 변경부 한정 검증1건을 승인합니다. 새 원점 전체1860초, Python99사례1세션/Windows PowerShell5.1 31사례1세션, 총8군130고유 입력을 상한으로 합니다. 정적 봉인 조건이 충족되지 않거나 더 많은 입력·세션·생산 코드 변경이 필요하면 기능 시험 전에 중지해 새 승인을 요청하세요. 최초 예상 밖 실패·예산 초과 후 수정·재시험·부분 probe·다른 엔진 fallback은 승인하지 않습니다. COMSOL/JVM/Java 컴파일/native/실제 콘솔·Job·정책 변경 및 실제 approval/release/runtime/token 생성은 승인하지 않습니다. 결과와 첫 실패를 보존하여 제출한 뒤 멈추세요.

## 1. 고정 출발점과 쓰기 범위

- 수용 소스: 본체 ZIP SHA `0a18cb64f8bcbcd4725b45088ee310f85e9292a1ffdced2332b5102f5fd6f9dc`, 원 CODE_MANIFEST SHA `4ce5c08dbde5153027819b5a651e3995ec82417b4429b9bb0f789082b440f5da`.
- 고정 consumer SHA `0cb1aa3cc4593dcb041115baf208c4dd09186fcc75055ddcde53c68086cc6b79`; Parent SHA `e9f8d366ca9931b84ded5753a560369b72fea8737a77075bc2b80ec771bc56ff`; control SHA `8ec75e57336c4ffa33e61d513076fb1facd1cf90430b1e1ce1c15f9bb57ac00d`. 다른 생산/계약 입력도 원 manifest로 대조한다. 버전 이름만으로 대체하지 않는다.
- 실행 기계의 제안 fixture 폴더는 `C:/Users/BML/Documents/Codex/2026-09-13/files-mentioned-by-the-user-comsol63/outputs/microshort_s1o_r1_20261008/future_validation_fixture_R1_001/` 하나다. 이미 존재하면 재사용·삭제·덮어쓰기·이름 fallback 없이 중지한다. 경로나 출발 소스가 다르면 새 선택을 받는다.
- 새 계획 정정본·정정표·하네스·fixture·원문 결과·review용 증거만 그 새 폴더에 쓴다. 원 패키지·원 CODE_MANIFEST·생산 소스·원 정적 감사·실행 상태·기존 영수증을 고치지 않는다. 계획 해시 변경은 새 validation manifest에 원 계보와 함께 결속한다. 새 해시를 미리 발명하지 않는다.
- 받은 후보 전체를 일반 실행하거나 native adapter를 채우지 않는다. 허용 추출 바이트를 봉인하고, inert 대체·origin 고정 이후에만 승인된 함수/분기를 하네스에서 호출한다.

## 2. 첫 기능 호출 전 필수 정정

1. S1Sha의 추출23–22를23–23으로 정정한다. LF 정규화·끝LF제외90B SHA `13c6456b30805e3b02063ca8cb804b201d948c5518bf01b102610297236d8eed`. 전체 추출 범위가 비어 있지 않고 함수 이름·범위·필수 집합·원문 해시와 맞는지 정적으로 대조한다.
2. PARENT12는 실제 `return_value.limited`와 final-boundary 관측을 사용한다. 생산 반환을 시험에 맞춰 바꾸지 않는다.
3. 계수 INIT07/08/10은 실제 INIT09 양성, FinalReturn 음성은 실제 PARENT12 양성에 연결한다. INIT11/12·READ·RESOURCE를 포함한 전 대조표를 실제 함수/fixture 기준으로 고정한다. PARENT14의 실제 analyze INCONCLUSIVE producer도 등록한다. 기존 ID의 도달 명확화와 이미 등록된 실제 대조 재사용만으로130입력 안에서 해결되지 않으면 **시험 전에 중지**한다. 숨은 추가 producer 실행이나 입력 증식은 없다.
4. 복수 leaf를 바꿀 사례는 정확한 변경 경로와 이유를 열거하고 나머지 byte/value 불변을 확인한다. 구조 결손으로 목표 함수 전에 거부되는 것은 해당 반례 PASS가 아니다.

생산 코드를 바꾸지 않는 위 계획/봉인 정정은 하네스720초 안에 수행한다. 원 잘못된 감사 결과와 정정 전 계획은 보존한다. 조건을 만족하면 이번 별도 승인의 범위에서 아래 시험으로 진행할 수 있으나, 조건이 충족됐다는 이유로 native_ready를 바꾸지는 않는다.

## 3. 두 단계 봉인과 횟수

첫 엔진 전: source raw SHA, 추출 bytes/SHA, 하네스·엔진 실행파일·의존 origin·정확 argv/cwd,130개 ID·입력 정의·파생 규칙·기대 첫 이유·도달함수·양성 대조표, 예산 원점을 고정한다. 이미 존재하는 원입력은 바이트로 봉인하되 Python 이후 생기는 출력 JSON은 아래 후속 봉인을 따른다. VERSION 문자열만의 결속이나 엔진을 바꿔 맞추는 fallback은 없다.

Python 세션: 실제 consumer/control 함수 경로99입력. 정상·보호·초과/경계 등 등록 producer의 JSON을 같은 실행에서 저장한다. 별도 미집계 예비 함수 호출은 없다.

Python 성공 후·PowerShell 전: 앞 세션에서 얻은 JSON 원바이트와 SHA를 고정한다. PS는 그 바이트를 실제로 읽어31개 부모 사례를 수행한다. 새로운 수제 producer 요약은 허용하지 않는다. 최초 실패면 다음 엔진을 실행하지 않는다.

기능 입력 수130, 기존98 ID+신규32의 대응을 유지한다. P0의 문구 역치환 정적 확인1은 별도다. 여러 assertion을 여러 사례로 세거나 공유 대조를 이중 집계하지 않는다. 기존389/67/그 외 과거 suite·COMSOL·Java helper를 반복하지 않는다.

## 4. 예산·중단

| 단계 | 상한 |
|---|---:|
| 계획 정정·하네스·봉인 | 720초 |
| Python1세션 | 420초 |
| Windows PowerShell5.1 1세션 | 300초 |
| 보존·전달 | 300초 |
| 미완 정리 | 120초 |
| 전체 | 1860초 |

미사용 예산 전용·자동 확대·이전2700초 원점 재사용은 없다. 시작 가용 디스크≥2GiB, fixture≤1GiB, 전달≤50MiB라는 기존 제안을 유지한다. 실제 승인 시 고정 엔진·명령/경로와 해당 관측 방법을 새 봉인에 넣고, 지원되지 않는 관측을 PASS/0으로 채우지 않는다. 원본 정책·registry·ACL·prefs는 변경하지 않는다.

실패·시간 초과·source/engine 불일치·경로 충돌·봉인 누락이면 첫/후속 오류와 raw stdout/stderr/외부rc/시간을 남기고 중지한다. 실패를 고쳐 같은 승인으로 다시 돌리지 않는다. 중지 및 기록 자체가 한도를 넘지 않도록 예약한다.

## 5. 제출·종료

정정 전후 계획·새 validation manifest·생산 원바이트 불변·130 ID별 실제 이유/도달/대조/결과·엔진별 원문rc·시간·원본 전후 식별·패키지 영수증과 실제 최종 도구 반환을 제출한다. 내부 snapshot과 반환 wall time을 합산하거나 사용자 전사를 독립 OS 로그로 부르지 않는다.

이전 R1 전달의 미수신 SUPPLEMENT_FINAL_TOOL_RETURN/SUPPLEMENT_CLOSEOUT은 기존 파일만 별도 보충할 수 있다. 이번 검증으로 과거 종결 시간을 다시 측정하지 않는다.

전부 통과해도 기능 한정 검증일 뿐이다. 설치본 일관초기화 직후t0·계수 실관측·native/raw/OS 어댑터 OPEN, native_ready=false, 전체/정상 gate INCOMPLETE를 유지하고 멈춘다. 실제 P0 또는 후속 native 승인과 무관하다.
