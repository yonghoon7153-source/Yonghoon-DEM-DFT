# R1_003 기존 PASS 재사용 독립 정적 검토

검토 대상은 새 중지 제출물 `received/`의 원문 결과, 정정 계획, 하네스, 입력/함수/producer 봉인이다. 받은 코드·함수·import·시험·COMSOL·하네스·제출 도구는 실행하지 않았다. JSON은 데이터로 읽었고 SHA/크기 비교와 텍스트 분기 대조만 했다. 아래 좌표는 `received/` 기준이다.

## 결론

**Python 99 + PowerShell 28의 원문 PASS 기록은 보존·재사용할 수 있다.** 실제 실행 결과라는 증거를 무효로 바꾸거나 이번 검토에서 재실행한 결과처럼 기록할 이유는 없다. 다만 **READ02–12의 동일 기본 입력 양성 대조는 미완**이며, 기존 127개가 모든 승인된 대조 요건까지 충족했다고 일괄 종결해서는 안 된다. 잔여 검증안 결함 P2 한 건을 아래에 기록한다.

기존 원문 127 PASS, PARENT_R113 목표 함수 전 하네스 실패 1, PARENT_R114/R115 미실행 2를 분리한다. 실패 원인 상세 및 새 PowerShell 입력의 설계는 별도 담당 검토에 따른다. Python 추가 양성 4개로 READ 대조를 보완하고 원래 PowerShell 3개를 별도 승인 하에 성공시키는 후속안은 정적으로 충분한 최소 범위다. 성공 시에도 `기존 127 + 새 원래 대상 3 = 원래 130 coverage`, `새 보조 양성 4`로 나누며 단일 세션 130 PASS 또는 134개 원래 사례라고 쓰지 않는다.

## 원문 결과와 봉인 대조

- `VALIDATION_PLAN_CORRECTED.json`은 고유 ID 130개, Python 99개, PowerShell 31개다. `PYTHON_RESULTS.json`의 99개는 모두 PASS이며 원문 `PYTHON_STDOUT.txt`의 99개 JSON 행과 모든 내용이 순서대로 일치한다. 미실행 Python은 없다.
- `results/ps_first_failure.json`에는 PARENT01–16 및 PARENT_R101–R112의 28개 PASS만 들어 있다. current_case는 PARENT_R113이다. 마지막 전체 실패 요약이 stdout에 앞선 28개를 다시 포함하는 것은 두 번째 실행 기록이 아니다.
- Python 결과의 내부 elapsed는 168.86000000010245초, 외부 `PYTHON_SESSION.json`의 프로세스 관측은 169.2547576초/rc0이다. 서로 다른 관측 경계이므로 두 숫자를 같은 시각처럼 치환하지 않는다. 원문 stderr는 비어 있다.
- consumer/control/Parent의 현재 bytes SHA는 source manifest와 이전 R1 검토본 모두에 일치한다. 각각 `0cb1aa3c…6b79`, `8ec75e57…c00d`, `e9f8d366…56ff`다. 생산 코드 변경으로 기존 결과를 폐기해야 하는 근거는 없다.
- `FIRST_SEAL.json`에 있는 Python/PS 하네스, shared_fixture, input_binding, control_cases, CONTROL_MAP, 정정 PLAN, CONSUMER_INPUT_IDENTITIES, CONTROL_INPUTS의 선택 9개 파일은 현재 크기·SHA와 일치한다.
- `PS_PRODUCER_SEAL.json`의 producer 결과 5개 및 context 5개 전부 현재 크기·SHA와 일치한다. 하네스 `ps_harness:25–28,41–54`도 시작 전에 이 10개 원문을 검사한다.

## 목표 도달·사유·호출 수

`python_harness:16–24`는 실제 source AST의 import/class/function 노드를 읽어 정의하며 시험용 반환값으로 바꾸지 않는다. `input_binding:20–24`는 매 호출의 함수명·정규화 인수 SHA/크기를 사전 봉인 순서와 대조한 뒤 실제 함수에 전달한다. `python_harness:181–188`은 실제 `.inactive.txt` 프레임의 call/return을 기록하고, `210–223`은 기대 사유·도달 함수·stage·추가 필드·최초 위반·구간 sign 등을 확인한다. `235`는 최초 불일치 뒤 중단한다.

130은 최상위 입력 ID 수다. 함수 내부의 정당한 호출을 별도 시험으로 세지 않는다. READ01의 명시된 복합 양성 6회(read_csv 2, timed 1, coverage 1, profile 2), INIT01의 pair 1/individual 2, AUTH01의 execute_once 1/authorize_execution 1은 수정 계획 및 실제 count에 드러나 있고 `213–215`에서 고정한다. 나머지 소비자 top-level 호출은 input proxy의 순차 fingerprint로 제한된다. 선언된 경로 밖의 candidate 호출을 이번 정적 검토에서 발견하지 못했다.

