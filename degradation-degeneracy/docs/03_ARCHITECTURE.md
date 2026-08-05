# 03. ARCHITECTURE — 목표 구조 · run.sh 스펙

---

## 1. 저장소 구조

```
degradation-degeneracy/
├── README.md
├── run.sh                       # ★ 단일 진입점 (모든 실행은 여기로)
├── requirements.txt
├── requirements-gpu.txt         # 선택
├── .gitignore                   # results/, .venv/, *.parquet
│
├── configs/
│   ├── base.yaml                # 물리 baseline (건드리지 말 것)
│   ├── sweep1d.yaml             # 32p 재현
│   ├── grid_coarse.yaml         # step 0.05 → 125조합 (스모크)
│   ├── grid_fine.yaml           # step 0.02 → 9,261조합 (본실행)
│   └── objectives.yaml          # 목적함수 4종 정의
│
├── src/
│   ├── __init__.py
│   ├── config.py                # yaml 로드 + 검증 + 해시
│   ├── model.py                 # DFN + composite 빌드 (캐시)
│   ├── baseline.py              # initialization + 완방상태 자동 산출
│   ├── modes.py                 # ★ 모드 → 파라미터 변환 (중첩 지원)
│   ├── protocol.py              # experiment / experiment2 매핑
│   ├── runner.py                # 단일 solve (순수 함수)
│   ├── sweep.py                 # 1D sweep (32p 재현)
│   ├── grid.py                  # 조합 격자 + 병렬 실행
│   ├── curves.py                # pOCV / dV/dQ / dQ/dV 변환
│   ├── objective.py             # J(p) — 34p 목적함수
│   ├── fitting.py               # α·β 최적화 (33p 이식)
│   ├── scoring.py               # 축퇴 판정
│   ├── hessian.py               # 조건수 · 고윳값 분석
│   └── io.py                    # parquet 저장/로드, 매니페스트
│
├── tools/
│   ├── interactive_ab.py        # 슬라이더 UI (로컬 전용)
│   ├── plot_sweep1d.py          # 32p 6-panel 재현
│   ├── plot_map.py              # 축퇴 지도
│   └── compare_objectives.py    # 목적함수 4종 비교표
│
├── tests/
│   ├── test_regression.py       # 원본 코드 재현 검증
│   ├── test_modes.py            # 모드 중첩 순서 검증
│   └── test_fitting.py          # α=1,β=0 항등 검증
│
├── results/                     # gitignore
│   └── <run_id>/
│       ├── manifest.yaml        # 실행 조건 + git commit + 환경
│       ├── curves.parquet
│       ├── fits.parquet
│       ├── degeneracy_map.parquet
│       ├── failed.csv
│       └── figures/
│
└── docs/                        # 이 md 파일들
```

---

## 2. run.sh 스펙 ★

### 2.1 기본 형태

```bash
./run.sh --mode <MODE> [옵션...]
```

### 2.2 모드

| mode | 설명 | 대략 소요 |
|---|---|---|
| `verify` | 환경 검증 (IDAKLU, composite DFN, GPU) | 1분 |
| `baseline` | 완방상태 산출 및 캐시 | 2분 |
| `sweep1d` | 32p 재현 — 모드별 1D sweep | 10분 |
| `grid` | ★ 조합 격자 곡선 생성 | 시간~일 |
| `fit` | 생성된 곡선에 α·β fitting | 시간 |
| `score` | 축퇴 판정 · 지도 생성 | 분 |
| `hessian` | 조건수 · 고윳값 분석 | 분 |
| `report` | 그림 + 표 생성 | 분 |
| `all` | grid → fit → score → report | — |

### 2.3 인자 전체

```bash
./run.sh \
  --mode grid \
  --config configs/grid_fine.yaml \
  \
  `# ── 열화 모드 축 (start:stop:step 또는 콤마 목록) ──` \
  --lli        0:0.20:0.02 \
  --lam-pe     0:0.20:0.02 \
  --lam-ne     0:0.20:0.02 \
  --lam-pe-type de \                 # de | li | both
  --lam-ne-type de \                 # de | li | both
  \
  `# ── 실험 조건 ──` \
  --c-rate     0.05 \
  --v-upper    4.2 \
  --v-lower    2.5 \
  \
  `# ── 노이즈 (합성 데이터 현실성) ──` \
  --noise      0,0.001,0.005 \       # V, gaussian
  --noise-seed 42 \
  \
  `# ── fitting 설정 ──` \
  --objective  pocv,pocv_dvdq,pocv_dvdq_dqdv,combined \
  --w-pocv     1.0 \
  --w-dvdq     1.0 \
  --w-dqdv     0:2:0.5 \             # 가중치도 sweep 가능
  --init-guess 1.03,-0.1,1.08,-0.01 \
  --bounds-lb  1.00,-0.30,1.00,-0.15 \
  --bounds-ub  1.10,0.00,1.10,0.00 \
  --n-restarts 5 \                   # multi-start (축퇴 진단용)
  \
  `# ── 실행 제어 ──` \
  --backend    cpu \                 # cpu | gpu
  --nproc      32 \
  --solver     idaklu \              # idaklu | casadi
  --chunk-size 200 \
  --resume \                         # 중단 지점부터 재개
  --dry-run \                        # 조건 수·예상시간만 출력
  \
  `# ── 출력 ──` \
  --out        results/grid_fine_v1 \
  --tag        "dqdv-objective-test" \
  --log-level  INFO
