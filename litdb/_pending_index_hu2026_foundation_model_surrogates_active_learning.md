# ⏳ pending — `hu2026_foundation_model_surrogates_active_learning` 의 INDEX / comparison 반영분
> ✅ **① INDEX.md 병합 2026-09-13** (조율 세션). ⏳ **②③ `comparison_vs_ours.md` 블록은 미병합** — 절 번호 충돌(J-11/J-12)·기존 판정 개정 요청이 섞여 있어 큐레이터 판단이 필요하다.

> 2026-09-09, litdb-curator. **동시작업 충돌 회피**로 `INDEX.md` · `comparison_vs_ours.md` 를 직접 안 고쳤다.
> 아래 블록을 **사람이(또는 조율 담당 세션이) 그대로 옮겨 붙이면 된다.**
> digest 본체: `litdb/papers/hu2026_foundation_model_surrogates_active_learning.md`
> 그림: `litdb/figures/hu2026_foundation_model_surrogates_active_learning/` (**11장** = Fig 1–5 + Table 1–6)

> 🔴🔴 **제목에 속으면 안 되는 편이다.** *"Foundation-model surrogates"* 의 foundation model 은
> **UMA·MACE 같은 MLIP 이 아니라 `TabPFN`(표 데이터용 in-context Bayesian 트랜스포머)** 이다.
> 원자·구조·힘·DFT 가 논문에 **전혀 없다.** 층위가 다르다 — UMA 는 *오라클*, TabPFN 은 *설계표 위 대리모형*.

---

## ① `litdb/INDEX.md` — **`## ✅ Digest 완료 (paper-level)`** 표에 추가할 행

