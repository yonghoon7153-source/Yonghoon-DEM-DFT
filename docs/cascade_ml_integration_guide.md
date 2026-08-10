# Cascade × ML integration guide

> **목적**: 현재 cascade에 이미 들어간 ML의 역할을 정확히 구분하고, 앞으로 계산·실험
> 라벨을 쌓아 uncertainty-aware active learning으로 확장하는 실무 규약이야.
>
> **현재 지위**: UMA는 빠른 에너지·힘 계산기고, co-doping ML v2는
> **HYPOTHESIS GENERATOR**야. 둘 다 최종 물리 판정을 대신하지 않아.

---

## 0. 한 줄 결론

**지금 ML은 cascade를 빠르게 돌려 주고 다음 가설의 순서를 제안해. 앞으로의 ML은
“다음에 무엇을 계산할지”를 고르는 폐루프가 될 수 있지만, 무엇이 참인지는 여전히
DFT와 실험이 판정해야 해.**

이 문서에서 “ML”은 아래 두 물건을 섞어 부르지 않아.

1. **Pretrained MLIP — UMA-s-1p1**
   - 원자 좌표를 받아 에너지와 힘을 내는 계산 엔진이야.
   - 현재 cascade의 TIER 1에서 configuration 탐색과 anneal을 빠르게 돌려.
2. **Project-specific surrogate — co-doping ML과 이후 active learner**
   - 우리 계산·실험 라벨을 이용해 후보의 순서와 다음 acquisition을 제안하는 모델이야.
   - 현재 co-doping v2는 실제 공동치환 라벨이 없어서 검증된 예측기가 아니야.

> 근거: 현행 pipeline은 MLIP → DFT → 축별 후처리 구조야
> (`docs/cascade_pipeline_guide.md:58-87`). UMA의 입력·출력과 사용 범위는
> `docs/cascade_pipeline_guide.md:198-215`에 정리돼 있어. 공동치환 라벨 부재와
> hypothesis-generator 지위는 `tools/cascade/codoping_ml.py:4-7`,
> `db/properties/codoping_ml_v2_meta.json:4`에 명시돼 있어.

---

## 1. 현재 ML은 정확히 무엇을 하나

### 1.1 UMA: “예측 결론”이 아니라 “빠른 계산 층”

현재 UMA가 맡는 일은 이거야.

- halogen configuration을 열거해.
- Li 부격자 배치를 훑어.
- 500 K Langevin anneal로 국소 최소를 벗어나게 해.
- 살아남은 champion configuration을 다음 계산으로 넘겨.
- 같은 프로토콜 안에서 에너지·탄성·구조의 **상대 순위**를 만드는 데 써.

현재 믿는 범위도 명확해.

- **쓸 수 있음**: 동일 프로토콜 안의 configuration 순위, 후보 간 상대 비교
- **그대로 인용하면 안 됨**: 절대 에너지, 절대 탄성계수, 절대 전도도
- **UMA로 판정하면 안 됨**: 산화상태·스핀·전하분리가 핵심인 사건
- **사용 금지 범위**: Li₃N 계열

UMA가 싸다고 해서 DFT가 사라지는 건 아니야. 현행 TIER 2는 MLIP EOS 사전스캔 뒤
Quantum ESPRESSO로 BM3 EOS, V₀ 이완, k-mesh 수렴을 다시 확인해.

> 근거: UMA가 하는 일과 믿을 범위는
> `docs/cascade_pipeline_guide.md:198-215`, DFT가 다시 재는 항목은
> `docs/cascade_pipeline_guide.md:219-227`에 있어. 웹앱도 UMA 절대값 대신
> 내부 상대비교만 허용하고, DFT 심층검증은 Nd₂O₃·B₂O₃ 두 건뿐이라고 밝혀
> (`webapp/data.py:835-840`).

### 1.2 Co-doping ML v2: “공동치환 예측기”가 아니라 “가설 정렬기”

현재 모델은 47개 단일 도펀트에서 얻은 특징을 이용해 가능한 1,081개 두 도펀트 조합을
정렬해. 구조는 아래와 같아.

