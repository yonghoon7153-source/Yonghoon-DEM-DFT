# Cascade research seminar — final Korean master script

> Frozen evidence: origin/claude/friendly-meitner-lldvar @ 17d9a373 (2026-08-16)
> Public claim boundary: phase-set comparability 270/270; operational factorial coverage 17/17 chain rows across 11 recipe systems; structural realization 0/11; approved current ranking 0.
> Visible figure labels are English; this file is the deliberately long Korean rehearsal master.


P1. screening은 winner가 아니라 다음 증거를 고른다

[1:40] 계산 완료와 의사결정 승인을 분리한다

[발표 대본]
안녕하세요. 오늘 발표의 질문은 90종 가운데 누가 1등인가가 아닙니다. cascade를 만든 목적은 모든 후보에 처음부터 DFT, 장시간 MD와 계면 계산을 쓰지 않고, 값싼 단계에서 가설과 경계를 넓게 찾은 뒤 결론을 바꿀 수 있는 계산에만 비용을 집중하는 것입니다. 모델 출력은 계산 순서를 바꾸고, matched validation이 claim status를 바꿉니다.

먼저 계보를 고정하겠습니다. 91개 화합물에 x002, x005, x010 세 라벨을 붙여 273개의 실행 슬롯을 만들었고, As2S3 세 슬롯을 제외한 270개가 활성화된 v23 workflow를 마쳤습니다. 이것을 chemistry로 접으면 90종입니다. 47종은 2026년 6월 29일 취합 경계일 뿐 물리적 gate가 아닙니다. 현재 승인된 current ranking과 explicit pair label은 모두 0입니다.

세 농도 라벨도 농도축이 아닙니다. champions_v2의 270행은 모두 generator-defined concentration 0.25입니다. 같은 loading의 별도 실행 기록이지, 2·5·10%의 농도 실험도 아니고 독립 반복도 아닙니다. 그리고 v23의 stage 10 MD conductivity와 stage 11 adhesion은 각각 0/270, 즉 미수확이 아니라 미실행입니다.

G3는 이제 두 층으로 나눠야 합니다. Candidate와 host가 같은 실행과 같은 chemsys에서 같은 pinned MP entry roster를 사용하므로 phase-set comparability는 270/270 닫혔습니다. 17개의 chain champion row에는 formula-level operational counterfactual을 만들었고, 이것은 11개 recipe system에 해당합니다. 그러나 실제 구조와 substitution site를 맞춘 검증은 0/11이고, 보편적인 원소 인과는 주장하지 않습니다. 그래서 operational factorial coverage는 17/17이지만 approved current ranking은 계속 0입니다.

[이해용 확장]
여기서 complete라는 말은 하나가 아닙니다. run complete, record present, method comparable, formula contrast available, structural validation, scientific approval을 따로 세야 합니다. 오늘의 결론은 계산을 많이 했다는 사실보다, 어떤 데이터가 어떤 문장을 허용하는지를 고정한 decision contract입니다.

[예상 질문]
Q. G3가 270/270이면 바로 ranking을 다시 만들 수 있나요?
A. 아닙니다. G3의 방법 비교와 식 수준 대비는 닫혔지만 구조·자리 인과는 열려 있고, G4는 순환·pool-relative composite이며 G5도 validity와 aggregation을 다시 고정해야 합니다.

[전환]
먼저 이 많은 실행이 실제로 어떤 단계로 구성됐는지 pipeline을 열어 보겠습니다.

[Sources]
- 17d9a373:db/properties/oxidation_stability_cascade_v3_pinned.json
- 17d9a373:db/properties/oxidation_matched_factorial.json
- 17d9a373:kb/methodology/cascade_pipeline_anatomy_2026_08_13.md

========================================================================================

P2. 한 개의 개질은 여러 위험을 동시에 움직인다 · 1:05

[1:05] 한 개의 개질은 여러 위험을 동시에 움직인다

[발표 대본]
황화물 전고체전지에서 개질은 한 축만 움직이지 않습니다. 중앙의 셀 개념도를 보면 양극 쪽에서는 전해질 산화와 양극 유래 분해, 계면 접촉 손실이 얽혀 있고, 음극 쪽에서는 환원 분해와 부피 변화, 덴드라이트 문제가 얽혀 있습니다. 따라서 산화 onset이 좋아졌다는 이유만으로 좋은 후보라고 말할 수 없고, Li 경로가 열려 있다는 이유만으로 계면에서 안정하다고 말할 수도 없습니다.

이 그림은 우리 계산 결과가 아니라 문헌에서 정리한 문제 지도입니다. 이 구분이 중요합니다. 우리 계산은 이 모든 실패 모드를 한 번에 재현하지 않습니다. 대신 어떤 축을 계산했고, 어떤 축은 아직 외부 문헌이나 후속 검증에 의존하는지 표시하는 기준으로 사용합니다. 예를 들어 bulk grand-potential 산화 onset은 열역학적 분해 가능성을 말하지만 passivation과 실제 계면 성장 속도는 말하지 않습니다. 정적 legacy BVS와 4 Å blocking은 구조적 경로 위험을 말하지만 실제 확산계수나 전도도는 아닙니다.

그래서 cascade를 여러 게이트로 나눈 이유는 점수를 많이 만들기 위해서가 아니라, 서로 다른 실패 질문을 서로 다른 방법으로 묻기 위해서입니다. 단일 composite score가 편해 보일 수 있지만, 정의가 다른 축을 합치면 어느 축이 결론을 만들었는지 추적하기 어렵습니다.

[이해용 확장]
이 슬라이드는 전고체전지를 처음 보는 청중에게 문제의 범위를 잡아 주는 장입니다. 산화·환원은 전자화학 축, 접촉과 균열은 역학 축, Li 이동은 수송 축이라고 한 단계씩 짚어 주세요. 다만 오늘 발표가 full-cell degradation model은 아니라는 점도 함께 말해야 합니다.

[예상 질문]
Q. 그러면 계면 계산이 없는 bulk screen은 의미가 없나요?
A. 의미가 없지는 않습니다. bulk screen은 위험 후보와 경계 후보를 찾는 저비용 단계입니다. 다만 계면 수명이나 실제 셀 성능을 직접 주장할 수 없고, 다음 계면 계산의 우선순위를 정하는 데 사용해야 합니다.

[전환] 이 여러 질문을 실제 캠페인에서는 몇 개의 실행으로 바꾸었는지 보겠습니다.

[Sources]
- Kang et al., Chemical Communications (2026), DOI 10.1039/D5CC06309D, Fig. 16
- litdb/figures/kang2026_intertwined_electrochemo_mechanical_sulfide_assb_review/fig_16.png (inspected)

========================================================================================

P3. 273은 화학종 수가 아니라 실행 슬롯 수다 · 1:10

[1:10] 273은 화학종 수가 아니라 실행 슬롯 수다

[발표 대본]
캠페인의 출발점은 91개 화합물입니다. 각 화합물에 x002, x005, x010이라는 세 개의 campaign label을 붙여 273개의 최상위 실행 슬롯을 만들었습니다. 여기서 가장 먼저 분리해야 하는 것은 chemistry와 label입니다. chemistry는 LiBr, Ga2S3, Sc2O3처럼 서로 다른 조성이고, label은 같은 chemistry를 다른 농도로 돌리려는 실행 표지였습니다.

v23의 실제 실행 코드를 다시 보면 세 라벨은 모두 `SUPERCELL=1,1,1`인 4 f.u. host cell로 들어갑니다. 구조 생성기는 `n_units = max(1, round(n_fu × requested_x))`를 사용하므로, 요청값 0.02·0.05·0.10은 모두 `n_units=1`로 양자화됩니다. CSV의 `actual_x=0.25`는 이 한 개의 compound formula unit을 4 host f.u.로 나눈 **generator-defined loading**입니다. 보편적인 dopant 25 at%라는 뜻은 아니며, M₂O₃처럼 compound 한 단위에 cation이 두 개면 원소별 site fraction은 화학식에 따라 달라집니다.

따라서 세 라벨은 서로 다른 농도축이 아닙니다. 그렇다고 세 결과가 문자 그대로 같은 원자 구조라는 뜻도 아닙니다. 같은 양자화 loading으로 생성된 별도 top-level execution record이고, seed와 configuration의 중복 가능성을 제거한 controlled replicate도 아닙니다. 따라서 독립성도 구조 동일성도 전제하지 않고, 농도 의존성이나 replicate 통계로 해석하지 않습니다.

이 구분은 뒤의 모든 순위에 영향을 줍니다. 농도 라벨을 실제 농도로 믿으면 blocking 증가나 구조 변화가 농도 응답처럼 보일 수 있고, 세 라벨 평균을 독립 샘플 평균처럼 다룰 수도 있습니다. 현재는 세 라벨을 provenance가 다른 campaign records로만 보존하고, 실제 농도축은 2×2×1 셀로 다시 만든 dual-x 실험에서만 다뤄야 합니다.

