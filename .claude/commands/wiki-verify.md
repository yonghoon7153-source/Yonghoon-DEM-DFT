---
description: 위키 페이지 하나를 sources 와 대조 검증
---

위키 페이지 하나를 source 대조 검증한다. 대상: $ARGUMENTS

1. 페이지를 읽고 검증 가능한 주장(수치·판정)을 추린다.
2. frontmatter `sources` 의 파일들(docs/·scripts/·litdb 동결 스냅샷·URL)을 열어 각
   주장을 원문과 대조한다. 수치는 자릿수까지.
3. 관련 위키 페이지·루트 CLAUDE.md 와 모순이 없는지 확인한다 (루트가 상위 규범).
4. 판정: 일치 → `verificationStatus: verified` + `verifiedAt`/`verifiedBy: agent`,
   `updated` bump / 불일치 → 페이지를 고치고 무엇을 왜 고쳤는지 보고 / 페이지 간
   충돌 → 양쪽 `disputed` + `> [!warning] Disputed` callout 상호 링크 (삭제 금지).
5. `wiki/log.md` 에 `## [YYYY-MM-DD] verify | {페이지}` append 후
   `python3 wiki/tools/lint.py`.

**금지**: `explored` 는 절대 건드리지 않는다 — 사람만 바꾼다.
