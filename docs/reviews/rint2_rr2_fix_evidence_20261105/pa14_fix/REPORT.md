# pa14_fix — 사전 공격 14 고침 (P3-a conv_ok 넘침 크래시 · P3-d 생산자 값 꼴 · P3-e resume 칸 집합 · P3-f 변이 생존 넷) · 11-09 · 작업 트리 에이전트 · 시험 먼저

- 근거 = 1저자 11-09 *"다 권고대로 해줘 물어보지말고"* (메인 세션 전달 · 오버나잇) = Codex 회차 ④ 전에 고침 · P3-b · P3-c = 선언된 한정 (고치지 않음) · 사전 공격 원문 = `../preattack14/REPORT.md` (반입 · 탐침 `../preattack14/probes/` · 출력 `../preattack14/out/` · SHA256SUMS) · 처분 기록 = `docs/reviews/rint2_rr3_fix_plan_20261108.md` §11.
- 바탕 `379e85856` (두 코드 파일 = 사전 공격 대상 `7a582acf5` 와 같은 blob = 사전 공격 13 고친 판 바이트) · 코드 sha256 (`code_sha256.txt`) = `scripts/rint_r_chain.py` 78d91ad0… → 47a520e8… · `scripts/test_rint_r_chain.py` 8ba91d45… → d5e1d9ea… · 바탕 + `code.diff` (patch -p1) = 그 바이트 (`logs/apply_check.log` · `tools/apply_check.sh`) · 시험 · 변이 · 탐침 다시 = 그 바이트.
- 환경 = 이 컨테이너 Python 3.11.17 · kgy 판 3.8.20 (numpy 1.24.4 · scipy 1.10.1) · 합성 폴더 · 가짜 러너 · 모의 `run_in_group` · 실제 git 원장 (PA14B · 탐침 p3 의 recover cli) · 합성 원장 줄 (탐침 p6) · kgy · ibb · GPU 아님.
- push · 게이트 (`scripts/check_all.sh`) · 원장 (`docs/reviews/findings.json`) = 메인 세션 · **웹앱 화면 없음** (`webapp/` 에 resume_ok · RESUME_NOT_ALLOWED · RESUME_MISMATCH · arms_read · arm_public_value_problem · rint_r_chain · "재실행 자격" · RESUME_KEYS · ARM_PID_RE · ARM_SID_RE = 0 건).
- ⚠ 작업 중 컨테이너 재시작 (11-09 18 시 무렵) = 돌던 끝-끝 3.11 · kgy 판 3.8 이 끊김 → 다시 돌림 (아래 수 = 다시 돈 판) · 이미 끝난 로그 (사슬 3.11 · 변이 · 탐침 · 행 표 · 정적) = 세션 scratchpad 에 남음 · 같은 코드 바이트 (sha = `logs/static_checks.log` · `logs/probe_rerun.log` · `logs/e2e_py38_code_sha.txt`).

## 바꾼 것 (줄 = 고친 판 `scripts/rint_r_chain.py` · `tools/fn_lines.py` → `logs/fn_lines.log`)

