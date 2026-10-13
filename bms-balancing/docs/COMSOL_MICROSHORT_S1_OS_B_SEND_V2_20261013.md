# S1 OS B 오프라인 준비 발송문 v2 초안

2026-10-13 · 검토 정정 반영본 · 사용자 미채택 · 실행용 승인 파일 아님

**현재 approved=false / usable=false / native_ready=false다.** 아래 문서 묶음 식별을 채우고 사용자에게 이 문서 전체 범위의 명시 승인을 받은 뒤에만 실행 담당자에게 작업 지시로 보낸다. 문서 수신·검토만으로 승인하지 않는다.

## 0 사용자 채택 전 필수 항목

권고 경로는 **(b) 별도 기계에서 받은 Microsoft 공식 문서 사본 묶음을 전달하고 실행 PC는 네트워크 0 유지**다. 이 초안은 문서 수집·네트워크·자동 발송도 승인하지 않는다.

- 공식 문서 묶음 파일명: `COMSOL_S1_OS_B_OFFICIAL_DOCS_20261013.zip`
- 파일 크기: `525600` B
- SHA256: `6579d317bfe43129e7364c973882912f95d29c8b0031115f6263fb82d1207dd6`
- 묶음 내 manifest SHA256: `8ce680e44907fa710e64ccfedc5ec7c57b83ceba22629e105d721c0389e81253`
- 본 v2 최종 식별 및 사용자 채택: `PENDING`

하나라도 미기입이면 착수하지 않는다. 문서 수집 범위 결정 → 묶음 생성/확인 → 실제 식별을 넣은 최종 v2 → 사용자 채택 → 실행 담당자 전달 순서다. 묶음에 없는 자료가 필요하면 임의 네트워크·SDK 설치로 보충하지 않고 해당 근거/기능을 OPEN으로 남긴다.

사용자가 나중에 채택할 문구:

> 식별이 완성된 이 문서의 S1 OS B 오프라인 준비 1건만 승인합니다. 공식 근거 대응, 새 비활성 provider 후보와 최소 diff, 변경부 검증안 작성·정적 봉인 후 멈춰 주세요. 자체 정적 자료 도구와 본문에 열거된 메타데이터 읽기를 허용합니다. 후보/수신 코드 실행, 기능 시험, 시험/native 자식·Job 및 실제 자원/중지 어댑터 실험, COMSOL/JVM/컴파일, 설치본 관측, 정책 변경, 실제 승인/release/runtime/token 생성은 승인하지 않습니다. 이후 변경부 검증·E·C·P0는 각각 별도 승인입니다.

이 인용문은 **승인 초안**이다. 현재 사용자가 승인했다고 전사하거나 승인 JSON으로 만들지 않는다.

## 1 고정 기준과 쓰기 경로

| 대상 | 식별 |
|---|---|
| OPEN-R1 CODE_MANIFEST | 2,820B · 14구성원 · `feb12ef6991141aab59fd2fbc0d5f0d138bdd735255aa7123274503ce80b8ecc` |
| resource_connection | 10,846B · `f45e6531383d03daa2e968437c6188be0229c144c6956647b0b0f81fae795816` |
| OS_API_MATRIX | 4,115B · `ec3ab0c209a5aab458fada593c31c63b73f6eec43b902a718823a2391d57622c` |
| RESOURCE_CONTRACT | 7,175B · `e45837427b1b8a69d53b10119ce7ab072bacb869bcdd53c863366c7bd04c67c1` |
| 기존 수용 회신 ZIP | 38,949B · `879cff578dfa52a7dcf0c008cded5f42698bb3b2916570b9e4b5da0b31e10d17` |

기준 root는 `C:/Users/BML/Documents/Codex/2026-09-13/files-mentioned-by-the-user-comsol63/outputs/microshort_s1_open_connection_r1_20261010/`다. RESOURCE_CLOCK_CONTRACT 및 실제 소비할 legacy 파일의 정확 경로·크기·SHA를 시작 선택 목록에 추가한다. 원본·계약·원 R1·consumer/control/Parent/legacy source를 수정하지 않는다.

