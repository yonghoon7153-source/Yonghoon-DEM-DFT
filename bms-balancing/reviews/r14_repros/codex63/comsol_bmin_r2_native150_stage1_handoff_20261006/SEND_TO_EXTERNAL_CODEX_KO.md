# 외부 실행 기기 Codex에 보내는 BMIN150 1단계 작업지시

**B-min r2 native 150초의 1단계 읽기 전용 사전 관측과 최종 승인 요청문 작성을 진행해 주세요. 실제 계산을 시작하라는 지시가 아닙니다.** 이 작업은 COMSOL이 설치되고 기존 자료가 있는 BML 실행 기기의 기존 Codex 대화에서만 수행합니다. 다른 PC·클라우드에서 대신 측정하거나 경로를 바꾸지 마세요.

## 사용자 승인 범위

> B-min r2 native 150 s 의 1 단계를 이 문서 (bms-balancing/docs/COMSOL_BMIN640_R2_NATIVE150_APPROVAL_REQUEST_20261006.md) 의 범위로 승인합니다. Codex 는 실행 기계에서 §9 표 2 번 및 §9-1 의 읽기 전용 사전 관측만 하고 (쓰기는 §9-1 의 새 기록 폴더 하나 · 그 한도 안), 그 결과를 붙인 최종 승인 요청문을 만들어 주세요. approval / token / runtime · `future_authorizations/*` 생성과 COMSOL 실행은 최종 승인 뒤에만 합니다. 예산은 §6 그대로 (전체 10,500 s · 연장 없음 · 1 회), 실효 정책 UNVERIFIED 를 수용하고, 결과 MPH 는 식별만 보내고 수신 검토가 끝날 때까지 지우지 않습니다.

이번 작업에 적용되는 한도는 **1단계 벽시계 1,800초·기록 폴더 50 MB 이하·1회**입니다. 10,500초는 향후 실제 부모 실행의 예산이며 이번 관측에 전용하지 않습니다. 실제 실행과 그 뒤 별도 1,800초 포장은 이번에 시작하지 않습니다.

## 고정 문서와 자료

- 저장소: `yonghoon7153-source/Yonghoon-DEM-DFT`
- 정정 커밋: `e4e06889338f22df53e4d4ece9e29e1131570fad`
- 정정 문서: `bms-balancing/docs/COMSOL_BMIN640_R2_NATIVE150_APPROVAL_REQUEST_20261006.md`
- 문서 Git blob: `d1d80525ad725d924054e647f2f2238f7446b361`
- 후보 CODE_MANIFEST SHA: `4cdca2e6bf7d073f813d97be73825b8cd2043c2fc44e285f4a190bc6fb97cf25`
- 검토에서 요청한 N150-N1 PowerShell 식별 추가와 N150-N2 시간 원점·마지막 snapshot 정정이 이 커밋에 반영돼 있습니다. 동일한 문구 검토·한정 검증을 반복하지 않습니다.

첨부 `READONLY_REFERENCE_SNAPSHOT.json`에는 이 커밋의 정정 요청문과 후보 CODE_MANIFEST·CONTRACT·COMMAND_MAP·NATIVE_APPROVAL_FIELD_SPEC 원문을 데이터로 담았습니다. 명령을 실행하는 파일이 아닙니다. 기존 수신 자료와 함께 읽고 현지 파일의 현재 바이트를 대조하는 근거로만 사용하세요. 기준 9개 및 외부 의존 16개의 정확한 경로·크기·SHA는 이 CONTRACT를 따릅니다. 필요한 자료를 읽을 수 없으면 누락을 보고하고 멈추세요. 이번 승인으로 네트워크 fetch·설치·checkout·파일 배치를 하지 않습니다.

## 시작과 기록 위치

실제 관측을 시작할 때 UTC·현지 시각과 단조 시계 원점을 한 번 기록합니다. 기존 세션의 경과 시간이나 과거 예산을 재사용하지 않습니다. 도구 정책이 조회를 허용하지 않으면 권한·shell·보안을 바꿔 우회하지 않고 중지합니다.

쓰기 허용 위치는 다음 새 폴더 하나입니다.

`C:/Users/BML/Documents/Codex/2026-09-13/files-mentioned-by-the-user-comsol63/outputs/bmin640_native150_preexec_20261006/`

처음 확인했을 때 이미 있으면 쓰지 말고 그 사실을 대화에 보고한 뒤 중지하세요. 삭제·재사용·다른 이름 fallback은 없습니다. 없을 때만 이번 기록을 위해 만듭니다. 첨부 원자료·기준 CSV·MPH·후보 소스를 이 폴더로 복사하지 말고 식별만 기록합니다.

다음 영역은 만들기·고치기·옮기기·지우기·권한 변경을 하지 않습니다.

- r2 root: `C:/Users/BML/Documents/Codex/2026-09-13/files-mentioned-by-the-user-comsol63/outputs/bmin_particle640_offline_preparation_20261004/`
- NORMAL480 기준 경로와 `b020_profile_unit_stages_20260927/`
- `C:/Users/BML/.comsol/`, COMSOL 설치 폴더, Codex 런타임 Python
- r2 root 아래 `future_run_001`, `future_parent_001`, `future_authorizations/*`

## 읽기 전용 관측

