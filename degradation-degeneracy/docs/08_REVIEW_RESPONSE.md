# 08. 적대적 교차리뷰 회답

> **리뷰 기준 커밋**: `1790a9cc`
> **1차 회답**: `cb23274` (F25~F30) / **2차 회답**: `3c1109f` (F31~F35) /
> **3차 회답**: `7557c33` (F36~F40) / **4차 회답**: `261ba00` (F42~F48) /
> **5차 회답**: `94433e0` (F49~F53) / **6차 회답**: 이 문서 §15 (F55~F62)
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

---

## 13. 4차 리뷰 회답 (F42~F48)

> **검증 대상**: `7557c33` / **회답 커밋**: `9b9d223d`
> **판정**: 8건 전부 타당. 전부 조치했습니다. 반박 없습니다.

### 가장 아픈 지적 — 리뷰가 제 테스트로 제 validator를 반증했습니다

발견 1이 정확합니다. `validate_provenance()`가 provenance의 **진위**가 아니라
필드의 형식적 자기일관성만 봤습니다. 그 증거로 리뷰가 **이 저장소의 fixture**를
들었습니다 — `_complete_artifact()`가 존재하지 않는 파일의 가짜 digest
(`aaaa1111`, `bbbb2222`)와 임의 서명(`sig000000001`)을 넣고 "provenance 검사를
실제로 통과하는 artifact"라고 부르고 있었고, 실제로 통과했습니다.
테스트 이름은 "forged signature 거부"인데 정작 자기일관적 위조를 통과시켰습니다.

강화한 validator를 붙이자 **그 fixture가 즉시 깨졌습니다.** 진짜 입력 파일을
만들고, 그 digest를 기록하고, `run_spec`을 실제로 해시해 서명을 만드는 형태로
다시 썼습니다.

### 항목별 조치

| # | 지적 | 조치 |
|---|---|---|
| 1 | F38이 가짜 digest·자기일관 위조를 통과 | **F43** — 입력 파일을 **다시 해시**해 대조, `run_spec`을 **다시 해시**해 `run_signature`와 대조, `restarts_json`을 **첫 행이 아니라 모든 행** 검사. 검사 항목 9 → 10 |
| 2 | manifest가 **종료 시점** git·입력을 기록 | **F42** — `manifest_start.yaml`에 시작 시점 git SHA·dirty·입력 digest를 먼저 기록. 종료 manifest에 `start_provenance`와 `git_commit_changed_during_run`을 병기 |
| 3 | paired가 restart **개수**만 일치 | **F44** — `restart_indices`를 보존하고 **index 집합 일치**를 요구. `{1,2}` vs `{1,3}`은 이제 paired가 아님 |
| 4 | 전역 교집합이 33p↔34p 비교를 과도하게 축소 | **F44b** — `pairwise` 블록을 **목적함수 쌍마다** 생성. 전역 값에는 `_주의_전역교집합`을 붙여 쌍대 비교에 쓰지 못하게 함 |
| 5 | half-cell 캐시를 CWD에서 glob | **F45** — `halfcell_cache_path()` 신설. 서명·manifest가 `get_halfcell_reference()`와 **같은 규칙으로 고른 경로 하나**를 씀 |
| 6 | `PE-NE 상쇄` 명칭 잔존 | **F46** — 22p 근방 문장·표 헤더·`compare_objectives` 헤더까지 전부 `raw 반대부호`로. `rg 'PE-NE 상쇄' tools/*.py src/*.py` = 0 |
| 7 | F37 확장자 allowlist | **F47** — allowlist 제거. critical 디렉터리 아래는 전부 dirty(`__pycache__`·`.pyc`만 제외). `src/new.py`·`configs/new.yaml`·`src/data.toml`·`tools/x.ini`·`scripts/y.cfg` positive test 5종 추가 |
| 8 | 문서 3차 SHA 미표기 | **F48** — 상단에 `7557c33` 명시 |

테스트 **185 → 189**.

### `halfcell_v2` 판정 — 6개 조건 중 1번이 artifact 안에서 닫혔습니다

강화된 validator로 `results/halfcell_v2`를 다시 검사했습니다. **10개 전부 통과**
(재해시 포함):

```
manifest_존재 · config_hash · clean_worktree · 입력_digest_재해시 ·
run_signature_기록 · run_signature_재계산 · 행별_서명 · 단일_서명 ·
manifest와_일치 · restart_출처   →  ok: true
```

시작 SHA(조건 1)는 **artifact 내부 증거로 성립합니다.**

```
manifest.git_commit = 3c1109f5968f...     ← 종료 시점(20:22)에 기록됨
restart_출처 통과 → restarts_json 에 source 존재 → 코드 ≥ 3c1109f (F31)
7557c33 은 실행 중 push 됐고 3c1109f 의 자식
∴ HEAD 가 움직였다면 종료 기록이 7557c33 이어야 하는데 3c1109f 다
∴ 실행 내내 HEAD = 3c1109f
```

즉 "종료 시점 SHA를 실행 SHA처럼 쓰는" 문제가 이 실행에서는 발생하지 않았음이
**두 방향에서** 확인됩니다(코드 하한 ≥ 3c1109f, 종료 상한 = 3c1109f).
다만 지적하신 구조적 결함은 그대로 유효하므로 F42로 고쳤고, 앞으로의 실행은
`manifest_start.yaml`로 직접 증명됩니다.

`input_sha256`에 실제 사용 파일 3개가 기록돼 있고 전부 재해시 일치했습니다:
`results/grid_fine_v2/curves.parquet`, `configs/base.yaml`,
`.cache/halfcell/a8e262f7d6aa4beb_ocp.json`.

**따라서 `halfcell_v2`는 폐기하지 않고 인용 가능 상태로 승격합니다.**
계산을 살린 판단에 동의해 주신 부분에 대한 근거도 이것으로 채웠습니다.

### 새 실측 결과 — F26/F26b가 end-to-end로 검증됐습니다

3차 회답에서 "기존 artifact에 사후 적용한 값이지 새 실행 경로를 검증한 것이
아니다"라고 지적하신 부분입니다. 재실행 결과가 사후 적용치와 일치했습니다
(공통 1,476조건, grid 기준 복원가능군).

| objective | 사후 적용 예상 | 재실행 실측 |
|---|---:|---:|
| pOCV only | 59.5% | **59%** |
| 33p | 6.6% | **7%** |
| 34p | 10.0% | **10%** |
| dQ/dV only | 99.8% | **100%** |

Case 1 vs Case 2 (각 칸 = halfcell / grid):

| objective | degeneracy | 바이어스 보정 | 평균 \|err\| |
|---|---|---|---|
| 33p | 7% / 62% | 6% / 15% | 1.4%p / 2.5%p |
| 34p | 10% / 63% | 5% / 24% | 1.4%p / 2.4%p |

⚠ 자기정정: 전체 3,069조건에서는 34p가 33p보다 나아 보였으나(보정 15.1% vs
31.6%), 공통 1,476조건에서는 raw가 33p 우세(7% vs 10%), 보정이 34p 근소 우세
(6% vs 5%)로 **raw와 보정의 방향이 다릅니다.** 이 표로는 어느 쪽이 낫다고
말할 수 없고, "기준 곡선이 목적함수의 우열까지 뒤집는다"는 제 추측도 지지되지
않습니다. (★ 2026-08-20 정정 — 여기서 두 목적함수를 동등하다고 부른 문장을
지웁니다. 방향이 갈린다는 관측은 동등성의 근거가 아니고, 동등성을 주장하려면
사전 equivalence margin 이 필요합니다 — 21차 리뷰 발견 2, 철회[WARM_TIE] 와
같은 오용입니다.)

### F40/F44의 실제 paired 수 (3차 리뷰의 미확인 항목)

`halfcell_v2`에서 나온 값입니다.

```
n_common_conditions   1242
n_paired_conditions   1242      (전역, F44 index 일치 적용 전 수치)
목적함수별 조건 수      dqdv_only 3008 · pocv 1667 · pocv_dvdq 2298 · 34p 2857
제외율                 25.5% ~ 58.7%
```

여기서 **제가 먼저 문제를 하나 발견해 F41로 기록했습니다.** paired subset은
무작위 표본이 아닙니다 — adaptive 조기 종료로 restart 2에서 멈춘 조건은 무작위
restart가 1개뿐이라 탈락하므로, 남는 것은 **네 목적함수 모두가 끝까지 간 조건**
= 모두에게 어려웠던 조건입니다. **결과(최적화 난이도)로 선택된 집합**이라
격자 전체로 일반화할 수 없습니다. 제외율이 목적함수마다 두 배 넘게 차이나는
것이 그 증거이고, `_선택편향` 필드로 요약에 박고 테스트로 고정했습니다.

flat_valley는 1.6~3.5%로 넷이 사실상 같습니다. 다만 34p의 multimodal이 95.1%라
**flat valley가 있어도 관측되지 않는** 상태이므로, 34p의 낮은 flat_valley를
"degeneracy가 적다"로 읽으면 안 됩니다(기존 경고 유지).

### 남은 것

- **Case 2 재fit 진행 중** (`results/grid_fine_v3`). 이게 끝나야 `RESULTS.md`의
  인용 금지 배너가 사라집니다. 현재 배너는 `grid_fine_v2`가 F25 이전 artifact라
  정상적으로 유지되고 있습니다.
- **동일 seed·동일 restart budget·early-stop off paired 재실행**은 아직입니다.
  그 전까지 결론 2는 "현재 비대칭 pipeline에서 관측된 값"으로만 씁니다 —
  이 제한은 그대로 유효합니다.
- 결론 1은 철회 상태 유지, 결론 3은 pipeline 수준 표현 유지입니다.

---

## 14. 5차 리뷰 회답 (F49~F53)

> **검증 대상**: `261ba004` (코드 `9b9d223d`) / **회답 커밋**: 아래 §14 끝 참조
> **판정**: 8건 전부 타당. 전부 조치했습니다. **그리고 제 논증 하나가 반박됐습니다.**

### 먼저 — 제가 틀린 것을 철회합니다

4차 회답 §13에서 `halfcell_v2`의 시작 SHA를 이렇게 논증했습니다.

> "`7557c33`을 실행 중 push했으니, HEAD가 움직였다면 종료 기록이 `7557c33`이어야
> 한다. `3c1109f`로 남았으니 실행 내내 HEAD가 거기 있었다."

**틀렸습니다.** 지적하신 대로 **push는 실행 worktree의 HEAD를 움직이지 않습니다.**
HEAD는 그 worktree에서 pull/checkout해야 움직이고, 그건 artifact 밖의 사실입니다.
따라서 이 논증은 artifact-internal proof가 아닙니다. `restarts_json.source` 역시
"F31 이후 계통"이라는 정황일 뿐, cherry-pick·dirty source·사후 변환을 구별하지
못한다는 지적도 맞습니다.

**`halfcell_v2`의 "인용 가능 승격"을 철회하고 quarantine으로 되돌립니다.**
F49~F53을 갖춘 clean SHA에서 fresh output으로 재실행합니다(진행 중).

### 항목별 조치

| # | 지적 | 조치 |
|---|---|---|
| 1 | 다른 코드의 resume 결과가 한 `run_sig`로 섞이고 validator도 통과 | **F49** — `git_commit`·`git_dirty`·`source_digest`(src/tools/configs 전체 내용 해시)를 `run_spec`에 넣고 `sig_version=3`. 코드가 바뀌면 서명이 바뀌므로 resume이 즉시 실패 |
| 2 | F43이 필수 입력·spec schema를 정의하지 않음 | **F50** — reference별 필수 입력(curves·base config·halfcell 캐시), `run_spec` 필수 키 11종, 시작/종료 일치, 실행 중 코드 불변을 검사 |
| 2 | `.dropna()`로 **전부 null이어도 통과**, `rs[0]`만 검사 | **F50** — 모든 행·모든 원소가 `p·J·i·source`를 갖는지 확인. 지적하신 두 반례를 테스트로 고정 |
| 3 | start manifest가 self-fit보다 늦고 resume 시 덮어씀 | **F51** — 함수 맨 앞(curves 로드·inventory·half-cell 캐시·pristine `p_ini` fitting **이전**)으로 이동. `attempts/manifest_start_<id>.yaml`로 시도별 보존, 대표 파일은 최초 것만 |
| 4 | 시작 SHA 추론은 증명이 아니고 artifact도 미공개 | **인정** — 위 철회. artifact는 재실행 후 `artifacts/`에 커밋 |
| 5 | 배너가 비교에 쓰인 half-cell artifact를 검사하지 않음 | **F52** — `compare_cases.py`가 양쪽 provenance를 검증하고 digest를 `case_comparison.yaml`에 봉인. **F52b** — 배너 판정에 비교 입력을 합산하고, 표 위에 artifact별 판정을 표시 |
| 6 | 1,242는 F44 적용 **전** 수치 | **인정** — 재실행 후 `pairwise['pocv_dvdq__vs__pocv_dvdq_dqdv']`로 제출 |
| 7 | 커밋된 RESULTS는 수정 전 generator 산출물 | **인정** — 재실행 후 새 generator로 재생성 |
| 8 | Windows `os.kill`이 `OSError [WinError 87]` | **F53** — WinError 87만 "죽음", 나머지는 안전하게 "살아 있음"으로 |

테스트 **189 → 195**.

### 발견 1이 가장 컸습니다

`run_sig`에 코드 identity가 없다는 지적, 그리고 3조건 반례로 직접 재현해 주신 것
(OLD_CODE 행 + NEW_CODE 행이 같은 `79f2e9c798ee`로 병합되고 `ok=True`)이 정확합니다.
제가 F32/F36에서 "설정"만 넣고 "코드"를 빼놨습니다. 서명의 목적이 *"이 행들이 같은
조건에서 나왔는가"* 인데, 코드가 조건의 일부라는 걸 두 라운드 동안 놓쳤습니다.

`source_digest()`는 git commit이 아니라 **파일 내용을 직접 해시**합니다. commit만
넣으면 dirty 실행을 못 잡기 때문입니다.

### 발견 2의 두 구멍은 제 완료 주장과 정면으로 어긋났습니다

§12에서 "`restarts_json`을 **첫 행이 아니라 모든 행** 검사한다"고 적었는데,
`.dropna()`가 앞에 있어서 **전부 null이면 검사 대상이 0행**이었습니다. 그리고
각 배열에서는 여전히 `rs[0]`만 봤습니다. 둘 다 제 문장이 구현보다 넓었습니다.

### 남은 것

- **재실행 진행 중**: `halfcell_v3` → `grid_fine_v3` → sweep (약 10시간).
  clean worktree, fresh output, resume 미사용으로 시작했습니다.
- 끝나면 `artifacts/`에 커밋해 외부에서 재검산 가능하게 하겠습니다(발견 4).
- **동일 seed·동일 restart budget·early-stop off paired 재실행**은 여전히 미실시입니다.
  그 전까지 결론 2는 "현재 비대칭 pipeline에서 관측된 값"으로만 씁니다.
- 결론 1 철회 유지, 결론 3은 pipeline 수준 표현 유지이며 **정량값은 재실행 결과가
  provenance를 통과할 때까지 인용 보류**입니다.

---

## 15. 6차 리뷰 회답 (F55~F62)

> **리뷰 기준 커밋**: `94433e0b` / **회답 커밋**: `ff0ed7bb` + 이 문서
> **결과**: 7건 + 추가 1건, **전부 유효**했습니다. 반박한 것은 없습니다.

### 이번 라운드의 성격 — 검증기가 자기 테스트에 속았습니다

가장 아픈 지적은 방법 자체였습니다. 리뷰어가 **이 저장소의 테스트 fixture
(`_complete_artifact`)를 그대로 써서** `validate_provenance` 를 통과시켰습니다.
제가 "위조를 잡는다"고 세 라운드에 걸쳐 강화한 검증기가, 정작 **기록끼리
일관되기만 하면 통과**하는 상태였다는 뜻입니다.

원인은 하나로 모입니다. 검증 대상이 **디스크의 실물이 아니라 manifest 안의
필드**였습니다. manifest는 실행이 스스로 쓴 것이므로, 그것끼리 맞춰보는 것은
자기증명입니다. 이번 수정의 방향은 전부 "**밖에 있는 것과 대조하라**"입니다.

### 항목별 조치

| # | 지적 | 조치 |
|---|---|---|
| 1 | 같은 커밋·같은 입력이라도 라이브러리 버전이 다르면 다른 답이 나오는데 서명에 없다 | **F55** — `env_fingerprint()`. python/platform/machine + numpy·scipy·pandas·joblib·pyarrow·pybamm·matplotlib·yaml 버전을 `run_spec["env"]` 와 시작 provenance에 기록. 환경이 다르면 서명이 갈린다 |
| 2 | 입력을 시작·종료에 따로 해시해 그 사이 교체를 못 잡는다 | **F56** — `seal_inputs()` 로 시작 시점에 한 번만 봉인하고 `run_spec`·`base_manifest` 가 그 map을 재사용. 종료 시 재해시해 `input_sha256_at_end` / `inputs_changed_during_run` 기록. 검증기에 `입력봉인_교차일치`(시작 봉인 = run_spec = 종료 = 현재 파일, 네 곳) 추가 |
| 3 | 검증기가 manifest 안의 nested 사본만 보고 디스크의 start/attempt 파일을 안 읽는다 | **F57** — `manifest_start.yaml` 과 `attempts/manifest_start_<attempt_id>.yaml` 을 디스크에서 직접 읽어 대조 (`start_파일_존재`·`attempt_파일_존재`·`attempt_파일_일치`·`start_파일_일치`) |
| 4 | half-cell 캐시를 읽은 **뒤에** 해시해서, 읽는 순간과 해시하는 순간 사이가 비어 있다 | **F58** — 캐시 경로를 `get_halfcell_reference()` **호출 전에** 계산해 봉인. 경로나 digest가 바뀌면 예외. `reference=="halfcell"` 이면 `halfcell_sha`·`halfcell_cache` 가 `run_spec` 필수 키. `sig_version` 4로 올리고 **값 자체를** 검사 |
| 5 | `compare` 가 임의 parquet을 채점하면서 검증은 `run_dir/fits.parquet` 에 한다 | **F59** — `validate_provenance(..., fits_path=)` + `채점파일_정본` 검사. 파일 인자 하나로 degeneracy를 94.4% → 0% 로 바꾸고도 통과하던 경로를 막음 |
| 6 | 배너가 `case_comparison.yaml` 안의 기록만 믿는다 | **F60** — `make_results` 가 비교 산출물 두 개를 **보고서 생성 시점에 다시** 검증하고 `fits_sha256` 을 재계산. tag 집합이 `{grid, halfcell}` 이고 `provenance_ok is True` 일 때만 case 절을 낸다 |
| 7 | restart 원소가 키만 있고 값이 전부 null이어도 통과 | **F61** — `_restart_ok()` 로 원소마다 `p`(길이 4 유한 실수)·`J`(유한 실수)·`i`(비음 정수)·`source`(enum)를 검사. 주신 반례 3종을 테스트로 고정 |
| 추가 | **보관된 artifact를 clone 한 쪽에서는 검증할 수 없다** | **F62** — 아래 별도 |

### F62 — 검증기를 강화하는 동안 보관 방식은 그대로였습니다

이게 이번 라운드에서 제일 부끄러운 항목입니다.

`archive_results.sh` 초판의 기준은 "재생성 비용"이었습니다. 그래서
`curves.parquet` 을 "재생성 5~8분"이라고 버렸습니다. 그런데 F56 이후
검증기는 봉인된 입력을 **다시 해시**합니다. 재생성한 curves는 바이트가 달라
digest가 맞지 않습니다 — **재생성으로 대체할 수 없습니다.** 같은 이유로
`manifest_start.yaml` 과 `attempts/` 도 빠져 있었고(F57이 디스크에서 읽습니다),
half-cell 캐시는 `.cache/` 가 gitignore라 저장소에 아예 없었습니다.

정리하면, **인용 가능성을 판정하는 장치는 계속 조였는데 그 판정에 필요한 재료는
저장소에 남기지 않고 있었습니다.**

조치:

- `tools/archive_bundle.py` 신설 — `bundle` / `check` / `restore`
  - `bundle`: 검증 필수 파일 + `run_dir` 밖의 봉인 입력을 `inputs/` 에 동봉하고
    원래 경로를 `restore_map.yaml` 에 기록
  - `check`: 묶음이 검증에 필요한 파일을 다 가졌는지 (해시가 아니라 **존재**)
  - `restore`: 원래 경로로 되돌린다. 묶음은 보관 형태이고 경로가 다르므로,
    **검증은 복원 후에** 한다
- `archive_results.sh` 가 보관 시점에 원본 실행을 검증해 `provenance.json` 으로
  같이 남기고, 묶음이 불완전하면 "검증 불가"로 표시
- `artifacts/README.md` — 지금 들어 있는 세 묶음(`grid_fine_v1`·`grid_fine_v2`·
  `halfcell_v1`)이 **전부 검증 불가**임을 명시. 실행 자체가 F26/F51/F58 이전이고,
  묶는 방식도 옛 기준이었습니다. 이력으로만 남깁니다

테스트 **195 → 205**.

### 재실행 전략을 바꿉니다

여섯 라운드 연속으로 유효한 결함이 나왔고, 그때마다 약 10시간의 재실행이
날아갔습니다. 이번 수정으로 `run_spec` 필수 키가 또 늘어(`env`·`sealed_inputs`·
`halfcell_sha`) **지금 돌던 `halfcell_v3` 산출물은 새 검증기를 통과하지 못합니다.**
중단했습니다.

그래서 순서를 바꿉니다.

1. 코드를 먼저 수렴시킨다 (이 커밋)
2. **"이제 돌려도 된다"는 확인을 리뷰에서 받는다** ← 지금 여기
3. 그 다음에 clean worktree · fresh output 으로 `halfcell_v3` → `grid_fine_v3`
   → sweep 을 한 번에 돌린다
4. `archive_results.sh` 로 묶고, **복원 후 `validate_provenance` 통과를 확인한 뒤**
   `artifacts/` 에 커밋한다
5. `docs/RESULTS.md` 상단의 인용 금지 배너가 사라지는지 확인한다

배너가 사라지기 전까지 결론 1은 철회 상태, 결론 2는 "현재 비대칭 pipeline에서
관측된 값", 결론 3은 pipeline 수준 표현이며 **정량값은 전부 인용 보류**입니다.

### 아직 안 한 것

- **동일 seed · 동일 restart budget · early-stop off 인 paired 재실행.**
  여섯 라운드째 미실시입니다. 이게 없으면 목적함수의 내재적 성능을 말할 수 없습니다
- `pairwise` 기반 1,242 재산출, 새 generator로 `RESULTS.md` 재생성 — 3번 이후

---

## 16. 14차 게이트 리뷰 회답 (2026-08-11, 발견 1~8)

리뷰 대상 커밋 `393ac3db`. scope: 과학적 타당성 / 수치 재현성 / 실행 일관성
(보안 제외). 전 발견을 RED-first 로 닫았다 — 수정 전 반례가 실제로 통과함을
실측(또는 실패 테스트로 재현)한 뒤 고쳤다. 좌표·테스트 이름은
`docs/GATE14_WORKING_STATE.md` §0 의 표가 정본이다.

| # | 발견 | 대응 |
|---|---|---|
| 1 | 같은 truth family(lli·lam_pe·lam_ne·유형)의 noise 멤버가 다른 clean truth 여도 validator ok=True (반례 실측: q 4000 vs 2000, offset 4.2 vs 3.2 V) | `_verify_noise_families` 신설 — family 마다 서명된 noise 집합 정확 1회씩, observed/failed 분할 금지, q_mah ≤1e-6 mAh, v_pe/v_ne/v_full pointwise ≤1e-10 V. 기대 집합은 하드코딩이 아니라 **서명된 spec.noise** (grid_run_spec 에 신규 서명, `grid_sig_version` 4→5 필수화) |
| 2 | `source_digest` 가 OS 경로 구분자·CRLF 로 갈리고(4fa3e2af/7ac22c10/808f19ea) RUN_SCOPE 6개 중 3개만 봄 | 경로 키·정렬을 POSIX 정규형으로(`_digest_path_key`), 범위를 `scripts/`·`run.sh`·`requirements*.txt` 까지 확대. `.as_posix()` 는 Linux digest 불변, 범위 확대는 digest 변경(계획된 `--force` 재생성으로 흡수). CRLF 0개 양성 테스트 추가 |
| 3 | sweep 을 같은 27조건으로 줄이고 `n_conditions` 맞춘 뒤 digest 삭제 → "일치" | `condition_ids_sha256` 누락/빈값 즉시 fail, 양 끝점 digest == 서명 digest, `끝점_서명digest_일치` 를 최상위 verdict 에 포함 |
| 4 | `build_weight_objectives([0, 0.001])` 이 `wdqdv_0.00` 하나로 붕괴, w=0 seed 조용히 삭제 | 값↔이름 1:1 강제 — 충돌·중복·비유한·음수 즉시 ValueError |
| 5 | guards 검사가 아무 키나 허용, bool 통과, 오타 키는 replay 에서 조용히 기본값 대체 | `canonical_guards()` 단일 출처 (`GUARD_DEFAULTS` + 범위 0≤mode<1, 0<por≤1, 0<vf<1). producer 는 채워서 서명, validator 는 정확 3-key 요구, `build_overrides` 도 동일 정규화 |
| 6 | 재현 명령이 fit 산출물 위에 곡선을 만들고 자기 자신을 fit 함; clean fit 인데 `--clean` 없음 | grid `--out` = manifest.input(producer), fit `--in` producer `--out` in_dir, `v_col=="v_full"` → `--clean`. 결론 2 인용 정본 `docs/RESULTS_PAIRED_FIXED5.md` 명시 |
| 7 | archive 승격 첫 이동 실패 시 candidate 가 기존 묶음 안으로 중첩된 채 exit 0 | 첫 `mv` 검사 — 실패 시 후보 제거 + `n_bad` 계상 (fake mv 주입 회귀 테스트) |
| 8 | `source_commit` 이 기록 시점 manifest 최상위 commit; "다음 commit" 문구 오류 | 계산 **시작** 커밋으로 (fit: `run_spec.git_commit`→`start_provenance`, grid: `curves_manifest_start.yaml`). 문구를 실제 단일 commit 워크플로에 맞게 수정 |

