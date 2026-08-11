---
title: P:S 킷 5종 (kit_ps_*) — SE 응답곡선·d_h 의 대조군 침대
created: 2026-08-11
updated: 2026-08-11
type: entity
tags: [mpm, calibration, dem]
sources: [docs/data/kit_ps_scaffolds, scripts/unpack_kit_scaffolds.py, scripts/run_se_curve_batch.sh, docs/data/se_curve_metrics]
confidence: high
explored: false
verificationStatus: unverified
author: agent
claimType: definition
evidenceScope: multi-source-primary
anchored: anchored
scope: n-a
---

# P:S 킷 5종

## 개요
`kit_ps_{10_0,7_3,5_5,3_7,0_10}` — 두께 ±1.4 %·SE/solid ±0.5 %p 로 고정하고
**P:S 조성만** 다른 대조군 침대.  같은 φ 에서 σ 가 P:S 순서대로 완벽 단조
(우연 확률 ~7e-5) → 조성 효과의 실재를 확정했고, 그 차이가 d_h 로 접힌다.

## 핵심 사실
- 보존: V100 반납 대비 `docs/data/kit_ps_scaffolds/` (flat·gz) — 킷 배치 복원은
  `scripts/unpack_kit_scaffolds.py`, 곡선 재적합은 `fit_dh_collapse.py` 로 바이트 재현.
- metrics JSON 정본: `docs/data/se_curve_metrics/` (xfer_*.json — n_grid·mach·ε 별).
- 재하율 함정: 이 침대들(~114 µm)은 기하 규칙에서 V/c_P≈0.43 —
  [[quasistatic-platen-gate]] 없이는 σ 비교 불가.  배치는 `run_se_curve_batch.sh`
  (`--mach 0.03` 통일 · `--skip-existing` · 실행 이력 헤더).
- 384 불가 (VRAM 35 GB > 32), 288 이 V100 상한.  두께 100 µm 급 공통.
- d_h 색인·φ 선택 규칙: [[dh-collapse]] · 진행 중 8런: [[dh-288-protocol-equalization]].

## 관련 페이지·경로
- 킷 실행: [[kit-run-protocol]] · 정본 판정문: docs/se_curve_transfer_verdict_20260806.md
