# 02. CODE AUDIT — 기존 코드 분석

> 대상 파일: `degrade_mode_sim_me.py` (437 lines)
> 이 파일은 32p 그림을 생성한 원본이며, 리팩터링의 출발점이다.

---

## 1. 코드가 하는 일 (5블록)

```
[A] 모델 구성       DFN + particle phases ("2","1") + Chen2020_composite
[B] baseline 설정   initialization() — 농도·부피분율·공극률 고정
[C] 완방상태 산출   0.05C 방전 후 각 상의 농도 측정
[D] 모드 sweep      LLI / LAM_pe_de / LAM_ne_de / LAM_pe_li / LAM_ne_li
[E] 출력            xlsx export + 6-panel figure + α·β 슬라이더 UI
```

### 1.1 모델 (A)

```python
model = pybamm.lithium_ion.DFN({
    "particle phases": ("2", "1"),                               # 음극 2상(Gr+Si), 양극 1상
    "open-circuit potential": (("single", "current sigmoid"), "single"),
})
param = pybamm.ParameterValues("Chen2020_composite")
```

- `("2","1")` = **음극이 composite** (Primary=Graphite, Secondary=Si)
- 25p 슬라이드의 "Si와 Gr를 별도 입자로" 가 여기서 구현됨
- `current sigmoid` = Si의 충·방전 OCP 히스테리시스 처리

### 1.2 baseline (B)

```python
def initialization():
    param.update({
        "Primary: Initial concentration in negative electrode [mol.m-3]":   27700.0,
        "Primary: Maximum concentration in negative electrode [mol.m-3]":   28700.0,
        "Secondary: Initial concentration in negative electrode [mol.m-3]": 276610.0,
        "Secondary: Maximum concentration in negative electrode [mol.m-3]": 278000.0,
        "Initial concentration in positive electrode [mol.m-3]":            17038.0,
        "Negative electrode porosity":                                      0.25,
        "Primary: Negative electrode active material volume fraction":      0.735,
        "Secondary: Negative electrode active material volume fraction":    0.015,
        "Positive electrode porosity":                                      0.335,
        "Positive electrode active material volume fraction":               0.665,
    })
```

**완충(charged) 상태 기준.** Si 부피분율 0.015 = 전체 음극 활물질의 약 2%.

### 1.3 모드별 파라미터 변환 (D) — 이 프로젝트의 핵심 로직

| 모드 | 조작 | 물리적 의미 |
|---|---|---|
| **LLI** | `Primary/Secondary Init conc × (1−i)` | 리튬 재고만 감소, 활물질은 그대로 |
| **LAM_ne_li** | `vf × (1−i)`, `porosity += (0.735+0.015)·i` | 리튬화된 상태로 음극 활물질 손실 |
| **LAM_ne_de** | 위 + 완방상태 농도를 `/(1−i)` 로 보정 | 탈리튬화 상태로 손실 |
| **LAM_pe_li** | `pe_vf × (1−i)`, `pe_porosity += 0.665·i` | 리튬화된 상태로 양극 손실 |
| **LAM_pe_de** | 위 + `pe init conc / (1−i)` | 탈리튬화 상태로 손실 |

**li / de 구분 핵심**: 활물질이 **Li을 품은 채** 죽으면 LLI를 동반(곡선 shift 발생),
**빈 상태로** 죽으면 용량만 감소(shrinkage만). 32p 패널의 자물쇠 아이콘이 이 표시.

**experiment 프로토콜도 모드마다 다름**

```python
experiment  = [방전 → rest → 충전 → rest → 방전]   # LLI, LAM_ne_li
experiment2 = [충전 → rest → 방전]                  # LAM_ne_de, LAM_pe_li, LAM_pe_de
```

→ 리팩터링 시 **모드↔프로토콜 매핑을 반드시 보존**할 것. 임의로 통일하면 결과가 달라진다.

### 1.4 α·β 슬라이더 (E)

```python
def windowed_curve(f_ref, x_cell_norm, alpha, beta):
    sto = (x_cell_norm - beta) / alpha
    y = f_ref(np.clip(sto, 0, 1))
    return np.where((sto >= 0) & (sto <= 1), y, np.nan)

LAM_PE = (1 - a_pe) * 100
LAM_NE = (1 - a_ne) * 100
LLI    = ((1 - a_pe) + (b_pe - b_ne)) * 100    # Birkl 2017 부호 규약
```

