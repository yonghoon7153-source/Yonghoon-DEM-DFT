---
title: SDCP 조각은 LiNiO₂(104)에서 Li 자리와 Ni 자리 중 어디에 붙는가
date: 2026-08-11
updated: 2026-08-11
tags: [sdcp, linio2, site-preference, uma, vasp-handoff, magnetism]
status: active
confidence: low
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: empirical
evidenceScope: multi-source-mixed
feedsInto: kb/reports/sdcp_preliminary_final_2026_08_03.md §6 재구축 + VASP 외주 결과 해석
---

## 질문

SDCP 술포네이트 조각(중성/도핑)이 LiNiO₂(104) 표면에서 **Li 자리와 Ni 자리 중
어디를 선호하는가** — 그리고 그 선호가 판정바닥 max(30 meV, 쌍 산포)를 넘는가?

## 왜 중요한가

계면 보호 서사("SDCP 가 양극 표면에 세게 붙는다")의 다음 단계가 **어디에 어떻게
붙는가**다. Ni 선호면 전이금속 자리 피복(전해질 산화 억제) 서사, Li 선호면 Li⁺ 수송
경로 간섭 서사로 갈라진다. 또한 이 답이 VASP 외주(§결정 실험)의 해석 틀을 정한다 —
외주 결과가 오면 이 카드의 어휘(ROBUST/MARGINAL/…)로 판정된다.

## 가설

선호가 있더라도 **얕다** (UMA 상 |ΔE| ≲ 판정바닥) — 얕은 선호는 MLIP 오차·자성
씨앗·고정 슬랩 산포에 다 묻히므로, 판정은 유한설계 분류로만 말한다.

## Evidence For

- (Ni 쪽 신호) doped·freeze 1.00 에서 자격쌍 5/5 의 ΔE(Ni−Li) 중앙값 **−0.131 eV**
  (db/properties/sdcp_ptfe_site_preference_uma_v1.json).
- Phase B 납품(runs/sdcp_phaseB_vasp_v1_2026_08_08)은 슬랩+조각 DFT 가 실제로
  돈다는 것과 자성 계보(afm2424 ±1 μB)를 고정해 줬다 — 방법의 실행 가능성 근거.

## Evidence Against

- 그 −0.131 eV 는 **쌍마다 부호가 뒤집혀** 바닥이 0.146 eV 로 부풀었고 판정은
  NOT_RESOLVED — 고정 슬랩이 만든 산포라는 주석이 데이터에 붙어 있다.
- freeze 0.85 에선 2/5 쌍이 **PAIR_MIGRATED**(Li시작→Ni · Ni시작→Li 맞교환)로
  실격 — 시작 자리를 유지 못 할 만큼 선호가 얕다는 독립 신호.
- 중성 조각은 ΔE −0.017 eV 로 바닥 0.03 미달 (freeze 두 조건 모두 NOT_RESOLVED).
- UMA 자체 오차가 수십 meV — 판정바닥 δ=30 meV 와 같은 자릿수라 MLIP 단독으로는
  원리적으로 결판 불가.
- DFT 쪽도 자성 씨앗(pm1 vs net4)이 ΔE 를 흔들 수 있음 — 씨앗쌍 불일치 >10 meV 면
  BLOCKED_MAGNETIC_SENSITIVITY 로 막는 게이트가 필요했던 이유.

## 결정 실험

**VASP 원샷 번들 v2** (tools/sdcp/vasp_handoff_bundle.py): 2상(이완→정적) × 씨앗 2종
seed-matched ΔE(≤10 meV 게이트) + probe 쌍 dense-k 검증 + fail-closed 분석기.
판정 어휘는 tools/sdcp/site_screen.py 의 유한설계 분류 — ROBUST_SCREENING /
MARGINAL_TENDENCY / SIGN_CONSISTENT_SMALL / UNRESOLVED_MIXED, n<3 은 즉시 NO_VERDICT.
현재 Codex GO/NO-GO 대기 (kb/reviews/vasp_bundle_v2_rereview_request_2026_08_11.md).

## Status Log

- 2026-08-03: LiNiO₂(104) 슬랩 깨짐 확정 → 계면 결합 전면 보류
  (kb/reports/sdcp_preliminary_final_2026_08_03.md §6.4).
- 2026-08-11: 재생성 슬랩에서 UMA v1 사이트 스크린 — 4판정 전부 NOT_RESOLVED
  (프로토콜: kb/methodology/site_preference_protocol_2026_08_11.md). VASP 번들 v1 →
  Codex HOLD (kb/reviews/vasp_bundle_codex_reply_2026_08_11.md) → v2 전면 재작성,
  재리뷰 요청 송부. 외주 생성은 GO 이후.
