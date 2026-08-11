---
title: DEM 웹앱 파이프라인 — LIGGGHTS + 접촉망 σ (Kirchhoff/Holm) + 대시보드
created: 2026-08-11
updated: 2026-08-11
type: entity
tags: [pipeline, dem, transport]
sources: [scripts/network_conductivity.py, scripts/run_network_full_corrections.py, webapp/pipeline_service.py, CLAUDE.md]
confidence: high
explored: false
verificationStatus: unverified
author: agent
claimType: definition
evidenceScope: multi-source-primary
anchored: n-a
scope: n-a
---

# DEM 웹앱 파이프라인

## 개요
LIGGGHTS 덤프 → 접촉 분석 → **접촉망 σ_ion/σ_e/κ** (Kirchhoff 노드법, Holm 협착
R=1/(2σr_c), 5-영역 접촉면적 cap, Stage-E Tabor 소성면적 보정) → 웹앱 대시보드
(스케일링법칙 3종 LOOCV .975/.953/.90, grade engine, 예측기).  코퍼스 ~132 케이스.

## 핵심 사실
- σ 폼 3종은 **동결** — 재적합·항 추가 금지 (CLAUDE.md 각 FINALIZED 절; φ_AM<0.3
  외삽 금지 가드 포함).
- 접촉망 σ 는 DEM 고유 (접촉당 A(δ)·파괴 시 접촉 소실·Stage-E 가 걸리는 자리) —
  [[frame5-division-of-labor]].  복셀 FV σ 와의 관계는 [[network-vs-voxel-sigma]].
- ⚠ **킷 파이프라인과 별개다** — 웹앱은 STEP3 를 부르지 않는다.  같은 결함이
  양쪽에 따로 있을 수 있다 (2026-08-11 thermal 무음-결손을 각각 고친 실사례).
- 환경 의존: `python3 scripts/trace_deps.py` 가 진입점별 전이 의존을 코드에서 유도
  (손-목록 드리프트 가드).

## 관련 페이지·경로
- 상대편 파이프라인: [[mpm-kit-pipeline]] · 데이터: `webapp/results/`, `docs/data/`
- 문헌 교차검증(같은 재료·같은 RNM): docs/lit_bazzoun2026_dem_fem_rnm.md
