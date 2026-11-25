# AI 기반 배터리 연구 자동화: LLM 기반 연구 분석에서 AI-Agent 전극 모델링까지 — 문장혁 (중앙대)

> slug `moon2026_cau_llm_agent_battery_automation` · type `talk` · 발표 2026-08-21 (2026년도 전지기술 심포지엄, 한국전기화학회, 기술세션 3-4) ·
> 발표자 **Janghyuk Moon**, Department of Energy Systems Engineering, Chung-Ang University ·
> 부제 "배터리 지식 분석, 모델 연계 및 전극 시뮬레이션 자동화" · 세션 대주제 "AI 전환기에서의 K-Battery 산업: 기회와 도전" ·
> PDF 22 pp (자료집 pp. 297–318) · 슬라이드 번호 2–39 + 표지 + 마무리 = 렌더 40장 · digested 2026-07-28 · status ✅ (덱), ⏳ 구술 txt 대기
>
> 🔁 **덱 실물 독립 재판독 완료 2026-08-03** — 같은 PDF가 inbox에 재투입(`litdb/inbox/문장혁 교수님.pdf`,
> **사용자 분류 `(미분류)`**)되어 **전 22 pp를 이미지로 다시 판독**했다. 이 PDF는 **텍스트 레이어 0**(전 페이지가
> 1737 px 폭 스캔을 18줄 스트립으로 쪼갠 raster)이라, 페이지를 슬라이드 단위로 잘라 **원해상도(1.15×)로 통독**하고
> 수치 영역은 **3–8× 확대**해 재판독했다(판독 배율은 각 항목에 표기). 결과 **교정 16건 · 신규 20건 ·
> 미해결질문 Q1 종결 · 슬라이드 3장(12·19·28·31·32) 신규 편입**. 전체 목록과 근거는 **§15**.
> 아래 본문은 재판독 값으로 이미 갱신돼 있다.
>
> ⚠ **덱 인용 규율**: `litdb/talks/README.md`. 이 덱은 **물성 수치가 거의 없고 인프라·워크플로 주장이 본체**다.
> 우리 물성 db 와 섞일 일은 없지만, **"이 방법으로 무엇을 얻었다"는 주장의 검증 가능성**이 낮으니
> (대부분 under review / arXiv) 인용 시 상태를 반드시 병기할 것.
> ⚠ 슬라이드 번호는 **덱 자체 표기(우하단)** 기준이고, PDF 페이지와 `p = (슬 + 5)/2` 로 대응한다(p3 = 슬 1–2).

---

## 1. 한 줄 요약

**"LLM을 문헌 분석(RAG·지식그래프)에서 시작해 시뮬레이션 실행·모델 피팅까지 도구로 연결하고,
종국엔 전극 미세구조 생성–검증–FEM 해석 전체를 다중 에이전트(BEARS)가 닫힌 루프로 돌린다"** —
즉 **물질이 아니라 연구 공정 자체를 자동화**하는 발표다. 우리 캠페인과 **물리 축은 겹치지 않지만
repo 운영 방식과는 정면으로 겹친다**.

---

## 2. 덱 구조 (4부)

| PDF p. | 슬라이드 | 섹션 |
|---|---|---|
| 3–8 | 1–11 | **01 AI for Battery Research and Development** — 상태추정/진단, 모델 계층, 산업 현황, 분자설계·셀설계·디지털트윈 |
| 8–11 | 12–17 | **02 LLM and Knowledge Intelligence for Battery Research** — LLM 필요성, SOH 워크플로, 온톨로지→KG→Graph RAG, 고장추론 KG, **ASSB KG+GNN**, 문헌 계량분석 |
| 11–14 | 18–24 | **03 Agentic AI for Battery Research Automation** — 정의, LLM 에이전트, MCP·FreeCAD, LLM-orchestrated FEM, 모델 피팅 에이전트, end-to-end 비전 |
| 15–22 | 25–39 | **04 AI-Agent-Based Electrode Modeling Automation** ★ 본체 — 스케일 지도, 병목, Physics–ML 파이프라인, 계보, **BEARS** |

p1 = 자료집 표지(p.297), **p2 = 백지(p.298)**, p22 하단 = "Thank You for Your Attention" + BEARS 로고·QR.

---

## 3. 01부 — 배경 (슬 2–11)

### 모델 계층 (슬 4) — 이 덱의 좌표계

```
① Empirical (capacity loss = f(I,T,SOC))          — data-fitting / phenomenological
② ECM (OCV + R0 + R1‖C1)                          — reduced-order electrical
③ Physics-based (DFN: ∂c/∂t = ∇·(D∇c) + R ,  ∂φ/∂x = −i/κ)  — electrochemical·transport·degradation
④ Data-driven ML                                   — NN / regression / sequence learning
                    →  Increasing model fidelity and complexity
```

> 🔑 **우리 위치**: 이 사다리의 **아래쪽 바깥**이다. 우리는 ③이 필요로 하는 **파라미터(σ, Ea, C_ij, ESW)를
> 원자 스케일에서 만드는 층**이고, 이 덱은 ③④를 자동화한다. **경쟁이 아니라 상하류**.
> 우리 open_items **M5(P2D 파라미터 export)** 가 정확히 이 접점이다 — 슬 39가 solver 실행을
> **"DIS / EIS / **P2D**"** 로 못박아, 소비자가 **파일 포맷 수준까지** 특정됐다.

### 산업 현황 (슬 8) — 발표에서 가장 구체적인 수치

**SK온 AI 기반 배터리 개발**
| 항목 | 값 |
|---|---|
| 시스템 | **AI 연구원(AI R&D 플랫폼)** |
| 도입 시점 | 2025년 7월 |
| 핵심 기능 | AI 기반 셀 설계와 소재 개발, 성능 예측과 원가 산출 효율화 |
| 개발 기간 변화 | 기존 대비 **3분의 1로 단축** |
| 원가 산출 속도 | 2시간 → **10초 (700배 향상)** |
| 프로젝트 절감 효과 | 완성차 프로젝트당 **수백억 원** 절감 예상 |
| 적용 산업 | 전기차, ESS, 로봇 등 배터리 응용 분야 |

**배터리 3사 글로벌 EV 시장** (*올해 1월 한 달간 기준. 자료 = SNE리서치*)
LG에너지솔루션 4.7 GWh (**−14.9 %**, 점유 6.6 %) · SK온 2.3 GWh (**−21.3 %**, 3.2 %) ·
삼성SDI 1.6 GWh (**−24.4 %**, 2.2 %) · **K배터리 3사 합계 8.6 GWh (−17.3 %, 12 %)**

> 🔑 이 두 슬라이드가 발표의 **동기 서사**다: 시장이 역성장하는 국면에서 AI가 개발 속도·원가로
> 활로를 낸다. **우리 원고/발표의 도입부 논리로 그대로 차용 가능**(출처 명시 조건).

### AI 연구량 급증 (슬 5) — 재판독으로 판독 완료 (3× 확대)

키워드 **"Battery & Artificial intelligence"** 연도별 링 차트. 안쪽부터 2019 → 바깥 2024.

| | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 |
|---|---|---|---|---|---|---|
| Publication numbers | 520 | 776 | 1,164 | 1,250 | 1,939 | 1,997 |
| Citation numbers | 4,159 | 8,165 | 14,037 | 22,707 | 23,443 | 31,644 |

⚠ 슬라이드에 **출처 표기 없음**(인용하려면 원 그림 추적 필요). 6년간 논문 **3.8배**, 인용 **7.6배**.
동반 삽화는 AI·에너지저장 연대기(1943 뉴런 모델 → 1991 SONY → 2014 ML → 2022 OpenAI DALL·E2/ChatGPT → 2023 준고체 → 2023 Na 계열).

### 기타 (슬 2–3, 6–7, 9–11)
- 상태추정/진단 지도 (슬 2): State estimation(SOC/SOH/Temp) · Diagnosis(fault detection) · Prognosis(SOC/RUL) · Health management
- 배터리 모니터링 AI 3분류 (슬 3): **model-based / data-driven / hybrid**, 과제는 state estimation(SOC·SOH·RUL·임피던스·SOP/SOT)과 fault diagnosis(과충방전·단락·열이상·센서고장)
- 데이터→분석→출력 지도 (슬 6, *Energy and AI*, 2020): 입력(시간·전압·전류·온도·전극전위·strain·압력)
  → 분석(EIS·ICA·CV·**HPPC**·GITT·DVA·**DTV**·**DRT**·acoustic) → 출력(용량손실·저항증가·직렬저항·전하이동증가·
  확산저항·활물질손실·**Li 인벤토리 손실**·엔트로피 계수)
- 멀티스케일 학습 프레임 (슬 7, *Adv. Funct. Mater.* **Volume 36, Issue 11 (2025)**): pm-nm → nm-µm → µm-cm → cm-m,
  각 스케일 기술자(조성·격자·에너지밴드·확산장벽·표면구조 / 결정성·입계·형상·내부균열·입도 / 기공률·압밀밀도·도전망·두께·접착강도 / form type·전극정렬·충전효율·formation 프로토콜·열 프로파일),
  **inverse design ↔ forward predicting** 양방향
- 전해질 분자 설계 (슬 9, **SES** 플랫폼): 헤더는 *Question → Search → Generation → Prediction → Validation*,
  플랫폼 탭은 **Ask → Search → Formulate → Design → Predict**. 데모 화면에 첨가제 영향 예측(Cycle Life ↑6.8 % / Rate Performance ↓2.6 %)
- 셀 설계 대시보드 (슬 10): **STEER OPENCELL** (SLAC / Stanford Doerr School of Sustainability · Precourt Institute for Energy).
  데모 값 — Energy 75.10 Wh · Cost per Unit Energy 39.12 $/kWh · Specific Energy 183.50 Wh/kg · Volumetric 414.85 Wh/L · Mass 409.25 g · Volume 0.181 L · Cost $2.94 (⚠ **데모 화면 값**, 벤치마크 아님)
