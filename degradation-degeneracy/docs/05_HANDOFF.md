# 05. HANDOFF — 구축된 환경 설명서

> **읽는 사람**: 이가형 (원본 `degrade_mode_sim_me.py` 작성자)
> **한 줄 요약**: 가형님 스크립트를 서버에서 **수천 조건 병렬로** 돌릴 수 있는 형태로
> 이식하고, 아무 머신에서나 **명령 한 줄로** 같은 환경이 재현되게 만들어 뒀습니다.
> 물리 수식과 파라미터는 그대로입니다. 바꾼 것은 아래 §5에 전부 적어 뒀습니다.

작성일: 2026-08-05 / 대상 브랜치: `claude/zip-git-gpu-setup-vdqdtd`

---

## 1. 왜 이 작업이 필요했나

원본 스크립트는 **한 번에 모드 하나만**(LLI만, LAM_NE만…) 넣어서 32p 그림을 만듭니다.
그런데 실제 셀은 LLI·LAM_PE·LAM_NE가 **동시에** 일어나므로, 22p의
`LAM_PE ≈ LAM_NE ≈ 13%`가 진짜인지 fitting degeneracy인지 확인하려면
**조합 격자를 훑어야** 합니다.

```
LAM_PE 11단계 × LAM_NE 11단계 × LLI 11단계 × 노이즈 3종 = 3,993 조건
```

원본의 순차 for-loop로는 하루가 걸리고, 전역 `param`을 계속 덮어쓰는 구조라
병렬화 자체가 불가능했습니다. 그래서 **물리는 그대로 두고 실행 구조만** 바꿨습니다.

실제 실행 결과: **V100 서버 32코어에서 fine 격자가 5~8분**입니다.

---

## 2. 시작하기 — 명령 세 줄

새 서버든 새 노트북이든 똑같습니다.

```bash
git clone https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT.git
cd Yonghoon-DEM-DFT/degradation-degeneracy
./scripts/setup_env.sh
```

`setup_env.sh`가 알아서 다 합니다:

1. 시스템 탐지 (CPU 코어 / 메모리 / 디스크 / **GPU 자동 감지**)
2. `.venv` 가상환경 생성
3. `pybamm[all]` 등 설치 — 네트워크 끊겨도 자동 재시도
4. GPU가 있으면 jax(CUDA) 추가 설치, **없으면 그냥 건너뜀** (있어도 그만 없어도 그만)
5. 환경 검증 후 `docs/ENV_REPORT.md` 생성

몇 번을 다시 실행해도 안전합니다. 환경이 꼬였으면 `./scripts/setup_env.sh --recreate`.

검증 리포트에서 이 세 줄만 확인하시면 됩니다.

```
[OK] IDAKLU: 사용 가능 (권장)              ← 없으면 2~5배 느려지지만 진행은 됨
[OK] composite DFN 빌드 성공 (particle phases 2,1)
[OK] Chen2020_composite 파라미터셋 로드 성공
```

---

## 3. 실행 방법 — 전부 `run.sh` 하나로

```bash
source .venv/bin/activate

./run.sh --mode verify                                    # 환경 재검증
./run.sh --mode baseline                                  # 완방상태 산출·캐시
./run.sh --mode sweep1d --out results/sweep1d_v1          # ★ 32p 그림 재현
./run.sh --mode grid --config configs/grid_coarse.yaml --dry-run   # 조건 수·예상시간만
./run.sh --mode grid --config configs/grid_fine.yaml --nproc 32 --out results/grid_fine_v1

# ── 여기서부터가 채점 단계 ──
./run.sh --mode fit     --in results/grid_fine_v1 --nproc 32   # α·β fitting (약 5시간)
./run.sh --mode score   --in results/grid_fine_v1              # degeneracy 판정·지도
./run.sh --mode hessian --in results/grid_fine_v1              # 곡률(flat direction) 진단
./run.sh --mode report  --in results/grid_fine_v1              # 비교표 + docs/RESULTS.md
./run.sh --mode wsweep  --in results/grid_fine_v1 --nproc 32   # 가중치 근거 (약 70분)

./run.sh --mode all --config configs/grid_fine.yaml --nproc 32 --out results/final_v1
#   grid → fit → score → hessian → report 를 한 번에
```

**꼭 알아두실 것 세 가지**

| | |
|---|---|
| `--dry-run` | 실제 계산 전에 **조건 수 / 예상 시간 / 예상 용량**을 실측 기반으로 알려줍니다. 큰 격자는 항상 이것부터 |
| `--resume` | 중간에 끊겨도 **완료된 조건은 건너뛰고** 이어서 갑니다. SSH 끊김·서버 재부팅 대비 |
| `tmux` | 긴 실행은 반드시 `tmux new -s grid` 안에서. 안 그러면 SSH 끊길 때 같이 죽습니다 (실제로 한 번 겪었습니다) |
| 동시 실행 금지 | 같은 `--out`에 두 개를 띄우면 막힙니다(`.run.lock` / `.fit.lock`). 막히기 전에 뚫린 적이 있어서 8절 아래 "실제로 겪은 사고들"에 남겨뒀습니다 |

한 조건이 발산해도 **전체가 죽지 않습니다.** `failed.csv`에 사유를 남기고 계속 진행합니다.

---

## 4. 저장소 구조 — 원본 코드가 어디로 갔나

