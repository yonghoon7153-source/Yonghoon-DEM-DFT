# RESULTS — full-cell 곡선으로 LAM_PE와 LAM_NE를 분리할 수 있는가

> 이 파일은 `tools/make_results.py`가 결과 파일에서 자동 생성한다. 직접 수정하지 말 것.

> ## 이 문서의 protocol — 공정 paired 비교
> 
> `--no-adaptive --no-warm-start`, restart 5개 고정, 목적함수 ['pocv_dvdq', 'pocv_dvdq_dqdv'].
> 모든 조건이 **같은 restart index 집합**을 끝까지 돌고, 목적함수 간 warm start 연쇄가 없다 (F66/F86).
> 
> 기본 `docs/RESULTS.md` 는 adaptive 조기 종료 + warm start 연쇄가 있는 **비대칭 pipeline** 결과다. 목적함수 간 비교(결론 2)는 이 문서의 값을 쓰고, 기본 문서의 multi-start 수치와 섞지 말 것.

> ✅ provenance 검증 통과 — `manifest_존재`, `config_hash`, `clean_worktree`, `필수_입력_존재`, `run_spec_schema`, `sig_version`, `optimizer_정책`, `producer_곡선일치`, `목적함수_순서`, `입력봉인_교차일치`, `입력_스냅샷`, `곡선_producer_재검`, `코드_identity`, `시작_provenance`, `start_파일_존재`, `attempt_파일_존재`, `attempt_파일_일치`, `start_파일_일치`, `실행중_코드불변`, `시작종료_서명일치`, `_참고_코드재계산불가`, `입력_digest_재해시`, `run_signature_기록`, `run_signature_재계산`, `채점파일_정본`, `출력봉인_재계산`, `조건집합_서명일치`, `출력_완전성`, `출력_격자완전성`, `행별_서명`, `단일_서명`, `manifest와_일치`, `restart_출처`, `restart_예산_완주`

생성: 2026-08-16 03:56 UTC  
입력: `results/paired_fixed5_v4`  
git: `c0f1daa0d92a7625c3602799c81db04b5e2e5783`  
앵커 fits_sha256: `e033b19510ddbed951cfebe7e28793f19c5f0da915268b0731a30c56f0b3b064`  
앵커 curves_sha256(sealed): `b69dc7bee0bb2e32aba73b6ace91255d964bceb41f9361886de7275bf48aa8b8`  
(대조: `artifacts/artifact_index.yaml` — 두 값이 같은 묶음이 이 보고서의 근거다)  

## 질문

2026-08-05 연구세미나 22p에서 `LAM_PE ≈ LAM_NE ≈ 13%`, `LLI ≈ 17%`가 나왔다. 이것이 실제 물리인가, 아니면 full-cell 곡선 하나로는 두 전극을 가를 수 없어서 생긴 **fitting degeneracy**인가.

정답을 아는 PyBaMM 합성 곡선을 격자로 만들고, 기존 α·β fitting이 그 정답을 복원하는지 채점해 답한다.

## 핵심 결론

1. dQ/dV 항을 넣으면 recovery failure 가 914/1476 (61.9%) → 1287/1476 (87.2%) 로 오히려 **25%p 늘어난다.** 34p 개선안이 이 격자에서는 이득을 주지 못한다. (행별 max-mode 절대오차의 평균 2.4%p → 6.5%p, raw PE/NE 오차 반대부호 비율 68% → 36% — **물리적 상쇄로 해석 불가**)

   ⓘ **위 반대부호 비율을 '34p가 상쇄를 줄였다'로 읽지 마세요.** 이 지표는 raw 오차의 부호만 세는데, 목적함수마다 전역 편향의 부호가 달라 그 차이가 그대로 잡힙니다. 목적함수별 평균편향을 뺀 뒤 다시 세면 방향이 뒤집힙니다. 전압 민감도로 가중하지 않은 파라미터 오차 부호는 full-cell 곡선에서 실제로 상쇄되는 양을 재지도 않습니다.

