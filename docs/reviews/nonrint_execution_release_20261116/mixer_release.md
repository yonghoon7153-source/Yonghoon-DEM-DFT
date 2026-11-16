# 승인 A/B V2 위 E0 한 팔 — 발사 도구와 블록

## 1. 승인본 보존과 역할

구현 핀 `6c1144cde6b3671be55b85c626044020ae1f734d`: `scripts/mixer_e0_pilot_ibb.py`, `scripts/test_mixer_e0_pilot_ibb.py`, `docs/reviews/mixer_e0_pilot_launch_20261116/runtime_reference.json`. 최종 실행 핀 `997aabe1b5a702e2f389007e3923018d778ce857`은 영수증의 등록 문서 문자열 한 곳만 리포 전체 경로로 정정한 후속 커밋이다. 최종 blob에서 아래20메서드를 다시 확인했다.

1저자가 승인한 A/B V2의 B 283파일 및 계획 자산40개를 반환 묶음과 다시 비교했다. 전부 같은 바이트다. 승인 B의 submit/job-start/봉인 코드를 바꾸지 않았다. source pin은 `8231f395cda98fed8dbbf5422ccda003b11a8da9` 그대로다. 새 도구는 승인 B 사본에 E0 전용 경로·권한 자료를 붙이고 기존 제출 가드를 한 번 호출한다. 새 운영 재봉인을 수행한 것이 아니다.

기준 계약: `docs/reviews/mixer_e0_pilot_registration_20261113/registration_candidate.md` §2–7·§11–12. 과거 초안의 비준 대기 표지는 당시 기록이며, 이번 A/B 승인과 발사 GO를 구별한다. **A/B 승인만으로 발사 GO를 생성하지 않는다.**

## 2. 1저자용 블록

외부 파일명: PASTE_MIXER_E0_IBB_ONE_ARM_20261116.txt. WSL에서 ssh/scp로 새 ibb 설치·한 잡 제출·감시·회수까지 이어진다. 접속 정보는 그 원문에만 있다.

| 항목 | 동작 |
|---|---|
| 발사 GO | 로컬 화면에서 GO_E0_ONCE를 직접 입력하기 전 원격 배포·제출 0. 원본 template의 execution_authorized는 false |
| 자원 | E0 · NP20 · 동시1 · CPU60 한도 · cpu/cpu-60 · 개발 자료 |
| 시간 | 예상 3.38–4.91h + I/O·대기 미정 · Slurm wall24h · 감시기 예산25h(대기 포함) |
| 중복 방지 | 고정 새 설치 경로가 이미 있으면 전체 블록 거부. 기존 승인 submit 가드의 예약·영수증·같은 팔 중복 거부 사용 |
| 신원 | 고정 tar·manifest·B283·AB12검사·source pin 대조. 바이너리/MPI/연결 라이브러리30 및 conda7묶음1011파일의 이전 메타 기준을 런 전·T9 대조 |
| 제출 전 | QoS·association·wall·CPU/동시성·공간/inode/OST·quota 읽기. live 수집10s 초과·실패는 재시도 없이 중단 |
| 진행 | 30s scheduler 조회 · 10min 관측. 숫자 step 진행·파일 증가·공간·로그 오류/입자 손실·quota 확인 |
| 멈춤 | STOP_RECOMMENDED와 해당 job ID의 중단 명령을 출력. 운영자가 중단한다. 자동 취소·재큐·재제출·예약 해제 없음 |
| 회수 | scheduler 끝·job_end·T9·전체 run/B 원천·control·증거를 새 반환 폴더에 묶음. report/full archive SHA256을 WSL에서 재검산 |
| 채택 | 수집 성공은 물리 자격 수용이 아님. T9 불일치·누락 및 등록 C1–C7/W9는 별도 판독. N0/B 팔 자동 전이 없음 |

자료를 받는 로컬 여유와 원격 여유는 각각 최소32,193,231,348 B부터 확인한다. archive는 case 폴더 밖에 작성한다. 최초 제출 전 거부 또는 런 실패도 가능한 report를 남기며 화면에 SUBMIT_RC·JOB_ID·RUNNER_RC·CONTROLLER_RC·REMOTE_ARCHIVE_RC·RETURN_RC를 표시한다. 제출 전 거부이면 JOB_ID/RUNNER_RC는 아직 없다.

SSH 단절·감시 실패·25h 초과는 작업 종료를 뜻하지 않는다. **기존 설치/예약을 지우거나 블록을 다시 제출하지 않고 같은 시도를 먼저 대조한다.** `--collect`는 기존 시도 확인 전용이며 새 제출을 하지 않는다. 이미 만들어진 반환 파일을 덮지 않으므로 완결된 회수의 임의 반복 명령으로 쓰지 않는다.

## 3. 시험과 알려진 한계

| 묶음 | 결과 | 해석 |
|---|---|---|
| 같은 신규19 / 이전 로컬 도구 | 3실패·2오류·1skip | author결속·시간예산·불완전 scheduler행·Bpin 차이 등의 결손 재현. 오류도 그대로 기록 |
| 같은 신규19 / 수정 도구 | 18통과·1skip·0실패/오류 | 같은 소스에서 기능 보완. skip은 OS symlink 생성 권한 |
| B 연결 시험 추가 뒤 커밋 판20 | 19통과·1skip·0실패/오류 | 별도 commit blob 실행. 위19와 합산하지 않음 |
| 승인 B 연결 모의 | 첫 가드 제출 성공·두 번째 거부 · B283 불변 | 실제 승인 canonical/submit 함수, fake scheduler 한 번만 호출 |
| 포장·블록 | tar294파일·manifest293/293 · Bash rc0 · 내장 Python4조각 AST 통과 | 실제 ibb 제출·Linux 자격을 대신하지 않음 |

Windows Python3.12.14에서 합성 입력만 썼고 감사 hook의 실제 프로세스/네트워크 시도는0이다. B 연결 시험의 runner문자열에는 Windows 절대경로 대신 고정 POSIX 합성 바인딩만 적용했다. 승인 소스 원문은 바꾸지 않았다. 이는 조립 연결 모의이며 Linux/Lustre의 링크·권한·동시 변경·SLURM/MPI 현장 자격을 확인한 결과가 아니다. 실제 symlink 시험1개는 OS 권한으로 skip, 별도 모의 링크 거부는 통과다.

준비 중 B 연결 시험의 경로 어댑터 오류2회와 초기 시험 fixture 덮어쓰기 오류1회는 시험 준비 기록에 보존했다. 현장 결함이나 해결된 물리 문제로 세지 않는다. 내부 확인이며 독립 반박 판정 또는 verified 근거로 올리지 않는다.
