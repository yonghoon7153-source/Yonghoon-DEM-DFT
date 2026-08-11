---
title: 적대 리뷰 프로토콜 — 3각 자체리뷰 + Codex 교차 + 원장 등재
created: 2026-08-11
updated: 2026-08-11
type: guide
tags: [review, epistemology]
sources: [scripts/context_budget.py, docs/reviews/selfreview_synthesis_vgcf_ptfe_se_grad_20260811.md, docs/reviews/codex_review_verdict_20260811.md, docs/reviews/findings.json, CLAUDE.md]
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

## 수정 순서 — 재현 테스트가 먼저 (2026-08-11 채택)
결함을 고치기 **전에** 그 결함을 재현하는 selftest 를 추가한다 (superpowers 의
red-green 을 우리 selftest 문화에 맞춘 것).  실효가 확인된 사례:
- 스탬프 도장 경로가 한 단계 얕아 `stamp_of` 가 **항상 None** 이던 것 → 6b 가 잡음.
- `trace_deps` 가 importlib 경로 간선을 못 따라가 skimage 를 놓친 것 → 8b 가 잡음.
- `context_budget` 이 여러 줄 경고를 문장 중간에서 **자르던** 것 → 5b 가 잡음.
테스트 없이 고치면 "고쳤다" 와 "안 깨졌다" 를 구분할 수 없다.

## 새로 만들기 전 사다리 (ponytail, 2026-08-11 채택)
필요한가 → **이 리포에 이미 있나** → stdlib → 기존 의존 → 최소 구현.
2번이 우리 급소다: `status_for_value()` 가 `_sigma_status()` 를 중복하며 NaN 처리를
빠뜨린 것, 웹앱↔킷 두 파이프라인에 같은 결함이 따로 존재하는 것이 같은 뿌리다.
리뷰에서 "이거 이미 있지 않나" 를 명시적으로 한 번 묻는다.

## 알려진 함정
- 자체 3각 리뷰는 **남의 오류는 잘 잡고 자기 오류는 못 잡는다** — 독립 리뷰가
  필요한 이유.  렌즈 간 충돌은 실험이 이긴다.
- 리뷰가 새 발견을 내면 (SR-01 처럼) 그것도 원장+위키 RQ 로 승격:
  [[sr01-delta-sigma-sign]] 이 그 전례.
- 정본 절차 문서: [[litdb-canon-procedure]] (근거 카드 접근).
