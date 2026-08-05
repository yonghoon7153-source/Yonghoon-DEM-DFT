# SETUP_GPU — 새 GPU 서버(V100 등)에서 환경 자동 구축 method

> 어떤 머신에서든(SSH V100 서버, 새 워크스테이션, HPC 노드) **명령 3줄**로
> 동일한 환경을 재현하기 위한 문서. 스크립트가 하는 일과 수동 대응까지 담는다.

---

## 0. TL;DR — 새 서버에서 할 일

```bash
git clone <이 저장소 URL>
cd Yonghoon-DEM-DFT/degradation-degeneracy
./scripts/setup_env.sh          # GPU 자동 감지. V100이면 --gpu와 동일하게 동작
```

끝. 스크립트가 시스템 탐지 → venv → `pybamm[all]` 설치 → (GPU 감지 시) jax 설치 →
`verify_env.py` 검증 → `docs/ENV_REPORT.md` 생성까지 자동으로 수행한다.

검증 통과 기준 (ENV_REPORT.md에서 확인):

| 항목 | 기대값 | 실패 시 |
|---|---|---|
| IDAKLU | `사용 가능` | CasadiSolver로 자동 fallback (2~5배 느림, 진행 가능) |
| composite DFN | `빌드 성공` | **진행 불가** — pybamm 버전 확인 (아래 §4) |
| Chen2020_composite | `로드 성공` | pybamm 재설치 |
| 1회 solve | ~2 s (IDAKLU 기준) | 10 s 이상이면 casadi로 돌고 있는지 확인 |

---

## 1. 전제 — GPU 현실론 (03_ARCHITECTURE.md 6절 요약)

**이 프로젝트의 1차 실행 경로는 CPU 대규모 병렬이다.**
PyBaMM DFN(stiff DAE, 암시적 적분)은 GPU로 빨라지지 않고, composite phases
모델은 JAX 변환이 실패할 가능성이 높다(Phase 7에서 실패 전제로 시도).

따라서 **V100 서버에서도 핵심 자원은 GPU가 아니라 CPU 코어 수다.**
GPU는 다음에만 쓴다:

- Phase 7: JAX 변환 시도 (실패 기록도 산출물)
- surrogate NN 학습 (grid 데이터 확보 후, PyTorch)
- 대규모 지도 후처리

`nvidia-smi`가 없어도 모든 Phase 0~6이 완전히 동작한다.

---

## 2. setup_env.sh 옵션

```bash
./scripts/setup_env.sh              # GPU auto-감지 (기본)
./scripts/setup_env.sh --gpu        # GPU 스택 강제 설치
./scripts/setup_env.sh --no-gpu     # CPU만 (GPU 서버라도 jax 생략)
./scripts/setup_env.sh --recreate   # .venv 갈아엎고 재구축
./scripts/setup_env.sh --python python3.11   # 인터프리터 지정
```

특징:
- **멱등** — 재실행 안전. 깨진 환경은 `--recreate`.
- pip에 `--timeout 180 --retries 8` 기본 적용 (원격 서버 네트워크 대비).
- GPU 스택 설치 실패는 경고로만 남기고 **전체를 실패시키지 않는다**.

---

## 3. V100 전용 노트

| 항목 | 내용 |
|---|---|
| 아키텍처 | Volta, compute capability **7.0 (sm_70)** |
| CUDA 지원 | CUDA 12.x까지 지원. **CUDA 13에서 Volta 제거** — cuda13용 휠 설치 금지 |
| 드라이버 | CUDA 12 런타임 휠 사용 조건: driver ≥ 525.60.13 (`nvidia-smi` 우상단 확인) |
| jax | `jax[cuda12]` 사용 (requirements-gpu.txt). sm_70 지원 여부는 jax 버전에 따라 다르므로 `python -c "import jax; print(jax.devices())"` 로 반드시 확인 |
| PyTorch | surrogate 단계에서만 필요: `pip install torch --index-url https://download.pytorch.org/whl/cu121` (cu121 휠은 sm_70 포함) |
| FP64 | V100은 FP64 1:2로 강력 — 나중에 surrogate보다 물리 계산에 GPU를 쓰게 되면 유리 |

