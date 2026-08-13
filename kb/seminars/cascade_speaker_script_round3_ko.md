# Cascade round-3 audit research seminar — Korean master script

> 처음 보는 발표자도 이해할 수 있도록 실제 발표보다 길게 쓴 마스터 대본이다.
> 본문은 상단 용어 설명 → 큰 불릿 → 작은 불릿 2개 → 하단 scheme/graph 구조를 따른다.
> 공개 결론: five audit panels conditional GO; current ranking and candidate recommendation NO-GO.

P1. 계산 완료와 승인 완료를 분리한다

[0:55] 무엇을 계산했는가보다 무엇을 승인할 수 있는가

[발표 대본]
안녕하세요. 오늘 발표는 90종 가운데 1등을 고르는 발표가 아닙니다. 먼저 여섯 숫자를 분리하겠습니다. 273은 91개 화학종에 세 개의 명목 라벨을 붙여 만든 실행 슬롯 수이고, 270은 활성화된 v23 workflow가 끝까지 도달한 슬롯 수입니다. 90은 그 270개가 대표하는 완주 화학종 수이고, 47은 계산이 끝나기 전에 별도 등록 흐름에서 고정됐던 역사적 snapshot입니다. 현재 승인된 ranking과 explicit pair-property label은 각각 0입니다. 이 숫자들을 한 줄에 놓는 이유는 계산 완료, 데이터 회수, 방법 비교 가능성, 의사결정 승인을 같은 말로 쓰지 않기 위해서입니다.

이번 동결 감사에서 campaign status, G3 phase-set sensitivity, G4 score deconstruction, post-hoc interface axes, ML validation의 다섯 panel은 제한된 범위에서 설명할 수 있습니다. 하지만 다섯 panel이 90종 ranking을 승인한다는 뜻은 아닙니다. 오늘의 결론은 계산을 많이 했다는 사실보다, 어떤 결과가 어떤 문장을 허용하는지를 분리한 decision contract입니다.

[이해용 확장]
숫자를 만들 수 있다는 것과 과학적 결론을 만들 수 있다는 것은 다릅니다. 예를 들어 90종 onset 표가 있어도 candidate와 host가 같은 competing-phase roster를 사용했다는 식별자가 없으면 작은 전압 차이를 동일 기준 비교로 읽을 수 없습니다. 마찬가지로 89행 ranking CSV가 있어도 score가 순환적이고 pool에 따라 값이 움직이면 current ranking으로 승인할 수 없습니다.

[예상 질문]
Q. 그러면 계산을 많이 해 놓고 결론이 없는 건가요?
A. 아닙니다. 승인된 winner가 없다는 판단 자체가 다음 비용을 어디에 써야 하는지 정해 줍니다. 지금 필요한 것은 더 많은 후보가 아니라 G3, G4, G5의 비교 정의를 고정하는 일입니다.

[전환]
먼저 완료와 승인 사이에 어디서 간격이 생겼는지 보겠습니다.

[Sources]
- db/properties/cascade_audit_manifest.json
- db/properties/cascade_audit_campaign_status.csv
- docs/reviews/cascade_round3_reaudit_cd4e43d0_2026_08_14.md

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

그런데 v23의 실제 구조 생성에서는 세 라벨이 모두 같은 1×1×1, 4 f.u. 셀의 정수 치환으로 들어갔습니다. 그 결과 x002, x005, x010은 각각 2%, 5%, 10% 농도가 아니라 모두 실제 x=0.25로 매핑됩니다. 따라서 세 라벨을 농도 의존성 데이터나 독립 반복 측정으로 해석하면 안 됩니다. 세 개의 작업 슬롯이 있었다는 사실은 맞지만, 세 개의 서로 다른 농도에서 물리가 측정됐다는 뜻은 아닙니다.

