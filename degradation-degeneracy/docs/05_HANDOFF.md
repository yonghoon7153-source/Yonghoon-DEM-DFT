# 05. HANDOFF — 구축된 환경 설명서

> **읽는 사람**: 이가형 (원본 `degrade_mode_sim_me.py` 작성자)
> **한 줄 요약**: 가형님 스크립트를 서버에서 **수천 조건 병렬로** 돌릴 수 있는 형태로
> 이식하고, 아무 머신에서나 **명령 한 줄로** 같은 환경이 재현되게 만들어 뒀습니다.
> 물리 수식과 파라미터는 그대로입니다. 바꾼 것은 아래 §5에 전부 적어 뒀습니다.

작성일: 2026-08-05 / **최종 갱신: 2026-08-07** / 대상 브랜치: `claude/zip-git-gpu-setup-vdqdtd`

> **2026-08-07 기준 상태**: Phase 0~7이 전부 끝났고 fine 격자 채점 결과가 나왔습니다.
> 결론 세 줄은 §8-0에, 전체 수치는 `docs/RESULTS.md`에 있습니다.

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
./run.sh --mode grid --config configs/grid_fine.yaml --nproc 32 --out results/grid_fine_v2

# ── 여기서부터가 채점 단계 ──
./run.sh --mode fit     --in results/grid_fine_v2 --nproc 32   # α·β fitting (3시간 17분)
./run.sh --mode score   --in results/grid_fine_v2              # degeneracy 판정·지도
./run.sh --mode hessian --in results/grid_fine_v2              # 곡률(flat direction) 진단
./run.sh --mode wsweep  --in results/grid_fine_v2 --nproc 32   # 가중치 근거 (약 70분)
./run.sh --mode report  --in results/grid_fine_v2 --compare results/halfcell_v1
#   비교표 + docs/RESULTS.md.  --compare 를 주면 Case 1 vs Case 2 절이 같이 들어갑니다

# Case 1 (전 범위 half-cell 기준) 은 --reference 만 바꿔 별도 --out 으로 돌립니다
./run.sh --mode fit --in results/grid_fine_v2 --out results/halfcell_v1 --reference halfcell --nproc 32

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
  io.py         parquet 저장·manifest·실행 잠금        ← 원본 xlsx export 대체

  # ── 채점 단계 (Phase 4~6, 전부 신규) ──
  objective.py    목적함수 4종 + savgol 밴드 캐시(F22)
  fitting.py      α·β fitting, 다중 restart, 청크·resume, warm start(F20)
  scoring.py      degeneracy 판정 · 복원가능군 분류(F1) · multi-start 진단(F21)
  hessian.py      최적점 곡률 · flat direction
  weight_sweep.py w_dqdv 훑기 → configs/objectives_optimized.yaml

tools/
  plot_sweep1d.py       32p 6-panel 그림               ← 원본 L304-318
  interactive_ab.py     α·β 슬라이더 UI                ← 원본 L321-436 (그대로 분리)
  plot_grid_summary.py  격자 용량 지도                 (신규)
  compare_objectives.py 목적함수 4종 비교표 · 격차 복원 분석 · 그림
  compare_cases.py      Case 1(halfcell) vs Case 2(grid), 표본 맞춤 비교
  make_results.py       ★ docs/RESULTS.md 자동 생성 (자기 감시형 — §10 참조)

scripts/
  setup_env.sh          새 머신 환경 구축 한 줄
  bg.sh                 SSH 끊겨도 살아남게 백그라운드 실행 (중복 실행 거부 포함)
  watch_fit.sh          진행률·ETA — 최근 3청크 기준
  archive_results.sh    results/ → artifacts/ (다시 만들기 비싼 것만)
  diagnose_objective.py 목적함수 자체 진단 (피크 해상도 실측, 기준곡선 자기검사)