21p 방법론의 **정방향(forward) 구현**. fitting은 이것의 역방향이다.
→ `src/fitting.py`는 이 `windowed_curve`를 그대로 재사용해야 한다.

---

## 2. 문제점 — 반드시 고칠 것

### 🔴 CRITICAL

#### C1. 완방상태 하드코딩 (stale baseline)

```python
"Primary: Initial concentration in negative electrode [mol.m-3]": 36.7 / (1-i),
"Secondary: Initial concentration in negative electrode [mol.m-3]": 3446.3 / (1-i),
"Initial concentration in positive electrode [mol.m-3]": 58439.9,
```

원본 코드에 **이미 경고 주석이 달려 있다**:

> "baseline이 바뀌었으므로 하드코딩 값(428, 82591, 62877.0)은 예전 baseline 기준이라
> 더 이상 정확하지 않음. 다시 뽑아서 교체해야 함"

즉 주석의 값(428, 82591, 62877)과 실제 코드값(36.7, 3446.3, 58439.9)이 다르고,
**어느 쪽이 현행 baseline과 일치하는지 보장이 없다.**

**→ 조치**: `baseline.py`에서 매 실행 시 방전 시뮬레이션으로 자동 산출.
결과를 캐시하되, baseline 파라미터 해시가 바뀌면 무효화.

```python
def get_discharged_state(param, model, cache_dir):
    key = hash_of(baseline_params)
    if cached(key): return load(key)
    sol = solve(["Discharge at 0.05C until 2.5V", "Discharge at 2.5V until 0.02C"])
    return {"ne_primary": ..., "ne_secondary": ..., "pe": ...}
```

#### C2. 전역 mutable `param` — 병렬화 불가

```python
def run_sweep(experiment, sweep_values, update_fn):
    for i in sweep_values:
        param.update(update_fn(i))      # ← 전역 객체 변형
        sim = pybamm.Simulation(model, parameter_values=param, ...)
        solutions.append(sim.solve())
        initialization()                # ← 매번 수동 리셋
```

`initialization()` 호출을 한 번이라도 빠뜨리면 **이전 조건이 누적**된다.
실제로 코드 안에 "Reference와 LLI=0이 같은 값인지" 확인하는 디버그 블록이 있는 것 자체가
이 위험을 저자도 인지하고 있다는 증거.

**→ 조치**: 순수 함수로 전환. `param`을 매번 새로 복제해서 넘긴다.

```python
def build_param(baseline: dict, overrides: dict) -> pybamm.ParameterValues:
    p = pybamm.ParameterValues("Chen2020_composite")
    p.update(baseline); p.update(overrides)
    return p                                   # 전역 상태 없음 → 병렬 안전
```

#### C3. Windows 절대경로

```python
r"C:\Users\ga117\OneDrive\!BML\python\params.txt"
r"C:\Users\ga117\OneDrive\!BML\python\degradation_data.xlsx"
```

Linux/GPU 서버에서 즉시 실패.

**→ 조치**: 모든 출력은 `--out` 인자 하위. `pathlib.Path` 사용.

#### C4. `os.chdir(pybamm.__path__[0] + "/..")`

패키지 설치 경로로 작업 디렉터리를 옮긴다. venv/conda 환경에서 예측 불가하고,
상대경로 출력이 엉뚱한 곳에 쌓인다.

**→ 조치**: 삭제.

---

### 🟡 MAJOR

#### M1. 순차 실행 — 병렬화 없음

`run_sweep`의 for-loop가 유일한 실행 경로. 5개 모드 × 4값 = 20회를 순차 처리.
조합 격자(9,261개)로 확장하면 **수일** 소요.

**→ 조치**: `joblib.Parallel` 또는 `multiprocessing.Pool`.
조건 간 완전 독립이므로 embarrassingly parallel.

#### M2. 인터랙티브 UI가 메인 스크립트에 포함

`Slider`, `Button`, `fig.canvas.draw_idle()` — headless 서버에서 실행 불가.

**→ 조치**: `tools/interactive_ab.py`로 분리. 메인 경로는 `matplotlib.use("Agg")`.

#### M3. 1D sweep만 지원

`run_sweep`이 스칼라 하나(`i`)만 받는다. LAM_PE와 LAM_NE를 **동시에** 넣을 수 없다.