| 결함 | 자리 | 무엇 |
|---|---|---|
| P3-a (회귀 크래시) | `arm_public_value_problem` 2195–2243 (2238–2239 `_num` 지킴 · 2235 · 2239 · 2242 `_show`) | positive cg_resid = 유한 수 (`_num` 1177–1184) 를 `RC.conv_ok` 앞에서 — 옛 = JSON 큰 정수 ±10**400 → `math.isfinite` OverflowError → arms_read_kind → prior_runs_problem → 결과 줄 셈 → recover --ledger traceback (사전 공격 13 고침 전엔 없던 길) · 사유의 큰 정수 = 자리 수만 (`_show` 1187–1191 · 반복 수 · cg_info · cg_resid) |
| P3-d (생산자 값 꼴) | `ARM_PID_RE` · `ARM_SID_RE` 2191–2192 · `arm_public_value_problem` 2213 · 2216 · 2228 | protocol_id = 'p3ca-' + 16 자리 소문자 hex 정확히 (생산자 `run_contract._ca_ext_protocol_id` 722 줄 = 유일한 'p3ca-' 생산자) · sid_fp = 32 자리 소문자 hex 정확히 (`step3_sigma._grid_fp` 232–239 줄 = blake2b 16 바이트 hexdigest · 접합 원장 fp.sid `carbon_junction` 1069 줄) · err_rel ≤ τ (`SVCF.CERT_TARGET_TOL` = 1e-4 = 증서 ⓓ 통과의 보장 오차) — 옛 = 앞자리 · 비지 않은 글 · 위 한계 없음 |
| P3-e (resume 칸 집합) | `RESUME_KEYS` 4348 · `resume_rerun_problem` 4367–4451 (4397) | 재실행 요약 resume 칸 집합 = 생산자 다섯 칸 정확히 (`ResumeRunner.__init__` 5305–5308 · 요약 = `getattr(rn, 'resume', None)` 6179 · 6387 · 그 줄을 바꾼 커밋 = ResumeRunner 첫 판 `8b2bc633a` 하나) — 덧붙인 칸 · 빠진 칸 (빠진 determinism ≠ null) · 글 아닌 열쇠 = 사유 · 집합 대조가 from · copied 대조보다 먼저 |
| P3-f (시험 빈틈) | 시험 PA14D | 변이 생존 넷 = 행 고정 (지금 코드 = 거부 · 고치기 전 · 뒤 같음): M14 copied_from True (bool ≠ int) · M18 대조 전 멈춤인데 compared 비지 않음 + determinism null · M47 compared 원소 = 정수 (객체 검사 없으면 AttributeError) · M54 from 1 < attempt.json resume_of 2 (시도 번호 바꿈 사본 `pa14_renum`) + 정직 꼴 (채택 = 시도 2 · from = resume_of = 2 · 원천 있음 · 없음) = 자격 True |

- 머리말 ★ 11-09 사전 공격 14 문단 188–192 · `resume_rerun_problem` 머리말 ① (칸 집합) · ⚠ 한정 (P3-b · P3-c).
- 시험 `scripts/test_rint_r_chain.py` = 244 줄 더함 · 지운 줄 4 (고정물 값 둘 — `ct06_pub` protocol_id 'p3ca-test' → 'p3ca-' + 16 자리 hex · sid_fp 'f' * 16 → 'f' * 32 · `PA13_PADS` pad_legacy_state 같은 두 값 = state 하나만 생산자 밖) · 옛 검사 491 그대로: PA14A (P3-a · 행 11) · PA14B (P3-a 실경로 · 실제 git 원장 recover --ledger → --add --resume 1 · 행 3) · PA14C (P3-d · 행 28 = 값 26 + τ + 정직 사다리 · 예측 판독 완료 팔 70 = 생산자 꼴 어긋남 0) · PA14D (P3-e · P3-f · 행 18).

## 수 (고치기 전 → 뒤)