원본 스크립트 437줄이 역할별로 나뉘었습니다. 파일명 옆이 원본의 해당 부분입니다.

```
src/
  config.py     yaml 로드·검증                        (신규)
  model.py      DFN + particle phases ("2","1")        ← 원본 L34-39
  baseline.py   initialization() + 완방상태 자동산출    ← 원본 L69-103
  modes.py      ★ 모드→파라미터 변환                   ← 원본 update_fn 5개
  protocol.py   experiment / experiment2               ← 원본 L52-67
  runner.py     단일 solve                             ← 원본 run_sweep 내부
  sweep.py      1D sweep (32p)                         ← 원본 L129-216
  curves.py     곡선 추출·dV/dQ·dQ/dV                  ← 원본 L265-351
  grid.py       ★ 조합 격자 + 병렬                     (신규 — 이번 작업의 핵심)
  io.py         parquet 저장·manifest                  ← 원본 xlsx export 대체

tools/
  plot_sweep1d.py    32p 6-panel 그림                  ← 원본 L304-318
  interactive_ab.py  α·β 슬라이더 UI                   ← 원본 L321-436 (그대로 분리)
  plot_grid_summary.py  격자 용량 지도                 (신규)

configs/           물리 baseline·격자·목적함수 정의 (yaml)
tests/             회귀 검증 56개
reference/         ★ 원본 스크립트 원본 그대로 (수정 금지 — 비교 기준)
```

**α·β 슬라이더는 없어지지 않았습니다.** 서버에서 돌 때 창이 뜨면 안 되니까
`tools/interactive_ab.py`로 분리만 했습니다. 로컬에서 예전처럼 쓰시면 됩니다.

```bash
python tools/interactive_ab.py --in results/sweep1d_v1
```

---

## 5. 원본에서 바뀐 것 — 전부 여기 있습니다

물리에 영향 있는 변경은 **3건**이고, 모두 `CHANGELOG.md`와 `physics(...)` 커밋에
근거를 남겼습니다. 나머지는 구조 변경뿐입니다.

### 5-1. 완방상태 하드코딩 → 자동 산출 ★

원본 코드의 이 값들입니다.

```python
"Primary: Initial concentration ...": 36.7 / (1-i),
"Secondary: Initial concentration ...": 3446.3 / (1-i),
"Initial concentration in positive electrode ...": 58439.9,
```

코드에 *"baseline이 바뀌었으므로 예전 값이라 부정확함, 다시 뽑아야 함"* 이라고
주석을 달아 두신 부분입니다. 매 실행 시 0.05C 방전으로 새로 뽑도록 바꿨습니다.

**실제로 뽑아보니:**

| | 원본 하드코딩 | 자동 산출 | 차이 |
|---|---|---|---|
| 흑연 | 36.7 | **36.6** | 0.3% |
| Si | 3446.3 | **3446.1** | 0.006% |
| 양극 | 58439.9 | **58439.9** | 0.0% |

→ **걱정하셨던 값들은 현행 baseline과 정합했습니다.** 다만 앞으로 baseline을
바꾸시면 자동으로 다시 계산되므로 이 문제가 재발하지 않습니다.
(baseline 해시로 캐시 → 파라미터 바꾸면 캐시 자동 무효화)

### 5-2. `LAM_pe_de`의 프로토콜

문서 초안에는 `experiment2`(충전 먼저)로 적혀 있었는데, **원본 코드 L174는
`experiment`(방전 먼저)** 를 씁니다. update_fn도 완충 기준 `17038.0/(1-i)`라
방전-먼저와 정합합니다. **원본 코드를 기준으로** 방전-먼저로 맞췄습니다.

### 5-3. 조합 격자에서의 LLI 적용 (새로 정한 규약)

단일 모드일 때는 원본과 100% 동일합니다(테스트로 고정). 조합할 때만 규약이 필요했습니다.

- 조합은 **완방 상태 기준**으로 통일 (충전-먼저 프로토콜)
- 이때 LLI는 **음극·양극 농도 모두**에 `×(1−LLI)` 적용

완방 상태에서는 리튬 재고가 거의 전부 양극에 있어서, 음극에만 곱하면 전체 재고의
0.1%만 줄어 사실상 아무 일도 안 일어납니다. 모든 저장소를 같은 비율로 줄여야
전체 재고가 정확히 LLI 비율만큼 감소합니다(Birkl 정의와 일치).

### 5-4. 물리와 무관한 변경

- Windows 절대경로(`C:\Users\ga117\...`) 제거 → 모든 출력은 `--out` 아래로
- `os.chdir(pybamm.__path__...)` 삭제
- xlsx → parquet (9천 조건에는 xlsx가 부적합)
- 전역 `param.update()` + `initialization()` 패턴 → 매번 새 객체 생성
  (`initialization()` 한 번만 빠뜨려도 이전 조건이 누적되던 위험 제거)

---

## 6. 검증 — 원본과 같은 결과가 나오는지

가형님이 코드에 넣어 두셨던 진단 블록(*"Reference와 LLI=0이 같은 용량인가"*)을
자동 테스트로 만들었습니다.

```bash
python -m pytest tests/ -v -m "not slow"   # 56개, 수 초
python -m pytest tests/ -v -m slow         # 3개, 약 20초 (실제 solve 포함)
```

