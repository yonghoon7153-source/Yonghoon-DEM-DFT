---
title: RQ — 점-스탬프 아티팩트는 σ_e 를 어느 방향으로 얼마나 움직이나
created: 2026-08-11
updated: 2026-08-11
type: research-question
tags: [transport, additive, review]
sources: [docs/session_20260811_progress.md, docs/reviews/findings.json, scripts/sr01_stamp_ab.sh, scripts/sr01_stamp_compare.py]
confidence: medium
explored: false
verificationStatus: unverified
author: agent
claimType: empirical
evidenceScope: multi-source-primary
anchored: n-a
scope: n-a
status: active
feedsInto: SR-01 종결 + 첨가제 headline 비교 재개 (grade/P3 blocker 해제)
---

# RQ — Δσ_e 의 부호와 크기

> [!question] 같은 압밀 베드에서 STEP3 래스터만 점→선분으로 바꾸면 σ_e 가 어느 방향으로 얼마나 움직이는가?

## 왜 중요한가
기하 단절률(킷별 20.6–75.8 %, [[sr01-stamp-fragmentation]])에서 σ_e 오차로 가는
다리가 없다.  부호 추론은 두 번 다 반쪽이 틀렸다 (자체리뷰 ↔ Codex 상반).
이 답이 나와야 첨가제 headline 비교(P1 blocker)가 풀린다.

## 가설
- H1 (과소평가): 점-스탬프가 탄소 백본을 끊어 σ_e ↓ → 선분에서 σ_e ↑.
- H2 (과대평가): 조각들이 여분 도통 경로·부피 인플레(9–20×)를 만들어 σ_e ↑ → 선분에서 ↓.
- H3 (무영향): 끊긴 섬유가 애초에 백본이 아니어서 |Δ| < 1 %.

## Evidence For
- (H1 쪽 정황) 토이 탄소 단독망: 점 = 비퍼콜(σ_z=0) vs 선분 0.0226 — 단 상한 성격.
- (H3 쪽 정황, 2026-08-11 arm A 실측) **VGCF 가 전자 전류의 4 % 만 나른다**
  (share AM_S 39 / AM_P 57 / VGCF 4 / SE 0) → 탄소상 아티팩트가 σ_e 를 움직일
  상한이 작다.  ⚠ 단 이건 **점-스탬프 팔** 값이라 조각남이 탄소 몫을 억눌러 4 % 로
  보일 수도 있다 — 선분 팔의 share 가 판별한다.

## Evidence Against
- 실침대는 AM 백본이 병렬로 있어 토이의 극단이 그대로 전이되지 않는다.

## Status Log
- [2026-08-11] active — arm A 전자 채널 **완료**: σ_e_eff 0.005122 S/cm
  (2,713,168 dof, resid 1.0e-08, CPU 3,485 s).  미수렴 경고 없음.  이온·열 진행 중.
  베드는 rate-오염(V/c_P 0.428) → Δ 만 유효, 절대값 인용 금지.  전문 원장:
  docs/session_20260811_progress.md
- [2026-08-11] active — A/B 하네스 완성 (`sr01_stamp_ab.sh` — 두 팔 직접 실행,
  manifest 도장 검증, selftest 28/28).  킷 압밀은 완료(ps_7_3), payload 는
  skimage 결손으로 1회 실패 → 의존 설치 후 A/B 실행 대기.  ⚠ 그 베드는
  rate-오염 (V/c_P 0.43) — Δ 는 공통모드로 유효하나 베드 절대값은 인용 금지
  ([[quasistatic-platen-gate]]).
