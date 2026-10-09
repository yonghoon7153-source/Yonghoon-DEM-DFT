# S1O R1 004 한정 검증 종결 검토

2026-10-09. 판정은 **LIMITED_VALIDATION_CLOSED_WITH_DOCUMENTED_SCOPE**다. 이전 회신의 S1O003-N1 하네스 보완과 S1O003-N2 동일 기본 입력 양성 보완을 수용한다. 원래 130개 사례의 충족 근거는 **R1_003의 127개 재사용 + R1_004의 원 미완 3개 신규 충족**이다. 새 Python 양성 4개는 별도 보조 대조다.

이는 비활성 R1 소비자·제어·부모의 한정 오프라인 검증 종결이며, S1-O 전체 준비 완료나 COMSOL 실행 승인이 아니다. `native_ready=false`, 전체·정상 gate `INCOMPLETE`, 설치본 t0·실효 계수·native/raw/OS 어댑터 OPEN을 유지한다. 원 R1_003의 실패와 INCOMPLETE를 고쳐 쓰지 않는다.

## 입력 식별과 검토 범위

| 항목 | 직접 확인한 식별 |
|---|---|
| R1_004 ZIP | 796,501 bytes · `cb85fa123395caf9ea323b0c531144bf30754322ba9b0362f1bbac3e5bc8ff2c` |
| PACKAGE_MANIFEST | 8,399 bytes · `83a07d177e52bb5bd9069e4267d6a731c5a0bfa7e7b490d10d1c5b8945e8311c` |
| 구성 | payload 50개 + manifest 1개; 정확 집합·크기·SHA·CRC·경로·대소문자 중복·symlink 검사 일치 |
| 내장 R1_003 원 ZIP | 876,456 bytes · `11a27f3034fed763442ccce9730f7e008058b819bfbffd9d58a5d2994b875d4b`; 이전 검토의 154개 파일과 바이트 동일 |
| 생산 CODE_MANIFEST | `4ce5c08dbde5153027819b5a651e3995ec82417b4429b9bb0f789082b440f5da`; 21개 구성원 식별 유지 |
| 새 PS 하네스 | `f2859616a8cf3b484fad97ff7ecdfb89ebf8a696d4742d722e3ebf4e80270b32` |

검토자는 ZIP을 데이터로 읽어 해시·기록·정적 소스 및 fixture 데이터 식별만 대조했다. 받은 모듈 import, AST 실행, 후보 함수 호출, 기능 시험, COMSOL/JVM/compile/solve, 실제 입력·Job·정책 조작은 하지 않았다. 검토자의 565개 데이터 대조는 새 기능 사례 수가 아니다.

세부 재현 근거는 `INPUT_CHECK.json`, `RECORD_AUDIT.json`, 검토자 작성 `inspect_data.py`·`audit_evidence.py`에 있다. 이 스크립트들은 받은 프로그램의 실행기가 아니다.

## 원 미완 3개 수용

실제 제출 PS 세션의 순서는 R115 → R113 → R114다. stdout의 3개 JSON과 `results/ps_results.json`의 사례가 모두 일치한다. 원문 결과·하네스·추출 함수 식별을 함께 대조했다.

| 사례 | 확인한 입력 및 도달 | 판정 |
|---|---|---|
| PARENT_R115 | 기존 POLICY02 문자열 `"0.001"`; S1Decision → S1Fields → S1ComparisonNumerics | 정상 판정 경로의 `WITHIN_LIMITS_THIS_WINDOW` 수용 |
| PARENT_R113 | 같은 producer의 숫자 token 변이 후 명시적 Double fixture; 위 실제 함수 경로 진입 | `DECIMAL_TRANSPORT_PRECISION`, `stage=comparison_numerics` 수용 |
| PARENT_R114 | POLICY03의 두 summary 필드만 WITHIN으로 바꿈; 실제 함수에서 수치와 summary 재대조 | `COMPARISON_SUMMARY_CONTRADICTION`, `stage=fields` 수용 |

R113의 파싱 직후 타입은 기록상 `System.Decimal`, 값은 `0.001`이다. `harness/ps_subset.ps1:129–154`는 타입 assertion 전에 진단을 저장하고, null·문자열·bool·비수치·비유한·값 불일치를 검사한 뒤 해당 leaf만 Double로 바꾼다. 이를 JSON 파서가 원래 Double을 만들었다는 증거로 사용하지 않는다. R1_003 당시의 미기록 CLR 타입도 이번 결과로 소급 확정하지 않는다.

