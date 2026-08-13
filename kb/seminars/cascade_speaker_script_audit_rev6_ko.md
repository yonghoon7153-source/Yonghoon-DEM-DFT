# Cascade audit-first research seminar — Korean master script

> 이 문서는 발표자가 내용을 처음부터 이해하고 스스로 줄일 수 있도록 실제 발표보다 의도적으로 길게 쓴 마스터 대본이다.
> 본문 슬라이드는 2026-06-15 연구세미나의 구조(상단 용어 정의 → 큰 주제 불릿 → 작은 불릿 → 하단 시각 근거)를 따른다.

권장 본문 길이: 22–25분. 아래 대본은 이해와 편집을 위해 실제 발표보다 의도적으로 길게 작성했다.
각 슬라이드의 첫 두 문단을 기본 발표로 사용하고, '이해용 확장'과 '예상 질문'은 필요에 따라 줄인다.

P1. 273개의 실행이 실제로 가르쳐 준 것 · 0:55

[0:55] 273개의 실행이 실제로 가르쳐 준 것

[발표 대본]
안녕하세요. 오늘은 LPSCl 개질의 MLIP 중심 스크리닝과 고비용 검증 사이의 handoff를 감사한 cascade를 말씀드리겠습니다. 다만 시작부터 결론을 분명히 하겠습니다. 이번 발표의 결과는 90종 가운데 1등을 고른 표가 아닙니다. 91개 화합물에 세 개의 명목 라벨을 붙여 273개의 실행 슬롯을 만들었고, 그중 활성화된 v23 workflow 기준 270개가 완료됐습니다. 이 완료에는 MD 전도도나 W_ad가 포함되지 않으며, 두 값은 v23에서 0/270입니다. 이후 원자료를 다시 모아 90종의 계산 흔적을 회수했지만, 현재 승인된 90종 leaderboard와 Pareto set, 수송 순위는 모두 0개입니다. 계산을 못 했다는 뜻이 아니라, 계산 결과가 같은 정의와 같은 provenance를 만족해야 순위라는 제품이 된다는 뜻입니다.

처음 이 프로젝트를 설명할 때는 값싼 모델이 넓게 보고, 물리 게이트가 후보를 줄이고, 비싼 DFT가 최종 후보를 확인한다고 말했습니다. 그 구조 자체는 여전히 맞습니다. 하지만 감사를 거치면서 더 중요한 질문이 생겼습니다. 각 게이트가 실제로 무엇을 재는지, 후보와 host를 같은 phase set에서 비교했는지, blocking이 독립 수송 정보인지, roster가 바뀌었을 때 정규화 값이 그대로 비교 가능한지 확인해야 했습니다. 이 질문을 통과하지 못한 숫자는 보기 좋은 순위가 되더라도 과학적 결론으로는 사용할 수 없습니다.

오늘의 중심 문장은 하나입니다. ML과 저비용 모델은 다음 비싼 계산의 순서를 정할 수 있지만, 주장 자체는 동일 규약의 DFT·MD·실험이 결정합니다. 따라서 이번 발표는 후보 추천 발표가 아니라, 어떤 증거가 다음 의사결정을 허용하는지 정리하는 발표입니다.

[이해용 확장]
발표를 짧게 해야 한다면 첫 문단과 마지막 문장만 말해도 됩니다. 교수님이나 대학원생이 숫자의 계보를 물으면 273은 실행 슬롯, 270은 완료 슬롯, 90은 회수된 고유 화학종, 47은 과거 정본 snapshot, 0은 현재 승인된 leaderboard와 Pareto/transport 결과라고 답하면 됩니다. 이 여섯 숫자를 섞지 않는 것이 오늘 발표 전체의 안전장치입니다.

[예상 질문]
Q. 그러면 계산을 많이 해 놓고 아무 결론도 없는 것 아닌가요?
A. 아닙니다. 승인 순위가 없다는 판정 자체가 다음 계산을 낭비하지 않게 합니다. 어떤 정의가 불안정한지, 어떤 태그가 빠졌는지, 어느 축을 먼저 다시 계산해야 하는지가 구체적으로 남았습니다.

[전환] 먼저 왜 이 문제를 한 개의 점수로 줄일 수 없는지부터 보겠습니다.

[Sources]
- db/properties/cascade_audit_manifest.json
- docs/reviews/cascade_dftweb_source_of_truth_2026_08_14.md
- kb/methodology/cascade_pipeline_anatomy_2026_08_13.md

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

P5. 계산은 끝났지만 승인된 의사결정 사슬은 끝나지 않았다 · 1:25

[1:25] 계산은 끝났지만 승인된 의사결정 사슬은 끝나지 않았다

[발표 대본]
왼쪽은 실행 상태입니다. 273개 슬롯 가운데 270개가 완료됐고, As2S3의 세 라벨만 구조 생성 단계에서 종료됐습니다. 오른쪽은 evidence registration 상태입니다. 완료된 고유 화학종은 90종인데, 역사적으로 정본에 들어간 snapshot은 47종이었습니다. 그리고 현재 승인된 90종 leaderboard는 0개입니다.

왜 47에서 멈췄는지 코드와 파일 시간까지 추적했습니다. 6월 25~29일에 당시 완료된 47종, 즉 산화물 37종과 불화물 10종이 별도 branch의 cascade_v23_all.csv로 등록됐습니다. 실제 계산은 7월 11일에 90종까지 끝났지만, 그 브랜치와 등록 파일은 다시 갱신되지 않았습니다. 따라서 빠진 43종은 물리 게이트에서 탈락한 것이 아니라 정본 취합 경계 밖에 남아 있었습니다.