검증: `python -m pytest tests -q` → **294 passed** (신규 12).
`grid_sig_version` 5 필수화로 v4 이하 산출물은 인용 불가로 강등된다 —
grid v4 재생성(GO 이후)이 전제다.

---

## 17. 14차 2차 리뷰 회답 (2026-08-12, 대상 `0cd1999` → 수정 `3bb6541`)

2차 리뷰 판정: pre-grid 차단점 1건(fully-failed family noise 완전성) + 같은
커밋 권고 3건 + 계산 후 가능 2건. 차단점과 권고 3건, portability 1건을 닫았다.

| # | 발견 | 심각도 | 대응 |
|---|---|---|---|
| 1 | fully-failed family 의 noise 집합을 검사하지 않는다 — failed 를 noise 없는 family `set` 으로 축약해, noise {0, 0.001} 만 failed 이고 0.005 는 의도 집합에도 없는 family 가 통과 (실측 `ok=True, fail=[]`) | 숫자가 바뀜 | `_verify_noise_families` 에서 failed 를 `family → [noise…]` multiset 으로 모으고, **fully-failed family 도 서명 noise 집합과 exact equality** 요구 (`실패_noise_family_완전성`). 교차 family 는 기존 `관측_noise_family_분할` 이 계속 실패시키고 이중 계상하지 않는다. 자동 강등 없음 (리뷰 Q1 답변대로 — 성공 곡선을 사후에 버리면 모집단이 바뀐다) |
| 3 | `w_grid` 가 이름과 exact round-trip 하지 않아도 통과 (`[0.001]`→`wdqdv_0.00`, `-0.0`→`wdqdv_-0.00`) | 숫자가 바뀜 (custom grid 한정) | 충돌 검사 뒤에 `float(obj_name(w).split("_")[-1]) == w` 요구, signed zero 를 `+0.0` 으로 정규화, 빈 격자 거부. 근거: `sweep_summary:163` 이 이름 suffix 를 되읽는다 |
| 4 | 재현 블록이 보고서 전체를 재생성하지 못한다 (wsweep·half-cell·`--compare` 없음) | 서술만 바뀜 | 리뷰 선택지 2 채택 — 렌더된 절과 **같은 조건**으로 `--mode wsweep`(서명된 sweep run_spec 의 w_grid·stride·restart·adaptive·warm), half-cell 준비 `--force --verify`, `--reference halfcell` fit·score, `report --compare <halfcell>` 까지 출력. 경로는 `case_comparison.provenance.halfcell.run_dir` 에서 |
| 5 | digest 와 dirty scope 의 requirements matcher 불일치 | 서술만 바뀜 | `in_run_scope()` 신설 — `RUN_SCOPE` 를 `requirements*.txt` glob 으로 통일하고 tracked/untracked 판정 모두 이 함수를 쓴다. root 의 untracked `run.sh`·`requirements*.txt` 도 critical |
| 6 | archive shell 회귀가 Windows native pytest 에서 실행 불가 | 사소 | `shutil.which("bash")` 없으면 명시 `pytest.skip` (조용한 통과가 아니라 미검증 표시) |
| 2 | 기존 Windows worktree 의 잔존 CRLF 26개 | 서술만 바뀜 | 코드 수정 없음 — `.gitattributes` 는 기존 worktree bytes 를 소급하지 않는다. 교차 OS code-identity 검증은 **attributes 적용 후 fresh clone** 에서만 유효하다고 기록 (아래 §신뢰 경계) |

계산 후로 미룬 것 (리뷰 동의 항목): paired 정본 문구를 실제 paired 보고서
생성·provenance gate 와 연결(2차 발견 7), grid producer `source_commit` fallback
을 `null/legacy` 로 엄격화(1차 Q5) — 둘 다 fresh v5 계획에서 비활성이다.

검증 (`3bb6541c33653e76a0d62f62f6c818f3e9cb0fa8`, clean):
`python -m pytest tests -q` → **299 passed** · `./scripts/smoke_e2e.sh` → 전 구간 통과 ·
`source_digest()` = `5e504288a5ebf66b` (LF canonical) ·
`git ls-files --eol` RUN_SCOPE 전 파일 `w/lf`.

---

## 18. 14차 3차 리뷰 회답 (2026-08-12, 대상 `010aa0b4` → 수정 `9e6ceb1`)

3차 리뷰 판정: pre-grid 차단점 2건(sweep 재현 명령) + 서술 2건. 전건 수정했다.

| # | 발견 | 심각도 | 대응 |
|---|---|---|---|
| 1 | sweep 재현 명령의 출력이 `<main-fit>` 자체 — `run_weight_sweep` 은 명시된 `--out` 을 그대로 쓰고 생략 시에만 `<in>/wsweep` 을 기본값으로 한다 | 실행 실패 | `--out {in_dir}/wsweep` 으로 수정. 정본 위치는 smoke(`$GFIT/wsweep`)와 동일 |
| 2 | 존재하지 않는 `--stride` 출력 (wrapper 는 `--w-stride`) | 실행 실패 | 옵션명 수정. **fixture 가 오류를 가리고 있었다** — `_wsweep_run` 의 `weight_sweep.yaml` 에 실제 producer 가 쓰는 `stride` 키가 없어 그 줄 자체가 생성되지 않았다. fixture 를 실물에 맞춰 채웠다 |
| — | 회귀 | — | 재현 블록의 **모든 `./run.sh` 줄을 실제 wrapper 로 실행**해 `알 수 없는 인자` 가 없음을 확인하고(`--help` 로 파싱 직후 종료), sweep 줄의 정본 경로·옵션명을 고정 |
| 3 | 제외 규칙이 digest·dirty 간 비대칭 (`_SKIP` 은 `.pyc` 를 이름 중간에도 제외) | 서술만 바뀜 | `is_scope_excluded()` 신설 — 캐시 디렉터리는 **경로 성분**, 바이트코드는 **suffix** 로만 판정하고 양쪽이 공유 |
| 4 | half-cell 재현 명령이 nondefault protocol 을 복원하지 않음 | 서술만 바뀜 | `_fit_flags()` 로 fit 플래그 생성을 단일화하고 half-cell 기준 fit 에도 적용 (objective_order·n_restarts·clean·adaptive·warm_start) |

검증 (`9e6ceb1f220bfafc57481d867123cfb062ffd6c4`, clean):
`python -m pytest tests -q` → **302 passed** · `./scripts/smoke_e2e.sh` → 통과 ·
`source_digest()` = `3de0596446abf364` · RUN_SCOPE `w/lf` 아닌 파일 0건.

### 이번에 새로 **측정된** 운영 리스크 — strict smoke 의 간헐적 SIGABRT

smoke 를 반복 실행하다 발견했다. 실패 시 시그니처가 항상 같다:

```
   ✅ 격리 복원 검증[results/_smoke/halfcell_fit]: 통과
   ✅ 격리 복원 검증[results/_smoke/grid_fit]: 통과
   ✅ 격리 복원 검증[results/_smoke/grid_fit/wsweep]: 통과
terminate called without an active exception
./scripts/smoke_e2e.sh: line 430: <pid> Aborted   "$PY" - "$ISO" "$HFIT" "$GFIT" <<'PYEOF'
```

**검사 3건이 모두 `통과` 를 출력한 뒤** 인터프리터 종료 시점에 죽는다 — 검증
실패가 아니라 **모든 validator 판정이 끝난 뒤 발생하는 native interpreter
teardown flake** 다. **정확한 library 원인은 미확정이다.**

> **정정 (14차 4차 발견 2)**: 위 문단은 처음에 "PyBaMM/CasADi 를 import 한
> 프로세스"라고 적었으나 **틀렸다**. 이 validator 경로를 실측하면
> `pybamm_loaded=False`, `casadi_loaded=False`, `pyarrow_loaded=True` 다 —
> pandas/Parquet 의 native extension 은 쓰지만 PyBaMM·CasADi 를 직접 로드하지
> 않는다. PyArrow 를 원인으로 확정할 근거도 아직 없다. 원인 규명은 artifact 별
> validator·producer 재검·Parquet/fits seal 단계를 분리하고 core/backtrace 로
> 어느 native finalizer 가 죽는지 보는 후속 조사로 남긴다.

변경 전후 분리 측정 (각각 **새 worktree**, 캐시 상태 통제):

| 커밋 | smoke 실패 | 시그니처 |
|---|---|---|
| `010aa0b` (3차 리뷰 대상, 변경 전) | **1 / 7** | 동일 — 같은 line 430, 검사 통과 후 abort |
| `9e6ceb1` (HEAD) | 1 / 3 | 동일 |

즉 **이번 diff 가 만든 회귀가 아니다** (동일 라인·동일 시그니처가 변경 전
커밋에서도 재현). `validate_provenance` 단독 반복은 30/30 정상이라 검증 로직
자체는 무관하다.

미해결로 남긴다 — 판단이 필요하다. 후보 대응은 (a) 해당 validator heredoc 이
종료 코드 확정 후 `os._exit()` 로 teardown 을 건너뛰기, (b) 근본 원인(스레드
teardown) 규명. (a) 는 결정적이지만 **10시간 실행을 게이트하는 스크립트에서
크래시를 가리는** 변경이라 리뷰 판단 없이 넣지 않았다. 게이트 증거로는 clean
통과 실행을 쓰되, 이 flake 는 공개해 둔다.

---

## 19. 14차 4차 리뷰 회답 (2026-08-12, 대상 `36fdad2` → 수정 `3a5b8c5`)

4차 판정: 수치 pipeline 은 GO 수준, 남은 차단점은 strict smoke 의 **종료
비결정성** 하나. 리뷰가 지정한 6개 사전 조건을 전부 충족했다.

| # | 발견 | 대응 |
|---|---|---|
| 1 | 격리 복원 validator 가 판정 완료 뒤 간헐 SIGABRT → exact gate 가 non-deterministic | 리뷰 지정 형태 그대로: `rc` 를 **먼저 확정** → `stdout`·`stderr` flush (flush 실패도 `rc=1`) → `os._exit(rc)`. 적용 범위는 `scripts/smoke_e2e.sh` 의 **read-only validator subprocess 하나**. 이 프로세스는 연구 산출물을 쓰지 않고 격리 디렉터리 삭제는 shell 이 한다 → 판정·수치 불변, native finalization 만 생략. 검증 중 예외·실패는 여전히 nonzero |
| 2 | "PyBaMM/CasADi teardown" 원인 단정이 근거와 불일치 | **정정.** 실측 `pybamm_loaded=False`, `casadi_loaded=False`, `pyarrow_loaded=True`. 원장 문구를 "모든 validator 판정이 끝난 뒤 발생하는 native interpreter teardown flake, **정확한 library 원인은 미확정**"으로 낮췄다. PyArrow 단정도 하지 않는다. 근본 원인은 후속 조사(단계 분리 + core/backtrace) |
| 3 | exclusion helper 가 tracked dirty 에는 미적용 → "완전 공유" 서술이 과함 | 리뷰가 준 두 선택지 중 **현재 동작 유지 + 서술 축소**. 이 비대칭은 false-clean 이 아니라 **보수적 false-dirty** 이고, 저장소 규칙(validator 를 느슨하게 만들지 않는다)에 따라 완화하지 않는다. 대신 의도를 회귀 테스트로 **고정**했다 (`test_tracked_dirty_is_conservative_for_excluded_paths`) |
| 4 | 일부 signed nondefault 설정이 재현 명령에서 유실 | half-cell `--method` 를 서명값(`run_spec.halfcell_recipe.method`)에서 낸다. 아직 명령으로 내보내지 않는 축(sweep bounds/reference/tol·optimizer method, 비기본 `eps` Hessian)은 보고서가 **재현 범위 블록**으로 스스로 한정한다 |
| 5 | 신규 wrapper 회귀는 parser smoke 이지 end-to-end 가 아님 | 테스트 이름을 `..._wrapper_parser_smoke_and_canonical_paths` 로 바꾸고 docstring 에 범위를 명시. 종료 코드까지 단언하도록 강화 |

### 게이트 증거 (커밋 `3a5b8c5239711257d8801f2e17db63adb5d64406`, clean)

```
python -m pytest tests -q                → 304 passed          (신규 2)
strict smoke — 사전 선언 10회, 재시도 없음 → 10 / 10 통과
                                            terminate called 총 0회
source_digest()                          → d50295f980ccaa81    (새 canonical)
git ls-files --eol … | grep -cv "w/lf"   → 0
python -m src.baseline --config configs/grid_fine.yaml --force
   → ne_primary 36.64970365755636 / ne_secondary 3446.0841935664557
     pe 58439.873864492365   (기존 서명값과 일치)
python -m src.halfcell --config configs/base.yaml --method ocp --force --verify
   → 구조검사 true / 구조검사_실패 [] / 재생성_배열일치 true
```

10회는 **실행 전에 횟수를 고정**했고 실패분을 버리고 재시도하지 않았다
(셸 시간 제한 때문에 5+3+2 로 나눠 실행했으나 같은 커밋의 연속 10회다).

---

## 20. 14차 게이트 GO 후 본 실행 기록 (2026-08-12 ~ 13)

리뷰 5차에서 GO. 코드는 `c0f1daa0` / `source_digest d50295f980ccaa81` 로 동결한
채 계산·보고·보관을 끝냈다. 아래는 **실행 로그에서 그대로 옮긴 수치**다.

### 20.1 환경과 실행

| 항목 | 값 |
|---|---|
| 코드 | `c0f1daa0d92a7625c3602799c81db04b5e2e5783`, `source_digest d50295f980ccaa81` |
| 하드웨어 | Tesla V100-PCIE-32GB · 32코어 · RAM 125 GB |
| GPU 사용 | **없음** — PyBaMM DFN + composite phases 는 IDAKLU(CPU) 경로 |
| pre-flight | pytest 304 passed (35분) · strict smoke 통과 |
| baseline | ne_primary 36.64970365763882 / ne_secondary 3446.0841935406315 / pe 58439.87386449178 |
| half-cell | `구조검사 true` · `재생성_배열일치 true` |

| 단계 | 결과 | 소요 |
|---|---|---|
| grid | ok 3,069 / failed 924 (의도 3,993) | 1,931.6 s |
| main fit (grid 기준) | 12,276행 = 3,069 × 4목적함수 | 10,364.4 s |
| half-cell fit | 12,276행 | 9,332.3 s |
| paired fixed-5 (1차) | 6,138행 — **무효, 폐기** (20.3) | 7,046.6 s |
| paired fixed-5 (재실행) | 6,138행 = 3,069 × 2목적함수 | 6,924.5 s |
| wsweep · score · Hessian · 보고서 | — | 약 9 h |
| archive | 요청 4 · 검증 가능 4 · 불완전 0 · 합계 116 MB | — |

### 20.2 grid invariant (fitting 전, 리뷰 조건 4)

```
validator ok = True | fail = []
grid_sig_version = 5 | signed noise = [0.0, 0.001, 0.005]
effective_solver = IDAKLUSolver · pybamm 26.7.1.0 · pybammsolvers 0.9.0 · casadi 3.7.2
observed conditions = 3069 (3069 기대)
observed family     = 1023 (1023 기대), noise 집합 불일치 0
max Δq_mah = 0 mAh (≤1e-6)   max Δv = 0 V (≤1e-10)
n_failed_total = 924 (924 기대)
fully-failed family = 308 (308 기대), noise 불일치 0
=== INVARIANT PASS ===
```

family 내 편차가 허용오차가 아니라 **정확히 0** 이다 — 14차 발견 1 이 요구한
"noise 는 solve 이후에만 얹힌다"가 3,069조건 전수에서 성립했다.

### 20.3 실행 중 사고 1건 — 검증 장치가 처음으로 실제 사고를 잡았다

paired fit(20:29~22:30) **도중**, 같은 clone 에서 작업하던 다른 세션이
`claude/stoic-knuth-NObVQ`(DEM/MPM 계열)로 브랜치를 전환했다. 그 브랜치에는
`degradation-degeneracy/src/`·`configs/` 가 없어 tracked 파일이 통째로 사라졌다.
이미 import 된 모듈로 계산은 끝까지 돌았지만, 산출물의 코드 정체성은 깨졌다.

검출:

```
results/grid_curves_v4    src_changed=False git_changed=None
results/grid_fit_v4       src_changed=False git_changed=False
results/halfcell_fit_v4   src_changed=False git_changed=False
results/paired_fixed5_v4  src_changed=True  git_changed=True
results/paired_fixed5_v4  ok=False fail=['입력봉인_교차일치', '실행중_코드불변']
```

- `실행중_코드불변` = `src/` 소멸, `입력봉인_교차일치` = 종료 시점에 봉인 입력
  (`configs/base.yaml` 등)을 재해시할 수 없게 된 것.
- **`--resume` 으로 잇지 않았다.** run_sig 가 같아 기술적으로는 가능하지만 어느
  행이 코드가 사라진 상태에서 계산됐는지 증명할 수 없다. 처음부터 재실행했고
  재실행분은 `src_changed=False / git_changed=False / ok=True` 다.
- 무효본은 `results/_INVALID_paired_fixed5_v4_srcchanged` 로 보존(gitignore).
- 재발 방지: DEM/MPM 작업을 `git worktree add ~/dem-work` 로 분리했다.

F49(5차)부터 쌓아 온 코드 identity 봉인이 **가정된 위협이 아니라 실제 사고**를
잡은 첫 사례다. 이 장치가 없었다면 결론 2의 인용 정본이 조용히 통과했다.

### 20.4 결과 (`docs/RESULTS.md`, 복원가능군 5,904행 · tol 2%p)

| objective | degeneracy | (바이어스 보정) | 평균 \|err\| | raw 반대부호 |
|---|---|---|---|---|
| pOCV only | 78% | 67% | 4.7%p | 29% |
| pOCV + dV/dQ (33p) | 62% | 15% | 2.5%p | 68% |
| + dQ/dV (34p) | 63% | 25% | 2.4%p | 48% |
| dQ/dV only | 77% | 66% | 5.0%p | 22% |

> ### ⛔ 정정 (15차 리뷰, 2026-08-13) — 아래 원문에 오류가 있었다
>
> 15차 리뷰가 **자기모순**을 지적했다. 이 절은 목적함수 비교의 인용 정본을
> paired 보고서라고 적으면서, 결론 수치는 **비대칭 pipeline** 값(62% → 63%)을
> 실었다. 산출물에서 재확인한 정본 수치는 다음과 같다.
>
> | 모집단·pipeline | 33p | 34p | 차이 |
> |---|---:|---:|---:|
> | 비대칭 main (`grid_fit_v4`) | 0.621951 | 0.627371 | +0.54%p |
> | **공정 paired (`paired_fixed5_v4`, 정본)** | **0.619241** | **0.871951** | **+25.27%p** |
>
> 즉 공정 비교에서 34p 는 "사실상 변화 없음"이 아니라 **recovery failure 가
> 61.9% → 87.2% 로 크게 악화**했다. 다만 이를 "dQ/dV 의 정보량이 더 나쁘다"로
> 읽으면 안 된다 — paired 에서 34p 해의 multimodal 비율이 97% 라 optimizer 가
> 그 목적함수를 못 푸는 효과가 섞여 있다.
>
> (★ 여기 있던 "두 protocol 모두에서 개선 미관측" 이라는 포괄 문구는
> 21차 발견 2 로 철회했다 — 철회[WARM_NO_IMPROVE_ANY]. 방어 가능한 형태는
> 아래 재정정 블록의 endpoint 한정 서술이다.)
>
> ### ⛔ 재정정 (2026-08-20) — +25.27%p 는 `warm_start=False` protocol 값이다
>
> 위 유보("optimizer 가 못 푸는 효과가 섞여 있다")가 **옳았고, 그 optimizer
> 축이 무엇인지 이제 측정됐다 — warm-start 연쇄다.**
>
> `paired_fixed5_v4` 의 manifest 실측: `warm_start: False`, `adaptive: False`,
> `n_restarts: 5`. 같은 조건 집합(`grid_curves_v4`, 3,069조건, `bounds
> expanded`)에서 **warm 만 켜서** 다시 돌리고, 코드 축을 소거하기 위해
> **현재 digest 에서 warm 을 끈 대조**도 함께 돌렸다:
>
> | 다리 | digest | warm | 33p (`pocv_dvdq`) | 34p (`pocv_dvdq_dqdv`) | 차이 |
> |---|---|---|---:|---:|---:|
> | `paired_fixed5_v4` (정본) | `d50295f9` | False | 0.619241 | 0.871951 | +25.27%p |
> | `paired_fixed5_v4_nowarm_now` | `a72c0f3a` | False | 0.615854 | 0.873984 | +25.81%p |
> | `paired_fixed5_v4_warm` | `a72c0f3a` | **True** | **0.615854** | **0.628726** | **+1.29%p** |
>
> **두 축이 완전히 분리된다:**
>
> | 비교 | 다른 것 | 33p 변화 | 34p 변화 |
> |---|---|---:|---:|
> | 정본 → `nowarm_now` | **코드 + runtime drift** | −0.0034 | **+0.0020** |
> | `nowarm_now` → `warm` | **warm 만** (같은 digest·runtime) | **0.0000** | **−0.2453** |
>
> 같은 digest 에서 warm 만 바꾸면 **33p 는 소수점 6자리까지 동일**하고
> (연쇄 1번째라 warm 할 것이 없다 — 설계상 그래야 한다), 34p 만 움직인다.
> 따라서 **이 paired 격자에서 34p 의 362행·24.53%p 변화는 warm-start
> protocol 에 귀속할 수 있다.**
>
> 첫 줄은 warm 축이 아니라 **잡음 대조**다. 그리고 "코드만" 이라고 쓸 수
> 없다 — 정본 다리와 지금 사이에는 Python·OS·NumPy·SciPy 도 함께 바뀌었다
> (21차 리뷰 발견 5, 철회[WARM_SYSTEMATIC]). 그 합쳐진 drift 가 ±0.003 이고
> 34p 를 오히려 **위로** 민다(0.871951 → 0.873984)는 것이 여기서 쓸 수 있는
> 전부다. 두 번째 줄만 digest·runtime·조건집합·예산이 모두 같은 matched 짝이다.
>
> 부수 지표도 같다 — 34p 의 `mean_abs_err` 0.065336 → 0.023653 (2.8배),
> `degenerate_frac_corrected` 0.947832 → 0.243902 (3.9배).
>
> **무엇이 바뀌고 무엇이 안 바뀌는가**
>
> - **"개선 없음" 은 endpoint 를 명시해야만 방어된다.** 쓸 수 있는 형태는
>   **"사전 지정한 aggregate raw-degeneracy endpoint 에서는 34p 개선이
>   관측되지 않았다"** 까지다 (warm 에서도 34p 0.628726 > 33p 0.615854).
>   그 밖으로 넓히면 **틀린다** — 21차 리뷰 발견 2 가 반례 둘을 찾았다
>   (철회[WARM_NO_IMPROVE_ANY]):
>
>   | noise | 33p 실패 | warm 34p 실패 | 34p − 33p |
>   |---:|---:|---:|---:|
>   | 0 | 292/492 | 316/492 | +4.88%p (악화) |
>   | 0.001 | 304/492 | 308/492 | +0.81%p (악화) |
>   | **0.005** | **313/492** | **304/492** | **−1.83%p (개선)** |
>
>   metric 을 바꿔도 방향이 갈린다: aggregate `mean_abs_err` 는 33p 0.024220
>   vs 34p 0.023653 으로 **34p 가 낫다**. raw degeneracy(0.615854 → 0.628726)
>   와 corrected degeneracy(0.141599 → 0.243902)에서만 34p 가 나쁘다.
>   따라서 이 결론은 **metric · 모집단 · noise 층을 명시한 형태로만** 쓴다.
> - **"61.9% → 87.2% 로 크게 악화" 는 protocol 조건부다.** warm 을 켜면
>   61.6% → 62.9% (+1.29%p)다. 이 문장을 인용할 때는 반드시
>   `warm_start=False` 를 병기한다. **+1.29%p 를 "차이 없음" 으로 부르지는
>   않는다** — 동등성 주장에는 사전에 정한 equivalence margin 과 조건별
>   paired 전이표(`33p pass/fail × 34p pass/fail`, McNemar)가 필요한데 둘 다
>   없다. 파라미터 오차 판정선 2%p 를 실패율 동등성 margin 으로 재사용할 수
>   없다 (21차 리뷰 발견 2, 철회[WARM_TIE]).
> - **warm 은 다봉성을 없애지 않았다.** 목적함수 간 비교에 써야 하는
>   `multistart_random_only` 블록이 두 arm 에서 **완전히 동일**하다 — 34p
>   multimodal `0.969512`, flat_valley `0.008130` 이 양쪽 같다. 같은 결정론적
>   난수에서 나온 같은 4개 random restart 는 그대로 다봉이었다. (모든 restart
>   를 세는 `multistart` 블록의 nowarm 0.9614 / warm 0.9621 은 slot 0 을
>   포함하므로 이 판단에 쓰면 안 된다.)
>
>   ### ⛔ 재재정정 (2026-08-20, 22차 리뷰 발견 1) — 추가가 아니라 **교체**다
>
>   여기 있던 서술 — warm 이 결정론적 계산점을 하나 보태기만 했다는 것 — 은
>   **틀렸다** (철회[WARM_UNION]). `src/fitting.py` 의 restart 루프는 정확히
>   `n_restarts` 번 돌고 slot 0 이 `base_init` **또는** `warm` 이다:
>
>   ```python
>   n_max = max(1, n_restarts)
>   for k in range(n_max):
>       x0 = init if k == 0 else rng.uniform(lb, ub)
>       src = ("warm" if warm_init else "base_init") if k == 0 else "random"
>   ```
>
>   커밋된 투영의 `restart_sources` 가 그대로 보인다 (3,069조건 전부 동일):
>
>   | arm · 목적함수 | 후보 구성 | 총 후보 |
>   |---|---|---:|
>   | no-warm 33p | `base_init=1;random=4` | 5 |
>   | no-warm 34p | `base_init=1;random=4` | 5 |
>   | warm 33p | `base_init=1;random=4` | 5 |
>   | **warm 34p** | **`random=4;warm=1`** | **5** |
>
>   즉 warm arm 의 34p 에서 **`base_init` 이 사라졌다.** 이 대조가 잰 것은
>   "warm 후보를 하나 더 주면 어떻게 되는가" 가 아니라 **"slot 0 의 결정론적
>   후보가 `base_init` 이냐 `warm` 이냐"** 다. 계약 용어로 `legacy_slot_replace`
>   이고, `union` 도 `equal_start_count` 도 아니다.
>
>   무엇이 바뀌나: 34p 개선을 "warm 후보가 좋다" 로만 읽을 수 없다. **`base_init`
>   이 34p 에서 나쁜 후보였다**는 해석과 구별되지 않는다. 두 해석을 가르려면
>   `base` 를 유지한 채 warm 을 넣는 arm 이 따로 필요하다 (계약 §2.5).
>
>   ### 전이표 — aggregate 하나로 보고하면 안 된다 (22차 발견 4)
>
>   커밋된 투영에서 직접 센 값이다 (recoverable 1,476조건).
>
>   **(A) no-warm 34p → warm 34p** — slot 0 교체가 무엇을 바꿨나
>
>   | | warm pass | warm fail |
>   |---|---:|---:|
>   | **no-warm pass** | 182 | **4** |
>   | **no-warm fail** | **366** | 924 |
>
>   순변화는 362행이지만 실제로 상태가 바뀐 것은 **370행**이다. 반대 방향
>   (pass→fail)이 4건 있다는 사실은 aggregate 에 보이지 않는다.
>
>   **(B) warm arm 안에서 33p → 34p** — 이쪽이 결론 1 의 실제 모습이다
>
>   | | 34p pass | 34p fail |
>   |---|---:|---:|
>   | **33p pass** | 381 | **186** |
>   | **33p fail** | **167** | 742 |
>
>   aggregate 는 `909 → 928`, +19 failures 다. 그런데 조건별 불일치는
>   **353/1476 = 23.9%** 다. 두 목적함수는 "거의 같은 답" 을 내는 것이 아니라
>   **네 조건 중 하나에서 서로 다르게 판정**하면서 총량만 비슷한 것이다.
>
>   따라서 단계 3 의 primary endpoint 는 aggregate 차이 하나가 아니라
>   **조건별 paired transition table** 을 포함해야 한다. 다만 이 격자는 확률
>   표본이 아니라 결정론적 조건집합이므로 전이 건수는 **기술통계**다 —
>   McNemar p-value 나 모집단 확률로 옮기려면 조건 표집 모형과 독립 반복을
>   먼저 정의해야 한다 (22차 Q4).
>
>   그래서 "warm 이 더 좋은 basin 에 앉혔다" 는 **말할 수 없다** (21차 리뷰
>   발견 3, 철회[WARM_BETTER_VALLEY]). 그러려면 조건별 `J` 를 비교해서 warm
>   해가 실제로 **더 낮은 J** 인지, 아니면 J 는 비슷한데 합성 truth 에 더
>   가까운 다른 basin 일 뿐인지 갈라야 한다. 지금 있는 것은 truth error 뿐이고,
>   truth 로 optimizer protocol 을 고르면 모의 truth 를 이용한 선택 편향이
>   된다. F20 의 "초기값을 주면 다봉성이 사라진다" 도 이 표로 측정된 적이
>   **없다** — 오히려 반대 방향의 관측이다.
>
>   > ⚠ 같은 문구가 봉인 summary 의 `multistart._해석` 문자열에도 남아 있다.
>   > 그 문자열은 `src/` 가 생성하므로 고치면 `source_digest` 가 바뀐다 —
>   > 단계 3 코드 라운드에서 함께 고친다. 그때까지 그 필드는 인용하지 않는다.
>
> 진단 다리 (`recorded_only` — 인용 정본 아님): `results/paired_fixed5_v4_warm`,
> `results/paired_fixed5_v4_nowarm_now` (경위와 원자료는
> `docs/22p_gap/LEG_INVENTORY.md` §27~§31).
>
> **붕괴율 "0%" 도 틀렸다.** 정확한 값은 `gap_collapse_frac =
> 0.004081632653061225 = 1/245 (0.41%)` 이며, 정수 percent 렌더링이 0% 로
> 반올림한 것이다. 실제로 0건이었다면 우도비가 90.0 이 아니라 무한대여야 한다
> (`LR = (36/98) / (1/245) = 90.0`). 붕괴 1건은 `cond_id c2e8442aa1f3`,
> truth LAM_PE/NE = 0.16/0.08 (참 격차 8.0%p) → 복원 0.16367/0.161593
> (복원 격차 0.21%p) 다.
>
> **LR 90 은 조건부 값이다.** 같은 지표를 전체 생성성공 격자에서 재계산하면
> `n_wide = 604`, 붕괴 `10.60%`, **LR 3.69** 다 — 넓은 격차 붕괴 64건 중
> 63건(98.4%)이 recoverability 필터로 빠진다. 90 을 인용하려면 3.69 와 52%
> 선택 효과를 반드시 병기해야 한다.
>
> 아래 원문은 기록으로 남기되, **인용하지 말 것.**

