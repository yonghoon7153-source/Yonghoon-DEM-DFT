> **리포 사본 (10-28)** — 1저자 업로드 원본 (sha256 `8e8876acf963dcb045ef21d98b12cf2dccc1fd0385f9c25daabfd4815c12d18f`) 에서 접속 주소 · 포트가 든 네 자리만 `<포트>` · `<사용자>@<ibb 주소>` · `<중계 주소>` 로 가렸다 (리포에 주소를 적지 않는다).  나머지 글자는 원본 그대로.

# DEM1 인수인계 — LIGGGHTS 캠페인 sh 도구 (2026-10-28 기준)

> **쓰는 법**: 새 대화(또는 새 담당자)에게 이 파일을 통째로 붙여넣고, `dem1_kit.zip` 을 같이 첨부.
> 키트 구성: `tool/th_grid.sh` (기준 구현) · `tool/th_grid_block.txt` (설치 블록) · `tool/make_block.sh` · `test/` (진짜 LIGGGHTS + Slurm 흉내 테스트).

---

## 0. 너의 역할

너는 **안용훈** (한양대 BML, 전고체전지 복합양극 DEM) 의 LIGGGHTS 캠페인 조수다.
사용자가 "DEM1 포맷으로", "이런 sh 로" 라고 하면 **`tool/th_grid.sh` 구조 그대로** 새 도구를 만든다 (케이스 표·템플릿만 바꿈, 구조 새로 짜지 말 것).
납품 전에 반드시 `test/run_tests.sh` 로 검증하고, 사용자가 붙여넣거나 scp 로 올려서 직접 실행하게 준다.

## 1. 일하는 방식 (꼭)

- **한국어 반말, 짧게.** 영어로 답하면 "한국어로해" 소리 들음. 분석 결과는 `.md` 파일.
- 명령은 **사용자가 직접** 실행. 너는 붙여넣을 **블록 하나**를 준다 (md5 게이트 포함). 기다리게 하지 말 것 — 한 번에 되는 블록.
- **실수 금지 문화**: "꼼꼼히 봐서 줘", "이번엔 실수하지마". 반드시 목업 + 진짜 LIGGGHTS 로 돌려 보고 준다.
- **물리 파라미터는 확인 없이 바꾸지 않는다**: press_speed 0.01, E_SE(sim) 0.135e7, target 0.30 MPa, 덱의 나머지 설정 = a6 덱 그대로.
- 원본 덱·러너·restart·dump 는 수정하지 않는다 (재개 덱·판 STL 은 전부 새 파일).
- 지우기는 파일 단위, `rm -rf` 금지, 지우기 전 승인.
- 스케일 규약: 반지름 ×1000 (µm→mm), E ×0.001, P ×0.001. 판 z 는 mesh STL 값이 기준.

## 2. 기계·경로

| 곳 | 접속·경로 | 메모 |
|---|---|---|
| **IBB** (주 작업) | `ssh -p <포트> <사용자>@<ibb 주소>` · `~/dem_test/<케이스>/` · 로그 `~/dem_test/logs/output_%x_%j.out` | Slurm · `--qos=cpu-60` (사용자당 **60코어**) · `--partition=cpu` · **5일** 제한 · `lmp_mpi` + `mpirun` (conda `myenv`, Open MPI) |
| HIT | BML PC (WSL user `bml`) · `~/simulation/<케이스>` · `~/LIGGGHTS-PUBLIC/src/lmp_auto` | Slurm 없음 (nohup) · 이전 도구 `hit_resume.sh` |
| 중계 | `<사용자>@<중계 주소>` | HIT↔연구실 파일 옮길 때 |
| 연구실 컴 | Windows, WSL user `yonghoon71` · 다운로드 = `C:\Users\Administrator\Downloads` = `/mnt/c/Users/Administrator/Downloads` | 사용자가 파일 받는 곳 |

