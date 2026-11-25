---
title: 회신 Z-3 — 폴라론 S0 내부 적대적 리뷰 3차 (NO-GO · P0 1 · P1 7)
date: 2026-09-03
updated: 2026-09-03
tags: [review, internal, sdcp, polaron, orca, reply]
status: 회신반영
kind: review-reply
system: sdcp
confidence: high
verificationStatus: verified
verifiedAt: 2026-09-03
verifiedBy: "내부 리뷰 원문 (scratch mutation 14건 · heredoc 실물 실행 · P0 이행 커밋 4a583441)"
campaign: sdcp_polaron_S0
reviewer: 내부 (별도 컨텍스트 서브에이전트 · 파일 무수정 · scratch 사본)
target: 커밋 341e0d7e (회신 Z-2 이행) + 91bd867f (사전등록 재발행)
verdict: NO-GO — 재비준 금지(현 판) · smoke 가 실행되면 반드시 죽어 증서가 영원히 안 나옴
---

> ⚠ **이 회신의 P0 는 캠페인을 완전히 멈추는 종류였다.** 회신 Z-2 의 P0 2건은 코드로 닫혔는데,
> 그 P0-2 를 이행하며 넣은 loccheck smoke 가 `%plots` 를 `%`-포맷 문자열에 그대로 넣어
> **실행되면 100 % ValueError** 로 죽었다. selftest 337건이 전부 통과했는데도 그랬다 —
> 러너의 python heredoc 을 **어느 시험도 실행하지 않았기** 때문이다.
> Claude 가 직접 재현해 확인했다: `ValueError: unsupported format character 'p' at index 42`.
> 아래는 원문 그대로다.

---

NO-GO — 현 판(341e0d7e + 91bd867f) 재비준 금지 · 실행 허용 범위 없음. 회신 Z-2 의 P0 2건은 코드로는 닫혔고(mutation 9개 전부 표지 시험 ✗ 로 뒤집힘) 봉인도 맞는데, **P0-2 의 smoke 가 실행되면 반드시 죽는다** — loccheck 증서가 이 빌더로는 영원히 안 나온다. 한 글자 고치면 빌더 SHA 가 바뀌므로 재봉인 → 재비준이 한 번 더 필요하다. 그 뒤에도 **loccheck 단독**만 GO (사람이 `plots_smoke.grid_check` 를 읽은 뒤 L·L2 는 다음 판정). seeds·probe·S·analyze·restart 금지.

## P0

1. **loccheck smoke 의 PYG heredoc 이 `%plots` 를 `%`-포맷 문자열 안에 그대로 넣어 항상 ValueError 로 죽는다 → 증서 발급 불가 → 캠페인이 한 발도 못 나간다.**
   `build_v7c_trimer.py:8713` — production `_pil_inp` 는 `%%plots`(4730)인데 smoke 는 `%plots` 라 `%p` 가 포맷 지시자로 해석된다. PIL_RUNNER 는 r-string 이고 heredoc 은 `<<'PYG'` 라 bash 도 안 건드린다 — 실행 시점에 그대로 터진다.
   재현(scratch, ORCA 없이): `ValueError: unsupported format character 'p' (0x70) at index 42`. `w3_grid.json` 은 써지고 `w3.inp` 는 **빈 파일**. 러너에서는 `|| fail=1` → w3 ORCA 스킵 → 증서 삭제 + "⛔ %loc 계약이 실물과 다릅니다" — **거짓 진단 메시지**를 달고 fail-closed.
   왜 selftest 337/0 이 못 잡았나: 러너의 python heredoc(PYLC·PYG·PYU·PYLG·PYCERT)은 **어느 시험도 실행하지 않는다** — 문자열 존재만 본다. `compile()` 로도 못 잡는 런타임 오류다. 실물 loccheck 는 아직 0회 — 이 heredoc 들은 한 번도 돈 적이 없다.
   고치는 법: 8713 `%plots` → `%%plots` (한 글자). **그리고** selftest 에 "heredoc 실행" 시험을 단다: PYG/PYU 를 추출해 합성 cube 로 돌린다 — 점-규약 → `bohr` · 구간-규약 → `GRIDFAIL:bohr` · Å-판독 → `GRIDFAIL:angstrom` · cell-centered → `GRIDFAIL:unknown`.

