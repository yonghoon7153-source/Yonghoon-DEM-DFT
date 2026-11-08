# Codex 회차 ③ 짧은 재확인 요청 — Rint ② 회차 ② (11-05) 고침 · 사전 공격 9 · 10 · 11 · 12 고침 · S0 단계 1 메모리 고침 (2026-11-08 · 사전 공격 ① ② ③ 반영 · ① 독립 대조 반영 · 발송 = 1저자)

> **한 줄**: Codex 회차 ② (`docs/reviews/codex_review_rint2_rr_round2_20261105.md` · 리뷰 핀 `6917c3c9f` · HOLD · 새 P1 0 · P2 1 · P3 2) 의 RR2-01 · 02 · 03 과 봉인 전 필수 PC6-05 를 `f5b00a838` 에서 고쳤고, 그 고침을 사전 공격 9 · 10 · 11 회차로 다시 깨서 나온 것을 `f5b00a838` · `766e1e80c` · `6a81f0c55` 에서 고쳤다 · 판정문 §8 Q8 의 S0 메모리 고침 = `f47bde0f6`.  §3 의 고침이 그 finding 과 같은 부류를 닫는지 · 재개 정책 HOLD 를 풀 수 있는지만 본다 (판정문 §8 끝 문단의 좁은 재검토).  사전 공격 12 (11-08 · §5-2) 가 `6a81f0c55` 확장에서 P2 셋 · P3 둘을 새로 찾았고 → 1저자 11-08 *"권고대로"* = (가) Codex 전에 고침 `d346ca943` (§5-3 · 원장 PC12-01–05 claimed_fixed).
> **리뷰 핀** = 이 요청서가 든 커밋 (작업 가지 B `claude/sdcp-dem-manuscript-si-pqwtv8` · push · stoic `claude/stoic-knuth-NObVQ` = 복귀 전까지 `6a81f0c55` 에서 동결 · 복귀 = stoic 을 B 끝으로 fast-forward) · 번호 = ZIP 의 PIN.txt (이 파일은 그 커밋 안이라 제 번호를 못 적는다) · **비교 기준** = `6917c3c9f` (회차 ② 리뷰 핀 · stoic) — 그 사이 Rint ② 밖 커밋 (50kg · Ⓐ G2c · FAM · /emod · 후막 · 게이트 나누기) 이 섞임 · Rint ② 범위 = §2.
> **1저자** — 11-05 *"권고대로"* (수정 계획 `docs/reviews/rint2_rr2_fix_plan_20261105.md` Q1–Q7 = (가) · 사전 공격 9 PA-01–07 고침) · 11-06 *"권고대로"* (사전 공격 10 고침 · N1 · N2 · N4 · 규칙 = 생산자가 쓰지 않는 칸 조합 = 모순 = 재실행 자격 없음) · 11-08 *"권고대로"* (이 요청서 · 인계 `docs/handoff_to_subsession_20261108.md` §5-1) · 11-08 *"권고대로"* (사전 공격 12 처분 = (가) Codex 전에 고침 `d346ca943`) · 발송 = 1저자.

## 0. 이번에 닫는 것 / 닫지 않는 것

| 이번에 닫으려는 것 (판정 요청) | 닫지 않는 것 (이 회차 범위 밖) |
|---|---|
| ① 회차 ② RR2-01 (P2) · RR2-02 · 03 (P3) + 봉인 전 필수 PC6-05 (P3) + 부분 PC6-13 (남은 분기 = RR2-01 · 수정 계획 Q5 (가)) — `f5b00a838` | 확장 한정 (`docs/reviews/rint2_rr2_fix_evidence_20261105/pc10_n_fix/ext/REPORT_EXT.md` §8 · 새 open PC11-05–08 · §4) |
| ② 사전 공격 9 PC9-01 (P2) · 02–07 (P3) — `f5b00a838` (PC9-08 = wontfix · 한정) | PC12 고침의 한정 (`docs/reviews/rint2_rr2_fix_evidence_20261105/pc12_fix/REPORT.md` 한정 절 §6 · §4) · SELF-158 (과장 정정 = 이 요청서 §5-2 · open) |
| ③ 사전 공격 10 PC10-01 (P2) · 02–07 (P3) — `766e1e80c` | Q5 현장 자격 — PC5-03 · 07 · 08 · PC6-01 · PC8-05 (현장 자격 = 판정문 §9 · 항목 = 수정 계획 Q5 · 결과 아직 0 건) |
| ④ PC10-08 · 09 (P2 · N1 · N2) · 10 (P3 · N4) + 사전 공격 11 확장 PC11-01 · 02 (P2 · P2-A · P2-B) · 03 · 04 (P3 · P3-5 · P3-6) — `6a81f0c55` (REPORT_EXT §9 · PC11-02 의 GU 기록 rc 꼴 = PC12-02 가 좁힘 → ⑥ 에서 닫음) | kgy S0 단계 1 재실행 결과 (새 핀 peak RSS · 시간 · rc · 출력 여섯 · 0 건) |
| ⑤ S0 메모리 SELF-155 (P2) — `f47bde0f6` · 회차 ② §8 Q8 칸 = `docs/reviews/rint2_s0_mem_fix_20261106/REPORT.md` §11 · 선언된 예외 둘 · CP-ORD 섞는 자리 옮김 · S0 계획 해시 바뀜 | 봉인 (숫자 칸 · 실행 정책 · S0 / R 계획 해시) · S0 단계 2 · 봉인 전 12 단위 분산 / 합치기 끝-끝 (수정 계획 Q6 (가) · 0 건) · R 런 · 정량 판정 · 생산 GO (0 건) · 빠진 물리 (v0 동결) · ⑦ SBE 탐침 (봉인 뒤 · Q7 (가)) |
| ⑥ 사전 공격 12 PC12-01 · 02 · 03 (P2) · 04 · 05 (P3) 고침 — `d346ca943` (시험 먼저 PC12A–E 0/5 → 5/5 · 사슬 476/476 → 481/481 · 변이 7/7 · 탐침 재실행 = F1–F5 위조 행 거부 · 정직 꼴 그대로 · 3.8 11 묶음 · §5-3) | 고친 가드에 대한 독립 재공격 (사전 공격 13) = 없음 (있는 것 = 변이 7 · 탐침 재실행 · 독립 대조 = 요청서 주장 ↔ 출처만) — Codex 반례 = 이 회차 Q3 |

## 1. 보내는 것 (ZIP · repo/ = 리뷰 핀 blob 그대로 + PIN.txt)