문자열 token의 따옴표 두 개만 제거한 mutant는 122,638 bytes, SHA `b49a89a13fe0313f27f02053441c5db6e9e9741476a325b497478964788dc013`이다. 원 producer SHA·token offset 122002·Double 비트 `3F50624DD2F1A9FC`도 독립 데이터 대조와 일치한다. 원 생산 함수 `S1ExactDecimal`의 비정수 CLR 숫자 거부가 `S1ComparisonNumerics`의 이유·단계로 반환되는 경로와 기록이 정합적이다.

R114의 양성 PARENT02는 재호출하지 않았다. 원 POLICY03 JSON/context, Parent·추출 함수, 엔진 식별, 원 PARENT02 반환 `EXCEEDS_LIMITS`와 도달 기록을 연결했다. 공통 HProducer의 바이트 읽기·JSON parsing 본문은 변경되지 않았다. R113 전용 cast를 다른 사례나 일반 파서에 적용한 것이 아니다.

근거: `received/harness/ps_subset.ps1:20–32, 129–159, 179–219`, `received/results/ps_results.json`, `received/REUSE_MAP.json`, 내장 R1_003의 `source/candidate/Parent.ps1.inactive.txt:27–35, 156–168, 272–298`.

## 보조 양성 4개와 기존 READ 사례의 연결

| 보조 양성 | 확인한 같은 기본 입력 | 연결한 기존 음성 |
|---|---|---|
| READ_CTRL_CSV | `time_s,value\n0,1\n1,2\n`, 정확 header·단위·fixture/simple.csv 식별 | READ02–07 |
| READ_CTRL_TIME | time_s만 있는 Decimal 0/1 두 행, end 문자열 `1` | READ08 |
| READ_CTRL_COVERAGE | 양쪽 Decimal [0,1], 세 문자열 요청 [0,1], safe `1` | READ09–10 |
| READ_CTRL_PROFILE | t0 N241점, 원 좌표·domain1·50자리 Decimal 규칙 | READ11–12 |

새 Python stdout 4개와 결과 JSON이 일치하고, 각 사례는 대상 함수 1회 진입 및 정상 반환 assertion을 기록했다. 검토자는 후보 함수를 호출하지 않고 기본 입력을 별도로 구성하여 봉인된 definition과 fingerprint를 대조했다. 이어 선언 변이만 적용한 11개 데이터 fingerprint가 R1_003의 `CONSUMER_INPUT_IDENTITIES.json`과 모두 일치하는지 확인했다.

READ05–07의 raw 교체와 identity 재계산은 복수 변경으로, READ10은 다섯 벡터에서 1을 제거하는 변경으로 명시되어 있다. 이를 단일 leaf 변이로 축소하지 않았다. 따라서 이전 11개 음성의 PASS 원문은 보존하면서 누락됐던 같은 기본 입력 양성 근거를 보완할 수 있다. 기존 음성 재시험은 필요하지 않다.

근거: `received/harness/inputs.py:5–29`, `received/harness/python_subset.py:17–39`, `received/INPUT_SEAL.json`, `received/results/PYTHON_RESULTS.json`.

## 재사용과 봉인

- 원 127개 ID·관측·도달 기록이 재사용 표와 일치한다. 새 3개를 합한 집합은 원 계획의 130개 ID와 정확히 같고 중복·누락이 없다. 보조 4개는 `auxiliary_cases`로 분리했다.
- 43개 추출 span의 비어 있지 않은 소스 텍스트 SHA를 대조했다. PS 관측 15개 span도 같은 식별이며, 기존 S1Sha 23–23행 정정이 유지된다.
- 새 PS_PRODUCER_SEAL은 새 하네스 SHA를 가리킨다. producer/context 10개는 원 바이트 그대로이며 Python producer를 재생성한 것으로 기록하지 않는다.
- 전후 보존 표 246개는 정확히 같은 집합과 식별이다. 원 봉인 123개를 포함한다. 이 중 전달 자료 안의 183개 파일 바이트는 직접 대조했고, 나머지 63개 엔진·환경 파일은 실행 기계의 제출 식별 기록으로만 수용한다. 검토자가 BML 기계의 현재 엔진을 직접 측정한 것은 아니다.
- source manifest의 `FUNCTIONAL_VALIDATION_NOT_RUN` 같은 생성 당시 문구를 지금 고쳐 재봉인하지 않는다. 검증 종결 상태는 이번 별도 회신으로 연결한다.