- **디지털 트윈**·스마트 제조 (슬 11): 공장/설비/배터리 시스템 가상화 → 설계검증·공정 모니터링·**HIL 시험**·품질평가.
  BESS self-qualification (Grid/Design/Load requirements → Simulation · Hardware in the Loop · Product Qualification)
  > ⚠ 지도교수 피드백(2026-07)에 따라 **우리 자료에서는 "디지털 트윈" 대신 "AI 계산"을 쓰기로 결정**했다.
  > 이 덱은 그 용어를 쓴다 — 우리가 안 쓰는 것은 방침이지 그들이 틀려서가 아님을 기록해 둔다.

---

## 4. 02부 — 지식 인텔리전스 ★ (슬 12–17)

### 4a. 왜 LLM인가 (슬 12) 🆕 *재판독으로 편입*

**Conventional Limitations 3**: ① **Scalability** — 데이터·모델이 커질수록 성능·비용 문제 ② **Data Standardization** —
포맷·구조가 달라 통합이 막힘 ③ **Real-World Deployment** — 특정 조건 과적합으로 일반화 실패.
→ **LLM-based Solution 2**: **Large-Scale Pretraining / Finetuning**(수작업 feature 의존 감소) ·
**Self-Attention**(장거리 상호작용 포착, 이종 데이터 지원).
LLM×Battery 응용 원형 도표: battery materials development / battery system management / battery intelligent manufacturing /
battery knowledge integration(전문 Q&A, 리포트 생성, 정보 추출, **knowledge graph construction**, 다국어 처리).
출처 ***Chen et al., The Innovation, 2026***.

> 🔑 이 슬라이드는 우리에게 **"KG 구축"이 그들 프레임에서 이미 1급 응용 카테고리**임을 보여준다.
> 우리 T6(litdb 그래프층)이 유행 추종이 아니라 이 분야의 표준 축이라는 근거.

### 4b. SOH 예측용 LLM 워크플로 (슬 13)

LLM이 **파이프라인 전체를 설계·자동화·최적화**(전처리·feature selection·모델 선택·코드 생성·HP 튜닝·평가)하되
**예측 자체는 Random Forest / XGBoost / CatBoost**. User Side ↔ ChatGPT Side **8단계 structured prompt** 예시
(참조논문 업로드 → 방법론 요약 → 데이터셋 제출·RF 예측 → HP 튜닝 문의 → Bayesian 최적화 선택 → 전체 코드 요청 →
로컬 경로 지시 → 파라미터 설정·제약). 출처 ***Tuncel et al., Energy Reports, 2025*** ← 🔧 교정(종전 "Lu et al." 오기).

> 🔑 "LLM은 오케스트레이터, 예측은 고전 ML" — **우리 codoping_ml.py 의 ridge/LOOCV 구조와 같은 철학**.

### 4c. 온톨로지 → 지식그래프 → Graph RAG (슬 14)

```
온톨로지(개념·관계·속성 정의) → Data mapping → Knowledge Graph(KG) DB
   User Specification + System Prompt + User Prompt + Markdown Text
   → LLM 이 Node-Edge Extraction → DB(neo4j) → Embedding → Retrieval → Embedding → Query
   → Top-k Data → GPT-5.1 API → Response
```
왼쪽 온톨로지 실물은 **BMS 고장 도메인**(Battery System Parameter / Battery Fault Mode / Fault Symptom /
Battery System Component / Battery Fault Cause / Maintenance Measure / Fault Detection Method / Detection Tool·Operation
+ 속성 Fault Threshold·Repair Cost·Repair Time·Tool Accuracy·Standard Repair Time 등).

**Advantages of Graph RAG 3가지 (덱 주장)**
1. **Structured Retrieval** — 고립된 텍스트 청크가 아니라 **그래프로 연결된 근거**를 검색
2. **Multi-hop Reasoning** — 엔티티·관계·경로를 이어 **숨은 링크 추론**
3. **Traceable Answers** — 근거 경로를 보여줘 응답이 투명·신뢰 가능

### 4d. 고장 추론 KG (슬 15)
사전 구축된 fault DB → 노드·엔티티 추출 → **neo4j** KG. 노드 종류: 배터리 소재 · 고장 유형 · 고장 기구 ·
운전 조건 · 고장 원인 · 안전 조치 · 제조사/위치 · abuse 영향.
질의 "Which fault caused 'Signal abnormal A'?" → **Cypher 변환 → KG 부분그래프 검색 → context 주입** →
답변 *"Sensor A data are missing from 5.8 to 12 s, indicating a possible sensor or communication fault."*

### 4e. **ASSB 문헌 KG + GNN 링크 예측** ★★ (슬 16) — 우리와 가장 관련 · **Q1 종결**

황화물계 ASSB 문헌에서 **소재–공정–계면–성능–열화** 관계를 추출해 KG 구축.
**Graph RAG는 근거 문헌 검색을, GNN은 아직 연결되지 않은 잠재 관계의 예측을 담당.**

**🆕 DB 규모 (4× 확대 판독, neo4j 브라우저 패널 실물)**
- **Nodes (9,596)** — 16종: `Cell` `Claim` `Component` `CurveData` `DerivedFeature` `Factor` `FigurePanel`
  `Material` `Mechanism` `Metric` `MetricResult` `Paper` `ProcessCondition` `Sample` `TestCondition` `TestRun`
- **Relationships (18,145)** — 17종: `AFFECTS` `CONCLUDES` `DERIVED_FROM` `EXPLAINED_BY` `FOR_SAMPLE`
  `HAS_COMPONENT` `HAS_CURVE` `HAS_PROCESSING` **`MEASURED_AS`** `PRODUCES` `REALIZED_BY` `REPORTS`
  `SHOWN_IN` `SUPPORTS` **`TESTED_BY`** `UNDER_CONDITION` **`USED_IN`**
  🔧 교정 — 종전 digest의 `HAS_UNIT`/`USES`/`TESTED_IN` 은 우리 오기, 위 3개가 실제
- **Property keys** (알파벳순 첫 화면만 표시, 총 개수 불명): `ac_amplitude` `ac_voltage` `activation` `active`
  `active_component` `active_loading_mg_cm2` `active_material` `active_material_content_wt_pct`
  `active_to_swcnt_ratio` `active_wt_pct` `actual_S_wt_pct` `additive` `affiliation` `AgPF6_wt_pct` `air_exposure_s`

> 🔑🔑 **스키마가 "수치의 출처 맥락"을 노드로 들고 있다.** `MetricResult`–`UNDER_CONDITION`→`TestCondition`,
> `MEASURED_AS`, `FOR_SAMPLE`, `SHOWN_IN`→`FigurePanel` 조합은 **"이 값이 어떤 조건·어느 그림에서 나왔는가"**
> 를 그래프로 표현한다는 뜻이다. §8의 종전 평가("방법 맥락이 노드 속성으로 남는지 불명")를 **부분 하향 조정**해야 한다
> — 스키마 수준에선 남아 있다. 다만 *DFT functional·k-mesh 수준의 계산 방법 맥락*까지 담는지는 여전히 불명.
> `active_loading_mg_cm2` `air_exposure_s` `actual_S_wt_pct` 같은 키가 보이는 것으로 보아
> **제조·측정 조건 중심**이고 계산 파라미터 중심은 아닌 듯하다(추정, 단정 금지).

**🆕 KG-RAG 질의 실물** — *"Effects of Stack Pressure on Sulfide-Based ASSB Performance"* → GPT 5.1:
> "Stack pressure improves electrode–electrolyte interfacial contact and directly affects ion transport,
> interfacial resistance, cycle life, and capacity retention.
> **Based on Papers 1, 3, 7, 18, 19, and 30**, sulfide-based ASSBs with composite cathodes can maintain stable
> interfaces and high capacity retention even under **relatively low stack pressures of 5–10 MPa**, when uniform
> electrode–electrolyte contact and dense ion transport networks are formed. In contrast, **excessive pressure
> (>20–100 MPa) can induce Li penetration, particle cracking, and interfacial degradation.** Therefore, optimizing
> the stack pressure is essential."
> Multi-hop context (JSON): `{entities: [ionic conductivity], process: [stack pressure], …}`

> 🔑🔑 **우리 DEM 트랙의 스택압 축과 정면으로 겹치는 유일한 정량 서술**이다 —
> `papers/cronau2021_stack_pressure_ionic_conductivity.md` · `papers/doux2020_stack_pressure_assb.md` ·
> `papers/lee2024_multiphysics_dem_fem_initial_pressure_assb.md` 와 같은 명제.
> ⛔ 단 이건 **LLM이 문헌을 요약한 문장**이지 측정치가 아니다. **5–10 MPa / >20–100 MPa 숫자를 우리 문서에
> 인용하지 말 것** — 인용하려면 원 논문(Papers 1,3,7,18,19,30 이 무엇인지 미상)으로 내려가야 한다.
> 우리에게 유용한 건 숫자가 아니라 **"KG가 우리와 같은 질문을 이미 던지고 있다"는 사실**.

**GNN 예측 사례 2건 (4× 확대 판독)**

| | Case 1 — *Unseen but Correct Prediction* | Case 2 — *Literature-Consistent Prediction* |
|---|---|---|
| Factor | **Soft-acid cation doping (HSAB: Sn/Sb/As) in sulfide SE** | **Halide A in Li₆PS₅A electrolyte (Cl/Br/I)** |
| Issue | Low ionic conductivity | Low ionic conductivity |
| 예측 | **RESOLVED** | **RESOLVED** |
| P(resolved) | **0.57** | **0.55** |
| P(not_resolved) | 0.18 | 0.15 |
| P(unknown) | 0.25 | 0.31 |
| 근거 경로 | KG에 직접 연결이 **없던** 링크(붉은 점선)를 예측 | `Li₆PS₅Br` ←`REALIZED_BY`— `Halide A in Li₆PS₅A elect…` —`AFFECTS`→ `Interfacial chemical react…` —`AFFECTS`→ … —`MEASURED_AS`→ `Interfacial reaction energ…` |

