# Foundation-Model Surrogates Enable Data-Efficient Active Learning for Materials Discovery — Hu, Dong, Feng, Hu & Hu (arXiv preprint, 2026)

> slug `hu2026_foundation_model_surrogates_active_learning` · arXiv `2603.12567v3` [cond-mat.mtrl-sci], **24 Mar 2026** · DOI `없음` (본문 각주에 `DOI:000000/11111` 이라는 **자리표시자**가 그대로 남아 있다) · type `ML 방법론 (능동학습 대리모형 벤치마크)` · PDF `a6a95804-97._Foundationmodel_surrogates_enable_dataefficient_active_learning_for_materials_discovery.pdf` · 19 pp · digested `2026-09-09` · status ✅
> elements: Cu, Fe
> methods: (none — 원자단위 계산 0건 · 실험 0건 · 순수 tabular ML)

> 🔴🔴 **동료심사 안 됐다 — arXiv preprint 다.** PDF 메타데이터 `creator = arXiv GenPDF (tex2pdf:a6404ea)` ·
> `producer = pikepdf 8.15.1`. 저널 흔적 없음. 게다가 **초고 단계 흔적이 여러 곳에 남아 있다**:
> ① 각주 인용 스텁 `"J.Hu et al. … 15 Pages…. DOI:000000/11111"` (실제 19 pp)
> ② `Table 3` 캡션이 **"Summary of 25 Benchmark Datasets"** 인데 표에는 **10행**뿐
> ③ §2.3 이 **ChEMBL/ADMET 분자 10종 데이터셋을 상세히 소개하는데 결과에 한 번도 안 나온다**
> ④ 초록의 *"electrolyte materials"* 에 해당하는 데이터셋이 **논문에 없다** (§0-B)
> ⑤ `Fig. 1` 축 라벨·패널 제목이 깨져 있다 (§0-C)
> ⑥ 본문의 *"8 out of 10 datasets"* 가 **자기 `Table 4` 와 안 맞는다 — 세면 7/10 이다** (§12-1)
> ⇒ **인용할 때 반드시 "preprint" 로 표기**하고, 아래 숫자는 게재본에서 바뀔 수 있다는 전제로 쓴다.

> 🔗 **왜 이 편인가 (2026-09-09 인입 맥락).** 우리는 **LPSCl 도펀트 스크리닝 cascade 를 재설계 중**이고
> (보고량 카드 `db/properties/cascade_d_rel_estimand_2026_09_08.json` = `active`), 같은 주에
> AL 축 두 편([Cho25AL] 실험 PSO · [Ma25AL] GP-EI)과 MLIP 파운데이션 축 세 편(Tompa · Alghamdi · Kurniawan)이
> 들어왔다. 제목이 *"foundation-model surrogate 가 데이터 효율적 AL 을 가능하게 한다"* 이고
> **우리는 이미 파운데이션 MLIP(UMA-s-1p1/omat)을 표준으로 쓰고 있으니**, 겉보기엔 우리 상황 그 자체다.
>
> 🔴🔴 **그런데 아니다. 이 논문의 "foundation model" 은 UMA·MACE 같은 MLIP 이 아니라 `TabPFN` 이다** —
> **표(table) 데이터용 in-context Bayesian 트랜스포머**다. 원자도, 구조도, 힘도, DFT 도 이 논문에는 없다.
> **층위가 다르다**: UMA 는 *오라클(라벨 생산자)* 자리에 있고, TabPFN 은 *설계표 위의 대리모형* 자리에 있다.
> 둘은 **경쟁 관계가 아니라 위아래로 겹치는 관계**다. 이 구분을 놓치면 이 논문 전체를 잘못 읽는다 (§0-A).

---

## 0. ⚠ 제목이 부르는 것과 내용이 다르다 — 먼저 읽을 것

### 0-A. "foundation model" 이 가리키는 것 (★2 의 절반)

| | 이 논문 | 우리 UMA |
|---|---|---|
| 모델 | **TabPFN** (Prior-Data Fitted Network, 트랜스포머) [44] = Hollmann et al., arXiv 2501.02945 | **UMA-s-1p1 (omat)**, fairchem |
| 입력 | **표 한 줄** = (조성 벡터 or Magpie 서술자) → 스칼라 물성 | **원자 좌표 + 격자** → 에너지·힘·응력 |
| 사전학습 | **수백만 개의 합성(synthetic) 표 회귀 과제** | OMat24 등 **실제 DFT 궤적** |
| 출력 | 물성의 **사후예측분포(PPD)** — 분위수 전체 | 에너지·힘 **점추정** |
| 역할 | AL 루프의 **대리모형(surrogate)** | 우리 cascade 의 **오라클(라벨 생산자)** |
| 이 논문에서 | 주인공 | **한 번도 안 나온다** (`MLIP`·`interatomic`·`force field` 0회) |

> 📎 **TabPFN 자체의 사양·한계는 이 논문에 없다.** 원전 digest 를 같이 본다 →
> `papers/hollmann2025_tabpfn_tabular_foundation_model.md` (Hollmann et al., *Nature* **637**, 319–326, 2025).
> **우리 랩(BML)에 이미 사용 경험도 있다** — §11-b.

⇒ **"우리가 UMA 로 이걸 그대로 할 수 있나"의 답은 "그 질문이 성립하지 않는다"** 이다.
UMA 를 이 논문의 TabPFN 자리에 넣을 수 없다 — UMA 는 조성 벡터를 받지 않는다.
**대신 성립하는 질문은 "UMA-MD 를 오라클로 두고 그 위에 TabPFN 을 대리모형으로 얹을 수 있나"** 이고,
그건 **가능하다**. 구체안은 §13.

### 0-B. 🔴 초록이 없는 데이터셋을 판다

초록: *"We evaluate ICAL across ten benchmark datasets spanning copper alloys, bulk metallic glasses,
crystal lattice thermal conductivity, **and electrolyte materials**."*

**`Table 3` 의 10개 데이터셋에 전해질은 없다.** LTC(3,148 결정) · Cu 합금 경도(1,614) · Cu 합금 전기전도도(1,826) ·
Fe계 벌크금속유리(495) 뿐이다. 서론 자체도 *"copper alloys, bulk metallic glasses, and crystal lattice thermal
conductivity"* **세 종류**만 열거한다. 전문 검색: `electrolyte` 3회 = 초록 1 + 참고문헌 [25] 관련 1 + 논의 1,
`lithium` 1회 = **참고문헌 [25] 제목**, `solid electrolyte` 0회, `battery` = 참고문헌뿐.

⛔ **따라서 이 논문을 "전해질 AL 논문" 으로 인용하면 안 된다.** 우리 계와의 화학적 접점은 **0** 이다.

### 0-C. `Fig. 1` 은 개념도인데 그림 자체가 깨져 있다 (**실제로 보고 적는다**)

`fig_1.png` 를 열어 확인한 것:
- 패널 **(b) 와 (c) 의 제목이 똑같다** — 둘 다 *"Tabular Foundation Models (Meta-Learned Priors)"*.
  그런데 캡션은 (c) 를 *"Active learning with foundation-model surrogates…"* 라고 부른다 ⇒ **캡션과 패널이 어긋난다.**
- (c) 의 y축 라벨이 **`"Uncerainty Capcion Quantification Capability"`** — 오타 2개가 든 채로 인쇄됐고,
  눈금이 위에서부터 `1 / 0 / 0` 으로 **말이 안 된다**.
- 오타가 더 있다: `Gausian Processes` · `Calibarted` · `Optimal Matarial Performance` · `DNN. RF`(쉼표 오타).
- (a)/(b)/(d) 는 **데이터가 아니라 손으로 그린 모식 곡선**이다 — 축에 숫자가 없다.

⇒ **`Fig. 1` 에서 인용할 수 있는 것은 "GP=원리적이나 표현력 부족 / RF·NN=표현력 있으나 캘리브레이션 나쁨 /
FM=둘 다" 라는 저자의 주장 구조뿐**이고, **수치는 하나도 없다**.

---

## 1. 한 줄 요약

소규모 실험 데이터(수십~수백 점)에서 능동학습의 병목은 **대리모형의 불확실도 품질**인데,
**GP 는 표현력이 부족하고 RF/NN 은 불확실도가 휴리스틱**이라는 오래된 딜레마를,
**합성 표 회귀 과제 수백만 개로 메타학습된 tabular 파운데이션 모델 `TabPFN` 을 대리모형으로 바꿔 끼워서**
푼다고 주장한다 — 10개 벤치마크(Cu 합금 · Fe계 금속유리 · 결정 격자열전도도)에서
**전역 최적점을 찾기까지 필요한 추가 평가 수를 GP 대비 평균 52%, RF 대비 29.77% 줄였다**는 것이 헤드라인이고,
그 원인은 회귀 정확도가 아니라 **NLL·AUSE 로 잰 불확실도 캘리브레이션**이라는 것이 기전 주장이다.

⚠ 그 헤드라인 두 숫자는 **10개가 아니라 "TabPFN 이 이긴 데이터셋 4개"의 평균**이다 (§12-2 에서 재계산해 확인).

## 2. 메타

| 항목 | 값 |
|---|---|
| 저자 | **Jeffrey Hu**¹, **Rongzhi Dong**², **Ying Feng**³, **Ming Hu**⁴, **Jianjun Hu**²\* |
| 소속 | ¹UIUC 재료공학 · ²Univ. of South Carolina 컴퓨터공학 · ³항저우전자대 Zuoyue Honors College · ⁴USC 기계공학 |
| 교신 | Jianjun Hu (`jianjunh@cse.sc.edu`) — **AI-for-materials 그룹**(TabPFN 물성예측 선행편 [45] 의 같은 그룹) |
| 발표 | **arXiv 2603.12567v3**, cond-mat.mtrl-sci, **2026-03-24**. **동료심사 전** |
| 분량 | 본문 16 pp + 참고문헌 3 pp = **19 pp**. **SI 없음** |
| 그림·표 | **Fig. 1–5** · **Table 1–6** (전부 본문) |
| 조성/계 | **Cu 기 합금**(경도·전기전도도) · **Fe 기 벌크금속유리**(임계주조직경 D_max) · **결정 LTC 3,148종** |
| 연구유형 | **ML 방법론 벤치마크** — DFT 0회 · MD 0회 · 실험 0회. 라벨은 전부 **공개 데이터셋 재사용** |
| 데이터 | Cu = [54] Gorsse et al., *Sci. Data* **10**, 504 (2023) · 유리 = [55]=[58] Bobadilla et al., *Metals* **15**, 763 (2025) · **LTC = "합리적 요청 시 교신저자에게"(비공개)** |
| 코드 | *"will be released openly at the project's GitHub repository **upon publication**"* ⇒ **지금은 없다.** URL·라이선스 **미기재** (`license` 전문 0회) |
| 기여 | 개념·방법·소프트웨어 = JF.H(제1저자) · 감독·자금 = J.H. ⚠ 기여 절에 **본문 저자 목록에 없는 `C.W.`** 가 등장 (초고 잔재 추정) |
| 이해상충 | **선언 없음** |