| 검증 | 결과 |
|---|---|
| 5개 모드 × 4개 값의 파라미터 dict가 원본 `update_fn`과 일치 | ✅ 20/20 |
| Reference 용량 ≡ LLI=0 용량 (오염 없음) | ✅ 둘 다 5621.1 mAh |
| 같은 조건 2회 실행 결과 완전 일치 (전역 오염 없음) | ✅ |
| 완방상태 2회 계산 재현성 | ✅ |
| 32p 6-panel 그림 재현 | ✅ `results/sweep1d_v1/figures/` |

머신이 달라도 물리 baseline 해시가 `a8e262f7d6aa4beb`로 동일하게 나옵니다
(개발 컨테이너 Python 3.11 ↔ V100 서버 Python 3.10). 결과를 그대로 비교하셔도 됩니다.

---

## 7. 실제 구축된 서버 환경 (V100)

| 항목 | 값 |
|---|---|
| GPU | Tesla V100-PCIE-32GB |
| CPU / 메모리 / 디스크 | 32코어 / 125 GB / 889 GB |
| Python / PyBaMM | 3.10.12 / 26.7.1.0 |
| solver | **IDAKLU 사용 가능** |
| 1회 solve | 2.41 초 |
| coarse 격자 (125조건) | 약 1분 |
| fine 격자 (3,993조건) | **약 5~8분** |

**GPU는 이 프로젝트에서 거의 안 씁니다.** PyBaMM의 DFN은 시간축이 인과적으로
묶인 암시적 적분이라 GPU로 빨라지지 않습니다. V100 서버에서도 실제 무기는
**32개 CPU 코어**입니다. GPU는 Phase 7에서 JAX 변환을 시도해 보고(실패 가능성 높음),
나중에 surrogate 학습을 할 때나 의미가 있습니다. 자세한 근거는
`docs/03_ARCHITECTURE.md` 6절 "GPU 현실론"에 있습니다.

→ **GPU 없는 노트북에서도 모든 기능이 그대로 돌아갑니다.** 격자만 좀 오래 걸립니다.

### 7-1. 단계별로 GPU가 의미 있나 (Phase 4~6)

Phase 0~3(곡선 생성)과 Phase 4~6(fitting·채점)은 계산 성격이 다릅니다.
DFN solve는 GPU가 **원리적으로** 안 맞지만, fitting은 순수 배열 연산이라
**원리적으로는 맞습니다.** 다만 규모가 작아서 실익이 없을 뿐입니다.

| 단계 | 계산 성격 | GPU | 이유 |
|---|---|---|---|
| Phase 4 fitting | 미지수 4개 최적화 × 조건 3,069개 | ✗ | 1회 fitting이 1초 미만. CPU 32코어로 **10~20분**이면 끝남 |
| Phase 5 채점 | 3,069행 표 연산 | ✗ | 초 단위. 논의 자체가 무의미 |
| Phase 5 Hessian | 4×4 행렬 | ✗ | 조건당 수십 번 함수 평가. 단 **JAX 자동미분은 정확도 면에서 가치 있음** (속도가 아니라 수치미분 오차 제거) |
| Phase 6 가중치 sweep | fitting × 가중치 조합 수 | **△** | **여기만 유일하게 검토 가치 있음** (아래) |

**Phase 6가 유일한 후보인 이유**

가중치를 몇 개까지 훑느냐에 따라 계산량이 급격히 늘어납니다.

| 가중치 sweep 범위 | fitting 횟수 | CPU 32코어 예상 |
|---|---|---|
| `w_dqdv`만 9단계 | 약 14만 | 20~30분 — **CPU로 충분** |
| 3개 가중치 5×5×5 | 약 190만 | **5시간 이상** — 이때는 GPU 검토 |

fitting 목적함수는 300점짜리 배열의 보간·RMSE·미분뿐이라 `jax.vmap`으로
수천 조건을 한 번에 태우기에 적합합니다. DFN과 달리 **인과적 순서 제약이 없습니다.**
다만 GPU로 가기 전에 CPU 쪽에서 먼저 할 일이 있습니다:

1. dQ/dV 피크 가중치를 조건마다 재계산하지 말고 **타깃별 1회 precompute**
2. multi-start를 무조건 5회가 아니라 **결과가 갈릴 때만 추가 실행**
3. 가중치 sweep은 곡선 재생성 없이 목적함수만 바꾸므로 **재사용 캐시**

이 셋만 해도 대부분 CPU로 감당됩니다. **그래도 부족하면** 그때 목적함수를
JAX로 다시 쓰고 vmap 배치를 태웁니다 (Phase 7-3과 같은 작업).

**결론**: Phase 4~6도 기본은 CPU입니다. GPU는 "3차원 가중치 격자를 전부 훑겠다"고
결정할 때만 실익이 생기고, 그때도 목적함수만 JAX로 옮기면 되므로
PyBaMM을 GPU화하는 것(Phase 7-1, 실패 예상)과는 난이도가 전혀 다릅니다.

---

## 8. 전체 로드맵 — 지금까지 된 것과 앞으로 할 것

