# Research Seminar — 용어·기호 규약

대상 덱: `Research_Seminar_2026_08_cascade_final.pptx`

이 문서는 발표·대본·질의응답에서 같은 단어를 같은 뜻으로 쓰기 위한 규약이다. 화면의 그림 라벨과 캡션은 영어를 유지한다.

## 1. 데이터 계보

| 용어 | 발표에서의 뜻 | 금지 표현 |
|---|---|---|
| manually curated roster | 사람이 정한 91종 후보 목록 | 전 공간을 탐색한 후보군 |
| run slot | 화합물 1종과 nominal campaign label 1개의 실행 단위 | 독립 화합물 1종 |
| 273 attempted run slots | 91종 × 3개 nominal label | 273종, 273개 완결 DFT 계산 |
| versioned canonical snapshot | 2026-06-25에 저장된 47종 O/F 표, 141행 | 273에서 물리 gate로 살아남은 47종 |
| x002 / x005 / x010 | 조성이 검증되기 전의 nominal campaign label | x=0.02/0.05/0.10 또는 2/5/10 at% |
| missing | 값이 없거나 canonical table에 미수집된 상태 | 0, 실패, 열등 후보 |
| candidate landscape | 47종의 현재 비교 가능한 범위 | 완전한 chemical-space map |

핵심 문장: **273과 47은 서로 다른 provenance 단위이며 순차 funnel이 아니다.**

## 2. 에너지·전압·수송 기호

| 기호 | 정의 | 주장 범위 |
|---|---|---|
| ΔE | 해당 표에 명시된 기준에 대한 상대 에너지 | 절대 형성에너지로 확대 금지 |
| V_ox | oxidation-side grand-potential-derived voltage | MP-derived 후처리값 |
| V_red | reduction-side grand-potential-derived voltage | MP-derived 후처리값 |
| window | V_ox − V_red | 실제 전지 안정창과 동일시 금지 |
| transport_norm | 47종 내부에서 정규화한 static BVSE transport proxy | D, σ, Ea가 아님 |
| blocking | static pathway의 inherited blocking proxy | 실험적 차단율이 아님 |
| BVSE | bond-valence 기반 빈 격자 경로 proxy | 동역학·전도도 계산이 아님 |
| β | MSD ∝ t^β의 확산 구간 진단값 | 특정 saddle/site의 직접 증거가 아님 |
| Ea | β-gated, 600/800/1000 K Arrhenius fit의 활성화에너지 | 단일시드·비표준 온도 fit 인용 금지 |
| σ | Nernst–Einstein, Haven=1 추정 | 절대값 인용 금지; 비율도 멀티시드만 |

## 3. G1–G5 gate

| Gate | 현재 구현·의미 | 상태 |
|---|---|---|
| G1 | 세 nominal-label champion의 평균 UMA-relative ΔE < 0 | 47/47 통과, 현재 pool에서는 vacuous |
| G2 | window ≥ 0.05 V | G3와 중복되어 unique kill=0 |
| G3 | V_ox ≥ 2.14 V | host-anchored hard comparison gate |
| G4 | transport_norm > 0.30 AND blocking < 0.60 | static heuristic, 특히 blocking cut은 host/literature anchor 없음 |
| G5 | E ≤ 46.9 GPa AND G/B ≤ 0.78 | roster-median 기반 ranking-only |

발표 endpoint는 **47 → 43 → 25 → 11 through G4**다. G5의 1종은 winner가 아니라 11종 안의 선호 정렬이다.

| 용어 | 뜻 |
|---|---|
| first-stop | 후보가 처음 멈춘 gate |
| unique kill | 다른 gate는 통과하면서 해당 gate만 실패한 후보 |
| post-hoc funnel | 기존 47종 표를 나중에 명시적 gate로 재표현한 감사 뷰 |
| G1–G4 endpoint | 비교를 위해 보고하는 11종 집합; G4 heuristic 표시는 유지 |
| order invariance | G1–G5 Boolean intersection이 120개 순열에서 동일함 |

Order invariance는 threshold의 물리적 정당성을 검증하지 않는다.

## 4. 수분·공기·비용 축

| 축 | 정확한 뜻 | 금지 해석 |
|---|---|---|
| T11 ΔE_H2S | 0 K pseudo-binary H₂O/H₂S thermodynamic driving-force 축 | kinetics, 수명, host 대비 개선 |
| ΔG_hyd,MS,lit | [Zhu20] same-cation binary-sulfide 문헌 proxy; 35/47만 존재 | doped-LPSCl coating의 직접 공기 안정성 |
| raw HSAB grade | cation HSAB 기반 curated grade | 정량 수분 안정성 또는 hard gate |
| cost tier | qualitative cation tier 1–5 + fluoride surcharge 0.5 | 시장가격, 원/kg 비용 |
| lightweight | formula mass/cation 기반 정렬 | 전극 수준 gravimetric benefit |
| label stability | 세 nominal label에서 static proxy가 얼마나 유지되는지 | 실제 농도 내성 |

Air/H₂O, cost, mass, label-stability 축은 **deployment question을 고르는 descriptive view**이며 추가 rejection gate가 아니다.

## 5. 근거 태그

| 태그 | 뜻 |
|---|---|
| UMA-relative | 같은 UMA protocol 안의 상대 score; 절대 DFT 에너지 아님 |
| MP-derived | Materials Project 원자료를 우리 grand-potential 규약으로 후처리 |
| static proxy | BVSE·pathway처럼 dynamics가 없는 구조 지표 |
| literature | 논문에서 소환한 값; 우리 계산값과 혼합 금지 |
| curated | 사람이 부여한 비용·HSAB 등급 |
| targeted DFT | 선택된 case study의 정밀 계산; 47종 전체 검증이 아님 |

## 6. Co-doping·ML

| 용어 | 뜻 |
|---|---|
| v1 heuristic | single-dopant endpoint를 조합한 규칙 기반 pair prior |
| v2 ML | 현재 feature/label로 학습한 pair-ranking model |
| +0.360 V | Cr₂O₃–HfO₂ single-dopant endpoint 조합의 constructed proxy gain |
| explicit pair label | 실제 co-doped 구조·site·charge closure·protocol이 붙은 계산/실험값 |
| LOOCV | 한 sample을 빼는 교차검증; 같은 dopant identity 누출 가능 |
| LODO | 한 dopant identity를 통째로 빼는 검증 |
| L2DO | 두 dopant identity를 통째로 빼는 더 강한 검증 |
| AD | applicability domain; 모델이 학습 분포 안에서 해석 가능한 범위 |
| acquisition loop | uncertainty·Pareto gain·chemical diversity·gate-boundary risk로 다음 계산을 고르는 과정 |

Cr₂O₃–HfO₂는 **v1 #1, v2 #8, uncomputed hypothesis**다. Predictive model이라고 부르려면 explicit pair labels, grouped CV, frozen prospective holdout이 필요하다.

## 7. 수치·표기 규칙

- 에너지는 eV 또는 meV/atom을 함께 표기하고 기준항을 말한다.
- 전압은 V, 탄성률은 GPa, 활성화에너지는 eV로 표기한다.
- 평균·정규화값은 대상 pool과 창을 같이 쓴다.
- 문헌값은 `[AuthorYY]` 또는 `literature` 태그를 붙인다.
- 근거가 섞인 profile은 `mixed evidence`라고 표시한다.
- missing은 제외 상태로 유지하고 0으로 채우지 않는다.
- 47, 11, 2는 각각 snapshot, post-hoc endpoint, targeted DFT coverage이며 순차 funnel로 연결하지 않는다.