드라이버가 CUDA 11.x까지만 지원하는 구형 V100 서버라면:
- 최신 jax는 CUDA 12 전용이므로 **CPU 경로로 진행**하는 것이 정답.
- 굳이 GPU가 필요하면 관리자에게 드라이버 업데이트 요청이 우선.

### SSH 서버에서 흔한 상황

```bash
# 1) 로그인 노드에서 곧바로 (일반 리눅스 서버)
./scripts/setup_env.sh

# 2) HPC(module 시스템)라면 python부터 로드
module avail python cuda        # 목록 확인
module load python/3.11 cuda/12.1
./scripts/setup_env.sh --python python3.11

# 3) 장시간 grid 실행은 반드시 세션 분리
tmux new -s grid    # 또는 nohup / slurm sbatch
./run.sh --mode grid --config configs/grid_fine.yaml --nproc $(nproc) --out results/grid_fine_v1
# 끊겨도: 같은 명령에 --resume 붙여 재개
```

---

## 4. 수동 설치 (스크립트를 못 쓸 때)

```bash
python3 -m venv .venv && source .venv/bin/activate
python -m pip install -U pip wheel
pip install --timeout 180 --retries 8 -r requirements.txt
python scripts/verify_env.py            # ← 반드시 실행
# GPU(선택, CUDA 12 확인 후):
pip install -r requirements-gpu.txt
```

검증된 버전 조합 (2026-08-05, 이 저장소에서 전체 테스트 통과):

| 패키지 | 버전 |
|---|---|
| Python | 3.11.15 |
| pybamm | 26.7.1.0 (IDAKLU 포함) |
| numpy / scipy / pandas | 2.4.6 / 1.17.1 / 3.0.5 |
| joblib / pyarrow | 1.5.x / 25.0.0 |

pybamm이 바뀌면 가장 먼저 깨지는 지점:
1. composite DFN 옵션 문법 (`particle phases`, `current sigmoid`)
2. 변수명 — 아래 4개가 존재해야 한다 (`model.variable_names()`로 확인):
   - `Average negative primary particle concentration [mol.m-3]`
   - `Average negative secondary particle concentration [mol.m-3]`
   - `Average positive particle concentration [mol.m-3]`
   - `Battery negative electrode bulk open-circuit potential [V]`
3. `Experiment` step 구조 (`sol.cycles[-1].steps[-1]` = 최종 방전)

---

## 5. 자주 겪는 문제

| 증상 | 원인 / 대응 |
|---|---|
| pip `ReadTimeoutError` | 네트워크. 스크립트 기본 재시도로 대부분 해결. 반복되면 `--timeout 300` |
| `IDAKLU 사용 불가` | `pip install "pybamm[all]"` 재설치. 안 되면 casadi로 진행 (자동) |
| `composite DFN 빌드 실패` | pybamm 24.x 이상인지 확인. 옵션 문법 변경 여부 릴리즈노트 확인 |
| jax가 GPU 대신 CPU 잡음 | `pip install "jax[cuda12]"` 재설치, driver/CUDA 버전 확인 (§3) |
| headless에서 그림 저장 실패 | `MPLBACKEND=Agg` (run.sh가 자동 설정). 직접 python 실행 시 주의 |
| grid 도중 SSH 끊김 | tmux/nohup 필수. 재시작은 `--resume` |
| 디스크 부족 | `results/` 정리. fine 격자 원시 청크는 수 GB |

---

## 6. 재현성 체크리스트 (새 환경에서 결과 이어가기)

1. `git log --oneline -3` — 코드 버전 확인 (모든 결과 manifest에 commit hash 기록됨)
2. `./run.sh --mode verify` — ENV_REPORT.md 생성 확인
3. `pytest tests/ -v -m "not slow"` — 빠른 테스트 통과 (수 초)
4. `pytest tests/ -v -m slow` — solve 포함 검증 (~1분, IDAKLU 기준)
5. `./run.sh --mode grid --config configs/grid_coarse.yaml --dry-run` — 예상 시간 확인
6. 이전 서버의 `results/<run>/manifest.yaml`과 `config_hash`가 같은지 대조
   — 같으면 곡선이 solver 오차 범위에서 동일해야 정상