```
Phase 0  스캐폴딩·환경          ✅   V100 환경 검증 완료
Phase 1  코어 리팩터링           ✅   완방상태 자동화, 전역 param 제거
Phase 2  모드 중첩·32p 재현      ✅   원본 회귀 검증 통과
Phase 3  조합 격자·병렬화        ✅   fine 격자 3,069조건 생성
Phase 4  Fitting 이식           ✅   구현 완료. LLI 환산식 유도 정정 (아래 ★)
Phase 5  degeneracy 판정·지도    ✅   구현 완료. coarse에서 검증
Phase 6  목적함수 4종 비교        ✅   구현 완료. fine 결과 대기 중
Phase 7  GPU 시도               ✅   7-1 판정 완료 → docs/GPU_NOTES.md
──────────────────────────────────
남은 것: fine 격자 실행 결과를 채워 넣는 일 (계산만 돌면 됨)
  ① Case 2 (grid 기준) fine fitting     — 진행 중, 2026-08-06 ETA 12:53
  ② score → hessian → report            — ①이 끝나면 10분
  ③ Case 1 (halfcell 기준) fine fitting — 별도 --out으로, 약 5시간
  ④ 가중치 sweep                        — 약 70분
```

Phase 0~3이 "정답을 아는 시험문제 3,069개를 출제"한 것이고, Phase 4~6이
"그 문제를 기존 fitting 코드에 풀려서 채점"하는 단계입니다. 코드는 전부
들어갔고, 지금은 **채점 결과가 나오기를 기다리는 상태**입니다.

테스트 120건이 통과 상태이며, 물리·수식을 건드린 변경은 모두 `CHANGELOG.md`에
근거와 실측값을 함께 남겼습니다.

---

### Phase 4 — Fitting 이식 (33p·34p)

**하는 일**: 가형님이 쓰시던 MATLAB `degradation_mode` 코드를 Python으로 옮깁니다.
32p 라이브러리가 *정방향*(모드 → 곡선)이라면, 이건 *역방향*(곡선 → 모드)입니다.

| 구현 | 내용 |
|---|---|
| `src/fitting.py` | `windowed_curve(f_ref, x, α, β)` — **원본 코드 그대로 재사용** |
| | `reconstruct(p)` — `p = [α_PE, β_PE, α_NE, β_NE]` → PE·NE·full cell 재구성 |
| | `to_degradation_modes(p, r, convention=...)` — ★ 아래 정정 참조 |

#### ★ Phase 4에서 확인된 정정 — LAM·LLI 환산식

**이 부분은 원본 코드와 결론이 달라졌습니다.** 합성 데이터에 정답이 있으니
"어느 식이 정답을 복원하는가"를 직접 검증할 수 있었고, 그 결과입니다.

**(1) α는 열화율이 아니라 용량비입니다.**

x축이 "각 셀 자기 용량"으로 정규화돼 있으므로

```
    α_PE = (1 − LAM_PE) / r ,      r = Q_degraded / Q_reference
```

즉 `LAM_PE = 1 − α_PE`는 `r = 1`일 때만 맞습니다. 용량이 줄면 α > 1이 됩니다.
합성 격자에서 참 α의 범위는 **0.92 ~ 1.39** 였습니다.

여기서 따라오는 결론 하나가 중요합니다.

> **α = 1.00 ⟺ LAM = 용량손실**

33p 원본 bound는 `lb = [1.00, …]`로 α의 하한을 정확히 이 지점에 못 박습니다.
최적화가 하한에 붙으면 **자동으로 `LAM_PE ≈ LAM_NE ≈ 용량손실`이 나옵니다.**
22p 결과 패턴과 정확히 일치합니다. 그리고 합성 격자에서 33p bound 안에 정답이
들어 있는 조건은 **17%뿐**이었습니다 — 나머지 83%는 원리적으로 복원 불가입니다.

그래서 `--bounds original_33p`(원본)와 `--bounds expanded`(참값을 담는 범위)를
둘 다 남겨 **비교 자체를 결과물로** 삼았습니다.

**(2) LLI 환산식을 전하 보존에서 다시 유도했습니다.**

원본식 `LLI = (1−α_PE) + (β_PE − β_NE)`와 21p식 둘 다 **정답을 복원하지
못했습니다**(참값 LLI를 아는 조건에서 각각 0.128, 0.200 → 참값과 불일치).
전하 보존으로 다시 유도한 결과:

```
    LLI = 1 − r·[ w_PE·α_PE + w_NE·α_NE + κ·(β_NE − β_PE) ]
```

같은 조건에서 오차 **0.012**로 떨어졌습니다. `w_PE`, `w_NE`, `κ`는 셀 형상에서
자동 계산됩니다(`src/inventory.py`, 기준 셀에서 `w_PE=0.2909, w_NE=0.7091,
κ=0.7057`). 21p식은 가중치와 β 부호가 **둘 다** 다릅니다.

세 규약을 모두 계산해 나란히 저장합니다 — `lli_hat`(유도식), `lli_hat_21p`,
`lli_hat_code`(원본). 어느 것을 쓸지는 보는 사람이 정할 수 있게 했습니다.

**(3) 기준 곡선을 두 가지로 나눠 병행합니다.**

| | 기준 | 비고 |
|---|---|---|
| **Case 1** | 전 범위 half-cell OCV를 PyBaMM OCP 함수에서 직접 추출 | 21p 논문 방식. `--reference halfcell` |
| **Case 2** | 격자의 무열화 조건 곡선 | 유도식 방식. `--reference grid` (기본) |

