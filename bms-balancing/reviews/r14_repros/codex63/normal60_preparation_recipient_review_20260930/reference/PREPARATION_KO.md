# 정상조건 fresh 0→60초 후보 준비

상태: **오프라인 후보 준비 완료, 변경부 기능 검증 미실행, native 실행 미승인.**

30초 독립 수용을 별도 ACCEPTANCE_NORMAL30.json에 기록했다. 원래 상태·ZIP·승인·영수증은 고치지 않았다. 수신 검토 ZIP 38,757 bytes / SHA `3b1f58594a6968bda4c55efc3fb2119dfe914c5c5f549933f4fd573df2683140`의 정확 집합·크기/SHA·CRC·경로·링크를 검사했다. 받은 검산기 및 후보 함수를 실행/import하지 않았다.

## 고정 후보와 변경

- 위치: `outputs/normal60_offline_preparation_20260930/`, run_id `normal60_candidate_001`.
- CODE_MANIFEST SHA `82e556243b29b10ae65b95dcdff7f854734b6f1cfffc1881327cab1939ebe5c8`.
- 이전 30초 manifest `6b9ae2a75a2035d0cc80359f5d83cc3ca5dc5aa744b68255d219ce8a55feb603`.
- 모든 후보 승인 플래그는 approved=false/usable=false. 실제 future_run_001/future_parent_001/future_authorizations는 만들지 않았다.

| 구분 | 실제 준비 내용 | 불변/검증 경계 |
|---|---|---|
| Java | Normal60Candidate 명칭·설명·완료 표식, checkShape 상한60, tlist737 | 허용 literal을 역치환하면 원 Java 전체 바이트와 동일. runAll 정적 호출1/loadCopy0. 모델·물성·초기화·출력 API 본문 불변 |
| 요청시간 | 기존0–30초437개를 정확한 prefix로 보존,30.1–60초300개 추가 | 유일·증가·마지막60을 데이터 검사. 실제 저장 개수는 고정하지 않음 |
| consumer | 정상60/보호중단·시간상한, 주 비교0–30, B0200–5 별도 비교, 후기30–60 | 비교 허용치·Li·단위·좌표·표면/OCP/guard 본문 유지. 새 두 기준 소비 경로는 미시험 |
| entry | 목적/클래스/모듈명/결과명/native60 승인 필드만 치환 | literal 역치환 시 전체 원문 동일. baseline_files에12개를 넣어 기존 보존 루프 재사용 |
| 부모 | 정상60/보호중단,737/437/187 시간 수, B020 별도 비교 필수 소비 | BSave/BInvoke 바이트 동일. 마지막 POST_WRITE 예산 판정 본문 동일 |
| 실행 연결 | 새 ROOT/run/승인·release·클래스 경로와 새 manifest | 사용자 일반 PS5.1 NoProfile/같은 Python fresh 두 입력·기존 C2/Job 유지. cwd는 승인된 B020 src 그대로 |

physical300(120/60/120), particle320/320,0.1C,sigma1e−20, threshold0, 기존 세 guard/OCP 외삽 금지/초기step/rtol/cap/strict/all-stored,241좌표·단위·수치 한도는 유지했다. solver/native 호환성 또는 기능 PASS를 정적 대조만으로 선언하지 않는다.

## 두 기준의 실제 연결

기준 CSV는 복제하지 않고 현재 원자료 경로·크기·SHA를 CONTRACT와 BASELINE_IDENTITIES에 고정했다. 30초6개와 B0206개, 합계12개를 기존 entry 보존 루프가 확인하도록 했다. B020 키만 `B020_` prefix를 써서 원본 경로를 구분한다.

1. `numeric.coverage` 및 기존 maximum_voltage_delta_V/maximum_surface_delta: 수용된30초 결과와 0–min(30,안전 prefix 끝)의 정확 공통 시각 비교. 정상60이면 기준 요청437개를 요구한다.
2. `numeric.b020_comparison`: 원 B020과 0–min(5,안전 prefix 끝)의 직접 전압/표면 비교. 정상60이면 기존187개 요청을 요구한다. 주 비교 PASS만으로 이 비교를 생략하지 않는다.
3. 두 coverage 모두 실제 전체 교집합과 비교 부분집합, 요청 누락·strict 누락·비공통 시각을 분리한다. 빈집합/t0만의 비교는 거부한다. 보간/최근접 대체 없다.
4. `numeric.electrolyte_comparison_observation`:30초 기준과 정확 공통 시각의 전체/domain별 최소농도 최대 절대차를 관측값으로 출력한다. 허용치는 null이며 새로운 PASS 기준이 아니다.
5. `numeric.late_interval`:30초 초과~60초의 저장 상태를 따로 기술한다. 기준 해와의 동등성/장시간 수렴 판정이 아니다.

초기Li 각항 절대차≤1e−9 mol/m², 총Li 상대변화≤1e−6, ΔV≤1mV, 표면Δx≤1e−4, 전압 항등식≤1e−8V를 유지한다. 정상 완료는 마지막60초·필수 출력·두 기준 비교·보존·정리·정책·시간·부모 반환 모두 충족해야 한다. 보호식 관측은 diagnostic에 남기며 수치 오류가 동반되면 limited_result는 INCOMPLETE다. 보호중단은 정상60초 완료가 아니다.

## 실행과 검증 경계

이번에는 소스·JSON·해시·텍스트 diff만 확인했다. 후보 import/AST 실행기/컴파일/JVM/COMSOL/시험/입력/정책 변경은0회다. STATIC_AUDIT의66개는 정적 대조 수이며 기능 시험 수가 아니다.

다음 제안은 변경부12군46사례의 한정 검증이다. Python 실제 consumer→entry, Java 실제 checkShape 추출 helper, PS5.1 실제 GDecision을 대상으로 한다. 이전111개/C2/Job/1198/30초 시험을 반복하지 않는다. 세부 목록과 엔진/예산은 LIMITED_VALIDATION_PLAN.json과 VALIDATION_REQUEST_KO.md에 있다. 현재 harness나 fixture를 실행하지 않았고 승인 전 시험 엔진도 시작하지 않는다.

수신 검토의 사전실행 참조6개 미포함 한계는 유지한다. 그 때문에 새 측정이나 정책 probe를 하지 않았다. 이번 새 후보는 독립 수용·변경부 검증 결과·현행 경로/정책·새 사용자 단발 승인에 결속되어야 한다.

원 overall/normal gate INCOMPLETE·실효정책 UNVERIFIED·전체 수렴 미완·TIME_CAPS 미확인·기존 failed/pending/원복/recipient=null을 유지한다.60초/120초/12시간·CDC·휴지·finite sigma·sweep·후보C 실행 권한은 생성하지 않았다.
