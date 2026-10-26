# P1 7:3 준비 상태 — 읽기 전용 확인

원본 여섯 파일의 신원 확인은 끝났다. 이제 **작업 폴더의 입력, 지정 실행 파일, 이미 성공했던 이력·문법 자료가 실제 위치에 남아 있는지** 확인할 차례다. 이 문서와 명령은 준비 상태 목록만 만들며 RJ나 preflight를 실행하지 않는다.

현재 Codex 환경에는 ibb 접속 수단이 설정되어 있지 않다. 실제 확인은 사용자의 **기존 ibb 터미널**에서 해야 한다. Codex는 SSH 접속을 시도하지 않았고 접속 정보를 요청하지 않는다.

## 사용 방법

1. [Bash 명령 전체](readiness-inventory.sh)를 열어 기존 ibb 터미널에 붙여 넣는다. 파일 저장·새 폴더·다운로드·Git fetch가 필요하지 않다. 명령은 하나의 subshell 안에서 끝난다.
2. 실제 작업 키트나 저장소 위치를 이미 알고 있다면, 붙여 넣기 전에 P1_KIT_DIR 또는 P1_REPO_DIR 변수에 **기존 실제 절대 경로**를 지정할 수 있다. 키트 경로를 모르면 비워 두며 최신 폴더를 자동 선택하지 않는다. 저장소 경로를 비워 두면 알려진 후보 /home/yonghoon/Yonghoon-DEM-DFT가 있을 때 그 worktree 목록만 읽는다. 후보는 키트 자동 선택이 아니다. P1_WORK_ROOT를 따로 지정하지 않으면 기존 /home/yonghoon/ps45_unload_20261009를 살펴본다. 경로를 바꿀 때도 기존 폴더만 선택한다.
3. 화면의 표준 출력과 오류를 생략하지 않고 함께 보내면 된다. 명령은 결과 파일을 만들지 않는다. MISSING/MISMATCH/UNKNOWN 또는 KIT_UNCONFIRMED가 나와도 새 실행·복사·재생성을 하지 말고 그대로 전달한다.

## 무엇을 확인하나

- host/user/KST 시각과 Python/mpirun 명령 위치만 본다. MPI나 LMP를 실행하지 않는다. NP6는 기준값으로 표시하며 MPI 동작 확인으로 주장하지 않는다.
- 지정 LMP, 과거 성공 이력의 verdict/manifest 두 파일, 첫 성공 문법의 verdict/manifest와 matching kit의 seal/reader/params 다섯 파일을 과거 크기·해시와 대조한다. 원래 문법 run의 P/GA/GB 목록도 본다. 이는 raw 자료가 완전하거나 19개 조건을 통과했다는 새 판정이 아니다.
- 실제 작업 폴더의 staged 입력 여섯 파일이 있으면 해시를 대조한다. 원본 여섯 경로를 직접 다시 검사하지 않는다. staged 경로가 심볼릭 링크나 하드 링크라면 같은 원본 파일을 가리킬 수 있다. 기존 RJ 및 RJ로 시작하는 이름은 목록만 표시하며 이전 시도를 변경하지 않는다.
- 선택한 기존 저장소는 optional locks와 lazy fetch를 끈 Git worktree list만 읽는다. 해당 Git 옵션이 지원되지 않으면 오류를 보고하며 다른 방법으로 fetch하지 않는다. worktree 목록은 후보 위치일 뿐 수용된 키트라는 증거가 아니다.
- P1_KIT_DIR를 지정했으면 SHA256SUMS 자체의 해시가 수용된 4c의 예상값과 같을 때만 그 목록을 따라 sha256sum -c를 실행한다. 다르면 목록을 따라가지 않는다. 키트의 Python/Bash 코드를 실행하지 않는다. 이 검사는 seal 목록에 든 파일의 바이트만 대상으로 하며 실행 자격이나 전체 저장소 일치를 뜻하지 않는다.

[기대값과 원본 근거](expectations.json)는 고정된 과거 기록이다. run verdict/manifest/seal은 이미 보유한 report 압축본에서 얻었다. 압축본에 없는 reader/params의 해시는 그 seal, 크기는 당시 manifest의 Git 핀에서 해시가 일치하는 blob으로 확인했다. 현재 ibb 결과는 아직 아니다.

## 결과의 한계와 다음 단계

inventory_rc는 missing/mismatch/unknown이 있으면 2, 없으면 0이다. 0도 준비 목록의 읽기·비교 범위에 한정되며 실행 자격이 아니다. match/missing/mismatch/unknown 범주와 개별 오류를 함께 읽어야 한다. 원래 실패 fixture를 최신 이름으로 고르거나 다른 run의 kit를 섞지 않는다. 첫 성공 문법 자료가 없으면 그 상태부터 확인하며 새 fixture 반복을 미리 전제하지 않는다.

준비 상태가 결속된 다음 단계는 **허용된 범위의 직접 runner --preflight-only**다. 이번 명령에는 포함하지 않았다. sbatch wrapper는 SLURM_JOB_ID에 따라 실제 실행으로 분기할 수 있어 사용하지 않는다. preflight도 reader 및 임시 출력 처리가 있는 별도 단계이고, 물리 RJ 복원은 그보다 뒤다. 이 목록만으로 READY/GO·RESTORED·S0 자격을 부여하지 않는다. P2 물리 T12는 NOT_RUN이며 기존 좁은 CLOSED 수정은 다시 검토하지 않는다.

근거: [수용된 키트 README](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/4c29705fa1c4ba94737a858b206fa4f4c5bb2bde/docs/data/ps45_unload_20261009/README.md), [직접 runner](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/4c29705fa1c4ba94737a858b206fa4f4c5bb2bde/docs/data/ps45_unload_20261009/run_unload.sh), [역사 이력 압축본](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/4c29705fa1c4ba94737a858b206fa4f4c5bb2bde/docs/reviews/dem_unloading_history_test_20261014/hist_20261014_094731.report.tgz), [첫 성공 문법 압축본](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/4c29705fa1c4ba94737a858b206fa4f4c5bb2bde/docs/reviews/dem_unloading_grammar_fixture_runs_20261015/raw/gram_20261015_030225.report.tgz).
