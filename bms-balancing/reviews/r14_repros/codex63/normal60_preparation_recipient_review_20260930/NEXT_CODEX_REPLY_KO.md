# 정상60 준비본 검토 회신 및 다음 제한 검증 승인 문안

2026-09-30. **검토 회신: 오프라인 준비본 수용. 기능 검증 및 native60 승인은 별개다.**

두 전달 ZIP의 집합·크기·SHA·CRC·경로 검사를 통과했다. 후보 manifest `82e556243b29b10ae65b95dcdff7f854734b6f1cfffc1881327cab1939ebe5c8`의 5개 파일, 이전30초 source/manifest, 기준 CSV12개 식별, Java/entry 역치환 전체 바이트 및 부모의 두 비교 소비를 확인했다. 737개 요청시각은 기존437 + 새300이며 저장 개수 고정값이 아니다. 새 차단 결함은 발견하지 않았다.

다음은 같은 계획 반복이 아니라 제안된 **12군46사례 변경부 한정 검증**이다. 아래 블록은 사용자가 채택해 전달할 때만 승인 문안으로 사용한다. 이 검토 문서 자체나 첨부 사실은 실행 승인이 아니다.

---

위 manifest에 고정된 정상60 후보의 **변경부 한정 오프라인 검증 1건만 승인합니다. 실제60초 계산은 승인하지 않습니다.**

1. LIMITED_VALIDATION_PLAN.json의 12군46사례(Python27/Java helper4/PS5.1 15)를 그대로 대상으로 합니다. 기존111개/C2/Job/1198/30초는 반복하지 않습니다. 후보 생산 코드·수치 한도·원본은 수정하지 마세요.
2. 첫 시험 전에 새 소유 fixture 위치, harness, 엔진 경로/현재 바이트 SHA, 정확 argv/cwd, 추출 함수 원문/SHA, 각 사례의 기대 이유와 도달 단계를 봉인하세요. 실제 future_run/future_parent/future_authorizations·승인/release/token은 만들지 않습니다. mock 승인은 별도 fixture로만 둡니다.
3. 실제 consumer→entry와 PS5.1 GDecision을 사용하고 Python 결과를 PS가 직접 소비하게 하세요. native/process/Job/실제 입력 차단은 대상 import 전에 설치합니다. Java는 COMSOL-free checkShape/TIMES 추출 helper compile1회와 stub JVM1세션만 허용합니다. COMSOL jars·전체 모델 compile/JVM·COMSOL/batch/solve·실제 콘솔 입력·정책/prefs/registry/ACL 변경은 제외합니다.
4. PY02-03의 변이 필드와 기대 이유, PY03-05/06의 선행 요청 누락 검사 여부를 fixture 봉인 때 특정하세요. 임의 예외·잘못된 fixture·의도하지 않은 앞단 실패를 해당 목표의 PASS로 세지 않습니다. 기존46사례 안에서 구체화하며 새 사례/추가시험을 자동으로 늘리지 마세요.
5. 횟수·예산은 봉인600초, Python1세션120초, helper compile1회90초, stub JVM1세션60초, PS5.1 1세션90초, 보존/포장300초, 미완기록120초, 전체1,380초입니다. 새 원점으로 단계별/전체 시간을 기록합니다. 첫 실패 또는 예산/범위 위반이면 최초 오류·원문·rc·미실행 목록을 보존하고 중지합니다. 자동 수정/재시도/부분 probe/다른 엔진·권한 fallback은 없습니다.
6. 최종 manifest와 실제 시험 소스를 대조하고 source/engine/harness/fixture/result/바깥 반환을 연결하세요. 포장 후 영수증·실제 마지막 도구 반환도 제공하되 내부 snapshot/호출 wall time/전체 누적시간을 구분합니다. 최초 실패 기록이나 기존 recipient=null을 덮어쓰지 마세요.
7. 결과와 다음 native60 비활성 승인문을 제출하고 멈추세요. 전부 통과해도 실제 native 승인/release를 활성화하거나 COMSOL로 이어서 실행하지 않습니다. 전체/정상 gate INCOMPLETE·실효 정책 UNVERIFIED·장시간 보류와 기존 실패/pending/원복을 유지합니다.

---

이 검증 결과가 수용되면 현행 정책 무변경 경로·고정 입력/소스·예산을 확인한 뒤 fresh 0→60초 최대1회를 따로 승인합니다. 120초/12시간·CDC·휴지·유한sigma·sweep·후보C는 포함하지 않습니다.
