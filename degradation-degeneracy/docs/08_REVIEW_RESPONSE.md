# 08. 적대적 교차리뷰 회답

> **리뷰 기준 커밋**: `1790a9cc`
> **1차 회답**: `cb23274` (F25~F30) / **2차 회답**: `3c1109f` (F31~F35) /
> **3차 회답**: 이 문서 (F36~F40)
> **회답일**: 2026-08-07
> **한 줄**: 코드·데이터로 검증 가능한 지적 9건을 전부 재계산했고, **하나도
> 반박되지 않았습니다.** 버그 4건을 고쳤고, 핵심 결론 문구 2개를 철회합니다.

---

## 0. 총평 — 무엇이 무너지고 무엇이 남았나

| 결론 | 리뷰 전 | 회답 후 |
|---|---|---|
| **1. 22p는 degeneracy가 아니다** (우도비 46:1) | 핵심 산출물 | ❌ **철회.** 46:1은 임계가 만든 국소 봉우리다. 남는 문장은 "이 격자의 복원가능군에서 뚜렷한 참 격차가 '같다'로 붕괴하는 일은 드물었다"뿐이고, 이것으로 22p를 판정할 수 없다 |
| **2. dQ/dV는 degeneracy를 못 줄였다** (62→63%) | 앞뒤 두 문장 | ⚠️ **앞 절반만.** "2%p 임계에서 유의한 차이를 검출하지 못했다"는 유지. **단 모집단에 따라 방향이 뒤집힌다.** 뒤 절반(PE-NE 상쇄 68→48%)은 ❌ 철회 |
| **3. 목적함수보다 기준 곡선이 크다** (7% vs 62%) | 부수 발견 | ✅ **유지.** 33p에서 McNemar p≈1e-202. 단 원인을 "곡선 범위"가 아니라 **"reference 생성 pipeline"** 으로 좁힘. 다른 목적함수의 halfcell 수치는 버그로 무효였고 재계산함 |

가장 아픈 것은 **결론 1**입니다. 이 프로젝트가 답하려던 질문의 답이었는데, 지금
자료로는 그렇게 말할 수 없습니다.

---

## 1. 검증 결과 — 9건 전부 확인

`artifacts/`에 fits.parquet이 커밋돼 있어 재계산이 가능했습니다.

| # | 리뷰의 주장 | 검증 | 방법 |
|---|---|---|---|
| 1 | 46:1은 posterior가 아니고 모집단 의존 | ✅ | 복원가능군 **46.25**, 전체 격자 **3.69** |
| 2 | 임계 선택이 46:1을 만든다 | ✅ | 참격차 ≥2/4/6%p → **2.3 / 4.5 / 46.4** |
| 3 | 복원불가 제외가 결론 2의 방향을 바꾼다 | ✅ | 복원가능군 33p 61.9 < 34p 63.3, **전체 74.1 > 71.9** |
| 4 | mixed-reference에서 recoverable이 전부 True | ✅ | `(reference != "grid").any()` — 프레임 전체 |
| 6 | 68→48%는 전역 편향의 산물 | ✅ | 중심화하면 **33.1 → 42.9%로 역전** |
| 8 | half-cell `p_ini`를 33p 하나로 덮어씀 | ✅ | 34p **99.1% → 10.0%** |
| 11 | `skip_first`가 warm이 아니라 best restart를 버림 | ✅ | `results.sort(key=lambda t: t[1])` 후 직렬화 |
| 12 | `pe_ne_coupled`가 가설과 반대 부호를 셈 | ✅ | `a_pe * a_ne > 0` |
| 14 | artifact provenance 없음 | ✅ | `config_hash: ''`, `git_dirty: true` |

나머지(5·7·9·10·13·15)는 해석·설계에 대한 지적이며 사실관계에 이견이 없습니다.

---

## 2. 결론 1 — 46:1을 철회합니다

### 계산은 맞았고, 해석이 틀렸습니다

