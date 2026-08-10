# Research Seminar spec — A gated MLIP-to-DFT screening cascade for LPSCl modification

> **발표자** 안용훈 (Yonghoon An) · Division of Materials Science & Engineering, Hanyang University
> **형식** 이가형 연구세미나 템플릿 승계 · 4:3 · English visible copy · Korean speaker notes
> **분량** 본문 18장(S1–S18, 표지 포함) + Appendix 6장(A1–A6) = **정확히 24장**
> **청중** 황화물 고체전해질과 계산재료를 처음 접하는 대학원생
> **발표 중심** LPSCl 물성 강의가 아니라, 큐레이션된 치환 후보를 물리 게이트로 감사하고 다음 DFT·실험 대상을 줄이는 **의사결정 cascade**

## 발표의 한 문장 목표

발표가 끝났을 때 청중은 이 연구가 47종에서 승자를 찾아낸 작업이 아니라, 같은 프로토콜로 얻은 상대 정보를 물리 게이트와 provenance로 제한해 **짧고 방어 가능한 검증 목록**으로 바꾸는 파이프라인이라는 점을 이해해야 한다.

## 전 슬라이드 공통 규율

1. 농도는 **x002 / x005 / x010 세 명목 수준**으로만 표기한다. 현재 계보 파일 사이의 수치 매핑이 충돌하므로 0.02·0.05·0.10 또는 다른 실제 x로 번역하지 않는다.
2. 91×3=273과 47은 단위와 계보가 다르다. 47종은 2026-06-25에 versioning된 앞 141행의 종별 snapshot이며, 나머지 44종은 정본 표에 미수집됐다. 전종별 실패 manifest가 없으므로 계산 미완결·물리 탈락·음성 라벨로 단정하지 않는다.
3. 47 → 47 → 43 → 25 → 11 → 1 waterfall은 기존 weighted-score 결과를 문헌형 hard gate로 **사후 재표현한 분석 뷰**다. 발견 성능이나 prospective funnel로 부르지 않는다.
4. G4는 BVSE 정적 기하 프록시와 경험적 cutoff를 쓰는 **heuristic gate**다. 실제 D, σ 또는 확산 판정으로 읽지 않는다.
5. G5는 roster median에 의존하는 **ranking-only preference**다. 마지막 1종을 winner, champion 또는 물리적 합격자로 부르지 않는다.
6. 현재 DFT 심층 검증 범위는 **2 / 47**이다. 나머지는 같은 UMA 계보 안의 상대 스크린이다.
7. comp1에는 현재 인용 가능한 Ea가 없다. modelc의 0.197 ± 0.032 eV만 온도 600/800/1000 K, 3-seed 규약과 함께 쓴다. comp1 barrier·prefactor·Ea 비교는 하지 않는다.
8. SDCP의 −1.465 eV는 유효 adsorption 또는 binding energy가 아니다. UMA가 산화 대가를 보지 못한 Li-transfer artifact의 한 장면으로만 쓴다. 9 meV 자세 차이도 site preference로 쓰지 않는다.
9. 서로 다른 프로토콜·정본 묶음의 절대값을 한 표에서 직접 비교하지 않는다. 모든 수치는 method tag, source file, status와 같이 이동한다.
10. 그림 라벨과 캡션은 영어만 쓴다. 한국어 설명은 speaker notes에 둔다.

---

# Main deck — 18 slides

## Part 1 — Context and motivation

### S1. Cover — A gated MLIP-to-DFT screening cascade for LPSCl modification

#### Visible copy

**A gated MLIP-to-DFT screening cascade for LPSCl modification**
*From curated substitutions to auditable decisions*

- MLIP screening
- Physical gates
- Targeted validation

#### 한국어 발표 대본

오늘 발표의 중심은 특정 도펀트 하나가 아니야. LPSCl을 개선하려고 여러 치환 후보를 계산했을 때, 무엇을 믿고 무엇을 탈락시킬지 결정하는 cascade를 설명할게. 최종 산출물은 승자 선언이 아니라 다음 DFT와 실험이 갈 수 있는 짧고 방어 가능한 후보 목록이야.

#### 핵심 근거 파일

- docs/cascade_pipeline_guide.md
- db/properties/cascade_screening_funnel.json

---

### S2. LPSCl is useful — and still not enough

#### Visible copy

**LPSCl**

- Fast Li⁺ conductor
- Processable sulfide platform

**Remaining constraints**

- Oxidation
- Interface
- Contact & mechanics
- Multi-objective trade-offs

**Coating · Substitution · Composite · Processing**

> There is no single repair knob.

#### 한국어 발표 대본