```markdown
| `papers/hu2026_foundation_model_surrogates_active_learning.md` | **[외부·methods·★능동학습 대리모형 벤치마크 · 🔴arXiv preprint(동료심사 전) · ⛔물성 4축 아님]** **Jeffrey Hu**(UIUC 재료), **Rongzhi Dong**(USC CSE), **Ying Feng**(항저우전자대), **Ming Hu**(USC 기계), **Jianjun Hu\***(USC CSE), "**Foundation-Model Surrogates Enable Data-Efficient Active Learning for Materials Discovery**" (**arXiv:2603.12567v3** [cond-mat.mtrl-sci], **2026-03-24** · DOI **없음**(각주에 자리표시자 `DOI:000000/11111` 잔존) · 본문 16 pp + refs 3 = **19 pp** · **SI 없음** · Fig 1–5 · Table 1–6 · **코드 미공개**(*"upon publication"*, URL·**라이선스 미기재**) · Cu/유리 데이터는 공개[54][55], **LTC 데이터는 비공개**(요청 시)). **🔴 제목 주의 — 이 논문의 "foundation model" 은 MLIP 이 아니라 `TabPFN` 이다**(표 데이터용 in-context Bayesian 트랜스포머, 원전 = 우리가 이미 가진 `papers/hollmann2025_tabpfn_tabular_foundation_model.md`). **원자단위 계산 0 · MD 0 · DFT 0 · 실험 0**; 라벨은 전부 공개 데이터셋 조회(pool-based 시뮬레이션). **질문**: *"소데이터 AL 의 병목인 대리모형 딜레마(GP=원리적 UQ/저표현력 vs RF·NN=고표현력/휴리스틱 UQ)를 파운데이션 모델로 풀 수 있나."* **답 = ICAL** — GP·RF 를 **TabPFN 으로 갈아끼우면** 전역최적 발견까지의 추가 평가가 준다. **★2 대리모형의 정체(`Table 2`)**: 동결·fine-tune·임베딩 **전부 아니다** — 라벨셋을 **컨텍스트로 프롬프트에 넣고 단일 forward pass** 로 사후예측분포를 얻고, **σ = (97.5%ile − 2.5%ile)/3.92**(정규 가정). **앙상블 아님 · GP 헤드 아님 · MC dropout 아님 ⇒ Grasselli 식 (27) 의 `M≥4` 제약이 이 층위에선 발생하지 않는다**(우회가 아니라 **다른 종류의 σ**). **★1 획득함수 6종(`Table 1`)**: Standard/Normalized/Hybrid × {UCB, EI}, β=**30** ξ=**0.2** 전역 고정; Hybrid = **TabPFN 평균 + 별도 GP 분산**. 🔴 **일관된 승자 없음 — 계마다 뒤집힌다**(TabPFN 최선: ucb 3 · ucb_norm 3 · ei 2 · ucb_hybrid 1 · ei_hybrid 1; 같은 Cu 합금도 특징만 바꾸면 ucb→ei_hybrid). **★3 batch = 1**(§3.1 + `Fig. 2` 캡션 G *"k=1 for maximum sample efficiency"*) — **배치 확장(qEI·qEHVI·local penalization) 0회**, 서론이 선언한 *"quality + **diversity** 선택전략"* 은 **`diversit*` 가 논문 전체에서 그 한 줄뿐**이고 정의·구현·평가 **전무**. **★4 비용 회계**: 지표는 **추가 평가 수 하나뿐**, **GPU·CPU·wall-clock 전문 0회**, **대리모형 비용을 분모에 안 넣었고 재지도 않았다**(암묵 가정 = 실험 1점 $500–$20,000 대비 무시 가능). **★5 거짓음성 0건**(`false` 0회; 전역최적을 찾을 때까지 돌리는 설정이라 **원리적으로 발생 불가**; `Fig. 2` 캡션의 *"Any of / All of Top-K"* 는 말만 하고 평가 0). **결과(`Table 4`, 10 데이터셋 = LTC 3,148×3특징 / Cu 경도 1,614×2 / Cu 전도도 1,826×2 / Fe계 BMG 495×3)**: 최대 절감 **cu_hardness 71.9%(vs GP) · 53.2%(vs RF)**; **특징 표현이 결정적** — Cu·LTC 는 고차원 Magpie(>120)가 AL 을 망치고(`ltc_magpie` GP **243.88** = ltc_conc 대비 6배 악화, `cu_*_magpie` 는 **GP 가 이긴다**), 유리형성능은 정반대로 **Magpie 가 최선**(48.8→32.6→28.2) ⇒ 저자 결론 ***"AL 특징 선택을 CV 정확도로 하면 안 된다"***(⚠ 그 근거인 "Magpie 가 회귀는 더 낫다"는 **논문 안에 수치가 없다**). **★★ 기전(`Table 5` Cu·`Table 6` LTC, 5-fold CV)**: **정확도가 아니라 캘리브레이션**이다 — LTC 에서 TabPFN·RF 가 **RMSE 48.86 vs 48.62 · R² 0.18 동일**인데 AL 은 39.9 vs 61.8 로 갈린다; **NLL 3.22 / 5.81(GP) / 7.53(RF)**, **AUSE 2.16 / 10.80 / 4.50**, GP 의 **PICP 0.99 는 MPIW 237.23**(TabPFN 33.16 의 7배)으로 산 것이라 무의미, RF 는 **PICP 0.86 과소피복**. **★ 최소 데이터 문턱 = 후보 풀의 10–20%** (그 아래선 GP 가 나을 수 있다; `Fig. 5a` ltc_conc init 0.05 에서 **TabPFN ≈506 vs GP ≈328 참패** → 0.10 에서 **111 vs 303 역전**, `figure-read ≈`). **🔴🔴 우리가 세거나 재계산해 잡은 오류 3건**: ①본문 *"8 out of 10 datasets"* 가 **자기 `Table 4` Winner 열과 불일치 — 세면 7/10**(TabPFN 7 · Gauss 2 · RF 1)이고 서론·§3.1·결론이 **같은 값을 세 번 반복**한다 ②**헤드라인 52%/29.77% 는 10개 평균이 아니라 "TabPFN 이 이긴 4개"(`Table 4` 의 대괄호 `[30.1] [8.8] [28.2] [39.9]`) 평균**이다 — 역산 확인 (48.5+71.9+58.2+29.4)/4=**52.00%**, (19.7+53.2+10.8+35.4)/4=**29.775%**; **10개 전체면 vs GP ≈39.0% · vs RF ≈12.8%** 로 떨어진다(우리 계산) ③본문 *"AUSE … 15.58 of GP"* vs `Table 5` **5.58** 불일치. **⛔ 그 밖의 한계(우리 지적)**: 🔴**랜덤 팔 0건**(서론의 *"order-of-magnitude vs random search"* 는 남의 문헌) ⇒ ***"AL 이 무작위보다 X배"를 이 논문으로 말할 수 없다*** · 🔴**획득함수를 보고 지표 위에서 골랐다**(selection-on-test, 홀드아웃·중첩CV·다중비교보정 0) + `Table 1` 정의상 hybrid 2종은 TabPFN 전용이라 **TabPFN 6개 중 최선 vs baseline 4개 중 최선 = 비대칭** · 🔴**초기화 규칙이 자기모순**(§2.1 앞 + `Fig. 2` C = *"Pick **bottom** K%"* ↔ §2.1 뒤 = *"**randomly** selecting"*) · 🔴🔴**문제 인스턴스가 데이터셋당 사실상 1개**(초기셋 결정론적 + init_ratio 를 키우면 초기셋이 **중첩**) ⇒ *"승률 90%"* 는 **강하게 상관된 20개 비교**이고 우리 cascade 카드가 금지한 계수 방식이다 · 🔴**기전 검증이 이긴 데이터셋 2개에서만**(진 3개의 NLL·AUSE 없음 = 확증편향 방향) · 🔴**통계 검정·CI·부트스트랩 0건**(`Fig. 5b` 는 GP 오차막대 상한 ≈500 이 TabPFN 506 과 겹치는데도 단정) · 🔴**TabPFN 결정성 주장이 미검증**이라 오차막대가 없는데 본문은 그것을 *"tight error bars"* 라고 **재현성 증거처럼 서술**(순환) · 🔴**재현 불가**(코드·LTC 데이터·GP 커널·RF 하이퍼파라미터·라이브러리 버전·라이선스 전부 미기재) · 🟠**초고 잔재**(`Table 3` 캡션 *"25 Benchmark Datasets"* 인데 10행 · §2.3 의 **ChEMBL/ADMET 10종이 결과에 0회** · 기여 절의 유령 저자 `C.W.` · `Fig. 1` 축 라벨 오타 `Uncerainty Capcion` + (b)(c) 제목 중복 + 캡션–패널 불일치) · 🔴🔴**초록의 *"electrolyte materials"* 에 해당하는 데이터셋이 논문에 없다**(`Table 3` = LTC/Cu/유리뿐; `lithium` 1회 = 참고문헌 제목) ⇒ **"전해질 AL 논문"으로 인용 금지**. **🔧 우리 좌표 — 판정**: ⛔ ***"UMA 를 AL 대리모형으로 쓰자"는 기각***(UMA 는 조성 벡터를 못 받고 σ 를 안 내며 D_rel 을 단일 forward 로 못 낸다 = **오라클이지 대리모형이 아니다**). ⭕ **성립하는 구조는 2층 AL**: 설계표 → **TabPFN 대리모형(μ,σ)** → 획득함수 → **UMA-MD 오라클(600 K·MSD 2–50 ps·시드≥2)** → 컨텍스트에 라벨 추가(재학습 0). **★ 착수 난이도가 낮다 — 원전 digest 를 이미 갖고 있고(`hollmann2025_…`) 우리 랩 BML(`talks/yang2026_ncm_radial_microstructure_ml`, ⛔citable=no)에 실사용 경험이 있다**; 원전 검증 범위 ≤10k행/500특징 vs 우리 227행 ⇒ 여유. **🔑 오늘 당장 가져올 것 하나 = `AUSE`** — σ 의 **순서만** 쓰고 **절대 크기를 안 쓰므로**, *"절대 σ 인용 금지"* + *"M=3 이라 식 (27) 캘리브레이션 불가"* 인 우리 committee(`tools/ionic/mlip_committee.py`)에도 **적용 가능한 유일한 UQ 품질 지표**다(⚠ 이 논문은 힘 층위 AUSE 를 한 적 없다 — **지표 정의까지만 인용**). **cascade 반영 4+1**: ①획득함수는 문헌 이식 금지, **우리 계에서 스윕하되 보고 지표 밖에서** ②**`LODO −0.1805` 는 착수를 막는 이유가 못 된다**(`Table 6` R²=0.18 로 굴러감 — [Ma25AL] 재계산과 **독립 두 번째 증거**) ③초기 라벨 **풀의 10–20%**(227설계면 23–45, 우리 front 39 = 17% 로 창 안) ④**랜덤 팔 필수**([Cho25AL]·[Ma25AL]·이 편 **세 편 연속 결손**) ⑤**bracketing 을 설계변수로**(우리 해석: 원전이 적은 *"외삽 취약"* + 초기셋=바닥 K% ⇒ 문턱의 진짜 원인이 "예시 부족"이 아니라 "목표를 괄호로 못 감쌈"일 수 있다 — **논문은 무작위 초기화 대조를 안 했다**). ⛔ **물성 4축(A/B/C/D) 편입 금지** — σ·Ea·ESW·탄성·gap **0건**, 그리고 이 논문의 *"electrical conductivity"* 는 **Cu 합금 전자전도도(%IACS)** 로 우리 이온전도도와 **이름만 같다** ⇒ `comparison_vs_ours.md` **§J-9c** + **`🔧 방법 원전`** 에만 | **방법론(능동학습 대리모형·획득함수·UQ 캘리브레이션 지표)** — 물성값 0, **AL 축 세 번째 편** |
```

