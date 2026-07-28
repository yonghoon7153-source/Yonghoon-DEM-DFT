# AI 기반 배터리 연구 자동화: LLM 기반 연구 분석에서 AI-Agent 전극 모델링까지 — 문장혁 (중앙대)

> slug `moon2026_cau_llm_agent_battery_automation` · type `talk` · 발표 2026-08-21 (2026년도 전지기술 심포지엄, 한국전기화학회, 기술세션 3-4) ·
> 발표자 **Janghyuk Moon**, Department of Energy Systems Engineering, Chung-Ang University ·
> 부제 "배터리 지식 분석, 모델 연계 및 전극 시뮬레이션 자동화" · 세션 대주제 "AI 전환기에서의 K-Battery 산업: 기회와 도전" ·
> PDF 22 pp (자료집 pp. 297–318), 슬라이드 39장 · digested 2026-07-28 · status ✅ (덱), ⏳ 구술 txt 대기
>
> ⚠ **덱 인용 규율**: `litdb/talks/README.md`. 이 덱은 **물성 수치가 거의 없고 인프라·워크플로 주장이 본체**다.
> 우리 물성 db 와 섞일 일은 없지만, **"이 방법으로 무엇을 얻었다"는 주장의 검증 가능성**이 낮으니
> (대부분 under review / arXiv) 인용 시 상태를 반드시 병기할 것.

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
| 3–8 | 2–11 | **01 AI for Battery R&D** — 상태추정/진단, 모델 계층, 산업 현황 |
| 8–11 | 12–17 | **02 LLM and Knowledge Intelligence** — RAG, 온톨로지→KG→Graph RAG, 문헌 계량분석 |
| 11–14 | 18–24 | **03 Agentic AI** — MCP 도구 연결, 모델 피팅 에이전트 |
| 15–22 | 25–39 | **04 AI-Agent-Based Electrode Modeling** ★ 본체 — **BEARS** |

---

## 3. 01부 — 배경 (슬 2–11)

### 모델 계층 (슬 4) — 이 덱의 좌표계

```
① Empirical (capacity loss = f(I,T,SOC))
② ECM (R0 + R1‖C1 + OCV)
③ Physics-based (DFN: ∂c/∂t = ∇·(D∇c) + R ,  ∂φ/∂z = −i/κ)
④ Data-driven ML
                    →  fidelity·complexity 증가 방향
```

> 🔑 **우리 위치**: 이 사다리의 **아래쪽 바깥**이다. 우리는 ③이 필요로 하는 **파라미터(σ, Ea, C_ij, ESW)를
> 원자 스케일에서 만드는 층**이고, 이 덱은 ③④를 자동화한다. **경쟁이 아니라 상하류**.
> 우리 open_items **M5(P2D 파라미터 export)** 가 정확히 이 접점이다 — 처음으로 **소비자가 특정됐다**.

### 산업 현황 (슬 8) — 발표에서 가장 구체적인 수치

**SK온 AI 기반 배터리 개발 (AI 연구원 플랫폼)**
| 항목 | 값 |
|---|---|
| 도입 시점 | 2025년 7월 |
| 핵심 기능 | AI 기반 셀 설계·소재 개발, 성능 예측, 원가 산출 |
| 개발 기간 | 기존 대비 **1/3 단축** |
| 원가 산출 속도 | 2시간 → **10초 (700배)** |
| 절감 효과 | 완성차 프로젝트당 수백억 예상 |

**배터리 3사 글로벌 EV 시장 (올해 1월 단월, SNE리서치)**
LG에너지솔루션 4.7 GWh (전년동기 **−14.9 %**, 점유 6.6 %) · SK온 2.3 GWh (**−21.3 %**, 3.2 %) ·
삼성SDI 1.6 GWh (**−24.4 %**, 2.2 %) · **K배터리 3사 합계 8.6 GWh (−17.3 %, 12 %)**

> 🔑 이 두 슬라이드가 발표의 **동기 서사**다: 시장이 역성장하는 국면에서 AI가 개발 속도·원가로
> 활로를 낸다. **우리 원고/발표의 도입부 논리로 그대로 차용 가능**(출처 명시 조건).