- 단일 도펀트 특징 16종과 group one-hot으로 기존 cascade score를 ridge로 해부해.
- 두 도펀트의 특징을 min/max/average 규칙으로 합쳐 pair 특징을 만들어.
- 물리적 의미를 부여한 2차 교호작용 8종을 추가해.
- 내부 LOOCV 잔차와 계수 공분산으로 수치적 ±를 붙여.
- 적용영역 `ad_d`, 모델 불안정성 `ad_eps`, 적용 여부 `ad_A`를 같이 내.

하지만 이 모델에는 **실제 공동치환 구조를 계산한 라벨도, 실험 라벨도 없어**. 학습
타깃도 실제 물성이 아니라 기존 cascade score와 v1 휴리스틱 synergy야.

현재 진단 결과는 이렇게 읽어야 해.

- stage 1의 LOOCV R² = 0.9998은 물성 예측력이 아니야. score가 입력 특징의 선형합이라
  항등식을 복원한 결과야.
- stage 3는 이미 알려진 휴리스틱 40쌍 **안의 순서**에는 신호가 있어.
- 하지만 1,081쌍에서 그 40쌍을 **발굴**하는 능력은 랜덤과 구별되지 않아
  (1.22×, p = 0.43).
- cR²p = 0.14로 QSAR 관례 문턱 0.5보다 낮아.
- pair 단위 CV는 같은 도펀트를 공유하는 쌍 때문에 R²를 +0.34 과대평가해.
- leave-both-dopants-out에서는 weighted R² = -0.2548이야.

따라서 지금 허용되는 표현은 이거야.

> “47개 단일 도펀트 결과로 1,081개 공동치환 **가설의 우선순위**를 제안했어.”

아래 표현은 아직 안 돼.

> “ML이 1,081개 공동치환 물성을 예측해 최적 조합을 발견했어.”

> 근거: 모델의 설계와 내부 ±의 한계는
> `tools/cascade/codoping_ml.py:9-27`에 있어. 발굴력·cR²p·CV 누수 수치는
> `db/properties/codoping_ml_v2_meta.json:275-286`과
> `db/properties/codoping_ml_v2_meta.json:391-421`에 있어. 최종 limitations도
> 이 모델을 물성 예측기가 아니라 휴리스틱 해부·확장으로 규정해
> (`db/properties/codoping_ml_v2_meta.json:432-438`).

---

## 2. 다음 구조: uncertainty-aware multi-fidelity loop

### 2.1 전체 루프

```text
Candidate space
dopant/pair × concentration × configuration
        │
        ▼
L0  Curated descriptors / literature / database
        │
        ▼
L1  UMA relax + BVSE + low-cost screening
        │
        ▼
Acquisition
Pareto gain + calibrated uncertainty + chemical diversity
        │
        ▼
L2  Matched DFT validation
energy · force · reaction · electronic structure
        │
        ▼
L3  Experimental feedback
phase purity · actual composition · σ(T)/Ea · stability · processing
        │
        └──────────► Versioned database ──► retrain ──► next batch
```

핵심은 **ML이 gate를 없애는 게 아니라 비싼 계산의 순서를 고르는 것**이야.

### 2.2 각 층의 역할

| Layer | 입력·라벨 | 용도 | 인용 한계 |
|---|---|---|---|
| L0 | 조성, 원소 기술자, 문헌 큐레이션, DB 값 | 후보 생성·싼 사전 필터 | 문헌값과 우리 계산값을 한 절대축으로 섞지 않아 |
| L1 | UMA energy/force/relax, BVSE·기하 프록시 | 넓은 configuration 탐색과 상대 ranking | UMA 절대값·BVSE 절대 σ로 읽지 않아 |
| L2 | 같은 구조의 DFT single point/relax, 반응에너지, 전자구조 | L1 오차 교정과 gate 경계 판정 | matched protocol끼리만 Δ를 학습해 |
| L3 | 상순도, 실제 조성, σ(T), Ea, 안정성, 공정조건 | 계산상 후보가 실험에서도 성립하는지 판정 | batch·공정 메타데이터 없이 숫자만 합치지 않아 |

“Multi-fidelity”를 서로 다른 물성을 한 열에 섞는다는 뜻으로 쓰면 안 돼.

- 같은 구조·같은 protocol의 UMA와 DFT가 있으면
  `Δ = y_DFT − y_UMA`를 별도 모델로 배울 수 있어.
