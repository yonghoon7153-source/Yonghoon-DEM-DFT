---
title: SR-01 — STEP3 점-스탬프가 탄소 섬유를 조각낸다
created: 2026-08-11
updated: 2026-08-11
type: concept
tags: [transport, additive, pipeline, review]
sources: [docs/reviews/findings.json, scripts/sr01_realbed_ab.py, scripts/fibre_segment_raster.py, scripts/sr01_stamp_ab.sh, docs/reviews/selfreview_synthesis_vgcf_ptfe_se_grad_20260811.md]
confidence: high
explored: false
verificationStatus: unverified
author: agent
claimType: empirical
evidenceScope: multi-source-primary
anchored: anchored
scope: n-a
---

# SR-01 — 점-스탬프 섬유 조각남

## 정의
STEP3 탄소 채널은 첨가제 **점**들을 1-복셀씩 찍는데(6-면 연결 FV), 점 간격이
MPM dx(≈0.099 µm)에 묶여 있고 STEP3 vox 는 0.4 µm 라 **오블리크 스텝의
코너-크로싱**에서 대각 셀이 면을 공유하지 못해 전기적으로 끊긴다.
실침대 실측: 킷별 섬유의 **20.6–75.8 %** 가 끊긴다 (`sr01_realbed_ab.csv`).

## 확정된 것 / 미확정인 것
- 확정: 기하 단절은 실재하고 점 재샘플링으로는 **원리적으로 못 고친다**
  (0.35·vox 에서도 96–97 % 단절 — Codex 재현).  해결은 선분-스탬프
  (Amanatides–Woo supercover, `scripts/fibre_segment_raster.py`, opt-in
  `--step3-fibre-stamp segment`).
- 미확정: **Δσ_e 의 부호와 크기.**  자체리뷰와 Codex 가 각각 부호를 추론했다가
  반대 결론에 닿았다 — 끊긴 섬유가 백본이 아니면 σ 는 안 움직이고, 조각남이
  병렬 경로·스탬프 부피 인플레와 겹치면 과대평가일 수도 있다.
  ⇒ **부호는 재야 안다**: [[sr01-delta-sigma-sign]].
- 범위 주의 (Codex CR-02): "동일 설정 상대비교는 생존" 은 **좁게만** 참 —
  같은 섬유 기하 고정 + σ 스칼라 변경 정도.  grade·n_grid·SBE↔DBE·raster
  origin 이 바뀌면 오차가 직접 달라진다 → 첨가제 headline 비교의 P1 blocker.

## 이 리포에서의 위치
- 원장 항목: SR-01 (docs/reviews/findings.json, [[findings-ledger]]).
- A/B 실행 절차는 [[kit-run-protocol]] · 판독기는 `scripts/sr01_stamp_compare.py`.
