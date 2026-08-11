---
title: litdb 정본 접근 절차 — 워크트리로 카드 추가/조회
created: 2026-08-11
updated: 2026-08-11
type: guide
tags: [review, environment, wiki]
sources: [CLAUDE.md, litdb/INDEX.md]
confidence: high
explored: false
verificationStatus: unverified
author: agent
claimType: prescriptive
evidenceScope: multi-source-primary
anchored: n-a
scope: n-a
---

# litdb 정본 접근 절차

## 목적
논문 카드를 정본 서랍([[litdb-canon]])에만 넣고, 다른 브랜치 세션에서 안전하게
조회/추가한다.  중복 digest 사고(ECER 이중 카드)의 재발 방지.

## 절차
1. **조회만**: 이 브랜치의 `litdb/` 동결 스냅샷(2026-07-16)을 읽는다 — 추가/수정 금지.
   최신 카드가 필요하면 `git fetch origin claude/friendly-meitner-lldvar` 후
   `git show origin/claude/friendly-meitner-lldvar:litdb/INDEX.md`.
2. **카드 추가** (litdb 한정 상시 승인, 2026-07-16):
   ```bash
   git fetch origin claude/friendly-meitner-lldvar
   git worktree add ../litdb-canon origin/claude/friendly-meitner-lldvar -b tmp-litdb
   # 카드 작성 (litdb-curator 에이전트 = "논문 에이전트" 사용)
   # → ../litdb-canon 브랜치로 커밋/푸시 → git worktree remove
   ```
3. **만들기 전 정본 INDEX 먼저 확인** — 이미 있으면 기존 카드 갱신.
4. **위키에서 참조**: `litdb-canon:<card-slug>` (lint 가 형식 검사).  카드 내용을
   위키로 복사하지 않는다 (living reference).
5. 카드가 [[anchor-waitlist]] 의 대기 항목에 앵커를 주는지 매번 대조한다.

## 주의
- 코드/문서 등 litdb 외 파일은 여전히 작업 브랜치에만 — 정본 브랜치는 litdb 전용.
- 리뷰 근거로 쓸 때의 규약은 [[adversarial-review-protocol]].