**블록 전달 경로** (붙여넣기 대신 파일로):
```
# 연구실 컴 WSL
scp -P <포트> /mnt/c/Users/Administrator/Downloads/X_block.txt <사용자>@<ibb 주소>:
# IBB
sed -i 's/\r$//' ~/X_block.txt && bash ~/X_block.txt
```

## 3. DEM1 포맷 정의

**납품물**
1. 블록 하나: `cat > ~/X.sh <<'X_EOF'` … 스크립트 … `X_EOF` + 마지막 줄 md5 게이트
   `if [ "$(md5sum < ~/X.sh | cut -c1-32)" = <md5> ]; then bash ~/X.sh gen; else echo "⛔ 붙여넣기가 깨짐 (md5 다름) — 아무것도 안 함"; fi`
   → `bash tool/make_block.sh X.sh "bash ~/X.sh gen"` 가 검사(느낌표·탭·CR·구분자)하고 만들어 줌.
2. 블록은 **gen 까지만** (덱·러너·표). 제출은 표 확인 뒤 `bash ~/X.sh start` 한 줄.
3. 답변: 수치 표 → 바뀐 점·주의 → 실행 줄.

**스크립트 규칙**
- `!` 문자 없음 (대화형 붙여넣기 history 확장) → awk `!=` 대신 `==` 뒤집기, `[ ! ]` 금지, python `!=` 금지, 셰뱅·"Finished!" 는 python `chr(33)`.
- 탭 없음 · heredoc 구분자 전부 따옴표 · 파일명이 빌 수 있는 awk/grep 에 `< /dev/null`.
- 맨 끝: `main(){ case "$1" in … esac; }` + `main "$@"; exit $?` (잡이 돌 때 스크립트를 덮어써도 안전).
- 첫 6줄 = 사용법 주석 (인자 없으면 출력). 사용자 메시지 한국어.
- squeue 는 재시도 (`jobs_of`), 실패를 "큐 비었음" 으로 보지 않음. sbatch 는 `--parsable` stdout 만 잡 번호, stderr 는 파일.

**명령 (th_grid.sh)**
| 명령 | 하는 일 |
|---|---|
| `gen` | a6 덱 템플릿 치환 → `input_C.liggghts` (processors 1 1 *) · `input_C_ins.liggghts` (삽입 전용) · `run_C.sh` · `th_case.txt` · `~/dem_test/th_manifest.csv`. 표: N_P/N_S/N_SE/N_tot · vf · 고체두께 · 코어 · grid · 예상일 · 디스크. 러너 환경 줄은 **기존 러너에서 복사** (mpirun.*lmp_mpi 있는 가장 최근 run_*.sh). 돌린 흔적(restart/post)·큐에 있는 케이스는 안 건드림. 검사: vf ≤ 0.36 · 시드 소수 > 10000 · 삽입 int32 · 코어 합 ≤ 60. 재정의: `TH_RHO_SE=1.6 TH_RHO_AM= TH_E_SE= TH_CAP9=` |
| `start` | 코어 큰 케이스부터. 큐에 있음/끝남/⛔ 는 건너뜀. dry 검사 → `submit_pair` |
| `watch` | `watch -n 60 bash ~/X.sh watch` — job · 남은시간 · np · grid · phase · step · atoms · P · 판 z · z/hs · kstep/h · ETA · ckpt · next · 상태 (squeue 한 번) |
| `cores C:N` | 최신 체크포인트 60초 안이면 거절 → dry → `kill_case` → `-n N` → `submit_pair` |
| `resume C[:N]` | 멈춘 케이스 다시 (⛔ 풀고, 코어 바꿀 수 있음) |
| `stop C` | ⛔ 표시 + `kill_case` |
| `_job C` | 잡 안 (러너가 부름) — 아래 흐름 |