configs/           물리 baseline·격자·목적함수 정의 (yaml)
tests/             회귀·단위 검증 163개
artifacts/         ★ 계산 결과 백업 (저장소에 포함 — §9-1)
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
python -m pytest tests/ -v -m "not slow"   # 160개, 수 초
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

## 8-0. 결론 — 지금 나온 답 (2026-08-07)

전체 수치와 단서는 `docs/RESULTS.md`(자동 생성)에 있습니다. 여기는 세 줄 요약입니다.
모두 **복원가능군(F1)에서만**, **fine 격자 3,069조건**을 채점한 값입니다.

**① 22p의 `LAM_PE ≈ LAM_NE`는 degeneracy의 증거가 아닙니다 — 오히려 반대입니다.**

물어야 할 것은 "22p 근방에서 복원이 잘 되나"가 아니라 **"참값이 뚜렷이 다를 때도
fitting이 둘을 같다고 답하는가"** 입니다. 답은 거의 아니오였습니다.

```
P(같다고 답 | 참값이 같음)          = 38%
P(같다고 답 | 참값이 6%p 이상 차이) = 0.8%      (n=245)
────────────────────────────────────────────
우도비 ≈ 46 : 1  →  "실제로 비슷하게 열화했다" 쪽
```

격차 붕괴율 1%, shrinkage 1.06 (참 격차 9.9%p → 복원 격차 10.5%p).
Hessian의 `α_PE·α_NE 결합`도 **0%** 입니다 — 평평한 방향에서 두 전극이 묶여 있지
않다는 뜻이고, "22p는 수학적 상쇄"라는 가설의 직접적인 반증입니다.

⚠ 단, 이 숫자들은 **임계 설정에 의존**합니다. 붕괴로 세려면 격차를 6%p에서 2%p
아래로 끌어내려야 하므로 최소 4%p의 격차 오차가 필요한데, 실측 격차 오차는
중앙값 2.6%p·99분위 5.7%p입니다. 낮은 붕괴율의 상당 부분은 **오차 스케일이 임계
간격보다 작다**는 사실에서 옵니다. 그대로 인용하지 마시고 이 문장을 같이 쓰세요.

**② 34p의 dQ/dV 추가는 최종 오차를 줄이지 못했습니다 (62% → 63%).**

| objective | n | degeneracy | (바이어스 보정) | 평균 \|err\| | PE-NE 상쇄 |
|---|---|---|---|---|---|
| pOCV only | 1476 | 78% | 67% | 4.7%p | 29% |
| **pOCV + dV/dQ (33p 기존)** | 1476 | **62%** | 15% | **2.5%p** | 68% |
| **pOCV + dV/dQ + dQ/dV (34p)** | 1476 | **63%** | 24% | **2.4%p** | 48% |
| dQ/dV only | 1476 | 77% | 64% | 4.9%p | 22% |

차이가 2%p 이내라 **사실상 동률**입니다. 다만 PE-NE 상쇄가 68% → 48%로 줄어든
것은 실제 개선입니다 — 오차의 *총량*은 같은데 *상쇄 지문*이 옅어졌습니다.

**③ 진짜 큰 변수는 목적함수가 아니라 기준 곡선이었습니다.**

공통 1,476조건(grid 기준 복원가능군으로 행 수를 맞춤), 각 칸 = **Case 1 halfcell / Case 2 grid**:

| objective | degeneracy | 평균 \|err\| |
|---|---|---|
| **pOCV + dV/dQ (33p 기존)** | **7% / 62%** | **1.4%p / 2.5%p** |
| pOCV + dV/dQ + dQ/dV (34p) | 99% / 63% | 3.9%p / 2.4%p |

전 범위 half-cell OCV를 기준으로 쓰면 degeneracy가 62% → 7%로 떨어집니다.
**목적함수를 바꾸는 것보다 기준 곡선을 제대로 잡는 쪽이 압도적으로 큽니다.**

