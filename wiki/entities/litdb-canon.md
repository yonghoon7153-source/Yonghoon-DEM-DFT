---
title: litdb 정본 — 논문 카드의 단일 서랍 (friendly-meitner 브랜치)
created: 2026-08-11
updated: 2026-08-11
type: entity
tags: [review, wiki, pipeline]
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

# litdb 정본 (단일 서랍)

## 개요
논문 카드(digest)의 정본은 **`origin/claude/friendly-meitner-lldvar` 의 `litdb/`
하나뿐**이다.  어느 세션에서 일하든 새 카드는 거기에만 넣는다 (litdb 한정 그
브랜치 커밋/푸시 상시 승인, 2026-07-16).  이 브랜치(stoic-knuth)의 `litdb/` 는
2026-07-16 동결 스냅샷 — 참조 가능, 추가/수정 금지.

## 핵심 사실
- 중복 사례 교훈: ECER-D-26-00097 을 두 세션이 각자 digest → 정본은
  `fan2026_sulfide_assb_stability_review_ECERD2600097.md`, 이 브랜치 사본은 동결.
  **카드 만들기 전 정본 INDEX 먼저 확인.**
- 카드 생성은 litdb-curator 에이전트("논문 에이전트") 소관 — 위키가 아니다.
- 위키와의 경계 ([[llm-wiki-kit-origin]] 채택 때 확정): 위키는 논문을 ingest 하지
  않는다.  카드를 `litdb-canon:<card-slug>` 로 **참조**하는 concept/comparison 만
  만든다 (킷의 Paper Ingest Mode 폐기).  lint 가 참조 형식을 검사한다.
- 오래된 lit digest 일부는 `docs/lit_*.md` 에 남아 있다 (litdb 이전 시절) — 신규는
  전부 정본으로.

## 관련 페이지·경로
- 정본 접근 절차(워크트리): [[litdb-canon-procedure]]
- 리뷰에서 카드를 근거로 쓰는 규약: [[adversarial-review-protocol]]
