# E0 366423 — 첫 반환 보존 후 수집만 (2026-11-16)

| 트랙 | 계산 | 상태 | 숫자 | 다음 |
|---|---|---|---|---|
| 믹서 E0 | 기존 366423 한 팔 | 1저자 확인 RUNNING, 수집 전용 블록 준비 | 19:1x KST 경과 2:16:09, wall 1일 (사용자 전달) | 종료 후 1저자가 수집 TXT 실행 |

## 1. 수령 사실

1저자 전달: GO_E0_ONCE로 제출한 366423의 감시 SSH가 rc255로 끊겼다. controller 기록은 INCOMPLETE, Broken pipe. 첫 반환은 e0_report.tar.gz 143346 B와 SHA256SUMS 83 B뿐이며 full archive는 없다. RETURN_RC=0은 이 두 파일의 회수 상태이며 계산 완료가 아니다. 실제 잡은 19:1x KST RUNNING이었다. 예상 종료 20:30–22:00 KST는 기존 블록 어림이며 새 측정이 아니다. 이 창은 호스트에 접속하지 않았다.

## 2. 이번 처리

고정 실행 컨트롤러 `997aabe1b5a702e2f389007e3923018d778ce857`의 scripts/mixer_e0_pilot_ibb.py SHA256=`56f2d5ea366e55c987417bc7fea0f777598fb807f21de1887ae4aeea8af2a943`는 변경하지 않는다. 배포 TXT의 결속 기록은 리포 밖 binding.json으로 제공한다.

새 prepare_collect.py는 366423만 허용한다. squeue 비어 있음과 sacct의 유일한 종료행, 기존 컨트롤러 부재, 소스 신원, 첫 반환 해시를 먼저 확인한다. RUNNING·상태 불명·살아 있는 컨트롤러·해시 오류이면 원 반환을 옮기지 않는다.

종료 확인 뒤 packet 내부의 returns/ 및 evidence/ 디렉터리를 collection_history/collect_366423_20261116/ 아래로 **이름만 옮겨 보존**한다. 파일을 삭제하거나 내용을 덮지 않으며 BEFORE.json·PRESERVED.json과 새 evidence/collection_recovery.json에 바이트 대조를 남긴다. B·control·승인·예약·case 출력은 변경하지 않는다. 이력 폴더가 이미 있으면 두 번째 보존/수집을 시작하지 않는다. 이동 중 오류가 나도 되돌리거나 자동 재시도하지 않는다.

그 뒤 원 컨트롤러를 `--collect`로만 호출한다. 새 반환은 새 returns/에 쓴다. 새 수집은 nohup+setsid로 SSH에서 분리하고 출력은 원격 파일에 쓴다. 같은 TXT를 다시 실행하면 기존 작업의 상태 확인/회수만 한다. 수집 작업의 완료 영수증 archive_rc=0과 report/full 두 파일·해시가 모두 있어야 반환 완료로 표시한다. 실패한 계산의 증거도 수집할 수 있으므로 WORKER_RC·계산 rc와 RETURN_RC를 분리한다.

## 3. 검증과 한정

합성 10메서드 통과. 첫 보존 구현 전 9메서드의 미구현 증인: 실패3/오류8. 마지막 한 메서드는 실제 고정 컨트롤러 main의 --collect 분기를 합성 디렉터리에서 호출해 원 report 충돌을 재현하고, 보존 뒤 두 새 archive/해시 생성까지 확인한다. scheduler·runtime·환경은 모의, 외부 명령은 호출 시 실패하도록 막았다. 이 시험을 실제 ibb 파일시스템·완료 잡 검증으로 세지 않는다. TXT·내장 worker의 bash 문법과 내장 Python 컴파일·해시도 대조한다.

실제 제출·취소·재큐·예약 해제·연구 계산·현장 접근 0. 다음 발사 감시도 SSH 분리 방식으로 바꿀 예정이다. 이번에는 이미 승인된 실행 소스를 바꾸지 않고 수집 경로만 분리한다. 원장·공유 기록은 Claude 반입 때 제안 문장만 적용한다. 명령 TXT는 접속 정보 때문에 리포 밖으로만 제공한다.
