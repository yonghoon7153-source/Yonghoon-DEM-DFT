# 다음 한 건 — 변경부 한정 검증 승인 초안

**현재 미승인·미실행이다.** 검토 대상은 `CODE_MANIFEST.json`의 `28dd6da5cc76885263c17b2671548a00692064807e02e77ceb6f3edbdd946fa5`와 `LIMITED_VALIDATION_PLAN.json`의 실제 변경 함수·사례 목록이다. 이전1198 전체78개·67/389개 시험을 다시 돌리는 계획이 아니다.

> 정상30초 후보의 변경부만 별도 test 폴더에서 한정 검증하는1건을 승인합니다. 시험 전에 source/harness/engine/argv/cwd/하위사례와 기대이유를 봉인합니다. 실제 consumer→entry와 PowerShell GDecision/최종기록 분기를 사용하고, Java는 변경된 checkShape helper만 추출한 COMSOL 무관 stub을 사용합니다. 기존 실행 경로의 native/console/Job 진입점은 import 전에 inert adapter로 차단합니다.
>
> 격리 Python1세션120초, Java helper compile1시도90초/JVM1세션60초, Windows PowerShell5.1 fixture1세션90초만 허용합니다. 전체후보 COMSOL컴파일/모델로드/solve·실제입력·토큰·Job·prefs/보안변경·실제승인/runtime 생성은 허용하지 않습니다. PS의 새 판정은 실제 함수와 JSON/rc fixture로 검사하고 기존BInvoke의 무해 자식프로세스 시험은 반복하지 않습니다.
>
> harness작성·정적봉인600초, 위엔진상한360초, 보존/포장300초, 실패자료정리120초, 전체1380초를 제안합니다. 실제 새 시행 원점에서 측정합니다. 첫 시험 실패에서 원문과 실패 source seal을 보존하고 이후엔진/재시도를 중지합니다. 정책상거부되면 다른엔진/셸/Bypass로 바꾸지 않습니다. 준비시간 부족도 임의연장하지 않습니다.
>
> fixture의 허위승인·rc·정책값은 tests 전용 경로에만 둡니다. 실제 승인 예정 경로나 future_run/parent에 쓰지 않습니다. 검증이 통과해도 실제30초는 따로 승인받습니다.

제안 engine은 계약의 고정Python, 일반 WindowsPS5.1, 이전 Java stub 검증의 정확한JDK를 우선한다. JDK 경로/버전/식별을 추정하지 않고 기존 기록에서 읽어 봉인한다. 이 단계에는 실제 엔진 식별 조회 프로세스나 컴파일을 하지 않았다. 다음 승인 범위 밖이 필요한 경우 해당 차이만 보고한다.

논리군·하위사례 수는 `LIMITED_VALIDATION_PLAN.json`에 명시한다. assertion 수나 이번에 통과한 시험 수가 아니다. 양성에 필요한 전체 새 시간축/출력형상은 fixture로 만들고 원 CSV 대형 복제나 COMSOL 새 control을 사용하지 않는다.