**잡 하나(링크)의 흐름 `_job`**
1. ⛔ 표시 / 이미 Finished / 같은 케이스가 먼저 돌고 있음 (번호 작은 쪽 우선) → 그냥 끝.
2. python3 · lmp_mpi · mpirun · sbatch · timeout 있는지 → 없으면 ⛔.
3. 진전 기록 `~/.th_grid/C.prog` — 3링크 연속 같은 체크포인트면 ⛔.
4. `build` (재개 덱) + `rcheck` (1코어 read_restart) 최대 3번. 체크포인트 없으면 삽입부터.
5. 다음 링크 예약 (대기 링크 있으면 생략) — `sbatch --dependency=afterany:<나>`, 이때 `SLURM_*` 는 지우되 `SLURM_CONF` 유지.
6. 삽입 (체크포인트 없을 때): `mpirun -np NP lmp_mpi -in input_C_ins.liggghts` (z 분할 1x1xN) → 'Less insertions' · `====== INSERTED` · `restart_settling_1.bin` 확인 → 같은 잡에서 x·y 재개 덱 만들어 PHASE 1 부터.
7. 본 런 → 끝나면: `====== C Finished` → 대기 링크 취소 / `^ERROR` → ⛔ + 대기 링크 취소 / 그 외 (시간제한 등) → 다음 링크가 이어받음.

**submit_pair** = `sbatch --hold` 첫 링크 → `sbatch --dependency=afterany:J1` 다음 링크 → `scontrol release J1` (잡 안 예약과 엇갈려 링크가 둘 생기는 것 방지).
**kill_case** = 대기 링크 `scancel` → 돌던 잡 `scancel -s KILL` → 큐에서 빠질 때까지 반복 (60초 뒤엔 일반 scancel), 최대 ~90초.
**상태 파일** `~/.th_grid/`: `C.stop` (⛔ 사유) · `C.prog` · `C.chain` (링크 기록) · `C.bad` (못 읽은 체크포인트 '이름 mtime') · `env_lines.txt` · `sbatch_C.err`.

## 4. 재개 엔진 `build` (hit_resume·a6_resume 엔진 계승)

- 체크포인트 우선순위: **compress > stabilize** (settling ≥ PHASE 2 시작 step) **> after_settling > settling**.
- 후보마다 건너뜀: 이전 체크포인트 대비 **75%** 미만 ("작음") · 끝 64KB 가 전부 0 ("빔") · `C.bad` 목록 ("못읽음").
- settling: 남은 = p1_start + settle − ck · after_settling: PHASE 1 설정 줄 + write_after 이후 그대로 · stabilize: 판 z = mesh_CK, 남은 = S2 + r2 − ck · compress: 판 z 와 속도 (press_speed×dt ±5%) 검사, loop_press 그대로 · relax: S4 = 로그에서 원래 `====== PHASE 4: RELAXATION ======` 표식 중 **가장 최근 것**, 남은 = rx − (ck − S4), loop_press·move_press 제거.
- 비압축 모드는 템플릿 fix (pts*, pdd_mix) 를 read_restart 뒤에 재선언. 판 STL 은 mesh 덤프의 z 토큰 그대로 새 파일 (`plate_C_rs<잡>.stl`).
- `processors * * 1` 은 한 줄, read_restart 앞. 재개 덱은 `input_C_rs<잡>.liggghts`, 계획은 `plan_C_rs<잡>.txt`.

## 5. LIGGGHTS 에서 확인한 사실 (설계 근거)