`tools/seal_consumer_inputs:29–40`은 자체 fixture 생성 함수만 읽고 CaptureOnly를 넘기며, `CaptureOnly:13–27`은 fingerprint/자체 CSV 정규화만 수행한다. 소스 under test를 호출해 기대값을 만드는 구조가 아니다. 실제 consumer producer는 `python_harness:229–232`에서 해당 등록 사례의 **같은 analyze 반환값**을 기록한다. producer 확보를 위해 별도 analyze를 재호출하지 않는다.

대표 경로의 증거는 다음과 같다.

| 대상 | 실제 기록과 하네스 확인 |
|---|---|
| N1 격자 불일치 | CHARGE_R101–R104/R107은 analyze 및 charge_balance 도달 후 해당 grid/Li 오류. R105/R106은 analyze의 source 결속, R108은 초기 NATIVE_END_TIME에서 끝난다. 목표 사유와 stage를 구분한다. |
| N2 구간 역행 | R110/R111/R114는 REVERSE_LI_INCREMENT·charge_balance stage이며 analyze/charge_balance 각 1회. `219–221`이 최초 위반 구간·전극·deadband를 별도로 대조한다. R112/R113은 직접 charge_balance 1회, INCONCLUSIVE와 RESOLUTION_LIMITED 확인이다. |
| 정상 producer | CHARGE01은 VALID/errors=[]/CONSISTENT, full charge257, actual=safe120, comparison255다. |
| 보호중단 producer | CHARGE_R109는 VALID/errors=[]/CONSISTENT, full charge251, actual90.1/safe90, comparison249다. PARENT03 원문은 실제 S1Decision→S1NativeAxis→S1Fields까지 도달한 뒤 PROTECTIVE_STOP_INCOMPLETE다. 선행 schema 오류를 양성으로 세지 않았다. |
| 정확 수치 경계 | POLICY02 producer의 voltage 문자열은 0.001/WITHIN, POLICY03은 0.0010000000000000000001/EXCEEDS다. PARENT02는 EXCEEDS를 보존한 제한 결과를 실제로 수용했다. 미실행 R114/R115의 결과를 여기서 추론해 PASS로 세지 않는다. |
| 짝 경계 | PAIRED04는 실제 paired_classification 1회, INCONCLUSIVE이며 `223`에서 D=.001/S=.002/E_D=E_S=0을 별도로 검사한다. |
| 제어 | AUTH01은 실제 내부 authorization 반환, 14개 inert event, 가상 compile/batch count 1, 전체/native INCOMPLETE를 검사한다(`control_cases:276–282`). RESOURCE16은 같은 execute_once 입력에서 manifest.native_ready만 false이며 authorization 오류 및 adapter event0을 검사한다(`264–266`). 이는 실제 native 제어 검증이 아니다. |

## 이전 V1–V3 정정 상태

V1은 종결 가능하다. 수정 PLAN의 S1Sha는 23–23행이고 `ps_extraction_observed.json`에 실제 추출 90B/SHA `13c6456b30805e3b02063ca8cb804b201d948c5518bf01b102610297236d8eed`가 있다. `make_first_seal:24–28`은 비어 있거나 뒤집힌 범위 및 해시 불일치를 거부한다.

V2는 종결 가능하다. PARENT12는 `return_value.limited`로 정정됐고 `ps_harness:154–156,181`이 실제 최종 경계 함수를 호출해 limited 및 snapshot100/오류0/within_limits를 검사한다. 원문 record도 limited=AWAITING_S1_LIMITED_EXTERNAL_REVIEW, PRE99/POST100, clock2/writer1/readback1이다.

V3의 특정 함수 오연결은 고쳐졌다. INIT07/08/10은 실제 INIT09 verify_coefficient_evidence 양성에, FinalReturn09/10/11/16은 실제 PARENT12 양성에 연결된다. INIT01 pair/individual 복합 양성 및 AUTH01 execute_once 내부 authorize 양성도 명시되어 있다. 다만 다음 READ 동일 fixture 조건은 남았다.

## P2 — READ 공유 양성이 같은 기본 입력의 무변이 대조가 아니다

**정확 위치:** `harness/python_harness.py:85–113`, 특히 `85,87–96,99,105–112`; `VALIDATION_PLAN_CORRECTED.json:766–776,952–962`; `CONTROL_MAP.json:277–305`.

수정 계획 READ02는 “raw SHA mismatch” 하나를 변이로 지정하면서 “Same valid sealed fixture with only stated mutation removed”를 요구하고 READ01을 공유 양성으로 둔다. 하지만 실제 READ02의 무변이 기본 입력은 `b'time_s,value\n0,1\n1,2\n'`, header 2개, simple.csv identity, units s/1이다(`85,99,113`). READ01은 그 입력을 호출하지 않고 time_s/coordinate_m/domain_id/x_surface/x_particle_average **5열 N/P profile CSV** 61,455행씩 두 개만 파싱한다(`87–96`).

사전 `CONSUMER_INPUT_IDENTITIES.json`도 이를 확인한다. READ01의 reader 호출 fingerprint 길이는 4,905,422B/4,873,462B 두 개이고 READ02는 370B 한 개다. 차이는 의도한 SHA 한 필드에 한정되지 않으며 원래 tiny CSV의 무변이 성공 호출이 없다. 같은 함수에 도달했다는 사실만으로 같은 fixture 대조까지 완료되지는 않는다.

