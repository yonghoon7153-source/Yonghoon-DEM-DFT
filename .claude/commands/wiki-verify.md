---
description: 단일 페이지를 raw 원문과 대조 검증하고 verificationStatus 를 기록
---

> 이 위키는 repo root `wiki/` 하위다 (킷 원본과 배치가 다름 — `wiki/README.md` 참조). 아래 절차의 모든 경로는 repo root 기준이다.

위키 페이지 하나를 source 대조 검증한다. 대상 페이지: $ARGUMENTS

절차 (v5 간소화):

1. 대상 페이지를 읽고, 검증 가능한 주장(claim)들을 추린다.
2. frontmatter 의 `sources` 에 적힌 raw 파일(들)을 열어 각 주장을 원문과 대조한다.
3. 다른 위키 페이지와 모순이 없는지도 확인한다 (관련 링크 페이지 위주).
4. 판정과 write-back:
   - **일치** → `verificationStatus: verified`, `verifiedAt: YYYY-MM-DD`, `verifiedBy: agent` 기록, `updated` bump.
   - **불일치 발견** → 페이지를 고치거나 `confidence` 를 낮춘 뒤 검증을 다시 본다. 무엇을 왜 고쳤는지 보고한다.
   - **페이지 간 충돌** → 어느 쪽도 삭제하지 않고 양쪽 `verificationStatus: disputed` + 본문에 `> [!warning] Disputed Claim` callout 으로 상호 링크한다.
5. `wiki/log.md` 에 `## [YYYY-MM-DD] verify | {페이지}` 기록 후 `python3 wiki/tools/lint.py` 실행.

**금지**: `explored` 필드는 절대 건드리지 않는다 — 사람이 읽었는가는 사람만 바꾼다.