🔧 교정 — Case 2 factor는 `Li₆PS₅Cl` 고정이 아니라 **`Li₆PS₅A` (A = Cl/Br/I) 일반형**이다.

> 🔑🔑 **Case 1이 우리 cascade의 `air_hsab` 축과 같은 명제다.** 우리는 HSAB soft-acid 도핑을
> 물리 기술자로 계산해서 순위를 매기고, 그들은 문헌 그래프에서 링크를 예측해 같은 결론에 도달했다.
> **완전히 다른 두 경로가 같은 답을 냈다 = 수렴 검증(convergent validation)**.
> 우리 원고에서 인용 가치가 크다. 단 **"우리 계산이 그들 예측을 검증했다"고 쓰지 말 것** —
> 시점·인과 주장 불가, "독립 경로의 일치"까지만.
> ⚠ 또한 `Sn` 은 **이상욱 랩의 가수분해 억제 도펀트**(LPSnSCl)와 같은 원소다. 세 갈래
> (문헌KG 예측 / 반응MD 기구 / 우리 스크리닝)가 **Sn 에서 만난다**.
> ⚠ P(resolved) 0.57 / 0.55 는 **과반을 겨우 넘는 값**이고 P(unknown) 이 0.25–0.31 이다.
> "GNN이 맞혔다"는 서술은 가능하지만 **"높은 확신으로"는 부정확** — 인용 시 확률까지 같이 쓸 것.

### 4f. LLM/RAG 문헌 계량분석 (슬 17) ★ — 방법론적으로 우리 것과 같은 종류

**Li-air 사례** (Clarivate Web of Science, Topic = "Li-Air Battery"):
```
5,689편 → (english O / review paper X 필터) 4,183편 → Select Papers → filtering
 → Top 1,000 Highly Cited Papers → PDF Download → GPT 5.1 로 {Energy Density}·{Weight Basis} 추출 → Data Extraction
```
🔧 교정 — 종전 "5,680편"은 우리 오기, 실제 **5,689편**.

박스플롯 *"Energy Density (<1500 Wh/kg) Distribution by Mass Basis"*, 질량 기준 6종:
**Whole Cell · Cell w/o Frame · Cell w/o Frame CC · Air Electrode · Active Material · Carbon** (500 Wh/kg 선 표시).

**발견 (덱 원문)**:
> "Energy densities based on total cell mass are generally below 500 Wh/kg. → Higher values are often calculated
> using lighter mass bases, such as Active Material, Carbon, or Electrode mass, and **may not reflect realistic
> whole-cell performance**. The 3 papers reporting energy densities above 500 Wh/kg mainly achieve this by
> **reducing electrolyte weight**."

> 🔑 이것은 **문헌의 보고 관행이 수치를 부풀린다는 메타분석**이고, **우리 깔때기의 정직성 장치와
> 정확히 같은 종류의 작업**이다(vacuous gate 표시, 절대 문턱 이식 시 empty gate 기록, 91→47은
> 물리 게이트가 아님 명시…). **이런 메타분석이 학회 발표 본론에 들어간다는 전례** — 우리 정직성
> 장치도 부록이 아니라 본론으로 낼 수 있다는 근거.

**ASSB 사례**: 임베딩·클러스터링 2D 맵 — `Sulfide` `Li₃PS₄` `LGPS` `Li₃PO₄` `superionic` `Borohydride`
`NASICON` `NASICON (LATP/LAGP)` `Si anode` `Li metal anode` `Li metal battery` `LCO cathode` `LFP cathode`
`halide` `fluoride` `(nano)composite` `Ceramic-polymer` `polymer` `PVDF based` `MOF/COF` `garnet` `perovskite`
`zn-battery` `nonflammable` `dendrite` + **"Predictive of k under Varying T & P"** 3D 반응면.
🔧 교정 — 종전 "LATP/LiPON"은 우리 오기, 실제 **LATP/LAGP** (LiPON 라벨 없음).

---

## 5. 03부 — Agentic AI (슬 18–24)

- **정의 (슬 18)**: 문제 해결 절차를 계획하고 외부 도구·모델과 상호작용해 작업을 수행하는 목표 지향 AI.
  Agent 1 내부 = Query → **Orchestrator (LLM + Google ADK)** ↔ Memory / Tools / Planning / Feedback → Output.
  옆에 **Multi-agent Protocol**: Discover Agent Capabilities → Share tasks → Update Task Information.
  4요소 도식: LLMs · Tools · Memory · Orchestration.
- **LLM Agents for battery research acceleration (슬 19)** 🆕 *재판독으로 편입*:
  ① **RAG 기반 배터리 도메인 Q&A** — Research Paper → ①Prompt ②Retriever ③Generation → Database;
  **BatteryBERT** 파인튜닝 QA 예시(Question "What's the device component?" + Context "LFP battery … LiFePO₄ cathode"
  → `[CLS] Tok₁ … [SEP] Tok_N … [SEP]` → Answer). ⚠ 덱의 정답 라벨이 **"Anode: LiFePO₄"** 로 적혀 있는데
  context는 LiFePO₄를 *cathode* 라고 말한다 — **덱 예시 자체의 라벨 오류**로 보인다(6× 확대 재판독 확인).
  ② **Property–Performance 예측 + 시뮬 실행** — "3C 충전 첫 1000 s 동안 SEI 성장은?" →
  입력 파라미터 5종(**SEI growth time / reaction rate constant / initial SEI thickness / charge-discharge rate /
  electrolyte concentration**) → 4장 결과 곡선(Reaction Constant / Initial Thickness 60 nm / Current Density at 3C /
  Concentration 1200 mol m⁻³). 답변 말미에 *"results provided by this function model are for reference only"*.
  > 🔑 **에이전트가 "간단한 물리 모델"을 스스로 세워 돌리고, 그 한계를 스스로 표기한다.**
  > 우리 digest의 "⚠ 인용 금지" 관례와 같은 장치가 응답 안에 들어 있다는 게 흥미롭다.
- **MCP (슬 20)**: LLM이 로컬 데이터·파일·API·CAD·시뮬레이션 도구를 표준 방식으로 호출.
  도구 아이콘 = FreeCAD · Blender · GitHub · COMSOL · MATLAB. LG 21700 M50 사양을 프롬프트로 주면
  **Extracted specifications**(Diameter **21.2 mm** / Length 70.2 mm / Weight 69.2 g / positive flat-top terminal /
  negative flat-bottom terminal with a metal ring / gray cylindrical 21700 form factor) 를 뽑고
  `create_document {'name':'LG_21700_M50_Battery'}` → `create_object {'obj_name':'Battery_Body','obj_type':'Part::Cylinder'}`
  → … → `get view {'view_name':'Front'}` 툴콜 시퀀스를 실행.
  🔧 교정 — 종전 "직경 21.7 mm"는 우리 오기, 덱은 **21.2 mm**.
- **FreeCAD MCP 실증 (슬 21)** — 전면 스크린샷 1장짜리 슬라이드. 🆕 **호스트가 Claude Desktop**
  (창 제목 `Claude`, 입력창 "Claude에게 답변하기", 모델 선택기 **Sonnet 4.5**) + FreeCAD MCP 서버.
  프롬프트 원문: *"Create an LG 21700 M50 cell model in FreeCAD using the specifications below. Show a vertical
  half-cut cross-section of the wound cell structure. Implement the jelly-roll as a continuous spiral structure,
  so that each layer remains connected without interruption."*

  | Category | Value / Structure | Note |
  |---|---|---|
  | Cell dimensions | **Diameter 21.2 mm, Length 70.2 mm** | Overall cell size |
  | Mandrel diameter | **2 mm** | Central core |
  | Jelly-roll outer diameter | **9.8 mm** | Outer diameter of the wound electrode stack |
  | Number of unit cells | **38** | Number of winding turns |
  | Layer sequence, inner to outer | Al (15 µm) → NCM (75 µm) → Separator (20 µm) → Graphite (85 µm) → Cu (10 µm) | Repeated layer structure |

  ⚠ **덱 내부 불일치(5× 확대 재판독 확인)**: 같은 슬라이드 우측 단면 도면의 치수는 **Ø46 mm × 80 mm
  (자유부 72 mm, 맨드릴 Ø4 mm, 두께 0.6 mm)** 로 **4680 규격**이다. 표(21700)와 도면(4680)이 다르다.
  슬 22의 생성 형상도 **Ø46 mm × 80 mm** 이므로, 도면은 21700 케이스가 아니라 **다른 예시의 재사용**일 가능성이 크다.
  ⛔ 두 세트를 섞어 인용하지 말 것.
- **LLM-Orchestrated Physics-Based Simulation (슬 22)**: 자연어("Can you run a model to evaluate OOO effects?")
  → Geometry Generation(코드 생성) → Generated geometry(**Ø46 mm × 80 mm**) → jelly-roll 단면(top view; Positive Tab /
  Positive CC / Positive Electrode / Separator / Negative Electrode / Negative CC / Negative Tab) →
  ("Suggest simulation parameters?") → Simulation Control & Analysis Optimization →
  결과장 4종(Temperature 20–40 °C · Current Density −2.0–2.0 A/m² · Potential −0.10–0.10 V · Li⁺ Concentration 0–3.0 mol/m³)
  + Analysis Results(Voltage vs Time 0–4000 s, Configuration A–D metric 막대) → 다시 파라미터로 되먹임.
- **Battery-Sim-Agent (슬 23)** ★ — *Battery-Sim-Agent, **ICLR 2026, under review***