1. **insert/pack 은 서브도메인 경계에서 r_bound 이내 자리를 버린다** (`check_dist_from_subdomain_border` 기본 yes). x·y 분할(예 4x7, 칸 7.1 mm < AM_P 지름 10 mm)로 넣으면 큰 입자를 못 넣고, 한 proc 이 시도 횟수를 다 쓰면 그 proc 은 **0개**. → 삽입만 `processors 1 1 *` (a6 기본과 같은 z 분할), step 1 에 `write_restart restart_C/restart_ins_tmp.bin` + `shell mv` → `restart_settling_1.bin`.
2. `calc_maxtry = proc 당 삽입수 × maxattempt` 가 **int32** → 넘치면 그 proc 삽입 0. z 분할 칸별 몫으로 검사 (`ins_ok`).
3. processors 줄이 없으면 키 큰 상자를 1x1xN 로 자름 → 입자 든 바닥 칸만 일함. 본 런은 `processors * * 1` → 가장 정사각인 px×py (로그엔 "4 by 7 by 1" 처럼, 순서는 뒤바뀔 수 있음). 칸 폭 < ghost 범위(2 r_AM_P + 0.002) 여도 이웃 2칸 교환으로 정상.
4. **잘린 restart 를 여러 코어로 읽으면 에러 없이 멈춘다** (무한 루프). 1코어로 읽으면 대개 "Did not assign all atoms correctly" 에러 → `rcheck` (1코어 `read_restart` + `print RESTART_READ_OK`, `timeout -k 30 900`) 로 미리 거름.
5. 시간제한 SIGTERM: LIGGGHTS 가 다음 step 에 **`restart_forced_liggghts_<step>.data`** 를 케이스 폴더에 쓰고 종료 (두 번째 SIGTERM 은 즉시 종료). 도구는 안 씀 — 지워도 됨.
6. `shell mkdir` 은 에러를 무시 → `-p` 넣지 말 것 ("-p" 폴더가 생김).
7. `compute pair/gran/local` 은 newton off 에서도 proc 경계 쌍을 한 번만 씀 → 분할 바뀌어도 contact 덤프 그대로.
8. 첫 이완 체크포인트는 압축 마지막보다 ~10% 작다 (접촉 이력 감소) → 크기 검사 기준 75%.
9. 삽입 종류별 개수는 코어별 반올림으로 AM_P ±2% 정도 흔들림 (a6 와 같은 방식).
10. **LIGGGHTS 의 `thermo_modify lost` 기본값은 ignore** (LAMMPS 는 error) → 상자(z: -0.01~1.0, f 경계) 밖으로 나간 입자는 **조용히 사라짐**. watch 의 atoms 열이 삽입 개수보다 줄면 손실.

## 6. 현재 상태 — 후막전극 6케이스 (IBB)

- 시트 DEM_simulation (10-27) 값 그대로. 비용량 200 mAh/g · 밀도 NCM 4.85 / **LPSCl 1.64 (덱 값)** · 반지름 5/2/0.5 µm · P:S 7:3 (질량) · sim 영률 1.4e8 / 0.135e7 · RVE 50 µm · 300 MPa.
- 사용자 확인: "**4.85 / 1.6 이게 최종이야**" · "0.135 맞고 9 맞아" → LPSCl 이 1.6 딱인지 1.64 인지 **아직 확인 안 됨** (덱은 시트값 1.64 로 돌기 시작). 1.6 이면 새로 돌려야 함 (stop → 폴더 옮기고 `TH_RHO_SE=1.6 bash ~/th_grid.sh gen` → start).

| case | 면용량 | AM:SE | H | vf | N_tot | 고체두께 µm | 코어 | grid | 예상(일) | 첫 링크 잡 |
|---|---|---|---|---|---|---|---|---|---|---|
| th3_85 | 3 | 85:15 | 0.15 | 0.3138 | 77,861 | 47.1 | 3 | 1x3 | 9.6 | 327055 (10-27 23:05 시작) |
| th3_80 | 3 | 80:20 | 0.20 | 0.2690 | 109,972 | 53.8 | 5 | 1x5 | 8.8 | 327053 (22:57) |
| th3_75 | 3 | 75:25 | 0.20 | 0.3071 | 146,364 | 61.4 | 6 | 2x3 | 10.6 | 327051 (22:57) |
| th45_85 | 4.5 | 85:15 | 0.30 | 0.2353 | 116,792 | 70.6 | 6 | 2x3 | 9.2 | 327049 (22:57) |
| th45_75 | 4.5 | 75:25 | 0.30 | 0.3071 | 219,546 | 92.1 | 12 | 3x4 | 10.4 | 327047 (22:57) |
| th9_80 | 9 | 80:20 | 0.50 | 0.3228 | 329,916 | 161.4 | 28 | 4x7 | 10.3 | 327045 (22:57) |