이 구분은 뒤의 모든 순위에 영향을 줍니다. 농도 라벨을 실제 농도로 믿으면 blocking 증가나 구조 변화가 농도 응답처럼 보일 수 있고, 세 라벨 평균을 독립 샘플 평균처럼 다룰 수도 있습니다. 현재는 세 라벨을 provenance가 다른 campaign records로만 보존하고, 실제 농도축은 2×2×1 셀로 다시 만든 dual-x 실험에서만 다뤄야 합니다.

[이해용 확장]
청중에게는 91×3=273이라는 산술을 먼저 보여 준 뒤, 곧바로 “세 라벨은 세 농도가 아니었습니다”라고 말하는 것이 좋습니다. 이 한 문장이 뒤 숫자의 과장을 막습니다. chemistry, configuration, property는 273에 다시 곱하는 추가 후보 수가 아니라 의사결정 차원이라는 점도 함께 설명하세요.

[예상 질문]
Q. 세 라벨이 같다면 270 완료라는 숫자도 중복 아닌가요?
A. 실행 기록으로는 270개의 슬롯이 완료된 것이 맞습니다. 다만 독립적인 농도 물리 정보의 개수로 세면 안 됩니다. workload count와 evidence count를 분리해야 합니다.

[전환] 이렇게 많은 작업을 모두 같은 정밀도로 계산할 수 없기 때문에 cascade가 필요합니다.

[Sources]
- tools/doping/master_batch_273.sh
- tools/doping/run_compound_batch.sh
- kb/methodology/cascade_pipeline_anatomy_2026_08_13.md
- db/properties/cascade_audit_campaign_status.csv

========================================================================================

P4. Cascade는 예측기가 아니라 비용 배치 규칙이다 · 1:10

[1:10] Cascade는 예측기가 아니라 비용 배치 규칙이다

[발표 대본]
Cascade의 핵심은 계산량 자체가 아니라 비용을 어디에 배치하느냐입니다. 먼저 문헌과 데이터베이스로 후보를 큐레이션하고, 같은 규약의 MLIP와 저비용 프록시로 넓게 봅니다. 그다음 물리적으로 위험한 경계와 모델 불일치를 찾아 비싼 DFT, 장시간 MD, 실험으로 올립니다. 값싼 모델은 최종 물성값을 대신하지 않고, 정밀 검증의 순서를 정합니다.

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

P5. 활성 workflow는 끝났지만 decision product는 끝나지 않았다

[1:20] 계산 완료와 의사결정 완료를 구분한다

[발표 대본]
왼쪽의 273과 270은 실행 상태이고, 오른쪽의 90과 47과 0은 증거 등록 및 승인 상태입니다. 91개 chemistry에 세 개의 directory label을 붙여 273개 job을 계획했고, 그중 270개가 활성화된 terminal marker에 도달했습니다. 여기서 완료는 v23에서 실제로 켜 둔 단계가 끝났다는 뜻입니다. MD conductivity나 W_ad가 포함됐다는 뜻은 아니며, 두 단계는 v23에서 0/270입니다.

이 270개를 화학종으로 묶으면 90종입니다. 과거 정본 table은 계산 종료일보다 먼저 47종에서 고정됐습니다. 따라서 나머지 43종은 물리 gate에서 탈락한 후보가 아니라 등록 snapshot 밖에 남았던 계산입니다. 지금은 90종을 회수했지만 회수는 파일이 존재한다는 뜻이고, 승인은 같은 방법, 같은 reference, 같은 pool identity로 비교할 수 있다는 뜻입니다. 그 조건이 아직 닫히지 않아 승인 current rank는 0으로 유지합니다.

[예상 질문]
Q. 90종을 회수했으면 바로 다시 정렬하면 되지 않나요?
A. 숫자는 만들 수 있지만 decision product는 아닙니다. G3 phase set, G4 normalization, G5 validity를 먼저 고정해야 합니다.

[Sources]
- db/properties/cascade_audit_campaign_status.csv
- kb/methodology/cascade_pipeline_anatomy_2026_08_13.md

