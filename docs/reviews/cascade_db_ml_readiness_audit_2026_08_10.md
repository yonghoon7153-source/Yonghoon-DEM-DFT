# Cascade DB 및 co-doping ML 준비도 감사

- 감사일: 2026-08-10
- 범위: `db/properties/`의 cascade 단일 도펀트·게이트·co-doping 파생 데이터, 관련 생성 코드와 Git 계보
- 목적: 연구세미나에서 어디까지 결과로 말할 수 있는지, co-doping 선택에 ML을 쓰려면 무엇이 더 필요한지 구분

## 한 줄 결론

현재 DB는 **47종 O/F 단일 도펀트 스냅샷을 여러 축에서 비교하는 데는 쓸 수 있지만**, 273개 실행 전체를 대표하거나 실제 co-doping 성능을 예측하는 DB는 아니다. 47종은 273개 실행에서 물리적으로 살아남은 집합이 아니라 2026-06-25에 versioning된 앞 141행의 종별 집계이고, 현행 `codoping_ml_v2`의 1,081쌍은 실제 pair 계산값이 아니라 단일 도펀트 값과 휴리스틱을 재조합한 **가설 목록**이다.

## 1. 273과 47의 단위부터 다르다

| 단계 | 수 | 단위 | 현재 확인 가능한 의미 |
|---|---:|---|---|
| 실행 roster | 91 | species | 사람이 수동으로 작성한 화합물 목록 |
| batch matrix | 273 | run slots | 91 species × 3 campaign labels (`x002/x005/x010`) |
| 2026-06-25 snapshot | 141 | run-level rows | commit `ce68d06d`, 메시지 `Cascade v23 (141 done)` |
| 종별 집계 | 47 | species | 141 rows ÷ 3 labels, commit `237bbee8` |
| post-hoc gate audit | 47→47→43→25→11→1* | species | 이 단계부터 G1–G5; `1*`은 roster-relative G5 순위일 뿐 winner가 아님 |

91종 roster의 family 구성은 다음과 같다.

| Family | 91-species roster | 2026-06-25 canonical snapshot |
|---|---:|---:|
| Oxide | 37 | 37 |
| Fluoride | 10 | 10 |
| Chloride | 19 | 0 |
| Bromide | 5 | 0 |
| Iodide | 4 | 0 |
| Nitride | 5 | 0 |
| Sulfide | 11 | 0 |
| **Total** | **91** | **47** |

47종은 역사 실행 스크립트의 **앞 47종**, 즉 37 oxides + 10 fluorides와 정확히 같다. 따라서 현재 가장 방어 가능한 설명은 다음이다.

> 91 manually curated species × 3 campaign labels = 273 run slots. The versioned 2026-06-25 snapshot contains 141 rows = 47 species × 3 labels. The remaining 44 roster species were not ingested into the canonical table; absence is not physical rejection.

2026-07-11 문서는 273/273 완료라고 기록하지만 동시에 `unified_dataset_273.csv` 통합 분석은 미실행이라고 적는다 (`kb/projects/cascade_v23_review_2026_07_11.md:34–36`). 현재 Git 전체 이력에는 `unified_dataset_273.csv`, 273-row 결과 manifest, 나머지 132행을 포함하는 정본 표가 없다. 개별 실패 원인이 문서로 확인되는 것은 As₂S₃ 세 label의 stage-01 `n_structures=0`뿐이다.

### 기존 funnel 설명의 수정 필요점

`db/properties/cascade_screening_funnel.json:12–15`는 91→47을 세 계산축 완결성에 따른 pipeline attrition으로 설명한다. 현재 versioned 증거는 이를 전종에 대해 입증하지 못한다. 이 필드는 다음 두 층으로 분리하는 편이 맞다.

1. **ingestion provenance**: 91×3 planned/run slots → 141 versioned rows → 47 species snapshot
2. **post-hoc scientific gates**: 47→47→43→25→11→1*

둘을 한 funnel로 그리면 44종이 물리적으로 탈락한 것처럼 보이는 오류가 생긴다.

## 2. DB를 다섯 층으로 나눠 읽어야 한다

