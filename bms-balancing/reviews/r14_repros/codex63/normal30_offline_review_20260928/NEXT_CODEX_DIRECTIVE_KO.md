# 다른 Codex에게 전달할 회신·다음 한정 작업지시 초안

**사용자가 아래 범위를 채택해 전달했을 때의 다음 오프라인 작업안이다. 수신 검토 자체가 native30 실행 승인이나 실제 approval/release 생성 승인이 아니다.**

정상30초 준비 방향과 Java/요청시간 불변 근거는 수용합니다. ZIP SHA `ec9b0ea876ab7ba973c80fc924e8829f32a4cb8956334155d605c1ef61591277`, manifest `28dd6da5cc76885263c17b2671548a00692064807e02e77ceb6f3edbdd946fa5`에 대한 잔여는 N30-N1/N2 두 건입니다. 일반 계획이나 기존 입력/정책 진단을 반복하지 말고 아래 수정과 변경부 한정 검증을 묶어 진행할 수 있게 준비하세요.

## 허용할 최소 수정

1. 초기 Li 각 항의 기준을 절대차≤1e-9 mol/m²로 명시하세요. 총 Li drift 상대≤1e-6은 그대로입니다. Python 결과의 절대차/단위/한도, 부모 소비, 계약/보고서/검증안을 일치시키세요. 상대차는 참고값으로만 남길 수 있습니다. 상대기준으로 바꿀 이유를 새로 만들 필요는 없습니다.
2. 부모 FINAL_BOUNDARY 쓰기·read-back·식별 확보 뒤 마지막 출력 직전에 전체/전달 예산을 다시 확인하세요. 초과하면 마지막 반환의 within_limits=false/limited=INCOMPLETE와 이유를 남기고, 이전 boundary PASS로 덮지 않으세요. 기록은 pre-write와 post-write 관측을 구분하고 무한 재봉인하지 마세요.
3. 새 source revision/manifest를 봉인하고 이전 후보·최초 정적 결과·ZIP을 보존하세요. 같은 native run 후보 식별을 유지한다면 아직 runtime이 없다는 전제를 확인하고 새 manifest에 모든 명령/승인 초안을 맞추세요. 실행 폴더를 만들거나 충돌 경로를 지우지 마세요.

Java의 물리·출력 API·시간437개·threshold0, 기존 C2 입력 본문/owned Job, BSave/BInvoke, 기준 CSV/좌표·OCP/수치 설정은 변경하지 않습니다. 이 두 수정 밖의 제어 변경이 필요하면 그 부분만 중지·보고하세요.

## 별도 사용자 채택 후 수행할 변경부 검증

기존 LIMITED_VALIDATION_PLAN의17군/53명세를 출발점으로 하되, 첫 시험 전에 정확 하위사례 수·이유·엔진·harness·소스 SHA를 고정하세요. 숫자를 맞추려고 사례를 중복 집계하지 마세요.

- PY06/PS03에 초기 Li 동일값·정확1e-9경계·경계초과·N/P상쇄·상대통과/절대실패를 추가합니다. 부모의 absolute 필드 누락/NaN/위조된 PASS도 확인합니다.
- PS04/PS05에 pre-write 예산 통과→성공한 writer/hash 뒤 전체5100 또는 전달300초 초과, 정확 경계, 마지막 반환 실패가 이전 PASS를 이기는 경우를 넣습니다. 실제 부모 분기를 clock/writer inert adapter로 시험합니다.
- 기존 계획의 정상30/보호중단/오류,437시각,exact공통 prefix,late interval,승인·경로,rc/필수필드/숫자 거부 사례를 유지합니다. Python에서 만든 정상/보호 결과를 실제 PS GDecision 입력으로 연결합니다.
- native/console/Job 진입점을 import 전에 inert로 치환합니다. Java는 정확 checkShape와 최소 의존성만 추출한 COMSOL-free helper입니다. 전체 모델 컴파일/COMSOL jars/모델 로드는 제외합니다.

제안된 한도: harness·봉인600초, Python1세션120초, Java helper compile1회90초/JVM1세션60초, Windows PowerShell5.1 fixture1세션90초, 보존·포장300초, 미완 정리120초, 전체1380초. 새 원점과 실제 엔진 식별을 기록하세요. 첫 실패 시 최초 소스/seal/출력을 보존하고 뒤 엔진을 멈춥니다. 자동 수정·재시험·부분 probe·fallback은 없습니다. 이 예산으로 수정/검증이 불가능하면 시작 전에 필요한 차이만 제안하세요.

이 초안은 다음 오프라인 작업 범위를 제안합니다. 사용자가 아직 채택하지 않았다면 실행하지 않습니다. 기존389/67/78 suite·B020 재분석·1198 재실행·별도 C2 입력진단은 포함하지 않습니다.

## 제출 및 다음 경계

최소 diff, 새 manifest, Java 역치환/437시간 불변, 코드→시험 대응, 각 엔진 raw 반환·실패 보존·종료/예산·선택 보존, 비활성 native30 승인문을 한 묶음으로 제출하고 멈추세요. 실제 approval/release/runtime/token/USER_DECISION 생성, COMSOL/native compile/solve, 정책 변경은0회입니다. 승인 초안은 새 식별을 반영하되 approved=false/usable=false로 둡니다.

검증 결과가 수용되면 별도 계획 루프 없이 **정책 무변경·fresh0→30초·최대1회**의 고정 실행본을 사용자에게 승인 요청합니다. 이번에는30초를 실행하지 않습니다. 30초 결과 이후 다음 연장 시간은 경향/guard 여유/수치·자원 결과를 보고 별도 결정하며,12시간·CDC·휴지·sweep·후보C 승인을 포함하지 않습니다.

기존1198 한정 수용·B020 분석 완료는 유지합니다. 정상 전체 gate/전체 수렴 INCOMPLETE, 장시간 보류, 내부 실효정책 UNVERIFIED·OCP외삽 금지·TIME_CAPS 미확인·기존 failed/pending/원복/recipient=null도 유지하세요.
