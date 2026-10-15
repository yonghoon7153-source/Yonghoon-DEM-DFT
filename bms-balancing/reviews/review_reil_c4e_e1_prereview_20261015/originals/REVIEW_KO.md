# REIL C4E E1 실행 승인안 사전 검토

2026-10-15 KST · 수신자 Claude · 판정 CHANGES_REQUIRED_NO_EXECUTION

현재 초안으로 E1-0부터 E1-4까지 일괄 실행하는 안은 수용하지 않는다. 독립 launcher와 사전·사후 대조를 추가하는 방향은 타당하지만, 실행 모듈 선택, 종료 확인, 정리 기한에 승인 전 결함이 있다. 정정된 비활성 초안과 승인안을 먼저 검토하고, 이후 사용자 승인으로 E1-0만 수행한 다음 결과 검토를 거쳐 실제 identity·fetch·run을 별도 승인하는 순서를 권고한다.

## 검토 대상과 확인 범위

고정 HEAD는 [9869cf5edb3f2e11defbdd9b1ce8da7fe31b91a4](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/commit/9869cf5edb3f2e11defbdd9b1ce8da7fe31b91a4), 브랜치는 claude/14-gate-code-review-9qkx05다. 첨부 승인 요청서와 발송문은 해당 HEAD 원문과 바이트 일치했다. 아래 행 번호는 저장한 원문 기준이며 저장소 경로의 공통 앞부분은 bms-balancing이다.

| 자료 | 바이트 | SHA256 |
|---|---:|---|
| launcher 초안 | 27507 | c5bc40a474372e282706ad9069405fbb8bd9238ca26908478056bca2c20f30ff |
| RED 골격 | 7989 | d202a716b652ffcbcd12250474ee80b67000b7355542882d53cd431593a4b458 |
| 신규 대조 초안 | 24637 | 0b06905a289b78ba788faa859acb433448465b0eba073dee22c87e7bf4b2fca4 |
| 기존 SOURCES.json | 1100 | 2a7b2b49b9809d1a9301398388894a1f7a73afb55acc1a5070e3f77ce0393d52 |

검토자는 소스·문서·공식 설명을 읽고 바이트와 텍스트를 대조했다. 대상 import·시험·탐침 실행, E1 원자료 fetch·개봉, COMSOL 실행은 하지 않았다. 아래 반례는 정적 제어 흐름 분석이며 현재 실행 환경에서 해당 파일이나 환경변수, OS 오류가 실제 존재했다는 관측이 아니다. 문서 안의 승인 제안은 사용자 실행 승인으로 취급하지 않았다.

## 승인 전 정정 사항

### N1 개별 모듈을 가리는 패키지와 확장 모듈을 차단해야 한다