Case 1은 초기에 훨씬 나빴는데(LAM 오차 0.054/0.126) 원인이 세 가지였습니다 —
테이블이 [0,1]로 정규화되지 않음, bound가 너무 좁음, 그리고 **NE 이력(hysteresis)
분기가 한 테이블에 섞임**. 고친 뒤 0.018/0.018로 수렴했습니다.
| `src/objective.py` | **34p 수식 그대로**: `J(p) = w_pocv·RMSE_pocv/scale + w_dvdq·RMSE_dvdq/scale + w_dqdv·RMSE^w_dqdv/scale` |
| | dQ/dV 피크 가중 (33p "peak weight factor"), savgol 스무딩 (33p "peak smoothing") |

**핵심 장치 — multi-start**: 초기값을 bound 안에서 무작위로 바꿔가며 여러 번(기본 5회)
최적화합니다. **결과가 서로 다르게 나오면 그 자체가 degeneracy의 직접 증거**입니다.
같은 데이터에 같은 코드인데 답이 갈린다는 뜻이니까요.

> ⚠ **미리 알려드릴 문제 — 33p의 bound**
> 33p 코드의 `lb = [1.00, -0.3, 1.00, -0.15]`는 **α 하한이 1.00**입니다.
> 그런데 열화는 α < 1로 표현됩니다(`LAM = 1−α`). 즉 **현재 bound로는 LAM > 0을
> 표현할 수 없거나**, 정규화 기준이 우리 생각과 다르다는 뜻입니다.
> 두 경우 모두 22p 결과 해석에 영향이 있어서, Phase 4에서 정규화 기준을 확인하고
> 필요하면 lb를 확장한 뒤 **`physics` 커밋으로 근거를 남기겠습니다.**
> 또 최적해가 bound에 붙는 경우(active constraint)를 자동 감지해 플래그합니다 —
> bound에 붙은 답은 "최적"이 아니라 "더 갈 데가 없어서 멈춘" 것이니까요.

**검증**: α=1, β=0을 넣으면 reference와 정확히 일치(항등) / 일부러 α_PE=0.9로 만든
곡선에서 0.9를 복원 / bound에 붙으면 플래그가 켜짐.

**실행**: `./run.sh --mode fit --in results/grid_fine_v1 --n-restarts 5`
**산출**: `fits.parquet` (조건별 복원값 + 수렴 정보 + restart별 결과)

---

### Phase 5 — degeneracy 판정 · 지도

**하는 일**: 정답과 복원값을 대조해 채점하고, 파라미터 공간 어디가 위험한지 지도를 그립니다.

채점 지표 (`src/scoring.py`):

| 지표 | 의미 |
|---|---|
| `err_lli`, `err_lam_pe`, `err_lam_ne` | 복원값 − 정답 |
| `abs_err_max` | 셋 중 최대 오차 |
| **`pe_ne_antisym`** | `err_pe × err_ne < 0` — **degeneracy의 특징적 지문.** PE를 과대평가한 만큼 NE를 과소평가해 상쇄된 경우 |
| `n_restarts_agree` | multi-start 결과 일치 개수 → 해의 유일성 지표 |
| `degenerate` | `abs_err_max > 0.02` (2%p) 이면 degeneracy 판정 |

**Hessian 분석** (`src/hessian.py`): 최적점에서 목적함수의 2차 미분을 계산합니다.

- 고윳값 하나가 0에 가까우면 → **평평한 골짜기(flat valley)** = degeneracy
- 그 최소 고윳값의 **고유벡터 방향**을 봅니다. α_PE와 α_NE가 **같은 부호로 묶여
  있으면**, "PE와 NE를 같이 움직여도 목적함수가 안 변한다" = 22p에서 두 값이
  붙어 나온 이유가 물리가 아니라 수학이라는 증거입니다.
- 조건수(최대/최소 고윳값)가 클수록 심한 degeneracy.

**지도** (`tools/plot_map.py`): x=LAM_PE, y=LAM_NE, 색=오차, LLI별로 여러 장.
그리고 여기에 **22p 실험 조건(LAM_PE≈13%, LAM_NE≈13%, LLI≈17%)을 마커로 찍습니다.**
→ *"우리 실험 조건이 degeneracy 영역 안에 있는가"* 에 그림 하나로 답합니다.

**실행**: `./run.sh --mode score --in results/grid_fine_v1` / `--mode hessian`
**산출**: `degeneracy_map.parquet`, `figures/degeneracy_map.png`

---

### Phase 6 — 목적함수 4종 비교 ★ 최종 산출물

**이게 이 프로젝트의 답입니다.** 같은 격자에 목적함수만 바꿔 적용해서,
34p의 dQ/dV 추가가 실제로 얼마나 효과가 있는지 정량화합니다.

| 목적함수 | 정체 |
|---|---|
| `pocv` | 전압 곡선만 |
| `pocv_dvdq` | **기존 방식 (33p)** |
| `pocv_dvdq_dqdv` | **개선안 (34p)** |
| `dqdv_only` | dQ/dV만 |

나오는 표:

```
| objective        | degeneracy 비율 | 평균 |err| | PE-NE 상쇄 비율 |
|------------------|----------|-----------|----------------|
| pocv             |    ?%    |     ?     |       ?        |
| pocv_dvdq        |    ?%    |     ?     |       ?        |   ← 기존
| pocv_dvdq_dqdv   |    ?%    |     ?     |       ?        |   ← 34p 개선
| dqdv_only        |    ?%    |     ?     |       ?        |
```