========================================================================================

P6. 완결성은 축마다 다르다

[1:25] complete라는 단어를 축별로 나눈다

[발표 대본]
이번 감사에서 가장 중요한 언어는 complete를 네 단계로 나누는 것입니다. record-present, method-valid, aggregation-usable, approved는 서로 다릅니다. G3에는 산화 onset record가 90종 모두 존재합니다. 하지만 candidate와 host가 같은 competing-phase roster를 사용했다는 shared phase_set_id가 없습니다. 그러므로 record-present는 90이지만 method-comparable은 0입니다.

G5는 탄성 열이 존재하는지만 세면 거의 모두 complete처럼 보입니다. 하지만 비양의 Hill modulus나 비물리 Poisson ratio를 제외하는 validity guard를 적용하면 86종만 세 label이 모두 유효합니다. AlBr3, MgI2, Na2S는 일부 label만 유효하고 AlI3는 usable species aggregate가 없습니다. 기존 aggregation으로 89행을 만들 수 있지만 이것도 승인 ranking과 같지 않습니다.

이 슬라이드의 목적은 missing을 fail로 바꾸지 않는 것, 존재를 valid로 바꾸지 않는 것, valid를 approved로 바꾸지 않는 것입니다. 앞으로 모든 headline에는 무엇을 세는지 이름을 붙입니다.

[예상 질문]
Q. 86과 89 중 어느 것이 분모인가요?
A. 목적에 따라 다릅니다. all-label validity를 묻는 분모는 86이고, 일부 label 평균까지 허용한 legacy species table은 89행입니다. current approval 분모는 아직 0입니다.

[Sources]
- db/properties/cascade_seminar_gate_denominators_round3.csv
- db/properties/cascade_v23_champions_v2.csv
- docs/reviews/cascade_round3_reaudit_cd4e43d0_2026_08_14.md

========================================================================================

P7. 다섯 게이트는 다섯 개의 비교 계약이다

[1:15] 다섯 게이트는 다섯 개의 비교 계약이다

[발표 대본]
G1부터 G5까지는 같은 종류의 점수를 순서대로 거르는 장치가 아닙니다. G1은 같은 UMA lineage 안에서 구조 에너지를 비교하는 질문입니다. G2는 grand-potential window branch identity가 필요합니다. G3는 candidate와 host가 같은 phase set과 같은 database snapshot을 써야 합니다. G4는 legacy BVS와 4 Å foreign-center rule을 합친 historical composite라서 pool identity와 actual concentration convention이 필요합니다. G5는 탄성 값이 물리적으로 유효한지 검사한 뒤 aggregation rule과 roster를 고정해야 합니다.

따라서 cutoff 하나만 기록해서는 gate가 재현되지 않습니다. 최소한 method_id, phase_set_id 또는 pool_id, source commit, 생성 시점, validity, approval status가 값과 함께 움직여야 합니다. 현재 90종 사슬은 이 다섯 계약을 동시에 만족하지 않기 때문에 current rank를 만들지 않습니다.

[전환]
가장 먼저 G3에서 record 수와 비교 가능성이 왜 갈라지는지 보겠습니다.

[Sources]
- tools/cascade/build_screening_funnel.py
- tools/cascade/build_cascade_themes.py
- db/properties/cascade_seminar_gate_denominators_round3.csv

========================================================================================

P8. G3는 90 records이지만 0 comparable이다

[1:25] G3의 90개 기록은 비교 가능한 90개가 아니다

[발표 대본]
G3는 기록 수와 비교 가능성의 차이를 가장 선명하게 보여 줍니다. recovered table에는 90종의 oxidation record가 있습니다. 하지만 각 candidate와 host가 어떤 competing phases를 허용했는지를 함께 식별하는 shared phase_set_id가 행에 남아 있지 않습니다.

