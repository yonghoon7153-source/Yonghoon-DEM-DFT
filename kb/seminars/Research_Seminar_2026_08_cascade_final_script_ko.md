# Research Seminar — Cascade final speaker script

> Deck: `Research_Seminar_2026_08_cascade_final.pptx`  
> Main: S1–S21 · Appendix: A1–A7 (S22–S28)

## S1. An audited screening cascade

오늘 발표는 특정 첨가제를 하나 골랐다는 이야기가 아니에요. LPSCl 치환 후보를 빠르게 줄이면서도 어떤 문장까지 허용되는지 계산 단계마다 제한하는 cascade를 보여드릴게요. 핵심 결과는 후보 하나보다, 버전이 고정된 47종 스냅샷과 11종 비교 집합, 그리고 다음 계산을 고르는 규칙이에요.

근거:

- `docs/cascade_pipeline_guide.md`
- `kb/seminars/cascade_seminar_2026_08_spec.md`

## S2. Why LPSCl needs a multi-axis screen

LPSCl은 전도도만 좋으면 끝나는 재료가 아니에요. 산화 안정성, Li·전해질·양극 계면, 접촉과 공정성이 동시에 걸려 있어요. 그래서 coating, 치환, 복합화, 공정 제어 중 어느 하나만으로 모든 문제를 해결하기 어렵고, 후보를 여러 축으로 동시에 보는 구조가 필요해요.

근거:

- `litdb/papers/sundar2025_oxide_coating_screening_lpscl.md`
- `litdb/figures/sundar2025_oxide_coating_screening_lpscl/figures.json`
- `docs/cascade_pipeline_guide.md`

## S3. The campaign unit is a run slot

여기서 273은 후보 물질 수가 아니에요. 수동으로 고른 91종에 x002, x005, x010이라는 세 campaign label을 붙인 273개 실행 슬롯이에요. 실제 조성 x는 아직 provenance가 닫히지 않았기 때문에, 이 라벨을 2·5·10%로 번역하지 않아요.

근거:

- `db/properties/cascade_seminar_pool_attrition_273_to_47.csv`
- `docs/reviews/cascade_db_ml_readiness_audit_2026_08_10.md`

## S4. Spend precision where it matters

Cascade는 계산을 많이 하는 방법이라기보다 비용을 배치하는 방법이에요. 문헌과 DB에서 후보를 만들고, UMA와 정적 proxy로 넓게 훑고, 물리 gate로 위험한 해석을 막은 뒤, 선택된 후보에만 DFT와 실험을 써요. 각 단계의 값에는 method, source, status가 같이 따라가야 해요.

근거:

- `docs/cascade_pipeline_guide.md`

## S5. 273 and 47 are different provenance units

273에서 물리 gate를 거쳐 47이 된 게 아니에요. 2026년 6월 25일에 versioned table로 들어온 건 oxide 37종과 fluoride 10종, 모두 141개 기록이에요. 나머지 44종은 canonical table에 들어오지 않았고, 전종별 실패 manifest가 없으므로 탈락이나 실패로 부르지 않아요. Post-hoc gate audit는 오른쪽의 47종에서 시작해요.

근거:

- `db/properties/cascade_seminar_pool_attrition_273_to_47.csv`
- `docs/reviews/cascade_db_ml_readiness_audit_2026_08_10.md`

## S6. The complete candidate cast

이 장은 순위표가 아니라 실제로 canonical snapshot에 들어온 47종 전체 명단이에요. 굵은 글씨는 post-hoc G1–G4 endpoint에 남은 11종이고, 십자가 표시는 targeted deep-DFT case 두 종이에요. 명단에 있다는 사실과 gate를 통과했다는 사실을 분리해서 보시면 돼요.

근거:

- `db/properties/cascade_seminar_scorecard_47.csv`
- `db/properties/cascade_v23_ranked.csv`

## S7. Evidence ladder

같은 숫자라도 계산 층위가 다르면 주장 강도가 달라져요. UMA는 같은 프로토콜 안의 상대적인 구조·에너지 탐색, BVSE는 정적 경로 geometry, DFT는 선택 후보의 matched validation, 실험은 최종 거동 확인에 써요. 위층의 결과를 아래층의 절대 물성처럼 말하지 않는 게 첫 번째 방어선이에요.