READ03–07도 같은 tiny CSV군인데 READ01을 양성으로 쓴다. READ08은 time_s만 있는 [0,0]/end1이고 READ01 timed_rows는 value도 있는 255행/end120이다. READ09/10은 0/1 또는 0만의 list 기반 coverage/end1이고 READ01은 full255 dictionary 기반/end120이다. READ11/12는 t0 한 시각 241점 profile_N인데 READ01 profile는 전체255시각이다. 따라서 READ02–12의 **기록된 목표 오류 PASS는 유지**하되, 요구한 동일 fixture 양성 대조의 충족은 보류한다. 이것은 production defect가 아니라 V3 검증 대조 요건의 잔여 결함이다.

### 최소 보완: 새 보조 양성 4개

생산 파일과 기존 127개 원문 결과를 보존한다. 별도 승인된 미래 한 번의 Python 세션에서 아래 직접 양성 입력을 각각 **한 번씩**, 새 고유 ID 4개로 봉인·관측하면 기존 11개 음성은 재호출하지 않고 대조할 수 있다.

1. **read_csv_bytes 양성 → READ02–07:** 정확 raw `b'time_s,value\n0,1\n1,2\n'`, header `['time_s','value']`, path `fixture/simple.csv`, 올바른 bytes/SHA, unit_record와 expected_units 모두 `{'time_s':'s','value':'1'}`. 반환한 Decimal 행 0/1 및 value1/2를 확인한다.
2. **timed_rows 양성 → READ08:** `rows=[{'time_s':Decimal(0)},{'time_s':Decimal(1)}]`, end_s 문자열 `'1'`. value 필드를 더하지 않는다. 실제 ordered keys0/1 반환을 확인한다.
3. **coverage 양성 → READ09/10:** times_a/times_b는 각각 **list** `[Decimal(0),Decimal(1)]`, requests_a/requests_b/common_requests는 각각 문자열 list `['0','1']`, safe_end 문자열 `'1'`. chosen0/1, PASS/count2/missing[]를 확인한다.
4. **profile_rows 양성 → READ11/12:** `shared_fixture:12,25–35`의 50자리 연산과 같은 t0 N241점, `times=[Decimal(0)]`, 동일 N 좌표241개, domain **int1**, 기본 coordinate_abs를 사용한다. 원래 네 인수만 전달해 기본 keyword의 유무까지 맞춘다. time0/241점 반환을 확인한다.

이를 기존 음성의 실제 sealed 인수와 연결하는 **검토자 독립 데이터 비교**가 필요하다. 후보 함수를 호출해 기대 입력을 역산하지 않는다. 원래 source/function/engine와 새 입력 bytes/정규화 타입/순서를 봉인하고 다음 변이만 허용한다.

- READ02 SHA; READ03 unit_record의 time_s; READ04 expected_header[0].
- READ05–07은 raw 전체 교체와 그에 따라 달라지는 bytes/SHA다. 원래 하네스가 행 수도 바꾸므로 “한 cell 변경”이라고 축약하지 말고 실제 before/after raw 및 derived identity를 명시한다.
- READ08 두 번째 time_s의 1→0.
- READ09 times_a에서1 삭제.
- READ10 times_a, times_b, requests_a, requests_b, common_requests **다섯 벡터**에서1 삭제. 이 복수 leaf는 zero-only 비교의 의도된 fixture로 사전 명시한다.
- READ11 첫 profile domain1→3, READ12 마지막 profile 행 삭제.

추가 4개는 새 보조 입력이며 기존 READ01에 숨겨 넣거나 원래130계수 안에 소급 편입하지 않는다. 4개 중 실패하면 그 첫 실패와 뒤 미실행을 보존한다. 승인된 수를 넘는 probe/추가 control/재시험은 이 설계에 포함하지 않는다.

## 재사용 조건과 한계

원래 source/fixture/harness/engine/result/producer의 식별과 중지 이력을 보존하고, 새 하네스의 변경 범위를 실패 입력 및 추가 양성4에 한정해 정적으로 설명한다. 기존 결과의 테스트 당시 하네스를 새 하네스로 덮어쓰지 않는다. 기존 결과는 당시 봉인의 관측이라는 출처를 유지한다.

이 조건에서 READ 대조 보완은 기존 음성11개를 다시 실행할 사유가 아니며, 실패한 PowerShell 사례의 후속 검증은 앞선 28개를 다시 실행할 사유가 아니다. 관련 생산 함수나 fixture 의미가 새로 바뀌면 그 변경이 영향을 주는 기존 결과의 재사용 여부는 다시 판단해야 한다.

현재 원문 증거는 오프라인 합성 fixture 검증이며 raw native adapter, 설치본 COMSOL mapping, 실제 quadrature 근거, 실제 OS/Job/중지 장치 검증으로 확대할 수 없다. 전체/정상 gate INCOMPLETE 및 native_ready=false는 유지된다.
