---
title: E_SE 유효연화 (bulk 24 → eff 1.35/1.53 GPa) — 왜 불가피한가
created: 2026-08-11
updated: 2026-08-11
type: concept
tags: [calibration, dem, mpm]
sources: [CLAUDE.md, docs/esse_calibration_2mAh_real_9.md, docs/mpm_dpc_cap_crosscheck.md, docs/mpm3d_calibration.md]
confidence: high
explored: false
verificationStatus: unverified
author: agent
claimType: empirical
evidenceScope: multi-source-primary
anchored: anchored
scope: n-a
---

# E_SE 유효연화 — 18×(≈15.8×)

## 정의
강체구 DEM 도 단상 연속체 MPM 도 입상 재배열·GB 슬라이딩·미세파괴를 표현하지
못하므로, 그 결손 기전을 **유효 탄성계수 연화**로 흡수한다:
E_SE bulk 24 GPa → DEM 1.35 / MPM 챔피언 1.53 GPa.

## 왜 불가피한가 (독립 확인 3회 + 되돌리기 실패 3회)
- **확인**: ① pure-SE Cronau overlap 11–12 % 재현 ② plastic-vs-rigid 비교
  ③ MPM 이 독립적으로 같은 연화를 요구 (E=24 는 33–38 % 과다공극으로 stuck).
- **되돌리기 실패**: real-E + cap / shear-jam / bulk-jam 전부 실험 Heckel 실패
  (docs/mpm_dpc_cap_crosscheck.md) — 연화는 양 수준(탄성·소성)에서 환원 불가.
- **단 bulk 축은 예외** (CORRECTION 1): 연화가 체적탄성률까지 깎으면 soft-bulk
  force-chain 아티팩트 → ν_SE=0.49 로 K=25.5 GPa ≈ DFT B₀ 26.23 복원.
  연화의 물리적 실체는 **전단 축**이다 (μ 15.8× 연화; "18×" 는 ν=0.30 가정 시절 수치).

## 이 리포에서의 위치
- 1.35 vs 1.5 는 물리적으로 동일 영역 — 1.35 FINAL (docs/esse_calibration_2mAh_real_9.md).
- 문헌 E 10–30 GPa 밴드 밖인 것은 결함이 아니라 3-층 구분 (실물성/유효/챔피언) —
  연화 = 재배열 프록시이지 물성 주장 아님.
- [[frame5-division-of-labor]] 의 근거이자 [[frame4-independent-calibration]] 의
  실증 사례 (양쪽이 **각자** 실험에서 같은 연화에 도달).
- 킷 러너에 구워지는 값: [[mpm-kit-pipeline]] (`--e-se 1.53 --nu-se 0.49`).
