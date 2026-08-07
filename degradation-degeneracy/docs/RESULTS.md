# RESULTS — full-cell 곡선으로 LAM_PE와 LAM_NE를 분리할 수 있는가

> 이 파일은 `tools/make_results.py`가 결과 파일에서 자동 생성한다. 직접 수정하지 말 것.

생성: 2026-08-07 15:09 KST  
입력: `results/grid_fine_v2`  
git: `075a1450` (dirty)  

## 질문

2026-08-05 연구세미나 22p에서 `LAM_PE ≈ LAM_NE ≈ 13%`, `LLI ≈ 17%`가 나왔다. 이것이 실제 물리인가, 아니면 full-cell 곡선 하나로는 두 전극을 가를 수 없어서 생긴 **fitting degeneracy**인가.

정답을 아는 PyBaMM 합성 곡선을 격자로 만들고, 기존 α·β fitting이 그 정답을 복원하는지 채점해 답한다.

## 핵심 결론

1. dQ/dV 항을 넣으면 degeneracy가 62% → 63%로 **사실상 변화가 없다**(차이 2%p 이내). 즉 34p의 dQ/dV 추가는 이 합성 격자에서 최종 오차를 측정 가능하게 줄이지 못한다. (평균 |오차| 2.5%p → 2.4%p, PE-NE 상쇄 68% → 48%)

2. 참값이 뚜렷이 다른 조건(|ΔLAM|_true ≥ 6%p)에서 fitting이 두 전극을 같다고 답하는 비율은 **1%** (n=245). 참 격차 9.9%p → 복원 격차 10.5%p, shrinkage 1.06. 

   관측 "두 전극이 같다"가 어느 쪽을 지지하는지는 우도비로 나온다.

   > P(같다고 답 | 참값 같음) = 38%
   > P(같다고 답 | 참값 6%p 이상 차이) = 0.8%
   > **우도비 ≈ 46 : 1**

   → **22p의 `LAM_PE ≈ LAM_NE`는 degeneracy의 증거가 아니라, 두 전극이 실제로 비슷하게 열화했다는 쪽의 증거다.**

   ⚠ 이 숫자들은 임계 설정에 의존한다. 붕괴로 세려면 격차를 6%p에서 2%p 아래로 끌어내려야 하므로 최소 4%p의 격차 오차가 필요한데, 실측 격차 오차는 중앙값 2.6%p·99분위 5.7%p다. 붕괴가 원리적으로 관측 가능한 범위이긴 하나, 낮은 붕괴율의 상당 부분은 **오차 스케일이 임계 간격보다 작다**는 사실에서 온다.

3. **22p 조건(LAM_PE≈LAM_NE≈13%, LLI≈17%) 근방 자체의 degeneracy는 12%** — 최근접 8개 조건의 평균 |오차| 1.7%p, PE-NE 오차 상쇄 50%, 참 PE-NE 격차 1.0%p → 복원 격차 1.8%p. ⚠ 이 근방은 참값이 애초에 LAM_PE = LAM_NE인 격자점이므로, 여기서 복원이 잘 된다는 사실만으로는 22p 결과를 옹호할 수 없다 (위 2번이 답이다).

4. **격자의 52%는 grid 기준에서 원리적으로 복원 불가**(참값 α<1 → 재구성 창이 reference 범위를 벗어남)다. 위 숫자는 모두 복원가능군 5904행에서만 센 값이며, 복원불가군을 섞으면 목적함수 간 차이가 묻힌다.

### 이 결론이 말하지 않는 것

- **격자 공백(F14)**: 완방 프레임 guard 때문에 저LLI 영역에 고LAM_PE 조건이 없다. 저LLI(≤2%)에서 도달한 최대 LAM_PE는 `0.08`, 격자 전체 최대는 `0.2`. 고LAM_PE 결론은 고LLI가 동반된 조건에서만 검증된 것이다.
- **restart 불일치율(F4)**: adaptive 조기 종료로 조건마다 restart 수가 달라, multi-start 불일치율을 목적함수 간 비교 지표로 쓰지 않았다. `degeneracy_summary.yaml`의 `restart_conditioned` 항목에 restart 수로 조건화한 값만 있다.
- **방법 바이어스(F5)**: 판정 기준 2%p가 방법 자체의 계통 편향과 같은 크기일 수 있어, 바이어스를 뺀 보정 판정을 표에 나란히 뒀다. 두 값이 크게 다르면 그 목적함수의 결론은 약하다.
- 모두 **합성 데이터** 결과다. 실제 셀의 모델 오차(SEI, 저항 분포 등)는 여기에 없다. 즉 이 값들은 degeneracy의 **하한**이다 — 실제는 더 나쁘다.

## 목적함수 4종 비교

복원가능군(F1)만, 노이즈 전체 합산.

