# 위키 색인

> 내용 목록. 모든 위키 페이지를 종류별로 한 줄 요약과 함께 싣는다.
> 마지막 갱신: 2026-09-16 | 전체 페이지: 35

## Entities (satellite 프로젝트)

- [[degradation-degeneracy]] — 22p LLI/LAM 분해가 물리인지 degeneracy 인지 판별하는 PyBaMM 합성 truth 프로젝트 (첫 satellite, 13차 게이트 리뷰 대기).
- [[mode-observability]] — "관측을 늘리면 갈리는가": PVS·SEV Jacobian 식별 가능성 + ML 라벨 degeneracy 전파 (둘째 satellite, 2026-09-03 개설).

## Concepts (개념)

- [[fitting-degeneracy]] — full-cell 곡선 하나로 LLI/LAM_PE/LAM_NE 를 가를 수 있는가: flat valley(데이터 한계) vs multimodal(최적화 난이도) 구분.
- [[provenance-fail-closed-verification]] — 13 라운드 게이트 리뷰에서 증류된 재현성 설계 원칙 7가지 (서명·재계산 렌더·봉인 읽기·fail-closed·신뢰 경계).
- [[near-optimal-set-width-measurement]] — 근최적 집합 위에서 유도량이 훑는 범위를 직접 미는 법: 등방 표집이 참 폭 40 %p 를 0.00 %p 로 보고한 반례, Hessian 의 같은 국소성 한계, 제약 최적화 + 등식 프로파일의 합집합과 그 한계 넷 (하한 · tol 은 통계가 아님 · 비용 · provenance).
- [[agent-harness-patterns]] — ponytail·caveman·superpowers 에서 무엇을 채택·각색·기각했는가와 그 근거 (결과: 루트 CLAUDE.md + 커맨드 4종).
- [[llm-wiki-pattern]] — Karpathy 식 LLM wiki: raw 불변층 + frontmatter progressive disclosure + wikilink 그래프 + mothership/satellite (이 위키의 근거 패턴).
- [[pvs-sev-degradation-mode-features]] — ICA 할선 기울기(PVS)와 스케일링 EOC 전압강하(SEV): 정의·물리 귀속·모드별 부호 구조, 그리고 두 부호 패턴이 같다는 관측.
- [[birkl-ocv-degradation-diagnostic]] — 우리가 판정 대상으로 삼는 OCV fitting 절차의 원전(2017): 자유 파라미터 3개 + 컷오프 등식 소거, 그리고 저자들이 스스로 진술한 li/de 축퇴.
- [[dubarry-mechanistic-mode-synthesis]] — 정방향 모드 합성(2012): α·β 창 좌표계 `(LR, OFS)` 와 li/de 4분류의 진짜 출처, 그리고 식 (8') 안에 이미 들어 있던 축퇴.
- [[interpretable-ml-battery-prognosis-taxonomy]] — interpretable ML 4분류(white box·PIML·physics-inspired feature·post-hoc), PVS·SEV 가 앉는 자리, 그리고 그 분류에 identifiability·uncertainty 어휘가 0회라는 전수 확인.
- [[zhang2020-eis-aging-dataset]] — Phase 2 가 쓰는 EIS 데이터의 정체 (2026-09-03 원전 대조로 verified): Eunicell LR2032 코인셀 12개 · 1C CC-CV / 2C CC · `state I~IX` 아홉 정의와 그중 넷이 DC 전류 중이라는 사실 · 모드 라벨 부재 확정 · ARD 가 고른 "두 주파수" 의 비식별성.
- [[fused-lasso-feature-design-framework]] — Rhyu 2025 의 자동 feature 설계 7단계: 물리는 후보를 지우고 사후 설명만 하며 feature 형태는 선형대수가 만든다, 그리고 이 계보에서 가장 엄격한 검증 설계(agnostic 기준선 + 프로토콜 group CV).
- [[thermo-kinetic-loss-partition]] — 전류를 축으로 쓰는 ΔE/η 분해 (Tao 2025): LLI·LAM_PE·LAM_NE 가 **전부 ΔE 한 칸 안**에 들어간다는 경계 확정, 그리고 "관측을 늘리면 갈리는가" 의 네 번째 후보(다전류 관측).
- [[np-lip-ocv-reparametrization]] — Lin & Khoo 2024 의 `(N/P, Li/P)` 최소 매개화와 **2 자유도 정리**: SOC 정규화 full-cell OCV 형상은 `(1−LLI):(1−LAM_NE):(1−LAM_PE)` 의 **비(比)** 에만 의존한다 → `LLI = LAM_PE = LAM_NE = x` 는 곡선을 전혀 바꾸지 않는 **닫힌 형태 null 방향**. 전극 DV fraction `λ±` 과 네 regime 도 여기.
- [[nullspace-coefficient-interpretation]] — Schaeffer 2024 의 nullspace 관점: `X(β+w)=Xβ` 이므로 **데이터는 계수를 부분공간 하나만큼 결정하지 못하고 그 안의 점은 정칙화가 고른다**. RR·PCR·PLS 는 그 성분을 0 으로 두고 lasso 계열은 아니다. "계수가 작다 ⇒ 중요하지 않다" 의 그림판 반증, 그리고 **우리 축퇴 방향을 그리는 기계**(식 19 `γ`-완화 사영 + 직교 성분 대조) — 파일·함수 이름까지.
- [[piml-physics-injection-points]] — 물리가 ML 파이프라인에 들어가는 **여섯** 자리: 표준 4분류(손실항·입력 feature·구조·사후해석)에 **학습 데이터**와 **라벨 그 자체**를 더한다. Navidi 2024 의 ablation 이 준 첫 실측 순위 **① 손실항 ≫ ⑤ 학습 데이터**, 그리고 여섯째 자리(정답이 물리 모형의 적합값)가 **방법 비교로는 원리적으로 검출되지 않는다**는 사각지대.
- [[constrained-crb-identifiability]] — 등식 제약이 걸린 상태의 Fisher/CRB (Stoica–Ng nullspace 사영, Mohtat 2019 식 28–34): 판정이 **이분법(𝒪ᵀ𝓘_f𝒪 특이 여부) + 정도(sqrt diag Σ)** 두 층이라는 것, 이 계보가 `Σ` 를 구해 놓고 **대각선만 보고하는 공통 습관**, 그리고 **제약 추가(모르는 방향을 줄임) ≠ 관측 추가(정보를 늘림)** 의 구분과 관측 추가가 이득이 되는 기계적 조건(새 감도 열 ≠ 0).
- [[data-window-identifiability]] — 관측 창 `DW = [Q_s, Q_e]`(DOD 구간)이 식별 가능성을 정하는 **세 번째 조작**(제약 추가·관측 추가와 구분: 감도행렬의 **행을 갈아 끼운다**). Lee 2020 의 창 전수 삼각지도와 처방 `DOD = [0.35, 0.73]`, 같은 폭 40 %라도 위치가 **어느 전극이 보이는지**를 고른다는 실측, 그리고 "넓을수록 좋다" 가 깨지는 자리(`y₁₀₀`: shallow 14.2 % < medium 25.1 %).
- [[halfcell-ocp-shape-invariance]] — 모든 electrode balancing 진단이 깔고 있는 **아핀 재조정 전제**(열화 전극 OCP = pristine 곡선의 α·β 변환)와 그 파괴: Si/graphite blend 에서 `γ_Si` 가 9.52 → 5.55 % 로 움직이면 **곡선 모양 자체가 바뀌고**, `γ_Si ↓` 는 `α_an ↓` 와 full-cell 에 **같은 서명**을 남긴다. 강제 시 편향은 방향이 정해져 있다 (LAM_an +2.4 pp 과대 · LAM_cat −3 pp · LLI −1.1 pp) — 그런데 OCV RMSE 는 9.9 → 8.2 mV 로 거의 안 변한다.
- [[reference-electrode-halfcell-dma]] — 기준전극을 셀에 심어 **최적화 없이** 전극별 열화를 재는 DMA (Natterer 2026): LAM 은 한 전극 **안** 두 DVA feature 사이 거리로, LLI 는 스케일한 pristine OCP 대비 **가로 이동량**으로. 축퇴가 풀리는 것이 아니라 **불확실성이 최적화 지형에서 특징점 판독으로 이동**하며, 그 대가 6개(feature 불변·0.2 C≈OCP·pristine OCP 재사용·판독 절차 미인쇄·RE 위치 20 mV·셀 1개)가 여기 정리돼 있다.
- [[rate-independent-li-plating-signature]] — 무율(rate-independent) 리튬 도금 (Wang (Xiong) 2025, LFP/graphite 17 셀 중 10 셀): 원인은 `Q_NE < Q_Li` (LAM_NE), 0.05 C 에서도 생기며 충전 말단 평탄역(≈3.46 V)·방전 시작 짝 평탄역·dV/dQ **새** 봉우리·≈2 mV 동역학 하강을 남긴다. 가역분은 **LLI/LAM 어느 칸에도 안 들어가고**, 아핀 창 매개화가 깨지자 원전은 자유도를 4 → 8 로 늘리고 유일성을 안 쟀다. 음극 0 V 교차점이 창 밖(1.08)에서 안(0.88)으로 들어올 때 `Q_NE` 가 계단으로 떨어지는 국면 전환, `bms-balancing/` 요구서용 구분 시험 T1–T5.
- [[ic-peak-area-direct-mode-readout-lfp]] — Cui 2026 의 적합 없는 직접 진단 (LFP/graphite 20 Ah): **Peak C 절대 면적 감소(Ah) = LLI**, Peak B 상대 감소 = LAM_NE — LFP 평탄 양극 덕에 full-cell dQ/dV 봉우리가 음극 stage 용량 그대로라서 성립하는 항등식. 이 계보 첫 **재료 라벨**(코인셀·XRD, OCV 적합 대비 1.35 / 1.68 %)과 그 대가(오차 막대 0·교차 셀 보간), IC 법의 정답 축은 적합값(1.79 / 1.62 %), 평탄 양극이 만드는 `(X1, X3)` = LAM_PE ↔ LLI 축퇴를 재료 측정이 대신 푼 구조, 사전믿음 등식으로 닫은 li/de 분할(0.36 = 순환 구간 중점), NMC·Si/Gr·무릎 이후로의 이식 조건.
- [[composite-cathode-percolation-utilization]] — **`assb` 축 첫 개념** (Bielefeld 2019): 복합양극 이용률 `θ = V_c/V_ν` — 퍼콜레이팅 전도 클러스터에 속한 활물질 부피 분율. 접촉 손실이 `LAM_PE` 와 섞이는 방식이 **곱셈**(`Q_apparent = θ_AM · Q_material`)이라는 것, 두 종류 부피분율(`g^V` 전체 부피 vs `g^S` 고상 기준)과 닫힌 형태 `p_c = [7.83 ln(d/µm) + 36.67] vol%`, 그리고 **라벨 자체가 폭을 갖는다**는 실측(거시 파라미터 고정에도 무작위 충전 배열만으로 `θ_AM` 이 ≈30 % ↔ ≈70 % 이봉; 임계 바로 위 `A_spec` 표준편차 ±32 %) — DEM 독립 라벨 계획에 붙는 제약. **2026-09-16 갱신(2호 Clausnitzer 2023)**: `θ` 와 `Connectivity = 1 − n_iso/n_tot` 가 **같은 양**임을 확인하고 두 논문의 좌표 변환표(`ρ_S = 1 − φ`, `1 m²/m³ = 10⁻² 1/cm`)를 추가, 곱셈만으로는 **불충분**하다는 반례와 산포 규율이 후속 논문에서 지켜지지 않았다는 기록.
- [[assb-apparent-capacity-decomposition]] — **`assb` 축 둘째 개념** (Clausnitzer 2023): 겉보기 용량의 3항 분해 `Q_apparent = θ_AM · η(i) · Q_material`. 1호의 곱셈 축퇴가 **충분하지 않다**는 논문 내부 반례(CAM 연결성 ≈100 % 인데 정규화 용량 ≈0.10), 이 계보 최초의 전압축 숫자(재료·기하 동일·입계 저항만 0→3.6 Ω cm² → 방전 용량 1.37→0.385 mAh/cm², 겉보기 `LAM_PE` 72 %), 그 곡선이 **아핀 스케일링이 아니라는 것**(시작 전압 −175 mV), 그리고 셋을 가르는 시험 — **율(rate)이 동역학 성분만 지운다**(`i→0` 에서 `η→1`, 기하·재료는 남는다). `θ` 가 스칼라가 아니라 `z` 의 함수라는 것도 여기.
- [[dv-peak-heterogeneity-descriptor]] — Kim 2023 의 DV `Peak_S2`: 진폭이 아니라 **ridge 절대 높이**이며(진폭은 valley 노이즈로 폐기), LFP‖Gr 에서의 음극 단일 귀속은 PVS 해석과 충돌하지 않는다 — 좌표를 맞추면 오히려 일치.

## Comparisons (비교)

- [[halfcell-window-parametrization-lineage]] — 같은 4개 창 좌표를 무엇으로 매개화하고 여분을 어떻게 죽이는가: Dubarry 2·Marongiu 5(제약 0)·Birkl 3(등식 2)·Lin 2·Navidi/우리 4(제약 0). 여분 처리는 **등식 / 0-고정 / 애초에 안 만들기** 셋뿐이며, Marongiu 식 (2)–(5) 의 null 2차원을 닫힌 형태로 풀어 **Birkl 의 3-파라미터 좌표가 그 몫공간임**을 확인.

## Guides (절차)

- [[gate-review-loop]] — 비싼 본 실행 전 외부 리뷰어와 도는 적대적 게이트 루프: 수정 → 검증 → push → 대상 커밋 명시 요청문 → GO 후에만 실행.
- [[new-project-kickoff]] — 새 프로젝트 킥오프 프롬프트: 폴더 세팅 + satellite 등록 표준 절차 (repo-root 상대 경로 `wiki` 적응판).
- [[paper-ingest-mode]] — 논문 수치·정의를 verbatim atom 으로 분해하는 opt-in ingest 모드 (사용자 승인 필수).

## Questions (열린 질문)

- [[22p-physics-or-degeneracy]] — 핵심 연구 질문 카드 (status: active): 22p 분해는 물리인가 flat-valley 결합의 산물인가.
- [[pvs-sev-lli-lampe-separability]] — 질문 카드 (status: open): PVS·SEV 두 feature 가 LLI 와 LAM_PE 를 실제로 가르는가, 아니면 같은 대비 하나를 재는가.
- [[assb-contact-loss-vs-lampe]] — 질문 카드 (status: open) · **`assb` 섹션의 닻**: 전고체(Li-In·Li·무음극)에서 OCV 적합이 LAM_PE 와 접촉 손실을 가르는가. 보류 항목이고 지금은 자료를 모으는 단계다. Q1~Q8 채움표 **2편 누적 ≈2.5/8** (2호가 Q8 전압축을 채웠고 Q4·Q5·Q6·Q7 은 여전히 0편).

## Syntheses (종합)

- [[mode-identifiability-unmeasured-lineage]] — 흡수한 17편(2026-09-11 현재)은 LLI/LAM 분해를 **보고**하지만 그 분해가 **유일한지**를 잰 편이 하나도 없고, **그것을 잴 도구는 이미 그 15편 안에 흩어져 있다**: 축퇴가 세 번 인쇄됐으나(Dubarry 식 · Birkl 산문 · Marongiu 식 (2)–(5)) 아무도 null 을 풀지 않았고, Lin 은 `C_θ` 를 쥐고 대각선만 그렸으며, 그리는 기계는 Schaeffer 에 있는데 **두 논문이 서로를 인용하지 않는다**(어휘 분단: `identifiab*` 26/0 vs `nullspace` 0/69). 우리 Phase 1c·1d 가 겨눈 결과와 "재지 않은 대가" 의 야생 실측(Marongiu: 초기값만 바꿔 오차 6.38 → 14.46 %; **Schmitt 2022: 음극 half-cell 곡선만 바꿔 LAM_an 15.5 → 13.1 % 인데 OCV RMSE 는 9.9 → 8.2 mV**)까지.

## Queries (질의 기록)

- [[lean-review-backlog]] — 사다리가 찾은 실제 중복 후보와 보류 사유 (리뷰 라운드 중 source_digest 변경 금지).
