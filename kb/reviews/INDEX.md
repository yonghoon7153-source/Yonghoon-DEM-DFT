---
title: "리뷰 사슬 색인 — 프롬프트↔회신 (자동 생성)"
date: 2026-09-11
updated: 2026-09-11
tags: [index, review, codex]
status: 자동생성
kind: index
confidence: high
verificationStatus: verified
verifiedAt: 2026-09-11
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
| U | 2026-08-29 | `codex_U_prompt_neutral_close_plan_2026_08_29.md` | — | 회신 수령 (원문 파일 없음 — 근거: U P0-2 가 회신 W 프롬프트에 인용) | ⚠ 인용 26회 — 라벨 재사용이라 **증거 아님** |
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
| AL | 2026-08-30 | `codex_AL_prompt_cascade_d_rel_2026_08_30.md` | `codex_AL_reply_cascade_d_rel_2026_08_30.md` | sent | 같은 라벨 · 주제 토큰 일치 ['cascade', 'd', 'rel']; 판정 인용 6회 |
| AM | 2026-08-31 | `codex_AM_prompt_c12_incar_2026_08_31.md` | `codex_AM_reply_c12_incar_2026_08_31.md` | sent | 같은 라벨 · 주제 토큰 일치 ['c12', 'incar']; 판정 인용 2회 |
| AN | 2026-08-31 | `codex_AN_prompt_c12_v7_2026_08_31.md` | — | sent | — |
| AP | 2026-08-31 | `codex_AP_prompt_c12_v14_2026_08_31.md` | — | 발송 대기 | 판정 인용 2회 |
| AQ | 2026-08-31 | `codex_AQ_prompt_c12_v15_2026_08_31.md` | `codex_AR_reply_c12_v15_2026_08_31.md` | 회신 수령 — `kb/reviews/codex_AR_reply_c12_v15_2026_08_31.md` | ⚠ 라벨 어긋남(AQ→AR) · 주제 slug 완전일치 |
| AS | 2026-08-31 | `codex_AS_prompt_c12_v16_2026_08_31.md` | — | 발송 대기 | 판정 인용 2회 |
| AT | 2026-08-31 | `codex_AT_prompt_c12_v17_2026_08_31.md` | `codex_AT_reply_c12_v17_2026_08_31.md` | 회신 수령 — `kb/reviews/codex_AT_reply_c12_v17_2026_08_31.md` | 회신 본문의 `요청:` 역링크; 판정 인용 5회 |
| AU | 2026-08-31 | `codex_AU_prompt_c12_v18_2026_08_31.md` | `codex_AV_reply_c12_v18_2026_08_31.md` | 회신 수령 — `kb/reviews/codex_AV_reply_c12_v18_2026_08_31.md` | 회신 본문의 `요청:` 역링크 |
| S | 2026-08-31 | `codex_S_prompt_backbone_polaron_estimand_2026_08_31.md` | — | 회신 수령 (원문 파일 없음 — 근거: 후속 T (폴라론 pilot seeds)) | ⚠ 인용 15회 — 라벨 재사용이라 **증거 아님** |
| T | 2026-08-31 | `codex_T_prompt_polaron_pilot_seeds_2026_08_31.md` | `codex_T_reply_polaron_pilot_2026_08_31.md` | 회신 수령 — `kb/reviews/codex_T_reply_polaron_pilot_2026_08_31.md` | 같은 라벨 · 주제 토큰 일치 ['pilot', 'polaron']; ⚠ 인용 19회 — 라벨 재사용이라 **증거 아님** |
| U | 2026-08-31 | `codex_U_prompt_polaron_S0_2026_08_31.md` | `codex_U_reply_polaron_S0_2026_09_01.md` | 회신 수령 — 후속 V (P0 9건 이행 완료) | 회신 본문의 `요청:` 역링크; ⚠ 인용 26회 — 라벨 재사용이라 **증거 아님** |
| AW | 2026-09-01 | `codex_AW_prompt_webapp_audit_2026_09_01.md` | `codex_AW_reply_webapp_audit_2026_09_01.md` | 회신 수령 — NO-GO · `kb/reviews/codex_AW_reply_webapp_audit_2026_09_01.md` · 이행 중 | 회신 본문의 `요청:` 역링크; 판정 인용 6회 |
| AX | 2026-09-01 | `codex_AX_prompt_lpsocl_600K_amendment_2026_09_01.md` | — | 발송 대기 | — |
| AY | 2026-09-01 | `codex_AY_prompt_c12_v19_2026_09_01.md` | — | 발송 대기 | 판정 인용 4회 |
| AZ | 2026-09-01 | `codex_AZ_prompt_c12_v20_2026_09_01.md` | — | 발송 대기 | 판정 인용 15회 |
| V | 2026-09-01 | `codex_V_prompt_polaron_S0_2026_09_01.md` | `codex_Y_reply_polaron_S0_2026_09_03.md` | 회신 수령 — 후속 W (P0 5건 이행) | ⚠ 라벨 어긋남(V→Y) · 주제 slug 완전일치; ⚠ 인용 14회 — 라벨 재사용이라 **증거 아님** |
| BA | 2026-09-02 | `codex_BA_prompt_c12_v21_2026_09_02.md` | — | 회신 수령 — 후속 BB | 판정 인용 7회 |
| BB | 2026-09-02 | `codex_BB_prompt_c12_v22_2026_09_02.md` | — | 발송 대기 | 판정 인용 3회 |
| BC | 2026-09-02 | `codex_BC_prompt_c12_v23_2026_09_02.md` | — | 발송 대기 | 판정 인용 7회 |
| W | 2026-09-02 | `codex_W_prompt_polaron_S0_2026_09_02.md` | — | 발송 대기 | ⚠ 인용 10회 — 라벨 재사용이라 **증거 아님** |
| X | 2026-09-02 | `codex_X_prompt_polaron_S0_2026_09_02.md` | — | 발송 대기 | ⚠ 인용 13회 — 라벨 재사용이라 **증거 아님** |
| BF | 2026-09-03 | `codex_BF_prompt_c12_v29_2026_09_03.md` | `codex_BF_reply_c12_v29_2026_09_03.md` | 발송 대기 | 같은 라벨 · 주제 토큰 일치 ['c12', 'v29'] |
| BG | 2026-09-07 | `codex_BG_prompt_webapp_aw_release_2026_09_07.md` | — | 작성 — 발송 대기 | 판정 인용 3회 |
| BH | 2026-09-07 | `codex_BH_prompt_md_axis_audit_2026_09_07.md` | — | 작성 — 발송 대기 | 판정 인용 1회 |
| BI | 2026-09-08 | `codex_BI_prompt_webapp_claim_binding_2026_09_08.md` | — | 발송 | — |
| BJ2 | 2026-09-09 | `codex_BJ2_prompt_cascade_redesign_2026_09_09.md` | `codex_BJ2_reply_2026_09_09.md` | 초안 | 회신 본문의 `요청:` 역링크 |
| BJ | 2026-09-09 | `codex_BJ_prompt_cascade_redesign_2026_09_09.md` | — | 회신됨-NO-GO | — |
| BK | 2026-09-09 | `codex_BK_prompt_doping_question_2026_09_09.md` | — | 초안 | — |
| BL | 2026-09-11 | `codex_BL_prompt_lpsocl_gate_ambiguity_2026_09_11.md` | `codex_BL_reply_lpsocl_gate_ambiguity_2026_09_11.md` | 진행 | 같은 라벨 · 주제 토큰 일치 ['ambiguity', 'gate', 'lpsocl']; 판정 인용 1회 |
| BM | 2026-09-12 | `codex_BM_prompt_li2s_layer1_density_gate_2026_09_12.md` | `codex_BM_reply_li2s_layer1_density_gate_2026_09_12.md` | 진행 | 1층 밀도 게이트 — **G4 재설계 필요, seed1 합격·2층 진행은 반대**. 후속: `db/properties/lpscl_li2s_layer1_g2_deviation_2026_09_12.json` (P0 G2 이탈 확인) |
| BN | 2026-09-12 | `codex_BN_prompt_cascade_rebuild_2026_09_12.md` | `codex_BN_reply_cascade_rebuild_2026_09_12.md` | **회신됨-NO-GO** | 560 GPU-h 불승인 · 재건 방향 찬성 · 카드 P0 7건(D 식·처방 미정의·`Li_48h` 미구현·UMA +34 % 정적대조 선행·무반복 factorial df 0·게이트 반례·성공전용 마감) · 채택 순서 = 처방감사(GPU 0) → 동일구조 DFT–UMA E/F/응력 대조 → 한 대비 파일럿 |
| BO | 2026-09-12 | `codex_BO_prompt_cascade_rebuild_v2_2026_09_12.md` | `codex_BO_reply_cascade_rebuild_v2_2026_09_12.md` | **회신됨-조건부GO** | 정적대조 2 SCF·파일럿 30런 둘 다 조건부 GO — 단 'UMA 내부 진단' 한정. 실행 전 5조건: basin 분기 삭제·공통 부모 배열 2·비-Li 골격 기준계(Li-COM 제거는 신호 삭제)·D=기울기/6·EOS↔B_V·df 설계별·factorial 자동진입 금지. 'UMA 편향 ~0'·'가짜 basin' → 가설 강등 |
| BP | 2026-09-13 | `codex_BP_prompt_static_pair_result_2026_09_13.md` | `codex_BP_reply_static_pair_result_2026_09_13.md` | **회신됨-조건부GO** | **조건 1 이행 인정** (리뷰어가 해시 대조 + δΔE 6.1276 · 힘 RMSE 0.0654687/0.0971261 독립 재현). **파일럿은 조건부 GO — 단 지금 코드 그대로의 즉시 실행 승인은 아니다**: 셀 정책 문서와 실제 경로가 어긋난다. ★ **구현 불일치 2건을 우리가 실물 확인**: ① 'NO vc-relax, fixed-cell' 은 **DFT 에만** 걸려 있고 같은 README 다음 줄이 'UMA full relax' · UMA 기본 경로는 형상 무제한 `CellFilter` ② `run_mlip_postproc.py` 의 `eos_sweep` 이 `atoms_ref` 를 안 바꿔 **EOS V₀ 가 후속 탄성에 전달되지 않는다**(post-anneal 구조가 들어간다) → `cell_policy_gap_2026_09_13.json`. **우리 서술 정정 7건**: 전단 상쇄 **반대**(공통인 것은 제약이지 응답이 아니다) · '모든 구조가 공유' **과함**(허용할 뿐 강제 아님) · δΔE 비전이 **이유가 틀렸다**(조성별 상수는 힘·MD·D 불변, Ea 차에서도 소거 ⇒ 진짜 이유는 기울기·곡률·이동경로 미검증 ⇒ '방법 간 Ea·탄성률 오차: 미측정') · Q5 **반대**(최소점 위치 금지, **대칭 연결 16원자를 독립 재현 16건으로 세지 말 것**) · (a) = 고정셀 원자 정상점 **후보** · 재실행 성공 ≠ 최초 실패 원인 배제 · 10–30 meV 항목은 δΔE 가 아니라 **방법 내 ΔE**. Q2 = **선택 ②**(문구 축소: '지정된 UMA·배열·셀 정책에서 치환 처방에 대한 모델의 응답과 관측 산포를 예비 진단') · Q6 = 하드게이트 소급 **안 함**, 대신 경보 초과를 알고도 내부 진단만 한다는 **운영 판단을 실행 전에 기록** |
| BQ | 2026-09-13 | `codex_BQ_prompt_eos_v0_disordered_2026_09_13.md` | `codex_BQ_reply_eos_v0_disordered_2026_09_13.md` | **회신됨-예비판정** | 무질서 초격자에서 per-구조 EOS V₀ 가 성립하는가 — §4b 차단. **양쪽 다 보류**: v4 실행 보류 + "무질서라 EOS 불성립" 결론도 반대. 코드 P0×3·P1 지적(전부 이행). 길 둘 — ① v4 유지하고 고친 코드로 재판단 ② E′(공통 총부피)+탄성 보류+조건부 수송 |
| BQ-2 | 2026-09-13 | `codex_BQ2_prompt_fix_verification_2026_09_13.md` | `codex_BQ2_reply_fix_verification_2026_09_13.md` | **회신됨-NO-GO** | **NO-GO** — P0-2(곡선 혼합)·P1(압력 부호)은 해제, **P0-1·P0-3 미해제**. 핵심: 수렴을 *기록만* 하고 게이트에 **배선하지 않았다**(굶긴 0/14 이 fit_ok=True). P0-3 수정이 **새 회귀**를 만들었다(실패 EOS 의 마지막 팽창점이 `final_v0_applied` 로 승격). Q2 게이트도 여전히 원시 dE/span. Q1 수렴 정의 오탐. **점별 구조 미저장 → 골짜기 질문 답 불가**. 스윕은 계속 두고 후처리로 재판정 |
| BQ-3 | 2026-09-13 | `codex_BQ3_prompt_sweep_complete_2026_09_13.md` | `codex_BQ3_reply_sweep_complete_2026_09_13.md` | **회신됨-NO-GO·10스윕 조건부GO** | **스윕 완결 25/25** — BQ 가 기다리던 §4 표. V₀ 조건간 산포: 질서 H0 **0.05 %·자격 5/5** 대 무질서 0.72–32.98 %·최대 2/5. 재판정 판정변경 0/25·사유변경 16/25. 회신: §4b 해제 **NO-GO 유지**(P0-1 잔여 = 하강 수렴 미요구 · P0-3 잔여 = 폴더 재사용 시 옛 파일 잔존 · P1 = 반환값이 힘 판정을 덮음·기록 개수만 셈) · **내 §4b① 오인용 지적** · 산포는 '설정 민감도'이지 조건 독립성 인증이 아님 · B₀′ 는 조건부 인용만 · ★ **다음 런 = 5구조×W3_f02/W3_f005 10스윕 조건부 GO**(점별 extxyz 140프레임 · 최근접 수렴점 승계 · RMSD+이웃 ID 비교 · 한 라운드 고정·자동 확대 금지). 실행 전 최소조건 3개 → 전부 이행(selftest 141 · 드라이버 9). B₀′ 는 질서 구조에서 fmax 0.005 면 창과 무관해진다(4.34/4.38) — f02 의 민감도는 완화 부족이었다 |

## 🔴 모순 (status 는 대기인데 증거는 회신 수령)

- `codex_AZ_prompt_c12_v20_2026_09_01.md` [발송 대기] — 판정이 15회 인용됐다 — 회신을 받은 것으로 보인다 (원문 파일 없음)
- `codex_BC_prompt_c12_v23_2026_09_02.md` [발송 대기] — 판정이 7회 인용됐다 — 회신을 받은 것으로 보인다 (원문 파일 없음)
- `codex_BF_prompt_c12_v29_2026_09_03.md` [발송 대기] — 회신 파일이 있다: codex_BF_reply_c12_v29_2026_09_03.md