**가중치 최적화**: `w_dqdv`를 0~2로 훑어서 degeneracy 비율이 최소가 되는 조합을 찾습니다.
*"가중치를 임의로 튜닝한 것 아니냐"* 는 질문에 대한 근거가 됩니다.
전체 격자에 9가지 가중치를 다 돌리면 CPU로 감당이 안 돼서, 축마다 격자를 반으로
성기게 잡은 **층화 표본**(6³×noise3)을 씁니다. 무작위 표본이 아니라 격자 구조를
보존하므로 코너가 빠지지 않습니다.

**`docs/RESULTS.md` 자동 생성** — 숫자를 손으로 옮겨 적지 않습니다. 격자를 다시
돌리면 문서도 다시 생성하면 됩니다.

#### ★ 22p 질문에 직접 답하는 지표 — 전극 격차 복원력

Phase 6을 짜다가 발견한 함정입니다. **22p 근방 격자점은 참값 자체가
`LAM_PE = LAM_NE`입니다.** 그러니 "그 근방에서 복원이 잘 됐다"는 22p를 옹호하는
증거가 되지 못합니다. 물어야 할 것은 반대 방향입니다.

> **참값이 뚜렷이 다를 때도 fitting이 둘을 같다고 말하는가?**

`gap_analysis()`가 이걸 셉니다.

| 지표 | 의미 |
|---|---|
| `gap_collapse_frac` | 참 격차 ≥6%p인데 복원 격차 <2%p로 답한 비율. **높으면 "두 전극이 비슷하다"는 관측 자체가 무의미해집니다** |
| `shrinkage` | 복원 격차 / 참 격차. 1이면 그대로 복원, 0이면 전부 뭉갬 |
| `false_split_frac` | 참값은 같은데 다르다고 답한 비율 (반대 방향 오류) |

coarse 격자(F15 수정 전) 잠정치는 **예상과 반대 방향**이었습니다.

```
gap_collapse_frac = 2.2%     shrinkage = 0.95     false_split_frac = 63%
```

이 방법은 서로 다른 전극을 뭉개지 **않습니다.** 실패는 *없는 격차를 만들어내는*
쪽으로 나타납니다. 이게 fine 격자에서도 유지되면, 22p의 `LAM_PE ≈ LAM_NE`를
"구분을 못 해서 나온 값"으로 단정할 수 없다는 뜻이 됩니다.

⚠ 단, `false_split` 판정 기준(2%p)이 F15 편향(~1.6%p)과 같은 크기라 63% 중
상당 부분이 그 편향일 수 있습니다. **fine 재fit 결과로 확정할 부분입니다.**

`tools/make_results.py`의 결론 문장은 이 숫자를 따라 분기합니다. 초안은 붕괴율과
무관하게 "증거가 되지 못한다"를 고정 출력하게 돼 있었는데, 데이터가 반대로 나온
지금 같은 경우 거짓 결론을 쓰게 됩니다. 양방향 모두 테스트로 고정해뒀습니다.

**실행**:
```bash
./run.sh --mode score   --in results/grid_fine_v1
./run.sh --mode hessian --in results/grid_fine_v1
./run.sh --mode report  --in results/grid_fine_v1     # 비교표 + RESULTS.md
./run.sh --mode wsweep  --in results/grid_fine_v1 --nproc 32
```

---

### Phase 7 — GPU 시도 (선택 · 실패해도 됨)

목적이 "성공"이 아니라 **"기록"** 인 단계입니다. 다음 사람이 같은 시도를
반복하지 않게 하는 것이 산출물입니다.

| 단계 | 시도 | 전망 |
|---|---|---|
| 7-1 | DFN을 JAX로 변환 | composite 2상 입자라 **실패 가능성 높음** |
| 7-2 | SPMe로 낮춰 재시도 | 되더라도 DFN 정확도 손실을 정량화해야 함 |
| 7-3 | `jax.vmap`으로 배치 | 성공 시 CPU 병렬과 처리량 비교표 |
| 7-4 | 자동미분 Hessian | Phase 5의 수치 Hessian과 비교, 정밀도 향상 여부 |

각 단계의 성공/실패와 예외 메시지를 `docs/GPU_NOTES.md`에 전부 남깁니다.
`--backend gpu`는 실패 시 경고와 함께 CPU로 안전하게 fallback합니다.

---

### 최종적으로 답하게 되는 질문 5개

1. 기존 fitting 코드는 어떤 (LAM_PE, LAM_NE, LLI) 조합에서 정답을 복원하는가?
2. degeneracy가 발생하는 영역은 파라미터 공간의 몇 %인가?
3. **22p의 실험 조건은 그 degeneracy 영역 안에 있는가?**
4. **34p의 dQ/dV 추가가 degeneracy 영역을 얼마나 줄이는가? (X% → Y%)**
5. 목적함수 가중치의 최적 조합은?

**4번이 가장 중요합니다.** 이 숫자가 나오면 34p 수정을 "기능을 추가했다"가 아니라
**"degeneracy 영역을 X%에서 Y%로 줄였다"** 로 정량 보고할 수 있습니다.

그리고 3번의 답이 "그렇다"로 나오면, 22p의 `LAM_PE ≈ LAM_NE ≈ 13%`는
**물리가 아니라 fitting의 한계**라는 결론이 되고, 지도교수님 지적에 대한
정면 답변이 됩니다. Part 1의 정성 데이터(7p·9p·14p·19p)와 COMSOL 결과(28p,
NCM LAM ≈ 0%)가 모두 NE 편향을 가리키는 것과도 앞뒤가 맞게 됩니다.

---