- **결론 1**: dQ/dV 추가로 62% → 63%, 사실상 변화 없음. 모집단에 따라 방향이
  뒤집힌다(복원가능군 +0.5%p vs 전체 격자 −2.6%p). optimizer protocol 이 달라
  정보량 비교가 아니며, 인용 정본은 `docs/RESULTS_PAIRED_FIXED5.md` 다.
- **결론 2**: 참 격차 ≥6%p 조건이 "같다"로 붕괴하는 비율 **0%** (n=245),
  사건 우도비 90.0. 임계를 흔들면 2.5~113.7(중앙값 16.8)로 움직이는 국소
  봉우리라 단독 인용 불가 — 6차 리뷰의 철회 판단이 v4 에서도 유지된다.
- **결론 3**: 22p 근방 degeneracy 12%.
- **기준 곡선 효과**: 33p 에서 Case 1(half-cell) **7%** vs Case 2(grid) **62%**.
  목적함수를 바꾼 차이(62↔63%)와 자릿수가 다르다 — 결론 3(기준 곡선 > 목적함수)
  이 v4 에서 재현됐다.
- 격자의 **52%** 는 grid 기준에서 원리적으로 복원 불가.


### 20.5 보관과 외부 검증

archive 4/4 승격(116 MB), `artifacts/artifact_index.yaml` 의 `source_commit` 은
전부 `c0f1daa0`(계산 시작 커밋 — 14차 발견 8). **다른 clone 에서 실제로 확인**:

```
── grid_curves_v4    검증 가능: 필요한 파일이 모두 있고 digest가 일치한다
── grid_fit_v4       검증 가능: …
── halfcell_fit_v4   검증 가능: …
── paired_fixed5_v4  검증 가능: …
```

### 20.6 이번 실행에서 새로 드러난 결함 — 15차 게이트 대상

전부 **실측으로 확인**했고, digest 동결 때문에 **이번 라운드에서는 고치지 않았다**.

| # | 결함 | 근거 | 영향 |
|---|---|---|---|
| A | `run.sh --mode hessian` 이 **분리 배치에서 동작 불가**. `run_hessian` 이 `curves.parquet` 과 `fits.parquet` 을 같은 `--in` 에서 읽는데, 게이트가 요구한 producer/fit 분리(F70)에서는 한 디렉터리에 둘 다 없다 | `src/hessian.py:135`, 실행 시 `FileNotFoundError: results/grid_fit_v4/curves.parquet` | 문서화된 실행 순서가 그대로는 실패. 이번엔 봉인 스냅샷(`_inputs/<digest>_curves.parquet`)을 staging 디렉터리로 먹여 우회 |
| B | **score → hessian → report 순서가 인용 금지 배너를 만든다.** hessian 이 `degeneracy_summary.yaml` 에 넣는 `hessian_pe_ne_coupled_frac`·`hessian_eps` 를 stale 검사의 재계산본이 모른다 | `_numbers_equal(saved+hessian키, 재계산)` → **False** (직접 측정) | 정상 실행이 스스로 인용 불가 문서를 만든다. 이번엔 hessian 뒤에 score 를 한 번 더 돌려 회피(보고서 Hessian 절은 `hessian_*.parquet` 에서 나오므로 손실 없음) |
| C | A·B 가 지금까지 안 드러난 이유 — **`scripts/smoke_e2e.sh` 에 hessian 단계가 없다** | smoke 8개 단계에 hessian 없음 | 커버리지 구멍. 15차에서 smoke 에 hessian 단계 추가 필요 |
| D | `_verify_noise_families` 의 `sorted(fams.items(), key=repr)` 이 **DataFrame 을 통째로 문자열화**한다 (값이 `(noise, cid, DataFrame)` 목록) | traceback 이 pandas `to_string` → `_trim_zeros_float` 에서 잡힘. 곡선 검증 1회에 수십 분 | 14차에 내가 넣은 결함. 기능은 정확하나 검증이 병목. `key=lambda kv: kv[0]` 로 고칠 것 |
| E | 보관 묶음이 **git EOL 정규화로 깨질 뻔했다**. `failed.csv` 는 `csv.writer` 가 CRLF 로 쓰는데 `.gitattributes` 의 `*.csv text eol=lf` 가 이를 LF 로 바꾼다 | `git add` 경고 4건 | 다른 clone 에서 복원한 바이트가 `payload_sha256`·`입력_digest_재해시` 와 어긋난다 = archive 의 존재 이유가 무너진다. `artifacts/** -text` 로 막았고(RUN_SCOPE 밖이라 digest 불변) 외부 clone 검증으로 확인했으나, **이를 고정하는 회귀 테스트가 없다** |
| F | 한 clone 을 두 세션이 공유하면 브랜치 전환만으로 실행 중 코드가 사라진다 (20.3) | 실제 사고 | 검출은 됐으나 **예방은 운영 규율에만 의존**한다. 실행 중 주기적 digest 확인 등 코드 측 강화 여지 |

A·B·C 는 **정상 실행 경로의 결함**이라 15차의 우선 대상이다. D 는 성능, E 는
회귀 테스트 부재, F 는 설계 판단이 필요한 항목이다.

---

## 21. 15차 게이트 리뷰 회답 (2026-08-13, 대상 `5b83c6c`)

판정: **봉인된 v4 curves/fits 는 GO** (폐기·재실행 불필요), **현재 `RESULTS*.md`
문구는 NO-GO**. 8시간 재실행이 아니라 렌더링·해석 수정이 필요하다는 것이 핵심이다.

### 21.1 수치 오류 — 산출물에서 재확인했다

리뷰 지적을 archive 에서 직접 재계산해 **전부 사실로 확인**했다.

```
paired_fixed5_v4  pocv_dvdq       degen=0.619241  corr=0.144309  mean_abs_err=0.024227
paired_fixed5_v4  pocv_dvdq_dqdv  degen=0.871951  corr=0.945122  mean_abs_err=0.065287
gap(recoverable)  n_wide=245  collapse=0.004081632653061225 (=1/245)  LR=90.0
gap(all)          n_wide=604  collapse=0.10596026490066225           LR=3.6903
verdict_22p       n_near=8    degenerate_frac=0.125 (=1/8)
unrecoverable_frac = 0.5190615835777126
population_sensitivity  recoverable +0.0054  /  all −0.0257  (direction_flips=True)
```

§20.4 에 정정 블록을 넣었다. 요지:

| 항목 | 원문(오류) | 정정 |
|---|---|---|
| 결론 1 정본 | 62% → 63% "사실상 변화 없음" | **paired 61.9% → 87.2% (+25.27%p)**, `warm_start=False` 조건부. 34p multimodal 97% 라 정보량 비교 불가. 방어 가능한 형태는 endpoint 를 명시한 "사전 지정한 aggregate raw-degeneracy endpoint 에서 34p 개선 미관측" 이다 (철회[WARM_NO_IMPROVE_ANY]) |
| 붕괴율 | 0% / 0건 | **1/245 = 0.41%** (정수 반올림이 만든 0%). 0건이면 LR 이 90 이 아니라 무한대 |
| LR 90 | 그대로 인용 | **조건부 값**. 전체 격자에서는 `64/604`, **LR 3.69**. 넓은 격차 붕괴 64건 중 63건(98.4%)이 recoverability 필터로 제외 |
| 22p 12% | 단독 인용 | **1/8**, 그 1건은 최대 mode 오차 2.02248%p 로 임계 2%p 를 0.022%p 초과한 경계 사건 |
| 평균 \|err\| | 일반 MAE 로 읽힘 | 실제는 **행별 max-mode 절대오차의 평균** (`src/scoring.py`) |
| Case 1 7% vs Case 2 62% | "기준 곡선이 목적함수보다 크다" | **reference-specific pipeline 비교**로 제한 (bounds·p_ini·mode 매핑이 함께 다름) |

### 21.2 A~F 판정 수용

- **A(hessian 분리배치)**: 이번 staging 은 봉인 곡선과 byte-identical 이었고
  (`b69dc7bee0bb2e32…`), 표본 cond_id 와 재계산 Hessian 도 일치(최대 상대차
  ~1.34e-11) → **오염 없음**. 다만 정식 경로가 아니므로 `--curves` 또는 봉인
  `_inputs` 자동 해석으로 고친다. half-cell Hessian 이 live cache 를 읽는 것도
  같이 고친다.
- **B(rescore 우회)**: canonical fits 에서 summary 만 재생성 → **수치 안전**.
  `src/hessian.py` 가 scoring 산출물을 변이시키지 않도록 분리한다.
- **C·D·E·F**: 각각 smoke 회귀 추가 / `key=repr` 제거(실측 16.47s → 0.838s,
  19.7배) / Git byte round-trip 회귀 / chunk 경계 fail-fast.

### 21.3 재실행이 불필요한 근거 (validator 설계)

`src/io.py:1511-1521` 은 **현재 commit == 기록 commit 이고 clean 일 때만**
`코드_재계산` 을 수행하고, 다른 commit 에서는 `_참고_코드재계산불가` 로 사실만
남긴다. 따라서 A~F 를 고쳐 digest 가 바뀌어도 **봉인 fits 로 score·report 를
재생성할 때 인용 금지 배너가 생기지 않는다.** v4 는 `c0f1daa0 /
d50295f980ccaa81` 산출물로 고정 인용하고, 렌더링만 새 코드로 다시 만든다.

### 21.4 남는 한계 — 재실행으로 해결되지 않는 것

리뷰가 명시한 대로, LR 모집단 문제(52% 조건부 선택)와 22p 임계 민감도는
**계산이 아니라 해석·조건화의 문제**다. 8시간을 다시 돌려도 바뀌지 않는다.
"실제 22p 셀에서 두 전극이 비슷하게 열화했다"는 판정은 이 자료로 불가능하며,
그 문장은 어느 버전에서도 쓰지 않는다.

---

## 22. 17차 게이트 전 자체 발견 — 16차 발견 4 의 잔여와 그 정정의 상수화

16차 발견 4("최근접 8점이 모두 참값 `LAM_PE = LAM_NE` 라는 전제는 거짓")를
닫았다고 보고했으나, 재생성한 보고서를 문장 단위로 다시 읽으면서 두 건이 더
나왔다. 리뷰가 지적한 것이 아니라 **우리가 먼저 찾은 것**이므로 여기 남긴다.

### 22.1 잔여 — 격차 절 도입부가 같은 거짓 전제를 다시 말한다

`tools/make_results.py` 의 `## 전극 격차를 구분하는가` 절 도입부가 그대로였다.

| 위치 | 문장 |
|---|---|
| `docs/RESULTS.md:128` · `RESULTS_PAIRED_FIXED5.md:115` | "22p 근방 격자점은 **참값이 애초에 `LAM_PE = LAM_NE`** 다" |

같은 문서 `:113` 의 "이 8점은 참값이 모두 같은 격자점이 아니다" 와 정면으로
모순됐다. 16차 대응에서 **결론 3 과 22p 절만** 고치고 이 절을 놓쳤다.

고친 문장: "22p 근방 격자점은 **참 격차가 작다** — PE=NE 가 4/8, |ΔLAM|>0 이
4/8 이고 최대 참 격차가 2.0%p 다." 논지(근방 성적은 증거가 못 된다)는 참 격차가
작다는 사실만으로 성립하므로, 거짓 전제 없이도 그대로 선다.

### 22.2 더 큰 문제 — 정정 문구 자체가 artifact 와 무관한 상수였다

16차 대응으로 넣은 정정 문구가 전부 문자열 상수였다.

| 상수 | 어디 |
|---|---|
| "절반은 PE=NE, 절반은 \|ΔLAM\|=2%p" | 결론 3 · 22p 절 경고 |
| "wide-gap(≥6%p)은 하나도 없다" | 같음 |
| "gap 분석의 분모는 noise=0 의 98·245조건, 22p 는 8조건" | 결론 4 |

v4 격자에서는 우연히 맞지만, 반경·step·noise·목적함수를 바꾸면 **provenance
통과 배지를 단 채 거짓을 말한다**. 지금 고치는 대상(하드코딩된 해석)과 같은
종류의 결함을 정정 문구로 새로 만든 셈이다.

- `p22_truth_composition()` 이 근방 표본의 참값 구성을 데이터에서 뽑는다
  (`n_near_exact_equal`, `max_true_pe_ne_gap`)
- `_p22_composition()` · `_denominator_note()` 가 그 count 로 문장을 만든다
- 구버전 artifact 로 렌더하면 구성을 **지어내지 않고** "이 artifact 에 기록되어
  있지 않다" 로 쓰고, 도입부도 "참 격차가 작다" 라고 단정하지 않는다

### 22.3 그 수정이 만든 두 번째 실수 — 봉인 schema 오염

구성 count 를 `verdict_22p` **반환**에 넣은 첫 판으로 v4 를 재생성했더니
인용 금지 배너가 떴다.

```
⛔ 인용 금지 — 실패한 검사: 파생_stale_objective_comparison.yaml
   objective_comparison.yaml의 저장본이 정본 fits 재계산과 다르다
```

F87 은 저장본과 재계산본의 **key 집합**을 대조한다. v4 의 봉인
`objective_comparison.yaml` 에는 그 key 가 없으므로 재계산본과 집합이 달라지고,
stale 판정이 **정당하게** 떴다. 되돌리려면 8시간 재실행이 필요한 종류의 실수다.

교훈: **렌더 전용 파생값을 봉인 YAML 의 schema 에 넣으면 안 된다.** 구성은
`make_results.build` 가 stale 대조를 끝낸 **뒤에** fits 정본에서 뽑아 주입한다.

이 결함은 fixture 로는 잡히지 않는다 — 같은 코드가 저장본을 쓰면 key 집합이
항상 일치하기 때문이다. 그래서 회귀는 **schema 자체**를 검사한다
(`test_p22_composition_stays_out_of_sealed_comparison_schema`) + 저장본에 구성
key 가 없는 상태에서 stale 없이 렌더되는지 보는 build 회귀를 함께 넣었다.

### 22.4 검증

| 항목 | 값 |
|---|---|
| 전체 테스트 | **320 passed** |
| strict smoke | 통과 (clean 커밋) |
| v4 재생성(격리 root) | 두 보고서 모두 **인용 금지 배너 0 · `provenance 검증 통과` 1** |
| 거짓 전제 잔여 | `애초에` 0회 · `구버전` fallback 0회 |
| 계산 산출물 | **불변** — `c0f1daa0` / `d50295f980ccaa81` 봉인 v4 그대로 |

---

## 23. 17차 리뷰 대응 — 발견 1~10

### 23.1 발견 1 (숫자가 바뀜) — 2%p 경계의 binary float

참 격차는 0.02 step 격자의 뺄셈이라 nominal 2%p 가 `0.01999999999999999` 로
표현된다. raw float 에 `< 0.02` 를 그대로 걸어 **수학적으로 2%p 인 조건이
"2%p 미만" 군**에 들어갔다. 봉인 v4 실측(recoverable·noise=0·`pocv_dvdq`):

| 지표 | 수정 전 | 수정 후 |
|---|---:|---:|
| 작은-gap 분모 | 98 | **66** |
| "같다"로 답한 분자 | 36 | **24** |
| 사건률 비 (recoverable) | 90.00 | **89.09** |
| 전체 격자 작은-gap | 61/156 | **34/93** |
| 전체 격자 사건률 비 | 3.69 | **3.45** |
| wide-gap 분모 / 붕괴 | 245 / 1 | **불변** |

wide-gap 쪽이 불변인 이유: nominal 6%p 는 float 에서 위로 떨어져
(`0.06000000000000001`) 이미 `>= 0.06` 에 들어 있었다. 즉 **한쪽 경계에서만**
샜다.

`gap_lt` / `gap_ge` / `gap_is_zero` 하나로 고정하고 `gap_analysis`·
`gap_sensitivity`·`p22_truth_composition` 이 전부 그것만 쓴다 (`GAP_ATOL=1e-9`).

**부수 결과 — 리뷰 미지적.** 경계를 canonical 하게 읽으면 F34 의 두 "같다"
정의(`< tol` / exact-zero)가 **인용 지점에서 같은 집합**이 된다. 격자 step 이
2%p 라 `< 2%p` 가 `= 0` 과 같아지기 때문이다.

```
tol=1%p  lt_tol n=66 LR=44.55  |  exact_zero n=66 LR=44.55
tol=2%p  lt_tol n=66 LR=89.09  |  exact_zero n=66 LR=89.09   ← 인용 지점
tol=3%p  lt_tol n=166 LR=13.28 |  exact_zero n=66 LR=15.19   ← 여기부터 갈린다
```

F34 가 두 정의를 나눈 이유는 "exact-zero 는 tol 과 무관한 고정 집합이라 임계
효과만 분리해 볼 수 있다" 였는데, **정작 인용하는 칸에서 그 분리가 성립하지
않는다.** 두 패널을 나란히 싣고 아무 말도 안 하면 독립인 두 확인으로 읽힌다 —
보고서가 그 사실을 데이터에서 렌더한다.

### 23.2 발견 2 — nested wsweep 의 `repo_root`

16차 대응이 main·scoring·case 세 경로만 관통시켰고 `make_results.py:563` 의
`_vp(in_dir / "wsweep")` 은 빠졌다. **기존 spy fixture 에 `wsweep/` 가 없어 그
분기를 실행조차 하지 않았다** — "관측된 호출은 모두 옳다" 는 형태의 검사로는
빠진 호출을 잡을 수 없다. 리뷰 지시대로 **기대 호출 집합**을 고정했고,
`wsweep_provenance` 를 header 검사 목록에 노출했다 (main 보고서에 1건 표시,
paired 는 nested sweep 이 없어 미표시).

### 23.3 발견 3·4·5·6·10 — 서술

| # | 수정 | 재생성 실물 |
|---|---|---|
| 3 | 노이즈 문장을 **표에서** 만든다 | main `noise 0 → +4%p, 0.001 → +0%p, 0.005 → −2%p … 방향이 바뀐다` · paired `+28/+26/+22%p … 모든 노이즈 수준에서 34p 가 더 크다` |
| 4 | `agree_frac` 경고를 adaptive / fixed-budget 로 분기 | paired 에서 `adaptive 조기 종료 때문에` 0건 |
| 5 | Case 표 라벨 | `평균 max-mode \|err\|` |
| 6 | eligibility rule | `현재 grid-reference 의 α-window eligibility rule 밖` (`src/scoring.py`: `alpha_true >= 1 − atol`) |
| 10-1 | 전체군 반대쪽 분자 | `작은 격차에서 "같다" 34/93 (36.56%)` 를 같은 문장에 |
| 10-2 | 22p protocol | `noise=0, radius=0.021 안의 최근접 8 grid 조건` |
| 10-3 | 임계 문구 | `낮은 붕괴율의 **일부는** … 오차 스케일이 임계 간격보다 작다는 사실에서` |

### 23.4 발견 7 — Hessian 범위

리뷰가 준 세 선택지 중 **2번(명시적 범위 제외 + 비인용 부록)** 을 택했다.

- 재현 블록에서 hessian 실행 명령 **삭제** — 분리배치에서 실패하고, 실행하면
  `degeneracy_summary.yaml` 을 변이시켜 보고서를 stale 로 만든다. 대신 그
  사실을 주석으로 남긴다
- Hessian 절 상단에 `⛔ 이 절은 문서 상단 provenance 검증 범위 밖입니다` +
  검증되지 않는 항목 열거(곡선·`obj_cfg`·`v_col`·reference·표본·`eps`)
- "같은 eps 에서의 순서는 의미 있다" **철회** — eps 안정성 근거가 없고, 표에
  objective 가 하나뿐이면 순서 자체가 없다
- `src/hessian.py` 머리말의 "이것이 degeneracy 의 **직접 증거**다" 를 부호 규약
  경고로 교체 (α_PE·α_NE 같은 부호를 세는데 22p 가설은 반대 부호다)

### 23.5 발견 8 — `05_HANDOFF.md`

최상단에 철회 안내표(5행)를 넣고, 문제가 되는 절 4곳에 철회 표시를 달았다.
지키는 방식은 **문구 금지가 아니라 구조 검사**다 (`tests/test_docs_lint.py`):
철회 명제가 나오는 절에는 같은 절 안에 철회 표시가 있어야 한다. 역사 기록을
지우라는 뜻이 아니라, 표시 없이 현행 답처럼 두지 말라는 뜻이다.

### 23.6 발견 9 — 22p selection protocol

`verdict_22p` 가 `radius` 를 기록하고(canonical protocol), renderer 는 기본값이
아니라 **기록된 radius** 로 구성을 뽑는다. 구성 helper 가 `n_near_composition`
을 함께 실어, verdict 와 표본 수가 다르면 `ValueError` 로 렌더를 멈춘다.