- BVSE channel과 MD diffusion은 같은 물성의 저·고정밀 값이 아니야. 서로 다른 출력
  head나 별도 모델로 둬.
- MP grand-potential ESW와 우리 DFT electronic structure도 출처와 질문이 달라.
- 실험 σ(T)는 계산 σ와 protocol·미세구조 domain이 달라서 조건을 입력 특징으로
  기록해야 해.

> 근거: 현행 후처리도 구조·전자·결합·수송·역학·전기화학을 서로 다른 관측량으로
> 분리해 (`docs/cascade_pipeline_guide.md:237-246`). 특히 BVSE는 정적 기하 프록시라
> 절대 σ·D로 읽으면 안 돼 (`docs/cascade_pipeline_guide.md:305-321`).

### 2.3 한 회차의 candidate routing

한 번의 acquisition batch에는 세 종류를 모두 넣어.

1. **Exploit**
   - 예상 Pareto 개선이 큰 후보
   - 여러 gate를 동시에 통과할 가능성이 높은 후보
2. **Explore**
   - 예측 불확실성이 큰 후보
   - 적용영역 밖 또는 경계인 후보
   - 기존 라벨에 드문 원소군·산화수·charge-compensation을 가진 후보
3. **Validate**
   - gate threshold 가까이에 있는 후보
   - 모델 위원회가 크게 불일치하는 후보
   - UMA가 판정하기 어려운 전하·스핀·반응 사건을 포함한 후보

상위 score만 계속 계산하면 모델이 이미 좋아하는 화학에 라벨이 몰려
winner’s curse가 커져. 현재 co-doping 결과에서도 상위 40쌍의 `ad_eps` 중앙값이 전체의
2.1배야. 그러니 `score − k·uncertainty` 하나로 전부 뭉개기보다 exploit·explore·validate
세 bucket을 따로 남기고, 각 후보가 왜 선택됐는지 기록해.

> 근거: 상위 40쌍의 불안정성 신호와 `ad_d/ad_eps/ad_A` 사용법은
> `db/properties/codoping_ml_v2_meta.json:381-384`에 있어. 기존 실행계획도
> 상위 후보에 불확실성 penalty를 적용하고 UMA 공동치환 슈퍼셀에서 첫 라벨을 만들도록
> 잡혀 있어 (`kb/open_items.md:443-448`).

### 2.4 불확실성은 “오차막대”가 아니라 “routing signal”부터 시작해

현재 쓸 수 있는 불확실성 대리량은 세 종류야.

- **Model-fit uncertainty**: co-doping ridge의 내부 잔차·계수 공분산
- **Applicability domain**: `ad_d`, `ad_A`
- **Model instability**: leave-one-dopant-out jackknife `ad_eps`
- **MLIP committee disagreement**: UMA·MACE-MP-0·SevenNet-0 힘 예측 불일치

어느 것도 바로 “실제 물리 오차 ±x”라고 부르면 안 돼.

현재 MLIP 위원회는 MACE와 SevenNet이 MPtrj를 공유하고 UMA만 OMat24라 실질적으로
세 명이 아니라 두 훈련데이터 진영에 가까워. 세 모델이 일치해도 모두 같은 functional
계열에서 같이 틀릴 수 있어. 먼저 matched QE single point로

`committee disagreement → actual |DFT − MLIP| error`

관계를 교정해야 해. 교정 전에는 선별·중단·DFT 승격을 위한 routing signal로만 써.

> 근거: 현재 위원회가 절대 정확도를 말하지 못하고 독립성이 낮다는 감사는
> `db/properties/mlip_committee_baseline.json:19-23`에 있어. 다음 단계도 계면 snapshot
> 탐지와 QE single-point 대조로 명시돼 있어
> (`db/properties/mlip_committee_baseline.json:61-66`).

---

## 3. 데이터 계약

### 3.1 한 행의 단위

도펀트별 평균 한 행만으로는 active learning을 하면 안 돼. 최소 단위는 아래 tuple이야.

```text
(host_id,
 dopant_a, dopant_b,
 concentration,
 charge_compensation,
 configuration_id,
 structure_hash,
 protocol_id,
 engine,
 seed)
```

같은 도펀트라도 농도·configuration·seed가 다르면 별도 행으로 남겨. 평균과 champion은
원자료에서 파생한 별도 view로 만들어.