### 기타 (슬 2–7, 9–11)
- 배터리 모니터링 AI 3분류: model-based / data-driven / **hybrid** (슬 3)
- 데이터→분석→출력 지도 (슬 6, *Energy and AI* 2020): 입력(시간·전압·전류·온도·전극전위·strain·압력)
  → 분석(EIS·ICA·CV·HPPC·GITT·DVA·DTA·**DRT**·acoustic) → 출력(용량손실·저항증가·SEI저항·전하이동·
  확산저항·활물질손실·**Li 인벤토리 손실**·엔트로피계수)
- 멀티스케일 학습 프레임 (슬 7, *Adv. Funct. Mater.* 36(11), 2025): atomistic→micro→meso→macro,
  **inverse design ↔ forward predicting**
- 전해질 분자 설계 (슬 9): **Ask → Search → Formulate → Design → Predict** (SES 플랫폼)
- 셀 설계 대시보드 (슬 10): STEER (SLAC/Stanford)
- **디지털 트윈**·스마트 제조 (슬 11): BESS self-qualification, HIL 시험
  > ⚠ 지도교수 피드백(2026-07)에 따라 **우리 자료에서는 "디지털 트윈" 대신 "AI 계산"을 쓰기로 결정**했다.
  > 이 덱은 그 용어를 쓴다 — 우리가 안 쓰는 것은 방침이지 그들이 틀려서가 아님을 기록해 둔다.

---

## 4. 02부 — 지식 인텔리전스 ★ (슬 12–17)

### 4a. 온톨로지 → 지식그래프 → Graph RAG (슬 14)

```
온톨로지(개념·관계·속성 정의) → 실데이터 매핑 → KG DB(neo4j)
   → LLM 이 Node-Edge 추출 → Embedding → Retrieval → Top-k → GPT-5.1 API → Response
```
**Graph RAG 의 이점 3가지 (덱 주장)**
1. **Structured Retrieval** — 고립된 텍스트 청크가 아니라 **그래프로 연결된 근거**를 검색
2. **Multi-hop Reasoning** — 엔티티·관계·경로를 이어 **숨은 링크 추론**
3. **Traceable Answers** — 근거 경로를 보여줘 응답이 투명·신뢰 가능

### 4b. 고장 추론 KG (슬 15)
노드 종류: 배터리 소재 · 고장 유형 · 고장 기구 · 운전 조건 · 고장 원인 · 안전 조치 ·
제조사/위치 · abuse 영향. 질의 "Which fault caused 'Signal abnormal A'?" → Cypher 변환 → 그래프 검색.

### 4c. **ASSB 문헌 KG + GNN 링크 예측** ★★ (슬 16) — 우리와 가장 관련

황화물계 ASSB 문헌에서 **소재–공정–계면–성능–열화** 관계를 추출해 KG 구축.
**Graph RAG는 근거 문헌 검색을, GNN은 아직 연결되지 않은 잠재 관계의 예측을 담당.**

관계 타입(덱에 나열): `AFFECTS` `CONCLUDES` `DERIVED_FROM` `EXPLAINED_BY` `FOR_SAMPLE`
`HAS_COMPONENT` `HAS_CURVE` `HAS_PROCESSING` `HAS_UNIT` `PRODUCES` `REALIZED_BY` `REPORTS`
`SHOWN_IN` `SUPPORTS` `TESTED_IN` `UNDER_CONDITION` `USES`

**GNN 예측 사례 2건:**

| | Case 1 — *Unseen but Correct* | Case 2 — *Literature-Consistent* |
|---|---|---|
| Factor | **Soft-acid cation doping (HSAB: Sn/Sb/As) in sulfide SE** | **Halide A in Li₆PS₅Cl electrolyte** |
| Issue | Low ionic conductivity | Low ionic conductivity |
| 예측 | **RESOLVES** | **RESOLVES** |
| 성격 | KG에 직접 연결이 **없던** 링크를 맞힘 | 문헌과 일치 |

