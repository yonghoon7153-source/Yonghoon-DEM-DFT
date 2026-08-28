---
title: "회신 R2 — Stage 0 재차 NO-GO: 빌더 실물이 카드와 불일치 (P0 6건 + 최소수정 8)"
date: 2026-08-28
updated: 2026-08-28
tags: [review, codex, sdcp, reopen, stage0, builder, verdict]
status: 접수 — 구현 완료 (R3 제출 대기)
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

# 회신 R2 (2026-08-28) — 원문 요지 보존

> 요청: `kb/reviews/codex_R2_prompt_doped_reopen_v3_2026_08_28.md` · 검토 고정점: 커밋 b3ff72de
> **판정: Stage 0 NO-GO.** 분자식·전자수·parity 는 맞지만 **실제 빌더 산출이 카드와 다르다.**
> 특기: 리뷰어가 커밋을 checkout 해 빌더를 **직접 실행**하고 산출 .inp/manifest 를 감사했다
> — "23 PASS 는 문자열 selftest 이지 e2e 증명이 아니다."
> 구현: 빌더 stage A/B 재작성 (같은 날, selftest 27건). R3 제출물에 실물 산출 첨부.

## 문서 밖 실행차단 P0 (전부 실측)

1. **모든 상태가 UKS Opt 로 생성** — neutral/RKS singlet/vertical SP 까지 전부
   `! UKS r2SCAN-3c Opt TightSCF`. manifest 의 RKS 와 모순.
2. **R⁰ = 최적화된 N3 − H 미구현** — 미이완 조립 기하에서 즉시 H 제거 후 곧바로 Opt.
   vertical/adiabatic 분리 없음. neutral-부모 dependency 없음.
3. **필수 batch fail-open** — `--n 6` 만 주면 neutral 하나로 성공, `--holes B,E` 만 줘도
   성공. 매트릭스 validator 부재.
4. **비정본 다이머 fail-open** — 조성이 달라도 검증 생략하고 계속. production 은
   fail-closed, 합성 selftest 만 명시적 플래그여야.
5. **중단코드·hybrid·stability 가 문자열** — emit 하는 analyzer 없음, stability/⟨S²⟩
   게이트 없음, hybrid 입력·선정기·fresh-start 검사 없음.
6. **manifest provenance 가 v3 가 아님** — schema v1 · estimand v2 · design_card v2.

## 조건 1–8 판정 (전부 불충분 — 요지)

1(P0) 비정본 fail-open + **"탈양성자화" 아님**: H 핵+전자 동시 제거 = neutral-H-deleted /
internal-redox microstate 로 명명. 2(P1) forbidden-word 검사로는 부족, localization_seed
"default" 는 seed 아님. 3(P0) **U_eff 는 핵 조성이 변해 순수 Hubbard U 아님** —
ΔE_disp / U_PCET(a,b) 로 개명, 순수 pairing 은 동일 h2 조성 안 sector 차로.
4(P1) 관측량 수식·정규화·class 경계·회수파일·index-remap validator 미정.
5(P0) 4단계 job type (neutral-parent SP → existence/stability → 상태별 Opt → 교차 SP).
6(P0) `--step` 은 seed 아님. CD/BE/AF 전부 centered — off-center 미탐지.
7(P0) 키워드는 유효하나 RKS/UKS·SP/Opt 오류 + hybrid 가 설명문. decision set 은
승자±0.10 eV 만이 아니라 **모든 결론 관련 realized topology 대표** 포함.
8(P0) microstate_id 가 realized 포함 가변 객체 — **calculation_id(불변) / realized_state_id
(사후) 분리.** conformer_cluster=torsion_scan_stepX 는 cluster 식별자 아님.

## Q2 — hA·hF 연기: **조건부 허용**
A,F 를 그 조성의 s/t/bs 비교에만 쓰고 U(AF)·short-medium-long 추세·DP6 부호 일반화를
주장하지 않으면 batch-2 가능. 대상이 최저상태/교차검사에 들면 자동 승격.
조립 conformer 에서 B≢E·C≢D 면 reflection 9 class 는 성립 안 함 — label pair 15개.
**off-center hBC 를 pilot 에 추가** (기존 singles 재사용, 값싸다).

## Q3 — h1 vertical: **N3 최적기하 − H 공통 부모로 통일.**
각 R⁰_k 마다 h0 / h1(a) / h1(b) / h2(a,b) 네 leg 를 같은 좌표 프레임으로.
vertical U 와 adiabatic U 는 별도 표, 혼합 금지.

## Q4 — seed 바닥 (operational floor):
DP3/DP4 = 초기 독립 torsion seed 4 + 연속 K=2 null batch 2 (최소 8) ·
DP6 = 초기 8 (maximin) + null batch 4 (최소 16). 변화 시 null counter 리셋.
전 섹터 동일 geometry seed set. geometry seed 와 SCF/localization seed 분리 관리.
--step 변경은 seed 로 안 센다.

## 재승인 최소 수정 8 → **구현 완료 (2026-08-28, 같은 날)**

| # | 요구 | 구현 |
|---|---|---|
| 1 | neutral Opt → H제거 vertical → SP/stability → 상태별 Opt 2단 빌드 | `--stage a` / `--stage b` (R⁰ = 부모−H, 무이완) + runner_rule |
| 2 | RKS/UKS·SP/Opt job type 명시 | `make_inp(job_type, wf)` — selftest 가 4종 .inp 원문 검사 |
| 3 | 필수 matrix·legs, 누락 시 생성 실패 | `REQUIRED_MATRIX` + U_PCET singles 대조 — SystemExit |
| 4 | 비정본/조성/패턴 fail-closed | 기본 거부, `--allow_noncanonical`·`--allow_partial` 은 시험 전용 명시 |
| 5 | abort code emit analyzer + 음성 e2e | `--analyze` (7코드) + 가짜 .out 음성 4종·양성 1종 selftest |
| 6 | 독립 seed + immutable calculation_id | geometry seed(LCG, DMIN_FLOOR 후보 중 선택) · SCF seed s0/s1(Hueckel) · `calculation_id`(conditioning 해시, realized 유입 시 발급 거부) |
| 7 | U_eff → ΔE_disp/U_PCET, 혼합 금지 | manifest `delta_definitions` (vert/ad 분리 + ⛔ 순수 U 아님 명시) |
| 8 | hybrid decision set 에 topology 대표 | `hybrid_select()` — class 별 최저 대표 전부 포함 (selftest) |

selftest 27건 PASS (음성 9종: 비정본 거부·부분 매트릭스 거부·realized 유입 거부·
analyzer 4종·닫힌꼴·parity). 실물 다이머 stage A e2e 포함.
