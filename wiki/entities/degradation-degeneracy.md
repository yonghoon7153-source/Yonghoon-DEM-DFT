---
title: degradation-degeneracy
description: "PyBaMM synthetic-truth grid for testing whether the 22p seminar LLI/LAM split is physics or fitting degeneracy"
created: 2026-08-11
updated: 2026-08-20
type: entity
tags: [project, satellite, battery, degradation, pybamm, gate-review]
sources: [raw/repositories/degradation-degeneracy-audit.md]
confidence: high
explored: false
verificationStatus: unverified
model: claude-fable-5
effort: high
claimType: empirical
evidenceScope: multi-source-primary
---

# degradation-degeneracy

## 개요
2026-08-05 세미나 22p 결과(LAM_PE ≈ LAM_NE ≈ 13%, LLI ≈ 17%)가 실제 물리인지
[[fitting-degeneracy]] 인지, 정답을 아는 PyBaMM 합성 곡선 격자로 판별하는 연구
프로젝트. 이 위키의 첫 satellite.

## 위치 (living reference — 내용 복사 금지)
- 코드: `degradation-degeneracy/` (작업 브랜치는 루트 `CLAUDE.md` 하드룰 1 참조 —
  브랜치 이름은 옮겨 적지 않는다. 브랜치 전체 지도는 루트 `BRANCHES.md`)
- 발견 대응 원장: `degradation-degeneracy/docs/08_REVIEW_RESPONSE.md`
- 게이트 리뷰 원문: `degradation-degeneracy/docs/1x_CODEX_*.md`
- 결과 정본: artifact + `degradation-degeneracy/docs/RESULTS*.md` (위키에 수치 복사 금지)

## 목표
1. 격자 truth 대비 복원 오차·degeneracy 비율로 22p 의 분리가능성 판정
2. 목적함수 4종(pOCV/dVdQ/dQdV 조합) 비교 — 무엇이 분리 능력을 더하는가
3. 기준 곡선 2종(Case 1 half-cell vs Case 2 grid) 비교

## 상태
- **[2026-08-11]** 13차 게이트 리뷰 요청 발신 (대상 `c9970ebc`). 12차까지의
  발견 전부 코드로 대응 — 테스트 277 passed, strict smoke 전 단계 통과.
  [[gate-review-loop]] 로 운영. GO 시 V100 에서 grid_curves_v4 재생성(~28분)
  후 약 10시간 파이프라인 (gfit → hfit → paired_fixed5 → wsweep → 채점·보고).
- **[2026-08-20]** 19차까지 진행, **본 실행 완료**. 테스트 650 passed, strict
  smoke exit 0. 발견 원장이 F1–F89 로 자랐다.
  - **결론이 실행 뒤에 바뀌었다** — 결론 1은 **철회**, 결론 2는 특정 모집단으로
    **한정**, 결론 3은 "reference-specific pipeline" 으로 **축소**됐다. 어느
    숫자가 어떻게 바뀌었는지는 원장 `docs/08_REVIEW_RESPONSE.md` §20.4 정정
    블록과 `docs/RESULTS*.md` 가 정본이다 (여기에 옮겨 적지 않는다).
  - 산출물이 문서보다 앞서 나가는 것을 막으려고, 철회된 주장은
    `docs/05_HANDOFF.md` 상단 배너와 절별 `⛔ 철회` + claim ID 표시로 고정하고
    `tests/test_docs_lint.py` 가 그 표시를 강제한다.
  - 진행 중: 모델 오차(half-cell OCP 왜곡) 민감도 스윕. 남은 항목은
    `docs/09_22P_GAP.md` §10 에 7개로 목록화돼 있다.
- 검증 설계는 [[provenance-fail-closed-verification]] 에 증류. 핵심 연구 질문
  카드는 [[22p-physics-or-degeneracy]].

## 한계
- 모든 비율은 guard-feasible 모집단에 **조건부**다 — 제외된 조건의 물리적
  정당성은 guard 재평가로 증명되지만 외삽 가능성은 별개 문제다. 모집단 크기와
  제외 수는 artifact·`docs/RESULTS*.md` 가 정본이다 (위키에 수치 복사 금지).
- 이 페이지의 상태 서술은 **파이프라인 진행 상태**이지 연구 결론이 아니다.
  결론은 실행 뒤 실제로 철회·한정됐으므로, 인용은 반드시 정본에서 한다.
