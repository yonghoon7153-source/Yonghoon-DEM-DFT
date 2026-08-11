---
title: 적대 리뷰 프로토콜 — 3각 자체리뷰 + Codex 교차 + 원장 등재
created: 2026-08-11
updated: 2026-08-11
type: guide
tags: [review, epistemology]
sources: [docs/reviews/selfreview_synthesis_vgcf_ptfe_se_grad_20260811.md, docs/reviews/codex_review_verdict_20260811.md, docs/reviews/findings.json, CLAUDE.md]
confidence: high
explored: false
verificationStatus: unverified
author: agent
claimType: prescriptive
evidenceScope: multi-source-primary
anchored: n-a
scope: n-a
---

# 적대 리뷰 프로토콜

## 목적
백로그 항목·계획서·헤드라인 수치를 **반박을 목표로** 검증한다 (2026-07-21 사용자
규약: 백로그 완료 시마다 코드·전기화학·물리 3각 적대 리뷰 필수).

## 절차
1. **3각 자체리뷰**: 물리/통계/구현 세 렌즈를 독립 실행 — 원본 PDF·실코드 직접
   검증, 가능하면 실제 솔버로 스탬프 실험까지 (추론 금지 원칙: "부호는 측정으로만").
2. **반영 후 Codex 교차 리뷰**: 자체리뷰가 반영된 버전을 리뷰시킨다.  요청서에
   질문을 명시 (근거는 [[litdb-canon]] 카드 = `litdb-canon:<slug>` 로 지목).
3. **원장 등재**: 발견은 전부 `docs/reviews/findings.json` ([[findings-ledger]]) —
   status 는 open → claimed_fixed → (Codex 재검증) → verified.  발견을 세션 로그에만
   두지 않는다 (RC6-Q8).
4. **수치는 하네스와 함께 커밋** (SR-02 교훈): 서브에이전트가 낸 수치도 raw
   vector·시드·하네스가 리포에 없으면 증거등급 C — 인용 금지.
5. **자기 오류 명시**: 자체리뷰가 못 잡은 자기 오류를 Codex 가 잡으면 그 표를
   리뷰 문서에 보존한다 (2026-08-11 실례: 밴드 오독·ESS 과장·재샘플 반증).

## 알려진 함정
- 자체 3각 리뷰는 **남의 오류는 잘 잡고 자기 오류는 못 잡는다** — 독립 리뷰가
  필요한 이유.  렌즈 간 충돌은 실험이 이긴다.
- 리뷰가 새 발견을 내면 (SR-01 처럼) 그것도 원장+위키 RQ 로 승격:
  [[sr01-delta-sigma-sign]] 이 그 전례.
- 정본 절차 문서: [[litdb-canon-procedure]] (근거 카드 접근).
