---
title: 회신 Z-2 — 폴라론 S0 내부 적대적 리뷰 2차 (NO-GO · P0 2 · P1 9)
date: 2026-09-03
campaign: sdcp_polaron_S0
reviewer: 내부 (별도 컨텍스트 서브에이전트 · 파일 무수정 · scratch 사본 mutation 17개)
target: 커밋 52b0edcd (회신 Z 이행) + 6d61104f (사전등록 재발행)
verdict: NO-GO — 재비준 금지(현 판) · 실행 허용 범위 없음
---

> 회신 Z 의 P0 4건은 **닫힌 것으로 확인**됐다(mutation 14개 전부 표지 시험이 ✗ 로 뒤집힘). 새 P0 는 둘:
> ① family 대조가 class 판정을 비교하지 않음 ② loccheck smoke 가 `%plots` 격자 규약(dim·origin)을
> 실측하지 않아 S 15잡 뒤 전건 CUBE_GRID_MISMATCH 가능. 아래는 원문 그대로다.

---

NO-GO — 현 판(52b0edcd + 6d61104f) 재비준 금지 · 실행 허용 범위 없음. 아래 P0 2건(새 것) 이행 → 재봉인 → 재비준 뒤에도 **loccheck 단독**만 GO(그 smoke 증서를 사람이 읽은 뒤 L·L2 는 다음 판정). seeds·probe·S·analyze·restart 금지.

회신 Z 의 P0 4건은 **실제로 닫혔다** — 봉인 일치, selftest 325/0 · 32/0, scratch 사본에서 새 가드 14개를 하나씩 지우면 각각의 Z 표지 시험이 ✗ 로 뒤집힌다(아래 확인 절). 그런데도 NO-GO 인 이유는 둘이다: ① Becke↔Hirshfeld family 대조가 **class 판정(margin)**을 비교하지 않아 calibration 이 지지하지 않는 class 가 나올 수 있고, ② loccheck smoke 가 `%plots` 의 **dim 규약**을 실측하지 않아 S 15잡을 다 태운 뒤 전건 CUBE_GRID_MISMATCH → class 0 이 될 수 있다(회신 Z P0-1 과 같은 유형의 "fail-closed 이지만 6시간 뒤").

## P0

1. **family 대조가 |ΔF| 만 보고 class 판정을 안 본다 — Hirshfeld 가 BACKBONE 인데 Becke 계열에선 MIXED_UNRESOLVED 인 잡이 게이트 없이 class 를 받는다.**
   `pil_calib_gate_for_job` 은 `max_g|F_out^Becke − F^Hir| ≤ PIL_CALIB_FAMILY_TOL(0.10)` 만 요구한다. 네 조건 ⓐ–ⓓ는 **Becke F_in vs Becke F_out** 사이에서만 평가되고, 보고되는 class 는 **Hirshfeld** 로 매긴다. 같은 repo 의 Löwdin↔Hirshfeld 대조 `pilot_partition_check` 는 `|ΔF_bb| ≤ 0.10` **그리고 class 동일**을 요구하는데, 새 family 대조만 class 동일 조건이 빠졌다.
   반례(실제 함수로 확인): Hirshfeld {bb 0.62, so3 0.36, other 0.02} → `pilot_class` = BACKBONE, 0.4/0.5/0.6 모두 같아 THRESHOLD_DEPENDENT 아님. Becke F_out = F_in = {0.525, 0.455, 0.02} → `direct_comparison_gate` = CALIB_AGREES(둘 다 margin 0.07 < 0.10 으로 **일치**), family max|ΔF| = 0.095 ≤ 0.10 → 게이트 없음. 그런데 이 Becke 벡터에 `pilot_class` 를 걸면 MIXED_UNRESOLVED(margin 0.07)다. 즉 calibration 이 "절댓값 위치가 class 를 바꾸지 않는다" 를 보증한 그 계열에서는 **class 자체가 없다**. Löwdin {0.60, 0.38, 0.02} 면 PARTITION_DEPENDENT 도 안 걸린다.
   고치는 법(한 줄): `pilot_class(hir_F)[0] == pilot_class(F_out_becke)[0]` 를 extended·strict 에 요구(불일치 → `CALIB_FAMILY_CLASS_DIFFERS`), 또는 ⓐ–ⓒ 를 Hirshfeld F ↔ Becke F_out 사이에도 적용.

2. **smoke 가 `%plots` 의 격자 규약(dim = 점 수 vs 구간 수 · origin = min)을 실측하지 않는다 → S 단계에서 전건 CUBE_GRID_MISMATCH 가능.**
   `pil_cube_grid` 는 `dims = ceil(L/0.30)+1`, `spacing = L/(dims−1)` 을 봉인하고, `pil_run_calib` 은 cube 헤더의 n·origin·간격을 **1e-3** 로 대조해 다르면 SystemExit(→ CALIB_MISSING → class 없음). 그런데 loccheck 의 OH• smoke 는 origin 으로 **단위**만 판정하고, 간격 규약은 보지 않는다. ORCA 가 `dim` 을 구간 수로 읽어 spacing = (max−min)/dim 을 쓰면: smoke 는 16/40 = 0.4000 bohr(0.2117 Å) — 0.35 Å 아래라 **QC 통과**, origin −8.0 그대로라 **단위 판정 통과**, 증서 발급. 그 뒤 200원자 잡(extent 18.8/23.8/14.6 Å + 여백 10 Å → dims 97/114/84)에서 봉인 0.3000/0.2991/0.2964 Å vs 실물 0.2969/0.2965/0.2929 Å, Δ = 0.0031/0.0026/0.0035 > 1e-3 → **15잡 전부** 대조 생성 실패. 증서에는 `grid_n`·`grid_spacing_max_A` 가 **기록**되지만 아무도 읽지 않는다.
   고치는 법: smoke 상자를 `pil_cube_grid(OH 좌표)` 로 만들고 `pil_run_calib` 와 **같은** n·origin·간격 대조를 smoke cube 에 걸어 통과해야 증서를 쓴다(convention 을 `plots_smoke` 에 봉인, `pil_read_loccheck` 가 요구). `_pil_fake_real_cube` 는 `pil_cube_grid` 값으로 cube 를 쓰므로 selftest 는 이 불일치를 원리적으로 못 본다 — 실물 smoke 만 잡는다.

