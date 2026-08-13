# 발표 대본 — Research Seminar 2026-08 · Cascade **rev3 (정본)**

* 덱: `kb/seminars/Research_Seminar_2026_08_cascade_rev3.pptx`
* 본문: 19장 · 목표 22–24분
* 부록: 11장 · 질문 때만 사용
* 흐름: 문제와 규모 → 비용 배치 → 게이트 감사 → 두 trade-off → 다음 label 획득

> **발표의 한 문장**: 싼 모델은 계산의 순서를 정하고, 물리와 실험이 주장을 결정합니다.

**db 대조 완료 (2026-08-13)** — P7 gap 2.066/2.099 · P9 47→43→25→11 · P10 G1 unique_kill 0 ·
P11 산화 상승 6종(B₂O₃·Cr₂O₃·Ga₂O₃·In₂O₃·Sc₂O₃·Y₂O₃) · P13 42.082/18위 ·
P14 non-dominated CaF₂·CaO·SiO₂·WO₃ · P29 seminar CSV 4종. 전부 정본과 일치.

---

# 본문

## P1. Opening — what changed after verification · 0:45
안녕하세요, 재료공학과 안용훈입니다. 처음 목표는 47개 후보에서 1등을 고르는 거였습니다. 그런데 값을 다시 확인하고 게이트를 감사할수록 더 또렷해진 건 1등이 아니라, 산화 안정성과 Li 경로가 같이 좋아지지 않는다는 제약이었습니다. 오늘은 그 결론까지 어떻게 갔고, 어디까지 믿을 수 있는지 말씀드리겠습니다.
→ 먼저 왜 한 개의 점수로는 이 문제를 풀기 어려운지부터 보겠습니다.

## P2. One modification meets several interfaces · 1:00
LPSCl을 고칠 때 상대는 한 군데가 아닙니다. Li 쪽, 전해질 내부, 양극 쪽 계면에서 요구하는 조건이 서로 다르고, 접촉과 압력까지 영향을 줍니다. 왼쪽 coating 그림은 치환과 coating이 같다는 뜻이 아니라, 하나의 처방이 여러 계면을 지나야 한다는 문제 구조를 보여주는 예입니다. 그래서 단일 점수보다 먼저 필요한 건 질문의 순서입니다.
→ 그 질문이 실제 캠페인에서는 얼마나 커지는지 보겠습니다.

## P3. 273 is a run-slot count · 0:50
후보 화합물은 91종이었고, 각 후보를 세 개의 campaign label로 돌려서 실행 슬롯은 273개였습니다. 여기서 chemistry, configuration, target property는 후보 수를 더 곱한 숫자가 아니라 의사결정 차원입니다. 또 x002, x005, x010은 실제 농도로 환산한 값이 아니라 명목 라벨입니다. 이 구분을 먼저 해야 뒤의 숫자를 과장하지 않게 됩니다.
→ 이 많은 조합에 비싼 계산을 똑같이 쓸 수는 없습니다.

## P4. The cascade is a cost-allocation rule · 1:00
Cascade의 핵심은 계산량이 아니라 비용 배치입니다. 싼 모델로 넓게 보고, 물리 게이트로 위험한 후보를 찾고, 비싼 DFT와 실험은 경계나 불일치에 씁니다. Xiao의 coating screen과 Kahle의 pinball-to-FPMD 흐름도 규모와 재료는 다르지만 같은 원칙을 씁니다. 값싼 모델은 최종값을 대신하지 않고, 정밀 계산의 순서를 정합니다.
→ 다만 우리 데이터의 출발점은 273개 생존 경쟁이 아닙니다.

## P5. The 47 are a versioned O/F snapshot · 1:05
원자료를 따라가면 2026년 6월 25일 표에 들어온 건 산화물 37종과 불화물 10종, 모두 47종입니다. 세 라벨을 합치면 141개 기록입니다. 나머지 44종은 무작위로 빠진 게 아닙니다. 염화물 19, 황화물 11, 브롬화물 5, 질화물 5, 요오드화물 4 — 다섯 계열이 통째로 빠졌고, 산화물과 불화물은 전원 들어왔습니다. 한 계열 안에서 일부만 살아남은 경우는 한 건도 없습니다. 경계가 계열과 정확히 일치하니 이건 물리 판정이 아니라 취합 경계입니다. 개별 종의 실패 원인은 여전히 기록에 없습니다. 그래서 273에서 47이 살아남았다고 말하지 않고, 이후 분석이 시작되는 versioned O/F snapshot이라고 부르겠습니다 — 이름의 O와 F가 바로 들어온 두 계열입니다.
→ 이 47종은 같은 저비용 규약으로 비교하고, 일부만 다음 층으로 올렸습니다.
🛡 *왜 산화물·불화물만 들어왔나?* → "계열 경계와 정확히 일치합니다 — Phase 1A 산화물 37종 전원, Phase 1B 중 불화물 10종 전원이 들어오고 염화물·황화물·브롬화물·질화물·요오드화물은 통째로 빠졌습니다. 물리 판정이라면 계열이 이렇게 깨끗하게 갈릴 수 없으니 취합 경계로 봅니다. 계열별 표는 attrition CSV 에 있습니다."
🛡 *그럼 그 44종은 나쁜 후보인가?* → "아닙니다. 판정된 적이 없습니다 — 오늘 결론은 전부 O/F 스냅샷 안에서만 유효합니다." 

