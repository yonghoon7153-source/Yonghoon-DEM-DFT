# 위키 색인

> 내용 목록. 모든 위키 페이지를 종류별로 한 줄 요약과 함께 싣는다.
> 마지막 갱신: 2026-09-03 | 전체 페이지: 21

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
- [[dv-peak-heterogeneity-descriptor]] — Kim 2023 의 DV `Peak_S2`: 진폭이 아니라 **ridge 절대 높이**이며(진폭은 valley 노이즈로 폐기), LFP‖Gr 에서의 음극 단일 귀속은 PVS 해석과 충돌하지 않는다 — 좌표를 맞추면 오히려 일치.

## Comparisons (비교)

## Guides (절차)

- [[gate-review-loop]] — 비싼 본 실행 전 외부 리뷰어와 도는 적대적 게이트 루프: 수정 → 검증 → push → 대상 커밋 명시 요청문 → GO 후에만 실행.
- [[new-project-kickoff]] — 새 프로젝트 킥오프 프롬프트: 폴더 세팅 + satellite 등록 표준 절차 (repo-root 상대 경로 `wiki` 적응판).
- [[paper-ingest-mode]] — 논문 수치·정의를 verbatim atom 으로 분해하는 opt-in ingest 모드 (사용자 승인 필수).

## Questions (열린 질문)

- [[22p-physics-or-degeneracy]] — 핵심 연구 질문 카드 (status: active): 22p 분해는 물리인가 flat-valley 결합의 산물인가.
- [[pvs-sev-lli-lampe-separability]] — 질문 카드 (status: open): PVS·SEV 두 feature 가 LLI 와 LAM_PE 를 실제로 가르는가, 아니면 같은 대비 하나를 재는가.

## Syntheses (종합)

## Queries (질의 기록)

- [[lean-review-backlog]] — 사다리가 찾은 실제 중복 후보와 보류 사유 (리뷰 라운드 중 source_digest 변경 금지).