### 23.7 검증

| 항목 | 값 |
|---|---|
| 전체 테스트 | **339 passed** |
| strict smoke | 통과 (clean 커밋 `424d295`) |
| 재생성 | 빈 격리 root 에 4묶음 복원 → `score → compare → report` |
| 두 보고서 | 인용 금지 배너 **0** · `provenance 검증 통과` **1** |
| 계산 산출물 | **불변** — `fits.parquet` 재fit 없음 |

### 23.8 남은 것 — 봉인 묶음 안의 파생 YAML 은 옛 숫자다

`artifacts/*/objective_comparison.yaml` 은 발견 1 이전 값(`36/98`, `90.0`)을
그대로 갖고 있다. 보고서는 `--mode report` 가 compare 를 먼저 돌려 재계산본을
싣지만, **묶음을 복원해 그 YAML 을 직접 읽는 소비자는 옛 숫자를 본다.**
발견 8 과 같은 실패 모드가 artifact 안에 남아 있는 셈이다. 재보관(v4.1 파생
갱신)을 할지 문서화로 둘지는 17차 답변을 받아 정한다.

---

## 24. 18차 리뷰 대응 — 발견 1~11

### 24.1 발견 1 (P0) — `collapse_measurable` 삭제

리뷰의 반례를 그대로 실행해 확인했다.

```
true 0.10 → recovered 0.20   (붕괴와 정반대 방향)
gap_collapse_frac = 0.0      collapse_measurable = True
```

`|recovered − true|` 의 p99 를 모든 행 공통 `gap_thresh − tol` 과 비교했으므로
(a) `true − recovered > 0` **방향**과 (b) 행마다 다른 필요 감소량 `true − tol`
을 둘 다 버렸다. 게다가 같은 결과에서 뽑은 오차분포로 그 결과의 낮은 사건률을
방어하므로 **순환 논리**였다.

boolean 과 "붕괴가 원리적으로 관측 가능한 범위" 문장을 삭제했다. 남긴 것은
부호 있는 행별 여유의 기술통계뿐이다.

| 지표 | v4 (recoverable·noise=0·33p) |
|---|---|
| `tol − 복원 격차` 중앙값 | −8.2%p |
| 같은 값 최대 | 1.8%p |
| 격차가 줄어든 방향 | 98/245 조건 |

문장에 "이 값들은 **기술통계일 뿐, 붕괴가 관측 가능했다는 근거가 아니다**" 를
명시하고, 견고성 판단은 임계 민감도 표와 모집단 제한으로만 하도록 했다.

### 24.2 발견 2·3·4 (P0) — protocol·모집단·재현 범위

| # | 수정 |
|---|---|
| 2 | `_random_only_note(warm_start)` — no-warm 에서는 restart 0 이 warm solution 이 아니라 `base_init` 이라고 쓴다. 절 제목도 표에서 종수를 센다 (paired 재생성본 `## 목적함수 2종 비교`) |
| 3 | `α/bounds feasible domain`·`원리적으로 복원 불가` 를 전부 `α-window eligibility criterion` 으로. `feasible domain` 토큰을 요구하던 기존 assertion 도 바꿨다 |
| 4 | `_reproduction_scope_note(has_wsweep, has_halfcell, has_hessian, warm_start)` — 실제 렌더 상태에서 만든다. Hessian 은 "기본 eps 포함 명령 전체 미출력" 으로 |

### 24.3 발견 5 (P0) — lint 강화 + `GATE14_CYCLE_SUMMARY.md`

1차 lint 의 네 한계를 모두 고쳤다.

| 한계 | 수정 |
|---|---|
| fenced code 안의 `#` 를 heading 으로 오인 | `_strip_fences()` 로 코드 블록 제외 |
| 절에 마커 하나면 그 절 전체 면제 | **claim ID 별 마커** — `⛔ 철회` 뒤 대괄호에 claim ID |
| 단일 문구 regex | 동의어 포함 (`원리적으로 정답이 안 나`, `feasible domain 밖` 등) |
| Hessian 순위·합성 하한 rule 부재 | `HESSIAN_EPS_ORDER`, `SYNTHETIC_IS_LOWER_BOUND`, `STALE_GAP_NUMBERS` 추가 |
| — | 정본 링크에 대한 **positive assertion** 추가 |

`GATE14_CYCLE_SUMMARY.md` 를 lint 대상에 넣고, "수치의 정본은
`objective_comparison.yaml`" 선언을 **superseded** 로 바꿨다(정정표 포함).
`05_HANDOFF.md` §10 의 F1·F7·F23 도 정정했다.

### 24.4 발견 6 (P0) — 파생 분석 provenance + semantic 게이트

리뷰가 제시한 스키마를 그대로 구현했다.

- `analysis_manifest.yaml` — raw 입력 digest / **생성 코드 좌표(분리)** /
  파라미터 / 출력 digest. raw 계산 `manifest.yaml` 은 건드리지 않는다
- `objective_comparison.yaml` 에 `_analysis` self-description
  (`schema_version` · `analysis_spec_id` · `fits_sha256`). `_` 로 시작하므로
  F87 key 집합 대조에서는 제외된다
- 파라미터에 22p selection protocol 을 박았다 (center · radius · metric
  `unscaled_euclidean_fractional_coordinates` · `nearest_fallback` · 선택
  cond_id digest) + noise 단위 `σ[V]`
- `python -m tools.check_derived_fresh <run>` 게이트를
  `scripts/archive_results.sh` 승격 직전에 태운다. stale 이면 그 run 은
  승격하지 않고 기존 묶음을 유지한다

### 24.5 발견 7·8·9·10·11 (P1)

| # | 수정 | 실측 |
|---|---|---|
| 7 | `p_spread=0` → "qualifying restart 가 하나였거나 **여러 restart 가 같은 파라미터에 수렴**한 경우 모두 가능" | — |
| 8 | 민감도 범위가 `<tol` 패널 값임을 명시 + exact-zero 패널 최대값 병기 | lt_tol `2.2~130.5`(중앙값 16.1) · exact_zero 최대 **165.4** — 리뷰 값과 일치 |
| 9 | p22 wide 판정을 공통 `gap_ge` 로; empty-radius fallback 을 `radius_fallback`/`p22_radius_fallback` 로 기록 | v4 는 radius 0.021 에 8점이 있어 값 변화 없음 |
| 10 | "안장점에서 곡률을 잰 것" → "국소 최소점임이 입증되지 않은 지점, saddle 인지 수치 artifact 인지 구분하지 않음". "최적점에서" → "optimizer 가 반환한 해에서(정상점 미검증)" | — |
| 11 | 경계 수정 이전 경험값과 "8시간 재실행" 표현을 docstring 에서 제거 | — |

### 24.6 검증

| 항목 | 값 |
|---|---|
| 전체 테스트 | **359 passed** |
| strict smoke | 통과 (clean 커밋 `3c77a94`) |
| 재생성 | 격리 root 에 4묶음 복원 → `score → compare → cases → report` |
| 두 보고서 | 인용 금지 배너 **0** · `provenance 검증 통과` **1** |
| 계산 산출물 | **재fit 없음** |

### 24.7 남은 것 — v4.1 파생 재보관

코드·게이트·스키마는 준비됐다. 실제 재보관(`artifacts/` 의 파생 YAML 교체 +
`analysis_manifest.yaml` 추가 + 네 v4 계열 보존 index 재생성)은 **아직 하지
않았다** — `artifacts/` 바이트를 바꾸는 작업이라 사용자 판단을 받고 진행한다.
raw `fits`/`curves`/`manifest`/`_inputs`/`wsweep` 는 byte-identical 로 보존한다.

---

## 25. 19차 사전 자체 리뷰 (fable-5 내부 실행) — 발견 4건

외부 리뷰어를 돌릴 수 없어 내부 적대 리뷰로 18차 대응과 v4.1 재보관을
재검토했다. 4건을 찾아 모두 RED-first 로 닫았다.

### 25.1 freshness 게이트가 한 방향만 순회 — 부분집합-stale 통과

`verify_derived_freshness` 의 walk 가 saved→now 만 돌았다. **새 코드가
계산하는 key 가 빠진** 저장본(더 오래된 schema)이 공유 key 숫자만 맞으면
통과했다. 실측: 재보관 직후 묶음에서 `collapse_margin_median` 을 지워도
`ok=True`. 역방향 key 대조를 추가했다.

### 25.2 게이트가 `analysis_spec_id` 를 대조하지 않음

spec 이 다른 파일이 숫자만 우연히 맞으면 통과했다. 현행 파라미터에서
spec_id 를 재계산해 저장본 `_analysis.analysis_spec_id` 와 대조한다.

### 25.3 18차 발견 9 의 부분 마감 — fallback 을 기록만 하고 렌더는 무분기

`radius_fallback` 을 verdict 에 **기록**했지만 renderer 는 여전히 무조건
"radius 안의 최근접 N grid 조건" 이라고 썼다 — fallback 이면 거짓 문장이다.
결론 3 이 플래그로 분기한다 (v4 는 fallback=False 라 렌더 결과 불변 —
따라서 committed 보고서 재생성은 불필요하고, 보고서의 report generator
좌표는 `739453aaf9c07be3` 그대로가 정확한 기록이다).

16차 발견 4(결론만 고치고 절 도입부 방치)와 같은 실패 모드 — "한 발견을 한
지점에서만 고침" — 이 자체 리뷰에서도 또 나왔다는 사실을 기록해 둔다.

### 25.4 수정 과정에서 만든 두 결함 (즉시 실측으로 드러남)

1. **F87 제외 집합 미공유** — 양방향 walk 를 넣자 smoke 의 **정상** 승격이
   `.figures.weight_curve: 저장본에 없다` 로 막혔다. `figures` 는 그림 경로
   목록이지 과학 수치가 아니다. 두 walk 가 F87 과 같은 제외 집합
   (provenance·provenance_ok·공통_run_spec·figures)을 쓴다.
2. **격리 복원 검증 heredoc 의 SIGABRT teardown flake 노출** — smoke 반복에서
   wrapper 승격이 2/4 실패했다. 실패 지점은 항상 같은 heredoc 이고 프로세스가
   출력 없이 죽었다(pyarrow 적재 상태 teardown SIGABRT, 원인 미규명 — 15차
   실측과 동일 서명). read-only 검증이므로 smoke 8단계의 기존 처방과 같이
   flush 후 `os._exit(rc)`. 수정 전 2/4 실패 → 수정 후 wrapper 단독 6/6 ·
   전체 smoke 연속 2회 0 fail.

### 25.5 통과 확인한 렌즈 (발견 없음)

| 렌즈 | 결과 |
|---|---|
| v4.1 재보관 raw byte-identity | payload digest 전수 대조 변경 0건 (§24 와 동일) |
| artifact_index 4계열 보존 + `source_commit=c0f1daa0` | 통과 |
| 보관된 `analysis_manifest` generator 좌표 | `dec589a` / `739453aaf9c07be3` / dirty=False — 정확 |
| 강화된 게이트 vs 보관 v4.1 세 묶음 | 3/3 통과 (spec_id 일치) |
| v4.1 묶음 격리 복원 → compare 없이 직접 report | 인용 금지 배너 0 |

### 25.6 검증

전체 테스트 **363 passed** · strict smoke 통과(clean `7b17bde`) + 재실행 0 fail
· 코드 identity `f2ff3092d3cdf610` · 계산 산출물 불변.

---

## 26. 18차 Q4 방어 3층 구축 (1층 → 2층 → 3층 순서 준수)

리뷰가 "리팩터링부터 하면 잘못된 protocol 문구를 새 구조에 그대로 옮길 위험이
있다" 며 지정한 순서를 그대로 따랐다.

### 26.1 1층 — 문서 전체 characterization matrix (`tests/test_report_matrix.py`)

helper 를 부르지 않는다. 완전한 artifact 조합에서 `build()` 로 문서를 통째로
만들고 **문서만 보고** 검사한다 — 지금까지 놓친 것들이 전부 "helper 는 옳은데
그 조합에서 안 불렀다" 였기 때문이다.

조합 4종(main adaptive/warm 전체 · paired fixed/no-warm 최소 · fixed+sweep ·
adaptive+Hessian) × 5축(protocol 문구 · heading 종수 · 절↔명령 상호 함의 ·
재현 범위 · 철회 명제 6종 부재) = **40 케이스**.

### 26.2 2층 — immutable `P22RenderFacts`

`build()` 가 `cmp_res['verdict_22p']` 를 `.update()` 하던 것을 없앴다. canonical
derived metric 층과 render-only presentation 층을 한 dict 에 섞으면, 그 dict 를
다시 저장하는 코드가 생기는 순간 봉인 schema 가 오염된다 (17차에 실제로 인용
금지 배너를 낸 경로다). `@dataclass(frozen=True)` 로 얼리고, 표본 일치
불변식(17차 발견 9)을 **fact 생성 시점**으로 끌어올렸다.

### 26.3 3층 — property test (`tests/test_p22_properties.py`)

radius·noise·격자 step·offset·임계 부동소수점 표현을 흔들며 불변식만 본다
(P1 표본 일치 · P2 경계 규약 · P3 fallback 정직 · P4 단조성 · P5 문장-사실 대응).

**property test 가 실제 결함을 찾았다.** `_near_22p` 의 반경 비교만 raw `<=`
였다 — 17차 발견 1 과 같은 부류로, nominal 경계 위의 점이
`(0.13+0.01)-0.13 = 0.010000000000000009 > 0.01` 처럼 표현 오차로 반경 **밖**
으로 떨어지고 최악의 경우 fallback 까지 유발했다. `GAP_ATOL` 로 흡수했다.
v4 실측 영향은 없다 (`n_near=8`, `fallback=False` 그대로).

### 26.4 뮤테이션 검증 — 새 테스트가 처음부터 통과하면 믿지 않는다

1·3층 모두 전부 통과해서, CLAUDE.md 규칙대로 성공으로 보지 않고 뮤테이션을
돌렸다. **fixture 결함 3건**이 거기서 나왔다.

| 뮤테이션 | 결과 | 드러난 것 |
|---|---|---|
| M1 warm 인과 무조건 출력 | 처음엔 **안 물었다** | fits 에 random restart 가 1개뿐이라 `multistart_random_only` 절이 아예 안 떠서 **warm 축이 통째로 미실행** |
| M2 제목 "4종" 하드코딩 | 4 fail | — |
| M3 재현범위 boilerplate | 6 fail | — |
| M4 adaptive 설명 무조건 | 2 fail | — |
| M5 hessian 명령 부활 | 2 fail | — |
| M6 feasible domain 부활 | 4 fail | — |
| M7 canonical dict 변이 부활 | 1 fail | — |
| M8 표본 불일치 검사 제거 | 1 fail | — |
| M9 경계 atol 제거 | 10 fail | — |
| M10 fallback 항상 False | 처음엔 **안 물었다** | 격자에 중심점이 항상 있어 empty-radius fallback 미발생 → P1·P3 축 미실행 |
| M11 구성 기본 radius 어긋남 | 처음엔 **안 물었다** | 기본값 일치 property 부재 |
| M12 반경 `<=` → `<` | 처음엔 **안 물었다** | 거리 == radius 인 점이 없어 경계 미실행 → §26.3 실제 결함 발견으로 이어짐 |

같은 라운드에서 "테스트가 축을 안 태운다" 가 **세 번** 나왔다. 뮤테이션 없이는
40·143개 통과를 그대로 믿었을 것이다.

### 26.5 검증

전체 테스트 **550 passed** (+183) · strict smoke 통과 · 계산 산출물 불변 ·
v4 보고서 재생성 불필요(반경 수정이 렌더 결과를 바꾸지 않음).

### 26.6 남은 것

- 4층 active-doc lint 는 §24.3 에서 이미 강화 (claim ID · fenced-code parser ·
  동의어 · positive assertion). `RESULTS*.md` 두 종을 lint 대상에 넣는 것은 미착수
- A · A' · B · C (Hessian provenance + smoke 커버리지) · E · F 미착수

---

## 27. 18차 잔여 전량 마감 — 4층 lint · A · A' · B · C · E · F

### 27.1 4층 — 생성물 정본 lint

`tests/test_docs_lint.py` 에 `GENERATED_DOCS`(`RESULTS.md`,
`RESULTS_PAIRED_FIXED5.md`)를 추가했다. 손으로 쓴 문서와 달리 마커가 아니라
**positive assertion** 으로 지킨다: 철회 명제 부재 · provenance 앵커 3종 존재 ·
인용 금지 배너 부재 · 경계 수정 **이후** 수치 사용.

생성 코드 회귀(1층 matrix)는 *새로 만든* 문서를 본다. 저장소에 **커밋돼 있는**
파일이 그 코드로 만들어졌는지는 별개 문제였고, 지금까지 아무도 안 봤다.

### 27.2 A — 분리 배치에서 Hessian 이 곡선을 못 찾아 죽었다

`resolve_curves()` 가 세 경로를 본다: `--curves` → `<in>/curves.parquet` →
봉인 `_inputs/<digest12>_curves.parquet`. 셋 다 없으면 raw `FileNotFoundError`
대신 무엇이 필요한지 말하고 멈춘다. **v4 가 그 배치이므로 문서가 제시하던
Hessian 재현 명령은 애초에 돌지 않았다** — 리뷰 지적 그대로 RED 로 재현했다.

### 27.3 A' — half-cell 기준을 live config·live cache 로 만들었다

봉인 스냅샷의 `base.yaml` 과 half-cell 캐시를 정규 이름으로 펼쳐 그것만 쓴다
(스냅샷은 `<digest12>_<이름>` 이라 캐시 키 조회가 안 된다). 봉인 입력이 없으면
경고하고 인용 불가임을 남긴다.

### 27.4 B — 채점 산출물 변이 제거

`degeneracy_summary.yaml` 덮어쓰기를 없애고 `hessian_summary.yaml` sidecar 로
분리했다. sidecar 안에 **인용 범위 밖**임과 곡선 출처를 함께 적는다. 부수로
"같은 eps 에서 목적함수끼리만 비교할 것"(18차 발견 7 에서 철회) 도 제거했다.

### 27.5 C — `run.sh --mode all` 옵션 전파 + smoke 커버리지

`--objective`·`--n-restarts`·`--clean`·`--no-adaptive`·`--no-warm-start`·noise 축을
전부 전파한다. `RUN_SH_DRY=1` 로 실제 실행 없이 합성된 하위 명령을 검사한다.
Hessian 은 인용 범위 밖 부록이라 기본 체인에서 뺐다.

smoke 8단계 신설: 분리배치 Hessian 실행 · `degeneracy_summary.yaml` 불변 ·
sidecar 기록 · `score → hessian → report` 순서에 stale 없음 (4/4 통과).
처음엔 9단계로 넣었다가 보관 음성 테스트가 fixture 를 소모해 실패 — 보관 앞으로
옮겼다.

**부수 발견 (이 회차에 실제로 당했다).** `--mode report` 의 기본 출력이 커밋된
정본 `docs/RESULTS.md` 다. 중단된 테스트가 임시 디렉터리에서 돌다가 report
단계에서 정본을 scratch 수치로 덮어썼다. 입력이 정본 경로(`results/…`)가 아니면
run 디렉터리에 쓰도록 가드를 넣었다.

### 27.6 E — artifacts byte round-trip + `eol` 상속 해제

Git blob 을 `git cat-file` 로 정규화 없이 꺼내 작업본과 바이트 대조한다
(CRLF 를 담은 파일 우선, 그런 파일이 하나도 없으면 그것도 실패로 본다).
검사 중 `git check-attr` 이 artifacts 에도 `eol: lf` 를 보고하는 것을 확인 —
`-text` 가 이기지만 git 문서상 `eol` 지정은 text 를 사실상 켜므로 `!eol` 로
명시 해제했다 (`eol: unspecified` 확인).

### 27.7 F — 청크 경계 fail-fast

같은 조건이 두 청크에 **다른 내용**으로 있고 mtime 이 같으면, 이름순
tie-break 로 조용히 하나를 골랐다. `chunk_idx` 는 프로세스마다 독립이라 이름
정렬에 시간 의미가 없다 — 아무 근거 없이 한쪽 곡선을 버리고 그 선택이
downstream fit 입력을 바꾼다. 내용이 실제로 다를 때만 멈춘다 (동일 내용이면
통과, mtime 이 다르면 기존 최신-승 유지).

### 27.8 뮤테이션 검증 — 네 번째 "축 미실행"

| 뮤테이션 | 결과 |
|---|---|
| M13 정본 보고서에 옛 수치 주입 | 1 fail |
| M14 provenance 앵커 제거 | 1 fail |
| M15 봉인 스냅샷 해석 제거 | 5 fail |
| M16 sidecar 미기록 | 2 fail |
| M17 half-cell live cache 회귀 | 1 fail |
| M18 청크 fail-fast 제거 | 1 fail |
| M19 `-text` 제거 | 1 fail |
| M20 `--objective` 전파 제거 | 1 fail |
| M21 정본 가드 무력화 | 처음엔 **안 물었다** |

M21: 부작용(정본 파일이 바뀌었는가)만 보면, 빈 scratch 입력에서는 report 가
compare 단계에서 조기 종료해 **가드에 닿지도 않는다**. 경로 결정을 compare
앞으로 옮기고, 회귀가 부작용 대신 **해석된 출력 경로**를 보게 고쳤다.

이 라운드에서 "테스트가 축을 안 태운다" 가 M1·M10·M12 에 이어 **네 번째**다.

### 27.9 검증

전체 테스트 **572 passed** · strict smoke 통과 (8단계 Hessian 4/4 포함) ·
계산 산출물 불변 · v4 보고서 재생성 불필요.

### 27.10 남은 것

18차 리뷰가 지정한 항목은 **전부 닫혔다**. `artifacts/README.md` 의 v4 목록
갱신만 미착수다.

---

## 28. 19차 심층 자체 리뷰 — 게이트 재점검 + 발견 2건

외부 리뷰어를 돌릴 수 없어 내부 적대 리뷰로 18차 release gate 13항목을 증거와
함께 재점검했다.

### 28.1 발견 1 — 커밋된 정본의 generator 좌표가 stale 이었다

커밋된 `RESULTS*.md` 는 `3c77a94`/`739453aaf9c07be3` 생성물인데 HEAD 는 그
뒤로 여러 렌더 경로(P22RenderFacts 리팩터, radius fallback 분기 등)를 바꿨다.
즉 문서가 "이 코드가 나를 만들었다" 고 적은 좌표가 사실이 아니었다.

**봉인 fits 에서 HEAD 코드로 재생성해 diff 를 떴다.**

```
diff 줄수: 4  (양쪽 보고서 모두)
  생성: <타임스탬프>
  report generator git/source_digest/dirty: …
```

**과학 내용은 바이트 동일**이다 — 그 사이 변경들이 v4 렌더 결과를 바꾸지
않았음이 증명됐다. 정본을 HEAD 생성물로 교체해 좌표를 사실로 만들었다
(`d4f43d1` / `e5fa9749fd899e3d`).

4층 lint 가 이걸 못 잡은 이유도 분명하다 — 철회 문구·앵커·수치만 보고
**generator 좌표의 최신성**은 안 본다. 매 코드 변경마다 재생성을 강제하면
소음이 크므로, 잡는 방법은 lint 가 아니라 "승격 직전 재생성 후 diff" 절차다.

### 28.2 발견 2 — A' staging 이 아무 봉인 json 이나 집었다

`_sealed_halfcell_staging` 의 `*_*.json` glob 은 half-cell 캐시가 아닌 봉인
입력까지 집었다. 그러면 정작 캐시가 없는데도 staging 이 non-None 이 되어
"봉인 입력을 찾지 못했다" 경고가 안 뜨고 조용히 캐시 미스로 **재계산**된다 —
A' 의 목적이 그대로 무너진다. 실제 캐시 이름 규칙으로 좁혔다.

좁히자마자 기존 A' 테스트가 깨졌다 — fixture 가 `k_ocp_v` 같은 비현실적
이름을 쓰고 있었고 glob 이 넓어서 통과하던 것이다. 실물 이름으로 고치고,
**실제 v4 묶음의 이름**과 규칙이 맞는지 보는 회귀를 따로 넣었다.

### 28.3 통과 확인한 렌즈

| 렌즈 | 결과 |
|---|---|
| 보관 v4.1 vs **현행 코드** semantic 게이트 | grid·paired 3/3 통과 |
| `merge_chunks` 예외를 삼키는 호출자 | 없음 (`src/grid.py:533`, `src/fitting.py:960` 모두 전파) |
| smoke 반복 안정성 | 5회 중 1회 실패(서명 미포착) → 이후 **3회 연속 clean** |

### 28.4 18차 release gate 13항목 — 증거

| # | 항목 | 증거 |
|---|---|---|
| 1 | `collapse_measurable` 제거 | 코드에 남은 1건은 **삭제 사실 주석** (`compare_objectives.py:343`) |
| 2 | paired no-warm 설명·objective heading | `## 목적함수 2종 비교` 1건 · warm 인과 문구 **0건** |
| 3 | 52% → α-window eligibility | 두 보고서 모두 `feasible domain` **0건** |
| 4 | 동적 reproduction-scope | matrix 축 4 통과 (뮤테이션 M3 6 fail) |
| 5 | `p_spread`·민감도 범위·p22 radius/fallback | 문구 수정 + property 143 케이스 |
| 6 | HANDOFF archival | claim ID 마커 + lint 4항목 통과 |
| 7 | GATE14 summary superseded | 정정표 + 절별 마커 |
| 8 | full-document protocol matrix | 40 케이스 통과 (뮤테이션 6종 검출) |
| 9 | `P22RenderFacts` + analysis schema | frozen dataclass + `analysis_manifest.yaml` |
| 10 | 봉인 fits 재생성 | `score → compare → report`, 재fit 없음 |
| 11 | derived semantic 게이트 | 승격 전 3/3 통과 |
| 12 | v4.1 index 4계열 보존 | `runs` 4개 (`c0f1daa0` 유지) |
| 13 | raw byte-identical | payload digest 전수 대조 **변경 0건** |

