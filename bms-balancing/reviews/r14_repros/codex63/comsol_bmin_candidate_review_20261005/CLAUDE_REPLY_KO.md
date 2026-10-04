# B-min 후보 준비 검토 회신

고정 커밋 74502af93db0f01bb3ae99eca981cc215300b8bf, manifest 3722a51fb1caeddd72fca3751f2ed78ed3e05d5f1938fa452503b3fa5c421a03을 검토했다.

**판정: 국소 정정 필요 — P2 2건.** Java/entry를 포함한 네 소스의 선언 변경 역치환은 NORMAL480 원본 바이트와 전부 일치했다. 기준 생산 8파일+runtime CSV 1개, 기준 CSV 9개, 요청 1,637·주 비교 301·좌표·한도·22개 runtime 설정 결속과 88개 저장소 보존을 확인했다. §46-7의 고정 보존 기준도 수용한다.

1. BMIN-N1: 부모 GFields(134–140행)가 구성 증거 실패 또는 분석/전달 예산 초과 시 확인된 정상 native 종료도 NOT_ESTABLISHED로 바꾼다. native 종료 근거의 검증을 비교/증거/후속 예산 판정과 분리하라. 정상 종료가 독립 확인되면 그 사실은 남기고 evidence_validity=INVALID, mesh_comparison=INCONCLUSIVE로 하라. consumer 문자열의 무검증 복사는 금지한다. PS01-09 기대값과 정상 종료+분석/최종 전달 예산 초과, native 근거 자체 실패의 대조를 고정하라.
2. BMIN-N2: consumer mesh_evidence(313–320행)는 DOF 문구가 없어도 PASS이고 초기화 DOF만 남아도 마지막 값을 사용한다. 단일 Time-Dependent Solver 구간의 실제 DOF 관측을 요구하라. 누락/구간 밖 값/모호함은 I-3 미완이다. 예상 156,925+12와 다른 유효 관측은 값과 차이를 남기되 차이만으로 실패시키지 않는다. PY03-05에 누락·초기화만·모호함의 반례를 보완하라.

비차단 C1: PS01-03/04는 짧은 소수의 한도 및 라벨 검사이지 decimal 자릿수 반올림 경계 시험은 아니다. PREPARATION 102–103행·요청문 자체 신고 d를 실제 범위로 좁히거나 명시적 사례를 추가하라.

Q1 허용 diff, Q4 제거 기능은 수용한다. Q2는 N1, Q3는 N2가 잔여다. Q5의 기준 경로는 원 NORMAL480 DIAGNOSTIC_RESULT의 tables_manifest와 path/bytes/SHA 모두 동일하며, Nord=1/CubicRoot도 원시 batch_console에서 직접 확인했다. 현 실행 PC의 현재 파일 존재까지 관측한 것은 아니다. native 전 identity 확인은 유지한다.

Q6의 9군 41사례·1,470초 합계는 맞지만 위 보완 뒤 새 사례/기대값/예산/manifest를 사전 고정해야 한다. native 10,500초·15GiB는 충분성 실측이 아닌 제안으로 유지한다.

수정은 사용자 별도 승인 뒤 위 국소 범위만 수행한다. 최소 diff·새 봉인·변경표·정적 대조·보완 검증안 제출 뒤 멈춘다. 이번 회신은 변경부 검증 또는 native 승인도, 수정 실행 지시를 대신하는 사용자 승인도 아니다. 기존 전체 suite·NORMAL480·rtol30을 반복하지 않는다.

받은 후보/도구 import·컴파일·실행, COMSOL/JVM 호출은 0회다. 검토자 자체 정적 도구만 사용했다. 전체/정상 gate INCOMPLETE와 960초·유한 σ·다른 공간 축 미승인은 그대로다.