### 미리 보인 징후 (coarse 격자에서)

곡선 단계에서 이미 상쇄가 보입니다. LLI=0.2 슬라이스의 방전용량 [mAh]:

| | LAM_NE=0 | 0.05 | 0.10 | 0.15 | 0.20 |
|---|---|---|---|---|---|
| **LAM_PE=0** | 4147 | 4141 | 4135 | 4129 | 4119 |
| **LAM_PE=0.20** | 4579 | 4575 | 4570 | 4556 | 4487 |

LAM_NE를 0에서 0.20까지 **4배 늘려도 용량이 28 mAh(0.7%)밖에 안 변합니다.**
측정 노이즈에 묻히는 수준입니다. 반면 LAM_PE 방향으로는 400 mAh 넘게 변합니다.

→ 고LLI 영역에서 **LAM_NE는 full-cell 곡선에 거의 흔적을 남기지 않습니다.**
fitting이 이 영역에서 LAM_NE를 제대로 복원할 가능성은 낮고, 그게 바로 degeneracy입니다.
22p의 조건(LLI≈17%)이 정확히 이 영역에 있다는 점이 중요합니다.
Phase 5의 지도로 확정할 부분입니다.

---

### 긴 실행을 돌릴 때 주의 — 실제로 겪은 사고들

5시간짜리 실행이라 사고가 나면 비쌉니다. 겪은 것만 적습니다.

**① 같은 `--out`에 두 프로세스가 붙었습니다 (2026-08-06)**

```
PID 330053  04:17:13 시작   ← curves.parquet 재생성(04:37:56) 이전
PID 333299  04:38:48 시작   ← 재생성 이후 (정상)
```

32워커씩 총 64개가 16물리코어를 나눠 써서 속도가 **24.5분/청크**로 반토막
났고(정상 11.8분), 더 나쁘게는 330053이 **재생성 전 옛 곡선**으로 fit_chunks에
결과를 쌓고 있었습니다. 청크 병합은 mtime 최신 우선이라 그대로 두면 정상
결과를 덮어씁니다.

원인은 `run_fit`이 실행 잠금을 **본체 마지막**에 잡고 있었던 것입니다. 그
앞 구간(curves 로드 → 3,069조건 태스크 구성 → halfcell이면 p_ini self-fitting)이
무방비였습니다. 지금은 함수 맨 앞에서 잡습니다.

- 잘못 뜬 쪽을 `kill`하고, 그 PID가 박힌 청크 파일을 지우면 복구됩니다
  (청크 파일명에 PID가 들어갑니다)
- **`--resume`을 쓸 때 주의**: 오염 청크를 지우면 "완료 표시는 있는데 결과 행이
  없는" 조건이 생기고, resume이 그걸 영원히 건너뜁니다. 결과가 조용히 비는
  가장 위험한 실패 모드라 지금은 코드가 걸러냅니다(경고 로그가 뜹니다)

**② kill한 프로세스의 워커가 남습니다**

`kill`(SIGTERM)로 부모를 죽이면 loky 워커 32개가 init에 입양돼 남을 수 있습니다.
메모리를 잡고 있고 화면을 헷갈리게 합니다.

```bash
# 확인 — ppid가 1이면 고아
ps -eo ppid,args | grep '[l]oky' | awk '{print $1}' | sort | uniq -c
# 정리
ps -eo pid,ppid,args | grep '[l]oky' | awk '$2==1 {print $1}' | xargs -r kill
# 애초에 이렇게 죽이면 안 남습니다 (프로세스 그룹째)
kill -- -$(ps -o pgid= -p <PID> | tr -d ' ')
```

**③ SSH가 끊기면 포그라운드 프로세스는 같이 죽습니다**

V100 접속이 자주 끊깁니다. 포그라운드로 띄운 작업은 SIGHUP으로 함께 죽고,
**아무 흔적도 안 남습니다** (로그도 traceback도 없이 그냥 사라짐). 실제로
30조건 스모크가 이렇게 사라져서 코드 버그를 의심하느라 시간을 썼습니다.

긴 작업은 **반드시 tmux 안에서**:

```bash
tmux new -s fit                       # 세션 시작
./run.sh --mode fit --in results/grid_fine_v1 --nproc 32 2>&1 | tee fit.log
# Ctrl+B 누르고 D 로 빠져나옴 (작업은 서버에서 계속 돎)
tmux a -t fit                         # 다시 붙기
tmux ls                               # 세션 목록
```

tmux 없이 급할 때:

```bash
setsid nohup ./run.sh --mode fit --in results/grid_fine_v1 --nproc 32 > fit.log 2>&1 < /dev/null & disown
```

접속하는 쪽 `~/.ssh/config`에 keepalive를 넣으면 끊김 자체가 줄어듭니다:

```
Host v100
    ServerAliveInterval 30
    ServerAliveCountMax 20
    TCPKeepAlive yes
```

**④ 명령을 붙여넣을 때 백슬래시 줄바꿈을 쓰지 마세요**

터미널에 여러 줄 명령을 붙여넣다가 줄이 끊겨서 엉뚱한 작업이 뜬 일이 세 번
있었습니다(한 번은 5.7시간짜리가 기본 설정으로 돌아갔습니다). **한 줄로** 쓰세요.

**⑤ 진행률은 `scripts/watch_fit.sh`로 보세요**

```bash
watch -n 60 './scripts/watch_fit.sh results/grid_fine_v1 fit_case2_fixed.log'
```

