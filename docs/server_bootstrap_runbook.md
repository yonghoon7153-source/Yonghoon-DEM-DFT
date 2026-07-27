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
| **로컬 WSL (DESKTOP-K1BLBIJ)** | webapp(dem-web:5002)·데이터 보관 | 코드 `/home/yonghoon/dem-web`, venv `~/Yonghoon-DEM-DFT/venv` | `dem5002` alias / `bash ~/run_dem5002.sh` |
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
```
자동으로: apt deps → repo clone/checkout → venv(또는 활성 conda env) → 파이썬 패키지 전부
(numpy/scipy/pandas/networkx/scikit-image/**taichi**/**pyamg**/**pybamm**) → **cupy-cuda12x[ctk] +
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

⚠ 이 런북과 setup 스크립트가 **정본**이다 — 새 지뢰를 밟으면 여기와 setup_gpu_server.sh 에
같이 추가할 것 (둘이 어긋나면 setup 스크립트가 우선).
