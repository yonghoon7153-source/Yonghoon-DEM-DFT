# Research Seminar — Slide Source Ledger

대상 덱: `Research_Seminar_2026_08_cascade_final.pptx`  
구성: 본문 S1–S21, 부록 A1–A7, 총 28장

이 표는 각 슬라이드의 비자명한 주장과 시각자료를 어느 정본에서 확인할지 지정한다. PPT notes에도 같은 경로가 `[Sources]` 블록으로 들어 있다.

| Slide | 핵심 내용 | 정본·근거 |
|---|---|---|
| S1 | 발표 범위와 cascade 질문 | `docs/cascade_pipeline_guide.md`; `kb/seminars/cascade_seminar_2026_08_spec.md` |
| S2 | sulfide SE의 계면 문제와 다중 해결 축 | `litdb/papers/sundar2025_oxide_coating_screening_lpscl.md`; `litdb/figures/sundar2025_oxide_coating_screening_lpscl/figures.json` |
| S3 | 91종 × 3 nominal labels = 273 slots | `db/properties/cascade_seminar_pool_attrition_273_to_47.csv`; `docs/reviews/cascade_db_ml_readiness_audit_2026_08_10.md` |
| S4 | multi-axis cascade 구조 | `docs/cascade_pipeline_guide.md`; `docs/cascade_ml_integration_guide.md` |
| S5 | 273과 47의 provenance 분리 | `db/properties/cascade_seminar_pool_attrition_273_to_47.csv`; `docs/reviews/cascade_db_ml_readiness_audit_2026_08_10.md` |
| S6 | 47종 전체 roster, G4 11, DFT 2 | `db/properties/cascade_seminar_scorecard_47.csv`; `db/properties/cascade_v23_ranked.csv`; `webapp/data.py` |
| S7 | L0–L3 evidence ladder | `docs/cascade_pipeline_guide.md`; `kb/methodology/terminology_register.md` |
| S8 | 14-axis map, descriptive/decision 구분 | `db/properties/cascade_v23_themes.json`; `webapp/templates/cascade.html`; `docs/cascade_pipeline_guide.md` |
| S9 | G1–G5 정의와 상태 | `db/properties/cascade_screening_funnel.json`; `docs/cascade_pipeline_guide.md` |
| S10 | 47→43→25→11 post-hoc funnel | `db/properties/cascade_screening_funnel.json` |
| S11 | first-stop, unique-kill, G2/G3 중복 | `db/properties/cascade_screening_funnel.json`; `docs/cascade_pipeline_guide.md` |
| S12 | oxidation–pathway dataset pattern | `db/properties/cascade_seminar_oxidation_transport_47.csv`; `db/properties/cascade_screening_funnel.json` |
| S13 | conditional Pareto view | `db/properties/cascade_seminar_pareto_47.csv`; `db/properties/cascade_seminar_scorecard_47.csv` |
| S14 | high-voltage, moisture, cost/light, label-stability 질문 | `db/properties/cascade_v23_themes.json`; `db/properties/cascade_air_axis_lit_vs_tier.csv`; `db/properties/cascade_seminar_scorecard_47.csv`; `litdb/papers/zhu2020_air_stable_se_design_principles.md` |
| S15 | LiF/MgO/CaO/Cu₂O decision profiles | `db/properties/cascade_stability_axes.csv`; `db/properties/cascade_v23_themes.json`; `db/properties/cascade_seminar_scorecard_47.csv` |
| S16 | 120 gate-order permutations | `db/properties/cascade_screening_funnel.json`; `docs/cascade_pipeline_guide.md` |
| S17 | 현재 trust boundary와 missing gate | `docs/cascade_pipeline_guide.md`; `docs/reviews/cascade_db_ml_readiness_audit_2026_08_10.md` |
| S18 | 철회·보류·provenance flag ledger | `db/properties/canonical_registry.json`; `db/properties/b2o3_vs_lpscl16_conductivity.csv`; `db/properties/cascade_air_axis_lit_vs_tier.csv` |
| S19 | targeted DFT 2/47와 비교 계약 | `db/properties/cascade_seminar_scorecard_47.csv`; `db/properties/electronic.json`; `webapp/data.py` |
| S20 | Cr₂O₃–HfO₂ v1 #1, v2 #8, +0.360 V proxy | `db/properties/cascade_v23_synergy_pairs.csv`; `db/properties/codoping_ml_v2.csv`; `db/properties/codoping_ml_v2_meta.json`; `docs/cascade_ml_integration_guide.md` |
| S21 | uncertainty-driven label acquisition loop | `docs/cascade_ml_integration_guide.md`; `litdb/papers/sendek2017_ml_screening_12k_conductors.md`; `litdb/papers/kim2025_conductive_agent_se_coating_cathode.md` |
| A1 | 용어·기호 규약 | `kb/methodology/terminology_register.md`; `db/properties/cascade_v23_themes.json` |
| A2 | protocol 및 claim boundary | `docs/cascade_pipeline_guide.md`; `AGENTS.md`; `db/properties/electronic.json` |
| A3 | 47종 heatmap | `db/properties/cascade_seminar_scorecard_47.csv`; `docs/figures/cascade/cascade_seminar_scorecard_47.png` |
| A4 | provenance·gate·air Defense Q&A | `docs/reviews/cascade_db_ml_readiness_audit_2026_08_10.md`; `db/properties/cascade_screening_funnel.json`; `db/properties/cascade_air_axis_lit_vs_tier.csv` |
| A5 | DFT coverage·co-doping·ML Defense Q&A | `db/properties/codoping_ml_v2_meta.json`; `docs/cascade_ml_integration_guide.md`; `webapp/data.py` |
| A6 | canonical data ledger | `db/properties/cascade_seminar_scorecard_47.csv`; `db/properties/cascade_v23_ranked.csv`; `db/properties/cascade_v23_champions.csv`; `db/properties/cascade_v23_litransport.csv`; `db/properties/oxidation_stability_cascade.csv`; `db/properties/cascade_v23_themes.json`; `db/properties/cascade_stability_axes.csv` |
| A7 | methods·audit·literature ledger | `docs/cascade_pipeline_guide.md`; `docs/cascade_ml_integration_guide.md`; `docs/reviews/cascade_db_ml_readiness_audit_2026_08_10.md`; `db/properties/cascade_screening_funnel.json`; `db/properties/canonical_registry.json`; `litdb/INDEX.md` |

