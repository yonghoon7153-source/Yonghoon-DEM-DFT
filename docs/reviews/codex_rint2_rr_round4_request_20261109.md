# Codex 회차 ④ 짧은 재확인 요청 — Rint ② 회차 ③ (11-08) RR3-01 · RR3-02 고침 · 사전 공격 13 · 14 고침 (2026-11-09 · 사전 공격 ① 반영 · 발송 = 1저자)

> **한 줄**: Codex 회차 ③ (`docs/reviews/codex_review_rint2_rr_round3_20261108.md` · 리뷰 핀 `17d45fb9c` · HOLD · 새 P1 0 · P2 1 · P3 1 · PC12-03 부분 · SELF-155 부분) 의 RR3-01 (P2) · RR3-02 (P3) 를 `742a3b83f` 에서 고쳤고, 그 고침을 사전 공격 13 회차 (독립 · diff 만) 로 다시 깨서 나온 P2 둘 · P3 하나를 `7a582acf5` 에서, 그 고침을 사전 공격 14 회차로 다시 깨서 나온 P3 넷을 `576953afd` 에서 고쳤다.  §3 의 고침이 RR3-01 과 그 같은 부류 (앞 런 판독 완료 · 재개 자격을 여는 요약 손질) 를 닫는지 · PC12-03 을 함께 닫는지 · 재개 정책 HOLD 를 풀 수 있는지만 본다 (판정문 §5 ① ② · §7).
> **리뷰 핀** = 이 요청서가 든 커밋 (작업 가지 B `claude/sdcp-dem-manuscript-si-pqwtv8` · push · stoic `claude/stoic-knuth-NObVQ` = 복귀 전까지 `6a81f0c55` 에서 동결 · 복귀 = stoic 을 B 끝으로 fast-forward) · 번호 = ZIP 의 PIN.txt (이 파일은 그 커밋 안이라 제 번호를 못 적는다) · **비교 기준** = `17d45fb9c` (회차 ③ 리뷰 핀 · B) — 그 사이 Rint ② 밖 커밋 (Codex 비 Rint 반입 · 믹서 · LHS) 이 섞임 · Rint ② 범위 = §2.
> **1저자** — 11-08 *"권고대로"* (수정 계획 `docs/reviews/rint2_rr3_fix_plan_20261108.md` §6 Q1–Q7 = (가)) · 11-09 *"다 권고대로 해줘 물어보지말고"* (사전 공격 13 · 14 처분 = Codex 전에 고침 · 선언 한정 · 이 요청서) · 발송 = 1저자.

## 0. 이번에 닫는 것 / 닫지 않는 것

| 이번에 닫으려는 것 (판정 요청) | 닫지 않는 것 (이 회차 범위 밖) |
|---|---|
| ① RR3-01 (P2) — 앞 런 판독 완료 = `ARM_PUBLIC` 구조 계약 (생성 `arms_read_record` · 분류 `arms_read_kind` · 소비 `prior_runs_problem` · 생산자 셋) — `742a3b83f` · 같은 부류 PC12-03 (회차 ③ 부분 → RR3-01 과 함께 · 수정 계획 Q3 (가)) | SELF-155 실침대 (kgy S0 단계 1 재실행 · 0 건 · 채택 조건 = 수정 계획 §8) |
| ② RR3-02 (P3) — 회차 ③ 요청서 제자리 정정 (취소선 + "11-08 정정 (RR3-02)" · 판정문 §2 rg 한 줄에 걸린 줄) — `742a3b83f` | 봉인 전 확인 ③ ④ (수정 계획 §7 · 봉인 때 실제 계획 · 시도 기록 대조) · PC11-05–08 (open · 한정 · 판정문 §5 ③) |
| ③ 사전 공격 13 PC13-01 (P2 · RESUME_MISMATCH 요약의 두 칸 손질 = 재실행 자격) · PC13-02 (P2 · 판독 완료 판정이 `ARM_PUBLIC` 값을 안 봄) · PC13-04 (P3 · `read_run` 킷 앞자리 식 사본) — `7a582acf5` | PC13-03 (P3 · 앞 런 기록 완결성 대조 없음 · 선언 한정 · §4) |
| ④ 사전 공격 14 PC14-01 (P3 · 값 검사 앞 넘침 크래시 · `7a582acf5` 회귀) · PC14-04 (P3 · 생산자가 안 쓰는 값 꼴) · PC14-05 (P3 · resume 칸 집합) · PC14-06 (P3 · 변이 생존 넷 = 시험 빈틈) — `576953afd` | PC14-02 (P3 · 원천 있는 재실행 시도의 복사 / 새 런 경계 다시 적기) · PC14-03 (P3 · resume.from ↔ 원장 사슬 끝 · attempt.json resume_of ↔ 원장 항목) = 선언 한정 (§4 · 봉인 전 확인 ③) |
| ⑤ SELF-158 (P3 · 사전 공격 11 P2-B 닫음 과장) — 정정 문장 = 회차 ③ 요청서 §5-2 (`17d45fb9c`) · 문장 확인만 | 현장 자격 (프로세스 · 잠금 · 권한 · 파일 시스템 · FIFO · NFS) · 12 단위 끝-끝 (수정 계획 Q6) · 봉인 (숫자 칸 · 실행 정책 · S0 / R 계획 해시) · S0 단계 2 · R 런 · 정량 판정 · 생산 GO · 빠진 물리 (v0 동결) · ⑦ SBE 탐침 (0 건) |

