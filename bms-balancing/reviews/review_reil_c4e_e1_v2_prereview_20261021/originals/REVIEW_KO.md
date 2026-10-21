# REIL C4-E E1 v2 사전 검토
2026-10-21 · 읽기 전용 정적 검토

## 판정

**CHANGES_REQUIRED_NO_EXECUTION — 현재 고정본으로 E1-0 승인 단계에 진입하는 것은 보류합니다.**

첨부된 승인 요청문을 실행 지시로 채택하지 않았습니다. N1·S1의 정적 보완과 N6의 활동·승인 범위 분리는 수용 가능합니다. 현재 E1-0에 관한 정정 5건과 미래 E1-2에만 해당하는 항목 1건을 구분합니다. 받은 프로그램은 실행하지 않았습니다.

## 1. 검토 기준과 식별

제출 문서 2개는 아래 고정 커밋 원문과 바이트가 같습니다.

- 저장소: yonghoon7153-source/Yonghoon-DEM-DFT
- 브랜치 식별명: claude/14-gate-code-review-9qkx05
- 검토 커밋: 0e4fbbde88d6b1bcfd47be65718c4ff0efe2191c
- 이전 기준: 2026-10-15 E1 사전 검토. 회신과 DECISION을 basis에 보존했습니다.
- 정정 범위: REIL_C4E_E1_REVISION_SCOPE_20261015.md. 정정 범위 채택과 E1-0 실행 승인은 별개입니다.

| 비활성 초안 | bytes | SHA-256 |
|---|---:|---|
| LAUNCHER_DRAFT_v2 | 47,030 | ab33844fbdaa4e6939871abec09953783cfccd7b4d32ee023ab8691cdb814398 |
| LAUNCHER_SKELETON_DRAFT_v2 | 13,404 | 5617a16aa8b093bac485e0bf775109c77ba9699d43301cf503e783365798b362 |
| LAUNCHER_CONTROLS_DRAFT_v2 | 41,093 | c1dc5b4353fa97e29b988604b612c7f40e46d3562980bde40dfd4712e4fde4ea |
| STEP_RUNNER_DRAFT | 12,849 | aae2ec14c4d652ef9a9e5b1c45bf52896d2234dce16eac77942911e596669fed |

전체 경로·Git blob 식별·SHA는 SOURCE_INDEX.json에 있습니다. 아래 L/C/S/A/R은 각각 launcher, controls, step runner, approval request, revision scope이며 모두 동봉 고정 소스의 1-based 행입니다.

## 2. 현재 E1-0 승인 전 정정

### V2-01 · P1 · 외곽 실행기의 관측 오류 유실

근거: S:118,138–151,208,229.

reap()은 proc_table()의 오류를 버립니다. settle.watch()는 곧바로 별도 descendants() 조회를 하고, 그 두 번째 관측이 정상·alive 0이면 empty를 반환합니다. 정상 pytest 종료와 정상 Git 기록을 전제로, 첫 관측의 권한/목록/파싱 오류가 사라지고 runner_ok=true가 될 수 있습니다.

timeout 루프에서도 descendants 오류를 버립니다. 그 경로는 timeout 플래그로 정상 판정이 막히지만 최초 관측 오류 증거는 누락됩니다. 이는 R:33–36,70 및 A:183의 “관측 오류는 unknown” 요구와 충돌합니다. launcher group_status 자체의 개선과 외곽 실행기 잔여를 구분해야 합니다.

정정 조건: reap·timeout·settle의 모든 오류를 동일 누적 기록에 결속하고 이후 정상 empty가 지우지 못하게 하세요. 첫 reap 오류 후 정상 빈 관측의 unknown·최초 오류·runner_ok=false를 정정안에 연결해야 합니다. 실제 오류를 발생시킨 결과가 아니라 소스의 정적 경로입니다.

### V2-02 · P1 · 첫 Git 호출 이전의 환경 격리 누락

근거: S:36,54–56,171–173; C:135–137,142–150; L:350–355,666–668.

