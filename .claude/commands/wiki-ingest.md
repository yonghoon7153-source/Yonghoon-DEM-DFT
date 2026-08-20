---
description: 외부 자료를 raw source 로 저장하고 위키 페이지로 컴파일
---

> 이 위키는 repo root `wiki/` 하위다 (킷 원본과 배치가 다름 — `wiki/README.md` 참조). 아래 절차의 모든 경로는 repo root 기준이다.

새 자료를 이 LLM Wiki 에 ingest 한다. 대상: $ARGUMENTS

`wiki/SCHEMA.md` 의 규칙을 따른다. 절차:

1. **목적 확인 (Collection Purpose Gate)**: 사용자에게 딱 한 번 묻는다 — "이 자료를 왜 수집하나요? 어디에 쓸 예정인가요?" 답을 받은 뒤 진행한다.
2. **Raw 저장**: 본문을 가능한 한 원형 그대로 `wiki/raw/articles/YYYY-MM-DD-{slug}.md` (논문이면 `wiki/raw/papers/`, 전사면 `wiki/raw/transcripts/`, 레포 감사면 `wiki/raw/repositories/`) 에 저장한다. frontmatter 는 `source_url`, `ingested`, `sha256` — 해시는 frontmatter 이후 본문(선행 빈 줄 제거)의 sha256. 수집 목적은 raw 파일 본문 상단에 한 줄 기록한다.
3. **중복 확인**: `wiki/index.md` 를 읽고 이미 있는 페이지와 겹치는지 확인한다. 겹치면 새 페이지 대신 기존 페이지를 갱신한다 (`updated` bump).
4. **RQ 라우팅**: `wiki/questions/` 의 열린 research-question 카드(status: open|active)를 훑고, 이 자료가 근거를 주면 해당 카드의 Evidence For/Against 와 Status Log 에 추가한다 (`updated` bump).
5. **논문이면 (DOI/arXiv/저널)**: 기본은 일반 컴파일. 프로젝트가 이 논문의 수치·정의를 verbatim 반복 참조할 것 같으면 **Paper Ingest Mode 를 사용자에게 제안**한다 (`wiki/guides/paper-ingest-mode.md`) — 승인 전에는 실행 금지, 승인 후에도 필요한 좌표만.
6. **컴파일**: 핵심 개념/엔티티/비교를 위키 페이지로 만든다 (보통 concept 1~3개). 새 페이지 frontmatter 는 `explored: false`, `verificationStatus: unverified`, `confidence` 는 정직하게 + `model`/`effort`/`claimType`/`evidenceScope` 기록. 각 페이지에 `[[wikilink]]` 2개 이상, 관련 기존 페이지에도 역링크를 추가한다.
7. **등록**: `wiki/index.md` 에 한 줄 요약과 함께 등록하고, `wiki/log.md` 에 `## [YYYY-MM-DD] ingest | {제목}` 항목을 append 한다.
8. **Lint**: `python3 wiki/tools/lint.py` 를 실행해 0 errors 를 확인하고 결과를 보고한다.

Raw source 는 절대 수정하지 않는다. 해석은 위키 페이지에서만 한다.