### L0. 원 실행·구조 계층 — repo에서 미완결

- gabia의 `FINAL_RANKING.json`, run directory, champion geometry가 원자료로 지목돼 있다.
- `db/properties/doping_cascade_verified.json:4–5`는 원자료와 구조가 gabia에 있다고 적지만, 현재 repo에는 해당 전체 raw manifest와 `db/structures/doping/` 구조 묶음이 없다.
- `doping_cascade_verified.json:2`와 `doping_cascade_trivalent_M3.json:2`에는 Sc₂O₃_x002, Al₂O₃_x005 값 충돌이 명시돼 있다.
- 원자료가 없으므로 snapshot 밖 44종을 재수집하거나 충돌 행을 독립 검산할 수 없다.

판정: **가장 먼저 복구해야 할 층**이다.

### L1. run-level versioned snapshot — 141행

`cascade_v23_champions.csv`

- 141 rows = 47 species × 3 labels
- 세 label은 각각 47행
- `concentration`은 전 행 `0.25`
- `anneal_converged=True`: 141/141
- `eos_fit_quality_ok=True`: 140/141, 나머지 1행은 `refit_lowr2`
- `sigma_300K_S_cm_NE`, `sigma_md_Ea_eV`, `wad_J_m2_mean`: 141/141 결측

`cascade_v23_litransport.csv`

- 141 rows, `_dir` 141개 고유
- cation site: Li_24g 100, Li_48h 8, P_4b 33
- anion site: S_16e 58, S_4a 53, Cl_4d 30
- 이 파일의 BVS/BVSE 계열 값은 정적 구조 proxy이지 MD 전도도나 실험 σ가 아니다.

판정: **47종 snapshot 내부의 세 label 비교에는 사용 가능**하다. 다만 label을 실제 농도로 해석하면 안 된다.

#### plain과 `+Clrich` variant가 종별 평균에 섞인다

141행 가운데 17행, 10개 base species가 `+Clrich` variant다. 9종은 세 campaign label 안에서 plain과 `+Clrich`가 섞이고, B₂O₃는 세 행이 모두 `+Clrich`다. 그런데 현행 species-level 집계 코드는 이름의 `+` 뒤를 버리고 base dopant별로 평균한다 (`tools/figures/plot_cascade_insights.py:34`). 반면 `oxidation_stability_cascade.csv`는 plain variant ESW를 정본으로 쓴다. 따라서 현행 47종 한 행에는 **plain ESW와 plain/Cl-rich 혼합 UMA 값**이 함께 놓일 수 있다.

판정: `variant_plain_or_clrich`를 key로 승격하기 전에는 species-level 회귀 target이나 농도 반응으로 쓰면 안 된다.

### L2. species-level canonical tables — 47종

| File | Rows | 역할 | 주의점 |
|---|---:|---|---|
| `cascade_v23_ranked.csv` | 47 | 세 label 집계·기존 composite rank | 첫 줄에 `x=0.25`; human-weighted score |
| `oxidation_stability_cascade.csv` | 47 | oxidation/reduction/window | `ocv_V` 9, `clrich_ox_V` 44 결측 |
| `cascade_stability_axes.csv` | 47 | 후속 stability axes | 47행 완결 |
| `cathode_reactivity_cascade.csv` | 94 | 47종 × 2 cathode states | LCO full/half만 포함 |
| `cascade_air_axis_lit_vs_tier.csv` | 47 | 문헌·preset air axis | 문헌값과 surrogate가 혼재; 일부 결측 |

`cascade_v23_ranked.csv`의 score는

```text
0.30 × oxidation
+ 0.25 × stability
+ 0.20 × softness
+ 0.15 × ductility
+ 0.10 × window
```

인 사람이 정한 합성점수다. 따라서 score 1위는 물리적으로 유일한 winner가 아니라 선택 가중치의 결과다.

판정: **47종 descriptive comparison에는 사용 가능**, 발견 성능이나 절대 순위 증거로는 부족하다.

#### 직접 계산값과 파생·큐레이션 값을 구분해야 한다