| 묶음 | 파일 | 수 |
|---|---|---|
| 이 요청서 | `docs/reviews/codex_rint2_rr_round3_request_20261108.md` | 1 |
| 회차 ② 판정 · 반입 · 수정 계획 | `docs/reviews/codex_review_rint2_rr_round2_20261105.md` · `docs/reviews/codex_rint2_rr_round2_evidence_20261105/` (우리 트리 재현 `_repro_ours_20261105/` 포함) · `docs/reviews/rint2_rr2_fix_plan_20261105.md` | 1 + 84 + 1 |
| 고침 증거 | `docs/reviews/rint2_rr2_fix_evidence_20261105/` — 보고 `docs/reviews/rint2_rr2_fix_evidence_20261105/REPORT.md` (RR2 · 사전 공격 9) · `docs/reviews/rint2_rr2_fix_evidence_20261105/preattack10_fix/REPORT.md` · `docs/reviews/rint2_rr2_fix_evidence_20261105/pc10_n_fix/REPORT.md` · `docs/reviews/rint2_rr2_fix_evidence_20261105/pc10_n_fix/ext/REPORT_EXT.md` · `docs/reviews/rint2_rr2_fix_evidence_20261105/preattack12/REPORT.md` · `docs/reviews/rint2_rr2_fix_evidence_20261105/pc12_fix/REPORT.md` (PC12 고침 · 67 파일) · `docs/reviews/rint2_rr2_fix_evidence_20261105/req3_verify/REPORT.md` (사전 공격 ① 독립 대조 · 2 파일) · 바깥 SHA256SUMS 287 줄 = preattack12/ · pc12_fix/ · req3_verify/ 를 뺀 파일 (SHA256SUMS 이름 뺌) · 안 SHA256SUMS = preattack10_fix/ 68 · pc10_n_fix/ 143 (ext/ 포함) · preattack12/ 16 · pc12_fix/ 66 · req3_verify/ 1 | 376 (= 307 + 67 + 2) |
| S0 메모리 | `docs/reviews/rint2_s0_mem_fix_20261106/` (SHA256SUMS 155) · 근거 측정 `docs/reviews/rint2_s0_mem_probe_20261106/` (SHA256SUMS 2) | 156 + 3 |
| 원장 | `docs/reviews/findings.json` | 1 |
| 바뀐 Rint ② 코드 · 시험 (`6917c3c9f` → 핀 · `d346ca943` 의 PC12 고침 = 앞 둘에 포함) | `scripts/rint_r_chain.py` · `scripts/test_rint_r_chain.py` · `scripts/carbon_junction.py` · `scripts/test_carbon_junction.py` · `scripts/ca_s0_census.py` · `scripts/test_ca_s0_census.py` (`git diff --stat 6917c3c9f <핀> -- scripts/` = 8 파일 · 나머지 둘 `scripts/check_all.sh` · `scripts/test_check_all_split.sh` = 게이트 나누기 · Rint ② 밖) | 6 |
| 실행 의존 (`6917c3c9f` 와 diff 0) | 사슬 CODE_FILES (`scripts/rint_r_chain.py` 302 줄) 의 나머지 16 · 시험이 간접 import 하는 다섯 (test_ca_ext_b6 ← test_carbon_junction · test_ca_ext_runner ← e2e · check_method_discipline ← test_ca_ext_* · sdcp_gain_verdict ← check_method_discipline · cam_kinetics ← step4_dyn 경유 · `scripts/test_rint_r_chain.py` 의 직접 import 아님) · `scripts/test_rint_r_chain_e2e.py` | 22 |
| 고친 문서 (RR2-02 · 03 · Q7) · 설계 · 등록 · 명령 | `docs/reviews/rint2_rr_fix_evidence_20261023/q9_predict_units_design.md` · `docs/reviews/rint2_rr_fix_evidence_20261023/q9_time_budget.py` · `docs/reviews/rint2_rr_fix_evidence_20261023/q9_time_budget.json` · `docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md` · `docs/reviews/rint_carbon_additive_design_v1_20261020.md` · `docs/reviews/codex_rint2_rr_round2_request_20261103.md` · `docs/reviews/codex_rint2_rr_round1_request_20261024.md` · `docs/reviews/rint2_dev_probe_ledger_20261026.md` · `docs/reviews/rint2_kgy_commands_20261020.md` | 9 |

- 합 = repo/ 660 파일 (= 591 + pc12_fix/ 67 + req3_verify/ 2) + PIN.txt (핀 40 자리 + 가지 이름) + 맨 위 SHA256SUMS (모든 파일 · 자기 뺌) · ZIP 이름 = codex_rint2_rr_round3_<핀 앞 12 자리>.zip · 만드는 것 = 핀 push 뒤 메인 (git archive · 경로 = 이 표 · 푼 파일 blob = 핀 ls-tree 대조 · 다시 풀어 sha256 대조) · ZIP = 리포 밖 · litdb 카드 = 안 보냄.

## 2. 무엇이 바뀌었나 (`6917c3c9f` 뒤 · Rint ② 몫만)

| 커밋 | 무엇 | 보고 |
|---|---|---|
| `a69bf7d53` | 회차 ② 판정 반입 · 원장 verified 35 · 새 open 3 · 수정 계획 초안 | `docs/reviews/codex_rint2_rr_round2_evidence_20261105/README_import.md` |
| `933863e47` | 수정 계획 비준 기록 (Q1–Q7 (가)) · 같은 커밋 = 50kg | 수정 계획 머리 |
| `f5b00a838` | A1 RR2-01 · PC9-02 · 05 · A1b PC9-01 · A2 PC6-05 · PC9-04 · A2b PC9-03 · A3 RR2-02 · PC9-06 · A4 RR2-03 · PC9-07 · A5 Q7 (11-05 판 = 기계 교체로 유실 → 다시 만듦 · 여덟 커밋 = 한 커밋) | `docs/reviews/rint2_rr2_fix_evidence_20261105/REPORT.md` |
| `766e1e80c` | 사전 공격 10 PB-01–07 = PC10-01–07 · 원장 (RR2 · PC6-05 · PC9 claimed_fixed · PC10 등재) · 같은 커밋 = FAM · 후막 | `docs/reviews/rint2_rr2_fix_evidence_20261105/preattack10_fix/REPORT.md` |
| `342eff6e1` | 원장 PC10-01–07 claimed_fixed · S0 메모리 근거 측정 `docs/reviews/rint2_s0_mem_probe_20261106/` 3 파일 · 원장 SELF-157 (open · P3) · 같은 커밋 = /emod · LHS 대기 지문 | 원장 · `docs/reviews/rint2_s0_mem_probe_20261106/README.md` |
| `f47bde0f6` | S0 메모리 SELF-155 (`scripts/carbon_junction.py` · `scripts/ca_s0_census.py` + 시험) | `docs/reviews/rint2_s0_mem_fix_20261106/REPORT.md` |
| `6a81f0c55` | N1 · N2 · N4 (PC10-08–10) + 사전 공격 11 확장 (P2-A · P2-B · P3-5 · P3-6) · 원장 SELF-155 claimed_fixed | `docs/reviews/rint2_rr2_fix_evidence_20261105/pc10_n_fix/REPORT.md` · `docs/reviews/rint2_rr2_fix_evidence_20261105/pc10_n_fix/ext/REPORT_EXT.md` |
| `2b3c42c6c` | 서브 세션 인계 기록 (문서만) | `docs/handoff_to_subsession_20261108.md` |
| `d346ca943` | 사전 공격 12 PC12-01–05 고침 (작업 트리 에이전트 커밋 → cherry-pick -x · 코드 2 + 증거 67 = 69 파일 · 시험 먼저 · 1저자 11-08 (가)) | `docs/reviews/rint2_rr2_fix_evidence_20261105/pc12_fix/REPORT.md` |
| (이 커밋) | 이 요청서 (초안 = 작업 트리 가지 커밋 → cherry-pick -x → 여기서 §0 · §1 · §2 · §3 · §4 · §5 · §6 고침 = §5-1 끝) · 사전 공격 12 반입 (preattack12/) · 사전 공격 ① 독립 대조 반입 (req3_verify/) · 원장 (PC12-01–05 claimed_fixed · §5-1 끝 줄) · Codex ZIP 수령 기록 (`docs/collab/received/20261108_codex_mixer_lhs_followup/RECEIPT.md` · Rint ② 밖) · 진행 기록 | — |

