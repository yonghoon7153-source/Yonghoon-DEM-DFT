---
title: "리뷰 사슬 색인 — 프롬프트↔회신 (자동 생성)"
date: 2026-09-01
updated: 2026-09-01
tags: [index, review, codex]
status: 자동생성
kind: index
confidence: high
verificationStatus: verified
verifiedAt: 2026-09-01
verifiedBy: tools/kb_wiki.py reviews --write (산출물에서 재구성)
explored: false
authoredBy: agent
effort: low
claimType: empirical
evidenceScope: multi-source-primary
---

# 리뷰 사슬 색인

> ⛔ **손으로 고치지 않는다.** `python3 tools/kb_wiki.py reviews --write` 로
> 재생성한다. 정본은 `kb/reviews/` 의 실물 파일이다.

회신 파일명의 라벨이 프롬프트와 **어긋나는 판이 섞여 있다**
(`AT_reply`←`AT_prompt` 이지만 `AV_reply`←`AU_prompt`).
그래서 짝은 파일명이 아니라 회신 본문의 `요청:` 역링크로 맺는다.

| 라벨 | 날짜 | 프롬프트 | 회신 | status | 근거 |
|---|---|---|---|---|---|
| O | 2026-08-28 | `codex_O_prompt_sdcp_doped_estimand_2026_08_28.md` | `codex_O_sdcp_doped_estimand_reply_2026_08_28.md` | 회신 수령 — `kb/reviews/codex_O_sdcp_doped_estimand_reply_2026_08_28.md` | 같은 라벨 · 주제 토큰 일치 ['doped', 'estimand', 'sdcp']; 판정 인용 3회 |
| P | 2026-08-28 | `codex_P_prompt_wave1_incar_audit_2026_08_28.md` | `codex_P_wave1_incar_audit_reply_2026_08_28.md` | 회신 수령 — `kb/reviews/codex_P_wave1_incar_audit_reply_2026_08_28.md` | 같은 라벨 · 주제 토큰 일치 ['audit', 'incar', 'wave1']; 판정 인용 3회 |
| Q | 2026-08-28 | `codex_Q_prompt_neutral_ptfe_closure_2026_08_28.md` | — | 발송 대기 | — |
| R2 | 2026-08-28 | `codex_R2_prompt_doped_reopen_v3_2026_08_28.md` | `codex_R2_doped_reopen_v3_reply_2026_08_28.md` | 회신 수령 — `kb/reviews/codex_R2_doped_reopen_v3_reply_2026_08_28.md` | 회신 본문의 `요청:` 역링크; 판정 인용 1회 |
| R3 | 2026-08-28 | `codex_R3_prompt_doped_reopen_impl_2026_08_28.md` | `codex_R3_doped_reopen_impl_reply_2026_08_28.md` | 회신 수령 — `kb/reviews/codex_R3_doped_reopen_impl_reply_2026_08_28.md` | 같은 라벨 · 주제 토큰 일치 ['doped', 'impl', 'reopen']; 판정 인용 1회 |
| R4 | 2026-08-28 | `codex_R4_prompt_doped_reopen_impl2_2026_08_28.md` | `codex_R4_doped_reopen_impl2_reply_2026_08_29.md` | 회신 수령 — `kb/reviews/codex_R4_doped_reopen_impl2_reply_2026_08_29.md` | 회신 본문의 `요청:` 역링크 |
| R | 2026-08-28 | `codex_R_prompt_doped_reopen_v2_2026_08_28.md` | `codex_R_doped_reopen_v2_reply_2026_08_28.md` | 회신 수령 — `kb/reviews/codex_R_doped_reopen_v2_reply_2026_08_28.md` | 회신 본문의 `요청:` 역링크 |
| AA | 2026-08-29 | `codex_AA_prompt_stageA_v5_regate_2026_08_29.md` | — | 발송 완료 — 회신 AA 접수, 후속은 codex_AB_prompt_stageA_v9_regate_2026_08_29.md | 판정 인용 6회 |
| AB | 2026-08-29 | `codex_AB_prompt_stageA_v9_regate_2026_08_29.md` | — | 회신 수령 (원문 파일 없음 — 근거: AD (Stage A v10)) | 판정 인용 7회 |
| Q2 | 2026-08-29 | `codex_Q2_prompt_claim_and_normalization_2026_08_29.md` | — | 발송 대기 | 판정 인용 1회 |
| S | 2026-08-29 | `codex_S_prompt_t13_msd_length_2026_08_29.md` | — | 회신 수령 (원문 파일 없음 — 근거: 판정 등재 db/properties/t13_msd_length_verdict_2026_08_29.json) | ⚠ 인용 13회 — 라벨 재사용이라 **증거 아님** |
| T | 2026-08-29 | `codex_T_prompt_sdcp_binding_energy_path_2026_08_29.md` | — | 회신 수령 (원문 파일 없음 — 근거: T P0-1 술포네이트 기전 철회가 db 에 등재) | ⚠ 인용 18회 — 라벨 재사용이라 **증거 아님** |
| U | 2026-08-29 | `codex_U_prompt_neutral_close_plan_2026_08_29.md` | — | 회신 수령 (원문 파일 없음 — 근거: U P0-2 가 회신 W 프롬프트에 인용) | ⚠ 인용 11회 — 라벨 재사용이라 **증거 아님** |
| V | 2026-08-29 | `codex_V_prompt_closure_incar_audit_2026_08_29.md` | — | 발송 대기 | 판정 인용 2회 |
| W | 2026-08-29 | `codex_W_prompt_mlip_selector_validity_2026_08_29.md` | — | 발송 대기 | — |
| X | 2026-08-29 | `codex_X_prompt_prospective_bundle_ready_2026_08_29.md` | `codex_X_bundle_reply_2026_08_29.md` | 회신 수령 — `kb/reviews/codex_X_bundle_reply_2026_08_29.md` | 같은 라벨 · 주제 토큰 일치 ['bundle']; 판정 인용 5회 |
| AC | 2026-08-30 | `codex_AC_prompt_manuscript_v8_crosscheck_2026_08_30.md` | — | 발송전 | — |
| AD | 2026-08-30 | `codex_AD_prompt_stageA_v10_final_regate_2026_08_30.md` | — | 발송전 | — |
| AE | 2026-08-30 | `codex_AE_prompt_stageA_v13_submit_gate_2026_08_30.md` | — | 발송전 | — |
| AG | 2026-08-30 | `codex_AG_prompt_stageA_go_nogo_2026_08_30.md` | — | sent | — |
| AH | 2026-08-30 | `codex_AH_prompt_am_i_lost_2026_08_30.md` | — | sent | — |
| AI | 2026-08-30 | `codex_AI_prompt_current_head_2026_08_30.md` | — | sent | — |
| AJ | 2026-08-30 | `codex_AJ_prompt_c12_submit_2026_08_30.md` | — | sent | — |
| AK | 2026-08-30 | `codex_AK_prompt_lpsocl_box331_md_2026_08_30.md` | `codex_AK_reply_lpsocl_box331_md_2026_08_30.md` | sent | 같은 라벨 · 주제 토큰 일치 ['box331', 'lpsocl', 'md']; 판정 인용 2회 |
| AL | 2026-08-30 | `codex_AL_prompt_cascade_d_rel_2026_08_30.md` | `codex_AL_reply_cascade_d_rel_2026_08_30.md` | sent | 같은 라벨 · 주제 토큰 일치 ['cascade', 'd', 'rel']; 판정 인용 1회 |
| AM | 2026-08-31 | `codex_AM_prompt_c12_incar_2026_08_31.md` | `codex_AM_reply_c12_incar_2026_08_31.md` | sent | 같은 라벨 · 주제 토큰 일치 ['c12', 'incar']; 판정 인용 1회 |
| AN | 2026-08-31 | `codex_AN_prompt_c12_v7_2026_08_31.md` | — | sent | — |
| AP | 2026-08-31 | `codex_AP_prompt_c12_v14_2026_08_31.md` | — | 발송 대기 | 판정 인용 2회 |
| AQ | 2026-08-31 | `codex_AQ_prompt_c12_v15_2026_08_31.md` | `codex_AR_reply_c12_v15_2026_08_31.md` | 회신 수령 — `kb/reviews/codex_AR_reply_c12_v15_2026_08_31.md` | ⚠ 라벨 어긋남(AQ→AR) · 주제 slug 완전일치 |
| AS | 2026-08-31 | `codex_AS_prompt_c12_v16_2026_08_31.md` | — | 발송 대기 | 판정 인용 2회 |
| AT | 2026-08-31 | `codex_AT_prompt_c12_v17_2026_08_31.md` | `codex_AT_reply_c12_v17_2026_08_31.md` | 회신 수령 — `kb/reviews/codex_AT_reply_c12_v17_2026_08_31.md` | 회신 본문의 `요청:` 역링크; 판정 인용 5회 |
| AU | 2026-08-31 | `codex_AU_prompt_c12_v18_2026_08_31.md` | `codex_AV_reply_c12_v18_2026_08_31.md` | 회신 수령 — `kb/reviews/codex_AV_reply_c12_v18_2026_08_31.md` | 회신 본문의 `요청:` 역링크 |
| S | 2026-08-31 | `codex_S_prompt_backbone_polaron_estimand_2026_08_31.md` | — | 회신 수령 (원문 파일 없음 — 근거: 후속 T (폴라론 pilot seeds)) | ⚠ 인용 13회 — 라벨 재사용이라 **증거 아님** |
| T | 2026-08-31 | `codex_T_prompt_polaron_pilot_seeds_2026_08_31.md` | `codex_T_reply_polaron_pilot_2026_08_31.md` | 회신 수령 — `kb/reviews/codex_T_reply_polaron_pilot_2026_08_31.md` | 같은 라벨 · 주제 토큰 일치 ['pilot', 'polaron']; ⚠ 인용 18회 — 라벨 재사용이라 **증거 아님** |
| U | 2026-08-31 | `codex_U_prompt_polaron_S0_2026_08_31.md` | — | 발송 대기 (⚠ 라벨 U 가 재사용됨 — 인용 횟수는 codex_U_prompt_neutral_close_plan 과 합산되므로 근거가 아니다) | ⚠ 인용 11회 — 라벨 재사용이라 **증거 아님** |
| AW | 2026-09-01 | `codex_AW_prompt_webapp_audit_2026_09_01.md` | — | 발송 대기 | — |
