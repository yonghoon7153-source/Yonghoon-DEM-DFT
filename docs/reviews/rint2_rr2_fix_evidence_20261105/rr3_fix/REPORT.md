# rr3_fix — RR3-01 (arms_read 구조 계약) · RR3-02 (요청서 한정표 정정) · 11-08 · 작업 트리 에이전트 · 시험 먼저

- 이 파일 = 11-09 소급 작성 — 11-08 당시 보고 파일 쓰기가 막혀 계획 `docs/reviews/rint2_rr3_fix_plan_20261108.md` §9 + 이 폴더 로그가 그 자리였다 (§9 의 "REPORT.md = 만들지 않았다" 를 이 파일이 채운다).  숫자 = 전부 이 폴더 로그 · 계획 §9 에서 옮김 (새로 잰 것 없음).
- 바탕 `40d9658c0` · 코드 sha256 (`logs/code_sha256.txt`) = `scripts/rint_r_chain.py` 48f0e7ff… → b37ef7c6… · `scripts/test_rint_r_chain.py` fedba635… → d83539a1… · 깨끗한 바탕 + `apply_chain.py` · `apply_tests.py` (이 폴더) = 그 바이트.
- 환경 = 계획 §9 머리 (Python 3.11.17 · kgy 판 3.8.20 · 합성 폴더 · 가짜 러너 · 모의 `run_in_group` · 실제 git 원장).  push · 게이트 · 원장 = 메인 세션 · 웹앱 화면 없음 (계획 §9).

## 바꾼 것 (계획 §9-1 표가 정본)
- 새 `ARM_FILE_ID_KEYS` · `ARM_SHA256_RE` · `arms_read_record` (생성 = 생산자 셋이 부름) · `arm_file_prefix` · `arms_read_kind` (verified / file_ids / empty / bad) · `prior_runs_problem` = verified 앞 런만 자격.
- 생산자 셋 (`Runner._execute` · `ResumeRunner._copy` · `MergeFetch.run`) = 성공 `arms_read_record(arms_)` · 실패 `arms_read_record(outdir=outdir)`.
- RR3-02 = 요청서 `docs/reviews/codex_rint2_rr_round3_request_20261108.md` 표지 (`rr3_02_check.py` · `logs/rr3_02_rg_check.log` = 바뀐 줄 [83, 84, 86, 94, 135, 140, 154] · 표지 줄과 같음 True · 결과 OK).

## 수 (고치기 전 → 뒤)

| 묶음 | 고치기 전 | 고친 뒤 | 로그 |
|---|---|---|---|
| 새 시험 + 고정물 둘 (`--only RR3,CT06,PC12C`) | 3/8 PASS (5.7 s) · 실패 RR3A · RR3B · RR3C · RR3D · RR3E | 8/8 PASS (6.2 s) | `logs/before_RR3.log` · `logs/after_RR3.log` · 행 `logs/before_RR3_rows.json` · `logs/after_RR3_rows.json` · 요약 `logs/before_RR3_summary.txt` · `logs/after_RR3_summary.txt` |
| 겨냥 (`--only RR3,CT06,PC12,CT08,RC01`) | — | 15/15 PASS (11.0 s) | `logs/after_RR3_targeted.log` |
| 사슬 전체 (3.11) | 481/481 PASS (364.3 s) | 487/487 PASS (465.7 s) | `logs/before_chain_full_py311.log` · `logs/after_chain_full_py311.log` |
| 옛 시험 파일 × 고친 사슬 | — | 479/481 PASS (512.4 s) · 실패 CT06 · PC12C = 기대 바뀜 (계획 §9-3) | `logs/cross_oldtests_fixedchain.log` · `logs/cross_oldtests_fixedchain_rows.json` |
| 끝-끝 (3.11) | 51 PASS · 0 FAIL (807.4 s) | 51 PASS · 0 FAIL (881.3 s) | `logs/before_e2e_py311.log` · `logs/after_e2e_py311.log` |
| kgy 판 3.8 (`scripts/check_kgy_py38.sh`) | — | 11 묶음 통과 · rc 0 | `logs/check_kgy_py38.out` · `logs/py38/` |
| 변이 (`mutate_rr3.py`) | — | 23/23 잡힘 · 무변이 9/9 PASS (7.7 s) · 되돌림 sha 같음 True | `logs/mutation_rr3.out` · `logs/mutation_rr3.json` |

## Codex 탐침 다시 (`probe_rerun/` · 계획 §9-4)
- 탐침 sha256 7f335c75… · 사슬 b37ef7c6… · 원본 그대로 = rc 1 (AssertionError `ledger_rows[1]['attempt_order_problem'] is None` = RR3-01 존재 assert · 기대한 뒤집힘 · PASS 로 바꾸지 않음) · oracle 사본 (`probe_rerun/oracle.diff`) = rc 0.
- 편집 뒤 결과 ["timeout", false] · 원장 original · edited = 둘 다 RESUME_NOT_ALLOWED · 복사 다시 읽기 ARM_JSON_COUNT · 잎 159 → 160 · 다른 잎 10 · 사슬 쪽 행 175 / 175 같음 (`probe_rerun/rerun_report.json` · `probe_rerun/leaf_diff.json`).

## 한정 (계획 §9-6 그대로)
- 구조 계약 = 값 대조 안 함 (sha256 ↔ 디스크 · 옮겨 붙인 기록 · 일관 위조 = 밖) · ARM_PUBLIC 의 그 밖 칸 값 꼴 안 봄 → 그 같은 부류를 사전 공격 13 이 P2-2 로 찾았다 (`../preattack13/REPORT.md`) · 고침 = `../pa13_fix/` (11-09).
- 이 고침의 독립 재공격 = 사전 공격 13 (11-08 · `../preattack13/`) · `rint_r_chain.py` sha 바뀜 = R 계획 code key 바뀜 (계획 §7 ④).
