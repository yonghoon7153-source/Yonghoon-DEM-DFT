# 서버 부트스트랩 런북 — GPU 인스턴스 껐다 켤 때마다 이것만 (2026-07-27 정본)

임시 GPU 인스턴스(runyour.ai V100 등)는 끄면 전부 증발한다.  **모든 설정이 코드화**되어
있으므로, 새로 켤 때마다 아래 표의 3~4줄이면 즉시 파이프라인 가동 상태로 복원된다.
이 세션(2026-07-26~27)에서 실제로 밟은 지뢰 전부가 `scripts/setup_gpu_server.sh` 에
자동화-회피되어 있다 (숫자·원인은 맨 아래 "지뢰 목록").

## ★ 기계-판독 정본 = `config/env_db.json` (+ `scripts/env_db.py`)

이 문서는 사람용 서술이고, **같은 내용의 기계-판독 정본이 `config/env_db.json`** 이다
(패키지·머신 프로필·솔버 env·앵커·레시피·지뢰).  외우지 말고 물어보면 된다:

```bash
python3 scripts/env_db.py --doctor      # ★현재 머신 진단 → 빠진 것 + 고침 명령 그대로 출력 (종료코드 0/1)
python3 scripts/env_db.py --machine v100   # 그 머신의 셋업/실행/회수 명령 + 주의사항
python3 scripts/env_db.py --pitfalls    # 증상→원인→고침 (아래 지뢰표와 동일 소스)
python3 scripts/env_db.py --env         # STEP4 솔버 노브 기본값·의미·현재값
```
`setup_gpu_server.sh` 의 마지막 단계가 `--doctor` 를 자동 실행한다.  DB 와 코드가 어긋나면
`--selftest` 가 잡는다(solver_env 키가 step4_dyn 에 실재하는지까지 대조).

## ⓪ 머신 프로필 (뭐가 어디에 있나)

| 머신 | 역할 | 경로/env | 비고 |
|---|---|---|---|
| **V100 (runyour.ai)** | MPM+STEP3+STEP4 GPU 런 | `~/Yonghoon-DEM-DFT` + `venv` | 인스턴스마다 host/pem 바뀜 → ① |
| **kgy (esp-Z590)** | 보조 GPU 런 | conda env `mpm`(py3.11) 필요 | 구 glibc(<2.32) → taichi 1.6.0 자동폴백 |
| **로컬 WSL (DESKTOP-K1BLBIJ)** | webapp(dem-web:5002)·데이터 보관 | 코드 `/home/yonghoon/dem-web`, venv `~/Yonghoon-DEM-DFT/venv` | `dem5002` alias → **`bash <repo>/scripts/run_dem_webapp.sh`** (아래 ⑤) |
| 클라우드(Claude) | 코드 수정·커밋 정본 | branch `claude/stoic-knuth-NObVQ` | GPU/sklearn 없음 — 정적검사만 |

## ① 새 인스턴스 접속 설정 (로컬 WSL에서, 인스턴스 새로 팔 때마다)

runyour.ai 가 주는 `ssh -i <새.pem> -p <포트> ubuntu@<호스트>` 에서 pem/호스트/포트만 바꿔서:

```bash
mkdir -p ~/.ssh && chmod 700 ~/.ssh
cp "/mnt/c/Users/안용훈/Downloads/<새키>.pem" ~/.ssh/ && chmod 600 ~/.ssh/<새키>.pem
# ~/.ssh/config 의 기존 Host v100 블록에서 HostName/Port/IdentityFile 세 줄만 교체 (블록 중복 금지!)
```
```
Host v100
    HostName <호스트>
    User ubuntu
    Port <포트>
    IdentityFile ~/.ssh/<새키>.pem
    ServerAliveInterval 60        # ← 연결 끊김(SIGHUP) 방지
    ServerAliveCountMax 3
    StrictHostKeyChecking accept-new
```
→ `ssh v100` / `scp v100:경로 .` 즉시 사용.

## ② 서버 세팅 (ssh 접속 후, 한 줄 — 멱등이라 재실행 안전)