Argyrodite LPSCl은 높은 이온전도성과 가공성 때문에 대표적인 황화물 고체전해질 플랫폼으로 쓰여. 하지만 산화 안정성, 전극과의 계면 반응, 입자 접촉과 기계적 안정성을 동시에 만족하지는 못해. 코팅, 치환, 복합화, 공정 제어가 모두 쓰이지만 하나의 조작이 여러 물성을 함께 바꿔. 그래서 단일 물성 최적화가 아니라 다목적 선별 문제로 봐야 해. 여기서부터 자연스럽게 “어떤 처방이 좋은가”보다 “어떤 처방이 다른 축을 망가뜨리지 않는가”라는 질문으로 넘어가면 돼.

#### 핵심 근거 파일

- docs/cascade_pipeline_guide.md §0
- litdb/papers/famprikis2019_fundamentals_inorganic_sse.md
- litdb/papers/xiao2019_cathode_coating_screening.md

#### Figure plan

- **실제 삽입**: `litdb/figures/sundar2025_oxide_coating_screening_lpscl/fig_1.png` — LPSCl particle coating과 Li/LPSCl/cathode interface를 함께 보여주는 intro schematic.
- 화면 citation: `Sundar et al., Adv. Sci. 2025, Fig. 1`.
- 경계: coating과 lattice substitution은 다른 문제이며, 이 그림은 “한 처방도 여러 계면을 동시에 만족해야 한다”는 문제 정의에만 쓴다.

---

### S3. Substitution turns one material into hundreds of decisions

#### Visible copy

- **Dopant chemistry** — Which element or compound?
- **Campaign label** — x002 / x005 / x010; actual concentration unresolved
- **Configuration** — Where are defects placed?
- **Target properties** — Stability · transport · mechanics

**91 curated compounds × 3 campaign labels = 273 campaign run slots**

> Element labels alone do not predict the effect.

#### 한국어 발표 대본

도펀트 종류만 바뀌는 게 아니야. 같은 화합물도 실제 농도, 결함 배치와 variant가 달라지면 다른 구조가 돼. 현재 funnel 계보와 ranked CSV의 concentration 표기가 충돌하므로 발표에서는 x002, x005, x010을 campaign label이라고만 부를게. 실험 한 점에는 합성, XRD, EIS, 셀 조립까지 많은 시간이 들고, 원소 이름만 보고 산화 안정성이나 Li 수송이 어느 방향으로 움직일지 알기 어려워. 비싼 검증 전에 실패 가능성이 큰 방향부터 줄이는 절차가 필요해.

#### 핵심 근거 파일

- docs/cascade_pipeline_guide.md §3
- db/properties/cascade_screening_funnel.json
- db/properties/cascade_v23_ranked.csv
- kb/projects/cascade_v23_review_2026_07_11.md

---

### S4. A cascade spends precision only where it matters

#### Visible copy

1. **CURATE** — Chemical priors · literature · database
2. **SCREEN** — Same-protocol MLIP and low-cost proxies
3. **GATE** — Reject physically unsafe directions
4. **VALIDATE** — Targeted DFT and experiment

**Candidate count ↓ · Cost and precision ↑**

> Computation narrows experiments; it does not replace them.

#### 한국어 발표 대본

Cascade는 단순히 계산을 많이 돌리는 방법이 아니야. 싼 단계에서는 후보를 넓게 비교하고, 물리 게이트로 위험한 후보를 제거한 뒤, 비싼 DFT와 실험을 남은 후보에 집중하는 비용 배치 전략이야. 각 단계가 무엇을 판정할 수 있는지 한계를 먼저 정하고 단계 사이에서 주장 강도를 올려. 따라서 빠른 단계에서 얻은 상대 순위를 바로 물성의 진실로 바꾸지 않는 것이 이 구조의 핵심이야.

#### 핵심 근거 파일

- docs/cascade_pipeline_guide.md §2
- litdb/papers/sendek2017_ml_screening_12k_conductors.md
- litdb/papers/xiao2019_cathode_coating_screening.md

---

## Part 2 — Pool and pipeline

### S5. Our starting pool was curated, not discovered

#### Visible copy

**91 curated species × 3 campaign labels = 273 run slots**

**2026-06-25 versioned snapshot**

- 141 champion records = 47 species × 3 labels
- 37 oxides + 10 fluorides
- 44 later-roster species not ingested into the canonical table
- Missing from this snapshot ≠ physically rejected

> 47 is a composition-family scan — not a 100,000-material discovery funnel.

#### 한국어 발표 대본

출발점은 수만 종 자동 발견이 아니야. 사람이 91개 species를 배열했고 세 campaign label을 붙여 273 run slot을 만들었어. Git에 실제로 versioning된 2026-06-25 snapshot은 실행 순서의 앞 141행, 즉 oxide 37종과 fluoride 10종의 세 label이야. 뒤 44종은 정본 표에 들어오지 않았고 later note는 273/273 완료라고 하지만 unified 273-row table은 남아 있지 않아. 따라서 이 44종을 구조 실패나 물리 탈락으로 부르면 안 돼. post-hoc 물리 gate는 versioned 47종에서 별도로 시작해.

#### 핵심 근거 파일

