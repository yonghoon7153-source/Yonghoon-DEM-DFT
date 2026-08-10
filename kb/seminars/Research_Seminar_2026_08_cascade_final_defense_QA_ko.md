# Research Seminar — Cascade Defense Q&A

대상 덱: `Research_Seminar_2026_08_cascade_final.pptx`  
원칙: 첫 문장으로 결론을 말하고, 필요할 때만 두 번째 문단의 근거까지 확장한다.

## 1. 데이터 계보

### Q1. 273개 계산에서 47종만 살아남은 건가?

아니요. **273은 91종 × 3개 nominal campaign label의 실행 슬롯 수이고, 47은 2026-06-25에 versioning된 O/F 스냅샷의 종 수**예요.

47종은 37개 oxide와 10개 fluoride로 이루어져 있고 141개 기록을 가집니다. 나머지 44종은 canonical table에 수집되지 않았으며, 전종별 실패 manifest가 없으므로 물리적 탈락이나 계산 실패로 분류하지 않습니다. 발표에서는 273과 47을 순차 funnel이 아닌 평행한 provenance 단위로 표시합니다.  
관련 슬라이드: S3, S5, A4.

### Q2. 나머지 44종은 왜 빠졌나?

현재 답은 **모른다**가 맞아요. Versioned table에 들어오지 않았고, 항목별 원인을 추적할 raw manifest가 저장소에 없습니다.

As₂S₃ × 3의 `n_structures = 0`만 개별적으로 문서화돼 있습니다. 이 공백 때문에 273-slot campaign의 discovery rate나 성공률을 주장하지 않습니다.  
관련 슬라이드: S5, A4.

### Q3. x002, x005, x010은 각각 2, 5, 10%인가?

아니요. **현재는 nominal campaign label**로만 취급합니다.

저장소의 농도 metadata가 서로 충돌해 실제 stoichiometric x가 닫히지 않았습니다. 따라서 농도 의존성이나 dose robustness라는 표현 대신 “세 campaign label 사이의 정적 proxy 변화”라고 말합니다.  
관련 슬라이드: S3, S14, A1.

### Q4. 왜 oxide와 fluoride만 들어 있는가? 선택 편향 아닌가?

맞아요. **현재 47종은 O/F 중심의 versioned snapshot이며 전체 91종을 대표하지 않습니다.**

그래서 후보 분포의 일반화, 계열별 성공률, 발견 확률을 주장하지 않습니다. 나머지 계열의 raw 결과를 회수해 동일 schema로 수집하는 것이 먼저입니다.  
관련 슬라이드: S5, S6.

### Q5. 47종이 high-throughput discovery pool이라고 부를 만큼 큰가?

아니요. **Human-curated, host-specific composition-family scan**이라고 부르는 게 정확해요.

47종은 물리 축과 gate 동작을 시험하고 다음 configuration label을 설계하는 데는 유용하지만, 광범위한 화학공간 discovery model의 학습셋으로는 작고 편향돼 있습니다.  
관련 슬라이드: S6, S19, A5.

## 2. Gate와 물리 해석

### Q6. G1이 47/47 통과면 왜 유지하나?

**이 pool에서 selection pressure가 0이었다는 감사 결과를 남기기 위해서**예요.

Gate를 지우면 다음 데이터 버전에서 선택 압력이 생겼는지 비교할 수 없습니다. 대신 G1이 안정성을 보편적으로 증명한 것처럼 해석하지 않습니다.  
관련 슬라이드: S9–S11.

### Q7. G2의 unique kill이 0이면 쓸모없는 gate 아닌가?

현재 pool에서는 **G3와 중복**이에요. 하지만 이 중복 자체를 기록하는 게 중요합니다.

CoO, Fe₂O₃, MnO, NiO 네 종은 G2와 G3를 함께 실패합니다. “late-TM chemistry가 원인”이라고 단정하지 않고, 같은 네 종이 두 조건을 동시에 실패했다고만 말합니다.  
관련 슬라이드: S11.

### Q8. 왜 최종 1종이 아니라 11종에서 결론을 멈추나?