```bash
curl -fsSL https://raw.githubusercontent.com/yonghoon7153-source/Yonghoon-DEM-DFT/claude/stoic-knuth-NObVQ/scripts/setup_gpu_server.sh | bash
pip install pyflakes      # ⚠ 이 판 스크립트가 안 깐다 — 아래 이유
```
⚠ **`pip install pyflakes` 를 빼먹지 말 것** — 이 stoic-knuth 판 setup 스크립트는 pyflakes 를 설치하지 않아,
팔 스크립트의 미정의-이름 게이트가 최소-AST 폴백으로 떨어지며 오탐 114건 → **팔 0** 으로 죽는다 (2026-09-13 실사고).
pyflakes 를 이미 넣은 setup 스크립트가 `sdcp-dem-manuscript-si-pqwtv8` 브랜치에 있으니, 그 판 URL 로 curl 하면 수동
설치가 필요 없다 (어느 쪽이든 checkout 코드는 stoic-knuth 로 동일 — 스크립트 안 `BRANCH` 가 stoic-knuth 고정).
자동으로: apt deps → repo clone/checkout → venv(또는 활성 conda env) → 파이썬 패키지 전부
(numpy/scipy/pandas/networkx/scikit-image/**taichi**/**pyamg**/**pybamm**/**pyflakes**) → **cupy-cuda12x[ctk] +
nvidia CUDA 라이브러리**(libcublasLt 포함) → **OCP 앵커 생성**(STEP4 SKIP 방지) → 7단계 검증
(taichi CUDA·cupy sparse CG·selftest).  실패하면 **세팅 단계에서 원인 출력하고 STOP**
(런 3시간 돌다 중간에 죽는 구조 아님).
- kgy(구 glibc + py3.13 base): 먼저 `conda create -y -n mpm python=3.11 && conda activate mpm` 후 위 실행.

## ③ 매 셸/재접속마다 (env + CUDA 경로 한 방)

```bash
dem            # = source ~/Yonghoon-DEM-DFT/scripts/activate_dem.sh (setup이 alias 자동등록)
```
★ **run 은 반드시 이걸 source 한 셸에서** — detached 자식(run_mpm.sh 의 setsid nohup)이
venv(numpy/cupy)·LD_LIBRARY_PATH 를 물려받아야 "ModuleNotFoundError: numpy" 재발이 없다.

## ④ 런 (킷 zip 을 ~/Yonghoon-DEM-DFT 에 풀고)

```bash
bash run_mpm.sh                    # 전체 STEP1~4 (detached — SSH 끊겨도 생존, tail -f 로그)
bash step4_only.sh [런폴더]         # step4만 재개 (step4_grid.npz 존재 시; 기본 latest_run)
```
env 노브(기존 킷 그대로 먹음): `MPM_S4_RINT` `MPM_S4_DS` `MPM_NO_PULL=1`(pull 끄기)
`MPM_FRACTURE=1` `MPM_PERIODIC_SIGMA=1` — STEP4 수치 노브는 docs/step4_bottleneck_analysis 참고.

## ⑤ 결과 회수 (로컬 WSL에서)

```bash
R='/home/ubuntu/Yonghoon-DEM-DFT/latest_run'
scp v100:"$R/mpm_metrics.json" v100:"$R/mpm_payload.json" .        # σ 정본 (webapp 업로드용)
scp v100:"$R/step4_*.npz" v100:"$R/*viz*.json" v100:"$R/mpm_run.log" .   # step4 곡선·뷰어·로그
DL="/mnt/c/Users/안용훈/Downloads"; cp <파일> "$DL/"                # 윈도우로 보낼 때
```
진행 중 부분곡선: `python3 ../scripts/step4_curve_from_log.py mpm_run.log:라벨 --out 부분곡선`

## 지뢰 목록 (이번에 실제로 밟은 것 → 전부 setup 에 코드화됨)

