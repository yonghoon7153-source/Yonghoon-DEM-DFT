# S1 OPEN 연결부 준비 검토

2026-10-10. 판정: **오프라인 준비 성과는 확인하되, 추가부 한정 검증은 아래 세 항목 정정 후 별도 승인 대상으로 둔다.** 현재 8군 50사례안을 그대로 실행하도록 권하지 않는다. `native_ready=false / approved=false / usable=false`, 네 OPEN 및 전체/정상 gate `INCOMPLETE`를 유지한다.

이번 회신은 정적 검토다. 후보·동봉 도구·기존 시험을 import·컴파일·실행하지 않았고 COMSOL/JVM/입력/Job 시험도 하지 않았다. 아래 반례는 제출 소스의 제어 흐름을 읽어 도출한 것으로, 새 동적 시험 결과가 아니다.

## 1. 확인된 준비 성과

- 수신 ZIP **1,929,576 bytes**, SHA256 `32cbb6ee5b8885a645da762154dab38d8f67ef4c7f97b5b4bc9c2ecd5fdd6f5c`. 79 payload + manifest = 80개 엔트리의 정확 집합·크기·SHA·CRC, 대소문자 중복·경로·symlink 검사를 통과했다.
- 새 CODE_MANIFEST SHA `be19764204a4695c9058f565a69c5e09ea528124d4659e9d8f9d1c11fd6f749f`의 11개 구성원과 원 R1 manifest SHA `4ce5c08dbde5153027819b5a651e3995ec82417b4429b9bb0f789082b440f5da`의 21개 구성원이 실제 동봉 바이트와 일치한다. 기존 consumer/control/Parent 수용은 유지한다.
- P0의 추가 블록 2,553 bytes를 제거하면 원 P0 **전체 바이트**와 같다. 블록은 LF fragment를 CRLF로 표현하고 구분용 빈 줄 하나를 더한 것이다. 새 호출 지점/runAll 추가 없이 `denyS0Execution()`을 유지했다. 설정/물리 본문을 바꿨다는 증거는 없다.
- 새 Python 두 파일의 소스 구문·전체 추가 diff와 24개 함수/클래스 span SHA를 대조했다. 이는 기능 검증이 아니다.
- 74개 정적 `matched=true` 기록과 검증안의 8군/50개 고유 ID, Python 44/Java helper 6, 예산 합계 1,350초는 구조상 일치한다. 정적 검사기의 `plan_expected_reach`는 문자열의 존재를, `plan_positive_controls_exist`는 ID 존재만 확인한다(`tools/static_check.py:54–55`). 실제 경로 적합성까지 증명하지 않는다.
- 33개 선택 원본의 BEFORE/AFTER_STATIC/AFTER_PREPACKAGE 식별 집합은 동일하다. 원격 기계의 현재 33개 파일을 리뷰어가 새로 측정한 것은 아니다. 동봉 원 R1 21개와 manifest는 여기서 실제 바이트를 대조했다.

## 2. 수정 요구

### OPEN-R1-N1 · P1 · 경과시간 원점을 샘플 밖의 고정 기준에 결속

좌표: `candidate/resource_connection.py.inactive.txt:69–86`, `reference/r1/candidate/control.py.inactive.txt:195–199`.

`project_owned_sample`은 `raw.native_origin_s`와 `raw.overall_origin_s`가 유한하고 순서가 맞는지만 확인한다. 실제 시작 때 고정한 원점과 대조하지 않고 그 값으로 경과시간을 계산한다. `anchors`는 Job/root/출력 경로를 결속하지만 이 두 원점은 결속하지 않는다. 뒤의 실제 `control.assess_resources`는 계산된 경과시간을 믿는다.

정적 반례: 실제 전체 원점 0, native 원점 300, 현재 end 10000이면 실제 전체/native 경과는 10000/9700초다. 그런데 동일 Job·멤버·정상 counter를 두고 raw의 두 원점만 9960, start=9999.5, end=10000, previous_end=9995로 주면 시간 순서·간격 5초·측정기간 0.5초 조건을 모두 만족하면서 두 경과가 40초가 된다. 다른 counter가 한도 안이면 현 코드의 시간 제한 분기는 중지 사유를 만들지 못한다. 이는 COMSOL에서 실제 발생한 예산 위반 신고가 아니라 새 투영 함수의 결속 누락이다.

필요한 수정:

1. 실행 시작 시 한 번 확정한 전체/native 원점 및 clock 단위를 샘플과 독립된 고정 context에 둔다. raw에도 원점을 기록한다면 그 context와 정확히 대조하고, 계산은 고정 원점으로 한다. 별도의 검증된 상위 경계에서 이를 보장하려면 그 실제 호출 경로와 결속을 이번 검증 대상에 포함해야 한다. 단순 주석으로 책임을 넘기지 않는다.
2. 샘플 하나가 원점을 새로 정하거나 바꾸지 못하게 한다. 원점 부재·변경·다른 run/clock 기준은 명시 이유로 거부한다. 기존 수치 예산·reserve는 바꾸지 않는다.
3. 같은 Job/정상 counter의 양성, 원점만 이동한 음성, 고정 원점 기준으로 실제 예산이 넘는 경우를 한정 검증안에 넣는다. 아직 실행하지 않는다.