새 쓰기는 아래 폴더 한 곳만 허용하는 제안이다.

`C:/Users/BML/Documents/Codex/2026-09-13/files-mentioned-by-the-user-comsol63/outputs/microshort_s1_os_b_prep_20261013/`

이미 있으면 덮어쓰기·삭제·재사용·다른 이름 우회 없이 중지한다. 변경할 소스는 새 폴더의 비활성 사본만 작성한다. 실제 배치·실행 경로·argv/cwd/approval 경로를 활성화하지 않는다.

## 2 허용 도구와 관측 경계

사용자 채택 시 허용할 범위는 다음과 같다.

- 자체 자료 도구로 텍스트/JSON/ZIP 읽기·작성, 해시/집합/크기/CRC/byte diff·정적 구문 분석·포장·시각 기록. AST를 실행기로 쓰거나 후보를 import하지 않는다.
- OS 판·빌드·아키텍처의 읽기 전용 식별 1회. 사용 명령·출력·시각을 기록한다. 이 관측을 target API 지원 PASS로 바꾸지 않는다.
- ABI 설명에 필요한 준비 도구/향후 adapter 비트수는 기존 식별 또는 실행 파일 메타데이터의 읽기로 연결한다. 불명은 UNVERIFIED이며 별도 engine/version probe나 ABI 호출 실험을 하지 않는다.
- 새 폴더 시작 디스크 여유와 파일/폴더 메타데이터, 진행 시간·자체 산출 크기 확인. 실제 자원 감시 provider의 주기 관측 시험은 아니다.
- 이미 지정된 로컬 COMSOL 6.3 도움말의 관련 텍스트 읽기만 가능하다. 앱/엔진을 띄우거나 새 도움말 설치·외부 지원 발송을 하지 않는다.

금지하는 실행은 **후보·수신 코드의 import/함수 호출, 기능 시험, 시험용/native 자식·실제 Job 생성, 실제 counter/Job 설정·조회/중지 어댑터 실험, COMSOL/JVM/컴파일**이다. 자체 셸/Python 자료 도구 사용은 별도 기록하며 “일반 프로세스 생성 0” 또는 “모든 OS API 호출 0”이라고 보고하지 않는다.

## 3 공식 근거 대응표

첨부한 고정 묶음만 읽는다. 각 행에 API/DLL·information class·구조체/필드·단위·권한·ABI·반환/오류 의미·최소 OS·문서 절·사본 SHA와 근거 등급을 적는다. 문서 확인, 프로젝트 소스 참고, 미확인, 실제 관측 NOT_RUN을 구분한다.

묶음 제작자가 먼저 고정할 범주는 다음과 같다. 전체 SDK를 받으라는 뜻이 아니며 실제 후보가 사용하는 의존 문서만 포함한다.

1. RSS: GetProcessMemoryInfo, PROCESS_MEMORY_COUNTERS_EX, 필요한 process handle 권한.
2. host commit/RAM: GetPerformanceInfo, PERFORMANCE_INFORMATION. 기존 GlobalMemoryStatusEx 경로를 재사용하면 GlobalMemoryStatusEx와 MEMORYSTATUSEX도 포함한다. PageSize 변환·물리 RAM과 commit 구분을 명시한다.
3. Job: Query/SetInformationJobObject, BASIC/EXTENDED_LIMIT_INFORMATION, BASIC_PROCESS_ID_LIST, Create/Assign/IsProcessInJob, Job access rights와 nested/breakaway 의미.
4. process/handle: 사용 예정인 CreateProcess/creation flags, OpenProcess, GetProcessTimes, ResumeThread, WaitForSingleObject, GetExitCodeProcess, CloseHandle 및 오류 코드 보존.
5. 시계: 사용하는 단조 시계와 단위/주파수 근거. QPC/QPF 경로면 해당 두 문서. 실행기 wrapper를 쓰면 그 wrapper가 어떤 시계에 연결되는지도 명시한다.
6. 디스크/산출: GetDiskFreeSpaceExW의 caller-available/volume-free 의미와 실제 사용하는 bounded metadata walk·reparse 확인의 근거.
7. 강제 종료: TerminateJobObject, KILL_ON_JOB_CLOSE. 협조적 COMSOL 중지는 별도 로컬 근거와 연결하며 없으면 UNVERIFIED다.

