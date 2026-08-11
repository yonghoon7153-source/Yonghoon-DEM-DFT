---
description: 위키를 근거로 답하고, 재사용 가치가 있으면 file-back
---

wiki/ 를 근거로 다음 질문에 답한다: $ARGUMENTS

1. `wiki/index.md` 에서 관련 페이지를 고르고 읽는다 (분류표의 미이관 docs/ 문서 포함).
   필요하면 frontmatter `sources` 를 따라 정본(docs/·scripts/·litdb)까지 내려간다.
2. 답변에 **사용한 페이지를 명시**하고 `verificationStatus`/`confidence`/`scope` 를 함께
   확인한다 — verified+high 면 단언, unverified·medium 이하면 그렇다고 밝히고,
   disputed 면 양쪽 제시, `scope: relative-only` 수치는 절대값으로 인용하지 않는다.
3. 위키·정본에 근거가 없으면 없다고 말한다. 지어내지 않는다 (§F1).
4. **File-back**: 한 번 쓰고 버리기 아까운 답(비교·의사결정·종합)이면 `wiki/queries/`
   (비교성이면 comparisons/) 저장을 제안한다 — new_page.py 로 만들고 index/log/lint.