> ⚠ Case 1의 `+dQ/dV` 99%는 degeneracy가 아니라 **calibration 문제**로 보입니다.
> LAM_PE에 거의 일정한 −4.1%p 오프셋이 걸려 있고(보정하면 6%), 원인은
> `to_modes_halfcell`의 `p_ini` 정규화로 좁혀졌습니다. 미해결 항목입니다.

---

## 8. 전체 로드맵 — 지금까지 된 것과 앞으로 할 것

```
Phase 0  스캐폴딩·환경          ✅   V100 환경 검증 완료
Phase 1  코어 리팩터링           ✅   완방상태 자동화, 전역 param 제거
Phase 2  모드 중첩·32p 재현      ✅   원본 회귀 검증 통과
Phase 3  조합 격자·병렬화        ✅   fine 격자 3,069조건 생성
Phase 4  Fitting 이식           ✅   LLI 환산식 유도 정정 (아래 ★)
Phase 5  degeneracy 판정·지도    ✅   fine 격자로 확정
Phase 6  목적함수 4종 비교        ✅   ★ 완료 → docs/RESULTS.md, §8-0
Phase 7  GPU 시도               ✅   7-1 판정 완료 → docs/GPU_NOTES.md
──────────────────────────────────
실행 완료한 계산
  ① Case 2 (grid 기준) fine fitting     ✅  results/grid_fine_v2  (3시간 17분)
  ② score → hessian → report            ✅  docs/RESULTS.md 자동 생성
  ③ Case 1 (halfcell 기준) fine fitting ✅  results/halfcell_v1   (5시간 42분)
  ④ 가중치 sweep                        ⏳  restart 5로 재실행 중 (아래 ⑦ 참조)

남은 것 (전부 선택 사항 — 결론에는 영향 없음)
  · Case 1 `+dQ/dV`의 −4.1%p 오프셋 원인 규명 (calibration, §8-0 ③ 각주)
  · Case 1 쪽 Hessian (지금은 Case 2만)
  · bound 좁히기 실험
```

Phase 0~3이 "정답을 아는 시험문제 3,069개를 출제"한 것이고, Phase 4~6이
"그 문제를 기존 fitting 코드에 풀려서 채점"하는 단계였습니다. **채점까지 끝났고
결과는 §8-0과 `docs/RESULTS.md`에 있습니다.**

테스트 163건이 통과 상태이며, 물리·수식을 건드린 변경은 모두 `CHANGELOG.md`에
근거와 실측값을 함께 남겼습니다.

### 계산 비용 (V100 32코어 실측)

| 단계 | 시간 | 비고 |
|---|---|---|
| fine 격자 생성 (3,069조건) | 5~8분 | PyBaMM DFN, IDAKLU |
| fitting v1 | 8시간+ | 9.6 s/조건 |
| **fitting v2** | **3시간 17분** | **3.9 s/조건** — warm start(F20) + savgol 캐시(F22) |
| score / hessian / report | 각 1~10분 | |
| 가중치 sweep | 약 70분 | 층화 표본 468조건 |

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

**실행**: `./run.sh --mode fit --in results/grid_fine_v2 --n-restarts 5`
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

**실행**: `./run.sh --mode score --in results/grid_fine_v2` / `--mode hessian`
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

**나온 표** (fine 격자, 복원가능군 1,476조건 — 전문은 `docs/RESULTS.md`):

```
| objective        | degeneracy | 평균 |err| | PE-NE 상쇄 |
|------------------|------------|-----------|------------|
| pocv             |    78%     |   4.7%p   |    29%     |
| pocv_dvdq        |    62%     |   2.5%p   |    68%     |   ← 기존 33p
| pocv_dvdq_dqdv   |    63%     |   2.4%p   |    48%     |   ← 34p 개선
| dqdv_only        |    77%     |   4.9%p   |    22%     |
```

