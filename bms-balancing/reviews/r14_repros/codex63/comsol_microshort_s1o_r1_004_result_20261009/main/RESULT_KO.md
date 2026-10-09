# S1O-R1 R1_004 잔여 검증 결과 — 2026-10-09

**새 7개 입력 한정 검증 PASS, 독립 수신 검토 대기입니다.** 실제 COMSOL 또는 microshort 계산은 하지 않았습니다.

집계는 원 127개 재사용 + 원 미완 PARENT_R115/R113/R114 3개 신규 충족이며, Python 보조 양성 4개는 별도입니다. 130개를 한 번에 재시험했다고 표현하지 않습니다. R1_003의 INCOMPLETE·첫 실패와 기존 원본은 그대로입니다.

Python READ_CTRL_CSV/TIME/COVERAGE/PROFILE은 각각 실제 생산 함수에 한 번 진입하여 정확한 정상 반환을 확인했습니다. 동일 기본 입력에서 선언한 변이만 적용한 데이터가 기존 READ02–12의 canonical 입력 해시와 모두 같았습니다. READ05–07은 raw와 identity의 복수 변이, READ10은 다섯 벡터의1 제거로 명시했습니다. 기존 음성함수는 재시험하지 않았습니다.

PowerShell 순서는 R115 → R113 → R114입니다. R115는 기존 POLICY02 문자열값의 정상 판정 및 WITHIN_LIMITS_THIS_WINDOW, R113은 DECIMAL_TRANSPORT_PRECISION/comparison_numerics, R114는 COMPARISON_SUMMARY_CONTRADICTION/fields를 실제 S1Decision·하위 함수에서 확인했습니다. 임의 조기 오류를 PASS로 세지 않았습니다.

R113 JSON 파서의 실제 형식은 **System.Decimal**, 값은 0.001였습니다. 유한한0.001인지 확인한 뒤 fixture의 해당 leaf만 **System.Double**로 명시 변환했습니다. Double64비트는 3F50624DD2F1A9FC이며 나머지 leaf는 동일합니다. 파서가 Double을 만들었다고 주장하지 않습니다. 실제 원문 producer를 재생성하지 않았고 원 JSON/context10개를 동일 바이트로 연결했습니다. R114 양성 대조 PARENT02는 같은 소스·엔진·POLICY03·원 반환/도달 기록으로 재사용했으며 새로 호출하지 않았습니다.

사전 봉인 381.890301/600초, Python 0.432908/120초·rc0, PS5.1 9.169032/180초·rc0입니다. 최종 전달 시간은 ZIP 밖 영수증과 마지막 포장 도구 반환을 함께 확인하세요. 내부 snapshot과 tool wall time은 합산하지 않습니다.

생산 소스 변경0, 재시도0입니다. 원 R1_003 ZIP153payload 대조와 원 봉인123개를 포함한 현재 봉인 246개 파일의 전후 식별이 일치합니다. 서로 다른 집합을 합쳐 고유 원본 수로 주장하지 않습니다. 기존 결과 ZIP은 reference에 원바이트로 포함했습니다.

native_ready=false, 전체/정상 gate INCOMPLETE, 설치본t0·계수·native/raw/OS 어댑터 OPEN을 유지합니다. 이번 결과는 실제 S1-P 또는 후속 COMSOL 실행 승인이 아닙니다. 제출 후 중지합니다.