| 묶음 | 고치기 전 | 고친 뒤 | 로그 |
|---|---|---|---|
| 새 검사 (`--only PA14,PA13`) | 4/8 PASS (6.4 s · 사슬 = 바탕 · 시험 = 고친 판 · PA13 4/4 · PA14 0/4) · 실패 행 A 6/11 · B 2/3 · C 20/28 · D 9/18 | **8/8 PASS** (5.8 s) · 실패 행 0 | `logs/pa14_before.log` · `logs/pa14_after.log` · 행 `logs/pa14_rows_before.json` · `logs/pa14_rows_after.json` · 요약 `logs/pa14_rows_summary.log` (`tools/rows_both.sh` · `tools/rows_dump.py`) |
| 사슬 전체 (3.11) | 491/491 PASS (409.5 s · `../preattack14/out/full_py311.log`) | **495/495 PASS** (372.9 s) = 옛 491 + 새 4 | `logs/full_py311.log` |
| 끝-끝 (3.11) | 51 PASS · 0 FAIL (749.4 s · `../preattack14/out/e2e_py311.log`) | **51 PASS · 0 FAIL** (798.2 s · 컨테이너 재시작 뒤 다시 돈 판) | `logs/e2e_py311.log` |
| kgy 판 3.8 (`scripts/check_kgy_py38.sh`) | 사슬 491/491 (523.1 s · `../preattack14/out/full_py38.log`) | **11 묶음 통과** (rc 0 · rint_r_chain 495/495 (455.1 s) · 끝-끝 51 PASS · 0 FAIL (548.3 s) · 그 밖 9 = run_contract 124/124 · step3_rint PASS · ptfe_face_alpha 242/0 · carbon_junction 547/547 · ca_ext_b6 502/0 · ca_ext_runner 151/0 · step3_target_cert 264/264 (12.2 s) · step3_conv_cert 29/29 · ca_s0_census 186/0 · 컨테이너 재시작 뒤 다시 돈 판) | `logs/check_kgy_py38.log` · `logs/py38/` |
| 변이 (`tools/mutate_pa14.py` · `--only PA14,PA13`) | 사전 공격 14 = 생존 4 (M14 · M18 · M47 · M54 · `../preattack14/out/mutation_PA13.json` · `../preattack14/out/mutation_PA13_extra.json`) | **23/23 잡힘** · 놓침 0 · 무변이 8/8 PASS (6.4 s) · 동치 1 (X01 = 놓침 · 목록 밖) | `logs/mutation_run.log` · `logs/mutation_results.json` · `logs/mutation_equiv_run.log` · `logs/mutation_equiv_results.json` |
| 탐침 다시 (`tools/run_probes.sh` · 탐침 원판 · 머리 env 규약 `PA14_SRC`) | 탐침 8 출력 = 사전 공격 14 출력과 같음 (바이트 6 · 정규화 뒤 2 = utc 시각 · 런 표지 · 폴더 요약 sha 만 · `tools/before_vs_preattack.py`) | 아래 표 | `logs/probe_rerun.log` · `logs/before_vs_preattack.log` · `logs/probe_diff.txt` (`tools/probe_diff.py`) · `probe_out/` |
| τ 위 한계 근거 (`tools/tau_bound_check.py` · 생산 `step3_conv_cert.target_judge`) | — | ⓓ 통과 383670 해 (칼날 300378) 중 e > τ 0 · 최대 e = τ | `logs/tau_bound_check.log` |
| 큰 정수 읽기 · 표시 (`tools/int_digits_check.py`) | — | 401 자리 = 읽음 · `_show` = 자리 수 · 5001 자리 = JSON 읽기 ValueError (3.11.17 · 3.8.20 둘 다) · `_show(10**5000)` = ValueError (메모리 직접 호출만) | `logs/int_digits_check.log` |
| 정적 (`tools/static_checks.sh`) | — | pyflakes rc 0 · 미정의 이름 없음 · kgy 판 3.8 py_compile rc 0 | `logs/static_checks.log` |

- 변이 23 = P3-a 4 (A01 `_num` 지킴 지움 · A02–A04 `_show` → repr) · P3-d 11 (D01 앞자리만 · D02 pid match · D03 pid 대문자 허용 · D04 pid 길이 느슨 · D05 sid 비지 않은 글 · D06 sid match · D07 sid 대문자 허용 · D08 sid 16–32 자리 · D09 τ 지움 · D10 > → ≥ · D11 τ × 10) · P3-e 4 (E01 집합 대조 지움 · E02 덧붙임 허용 · E03 빠짐 허용 · E04 determinism 뺀 상수) · P3-f 4 (M14 · M18 · M47 · M54 = 사전 공격 14 의 같은 바꿈) · 뿌리 = 작업 트리 링크 + 변이 사슬 + 고친 시험 사본 (`tools/mktree.py`) · 동치 X01 = conv_ok 사유의 cg_resid `_show` → repr (그 자리 값은 이미 `_num` 통과 = 같은 글 · `tools/mutate_pa14_equiv.py`).

## 탐침 (고치기 전 → 뒤 · 바뀐 줄 = `logs/probe_diff.txt`)