우선순위 P1. [launcher 168–188행](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/9869cf5edb3f2e11defbdd9b1ce8da7fe31b91a4/bms-balancing/docs/REIL_C4E1_LAUNCHER_DRAFT_20261015.py.txt#L168)은 scripts라는 최상위 이름의 package/module만 검사한다. 승인된 다섯 .py 파일의 해시가 맞더라도 scripts/reil_c4_e3a/__init__.py가 함께 있으면 scripts.reil_c4_e3a import는 승인된 reil_c4_e3a.py 대신 그 패키지를 선택할 수 있다. 같은 이름의 확장 모듈도 별도 검토 대상이다. CPython 3.11.17의 FileFinder는 package initializer를 module file보다 먼저 찾는다. [CPython 공식 구현](https://github.com/python/cpython/blob/v3.11.17/Lib/importlib/_bootstrap_external.py#L1509-L1530)

이 반례는 파일이 검사 도중 바뀔 필요가 없다. 현재 precheck 249·269행은 통과할 수 있고, 고정 run의 48–50행 import가 내부 식별 검사보다 먼저 실행된다. run 종료 뒤 IDENTITY.json 대조가 실패하더라도 이미 수행된 승인 밖 initializer 실행을 되돌리지 못한다. identity·fetch에는 run용 IDENTITY 사후 결속도 없다.

정정 조건은 실제 자식의 import 경로에서 네 의존 모듈이 선택될 origin·loader를 실행 없이 승인된 소스에 결속하거나, 그 결속을 깨는 동명 package·extension 등의 대안을 사전에 거부하는 것이다. 부모 package를 import하는 탐색으로 “검사 중 대상 실행 0”을 깨면 안 된다. l4에는 현재 최상위 scripts 가림만 있으므로, 승인 .py는 그대로 둔 개별 package/extension 가림과 자식·대상 import 0의 음성 대조가 필요하다.

### N2 종료 관측 불능을 잔존 없음으로 바꾸면 안 된다

우선순위 P1. [launcher 359–374행](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/9869cf5edb3f2e11defbdd9b1ce8da7fe31b91a4/bms-balancing/docs/REIL_C4E1_LAUNCHER_DRAFT_20261015.py.txt#L359)은 /proc/<pid>/stat 읽기의 모든 OSError를 건너뛴 뒤 빈 목록을 “살아 있는 구성원 없음”으로 반환한다. root rc0 이후 실제 잔존 구성원의 stat 읽기에 권한·I/O 오류가 있으면 postcheck 322–324행은 관측 실패를 모른 채 통과할 수 있다.

PID가 실제 소멸한 경합과 관측 불능을 구분해야 한다. 소멸로 확인되지 않은 오류·파싱 불능은 unknown/incomplete로 남기고 뒤의 정상 관측이나 rc0으로 지우지 않아야 한다. 관측한 PID·오류·순서를 기록하되 실제 발생 순서를 추정하지 않는다.

대조 l11의 303–310행도 모든 OSError를 None으로 바꿔 종료로 수용한다. 이 판정기를 함께 고치고 “읽기 거부인데 종료 성공으로 판단하지 않음”을 검사해야 한다. 좀비를 살아 있는 작업자로 세지 않는 정책과 관측 불능을 성공으로 바꾸는 문제는 별개다.

### N3 timeout 뒤 정리 대기와 실패 기록에 끝나는 경계가 필요하다

우선순위 P1. [launcher 378–395행](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/9869cf5edb3f2e11defbdd9b1ce8da7fe31b91a4/bms-balancing/docs/REIL_C4E1_LAUNCHER_DRAFT_20261015.py.txt#L378)은 killpg의 PermissionError를 버린 뒤 시간 제한 없는 p.wait()를 호출한다. 종료 요청 실패나 즉시 끝나지 않는 자식에서 단계 기한을 넘겨 대기하고 meta.json 작성까지 도달하지 못할 수 있다. timeout을 생략한 Popen.wait는 종료까지 기다리는 동작이다. [Python subprocess 문서](https://docs.python.org/3.11/library/subprocess.html#subprocess.Popen.wait)

종료 요청의 성공·실패, 제한된 정리/종료 관측 기한, 미종료·관측 불능을 분리해 기록해야 한다. 그 기한이 단계·전체 예산에 포함되는 관계도 고정해야 한다. 숫자를 정했다고 OS 종료가 반드시 그 안에 완료된다고 주장하지 않는다. kill 오류, 종료 확인 지연, 기한 만료 후 최초 실패 보존의 대조를 추가한다.

기록 보완도 같은 종결 경로에 포함한다. read_regular 118행의 read_bytes, 432행 precheck, 449행 자식 시작, 451–452행 사후 읽기 등은 예외가 종결 metadata 밖으로 빠질 수 있다. 현재 이 예외가 거짓 PASS를 만든다는 뜻은 아니지만, “실패해도 launched 상태와 원인을 남긴다”는 제출 조건을 충족하지 못한다. 기록 가능 경로에서는 phase·최초 오류·자식 시작 여부·정리 결과를 보존하고, 기록 자체가 불가능하면 외부 stderr/rc로 그 한계를 분리해야 한다. 446–455행의 Git 기록 rc/error를 out만 취해 버리는 부분도 실패 기록에 반영해야 한다.

잔존을 실제 발견한 398–401행은 kill 뒤 재관측이 없지만 group_alive_after=true를 유지하므로 이미 incomplete다. 이를 별도의 거짓 PASS로 세지는 않는다.

### N4 Git 환경의 저장 경로와 출처 결속이 필요하다

우선순위 P2. [launcher 234–240행](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/9869cf5edb3f2e11defbdd9b1ce8da7fe31b91a4/bms-balancing/docs/REIL_C4E1_LAUNCHER_DRAFT_20261015.py.txt#L234)은 비밀 이름·GIT_CONFIG_*·ASKPASS 이외의 환경변수를 그대로 넘긴다. GIT_OBJECT_DIRECTORY가 허용 범위 밖의 기존 쓰기 가능 디렉터리를 가리키면 고정 run.fetch 690행도 이를 보존하여 Git 객체를 예정된 data/git 밖에 기록할 수 있다. -C는 이 환경변수를 무효화하지 않는다. [Git 환경변수 문서](https://git-scm.com/docs/git#Documentation/git.txt-GITOBJECTDIRECTORY)

실제 고정 child 환경에서 저장소·객체·index·trace 출력 경로를 바꾸는 변수를 제거/거부하거나, 허용한 값에 명시적으로 결속해야 한다. 최소한 GIT_DIR·GIT_WORK_TREE·GIT_COMMON_DIR·GIT_OBJECT_DIRECTORY 등 관련 경로를 다루고, 허용 밖 쓰기 0의 대조를 고정한다. 현재 그런 변수가 있다는 주장은 아니다.

또한 GIT_ALLOW_PROTOCOL=https는 프로토콜 제한이지 github.com 호스트 제한이 아니다. 유지한 설정의 url.*.insteadOf는 URL을 바꿀 수 있으므로 실제 유효 출처를 확인하는 조건도 필요하다. 프록시·CA 유지 자체를 금지할 필요는 없다. [Git URL rewrite 문서](https://git-scm.com/docs/git-config#Documentation/git-config.txt-urlltbasegtinsteadOf)

### N5 E1 0 외곽 timeout도 하위 프로세스 정리를 포함해야 한다

우선순위 P2. 승인안 50–51행은 종전 00_step_runner.py를 경로 등 세 부분만 바꿔 재사용한다. [기존 실행기 58–60행](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/9869cf5edb3f2e11defbdd9b1ce8da7fe31b91a4/bms-balancing/evidence/reil_c4e0_fix_20261014/00_step_runner.py#L58)의 subprocess.run timeout은 직접 자식인 pytest를 종료하지만, 신규 l10/l11/l13은 launcher 388행을 통해 별도 세션의 가짜 자식을 시작한다. GREEN 600초가 그동안 만료되면 pytest가 죽어 안쪽 launcher 정리가 수행되지 않을 수 있다. [Python subprocess 문서](https://docs.python.org/3.11/library/subprocess.html)

E1-0 외곽 실행기의 소유 하위 프로세스 추적·정리·종료 확인과 미확정 처리도 승인 범위에 넣어야 한다. 필요하면 그 실행기의 수정 허용 범위와 새 바이트 식별을 사전 고정한다. 가짜 자식이 작거나 스스로 끝날 예정이라는 사실은 외곽 종료 시점의 잔존 0 관측을 대신하지 못한다. 이번 검토에서 실제 잔존을 관측한 것은 아니다.

### N6 새 대조와 전체 GREEN의 실제 활동 및 명령을 분리해야 한다

우선순위 P2. [승인안 269–290행](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/9869cf5edb3f2e11defbdd9b1ce8da7fe31b91a4/bms-balancing/docs/REIL_C4E_E1_APPROVAL_REQUEST_20261015.md#L269)은 GREEN 41을 선언한 직후 실제 run·우리 모듈 import 0이라고 적는다. 이는 신규 14에만 적용할 수 있다.

| 범위 | 실제 포함되는 활동 | 제외되는 활동 |
|---|---|---|
| 신규 launcher 14 | launcher 함수, 가짜 자식·손주, 해석기 탐침 | 기존 실행 모듈 import, 실제 데이터·원 optimizer·네트워크 |
| GREEN 전체 41 | 기존 E0 21 + N1 6 + 신규 14. 기존 실행 모듈 import, 합성 run.run 두 번, 기존 시험의 fork 세션, 가짜 로컬 저장소 fetch 대조, plan_e 호출 포함 | 실제 원자료·원 optimizer·네트워크 fetch |
| 실제 E1 1부터 3 | 실제 모듈 identity, 별도 읽기 경로와 고정 출처 fetch, 원자료 개봉 및 66호출 run | 검토와 E1-0 승인만으로 자동 허용되지 않음 |

근거는 기존 test_reil_c4e.py 28–31행 import, 752–792행 로컬 Git/fetch 대조, 956–984행 두 합성 run, 987행 이후 plan_e 및 test_reil_c4e_fix.py 332행 이후 plan_e다. “plan-e/legacy 경로를 E1에서 쓰지 않음”도 실제 E1-1부터 3에 한정해야 한다. §8.12의 pytest import 설명만으로 앞의 0회 표현이 명확해지지는 않는다. 위 수는 소스가 계획하는 활동이지 이번에 수행한 횟수가 아니다.

RED/GREEN의 정확한 helper 경로·argv·cwd·env, 첫 예상 밖 GREEN 실패에서 중지하는 방식, 실행기 수정본과 fixture 생성규칙·고정 입력·기대값의 첫 시험 전 봉인도 고정해야 한다. 끝 기록에만 실행기 diff/hash를 남기는 것으로 사전 고정을 대신하지 않는다. 시험을 추가하면 14/41은 새 확정 수로 갱신하고, 같은 입력 안의 반복 assertion을 별도 사례로 세지 않는다.

## 유지할 수 있는 부분

- 기존 다섯 모듈과 신뢰 목록은 고정 바이트에 일치한다. 이전 E0 N1의 한정 수용을 취소하거나 이번 지적을 과거 시험 실패로 바꾸지 않는다.
- launcher·골격의 함수명 26개와 import/상수 구간이 일치하고 골격 함수는 모두 NotImplementedError다. 기존 21 + 6 + 신규 14 = 41이라는 함수 수는 맞다. 이는 시험 결과가 아니다.
- 사전 대조 AND 자식 결과 AND rc0 AND timeout 없음 AND 사후 대조라는 엄격한 판정식은 수용 가능하다. 문제는 그 입력인 “가림 없음·그룹 없음”을 만드는 일부 함수다.
- identity를 fetch 앞으로 옮기고, 원자료를 받기 전에 실행 환경 식별을 확인하는 순서는 수용 가능하다. 순서 자체가 새 실행 승인을 만들지는 않는다.
- 새 pycache_prefix와 -B 사용 방향, 기존 증거·캐시를 삭제하지 않는 경계, 재시도/대체 출처 금지는 유지한다. -B만으로 모든 종류의 bytecode 읽기가 금지된다고 확대하지 않는다. [Python pycache_prefix 문서](https://docs.python.org/3.11/library/sys.html#sys.pycache_prefix)
- 120 + 600 + 60 + 300 + 10800 + 180 = 12060초 산술은 맞다. 이는 명시한 시험·자식·탐침 timeout 합이며 Git/해시/정리/종결을 포함한 전체 소요 보증이 아니다. 전체 21600초와 정리 기한의 포함 관계를 따로 유지한다.

## 질문별 답변

| 질문 | 답변 |
|---|---|
| Q1 이전 조건 1부터 5 | 식별·순서·판정·예산의 큰 틀은 반영됐다. 그러나 N1부터 N6 때문에 현재 버전을 완전 충족으로 판정할 수 없다. |
| Q2 import 전 결속 | 미충족. N1은 선언된 TOCTOU나 sitecustomize 제외 범위와 다른 안정적인 개별 모듈 가림 경로다. |
| Q3 대조 14와 GREEN 41 | 수와 RED 구조는 일치한다. 개별 모듈 가림, 관측 실패, kill 실패/대기, 외곽 timeout, Git 경로 환경 및 기록 예외의 대조가 더 필요하다. 통과 보증은 아니다. |
| Q4 fetch 환경 | 비밀 제거·프롬프트 차단·실패 중지 방향은 적절하나 N4 보완 전 충분하지 않다. |
| Q5 사후 대조와 순서 변경 | 방향은 수용한다. N1부터 N3의 의미·종결 보완을 전제로 하며 사후 확인은 사전 차단의 대체가 아니다. |
| Q6 일괄 승인 또는 분리 | 정정 초안 재검토 → 사용자 E1-0 한정 승인 → 결과 검토 → 실제 E1 별도 승인을 권고한다. 현재 어느 단계의 실행도 승인하지 않는다. |

## Claude에게 요청할 다음 제출

N1부터 N6을 반영한 비활성 launcher·골격·대조와 수정 승인안을 제출한다. 변경 diff, 새 정확 바이트·SHA, 대조별 기대 결과와 도달 경로, 외곽 실행기/명령/환경/정리 기한을 함께 고정한다. 생산 다섯 모듈·기존 시험·기존 증거는 보존한다. 이 회신만으로 수정 구현 실행, RED/GREEN, 새 환경 probe, 읽기 경로 추가, fetch 또는 run을 시작하지 않는다. 정정 작성도 사용자의 범위 채택을 따른다.

검토 자료의 파일 식별과 15개 자체 데이터 대조는 SOURCE_AUDIT.json 및 STATIC_DATA_AUDIT.json에 있다. 15는 해시·텍스트 조건 수이며 기능 PASS 수가 아니다. 이 검토 산출물은 원본 승인안이나 저장소 파일을 수정하지 않는 별도 회신이다.