## 1. 보내는 것 (ZIP · repo/ = 리뷰 핀 blob 그대로 + PIN.txt)

| 묶음 | 파일 | 수 |
|---|---|---|
| 이 요청서 | `docs/reviews/codex_rint2_rr_round4_request_20261109.md` | 1 |
| 회차 ③ 판정 · 반입 · 수정 계획 · 회차 ③ 요청서 (RR3-02 정정 자리) | `docs/reviews/codex_review_rint2_rr_round3_20261108.md` · `docs/reviews/codex_rint2_rr_round3_evidence_20261108/` (우리 트리 재현 `_repro_ours_20261108/` 포함 · SHA256SUMS 110) · `docs/reviews/rint2_rr3_fix_plan_20261108.md` (§6 Q1–Q7 · §7 봉인 전 확인 · §8 kgy 채택 조건 · §9 RR3 실행 기록 · §10 · §11 사전 공격 처분) · `docs/reviews/codex_rint2_rr_round3_request_20261108.md` | 1 + 111 + 1 + 1 |
| 고침 증거 (E = `docs/reviews/rint2_rr2_fix_evidence_20261105`) | `docs/reviews/rint2_rr2_fix_evidence_20261105/rr3_fix/` (RR3 · 57 파일 · 보고 `docs/reviews/rint2_rr2_fix_evidence_20261105/rr3_fix/REPORT.md`) · `docs/reviews/rint2_rr2_fix_evidence_20261105/preattack13/` (37 · `docs/reviews/rint2_rr2_fix_evidence_20261105/preattack13/REPORT.md`) · `docs/reviews/rint2_rr2_fix_evidence_20261105/pa13_fix/` (68 · `docs/reviews/rint2_rr2_fix_evidence_20261105/pa13_fix/REPORT.md`) · `docs/reviews/rint2_rr2_fix_evidence_20261105/preattack14/` (26 · `docs/reviews/rint2_rr2_fix_evidence_20261105/preattack14/REPORT.md`) · `docs/reviews/rint2_rr2_fix_evidence_20261105/pa14_fix/` (71 · `docs/reviews/rint2_rr2_fix_evidence_20261105/pa14_fix/REPORT.md`) · 폴더마다 SHA256SUMS (자기 뺌) | 259 |
| 원장 | `docs/reviews/findings.json` | 1 |
| 바뀐 Rint ② 코드 · 시험 (`17d45fb9c` → 핀) | `scripts/rint_r_chain.py` · `scripts/test_rint_r_chain.py` (`git diff --stat 17d45fb9c <핀> -- scripts/` 의 나머지 9 = 믹서 생성기 · 판독 · 관측 · 시험 + 게이트 `scripts/check_all.sh` 에 믹서 시험 세 줄 = Rint ② 밖) | 2 |
| 실행 의존 (`17d45fb9c` 와 diff 0) | 사슬 CODE_FILES (`scripts/rint_r_chain.py` 319 줄 · 19) 의 나머지 18 · 간접 import 다섯 (`scripts/cam_kinetics.py` · `scripts/check_method_discipline.py` · `scripts/sdcp_gain_verdict.py` · `scripts/test_ca_ext_b6.py` · `scripts/test_ca_ext_runner.py`) · 끝-끝 `scripts/test_rint_r_chain_e2e.py` · 회차 ③ 에 보낸 시험 둘 (`scripts/test_carbon_junction.py` · `scripts/test_ca_s0_census.py`) | 26 |