## P6. Different tiers answer different questions · 0:50
L0는 사람이 고른 조성과 provenance, L1은 UMA와 저비용 프록시, L2는 선택된 후보의 matched DFT, L3는 실험입니다. 중요한 건 값마다 프로토콜과 출처가 같이 움직인다는 점입니다. 47종은 같은 규약 안의 상대 screen이고, deep DFT는 두 건뿐입니다. 둘을 같은 정확도의 표처럼 섞지 않습니다.
→ 그럼 저비용 screen에서 무엇을 볼지, host 비교에서 배운 기준을 보겠습니다.

## P7. Host evidence sets the descriptor priorities · 0:55
같은 프로토콜에서 comp1과 Cl-rich model을 비교했을 때 band gap은 2.066과 2.099 eV로 의미 있게 갈리지 않았습니다. 반면 Li vacancy와 anti-site disorder는 구조 쪽에서 분명했습니다. 그래서 전자구조는 가드레일로 두고, 구조와 Li 경로를 우선 축으로 잡았습니다. 여기서 gap은 fixed-occupation 고유값만 쓰고, DOS 문턱값은 쓰지 않습니다.
→ 이 축들을 다섯 질문으로 나눈 게 다음 게이트입니다.

## P8. Five gates, five questions · 1:05
G1은 구조 안정성, G2는 electrochemical window, G3는 산화 onset, G4는 정적 Li pathway, G5는 역학 순위입니다. 여기서 G4의 blocking 0.60은 working heuristic이고, G5는 물리 탈락 게이트가 아니라 roster-relative ranking입니다. 따라서 오늘 비교 endpoint는 G1부터 G4까지입니다.
→ 이 규칙을 47종 snapshot에 적용하면 숫자는 이렇게 줄어듭니다.

## P9. The auditable endpoint is 11 · 1:00
47종에서 window를 지나 43, oxidation을 지나 25, 정적 Li pathway까지 11종이 남습니다. G5를 적용하면 하나가 보이지만, 그 한 종은 임계값을 바꾸면 쉽게 바뀌는 순위 결과입니다. 그래서 물리 게이트의 보고 지점은 11종이고, 이 waterfall은 문헌 기준을 사후에 투영한 audit view입니다.
→ 그런데 이 숫자보다 먼저 봐야 할 건 게이트가 실제로 일을 했는가입니다.

## P10. G1 selects nobody; G2 adds no unique exclusion · 0:50
G1은 47종이 전부 통과합니다. 이건 보편적 안정성을 증명한 게 아니라, 안정한 후보를 먼저 고른 큐레이션 흔적입니다. G2에서 빠진 네 종은 G3에서도 모두 빠져 unique kill이 0입니다. 후보만 평가한 게 아니라, 게이트의 선택 압력과 중복도 같이 기록했습니다.
→ 그 감사를 통과하고도 남은 가장 강한 패턴이 다음 장입니다.

## P11. All six oxidation gains stop at the Li-path gate · 1:25
Host보다 산화 onset이 오른 후보는 여섯입니다. 그런데 여섯 모두 G4에서 멈춥니다. 한 후보의 예외가 아니라 이 snapshot에서 반복되는 trade-off입니다. 다만 G4는 BVSE 기반 정적 pathway risk라서 전도도도 아니고, M–O 결합이 원인이라는 증명도 아닙니다. 지금 말할 수 있는 건 산화 개선 후보 전부가 별도의 경로 위험을 동반했다는 것까지입니다.
→ 이 제약 방향이 황화물 문헌에서도 보이는지 확인했습니다.

