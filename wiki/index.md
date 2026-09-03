# 위키 색인

> 내용 목록. 모든 위키 페이지를 종류별로 한 줄 요약과 함께 싣는다.
> 마지막 갱신: 2026-09-03 | 전체 페이지: 25

## Entities (satellite 프로젝트)

- [[degradation-degeneracy]] — 22p LLI/LAM 분해가 물리인지 degeneracy 인지 판별하는 PyBaMM 합성 truth 프로젝트 (첫 satellite, 13차 게이트 리뷰 대기).
- [[mode-observability]] — "관측을 늘리면 갈리는가": PVS·SEV Jacobian 식별 가능성 + ML 라벨 degeneracy 전파 (둘째 satellite, 2026-09-03 개설).

## Concepts (개념)

- [[fitting-degeneracy]] — full-cell 곡선 하나로 LLI/LAM_PE/LAM_NE 를 가를 수 있는가: flat valley(데이터 한계) vs multimodal(최적화 난이도) 구분.
- [[provenance-fail-closed-verification]] — 13 라운드 게이트 리뷰에서 증류된 재현성 설계 원칙 7가지 (서명·재계산 렌더·봉인 읽기·fail-closed·신뢰 경계).
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

## Syntheses (종합)

- [[mode-identifiability-unmeasured-lineage]] — 흡수한 13편은 LLI/LAM 분해를 **보고**하지만 그 분해가 **유일한지**를 잰 편이 하나도 없고, **그것을 잴 도구는 이미 그 13편 안에 흩어져 있다**: 축퇴가 세 번 인쇄됐으나(Dubarry 식 · Birkl 산문 · Marongiu 식 (2)–(5)) 아무도 null 을 풀지 않았고, Lin 은 `C_θ` 를 쥐고 대각선만 그렸으며, 그리는 기계는 Schaeffer 에 있는데 **두 논문이 서로를 인용하지 않는다**(어휘 분단: `identifiab*` 26/0 vs `nullspace` 0/69). 우리 Phase 1c·1d 가 겨눈 결과와 "재지 않은 대가" 의 야생 실측(Marongiu: 초기값만 바꿔 오차 6.38 → 14.46 %)까지.

## Queries (질의 기록)

- [[lean-review-backlog]] — 사다리가 찾은 실제 중복 후보와 보류 사유 (리뷰 라운드 중 source_digest 변경 금지).