- 합 = repo/ 403 파일 + PIN.txt (핀 40 자리 + 가지 이름) + 맨 위 SHA256SUMS (모든 파일 · 자기 뺌) · ZIP 이름 = codex_rint2_rr_round4_<핀 앞 12 자리>.zip · 만드는 것 = 핀 push 뒤 메인 (git archive · 경로 = 이 표 · 푼 파일 blob = 핀 ls-tree 대조 · 다시 풀어 sha256 대조) · ZIP = 리포 밖 · litdb 카드 = 안 보냄 · 회차 ③ 에 보낸 E 폴더의 옛 묶음 (RR2 · 사전 공격 9–12 · pc12_fix · req3_verify) · S0 메모리 폴더 = 바뀌지 않아 안 보냄 (회차 ③ ZIP 그대로).

## 2. 무엇이 바뀌었나 (`17d45fb9c` 뒤 · Rint ② 몫만)

| 커밋 | 무엇 | 보고 |
|---|---|---|
| `40d9658c0` | 회차 ③ 판정 반입 · 우리 트리 재현 (판정값 차이 0) · 원장 (닫힘 30 → verified · PC12-03 · SELF-155 = claimed_fixed 그대로 + 메모 · PC11-05–08 = open + 메모 · 새 open RR3-01 · RR3-02) · 수정 계획 초안 | `docs/reviews/codex_rint2_rr_round3_evidence_20261108/README_import.md` |
| `742a3b83f` | RR3-01 고침 (구조 계약 · 시험 먼저) · RR3-02 요청서 정정 · 봉인 전 확인 목록 (§7) · kgy S0 채택 조건 (§8) · 1저자 11-08 Q1–Q7 (가) | 수정 계획 §9 · `docs/reviews/rint2_rr2_fix_evidence_20261105/rr3_fix/REPORT.md` (11-09 소급 작성 · 숫자 = 그 폴더 로그) |
| `7a582acf5` | 사전 공격 13 고침 (PC13-01 · 02 · 04 · 시험 먼저) · 사전 공격 13 반입 · rr3_fix 보고 소급 | `docs/reviews/rint2_rr2_fix_evidence_20261105/pa13_fix/REPORT.md` · 수정 계획 §10 |
| `576953afd` | 사전 공격 14 고침 (PC14-01 · 04 · 05 · 06 · 시험 먼저) · 사전 공격 14 반입 | `docs/reviews/rint2_rr2_fix_evidence_20261105/pa14_fix/REPORT.md` · 수정 계획 §11 |
| (이 커밋) | 이 요청서 · 원장 (RR3-01 · 02 · PC13 · PC14 · SELF-158 · PC12-03 메모) · 진행 기록 | — |

- Rint ② 밖 (ZIP 에 안 넣음) = Codex 비 Rint 반입 (`f5fb89792` 와 그 앞 cherry-pick 25 · `9c061aafd` · `2e07fb985` · `dff4ceec9` · `f44478535` · `455171e3d` · `0b2c1a39b` · `356dfefd1` · `379e85856`).

## 3. finding → 고친 자리 → 시험 (수 = 그 파일 · E = docs/reviews/rint2_rr2_fix_evidence_20261105 · R3 = E/rr3_fix · F13 = E/pa13_fix · F14 = E/pa14_fix)