[이해용 확장]
청중에게는 91×3=273이라는 산술을 먼저 보여 준 뒤, 곧바로 “세 라벨은 세 농도가 아니었습니다”라고 말하는 것이 좋습니다. 이 한 문장이 뒤 숫자의 과장을 막습니다. chemistry, configuration, property는 273에 다시 곱하는 추가 후보 수가 아니라 의사결정 차원이라는 점도 함께 설명하세요.

[예상 질문]
Q. 세 라벨이 같다면 270 완료라는 숫자도 중복 아닌가요?
A. 실행 기록으로는 270개의 슬롯이 완료된 것이 맞습니다. 다만 독립적인 농도 물리 정보의 개수로 세면 안 됩니다. workload count와 evidence count를 분리해야 합니다.

[전환] 이렇게 많은 작업을 모두 같은 정밀도로 계산할 수 없기 때문에 cascade가 필요합니다.

[Sources]
- 3d5195d0:tools/doping/master_batch_273.sh
- 3d5195d0:tools/doping/run_compound_batch.sh
- kb/methodology/cascade_pipeline_anatomy_2026_08_13.md
- db/properties/cascade_audit_campaign_status.csv

========================================================================================

P4. Cascade는 예측기가 아니라 비용 배치 규칙이다 · 1:20

[1:20] Cascade는 예측기가 아니라 비용 배치 규칙이다

[발표 대본]
Cascade의 핵심은 계산량 자체가 아니라 비용을 어디에 배치하느냐입니다. 먼저 문헌과 데이터베이스로 후보를 큐레이션하고, 같은 규약의 MLIP와 저비용 프록시로 넓게 봅니다. 그다음 물리적으로 위험한 경계와 모델 불일치를 찾아 비싼 DFT, 장시간 MD, 실험으로 올립니다. 값싼 모델은 최종 물성값을 대신하지 않고, 정밀 검증의 순서를 정합니다.

그래서 screening의 성공 기준도 1등 이름을 얼마나 빨리 얻었느냐가 아닙니다. 어떤 후보가 어느 질문에서 멈췄는지, 그 멈춤이 물리 때문인지 정의나 결측 때문인지, 그리고 어떤 추가 계산이 그 불확실성을 가장 싸게 줄이는지를 남겼는지가 더 중요합니다. 최종 생존자가 없어도 다음 계산을 바꾸는 정보가 남으면 cascade는 역할을 한 것이고, 반대로 화려한 ranking이 있어도 그 근거를 추적할 수 없으면 decision product로는 실패입니다.

이 원리는 Xiao의 대규모 coating screen이나 Kahle의 pinball-to-FPMD 흐름과 같은 계열입니다. 규모와 재료, 세부 방법은 다르지만 공통점은 cheap model과 expensive validation의 역할을 분리한다는 것입니다. cheap stage를 acquisition 순서에만 쓰면 오류 비용은 우선순위가 빗나가는 데 제한됩니다. 반대로 hard exclusion에 쓰면 좋은 후보를 영구히 놓칠 수 있으므로, 불확실한 후보는 경계 검증으로 남겨야 합니다. 반대로 cheap stage의 출력을 그대로 최종 물성으로 발표하면 모델 오차가 곧 논문 결론의 오차가 됩니다.

우리 캠페인의 문제는 이 아키텍처가 없었던 것이 아닙니다. 실행·재개·스테이지 기록은 매우 치밀했습니다. 문제는 계산이 끝난 뒤 정본 데이터와 decision product로 이어지는 registration contract가 끊겼다는 점입니다. 따라서 다음 장부터는 계산 성능보다 evidence handoff를 감사합니다.

[이해용 확장]
이 슬라이드에서 “MLIP-to-DFT”를 단순한 정확도 사다리로 설명하지 마세요. 각 층은 다른 질문과 다른 실패 비용을 가집니다. 가장 싼 층은 넓은 탐색, 중간 층은 경계 확인, 비싼 층은 주장 검증입니다.

[예상 질문]
Q. 값싼 모델이 랜덤보다 낫다는 증거가 약하면 cascade도 무의미한가요?
A. 최종 판정을 맡기면 위험합니다. 하지만 오류 가능성을 표시하고 경계·불확실성·다양성 위주로 검증 순서를 정하면 여전히 비용 배치 도구로 쓸 수 있습니다.

[전환] 실제로 계산은 어디까지 끝났고, 정본 의사결정 제품은 어디에서 멈췄는지 보겠습니다.

[Sources]
- Xiao et al., Joule (2019), DOI 10.1016/j.joule.2019.02.006
- Kahle et al., Energy & Environmental Science (2020), DOI 10.1039/C9EE02457C
- litdb local digests and inspected figure crops for Xiao 2019 and Kahle 2020
- docs/cascade_pipeline_guide.md

========================================================================================

P5. stages 00–04는 label 하나를 annealed 후보군으로 바꾼다

[2:10] generate, relax, select, anneal

[발표 대본]
Stage 00의 질문은 계산을 시작할 수 있는가입니다. 환경, 기준구조, 입력과 경로를 점검하고 preflight report와 DONE marker를 남깁니다. 이것은 물성 판정이 아니라 잘못된 실행을 비싼 단계로 넘기지 않는 안전장치입니다.

Stage 01은 어떤 자리에 어떤 치환 recipe를 만들 수 있는가를 묻습니다. Parent structure와 dopant recipe를 받아 substitution site를 열거하고 후보 구조 파일을 냅니다. 여기에는 중요한 알려진 결함이 있습니다. COMPOUND_FILTER가 빠지면 요청한 종 하나가 아니라 약 85종을 전수 열거해 5천 개가 넘는 구조를 만들 수 있습니다. 그래서 이 단계의 핵심 산출물은 구조 수뿐 아니라 어떤 filter와 generator variant를 썼는지에 대한 provenance입니다.

Stage 02는 생성된 구조가 UMA geometry relaxation을 견디는지 묻습니다. 각 후보를 최대 1500 step relax하고 에너지, 부피 변화와 수렴 상태를 냅니다. 비용은 DFT보다 싸지만, 결과는 UMA lineage 안의 screening value입니다. 열역학적 formation energy나 DFT validation은 아닙니다.

Stage 03은 어떤 구조를 다음 단계에 보낼지 묻습니다. 수렴한 후보를 그룹별로 비교하고 --max_dv 0.25, --require_converged 조건으로 winner set을 만듭니다. 이 단계는 후보 수를 줄이지만 화학종의 안정성이나 전도도를 증명하지 않습니다.

Stage 04는 짧은 열 이력 뒤에도 선택 구조가 유지되는지 묻습니다. 500 K, 50 ps의 anneal/FIRE protocol로 post-anneal geometry와 energy를 만듭니다. 과거 300 K, 20 ps는 kT와 장벽 관점에서 폐기됐습니다. 그래도 이것은 conductivity MD가 아니라 구조 흔들기와 재이완입니다. 그래서 다음 stage가 post-anneal geometry를 다시 읽습니다.

[이해용 확장]
이 다섯 단계의 순서는 비용 때문입니다. 먼저 잘못된 환경과 과생성을 막고, 싼 relaxation으로 구조 공간을 줄인 뒤, selected set에만 anneal 비용을 씁니다. 각 단계가 못 하는 것을 다음 단계가 받도록 설계돼 있습니다.

[예상 질문]
Q. Stage 04가 50 ps면 MD 아닌가요?
A. 시간 적분을 쓰더라도 여기서 묻는 것은 전도도나 확산계수가 아니라 anneal 뒤 구조·에너지의 안정성입니다. v23의 σ MD는 별도 stage 10이고 0/270 미실행입니다.

[전환]
Anneal이 끝나면 같은 기하에서 pathway와 mechanical proxy를 읽습니다.

[Sources]
- 17d9a373:tools/doping/tier_cascade.sh
- 17d9a373:kb/methodology/cascade_pipeline_anatomy_2026_08_13.md

========================================================================================

P6. stages 05–08은 annealed geometry를 정적 proxy로 바꾼다

[2:00] pathway proxy, rerank, EOS, elastic

[발표 대본]
Stage 05는 anneal 뒤 geometry에서 Li 환경이 얼마나 열려 보이는가를 묻습니다. 입력은 stage 04의 구조이고 출력은 legacy BVS score와 foreign-center 4 Å proximity metric입니다. BVS는 결합길이에 지수적으로 민감하므로 pre-anneal 구조가 아니라 annealed geometry를 쓰는 순서가 중요합니다. 다만 이 구현은 project canonical softBV와 parameter convention이 다르고, migration barrier·diffusivity·conductivity가 아닙니다.