Job 현재 commit의 공개 지원 계약이 확인되지 않으면 OPEN으로 남긴다. Microsoft 프로젝트 소스의 class28 선언은 공개 Win32 지원/최소 OS/계수 의미와 동등하지 않다. 현 Learn 목록에 임의로 소스를 추가하거나 그 class를 채택하지 않는다. peak·notification 시점 값·구성원 합·host commit으로 현재 Job commit을 대체하지 않는다.

문서 미확인은 예상 가능한 OPEN 결과다. 문서 파일 손상·식별 불일치·읽기 도구 오류 등은 다음 절의 중지 규칙을 따른다.

## 4 비활성 후보와 연결 표

OS_API_MATRIX의 행마다 후보 또는 OPEN 이유를 남긴다. 문서로 지원되지 않는 동작은 stub이 PASS를 반환하게 만들지 않는다.

- **소유권:** 명시적으로 소유한 Job handle과 retained root/member handles, PID+생성시각을 연결한다. NULL ambient Job·기존 이름 Job 재사용·unknown PID 종료를 거부한다. root가 먼저 끝나고 소유 자식이 남는 경우도 분리한다.
- **시작과 상한:** 제한 설정/정확 readback·root 할당·소유 확인 전 Resume 금지를 계약화한다. breakaway·권한 완화·다른 launcher로 우회하지 않는다. 기존 launcher를 바꾸지 않으며 필요한 연결이 범위를 넘으면 OPEN으로 제출한다.
- **membership/RSS:** 용량·반환 수·길이·경합을 유한하게 처리한다. 같은 retained handle로 신원을 확인하고 고유 (PID,생성시각)별 WorkingSetSize를 한 번 합한다. shared page 중복 가능과 표본 사이 미관측을 밝힌다.
- **commit:** 현재 Job commit 10GiB 조기중지와 12GiB Job cap은 별개다. 기존 계약의 필수 현재값/mapping을 삭제하거나 0으로 채우지 않는다. 한도 초과 commit 거부를 자동 정상 종료로 표현하지 않는다.
- **host RAM/commit/디스크:** 단위·범위·quota 의미를 고정한다. query 실패·overflow·역전 값을 구조화해 미완으로 연결한다.
- **산출:** 본체·wrapper·temp·최종 기록 루트를 사전 열거하고 겹친 루트는 한 번만 센다. exact 또는 구분자 하위 경로만 포함한다. 유사 접두사 형제·reparse·교체 경합·미상 파일·권한 오류·walk 시간 초과를 처리한다. 원본 제외·삭제 금지다.
- **중지:** 지원된 협조 요청 → 기존 한정 대기 → 남은 소유 Job 강제 → 실제 종료 확인을 기존 상태기와 연결한다. 협조 미지원이면 force-only 승인 없는 native를 거부한다. Terminate 요청의 반환과 Job empty/root signaled/exit query 성공은 별개다. kill-on-close만으로 graceful 또는 정리 PASS를 만들지 않는다.
- **clock/session:** 독립 start_record·동일 ResourceSession·previous cursor의 소유자를 고정한다. compile/batch 생애주기와 Job/root 연결을 명시하며 표본마다 원점·session을 재생성하지 않는다.
- **최종 연결:** Parent.S1FinalReturn 본문은 유지하고 실제 child rc·clock·writer 연결점만 표시한다. 현재 수정 범위를 넘는 생산 연결은 OPEN으로 남긴다.

표본 규칙은 계약값을 그대로 쓴다. 요청/도착 시각을 남기고 도착 공백을 **cursor 갱신 전** 검사한다. 첫 지연·예외·값 없음은 따로 기록한다. 하나의 완전한 표본 transaction의 수집 시간과 gap을 검사하며, 마지막 느린 조회가 다른 값의 오래된 관측을 숨기지 못하게 한다.