launcher.child_env는 GIT_SSL_CAINFO 외의 상속 GIT_*를 제거한 뒤 GIT_TERMINAL_PROMPT=0을 고정하지만 외곽 실행기는 비밀 형태의 이름만 제거합니다. GIT_OBJECT_DIRECTORY, GIT_DIR, GIT_INDEX_FILE, GIT_TRACE 등이 pytest에 남을 수 있습니다. 새 대조의 _tree()는 L.child_env 전에 env를 지정하지 않은 git init·빈 commit을 실행합니다. 외곽 자체 Git 기록과 launcher의 git_out 역시 env를 지정하지 않아 원래 환경을 상속합니다.

정적 반례: GIT_OBJECT_DIRECTORY가 허용 밖의 기존 쓰기 가능 위치를 가리키면 RED fixture 초기화부터 객체가 tmp 밖에 기록될 수 있습니다. GIT_DIR은 HEAD/porcelain을 다른 저장소에서 읽게 할 수 있습니다. 현재 해당 변수가 있다는 관측은 아닙니다. 이 입력에서 “tmp 안 로컬 Git” 경계를 지키지 못하는 소스 추론입니다. Git 공식 문서는 이러한 객체·저장소 위치 재지정을 명시합니다. [Git 환경변수](https://git-scm.com/docs/git#_environment_variables)

정정 조건: 외곽 자체 Git·pytest·fixture 직접 Git까지 첫 호출 전부터 일관된 제거/거부 정책을 적용하세요. launcher 내부에서 나중에 정리하는 것으로 대신하지 마세요. 허용 밖 object/index/trace와 다른 저장소 지정의 음성 대조 또는 명시적 착수 차단을 고정해야 합니다.

### V2-03 · P2 · 정리 15초와 명목 대기 합 불일치

근거: A:77–78; S:40–41,129–155,206–221.

승인 표는 각 단계 “실행기 정리 ≤15초”입니다. timeout 경로는 kill 대기 10초 후 settle의 자연 종료 관측 5초, 남으면 kill 후 재관측 5초를 더합니다. 명목 배정만 10+5+5=20초입니다. 남은 기한이 없어도 후속 p.wait에 timeout=0.1초를 부여할 수 있으며, 스캔·기록 시간도 별도입니다. 0.1초가 반드시 소비된다는 뜻은 아닙니다. 15초의 공통 절대기한도 없습니다.

S:220의 elapsed_s는 settle 전에 계산되어 전체 정리 완료 시간이 아닙니다. OS 종료시간 보장과 별개로 코드와 승인 표의 배정이 맞지 않는 문제입니다.

정정 조건: 요청한 한도 안의 공통 절대기한으로 정리하거나 새 예산을 사용자 선택 대상으로 명시하세요. 검토자가 15초를 20초로 자동 확대하지 않습니다. child 대기·정리 종료·후속 기록의 시간 경계를 나누세요.

### V2-04 · P2 · 준비 예외가 최초 오류 기록 밖에 있음

근거: R:45–46; L:688–703,738–751; C:561–587.

prefix/mpl/tmp 생성, argv 구성, 자기 파일 읽기·해시, 최초 disk 조회는 오류 기록 try 이전입니다. 최초 폴더 생성이나 disk 조회 오류는 약속한 errors/first_error/launched 및 meta 실패의 구조화된 stderr/rc4 경로에 들어가지 않습니다.

실패를 성공으로 바꾼다는 지적은 아닙니다. 채택된 “준비 포함 단계별 최초 오류 보존”이 불완전합니다. l20은 precheck/start/postcheck만 다룹니다. 기존 경로를 거부하는 의도적 SystemExit와 예상 밖 준비 I/O 오류도 구분해야 합니다.

정정 조건: 준비부터 최소 실패 상태를 확보하고, meta 저장 자체가 불가능할 때도 원 오류를 유지하는 외부 기록을 고정하세요. 준비 실패의 launched=false·외부 rc·기록 위치를 대조안에 연결해 주세요.

### V2-05 · P2 · 단계별 소스 해시 기록의 생성 책임 누락

근거: A:115–117; S:165 및 실행기 전체; 제공된 대조 파일들.

요청은 01_red.source_sha256.txt와 02_green.source_sha256.txt를 필수 산출물로 나열하지만 실행기는 만들지 않습니다. 제공된 단계 설명·시험 소스에도 두 파일의 작성 명령·대상 집합·시점·실패 처리가 연결되어 있지 않습니다. 착수/끝 해시 표를 요구한다는 사실로 단계별 파일의 생성 책임이 정해지지는 않습니다.

정정 조건: 수동 절차든 실행기든 생성 주체·정확 대상·시점·대조 기준을 고정하거나 제출 목록을 실제 기록 구조와 맞추세요. 저장소 전체에 그런 도구가 없다는 주장이 아니라 이번 고정 승인안의 연결 누락입니다. 사전 봉인을 끝 diff로 대체하지 않는 원칙은 유지합니다.

## 3. 미래 E1-2에만 해당하는 사항

### FUTURE-01 · P2 · 사전 Git 문맥과 실제 fetch 문맥이 다름

근거: L:384–417,477–481; reil_c4e_run.py:665–669,688–706; C:614–638.

fetch 전 config/URL 검사는 WORK에서 수행하지만 실제 fetch는 새 data/git 저장소 문맥입니다. includeIf의 gitdir 조건은 실제 .git 위치에 따라 달라집니다. [Git 조건부 설정](https://git-scm.com/docs/git-config#_conditional_includes)

data/git/.git에만 적용되는 포함 파일에 http.sslVerify=false가 있으면 WORK 검사에서 보이지 않고 실제 fetch에서 활성화될 수 있습니다. 사후 검사는 URL·shallow·alternates만 확인하므로 이 설정을 놓칠 수 있습니다. 조건부 URL rewrite라면 사후 차단돼도 다른 출처에 접근한 뒤입니다. 공개된 “실제 TLS 연결 호스트 미관측”과 다른, 금지 설정 차단 누락입니다.

현재 E1-0에서 실자료 fetch를 한다는 뜻은 아닙니다. 이 항목으로 E1-0 범위를 확대하지 않습니다. 다만 미래 E1-2를 같은 고정본으로 실행 가능하다고 종결하지 마세요. 실제 저장소의 조건부/template 설정을 부작용 전 배제하거나 결속해야 하며 사후 검사만으로 사전 차단을 대신할 수 없습니다.

## 4. 이전 지적의 종결 범위

| 항목 | 이번 판정 |
|---|---|
| N1 | 정적 보완 수용 가능. leaf package/extension 차단·명시 parent locations 조회·origin/loader 결속·l15/l16 확인. 기능 NOT_RUN. |
| N2 | launcher unknown 보존 개선. 외곽 V2-01 때문에 전체 종결 불가. |
| N3 | kill 결과·유한 wait·단계 기록 개선. 준비 예외 V2-04가 남아 부분 수용. |
| N4 | launcher 환경 정제 개선. 현재 V2-02와 미래 FUTURE-01 유지. |
| N5 | subreaper·별도 세션 후손 처리 설계 개선. V2-01/V2-03으로 종결 불가. |
| N6 | E1-0/실제 E1-1–3 및 24/51 활동 구분 수용. V2-05 기록 책임 보완 필요. |
| S1 | 추가 실행 소스·manifest→lock→env_profile 해시 연결과 대조 설계 정적 수용. |

N1 수동 finder 조회는 importlib.util.find_spec의 자동 부모 import 방식과 다릅니다. 표준 finder에 명시 경로를 넘기는 의미는 공식 문서와 부합합니다. custom finder/sitecustomize 신뢰 및 probe→실행 TOCTOU까지 없앤 것은 아니며 요청서도 이를 남깁니다. [Python 3.11 importlib](https://docs.python.org/3.11/library/importlib.html#importlib.abc.MetaPathFinder.find_spec)

S1의 reil_c6_profile.py와 env_profile.py 크기·SHA, 실제 MANIFEST·lock 바이트, lock 첫 줄의 env_profile SHA는 고정 커밋 파일과 일치합니다. 설치 환경 실행 성공을 확인한 것은 아닙니다.

## 5. 대조 계획과 승인 질문

34개 최상위 launcher/골격 함수의 이름·서명, 공유 literal 상수, 골격의 NotImplementedError 종료를 AST로 확인했습니다. 새24+기존21+6=51은 계획 함수 수입니다. 24 RED나 51 GREEN을 실제 관측하지 않았습니다.

새24는 실제 다섯 실행 모듈 import를 제외하지만 전체 GREEN은 실제 import·합성 run.run 두 경로·plan_e·fork·로컬 Git/fetch 대조를 포함합니다. A:125–129의 구분은 기존 소스와 부합합니다.

외곽 timeout 무시험은 공개된 범위이므로 그 사실만으로 새 결함을 더하지 않습니다. 그러나 정상 RED/GREEN의 끝 잔존0만으로 V2-01/V2-03을 검증할 수 없습니다. 정정안에는 오류 뒤 정상 관측·정리 기한·첫 Git 전 환경 격리·준비 실패 기록의 정확 기대 결과가 필요합니다. 실행 대조를 추가한다면 수·명령·SHA·예산을 다시 제시하고 승인받아야 합니다. 24/51에 숨은 대조를 넣지 마세요.

- Q1: N1 정적 종결 가능, N2–N6 일괄 종결 불가.
- Q2: S1 정적 결속 수용 가능.
- Q3: 현재 계획만으로 확인된 외곽 실행기 잔여를 수용하기 어려움.
- Q4: 현재 고정본의 E1-0 승인 단계 진행 보류 권고.
- Q5: 미래 E1-2에는 FUTURE-01을 별도로 유지.

시작 Git 기록 실패 뒤 child를 실행하는 경로는 존재합니다. 그러나 R:47이 사후 stage=false 처리를 명시하고 l21도 이를 기대하므로 별도 새 범위 위반으로 세지 않았습니다.

또한 /proc PID/ppid 스캔은 비원자적이며 번호 기반 kill은 안정된 생성 신원을 계속 보장하지 않습니다. 이를 모든 자손의 연속 소유·종료 증명으로 확대하지 마세요. 실제 사고나 실행시험을 관측했다는 뜻은 아닙니다.

## 6. 자료 대조·보존과 수행 경계

고정 커밋 19개 사본의 Git blob 식별과 로컬 바이트가 일치합니다. 기존 실행 모듈5·시험2·SOURCES.json은 이전 보존본8개와 바이트가 같습니다. 다섯 실행 모듈은 SOURCES의 크기·SHA와도 같습니다. Python 3.11 문법 AST 대상은13개이며 기능 실행이 아닙니다. 상세 수치는 STATIC_CHECKS.json이 기준입니다.

선택 로컬 입력12개는 제출 문서2·이전 회신/판정2·이전 소스8개입니다. 보존 원점은 소스 읽기 이후·회신 작성/포장 이전입니다. 원격 Linux 작업 트리나 전체 PC 전후 불변 감사가 아닙니다.

검토자 자체 자료 도구의 AST 상수 해석 오류를 정정했습니다. REVIEWER_DATA_TOOL_NOTE.json에 원인·범위를 남겼습니다. 받은 프로그램 기능 실패·재시험 또는 E1 재시도가 아닙니다.

문서 작성 스킬에 따라 수용·잔여 지적·권한을 별도 회신으로 정리했습니다. 원본·후보·계약·원격 저장소는 수정하지 않았습니다. 받은 코드 import/시험/probe, Git fixture, 원자료 fetch/open, optimizer, COMSOL, 환경 변경, commit/push 및 외부 발송은0회입니다. GitHub 고정 소스와 공식 문서는 열람했습니다. 숫자 검토 예산이나 전체 소요 준수 주장은 없습니다.

이번 회신 자체는 정정 구현이나 E1-0 실행을 승인하지 않습니다. 권고 흐름은 비활성 정정안 → 갱신 식별/계획 재검토 → 명시적 E1-0 승인 → 결과 검토 → 별도 E1-1–3 승인입니다.