> 🔑🔑 **Case 1이 우리 cascade의 `air_hsab` 축과 같은 명제다.** 우리는 HSAB soft-acid 도핑을
> 물리 기술자로 계산해서 순위를 매기고, 그들은 문헌 그래프에서 링크를 예측해 같은 결론에 도달했다.
> **완전히 다른 두 경로가 같은 답을 냈다 = 수렴 검증(convergent validation)**.
> 우리 원고에서 인용 가치가 크다. 단 **"우리 계산이 그들 예측을 검증했다"고 쓰지 말 것** —
> 시점·인과 주장 불가, "독립 경로의 일치"까지만.
>
> ⚠ 또한 `Sn` 은 **이상욱 랩의 가수분해 억제 도펀트**(LPSnSCl)와 같은 원소다. 세 갈래
> (문헌KG 예측 / 반응MD 기구 / 우리 스크리닝)가 **Sn 에서 만난다**.

### 4d. LLM/RAG 문헌 계량분석 (슬 17) ★ — 방법론적으로 우리 것과 같은 종류

**Li-air 사례**: Clarivate Web of Science "Li-air battery" **5,680편 → 4,183편** → 토픽 검색 →
논문 선별 → 마이닝 → **피인용 상위 1,000편** → PDF 다운로드 → 에너지밀도·질량기준 추출(GPT-5.1) → 데이터 추출

**발견**:
> "**전셀 질량 기준** 에너지밀도는 대체로 **500 Wh/kg 미만**이다. 더 높은 값들은 활물질·탄소·전극
> 질량 같은 **가벼운 질량 기준으로 계산된 것**이라 현실적인 전셀 성능을 반영하지 않을 수 있다.
> **500 Wh/kg 을 넘는다고 보고한 3편은 주로 전해질 무게를 줄여** 그것을 달성했다."

> 🔑 이것은 **문헌의 보고 관행이 수치를 부풀린다는 메타분석**이고, **우리 깔때기의 정직성 장치와
> 정확히 같은 종류의 작업**이다(vacuous gate 표시, 절대 문턱 이식 시 empty gate 기록, 91→47은
> 물리 게이트가 아님 명시…). **이런 메타분석이 학회 발표 본론에 들어간다는 전례** — 우리 정직성
> 장치도 부록이 아니라 본론으로 낼 수 있다는 근거.

**ASSB 사례**: 임베딩·클러스터링으로 전해질 계열 지도(sulfide, LPSCl, LGPS, halide, garnet,
perovskite, polymer, LATP/LiPON, NASICON…) + **T·P 변화에 따른 σ 예측면**

### 4e. SOH 예측용 LLM 워크플로 (슬 13)
LLM이 **파이프라인 전체를 설계·조율**(전처리·feature selection·모델 선택·코드 생성·HP 튜닝·평가)하되
**예측 자체는 RF/XGBoost/CatBoost**. 8단계 structured prompt 예시. *Lu et al., Energy Reports, 2025*
> 🔑 "LLM은 오케스트레이터, 예측은 고전 ML" — **우리 codoping_ml.py 의 ridge/LOOCV 구조와 같은 철학**.

---

## 5. 03부 — Agentic AI (슬 18–24)

- **정의 (슬 18)**: 문제 해결 절차를 계획하고 외부 도구·모델과 상호작용해 작업을 수행하는 목표 지향 AI.
  Orchestrator LLM(Google ADK) + Memory + Tools + Planning + Feedback, 다중 에이전트 프로토콜
  (Discover agent capabilities → Share tasks → Update task information)
- **MCP (슬 20–21)**: LLM이 로컬 데이터·파일·API·CAD·시뮬레이션 도구를 표준 방식으로 호출.
  실증 예: **FreeCAD로 LG 21700 M50 셀 3D 모델 생성** — 직경 21.7 mm × 길이 70.2 mm, 맨드릴 2 mm,
  단위셀 38개, 층 순서 Al(15 µm)→NCM(75 µm)→separator(20 µm)→graphite(85 µm)→Cu(10 µm).
  `create_document` → `create_object` → `get_view` 툴콜 시퀀스를 그대로 보여줌.
