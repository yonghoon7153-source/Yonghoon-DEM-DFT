---
title: frame[5] — DEM/MPM 분업 (무엇을 어느 모델이 내는가)
created: 2026-08-11
updated: 2026-08-11
type: concept
tags: [epistemology, dem, mpm, transport, pipeline]
sources: [CLAUDE.md, docs/mpm_dem_wallP_crossvalidation.md, docs/mpm3d_calibration.md, docs/mpm_dpc_cap_crosscheck.md]
confidence: high
explored: false
verificationStatus: unverified
author: agent
claimType: empirical
evidenceScope: multi-source-primary
anchored: n-a
scope: n-a
---

# frame[5] — DEM/MPM 분업

## 정의
두 모델은 상보적이고 **어느 쪽도 다른 쪽을 대체하지 못한다** — 재질 스윕으로
경험적으로 확정된 분업 (가정이 아님).

| | DEM 고유 | MPM 고유 | 둘 다 (교차검증) |
|---|---|---|---|
| 소관 | **접촉망** σ (Holm 협착·접촉당 A(δ)·Stage-E) · 퍼콜레이션 · 배위수 · force chain · 파괴(Auerbach) · AM 패킹 · **Furnas dip** | SE 소성 형상변화 · 체적보존 void-fill · 소성변형률/응력 장 · 채널 기하 | porosity · 두께 · Tabor coverage · 조성→porosity 트렌드 |

## 왜 중요한가
- **Furnas dip 은 DEM 전용** (CORRECTION 2): 챔피언→강체 재질 스윕 전 구간에서
  소성 연속체는 dip 모양+절대값을 동시에 못 낸다 — dip 은 강체구 초기 패킹 기하.
- cap/shear-jam/bulk-jam 삼중 확인: resolved-grain 연속체는 실험 Heckel 을 못 낸다
  (docs/mpm_dpc_cap_crosscheck.md) — 압밀 Heckel 은 접촉망 현상.
- ⇒ "porosity-incl-dip 은 DEM, morphology 는 MPM" 이 실무 라우팅 규칙.

## 이 리포에서의 위치
- ★ 정정 2026-08-11: 옛 한 줄 "DEM = TRANSPORT, MPM = MECHANICS" 는 STEP3 도입 후
  **과단순** — σ 를 내는 솔버는 둘이다.  상세는 [[network-vs-voxel-sigma]].
- 보정은 각자 실험으로만: [[frame4-independent-calibration]].
- 소성연화의 불가피성(양쪽 모두)은 [[ese-softening-18x]].
- 논지로서의 방어·반론 보존: [[dem-transport-mpm-mechanics]].