| 구분 | 예시 | ML 취급 |
|---|---|---|
| 직접 계산 출력 | UMA relative energy/volume/elasticity, BVSE blocking·path proxy, MP-hull ESW·interface energy | protocol·단위·quality flag와 함께 feature/target 후보 |
| 파생값 | 3-label 평균, min-max norm, composite score, Pareto, G1–G5 pass/fail | source feature와 함께 target으로 쓰면 정의식 누수 |
| 문헌·큐레이션 | `gap_lit_eV`, cost tier, air/HSAB tier, hydrolysis literature value | 계산값과 별도 column lineage 필요 |
| 역사 snapshot | `doping_cascade_verified.json`, `doping_cascade_trivalent_M3.json` | canonical과 자동 병합 금지 |

`cathode_reactivity_cascade.csv`의 LCO full/half 값은 `cascade_stability_axes.csv`에도 들어가 있으므로 두 파일을 sample처럼 합치면 중복된다. `cascade_v23_eos_refit.json`도 새 계산이 아니라 기존 UMA E–V 점의 재적합이다. `site_preference_raw_78.csv`는 MgO_x005가 서로 다른 값으로 중복되고 MgO_x002가 빠져 있어, 그대로 78개의 독립 sample로 세면 안 된다.

정의상 겹치는 canonical CSV와 역사 JSON을 비교하면 22행이 `|Δde|>0.02 eV/atom`, `|ΔE|>2 GPa` 또는 `|ΔB0|>2 GPa`로 다르다. 그런데 `webapp/data.py:846`은 이 계보들을 동시에 로드한다. 따라서 ML loader는 glob이 아니라 명시적 registry와 `status=canonical|historical|derived|literature`를 써야 한다.

### L3. derived narrative·gate layer

`cascade_v23_themes.json`과 `cascade_screening_funnel.json`은 L1/L2를 다시 조합한 해석 계층이다.

- 실제 계산값, 문헌값, 등급형 surrogate, roster-relative normalization이 한 파일에 공존한다.
- `norm`은 47종 roster가 바뀌면 달라진다.
- G4는 `transport_norm > 0.30 AND blocking < 0.60`이다.
- G4 단독 탈락 27종 중 24종은 host/문헌 anchor가 없는 inherited `blocking<0.60`에 의해 탈락하고, BVSE cut의 단독 기여는 B₂O₃·GeO₂·MoO₃ 세 종뿐이다 (`cascade_screening_funnel.json:230–233, 2402–2444`).
- G5는 host anchor가 없는 roster median split이므로 최종 1종을 결론처럼 인용하면 안 된다 (`cascade_screening_funnel.json:313, 2515`).

판정: **가설과 trade-off를 보여주는 사후 audit view**다. 독립 validation set이나 discovery funnel이 아니다.

### L4. co-doping hypothesis layer

`cascade_v23_synergy_pairs.csv`

- 40개 pair 가설
- 첫 줄부터 `single-dopant proxy, NOT validated`
- `synergy = max(joint_window_gain,0) × radius_match × stability_gate`

`codoping_ml_v2.csv`

- 1,081 rows = C(47,2), 모든 unordered pair 이름 조합
- 실제 co-doped structure: 0
- pair × 농도 label: 0
- site·charge compensation·configuration label: 0
- 공동치환 UMA/DFT/실험 target: 0
- 18/1,081은 내부 AD 밖이지만, top 40에는 AD-out이 0개

`codoping_ml_v2_meta.json:4`도 상태를 `HYPOTHESIS GENERATOR — NOT VALIDATED`로 고정한다.

판정: **첫 계산 batch 후보를 구성하는 보조 휴리스틱**일 뿐, 공동치환의 성능 예측 모델은 아니다.

### L5. deep validation layer

현재 deep DFT coverage는 B₂O₃와 Nd₂O₃ 두 종, 즉 2/47이다. 둘은 G1–G4의 11종 생존 집합에 포함된 downstream subset이 아니다. 따라서

```text
47 → 11 → 2 DFT
```

처럼 화살표를 연결하면 틀린 그림이다. 세 수치는 다음처럼 병렬로 써야 한다.