## P1

- **새 결박 3건에 음성 시험이 없다** (scratch mutation 으로 확인 — 가드를 지워도 ✗ 0): ⓐ F 재계산 불일치 `CALIB_INTERNAL_INCONSISTENT` ⓑ calib receipt 행 소비 `CALIB_RECEIPT_MISSING/STALE` ⓒ strict 분할 불일치 `ESTIMAND_FORM_DISAGREES(strict)`. 사전등록 `결박 ③·⑤` 가 이 셋 위에 서 있는데 양성 시험(CALIB_AGREES)만 있다.
- **receipt 가 "그 실행의" cube 가 아니라 "그 자리에 있는" cube 를 봉인한다.** `run()` 은 ORCA 전에 `<tag>_spin.cube` 를 지우지 않고, `pil_write_receipt` 는 존재하는 파일을 해시한다. `.out` 만 지우고 재실행한 잡이 `%plots` 없이 정상종료하면 옛 cube 가 새 receipt 에 봉인된다. `rm -f "$j/$tag"_spin.cube` 한 줄.
- `_pil_require_builder` 가 없는 진입점: `--polaron_preflight`(`pil_preflight`)·`--polaron_receipt`(`pil_write_receipt`). receipt 는 `builder_sha256` 에 **manifest 값**을 적어 실제 실행 빌더가 아니다 — `_sha(__file__)` 로.
- 러너 `_PSU` 판정: heredoc 파이썬이 죽으면 `_PSU=""` 이고 `[ "" != "unknown" ]` 이 참이라 "✔ 단위 실측: " 을 찍는다. 증서는 판독기가 거부하니 fail-closed 지만 화면이 거짓이다 — `case "$_PSU" in bohr|angstrom) ;; *) fail=1;; esac`.
- 원자적 쓰기는 PYL2 만. `pilot_seeds`·`pilot_restart` 의 manifest `write_text` 는 그대로다.
- `class_candidate` 는 `class` 만 옮긴다. 게이트된 잡의 `hirshfeld_strict.class`·`partition.class_lowdin/class_hirshfeld` 는 인용 가능한 채 남는다.
- 사전등록 문구: `estimand_form_calibration.도구` "selftest 29건 (음성 ≥ 15)" → 지금 32건. `ratification` 은 옛 digest 를 단 채 `state: ratified` 이고 `status: proposed` — 게이트는 막지만 기록이 혼란스럽다. 재비준 시 digest 재계산 필수.
- `pil_calib_gate_matches` 는 코드 상수 7개만 본다 — 사전등록 `calib_gate` 에 코드에 없는 문턱이 들어가도 조용하다. 여분 키가 있으면 위반으로.
- 회신 Y Q1(plan-only) 미결 표기: **지금은 수용 가능.** 조건: `미결.plan_only_Q1` 을 지우지 말고, 환경 확장(규모 변경) 전에 다시 연다.

## 확인한 것

- 봉인: builder 87326fd5… · calib 02d9cb38… = 사전등록 `0_시각_증거`; last_change 52b0edcd; working tree clean(HEAD 6d61104f). `pil_calib_gate_constants()` = 사전등록 `calib_gate`.
- 지금 상태: 실물 사전등록 + 합성 manifest 로 `_pil_check_prereg` → "status 가 'proposed'" · "비준 이후에 바뀌었다" 로 SystemExit — **지금은 생성도 loccheck 도 안 열린다**.
- selftest: 빌더 325 ✓ / 0 ✗ · Z 표지 23건 · calib 32/32 · convention 0 위반.
- Mutation(scratch 사본 17개): M1 shortcut 제거 → Z P0-4 ✗; M2 `_cert_orca` 없을 때 pass → ✗; M3 CALIB_CUBE_NOT_FROM_RUN 제거 → ✗; M4 family 제거 → ✗; M5 사전등록 calib_tool 미읽음 → 2건 ✗; M6 calib_gate 미읽음 → 2건 ✗; M7 `_pil_require_builder` 무력화 → ✗; M8 plots_smoke 미요구 → ✗; M9 CUBE_GEOMETRY → ✗; M10 CUBE_GRID → ✗; M11 dV Å³ 복원 → calib 2건 + 빌더 2건 ✗; M12 class_candidate → ✗; M13 S 게이트 재계산 제거 → ✗; M14 receipt spin_cube_sha256=None → 13건 ✗. M15/M16/M17(P1 첫 항 셋) → **0건 ✗**.
- P0-1(단위)·P0-2(결박)·P0-3·P0-4 의 코드 경로를 줄 단위로 확인 — 같은 사용자 위조 밖에서 다른 실행의 cube 를 통과시키는 경로는 찾지 못했다. "없어서 검사가 꺼지는" 자리도 더 못 찾았다.