| finding | 커밋 | 고친 자리 (요지) | 시험 · 증거 |
|---|---|---|---|
| RR3-01 (P2) · PC12-03 | `742a3b83f` | `arms_read_record` (생성 · 생산자 셋 `Runner._execute` · `ResumeRunner._copy` · `MergeFetch.run` = 성공 ARM_PUBLIC · 실패 파일 신원) · `arm_file_prefix` · `arms_read_kind` (verified = ARM_PUBLIC 칸 정확히 + 그 기록 요청 팔과 일대일 · file_ids · empty · bad) · `prior_runs_problem` = verified 앞 런만 (수정 계획 §9-1 · §9-5 생산자 꼴 표) | 새 RR3A–E · RR3P + 고정물 CT06 · PC12C 3/8 → 8/8 (R3/logs/before_RR3.log → after_RR3.log) · 겨냥 15/15 · 사슬 481/481 → 487/487 · 끝-끝 51 PASS · 0 FAIL · kgy 3.8.20 11 묶음 · 변이 23/23 · 무변이 9/9 · Codex 탐침 (`pc12_attack/probe_pc12_independent.py` · 원본 sha256 7f335c75…) 원본 = rc 1 (RR3-01 존재 assert · 기대한 뒤집힘) · oracle 사본 = rc 0 · 편집 뒤 ["timeout", false] · 원장 RESUME_NOT_ALLOWED (R3/probe_rerun/) |
| RR3-02 (P3) | `742a3b83f` | 회차 ③ 요청서 83 · 84 · 86 · 94 · 135 · 140 · 154 줄 = 취소선 + "11-08 정정 (RR3-02)" 현재 범위 (역사 보존) | R3/logs/rr3_02_rg_check.log (바뀐 줄 = 표지 줄 · OK) |
| SELF-158 (P3) | `17d45fb9c` | 회차 ③ 요청서 §5-2 "F2 = 과장 확인" 문단 = 정정 문장 (`6a81f0c55` 커밋 글 · pc10_n_fix/REPORT.md §8 의 "한 칸 손질 넷 닫음" 중 GU 기록 rc 꼴 과장 · 원 글 = 역사 · 고치지 않음) | 문장 확인만 (원장 claimed_fixed = 이 커밋) |
| PC13-01 (P2) | `7a582acf5` | `resume_mismatch_problem` (compared 에 same 이 정확히 True 아닌 원소 → 멈춤 = RESUME_MISMATCH · run = resume.rerun 일 때만) · `resume_rerun_problem` (자격 원인 멈춤의 resume 칸 ↔ 런 기록 생산자 꼴 + 원천 시도 남은 payload ↔ 이 시도 런 폴더 바이트 다시 대조) · `stop_record_problem` 두 자리 | PA13A 행 48 (실패 38 → 0) · 탐침 p2 · p2b · p2c 편집 행 = resume_ok False · 원장 RESUME_NOT_ALLOWED · 정직 행 그대로 (F13/logs/probe_table.txt) |
| PC13-02 (P2) | `7a582acf5` | `ARM_STATES` · `arm_public_value_problem` (판독 완료 팔 값 = `read_run` 성공 꼴 · 한 함수) · `arms_read_kind` · `read_run` 자기 대조 (어긋남 = ARM_UNREADABLE) | PA13B 행 59 (48 → 0) · PA13D 실경로 CLI 행 3 (2 → 0) · 탐침 p1 · p1b 덧붙임 = bad · rc 3 · 정직 팔 406 거부 0 (p5 · p5b) · 요청 꼴 510 verified 그대로 (p4v) |
| PC13-04 (P3) | `7a582acf5` | `read_run` · `RunnerGraphSource._run` 킷 앞자리 = `arm_file_prefix` (식 하나) | PA13C 행 7 (5 → 0) |
| `7a582acf5` 회귀 | — | 시험한 판 = 커밋 blob (F13/code_sha256.txt) | 새 검사 PA13A–D 0/4 → 4/4 · 사슬 487/487 → 491/491 · 끝-끝 51 PASS · 0 FAIL · kgy 3.8.20 11 묶음 (사슬 491/491) · 변이 49/49 · 무변이 4/4 · 원 탐침 9 출력 = 사전 공격 13 출력과 바이트 같음 9/9 (고치기 전) |
| PC14-01 (P3) | `576953afd` | `arm_public_value_problem` — positive 팔의 cg_resid 를 `_num` (유한 수) 으로 먼저 거른 뒤 `RC.conv_ok` (옛 = ±10**400 → math.isfinite OverflowError → `recover --ledger` traceback · `7a582acf5` 회귀) · 사유의 큰 정수 = 자리 수만 (`_show`) | PA14A 행 11 (실패 6 → 0) · PA14B 실경로 git 원장 행 3 (2 → 0) · 탐침 p3_value_domain = 크래시 없음 · recover rc 0 · 자격 False · --resume rc 3 RESUME_NOT_ALLOWED (F14/logs/probe_diff.txt) |
| PC14-04 (P3) | `576953afd` | `ARM_PID_RE` (protocol_id = 'p3ca-' + 16 자리 소문자 hex · 생산자 = `run_contract._ca_ext_protocol_id` 하나) · `ARM_SID_RE` (sid_fp = 32 자리 소문자 hex · `step3_sigma` 격자 지문) · positive err_rel ≤ τ (증서 목표 허용 1e-4) · 고정물 `ct06_pub` · pad_legacy_state 값 = 생산자 꼴 | PA14C 행 28 (20 → 0) · τ 근거 = ⓓ 통과 383670 해 (칼날 300378) 중 e > τ 0 · 최대 e = τ (F14/logs/tau_bound_check.log) · 탐침 p3 의 pid · sid · err 여덟 행 = bad |
| PC14-05 (P3) | `576953afd` | `RESUME_KEYS` · `resume_rerun_problem` — 재실행 요약 resume 칸 집합 = 생산자 다섯 칸 정확히 (덧붙임 · 빠짐 · 글 아닌 열쇠 = 사유 · 집합 대조가 from · copied 대조보다 먼저) | PA14D 행 18 (9 → 0) · 탐침 p1_resume_bypass A1 · A2 · A4 = 자격 False · 받는 것 = 선언 한정 셋 (원천 다른 곳 · PC13-01 한정) 만 · 정직 셋 그대로 |
| PC14-06 (P3) | `576953afd` | 시험 PA14D 에 변이 생존 넷 행 고정 (M14 copied_from 형 · M18 대조 전 멈춤의 compared · M47 compared 원소 객체 · M54 from 아래 경계 = 시도 번호 바꾼 사본 + 정직 꼴) | 그 행 = 고치기 전 · 뒤 모두 거부 (고정 · 정직 꼴 = 자격 True) · 같은 네 바꿈 = 변이 23/23 안에서 잡힘 (F14/logs/mutation_results.json) |
| `576953afd` 회귀 | — | 시험한 판 = 커밋 blob (F14/code_sha256.txt) | 새 검사 (`--only PA14,PA13`) 4/8 → 8/8 · 사슬 491/491 → 495/495 · 끝-끝 51 PASS · 0 FAIL · kgy 3.8.20 11 묶음 (사슬 495/495) · 변이 23/23 · 무변이 8/8 · 동치 1 (놓침으로 기록 · 목록 밖) · 고치기 전 탐침 8 출력 = 사전 공격 14 출력과 같음 (바이트 6 · 시각 · 런 표지 정규화 뒤 2) · 고침 중 컨테이너 재시작 = 끝-끝 · kgy 판 다시 돈 판 (F14/REPORT.md 머리) |

