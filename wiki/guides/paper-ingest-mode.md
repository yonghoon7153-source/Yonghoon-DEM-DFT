---
title: Paper Ingest Mode
created: 2026-08-06
updated: 2026-08-11
type: guide
tags: [wiki]
sources: [raw/articles/2026-08-06-cmds-llm-wiki-changelog.md]
confidence: medium
explored: false
verificationStatus: unverified
model: claude-fable-5
effort: max
claimType: prescriptive
evidenceScope: single-source
---

# Paper Ingest Mode

## 목적
논문의 수치·정의·인용문을 나중에 **verbatim 재사용**할 수 있는 atom 페이지로 분해하는 ingest 모드. 일반 /ingest 는 논문을 요약 1~3페이지로 뭉개는데, 집필·재분석 시 "그 논문의 β 값이 정확히 뭐였지"를 다시 원본에서 찾게 된다. 이 모드는 그 재조회 비용을 없앤다. 원본 패턴: cmds-llm-wiki v1.10.0 "12-step paper atomization" (Raw → Hub → atom 30~100+ → Wiki 승격)의 **lite 채택판**.

## 발동 조건 (opt-in — 자동 실행 금지)
1. 기본값: 논문도 일반 /ingest (요약 컴파일)로 처리한다.
2. 에이전트는 **프로젝트가 이 논문의 수치·정의를 반복 참조할 것 같을 때만** 이 모드를 사용자에게 제안한다 — "이 논문 X, paper ingest 로 atom 화할까? 필요한 좌표는 A·B·C."
3. **사용자 승인 후 실행.** 승인 없이는 절대 실행하지 않는다.
4. 논문 전체(12좌표)가 아니라 **필요한 좌표만** 부분 atomization 한다.

## 절차
1. **감지·분류**: DOI/arXiv/저널 URL 확인. 논문 유형 분류 — quantitative / qualitative / theory-concept / mixed-methods / scale-development / meta-analysis (유형에 따라 의미 있는 좌표가 다름).
2. **범위 합의**: 어떤 좌표가 필요한지 사용자와 합의. 좌표 세트 (원본 S01~S12 의 lite 버전):
   - `citation` — 서지 정보, 인용 형식
   - `method` — 방법론 핵심 (조건, 프로토콜)
   - `results` — 수치 결과 **verbatim** (β, 효율, 오차 포함 원문 그대로)
   - `definitions` — 용어 정의 원문
   - `limitations` — 저자가 인정한 한계
   - `writing-value` — 재사용할 표현·프레이밍
3. **Raw 저장**: `raw/papers/YYYY-MM-DD-{slug}.md` 로 원문 저장 (sha256 규칙 동일).
4. **Hub + atom 컴파일**: hub 는 concept 1페이지 (논문 개요 + atom 목록), atom 은 좌표당 섹션 또는 독립 페이지 — 소수면 hub 안의 섹션으로 충분 (페이지 남발 금지, Page Thresholds 준수).
5. **인용 검증**: 모든 verbatim 인용·수치를 raw 원문과 대조한다. 원문에 없는 문자열은 atom 에 넣지 않는다.
6. **RQ 라우팅**: 열린 research-question 카드에 이 논문이 근거를 주면 Evidence For/Against 에 추가한다.

## 한계·불확실성
- 원본 v1.10.0 의 정식 12좌표 이름 전체(S01~S12)는 미확보 — 위 좌표 세트는 릴리스 노트 기반 adapted 버전이다. 원본 템플릿 확보 시 갱신.
- 대량(수백~수천 편) 자동 처리는 이 모드의 범위가 아니다 — 사람이 정독할 소수 논문 전용.

## 관련
- [[llm-wiki-pattern]] — 이 모드가 붙는 위키 패턴 본체
- [[new-project-kickoff]] — satellite 등록 절차 (프로젝트가 논문을 반복 참조하게 되면 이 모드를 제안)
