---
title: mode-observability
description: "관측을 늘리면(PVS·SEV) 정말 LLI 와 LAM_PE 가 갈리는가 — Jacobian 식별 가능성 + ML 라벨 degeneracy 전파를 묻는 satellite"
created: 2026-09-03
updated: 2026-09-03
type: entity
tags: [project, satellite, battery, degradation, research]
sources: [raw/papers/2026-09-02-siwon-kim-degradation-mode-ml-seminar.md]
confidence: medium
explored: false
verificationStatus: unverified
claimType: prescriptive
evidenceScope: single-source
---

# mode-observability

## 개요

[[degradation-degeneracy]] 의 후속 질문 — "full-cell OCV **하나**로 안 갈리면,
**관측을 늘리면** 갈리는가" — 를 다루는 두 번째 satellite. 2026-09-02 BML
세미나가 제안한 [[pvs-sev-degradation-mode-features]] 가 그 "늘린 관측" 의
구체적 후보이고, 판별 설계는 [[pvs-sev-lli-lampe-separability]] 카드의 4단계를
따른다.

## 핵심 사실

- 위치: repo root `mode-observability/` (작업 브랜치는 루트 `CLAUDE.md`
  하드룰 1 참조 — 이름은 옮겨 적지 않는다).
- Phase 1 PVS Jacobian → Phase 2 SEV P2D 시뮬레이션 → Phase 3 ML 라벨
  degeneracy 전파. 셋 다 **미착수** (2026-09-03 개설).
- degradation-degeneracy 의 코드를 **읽기 전용으로 재사용**한다 — RUN_SCOPE
  (`src/ tools/ configs/ scripts/ run.sh requirements*.txt`)를 수정하지 않는
  것이 이 프로젝트의 하드 룰 1 (게이트 code identity 보호).
- Phase 1·2 는 본 실행 없이(국소 Jacobian) 판정하도록 설계했다.

## 이 위키와의 관계

- [[pvs-sev-lli-lampe-separability]] 의 `feedsInto` 대상 — 그 카드의 Evidence
  는 이 프로젝트의 실행 결과로 채워진다.
- [[22p-physics-or-degeneracy]] 의 "어떤 측정에서 분해가 의미를 갖는가" 축에
  답을 공급한다.
- 결과 수치의 정본은 이 satellite 의 artifact + docs — 위키에는 복사하지
  않는다 ([[provenance-fail-closed-verification]] 원칙).
