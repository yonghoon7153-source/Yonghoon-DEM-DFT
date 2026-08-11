---
description: 컴파일된 위키를 근거로 질문에 답하고, 재사용 가치가 있으면 file-back
---

> 이 위키는 repo root `wiki/` 하위다 (킷 원본과 배치가 다름 — `wiki/README.md` 참조). 아래 절차의 모든 경로는 repo root 기준이다.

이 LLM Wiki 를 근거로 다음 질문에 답한다: $ARGUMENTS

절차:

1. `wiki/index.md` 에서 관련 페이지를 고르고, 해당 위키 페이지들을 읽는다. 필요하면 frontmatter 의 `sources` 를 따라 raw 원문까지 내려간다.
2. 답변을 합성하되 **사용한 위키 페이지를 명시**한다. 인용하는 페이지의 `verificationStatus` 와 `confidence` 를 함께 확인한다 — verified + high 면 단언하고, unverified 나 medium 이하면 그렇다고 밝히고, disputed 면 양쪽 입장을 모두 제시한다.
3. 위키에 근거가 없으면 없다고 말한다. 지어내지 않는다.
4. **File-back 판단**: 답변이 한 번 쓰고 버리기 아까운 것(비교, 의사결정, 종합)이면 `wiki/queries/` (비교성이면 `wiki/comparisons/`) 에 저장을 제안한다. 저장 시: SCHEMA frontmatter (`type: query`, `explored: false`, `verificationStatus: unverified`), 질문/짧은 답/근거/관련 구조, `wiki/index.md` 등록, `wiki/log.md` 에 `## [YYYY-MM-DD] query | {질문}` 기록, lint 실행.