Stage 06은 anneal 뒤에도 에너지 순서가 유지되는지 묻습니다. Post-anneal energy로 후보를 다시 정렬해 rerank 결과를 냅니다. 이것은 pristine host baseline과 비교한 UMA energy difference이며 chemical potential을 포함한 formation energy가 아닙니다. Low-cost ranking을 갱신하지만 과학적 승인 ranking은 아닙니다.

Stage 07은 작은 부피 변형에 대한 curvature를 물어 EOS와 B0를 만듭니다. Stage 08은 여섯 Voigt strain의 중앙차분과 relaxed-ion response로 Cij, VRH Young modulus와 Pugh ratio를 만듭니다. 둘 다 mechanical plausibility를 보는 MLIP post-processing입니다. 비양의 Hill modulus나 비물리 Poisson ratio는 producer 단계에서 validity failure로 분리해야 합니다.

비용 순서는 stage 05와 06이 많은 후보를 정적 proxy로 줄이고, 그 뒤에 EOS와 elastic finite-strain 계산을 배치하는 구조입니다. 이 네 단계가 알려 주지 못하는 것은 장시간 Li 확산, 실제 BVSE barrier, 전자절연성, 계면 접착과 실험적 내구성입니다.

[이해용 확장]
G4의 blocking은 도펀트 4 Å 안의 Li 비율이고, 도펀트 원자 수와 강하게 연동합니다. 또 historical transport_norm은 blocking fail이면 0.05로 강제되는 순환 구조가 있습니다. 따라서 stage 05를 Li transport라고 부르지 않고 legacy pathway heuristic이라고 부릅니다.

[예상 질문]
Q. Stage 08의 E와 Pugh는 DFT 탄성인가요?
A. 아닙니다. 같은 UMA/MLIP lineage의 finite-strain 결과입니다. relaxed-ion protocol 자체는 표준적이지만, 최종 경계 후보는 matched DFT나 실험으로 다시 봐야 합니다.

[전환]
다음은 계산을 하나의 dataset과 proposal로 묶는 09 계열입니다.

[Sources]
- 17d9a373:tools/doping/tier_cascade.sh
- 17d9a373:tools/doping/run_mlip_postproc.py
- 17d9a373:kb/methodology/cascade_pipeline_anatomy_2026_08_13.md

========================================================================================

P7. stages 09a–09f는 자료를 조립하지만 후보를 검증하지 않는다

[2:05] combine, collect, predict, prepare, audit

[발표 대본]
09a와 09b는 앞 단계의 ranking과 descriptor를 합치고 dataset으로 수집합니다. 질문은 계산 결과가 한 schema로 모였는가입니다. 입력은 여러 JSON이고 출력은 combined ranking과 tabular dataset입니다. 이 단계는 새 물리를 계산하지 않으며, upstream의 잘못된 정의를 그대로 전파할 수 있습니다.

09c는 수집된 campaign 내부 자료로 predictor를 학습합니다. 이것은 global chemistry discovery model이 아니라 이미 생성된 후보 안의 ordering helper입니다. 09d는 상위 후보의 DFT input을 준비합니다. Input deck을 만든다는 것은 DFT가 실행됐거나 검증이 끝났다는 뜻이 아닙니다.

09e는 top 10 composition에 대해 MP phase diagram에서 해당 조성의 hull energy와 decomposition을 기록합니다. 여기서 저장된 값은 E above hull이 아니라 그 조성에서의 hull energy입니다. Candidate UMA energy와 MP DFT hull energy를 직접 빼지 않으므로 metastability gate로 쓰지 않습니다. 대신 decomposition products는 reaction audit에 참고할 수 있습니다.

09f라는 이름에는 ESW가 들어가지만 진짜 grand-potential ESW가 아닙니다. Cascade 내부의 heuristic summary이고 current G2/G3 source로 쓰면 안 됩니다. 현재 G3의 270/270 phase-set-matched 값은 pipeline 밖의 esw_cascade_batch.py가 candidate와 same-run host를 pinned MP entry roster에서 다시 계산해 만든 것입니다.

이 구분을 스테이지 절에서 한 번 강하게 말하고, G3 슬라이드에서는 source가 09f가 아니라 pinned GP라는 한 줄만 다시 연결합니다. 같은 경고를 두 번 반복하는 것이 아니라, 한 번은 pipeline 의미를 고정하고 한 번은 실제 evidence lineage를 고정하는 역할입니다.

[예상 질문]
Q. 09d DFT input이 270개면 DFT 검증도 270개인가요?
A. 아닙니다. 입력 준비와 실행 완료는 다른 상태입니다. 동일하게 09f 파일 존재도 true ESW completion을 뜻하지 않습니다.

[전환]
마지막 tail은 원래 가장 비싼 validation을 배치하려 했지만 v23에서는 실제로 꺼져 있었습니다.

[Sources]
- 17d9a373:tools/doping/tier_cascade.sh
- 17d9a373:kb/methodology/cascade_pipeline_anatomy_2026_08_13.md
- 17d9a373:tools/oxidation/esw_cascade_batch.py

========================================================================================

P8. stages 10–12b에서 미실행과 완료를 분리한다

[2:05] expensive validation tail and orchestration

[발표 대본]
Stage 10은 Li conductivity MD를 의도한 단계입니다. TOP_K_SIGMA 후보에 세 온도, 각 50 ps를 적용하면 대략 12시간이 드는 가장 비싼 축입니다. 그러나 v23에서는 TOP_K_SIGMA가 0이었고 STAGE_10.DONE도 0개입니다. 따라서 정확한 상태는 미수확이 아니라 NOT RUN, 0/270입니다.

Stage 11은 NCM 계면 adhesion과 W_ad를 의도했고 한 건에 약 5–15시간을 예상했습니다. 이것도 v23에서는 STAGE_11.DONE 0개, 즉 NOT RUN 0/270입니다. 파일 열이 비어 있는 이유는 collector가 놓친 것이 아니라 실행 자체가 없었기 때문입니다.

Stage 12와 12b는 enabled evidence를 최종 수집하고 final model을 다시 학습합니다. 여기서 final이라는 이름은 모든 물리축이 계산됐다는 뜻이 아닙니다. 꺼진 stage 10과 11을 채워 주지 않으며, 09f를 true ESW로 바꾸지도 않습니다.

바깥 runner는 STAGE_NN.DONE marker로 resume하고, 24시간 timeout과 다섯 trigger의 skip 감지를 사용합니다. Full tail을 모두 켠 설계치는 cascade당 약 17시간, 한 GPU sequential 약 193일입니다. 실제 v23은 2026년 5월 26일부터 7월 11일까지 46일 동안 273개를 처리했고, 10과 11이 꺼진 realized cost는 cascade당 약 4시간과 정합합니다.

[이해용 확장]
표에 stage 이름이 있다는 이유만으로 실행됐다고 읽으면 안 됩니다. 앞으로 상태표는 ENABLED, NOT RUN, COMPLETE, INVALID를 분리하고, 10과 11은 이름 옆에 항상 NOT RUN · 0/270을 붙입니다.

[예상 질문]
Q. 그러면 conductivity와 W_ad가 어디엔가 조금이라도 있나요?
A. v23에는 없습니다. 더 오래된 radius-only campaign에 7/6개 흔적이 있지만 current 270-slot campaign의 증거로 이식하지 않습니다.

[전환]
이제 실행 완료와 decision product가 왜 다른지 campaign audit으로 넘어가겠습니다.

[Sources]
- 17d9a373:kb/methodology/cascade_pipeline_anatomy_2026_08_13.md
- 17d9a373:tools/doping/tier_cascade.sh

========================================================================================

P9. 활성 workflow는 끝났지만 decision product는 끝나지 않았다

[1:15] 273, 270, 90, 47, 0을 한 화면에서 분리한다

[발표 대본]
왼쪽의 273과 270은 실행 상태이고 오른쪽의 90, 47, 0은 데이터 계보와 승인 상태입니다. 91개 chemistry에 세 directory label을 붙여 273개 job을 계획했고 270개가 활성화된 terminal marker에 도달했습니다. 완료라는 말은 v23에서 실제로 켜 둔 구조 생성, UMA screen, anneal, legacy proxy, mechanics, campaign-local collector가 끝났다는 뜻입니다. canonical DB 등록이나 MD conductivity, W_ad가 끝났다는 뜻은 아닙니다. v23의 MD conductivity와 W_ad 결과는 각각 0/270입니다.

이 270개를 base chemistry로 묶으면 90종입니다. 과거 canonical table은 계산 종료일 전에 47종에서 고정됐고, 빠진 43종은 물리 gate에서 탈락한 것이 아니라 등록 snapshot 밖에 남았습니다. 지금은 90종 raw recovery가 끝났고 G3 phase-set identity는 270/270이고 operational factorial coverage는 17/17 chain rows입니다. 그렇지만 raw recovery, method comparability, effect attribution, ranking approval은 서로 다른 상태입니다. 17/17 chain rows에는 formula-level counterfactual이 있지만 structure/site validation은 0/11이고 G4/G5 계약도 닫히지 않았기 때문에 approved current rank는 0입니다.