```
Perception(Expert Knowledge · Exploration Knowledge) + Dynamic Memory
  → Scenario(First-Cycle Calibration / Long-horizon Degradation)
  → Structured Information(Cycle Protocols · Battery Modeling Framework · Cycle Description · Current Parameters)
  → Reasoning(Feedback Analysis → Physics-Informed Hypothesis Formation → Mechanism-Aware Update Proposal)
  → [Battery Simulator 와 Loop: Simulated Data ≈ Target Data 비교]
  → Physics Parameters(Electrochemistry · Physical Design · Dynamics) → Digital Twin Battery
  ↑ Multi-modal Feedback(Curve · Capacity · Step-by-step Loss · Degradation) ← Target Battery
```
| 지표 | 값 |
|---|---|
| Total Duration | **8565.8 s** (≈ 2.38 h) |
| Final RMSE | **0.5513** |
| Final MAPE | **2.4258** |
| Round Index | 0 → ~70 |

🔧 교정 — 종전 "8,965.8 s (≈2.5 h)"는 우리 오기, 5× 확대 재판독 결과 **8565.8 s**.
손실 곡선 4종(best_Q_mape = 용량 피팅 오차 / best_I_mape = 전류 / best_V_mape = 전압 / best_total_mape = 총오차)이
**계단형**으로 떨어진다 — 에이전트가 가설을 바꿀 때마다 뚝 떨어지는 형태. total 은 ~15.5 → ~2.5 수준.

> 🔑 **"에이전트가 물리 모델 파라미터를 스스로 피팅한다"의 정량 증거**. 우리가 서버 작업을 붙여넣기
> 루프로 도는 것과 대비된다. 다만 under review 이고 단일 케이스다.

- **End-to-end 비전 (슬 24)**: LLM Agent — Knowledge Retrieval / Model Setup → Geometry Generation / Simulation /
  Optimization → Result Analysis / Design Recommendation → **Battery Design Exploration** → **Battery R&D Acceleration**.

---

## 6. 04부 — BEARS ★★ 본체 (슬 25–39)

### 6a. 스케일 지도와 자동화 배경 (슬 25–26)

**슬 25** Battery Design Across Multiple Length Scales — 위줄:
Structure(Migration & Diffusion) → Interface(SEI interface growth) → Particle(Kinetics & Mechanics) →
**Electrode(Composite design, solid electrolyte)** → Electrochemistry(Full cell, Li metal cell);
아래줄: Product engineering → Cell design → Thermal simulation → Module design(Scale up) → BMS.

**슬 26** Automation Across Battery Materials and Manufacturing — 자율실험실 로봇(***Nature*, 624, 86–91 (2023)**)과
자동 셀 조립 라인(*JH Robotics Inc.*: 출하박스→최종 지그 삽입, 전압 체크·바코드·라벨링, FANUC force control +
iRvision 극성·유무 검증).

### 6b. 문제 — 전극 설계의 병목 (슬 27, 30)

**슬 27** Experimental Data → **Manual Bottleneck** → Analysis Results 구도.
- 실험 입력 5종: SEM(5 µm) · 입도분포(0.1–100 µm) · 단면 · 조성 파이(**Active Material 65 % / Conductive Additive 20 % /
  Binder · Others 나머지, 라벨 5 %**) · **캘린더링 조건(Pressure 100 MPa · Speed 10 m/min · Gap 50 µm · Temperature 25 °C)**
- 병목 4: Manual Analysis · **Setup Errors** · **Software Fragmentation** · Slow Iterative Review
  + 3줄: 실제 전극 구조·공정 정보 반영 부족 / 이미지분석–구조생성–조건설정–시뮬의 **분절 워크플로** /
  전문가·고가장비 의존과 긴 반복 개발 주기
- 결과 비교 (Design A / **B** / C): 에너지밀도 280 / **305** / 270 Wh/kg · 사이클수명 820 / **950** / 760 ·
  저항 1.2 / **0.9** / 1.4 **mΩ·cm²** · 기공률 35 / **38** / 32 %

**슬 30** Bottlenecks in Electrode Reconstruction and Generation —
Top-down(FIB-SEM / XCT): **"Over $5k per 1 scan"** + **Few weeks~** + Cost + Expertise.
Bottom-up: Structural Information(Loading Level·Density·Composition) → Modeling → Validation 이지만
**"Expert interpretation & decision-making"** 이 가운데 박혀 있다. 관측기법 해상도 스펙트럼(TEM/SEM/XCT/EELS/EBSD/SIMS,
10⁻¹⁰–10⁻⁵ m). 출처 *ACS Energy Lett. 2022, 7, 12, 4368–4378* / *ACS Energy Lett. 2024, 9, 10, 5225–5239*.

### 6c. 미세구조가 필요한 이유 (슬 29)

**τ = ε⁻ᵅ** (Bruggeman). **NMC α = 0.5 vs Graphite α = 1.9** — 같은 관계식인데 지수가 4배 다르다.
정의식도 함께: ε₀ = Ω_l/Ω, τ = L_e/L_s.
왼쪽 곡선은 τ₀ = ε₀^(−0.5 / −1 / −2 / −4) 별 **C-rate(80 % 방전용량 기준) vs 기공률** — High Capacity ↔ High Power 트레이드오프.
입력 변수: 기공률 · 굴곡도 · 입자 형상 · 형태 · 구형도 · 연결성 → 전해질 수송 · 굴곡도 · 활용률 · 분극 → **performance?**
출처 *ACS Energy Lett. 2022, 7, 12, 4368–4378* / *Adv. Energy Mater. 2014, 4, 1301278*.

### 6d. Physics–ML 파이프라인 (슬 28) 🆕 *재판독으로 편입* ★★

**Inputs**: active-material fraction, calendaring degree, solid content
**Outputs**: electronic conductivity, porosity, active surface area, density

```
01 합성 실험 설계(design of synthetic experiments — 제조 조건 공간 대표 샘플)
 → 02 제조 물리 모델링(Slurry → Drying → Calendering, manufacturing physical modeling)
 → 03 전극 물성 계산(전자전도도 · 비틀림도(tortuosity) · 활성 표면적 · 밀도)
 → 04 결정론적 학습(deterministic learning — 시뮬 결과를 빠르게 예측하는 surrogate 로 대체)
 → 05 다목적 최적화 및 설계(experimental cell design ↔ multi-objective optimization, Pareto)
 → ↺ 최적화된 전극 물성과 설계가 실험 설계로 피드백
```

> 🔑🔑 **이게 우리 DEM 트랙과 가장 직접 겹치는 슬라이드인데 종전 digest가 통째로 빠뜨렸다.**
> 구조가 `papers/ngandjong2021_dem_calendering_digital_twin.md` · `papers/duquesnoy2023_ml_multiobjective_manufacturing_optimization.md`
> (ARTISTIC 계보)와 **단계 대 단계로 대응**한다 — 슬러리→건조→캘린더링 DEM, 물성 추출, surrogate, 다목적 최적화.
> ⇒ **BEARS는 ARTISTIC 파이프라인을 "에이전트가 운전하는" 버전**으로 읽는 게 정확하다.
> 우리 DEM 트랙의 상대 위치는 "새 물리"가 아니라 **"건식 압밀 + granular constriction + 소성"** 이라는
> `positioning_vs_geodict.md` 의 좁힌 정의가 여기서도 유효하다.

### 6e. 모델 해상도 사다리 (슬 31) 🆕 *재판독으로 편입*

Problems(Hidden internal states SOC/SOH/degradation · Complex dynamics chemical/thermal/electrical ·
Varied operating conditions **temperature, pressure**)
→ **ECM**(fast system-level) → **Physics-based**(coupled transport ∂c/∂t = ∇·(D_eff∇c) + a_s j_n/F 와
Butler–Volmer i_n = i₀[exp(α_aFη/RT) − exp(−α_cFη/RT)])
→ **Microstructure-resolved**(particle arrangement + pore network, local heterogeneity, Li⁺ 농도장)
→ **Need for automation**(Geometry ↔ Meshing ↔ Simulation ↔ Analysis 순환, "Executable workflow required")

배너: **"As model resolution increases, automated workflows become essential for geometry, meshing, simulation, and analysis."**

### 6f. 선행 연구 인용 (슬 32) 🆕 *재판독으로 편입* ★

**Reference Work: Stochastic Electrode Generation and ML Surrogates — Ying Shirley Meng @ U Chicago**
논문 실물: *"Improved Rate Capability for Dry Thick Electrodes through Finite Elements Method and Machine
Learning Coupling"* — Mehdi Chouchane, Weiliang Yao, Ashley Cronk, Minghao Zhang, Ying Shirley Meng,
***ACS Energy Lett.* (2024), 9, 4** (received 2024-01-24 / accepted 2024-03-11 / published 2024-03-15).

Scheme 1 워크플로: **Library of Real Particles → Stochastic Generation of Electrodes → FEM Simulations →
Extract the Average SOD(state of discharge) for each Particle → ML Algorithm (Random Forest)**.
검증: ML Predictions vs FEM State of Discharge 패리티(0.2–1.0, over/underestimation 대각), FEM 단면 vs ML 예측 단면 비교.

> 🔑 **Chouchane 은 ARTISTIC(Franco) 계보에서 Meng 그룹으로 넘어간 사람**이고, 이 논문이 BEARS의 직접 선행이다.
> 우리 `papers/` 에 **미보유** — DEM/미세구조 트랙 확보 1순위 후보. `kb/open_items.md` 에 넣을 것.

### 6g. 계보 (슬 33) — 이 분야의 시간축 (2트랙 병기)

