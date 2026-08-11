---
description: 자료를 위키에 흡수 (논문이면 litdb 정본으로 라우팅)
---

새 자료를 wiki/ 에 ingest 한다. 대상: $ARGUMENTS

`wiki/SCHEMA.md` 를 따른다. 절차:

1. **라우팅 게이트**: 대상이 **논문**(DOI/arXiv/저널 PDF)이면 여기서 멈추고 litdb-curator
   에이전트("논문 에이전트")로 보낸다 — 카드는 정본 서랍(friendly-meitner)에만
   (절차: wiki/guides/litdb-canon-procedure.md). 위키에는 그 카드를
   `litdb-canon:<slug>` 로 참조하는 concept/comparison 만 만든다.
2. **목적 확인**: 딱 한 번 묻는다 — "이 자료를 왜 수집하나요? 어디에 쓸 예정인가요?"
3. **원본 저장**: 리포에 이미 있는 파일(docs/, docs/data/)이면 그대로 sources 로 쓴다
   (복사 금지). 리포 밖 자료(강연 전사 등)만 `wiki/raw/<분류>/YYYY-MM-DD-{slug}.md` 에
   저장 (frontmatter: source_url, ingested; 수정 금지).
4. **중복 확인**: `wiki/index.md` 를 읽고 겹치면 새 페이지 대신 기존 페이지 갱신 (`updated` bump).
5. **RQ 라우팅**: `wiki/questions/` 의 open|active 카드와 `anchor-waitlist` 를 훑고, 이
   자료가 근거/앵커를 주면 해당 카드의 Evidence·Status Log 에 추가한다.
6. **컴파일**: concept 1~3개. `python3 wiki/tools/new_page.py <type> <slug>` 로 만들고
   frontmatter 정직하게 (`confidence`, `anchored`, `scope`; single-source 면 high 금지).
   `[[위키링크]]` 2개 이상 + 관련 기존 페이지에 역링크. ⚠ 모델 ID 를 페이지에 적지 않는다.
7. **등록**: `wiki/index.md` 한 줄 등록(+Total 갱신), `wiki/log.md` append.
8. **Lint**: `python3 wiki/tools/lint.py` 0 errors 확인 후 보고.
