# P1 staging·사전 점검 완료 접수와 RJ 1회 제출 승인안

**업로드된 실제 터미널 파일에는 staging 완료와 직접 preflight 통과가 기록되어 있다.** 문법 prerequisite의 재판독도 PASS다. 이미 승인받은 staging·preflight를 다시 승인받거나 반복할 필요는 없다. 다음 승인 대상은 **7:3 생산 침대의 물리 RJ 복원 시험을 sbatch로 한 번 제출하는 것**이며, 아직 제출하지 않았다.

## 업로드 근거와 한계

[업로드 원본](uploaded-terminal.original.txt)은 **19,957바이트**, SHA256 `b13560113f38eb6f215c6d42d1eb104a5718df5cdd7e7476af2a7240d7c514bf`다. CRLF를 포함한 원본 바이트를 보존했고, [접수 기록](preflight-receipt.json)은 판독 결과를 구분한다. 앞선 수동 전사와 달리 이번에는 실제 첨부 파일이다.

관찰된 P1 출력은 다음과 같다.

- detached 4c checkout의 짧은 HEAD 표시, 키트 봉인 목록 76개씩 두 차례 OK, staged 여섯 목적지의 IDENTITY_MATCH.
- 22:00:31 직접 preflight 시작, 지정 LMP·NP6/myenv 명령·입력 확인.
- GRAMMAR_PREREQ status=PASS 및 reread=PASS, 고정 verdict/LMP/reader 해시, RJ gate ALLOW.
- 22:00:38 “사전 점검만 — 통과”와 staging 완료·physical RJ NOT_RUN 종료 표지.

터미널에는 시각만 있고 날짜는 세션의 2026-10-26, 시간대는 대화의 KST 문맥에서 붙였다. 최종 shell 반환값은 별도로 출력되지 않았다. 깨진 붙여 넣기 echo는 실행된 스크립트 바이트의 증명이 아니며, Codex가 ibb 파일을 독립적으로 다시 해시한 것도 아니다. 이 자료는 **보고된 실행 출력의 근거**다.

파일 앞부분의 별도 50kg 작업 323925는 제출 메시지만 확인된다. 그 작업이 현재 실행 중인지, 끝났는지, 성공했는지는 여기서 판정하지 않는다. P1 근거에 합치거나 상태 조회·취소·수정하지 않는다.

## 다음에 승인할 정확한 작업

[검토용 단일 제출 스크립트](submit-one-rj.plan.sh)는 기본 상태에서 외부 명령이나 쓰기 전에 거부한다. 실제 물리 작업 승인은 아직 대기 중이며 이 문서는 실행 결과가 아니다.

1. ibb 로그인 세션에서 수용된 4c checkout·봉인, staged 여섯 입력, 지정 LMP와 기존 성공 이력·문법 자료의 신원을 확인한다. 새 fetch나 키트 변경, 입력 복사는 하지 않는다.
2. 작업 루트 아래 **submission_ps73_RJ_20261026_once**라는 고정 영수증 폴더를 mkdir 한 번으로 독점 생성한다. bed/RJ.* 밖에 두므로 runner의 이전 시도 폴더 판정과 섞이지 않는다. 기존 폴더·파일·dangling symlink 또는 이전 RJ 이름이 있으면 멈춘다.
3. 수용된 변경 없는 wrapper를 **sbatch로 정확히 한 번** 제출한다. 대상은 ps_7_3_r45 / RJ, partition cpu, qos cpu-60, ntasks 6, 최대 walltime 5-00:00:00이다. **5일은 등록된 최대 한도이지 예상 소요시간이 아니다.** --no-requeue를 지정하며 자동 재제출·retry·후속 팔 제출은 없다.
4. sbatch의 stdout/stderr·실제 반환값·반환된 job ID를 영수증 폴더에 남긴다. Slurm stdout/stderr도 그 폴더의 job별 이름으로 지정한다. 반환이 불확실하거나 통신이 끊기면 영수증을 보존하고 중단하며 같은 스크립트를 다시 제출하지 않는다.

명시 환경은 기존 WORK_ROOT, myenv Python/mpirun, 지정 LMP, 성공 HIST/GRAM, NP6, 등록 MPI flags와 RESUME=0 / UL_KIT=0 / ALLOW_OTHER_LMP=0이다. 상속된 SBATCH_* 옵션은 제거하고 제출 자원을 명시한다. 로그인 노드에서 wrapper를 bash로 직접 실행하지 않는다.

**기존 봉인 wrapper는 allocation 안에서 ALLOW_CONCURRENT=1을 설정한다.** 이 등록된 동작을 숨기거나 봉인 코드를 고치지 않는다. wrapper는 기존 ~/.bashrc를 읽고 myenv를 활성화한다. 별도 50kg 작업이나 다른 작업을 끄거나 조작하지 않으며, 자원이 없으면 스케줄러가 대기시킬 수 있다. 이 제출 승인은 다른 작업 관리 승인이 아니다.

## 어디서 멈추나

현재 승인안은 RJ 1회 제출까지만이다. sbatch rc=0과 job ID는 제출 접수 증거일 뿐 실행·완료·복원 성공이 아니다. 나중에 정확히 결속된 job 및 단계 증거, 정상 완료의 fails=0/reader_rc=0, grammar_prereq=PASS, 생산 restore_verdict의 RESTORED를 확인해야 복원 성공을 판정할 수 있다.

중단되거나 job ID를 잃어도 기존 영수증을 삭제하지 않는다. 제출 여부를 별도로 확인하기 전에는 재제출하지 않는다. UB/UT/UC, 10:0, P2/50kg 실행, 새로운 fixture 실행, Claude 가지 반입, CI 변경 및 외부 검토 발송은 이 승인안에 없다. 기존 좁은 CLOSED 판정은 유지하며 P2 물리 T12는 NOT_RUN이다.

근거: [수용된 wrapper](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/4c29705fa1c4ba94737a858b206fa4f4c5bb2bde/docs/data/ps45_unload_20261009/run_unload_ibb.sbatch), [직접 runner와 RJ 순서](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/4c29705fa1c4ba94737a858b206fa4f4c5bb2bde/docs/data/ps45_unload_20261009/run_unload.sh), [등록·완료 조건](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/4c29705fa1c4ba94737a858b206fa4f4c5bb2bde/docs/data/ps45_unload_20261009/README.md).