```

### 2.4 축 문법

| 표기 | 해석 |
|---|---|
| `0:0.2:0.02` | 0부터 0.2까지 0.02 간격 (11개) |
| `0,0.05,0.1,0.2` | 명시 목록 (4개) |
| `0.1` | 단일값 |
| `none` | 이 축 비활성 |

### 2.5 필수 동작

1. **`--dry-run` 먼저 지원할 것.** 조건 수와 예상 시간을 출력하고 종료.
   ```
   [dry-run] LLI 11 × LAM_PE 11 × LAM_NE 11 × noise 3 = 3,993 conditions
   [dry-run] est. 4.2 s/cond × 3993 / 32 proc ≈ 8.7 min
   [dry-run] est. output size ≈ 1.2 GB
   ```

2. **`--resume` 지원.** `manifest.yaml`에 완료 조건을 기록하고, 재실행 시 건너뛴다.

3. **실패 격리.** 발산 조건은 `failed.csv`에 `(조건, 예외메시지)` 기록 후 계속.

4. **매니페스트 기록.** 모든 실행은 재현 가능해야 한다.
   ```yaml
   run_id: grid_fine_v1
   timestamp: 2026-08-05T14:23:11
   git_commit: a3f9c21
   git_dirty: false
   config_hash: 7b2e...
   pybamm_version: 24.5
   solver: idaklu
   nproc: 32
   n_conditions: 3993
   n_failed: 7
   ```

---

## 3. Config 스키마

### 3.1 `configs/base.yaml` — 물리 baseline

```yaml
model:
  type: DFN
  particle_phases: ["2", "1"]          # 음극 composite (Gr + Si)
  open_circuit_potential:
    negative: ["single", "current sigmoid"]
    positive: "single"

parameter_set: Chen2020_composite

cell:
  upper_voltage_cutoff: 4.2
  lower_voltage_cutoff: 2.5

# ── 완충 상태 기준 baseline. 임의 변경 금지 ──
baseline:
  ne_primary_init_conc:   27700.0      # mol/m3
  ne_primary_max_conc:    28700.0
  ne_secondary_init_conc: 276610.0
  ne_secondary_max_conc:  278000.0
  pe_init_conc:           17038.0
  pe_max_conc:            63104.0      # print문에서 역산된 값
  ne_porosity:            0.25
  ne_primary_vf:          0.735        # Graphite
  ne_secondary_vf:        0.015        # Si
  pe_porosity:            0.335
  pe_vf:                  0.665

# ── 완방 상태: 하드코딩 금지, 자동 산출 ──
discharged_state:
  auto_regenerate: true
  cache: true
  protocol: ["Discharge at 0.05C until 2.5V", "Discharge at 2.5V until 0.02C"]
  # 산출 결과가 여기 캐시됨 (baseline 해시 변경 시 무효화)

protocol:
  c_rate: 0.05
  rest_minutes: 10
  discharge_first:                      # 원본 `experiment`
    - "Discharge at 0.05 C until 2.5 V"
    - "Rest for 10 minutes"
    - "Charge at 0.05 C until 4.2 V"
    - "Rest for 10 minutes"
    - "Discharge at 0.05 C until 2.5 V"
  charge_first:                         # 원본 `experiment2`
    - "Charge at 0.05 C until 4.2 V"
    - "Rest for 10 minutes"
    - "Discharge at 0.05 C until 2.5 V"

# ── 모드 ↔ 프로토콜 매핑 (원본 유지, 변경 금지) ──
mode_protocol:
  reference:  discharge_first
  lli:        discharge_first
  lam_ne_li:  discharge_first
  lam_ne_de:  charge_first
  lam_pe_li:  charge_first
  lam_pe_de:  charge_first

solver:
  type: idaklu
  fallback: casadi
  rtol: 1.0e-6
  atol: 1.0e-6

postprocess:
  n_trim: 3                             # cutoff 근처 절단 포인트 수
  n_interp: 300                         # 정규화 용량 격자