회수 자체는 성공했습니다. 270개의 champion에 대해 grand-potential 결과를 다시 만들었고, 과거 141개와 겹치는 항목은 oxidation onset drift가 0이었습니다. 하지만 recovery는 approval이 아닙니다. 기존 산문과 gate metadata가 47종 규약을 상속했고, roster-relative 정규화가 바뀌며, 일부 핵심 태그와 축이 비어 있습니다. 그래서 화면과 발표 모두 “90 recovered”와 “90 ranked”를 구분해야 합니다.

[이해용 확장]
이 슬라이드에서는 “43종을 새로 발견했다”라고 말하지 마세요. 계산은 이미 있었고 회수한 것입니다. 또한 47종 결과가 틀렸다고 말하기보다, 47종 snapshot 안에서는 계산된 절대 필드가 유효하지만 범위 주장과 roster-relative 순위는 현재 풀로 확장할 수 없다고 설명하세요.

[예상 질문]
Q. 회수한 90종으로 바로 표를 다시 만들면 되지 않나요?
A. 숫자 표는 만들 수 있습니다. 그러나 phase-set 태그, branch comparability, exact gate inputs와 roster-relative normalization을 다시 검증하지 않으면 그 표는 계산 산출물이지 승인된 decision product가 아닙니다.

[전환] 그렇다면 90종 회수본이 실제로 어느 축까지 완전한지 분리해 보겠습니다.

[Sources]
- db/properties/cascade_audit_campaign_status.csv
- docs/figures/cascade/cascade_audit_campaign_status.png
- kb/methodology/cascade_pipeline_anatomy_2026_08_13.md
- db/properties/cascade_audit_manifest.json

========================================================================================

P6. 90종 회수본은 89행 파생표이지만 현재 순위표는 아니다 · 1:25

[1:25] 90종 회수본은 89행 파생표이지만 현재 순위표는 아니다

[발표 대본]
회수된 화학종은 90종이고, 현재 파생 ranked table에는 89종이 들어갑니다. AlI3는 세 라벨 모두에서 post-anneal ΔE, E/Pugh, legacy BVS 등 gate 입력이 비어 있어 파생표에서 완전히 빠집니다. MgI2는 G1/G5의 all-label 입력이 불완전하고, G4가 고정해 쓰는 x005 legacy-BVS 입력도 없습니다. 두 종 모두 G4에서 fail이 아니라 missing입니다. 이 두 종은 단순히 0점으로 두면 안 되고 missing으로 유지해야 합니다.

여기서 71 complete, 18 partial, 1 dropped라는 예전 완결성 숫자를 headline으로 쓰지 않는 이유가 있습니다. 그 감사기는 실제 게이트에 쓰지 않는 EOS B0를 필수 열로 세면서, 반대로 G5에 쓰는 Pugh ratio는 검사하지 않았습니다. 따라서 그것은 선택된 다섯 열의 완결성이지 gate completeness가 아닙니다. 축별로 다시 보면 G1/G5 all-label 입력이 완전한 종은 88종이고 MgI2는 partial, AlI3는 absent입니다. G4의 x005 입력도 88종이 존재하고 MgI2와 AlI3가 빠집니다.

G2와 G3는 90종 레코드가 있지만, 현재 CSV에는 후보와 host를 같은 분해상 집합으로 비교했는지 확인할 phase_set과 branch comparability 태그가 보존되지 않았습니다. 행 수가 90이라고 비교 가능성이 90이라는 뜻이 아닙니다. 따라서 현재 승인 순위는 0으로 유지합니다.

[이해용 확장]
이 슬라이드는 missingness를 가장 정확히 설명하는 장입니다. “부분 결측 18종”이라는 표현을 그대로 쓰지 말고, 어떤 축에 필요한 열이 비었는지 말하세요. B0만 비어 있는 종을 전체 funnel partial이라고 부르면 실제보다 훨씬 심각하게 보이거나 반대로 중요한 Pugh 결측을 놓칠 수 있습니다.

[예상 질문]
Q. 89종 파생표는 왜 다운로드할 수 있나요?
A. 감사와 재현을 위해 파생 산출물로 공개할 수 있습니다. 다만 상태를 recovered/derived로 표시하고 current leaderboard로 노출하지 않습니다. 다운로드 가능성과 승인 상태는 별개입니다.

[전환] 다음부터는 각 게이트가 요구하는 방법 계약을 하나씩 열어 보겠습니다.

[Sources]
- db/properties/cascade_audit_gate_completeness.csv
- db/properties/cascade_pool_audit_v2.json
- db/properties/cascade_v23_ranked_v2.csv
- docs/reviews/cascade_dftweb_source_of_truth_2026_08_14.md

========================================================================================

P7. 다섯 게이트는 다섯 개의 다른 방법 계약이다 · 1:15

[1:15] 다섯 게이트는 다섯 개의 다른 방법 계약이다

[발표 대본]
역사적 G1부터 G5까지는 이름만 다른 점수가 아니라 서로 다른 질문입니다. G1은 같은 UMA 계보 안에서 host보다 구조 에너지가 낮은지 묻습니다. G2는 전기화학 window가 무너지는지 묻고, G3는 산화 onset을 host와 비교합니다. G4는 legacy BVS와 4 Å blocking을 합친 정적 pathway heuristic입니다. G5는 E와 Pugh를 roster median으로 나누는 상대 ranking입니다.

중요한 것은 각 질문마다 비교 계약이 다르다는 점입니다. G3에서는 후보와 host가 같은 competing-phase set을 써야 합니다. G4의 cascade BVS 파라미터는 현재 프로젝트의 canonical softBV 규약과 다릅니다. G5는 roster가 47에서 90으로 바뀌면 median이 바뀌므로 과거 점수와 직접 비교할 수 없습니다. 따라서 같은 CSV에 열이 존재한다는 이유만으로 다섯 게이트를 직렬로 연결하면 안 됩니다.