## P12. Related sulfide work points to the same difficulty · 1:05
Banik, Zeier, Mo의 2022년 연구는 HAXPES, pDOS와 COHP, grand-potential, stepwise CV를 함께 써서 sulfide framework 안의 치환으로 산화 onset을 크게 움직이기 어렵다는 제약을 보여줍니다. 우리 쪽은 oxide와 fluoride unit을 더하는 다른 조성축이라 독립 재현이라고 부를 수는 없습니다. 다만 우리 screen에서도 산화가 오른 후보가 모두 별도 pathway risk를 가진다는 방향성은 맞닿아 있습니다.
→ 그리고 두 번째 trade-off는 물리 게이트가 아니라 값 검증에서 나왔습니다.

## P13. One corrected value changed the conclusion · 1:00
Sc2O3의 E_VRH가 한 파일에는 18.7 GPa로 적혀 있었는데, raw output은 42.082 GPa였습니다. 교정 뒤에는 가장 연한 후보에서 18위로 내려갔고, 형성에너지 1위만 남았습니다. 숫자 한 자리 수정이 아니라 '한 후보가 두 축을 모두 이긴다'는 해석이 사라진 겁니다. 이후에는 교차파일 값과 raw output을 함께 확인하는 규칙으로 바꿨습니다.
→ 그래서 최종 선택도 단일 점수 대신 조건부 Pareto로 읽습니다.

## P14. Four conditional trade-off options remain · 0:55
G1부터 G4까지 남은 11종에서 mean relative energy와 transport proxy 두 축만 보면 WO3, SiO2, CaF2, CaO 네 종이 non-dominated입니다. 이것은 webapp의 legacy 3D Pareto 네 종과 다른 집합입니다. 축과 모수가 다르기 때문에 숫자 4만 보고 섞으면 안 됩니다. 이 네 종도 winner가 아니라 다음 질문을 나눠 가진 후보입니다.
→ 후보를 실제로 고를 때는 적용 질문을 하나 더 붙여야 합니다.

## P15. The answer changes with the deployment question · 1:05
LiF는 정적 계면 안정성 쪽이 강하고, MgO와 CaO는 비용과 질량이 유리합니다. Cu2O는 문헌 수분 proxy가 좋지만 oxidation과 LPSCl interface 쪽에서는 불리합니다. 같은 후보도 어느 계면과 공정을 우선하는지에 따라 다음 실험이 달라집니다. 이 표는 수명이나 kinetics를 확정하는 표가 아니라 후속 질문을 고르는 표입니다.
→ 여기까지의 주장을 어디까지 허용할지 경계를 명시했습니다.

## P16. Claim strength follows method strength · 0:55
게이트 통과와 같은 규약 안의 상대 비교는 말할 수 있습니다. UMA 절대 에너지, BVSE-derived conductivity, 축퇴군 안의 세밀한 순위는 말하지 않습니다. 또 G4 threshold sensitivity는 아직 닫히지 않았습니다. 120개 gate order의 최종 교집합이 같은 건 AND gate의 성질이라 본문 근거로 과장하지 않고 부록 audit로만 남겼습니다.
→ 검증 범위도 같은 방식으로 분리해서 읽습니다.

## P17. 47, 11, and 2 are parallel coverage counts · 0:55
47은 상대 screen, 11은 post-hoc G1–G4 endpoint, 2는 targeted deep-DFT case입니다. 이 셋은 47에서 11, 다시 2로 내려가는 선형 funnel이 아닙니다. B2O3와 Nd2O3는 11종 생존자 검증셋이 아니라, 서로 다른 실패 경계를 확인하려고 고른 case study입니다.
→ 이제 ML이 이 구조에서 실제로 하는 일을 나누어 보겠습니다.

## P18. ML saves cost; it does not certify discovery · 1:15
UMA는 이미 에너지와 힘을 빠르게 계산하는 엔진입니다. 반면 co-doping v2는 47개 단일 후보를 1,081개 pair hypothesis로 정렬하지만, explicit pair structure와 DFT·실험 pair label은 아직 0개입니다. 도펀트를 통째로 빼는 검증에서는 R2가 음수입니다. Sendek과 Kahle의 사례처럼 싼 모델의 역할은 비싼 계산을 고르는 것이지, 그 자체로 물성을 확정하는 게 아닙니다.
→ 그래서 다음 단계는 더 큰 모델이 아니라 실제 pair label을 얻는 일입니다.

## P19. The next cascade chooses the next expensive calculation · 1:15
다음 loop에서는 explicit co-doped 구조를 만들고, matched DFT와 실험으로 실제 label을 얻습니다. acquisition은 Pareto gain만 보지 않고 불확실성, 새로운 화학, gate boundary를 같이 고릅니다. Duquesnoy의 multi-objective loop처럼 모델은 다음 점을 제안하고, 물리와 실험이 판정을 합니다. 현재 증거는 보편적 승자를 지지하지 않습니다. 대신 다음 비싼 계산을 어디에 써야 하는지는 분명해졌습니다. 감사합니다.
→ 질문 주시면 뒤의 출처·규약·후보별 표로 바로 확인하겠습니다.