- **LLM-Orchestrated Physics-Based Simulation (슬 22)**: 자연어 → 설계조건 추출 → CAD 생성 →
  해석모델 설정 → 실행 → 결과 분석 (온도·전류밀도·전위·Li⁺ 농도장)
- **Battery-Sim-Agent (슬 23)** ★ — *ICLR 2026, under review*

```
Perception(전문지식·탐색지식·동적기억) → Scenario(첫 사이클 캘리브레이션 / 장기 열화)
  → Structured Info(사이클 프로토콜·모델링 프레임·현재 파라미터)
  → Reasoning(피드백 분석 → physics-informed 가설 → 기구 인지 업데이트 제안)
  → [Battery Simulator 와 루프] → Multi-modal feedback(곡선·용량·스텝별 손실·열화)
  → Target Battery 와 비교
```
| 지표 | 값 |
|---|---|
| Total Duration | **8,965.8 s** (≈ 2.5 h) |
| Final RMSE | **0.5513** |
| Final MAPE | **2.4258** |
| 라운드 | ~70 |

손실 수렴 곡선이 **계단형**(best_Q_mape / best_I_mape / best_V_mape / best_total_mape)
— 에이전트가 가설을 바꿀 때마다 뚝 떨어지는 형태.

> 🔑 **"에이전트가 물리 모델 파라미터를 스스로 피팅한다"의 정량 증거**. 우리가 서버 작업을 붙여넣기
> 루프로 도는 것과 대비된다. 다만 under review 이고 단일 케이스다.

---

## 6. 04부 — BEARS ★★ 본체 (슬 25–39)

### 6a. 문제 — 전극 설계의 병목 (슬 27, 30)
- 수작업 모델링: 수동 분석 · 셋업 오류 · **소프트웨어 파편화** · 느린 반복 검토
- **Top-down 재구성(FIB-SEM/XCT): 스캔 1회당 $5,000 이상, 수 주 소요**
- Bottom-up 생성: 빠르지만 모델링 전문성과 검증 필요
- 설계 A/B/C 비교 예시: 에너지밀도 280/**305**/270 Wh/kg · 사이클수명 820/**950**/760 ·
  저항 1.2/**0.9**/1.4 mΩ/cm² · 기공률 35/38/32 %

### 6b. 미세구조가 필요한 이유 (슬 29)
**τ = ε^(−α)** (Bruggeman). **NMC α = 0.5 vs Graphite α = 1.9** — 같은 관계식인데 지수가 4배 다르다.
입력 변수: 기공률·굴곡도·입자 형상·형태·구형도·연결성.

### 6c. 계보 (슬 33) — 이 분야의 시간축
```
1990s 다공성 전극 모델(Doyle–Fuller–Newman 1993)
 → 2009–2012 미세구조 특성화 → 2013–2016 이미지 기반 모델링
 → 2015–2020 확률적 재구성 & ML → 2020–2025 생성형 AI 미세구조 생성
 → 2023–2026 도구 사용 LLM 에이전트 → **BEARS**
```
LLM 계보 병기: 2017 Transformer → 2018 BERT → 2020 GPT-3 → 2020 RAG → 2022 ReAct →
2023 HuggingGPT / Toolformer / AutoGen·LangChain·CAMEL-AI → 2025 ChatBattery →
2026 BATTERY-SIM-AGENT → BEARS

### 6d. BEARS 구조 (슬 34, 39)

**닫힌 루프 8단계**: `1 파라미터 식별 → 2 Geometry → 3 Materials → 4 Physics → 5 Meshing →
6 Simulation/Solver → 7 Validation → 8 Analysis` (+ 역방향 Debugging, 최적화 루프)

**전문 에이전트 5 + 총괄 1**
| 에이전트 | 역할 |
|---|---|
| **Analyzer** | SEM 이미지 분석 & 3D 재구성 |
| **Generator** | 전극 구조 생성 |
| **Fabricator** | 3D 시각화 & export |
| **Validator** | 구조 분석 & 검증 |
| **Simulator** | FEM 전기화학 해석 |
| Main | 총괄 |