[예상 질문]
Q. 90종을 회수했고 G3 방법도 맞췄으면 숫자를 정렬하면 되지 않나요?
A. diagnostic CSV는 만들 수 있습니다. 그러나 B₂O₃처럼 species label 하나가 서로 다른 exact composition을 연결하거나, G4처럼 한 입력이 다른 score를 강제로 덮어쓰면 그 순위는 decision product가 아닙니다.

[Sources]
- db/properties/cascade_audit_campaign_status.csv
- f9adc9d2:db/properties/oxidation_stability_cascade_v3_pinned.json
- kb/methodology/cascade_pipeline_anatomy_2026_08_13.md

========================================================================================

P10. G3 operational contrast는 생겼고 승인 경계는 남아 있다

[1:20] complete라는 단어를 단계별로 쪼갠다

[발표 대본]
이번 장의 핵심은 complete라는 한 단어를 쓰지 않는 것입니다. record-present, method-comparable, operational-contrast-complete, structure-validated, approved는 서로 다릅니다. G3에는 270개 candidate champion record와 각 record에 대응하는 same-run host가 있습니다. phase_set_id는 sorted MP entry IDs의 hash이고 candidate와 host가 동일 ID를 공유하므로 method-comparable은 270/270입니다.

이제 11개 recipe에는 H_plain, H_Cl, D_plain, D_Cl formula profile이 모두 있어 operational 2×2 contrast를 계산할 수 있습니다. baseline recipe contrast H_Cl−H_plain은 반복된 host comparison에서 0 V이고, conditional recipe contrast D_Cl−D_plain은 −0.017에서 +0.283 V까지 분포합니다. 따라서 `Cl effect = 0`도, `Cl-rich는 항상 개선한다`도 성립하지 않습니다. 다만 이 값은 composition-level grand-potential 대비이며 실제 구조·site validation은 0/11입니다.

따라서 화면의 status는 G3 phase identity 270/270, operational factorial coverage 17/17 chain rows, 11 recipe systems, structural validation 0/11, approved rank 0을 동시에 보여 줍니다. G5는 별도 validity 기준에서 86 all-label-valid, 3 partial, 1 dropped이며 legacy usable 89라도 approved는 0입니다. 존재를 valid로, formula contrast를 elemental causality로, legacy usable을 approved로 바꾸지 않는 것이 이 슬라이드의 목적입니다.

[이해용 확장]
phase_set_id는 경쟁상 roster identity를 고정합니다. 전체 method identity는 same-run protocol, method_id, DB version과 함께 고정합니다. composition_id와 paired counterfactual은 formula 대비가 무엇을 의미하는지 고정합니다. 구조·site identity가 없으면 operational recipe contrast는 말할 수 있어도 특정 원소의 구조적 인과는 말할 수 없습니다.

[Sources]
- c0c879ac:db/properties/oxidation_stability_cascade_v3_pinned.json
- c0c879ac:db/properties/oxidation_matched_factorial.json
- c0c879ac:tools/oxidation/esw_matched_factorial.py

========================================================================================

P11. 다섯 게이트는 다섯 개의 비교 계약이다

[1:20] cutoff보다 먼저 identity와 estimand를 고정한다

[발표 대본]
G1부터 G5까지는 같은 종류의 점수를 순서대로 거르는 장치가 아닙니다. G1은 같은 UMA lineage 안의 구조 에너지를 묻습니다. G2는 같은 grand-potential 방법에서 reduction과 oxidation branch를 추출해 window가 붕괴했는지 묻습니다. G3는 same-run phase_set_id를 기록했고, 11개 recipe system에 대해서는 exact formula를 맞춘 2×2 operational contrast까지 만들었습니다. G4는 legacy BVS와 4 Å foreign-center rule을 합친 historical composite라 pool identity와 generator loading·원소별 site-fraction convention이 필요합니다. G5는 탄성값의 물리 validity를 먼저 검사하고 aggregation rule과 roster를 고정해야 합니다.

이번 감사에서 새로 닫힌 계약은 formula-level composition lineage입니다. 같은 dopant label이나 같은 charge_compensation 이름만으로는 부족해서 exact formula와 pinned phase roster를 맞춰 비교했습니다. 다만 exact formula가 같아도 실제 parent structure, substitution site, relaxed geometry가 같다는 뜻은 아닙니다. B₂O₃처럼 dopant label이 같아도 Li₁₇B₂P₄S₁₆Cl₅O₃와 Li₅₈P₈S₄₁Cl₁₆B₂O₃는 다른 candidate이므로, 후자를 전자의 DFT validation으로 이어 붙이면 안 됩니다.

따라서 current chain이 만족해야 하는 조건은 method identity, exact recipe identity, structure·site identity, pool identity, physical validity, approval status입니다. G3의 phase-set 비교와 식 수준 operational contrast는 닫혔지만, 구조·자리 인과성과 G4·G5 계약이 아직 열려 있어 approved rank는 계속 0입니다.

[전환]
다음 장에서 G3가 어디까지 닫혔고 어디서 다시 열리는지 한 장으로 보겠습니다.

[Sources]
- tools/oxidation/esw_cascade_batch.py
- tools/cascade/build_screening_funnel.py
- docs/reviews/cascade_f9adc9d2_codex_review_2026_08_16.md

========================================================================================

P12. G3는 식 수준 대비를 닫았지만 원소 인과를 닫지 않았다

[2:30] 17/17 operational coverage, 11 recipe systems, structural validation 0/11

[발표 대본]
G3의 첫 층은 방법 비교입니다. Candidate와 host를 같은 실행, 같은 chemsys, 같은 pinned MP entry set에서 계산하고 sorted entry IDs의 hash를 phase_set_id로 저장했습니다. Host onset은 84개 phase set에서 모두 2.140 V였고 270/270 candidate-host pair가 method-comparable입니다.

두 번째 층은 effect attribution입니다. Champion 270행 가운데 plain은 253, chain은 17입니다. 그러나 chain 17행은 하나의 S-to-Cl 치환군이 아닙니다. 같은 자리에서 ΔLi=-1, ΔS=-1, ΔCl=+1인 exact transform은 10행이고, B2O3 세 행과 MoO3·WO3 각 두 행은 site와 Li/P 화학량론까지 바뀐 multi-transform 7행입니다. Plain 역시 host 대비 O/S 치환, site, Li charge compensation이 함께 바뀌므로 dopant effect가 아니라 recipe-level host contrast라고 부릅니다.

사후 기술통계는 숨기지 않되 분모를 같이 말합니다. 전체 selected champions에서는 plain 17/253, chain 11/17로 9.63배입니다. Chain 후보가 실제 존재한 33슬롯만 보면 plain 4/16, chain 11/17로 2.59배입니다. 둘 다 combined_score 최대값으로 사후 선택된 연관이고, 농도 라벨도 독립 반복이 아니므로 causal effect가 아닙니다.

Formula-level 2×2는 H_plain Li24P4S20Cl4, H_Cl Li23P4S19Cl5, D_plain과 D_Cl을 11개 chemsys의 pinned roster에서 계산합니다. Undoped baseline recipe contrast H_Cl-H_plain은 0.000 V였지만 독립 표본 11개가 아니라 같은 두 host 조성이 expanded roster에서 반복된 것입니다. Dopant가 있을 때 conditional contrast D_Cl-D_plain은 -0.017에서 +0.283 V까지 달라집니다. 따라서 Cl-rich가 보편적으로 개선한다는 주장은 반증됩니다.

B2O3의 chain composition 2.317 V는 같은 phase set의 host와 비교된 유효한 exact-composition result입니다. NA가 아닙니다. 다만 species-level로 B2O3 dopant가 onset을 올렸다고 귀속할 수 없어서 attribution audit에서 unresolved입니다. Historical G2 생존 43종은 algorithmic pass 25/fail 18이고, 귀속 감사는 supported-pass 24/fail 18/unresolved 1입니다.

이 계산은 exact formula를 PhaseDiagram에 넣은 operational audit입니다. 실제 parent structure와 substitution site를 만든 것이 아니므로 structural realization validated는 0/11입니다. Formula-level round-trip consistency는 독립 물리 검증이 아닙니다.

[예상 질문]
Q. Baseline이 0이면 Cl 효과가 0인가요?
A. 아닙니다. 0은 undoped host에서 한 계단의 recipe contrast이고, doped conditional response는 chemistry마다 다릅니다. 뒤 부록의 ladder는 네 계단에서 host만으로도 +0.216 V 점프가 생김을 보여 줍니다.

[전환]
G3의 operational result는 살리되 current ranking과 보편적 원소 인과는 계속 분리합니다.