- Rint ② 밖 = `504d84e52` · `cc1a96796` · `18bb6a2e4` · `70f7292e6` (Ⓐ · 50kg · FAM · `scripts/check_all.sh` 나누기 · /emod 정본 보탬) — ZIP 에 안 넣음.

## 3. finding → 고친 자리 → 시험 (수 = 그 파일 · E = docs/reviews/rint2_rr2_fix_evidence_20261105 · P10 = E/preattack10_fix · N = E/pc10_n_fix · X = N/ext · F12 = E/pc12_fix)

| finding | 커밋 | 고친 자리 (요지) | 시험 · 증거 |
|---|---|---|---|
| RR2-01 (P2) · PC9-02 · 05 | `f5b00a838` A1 | rc 판독 한 함수 rc_kind · rc_success · 소비자 (판독 함수 밖 rc 읽기 0 = RC01 원천 AST) · load_ladders 가 R_j,0 확인 팔 rc 를 읽음 | RC01–RC05 0/5 → 5/5 (E/logs/before_A1_RC.log → after_A1_RC.log) |
| PC9-01 (P2) | `f5b00a838` A1b | 끝 기록 원인 한 읽기 CHAIN_END_CAUSES · chain_cause_known | PE03u · CE01 · CE02 0/3 (E/logs/before_A1b_CE.log) → 고른 묶음 14/14 (after_A1b_targeted.log) |
| PC6-05 (P3) · PC9-04 | `f5b00a838` A2 | 런 로그 = (글, 상태) · read_regular_file (한 번 연 fd · 일반 파일) · ok 아니면 자격 False (런 전 TIME_LIMIT 만 예외) | LG01–LG03 0/3 (before_A2_LG.log) → 고른 묶음 34/34 (after_A2_targeted.log) · 행 보강 3/3 (after_A2_LG_rows2.log) |
| PC9-03 | `f5b00a838` A2b | 못 읽는 단계 요약 = summary_unreadable · 요약 원자적 쓰기 | SU01 · SU02 0/2 (before_A2b_SU.log) → 12/12 (after_A2b_SU.log) |
| RR2-02 (P3) · PC9-06 | `f5b00a838` A3 | Q9 설계 69 번째 줄 (1 줄) 의 두 어구 취소선 + 11-05 정정 문장 (현행 계약 · 파일의 취소선 줄 17 → 18) · 회차 ① · ② 요청서 표지 · q9_time_budget.py 낱말만 | 산식 출력 바이트 = 고치기 전 (E/logs/q9_time_budget_before.out = after.out) |
| RR2-03 (P3) · PC9-07 | `f5b00a838` A4 | 등록 R ⑫ = 코드 한정어 그대로 + Δ/λ 0.02–0.63 · q 0.4–19 · 설계 v1 · RINT2-L01 표지 | verify_rr2_03_quote ok (E/logs/verify_rr2_03_quote.out) · K01 · PC18 · PC20 · EP06 4/4 (E/logs/after_A4_doc_tests.log) |
| `f5b00a838` 회귀 | — | 시험한 판 = 커밋 blob (E/logs/code_sha256.txt) | 사슬 463/463 (E/logs/final_chain_full_py311.log) · 끝-끝 51 PASS · 0 FAIL · kgy 3.8.20 11 묶음 · 변이 40/40 (E/logs/mutation_rr2fix.out) · Codex 회차 ② 탐침 다시 310/311 (E/codex_probe_rerun/results.json · 다른 1 행 = known_PC6_05 = 고친 결과) |
| PC10-01 (P2) | `766e1e80c` | rc null 한 읽기 · GU 런 기록 없음 · 칸 없음 · 모르는 값 = 읽음 False | RN01 · RN02 + 기대 바뀐 다섯 3/10 → 10/10 (P10/logs/before_PB01.log → after_PB01.log) |
| PC10-02 · 03 · 04 · 06 | `766e1e80c` | 판정 입력 · 합치기 목록 못 읽는 요약 = Stop · FIFO = read_regular_file · RC01 허용 문맥 목록 · 런 전 TIME_LIMIT = 흔적 없을 때만 | SU03 · SU04 0/2 → 2/2 · FF01 0/1 → 1/1 · RC01 0/1 → 1/1 · 3/4 → 4/4 (P10/logs/before_PB0n.log → after_PB0n.log) |
| PC10-05 · 07 | `766e1e80c` | 문구 (주석 · 보고서) | — |
| `766e1e80c` 회귀 | — | 시험한 판 = 커밋 blob (P10/logs/code_sha256.txt) | 사슬 468/468 · 끝-끝 51/0 · kgy 11 묶음 · 변이 28/28 (P10/logs/mutation_pa10fix.out) · Codex 탐침 310/311 |
| PC10-08 · 09 (P2) | `6a81f0c55` | STOP_RUN_SHAPES · run_record_shape · stop_record_problem · run_exit_failed (생산자 꼴 표 = N/REPORT.md §1) · 같은 부류 end_record_known | CT01 91/150 → 0 · CT02 12/21 → 0 · CT04 4 → 0 (N/logs/count_bad_before.json → count_bad_after.json) · 기대 고친 기존 시험 합 73 (N/REPORT.md §3) |
| PC10-10 (P3) | `6a81f0c55` | rejected_record → result_recount · recover_ledger | CT03 6/10 → 0 (같은 두 파일) |
| PC11-01 (P2-A) | `6a81f0c55` | 시도 폴더 거부 기록 = 생산자 꼴일 때만 (rejected_in_folder) | CT05 28/31 → 0 (X/logs/count_bad_before.json → count_bad_after.json) |
| PC11-02 (P2-B) | `6a81f0c55` | stopped_record_problem — runs 마지막 · outdir 정확한 이름 · arms_read [] · GU = 끝 기록 확인 False | CT06 35/61 → 0 (중간 판 outdir 접두만 7/61 = X/logs/count_bad_prefix_only.json) · ⚠ GU 기록 rc 꼴 = 끝 기록 확인 True 고정물만 (§5-2 F2) |
| PC11-03 · 04 (P3) | `6a81f0c55` | summary_shape_problem = 그 폴더 Stop · 머리말 이름 정정 | CT07 8/9 → 0 · CT08 실패 → 통과 (같은 두 파일) |
| `6a81f0c55` 회귀 | — | 시험한 판 = 커밋 blob (X/logs/code_sha256.txt) | 사슬 476/476 (X/logs/final_chain_full_py311.log) · 끝-끝 51/0 · kgy 3.8.20 11 묶음 (X/logs/check_kgy_py38.out) · 변이 = 첫 판 26 중 25 (생존 K1 = 동등 · N/logs/mutation_pc10_K1c.out) · 확장 재실행 26 중 24 잡힘 · 생존 1 (K1) · 건너뜀 1 (X/logs/mutation_pc10_rerun.out) · 새 가드 36/36 (X/logs/mutation_pc10ext.out) · 사전 공격 11 14/14 (X/logs/mutation_pa11_rerun.out) · Codex 탐침 303/311 (X/codex_probe_rerun/results.json · §6 Q3) |
| SELF-155 (P2) | `f47bde0f6` | 근접 후보 = 조각 중점 · 좁은 반지름 · 덩어리 질의 (_self_pairs · S0 같은 꼴) · 시험한 blob 넷 = 커밋 blob | carbon_junction 547/547 · S0 186/0 · 새 시험 + 옛 구현 = 532/547 · 180/6 · 3.8 11 묶음 · 변이 7/7 · S0 끝-끝 킷 4 · npz 배열 41 중 다른 것 0 (`docs/reviews/rint2_s0_mem_fix_20261106/REPORT.md` §5 · §6 · §9 · 그 logs/) |
| PC12-01 (P2) | `d346ca943` | request_fields_problem + ARMS_RANGE · ARM_INDEX_RANGE (요청 칸 = 생산자 범위 arms 1–8 · arm_list 정렬 · 중복 없음 · 0–7 · 접두 아님 · 길이 = arms · 아니면 사유) · record_outdir 범위 밖 = '' · stop_trace = 기록의 outdir + 디스크의 &lt;런&gt; · &lt;런&gt;_arm* 전부 (옛 = od 하나) · result_fields 가 stop_trace 를 부름 (4883–4915 · 4061–4063 · 3786–3800 · 4358) | PC12A 27 행 (정직 9 · 함께 고침 13 · 옆 이름 1 · 실경로 4) 실패 16 → 0 (F12/logs/before_PC12.log → after_PC12.log · before/after_PC12_rows.json) · 탐침 다시 p1 True 12 줄 → 전부 False (F12/probe_rerun/after_p1_outdir_coedit.out) · p2 (1b) 실제 원장 resume rc 0 → rc 3 RESUME_NOT_ALLOWED |
| PC12-02 (P2) | `d346ca943` | chain_side · CHAIN_SIDE_SHAPES · STOP_CONFIRMED · chain_side_problem · rc_equal (판독 함수 · RC01 목록 등재) — 멈춘 런 기록 (group_cause, rc) ↔ 사슬 쪽 끝 기록 (원인 · rc · 확인) 생산자 대응표 (F12/REPORT.md §5) · 세 멈춤 코드 모두 (옛 = GU 의 확인 칸만) · chain_confirmed = 확인 칸 wrapper (4082–4155 · 3852–3856 · 4072–4078) | PC12B 33 행 (정직 15 · 모순 14 · 실경로 4) 실패 16 → 0 · 탐침 p2 (2b 한 칸 · 2c 두 칸) group_unconfirmed · True · rc 0 → False · rc 3 (F12/probe_rerun/after_p2_real_ledger.out) · p5 (c4) 선언 한정 닫힘 |
| PC12-03 (P2) | `d346ca943` | prior_runs_problem — 멈춘 런 앞의 런 기록 전부 = 끝난 런 (exit_ok + arms_read 비지 않음) · 런 기록 없는 TIME_LIMIT = runs 전부 · stop_record_problem 끝에서 부름 (4157–4175 · 4035) | PC12C 17 행 (정직 5 · 모순 8 · 실경로 4) 실패 10 → 0 · 탐침 p4 (TIME_LIMIT run L02_ceiling · zzz) timeout · True → False · rc 3 · p5 (a1 · a2) True → False (F12/probe_rerun/after_p4_tl_none_after_fail.out · after_p5_misc_b.out) |
| PC12-04 (P3) | `d346ca943` | read_summary_state = _json_strict (중복 칸 · NaN · ±Infinity = unreadable · 자격 False · 옛 = json.loads) (5759) | PC12D 10 행 실패 7 → 0 · 탐침 p5 (b) 중복 칸 요약 읽기 ok · 다시 셈 True → unreadable · summary_unreadable · False (F12/probe_rerun/after_p5_misc_b_fixed.out · 원 탐침은 None 첨자 Traceback = 고침의 효과) |
| PC12-05 (P3) | `d346ca943` | rejected_form_problem code ∈ STOPS (옛 = 글자 꼴만) (4410) · 고정물 AL12c 'rej' 멈춤 이름 'X' → MACHINE_NOT_ALLOWED (뜻 그대로) | PC12E 14 행 실패 9 → 0 · 탐침 p6 code XYZ · CALIBRATED rejected → Stop ATTEMPT_LEDGER_MISMATCH · GENERATION · OUTDIR_NOT_EMPTY = rejected 그대로 (한정 · F12/probe_rerun/after_p6_rejected.out) |
| `d346ca943` 회귀 | — | 시험한 판 = 커밋 blob (F12/logs/code_sha256.txt 끝 판 = `sha256sum scripts/rint_r_chain.py scripts/test_rint_r_chain.py` 48f0e7ff… · fedba635… 같음) | 사슬 476/476 (F12/logs/before_chain_full_py311.log) → 첫 전체 479/481 (고정물 AL12c · RC01 날 rc 읽기 셋 → 고침 · 겨냥 14/14) → 481/481 (F12/logs/after_chain_full_py311.log) · 끝-끝 51 PASS · 0 FAIL (after_e2e_py311.log) · first_result 9/9 · ca_ext_runner 151 PASS · 0 FAIL · kgy 3.8.20 11 묶음 (check_kgy_py38.out) · 변이 7/7 (mutation_pc12.json · 가드 하나 ↔ 검사 하나 · 무변이 5/5) · check_doc_refs 깨진 참조 0 |

