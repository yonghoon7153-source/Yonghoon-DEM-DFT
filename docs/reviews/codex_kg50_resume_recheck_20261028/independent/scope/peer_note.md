# 두 finding의 독립 교차검토

핀 f118c1fd1e3eb1a558299663dcee6a0bf83b9942. 실제 Bash·LIGGGHTS·MPI·scheduler 미실행. 코드 분기 판독과 원문 내장 Python 함수만 직접 실행했다.

## 1. stale job 승격 — 반박할 방어 없음; P1에 동의하되 조건 명시

- `resume_ckpt.sh:661–662` squeue 실패 또는 busy는 **첫 for의 continue**다. :655(S 폴더 없음), :664(backup 이름 충돌)도 같은 구조다.
- 둘째 for는 :718에서 원래 `$CASES` 전체를 다시 순회한다. :719의 유일 진입 키는 디스크의 `$W/job_${SFX}t.txt` 존재다. 이번 invocation이 실제 제출한 목록·attempt ID를 요구하지 않는다.
- 기존 W에 동일 SFX의 완료 trial job 파일·mode·원 로그·trial 로그·runner가 남아 있으면, 첫 loop가 skip했어도 둘째 loop가 그 옛 job을 읽는다. sacct 옛 trial COMPLETED/0:0, 그 job만의 squeue 빈 출력, 일관된 옛 로그로 G0–G3를 통과할 수 있다. :777–780은 현재 main job 존재를 다시 묻지 않고 본 제출한다.
- 특히 :662가 잡은 **현재 실행 중 main C_r56**과 :725가 조회하는 **옛 trial job ID**는 다르다. '둘째 squeue도 있으므로 안전'이라는 반박은 성립하지 않는다. 첫 squeue만 일시 실패한 경우도 이후 조회가 회복되면 경로가 열린다.
- 경계: `TONLY=0`, 같은 case/SFX의 재사용, 오래된 성공 trial와 그 검증 파일의 잔존이 전제다. 새 빈 작업 폴더·옛 job 파일 없음이면 이 반례는 성립하지 않는다. 실제 duplicate 제출이 발생했다는 실측은 아니다.
- 최소 해결: **이번 invocation에서 정상적으로 제출한 trial만** 고유 attempt ID와 명시적 목록에 넣어 둘째 loop가 그것만 소비하게 한다. 기존 파일을 삭제하여 증거를 잃는 방식 대신 별도 attempt 폴더/manifest를 쓴다. 본 제출 직전 main 충돌·동일 attempt의 main 이미 제출 여부도 확인하고, 조회 실패는 승격 거부. 회귀 = 옛 성공 파일이 존재 + 첫루프 busy/조회실패 → trial0/main0; 정상 신규 attempt → trial1/main1.

## 2. 첫 long run의 every 소실 — 반박할 방어 없음; 직접 함수 반례 성립

- :693은 첫 long run의 원문 옵션을 읽지 않고 `print "run " n; exit`로 시험을 만든다. `every`/`start`/`stop` 등이 시험에서 사라진다.
- `run_n()`(:148–160)가 every를 거부하지만 :703의 검사 대상은 이미 옵션을 지운 **trial 덱**이다.
- settling static check :334–365의 known 경로는 run 숫자/upto로 끝 step만 계산한다. 첫 run을 `run_n()`으로 검사하지 않는다. `FWD`(:40)에 run이 없고, E(:396–397)는 첫 long run **다음**부터 비교하므로 suffix를 놓친다.
- 독립 직접 실행(원문 내장 Python `check()`/`trial_steps()`):
  - main: `run 1; restart 1000 restart_settling_*.bin; run 200000`
  - resumed: `read_restart restart_settling_20001.bin; run 180000 every 1000 "velocity all set 0 0 0"`
  - 정적 problems=[] · note=`남은 step 같음: 끝 200001`.
  - :693이 이 fixture에서 출력할 trial=`read_restart ...; run 2000`을 전달하면 `trial_steps rc=0`, `2000 1 [run 2000]`.
  - 결과 `peer_every_result.json`, 입력 `peer_main.liggghts`, `peer_resume.liggghts`, `peer_trial.liggghts`.
- 한정: **전체 wrapper/Bash/SLURM 성공 실측은 아니다.** 또한 모든 after_settling·compress 경로가 허용하는 것은 아니다. 그 경로의 `plain()`/`sched_cmp()`가 막을 수 있으므로 **settling known 분기**로 좁혀야 한다. 현재 제공 정상 v2/v3 덱에 every가 들어 있다고 주장하지 않는다. 외부 생성기가 만든 잘못된 첫 run을 관문이 놓치는 반례이다.
- 최소 해결: trial을 자르기 **전** 원 재개 long run 전체를 공통 run parser로 검증하고 unsupported 꼬리를 거부. 허용된 pre/post 옵션도 실제 main/trial 의미가 같도록 보존·정의해야 한다. settling static check 또한 첫 run의 숫자 외 토큰을 검증한다. 변이 시험은 trial_steps에 every를 직접 주는 것만으로 부족하며, 원 resume→시험 생성→정적검사 전체를 통과시켜 거부를 확인해야 한다.

두 건 모두 '실제 생산 사고가 났다'가 아니라 코드상 본 제출 관문의 반례다. 첫 건은 scheduler분기 source 증명, 둘째는 source증명 + 원문 Python함수 직접 실행으로 근거 강도를 구별한다.
