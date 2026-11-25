# Research Seminar 2026-08 — Korean speaker script

> Closed deck: 29 slides (20 main + 9 appendix). Visible slide copy is English; this script is conversational Korean.

## Slide 1. Self-auditing computational screening

오늘 발표의 핵심은 후보 하나를 골랐다는 이야기가 아니에요. 황화물 고체전해질의 치환 후보를 계산으로 줄이는 동안, 어떤 주장까지 허용되는지 gate로 제한하고 틀린 결론을 다시 철회한 과정을 보여드리려 해요. 그래서 결과보다도 ‘어떤 근거가 어떤 문장을 허용하는가’를 중심으로 보시면 돼요.

Sources:
- `kb/seminars/cascade_seminar_2026_08_spec.md`

## Slide 2. 왜 screening이 필요한가

LPSCl 같은 host에서도 할로겐 종류, 비율, 치환종, campaign label이 곱으로 늘어나요. 실험은 합성부터 구조·임피던스·셀 평가까지 시간이 오래 걸리니까, 계산의 역할은 실험을 대체하는 게 아니라 우선순위를 줄이는 거예요. 다만 오른쪽 waterfall은 273에서 47이 물리적으로 걸러졌다는 뜻이 아니고, 47종 snapshot에서 한 사후 gate audit이에요.

Sources:
- `db/properties/cascade_v23_ranked.csv`
- `db/properties/cascade_screening_funnel.json`

## Slide 3. 발표의 논지

좋은 screening은 rank가 예쁜지가 아니라, 실패했을 때 왜 실패했는지 남기는지가 중요해요. 이 발표에서는 잘못된 gap 판독, 단일 seed 수송 결론, MLIP 반응 해석 같은 사례를 gate로 바꿨어요. 즉 self-auditing은 사후 변명이 아니라 다음 계산에서 자동으로 작동하는 규칙이에요.

Sources:
- `kb/seminars/cascade_seminar_2026_08_spec.md`
- `db/properties/canonical_registry.json`

## Slide 4. 닫힌 계산 루프

전체 흐름은 curate, compute, verify, screen의 반복이에요. compute에서 숫자가 나와도 바로 screening에 넣지 않고, verify에서 방법·source·status가 맞는지 확인해요. screen 뒤에는 다시 어떤 라벨이 부족한지 계산해 다음 구조를 고릅니다. 뒤의 co-doping은 바로 이 마지막 feedback 단계예요.

Sources:
- `kb/seminars/cascade_seminar_2026_08_spec.md`

## Slide 5. 273과 47의 provenance

여기는 반드시 단위를 분리해서 말씀드릴게요. 273은 91종에 세 개 nominal label을 곱한 실행 슬롯이에요. 현재 versioned canonical table은 2026년 6월 25일 snapshot으로, oxide 37종과 fluoride 10종, 총 47종의 141개 record만 들어 있어요. 나머지 44종이 물리적으로 탈락한 건 아니고, 개별 실패 manifest가 없어서 현재는 미분류예요. 따라서 273에서 47로 떨어졌다는 discovery funnel 해석은 하지 않습니다.

Sources:
- `db/properties/cascade_v23_champions.csv`
- `db/properties/cascade_v23_ranked.csv`
- `kb/seminars/cascade_seminar_2026_08_spec.md`

## Slide 6. 방법별 claim boundary

계산마다 말할 수 있는 문장이 달라요. UMA는 많은 구조와 상대 경향을 빠르게 보고, BVSE는 빈 격자에서 정적 경로를 보며, MLIP-MD는 확산 구간을 통과한 동역학을 보고, DFT는 전자상태와 최종 후보를 확인해요. 이 경계를 섞으면 빠른 계산의 숫자가 곧바로 열역학이나 실험 물성처럼 보이는 문제가 생깁니다.

Sources:
- `kb/seminars/cascade_seminar_2026_08_spec.md`
- `kb/results/mlip_md_diffusive_gate_2026_08_01.md`

## Slide 7. MLIP의 역할과 한계

MLIP의 장점은 DFT보다 훨씬 많은 configuration을 탐색할 수 있다는 점이에요. 하지만 charge state를 직접 선택할 수 없고, 결합이 끊기거나 Li가 추출되는 사건의 에너지 의미를 자동으로 보장하지 않아요. 그래서 여기서는 구조 탐색과 상대 screening에 쓰고, 반응이나 최종 adsorption 해석은 DFT 단계로 넘깁니다.