## 4. 알려진 한정 (닫지 않는 것)

| 한정 | 출처 | 처분 |
|---|---|---|
| 런 기록 ↔ 그룹 끝 기록 교차 대조 없음 (원인 · rc · 확인 True · 남는 예 = 세 칸 손질 probe_rr S9 · 신호 경합 · 복사 런 · recover 끝 기록) | REPORT_EXT §8 · N/REPORT.md §8 | 한정 (Q-D 부류) · ⚠ 한 칸 꼴 F2 = §5-2 |
| 같은 이름 런 기록 둘 · 런 전 TIME_LIMIT 이름 차례 · 다른 칸 (copied_from · seconds · machine) 미검사 · 디스크 signal_after 받음 | REPORT_EXT §8 | 새 원장 PC11-05 · 06 · 07 · 08 (P3 · open) |
| 칸 없음 받음 (rc 칸 없음 = null · arms_read 칸 없음 = [] · 요청 칸 없는 기록 = outdir 접두만) · GU 확인 대조 = 읽힐 때만 · 경합 꼴 (원인 + 정수 rc) | REPORT_EXT §8 · N/REPORT.md §8 | 한정 |
| 거부 기록 utc 꼴 · cause 내용 · code 의 STOPS 소속 안 봄 · 흔적 다 지운 폴더 + 위조 기록 · 두 칸 이상 함께 바꾼 손 · .nfs* 부산물 = 흔적 (보수) | REPORT_EXT §8 | 한정 (Q-D) |
| 봉인 원천 런 (G01_&lt;런&gt;_a&lt;i&gt;) 중 신호 = runner_rc (안전 쪽) | E/REPORT.md §5 | PC9-08 wontfix |
| 원인 None + rc 0 + 잘못된 주소 · CUDA 낱말 로그 = by chain 끝난 런 ↔ recover runner_rc (보수 · 옛부터) · ResumeRunner._src_done = rc 0 만 · 원장 옛 결과 줄 = 다시 셈이 거부 (따로 시험 안 함) | P10/REPORT.md §6 · N/REPORT.md §8 | 그대로 |
| 실제 SIGKILL · flock 경쟁 · 비 root /proc · hidepid · GPU · NFS/FUSE · kgy 3.8.10 (시험 = 3.8.20) | 각 보고 한정 절 | Q5 현장 자격 |
| 열림 그대로: PC6-03 · 06 · PC7-06 · 07 · RINT2-T01 · RINT2-L01 | 원장 (회차 ② 답) | open |
| S0 실침대 peak RSS · 시간 = 미측정 · 예외 ② 꼴의 실침대 존재 = 미확인 · _cand_pairs 긴 꼬리 잔여 위험 · 11-06 실측 1,356 s 의 6.96 GB 튐 = 원인 미확인 | S0 REPORT §4 · §10 | kgy 재실행 (0 건) |
| `6a81f0c55` 회귀 수 = 반입 전 작업 트리 (바탕 `766e1e80c` · S0 고침 전 carbon_junction) · 합친 판 게이트 기록 = 리포에 없음 (미확인) | REPORT_EXT §5 | ⬜ 메인 |
| PC12 고침 한정 — 요청 칸 없는 기록 (arms 칸 없음 = 시험 고정물 꼴) 은 outdir 접두 규칙만 (흔적 있는 옆 이름은 막힘 · 흔적 없는 옆 이름 자체는 받음) · 옆 이름 폴더가 있다는 사실 자체 = 모순 아님 · 사슬 쪽 끝 기록 없음 (그룹 기록 없는 GU · c2) · 시작 기록에 결합 안 됨 · chain_end 없는 옛 recover 끝 기록 = 대조 안 함 · 런 전 TIME_LIMIT 의 run 이름 차례 안 봄 ('zzz' 는 앞 런 실패 규칙으로만) · 1e400 같은 큰 수 리터럴 = inf 로 읽힘 (칸 꼴 검사가 따로) · STOPS 안이지만 풀기 전 자리에서 생산자가 쓰지 않는 이름 (GENERATION · ARM_* · OUTDIR_NOT_EMPTY) 받음 · 같은 이름 런 기록 둘 · 다른 칸 (copied_from · seconds · machine …) · utc 글 꼴 = 그대로 | F12/REPORT.md §6 | 한정 (Q3) |
| PC12 고침으로 범위가 바뀐 것 (모두 자격 없음 쪽 · 생산자 꼴 아님): ① TIME_LIMIT · RUNNER_RC 멈춤인데 그 런 끝 기록의 사슬 쪽 확인 False (또는 원인 · rc 어긋남) = 자격 없음 (옛 = GU 만) ② 앞 런 기록 exit_ok 인데 arms_read 빈 목록 · 꼴 틀림 · group_cause 칸 없음 = 모순 (10-27 묶음 C1b 전 옛 요약 = 그 뒤 멈춤이 자격 없음으로 읽힘 · 그런 요약에 자격을 준 적 없음) ③ 요약 있는 길에서 디스크 끝 기록 원인 'signal_after' = 런 기록 killed:signal_after 와 모순 (생산자 디스크 원인 = None · 요약 없는 길 orphan_cause · A1b 는 안 바꿈) ④ 단계 요약 중복 칸 · NaN · ±Infinity = unreadable (옛 = 읽음 · 생산자 바이트에는 없음) | F12/REPORT.md §6 | Q3 (기대 변경으로 받는가) |
| PC12 시험 = 합성 · 가짜 러너 · 실제 git 원장 · 이 컨테이너 (실제 kgy 3.8.10 · ibb · GPU 아님) · 웹앱 화면 없음 (재실행 자격 · resume_ok · 원장 · 멈춤 사유를 보이는 화면 = grep 0) · 고친 가드에 대한 독립 재공격 = 없음 | F12/REPORT.md 머리 · §6 | Q5 현장 자격 · 웹앱 = "없음" 기록 · Codex 반례 (Q3) |

