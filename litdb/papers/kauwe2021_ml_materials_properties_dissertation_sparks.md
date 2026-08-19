# Machine Learning of Materials Properties — Steven K. Kauwe 박사학위논문 (Univ. of Utah, 2021-05, 지도 Taylor D. Sparks)

> slug `kauwe2021_ml_materials_properties_dissertation_sparks` · DOI (장별, 아래 §2) · type `dft` (ML-on-DFT-data 방법론) · PDF `4cb486bf-Machine_Learning_of_Materials_.pdf` (96쪽) · digested `2026-08-19` · status 🟡 **부분 (2장·6장만)**

> elements: B, C, N, V, Co, Mo, Tc, Re, Os, Ir, W, Cs
> methods: DFT, elastic, band gap

<!-- ⚠ methods 태그 주석: 이 논문은 DFT를 **직접 돌리지 않는다.** AFLOW가 계산해 둔 DFT 물성
     (bulk/shear modulus, band gap, Debye T, 열전도·열팽창)을 ML의 타깃으로 소비한다.
     태그는 "DFT 물성을 다루는 논문"으로 라우팅하려는 것이고, 방법 주장은 아니다.
     elements 태그는 6장이 **결과로 뽑은** extraordinary 원소들(Fig. S6, Fig. S2)이다. -->

---

## 0. 이 카드의 진행 상태 (장별 페이스아웃)

1저자 지시(2026-08-19): 장별로 나눠 읽고 **같은 카드에 덧붙인다.**

| 장 | 제목 | 원 출처 | 문서쪽 | 이번 차수 |
|---|---|---|---|---|
| 1 | Introduction | — | 1–5 | ⬜ 미독 — 2차 예정 |
| **2** | **ML for Materials Scientists: A Guide toward Best Practices** | Wang et al., *Chem. Mater.* **32**, 4954–4965 (2020) | **6–18** | ✅ **읽음 (1차)** |
| 3 | ML Prediction of Heat Capacity for Solid Inorganics | Kauwe et al., *IMMI* **7**, 43–51 (2018) | 19–28 | ⬜ 미독 — 2차 예정 |
| 4 | Extracting Knowledge from DFT: Experimental Band Gap Predictions through Ensemble Learning | *IMMI* **9** (2020) 213–220 | 29–37 | ⬜ 미독 — 2차 예정 |
| 5 | Is Domain Knowledge Necessary for Learning Materials Properties? | Murdock et al., *IMMI* **9** (2020) 221–227 | 38–45 | ⬜ 미독 — 2차 예정 ★ (one-hot vs CBFV 정면 대결 — 우리 감사 항목 B의 원출처) |
| **6** | **Can Machine Learning Find Extraordinary Materials?** | Kauwe et al., *Comput. Mater. Sci.* **174**, 109498 (2020) | **46–53** | ✅ **읽음 (1차)** |
| 7 | The Compositionally-Restricted Attention-Based Network (CrabNet) | Wang et al., *npj Comput. Mater.* (2021) | 54–82 | ⬜ 미독 — 2차 예정 |
| 8 | Conclusion | — | 83– | ⬜ 미독 |

**쪽 번호 오프셋 (직접 확인함)**: **PDF쪽 = 문서쪽 + 12**.
근거 — PDF p13 = "CHAPTER 1 INTRODUCTION"(문서 1쪽, 쪽번호 미인쇄), PDF p14 하단 인쇄번호 = `2`,
PDF p18 = "CHAPTER 2"(문서 6쪽), PDF p58 = "CHAPTER 6"(문서 46쪽).
→ 2장 = PDF 18–30, 6장 = PDF 58–65. (다음 차수: 3장 = PDF 31–40, 4장 = 41–49, 5장 = 50–57, 7장 = 66–94.)

---

## 1. 한 줄 요약

**2장** = "재료 ML 논문을 쓸 때 지켜야 할 것" 프로토콜 문서 (데이터 누출·p-hacking·재현성 체크리스트).
**6장** = "ML이 학습 데이터 밖의 **비범한(top 1%)** 물질을 정말 찾아내는가"를 AFLOW DFT 물성 6종으로 실험 →
**찾는다** (recall ≈0.75–0.9, precision ≈0.55, 무작위 추측 6% 대비 ~9배), 단 **분류(classification)로 풀 때** 그렇고,
**학습에 없던 원소로 넘어가면 성능이 확 떨어지며**(PR-AUC 0.79 → 0.54), **도핑처럼 미세 조성 효과는 원리적으로 못 배운다**.

우리에게 이 논문의 값어치는 "좋은 리뷰"가 아니라 **우리 cascade ML predictor의 검사표**다. §8이 그 감사다.

---

## 2. 메타

| 항목 | 내용 |
|---|---|
| 저자 | Steven K. Kauwe (박사학위논문), 지도 Taylor D. Sparks (Univ. of Utah MSE) |
| 형식 | 논문-묶음형 학위논문 (published papers 재수록 + 장별 기여 진술) |
| 2장 원출처 | A. Y.-T. Wang, R. J. Murdock, **S. K. Kauwe**, A. O. Oliynyk, A. Gurlo, J. Brgoch, K. A. Persson, T. D. Sparks, *Chem. Mater.* **32**, 4954–4965 (2020). DOI 10.1021/acs.chemmater.0c01907. 코드: `github.com/anthony-wang/BestPractices` |
| 2장 내 기여 | Kauwe = best-practice 방법론 초안 작성·집필 지도·기술 검증·예제 구현/데이터 큐레이션 관리 |
| 6장 원출처 | **S. K. Kauwe**, J. Graser, R. Murdock, T. D. Sparks, *Comput. Mater. Sci.* **174**, 109498 (2020). DOI 10.1016/j.commatsci.2019.109498. 접수 2019-08-08 / 수정 2019-11-12 / 게재확정 2019-12-18. 코드: `github.com/kaaiian/can_machine_learning_find_extraordinary_materials` |
| 6장 내 기여 | Kauwe = 데이터 수집, 실험 설계·수행, 모델 선택, 원고 초안 |
| 조성/계 | (배터리 아님) AFLOW/ICSD 무기물 전반 — 결과로 뽑힌 원소: C·N·Re·W·B·Ir·Os·Mo·V·Co (AFLOW top1%), W·C·Ir·Re·N·Os·B·Tc (PCD 스크리닝), Cs (열팽창 withheld element) |
| 연구유형 | ML 방법론 + DFT 데이터 재사용 (자체 DFT/실험 없음) |
| 지원 | NSF CAREER DMR 1651668, CMMI-1562226, INL LDRD DE-AC07-05ID145142 |

---

# 3. 2장 — ML for Materials Scientists: A Guide toward Best Practices (문서 6–18쪽)

형식은 ACS *Chem. Mater.*의 **Methods/Protocols** 기사. 결과 논문이 아니라 **규범 문서**다.
동반 Jupyter 노트북 5개(`Table 1`)로 "열용량 예측"이라는 하나의 예제를 끝까지 따라가게 만들어 놨고,
본문에서 별표(*)가 붙은 절이 노트북과 짝이다.

`Fig. 1` — 전체 워크플로 도식. 실제로 보면 순서가 이렇다:
**Materials question → Data input/processing/integration → Data-driven research & feature engineering →
Machine Learning & Analysis → Knowledge → (Open-source contribution)**.
곁가지 두 개가 중요하다: 데이터 소스(온라인 DB / 데이터시트 / 기타)에서 들어오는 화살표에
**"Data validation" 박스**가 따로 달려 있고, 데이터 입력 단계 아래에 **"Local database"(로컬 아카이브)** 가
따로 그려져 있다. 즉 "원본을 그대로 박제해 두고, 검증을 거친 뒤에만 쓴다"가 그림 수준에서 강제돼 있다.

## 3.1 §2.3 Meaningful Machine Learning — 언제 ML을 **쓰지 말아야** 하나

> "Machine learning is a powerful tool, but not every materials science problem is a nail."

- ML이 이기는 곳: **사람이 배울 수 없는 곳** — 데이터와 그 안의 상호작용이 너무 복잡할 때.
- ML이 지는 곳: **데이터가 적을 때**. 사람 머리가 오히려 나을 때가 많다.
- ★ 우리에게 직격인 문장: **"당신 모델의 입력 특징이 DFT 계산이나 결정구조라면, 남들이 그냥 DFT를
  직접 돌리는 게 더 간단하지 않은가?"** — ML 모델의 존재 이유는 "원래 계산보다 싸야" 성립한다.
- 해석력 ↔ 예측력 트레이드오프: 물리·화학적 통찰을 원하면 신경망 같은 블랙박스에선 안 나온다.
- 좋은 ML 프로젝트가 해야 하는 것 (넷 중 하나 이상): ① 후보 스크리닝/down-select,
  ② 데이터 획득·처리로 새 통찰, ③ 새 모델링 접근 개념화, ④ 재료 특화 ML 탐색.

## 3.2 §2.5 Working with Materials Data ★ — **누출(leakage)의 원본 규정**

### (a) 데이터 소스
`Table 3` (물성 중심 저장소 16개) — 컬럼: 구조정보 / 기계 / 열 / 전자 물성 / API / 데이터 라이선스.

| 저장소 | 구조 | 기계 | 열 | 전자 | API | 라이선스 |
|---|---|---|---|---|---|---|
| Materials Project | Y | Y | Y | Y | Y | CC BY 4.0 |
| OQMD | Y | N | Y | Y | Y | CC BY 4.0 |
| AFLOW | Y | Y | Y | Y | Y | 미지정 |
| NOMAD | Y | Y | Y | Y | Y | CC BY 4.0 |
| Open Materials Database | Y | N | Y | Y | Y | CC BY 4.0 |
| Citrine Informatics | Y | Y | Y | Y | Y | CC BY |
| MPDS | Y | Y | Y | Y | Y | CC BY 4.0 |
| AiiDA/Materials Cloud | Y | Y | Y | Y | Y | Varies |
| NREL MatDB | Y | N | Y | Y | N | 자체 |
| NIST TRC Alloy Data | N | N | Y | N | 요청시 | Free |
| NIST TRC ThermoData | N | N | Y | N | N | NIST SRD |
| NIST JARVIS-DFT/-ML | Y | Y | Y | Y | Y | Public domain |
| MatWeb / Total Materia / Ansys Granta / MATDAT | N | Y | Y | N | N | 유료 |

`Table 4` (구조 중심 저장소, 레코드 수는 2020-05 기준):
CSD 1,055,780 (API O, 유료) · ICSD 216,302 (API X, 유료) · **PCD 335,000** (API X, 유료) ·
ICDD 1,004,568 (유료) · COD 455,714 (API O, **오픈**) · Pauling File 357,612 (API O, 유료) · CrystMet 160,000 (유료).