## 4. 알려진 한정 (닫지 않는 것)

| 한정 | 출처 | 처분 |
|---|---|---|
| 구조 · 값 계약은 **바이트 출처** 를 대조하지 않는다 — 판독 완료 기록의 sha256 ↔ 디스크 파일 · 다른 런에서 옮겨 붙인 판독 완료 기록 · 그럴듯한 값으로 모든 칸 · 사본을 일관되게 고친 위조 = 계약 밖 (판정문 §5 끝 = 새 요구 아님 · 실제 재개 복사는 원 팔을 다시 읽어 거부) · `read_run` 이 값을 고정하지 않는 칸 (imbalance · sv_cf_status · zero 의 cg_info · cg_resid · cert_pass 원소) = 대조 안 함 | R3/REPORT.md 한정 · F13/REPORT.md 한정 | 한정 (Q-D) |
| PC13-03 — 앞 런 기록 완결성 (arm_list 칸 없음 · REQ_KEYS 결손 · outdir 아무 값 · 파일 이름 NUL · 줄바꿈 · `..`) 대조 없음 = verified · 이것만으로 실패 런 자격 길 아님 · MergeFetch 기록 outdir 꼴 = 생산자별로 다름 | E/preattack13/REPORT.md P3 ① · F13 탐침 p6 | 새 원장 PC13-03 (P3 · open · 한정) |
| PC13-01 고침의 범위 — 원천 시도가 같은 바탕에 없으면 바이트 다시 대조 안 함 (F13 탐침 p2c LIMIT_e3_same_true_src_elsewhere = 자격 True 그대로 · 같은 바탕에서 다시 세면 대조 실패 = LIMIT_resume_chain_recount) | F13/REPORT.md 한정 | 한정 |
| PC14-02 — 원천 시도가 있어도 정직 RESUME_MISMATCH 요약의 복사 / 새 런 경계만 다시 적으면 (R1 = 7 칸 · R2 = 6 칸) 자격 True · 디스크로 가를 수 있음 (groups/&lt;런&gt;.launch.json 바이트 · 복사 런 = 원천과 같음 · 새로 돈 런 = 다름) · 구현 안 함 | E/preattack14/REPORT.md P3-b · 탐침 p7_relabel | 새 원장 PC14-02 (P3 · open · 한정 · 봉인 전 확인 ③ = 실제 기록의 복사 출처 대조) |
| PC14-03 — resume.from 이 원장 사슬 끝에 묶이지 않음 (정직 3 시도 사슬 7 칸 손질 = 자격 True) · attempt.json resume_of ↔ 원장 항목 대조 = 판정 · 합치기 (`found_attempts_problem`) 에서만 (결과 줄 길 = attempt.json 꼴만) | E/preattack14/REPORT.md P3-c · 탐침 p2_chain3 · p6_attempt_json | 새 원장 PC14-03 (P3 · open · 한정 · 봉인 전 확인 ③ = 실제 순서 · 원장 항목 대조) |
| 고침 B (`576953afd`) 의 한정 — protocol_id · sid_fp = 꼴만 (그 값이 이 런의 것인지 = 값 계약 밖) · err_rel −0.0 = verified 그대로 · 반복 수 위 한계 없음 · zero 의 증서 칸 = 그대로 · 4300 자리 넘는 정수 = JSON 읽기가 먼저 거부 (3.11.17 · 3.8.20 = `sys.get_int_max_str_digits()` 4300 · 실측) · kgy 3.8.10 의 자리 한도 · 그 판에서 읽힌 큰 정수의 사유 길 = 미확인 (`_num` 은 OverflowError 를 잡고 `_show` 는 자리 수만 적는다) | F14/REPORT.md 한정 | 한정 (kgy 3.8.10 = 현장 자격) |
| 관찰 (시험으로 확인 전) — 앞 런이 모두 판독 완료인 뒤의 단계 차원 검사 멈춤 (값 판정) 을 런 전 TIME_LIMIT (다음 이름) 로 바꾼 두 칸 손질 = 정직 런 전 TIME_LIMIT 와 기록 꼴이 같아 구조로 못 가른다 (시간 회계 대조 = 범위 밖) | 수정 계획 §9-6 | 한정 |
| 회차 ③ 에서 넘어온 한정 그대로 — PC11-05–08 · PC12 고침 한정 (회차 ③ 요청서 §4 · 11-08 정정 표지 뒤 문장) · 보조 관측 = 그룹 기록 판독 (`_read_group_json`) = 일반 json.loads · 엄격 JSON = 단계 요약 한정 | 수정 계획 §7 ③ ⑤ | 봉인 전 확인 · 한정 |
| 시험 = 합성 · 가짜 러너 · 모의 `run_in_group` · 실제 git 원장 · 이 컨테이너 (Linux · Python 3.11 · kgy 판 3.8.20 — 실제 kgy 3.8.10 · ibb · GPU · 실제 SIGKILL · flock · NFS 아님) · 웹앱 화면 없음 (resume_ok · RESUME_NOT_ALLOWED · RESUME_MISMATCH · arms_read · 재실행 자격 화면 = grep 0) | 각 보고 머리 | Q5 현장 자격 · 웹앱 = "없음" 기록 |
| `scripts/rint_r_chain.py` sha 바뀜 = R 계획 code key (CODE_FILES) 바뀜 → 봉인 = 새 핀 (S0 코드 지문 묶음 `S0_SAME_FILES` 엔 없음 = S0 단계 1 결과 지문 그대로) | 수정 계획 §7 ④ · §8 | 봉인 때 |