## 5. 사전 공격 리뷰 (CLAUDE.md ①–④)

- 사전 공격 ① 독립 대조 (11-08 · 읽기 전용 에이전트 · 대상 = 초안 커밋 e540c73fe (작업 트리 가지 · push 안 됨 · 이 커밋에 cherry-pick) 의 이 요청서) = **같음 81 · 다름 1 · 미확인 4** (표 86 행) · 보고 `docs/reviews/rint2_rr2_fix_evidence_20261105/req3_verify/REPORT.md` — 다름 1 = §5-2 F1 "함께 고침 11 가지" (실제 = RUNNER_RC 10 + TIME_LIMIT 2 · True 12 줄) · 미확인 4 = 리뷰 핀 push · "(판정문 §9 · 0 건)" 의 부재 · ZIP · PIN.txt · 검사기 rc (리포 밖) · 과장 · 모호 5 = 이 커밋에서 좁힘 (§5-1 둘째 불릿).

### 5-1. ① 숫자 · 전칭 ↔ 출처 (11-08 · 이 작업 트리 · 이 대조로 고친 것 = 표 아래)

| 주장 | 출처 · 명령 | 결과 |
|---|---|---|
| 커밋 번호 (이 파일의 백틱 SHA 12 개) | `git rev-list HEAD` 와 접두 대조 | 12 / 12 조상 · 유일 접두 |
| stoic 동결 `6a81f0c55` | `git rev-parse origin/claude/stoic-knuth-NObVQ` | 같음 |
| 회차 ② HOLD · P1 0 · P2 1 · P3 2 · 핀 `6917c3c9f` · verified 35 | 판정문 머리 · `docs/reviews/codex_rint2_rr_round2_evidence_20261105/README_import.md` 원장 표 | 같음 |
| 폴더 수 84 · 307 · 156 · 3 · SHA256SUMS 287 · 68 · 143 · 16 · 155 · 2 | `find <폴더> -type f` · `wc -l SHA256SUMS` · 폴더마다 `sha256sum -c` | 같음 · -c 통과 |
| 의존 22 = diff 0 · 바뀐 6 | `git diff --stat 6917c3c9f HEAD -- <파일>` | 빈 출력 · 6 파일 |
| CODE_FILES 302 줄 · 19 | `grep -n CODE_FILES scripts/rint_r_chain.py` | 같음 |
| §3 의 수 (전 → 뒤 · 회귀 · 변이 · 탐침) | 그 행의 로그 끝 줄 · count_bad JSON · results.json passed/total | 같음 |
| 시험한 판 = 커밋 blob (넷) | `git show <커밋>:<파일> \| sha256sum` ↔ code_sha256.txt · tested_code_blobs.txt | 같음 |
| Codex 탐침 "무변경" | probe_runtime.py sha256 ↔ E/rerun_codex_probe.py PROBE_SHA | 같음 |
| PC12 줄 번호 (4000 · 4021 · 4027–4033 · 4037 · 4044–4069 · 4303 · 4773 · 5625) = 고치기 전 `6a81f0c55` 판 | `awk 'NR==n' scripts/rint_r_chain.py` (초안 때) | 같음 · ⚠ 핀의 파일은 `d346ca943` 에서 바뀜 → 고친 자리 줄 = §3 PC12 행 (F12/REPORT.md §1) |
| 원장 997 → 1011 · open 336 → 343 · claimed_fixed 371 → 378 · verified 279 · wontfix 11 (초안) → 이 커밋 = 1011 · open 338 · claimed_fixed 383 · verified 279 · wontfix 11 (PC12-01–05 open → claimed_fixed) | `python3 scripts/check_review_findings.py` (앞 · 뒤 · 이 커밋) | rc 0 |
| 합친 판 게이트 (`6a81f0c55`) | 리포 기록 찾기 (진행 기록 · 인계) | 없음 → §4 "미확인" |

