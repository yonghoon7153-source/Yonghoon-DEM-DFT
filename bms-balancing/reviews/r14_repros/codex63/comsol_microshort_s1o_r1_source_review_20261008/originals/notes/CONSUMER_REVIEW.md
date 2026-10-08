# S1O-R1 consumer 독립 정적 검토

검토 대상: `received/main/candidate/consumer.py.inactive.txt`, `contracts/CHARGE_BALANCE.json`, `SOURCE_CONTRACT_LINKS.json`, `VALIDATION_PLAN_R1.json`의 CHARGE 관련 사례. 비교 기준은 `microshort_s1o_preparation_review_20261007/received`와 당시 N1/N2 정적 반례다. 좌표는 별도 언급이 없으면 R1 `received/main` 아래다.

결론: **N1/N2는 정적 준비 수준에서 종결 가능. 담당 변경 범위에서 새 차단 결함을 확인하지 못했다.** 기능 검증, 실제 native 원자료 결속, COMSOL 설치본 적합성을 확인한 결론은 아니다. 제출 소스, 도구, 함수, harness, 시험, import, COMSOL을 실행하지 않았다. 파일은 텍스트 및 JSON 데이터로만 읽었으며 독립 상수 산술에만 PowerShell의 decimal/BigInteger를 사용했다.

## N1: 전체 수지 격자·끝시각·Li·출처 결속

- `consumer:218–220`은 native 시각, global 표, configured/actual/safe 끝시각, reason, 출처 결속을 필수 keyword 입력으로 받는다. 단순 charge 두 행만으로 새 함수를 호출할 수 없다.
- `consumer:226–235`는 독립 native 시각 벡터의 시작 0, 유한 Decimal, 엄격 증가, 마지막 실제 시각을 검사한다. 정상 종료는 `actual == configured == safe`; 보호중단은 `safe == native[-2] < actual < configured`다.
- `consumer:236–237`은 charge의 전체 순서 벡터 및 global의 전체 순서 키가 native 벡터와 정확히 같은지 검사한다. 마지막 한 행, 중간 한 행, 같은 개수의 다른 시각, 정렬 변경 모두 이 조건에서 실패한다.
- `consumer:238–259`는 정확 단위 사전, 세 출처 identity의 필드/타입/해시 형태, 각 global 행의 시각 및 모든 시각의 LiN/LiP/LiE 일치를 검사한다.
- `analyze:380–390`은 charge provenance의 run/manifest를 binding과, charge/global/native identity를 별도 입력 및 source_evidence와 대조한다. `391–396`은 quadrature 근거의 격자 SHA도 같은 native identity에 결속한다. `397–400`은 위 입력을 실제 charge 함수에 전달한다.
- 이 연결은 `CHARGE_BALANCE:143–163`, `SOURCE_CONTRACT_LINKS:10–15`와 일치한다.

### 기존 0–1초 반례의 실제 분기

global/native는 0–120초 전체이고 charge만 `[0,1]`인 기존 반례를 유지한다. 출처, 초기화, 계수, global 불변량 등 선행 조건을 유효하게 유지하면 `analyze:397`에서 수지 함수에 진입한다. `charge_balance:232–235`의 native 끝시각 검사는 120초로 통과하지만 `236–237`에서 `[0,1] != full_native_times`가 되어 `CHARGE_GRID_BINDING`으로 거부된다. `analyze:408`은 INVALID를 보존하며 `405–406`의 정상 제한 결과 분기에 도달하지 못한다.

charge와 native 벡터를 함께 `[0,1]`로 줄이고 실제 끝을 120으로 남기면 `232`가 거부한다. 실제 끝도 1로 바꾸고 정상 설정 끝을 120으로 유지하면 `analyze:366`의 `NATIVE_END_TIME`이 먼저 거부한다. 서로 다른 실행의 manufactured identity를 모두 일관되게 바꾼 입력의 진위를 이 함수만으로 입증하는 문제는 아래 공개 OPEN에 해당한다.

## N2: 누적 양수인 구간 역행