**→ 조치**: `update_fn`을 dict를 받도록 일반화.

```python
def build_overrides(mode_values: dict, baseline: dict, discharged: dict) -> dict:
    # {"lli": 0.10, "lam_pe": 0.05, "lam_ne": 0.15, "lam_type": "de"}
    # → 중첩 적용된 파라미터 dict 반환
```

> **주의**: 모드를 중첩 적용할 때 `porosity`와 `vf`가 서로 간섭한다.
> LAM_NE와 LLI를 동시에 넣으면 초기농도 보정 순서에 따라 결과가 달라질 수 있다.
> **적용 순서를 명시적으로 고정**하고 문서화할 것. (권장: LAM → LLI 순)

#### M4. solver 미지정

`sim.solve()` 기본값(CasadiSolver) 사용. IDAKLU가 DFN에서 통상 2~5배 빠르다.

**→ 조치**: config에서 solver 선택 가능하게. 기본값 IDAKLU, 없으면 Casadi fallback.

#### M5. 실패 처리 없음

한 조건이 발산하면 전체 스크립트가 죽는다. 9천 조건 중 하나만 실패해도 전부 손실.

**→ 조치**: try/except로 감싸고 `failed.csv`에 기록 후 계속 진행.

---

### 🟢 MINOR

| # | 항목 | 조치 |
|---|---|---|
| m1 | xlsx export — 9천 조건엔 부적합 | parquet 또는 HDF5 |
| m2 | `ltype` 색 배열 7개 고정 | 조건 수 많으면 colormap |
| m3 | `n_trim = 3` 매직넘버 | config로 노출 |
| m4 | 디버그 print가 코드에 상주 | `logging` 모듈 |
| m5 | 한글 주석/출력 | 유지해도 무방 (UTF-8 명시) |

---

## 3. 반드시 보존할 것 (건드리지 말 것)

1. **모델 옵션** — `("2","1")`, `current sigmoid` 조합
2. **baseline 수치** — 농도·부피분율·공극률 10개 값
3. **모드별 파라미터 변환식** — 특히 `porosity += vf_total × i` 관계
4. **모드↔프로토콜 매핑** — `experiment` vs `experiment2`
5. **`windowed_curve` 로직** — `sto = (x − β)/α`, 범위 밖 NaN
6. **LLI 부호 규약** — `LLI = (1−α_PE) + (β_PE − β_NE)`, Birkl 2017 기준
7. **전압 cutoff** — 4.2 / 2.5 V, C-rate 0.05

---

## 4. 리팩터링 우선순위

| 순위 | 항목 | 근거 |
|---|---|---|
| 1 | C1 완방상태 자동화 | 이게 틀리면 **모든 결과가 무의미** |
| 2 | C2 전역 param 제거 | 병렬화의 전제조건 |
| 3 | C3·C4 경로 정리 | 서버 실행 불가 |
| 4 | M3 다차원 조합 | 프로젝트 목적 자체 |
| 5 | M1 병렬화 | 실행 시간 |
| 6 | M5 실패 처리 | 대규모 실행 안정성 |
| 7 | M2 UI 분리 | headless |
| 8 | M4 solver | 성능 |

---

## 5. 검증 기준 — 리팩터링이 맞는지 확인

리팩터링 후 **반드시** 다음을 통과해야 한다.

```python
# tests/test_regression.py
def test_reproduces_original_32p():
    """기존 코드와 동일 조건에서 곡선이 일치하는가"""
    for mode in ["LLI", "LAM_ne_li", "LAM_ne_de", "LAM_pe_li", "LAM_pe_de"]:
        for val in [0, 0.1, 0.2, 0.3]:
            new = run_new(mode, val)
            ref = load_reference(mode, val)      # 원본 코드 출력 저장본
            assert np.allclose(new.voltage, ref.voltage, rtol=1e-4)

def test_zero_degradation_equals_reference():
    """모든 모드 0%일 때 reference와 동일해야 함 (원본 디버그 블록의 의도)"""
    assert abs(cap(mode_all_zero) - cap(reference)) < 1e-2   # mAh
```

**두 번째 테스트가 특히 중요하다.** 원본 코드에 이 검증이 print문으로 들어 있는 것은
저자가 baseline 오염을 실제로 겪었다는 뜻이다.

---

## 6. 다음 파일

→ **`03_ARCHITECTURE.md`** — 목표 구조와 run.sh 스펙
