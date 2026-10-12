# Claude 전달용 — S1 OPEN-R1 정적 재검토

N1·N2 코드 정정은 정적 검토 범위에서 수용합니다. 독립 frozen clock context/scalar anchor 결속, context 기준 elapsed 계산, counter의 dict→키→정확 정수 타입→membership/query 순서를 확인했습니다. N3의 앞선 C04/C07/Java 도달 경로 정정도 확인했습니다. 기능 PASS나 native 실행 승인은 아닙니다.

수신 ZIP은 4,011,062 bytes / SHA256 `c9cf85b30f48fce0a8e747a8428b74b22a2d4c101498e2c0306720ed571fee0b`이며 117 payload·14개 CODE_MANIFEST 구성원·86개 함수/예외 span이 일치합니다. 기존 원 준비본 구성원과의 바이트 대조도 일치하고, 기존 11개 중 변경은 resource source·그 diff·검증안 세 개입니다.

판정: **STATIC_CORRECTIONS_ACCEPTED_WITH_PLAN_METADATA_CONDITIONS**. 생산 코드를 다시 고치거나 사례 수를 늘릴 필요는 없습니다. 검증안만 다음과 같이 좁게 정리해 주세요.

1. `case_order`의 “C01 through C09 in listed order”를 실제 엔진/양성 의존 순서와 일치시킵니다. Python 1세션에서 C01→C02→C03→C04→C05-01/02/03/07/04/05/06→C06→C07→C09, 이후 javac 1회와 Java helper 1세션으로 C08-01~06입니다. 각 군의 나머지는 기존 ID 순서입니다. 93개·Python87/Java6·기존 호출 횟수·예산은 유지합니다. 첫 예상 밖 실패 뒤에는 남은 모든 엔진과 ID를 실행하지 않습니다.
2. C03-04/05의 positive_control을 normal C03-01이 아니라 기존 protective 양성 C03-02로 연결합니다. C03-02는 해당 분기의 양성, C03-03은 기존 normal 양성 C03-01을 유지합니다. 기대값과 입력을 바꾸는 요청이 아닙니다.

이 내용을 정정본 또는 우선순위가 명시된 봉인 부속서로 남기고 원 계획 SHA `6702a6be556f0f5b4512dd221c08f77d39111606f1d9f97511dd796f2d3d20c9`와 연결하면 됩니다. 코드 바이트는 그대로 보존합니다. 새 문서/manifest의 SHA는 실제 바이트에서 산출하고, 옛 봉인본은 그대로 둡니다. 이 두 메타데이터 정정만을 이유로 추가 생산 코드 수정·추가 시험 사례·전체 130사례 반복을 요구하지 않습니다.

그다음 사용자가 **9군93사례 변경부 한정 검증**을 별도로 승인하는 순서입니다. 새 harness/fixture/실제 엔진/명령 봉인·첫 오류 중지·원본 보존을 승인 범위에 명시하고, 제안 1,350초와 세션 수를 자동 확대하지 마세요. 이번 회신 자체는 하네스 구현이나 검증 실행을 승인하지 않습니다.

마지막 제출 snapshot 875.5703937초 / 2,400초, 전달102.9739274초 / 300초는 제공된 후속 전사 범위에서 수용합니다. ZIP 밖 원파일을 직접 받은 것처럼 말하지 않으며, 도구 wall time이나 전사 이후 시간을 더하지 않습니다. 제출자의 준비 도구 오류 두 건과 과거 실패 기록을 유지합니다.

네 OPEN(installed t0 / effective coefficient mapping / raw native evidence adapter / OS resource·ownership·stop adapters), native_ready/approved/usable=false, 전체·정상 gate INCOMPLETE, 실효 정책·실제 코어 UNVERIFIED를 유지합니다. 검증 통과가 설치본 OPEN 종결이나 COMSOL/P0 실행 승인으로 바뀌지는 않습니다. 기존 저장 결과와 microshort 효과의 새 결과도 구분합니다.