LiS4를 포함하는 host-only sensitivity scenario에서는 onset이 2.140 V이고, 이를 제외하면 2.256 V로 0.116 V 움직입니다. 이 차이는 gate threshold에 비해 작지 않습니다. 다만 두 값은 현재 90개 candidate 행의 provenance를 복원한 것이 아닙니다. phase-set 선택이 결과를 얼마나 움직일 수 있는지를 보여 주는 분석 시나리오입니다. 그래서 이 슬라이드에는 90 records present와 0 comparable candidate-host pairs를 동시에 적습니다.

반응식 문자열에 LiS4가 보인다고 해서 전체 entry roster와 database snapshot이 보존됐다는 뜻도 아닙니다. 재계산에서는 candidate와 host를 같은 Materials Project snapshot, 같은 entry set, 같은 phase_set_id로 묶어야 합니다.

[예상 질문]
Q. 2.140과 2.256 중 어느 값을 threshold로 쓰나요?
A. 지금은 둘 중 하나를 universal cutoff로 선택하지 않습니다. same-phase-set 재계산 뒤에만 candidate-host 차이를 말합니다.

[Sources]
- db/properties/cascade_seminar_g3_sensitivity_round3.csv
- db/properties/esw_lis4excluded.json
- docs/reviews/cascade_round3_reaudit_cd4e43d0_2026_08_14.md

========================================================================================

P9. 역사적 G4 stop은 순환적이고 pool-relative다

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

P10. old waterfall은 historical audit이다

[1:00] old waterfall은 규칙 감사 자료다

[발표 대본]
이 waterfall은 삭제할 필요는 없습니다. 47종 snapshot에서 어떤 gate가 중복됐고 어떤 순서에서 count가 줄었는지 보여 주는 역사적 감사 자료이기 때문입니다. 다만 current selection result로 읽으면 안 됩니다. recovered pool에는 당시 없던 family와 다른 missingness가 들어왔고, G3는 method identity가 없으며 G4는 circular composite와 roster-relative normalization을 사용합니다. G5도 validity와 aggregation policy를 다시 고정해야 합니다.

따라서 이 그림이 허용하는 문장은 과거 규칙에서 gate redundancy와 order sensitivity를 관찰했다까지입니다. 현재 endpoint나 winner를 말하는 문장은 허용하지 않습니다.

[Sources]
- db/properties/cascade_screening_funnel.json
- db/properties/cascade_audit_manifest.json

========================================================================================

P11. 계면 축은 post hoc다

[1:15] 계면 축은 강하지만 post hoc다

[발표 대본]
계면 축은 core funnel보다 더 큰 분리력을 보입니다. 역사적 47종에서 선택한 100 meV/atom cutoff를 적용하면 SE 쪽 반응 축은 29종, Li metal 쪽 축은 35종을 제외합니다. 하지만 이 값은 0 K pseudo-binary reaction driving force입니다. 실제 계면 원자 구조를 이완한 계산도 아니고, W_ad도 아니며, passivation 성장 속도나 kinetics도 아닙니다. cathode-side coating 문제에 Li-metal axis를 똑같이 적용하는 것도 과도할 수 있습니다.

그래서 이 panel은 계면 질문을 future core contract에 포함해야 한다는 근거로는 쓸 수 있지만, current candidate를 탈락시키는 승인 gate로는 쓰지 않습니다.

[Sources]
- db/properties/cascade_audit_interface_axes.csv
- db/properties/cascade_stability_axes_verdict.json

========================================================================================

P12. recovery는 대조군을 늘린다

[1:10] recovery의 가치는 순위보다 대조군이다

[발표 대본]
90종 회수의 과학적 가치는 ranking보다 대조군에 있습니다. 산화물 중심 historical snapshot에 없던 halide와 sulfide family가 들어오면서 oxide-only로 설명했던 패턴을 다른 가설과 비교할 수 있게 됐습니다. 이 대조군은 특정 family만의 효과라는 해석을 약화시킵니다.

