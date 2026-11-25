# AI 기반 고체전해질 screening 문헌과 우리 cascade의 위치

- 작성일: 2026-08-10
- 범위: 로컬 `litdb` digest + `figures.json` + 실제 crop, 그리고 최신 공개 원문 페이지
- 원칙: 논문 수치는 외부 소환값으로만 취급하고 우리 DB 절대값과 섞지 않는다.

## 한 줄 결론

우리 연구의 가장 방어 가능한 위치는 **“가장 큰 AI discovery funnel”**이 아니다. 현재 강점은 **한 LPSCl modification family 안에서 여러 물리축, gate selection pressure, missingness, 철회 이력과 protocol boundary를 함께 보존하는 failure-aware·provenance-first cascade**다.

ML의 다음 역할도 최종 판정기가 아니라 다음과 같다.

> ML chooses what to calculate next; physics and experiments decide what is true.

## 1. 먼저 서로 다른 계보를 구분해야 한다

| 계보 | 대표 논문 | 실제 역할 | 그림 문법 |
|---|---|---|---|
| physics-only hard funnel | Xiao 2019 | 큰 DB를 안정성·계면·전도·NEB로 순차 필터 | 단계마다 후보 수를 적은 긴 funnel |
| physics gates + small-data classifier | Sendek 2017 | 물리 prerequisite와 40개 실험 label의 logistic classifier를 합침 | physics branch와 ML branch가 최종 shortlist에서 합류 |
| unsupervised prioritization | Zhang 2019 | label이 부족한 상황에서 anion-lattice similarity로 AIMD 후보를 줄임 | 구조 표현→clustering→AIMD verification |
| increasing-fidelity dynamics | Kahle 2020 | 구조 필터→pinball MD→FPMD | 후보 폭은 줄고 계산 fidelity·비용은 증가 |
| expert-curated experimental ML | Hargreaves 2023 | 문헌 전도도 DB를 사람이 정제하고 LOCO·외부 holdout 평가 | 데이터 지도·cluster와 validation을 함께 표시 |
| active-learning DFT flywheel | GNoME 2023 | GNN이 후보를 고르고 DFT label이 다음 round 학습으로 돌아감 | 폐루프 flywheel |
| system-specific MLIP active learning | Kim 2025 | MTP uncertainty로 CSP query를 DFT에 보내고 재학습 | 구조 생성–MLIP–DFT query loop |
| rule funnel + downstream MLIP | Kim 2026 coating | 17,230개 rule/DFT funnel 뒤 한 후보를 AIMD·MLIP interface MD로 심층 검증 | 큰 funnel + finalist deep dive |
| sulfide-specific pretrained MLIP | DPA-SSE 2025 | 15원소 황화물용 energy/force·MD engine | training-coverage map + MD benchmark |
| composition ML + experiment | Kong 2026 argyrodite | 조성만으로 co-substitution 후보를 제안하고 실제 합성·EIS로 닫음 | composition map→predicted optimum→experimental validation |

이 분류가 필요한 이유는 `MLIP`, `ML screening`, `active learning`, `high-throughput DFT`가 같은 말이 아니기 때문이다. UMA나 DPA-SSE는 원자 에너지·힘을 빠르게 계산하는 엔진이고, Sendek·Kong의 모델은 후보 우선순위를 만드는 property model이다. GNoME·Kim 2025는 새 label이 다시 모델로 돌아가는 폐루프다.

## 2. 대표 screening 논문과 배울 그림 문법

### 2.1 Xiao et al. 2019 — 물리 funnel의 고전적 표현

- 104,082 → 62,437 → 1,600 → 302 → 184 → 66 → 6 → 3으로 coating 후보를 단계적으로 줄인다.
- ML이 아니라 thermodynamic·electronic·ionic screening과 계면/NEB 계산의 순차 funnel이다.
- 장점: 각 단계에 후보 수와 criterion이 보이므로 비용과 선택압이 한눈에 들어온다.
- 한계: coating 문제이고, 다축 결과를 모두 남기는 matrix보다 탈락 중심 서사다.

로컬에서 digest·caption·crop을 모두 확인했다.