- 47-species versioned snapshot
- 11 retained in the post-hoc G1–G4 view
- 2 species with deep DFT coverage

## 3. 농도 provenance 충돌

세 곳의 의미가 현재 일치하지 않는다.

| Source | 표기 |
|---|---|
| directory labels | `x002/x005/x010` |
| `cascade_screening_funnel.json:12,232` | x=0.02/0.05/0.10으로 해석 |
| `cascade_v23_champions.csv` | `concentration=0.25` 전 행 |
| `cascade_v23_ranked.csv:1` | `x=0.25` |

commit `ce68d06d` 계보에서는 50-atom 구조의 floor 때문에 실제 배치가 0.25이고 label은 placement campaign을 구분하는 이름으로 사용된 정황이 있다. 원 구조·조성 manifest가 repo에 없으므로 현재 발표와 ML feature에서는 다음 규약만 안전하다.

> x002/x005/x010 are nominal campaign labels, not verified physical concentrations.

따라서 세 label의 기울기를 `dose_slope`, 농도 민감도 또는 희석 한계로 학습시키면 안 된다. 실제 조성 원자수와 structure hash가 복구된 뒤 다시 정의해야 한다.

## 4. 현재 co-doping ML이 실제로 학습한 것

### Stage 1: 높은 R²가 물성 예측력은 아니다

Stage 1은 47종의 기존 cascade composite score를 target으로 쓴다. 그 score 자체가 입력 feature의 선형합이므로 LOOCV R²=0.9998은 새 물리를 배운 것이 아니라 score 공식을 거의 역산한 결과다 (`codoping_ml_v2_meta.json:13–17`; `docs/cascade_ml_integration_guide.md:78`).

### Stage 3: 실제 pair label이 아니다

Stage 3의 양성 40쌍도 실제 공동치환 계산값이 아니라 기존 v1 휴리스틱이다. 나머지 1,041쌍에는 `synergy≈0`, 낮은 weight 0.1을 둔다. 따라서 모델은 실측/계산 interaction을 배우지 않고 기존 휴리스틱을 재표현한다 (`codoping_ml_v2_meta.json:78, 282–286`).

### 독립 화학 일반화가 무너진다

| Validation | weighted R² |
|---|---:|
| pair-LOOCV | +0.0892 |
| LODO | −0.1805 |
| L2DO | −0.2548 |

pair-CV와 L2DO의 차이는 +0.344다. 같은 도펀트를 공유하는 pair가 train/test에 동시에 들어가 낙관 편의가 생긴다 (`codoping_ml_v2_meta.json:391–421`).

이미 알려진 40쌍 내부 순서에는 Spearman 0.498의 약한 신호가 있지만, 1,081쌍에서 그 40쌍을 찾아내는 precision@40은 0.100 대 shuffle 0.0823, p=0.426으로 랜덤과 구별되지 않는다. stage-3 cR²p=0.142도 관례적 0.5 문턱보다 낮다 (`codoping_ml_v2_meta.json:304–327`).

### 현 cascade gate와도 정렬되지 않는다

현 ML top 40과 G1–G4 생존 11종을 교차하면:

- 두 구성원이 모두 생존 11종인 pair: **0/40**
- 한쪽이라도 생존 11종인 pair: **2/40**

현재 score가 oxidation/window와 기존 single-dopant score에 강하게 끌리고 G4 transport를 거의 반영하지 않기 때문이다. 이것이 top pair가 반드시 나쁘다는 뜻은 아니지만, 적어도 이 모델은 “현 cascade를 통과할 co-doping pair”를 고르는 모델이 아니다.

## 5. ML로 co-doping 선택은 가능하다 — 단, 순서가 반대다

현재는 `ML → pair 계산`이 아니라 다음 순서가 맞다.

### Step 0. full ledger 복구

먼저 gabia/backup에서 273 run 결과를 immutable ledger로 재수집한다.

필수 열:

```text
candidate_id
base_species
campaign_label
actual_composition
structure_id
structure_sha256
variant/site/charge_compensation
protocol_id
run_status/convergence
raw property columns with units
source_path/source_sha256
timestamp/git_commit
```