2. 참값이 뚜렷이 다른 조건(|ΔLAM|_true ≥ 6%p)에서 fitting이 두 전극을 같다고 답한 것은 **1/245 (0.41%)** 다. 참 격차 9.9%p → 복원 격차 10.4%p, shrinkage 1.06. 

   이 관측이 어느 쪽을 지지하는지 **동일가중 합성격자의 조건부 사건률 비**로 보면 (population=recoverable)

   > P(같다고 답 | 참 격차 < 2%p) = 36/98 (36.73%)
   > P(같다고 답 | 참 격차 ≥ 6%p) = 1/245 (0.41%)
   > 사건률 비 = 90.0

   같은 지표를 **전체 생성성공 격자**(population=all)에서 재계산하면 넓은 격차 붕괴 64/604 (10.60%), 사건률 비 **3.69** 다. 즉 위 값은 복원가능군 선택에 강하게 의존한다 — 두 값을 **함께** 인용하지 않으면 안 된다.

   **이 값을 '두 전극이 실제로 비슷하다'로 읽을 수 없다.** 세 가지 때문이다.

   1. **임계 의존** — 같은 데이터에서 (참격차, 동일판정) 임계를 흔들면 사건률 비가 2.5~113.7(중앙값 16.8)로 움직인다. 현재 조합은 이웃보다 유독 높은 **국소 봉우리**다 — 이 값을 대표값으로 인용하면 사후선택이 된다. 아래 임계 민감도 표를 함께 볼 것.

   2. **posterior가 아님** — 이건 두 합성 가설 아래의 *사건률 비*다. `P(참값이 같다 | fitting이 같다고 답함)`으로 바꾸려면 실제 셀 집단의 사전확률과, 여기서 버린 중간 격차 구간의 주변분포가 필요하다. 격자점을 같은 빈도로 센 것은 실제 셀의 분포가 아니다.

   3. **부분집단 조건화** — 복원가능군(population=recoverable)에서만 센 값이다. 실제 셀이 그 부분집단에 속한다는 독립 근거가 없으면 적용할 수 없고, 전체 격자에서는 값이 크게 달라진다(아래 표).

   → 지금 자료로 방어할 수 있는 문장은 하나뿐이다: **이 합성 격자의 복원가능군에서, 참 격차가 뚜렷한 조건이 '같다'로 붕괴하는 일은 드물었다.** 22p가 물리인지 degeneracy인지는 이것만으로 판정되지 않는다.

   ⚠ 이 숫자들은 임계 설정에 의존한다. 붕괴로 세려면 격차를 6%p에서 2%p 아래로 끌어내려야 하므로 최소 4%p의 격차 오차가 필요한데, 실측 격차 오차는 중앙값 2.6%p·99분위 5.7%p다. 붕괴가 원리적으로 관측 가능한 범위이긴 하나, 낮은 붕괴율의 상당 부분은 **오차 스케일이 임계 간격보다 작다**는 사실에서 온다.

3. **22p 조건(LAM_PE≈LAM_NE≈13%, LLI≈17%) 근방의 recovery failure 는 1/8 (12.50%)** (목적함수 `pocv_dvdq`, 최근접 8 grid 조건, raw max-mode 오차 > 2%p 임계)  — 행별 max-mode 절대오차의 평균 1.7%p, raw PE/NE 오차 반대부호 비율 50%, 참 PE-NE 격차 1.0%p → 복원 격차 1.9%p. ⚠ 이 근방은 참값이 애초에 LAM_PE = LAM_NE인 격자점이므로, 여기서 복원이 잘 된다는 사실만으로는 22p 결과를 옹호할 수 없다 (위 2번이 답이다). 이 8개는 실제 셀이 아니라 설계 격자의 최근접 점이며, 임계·반경·noise·목적함수를 바꾸면 값이 달라진다.

