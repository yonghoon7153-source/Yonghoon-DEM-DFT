---
title: "Codex 회신 접수 — VASP 번들 HOLD · v2 작업 목록"
tags: [review/codex, sdcp, vasp, dft+u]
date: 2026-08-11
status: HOLD 수용 — v2 구현 대기
회신 원문: 사용자 채널로 수신 (2026-08-11 저녁)
---

# 판정: 발송 HOLD — 수용한다

Codex 종합: "현재 번들은 relax-only pilot 로는 쓸 수 있지만 final DFT bundle 로는
발송 불가." 반박할 것이 없다 — 특히 ①③⑤는 우리 repo 의 **기존 정본 계보를 내가
안 쓴 것**이라 자업자득이다.

## 수용 항목 → v2 구현 지도

| # | Codex 지적 | v2 조치 | 출처 |
|---|---|---|---|
| 1 | relax 마지막 에너지(LREAL=Auto·EDIFF 1e-5)를 최종값으로 씀 | **4상 러너**: pre-SCF → relax(2×3×1) → final static(3×4×1·LREAL=.FALSE.·EDIFF 1e-6·ISTART=0/ICHARG=1) → 민감도(4×6×1 대표쌍+clean) | Codex INCAR 템플릿 §2.2 |
| 2 | afm_balanced 가 정본 AFM 계보가 아님 | `vasp_stage.py ni_afm_signs()` 12-Ni 패턴 ×4 = qe_afm24_24_pm1 기본. magbias_net2 · contactNi 추가, afm_net4 는 exploratory 로 강등 | tools/sdcp/ptfe_linio2_uma/vasp_stage.py |
| 3 | 탐침 1쌍으로는 coverage 부족 + **독립 min 이 ΔE 를 오염** | tier1 전 끝점 2 seed (pose 32) · **seed-매칭 ΔE** · \|ΔE_s1−ΔE_s2\|≤10 meV · 실패 → BLOCKED_MAGNETIC_SENSITIVITY | §4.3 |
| 4 | 기체상 쌍극자/스핀 | IDIPOL=4+DIPOL(COM)·AMIN=0.01 · doped NUPDOWN=1 / closed 0 · 상자 span+20/+24 Å 2종(≤10 meV) | §3.2–3.3 |
| 5 | 최근접 하나로는 기하 감사 부족 | `geometry_audit()`/`magnetic_audit()` 재사용 — 결합 그래프 변화·PAIR_COLLAPSED·탈착·drift·Ni 모멘트·LDAU 점유 | §5.2–5.3 |
| 6 | k 2×2×1 근거 부족 | relax 2×3×1 · static 3×4×1 · 민감도 4×6×1(≤10 meV 게이트) | §7 |
| 7 | GGA=PE·ISYM=0·ADDGRID·DIPOL·AMIN 미명시 | 전 잡 명시 | §2.1 |
| 8 | 잡 수 오산 (요청문 58) | **pose 46 + refs 6 = 52** 로 정정 | §4.2 |
| 9 | 완결성/음성 selftest | planned matrix 하드 검증 · migration/bond-break/missing-seed 심은 음성 테스트 | §8 |

## 유지 확정 (Codex 동의)
IVDW=11 · U(Ni)=6.2 Dudarev · 중성 complex(NELECT 미지정) · NUPDOWN 미지정(슬랩 complex)
· δ=30 meV = practical indifference floor + 수치 게이트(seed/k/box 각 ≤10 meV).

## 발송 재개 조건 (Codex 체크리스트 그대로)
- [ ] Ni_pv + canonical AFM seed 계보 복구
- [ ] tier1 전 끝점 2 magnetic seeds
- [ ] 2×3×1 relax + 3×4×1 final static
- [ ] gas IDIPOL=4 · radical spin · 20/24 Å box gate
- [ ] final geometry/bond/registry/reconstruction/magnetic audits
- [ ] planned matrix 완결성 하드 게이트
- [ ] phase runner/restart/반송 아카이브
- [ ] full SHA-256/POTCAR/VASP provenance
- [ ] negative-path selftest 통과
- [ ] analyzer nonzero exit on required-data failure