**G1–G4의 11종을 비교용 endpoint로 보고하고, G5는 ranking-only로 취급하기 때문**이에요.

G4도 `transport_norm > 0.30`과 `blocking < 0.60`을 쓰는 heuristic이고, 특히 blocking cutoff에는 host·문헌 anchor가 없습니다. G5는 roster median에 따른 기계축 선호 정렬이므로 G5 1위를 discovered winner로 부르지 않습니다.  
관련 슬라이드: S9, S10, A4.

### Q9. BVSE에서 탈락하면 실제 conductivity가 낮다는 뜻인가?

아니요. **정적 경로 geometry의 위험 신호**일 뿐이에요.

BVSE는 D, σ, Ea를 계산하지 않습니다. 실제 수송 판정에는 canonical protocol의 multiseed MLIP-MD 또는 실험이 필요합니다.  
관련 슬라이드: S7, S9, A2.

### Q10. 산화 안정성과 Li pathway trade-off가 원인관계를 보여주나?

아니요. **이 47종 스냅샷에서 관찰된 dataset-level 동시 패턴**이에요.

산화 onset을 높이는 여섯 후보가 모두 G4 정적 proxy에서 멈추지만, M–O 결합이 Li blocking을 유발했다는 인과 증거는 없습니다. 명시적인 구조·결함·조성 비교가 후속 검증입니다.  
관련 슬라이드: S12.

### Q11. Gate 순서 120개에서 결과가 같으면 threshold도 검증된 것 아닌가?

아니요. **Boolean intersection의 순서 불변성만 확인한 것**이에요.

중간 waterfall과 kill attribution은 달라지고, threshold의 물리적 정당성은 별개입니다. 그래서 G4의 heuristic 표기를 유지합니다.  
관련 슬라이드: S16.

### Q12. H₂O/air stability 축은 왜 gate가 아닌가?

**직접적인 doped-LPSCl 수분 안정성 label이 없기 때문**이에요.

T11은 0 K pseudo-binary H₂O→H₂S thermodynamic driving force이고 kinetics가 아닙니다. Zhu 축은 same-cation binary-sulfide 문헌 proxy로 35/47만 존재하며, raw HSAB grade는 문헌 대비 한 방향 under-rating을 보였습니다. 따라서 수분 관련 축은 follow-up prioritization에만 씁니다.  
관련 슬라이드: S14, S15, S18, A4.

### Q13. Missing을 0으로 넣지 않으면 비교가 불편하지 않나?

불편해도 **missing은 0도 아니고 실패도 아닙니다.**

0으로 채우면 실제로 계산된 중립값처럼 해석돼 rank와 ML label을 오염시킵니다. 현재는 제외와 상태 표시를 유지하고, 결측을 채울 계산 자체를 acquisition 대상으로 삼습니다.  
관련 슬라이드: S8, A1.

## 3. DFT 검증과 co-doping ML

### Q14. 47종이 모두 DFT로 검증됐나?

아니요. **Targeted deep-DFT case는 2/47**이에요.

B₂O₃와 Nd₂O₃는 각각 G4와 G3에서 멈추므로 11종의 downstream validation set도 아닙니다. 47, 11, 2는 평행한 coverage 기록입니다.  
관련 슬라이드: S19, A5.

### Q15. Cr₂O₃–HfO₂의 +0.360 V는 실제 co-doping 계산값인가?

아니요. **Single-dopant endpoint를 조합한 v1 proxy gain**이에요.

Explicit co-doped structure, site assignment, charge/Li-count closure, formation energy, pair DFT·실험 label은 아직 없습니다. 두 single-dopant champion이 모두 `Li_24g`라 site competition도 열려 있습니다.  
관련 슬라이드: S20.

### Q16. Cr₂O₃–HfO₂가 최상 pair인가?

아니요. **v1 heuristic에서는 #1, v2 ML에서는 #8**이에요.

이 순위 변화 자체가 지금 모델이 chemistry truth를 확정하지 못한다는 신호입니다. 따라서 “model-prioritized, uncomputed hypothesis”로만 부릅니다.  
관련 슬라이드: S20.