현재 90종 회수본은 각 축의 원자료를 상당 부분 가지고 있지만, 이 다섯 계약을 모두 만족하는 frozen schema가 없습니다. 그래서 다음 계산보다 먼저 해야 할 일은 gate schema를 다시 고정하고, 필드마다 protocol tag와 status를 같이 이동시키는 것입니다.

[이해용 확장]
청중에게는 “게이트는 컷오프가 아니라 질문+방법+참조계의 묶음”이라고 설명하면 됩니다. 같은 2.14 V 숫자도 phase set이 다르면 같은 문턱이 아닐 수 있고, 같은 transport_norm도 roster나 파라미터가 바뀌면 같은 척도가 아닙니다.

[예상 질문]
Q. 그러면 기존 G1–G5를 전부 버려야 하나요?
A. 역사적 47종 audit로는 보존할 가치가 있습니다. 다만 90종 current gate로 승계하려면 각 계약을 다시 명시하고 재계산해야 합니다.

[전환] 가장 먼저 결론을 흔드는 것은 G3의 phase-set 의존성입니다.

[Sources]
- db/properties/cascade_screening_funnel.json
- tools/cascade/build_screening_funnel.py
- tools/doping/bvse_proxy.py
- AGENTS.md canonical BVSE convention

========================================================================================

P8. G3 문턱은 competing phase set에 따라 0.116 V 움직인다 · 1:20

[1:20] G3 문턱은 competing phase set에 따라 0.116 V 움직인다

[발표 대본]
같은 LPSCl host의 산화 onset도 어떤 경쟁상을 허용하느냐에 따라 달라집니다. LiS4를 competing phase set에 포함하면 host onset은 2.140 V이고, LiS4를 제외한 별도 계산에서는 2.256 V입니다. 차이는 0.116 V입니다. 후보의 산화 onset이 2.20 V라면 한 phase set에서는 host보다 개선된 것처럼 보이고, 다른 phase set에서는 개선되지 않은 것으로 판정됩니다.

따라서 G3는 보편적인 2.14 V 문턱을 모든 레코드에 적용하는 문제가 아닙니다. 후보와 host가 동일한 phase_set_id, 동일한 reference와 correction 규약 안에 있어야 차이를 비교할 수 있습니다. 현재 회수 JSON에는 분해 반응식이 풍부하게 남아 있지만, v2 CSV와 일부 빌더는 이 비교 태그를 충분히 전달하지 않습니다.

회수된 270 onset 반응 가운데 LiS4가 124건에 등장한다는 사실도 중요합니다. LiS4 포함 여부는 드문 예외가 아니라 상당수 반응을 건드리는 분기입니다. 따라서 phase set을 먼저 고정하지 않고 90종 G3 통과 수나 순위를 말하는 것은 방어할 수 없습니다.

[이해용 확장]
grand-potential phase diagram이 낯선 청중에게는 이렇게 설명하세요. 후보가 분해될 수 있는 “허용된 분해산물 목록”이 바뀌면 가장 낮은 에너지 경로가 바뀌고, 그 결과 산화가 시작되는 전압도 바뀝니다. 시험 문제의 보기 목록을 바꾸면서 점수를 직접 비교하는 것과 비슷합니다.

[예상 질문]
Q. 어느 phase set이 맞나요?
A. 지금 슬라이드의 목적은 둘 중 하나를 즉시 정답으로 고르는 것이 아니라, 후보와 host를 동일 세트에서 비교해야 한다는 계약을 고정하는 것입니다. 물리적으로 제외할 상은 명시적 근거가 필요합니다.

[전환] 두 번째 핵심 감사는 역사적 G4가 실제 수송을 독립적으로 판정했는지입니다.

[Sources]
- db/properties/cascade_audit_g3_phase_set.csv
- docs/figures/cascade/cascade_audit_g3_phase_set.png
- db/properties/esw_lpscl_hull.json
- db/properties/esw_lis4excluded.json

========================================================================================

P9. 역사적 6/6 G4 stop은 물리적 수송 trade-off가 아니다 · 1:35

[1:35] 역사적 6/6 G4 stop은 물리적 수송 trade-off가 아니다

[발표 대본]
과거 발표에서는 산화 onset을 올린 여섯 후보가 모두 G4에서 멈췄다는 패턴을 산화–Li 경로 trade-off로 읽었습니다. 하지만 코드를 열어 보면 G4 composite는 blocking이 실패하는 순간 transport_norm을 0.05로 강제합니다. blocking은 도펀트 원자에서 4 Å 안에 있는 Li의 비율이고, 실제 확산이나 전도 측정이 아닙니다. 즉 빨간 표식의 낮은 값은 독립 BVS 결과가 아니라 blocking 실패를 다시 쓴 값입니다.

오른쪽 청록색 점은 그 0.05 floor를 제거하고 legacy BVS 값만 같은 방식으로 재정규화한 결과입니다. B2O3만 0.10으로 문턱 0.30 아래에 남고, Cr2O3, Ga2O3, In2O3, Sc2O3, Y2O3 다섯 종은 0.40~0.88로 통과합니다. 6/6 실패가 1/6 실패로 바뀝니다. 따라서 역사적 “산화 개선 후보 전부가 수송을 잃는다”는 결론은 독립적인 수송 증거가 아닙니다.

여기서 BVS-only 통과가 실제 전도성 개선을 증명하는 것도 아닙니다. cascade의 BVS 파라미터는 현재 canonical softBV와 다르고, v23에는 usable multiseed MD sigma가 없습니다. 따라서 먼저 matched low-x 구조에서 canonical softBV로 G4를 재정의하고, 경계 후보를 multiseed MD로 검증해야 합니다. 정확한 결론은 더 보수적입니다. 역사적 G4는 blocking과 BVS가 결합된 heuristic이고, 이 결합은 순환적으로 6/6 stop을 만들었습니다. 90종 current gate는 canonical softBV 또는 검증된 MD로 다시 정의해야 합니다.

