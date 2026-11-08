# pa13_fix — 사전 공격 13 고침 (P2-1 RESUME_MISMATCH 모순 · P2-2 ARM_PUBLIC 값 꼴 · P3-2 앞자리 한 함수) · 11-09 · 작업 트리 에이전트 · 시험 먼저

- 근거 = 1저자 11-09 *"다 권고대로 해줘 물어보지말고"* (메인 세션 전달) = (가) Codex 회차 ④ 전에 고침 · P3-1 = 선언된 한정 · 사전 공격 원문 = `../preattack13/REPORT.md` (반입 · 탐침 · 출력 · 로그 · SHA256SUMS) · 처분 기록 = `docs/reviews/rint2_rr3_fix_plan_20261108.md` §10.
- 바탕 `f44478535` (두 코드 파일 = 사전 공격 대상 `742a3b83f` 와 같은 blob) · 코드 sha256 (`code_sha256.txt`) = `scripts/rint_r_chain.py` b37ef7c6… → 78d91ad0… · `scripts/test_rint_r_chain.py` d83539a1… → 8ba91d45… · 바탕 + `code.diff` (apply) = 그 바이트 · 시험 · 변이 · 탐침 다시 = 그 바이트.
- 환경 = 이 컨테이너 Python 3.11 · kgy 판 3.8.20 · numpy 1.24.4 · scipy 1.10.1 · 합성 폴더 · 가짜 러너 · 모의 `run_in_group` · 실제 git 원장 (시험 PA13D · 탐침 p1b) · 합성 원장 줄 (`ledger_parse` · 탐침 p1 · p2 · p2b) · kgy · ibb · GPU 아님.
- push · 게이트 (`scripts/check_all.sh`) · 원장 (`docs/reviews/findings.json`) = 메인 세션 · 웹앱 화면 없음 (`webapp/` 에 resume_ok · RESUME_NOT_ALLOWED · RESUME_MISMATCH · arms_read · arm_public_value_problem · rint_r_chain · "재실행 자격" = 0 건).

## 바꾼 것 (줄 = 고친 판 `scripts/rint_r_chain.py` · `tools/fn_lines.py`)

| 결함 | 자리 | 무엇 |
|---|---|---|
| P2-1 ① | `resume_mismatch_problem` 4327–4340 · `stop_record_problem` 4153 (맨 앞 · 모든 멈춤) | 요약 resume 칸 compared 에 same 이 정확히 True 아닌 원소 → 멈춤 = RESUME_MISMATCH · run = resume.rerun 일 때만 받음 |
| P2-1 더 굳게 | `resume_rerun_problem` 4343–4420 · `stop_record_problem` 4171 · `RESUME_DETERMINISM` · `RESUME_COMPARED_KEYS` 4323–4324 | 자격 원인 멈춤 (앞 대조 뒤) 의 resume 칸 ↔ 런 기록 = 생산자 꼴 (재실행 시도면 객체 · from 범위 · copied ↔ 복사 기록 · 복사 먼저 · 첫 새 런 = rerun · 대조 전 멈춤 = [] · null · 대조 뒤 = determinism · compared 꼴 · rerun outdir) + 원천 시도 (같은 바탕) 남은 payload ↔ 이 시도 그 런 폴더 바이트 다시 대조 · 원천 자리 = 옆 거부 기록 = 모순 · 못 읽음 = 사유 |
| P2-2 | `ARM_STATES` 2180 · `arm_public_value_problem` 2183–2222 · `arms_read_kind` 2261 · `read_run` 2454–2460 | 판독 완료 팔 값 = read_run 성공 꼴 (state · protocol_id 앞자리 · sid_fp · cert_pass · err_rel · 반복 수 · positive 수렴 계약) · 한 함수 = verified 조건 + read_run 자기 대조 (어긋남 = ARM_UNREADABLE) |
| P3-2 | `read_run` 2321 · 같은 부류 `RunnerGraphSource._run` 5431 | 킷 앞자리 = `arm_file_prefix` (식 = 2175 하나) |