현재 47종은 사람이 고른 91종 roster의 2026-06-25 versioned O/F snapshot이야.
91 화합물 × 3 campaign label = 273 run slot이지만, repo에 남은 canonical 표는 실행 순서의
앞 141행 = oxide 37종 + fluoride 10종의 세 label이야. later note에는 273/273 완료 기록이
있어도 통합 273-row 표와 전종별 실패 manifest가 없으므로, 91 → 47을 물리 gate나
data-completeness 탈락으로 부르지 않아.

> 근거: `docs/reviews/cascade_db_ml_readiness_audit_2026_08_10.md`의 Git 계보 감사와
> `docs/cascade_pipeline_guide.md` §3.

### 3.2 필수 identity·protocol 필드

| 묶음 | 필수 필드 |
|---|---|
| Identity | `candidate_id`, `host_id`, `dopant_a`, `dopant_b`, `concentration`, `charge_compensation` |
| Structure | `configuration_id`, `structure_hash`, `parent_structure_id`, `site_mapping` |
| Protocol | `protocol_id`, `method_id`, `engine`, `software_version`, `seed`, `temperature_K` |
| Provenance | source file, run directory, Git commit, input hash, output hash |
| Comparison | `comparison_group_id`, `label_scope=relative/absolute`, units |
| Selection | `acquisition_round`, `selection_bucket`, `selection_reason` |

`comparison_group_id`는 같은 규약끼리만 비교하게 만드는 안전장치야. UMA와 DFT,
single-seed와 multiseed, ordered와 disorder를 한 비교군에 넣지 않아.

### 3.3 상태는 null과 실패를 분리해

최소한 아래 상태를 구분해.

| status | 뜻 | ML에서의 처리 |
|---|---|---|
| `complete` | 요청한 protocol이 정상 완료 | 해당 label 사용 가능 |
| `not_run` | 아직 실행하지 않음 | missing; 0이나 실패로 바꾸지 않아 |
| `pipeline_failed` | seed 생성·입력·수렴 등 계산 경로 실패 | 별도 failure model 후보; 물성 음성 라벨 아님 |
| `physical_failed` | 같은 protocol에서 구조 붕괴·명시적 gate 탈락 | 정의와 근거가 있을 때만 물리 라벨로 사용 |
| `censored` | 계산·측정 한계 때문에 상·하한만 앎 | censored label로 보존 |
| `not_applicable` | 해당 물성이 그 계에 정의되지 않음 | 학습 대상에서 제외 |

특히 `pipeline_failed`를 낮은 score로 바꾸면 모델이 화학이 아니라 계산 실패 패턴을
배워. 91 → 47의 44종을 negative label로 넣으면 안 되는 이유가 이거야.

### 3.4 물성 라벨은 합성 score와 분리해

아래 label은 각자 별도 열·별도 provenance를 가져.

- **Structure/energy**: converged, relative energy, force residual, volume change,
  phase identity
- **Electrochemistry**: ox_V, red_V, reaction ΔE, 기준 전극·상 집합
- **Transport proxy**: BVSE channel volume, blocking fraction, cell convention
- **Dynamics**: D(T), Ea, seed 수, MSD fit window, β gate
- **Mechanics**: C_ij, E, G, B, clamped/relaxed-ion 구분
- **Electronic**: fixed-occupation VBM/CBM gap, DOS/ELF provenance
- **Experiment**: synthesis outcome, phase purity, actual composition, σ(T), Ea,
  atmosphere, pellet density, pressure, batch

`cascade_score`는 위 물성의 파생 합성지표로만 남겨. 모델의 최종 truth label로 쓰면
score 공식을 다시 배우는 항등식 문제가 반복돼.

> 근거: 현재 stage 1의 타깃도 “cascade v23 score — 합성 지표, 물성 실측 아님”으로
> 명시돼 (`db/properties/codoping_ml_v2_meta.json:13-18`).

### 3.5 실험 feedback은 공정조건까지 한 묶음이야

실험 한 점은 아래처럼 기록해.

```text
(candidate_id,
 synthesis_route,
 precursor_lot,
 temperature_time_profile,
 atmosphere,
 pressure,
 pellet_density,
 measured_composition,
 phase_purity,
 property,
 value,
 uncertainty,
 replicate_id)
```