새 기능 시험이나 엔진 probe가 아니라 기본 셸의 파일 읽기·속성·해시·목록·자원 조회만 사용합니다. 관측 명령·원 출력·시각·결과를 남기며, 기준과 관측을 서로 다른 필드에 적습니다.

1. 실행 기기의 실제 경로를 확인하고 r2 root의 manifest 및 5개 봉인 파일, COMMAND_MAP과 승인 필드 명세를 고정 근거와 대조하세요. root 부재나 v1/r1 바이트 충돌은 고치지 말고 기록하고 중지합니다. 필요한 배치 사항은 미완 2단계 초안에 적습니다.
2. `future_run_001`, `future_parent_001`, `future_authorizations/bmin640_001.json`, `VALIDATION_RELEASE.json`, `USER_DECISION.json` 다섯 경로의 부재를 확인하세요. 하나라도 있으면 중지합니다.
3. 계약에 적힌 NORMAL480 `future_run_001/tables/` 9개 파일의 현재 크기·SHA를 대조하세요. 더 짧은 과거 ZIP `baseline/`을 대용하지 않습니다. 대형 CSV 내용을 원문 기록에 덤프하지 않습니다.
4. 기본 prefs `C:/Users/BML/.comsol/v63/comsol.prefs`의 현재 크기·SHA와 `security.` 줄을 읽고 중복·현재 `security.external.enable=on` 조건을 기록하세요. 값을 바꾸거나 과거 SHA를 현재 관측으로 쓰지 않습니다. 다른 prefs 내용이나 무관한 개인정보는 기록하지 않습니다.
5. 외부 의존 16개, 고정 COMSOL 실행파일 둘, Python 실행파일의 현재 식별을 대조하세요. 파일을 import·실행하거나 버전 probe를 하지 않습니다.
6. `C:/WINDOWS/System32/WindowsPowerShell/v1.0/powershell.exe`의 현재 경로·크기·SHA를 읽어 부모 고정값 `8bb6fa8c283b4d92120b1ef249a9b311b0f804d4cabbe9981159976c8be76a5e`와 대조하세요. 불일치 시 중지하고 엔진·정책·부모 코드를 바꾸지 않습니다.
7. 가용 디스크·RAM·관련 COMSOL 프로세스 목록을 읽기 전용으로 관측하세요. 프로세스를 종료하거나 핸들을 조작하지 않습니다. 향후 native 시작 디스크 15 GiB 조건과 현지 관측을 비교하되, 새 RAM 하한·working-set 감시를 구현하지 않습니다. 관측할 수 없으면 UNVERIFIED로 남깁니다.

조회 오류·식별 불일치·경로 충돌·시간 또는 크기 초과가 나면 첫 오류와 확보한 기록을 보존하고 중지합니다. 자동 재시도·추가 probe·과거 시험 반복은 없습니다. 같은 관측을 성공할 때까지 반복하지 않습니다. 미완 정리·기록도 이번 1,800초 한도 안에서 수행하며, 초과 뒤 추가 쓰기 권한을 임의로 만들지 않습니다.

## 제출하고 멈출 것

허용 폴더 안에 사전 관측 원문, 항목별 대조 결과, 시작·종료 시각/경과·총 크기·예산 판정, 실제 측정 항목과 미확인 항목, manifest, **비활성 2단계 최종 승인 요청문**을 남기세요. manifest 자체를 자기 해시에 넣지 않습니다. 최종 파일 쓰기·재읽기 뒤 관측과 도구 반환은 구분하여 대화에 보고합니다. 이번 기록 작업을 완료했다고 원래 실행 전체 PASS로 바꾸지 않습니다.

2단계 초안에는 현재 관측된 식별, 필요한 배치 여부와 별도 허용 요청, 정확한 source/run/cwd/argv, 승인·release·사용자 결정의 생성 순서, native 1회·실패 중지·정리·보존·판정 범위를 연결하세요. 실제 승인 파일은 만들지 않습니다. 누락·불일치가 있으면 초안도 미완이며 실행 가능으로 표시하지 않습니다.

향후 실행 예산 설명은 부모 4행 Stopwatch 원점, 239행 POST_WRITE snapshot, 그 뒤 출력·STOP·프롬프트 복귀는 사후 실측 아님으로 유지합니다. POST_WRITE는 transcript 밖이므로 사용자의 화면 원문 보존이 필요하다는 조건도 남깁니다. NoExit의 OS rc를 만들지 않습니다. 포장은 부모와 별도 예산이며 이번에는 수행하지 않습니다.

**완료하면 요약과 파일 위치를 보고하고 반드시 멈추세요.** 2단계 요청문 작성 완료는 실제 계산 승인이 아닙니다. COMSOL/JVM/compile/batch/solve/loadCopy/Evaluate/Export, 부모·entry·동봉 코드·Python 실행본 실행, C2 입력 시험, 설정 변경, approval/token/runtime/USER_DECISION/VALIDATION_RELEASE 생성은 이번에 모두 금지합니다. 저장소 원장 수정·커밋·외부 발송도 하지 않습니다.

이 작업은 REIL·게이트 라운드와 분리합니다. PS01-16 내부 분기 UNOBSERVED, 실효 정책·실제 코어 UNVERIFIED, 전체/정상 gate INCOMPLETE, 기존 실패·pending·원복·recipient=null을 유지합니다. 960초 연장이나 추가 메시 축 시험은 포함하지 않습니다.