실패도 삭제하지 않고 `run_status`로 남긴다. snapshot 밖 44종을 negative label로 채우면 안 된다.

### Step 1. single-dopant canonical table 동결

- raw·processed·derived·literature 열을 분리
- 실제 조성·구조 hash를 key로 사용
- Sc₂O₃·Al₂O₃ 충돌 행 해결
- x label과 actual concentration 분리
- composite score는 결과 열이 아니라 view layer로 이동

### Step 2. 실제 pair pilot 생성

최소 pilot 권장안:

- 12 pair chemistries
- 3 campaign levels
- 3 independent starting configurations
- 총 108 UMA pair relaxations

pair 구성은 top-score만 고르지 않고 다음을 균형 있게 넣는다.

1. 4 physics/Pareto exploitation pairs
2. 4 high-uncertainty 또는 rare-chemistry exploration pairs
3. 4 additive-null/negative controls

한 dopant가 pair 대부분을 지배하지 않게 하고, 최소 16개 서로 다른 dopant를 포함하는 편이 좋다. 이 수는 모델 완료선이 아니라 현재의 min/max/average 결합 가정을 처음 반박할 수 있는 pilot 규모다.

### Step 3. raw target과 interaction residual 학습

composite score 하나를 target으로 두지 않는다.

- relaxation/phase-retention success
- matched relative energy
- actual co-doped oxidation/reduction/window
- BVSE raw score와 blocking
- mechanics
- 선택 후보의 DFT electronic/reaction labels

interaction은 같은 protocol의 matched controls로 정의한다.

```text
synergy_y(A,B) = y_AB − y_additive_baseline(A,B)
```

pair·level·configuration을 모두 같은 group fold로 묶는다.

### Step 4. small-data model과 검증

초기에는 deep network보다 다음이 적합하다.

- Bayesian ridge / elastic net
- Gaussian process
- 작은 tree ensemble
- symmetric additive + interaction model

검증은 pair-LOOCV가 아니라 다음을 기본으로 한다.

- LODO: leave-one-dopant-out
- L2DO: leave-both-dopants-out
- LOFO: leave-one-chemical-family-out
- frozen chronological prospective holdout

비교 baseline:

- random/diversity selection
- additive single-dopant model
- physics-only Pareto selection
- 현행 heuristic H0

### Step 5. active-learning loop

```text
DB ledger
  → uncertainty/diversity/Pareto acquisition
  → UMA geometry + relative screening
  → boundary/disagreement candidates only DFT
  → provenance-preserving ingestion
  → grouped retraining
```

DFT는 1,081쌍을 모두 도는 첫 단계가 아니라, UMA의 경계·불일치·전하/산화상태 민감 후보를 검증하는 calibration layer로 둔다.

내부 surrogate H1을 시도할 실용적 하한은 약 40 independent pair chemistries × 3 levels × 3 configurations = 360 UMA relaxations이고, 그중 10 pair는 결과를 보기 전에 prospective/L2DO holdout으로 동결하는 편이 좋다. 선택된 8 pair 정도의 대표 구조는 같은 구조·같은 protocol의 UMA–DFT energy/force calibration을 두는 게 좋다. 이 숫자는 통계적 보증이 아니라 첫 H1 campaign의 planning floor다.

## 6. 세미나에서 쓸 수 있는 문장과 쓰면 안 되는 문장

### 쓸 수 있음

> We organized a versioned 47-species O/F snapshot across multiple screening axes and used post-hoc gates to expose trade-offs and protocol weaknesses.

> The present co-doping model is an H0 hypothesis generator; it helps design the first balanced calculation batch but does not yet predict pair synergy.

> The next step is active learning on actual co-doped structures with uncertainty, diversity, matched controls, and selective DFT calibration.

### 쓰면 안 됨

- “273종에서 계산 게이트로 47종을 선별했다.”
- “47종은 273개 계산 중 성공한 후보들이다.”
- “x002/x005/x010은 검증된 2/5/10% 농도다.”
- “ML이 1,081개 공동치환을 예측했고 top pair를 발견했다.”
- “LOOCV R²=0.9998이므로 일반화 성능이 높다.”
- “G4 통과 11종이 객관적인 최종 후보군이다.”

