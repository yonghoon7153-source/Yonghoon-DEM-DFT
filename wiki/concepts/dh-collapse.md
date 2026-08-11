---
title: d_h 접힘 — 다섯 침대의 σ(φ) 를 채널폭 하나로
created: 2026-08-11
updated: 2026-08-11
type: concept
tags: [mpm, transport, calibration]
sources: [docs/se_curve_transfer_verdict_20260806.md, scripts/fit_dh_collapse.py, scripts/plan_se_curve_targets.py]
confidence: high
explored: false
verificationStatus: unverified
author: agent
claimType: empirical
evidenceScope: multi-source-primary
anchored: anchored
scope: relative-only
---

# d_h 접힘

## 정의
SE 응답곡선 σ(φ) 의 베드-간 차이(조성 의존, 같은 φ 에서 최대 1.87×)가
**수력반경 d_h = V_free/S_AM** 하나로 접힌다: log σ vs log d_h 선형.
가치는 지수 절대값이 아니라 **접힘 그 자체** — 새 전극마다 5점을 재는 대신
스캐폴드 CSV 에서 d_h 를 계산해 곡선을 이동하면 된다 (측정 부담 소멸).

## 핵심 수치 (인용 규약)
- 192 5침대: 기울기 −0.563 · R² 0.910 (전부 보간, 외삽 0).
- 288: 공통 φ 0.75 에서 −0.575 · R² 0.926 (현재 "소규모 외삽 포함" 라벨;
  프로토콜 대등화 8런 진행 — [[dh-288-protocol-equalization]]).
- ⚠ **기울기는 하한, 물리상수 인용 금지** — 격자 수렴차수 ≈0.10 (비수렴),
  |기울기| 는 조일수록 커진다.  해상도에 걸쳐 뜻이 있는 것은 R²(접히는가)뿐.
- ⚠ 공통 φ 는 단일점 침대들의 **착지 중앙값**에 둔다 (외삽 규모 최소화 규칙, §⑩).
- 실용 규칙: `d_h/dx ≳ 3.5` = SE 응력을 믿을 최소 해상도 (미해상 협착은 격자에서
  사라져 σ 를 낮게 낸다 — 부호가 직관과 반대였던 자리).

## 왜 중요한가
- SE 응답곡선의 베드-전이 기각(재하율 일치 후에도 2.8–3.8×)을 **구제**하는 유일한
  색인 — φ 가 못 담는 자유도(잔여공극 도달가능성)를 d_h 가 담는다.
- 재하율 통일이 전제: [[quasistatic-platen-gate]] (`--mach 0.03` 게이트 내장).

## 이 리포에서의 위치
- 도구: `scripts/fit_dh_collapse.py` (`--list` 로 섞임 확인 먼저) · 침대는 [[se-curve-kits]].