### 28.5 검증

전체 테스트 **575 passed** · strict smoke 3회 연속 통과 · 정본 재생성본
인용 금지 배너 0 / provenance 통과 · 계산 산출물 불변.

### 28.6 남은 것

`artifacts/README.md` 의 v4 목록 갱신 하나. 18차 리뷰가 지정한 코드·문서
항목은 전부 닫혔다.

## 29. 21차 게이트 리뷰 회답 (1) — 문서 라운드, `source_digest` 불변

> 리뷰 대상 커밋 `f57ecd4d` · 판정 **NO-GO** (주 paired warm 대조는 통과,
> 정본 승격과 단계 3 착수는 불허). 리뷰가 지정한 실행 순서의 **1번**만
> 이 라운드에서 닫는다 — "`docs/09_22P_GAP.md` 의 활성 철회 잔여와 §20.4
> 문구를 먼저 고친다. 이 단계는 source digest 를 바꾸지 않는다."
>
> `source_digest` 전후 **`a72c0f3a485c19bb` 동일** — 기존 산출물 무효화 없음.

### 29.1 발견 8 — 배너 방식이 두 번 실패했으므로 기계로 바꿨다

19~20차에서 결론 7개를 철회하면서 **배너만** 달았다. 배너 위아래의 본문·
표·제목은 그대로 남아 같은 말을 계속했고, 21차 리뷰가 8곳을 찾아냈다.
사람이 지우는 방식은 실패 모드가 재발형이므로 **원장 + 기계 검사**로 바꾼다.

| 조각 | 무엇 |
|---|---|
| `docs/22p_gap/CLAIM_STATUS.yaml` | 철회·격하된 주장의 **정본 목록**. claim ID, 사유, `banned` 정규식, 대상 파일, `record`(quarantined/removed) |
| `<!-- QUARANTINE:<claim> -->` … `<!-- /QUARANTINE -->` | 옛 문장을 기록으로 남길 수 있는 **유일한 자리**. 마크다운에 안 보인다. 줄 전체가 마커 하나일 때만 울타리로 인정된다 (§30.8) |
| `test_retracted_claims_do_not_reappear_in_active_prose` | 울타리 **밖** 전부(활성 본문)에서 `banned` 를 찾는다. 걸리면 실패 |
| `test_every_quarantined_claim_still_has_a_visible_retraction` | 양성 결속 — 배너를 지워도 실패한다 |
| `test_claim_status_registry_is_wellformed` | 원장이 깨지면 위 둘이 조용히 통과하는 것을 막는다 |

**인용(blockquote)을 격리로 치지 않는다.** §20.4 는 재정정 블록 **전체**가
인용이라, 인용을 격리로 보면 정정문 자신이 검사에서 빠진다 — 리뷰가 지적한
바로 그 실패 모드의 재발이다.

이 검사가 처음 돌았을 때 **53건**이 걸렸다. 리뷰가 지목한 8곳보다 많다
(예: 철회된 `3/51 ≈ 5.9%` 상한을 §7.8·§7.10 이 계속 인용, `2 mV 상전이`가
두 절에서 되살아남). 전부 닫았다.

정규식 두 개는 **처음에 오탐**을 냈고 고쳤다 — `3/51` 은 `203/518` 과
seed_101 10 mV 다리의 실제 붕괴 건수 `3/51 (5.9%)` 를 함께 잡았고,
`3/306` 은 `13/306`·`30/306` 을 잡았다. 철회된 것은 **건수가 아니라 그것을
확률 상한으로 옮긴 계산**이라 `≈` 까지 본다.

### 29.2 발견 2 — endpoint 한정 없는 "개선 없음" 은 틀렸다

봉인 summary 에서 직접 뽑은 noise 층 (paired, 같은 digest·같은 예산):

| noise | 33p 실패 | warm 34p 실패 | 34p − 33p |
|---:|---:|---:|---:|
| 0 | 292/492 | 316/492 | +4.88%p (악화) |
| 0.001 | 304/492 | 308/492 | +0.81%p (악화) |
| **0.005** | **313/492** | **304/492** | **−1.83%p (개선)** |

metric 을 바꿔도 방향이 갈린다 — aggregate `mean_abs_err` 는 33p 0.024220
vs 34p 0.023653 으로 **34p 가 낫다**. 따라서 방어 가능한 형태는
**"사전 지정한 aggregate raw-degeneracy endpoint 에서는 34p 개선이 관측되지
않았다"** 까지다. `+1.29%p` 를 "차이 없음" 으로 부르던 문장도 지웠다 —
사전 equivalence margin 과 조건별 paired 전이표가 없다 (철회[WARM_TIE]).
같은 오용이 §14 (2026-05 판)에도 있어 함께 고쳤다.

회귀 `test_p22_doc_records_the_noise_layer_reversal` 은 세 층의 실패 건수를
봉인 summary 에서 계산해 문서와 대조하고, **반례 층이 0.005 하나뿐**인지도
확인한다. 문구만 지우면 다음 판이 같은 말을 다시 쓰므로 반례 자체를 묶는다.

### 29.3 발견 3 — multimodality 해석은 결과와 반대였다

목적함수 간 비교에 써야 하는 `multistart_random_only` 블록이 두 arm 에서
**완전히 동일**하다 — 34p multimodal `0.969512`, flat_valley `0.008130`.
같은 결정론적 난수의 같은 4개 random restart 는 그대로 다봉이었고, warm 이
한 일은 slot 0 의 결정론적 후보가 `base_init` → `warm` 으로 **교체**된
것이다 (★ 이 문단은 초판에 "하나를 더했다" 고 썼고, 22차 리뷰 발견 1 이
반증했다 — 철회[WARM_UNION]). 문서가 인용하던
nowarm 0.9614 / warm 0.9621 은 **교체된 slot 0 을 포함하는** `multistart`
블록이라 이 판단에 쓸 수 없었다. 양 arm 의 후보 수는 5로 같다.

warm 이 더 좋은 basin 에 앉혔다는 해석은 조건별 `J` 비교 없이 truth error
만으로 말할 수 없다 —
철회[WARM_BETTER_VALLEY]. F20 이 이 표로 측정됐다는 서술도 철회한다.

회귀 `test_random_only_multimodality_is_identical_across_the_warm_arms` 가
두 arm 의 블록 동일성을 고정한다.

> ⚠ 같은 F20 문구가 봉인 summary 의 `multistart._해석` 문자열에도 있다.
> `src/` 가 생성하므로 고치면 `source_digest` 가 바뀐다 — 단계 3 코드
> 라운드에서 함께 고친다. 그때까지 그 필드는 인용하지 않는다.

### 29.4 발견 5 — "코드만" 이 아니라 code + runtime drift

`정본 → nowarm_now` 를 "코드만" 이라고 쓴 것을 고쳤다. 그 사이에
Python·OS·NumPy·SciPy 도 함께 바뀌었다. 그 줄은 warm 축이 아니라 **잡음
대조**이고, 두 번째 줄(`nowarm_now → warm`)만 digest·runtime·조건집합·예산이
모두 같은 matched 짝이다. 5 mV 교차-digest 짝을 paired 밖까지 일반화하던
서술도 철회[WARM_SYSTEMATIC].

### 29.5 발견 9 — `origin/main` 반박은 내가 틀렸다

리뷰어 값이 맞다. **원인은 작업 클론이 shallow 였던 것**이다:

```
수정 전  git rev-parse --is-shallow-repository → true (경계 b7d61881, 155커밋)
         git merge-base origin/main HEAD       → (빈 출력)
git fetch --unshallow origin
수정 후  merge-base --is-ancestor origin/main HEAD → exit 0
         git merge-base origin/main HEAD           → bf0dd1a3
         git rev-list --left-right --count ...     → 0  234
         origin/main 이 조상인 브랜치              → 37 / 37
```

`BRANCHES.md` 에 정정과 원인을 적고, 재현 명령 맨 앞에 shallow 확인 단계를
넣었다. 이 문서의 모든 그래프 주장은 full clone 에서만 재현된다.

### 29.6 발견 10 / 20차 발견 11 — 실행 일관성 둘

- `wiki/tools/status.py` 는 **stdout** 이 CP949 일 때 죽었다. 입력에
  `encoding='utf-8'` 을 넣은 것으로는 안 닫혔다. 실측:
  수정 전 `PYTHONIOENCODING=cp949 python3 tools/status.py` → exit 1
  (`'cp949' codec can't encode character '—'`), 수정 후 exit 0.
  `lint.py` 는 현재 데이터에서 수정 없이도 통과했으나 같은 구조라 함께 닫았다.
  회귀 `test_wiki_tools_survive_a_cp949_console` 이 두 도구를 비-UTF8
  콘솔에서 돌린다.
- `/lean-review` 의 diff 대상이 `origin/$(git rev-parse --abbrev-ref HEAD)`
  였다. detached HEAD 에서 `--abbrev-ref HEAD` 는 문자열 `HEAD` 를 반환한다.
  upstream 을 조립하지 말고 `@{upstream}` → `origin/HEAD` 순으로 git 에게
  묻도록 고쳤다.

### 29.7 뮤테이션 검증 — 새 검사가 진짜 잡는가

새 테스트가 처음부터 통과하면 fixture 가 진실을 가린 신호다 (CLAUDE.md
규율 2). 다섯 가지를 일부러 깨뜨려 전부 실패하는 것을 확인했다:

| 변이 | 결과 |
|---|---|
| 철회 문구를 활성 본문에 되살림 | `reappear_in_active` 실패 |
| `<!-- QUARANTINE:OP_EQUIV -->` 여는 울타리 삭제 | 2건 실패 (금지어 + 양성 결속) |
| noise 반례 수치 훼손 (`304/492` → `305/492`) | `noise_layer_reversal` 실패 |
| `0.969512` 인용 삭제 | `random_only` 실패 |
| restart 표 수치 훼손 | 기존 `restart_table` 회귀 실패 |
| `status.py` 의 stdout 수정 제거 | `cp949[status.py]` 실패 |

기존 회귀 `test_p22_restart_table_matches_the_canon_outputs` 는 문구 수정
과정에서 **먼저 깨졌다** — 앵커가 옛 제목과 `restart 5` 행 이름에 걸려
있었기 때문이다. 앵커만 새 문구로 옮기고 검사(정본 대조)는 그대로 뒀다.

### 29.8 검증

```
python -m pytest tests/ -q          → 663 passed
python3 wiki/tools/lint.py          → ERRORS 0 / WARNINGS 0, exit 0
source_digest()                     → a72c0f3a485c19bb (수정 전과 동일)
```

strict smoke 는 이 라운드에서 돌리지 않았다 — `src/ tools/ configs/
scripts/ run.sh requirements*` 를 한 줄도 건드리지 않았고 `source_digest`
가 불변이라 계산 경로가 그대로다. 단계 3 코드 라운드에서 다시 돌린다.

### 29.9 남은 것 (리뷰 실행 순서 2~8)

2. 현재 warm raw fits·입력을 완전한 diagnostic bundle 로 보존 (발견 6)
3. 새 회귀를 row-level digest + normalized run_spec exact equality 로 보강 (발견 7)
4. 단계 3 schema 에 `p_ini_warm_start` / `condition_warm_start` 분리 (발견 4)
5. restart bank · freshness gate · index merge
6. 2×2 half-cell arm + nested bank prefix 를 smoke 에 작은 fixture 로
7. 한 clean source 에서 budget plateau 측정
8. claim-supporting 다리만 재실행 → 최종 정본 승격

2~8 은 전부 `source_digest` 를 바꾸므로 **기존 산출물 재실행**이 걸린다.

## 30. 21차 게이트 리뷰 회답 (2) — 행 수준 감사와 회귀 강화

> 리뷰 실행 순서 **2·3** 과 **발견 4·6·7**, Q2 를 닫는다. `source_digest` 는
> 여전히 `a72c0f3a485c19bb` — RUN_SCOPE 를 건드리지 않았다.

### 30.1 발견 6 — 원자료 없이 감사할 수 있게 만들었다

리뷰가 확인할 수 있던 것은 "문서 숫자 == summary 숫자" 뿐이었다. 원자료
(`fits.parquet`)는 다리당 수십 MB 라 git 에 못 넣는다. 리뷰가 제시한 대안인
**compact keyed projection + full digest** 를 만든다:

`docs/22p_gap/row_projection.py` (RUN_SCOPE 밖 — `leg_probe.py` 와 같은 이유)

- 열: `cond_id · objective · noise · truth(3) · hats(3) · J · abs_err_max ·
  degenerate · recoverable · 예산(2) · warm_started · converged ·
  any_bound_active · best_restart_source · restart_sources`
- 정렬 `(cond_id, objective)` · 부동소수 `repr` (왕복 보장) · 탭 구분 ·
  **압축 전 바이트의 sha256** 이 digest (gzip 수준과 무관)
- 목적함수별 **부분 digest** 도 낸다 → 33p 만 따로 대조할 수 있다
- `analysis_spec_sha256` 로 규격 자신을 못박는다
- `gzip(mtime=0)` — timestamp 만 고정한다. 같은 zlib 구현끼리는 파일 바이트도
  같았지만 **보장은 아니다** (22차 발견 6: zlib-ng 1.3.1 에서 다른 바이트).
  정본 앵커는 압축 전 sha256 이다

그리고 같은 실행에서 **재계산 검증**을 한다 — 봉인 fits 를 `src.scoring` 의
정규 경로(`add_error_columns → classify_recoverability → clean_bias →
apply_bias_correction → summarize`)로 **다시 채점**해서 커밋된 summary 와
자리별로 대조한다. 이것이 Q3 의 "복원 후 score → analyze 가 같은 값을 내는가"
에 대한 답이다.

컨테이너에 원자료가 있는 유일한 다리로 실측했다:

```
✅ paired_fixed5_v4: 6138행 · projection ad598fe77e75afec · 재계산 일치 True
   357 KB (gz) · 재실행 시 바이트 동일
```

나머지 7다리는 이 컨테이너에 원자료가 없었다. **회귀 2건이 그 산출물이 없으면
실패하도록** 걸어 뒀다 (skip 하지 않는다) — 없는 상태가 곧 리뷰의
"citation-ready 아님" 판정이고, 조용히 넘어가면 그 판정이 사라진다.

> **★ 2026-08-24 정정** — 위 문장을 쓸 때는 "작업 기계에는 있다" 였다. 그
> 기계가 교체되면서 7다리 원자료는 **어디에도 없다** (§32). 지금 그 7다리는
> `preservation_status: recorded_projection` 이고 되살릴 수 없다. 보존 상태의
> 정본은 `docs/22p_gap/LEG_PRESERVATION.yaml` 하나다.

### 30.2 발견 4 — half-cell 짝은 warm "한 축" 이 아니었다 (회귀가 독립 재현)

새로 넣은 `test_warm_pair_manifests_differ_only_by_the_warm_axis` 는 두
manifest 를 평탄화해 **화이트리스트 밖 차이를 전부 거부**한다. 화이트리스트는
실행 부산물(시각·경과·attempt id·출력 경로·fits 봉인·`run_signature`)과 warm
축뿐이며, `git_commit` 은 **`source_digest` 가 같을 때만** 허용한다.

이 테스트를 처음 돌리자 half-cell 짝에서 걸렸다:

```
p_ini.pocv_dvdq_dqdv:
  [1.509716, -0.418050, 1.087242, -0.084175]
≠ [1.518503, -0.421892, 1.063315, -0.060152]
```

리뷰 발견 4 를 **리뷰 문서를 보지 않고 재현한 것**이다. 대응은 화이트리스트
확장이 아니라 분류 변경이다:

- `_WARM_PAIRS` 에서 뺐다 → 격자 짝 하나만 남는다 (그쪽은 `p_ini=null`,
  warm 외 차이 0)
- `_CONFOUNDED_PAIRS` 로 옮기고 **교란이 실재하는지를 양성으로 검사**한다.
  목록에서 조용히 빼면 다음 판이 되돌린다. 단계 3 에서 원점을 고정해 교란이
  사라지면 이 테스트가 실패하고, 그때 승격하면 된다.
- `LEG_INVENTORY.md` §23 에 정정 블록 — `0.640625 → 0.184375` 은 (1) pristine
  `p_ini` warm 연쇄 (2) 조건별 warm 초기값 (3) adaptive 실현 예산 변화가
  합쳐진 total protocol effect 다.

### 30.3 발견 7 — 다섯 구멍

| 리뷰가 지적한 구멍 | 닫은 방법 |
|---|---|
| 1. 숫자가 문서 "어딘가" 있는지만 봤다 | `test_warm_probe_numbers_are_bound_to_keyed_table_cells` — §20.4 표를 **행 라벨로 찾아 열 위치로** 읽는다 (33p=4번째 칸, 34p=5번째 칸, warm=3번째 칸) |
| 2. protocol test 가 non-null 만 봤다 | 위 run_spec exact-match 회귀 — `adaptive`·`n_restarts`·조건집합 해시·목적함수 순서 변경을 전부 거부 |
| 3. 조건별 결과가 뒤바뀌어도 총 비율만 같으면 통과 | `test_warm_pairs_agree_row_by_row_on_the_first_objective` — 33p 부분 투영 sha256 을 통째로 비교. 34p 는 반대로 **달라야** 한다는 것도 함께 |
| 4. summary 의 fits digest ↔ manifest 봉인 미검사 | `test_warm_probe_summary_fits_digest_matches_the_manifest_seal` |
| 5. same-digest 짝의 input SHA·조건 해시·bounds·reference·optimizer·환경 exact equality 미강제 | 위 run_spec exact-match 회귀가 평탄화된 **전 키**를 본다 |

### 30.4 Q2 항목 1 — 연쇄 1번째의 warm 비접촉

이미 있었다 (`tests/test_compare.py::test_warm_start_passes_smooth_solution_to_dqdv_objectives`).
다만 목적함수 **순서 하나만** 봤다. `pocv_dvdq_dqdv` 를 맨 앞에 둔 배치를
추가했다 — 그 경우 `_has_dqdv` 는 True 인데 `seed_p` 가 아직 None 이라
여전히 기본 초기값을 써야 한다. 불변량은 "어떤 목적함수인가" 가 아니라
**연쇄 위치**에 걸려 있고, §20.4 의 warm 귀속이 기대는 것도 그쪽이다.

뮤테이션 확인: `seed_p = None` → `seed_p = list(task["init"])` 로 바꾸면
이 테스트가 실패한다 (실측). 되돌린 뒤 `source_digest` 재확인 `a72c0f3a`.

### 30.5 지금 상태 — 회귀 2건이 의도적으로 RED

```
python -m pytest tests/test_docs_lint.py -q
  → 2 failed, 44 passed
     test_warm_probe_row_projections_are_committed_and_self_consistent
     test_warm_pairs_agree_row_by_row_on_the_first_objective
```

둘 다 "행 수준 투영이 아직 커밋되지 않았다" 는 같은 이유다. 원자료가 있는
기계에서 아래를 돌려 커밋하면 닫힌다:

```bash
python docs/22p_gap/row_projection.py --all
git add docs/22p_gap/warm_probe/*.projection.*
```

투영이 붙기 전까지 warm-probe 다리들의 상태는 리뷰 Q4 분류로
**`recorded_only`** 다 — 진단·설계 근거로는 쓰되 인용 정본이 아니다.

### 30.6 8다리 전량 재계산 검증 통과 — 그리고 §22 가 행 수준으로 올라갔다

원자료가 있는 기계에서 `row_projection.py --all` 실측 (2026-08-20):

```
✅ fit_22p_seed_404_hc            1280행  cbe040612aa4415a  재계산 일치 True
✅ fit_22p_seed_404_hc_nowarm     1280행  2a2ac3072afe8bca  재계산 일치 True
✅ fit_22p_seed_404_hc_warm_now   1280행  cbe040612aa4415a  재계산 일치 True
✅ fit_seed404_pe5mv              1280행  e984cd337be13d47  재계산 일치 True
✅ fit_seed404_pe5mv_nowarm       1280행  7b3e57bdf07ca9ce  재계산 일치 True
✅ paired_fixed5_v4               6138행  ad598fe77e75afec  재계산 일치 True
✅ paired_fixed5_v4_nowarm_now    6138행  8382ff247e2b5410  재계산 일치 True
✅ paired_fixed5_v4_warm          6138행  267558a1d3088e4e  재계산 일치 True
```

**여덟 다리 전부 봉인 summary 가 원자료에서 자리별로 재현된다.** 발견 6 이
"확인할 수 없다" 고 적은 세 줄 중 첫 줄(`봉인 fits 를 직접 재계산한 summary ==
커밋된 summary`)이 닫혔다.

그리고 예상하지 않은 것이 하나 나왔다:

```
fit_22p_seed_404_hc          (7250c6e6)  cbe040612aa4415a
fit_22p_seed_404_hc_warm_now (a72c0f3a)  cbe040612aa4415a   ← 완전 동일
```

digest 가 다른 두 다리의 **1280행 × 20열이 바이트 단위로 같다.**
`LEG_INVENTORY.md` §22 는 이 주장을 aggregate 네 값으로만 세웠는데 — 그리고
aggregate 일치는 조건별 일치가 아니라는 것이 21차 Q2 의 지적이었다 — 이제
행 수준 근거가 붙었다. §22 에 정정 블록을 넣고 회귀
`test_cross_digest_exact_pair_reproduces_row_for_row` 로 고정했다.

범위는 좁게 적는다: **이 다리의 경로에서 불활성**이지 그 코드 구간이 어디서나
무해하다는 뜻이 아니다. 5 mV 짝은 여기 해당하지 않는다 (warm 축이 함께 다르다
— 발견 5).

### 30.7 투영 digest 가 교차 기계에서 재현된다 (gzip 바이트는 별개 — §30.7.1)

투영 digest 가 감사 앵커로 쓸 수 있으려면, 원자료를 가진 제3자가 같은 값을
독립적으로 얻어야 한다. 두 기계에서 실측했다.

| | 기계 A (로컬 WSL) | 기계 B (리뷰 컨테이너) |
|---|---|---|
| 입력 `fits.parquet` sha256 | `e033b19510ddbed9…` | `e033b19510ddbed9…` (manifest 봉인과 일치) |
| 투영 digest | `ad598fe77e75afec` | `ad598fe77e75afec` |
| 커밋 바이트 | — | `git status` 변경 0 |
| 전체 테스트 | 674 passed | 674 passed |

기계 A 가 `--all` 로 재생성한 `paired_fixed5_v4.projection.csv.gz` 는 기계 B 가
먼저 만들어 커밋한 파일과 **바이트 단위로 같아** git 이 변경으로 잡지 않았다.
반대 방향(B 가 A 의 커밋 위에서 재생성)도 같다.

**이것이 말하는 것**: 투영 직렬화와 채점 재계산이 기계에 의존하지 않는다.
고정 열 순서 · `(cond_id, objective)` 정렬 · `repr` 부동소수가 의도대로
동작한다. 따라서 `projection_sha256`(= **압축 전** canonical TSV 의 sha256)은
원자료를 가진 누구든 독립 검산할 수 있는 앵커다.

#### 30.7.1 ★ 정정 (22차 리뷰 발견 6) — `gzip(mtime=0)` 은 바이트 동일을 보장하지 않는다

> **압축 전 digest 는 재현되지만 gzip 파일 바이트는 zlib 구현에 달렸다.**
> 위 두 기계는 둘 다 zlib 1.3 이었다. 리뷰어 환경(Python 3.14.0 · **zlib-ng
> 1.3.1**)에서 같은 옵션으로 재압축하면 **다른 바이트**가 나온다:
>
> ```
> committed gzip   357,509 bytes
> recompressed     359,210 bytes   (first difference offset 44)
> uncompressed SHA ad598fe77e75afec…  ← 동일
> ```
>
> `mtime=0` 은 timestamp 만 고정하고 deflate 구현 차이는 고정하지 않는다.
> 우리 컨테이너(zlib 1.3)에서는 재압축 바이트가 같았다 — **환경이 같아서**이지
> 보장이 아니었다.
>
> 방어 가능한 서술은 이것뿐이다: **정본 앵커는 압축 전 canonical TSV 의
> sha256 이고, 시험한 두 zlib 1.3 환경에서는 gzip 파일까지 같았다.**
> 설계는 원래 압축 전 digest 를 앵커로 삼았으므로 감사 능력은 그대로다 —
> 틀렸던 것은 "바이트까지 재현된다" 는 **주장의 범위**다.

**말하지 않는 것**: fitting 자체가 기계 독립이라는 뜻은 아니다. 두 기계가 쓴
`fits.parquet` 은 **같은 파일**이다 (sha256 일치). 재실행의 재현성은 별개
문제이고, 21차 발견 5 가 지적한 runtime drift 는 그쪽에 걸린다.

## 31. 22차 게이트 리뷰 회답 — 발견 1·5·6·7·8 + 계약 v2

> 리뷰 대상 `db19a7b1` · 판정 **NO-GO** (21차 10건 미완결 + 계약 구현 불가).
> `source_digest` 는 `a72c0f3a485c19bb` 그대로.

### 31.1 발견 1 — 21차 실험은 union 이 아니라 slot 교체였다

가장 큰 정정이다. §20.4·계약 v1·21차 회답이 전부 이 틀린 전제 위에 있었다.
근거는 코드와 **우리가 커밋한 투영** 둘 다다 (§20.4 재재정정 참조).

무엇이 바뀌나: 34p 개선을 "warm 후보가 좋다" 로만 읽을 수 없고 **"`base_init`
이 34p 에서 나쁜 후보였다"** 와 구별되지 않는다. 계약 §3 이 후보 정책을 세
가지로 나눠 이름 붙였고, 21차 실험은 `legacy_slot_replace` 다.

회귀 `test_warm_replaces_the_deterministic_slot_it_does_not_add_one` 은 문장이
아니라 **실제 후보 배열**(`restart_sources`·총 후보 수·`base_init` 소멸)을
고정한다.