## 7. 세미나 figure 배치 권장

1. **Data lineage slide**  
   `91 species × 3 campaign labels = 273 run slots → 2026-06-25 snapshot: 141 rows = 47 species`를 보여주고, 44종은 `not ingested`로 표시한다. 이 그림과 G1–G5 waterfall은 분리한다.

2. **Trade-off slide**  
   oxidation onset과 BVSE/pathway proxy를 함께 그려, host onset을 올린 6종이 모두 G4에서 멈추는 현상을 보여준다. 캡션에 `static pathway heuristic ≠ conductivity`를 쓴다.

3. **Pareto slide**  
   G1–G4 11종 안의 conditional 2D Pareto 4종을 보여주되 `axis-dependent; not a winner set`을 쓴다.

4. **Appendix scorecard**  
   47종을 알파벳순으로 두고 favorable percentile과 first-stop gate만 보여준다. composite score나 winner 표시는 쓰지 않는다.

5. **ML future slide**  
   현재 `0 actual pair labels`에서 시작해 `balanced pair pilot → grouped validation → selective DFT → active learning`으로 넘어가는 도식을 쓴다.

## 8. 우선순위

### P0 — ML 전에 닫아야 함

1. 273 run ledger와 나머지 132행 복구 또는 “미복구” 상태 명시
2. actual composition·structure hash 복구
3. x label vs 0.25 농도 충돌 해소
4. Sc₂O₃·Al₂O₃ cross-file conflict 해소
5. 실제 co-doping pair·configuration·matched-control labels 생성

### P1 — 세미나/웹앱에서 정리

1. 91→47을 pipeline attrition으로 쓰는 문구 수정
2. computed·literature·curated·derived 열의 status 표시
3. G4 blocking 상수 민감도와 heuristic status 상시 노출
4. co-doping `ml_score ± uncertainty`를 `heuristic index ± model-fit spread`로 낮춤
5. 47종 모델의 적용범위를 O/F snapshot으로 제한

## 9. 근거 파일과 Git 계보

- `origin/claude/unified-2026-05-15:tools/doping/master_batch_273.sh` — 91종 roster와 3-label loop
- commit `ce68d06d` — `Cascade v23 (141 done)`, `cascade_v23_champions.csv` 최초 반입
- commit `237bbee8` — 141행을 47종으로 집계한 `cascade_v23_ranked.csv`
- `kb/projects/cascade_v23_review_2026_07_11.md:34–36` — 273/273 완료 주장과 unified 통합 미실행
- `db/properties/cascade_v23_champions.csv`
- `db/properties/cascade_v23_litransport.csv`
- `db/properties/cascade_v23_ranked.csv`
- `db/properties/oxidation_stability_cascade.csv`
- `db/properties/cascade_stability_axes.csv`
- `db/properties/cathode_reactivity_cascade.csv`
- `db/properties/cascade_air_axis_lit_vs_tier.csv`
- `db/properties/cascade_v23_themes.json`
- `db/properties/cascade_screening_funnel.json`
- `db/properties/doping_cascade_verified.json`
- `db/properties/doping_cascade_trivalent_M3.json`
- `db/properties/cascade_v23_synergy_pairs.csv`
- `db/properties/codoping_ml_v2.csv`
- `db/properties/codoping_ml_v2_meta.json`
- `tools/cascade/codoping_ml.py`
- `docs/cascade_ml_integration_guide.md`

## 최종 판정

현재 47종 DB는 버릴 데이터가 아니다. **“47종 O/F snapshot의 다축 trade-off를 보여주는 감사 가능한 데이터셋”**으로 위치를 정확히 잡으면 충분히 강하다. 다만 이를 273 전체 campaign이나 실제 co-doping 예측으로 확장하는 순간 provenance가 끊긴다. 다음 연구 단계는 더 복잡한 모델을 먼저 붙이는 것이 아니라, 273 ledger와 actual pair labels를 복구·생성한 뒤 작은 모델로 불확실성과 상호작용 잔차를 배우게 하는 것이다.