`consumer:281`의 누적 qN/qP 외에 `284`에서 바로 이전 native 저장 행과의 signed dqN/dqP를 계산한다. `285`는 두 전극을 독립적으로 검사하며 임계값은 기존 `q_abs=2e-4` 그대로이고 비교는 엄격한 `< -q_abs`다. 누적량이 허용되면 `REVERSE_LI_INCREMENT`, 누적량도 실패하면 기존 `REVERSE_LI_TRANSFER`를 선택한다(`292`). `287–299`는 최초 위반의 두 시각, 두 증분, deadband, 위반 전극 및 앞선 records를 오류에 붙이며 `analyze:409–410`에서 결과로 보존된다. `CHARGE_BALANCE:165–176`와 일치한다.

### 기존 누적 양수 반례의 실제 분기

기존 반례는 j=RN=0.25, RP=-0.25, I=A*j이며 qN=qP가 100초에서 25.001, 100.001초에서 25.00025 C/m²다. 독립 스칼라 산술에서 마지막 증분은 `25.00025 - 25.001 = -0.00075`; 100초의 기존 누적 허용치는 `0.0002 + 0.0001*25.001 = 0.0027001`이다. 이전 잔차 0.001은 그 한도 안이고 마지막 누적량도 양수다.

전체 격자 및 global Li를 일관되게 결속하고 선행 검사 통과 자료를 주면 `consumer:284–285`에서 두 증분이 -0.0002보다 작아진다. `292`는 누적량이 양수이므로 `REVERSE_LI_INCREMENT`를 고르고 `300`에서 중단한다. first_violation은 `[100,100.001]`, 위반 전극은 `['N','P']`다. N만 또는 P만 뒤집는 검증안 CHARGE_R110/R111은 같은 분기의 각 전극 독립 확인이다. 그 행 이후 records나 성공 분류를 만들지 않는다.

### 경계와 작은 초기 구간

- 정확 -0.0002는 `285`의 엄격 부등식을 통과하고 `301`에서 RESOLUTION_LIMITED다. -0.000199도 같은 분기다. -0.0002000001은 거부된다. +0.0002는 포함 deadband이며 두 전극 모두 +0.0002를 엄격히 넘어야 RESOLVED_EXPECTED_DIRECTION이다.
- 작은 초기 구간의 RESOLUTION_LIMITED만으로 전체 결과를 영구 미완으로 만들지 않는다. `321–325`는 기존 최종 누적/current sign 및 quadrature 규칙을 유지한다. 이는 계약 `176`의 명시된 분리와 일치한다.
- CHARGE_R112/R113의 pinned r은 각각 50자리 정밀도에서 F*r가 정확 0.0002/0.000199가 되도록 고정되어 있다. 후보 함수와 무관한 정수 곱으로 확인했다. F의 정수 계수는 9648533212(scale 5), r의 정수 계수는 각각 20728539313235459275942014552916273881402482340339, 20624896616669281979562304480151692511995469928637(scale 58)이다. 정확 곱은 각각 `200000000000000000000000000000000000000000000000004328838868`, `199000000000000000000000000000000000000000000000001364392044`(scale 63)이다. 50유효자리 뒤의 나머지는 절반보다 작으므로 선언된 값으로 반올림된다.
- 이 경계 사례는 N:0→r, P:r→0, E=1, j/RN/RP/I=0, bound=0이다. qN=qP는 작은 음수, 총 Li는 보존, 적분 잔차는 한도 안, 최종 sign은 RESOLUTION_LIMITED이므로 INCONCLUSIVE 반환 경로가 존재한다. 이를 초기 모델 적합성 시험으로 확대하지 않는다는 계획 `4951`의 한계도 정확하다.

## 정상·보호중단 양성 경로

정상 120초 전체 격자는 `232–235`의 NORMAL_END 조건을 만족할 수 있고, charge/global/native의 동일 시각·Li 및 출처를 공급하면 새 결속 분기에서 선행 거부되지 않는다. 상수 양의 j/RN/-RP, 동일한 선형 N 손실/P 증가, 일정 E 및 bound=0은 새 증분 검사를 만족하는 해석적 양성 예다. 작은 초기 구간은 허용되며 최종 신호가 충분하면 CONSISTENT가 가능하다. CHARGE01은 전체 `analyze` 반환, charge CONSISTENT, evidence VALID, errors=[]를 요구한다(`1491–1529`).