같은 조성이라도 공정이 다르면 다른 domain이야. 공정 메타데이터 없이 전도도 숫자만
합치지 않아. 반복 측정은 평균 하나로 덮지 말고 replicate를 보존해. 그래야 aleatoric
variation과 모델 uncertainty를 구분할 수 있어.

---

## 4. 검증 split 계약

### 4.1 random-row split 금지

공동치환 쌍 A–B와 A–C는 A를 공유해 비독립이야. configuration과 농도도 같은 부모
화학을 공유해. 행을 무작위로 나누면 train과 test에 사실상 같은 화학이 동시에 들어가.

필수 split은 아래 순서로 봐.

1. **LODO — leave-one-dopant-out**
   - 한 도펀트가 들어간 모든 농도·configuration·pair를 같은 fold로 묶어.
2. **L2DO — leave-both-dopants-out**
   - pair의 두 도펀트가 모두 train에 없는 상황을 시험해.
3. **LOFO — leave-one-family-out**
   - oxide, fluoride, late-TM, lanthanide 같은 화학족 전체를 숨겨.
4. **Prospective chronological holdout**
   - acquisition 전에 다음 round 후보와 평가 규약을 동결해.
   - 모델이 한 번도 보지 않은 미래 라벨로 최종 성능을 봐.

현재 데이터에서 pair-LOOCV weighted R²는 +0.0892지만 LODO는 -0.1805,
L2DO는 -0.2548이야. 같은 도펀트 누수만으로 ΔR² = +0.344가 생겼어.

> 근거: 세 split의 직접 비교는
> `db/properties/codoping_ml_v2_meta.json:391-421`에 있어.

### 4.2 전처리와 모델 선택도 fold 안에서 해

- scaling의 mean/std는 train fold에서만 계산해.
- feature selection과 hyperparameter 선택도 train fold 안의 nested CV로 해.
- imputation도 train fold 통계만 사용해.
- acquisition threshold는 prospective 결과를 본 뒤 바꾸지 않아.
- 같은 원구조에서 파생한 augmentation은 전부 같은 fold에 넣어.

소표본에서는 복잡한 모델보다 ridge 같은 단순 baseline을 먼저 이겨야 해. TabPFN이나
비선형 모델을 붙이더라도 ridge·random ranking·physics-only Pareto와 같이 비교해.

> 근거: 현행 후속 계획도 ridge와 TabPFN을 LOOCV·X-randomization·농축배수로
> 비교하도록 잡혀 있어 (`kb/open_items.md:430-436`).

### 4.3 보고할 metric

R² 하나로 끝내지 않아.

- **Regression**: MAE/RMSE와 group-CV R²
- **Ranking**: Spearman, top-k overlap
- **Screening**: base rate 대비 top-k enrichment
- **Multi-objective**: Pareto recall, hypervolume improvement
- **Uncertainty**: interval coverage, calibration curve, error–uncertainty correlation
- **Reliability**: pipeline failure rate, out-of-domain fraction
- **Prospective**: 다음 round에서 실제로 살아남은 비율과 baseline 대비 improvement

소표본에서는 “정확도 90%”보다 **base rate와 랜덤 대비 농축배수**를 함께 말해.

> 근거: 현행 meta도 휴리스틱 재현 농축을 물성 적중률로 읽지 말라고 명시해
> (`db/properties/codoping_ml_v2_meta.json:284-287`).

---

## 5. Promotion contract

모델 이름보다 **어떤 지위로 배포할 수 있는지**를 먼저 정해.

| Level | 이름 | 필요한 증거 | 허용 표현 |
|---|---|---|---|
| H0 | Hypothesis generator | 실제 target label 없음 또는 휴리스틱 target만 있음 | “후보 우선순위를 제안해” |
| H1 | Internal surrogate | 실제 계산 label 확보, group-CV, 단순 baseline 비교 | “같은 host·protocol 안에서 다음 계산 후보를 줄여” |
| H2 | Prospective candidate selector | 동결된 다음 round에서 calibration·ranking 개선 재현 | “새 batch의 계산 우선순위 결정에 사용해” |
| H3 | Experiment-aware decision support | 표준화된 실험 반복·공정 메타데이터·외부 또는 시간 holdout | “명시된 domain 안에서 실험 후보 선정에 보조적으로 사용해” |

