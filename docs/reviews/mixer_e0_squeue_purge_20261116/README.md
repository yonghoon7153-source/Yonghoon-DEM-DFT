# E0 감시 — Slurm 메모리에서 지워진 잡의 대기열 부재 처리

| 트랙 | 계산 | 상태 | 숫자 | 다음 |
|---|---|---|---|---|
| 믹서 E0 | 기존366423 결과 수집 | 컨트롤러 수정·합성 확인 완료, 새 현장 실행0 | 새12/12·기존19통과/1건너뜀 | Claude 반입; 기존 수집물은 별도 수령 |

## 1. 문제와 변경

바탕 = B `63f12d8a594c7490695abee0eaadc17f2257dd05`. 1저자 전달: 끝난 잡이 slurmctld 메모리에서 지워진 뒤 단일 잡 squeue 조회가 rc1과 `Invalid job id specified`를 반환했다. 원 scripts/mixer_e0_pilot_ibb.py의 wait_job은 모든 비정상 rc를 조회 실패로 처리해 sacct 확인에 도달하지 않았다. Claude가 제공한 임시 TXT는 squeue 대리 파일로 이 경우를 대기열 부재로 바꾸어 수집했다. 이 창은 그 TXT나 현장 명령을 실행하지 않았다.

수정은 **rc=1 + stdout 공백/빈 값 + stderr 전체가 지정 진단 하나**인 경우에만 ABSENT로 이어간다. 수용하는 진단은 `Invalid job id specified`, `slurm_load_jobs error: Invalid job id specified`, `squeue: error: Invalid job id specified` 세 꼴이다. 부분 문자열 일치가 아니다. 다른 rc, 비어 있지 않은 stdout, 권한/통신 오류, 추가 경고·오류·중복 진단은 종전처럼 실패한다. 전역/사용자 대기열 조회나 제출 경로에는 적용하지 않는다.

ABSENT는 완료 판정이 아니다. 기존 sacct의 **같은 잡 ID·유일한 종료행**이 있어야 종료 상태를 반환한다. accounting 지연은 기존300초 범위에서 기다리며, 없거나 다른 잡/비종료/중복행이면 완료 파일을 쓰지 않는다. FAILED는 FAILED 그대로다. sacct 자체 실패도 유지된다. 숨긴 원진단이 없도록 evidence/squeue_absent_*.json에 rc·stdout·stderr·잡ID와 terminal_confirmed=false를 남긴다.

## 2. 확인

같은 scripts/test_mixer_e0_squeue_absent.py의 12메서드: 수정 전 실패12관측/오류0 → 수정 후12/12. 메서드·subtest·반복 조회를 합산하지 않는다. 실제 wait_job을 호출하고 scheduler·시간·watch 관측만 모의했다. 즉시종료·accounting지연·accounting부재·실패종료·혼합오류·다른rc·RUNNING→부재·잘못된잡ID·중복행을 포함한다.

기존 scripts/test_mixer_e0_pilot_ibb.py: 20메서드 중19통과·1건너뜀(Windows 네이티브 symlink 자격), 실패0. 승인B fixture를 공급했다. 스킵을 통과로 세지 않는다. AST 비교: 기존 함수는 wait_job 하나만 변경, 새 squeue_reports_absent 하나 추가, 나머지27함수 동일. 소스의 제출·승인·archive·terminal 판독 함수는 그대로다. 전체 gate/실제Slurm/새연구계산은 실행하지 않았다.

## 3. 고정 자료 보존과 적용 경계

받은 purgedfix TXT는 리포 밖에 그대로 보존했다. 전체 파일 SHA256=`9aaf0cae17fb298a8ca56fb642b2dc101b9b1df326c19dc8b714395bffcf6adc` (15630 B). 내장 prepare_collect.py SHA256=`98ac01f5ef780513dd1a137842cc8912e388ebc2705c331cd109e8f1705279c5`, worker.sh SHA256=`b6083765ca78f4142947528995a9099bb9710ad40496dfd3c41ae977b0b1ec09`: 기존 제공 TXT와 바이트 동일(내장 텍스트의 LF 기준).

기존366423 컨트롤러는 고정핀 `997aabe1b5a702e2f389007e3923018d778ce857`·소스SHA256=`56f2d5ea366e55c987417bc7fea0f777598fb807f21de1887ae4aeea8af2a943` 그대로 둔다. 새 소스SHA256=`dc31f871701cab595905d99fad1cd9377f02e24989b48c1175732e92ec82107e`를 기존 승인/고정해시 파일에 덮어쓰지 않는다. 새 소스의 author_go 결속은 별도 새 패킷에서 이루어져야 한다. 현재 수집의 대리 squeue를 리포 코드/새 제출에 자동 적용하지 않는다.

다음 수집 TXT의 앞부분도 새 컨트롤러의 squeue_reports_absent를 사용한 뒤 sacct를 확인하도록 결속한다. 기존 고정 helper/worker를 바꾼 새 현장 블록은 이번에 만들지 않았다. 감시 SSH 분리(nohup/setsid) 문제와 이 조회 해석 문제는 별개다.

## 4. 재현·공유 기록 제안

리포 루트: `python -I -X utf8 -B scripts/test_mixer_e0_squeue_absent.py`. 전달 ZIP의 before 소스를 E0_TEST_SOURCE로 지정하면 같은 시험의 수정 전 실패를 확인할 수 있다. 실제 squeue·sacct·MPI·엔진은 호출하지 않는다.

Claude 공유 기록 제안: "E0 단일 잡 조회 rc1/Invalid job id specified를 좁게 ABSENT로 처리하고 sacct 종료 확인을 유지하는 수정. 새12/12, 기존19통과·1Windows건너뜀. 사용자 제공 purgedfix의 고정 내장2파일 동일 확인. 366423 현장 고정소스·승인·반환 불변, 새제출/취소/현장실행0. 결과 수집물의 내용 판정은 별도."

공유 원장·CLAUDE.md·진행 기록·check_all.sh는 수정하지 않는다. 새 회귀를 전체 게이트에 넣을 명령은 위와 같으며 Claude 반입 때 적용한다. 원장 verified/운영 GO를 새로 부여하지 않는다.