하지만 이것만으로 특정 cation이 원인이라고 확정하거나 Cl을 더하면 보편적으로 좋아진다고 말할 수는 없습니다. concentration, site occupancy, Li count, phase set이 함께 달라질 수 있기 때문입니다. 그래서 공개 슬라이드에는 candidate rank가 아니라 family-level control의 역할만 보여 줍니다. 넓어진 pool은 더 강한 결론을 자동으로 주는 것이 아니라 더 좋은 반증 실험을 설계하게 해 줍니다.

[Sources]
- db/properties/oxidation_stability_cascade_v2.json
- kb/methodology/cascade_pipeline_anatomy_2026_08_13.md

========================================================================================

P13. 다섯 audit panel만 conditional GO다

[1:15] 다섯 panel은 조건부 GO, leaderboard는 NO-GO

[발표 대본]
이번 round-3의 공개 경계를 한 번에 정리합니다. 조건부로 보여 줄 수 있는 것은 campaign completion, G3 host sensitivity, G4 historical deconstruction, post-hoc interface-axis audit, ML validation의 다섯 panel입니다. frozen source와 companion CSV가 있고 현재 fingerprint가 맞습니다.

반면 current leaderboard, Pareto set, G4 endpoint, winner, explicit pair-property prediction은 모두 blocked입니다. 화면 중앙의 approved current rank는 0입니다. 여기서 조건부 GO는 audit 결과를 그 범위 안에서 설명할 수 있다는 뜻이지, 이 데이터로 후보를 추천해도 된다는 뜻이 아닙니다. manifest와 API의 full machine contract도 아직 닫히지 않았으므로 fingerprint를 approval과 혼동하지 않습니다.

[예상 질문]
Q. 후보 이름은 왜 안 보여 주나요?
A. 이름은 다음 계산 순서를 정하는 acquisition workspace에서는 필요합니다. 공개 deck에 넣는 순간 diagnostic score가 추천으로 읽히기 때문에 채널을 분리합니다.

[Sources]
- db/properties/cascade_audit_manifest.json
- docs/reviews/cascade_round3_reaudit_cd4e43d0_2026_08_14.md

========================================================================================

P14. ML은 evidence를 schedule한다

[1:20] ML은 새 화학의 물성을 예측하지 못한다

[발표 대본]
pair LOOCV의 R²는 약 0.089이고 dopant chemistry를 통째로 빼는 LODO와 L2DO에서는 R²가 음수입니다. 처음 보는 화학의 물성값을 예측하는 모델로 사용할 수 없다는 뜻입니다. 전체 후보 공간에서 좋은 항목을 top group으로 끌어오는 global discovery도 shuffle과 유의하게 구분되지 않습니다.

이미 prelist된 40개 안에서 retrospective ordering만 유의한 신호가 있습니다. 그러나 explicit pair structure와 pair-property label은 0개입니다. 그러므로 모델 출력은 이 pair가 최고다가 아니라 어느 가설부터 계산할지를 정하는 queue로만 씁니다.

[Sources]
- db/properties/cascade_audit_ml_validation.csv
- db/properties/codoping_ml_v2_meta.json

========================================================================================

P15. acquisition은 queue다

[1:10] acquisition은 물성표가 아니라 queue다

[발표 대본]
Acquisition engine을 가장 간단히 말하면 모델 출력이 물성값이 아니라 계산 순서라는 뜻입니다. 먼저 물리적으로 허용된 question space를 만들고 그 안에서 expected utility, uncertainty, diversity, gate boundary를 조합해 다음 계산을 고릅니다. 후보 identity는 명시적 acquisition workspace에서만 보입니다. 공개 발표에서는 A, B, C 같은 익명 queue나 chemistry-family 수준만 보여 줍니다.

실제 pair를 계산하면 그 결과가 새 label이 되고 모델을 갱신합니다. acquisition의 성패는 첫 예측이 정확했는가가 아니라 random보다 적은 계산으로 불확실성을 줄였는가로 평가합니다.