| 탐침 | 고치기 전 | 고친 뒤 |
|---|---|---|
| p3_value_domain (P3-a · P3-d) | protocol_id 'p3ca-' · 'p3ca-' + 폭 없는 공백 · 공백 · 줄바꿈 / sid_fp ' ' · NUL / positive err_rel 0.5 · 1e300 = verified · cg_resid ±10**400 = OverflowError (arms_read_kind · result_fields · result_recount · recover cli) · cg_info 10**400 사유 = 401 자리 글 | 그 여덟 = bad · cg_resid ±10**400 = bad (사유 = 자리 수만) · result_fields = timeout · 자격 False · result_recount = 결과 줄 셈 (자격 False) · recover cli = rc 0 · 자격 False · --resume rc 3 RESUME_NOT_ALLOWED · cg_info 사유 = 자리 수만 · 선언 한정 행 (반복 수 10**30 · zero 의 cert_pass · cg_* · err −0.0) = verified 그대로 |
| p1_resume_bypass (P3-e) | A1 · A4 (resume 덧붙인 칸) · A2 (빠진 determinism) = 자격 True | 자격 False · 사유 "resume 칸 집합" · A3 (빠진 compared · 옛도 거부) = 사유만 집합 쪽 · 받음 = 선언 한정 셋 (C1 · C2 · G2 = 원천 다른 곳 · 사전 공격 13 한정) 만 · 정직 셋 그대로 |
| p8_survivor_inputs (P3-f) | M14 · M18 · M47 입력 = 거부 | 거부 그대로 (시험 PA14D 행으로 고정 · M54 = PA14D 시도 번호 바꿈 행) |
| p2_chain3 (P3-c (1)) | 정직 3-시도 사슬 그대로 · a3 RESUME_MISMATCH 위조 from 1 + copied_from 1 = 자격 True | 같음 (선언된 한정 · 바뀐 줄 0) |
| p6_attempt_json (P3-c (2)) | attempt.json resume_of null + resume null + stop 2 칸 = 결과 줄 자격 True · --resume 차례 None · 풀기 전 None | 같음 (선언된 한정 · 바뀐 줄 0) |
| p7_relabel (P3-b) | R1 (7 칸) · R2 (6 칸) 복사 · 새 경계 다시 적기 = 자격 True · launch 기록 바이트 = 복사 같음 · 새 런 다름 | 같음 (선언된 한정 · 바뀐 줄 0) |
| p4_predict_resume · p5_arm_forms (정직) | 예측 재실행 셋 = resource · 자격 True · 꼴 255 + 정직 런 verified | 같음 (바뀐 줄 0 · p5 고친 뒤 = 생산자 꼴 고정물) |

## 한정 (닫지 않은 것)

- **P3-b = 선언된 한정**: 정직 RESUME_MISMATCH 요약에서 복사 · 새 경계만 다시 적으면 (탐침 p7 R1 7 칸 · R2 6 칸 · 요약만) 자격 True — 디스크로 가를 수 있는 groups/<런>.launch · end 기록 바이트 (복사 런 = 원천과 같음 · 새로 돈 런 = 다름) ↔ 원천 대조 없음 (`resume_rerun_problem` 머리말 ⚠).
- **P3-c = 선언된 한정**: (1) 요약 resume.from ↔ 원장 사슬 끝 (`adoption` effective) 결합 없음 (탐침 p2_chain3) · (2) attempt.json resume_of ↔ 원장 항목 결합 없음 (탐침 p6 · `attempt_order_problem` · 풀기 전 `resume_chain_problem` = attempt.json 꼴만 · 원장 항목 대조 = 판정 · 합치기의 `found_attempts_problem` 몫).
- P3-d: protocol_id · sid_fp 의 꼴만 (그 값이 이 런의 것인지 = 값 계약 밖 · 다른 런 판독 완료 기록 옮겨 붙임 = 사전 공격 13 처분 §10-4 그대로) · err_rel −0.0 = verified 그대로 (사전 공격 14 탐침 표지 trivial) · 반복 수 위 한계 없음 · zero 의 증서 칸 = 그대로.
- P3-a: `_show` = float 로 못 바꾸는 정수만 자리 수 (그 밖 긴 값 = repr) · 4300 자리 넘는 정수 = JSON 읽기가 먼저 ValueError (3.11.17 · 3.8.20 실측) · 메모리 직접 호출 `_show(10**5000)` = ValueError · kgy 3.8.10 의 자리 한도 = 미확인.
- 안 돌린 것 = `scripts/check_all.sh` 전체 (메인 세션) · 이 고침의 독립 재공격 · Codex 회차 ④ (메인 세션) · 사전 공격 14 변이 도구 원판 (`../preattack14/probes/mutate.py` = 바탕 패턴 · 고친 판에선 패턴이 바뀜 → 같은 생존 넷 바꿈을 `tools/mutate_pa14.py` 로).

## 다시 만들기

- 뿌리: `tools/mk_before.sh` (사슬 = 바탕 · 시험 = 고친 판 · 새 검사 고치기 전) · `tools/mk_base.sh` (사슬 · 시험 = 바탕 · 탐침 고치기 전) · `tools/mktree.py`.
- 행 표 `bash tools/rows_both.sh` · 변이 `python3 tools/mutate_pa14.py <작업 트리> <결과 폴더> 2` · 동치 `python3 tools/mutate_pa14_equiv.py <작업 트리> <결과 폴더>` · 탐침 `bash tools/run_probes.sh both` · 끝-끝 + kgy 판 `bash tools/run_e2e_py38.sh` · 모으기 `bash tools/assemble.sh` · ⚠ 도구 안 절대 경로 = 이 세션 scratchpad · 작업 트리 (다른 자리에서는 바꾼다).