Sources:
- `kb/results/mlip_md_diffusive_gate_2026_08_01.md`
- `kb/projects/sdcp_phaseB_direction_2026_08_06.md`

## Slide 8. 전자구조는 guardrail

comp1과 Cl-rich modelc의 fixed-occupation gap은 각각 2.066과 2.099 eV로 차이가 0.033 eV예요. PBE 절대값을 실험 gap처럼 주장하려는 게 아니라, 같은 protocol에서 변화가 작다는 걸 보는 겁니다. 따라서 electronic axis가 주된 설계 신호라기보다, 구조·결함 쪽으로 시선을 옮기는 guardrail 역할을 해요.

Sources:
- `db/properties/electronic.json`
- `db/properties/canonical_registry.json`

## Slide 9. 구조 descriptor의 동기

Cl-rich 조성에는 Li vacancy와 4d-Cl antisite가 같이 들어가요. 정적 BVSE 채널은 오히려 줄고, MLIP-MD에서는 더 큰 Li motion이 보입니다. 이 차이는 disorder-sensitive descriptor를 선택할 이유는 되지만, composition과 defect population이 함께 바뀌었기 때문에 인과를 분리한 증거는 아니에요. 또 comp1에는 인용 가능한 multi-seed Ea가 없어서 비교 수송 향상을 확정하지 않습니다.

Sources:
- `db/properties/canonical_registry.json`
- `kb/results/mlip_md_diffusive_gate_2026_08_01.md`

## Slide 10. 문헌 screening 선례

Sendek 연구에서는 1만 종이 넘는 후보에 먼저 안정성·gap·전압 같은 싼 prerequisite gate를 적용하고, 40개의 측정 전도도로 학습한 classifier를 뒤에 썼어요. 중요한 점은 classifier보다 앞의 physics gate가 더 크게 후보를 줄였다는 거예요. 우리 47종과 데이터 크기가 같다는 뜻은 아니고, 작은 라벨에서는 grouped validation과 prospective test가 필요하다는 교훈만 가져옵니다.

Sources:
- `litdb/papers/sendek2017_ml_screening_12k_conductors.md`
- `litdb/papers/xiao2019_cathode_coating_screening.md`

## Slide 11. 다섯 gate의 계약

G1은 세 campaign-label champion의 평균 상대에너지, G2는 window 존재, G3는 host 이상의 oxidation onset, G4는 정적 BVSE proxy, G5는 softness와 ductility 순위예요. 여기서 G1은 47종 모두 통과해서 현재 pool에서는 gate power가 없고, G2의 네 탈락은 전부 G3에도 걸립니다. G4 두 cutoff는 heuristic이고, G5는 roster median이라 ranking-only예요.

Sources:
- `db/properties/cascade_screening_funnel.json`
- `db/properties/cascade_v23_ranked.csv`

## Slide 12. waterfall을 감사하기

47에서 43, 25, 11로 줄어드는 구간까지가 G4까지의 결과예요. 마지막 1은 G5 순위 cutoff가 만든 값이라 winner로 부르지 않습니다. 120개 gate 순서를 전부 바꿔도 최종 Boolean intersection은 같았지만, 중간 count와 어느 gate가 탈락시켰는지는 달라져요. 즉 waterfall 모양은 설명 방식이고, terminal set만 논리적으로 invariant합니다.

Sources:
- `db/properties/cascade_screening_funnel.json`

## Slide 13. oxidation과 pathway proxy의 trade-off

47종 snapshot에서 oxidation onset을 높인 여섯 후보가 모두 같은 G4 정적 경로 heuristic에서 멈췄어요. 이건 데이터셋 수준의 trade-off이고, M–O 결합이 Li blocking을 일으킨다는 인과 증명은 아닙니다. 그리고 BVSE는 conductivity가 아니에요. 다만 한 후보의 약점과 다른 후보의 강점을 조합해 볼 이유는 충분히 줍니다.

Sources:
- `db/properties/cascade_seminar_oxidation_transport_47.csv`
- `docs/figures/cascade/cascade_seminar_oxidation_transport_47.png`

## Slide 14. 왜 funnel이 endpoint가 아닌가

AND funnel은 한 축의 약점을 이유로 후보를 완전히 버려요. 그런데 oxidation은 좋고 pathway proxy는 약한 후보가 co-doping에서는 필요한 cathode-side half일 수 있어요. B2O3처럼 지표마다 방향이 다른 후보도 하나의 score로 좋다·나쁘다를 말하기 어렵습니다. 그래서 14축 구조를 유지하고, combination을 실제 계산하는 쪽으로 넘어갑니다.

