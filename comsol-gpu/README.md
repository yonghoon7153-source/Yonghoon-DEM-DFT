# COMSOL GPU 파이프라인 (배터리 FEM)

원격 GPU 서버(`ssh root@<HOST>`)에서 COMSOL Multiphysics **6.4**를 배치(batch) 모드로
돌리고, **git으로 모델/설정을 연계**하고, **CPU vs GPU 성능을 실측**해서 배터리 모델별로
GPU가 실제로 도움이 되는지 확인하는 파이프라인입니다.

대상 모델: 배터리 FEM — **1D / P2D / 2D / 3D + phase field**.

---

## 0. 먼저 읽기: COMSOL의 GPU는 "아무거나 빨라지는" 게 아니다

COMSOL의 GPU 가속은 일반 CUDA 앱처럼 모든 시뮬레이션을 가속하지 않습니다.
**특정 솔버에만** 적용됩니다 (2026-06, COMSOL 6.4 기준).

| 기능 | GPU 가속 | 도입 |
|------|---------|------|
| 일반 FEM **직접(Direct) 솔버** = NVIDIA **cuDSS** | ✅ | **6.4** (2025-11) |
| 시간영역 음향 (Pressure Acoustics, Time Explicit, dG) | ✅ (`-hwacc`) | 6.3 / 6.4 멀티-GPU |
| DNN 대리모델(Surrogate) 학습 | ✅ | 6.3 |
| 일반 **반복(Iterative)** 솔버(GMRES+AMG 등), 대부분 multiphysics | ❌ CPU only | — |

➡ **배터리 FEM의 GPU 경로 = cuDSS 직접 솔버.** 음향용 `-hwacc` 플래그는 배터리와 무관합니다.

### 배터리 모델별 현실 (중요)

| 모델 | 규모(DOF) | GPU(cuDSS) 효과 | 권장 |
|------|-----------|-----------------|------|
| **1D / P2D (Newman/DFN)** | 수백~수천 | ❌ **거의 없음** (오히려 전송 오버헤드로 느려질 수 있음) | GPU 말고 **CPU 배치로 파라미터 스윕 throughput**에 집중 |
| **2D 공간분해** | 1e4~1e5 | △ 중간 (메시·물리에 따라) | cuDSS 시도 + 벤치마크로 확인 |
| **3D 공간분해** | 1e5~1e7 | ✅ 가능, **단 GPU 메모리(VRAM)에 인수분해가 들어가야 함** | cuDSS, VRAM 초과 시 iterative(CPU)로 폴백 |
| **Phase field** (dendrite, LFP 상분리, Cahn–Hilliard/Allen–Cahn) | 메시 의존 | ✅ **이득 큼** (비선형·시간의존 → 직접솔버 반복 호출) | cuDSS 1순위, 메시 미세할수록 유리 |

> **왜 P2D는 GPU가 의미 없나?** P2D(Newman)는 1D 전기화학 + 입자 의사차원(pseudo-dimension)
> 구조라 미지수가 수백~수천 개뿐입니다. 직접 솔버가 CPU에서 이미 수초 안에 끝나며,
> 행렬을 GPU로 보내고 받는 전송 비용이 계산 비용보다 커서 **GPU가 더 느릴 수 있습니다.**
> 이런 모델은 "한 번 빨리"가 아니라 "여러 케이스를 많이"가 목표 → **CPU 배치 throughput** 파이프라인을 쓰세요.

> **3D/phase-field 주의(VRAM):** 직접 솔버는 LU 인수분해 결과(fill-in 포함)를 메모리에 올립니다.
> 3D는 이게 매우 커져서 GPU 메모리(예: 24/48/80GB)를 넘으면 cuDSS가 실패하거나 느려집니다.
> 그 경우 CPU iterative(예: GMRES + Multigrid)가 유일한 현실 해법일 수 있습니다.
> → 이 파이프라인은 **솔버를 설정으로 바꿔가며 실측**하도록 설계되어 있습니다.

---

## 1. 디렉토리 구조