4. **생성성공 격자의 52%는 선택한 grid-reference fitter 의 현재 α/bounds feasible domain 밖**이다 (참값 α<1 → 재구성 창이 reference 범위를 벗어나 truth 가 **표현 가능**하지 않다). 위 숫자는 모두 그 안쪽 2952행에서만 센 값이며, 바깥을 섞으면 목적함수 간 차이가 묻힌다. 이는 데이터의 물리 속성이 아니라 현재 표현식의 정의역 판정이다.

### 이 결론이 말하지 않는 것

- **격자 공백(F14)**: 완방 프레임 guard 때문에 저LLI 영역에 고LAM_PE 조건이 없다. 저LLI(≤2%)에서 도달한 최대 LAM_PE는 `0.08`, 격자 전체 최대는 `0.2`. 고LAM_PE 결론은 고LLI가 동반된 조건에서만 검증된 것이다.
- **restart 불일치율(F4)**: adaptive 조기 종료로 조건마다 restart 수가 달라, multi-start 불일치율을 목적함수 간 비교 지표로 쓰지 않았다. `degeneracy_summary.yaml`의 `restart_conditioned` 항목에 restart 수로 조건화한 값만 있다.
- **방법 바이어스(F5)**: 판정 기준 2%p가 방법 자체의 계통 편향과 같은 크기일 수 있어, 바이어스를 뺀 보정 판정을 표에 나란히 뒀다. 두 값이 크게 다르면 그 목적함수의 결론은 약하다.
- 모두 **합성 데이터** 결과다. 실제 셀의 모델 오차(SEI, 저항 분포 등)는 여기에 없다. 합성 truth 생성이 LLI를 양·음극 초기농도에 일률적으로 적용하는 **한 가지 규약**에 조건부이기도 하다 (SEI·plating·전극별 endpoint 이동은 같은 총 inventory loss에서도 다른 곡선을 만든다). 실제 셀이 더 나쁠지 나을지는 **증명되지 않았다** — 복잡성이 추가 정보를 만들 수도, 없앨 수도 있다.

## 목적함수 4종 비교

복원가능군(F1)만, 노이즈 전체 합산.

| objective | n | degeneracy | (바이어스 보정) | 평균 max-mode \|err\| | raw 반대부호 |
|---|---|---|---|---|---|
| pOCV + dV/dQ  (33p 기존) | 1476 | 62% | 14% | 2.4%p | 68% |
| pOCV + dV/dQ + dQ/dV  (34p 개선) | 1476 | 87% | 95% | 6.5%p | 36% |

### 전체 격자 (복원불가군 포함)

복원불가군(참 α<1)은 grid 기준에서 정답이 재구성 창 밖이라 **원리적으로** 복원되지 않는 조건이다. 위 표에서 뺀 근거는 그것이다. 다만 그 제외가 난이도와 무관하지 않으므로(저LLI에서 복원가능 비율이 훨씬 낮다) 전체군을 같이 싣는다.

| objective | n | degeneracy | (바이어스 보정) | 평균 max-mode \|err\| | raw 반대부호 |
|---|---|---|---|---|---|
| pOCV + dV/dQ  (33p 기존) | 3069 | 74% | 52% | 3.7%p | 55% |
| pOCV + dV/dQ + dQ/dV  (34p 개선) | 3069 | 90% | 89% | 6.6%p | 30% |

### 노이즈 수준별 (F10)

dQ/dV의 이점은 노이즈에서 희석된다. 노이즈 0 결과만 인용하면 과대평가가 된다.

| objective | noise | n | degeneracy | (바이어스 보정) | 평균 max-mode \|err\| | raw 반대부호 |
|---|---|---|---|---|---|---|
| pOCV + dV/dQ  (33p 기존) | 0 | 492 | 60% | 12% | 2.3%p | 71% |
| pOCV + dV/dQ  (33p 기존) | 0.001 | 492 | 62% | 13% | 2.4%p | 69% |
| pOCV + dV/dQ  (33p 기존) | 0.005 | 492 | 64% | 18% | 2.5%p | 65% |
| pOCV + dV/dQ + dQ/dV  (34p 개선) | 0 | 492 | 88% | 94% | 6.6%p | 39% |
| pOCV + dV/dQ + dQ/dV  (34p 개선) | 0.001 | 492 | 88% | 94% | 6.6%p | 37% |
| pOCV + dV/dQ + dQ/dV  (34p 개선) | 0.005 | 492 | 86% | 96% | 6.4%p | 31% |