[Sources]
- db/properties/cascade_audit_ml_validation.csv
- docs/reviews/cascade_dftweb_source_of_truth_2026_08_14.md

========================================================================================

P16. pair ranking보다 validation이 먼저다

[1:15] pair ranking 전에 target definition을 고정한다

[발표 대본]
다음 loop는 pair ranking으로 바로 넘어가지 않습니다. 먼저 비교 정의를 freeze합니다. G3는 same-snapshot phase_set_id, G4는 canonical softBV convention과 actual low-x structure, G5는 elastic validity와 aggregation rule을 고정합니다. 그다음 결측과 invalid label을 provenance와 함께 회수하고 cutoff 주변이나 지표가 불일치하는 boundary case를 계산합니다. 이 단계가 끝난 뒤에야 explicit co-substituted structures를 만들고 pair acquisition을 시작합니다.

target definition이 흔들리는 상태에서 pair label을 많이 만들면 모델은 물리가 아니라 파이프라인 artifact를 학습합니다. 그래서 계산량보다 순서가 중요합니다.

[Sources]
- docs/reviews/cascade_round3_reaudit_cd4e43d0_2026_08_14.md
- docs/reviews/cascade_dftweb_source_of_truth_2026_08_14.md

========================================================================================

P17. 세 contract repair가 go/no-go를 정한다

[1:15] 세 가지 contract repair가 go/no-go를 정한다

[발표 대본]
첫째 G3에서 candidate와 host를 같은 database snapshot과 같은 competing-phase roster로 다시 계산해 phase-set sensitivity가 실제 순서를 바꾸는지 봅니다. 둘째 G4에서 blocking fail이 BVS score를 강제로 낮추는 override를 제거하고 canonical softBV parameter와 realistic low-x structure를 사용하며 pool_id를 고정합니다. 셋째 G5에서 비물리 탄성 행을 producer 단계에서 제외하고 aggregation rule을 버전으로 남깁니다.

세 결과가 안정적일 때만 current rank schema를 freeze합니다. 그 다음 explicit pair를 만들어 ML acquisition이 random보다 계산 순서를 개선하는지 prospective하게 확인합니다.

[Sources]
- db/properties/cascade_seminar_gate_denominators_round3.csv
- docs/reviews/cascade_round3_reaudit_cd4e43d0_2026_08_14.md

========================================================================================

P18. 결론은 decision contract다

[0:55] 결론은 승자가 아니라 decision contract다

[발표 대본]
오늘 얻은 결과는 winner가 아니라 decision contract입니다. 273개 실행 슬롯 중 270개가 활성 workflow를 마쳤고, 90종의 흔적을 회수했으며, 47종 snapshot이 왜 굳었는지 설명할 수 있습니다. 다섯 audit panel은 조건부 GO지만 current rank, Pareto, endpoint와 후보 추천은 NO-GO입니다.

따라서 다음 순서는 contract freeze, matched label 회수, boundary test, explicit pair acquisition입니다. ML은 그 순서를 제안하고 같은 규약의 DFT, MD, interface calculation, experiment가 최종 주장을 결정합니다. 이것이 계산량을 늘리는 것보다 먼저 해야 할 일입니다.

[Sources]
- db/properties/cascade_audit_manifest.json
- docs/reviews/cascade_round3_reaudit_cd4e43d0_2026_08_14.md

========================================================================================

P19. 전체 도펀트 명단은 91종이다 · 부록

[1:20] 전체 도펀트 명단은 무엇이었나

[발표 대본]
이 부록은 캠페인의 분모를 고정하는 장입니다. 계획한 화합물은 산화물 37, 불화물 10, 염화물 19, 브롬화물 5, 요오드화물 4, 질화물 5, 황화물 11로 합계 91종입니다. 각 종에 세 개의 명목 실행 라벨을 붙여 273개의 슬롯을 만들었습니다. 여기 적힌 명단은 통과 후보도, 좋은 후보도 아닙니다. 처음에 무엇을 계산 대상으로 삼았는지 보여 주는 roster입니다.