⚠ 경고: **저장소마다 측정·계산·큐레이션 방법이 달라 물성 값이 서로 직접 비교 가능하지 않다.**
합치거나 병합할 계획이면 이걸 먼저 의심하라. (우리 CLAUDE.md의 "문헌 수치는 소환값 — 우리 db 절대값과
섞지 않기"와 정확히 같은 규율이다.)

### (b) 데이터셋 크기·구성 — **군집(cluster) 편향**
> "Does your data form clusters based on **chemical formula, test condition, structure type**, or other criteria?
> Are some clusters greatly over- or under-represented?"

- 대부분의 ML 통계 모델은 빈도주의라 **불균형·편향에 그대로 끌려간다.**
- 진단 도구로 **t-SNE, UMAP, 그리고 원소 출현빈도(element prevalence) 매핑**을 권한다 → `Fig. 5`(히스토그램), `Fig. 6`(주기율표 히트맵).
- 데이터가 너무 크면 "toy data set"으로 프로토타이핑하되 **샘플링이 편향을 새로 만들지 않게** 하라.

### (c) 데이터 버전 관리
원본(raw) 사본을 **아카이브해 언제든 되찾을 수 있게** 하고, 변경은 **재현 가능한 절차로 기록**하라 (Git/Mercurial/SVN).

### (d) 정리·전처리
NaN·비현실적 음수/양수·이상치·무한대·인코딩 깨짐·숫자가 문자열로 저장된 것·저장소 스키마 변경으로 인한 포맷 불일치.
**모든 정리 단계를 문서화**하라 — "ML 연구에서 자주 빠뜨리는, 재현성의 핵심 단계".

### (e) ★★ Train–Validation–Test Split — 누출 규정 (이 카드에서 가장 중요한 단락)

> "Split your data **once** into three data sets: train, validation, and test."
> "**Make sure that no same (or similar) data appear in the test data set, if they are already present
> in the train or validation data set.** For example, if you have several measurements of a chemical
> compound that are performed at different measurement conditions in the train data set (e.g. temperature
> or pressure), during the testing phase, your model would likely perform well if it is asked to predict
> the property of the same compound at a different condition. **This, however, gives you an inflated
> estimate of how well the model will generalize** in cases where it has not seen a particular chemical
> compound before. For a truly rigorous evaluation of your model's generalization performance, you should
> take care to avoid this **data leakage** when you split your data."

정리하면:
1. **한 번만** 나눈다. 재현 가능하게(시드+셔플) 또는 분할 결과를 파일로 저장.
2. **같거나 비슷한 데이터가 train/val과 test에 동시에 있으면 안 된다.** 논문이 든 예가 "같은 화합물의
   다른 측정 조건" — 즉 **화합물(=종) 단위로 묶어서 갈라야 한다**는 뜻이다.
3. train = 학습만, validation = 하이퍼파라미터 튜닝, **test = 최종 1회 평가만.** 테스트로 학습·튜닝 금지.
4. **모든 모델 비교·벤치마킹에 동일한 분할을 쓴다.**
5. k-fold CV는 **train 안에서** 하는 것 (test 대체가 아니다). 통상 K = 5 또는 10. 분할 세부를 기록하라.

⚠ **이 논문은 "누출되면 R²가 얼마나 부풀려지는지" 숫자를 주지 않는다.** 정성적 경고("inflated estimate")만
있다. 동반 노트북 3번이 "effect of different train/validation/test splits"를 다룬다고 `Table 1`에 적혀 있으나
본문에 수치는 없다. → 그래서 **우리 데이터로 직접 계산했다(§8.0).**

## 3.3 §2.6 Modeling — 특징·모델·스케일링

- **데이터 크기가 모델을 정한다.** 소규모 → 회귀·SVM·kNN·의사결정나무(+ bagging/boosting/stacking, scikit-learn).
  신경망은 **수천 점 이상**부터 쓸 만해진다.
- **특징공학은 소규모에서 크게 남는다.** 조성 기반 특징 벡터(**CBFV**) 종류: **Jarvis, Magpie, mat2vec, Oliynyk**.
  대안으로 원소 one-hot 인코딩.
- ★ **"데이터가 충분히 크고 모델이 충분히 유능하면(깊은 FC망, CrabNet 같은 attention 구조)
  CBFV로 도메인 지식을 넣는 게 무의미해지고 단순 one-hot과 차이가 없다"** — 뒤집으면
  **작은 데이터 + 단순 모델에서는 one-hot이 CBFV보다 불리하다.** (근거는 5장 Murdock et al. — 미독)
- **스케일링**: X' = (X − X̄)/σ_X. **반드시 train 통계로만** 계산해 val/test에 적용. log 변환이 도움이 될 때가 있음.
  **스케일링과 정규화는 교환 불가 — scale → normalize 순서, 되돌릴 땐 unnormalize → unscale.**
- **Keep it simple**: 소규모에선 ridge/lasso·RF·kNN이 복잡한 모델을 이기는 경우가 흔하다.
- **하이퍼파라미터**: 모델이 학습하는 게 아니라 사람이 고르는 것. grid search를 **validation set**으로.
- **평가 지표**: 분류 = accuracy, log loss, precision, recall, F1, ROC, AUC / 회귀 = r², MAE, (R)MSE. + CV.
- **Show Your Model**: 전체 소스, 하이퍼파라미터, **사용한 랜덤 시드**, 사전학습 가중치, 구조 도식, 재현 절차.

## 3.4 §2.7 Fitting and Testing ★

1. **과적합 회피**: 학습오차는 0으로 가지만 그건 우리가 보는 지표가 아니다. **validation 오차가 다시 올라가면
   외우고 있는 것.** 신경망은 학습곡선으로 추적 → `Fig. 4`.
   과적합이 쉽게 나면 **모델 복잡도를 줄이거나 정규화**하라.
2. **랜덤 초기화 주의**: sklearn의 선형회귀·RF·SVM·부스팅, 신경망 가중치/편향/옵티마이저 모두
   시스템 난수에 의존한다. **시드를 고정하고, 그 시드를 논문과 코드에 밝혀라.**
3. **p-hacking 금지**: 학습은 train, 튜닝은 validation. **튜닝이 끝날 때까지 test를 보지 마라.
   test를 여러 번 들여다보며 하이퍼파라미터를 고르는 것은 p-hacking이고 부정행위다(cheating).**

## 3.5 §2.8 Benchmarking and Testing ★

1. **비교/ablation은 동일한 train/val/test 분할로.**
2. **가장 공정한 비교는 남의 모델을 직접 돌려 보는 것.** 모델별 추가 데이터 조작이 있으면 문서화하고 재현 가능하게.
3. ★ **절차**: 튜닝 동안엔 train으로 학습 → validation으로 평가. **구조·하이퍼파라미터를 확정한 뒤
   train+validation을 합쳐 다시 학습하고, 그 모델을 test로 한 번 평가한다.**
4. ★★ **Existing Benchmarks (= 더미/베이스라인 권고의 실제 형태)**:
   > "There are some tools and software packages online that can be used as **baselines to judge the
   > performance of your models**. Some of these tools can perform automatic feature engineering and testing
   > of several different ML models. **We suggest that you download these tools and compare the performance
   > of your models against them. If your model does not perform better or does not offer any advantages
   > over these existing tools, consider other venues of improvement.**"

   ⚠ 정확히 말하면 **"DummyRegressor 같은 무지성 베이스라인과 비교하라"는 문구는 2장에 없다.**
   2장이 요구하는 베이스라인은 **AutoML/기성 툴킷**이다. "무작위 추측 대비 몇 배"라는 형태의
   trivial baseline은 **6장 §6.4.3의 Scenario 1** (무작위 추측 6%)이 담당한다. 둘 다 우리에게 필요하다.

## 3.6 §2.9 Making Publication-Ready, Reproducible Work ★ (체크리스트 그대로)

| # | 요구 | 세부 |
|---|---|---|
| 1 | **소스코드 전량** | 데이터 처리·정리·**분할**·학습·평가 구현이 전부 포함. 가능하면 permissive/오픈소스 라이선스 |
| 2 | **그대로 실행하면 같은 결과** | 의존 라이브러리 **버전 번호까지** 명시, 가능하면 **environment 파일**로. 남의 코드 라이선스 준수. GitHub/GitLab/Bitbucket/DLHub 등 버전관리 호스팅 |
| 3 | **문서화** | PEP 8 등 표준 준수, 주석보다 **자명한 코드**(명확한 변수명, explicit), 설치·사용·**재현 절차가 든 README**. 대규모 배포엔 Docker 컨테이너 |
| 4 | **데이터 전량 제공** | 결과·데이터셋 전부, 가능하면 raw까지. 라이선스로 불가능하면 **이유를 밝히고** 부분/익명 데이터·가중치·획득 절차라도 제공 |
| 5 | **학습된 모델·가중치** | **시험해 본 모든 하이퍼파라미터 기록** + 최종 최적값. NN 가중치와 구조 재생성 코드. 사용자가 자기 입력으로 예측해 볼 수 있는 친절한 경로 |
| 6 | **시각화 재현성** | 논문의 모든 그림이 공개 코드로 재생성 가능해야. SI 그림은 그것만 보고도 이해되게 |

**MI 연구가 통상 실어야 하는 그림 4종** (이게 §2.9가 명시한 "보고 항목"이다):
`Fig. 2` 예측 vs 실측 (+ marginal histogram) · `Fig. 3` 잔차 산점도 + 잔차 히스토그램(kde) ·
`Fig. 4` 학습/검증 손실 곡선 · `Fig. 5`,`Fig. 6` 원소 출현빈도(히스토그램 / 주기율표 히트맵).

## 3.7 §2.10 Benchmark Data Sets ★

- MI에는 **공표된 train/val/test 분할이 거의 없다** → 공정한 벤치마크가 불가능하다.
  비교 대상: 컴퓨터비전의 CIFAR·Google Open Images·CelebFaces·ImageNet, NLP의 Glue·decaNLP·WMT 2014 EN-DE.
- 재료 데이터셋은 **이질성(물질 클래스·물성 종류·원소 다양성)이 제각각이고 대체로 좁다.**
- 일부 데이터는 **접근 제한/독점 라이선스**라 공유가 막힌다.
- ★ **온라인 저장소가 "체크포인트 상태"를 제공하지 않는다** — 저장소는 언제든 바뀌고 과거 상태로
  되돌릴 방법이 없다. 그래서 현업 연구자들은 **내려받아 로컬에 박제해 놓고** 벤치마크를 돌린다.
  (→ 우리가 `db/properties/*.csv`를 repo에 박아 두는 관행이 바로 이 권고와 일치한다.)

---

# 4. 6장 — Can Machine Learning Find Extraordinary Materials? (문서 46–53쪽)

## 4.1 질문과 답

**질문**: ML의 가장 흔한 비판 — "모델은 외삽을 못 한다, 즉 학습 데이터에 없던 수준의 물성을 가진
물질은 못 찾는다." 이게 사실인가?

배경 가정이 **i.i.d.** (독립 동일분포)다. 재료 데이터는 i.i.d.가 아니다 — 합성/계산이 쉬운 것,
관심 있는 것, 값싼 것에 편향돼 있다. 그래서 "애초에 물리적으로 비범함을 판정할 정보가 데이터에 있나?"를 묻는다.

**답**: 있다 — 단, **최선의 조건(DFT 데이터, 다양·잘 분포된 물성)에서**. 그리고 **분류로 풀 때** 더 낫다.

## 4.2 실험 설계 (전부 수치로)

| 항목 | 내용 |
|---|---|
| 데이터 출처 | **AFLOWlib.org**, ICSD 구조 기반 계산값. 중복은 ICSD 번호로 정렬해 **마지막 항목만** 남김 |
| 물성 6종 | bulk modulus **B**, shear modulus **G**, thermal conductivity **κ**, thermal expansion **α**, band gap **E_g**, Debye temperature **T_D** |
| 타깃 변환 | T_D, κ, G, α 는 **log10** 적용 (정규분포에 가깝게) |
| 특징 | **CBFV** — 원소 물성의 **average · range · variance** (조성 가중). scikit-learn `StandardScaler` + `Normalizer`, **train 통계로만** |
| "extraordinary" 정의 | ★ **데이터셋 물성 상위 1%** (임계값이 아니라 **분위수**) |
| test set 구성 | 상위 1% **전부**(100%) + 하위 99%에서 **무작위 15%** |
| train set 구성 | 나머지(하위 99%의 85%). 그 안에서 **상위 6%**에 'extraordinary' 라벨을 붙여 test와 라벨 비율을 맞춤 |
| 외삽 거리 조작 ① gap | extraordinary 임계 **아래로 4% / 8% / 12%** 를 학습에서 제거 (인공 공백) |
| 외삽 거리 조작 ② element | gap + **extraordinary에서 가장 흔한 원소를 포함한 화합물 전부** 학습에서 제거 |
| 외삽 거리 조작 ③ structure | gap + **가장 흔한 "structure type" 제거**. structure type ≡ **공간군 + 단위셀 원자수** (예: 221-2) |
| 모델 | 회귀: **ridge regression**, **SVR(rbf)** / 분류: **logistic regression**, **SVC(rbf)** / 베이스라인: **nearest-neighbor 회귀(nnr)·분류(nnc)** (조성 벡터 euclidean 최근접) |
| 구현 | scikit-learn, grid search로 파라미터 최적화 |
| 임계값 | 분류기는 기본 0.5. **회귀는 train 데이터에서 F1을 최적화**해 임계값 결정 |
| 지표 | precision = tp/(tp+fp), recall = tp/(tp+fn), F1 = 2·(P·R)/(P+R), 그리고 **임계값-무관 지표인 precision–recall AUC** (불균형 데이터에 강건) |
| 반복 | 하위 99%의 train-test 분할을 **랜덤 시드 5개**로 반복 → 그림 음영 = 표준편차 |
| 외부 적용 | **PCD 156,421** 조성 + **elpasolite 10,590** 계산 조성에 최종(분류) 모델 적용 |

## 4.3 결과 — 그림에서 읽은 수치

### `Fig. S1` (= 학위논문 Fig. 6.1) — extraordinary 정의와 분할
Bulk modulus 히스토그램. x축 "Bulk Modulus"(GPa 라벨 없음, 0–450 범위), y축 발생 횟수(최빈 ≈265).
초록 음영(=extraordinary)이 **figure-read ≈ 315 GPa** 부터. 아래에 분할 도식: 하위 99%의
**85% → train**, **15% → test**, 상위 1%는 **100% → test**.
※ 분포 모양(오른쪽 꼬리가 긴 단봉)에서 보면 데이터 규모는 대략 수천 개 수준 (§4.5 검산 참조).

### `Fig. S2` (= Fig. 6.2) — 외삽 3종을 한 그림에
x = Log Thermal Expansion (≈ −11.5 … −7.5), y = Predicted Log Thermal Expansion (≈ −11.5 … −8.0).
가로 파선 = threshold **figure-read ≈ −9.45**, 세로 점선 = extraordinary 경계 **figure-read ≈ −8.6**,
빗금 = artificial gap (**≈ −9.2 … −8.6**). 노란 점 = **element: Cs**, 빨간 원 = **space group: 221-2**.
사분면 색: 좌상 파랑 = 위양성, 우상 초록 = 참양성, 우하 자주 = 위음성.

⚠ **본문–그림 불일치 (검증 결과)**: §6.3 본문은 이 그림을 "**boron-containing structures when predicting
shear modulus** in Figure 2"라고 가리킨다. 그런데 실제 `Fig. S2`는 **Cs / 열팽창**이다.
구조 조건(빨강 = 221-2)만 본문과 맞는다. → 본문 괄호가 옛 버전 그림을 가리킨 채 남은 것으로 보인다. §6에 기록.

### `Fig. S3` (= Fig. 6.3) — bulk modulus, 회귀 vs 분류 한 판
(a) ridge 회귀: x = Bulk Modulus (GPa) 0–450, y = Predicted (GPa). 가로 파선 threshold **figure-read ≈ 203 GPa**,
세로 점선 extraordinary 경계 **≈ 315 GPa**. 사분면 비율(범례에 인쇄):
**위음성 1% · 위양성 4% · 참양성 5% · 참음성 90%**.
(b) logistic 분류: y = Probability of Being Extraordinary (0–1), 임계 0.5.
사분면: **위음성 0% · 위양성 3% · 참양성 6% · 참음성 91%**.
캡션이 명시: "All data in the training set has values lower than 300 GPa."

→ 분류가 위양성 4%→3%, 위음성 1%→0%. 같은 데이터에서 분류가 회귀보다 낫다는 게 **한 그림 안에서** 보인다.

### `Fig. S4` (= Fig. 6.4) — ★ 핵심 성능 그림 (3패널: Precision / Recall / F1, x축 = 물성 B, κ, G, E_g, T_D, α)
4개 모델: **Ridge(빨강 실선 ×) · SVR(파랑 실선 ■) · Logistic(초록 파선 ◆) · SVC(주황 파선 ★)**.
음영 = 시드 5개의 표준편차. 실선 = 회귀, 파선 = 분류.

**figure-read ≈ (내가 눈으로 읽은 값, 소수 둘째자리는 ±0.02 수준)**

| 지표 | 모델 | B | κ | G | E_g | T_D | α | 평균 |
|---|---|---|---|---|---|---|---|---|
| Precision | Ridge | 0.47 | 0.41 | 0.375 | 0.32 | 0.385 | 0.40 | **≈0.39** |
| | SVR | 0.525 | 0.415 | 0.425 | 0.375 | 0.485 | 0.40 | **≈0.44** |
| | **Logistic** | 0.575 | 0.60 | 0.545 | 0.565 | 0.555 | 0.51 | **≈0.56** |
| | **SVC** | 0.59 | 0.63 | 0.565 | 0.54 | 0.57 | 0.50 | **≈0.57** |
| Recall | Ridge | 0.90 | 0.78 | 0.90 | 0.92 | 0.86 | 0.87 | **≈0.87** |
| | SVR | 0.895 | 0.945 | 0.755 | 0.925 | 0.745 | 0.865 | **≈0.86** |
| | **Logistic** | 0.985 | 0.765 | 0.805 | 0.86 | 0.915 | 0.90 | **≈0.87** |
| | **SVC** | 0.90 | 0.755 | 0.685 | 0.83 | 0.92 | 0.845 | **≈0.82** |
| F1 | Ridge | 0.615 | 0.545 | 0.53 | 0.48 | 0.51 | 0.545 | **≈0.54** |
| | SVR | 0.66 | 0.57 | 0.54 | 0.535 | 0.57 | 0.545 | **≈0.57** |
| | **Logistic** | 0.725 | 0.665 | 0.65 | 0.685 | 0.70 | 0.645 | **≈0.68** |
| | **SVC** | 0.715 | 0.685 | 0.605 | 0.655 | 0.695 | 0.62 | **≈0.66** |

읽히는 것:
- **분류 두 개가 precision에서 회귀 두 개를 전 물성에서 이긴다** (≈0.56 vs ≈0.39–0.44), recall은 사실상 동률.
  → 본문 §6.4.2 "classification is almost always superior … consistently higher precision and a nearly
  equivalent recall"과 그림이 일치한다.
- 시드 산포(음영)가 **Ridge의 T_D·α, SVR의 T_D·E_g, SVC의 G**에서 특히 넓다 (recall 패널에서 폭 ±0.2 이상).
  즉 **단일 시드로 이 순위를 논하면 안 된다** — 우리 MSD 규율("단일시드 판정 금지")과 같은 결론.

### `Fig. S5` (= Fig. 6.5) — 외삽 거리를 늘렸을 때 (물성 평균 PR-AUC)
3패널: (좌) all data, (중) element removed, (우) structure removed. x = gap size (% data) 0/4/8/12.
모델 4종: Ridge(빨강) · Logistic(파랑) · **nnr(초록 파선)** · **nnc(자주 파선)**.

| 패널 | 모델 | gap 0 | 4 | 8 | 12 |
|---|---|---|---|---|---|
| all data | Logistic | ≈0.79 | ≈0.69 | ≈0.76 | ≈0.69 |
| | Ridge | ≈0.68 | ≈0.63 | ≈0.64 | ≈0.64 |
| | nnr | ≈0.655 | ≈0.355 | ≈0.315 | ≈0.315 |
| | nnc | ≈0.365 | ≈0.215 | ≈0.19 | ≈0.18 |
| **element removed** | Logistic | **≈0.54** | ≈0.52 | ≈0.67 | ≈0.61 |
| | Ridge | **≈0.445** | ≈0.585 | ≈0.635 | ≈0.645 |
| | nnr | ≈0.26 | ≈0.18 | ≈0.20 | ≈0.24 |
| | nnc | ≈0.13 | ≈0.10 | ≈0.115 | ≈0.14 |
| structure removed | Logistic | ≈0.775 | ≈0.755 | ≈0.71 | ≈0.715 |
| | Ridge | ≈0.665 | ≈0.625 | ≈0.62 | ≈0.64 |
| | nnr | ≈0.61 | ≈0.35 | ≈0.30 | ≈0.31 |
| | nnc | ≈0.35 | ≈0.245 | ≈0.175 | ≈0.17 |

★ **이 그림이 우리에게 제일 중요하다**:
1. **gap(값의 공백)은 별 타격이 없다** — Logistic 0.79 → 0.69, Ridge 0.68 → 0.64로 거의 평평.
2. **"가장 흔한 원소를 빼는 것"이 진짜 타격이다** — gap 0에서 Logistic **0.79 → 0.54 (상대 −32%)**,
   Ridge **0.68 → 0.445 (−35%)**. 즉 **"본 적 없는 화학"으로 넘어갈 때 성능이 무너진다.**
3. **구조 제거는 거의 영향이 없다** (0.79 → 0.775). 본문 스스로 해석하길, **"공간군+원자수"라는
   structure type 정의가 구조를 기술하기에 부적절**해서일 가능성이 크다 — 즉 이 실험은
   "구조 외삽은 쉽다"의 근거가 **아니다**.
4. **nnr/nnc(최근접이웃 = "화학적 직관 자동화")는 gap이 4%만 생겨도 반토막**난다 (0.655 → 0.355).
   학습된 모델과의 격차는 외삽을 밀수록 벌어진다.
5. 이상 현상: element removed 패널에서 **Ridge가 gap이 커질수록 좋아진다**(0.445 → 0.645).
   본문 설명은 "경계 근처 화합물이 오라벨될 확률이 제일 높은데 gap이 그들을 제거해 준다" — 손으로 쓴 설명이고
   검증은 없다.

### `Fig. S6` (= Fig. 6.6) — AFLOW top1% vs PCD 스크리닝 결과의 원소 순위
위(초록) **AFLOW top 1%**: C 15, N 13, Re 10, W 8, B 6, Ir 6, Os 5, Mo 3, V 2, Co 2 (막대 위 숫자 = 개수, y축은 비율).
아래(주황) **PCD Screened**: W 56, C 47, Ir 42, Re 37, N 24, Os 23, B 15, Tc 5.

→ **원소 목록은 거의 같은데 순위·비율이 완전히 다르다** (C 1위 → W 1위, Mo·V·Co는 사라지고 Tc가 등장).
본문 결론: "학습 데이터와 실제 합성된 화합물 사이에 **parity(대응)가 없다**."
그리고 **PCD 조성 중 extraordinary로 예측된 것은 0.1% 미만**인데 학습 데이터는 상위 1%를 라벨했다 —
**분포가 어긋나 있다는 직접 증거.** elpasolite 10,590개에 대해서는 **단 하나도 extraordinary로 라벨되지 않아
비교 자체가 불가능했다.**

## 4.4 §6.4.3 — 4개 시나리오 (베이스라인 논증의 형식) ★

우리가 그대로 베낄 수 있는 "베이스라인 사다리"다.

| 시나리오 | 내용 | 성능 |
|---|---|---|
| **1. 무작위 추측** | test set의 extraordinary 비율이 곧 성공률 | **≈ 1/15 ≈ 6%** |
| **2. 화학적 직관** | 연구자의 도메인 지식·문헌 흡수. 실제 현업의 modus operandi | 정량화 불가, **가변적·주관적**, 느리고 **국소 최적**에 갇힌다 (MGI가 재고를 촉구) |
| **3. 최근접이웃** | "비슷한 화학은 비슷한 물성" — 시나리오 2의 자동화판. 조성 벡터 euclidean 최근접의 값을 그대로 부여 | PR-AUC ≈0.36–0.66, **gap이 생기면 급락** (`Fig. S5`) |
| **4. ML 예측 + 도메인 지식** | 학습 모델의 후보 목록을 받아, 그중 **통상 연구되지 않는 화학/구조**에 집중 | **precision ≈0.5 → 두 개 제안하면 하나가 진짜**, **recall ≈0.75+** |

논문 자신의 문장: "every other compound suggested would be extraordinary!" — 단, 바로 다음 문장에서
"we explain why this will likely have reduced efficacy"라고 스스로 깎아 놓는다(§6.4.4).

## 4.5 검산 (내가 직접 확인한 것)

| 검산 | 결과 |
|---|---|
| test set의 extraordinary 비율 | 상위 1% 전부 + 하위 99%의 15% → 0.01/(0.01+0.15×0.99) = **6.31%**. 논문의 "1/15 ≈ 6%"(=6.67%)는 0.99≈1로 근사한 값. **`Fig. S3`의 사분면(TP+FN = 5+1 = 6%, 6+0 = 6%)과 일치** ✅ |
| precision lift | 분류 precision ≈0.56 ÷ 무작위 0.063 = **≈8.9배** (논문은 배수를 안 쓴다) |
| `Fig. S6` 정규화 | AFLOW 개수 합 15+13+10+8+6+6+5+3+2+2 = **70**; 15/70=0.214 = 막대높이 ✅. PCD 합 56+47+42+37+24+23+15+5 = **249**; 56/249=0.225 ✅ → 두 패널 모두 **자기 개수 합으로 정규화**한 비율이 맞다 |
| "PCD의 0.1% 미만" | 249 원소-출현 ÷ (화합물당 ~2원소) ≈ **125 화합물** / 156,421 = **0.080%** → "<0.1%" **자기일관** ✅ |
| AFLOW top1% 규모 | 70 원소-출현 ÷ ~1.75 = **≈40 화합물** = top 1% → 원 데이터셋 ≈ **4,000 화합물** (`Fig. S1` 히스토그램 규모와 일치) ✅ |
| ⚠ **recall 수치 불일치** | 초록 "identify **3/4**", §6.4.3 "recall values are typically **0.75 or greater**", `Fig. S4` figure-read 평균 **≈0.82–0.87**, 그런데 **결론(§6.5)은 "average recall ~0.6"**. → **세 값이 서로 안 맞는다.** 그림이 뒷받침하는 건 0.75–0.87이고, **결론의 0.6은 어느 그림·표에서도 나오지 않는다** ❌ |
| ⚠ "precision typically above 0.5" | **분류만 참**(Logistic ≈0.56, SVC ≈0.57). **회귀는 평균 ≈0.39–0.44로 0.5 미만** — 초록이 모델을 구분하지 않아 과대 진술 ❌ |
| ⚠ `Fig. S3a` ↔ `Fig. S4` | 사분면 비율로 역산한 ridge-B precision = 5/9 = **0.556**, recall = 5/6 = **0.833**. 그런데 `Fig. S4`의 Ridge-B는 **precision ≈0.47, recall ≈0.90**. 1% 단위 반올림 + 단일시드 vs 5시드 평균으로 설명 가능하지만 **논문은 이 대조를 하지 않는다** |

## 4.6 §6.4.4 Limitations — 저자 자신의 경고 (우리에게 제일 중요한 절)

1. **메커니즘의 벽**: 학습 데이터와 **같은 메커니즘**으로 기록을 깨는 물질은 찾을 수 있다.
   **새로운 메커니즘**으로 비범해지는 물질은 못 찾는다. 예시가 강렬하다 —
   *BCS 초전도체를 아무리 많이 학습시켜도 큐프레이트 고온초전도체는 후보로 안 나온다.*
   반대로 **일관되게 못 맞히는 화학군**이 있으면 "우리 서술자가 그 물리를 못 담고 있다"는 신호로 읽어
   물리적 통찰의 단서로 쓰라는 제안도 한다.
2. **i.i.d. 붕괴 / 데이터 인프라 부족**: 이질성, 측정·계산 자체의 오차, 클래스 불균형, 희소성,
   **고성능 물질 쪽으로의 편향**. Babbage 인용("쓰레기를 넣고 정답이 나오길 바라는가").
   후보 목록을 어떻게 생성하느냐도 문제 — PCD(실존 화합물) vs elpasolite(가상 조성) 예시.
3. **복합재를 못 다룬다**: 입력이 단일 화합물의 화학식이라, 페라이트+세멘타이트(강)나 석출경화 알루미늄처럼
   **상들의 시너지로 물성이 나오는 재료**는 표현이 안 된다. 저자들이 아는 한 그런 예측 사례가 문헌에 없다.
4. ★★ **희소 사건 = 도핑을 못 다룬다**:
   > "A related problem is associated with **rare events such as doping** where a few percent elemental
   > substitution can lead to drastic changes in properties due to complicated defect chemistry.
   > For instance, doping silicon with phosphorus from 10¹² cm⁻³ (~0%) up to 10²¹ cm⁻³ (~2%) is accompanied
   > by a change of electrical conductivity approximately **eight orders of magnitude**!"
   > "…**a database of stoichiometric compounds will not be able to predict the influence of doping**,
   > but rather, it will require a database where **many slight dopant compositions are reported with an
   > associated material property**."

   → **이 문단이 우리 cascade의 존재 이유를 정확히 서술한다.** Kauwe의 결론은 "도핑은 ML이 원리적으로
   불가능"이 아니라 **"도핑 농도가 촘촘히 라벨된 데이터베이스가 있어야 가능하다"**이다.
   우리가 만들고 있는 게 바로 그 데이터베이스다 — 다만 §8.0에서 보듯 **지금 우리 CSV의 농도 컬럼은 상수다.**

---

## 5. Figure set ★

> ⚠ **번호 규약 (이 카드 한정)**: 학위논문은 그림을 `2.1`·`6.3`처럼 **장.번호**로 매기는데,
> webapp의 링크 정규식이 `Fig. 6.3` 형태를 잡지 못한다(점 뒤 숫자에서 매칭이 끊긴다).
> 그래서 **본문 그림 = 2장(`Fig. 1`–`Fig. 6` = 학위논문 Fig. 2.1–2.6)**,
> **S 번호 = 6장(`Fig. S1`–`Fig. S6` = 학위논문 Fig. 6.1–6.6)** 으로 매핑했다.
> **S는 supplementary가 아니다** (이 학위논문 PDF에는 SI가 없다). 장 안 번호는 1:1로 보존된다(S3 = 6.3).

| Fig | 내용 (무엇을 보여주나) | 우리 활용 |
|---|---|---|
| 1 | (=Fig. 2.1) 재료 ML 워크플로 도식. Materials question → data input/processing → feature engineering → ML → Knowledge → open-source. **Data validation 박스**와 **Local database(원본 박제)** 가 별도 분기 | 우리 cascade 문서 그림의 뼈대. "원본 박제 + 검증 게이트"가 그림에 명시돼 있다는 점이 인용 포인트 |
| 2 | (=Fig. 2.2) 예측 vs 실측 표준 그림, marginal histogram 유무 비교. ideal 파선 + linear fit. **선형 fit이 고값 쪽에서 ideal 아래로 처진다** (회귀의 평균 회귀 현상) | 우리 predictor 출력에 **없는** 그림. §8.3-①에서 추가 권고. 고값 처짐은 "상위 후보를 과소예측한다"는 우리 스크리닝의 약점과 직결 |
| 3 | (=Fig. 2.3) 잔차 그림 2종: 잔차 vs 실측(왼쪽), 잔차 히스토그램+kde(오른쪽). 왼쪽에서 **고값 쪽 잔차가 음으로 벌어지는 이분산**이 뚜렷 | 같은 이유로 필수. B0/E_young 예측의 잔차를 실측값에 대해 그리면 "winner 편향"이 눈으로 보인다 |
| 4 | (=Fig. 2.4) 학습/검증 손실 곡선 (0–1000 epoch). train ≈5.7, validation ≈12.2로 **2배 격차가 벌어진 채 평탄화** (validation이 상승하진 않음) | 우리는 GBR/RF라 epoch 곡선이 아니라 **n_estimators 대비 CV 곡선**이 대응물 |
| 5 | (=Fig. 2.5) 데이터셋 원소 출현빈도 **히스토그램** | 🔸 **안 봤다** (Fig. 6과 같은 정보의 다른 표현이라 생략) |
| 6 | (=Fig. 2.6) 원소 출현빈도 **주기율표 히트맵**. 컬러바 0–453. O가 최대(진한 초록), Al 그 다음, Ni 중간. **회색 = 데이터 0** (Nd·Pm·Sm·Bk·Cf·Es, 비활성기체, Fr/Ra, 초악티늄족) | ★ 우리 도펀트 101종의 **커버리지 지도**를 이 양식으로 그리면 "우리가 어디를 안 봤나"가 한 장에 나온다. §8.3-⑥ |
| S1 | (=Fig. 6.1) bulk modulus 분포를 ordinary/extraordinary로 가르고 **85/15/100% 분할 도식**. 초록 경계 figure-read ≈315 GPa | ★ **"상위 1% = extraordinary" 조작적 정의**의 원본 그림. 우리 cascade 랭킹의 "우수 후보" 정의를 이 형식으로 못박을 수 있다 |
| S2 | (=Fig. 6.2) 로그 열팽창 actual vs predicted에 **gap(빗금)·withheld element(노랑 Cs)·withheld structure(빨강 221-2)** 를 한꺼번에 표시 | ★ 외삽 거리를 **그림 하나로 정의**하는 방식. ⚠ 본문은 이 그림을 "붕소/전단탄성률"이라 잘못 지칭 (§6) |
| S3 | (=Fig. 6.3) (a) ridge 회귀 (b) logistic 분류, 같은 bulk modulus. 사분면 비율 인쇄: (a) FN 1·FP 4·TP 5·TN 90% (b) FN 0·FP 3·TP 6·TN 91% | ★ **회귀 vs 분류를 한 그림에서 비교**하는 양식. 우리 cascade 랭킹 그림을 이렇게 바꾸면 "몇 개 헛짚나"가 바로 보인다 |
| S4 | (=Fig. 6.4) **핵심 성능 그림.** Precision/Recall/F1 × 물성 6종 × 모델 4종, **시드 5개 표준편차 음영** | ★★ 우리 predictor 성능 보고의 **표준 양식**. 특히 (i) 회귀·분류를 같은 축에, (ii) **시드 산포를 음영으로**. 우리는 지금 시드 1개 |
| S5 | (=Fig. 6.5) 외삽 거리(gap 0/4/8/12%) × 3조건(all / element removed / structure removed) × 4모델의 **PR-AUC** | ★★ **"본 적 없는 원소로 넘어갈 때 −32%"** 의 출처. 우리 LOCO(leave-one-species-out) 결과를 이 그림 양식으로 보고하면 그대로 대응된다 |
| S6 | (=Fig. 6.6) AFLOW top1% vs PCD 스크리닝의 **원소 순위 비교** (막대 위 개수 인쇄) | ★ **학습 분포 ↔ 적용 분포의 어긋남**을 보이는 가장 간단한 그림. 우리 "학습된 winner 681행" vs "적용 대상 3,615행"의 도펀트 분포를 이렇게 나란히 그리면 §8.1-I가 한 장에 증명된다 |
| Table 1–4 | (2장) 노트북 목록 / ML 적용 사례 / 물성 저장소 16종 / 구조 저장소 7종 | 본문 §3.2에 **PDF 텍스트로 전사**했다 — 표 크롭(`tab_1`–`tab_3`)은 영역이 겹쳐 잘려 신뢰하지 않는다(`tab_4`는 추출 실패) |

**본 그림 / 안 본 그림**: 크로핑 15장(그림 12 + 표 3) 중 **그림 11장을 실제로 Read 해서 봤다**
(`1,2,3,4,6` + `S1–S6`). **안 본 것: `Fig. 5`(정보 중복), 표 3장**(표는 PDF 텍스트가 정확하므로 관례대로 생략).

---

## 6. 본문 주장과 그림이 어긋난 곳 (그림을 보고 나서야 잡힌 것)

1. **`Fig. S2` 지칭 오류** — §6.3 본문: "yellow data points representing **boron-containing structures when
   predicting shear modulus** in Figure 2". 실제 그림: 노랑 = **Cs**, 물성 = **log thermal expansion**.
   빨강(공간군 221-2)만 맞다. 옛 버전 그림을 가리킨 캡션 잔재로 보인다.
2. **결론의 "average recall ~0.6"** — `Fig. S4` 어디에서도 0.6 근처가 안 나온다(전 모델·전 물성 0.685–0.985).
   초록/§6.4.3의 0.75와도 안 맞는다. 셋 중 그림이 뒷받침하는 건 **0.75–0.87**이다.
3. **초록의 "precision typically above 0.5"** — 그림상 **분류에서만** 성립. 회귀(Ridge/SVR) 평균은 0.39–0.44.
4. **"structure removal은 영향 없다"** — 그림은 맞지만, 본문 스스로 "structure type 정의(공간군+원자수)가
   부적절해서일 것"이라 인정한다. 즉 **결과가 아니라 실험 실패**로 읽어야 한다.

---

## 7. Post-processing / 도구

| 항목 | 내용 |
|---|---|
| 계산 도구 | scikit-learn (모델·`StandardScaler`·`Normalizer`·grid search), 2장은 PyTorch/TensorFlow도 언급 |
| DFT | **직접 안 함.** AFLOW(ICSD 구조 기반) 계산값을 소비. 6장의 물성 6종 전부 AFLOW |
| 특징화 | CBFV — 원소 물성의 average/range/variance (6장). 2장은 Jarvis/Magpie/mat2vec/Oliynyk/one-hot 소개 |
| 지표 산출 | precision·recall·F1(회귀는 train F1으로 임계값 결정), **precision–recall AUC**(임계값 무관, 불균형 강건) |
| 불확실도 | **랜덤 시드 5개**로 train/test 분할 반복 → 표준편차를 그림 음영으로 |
| 공개 | 6장 코드 `github.com/kaaiian/can_machine_learning_find_extraordinary_materials`, 2장 `github.com/anthony-wang/BestPractices` (Jupyter 5종) |
| 기록 방식 | 데이터 정리·분할 절차를 코드로 공개, 하이퍼파라미터·시드 명시를 규범으로 제시(§2.9) |

---

## 8. ⭐ 우리 cascade ML 감사 (2026-08-19)

대상: `origin/claude/unified-2026-05-15` 의 `tools/doping/train_predictor.py`,
`predict_new.py`, `predict_best_site.py`, `chain_predict.py` + 데이터 `db/properties/cascade_v23_all.csv`.
⚠ **코드는 안 고쳤다. 진단·처방만.**

### 8.0 먼저 — 이번 감사에서 **새로 계산한 우리 데이터 사실**

| 사실 | 값 |
|---|---|
| 행 수 | **3,615** |
| 도펀트 라벨 | **101종** |
| 자리 | cation_site 3 (`Li_24g`,`Li_48h`,`P_4b`) × anion_site 3 (`Cl_4d`,`S_16e`,`S_4a`) × charge_comp 2 |
| **슬롯** (도펀트×양이온자리×음이온자리) | **229개** — 225개가 15행(농도라벨 3 × 시드 5), 4개가 60행 |
| ⚠ `concentration` 컬럼 | **전 행 `0.25` 상수** (파일명은 `x020/x050/x100`으로 갈리는데 컬럼은 안 갈린다) |
| ⚠ `n_fu_actual` 컬럼 | **전 행 `4` 상수** |
| 타깃 가용 행 | screen_de 3,615 / **eos_B0 622** / **E_young 681** / **Pugh 681** / **migration 681** / **`sigma_300K_S_cm_NE` = 0행** |
| ⚠ ΔE/atom 중복 | 같은 (도펀트,자리,시드)에서 농도라벨 3개의 값이 **1e-4 이내로 동일**한 블록이 1,080 중 **719 (66.6%)** → **정확한 중복행** |
| 슬롯내 σ ÷ 슬롯간 σ | ΔE **0.08** / B0 **0.71** / E_young **0.76** / 이동부피 **0.74** (kb 카드 §4-2의 0.49–0.88과 일치 ✅) |

**★ 누출이 R²를 얼마나 부풀리나 — 우리 데이터로 직접 계산한 상한**
(방법: "각 그룹의 평균을 완벽히 외우는 모델"의 R². 어떤 모델도 이 위로 못 간다.)

| 타깃 | ① 도펀트+자리 기억 = **랜덤 CV 상한** | ② 도펀트만 | ③ **자리만 = 새 도펀트(LOCO) 상한** | ①→③ |
|---|---|---|---|---|
| screen_de_per_atom | **+0.986** | +0.930 | **+0.220** | 0.99 → 0.22 |
| eos_B0_GPa | **+0.572** | +0.407 | **+0.172** | |
| elastic_E_young_GPa | **+0.502** | +0.309 | **+0.136** | |
| elastic_pugh_GoverB | **+0.345** | +0.175 | **+0.020** | 사실상 0 |
| migration_volume_fraction | **+0.576** | +0.421 | **+0.128** | |

③이 이렇게 낮은 이유는 구조적이다: 특징이 **도펀트 one-hot**이라, 학습에 없던 도펀트가 들어오면
`OneHotEncoder(handle_unknown='ignore')`가 그 블록을 **전부 0**으로 만든다 →
남는 정보는 자리(3×3)와 charge_comp(2)뿐 → 예측이 **자리별 평균**으로 붕괴한다.
즉 **우리 predictor는 "새 도펀트"에 대해 원리적으로 자리 평균밖에 못 낸다.**

### 8.1 걸리는 것 — 항목별 "논문이 뭐라 하나 / 우리가 뭘 하나 / 판정"

| # | 논문이 뭐라 하나 | 우리가 뭘 하나 | 판정 |
|---|---|---|---|
| **A. 누출·분할** | §2.5: "같거나 **비슷한** 데이터가 train과 test에 동시에 있으면 안 된다 … 일반화 성능을 **부풀린 추정**을 준다 = data leakage". 예시가 **"같은 화합물의 다른 측정 조건"** | `cv_schemes['random'] = KFold(shuffle=True)` 가 **캐노니컬**. 같은 도펀트의 15행(농도3×시드5)이 fold를 가로질러 섞인다. ΔE는 그중 **66.6%가 값까지 동일한 중복행** | ❌ **확정 누출.** 논문이 든 예("같은 화합물, 다른 조건")보다 **더 나쁘다** — 우리는 조건까지 같은 **완전 중복**이 3분의 2다. 랜덤 CV R² 0.99는 "외우기"의 상한(0.986)에 붙어 있을 뿐 |
| **B. 특징이 화학이 아니다** | §2.6: 소규모 데이터에서 **CBFV(Magpie/Oliynyk/mat2vec/Jarvis)** 를 쓰라. one-hot이 CBFV와 같아지는 건 "**충분히 큰 데이터 + 유능한 구조**"에서만. 6장은 CBFV(원소 물성 avg/range/var)를 써서 **외삽이 된다**고 보인 것 | `feats_categorical = [dopant, cation_site, anion_site, charge_compensation]` 전부 one-hot. 수치 특징 2개(`concentration`, `n_fu_actual`)는 **상수**. `with_structure` 모드의 Tier-2/BVSE는 **622–681행에만** 있다 | ❌ **가장 중대.** cold_start 모드는 **화학이 아니라 lookup key**다. Kauwe 6장의 "외삽 가능" 결론은 **CBFV 위에서만 성립** — 우리 특징으로는 그 결론을 인용할 자격이 없다 |
| **C. 모델 선택 지표** | §2.7 "Avoid p-Hacking": 튜닝은 validation으로. §2.8: 확정 후 **train+val 재학습 → test 1회** | `if random_r2 > best_r2` — **누출된 random KFold R²로 최적 모델을 고르고**, 최상위 `cv_r2_mean` 도 그 값. `group_dopant`/`loco` 는 **계산은 하는데 선택에 안 쓴다**(`cv_by_scheme`에 보관만) | ❌ 선택 편향. 6개 타깃 × 3–6개 모델을 **같은 누출 지표**로 골랐다 |
| **D. held-out test 없음** | §2.5: **한 번만** train/val/test로 나눠라. test는 최종 1회 | CV만 있고 **봉인된 test set이 없다.** 보고되는 건 전부 validation 성격 | ❌ 논문 기준 미달. 지금 숫자는 "test 성능"으로 부를 수 없다 |
| **E. 베이스라인 보고** | §2.8: **기성 툴(AutoML 등)을 내려받아 내 모델과 비교하라. 못 이기면 다른 길을 찾아라.** 6장 §6.4.3: **무작위 추측(6%)** 을 명시적 시나리오 1로 | `DummyRegressor(strategy='mean')` 가 `available_models`에 **있다** ✅. 그런데 `all_models` dict에 묻히고, **"더미 대비 lift"가 어디에도 출력되지 않는다.** AutoML 비교는 없음 | ⚠ **절반.** 계산은 하는데 **보고 형식이 없다** |
| **F. 회귀 vs 분류** | 6장 결론: **상위 1%를 찾는 일에선 분류가 회귀보다 낫다** — recall은 동률, **precision이 뚜렷이 높다**(`Fig. S4`: ≈0.56 vs ≈0.39–0.44), 위양성이 적다(`Fig. S3`: 4%→3%) | 6개 타깃 **전부 회귀**(`GradientBoostingRegressor` 등). 랭킹은 `combined_score`로 사후 정렬 | ❌ **작업 형식이 목적과 안 맞는다.** 우리 목적은 "상위 후보 골라내기" = 분류인데 회귀로 풀고 있다 |
| **G. 타깃 변환** | 6장: **T_D·κ·G·α 는 log10** 적용(정규분포 근사). §2.6: log 변환이 성능을 올릴 수 있다 | 변환 없음. `sigma_300K_S_cm_NE`(자릿수 스케일), `migration_volume_fraction`(0–1 유계) 모두 원값 | ⚠ 실제 손해. 특히 σ는 log10이 정석 |
| **H. 시드 반복** | 6장: **랜덤 시드 5개**로 분할을 반복, 표준편차를 그림 음영으로 (`Fig. S4`) | `random_state=42` **1개 고정** (고정 자체는 §2.7 준수 ✅). 산포 보고 없음 | ⚠ 우리 CLAUDE.md의 "단일시드 판정 금지"(MSD 규율)와도 어긋난다 |
| **I. 학습 분포 편향** | §6.4.4 한계 2: 재료 데이터는 **고성능 쪽으로 편향**돼 있다. `Fig. S6`: 학습(AFLOW top1%) vs 적용(PCD)의 원소 분포가 어긋나 **PCD의 0.1% 미만만 extraordinary로 예측** | B0/E_young/Pugh/migration 타깃이 **622–681행 = cascade winner**에만 있다. 그런데 predictor는 **3,615행 전체(그리고 그 밖의 새 조성)** 를 스코어링하는 데 쓴다 | ❌ **학습 분포 ≠ 적용 분포.** Kauwe가 PCD에서 실패한 것과 **같은 구조의 실패** |
| **J. 데이터 편향 시각화** | §2.5: t-SNE/UMAP/**원소 출현빈도 매핑**으로 군집·불균형을 눈으로 확인 (`Fig. 5`,`Fig. 6`) | 없음 | ⚠ 값싼 누락 |
| **K. 결과 그림** | §2.9: 예측 vs 실측(+marginal), **잔차 2종**, 손실곡선, 원소 빈도 — 이 넷이 MI 표준 | `cv_metrics.json`/`training_summary.json` 숫자만 | ⚠ 값싼 누락 |
| **L. 데이터 무결성** | §2.5 cleanup: "숫자가 비수치로 저장", "스키마 변경", "예상 못 한 값" 전부 점검하고 **문서화** | `concentration`이 전 행 0.25인데 **파일명은 x020/x050/x100** — 모델이 농도를 못 본다. `n_fu_actual`도 상수. `sigma_300K_S_cm_NE`는 **0행인데 TARGETS에 남아 있다** | ❌ 특징 2개가 무정보. 논문 §6.4.4의 "도핑을 배우려면 **농도가 촘촘히 라벨된 DB**가 필요하다"와 정면 충돌 — 우리 DB에서 그 라벨이 컬럼에 안 실려 있다 |
| **M. 재현성 코드 버그** | §2.9: 코드를 그대로 돌리면 같은 결과가 나와야 | `training_summary.json`의 `'features_numeric': feats_numeric` 은 **마지막 타깃 루프의 값**을 쓴다(타깃마다 optional 특징이 다른데 하나만 기록). 모든 타깃이 skip되면 `NameError` | ⚠ 실제 버그. 사후에 "이 모델이 무슨 특징을 썼나"를 요약에서 복원 못 한다 |
| **N. 과제 자체의 난이도** | §6.4.4 한계 4: **도핑은 "화학량론 화합물 DB로는 원리적으로 예측 불가"**, 촘촘한 농도 라벨 DB가 있어야 한다 | 우리는 그 DB를 만들고 있다 (= 옳은 방향) | ✅ **방향은 맞다.** 단 위 L 때문에 지금은 농도축이 모델에 안 들어간다 |

### 8.2 바로 고칠 수 있는 것 (코드 수정 수준 + 예상 영향)

| # | 수정 | 위치 | 예상 영향 |
|---|---|---|---|
| ① | **모델 선택·헤드라인 지표를 `group_dopant`로 교체** (`random_r2` → `cv_by_scheme['group_dopant']['cv_r2_mean']`). `random`은 "in-distribution 상한"으로 이름 붙여 병기 | `train_predictor.py` L248–263 | **보고 R²가 급락한다.** 상한 계산상 screen_de 0.99 → 0.22 수준, B0 0.57 → 0.17, Pugh 0.35 → 0.02. **아프지만 이게 진짜 숫자다.** 선택되는 모델도 바뀔 수 있다 |
| ② | **`is_ood`일 때 `loco` R²를 띄운다.** 지금은 "extrapolation이니 rough guess"라 경고하면서 **바로 옆에 in-distribution R²를 인쇄**한다. `predict_new.py`에는 `is_ood` 자체가 없다 | `chain_predict.py` L104–125, `predict_best_site.py` L88–99, `predict_new.py` L113–121 | 경고와 숫자가 모순되는 것을 없앤다. 비용 0 |
| ③ | **더미 대비 lift를 항상 출력** (`R²_model − R²_dummy`, MAE 비). 6장 시나리오 1 형식 | `train_predictor.py` 출력부 | 비용 0. "모델이 평균 예측보다 나은가"가 한 줄로 |
| ④ | **skew 타깃 log10** (`sigma_300K_S_cm_NE`는 필수, `migration_volume_fraction`은 logit 검토) | `TARGETS` 처리부 | 6장이 정확히 이 4개 물성에 쓴 처리 |
| ⑤ | **분류 헤드 추가** — 타깃별 상위 10%(또는 상위 1%)에 라벨을 붙이고 logistic/GBC로 풀어 **precision·recall·F1·PR-AUC** 보고 | 새 함수 | 6장의 핵심 이전. **랭킹이 목적이면 이쪽이 정답**이고, 우리 "슬롯내 σ ≈ 슬롯간 σ" 문제에도 강하다(값이 아니라 순위만 맞추면 되므로) |
| ⑥ | **시드 5개 반복 + ±σ 보고** (`random_state` 42/43/44/45/46) | CV 루프 | `Fig. S4` 양식. 우리 MSD 규율과도 일관 |
| ⑦ | **`concentration` 컬럼을 파일명 `x###`에서 채우거나, 특징에서 제거** | 데이터 생성부 | 지금은 무정보 특징. 채우면 §6.4.4가 요구하는 "농도 라벨"이 처음으로 모델에 들어간다 |
| ⑧ | **`features_numeric` 요약 버그** — 타깃별로 기록 | `train_predictor.py` L299 | 재현성 |
| ⑨ | **원소 출현빈도 주기율표 히트맵**(`Fig. 6` 양식) + **학습분포 vs 적용분포 원소 순위 비교**(`Fig. S6` 양식) | 새 그림 스크립트 (house_style) | 값싸고, §8.1-I·J를 한 장으로 증명. Origin-ready CSV 동시 출력 |

### 8.3 재계산·재설계가 붙는 것 (비용 명시)

| # | 처방 | 비용 |
|---|---|---|
| ㉠ | **CBFV 특징 도입** (Magpie/Oliynyk/mat2vec). 우리 도펀트는 원소가 아니라 **화합물(Ag₂O, Nd₂O₃…)** 이라 조성 가중 평균/range/variance로 벡터화해야 한다 | **DFT/MD 재계산 0.** 원소 물성 테이블 조회 + 재학습(수 분). **가장 값싼 근본 처방** — one-hot 붕괴(§8.0 ③)를 없앨 유일한 길 |
| ㉡ | **진짜 held-out 종 세트 봉인** — 도펀트 101종 중 예: 15종을 시작부터 잠그고, 모든 튜닝이 끝난 뒤 **1회만** 연다 | 재계산 0. 학습 데이터 ~15% 손실. §2.5/§2.8 준수를 위해 필요 |
| ㉢ | **슬롯 대표 정책 재정의** — 개별 배열이 아니라 **슬롯 평균 ± σ**를 타깃으로. kb §4-2가 이미 "슬롯내 산포는 잡음이 아니라 **실제 구조 다양성**"이라고 판정했으므로, 예측 대상은 **분포**여야 한다 | 재계산 0(라벨 재정의). 유효 표본이 3,615 → 229(또는 681 → ~227)로 줄어드는 게 대가 |
| ㉣ | **winner 편향 해소** — 비-winner에도 EOS/elastic/이동부피를 돌려 학습 분포를 적용 분포에 맞춘다 | ★ **진짜 계산비.** 622–681행 → 3,615행이면 **약 5.3–5.8배**. 전량은 과하고, **랭킹 하위·중위에서 층화표집**(예: 각 구간 100행)이 현실적 |
| ㉤ | **σ·Ea 타깃 부활** — `sigma_300K_S_cm_NE`가 **0행**이라 모델이 아예 안 만들어진다 | MD 재계산. CLAUDE.md의 "σ 절대값 인용 금지·멀티시드 판정만" 규율상, **소수 표본으로 σ 회귀 R²를 보고하는 것 자체가 위험** — 분류(빠름/느림)로 바꾸는 게 안전 |

### 8.4 감사에 **안** 걸린 것 (이미 논문 기준을 만족하는 것)

- `random_state=42` 고정 + pipeline 재현성 → §2.7 "Beware of Random Initialization" ✅
- **`GroupKFold(groups=dopant)`와 `LeaveOneGroupOut`을 이미 계산**한다 (DT-4). 도펀트로 묶으면 시드 5개·농도라벨 3개가 한 그룹에 들어가므로 **분할 설계 자체는 옳다** — 문제는 그걸 **선택·보고에 안 쓴다**는 것뿐 ✅→⚠
- `predict_best_site.py`·`chain_predict.py`의 **OOD(cold-start) 경고** ✅ (논문에는 이런 장치 요구조차 없다)
- `get_provenance()` — timestamp/python/platform/패키지 버전/UMA 모델명/git commit 기록 → §2.9 요구(환경 파일·버전 명시)를 **초과 달성** ✅
- `DummyRegressor` 구현 존재 ✅ (보고만 붙이면 된다)
- 데이터 CSV를 repo에 박제 → §2.10 "저장소는 체크포인트를 안 준다, 로컬에 아카이브하라" ✅

### 8.5 ★ 사용자 질문 넷에 대한 직답

**Q1. 2장이 우리 누출을 어떻게 다루나 / 어떤 분할을 써야 하나 / 부풀림 수치를 주나?**
- 다룬다. §2.5 Train–Validation–Test Split이 **"같거나 비슷한 데이터를 train과 test에 동시에 두지 마라 —
  같은 화합물의 다른 조건이 그 예다"** 로 우리 케이스를 정확히 지목한다.
- 써야 할 분할 = **종(도펀트) 단위 그룹 분할**. 우리 코드의 `GroupKFold(groups=dopant)`가 정확히 그것이고,
  더 엄격한 건 `LeaveOneGroupOut`(= leave-one-species-out). 둘 다 **이미 구현돼 있다** — 안 쓰고 있을 뿐.
  (scaffold split은 분자 화학의 관용어라 이 논문엔 안 나온다. 우리 대응물은 "도펀트 화합물 계열별 분할".)
- ⚠ **부풀림 수치는 논문이 주지 않는다.** 정성적 경고뿐. 그래서 **우리 데이터로 계산했다**:
  랜덤 CV 상한 **0.99 / 0.57 / 0.50 / 0.35 / 0.58** → 새 도펀트 상한 **0.22 / 0.17 / 0.14 / 0.02 / 0.13**.

**Q2. 6장이 외삽에서 뭘 보이나 / 우리 `predict_best_site`·`chain_predict`는 어디까지 정당한가?**
- 보이는 것: **값의 공백(gap)을 건너뛰는 외삽은 된다**(PR-AUC 거의 평평). **본 적 없는 원소로 가는 외삽은
  크게 깎인다**(0.79 → 0.54). **최근접이웃(=직관 자동화)은 gap 4%에서 반토막.** 실제 DB(PCD)에 적용하면
  **새 화학을 못 뚫고**, 학습 분포와 어긋난다.
- 우리 도구의 정당한 용도:
  - ✅ **학습에 있는 도펀트**의 **다른 자리 조합**을 고르는 것 (= `predict_best_site`의 원래 목적).
    이건 gap-외삽에 가깝고, 6장이 "된다"고 보인 영역이다.
  - ⚠ **학습에 없는 새 도펀트**의 값 예측 = **6장의 "element removed" 상황**이고, 게다가 우리는 CBFV가
    아니라 one-hot이라 **6장보다 더 나쁘다**(자리 평균으로 붕괴). → **순위 힌트로만**, 절대 수치 인용 금지.
  - ❌ **새 도펀트의 절대 물성값을 논문/발표에 싣는 것**은 지금 근거로 정당화 안 된다.
- 논문이 준 대안 프로토콜, 그대로 가져올 것 두 개:
  ① **분류로 바꾸고 precision/recall/F1 + PR-AUC로 보고** (임계값 무관·불균형 강건).
  ② **베이스라인 사다리(시나리오 1–4)**: 무작위 추측 → 직관 → 최근접이웃 → 모델. 우리 버전은
     "무작위" = 슬롯 무작위 선택, "최근접이웃" = 조성 유사 도펀트 값 복사, "모델" = predictor.
     **최근접이웃을 못 이기면 모델을 쓸 이유가 없다** — 이게 6장이 실제로 한 논증이다.

**Q3. 2장이 권하는 보고 항목 (그림·통계·베이스라인)**
- **그림 4종**: 예측 vs 실측(+marginal histogram, ideal선+선형fit) / 잔차 vs 실측 + 잔차 히스토그램(kde) /
  학습·검증 손실 곡선 / 원소 출현빈도(히스토그램 + 주기율표 히트맵).
- **통계**: 회귀 = r², MAE, (R)MSE / 분류 = accuracy, log loss, precision, recall, F1, ROC, AUC. + CV.
  6장이 추가로 쓰는 것: **PR-AUC**(임계값 무관), **시드 5개 표준편차**.
- **베이스라인**: §2.8은 **"기성 툴/AutoML을 내려받아 비교하고, 못 이기면 다른 길을 찾아라"**.
  "DummyRegressor와 비교하라"는 문구는 **2장에 없다** — 그 역할은 6장의 **시나리오 1(무작위 추측 6%)** 과
  **시나리오 3(최근접이웃)** 이 한다. 우리는 셋 다 붙이는 게 맞다(더미 = 평균, 최근접이웃, AutoML).
- **분할 보고**: 분할 방법·시드·fold 수를 적고, **모든 모델 비교에 같은 분할**을 쓴다.

**Q4. §2.9가 요구하는데 우리가 안 하는 것**
- ❌ **봉인된 test set이 없다** (CV만) — 가장 큰 미준수.
- ❌ **시험한 하이퍼파라미터 전량 기록**이 없다 (고정값만 하드코딩, grid search 없음).
- ❌ **그림 재현성** — 학습 산출물에 그림이 아예 없다(§2.9의 표준 4종 전부).
- ❌ **데이터 정리 단계 문서화** — `concentration` 상수화처럼 언제 어디서 정보가 사라졌는지 기록이 없다.
- ⚠ **README/재현 절차**: docstring의 usage는 있으나 "이 명령으로 논문 숫자가 재생성된다"는 경로가 없다.
- ✅ 이미 하는 것: 시드 고정, 버전관리(git), provenance(패키지 버전·commit), 데이터 CSV 동봉, 오픈 코드.

---

## 9. 우리 DFT/파이프라인 대비 (`our_dft_baseline.md`)

| 항목 | 이 논문 | 우리 | 차이 / 이유 |
|---|---|---|---|
| 물성 출처 | AFLOW DFT (ICSD 구조), 6물성 | 우리 QE/UMA 자체 계산 (comp1/modelc + cascade 3,615행) | 우리 쪽이 **자체 생성 데이터**라 큐레이션 통제권이 있다. 대신 **표본이 작고 winner 편향** |
| 기계 물성 | bulk/shear modulus를 **ML 타깃**으로만 사용 | EOS B0, elastic B/G/E/ν/Pugh를 **직접 계산** | 논문의 B·G 절대값은 우리와 비교 대상이 아니다 (AFLOW 소환값, 조성계 자체가 다름) |
| band gap | AFLOW DFT gap을 타깃으로 (functional 미명시) | fixed-occ nscf VBM/CBM: comp1 2.066 / modelc 2.099 / +B₂O₃ 1.9671 / LPSOCl 2.2309 eV | **비교 금지.** 논문은 gap을 "값"이 아니라 "ML 대상 분포"로만 쓴다. 우리 gap은 PBE 과소평가·무질서 민감이라 "wide-gap" 수준 비교만 |
| 무질서 처리 | 없음 (조성 하나 = 데이터 한 점) | 슬롯당 배열 5개(시드) — kb §4-2: **실제 구조 다양성** | ★ 논문의 "1조성 1값" 가정이 우리 데이터에 **성립하지 않는다.** 이게 §8.1-A 누출의 물리적 뿌리 |
| 불확실도 | 랜덤 시드 5개 → 그림 음영 | Ea 오차막대 = 600 K 3-시드 (MD). ML 쪽은 단일시드 | ML 쪽만 규율이 빠져 있다 |
| 외삽 주장 | CBFV 위에서 "된다" (단 원소 제거 시 −32%) | one-hot 위에서 "된다"고 암묵 가정 | ❌ **근거 이전 불가.** §8.1-B |

---

## 10. 적용 인사이트

- ① **랭킹이 목적이면 회귀가 아니라 분류다.** 6장이 같은 데이터에서 회귀 대비 위양성 4%→3%,
  precision 0.39–0.44 → 0.56을 보였다. 우리 cascade의 "상위 후보 고르기"는 정확히 이 작업이고,
  **슬롯내 σ ≈ 슬롯간 σ**(0.71–0.76)라는 우리 노이즈 구조에서 **값 회귀는 원리적으로 불리하다**(R² 상한 0.35–0.58).
  순위/등급만 맞히면 되는 분류로 바꾸면 그 상한 제약을 우회한다.
- ② **"새 도펀트 예측"은 지금 자리 평균이다.** one-hot + `handle_unknown='ignore'` 구조상 그렇고,
  LOCO 상한이 0.02–0.22다. 처방은 **CBFV 도입(계산비 0)** 하나뿐. 이걸 하기 전엔
  `predict_new`/`chain_predict`의 새 조성 수치를 대외 자료에 쓰면 안 된다.
- ③ **베이스라인 사다리를 그대로 이식하라.** 무작위 → 최근접이웃 → 모델. 6장의 설득력은
  "precision 0.56"이 아니라 **"무작위 6% 대비 9배, 그리고 최근접이웃보다 낫다"** 에서 나온다.
  우리 발표/원고도 같은 형식이어야 심사에서 안 깨진다.
- ④ **§6.4.4 도핑 문단은 우리 프로젝트의 정당화 문장이다.** "화학량론 DB로는 도핑 효과를 예측할 수 없고,
  **농도가 촘촘히 라벨된 DB**가 필요하다" → 우리 cascade가 그 DB다. 단, **지금 농도 컬럼이 상수**라는 걸
  고치지 않으면 이 인용이 자기모순이 된다.

---

## 11. 인용 가능 문장 (deck/paper용)

- "Wang·Kauwe·Sparks 등은 재료 ML의 표준 프로토콜에서, **같은 화합물의 다른 조건 데이터가 학습·시험 집합에
  동시에 존재하면 일반화 성능이 부풀려진다**고 명시한다 (*Chem. Mater.* **32**, 4954 (2020))."
- "Kauwe 등은 AFLOW의 DFT 물성 6종에서 **상위 1%를 '비범한(extraordinary)' 물질로 조작적으로 정의**하고,
  하위 99%만 학습해도 이들을 **recall 0.75 이상, precision ~0.5**로 식별할 수 있음을 보였다
  (*Comput. Mater. Sci.* **174**, 109498 (2020))."
- "같은 연구에서 **분류 기반 접근이 회귀 기반보다 동등한 recall을 유지하면서 위양성을 뚜렷이 줄였다** —
  스크리닝을 값 예측이 아니라 등급 판정으로 다뤄야 하는 근거다."
- "다만 저자들은 **학습 데이터에서 가장 흔한 원소를 제거하면 precision–recall AUC가 0.79에서 0.54로 떨어진다**고
  보고했고, **도핑처럼 수 % 치환이 물성을 수 자릿수 바꾸는 문제는 화학량론 화합물 데이터베이스로는 예측할 수 없으며
  농도가 촘촘히 라벨된 데이터베이스가 필요하다**고 명시했다."

---

## 12. 주의/한계 — 2021년 문서를 2026년에 쓸 때 ★

**(a) 논문 자체의 약점 (기준선 측정)**
1. **내부 수치 불일치 3건** (§6): 결론의 "average recall ~0.6" ↔ 초록 3/4 ↔ `Fig. S4` ≈0.82–0.87.
   초록의 "precision typically above 0.5"는 분류에만 참. `Fig. S2` 지칭 오류.
2. **성능 표가 없다.** 6장은 precision/recall/F1을 **그림으로만** 준다 — 숫자 표가 없어
   재인용하려면 눈으로 읽어야 한다(이 카드의 `figure-read ≈` 가 그래서 붙었다).
3. **structure type = 공간군 + 원자수**는 조악하다. 저자도 인정한다. "구조 외삽은 쉽다"는 결론을
   여기서 끌어내면 안 된다.
4. **단 하나의 데이터 원천(AFLOW)** 에서만 검증. 실험 데이터·다른 저장소로의 일반화는 안 보였다.
5. **"best case scenario"** 를 저자 스스로 강조한다 — 잘 분포된 DFT 데이터. 우리 데이터는 그 조건이 아니다
   (표본 622–681, winner 편향, 슬롯내 산포 큼).
6. 2장은 **규범 문서라 근거 수치가 거의 없다.** 권고의 상당수가 "consider…", "ideally…" 수준이다.

**(b) 2021 → 2026, 그동안 바뀐 것 (이 조언을 그대로 쓸지 판단하는 근거)**
- **범용 MLIP / 파운데이션 모델의 등장**. 2장 §2.3의 "당신 특징이 DFT나 결정구조면, 남들은 그냥 DFT를
  돌리는 게 낫지 않나"라는 논변은 **UMA/MACE 같은 범용 퍼텐셜이 DFT를 10³–10⁶배 싸게 대체하면서 반쯤 무너졌다.**
  우리 cascade가 UMA로 3,615행을 만든 것 자체가 2021년엔 불가능했던 일이다.
  → **"ML 대리모델 vs 직접 계산"의 손익분기가 이동했다.** 다만 우리 CLAUDE.md의 "UMA는 Li₃N에 사용 금지"처럼
  **범용 MLIP도 계 의존적 편향**이 있어, 2장의 "데이터 검증" 요구는 오히려 더 중요해졌다.
- **표형 파운데이션 모델**(TabPFN, 2025 — litdb `hollmann2025_tabpfn_tabular_foundation_model`)이
  "소데이터에선 GBDT" 라는 §2.6의 전제를 흔든다. 우리 622–681행 규모는 TabPFN의 주 타깃 구간이다.
  → §8.2-⑤(분류 헤드)를 붙일 때 GBR과 TabPFN을 같이 재는 게 2026년식이다.
- **CrabNet(7장, 미독)** 이 이미 논문 안에서 "충분한 데이터 + attention이면 CBFV가 무의미"를 주장한다.
  하지만 그 "충분"은 수만 행이다 — **우리 규모에선 여전히 CBFV 쪽 조언이 유효**하다(§8.3-㉠).
- **분할·누출 규율은 안 바뀌었다.** 오히려 재료 ML에서 leakage 재현성 논쟁이 커진 5년이었다.
  §2.5·§2.7·§2.8은 **지금도 그대로 적용**해야 한다.

**(c) 이 카드 자체의 한계**
- **2장·6장만 읽었다.** 특히 **5장(Is Domain Knowledge Necessary?)** 은 §8.1-B(one-hot vs CBFV)의
  1차 근거라 **다음 차수에서 반드시 읽어야 한다.** 4장(DFT gap → 실험 gap 앙상블)은 우리 gap 규율과
  직접 닿고, 7장(CrabNet)은 (b)의 판단 근거다.
- 6장 성능 수치는 **그림 판독값**이다. 원 논문 GitHub의 결과 파일을 받으면 정확한 값으로 대체할 수 있다.

---

## 13. 미독 장 — 다음 차수 예정 (2차)

| 장 | 왜 읽어야 하나 | 우선순위 |
|---|---|---|
| **5** Is Domain Knowledge Necessary for Learning Materials Properties? (문서 38–45, PDF 50–57) | **one-hot vs CBFV**를 정면으로 비교. §8.1-B와 §8.3-㉠의 판정 근거가 여기 있다 | ★★★ 최우선 |
| **7** CrabNet (문서 54–82, PDF 66–94) | 28개 물성 벤치마크 표(`Table 7.1`,`7.2`)와 "특징공학이 언제 무의미해지나"의 규모 기준. 12장 (b) 판단 | ★★ |
| **4** Extracting Knowledge from DFT: 실험 band gap 앙상블 (문서 29–37, PDF 41–49) | **DFT gap → 실험 gap** 보정. 우리 PBE 과소평가 규율과 직접 연결 | ★★ |
| **3** Heat capacity ML (문서 19–28, PDF 31–40) | 2장 노트북의 예제 데이터셋 원본. 특징 생성 절차(`Fig. 3.1`, `Table 3.2`)가 CBFV 구현 참고 | ★ |
| **1**, **8** Introduction / Conclusion | 전체 논지 봉합 | ★ |

---

## INDEX·비교표에 넣을 항목 (수동 병합 대기)

⚠ 다른 litdb 에이전트와 충돌 방지를 위해 `INDEX.md`·`comparison_vs_ours*.md` 는 **건드리지 않았다**
(근거: `kb/methodology/litdb_shared_branch_convention_2026_08_19.md`). 아래를 사람이 병합할 것.

**`litdb/INDEX.md` 행 (track: dft)**
```
| kauwe2021_ml_materials_properties_dissertation_sparks | Machine Learning of Materials Properties (박사학위논문, Utah 2021) — Kauwe/Sparks | dft | 🟡 부분 (2장 best-practices + 6장 extraordinary materials만; 3·4·5·7장 미독) | ML 방법론·데이터 누출·외삽 한계 / cascade predictor 감사 |
```

**`litdb/comparison_vs_ours.md` — 새 축 제안 (E: ML/데이터 방법론)**
기존 A(이온전도)/B(산화 4축)/C(기계)/D(전자구조) 중 어디에도 안 맞는다. **축 E "ML·데이터 방법론"** 신설 제안:

| 항목 | 문헌 (Kauwe 2021 §2·§6) | 우리 (cascade predictor) | 판정 |
|---|---|---|---|
| 분할 | 종 단위 그룹 분할 필수, 같은/비슷한 데이터의 train-test 동거 금지 | 랜덤 5-fold가 캐노니컬 (GroupKFold/LOCO는 계산만) | ❌ 누출. 랜덤 CV 상한 0.99 → 새-도펀트 상한 0.22 |
| 특징 | CBFV (원소 물성 avg/range/var) | 도펀트 one-hot + 상수 2개 | ❌ 외삽 근거 이전 불가 |
| 작업 형식 | 상위 1% 찾기는 **분류**가 회귀보다 우월 (precision 0.56 vs 0.39–0.44) | 6타깃 전부 회귀 | ❌ 목적-형식 불일치 |
| 베이스라인 | 무작위(6%) → 최근접이웃 → 모델 사다리 | DummyRegressor 구현은 있으나 미보고 | ⚠ 절반 |
| 불확실도 | 시드 5개 ±σ 음영 | 단일 시드 (`random_state=42`) | ⚠ 우리 MSD 규율과도 불일치 |
| 학습↔적용 분포 | PCD 적용 시 0.1% 미만만 검출 = 분포 어긋남을 명시적으로 보고 | winner 622–681행 학습 → 3,615행+신규에 적용 | ❌ 같은 구조의 실패 위험 |
| 재현성 | 소스·데이터·가중치·하이퍼파라미터·시드·환경파일 전량 | provenance/시드/CSV ✅, held-out test·HP 기록·그림 ❌ | ⚠ 부분 |

**`litdb/properties/` 해당 없음** (이 논문은 물성 값이 아니라 방법론).