## P1

- **strict 계열 class 대조는 시험되지 않는다.** 합성 다이머엔 ether_O 가 없어 strict ≡ extended 이고, 실물 D 프레임은 strict ≠ extended 인 쪽이다 — e2e 가 도는 분기와 실물이 도는 분기가 다르다.
- **smoke 격자 대조가 `pil_run_calib` 와 "같은 대조" 가 아니다** — origin 허용차 smoke 1e-2 bohr vs production 1e-3. 규약이 두 곳에 **복사**돼 있다(CLAUDE.md 규약 복사 금지).
- **Å 경로가 죽은 코드다.** PYU 는 `unit == "bohr"` 만 통과시키는데 `pil_read_loccheck` 는 `"angstrom"` 도 받고 seeds 가 그 단위로 `%plots` 를 쓴다. 도달 불가능하다 — Å 지원을 지우거나 완성하거나 둘 중 하나.
- **THRESHOLD_DEPENDENT 는 Hirshfeld 만 본다.** calibration 이 지지하는 것은 **봉인 문턱에서의 class** 뿐이다 — `못 하는 것` 에 한 줄 적을 것.
- **`_pil_require_builder` 신규 2곳에 음성 시험이 없다** — `pil_write_receipt`·`pil_preflight` 을 지워도 0 ✗.
- **receipt builder 시험은 동어반복이다.** `_pil_require_builder` 가 둘의 동일을 강제하므로 `== _sha(__file__)` 는 항상 참.
- **게이트된 잡에 class 문자열이 또 남는다** — `estimand_form_calibration.family_class_{extended,strict}`(`_fail` **앞에** 기록).
- 사전등록 문구: `도구` "selftest 32건 (음성 ≥ 18)" — 실측 ⛔음성 **17건**. `ratification` 은 옛 digest 를 단 채 `state: ratified` + `status: proposed` — 재비준 시 digest 재계산 필수.

## 확인한 것

- 봉인: builder `b92ff52b…` · calib `02d9cb38…` = 사전등록 `0_시각_증거`; working tree clean. `pil_calib_gate_matches(prereg.calib_gate)` = (True, []).
- selftest: 빌더 337 ✓/0 ✗ · calib 32/32 · Z-2 표지 12건 전부 ✓.
- **지금 상태(재현)**: 실물 사전등록 + 합성 manifest 로 `_pil_check_prereg(pre_seed=True)` → SystemExit, 위반 2건: "status 가 'proposed'" · "비준 이후에 바뀌었다". **지금은 생성도 loccheck 도 안 된다.** 현 판을 그대로 재비준하면 생성만 열리고 loccheck 는 P0-1 로 반드시 실패한다 — 현 판 재비준은 무의미하다.
- 회신 Z-2 P0-1 반례 직접 실행: Hir {0.62,0.36,0.02}=BACKBONE · Becke {0.525,0.455,0.02}=MIXED_UNRESOLVED → `CALIB_FAMILY_CLASS_DIFFERS` ✓.
- **smoke heredoc 실측**(PYG 를 `%%plots` 로 고친 사본): 점-규약 → `bohr` · production ok · ∫Δρ=1.0000; 구간-규약 → `GRIDFAIL:bohr`; Å-판독 → `GRIDFAIL:angstrom`; cell-centered → `GRIDFAIL:unknown`; origin +5e-3 bohr → smoke ok / **production 실패**(P1 둘째). PYCERT(가짜 ORCA) → 증서 → `pil_read_loccheck` 수락 확인.
- Mutation(scratch 14개): MA class 동일 제거 → ✗; MB grid_verified 미요구 → ✗; MC INTERNAL_INCONSISTENT → ✗; MD/ME RECEIPT_MISSING/STALE → ✗; MF strict 게이트 → ✗; MG 여분 키 → ✗; MH nested candidate → ✗; ML rm 줄 → ✗. **0 ✗**: MI(receipt builder=manifest) · MK1/MK2(require_builder 제거) · MM(seeds 비원자) · MN(strict 계열 class 대조 제거).