- db/properties/cascade_screening_funnel.json
- docs/cascade_pipeline_guide.md §3
- db/properties/cascade_v23_ranked.csv
- docs/reviews/cascade_db_ml_readiness_audit_2026_08_10.md

#### Figure plan

- **실제 삽입**: `docs/figures/cascade/cascade_seminar_pool_attrition_273_to_47.png`.
- 이 그림과 `47→47→43→25→11→1*` waterfall은 서로 다른 슬라이드에 둔다.

---

### S6. Search, validation, and interpretation are different jobs

#### Visible copy

- **L0 CURATED INPUT** — Composition · nominal level · configuration · provenance
- **L1 LOW-COST SCREEN** — UMA relaxation · BVSE · derived axes
- **L2 MATCHED DFT** — Selected candidates only
- **L3 EXPERIMENT** — Phase · σ(T) · stability · processing

> Protocol tag + source file + status travel with every value.

**Current scope: 47 relative screens; targeted DFT validation covers 2 candidates.**

#### 한국어 발표 대본

L1에서는 UMA와 저비용 프록시로 넓게 보고, L2에서는 필요한 후보만 matched DFT로 확인해. L3는 상형성, 전도도, 안정성, 공정성을 실제로 확인하는 실험 단계야. 모든 조성이 똑같은 고비용 계산을 받는다는 뜻이 아니라, 각 tier 안에서 프로토콜을 고정하고 선택된 후보만 다음 tier로 올린다는 뜻이야. 현재 DFT 심층 검증은 Nd₂O₃와 B₂O₃ 두 후보뿐이라는 범위를 계속 표시해야 해.

#### 핵심 근거 파일

- docs/cascade_pipeline_guide.md §2, §4–§6
- webapp/data.py의 CASCADE_META
- db/properties/doping_cascade_verified.json

---

### S7. LPSCl taught us which descriptors to watch

#### Visible copy

**Electronic guard**

- E_g = 2.066 vs 2.099 eV
- Δ = 0.033 eV
- Fixed-occupation eigenvalues

**Structural contrast**

- Li vacancies
- 4d-Cl anti-sites
- Disorder, not a new chemistry

**Transport evidence**

- modelc Ea = 0.197 ± 0.032 eV
- 3-seed · 600/800/1000 K
- No citable comp1 Ea

> Structural descriptors first; electronics remain a guardrail.

#### 한국어 발표 대본

기존 LPSCl과 Cl-rich modelc 비교는 cascade의 결과가 아니라 축 선택의 선행 사례야. fixed-occupation band gap 차이는 0.033 eV로 작지만 Cl-rich 구조에는 Li 공공과 4d-Cl anti-site가 생겨. 그래서 구조 안정성, Li 이동 경로, 무질서와 기계 축을 우선 기술자로 잡았어. 수송에서는 modelc의 0.197 ± 0.032 eV만 3-seed, 600·800·1000 K 규약과 함께 인용할 수 있어. comp1에는 현재 인용 가능한 멀티시드 Ea가 없으므로 두 계의 barrier, prefactor 또는 Ea를 비교하면 안 돼. gap 값은 canonical이지만 계통별 fixed-occ 실행 입출력은 provenance-open이라는 꼬리표도 유지해.

#### 핵심 근거 파일

- db/properties/electronic.json
- db/properties/canonical_registry.json
- kb/methodology/terminology_register.md
- kb/open_items.md
- tools/modelc_v3 및 tools/ionic의 MD 정본 계보

---

## Part 3 — The post-hoc physical gate view

### S8. Five gates ask five different questions

#### Visible copy

| Gate | Question | Metric / threshold |
|---|---|---|
| G1 | Is the structure more stable than the host? | mean ΔE < 0 |
| G2 | Does the electrochemical window collapse? | window ≥ 0.05 V |
| G3 | Is oxidation worse than the host? | Vox ≥ 2.14 V |
| G4 | Is the Li pathway retained? | transport_norm > 0.3 AND blocking < 0.6 |
| G5* | How do survivors rank mechanically? | roster medians |

**G4 is heuristic. G5 is roster-relative ranking.**

#### 한국어 발표 대본

각 게이트는 하나의 질문을 맡아. G1은 host 대비 구조 안정, G2는 전기화학 창 붕괴, G3는 host 대비 산화 onset이야. G4는 BVSE 기하 프록시의 두 cutoff를 쓰며 실제 확산이나 전도도 게이트가 아니야. 특히 blocking 0.6은 host나 문헌 절대 기준에 직접 앵커된 값이 아니라 경험적 규약이야. G5도 로스터 median 기반 정렬이므로 G1부터 G3와 같은 객관성으로 말하면 안 돼. mean ΔE는 x002, x005, x010 명목 수준의 내부 집계로만 읽고 실제 조성값으로 환산하지 않아.

#### 핵심 근거 파일

- db/properties/cascade_screening_funnel.json
- docs/cascade_pipeline_guide.md §7–§11
- db/properties/cascade_v23_litransport.csv

