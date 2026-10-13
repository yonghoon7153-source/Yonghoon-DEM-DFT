# S1 OPEN-R1 003 한정 검증 검토

2026-10-13. 결과 본체와 ZIP 밖 기록, 추가 제출한 Python 사전 관측 보충본을 대상으로 한 독립 정적 검토다.

## 판정

**봉인된 9군 93사례의 한정 기능 검증을 수용한다. 현재 기능 결과를 막는 P1은 발견하지 못했다.** Python 87개와 Java helper 6개의 결과·이유·도달 경로가 해당 계획과 연결된다. 기존 130개 시험이나 COMSOL 계산을 반복할 필요는 없다.

수용 상태는 `LIMITED_VALIDATION_ACCEPTED_WITH_DOCUMENTED_SCOPE`다. `native_ready=false`, `approved=false`, `usable=false`, 전체·정상 gate `INCOMPLETE`를 유지한다. 승인 플래그를 바꾸거나 실제 실행을 시작하는 판정이 아니다.

보존은 구간별로 수용한다. `_003`의 선택 114개와 `_002` 선택 중지 기록은 전후 결속을 확인했다. 추가 `_001` 원문과 보존 기록은 **그 당시 Python 사전 관측 구간**의 근거이며, `_003` 전후 보존으로 소급하지 않는다. §보존 기록의 구간 정정을 함께 적용한다.

## 식별과 무결성

- 결과 ZIP: `COMSOL_MICROSHORT_S1_OPEN_R1_VALIDATION_003_20261013.zip`, 665,105 bytes, SHA256 `6458419127231ce44203ddef9d10981954ae877fdbf990faab5d3649db172bb3`.
- PACKAGE_MANIFEST: 24,117 bytes, SHA256 `0345322ff029459bb421a8b249f785c06e46455fdaa8beb5f69ba9ff42975961`.
- payload 138개 + manifest 1개. 정확 집합·크기·SHA·CRC·대소문자 중복·경로·심볼릭 링크 검사를 통과했다. 검토자가 새로 수행한 archive CRC 확인은 제출 당시의 CRC 확인 범위를 소급 변경하지 않는다.
- 원 CODE_MANIFEST: `feb12ef6991141aab59fd2fbc0d5f0d138bdd735255aa7123274503ce80b8ecc`.
- 유효 검증안: `88a56e55f2b5a94956a708ed1e84a97c0c5531bf461cb6d76165b178717b34e5`.
- CASE_RESULT_MAP: `b220139aeb41f0d797ab5e203c430046280b39990b6711e362c6316df1c0a2cd`.
- 포장 후 AFTER 원파일: 34,659 bytes, SHA256 `b22417b5f8a42da934f58bc73941c40eb1fd35d557a7e3eaaa2c347652757e4d`. 붙여넣은 텍스트 첨부의 실제 바이트와 일치한다.

원문 결과와 사본 78개를 재해시했다. 원격 실행 기계의 파일을 지금 다시 측정한 것은 아니다. 과거 도구 반환 전사는 원시 OS 감사나 이번 검토자의 직접 실행 관측과 구분한다.

## 93사례 집계와 실제 도달

| 범위 | 사례 | 확인 결과 |
|---|---:|---|
| Python C01–C07 | 44 | raw 변환·증거 소비·수지·자원·중지 계획의 봉인 사례와 결과 일치 |
| Python C09 | 43 | 고정 시계 문맥·session·counter 형식 거절 및 실제 자원 판정 연결 일치 |
| Java helper C08 | 6 | 원문 추출·stub 경계·표 출력·예외 전파가 봉인 사례와 일치 |
| 합계 | 93 | 고유 ID 93, PASS 93, FAIL 0, 최종 NOT_RUN 0 |

군별 수는 C01=7, C02=6, C03=5, C04=5, C05=7, C06=8, C07=6, C08=6, C09=43이다. 계획과 최종 map의 사례 집합·기대 결과·필수/금지 도달·계획 호출 수가 모두 같다. map의 actual은 Python 원시 결과 또는 Java 원시 출력의 해당 객체와 정확히 같다.

Python 단계의 `not_run=6`은 전체 93개 배열에서 뒤의 Java 6개가 아직 실행되지 않은 상태다. Python 사례 누락이나 최종 미실행 6개가 아니다. 이 원문을 고치지 않고 Java 후속 결과와 결합한 방식은 수용한다.

