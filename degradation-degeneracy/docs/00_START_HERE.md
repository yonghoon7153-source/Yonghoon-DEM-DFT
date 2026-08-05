# 00. START HERE — 부트스트랩 지시서

> 이 파일은 **코딩 에이전트(Claude Code 등)에게 가장 먼저 읽히는 파일**이다.
> 이 파일 + 발표 PDF + 기존 코드 zip 세 개만 있으면 환경 구축부터 실행까지 자율적으로 진행할 수 있도록 작성되었다.

---

## 0. 에이전트가 받을 입력물

| 파일 | 내용 | 용도 |
|---|---|---|
| `_2026_08_05__연구세미나_이가형.pdf` | 41장 세미나 슬라이드 | 연구 배경, 21·22·32·33·34p가 핵심 |
| `degrade_mode_sim_me.txt` (또는 zip 내 `.py`) | 기존 PyBaMM 열화모드 시뮬레이션 스크립트 | 리팩터링 대상 원본 |
| `01~04_*.md` | 컨텍스트 / 코드감사 / 설계 / 단계별 프롬프트 | 작업 지시 |

---

## 1. 에이전트가 가장 먼저 할 일 (순서 고정)

```
1. 이 파일(00_START_HERE.md) 전체 읽기
2. 01_CONTEXT.md 읽기            → 왜 이걸 만드는지 (축퇴 문제)
3. 02_CODE_AUDIT.md 읽기          → 기존 코드의 문제점
4. 03_ARCHITECTURE.md 읽기        → 만들 구조와 run.sh 스펙
5. PDF에서 21, 22, 32, 33, 34p 확인 → 수식·파라미터 대조
6. 04_PROMPTS.md의 Phase 0부터 순차 실행
```

**PDF에서 반드시 확인할 페이지**

| p | 확인 사항 |
|---|---|
| 21 | LLI / LAM_PE / LAM_NE 정의식, α·β 의미 |
| 22 | 현재 fitting 결과 수치 (LAM_PE ≈ LAM_NE 문제) |
| 32 | 6개 열화모드 패널 — 기존 코드가 생성한 그림 |
| 33 | MATLAB fitting 코드의 initial / ub / lb |
| 34 | 개선된 목적함수 J(p) = w_pocv·… + w_dvdq·… + w_dqdv·… |

---

## 2. 환경 자동 구축

### 2.1 시스템 요구사항 탐지

에이전트는 먼저 다음을 확인하고 로그로 남긴다.

```bash
python3 --version              # 3.10~3.12 권장
nvidia-smi                     # GPU 유무 (없어도 진행)
nproc                          # CPU 코어 수 → run.sh 기본 병렬도
free -g                        # 메모리
df -h .                        # 디스크 (grid 결과가 수 GB 나올 수 있음)
```

### 2.2 설치 절차

```bash
# 1) 가상환경
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip wheel

# 2) 핵심 패키지
pip install "pybamm[all]"      # IDAKLU solver 포함
pip install numpy scipy pandas matplotlib openpyxl pyyaml tqdm
pip install joblib             # CPU 병렬
pip install pytest             # 테스트

# 3) (선택) GPU 경로 — nvidia-smi가 잡힐 때만
pip install "jax[cuda12]"      # CUDA 버전에 맞춰 조정
pip install torch --index-url https://download.pytorch.org/whl/cu121   # surrogate용
```

### 2.3 설치 검증 (반드시 통과시킬 것)

```python
# scripts/verify_env.py
import pybamm, numpy, scipy, pandas, matplotlib, yaml
print("pybamm", pybamm.__version__)

# IDAKLU 사용 가능 여부 — 이게 CPU 성능의 핵심
try:
    s = pybamm.IDAKLUSolver()
    print("IDAKLU: OK")
except Exception as e:
    print("IDAKLU: UNAVAILABLE ->", e)
    print("  CasadiSolver로 fallback (2~5배 느림)")

# composite particle phases 모델이 실제로 빌드되는지
m = pybamm.lithium_ion.DFN({
    "particle phases": ("2", "1"),
    "open-circuit potential": (("single", "current sigmoid"), "single"),
})
print("composite DFN: OK")

# GPU
try:
    import jax
    print("jax devices:", jax.devices())
except ImportError:
    print("jax: not installed (CPU-only 경로로 진행)")
```

**IDAKLU가 안 잡히면** 그 사실을 로그에 남기고 CasadiSolver로 진행한다. 중단하지 말 것.

---

## 3. 절대 원칙 (에이전트 준수사항)

