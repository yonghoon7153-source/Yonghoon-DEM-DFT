---
source_url: https://github.com/johnfkoo951/cmds-llm-wiki/releases
ingested: 2026-08-06
sha256: 28e69723064765fa9f9dff3a8fccb14818912204fde5bbca7ce2c923e2cd8a1c
---

수집 목적: 우리 3-vault LLM Wiki 하네스를 원본 패턴(cmds-llm-wiki)의 v1.8~v1.10 업데이트에 맞춰 발전시키기 위한 근거 자료.

# cmds-llm-wiki 릴리스 노트 (v1.7.0 ~ v1.10.0)

출처: https://github.com/johnfkoo951/cmds-llm-wiki/releases 및 https://llm-wiki.cmdspace.work/ (v2.7 문서, 템플릿 v1.10.0, 2026-07-23). 2026-08-06 WebFetch 로 수집 — 페이지 요약본이며 원문 전문은 아님.

## v1.10.0 — Paper Ingest Mode (2026-07-23)
- 학술 논문 전용 3번째 ingest 모드. "12-step paper atomization".
- 흐름: Raw Source → Paper Hub(S00) → 지식 atom 30~100+ → Wiki 승격.
- 좌표 S01 CITATION ~ S12 WRITING VALUE, 논문 유형 6종 분기(quantitative, qualitative, theory-concept, mixed-methods, scale-development, meta-analysis).
- 목적은 요약이 아니라 집필 지원: "when you draft your own paper or post, you pull the original β values, definitions, and quotes verbatim from your atoms."
- DOI/arXiv/저널 URL 자동 감지, p7_verify.py 기계 검증(YAML 구조·좌표·provenance·인용문 원본 일치), v1.9 Research Question 카드 연동, Zotero 선택 연동.

## v1.9.1 — Documentation Update (2026-07-23)
- 카드 타입 사용처 구분 문서화: 위키 페이지(학습 기록) / Research Question 카드(진행 중 질문, status·feedsInto 라우팅) / Synthesis 카드(하나의 thesis 를 근거로 방어).

## v1.9.0 — Question & Argumentation Layer (2026-07-23)
- Research Question 카드: 반복해서 돌아오는 연구 질문을 1급 객체로. frontmatter status·questionType·feedsInto, 본문 질문 1문장 → 왜 중요한가 → 가설(H1…) → Evidence For / Against → Status Log(날짜별) → References.
- Synthesis 카드: targetVenue·supports·counters. 본문 Thesis 1문장 → Argument(claim+근거) → Counter-arguments(경쟁 가설 보존) → Gap(빈 근거) → References.
- 선택: Citation Standard (BetterBibTeX citekey, Pandoc/CSL, Zotero 호환). 템플릿 5종 → 7종.

## v1.8.0 — Provenance & Description Rules (2026-07-23)
- description 필드 따옴표 강제 (콜론·em-dash·괄호가 YAML 파싱을 깨는 것 방지).
- 에이전트 작성 콘텐츠에 model + effort 키 기록 — cross-runtime provenance. 전 템플릿 반영.

## v1.7.1 — Hook & Template Fixes (2026-07-02)
- macOS hook 런타임 버그(date 명령 이식성, stale-lock lockout), 누락 템플릿, 템플릿-스키마 drift 수정.

## v1.7.0 — v5 Verification Schema (2026-07-01)
- v5 검증 프레임워크 완성: Wiki Page 키 6종 신설 — claimType(definition·empirical·theoretical·historical·prescriptive·interpretive·mixed), evidenceScope(single-source·multi-source-primary·multi-source-mixed·synthesis-only·user-original), verificationStatus(verified·partial·unverified·disputed), verifiedAt(ISO date), verifiedBy(agent·human·both), disputed(boolean — 양방향 Disputed Claim callout).
- cross-vault 링크 하드닝, v5 lint 커버리지.

## 사이트 전역 현황 (v2.7 문서 기준)
- 3-Layer: Raw Sources 248 파일 / Wiki 754 페이지(Concepts 230, Entities 187, Guides 36, Maps 20) / CLAUDE.md 하네스.
- 커맨드 11종: ingest, query, lint, inbox, status, reindex, refresh-context, onboard, capture-tabs, verify, audit.
- Exploration Gate(v4): explored:false 시작, 사람 읽음 또는 에이전트 source-backed 검증 후 승격.
- Book Ingest: 5장+ 자료는 progressive stub(색인 1 + 챕터 stub, 읽으며 completed 승격).
- qmd MCP(BM25+Vector+HyDE) 검색, Obsidian Web Clipper 18종 — Obsidian 종속 기능.
- Mothership↔Satellite: Core Context.md 30일 스냅샷 + /refresh-context, 크로스-vault 는 obsidian:// URL.