현재 co-doping ML v2는 **H0**야.

H0 → H1 승격 조건:

- 실제 공동치환 구조를 생성하고 계산한 label이 있어.
- 평균 행이 아니라 농도·configuration 원자료가 있어.
- LODO/L2DO 성능을 함께 보고해.
- ridge·random·physics-only baseline보다 나아.
- uncertainty와 실제 out-of-fold error의 관계를 확인해.
- 모델 카드에 host·조성·protocol domain을 적어.

H1 → H2 승격 조건:

- 다음 acquisition round를 보기 전에 후보·metric·threshold를 동결해.
- prospective 결과에서 ranking과 uncertainty calibration이 재현돼.
- high-score만 고른 batch보다 diversity·uncertainty routing이 이점을 보여.

H2 → H3 승격 조건:

- 실험 protocol과 batch metadata가 표준화돼.
- phase purity와 실제 조성을 확인해.
- 반복 실험의 산포를 보존해.
- 계산 성공과 합성 성공을 별도 target으로 다뤄.
- 명시한 domain 밖에서는 자동으로 low-confidence 또는 abstain을 내.

> 참고: disorder surrogate는 configuration 표본 9개 이상을 시작 trigger로 잡고 있고
> 현재는 3개야 (`kb/open_items.md:450-452`). **9개는 구현 시작선이지 검증 완료선이
> 아니야.** 공동치환 상위 5쌍 UMA 계산 계획도 첫 라벨 획득 pilot이지 예측기 검증
> 표본 수가 아니야 (`kb/open_items.md:443-448`).

---

## 6. 금지 주장

아래 문구는 promotion contract를 통과하기 전에는 쓰지 않아.

1. **“ML이 최적 도펀트/공동치환을 발견했어.”**
   - 현재는 큐레이션된 47종 안의 hypothesis ranking이야.
2. **“1,081개 공동치환을 계산·검증했어.”**
   - 열거와 점수화만 했고 실제 공동치환 label은 없어.
3. **“LOOCV R² = 0.9998이므로 물성 예측력이 높아.”**
   - 합성 score 항등식 복원이야.
4. **“모델 위원회가 동의하므로 DFT 정확도야.”**
   - 같은 functional 계열에서 같이 틀릴 수 있고 위원회도 실질 2진영이야.
5. **“UMA absolute energy/E/σ가 실험 또는 DFT와 일치해.”**
   - 현재 규율은 동일 UMA protocol 안의 상대 순위만 허용해.
6. **“BVSE channel이 넓으므로 절대 전도도가 높아.”**
   - BVSE는 정적 기하 proxy야.
7. **“91 → 47에서 44종을 물리적으로 제거했어.”**
   - canonical table 미수집 상태이고, 전종별 실패 manifest가 없어서 탈락 원인을 단정할 수 없어.
8. **“random split 성능이 새 도펀트 일반화 성능이야.”**
   - 같은 도펀트·configuration 누수가 생겨.
9. **“현재 모델이 새 host나 새 화학족에도 그대로 적용돼.”**
   - host-scoped domain이고 외부 화학 검증이 없어.
10. **“missing을 0으로 채워 보수적으로 학습했어.”**
    - 모름을 나쁨으로 바꿔 selection bias를 학습하게 돼.

> 근거: 현재 campaign이 믿는 것은 동일 protocol 내부의 판정·상대 순위·trade-off고,
> 믿지 않는 것은 UMA 절대값·BVSE 절대 σ·자의적 최종 승자야
> (`docs/cascade_pipeline_guide.md:389-405`).

---

## 7. 단계별 실행 계획

### Phase 0 — 현재 상태를 H0로 동결

할 일:

- `codoping_ml_v2.csv`와 meta를 versioned baseline으로 보존해.
- model status를 `HYPOTHESIS GENERATOR — NOT VALIDATED`로 유지해.
- 현재 feature, target, split, seed, output hash를 manifest로 남겨.
- 1,081개 pair는 “candidate universe”로만 등록해.

완료 기준:

- 같은 commit에서 산출물을 재생성할 수 있어.
- 웹앱·PPT·문서의 status 문구가 같아.

### Phase 1 — label ledger와 원자료 단위를 먼저 만들기

할 일:

