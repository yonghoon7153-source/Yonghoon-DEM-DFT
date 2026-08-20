---
description: 위키 건강 점검 (read-only) — 오류 보고와 수정 제안까지만
---

> 이 위키는 repo root `wiki/` 하위다 (킷 원본과 배치가 다름 — `wiki/README.md` 참조). 아래 절차의 모든 경로는 repo root 기준이다.

이 LLM Wiki 의 건강을 점검한다.

1. `python3 wiki/tools/lint.py` 를 실행한다.
2. 결과를 해석해 보고한다:
   - **ERRORS**: 깨진 링크, index 누락/불일치, frontmatter 누락, raw hash 불일치, 하드코딩된 브랜치 이름(검사 15) — 각각 원인과 수정 방법을 제시한다.
   - **WARNINGS**: orphan(들어오는 링크 없음), stale(90일 미갱신), 링크 2개 미만 — 조치가 필요한지 판단 근거와 함께 제시한다.
   - **NOTES**: confidence:high 인데 Bias Check/불확실성 섹션이 없는 페이지 — backlog 로 안내한다.
3. 추가로 `explored: false` 와 `verificationStatus: unverified` backlog 수를 요약하고, 다음 검증 대상을 1~2개 추천한다 (근거가 가장 오래됐거나 열린 research-question 에 물린 페이지 우선).

**Read-only 원칙**: 이 command 는 보고와 제안까지만 한다. 실제 수정은 사용자가 승인한 뒤에만 수행하고, 수정했다면 `wiki/log.md` 에 `## [YYYY-MM-DD] lint | {수정 요약}` 을 기록한다.