**⚠ INDEX 행에 같이 반영할 것**
- `hollmann2025_tabpfn_tabular_foundation_model` 행 → *"이 모델을 **AL 대리모형으로** 쓴 벤치마크가
  **`hu2026_foundation_model_surrogates_active_learning`**. 원전 §3 의 *'외삽 취약'* 이 그 논문의
  '최소 데이터 문턱 10–20%' 를 설명할 수 있다(우리 해석)"*
- `cho2025_multicompositional_argyrodite_experimental_active_learning` · (있으면) `ma2025` 행 →
  *"**랜덤 팔 결손이 세 편째다** — `hu2026_…` 도 없다"*
- `tompa2026_finetuning_mlip_foundation_strategies` 행 → *"⚠ 이름이 비슷한 `hu2026_…` 은 **다른 층위**다
  (MLIP 파운데이션 vs tabular 파운데이션). 섞지 말 것"*
- **`hu2026_…` 행 자체에 preprint 표지**: `🔴 arXiv preprint — 동료심사 전, 게재본에서 수치 변경 가능`.

---

## ② `litdb/comparison_vs_ours.md` — **§J-0 출처표** 에 추가할 줄

```markdown
| **[Hu26ICAL]** 🔧 | `hu2026_foundation_model_surrogates_active_learning` — **능동학습 대리모형 벤치마크(ICAL / TabPFN)** (**arXiv:2603.12567v3**, 2026-03-24, **동료심사 전**). 🔴 **"foundation model" = TabPFN(표 데이터용 in-context 트랜스포머)이지 MLIP 이 아니다** — 원자·구조·힘·DFT **전무**. ⚠ **물성값 0**(σ·Ea·ESW·탄성·gap 전무; 이 논문의 "electrical conductivity" 는 **Cu 합금 %IACS**) → 아래 **J-9c** 와 **J-7** 에만 등장, A–D 축 금지. 모델 원전은 우리가 이미 보유 → `hollmann2025_tabpfn_tabular_foundation_model` |
```