## 5. 사전 공격 리뷰 (CLAUDE.md ①–④)

### 5-1. ① 숫자 · 전칭 ↔ 출처 (11-09 · 메인 세션 · 이 커밋을 만든 작업 트리 · 커밋 전 · push 전은 precheck 로 다시)

| 주장 | 출처 · 명령 | 결과 |
|---|---|---|
| 커밋 번호 (이 파일의 백틱 SHA 15 개) | `git rev-parse --verify <sha>^{commit}` · `git merge-base --is-ancestor <sha> <핀>` | 15 / 15 조상 |
| stoic 동결 `6a81f0c55` · B = `379e85856` 까지 push | `git rev-parse origin/claude/stoic-knuth-NObVQ` · `origin/claude/sdcp-dem-manuscript-si-pqwtv8` (11-09 fetch) | 같음 |
| 회차 ③ HOLD · P1 0 · P2 1 · P3 1 · 닫힘 30 · PC12-03 · SELF-155 부분 · 핀 `17d45fb9c` | 판정문 머리 · §3 · `docs/reviews/codex_rint2_rr_round3_evidence_20261108/README_import.md` 원장 표 | 같음 |
| 폴더 파일 수 111 · 57 · 37 · 68 · 26 · 71 · SHA256SUMS 110 · 56 · 36 · 67 · 25 · 70 | `find <폴더> -type f \| wc -l` · `wc -l SHA256SUMS` · 폴더마다 `sha256sum -c` | 같음 · -c 통과 |
| 의존 26 = diff 0 · 바뀐 Rint ② 코드 2 · 나머지 9 = Rint ② 밖 | `git diff --quiet 17d45fb9c <핀> -- <파일>` · `git diff --name-only 17d45fb9c <핀> -- scripts/` | 같음 |
| CODE_FILES 319 줄 · 19 | `grep -n '^CODE_FILES' scripts/rint_r_chain.py` | 같음 |
| §3 의 수 (RR3 · PA13 · PA14 전 → 뒤 · 회귀 · 변이 · τ · 탐침) | 그 행 로그의 끝 줄 (R3 · F13 · F14 의 before · after · full · e2e · check_kgy · mutation · tau_bound_check · rr3_02_rg_check · 행 요약) | 같음 |
| 시험한 판 = 커밋 blob (셋) | `git show <커밋>:scripts/rint_r_chain.py \| sha256sum` · 시험 파일 같음 ↔ R3/logs/code_sha256.txt · F13/code_sha256.txt · F14/code_sha256.txt | 같음 (b37ef7c6 · d83539a1 / 78d91ad0 · 8ba91d45 / 47a520e8 · d5e1d9ea) |
| 사전 공격 14 반입 = 원문 바이트 | 반입 폴더 REPORT.md · probes/ · out/ ↔ 세션 원문 (`cmp`) | 같음 (빠진 파일 0) |
| 원장 1020 → 1030 (open 344 · claimed_fixed 353 → 363 · verified 312 · wontfix 11) | `python3 scripts/check_review_findings.py` (앞 · 뒤) | rc 0 |

