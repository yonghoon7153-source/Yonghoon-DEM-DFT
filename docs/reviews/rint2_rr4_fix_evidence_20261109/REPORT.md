# rint2_rr4_fix — Codex 회차 ④ 수정 계획 Q1–Q3 (가) 고침 (PC14-02 · PC14-03 재개 출처 공통 검증 · RR4-01 변이 회계) · 11-09 · 작업 트리 에이전트 · 시험 먼저

- 근거 = 1저자 11-09 *"권고대로"* = `docs/reviews/rint2_rr4_fix_plan_20261109.md` §5 Q1–Q3 (가) · 판정문 `docs/reviews/codex_review_rint2_rr_round4_20261109.md` §3 ① · §4 · 반례 입력 = `docs/reviews/codex_rint2_rr_round4_evidence_20261109/resume_attack/frozen_cases/` (바이트 그대로 · RR4A Z1–Z4 · RR4B P8 · P9).
- 바탕 `e48e5fa04` (두 코드 파일 = 리뷰 핀 `1f9f3607e` 같은 바이트 · 47a520e8… · d5e1d9ea…) · 고친 판 = 바탕 + code.diff (patch -p1 같은 바이트 · `logs/apply_check.log`) · `code_sha256.txt` · 시험 먼저 = 고친 시험 (92998cbc…) 을 바탕 사슬에 먼저.
- 환경 = Python 3.11.17 · kgy 판 3.8.20 (numpy 1.24.4 · scipy 1.10.1) · 합성 시도 폴더 · 실제 ResumeRunner + 가짜 _execute · 실제 git 원장 (scratch · --stage recover --ledger) · GPU 아님 · 웹앱 = 없음 (`logs/webapp_grep.log`) · 게이트 · 원장 · push = 메인 세션.
- 이 문서 = 작업 트리 에이전트의 보고문을 메인 세션이 옮겨 적은 것 (에이전트 쪽에서 보고 파일 쓰기가 막혀 있었다 · 수 = 아래 로그와 메인 세션이 한 줄씩 대조함).

## 바꾼 것 (줄 = 고친 판 `scripts/rint_r_chain.py` · `logs/fn_lines.log`)
| 자리 | 줄 | 무엇 |
|---|---|---|
| resume_provenance_problem | 4617–4655 (ⓐ 4635 · ⓑ 4641 · 원천 4647 · ⓒ 4650 · ⓓ 4653 · RESUME_PROV 4484) | 사유 = "재개 출처" + [ⓐ]·[ⓑ]·[원천]·[ⓒ]·[ⓓ] · 요약 없는 시도 = ⓐ 만 · 새 시도 = ⓐ·ⓑ 만 · 멈춘 런 = rerun 이어도 ⓐ–ⓒ |
| ⓐ attempt_entry_diff | 5091–5098 | found_attempts_problem (5101–5132) 과 같은 함수 · 동작 그대로 |
| ⓑ resume_from_problem | 4494–4509 | type(from) is int ∧ from = adoption upto=n effective / 항목 null ⇒ 요약 resume null |
| 원천 resume_source_locate | 4512–4533 | found 또는 같은 바탕 · 결과 줄 폴더 이름 · 링크 아님 · 하나 · attempt.json 번호·대상 · 요약 sha · 못 찾음 = [원천] fail-closed |
| ⓒ resume_boundary_problem | 4543–4590 (_src_run_done 4536–4540) | 복사 런 = 새 런 앞 · copied_from = from · 원천에서 끝난 런 · launch/end 바이트 = 원천 · payload = 원천 / 첫 새 런 = 원천에서 안 끝난 런 · 새 런 launch ≠ 원천 (원천에 없으면 건너뜀) |
| ⓓ resume_first_new_problem | 4593–4614 (resume_recompare 4487–4491) | 실제 첫 새 런 = rerun · 원천 payload 다시 대조 = compared |
| 결과 줄 쓰기 | attempt_result 4895–4900 → attempt_close 5039 · recover_ledger 8278 | result_fields_ledger 4865–4877 · 자격 False · 사유 = 커밋 글 · 화면 · 칸 · 원인 그대로 |
| 다시 셈 | _result_recount 4987–5005 ← result_recount · result_line_problem 5017–5028 | st · found 를 주면 같은 셈 함수 · 부르는 자리 ledger_inputs_check 5155 · target_ledger_problem 5224 · resume_chain_problem 3817 |
| 다음 재개 허용 | attempt_order_problem 3585 · resume_chain_problem 3811 | resume_chain_provenance_problem 4658–4678 (시작 기록 자리) · 사슬 시도마다 → RESUME_NOT_ALLOWED |
| 그대로 | result_fields · attempt_result_line · ResumeRunner._src_done 5595–5601 | _src_done sha256 b530c2ad… = 바탕 (`logs/src_done_sha.log`) |