---

## ③ `litdb/comparison_vs_ours.md` — **§J-9 밑에 신설: `#### J-9c. [Hu26ICAL] — 파운데이션(tabular) 대리모형 AL 벤치마크`**

```markdown
#### J-9c. [Hu26ICAL] — TabPFN 대리모형 AL 벤치마크 (2026-09-09 신설)

> 🔴🔴 **먼저 층위를 못박는다.** 이 편의 *"foundation model"* 은 **UMA·MACE 가 아니라 `TabPFN`** 이다.
> **UMA 는 오라클(라벨 생산자), TabPFN 은 설계표 위 대리모형** — 둘은 경쟁하지 않고 위아래로 겹친다.
> ⇒ ***"UMA 를 AL 대리모형으로 쓰자"는 이 논문으로 정당화되지 않는다. 기각.***
>
> 🔑 **그런데 우리에게 유리한 사실이 있다** — **TabPFN 원전 digest 를 이미 갖고 있고**
> (`hollmann2025_tabpfn_tabular_foundation_model`, *Nature* 637, 319–326), **우리 랩 BML 에 실사용 경험이 있다**
> (`talks/yang2026_ncm_radial_microstructure_ml` — ⛔ `citable=no`, 여기서는 "역량 존재"만 쓴다).
> ⇒ **새 기법 도입이 아니라 다른 층에 재사용하는 것**이다.

| 항목 | [Hu26ICAL] | 우리 cascade (`cascade_d_rel_estimand_2026_09_08.json`, active) | 판정 |
|---|---|---|---|
| **오라클** | **데이터셋 조회** — 비용 0 · 잡음 0 · 결정론 | **UMA-MD** — 설계당 GPU 수시간 · **시드 잡음 있음** | 🔴🔴 **가장 큰 차이.** 이 논문 세계에는 라벨 잡음 모델이 아예 없다 |
| 탐색 공간 | 495–3,148 (라벨 이미 전부 있음) | **227 설계** → front **39** (30 dopant) | 🟡 우리가 1자릿수 작다 |
| **보고량** | **전역최적 발견까지의 추가 평가 수** (극단값 탐색) | **`D_rel(600 K, 2–50 ps, cell-conditioned)` 의 값·CI · 순위 안정성 · ρ̂+CI+유효표본수** | 🔴 **다른 양이다.** 이 지표를 우리 카드에 넣을 수 없다 |
| 초기셋 | **물성 최저 K%**(결정론적) ⇒ **순수 외삽 과제** | front 39 = **점수 상위**(예측기가 고른 것) | 🔴 **정반대 방향** |
| 목표 | **Top-1 단일목적** | **4축** (행별 `score = 3m+b` 후 집계) | 🔴 **다목적을 안 한다**(저자 future work) ⇒ [Jain26Rev] 의 스칼라화 비판은 **그대로 남는다** |
| **batch** | **1** (`Fig. 2` 캡션 G) · 배치 확장 **0** · 다양성 **선언만** | **병렬 GPU 큐** (배치가 자연) | 🔴 **안 맞는다.** 배치 AL 근거는 다른 문헌에서 |
| 대리모형 σ | **TabPFN 분위수** `(q97.5−q2.5)/3.92` — 단일 모델 | ⛔ **설계표 위 대리모형 자체가 없다.** 우리 σ 는 **힘 층위** 이종 committee **M=3** | ⚠ **층위가 다르다** — 서로 대체하지 않는다 |
| **M≥4 (Grasselli 식 27)** | ⭕ **이 층위에선 제약이 발생하지 않는다** (앙상블이 아니므로 M 이 정의되지 않음) | 힘 층위 M=3 문제는 **그대로 남는다** | ⚠ **우회가 아니라 다른 σ.** "M 문제를 풀었다"고 쓰면 안 된다 |
| UQ 지표 | **NLL · PICP · MPIW · AUSE** | ⛔ 없음 (절대 σ 금지라 캘리브레이션을 못 잰다) | ⭕⭕ **`AUSE` 는 스케일 불변 ⇒ 우리도 잴 수 있다** (아래) |
| 예측기 품질 문턱 | **R² 0.18 로도 굴러갔다** (`Table 6`) | **LODO −0.1805** / 쌍 LOOCV 0.0892 | ⭕ **착수를 막는 이유가 못 된다** — [Ma25AL] 과 **독립 두 번째 증거** |
| 통계 규율 | ⛔ 검정·CI·부트스트랩 **0건** · TabPFN 반복 **1회**(오차막대 없음) | ρ̂ + **Fisher 95% CI** + **블록 부트스트랩** + 유효표본수 + **사전 검정력 고지** | ⭕⭕ **우리 규율이 더 엄격하다.** 이 논문은 우리 카드 §7 무효조건 여러 개에 걸린다 |
| **순환 검증** | 없음 (라벨이 참값) | 🔴 점수도 UMA, 검증 D 도 UMA-MD | 🔴 **이 논문은 그 문제를 다루지 않는다** |
| 랜덤 팔 | ⛔ **없다** | — | 🔴🔴 **[Cho25AL]·[Ma25AL] 에 이어 세 편 연속 결손** |

**🔑 우리가 실제로 가져오는 것 (값이 아니라 지표와 설계 규칙)**

| # | 가져올 것 | 근거 | 강도 |
|---|---|---|---|
| 1 | **AUSE 를 우리 committee 에 이식** — σ 내림차순으로 5%씩 버리며 남은 평균 힘오차 곡선 vs oracle 곡선의 면적. **σ 의 순서만 쓰고 절대 크기를 안 쓴다** ⇒ *"절대 σ 인용 금지"*·*"M=3 캘리브레이션 불가"* 를 **둘 다 우회** | `Table 5`·`Table 6` 의 지표 정의 | ⭕⭕⭕ **오늘 실행 가능. DFT 새 계산 0회** (⚠ 값을 원고에 실을 거면 보고량 카드 먼저) |
| 2 | **획득함수는 문헌 이식 금지 — 우리 계에서 스윕**. 단 **보고 지표 밖에서** 고른다 | §4.3(6종이 계마다 뒤집힘) + §12-4(이 논문의 selection-on-test) | ⭕ 강함 |
| 3 | **`LODO −0.1805` 는 AL 착수를 막지 않는다** | `Table 6`(R² 0.18) + [Ma25AL] | ⭕ 강함 (독립 2편) |
| 4 | **초기 라벨 = 풀의 10–20%** (227설계면 23–45; 우리 front 39 = 17%) | §3.1·§4 저자 명시 | 🟡 중간 (다른 재료계) |
| 5 | **랜덤 팔 필수** | §12-5 | ⭕⭕ 가장 강함 (세 편 연속 결손) |
| 6 | **bracketing 을 설계변수로** — 초기셋이 목표 영역을 괄호로 감싸는지 | 원전 `hollmann2025` §3 *"외삽 취약"* + `Fig. 5a` 506→111 급전환 | 🟡 **우리 해석.** 논문은 무작위 초기화 대조를 **안 했다** |

**🔴 이 편이 닫지 못하는 것 — 반드시 같이 인용**
1. 🔴 **동료심사 안 됐다** (arXiv v3, DOI 자리표시자 잔존).
2. 🔴🔴 **"8 out of 10 datasets" 가 자기 `Table 4` 와 안 맞는다 — 세면 7/10** (TabPFN 7 · Gauss 2 · RF 1).
3. 🔴🔴 **헤드라인 52% / 29.77% 는 "TabPFN 이 이긴 4개" 평균**이다 (역산 확인: 52.00% / 29.775%).
   **10개 전체면 vs GP ≈39.0% · vs RF ≈12.8%** (우리 계산). 초록·결론에는 그 단서가 없다.
4. 🔴 **본문 AUSE(GP, Cu) `15.58` vs `Table 5` `5.58` 불일치** ⇒ 그 값 인용 금지.
5. 🔴 **랜덤 팔 0건** ⇒ *"AL 이 무작위보다 X배"* 를 이 논문으로 말할 수 없다.
6. 🔴 **문제 인스턴스가 데이터셋당 사실상 1개** (초기셋 결정론적 + init_ratio 증가 시 중첩)
   ⇒ *"승률 90%"* 는 독립 20시행이 아니라 **강상관 20비교**. 우리 카드가 금지한 계수 방식이다.
7. 🔴 **획득함수를 보고 지표 위에서 선택** + hybrid 2종이 TabPFN 전용이라 **비대칭 다중비교**.
8. 🔴 **기전 검증이 이긴 데이터셋 2개에서만** — 진 3개의 NLL·AUSE 없음.
9. 🔴 **TabPFN 오차막대 부재를 *"tight error bars"* 라고 서술** (1회 실행이라 산포를 잴 수 없다 — 순환).
10. 🔴 **재현 불가**: 코드 미공개 · LTC 데이터 비공개 · GP 커널/RF 하이퍼파라미터/라이브러리 버전/**라이선스 전부 미기재**.
11. 🔴 **초기화 규칙이 논문 안에서 자기모순** (*"bottom K%"* ↔ *"randomly"*).
12. 🔴 **초록의 *"electrolyte materials"* 데이터셋이 논문에 없다** · §2.3 의 **ChEMBL 10종도 결과에 0회**.

**⛔ 이 축에서 인용하면 안 되는 것 (→ §J-6 에도 추가)**
- ⛔ *"파운데이션 모델이 AL 대리모형으로 검증됐으니 **UMA 를 대리모형으로** 쓰자"* — **층위가 다르다.**
  UMA 는 조성 벡터를 받지 않고, σ 를 내지 않으며, `D_rel` 을 단일 forward 로 못 낸다.
- ⛔ *"52% 절감"* 을 단서 없이 — **TabPFN 이 이긴 4개 데이터셋 평균**이다.
- ⛔ *"8/10 에서 이겼다"* — **7/10 이다**.
- ⛔ *"AL 이 무작위보다 낫다"* 를 이 논문 근거로 — **랜덤 팔이 없다**.
- ⛔ *"전해질 AL 논문"* — **전해질 데이터셋이 없다**.
- ⛔ *"배치 다양성 전략을 제시했다"* — **선언 한 줄뿐, 구현·평가 0**. batch=1 이라 구조적으로도 불가.
- ⛔ *"거짓음성이 없음을 보였다"* — **거짓음성이 발생할 수 없는 설정**이다.
- ⛔ *"M≥4 문제를 풀었다"* — **다른 층위의 다른 σ** 다. 힘 층위 M=3 은 그대로 남는다.
- ⛔ 이 논문의 **"electrical conductivity"(Cu 합금 %IACS)** 를 우리 **이온전도도(mS/cm)** 와 같은 표에 놓기.
- ⛔ `figure-read ≈` 값을 본문 명시값처럼 쓰기 — `Fig. 3–5` 곡선 값은 전부 눈금 판독(±10–15%).
```

