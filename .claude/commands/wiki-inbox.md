---
description: inbox/ 대기 자료를 미리보고 일괄 ingest 라우팅
---

> 이 위키는 repo root `wiki/` 하위다 (킷 원본과 배치가 다름 — `wiki/README.md` 참조). 아래 절차의 모든 경로는 repo root 기준이다.

`wiki/inbox/` 폴더의 대기 자료를 처리한다.

절차:

1. **스캔**: `wiki/inbox/` 의 파일 목록을 본다 (`README.md` 제외). 비어 있으면 "inbox 비어 있음"을 보고하고 끝낸다.
2. **미리보기**: 각 파일에 대해 제목/출처 URL(있으면)/한 줄 요약/제안 분류(`wiki/raw/articles|papers|transcripts|repositories`)를 표로 보여준다. `urls.md` 가 있으면 각 URL 을 개별 항목으로 다룬다.
3. **확인**: 어떤 항목을 ingest 할지, 수집 목적이 무엇인지 사용자에게 **한 번에** 묻는다 (항목마다 따로 묻지 않는다).
4. **처리**: 승인된 각 항목에 대해 `/wiki-ingest` 절차를 그대로 수행한다 — raw 저장(frontmatter: source_url/wiki-ingested/sha256) → 중복 확인 → 위키 컴파일(`explored: false`, `verificationStatus: unverified`) → `wiki/index.md`/`wiki/log.md` 갱신.
5. **정리**: ingest 가 lint 까지 통과한 항목만 inbox 원본을 삭제한다 (move 의미론 — raw 에 원문이 보존되었을 때만).
6. **보고**: 처리 N건 / 보류 M건 / 생성·갱신된 페이지 목록.