- 머리말 ★ 11-09 문단 181–187 · 시험 `scripts/test_rint_r_chain.py` = 470 줄 더함 · 지운 줄 0 (옛 검사 487 그대로): PA13A (P2-1 · 행 48) · PA13B (P2-2 · 행 59) · PA13C (구조 · 행 7) · PA13D (P2-2 실경로 CLI · 행 3) · 고치기 전에도 통과한 행 = 정직 · 생산자 · 양성 대조 (10 · 11 · 2 · 1) · 나머지 = 편집 · 덧붙임 · 값 · 구조 반례.

## 수 (고치기 전 → 뒤)

| 묶음 | 고치기 전 | 고친 뒤 | 로그 |
|---|---|---|---|
| 새 검사 (`--only PA13`) | 0/4 PASS (7.6 s · 사슬 = 바탕 · 시험 = 고친 판) · 실패 행 A 38/48 · B 48/59 · C 5/7 · D 2/3 | 4/4 PASS (7.0 s) · 실패 행 0 | `logs/pa13_before.log` · `logs/pa13_after.log` · 행 `logs/pa13_rows_before.json` · `logs/pa13_rows_after.json` (`tools/rows_dump.py` · `tools/rows_summary.py`) |
| 사슬 전체 (3.11) | 487/487 PASS (363.7 s · `../preattack13/full_py311.log`) | 491/491 PASS (445.5 s) | `logs/full_py311.log` |
| 끝-끝 (3.11) | 51 PASS · 0 FAIL (829.1 s · `../preattack13/e2e_py311.log`) | 51 PASS · 0 FAIL (781.1 s) | `logs/e2e_py311.log` |
| kgy 판 3.8 (`scripts/check_kgy_py38.sh`) | 사슬 487/487 (547.6 s · `../preattack13/full_py38.log`) | 11 묶음 통과 · rc 0 — rint_r_chain 491/491 (537.2 s) · 끝-끝 51 PASS · 0 FAIL (605.4 s) · 그 밖 9 = run_contract 124/124 · step3_rint PASS · ptfe_face_alpha 242/0 · carbon_junction 547/547 · ca_ext_b6 502/0 · ca_ext_runner 151/0 · step3_target_cert 264/264 (11.8 s) · step3_conv_cert 29/29 · ca_s0_census 186/0 | `logs/check_kgy_py38.log` · `logs/py38/` |
| 변이 (`tools/mutate_pa13.py`) | — | 49/49 잡힘 · 놓침 0 · 무변이 M00 4/4 PASS (8.0 s) | `logs/mutation_run.log` · `logs/mutation_results.json` |
| 탐침 다시 (`tools/run_all_probes.sh` · `tools/run_probes.py`) | 원 탐침 9 출력 = 사전 공격 13 출력과 바이트 같음 9/9 (`logs/before_vs_preattack.log`) | 아래 표 | `logs/probe_rerun.log` · `logs/probe_table.txt` (`tools/probe_table.py`) · `probe_out/` |

- 변이 49 = 값 꼴 19 (V01–V14 · V02b · V03b · V04b · V06b · V09b → PA13B · PA13C) · 규칙 ① 6 (R01–R06 → PA13A) · resume 칸 22 (S01–S18 · S04b · S05b · S13b · S14b → PA13A) · 앞자리 2 (P01 · P02 → PA13C) · 뿌리 = 작업 트리 링크 + 변이 사슬 + 고친 시험 사본 (`tools/mktree.py`).
- 그 밖 점검 (`logs/static_checks.log` · `tools/static_checks.sh`) = pyflakes (두 파일) rc 0 · `scripts/check_undefined_names.py` (두 파일) 없음 · kgy 판 3.8 py_compile rc 0.

## 탐침 (고치기 전 → 뒤 · 원 탐침 = `../preattack13/probes/` · 새 탐침 = `probes/`)

