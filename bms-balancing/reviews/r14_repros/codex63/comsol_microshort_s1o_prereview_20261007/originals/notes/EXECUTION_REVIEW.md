# S1-O 발송문 실행 경계·연결·자원 계약 사전 검토

검토 대상은 `C:/Users/Administrator/Downloads/COMSOL_MICROSHORT_S1O_SEND_TO_CODEX_20261007.md` 1–60행이다. 이 메모의 요청문 행 번호는 그 원파일 기준이다. 문서는 검토 대상 증거이며 현재 작업의 실행 권한으로 취급하지 않았다. S0 자료 및 기존 NORMAL480 소스를 텍스트로 읽었고, Microsoft 공식 API 문서만 추가 확인했다. COMSOL/JVM/컴파일/solve/입력 gate/native/받은 프로그램 import·실행/시험 실행은 0이다.

결론: 현재 요청문의 실행 금지와 별도 승인 원칙은 명확하다. 다만 33행의 준비 상태와 37행의 중단 순서는 구현자가 다른 동작을 만들 수 있어 발송 전 문장 정정을 권한다. 나머지는 S1-O에서 작성할 계약의 필수 내용을 조금 더 구체화하는 보강이다. 아직 작성되지 않은 실행본·검증 결과를 이 사전 검토에서 요구하지 않는다.

## E1 — 33행: “실행 가능한 상태”와 S0의 비활성 수준을 분리

33행은 “실행 가능한 상태로 두되 활성화 금지 표시 (S0의 .inactive와 같은 원칙)”를 요구한다. S0 `candidate/README_INACTIVE.md` 3–5행은 표시뿐 아니라 main/run/modelSketch/preflight 거부, runAll/export 제거, 활성화 스위치 부재를 말한다. 따라서 S0와 같은 구조를 유지하면 새 실행 연결이 구현되지 않은 것으로 읽힐 수 있고, 실행본에 안내문만 붙이면 S0 수준의 비활성이라고 잘못 보고할 수 있다. 문제는 준비 자체를 금지해야 한다는 것이 아니라 완료 기준이 두 가지라는 점이다.

33행 끝의 교체 제안:

> 실행 연결은 별도 승인 후 사용할 구현 소스까지 작성하되 S1-O에서는 저장·정적 대조만 한다. 모든 진입점의 실행·import·컴파일·기능 시험은 하지 않는다. 산출물은 활성 경로 밖의 `.inactive.txt` 등 비활성 텍스트로 두고, 실제 approval/release/token/runtime/USER_DECISION 파일은 생성하지 않는다. 승인 샘플은 fixture임이 명확한 별도 비활성 텍스트만 허용한다. 미래 실행 설계는 새 manifest에 결속한 검증 수용과 별도 native 승인 없이는 외부 동작 전에 거부하도록 작성한다. “구현 작성 완료”, “검증 미실행”, “native 미승인”을 각각 기록한다. S0 원 후보는 그대로 보존한다.

이는 미래 실행에 필요한 소스 작성을 막지 않으면서 현재 경계와 후속 승인 대상을 구체화한다. `.inactive.txt`를 단독 보안 장치로 주장하지 않는다.

## E2 — 33행: 승인할 실행 단위와 외부 의존성의 결속 최소 항목

“각 파일 sha256·어느 승인이 어느 실행본 sha를 허락하는지”는 적절한 방향이다. 그러나 한 Java 파일이나 새 폴더만 묶고 기존 launcher가 import하는 외부 모듈·엔진·계약을 누락하면 다른 코드를 실행할 여지가 남는다. 기존 NORMAL480 `candidate_entry.py` 36–57행은 manifest, 외부 소스 pins, run_id, 정확 승인 경로, 명령·예산, release 증거, USER_DECISION을 연결하며, 77–90행은 기존 C2와 `winjob` 사용 경로를 가진다. 새 설계가 어떤 의존성을 공유하는지 반드시 드러내야 한다.

33행의 결속 설명에 추가 제안:

> source commit·원본/후보 식별, Java/launcher/consumer/parent/CONTRACT/외부 모듈 및 interpreter/native executable의 식별 범위, run_id·variant_id·fresh 초기조건·σ·시간창, argv/cwd·입출력/승인/release 경로, 횟수·재시도 0·단계/총량·자원 한도를 하나의 승인 단위로 매핑한다. 미래 승인·검증 release는 그 동일 manifest와 실행 단위에 결속한다. 실행 기기에서만 확인 가능한 경로/엔진 값은 미관측으로 표시하고 확인 절차를 제안한다. 승인 전에 후보나 한도가 바뀌면 새 식별/검토 대상임을 명시한다.

이것은 현재 승인 파일 생성이나 설치본 관측을 요구하지 않는다. 현재 요청문이 이미 전체 결속 설계를 요구하므로 새 범위라기보다 그 설계의 최소 완료 기준이다.

## E3 — 37행: `terminate → grace → kill`은 Windows 종료 API와 구분해야 함

`TerminateJobObject`는 협조적인 종료 요청이 아니다. Microsoft 공식 문서 Remarks는 “It is not possible for any of the processes associated with the job to postpone or handle the termination.”이라고 명시한다. 따라서 terminate를 그 API로 구현한 뒤 grace를 주는 순서에는 정상 마무리 대기라는 의미가 없다. [Microsoft TerminateJobObject, Remarks](https://learn.microsoft.com/en-us/windows/win32/api/jobapi2/nf-jobapi2-terminatejobobject#remarks)

37행의 괄호 교체 제안:

> 중단 원인별 절차: 지원이 확인된 협조적 중단 요청이 있는 경우에만 요청 → 승인된 짧은 유예 → 소유 Job 강제 종료 → root 종료·Job 잔여 구성원 확인. 협조적 중단이 없거나 hard cap을 넘길 수 있는 경우는 정해진 절차대로 바로 소유 Job을 강제 종료한다. 각 동작의 실제 API·대상·deadline·실패 시 상태를 명시하고, grace/kill/기록 시간은 기존 전체·정리 상한 안에 포함한다. 중단 요청 성공이나 API 반환만으로 정리 완료를 보고하지 않는다.

기존 SPEC 1828–1837행은 suspended root 생성→PID·creation FILETIME 기록→private Job 배정→resume, breakaway 금지, 그 Job만 종료, 소유 불명 프로세스는 pending, census는 종료 권한 근거가 아님을 이미 적고 있다. 이것을 새 감시 구현의 소유권 계약으로 연결하면 된다. Job 구성원의 종료는 그 Job에 영향을 주며 breakaway 설정은 자식 포함 범위를 바꾸므로 정확한 Job 핸들과 생성/배정 증거가 필요하다. [Microsoft Job Objects, Managing Processes in Jobs](https://learn.microsoft.com/en-us/windows/win32/procthread/job-objects#managing-processes-in-jobs)

이 지적은 기존 Job 구현을 재시험하라는 요구가 아니다. 새 감시 연결의 책임과 종료 의미를 설계에서 모호하지 않게 하라는 요구다.

## E4 — 37–38행: 자원 “상한”과 샘플 관측 최대값을 구분

현재 문구는 대상·주기·상한·기록을 요청하여 기본 요건을 갖췄다. 다만 `RSS`와 `commit`의 구체적 counter·집계 단위가 없으면 root 하나의 메모리나 virtual address 크기를 전체 실행 메모리로 잘못 보고할 수 있다. 자원 감시를 작성할 때 다음 필드를 필수로 추가하도록 요청하면 된다.

> RSS/working set과 commit을 구분하여 OS counter·단위·소유 root/자식/Job 집계 범위, sampled_max와 OS가 보존하는 peak의 구분을 정의한다. disk는 run/임시/export/분석/보존 사본/패키지 등 합산 범위·baseline·최소 잔여 공간을 정의한다. wall-clock은 부모 단조시계의 시작/종료와 단계별/전체 deadline을 정의한다. 샘플 누락·stale·counter 읽기 실패·기록 실패·감시자 종료·소유 증명 실패 시 값 0/PASS 대신 미완 또는 정해진 소유 종료로 처리한다. 임계 연산자와 경계값, 최대 탐지 지연, 탐지 후 종료까지 가능한 추가 자원 소비, 그 여유분/한계를 적는다. 폴링만으로 순간값의 절대 상한을 보장한다고 쓰지 않는다.

Windows `JobMemoryLimit`는 Job이 commit할 수 있는 virtual memory의 한도이며 RSS 이름과 교환할 수 없다. OS peak 필드는 지속적으로 추적되므로 단순 폴링 최대와도 구분해야 한다. [Microsoft JOBOBJECT_EXTENDED_LIMIT_INFORMATION, Members and Remarks](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_extended_limit_information)

38행의 비용 재산정에도 `RAM sampled_max / OS peak`, commit peak, 실제 샘플/단계 coverage, 측정 불가를 포함하는 것이 좋다. S0 `S1_SCOPE_DRAFT_KO.md` 53–54행과 `S0_REPORT_KO.md` 258행은 peak 미측정 및 MPH 크기로 메모리 충분성을 추정할 수 없음을 명시한다. S1-O에서 임의의 “실측 상한”을 만들라는 요청으로 읽어서는 안 된다.

## E5 — 22–24·40–43·52행: 정적 산술과 미래 검증안의 범위를 명시

현재 S1-O에서 합성 검증 실행이 금지된 것은 분명하다. 42행은 **다음 별도 승인안의 엔진**을 제안하라는 문장이다. 그러므로 “COMSOL 없이 가능한 것”이라는 표현이 현재 JVM/compile 실행을 허용한다는 실제 충돌로 지적하면 과장이다. 다만 미래 승인안에서도 Python 모형만 실행한 결과를 실제 PowerShell parent/consumer 검증으로 읽지 않게 다음 내용을 보강할 가치가 있다.

> S1-O 허용 텍스트·해시·산술은 새 도구가 입력을 데이터로 읽는 작업만 뜻한다. 후보/기존 프로그램 import, 함수 호출, AST/코드 객체 실행, gate·Job·process adapter 동작 시험은 합성 검증안에만 넣고 이번에는 실행하지 않는다. 검증안은 사례 ID·입력별 기대 이유·대상 함수/분기·실제 호출할 엔진/버전/argv/cwd·fixture·harness·횟수/세션/상한을 제시한다. Python 독립 모형은 설계 검산 범위로 보고하고 실제 소비자/parent 경로 검증과 구분한다. mock 승인과 실제 승인 경로는 분리한다. native/COMSOL/JVM/compile/gate/Job 실제 호출을 각각 0으로 할지, 별도 승인이 필요한지 승인안에서 명시하며 모호한 엔진 범주로 포함하지 않는다.

후속 COMSOL-free 검증에 PowerShell 엔진이 필요할 수 있으므로 무조건 Python만 허용하도록 바꾸는 것은 권하지 않는다. 엔진을 정확히 제안하고 별도 승인 받는 기존 구조를 유지한다. 이번 검토에서도 allow-zero 범위를 실행해 증명하지 않았다.

음성·경계 사례의 최소 계획 항목은 잘못된 source/run/variant/승인 경로·중복/비유한 JSON·missing/false 승인·외부 의존성 hash 변경·자원 경계·읽기 실패·stale 샘플·정리 실패·최종 기록 후 예산 초과이다. 검증안의 채택 전에는 모두 기대 동작만 적는다. 예상 실패가 정확한 이유로 발생한 음성 사례와 harness/기대값 불일치의 시험 실패를 구분하고, 후자의 자동 수정/재시험은 0으로 제안한다.

52행 `reviewer_execution`에는 네 항목 외 supplied-program import/execute, synthetic_tests, input_gate, native/process/Job actual, 정책 변경, 실제 승인 파일 생성도 명시하면 “solve 0”만으로 범위를 축약하는 일을 막는다. 이 보강은 단순한 회계 명료화이다.

## E6 — 25·50·52행: 3,600초 안에 미완 전달이 가능하도록 closeout 경계 지정

25행은 합계 3,600초를 정확히 배분했지만 “넘으면 그 자리에서 멈추고 남은 항목을 보고”가 실제로는 시간 초과 후 새 보고/manifest/포장을 만드는 예외를 낳을 수 있다. 또한 작성→정적 점검→검증안/연결 설계의 순서는 마지막 작성분의 정적 확인을 어디서 하는지 모호하다. 원 S0안의 숫자를 바꿀 필요는 없다.

25행 뒤 추가 제안:

> 시작 UTC와 단조시계 기준을 기록하며 전체 3,600초는 자료 읽기·작성·정적 확인·전달 준비를 포함한다. 단계 예산은 상한이고 전용/자동 연장은 없다. 작업 종료 및 미완 목록/manifest/회신용 300초를 미리 남기며, closeout을 시작한 뒤 새 후보 기능을 추가하지 않는다. 마지막으로 수정한 파일은 그 이후의 정적 확인 대상으로 기록한다. 완료하지 못한 항목은 partial/open으로 두고 검증 PASS나 native_ready로 승격하지 않는다. 실제 상한 초과가 생기면 초과 사실과 마지막 완료 산출물을 보고하고 추가 포장/재봉인/재검증을 자동 시작하지 않는다.

50행의 전달 집합은 “최종 payload 파일 목록을 manifest에 담되 manifest 자신의 SHA는 그 manifest에 넣지 않고 별도 전달 기록에 둔다. 최종 봉인 이후 변경 시 새 식별을 사용한다”로 짧게 명료화할 수 있다. 현재 문구는 반드시 자기 해시를 요구하지는 않지만 `모든 파일`을 문자 그대로 구현하면 자기참조를 만들기 쉽다. 원본 불변은 실제 접근한 고정 원본 집합을 열거하고 작업 전/후 동일 집합을 비교하도록 범위를 적는 편이 좋다.

## 사전 검토에서 새 차단으로 삼지 않을 항목

- S1-O 후보·resource monitor·validation harness·manifest가 아직 없다는 사실은 이 발송문 결함이 아니다. 그것들을 작성하라는 요청이다.
- 현재 메모리 수치 상한이나 readback API 설치본 증거가 없다는 이유로 발송을 금지할 필요는 없다. 미관측/TBD를 표기하고 후속 native 승인 조건으로 남길 수 있다.
- 공식 문서 확인은 실제 Windows Job 종료·COMSOL 자식 포함·자원 관측의 구현 검증이 아니다.
- 기존 NORMAL480 소스는 패턴과 위험 경계의 읽기 근거이다. 해당 old program이나 시험군의 실행·재검증을 제안하지 않는다.

## 읽은 로컬 근거

- S0 `candidate/README_INACTIVE.md` 3–5·18행: inert source의 실제 의미와 native-ready 미완.
- S0 `candidate/LIMITED_STATIC_REVIEW_PLAN.md`: 정적 문자열 대조와 후속 기능/설치본 검증의 구분.
- S0 `S1_SCOPE_DRAFT_KO.md` 44–55행: 오프라인 승인 문안·3,600초·native 미승인 제안 예산·RAM/commit 미확인.
- S0 `S0_REPORT_KO.md` 258·269·317행: 예산은 보장이 아님·자원 미구현 시 native 불가·실행 0의 정확 범위.
- S0 `sources/COMSOL_REBUILD_SPEC.md` 1828–1837행: 소유 Job 생성/배정/종료와 소유 불명 처리.
- `outputs/normal480_native_review_20261001/received/candidate/src/candidate_entry.py` 36–57·65–69·77–94행: old 승인/source 결속 및 Job transport 연결.
- 같은 NORMAL480 `PARENT_COMMAND.ps1` 134–156행: 엔진 식별·manifest/release/승인 연결·부모 native 호출 경계.