→ **dQ/dV 추가로 degeneracy 비율은 안 줄었습니다(62%→63%).** 대신 PE-NE 상쇄가
68%→48%로 줄었습니다. 즉 34p는 "오차를 줄인다"가 아니라 **"상쇄 지문을 옅게
한다"** 로 보고해야 정확합니다.

**가중치 최적화**: `w_dqdv`를 0~2로 훑어서 degeneracy 비율이 최소가 되는 조합을 찾습니다.
*"가중치를 임의로 튜닝한 것 아니냐"* 는 질문에 대한 근거가 됩니다.
전체 격자에 9가지 가중치를 다 돌리면 CPU로 감당이 안 돼서, 축마다 격자를 반으로
성기게 잡은 **층화 표본**(6³×noise3, 468조건)을 씁니다. 무작위 표본이 아니라 격자
구조를 보존하므로 코너가 빠지지 않습니다.

⏳ **현재 `docs/RESULTS.md`에 실린 sweep 숫자는 잠정치입니다** — `n_restarts = 2`로
돌린 것이라 아래 ⑦의 함정에 걸려 있습니다. `warm_start=False` + `n_restarts=5`로
재실행 중이고, 끝나면 `--mode report`를 다시 돌려 갱신합니다.

잠정치(restart 2): 노이즈 평균 최적 **`w_dqdv = 0.5`**(보정 degeneracy 25.7%),
기본값 1.0은 27.4%. 다만 **노이즈 수준별 최적값이 갈립니다** — noise 0에서 1.0,
0.001에서 0.25, 0.005에서 0.75. 단일 값을 채택하려면 실험 노이즈 수준을 먼저
특정해야 합니다. `pick_optimum`이 `noise_levels_agree` 플래그로 이걸 매번
알려줍니다. 산출물은 `configs/objectives_optimized.yaml`.

**이 절의 숫자만 미확정이고, §8-0의 결론 세 건은 sweep과 무관하게 확정입니다.**

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

**fine 격자 확정치** (`pocv_dvdq`, noise=0, n=245) — coarse 잠정치와 방향이 같고
더 강했습니다.

```
gap_collapse_frac = 1%     shrinkage = 1.06     false_split_frac = 62%
```

이 방법은 서로 다른 전극을 뭉개지 **않습니다.** 실패는 *없는 격차를 만들어내는*
쪽으로 나타납니다. 그래서 22p의 `LAM_PE ≈ LAM_NE`를 "구분을 못 해서 나온 값"으로
단정할 수 없습니다. 우도비로 정리하면 **46 : 1로 "실제로 비슷하게 열화했다" 쪽**
입니다 (§8-0 ①).

⚠ **임계 의존성 — 이 문장을 빼고 인용하지 마세요.** 붕괴로 세려면 격차를 6%p에서
2%p 아래로 끌어내려야 하니 최소 4%p의 격차 오차가 필요한데, 실측 격차 오차는
중앙값 2.6%p·99분위 5.7%p입니다. 붕괴가 원리적으로 관측 가능한 범위이긴 하나,
낮은 붕괴율의 상당 부분은 **오차 스케일이 임계 간격보다 작다**는 사실에서 옵니다.
`objective_comparison.yaml`의 `collapse_requires_gap_err` / `gap_err_median` /
`collapse_measurable`이 이걸 매번 같이 출력합니다.

⚠ `false_split` 판정 기준(2%p)도 방법 편향과 같은 크기일 수 있습니다. 그래서 표에
바이어스 보정치를 나란히 둡니다 (F5).

`tools/make_results.py`의 결론 문장은 이 숫자를 따라 분기합니다. 초안은 붕괴율과
무관하게 "증거가 되지 못한다"를 고정 출력하게 돼 있었는데, 데이터가 반대로 나온
지금 같은 경우 거짓 결론을 쓰게 됩니다. 양방향 모두 테스트로 고정해뒀습니다.

