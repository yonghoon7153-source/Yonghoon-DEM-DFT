---
title: RQ — 288 5침대 프로토콜 대등화가 φ-선택 감도를 없애는가
created: 2026-08-11
updated: 2026-08-11
type: research-question
tags: [mpm, calibration, transport]
sources: [docs/se_curve_transfer_verdict_20260806.md, scripts/run_se_curve_batch.sh, scripts/fit_dh_collapse.py]
confidence: medium
explored: false
verificationStatus: unverified
author: agent
claimType: empirical
evidenceScope: multi-source-primary
anchored: anchored
scope: relative-only
status: active
feedsInto: d_h 접힘의 288 정식 인용값 (외삽 0) + 검증서 §⑩ 규칙 검증
---

# RQ — 288 대등화와 φ-선택 감도

> [!question] 4침대 × 바깥 2점 = 8런을 채워 288 이 전부-보간이 되면, 공통 φ 0.72↔0.75 가 R² 를 0.844↔0.926 으로 가르던 감도가 사라지는가?

## 왜 중요한가
[[dh-collapse]] 의 288 값은 현재 "소규모 외삽 포함" 라벨이다 — 네 침대가 단일점이라
공통 φ 선택이 외삽 규모를 정하고, 그 보정을 192 곡선으로 해서 방법이 섞인다.
대등화되면 φ-감도는 192 수준(±0.03–0.05, 방법 혼합 없음)으로 줄어야 하고,
그게 §⑩ "공통 φ = 단일점 착지 중앙값" 규칙의 검증이다.

## 가설
- H1: 대등화 후 φ0.72/0.75 두 적합이 같은 방향·비슷한 R² → 규칙 검증, 라벨 제거.
- H2: 감도가 남는다 → φ-선택이 외삽 규모가 아닌 다른 것(침대별 곡선 곡률)을 반영
  — 접힘 해석 재검토.

## Evidence For
- 같은 φ0.75 에서 192→288: R²·잔차 sd·LOO·|기울기| 네 지표 전부 개선/가팔라짐
  방향 (§⑩) — 정밀화가 접힘을 강화한다는 자기일관.

## Evidence Against
- (아직 없음 — 8런 완료 후 기입)

## Status Log
- [2026-08-11] active — 계획 확정: 8런 (12 아님 — 중간점 4개 기존, planner ε 이
  격자 무관임을 확인) ≈ 13–15 h GPU.  `run_se_curve_batch.sh --skip-existing`
  신설, dry-run 으로 skip 5점 확인.  침대·게이트는 [[se-curve-kits]] ·
  [[quasistatic-platen-gate]].  SR-01 A/B 뒤에 착수 (GPU 한 대 = 한 런).