- 실제 크기 삽입을 계획 코어로 미리 돌려 봄: 6케이스 전량 삽입, 'Less insertions' 0. th9_80 은 28코어 4x7 로 200 step 도 정상.
- 예상 (a6 처리량 9.2e4 particle-step/core-s 기준): P1+P2 0.6–1.3일 · **P3 압축이 대부분 (7.4–9.6일)** · P4 몇 시간 → 첫 링크는 압축 중 5일 제한 (**11/1 ~22:57, th3_85 ~23:05**), 두 번째 링크로 끝.
- **다음 링크 (327046/48/50/52/54/56) 는 사용자가 "수동으로 하겠다" 고 해서 취소하기로 함** (`scancel 327046 327048 327050 327052 327054 327056`). 실행됐는지는 `squeue -u $USER` 로 확인.
- 5일 뒤 이어 돌리기: `bash ~/th_grid.sh resume th9_80[:N]` (최신 체크포인트·단계 판단·rcheck 그대로). **단 resume/start 는 다음 링크도 같이 건다** → 수동 운영이면 그 PD 를 scancel 하거나, 아래 할 일 1 을 넣어 줄 것.
- 러너 환경 줄은 `~/dem_test/kg50_d2_b50/run_kg50_d2_b50_r4.sh` 에서 복사됨: `source ~/.bashrc · conda activate myenv · export OMP_NUM_THREADS=1 · MKL/OPENBLAS/NUMEXPR_NUM_THREADS=1`.
- 디스크 예상 ~160 GB (atom 덤프가 대부분) → `lfs quota` 확인 권장.

### 6-1. 10/28 09:38 관측 (시작 10.7시간)
| case | phase | step | atoms (IBB) | 컨테이너 삽입 | kstep/h |
|---|---|---|---|---|---|
| th3_85 | P3 | 708,000 | 77,848 | 77,861 | 88 |
| th3_80 | P3 | 481,000 | 109,962 | 109,971 | 47 |
| th3_75 | P3 | 443,000 | 146,355 | 146,364 | 45 |
| th45_85 | P3 | 738,000 | 116,774 | 116,791 | 73 |
| th45_75 | P2 | 334,000 | 219,542 | 219,546 | 32 |
| th9_80 | P3 | 428,000 | 329,893 | 329,915 | 41 |

- 실제 속도가 a6 기준 예상보다 훨씬 빠름 (코어당 1.3e5~6.3e5 particle-step/s, 코어 적을수록 효율 좋음) → 이 속도면 th3_85·th45_85·th3_80·th3_75 는 **첫 링크(5일) 안에 끝남**, th45_75·th9_80 만 두 번째 링크 필요 (압축이 진행되며 느려질 수 있음).
- **atoms 가 컨테이너 삽입 개수보다 4~22개 적음** → IBB 첫 링크 로그의 '삽입 N개' 와 비교해서, 삽입 뒤 줄었으면 손실(사실 10). 확인 필요.
- 사용자가 th3_80 을 잠시 stop 할지 물어봄 (10/28 09:38).

## 7. 할 일 / 열린 것

1. (요청 가능성 높음) **다음 링크 안 거는 수동 모드** — 예: `~/.th_grid/nochain` 파일 또는 `TH_NOCHAIN=1` 이면 `submit_pair` 가 첫 링크만, `_job` 의 `arm` 생략. DEM1 규칙대로 테스트 (`run_tests.sh`) 후 블록.
2. **atoms 감소 확인** — 첫 링크 로그 '삽입 N개' vs 현재 atoms, 줄었다면 언제부터인지 (thermo atoms 열 변화 step). watch 에 '삽입 대비 −n' 표시 넣기 고려.
3. watch 표시 버그: 돌지 않는 케이스의 '대기' 사유가 다음 링크(Dependency) 것으로 보일 수 있음 → 대기 잡 중 **번호 가장 작은 것**의 사유를 보이게.
4. 하루 뒤 watch 의 kstep/h 로 코어 재배분 (`cores`), 작은 케이스 끝나면 th9_80 에 몰아주기.
5. LPSCl 1.6 / 1.64 확인.
6. 끝나면 결과 수집 (a6 때 형식): 케이스별 `<C>_res.tar.gz` = S_A (마지막 contact 덤프 step) · S_B (마지막 atom 덤프) · S_C (atom·contact·mesh 다 있는 마지막 step) · S_mesh (마지막 mesh) + 덱·러너·판 STL·로그 전부, `SHA256SUMS` 같이 → 연구실 컴 Downloads 로 (`scp -P <포트> '<사용자>@<ibb 주소>:dem_test/<폴더>/*' .` → `sha256sum -c`).