## 22p 실험 조건 판정

*모두 `noise = 0` 조건이다. 노이즈가 있으면 값이 달라진다(F10) — `objective_comparison.yaml`의 `verdict_22p.noise` 참조.*

| objective | 근방 조건 | degeneracy | 평균 \|err\| | err LAM_PE | err LAM_NE | raw 반대부호 |
|---|---|---|---|---|---|---|
| pocv_dvdq | 8 | 12% | 1.7%p | -1.7%p | 0.1%p | 50% |
| pocv_dvdq_dqdv | 8 | 50% | 3.7%p | -3.4%p | 0.4%p | 50% |

> ⚠ **`raw 반대부호` 열을 degeneracy의 지문으로 읽지 마세요.** 이 열은 raw 오차의 부호가 반대인 비율일 뿐이고, 목적함수마다 전역 편향의 부호가 다르면 그 차이가 그대로 잡힙니다. 편향을 중심화하면 목적함수 간 순서가 뒤집힙니다. 또 전압 민감도로 가중하지 않은 파라미터 오차 부호는 full-cell 곡선에서 실제로 상쇄되는 양을 재지 않습니다.

## 전극 격차를 구분하는가 — 22p 질문의 직접적인 답

*`noise = 0` 조건 기준.*

22p 근방 격자점은 **참값이 애초에 `LAM_PE = LAM_NE`** 다. 거기서 복원값이 비슷하게 나오는 건 아무 증거가 못 된다. 물어야 할 것은 반대 방향이다 — **참값이 뚜렷이 다를 때도 fitting이 둘을 같다고 말하는가.**

| objective | 넓은 격차 조건 n | **격차 붕괴율** | shrinkage | 거짓 분리율 | 붕괴에 필요한 격차오차 / 실측 중앙값 |
|---|---|---|---|---|---|
| pocv_dvdq | 245 | **0%** | 1.06 | 63% | 4%p / 2.6%p |
| pocv_dvdq_dqdv | 245 | **7%** | 1.40 | 73% | 4%p / 4.2%p |

- **격차 붕괴율**: 참 격차 ≥ 6%p인데 복원 격차 < 2%p로 답한 비율. 높을수록 "두 전극이 비슷하다"는 관측이 무의미해진다.
- **shrinkage**: 복원 격차 / 참 격차의 평균. 1이면 격차를 그대로 복원, 0에 가까우면 전부 뭉갠다.
- **거짓 분리율**: 참값은 같은데 다르다고 답한 비율 (반대 방향 오류).
- **붕괴에 필요한 격차오차**: 붕괴로 세려면 격차를 6%p에서 2%p 아래로 끌어내려야 하므로 최소 4%p의 격차 오차가 필요합니다. 이 값이 실측 격차오차 중앙값보다 크면, **낮은 붕괴율은 측정이 아니라 임계 설정의 결과**입니다 — 그대로 인용하지 마세요.

### 임계 민감도 — 위 숫자를 인용하기 전에 볼 것

같은 데이터에서 (참 격차 cutoff, 동일 판정 tol) 두 임계만 바꿔 사건률 비를 다시 센 것이다 (`pocv_dvdq`, noise=0, 복원가능군). 값이 한 자릿수에서 수십까지 움직이면, 특정 조합의 값은 **측정이 아니라 선택**이다.

**참값 "같다" = 참 격차 < tol**