---

## ④ `litdb/comparison_vs_ours.md` — **§J-7 `🔧 방법 원전`** 에 한 줄 (교차 포인터만)

```markdown
**[Hu26ICAL] `hu2026_foundation_model_surrogates_active_learning`** — 능동학습 **대리모형·획득함수·UQ 캘리브레이션 지표**의
방법 원전. **물성값 0.** 본문 판정은 **§J-9c** 에 있다(AL 축이라 그쪽이 본진). 여기서는 두 가지만 남긴다:
① **`AUSE`** = σ 의 **순서**만 쓰는 스케일 불변 UQ 품질 지표 ⇒ 우리 committee(M=3, 절대 σ 금지)에 **적용 가능한 유일한 것**.
② **획득함수 6종의 수식**(`Table 1`, β·ξ 포함)은 **두세 줄짜리라 직접 구현**한다 — 저자 코드는 미공개다.
```

---

## ⑤ 🎤 talk 역링크 — **해당 없음** (단, 인접 talk 2건에 포인터 후보)

`grep -l "논문 에이전트 인입 대기열" litdb/talks/*.md` → `talks/lee2026_skku_mlip_materials_design.md` 하나.
그 §99-10 대기열(#1–9)을 전수 확인했고 **이 논문은 대기열에 없다.** ⇒ **talk 파일을 건드리지 않았다.**

> 🟡 **조율 담당이 판단할 포인터 후보 2건** (둘 다 정정이 아니라 **연결**이다):
> 1. **`talks/yang2026_ncm_radial_microstructure_ml.md`** — 우리 랩 BML 이 **TabPFN 을 실제로 돌린 덱**이다
>    (COMSOL 1911건 → TabPFN → SHAP → 4목적). 그 덱의 비판 *"TabPFN R² 0.99 인데 Ridge 조차 0.91 ⇒
>    'TabPFN 이어야 했다'는 지지되지 않는다"* 에 대해, **[Hu26ICAL] 이 부분적인 답을 준다** —
>    *"회귀 R² 우위가 작아도 AL 성능은 갈린다, 결정하는 것은 캘리브레이션"*(`Table 6`).
>    ⛔ **완전한 답은 아니다**: 그 덱은 **잡음 0 결정론적 시뮬레이터**에 **AL 을 안 했다**.
>    ⇒ **한쪽으로 다른 쪽을 덮지 말 것.** 그리고 그 덱은 `citable=no`(L&F 소재, 회사 출판 반대) —
>    **방향은 논문 → talk 뿐**이고 덱의 수치를 digest 로 옮기지 않았다.
> 2. **`talks/lee2026_skku_mlip_materials_design.md`** — MTP 의 `γ`(maxvol/D-optimality 외삽등급) 계보와
>    **같은 질문("어느 후보를 다음에 계산할까")의 다른 답**이다. 대기열 밖이라 손대지 않았다.

---

## ⑥ 이 curator 가 **하지 않은 것** (조율 담당이 확인할 것)

- ⛔ `litdb/INDEX.md` 미수정 (위 ① 를 옮겨야 함)
- ⛔ `litdb/comparison_vs_ours.md` 미수정 (위 ②③④ 를 옮겨야 함)
- ⛔ `db/` 미수정 (`cascade_d_rel_estimand_2026_09_08.json` 은 **읽기만**) · **git 명령 미실행** (요청에 따라)
- ⛔ `litdb/talks/` 미수정 (대기열 밖 — ⑤ 의 포인터 후보만 남김)
- ⛔ `litdb/properties/` 없음 — 물성 원장은 `db/properties/` 이고 이 논문은 넣을 값이 **0** 이다
- ⚠ **`litdb/figures/_sources.json` 은 추출기가 자동 갱신했다** (204편 색인에 이 논문 추가). 의도된 동작이고,
  **다른 큐레이터의 항목은 건드리지 않았다** (추출기가 자기 slug 만 갱신한다).
- ✅ **자동 추출 11장이 전부 정상**이다 — **Fig 1–5 + Table 1–6 = 논문의 전량**, 누락 0.
  추출기가 p.10 에서 후보 2건을 *"영역 없음"* 으로 버렸는데 **둘 다 옳은 기각**이다
  (본문의 *"Figure 4 (a) shows…"* · *"Figure 4 (b)(d) presents…"* 참조 문장이고 위에 그래픽이 없다).