**Planner/Orchestrator**: Decompose → Plan → Execute → Monitor → Iterate
**입력**: 연구 의도(가설·목표, 레시피·조건, 목표 성능) + 지식원(논문, 소재 DB·파라미터,
**이전 실행 결과**, **실패 사례·노트**) + 구조 기술자(SEM 형태, PSD·기공률·로딩, 조성, 두께·굴곡도)
**출력**: 입자 / 전극 / 검증 / 시뮬레이션 / **다음 실행 추천**
**4 기둥**: Reproducible workflow · Expert knowledge reuse · **Failure-aware debugging** · Scalable automation
**메모리**: BEARS Knowledge Bank + **GitHub issues & comments**

### 6e. **Modular Skills 3계층** ★★ (슬 35) — 우리가 가장 직접 가져올 수 있는 것

> "Skills는 Agent에 내장된 **경량 instruction module**로, 복잡한 추론이나 코드 생성 없이 특정
> 작업을 효율적으로 수행하여 **낮은 토큰 사용량과 신뢰도 높은 출력**을 보장"

**40+ Modular Skills**, 8 범주: Image analysis / Geometry / Visualization & export / Mesh processing /
Validation / Simulation / Debugging & Analysis / Utility

**3-Level hierarchy** ★
| Level | 내용 | 로딩 |
|---|---|---|
| **1** | Metadata (YAML) | **항상 로드**, ~100 토큰 |
| **2** | Body (Markdown) | **스킬이 트리거될 때만**, < 5k |
| **3** | Bundled files (scripts, data) | **에이전트가 필요할 때만** |

동반 그래프: **Stage 1 High Efficiency Zone → Stage 2 Cognitive Overload (Flat)** —
컨텍스트를 늘리다 보면 정확도가 평탄해지는 구간이 온다. arXiv:2601.04746(판독 주의)

> 🔑🔑 **우리 repo가 정확히 Level 2 만 있는 상태다.** `CLAUDE.md`(항상 로드, 근데 100 토큰이 아님) +
> `tools/*.py`(Level 3) 는 있지만 **Level 1 메타데이터 층이 없어** 매번 전체를 읽어야 한다.
> 이게 우리 세션이 컨텍스트를 태우는 구조적 이유고, **T7 로 실행 항목화**한다.

### 6f. 실증 결과 (슬 36–38)

**슬 36 — 단일 SEM 이미지 → 3D 입자 라이브러리** (Analyzer Agent)
U-Net + **SAM 2**(ViT-H image encoder + prompt encoder + mask decoder) 분할 →
**Multi-view Diffusion → LRM(Large Reconstruction Model)** → FEM-ready mesh(dense/sparse) →
클러스터링 → 재사용 가능한 particle library. 그래파이트(이미지→3D), NMC811(FIB-SEM 재구성) 예시.

**슬 37 — 전극 생성·검증**
DOE 기반, 고정 조건: 그래파이트, footprint **30 × 38 µm**, 로딩 **8 mg/cm²**, wt% **95:3:2**.
가변 노브: 입자 템플릿 · PSD/DSD · 아키텍처(single/binary/gradient).
**가상 전극 80개(n=80) 생성 → 대표 5개 검증**: SPH10(구) · HC01(single) · HC06(binary) ·
HC05(binary) · GRD01(gradient). Through-plane 굴곡도 vs 기공률 플롯.

**슬 38 — 고율 방전 성능** ★ 정량 결론
C-rate sweep 0.5C / 1C / 2C / 3C.
> **3C 에서 binary 구조가 막히지 않은 전해질 경로 덕에 single 구조 대비 약 3배 높은 용량 유지**

3C 방전용량 순위: **HC06 > HC05 > GRD01 > SPH10 > HC01**.
SOC 분포도 + 전해질 전류밀도 벡터장으로 기구 시각화.

> 🔑 이 결과 자체가 **우리 DEM 트랙(bimodal AM 시스템)과 같은 물리**다 — bimodal 입도가 수송
> 경로를 여는가. 우리는 DEM(접촉·응력·percolation)으로, 그들은 FEM+전기화학으로 본다.
> **상보적이고, 우리 DEM 결과를 그들 언어로 번역할 수 있다.**

---

## 7. 우리 대비 — 축별 판정 ★★