### Q17. 47개 row로 ML을 할 수 없다는 뜻인가?

일반적인 discovery predictor는 어렵지만, **gate별 surrogate와 acquisition prior**는 만들 수 있어요.

다음 학습 단위는 dopant 평균 한 행이 아니라 site·농도·defect configuration과 protocol이 붙은 구조 label이어야 합니다.  
관련 슬라이드: S20, S21, A5.

### Q18. LOOCV R² = 0.9998이면 모델이 잘 된 것 아닌가?

아니요. **Stage 1은 입력으로 구성한 score 식을 같은 입력에서 다시 복원한 결과**예요.

별도의 pair model은 pair-LOOCV R² = 0.0892, LODO = −0.1805, L2DO = −0.2548로 무너집니다. Dopant identity를 새로 떼어내는 grouped split이 실제 일반화 한계를 더 잘 보여줍니다.  
관련 슬라이드: A5.

### Q19. 다음 ML 단계는 무엇인가?

**Uncertainty + Pareto gain + chemical diversity + gate-boundary risk로 다음 구조를 고르는 acquisition loop**예요.

Explicit pair 구조를 만들고, 동일 프로토콜 UMA/DFT label을 추가하고, prospective holdout을 고정한 뒤 재학습합니다.  
관련 슬라이드: S21.

### Q20. 언제 predictive model이라고 부를 수 있나?

**실제 pair 구조와 pair-property label이 생기고, grouped CV와 frozen prospective holdout을 통과한 뒤**예요.

그전에는 hypothesis generator 또는 acquisition model이라고 부릅니다.  
관련 슬라이드: S20, S21, A5.

## 4. 발표의 기여와 한계

### Q21. 기존 AI screening 논문 대비 이 연구의 이점은 무엇인가?

**후보 생성, 물리 gate, 값의 provenance, 철회 규칙을 같은 decision loop 안에 넣었다는 점**이에요.

현재 데이터 규모와 DFT coverage는 작지만, missing과 protocol drift를 숨기지 않고 어떤 계산을 다음 label로 만들지 명시합니다. 큰 모델보다 감사 가능한 label acquisition을 먼저 설계한 접근입니다.

### Q22. 결국 winner를 못 찾았으면 cascade가 실패한 것 아닌가?

아니요. **검증 비용을 어디에 쓰지 말아야 하는지와 무엇을 더 측정해야 하는지를 정한 것이 현재 단계의 결과**예요.

정직한 산출물은 47종 versioned snapshot, heuristic 11종 endpoint, 후보별 trade-off, 그리고 다음 구조 label 계획입니다.

### Q23. 실패와 철회가 많으면 데이터를 믿기 어려운 것 아닌가?

반대로 **철회를 실행 가능한 gate와 exclusion으로 고정했기 때문에 이후 버전이 같은 오류를 반복하지 않아요.**

단일시드 비율, 비확산 MSD, DOS-threshold gap, air proxy bias가 각각 프로토콜 규칙으로 바뀌었습니다.  
관련 슬라이드: S18.

### Q24. 한 문장으로 결론을 말하면?

**이 연구는 winner를 선언한 것이 아니라, LPSCl 치환 후보를 감사 가능하게 줄이고 다음 계산을 고르는 cascade를 만든 것**이에요.

## 정본 근거

- `db/properties/cascade_seminar_pool_attrition_273_to_47.csv`
- `db/properties/cascade_screening_funnel.json`
- `db/properties/cascade_seminar_scorecard_47.csv`
- `db/properties/cascade_stability_axes.csv`
- `db/properties/cascade_v23_themes.json`
- `db/properties/cascade_v23_synergy_pairs.csv`
- `db/properties/codoping_ml_v2.csv`
- `db/properties/codoping_ml_v2_meta.json`
- `docs/cascade_pipeline_guide.md`
- `docs/cascade_ml_integration_guide.md`
- `docs/reviews/cascade_db_ml_readiness_audit_2026_08_10.md`