Python에서는 계획상 함수 호출 횟수 기대항목 331개, 명시적 금지 함수 횟수 기대항목 136개를 대조해 불일치가 없었다. 이 수는 총 호출 횟수가 아니라 대조 항목 수다. `optimize=0`이 기록돼 assertion이 꺼진 실행이 아니다. 대상 로드 전에 위험 진입을 inert 처리했으며, 이를 OS 수준의 독립 격리 증명으로 확대하지 않는다.

- **C05:** 실제 `consumer.analyze` 1회의 반환 = 보존 expected = 관측 반환 = 연결 함수의 반환이다. 동일 객체 확인도 활성 상태였다. 합성 proof provider가 실제 설치본 관측을 대신 증명한 것은 아니다. 근거: `cases_raw.py:97–119`, `run_python.py:207` 및 `PYTHON_TRACE.json`의 C05-01.
- **C09:** 한 session에서 두 decide가 고정 원점을 사용한다. 원점 불일치는 assessor 전에 거절되고, 임계값 사례는 실제 `control.assess_resources`에 도달한다. caller dict 변경, 실제 frozen dataclass 대입 예외, counter의 dict/필수 키/정수형 순서 및 typed catch를 확인했다. 근거: `cases_resource.py:40–74`, `reference/022_resource_connection.py.inactive.txt:65–184`.
- **Java:** 12개 source slice의 전체 파일·구간 해시와 helper의 바이트가 일치한다. header 912 + 원문 구간 6,870 + tail 16,503 = helper 24,285 bytes다. SHA256은 `4664c984db7d34fa66596176c8912f3ce33910f1df9c58ead439b4c5252da639`다. 6개 원시 출력의 표·예외·호출 순서를 확인했다. 근거: `JAVA_EXTRACTION.json`, `OpenReadbackHarness.java:21–117,225–230`, `Java_helper.stdout.txt:1–7`.

Java의 type/model/FeatureInfo/NumericalFeature는 stub이다. 따라서 설치 COMSOL API 호환성이나 전체 P0 컴파일 PASS로 읽지 않는다. C08-04의 저장 시각 0도 일관 초기화 직후 상태라는 증명이 아니며, 원문처럼 `POST_CONSISTENCY_PROOF_OPEN`이다.

## 소스와 엔진 결속

PRETEST_SEAL은 첫 Python 예약 전에 작성됐고, 소스·하네스·입력·명령·엔진 핀이 연결된다. 세 단계 argv/cwd/상한은 부속 승인 기록·봉인·예약·반환에서 일치한다. 실행은 원 source root를 소비하며 전달 ZIP의 reference 사본을 실행 경로로 바꾼 것이 아니다.

Python 현재 핀은 106,448 bytes / `10d845f50a2af64e3500bb2fcb348b5bc98a75d8ddada63e45ba1da6a1fc79d1`, 단일 세션의 판은 3.12.14다. 과거 107,312 bytes / `b7a12c3a…ddca2`는 이전 기대값으로 남아 있다. 엔진 교체를 동일 바이트라고 처리하지 않았다. 모듈 원점 기록에서 frozen/built-in을 실제 소스 로딩으로 오인하지 않는다.

`_002`의 새 Python 승인 전사, 중지 판정, `_003`의 “다시 ㄱ” 재개 전사가 연결돼 있다. 이는 보존된 승인 기록을 읽은 것이지 검토자가 별도 대화 원본을 감사한 것은 아니다. 비활성 초안 필드를 실행 허가로 읽거나 이를 true로 고치지 않는다.

## 보존 기록의 구간 정정

PRETEST_SEAL·시험 후·포장 후 AFTER의 **114개 고유 경로**는 크기와 SHA가 같다. 이 중 `_002` 선택 파일은 33개다. reference 사본 78개와 현재 attempt 파일 21개는 첨부 바이트로 대조했으며 서로 중복될 수 있으므로 합산해 고유 원본 수라고 부르지 않는다. runtime/engine 36개는 실행 기계의 기록된 식별이며 검토자가 현재 바이너리를 다시 해시한 값이 아니다.

**P2 기록 범위 정정:** `REPORT_KO.md:14` 및 `RESULT_SUMMARY.json:108`의 `_001·_002 보존`은 아래처럼 구분해야 한다. 원 봉인본을 수정하지 말고 회신 접수 기록에 부속 정정으로 남긴다.

> `_002` 선택 기록은 `_003`의 114개 전후 대조에 포함된다. `_001 FIRST_ERROR.json`은 별도 사전 관측 ZIP에서 원문과 당시 전후 기록을 확인했다. 그러나 `_003`의 114개에는 없으므로 `_003` 실행 전후 불변은 미확인이다. 변조됐다는 뜻은 아니며 현재 해시를 새로 재어 과거 구간을 메우지 않는다.

