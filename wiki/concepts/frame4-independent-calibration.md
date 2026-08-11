---
title: frame[4] — DEM↔MPM 상호 보정 금지 (독립 보정 인식론)
created: 2026-08-11
updated: 2026-08-11
type: concept
tags: [epistemology, calibration, dem, mpm]
sources: [CLAUDE.md, docs/mpm3d_calibration.md, docs/mpm_dem_wallP_crossvalidation.md]
confidence: high
explored: false
verificationStatus: unverified
author: agent
claimType: prescriptive
evidenceScope: multi-source-primary
anchored: n-a
scope: n-a
---

# frame[4] — DEM↔MPM 상호 보정 금지

## 정의
DEM 과 MPM 은 각각 **실험에만** 독립적으로 보정한다.  한쪽을 다른 쪽에 맞추는 것
(예: MPM σ_y 를 DEM Heckel σ_y_eff 에 튜닝)은 **순환**이라 금지.

## 왜 중요한가
- 결과가 **수렴**하면 = 교차검증 증거.  **발산**하면 = 정량화된 모델 한계
  (DEM 탄성연화 한계 or MPM 연속체근사 한계) — 둘 다 출판 가능한 정보이지 실패가 아니다.
- 실전 사례: real_14 scaffold 에서 porosity 16.7↔15.6 %·두께·coverage 가 독립 보정
  상태로 일치 (docs/mpm3d_calibration.md) — 서로 맞춘 적이 없기에 이 일치가 증거가 된다.
- 512 격자수렴으로 1.2 %p 잔차가 **수렴된 구성모델 차이**임을 확인 = 모델 신뢰폭.

## 이 리포에서의 위치
- 보정 앵커는 공유하되 (Minnmann pure-SE 10 % @300 MPa) 서로의 출력은 앵커가 아니다.
- [[frame5-division-of-labor]] 와 쌍 — 분업은 frame[5], 보정 독립은 frame[4].
- 같은 원리가 σ 이중화에도 적용: [[network-vs-voxel-sigma]] 의 두 솔버는 서로의
  근사가 아니라 **다른 이산화의 독립 측정**이다.
- 위키 규범으로서: 페이지끼리 충돌하면 한쪽을 다른 쪽에 맞추지 말고 양쪽 기록
  (SCHEMA Update Policy 와 동형).