**전극 모델링 트랙**
```
1990s Early Porous Electrode Models (1993 Doyle–Fuller–Newman; 1994; 1995)
 → 2009–2012 Microstructure Characterization (2010 Shearing, graphite 3D 미세구조)
 → 2013–2016 Image-based Modeling (2013 Cooper, LiFePO₄ 미세구조 불균일)
 → 2015–2020 Stochastic Reconstruction & ML (2015 Xu, ML 기반 설계 표현)
 → 2020–2025 Generative AI-based Microstructure Generation (2020 Gayon-Lombardo, "Pores for thought" GAN)
가운데 박스: 1990s–2010s 다공성 전극 모델 → 2010–2020 3D imaging & image-based → 2020–2025 Generative AI
             → 2023–2026 Tool-using LLM agents → **BEARS**
```
**LLM 트랙**
```
LLM·Transformer (2017 Vaswani Attention / 2019 Devlin BERT / 2020 Brown GPT-3)
 → RAG·Tool Usage·Agent Init (2020 Lewis RAG / 2022 Yao ReAct / 2022 Schick Toolformer)
 → LLM Multi-Agent Framework (2023 Park Generative Agents / 2023 Shen HuggingGPT / 2023 Microsoft AutoGen /
                              2023 LangChain·LangGraph / 2024 Chen survey)
 → Battery Electrode Specialized LLM-Agent (2025 Liu ChatBattery / 2025 Robson Zn-ion 전해질 아이디어 생성(Wiley) /
                              2025 BatteryAgent / 2025 BATTERY-SIM-AGENT)
 → Agent Skill Acquisition & Composition (2026 Li "When Single-Agent with Skills Replace Multi-Agent Systems and
    When They Fail" / 2026 Wei "Towards Compositional Generalization of LLMs via Skill Taxonomy Guided Data
    Synthesis" / 2026 Shi "Evolving Programmatic Skill Networks")
 → **BEARS**
```
🔧 교정 — Toolformer는 **2022**(종전 2023 표기), BATTERY-SIM-AGENT는 **2025 항목**(종전 2026 표기), **CAMEL-AI는 덱에 없다**.

> 🔑 마지막 칸 3편이 전부 **"스킬"** 논문이다. 즉 BEARS의 자기 위치 주장은 "다중 에이전트"가 아니라
> **"스킬 조합"** 쪽이다 — 우리 T7(3계층 스킬 로딩)의 근거 문헌군이 여기 다 있다.

### 6h. BEARS 구조 (슬 34, 39)

**닫힌 루프 8단계**: `1 Parameter Identification → 2 Geometry → 3 Materials → 4 Physics → 5 Meshing →
6 Simulation/Solver → 7 Validation → 8 Analysis` (+ 역방향 **Debugging**, 바깥 **Optimization** 루프,
왼쪽 **Reverse Design**, 7↔실험 **Experimental Validation**: Model ↔ Experiment verification)

**🆕 Key tools 실물 (4.5× 확대 판독)**
| 역할 | 도구 |
|---|---|
| Geometry (3D Modeling) | **Blender** |
| Validation (Verification) | **MATLAB** |
| Simulation (FEM) | **COMSOL** |
| Analysis (Data & Code) | **Python** |

**전문 에이전트 5 + Main + User**
| 에이전트 | 역할 | 스킬 수 |
|---|---|---|
| **Analyzer** | SEM Image Analysis & 3D Reconstruction — SEM에서 개별 입자 분할, 단일 이미지로 3D 메시 복원, 입자 형태(크기·형상·종횡비) 분석 | *표기 없음* ⚠ |
| **Generator** | Electrode Structure Generation — 다중 packing 알고리즘으로 3D 미세구조 생성. **구형·custom-shaped·bimodal 입자 + 다분산 입도** 지원 | **[3] geometry skills** |
| **Fabricator** | 3D Visualization & Export — Blender 렌더링 파이프라인, 다중 포맷 export, **물리엔진으로 캘린더링 시뮬** | **[6] visualization & export skills** |
| **Simulator** | 자동화된 **COMSOL Multiphysics** 3D 전기화학 해석 — geometry import → post-processing 완전 자동 | **[5] simulation skills** |
| **Validator** | Structural Analysis & Validation — 생성 전극에 **8종 구조 검증 지표**(형태·수송·통계) 적용 | **[8] validation skills** |
| Main | 총괄 (User ↔ 5 에이전트 사이 SEM Data / 3D Mesh / Packed Geometry / Validation Report / Simulation Results 중계) | — |

⚠ 5개 에이전트 스킬 수 합 = 3+6+5+8 = **22 + Analyzer(미표기)**. 슬 35의 **"40+ Modular Skills"** 와 맞지 않는다.
"40+"는 라이브러리 전체, 대괄호 숫자는 **해당 에이전트에 바인딩된 수**로 읽는 게 자연스럽지만 덱에 설명은 없다 — 추정 금지.

**슬 39 = end-to-end 전체 도면**
- **INPUTS** — *Research Intent*(Hypothesis/Goal · Recipe/Conditions · Target performance) ·
  *Knowledge Sources*(Papers/Literature · Material DB & Parameters · **Prior Runs & Results** · **Failure Cases & Notes**) ·
  *Structure Descriptors*(SEM images(morphology) · PSD, Porosity, Loading · Electrode Composition · Thickness, Tortuosity(exp.))
- **BEARS ORCHESTRATION ENGINE** — Planner/Orchestrator (**LLM-Driven Sequential Pipeline**):
  Decompose → Plan → Execute → Monitor → Iterate (Task decomposition · Tool selection · Progress monitoring · Result interpretation)
  | # | 단계 | 담당 | 세부 | Skills 산출 |
  |---|---|---|---|---|
  | 1 | Parameter Extraction | Analyzer | 문헌 파싱 · 이미지/SEM 분석 · RAG retrieval | Parameter set |
  | 2 | Geometry Generation | Generator | packing 알고리즘 · 물질 고유 물성 · 전극 레시피 생성 | 3D Geometry |
  | 3 | Fabrication & Meshing | Fabricator | Blender 렌더링 · settling · 전극 제조 규칙 · 메시 단순화 | FEM-ready Mesh |
  | 4 | Geometry Validation | Validator | 메시 품질 · **Bruggeman references** · 물리 정합성 · 기공률/PSD | Validated Geometry |
  | 5 | FEM Simulation | Simulator | 물리 설정 · 경계조건 · **solver 실행 (DIS / EIS / P2D)** | Simulation Results |
- **Debug & Review**: solver log & error detection · hypothesis generation · auto-fix / parameter sweep ·
  external code review · verification reports — **Failure → Diagnose → Fix → Re-run**
- **Memory & Knowledge Bank** (= BEARS Knowledge Bank): auto-memory(run logs, params, results, fixes) ·
  **docs/knowhow (INDEX.md)** · solver settings & recipes · failure patterns & solutions · **GitHub issues & comments**
  — **Experience → Reuse → Continuous Improvement**
- **OUTPUTS**: Particle · Electrode · Validate · Simulation · **Next run recommendations**
- **4 기둥**: Reproducible workflow · Expert knowledge reuse · **Failure-aware debugging** · Scalable automation

> 🔑🔑 **"docs/knowhow (INDEX.md)"** — 그들 메모리 층의 이름이 **문자 그대로 우리 `litdb/INDEX.md`** 다.
> 우리가 이미 갖고 있는 것(INDEX.md + 실패 기록 + git 이력)이 그들 설계도의 한 칸이라는 뜻 —
> **§7 "지식층" 행의 평가를 "완패"가 아니라 "같은 부품, 다른 배선"으로 읽어야 한다.**
> 우리에게 없는 건 저장소가 아니라 **그 위의 orchestration 루프**다.

### 6i. **Modular Skills 3계층** ★★ (슬 35) — 우리가 가장 직접 가져올 수 있는 것

> "Skills는 Agent에 내장된 **경량 instruction module**로, 복잡한 추론이나 코드 생성 없이 특정
> 작업을 효율적으로 수행하여 **낮은 토큰 사용량과 신뢰도 높은 출력**을 보장함"

**40+ Modular Skills**, 8 범주 (덱 원문 요약)
| 범주 | 내용 |
|---|---|
| Image analysis | SEM 분할, 단일 이미지 3D 복원, 입자 형태 분석(크기·형상·종횡비) |
| Geometry | 구형·custom-shaped·bimodal 입자 전극 생성, 다중 packing 알고리즘·입도분포 |
| Visualization & export | 3D 렌더링, 다중 포맷 export, **캘린더링 물리 시뮬**, 자동 viewport 캡처 |
| Mesh processing | 메시 단순화·remeshing·watertight 복구·FEM 최적 형상 준비 |
| Validation | 기공률·굴곡도·입도분포·표면적·연결성·공간통계 등 종합 구조 지표 |
| Simulation | 반쪽셀/풀셀·기계응력·임피던스·캘린더링, **반복 버전 관리** 포함 전기화학 해석 |
| Debugging & Analysis | 결과 추출, solver 진단, 수렴 분석, **자동 오류 복구** |
| Utility | 파라미터 변환, 문헌 검색, 파이프라인 오케스트레이션, 환경 설정, 리포트 생성 |

**3-Level hierarchy** ★
| Level | 내용 | 로딩 |
|---|---|---|
| **1** | Metadata (YAML) | **항상 로드**, ~100 #tokens |
| **2** | Body (Markdown) | **스킬이 트리거될 때만**, < 5k |
| **3** | Bundled files (scripts, data — Python/JS/DB/MCP/BASH) | **에이전트가 필요할 때만** |

동반 그래프: x축 10 → 10,000 (도구/스킬 수 추정), y축 **Selection Accuracy (%)**.
**Flat Selection (Bounded Capacity)** 은 100 → ~100개 근처에서 급락해 **Stage 2 Cognitive Overload (Flat)** 로 붕괴하고,
**Hierarchical Routing** 은 **Stage 1 High Efficiency Zone** 을 지나 10,000까지 80 % 대를 유지 = **Hierarchical Solution**.
출처 **arXiv:2601.04748** ← 🔧 교정(종전 2601.04746 오기, 6× 확대 재판독).

> 🔑🔑 **우리 repo가 정확히 Level 2 만 있는 상태다.** `CLAUDE.md`(항상 로드, 근데 100 토큰이 아님) +
> `tools/*.py`(Level 3) 는 있지만 **Level 1 메타데이터 층이 없어** 매번 전체를 읽어야 한다.
> 이게 우리 세션이 컨텍스트를 태우는 구조적 이유고, **T7 로 실행 항목화**한다.
> ⚠ 단 그래프의 x축 라벨이 판독되지 않는다(도구 수인지 컨텍스트 길이인지 불명) — **"~100개에서 급락"은 추정**.