[이해용 확장]
이 장은 발표의 가장 중요한 정정입니다. “blocking을 빼면 5/6이 통과하므로 다섯 후보가 좋은 수송재다”라고 말하면 또 과장입니다. 말할 수 있는 것은 기존 6/6 trade-off가 독립 수송 판정이 아니었다는 것뿐입니다. 청록 점은 반증용 rescore이지 새 leaderboard가 아닙니다.

[예상 질문]
Q. blocking 자체는 쓸모없나요?
A. 구조적 혼잡도를 빠르게 표시하는 heuristic으로는 쓸 수 있습니다. 다만 도펀트 수와 강하게 상관하고 실제 이동 장벽을 직접 재지 않으므로, 독립 transport evidence처럼 composite에 강제 floor로 넣으면 안 됩니다.

[전환] 따라서 과거 waterfall은 현재 후보 순위가 아니라 게이트 정의를 감사한 기록으로 남깁니다.

[Sources]
- db/properties/cascade_audit_g4_rescore.csv
- docs/figures/cascade/cascade_audit_g4_rescore.png
- tools/doping/run_uma_screening.py
- tools/cascade/build_cascade_themes.py
- tools/cascade/build_screening_funnel.py

========================================================================================

P10. 47종 waterfall은 역사적 audit이지 현재 선택 결과가 아니다 · 1:05

[1:05] 47종 waterfall은 역사적 audit이지 현재 선택 결과가 아니다

[발표 대본]
과거 47종 snapshot에서 G1은 47종 전부를 통과시켰고, G2가 유일하게 제거한 후보는 0종이었습니다. G1이 아무도 거르지 않은 이유를 threshold 문제라고 의심해 E_above_hull 기준도 시험했지만, 역시 사실상 제거가 없었습니다. 풀 자체가 안정한 흔한 이성분 산화물과 불화물로 큐레이션됐기 때문입니다. G2의 window-collapse 실패 네 종도 G3에서 모두 제거되어 unique kill이 0이었습니다.

이 결과는 무의미하지 않습니다. 후보의 물리보다 pool 설계와 gate redundancy를 알려 줍니다. 다만 G1부터 G5까지 이어진 47→47→43→25→11→1 숫자를 current 90종에 그대로 재사용하면 안 됩니다. G3 phase set, G4 circularity, G5 roster normalization이 모두 바뀌기 때문입니다. 과거 funnel은 historical archive로 보존하고, current 화면에서는 leaderboard와 Pareto를 숨기는 것이 맞습니다.

따라서 웹앱과 발표의 기본 화면도 승자표가 아니라 provenance와 status를 먼저 보여 줘야 합니다. 사용자가 recovered CSV를 내려받을 수는 있지만, archive·recovered·approved 상태가 파일과 함께 보이도록 해야 합니다.

[이해용 확장]
이 슬라이드는 “게이트가 아무도 안 거르면 왜 남겨 두나”라는 질문을 선점합니다. 제거 수가 0이라는 기록도 중요합니다. 다음 풀에서 같은 게이트가 작동할지 판단할 baseline이 되고, 중복 게이트를 줄이는 근거가 됩니다.

[예상 질문]
Q. G1과 G2를 다음 버전에서 삭제할 건가요?
A. 바로 삭제하기보다 새 풀에서 selection pressure와 독립 기여를 다시 측정해야 합니다. 다만 현재처럼 hard-gate 역할을 주장할 근거는 없습니다.

[전환] core funnel 밖에서 계산된 계면 축도 결론을 크게 바꾸지만, 적용 조건을 따로 봐야 합니다.

[Sources]
- db/properties/cascade_screening_funnel.json
- db/properties/cascade_stability_axes.csv
- db/properties/cascade_stability_axes_verdict.json
- db/properties/cascade_audit_manifest.json

========================================================================================

P11. 계면 축은 강하지만 core funnel에 아직 통합되지 않았다 · 1:20

[1:20] 계면 축은 강하지만 core funnel에 아직 통합되지 않았다

[발표 대본]
역사적 47종에 대해 계면 반응 축도 별도로 계산돼 있습니다. 이 값은 0 K pseudo-binary reaction driving force이며, 명시적 relaxed interface, 접착에너지 W_ad, 계면 성장 속도를 계산한 결과는 아닙니다. 100 meV/atom cutoff에서 양극 full과 half 모델은 각각 2종과 3종을 제거하지만, LPSCl–SE 축은 29종, Li metal 축은 35종을 제거합니다. 즉 bulk G1–G5보다 훨씬 강한 선택 압력이 숨어 있습니다.

하지만 이 숫자를 곧바로 새 hard gate로 넣으면 안 됩니다. 첫째, 47종 historical snapshot에 대한 post-hoc 계산입니다. 둘째, cutoff와 geometry sensitivity가 남아 있습니다. 셋째, 양극 coating 후보를 고르는 질문에서는 Li metal 축이 과도하게 엄격할 수 있습니다. 어떤 deployment question을 묻느냐에 따라 필요한 계면이 달라집니다.

그럼에도 이 결과는 다음 설계를 바꿉니다. bulk에서 좋아 보이는 shortlist를 곧바로 Pareto winner라고 부르기보다, 목적 계면에 대해 matched interface 계산을 먼저 해야 합니다. 특히 LPSCl 자체와의 반응 축이 29종을 제거한다는 점은 bulk descriptor만으로 coating 또는 additive 역할을 결정할 수 없음을 보여 줍니다.

[이해용 확장]
양극 full/half는 계면 모델의 두 구성이고, LPSCl SE와 Li metal은 다른 deployment 환경입니다. 청중에게 모든 축을 동시에 통과해야 한다고 말하지 말고, 사용 위치에 맞는 축을 고른다고 설명하세요.

