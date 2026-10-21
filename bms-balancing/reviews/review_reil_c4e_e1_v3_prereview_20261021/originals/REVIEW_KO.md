# REIL C4E E1 v3 사전 검토 — 정정 후 재검토

2026-10-21 · 판정: CHANGES_REQUIRED_NO_EXECUTION

현재 E1-0 승인안은 그대로 실행하도록 권고하지 않습니다. 정정 필요 사항은 P2 네 건이며, 별도 P3 문구 불일치 한 건이 있습니다. 이 판단은 코드·문서의 정적 경로 검토입니다. 후보를 실행해 결함이나 GREEN 결과를 관측했다는 뜻이 아닙니다.

사용자의 “ultra로 봐줘” 요청에 따라 종료/시간, 봉인/Git 경계, RED/GREEN 대조를 각각 ultra 심도 독립 검토한 뒤 주 검토에서 교차 확인했습니다. 첨부 승인문은 검토 대상이지 실행 지시가 아닙니다. 문서 작성 스킬은 원본을 바꾸지 않는 별도 회신 구성에만 적용했습니다.

## 1. 식별과 실제 검토 범위

- 저장소: yonghoon7153-source/Yonghoon-DEM-DFT
- 고정 commit: 0c9c48e8c5b55bd7b9355fdba5a6833c01fabfb8
- 첨부 요청서·전달문 2개는 위 commit의 동명 파일과 바이트 동일합니다.
- 고정 commit에서 21개 파일을 읽었고 모두 Git blob SHA-1을 재계산해 수신 식별과 대조했습니다. 파일별 SHA-256/크기는 SOURCE_IDENTITIES.json에 있습니다.
- 코드 15개는 텍스트 AST로만 파싱했습니다. 새 초안 5개의 최상위 함수/클래스 145개 원문 span을 기록했습니다.
- 자체 자료 검사 105조건은 모두 일치했습니다. 이는 후보 기능 시험 수가 아닙니다.
- v2에서 보존한 공통 참조 13개와도 바이트 동일합니다. 다섯 모듈, 기존 시험 둘, 추가 실행 파일 둘, SOURCES, v2 runner, MANIFEST, lock을 포함합니다.
- 코드·원문·원격 저장소를 수정하지 않았습니다. 받은 프로그램 import/호출/시험, fixture, 탐침, 실제 /proc·process/Job 실험, 원자료·optimizer·COMSOL 실행은 0회입니다. GitHub/공식 문서 읽기와 자체 자료 도구 실행은 이 0회에 포함시키지 않습니다.

## 2. 현재 E1-0의 정정 필요 사항

### V3-01 · P2 — 공유 정리 기한이 새 관측과 복구 경로에 끝까지 전달되지 않음