### 6j. 실증 결과 (슬 36–38)

**슬 36 — 단일 SEM 이미지 → 3D 입자 라이브러리** (Analyzer Agent)
```
Input image → [U-Net encoder–skip–decoder 로 point prompt 생성]
            → SAM V2 (Image encoder ViT-H + Prompt encoder + Mask decoder) → Final segmentations
            → Multi-view Diffusion Model → Sparse-view Large Reconstruction Model (LRM)
            → Mesh preparation for FEM (Dense → Sparse)
            → clustering → 재사용 가능한 particle library
```
**🆕 정량 (5× 확대 판독)**
- **Graphite Particle Library: 11 STL Templates** (image → 3D reconstruction, PCA 산점도 + 3면도 그리드)
- **NMC 811 from FIB-SEM reconstruction: 2,054개 입자 → 6 cluster 대표**
  (C0 elongated · C1 concave · C2 large angular · C3 mid concave · C4 large · C5 small concave)
- Dense → Sparse 메시 형상지표 보존: watertight=True 유지, sphericity **−0.02 %**, aspect **−0.21 %**,
  elongation **+0.25 %**, flatness **−0.04 %** (⚠ face 수 절대값은 원 raster 한계로 판독 불가 —
  dense 5만 대, sparse 800 규모로만 읽힘. **숫자 인용 금지**)

**슬 37 — 전극 생성·검증** (Generator + Fabricator + Validator 협업)
- **DOE-based generation under fixed loading**
  - Fixed Condition: Material **Graphite** · Footprint **30 × 30 µm** · loading **8 mg/cm²** · wt% **95:3:2**
    🔧 교정 — 종전 "30 × 38 µm"는 우리 오기
  - Variable knobs: Particle template · **PSD / D50** · architecture (Single, Binary, Gradient)
- **Electrode library — "Graphite Structure Space (D_eff = D · ε^β)"**: Through-plane Tortuosity (τ_z) vs Porosity,
  가이드 곡선 **α = 1.9 (Ebner) / α = 1.7 / α = 1.5 (sphere)**.
  **n = 80 = Single (55) + Binary (19) + Gradient (6)** 🆕
- **대표 5개**(🔧 교정: `SPH10` 아니라 **`SPH010`**): **SPH010**(sphere, τ_z ≈ 1.55 · ε ≈ 0.48) ·
  **HC01**(single, τ_z ≈ 1.92) · **HC06**(binary, ≈ 1.90) · **HC05**(binary, ≈ 1.81) · **GRD01**(gradient, ≈ 1.93)
  (τ_z·ε는 그림에서 읽은 **근사 좌표** — 인용 시 "≈" 유지)
- 구조별 PSD 히스토그램 + Pore Size vs Z 프로파일 5쌍 (각 패널에 porosity·τ(z)·특성 pore 크기가 적혀 있으나
  원 raster 한계로 **자릿수 판독 불가 → 인용 금지**)

**슬 38 — 고율 방전 성능** ★ 정량 결론 (Simulator Agent)
BEARS 지시: *"Run electrochemical simulations at **0.5C, 1C, 2C, and 3C** for all generated electrodes.
Identify and analyze the best and worst performers at each rate."*

**3C Discharge Capacity Ranking (Core 5)** — 🔧 **순위 교정** (6× 확대 재판독)
| 순위 | 구조 | 3C 방전용량 (mAh/g) |
|---|---|---|
| 1 | **HC05 binary** | **56.8** |
| 2 | HC06 binary | 53.4 |
| 3 | GRD01 gradient | 45.4 |
| 4 | SPH010 sphere | 33.6 |
| 5 | HC01 single | 16.8 |

- 덱 본문: *"3C 조건에서 binary 구조는 막히지 않은 전해질 경로로 인해 single 구조보다 **약 3배** 높은 용량을 유지"*
  → 실제 비교쌍은 **HC05(56.8) vs HC01(16.8) = 3.38×**. 🔧 종전 digest가 "HC06 vs HC01"이라 적은 것은 오기.
  그림에서도 빨간 테두리로 강조된 두 구조가 **HC01 single 과 HC05 binary** 다.
- 🆕 **막대 그림의 두 화살표가 트레이드오프를 명시한다**:
  **0.5C 에서는 HC01(single) → HC05(binary) 로 −6.4 %** (저율에선 binary가 손해),
  **3C 에서는 +70.4 %** (= (56.8−16.8)/56.8, binary 기준 상대 격차).
  ⇒ **"binary가 항상 낫다"가 아니라 "고율에서만 역전된다"** 가 정확한 서술.
- 기구 시각화: 3C SOC 분포(Z 0–70 µm vs SOC 0–0.6, lithiation 스케일) · 전해질 전위 φ_l(−0.7 → 0.0 V) ·
  **electrolyte current density vector** 맵(HC01 은 경로가 막혀 상단만 반응, HC05 는 하부까지 전류가 뻗음)

> 🔑 이 결과 자체가 **우리 DEM 트랙(bimodal AM 시스템)과 같은 물리**다 — bimodal 입도가 수송
> 경로를 여는가. 우리는 DEM(접촉·응력·percolation)으로, 그들은 FEM+전기화학으로 본다.
> **상보적이고, 우리 DEM 결과를 그들 언어로 번역할 수 있다.**
> 🔑🔑 🆕 **더 중요한 건 순위의 비단조성**: **SPH010 은 τ_z 가 1.55 로 5개 중 가장 낮은데 3C 순위는 4위**다.
> 즉 **through-plane 굴곡도만으로 rate 성능이 설명되지 않는다**(활성 표면적·국소 경로 연결성이 따로 작동).
> 우리 DEM/BVSE 문서에서 "굴곡도 하나로 순위를 매기지 않는다"는 규율의 **외부 근거**로 쓸 수 있다.
> ⚠ 단 SPH010 은 입자 형상 자체가 다른(구형) 케이스라 변수 분리가 안 돼 있다 — **단정 금지, 관찰까지만**.

---

## 7. 우리 대비 — 축별 판정 ★★

| 축 | 그들 (BEARS) | 우리 (이 repo) | 판정 |
|---|---|---|---|
| **문제 층위** | 전극 미세구조 ~ 셀 (µm–mm) | 원자·결정 (Å–nm) | **직교 — 상하류**. 우리 M5(P2D export)가 접점, 슬 39가 **P2D 를 명시** |
| **지식층 구조** | neo4j KG **9,596 노드 / 18,145 관계** + Graph RAG + **GNN 링크예측** | litdb 118 MD + INDEX.md + comparison_vs_ours.md (평면) | **그들 우위(구조)·우리 우위(정합)**. §8 참조 |
| **스킬/컨텍스트 관리** | 40+ 스킬 **3계층 로딩** (L1 YAML ~100 tok) | CLAUDE.md + tools/ (Level 1 없음) | **완패 — 즉시 채택 대상 (T7)** |
| **실패 처리** | Failure-aware debugging, **Failure → Diagnose → Fix → Re-run**, GitHub issues 를 메모리로 | kb/open_items.md + 탈락 명단 + vacuous 표시 | **호각**. 우리 쪽이 "실패의 종류"를 더 세분, 그들은 **루프에 물려 있음** |
| **메모리 저장소** | auto-memory + **docs/knowhow (INDEX.md)** + solver recipes | git 버전 db + INDEX.md + digest | **같은 부품** 🆕 — 차이는 저장소가 아니라 **그 위의 orchestration** |
| **재현성** | Reproducible workflow 주장 | git 버전 db + 빌더 스크립트 **2회 실행 md5 동일** 강제 | **우리 우위 (검증 방식이 구체적)** |
| **닫힌 루프 자동화** | 8단계 완전 자동 + 다음 실행 추천 | 붙여넣기 루프(사용자 경유) | **완패** — 단 우리는 원격 서버 다수·자원 게이트 문제 |
| **정직성 장치** | 슬 17 Li-air 메타분석 1건, 슬 19 "for reference only" 자기표기 | 깔때기 vacuous·순서민감도·컷 지배 경고·empty gate 기록 | **우리 우위 (체계화 수준)** |
| **검증 상태** | 다수 under review / arXiv | db 값은 재현 스크립트 동반 | 인용 시 상태 병기 필요 |
| **미세구조–성능** | 80 전극(55/19/6) · **3C 에서 HC05 binary 3.38×**, 단 **0.5C 는 −6.4 %** | DEM 트랙(접촉·응력·percolation) | **같은 물리, 다른 도구 — 상보** |
| **제조 물리 파이프라인** 🆕 | 슬 28 = 슬러리→건조→캘린더링 물리 모델 → 물성 → surrogate → 다목적 최적화 | 우리 DEM(건식 압밀·granular constriction·소성 MPM) | **ARTISTIC 계보와 같은 골격** — 우리 차별은 *건식·압밀 물리* 로 좁혀 유지 |

---

## 8. 지식층 정면 비교 — 우리가 이기는 지점 ★ (재판독 반영)

그들 KG의 강점은 **구조(멀티홉·링크예측)**, 우리 litdb의 강점은 **정합(alignment)** 이다.