**실행** (실제로 돌린 명령):
```bash
./run.sh --mode score   --in results/grid_fine_v2
./run.sh --mode hessian --in results/grid_fine_v2
./run.sh --mode wsweep  --in results/grid_fine_v2 --nproc 32
# Case 1(halfcell)과 나란히 비교해서 RESULTS.md 생성
./run.sh --mode report  --in results/grid_fine_v2 --compare results/halfcell_v1
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

### 최종적으로 답하게 되는 질문 5개 — **답이 나왔습니다**

| | 질문 | 답 (2026-08-07, fine 격자) |
|---|---|---|
| 1 | 어떤 (LAM_PE, LAM_NE, LLI)에서 정답을 복원하는가? | 격자의 **52%는 grid 기준에서 원리적으로 복원 불가**(참 α<1 → 재구성 창 부족). 나머지 복원가능군 1,476조건에서 `pocv_dvdq` 평균 \|err\| **2.5%p** |
| 2 | degeneracy 영역은 몇 %인가? | **62%** (`pocv_dvdq`, 바이어스 보정 시 15%) |
| 3 | **22p 조건이 그 영역 안에 있는가?** | **근방 자체의 degeneracy는 12%** 로 낮습니다. 다만 그 근방은 참값이 애초에 `LAM_PE=LAM_NE`라 증거가 못 됩니다 — 아래 ★ 참조 |
| 4 | **dQ/dV가 degeneracy를 얼마나 줄이는가?** | **62% → 63%. 줄이지 못했습니다.** 대신 PE-NE 상쇄가 68% → 48%로 줄었습니다 |
| 5 | 가중치 최적 조합은? | ⏳ **미확정.** 잠정치는 노이즈 평균 `w_dqdv = 0.5`(25.7%), 기본값 1.0은 27.4%. 단 restart 2로 돌린 값이라 재실행 중이고, 노이즈 수준별로 최적값도 갈립니다 |

★ **3번은 질문 자체를 바꿔야 했습니다.** 22p 근방은 참값이 `LAM_PE = LAM_NE`인
격자점이라, 거기서 복원이 잘 됐다는 사실은 22p를 옹호하지도 반박하지도 못합니다.
방향을 뒤집어 **"참값이 뚜렷이 다를 때도 같다고 답하는가"** 를 물었더니 0.8%였고,
우도비 **46 : 1로 "실제로 비슷하게 열화했다"** 쪽이 나왔습니다 (§8-0 ①).

**즉 당초 가설 — "22p는 물리가 아니라 fitting의 한계" — 은 이 합성 격자에서
지지되지 않습니다.** 4번도 마찬가지로, 34p 수정을 "degeneracy 영역을 X%에서 Y%로
줄였다"로는 보고할 수 없습니다. 정직하게 보고할 수 있는 것은 두 가지입니다.

1. dQ/dV는 오차 총량을 줄이지 않지만 **PE-NE 상쇄 지문을 68% → 48%로 옅게** 한다.
2. **기준 곡선을 전 범위 half-cell로 바꾸면 degeneracy가 62% → 7%** 로 떨어진다
   (§8-0 ③). 목적함수 튜닝보다 이쪽이 압도적으로 크다.

⚠ 이 결론들은 **합성 데이터의 하한**입니다 (F7). 실제 셀의 모델 오차(SEI, 저항
분포)는 여기에 없으므로, Part 1의 정성 데이터(7p·9p·14p·19p)나 COMSOL 결과(28p,
NCM LAM ≈ 0%)와 어긋나는 부분은 "합성 격자에서는 degeneracy로 설명되지 않는다"
까지만 말합니다. 실측 셀에서도 그렇다는 뜻은 아닙니다.

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

**→ 채점 결과, 이 징후는 그대로 이어지지 않았습니다.** 용량(스칼라 하나)만 보면
LAM_NE가 거의 안 보이는 것이 맞지만, fitting은 곡선의 **형상 전체**(dV/dQ 포함)를
씁니다. 참값이 6%p 이상 다른 조건에서 두 전극을 같다고 답한 비율은 0.8%였습니다
(§8-0 ①). 즉 **"용량이 안 변한다 ⇒ 복원 불가"는 성립하지 않습니다.** 이 표는
직관의 출발점이었을 뿐이고, 결론은 §8-0을 보세요.

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
./run.sh --mode fit --in results/grid_fine_v2 --nproc 32 2>&1 | tee fit.log
# Ctrl+B 누르고 D 로 빠져나옴 (작업은 서버에서 계속 돎)
tmux a -t fit                         # 다시 붙기
tmux ls                               # 세션 목록
```