## 수 (고치기 전 → 뒤)
| 묶음 | 고치기 전 | 고친 뒤 | 로그 |
|---|---|---|---|
| --only RR3,PA13,PA14,RR4 | 15/19 (RR4 = RR4C 만) · 바탕 시험 14/14 | 19/19 (11.9 s) | `logs/rr4_before.log` · `logs/base_subset.log` · `logs/rr4_after_final.log` · `logs/rr4_rows_summary.log` |
| RR4A 음성 9 × 세 자리 | 9/9 받음 | 9/9 거부 · N1·N2·Z1·Z2 [ⓒ] · N3·N3a·Z3 [ⓐ] · N4·Z4 [ⓑ] · 다시 셈 None | 위 |
| RR4B 양성 12 | 행동 같음 · 다시 셈 인자 없음 | 12/12 | 위 |
| RR4C (RR4-01) | 통과 | 통과 · M56 잡힘 | 위 |
| RR4D | F1 자격 True | F1·F2 [원천] · F3 [ⓓ] | 위 |
| 사슬 3.11 | 495/495 | 500/500 (355.5 s) | `logs/full_py311.log` |
| 끝-끝 3.11 | 51 | 51 PASS · 0 FAIL (707.7 s) | `logs/e2e_py311.log` |
| kgy 판 3.8 | 11 묶음 | 11 묶음 · 사슬 500/500 (464.1 s) · 끝-끝 51/0 (540.7 s) · 그 밖 9 그대로 | `logs/py38_bundles.log` · `logs/py38/` |
| 변이 | — | 12/12 잡힘 · 무변이 5/5 | `logs/mutation_rr4.log` · `logs/mutation_results.json` |
| Codex 재개 탐침 무변경 | 자격 True 단언 통과 | AssertionError 181 줄 (기대한 뒤집힘) | `logs/probe_rerun.log` |
| 정적 | — | pyflakes 0 · 미정의 없음 · 3.8 py_compile 0 | `logs/static_checks.log` |

변이: MA (ⓐ) → N3a · MB (ⓑ) → N4·Z4 · MC (ⓒ) → N1·N2·Z1·Z2 · MD (ⓓ) → RR4D F3 · MS (원천) → F1·F2 · MAB → N3a·N4·Z4 · W1 (차례 부름) → 차례 9/9 None · W2 (풀기 전 부름) → 사슬 9/9 ATTEMPT_LEDGER_MISMATCH · W3·W4·W5 (쓰기 · 다시 셈 셈 함수) · M56 (is_dir → exists) → RR4C.

## 하위 결정 = fail-closed 구현 · 정직 흐름 깨짐 없음 (사슬 500 · 끝-끝 51 · kgy 판 11 묶음 · RR4B 12) → STOP 없음.

## 벗어남
① pa13_ledger 항목 기계 'synthetic' → MACH (기대값 그대로 · `logs/pa13_old_fixture_check.log`)
② 사전 공격 14 SHA256SUMS REPORT.md 줄 갱신 (옛 해시 = 반입 증거 그대로)
③ 결과 줄 칸 · 원인 그대로 (자격만 False · 사유 = 커밋 글 · 화면)

## 한정
_src_done 그대로 · 모든 사본 일관 위조 = 계약 밖 · 요약 없는 시도 = ⓐ 만 · ⓐ `!=` (True == 1) · 새 런 launch 다름 = 원천에 같은 이름 있을 때만 · 다음 재개 = 시작 기록 바탕 (옮김 · 지움 = 거부).

## 다시 만들기
`tools/mktree.py` · `tools/apply_check.sh` · `tools/rows_dump.py` · `tools/rows_summary.py` · `tools/mutate_rr4.py` · `tools/static_checks.sh` · `tools/fn_lines.py` · `tools/src_done_sha.py` · 무결성 `SHA256SUMS`.