| | 그들 KG/Graph RAG | 우리 litdb |
|---|---|---|
| 규모 | **9,596 노드 / 18,145 관계** (16 노드종 · 17 관계종) | digest 118편 + 덱 3편 + 서베이/개념 |
| 추출 | LLM이 PDF에서 노드·엣지 자동 추출 | 사람+에이전트가 digest를 **논문 수준으로 재서술** |
| 방법 맥락 | 🆕 **스키마엔 있다** — `MetricResult`·`TestCondition`·`UNDER_CONDITION`·`MEASURED_AS`·`SHOWN_IN→FigurePanel`. 다만 property key가 **제조·측정 조건 중심**(`active_loading_mg_cm2`, `air_exposure_s`)이라 *계산 방법 맥락*(functional·k·supercell)까지 담는지는 불명 | digest §DFT/계산 방법에 functional·k·supercell·무질서 처리까지 명시 |
| 우리 값과의 대조 | 없음(문헌 내부 그래프) | **`comparison_vs_ours.md` + 각 digest §우리 대비** = 수작업 정합층 |
| 인용 금지 규칙 | 없음 | **"소환값 — 우리 db 절대값과 섞지 말 것"**, 특정 수치 인용 금지 지시가 digest 안에 박혀 있음 |
| 오류 정정 이력 | 불명 | 오귀속 철회 사례가 **17개 파일 횡단으로 기록**(Schlem·Deng), **덱 재판독 대장**(이 문서 §15) |
| 추론 | **GNN 링크예측**(P(resolved) 0.55–0.57) | 없음 — 사람이 읽고 연결 |

> **결론(재판독 후 수정)**: 우리가 KG로 가야 할 이유는 "검색이 안 돼서"가 아니라 **"멀티홉 가설 생성이 없어서"**다.
> 반대로 **KG로 가면서 잃으면 안 되는 것은 계산 방법 맥락과 인용 금지 규칙**이다 —
> 그들 스키마는 *실험 조건* 맥락은 잘 잡지만 *계산 파라미터* 맥락 노드는 안 보인다.
> → T6(litdb 그래프층)은 **digest를 대체하는 게 아니라 digest 위에 얹는 것**으로 설계하고,
> **`Method`/`Functional`/`kMesh` 노드타입을 우리 쪽 고유 확장으로 넣는다**(그들 스키마엔 없는 칸).

---

## 9. 우리가 가져올 것

`kb/projects/symposium_2026_competitive_analysis.md` 의 **T5–T8**.

1. **3계층 스킬 로딩** (슬 35) — Level 1 메타데이터(YAML ~100토큰) 층 신설. 비용 대비 효과 최대. **T7**
2. **litdb 그래프층 + 링크 예측** (슬 16) — digest 위에 얹는 방식. Case 1(HSAB Sn/Sb/As)이
   우리 cascade와 수렴한 것을 **원고 인용 소재**로 확보. 스키마는 그들 16/17종을 참고하되
   **계산 방법 노드는 우리가 추가**. **T6**
3. **실패 사례를 1급 입력으로** (슬 39) — `Failure → Diagnose → Fix → Re-run` 루프. 우리 `kb/open_items.md`·
   탈락 명단을 "다음 실행 추천"의 입력으로 쓰는 구조. 이미 절반은 있다.
4. **P2D/FEM 파라미터 export (M5)** — 소비자가 특정됐다. 슬 39 solver 칸이 **DIS/EIS/P2D**.
   우리 σ/Ea/C_ij 가 그들 ③층 입력.
5. **DEM 결과의 전기화학 번역** — 우리 bimodal DEM ↔ 그들 3C HC05 3.38×. 같은 명제의 두 증거.
   **단 0.5C −6.4 % 트레이드오프까지 같이 옮길 것** (한쪽만 쓰면 우리가 문헌을 부풀리는 셈).
6. **도입부 서사** (슬 8) — K배터리 −17.3 % / SK온 원가산출 700배. 출처 명시 후 차용.
7. 🆕 **Chouchane 2024 (ACS EL 9, 4) 확보** (슬 32) — 우리 DEM/미세구조 트랙의 직접 선행. `papers/` 미보유.
8. 🆕 **"구조 검증 8종 지표"** (슬 34 Validator) — 우리 DEM 산출 구조에도 같은 종류의 검증 세트가 필요하다.
   덱엔 항목이 안 적혀 있으니 arXiv 확보 후 채울 것.

---

## 10. 주의 / 한계

1. **검증 상태**: BEARS(arXiv), Battery-Sim-Agent(**ICLR 2026, under review**), 슬 33의 다수 항목이
   arXiv. **peer-review 통과 결과로 인용 금지**.
2. **슬 37–38의 n**: 80개 생성 중 **5개만** 전기화학 검증. "80개를 시뮬레이션했다"고 쓰면 오독.
   "3C에서 3.38배"는 **HC05(binary) vs HC01(single)** 두 구조의 비교다. 🔧 (종전 HC06 표기 교정)
3. **슬 38 트레이드오프 누락 주의**: 0.5C에서 binary는 single 대비 **−6.4 %**. 고율 이득만 인용하면 왜곡.
4. **슬 35 "40+ Skills"** 는 개수 주장이고, 각 스킬의 신뢰도 근거는 덱에 없다.
   "낮은 토큰·높은 신뢰"는 주장이지 측정치가 아니다. 에이전트별 표기 합(22+α)과도 안 맞는다.
5. ~~슬 16 KG 규모 판독 불가~~ → **2026-08-03 종결**: 9,596 노드 / 18,145 관계.
   단 **소스 논문 편수는 여전히 불명**(RAG 답변이 "Papers 1, 3, 7, 18, 19, 30"을 인용 → 최소 30편 이상 시사, 추정).
6. ~~슬 5 논문·인용 수 판독 불가~~ → **2026-08-03 종결** (표 §3). 단 **원 그림 출처가 슬라이드에 없다** — 인용하려면 추적 필요.
7. **디지털 트윈 용어** — 그들은 쓰고 우리는 안 쓴다(지도교수 방침). 비교 서술 시 우리 방침을
   그들 비판처럼 쓰지 말 것.
8. **슬 8 시장 수치**는 SNE리서치 **단월(1월)** 기준이다. 연간으로 오독 금지.
9. 🆕 **슬 21 표(21700) vs 도면(Ø46×80 = 4680) 불일치** — 두 세트 혼용 금지.
10. 🆕 **슬 16 stack pressure 문장(5–10 MPa / >20–100 MPa)은 LLM 요약문**이지 측정치가 아니다. **우리 문서 인용 금지.**
11. 🆕 **슬 37 패널 내 porosity·τ 숫자, 슬 36 mesh face 수**는 원 raster 한계로 판독 불가 — 추정 금지.
12. 🆕 **슬 19 BatteryBERT 예시의 정답 라벨("Anode: LiFePO₄")은 덱 자체 오류**로 보인다. 인용 금지.

---

## 11. 미해결 질문 (구술 txt / 논문으로 닫을 것)

| # | 질문 | 상태 | 닫는 방법 |
|---|---|---|---|
| Q1 | ASSB KG의 노드/관계 실제 규모 | ✅ **종결 2026-08-03** — 9,596 / 18,145 | 재판독 (§4e) |
| Q1b | KG **소스 논문 편수**와 수집 기준 | ⏳ 미해결 | 구술 / 논문 |
| Q2 | GNN 링크예측의 **평가 프로토콜**(negative sampling, 시간분할 여부) — Case 1이 진짜 "unseen"인지 | ⏳ 미해결 (확률값 0.57/0.18/0.25 는 확보) | 논문 |
| Q3 | BEARS 3계층 스킬의 **토큰 절감 실측치** | ⏳ 미해결 — 출처 번호만 교정 | **arXiv:2601.04748** |
| Q4 | Battery-Sim-Agent 의 **베이스라인**(수동 피팅 대비 RMSE) | ⏳ 미해결 (8565.8 s / RMSE 0.5513 확보) | ICLR 제출본 |
| Q5 | 80 전극 중 5개 선정 기준 | ⏳ 부분 — 구조공간 그림상 **τ–ε 공간을 넓게 덮게** 뽑은 것으로 보이나 명시 기준 없음 | 구술 |
| Q6 | 우리 σ/Ea 를 그들 P2D에 넣으려면 **어떤 형식**이 필요한가 | ⏳ 미해결 — 슬 39가 **DIS/EIS/P2D** 로 좁혀줌 | 구술 — **협업 제안 각도** |
| Q7 🆕 | Validator 의 **"8종 구조 검증 지표"** 목록 | ⏳ 미해결 | arXiv (BEARS) |
| Q8 🆕 | "40+ skills" 와 에이전트별 [3]/[5]/[6]/[8] 표기의 관계 | ⏳ 미해결 | arXiv (BEARS) |

> Q6은 질문이자 **협업 제안 포인트**다. 우리는 파라미터를 만들고 그들은 소비한다.

---

## 12. 인용 가능 문장

- "FIB-SEM/XCT 기반 전극 재구성은 스캔 1회에 $5,000 이상과 수 주가 든다 — 그래서 가상 생성이 필요하다" (슬 30)
- "같은 Bruggeman 관계식이어도 NMC α = 0.5, 그래파이트 α = 1.9 로 굴곡도–기공률 지수가 4배 다르다" (슬 29)
- "LLM은 파이프라인을 조율하고 예측 자체는 고전 ML(RF/XGBoost/CatBoost)이 맡는 분업이 실무 표준으로 자리잡고 있다" (슬 13, Tuncel 2025)
- "문헌의 에너지밀도 보고는 질량 기준이 통일돼 있지 않아, 전셀 기준으로 환산하면 대부분 500 Wh/kg 미만이다" (슬 17, Li-air 5,689→4,183→1,000편)
- 🆕 "모델 해상도가 올라갈수록 geometry·meshing·simulation·analysis 를 잇는 자동화 워크플로가 필수가 된다" (슬 31 배너)
- 🆕 "전극 미세구조 자동화 파이프라인의 최신 형태는 스킬 단위 다중 에이전트이며, 그 메모리 층은 run log·실패 패턴·
  GitHub 이슈까지 포함한다" (슬 39)
- 🆕 "동일 로딩·동일 조성에서 생성한 80개 흑연 전극 중 bimodal 구조는 3C 고율에서 단봉 구조보다 3배 이상의 용량을
  유지하지만, 0.5C 저율에서는 오히려 6 % 낮다" (슬 37–38) ⚠ 덱 소환값, 절대값 인용 금지

---

## 13. 이 덱과 우리 `papers/` 의 연결