근거:

- `docs/cascade_pipeline_guide.md`
- `kb/methodology/terminology_register.md`

## S8. Fourteen axes do not share one evidence level

Webapp에는 산화, 환원, 전자 절연, 경로, 기계, 공기 안정성, 비용과 질량 등 14개 관점이 있어요. 하지만 이 축들은 계산·문헌·큐레이션이 섞여 있으므로 한 점수로 합쳐 winner를 만들지 않아요. 각 질문 안에서만 같은 축을 묶고, missing은 0점이 아니라 제외와 표시로 다뤄요.

근거:

- `db/properties/cascade_v23_themes.json`
- `webapp/templates/cascade.html`
- `docs/cascade_pipeline_guide.md`

## S9. Five gates ask different questions

G1은 host 대비 상대 안정성, G2는 window collapse, G3는 host oxidation onset, G4는 정적 Li-path proxy를 봐요. G4는 transport_norm과 blocking 두 조건을 함께 쓰지만 둘 다 heuristic이고, 특히 blocking 0.60에는 host나 문헌 anchor가 없어요. G5는 11종 안의 roster-relative mechanics ranking일 뿐 hard gate가 아니에요.

근거:

- `db/properties/cascade_screening_funnel.json`
- `docs/cascade_pipeline_guide.md`

## S10. The post-hoc funnel stops at 11

47종에서 G1은 아무도 제거하지 않고, G2와 G3를 거치면 25종, G4까지 적용하면 11종이 남아요. 이 11종을 비교용 endpoint로 보고하고, G5의 1종은 별표가 붙은 선호 정렬로만 남겨요. 이 funnel 자체가 문헌 기준을 뒤에서 매핑한 post-hoc audit라는 점도 같이 표시해요.

근거:

- `db/properties/cascade_screening_funnel.json`

## S11. Gate power is itself a result

G1은 47종 모두 통과해서 이 pool에서는 선택 압력이 없어요. G2가 단독으로 잡는 네 종은 전부 G3에서도 탈락하므로 unique kill은 0이에요. 이걸 숨기지 않고 gate가 vacuous 또는 redundant였다고 보고하면, 다음 버전에서 threshold와 데이터 수집을 어디서 바꿔야 하는지 알 수 있어요.

근거:

- `db/properties/cascade_screening_funnel.json`
- `docs/cascade_pipeline_guide.md`

## S12. Oxidation and pathway proxies trade off

Oxidation onset을 올리는 여섯 후보가 이 스냅샷에서는 모두 G4의 정적 pathway heuristic에서 멈춰요. 이건 dataset-level trade-off이지, M–O 결합이 Li blocking을 원인적으로 만든다는 증명은 아니에요. 따라서 보완성이 있는 후보를 co-doping 가설로 넘길 수는 있지만 자동으로 좋은 조합이라고 부르지는 않아요.

근거:

- `db/properties/cascade_seminar_oxidation_transport_47.csv`
- `db/properties/cascade_screening_funnel.json`

## S13. Pareto sets preserve complementarity

AND gate 하나만 따라가면 한 축이 강하고 다른 축이 약한 후보를 일찍 버릴 수 있어요. 그래서 11종 안에서도 축별로 non-dominated 후보를 따로 보여줘요. 이 Pareto 집합은 질문에 따라 달라지는 후보군이고, winner list가 아니에요.

근거:

- `db/properties/cascade_seminar_pareto_47.csv`
- `db/properties/cascade_seminar_scorecard_47.csv`

## S14. Deployment questions map to different axes

어떤 후보가 좋은지는 어디에 쓰려는지에 따라 달라져요. 고전압 양극 쪽은 산화 onset과 window, 수분 대응은 T11 정적 반응축과 Zhu 문헌 proxy·HSAB, 대량 적용은 qualitative cost tier와 질량을 봐요. 이 축들은 추가 gate가 아니라 후속 실험과 계산 우선순위를 정하는 descriptive evidence예요.

근거:

- `db/properties/cascade_v23_themes.json`
- `db/properties/cascade_air_axis_lit_vs_tier.csv`
- `db/properties/cascade_seminar_scorecard_47.csv`
- `litdb/papers/zhu2020_air_stable_se_design_principles.md`

## S15. Four candidates illustrate the decision shift

LiF는 정적 interface 축에서 안정적으로 보이지만 kinetics나 coating lifetime까지 말할 수는 없어요. MgO와 CaO는 비용·질량 측면이 좋지만 H2S나 LPSCl 반응축에서 서로 다른 부담이 보여요. Cu2O는 문헌 수분 proxy는 좋아도 G3와 interface 축이 불리해요. 결국 한 후보의 장점은 적용 조건과 함께 읽어야 해요.

근거:

- `db/properties/cascade_stability_axes.csv`
- `db/properties/cascade_v23_themes.json`
- `db/properties/cascade_seminar_scorecard_47.csv`

## S16. Order invariance is not threshold validation

5개 gate의 120개 순서를 전부 바꿔도 최종 Boolean intersection은 같았어요. 하지만 중간 숫자와 어떤 gate가 누구를 죽였는지는 달라져요. 그리고 순서 불변성이 threshold 자체를 물리적으로 검증해 주는 건 아니므로, 보고 endpoint는 여전히 heuristic G4까지의 11종으로 제한해요.

근거:

- `db/properties/cascade_screening_funnel.json`
- `docs/cascade_pipeline_guide.md`

## S17. Trust boundary

현재 지지되는 건 gate pass·fail, 같은 프로토콜 안의 상대 비교, trade-off, gate-order audit예요. 반대로 UMA 절대 열역학, BVSE conductivity, degenerate group 내부 순위, G5 winner는 지지하지 않아요. Full gate로 아직 비어 있는 건 interface reaction, electronic insulation, 그리고 실제 doped-LPSCl moisture response예요.

근거:

- `docs/cascade_pipeline_guide.md`
- `docs/reviews/cascade_db_ml_readiness_audit_2026_08_10.md`

## S18. Retractions became executable rules

단일시드 1.33배 전도도는 멀티시드 판정으로, 비확산 MSD fit은 beta gate로, DOS threshold gap은 fixed-occupation eigenvalue로 바꿨어요. 공기 안정성의 raw HSAB grade는 Zhu 문헌축과 비교해 한 방향 bias가 보여 non-gating curated 축으로만 남겼어요. 실패한 주장을 숨긴 게 아니라 rule과 exclusion으로 바꾼 게 이 pipeline의 신뢰성 부분이에요.

근거:

- `db/properties/canonical_registry.json`
- `db/properties/b2o3_vs_lpscl16_conductivity.csv`
- `db/properties/cascade_air_axis_lit_vs_tier.csv`

## S19. Three coverage counts are parallel

47은 relative screen 수, 11은 post-hoc G1–G4 endpoint, 2는 targeted deep-DFT case 수예요. 이 세 숫자는 순차 funnel이 아니고, DFT 두 건도 11종에서 뽑힌 validation set이 아니에요. B2O3는 G4, Nd2O3는 G3에서 멈추므로 direct comparison을 하려면 앞으로 동일 구조·셀·k-mesh·reference·자기 프로토콜을 맞춰야 해요.

근거:

- `db/properties/cascade_seminar_scorecard_47.csv`
- `db/properties/electronic.json`
- `webapp/data.py`

## S20. Co-doping ML is a hypothesis engine

Cr2O3–HfO2는 v1 heuristic에서는 1위였지만 v2 ML에서는 8위예요. +0.360 V도 explicit pair 계산값이 아니라 두 single-dopant endpoint로 만든 proxy gain이에요. 두 single-dopant champion이 모두 Li_24g라 site competition도 열려 있고, pair structure·DFT·실험 label은 아직 0개예요. 그래서 현재 역할은 hypothesis ordering이에요.

근거:

- `db/properties/cascade_v23_synergy_pairs.csv`
- `db/properties/codoping_ml_v2.csv`
- `db/properties/codoping_ml_v2_meta.json`
- `docs/cascade_ml_integration_guide.md`

## S21. The next cascade learns what to calculate