## 재현성 메모

- S15와 S20에서 이전 draft의 radar 그림은 제거했다. 원자료·생성기·PNG는 origin commit `9ee411a3`의 `cascade_radar_axes_origin.csv`, `fig_cascade_radar.py`, `cascade_radar_*.png`로 재현 가능하다. 다만 최종본은 후보별 수치를 화면에서 바로 감사할 수 있는 canonical DB 표·카드를 선택했고, radar 복원은 발표 구성상의 선택 사항으로 남겼다.
- S15는 실제 canonical CSV에서 읽을 수 있는 후보별 decision profile로 교체했다.
- S20은 v1 heuristic과 v2 ML 순위를 분리해 표시하고, +0.360 V를 pair 계산값이 아닌 constructed proxy로 표기했다.
- 외부 논문 그림은 해당 litdb figure 폴더의 `figures.json`과 crop을 함께 확인한 경우만 사용한다.

## 발표 전 빠른 검증

1. `273`, `47`, `141`이 같은 funnel 화살표로 연결되지 않았는지 확인한다.
2. `x002/x005/x010`이 숫자 농도로 번역되지 않았는지 확인한다.
3. G4에 `heuristic`, G5에 `ranking-only`가 보이는지 확인한다.
4. 47/11/2가 평행 coverage로 설명되는지 확인한다.
5. H₂O·air 축이 doped-LPSCl 직접 안정성으로 표현되지 않았는지 확인한다.
6. Cr₂O₃–HfO₂가 `v1 #1 → v2 #8, uncomputed`로 표시되는지 확인한다.
7. 모든 비자명 claim의 notes 끝에 `[Sources]`가 있는지 확인한다.