[Sources]
- 17d9a373:db/properties/oxidation_stability_cascade_v3_pinned.json
- 17d9a373:db/properties/oxidation_matched_factorial.json
- 17d9a373:kb/methodology/cascade_composition_family_2026_08_16.md

========================================================================================

P13. 역사적 G4 stop은 순환적이고 pool-relative다

[1:35] 역사적 G4 stop은 독립적인 수송 trade-off가 아니다

[발표 대본]
역사적 G4에서 여섯 case가 모두 멈춘다는 관측은 재현되지만, 독립적인 두 수송 신호가 동시에 나빠졌다는 해석은 성립하지 않습니다. 코드에서는 blocking cutoff를 넘으면 legacy BVS 값을 그대로 두지 않고 transport_norm을 0.05로 강제로 낮춥니다. 즉 blocking fail이 composite fail을 자동으로 만듭니다.

이 override를 제거하고 같은 historical 47-species pool에서 legacy BVS branch만 다시 보면 여섯 case 중 다섯 case가 old cutoff를 넘고 한 case만 남습니다. 하지만 이 rescore도 conductivity나 BVSE barrier가 아닙니다. 더구나 BVS branch는 roster 안에서 min–max 정규화하므로 pool이 바뀌면 같은 chemistry의 점수도 움직입니다. historical pool에서 한 case는 0.1000이지만 recovered valid-x005 88종 pool에서는 0.1998입니다. 둘 다 fail이지만 숫자는 고정 물성이 아닙니다.

공개 그림에서 case를 익명화한 이유도 같습니다. 이 슬라이드는 score 정의를 감사하는 자료이지 후보를 추천하는 표가 아닙니다.

[예상 질문]
Q. 그러면 G4를 완전히 버리나요?
A. historical heuristic로는 보존합니다. 다만 current transport 판정에는 forced floor를 제거하고 canonical softBV와 realistic low-x structure, frozen pool_id가 필요합니다.

[Sources]
- db/properties/cascade_seminar_g4_anonymized_round3.csv
- tools/cascade/build_cascade_themes.py
- tools/cascade/build_screening_funnel.py

========================================================================================

P14. old waterfall은 historical audit이다

[1:05] 숫자가 유지돼도 과학적 분류는 바뀔 수 있다

[발표 대본]
이 waterfall은 삭제할 필요가 없습니다. 47종 snapshot에서 어떤 규칙을 어떤 순서로 적용했는지 보여 주는 역사적 감사 자료이기 때문입니다. f9 전후 기계적 count는 47, 47, 43, 25, 11, 1로 같고 최종 WO₃도 plain onset을 사용합니다.

하지만 G3의 25를 species-level clean pass 25라고 부르면 안 됩니다. B₂O₃ chain champion의 2.317 V는 같은 실행·같은 phase set의 host와 비교된 유효한 **exact-composition pass**입니다. 다만 세 concentration label 모두 chain champion이고 plain champion이 없으므로, “B₂O₃라는 도펀트가 onset을 올렸다”는 종 수준 귀속은 unresolved입니다. 따라서 G2 생존 43종의 attribution audit은 supported pass 24, fail 18, species-level attribution unresolved 1로 적습니다. historical algorithm count 25와 B₂O₃ 행 값은 보존하되 claim scope만 분리합니다.

오른쪽 current 상태에는 90종 raw recovery, G3 phase identity 270/270, formula-level operational contrast 11/11, structural·species-level attribution open, approved current chain 없음이라고 적습니다. count가 그대로라는 사실과 claim scope가 그대로라는 사실은 다릅니다.

[Sources]
- db/properties/cascade_screening_funnel.json
- f9adc9d2:db/properties/oxidation_stability_cascade_v3_pinned.json
- docs/reviews/cascade_f9adc9d2_codex_review_2026_08_16.md

========================================================================================

P15. 계면 축은 post hoc다

[1:15] 계면 축은 강하지만 post hoc다

[발표 대본]
계면 축은 core funnel보다 더 큰 분리력을 보입니다. 역사적 47종에서 선택한 100 meV/atom cutoff를 적용하면 SE 쪽 반응 축은 29종, Li metal 쪽 축은 35종을 제외합니다. 하지만 이 값은 0 K pseudo-binary reaction driving force입니다. 실제 계면 원자 구조를 이완한 계산도 아니고, W_ad도 아니며, passivation 성장 속도나 kinetics도 아닙니다. cathode-side coating 문제에 Li-metal axis를 똑같이 적용하는 것도 과도할 수 있습니다.

그래서 이 panel은 계면 질문을 future core contract에 포함해야 한다는 근거로는 쓸 수 있지만, current candidate를 탈락시키는 승인 gate로는 쓰지 않습니다.

[Sources]
- db/properties/cascade_audit_interface_axes.csv
- db/properties/cascade_stability_axes_verdict.json

========================================================================================

P16. recovery는 대조군과 provenance를 늘린다

[1:10] 더 넓은 pool은 더 좋은 인과 질문을 만든다

[발표 대본]
90종 회수의 가장 큰 가치는 ranking보다 대조군과 provenance입니다. 산화물 중심 47종 snapshot에 없던 halide와 sulfide family가 들어오면서 oxide-only 해석을 시험하고 반박할 수 있는 대조군이 생겼고, 이번 f9에서는 champion이 어떤 generator recipe에서 왔는지도 보이기 시작했습니다.

그러나 generator label은 mechanism label이 아닙니다. 253 plain과 17 chain은 selected champion의 provenance이고, plain도 host 대비 여러 원자가 함께 바뀝니다. chain 17행 중 7행은 site와 Li/P 화학량론까지 달라 Cl 하나의 효과를 분리하지 못합니다. 식 수준 matched contrast는 이번에 만들었지만, recovery가 아직 주지 못한 것은 실제 구조·자리에서의 cation mechanism이나 universal Cl benefit입니다. 이제 이 데이터는 matched structure와 site validation을 설계할 좌표로 씁니다.

왼쪽에는 phase identity와 recipe lineage가 control을 늘린다고 적고, 오른쪽에는 causal Cl effect, cation mechanism, winner를 증명하지 않는다고 적습니다. 더 많은 데이터는 더 강한 결론을 자동으로 주지 않습니다. 더 날카로운 반증 실험을 가능하게 합니다.

[Sources]
- f9adc9d2:db/properties/cascade_v23_all.csv
- f9adc9d2:db/properties/oxidation_stability_cascade_v3_pinned.json
- docs/reviews/cascade_f9adc9d2_codex_review_2026_08_16.md

========================================================================================

P17. 공개 가능한 감사와 선택 가능한 결과는 다르다

[1:25] exact-composition operational contrasts are supported; causal shortlist is blocked

[발표 대본]
조건부로 공개할 수 있는 것은 campaign status, G3 phase-set closure, exact-composition operational contrasts, historical G4 deconstruction, post-hoc interface axes, retrospective ML validation입니다. 이 결과들은 각자의 audit scope 안에서 재현 가능한 기록입니다.

반대로 current rank, Pareto, G4 endpoint, winner, conductivity from legacy proxies, universal elemental Cl effect와 explicit pair-property prediction은 blocked입니다. G3 formula audit이 닫혔다고 causal shortlist가 생기지는 않습니다. Operational factorial coverage는 17/17 chain rows이고 11 recipe system에서 계산됐지만 actual structure/site validation은 0/11입니다.

Public deck에는 9.63배와 2.59배를 분모와 non-causal 표시와 함께 보여 줄 수 있습니다. Phase_set_id도 공개 MP entry IDs의 fingerprint라 audit identifier로 공개할 수 있습니다. Candidate identity와 rank는 acquisition-only 영역에 둡니다.

[전환]
이 경계 안에서 ML의 역할도 prediction이 아니라 acquisition으로 제한합니다.

[Sources]
- 17d9a373:db/properties/oxidation_matched_factorial.json
- 17d9a373:docs/reviews/cascade_f9adc9d2_codex_review_2026_08_16.md
- 17d9a373:docs/reviews/cascade_f9adc9d2_webapp_handoff_2026_08_16.md

========================================================================================

P18. ML은 evidence를 schedule한다

[1:20] ML은 새 화학의 물성을 예측하지 못한다

[발표 대본]
rowwise pair LOOCV의 weighted R²는 약 0.089이고 dopant overlap이 남아 있습니다. dopant chemistry를 통째로 빼는 LODO와 L2DO에서는 R²가 음수입니다. 처음 보는 화학의 물성값을 예측하는 모델로 사용할 수 없다는 뜻입니다. 전체 후보 공간에서 좋은 항목을 top group으로 끌어오는 global discovery도 shuffle과 유의하게 구분되지 않습니다.