1. **기존 코드의 물리 파라미터를 임의로 바꾸지 않는다.**
   `Chen2020_composite` 기반 baseline 값(농도, 부피분율, 공극률)은 그대로 이관한다.
   변경이 필요하면 반드시 커밋 메시지와 `CHANGELOG.md`에 근거를 남긴다.

2. **하드코딩된 완방 상태값(`36.7`, `3446.3`, `58439.9`)을 그대로 쓰지 않는다.**
   원본 코드에 "예전 baseline 기준이라 부정확함, 다시 뽑아야 함"이라는 경고 주석이 있다.
   → `discharged_state.auto_regenerate: true`로 매 실행 시 재계산한다. (02_CODE_AUDIT.md 참조)

3. **Windows 절대경로를 제거한다.** 모든 출력은 `--out` 인자로 받은 디렉터리 아래에만 쓴다.

4. **인터랙티브 matplotlib(Slider/Button)은 서버 실행 경로에서 분리한다.**
   headless 실행이 기본이고, 슬라이더 UI는 `tools/interactive_ab.py`로 따로 뺀다.

5. **각 Phase 끝에서 반드시 커밋한다.** (04_PROMPTS.md의 git 규칙 준수)

6. **GPU를 무리하게 쓰려 하지 않는다.**
   PyBaMM DFN + composite phases는 JAX 백엔드에서 동작하지 않을 가능성이 높다.
   1차 목표는 **CPU 대규모 병렬**이고, GPU는 surrogate 학습·축퇴 지도 후처리에서만 시도한다.
   (03_ARCHITECTURE.md의 "GPU 현실론" 절 참조)

---

## 4. 최종 산출물 정의 (Definition of Done)

```
degradation-degeneracy/
├── README.md
├── run.sh                        # ★ 단일 진입점
├── requirements.txt
├── configs/
│   ├── base.yaml                 # 물리 baseline
│   ├── sweep1d.yaml              # 32p 재현
│   └── grid.yaml                 # 조합 격자
├── src/
│   ├── model.py                  # DFN + composite 빌드
│   ├── baseline.py               # initialization(), 완방상태 자동 산출
│   ├── modes.py                  # LLI / LAM_{pe,ne}×{li,de} 파라미터 변환
│   ├── runner.py                 # 단일 solve
│   ├── sweep.py                  # 1D sweep (32p 재현)
│   ├── grid.py                   # 조합 격자 + 병렬
│   ├── fitting.py                # α·β fitting (33·34p 이식)
│   ├── objective.py              # J(p) — pOCV / dV/dQ / dQ/dV
│   ├── scoring.py                # 축퇴 판정
│   └── io.py                     # 저장·로드 (parquet/hdf5)
├── tools/
│   ├── interactive_ab.py         # 슬라이더 UI (로컬 전용)
│   └── plot_map.py               # 축퇴 지도 그리기
├── tests/
├── results/                      # gitignore
└── docs/                         # 이 md들
```

**성공 기준**

- [ ] `./run.sh --mode sweep1d` 로 32p 그림 6장이 재현된다
- [ ] `./run.sh --mode grid --lam-pe 0:0.2:0.05 --lam-ne 0:0.2:0.05 --lli 0:0.2:0.05 --nproc N` 이 동작한다
- [ ] `./run.sh --mode fit` 이 생성된 곡선에서 α·β를 복원한다
- [ ] `./run.sh --mode score` 가 "정답 vs 복원값" 오차 지도를 출력한다
- [ ] 축퇴 판정 결과가 `results/<run>/degeneracy_map.parquet`에 저장된다
- [ ] 목적함수 4종(pocv / pocv+dvdq / +dqdv / combined) 비교표가 나온다

---

## 5. 막혔을 때

| 상황 | 대응 |
|---|---|
| IDAKLU 설치 실패 | CasadiSolver로 진행, 로그에 명시 |
| composite DFN 빌드 실패 | PyBaMM 버전 확인 (24.x 이상 권장), 옵션 문법 변경 여부 확인 |
| solve 발산 / 수렴 실패 | 해당 조건을 `failed.csv`에 기록하고 **건너뛴다**. 전체 중단 금지 |
| 격자가 너무 커서 시간 초과 | step을 키워 coarse 격자부터. `--dry-run`으로 조건 수 먼저 출력 |
| JAX/GPU 경로 실패 | 예상된 결과. CPU 병렬로 진행하고 사유를 `docs/GPU_NOTES.md`에 기록 |

---

## 6. 다음 파일

→ **`01_CONTEXT.md`** 로 이동. 왜 이 작업을 하는지부터 이해할 것.