```
comsol-gpu/
├── README.md                     # 이 문서
├── config/
│   ├── server.env.example        # 서버 접속 + COMSOL 경로 (복사해서 server.env로)
│   └── models/
│       ├── p2d_baseline.env.example     # P2D 예시 (CPU 권장)
│       ├── battery3d_cudss.env.example  # 3D + cuDSS(GPU) 예시
│       └── phasefield_cudss.env.example # phase field + cuDSS 예시
├── scripts/
│   ├── lib/common.sh             # 공통 헬퍼(로깅/설정 로드/검증)
│   ├── check_env.sh              # [서버] GPU/COMSOL/라이선스/cuDSS 점검
│   ├── run.sh                    # [서버] 모델 1개 배치 실행 (CPU/GPU)
│   ├── benchmark.sh              # [서버] 같은 모델 CPU vs GPU 비교 + nvidia-smi 실측
│   ├── parse_log.py             # COMSOL 로그 → 지표(JSON/CSV) 추출
│   └── remote.sh                 # [로컬] push→서버 pull→실행→결과 회수 오케스트레이션
├── methods/
│   └── set_cudss_solver.md       # 모델에서 cuDSS 켜는 법 (GUI + Record Method)
├── models/                       # .mph 파일 (LFS 권장, 아래 참고)
├── results/                      # 실행 산출물 (git 제외)
└── benchmarks/                   # 벤치마크 CSV/리포트 (요약만 git 추적)
```

---

## 2. 사전 준비 (서버에서 1회)

> 서버에 **COMSOL이 아직 없으면** 먼저 [`docs/INSTALL_server.md`](docs/INSTALL_server.md)로
> 헤드리스 설치(무인 + GPU/cuDSS 포함)부터 끝내세요.

GPU 서버에 SSH 접속 후:

```bash
# 1) 레포 클론 (이미 scp/git 쓰는 흐름에 맞춤)
git clone <repo-url> ~/Yonghoon-DEM-DFT      # 또는 기존 클론에서 git pull
cd ~/Yonghoon-DEM-DFT/comsol-gpu

# 2) 환경 점검 (GPU·드라이버·COMSOL·라이선스·cuDSS 라이브러리)
cp config/server.env.example config/server.env
$EDITOR config/server.env                    # COMSOL_BIN 등 경로 수정
bash scripts/check_env.sh
```

`check_env.sh`가 확인하는 것:
- `nvidia-smi` (GPU 존재/드라이버/VRAM)
- `comsol` 바이너리 + 버전 (6.4 여부)
- `comsol batch -h` 실제 지원 플래그 덤프 (← 버전별 `-hwacc` 등 정확한 옵션을 *서버 본인 바이너리*에서 확인)
- 라이선스 접근(`comsol -checkout`/`server` 가용성 점검)
- COMSOL GPU 컴포넌트 / cuDSS 라이브러리 경로 힌트

> COMSOL 6.4 설치 시 **GPU Compute Components가 기본 포함**됩니다.
> GUI에서 검증: `File ▸ Preferences ▸ Computing ▸ GPU Acceleration ▸ Verify CUDA Installation`,
> 그리고 같은 화면에서 **cuDSS 라이브러리 경로**를 수동 확인하세요.

---

## 3. 모델에서 cuDSS(GPU) 켜기

cuDSS는 **CLI 플래그가 아니라 모델의 Direct 솔버 설정**입니다. 두 가지 방법:

1. **GUI(권장):** `Study ▸ Solver Configurations ▸ Stationary/Time-Dependent Solver ▸
   Direct ▸ Solver = "CUDA Direct Sparse Solver (cuDSS)"` 로 바꾸고 저장.
2. **Record Method(자동화):** GUI에서 "Record Method"를 켠 상태로 위 변경을 한 번 수행하면
   COMSOL이 정확한 API 코드를 생성해 줍니다. 그 코드를 모델 메서드로 저장하면 배치에서 재현 가능.

자세한 단계와 메서드 템플릿: [`methods/set_cudss_solver.md`](methods/set_cudss_solver.md)

> 보통 **CPU용(`*_cpu.mph`, MUMPS/PARDISO)** 과 **GPU용(`*_cudss.mph`)** 두 변형을 저장해두면
> 벤치마크가 깔끔합니다. (같은 물리, 솔버만 다름)

---

## 4. 사용법 (워크플로우)

### A. 로컬에서 한 방에 (권장)

```bash
# 로컬 PC에서: 변경 커밋·푸시 → 서버 git pull → 서버 실행 → 결과 요약 회수
cp config/server.env.example config/server.env   # 로컬에도 서버 접속정보
bash scripts/remote.sh run battery3d_cudss
bash scripts/remote.sh bench --cpu battery3d_cpu --gpu battery3d_cudss
```

### B. 서버에서 직접

```bash
# 서버에서
cd ~/Yonghoon-DEM-DFT/comsol-gpu
bash scripts/run.sh battery3d_cudss              # 모델 1개 실행
bash scripts/benchmark.sh --cpu battery3d_cpu --gpu battery3d_cudss
```