tmux 없이 급할 때는 **`scripts/bg.sh`** 를 쓰세요. 위 `setsid nohup … & disown`을
한 줄로 감싼 것인데, 세 가지를 더 합니다.

```bash
./scripts/bg.sh fit ./run.sh --mode fit --in results/grid_fine_v2 --nproc 32
#              └ 로그 이름 (생략 가능 — 명령과 --mode 값으로 자동 작명)
#   → 로그 파일 경로를 찍어주고
#   → 3초 뒤 실제로 살아있는지 확인해서 알려주고
#   → src.fitting / src.grid / src.weight_sweep 가 이미 돌고 있으면 아예 시작을 거부합니다 (①의 재발 방지)
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
watch -n 10 './scripts/watch_fit.sh results/grid_fine_v2 <bg.sh가 찍어준 로그파일>'
```

속도를 **최근 3청크**로 계산합니다. fitting 자체 로그의 "남은 예상"은 전체
평균이라, 위 ①처럼 초반에 느렸던 구간이 섞이면 실제보다 2배 가까이 늦게 나옵니다
(실측: 로그 291분 vs 실제 166분). 그리고 `src.fitting`이 2개 이상이면 크게
경고합니다 — ①을 그때 잡을 수 있었던 화면입니다.

**⑥ 잠금 코드가 `src.weight_sweep`을 몰라서 살아있는 잠금을 지웠습니다**

`.fit.lock`은 안에 적힌 PID가 죽었으면 "고아 잠금"으로 보고 지웁니다. 그런데 그
판정 함수(`_pid_alive`)가 `src.grid`와 `src.fitting`만 알고 있어서, **정상적으로
돌고 있던 sweep 프로세스를 죽은 것으로 판정**하고 잠금을 지웠습니다. 결과적으로
sweep 두 개가 같은 디렉터리에 겹쳐 돌았습니다. `watch_fit.sh`도 같은 이유로
"프로세스 없음"을 띄웠습니다.

지금은 진입점 목록을 한 곳(`src/io.py`의 `_RUN_ENTRYPOINTS`)에 모아 두고,
**`run.sh`를 파싱해서 거기 등장하는 `python -m src.*` 가 전부 목록에 있는지
검사하는 테스트**를 걸어 뒀습니다. 새 실행 모드를 추가하면 테스트가 먼저 깨집니다.

**⑦ sweep 결과가 "warm start 때문"인 줄 알았는데 restart 수 때문이었습니다**

가중치 sweep에서 `w_dqdv = 0` 만 degeneracy 86%로 튀었습니다. warm start 시딩이
`w=0`에게만 불리하게 걸린 것으로 두 번 진단했는데 **두 번 다 틀렸습니다.** 진짜
원인은 `n_restarts = 2` 였습니다. 같은 목적함수·같은 237조건으로 대조하니
**restart 2에서 86%(보정 17.3%), restart 5에서 91.7% 보정** — 즉 sweep이 잰 것은
가중치의 효과가 아니라 **restart 부족이었습니다.**