### 31.2 발견 5 — 투영 v2

| 리뷰 지적 | 대응 |
|---|---|
| 실제 fits SHA 를 계산하지 않고 manifest 값을 복사 | 읽은 바이트를 해시해 **summary·manifest 와 삼중 대조** |
| `재계산_검증` 이 `by_objective` 숫자만 부분 순회 | 봉인 summary **전체**를 재귀 비교 (key 집합·`by_objective_noise`·`overall_recoverable`·`restart_conditioned`·`multistart*`·문자열·불리언) |
| restart trace 지표를 재계산하지 않음 | `multistart` 블록 재계산 경로 추가 |
| per-restart 자료 없음 | `<leg>.restarts.csv.gz` — `(cond_id, objective, i, source, J, p0..p3, warm)` |
| 분석기 provenance 없음 | `analyzer` 블록 |
| malformed 입력을 조용히 통과 | 중복 키·비유한값·읽기 실패 시 **즉시 실패** |

**전면 대조가 곧바로 구멍을 드러냈다**: `multistart`·`multistart_random_only`
는 `summarize()` 산물이 아니라 `run_scoring` 이 `restarts_json` 에서 붙이는
블록이다. 초판 재계산은 그 둘을 통째로 못 봤고, **발견 3 의 근거가 바로 그
블록**이었다.

그리고 restart 투영으로 random-only 다봉성을 **원자료 없이** 재계산해 봉인값과
마지막 자리까지 맞췄다 (회귀
`test_random_only_multimodality_is_recomputable_from_the_restart_projection`).

8다리 전량 실측 (2026-08-20, 당시 원자료가 살아 있던 기계 — 그 기계는 §32
에서 사라졌다. 아래는 그때의 영수증이며 지금 재현할 수 있는 것은
`paired_fixed5_v4` 뿐이다):

```
전체 True · by_obj True · fits삼중 True · 봉인일치 True  ×8
투영 내용 digest 일치 ×8 · restart 투영 digest 일치 ×8
```

### 31.3 발견 6 — gzip 바이트 주장의 범위

리뷰어 환경(Python 3.14.0 · zlib-ng 1.3.1)에서 재압축하면 `357,509 →
359,210` 으로 갈린다. **압축 전 SHA 는 동일**하다. 우리 두 환경이 같았던 것은
둘 다 zlib 1.3 이어서였다. 정본 앵커를 압축 전 canonical TSV SHA 로 한정했다 —
설계는 원래 그랬고, 틀렸던 것은 **주장의 범위**다.

### 31.4 발견 7 — 원장의 세 구멍, 그리고 fence 가 잡은 진짜 버그

(a) `MV_1P5`·`THRESH_FREE`·`FPR_AS_FDR` 이 문서에 있는데 원장에 없었다 →
추가 + **파일→원장 방향** 완전성 검사.

(b) fence 균형 검사를 넣자마자 **이미 일어난 사고**를 잡았다:

```
08_REVIEW_RESPONSE.md:1831  | `<!-- QUARANTINE:ID -->` … | 옛 문장을 …
   ↑ §29.1 설명 표의 인용이 여는 울타리로 파싱됐다
   → 1831줄 이후 문서 전체가 금지어 검사에서 빠져 있었고
   → 그 안에 금지어 4개가 살아 있었다
```

파서를 **"줄 전체가 마커 하나일 때만"** 으로 고쳤다. 리뷰가 예측한 실패 모드가
예측대로 이미 발생해 있었다.

(c) wiki 가 원장 관할 밖이었다 → 관할에 포함. 활성 잔여 **8곳** 정리
(09 2건 · 08 3건 · `LEG_INVENTORY` 2건 · wiki 1건 — 초판은 여기 6곳이라고
적었는데 열거한 항목의 합과 안 맞았다. 23차 리뷰가 지적).