분자·분모를 뒤집어 쓰지는 않았습니다. 재계산해도 `37/98 ÷ 2/245 = 46.25`가
그대로 나옵니다. 문제는 이 값이 **특정 임계 조합에서만** 나온다는 것입니다.

**임계 민감도** (33p, noise=0, 복원가능군). 아래 좌측 열은 **참 격차 정확히 0**을
"같다"로 본 값이고, 우측 열과 46.25는 **참 격차 < tol**을 "같다"로 본 값이다.
두 정의가 다르다는 것을 F34에서 코드로 분리했다:

| 참 격차 cutoff | 우도비 | | 복원 동일 임계 | 우도비 |
|---:|---:|---|---:|---:|
| ≥2%p | **2.3** | | <1%p | 22.3 |
| ≥4%p | **4.5** | | **<2%p** | **46.4** |
| **≥6%p** | **46.4** | | <3%p | 15.2 |
| | | | <4%p | 9.2 |
| 전체 격자 | **3.69** | | <6%p | 5.0 |

이웃 임계에서 한 자릿수인 값을 46:1로 인용하면 사후선택입니다. 제가 붙여뒀던
임계 경고는 **경고로 부족했습니다** — 경고가 아니라 "그 숫자를 못 쓴다"는
뜻이었어야 했습니다.

### 세 가지 제약

1. **posterior가 아닙니다.** 두 합성 가설 아래의 *사건* 우도비입니다.
   `P(참값이 같다 | fitting이 같다고 답함)`으로 바꾸려면 실제 셀 집단의
   사전확률과, 버린 2~6%p 중간 구간의 주변분포가 필요합니다.
   격자점을 같은 빈도로 센 것은 실제 셀의 분포가 아닙니다.
2. **부분집단 조건화입니다.** 복원가능군에서만 센 값이고, 실제 셀이 그
   부분집단에 속한다는 truth 없는 판정 방법이 없습니다.
3. **임계 의존입니다.** 위 표.

### 지금 방어할 수 있는 문장

> 이 합성 격자의 복원가능군에서, 참 격차가 뚜렷한(≥6%p) 조건이 복원 시
> '같다'(<2%p)로 붕괴하는 일은 드물었다 (2/245).

**22p가 물리인지 degeneracy인지는 이것만으로 판정되지 않습니다.**

### 코드 조치

- `gap_sensitivity()` 신설 — 임계 2차원 표를 **항상** 함께 낸다
- `gap_analysis`가 `lr_sensitivity_min/max/median`·`lr_is_local_spike`를
  자기 dict에 넣어 떼어 인용하지 못하게 한다
- `make_results.py`가 우도비 밑에 세 제약을 **상시** 붙인다
- 테스트: `"실제로 비슷하게 열화했다"`가 문서에 나오면 실패

---

## 3. 결론 2 — 절반만, 그것도 모집단을 밝혀야

### (a) 방향이 모집단에 따라 뒤집힙니다

raw degeneracy 비율:

| 목적함수 | 전체 격자 | 복원가능군 | 복원불가군 |
|---|---:|---:|---:|
| dQ/dV only | 80.4% | 76.7% | 83.9% |
| pOCV only | 80.3% | 77.8% | 82.5% |
| **33p** | **74.1%** | **61.9%** | 85.3% |
| **34p** | **71.9%** | **63.3%** | 80.0% |

복원가능군에서는 33p가 1.4%p 낫고, **전체 격자에서는 34p가 2.2%p 낫습니다.**

복원불가군(참 α<1)은 grid 기준에서 정답이 재구성 창 밖이라 원리적으로 복원되지
않는 조건이므로 제외에 근거는 있습니다. 하지만 **그 제외가 우열을 바꾼다면**
제외 사실을 결론과 같은 무게로 적어야 합니다. 게다가 제외는 난이도와 무관하지
않습니다 — 복원가능 비율이 LLI=0에서 2.3%, LLI=0.20에서 91.7%입니다.