| 축 | 그들 (BEARS) | 우리 (이 repo) | 판정 |
|---|---|---|---|
| **문제 층위** | 전극 미세구조 ~ 셀 (µm–mm) | 원자·결정 (Å–nm) | **직교 — 상하류**. 우리 M5(P2D export)가 접점 |
| **지식층 구조** | neo4j KG + Graph RAG + **GNN 링크예측** | litdb 118 MD + INDEX.md + comparison_vs_ours.md (평면) | **그들 우위(구조)·우리 우위(정합)**. §8 참조 |
| **스킬/컨텍스트 관리** | 40+ 스킬 **3계층 로딩** | CLAUDE.md + tools/ (Level 1 없음) | **완패 — 즉시 채택 대상** |
| **실패 처리** | Failure-aware debugging, GitHub issues 를 메모리로 | kb/open_items.md + 탈락 명단 + vacuous 표시 | **호각**. 우리 쪽이 "실패의 종류"를 더 세분 |
| **재현성** | Reproducible workflow 주장 | git 버전 db + 빌더 스크립트 **2회 실행 md5 동일** 강제 | **우리 우위 (검증 방식이 구체적)** |
| **닫힌 루프 자동화** | 8단계 완전 자동 + 다음 실행 추천 | 붙여넣기 루프(사용자 경유) | **완패** — 단 우리는 원격 서버 다수·자원 게이트 문제 |
| **정직성 장치** | 슬 17 Li-air 메타분석(질량기준 부풀림) 1건 | 깔때기 vacuous·순서민감도·컷 지배 경고·empty gate 기록 | **우리 우위 (체계화 수준)** |
| **검증 상태** | 다수 under review / arXiv | db 값은 재현 스크립트 동반 | 인용 시 상태 병기 필요 |
| **미세구조–성능** | 80 전극 · 3C binary 3배 | DEM 트랙(접촉·응력·percolation) | **같은 물리, 다른 도구 — 상보** |

---

## 8. 지식층 정면 비교 — 우리가 이기는 지점 ★

그들 KG의 강점은 **구조(멀티홉·링크예측)**, 우리 litdb의 강점은 **정합(alignment)** 이다.

| | 그들 KG/Graph RAG | 우리 litdb |
|---|---|---|
| 추출 | LLM이 PDF에서 노드·엣지 자동 추출 | 사람+에이전트가 digest를 **논문 수준으로 재서술** |
| 방법 맥락 | 관계 타입엔 있으나 **"이 수치가 어떤 방법에서 나왔는가"가 노드 속성으로 얼마나 남는지 불명** | digest §DFT/계산 방법에 functional·k·supercell·무질서 처리까지 명시 |
| 우리 값과의 대조 | 없음(문헌 내부 그래프) | **`comparison_vs_ours.md` + 각 digest §우리 대비** = 수작업 정합층 |
| 인용 금지 규칙 | 없음 | **"소환값 — 우리 db 절대값과 섞지 말 것"**, 특정 수치 인용 금지 지시가 digest 안에 박혀 있음 |
| 오류 정정 이력 | 불명 | 오귀속 철회 사례가 **17개 파일 횡단으로 기록**(Schlem·Deng) |

> **결론**: 우리가 KG로 가야 할 이유는 "검색이 안 돼서"가 아니라 **"멀티홉 가설 생성이 없어서"**다.
> 반대로 **KG로 가면서 잃으면 안 되는 것은 방법 맥락과 인용 금지 규칙**이다.
> → T6(litdb 그래프층)은 **digest를 대체하는 게 아니라 digest 위에 얹는 것**으로 설계한다.

---

## 9. 우리가 가져올 것

`kb/projects/symposium_2026_competitive_analysis.md` 의 **T5–T8**.

1. **3계층 스킬 로딩** (슬 35) — Level 1 메타데이터(YAML ~100토큰) 층 신설. 비용 대비 효과 최대.
2. **litdb 그래프층 + 링크 예측** (슬 16) — digest 위에 얹는 방식. Case 1(HSAB Sn/Sb/As)이
   우리 cascade와 수렴한 것을 **원고 인용 소재**로 확보.
