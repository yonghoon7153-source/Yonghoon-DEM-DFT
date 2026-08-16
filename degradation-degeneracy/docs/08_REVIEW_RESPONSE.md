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
(6% vs 5%)로 **raw와 보정의 방향이 다릅니다.** 사실상 동률로 읽는 것이 맞고,
"기준 곡선이 목적함수의 우열까지 뒤집는다"는 제 추측은 이 표로 지지되지 않습니다.

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
> 그 목적함수를 못 푸는 효과가 섞여 있다. 방어 가능한 문장은 **"두 protocol
> 모두에서 dQ/dV 추가의 개선은 관측되지 않았다"** 까지다.
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
| 결론 1 정본 | 62% → 63% "사실상 변화 없음" | **paired 61.9% → 87.2% (+25.27%p)**. 단 34p multimodal 97% 라 정보량 비교 불가 — 방어 가능한 문장은 "두 protocol 모두 개선 미관측" |
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
| 절에 마커 하나면 그 절 전체 면제 | **claim ID 별 마커** `⛔ 철회[CLAIM_ID]` |
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