| 참 격차 ≥ \ 동일 판정 < | 1%p | 2%p | 3%p | 4%p | 5%p |
|---|---|---|---|---|---|
| **2%p** | 2.5<br><sub>12/66 ÷ 29/394</sub> | — | — | — | — |
| **4%p** | 4.5<br><sub>12/66 ÷ 12/299</sub> | 4.6<br><sub>36/98 ÷ 24/299</sub> | 5.1<br><sub>99/166 ÷ 35/299</sub> | — | — |
| **6%p** | 44.5<br><sub>12/66 ÷ 1/245</sub> | 90.0<br><sub>36/98 ÷ 1/245</sub> | 13.3<br><sub>99/166 ÷ 11/245</sub> | 6.5<br><sub>133/193 ÷ 26/245</sub> | 5.0<br><sub>183/247 ÷ 36/245</sub> |
| **8%p** | 30.0<br><sub>12/66 ÷ 1/165</sub> | 60.6<br><sub>36/98 ÷ 1/165</sub> | 98.4<br><sub>99/166 ÷ 1/165</sub> | 113.7<br><sub>133/193 ÷ 1/165</sub> | 20.4<br><sub>183/247 ÷ 6/165</sub> |

**참값 "같다" = 참 격차 정확히 0**

| 참 격차 ≥ \ 동일 판정 < | 1%p | 2%p | 3%p | 4%p | 5%p |
|---|---|---|---|---|---|
| **2%p** | 2.5<br><sub>12/66 ÷ 29/394</sub> | — | — | — | — |
| **4%p** | 4.5<br><sub>12/66 ÷ 12/299</sub> | 4.5<br><sub>24/66 ÷ 24/299</sub> | 5.8<br><sub>45/66 ÷ 35/299</sub> | — | — |
| **6%p** | 44.5<br><sub>12/66 ÷ 1/245</sub> | 89.1<br><sub>24/66 ÷ 1/245</sub> | 15.2<br><sub>45/66 ÷ 11/245</sub> | 8.7<br><sub>61/66 ÷ 26/245</sub> | 6.6<br><sub>64/66 ÷ 36/245</sub> |
| **8%p** | 30.0<br><sub>12/66 ÷ 1/165</sub> | 60.0<br><sub>24/66 ÷ 1/165</sub> | 112.5<br><sub>45/66 ÷ 1/165</sub> | 152.5<br><sub>61/66 ÷ 1/165</sub> | 26.7<br><sub>64/66 ÷ 6/165</sub> |

각 칸은 `사건률 비` 아래에 `분자/분모 ÷ 분자/분모`를 함께 적었다. `∞`는 넓은 격차군에서 붕괴가 0건이라는 뜻이며, 요약 통계의 min/max 범위에서는 제외되므로 개수를 `gap_analysis.lr_sensitivity_n_infinite`로 따로 센다. 표의 최댓값을 대표값으로 쓰지 말 것.

### 모집단을 바꾸면 (복원불가군 포함)

| 모집단 | n(참격차 작음) | n(참격차 큼) | 붕괴 | 사건률 비 |
|---|---|---|---|---|
| 복원가능군 | 98 | 245 | 0% | 90.0 |
| 전체 격자 | 156 | 604 | 11% | 3.7 |

복원가능군 조건화는 물리적 근거가 있지만(참 α<1이면 정답이 재구성 창 밖), **그 조건화가 사건률 비를 크게 바꾼다**는 사실은 결론과 같은 무게로 적어야 한다.

## multi-start 진단 — 진짜 degeneracy와 최적화 난이도의 구분

같은 조건을 여러 초기값에서 다시 풀었을 때 어떻게 갈리는지를 봅니다. **두 실패 모드는 처방이 정반대**라 반드시 나눠야 합니다.

> 아래 표는 **무작위 restart끼리만** 비교한 것입니다(F21b). dQ/dV 목적함수는 첫 restart에 매끄러운 해를 초기값으로 받으므로, 그것을 포함하면 최적 J에 닿는 restart가 정의상 하나뿐이 되어 항상 multimodal로 찍힙니다.

