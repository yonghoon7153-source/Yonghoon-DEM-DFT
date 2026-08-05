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

## 8. 지금까지 된 것 / 앞으로 할 것

```
Phase 0  스캐폴딩·환경          ✅
Phase 1  코어 리팩터링           ✅   완방상태 자동화, 전역 param 제거
Phase 2  모드 중첩·32p 재현      ✅   원본 회귀 검증 통과
Phase 3  조합 격자·병렬화        ✅   fine 격자 3,069조건 생성
──────────────────────────────────
Phase 4  Fitting 이식 (33p)      ⬜   MATLAB → Python, 목적함수 J(p) (34p)
Phase 5  축퇴 판정·지도          ⬜   정답 vs 복원값 채점, Hessian
Phase 6  목적함수 4종 비교        ⬜   ★ "축퇴 X% → Y%" 최종 답
Phase 7  GPU 시도               ⬜   선택, 실패해도 기록이 산출물
```

Phase 6까지 가면 **"dQ/dV 항 추가가 축퇴 영역을 X%에서 Y%로 줄였다"** 를
숫자로 말할 수 있습니다. 34p 수정이 "기능 추가"가 아니라 정량적 개선이 됩니다.

한 가지 격자에서 미리 보인 것: **LLI가 클수록 LAM_NE에 대한 용량 민감도가
거의 사라집니다.** 곡선 단계에서 이미 상쇄가 보이므로, 그 영역에서 fitting이
축퇴를 일으킬 가능성이 높습니다. Phase 5에서 지도로 확인할 부분입니다.

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
