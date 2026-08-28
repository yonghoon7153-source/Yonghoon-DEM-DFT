---
title: "회신 R3 — Stage 0 재차 NO-GO: 실측 fail-open 5건 + 관측량 회수 계약 (GO 요건 9)"
date: 2026-08-28
updated: 2026-08-28
tags: [review, codex, sdcp, reopen, stage0, builder, verdict]
status: 접수 — 구현 완료 (R4 제출 대기)
confidence: high
verificationStatus: verified
verifiedAt: 2026-08-28
verifiedBy: codex
explored: false
authoredBy: human
effort: max
claimType: prescriptive
evidenceScope: multi-source-primary
---

# 회신 R3 (2026-08-28) — 요지 보존

> 검토 고정점 25e600c6 (리뷰어가 재차 **직접 실행**). 판정: **NO-GO** —
> "27 PASS 는 실패 경로를 덮지 못한다." 구현: 같은 날 재작성 (selftest 40건).

## 실행 전 P0 (전부 실측 재현)

0. **관측량 회수 계약**: 입력에 HIRSHFELD·UNO/UCO 요청이 없다 — Löwdin–Hirshfeld 강건성·
   UNO 지표·localization class 를 실행 후 복구할 보장이 없다. P1 분석기 문제가 아니라
   **실행 전 데이터 계약**이다.
1. **seed 미강제**: --seeds 1 이 성공(manifest 는 바닥 8 선언) · 음수 seed 허용 ·
   DP3 8개 요청에 고유 4개 · 적격 후보 없으면 cands[:1] 폴백으로 dmin 1.417 Å 도 성공.
2. **미이완 부모 수용**: xyz 주석의 "ORCA" 문자열 검사뿐 — stage A 조립본을 그대로 넣어도
   56잡 생성, gseed 999 재라벨도 통과. **자유문구는 증거가 아니다.**
3. **SP→Opt gate 가 문장**: dependency 없음. (pattern,sector) 만 쓰고 seed 구분 없음.
4. **analyzer 광범위 fail-open**: all-PENDING=성공(exit 0) · 종료문구만으로 OK ·
   동일 가짜 OUT 복사에 서로 다른 realized ID · 대문자 UNSTABLE 놓침 · stability 수행
   양성증거 미요구 · BS 미플립 <S²>=2.0 OK · Opt 수렴 미검사 · 첫 값 사용 ·
   입출력 해시 미결속 · errors="ignore".
5. **hybrid 미배선**: selector 호출 없음 · 입력 생성 없음 · class 미산출 · **핵·전자수가
   다른 종(h1/h2)의 절대에너지를 같은 0.10 eV 창에서 비교(물리적 무의미)** ·
   "MORead 금지" 주석은 강제 아님 — ORCA AutoStart 는 **NoAutoStart** 로만 꺼진다.

## 프로파일 P0 승격 (전부 유예 반대)
실행 전 고정: 관측량 수식·부호·정규화·UNRESOLVED 규칙 · 중성→doped remap validator ·
Hirshfeld/UNO/UCO/최종기하 회수 계약 · BS 붕괴 판정 최소 게이트 · **localization class
사전 규칙** (결과 본 뒤 경계 정하면 사후 선택). 시각화·정교한 classifier 만 후속 유예.

## 미이완 stage B 시연 = 증거 아님 — "파일 생성기 wiring test", 오히려 우회로 실증.

## GO 재심사 요건 9
① 검증된 stage A neutral Opt receipt ② parent/gseed 결속 stage B manifest
③ underseed·dmin·부모 불일치 음성 e2e ④ all-PENDING·복제 OUT 거부 e2e
⑤ stability 부재·대문자 unstable·미플립 BS·미수렴 Opt 거부 e2e
⑥ calculation-ID 기반 SP→Opt dependency 시험 ⑦ Hirshfeld/UNO/UCO 실제 입력
⑧ 조성별 hybrid selector + NoAutoStart ⑨ U_PCET 4-leg cycle 의 ID 일치 검사

## P1: stage A calc_id/해시/commit 부재 · 중첩 realized 통과 · 레거시 암묵 실행 ·
NA_SPIN_MODEL/METHOD_DEPENDENT emit 경로 부재. P2: CP949 콘솔 ✓ 인코딩.

## 구현 (같은 날) — 요건 9 를 selftest 40건으로 봉인
receipt 3중 결속(manifest+out+xyz, 좌표 대조·미이완/재라벨 거부) · seed 바닥/고유성/
dmin 강제(폴백 제거) · depends_on=선행 sp calc_id + DEPENDENCY_NOT_MET ·
analyzer 재작성(마지막 segment·마지막 값·양성증거·DUPLICATE_OUTPUT·OPT_UNCONVERGED·
STABILITY_UNVERIFIED·strict decode·PENDING 비영) · Hirshfeld/UNO UCO 입력 계약 ·
localization class 사전 규칙(share≥0.5 유일, MIXED_UNRESOLVED/NO_SPIN) + remap validator ·
hybrid 조성별 그룹 + NoAutoStart + --hybrid 생성기 · --compare 가 METHOD_DEPENDENT emit ·
U_PCET cycle 레코드(4-leg calc_id, A,F 제외) · 중첩 realized 거부 · --legacy 명시.
