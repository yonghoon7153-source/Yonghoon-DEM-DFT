# Rint ② PC10-08 · 09 · 10 고침 — N1 · N2 (P2 후보) · N4 (P3) + 같은 부류 (11-06 · 작업 트리 에이전트 · 1저자 11-06 "권고대로")

- 근거 = preattack10_fix/REPORT.md §7 (N1 · N2 · N4 · 탐침 new_findings/probe_new.py) · 같은 부류 = preattack10/PREATTACK10_report.md PB-01.
- 규칙 (1저자 11-06) = 생산자가 쓰지 않는 칸 조합 = 모순 = 재실행 자격 없음 (읽음 False · fail-closed) · 시험 먼저.
- 바탕 = 766e1e80c (작업 트리 가지가 처음에 main 첫 커밋 bf0dd1a32 → fast-forward) · 작업 트리 커밋 (뒤에 확장 고침과 한 커밋으로 다시 · main 반입 = cherry-pick -x · 원 번호 = 반입 커밋 메시지) · push 없음 · 원장 · CLAUDE.md · check_all.sh 무변경 · 게이트 안 돌림.
- 환경 = logs/environment.txt (Linux 6.18 · Python 3.11.18 · numpy 2.4.6 · scipy 1.17.1 · kgy 판 uv CPython 3.8.20 · numpy 1.24.4 · scipy 1.10.1 · 4 코어 · root).
- 코드 sha256 = logs/code_sha256.txt (사슬 f3d6a40f… · 시험 f7f1c0f7… · 끝-끝 41762029… 무변경) · 고치기 전 = 사슬 da4c2ef6… (지난 회차 끝 판 = probe_new.json 이 본 판) · 시험 f797fe7e….
- ⚠ 이 REPORT.md 는 작업 트리 에이전트가 쓰지 못해 (하네스가 하위 에이전트의 보고 파일 쓰기를 막음) 본 세션이 넣었다 (에이전트 보고 본문 그대로) · 넣은 뒤 이 폴더 · 바깥 폴더 SHA256SUMS 를 다시 만든다.

## 0. 쉽게 말하면
- N1 — 멈춤 코드 한 칸만 RUNNER_RC → TIME_LIMIT (런 기록 {group_cause None · rc 1} · Traceback) = timeout · 자격 True 였다 → runner_rc (멈춤 코드와 무관하게 group_cause None 이면 정확한 정수 0 만 성공) · 자격 False (TIME_LIMIT 생산자 런 기록 = {timeout · null} 뿐).
- N2 — group_cause 한 칸만 None → timeout · signal (rc 1 그대로) = 자격 True 였다 → 원인 글 그대로 · 자격 False (사슬이 죽인 원인이면 rc null · RUNNER_RC + timeout 없음).
- N4 — recover --ledger 가 객체 아닌 rejected.json 에 AttributeError (깊은 중첩 = RecursionError) traceback → rejected_record (다시 셈과 같은 읽기) = Stop ATTEMPT_LEDGER_MISMATCH · 결과 줄 없음 · rc 3.
- 같은 부류 (같은 규칙 · 덮음) — 요약 있는 길: 메모리 낱말 + 생산자 밖 런 기록 (RUNNER_RC + {None · 0 · null · 꼴 틀림} · GROUP_UNCONFIRMED + {None · null · 꼴 틀림} · {죽인 원인 · rc 있음} · group_cause 칸 없음) = resource · 자격 True 였다 · 런 기록 없는 TIME_LIMIT + 읽히는 로그 = 자격 True 였다 → 자격 False.  요약 없는 길: 끝 기록 · chain_end 원인 None + rc null · 꼴 틀린 rc = 읽음 True 였다 → False.

