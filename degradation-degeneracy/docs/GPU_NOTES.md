# GPU_NOTES — PyBaMM/DFN을 CUDA에서 돌릴 수 있는가 (실측 기록)

> 질문: "PyBaMM이나 DFN은 CUDA 환경에서 못 하는 건가? CPU 폴백 안 되게 GPU에서 돌리는 방법이 있는데."
> 근거로 제시된 것: 같은 저장소의 `claude/stoic-knuth-NObVQ` 브랜치 (3D geometry, 도전재 cycle).
>
> **결론 먼저**: 그 브랜치는 **PyBaMM을 GPU에서 돌리고 있지 않다.** GPU를 쓰는 것은
> 직접 작성한 voxel 솔버와 MPM이고, PyBaMM은 **CPU 참조(anchor)** 로만 쓰인다.
> 그리고 PyBaMM의 유일한 GPU 경로(JAX)는 우리 모델에서 실측상 사용 불가다.

작성 2026-08-05 / 검증 환경: pybamm 26.7.1.0, jax 0.6.2 (V100과 동일 버전)

---

## 1. `claude/stoic-knuth-NObVQ` 브랜치가 실제로 하는 일

파일을 전수 조사한 결과, GPU 사용처와 PyBaMM 사용처가 **완전히 분리**돼 있다.

| 파일 | 역할 | GPU |
|---|---|---|
| `scripts/step4_dyn.py` | **직접 작성한 voxel-DFN 솔버** (BV + 구형확산, 2.9M DOF) | ✅ CuPy — CG + AMG V-cycle 전처리 |
| `scripts/mpm3d_compaction.py` | MPM 압축 (입자 역학) | ✅ Taichi (`ti.init(arch=cuda)`) |
| `scripts/step3_sigma.py` | 유효 전도도 (복셀 라플라시안) | ✅ CuPy |
| `scripts/step4_pybamm_anchor.py` | **PyBaMM DFN — 균질 트윈 참조** | ❌ **GPU 코드 0줄** |

`step4_pybamm_anchor.py`를 `cupy|cuda|gpu|jax|device`로 grep하면 **결과 0건**이다.
헤더에도 용도가 명시돼 있다:

> "균질 half-cell DFN 트윈: 우리 STEP3 유효값을 pybamm DFN에 넣고 V(t) 대조.
>  균일-구조 극한에서 voxel-v2 ≈ pybamm 수 % = **솔버 검증**;
>  실제 침대와의 편차 = 미세구조 효과의 정량. **cross-fit 금지 — 대조만.**"

즉 그 프로젝트의 구조는 **"GPU = 자체 3D 솔버 / CPU = PyBaMM 참조"** 이고,
이는 우리가 `03_ARCHITECTURE.md` 6절에서 택한 방침과 **정확히 같다**.

### 왜 거기선 GPU가 이겼나 — 문제의 성격이 다르다

| | stoic-knuth의 step4_dyn | 우리 PyBaMM DFN |
|---|---|---|
| 미지수 | **2.9 M DOF** (복셀 격자) | ~10³ (1D 이산화) |
| 병목 | **거대 희소 선형계 반복해** (CG+AMG) | 적응 시간적분 (암시적 DAE) |
| 병렬성 | 격자 전체 동시 — GPU 최적 | 시간축이 인과적으로 직렬 |
| GPU 효과 | 실측 이득 있음 | 커널 실행 오버헤드 > 계산량 |

CG/AMG는 GPU의 교과서적 적지다. 반면 우리 문제는 미지수가 세 자릿수라
GPU에 올리는 순간 데이터 이동 비용이 계산 자체보다 크다.

---

## 2. PyBaMM의 GPU 경로는 하나뿐 — JAX. 그리고 우리 모델에선 막힌다

PyBaMM의 솔버 3종 중 GPU가 가능한 것은 `JaxSolver` 하나다.

| 솔버 | 백엔드 | GPU |
|---|---|---|
| `IDAKLUSolver` (우리 기본) | SUNDIALS + KLU (C) | ❌ CPU 전용 |
| `CasadiSolver` | CasADi (C++) | ❌ CPU 전용 |
| `JaxSolver` | JAX | ✅ 가능 (jax[cuda] 설치 시) |

### 실측 결과 (jax 0.6.2, CPU 백엔드 — GPU 이전에 "동작 여부"부터 판정)

```
SPM            ✓  2.0 s
SPMe           ✓  2.7 s
DFN (단상)      ✗  35분 초과 미완료 (타임아웃)
composite DFN  —  DFN이 안 끝나 도달 못 함
```

비교: **같은 composite DFN을 IDAKLU는 2.4초에 푼다.**

### 막히는 지점 2개