활성화된 v23 workflow를 끝까지 완료한 화학종은 90종입니다. As2S3의 세 슬롯만 구조 생성 단계에서 종료됐습니다. 따라서 270 완료라는 숫자는 90종 곱하기 세 라벨의 실행 상태이지, 270개의 독립 농도 실험이라는 뜻이 아닙니다. x002, x005, x010은 모두 4 f.u. 셀의 정수 치환 때문에 실제 x=0.25로 구현됐습니다.

[이해용 확장]
명단을 한 종씩 읽을 필요는 없습니다. 계열별 분모와 As2S3 한 종의 예외만 설명하면 됩니다. 특히 과거 47종 표는 이 명단의 첫 47종, 즉 산화물 37종과 불화물 10종에서 끊겼습니다. 그것이 물리적 생존자가 아니라 등록 시점의 prefix였다는 근거입니다.

[예상 질문]
Q. LiBr 같은 재료는 왜 과거 표에 없었나요?
A. 계획 명단에 있었고 활성 workflow도 완료했습니다. 과거 47종 정본이 산화물과 불화물까지만 등록된 시점에서 굳었기 때문에 표에 없었습니다. 회수되었다는 사실과 승인된 후보라는 판단은 분리합니다.

[전환] 이 273개 슬롯 안에서 실제로 무엇이 실행됐는지 다음 장에서 보겠습니다.

[Sources]
- historical master_batch_273.sh roster, frozen campaign lineage
- db/properties/cascade_audit_manifest.json
- kb/methodology/cascade_pipeline_anatomy_2026_08_13.md

========================================================================================

P20. 실제 cascade의 활성 경로와 미실행 단계 · 부록

[1:25] 실제 cascade는 무엇을 했나

[발표 대본]
이 장은 폴더에 단계 이름이 많다는 사실과 실제 물리 검증 범위를 분리합니다. 활성 경로는 roster에서 구조를 만들고, UMA로 넓게 relax·screen하고, winner를 선택해 anneal한 뒤 legacy BVS와 4 Å 지표, EOS와 탄성 후처리를 만들었습니다. grand-potential 기록은 이 GPU cascade 내부의 09f가 아니라, 이후 MP hull 배치가 별도로 계산했습니다. 마지막으로 dataset과 등록 상태가 만들어졌습니다.

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

P21. Convex hull은 최저에너지 분해 경계다 · 부록

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
- kb/concepts/convex-hull-related local records

========================================================================================

P22. Grand potential은 Li 저장고를 연다 · 부록

[1:30] Grand potential phase diagram은 무엇인가

[발표 대본]
일반 convex hull은 Li 원자 수가 고정된 닫힌계를 생각합니다. 전지에서는 Li를 전극 저장고와 주고받기 때문에 Li 개수 대신 화학퍼텐셜 μLi를 조건으로 둡니다. 그래서 자유에너지 G에서 μLi 곱하기 Li 개수를 뺀 grand potential Φ를 최소화합니다. 전압을 하나 고르고, 그 전압의 μLi에서 가장 낮은 Φ를 갖는 상 조합을 찾고, 전압을 바꿔 반복합니다.

평형 상 조합이 처음 바뀌는 전압이 분해 onset과 연결됩니다. 하지만 이 값은 허용한 competing phase 목록에 의존합니다. LPSCl host에서 LiS4를 포함하면 2.140 V, 제외하면 2.256 V로 0.116 V 이동합니다. 그러므로 후보 2.20 V를 host보다 개선이라고 부르려면 후보와 host를 같은 phase_set_id 안에서 계산해야 합니다.