## 1. 생산자가 쓰는 칸 조합 (원천 · 줄 = 고친 판)
### 1-1 멈춘 런 기록 — Runner._execute (4642–4665) · ResumeRunner._copy (4747) · ae8ea5ebd (10-27) 3283–3304 와 같은 꼴
| 멈춤 코드 | group_cause | rc | 자리 |
|---|---|---|---|
| TIME_LIMIT | (기록 없음 · 흔적 없음) | — | 시간 상한 관문 |
| TIME_LIMIT | timeout | null | 시간 초과 · 종료 확인 |
| RUNNER_RC | signal · signal_after | null | 신호 · 정리 중 신호 |
| RUNNER_RC | None | 정수 ≠ 0 | 러너 rc |
| RUNNER_RC | (runs[] 에 없음) | — | 봉인 원천 G&lt;n&gt;_… (기록 = sv_graph_source) |
| GROUP_UNCONFIRMED | None | 정수 (0 포함) | 종료 미확인 |
| GROUP_UNCONFIRMED | timeout · signal · signal_after | null | 종료 미확인 |
| 검사 멈춤 · RESUME_MISMATCH | None | 0 | read_run · 결정성 |
| CHAIN_EXCEPTION (run null) | (칸 없음 가능) | null | 사슬 예외 |
| OUTDIR_NOT_EMPTY · DUPLICATE_RUN · NOT_REGISTERED · RESUME_NOT_ALLOWED | (기록 없음) | — | 런 기록 전 |
### 1-2 그룹 끝 기록 — run_in_group (2746–2789) · recover_group (7205 · 7252): by chain 원인 None ⇒ rc 정수 · timeout · signal · exception ⇒ rc 정수 (경합이면 러너 값 0 · 1 가능) 또는 null · by recover = rc null · parent_dead · chain_end = 사본.  디스크 끝 기록의 원인 signal_after = **어느 판도 쓰지 않았다** (C2b 4ed966b5d 부터 run_in_group 의 디스크 원인 = None · signal_after 는 돌려주는 dict 칸뿐 · 받는 근거 = 시험 고정물 꼴뿐 · 받는 결정 = A1b 그대로 · 한정) — ★ 11-06 확장 정정: 옛 글 "옛 기록" 은 판 근거가 없었다 (ext/REPORT_EXT.md).  경합 꼴 = 발견 아님.
### 1-3 거부 기록 — attempt_reject (3458) = JSON 객체 (REJECTED_KEYS).

## 2. 고친 것 (scripts/rint_r_chain.py)
- N1 · N2: STOP_RUN_SHAPES · run_record_shape · stop_record_problem (사유 글) · stop_record_readable — §1-1 표 밖 = 읽음 False (원인 글 그대로) · 런 기록 없는 TIME_LIMIT = RUN_DIR_RE 이름 + 흔적 없음 (run_traces · 로그가 읽혀도) · PB-01 GROUP_UNCONFIRMED 행 포함 · 표 밖 멈춤 = 그대로.
- N1 원인: run_exit_failed (group_cause 칸 None + 정확한 정수 0 아님) — TIME_LIMIT · GROUP_UNCONFIRMED 한 읽기 (GROUP_UNCONFIRMED 옛 식 값 그대로).
- 같은 부류: end_record_known → orphan_cause (by chain · chain_end) 읽음 False.
- N4: rejected_record → result_recount · recover_ledger (사유 글 = 옛 다시 셈 글).
- run_traces = stop_log_readable 에서 옮김 (결과 그대로).
- RC01 안: 새 rc 읽기 넷 = 판독 함수 바로 인자 · 'rc' 칸 존재 검사 = 허용 문맥 밖 → rc 칸 없음 = null 같은 읽기 (§8).  웹앱 화면 없음.

## 3. 시험 (시험 먼저)
- 새 CT01 (요약 있는 길 150 행 · 대조 · 사유 · 따로 적은 생산자 표) 91 → 0 · CT02 (요약 없는 길 21 행 · 격자 70) 12 → 0 · CT03 (N4 · 실제 원장 · 바이트 9 + 대조) 6 → 0 · CT04 (실경로 recover → --add --resume · N4 CLI) 4 → 0 (logs/count_bad_before.json · count_bad_after.json · 같은 시험 판 f7f1c0f7…).
- 기대 고친 기존 시험 (옛 허용을 박은 행 · 합 73): RN01 42/112 · PD13 10/78 · PD02 7/200 (rc_timeout = PD_CONTRA · rc_signal_after 입력 rc 0 → null) · PD02c 2/99 · PE03u 4/44 · RC02 6/8 · LG01 2/63.
- 고르기 (--only CT,RN,RC0,PE03,PD13,PD02,LG,CE,SU,FF): 원 모듈 사본 21/32 (실패 = 위 11) → 32/32 (logs/before_targeted.log · after_targeted.log) · 첫 시험 먼저 실행 (중간 시험 판 d662ab0f…) = 6/17 · 같은 11 실패 (logs/before_new_and_corrected.log).