| objective | n | **flat valley** | multimodal | unique min |
|---|---|---|---|---|
| pocv_dvdq | 1476 | **4%** | 60% | 36% |
| pocv_dvdq_dqdv | 1476 | **1%** | 97% | 2% |

- **flat valley** — 같은 J인데 해가 서로 멀다. **데이터가 그 조합을 구분하지 못한다는 직접 증거**입니다. 초기값을 아무리 잘 줘도 사라지지 않고, 측정 방식을 바꿔야 줄어듭니다.
- **multimodal** — J가 다른 국소최소가 여럿. degeneracy가 아니라 **최적화 난이도**입니다. 좋은 초기값을 주면 사라집니다 (dQ/dV 항이 이 경우였습니다 — 아래 참조).
- **unique min** — 해가 유일. 문제 없음.

> ⚠ **`pocv_dvdq_dqdv`의 multimodal이 97%로 극단적입니다.** flat valley 판정은 restart 2개 이상이 같은 J에 닿아야 성립하므로, 이렇게 지형이 울퉁불퉁하면 flat valley가 있어도 **관측되지 않습니다.** 이 목적함수의 낮은 flat valley 값을 "degeneracy가 적다"로 읽으면 안 됩니다. (예전에는 여기서 Hessian을 대안으로 안내했으나, 그 지표도 eps 미수렴·안장점 혼입·가설과 다른 부호 규약으로 근거가 되지 못합니다 — F33.)

> ⚠ `degeneracy_summary.yaml`의 `restart_conditioned` 블록에 있는 `agree_frac`과 `p_spread`는 인용하지 마세요. adaptive 조기 종료 때문에 `agree_frac`은 restart를 5까지 간 조건에서 **정의상 0**이고, `p_spread = 0`은 "해가 일치"가 아니라 "최적 J에 도달한 restart가 하나뿐"이라는 뜻입니다. 위 표가 그 자리를 대신합니다.

## 그림

- `results/paired_fixed5_v4/figures/gap_recovery_pocv_dvdq.png` — gap_pocv_dvdq
- `results/paired_fixed5_v4/figures/gap_recovery_pocv_dvdq_dqdv.png` — gap_pocv_dvdq_dqdv
- `results/paired_fixed5_v4/figures/objective_panel_noise0.png` — noise_0
- `results/paired_fixed5_v4/figures/objective_panel_noise0.001.png` — noise_0.001
- `results/paired_fixed5_v4/figures/objective_panel_noise0.005.png` — noise_0.005

## 재현

```bash
./scripts/setup_env.sh && source .venv/bin/activate
./run.sh --mode verify
./run.sh --mode grid --config configs/grid_fine.yaml --nproc $(nproc) --out results/grid_curves_v4
./run.sh --mode fit   --in results/grid_curves_v4 --out results/paired_fixed5_v4 --nproc $(nproc) --objective pocv_dvdq,pocv_dvdq_dqdv --n-restarts 5 --no-adaptive --no-warm-start
./run.sh --mode score --in results/paired_fixed5_v4
./run.sh --mode hessian --in results/paired_fixed5_v4
./run.sh --mode report --in results/paired_fixed5_v4
```

> **재현 범위**: 위 명령은 이 산출물의 서명된 fit·sweep·half-cell 설정(objective·restart·clean/noisy·adaptive·warm start·reference·bounds preset·half-cell method·sweep w_grid/stride)을 복원합니다. 아직 명령으로 내보내지 않는 축은 sweep 의 bounds/reference/tol·optimizer method 와 비기본 `eps` 의 추가 Hessian 입니다 — 이 artifact 들이 기본값으로 돌았다면 그대로 재현되고, 아니면 해당 절은 `manifest.yaml` 의 `run_spec` 을 직접 보고 맞춰야 합니다.

관련 문서: `docs/06_REVIEW_DECISIONS.md`(해석 규칙), `docs/07_LAM_LLI.md`(열화모드 정의), `docs/GPU_NOTES.md`(GPU 판정)