지금 sweep은 `warm_start=False` + `n_restarts=5`로 고정하고, 실제 사용한 값을
`weight_sweep.yaml`의 `seed_objective_used` / `warm_start` 필드에 기록합니다.
`make_results.py`는 옛 warm-start sweep 결과를 읽으면 경고를 붙입니다.

> **교훈**: 목적함수를 비교할 때는 optimizer 설정(restart 수, 초기값, 조기 종료)이
> 모든 조건에서 **동일한지** 부터 확인하세요. 이 프로젝트에서 가장 오래 헤맨
> 오진 두 건(⑦, 그리고 dQ/dV가 "나쁘다"고 나온 건)이 전부 여기서 나왔습니다.
> 후자는 `J_at_truth = 0.0` vs `J_at_found = 0.402` — degeneracy가 아니라
> **optimizer가 정답 근처에 가지도 못한 것**이었고, warm start로 해결됐습니다.

---

### 알려진 개선 여지 (지금은 급하지 않음)

| 항목 | 내용 |
|---|---|
| 노이즈 축 중복 | fine 격자 3,993조건 중 **물리적으로 다른 건 1,331개**입니다. 노이즈는 solve 후에 더하는 후처리인데 지금은 노이즈 값마다 같은 시뮬레이션을 3번 돌립니다. 정리하면 격자 생성이 **3배 빨라집니다** |
| 곡선 저장량 | 조건당 300점만 저장 중. `scripts/diagnose_objective.py --mode resolution`이 dQ/dV 피크의 실제 FWHM을 재서 부족한지 알려줍니다 (설정값이 아니라 실측 폭입니다) |
| Case 1 calibration | `+dQ/dV`에서 LAM_PE에 −4.1%p 오프셋. `to_modes_halfcell`의 `p_ini` 정규화로 좁혀졌으나 미해결 |
| ~~목적함수 JAX/GPU화~~ | **기각.** F22(savgol 밴드 캐시)로 CPU에서 목표를 넘겼습니다 — fitting이 9.6 → 3.9 s/조건. 남은 병목은 연산이 아니라 **메모리 대역폭**이라 GPU로 옮겨도 이득이 작습니다. 근거는 `docs/GPU_NOTES.md` |

#### F22 실측 (참고 — 왜 GPU가 필요 없어졌는지)

Savitzky–Golay는 선형 연산자라 행렬로 미리 뽑아 캐시할 수 있습니다. 처음엔 조밀
행렬로 캐시했는데 V100 32워커에서 **1.65배**밖에 안 나왔습니다(단일 스레드에서는
2.6배). 32워커가 각자 698 KB 행렬을 들고 메모리 대역폭을 갉아먹고 있었습니다.
띠(banded) 표현으로 바꾸니 캐시가 **698 KB → 3.4 KB (203배)** 로 줄면서 병목이
사라졌습니다.

```
scipy savgol_filter   387 µs
조밀 행렬 캐시         18.1 µs
띠 표현 캐시           13.2 µs      (scipy 대비 오차 1.3e-13 — 수치적으로 동일)
```

`DD_SMOOTH_CACHE=0` 으로 끄면 scipy 경로로 돌아갑니다 (동치성 검증용).

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
| `docs/RESULTS.md` | ★ **최종 결과 — 자동 생성, 손으로 고치지 말 것** |
| `CHANGELOG.md` | **물리 변경 이력 (근거 포함)** |

---

## 9-1. 결과 백업 — 서버가 날아가도 남는 것

계산 결과는 `results/`에 쌓이는데 이건 git에서 제외돼 있습니다(수 GB). 대신
**다시 만들기 비싼 것만** 골라 저장소에 넣어 뒀습니다.

```bash
./scripts/archive_results.sh          # results/ → artifacts/ 로 복사
git add artifacts && git commit -m "backup: ..." && git push -u origin claude/zip-git-gpu-setup-vdqdtd
```