속도를 **최근 3청크**로 계산합니다. fitting 자체 로그의 "남은 예상"은 전체
평균이라, 위 ①처럼 초반에 느렸던 구간이 섞이면 실제보다 2배 가까이 늦게 나옵니다
(실측: 로그 291분 vs 실제 166분). 그리고 `src.fitting`이 2개 이상이면 크게
경고합니다 — ①을 그때 잡을 수 있었던 화면입니다.

---

### 알려진 개선 여지 (지금은 급하지 않음)

| 항목 | 내용 |
|---|---|
| 노이즈 축 중복 | fine 격자 3,993조건 중 **물리적으로 다른 건 1,331개**입니다. 노이즈는 solve 후에 더하는 후처리인데 지금은 노이즈 값마다 같은 시뮬레이션을 3번 돌립니다. 정리하면 격자 생성이 **3배 빨라집니다** |
| 곡선 저장량 | 조건당 300점만 저장 중. Phase 4에서 dQ/dV 피크 해상도가 부족하면 늘려야 할 수 있습니다 |

---

## 9. 막히면

| 상황 | 대응 |
|---|---|
| 환경이 꼬였다 | `./scripts/setup_env.sh --recreate` |
| IDAKLU가 안 잡힌다 | 그냥 진행됩니다 (casadi 자동 전환, 2~5배 느림) |
| SSH 끊겨서 죽었다 | 같은 명령에 `--resume` 붙여 재실행 |
| 격자가 너무 크다 | `--dry-run`으로 먼저 확인, step을 키워 coarse부터 |
| GPU 관련 문제 | `docs/SETUP_GPU.md` (V100 CUDA 버전 주의사항 포함) |
| 결과가 이상하다 | `results/<run>/manifest.yaml`에 git commit·config 해시·환경이 다 기록돼 있습니다 |

문서 지도:

| 파일 | 내용 |
|---|---|
| `docs/SETUP_GPU.md` | 새 서버 환경 구축 상세 (V100 노트, 트러블슈팅) |
| `docs/01_CONTEXT.md` | degeneracy 문제가 뭔지 |
| `docs/02_CODE_AUDIT.md` | 원본 코드 분석 |
| `docs/03_ARCHITECTURE.md` | 구조 설계, GPU 현실론 |
| `docs/04_PROMPTS.md` | Phase별 작업 계획 |
| `docs/06_REVIEW_DECISIONS.md` | **적대적 리뷰 처리 대장 — 기각·유보 항목과 해석 규칙** |
| `docs/07_LAM_LLI.md` | **LAM / LLI 정의 — 물리·수식·코드·흔한 오해** |
| `docs/GPU_NOTES.md` | PyBaMM/DFN을 CUDA로 돌릴 수 있는가 (실측 판정) |
| `docs/RESULTS.md` | 최종 결과 (자동 생성 — 계산이 끝나면 생깁니다) |
| `CHANGELOG.md` | **물리 변경 이력 (근거 포함)** |

---

## 10. 결과를 읽을 때 지켜야 할 규칙

적대적 리뷰에서 나온 것들입니다. 상세는 `docs/06_REVIEW_DECISIONS.md`에 있고,
**코드가 이미 이대로 계산합니다** — 아래는 왜 그런지에 대한 설명입니다.

| | 규칙 | 이유 |
|---|---|---|
| **F1** | 복원가능군(참 α ≥ 1)에서만 비율을 센다 | grid 기준에서 참 α<1인 조건은 재구성 창이 reference 범위를 벗어나 **원리적으로** 정답이 안 나옵니다. 게다가 이 벽은 box bound가 아니라 창 부족 벌점이 만드는 소프트 벽이라 `bound_active`에 안 잡힙니다 — 분리하지 않으면 "bound 문제 아님 → 진짜 물리"로 오판합니다 |
| **F5** | 방법 바이어스를 뺀 보정 판정을 나란히 본다 | 판정 기준 2%p가 방법 자체의 계통 편향과 같은 크기일 수 있습니다. 실제로 F15 수정 전에는 편향이 1.6%p였습니다 |
| **F10** | dQ/dV 계열은 노이즈 수준별로 따로 본다 | 노이즈에서 피크 가중이 희석됩니다. 노이즈 0 결과만 인용하면 과대평가입니다 |
| **F4** | multi-start 불일치율을 전체 평균으로 보고하지 않는다 | adaptive 조기 종료로 조건마다 restart 수가 달라 검정력이 다릅니다. 실측으로 확인: `n_restarts=2 → 일치 100%`, `n_restarts=5 → 일치 0%`. 뭉쳐서 평균 내면 의미 없는 숫자가 됩니다 |
| **F14** | 저LLI + 고LAM_PE 코너가 격자에 없다 | 완방 프레임 guard의 산물입니다. 고LAM_PE 결론은 고LLI가 동반된 조건에서만 검증된 것입니다 |
| **F7** | 모두 합성 데이터 결과다 | 실제 셀의 모델 오차(SEI, 저항 분포)는 없습니다. 즉 이 값들은 degeneracy의 **하한**이며 실제는 더 나쁩니다 |

`docs/RESULTS.md`는 이 규칙을 지킨 형태로 자동 생성되고, 한계 항목을 **결론
바로 밑**에 붙입니다 — 결론만 떼어 인용되는 걸 막기 위해서입니다.