Sources:
- `db/properties/cascade_seminar_scorecard_47.csv`
- `litdb/papers/zhu2020_air_stable_se_design_principles.md`

## Slide 15. co-doping v1 proxy

표의 +0.360 V는 실제 Cr2O3–HfO2 co-doped 구조 계산값이 아니에요. single-dopant의 reduction edge와 oxidation edge를 조합한 end-member proxy입니다. Cr oxide가 높은 oxidation edge를, HfO2가 낮은 reduction edge를 주는 조합이에요. 더구나 두 single-dopant champion이 모두 Li_24g라 site competition 위험이 있습니다. 구조를 만들기 전에는 chemistry가 검증된 게 아닙니다.

Sources:
- `db/properties/codoping_ml_v2.csv`
- `db/properties/codoping_ml_v2_meta.json`
- `tools/cascade/codoping_ml.py`

## Slide 16. co-doping 모델 감사

single-dopant score 공식을 다시 맞추는 stage 1은 R²가 0.9998로 높아요. 하지만 pair hypothesis에 들어가면 pair-LOOCV가 0.0892, dopant를 통째로 빼는 LODO와 L2DO는 음수가 됩니다. 지금은 1,081개 H0 가설이 있지만 실제 pair structure와 pair target은 0개예요. 따라서 predictor가 아니라 다음 계산을 정하는 hypothesis generator로만 씁니다.

Sources:
- `db/properties/codoping_ml_v2_meta.json`
- `tools/cascade/codoping_ml.py`

## Slide 17. 필요한 다음 라벨

다음 단계는 숫자 농도를 가정하는 게 아니라, explicit co-substituted structure를 만드는 거예요. x002, x005, x010은 nominal campaign label이므로 실제 stoichiometry를 먼저 닫아야 합니다. 각 pair에서 site, charge/Li-count, formation energy를 정하고 prospective holdout으로 검사해요. 모델이 맞으면 다음 구조 선택 효율이 좋아지고, 틀리면 complementarity 가설을 버리면 됩니다.

Sources:
- `db/properties/codoping_ml_v2_meta.json`
- `kb/seminars/cascade_seminar_2026_08_spec.md`

## Slide 18. 감사 ledger

이 표는 실패를 숨기지 않고 claim과 gate를 연결한 ledger예요. SDCP는 세 숫자를 분리해야 합니다. 9 meV는 site-pose 비교, −32/−26 meV는 old doped–neutral adsorption 비교, +0.336/+0.340 eV는 Li-transfer endpoint 비교예요. 마지막 값도 old protocol의 provisional endpoint라 v2 재검 전에는 반응 자유에너지나 barrier로 부르지 않습니다.

Sources:
- `kb/projects/sdcp_phaseB_direction_2026_08_06.md`
- `kb/results/sdcp_master_summary_2026_07_16.md`
- `db/properties/canonical_registry.json`

## Slide 19. 결론

결론은 winner가 아니라 세 가지 산출물이에요. 첫째, provenance가 분리된 47종 versioned snapshot. 둘째, heuristic임을 공개한 11종 G4 shortlist와 G5 ranking. 셋째, real pair label을 얻기 위한 acquisition plan입니다. 그리고 11개 감사 판정 중 9개는 철회했고, 하나는 hold, 하나는 provenance-open 상태로 값과 함께 표시합니다.

Sources:
- `db/properties/cascade_screening_funnel.json`
- `db/properties/codoping_ml_v2_meta.json`
- `db/properties/canonical_registry.json`

## Slide 20. 닫힌 루프의 다음 단계

처음의 loop로 돌아오면, 지금 위치는 screen에서 verify와 label acquisition으로 넘어가는 지점이에요. explicit pair structure를 만들고 UMA로 configuration space를 줄인 뒤, 필요한 후보만 DFT와 실험으로 확인합니다. 이후 새 라벨이 쌓이면 모델을 다시 학습해 다음 계산을 고르는 active-learning loop로 확장할 수 있어요.

Sources:
- `kb/seminars/cascade_seminar_2026_08_spec.md`
- `tools/cascade/codoping_ml.py`

## Slide 21. Appendix — DFT terms

질문이 나오면 DFT, exchange-correlation, U, k-point, fixed occupations를 이 표로 짧게 정의하면 돼요. 핵심은 모든 숫자에 method tag를 붙이고, 서로 다른 protocol의 절대값을 한 축에 섞지 않는다는 겁니다.