조치: `comparison_table(recoverable_only=False)` 추가, 전체군 표 상시 병기,
`population_sensitivity.direction_flips`로 뒤집힘을 스스로 판정해 경고.

### (b) "PE-NE 상쇄 68→48%"는 철회합니다

noise=0·복원가능군의 목적함수별 **평균 편향**:

| 목적함수 | LLI | LAM_PE | LAM_NE |
|---|---:|---:|---:|
| 33p | −1.57%p | **−1.64%p** | **+0.98%p** |
| 34p | −1.86%p | **−2.17%p** | **−0.21%p** |

33p는 PE·NE 편향의 **부호부터 반대**이고 34p는 같습니다. `pe_ne_antisym`은 raw
오차의 부호만 세므로 이 전역 위치 차이를 그대로 "상쇄"로 잡습니다.

```
raw 반대부호 비율        70.5%  →  52.6%
목적함수별 편향 중심화    33.1%  →  42.9%     ← 방향이 뒤집힘
raw PE-NE 오차 상관     +0.754    −0.287
```

33p의 중심화 상관이 **+0.754**라는 건 두 전극 오차가 *같이* 움직인다는 뜻입니다.
PE-NE 트레이드오프가 아닙니다. "34p가 상쇄를 줄였다"는 인과 해석을 내립니다.

덧붙여, 전압 민감도로 가중하지 않은 파라미터 오차 부호는 full-cell 곡선에서
실제로 상쇄되는 양을 재지도 않습니다.

조치: 결론에 경고 상시 부착 + 테스트로 고정.

### (c) 유지되는 것

**"사전 지정한 2%p 임계에서, 복원가능군 기준으로 33p와 34p의 유의한 차이를
검출하지 못했다."** 이건 null 결과이지 동등성 증명이 아닙니다.

리뷰의 paired 검정(McNemar p=0.30, bootstrap 95% CI `[-1.1, +3.8]%p`)도
같은 방향입니다.

---

## 4. 결론 3 — 유지하되 원인 귀속을 좁힙니다

### 관측은 강합니다

33p 공통 1,476조건 paired: half-cell **6.6%** vs grid **61.9%**,
grid에서만 실패 855 / half-cell에서만 실패 38, exact McNemar **p ≈ 3.7e-202**.
임계를 0.5~5%p로 흔들어도 방향이 유지됩니다.

**그리고 이 값은 아래 `p_ini` 버그를 고쳐도 한 자리도 안 변합니다** — 33p가 곧
원점 제공자였기 때문입니다.

### 다만 "곡선 범위 때문"은 못 씁니다

case 변경에는 reference coverage뿐 아니라 좌표 원점·정규화·half-cell 변환식·
bounds preset·pristine `p_ini`가 함께 들어갑니다. ablation 없이 단일 원인으로
귀속할 수 없습니다.

→ **"reference 생성 pipeline이 목적함수 변경보다 큰 관측 차이를 만들었다"** 로
축소합니다.

---

## 5. 버그 4건 — 고쳤습니다

### F26. half-cell `p_ini`를 목적함수 하나로 전부 덮어씀 ★

`src/fitting.py`가 pristine 조건을 `pocv_dvdq`로 **한 번만** fit해 모든 목적함수
task에 주입하고 있었습니다. 목적함수마다 pristine optimum이 다른데 공통 원점을
강제한 셈입니다.

목적함수별 pristine fit (실측):

| objective | α_PE | β_PE | α_NE | β_NE |
|---|---:|---:|---:|---:|
| pocv | 1.51409 | −0.41920 | 1.12157 | −0.11930 |
| pocv_dvdq | 1.47598 | −0.40844 | 1.06166 | −0.05826 |
| pocv_dvdq_dqdv | 1.51873 | −0.42200 | 1.06265 | −0.05949 |
| dqdv_only | 1.48489 | −0.41018 | 1.05073 | −0.05073 |