## 4. 생산자 꼴 그대로
- CT01 151 행 (logs/rows_diff_summary.json): 바뀐 90 = 모두 자격 True → False · 반대 0 · 받아들이는 꼴 행 변화 0 · 원인 글 바뀐 16 = 모두 TIME_LIMIT + group_cause None + 정확한 정수 0 아님 (runner_rc 8 · resource 8 · 자격 False).
- CT02 대조 10 행 변화 0 · CT04 대조 셋 (정직 rc 1 · 생산자 시간 초과 · 신호) 같음.
- 끝-끝 (실제 러너 · 생산자 꼴) 51 PASS · 0 FAIL (고치기 전 = 같은 끝-끝 판 지난 회차 기록 51/0).

## 5. 회귀
- 사슬 3.11 468/468 (고치기 전 · 482.7 s) → 472/472 (474.1 s).  끝-끝 3.11 51 PASS · 0 FAIL (904.9 s).
- kgy 판 3.8.20 11 묶음 통과 (logs/check_kgy_py38.out · run_contract 124/124 · step3_rint · ptfe 242 · carbon_junction 500/500 · ca_ext_b6 502 · ca_ext_runner 151 · 사슬 472/472 (638.3 s) · 끝-끝 51/0 (720.7 s) · target_cert 264/264 · conv_cert 29/29 · s0_census 167) · ⚠ 그 사슬 시험 도중 (13:05–13:07 UTC) 독스트링 · 주석 한 줄씩 고쳤다 되돌림 → 최종 sha 로 3.8 사슬만 따로 = 472/472 (593.5 s · logs/py38_chain_rerun.*).
- pyflakes 4.1.0 (스크래치) rc 0 · check_doc_refs 깨진 참조 없음 · check_review_findings rc 0 · --ban-sweep 42 × 9,483 누수 없음.

## 6. 변이 (mutate_pc10.py · git 없는 사본 · logs/mutation_pc10.*)
- 기준 26/26 · 26 중 25 잡힘 · 생존 1 · 건너뜀 0 · 되돌림 True — G1–G11 (요약 있는 길) · H1–H4 (요약 없는 길) · J1–J3 (N4) · K2–K6 · K1b · K1c (지난 회차 건너뛴 자리 짝) 잡힘 · K1 = 동등 변이 (모르는 글을 killed:&lt;글&gt; 로 내도 허용 집합에 없어 같은 False · 두 겹 가드 · 두 겹 함께 = K1c 잡힘).
- G2 = CT01 만 잡음 (Traceback 행은 N1 원인 조항이 따로 막음 · 메모리 낱말 행이 가름).
- 지난 회차 묶음 (mutate_pa10fix.py · 같은 사본) = 28 중 18 잡힘 · 생존 0 · 건너뜀 10 (B2–B5 · B8 · D3 · D4 · E9 · F3 · F4 = 글자 옮김 · 짝 = G11 · G1 · G9 · K6 · K1c · K2 · J3 · K5 · K3 · K4).

## 7. 탐침 다시 (고치지 않고)
- Codex 회차 ② 303/311 (지난 310/311) · 다른 행 = known_PC6_05 (그대로) + summary_&lt;plain·python·oom·host·disk·gpu·cupy_oom&gt;_TIME_LIMIT_None (고정물 TIME_LIMIT + {rc null · group_cause null} = 생산자 꼴 아님 · stop_cause 글만 'timeout' 기대 → N1 조항 runner_rc · resource · 그 꼴 자격 False) · residual_orphan 정수 아닌 rc 넷 읽음 True → False · integration · candidate 같음 (codex_probe_rerun/compare_prev.out).
- probe_new: N1 → [runner_rc, False] · N2 → [timeout, False] · [signal, False] · 정직 · 대조 그대로 · N4 칸 = result_recount Stop (그대로) · 글자 대조 recover_ledger_isinstance_check False 그대로 (검사가 rejected_record 로 옮김 · 동작 = CT03 · CT04).
- 리뷰어: units 57 중 9 (R1 · R2 · R6 · R7 = 요약 없는 길 읽음 True → False · V0–V4 = 임시 경로) · units2 0/11 · ledger 3/6 (orphan 읽음 → False · 결과 줄 · resume rc 그대로) · rcscan 17/17 · 5/5 · 날 읽기 0 · 자리 38 → 41.