- digest: `litdb/papers/xiao2019_cathode_coating_screening.md`
- **ACTUALLY VIEWED**: `litdb/figures/xiao2019_cathode_coating_screening/fig_1.png`
- 시사점: 우리도 G1–G5 waterfall에는 이 문법을 쓸 수 있지만, `273→47`은 물리 funnel이 아니므로 같은 화살표에 놓으면 안 된다.

### 2.2 Sendek et al. 2017 — physics와 ML branch의 합류

- 12,831개 Li-containing structure에 물리 prerequisite를 먼저 적용하고, 40개 실험 구조–전도도 pair로 학습한 logistic classifier를 결합해 21개를 남긴다.
- Fig. 1은 물리 branch와 ML branch가 합류하는 구조라서, “ML이 물리를 대체하는 게 아니라 shortlist를 보조한다”는 메시지가 명확하다.
- applicability-domain distance와 uncertainty를 함께 보여준 Fig. 4도 중요하다.
- 우리보다 강한 점: 실제 experimental label, LOOCV/X-randomization, 적용영역을 갖는다.
- 우리보다 약한 점: conductivity 중심이며 host-specific multi-axis trade-off와 철회 ledger는 없다.

로컬에서 digest·caption·crop을 모두 확인했다.

- digest: `litdb/papers/sendek2017_ml_screening_12k_conductors.md`
- **ACTUALLY VIEWED**: `litdb/figures/sendek2017_ml_screening_12k_conductors/fig_1.png`
- **ACTUALLY VIEWED**: `litdb/figures/sendek2017_ml_screening_12k_conductors/fig_4.png`
- 원문: [Machine learning-assisted materials discovery using failed experiments](https://pubs.rsc.org/en/content/articlelanding/2017/ee/c6ee02697d)

### 2.3 Zhang et al. 2019 — label 부족을 unsupervised learning으로 우회

- 2,986개 ICSD entry에서 528개 대표 anion structure를 만들고, modified XRD representation으로 clustering한다.
- 세 clustering model의 fast-conductor group 교집합을 82개 이하 후보로 줄인 뒤 AIMD로 검증해 16개 fast-ion candidate를 보고했다.
- 장점: 적은 label로 넓은 구조공간을 우선순위화한다.
- 한계: anion lattice 중심 descriptor라 cation blocking·연결성·interface·mechanics를 놓칠 수 있고, 실제 논문도 이 false-positive 원인을 인정한다.
- 우리에게 주는 교훈: co-doping label이 없는 현재는 supervised “synergy predictor”보다 구조/화학 다양성 clustering을 acquisition에 쓰는 편이 정직하다.

원문은 [Nature Communications 2019](https://www.nature.com/articles/s41467-019-13214-1)에서 확인했다.

### 2.4 Kahle et al. 2020 — 점점 비싸지는 dynamics funnel

- 4,963 unique structure → 1,362 → 1,016 → 971 → 796 pinball MD → 132 FPMD.
- pinball은 ML이 아니라 frozen-host, 3-parameter physics surrogate다.
- 장점: 음성 사례까지 넓게 계산하고, 싸고 거친 동역학을 FPMD 앞에 둔다.
- 한계: 부분점유 구조를 입구에서 제외해 argyrodite disorder를 놓치고, host relaxation도 제한된다.

로컬에서 digest·caption·crop을 모두 확인했다.

- digest: `litdb/papers/kahle2020_ht_aimd_screening.md`
- **ACTUALLY VIEWED**: `litdb/figures/kahle2020_ht_aimd_screening/fig_1.png`
- 시사점: 우리 발표의 cascade schematic은 “candidate count↓ / cost and fidelity↑”를 유지하되, UMA/BVSE/DFT의 허용 주장 강도도 같이 적어야 한다.

### 2.5 Hargreaves et al. 2023 — 모델보다 먼저 DB를 만든 사례

- 214개 출처에서 820개 entry를 사람이 정제했고, 상온 부근 unique composition은 403개다.
- composition-only classifier/regressor를 LOCO와 별도 11-material experimental holdout으로 평가한다.
- 장점: 단위·측정법·온도·중복 문헌값의 문제를 모델보다 먼저 다룬다.
- 우리에게 가장 직접적인 교훈: `x label`, actual composition, plain/Cl-rich, raw/derived/literature status를 먼저 고치지 않으면 모델 성능은 의미가 없다.

원문은 [npj Computational Materials 2023](https://www.nature.com/articles/s41524-022-00951-z)에서 확인했다.

### 2.6 GNoME 2023 — DFT가 다시 학습 데이터가 되는 flywheel

- candidate generation → GNN filtering/uncertainty → DFT verification → retraining을 6회 반복한다.
- 2.2 million hull-below structures를 보고했고, updated hull의 new entry는 381,000개다.
- 장점: prospective DFT hit rate가 round마다 개선되는 실제 active-learning loop다.
- 한계: 주 target은 crystal stability이며, LPSCl의 conductivity·oxidation·mechanics·interface를 한 모델이 판정하는 것은 아니다.
- 시사점: 우리 future slide는 “ML top-1”보다 **boundary/disagreement/novel chemistry를 DFT에 보내고 label을 append하는 loop**로 그리는 게 맞다.

원문은 [Nature 2023](https://www.nature.com/articles/s41586-023-06735-9)에서 확인했다.

### 2.7 Kim et al. 2025 — 황화물 CSP의 system-specific active learning

- MTP가 USPEX 구조 탐색을 가속하고, uncertainty가 큰 query structure를 DFT로 보내 재학습한다.
- 최종 structure ranking은 DFT energy와 RDF 비교로 다시 확인한다.
- 우리 공동치환 future와 가장 가까운 도해지만, 이 논문은 네 조성의 crystal-structure prediction이고 47종 multi-property screening은 아니다.

로컬에서 digest·caption·crop을 모두 확인했다.

- digest: `litdb/papers/kim2025_csp_metastable_edge_sharing_sse.md`
- **ACTUALLY VIEWED**: `litdb/figures/kim2025_csp_metastable_edge_sharing_sse/fig_1.png`

### 2.8 Kim et al. 2026 — rule funnel 뒤 MLIP interface MD

- 17,230 → 4,634 → 265 → 154 → 150 → 88 → 8 → finalist로 줄인다.
- 뒤에서 AIMD와 SevenNet interface MD를 쓴다. 즉 MLIP가 입구의 discovery classifier가 아니라 finalist dynamics engine이다.
- 우리보다 강한 점: 두 계면과 downstream long-time dynamics까지 연결한다.
- 우리보다 약한 점: Li–Li distance 같은 단일 descriptor의 blind spot과 단일 interface configuration의 일반화 문제가 남는다.

로컬에서 digest·caption·crop을 모두 확인했다.

- digest: `litdb/papers/kim2026_hts_li3sc2po43_coating_midni_ncm.md`
- **ACTUALLY VIEWED**: `litdb/figures/kim2026_hts_li3sc2po43_coating_midni_ncm/fig_1.png`

### 2.9 Anderson & McCalla 2024 — 우리와 가장 가까운 실험형 dopant matrix

- LLZO라는 다른 host지만, 많은 dopant를 같은 실험 matrix에서 phase fraction, ionic/electronic conductivity, electrochemical window, CCD로 비교한다.
- 장점: 모든 후보×여러 축을 실제 측정하고, 자기 cut이 전 후보를 없애면 codoping 필요성을 결론으로 남긴다.
- 우리 대비: 그들은 experimental matrix가 강하고, 우리는 LPSCl에서 computation provenance·gate audit·protocol boundary가 더 상세하다.
- 절대값과 dopant ranking은 LLZO→LPSCl로 이식하면 안 된다.

로컬에서 digest·caption·crop을 모두 확인했다.

- digest: `litdb/papers/anderson2024_llzo_comprehensive_dopant_screening.md`
- **ACTUALLY VIEWED**: `litdb/figures/anderson2024_llzo_comprehensive_dopant_screening/fig_1.png`

## 3. 황화물·argyrodite에 특히 직접적인 AI/ML 사례

### DPA-SSE 2025

DPA-SSE는 15원소와 equilibrium/out-of-equilibrium configuration을 포함하는 황화물 전용 pretrained Deep Potential이다. 논문은 heating trajectory에서 energy error <2 meV/atom, force error 약 30 meV/Å를 보고하고, LGPS·argyrodite 계열을 포함한 MD와 fine-tuning/continuous learning을 제안한다. 이는 universal UMA와 별도로 **황화물 domain specialization**이 얼마나 중요한지 보여준다. 다만 energy/force 정확도가 oxidation onset, interface stability, synthesizability를 자동 판정한다는 뜻은 아니다. [npj Computational Materials 2025](https://www.nature.com/articles/s41524-025-01764-6)

### Kong et al. 2026 — composition ML로 argyrodite co-substitution을 실제 검증

Elements-To-Ionics 모델은 argyrodite 조성만으로 conductivity landscape를 예측하고 Si–Sn, Ge–Si, Ge–Sn co-substitution을 실제 합성했다. 보고된 최고 조성은 `Li6.7Ge0.595Si0.105P0.3S5I`, conductivity 7.2×10⁻³ S cm⁻¹, Ea 0.20 eV다. 이 사례의 핵심은 최고 숫자보다 **실제 pair label과 prospective synthesis가 모델 뒤에 붙었다**는 점이다. 우리 `codoping_ml_v2`에는 이 단계가 아직 없다. [PubMed / Small](https://pubmed.ncbi.nlm.nih.gov/41255030/)

### high-entropy SSE screening 2026

Choi & Jung은 93개 known Li-ion conductor prototype에서 113,098 high-entropy material을 생성하고, ML/DFT/MLIP-MD를 단계적으로 적용해 8개 halide candidate를 제안했다. 표현상 장점은 `generation → ML filter → DFT → fine-tuned MLIP MD`를 한 workflow로 보인다는 점이다. 우리 co-doping future와 방향은 비슷하지만, 현재 우리 DB는 실제 pair structure/label이 0이므로 같은 단계에 있다고 말하면 안 된다. [npj Computational Materials 2026](https://www.nature.com/articles/s41524-026-02116-8)

### co-doping이 다목적 개선을 만든 실험 평행선

로컬 litdb에는 ML이 아니더라도 공동치환의 실험적 가능성을 보여주는 사례가 있다.

- `litdb/papers/ma2024_sb_doping_lpsc_conductivity.md`: Sn/Sb/I multi-substitution으로 conductivity·air stability·Li interface를 함께 본다. **ACTUALLY VIEWED** Fig. 2는 농도 최적점과 과도 치환의 성능 저하를 보여준다.
- `litdb/papers/taklu2021_cucl_dualdoping_air_stability_argyrodite.md`: Cu/Cl dual doping.
- `litdb/papers/li2025_cubr2_dualdoping_argyrodite.md`: Cu/Br dual doping.
- `litdb/papers/liyaru_gaf3_codoping_argyrodite.md`: Ga/F co-doping.

이 문헌들은 “공동치환은 의미 없다”가 아니라 반대로 **조합·농도·자리·전하보상이 상호작용하므로 단순 pair 평균으로는 충분하지 않다**는 근거다.

## 4. 우리 cascade의 이점과 약점

### 실제 이점

1. **같은 host에서 여러 물리축을 동시에 본다.** 일반적인 conductor discovery는 conductivity나 stability 한 축에 집중하는 경우가 많다. 우리는 oxidation, relative stability, mechanics, BVSE/pathway risk를 같은 후보군에서 함께 본다.
2. **trade-off를 결과로 인정한다.** oxidation onset을 올린 6종이 모두 G4에서 멈춘다는 사실을 winner score 뒤에 숨기지 않는다.
3. **gate 자체를 감사한다.** vacuous G1, redundant G2, heuristic-dominated G4, roster-relative G5를 구분한다.
4. **철회와 claim boundary를 보존한다.** single-seed, 잘못된 MSD window, DOS-threshold gap, MLIP reaction artifact를 ledger에 남긴다.
5. **선택적 고비용 검증의 위치가 명확하다.** DFT는 47종 전수 장식이 아니라 boundary·model disagreement·new chemistry를 확인하는 calibration layer가 될 수 있다.

### 아직 이점이라고 부를 수 없는 부분

1. 47종은 O/F 중심의 2026-06-25 snapshot이며 273-run unified ledger가 아니다.
2. `x002/x005/x010`과 실제 concentration=0.25가 충돌한다.
3. plain과 `+Clrich` variant가 일부 species 평균에 섞인다.
4. G4 blocking cutoff가 inherited heuristic이고 selection pressure를 지배한다.
5. deep DFT는 2/47이고 prospective 실험 validation은 없다.
6. 1,081 co-doping pair에는 실제 pair structure·UMA/DFT/experimental target이 0개다.

따라서 발표 제목·초록의 안전한 표현은 다음이다.

> A failure-aware, provenance-first screening cascade for a curated LPSCl modification family

`AI-discovered optimal co-dopant` 또는 `273 candidates screened to 47`은 현재 증거보다 강하다.

## 5. 발표에 적용할 figure 전략

### 본문에 실제 삽입

1. **Introduction** — Sundar 2025 Fig. 1 또는 Fig. 2
   - 실제 crop 확인: `litdb/figures/sundar2025_oxide_coating_screening_lpscl/fig_1.png`, `fig_2.png`
   - 역할: 한 coating도 Li/LPSCl/cathode 계면을 동시에 만족해야 한다는 다목적 문제 제시
   - 주의: coating과 lattice substitution은 같은 문제가 아니다.

2. **Our data lineage** — 자체 redraw
   - `docs/figures/cascade/cascade_seminar_pool_attrition_273_to_47.png`
   - `91×3=273 run slots`과 `47-species versioned snapshot`을 분리

3. **Core result** — 자체 47종 scatter
   - `docs/figures/cascade/cascade_seminar_oxidation_transport_47.png`

4. **Decision view** — 자체 conditional Pareto
   - `docs/figures/cascade/cascade_seminar_pareto_47.png`

5. **Appendix** — 자체 47종 scorecard
   - `docs/figures/cascade/cascade_seminar_scorecard_47.png`

### 그림 문법만 차용하고 자체 redraw

- Xiao/Kim 2026: 각 단계 후보 수를 funnel에 직접 표시
- Sendek: physics branch와 ML branch를 분리한 뒤 validation에서 합류
- Kahle: candidate count↓와 fidelity/cost↑를 동시에 표시
- GNoME/Kim 2025: 새 DFT/실험 label이 DB로 돌아오는 loop
- Anderson 2024: dopant periodic-table map + 모든 축을 동일 matrix로 비교

출판사 crop을 공개 배포 PPT에서 변형·재배포할 때는 license를 별도 확인한다. 내부 연구세미나에서는 원 그림 번호·DOI를 화면에 붙이고, 수정한 도해는 `adapted conceptually from`이라고 구분하는 편이 안전하다.

## 6. 발표용 짧은 비교 문장

> Prior screens usually optimize one discovery target or apply increasingly expensive filters. Our contribution is narrower but different: a host-specific cascade that exposes multi-axis trade-offs, gate weakness, missingness, and retraction history before allocating DFT and experiments.

> The current co-doping model is not yet comparable to experimentally closed-loop argyrodite ML. It is an H0 ranker for designing the first balanced calculation batch.

> Our next defensible AI step is not a deeper model. It is a versioned ledger, real co-doped labels, grouped validation, and an acquisition loop that sends uncertainty, disagreement, and novel chemistry to matched DFT or experiment.

## 7. 핵심 online sources

- [Sendek et al., Energy Environ. Sci. 2017](https://pubs.rsc.org/en/content/articlelanding/2017/ee/c6ee02697d)
- [Zhang et al., Nature Communications 2019](https://www.nature.com/articles/s41467-019-13214-1)
- [Hargreaves et al., npj Computational Materials 2023](https://www.nature.com/articles/s41524-022-00951-z)
- [Merchant et al., GNoME, Nature 2023](https://www.nature.com/articles/s41586-023-06735-9)
- [DPA-SSE, npj Computational Materials 2025](https://www.nature.com/articles/s41524-025-01764-6)
- [Kong et al., argyrodite composition ML + experiment](https://pubmed.ncbi.nlm.nih.gov/41255030/)
- [Choi & Jung, high-entropy SSE screening 2026](https://www.nature.com/articles/s41524-026-02116-8)