PS_PRODUCER_SEAL의 `utc`는 재사용한 R1_003 producer seal 시각이다. 새 하네스의 사전 봉인 시각으로 사용하지 않는다. R1_004 FIRST_SEAL의 원점·경과와 두 ATTEMPT가 가리키는 FIRST_SEAL SHA로 새 세션의 연결을 판단했다.

## 예산과 전달 경계

| 경계 | 제출 기록 | 해석 |
|---|---:|---|
| 사전 봉인 | 381.8903014 / 600초 | 새 원점의 준비 단계 |
| Python 프로세스 | 0.4329076 / 120초, rc0 | session 파일 쓰기 전 |
| Python 기록 후 | 0.4488671 / 120초 | tool 반환 원문의 POST_SESSION_RECORD_WRITE |
| PS 프로세스 | 9.1690324 / 180초, rc0 | session 파일 쓰기 전 |
| PS 기록 후 | 9.1838897 / 180초 | tool 반환 원문의 POST_SESSION_RECORD_WRITE |
| ZIP 내부 closeout | 전체 569.5799204, 전달 116.4652898초 | 포장 전 |
| 사용자 첨부 receipt 내용 | 전체 569.9025540, 전달 116.7879229초 | ZIP 재읽기 후·receipt 쓰기 전 |
| 사용자 첨부 eb8612 반환 전사 | 전체 569.9144170, 전달 116.7997864초, rc0 | receipt 재읽기 후·도구 반환 전 |
| 사용자 보고 최종 확인 | 614.480 / 1200초 | 해당 별도 원문은 현재 미제공 |

기능 시험 및 위 기록으로 확인되는 전달 snapshot은 전체 1200초·전달 240초 안이다. 도구 wall time 6.7332629초를 569.914417초에 더하지 않는다. 614.480초를 포장 snapshot 또는 직접 확인한 종료 측정으로 바꿔 쓰지도 않는다.

ZIP 밖 DELIVERY_RECEIPT와 FINAL_PACKAGE_TOOL_RETURN은 이번에는 사용자가 붙여준 내용으로 확인했다. 원본 파일의 전바이트 SHA를 독립 확인했다고 하지 않는다. ZIP 자체의 크기·SHA는 직접 일치했다. 614.480초의 당시 원문은 추가 요청했으며, 이 전달 경계의 확인 범위를 기능 검증 종결과 분리한다. 새 측정·재시험·재포장으로 과거 경계를 보충할 필요는 없다.

## 남은 것과 다음 순서

이번 잔여 한정 검증에는 새로운 차단 결함을 찾지 못했다. 기존 130개 전체를 다시 실행할 이유는 없다. 다만 실제 microshort 효과를 측정한 결과도 아직 아니다.

다음은 기존 OPEN에만 범위를 한정한 **설치본 관측·실행 어댑터 연결 작업의 승인 범위 확정**이다.

1. 일관초기화 직후 정확 t0를 같은 승인된 solve 안에서 확인할 방법, CDI 종류 및 초기 재고·조성의 원시 증거를 고정한다. 첫 양의 시각이나 입력 설정을 t0 관측으로 바꾸지 않는다.
2. 생성식·실제 계수의 설치본 변수/API와 raw artifact → 소비자 입력 매핑을 결속한다. 단순 설정값을 실효 계수라고 쓰지 않는다. 전체 저장 시간·단위·전류/전하·Li·보호중단 증거와 수치 적분오차 근거도 같은 raw 경로로 연결한다.
3. 소유 Job·자원 계측·중단·부모 반환 어댑터를 정확 API와 범위에 결속한다. 순수 상태기 시험 PASS를 실제 OS 구현 PASS로 승격하지 않는다. graceful stop이 지원되지 않으면 force-only의 별도 수용 조건을 먼저 정한다.
4. 위 변경부의 최소 검증과 현재 정책·자원 관측을 독립 수용한 후, 고정된 P0 한 건만 별도 승인한다. P1–P3, K 최대24회, 장시간 cohort를 일괄 승인하지 않는다.

이는 다음 범위 제안이며 이번 회신 자체가 구현·관측·COMSOL·실제 승인 파일 생성 권한은 아니다. 원 실패·pending·원복·recipient=null, 실효 정책/실제 코어 UNVERIFIED, OCP 외삽 금지와 기존 장시간 보류를 유지한다.