3. **실패 사례를 1급 입력으로** (슬 39) — 우리 `kb/open_items.md`·탈락 명단을 "다음 실행 추천"의
   입력으로 쓰는 구조. 이미 절반은 있다.
4. **P2D/FEM 파라미터 export (M5)** — 소비자가 특정됐다. 우리 σ/Ea/C_ij가 그들 ③층 입력.
5. **DEM 결과의 전기화학 번역** — 우리 bimodal DEM ↔ 그들 3C binary 3배. 같은 명제의 두 증거.
6. **도입부 서사** (슬 8) — K배터리 −17.3 % / SK온 원가산출 700배. 출처 명시 후 차용.

---

## 10. 주의 / 한계

1. **검증 상태**: BEARS(arXiv), Battery-Sim-Agent(**ICLR 2026 under review**), 슬 33의 다수 항목이
   arXiv. **peer-review 통과 결과로 인용 금지**.
2. **슬 37–38의 n**: 80개 생성 중 **5개만** 전기화학 검증. "80개를 시뮬레이션했다"고 쓰면 오독.
   "3C에서 3배"는 **HC06(binary) vs HC01(single)** 두 구조의 비교다.
3. **슬 35 "40+ Skills"** 는 개수 주장이고, 각 스킬의 신뢰도 근거는 덱에 없다.
   "낮은 토큰·높은 신뢰"는 주장이지 측정치가 아니다.
4. **슬 16 KG 규모 수치**(노드/관계 수)는 저해상도로 판독 불가 — **추정 금지**.
5. **슬 5 논문·인용 수**도 판독 신뢰도 낮음. 인용하려면 원 출처 확인.
6. **디지털 트윈 용어** — 그들은 쓰고 우리는 안 쓴다(지도교수 방침). 비교 서술 시 우리 방침을
   그들 비판처럼 쓰지 말 것.
7. **슬 8 시장 수치**는 SNE리서치 단월(1월) 기준이다. 연간으로 오독 금지.

---

## 11. 미해결 질문 (구술 txt / 논문으로 닫을 것)

| # | 질문 | 닫는 방법 |
|---|---|---|
| Q1 | ASSB KG의 **노드/관계 실제 규모**와 소스 논문 수 | 구술 / 논문 |
| Q2 | GNN 링크예측의 **평가 프로토콜**(negative sampling, 시간분할 여부) — Case 1이 진짜 "unseen"인지 | 논문 |
| Q3 | BEARS 3계층 스킬의 **토큰 절감 실측치** | arXiv 2601.04746 |
| Q4 | Battery-Sim-Agent 의 **베이스라인**(수동 피팅 대비 RMSE) | ICLR 제출본 |
| Q5 | 80 전극 중 5개 선정 기준 | 구술 |
| Q6 | 우리 σ/Ea 를 그들 P2D에 넣으려면 **어떤 형식**이 필요한가 | 구술 — **협업 제안 각도** |

> Q6은 질문이자 **협업 제안 포인트**다. 우리는 파라미터를 만들고 그들은 소비한다.

---

## 12. 인용 가능 문장

- "FIB-SEM/XCT 기반 전극 재구성은 스캔 1회에 $5,000 이상과 수 주가 든다 — 그래서 가상 생성이 필요하다" (슬 30)
- "같은 Bruggeman 관계식이어도 NMC α = 0.5, 그래파이트 α = 1.9 로 굴곡도–기공률 지수가 4배 다르다" (슬 29)
- "LLM은 파이프라인을 조율하고 예측 자체는 고전 ML(RF/XGBoost)이 맡는 분업이 실무 표준으로 자리잡고 있다" (슬 13)
- "문헌의 에너지밀도 보고는 질량 기준이 통일돼 있지 않아, 전셀 기준으로 환산하면 대부분 500 Wh/kg 미만이다" (슬 17, Li-air)

---

## 99. ⏳ 발표 구술 내용 (txt 대기 중)

사용자가 발표 구술 txt를 제공하기로 함 (2026-07-28). 받으면 여기에 정리하고 §11의 Q1–Q6를 닫는다.

_(비어 있음)_