- 이 대조로 고친 것 = §1 의 "게이트 줄 하나" → 믹서 시험 세 줄 (`git diff 17d45fb9c <핀> -- scripts/check_all.sh`) · 확인 못 한 것 = 리뷰 핀 push · ZIP · PIN.txt (리포 밖 · push 뒤 메인 · 진행 기록에 적음).

### 5-2. ② ③ 사전 공격 13 (11-08 · 독립 · diff 만 `40d9658c0..742a3b83f` · 계획 안 읽음 · 보고 `docs/reviews/rint2_rr2_fix_evidence_20261105/preattack13/REPORT.md`)

- 결과 = **P1 0 · P2 2 · P3 2** · 버틴 것 = 정직 출력 잘못 거부 0 (실제 CLI 런 기록 260 전부 verified · 합성 510 꼴 전부 verified · 실패 꼴 전부 file_ids) · 변이 30/30 (RR3 · PC12 · CT06) · 사슬 487/487 (3.11 · 3.8.20) · 끝-끝 51/0.
- P2-1 (= PC13-01) — 정직 RESUME_MISMATCH 시도 요약의 stop 두 칸 (code → TIME_LIMIT · run → 다음 이름) = 재실행 자격 · 앞 런 둘 = 생산자가 실제로 쓴 exit_ok + verified · 다음 재실행이 시도 1 과 바이트 다른 L02 를 대조 없이 복사 · 부모 `40d9658c0` 에서도 같음 (회귀 아님 · RR3-01 고침이 못 닫은 같은 부류).
- P2-2 (= PC13-02) — verified 판정이 칸 이름 + file · index · sha256 만 봄 → 판독 실패 기록에 ARM_PUBLIC 나머지 11 칸을 생산자가 안 쓰는 값으로 덧붙이면 verified · 실제 git 원장 `--add --resume 1` rc 0.
- P3-1 (= PC13-03 · 한정) · P3-2 (= PC13-04 · 고침).
- 처분 = (가) Codex 전에 고침 (1저자 11-09) · `7a582acf5` · 수 = §3.

### 5-3. ② ③ 사전 공격 14 (11-09 · 독립 · diff 만 `f44478535..7a582acf5` · 보고 `docs/reviews/rint2_rr2_fix_evidence_20261105/preattack14/REPORT.md`)

- 결과 = **P1 0 · P2 0 · P3 6** · 버틴 것 = 원천이 같은 바탕일 때 1–4 칸 편집 21 행 전부 거부 · 정직 꼴 거부 0 (새 시도 · 정직 RESUME_MISMATCH · 재실행 런 멈춤 · 대조 같은 뒤 자원 멈춤 · 3 시도 사슬 · 예측 재실행 뒤 멈춤 3) · arms 1–8 · arm_list 255 + 실제 사다리 · 예측 기록 verified · `read_run` 자기 대조 = 정직 출력에서 안 걸림 · 변이 51 (동치 2) 중 45/49 를 PA13A–D 가 잡음 · 사슬 491/491 (3.11 · 3.8.20) · 끝-끝 51/51 (3.11).
- P3-a (= PC14-01 · `7a582acf5` 회귀) — positive 팔의 cg_resid = JSON 큰 정수 (10**400) → `RC.conv_ok` 의 math.isfinite OverflowError → `recover --ledger` traceback (같은 바탕 뒤 폴더 못 셈 · PC11-03 부류 = 사전 공격 11 P3-5 · 원 보고의 "PC10 P3-5" 이름표 = 이 항목).
- P3-d (= PC14-04) — protocol_id 앞자리만 · sid_fp 비지 않은 글 · positive err_rel 위 한계 없음 → 생산자가 안 쓰는 값이 verified.
- P3-e (= PC14-05) — resume 칸 집합 대조 없음 (여분 칸 · run == rerun 때 determinism 칸 지움 = 자격 True).
- P3-f (= PC14-06) — 변이 생존 넷 (copied_from 형 · run == rerun 가지 compared 빈 목록 · compared 원소 객체 · from 아래 경계) = 현 코드는 네 입력 다 거부 · 시험 행 없음.
- P3-b (= PC14-02) · P3-c (= PC14-03) = 선언 한정 (§4).
- 처분 = (가) a · d · e · f 고침 (1저자 11-09) · `576953afd` · b · c = 한정 · 이 고침의 독립 재공격 = 없음 (사전 공격은 13 · 14 두 회차 · 다음 = Codex).