---

### S9. The auditable hard-gate view stops at 11

#### Visible copy

| Stage | Count |
|---|---:|
| Data-complete pool | 47 |
| G1 Structure | 47 |
| G2 Window | 43 |
| G3 Oxidation | 25 |
| G4 Li transport | 11 |
| G5 Mechanical ranking | 1* |

> *This funnel is a post-hoc analysis view. G4 is heuristic; G5 is ranking-only.*

#### 한국어 발표 대본

기본 산출물은 weighted score이고 이 5단계 hard-gate funnel은 문헌 기준을 기존 결과에 투영한 사후 분석 뷰야. waterfall은 47에서 47, 43, 25, 11로 줄어. G4에도 heuristic cutoff가 있고 G5의 한 종은 median 정렬 결과라 최종 승자라고 부르지 않아. 방어 가능한 보고는 G4 통과 11종과 각 게이트의 한계를 함께 제시하는 방식이야. “우리 pipeline이 prospectively 47종에서 11종을 발견했다”라고 말하면 범위를 넘는다.

#### 핵심 근거 파일

- db/properties/cascade_screening_funnel.json
- docs/cascade_pipeline_guide.md §7–§13
- tools/cascade/build_screening_funnel.py

---

### S10. Two gates reveal more about the pool than the candidates

#### Visible copy

**G1: 47 / 47 pass**

- VACUOUS
- No selection pressure in this curated pool
- Does not prove universal stability

**G2: unique kill = 0**

- REDUNDANT
- Four window-collapse failures also fail G3
- Late-TM chemistry drives both

> Keep the records. Change the interpretation.

#### 한국어 발표 대본

G1이 아무 후보도 제거하지 못한 것은 모든 후보가 훌륭하다는 뜻이 아니야. 출발 풀이 안정 후보 위주로 큐레이션됐다는 뜻이야. G2에서 탈락한 네 late-transition-metal 후보는 G3에도 모두 탈락해서 unique kill이 0이야. 게이트가 실제로 독립적인 정보를 주는지 감사하는 것 자체가 결과야. 게이트를 숨기거나 삭제하기보다 현재 풀에서 선택압이 없거나 중복됐다고 정확히 표시하는 편이 다음 라운드에도 유용해.

#### 핵심 근거 파일

- db/properties/cascade_screening_funnel.json
- docs/cascade_pipeline_guide.md §7–§9

---

## Part 4 — What the cascade actually teaches

### S11. Oxidation stability and Li transport pull in opposite directions

#### Visible copy

**OXIDATION**

- 6 / 6 candidates raise onset above the host

**LI TRANSPORT**

- The same 6 / 6 fail G4 pathway retention

**B₂O₃ · Cr₂O₃ · Ga₂O₃ · In₂O₃ · Sc₂O₃ · Y₂O₃**

> The central result is a trade-off, not a winner.
> G4 is a static BVSE proxy — not conductivity.

#### 한국어 발표 대본

Host보다 산화 onset을 높인 후보는 B₂O₃, Cr₂O₃, Ga₂O₃, In₂O₃, Sc₂O₃, Y₂O₃ 여섯 종이야. 그런데 여섯 종 모두 G4에서 Li 경로 유지 조건을 통과하지 못했어. 이 trade-off가 cascade의 가장 중요한 물리 결과야. 다만 G4는 BVSE 기반 정적 기하 프록시라 실제 전도도나 확산계수라고 읽으면 안 돼. 따라서 결론은 “산화 개선 후보가 정적 경로 지표에서 불리했다”까지이고, 실제 σ 저하 확정은 MD나 실험의 몫이야.

#### 핵심 근거 파일

- db/properties/oxidation_stability_cascade.csv
- db/properties/cascade_v23_litransport.csv
- db/properties/cascade_screening_funnel.json
- docs/cascade_pipeline_guide.md §10

#### Figure plan

- **실제 삽입**: `docs/figures/cascade/cascade_seminar_oxidation_transport_47.png`.
- 캡션에 `Static BVSE/pathway heuristic ≠ conductivity`를 고정한다.

---

### S12. A ranking is a preference model, not a measurement

#### Visible copy

**Geometric mean = AND**

- One weak axis pulls the combined score down
- Weights encode priorities, not physics

**Pareto front**

- Keep non-dominated trade-offs visible
- Do not hide them behind one score

**Missing ≠ zero**

- Uncomputed, incomplete, and physically failed are distinct
- Degenerate ties remain unresolved

> Show score, Pareto set, gate status, and missingness together.

#### 한국어 발표 대본

가중점수나 기하평균은 측정된 물리량이 아니라 의사결정 함수야. 축 선택과 가중치를 바꾸면 순위가 바뀌기 때문에 Pareto front를 함께 보여야 해. 데이터가 없는 후보를 0점으로 주면 계산 실패를 나쁜 화학으로 오인하게 돼. 그래서 미계산, pipeline incomplete, physical fail을 서로 다른 상태로 보존해. G3처럼 같은 2.14 V에 묶인 후보도 소수점 차이로 억지 순위를 만들지 않아. G5의 단일 잔존자도 같은 이유로 winner가 아니야.