마지막 필수 쓰기·재읽기·해시·산출 재측정 뒤 현재 시각으로 단계/전체 상한과 필수 관측 유효성을 재판정한다. child 정상 종료는 감시 실패를 해소하지 않는다. 활성 표본의 빈 Job은 가짜 0 표본이 아니며 별도 종료 확인 경로에서 처리한다.

## 5 변경부 검증안 작성만

새 함수·어댑터 경계에 한정한 계획을 제출한다. 실제 함수·실제 의존부·가짜 OS seam·필수/금지 호출 수·정확 이유·도달 경로·같은 분기 양성 대조를 묶는다. 실제 엔진/하네스/fixture/명령/사례 수/세션/예산은 후속 검증 승인 전에 봉인하도록 제안한다. 이번에는 검증을 실행하지 않는다.

검증안은 늦은 성공·첫 표본 지연·실패 후 cursor, 최종 write/hash 마감 초과, 느린 마지막 query와 다른 counter 최신성, PID 재사용·목록 경합, NULL/다른 Job, 상한 readback 불일치, root 선종료/자식 잔류, 빈 Job이나 exit query 실패, cooperative 미지원, 산출 루트 중복/유사 접두사/reparse/미상 항목을 해당 양성과 함께 다룬다. 기존 93개/130개 전체 반복은 기본 요구가 아니다.

## 6 예산과 보존

새 원점 총 3,600초이며 단계 상한은 근거 대응 600, 후보 작성 1,800, 정적 대조 600, 보존·전달 480, 미완 정리 120초다. 단계 사이 전용·자동 확대·재시도는 없다. 이것은 오프라인 준비 예산이며 기존 native 9,000초 계약을 바꾸지 않는다.

새 폴더 ≤50MiB, 시작 디스크 여유 ≥512MiB를 확인한다. 입수/사전 확인과 승인 작업 원점의 경계를 명시하고 승인된 준비 관측은 원점 뒤에 기록한다. 기존 14개 정정 구성원·소비하는 계약/legacy 파일·수용 회신·공식 문서 묶음의 선택 목록을 시작 때 고정하고 전후 크기/SHA로 대조한다. 새 파일을 원본으로 더 세거나 PC 전체 보존으로 확대하지 않는다.

첫 예상 밖 오류·식별/경로 충돌·미예정 변경·예산/크기 초과에서는 오류와 확보된 자료를 보존하고 중지한다. 남은 작업은 NOT_RUN이다. 수정 후 재시험·다른 shell/fallback·추가 권한·원본 삭제로 복구하지 않는다. 소유한 새 기록 안에 중지 이유를 남긴다.

## 7 제출 후 정지

결과 보고서, 근거 대응표, 비활성 후보·최소 diff, 변경부 검증안, code/package manifest, 선택 보존 기록, 시간 기록을 제출한다. ZIP 밖 영수증·포장 반환·포장 후 보존·최종 확인·최종 반환 전사를 한 번에 연결한다. 원바이트·snapshot·후속 전사의 범위를 구분하고 도구 wall time을 snapshot에 더하지 않는다. 자기 자신의 미래 반환까지 기록했다고 하지 않는다.

B는 ④ 전체를 종결하지 않는다. B 변경부 검증과 비-COMSOL E는 각각 별도 승인이며 E는 OS API 대응만 검증한다. COMSOL 협조적 중지 또는 별도 force-only 정책·통합 근거가 남는다. C의 실제 solve0 관측도 안전 조건을 우회하지 않는다.

D는 향후 승인될 한 P0 runAll 안에서 실제 t0·계수·raw 증거를 생성하는 단계다. 그 전에는 획득 경로·판정기·자원/중지 연결을 준비하고 그 후에 실제 증거를 수용한다. 현 경로로 증명 불가하면 승인 보류이며 추가 pre-P0 solve는 없다.

OPEN 4·native_ready/approved/usable=false·전체/정상 gate INCOMPLETE·실효 정책/실제 코어 UNVERIFIED와 `_001`의 `_003` 구간 보존 미확인을 유지한다. 12GiB cap 제거, 현재 commit 필수값 제거, force-only 채택, P0/P1–P3/K/장시간 실행·정책 완화·microshort 효과 주장은 범위 밖이다.