| 탐침 | 고치기 전 | 고친 뒤 |
|---|---|---|
| p1 (P2-2 · 판독 실패 기록에 11 칸 덧붙임 셋 · 합성 원장) | verified · resume_ok True · 원장 허용 (셋) | bad · resume_ok False · 원장 RESUME_NOT_ALLOWED (셋) · 덧붙이지 않은 꼴 = file_ids 그대로 · py3.8 출력 = 3.11 과 바이트 같음 |
| p1b (P2-2 · 실제 CLI · git 원장) | 덧붙임 resume_ok True · --resume 1 rc 0 | resume_ok False · rc 3 RESUME_NOT_ALLOWED (덧붙이지 않은 꼴 = rc 3 그대로) |
| p2 (P2-1 · 단일 시도 합성 원장) | 두 칸 편집 resume_ok True · 원장 허용 | resume_ok False · 사유 · 원장 RESUME_NOT_ALLOWED · 정직 결과 줄 (check · False) 그대로 · 시도 2 런의 `_src_done` True 그대로 (재실행이 원장에서 막힘) |
| p2b (P2-1 · 두 시도 합성 원장 사슬) | 편집 결과 줄 resume_ok True · 다음 --resume 1 허용 | False · 다음 = RESUME_NOT_ALLOWED · 다시 셈 None |
| p2c (새 · 편집 7 + 정직 3 + 한정 2) | 편집 7 = resume_ok True | 편집 7 = False + 사유 · 정직 셋 그대로 (RESUME_MISMATCH = check False · 대조 같음 뒤 런 rc = resource True · 그 원천이 다른 곳 = True) · 한정 = 아래 |
| p3 (정직 출력 260 · 사다리 · 예측 · 12 단위 · 합치기 · 넘침) | 전부 verified · bad 0 | 같음 |
| p4 (요청 꼴 510 · 팔 값 전부 null) | 510 verified | 0 verified (원판 팔 = p1 의 전부 null 꼴 → bad 가 옳다 · 출력은 탐침 원판대로 2000 자에서 잘림) |
| p4v (새 · 같은 510 꼴 · read_run 성공 값) | 510 verified · null 판 510 verified | 510 verified 그대로 · null 판 510 bad · 판독 실패 꼴 = file_ids (어긋남 0) |
| p5 (정직 팔 406 · 제안 값 꼴) | 거부 0 | 거부 0 |
| p5b (새 · 정직 팔 406 · 사슬 함수) | 함수 없음 (N/A) | 거부 0 · 런 172 verified |
| p6 (P3-1 구조 가장자리 8) | verified 8 | verified 8 그대로 (선언된 한정) |

## 한정 (닫지 않은 것)

- P3-1 = 선언된 한정: 앞 런 기록 완결성 대조 없음 (arm_list 칸 없음 · REQ_KEYS 결손 · outdir 아무 값 · 파일 이름 가운데 NUL · 줄바꿈 · `..` · 가운데 없는 이름 = verified · 탐침 p6) · 이것만으로 실패 런 자격 길 아님 · MergeFetch 기록 outdir 꼴 = 생산자별로 다름.
- P2-2: read_run 이 값을 고정하지 않는 칸 (imbalance · sv_cf_status · zero 의 cg_info · cg_resid · cert_pass 원소) = 대조 안 함 · 그럴듯한 값 일관 위조 · 다른 런 판독 완료 기록 옮겨 붙임 = 그대로 (값 계약 밖).
- P2-1: 원천 시도가 같은 바탕에 없으면 바이트 다시 대조 안 함 — p2c 의 LIMIT_e3_same_true_src_elsewhere = resume_ok True 그대로 · 그 결과 줄을 같은 바탕 (원천 있음) 에서 다시 세면 대조 실패 (LIMIT_resume_chain_recount · 고치기 전 None) · from = 원장 사슬 끝인지 못 봄 · attempt.json resume_of 까지 함께 고친 위조 = 원장 항목 대조 몫.
- 안 돌린 것 = `scripts/check_all.sh` 전체 · Codex 회차 ④ (메인 세션) · 사전 공격 13 의 변이 도구 (`../preattack13/probes/mutate.py` · `mutate2.py` = RR3 시험 변이 · 탐침 아님) · 이 고침의 독립 재공격.