추가 ZIP은 `COMSOL_MICROSHORT_S1_OPEN_R1_PYTHON_PREFLIGHT_20261013.zip`, 53,751 bytes, SHA256 `45bdff07b0db0d24f96766e6224807822ddae6278405a663924c4080edbb8fe8`다. `_001` 원문 기대 식별은 1,448 bytes / `df14d1c180cecf5b4dd51816321b6d5d201649254e9c8fbaaf42b9d4b6be0269`다. 사전 관측 구간은 10월 13일 02:04–02:07 KST이며 이후 `_003` 구간으로 확대하지 않는다. 추가 대조의 세부는 `notes/PROVENANCE_SUPPLEMENT_AUDIT.json`을 따른다.

이 정정은 기능 93사례의 수용을 막지 않는다. `_001` 원문 보충 이전의 검토 메모는 보충 후 판정으로 대체하되, `_003` 구간 미확인 한계 자체는 남긴다. 이전 중지를 PASS로 다시 쓰지 않는다.

## 시간과 반환의 경계

| 단계 | 기록된 경과 | 한도 |
|---|---:|---:|
| 하네스 사전 봉인 | 499.0560668 s | 600 s |
| Python 한 세션 | 10.8930094 s | 180 s |
| Java helper 컴파일 한 번 | 1.7277404 s | 90 s |
| Java helper JVM 한 세션 | 0.5369169 s | 60 s |
| 마지막 최종 확인 snapshot | 809.8249618 s | 전체 1,350 s |
| 같은 최종 확인의 전달 경과 | 248.7441909 s | 300 s |

Python 내부 측정 10.5561265초는 외부 stage 측정과 다르다. 보존/전달 원점은 마지막 JVM 종료 누적 561.0808747초다. 기록된 봉인·엔진·최종 snapshot은 각 상한 이내다. 전체 snapshot에서 원점을 뺀 값과 별도 delivery 읽기는 약 0.000104초 차이로, 동시 측정이라고 합치지 않는다.

최종 809.8249618초는 확인 파일 쓰기·재읽기·해시 후, 도구 반환 전의 값이다. 마지막 전사 저장·그 반환까지 모두 포함한 최종 전체 경과는 관측됐다고 하지 않는다. 도구 wall time을 더하지 않는다. ZIP 밖 receipt/반환/최종 확인은 사용자가 제공한 내용 전사로 대조했고, 이 JSON들의 원파일 SHA를 검토자가 전부 독립 재해시한 것은 아니다. 포장 후 AFTER는 원파일 첨부를 직접 확인했다.

이 경계는 제출자가 명시한 것과 같고, 새 시간 측정·재포장·재시험을 요구하지 않는다. 수용은 **기록된 예산 관측 범위**에 한정한다.

## 남은 네 OPEN과 다음 경계

1. 설치본의 일관 초기화 직후 t0 증거.
2. 생성식과 실제 설치 계수·변수/API의 결속.
3. native 원시 증거를 소비자와 Parent까지 연결하는 어댑터.
4. 실제 OS 자원·소유권·중지 어댑터.

이번 합성 시험은 이 네 가지의 설치본·운영 증거를 만들지 않았다. 자원 hard cap·실제 종료·실효 정책·실제 코어도 새로 검증하지 않았다. Parent manifest 세대 연결, quadrature bound 등의 하위 미완도 OPEN 지도 그대로 남긴다.

다음 제안은 네 OPEN 중 먼저 닫을 항목의 **설치본 관측 및 연결 구현 범위·검증안**을 따로 고정하는 것이다. 기존 93개를 다시 돌리는 단계가 아니며, P0·native·microshort 물리 효과 실험을 자동 승인하지 않는다. 현재 결과는 “microshort 효과 입증”이 아니라 “지정된 연결 코드의 합성 검증 수용”이다. 현재 보고·판정 접수 뒤 실제 계산 없이 멈춘다.

## 검토 수행 범위

수신 ZIP/JSON/소스/로그를 데이터로 읽고 자체 해시·CRC·텍스트·구조 대조를 수행했다. 수신 코드 import·함수 실행·재시험·엔진 probe·컴파일·JVM·COMSOL 실행은 0회다. 검토 자료 작성용 도구는 사용했다. 자체 집계기의 첫 읽기에서 Java footer를 사례로 잘못 읽은 오류는 REVIEW_ACTIVITY_NOTE에 보존했으며, 수신 시험 실패와 구분했다. 외부 발송이나 실행 승인 파일 생성은 하지 않았다.
