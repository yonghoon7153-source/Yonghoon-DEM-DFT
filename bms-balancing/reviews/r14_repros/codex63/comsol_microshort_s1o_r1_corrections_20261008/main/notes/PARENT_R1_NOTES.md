# R1 부모 소비 변경 — 정적 작성 기록

대상은 `candidate/Parent.ps1.inactive.txt`이다. 후보 함수 호출·기능 시험은 하지 않았다. 텍스트 편집, 소스 구간 바이트 비교 및 SHA 계산만 수행했다. 설치본/native/raw 어댑터는 계속 OPEN이다.

## N3: 요청 목록과 검증된 종료 경계

- `S1NativeAxis`(170행)는 실제 native 저장 시각 배열과 식별을 요구한다. 정상 종료는 exact final=end이다. 보호중단은 exact `t_minus < t_plus < configured_end`, `t_plus=final`, 마지막 두 실제 저장 시각이 `t_minus/t_plus`임을 요구한다. 기존 native reason/operator/unit/domain, no-post-integration 및 typed rc 조건은 유지한다.
- `Expected.common_requested_times_s`는 봉인 계약의 전체 요청 목록이다. `Expected.required_count`는 그 전체 목록 개수이며 결과에서 복사하지 않는다. `S1Coverage`(69행)는 이를 검증된 safe end 이하로 잘라 기대 비교 목록을 독립 유도한다.
- 비교 목록은 유한·0부터 증가·중복 없음·safe end 이내이고 기대 목록과 원소별 동일해야 한다. 정확 시각값은 숫자로 해석하여 비교하므로 `1.0`과 `1`은 같은 시각이다. 보간/근접 대체는 없다.
- `full_intersection`은 별도 전체 시간 교집합이다. 실제 native 종료까지의 상태를 보존하며 보호중단 `t_plus`를 포함할 수 있다. 비교 목록은 이 교집합의 부분집합, 교집합은 native 실제 저장 격자의 부분집합이어야 한다. `full_intersection`까지 safe end로 잘라 버리지 않는다.
- PARENT03은 전체 고정 목록 255개와 required_count=255를 유지하되, safe end=90에서는 별도로 유도한 prefix 249개를 기대한다. 실제 종료 90.1초의 charge/native 상태는 보존한다. 목표는 `PROTECTIVE_STOP_INCOMPLETE`이며 앞단 coverage 거부를 통과로 세지 않는다.

## N1/N2 부모 연결

`S1ChargeFields`(108행)는 consumer의 `S1O_CHARGE_BUDGET_R1`을 소비한다. `grid_binding`의 full times/count/start/actual/configured/safe end, native reason, 단위·global Li exact-match 상태와 세 원자료 식별을 대조한다. 각 식별은 결과의 `source_evidence`에 정확히 하나 있어야 하며 native-grid 식별은 native 기록과도 같다. 각 charge record의 시각을 full native grid와 원소별 대조한다.

`interval_direction`의 고정 deadband 0.0002 C/m², 체크 구간 수, first_violation=null 및 상태를 요구한다. t0는 구간 없음이며 이후 각 구간 시작점, signed Δq_N/Δq_P와 방향 표식이 일치해야 한다. 부모에 전체 CSV 분석기나 적분기를 새로 만들지 않았다. 실제 생산자 계산·원시 입력 결속은 consumer 및 향후 별도 raw 어댑터의 책임이다.

## Decimal 전송과 비교 경계

새 `S1ExactDecimal`(27행), `S1ExactCompare`(51행)는 문자열의 부호·유효 숫자·10진 자릿수 위치로 임의 정밀도 유한 십진수를 비교한다. 문자열을 double/decimal로 반올림하지 않는다. 문자열 또는 정수형만 허용하고 이미 float/double/CLR decimal로 변환된 입력은 `DECIMAL_TRANSPORT_PRECISION`으로 INCOMPLETE 처리한다. ASCII 십진 문법·정수 범위 exponent만 허용한다. 이 제한은 수치 허용치 변경이 아닌 전송 schema이며 미래 검증에 양성/음성 경계를 포함한다.

`S1ComparisonNumerics`(156행)는 기존 ΔV=0.001 V, 표면 Δx=0.0001, Li 상대=0.000001의 세 비교 문턱을 그대로 exact 비교한다. 정확 경계는 허용하고 엄격히 초과하면 EXCEEDS_LIMITS이며, 요약 문자열과 다르면 `COMPARISON_SUMMARY_CONTRADICTION`이다. 예를 들어 문자열 `0.00100000000000000000001`이 double에서 0.001로 반올림돼도 WITHIN으로 승격하지 않는다. 예산·POST_WRITE의 기존 double 계산은 변경하지 않았다.

## 검증안 이유 연결

| 대상 변이 | 기대 최초 이유 / 도달 함수 |
|---|---|
| 비교 목록 중복·비증가·safe 밖 | COMPARISON_TIME_ORDER_OR_RANGE / S1Coverage |
| 같은 길이지만 다른 시각 | COMPARISON_TIME_CONTENT / S1Coverage |
| NaN·Infinity 또는 잘못된 문자 | DECIMAL_TRANSPORT_FORMAT / 정확 비교 호출 함수 |
| 미리 binary double로 변환된 값 | DECIMAL_TRANSPORT_PRECISION / 정확 비교 호출 함수 |
| 교집합에서 비교 시각 제거 | COMPARISON_NOT_INTERSECTION_SUBSET / S1Coverage |
| 교집합에 native에 없는 시각 삽입 | INTERSECTION_NOT_NATIVE_SUBSET / S1Coverage |
| charge count/단위/global 결속 상태 결손 | CHARGE_GRID_SCHEMA / S1ChargeFields |
| charge record 시각 또는 실제 끝 변조 | CHARGE_RECORD_TIME_BINDING 또는 CHARGE_ENDPOINT_BINDING / S1ChargeFields |
| 등록되지 않은 charge/global 식별 | CHARGE_SOURCE_NOT_REGISTERED / S1ChargeFields |
| signed Δq가 -deadband보다 작음 | CHARGE_INTERVAL_DIRECTION / S1ChargeFields |
| Δq와 interval_sign 요약 모순 | CHARGE_INTERVAL_SIGN_CONTRADICTION / S1ChargeFields |
| exact 초과인데 WITHIN 요약 | COMPARISON_SUMMARY_CONTRADICTION / S1Fields |

각 반례는 완전 양성 Python 결과와 native/Expected를 먼저 고정한 뒤 해당 항목만 변이해야 한다. 실제 Python 출력의 JSON은 decimal string을 유지하여 PowerShell이 직접 소비한다. PS 판정을 다른 언어의 모사 함수로 대신하지 않는다. 이 기록은 실행된 시험 결과가 아니다.

## 불변 범위

S1Has, S1Struct, S1Number, S1Sha, S1Failure, S1FinalReturn의 함수 시작부터 다음 함수/최상위 throw 전까지 raw UTF-8 span이 원본과 정확히 같다. 구간 SHA와 추출 규칙은 `PARENT_R1_NOTES.json`에 있다. 정책·예산·입력·소유 Job·native 실행 연결이나 새 엔트리포인트는 추가하지 않았다. 파일 마지막의 비활성 throw도 유지한다.