- 이 대조로 고친 것 = 원장 PC10-10 메모 (N4 줄에 옮겨 적힌 N1 · N2 권고 글 → 정정 표지) · §2 `f5b00a838` 행 (PC9-02 · 05 빠짐) · 진행 기록 줄 (② ③ = 메인 몫 → 사전 공격 12 로 채움) · 확인 못 한 것 = 합친 판 게이트 (§4).
- 독립 대조 (req3_verify · 위) 로 이 커밋에서 좁힌 것 = §5-2 F1 "함께 고침 11 가지" → RUNNER_RC 10 + TIME_LIMIT 2 (True 12 줄) · §3 RR2-02 "69 줄" → 69 번째 줄 (1 줄) · §1 "시험 import 다섯" → 간접 import · §2 `342eff6e1` 행 (rint2_s0_mem_probe 3 파일 · SELF-157) · §3 `6a81f0c55` 회귀 행 (확장 재실행 24 · 1 · 1 병기) · §0 ③ "(판정문 §9 · 0 건)" → 항목 출처 = 수정 계획 Q5 · 미확인 4 = 그대로 (리포 밖 · push 뒤 PIN.txt · 진행 기록에 적음).
- 원장 이 커밋 = PC10-08 · 09 · 10 → claimed_fixed `6a81f0c55` · 새 PC11-01–04 claimed_fixed `6a81f0c55` · 새 PC11-05–08 open (한정) · 새 PC12-01–05 → **claimed_fixed `d346ca943`** (처분 (가) · 시험 PC12A–E · 한정 메모 · 11 가지 정정 메모) · SELF-158 open (정정 문장 = §5-2 · claimed_fixed 는 이 커밋 push 뒤 다음 원장 커밋) · PC11-02 메모 (범위 좁힘) · PC10-10 메모 정정.

### 5-2. ② ③ 사전 공격 12 (11-08 · 독립 · diff 만 · 대상 = `6a81f0c55` 의 `scripts/rint_r_chain.py` 새 가드 · 보고 `docs/reviews/rint2_rr2_fix_evidence_20261105/preattack12/REPORT.md` · 탐침 · 출력 = 같은 폴더 · SHA256SUMS 16 — 고침 = §5-3)

- 결과 = **P1 0 · P2 3 · P3 2 · 거짓 fail-closed 못 찾음** (생산자 꼴 = 받음) · 버틴 것 = 요약 꼴 무작위 30,000 의 Stop 아닌 예외 0 (p3_fuzz_shapes.out) · 거부 기록 형 · 중복 칸 · BOM · inf 등 = Stop (p6_rejected.out) · 줄 = 고치기 전 판 (초안 핀 `2b3c42c6c` 의 파일 = `6a81f0c55` 와 같음 · 고친 자리 = §3 PC12 행).

| # | 무엇이 무엇을 받나 | 함수 · 줄 | 탐침 (P = 그 폴더) |
|---|---|---|---|
| F1 · PC12-01 (P2) | outdir 와 요청 칸 (arms · arm_list) 을 함께 고친 멈춘 런 기록 = 재실행 자격 (RUNNER_RC 함께 고침 10 가지 전부 True (+ TIME_LIMIT 2 가지 · True 12 줄 · P/p1_outdir_coedit.out · preattack12/REPORT.md 와 pc12_fix/REPORT.md §4 의 "11 가지" = 옮겨 적은 수 · 봉인 폴더라 글은 그대로 두고 여기서 정정) · 범위 밖 arms 9 · 0 · −1 · 10**30 · arm_list [] · [0] · [9] · [3,3] · [3,1] · 범위 안 arms 2 도 · 실제 원장 --add --resume rc 0) | stopped_record_problem ② 4027–4033 · record_outdir 4773 | P/p1_outdir_coedit.py · P/p2_real_ledger.py (1b) |
| F2 · PC12-02 (P2) | 정직 GU (러너 rc 1 · 끝 기록 확인 False → recover chain_end rc 1) 의 요약 런 기록 rc 1 → 0 **한 칸** = group_unconfirmed · 재실행 자격 · rc 0 ({timeout · null} 두 칸도) | chain_confirmed 4044–4069 · 4037 | P/p2_real_ledger.py (2a · 2b · 2c) |
| F3 · PC12-03 (P2) | 정직 RUNNER_RC L01 rc 1 의 stop 두 칸 (code TIME_LIMIT · run = 다음 이름 L02_ceiling 또는 zzz) = timeout · 재실행 자격 · rc 0 → 재실행이 rc 1 런을 다시 돈다 (F3b = 앞 기록 exit_ok 안 봄) | stop_record_problem 4000 · stopped_record_problem 4021 | P/p4_tl_none_after_fail.py · P/p5_misc_b.py (a1 · a2) |
| F4 · PC12-04 (P3) | 단계 요약 중복 칸 · NaN (느슨한 json.loads) → 코드 = 뒤 값 (F1 이 겉보기 정직한 기록으로) | read_summary_state 5625 | P/p5_misc_b.py (b) |
| F5 · PC12-05 (P3) | 시도 폴더 거부 기록 code = 글자 꼴만 (XYZ · CALIBRATED · GENERATION · OUTDIR_NOT_EMPTY = rejected · 표시만) | rejected_form_problem 4303 | P/p6_rejected.py |