[예상 질문]
Q. 계면 축이 이렇게 강하면 core funnel에 바로 G6, G7으로 넣어야 하지 않나요?
A. 후보는 될 수 있습니다. 다만 geometry, cutoff, applicability를 먼저 고정하고 90종 current pool에서 재계산해야 합니다. 지금은 audit-only evidence입니다.

[전환] 90종 회수가 추가한 화학적 대조군도 있지만, 그것 역시 순위가 아니라 가설 수정에 가깝습니다.

[Sources]
- db/properties/cascade_audit_interface_axes.csv
- docs/figures/cascade/cascade_audit_interface_axes.png
- db/properties/cascade_stability_axes.csv
- db/properties/cascade_stability_axes_verdict.json

========================================================================================

P12. Recovery는 대조군을 늘렸지만 원인이나 승자를 확정하지 않았다 · 1:20

[1:20] Recovery는 대조군을 늘렸지만 원인이나 승자를 확정하지 않았다

[발표 대본]
90종 회수의 가장 큰 가치는 순위가 아니라 대조군입니다. 역사적 47종은 산화물과 불화물만 포함해 “삼가 산화물”이 산화 onset을 올리는 것처럼 보였습니다. 회수분에는 Ga2S3와 Al2S3가 들어왔고, 같은 계열의 산화물과 비슷한 2.35 V 수준 onset이 나타납니다. 따라서 oxide-only 설명이 유일하지 않음을 시사합니다.

하지만 여기서 곧바로 “양이온이 전부 결정한다”고 말할 수는 없습니다. phase-set contract가 아직 통일되지 않았고, 조성·구조·분해상 차이를 통제한 matched causal pair가 아닙니다. Cl-rich variant에서 WO3, MoO3, Al2O3의 onset이 올라간 기록도 co-modification의 흥미로운 선례이지만, 같은 구조에 파트너 하나만 바꾼 명시적 pair 계산이 아니므로 인과 증거가 아닙니다.

회수가 실제로 바꾼 결론은 더 겸손하지만 중요합니다. 산화물만 보던 풀에서 세운 화학 가설은 더 넓은 family control을 만나면 바뀔 수 있습니다. 따라서 다음 후보는 기존 47종 점수 상위가 아니라, 가설을 가장 잘 반증하거나 구분하는 control이어야 합니다.

[이해용 확장]
이 슬라이드는 chemistry 이야기를 넣되 current ranking으로 보이지 않게 하는 장입니다. Ga2S3와 Al2S3의 숫자는 “대조군이 생겼다”는 예시로만 쓰고, cation-only mechanism이나 best sulfide라는 문장은 피하세요.

[예상 질문]
Q. LiBr, LiCl 같은 halide는 회수 후 어떻게 됐나요?
A. 산출물에는 존재하지만 current G4에는 host 원소 정의 때문에 blocking=0 artifact가 생길 수 있고, current rank는 승인되지 않았습니다. 값이 있다는 이유로 LiF와 동급이라고 결론 내리지 않습니다.

[전환] 이제 현재 증거로 말할 수 있는 것과 말할 수 없는 것을 명시적으로 나누겠습니다.

[Sources]
- db/properties/oxidation_stability_cascade_v2.json
- db/properties/cascade_v23_champions_v2.csv
- kb/methodology/cascade_pipeline_anatomy_2026_08_13.md
- docs/reviews/cascade_dftweb_source_of_truth_2026_08_14.md

========================================================================================

P13. 현재 지원되는 주장은 provenance와 반증까지다 · 1:10

[1:10] 현재 지원되는 주장은 provenance와 반증까지다

[발표 대본]
왼쪽은 현재 지원되는 주장입니다. 273개 슬롯 중 270개 완료, 90종 회수, 과거 141개와의 oxidation onset drift 0, G3의 phase-set 민감도, G4의 circular floor, post-hoc interface axis, ML 검증 지표는 각자의 출처와 규약 안에서 말할 수 있습니다. 이것들은 후보 순위보다 파이프라인의 신뢰 경계를 설명합니다.

오른쪽은 현재 지원되지 않는 주장입니다. 승인된 90종 leaderboard와 Pareto set, conductivity inferred from legacy BVS, 90종 current transport ranking, Cl의 인과 효과, 보편적 co-modification pair, 단일 winner는 말할 수 없습니다. x002/x005/x010을 실제 농도로 해석하는 것도 금지합니다.

이 경계를 명시하면 결과가 약해 보일 수 있지만 실제로는 반대입니다. 어떤 숫자가 raw, recovered, audit-only, approved인지 상태가 분리되면 후속 계산이 기존 결론을 조용히 덮어쓰지 않습니다. 그리고 실패한 가설도 negative result로 남아 다음 사람이 같은 실수를 반복하지 않게 합니다.

[이해용 확장]
이 슬라이드에서 “supported”는 진실의 등급이 아니라 현재 method contract가 허용하는 문장입니다. 예를 들어 phase-set sensitivity는 지원되지만 어느 phase set이 유일한 정답인지까지 지원되는 것은 아닙니다.

[예상 질문]
Q. 발표에서 후보 이름을 전혀 말하지 않으면 너무 소극적이지 않나요?
A. 후보 이름은 follow-up 예시로 말할 수 있습니다. 다만 현재 rank나 winner라고 부르지 않고, 어떤 가설을 시험하는 control인지 함께 말해야 합니다.

[전환] 같은 원칙으로 ML의 능력도 예측과 acquisition으로 나누어 봅니다.

[Sources]
- db/properties/cascade_audit_artifact_status.csv
- db/properties/cascade_audit_manifest.json
- docs/reviews/cascade_dftweb_source_of_truth_2026_08_14.md
- kb/methodology/terminology_register.md

========================================================================================

P14. ML은 새 화학의 물성을 예측하지 못하지만 제한된 순서는 도울 수 있다 · 1:25

[1:25] ML은 새 화학의 물성을 예측하지 못하지만 제한된 순서는 도울 수 있다

