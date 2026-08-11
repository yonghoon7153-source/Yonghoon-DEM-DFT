---
title: 준정적 플래튼 게이트 — V/c_P ≤ 0.01, 위반은 등급 B (상대비교 전용)
created: 2026-08-11
updated: 2026-08-11
type: concept
tags: [mpm, calibration, pipeline]
sources: [docs/mpm_platen_kinematic_stop_defect.md, scripts/mpm3d_compaction.py, scripts/patch_kit_quasistatic.py, docs/se_curve_transfer_verdict_20260806.md]
confidence: high
explored: false
verificationStatus: unverified
author: agent
claimType: empirical
evidenceScope: multi-source-primary
anchored: anchored
scope: n-a
---

# 준정적 플래튼 게이트

## 정의
MPM 압밀의 기하 규칙 `vmax = 0.008·(WALL0−FLOOR)` 은 플래튼 속도가 **베드 높이에
비례**하는 항등식 → 두꺼운 전극일수록 빨리 내려찍는다 (114 µm P:S 킷 실측
V/c_P ≈ 0.43, 전단파 기준 초음속).  판독 편향 + **베드 상태 자체의 rate-오염**
두 결함이 겹친다.  2026-08-11 부터 mpm3d 가 `V/c_P > 0.01` 이면 거부한다.

## 규칙 (실무)
- **`--platen-mach 0.01`** = 처방 (절대값용; 런타임 ~3–10×, 기존 코퍼스와 별도 트랙).
- **`--allow-fast-platen`** = 알고 진행 — 위반이 `mpm_metrics.json` 의
  `quasistatic_violation`/`platen_mach_VcP` 에 박혀 결과가 달고 다닌다.
  같은 마하로 통일한 **상대 비교는 공통모드 상쇄로 유효 = 등급 B** (`scope:
  relative-only`); 절대값 인용 금지.  실측 크기: 0.0306→0.01 에서 σ +4.8 %.
- 배포된 킷 러너 소급 배선: `scripts/patch_kit_quasistatic.py` (멱등) —
  git pull 은 scripts/ 만 당기고 run_mpm.sh 는 킷 안에 있어 갱신 안 되는 구멍.

## 왜 중요한가
- 크로스-베드 σ(φ) 비교가 통째로 교란된 실사고 (재하율 3.4× 차이가 베드 차이로
  오독될 뻔; d_h 판정 전체가 `--mach 0.03` 통일 후에야 성립 — [[dh-collapse]]).
- 정지도 결함: wallP 순간-판독 정지는 갭 산술이 정한 걸음수에서 멈춘다
  (docs/mpm_platen_kinematic_stop_defect.md §4) — 처방은 동결-프로브 + 감속 **둘 다**.

## 이 리포에서의 위치
- 킷 실행 절차와 env 노브(MPM_QUASISTATIC 등)는 [[kit-run-protocol]].
- SE 응답곡선·킷 대조군이 모두 이 게이트 아래 있다: [[se-curve-kits]].