- **F2 = 과장 확인** — `6a81f0c55` 커밋 글 (★ 확장 P2-B 「옛 = 한 칸 손질 넷 (… · GU 기록 rc) …」 · ★ 문구 정정 「… 한 칸 손질 넷이 있었다 · 이번에 닫음」) 과 N/REPORT.md §8 「… 그 넷 (+ 옆 이름 outdir) 을 닫음」 은 GU 기록 rc 꼴에서 과장이다 — CT06 S2_forged_GU_rc0 는 끝 기록 CHAIN_OK1 (by chain · 확인 True = GU 생산자가 남기지 않는 꼴) 위에서만 시험됐다 (원장 SELF-158 · PC11-02 메모로 좁힘 · 상태 claimed_fixed 그대로 = 원 반례 꼴만).
- 한정과의 관계 — F1 · F3 = 두 칸 함께 고친 꼴이라 선언 한정 (일관 편집 Q-D · 런 기록 ↔ 끝 기록 교차 대조) 에 일부 걸린다 (F1 의 요청 칸 범위 · 흔적 범위 · F3 의 runs · 앞 기록 무시는 한정 글에 없음) · **F2 = 한 칸 손질이라 선언 한정에 안 걸린다** · F5 = REPORT_EXT §8 에 이미 한정 ("code 의 STOPS 소속 안 봄").
- 처분 = ✅ **(가) 고침** (1저자 11-08 *"권고대로"*) · 커밋 `d346ca943` · 증거 `docs/reviews/rint2_rr2_fix_evidence_20261105/pc12_fix/REPORT.md` · 시험 먼저 PC12A–E 0/5 → 5/5 · 사슬 476/476 → 481/481 · 끝-끝 51 PASS · 0 FAIL · 변이 7/7 · 탐침 재실행 = F1–F5 위조 행 거부 (p1 True 12 줄 → 0 · p2 (1b · 2b · 2c) rc 0 → rc 3 RESUME_NOT_ALLOWED · p4 · p5 (a1 · a2 · c1 · c4) True → False · p5 (b) 읽기 ok → unreadable · p6 XYZ · CALIBRATED → Stop) · 정직 꼴 변화 0 (p1 정직 · p2 (1a · 1c · 2a) · p4 정직 · p5 (c2 · c3) · p6 생산자 꼴 = 바탕 값 그대로) · 3.8 11 묶음 · 웹앱 화면 없음 · 원장 PC12-01–05 claimed_fixed = 이 커밋 · 한정 = §4 (pc12_fix/REPORT.md §6) · 리뷰어 권고 ①–⑤ = 전부 반영 (§5-3).

### 5-3. 사전 공격 12 고침 뒤 (`d346ca943` · F12 = `docs/reviews/rint2_rr2_fix_evidence_20261105/pc12_fix/` · 1저자 11-06 규칙 = 생산자가 쓰지 않는 칸 조합 = 모순 = 재실행 자격 없음 · 정직 (생산자 꼴) 기록의 판정은 그대로)