#### 핵심 근거 파일

- db/properties/cascade_v23_ranked.csv
- db/properties/cascade_v23_themes.json
- docs/cascade_pipeline_guide.md §9, §12

#### Figure plan

- **실제 삽입**: `docs/figures/cascade/cascade_seminar_pareto_47.png`.
- conditional 2D Pareto 네 종은 `axis-dependent; not a winner set`으로 표시한다.

---

### S13. Gate order changes the story, not the terminal intersection

#### Visible copy

**120 / 120 gate permutations tested**

- G1 → G2 → G3 → G4 → G5
  47 → 47 → 43 → 25 → 11 → 1
- G1 → G3 → G2 → G5 → G4
  47 → 47 → 25 → 25 → 7 → 1
- Other 118 orders
  different intermediate attribution

> Terminal set invariant; intermediate waterfall and “who killed what” are order-dependent.

#### 한국어 발표 대본

다섯 게이트의 120개 순열을 모두 시험했어. 게이트가 정적인 boolean 조건이라 최종 교집합은 순서와 무관했어. 대신 중간 생존자 수와 어느 게이트가 후보를 탈락시킨 것으로 보이는지는 달라져. 따라서 waterfall 모양은 결과 자체라기보다 설명 순서라는 걸 밝혀야 해. 이 불변성은 G5 기준이 객관적이라는 뜻이 아니라, 고정된 다섯 조건의 교집합이 순서와 무관하다는 수학적 확인이야.

#### 핵심 근거 파일

- db/properties/cascade_screening_funnel.json
- docs/cascade_pipeline_guide.md §13
- tools/cascade/build_screening_funnel.py

---

### S14. Claim strength must match the method

#### Visible copy

**SUPPORTED**

- Gate pass / fail under the declared rules
- Same-protocol relative ranking
- Oxidation–transport trade-off
- Gate-order invariance

**NOT SUPPORTED**

- UMA absolute energies or moduli
- BVSE-derived conductivity
- Ranking inside degenerate groups
- A unique G5 winner

**Still missing as full gates: interface reaction + electronic insulation**

#### 한국어 발표 대본

같은 프로토콜 안에서의 통과·탈락과 상대 순위, 산화–수송 trade-off, 순서 불변성은 현재 데이터로 지지돼. 반면 UMA 절대 에너지와 탄성값, BVSE를 전도도로 환산한 값, 축퇴군 내부 순위, G5의 단일 승자는 지지되지 않아. 계면 반응성과 전자 절연은 아직 47종 전체에 완결된 게이트로 들어오지 않았어. “문헌 게이트를 모두 재현했다”거나 “11종이 실험 후보로 검증됐다”는 표현도 쓰지 않아.

#### 핵심 근거 파일

- docs/cascade_pipeline_guide.md §14
- AGENTS.md의 데이터 규율
- db/properties/cascade_screening_funnel.json

---

## Part 5 — Validation boundary and ML roadmap

### S15. Failures made the cascade more credible

#### Visible copy

| Initial claim | Corrective rule |
|---|---|
| Single-seed 1.33× conductivity | Multi-seed verdict only |
| MSD fit outside diffusion | β ∈ [0.8, 1.2] gate |
| DOS-threshold band gap | Fixed-occupation eigenvalues |
| Deep adsorption = strong bond | Geometry + charge-state audit |
| 9 meV pose difference = preference | Matched counterfactual required |

> A deeper energy is not necessarily a stronger bond.

#### 한국어 발표 대본

이 파이프라인은 처음부터 완성된 규칙이 아니었어. 단일시드 전도도 비교, 확산영역 밖 MSD 피팅, DOS-threshold gap을 모두 철회했어. 표면 계산에서는 에너지가 깊다는 이유만으로 결합이라고 판단하면 안 되고 원자 이탈과 전하상태까지 확인해야 해. SDCP의 −1.465 eV는 유효 흡착에너지나 binding energy가 아니라 UMA가 산화 대가를 보지 못한 Li-transfer 사건으로만 설명해야 해. Li와 Ni 자세의 9 meV 차이도 matched pose와 전자상태가 없는 상태에서는 site preference가 아니야. 이 사례들은 cascade 47종의 정량 결과와 섞지 않고, 검증 규칙이 왜 필요한지 보여주는 별도 artifact 경계 사례로만 사용해.

#### 핵심 근거 파일

- docs/cascade_pipeline_guide.md §15
- webapp/data.py의 SDCP highlight
- kb/projects/sdcp_phaseB_direction_2026_08_06.md
- db/properties/canonical_registry.json
- AGENTS.md의 band-gap 및 MLIP-MD 규율