### 5-4. ④ 닫는 것 / 닫지 않는 것 = §0.

## 6. 판정 요청 질문

| # | 질문 |
|---|---|
| Q1 | §3 의 finding 마다 닫힘 / 부분 / 열림 — RR3-01 · RR3-02 · PC12-03 · PC13-01 · 02 · 04 · PC14-01 · 04 · 05 · 06 · SELF-158 (최소 해결 ↔ 고친 자리 · 회차 ③ 반례 재실행 = R3/probe_rerun/ · 사전 공격 13 · 14 탐침 재실행 = F13/probe_out/ · F14). |
| Q2 | RR3-01 고침 (판정문 §2 최소 해결의 첫 꼴 = 완성 ARM_PUBLIC 구조 + 요청 팔 대응) + PC13-02 (값 꼴 = `read_run` 성공 꼴 한 함수) + PC14-04 (생산자 값 꼴 정확히) 가 "검증을 마친 팔 기록 ↔ 실패 때 보존한 파일 신원 목록" 구분으로 충분한가 — 양성 (성공 · 복사 성공 · 합치기 성공 · 실제 CLI 런 기록 · 사다리 · 예측) 그대로 · 원 RR3-01 반례 거부 · 바이트 출처 대조는 계약 밖 (§4 첫 행). |
| Q3 | PC13-01 의 재개 칸 대조 (`resume_mismatch_problem` · `resume_rerun_problem` + PC14-05 칸 집합) 가 같은 부류 (멈춤 원인을 자격 원인으로 바꾸는 요약 손질) 를 닫는가 · 선언 한정 PC14-02 (원천 있는 시도의 복사 / 새 런 경계 다시 적기 · launch 바이트로 가를 수 있으나 구현 안 함) · PC14-03 (resume.from ↔ 원장 사슬 끝 · attempt.json resume_of ↔ 원장 항목) 를 봉인 전 확인 (수정 계획 §7 ③ = 실제 계획 · 시도 기록 대조) 으로 넘겨도 되는가, 봉인 전에 코드로 막아야 하는가. |
| Q4 | 기대 바뀜을 받는가 — 정직 앞 런 고정물 CT06_ARM (생산자의 판독 실패 꼴) → ct06_pub (생산자 성공 꼴 · 수정 계획 §9-3) · ct06_pub 값 → 실제 생산자 값 꼴 (PC14-04 · F14/REPORT.md) · 옛 시험 파일 × 고친 사슬 = 바뀐 행 (CT06 · PC12C 행 · 사유 file_ids · R3/logs/cross_oldtests_fixedchain_rows.json). |
| Q5 | 이 회차 뒤 판정문 §7 의 문안 "코드 · 설계 · 문서 GO (재개 정책 포함) + 봉인 전 확인" 을 줄 수 있는가 — 남는 것 = 현장 자격 · kgy S0 단계 1 재실행 (채택 조건 §8) · 12 단위 끝-끝 · 봉인 전 확인 (수정 계획 §7 ③ ④) · 봉인 → S0 단계 2 → 등록 R 진입 판단 (판정문 §7 순서 그대로). |

## 7. 묻지 않는 것

- 등록 R 캠페인 GO · R 런 · 정량 판정 · 생산 GO · 숫자 칸의 값 · ⑦ SBE 탐침 (봉인 뒤).
- 회차 ③ 에서 verified 된 30 의 다시 판정 (회귀가 깨졌을 때만) · SELF-155 실침대 · S0 단계 2 · 빠진 물리 (v0 동결) · 다음 트랙 설계.
- Rint ② 밖 트랙 (50kg · LHS · 믹서 · FAM · 웹앱 /emod · 후막).