목적함수별 원점으로 다시 변환 (공통 1,476조건):

| objective | 공통 `p_ini` | 목적함수별 `p_ini` | 평균\|err\| |
|---|---:|---:|---|
| pOCV only | 99.5% | **59.5%** | 9.38 → 4.17%p |
| 33p | 6.6% | 6.6% | 1.41 → 1.41%p (원점 제공자) |
| **34p** | 99.1% | **10.0%** | **3.94 → 1.43%p** |
| dQ/dV only | 99.9% | 99.8% | 6.53 → 6.08%p |

> **제가 "미해결"로 남겨뒀던 Case 1의 LAM_PE −4.1%p 오프셋이 바로 이것이었습니다.**
> −3.83 → −1.09%p. 리뷰가 제 숙제를 풀어줬습니다. 잔여 −1.2%p는 여전히 남습니다.

`docs/RESULTS.md`의 halfcell 100%/99% 표와 "reference 효과가 모든 목적함수에
공통"이라는 일반화를 철회합니다.

### F25. `skip_first`가 warm이 아니라 best restart를 버림 ★

`fit()`이 `results.sort(key=lambda t: t[1])`로 **J 오름차순 정렬 후** 직렬화하는데,
`multistart_diagnostics(skip_first=True)`는 "첫 항목 = warm start"로 보고 그걸
버렸습니다. 실제로는 **가장 좋은 해를 버리고** 있었습니다.