| 들어가는 것 | 이유 |
|---|---|
| `fits.parquet` | 3~6시간짜리. 이게 핵심입니다 |
| `manifest.yaml` | git commit·config 해시·환경 — 재현의 근거 |
| `degeneracy_summary.yaml`, `objective_comparison.yaml`, `wsweep/` | 채점 결과 |
| `figures/` | 그림 |

| 빼는 것 | 이유 |
|---|---|
| `curves.parquet` | 5~8분이면 다시 만듭니다. 대신 용량이 큽니다 |
| `fit_chunks/` | `fits.parquet`으로 이미 병합돼 있습니다 |

현재 `artifacts/`에 **19 MB** — `grid_fine_v1`, `grid_fine_v2`(Case 2 최종),
`halfcell_v1`(Case 1) 셋이 들어 있고 GitHub에 올라가 있습니다.

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
| **F21** | multi-start는 **무작위 restart끼리만** 비교한다 | dQ/dV 목적함수는 첫 restart에 매끄러운 해를 초기값으로 받습니다(warm start). 그걸 섞으면 최적 J에 닿는 restart가 정의상 하나뿐이 되어 항상 multimodal로 찍힙니다. `degeneracy_summary.yaml`에서 **`multistart_random_only` 블록**을 보세요 |
| **F23** | Hessian 조건수의 **절대값을 인용하지 않는다** | 목적함수가 여러 스케일에서 울퉁불퉁하면 수치 Hessian이 수렴하지 않아 eps를 바꾸면 값이 자릿수 단위로 움직입니다. 의미 있는 것은 **같은 eps에서의 순서**뿐입니다 |

`docs/RESULTS.md`는 이 규칙을 지킨 형태로 자동 생성되고, 한계 항목을 **결론
바로 밑**에 붙입니다 — 결론만 떼어 인용되는 걸 막기 위해서입니다.

### 제가 틀렸다가 리뷰에서 뒤집힌 것 두 개 ★

인용하기 전에 반드시 아세요. 둘 다 **한 번은 제 입으로 잘못 보고했던** 것입니다.

**(a) "Case 1은 복원불가가 0%" 는 측정값이 아닙니다.**

`src/scoring.py`의 `classify_recoverability`가 `reference != "grid"` 이면
`recoverable = True` 로 **하드코딩**합니다. 전 범위 half-cell 테이블이라 창 부족이
없다는 물리적 근거는 있지만, 재 본 적은 없습니다. 그래서 §8-0 ③의 Case 1 / Case 2
비교표는 **두 실행의 공통 조건 중 grid 기준에서 복원가능한 것**으로 행 수를 맞춰
계산했습니다 (`tools/compare_cases.py`). 행 수를 안 맞추면 "Case 1이 좋다"가
표본이 달라서 생긴 착시일 수 있습니다.

**(b) 조건수가 낮다고 "정보가 더 많다"고 말하면 안 됩니다.**

이 격자에서 **조건수 순서와 실제 복원 오차는 역상관**입니다(상관계수 −0.12).
`dqdv_only`가 조건수는 제일 좋은데(98.8) 평균 |오차|는 제일 나쁩니다(4.9%p).
지형이 거칠면 곡률이 크게 잡히므로, 낮은 조건수가 "잘 정의된 최적점"이 아니라
**울퉁불퉁함**을 잰 것일 수 있습니다. `make_results.py`가 상관계수를 매번 직접
계산해서 역상관이면 경고를 자동으로 붙입니다.

> 이 두 건이 `make_results.py`를 **자기 감시형**으로 바꾼 계기입니다. 지금 이
> 스크립트는 조건수 역상관, eps 혼용, 표본 수 불일치, 임계에 의해 결정된 붕괴율,
> 노이즈 수준별 최적 w 불일치, 옛 warm-start sweep — 여섯 가지를 **결과를 보고
> 스스로 판단해서** 경고로 붙입니다. 결론 문장의 방향도 숫자에서 읽습니다.