| objective | n | degeneracy | (바이어스 보정) | 평균 \|err\| | PE-NE 상쇄 |
|---|---|---|---|---|---|
| pOCV only | 1476 | 78% | 67% | 4.7%p | 29% |
| pOCV + dV/dQ  (33p 기존) | 1476 | 62% | 15% | 2.5%p | 68% |
| pOCV + dV/dQ + dQ/dV  (34p 개선) | 1476 | 63% | 24% | 2.4%p | 48% |
| dQ/dV only | 1476 | 77% | 64% | 4.9%p | 22% |

### 노이즈 수준별 (F10)

dQ/dV의 이점은 노이즈에서 희석된다. 노이즈 0 결과만 인용하면 과대평가가 된다.

| objective | noise | n | degeneracy | (바이어스 보정) | 평균 \|err\| | PE-NE 상쇄 |
|---|---|---|---|---|---|---|
| pOCV only | 0 | 492 | 78% | 64% | 4.8%p | 29% |
| pOCV only | 0.001 | 492 | 78% | 68% | 4.6%p | 28% |
| pOCV only | 0.005 | 492 | 77% | 68% | 4.8%p | 31% |
| pOCV + dV/dQ  (33p 기존) | 0 | 492 | 60% | 12% | 2.4%p | 71% |
| pOCV + dV/dQ  (33p 기존) | 0.001 | 492 | 62% | 14% | 2.4%p | 69% |
| pOCV + dV/dQ  (33p 기존) | 0.005 | 492 | 64% | 20% | 2.5%p | 63% |
| pOCV + dV/dQ + dQ/dV  (34p 개선) | 0 | 492 | 65% | 22% | 2.4%p | 53% |
| pOCV + dV/dQ + dQ/dV  (34p 개선) | 0.001 | 492 | 62% | 24% | 2.3%p | 46% |
| pOCV + dV/dQ + dQ/dV  (34p 개선) | 0.005 | 492 | 63% | 27% | 2.5%p | 47% |
| dQ/dV only | 0 | 492 | 75% | 65% | 4.9%p | 22% |
| dQ/dV only | 0.001 | 492 | 76% | 63% | 4.7%p | 20% |
| dQ/dV only | 0.005 | 492 | 79% | 65% | 5.1%p | 23% |

## 22p 실험 조건 판정

*모두 `noise = 0` 조건이다. 노이즈가 있으면 값이 달라진다(F10) — `objective_comparison.yaml`의 `verdict_22p.noise` 참조.*

| objective | 근방 조건 | degeneracy | 평균 \|err\| | err LAM_PE | err LAM_NE | PE-NE 상쇄 |
|---|---|---|---|---|---|---|
| pocv | 8 | 88% | 2.8%p | -1.3%p | 1.2%p | 50% |
| pocv_dvdq | 8 | 12% | 1.7%p | -1.7%p | 0.1%p | 50% |
| pocv_dvdq_dqdv | 8 | 12% | 1.9%p | -1.8%p | -0.0%p | 50% |
| dqdv_only | 8 | 50% | 3.8%p | -2.3%p | -3.2%p | 25% |

`err LAM_PE`와 `err LAM_NE`의 **부호가 반대**면, 한쪽을 과대평가한 만큼 다른 쪽을 과소평가해 full-cell 곡선에서 상쇄된 것이다 — degeneracy의 특징적 지문이다.

## 전극 격차를 구분하는가 — 22p 질문의 직접적인 답

*`noise = 0` 조건 기준.*

22p 근방 격자점은 **참값이 애초에 `LAM_PE = LAM_NE`** 다. 거기서 복원값이 비슷하게 나오는 건 아무 증거가 못 된다. 물어야 할 것은 반대 방향이다 — **참값이 뚜렷이 다를 때도 fitting이 둘을 같다고 말하는가.**

| objective | 넓은 격차 조건 n | **격차 붕괴율** | shrinkage | 거짓 분리율 | 붕괴에 필요한 격차오차 / 실측 중앙값 |
|---|---|---|---|---|---|
| pocv | 245 | **7%** | 1.05 | 53% | 4%p / 2.2%p |
| pocv_dvdq | 245 | **1%** | 1.06 | 62% | 4%p / 2.6%p |
| pocv_dvdq_dqdv | 245 | **1%** | 1.10 | 54% | 4%p / 2.1%p |
| dqdv_only | 245 | **4%** | 1.09 | 54% | 4%p / 1.8%p |