**★ 원장 regex 도 세 번 틀렸다.** `3/51` 이 실측 붕괴 건수를, `THRESH_FREE` 의
두 패턴이 **배너가 명시적으로 유지한다고 적은 문장**을 잡았다 (§0 의 "판정선을
어디에 두든 고칠 수 없다" 는 정반대 주장이다). 원장이 참인 문장을 금지하면
문서를 거짓으로 만든다 — "금지어는 인접 단어가 아니라 **철회된 의미**에
묶어라" 를 원장 헤더 규칙으로 박았다.

### 31.5 발견 8 — `/lean-review`

upstream 조회 실패 시 `origin/HEAD` 로 자동 대체하던 것을 없애고 **중단**한다.
회귀는 attached+upstream / attached+no-upstream / detached / 명시 base 네
상태를 진짜 git 저장소로 만들어 검증한다.

### 31.6 자체 발견 — 분석기 provenance 가 갈려 있었다

8다리 검산 중 `row_projection_py_sha256` 이 두 값으로 갈린 것을 발견했다
(7다리 `b46389d0` · `paired_fixed5_v4` `5711f104`). 확인해 보니 **차이는
`main()` 의 출력 문구뿐**이고 계산 함수 여섯 개는 바이트 동일이었다. 그러나
리뷰어는 sha 만 보고 그것을 알 수 없다 — 비교 집합의 "같은 규격으로 만들었다"
전제가 흔들린다.

파일 전체 대신 **계산 경로만** 해시하도록 바꿨다 (`compute_sha256` — 계산
함수 여섯 개의 source + `COLUMNS`·`RESTART_COLUMNS`·`ANALYSIS_SPEC`). 표시
코드를 고쳐도 안 흔들리고, 계산이 바뀌면 반드시 흔들린다.
`analysis_spec_sha256` 이 **무엇을 만들기로 했는가**라면 이것은 **무엇이
만들었는가**다. 회귀 `test_all_projections_share_one_compute_provenance` 가
비교 집합 전체의 동일성을 강제한다.

### 31.7 계약 v2

발견 1·2·3·4 와 Q1~Q6 을 반영해 전면 개정했다 —
`docs/22p_gap/STAGE3_CONTRACT.md`. 요지:

| 절 | 무엇이 바뀌었나 |
|---|---|
| §0 | v1 의 union 오분류 정정 |
| §2 | 예산을 **목적함수별**로 (33p 예산이 34p warm 후보를 끌고 간다) · `warm_provider_map` · `realized_candidate_map_sha256` · `N` 의 정의 1회 |
| §2.1 | 하위호환을 **version-dispatched read-only** 로 완화 (Q3 — v1 의 전면 거부는 과했다) |
| §2.2 | adaptive diagnostic arm 의 표현 가능한 schema |
| §3 | 후보 정책 3종. `equal-cost` → **`equal_start_count`** (시작점 수가 같아도 `n_eval` 이 다르다) |
| §4 | pair id 를 **행 단위**로 · `pairing_design_id` · unit cube bank · **exact ordered bounds digest** (Q1) |
| §6 | plateau 를 진짜 truth-free 로 — `degenerate` 전이·`p` 이동·restart-source 승자 구성을 gate 에서 빼고 민감도 표로. **sentinel panel** 도입 (Q2) |
| §7 | primary = grid reference 의 optimizer-controlled paired contrast + **transition table** (Q4) |
| §9 | 재실행 목록에 seed 별 0 mV control·grid sentinel·비-PE 다리·hard/noisy sentinel·후보 정책 arm 추가. **12시간 추정 폐기** (Q5) |
| §10 | 보존 단위 (Q6) |

### 31.8 남은 것

계약 §2·§4·§6 은 **정의만 있고 구현이 없다.** 리뷰 순서로 11번(문서·회귀
재심사)이 지금이고, 12번(RUN_SCOPE 변경 → `source_digest` 변화 → 재실행)은
그 뒤다. 비용은 재산정 전까지 승인 요청하지 않는다 (§9.3).

## 32. 작업 기계 교체로 원자료 7다리 손실 — 그리고 정본 한 다리의 완전 검증

> 2026-08-24. 문서 라운드 중 작업 환경이 바뀌면서 `results/` 가 사라졌다.
> 이 절은 **무엇이 남고 무엇이 사라졌는지의 정본**이다. 기계로 읽는 형태는
> `docs/22p_gap/LEG_PRESERVATION.yaml`.

### 32.1 무슨 일이 있었나

작업 기계가 교체됐다 (`DESKTOP-K1BLBIJ`/`yonghoon` → `DESKTOP-IK8J81H`/
`yonghoon71`). 옛 기계의 WSL 홈에 있던 `degradation-degeneracy/results/`
(1.9 GB, 73 디렉터리)는 git 밖이라 함께 사라졌다.

네 곳을 전수 조사했다 — 새 WSL 홈 · D 드라이브 2곳 · C 드라이브. **8다리 중
하나만 살아남았다.**

### 32.2 `paired_fixed5_v4` — 완전 bundle 복구 + 34검사 통과

2026-08-16 백업(`v4_run_extras`)에서 복구했다. 실측:

```
복구본 sha256  e033b19510ddbed951cfebe7e28793f19c5f0da915268b0731a30c56f0b3b064
manifest 봉인  동일  ✅
동봉  _inputs/ · attempts/ · fit_chunks/ · manifest.yaml · provenance.json
```

`_inputs/` 까지 있어 **축약본이 아니라 완전 bundle** 이다. 그래서 21차 발견 6
이 "확인할 수 없다" 고 적은 세 번째 줄을 이 다리에서 실제로 돌렸다:

```
$ validate_provenance('results/paired_fixed5_v4')
ok      : True
검사 수 : 34
실패    : []

  ✅ 출력봉인_재계산    ✅ 입력_digest_재해시   ✅ 조건집합_서명일치
  ✅ run_signature_재계산  ✅ 곡선_producer_재검  ✅ 코드_identity
  ✅ 입력봉인_교차일치   ✅ 입력_스냅샷        ✅ restart_예산_완주
  … (34/34 통과)
```

**검사기가 실제로 실패를 잡는지도 확인했다** (변이 시험). fits 중간 바이트를
1비트 뒤집으면:

```
변이본 sha  e07032f5…  (원본 e033b195…)
ok: False
실패한 검사: ['출력봉인_재계산', 'restart_출처', 'restart_예산_완주']
```

즉 `fail: []` 는 검사가 안 돈 것이 아니라 **34건이 돌아서 전부 통과한 것**이다.

투영도 **세 번째 기계**에서 바이트 동일하게 재생성됐다 (WSL2/py3.12 →
컨테이너/py3.11 → 새 WSL2/py3.12, 전부 `ad598fe77e75afec`).

곁들여 `grid_curves_v4`(봉인 입력 곡선) · `grid_fit_v4` · `halfcell_fit_v4`
도 복구됐다. 계약 §9 가 "producer identity 가 불변이면 곡선을 재사용한다
(재생성 ~28분 절약)" 고 적은 그 곡선이 실물로 있다.

### 32.3 warm 실험 7다리 — 손실

2026-08-20 에 만든 것들이라 8/16 백업 이후다. 네 곳 어디에도 없다.

```
paired_fixed5_v4_nowarm_now · paired_fixed5_v4_warm
fit_22p_seed_404_hc · _nowarm · _warm_now
fit_seed404_pe5mv · _nowarm
```

**안 바뀌는 것** (커밋된 투영에서 전부 재계산된다):

| 근거 | 어디서 |
|---|---|
| 전이표 `131/436/55/854` · `381/186/167/742` | 행 투영 |
| 후보 구성 (`base_init` → `warm` slot 교체) | restart 투영 |
| random-only 다봉성 `0.969512` | restart 투영 |
| summary·manifest·투영 digest 자기정합 | 커밋된 파일 |

**바뀌는 것**:

- 7다리는 투영을 **원자료에서 다시 만들 수 없다** → 영구 `diagnostic`
- `validate_provenance` 영구 불가
- 투영에 없는 열(`p_spread`·경계 플래그 세부·`restarts_json` 전문) 영구 손실
- 계약 §9 의 재실행에서 그 7다리는 "재실행" 이 아니라 **"새로 생성"**

### 32.4 계약 §8 의 3축이 여기서 실증됐다

23차 P0-6 이 단일 `inference_status` 를 셋으로 나누라고 했다. 지금 상태가
정확히 그 이유다 — 단일 축으로는 "원자료가 없지만 투영은 검증된" 상태를 못 적는다.

| 다리 | `preservation_status` | `validation_status` | `inference_role` |
|---|---|---|---|
| `paired_fixed5_v4` | `full_bundle` | `historical_validated` | `diagnostic` |
| 나머지 7 | `recorded_projection` | `unvalidated` | `diagnostic` / `confounded` |

> **★ 2026-08-24 정정 (24차 보충 리뷰)** — 이 표의 초판은 `current_validated` ·
> `canonical_candidate` · `missing` 이었다. 셋 다 틀렸다.
> · `canonical_candidate` 는 **계약 §8 에 없는 값**이다. 계약을 고치지 않고
>   원장과 회귀가 만들어 두 번째 authority 가 생겼다 — 직전 라운드 Q5 가
>   경고한 것이 같은 커밋에서 재발했다.
> · `current_validated` 도 틀렸다. 이 다리의 run_spec 은
>   `source_digest: d50295f980ccaa81` 로 현행 `a72c0f3a485c19bb` 가 아니고,
>   `코드_identity` 검사는 (`src/io.py:1514`) run_spec 이 digest 를 갖고 dirty
>   가 아닌지만 본다 — 현행 트리와의 일치는 보지 않는다.
> · 7다리는 `missing` 이 아니라 `recorded_projection` 이다. 계약 §8 이 그
>   상태에 이미 칸을 갖고 있었는데 안 쓰고 더 센 말을 골랐다.
>
> 정본은 `docs/22p_gap/LEG_PRESERVATION.yaml` (schema 2) 이고, 회귀는 3축
> enum 을 계약에서 파싱한다.

### 32.5 교훈 — 도구가 없었던 게 아니라 **강제가 없었다**

> **★ 2026-08-24 정정 (24차 보충 리뷰)** — 이 절의 초판은 "23차 Q6 의 보존
> 단위 구현을 미룬 대가" 라고 적었다. **원인 진단이 틀렸다.**

보존 체계는 이미 있었다:

| 있던 것 | 증거 |
|---|---|
| `tools/archive_bundle.py` | 6차 F62 → 7차 F71, fail-closed·payload digest·원자적 교체 |
| `scripts/archive_results.sh` | 묶음 생성 wrapper |
| git `artifacts/` | `artifacts/paired_fixed5_v4/` 26파일 · 23,863,555 B 가 저장소 안에 있다 |
| 그것이 **작동했다** | `python -m tools.archive_bundle check artifacts/paired_fixed5_v4` → 불일치 0 |

`paired_fixed5_v4` 가 살아남은 이유가 백업 운뿐이 아니다 — 그 다리는 이
체계를 **통과했다**. 8월 20일 warm 다리 7개는 통과하지 않았다.

따라서 실패는 도구 부재가 아니라 **coverage·운영** 문제다: 다리를 만들고
보존 없이 끝낼 수 있었다. 계약 v4 가 고칠 것은 "보존 도구를 만든다" 가 아니라
**"보존 영수증 없이는 leg_index 등록이 실패한다"** — 트랜잭션으로 만드는 것이다
(계약 v4 **묶음 9**). 23차 Q6 의 권고 자체는 여전히 유효하지만, 그것은 외부
저장소 이야기이고 이번 사고를 막았을 것은 **필수 gate** 쪽이다.

### 32.6 부수 발견 — `validate_provenance` 가 깨진 parquet 에서 예외로 죽는다

footer 를 깨면 `pd.read_parquet` 이 먼저 죽어 `ArrowInvalid` 가 그대로
올라온다 (`src/io.py:1676`). 조용히 통과하는 것이 아니라 fail-hard 라 안전
쪽이지만, 함수 계약은 `{"ok":…, "fail":[…]}` 를 돌려준다고 적혀 있다.
**깨진 파일을 "발견" 으로 보고하지 못하는 구멍**이다.

`src/` 라 지금 고치면 `source_digest` 가 바뀐다 → 단계 3 항목으로 이월
(계약 §9.4 에 추가). 파싱 가능한 손상은 정상적으로 `출력봉인_재계산` 실패를
낸다는 것은 위 변이 시험으로 확인했다.

## 33. 24차 **보충** 리뷰 대응 — 보존 원장을 계약 안으로 되돌린다

> 2026-08-24. 보충 응답 `0ca48cbf` 에 대한 재검증이 NO-GO 로 돌아왔다.
> 판정 자체는 받아들인다. 원자료 손실을 공개하고 보존을 앞으로 당긴 결정은
> 수용됐지만, **그 결정을 담은 원장이 계약을 위반했다.**

### 33.1 무엇이 틀렸나 — 한 문장

계약에 없는 상태값을 만들고, 그것을 통과시키려고 **회귀에 enum 을 하나 더
적었다.** 계약을 고친 것이 아니라 회귀를 두 번째 authority 로 만든 것이다.
직전 라운드 Q5 가 "구조적 literal 의 독립 복제" 를 경고했는데 **같은 커밋에서**
재발했다.

### 33.2 발견별 대응

| # | 발견 | 대응 | 증거 |
|---|---|---|---|
| 1 | `canonical_candidate` 가 계약 enum 밖 | 값을 버렸다. 회귀가 enum 을 **계약에서 파싱**한다 | `test_status_axis_enums_have_exactly_one_authority` — 계약 밖 상태 literal 이 회귀 파일에 있으면 실패 |
| 2 | 7다리는 `missing` 이 아니라 `recorded_projection` | 재분류 | 계약 §8 정의 그대로 |
| 3 | v5 artifact 를 `current_validated/canonical_candidate` 로 적었다 | `full_bundle / historical_validated / diagnostic` + `claim_roles` 로 claim 별 role 분리 | `LEG_PRESERVATION.yaml` |
| 4 | 보존 원장이 bundle 위치·SHA·크기·receipt·validator 를 결속 안 함 | `evidence` 블록 + 회귀가 **디스크에서 재계산** | `test_full_bundle_claims_are_backed_by_a_real_bundle` |
| 5-1 | 회귀가 불가능한 튜플·중복 ID 를 통과시킴 | 계약 §8 에 **허용 조합표**, 회귀가 그것을 읽는다 | `test_registry_rejects_impossible_status_tuples` |
| 5-2 | 되살릴 수 있다는 문구를 막겠다던 테스트가 정작 그 문구를 검색 안 함 | 두 테스트를 하나로 합치고 금지 문구 검색을 넣었다 | `test_docs_do_not_claim_lost_legs_are_regenerable` |
| 6 | CI 가 잃은 다리에 재생성을 강요 (충족 불가) | 세대 pin + `regeneration_capability` 분기 | `projection_generation_pin`, `test_analyzer_change_breaks_the_comparison_set_loudly` |
| 7 | "보존을 앞으로" 가 다른 문서에 반영 안 됨 | 4개 문서 stale 정정 + digest 동결 시점 명시 | 계약 §11, 요청문 §0·§7·§10 |
| 8 | `validate_provenance` 가 깨진 parquet 에서 예외 | 수용 조건을 **strict xfail** 로 지금 적어 뒀다 | `test_validate_provenance_reports_a_corrupt_fits_as_a_finding` |
| 9 | contract v4 여섯 묶음 미구현 | 열 묶음을 계약 §13 에 원장화. 7·10 은 닫았고 8 은 부분, 9 는 다음 라운드 본체 | 계약 §13 |

### 33.3 원인 진단을 뒤집었다 — 도구는 있었다

초판이 "보존 단위를 안 세워서 잃었다" 고 적은 것은 **틀렸다.** 리뷰가
바로잡은 대로 확인했다:

```
$ python -m tools.archive_bundle check artifacts/paired_fixed5_v4
검증 가능: 필요한 파일이 모두 있고 digest가 일치한다

$ git ls-files artifacts/paired_fixed5_v4/ | wc -l
26
```

`tools/archive_bundle.py` 는 6차 F62 → 7차 F71 로 fail-closed 까지 갖췄고,
`paired_fixed5_v4` 에서 **실제로 작동했다.** 8월 20일 warm 다리 7개는 그 체계를
통과하지 않았을 뿐이다. 실패는 도구 부재가 아니라 **강제 부재**다 — 다리를
만들고 보존 없이 끝낼 수 있었다. 그래서 계약 v4 묶음 9 는 "보존 도구를
만든다" 가 아니라 **"보존 영수증 없이는 등록이 실패한다"** 로 적었다.

### 33.4 `paired_fixed5_v4` 를 이 컨테이너에서 다시 검증했다

사용자 기계(py3.12)의 결과를 옮겨 적지 않고, 컨테이너(py3.11)에서 직접 돌려
영수증을 커밋했다:

```
validator_source_digest: a72c0f3a485c19bb
python: 3.11.15
ok: True
fail: []
n_checks: 34
```

정본은 `docs/22p_gap/receipts/paired_fixed5_v4.validate.txt` 이고, 원장이 그
파일의 sha256 을 들고 있으며, 회귀가 매번 다시 해시한다.

**다만 이것이 `current_validated` 를 뜻하지 않는다.** 이 다리의 run_spec 은
`source_digest: d50295f980ccaa81` 이고 `코드_identity` 검사는
(`src/io.py:1514`) run_spec 이 digest 를 갖고 dirty 가 아닌지만 본다 — 현행
트리와의 일치를 보지 않는다. 리뷰가 지적한 그대로 `historical_validated` 다.

### 33.5 변이 시험 — 리뷰가 준 반례 다섯을 전부 재현했다

새 회귀가 fixture 에 가려져 있지 않은지 확인했다. 각 변이 후 복원했다.

| 변이 | 결과 |
|---|---|
| `bundle_uri` 를 없는 경로로 | `묶음 경로가 없다` 로 실패 |
| `recorded_projection / current_validated / canonical` | 허용 조합표 위반 + 검증근거 없음, 둘 다 실패 |
| `missing / unvalidated / canonical` | 허용 조합표 위반으로 실패 |
| 같은 `leg_id` 두 번 등록 | `중복 등록됐다` 로 실패 |
| 영수증의 `ok: True` → `ok: False` | sha 불일치 + "통과를 말하지 않는다" 둘 다 실패 |
| 회귀 파일에 `canonical_candidate` literal 재도입 | 계약 밖 토큰으로 실패 |
| `row_projection.py` **계산 경로** 변경 | 원자료 있는 다리만 stale, 잃은 7다리는 무사 · 교차비교 선언 강제로 실패 |
| `row_projection.py` **주석만** 변경 | 교차비교는 무사 (계산 축만 본다) |

마지막 두 줄이 발견 6 의 핵심이다 — 트랩은 사라졌고 낡음 감시는 남았다.

### 33.6 닫지 못한 것

| 묶음 | 상태 | 왜 |
|---|---|---|
| 1~6 (24차) | **미착수** | 전부 `src/`·새 schema 구현이다. RUN_SCOPE 를 건드리므로 계약 재심사 후 |
| 8 immutable index | **부분** | bundle URI·SHA·크기·validator 는 결속했다. **score/analyze 산출 digest 를 묶은 영수증**과 비-git backend URI 형식이 없다 (보충 발견 4) |
| 9 트랜잭션 gate | **미착수** | 다음 라운드의 본체. 원장 coverage 가 아직 커밋된 투영 기준이라 실행 **전** 강제가 안 된다 — 계약 §13.4 에 명시 |
| Q2 canonical design | **미착수** | canonical bytes·arm registry·serialization/hash domain·golden vector 필요 |

Q1·Q3·Q4·Q5 회신은 전부 수용한다. Q5("literal audit 지금") 는 이번 라운드에서
상태 enum 축을 단일 authority 로 만드는 것으로 착수했고, schema version·step
number·target SHA·receipt field 축은 남았다.

## 34. 25차 (2차 보충) 리뷰 대응 — 보존 트랜잭션을 실제로 만든다

> 2026-08-25. 판정은 **묶음 9 설계·구현 착수 조건부 GO / 묶음 9 완료·새 leg
> 실행 NO-GO**. 선행조건 10건이 붙었고 그것을 닫는다. 이 라운드에서 처음으로
> **RUN_SCOPE 를 건드린다** — `source_digest` 가 `a72c0f3a485c19bb` →
> `0b9fb0d4519d34ae` 로 움직였다.

### 34.1 이번 라운드가 뒤집은 두 가지

**(1) 회귀가 만든 트랩을 회귀로 풀었다.** 24차 보충에서 "원자료를 잃은 다리는
기록된 세대 바이트에 대고 검사한다" 로 고쳤는데, 25차가 **그것으로는 부족하다**
고 지적했다. 다른 세 회귀가 여전히 여덟 투영을 전역 하나로 묶고 있어서,
analyzer 를 고치면 어느 쪽으로도 suite 를 만족시킬 수 없었다:

```
살아 있는 다리를 옛 투영 그대로 둔다   → current-tree equality 실패
살아 있는 다리만 새 analyzer 로 재생성  → 전역 pin · 단일 세대 equality 실패
```

`comparison_set_status` 를 바꿔도 저 셋은 해제되지 않는다. 맞다. **cohort** 로
나눴다 — g1(8다리, frozen) · g2(1다리, active). 새 세대는 새 경로에 쓰고 옛
바이트를 덮지 않는다.

**(2) 계산 digest 가 계산 의미를 빠뜨리고 있었다.** `_RESTART_SOURCES` 는
`_restart_list()` 의 허용·거부를 정하는데 `compute_sha256` 밖에 있었다. 허용
목록에 값을 하나 더해도 digest 가 안 움직이고, breaker 는 파일 전체 SHA 를
일부러 제외하므로 교차비교도 `intact` 로 남는다 — **의미가 바뀌었는데 아무 것도
안 깨진다.** 손으로 고른 목록을 **dependency closure** 로 바꿨다.

이 둘을 고친 뒤 `paired_fixed5_v4` 를 새 cohort 에 재생성한 결과가 중요하다:

| | g1 | g2 |
|---|---|---|
| `projection_sha256` | `ad598fe7…` | **동일** |
| `restart_projection_sha256` | `84333ad3…` | **동일** |
| `analysis_spec_sha256` · `fits_sha256` | | **동일** |
| `compute_sha256` | `73c1ac4b…` | `1c36a92f…` |
| `row_projection_py_sha256` | `bbb47442…` | `923ba02d…` |

**내용은 그대로고 identity 회계만 엄격해졌다.** digest 수정이 계산을 바꾸지
않았다는 직접 증거다. (g1 은 py3.12.3/numpy 2.5.2, g2 는 py3.11.15/numpy 2.4.6
에서 만들었다 — runtime 이 equality 축이 아니라는 것도 같이 실측됐다.)

### 34.2 발견별 대응

| # | 발견 | 대응 | 검사 |
|---|---|---|---|
| 1 | historical dispatch 가 여전히 충족 불가능 | cohort 로 분리 (frozen/active) | `test_every_projection_matches_its_own_cohort_pin` 외 3건 |
| 2 | `compute_sha256` 가 계산 의미를 빠뜨림 | dependency closure | `test_compute_digest_moves_when_a_constant_the_compute_path_reads_moves` + 반대 방향 1건 |
| 3 | "실물 검사" 가 같은 크기 손상을 놓침 | `archive_bundle.check()` 를 **호출**해 전수 재해시 | `test_full_bundle_payload_members_are_rehashed_one_by_one` |
| 4 | 영수증이 재생 불가·결속 없음 | `make_receipt.py` — 빈 root 복원 + 재채점 + 두 digest, core/stamp 분리 | `test_full_bundle_claims_are_backed_by_a_real_bundle` (구조 파싱) |
| 5 | 허용표가 정상 상태를 빠뜨림 | 열거 → **제약에서 생성**, 계획 다리 분리 | `_allowed_combos` · `test_preservation_registry_holds_executed_legs_only` |
| 6 | `claim_roles` 가 자유문장 | `CLAIM_STATUS.active_claims` + role enum + 세대 | `test_claim_roles_are_a_machine_contract_not_free_prose` |
| 7 | 묶음 9 트랜잭션 미정의 | `tools/preserve.py` two-phase + 실패 17종 | `tests/test_preserve.py` 26건 |
| 8 | smoke 가 실행 승인을 발행 | 문구 제거 + 보존 gate 미완료 경고 | 실행 출력 |
| 9 | xfail 이 실패 원인을 넓게 삼킴 | 손상 뒤 `ArrowInvalid` 에만 한정 | 전제 파괴 변이 = 정상 FAIL 확인 |
| 10 | committed 요청문 stale | 묶음 번호 3→9, 옛 상태 tuple 철회 표기 | `test_docs_do_not_claim_lost_legs_are_regenerable` 외 |

### 34.3 묶음 2 를 앞당겼다 (Q3)

리뷰가 "묶음 9 는 planned leg index 를 key 로 쓰므로 묶음 2 가 먼저" 라고
답했다. `tools/design_wire.py` + `tools/design_golden.yaml`:

- **arm registry** 가 계약 §5 의 2×2 와 회귀로 묶였다 (표와 코드가 갈리면 실패)
- **좌표에 이진 float 를 금지**하고 십진 문자열만 받는다
- 십진 **정규화** — 초판 golden 이 `0.17` 과 `0.170` 을 **다른 조건**으로
  갈랐다. 그것을 보고 고쳤다. 계약 §4.2 가 경고한 "조용한 merge/split" 의
  숫자판이다
- ID 사슬 `pair_group_id → bank_id → candidate_id` 를 golden vector 로 고정.
  arm registry 를 한 글자 고치거나 직렬화 구분자를 바꾸면 golden 이 깨진다
  (변이 2종 확인)

### 34.4 묶음 9 — 무엇을 만들었고 무엇이 아직 아닌가

`tools/preserve.py` 의 불변식은 하나다: **어느 단계에서 멈추든 public index 는
오염되지 않는다.** 실패 17종을 주입해 전부 확인했다 (계약 §13.2 표).

**아직 "닫음" 이 아닌 이유 셋:**

1. `run.sh`·smoke 의 **필수 gate 로 배선되지 않았다.** 호출하지 않으면 그만이고,
   그것이 정확히 8월 20일 사고의 형태다.
2. 실제 운영 backend canary 가 없다. Q1 대로 local `file+cas://` 로 트랜잭션
   **의미**만 검증했다.
3. `planned_leg_index` 가 실제 leg 원장과 결속되지 않았다 (묶음 1·6 필요).

### 34.5 스스로 찾은 것 — 영수증이 조용히 낡았다

`tools/` 에 파일을 더하자 `source_digest` 가 또 움직였고 (`73c67903` →
`0b9fb0d4`), 커밋된 영수증은 옛 digest 를 들고 있었다. **그런데 회귀가
통과했다** — 영수증과 원장을 서로 비교하기만 했기 때문이다. 24차 보충 발견 5-1
이 지적한 형태가 새 파일에서 재발한 것이다.

영수증이 **현행 검증기**보다 낡으면 실패하도록 고쳤다. 그 뒤 재생성했고,
dirty 트리와 clean 트리에서 만든 core sha 가 `f0bae903e015a177` 로 **같다** —
core/stamp 분리가 의도대로 동작한다는 증거다.

### 34.6 계약 v4 §13 — "닫음" 판정을 전부 철회

초판이 묶음 7·10 을 "닫았다" 고 적었고 리뷰가 둘 다 반례를 냈다. §13 은 이제
**미착수 / 부분** 둘만 쓴다. 닫힘 판정은 리뷰가 한다.

## 35. 26차 리뷰 대응 — 내가 통과한다고 적은 것 둘이 실제로는 거짓이었다

> 2026-08-25. 판정은 **선행조건 3건 닫힘 / 4건 부분 / 3건 미결**, 묶음 9 배선과
> 묶음 2 동결은 NO-GO. 리뷰가 P0 로 지목한 둘은 전부 **false-green** 이었고,
> 둘 다 내가 §34 에서 "확인했다" 고 적은 항목이다.

### 35.1 무엇이 거짓이었나

**(1) "빈 root 로 복원해 검증했다" — 복원이 CAS 를 안 봤다.**

`run_transaction()` 은 member 와 manifest 를 CAS 에 넣고 `read_back()` 으로
되읽기까지 했다. 그런데 **되읽은 bytes 를 해시만 확인하고 버렸다.** 실제 복원은
이 줄이었다:

```python
hooks.restore(man, run_dir, root)     # ← source 가 보존 전 **원본**이다
```

리뷰가 read-back 직후 CAS object 를 전부 지우자 트랜잭션이 `objects_remaining=0`
인 채로 public index publish 까지 성공했다. 보존 체계가 아무 것도 보존하지
않아도 통과하는 상태였다.

내가 만들어 둔 `restore_incomplete` 시험은 validator 가 임시 root 를 읽는지만
봤을 뿐, **그 root 가 backend 에서 나왔다는 것은 증명하지 않았다.** 시험의
이름이 검사하는 내용보다 강했다 — 24차 보충 발견 5-2 와 같은 형태다.

**(2) "영수증을 봉인했다" — 회수할 수 없는 digest 였다.**

receipt 를 메모리 dict 로 만들고 digest 만 index 에 적었다. 그 digest 로
아무 것도 되찾을 수 없으니 감사가 불가능하다. 그리고 마지막 "등록" 은 상태
변경이 아니라 단순 `return` 이었다. crash 뒤 남는 것은:

```text
public index entry     있음
receipt_digest         있음
그 digest 로 회수할 receipt   없음
등록                    없음
resume cursor          없음
```

내 "재시도" 시험은 같은 결정론 hook 으로 **계산 전체를 다시 실행**했다. 실제
사고에서 원본 계산은 12시간짜리고 crash 뒤 남는 것은 CAS 와 index 뿐이다.

### 35.2 고친 방식 — 구조로 막는다

| 무엇 | 어떻게 |
|---|---|
| CAS 복원 | `restore_from_cas(backend, manifest_digest, root)` 가 **원본 경로를 받지 않는다.** 인자에 없으면 재발이 불가능하다 |
| 증명 | `drop_source_after_seal=True` — 업로드 직후 원본을 지운다. 그러고도 끝까지 가면 복원이 backend 에서 나온 것이 확실하다 |
| 영수증 | canonical bytes 를 CAS 에 넣고 되읽어 대조. index 가 회수 가능한 `receipt_object` 를 가리킨다 |
| 등록 | durable journal 파일 (`O_EXCL`). `is_registered()` 로 확인된다 |
| crash 복구 | `finalize_only(leg_id, backend, index, hooks)` — **재계산 없이** CAS 만으로 닫는다 |
| publish | leg 마다 독립 파일을 `O_EXCL` 로. read-modify-write 가 아니다 |

**불변식도 정정했다.** "어느 단계에서 멈추든 public index 는 오염되지 않는다"
는 틀렸다 — publish 뒤 crash 는 durable 한 중간 상태를 남긴다. 숨기지 않고
두 단계로 적는다:

```text
publish 전 실패  →  항목 없음
publish 후 실패  →  항목은 durable, **등록 안 됨**. finalize_only 로만 닫힌다
```

### 35.3 두 번째 false-green — 영수증의 "빈 root"

`make_receipt.py` 도 같은 병이었다. `os.chdir(root)` 만 하고
`validate_provenance` 에 `repo_root` 를 넘기지 않았다. 검증기는 cwd 가 아니라
`src/io.py` 가 있는 저장소를 root 로 잡으므로 (`src/io.py:1328`) 봉인 입력을
**원본 checkout** 에서 풀었다. 이 컨테이너에 `results/grid_curves_v4` 가 남아
있어서 통과했을 뿐이고, 리뷰어의 clean checkout 에서는
`producer_곡선일치`·`입력_digest_재해시` 로 실패했다.

직접 확인하는 회귀를 넣었다: 복원 root 에서 봉인 입력 하나를 지우면
`repo_root=root` 검증이 **실패해야** 한다. 실패하지 않으면 검증기가 원본을
보고 있다는 뜻이다.

### 35.4 세 번째 — 영수증이 semantic 불일치를 성공으로 기록했다

재채점 결과와 봉인 summary 를 나란히 적어 놓고 **비교하지 않았다.** 주석에는
"자리별로 대조한다" 고 썼지만 assertion 이 없었고, 실제로 두 digest 가 달랐다.

원인을 찾았더니 `summarize()` 가 `multistart`·`multistart_random_only` 를
만들지 않는다는 것이었다 — `run_scoring` 이 restart trace 에서 따로 붙인다
(22차 발견 5 가 이미 지적한 것이다). `row_projection._add_multistart_blocks`
를 쓰지 않았으므로 두 값은 **영원히 다를 수밖에** 없었다. 정규 view 를
정의하고 equality 를 강제하니 이제 같다.

### 35.5 나머지 P1·P2

| # | 발견 | 대응 |
|---|---|---|
| 3 | 계획·semantic 결속이 optional | `run_spec` 누락 시 default 채우기 금지, `expected_semantic` 필수, 산출 schema 강제 |
| 4 | publish 가 동시 writer 에서 항목 유실 | per-leg `O_EXCL`. 16-thread 동시 publish 무손실, 같은 leg 동시 쓰기는 정확히 하나 |
| 7 | 사람용 label 이 정본 hash 안 | label 을 hash 밖으로, `PlannedLeg` 가 `pairing_design_sha256` 를 받는다 |
| 8 | candidate provenance 가 schema 없음 | source 별 닫힌 schema + 재귀 float 금지 + `src.grid.Condition` 결속 |
| 9 | cohort trap 둘 · frozen 목적지 쓰기 | 회귀를 cohort 순회로, `--cohort` 도입, frozen 거부, staging 후 원자적 승격 |
| 10 | 활성 cohort payload 미검증 | 같은 순회가 g2 gzip 도 압축 해제·재해시 (삭제 변이 확인) |
| 11 | claim role 세대가 자유문자 | `protocol_generations` 닫힌 집합 + 세대 불일치 시 `reason` 요구 |
| 12 | 커밋된 요청문에 placeholder | placeholder·없는 커밋·낡은 sha 를 잡는 회귀 (GATE26 의 낡은 core sha 를 실제로 잡았다) |

### 35.6 float→십진 다리에서 새로 정한 것

`src.grid.Condition` 은 float 다. 그것을 wire 로 옮기는 다리가 없으면 ID 체계가
격자와 무관한 장난감이다. 다만 **조용히 반올림하면 다른 조건이 같은 ID 로
합쳐진다.** 그래서 `decimal_from_float(x, places)` 는 변환 뒤 `float(s) == x`
를 확인하고, 어긋나면 실패한다 — 자릿수를 올리든 격자를 고치든 **사람이**
결정하게 만든다. `0.1 + 0.2` 를 3자리로 옮기려 하면 거부한다.

### 35.7 이번 라운드의 교훈 — 이름이 검사보다 강한 시험

두 P0 와 §35.3·§35.4 가 전부 같은 형태다: **시험의 이름이 실제로 하는 일보다
강했다.** `truly empty root`, `read-back`, `자리별로 대조` — 셋 다 그렇게
불렀지만 그렇게 하지 않았다.

이 저장소에서 반복된 형태이므로 (24차 보충 발견 5-2, 25차 발견 3) 대응도
이름이 아니라 **구조**로 한다: 복원 함수가 원본 경로를 아예 받지 않게 하고,
비교 결과를 영수증에 값으로 적고, 그 값이 틀리면 생성이 멈추게 했다.

## 36. 27차 리뷰 대응 — 같은 병의 세 번째 형태

> 2026-08-25. 26차 P0-1(CAS 복원)은 닫혔다. **P0-2 는 아직 열려 있었다.**
> 리뷰가 직접 돌린 반례 셋이 전부 재현됐고, 셋 다 §35.7 에 내가 적어 둔
> 형태 그대로다 — *시험의 이름이 실제로 하는 일보다 강하다.*

### 36.1 반례 셋

**(1) receipt 를 되읽은 직후 지워도 성공하고 등록됐다.**
`_drop_from_cas()` 는 receipt 가 만들어지기 **전에만** 돌았다. 그래서 CAS 훼손
시험 넷은 member·manifest 만 건드렸고 receipt 는 손대지 못했다. 요청문 §3 은
"member/manifest/**receipt** 훼손 시 publish 전 실패" 라고 적었는데, 나열한
시험에는 receipt 가 없었다. **한 번의 read-back 은 회수 가능성 불변식이
아니다.**

**(2) `finalize_only()` 가 다시 계산했다.** `_finalize()` 를 재호출했으므로
restore → validate → rescore → **새 receipt 생성**까지 반복했다. 원본 12시간
fitting 을 다시 돌리지 않는다는 좁은 뜻은 맞지만, 계약과 요청문이 적은
"재계산 없이 CAS 만으로" 는 사실이 아니었다. 리뷰가 `rescore_calls=2` 를
실측했다.

**(3) 등록 journal 이 존재만으로 완료였다.** `_register` 는 충돌 시 내용을
비교하지 않았고 `is_registered` 는 JSON 을 읽지도 않았다. 남의
`receipt_object` 를 가진 journal 을 심어 두면 트랜잭션이 `ok=True` 를
돌려주면서 등록은 남의 것을 가리켰다. 5바이트 쓰레기 파일도 "등록 완료" 였다.

### 36.2 이번에는 API 에서 없앴다

(2)의 고침이 이 라운드의 요점이다. 검사를 더하는 대신 **인자를 없앴다**:

```python
finalize_only(leg_id, backend, index_path)     # hooks 가 없다
```

hook 을 받지 않으면 재계산이 **구조적으로 불가능**하다. receipt 를 회수하고
결속을 대조하고 등록만 한다. 없거나 다르면 재생성하지 말고 멈춘다. 회귀는
validate/rescore 호출 횟수를 세어 0 인지 확인한다 — "안 불렀다" 를 문장이
아니라 카운터로 증명한다.

같은 방식으로 (1)은 등록 **직전** 재회수 대조로, (3)은 journal 파싱 + index
대조로 닫았다.

### 36.3 P1 여덟

| # | 무엇이 열려 있었나 | 고침 |
|---|---|---|
| 3 | 배타 생성이 crash-atomic 이 아니었다 — 5바이트만 쓰이면 "생성 성공" 인데 다음 읽기가 JSONDecodeError | temp 에 전부 쓰고 fsync → `os.link` no-replace commit → dir fsync |
| 3 | `publish()` 필수 키에 `receipt_object`·`payload_manifest_digest` 가 없는데 `finalize_only` 가 무조건 썼다 | 필수 목록에 추가 |
| 4 | `../escaped.bin` 이 restore root **밖에** 파일을 썼다 | manifest 닫힌 schema + 집계·root digest 재계산 + 중복 경로 거부 + 경로 봉쇄 |
| 4 | `leg_id='../../escaped'` 가 index 밖에 파일을 만들었다 | `check_id()` — separator·`.`/`..`·device name·길이 |
| 5 | 산출 manifest 가 byte output 을 증명하지 않았다 | relative_path·byte_size·file_sha256·producer 필수 |
| 6 | 안전 문구를 hash 밖으로 버렸다 (§36.4) | `_F4_주의` 를 skip 에서 뺐다 |
| 7 | receipt core 가 OS 독립이 아니었다 | `.as_posix()` + `write_bytes` 로 LF 고정 |
| 8 | frozen 보호가 CLI 에만 있었다 | 검사를 **쓰기 지점**으로 |
| 9 | design wire 의 domain 이 열려 있었다 | 닫힌 키 집합 · objective 순서 보존 · 수치 domain · NFC |
| 10 | 세대 간 role 이 `reason` 하나로 뚫렸다 | (role 세대, claim 세대) 허용표, 표에 없으면 fail-closed |

### 36.4 P1-6 — 안전 문구를 해시 밖으로 버렸다

26차에 정규 view 를 만들면서 `SEMANTIC_SKIP` 에 `_F4_주의` 를 넣었다.
"재채점이 만들 수 없는 실행 메타" 라고 적었는데 **틀렸다.** 그것은
`summarize()` 가 결정론적으로 만드는 **인용 금지 경고**다
(`src/scoring.py:369`):

> "이 블록의 두 지표는 그대로 인용하지 말 것 …"

떼어 놓으니 리뷰의 반례가 성립했다 — `"do not cite"` → `"safe to cite"` 로
바꿔도 semantic digest 가 같다. **안전 문구를 해시 밖으로 버린 것이다.**

`_채점원본` 은 `run_scoring` 이 붙이는 실행 메타라 재채점이 만들 수 없지만,
그 안에 `canonical`·`봉인상태`·`인용가능` 이 있다. 통째로 빼면 `인용가능` 을
뒤집어도 digest 가 같다. equality 로 못 보는 것은 **명시적 assertion** 으로
본다 (`_citation_safety`).

그리고 산출이 하나뿐일 때 `_outputs_agree()` 가 `True` 를 돌려줬다 —
**비교 대상이 없는데 "일치"** 다. 이제 실패한다.

### 36.5 이번 라운드에 배운 것

§35.7 에서 "이름이 아니라 구조로" 라고 적었는데, 그 원칙을 절반만 적용했다.
복원은 인자를 없애 구조로 막았지만 receipt·finalize·journal 은 **검사를 더하는
방식**으로 뒀고, 그래서 검사가 닿지 않는 자리가 남았다.

이번에는 셋 다 구조 쪽으로 옮겼다:

| 무엇 | 검사로 막던 것 | 구조로 바꾼 것 |
|---|---|---|
| 재계산 | "hook 을 안 부른다" 는 주석 | hook 을 **인자에서 제거** |
| 회수 가능성 | 한 번 read-back | 등록 직전 재회수가 **필수 경로** |
| 등록 | 파일 존재 | index 결속 대조가 `is_registered` **정의** |
| frozen | CLI 인자 검사 | **쓰기 지점** 검사 |

리뷰가 준 요약이 정확하다 — 검사는 가장 낮은 공통 지점에 두어야 한다.

## 37. 28차 리뷰 대응 — 검사 시점을 하나 더 두는 것으로는 안 된다

> 2026-08-25. 27차의 hook-free `finalize_only` 와 OS 독립 receipt core 는
> 닫혔다. **receipt lifecycle P0 는 아직 열려 있었다.** 리뷰가 한 문장으로
> 정리했고 그것이 이 라운드의 전부다:
>
> **read-before-register 는 retention 구조가 아니라 또 하나의 검사 시점이다.**

### 37.1 반례를 직접 재현했다

마지막 receipt read 가 bytes 를 돌려준 직후 object 를 지우는 backend 로 돌렸다:

```
transaction ok     : True
is_registered      : True
receipt 회수 가능?  : False
finalize_only      : {'ok': True, 'already': True}
```

`finalize_only()` 는 journal 과 index 의 digest 가 같으면 backend 를 **보지도
않고** `already=True` 를 돌려줬다. `is_registered()` 는 backend 인자조차 없어
"등록됨" 을 "receipt 가 회수 가능함" 으로 정의할 수 없었다.

receipt 만의 문제도 아니었다. manifest·member 를 restore read 직후 지워도
receipt 만 남긴 채 등록됐다. `retention_days=3650` 은 backend 가 보존을
강제했다는 증거가 아니라 dataclass 의 **자기신고 숫자**였다.

### 37.2 고침 — 등록을 retention commit 으로

성공 불변식을 문장이 아니라 구조로 적는다:

```text
registered(leg) ⇒ receipt · manifest · member · 산출 전부 회수 가능
```

local 에서 object-lock 의 대응물은 **hardlink** 다. `pins/<leg>/<dg>` 가
inode 를 붙들므로 `objects/` 를 통째로 비워도 회수된다. 등록 기록은 pin 집합
digest 를 이름하고, `is_registered(index, leg, backend)` 가 pin 완전성과
바이트를 확인한다. `finalize_only` 는 등록된 뒤에도 graph 를 다시 본다.

같은 반례를 다시 돌리면 이제 **pin 단계에서 멈춘다**:

```
✓ 등록이 막혔다: [pin] pin 할 object 가 없다: 510f1fe46deafd1a
  is_registered(backend 포함): False
```

### 37.3 receipt validator 를 닫았다

일곱 키만 있는 self-consistent receipt 가 등록됐고, `backend_uri` 가
`file+cas:///foreign` 이어도 receipt·index 가 서로 같은 문자열이면 통과했다.
`planned_envelope`·`outputs`·`validation` 이 없어도 됐다.

`check_receipt(rec, entry, backend_uri)` 하나로 exact key set ·
`planned_id == H(planned_envelope)` · **손에 든 backend** URI · outputs schema
를 보고, run 경로와 finalize 경로가 그것을 공유한다.

### 37.4 산출이 자기신고였고 성공 뒤 사라졌다

`check_output()` 은 root 를 받지 않아 파일을 열지 않았다. 다음이 오류 0건으로
통과했다:

```text
relative_path = C:\missing\escape.bin
byte_size     = 999
file_sha256   = bbbb...bbbb
producer      = invented/producer
```

더 결정적인 것은 산출 파일이 restore temp root 와 함께 삭제됐다는 점이다 —
payload manifest 는 rescore **전에** 봉인됐으므로 산출을 담지 않는다.
descriptor 는 회수 가능한 증거가 아니라 "있는 필드" 였다.

wrapper 가 봉쇄된 경로에서 bytes 를 한 번 읽어 size/SHA 를 **측정**하고 CAS 에
올린다. 자기신고가 실측과 다르면 실패한다. 증명과 주장의 주체를 갈랐다.

### 37.5 나머지 P1·P2

| # | 무엇이 열려 있었나 | 고침 |
|---|---|---|
| 2 | Windows 에서 hardlink 를 만든 **뒤** parent fsync 가 거부돼 상태를 바꿔 놓고 실패했다 (리뷰 환경 17건) | capability 를 **만들기 전에** 재고, 못 하면 그 자리에서 멈춘다. staged object 도 fsync |
| 3 | `True == 1` 이라 manifest 집계를 bool 로 바꿔도 통과 · `truly empty root` 가 비어 있지 않아도 성공 | 둘 다 거부 |
| 4 | `make_receipt` 는 `_F4_주의` 를 넣었는데 `row_projection` 비교기는 계속 뗐다 — **두 감사 경로가 또 갈렸다** | `SEMANTIC_SKIP` 정본을 한 곳에 두고 import |
| 5 | frozen guard 가 exact root 만 봤고 원장 부재 시 fail-open | 자손까지, 원장 없으면 fail-closed |
| 6 | design validator 가 top-level 만 닫아 nested 변이 다섯이 통과 · dict **키** NFC 미검사 | nested 재귀 검증 · 키 NFC · 부모 digest domain · provider objective membership |
| P2 | role 과 `protocol_generation` 을 **함께** 바꾸면 통과 — `reason` loophole 이 두 필드 loophole 로 옮겨갔다 | role 행에서 세대를 없애고 봉인된 `leg_source_digest` 에서 **도출** |

### 37.6 세 라운드째 같은 자리

24차 보충 발견 5-2 · 25차 발견 3 · 26차 P0 · 27차 P0 · 28차 P0 가 전부 한
형태다. 이번 리뷰가 그것을 다시 짚었다 — "manifest-last 라는 이름이 set
atomicity 보다 강했다".

지난 라운드에 "구조로 바꿨다" 고 적은 네 항목 중 셋은 실제로 구조였지만,
**등록만 검사 두 번**이었다. 검사를 한 번 더 두는 것과 불변식을 구조로 만드는
것의 차이가 이번 P0 다.

남은 것 중 같은 위험이 있는 자리를 미리 적어 둔다 — `row_projection` 의
승격은 아직 **fixed-name 세 파일**이라 set atomicity 가 아니다 (리뷰 P1-5).
immutable generation directory + 단일 pointer 로 바꾸는 것이 다음 checkpoint 다.

## 38. 29차 리뷰 대응 — 저널의 자기신고가 권위였다

> 2026-08-25. 28차의 hardlink pin 은 방향은 맞았지만 **권위가 여전히 저널의
> 자기신고**였고, pin 자체가 CAS 원본을 파괴하는 경로를 갖고 있었다.
> 리뷰가 준 반례 셋을 전부 재현했고, 이번에는 검사를 더 두는 대신 **그래프를
> 다시 도출하는 단일 권위**를 만들었다.

### 38.1 P0-1 — 저널이 적은 것이 곧 등록이었다

`is_registered` 는 journal 이 나열한 digest 가 pin 으로 존재하는지만 봤다.
그래서 journal 이 **부분집합**을 적으면 그 부분집합만 확인하고 통과했고,
등록 전체를 다른 backend 로 복사해도 그 backend 의 pin 이 self-consistent 하면
통과했다. 저널을 쓰는 쪽과 검증하는 쪽이 같은 문서를 봤다는 뜻이다.

`verify_registered_graph(backend, index_path, leg_id)` 하나가 권위가 된다.
여섯 단계 전부 **pin 에서 읽은** 영수증에서 출발한다:

```text
1  pin 에서 receipt 를 읽는다 (objects/ 가 비어도 회수돼야 한다)
2  닫힌 스키마 + 손에 든 backend 의 URI 로 receipt 를 검증
3  pin 에서 manifest 를 읽어 receipt 집계와 결속
4  receipt+manifest 로 기대 그래프를 다시 도출
5  expected == journal.objects == 디스크 pin 이름  (삼면 일치)
6  pin 된 바이트 전수 + 산출 객체 크기 확인
```

반례 둘이 이제 fail-closed 다:

```
반례1 subset journal  → registered: False
반례2 foreign backend → registered: False
```

### 38.2 P0-4 — pin 이 CAS 원본을 0바이트로 만들었다

hardlink 불가 FS 예비 경로가 목적지를 열어 썼다. 목적지는 **같은 inode 의 CAS
원본**이었다. 재현:

```
원본 바이트 이후: b''
원본 digest 유효: False
```

보존 도구가 보존 대상을 파괴하는 형태다. 목적지를 직접 여는 경로를 없앴다:

| 상황 | 이제 |
|---|---|
| 이미 pin 이 있다 | 바이트를 대조한다. 다르면 실패. symlink 면 거부 |
| 경쟁 `EEXIST` | 같은 규칙으로 내용 확인 |
| hardlink 불가 | 임시파일에 쓰고 `os.link` 로 원자 배치, temp 는 항상 정리 |

### 38.3 P1 — 스키마·바이트·플랫폼

| # | 무엇이 열려 있었나 | 고침 |
|---|---|---|
| 1 | receipt 의 `planned_envelope`·`validation`·`outputs` 가 **중첩에서** 열려 있었다 | 세 곳 전부 닫힌 키 집합 + manifest 집계 결속 + 산출 객체 바이트 크기 확인 |
| 2 | manifest 경로가 대소문자·NFC 로 충돌 가능했다 | 두 충돌 모두 거부, 비-NFC 경로 자체를 거부 |
| 3 | Windows 텍스트 모드가 CRLF 를 변환할 수 있었다 | `os.O_BINARY` 명시 + LF/CRLF/NUL/BOM/비-UTF8 6종 왕복 회귀 |
| 4 | `retention_days` 가 정책 하한 없이 자기신고 | `MIN_RETENTION_DAYS = 365` |

### 38.4 P2 — 세대 계약이 가변 YAML 을 믿었다

claim role 의 세대를 `evidence.leg_source_digest` 에서 도출하도록 28차에
바꿨지만, `evidence` 는 여전히 **가변 YAML** 이다. evidence 와 role 을 함께
바꾸는 변형이 통과했다. 이제 **봉인된 투영이 적은** `source_digest` 와
대조한다.

그리고 이 자리에서 반대 방향 실수를 하나 만들었다 — 기록한다.

29차 초판은 28차가 죽여 놓은 조건(`r.get("protocol_generation")` 을 금지해
놓고 그 필드를 다시 비교)을 `rg == tg` 로 되살렸다. **너무 넓었다.**
`paired_fixed5_v4`(v5) 가 v5 legacy 주장의 정본이 되는 것까지 막았고, 그것은
24차 보충 리뷰가 명시적으로 허용한 것이다 — "legacy claim scope 와 당시
protocol 을 명시한 채 유지할 수 있다". 전체 시험이 그 자리에서 빨갛게 됐다.

원인은 leg-level `inference_role` 이 **무엇에 대한 판정인지**를 잘못 읽은
것이다. 원장이 그 다리를 `diagnostic` 이라고 적은 근거는 원장 안에 그대로
있다 — "**현행 정본은 아니다**: run_spec 의 `source_digest` 가 현행과 다르다".
즉 leg-level 은 **현행 세대에 대한** 역할이지 모든 세대에 대한 상한이 아니다.
비교 대상은 `current` 이고, 옛 세대는 `role_compatibility` 가 관장한다.

`current` 를 자유필드로 두면 한 줄 고쳐서 옮길 수 있으므로 **도출**한다 —
`protocol_generations` 순서에서 실제 source digest 가 도달한 가장 새로운 세대
(그래서 산출물 없는 `v6` 은 현행이 될 수 없다). 세대표에 가짜 digest 한 줄을
더해 현행을 옮기는 경로는, 표의 모든 digest 가 **봉인된 투영에 묶여** 있어야
한다는 검사로 막는다.

네 규칙이 실제로 무는 것을 변이로 확인했다:

| 변이 | 실패하는 회귀 |
|---|---|
| leg-level 조항을 `False` 로 | `..._legacy_claim...` · `..._self_promote...` |
| `tg == current` 를 `rg == tg` 로 되돌림 | 위 둘 + 본 계약 시험 |
| 세대표 anchoring 삭제 | `..._anchored_to_sealed_projections` |
| `current` 도출을 선언으로 | 셋 |

이 변이를 걸 수 있게 하려고 계약 본문을 `_claim_role_problems` 순수 함수로
꺼냈다. 인라인일 때는 규칙을 고쳐도 "고친 규칙이 실제로 무는가" 를 보일
방법이 없었다 — 35.7 이 적은 "이름이 검사보다 강한 시험" 의 다른 얼굴이다.

### 38.5 자체 발견 — spec 이 거짓을 선언하고 있었다

`ANALYSIS_SPEC.summary_comparison.skip_top_level_keys` 가
`[_채점원본, _F4_주의]` 라고 적혀 있었지만 비교기는 `SEMANTIC_SKIP` 을 썼다.
이력을 확인했다:

* 23차 `f49cd66e` — 비교기도 둘 다 뗐다. 그때는 선언이 참이었다.
* 28차 — 비교기를 `("_채점원본",)` 로 좁히면서 **선언은 안 고쳤다**. 직전
  커밋 `2e505317` 에 `_SKIP = set(SEMANTIC_SKIP)` 과 옛 선언이 공존한다.
* 29차 — spec 이 `SEMANTIC_SKIP` 을 읽는다.

그 결과 `analysis_spec_sha256` 이 `f1898eb6…` → `43d74dd3…` 로 움직였다.
**비교 규칙이 바뀐 것이 아니라 거짓 선언이 사라진 것**이며, 원장 g2 항목이
이 값을 g1 과 바이트 동일이라고 적고 있었으므로 그 산문도 정정했다. 행
바이트(`projection_sha256`·`restart_projection_sha256`·`fits_sha256`)는 g1 과
여전히 동일하다.

### 38.6 다음 checkpoint — 아직 안 한 것

리뷰가 요구한 최소 증거 9항 중 **두 항이 열려 있다**. 닫았다고 적지 않는다.

| 항 | 상태 |
|---|---|
| 4 | object/pin 디렉터리 fsync **순서**는 고쳤다. **crash/reopen drill 은 없다** |
| 9 | immutable cohort generation + 단일 `CURRENT` 승격 (P1-5) — **미착수**. `row_projection` 승격은 여전히 fixed-name 세 파일이라 set atomicity 가 아니다 |

## 39. 30차 리뷰 대응 — retention 의 권위를 backend 로 옮겼다

> 2026-08-25. 리뷰가 세 회차의 병을 한 줄로 정리했다:
>
> ```text
> Gate28: receipt read → journal 사이
> Gate29: pin read → journal 사이
> Gate30: post-commit graph verification 의 pin read → return 사이
> ```
>
> 그리고 처방도 함께 줬다 — "다음 checkpoint 는 더 많은 read 가 아니라
> **retention state 의 authority 를 backend transaction/lease 로 옮기는 것**".
> 이 라운드는 그 문장을 그대로 구현한 것이다.

### 39.1 P0-1 — 전수 읽기 도중 사라져도 성공했다

`verify_registered_graph()` 의 순서가 이랬다:

```text
receipt pin read → manifest pin read → on_disk snapshot
→ verify_pins() 전수 읽기 → output 만 다시 읽기 → 성공
```

`on_disk` snapshot 이 전수 읽기 **앞**이고 두 번째 읽기는 output 뿐이다.
그래서 member pin 을 읽은 직후 지우면 receipt·manifest·member 가 사라진 채
성공이 반환됐다. 리뷰가 준 그대로 재현했고, 29차의 `_DropAfterRead` 로는
잡히지 않는다는 지적도 맞았다 — 그것은 `read_back()` 의 `objects/` 만
건드린다. member 는 전수 읽기에서 **딱 한 번** 읽히므로 그것을 겨냥해
`_DropPinAfterRead` 를 새로 만들었다.

리뷰가 요구한 세 primitive 를 만들었다:

```text
retain(graph, min_retention_days) -> lease
verify_retention(lease, actual_backend)
retrieve_retained(lease, digest)
```

lease 는 그 자체가 CAS object 이고 pin 된다 — graph 의 일부라서 위조하면
graph digest 가 어긋난다. 등록 검증의 **마지막 단계가 바이트 읽기가 아니라
lease 상태 확인**이므로 전수 읽기 도중의 삭제가 잡힌다.

### 39.2 그 뒤의 창은 닫지 않았다 — 대신 성공의 뜻을 좁혔다

local filesystem 에서 마지막 검사와 반환 사이는 **닫을 수 없다.** 이 저장소의
실행 환경은 uid 0 이라 directory mode bit 도 잠금이 아니다 (실측: `chmod 0o500`
뒤에도 unlink 가 성공했다). 검사를 하나 더 두면 창이 한 칸 뒤로 갈 뿐이고,
그것이 28·29·30차가 같은 자리에 선 이유다.

그래서 검사를 늘리는 대신 **`ok=True` 의 뜻을 좁혔다.** lease 가 강제 수준을
값으로 신고한다:

| 값 | 뜻 |
|---|---|
| `advisory_local` | pin 은 붙들지만 강제하지 못한다. local 이 여기다 |
| `object_lock` | backend 가 retention 을 강제한다 |

`run_transaction` 은 `durable: False` 를 함께 돌려주고,
`assert_durable_retention()` 은 `object_lock` 이 아니면 거부한다. 비싼 본
실행을 승인하는 gate 가 그 자리다. 리뷰의 문장 — "그 전에는 `ok=True` 를
durable retention 성공으로 부르면 안 된다" — 을 타입으로 적은 것이다.

### 39.3 P0-2 · P0-3

| # | 무엇이 열려 있었나 | 고침 |
|---|---|---|
| P0-2 | `is_registered(index, leg)` 가 backend 없이 참을 돌려줬다 — `pins/`·`objects/` 를 다 지워도 참 | backend **필수**. journal 주장은 `has_registration_journal()` 로 분리 |
| P0-2 | identity 가 `file+cas://{self.root}` 문자열뿐 — `root=Path("cas")` 로 등록 뒤 cwd 를 바꾸면 다른 store 를 가리키며 URI 가 같다 | URI 를 절대 경로로 정규화 · 생성 시각에 고정되는 store UUID 를 receipt 와 lease 에 결속 |
| P0-3 | `_fsync_dir()` 실패를 `False` 로 돌리고 **무시**했다 | `_fsync_dir_strict()` 가 오류로 전파 |
| P0-3 | `objects/<prefix>`·`pins/<leg>` 를 만들고 **자기 자신만** flush | `_mkdir_durable()` 이 새로 만든 모든 층의 부모 edge 를 flush |
| P0-3 | capability 캐시 키가 `resolve().anchor` — POSIX 의 모든 mount 가 `/` 하나로 합쳐졌다 | `st_dev` |

그리고 요청문이 "없다" 고 신고했던 **crash/reopen drill** 을 넣었다. 예외
주입은 `finally` 를 돌지만 kill 은 아무 것도 돌지 않는다 — 자식 프로세스를
`os._exit(9)` 로 죽이고 부모가 다시 열어 `journal visible ⇒ full graph
retrievable` 을 확인한다. commit 순서를 뒤집는 변이로 물리는 것을 봤다.

### 39.4 P1 넷

| # | 무엇 | 고침 |
|---|---|---|
| 1 | journal 의 duplicate·surplus key·거짓 `pin_set_digest` 가 통과 (`set(...) == expected` 만 봤다) | 닫힌 키 집합 · unique 정렬 64-hex · **유도한 graph 로** 재계산 · journal 없으면 fail-closed. 등록 전 검증은 `verify_graph_before_registration()` 으로 이름을 갈랐다 |
| 2 | planned envelope 의 값 domain 이 없었다 (`protocol_generation=7` 등) · hook 의 `ok` 를 truthiness 로 봤다 · output 이 role 무관 8키 nonempty · manifest member path 에 domain 없음 | `check_envelope()` · `check_hook_validation()` · role 별 tagged union · seal 시점 `_safe_member_path` |
| 3 | retention 하한이 receipt 의 자기신고 숫자 | `min_retention_days` 를 envelope 에 봉인하고 lease 검증이 **지금 backend** 를 재조회 |
| 4 | `objective_plan` 이 caller 의 자유 인자 | `design_binding()` 이 봉인 design 에서 chain 을 유도하고 `candidate_id` 는 그것만 받는다 |

P1-2 에서 하나 더 나왔다 — `envelope()` 이 `int(self.total_start_budget)` 로
**강제 변환**하고 있어서 `True` 가 `1` 이 되어 domain 검사에 도달하지 못했다.
변환을 없앴다.

P1-4 의 golden vector 는 **바이트 동일**하다. ID domain 은 안 움직였고 움직인
것은 plan 의 권위 위치다.

### 39.5 P2 — 세대 chain, 그리고 닫지 못한 것

닫은 것:

* 투영의 `manifest_sha256` 을 봉인 manifest **바이트에서 재해시**한다
* 투영의 `source_digest` 를 그 manifest 의 `run_spec.source_digest` 와 대조
* cohort 가 갈리면 실패하고 active cohort 를 우선한다 (초판은 처음 찾은 것)
* 세대표의 **값**에 근거를 붙였다 (`source_digest_evidence`)
* `STAGE3_CONTRACT.md` §8 에 leg-level 과 per-claim 두 층을 명시 — 리뷰가
  지적한 "authority 문서에 반영되지 않은 재해석"

닫지 **못한** 것을 그대로 적는다. 실행이 남긴 어떤 산출물에도
"protocol generation" 이라는 필드가 **없다** — 그 이름은 이 원장의 분류다.
그러므로 `digest → generation` 화살표는 도출이 아니라 **선언**이고, 여기서 할
수 있는 것은 그 선언을 봉인물이 지지하는 digest 에 묶어 두는 것까지다. 묶음 9
등록이 생기는 순간 registered receipt 의 `planned_envelope` 이 정본이 되도록
fail-closed 검사를 미리 켜 뒀고, 지금은 그 검사가 "등록된 다리 없음" 을
고정하고 있다.

### 39.6 자체 발견 둘

**lease 가 재실행마다 늘었다.** `retain_until_utc` 때문에 부를 때마다 lease
바이트가 달라져, 재실행이 초 경계를 넘으면 lease 가 하나 더 pin 됐다. 전체
시험을 열두 번 돌려 두 번 빨갰고 원인이 시계라 재현이 확률적이었다. 시계를
강제로 전진시키는 결정적 회귀로 고정하고 `retain()` 을 멱등으로 만들었다.

**요청문 lint 가 archive 를 거짓으로 만들었다.**
`test_committed_gate_requests_are_self_contained` 가 **모든** 요청문의 인용을
**오늘의** 영수증과 대조했다. 요청문은 그 회차의 기록이므로 다음 회차에
영수증이 바뀌면 지나간 요청문이 전부 거짓이 된다. "최신 것만 본다" 로
약화하면 archive 는 아무도 안 보게 되므로, **그 요청문이 이름한 대상 커밋의
영수증**과 대조하도록 바꿨다 — 그것이 자기완결의 뜻이기도 하다.

### 39.7 변이로 확인했고, 물지 않은 것 셋

이번에 넣은 규칙을 전부 변이로 시험했다. **물지 않은 변이가 셋** 있었고 전부
시험이 다른 축에 업혀 통과하던 자리였다:

| 물지 않은 변이 | 왜 | 처리 |
|---|---|---|
| URI 정규화 삭제 | `relative_root` 시험이 lease 의 store UUID 축으로 통과 | store 를 `store.json` 째 복사해 UUID 축을 무력화한 시험으로 고쳤다 |
| receipt 의 `backend_store_id` 결속 삭제 | end-to-end 로는 lease 검사가 먼저 걸린다 | validator 를 직접 시험하는 회귀를 따로 만들었다 |
| journal 의 자기 `pin_set_digest` 재계산 삭제 | `verify_registered_graph` 가 **유도한 graph 로** 다시 계산한다 | 실제 중복이므로 **약한 쪽을 지웠다** — 같은 계산이 두 곳에 있으면 강한 쪽을 지워도 초록이다 |

35.7 이 적은 "이름이 검사보다 강한 시험" 이 이번에는 **변이가 통과하는 시험**
의 형태로 나타났다. 규칙을 넣을 때마다 지워 보는 것을 절차로 굳힌다.

### 39.8 여전히 미착수

묶음 9 의 immutable cohort generation + 단일 `CURRENT` 승격 (리뷰 최소 증거
9항) 은 이번에도 **미착수**다. `row_projection` 의 승격이 여전히 fixed-name 세
파일이라 set atomicity 가 아니다. 계약 §13 의 열 묶음도 "닫음" 으로 바꾸지
않았다.

## 40. 31차 리뷰 대응 — 좁힌 의미가 문자열 하나로 무너졌다

> 2026-08-27. 30차에 "`ok=True` 의 뜻을 좁혔다" 고 적었다. 리뷰가 그 경계를
> 한 줄로 넘었다:
>
> ```python
> b = CasBackend(root=cas, enforcement="object_lock")   # 구현은 여전히 local pin
> r = run_transaction(..., backend=b, ...)
> assert r["durable"] is True                            # 통과했다
> assert_durable_retention(b, index, leg)                # 통과했다
> ```
>
> `enforcement` 가 **dataclass field** 였다. 강제 수준을 값으로 신고하게 만든
> 것까지는 맞았는데, 그 값을 **호출자가 붙일 수 있게** 뒀다.

### 40.1 P0-1 — label 이 아니라 capability 로

| 무엇 | 지금 |
|---|---|
| `enforcement` 를 생성자로 지정 | `ENFORCEMENT` 는 `ClassVar` — 인자가 아니고 대입도 `__setattr__` 이 막는다 |
| 신고값을 그대로 lease 에 저장 | `probe_enforcement()` 가 provider 를 **지금 조회**하고, 그 결과를 싣는다 |
| lease 의 문자열을 다시 안 봄 | `verify_retention()` 이 lease ↔ 조회 결과를 대조한다 |
| lock 증거가 없음 | lease 가 provider 의 `lock_mode` 와 immutable `object_versions` 를 싣고, 검증 때 version 을 **다시 조회**한다 |
| `finalize_only()` 가 `ok=True` 만 | 두 경로 모두 `run_transaction` 과 같은 typed 결과 |

`ObjectLockBackend` 로 adapter 자리를 만들었다. **실제 provider adapter 는
아직 없다** — 세 메서드(`query_object_lock` · `lock_objects` ·
`query_object_versions`)를 구현하는 것이 남은 일이고, 그 전에는
`probe_enforcement()` 가 `advisory_local` 로 떨어져 `retain()` 부터 실패한다.
클래스 이름만으로는 강제가 아니라는 뜻이다.

경계가 한쪽으로만 닫히면 그것도 시험이 아니므로, 강제가 **있는** 쪽도
canary 로 고정했다 — 가짜 provider 가 version·mode·retain-until 을 만들면
`durable=True` 가 되고, 정책 하한이 내려가거나 version 이 사라지면 그 자리에서
durable 을 잃는다.

### 40.2 §2.1 질문에 대한 답을 받았다

리뷰의 답을 그대로 옮긴다:

1. "local 에서는 durable retention 을 주장하지 않는다" 는 **정책 방향은 맞다.**
2. **P0-1 전체 종결에는 actual object-lock backend 구현이 필요하다.**

그래서 이 라운드는 (2) 를 닫지 않았고 닫았다고 적지도 않는다. 타입 경계와
canary 까지가 이번 몫이다.

### 40.3 P0-3 — CAS 쪽만 닫혀 있었다

| # | 무엇이 열려 있었나 | 고침 |
|---|---|---|
| 1 | `_exclusive_write()` 가 `index/`·`index/legs`·`index/registered` 새 edge 를 안 굳혔다 | `_mkdir_durable()` 을 쓴다 |
| 2 | `_fsync_dir_strict()` 가 capability 없으면 조용히 `return` | 그 자리에서 멈춘다 |
| 3 | link 성공 뒤 fsync 실패 → 재시도가 `EEXIST` 로 fsync 를 건너뛰고 성공 | 이름이 있는 한 **항상** 굳힌다 |
| 4 | crash drill 의 두 지점이 모두 `_register()` 앞 | `after_register`·`during_journal_fsync` 를 더했다 |

2번은 주석까지 틀렸었다 — "publish 가 이미 막는다" 는 CAS 와 index 가 **같은
filesystem** 일 때만 참이다. 갈라 주입하니 `put_if_absent()` 가 그냥 성공했다.

4번이 이번 라운드의 대표적인 자기기만이다. 시험 이름은
`journal visible ⇒ full graph retrievable` 인데 **전건이 한 번도 참이 되지
않았다.** 공허하게 참인 시험을 "drill 을 넣었다" 고 적었던 것이다. 이제
양성/음성이 모두 나왔는지를 별도 시험이 강제한다.

### 40.4 P1 넷

| # | 무엇 | 고침 |
|---|---|---|
| 1 | `{"ok": True, "checks": {"payload": False}}` 가 통과하고 receipt 가 `n_checks: 1` 로 축약해 false subcheck 를 **지웠다** | 값이 전부 참이어야 하고 검사 **이름 집합**을 receipt 에 봉인 |
| 2 | output 이 role 별 **subset** 검사라 `rescored_rows` 에 summary 전용 필드가 통과 · `relative_path` domain 이 manifest 와 달랐다 | role 별 exact key set · 같은 `_safe_member_path()` 공유 |
| 3 | `candidate_mode` enum 이 계약 §3 과 **달랐다** — 계약의 두 mode 를 거부하고 계약에 없는 세 mode 를 허용 | 계약에서 파싱 (값을 두 곳에 두지 않는다) |
| 4 | `binding` 이 자유 dict — key set 과 bank 동일성만 봐서 위조가 통과 | `binding` 인자를 없앴다. `candidate_id` 가 봉인물만 받고 chain 을 유도 |

P1-4 는 **두 회차 연속 같은 형태**다. 30차에 "plan 을 인자로 받을 수 있다는
것 자체가 결함" 이라고 적어 놓고, plan 을 담은 dict 를 인자로 만들었다.
한 겹 포장했을 뿐이었다.

### 40.5 P2 — 30차의 설명이 거짓이었다. 철회한다

30차 요청문과 원장 §39.5 에 "묶음 9 등록이 생기는 순간 registered receipt 가
정본이 되도록 **fail-closed 검사를 미리 켜 뒀다**" 고 적었다. **거짓이다.**

그 검사는 등록된 다리를 가변 `LEG_PRESERVATION.yaml` 의 **optional**
`evidence.registered_receipt` 필드로 골랐다. 실제 등록이 생겨도 그 필드를 안
적으면 검사가 잠든다 — 원장이 검사 대상을 스스로 고르는 구조였다.

이제 실제 index 의 journal 을 읽고 양방향으로 본다 (index 에 있는데 원장에
없음 / 원장이 주장하는데 index 에 없음). 실물 index 가 아직 없어 결과는
여전히 비어 있지만 **이유가 다르다** — 원장이 고른 것이 아니라 실물이 없다.
규칙이 무는지는 합성 index 시험이 보인다.

### 40.6 변이로 확인했고, 물지 않은 것 다섯

| 물지 않은 변이 | 왜 | 처리 |
|---|---|---|
| `assert_durable_retention` 의 재조회 삭제 | `verify_retention` 이 이미 대조한다 | 중복이라 **삭제** — 권위를 한 곳으로 |
| output exact key set → subset | 시험이 **남는** 키만 넣고 **모자란** 경우를 안 봤다 | 누락 축을 시험에 추가 |
| capability fail-closed 삭제 | 시험이 `store.json` 쓰기 경로에 업혀 통과 | store 를 먼저 만들고 CAS 쓰기만 보게 분리 |
| `bank_version` 유도 삭제 | design digest 에 이미 들어 있어 `bank_id` 가 어차피 달라진다 | 유도값 자체를 보는 시험으로 |
| crash drill 양성 상태 | 전건이 거짓이라 공허하게 참 | 양성/음성 도달을 강제하는 시험 추가 |

30차에 "규칙을 넣을 때마다 지워 보는 것을 절차로 굳힌다" 고 적었고, 이번에도
다섯이 나왔다. 절차가 없었으면 다섯 전부 "닫았다" 로 보고됐을 것이다.

### 40.7 미종결

| 항 | 상태 |
|---|---|
| P0-1 durable retention 전체 | actual object-lock adapter 없음 — 리뷰가 그것을 조건으로 명시했다 |
| 최소 증거 9 | immutable cohort generation + 단일 `CURRENT` — **미착수** |
| P2 generation value | `digest → generation` 은 여전히 선언이다 (실행 산출물에 그 필드가 없다) |
