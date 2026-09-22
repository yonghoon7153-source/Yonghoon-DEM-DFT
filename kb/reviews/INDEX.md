---
title: "리뷰 사슬 색인 — 프롬프트↔회신 (자동 생성)"
date: 2026-09-22
updated: 2026-09-22
tags: [index, review, codex]
status: 자동생성
kind: index
confidence: high
verificationStatus: verified
verifiedAt: 2026-09-22
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
| R4 | 2026-08-28 | `codex_R4_prompt_doped_reopen_impl2_2026_08_28.md` | `codex_R4_doped_reopen_impl2_reply_2026_08_29.md` | 회신 수령 — `kb/reviews/codex_R4_doped_reopen_impl2_reply_2026_08_29.md` | 회신 본문의 `요청:` 역링크; 판정 인용 1회 |
| R | 2026-08-28 | `codex_R_prompt_doped_reopen_v2_2026_08_28.md` | `codex_R_doped_reopen_v2_reply_2026_08_28.md` | 회신 수령 — `kb/reviews/codex_R_doped_reopen_v2_reply_2026_08_28.md` | 회신 본문의 `요청:` 역링크 |
| AA | 2026-08-29 | `codex_AA_prompt_stageA_v5_regate_2026_08_29.md` | — | 발송 완료 — 회신 AA 접수, 후속은 codex_AB_prompt_stageA_v9_regate_2026_08_29.md | 판정 인용 7회 |
| AB | 2026-08-29 | `codex_AB_prompt_stageA_v9_regate_2026_08_29.md` | — | 회신 수령 (원문 파일 없음 — 근거: AD (Stage A v10)) | 판정 인용 7회 |
| Q2 | 2026-08-29 | `codex_Q2_prompt_claim_and_normalization_2026_08_29.md` | — | 발송 대기 | 판정 인용 1회 |
| S | 2026-08-29 | `codex_S_prompt_t13_msd_length_2026_08_29.md` | — | 회신 수령 (원문 파일 없음 — 근거: 판정 등재 db/properties/t13_msd_length_verdict_2026_08_29.json) | ⚠ 인용 15회 — 라벨 재사용이라 **증거 아님** |
| T | 2026-08-29 | `codex_T_prompt_sdcp_binding_energy_path_2026_08_29.md` | — | 회신 수령 (원문 파일 없음 — 근거: T P0-1 술포네이트 기전 철회가 db 에 등재) | ⚠ 인용 19회 — 라벨 재사용이라 **증거 아님** |
| U | 2026-08-29 | `codex_U_prompt_neutral_close_plan_2026_08_29.md` | — | 회신 수령 (원문 파일 없음 — 근거: U P0-2 가 회신 W 프롬프트에 인용) | ⚠ 인용 27회 — 라벨 재사용이라 **증거 아님** |
| V | 2026-08-29 | `codex_V_prompt_closure_incar_audit_2026_08_29.md` | — | 발송 대기 | ⚠ 인용 14회 — 라벨 재사용이라 **증거 아님** |
| W | 2026-08-29 | `codex_W_prompt_mlip_selector_validity_2026_08_29.md` | — | 발송 대기 | ⚠ 인용 10회 — 라벨 재사용이라 **증거 아님** |
| X | 2026-08-29 | `codex_X_prompt_prospective_bundle_ready_2026_08_29.md` | `codex_X_bundle_reply_2026_08_29.md` | 회신 수령 — `kb/reviews/codex_X_bundle_reply_2026_08_29.md` | 같은 라벨 · 주제 토큰 일치 ['bundle']; ⚠ 인용 13회 — 라벨 재사용이라 **증거 아님** |
| AC | 2026-08-30 | `codex_AC_prompt_manuscript_v8_crosscheck_2026_08_30.md` | — | 발송전 | — |
| AD | 2026-08-30 | `codex_AD_prompt_stageA_v10_final_regate_2026_08_30.md` | — | 발송전 | — |
| AE | 2026-08-30 | `codex_AE_prompt_stageA_v13_submit_gate_2026_08_30.md` | — | 발송전 | — |
| AG | 2026-08-30 | `codex_AG_prompt_stageA_go_nogo_2026_08_30.md` | — | sent | — |
| AH | 2026-08-30 | `codex_AH_prompt_am_i_lost_2026_08_30.md` | — | sent | — |
| AI | 2026-08-30 | `codex_AI_prompt_current_head_2026_08_30.md` | — | sent | — |
| AJ | 2026-08-30 | `codex_AJ_prompt_c12_submit_2026_08_30.md` | — | sent | — |
| AK | 2026-08-30 | `codex_AK_prompt_lpsocl_box331_md_2026_08_30.md` | `codex_AK_reply_lpsocl_box331_md_2026_08_30.md` | sent | 같은 라벨 · 주제 토큰 일치 ['box331', 'lpsocl', 'md']; 판정 인용 5회 |
| AL | 2026-08-30 | `codex_AL_prompt_cascade_d_rel_2026_08_30.md` | `codex_AL_reply_cascade_d_rel_2026_08_30.md` | sent | 같은 라벨 · 주제 토큰 일치 ['cascade', 'd', 'rel']; 판정 인용 7회 |
| AM | 2026-08-31 | `codex_AM_prompt_c12_incar_2026_08_31.md` | `codex_AM_reply_c12_incar_2026_08_31.md` | sent | 같은 라벨 · 주제 토큰 일치 ['c12', 'incar']; 판정 인용 4회 |
| AN | 2026-08-31 | `codex_AN_prompt_c12_v7_2026_08_31.md` | — | sent | — |
| AP | 2026-08-31 | `codex_AP_prompt_c12_v14_2026_08_31.md` | — | 발송 대기 | 판정 인용 2회 |
| AQ | 2026-08-31 | `codex_AQ_prompt_c12_v15_2026_08_31.md` | `codex_AR_reply_c12_v15_2026_08_31.md` | 회신 수령 — `kb/reviews/codex_AR_reply_c12_v15_2026_08_31.md` | ⚠ 라벨 어긋남(AQ→AR) · 주제 slug 완전일치 |
| AS | 2026-08-31 | `codex_AS_prompt_c12_v16_2026_08_31.md` | — | 발송 대기 | 판정 인용 5회 |
| AT | 2026-08-31 | `codex_AT_prompt_c12_v17_2026_08_31.md` | `codex_AT_reply_c12_v17_2026_08_31.md` | 회신 수령 — `kb/reviews/codex_AT_reply_c12_v17_2026_08_31.md` | 회신 본문의 `요청:` 역링크; 판정 인용 16회 |
| AU | 2026-08-31 | `codex_AU_prompt_c12_v18_2026_08_31.md` | `codex_AV_reply_c12_v18_2026_08_31.md` | 회신 수령 — `kb/reviews/codex_AV_reply_c12_v18_2026_08_31.md` | 회신 본문의 `요청:` 역링크 |
| S | 2026-08-31 | `codex_S_prompt_backbone_polaron_estimand_2026_08_31.md` | — | 회신 수령 (원문 파일 없음 — 근거: 후속 T (폴라론 pilot seeds)) | ⚠ 인용 15회 — 라벨 재사용이라 **증거 아님** |
| T | 2026-08-31 | `codex_T_prompt_polaron_pilot_seeds_2026_08_31.md` | `codex_T_reply_polaron_pilot_2026_08_31.md` | 회신 수령 — `kb/reviews/codex_T_reply_polaron_pilot_2026_08_31.md` | 같은 라벨 · 주제 토큰 일치 ['pilot', 'polaron']; ⚠ 인용 19회 — 라벨 재사용이라 **증거 아님** |
| U | 2026-08-31 | `codex_U_prompt_polaron_S0_2026_08_31.md` | `codex_U_reply_polaron_S0_2026_09_01.md` | 회신 수령 — 후속 V (P0 9건 이행 완료) | 회신 본문의 `요청:` 역링크; ⚠ 인용 27회 — 라벨 재사용이라 **증거 아님** |
| AW | 2026-09-01 | `codex_AW_prompt_webapp_audit_2026_09_01.md` | `codex_AW_reply_webapp_audit_2026_09_01.md` | 회신 수령 — NO-GO · `kb/reviews/codex_AW_reply_webapp_audit_2026_09_01.md` · 이행 중 | 회신 본문의 `요청:` 역링크; 판정 인용 6회 |
| AX | 2026-09-01 | `codex_AX_prompt_lpsocl_600K_amendment_2026_09_01.md` | — | 발송 대기 | — |
| AY | 2026-09-01 | `codex_AY_prompt_c12_v19_2026_09_01.md` | — | 발송 대기 | 판정 인용 4회 |
| AZ | 2026-09-01 | `codex_AZ_prompt_c12_v20_2026_09_01.md` | — | 발송 대기 | 판정 인용 21회 |
| V | 2026-09-01 | `codex_V_prompt_polaron_S0_2026_09_01.md` | `codex_Y_reply_polaron_S0_2026_09_03.md` | 회신 수령 — 후속 W (P0 5건 이행) | ⚠ 라벨 어긋남(V→Y) · 주제 slug 완전일치; ⚠ 인용 14회 — 라벨 재사용이라 **증거 아님** |
| BA | 2026-09-02 | `codex_BA_prompt_c12_v21_2026_09_02.md` | — | 회신 수령 — 후속 BB | 판정 인용 10회 |
| BB | 2026-09-02 | `codex_BB_prompt_c12_v22_2026_09_02.md` | — | 발송 대기 | 판정 인용 8회 |
| BC | 2026-09-02 | `codex_BC_prompt_c12_v23_2026_09_02.md` | — | 발송 대기 | 판정 인용 8회 |
| W | 2026-09-02 | `codex_W_prompt_polaron_S0_2026_09_02.md` | `internal_Z2_reply_polaron_S0_2026_09_03.md` | 발송 대기 | ⚠ 라벨 어긋남(W→Z2) · 주제 slug 완전일치; ⚠ 인용 10회 — 라벨 재사용이라 **증거 아님** |
| X | 2026-09-02 | `codex_X_prompt_polaron_S0_2026_09_02.md` | `internal_Z3_reply_polaron_S0_2026_09_03.md` | 발송 대기 | ⚠ 라벨 어긋남(X→Z3) · 주제 slug 완전일치; ⚠ 인용 13회 — 라벨 재사용이라 **증거 아님** |
| BF | 2026-09-03 | `codex_BF_prompt_c12_v29_2026_09_03.md` | `codex_BF_reply_c12_v29_2026_09_03.md` | 발송 대기 | 같은 라벨 · 주제 토큰 일치 ['c12', 'v29'] |
| BG | 2026-09-07 | `codex_BG_prompt_webapp_aw_release_2026_09_07.md` | — | 작성 — 발송 대기 | 판정 인용 3회 |
| BH | 2026-09-07 | `codex_BH_prompt_md_axis_audit_2026_09_07.md` | — | 작성 — 발송 대기 | 판정 인용 1회 |
| BI | 2026-09-08 | `codex_BI_prompt_webapp_claim_binding_2026_09_08.md` | — | 발송 | — |
| BJ2 | 2026-09-09 | `codex_BJ2_prompt_cascade_redesign_2026_09_09.md` | `codex_BJ2_reply_2026_09_09.md` | 초안 | 회신 본문의 `요청:` 역링크; 판정 인용 4회 |
| BJ | 2026-09-09 | `codex_BJ_prompt_cascade_redesign_2026_09_09.md` | — | 회신됨-NO-GO | — |
| BK | 2026-09-09 | `codex_BK_prompt_doping_question_2026_09_09.md` | — | 초안 | — |
| BL | 2026-09-11 | `codex_BL_prompt_lpsocl_gate_ambiguity_2026_09_11.md` | `codex_BL_reply_lpsocl_gate_ambiguity_2026_09_11.md` | 진행 | 같은 라벨 · 주제 토큰 일치 ['ambiguity', 'gate', 'lpsocl']; 판정 인용 1회 |
| BM | 2026-09-12 | `codex_BM_prompt_li2s_layer1_density_gate_2026_09_12.md` | `codex_BM_reply_li2s_layer1_density_gate_2026_09_12.md` | 발송대기 | 회신 본문의 `요청:` 역링크 |
| BN | 2026-09-12 | `codex_BN_prompt_cascade_rebuild_2026_09_12.md` | `codex_BN_reply_cascade_rebuild_2026_09_12.md` | (frontmatter 없음) | 같은 라벨 · 주제 토큰 일치 ['cascade', 'rebuild']; 판정 인용 7회 |
| BO | 2026-09-12 | `codex_BO_prompt_cascade_rebuild_v2_2026_09_12.md` | `codex_BO_reply_cascade_rebuild_v2_2026_09_12.md` | (frontmatter 없음) | 같은 라벨 · 주제 토큰 일치 ['cascade', 'rebuild', 'v2']; 판정 인용 2회 |
| BP | 2026-09-13 | `codex_BP_prompt_static_pair_result_2026_09_13.md` | `codex_BP_reply_static_pair_result_2026_09_13.md` | 발송대기 | 같은 라벨 · 주제 토큰 일치 ['pair', 'result', 'static']; 판정 인용 5회 |
| BQ2 | 2026-09-13 | `codex_BQ2_prompt_fix_verification_2026_09_13.md` | `codex_BQ2_reply_fix_verification_2026_09_13.md` | (frontmatter 없음) | 같은 라벨 · 주제 토큰 일치 ['fix', 'verification']; 판정 인용 2회 |
| BQ3 | 2026-09-13 | `codex_BQ3_prompt_sweep_complete_2026_09_13.md` | `codex_BQ3_reply_sweep_complete_2026_09_13.md` | 발송 대기 | 같은 라벨 · 주제 토큰 일치 ['complete', 'sweep'] |
| BQ4 | 2026-09-13 | `codex_BQ4_prompt_10sweep_basin_2026_09_13.md` | `codex_BQ4_reply_10sweep_basin_2026_09_13.md` | 회신됨-종결GO | 같은 라벨 · 주제 토큰 일치 ['10sweep', 'basin'] |
| BQ5 | 2026-09-13 | `codex_BQ5_prompt_eprime_card_2026_09_13.md` | `codex_BQ5_reply_eprime_card_2026_09_13.md` | 회신됨-방향GO-카드NO-GO | 같은 라벨 · 주제 토큰 일치 ['card', 'eprime'] |
| BQ6 | 2026-09-13 | `codex_BQ6_prompt_eprime_v51_2026_09_13.md` | `codex_BQ6_reply_eprime_v51_2026_09_13.md` | 회신됨-②미해제 | 같은 라벨 · 주제 토큰 일치 ['eprime', 'v51'] |
| BQ7 | 2026-09-13 | `codex_BQ7_prompt_eprime_v52_2026_09_13.md` | — | 발송 대기 | — |
| BQ | 2026-09-13 | `codex_BQ_prompt_eos_v0_disordered_2026_09_13.md` | `codex_BQ_reply_eos_v0_disordered_2026_09_13.md` | (frontmatter 없음) | 같은 라벨 · 주제 토큰 일치 ['disordered', 'eos', 'v0']; 판정 인용 16회 |
| BR | 2026-09-14 | `codex_BR_prompt_li2s_layer1_g2_density_2026_09_14.md` | `codex_BR_reply_li2s_layer1_g2_density_2026_09_14.md` | 발송됨 | 같은 라벨 · 주제 토큰 일치 ['density', 'g2', 'layer1', 'li2s']; 판정 인용 14회 |
| BS | 2026-09-22 | `li2s1a_BS_prompt_li2s_relax_provenance_2026_09_22.md` | `li2s1a_BS_reply_li2s_relax_provenance_2026_09_22.md` | 수신됨-회신함 | 같은 라벨 · 주제 토큰 일치 ['li2s', 'provenance', 'relax'] |
| BT | 2026-09-22 | `li2s1a_BT_prompt_neff_window_bootstrap_2026_09_22.md` | `li2s1a_BT_reply_neff_window_bootstrap_2026_09_22.md` | 수신됨-회신함 | 같은 라벨 · 주제 토큰 일치 ['bootstrap', 'neff', 'window'] |
| BU | 2026-09-22 | `li2s1a_BU_prompt_variance_ratio_rule_2026_09_22.md` | `li2s1a_BU_reply_variance_ratio_rule_2026_09_22.md` | 수신됨-회신함 | 같은 라벨 · 주제 토큰 일치 ['ratio', 'rule', 'variance'] |