```

### 3.2 `configs/objectives.yaml`

```yaml
objectives:
  pocv:
    w_pocv: 1.0
    w_dvdq: 0.0
    w_dqdv: 0.0

  pocv_dvdq:                            # 기존(33p) 방식
    w_pocv: 1.0
    w_dvdq: 1.0
    w_dqdv: 0.0

  pocv_dvdq_dqdv:                       # 34p 개선안
    w_pocv: 1.0
    w_dvdq: 1.0
    w_dqdv: 1.0

  dqdv_only:
    w_pocv: 0.0
    w_dvdq: 0.0
    w_dqdv: 1.0

# 각 항은 scale로 정규화 (34p 수식)
#   J(p) = w_pocv·RMSE_pocv/scale_pocv
#        + w_dvdq·RMSE_dvdq/scale_dvdq
#        + w_dqdv·RMSE^w_dqdv/scale_dqdv
scaling:
  method: reference_rmse                # baseline 조건의 RMSE로 정규화

dqdv:
  smoothing: savgol                     # 33p "peak smoothing control parameter"
  window: 21
  polyorder: 3
  peak_weight: 3.0                      # 33p "peak weight factor"
  peak_prominence: 0.05
```

---

## 4. 모드 중첩 규칙 ★ (가장 주의할 부분)

여러 모드를 동시에 적용할 때 파라미터가 서로 간섭한다. **적용 순서를 고정한다.**

```python
def build_overrides(lli, lam_pe, lam_ne, lam_pe_type, lam_ne_type,
                    baseline, discharged) -> dict:
    """
    적용 순서 (고정):
      1) LAM_PE  — pe_vf, pe_porosity, (de면 pe 농도 보정)
      2) LAM_NE  — ne_vf×2, ne_porosity, (de면 ne 농도 보정)
      3) LLI     — 최종 ne 초기농도에 (1−lli) 곱
    """
    ov = {}

    # 1) LAM_PE
    if lam_pe > 0:
        ov["Positive electrode active material volume fraction"] = baseline.pe_vf * (1 - lam_pe)
        ov["Positive electrode porosity"] = baseline.pe_porosity + baseline.pe_vf * lam_pe
        if lam_pe_type == "de":
            ov["Initial concentration in positive electrode [mol.m-3]"] = \
                discharged.pe / (1 - lam_pe)
        else:  # li
            ov["Initial concentration in positive electrode [mol.m-3]"] = discharged.pe

    # 2) LAM_NE
    if lam_ne > 0:
        vf_tot = baseline.ne_primary_vf + baseline.ne_secondary_vf
        ov["Primary: Negative electrode active material volume fraction"]   = baseline.ne_primary_vf * (1 - lam_ne)
        ov["Secondary: Negative electrode active material volume fraction"] = baseline.ne_secondary_vf * (1 - lam_ne)
        ov["Negative electrode porosity"] = baseline.ne_porosity + vf_tot * lam_ne
        if lam_ne_type == "de":
            ov["Primary: Initial concentration in negative electrode [mol.m-3]"]   = discharged.ne_primary / (1 - lam_ne)
            ov["Secondary: Initial concentration in negative electrode [mol.m-3]"] = discharged.ne_secondary / (1 - lam_ne)

    # 3) LLI — 마지막에 적용
    if lli > 0:
        base_p = ov.get("Primary: Initial concentration in negative electrode [mol.m-3]",
                        baseline.ne_primary_init_conc)
        base_s = ov.get("Secondary: Initial concentration in negative electrode [mol.m-3]",
                        baseline.ne_secondary_init_conc)
        ov["Primary: Initial concentration in negative electrode [mol.m-3]"]   = base_p * (1 - lli)
        ov["Secondary: Initial concentration in negative electrode [mol.m-3]"] = base_s * (1 - lli)

    return ov
```

**검증 필수**

```python
def test_mode_composition():
    # 단일 모드는 원본과 동일해야 함
    assert build_overrides(lli=0.1, lam_pe=0, lam_ne=0, ...) == original_lli_override(0.1)
    # 모두 0이면 override 없음
    assert build_overrides(0, 0, 0, ...) == {}
    # 순서 무관성이 깨지는 조합을 명시적으로 문서화
