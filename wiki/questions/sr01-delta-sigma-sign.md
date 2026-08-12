---
title: RQ — 점-스탬프 아티팩트는 σ_e 를 어느 방향으로 얼마나 움직이나 (해결 ×35.8)
created: 2026-08-11
updated: 2026-08-12
type: research-question
tags: [transport, additive, review]
sources: [docs/session_20260811_progress.md, docs/reviews/findings.json, scripts/sr01_stamp_ab.sh, scripts/sr01_stamp_compare.py]
confidence: medium
explored: false
verificationStatus: unverified
author: agent
claimType: empirical
evidenceScope: single-source
anchored: anchored
scope: relative-only
status: answered
feedsInto: SR-01 종결 + 첨가제 headline 비교 재개 (grade/P3 blocker 해제)
---

# RQ — Δσ_e 의 부호와 크기 — **답: 점 스탬프가 ×35.8 과소평가**

> [!question] 같은 압밀 베드에서 STEP3 래스터만 점→선분으로 바꾸면 σ_e 가 어느 방향으로 얼마나 움직이는가?

## 답 (2026-08-12 실측, kit_ps_7_3, GPU, 60 °C)

| | arm A (점) | arm B (선분) | Δ |
|---|---|---|---|
| **σ_e_eff** | 0.005122 | **0.1833** S/cm | **×35.79 (+3,479 %)** |
| 소산 share **VGCF** | **4 %** | **95 %** | 탄소 백본 부활 |
| share AM_S / AM_P | 39 / 57 % | 3 / 3 % | AM 우회가 사라짐 |
| σ_ion_eff | 0.001982 | 0.001835 | **−7.4 %** |
| κ_eff | 1.963 | 2.01 W/m·K | **+2.4 %** |
| n_dof 전자 / 이온 | 2,713,168 / 1,597,970 | 2,786,279 / 1,553,369 | +2.7 % / −2.8 % |

⇒ **H1(과소평가) 확정**, H2·H3 기각.  크기는 세 가설 어느 것이 예상한 것보다도 크다.

## 기전 — share 가 직접 말한다
점 스탬프에서 탄소는 전류의 **4 %** 만 나르고 AM 이 96 % 를 진다.  선분으로 바꾸면
**탄소 95 %** 로 뒤집힌다.  즉 점 스탬프는 탄소망을 전도 백본에서 **사실상 지우고**
전류를 AM 골격으로 우회시켰다 ([[sr01-stamp-fragmentation]] 의 기하 단절이 그대로 전기로
번역된 것).  σ(VGCF) ~1e3 vs σ(AM) ~5e-3 S/cm 이므로 백본이 살아나면 두 자릿수 도약이
물리적으로 정합.  이온이 −7.4 % 인 것도 같은 그림이다 — 탄소가 두꺼워지며 SE 이온망
단면을 잠식한다(이온 dof −2.8 %).  κ +2.4 % 도 탄소가 열전도체라 정합.

## 폐기된 추론 (기록)
- 자체리뷰·Codex 가 각각 부호를 **추론**했다가 서로 반대 결론에 닿았다 → 재야 알았다.
- 2026-08-11 arm A 중간값의 "VGCF 4 % → 아티팩트 상한이 작다(H3)" 해석은 **틀렸다**.
  그때 단 단서("조각남이 탄소 몫을 억눌러 4 %로 보일 수도")가 사실이었다 — **4 % 자체가
  아티팩트의 크기**였다.  중간값을 신호로 읽을 때 그 값이 이미 결함의 산물일 수 있다.

## 신뢰 범위 (⚠ 넘겨 쓰지 말 것)
- **1 킷 1 베드**.  기하 단절률은 킷마다 20.6–75.8 % 로 다르므로 ×35.8 은 이 베드의 값이다.
  다른 킷의 배수는 재야 한다.
- 베드가 **rate-오염**(V/c_P 0.428, [[quasistatic-platen-gate]]) → **절대값 인용 금지**.
  두 팔이 같은 베드이므로 **비(Δ)만** 유효 = `scope: relative-only`.
- **60 °C** 런 (`sigma_ion ×4.785, Ea 0.41 eV, Ea-band ×2.93–5.87`).
- 어느 쪽이 "옳은가" 는 이 실험이 직접 말하지 않는다.  다만 선분 스탬프가 **6-face 연결을
  보존하는 기하학적으로 올바른 래스터화**이므로 점 스탬프 쪽이 오차다.

## 파급
탄소를 가진 모든 침대의 STEP3 **σ_e 절대값과 소산 share 가 점-스탬프 시절 전부 과소평가**
(이 베드 기준 ×35.8).  첨가제 headline 비교(P1 blocker)는 선분 스탬프로 재산출해야 한다.

## Status Log
- [2026-08-12] **resolved** — 두 팔 완주 (GPU, 각 ~21분).  ★ 덤: 같은 arm A 를 CPU 와 GPU 로
  각각 돌아 **backend 무해성이 측정됐다** — σ_e·σ_ion·κ 가 인쇄 자릿수까지 동일
  (0.005122 / 0.001982 / 1.963), `CPU fallback` 0 건, 가속 11.2×·23.9×.  지금까지 "같은 행렬·
  같은 rtol 이니 같아야 한다"는 **가정**이던 것이 측정이 됐다.
- [2026-08-11] active — arm A 전자 채널 CPU 실측 (σ_e_eff 0.005122, 3,485 s).  ⚠ 그 payload 는
  터미널 끊김으로 **step3 블록 없는 불완전본**이었음이 뒤에 `--check-arm` 으로 드러났다.
- [2026-08-11] active — A/B 하네스 완성 (`sr01_stamp_ab.sh`, 두 팔 직접 실행·manifest 도장 검증).