- **격차 붕괴율**: 참 격차 ≥ 6%p인데 복원 격차 < 2%p로 답한 비율. 높을수록 "두 전극이 비슷하다"는 관측이 무의미해진다.
- **shrinkage**: 복원 격차 / 참 격차의 평균. 1이면 격차를 그대로 복원, 0에 가까우면 전부 뭉갠다.
- **거짓 분리율**: 참값은 같은데 다르다고 답한 비율 (반대 방향 오류).
- **붕괴에 필요한 격차오차**: 붕괴로 세려면 격차를 6%p에서 2%p 아래로 끌어내려야 하므로 최소 4%p의 격차 오차가 필요합니다. 이 값이 실측 격차오차 중앙값보다 크면, **낮은 붕괴율은 측정이 아니라 임계 설정의 결과**입니다 — 그대로 인용하지 마세요.

## 곡률 진단 (Hessian) — 최적화와 무관한 측정

최적점에서 목적함수의 2차 미분. 최소 고윳값 방향으로는 파라미터를 움직여도 곡선이 거의 안 변한다 = **데이터가 그 조합을 구분하지 못한다**. optimizer가 어떻게 헤맸는지와 무관한 국소 지표라는 점이 장점이지만, **목적함수가 비매끄러우면 곡률 자체가 잘 정의되지 않는다** — 아래 두 경고를 반드시 함께 볼 것.

| objective | n | 조건수(중앙값) | flat score | 최소고윳값>0 | α_PE·α_NE 결합 |
|---|---|---|---|---|---|
| pocv | 200 | 3.41e+04 | 2.9e-05 | 99% | 0% |
| pocv_dvdq | 200 | 4.21e+04 | 2.4e-05 | 96% | 0% |
| pocv_dvdq_dqdv | 200 | 432 | 0.0023 | 84% | 0% |
| dqdv_only | 200 | 98.8 | 0.01 | 97% | 1% |

- **조건수**는 매끄러운 목적함수라면 작을수록 최적점이 잘 정의돼 있다는 뜻이다. 다만 그 해석은 아래 조건이 모두 만족될 때만 쓸 수 있다.
- ⚠ **조건수의 절대값은 인용하지 마세요.** 목적함수가 여러 스케일에서 울퉁불퉁하면 수치 Hessian이 수렴하지 않아, eps를 바꾸면 값이 자릿수 단위로 움직입니다 (F23). 의미가 있는 것은 **같은 eps에서의 순서**뿐입니다 (이 표는 eps=0.0001).
- ⚠⚠ **이 격자에서 조건수 순서는 실제 복원 성능과 역상관입니다** (상관계수 -0.12). 예: `dqdv_only`가 조건수는 가장 좋은데 평균 |오차|는 4.9%p로 나쁩니다. 지형이 거칠면 곡률이 크게 잡히므로, 낮은 조건수가 "잘 정의된 최적점"이 아니라 **울퉁불퉁함**을 잰 것일 수 있습니다. 조건수를 "정보가 더 많다"의 단독 근거로 쓰지 마세요.
- **최소고윳값>0** — 100%가 아니면 그만큼은 최적점이 아니라 **안장점**에서 곡률을 잰 것입니다. 그 조건들의 조건수는 해석하지 마세요.
- **α_PE·α_NE 결합** — 평평한 방향에서 두 전극이 같은 부호로 묶여 있는 비율. 높으면 "PE와 NE를 함께 움직여도 곡선이 안 변한다"는 뜻이고, 22p에서 LAM_PE ≈ LAM_NE가 나온 것이 물리가 아니라 수학이라는 직접 증거가 된다.

## multi-start 진단 — 진짜 degeneracy와 최적화 난이도의 구분

같은 조건을 여러 초기값에서 다시 풀었을 때 어떻게 갈리는지를 봅니다. **두 실패 모드는 처방이 정반대**라 반드시 나눠야 합니다.

> 아래 표는 **무작위 restart끼리만** 비교한 것입니다(F21b). dQ/dV 목적함수는 첫 restart에 매끄러운 해를 초기값으로 받으므로, 그것을 포함하면 최적 J에 닿는 restart가 정의상 하나뿐이 되어 항상 multimodal로 찍힙니다.

| objective | n | **flat valley** | multimodal | unique min |
|---|---|---|---|---|
| dqdv_only | 1465 | **2%** | 95% | 3% |
| pocv | 1421 | **4%** | 81% | 14% |
| pocv_dvdq | 1403 | **4%** | 79% | 17% |
| pocv_dvdq_dqdv | 1466 | **1%** | 98% | 1% |

- **flat valley** — 같은 J인데 해가 서로 멀다. **데이터가 그 조합을 구분하지 못한다는 직접 증거**입니다. 초기값을 아무리 잘 줘도 사라지지 않고, 측정 방식을 바꿔야 줄어듭니다.
- **multimodal** — J가 다른 국소최소가 여럿. degeneracy가 아니라 **최적화 난이도**입니다. 좋은 초기값을 주면 사라집니다 (dQ/dV 항이 이 경우였습니다 — 아래 참조).
- **unique min** — 해가 유일. 문제 없음.

