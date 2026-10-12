# 추가부 한정 검증 제안 — 이번에는 실행하지 않음

**8군·50개 고유 사례: Python 44, COMSOL 없는 Java helper 6.** 세부 ID·입력 변이·양성 대조·기대 이유·도달 함수는 `LIMITED_VALIDATION_PLAN.json`에 있다. 새 source hash도 같은 계획에 들어 있다. 이 숫자는 원 R1 130사례 재실행 수가 아니다.

| 군 | 범위 | 사례 수 |
|---|---|---:|
| C01 | raw bytes/header/단위/Decimal 읽기 | 7 |
| C02 | 전체 저장 grid와 charge 전류/Li 투영 | 6 |
| C03 | 정상 요청/보호 prefix/누락 거부 | 5 |
| C04 | 적분오차 raw 및 검토된 방법 결속, 미확인 유지 | 5 |
| C05 | installed proof 기본 차단, mapping byte 결속, 실제 consumer seam | 7 |
| C06 | PID+생성시각·RSS·Job commit·디스크·시각 투영 | 8 |
| C07 | 실제 control 자원/중단 함수 연결, force와 graceful 분리 | 6 |
| C08 | 정확 Java helper 추출, typed property/recursive table/stored t0/오류 전달 | 6 |

Python 한 세션≤180초 → helper compile 한 번≤90초 → helper JVM 한 세션≤60초를 제안한다. 새 원점의 하네스/봉인600 + 시험330 + 보존/전달300 + 미완 정리120 = 전체 **1,350초**다. 현재 준비 예산과 별개이며 미승인이다. PS 부모를 수정하거나 새 PS projection을 만들지 않았으므로 이번 추가부 검증에서 PS 세션을 제안하지 않는다. 향후 실제 native→Parent adapter를 구현하면 그 변경부만 별도 검증해야 한다.

실행 전에 새 fixture 폴더 부재, source/원 함수/추출 바이트/하네스/엔진/입력·기대 이유/argv/cwd를 봉인한다. 현재 제안 fixture 폴더는 만들지 않았다. Java 엔진은 이전 COMMANDS의 경로를 참고하여 현재 파일 바이트만 읽었다. 버전 명령·JVM·컴파일을 실행하지 않았다.

실제 새 함수를 검사하고 원 consumer/control 함수에 연결한다. 비슷한 모사 함수 통과로 대체하지 않는다. C05의 semantic verifier와 C06의 OS snapshot은 명시적인 inert fixture여야 하며 설치 관측으로 승격하지 않는다. native/입력/Job/프로세스 진입점은 대상 로드 전에 차단한다. Java는 정확 helper+필요한 기존 pure dependency와 최소 stub만, COMSOL jar/전체 모델 컴파일은 제외한다.

기대한 거부 이유와 도달 함수가 모두 맞아야 한다. 임의 예외나 앞단 해시 실패를 다른 목표의 PASS로 세지 않는다. 첫 예상 밖 실패나 각 단계/전체 상한 초과에서 뒤 엔진을 멈추고 최초 원문·rc·미실행 ID를 보존한다. 자동 수정/재시험/부분 probe/다른 엔진·권한 fallback은 없다.

통과해도 installed t0/계수/raw 종료 의미·실제 OS counter/commit cap/cooperative stop·native 출판 준비는 증명되지 않는다. 결과를 독립 수용한 뒤 필요한 별도 관측 범위를 정한다. P0/native 승인은 포함하지 않는다.