Sources:
- `db/properties/electronic.json`
- `kb/seminars/cascade_seminar_2026_08_spec.md`

## Slide 22. Appendix — property terms

window, oxidation onset, BVSE, elastic 지표가 무엇을 뜻하는지 묻는 질문용이에요. 각 항목은 서로 다른 물성을 보므로, 하나의 universal score로 합치는 순간 해석이 바뀐다는 점을 강조하면 됩니다.

Sources:
- `db/properties/cascade_screening_funnel.json`
- `db/properties/cascade_seminar_scorecard_47.csv`

## Slide 23. Appendix — protocol matrix

이 표는 method-to-claim 계약의 세부 버전이에요. 입력, 기준 구조, 허용 claim, 금지 claim을 함께 보고 답하면 됩니다. 특히 screen 값과 DFT case study를 같은 validation coverage처럼 말하지 않는 게 중요해요.

Sources:
- `kb/seminars/cascade_seminar_2026_08_spec.md`
- `db/properties/canonical_registry.json`

## Slide 24. Appendix — β gate

β는 MSD가 확산 구간인지 확인하는 지표예요. 0.8에서 1.2 사이가 아니면 cage rattling을 D로 잘못 맞출 수 있습니다. 판정은 600, 800, 1000 K와 2–50 ps 창을 사용하고, 절대 conductivity는 인용하지 않으며 비율도 multi-seed 판정일 때만 씁니다. β 자체가 특정 saddle을 알려주는 건 아니에요.

Sources:
- `kb/results/mlip_md_diffusive_gate_2026_08_01.md`
- `db/properties/canonical_registry.json`

## Slide 25. Appendix — 47-candidate axis map

후보별 전체 축을 묻는 질문에 쓰는 backup이에요. percentile과 theme 내부 geometric mean은 표시용 비교이고, theme를 가로지르는 universal score는 없습니다. missing은 0으로 채우지 않고 제외·flag 처리했고, air와 HSAB 관련 축은 아직 descriptive 또는 provisional입니다.

Sources:
- `db/properties/cascade_seminar_scorecard_47.csv`
- `docs/figures/cascade/cascade_seminar_scorecard_47.png`

## Slide 26. Appendix — defense Q&A

질문에는 먼저 한 문장으로 범위를 닫고, 필요할 때 숫자를 추가하세요. 특히 WO3는 winner가 아니라 G5 top rank, 2/47은 targeted DFT case study, co-doping은 explicit structure가 없는 hypothesis라는 세 문장을 먼저 기억하면 대부분의 과장을 막을 수 있어요.

Sources:
- `kb/seminars/cascade_seminar_2026_08_spec.md`
- `db/properties/codoping_ml_v2_meta.json`

## Slide 27. Appendix — harder questions

어려운 질문에서는 모르는 걸 분명히 말하는 게 답이에요. Ea는 Arrhenius slope이지 자동으로 특정 saddle이 아니고, UMA의 상대 geometry 활용과 charge-state 한계를 분리해야 합니다. 그리고 44종 provenance gap 때문에 273-slot campaign의 discovery rate를 계산할 수 없다고 명확히 답하면 됩니다.

Sources:
- `kb/results/mlip_md_diffusive_gate_2026_08_01.md`
- `kb/seminars/cascade_seminar_2026_08_spec.md`

## Slide 28. Appendix — ML numbers

모델 수치를 요구하면 stage 1과 stage 3을 분리하세요. 0.9998은 만든 공식을 다시 찾은 결과이고, pair prediction 성능은 0.0892입니다. 새로운 dopant를 통째로 빼면 R²가 음수라 일반화에 실패해요. 그래서 real pair structure와 prospective label이 다음 병목입니다.

Sources:
- `db/properties/codoping_ml_v2_meta.json`
- `tools/cascade/codoping_ml.py`

## Slide 29. Appendix — references

참고문헌은 로컬 litdb에 실제로 보유한 논문만 넣었어요. 발표에서는 숫자를 기억으로 옮기지 않고, digest와 figure crop이 있는 자료만 method와 함께 인용합니다.

Sources:
- `litdb/papers/sendek2017_ml_screening_12k_conductors.md`
- `litdb/papers/xiao2019_cathode_coating_screening.md`
- `litdb/papers/zhu2020_air_stable_se_design_principles.md`
- `litdb/papers/kahle2020_ht_aimd_screening.md`
- `litdb/papers/liyaru_gaf3_codoping_argyrodite.md`