**(A) terminate event 미지원 — 이게 결정타다**

```
RuntimeError: Terminate events not supported for this solver.
```

우리 프로토콜은 전부 이벤트 구동이다 — `"Discharge at 0.05C until 2.5V"`.
JaxSolver는 전압 cutoff에서 멈출 수 없으므로, **실험 프로토콜 자체를 표현할 수 없다.**
고정 시간구간으로 바꾸면 돌지만, 그 순간 "2.5 V까지 방전한 용량"이라는
우리 관측량의 정의가 무너진다. 우회로 없음.

**(B) DFN은 JAX 컴파일이 비현실적으로 느리다**

이벤트를 제거해도 DFN은 35분 안에 끝나지 않았다. JAX가 야코비안을 심볼릭으로
전개·컴파일하는 비용이 DFN 규모에서 폭발한다. GPU를 붙여도 **줄어드는 것은 solve
시간이지 컴파일 시간이 아니다.**

---

## 3. 그래서 "CPU 폴백 없이 GPU로" 는 가능한가

**우리 모델(composite DFN + 이벤트 프로토콜)에 대해서는 불가능하다.** 폴백을 막는
문제가 아니라 **경로가 존재하지 않는다.** `--backend gpu`를 강제 모드로 만들어봐야
`JaxSolver`가 이벤트를 거부하는 지점에서 실패할 뿐이다.

단, **모델을 낮추면 열린다:**

```
SPM  ✓  JAX 2.0 s      ← GPU + vmap 가능
SPMe ✓  JAX 2.7 s      ← GPU + vmap 가능
DFN  ✗                 ← 불가
```

SPMe가 JAX에서 도는 것은 실측으로 확인됐다. 여기에 `jax.vmap`을 걸면
**수천 조건을 한 번에** 태울 수 있고, 이게 GPU가 실제로 이기는 유일한 구도다.
대신 DFN → SPMe 하향의 **곡선 손실을 정량화해야** 하며(Phase 7-2),
그 손실이 우리가 재려는 degeneracy 신호보다 크면 의미가 없다.

---

## 4. 이 프로젝트에서 GPU가 실제로 이득인 곳

| 대상 | GPU | 비고 |
|---|---|---|
| composite DFN solve (Phase 0~3) | ❌ | 경로 없음 (위 §2) |
| α·β fitting 1건 (Phase 4) | ❌ | 미지수 4개, 1초 미만 |
| degeneracy 채점 (Phase 5) | ❌ | 표 연산, 초 단위 |
| **목적함수 가중치 sweep (Phase 6)** | **△** | 3차원 격자면 190만 fitting → JAX vmap 검토 가치. **PyBaMM이 아니라 목적함수만 JAX로 옮기면 되므로 §2의 벽과 무관** |
| **surrogate NN 학습** | **✅** | grid 결과를 학습 데이터로. 원래 GPU 영역 |
| SPMe 배치 곡선 생성 | △ | 위 §3. DFN 손실 정량화 선행 필요 |

**가장 유망한 것은 Phase 6의 목적함수 vmap이다.** 목적함수는 300점 배열의
보간·RMSE·미분뿐이라 인과적 순서 제약이 없고, PyBaMM을 전혀 건드리지 않는다.
난이도가 DFN GPU화(§2, 실패 확정)와 **비교가 안 되게 낮다.**

---

## 5. 재현 방법

```bash
pip install "jax==0.6.2" "jaxlib==0.6.2"     # 0.10 이상은 pybamm과 API 불일치
python - <<'PY'
import pybamm, time
m = pybamm.lithium_ion.SPMe(); m.events = []; m.convert_to_format = "jax"
sim = pybamm.Simulation(m, parameter_values=pybamm.ParameterValues("Chen2020"),
                        solver=pybamm.JaxSolver(method="BDF"))
t0=time.perf_counter(); sol = sim.solve([0, 600])
print(f"{time.perf_counter()-t0:.1f}s, V={sol['Terminal voltage [V]'].entries[-1]:.3f}")
PY
```

`m.events = []` 를 빼면 `RuntimeError: Terminate events not supported`.
`SPMe`를 `DFN`으로 바꾸면 35분 내 미완료.

### 버전 주의

- jax **0.10.x는 pybamm 26.7과 호환 불가**: `jax.core.get_aval`이 0.10.0에서 제거됨
  → `AttributeError`. V100에 깔린 0.6.2가 맞는 버전이다.
- `scripts/setup_env.sh --gpu`는 `requirements-gpu.txt`의 `jax[cuda12]>=0.4.30`을 깔므로
  **최신 jax가 들어올 수 있다.** GPU 실험을 할 때는 버전을 0.6.x로 고정할 것.