[발표 대본]
왼쪽은 새 도펀트 일반화 성능입니다. pair-CV weighted R2는 0.089로 낮고, 도펀트 하나를 통째로 뺀 LODO는 -0.180, 양쪽 도펀트를 모두 뺀 L2DO는 -0.255입니다. R2가 음수라는 것은 처음 보는 화학에 대해 평균값으로 찍는 것보다 못하다는 뜻입니다. 따라서 “모델이 이 pair의 물성을 예측했다”는 문장은 방어할 수 없습니다.

오른쪽은 acquisition 관련 지표입니다. 1081쌍 전체에서 좋은 40쌍을 top-40으로 끌어올리는 global discovery enrichment는 1.22배지만 p=0.426으로 랜덤과 구별되지 않습니다. 반면 이미 v1 휴리스틱으로 정한 40쌍 안의 순서는 3.35배, p=0.010으로 유의합니다. 하지만 이 양성 라벨은 실제 물성 성공이 아니라 기존 휴리스틱 수록 여부입니다. 따라서 이 결과는 retrospective ordering 능력이지 property discovery 검증이 아닙니다.

명시적 co-doped property label은 0개입니다. 이 상태에서 ML이 Cr2O3⊕HfO2 같은 pair가 좋다고 말하면 모델이 결론을 낸 셈입니다. 현재 허용되는 역할은 사람이 물리적으로 정의한 후보군 안에서 계산 순서를 조금 더 효율적으로 정하는 것입니다.

[이해용 확장]
LOOCV 0.9998 같은 높은 숫자를 질문받으면 target score가 입력 feature의 선형조합이라 공식을 되짚은 결과라고 설명하세요. 진짜 외삽 능력은 group holdout인 LODO/L2DO에서 봐야 합니다.

[예상 질문]
Q. ordering within 40이 유의하면 top-10을 바로 계산해도 되나요?
A. 그 40 자체가 과거 휴리스틱으로 선정됐기 때문에 global 발굴을 증명하지 않습니다. 물리가 먼저 후보군을 정하고, 그 안에서 순서 보조로만 사용해야 합니다.

[전환] 그래서 acquisition engine은 예측기와 무엇이 다른지 다음 장에서 구체적으로 보겠습니다.

[Sources]
- db/properties/cascade_audit_ml_validation.csv
- docs/figures/cascade/cascade_audit_ml_validation.png
- db/properties/codoping_ml_v2_meta.json
- db/properties/codoping_ml_v2.csv

========================================================================================

P15. Acquisition engine은 답이 아니라 다음 계산의 순서를 낸다 · 1:20

[1:20] Acquisition engine은 답이 아니라 다음 계산의 순서를 낸다

[발표 대본]
예측기와 acquisition engine의 가장 큰 차이는 모델 출력의 책임입니다. 예측기는 출력 숫자를 물성값으로 믿기 때문에 모델이 틀리면 논문 결론이 틀립니다. acquisition engine은 출력으로 계산 순서만 정합니다. 모델이 틀리면 비싼 계산 하나를 덜 효율적으로 쓸 수 있지만, DFT·MD·실험이 최종 라벨을 만들고 그 실패도 다음 학습 데이터로 회수됩니다.

현재 loop는 VALIDATE, RECOVER, EXPLORE, ACQUIRE의 네 단계로 생각할 수 있습니다. recovered structure pool을 출발점으로 두고, 먼저 정의가 불안정한 G3·G4 contract를 validate합니다. 그다음 AlI3와 MgI2 같은 missing axis를 recover합니다. 이후 새 chemistry와 boundary case를 explore하고, 그때 처음 explicit pair 구조를 만듭니다. 검증 결과는 versioned database에 돌아가며 다음 acquisition을 갱신합니다.

여기서 모델은 모든 1081쌍을 한 번에 물성 순위로 선언하지 않습니다. phase-set 경계, canonical BVSE 경계, 계면 반응 경계처럼 현재 결론을 가장 크게 바꿀 수 있는 점을 먼저 고르는 데 사용합니다. 즉 exploitation보다 validation과 information gain이 앞섭니다.

[이해용 확장]
초심자에게는 병원 검사 순서로 비유할 수 있습니다. acquisition engine은 진단명을 내리는 모델이 아니라, 제한된 검사 예산으로 어떤 검사를 먼저 해야 불확실성이 가장 빨리 줄어드는지 정하는 도구입니다. 최종 진단은 실제 검사 결과가 내립니다.

[예상 질문]
Q. 모델이 랜덤과 구별되지 않는데 왜 굳이 쓰나요?
A. global discovery에는 아직 쓰지 않습니다. 물리적으로 제한한 후보군 안의 순서 보조, 불확실성·다양성·경계 표본화에만 사용하고 prospective 결과로 다시 검증합니다.

[전환] 이 원칙을 실제 실행 순서로 바꾸면 다음 네 단계가 됩니다.

[Sources]
- docs/cascade_ml_integration_guide.md
- db/properties/codoping_ml_v2_meta.json
- Duquesnoy et al., Energy Storage Materials (2023), DOI 10.1016/j.ensm.2022.12.040

========================================================================================

P16. 다음 loop는 pair ranking보다 정의 검증이 먼저다 · 1:20

[1:20] 다음 loop는 pair ranking보다 정의 검증이 먼저다

[발표 대본]
첫 단계는 VALIDATE CONTRACTS입니다. G3 후보와 host를 같은 phase_set_id로 다시 계산하고, G4는 프로젝트 canonical softBV 파라미터와 명시된 구조 규약으로 재정의합니다. 이 단계에서 historical cutoff를 그대로 유지할지, 어떤 branch를 허용할지 frozen schema로 남깁니다.