> ✅ **서지 확인**: 화면 서지(`J. Hu, R. Dong, Y. Feng, M. Hu, J. Hu — arXiv:2603.12567, 2026`)는
> **표지·PDF 메타데이터와 일치한다.** 보탤 것 둘 — ⓐ 제1저자 Jeffrey Hu 와 교신 Jianjun Hu 는 **다른 사람**이고
> 둘 다 성이 Hu 다(공저자 Ming Hu 까지 **Hu 가 셋**), ⓑ **v3** 이다(v1·v2 는 확인 못 했다).
> 인용은 `J. Hu, R. Dong, Y. Feng, M. Hu, J. Hu, arXiv:2603.12567v3 (2026)`.

## 3. 핵심 수치

> ⛔ **우리 물성 4축(A 이온전도 / B 산화안정 / C 기계 / D 전자구조)에 넣을 값이 하나도 없다.**
> σ · Ea · ESW · 탄성상수 · band gap 을 **한 번도 계산하지 않는다.** 원자단위 계산 자체가 없다.
> ⇒ `comparison_vs_ours.md` 는 **§J-9c(AL 축)** 과 **`🔧 방법 원전`** 에만 넣는다.
>
> ⚠ 이 논문에 나오는 "electrical conductivity" 는 **Cu 합금의 전자전도도(%IACS)** 다 —
> 우리 이온전도도(mS/cm)와 **이름만 같고 완전히 다른 양**이다. 절대 섞지 않는다.

**이 논문의 "물성" 은 AL 효율 지표다.** 우리에게 의미 있는 것만:

| 지표 | 값 | 조건 | 출처 |
|---|---|---|---|
| **추가 평가 절감 (vs GP)** | **평균 52%** (개별 최대 **71.9%**, cu_hardness) | ⚠ **TabPFN 이 이긴 4개 데이터셋 평균** | `Table 4` |
| **추가 평가 절감 (vs RF)** | **평균 29.77%** (개별 최대 **53.2%**) | ⚠ 동 | `Table 4` |
| **무작위 대비** | **⛔ 없다 — 랜덤 팔이 논문에 없다** | — | 전문 검색 |
| 승률 (init 격자 기준) | cu_hardness **90%** (GP·RF 둘 다) · glass_ds3 **95%**(GP)/**80%**(RF) · ltc_conc **75%**(GP)/**95%**(RF) · cu_electric **75%**(둘 다) | 20개 init_ratio 점 중 이긴 비율 | `Fig. 3–5` 인셋 |
| **최소 데이터 문턱** | **후보 풀의 10–20% 를 초기 라벨로 확보해야** TabPFN 우위가 발현 | 그 아래에선 GP 가 나을 수 있다 | §3.1·§4 |
| **NLL** (Cu 전도도) | **TabPFN 2.34** vs RF 3.11 vs GP 3.46 | 5-fold CV | `Table 5` |
| **AUSE** (Cu 전도도) | **TabPFN 0.83** vs RF 1.77 vs GP **5.58** | 동 (⚠ 본문은 GP 를 `15.58` 이라 쓴다 — 표와 불일치, §12-3) | `Table 5` |
| **MPIW** (Cu 전도도) | TabPFN **11.16** vs RF 15.93 vs GP **32.50** (%IACS) | PICP 0.88 / 0.87 / 0.93 | `Table 5` |
| **NLL** (LTC 농도특징) | **TabPFN 3.22** vs GP 5.81 vs RF 7.53 | 5-fold CV | `Table 6` |
| **AUSE** (LTC) | **TabPFN 2.16** vs RF 4.50 vs GP 10.80 | 동 | `Table 6` |
| **PICP / MPIW** (LTC) | TabPFN **0.94 / 33.16** · GP **0.99 / 237.23**(무의미하게 넓음) · RF **0.86 / 24.37**(과소피복) | 목표 0.95 | `Table 6` |
| 회귀 정확도 (LTC) | **셋 다 나쁘다** — TabPFN·RF R² **0.18**, GP R² **−0.01** | 5-fold CV | `Table 6` |

★ **`Table 6` 이 이 논문에서 우리에게 제일 중요한 표다**: `R² = 0.18` 짜리 예측기로도 AL 이 굴러갔다.
이건 [Ma25AL] 재계산(out-of-sample 설명분산 ≤ 0 인데 루프가 돌았다)과 **같은 방향의 증거**다 (§13-4).

## 4. 방법 ★

> ⚠ 이 절의 "계산 방법" 은 DFT 설정이 아니라 **AL 루프 사양**이다. DFT·MD 설정은 존재하지 않는다.
> 우리 §4 표준 항목(functional / pseudo / k-points / ecut / supercell / DFT+U / AIMD / 무질서 처리)은
> **전부 해당 없음**이다.

### 4.1 pool-based AL 루프 — `Fig. 2` (그림을 실제로 보고 적었다)

`Fig. 2` 는 A→K 블록 흐름도다. 그림에서 직접 읽은 것:

| 블록 | 내용 | 우리 해석 |
|---|---|---|
| **A** | 재료 DB 적재 | — |
| **B** | 정제·인코딩 (범주형 → 수치) | 결측·비수치는 **0 으로 대치** (§2.3) |
| **C** | ⚠ **"Pick bottom *K*% of samples"** = 물성 **최저** K% 를 초기 라벨셋으로 | **무작위가 아니다** — §4.4 참조 |
| **D** | 대리모형 학습 | TabPFN 은 학습 없음(단일 forward) |
| **E** | 미라벨 풀 전체 예측 → **μ, σ** | |
| **F** | 획득함수 (EI; 캡션 *"F: EI can be replaced with any other acquisition functions"*) | |
| **G** | Top-k 선택. 캡션 ***"G: k=1 is used for maximum sample efficiency"*** | 🔴 **batch = 1** (★3) |
| **H** | *"Is Global Max Found?"* → Yes 면 종료 | **목표 = Top-1 탐색**. 캡션 *"H: Top-1 task can be replaced with discovering Any of / All of Top-K tasks"* ⇒ **말만 하고 안 했다** |
| **I** | 선택된 후보를 학습셋으로 이동 → D 로 | |
| **K** | 종료. 출력 = **Extra Evaluations** | **유일한 성능 지표** |

⚠ `Fig. 2` 그림 자체의 결함: 마름모 **H 에서 나가는 화살표가 "Yes" 1개 · "No" 2개**다(하나는 I 로, 하나는 F 로).
흐름도로서 애매하다 — 본문 서술로 보면 No 는 I 로 가는 쪽이 맞다.

### 4.2 ★2 "foundation-model surrogate" 가 정확히 무엇인가 — `Table 2`

**답: ③ 예측을 그대로 대리값으로 쓴다. 동결도 fine-tune 도 임베딩 추출도 아니다.**

| 물음 | 답 | 근거 |
|---|---|---|
| 파운데이션 모델을 **동결**하고 임베딩만 특징으로 쓰나? | ⛔ **아니다.** 임베딩을 꺼내 쓰지 않는다 | §2.2 |
| **fine-tune** 하나? | ⛔ **아니다.** *"performs inference in a single forward pass **without any gradient-based optimization on the target dataset**"* | §1·§2.2 |
| **예측을 그대로** 대리값으로? | ⭕ **그렇다.** 라벨된 데이터를 **컨텍스트(support set)** 로 프롬프트에 넣고, 미라벨 후보를 query 로 붙여 **한 번의 forward pass** 로 사후예측분포를 얻는다 | §2.2 |
| **σ 를 어디서 뽑나** | 🔴 **앙상블 아니다. GP 헤드 아니다. MC dropout 아니다.** **모델이 직접 뱉는 분위수**에서 뽑는다: `σ(x) = (q₉₇.₅ − q₂.₅) / 3.92` (정규분포 가정, 2×1.96=3.92) | **`Table 2`** |
| μ 는 | **예측분포의 중앙값(50번째 분위수)** | `Table 2` |
| 모델 버전·크기 | ⛔ **미기재.** 참고문헌 [44] 이 *TabPFN v2* 논문이지만 본문에 버전·파라미터 수·컨텍스트 길이 상한 서술 **없음** | — |
| 재학습 | **0회.** 매 AL 사이클마다 컨텍스트가 한 줄씩 길어질 뿐 | §2.2 |

⇒ ★6 의 *"σ 를 앙상블로 뽑는다면 M 을 몇으로 썼나"* 에 대한 답: **앙상블을 안 쓴다. M 개념 자체가 없다.**
Grasselli 식 (27) 의 `M ≥ 4` 제약이 **이 층위에서는 발생하지 않는다** — 우회가 아니라 **다른 종류의 σ** 다 (§13-3).

**비교 대상 두 개의 σ 정의도 `Table 2` 에 같이 있다** (우리가 자주 헷갈리는 자리라 적어 둔다):

| 대리모형 | μ(x) | σ(x) |
|---|---|---|
| **TabPFN** | 예측분포 **중앙값** | **(97.5%ile − 2.5%ile)/3.92** |
| **RF** | T개 트리 예측의 평균 | 트리 간 **표준편차** = "committee disagreement" (저자 표현: *heuristic*) |
| **GP** | 해석적 사후평균 | 해석적 사후표준편차 — **커널 공간 거리**가 지배 |

### 4.3 ★1 획득함수 6종 — `Table 1` + 실제 승자

**정의 (표 그대로).** β = **30**, ξ = **0.2** 로 전 데이터셋·전 실험 고정.

| # | 이름 | 수식 | μ 출처 | **σ 출처** | 비고 |
|---|---|---|---|---|---|
| 1 | **Standard UCB** | `μ(x) + βσ(x)` | 자기 모델 | **자기 모델** | 원단위 → 스케일 문제 |
| 2 | **Normalized UCB** | `μ_norm(x) + βσ_norm(x)` | 자기 모델 | **자기 모델** | μ·σ 를 각각 **[0,1] min-max** |
| 3 | **Hybrid UCB** | `μ_norm(x) + βσ_GP_norm(x)` | **TabPFN** | 🔴 **별도로 돌린 GP** | 두 모델을 동시에 유지 |
| 4 | **Standard EI** | `(μ−f_best)Φ(Z) + σφ(Z)` | 자기 모델 | 자기 모델 | ξ 없음 |
| 5 | **Normalized EI** | `(μ̂−f̂_best−ξ)Φ(Z) + σ̂φ(Z)`, `Z=(μ̂−f̂_best−ξ)/σ̂` | 자기 모델 | 자기 모델 | min-max 정규화 + ξ |
| 6 | **Hybrid EI** | Normalized EI 와 같은 식 | **TabPFN** | 🔴 **GP** | |

**순위 — `Table 4` 의 "Best Acq (TabPFN)" 열 + `Fig. 3–5` 범례에서 읽은 실제 승자:**

| 데이터셋 | TabPFN 최선 | GP 최선 | RF 최선 |
|---|---|---|---|
| cu_electric | **ei** | ei | ei |
| cu_electric_magpie | ucb_norm | (미기재) | (미기재) |
| cu_hardness | **ucb** | ucb_norm | ei_norm |
| cu_hardness_magpie | **ei_hybrid** | (미기재) | (미기재) |
| glass_ds1_conc | ucb_norm | (미기재) | (미기재) |
| glass_ds2_physical | ucb_norm | (미기재) | (미기재) |
| glass_ds3_magpie | **ucb** | ei | ucb_norm |
| ltc_conc | **ucb_hybrid** | ucb | ucb |
| ltc_magpie | ucb | (미기재) | (미기재) |
| ltc_structure | ei | (미기재) | (미기재) |

🔴🔴 **★1 의 핵심 답: 일관되게 이기는 획득함수는 없다. 계마다 완전히 뒤집힌다.**
10개 데이터셋에서 TabPFN 의 최선이 **`ucb` 3회 · `ucb_norm` 3회 · `ei` 2회 · `ucb_hybrid` 1회 · `ei_hybrid` 1회**
— **6종이 사실상 고르게 나눠 가진다.** 같은 Cu 합금이라도 특징만 바꾸면(`cu_hardness` → `cu_hardness_magpie`)
`ucb` → `ei_hybrid` 로 갈아탄다. **GP·RF 도 마찬가지로 데이터셋마다 다른 것을 고른다**(cu_hardness 에서
GP=ucb_norm, RF=ei_norm, TabPFN=ucb — **셋이 전부 다르다**).

⇒ **우리에게 더 중요한 것은 이쪽이다**: 획득함수는 **하이퍼파라미터**이지 방법론적 선택이 아니다.
"어느 획득함수를 쓸까"를 문헌에서 이식할 수 없다. **우리 계에서 직접 스윕해야 한다.**
그리고 그 스윕을 **보고할 지표 위에서 하면 안 된다** — 이 논문이 바로 그렇게 했다 (§12-4).

⚠ **무작위 대비 배수는 논문에 없다.** 표의 "성능" 칸을 채울 수가 없다 — **랜덤 팔이 아예 없다** (§12-5).

### 4.4 ★3 batch 크기와 배치 다양성

| 물음 | 답 |
|---|---|
| batch size = 1 이 사실인가 | ⭕ **사실이다.** §3.1: *"…locate the global optimum **with batch size of 1**"*, `Fig. 2` 캡션 G: *"**k=1 is used for maximum sample efficiency**"* |
| 배치 확장(qEI / qEHVI / local penalization / Kriging believer)을 다뤘나 | ⛔ **한 글자도 없다.** `qEI`·`qEHVI`·`penalization`·`parallel` 전부 0회 |
| 배치 다양성(diversity)을 다뤘나 | 🔴 **서론에서 "한다"고 선언하고 안 한다.** §1 마지막: *"we additionally introduce an improved sample selection strategy that balances both quality (acquisition function score) **and diversity** to mitigate redundant querying — a known failure mode of greedy acquisition in materials spaces."* — 그런데 **`diversit*` 는 논문 전체에서 그 한 줄이 유일**하다. 정의도, 수식도, 실험도, 결과도 없다 |
| 왜 구조적으로 불가능한가 | **batch=1 이면 "배치 안의 다양성" 이라는 개념이 성립하지 않는다.** 한 번에 하나 고르는데 중복 질의를 막을 대상이 없다 |

🔴🔴 **우리에게 이건 치명적이다.** 우리 오라클은 **UMA-MD 이고 GPU 큐에 병렬로 던진다** —
설계 하나를 돌리고 결과를 기다렸다가 다음 하나를 고르는 순차 루프는 자원 낭비다.
**이 논문은 배치 AL 에 대해 아무 근거도 주지 않는다.** 배치가 필요하면 다른 문헌을 찾아야 한다.

⚠ 추가로 짚을 것: **초기 라벨셋이 무작위가 아니라 "물성 최저 K%"** 다.
§2.1: *"our initial population is selected as a given percentage of samples with the **lowest/highest** properties
instead of random selection to reduce the experiment uncertainty"* — 그리고 `Fig. 2` C 블록이
*"Pick **bottom** K% of samples"* 로 그림에도 박혀 있다.
🔴 **그런데 같은 §2.1 의 몇 줄 뒤가 정반대로 쓴다**: *"The process initializes by **randomly** selecting a small
percentage of these materials to form the initial 'labeled' training set."* — **자기모순이다.**
그림과 앞 문장이 일치하므로 **"최저 K%" 가 실제 구현으로 보인다**(§12-6).
이 선택은 결과에 크게 작용한다: 초기셋에 고성능 표본이 **정의상 하나도 없으므로** 순수 **외삽 과제**가 되고,
"추가 평가 수"의 절대값은 이 규칙에 완전히 종속된다.

### 4.5 baseline 사양 — **재현 불가 수준으로 비어 있다**

| 항목 | 기재 여부 |
|---|---|
| GP 커널 | ⛔ **미기재.** 본문에 *"such as the Radial Basis Function (RBF) or Matérn"* 라는 **예시**만. `Matern` 전문 0회 |
| GP 커널 하이퍼파라미터 최적화 | ⛔ 미기재 (재시작 횟수·경계·정규화 모두) |
| GP 노이즈항(α) | ⛔ 미기재 |
| RF 트리 수 T · 깊이 | ⛔ **미기재** (`n_estimators` 0회) |
| 특징 스케일링 | ⛔ 미기재 |
| 라이브러리·버전 (sklearn 등) | ⛔ **미기재** (`sklearn` 0회) |
| 반복 | GP·RF **20회**, TabPFN **1회** (*"TabPFN has no such randomness"* — 결정성 주장만 있고 검증 없음) |
| 하이퍼파라미터 튜닝 | *"We have tuned the hyper-parameters for the UCB and normalized UCB and normalized EI"* — **어떻게·어디서 튜닝했는지 미기재.** β=30, ξ=0.2 로 전체 고정 |

⚠ **β = 30 은 정규화 UCB 에서 사실상 순수 불확실도 샘플링이다.** μ_norm·σ_norm 이 둘 다 [0,1] 이므로
`μ_norm + 30·σ_norm` 은 σ 항이 30배 무겁다 ⇒ **`ucb_norm` ≈ max-variance 질의**.
저자는 이걸 논하지 않는다. **"UCB 가 이겼다"가 "탐색이 이겼다"인지 "UCB 라는 형식이 이겼다"인지 구분이 안 된다.**

### 4.6 데이터셋 — `Table 3`

| 코드 | 데이터셋 | 표본 | 특징수 | 목표 |
|---|---|---|---|---|
| LTC_C | LTC 농도특징 | 3,148 | 62 | 격자열전도도 최대 |
| LTC_M | LTC Magpie | 3,148 | 126 | 동 |
| LTC_S | LTC Magpie+구조 20 | 3,148 | 146 | 동 |
| Cu_HD_C | Cu 합금 경도 (농도) | 1,614 | 34 | 경도 |
| Cu_HD_M | Cu 합금 경도 (Magpie) | 1,614 | 132 | 경도 |
| Cu_EC_C | Cu 합금 전기전도도 (농도) | 1,826 | 34 | %IACS |
| Cu_EC_M | Cu 합금 전기전도도 (Magpie) | 1,826 | 132 | %IACS |
| Glass_DS1 | Fe계 BMG (농도) | 495 | 22 | 임계주조직경 D_max |
| Glass_DS2 | Fe계 BMG (물리특징) | 495 | 14 | 동 |
| Glass_DS3 | Fe계 BMG (Magpie) | 495 | 145 | 동 |

- 특징 산출: **matminer** [53]. 조성(Magpie 통계·평균 원자가궤도·이온성 근사) + 구조(밀도) + 대칭(공간군).
- **다이아몬드(C)는 LTC 데이터셋에서 의도적으로 제외** — LTC 가 너무 높아 과제를 자명하게 만들기 때문.
- ⚠ 표 캡션은 **"25 Benchmark Datasets"** 인데 10행이다. §2.3 이 소개하는 **ChEMBL/ADMET 분자 10종**
  (Caco-2 910 · clearance microsome 1,102 · clearance hepatocyte 1,213 · VDSS 1,130 · PPBR 1,614 ·
  lipophilicity 4,200 · LD50 7,385 · half-life 667 · FreeSolv 642 · SARS-CoV-2 3CLpro 880, RDKit 210 서술자)은
  **결과에 단 한 번도 안 나온다**. 10+10=20 이고 25도 아니다.
- ⚠ §2.3 오타: *"The hardness dataset (**Cu_HD_C/M**) has 1614 samples while the electrical conductivity
  dataset (**Cu_HD_C/M**) has 1826"* — 뒤쪽은 `Cu_EC_C/M` 이어야 한다.

### 4.7 ★4 비용 회계 — **분모에 대리모형 비용이 없다**

| 물음 | 답 |
|---|---|
| "데이터 효율" 을 무엇으로 쟀나 | **전역 최적점을 찾을 때까지 추가로 라벨한 표본 수(extra evaluations) 하나뿐.** batch=1 이므로 = AL 사이클 수 |
| DFT 호출 수를 쟀나 | 해당 없음 — **DFT 를 안 쓴다.** 라벨은 이미 다 있는 데이터셋에서 조회한다 (pool-based 시뮬레이션) |
| GPU 시간 / wall-clock 을 쟀나 | ⛔ **0.** 전문 검색: `GPU` 0회 · `CPU` 0회 · `runtime` 0회 · `wall` 0회 · `second`(초) 는 전부 *"second group of datasets"* 류 |
| **대리모형 학습·추론 비용을 분모에 넣었나** | 🔴 **넣지 않았다.** 그리고 **재지도 않았다.** 비용 논의는 전부 **실험 비용**(합금 1점 $500–$3,000, 기능성 재료 $20,000)으로만 환산된다 |
| 그 은폐가 실제로 문제인가 | ⚠ **이 논문의 설정에서는 상대적으로 덜 문제다** — 실험 1점이 $500–$20,000 이면 forward pass 는 무시할 만하다. 저자의 암묵 가정은 그것이고, 명시하지 않았을 뿐이다. **🔴 그러나 우리에게는 그 가정이 성립하지 않는다** (§13-2) |
| GP 의 O(n³) 를 언급하나 | ⭕ 서론에서 한계로 언급. 하지만 **실측 시간은 안 잰다** |

⇒ **★4 판정: "안 넣었다." 그리고 대리모형 쪽 비용을 어떤 단위로도 보고하지 않는다.**
이 축의 전형적 은폐이고, 이 논문도 예외가 아니다. 다만 **의도적 은폐라기보다 "실험 대비 무시 가능"이라는
미진술 가정**으로 보인다 — 그 가정을 우리 계로 옮기면 깨진다.

## 5. Figure set ★

| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| 1a–d | 대리모형 딜레마 개념도 — (a) GP=원리적/저표현력 vs RF·NN=고표현력/저캘리브레이션, (b) 파운데이션 모델이 둘을 합친다, (c) 표현력–UQ 2D 배치도, (d) AL 수렴곡선 모식 | **수치 0 · 손그림.** 슬라이드 도해 착상용으로만. ⚠ 축 라벨 오타·(b)(c) 제목 중복·캡션과 패널 불일치 — **그대로 재사용 금지** |
| 2 | pool-based AL 파이프라인 A→K 흐름도 | **우리 cascade 흐름도와 1:1 대조 가능.** ★ C 블록 *"Pick bottom K%"* (무작위 아님) · G 블록 *"k=1"* (batch 1) · H 블록 *"Top-1"* 이 이 논문 설계의 3대 제약 |
| 3a,b | cu_hardness, GP(ucb_norm) vs TabPFN(ucb). (a) 전 init_ratio 곡선, (b) 0.05–0.50 막대+오차막대 | GP 는 init 0.05–0.10 에서 100 넘게 쓰고 TabPFN 은 5–39. **★ (b) 에서 TabPFN 막대에만 오차막대가 없다** — 단일 실행이기 때문 |
| 3c,d | 동 데이터셋, RF(ei_norm) vs TabPFN | RF 의 **불안정성**(0.25 에서 ~87, 0.40 에서 ~65 스파이크, 오차막대 상한 ~155)이 이 논문 최고의 그림. **우리 committee 산포 논의에 쓸 수 있는 형태** |
| 4a,c | **cu_electric**, GP(ei)/RF(ei) vs TabPFN(ei) | ★ **저-init 역전**: init 0.05–0.10 에서 TabPFN 이 80–83 으로 **GP·RF 보다 나쁘다**. 최소 데이터 문턱의 실물 |
| 4b,d | **glass_DS3(Magpie)**, GP(ei)/RF(ucb_norm) vs TabPFN(ucb) | 승률 최고(95%/80%). ⚠ **패널에 데이터셋 이름이 없다** — 캡션에만 있어 a/c 와 혼동하기 쉽다 |
| 5a,b | **ltc_conc**, GP(ucb) vs TabPFN(ucb_hybrid) | ★ **init 0.05 에서 TabPFN 506 vs GP 328 (TabPFN 참패), 0.10 에서 111 vs 303 (역전)** — 문턱이 0.05↔0.10 사이에 있다는 유일한 직접 증거 |
| 5c,d | 동, RF(ucb) vs TabPFN(ucb_hybrid) | RF 가 init 0.50 까지도 89–152 로 **수렴 자체를 못 한다**. ★ 단 (d) 의 init 0.05 는 **RF ~157 vs TabPFN ~505 로 TabPFN 이 3배 나쁜데 본문이 이 사실을 언급하지 않는다** |
| Table 1 | 획득함수 6종 정의 | ★1 원표. 그대로 우리 스윕 목록으로 쓸 수 있다 |
| Table 2 | 세 대리모형의 μ·σ 정의 | ★2 원표. **TabPFN σ = (q97.5−q2.5)/3.92** 가 여기 있다 |
| Table 3 | 벤치마크 10종 사양 | ⚠ 캡션은 "25" |
| Table 4 | 데이터셋별 평균 추가평가 + 절감률 | ★ 헤드라인 원표. **승자 열을 세면 TabPFN 7/10** (본문 주장 8/10 과 불일치) |
| Table 5 | Cu 전도도 5-fold CV: RMSE·R²·Spearman·NLL·PICP·MPIW·AUSE | ★ **기전 주장의 근거.** GP 는 PICP 0.93 을 MPIW 32.5 로 사서 얻는다 |
| Table 6 | LTC 농도특징 5-fold CV, 동일 지표 | ★★ **R²=0.18 예측기로 AL 이 굴러간 증거.** GP PICP 0.99 / MPIW 237 = 병적 과대추정 |

**본 그림 / 안 본 그림**: 크로핑 11장 중 **`Fig. 1–5` 5장 전부**와 **`tab_4.png` 1장**을 실제로 Read 로 봤다
(= **6/11**). `tab_4.png` 만 예외적으로 본 이유는 §12-2 의 근거인 **`[ ]` 표시가 조판 형식이라 텍스트 추출로는
확인이 안 되기 때문**이고, 보고 나서 **`[30.1]`·`[8.8]`·`[28.2]`·`[39.9]` 네 개가 실제로 대괄호+굵게** 표시돼 있고
그 넷이 헤드라인 평균의 구성원임을 확인했다. `Table 1·2·3·5·6` 5장은 **안 봤다** — 글자라 PDF 텍스트가 더 정확하고,
위 수치는 전부 본문 텍스트에서 왔다.
그림에서만 읽은 값은 아래에서 **`figure-read ≈`** 로 표시한다.

### 5-b. 그림 ↔ 본문 대조 — 어긋난 것 (실제로 보고 잡은 것)

| # | 본문 서술 | 그림이 보여주는 것 | 판정 |
|---|---|---|---|
| ① | *"TabPFN maintains both low mean extra evaluations **and tight error bars** throughout"* (§3.1, cu_hardness) | `Fig. 3b`·`3d`·`5b`·`5d` 의 **TabPFN 막대에는 오차막대가 아예 없다** | 🔴 **"tight" 가 아니라 "없다".** 1회 실행이라 산포를 잴 수 없다. **재현성 주장의 근거가 되지 못한다** |
| ② | cu_electric: *"a notable exception emerges at very low initial training set sizes (**init_ratio ≤ 0.15**): TabPFN requires ~80–83"* | `Fig. 4a`: TabPFN 은 0.05≈80, 0.10≈83 인데 **0.15 에서 ≈37 로 이미 GP(≈75)를 크게 이긴다** (`figure-read ≈`) | 🟠 **문턱을 한 점 과대 서술.** 실제 열세 구간은 ≤0.10 |
| ③ | cu_electric: *"TabPFN drops to **below 15** evaluations across the same range [0.20 이상]"* | `Fig. 4a`: 0.45≈29, 0.65≈36, 0.80≈25 (`figure-read ≈`) | 🔴 **사실과 다르다.** 최소 3점이 15를 크게 넘는다 |
| ④ | ltc_conc RF 비교: *"RF (UCB) fails catastrophically… requires **100–160** across init 0.15–0.50"* | `Fig. 5c`: 0.15≈151, 0.20≈152, 0.25≈120, 0.30≈104, 0.35≈110, 0.40≈121, 0.45≈97, **0.50≈89** (`figure-read ≈`) | 🟠 하한이 89 다. 방향은 맞고 범위가 살짝 넓게 잡혔다 |
| ⑤ | ltc_conc: TabPFN 이 init 0.05 에서 GP 보다 나쁘다는 것만 논한다 | `Fig. 5d`: **같은 지점에서 RF ≈157 vs TabPFN ≈505 로 3.2배 나쁘다** (`figure-read ≈`) — 본문은 **언급하지 않는다** | 🔴 **불리한 비교의 선택적 미보고** |
| ⑥ | `Fig. 1` 캡션 (c) = *"Active learning with foundation-model surrogates…"* | 패널 (c) 제목은 **(b)와 동일한 "Tabular Foundation Models (Meta-Learned Priors)"** 이고 내용은 2D 배치도 | 🔴 캡션–패널 불일치 |
| ⑦ | §3.1 *"averaged across all **19** init levels (5%–95%)"* | `Fig. 3–5` 의 x축은 **0.05–1.00, 20점**이고, 승률이 **90.0 / 75.0 / 95.0 / 80.0%** 로 전부 1/20 의 배수 ⇒ **분모가 20** (우리 계산) | 🟠 승률 분모(20)와 평균 분모(19)가 다르고, 20에는 **init=1.0 이라는 자명한 점**이 들어간다 |

## 6. 결과 — 절별 정리

### 6.1 cu_hardness — `Fig. 3` (승률 90% / 90%, 이 논문 최고 성적)

- 대진: **TabPFN(ucb)** vs **GP(ucb_norm)** vs **RF(ei_norm)**.
- GP: init 0.05 에서 **≈104**, 0.10 에서 **≈109**(최고점), 0.15 ≈74, 0.20 ≈47, 0.25 ≈30, 이후 0.6 까지 **25–28 고원** (`figure-read ≈`).
- TabPFN: 0.05 ≈**39** → 0.10 ≈**6** → 0.15·0.20 ≈**5** → 0.25–0.40 에서 ≈10–17 로 살짝 반등 → 이후 <10 (`figure-read ≈`).
  본문 표현: *"a 3–20× reduction in experimental effort in the most data-scarce regime"*.
- RF: **불안정.** 0.25 에서 ≈**87**, 0.40 에서 ≈**65** 스파이크. `Fig. 3d` 오차막대 상한이 0.25 에서 ≈**155**.
  저자의 비용 환산: *"a practitioner using RF could require over 150 additional synthesis-and-characterization
  cycles… at a potential cost exceeding **$300,000**"*.
- ⚠ **0.05 지점만 보면 RF(≈33)가 TabPFN(≈39)보다 낫다** (`Fig. 3c`, `figure-read ≈`) — 본문 미언급.

### 6.2 cu_electric + glass_DS3 — `Fig. 4`

**cu_electric (승률 75%/75%)** — 이 논문에서 **최소 데이터 문턱**을 처음 드러내는 데이터셋.
- init ≤0.10 에서 TabPFN(≈80–83)이 GP(≈39–78)·RF(≈23–41)보다 **나쁘다** (`figure-read ≈`).
- 0.20 이후 GP 는 40–85 고원(0.55 에서 ≈85 정점), TabPFN 은 대체로 10–30.
- 저자 결론: *"a minimum initial dataset size, approximately **15–20% of the candidate pool**, should be
  collected before deploying TabPFN-based active learning."*

**glass_DS3 (Magpie) (승률 95%/80%)** — 최고 승률.
- GP 는 init 0.05–0.65 내내 55–89 (`figure-read ≈`), TabPFN 은 전 구간 45 이하.
- RF 와는 중간대(0.45–0.75)에서 곡선이 자주 교차 ⇒ RF 승률 20% (모든 baseline 중 최고).
- 저자 해석: 유리형성능은 결정화 회피라는 **복잡·비선형** 관계라 GP 의 강성 커널이 못 잡는다.

### 6.3 ltc_conc — `Fig. 5` (승률 75%/95%)

- **두 개의 대비되는 실패가 한 그림에 있다.**
  - **GP 형 실패 = 데이터가 더 필요할 뿐**: init 0.05 ≈328, 0.10 ≈303 → 0.15 부터 급락, 0.25 이후 <10.
  - **RF 형 실패 = 수렴 자체를 못 함**: 0.50 까지도 **89–152**, 라벨을 절반 채워도 <10 에 못 간다.
    `Fig. 5d` 오차막대가 크다 ⇒ *"highly sensitive to random seed"*.
- **TabPFN 의 문턱이 여기서 가장 선명하다**: 0.05 에서 **≈506**(GP 328 보다 나쁨) → 0.10 에서 **≈111** (3배 개선).
- 저자의 물리 해석: LTC 는 포논 산란 지배 → 원자질량 대비·결합강성이 조성에 따라 **매끄럽게** 변하므로
  농도 특징만으로도 지형이 단순하다. *"once roughly 20% of the compositional space is sampled, the global
  optimum becomes straightforward to locate."*
- ⚠ 그러면서 *"this result is still surprising as accurate prediction of LTC is extremely difficult by itself"*
  라고 덧붙인다 — **회귀 난이도와 AL 난이도가 다르다**는 이 논문의 반복 주제.

### 6.4 특징 표현(feature representation)이 결정적이다 — `Table 4`

**평균 추가 평가 수 (19개 init 수준 평균, 각 모델의 최선 획득함수 사용)**

| 데이터셋 | GP | RF | TabPFN | 승자 | vs GP | vs RF |
|---|---|---|---|---|---|---|
| cu_electric | 58.5 | 37.5 | **[30.1]** | TabPFN | 48.5% | 19.7% |
| cu_electric_magpie | **82.5** | 90.3 | 83.9 | **GP** | −1.7% | 7.1% |
| cu_hardness | 31.3 | 18.8 | **[8.8]** | TabPFN | **71.9%** | **53.2%** |
| cu_hardness_magpie | **21.9** | 23.5 | 24.1 | **GP** | −10.0% | −2.6% |
| glass_ds1_conc | 72.4 | 66.0 | **48.8** | TabPFN | 32.6% | 26.1% |
| glass_ds2_physical | 37.6 | 43.7 | **32.6** | TabPFN | 13.3% | 25.4% |
| glass_ds3_magpie | 67.5 | 31.6 | **[28.2]** | TabPFN | 58.2% | 10.8% |
| ltc_conc | 56.55 | 61.8 | **[39.9]** | TabPFN | 29.4% | 35.4% |
| ltc_magpie | 243.88 | 44.17 | **41.70** | TabPFN | 82.9% | 5.6% |
| ltc_structure | 237.37 | **55.05** | 84.1 | **RF** | 64.6% | **−52.8%** |
| **헤드라인 평균** | | | | | **52%** | **29.77%** |

`[ ]` = 헤드라인 평균 계산에 들어간 4개 (우리가 역산해 확인 — §12-2).

**저자가 뽑은 세 결론:**
1. **Cu·LTC 에서는 고차원 Magpie(>120)가 AL 을 망친다.** `ltc_magpie` 에서 GP 는 **243.88**(ltc_conc 대비 **6배** 악화).
   원인 주장: 고차원이 GP 커널 추정을 과적합시키고 RF 앙상블 분산을 불안정하게 만들어 **UQ 를 깨뜨린다**.
2. **유리형성능은 정반대다.** 48.8(농도) → 32.6(물리) → **28.2(Magpie)** 로 **특징이 풍부할수록 좋아진다**.
   ⇒ **특징 민감도는 물질군에 종속**된다.
3. ★★ *"the magpie feature can obtain better LTC prediction models, but not necessarily better AL performance"*
   ⇒ **AL 특징 선택을 CV 정확도로 하면 안 되고 AL 성능으로 해야 한다.**
   (⚠ 단, 이 문장의 근거가 되는 "Magpie 가 회귀는 더 잘한다"는 **이 논문 안에 수치로 없다** — `Table 5`·`Table 6` 은
   Magpie 판을 아예 안 잰다. **저자의 인용 없는 주장**이다.)
4. `ltc_structure` 는 **유일하게 RF 가 이긴다**(55.05 vs 84.1). 저자 해석: 구조 특징이 트리 구조에 유리한 귀납편향.

### 6.5 기전 — UQ 캘리브레이션 (`Table 5`·`Table 6`)

**Cu 전기전도도 (%IACS), 5-fold CV** — `Table 5`

| 모델 | RMSE↓ | R²↑ | Spearman↑ | NLL↓ | PICP(0.95) | MPIW↓ | AUSE↓ |
|---|---|---|---|---|---|---|---|
| GP | 8.38±0.51 | 0.73±0.04 | 0.81±0.02 | 3.46±0.03 | **0.93**±0.01 | 32.50±1.02 | 5.58±0.16 |
| RF | 5.86±0.28 | 0.87±0.02 | 0.89±0.02 | 3.11±0.25 | 0.87±0.02 | 15.93±0.35 | 1.77±0.42 |
| **TabPFN** | **5.56**±0.42 | **0.88**±0.03 | **0.92**±0.01 | **2.34**±0.15 | 0.88±0.02 | **11.16**±0.34 | **0.83**±0.12 |

**LTC (농도 특징), 5-fold CV** — `Table 6`

| 모델 | RMSE↓ | R²↑ | Spearman↑ | NLL↓ | PICP(0.95) | MPIW↓ | AUSE↓ |
|---|---|---|---|---|---|---|---|
| GP | 53.26±33.75 | −0.01±0.01 | 0.61±0.04 | 5.81±1.08 | 0.99±0.00 | **237.23**±39.87 | 10.80±3.56 |
| RF | **48.62**±32.22 | 0.18±0.06 | 0.83±0.01 | 7.53±3.42 | 0.86±0.02 | **24.37**±2.74 | 4.50±1.84 |
| **TabPFN** | 48.86±32.78 | 0.18±0.06 | **0.86**±0.01 | **3.22**±0.32 | **0.94**±0.01 | 33.16±3.47 | **2.16**±0.43 |

**저자의 논증 (이 논문에서 가장 잘 쓴 부분):**
- **정확도만으로는 설명이 안 된다** — LTC 에서 TabPFN 과 RF 는 RMSE·R² 가 사실상 동일(48.86 vs 48.62, 0.18 vs 0.18)
  인데 AL 성능은 39.9 vs 61.8 로 갈린다.
- **GP 의 PICP 0.99 는 기만적이다** — MPIW 237.23(TabPFN 의 **7배**)으로 산 것이라
  *"covers almost the entire output range regardless of input and provides no meaningful signal"*.
  ⇒ **과대 불확실도 = 눈먼 탐색**.
- **RF 는 반대로 과소피복** — PICP 0.86 < 0.95 ⇒ *"over-exploit overconfident predictions and miss the global optimum"*.
- **AUSE 가 결정타** — 불확실도 **순서**가 오차 순서와 맞는지를 재는 지표. TabPFN 2.16 vs RF 4.50 vs GP 10.80.
  *"a low AUSE means that samples flagged as uncertain by the surrogate are indeed the ones with the largest
  prediction errors."*
- ⚠ **한계**: CV 는 **랜덤 분할**이고 AL 은 **바닥 K% 시작 → 외삽**이다. **분포가 다른 두 상황을 인과로 연결**한다.
  게다가 CV 를 잰 것은 **10개 중 2개**뿐이고 둘 다 TabPFN 이 이긴 데이터셋이다 —
  **TabPFN 이 진 3개(cu_*_magpie, ltc_structure)에서 UQ 지표가 어떻게 되는지 안 잰다.**
  기전 주장이 반대 사례에서 검증되지 않았다 (§12-8).

## 7. 지표 미니 용어집 (우리가 앞으로 쓸 것들)

| 지표 | 정의 | 무엇에 민감한가 | 우리 쪽 대응 |
|---|---|---|---|
| **NLL** (negative log-likelihood) | `−log p(y_true | μ,σ)`. 정규 가정이면 `½log(2πσ²) + (y−μ)²/(2σ²)` | **proper scoring rule** — 오차와 캘리브레이션을 동시에 벌준다. σ 를 크게 불러 도망갈 수 없다 | 우리 committee 는 NLL 을 안 잰다 (절대 σ 금지라 잴 수 없다) |
| **PICP** (prediction interval coverage probability) | 95% 구간이 참값을 덮은 비율. 목표 0.95 | **혼자 보면 속는다** — σ 를 무한대로 하면 1.0 | — |
| **MPIW** (mean prediction interval width) | 구간 폭 평균 | PICP 의 짝. **둘을 같이 봐야 뜻이 생긴다** | — |
| **AUSE** (area under sparsification error curve) | 불확실도 큰 것부터 버려가며 남은 오차를 그린 곡선과, 실제 오차 순서로 버린 이상적 곡선 사이의 면적 | **σ 의 절대 크기가 아니라 순서만 본다** ⇒ 🔑 **스케일 불변** | ★★ **우리한테 딱 맞다** — 절대 σ 인용이 금지된 우리 committee 도 **AUSE 는 잴 수 있다** (§13-3) |
| **Spearman ρ** | 순위 상관 | 획득함수가 **순위**로 고르므로 RMSE 보다 AL 에 직결 | 우리 cascade 판정 규칙이 이미 ρ̂ + Fisher CI 다 |
| **extra evaluations** | 초기셋 이후 전역 최적을 찾을 때까지 라벨한 개수 | **극단값 탐색 지표** — 꼬리가 지배, 분산 크다 | ⚠ 우리 보고량(D_rel 순위 상관)과 **다른 양** |

**sparsification curve 를 한 단계씩** (우리 쪽에 없는 개념이라 풀어 둔다):
① 테스트셋의 모든 후보에 대해 예측오차 `|y−μ|` 와 불확실도 `σ` 를 구한다.
② σ 가 큰 것부터 5%씩 버리면서, **남은 것들의 평균 오차**를 그린다 → 이게 sparsification curve.
③ 같은 일을 **실제 오차** 순서로 버리며 그린다 → oracle curve (이상적 하한).
④ 두 곡선 사이 면적 = **AUSE**. 0 이면 σ 의 순서가 오차 순서와 완벽히 일치.
⑤ **σ 의 단위·스케일이 전혀 안 들어간다** — 그래서 우리처럼 "절대 σ 는 인용 금지" 인 상황에서도 쓸 수 있다.

## 8. Post-processing

- **한 것**: 5-fold CV 회귀·UQ 평가(§6.5) · 승률 집계 · 평균 추가평가 집계 · 절감률 계산.
- **도구**: `matminer`(특징 생성) · TabPFN(참고문헌 [44]) · GP·RF(라이브러리 미기재).
- **안 한 것**: 통계 검정 0건(p-value·부트스트랩·신뢰구간 전무) · 랜덤 팔 0건 ·
  ablation(β·ξ 민감도) 0건 · 다목적 0건 · 거짓음성 분석 0건.

## 9. ★1–★7 직답 (요청 체크리스트)

| ★ | 물음 | 답 |
|---|---|---|
| **1** | 획득함수 6종과 순위 | §4.3 표. **일관된 승자 없음 — 데이터셋마다 뒤집힌다**(ucb 3 / ucb_norm 3 / ei 2 / ucb_hybrid 1 / ei_hybrid 1). **무작위 대비 배수는 논문에 없다(랜덤 팔 부재)** |
| **2** | foundation-model surrogate 의 정체 | **③ 예측을 그대로 대리값으로.** 동결·fine-tune·임베딩 전부 아니다. **σ = 모델이 직접 낸 분위수**, `(q97.5−q2.5)/3.92`. **앙상블 아님 · GP 헤드 아님 · MC dropout 아님** |
| **3** | batch 크기·다양성 | **batch = 1 확정** (§3.1 + `Fig. 2` 캡션 G). **배치 확장 전무**(qEI·qEHVI·penalization 0회). **다양성은 서론에서 선언만 하고 구현·평가 0** |
| **4** | 비용 회계 | **추가 평가 수 하나뿐.** GPU·wall-clock **측정 0**. **대리모형 비용을 분모에 안 넣었다** — 그리고 재지도 않았다 |
| **5** | 거짓 음성 확인 | ⛔ **안 했다.** `false` 0회. 게다가 과제 정의상(*"전역 최적을 찾을 때까지 돌린다"*) 거짓음성이 **발생할 수 없는 설정**이다 — 조기 중단이 없으니 놓칠 기회가 없다. `Fig. 2` 캡션이 *"Any of / All of Top-K"* 를 언급하지만 **평가 0** |
| **6** | Tompa/Alghamdi/Kurniawan 판정과의 충돌·보강 | §11 |
| **7** | 우리가 쓸 수 있는 것 / 못 쓰는 것 | §12·§13. **코드: 미공개(게재 시 공개 예정) · 라이선스: 미기재 · LTC 데이터: 비공개(요청 시)** |

## 10. 우리 DFT / cascade 대비

> ⛔ 물성 대조표를 만들 수 없다 — **공통 물성이 0** 이다. 대신 **AL 루프 설계**를 대조한다.

| 항목 | [Hu26ICAL] | **우리 cascade** (`cascade_d_rel_estimand_2026_09_08.json`, active) | 판정 |
|---|---|---|---|
| 탐색 공간 | 고정 풀 495–3,148 (라벨 **이미 전부 있음**, 시뮬레이션) | **227 설계** → front **39** (30 dopant × 구조환경) | 🟡 규모는 우리가 1자릿수 작다 |
| **오라클** | **데이터셋 조회**(비용 0, 잡음 0) | **UMA-MD** (설계당 GPU 수시간, **시드 잡음 있음**) | 🔴🔴 **가장 큰 차이.** 이 논문의 라벨은 **결정론적·즉시**다 |
| 라벨 잡음 | **0 으로 가정** (같은 표를 다시 읽으면 같은 값) | **시드 ≥2 (host ≥3), 게이트 근처 3시드** | 🔴 이 논문에는 **반복측정·잡음 모델이 아예 없다** |
| 보고량 | **전역 최적 발견까지의 추가 평가 수** (극단값 탐색) | **`D_rel(600 K, 2–50 ps, cell-conditioned)` 의 값·CI, 순위 안정성, ρ̂+CI+유효표본수** | 🔴 **다른 양이다.** 이 논문의 지표를 우리 카드에 넣을 수 없다 |
| 초기셋 | **물성 최저 K%** (결정론적, 외삽 과제) | front 39 = **점수 상위** (예측기가 고른 것) | 🔴 **정반대 방향.** 우리는 "좋아 보이는 것부터", 이 논문은 "나쁜 것부터" |
| 목표 | **Top-1** 단일목적 | **4축**(이동도·기계·전자·안정) — 행별 `score = 3m+b` 후 집계 | 🔴 **이 논문은 다목적을 안 한다** (저자 스스로 future work) |
| batch | **1** | 병렬 GPU 큐 (배치가 자연스럽다) | 🔴 **안 맞는다** |
| 대리모형 σ | TabPFN 분위수 (단일 모델) | ⛔ **설계표 위 대리모형이 아예 없다.** 우리 σ 는 **힘 층위**의 이종 committee **M=3** (`tools/ionic/mlip_committee.py`) | ⚠ **층위가 다르다** — 겹치지 않는다 |
| UQ 지표 | NLL·PICP·MPIW·AUSE | ⛔ **없다.** 절대 σ 인용 금지라 캘리브레이션을 안 잰다 | ⭕ **AUSE 는 스케일 불변이라 우리도 잴 수 있다** (§13-3) |
| 통계 규율 | ⛔ 검정·CI·부트스트랩 **0건**, 반복 1(TabPFN)/20(GP·RF) | ρ̂ + **Fisher 95% CI** + **블록 부트스트랩** + 유효표본수 + **사전 검정력 고지**(n=39 에서 ρ=0.35 통과확률 ~50%) | ⭕⭕ **우리 규율이 이 논문보다 엄격하다.** 이 논문은 우리 카드의 §7 무효조건 여러 개에 걸린다 |
| 예측기 품질 | LTC 에서 **R² 0.18** 로도 굴러감 | **LODO −0.1805** / 쌍 LOOCV 0.0892 | ⭕ **착수를 막는 이유가 못 된다**는 근거가 하나 더 늘었다 ([Ma25AL] 과 같은 방향) |
| **순환 검증** | 없음 (라벨이 참값) | 🔴 **점수도 UMA, 검증 D 도 UMA-MD** — 같은 퍼텐셜이 틀리면 상관이 오히려 좋아진다 | 🔴 **이 논문은 그 문제를 다루지 않는다.** 라벨이 참값인 세계라서 |

## 11. ★6 — 같은 축 문헌들과의 접속

| 문헌 | 판정 | [Hu26ICAL] 이 하는 일 |
|---|---|---|
| **[Tompa26FT]** *"파운데이션 교체(3배) > fine-tuning 전략 선택(25%)"* | 🟡 **간접 보강, 직접 관련 없음.** 층위가 다르다(MLIP vs tabular). 다만 **"사전학습 프라이어의 품질이 다운스트림을 지배한다"**는 같은 방향의 주장이다 — Hu 는 **fine-tune 을 아예 안 하고** 메타학습 프라이어만으로 GP·RF 를 이긴다 |
| **[Tompa26FT] EMA 긴장** (EMA 0.999–0.9999 가 snapshot ensemble 을 죽인다) | ⛔ **해당 없음.** 이 논문에 EMA·체크포인트·학습 스케줄이 **없다**(학습을 안 하니까). `EMA`·`checkpoint`·`epoch` 전문 0회 |
| **[Alghamdi26]** *"fine-tune 안 한 파운데이션이 Ea 는 8% 안, D 는 2배 과소(D₀ 정확히 1/3)"* | 🟡 **같은 교훈의 다른 사례.** Alghamdi = "지표 하나(Ea)가 맞는다고 다른 지표(D)가 맞지 않는다", Hu = **"회귀 정확도(RMSE·R²)가 같아도 AL 성능은 갈린다"**(`Table 6`: RMSE 48.86 vs 48.62 인데 39.9 vs 61.8). ⇒ **"한 지표로 모델을 승인하지 마라"가 두 층위에서 같이 나온다** |
| **[Kurniawan25]** *"1회 학습의 snapshot ensemble ≈ 100회 앙상블"* | ⛔ **접점 없음.** 앙상블을 안 쓴다. 다만 방향은 같다 — **"UQ 를 위해 모델을 여러 개 만들 필요가 없을 수도 있다"**. Kurniawan 은 학습을 1회로 줄였고, **Hu 는 0회로 줄였다** |
| **[Grasselli25] 식 (27), M ≥ 4** | ⭕ **이 층위에서는 제약이 소멸한다.** TabPFN σ 는 앙상블 분산이 아니라 **단일 모델의 사후분위수**라 M 이 정의되지 않는다. ⚠ **우회했다고 말하면 안 된다** — 우리 M=3 문제는 **힘 층위**이고, 이 논문은 **설계표 층위**다. 두 σ 는 서로를 대체하지 않는다 |
| **[Carrete23]** *"복잡한 추정기가 단순 committee 를 못 이긴다"* (⚠ Carrete 주장, Kurniawan 아님) | 🔴 **정면으로 반대 방향이다.** Hu 는 **더 복잡한 추정기(메타학습 트랜스포머)가 단순 committee(RF 트리 분산)를 이긴다**고 주장한다. **단, 재료·층위·과제가 전부 다르다**: Carrete = NN 힘장의 힘 불확실도(원자 단위, 데이터 수만 점), Hu = 표 회귀의 물성 불확실도(수백 점). ⚠ **"Hu 가 Carrete 를 반박했다" 고 쓰면 안 된다** — 같은 질문을 안 했다 |
| **[Cho25AL]** (argyrodite 실험 PSO, 대리모형 없음, 우리 재계산 enrichment 4.5×) | ⚠ **대조군.** Cho 는 대리모형 없이도 굴러갔고, Hu 는 대리모형 품질이 전부라고 한다. **둘 다 랜덤 팔이 없다** — Cho 는 우리가 `Table S1` 에서 4.5× 를 재계산했고, **Hu 는 재계산할 재료조차 없다** |
| **[Ma25AL]** (GP+EI 액체전해질, 대리모형 out-of-sample 설명분산 ≤0) | ⭕⭕ **직접 보강.** Ma 에서 "예측력이 0 인데 루프가 돌았다"가 관찰이었다면, **Hu `Table 6` 이 그 이유를 준다** — AL 을 굴리는 것은 R² 가 아니라 **σ 의 순서(AUSE)** 다 |
| **[Jain26Rev]** (SSE ML 파이프라인 리뷰: 다목적 집계를 스칼라화하는 우리 09a 를 비판) | 🔴 **도움이 안 된다.** Hu 는 **단일목적 전용**이고 다목적을 명시적으로 future work 로 미룬다 ⇒ **우리 4축 집계 문제에 이 논문은 아무 답도 주지 않는다** |

### 11-b. 🔑 **우리가 이미 TabPFN 을 갖고 있다** (이 인입에서 새로 붙은 연결)

이 논문을 읽고 litdb 를 뒤져 확인한 것 — **우리 쪽에 TabPFN 계보가 이미 두 개 있다.**

| 우리 자산 | 내용 | 이 논문과의 관계 |
|---|---|---|
| `papers/hollmann2025_tabpfn_tabular_foundation_model.md` | **TabPFN 원전** (Hollmann et al., *Nature* **637**, 319–326, 2025, DOI `10.1038/s41586-024-08328-6`, **OA**) — 이 논문 참고문헌 [44] 의 **직계 선행**(그쪽은 *Nature* 본편, [44] 는 v2 arXiv) | ⭕ **모델 사양·한계는 원전에서 읽는다.** Hu 는 모델 자체를 설명하지 않는다 |
| `talks/yang2026_ncm_radial_microstructure_ml.md` | **한양대 BML(우리 랩) 양수영** — 방사형 NCM 미세구조 설계에서 **COMSOL 1911건 → TabPFN 대리모델 → SHAP → 4목적 Pareto** | ⭕⭕ **우리 랩에 TabPFN 을 실제로 돌린 사람이 있다.** ⛔ 단 그 덱은 `citable=no`(L&F 소재, 회사 출판 반대) — **수치 인용 전면 금지**, 여기서는 "역량이 있다"는 사실만 쓴다 |

🔴🔴 **그리고 원전이 이 논문의 헤드라인에 제동을 건다.**
`hollmann2025` digest §3(한계): *"≤10k행/500특징 스케일 검증 — 대용량은 범위 밖. **외삽(훈련범위 밖)은
여전히 취약 계열**."*
그런데 **[Hu26ICAL] 의 과제 설정이 정확히 외삽이다** — 초기셋 = **물성 최저 K%**(§4.4), 목표 = **전역 최대**.
⇒ **"최소 데이터 문턱 10–20%" 는 저자 설명("in-context 예시가 부족해서")보다,
원전이 말한 외삽 취약성으로 더 잘 설명된다** (**우리 해석 · 두 논문 어디에도 없는 논증**):
초기 라벨이 목표값을 **괄호로 감싸지(bracket) 못하면** TabPFN 이 특히 불리하고,
K 를 키워 상위 표본이 섞이기 시작하는 지점에서 갑자기 좋아진다.
`Fig. 5a` 의 0.05→0.10 급전환(506→111)이 그 그림이다.
⚠ **검증 방법도 같이 적어 둔다**: 초기셋을 "바닥 K%" 가 아니라 "무작위 K%" 로 바꿔 다시 돌리면
문턱이 사라져야 한다 — **이 논문은 그 대조를 안 했다.**

⚠ **반대 방향의 우리 기록도 있다 (공정하게)**: 같은 랩 덱은 TabPFN 을 이렇게 평가한다 —
*"TabPFN R² ≈0.99 인데 **Ridge 조차 0.91**, RF/ET/XGB 0.98 ⇒ 'TabPFN 이어야 했다'는 지지되지 않는다."*
🟡 **이 논문이 그 비판에 부분적으로 답한다**: Hu 의 논지가 바로 *"회귀 R² 우위는 작아도 AL 성능은 갈린다
— 결정하는 것은 캘리브레이션"*(`Table 6`)이기 때문이다.
⛔ **그러나 완전한 답은 아니다** — 그 덱의 대상은 **잡음 0 인 결정론적 시뮬레이터**이고 **AL 을 안 했다.**
두 판정은 **다른 과제에 대한 것**이므로 한쪽으로 다른 쪽을 덮으면 안 된다.

## 12. 주의 / 한계 (비판)

**우리가 세거나 재계산해 확인한 것부터.**

1. 🔴🔴 **"8 out of 10 datasets" 가 자기 표와 안 맞는다 — 세면 7 이다.**
   `Table 4` 의 Winner 열: TabPFN = cu_electric · cu_hardness · glass_ds1 · glass_ds2 · glass_ds3 · ltc_conc · ltc_magpie = **7**;
   Gauss = cu_electric_magpie · cu_hardness_magpie = **2**; RF = ltc_structure = **1**.
   그런데 서론·§3.1·결론이 모두 *"lowest number of extra evaluations on **8 out of 10** datasets"* 라고 쓴다.
   **셋 다 같은 값을 반복하므로 오타가 아니라 집계 실수로 보인다.**

2. 🔴🔴 **헤드라인 52% / 29.77% 는 10개 평균이 아니라 "이긴 4개" 평균이다 — 역산해 확인했다.**
   vs GP: (48.5 + 71.9 + 58.2 + 29.4)/4 = **52.00%**  ·  vs RF: (19.7 + 53.2 + 10.8 + 35.4)/4 = **29.775% → 29.77%**.
   ⇒ 들어간 4개 = `cu_electric`, `cu_hardness`, `glass_ds3_magpie`, `ltc_conc` (`Table 4` 에서 `[ ]` 로 표시된 값들).
   **10개 전체 평균이면 vs GP ≈ 39.0%, vs RF ≈ 12.8% 로 크게 떨어진다** (우리 계산 — 특히 vs RF 는 `ltc_structure`
   의 −52.8% 하나가 평균을 반토막 낸다).
   본문 §3.1 에는 *"averaged over the datasets where TabPFN wins **with the best-performing feature set**"* 라고
   **한 번은** 밝혀 두었지만, **초록·결론에는 그 단서가 없다.**
   ⛔ **인용할 때 반드시 "TabPFN 이 이긴 4개 데이터셋 평균" 을 붙인다.**

3. 🔴 **본문–표 수치 불일치 1건.** §3.2 가 *"the lowest AUSE (0.83) compared to **15.58 of GP**"* 라고 쓰는데
   `Table 5` 의 GP AUSE 는 **5.58** 이다. 어느 쪽이 맞는지 알 수 없다 ⇒ **AUSE(GP, Cu) 를 인용하지 않는다.**

4. 🔴🔴 **획득함수를 "보고할 지표 위에서" 골랐다 (selection on test).**
   §3.1: *"For each surrogate model, we pick its **best acquisition function based on the mean extra evaluations**…"*
   → 그 최소값을 그대로 `Table 4` 에 보고한다. **홀드아웃도, 중첩 CV 도, 다중비교 보정도 없다.**
   ⇒ 세 모델 모두 낙관 편향되고, **선택지가 많은 쪽이 더 유리하다**.
   ⚠ 그리고 `Table 1` 의 정의상 **`*_hybrid` 두 개는 "TabPFN 평균 + GP 분산"으로 못 박혀 있어** GP·RF 에는
   적용할 수 없다(실제로 `Fig. 3–5` 에서 baseline 이 hybrid 를 고른 적이 없다) ⇒
   **TabPFN 은 6개 중 최선, baseline 은 사실상 4개 중 최선**일 가능성이 크다. **비대칭 다중비교다.**

5. 🔴🔴 **랜덤 팔이 없다.** `Table 4` 는 GP·RF·TabPFN 셋만 비교한다.
   *"AL enables order-of-magnitude reductions … relative to conventional design-of-experiments or random search"*
   는 **서론의 남의 문헌 인용**이고 이 논문의 실험이 아니다.
   ⇒ **"ICAL 이 무작위보다 몇 배 낫다"를 이 논문으로 말할 수 없다.**
   참고로 우리가 눈금만 대 보면: ltc_conc(풀 3,148, init 5% = 157) 에서 무작위로 단일 전역최적을 찾는 기대값은
   ≈(2,991+1)/2 ≈ **1,496** 이므로 TabPFN 505 는 무작위 대비 ≈3배다 (**우리 계산 · 균등가정 · 논문 미보고**).
   그런데 GP 328 이면 ≈4.6배로 **TabPFN 보다 낫다** — **이 지점에서 "AL 이 낫다"와 "TabPFN 이 낫다"는 다른 명제다.**

6. 🔴 **초기화 규칙이 논문 안에서 자기모순.** §2.1 A: *"lowest/highest properties instead of random selection"* +
   `Fig. 2` C: *"Pick **bottom** K%"* ↔ §2.1 B: *"initializes by **randomly** selecting"*.
   **둘 중 무엇을 돌렸는지 확정할 수 없다.** 이 규칙은 결과의 절대값을 좌우한다.

7. 🔴🔴 **문제 인스턴스가 데이터셋당 사실상 1개다.** 초기셋이 결정론적("최저 K%")이면
   (데이터셋, init_ratio) 조합마다 **AL 문제는 하나뿐**이고, 반복 20회는 **모델 내부 난수**만 흔든다.
   그리고 init_ratio 를 키우면 초기셋이 **중첩(nested)** 되므로 20개 점은 **독립 시행이 아니다**.
   ⇒ **"승률 90%" 는 20번의 독립 시험이 아니라 강하게 상관된 20개 비교**다.
   ⚠ 이건 우리 cascade 카드가 이미 금지한 것과 같은 구조다 — *"39개는 30 dopant·10여 구조환경에 묶여
   독립 표본이 아니다 → 블록 부트스트랩 / 유효 표본수"*. **이 논문은 그 보정을 하지 않는다.**

8. 🔴 **기전 검증이 승리한 데이터셋에서만 이뤄졌다.** CV/UQ 표는 `Table 5`(cu_electric)·`Table 6`(ltc_conc)
   **2개뿐**이고 둘 다 TabPFN 승리 케이스다. **TabPFN 이 진 3개**(cu_electric_magpie, cu_hardness_magpie,
   ltc_structure)의 NLL·AUSE 는 **없다.** *"패배도 캘리브레이션으로 설명되는가"* 를 검증하지 않았다
   ⇒ 기전 주장이 **확증편향 방향으로만** 검사됐다.

9. 🔴 **"고차원 Magpie 가 회귀는 개선하지만 AL 은 악화시킨다"의 앞쪽 절반에 수치가 없다.**
   §4 가 *"high-dimensional Magpie features degrade AL performance … **despite improving standalone regression
   metrics**"* 라고 단정하는데, Magpie 판의 회귀 지표를 **재지 않았다**. **근거 없는 절반**이다.

10. 🔴 **통계적 유의성 판정이 0건.** p-value·신뢰구간·부트스트랩·효과크기 전무.
    `Fig. 5b` 에서 GP 의 오차막대 상한(≈500)이 TabPFN 의 단일값(≈506)과 **겹치는데도** 본문은
    *"a rare case where TabPFN is worse"* 라고 단정한다 (`figure-read ≈`).

11. 🔴 **TabPFN 결정성 주장이 검증되지 않았다.** *"TabPFN has no such randomness"* 라고만 하고,
    입력 순열 앙상블·전처리 난수 등을 어떻게 고정했는지 **기재가 없다.** 그 결과 **TabPFN 은 오차막대가 없고**,
    본문은 그것을 *"tight error bars"*(§5-b ①) 라고 **재현성의 증거처럼 서술한다** — 순환논법이다.

12. 🔴 **재현 불가.** 코드 미공개(*"upon publication"*) · LTC 데이터 비공개 · GP 커널·RF 하이퍼파라미터·
    라이브러리 버전 전부 미기재 · **라이선스 미기재**. 지금 상태로는 어떤 숫자도 우리가 확인할 수 없다.

13. 🟠 **초고 잔재가 많다** (§0 머리말 ①–⑥). `Table 3` 캡션의 "25", 결과에 안 나오는 ChEMBL 10종,
    자리표시자 DOI, 기여 절의 유령 저자 `C.W.`, `Fig. 1` 오타·중복 제목, `Cu_HD_C/M` 오타.
    **개별로는 사소하지만 합치면 "검수 밀도가 낮다"는 신호**이고, §12-1·§12-3 같은 실제 수치 오류와 같은 계열이다.

14. 🟠 **적용 범위 과장.** 초록의 *"electrolyte materials"*(§0-B) · 논의의 *"molecule discovery and drug design"*
    (ChEMBL 실험을 준비만 하고 결과 0) · *"self-driving laboratories"* · *"open-ended generative design"*.
    **전부 하지 않은 것**이다.

15. ⚠ **호의적으로 인정할 것도 있다** — 공정하게 적는다:
    - **저자에게 불리한 결과를 지웠다고 볼 근거는 없다.** `Table 4` 에 **패배 3건(음수 절감률 포함)** 을 그대로 실었고,
      `ltc_conc`·`cu_electric` 의 저-init 열세도 본문에서 **먼저 지적한다**.
    - **최소 데이터 문턱(10–20%)** 을 스스로 한계로 명시한다.
    - **기전 분석(§6.5)의 논리 구조 자체는 옳다** — "정확도가 같은데 AL 성능이 다르다 → 원인은 UQ" 는
      우리가 그대로 빌릴 수 있는 논증 형식이다.

## 13. §우리 cascade · UQ 축에 주는 것 — **UMA 를 AL 대리모형으로 쓰는 구체안**

> ★1–★3 을 근거로 쓴다. 근거가 없는 곳은 **"논문에 없다"** 로 적었다.

### 13-1. 먼저 판정: **UMA 는 이 논문의 자리에 들어갈 수 없다** (★2 의 직접 귀결)

**못 쓰는 이유는 성능이 아니라 형식이다.**
- TabPFN 이 받는 입력은 **표 한 줄**(조성 벡터 또는 Magpie 서술자)이고 출력은 **스칼라 물성의 사후분포**다.
- UMA 가 받는 입력은 **원자 좌표 + 격자**이고 출력은 **에너지·힘·응력의 점추정**이다.
- UMA 는 `D_rel` 을 **한 번의 forward 로 예측하지 못한다** — MD 를 200 ps 돌려야 나온다.
  즉 **UMA 는 대리모형이 아니라 오라클이다.**
- 그리고 UMA 는 **불확실도를 내지 않는다.** 우리가 σ 를 얻는 유일한 경로는 이종 committee **M=3** 이고,
  그건 **힘 층위**의 σ 이지 `D_rel` 층위의 σ 가 아니다.

⇒ **"UMA 를 AL 대리모형으로 쓴다"는 명제는 기각한다.** 대신 성립하는 구조는 아래다.

### 13-2. 성립하는 구조 — **2층 AL** (UMA = 오라클, tabular FM = 대리모형)

```
설계 공간 (227 설계 · 30 dopant × 구조환경)
        │  특징 = 도펀트 조성 벡터 + 우리가 이미 가진 싼 서술자
        ▼
[대리모형 층]  TabPFN — 한 번의 forward 로 D_rel 의 μ·σ (Table 2)
        │  획득함수로 다음 배치 선택
        ▼
[오라클 층]    UMA-MD (Langevin NVT, 600 K, MSD 2–50 ps, 시드 ≥2)  ← 라벨 생산 (GPU 수시간)
        │
        └──→ 라벨을 컨텍스트에 추가 → 재학습 없이 다음 사이클
```

**이 구조에서 이 논문이 실제로 주는 것 / 안 주는 것:**

| 우리 물음 | 이 논문의 답 | 신뢰도 |
|---|---|---|
| 대리모형을 GP 로 할까 RF 로 할까 tabular FM 으로 할까 | **tabular FM** (`Table 5`·`Table 6` 의 NLL·AUSE) | 🟡 **preprint · 우리 계 아님 · 4개 데이터셋 평균** |
| 라벨 몇 개부터 시작해야 하나 | **후보 풀의 10–20%** | 🟡 **우리 227 설계면 23–45 개.** 우연히도 우리 front 39 = 17% 로 **그 창 안에 있다** |
| 예측기 R² 가 낮은데 시작해도 되나 | ⭕ **된다** — LTC 에서 **R² 0.18** 로도 굴러갔다 | ⭕ [Ma25AL] 과 **독립적인 두 번째 증거** |
| 배치로 던져도 되나 | ⛔ **답 없음** — batch=1 만 했다 | 🔴 **다른 문헌 필요** |
| 4축을 어떻게 합치나 | ⛔ **답 없음** — 단일목적 전용, 다목적은 future work | 🔴 **[Jain26Rev] 의 비판이 그대로 남는다** |
| 대리모형 비용을 어떻게 계산하나 | ⛔ **답 없음** — 재지도 않았다 | 🔴 **우리는 재야 한다**: 우리 오라클은 실험($500–$20k)이 아니라 **GPU 수시간**이라 대리모형 비용이 무시 가능하다는 이 논문의 암묵 가정이 **약해진다** (그래도 forward pass 는 여전히 훨씬 싸다 — 정량은 우리가 재야 한다) |
| 안 고른 후보가 정말 나빴나 | ⛔ **답 없음** — 거짓음성 분석 0 | 🔴 **깔때기의 최대 위험이 그대로 미해결** |

### 13-3. 🔑 **오늘 당장 가져올 수 있는 단 하나 — AUSE**

우리 규율은 **절대 σ 인용 금지**이고, Grasselli 식 (27) 때문에 **M=3 에서는 캘리브레이션조차 불가**다.
그래서 우리는 지금 **committee σ 의 품질을 평가하는 수단이 전혀 없다.**

**AUSE 는 그 막다른 골목을 우회한다** — σ 의 **순서**만 쓰고 **절대 크기를 쓰지 않기 때문**이다 (§7).

구체안:
- 대상: `tools/ionic/mlip_committee.py` 의 **M=3 이종 committee 힘 불일치 σ**.
- 절차: DFT 라벨이 있는 구조 집합에서 ① 원자별 힘오차 `|F_UMA − F_ref|` ② committee σ 를 구하고,
  ③ σ 내림차순으로 5%씩 버리며 남은 평균오차를 그리고, ④ oracle 곡선과의 면적 = AUSE.
- **얻는 것**: *"우리 σ 가 큰 배열이 실제로 UMA 가 많이 틀리는 배열인가"* 에 **처음으로 숫자가 붙는다.**
- **얻지 못하는 것**: 절대 σ 의 의미(변함없이 금지) · 캘리브레이션(M≥4 필요, 그대로) ·
  σ 가 물리적으로 옳은가(committee 가 공통으로 틀리면 AUSE 도 좋게 나온다 — 우리 순환검증 문제 그대로).
- ⚠ **새 물리량이 아니라 기존 σ 의 진단이므로 보고량 카드가 필요한지 애매하다** — 값을 원고에 실을 거면
  `kb/templates/estimand_card.md` 를 먼저 채우는 쪽이 안전하다.
- ⚠ **이 논문은 힘 층위 AUSE 를 한 적이 없다** — 우리가 층을 옮겨 쓰는 것이다. **인용은 "지표 정의"까지만.**

### 13-4. 우리 cascade 재설계에 실제로 반영할 4가지

| # | 반영 | 근거 | 강도 |
|---|---|---|---|
| **1** | **획득함수를 문헌에서 고르지 않는다 — 우리 계에서 스윕한다.** 대신 스윕은 **보고 지표 밖에서** 한다(홀드아웃 설계 또는 사전 등록) | §4.3(6종이 계마다 뒤집힘) + §12-4(이 논문이 저지른 selection-on-test) | ⭕ **강함** — 이 논문의 성공과 실패 양쪽에서 나온다 |
| **2** | **`LODO −0.1805` 는 AL 착수를 막는 이유가 아니다.** 문턱은 R² 가 아니라 **σ 순서의 품질** | `Table 6`(R² 0.18 로 굴러감) + [Ma25AL] 재계산(설명분산 ≤0) | ⭕ **강함** — 독립 두 편 |
| **3** | **초기 라벨은 풀의 10–20% 를 목표로.** 227 설계면 **23–45**. 우리 front 39(17%)가 그 창 안 | §3.1·§4(저자 명시) + `Fig. 4a`·`Fig. 5a` 의 역전 | 🟡 **중간** — 다른 재료계·다른 지표에서 나온 수 |
| **4** | **랜덤 팔을 반드시 넣는다.** 이 논문에도 [Cho25AL] 에도 [Ma25AL] 에도 없다 — **세 편 연속 없는 구멍** | §12-5 | ⭕⭕ **가장 강함.** 우리가 이 축 문헌 전체에서 반복 확인한 결손이다 |
| **5** | **초기 라벨셋이 목표 영역을 괄호로 감싸는지(bracketing) 를 설계변수로 승격.** "몇 개" 보다 "어디를 덮는가" 가 먼저 | §11-b(원전의 외삽 취약성 + `Fig. 5a` 급전환) | 🟡 **중간 — 우리 해석이다.** 논문은 이 대조를 안 했다 |

### 13-4b. 착수 난이도 — **생각보다 낮다**

- **모델 조달**: TabPFN 원전이 이미 우리 litdb 에 있고(`hollmann2025_…`), **우리 랩 안에 실제 사용 경험이 있다**
  (`talks/yang2026_…`, ⛔ 수치 인용 금지). ⇒ **새 기법 도입이 아니라 다른 층에 재사용하는 것**이다.
- **규모 적합성**: 원전 검증 범위가 **≤10,000행 / ≤500특징**. 우리 설계 공간은 **227행 × 수십 특징** ⇒ **여유 있다.**
- **배포 제약**: 추론에 **torch + 사전학습 체크포인트** 필요 (우리 덱 기록). gabia/kgy 는 이미 torch 환경이 있지만
  **UMA 와 GPU 를 다투지 않도록** 주의 — TabPFN 추론은 CPU 로도 충분한 규모다.
- ⛔ **[Hu26ICAL] 의 코드는 못 쓴다** (미공개·라이선스 미기재). **획득함수 6종은 `Table 1` 수식으로 직접 구현**한다 —
  전부 두세 줄짜리다.

### 13-5. ⛔ 이 논문으로 하면 안 되는 것

- ⛔ *"파운데이션 모델이 AL 대리모형으로 검증됐으니 UMA 를 대리모형으로 쓰자"* — **층위가 다르다** (§13-1).
- ⛔ *"52% 절감"* 을 단서 없이 인용 — **TabPFN 이 이긴 4개 평균**이다 (§12-2).
- ⛔ *"8/10 데이터셋에서 이겼다"* — **7/10 이다** (§12-1).
- ⛔ *"AL 이 무작위보다 X배 낫다"* — **랜덤 팔이 없다** (§12-5).
- ⛔ *"이 논문이 전해질 AL 을 다뤘다"* — **전해질 데이터셋이 없다** (§0-B).
- ⛔ *"배치 다양성 전략을 제시했다"* — **선언만 하고 구현·평가 0** (§4.4).
- ⛔ *"거짓음성이 없음을 보였다"* — **거짓음성을 볼 수 없는 설정**이다 (§9 ★5).
- ⛔ `AUSE(GP, Cu 전도도)` 인용 — **본문 15.58 vs 표 5.58 불일치** (§12-3).
- ⛔ `figure-read ≈` 값을 본문 명시값처럼 쓰기 — `Fig. 3–5` 의 곡선 값은 **전부 눈금 판독**이고
  본문에 인쇄된 숫자는 `Table 4–6` 과 §3 본문의 "≈" 서술뿐이다. **±10–15% 오차 가정.**

## 14. 인용 가능 문장 (deck / paper 용)

- "In pool-based active learning benchmarks, a tabular foundation-model surrogate (TabPFN) reduced the number
  of extra evaluations needed to locate the optimum by ~52% versus Gaussian-process and ~30% versus
  random-forest surrogates **on the four datasets where it won with the best feature set**
  [Hu et al., arXiv:2603.12567 (2026), preprint]."
- "The advantage was attributed not to regression accuracy — TabPFN and random forest reached identical
  RMSE and R² = 0.18 on the lattice-thermal-conductivity task — but to uncertainty calibration
  (NLL 3.22 vs 7.53; AUSE 2.16 vs 4.50) [ibid.]."
- "A minimum initial labelled fraction of roughly 10–20% of the candidate pool was required before the
  foundation-model surrogate outperformed a Gaussian process [ibid.]."
- "The benchmark used a batch size of one and did not address batch acquisition or batch diversity [ibid.]."
- ⚠ 위 네 문장 모두 **"(preprint)" 표기를 붙인다.**

---

## 15. 관련 digest

★ **`hollmann2025_tabpfn_tabular_foundation_model`** (**이 논문이 쓰는 모델의 원전** — 모델 사양·한계는 여기서 읽는다) ·
🎤 **`talks/yang2026_ncm_radial_microstructure_ml`** (우리 랩 BML 이 TabPFN 을 실제로 돌린 사례 · ⛔ `citable=no`) ·
`tompa2026_finetuning_mlip_foundation_strategies` (파운데이션 MLIP fine-tuning) ·
`alghamdi2026_finetuning_strategies_li_diffusion_mace` (Ea 맞고 D 틀림) ·
`kurniawan2025_comparative_ensemble_uq_nnip` · `grasselli2025_uncertainty_era_ml_atomistic` (M≥4) ·
`carrete2023_deep_ensembles_vs_committees` · `cho2025_multicompositional_argyrodite_experimental_active_learning` ·
`jain2026_ml_pipelines_solid_state_electrolyte_design`