- 가드가 이제 보는 것 (F12/REPORT.md §0 · §1): **F1** 멈춘 런 기록의 요청 칸 (arms · arm_list) 은 생산자 범위 (arms 1–8 · arm_list 정렬 · 중복 없음 · 0–7 · 접두 아님 · 길이 = arms) 아니면 사유 (`request_fields_problem` · `ARMS_RANGE` · `ARM_INDEX_RANGE` · `record_outdir` 범위 밖 = '') · 검사 실패 흔적은 기록의 outdir + 디스크의 &lt;런&gt; · &lt;런&gt;_arm* 폴더 **전부** 에서 (`stop_trace` · 폴더 못 읽음 = 흔적 있음 · 옛 = od 하나) · **F2** 멈춘 런 기록 꼴 (group_cause, rc) ↔ 사슬 쪽 끝 기록 (by chain 끝 기록 · recover 의 chain_end) 의 (원인 · rc · 확인) 을 생산자 대응표로 대조 (`chain_side` · `CHAIN_SIDE_SHAPES` · `STOP_CONFIRMED` · `chain_side_problem` · rc 같음 = 판독 함수 `rc_equal` · RC01 목록 등재 · 세 멈춤 코드 모두 · 옛 = GU 의 확인 칸만) · **F3** 멈춘 런 **앞** 의 런 기록 전부 = 끝난 런 (exit_ok + arms_read 비지 않음 · `prior_runs_problem` · 런 기록 없는 TIME_LIMIT 은 runs 전부) · **F4** 결과 줄 길의 단계 요약 읽기 = `_json_strict` (중복 칸 · NaN · ±Infinity = unreadable · 자격 False) · **F5** 거부 기록 code ∈ `STOPS`.
- 생산자 대응표 = F12/REPORT.md §5 (코드 = `CHAIN_SIDE_SHAPES` 4123 · `STOP_CONFIRMED` 4127 · `rc_equal` 3852 · 근거 줄 = `Runner._execute` 4974–4988 · `run_in_group` 2778–2800 · `recover_group` 7530 · 7582 · F3 = `ResumeRunner._copy` 5071 · 5079 · `MergeFetch` 6397 · 6415 · F1 = `run_request` 4861–4863 · 러너 `scripts/sdcp_gain_vox015_8arm.sh` 46–63 · 73–76 · `Runner._prepare` 4955 · F4 = `write_summary` → `canon_bytes` + `_clean` = 정직 요약에 중복 칸 · NaN 없음) — killed:signal_after 의 디스크 원인 = None · rc = 러너 스스로의 wait 값 · 확인 False ⇒ GROUP_UNCONFIRMED 먼저 · TIME_LIMIT · RUNNER_RC = 확인 True 뒤에만.
- 수 (F12/REPORT.md §2 – §4): 새 시험 PC12A–E = 바탕 0/5 (실패 행 = 위조 · 함께 고침 행만 A 16 · B 16 · C 10 · D 7 · E 9 · 정직 행 전부 통과) → 5/5 · 사슬 476/476 → 첫 전체 479/481 (고정물 AL12c code 'X' · RC01 날 rc 읽기 셋) → 고정물 · `rc_equal` 고침 → 481/481 · 끝-끝 51 PASS · 0 FAIL · first_result 9/9 · ca_ext_runner 151 PASS · 0 FAIL · kgy 판 3.8.20 11 묶음 · 변이 7/7 (가드 하나 ↔ 검사 하나 · 무변이 5/5) · 탐침 재실행 (원본 그대로 · 하네스만 작업 트리) = 위조 행 전부 자격 없음 · 정직 행 그대로 · 선언 한정 c1 · c4 도 닫힘 · c2 유지 · 시험한 판 = 커밋 blob (F12/logs/code_sha256.txt 끝 판 = `sha256sum scripts/rint_r_chain.py scripts/test_rint_r_chain.py` 48f0e7ff… · fedba635…).
- 한정 (F12/REPORT.md §6 그대로): 요청 칸 없는 기록 (arms 칸 없음 = 시험 고정물 꼴) 은 outdir 접두 규칙만 (그대로) — 흔적은 이제 그 런 폴더 전부에서 보므로 흔적 있는 옆 이름은 막힌다 (c1) · 흔적 없는 옆 이름 자체는 받는다 · 디스크에 그 런의 다른 출력 폴더 (옆 이름) 가 있다는 사실 자체는 모순으로 세지 않는다 (흔적 없으면 받음) · 사슬 쪽 끝 기록이 없거나 (그룹 기록 없는 GU · c2) · 시작 기록에 결합 안 됨 · chain_end 없는 옛 recover 끝 기록 = 대조 안 함 (옛 그대로) · 런 전 TIME_LIMIT 의 run 이름 차례 (다음 이름인지) 는 보지 않는다 — 'zzz' 는 앞 런 실패 규칙으로만 막혔다 (앞 런이 정직하게 끝난 뒤 'zzz' = 받음) · F4: 1e400 같은 큰 수 리터럴은 inf 로 읽힌다 (`_json_strict` = NaN · Infinity 상수 · 중복 칸만) — 읽는 칸의 꼴 검사가 따로 막는다 · F5: `STOPS` 안이지만 풀기 전 자리에서 생산자가 쓰지 않는 이름 (GENERATION · ARM_* 등 결과 뒤 멈춤 · OUTDIR_NOT_EMPTY 옆 기록 전용) 은 받는다 — 풀기 전 코드 집합은 열거하지 않았다 (`attempt_open` 의 Stop 전부) · 같은 이름 런 기록 둘 · 다른 칸 (copied_from · seconds · machine …) · utc 글 꼴 = 그대로 · 범위가 바뀐 것 (모두 자격 없음 쪽 · 생산자 꼴 아님) ①–④ = §4 · 시험 = 합성 · 가짜 러너 · 실제 git 원장 · 이 컨테이너 — 실제 kgy 3.8.10 · ibb · GPU 아님 · 웹앱 화면 없음 · 고친 가드에 대한 독립 재공격 = 없음 (§0 ⑥).

### 5-4. ④ 닫는 것 / 닫지 않는 것 = §0.

## 6. 판정 요청 질문

| # | 질문 |
|---|---|
| Q1 | §3 의 finding 마다 닫힘 / 부분 / 열림 — RR2-01 · 02 · 03 · PC6-05 · PC6-13 · PC9-01–07 · PC10-01–10 · PC11-01–04 · PC12-01–05 · SELF-155 (최소 해결 ↔ 고친 자리 · 회차 ② 반례 재실행 · 사전 공격 12 탐침 재실행 = F12/probe_rerun/). |
| Q2 | 1저자 11-06 규칙 (생산자가 쓰지 않는 칸 조합 = 모순 = 재실행 자격 없음 · 읽음 False) 과 생산자 꼴 표 (N/REPORT.md §1 · REPORT_EXT §1) 가 재개 정책 HOLD 를 푸는 근거로 충분한가 — 정상 생산자 꼴 행 변화 0 (N/logs/rows_diff_summary.json · X/logs/rows_diff_summary.json) · 끝-끝 51 포함. |
| Q3 | Codex 회차 ② 탐침 무변경 다시 = 303/311 — 다른 8 행 = known_PC6_05 (고친 결과) + summary_&lt;7&gt;_TIME_LIMIT_None (고정물 TIME_LIMIT + {rc null · group_cause null} = 생산자 꼴 아님 → N1 조항 runner_rc · resource · 자격 False) — 이 기대 변경을 받는가 · PC12 고침 (`d346ca943` · §5-3) 이 같은 부류 (요청 칸 범위 · 끝 기록 대조 · 앞 런 정상 종료 · 엄격 JSON · STOPS) 를 닫는가 · 한정 목록 (§4 · pc12_fix/REPORT.md §6) 에 빠진 것이 있나 · 범위가 바뀐 넷 (§4 ①–④ · 모두 자격 없음 쪽) 을 기대 변경으로 받는가. |
| Q4 | 한정 (§4 · PC11-05–08 · 교차 대조 없음) 중 봉인 전에 막아야 할 것이 있는가. |
| Q5 | S0 메모리 고침 — 선언된 예외 둘 (정준 동률 순서 · 옛 판이 놓친 경계 참 쌍) · CP-ORD 섞는 자리 옮김 · S0 계획 해시 바뀜 (도구 sha) 을 회차 ② §8 Q8 칸 (S0 REPORT §11) 으로 받는가 · kgy 재실행 채택 조건 (S0 REPORT §12 · rc 0 + 출력 여섯) 이 충분한가. |
| Q6 | 이 회차 뒤 남는 것이 "Q5 현장 자격 + kgy S0 단계 1 + 12 단위 끝-끝 (수정 계획 Q6) + 봉인" 이라고 볼 수 있는가 — 판정 꼴 "코드 · 설계 · 문서 GO (재개 정책 포함) + 봉인 전 확인" 으로 줄 수 있는가. |

## 7. 묻지 않는 것

- 등록 R 캠페인 GO · R 런 · 정량 판정 · 생산 GO · 숫자 칸의 값 · ⑦ SBE 탐침 (봉인 뒤).
- 회차 ② 에서 verified 된 35 의 다시 판정 (회귀가 깨졌을 때만) · 빠진 물리 (v0 동결 · 회차 ② 요청서 §6) · 다음 트랙 설계.
- Rint ② 밖 트랙 (50kg · LHS · 믹서 · FAM · 웹앱 /emod · 후막).