이미 prelist된 40개 안에서 retrospective ordering만 유의한 신호가 있습니다. 그러나 explicit pair structure와 pair-property label은 0개입니다. 그러므로 모델 출력은 이 pair가 최고다가 아니라 어느 가설부터 계산할지를 정하는 queue로만 씁니다.

[Sources]
- db/properties/cascade_audit_ml_validation.csv
- db/properties/codoping_ml_v2_meta.json

========================================================================================

P19. acquisition은 queue다

[1:10] acquisition은 물성표가 아니라 queue다

[발표 대본]
Acquisition engine을 가장 간단히 말하면 모델 출력이 물성값이 아니라 계산 순서라는 뜻입니다. 먼저 물리적으로 허용된 question space를 만들고 그 안에서 expected utility, uncertainty, diversity, gate boundary를 조합해 다음 계산을 고릅니다. 후보 identity는 명시적 acquisition workspace에서만 보입니다. 공개 발표에서는 A, B, C 같은 익명 queue나 chemistry-family 수준만 보여 줍니다.

실제 pair를 계산하면 그 결과가 새 label이 되고 모델을 갱신합니다. acquisition의 성패는 첫 예측이 정확했는가가 아니라 random보다 적은 계산으로 불확실성을 줄였는가로 평가합니다.

[Sources]
- db/properties/cascade_audit_ml_validation.csv
- docs/reviews/cascade_dftweb_source_of_truth_2026_08_14.md

========================================================================================

P20. 다음 loop는 formula audit 이후의 검증을 배치한다

[1:35] robustness and ladder are first-pass complete; structures and gate repairs come next

[발표 대본]
Matched four-cell formula audit은 완료됐습니다. LiS4를 제외한 다른 pinned phase roster에서의 1차 robustness도 완료됐고, undoped Li/Cl ladder 네 계단도 계산했습니다. 따라서 다음 loop의 첫 단계라고 다시 쓰면 안 됩니다.

새 결과는 conditional contrast 자체가 phase roster에 의존한다는 것입니다. LiS4를 빼면 WO3의 +0.216 V는 0.000 V로 사라지고, Al2O3는 +0.214에서 +0.098 V, MoO3는 +0.216에서 +0.129 V로 줄어듭니다. B2O3의 +0.283 V는 그대로이고 Sc2O3는 -0.017에서 -0.046 V로 이동합니다. 다른 phase set의 절대값을 current gate에 이식하지 않고, contrast와 roster ID를 함께 보존합니다.

이제 우선순위는 actual matched structure와 site를 생성·이완하는 것입니다. 특히 B2O3, MoO3, WO3는 historical plain과 chain이 site·Li·P까지 달랐으므로 formula profile을 구조적 인과로 승격하려면 새 구조가 필요합니다. 그다음 canonical low-x G4와 validity-aware G5를 고치고 explicit pair acquisition으로 넘어갑니다.

[전환]
이 작업을 세 개의 go/no-go contract로 정리하겠습니다.

[Sources]
- 17d9a373:db/properties/oxidation_matched_factorial.json
- 17d9a373:db/properties/oxidation_matched_factorial_nolis4.json
- 17d9a373:kb/methodology/cascade_composition_family_2026_08_16.md

========================================================================================

P21. 세 가지 contract repair가 다음 campaign을 결정한다

[1:30] structure, G4, G5 before ranking

[발표 대본]
첫째 G3는 formula를 더 만드는 단계가 아니라 actual structure와 site를 맞추는 단계입니다. LiS4 include/exclude 결과는 phase-roster sensitivity가 존재함을 이미 보여 줬으므로, 다음에는 matched structures에서 같은 방향이 유지되는지 봅니다. Ladder도 formula phase boundary audit에서 실제 charge-balanced structural series로 옮겨야 합니다.

둘째 G4는 blocking fail이 BVS score를 0.05로 강제하는 override를 제거하고, project canonical softBV parameter, realistic low-x structure, fixed pool_id를 사용해야 합니다. 셋째 G5는 비양의 modulus와 비물리 Poisson ratio를 producer 단계에서 제외하고 aggregation rule을 version으로 고정해야 합니다.

이 세 contract가 닫힌 뒤에만 current rank schema를 freeze하고 explicit pair를 계산합니다. ML은 그 순서를 제안할 수 있지만 물성 claim을 대신하지 않습니다.

[Sources]
- 17d9a373:kb/methodology/cascade_composition_family_2026_08_16.md
- db/properties/cascade_audit_g4_rescore.csv
- db/properties/cascade_audit_gate_completeness.csv

========================================================================================

P22. 결론은 winner가 아니라 다음 증거를 고르는 규칙이다

[1:20] operational decomposition available; universal causality remains open

[발표 대본]
273개의 계획 슬롯 가운데 270개가 활성 workflow를 마쳤고 90종을 회수했습니다. 47종은 역사적 취합 경계이며 current approved rank는 0입니다. Stage 10 conductivity MD와 stage 11 adhesion은 각각 NOT RUN 0/270입니다.

G3 phase-set comparability는 270/270 닫혔고 operational factorial coverage는 chain 17/17, 11 recipe system입니다. Baseline과 conditional recipe contrast를 분리할 수 있지만 actual structure/site validation은 0/11이고 universal elemental causality는 열려 있습니다. Li/Cl ladder와 LiS4 include/exclude는 기전 후보와 phase-roster sensitivity를 보여 주지만 appendix hypothesis를 넘지 않습니다.

따라서 공개 가능한 것은 audit와 exact-composition operational result이고, current ranking·Pareto·endpoint·winner는 NO-GO입니다. 다음 순서는 matched structures, canonical G4, valid G5, explicit pair acquisition입니다. Cascade의 목적은 답을 미리 선언하는 것이 아니라 결론을 가장 크게 바꿀 다음 계산에 비용을 배치하는 것입니다.

[Sources]
- 17d9a373:db/properties/oxidation_matched_factorial.json
- 17d9a373:db/properties/oxidation_matched_factorial_nolis4.json
- 17d9a373:kb/methodology/cascade_pipeline_anatomy_2026_08_13.md

========================================================================================

P23. 전체 도펀트 명단은 91종이다 · 부록

[1:20] 전체 도펀트 명단은 무엇이었나

[발표 대본]
이 부록은 캠페인의 분모를 고정하는 장입니다. 계획한 화합물은 산화물 37, 불화물 10, 염화물 19, 브롬화물 5, 요오드화물 4, 질화물 5, 황화물 11로 합계 91종입니다. 각 종에 세 개의 명목 실행 라벨을 붙여 273개의 슬롯을 만들었습니다. 여기 적힌 명단은 통과 후보도, 좋은 후보도 아닙니다. 처음에 무엇을 계산 대상으로 삼았는지 보여 주는 roster입니다.

활성화된 v23 workflow를 끝까지 완료한 화학종은 90종입니다. As2S3의 세 슬롯만 구조 생성 단계에서 종료됐습니다. 따라서 270 완료라는 숫자는 90종 곱하기 세 라벨의 실행 상태이지, 270개의 독립 농도 실험이라는 뜻이 아닙니다. x002, x005, x010은 모두 4 f.u. cell에서 `n_units=1`로 양자화됐고, 저장된 0.25는 compound formula unit 기준의 generator loading입니다. 원소 at%나 site fraction은 compound 화학식과 치환 site에 따라 따로 계산해야 합니다.

[이해용 확장]
명단을 한 종씩 읽을 필요는 없습니다. 계열별 분모와 As2S3 한 종의 예외만 설명하면 됩니다. 특히 과거 47종 표는 이 명단의 첫 47종, 즉 산화물 37종과 불화물 10종에서 끊겼습니다. 그것이 물리적 생존자가 아니라 등록 시점의 prefix였다는 근거입니다.

[예상 질문]
Q. LiBr 같은 재료는 왜 과거 표에 없었나요?
A. 계획 명단에 있었고 활성 workflow도 완료했습니다. 과거 47종 정본이 산화물과 불화물까지만 등록된 시점에서 굳었기 때문에 표에 없었습니다. 회수되었다는 사실과 승인된 후보라는 판단은 분리합니다.

[전환] 이 273개 슬롯 안에서 실제로 무엇이 실행됐는지 다음 장에서 보겠습니다.

[Sources]
- historical master_batch_273.sh roster, frozen campaign lineage
- db/properties/cascade_audit_campaign_status.csv
- kb/methodology/cascade_pipeline_anatomy_2026_08_13.md

========================================================================================

P24. 실제 cascade의 활성 경로와 미실행 단계 · 부록

[1:25] 실제 cascade는 무엇을 했나

[발표 대본]
이 장은 폴더에 단계 이름이 많다는 사실과 실제 물리 검증 범위를 분리합니다. 활성 경로는 roster에서 구조를 만들고, UMA로 넓게 relax·screen하고, winner를 선택해 anneal한 뒤 legacy BVS와 4 Å 지표, EOS와 탄성 후처리를 만들었습니다. grand-potential 기록은 이 GPU cascade 내부의 09f가 아니라, 이후 MP hull 배치가 별도로 계산했습니다. 마지막으로 campaign-local dataset과 terminal marker가 만들어졌지만 canonical DB registration은 별도 흐름이었습니다.

