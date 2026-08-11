---
title: MPM 킷 파이프라인 — scaffold 압밀 + payload + STEP3/4
created: 2026-08-11
updated: 2026-08-11
type: entity
tags: [pipeline, mpm, transport, electrochem]
sources: [scripts/mpm3d_compaction.py, scripts/mpm_webapp_payload.py, scripts/step3_sigma.py, scripts/step4_dyn.py, scripts/mpm_input_from_case.py]
confidence: high
explored: false
verificationStatus: unverified
author: agent
claimType: definition
evidenceScope: multi-source-primary
anchored: n-a
scope: n-a
---

# MPM 킷 파이프라인

## 개요
케이스 → `mpm_input_from_case.py` 가 킷 zip 생성 (`run_mpm.sh` 포함) → GPU 박스에서
① `mpm3d_compaction.py` (Taichi MLS-MPM, J2, DEM AM scaffold 동결 + 실 SE 위치,
`--e-se 1.53 --nu-se 0.49 --readout wallP`) ② `mpm_webapp_payload.py` (3D 메쉬 +
STEP3 복셀 σ + STEP4 그리드) → 웹앱에 업로드.

## 핵심 사실
- AM 동결 4근거: rigid 접촉망은 DEM 소관 / mobile-rigid 는 force-chain 과차폐 /
  CFL·OOM / DEM 골격이 이미 검증된 300 MPa 평형 ([[frame5-division-of-labor]]).
- 재하율: 기하 규칙은 베드 높이 비례 → [[quasistatic-platen-gate]] 필수 숙지.
  킷 기본 = `--allow-fast-platen` (등급 B) · `MPM_QUASISTATIC=1` 로 처방 팔.
- 첨가제(VGCF/PTFE/SuperP/SDCP/SWCNT)는 압밀에 시딩되고 STEP3 탄소 채널로 σ_e 에
  들어간다 — 점-스탬프 한계는 [[sr01-stamp-fragmentation]].
- v3 열화물리 opt-in: MPM_FRACTURE(취성 crack-void) · MPM_PERIODIC_SIGMA · Joule 맵 기본 ON.
- 유효연화 값의 근거는 [[ese-softening-18x]] — 킷에 구워진 1.53/0.49 를 바꾸지 말 것.

## 관련 페이지·경로
- 실행 절차·완료 판정·A/B: [[kit-run-protocol]] · 대조군 킷 5종: [[se-curve-kits]]
- 정본 문서: docs/mpm3d_calibration.md · docs/pipeline_step1_to_step5_guide.md