## 🔴 모순 (status 는 대기인데 증거는 회신 수령)

- `codex_AS_prompt_c12_v16_2026_08_31.md` [발송 대기] — 판정이 5회 인용됐다 — 회신을 받은 것으로 보인다 (원문 파일 없음)
- `codex_AZ_prompt_c12_v20_2026_09_01.md` [발송 대기] — 판정이 21회 인용됐다 — 회신을 받은 것으로 보인다 (원문 파일 없음)
- `codex_BB_prompt_c12_v22_2026_09_02.md` [발송 대기] — 판정이 8회 인용됐다 — 회신을 받은 것으로 보인다 (원문 파일 없음)
- `codex_BC_prompt_c12_v23_2026_09_02.md` [발송 대기] — 판정이 8회 인용됐다 — 회신을 받은 것으로 보인다 (원문 파일 없음)
- `codex_BF_prompt_c12_v29_2026_09_03.md` [발송 대기] — 회신 파일이 있다: codex_BF_reply_c12_v29_2026_09_03.md
- `codex_BM_prompt_li2s_layer1_density_gate_2026_09_12.md` [발송대기] — 회신 파일이 있다: codex_BM_reply_li2s_layer1_density_gate_2026_09_12.md
- `codex_BP_prompt_static_pair_result_2026_09_13.md` [발송대기] — 회신 파일이 있다: codex_BP_reply_static_pair_result_2026_09_13.md
- `codex_BQ3_prompt_sweep_complete_2026_09_13.md` [발송 대기] — 회신 파일이 있다: codex_BQ3_reply_sweep_complete_2026_09_13.md
- `codex_W_prompt_polaron_S0_2026_09_02.md` [발송 대기] — 회신 파일이 있다: internal_Z2_reply_polaron_S0_2026_09_03.md
- `codex_X_prompt_polaron_S0_2026_09_02.md` [발송 대기] — 회신 파일이 있다: internal_Z3_reply_polaron_S0_2026_09_03.md