OS 수집기가 미구현이라는 기존 OPEN은 그대로다. 다만 이번에 작성한 순수 시간 투영을 검증하기 전에 그 입력 계약을 고정해야 한다.

### OPEN-R1-N2 · P2 · 잘못된 process counter 구조도 명시적인 STOP으로 반환

좌표: `candidate/resource_connection.py.inactive.txt:49–58,96–104`.

`process_counters`는 list와 길이만 검사하고 각 항목의 dict 여부를 확인하기 전에 `p.get(...)`을 호출한다. 멤버 한 개에 `process_counters=[null]`이면 앞단 검사를 통과한 뒤 `AttributeError`가 발생한다. `resource_decision`은 `ResourceConnectionError`만 받아 `STOP_REQUIRED`로 바꾸므로 이 오류는 약속된 반환 형식을 벗어난다. 숫자 0이나 PASS로 바뀌는 오류는 아니지만, 자원 감시 실패를 중지/정리 상태기로 전달할 구조화된 결과가 없다. 미래 실행기의 일반 예외 처리가 이를 보완한다고 이번 후보에서 증명하지 않았다.

각 counter 항목의 타입·필수 키·PID/creation 타입을 읽기 전에 검사하고 전용 이유를 주도록 한다. `null`, scalar, 누락된 키 등은 해당 투영 단계의 실패로 기록하고, 기존 실제 `assess_resources`에는 전달하지 않는 경로를 고정한다. 모든 예외를 무조건 PASS나 정상 counter로 치환하는 수정은 안 된다. 정상 양성과 이 잘못된 구조의 음성을 추가부 검증에 포함한다.

### OPEN-R1-N3 · P2 · 사례의 실제 도달 경로와 같은 분기의 양성 대조를 고정

좌표: `LIMITED_VALIDATION_PLAN.json` C04-03~05, C07-03~06, C08-01~06. 특히 C07-03의 577–586행.

- **C07-03:** `raw.query_success=false`는 `project_owned_sample` 첫 검사에서 `OS_QUERY_FAILURE`를 내고 `resource_decision`의 except로 돌아온다. 계획의 필수 도달 경로 `resource_decision -> control.assess_resources`에는 도달할 수 없다. 올바른 기대는 **project_owned_sample에서 이유 발생 → resource_decision이 STOP_REQUIRED 반환, assess_resources 호출 0**이다. 원래 차단 코드를 약화해 뒤 함수에 억지로 도달시키면 안 된다.
- **C04-03~05:** 현재 양성은 C04-01(`proof=None`)이다. 이는 non-null proof 검사를 전혀 거치지 않는 조기 반환이다. 이미 존재하는 C04-02의 바이트/방법/grid가 맞는 non-null proof를 각 음성의 대응 양성으로 지정한다. C04-01은 별도 INCONCLUSIVE 분기 확인으로 남긴다.
- **C07-05/06:** 양성 C07-01은 `assess_resources` 경로이고 `advance_stop`을 호출하지 않는다. C07-04의 동일 STOP_REQUESTED/소유·capability fixture를 대응 양성으로 지정하거나 별도 같은 분기의 양성을 명시한다. 판정 위치도 `transition.error`, `action` 등으로 고정한다. 강제 종료 *계획*은 실제 강제 종료 관측이 아니다.
- **C08:** property/equation/stored-grid를 서로 다른 양성으로 연결한다. C08-05는 C08-04처럼 stored-grid 양성을 기준으로 실제 원 `checkShape`의 `TIME_ORIGIN`에 도달해야 한다. 하네스가 해당 예외 문자열을 스스로 만들어 내면 증거가 아니다. 실행 전에 정확 추출 함수/기존 의존부의 span·SHA 및 stub 경계를 고정한다. helper 시험으로 COMSOL API 호환성까지 수용하지 않는다.

N1/N2를 반영하면 사례 수가 달라질 수 있다. 50개 숫자를 유지하려고 필요한 사례를 누락하지 말고, 확정 ID/엔진/입력/기대 이유·반환 위치/필수 및 금지 도달 함수/양성/횟수·예산을 새 plan과 manifest로 봉인한 뒤 별도 승인을 받는다. 기존 R1 130사례 재실행은 요구하지 않는다.

## 3. 네 OPEN은 그대로 유지

