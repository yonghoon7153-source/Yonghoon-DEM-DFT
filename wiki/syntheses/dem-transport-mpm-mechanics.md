---
title: 논지 — "DEM=수송/패킹, MPM=형상/소성" 은 정정을 거쳐 더 강해졌다
created: 2026-08-11
updated: 2026-08-11
type: synthesis
tags: [epistemology, dem, mpm, transport]
sources: [CLAUDE.md, docs/mpm_dem_wallP_crossvalidation.md, docs/mpm_dpc_cap_crosscheck.md, docs/lit_varkey2026_multicontact_dem.md]
confidence: high
explored: false
verificationStatus: unverified
author: agent
claimType: interpretive
evidenceScope: synthesis-only
anchored: n-a
scope: n-a
targetVenue: 방법론 논문 discussion / 학위 defense
---

# 논지 — DEM/MPM 분업은 경험적 사실이다

## Thesis
DEM 과 MPM 은 각각 현실의 **다른 절반**(이산 패킹 vs 소성 유동)을 기술하며, 이
분업은 가정이 아니라 재질 스윕·격자 수렴·문헌 대조로 확정된 경험적 결과다.

## Argument
- 소성 MPM 은 어떤 보정에서도 Furnas dip 의 모양+절대값을 동시에 못 낸다
  (재질 스윕 증명) — dip 은 강체구 패킹 기하 = DEM 소유.
- 연속체는 실험 Heckel 을 못 낸다 (cap/shear-jam/bulk-jam 삼중 기각) — 압밀
  Heckel 은 접촉망 현상.
- 역방향: 강체구 DEM 은 형상변화·void-fill·변형률 장이 원리적으로 없다.  2026
  최신 다접촉 DEM(Varkey)도 구 형상·~20 % porosity 한계를 자인 — 분업이 우리
  목발이 아니라는 독립 방증.
- 접점에서는 일치한다: scaffold 결합에서 porosity·두께·coverage 가 독립 보정으로
  ~1 %p 일치 ([[frame4-independent-calibration]]).

## Counter-arguments (보존 — 논지가 정정으로 강해진 기록)
- **"DEM = TRANSPORT" (2026-06 옛 서술)** — 2026-08-11 사용자 지적으로 **과단순**
  판정: STEP3 복셀 FV 가 MPM 상 격자에서 σ 삼중항을 낸다.  정정 후 논지는
  "DEM 고유 = **접촉망 방식** σ" 로 좁아졌고, 두 솔버는 독립 이중 측정이 됐다
  ([[network-vs-voxel-sigma]]) — 반례가 논지를 죽이지 않고 정밀하게 만들었다.
- **"MPM porosity 전구간 신뢰" 반론** — regime map 이 기각: mono-large+thin 은
  MPM 과압축, SE-rich 는 DEM 과압축 (105 케이스 중 76 % 만 상호 검증).  분업은
  porosity 축에서도 **영역-조건부**다.

## Gap
- Heckel 실험 다압력 직접 검증 (LPSCl 분말 문헌 데이터로 닫을 수 있는 잔여 고리).
- 분업 지도의 정본 표는 [[frame5-division-of-labor]] — 이 페이지는 논지 방어만.