## 8. 같은 부류 — 고치지 않은 것 (왜)
- orphan_cause 경합 꼴 (원인 None → timeout · signal · rc 1) = 생산자 꼴과 구별 불가 (발견 아님).
- 요약 · 런 기록 ↔ 그룹 끝 기록 교차 대조 없음 — ★ 11-06 확장 정정: 옛 글 "여러 칸 함께 맞춘 위조는 못 가림" 은 과소 기술이었다 — 사전 공격 11 P2-B = **한 칸** 손질 넷 (멈춤 이름 · 멈춘 런 이름 · outdir · GROUP_UNCONFIRMED 런 기록 rc) 이 이 판에서 재실행 자격을 얻었다 (바탕 766e1e80c 에도 있던 꼴) → 확장 (ext/REPORT_EXT.md) 이 기록 안 대조 (runs 마지막 · outdir = 요청 칸이 정하는 정확한 이름 · arms_read · GROUP_UNCONFIRMED 끝 기록의 사슬 쪽 확인) 로 그 넷 (+ 옆 이름 outdir) 을 닫음 · 남은 것 = 런 기록 ↔ 끝 기록 (원인 · rc) 교차 대조 (예 TIME_LIMIT 런 기록 {timeout · null} ↔ 끝 기록 원인 None · rc 1 = 세 칸 손질) · 신호 경합 · signal_after · 복사 런 · recover 끝 기록을 다뤄야 해 범위 밖 (Q-D).
- rc 칸 없음 = null (RC01 · CT01 CT_READ_AS 한정 표시).
- 같은 이름 런 기록 둘 = 마지막 (생산자 이름 안 겹침).
- ResumeRunner._src_done = rc 0 만 (공개 한정 · read_run 다시 대조).
- MergeFetch.run · Replay.run · noop_check · load_ladders = rc_success 만 (자격 무관 · fail-closed).
- 검사 · 관문 멈춤 = 판독 안 함 (원인 자격 아님 · N1 조항을 넓히면 메모리 낱말로 자격이 열릴 수 있음).
- 요약 칸 꼴 틀림 예외 → ★ 11-06 확장에서 고침 (P3-5 · 그 폴더 Stop · 뒤 폴더 계속) · 디스크 signal_after = 받음 그대로 (근거 = 시험 고정물 꼴뿐 · 쓴 판 없음 · §1-2 정정).
- 원장 옛 결과 줄 (고치기 전 판 resume_ok True) = 풀기 전 대조의 다시 셈 (resume_chain_problem) 이 거부하는 설계 · 이번에 따로 시험 안 함.

## 9. 한정 · 확인 못 한 것
- §7 의 탐침 기대 차이 (옛 읽기 · 고정물 · 글자 위치) · 실제 SIGKILL · flock · 비 root · hidepid · GPU · NFS/FUSE · kgy 3.8.10 아님 · pyflakes 판 · 게이트 · Codex 확인 전 = claimed 범위.

## 10. 남은 것 (본 세션)
- 원장 PC10-08 · 09 · 10 → claimed_fixed · §0 같은 부류 · §8 등재 여부 · 게이트 · Codex 요청서 (닫는 것 = N1 · N2 · N4 + §0 같은 부류 / 닫지 않는 것 = §8).

## 11. 파일
REPORT.md · dump_ct_rows.py · diff_rows.py · count_bad.py · mutate_pc10.py · logs/ (baseline_* · before_* · after_* · final_* · rows_* · count_bad_* · mutation_* · py38/ · py38_chain_rerun.* · check_* · pyflakes.log · environment.txt · code_sha256.txt · before_code_sha256.txt) · codex_probe_rerun/ · probe_rerun/ · SHA256SUMS · ★ 11-06 확장 (사전 공격 11 P2-A · P2-B · P3-5 · P3-6 · 같은 커밋) = ext/ (REPORT_EXT.md · mutate_pc10ext.py · rerun_probes_ext.py · pa11_probes/ · probe_rerun/ · codex_probe_rerun/ · logs/) — 이 판의 §1-2 · §8 문구 정정 = 확장 때.