---

### S16. Promotion is selective — not every candidate receives DFT

#### Visible copy

**47 same-protocol screens**

**11 G1–G4 post-hoc survivors**

**2 / 47 existing DFT deep validations**

> These are coverage counts, not a sequential 47 → 11 → 2 funnel.

**Promote when**

- Near a gate boundary
- Model heads disagree
- Pareto value is high
- Chemistry is under-sampled

**Matched validation contract**

- Same structure
- Same cell and constraints
- Same k-mesh and reference
- Same magnetic protocol

> The 47-candidate result is a relative screen — not 47 DFT confirmations.

#### 한국어 발표 대본

현재 47종 전체가 DFT로 검증된 것이 아니고 DFT 심층 검증은 Nd₂O₃와 B₂O₃ 두 후보뿐이야. 비싼 계산은 게이트 경계, 모델 불일치, Pareto 가치, 새로운 화학을 대표하는 후보에 집중해야 해. DFT로 올릴 때는 구조, 셀, 제약, k-mesh, 기준 에너지, 자기 프로토콜을 맞춰야 비교가 성립해. 여기서 11은 G4 heuristic을 포함한 post-hoc 생존 집합이고, 기존 DFT 두 건은 그 11에서 순차 선발한 downstream subset이 아니야. 특히 B₂O₃는 G4에서 탈락하므로 47 → 11 → 2처럼 화살표로 연결하면 틀려. 세 숫자는 각각 screen 규모, post-hoc gate 결과, 기존 심층검증 coverage로 나란히 표시해.

#### 핵심 근거 파일

- webapp/data.py의 CASCADE_META 및 CASCADE_DOPANT
- db/properties/doping_cascade_verified.json
- docs/cascade_pipeline_guide.md §2, §5
- kb/methodology/computational_methods_canonical.md

---

### S17. ML is already here — but it is not yet a discovery model

#### Visible copy

**UMA MLIP**

- Energy and force surrogate
- Fast configuration search
- Same-protocol relative screen

**Physics cascade**

- Gate pass / fail
- Trade-off structure
- Shortlist for expensive validation

**Co-doping ML v2**

- 47 single-dopant scores → 1,081 pair hypotheses
- No real co-doped labels yet
- LODO / L2DO R² < 0

> Current role: cost reduction + hypothesis ordering, not discovery certification.

#### 한국어 발표 대본

ML이라는 말을 둘로 나눠야 해. UMA는 에너지와 힘을 빠르게 계산하는 사전학습 ML potential이고, 이 덕분에 후보를 같은 규약으로 넓게 볼 수 있어. 공동치환 ML v2는 47개 단일 도펀트의 합성점수를 1,081개 쌍 가설에 이식한 순서 제안기야. 실제 공동치환 물성 라벨이 없고 독립 도펀트 검증에서는 LODO와 L2DO R²가 모두 음수라서 discovery predictor라고 부르면 안 돼. 높은 LOOCV 수치는 타깃이 입력 특징의 선형 합성이라는 항등식을 복원한 결과이며 외부 예측력의 증거가 아니야.

#### 핵심 근거 파일

- tools/cascade/codoping_ml.py
- db/properties/codoping_ml_v2_meta.json
- db/properties/codoping_ml_v2.csv
- docs/cascade_pipeline_guide.md §4

---

### S18. The next cascade learns where to calculate next

#### Visible copy

**CANDIDATE SPACE**
dopant × nominal level × configuration

→ **L1 FAST SCREEN**
UMA + BVSE + gate risk

→ **ACQUISITION**
Pareto gain + uncertainty + diversity

→ **L2 DFT**
matched validation

→ **L3 EXPERIMENT**
phase · σ(T) · stability

→ **VERSIONED DATABASE**

**EXPLOIT: predicted Pareto gain · EXPLORE: uncertainty / new chemistry · VALIDATE: gate boundary**

> ML chooses what to calculate next; physics and experiments decide what is true.

#### 한국어 발표 대본

다음 단계는 현재 게이트를 ML로 없애는 게 아니라 비싼 계산을 어디에 먼저 쓸지 정하는 폐루프야. 상위 예측만 반복하지 않고 불확실하거나 새로운 화학도 일부 선택하고, 게이트 경계나 모델 불일치 구조를 DFT로 확인해. UMA, BVSE, DFT, 실험값은 한 열에 섞지 않고 provenance와 fidelity를 분리해. canonical table에 미수집된 44종은 음성 라벨이나 incomplete case로 단정하지 않고 미관측 상태로 남겨야 해. 실제 공동치환 라벨, 화학 계열 group split, prospective validation round가 쌓인 뒤에만 예측 모델이라는 표현을 검토할 수 있어. 최종 판단은 여전히 물리 게이트와 실험이 맡아.

#### 핵심 근거 파일

- kb/open_items.md
- db/properties/mlip_committee_baseline.json
- db/properties/codoping_ml_v2_meta.json
- tools/cascade/codoping_ml.py