- 273 실행을 candidate × concentration × configuration 단위로 backfill해.
- `complete/not_run/pipeline_failed/physical_failed/censored/not_applicable`를 분리해.
- score를 label과 분리하고 raw property provenance를 연결해.
- `comparison_group_id`와 `protocol_id`를 넣어.
- split manifest를 모델 학습 전에 생성해.

완료 기준:

- canonical table에 미수집된 44종을 negative label로 쓰지 않아.
- 평균·champion view를 원자료에서 다시 만들 수 있어.

### Phase 2 — 첫 공동치환 계산 label 만들기

한 batch에 아래 세 bucket을 같이 뽑아.

- 예상 Pareto 개선 상위 후보
- `ad_eps`가 크거나 committee disagreement가 큰 후보
- 화학족·산화수·charge-compensation이 드문 diverse 후보

각 pair에서:

- 실제 공동치환 슈퍼셀을 만들어.
- 가능한 site/configuration을 하나로 고정하지 말고 여러 개 둬.
- 농도축을 보존해.
- UMA relax·energy·force·convergence·phase identity를 기록해.
- BVSE와 gate 관련 관측량을 별도 label로 계산해.

주의:

- 이 단계의 UMA 결과는 **L1 label**이지 물리 truth가 아니야.
- 기존 “상위 5쌍” 계획은 첫 pilot로는 좋아도 predictive model의 검증 완료선은 아니야.

### Phase 3 — DFT calibration set 만들기

DFT 승격 우선순위:

1. gate threshold 근처
2. committee disagreement 상위
3. `ad_A=0` 또는 새로운 화학족
4. 전하·스핀·반응이 핵심인 사건
5. 예상 Pareto front의 대표 후보

같은 구조를 UMA와 DFT에 넣고 matched label을 만들어.

- single-point energy/force
- 필요한 경우 relax basin 유지 여부
- reaction energy
- electronic structure
- protocol별 discrepancy

그 뒤에야 `DFT − UMA` delta model과 committee calibration을 맞춰.

완료 기준:

- committee disagreement와 실제 DFT error의 상관·calibration을 보고해.
- 일치하지 않는다면 committee는 탐지 지표로만 남겨.

### Phase 4 — 첫 prospective active-learning round

학습 전에 아래를 동결해.

- candidate universe
- train/validation/test split
- acquisition bucket
- 평가 metric
- gate threshold와 abstention rule

비교할 baseline:

- random selection
- 현재 cascade score
- physics-only Pareto
- ridge
- 선택한 비선형 surrogate

다음 batch 결과를 본 뒤:

- top-k enrichment
- Pareto recall
- uncertainty coverage
- out-of-domain failure
- 계산비용 절감

을 비교해. 여기서 baseline을 이기고 calibration이 맞아야 H1 → H2를 논의해.

### Phase 5 — 실험 feedback 연결

첫 실험 batch는 계산상 1등만 보내지 않아.

- predicted Pareto 후보
- uncertainty가 낮은 control
- uncertainty가 높은 exploration 후보
- 기존 host/baseline

을 같이 보내. 실험에서는 최소한 아래를 되가져와.

- 합성 성공 여부
- phase purity
- 실제 조성
- σ(T)와 Ea
- 공기·전기화학 안정성 protocol
- pellet density·pressure·열처리·batch

계산 실패, 합성 실패, 물성 미달을 서로 다른 target으로 학습해. 실험 회차가 쌓이면
“좋은 물성”과 “실제로 만들 수 있음”을 별도 head로 두고 multi-objective selection을 해.

### Phase 6 — 배포

모델 artifact와 함께 아래를 묶어.

- dataset hash
- feature schema
- split manifest
- model card
- applicability domain
- calibration plot
- prospective result
- known failure modes
- promotion level

웹앱에는 score만 보여 주지 말고 최소한 아래를 같이 보여.

- prediction
- calibrated uncertainty
- `ad_d/ad_eps/ad_A`
- selection reason
- protocol/comparison group
- promotion level
- DFT·experiment validation status

---

## 8. Defense Q&A

### Q1. UMA도 ML인데 왜 “추후 ML 결합”이라고 해?

