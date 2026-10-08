# S1-O 준비본 정적 검토 — 정책·K·비용·관련 검증안

검토 대상 루트: `outputs/microshort_s1o_preparation_review_20261007/received/`.
아래 경로와 줄 번호는 별도 표시가 없으면 이 루트 기준이다. 받은 코드의 import/실행/함수 호출/시험·COMSOL/JVM/compile/solve는 모두 0회다. 코드와 계약을 텍스트로 읽고 분기를 추적했으며, 반례는 실행 결과가 아니라 정적 추론이다.

## 결론

P0–P3 변형, paired near-zero를 포함한 K, 120s pilot의 후기 cap 한계와 별도 M/N 순서, 비용의 시나리오/승인 상한 구분은 전반적으로 정합하다. 담당 범위에서 확인한 확정적인 소스 불일치는 P0의 저장 정책 로그 한 곳이다. Decimal→double 경계는 실제 유효 결과를 INCOMPLETE로 돌릴 수 있지만 이미 `SOURCE_CONTRACT_LINKS.json:24`에 선언한 fail-closed 한계이므로 숨은 native 승인 결함으로 부풀리지 않는다. 98사례의 구체 fixture 봉인에서 정할 사항은 아래에 별도로 분리했다.

## A. 확정 소스 불일치

### [P2/경미] P0는 all-steps로 설정하면서 tlist 저장이라고 기록한다

- 위치: `candidate/variants/P0.java.inactive.txt:439`.
- 근거: 416행은 `tout=tsteps`; 439행은 `S1_PROPOSED_TIME=...|requested tlist storage|...`; 540행은 실제 `getString("tout")`를 읽는다. `contracts/POLICY_VARIANTS.json:2027`도 P0의 `tout=tsteps`를 요구하고, 2248–2249행은 변형별 식별자와 logger claimed settings를 맞추라고 명시한다.
- 정적 추적: 이 후보의 비활성 차단이 훗날 승인된 코드로 대체된다면 같은 실행 기록에 사람이 읽는 `tlist` 설명과 실제 `tsteps` readback이 공존한다. 현재 실제 실행이 가능하거나 실행되었다는 뜻은 아니다.
- 영향: P0/P1의 핵심 대조 축인 저장정책의 요약 증거가 서로 모순된다. 실제 설정 readback이 따로 있어 solver 정책 자체가 잘못된 것은 아니다.
- 수정 방향: P0 요약 문자열을 `accepted tsteps storage` 등 실제 정책으로 바꾸거나, 하드코딩한 저장정책 설명 대신 설정 readback을 출력하도록 새 변경본에서 고친다. P1–P3의 `tlist`는 유지한다. 현재 받은 파일은 수정하지 않았다.

## B. 실제 경계 결과이나 이미 선언된 한계

### [P2 수용조건] Decimal EXCEEDS 결과가 부모의 double 반올림 때문에 INCOMPLETE가 될 수 있다

- 위치: `candidate/consumer.py.inactive.txt:202`, `candidate/Parent.ps1.inactive.txt:140`–143; 관련 `SOURCE_CONTRACT_LINKS.json:24`, `VALIDATION_PLAN.json:1253`–1263.
- 정적 반례: 다른 축은 모두 정상이고 consumer의 최대 전압차가 문자열 `0.00100000000000000001`일 때 Decimal50은 이 값이 `0.001`보다 크므로 `EXCEEDS_LIMITS`를 반환한다. 예를 들어 현재 `P=4.001,N=0`, 참조 `P=4,N=1e-20`로부터 이 차이가 생길 수 있다. 나머지 분해 항도 동일 전압 항등식을 만족하도록 설정할 수 있다.
- 부모 분기: 위 값과 `0.001`은 binary64에서 같은 값으로 반올림된다. 이 크기에서 인접 double 간격은 약 `2.17e-19`, 반례의 초과량은 `1e-20`이다. 따라서 부모는 `WITHIN_LIMITS_THIS_WINDOW`를 기대하고 143행에서 `COMPARISON_SUMMARY_CONTRADICTION`으로 거부한다. 이는 과학적 수치초과를 과학적 결과로 보존하지 못하는 경계다.
- 범위 해석: `SOURCE_CONTRACT_LINKS.json:24`가 이미 conversion을 조사하고 contradictions를 reject한다고 명시하므로, 이를 몰래 false PASS하는 버그로 세지 않는다. 현재 동작은 보수적 거부다. 선언한 정책을 유지하려면 이 경우를 알려진 정밀도 한계로 보고하고, PARENT02의 일반 numerical-exceedance 기대값과 경계 입력 기대값을 봉인 때 구분해야 한다. 수치초과를 항상 별도 결과로 보존하려면 부모 비교를 Decimal 판정과 같은 정밀도로 맞추는 별도 수정이 필요하다.
- 검증안 연결: POLICY02/03과 PARENT02가 있지만, 현재 문구만으로는 정확히 같은 경계를 Python→JSON→PowerShell로 통과시키는지 알 수 없다. 98사례를 지금 실행하거나 임의로 늘리지 않았으며 구체 fixture/기대 이유의 봉인 조건으로 전달한다.

## C. 98사례 봉인 때 확정할 조건 — 지금 코드 오류로 세지 않음

### PARENT03의 보호중단은 safe-prefix 요청 수를 써야 목표 분기에 도달한다

