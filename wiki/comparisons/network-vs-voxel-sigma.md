---
title: σ 를 내는 솔버는 둘이다 — 접촉망(DEM) vs 복셀 FV(STEP3)
created: 2026-08-11
updated: 2026-08-11
type: comparison
tags: [transport, dem, mpm, pipeline]
sources: [CLAUDE.md, scripts/network_conductivity.py, scripts/voxel_conductivity.py, scripts/step3_sigma.py]
confidence: high
explored: false
verificationStatus: unverified
author: agent
claimType: definition
evidenceScope: multi-source-primary
anchored: n-a
scope: n-a
---

# 접촉망 σ vs 복셀 FV σ

## 비교 이유
2026-08-11 사용자 지적으로 정정된 자리: 옛 서술 "MPM 은 transport σ 를 못 낸다 /
DEM = TRANSPORT" 은 STEP3 도입 후 **과단순**이다.  못 내는 것은 **접촉망 방식의
σ** 이지 σ 자체가 아니다.  두 솔버의 관계를 정확히 못 박아야 다음 세션이 같은
오독을 반복하지 않는다.

## 비교표
| | 접촉망 (`network_conductivity.py`) | 복셀 FV (`voxel_conductivity.py` · `step3_sigma.py`) |
|---|---|---|
| 이산화 | DEM 구의 접촉망 — 접촉당 Holm 협착 R=1/(2σr_c) | MPM 상(phase) 격자 — 유한체적 ∇·(σ∇φ)=0, 면 조화평균 |
| 입력 | LIGGGHTS 덤프 | MPM phase grid (payload) |
| 채널 | ionic · electronic · thermal | ionic · electronic · thermal |
| 실행 위치 | **웹앱 파이프라인** | **킷** (run_mpm.sh → payload) |
| 고유 강점 | 접촉당 A(δ)·파괴 시 접촉 소실·Stage-E 소성면적 | 형상-충실 (소성 후 실제 상 분포 위에서 품) |
| 고유 약점 | 구 형상 고정 | 래스터 아티팩트 ([[sr01-stamp-fragmentation]]) |

## 결론
둘은 **다른 이산화의 독립 측정** — 한쪽이 다른 쪽의 근사가 아니다.  일치하면
frame[4] 교차검증, 갈라지면 정량화된 이산화 한계 ([[frame4-independent-calibration]]).
분업 지도에서의 자리는 [[frame5-division-of-labor]].

## 불확실성
- ⚠ 두 파이프라인은 **코드가 따로다** — 웹앱([[dem-webapp-pipeline]]) 쪽 수정이
  킷([[mpm-kit-pipeline]])의 STEP3 에 자동 적용되지 않는다 (2026-08-11 thermal
  무음-결손이 양쪽에 따로 있어 각각 고친 실사례).  한쪽을 고치면 반드시 다른
  쪽의 같은 자리를 확인할 것.