근거: [runner watch/settle](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/0c9c48e8c5b55bd7b9355fdba5a6833c01fabfb8/bms-balancing/docs/REIL_C4E1_STEP_RUNNER_DRAFT_v3_20261021.py.txt#L290), [timeout 정리](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/0c9c48e8c5b55bd7b9355fdba5a6833c01fabfb8/bms-balancing/docs/REIL_C4E1_STEP_RUNNER_DRAFT_v3_20261021.py.txt#L319), [예외 후 cleanup 재호출](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/0c9c48e8c5b55bd7b9355fdba5a6833c01fabfb8/bms-balancing/docs/REIL_C4E1_STEP_RUNNER_DRAFT_v3_20261021.py.txt#L431). 승인요청 56행과 runner 13–17행은 같은 15초 기한, 기한 전에 시작한 관측 한 번의 초과만 허용합니다.

watch는 관측을 시작한 다음에 시간을 확인합니다. timeout 루프도 같습니다. 기한이 지난 상태로 settle에 들어와도 첫 관측을 시작하고, 살아 있는 자손이 남으면 kill 뒤 관측을 다시 시작합니다.

정적 반례: 정리 시작 후 6.9초에 시작한 timeout 관측이 15.9초에 끝나며 자손이 살아 있다고 반환합니다. 그 뒤에도 settle의 새 관측 및 kill 뒤 새 관측이 시작될 수 있습니다. 이는 이미 진행 중인 관측 하나의 초과만 허용한다는 설명보다 넓습니다. 정상 루프에서도 sleep으로 기한에 도달한 다음 새 관측을 시작합니다.

또한 첫 cleanup이 늦게 예외를 내면 cl은 None이므로 435행에서 cleanup을 다시 부릅니다. 319행은 다시 현재 시각+15초를 부여하고, 돌아온 cleanup_s는 첫 호출에서 소비한 시간을 포함하지 않습니다. 총 total_s가 존재해도 정리 단계 배정의 재설정은 해결되지 않습니다.

최소 보완: 단계에 속하는 정리 원점·절대 기한을 최초 한 번 만들고 복구에도 전달하십시오. 새 관측/대기 착수 전에 남은 기한을 검사하고, 초과 후 허용할 조치와 미완 기록을 명시하십시오. 관측 비용이 0이 아닌 가짜 시계와 늦은 정리 예외를 대조에 넣어야 합니다. r3의 시계는 sleep/wait만 진행하므로 현재 반례를 잡지 못합니다. 여기서 새 시험을 실행하도록 승인하지는 않습니다.

### V3-02 · P2 — 끊어진 meta 링크가 “기존 기록이면 자식 0” 거부를 통과함

근거: [launcher 기존 기록 검사](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/0c9c48e8c5b55bd7b9355fdba5a6833c01fabfb8/bms-balancing/docs/REIL_C4E1_LAUNCHER_DRAFT_v3_20261021.py.txt#L701), [runner 기존 기록 검사](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/0c9c48e8c5b55bd7b9355fdba5a6833c01fabfb8/bms-balancing/docs/REIL_C4E1_STEP_RUNNER_DRAFT_v3_20261021.py.txt#L377), 각각 마지막 meta 쓰기 769행/454행. 승인요청 66행·l12/r7(d)는 기존 기록이면 쓰기와 자식 실행이 없어야 한다고 정합니다.

두 검사는 Path.exists()만 사용합니다. 다른 조건이 정상인 입력에 <단계>.meta.json을 존재하지 않는 대상을 가리키는 symlink로 미리 두면 검사 결과는 false입니다. 메타는 자식이 끝난 뒤 마지막에 쓰므로, 자식 및 앞선 기록 생성이 진행된 뒤 exclusive open에서 실패해 rc4가 됩니다. 경쟁 상태 없이 성립하는 경로입니다.

Python의 exists는 링크 항목 자체가 아니라 대상 존재를 따릅니다. [Python 3.11 pathlib](https://docs.python.org/3.11/library/pathlib.html#pathlib.Path.exists)

최소 보완: lstat 기반 항목 존재 확인 또는 동등한 링크 포함 검사로 기존 항목을 작업 시작 전에 거부하고, l12와 r7(d)에 dangling-meta 입력을 추가하십시오. open x가 덮어쓰기는 막습니다. 이 지적은 덮어쓰기 성공이나 정상 수용 오판이 아니라 실행 전 거부 실패입니다.

### V3-03 · P2 — /proc 디코딩 예외가 누적 오류 기록에 들어가기 전에 빠져나감

근거: [runner proc_table/observe](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/0c9c48e8c5b55bd7b9355fdba5a6833c01fabfb8/bms-balancing/docs/REIL_C4E1_STEP_RUNNER_DRAFT_v3_20261021.py.txt#L203), [launcher proc_members](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/0c9c48e8c5b55bd7b9355fdba5a6833c01fabfb8/bms-balancing/docs/REIL_C4E1_LAUNCHER_DRAFT_v3_20261021.py.txt#L580). runner의 읽기 214행 catch는 OSError뿐이고, launcher 592–598행도 같습니다.

Path.read_text의 엄격한 디코딩에서 UnicodeDecodeError가 나면 뒤의 숫자 파싱 catch까지 도달하지 않습니다. 예를 들어 UTF-8로 디코딩할 수 없는 프로세스 이름이 stat에 있으면 이런 경로가 가능합니다. Linux 이름은 바이트 길이 제한의 문자열이고 stat의 comm에 노출됩니다. 이 가능성은 문서와 코드에서 추론한 것이며 이 기기에서 관측한 상태가 아닙니다. [PR_SET_NAME](https://man7.org/linux/man-pages/man2/PR_SET_NAME.2const.html), [/proc/pid/stat](https://man7.org/linux/man-pages/man5/proc_pid_stat.5.html), [Path.read_text](https://docs.python.org/3.11/library/pathlib.html#pathlib.Path.read_text)

같은 스캔에서 먼저 PermissionError를 errors에 담았더라도, 뒤의 PID에서 디코딩이 실패하면 proc_table이 반환하지 못해 observe의 ledger 추가가 실행되지 않습니다. 일시적 디코딩 실패 뒤 복구가 성공하면 cleanup.status는 empty일 수 있으며, 앞선 관측 오류는 사라집니다. 지속 실패면 두 cleanup 호출 모두 나머지 자손 처리 전에 중단될 수 있습니다. launcher도 그룹 관측을 마치지 못합니다.

외곽 errors가 전체 실패를 남기므로 runner_ok가 true가 된다는 지적은 아닙니다. 문제는 관측 오류의 완전한 보존과 자손 정리의 중단입니다. 기존 r1/r2는 이미 만들어진 오류 목록을 주입하므로 reader 자체의 이 실패는 다루지 않습니다.

최소 보완: PID별 읽기/디코딩 경계에서 오류를 보존하고 이전 오류를 잃지 않게 하십시오. 바이트 기반 파싱을 택한다면 파싱 불가와 PID 소멸을 구별해야 합니다. 앞선 오류 + 뒤의 디코딩 실패 + 후속 정상 관측의 순서를 대조에 고정하십시오.

### V3-04 · P2 — 수동 시작·끝 Git 기록은 정제 환경을 거치지 않음

근거: [승인요청 152–155행](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/0c9c48e8c5b55bd7b9355fdba5a6833c01fabfb8/bms-balancing/docs/REIL_C4E_E1_APPROVAL_REQUEST_v3_20261021.md#L152). 00_start/00_porcelain_start/04_porcelain_end/04_end의 고정 명령은 raw git -C이고, 상속 GIT_*의 제거 또는 착수 거부가 없습니다.

실행기 base_env는 그 프로세스와 자식에게만 적용됩니다. 부모 셸에서 실행하는 앞뒤 수동 명령을 정제하지 않습니다. GIT_DIR/GIT_WORK_TREE가 다른 저장소를 가리키면 이 기록의 HEAD/status는 다른 저장소의 것이 될 수 있고, GIT_TRACE가 허용 밖 파일을 가리키면 그곳에 기록을 시도할 수 있습니다. -C는 cwd 변경이며 이 환경변수를 무효화하지 않습니다. [Git 환경변수와 -C](https://git-scm.com/docs/git#_environment_variables)

최소 보완: 수동 기록도 같은 환경 정제 책임자와 정확 argv/cwd를 사용하거나, 해당 상속 상태에서는 첫 수동 Git 전에 중지하도록 고정하십시오. l25/r4/r6의 코드 경로 수정은 수용 가능하지만, 새로 구체화된 전체 기록 절차의 이 경로는 별개입니다. Git 설정 전체 격리나 향후 E1-2 FUTURE-01의 조기 구현을 요구하는 지적은 아닙니다.

## 3. 별도 문구 불일치

### V3-N1 · P3 — S4 first_error 설명과 runner의 실제 기록 위치

[승인요청 61행](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/0c9c48e8c5b55bd7b9355fdba5a6833c01fabfb8/bms-balancing/docs/REIL_C4E_E1_APPROVAL_REQUEST_v3_20261021.md#L61)은 launcher와 runner 모두 첫 오류가 record/GitRecordFailed라고 적습니다. launcher는 731–733행에 해당 기록을 만듭니다. runner는 [401–404행](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/0c9c48e8c5b55bd7b9355fdba5a6833c01fabfb8/bms-balancing/docs/REIL_C4E1_STEP_RUNNER_DRAFT_v3_20261021.py.txt#L401)에서 시작 Git 실패를 problems에만 넣고 449행 first_error는 errors에서 만듭니다.

Git가 오류 rc를 정상 반환하면 started=false·외부 반환 3(meta.rc=null)·problems 기록은 남지만 errors=[]·first_error=null입니다. r7(e)도 차단과 problems만 검사합니다. 자식 차단은 작동하므로 안전성 차단 실패로 확대하지 않습니다. 문구를 실제 기록 위치로 좁히거나 구현·기대값을 문구에 맞추면 됩니다.

## 4. 수용 가능한 정정과 남은 경계

| 기존 항목 | v3의 정적 상태 |
|---|---|
| V2-01 오류 보존 | 일반 목록/읽기 OSError·숫자 파싱 오류의 공통 ledger 연결은 개선됨. V3-03 디코딩 경로는 남음. |
| V2-02 Git 환경 | runner·launcher·fixture의 지정 코드 경로는 연결됨. 전체 수동 기록 절차는 V3-04 보완 필요. |
| V2-03 15초 | sleep/wait 남은 시간 사용과 시간 필드 분리는 개선됨. V3-01 때문에 종결 불가. |
| V2-04 준비 예외 | mkdir·자기 해시·disk 등 지정 예외와 meta 불가 fallback은 연결됨. V3-02 기존 항목 판정은 남음. |
| V2-05 소스 해시 | TARGETS 14·세 단계 EXPECT·사전 거부·사후 판정·두 해시 파일 생성자 연결을 정적으로 확인함. |
| N1·S1 | 가림 검사 및 추가 실행 파일/봉인 결속의 수용 범위 유지. 이번 바이트 대조도 일치. |
| S2·S3·S4 | 시간 필드 분리·fixture 첫 Git 전 격리·시작 Git 실패의 자식 차단 확인. S4 문구만 V3-N1. |
| FUTURE-01 | 별도 E1-0b 및 E1-1–3 승인 전 해결 조건으로 분리됨. 지금 E1-0에 미래 실행 준비 완료를 요구하지 않음. |

공개한 기록용 Git 설정 상속, 해석기/pytest helper 신뢰, /proc 비원자성·PID 번호 재사용, zombie와 비-zombie 구분, TOCTOU는 이번에 새로운 발견인 것처럼 중복 계산하지 않았습니다. launcher의 미래 명목 20초와 현재 외곽 runner의 15초 요구도 구분했습니다.

## 5. 대조 수와 RED/GREEN의 의미

정적 함수 수는 기존 21 + N1 6 + 새 launcher 26 + 새 runner 8 = 61입니다. 이를 늘리는 parametrization/decorator는 없습니다. 새 34개에는 하나의 함수 안에 여러 하위 시나리오가 있으며, r6–r8의 driver 실행 계획은 총 7회입니다. 이는 “시험 함수 하나=사례 하나”라는 문서 정의와 모순되지 않습니다.

RED-L의 26개는 골격 NotImplementedError에 도달하는 구조입니다. RED-R r1은 v2의 첫 오류 유실을 겨냥한 AssertionError이고 r2–r8은 부재 인터페이스의 AttributeError라는 선언과 부합합니다. 인터페이스 수준 RED임을 공개했으므로 그 자체를 결함으로 세지 않습니다. GREEN 새 34개의 기대값에서 확정적인 정적 불일치는 찾지 못했습니다. 어느 것도 실행 PASS를 뜻하지 않습니다.

현재 대조가 위 네 반례를 모두 막지는 못하므로, 예정대로 61개가 나중에 통과하더라도 그 수만으로 해당 결함을 종결할 수 없습니다. 보완 후 사례 수·실제 입력·기대 이유·호출 경로·해시를 다시 고정해야 하며, 구체 새 개수는 작성 전에 임의로 정하지 않습니다.

## 6. 다음 전달과 권한

Claude에는 CODEX_REPLY_KO.txt와 이 보고서를 전달하면 됩니다. 다음 요청은 위 항목을 반영한 비활성 초안·문서 정정본이며, 이번 회신 자체는 수정 실행·E1-0 시험·커밋·push·E1-1–3 실행을 승인하지 않습니다. 수정과 시험의 사전 권한은 각각 사용자 범위에 맞춰야 합니다.

원 REIL 코드·기존 증거·v1/v2/v3 제출 원본은 보존합니다. 별도 COMSOL microshort의 JOB_CURRENT_COMMIT/계약 미채택/native_ready=false 경계와 이번 REIL E1-0 검토를 합치지 않습니다.

## 7. 검토 도구와 보존의 한계

자체 SHA/JSON/AST 자료 도구만 실행했습니다. 별도 텍스트 diff 출력에서 콘솔 cp949가 em dash를 인코딩하지 못해 1회 rc1이 있었고, 자체 출력 UTF-8 설정으로 다시 읽어 rc0을 얻었습니다. 후보 시험 실패/재시험이 아니며 소스 변경은 없었습니다. 원도구 식별은 ACTIVITY_NOTES.json에 남겼습니다.

SELECTED_REVIEW_INPUTS_BEFORE/AFTER의 23개는 첨부 2개와 이 검토의 pinned 사본 21개입니다. BEFORE는 초기 읽기·자료 검사 후, 회신 작성 전 경계입니다. 원격 Linux 작업 전체의 불변성이나 과거 실행의 독립 감사를 주장하지 않습니다. 수신 문서에 적힌 과거 실행 수·환경 관측·승인 이력은 저자의 기록이지 이번 검토자의 OS 재관측이 아닙니다.