```

> ⚠️ **주의**: 프로토콜이 모드마다 달랐는데(`experiment` vs `experiment2`),
> 조합 시에는 하나를 골라야 한다. **`charge_first`로 통일하되 그 사실을 매니페스트에 기록**하고,
> `sweep1d` 모드에서는 원본 매핑을 유지해 재현성을 확보한다.

---

## 5. 축퇴 판정 기준

```python
# src/scoring.py
def score(truth: dict, recovered: dict) -> dict:
    """
    truth     : {"lli": 0.10, "lam_pe": 0.05, "lam_ne": 0.15}
    recovered : fitting 결과
    """
    err = {k: recovered[k] - truth[k] for k in truth}

    return {
        **{f"err_{k}": v for k, v in err.items()},
        "abs_err_max": max(abs(v) for v in err.values()),
        # 축퇴의 특징적 지문: PE와 NE 오차가 서로 반대 부호로 상쇄
        "pe_ne_antisym": err["lam_pe"] * err["lam_ne"] < 0,
        "pe_ne_gap_true": abs(truth["lam_pe"] - truth["lam_ne"]),
        "pe_ne_gap_recovered": abs(recovered["lam_pe"] - recovered["lam_ne"]),
        # 판정
        "degenerate": abs_err_max > TOL,          # TOL = 0.02 (2%p)
    }
```

**축퇴 지도 출력**

```
degeneracy_map.parquet
├── lli, lam_pe, lam_ne, lam_type, noise, objective
├── recovered_lli, recovered_lam_pe, recovered_lam_ne
├── err_*, abs_err_max
├── degenerate (bool)
├── n_restarts_agree      # multi-start 결과 일치 개수 → 해의 유일성 지표
└── J_final, n_iter, converged
```

**핵심 요약 지표**

```
축퇴 영역 비율 = degenerate.sum() / len(df)

objective별 비교:
  pocv           : 62%
  pocv_dvdq      : 41%      ← 기존 (33p)
  pocv_dvdq_dqdv : 18%      ← 개선 (34p)   "축퇴 41% → 18%로 감소"
```

---

## 6. GPU 현실론 ★

> 이 절을 반드시 읽고 판단할 것. 무리한 GPU 적용은 시간 낭비다.

### 6.1 GPU가 **안 되는** 것

| 대상 | 이유 |
|---|---|
| **PyBaMM DFN 단일 solve** | stiff DAE 암시적 시간적분. 시간축이 인과적으로 묶여 병렬화 불가. 미지수 수백~수천 개는 GPU 커널 오버헤드가 계산량보다 큼 |
| **composite phases + JAX** | `convert_to_format="jax"`가 2상 입자 모델에서 실패할 가능성이 높음. 시도는 하되 **실패를 전제로 계획할 것** |
| **fitting 자체** | 미지수 4개 최적화. 몇 초면 끝나므로 가속 의미 없음 |
| **축퇴 해결** | 정보 부족 문제. 계산 자원으로 풀리지 않음 |

### 6.2 GPU가 **되는** 것

| 대상 | 방법 | 조건 |
|---|---|---|
| **대규모 배치 곡선 생성** | JAX + `vmap`, SPMe급으로 모델 하향 | DFN 포기 필요 |
| **surrogate 학습** | grid 결과를 학습 데이터로, PyTorch NN | 데이터 확보 후 |
| **Hessian 해석적 계산** | JAX 자동미분 | 모델 JAX화 성공 시 |
| **지도 후처리·시각화** | cuDF, cuML | 데이터 크면 |

### 6.3 권장 실행 경로

```
[1차] CPU 대규모 병렬     ← 현실적이고 확실함. 이것부터.
      nproc = 코어 수, IDAKLU solver
      9,261 조건 × 4.2s / 32proc ≈ 20분

[2차] GPU 시도 (선택)
      SPMe로 하향 → JAX vmap → 배치 1000개
      실패해도 1차 결과로 목적 달성 가능

[3차] surrogate (후속)
      1차 데이터로 NN 학습 → GPU 유효
```

**`--backend gpu`는 인터페이스만 만들어두고, 내부는 CPU fallback으로 시작한다.**
GPU 경로가 실제로 동작하면 그때 채운다.

### 6.4 CPU 성능 최적화 (실질적 이득)

```python
# 1) IDAKLU — 통상 2~5배
solver = pybamm.IDAKLUSolver(rtol=1e-6, atol=1e-6)

# 2) 모델 1회 빌드 후 재사용 (discretisation 캐시)
#    조건마다 새로 빌드하면 오버헤드가 solve보다 큼

# 3) joblib — 프로세스 병렬
from joblib import Parallel, delayed
results = Parallel(n_jobs=nproc, backend="loky")(
    delayed(run_one)(cond) for cond in conditions
)

# 4) 청크 단위 저장 — 메모리 폭발 방지
for chunk in chunks(conditions, size=200):
    save_parquet(run_chunk(chunk), out / f"chunk_{i}.parquet")
```

---

## 7. 다음 파일

→ **`04_PROMPTS.md`** — 단계별 실행 프롬프트 (git 연동)