보호중단의 configured=120, safe=t_minus=90, actual=t_plus=90.1 및 penultimate native=90은 `analyze:368–373`과 `charge_balance:234`를 동시에 만족한다. 전체 charge에는 90.1초가 남고, `compare_policy -> coverage:68–78`의 비교 요청만 90초 이하로 제한된다. 결과의 native_completion은 PROTECTIVE_STOP, limited_result는 INCOMPLETE로 남는다. CHARGE_R109는 단순 label만 확인하지 않고 evidence VALID, errors=[], actual/safe를 함께 요구한다(`3309–3340`). 부모의 실제 수용 여부는 부모 담당 검토 범위다.

## 관련 검증안의 정적 정합성

- CHARGE_R101/R102/R103/R107은 끝·중간·동일 개수 위조·native 격자 변경으로 `CHARGE_GRID_BINDING`; R104는 같은 시각 Li 불일치로 `CHARGE_GLOBAL_LI_MISMATCH`; R105/R106은 analyze의 `CHARGE_SOURCE_BINDING`; R108은 analyze의 `NATIVE_END_TIME`; R115는 `CHARGE_UNIT_BINDING`; R116은 `COMPARISON_WINDOW_OR_REQUEST_BINDING`; R117은 첫 `CHARGE_TIME`에 도달한다. 선행 전제를 모두 유효하게 유지할 때 계획한 첫 사유와 소스 순서가 맞는다.
- 유지된 CHARGE11은 순서 변경의 첫 사유를 새 격자 검사에 맞게 CHARGE_GRID_BINDING으로 갱신했다. 원래 CHARGE05–10/12는 직접 수지 함수 호출이고 원래 목표 전의 결속 조건을 유효하게 만든다고 명시한다. 따라서 analyze의 선행 invariant 검사를 잘못 성공으로 셀 구조가 아니다.
- R110/R111/R114는 global/charge Li의 공동 수정, 전체 불변량·선행 적분 조건, 독립 반올림 산술 및 최초 위반 전극 봉인을 요구한다. 실제 fixture bytes는 아직 없으므로 그 구체적 만족은 미래 봉인 단계에서 확인해야 한다.
- 계획 `4946–4979`는 정상/보호 실제 producer JSON의 부모 전달, 경계 합성 fixture 한계, 사전 봉인 미완 항목 및 선행 오류를 목표 성공으로 세지 않는 규칙을 명시한다. 담당 CHARGE 사례에서 실행 불가능한 기대 분류를 발견하지 못했다.

## 공개 OPEN 및 결론의 한계

1. Raw native/readback adapter 및 installed COMSOL mapping이 없다. 세 identity를 형식·입력 간에 대조하는 준비 코드는 실제 bytes·units·저장 시각을 읽었다는 증거가 아니다. 계약 `149` 및 `SOURCE_CONTRACT_LINKS:17–22`가 이를 공개한다. 이 공개 상태를 N1의 잔여 새 결함으로 재분류하지 않는다.
2. 독립 quadrature bound의 실제 도출/원자료 근거는 OPEN이다. null bound는 INCONCLUSIVE이며 실제 근거 없는 bound를 합법화하는 결론이 아니다.
3. 130개 입력/harness는 계획 단계이며 CHARGE의 정적 기대 경로를 확인했을 뿐 기능 결과는 0건이다. source_loading·PowerShell extraction 전체 및 다른 검증군의 봉인 정합성은 별도 담당 검토에 따른다.
4. 전체/정상 gate는 consumer 초기값 INCOMPLETE로 유지되고 본 검토는 native 실행 승인이나 모델·실험적 타당성 승인이 아니다.

담당 범위 권고: **N1/N2 정정 수용(정적 준비 수준), 추가 consumer 수정 요구 없음.**