| 지뢰 | 증상 | 코드화된 해결 |
|---|---|---|
| venv 안 켠 셸에서 run | detached 자식 `No module named numpy` (STEP1 즉사) | activate_dem.sh source 규칙(③) + PATH 상속 |
| cupy 만 설치 | `libcublasLt.so not found` | nvidia-*-cu12 라이브러리 동시 설치 |
| CUDA 헤더 없음 | `Failed to find CUDA headers` (커널 JIT 실패) | `cupy-cuda12x[ctk]` |
| CUDA 13 드라이버 | cupy 호환 걱정 | cuda12x wheel backward-compat (V100 실검증 ✓) |
| 구 glibc + py3.13 (kgy) | taichi `GLIBC_2.32 not found` / 1.6.0 wheel 없음 | conda py3.11 안내 + import-검증 폴백 |
| anchor_params 없음 | `STEP4 SKIP — OCP 앵커 없음` | setup 이 `--export-params anchor_params` 자동 실행 |
| SSH 끊김 | 포그라운드 런 SIGHUP 사망 / 3일 낭비 | ServerAliveInterval + detached 런 + tmux 권장 |
| 프로세스 확인 착오 | `kill <틀린PID>` / tail ^C를 런 종료로 오인 | `pgrep -af 'step4_dyn\|mpm3d'` 로 이름 검색, ^C는 tail만 멈춤 |
| 실행 중 코드 교체 | git checkout 해도 옛 코드로 계속 돔 | 파이썬은 시작 시점 로드 — **kill 후 재시작** 필수 |
| pyflakes 미설치 | Phase A/SDCP **팔 0** (미정의-이름 게이트 ABORT, 오탐 114건) | setup [4/7] pyflakes 설치·[7/7] import 검증 — ⚠ **sdcp 판 curl** 로만 (옛 stoic-knuth 판엔 없음) |
| **CUDA 13 pip 세트가 NVRTC 를 가로챔** | V100 에서 `nvrtc: error: invalid value for --gpu-architecture (-arch)` · `NVRTC_ERROR_INVALID_OPTION` — import 는 되는데 **첫 GPU 연산에서** 죽는다 | **CUDA 13 은 Volta(sm_70) 지원을 끊었다.**  접미사 **없는** `nvidia-*`(=CUDA 13, `site-packages/nvidia/cu13/lib/`)가 깔려 있으면 cupy-cuda12x 라도 그쪽 `libnvrtc.so.13` 을 잡는다.  ⇒ 고아면 세트째 `pip uninstall`.  ⚠ **드라이버가 13 인 건 무해하다** — 문제는 **NVRTC 가 13** 인 것 (2026-09-21 실사고) |
| `LD_LIBRARY_PATH` 로 안 고쳐짐 | cu12 nvrtc 경로를 앞세워도 그대로 cu13 을 연다 | cupy 가 **전체 경로로 직접 dlopen** 한다 ⇒ 검색 경로가 무의미.  패키지를 빼는 수밖에 없다 |
| `cupy-cuda12x[ctk]` 가 아무것도 안 가져옴 | 설치 로그에 `nvidia-*` 가 하나도 없다 | `[ctk]` 를 믿지 말고 `pip list \| grep -i nvidia` 로 **실제로 확인**할 것 |
| cu12/cu13 이 같은 디렉터리를 공유 | cu13 을 지웠더니 **torch 가** `libcudnn.so.9` → `libnccl.so.2` 로 연쇄 실패 | 둘 다 `site-packages/nvidia/<lib>/lib/` 에 쓴다 ⇒ 한쪽 제거가 다른 쪽 파일을 가져간다.  `pip install --force-reinstall --no-deps <cu12 세트>` 로 복구 (**`--no-deps` 없으면 cu13 이 다시 딸려온다**) |
| **런 중에 `pip` 실행** | 솔브가 오류 한 줄 없이 사라지고 루프가 `Done` 으로 끝난다 | 파일이 발밑에서 바뀐다.  ⛔ **솔브와 `pip` 를 동시에 돌리지 말 것** (2026-09-21 실사고) |
| 루프를 죽여도 **자식 솔브가 살아남음** | `Done` 이 떴는데 `ps` 에 솔브가 남아 있고, 재시작하면 **같은 `--out` 에 두 프로세스**가 쓴다 | 루프 정지 후 `ps -eo pid,ppid,etime,rss,args \| grep '[m]pm_webapp_payload'` 로 **고아를 PID 로 확인·정리**한 뒤 재시작 |
| **WSL 에서 MPI 경로가 통째로 막힘** (1저자 데스크탑) | `lmp_auto` 직접 실행도 `mpirun -np 1` 도 **둘 다** CPU 0 % · RSS 13~20 MB · sleeping · 로그 0 바이트 | 이 기계에서는 **MPI 를 쓰지 않는다**.  `lmp_serial`(STUBS 직렬 빌드, `~/src/LIGGGHTS-PUBLIC/src/`) 로 돌린다 — 믹서 대조쌍(2026-09-19)도 그것으로 돌았다.  ⇒ 런처 기본값은 `lmp_serial`, MPI 빌드를 주면 **거부**한다 (`MPIOK=1` 로만 강제).  **"serial 로 동시에"** = 런마다 1 코어 · 여러 개 병렬 |
| **MPI 빌드를 `mpirun` 없이 실행** | 배너도 없고 **CPU 0 % · RSS ~20 MB 고정 · sleeping · 로그 0 바이트**.  죽은 줄 알기 쉽다 | `MPI_Init` 무한 대기다.  **np=1 이라도 `mpirun -np 1` 을 거친다.**  2026-08-25 `oat_sweep` 에서 39 분, 2026-09-21 믹서에서 **같은 사고 재현** — 새 런처에 그 교훈을 안 담았기 때문 ⇒ 런처를 새로 쓸 때 `dem_scripts/oat_sweep/run_all.sh` 의 머리말을 먼저 읽을 것 |
| 로그가 비어 보임 | 살아 있는데 `log` 가 0 바이트 / 안 자람 | 파일로 보내면 stdio 가 **4 KB 블록 버퍼**를 쓴다 ⇒ `stdbuf -oL -eL` 로 줄 단위로 흘린다 |
| **실행 중인 런의 덱을 덮어씀** | 몇 시간 뒤 `ERROR: Unknown command: <줄의 꼬리>` — 덱에 없는 명령 | **LIGGGHTS 는 입력을 읽어 가며 실행한다.**  같은 inode 를 잘라 새로 쓰면 프로세스가 다음 읽기에서 **새 파일의 바이트**를 명령으로 받는다 (2026-09-22 `E0_s32452843`: 옛 덱 6,917 B 를 다 돌고 EOF 자리에서 새 덱의 6,917 번째 바이트 `z radius` 를 읽음).  런 중 `pip` 와 같은 부류의 사고.  ⇒ 생성기는 살아 있는 런을 건너뛰고 `mv`(rename = 새 inode)로만 바꿔 넣는다 (`gen_all.sh` 2026-09-22) |
| **`Total wall time` 만으로 완주 판정** | 마지막 `run` 통계까지 찍고 배너 없이 끝난 런이 "죽음" 으로 보이고, 런처가 **재발사해 로그·덤프를 지운다** | 09-21 덱(`restart` 포함)은 E0 3/3 이 같은 자리에서 배너 없이 죽었다 (종료 결함, 데이터 무사).  완주 = 배너 **또는** 마지막 thermo step ≥ `run` 합.  죽은 런은 자동 재발사하지 않고 `FORCE=1` 로만 (`run_all.sh`·`watch.sh` 2026-09-22, 회귀 `test_launcher.sh`) |
| 런처가 옛 인스턴스를 안 죽임 | `git pull` 해도 웹앱에 **새 라우트가 404**, 런처는 `✓ PID` 를 찍음 (거짓 초록) | `run_dem_webapp.sh` 가 포트 기준 `_stop_port` 로 **먼저 종료 후 기동** + `--stop` 모드.  ⚠ `pkill -f webapp/app.py` 는 안 맞는다 (cmdline 이 `python3 app.py`) |