실행이 끝나면:
- `results/<model>/<timestamp>/` 에 출력 `.mph`, `batchlog.txt`, `metrics.json`
- 콘솔에 **DOF 수 / 솔루션 시간 / 사용 솔버 / GPU 사용 확인 / 메모리** 요약
- 벤치마크는 `benchmarks/<name>.csv` 에 CPU·GPU·**speedup**, 그리고 실행 중
  `nvidia-smi` 샘플(GPU 사용률·VRAM)을 남겨 **GPU가 실제로 돌았는지 실측**합니다.

> **"GPU 사용 확인"이 핵심:** 로그에 cuDSS/GPU 흔적이 없거나 nvidia-smi 사용률이 0이면,
> 설정은 GPU인데 실제로는 CPU로 돈 것입니다. 파이프라인이 이를 잡아내 경고합니다.

---

## 5. 모델 등록 (config/models/*.env)

모델 하나당 `.env` 파일 하나. YAML 파서 의존성 없이 bash가 바로 `source` 합니다.

```bash
# config/models/battery3d_cudss.env
MODEL_NAME=battery3d_cudss
MPH_FILE=models/battery3d_cudss.mph   # comsol-gpu/ 기준 상대경로
STUDY=std1                             # 실행할 study 태그 (비우면 모델 기본)
SOLVER=cudss                           # cudss | mumps | pardiso | spooles (문서/검증용 라벨)
USE_GPU=true                           # GPU 의도(로그 검증의 기준)
NP=8                                   # 사용할 물리 코어 수
HWACC=                                 # 음향 explicit 전용. 배터리는 비워둠.
EXTRA_FLAGS=                           # 그 외 comsol batch 플래그
NOTES="3D 공간분해 배터리, cuDSS 직접솔버"
```

예시 3종(`.example`)이 들어 있습니다. 복사해서 `.env`로 쓰세요.

---

## 6. .mph 파일 버전관리

`.mph`는 바이너리라 git에 그대로 넣으면 비대해집니다. 둘 중 택1:

- **Git LFS (권장):** 레포 루트 `.gitattributes`에 `*.mph filter=lfs ...` 설정됨.
  서버/로컬에 `git lfs install` 필요.
- **scp:** 기존처럼 `.mph`만 직접 전송. `results/`·tmp는 `.gitignore` 처리됨.

요약 지표(`metrics.json`, 벤치 `*.csv`)는 가벼우니 git으로 추적해 이력을 남기길 권장합니다.

---

## 7. 트러블슈팅

| 증상 | 점검 |
|------|------|
| "GPU 설정인데 안 빨라짐" | 모델 규모가 작음(P2D/1D)→정상. 큰 3D면 로그에서 cuDSS 실제 사용 여부·VRAM 초과 확인 |
| cuDSS인데 nvidia-smi 0% | 모델 Direct 솔버가 cuDSS가 아님(저장 누락) 또는 iterative 솔버 사용 중 |
| `out of memory` (GPU) | 3D 직접솔버가 VRAM 초과 → CPU iterative(GMRES+Multigrid)로 전환 |
| 라이선스 오류(batch) | 플로팅 네트워크 라이선스(FNL) 필요(멀티-GPU/MPI). `check_env.sh` 참고 |
| `comsol: command not found` | `config/server.env`의 `COMSOL_BIN` 경로 수정 |

---

## 참고 출처

- [GPU Acceleration Updates — COMSOL 6.4 Release Highlights](https://www.comsol.com/release/6.4/gpu-acceleration)
- [Study and Solver Updates — COMSOL 6.4](https://www.comsol.com/release/6.4/studies-and-solvers)
- [Setting Up GPU-Accelerated Computing Within COMSOL Multiphysics](https://www.comsol.com/support/learning-center/article/92461)
- [GPU Selection Guidelines for COMSOL Computing](https://www.comsol.com/support/learning-center/article/gpu-selection-guidelines-for-comsol-computing-131452)
- [How to Run Simulations in Batch Mode from the Command Line — COMSOL Blog](https://www.comsol.com/blogs/how-to-run-simulations-in-batch-mode-from-the-command-line/)
- [Running COMSOL in Parallel on Clusters — KB 1001](https://www.comsol.com/support/knowledgebase/1001)
- [System Requirements for COMSOL 6.4](https://www.comsol.com/system-requirements/64/general)