- 근거: consumer 297–300행은 safe end를 보호중단 `t_minus`에 묶고, coverage 70–72행은 그 시각까지의 요청만 고른다. Parent 118행은 `coverage.common_requested_count == Expected.required_count`를 요구한다.
- 예: 정상 끝시각120s, `t_minus=115s`이면 sparse prefix는254개다. `Expected.required_count=255`를 그대로 두면 부모는 `COMPARISON_COVERAGE`에서 먼저 거부하여 계획한 `PROTECTIVE_STOP_INCOMPLETE`에 도달하지 못한다.
- 그러나 부모 코드가255를 하드코딩한 것은 아니다. expected count를 검증된 safe prefix254로 봉인하면 목표 경로에 도달할 수 있다. 따라서 확정적인 보호중단 코드 버그가 아니라 `VALIDATION_PLAN.json:1267`–1278의 fixture 정의 요구다. 실행 후 임의로 expected count를 바꾸지 않도록 정상 계획 끝시각/guard safe end/기대 prefix를 함께 봉인해야 한다.

### PAIRED04는 D만 문턱과 같다는 설명으로 기대값을 유일하게 정하지 못한다

- 근거: `VALIDATION_PLAN.json:965`는 `D equalspositive threshold`만으로 `INCONCLUSIVE`를 기대한다. consumer 280–282행은 D/S/E를 함께 판단한다.
- 정적 예: `D=.001,S=.001,E_D=E_S=0`이면 `NOT_DISTINGUISHABLE_WITHIN_T`가 올바른 코드 결과다. 반면 `D=.001,S=.002,E_D=E_S=0`이면 `INCONCLUSIVE`다. 두 경우 모두 D가 양의 threshold와 같다.
- 조치: 봉인 fixture에 D/S/E_D/E_S 네 값을 모두 명시하면 해결된다. 98사례 중 한 사례를 구체화하는 문제이며 사례 수를 반드시 늘려야 한다는 의미가 아니다. 수치 문턱/분류식을 바꿀 필요도 없다.

### own request coverage는 미래 raw adapter의 실제 결속 증거가 필요하다

- 코드 관찰: consumer 299행은 common vector를 binding과 비교하지만 313행에 주는 `requests_current/requests_reference`는 그 함수 안에서 별도 binding과 대조하지 않는다. coverage 70–74행은 전달받은 목록을 그대로 요구 집합으로 삼는다.
- 제한된 반례: P1의 자체1337개 요청 중 sparse255개만 남기고 `requests_current`도 그255개로 줄이면 coverage 자체는 PASS할 수 있다. 부모는 공통255개를 확인하므로 자체1337개가 누락됐음을 추가로 알지 못한다. 이는 fixed 1337 목록이 전달된 정상 입력에서는 일어나지 않으며, 목록을 줄이지 않고 데이터만 누락하면 `REQUIRED_TIME_MISSING`으로 올바르게 거부한다.
- 과장 방지: `SOURCE_CONTRACT_LINKS.json:11`은 selected variant의 등록 요청을 전달해야 한다고 정의했고, 13행의 immutable raw adapter는 명시 OPEN이다. 따라서 이 반례를 현재 adapter가 이미 잘못 구현되었다는 finding으로 세지 않는다. 후속 연결 구현의 수용조건은 variant/source/settings에 묶인 자체 요청 목록을 생성·봉인하고 caller의 임의 배열로 줄일 수 없음을 증명하는 것이다. 현재 준비 범위에 native adapter 완성을 강제하지 않는다.

## D. 정합성이 확인된 항목

- P0/P1 dense0–120은1337개, P2/P3 sparse0–120은255개다. sparse는 `0–5s187 + 5.5–30s50 + 35–120s18`로255개이며 공통 비교격자로 쓰는 것이 맞다. 241개는 전극별 profile 좌표 수다.
- P0→P1은 storage, P1→P2는 request vector, P2→P3는 cap 변경이다. 모든 변형의120s/highσ1.7e-6/fresh 조건은 일치한다. 제공 diff는 S0 대비지만, 읽은 소스와 diff에서 인접한 변형의 수치 정책 차이는 이 정의와 일치한다. 비활성 진입 차단은 유지된다.
- K는 baseline4와4개 축×4σ=16의 고유20회이고 P4까지24회다. near-zero는 축 내에서 공유하고 다른 축으로 대체하지 않는다. P3_120을3600s baseline으로 재사용하지 않는다고 명시했다.
- 후기 cap의 Z/H baseline·half-cap 네 실행은 기존 M4/N16에 포함되며 숨은 P4/P5 추가가 아니다. K 고정 후 M/N 실행 순서이며2700–3600s 창을 포함한다. cap이 비활성으로 작용한 경우 blanket qualification을 OPEN으로 남긴다.
- `paired_classification`의 D 부호와 S의 시간 단위는 맞다. S 계산의 `×4`는900초 차이를 V/h로 바꾸는 값이다. E_D/E_S는 각 축의 matching near-zero/finite 쌍을 사용한다.
- COST_MODEL은120s측정을 후기/다른σ/격자 비용 보증으로 승격하지 않는다. nested phase 시간의 중복 합산을 금지하고 RAM/commit 미측정을 UNKNOWN으로 유지한다. 명목24×9000s=216000s=60h는 미승인 상한 산술임을 표시한다.
- 검증안 사례 수는 AUTH15+READ12+INIT12+POLICY8+CHARGE12+PAIRED7+RESOURCE16=Python82, PARENT16을 합해98개·8군으로 맞는다. 상한600+300+180+300+120=1500s도 맞다. 사례수가 많다는 사실 자체를 함수정확성 검증 완료로 읽지 않았다.

## E. 중복 방지 메모

초기 pair 검사 함수가 `analyze`에 호출되지 않는다는 이유만으로 새 finding을 만들지 않았다. `SOURCE_CONTRACT_LINKS.json:8`과12는 near-zero/finite cohort 조립에서 그 검사를 요구하고 해당 조립기가 OPEN이라고 명시한다. data charge grid와 global/profile end 결속 및 구간 역방향 Li 검사는 물리 담당 검토가 별도로 다룬다.