`degeneracy_summary.yaml`의 `multistart_random_only` 블록 **전체가 무효**입니다.
그리고 `docs/06_REVIEW_DECISIONS.md`의 F4 처리 사유("원본을 저장했으므로 사후
재집계 가능")도 틀렸습니다 — 정렬 과정에서 출처가 소실됐습니다.

조치:
- restart마다 `{"p", "J", "i", "warm"}` 저장 (`fit(warm_init=...)`)
- `skip_first`는 flag로 거른다. 출처 없는 옛 형식은 **보정을 생략하고 경고**
- 요약에 `warm_start_보정_적용` 필드 — 무효인 블록을 모르고 인용하지 못하게
- **기존 artifact로는 복구 불가.** 재fit 필요

### F27. `recoverable` 판정이 프레임 전체

`(out["reference"] != "grid").any()` — halfcell 행이 하나만 섞여도 grid 행까지
전부 복원가능이 됐습니다. 비교표의 분모가 소리 없이 늘어나는 실패라 눈으로는
못 잡습니다. 행별 `np.where`로 바꾸고, halfcell의 `True`가 **측정이 아니라
가정**임을 `recoverable_measured` 열로 남깁니다.

### F30. artifact provenance 없음

`grid_fine_v2`·`halfcell_v1` 둘 다 `config_hash: ''` + `git_dirty: true`,
dirty patch 없음. parquet은 재집계할 수 있어도 그 숫자를 만든 코드가 없습니다.

조치: `base_manifest(cfg_hash, out_dir=, inputs=)`가 dirty diff를
`run_dirty.patch`로 저장하고, 입력 파일 SHA-256을 기록하며, `reproducible`
플래그와 `_주의`를 자동으로 답니다. fitting은 실제 `obj_cfg` 내용을 해시해
`config_hash`에 넣습니다.

---

## 6. Hessian — 식별성 근거에서 내립니다

### `pe_ne_coupled`가 가설과 반대 방향을 셌습니다

`src/hessian.py`는 평평한 방향에서 `a_pe * a_ne > 0`, 즉 **같은 부호**를 셉니다.
그런데 22p의 degeneracy 가설은 "한 전극을 과대평가한 만큼 다른 전극을 과소평가"
= `δLAM_PE · δLAM_NE < 0`이고, `LAM = 1 − rα`이므로 α에서도 **부호가 반대**입니다.
지표가 정확히 그 방향을 제외하고 있었습니다.

제가 반대부호 방향도 직접 세봤습니다:

| objective | 같은 부호 (코드가 센 것) | 반대 부호 (22p 가설 방향) |
|---|---:|---:|
| pocv | 0.0% | 0.5% |
| pocv_dvdq | 0.0% | 0.0% |
| pocv_dvdq_dqdv | 0.0% | 0.0% |
| dqdv_only | 1.0% | 0.0% |

지표 방향을 고쳐도 숨어 있던 결합이 나타나지는 않습니다. 그래도
**`pe_ne_coupled = 0%`를 "degeneracy가 아니다"의 근거로 쓸 수 없습니다** —
지표가 묻는 질문이 달랐기 때문입니다.

### eps 미수렴·안장점 혼입

`docs/RESULTS.md`가 이미 경고를 달고 있었지만, **경고를 단 같은 표를 식별성
결론에 계속 쓰는 것은 타당하지 않다**는 지적이 맞습니다. 34p는
`min_eigval_positive`가 83.5%로, 16.5%는 안장점에서 곡률을 잰 것입니다.

→ Hessian 절을 결론 근거에서 내리고 **진단 참고**로만 둡니다.

---

## 7. 리뷰의 이전 결정 재판정을 수용합니다

| 항목 | 기존 처리 | 재판정 | 수용 |
|---|---|---|---|
| F1 복원불가군 분리 | 분리 보고 | 전체군을 동등하게 병기해야 | ✅ F29 |
| F4 restart 원본 저장 | 사후 재집계 가능 | **기각 사유가 틀렸다** | ✅ F25 |
| F5 clean bias 차감 | 이원화 | operational calibration이지 식별성 보정이 아님 | ✅ 문구 수정 |
| F14 저LLI·고LAM_PE 코너 | 경고 | 경고로 부족, 설계 결손 | ✅ 인정 |
| F15 프레임 불일치 | 수정 완료 | halfcell `p_ini`는 별개로 남음 | ✅ F26 |
| F20~F20d warm start | 이력 기록 | 동일 budget 비교 남음 | ⏳ 재실행 필요 |
| F23 Hessian eps | 경고 | 경고 단 표를 계속 쓰면 안 됨 | ✅ §6 |

---

## 8. 남은 것 — 재실행이 필요한 두 가지

계산 없이 되는 건 다 했습니다. 아래는 CPU 시간이 듭니다.

| 항목 | 내용 | 비용 |
|---|---|---|
| **A. Case 1 재fit** | F26 수정 반영 (목적함수별 `p_ini`) + F25 restart 출처 | 약 5시간 |
| **B. Case 2 재fit** | F25 restart 출처. 모드 수치 자체는 안 바뀜 | 약 3시간 |
| **C. paired 비교 재실행** | 33p/34p 동일 seed·동일 restart budget·early stop off | 약 4시간 |
| **D. clean commit 재생성** | F30 provenance를 갖춘 artifact | A~C에 포함 |

**A와 D는 필수**입니다 — `docs/RESULTS.md`의 halfcell 표가 현재 무효입니다.
B는 모드 수치가 안 바뀌므로 multi-start 진단을 살릴 때만 필요합니다.
C는 결론 2를 "objective의 정보량 비교"로 말하려면 필요하고, "현재 pipeline에서
관측된 값"으로만 말한다면 생략할 수 있습니다.

### 재실행 전에 인용하면 안 되는 것

- `docs/RESULTS.md`의 **우도비 46:1** 및 그에 딸린 결론 문장
- **halfcell 100% / 99%** 표 (pocv·34p·dqdv_only)
- **PE-NE 상쇄 68% → 48%**
- **`multistart_random_only`** 블록 전체
- **`pe_ne_coupled = 0%`**
- 현재 `artifacts/`의 수치 일반 (provenance 없음 — 방향성 참고로만)

### 인용해도 되는 것

- 33p의 **halfcell 6.6% vs grid 61.9%** (McNemar p≈1e-202, `p_ini` 버그 무관)
- 복원가능군 기준 **"33p와 34p의 유의한 차이를 검출하지 못했다"** (모집단 명시 필수)
- **격자의 52%가 grid 기준에서 원리적으로 복원 불가**라는 사실
- 저LLI에서 LAM_NE가 full-cell 용량에 거의 흔적을 안 남긴다는 곡선 단계 관측

---

## 9. 왜 이걸 못 잡았나 — 재발 방지

리뷰가 지적한 것 중 **테스트 174개가 하나도 못 잡은 것**들이 있습니다.
이유가 전부 같습니다: **테스트가 production 경로를 안 지났습니다.**

| 놓친 것 | 왜 | 조치 |
|---|---|---|
| F25 restart 출처 | 테스트가 warm entry를 손으로 첫 번째에 두고 JSON을 만들었다. production은 J로 정렬한다 | round-trip 테스트 + "위치가 아니라 flag" 테스트 |
| F26 `p_ini` | half-cell 변환 테스트가 양쪽에 같은 `p_ini`를 넣었다 | `run_fit` 소스에서 목적함수별 fit을 강제 |
| F27 프레임 전체 판정 | 단일 reference 프레임만 테스트했다 | mixed-reference 테스트 |
| F28/F29 임계·모집단 | 정해진 임계의 count만 확인했다 | 민감도 표·전체군 표 생성 테스트 |
| F30 provenance | dirty manifest를 실패시키는 테스트가 없었다 | `reproducible` 플래그 테스트 |

그리고 더 근본적으로 — **`make_results.py`를 "자기 감시형"으로 만든 것으로는
부족했습니다.** 경고를 붙이는 것과 그 숫자를 결론에서 내리는 것은 다릅니다.
임계 의존성을 스스로 경고하면서 46:1을 결론 문장에 그대로 실었던 것이 그
예입니다. 이번에는 **경고가 아니라 문장 자체를 바꿨고**, 옛 문장이 다시 나오면
테스트가 깨지게 해뒀습니다.

---

## 10. 재현

```bash
# 리뷰 주장 재계산 (계산 없이 커밋된 parquet만 읽음)
python - <<'EOF'
import pandas as pd
from src.scoring import add_error_columns, classify_recoverability
d = pd.read_parquet('artifacts/grid_fine_v2/fits.parquet')
s = classify_recoverability(add_error_columns(d, 0.02))
for o in ['pocv_dvdq', 'pocv_dvdq_dqdv']:
    g = s[s.objective == o]
    print(o, '전체', g.degenerate.mean(), '복원가능', g[g.recoverable].degenerate.mean())
EOF

# sweep과 본 실행의 일치 확인
python -m tools.check_sweep_consistency --sweep results/grid_fine_v2/wsweep --main results/grid_fine_v2
```

관련 문서: `CHANGELOG.md`(F25~F30 상세), `docs/06_REVIEW_DECISIONS.md`(이전 리뷰
대장), `docs/RESULTS.md`(자동 생성 — 재실행 후 갱신 예정).

---

## 11. 2차 리뷰 회답 (2026-08-07, F31~F35)

1차 회답(`cb23274`)에 대한 재리뷰에서 **차단 항목 5건**이 나왔고, 전부 맞았습니다.
아래를 고친 뒤에야 재실행에 착수합니다.

| # | 지적 | 판정 | 조치 |
|---|---|---|---|
| 1 | pristine `p_ini`가 본 fitting과 다른 optimizer protocol | ✅ | **F26b** — 실행 로그에서 독립적으로 먼저 잡음. 목적함수 dict 전체를 한 task로 넘겨 warm start 연쇄를 본 fitting과 일치시킴. 실측: `dqdv_only` 원점이 단독 `1.5708` vs 연쇄 `1.4849`로 갈렸음 |
| 2 | resume signature가 결과 혼합을 못 막음 | ✅ | **F32** — 서명에 가중치·수치 bounds·`n_restarts`·dqdv/scaling 설정·base config·curves SHA를 포함. 행마다 `run_sig`를 박고, 병합 시 서명이 둘 이상이면 **실패시킴** |
| 3 | 철회한 Hessian 해석이 생성기에 남음 | ✅ | **F33** — 핵심 결론에서 제거, 절 제목을 "참고용, 결론 근거 아님"으로 강등, "최적화와 무관" 표현 삭제, multistart 경고의 Hessian 유도 제거. "실제 degeneracy의 하한"과 "degeneracy 특징적 지문"도 삭제 |
| 4 | F28의 "정확히 0"과 구현 불일치 | ✅ | **F34** — `same_def`를 `lt_tol`/`exact_zero` 둘 다 계산해 표를 나란히 냄. `lr_is_local_spike`를 **이웃 한 칸**(gap±1, tol±1) 중앙값 기준으로 변경. `∞` 개수를 `lr_sensitivity_n_infinite`로 별도 표기. 각 칸에 분자/분모 병기 |
| 5 | "random-only"가 실제로는 random-only가 아님 | ✅ | **F31** — restart 출처를 `warm` / `base_init` / `random` 3종으로 기록하고, random-only는 `source == "random"`만 사용. `warm_dropped`(형식 판정) → `n_nonrandom_dropped`(실제 개수). 목적함수 간 남은 restart 수 편차를 재서 `비교가능` 플래그로 표기 |

추가로 **F35** — `RESULTS.md` 맨 위에 인용 금지 배너를 생성기에 넣었습니다.
provenance가 갖춰지면 배너가 사라지도록 양방향 테스트로 고정했습니다.

### 지적 6·7에 대한 답

- **6 (provenance 미완)**: untracked 파일을 dirty 판정에서 뺀 것은 의도적입니다 —
  사용자 저장소 루트에 다른 프로젝트 산출물이 상시 20여 개 있어, 그대로 두면
  모든 실행이 영구히 dirty로 찍혀 플래그가 무의미해집니다. 대신
  `git_untracked_count`로 개수를 남깁니다. half-cell 캐시는 이제 `input_sha256`에
  포함됩니다. 청크별 서명은 행 단위 `run_sig`로 대체했고, 병합 시 혼합을
  **에러로** 막습니다.
- **7 (RESULTS.md 인용 금지 + 자기모순)**: 배너를 넣었고, "6.6% vs 61.9%는 인용
  가능"을 **철회**합니다. provenance 기준을 적용한다면 정확한 비율과 p-value도
  재실행 전에는 쓸 수 없습니다. 방향성 관측으로만 남깁니다.

### 이번에도 같은 교훈

리뷰의 *"현재 테스트는 실행 동작 대신 소스 문자열만 검사한다"* 가 정확합니다.
F26b 테스트도 처음엔 `_fit_one`을 monkeypatch한 뒤 그 fake를 호출하는 껍데기였고,
`_run_fit_locked`을 지나지 않았습니다. 지금은 합성 `curves.parquet`으로
`run_fit`을 실제로 태워 `run_sig`가 설정 변화에 반응하는지 확인합니다
(`test_run_fit_records_run_signature_and_blocks_mixed_resume`,
`test_run_fit_signature_covers_restart_count`).

테스트 174 → 182.

---

## 12. 3차 리뷰 회답 (F36~F40)

2차 회답(`3c1109f`)에 대한 재검증에서 차단 8건. **전부 맞았습니다.**

| # | 지적 | 조치 |
|---|---|---|
| 1 | signature가 base config **내용**과 half-cell 캐시를 놓침 | **F36** — `sig_version`, `base_config_sha`, `halfcell_sha`(파일별), resolved `obj_cfg` 전체, 유도된 inventory 상수를 `run_spec`에 포함 |
| 2 | 단일이지만 다른 signature를 경고만 하고 통과 | **F36** — `run_sig` 열 없음 / null 행 존재 / 서명 2종 이상 / 현재 실행과 불일치 — **네 경우 모두 예외**로 죽인다 |
| 3 | 배너가 `run_sig` 열 존재만 검사 | **F38** — `src.io.validate_provenance()` 신설. manifest 존재·`config_hash`·clean worktree·입력 digest 완전성·`run_signature` 기록·행별 서명 non-null·단일 서명·manifest 일치·restart `source` 존재 **9개 검사**. 전부 통과해야 배너가 사라짐 |
| 4 | `비교가능`이 조건 집합 차이를 놓침 | **F40** — 공통 `cond_id` ∩ 동일 restart 수의 **paired subset**을 만들어 `paired` 블록으로 별도 집계. 목적함수별 제외율도 기록 |
| 5 | `PE-NE 상쇄`가 핵심 결론에 잔존 | **F33b** — 이름을 `raw PE/NE 오차 반대부호 비율 — 물리적 상쇄로 해석 불가`로 변경 |
| 6 | "34p에 유리하므로 보수적" 재단정 | **F39** — 삭제. "optimizer protocol이 다르다"는 사실만 적고 **어느 쪽이 유리한지도 단정하지 않는다**. 비볼록 문제에서 특정 seed가 항상 더 좋은 basin으로 데려간다는 보장이 없다 |
| 7 | untracked 전부 제외 → false clean | **F37** — `src/`·`tools/`·`configs/`·`scripts/` 아래의 `.py/.yaml/.json/.sh/.csv` untracked만 **dirty로 센다**. 그 밖은 개수·목록만 정보로 남김 |
| 8 | 문서 커밋 표기·앞 임계표 설명 불일치 | 상단에 1·2·3차 SHA를 각각 표기. 앞 임계표에 두 정의를 명시 |

### 판단 하나 — 실행을 죽이지 않았습니다

리뷰는 *"여섯 항목을 고치기 전에는 장시간 재실행을 시작하지 않는 것이 안전하다"*
고 권고했지만, halfcell_v2 실행(17:42 시작)을 그대로 뒀습니다. 근거는 셋입니다.

1. **위 8건 중 fits 숫자를 바꾸는 것이 하나도 없습니다.** signature 값, 병합 검사,
   보고서 문구, scoring 집계만 바뀝니다. 같은 코드로 다시 돌려도 `fits.parquet`의
   수치는 동일합니다.
2. **provenance 기록 자체는 이미 완전합니다.** F30이 manifest의 `input_sha256`에
   curves·base config·half-cell 캐시 digest를 넣습니다. 좁은 것은 resume
   signature뿐입니다.
3. **그 좁음이 만드는 위험은 F36이 닫습니다.** 고친 코드로 halfcell_v2에 resume하면
   서명이 달라 **즉시 실패**합니다. 즉 혼합이 원천 차단됩니다.

이 판단이 틀렸다면 halfcell_v2를 폐기하고 재실행하면 됩니다. 다만 그 경우에도
잃는 것은 5시간의 CPU 시간이지 결론이 아닙니다.

### 아직 못 한 것

- **F31의 `paired` 블록이 실제로 몇 조건 남는지**는 새 artifact가 나와야 압니다.
  30조건 미만이면 `비교가능=false`가 되고, multi-start는 목적함수 간 비교에
  쓸 수 없습니다.
- **동일 seed·동일 restart budget·early-stop off paired 재실행**(리뷰 #10)은
  아직입니다. 그 전에는 결론 2를 "현재 pipeline에서 관측된 값"으로만 씁니다.
- Case 2(`grid_fine_v2`)도 F31/F36/F37을 갖추려면 재fit이 필요합니다. 모드 수치는
  안 바뀌고 multi-start 진단과 provenance만 복구됩니다.

테스트 182 → 184.