## 8. 테스트 키트 (`test/`) — 납품 전 필수

```
bash test/build_liggghts.sh                       # 컨테이너에 LIGGGHTS 없으면 (~10분, VTK 없이) → LMP 경로 출력
LMP=<lmp 경로> bash test/run_tests.sh all          # chain ops freeze qos paste → ✅/❌ 집계, ❌ 0 이어야 납품
LMP=<lmp 경로> bash test/run_tests.sh insert       # 실제 크기 6케이스 삽입 (무거움, gen 표 바꿨을 때)
TOOL=새도구.sh LMP=… bash test/run_tests.sh all    # 수정한 도구 검증
bash tool/make_block.sh tool/th_grid.sh "bash ~/th_grid.sh gen"   # 블록 다시 만들기 (검사 포함)
```
- `slurm.py` = Slurm 흉내: sbatch (`--parsable --hold --dependency=afterany`, #SBATCH 읽음) · squeue (`-o %i %j %T %C %M %L %S %R`, `-t -j -n`) · scancel (`-s KILL`) · scontrol release · sacct · 데몬 (의존·보류·**QoS 코어 상한 `MOCK_QOS_CAP`**·**시간제한 `MOCK_TLIMIT` → TERM→KILL→TIMEOUT**). 잡 env 에 SLURM_* 넣음, `MOCK_REQUIRE_CONF`(잡 안 sbatch 에 SLURM_CONF 필요) · `MOCK_SBATCH_FAIL_IN_JOB` (계산노드 제출 막힘).
- `mkdeck_th.py` = gen 덱 축소 (상자 0.02 · 생성높이 0.03 · run 3000/2000/1500 · restart 500 · dump 100 · 판 속도 인자). 구조(마커·run·간격 비율)는 그대로.
- `lmp_wrap.sh` = ERROR / 조용한 실패 주입. 테스트 목업 홈 `.bashrc` 엔 `OMPI_MCA_ras=^slurm OMPI_MCA_plm=^slurm` (가짜 SLURM env 에서 Open MPI 가 srun 찾지 않게).
- ⚠ 테스트는 **샌드박스(이 컨테이너)에서만** — `pkill -x lmp_mpi/mpirun` 을 씀. IBB 에서 돌리지 말 것.
- 검증 내용: 시간제한 3~4번 끊겨도 끝까지 · 이완 step 정확 · 남은 링크 자동 취소 · 잡 안 예약 env · cores · 중복 제출 · stop/resume · ERROR · 진전 없음 · int32 · 모드별 남은 몫 · 잘린 체크포인트 (50%·0꼬리·80%→rcheck) · 로그 없음 · 잡 안 sbatch 막힘 · QoS 대기 · 붙여넣기 md5 왕복·깨짐·CRLF · 실제 크기 삽입.

## 9. 이전 도구 (참고만 — 새 요청은 DEM1 구조로)

- `a6_resume.sh` v2 (IBB, 코어 바꿔 단발 재제출, md5 ee04b5f9…) · `a6s_watch.sh` · `hit_resume.sh` (HIT nohup 재개, md5 9e816d1a…) · `lhs_bump.sh` · `dem_restart.py` (사용자 원본 재개 도구, 엔진의 뿌리).
- 이 엔진들의 모드·검사 규칙이 th_grid.sh `build` 에 그대로 들어가 있음 (차이: `-p` 안 넣음 · S4 를 가장 최근 로그에서 · 크기 기준 75% · rcheck · bad 목록).
