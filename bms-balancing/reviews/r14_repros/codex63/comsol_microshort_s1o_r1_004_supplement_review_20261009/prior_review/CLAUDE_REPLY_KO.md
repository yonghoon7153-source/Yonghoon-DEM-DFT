# S1O R1 004 검증 종결 회신

R1_004를 읽기 전용으로 검토했습니다. 판정은 **LIMITED_VALIDATION_CLOSED_WITH_DOCUMENTED_SCOPE**입니다. S1O003-N1 하네스 보완과 S1O003-N2 동일 기본 입력 양성 보완을 수용합니다.

- 입력 ZIP 796,501 bytes / SHA `cb85fa123395caf9ea323b0c531144bf30754322ba9b0362f1bbac3e5bc8ff2c`, payload50과 manifest의 집합·크기·SHA·CRC가 일치합니다. 내장 R1_003도 기존 원본과 같습니다.
- 원 127개 재사용 + 원 미완 R115/R113/R114 3개 신규 충족으로 원 130개 범위가 닫혔습니다. 새 READ 양성 4개는 별도입니다. 130개 단일 재시험 또는 134개 신규 PASS라고 기록하지 마세요.
- R113은 파싱 직후 System.Decimal 관측 → 해당 leaf의 명시적 System.Double fixture 변환 → 실제 S1Decision/S1Fields/S1ComparisonNumerics의 DECIMAL_TRANSPORT_PRECISION 거부가 연결됩니다. 원 R1_003 당시 미기록 타입을 소급 확정하지 않습니다. R114는 실제 fields 단계의 COMPARISON_SUMMARY_CONTRADICTION이며, 원 PARENT02 양성 재사용이 결속됩니다.
- READ 양성 4개의 같은 기본 입력과 선언 변이로 기존 READ02–12의 입력 fingerprint 11개가 정확히 재구성됩니다. 기존 음성 재시험 없이 보완 근거를 수용합니다.
- 생산 CODE_MANIFEST `4ce5c08dbde5153027819b5a651e3995ec82417b4429b9bb0f789082b440f5da`와 구성원21개가 유지됩니다. 전후 보존246개 기록 중 전달된183개 파일 바이트는 직접 대조했고,63개 엔진·환경은 제출 관측 기록 범위입니다.

두 기능 세션은 rc0이며 각 기록 후 경계도 예산 안입니다. 포장 반환 전사 eb8612의 전체569.914417초·전달116.799786초는 각각1200/240초 안입니다. 별도 최종614.480초는 현재 사용자 보고 범위이며 당시 원문 요청을 남겼습니다. 원문 없이 도구 wall time을 더하거나 현재 측정으로 보충하지 않습니다. ZIP 밖 영수증·포장 반환은 붙여준 내용 확인과 원파일 바이트 확인을 구별합니다.

**원 R1_003 INCOMPLETE·실패 기록과 비활성 source manifest는 그대로 두고 이 회신을 별도 연결하세요. 검증 반복은 요구하지 않습니다.**

다음은 설치본 t0/CDI·실효 계수·raw 증거 매핑·소유 Job/자원/중단 어댑터 OPEN만을 대상으로 한 좁은 연결 작업 범위 확정입니다. 순수 함수 검증으로 실제 설치본과 OS 어댑터가 확인됐다고 하지 마세요. 고정 소스와 필요한 변경부 검증·현재 관측 수용 후 P0 한 건의 명시 승인을 따로 요청하세요.

이번 회신은 구현 또는 native 실행 GO가 아닙니다. `native_ready=false`, 전체·정상 gate INCOMPLETE, 실효 정책/실제 코어 UNVERIFIED를 유지합니다. COMSOL/JVM/solve/후속 P1–P3·K cohort·장시간 실행은 승인하지 않습니다.