중요한 제한은 두 가지입니다. 첫째, v23의 MD 전도도와 W_ad는 각각 0/270입니다. 옵션 이름이나 빈 열이 있다고 계산된 것이 아닙니다. 둘째, dft_inputs 폴더는 입력 파일을 만들려 한 흔적이지 270건의 DFT 검증이 끝났다는 증거가 아닙니다. 따라서 이 발표를 MLIP-to-DFT 검증 완료 캠페인이라고 부르지 않습니다.

[이해용 확장]
완료 마커는 활성화된 workflow가 끝났다는 운영 증거입니다. 모든 선택적 물리 모듈이 실행됐다는 의미는 아닙니다. 이 차이를 먼저 이해하면 왜 정적 legacy proxy를 전도도라고 부를 수 없는지도 자연스럽게 이어집니다.

[예상 질문]
Q. 그럼 270 완료라는 표현을 써도 되나요?
A. “활성화된 v23 workflow 기준 270 슬롯 완료”라고 범위를 붙이면 됩니다. MD, W_ad, matched DFT 완료로 넓히면 안 됩니다.

[전환] 다음 두 장은 hull과 grand potential이 무엇을 계산하는지 기초부터 설명합니다.

[Sources]
- historical tier_cascade.sh and master_batch_273.sh
- kb/methodology/cascade_pipeline_anatomy_2026_08_13.md
- docs/reviews/cascade_dftweb_source_of_truth_2026_08_14.md

========================================================================================

P25. Convex hull은 최저에너지 분해 경계다 · 부록

[1:30] Convex hull은 무엇인가

[발표 대본]
점 하나는 특정 조성의 후보상과 그 형성에너지입니다. 같은 전체 조성에서 가능한 모든 상 혼합물 가운데 가장 낮은 에너지를 이은 경계가 convex hull입니다. 아래에서 고무줄을 당겼을 때 닿는 점이라고 생각하면 됩니다. hull 위의 점은 선택한 phase set 안에서 더 낮은 분해 조합이 없고, hull 위쪽 점은 아래의 tie-line에 있는 상 조합으로 분해하면 에너지가 내려갑니다.

수직 거리가 E_above hull입니다. 식은 후보 에너지에서 같은 조성의 hull 에너지를 뺀 값이고 0 이상입니다. 다만 참조가 같아야 합니다. 이번 cascade의 UMA 구조 에너지와 Materials Project DFT hull 에너지를 직접 빼면 기준계가 달라 물리적인 E_above hull이 되지 않습니다. 09e의 hull_E_at_winner_composition도 hull 절대 에너지이지 이 수직 거리가 아닙니다.

[이해용 확장]
tie-line 양 끝은 평형 공존상이고 비율은 lever rule로 구합니다. 두 재료 A와 B 사이 계면 반응은 전체 다성분 공간을 A–B 조성선으로 잘라 pseudo-binary 형태로 읽을 수 있습니다. 이때 반응에너지가 더 음수일수록 열역학적 반응 구동력이 큽니다. 작은 E_above hull이 합성 가능성을 보장하는 보편 문턱은 아닙니다.

[예상 질문]
Q. 25 또는 50 meV/atom 이하면 합성 가능하다고 보면 되나요?
A. 작은 준안정성이라는 경험적 참고는 되지만 보편 법칙은 아닙니다. 온도, 엔트로피, 동역학, DFT 오차와 phase set에 따라 달라집니다.

[전환] 전지처럼 Li를 주고받는 열린계에서는 에너지 대신 grand potential을 씁니다.

[Sources]
- Richards et al., Chemistry of Materials (2016), DOI 10.1021/acs.chemmater.5b04082
- litdb/figures/richards2016_interface_stability_pseudobinary/fig_3.png (inspected)
- tools/doping/convex_hull_ehull.py
- kb/results/b2o3_convex_hull_2026_06_29.md

========================================================================================

P26. Grand potential은 Li 저장고를 열고 phase identity를 요구한다 · 부록

[1:35] 방법 비교는 닫혔지만 composition estimand는 별도다

[발표 대본]
일반 convex hull은 Li 원자 수가 고정된 닫힌계를 생각합니다. 전지에서는 Li를 전극 저장고와 주고받기 때문에 자유에너지 G에서 μLi 곱하기 Li 개수를 뺀 grand potential Φ를 최소화합니다. 전압을 하나 고르고, 그 전압의 μLi에서 가장 낮은 Φ를 갖는 상 조합을 찾고, 전압을 바꿔 반복합니다.

LiS4를 포함한 host-only sensitivity에서는 onset이 2.140 V이고 제외하면 2.256 V로 0.116 V 움직입니다. 이 두 값은 phase roster가 결과를 움직일 수 있다는 외부 sensitivity scenario입니다. 현재 v3 candidate 결과는 candidate와 host를 same-run pinned entry set에서 계산하고 phase_set_id를 기록했기 때문에 270/270 method-comparable입니다. 따라서 예전처럼 phase_set_id가 없어서 current G3 전체를 막지는 않습니다.

그러나 same phase set과 식 수준 2×2 contrast도 구조적 causal attribution을 보장하지 않습니다. operational formula profile은 분리했지만 실제 parent structure, substitution site와 relaxation이 같다는 뜻은 아닙니다. 그래서 하단 caveat는 same phase identity와 formula contrast는 closed, structure·site causality는 open으로 바뀝니다.

[예상 질문]
Q. 그러면 2.140과 2.256 중 어느 값을 current cutoff로 쓰나요?
A. 둘 중 하나를 universal cutoff로 이식하지 않습니다. current candidate는 각 same-run host와의 delta를 쓰고, sensitivity scenario는 phase-roster dependence를 설명하는 부록으로만 남깁니다.

[Sources]
- f9adc9d2:db/properties/oxidation_stability_cascade_v3_pinned.json
- db/properties/esw_lis4excluded.json
- docs/reviews/cascade_f9adc9d2_codex_review_2026_08_16.md

========================================================================================

P27. G1–G5 method contract · 부록

[부록] G3의 method contract와 effect contract를 분리한다

[발표 대본]
표의 핵심은 count보다 계약입니다. G3 v3 implementation은 candidate onset과 same-run host onset의 차이이고 phase_set_id는 270/270에 기록돼 phase-roster comparability가 닫혔습니다. 이어 11개 recipe에서 H_plain, H_Cl, D_plain, D_Cl formula profile을 계산해 operational contrast도 만들었습니다. 그러나 이는 composition-level recipe audit이며 구조·site validation과 보편적 원소 causality는 아직 닫히지 않았습니다.

G4는 historical diagnostic만 가능하며 pool_id, normalization denominator, canonical parameter와 generator-loading·site-fraction convention이 필요합니다. G5는 86 all-label-valid, 3 partial, 1 dropped이고 legacy aggregation으로 89행을 만들 수 있어도 approved rank는 아닙니다. missing, invalid, unresolved attribution, fail을 서로 바꾸지 않는 것이 표의 목적입니다.

[Sources]
- c0c879ac:db/properties/oxidation_stability_cascade_v3_pinned.json
- c0c879ac:db/properties/oxidation_matched_factorial.json
- tools/cascade/build_screening_funnel.py
- c0c879ac review: formula-level operational contrast audit

========================================================================================

P28. Evidence ledger · 부록

[부록] 허용된 claim과 차단된 claim을 한 줄씩 고정한다

[발표 대본]
Supported에는 273, 270, 90, 47의 계보, 141-overlap drift 0, G3 phase-set identity 270/270, 253 plain과 17 chain generator provenance, 17/17 chain-row operational coverage와 11개 recipe system의 formula-level contrast를 둡니다. 9.63배와 2.59배는 post-selection descriptive audit이고, 2×2 contrast는 exact formula recipe의 response입니다. 어느 쪽도 보편적 Cl 효과 크기로 부르지 않습니다.

Blocked에는 current rank, Pareto, endpoint, conductivity inferred from legacy BVS, explicit pair property, universal elemental Cl effect를 둡니다. G3의 missing 항목은 formula counterfactual이 아니라 structure/site validation 0/11이며 LiS4 include/exclude 1차 robustness는 완료입니다. G5는 86 complete, 3 partial, 1 dropped이고 explicit pair label은 0입니다.

다음 순서는 G3 matched structure realization과 robustness 확장, canonical low-x G4, validity-aware G5, explicit pair acquisition입니다. raw value는 지우지 않고 allowed use만 좁힙니다.

[Sources]
- c0c879ac:db/properties/oxidation_stability_cascade_v3_pinned.json
- c0c879ac:db/properties/oxidation_matched_factorial.json