다음 단계의 ML은 47개 평균값만으로 winner를 예측하는 모델이 아니에요. 불확실성, Pareto gain, chemistry diversity, gate boundary를 합쳐 다음 explicit configuration을 고르는 acquisition model이에요. 계산과 실험이 새 label을 만들고, versioned DB가 다시 proposal로 돌아오는 closed loop를 목표로 해요.

근거:

- `docs/cascade_ml_integration_guide.md`
- `litdb/papers/sendek2017_ml_screening_12k_conductors.md`
- `litdb/papers/kim2025_conductive_agent_se_coating_cathode.md`

## S22. Terminology and symbols

질문이 나오면 우선 단위를 맞춰야 해요. transport_norm은 conductivity가 아니고, DeltaG_hyd 문헌축은 same-cation binary sulfide proxy예요. x002·x005·x010은 실제 농도가 아니라 campaign label이고, cost tier는 시세가 아닌 qualitative cation tier에 fluoride surcharge가 붙은 값이에요.

근거:

- `kb/methodology/terminology_register.md`
- `db/properties/cascade_v23_themes.json`

## S23. Protocol matrix

이 표는 방법별로 무엇을 말해도 되는지 방어하는 장이에요. MLIP-MD는 canonical temperature와 MSD window에서 beta-gated multiseed Ea까지만, DFT는 matched protocol의 선택 후보 검증까지만 말해요. 외부 문헌값은 방향성 cross-check이고 내부 절대값과 섞지 않아요.

근거:

- `docs/cascade_pipeline_guide.md`
- `AGENTS.md`
- `db/properties/electronic.json`

## S24. The 47-species scorecard

전체 후보를 한 번에 물어보면 이 heatmap을 보여주면 돼요. 색은 pool 내부의 favorable percentile이고, 오른쪽은 first-stop gate예요. 절대 물성이나 하나의 composite score가 아니므로 색이 진하다고 winner라고 부르지 않아요.

근거:

- `db/properties/cascade_seminar_scorecard_47.csv`
- `docs/figures/cascade/cascade_seminar_scorecard_47.png`

## S25. Defense Q&A: cascade

이 장은 provenance와 gate 해석에 대한 짧은 답을 모아둔 backup이에요. 가장 중요한 답은 47이 273의 물리적 survivor가 아니라는 것, G4가 heuristic이라는 것, BVSE failure가 낮은 conductivity를 증명하지 않는다는 것이에요. 질문이 길어지면 관련 본문 장으로 돌아가면 돼요.

근거:

- `docs/reviews/cascade_db_ml_readiness_audit_2026_08_10.md`
- `db/properties/cascade_screening_funnel.json`

## S26. Defense Q&A: validation and ML

DFT coverage는 2/47이고, 47개 dopant 평균값은 일반적인 discovery model을 학습시키기에는 부족해요. Stage 1의 높은 LOOCV는 구성한 score를 복원한 결과이고, 별도의 pair model은 LODO와 L2DO에서 음수예요. 실제 co-doped 구조와 prospective holdout이 생긴 뒤에야 predictive라고 부를 수 있어요.

근거:

- `db/properties/codoping_ml_v2_meta.json`
- `docs/cascade_ml_integration_guide.md`

## S27. Data source ledger

이 장에는 발표 숫자를 다시 만들 때 직접 여는 정본 데이터 파일만 모았어요. 특히 attrition, gate funnel, scorecard, stability axes, co-doping v1·v2를 분리해 두었어요. Radar source는 origin commit `9ee411a3`에서 재현 가능하지만, 최종본은 수치를 직접 감사하기 쉬운 canonical 표·카드를 선택했어요.

근거:

- `db/properties/`
- `docs/cascade_pipeline_guide.md`

## S28. Method and audit source ledger

마지막 장은 수치보다 해석 규칙과 문헌 역할을 추적하는 파일들이에요. Pipeline guide, ML guide, DB readiness audit, terminology register, 그리고 local litdb digest를 기준으로 문장을 방어해요. 발표 후 수정이 생기면 이 원장과 speaker notes의 Sources 블록을 같이 갱신하면 돼요.

근거:

- `docs/`
- `kb/methodology/terminology_register.md`
- `litdb/papers/`