| 덱 항목 | 우리 정본 | 관계 |
|---|---|---|
| 슬 16 KG-RAG "stack pressure 5–10 MPa" | `cronau2021_stack_pressure_ionic_conductivity.md` · `doux2020_stack_pressure_assb.md` · `lee2024_multiphysics_dem_fem_initial_pressure_assb.md` | **같은 명제, 우리 쪽이 정본** — 덱 숫자 인용 금지 |
| 슬 16 Case 1 HSAB Sn/Sb/As | 우리 cascade `air_hsab` + `zhu2020_air_stable_se_design_principles.md` | 독립 경로 수렴 |
| 슬 28 Physics–ML 파이프라인 | `ngandjong2021_dem_calendering_digital_twin.md` · `duquesnoy2023_ml_multiobjective_manufacturing_optimization.md` | **같은 골격(ARTISTIC 계보)** |
| 슬 32 Chouchane 2024 | **미보유** ⛔ | 확보 1순위 |
| 슬 33 계보 2020 Gayon-Lombardo GAN | 미보유 | 필요시 확보 |
| 슬 29 τ = ε⁻ᵅ, Ebner α | `taufactor_tortuosity_factor_tomography_tool.md` | 같은 지표계 |
| 슬 37–38 bimodal vs single | `oh2026_bimodal_composite_cathode.md` · `mcgeary1961_bimodal_sphere_packing.md` · `kang2025_toughened_bimodal_nca_lzo.md` | **같은 물리, 다른 도구** |
| 슬 25 "Electrode: composite design, solid electrolyte" | `bielefeld2019_microstructural_modeling_composite_cathode.md` | 스케일 지도상 같은 칸 |

---

## 14. 판독 메타 (재현용)

- 원본: `litdb/inbox/문장혁 교수님.pdf` — 22 pp, **텍스트 레이어 0 byte**, 각 페이지가 1737 px 폭 JPEG를
  **18줄 스트립**으로 분할한 스캔(페이지 유효 raster ≈ 1737 × 2458).
- 통독: 페이지당 슬라이드 2장 crop, **1.15 × native** (슬라이드당 ≈ 1700 × 1230 px).
- 정밀 판독: 문제 영역만 **3× / 4× / 4.5× / 5× / 6× / 8×** 재렌더.
  - 3× — 슬 5 링 차트 수치
  - 4× — 슬 16 neo4j DB 패널(노드·관계·property key), GNN Case 확률
  - 4.5× — 슬 34 Key tools 아이콘, 에이전트별 스킬 수
  - 5× — 슬 21 셀 사양표·도면, 슬 23 Total Duration, 슬 36 mesh 지표
  - 6× — 슬 35 arXiv 번호, 슬 38 막대·랭킹
  - 8× — 슬 34 Analyzer Agent 스킬 표기(숫자 부재 확인)
- **원 raster 한계로 끝내 판독 못 한 것**: 슬 36 mesh face 수, 슬 37 패널별 porosity/τ 숫자,
  슬 35 그래프 x축 라벨, 슬 20 LG 사양 박스 일부(가림).

---

## 15. 🔁 2026-08-03 재판독 대장

### 15a. 교정 16건 (우리 종전 digest가 틀렸고 덱이 맞음)

| # | 위치 | 종전 (우리) | 실제 (덱) | 배율 |
|---|---|---|---|---|
| 1 | 슬 5 | "판독 불가 — 추정 금지" | 논문 520/776/1164/1250/1939/1997, 인용 4159/8165/14037/22707/23443/31644 (2019→2024) | 3× |
| 2 | 슬 4 | `∂φ/∂z = −i/κ` | `∂φ/∂x = −i/κ` | 1.15× |
| 3 | 슬 13 | *Lu et al.*, Energy Reports, 2025 | ***Tuncel et al.***, Energy Reports, 2025 | 1.15× |
| 4 | 슬 16 | 관계 `HAS_UNIT` `USES` `TESTED_IN` | **`MEASURED_AS` `USED_IN` `TESTED_BY`** | 4× |
| 5 | 슬 16 | Case 2 = "Halide A in Li₆PS₅Cl" | **"Halide A in Li₆PS₅A (Cl/Br/I)"** | 4× |
| 6 | 슬 17 | 5,680편 | **5,689편** | 1.15× |
| 7 | 슬 17 | 클러스터 "LATP/LiPON" | **"NASICON (LATP/LAGP)"**, LiPON 없음 | 1.15× |
| 8 | 슬 20·21 | 직경 21.7 mm | **21.2 mm** | 5× |
| 9 | 슬 20 | 툴콜 시퀀스를 "슬 20–21" | **슬 20** (슬 21은 Claude Desktop 스크린샷) | 1.15× |
| 10 | 슬 23 | 8,965.8 s (≈2.5 h) | **8565.8 s (≈2.38 h)** | 5× |
| 11 | 슬 27 | 저항 단위 mΩ/cm² | **mΩ·cm²** | 1.15× |
| 12 | 슬 33 | Toolformer 2023 / BATTERY-SIM-AGENT 2026 / CAMEL-AI | **Toolformer 2022 / BSA 2025 / CAMEL-AI 없음** | 1.15× |
| 13 | 슬 35 | arXiv:2601.04746 | **arXiv:2601.04748** | 6× |
| 14 | 슬 37 | footprint 30 × 38 µm | **30 × 30 µm** | 1.15× |
| 15 | 슬 37·38 | `SPH10` | **`SPH010`** | 1.15× |
| 16 | 슬 38 | 랭킹 HC06 > HC05 > … , "3배" = HC06 vs HC01 | **HC05(56.8) > HC06(53.4) > GRD01(45.4) > SPH010(33.6) > HC01(16.8)**, 3.38× = **HC05 vs HC01** | 6× |

### 15b. 신규 20건

| # | 위치 | 내용 |
|---|---|---|
| 1 | 슬 12 | 슬라이드 전체 누락분 편입 — Conventional Limitations 3 / LLM-based Solution 2, *Chen et al., The Innovation, 2026* |
| 2 | 슬 19 | 슬라이드 전체 누락분 편입 — BatteryBERT QA + SEI 성장 시뮬(파라미터 5종) |
| 3 | 슬 28 | 슬라이드 전체 누락분 편입 — **Physics–ML Pipeline 5단계** (ARTISTIC 계보와 대응) ★★ |
| 4 | 슬 31 | 슬라이드 전체 누락분 편입 — Lumped → Microstructure-resolved 사다리 + 자동화 배너 |
| 5 | 슬 32 | 슬라이드 전체 누락분 편입 — **Chouchane·Meng, ACS Energy Lett. 2024, 9, 4** (FEM+RF surrogate) ★ 정본 미보유 |
| 6 | 슬 16 | **KG 규모 9,596 노드 / 18,145 관계**, 노드 16종·관계 17종 전수 → **Q1 종결** |
| 7 | 슬 16 | property key 실물 15개(알파벳 첫 화면) — 제조·측정 조건 중심 |
| 8 | 슬 16 | **KG-RAG 질의 실물**(stack pressure 5–10 MPa vs >20–100 MPa, "Papers 1,3,7,18,19,30") ★ 우리 스택압 축 |
| 9 | 슬 16 | GNN 확률 Case1 0.57/0.18/0.25 · Case2 0.55/0.15/0.31 |
| 10 | 슬 21 | MCP 호스트 = **Claude Desktop (Sonnet 4.5)** + FreeCAD MCP, 프롬프트 원문 |
| 11 | 슬 21 | 셀 스펙표 전체(mandrel 2 mm · jelly-roll 9.8 mm · 38 turns · 층서열) + **표(21700) vs 도면(4680) 불일치** |
| 12 | 슬 34 | **Key tools = Blender / MATLAB / COMSOL / Python** |
| 13 | 슬 34 | 에이전트별 스킬 수 [3] geometry · [5] simulation · [6] visualization&export · [8] validation, **Analyzer 미표기** (8× 확인) |
| 14 | 슬 34 | Validator 가 **8종 구조 검증 지표** 사용 (항목은 미공개 → Q7) |
| 15 | 슬 36 | graphite **11 STL templates**, NMC811 **2,054 입자 → 6 cluster 대표**(C0–C5 명칭) |
| 16 | 슬 36 | dense→sparse 메시 형상지표 보존 −0.02 / −0.21 / +0.25 / −0.04 % |
| 17 | 슬 37 | n=80 내역 **Single 55 / Binary 19 / Gradient 6**, 구조공간 축 **D_eff = D·ε^β**, 가이드 α=1.9(Ebner)/1.7/1.5(sphere) |
| 18 | 슬 38 | **0.5C −6.4 % / 3C +70.4 %** 두 화살표 = 트레이드오프 명시 |
| 19 | 슬 38 | **SPH010 은 τ_z 최저(≈1.55)인데 3C 4위** → 굴곡도 단독으로 rate 설명 불가 (관찰) |
| 20 | 슬 39 | 메모리 층에 **docs/knowhow (INDEX.md)** 명시, solver 실행 **DIS/EIS/P2D** ★ M5 접점 |

### 15c. 절차 기록

`talks/README.md` 3b 규율(덱을 오류로 적기 전에 원해상도 재판독)을 이번에도 적용했다.
**이번 재판독에서 "덱 오류"로 확정한 건 2건뿐**이다 — 슬 21 표/도면 규격 불일치, 슬 19 BatteryBERT 정답 라벨.
나머지 16건은 전부 **우리 저해상도 전사 오류**였다. 즉 **1차 digest의 수치 오류율이 낮지 않다**
(수치성 항목 기준 대략 1/4). 스캔 덱은 **처음부터 슬라이드 단위 crop + 수치 영역 확대**로 읽어야 한다 —
페이지 통짜 렌더는 제목·구조만 신뢰할 수 있고 **숫자는 신뢰할 수 없다**.

---

## 99. ⏳ 발표 구술 내용 (txt 대기 중)

사용자가 발표 구술 txt를 제공하기로 함 (2026-07-28). 받으면 여기에 정리하고 §11의 Q1b–Q8을 닫는다.

_(비어 있음)_