---

# 부록 운용

## P20. Appendix A1 — 47-species cast list
특정 후보가 전체 pool에 있었는지 물을 때 사용합니다. 굵은 글씨는 post-hoc G4 retained, 단검은 targeted deep-DFT case입니다. 명단 포함과 gate pass는 다른 사실입니다.

## P21. Appendix A2 — evidence by deployment question
적용 질문마다 보는 축과 증거 등급이 다릅니다. air, cost, mass, campaign labels는 follow-up axis이지 추가 hard gate가 아닙니다.

## P22. Appendix A3 — gate-order audit
120개 순서를 전수 확인했을 때 terminal intersection은 같습니다. 이것은 threshold validation이 아니라 중간 waterfall의 attribution이 순서에 따라 달라진다는 audit입니다.

## P23. Appendix A4 — retraction ledger
초기 규칙이 불완전했던 사례와 재발 방지 규칙을 함께 기록했습니다. 철회 목록 자체보다 오류 검출이 실행 규칙으로 바뀌었는지가 핵심입니다.

## P24. Appendix A5 — terminology
기호나 x-label 해석 질문에 씁니다. 특히 transport_norm은 정적 pathway proxy이며 D나 conductivity라고 부르지 않습니다.

## P25. Appendix A6 — allowed claims by method
방법마다 허용되는 주장과 금지되는 주장을 정리한 표입니다. 서로 다른 fidelity의 값을 하나의 truth column으로 섞지 않습니다.

## P26. Appendix A7 — 47-species scorecard
후보별 축을 한눈에 볼 때 씁니다. 색은 within-pool favorable percentile이고 composite score나 universal winner는 없습니다.

## P27. Appendix A8 — cascade defense
273/47 계보, vacuous gate, G4 heuristic, 11종 endpoint 질문에 대한 짧은 답입니다.

## P28. Appendix A9 — validation and ML defense
DFT 2/47, LOOCV와 grouped holdout의 차이, explicit pair label이 필요한 이유를 정리한 표입니다.

## P29. Appendix A10 — data sources
발표 숫자는 Origin-ready seminar CSV 네 종과 gate JSON에서 읽습니다. Webapp은 확인용 reader이며 별도의 정본이 아닙니다. Webapp의 legacy Pareto와 현행 2D conditional Pareto는 구분합니다.

## P30. Appendix A11 — methods and literature
방법 규약, 감사 기록, 외부 문헌의 경로입니다. 외부 문헌 수치는 맥락과 방법 계보로만 쓰고 우리 threshold로 이식하지 않습니다.

---

# 리허설 카드

* 5분: P1–P4 — 질문과 비용 배치
* 5분: P5–P9 — 47 snapshot과 게이트
* 7분: P10–P15 — gate audit, 6/6 trade-off, 문헌, 값 교정, Pareto
* 3분: P16–P17 — trust boundary와 47/11/2
* 4분: P18–P19 — ML의 현재 역할과 다음 계산

**반드시 정확히 말할 숫자**

1. 273 = 91종 × 3 nominal campaign labels의 run slots
2. 47 = versioned O/F snapshot, 141 ingested records (산화물 37/37 + 불화물 10/10 전원; 빠진 44는 염화물 19·황화물 11·브롬화물 5·질화물 5·요오드화물 4 — 계열 단위)
3. 47 → 43 → 25 → 11은 post-hoc G1–G4 audit view
4. 산화 onset이 오른 6종은 모두 static Li-pathway gate에서 정지
5. deep DFT 2건은 11종 생존자 검증셋이 아니라 parallel case studies

**말하지 않을 것**

* 273개 후보 중 47개가 살아남았다고 말하지 않기
* 빠진 44종을 '탈락' 이나 '나쁜 후보' 라고 말하지 않기 — 계열 단위 취합 경계이지 물리 판정이 아니다
* BVSE를 conductivity로 부르지 않기
* webapp legacy Pareto 4종과 seminar conditional 2D Pareto 4종을 섞지 않기
* Banik 2022를 우리 조성축의 독립 재현이라고 부르지 않기
* 47 → 11 → 2를 하나의 순차 funnel로 그리지 않기

**확인한 자료 범위**
Origin-ready CSV/PNG 네 종, webapp cascade loader와 template, canonical registry 상태, 관련 litdb digest와 주요 figure crop을 대조했습니다. 문헌 그림에서만 읽은 값을 발표의 정량값으로 이식하지 않았습니다.