**A.** UMA는 이미 쓰는 pretrained ML potential이야. 원자 구조에서 에너지와 힘을
빠르게 계산해 configuration screening 비용을 줄여. 추후 결합하려는 ML은 우리
계산·실험 label로 “어떤 후보를 다음에 계산할지”를 배우는 project-specific
surrogate/active learner야. 입력·target·검증 계약이 달라서 둘을 구분해야 해.

근거: `docs/cascade_pipeline_guide.md:198-227`.

### Q2. 47개로 ML을 할 수 있어?

**A.** 같은 host 안에서 단순 모델로 후보 순서를 보조하는 건 가능해. 하지만 범용
discovery model이나 새 화학족 일반화를 주장하기엔 작아. 그래서 복잡한 모델보다
group-CV, random/X-randomization baseline, uncertainty calibration, prospective round가
더 중요해. 현재 47종은 대규모 발견 풀이 아니라 사람이 고른 조성족이야.

근거: `docs/cascade_pipeline_guide.md:91-129`,
`db/properties/codoping_ml_v2_meta.json:268-286`.

### Q3. 그러면 1,081개 공동치환을 스크리닝한 건 아니야?

**A.** 1,081개 조합을 **열거하고 가설 순위를 매긴 것**은 맞아. 하지만 실제
공동치환 구조의 계산·실험 label은 없어서 물성을 검증한 screening이라고 부르면 안 돼.
현 모델은 단일 도펀트 특징을 min/max/average로 합치고 휴리스틱 교호작용을 붙인
hypothesis generator야.

근거: `tools/cascade/codoping_ml.py:13-27`,
`db/properties/codoping_ml_v2_meta.json:432-438`.

### Q4. 모델 위원회 불일치를 uncertainty로 쓰면 충분해?

**A.** 후보 routing에는 쓸 수 있지만 실제 오차막대로 바로 쓰면 안 돼. MACE와
SevenNet은 훈련셋을 공유하고 UMA만 다른 훈련셋이라 위원회 독립성이 낮아. 세 모델이
같은 functional bias로 함께 틀릴 수도 있어. matched QE single point로
불일치와 실제 오차의 관계를 교정한 뒤에야 calibrated uncertainty라고 부를 수 있어.

근거: `db/properties/mlip_committee_baseline.json:19-23`,
`db/properties/mlip_committee_baseline.json:61-66`.

### Q5. random split이나 계산 실패를 negative label로 쓰면 왜 안 돼?

**A.** random split은 같은 도펀트·농도·configuration을 train과 test에 동시에 넣어
일반화 성능을 부풀려. 실제로 pair-CV는 L2DO보다 R²를 0.34 높게 보였어. 계산 실패도
물성이 나쁘다는 뜻이 아니야. 91 → 47의 44종은 canonical table에 미수집됐고 전종별
실패 manifest가 없어서 negative로 넣을 수 없어. 그렇게 넣으면 모델이 물리가 아니라
ingestion 상태를 배워. 그래서 group split과 상태 분리가 데이터 수보다 먼저야.

근거: `db/properties/codoping_ml_v2_meta.json:391-421`,
`docs/cascade_pipeline_guide.md:107-115`.

---

## 9. 실행 전 체크리스트

- [ ] UMA와 project-specific surrogate를 발표·코드·웹앱에서 구분했어?
- [ ] target이 실제 물성인지 합성 score인지 적었어?
- [ ] candidate × concentration × configuration 원자료가 있어?
- [ ] missing, pipeline failure, physical failure를 분리했어?
- [ ] 같은 chemistry가 train/test에 새지 않게 group split을 만들었어?
- [ ] scaling·feature selection·hyperparameter가 fold 안에서만 일어나?
- [ ] ridge·random·physics-only baseline과 비교해?
- [ ] uncertainty를 matched DFT error로 교정했어?
- [ ] acquisition에 exploit·explore·validate가 모두 들어가?
- [ ] prospective batch를 결과 보기 전에 동결했어?
- [ ] 실험 batch·공정 metadata를 보존해?
- [ ] model card에 host·protocol·적용영역·금지 주장을 적었어?
- [ ] promotion level(H0–H3)을 산출물에 표시했어?

이 체크리스트를 통과하지 못하면 모델을 없애라는 뜻은 아니야. **모델 지위를 H0로
낮춰서 가설 생성기로 쓰면 돼.** 가장 위험한 건 약한 모델이 아니라, 약한 증거에
강한 이름을 붙이는 거야.
