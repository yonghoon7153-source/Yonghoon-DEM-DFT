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
`LAM_PE ≈ LAM_NE ≈ 13%`가 진짜인지 fitting 축퇴인지 확인하려면
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
```

**꼭 알아두실 것 세 가지**

| | |
|---|---|
| `--dry-run` | 실제 계산 전에 **조건 수 / 예상 시간 / 예상 용량**을 실측 기반으로 알려줍니다. 큰 격자는 항상 이것부터 |
| `--resume` | 중간에 끊겨도 **완료된 조건은 건너뛰고** 이어서 갑니다. SSH 끊김·서버 재부팅 대비 |
| `tmux` | 긴 실행은 반드시 `tmux new -s grid` 안에서. 안 그러면 SSH 끊길 때 같이 죽습니다 (실제로 한 번 겪었습니다) |

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

---

## 8. 전체 로드맵 — 지금까지 된 것과 앞으로 할 것

```
Phase 0  스캐폴딩·환경          ✅   V100 환경 검증 완료
Phase 1  코어 리팩터링           ✅   완방상태 자동화, 전역 param 제거
Phase 2  모드 중첩·32p 재현      ✅   원본 회귀 검증 통과
Phase 3  조합 격자·병렬화        ✅   fine 격자 3,069조건 생성   ← 여기까지 완료
──────────────────────────────────
Phase 4  Fitting 이식           ⬜   33p MATLAB → Python, 34p 목적함수
Phase 5  축퇴 판정·지도          ⬜   정답 vs 복원값 채점, Hessian
Phase 6  목적함수 4종 비교        ⬜   ★ 최종 산출물
Phase 7  GPU 시도               ⬜   선택. 실패해도 기록이 산출물
```

여기서부터가 **실제로 질문에 답하는 부분**입니다. 지금까지(Phase 0~3)는
"정답을 아는 시험문제 3,069개를 출제"한 것이고, Phase 4~6이 "그 문제를
기존 fitting 코드에 풀려서 채점"하는 단계입니다.

---

### Phase 4 — Fitting 이식 (33p·34p)

**하는 일**: 가형님이 쓰시던 MATLAB `degradation_mode` 코드를 Python으로 옮깁니다.
32p 라이브러리가 *정방향*(모드 → 곡선)이라면, 이건 *역방향*(곡선 → 모드)입니다.

| 구현 | 내용 |
|---|---|
| `src/fitting.py` | `windowed_curve(f_ref, x, α, β)` — **원본 코드 그대로 재사용** |
| | `reconstruct(p)` — `p = [α_PE, β_PE, α_NE, β_NE]` → PE·NE·full cell 재구성 |
| | `to_degradation_modes(p)` — `LAM_PE = 1−α_PE`, `LAM_NE = 1−α_NE`, `LLI = (1−α_PE)+(β_PE−β_NE)` (Birkl 2017 부호 규약, 원본 유지) |
| `src/objective.py` | **34p 수식 그대로**: `J(p) = w_pocv·RMSE_pocv/scale + w_dvdq·RMSE_dvdq/scale + w_dqdv·RMSE^w_dqdv/scale` |
| | dQ/dV 피크 가중 (33p "peak weight factor"), savgol 스무딩 (33p "peak smoothing") |

**핵심 장치 — multi-start**: 초기값을 bound 안에서 무작위로 바꿔가며 여러 번(기본 5회)
최적화합니다. **결과가 서로 다르게 나오면 그 자체가 축퇴의 직접 증거**입니다.
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

### Phase 5 — 축퇴 판정 · 지도

**하는 일**: 정답과 복원값을 대조해 채점하고, 파라미터 공간 어디가 위험한지 지도를 그립니다.

채점 지표 (`src/scoring.py`):

| 지표 | 의미 |
|---|---|
| `err_lli`, `err_lam_pe`, `err_lam_ne` | 복원값 − 정답 |
| `abs_err_max` | 셋 중 최대 오차 |
| **`pe_ne_antisym`** | `err_pe × err_ne < 0` — **축퇴의 특징적 지문.** PE를 과대평가한 만큼 NE를 과소평가해 상쇄된 경우 |
| `n_restarts_agree` | multi-start 결과 일치 개수 → 해의 유일성 지표 |
| `degenerate` | `abs_err_max > 0.02` (2%p) 이면 축퇴 판정 |

**Hessian 분석** (`src/hessian.py`): 최적점에서 목적함수의 2차 미분을 계산합니다.

- 고윳값 하나가 0에 가까우면 → **평평한 골짜기(flat valley)** = 축퇴
- 그 최소 고윳값의 **고유벡터 방향**을 봅니다. α_PE와 α_NE가 **같은 부호로 묶여
  있으면**, "PE와 NE를 같이 움직여도 목적함수가 안 변한다" = 22p에서 두 값이
  붙어 나온 이유가 물리가 아니라 수학이라는 증거입니다.
- 조건수(최대/최소 고윳값)가 클수록 심한 축퇴.

**지도** (`tools/plot_map.py`): x=LAM_PE, y=LAM_NE, 색=오차, LLI별로 여러 장.
그리고 여기에 **22p 실험 조건(LAM_PE≈13%, LAM_NE≈13%, LLI≈17%)을 마커로 찍습니다.**
→ *"우리 실험 조건이 축퇴 영역 안에 있는가"* 에 그림 하나로 답합니다.

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
| objective        | 축퇴 비율 | 평균 |err| | PE-NE 상쇄 비율 |
|------------------|----------|-----------|----------------|
| pocv             |    ?%    |     ?     |       ?        |
| pocv_dvdq        |    ?%    |     ?     |       ?        |   ← 기존
| pocv_dvdq_dqdv   |    ?%    |     ?     |       ?        |   ← 34p 개선
| dqdv_only        |    ?%    |     ?     |       ?        |
```

**가중치 최적화**: `w_dqdv`를 0~2로 훑어서 축퇴 비율이 최소가 되는 조합을 찾습니다.
*"가중치를 임의로 튜닝한 것 아니냐"* 는 질문에 대한 근거가 됩니다.

**`docs/RESULTS.md` 자동 생성** — 실행 조건, 비교표, 핵심 결론 3줄,
그리고 22p 실험 조건의 축퇴 여부 판정.

**실행**: `./run.sh --mode all --config configs/grid_fine.yaml --nproc 32 --out results/final_v1`

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
2. 축퇴가 발생하는 영역은 파라미터 공간의 몇 %인가?
3. **22p의 실험 조건은 그 축퇴 영역 안에 있는가?**
4. **34p의 dQ/dV 추가가 축퇴 영역을 얼마나 줄이는가? (X% → Y%)**
5. 목적함수 가중치의 최적 조합은?

**4번이 가장 중요합니다.** 이 숫자가 나오면 34p 수정을 "기능을 추가했다"가 아니라
**"축퇴 영역을 X%에서 Y%로 줄였다"** 로 정량 보고할 수 있습니다.

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
fitting이 이 영역에서 LAM_NE를 제대로 복원할 가능성은 낮고, 그게 바로 축퇴입니다.
22p의 조건(LLI≈17%)이 정확히 이 영역에 있다는 점이 중요합니다.
Phase 5의 지도로 확정할 부분입니다.

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
| `docs/01_CONTEXT.md` | 축퇴 문제가 뭔지 |
| `docs/02_CODE_AUDIT.md` | 원본 코드 분석 |
| `docs/03_ARCHITECTURE.md` | 구조 설계, GPU 현실론 |
| `docs/04_PROMPTS.md` | Phase별 작업 계획 |
| `CHANGELOG.md` | **물리 변경 이력 (근거 포함)** |