| OPEN | 이번에 인정할 수 있는 범위 | 아직 필요한 것 |
|---|---|---|
| 설치본 post-consistency t0 | 저장 0과 초기화 의미를 구분하는 미호출 helper 및 문서 근거 | 실제 CDI/Time 순서·solution index·재고/조성의 설치본 증거 |
| 설치본 계수 연결 | typed property와 recursive/all 정보표 후보 | 실제 변수/domain/단위/생성식과 평가 수치의 봉인 |
| native 원자료 연결 | 바이트·Decimal·grid·전류/Li 투영의 후보 | 실제 로그/단위/종료사유 loader, 초기화/계수 provider, 검토된 적분오차 방법 |
| OS 소유·자원·중지 | 기존 상태기 연결 및 이번 순수 투영 후보 | 실제 counter/ABI/Job cap/스케줄러/중지·정리 provider 및 별도 검증 |

`FeatureInfo`의 recursive/all와 `PropFeature`의 getType는 동봉 설치 도움말 텍스트와 맞는다. 이것은 실제 설치 API 호출·타입 호환성·계수 의미를 확인했다는 뜻이 아니다. 이번 리뷰는 설치본/Windows 원격 관측을 하지 않았다.

기본 installed/OS provider가 OPEN 오류로 막고, 정확 native argv/cwd·승인 경로가 null이며, R1 manifest와 기존 authorization의 schema 차이를 공개한 점은 적절하다. 이를 지금 수정해 native로 연결하라는 요구는 아니다. 문서 A~E는 별도 검토 순서이지 이번 리뷰의 실행 허가가 아니다.

## 4. 보충 전달 기록 수용 범위

사용자가 추가 제공한 JSON 본문을 전달 기록의 후속 전사로 함께 검토했다. ZIP 밖 파일 자체의 원바이트를 받은 것은 아니므로, 전사문을 다시 저장한 바이트에 원 파일 SHA를 붙이지 않는다.

| 경계 | 전체/전달 경과초 | 의미 |
|---|---|---|
| 내부 포장 전 | 1630.4865287 / 75.4538854 | 내부 closeout |
| ZIP 재읽기·원본 대조 후 | 1631.3320085 / 76.2993652 | 영수증 쓰기 전 |
| 영수증 쓰기·재읽기 후 | 1631.396287 / 76.3636437 | d512d1 출력/반환 전 |
| 최종 확인 파일 쓰기 전 | 1684.9520819 / 129.9194386 | FINAL_SUBMISSION_CHECK 본문 |
| 최종 확인 파일 쓰기·재읽기 후 | 1685.0463578 / 130.0137145 | **확인 파일 SHA 계산·도구 반환 전** |

준비 1466.6525769/2400초, 정적 88.3800664/600초는 tick 차이와 정확히 맞는다. 전달 원점 차이 1555.0326433초도 위 전체/전달 snapshot과 맞는다. 기록된 범위는 전체 3600초·전달 480초 안이다. 폴더 관측 4,949,132 bytes도 50 MiB 안이다.

`FINAL_CHECK_TOOL_STDOUT.phase`의 HASH 포함은 후속 `timing_scope` 정정대로 좁혀 읽는다. SHA 계산 이후·도구 반환 이후·반환 전사 자신의 쓰기까지의 완전 종료 시간은 관측하지 않았다. wall time 7.2067983/6.7977399를 snapshot에 더하지 않는다. 이는 기록 누락을 예산 초과로 판정한다는 뜻이 아니다.

포장 후 원본 기록의 보고된 SHA `eab7035b…6306c`는 동봉 BEFORE/AFTER_PREPACKAGE 원파일 SHA와 같다. 제출자가 보고한 post-package 재대조와 연결되는 근거로 받되, 리뷰어의 원격 새 측정이라고 부르지 않는다. 현재 보충 내용으로 코드 검토를 계속하는 데 추가 포장·재측정은 필요 없다.

## 5. 다음 한 건

**새 비활성 revision에서 N1/N2의 투영 계약·코드, N3의 검증안만 정정하고 정적 재봉인 결과를 제출하는 작업**을 권고한다. 사용자 별도 승인 전에는 수정도 실행도 시작하지 않는다. 원 R1과 이번 제출본/74개 기록은 덮어쓰지 않는다. 기존 130사례 수용·기존 실패·recipient=null을 유지한다.

그 정정본의 원점·형식·도달 조건이 닫히면 새 하네스 봉인과 변경부 한정 검증만 별도 승인할 수 있다. 그때에도 COMSOL 실제 관측과 P0는 별도다. 지금 microshort 효과를 확보했다는 결론이나 K/장시간 연장 승인은 없다.

자료 검증 방법은 `INPUT_CHECK.json`, `DATA_AUDIT.json` 및 검토자 작성 스크립트에 남겼다. 검토자 자체 데이터 검사에서 구분 빈 줄 가정과 encoding 이름 오타를 정정한 두 실패는 `REVIEWER_METHOD_NOTES.json`에 공개했다. 제출 코드/시험 실패로 세지 않았다.