⚠ 이 런북과 setup 스크립트가 **정본**이다 — 새 지뢰를 밟으면 여기와 setup_gpu_server.sh 에
같이 추가할 것 (둘이 어긋나면 setup 스크립트가 우선).

## ⑤ webapp 런처 · alias (2026-08-25 — 홈이 아니라 **리포**에 둔다)

⚠ **왜 옮겼나**: 옛 런처가 `~/run_dem5002.sh` 라 홈에만 있었고, 윈도우 재설치로 WSL 이
통째로 날아가면서 **같이 사라졌다**.  리포에 두면 `git clone` 한 번으로 돌아온다.

```bash
# ~/.bashrc 에 한 번만 (경로는 코드 worktree)
echo 'export DEM_WEB_CODE=$HOME/dem-web' >> ~/.bashrc
echo 'export DEM_WEB_DATA=$HOME/Yonghoon-DEM-DFT' >> ~/.bashrc
echo 'alias dem5002="bash $DEM_WEB_CODE/scripts/run_dem_webapp.sh --bg --open"' >> ~/.bashrc
echo 'alias demfg="bash $DEM_WEB_CODE/scripts/run_dem_webapp.sh --open"' >> ~/.bashrc
echo 'alias demstop="kill \$(cat $DEM_WEB_DATA/webapp/dem_webapp.pid) 2>/dev/null && echo stopped"' >> ~/.bashrc
echo 'alias demlog="tail -f $DEM_WEB_DATA/webapp/dem_webapp.log"' >> ~/.bashrc
source ~/.bashrc
```

| alias | 무엇 |
|---|---|
| `dem5002` | git pull → 백그라운드 기동 → **브라우저 자동 열기** (셸을 안 잡는다) |
| `demfg` | 포그라운드 (로그를 눈으로 보며, Ctrl-C 로 종료) |
| `demstop` · `demlog` | 종료 · 로그 따라보기 |

런처가 하는 일: ① 현재 브랜치로 `git pull --ff-only` (실패해도 **멈추지 않는다**)
② venv 탐색(`DATA/venv` → `CODE/venv`) ③ **`WEBAPP_*_FOLDER` 4개 배선** — 코드 worktree 와
데이터 폴더가 갈려 있어 이걸 안 하면 웹앱이 빈 폴더를 보고 "케이스 0건" 으로 뜬다
④ 포트 대기 후 브라우저.  `PORT=5050 dem5002` 로 포트 변경, `--no-pull` 로 오프라인.

⚠ WSL 이 아예 새로 깔린 경우엔 리포부터:
```bash
git clone -b claude/stoic-knuth-NObVQ https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT.git ~/dem-web
python3 -m venv ~/Yonghoon-DEM-DFT/venv && ~/Yonghoon-DEM-DFT/venv/bin/pip install -q flask numpy scipy
```
⚠ **데이터(`~/Yonghoon-DEM-DFT/webapp/{uploads,results,archive,mpm_lab}`)는 git 에 없다** —
백업에서 복원해야 한다.  없으면 웹앱은 뜨지만 케이스가 0건이다.