> ⚠ **`pocv_dvdq_dqdv`의 multimodal이 98%로 극단적입니다.** flat valley 판정은 restart 2개 이상이 같은 J에 닿아야 성립하므로, 이렇게 지형이 울퉁불퉁하면 flat valley가 있어도 **관측되지 않습니다.** 이 목적함수의 낮은 flat valley 값을 "degeneracy가 적다"로 읽으면 안 됩니다 — 최적화와 무관한 곡률(Hessian) 쪽을 보세요.

> ⚠ `degeneracy_summary.yaml`의 `restart_conditioned` 블록에 있는 `agree_frac`과 `p_spread`는 인용하지 마세요. adaptive 조기 종료 때문에 `agree_frac`은 restart를 5까지 간 조건에서 **정의상 0**이고, `p_spread = 0`은 "해가 일치"가 아니라 "최적 J에 도달한 restart가 하나뿐"이라는 뜻입니다. 위 표가 그 자리를 대신합니다.

## 기준 곡선 비교 — Case 1 (전 범위 half-cell) vs Case 2 (격자 곡선)

목적함수를 바꾸는 것과 **기준 곡선을 바꾸는 것** 중 어느 쪽이 큰지.

공통 1476조건 (전체 3069 중, grid 기준 복원가능군으로 맞춤)

| objective | degeneracy | (바이어스 보정) | 평균 \|err\| |
|---|---|---|---|
| pOCV only | 100% / 78% | 27% / 67% | 9.4%p / 4.7%p |
| pOCV + dV/dQ  (33p 기존) | 7% / 62% | 6% / 15% | 1.4%p / 2.5%p |
| pOCV + dV/dQ + dQ/dV  (34p 개선) | 99% / 63% | 6% / 24% | 3.9%p / 2.4%p |
| dQ/dV only | 100% / 77% | 27% / 64% | 6.5%p / 4.9%p |

*(각 칸 = **Case 1 halfcell** / Case 2 grid)*

> ⚠ halfcell 쪽의 "복원불가 0%"는 **측정이 아닙니다.** `src/scoring.py`가 `reference != "grid"`이면 `recoverable=True`로 고정합니다(전 범위 테이블이라 창 부족이 없다는 물리적 근거). 그래서 위 표는 **두 실행의 공통 조건 중 grid 기준에서 복원가능한 것**으로 행 수를 맞춰 비교한 것입니다.

## dQ/dV 가중치 — 임의 튜닝이 아니라는 근거

`w_dqdv`를 [0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0]로 훑어 degeneracy 비율이 최소가 되는 값을 찾았다 (층화 표본 468조건, restart 5).

- 노이즈 평균 최적: **w_dqdv = 0.0** (degenerate_frac_corrected = 15.2%), 기본값 w=1.0일 때 90.3%
- noise=0.0: 최적 w = 0.0 (15.2%, n=79)
- noise=0.001: 최적 w = 0.0 (13.9%, n=79)
- noise=0.005: 최적 w = 0.0 (16.5%, n=79)

모든 노이즈 수준에서 같은 w가 최적 — 단일 값 채택 근거 있음.

결과: `configs/objectives_optimized.yaml`

## 그림

- `results/grid_fine_v2/figures/gap_recovery_pocv.png` — gap_pocv
- `results/grid_fine_v2/figures/gap_recovery_pocv_dvdq.png` — gap_pocv_dvdq
- `results/grid_fine_v2/figures/gap_recovery_pocv_dvdq_dqdv.png` — gap_pocv_dvdq_dqdv
- `results/grid_fine_v2/figures/gap_recovery_dqdv_only.png` — gap_dqdv_only
- `results/grid_fine_v2/figures/objective_panel_noise0.png` — noise_0
- `results/grid_fine_v2/figures/objective_panel_noise0.001.png` — noise_0.001
- `results/grid_fine_v2/figures/objective_panel_noise0.005.png` — noise_0.005
- `results/grid_fine_v2/figures/weight_sweep.png` — weight_curve

## 재현

```bash
./scripts/setup_env.sh && source .venv/bin/activate
./run.sh --mode verify
./run.sh --mode grid --config configs/grid_fine.yaml --nproc $(nproc) --out results/grid_fine_v2
./run.sh --mode fit   --in results/grid_fine_v2 --nproc $(nproc)
./run.sh --mode score --in results/grid_fine_v2
./run.sh --mode hessian --in results/grid_fine_v2
./run.sh --mode report --in results/grid_fine_v2
```

관련 문서: `docs/06_REVIEW_DECISIONS.md`(해석 규칙), `docs/07_LAM_LLI.md`(열화모드 정의), `docs/GPU_NOTES.md`(GPU 판정)