---

# Appendix — 6 slides

### A1. Terminology and symbol conventions

#### Visible copy

| Symbol / term | Meaning | Usage rule |
|---|---|---|
| ΔE | Doped − host relative energy | Same engine, cell, and composition convention |
| Vox | Grand-potential oxidation onset | V vs Li; ties at 2.14 V remain unresolved |
| window | Vox − Vred | Collapse gate only; not kinetic stability |
| transport_norm | BVSE geometric proxy | Never call it D or conductivity |
| β | d log(MSD) / d log(t) | 0.8–1.2 required for a diffusive verdict |
| Ea | Arrhenius activation energy | State temperatures, fitting window, and seeds |
| missing | Not calculated or incomplete | Not zero and not physical failure |

**Concentration label:** x002 / x005 / x010 = nominal campaign levels only.

#### 한국어 발표 대본

이 표는 발표 전체에서 기호를 어떻게 읽는지 고정해. transport_norm은 BVSE 프록시라서 D나 전도도라고 부르면 안 되고, missing은 0점도 탈락도 아니야. Ea를 말할 때는 온도, MSD 창, 시드 수를 함께 붙여. x002, x005, x010은 현재 캠페인 디렉터리와 열 이름을 식별하는 명목 라벨이며 실제 농도값으로 번역하지 않아. ΔE와 Vox도 method tag 없이 단독 숫자로 이동시키지 않아.

#### 핵심 근거 파일

- kb/methodology/terminology_register.md
- docs/cascade_pipeline_guide.md §6–§12
- AGENTS.md

---

### A2. Protocol matrix and allowed claims

#### Visible copy

| Tier / method | Primary output | Allowed claim | Do not claim |
|---|---|---|---|
| UMA MLIP | Relative E, forces, relaxation | Same-protocol ordering | Absolute thermodynamics |
| BVSE | Static pathway geometry | Pathway-retention risk | D or conductivity |
| MLIP-MD | MSD, D(T), Ea | Multi-seed verdict at 600/800/1000 K | Single-seed ratio |
| DFT | Matched energy and electronic response | Selected-candidate validation | 47 / 47 DFT coverage |
| Literature / experiment | External measured or computed values | Directional cross-check | Mix with internal absolutes |

#### 한국어 발표 대본

이 표의 핵심은 계산 엔진 이름이 아니라 허용되는 주장 강도야. UMA는 상대 스크리닝, BVSE는 정적 경로 프록시, MD는 멀티시드와 β를 통과한 수송, DFT는 선택된 후보의 matched validation이야. 서로 다른 프로토콜 절대값을 같은 표에 섞지 않아. comp1 Ea는 MD 행의 규약을 통과하지 못했으므로 공란으로 두고, modelc 값만 600·800·1000 K와 3-seed 정보를 붙여 사용해.

#### 핵심 근거 파일

- AGENTS.md
- docs/cascade_pipeline_guide.md §4–§6
- kb/methodology/computational_methods_canonical.md
- db/properties/canonical_registry.json

---

### A3. 47-candidate scorecard

#### Visible copy

**Favorable percentile by axis · first-stop gate · alphabetical species order**

> This is an audit matrix, not a winner heatmap.

#### 한국어 발표 대본

47종을 알파벳순으로 놓고 각 축의 favorable percentile과 첫 stop gate를 같이 보여줘. 한 색으로 합산한 score보다 어떤 축에서 trade-off가 생겼는지가 먼저 보이게 하는 appendix야. 색이 진하다고 실제 물성이 좋다고 단정하지 않고, 각 열의 protocol과 gate caveat는 본문 S8에서 확인해.

#### 핵심 근거 파일

- db/properties/cascade_screening_funnel.json
- db/properties/cascade_v23_ranked.csv
- docs/figures/cascade/cascade_seminar_scorecard_47.png
- db/properties/cascade_seminar_scorecard_47.csv

---

### A4. Defense Q&A — cascade and evidence

#### Visible copy

| Question | Defense answer |
|---|---|
| Is 47 a high-throughput discovery funnel? | No. It is a human-curated, host-specific composition-family scan. |
| What happened to the other 44 of 91? | They are absent from the versioned canonical snapshot. Later notes report 273/273 completion, but the unified table is not versioned; absence is not physical rejection. |
| Why keep vacuous or redundant gates? | Auditability. Their selection pressure is reported and may change with a new pool. |
| Why conclude at 11 instead of one? | G5 is roster-median ranking. G4 defines the defensible reported set under stated heuristics. |
| Does BVSE failure prove low conductivity? | No. It flags pathway risk; multi-seed MD or experiment is required. |

#### 한국어 발표 대본

