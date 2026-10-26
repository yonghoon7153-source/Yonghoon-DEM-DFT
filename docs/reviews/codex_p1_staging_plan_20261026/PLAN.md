# P1 준비 결과 접수와 다음 작업 승인안

**지정 실행 파일과 기존 성공 이력·문법 자료 8개는 일치했다. 기본 작업 폴더의 입력과 선택된 실행 키트가 아직 준비되지 않아 inventory_rc=2였다.** 다음은 새 작업 공간에 수용된 키트와 입력을 준비한 뒤 직접 preflight까지만 수행하는 안이다. **아직 실행하지 않았으며 사용자 승인을 기다린다. 물리 RJ는 포함하지 않는다.**

## 이번에 확인된 범위

[전달 출력 전사본](user-relayed-inventory.txt)과 [비교 기록](inventory-receipt.json)을 보존한다. 사용자가 전달한 2026-10-26 21:42:58–21:43:01 KST ibb-master/yonghoon 결과 블록만 수동 전사했다. 로그인 정보·깨진 붙여 넣기 echo는 제외했다. 원본 터미널 파일의 바이트 사본이나 실제 실행된 스크립트의 바이트 증명은 아니다. Codex가 ibb에 접속한 결과도 아니다.

- 지정 LMP는 기존 크기·해시와 일치하고 실행 비트가 있었다. Python/mpirun은 myenv 경로로 관찰됐지만 MPI 동작을 시험하지 않았다.
- 성공 이력의 verdict/manifest와 첫 성공 문법의 verdict/manifest·matching kit 3개 파일이 일치했다. P/GA/GB 디렉터리의 이름 목록도 확인됐다. 원시 문법 결과를 다시 판독한 것은 아니다.
- 기본 work root와 in/ 디렉터리, staged 여섯 파일이 없어 missing=8이었다. 이는 해당 기본 경로의 관찰이며 다른 모든 위치에 파일이 없다는 뜻이 아니다.
- 표시된 worktree 9개 중 4c 핀의 checkout은 없었다. Git 객체 저장소에도 4c가 없다는 결론은 내리지 않는다. 실행 키트는 미선택이므로 unknown=1이며 mismatch=0이었다.

앞선 원본 여섯 파일 일치 기록과 기존 한정된 CLOSED 판정은 유지한다. 사용자가 알려 준 20:14 원문 게시 경로는 후속 source `2aee692dce4fb9ec173b03ee3d4e40b49473e10f` 확인에서도 아직 발견되지 않았으며, 전사본과 원격 원문을 동일시하지 않는다.

## 승인받을 정확한 변경

[검토용 계획 스크립트](stage-and-preflight.plan.sh)는 승인 표시가 없으면 외부 명령이나 쓰기 전에 거부한다. 아래는 지금 실행하라는 명령이 아니라 **승인 범위를 고정한 계획**이다.

1. 기존 저장소 /home/yonghoon/Yonghoon-DEM-DFT에서 origin의 codex/unloading-ulpri만 명시적으로 fetch한다. FETCH_HEAD가 전체 핀 `4c29705fa1c4ba94737a858b206fa4f4c5bb2bde`와 다르면 멈춘다. 기존 checkout의 HEAD와 작업 파일 상태를 보존한다.
2. 새 detached worktree /home/yonghoon/unload_src_4c29705fa1c4를 만든다. 기존 checkout을 전환하지 않는다. 새 경로에 파일·디렉터리·dangling symlink가 있으면 멈춘다. worktree 생성에 checkout hook을 사용하지 않는다.
3. 키트의 SHA256SUMS 자체가 수용된 4c의 크기 7403 및 SHA256 `bb9f305f476815d7448ee5069ceb8fa3b9f138f3be1dc59703fcc8eec09c03bb`와 일치한 뒤에만 목록의 파일을 검사한다. 봉인을 통과하기 전에 키트 코드를 실행하지 않는다.
4. 새 /home/yonghoon/ps45_unload_20261009와 그 아래 ps_7_3_r45/in/을 만든다. mkdir -p나 기존 폴더 재사용을 하지 않는다. 앞서 확인한 원본 여섯 파일을 다시 크기·해시로 확인하고 새 in/에 덮어쓰기 없이 복사한 뒤 목적지도 전부 비교한다. cp -n의 성공 반환만으로 복사 성공을 주장하지 않는다.
5. 지정 Python/mpirun, LMP, 기존 성공 HIST/GRAM 자료 및 NP6로 **직접 run_unload.sh의 --preflight-only**만 호출한다. sbatch wrapper를 호출하지 않으므로 SLURM_JOB_ID가 있어도 wrapper의 물리 실행 분기를 타지 않는다. RESUME=0, ALLOW_OTHER_LMP=0, ALLOW_CONCURRENT=0과 등록된 MPI flags를 명시한다.

입력 여섯 파일은 합계 **252,405,453바이트(약 240.71 MiB)**다. 전체 worktree와 Git fetch 객체, preflight의 임시 출력은 별도 공간을 쓰므로 이것이 전체 디스크 요구량은 아니다. 원본 파일을 이동·수정하지 않는다. fetch는 Git 메타데이터/객체를, 새 worktree는 작업 파일과 worktree 메타데이터를 추가한다. 새 work root에는 staged 입력이 생긴다. preflight는 봉인된 reader와 기존 문법 결과를 판독하며 임시 출력을 사용할 수 있지만 LMP/MPI 시뮬레이션이나 RJ 작업을 시작하지 않는다.

## 실패했을 때와 종료 경계

경로가 점유됐거나 핀·크기·해시가 다르거나 복사·preflight가 실패하면 즉시 멈춘다. 부분적으로 생긴 폴더는 삭제·덮어쓰기·자동 재시도하지 않고 출력과 함께 보존한다. 특히 한 번 중단된 뒤 같은 계획을 다시 실행하면 기존 새 루트가 있으므로 거부된다. 별도 확인 없이 강제 정리하지 않는다.

preflight 통과도 물리 복원 RESTORED나 S0 자격을 뜻하지 않는다. 승인 범위는 **한 번의 명시적 fetch, 새 detached worktree, 새 작업 루트, 여섯 파일 복사·대조, 직접 preflight**까지다. 물리 RJ/UB/UT/UC, 새로운 fixture 실행, Claude 가지 반입, P2/50kg, CI 변경과 외부 검토 발송은 제외한다. 현재 상태는 **계획 미실행·승인 대기**, 물리 RJ와 P2 T12는 NOT_RUN이다.

근거: [수용된 README](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/4c29705fa1c4ba94737a858b206fa4f4c5bb2bde/docs/data/ps45_unload_20261009/README.md), [직접 runner의 preflight 분기](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/4c29705fa1c4ba94737a858b206fa4f4c5bb2bde/docs/data/ps45_unload_20261009/run_unload.sh#L104-L140), [고정 params와 입력 신원](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/4c29705fa1c4ba94737a858b206fa4f4c5bb2bde/docs/data/ps45_unload_20261009/unload_params.json).