두 번째는 RECOVER LABELS입니다. AlI3 전면 결측과 MgI2 부분 결측을 복구하고, 실제 G5 입력인 E와 Pugh를 포함한 gate-specific completeness를 검사합니다. 불필요한 B0 결측 때문에 전체 종을 partial이라고 부르지 않고, 각 게이트에 필요한 필드만 fail-closed로 검사합니다.

세 번째는 TEST BOUNDARIES입니다. 저농도 2×2×1 구조에서 canonical 정적 pathway를 먼저 보고, 경계 후보만 multiseed MD와 목적 계면 계산으로 올립니다. 마지막이 EXPLICIT PAIRS입니다. 서로 다른 역할을 가정한 두 개질자를 명시적 구조에 같이 넣고, 같은 cell·reference·constraint로 matched label을 얻은 뒤에만 grouped CV를 시작합니다.

[이해용 확장]
이 순서가 중요한 이유는 pair 공간이 크기 때문입니다. 정의가 불안정한 gate로 pair를 먼저 계산하면 잘못된 target을 더 많은 데이터로 정밀하게 학습하게 됩니다. 작은 검증 계산 세 개가 큰 pair campaign보다 먼저입니다.

[예상 질문]
Q. In2O3, Ga2O3, B2O3 저농도 계산을 먼저 돌리는 게 맞나요?
A. 구조적 참고는 되지만, 먼저 canonical G4 정의를 고정해야 합니다. 그렇지 않으면 낮아진 4 Å blocking을 실제 수송 개선으로 다시 오해할 수 있습니다.

[전환] 그래서 바로 실행할 최소 계산과 stop/go 규칙을 숫자로 정리하겠습니다.

[Sources]
- docs/reviews/cascade_dftweb_source_of_truth_2026_08_14.md
- AGENTS.md canonical BVSE and MLIP-MD conventions
- db/properties/cascade_audit_gate_completeness.csv
- kb/methodology/cascade_pipeline_anatomy_2026_08_13.md

========================================================================================

P17. 세 개의 작은 검증이 다음 큰 캠페인의 go/no-go를 정한다 · 1:15

[1:15] 세 개의 작은 검증이 다음 큰 캠페인의 go/no-go를 정한다

[발표 대본]
첫 번째 최소 계산은 G3 matched phase-set test입니다. LiS4 포함과 제외를 혼합하지 않고, 동일 phase_set에서 host와 대표 후보를 비교해 0.116 V 민감도가 candidate ordering을 실제로 바꾸는지 확인합니다. 두 번째는 canonical low-x pathway case 두 건입니다. historical cascade BVS가 아니라 프로젝트 표준 softBV로, 의도 범위의 낮은 농도 구조를 비교합니다.

세 번째는 이 경계에서 살아남는 후보 세 건 정도의 multiseed MD 또는 목적 계면 계산입니다. 정적 proxy가 실제 동역학이나 interface reaction과 같은 방향인지 확인합니다. 여기서 결과가 historical G3/G4 story를 바꾸면 gate를 재설계하고 과거 순위를 승계하지 않습니다. 반대로 경계가 강건하면 schema를 freeze하고 그때 90종 current ranking을 다시 만듭니다.

모든 직접 비교에는 같은 구조 계보, cell, constraint, k-mesh, reference, magnetic protocol, uncertainty와 status가 필요합니다. 이 계약이 지켜진 뒤에만 explicit co-modification pair를 acquisition queue에 올립니다. 다음 성과의 단위는 후보 이름 하나보다, 다시 실행해도 같은 판단을 내리는 decision contract입니다.

[이해용 확장]
숫자 1·2·3은 거대한 생산 계산 수가 아니라 최소 검증 묶음입니다. 실제 케이스 수는 계산 비용과 경계 밀도에 따라 바꿀 수 있지만, validation→recovery→boundary라는 순서는 유지합니다.

[예상 질문]
Q. 그러면 언제 90종 leaderboard를 공개할 수 있나요?
A. G3 phase-set과 G4 canonical definition을 freeze하고, AlI3/MgI2를 포함한 gate-specific completeness가 fail-closed로 통과하며, roster normalization을 같은 버전으로 재생성했을 때입니다.

[전환] 마지막으로 오늘의 결론을 후보 이름이 아니라 의사결정 규칙으로 닫겠습니다.

[Sources]
- db/properties/cascade_audit_manifest.json
- db/properties/cascade_audit_gate_completeness.csv
- AGENTS.md matched-method conventions
- docs/cascade_pipeline_guide.md

========================================================================================

P18. 결론은 승자가 아니라 검증 가능한 의사결정 계약이다 · 0:55

[0:55] 결론은 승자가 아니라 검증 가능한 의사결정 계약이다

[발표 대본]
정리하겠습니다. 273개 실행 슬롯 중 270개가 완료됐고 90종의 계산이 회수됐습니다. 과거 47종 snapshot은 물리적 생존 집합이 아니라 당시 등록 경계였습니다. 회수된 90종은 화학 대조군을 넓혔지만, G3 phase-set, G4 circularity, gate-specific missingness와 roster normalization 때문에 현재 승인된 leaderboard와 Pareto, transport ranking은 없습니다.

대신 무엇을 먼저 계산해야 하는지는 분명해졌습니다. G3와 G4의 정의를 같은 참조계에서 검증하고, 결측 축을 회수하고, boundary를 MD와 interface로 확인한 뒤, explicit pair label을 얻습니다. ML은 그 순서를 정하는 acquisition engine으로 사용하고, DFT·MD·실험이 주장 여부를 결정합니다.

그래서 이번 프로젝트의 ‘so what’은 1등 첨가제 이름이 아닙니다. 계산을 많이 돌리는 것과 믿을 수 있는 결론을 만드는 것은 다른 일이며, 그 사이를 연결하는 provenance와 method contract가 다음 캠페인의 가장 중요한 설계 변수라는 것입니다.