첫째, 47은 DB 전수 탐색 결과가 아니라 사람이 고른 host-specific 조성족의 versioned snapshot이야. 둘째, 나머지 44종은 정본 표에 미수집됐고 전종별 실패 manifest가 없으므로 음성 라벨이 아니야. 셋째, G1과 G2가 약하다는 점은 숨기지 않고 게이트 감사 결과로 보고해. 넷째, G5는 roster median이므로 한 종을 결론으로 내리지 않고 G4까지의 11종을 한계와 함께 보고해. 다섯째, G4 자체도 BVSE heuristic이라 11종을 실제 고전도 후보로 확정한 것은 아니며 MD나 실험이 필요해.

#### 핵심 근거 파일

- docs/cascade_pipeline_guide.md §3, §7–§14
- db/properties/cascade_screening_funnel.json
- db/properties/cascade_v23_litransport.csv

---

### A5. Defense Q&A — validation and ML

#### Visible copy

| Question | Defense answer |
|---|---|
| Are all 47 candidates DFT-validated? | No. Current DFT coverage is 2 / 47; the rest are relative screens. |
| Can 47 rows train a discovery model? | Not a general model. They can seed small gate-specific surrogates and active learning. |
| Why not trust LOOCV R² = 0.9998? | The target score is constructed from the same inputs; independent dopant splits collapse. |
| Why not choose only the predicted top candidate? | That creates winner’s curse. Acquisition must include uncertainty and chemical diversity. |
| When can the model be called predictive? | After real co-doped labels, group-CV, and at least one prospective validation round. |

#### 한국어 발표 대본

47종 전체가 DFT로 검증된 것이 아니라 두 종만 심층 검증됐다는 범위를 먼저 말해. 47행은 범용 discovery model에는 작지만 게이트별 작은 surrogate와 active learning의 시작점은 될 수 있어. LOOCV R² 0.9998은 cascade score가 입력 특징의 합성이라는 항등식을 복원한 값이라 외부 예측력이 아니야. 실제로 같은 도펀트가 폴드 사이에 공유되지 않도록 LODO와 L2DO를 적용하면 R²가 음수가 돼. 따라서 상위 점수만 고르면 winner’s curse가 커지고, 불확실도와 화학 다양성을 함께 선택해야 해. 실제 공동치환 라벨, group-CV, prospective validation이 있어야 predictor라는 표현을 쓸 수 있어.

#### 핵심 근거 파일

- webapp/data.py의 CASCADE_META
- db/properties/codoping_ml_v2_meta.json
- tools/cascade/codoping_ml.py
- db/properties/mlip_committee_baseline.json

---

### A6. Canonical sources held in the repository

#### Visible copy

| Source | Role |
|---|---|
| docs/cascade_pipeline_guide.md | Canonical narrative, gates, trust limits |
| db/properties/cascade_screening_funnel.json | Waterfall, gate outcomes, permutations |
| db/properties/cascade_v23_ranked.csv | 47-candidate ranked property table |
| db/properties/oxidation_stability_cascade.csv | Vox and ESW lineage |
| db/properties/cascade_v23_litransport.csv | BVSE transport proxy |
| db/properties/canonical_registry.json | Canonical values and provenance flags |
| db/properties/electronic.json | Fixed-occupation band gaps |
| db/properties/codoping_ml_v2_meta.json | ML validation limits |
| kb/methodology/terminology_register.md | Terms and symbol contract |
| docs/reviews/cascade_db_ml_readiness_audit_2026_08_10.md | 273→47 provenance and ML-readiness audit |
| docs/reviews/cascade_ai_screening_literature_comparison_2026_08_10.md | Screening/AI literature comparison and figure plan |

#### 한국어 발표 대본

발표에서 숫자를 기억으로 인용하지 않고 정본 파일로 돌아가. waterfall은 funnel JSON, 랭킹은 ranked CSV, 산화축은 oxidation CSV, 수송 프록시는 litransport CSV, gap은 fixed-occupation 전자 정본을 기준으로 해. ML의 성능과 한계는 codoping meta 파일에서 LODO와 L2DO를 함께 확인해. 정본 레지스트리에 provenance-open 표시가 있으면 값이 틀렸다는 뜻은 아니지만 계통별 실행 입출력으로 완전 재현하지 못한다는 경계를 유지해.

#### 핵심 근거 파일

- 위 표의 모든 파일
- AGENTS.md
- kb/open_items.md

---

# 발표자가 마지막으로 외울 다섯 문장

1. **273은 91종×3 campaign run slot이고, 47은 2026-06-25에 versioning된 O/F snapshot이다.**
2. **47 → 47 → 43 → 25 → 11 → 1은 prospective discovery가 아니라 post-hoc hard-gate view다.**
3. **핵심 결과는 winner가 아니라 산화 onset 개선 6종이 모두 G4에서 불리했던 oxidation–transport trade-off다.**
4. **G4는 BVSE heuristic, G5는 roster-relative ranking이며 DFT 검증 범위는 2 / 47이다.**
5. **ML은 다음 계산을 고르지만, 무엇이 참인지는 matched DFT와 실험이 결정한다.**