========================================================================================

P29. Artifact status와 access policy · 부록

[부록] public audit와 diagnostic identity를 분리한다

[발표 대본]
이 페이지는 artifact status와 접근 범위를 설명합니다. 정책상 G3 v3 pinned record는 `approval_status=audit_current`, `use_scope=diagnostic_only`로 manifest에 등록해야 합니다. public deck에서는 270/270 method comparability와 composition-family count 같은 익명 요약을 보여 주고 candidate identity나 diagnostic ranking은 별도 acquisition workspace에서만 봅니다. phase_set_id 자체는 감출 값이 아니라 재현성을 위한 provenance입니다.

B₂O₃ sign conflict는 기존의 잘못된 validation join을 바로잡는 correction이므로 public summary로 보여 줄 수 있습니다. 다만 raw legacy `b2o3_esw`는 `approval_status=historical`, `use_scope=archive_only`, `method_status=unverified`로 분리해야 합니다. phase_set_id와 exact host identity가 없으므로 같은 dopant label만으로 두 조성을 연결하지 않습니다.

machine contract에는 one manifest owner, artifact-level source commit, method_id와 pool_id뿐 아니라 현재 원자료에서 유도 가능한 composition_hash, generator_variant, matched_counterfactual_id가 필요합니다. parent_structure_id나 seed처럼 기록되지 않은 값은 빈 provenance 열로 꾸미지 않고 missing으로 명시합니다. public HTML loader도 use_scope를 적용해 기본 결과 화면에 archive ranking이나 diagnostic candidate rows가 들어오지 않게 해야 합니다.

[예상 질문]
Q. 경고 배너나 접힌 details면 충분한가요?
A. 아닙니다. 초기 HTML이나 정적 PPT에 identity가 들어가면 이미 공개된 것입니다. 서버측 opt-in 또는 별도 acquisition artifact가 필요합니다.

[Sources]
- docs/reviews/cascade_f9adc9d2_webapp_handoff_2026_08_16.md
- docs/reviews/cascade_dftweb_source_of_truth_2026_08_14.md

========================================================================================

P30. 11종 formula factorial 표 1/2 · 부록

[2:00] Al, B, Mo, W, Sc, Y

[발표 대본]
이 표는 pinned phase roster 안에서 계산한 식 수준 grand-potential onset입니다. 모든 baseline H_plain과 H_Cl은 2.140 V라 baseline recipe contrast는 0.000 V입니다.

Al2O3는 D_plain 2.140, D_Cl 2.354로 plain contrast 0.000, conditional +0.214, total +0.214 V입니다. B2O3는 D_plain 2.034, D_Cl 2.317로 plain -0.106, conditional +0.283, total +0.177 V입니다. MoO3와 WO3는 각각 D_plain 2.140, D_Cl 2.356으로 conditional과 total이 +0.216 V입니다.

Sc2O3는 D_plain 2.356, D_Cl 2.339라 plain +0.216, conditional -0.017, total +0.199 V입니다. Y2O3는 D_plain과 D_Cl이 모두 2.282라 plain +0.142, conditional 0.000, total +0.142 V입니다.

여기서 같은 숫자가 반복돼도 독립 표본이나 universal mechanism으로 읽지 않습니다. B2O3의 새 same-recipe D_plain 2.034 V와 legacy deep composition 2.03 V는 branch-level consistency를 시사하지만 legacy record에는 phase_set_id와 exact host identity가 없어 독립 검증이 아닙니다.

[Sources]
- 17d9a373:db/properties/oxidation_matched_factorial.json
- 17d9a373:db/properties/b2o3_esw.json

========================================================================================

P31. 11종 formula factorial 표 2/2 · 부록

[1:50] La, Nd, Sm, Mg, Zn

[발표 대본]
La2O3는 D_plain 1.893, D_Cl 1.925 V입니다. Plain recipe contrast는 -0.247, conditional은 +0.032, total은 -0.215 V입니다. Nd2O3는 1.920에서 1.987 V로 plain -0.220, conditional +0.067, total -0.153 V입니다. Sm2O3는 1.989에서 2.034 V로 plain -0.151, conditional +0.045, total -0.106 V입니다.

MgO와 ZnO는 H와 D 네 칸이 모두 2.140 V라 baseline, plain, conditional, total이 모두 0.000 V입니다. 즉 conditional response는 -0.017부터 +0.283 V까지 chemistry-dependent하고, 개선·불변·감소가 모두 존재합니다. 이것이 Cl-rich가 보편적으로 개선한다는 주장을 반증하는 직접적인 이유입니다.

총합 D_Cl-H_plain은 historical chain champion delta와 소수점까지 일치하지만 round-trip consistency입니다. 동일한 계산 원장 안에서 값이 재조립된다는 확인이지 실제 structure나 외부 방법의 독립 validation이 아닙니다.

[Sources]
- 17d9a373:db/properties/oxidation_matched_factorial.json
- 17d9a373:tools/oxidation/esw_matched_factorial.py

========================================================================================

P32. Mechanism hypothesis · appendix only

[2:10] S17→S16 branch boundary and phase-roster dependence

[발표 대본]
이 슬라이드는 결론이 아니라 mechanism hypothesis입니다. Undoped host에서 -Li-S+Cl을 네 번 반복한 ladder0부터 ladder3까지 onset은 2.140 V로 유지되고 Li3PS4 branch를 따릅니다. Ladder4, Li20P4S16Cl8에서 2.356 V로 점프하며 P2S7 branch가 나타납니다. 중요한 정정은 ladder4에도 0.5 LiS4가 남는다는 것입니다. 따라서 LiS4 소멸이 점프 원인이라는 설명은 pure-host ladder가 반증합니다.

전환 지점은 ladder3의 S17에서 ladder4의 S16으로 내려갈 때입니다. Al, Mo, W의 D_plain S17과 D_Cl S16에서도 약 +0.214에서 +0.216 V 점프가 보입니다. 이것은 dopant가 recipe를 common Li-P-S backbone의 branch boundary로 밀었을 가능성을 제시합니다. 그러나 B2O3와 Sc2O3는 같은 pattern을 따르지 않으므로 일반 기전으로 승격하지 않습니다.

또 LiS4를 phase roster에서 제외하면 WO3 conditional +0.216이 0.000으로 사라지고 Al은 +0.098, Mo는 +0.129로 줄어듭니다. B2O3는 +0.283으로 유지되고 Sc는 -0.046으로 이동합니다. Conditional contrast 자체가 phase roster에 의존하므로 숫자를 인용할 때 roster identity를 반드시 붙여야 합니다.

허용되는 문장은 S17-to-S16 전환과 P2S7 branch가 일부 recipe에서 함께 나타난다는 관찰입니다. 금지되는 문장은 Cl이 보편적으로 onset을 올린다, LiS4 소멸이 원인이다, 또는 이 branch가 실제 relaxed structure에서 확인됐다는 주장입니다.

[Sources]
- 17d9a373:db/properties/oxidation_matched_factorial.json
- 17d9a373:db/properties/oxidation_matched_factorial_nolis4.json
- 17d9a373:kb/methodology/cascade_composition_family_2026_08_16.md

========================================================================================

P33. stage 번호와 G1–G5는 다른 체계다 · 부록

[1:40] executable provenance versus decision contracts

[발표 대본]
Stage 번호는 파일이 어떻게 만들어졌는지를 나타내는 실행 순서이고, G1부터 G5는 어떤 질문으로 후보를 판단하는지 나타내는 decision contract입니다. 둘을 일대일로 대응시키면 안 됩니다.

G1의 historical structure-energy input은 주로 stage 06 rerank에서 옵니다. G4의 legacy BVS input은 stage 05이고 blocking은 stage 02 geometry에서 계산된 foreign-center proximity입니다. G5의 elastic input은 stage 08입니다.

반대로 current G2와 G3의 pinned grand-potential 값은 stage 09f가 아닙니다. Pipeline 밖의 esw_cascade_batch.py가 candidate와 host를 same-run pinned MP entry set에서 재계산한 자료입니다. Stage 09a부터 09d는 aggregation, predictor와 DFT input preparation이고, 09e는 decomposition audit입니다. Stage 10과 11은 intended validation tail이지만 v23에서는 0/270 미실행입니다.

그래서 한 row에는 stage provenance와 gate contract를 별도 필드로 기록합니다. Stage complete가 gate pass를 뜻하지 않고, gate pass가 DFT나 MD validation을 뜻하지 않습니다.

[Sources]
- 17d9a373:tools/doping/tier_cascade.sh
- 17d9a373:tools/cascade/build_screening_funnel.py
- 17d9a373:tools/oxidation/esw_cascade_batch.py
- 17d9a373:kb/methodology/cascade_pipeline_anatomy_2026_08_13.md