[이해용 확장]
마지막에는 숫자를 다시 한 번 천천히 읽어 주세요. 273 workload, 270 complete, 90 recovered, 47 historical, current rank 0, current Pareto/transport 0. 그리고 “0은 좋은 후보가 0개라는 뜻이 아니라, 현재 조건으로 승인된 순위 행이 아직 없다는 뜻”이라고 마무리하면 됩니다.

[예상 질문]
Q. 한 문장으로 다음 액션은 무엇인가요?
A. 같은 phase set의 G3와 canonical low-x pathway를 먼저 검증하고, 그 결과로 explicit pair acquisition queue를 만듭니다.

[전환] 질문을 주시면 각 숫자의 원자료와 허용되는 주장 범위를 함께 확인하겠습니다.

[Sources]
- db/properties/cascade_audit_manifest.json
- docs/reviews/cascade_dftweb_source_of_truth_2026_08_14.md
- kb/methodology/cascade_pipeline_anatomy_2026_08_13.md

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

P23. G1–G5는 다섯 개의 방법 계약이다 · 부록

[1:35] G1부터 G5까지 정확히 무엇을 재나

[발표 대본]
G1은 같은 UMA 계보 안에서 host보다 구조 에너지가 낮은지를 보는 역사적 상대값입니다. Materials Project convex hull의 E_above hull이 아닙니다. G2는 역사적 grand-potential window branch이고, G3는 후보 onset을 host와 비교합니다. G3는 반드시 같은 phase set에서만 비교해야 합니다.

G4가 가장 주의할 부분입니다. cascade의 legacy Adams BVS를 현재 후보 풀 안에서 min-max 정규화한 값과, foreign atom에서 4 Å 안에 있는 Li의 비율을 결합합니다. 그리고 blocking cutoff를 실패하면 BVS 값과 무관하게 composite를 0.05로 강제합니다. 그래서 두 독립 수송 증거가 아닙니다. canonical BVSE 장벽도, 확산계수 D도, 전도도 sigma도 아닙니다.

G5는 Young's modulus와 Pugh ratio를 후보 목록의 median에 대해 비교한 상대 ranking입니다. 후보 목록이 47에서 90으로 바뀌면 기준 자체가 바뀝니다. 따라서 historical 점수와 current 점수를 직접 이어 붙일 수 없습니다.

[이해용 확장]
Li2S와 LiCl은 구현상 foreign atom이 하나도 없어 blocking=0이 됩니다. 이는 좋은 채널을 찾은 것이 아니라 지표가 적용 대상을 찾지 못한 것입니다. 값이 없으면 통과나 탈락을 억지로 정하지 않고 missing으로 보류해야 합니다.

[예상 질문]
Q. 그럼 기존 G1–G5는 전부 버리나요?
A. 역사적 audit와 코드 회귀에는 남길 수 있습니다. 하지만 current ranking에 쓰려면 phase set, canonical low-x softBV, roster와 missingness 계약을 다시 고정해야 합니다.

[전환] 마지막 부록은 현재 허용되는 주장과 금지되는 주장을 한 화면에 정리합니다.

[Sources]
- tools/cascade/build_cascade_themes.py and build_screening_funnel.py, frozen audit
- db/properties/cascade_audit_g4_rescore.csv
- docs/reviews/cascade_dftweb_source_of_truth_2026_08_14.md

========================================================================================

P24. 최종 산출물은 evidence ledger다 · 부록

[1:25] 현재 무엇을 말할 수 있고 무엇을 말할 수 없나

[발표 대본]
현재 확실히 말할 수 있는 것은 실행과 감사입니다. 273개 계획 슬롯, 활성 workflow 270개 완료, 90종 회수, 과거 47종 snapshot의 등록 경계, 과거 141개와 회수본 사이 산화 onset drift 0, G3 phase-set 민감도와 G4 순환 구조는 출처와 범위를 붙여 말할 수 있습니다. 계면 축과 ML 검증도 각각 historical post-hoc와 retrospective audit라는 범위 안에서 말할 수 있습니다.

말할 수 없는 것은 current 90종 leaderboard, Pareto, transport shortlist, legacy BVS에서 얻은 전도도, Cl의 인과 효과, 보편적인 pair와 단일 winner입니다. AlI3의 gate 입력은 전면 결측이고 MgI2는 축별 결측이 있습니다. 71 complete, 18 partial, 1 dropped라는 sidecar는 사용하지 않는 B0를 필수로 세고 실제 G5의 Pugh를 빠뜨렸으므로 gate completeness가 아닙니다.

ML도 범위를 나눕니다. 1081쌍 전역에서 좋은 후보를 top-40으로 끌어올리는 능력은 1.22배, p=0.426으로 무작위와 구별되지 않습니다. 이미 선택된 40쌍 내부의 순서는 3.35배, p=0.010이지만 retrospective 결과입니다. explicit pair property label은 0개입니다. 따라서 ML은 답을 내는 예측기가 아니라 다음 계산의 순서를 제안하는 acquisition helper입니다.

[이해용 확장]
다음 순서는 같은 phase set의 GP, realistic low-x canonical softBV, 경계 후보 multiseed MD와 목적 계면 계산, 마지막으로 explicit pair입니다. 각 결과가 데이터베이스에 method tag와 approval status를 가진 label로 돌아와야 그때 처음 current ranking을 만들 수 있습니다.

[예상 질문]
Q. 이 감사의 최종 산출물은 무엇인가요?
A. 좋은 후보 이름이 아니라, 어떤 증거가 다음 비싼 계산과 발표 문장을 허용하는지 정의한 decision contract입니다.

[전환] 본문 결론으로 돌아가면, validate definitions, recover labels, test boundaries, acquire pairs 순서입니다.

[Sources]
- db/properties/cascade_audit_manifest.json
- db/properties/cascade_audit_gate_completeness.csv
- db/properties/cascade_audit_ml_validation.csv
- kb/reviews/cascade_9abe5105_release_audit_2026_08_14.md