[이해용 확장]
이 계산은 0 K 열역학입니다. 어떤 분해산물이 가능한지와 구동력은 말하지만, 실제 계면층이 전자를 막아 자기제한되는지, 얼마나 빨리 자라는지, 접착에너지 W_ad가 어떤지는 말하지 않습니다. thermodynamic window와 practical operating window를 분리해야 합니다.

[예상 질문]
Q. 그러면 2.14 V와 2.256 V 중 어느 값이 맞나요?
A. 둘 다 각 phase set 안에서는 계산 결과입니다. 현재 문제는 어느 목록을 정본으로 고정했는지와 후보·host가 같은 목록을 썼는지 태그가 빠졌다는 점입니다. 먼저 phase set을 freeze해야 합니다.

[전환] 다음 장에서 이 원칙을 G1–G5의 실제 정의에 연결합니다.

[Sources]
- Zhu et al., ACS Applied Materials & Interfaces (2015), DOI 10.1021/acsami.5b07517
- litdb/figures/zhu2015_esw_grand_potential_origin/fig_1.png and fig_2.png (inspected)
- db/properties/esw_lis4excluded.json

========================================================================================

P23. G1–G5 method contract

[부록] G1–G5 method contract

[발표 대본]
표의 핵심은 count보다 계약입니다. G3는 90개 record가 있지만 method-complete comparison은 0입니다. G4는 historical diagnostic만 가능하고 pool_id, normalization denominator, actual-x convention이 필요합니다. G5는 86 all-label-valid, 3 partial, 1 dropped이며 legacy aggregation으로 89행을 만들 수 있어도 approved rank는 아닙니다. missing, invalid, fail을 서로 바꾸지 않는 것이 이 표의 목적입니다.

[Sources]
- db/properties/cascade_seminar_gate_denominators_round3.csv
- tools/cascade/build_screening_funnel.py

========================================================================================

P24. Evidence ledger

[부록] Evidence ledger

[발표 대본]
Allowed에는 273, 270, 90, 47의 계보와 다섯 audit panel의 제한된 결론만 둡니다. Blocked에는 current rank, Pareto, endpoint, conductivity inferred from legacy BVS, pair-property prediction, single winner를 둡니다. G3는 method-complete 0이고 G5는 86 complete, 3 partial, 1 dropped입니다. candidate names는 기본 public result artifact가 아니라 acquisition-only artifact입니다.

[Sources]
- db/properties/cascade_audit_manifest.json
- db/properties/cascade_seminar_gate_denominators_round3.csv

========================================================================================

P25. Artifact status와 access policy

[부록] Artifact status와 access policy

[발표 대본]
이 페이지는 artifact status와 접근 범위를 설명합니다. historical은 당시 기록으로 유효하지만 current selection에는 쓰지 않고, superseded는 더 새 세대가 있어 selection에서 폐기됐다는 뜻입니다. recovered-unvalidated는 파일을 회수했지만 method contract가 닫히지 않았다는 뜻이고 approved만 current decision을 구동할 수 있습니다.

Public deck에는 audit와 status만 둡니다. diagnostic candidate identity는 명시적인 acquisition-only 접근 뒤에 둡니다. approved 결과 화면에는 approved artifact만 들어갑니다. 지금은 다섯 audit panel만 conditional GO이고 current ranking은 NO-GO입니다. machine contract 측면에서도 one manifest owner, artifact-level method_id와 pool_id와 source commit, unknown phase_set_id의 fail-closed 처리가 남아 있습니다.

[예상 질문]
Q. details를 접어 두는 것만으로 opt-in인가요?
A. 아닙니다. 초기 HTML이나 정적 PPT에 이름이 포함되면 scraper와 검색에는 이미 노출됩니다. 서버측 opt-in 또는 별도 acquisition artifact가 필요합니다.

[Sources]
- docs/reviews/cascade_round3_reaudit_cd4e43d0_2026_08_14.md
- docs/reviews/cascade_dftweb_source_of_truth_2026_08_14.md
