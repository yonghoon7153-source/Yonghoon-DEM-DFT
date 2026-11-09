# 고침 C — 사전 공격 15 처분 (PC15-01 – 06) · 11-09

- 작성 = 고침 C 작업 트리 에이전트의 마지막 보고 (메인 세션이 이 파일로 옮김 · 내용 그대로 · 작업 트리 경로 줄만 뺌).
- 커밋 = 작업 트리 커밋 f8cc7732e (로컬 · push 안 함 · 부모 `69d714d09`) → 가지 B `db8322e70` (`cherry-pick -x` · 진행 기록 끝줄 충돌 = 둘 다 살림 · 나머지 141 파일 blob 같음).  원장 (`docs/reviews/findings.json`) 등재 · 게이트 · push = 메인 세션.
- **STOP 항목 없음.** 정직 흐름을 깨야만 고칠 수 있는 항목은 없었다. 생산자 코드 (`Runner._execute` · `run_in_group` · `ResumeRunner.run` · `stop_trace`) 를 먼저 읽고 가드를 맞췄다.
- 증거 = 이 폴더 (code.diff · code_sha256.txt · logs · tools · SHA256SUMS).  사전 공격 15 반입 = `docs/reviews/rint2_rr4_fix_evidence_20261109/preattack15/` (REPORT.md · probes 18 · out 23 · 바이트 그대로 · td/ 와 __pycache__ 는 뺐다 · SHA256SUMS 42 줄).
- 코드 sha256: `scripts/rint_r_chain.py` d0e04017… → 986bbdb3… · `scripts/test_rint_r_chain.py` 92998cbc… → 98480e89… · 바탕 + code.diff = 고친 판, 바이트 같음 2/2 (logs/apply_check.log).
- 문서: 수정 계획 `docs/reviews/rint2_rr4_fix_plan_20261109.md` §7 · 상태 줄 한 줄 · 진행 기록 한 줄.  `check_doc_refs` rc 0 · `check_review_findings` rc 0 · `--ban-sweep` rc 0.

## 1. 바꾼 자리 (`scripts/rint_r_chain.py` · 바탕 줄 → 고친 판 줄)

| 함수 · 상수 | 바탕 | 고친 판 | 무엇 |
|---|---|---|---|
| `resume_rerun_problem` ⑤ | 4389–4476 | 4389–4479 | 다시 대조를 `resume_recompare_run` 으로 = 디스크 출력 폴더 기준 (옛 = 요약 outdir) (PC15-02) |
| `RESUME_PROV` 주석 · `RUN_ORDER_RE` (새) | 4484 | 4489 · 4492 | 표지 [꼴] 추가 · [원천] = 결과 줄 안 씀 · 런 번호 차례 |
| `run_dirs` (새) | — | 4502–4508 | 런의 디스크 출력 폴더 `<런>` · `<런>_arm…` (`stop_trace` 와 같은 이름 규칙) |
| `resume_recompare_run` (새) | — | 4511–4518 | 원천 ∪ 이 시도의 디스크 폴더마다 `resume_recompare` |
| `run_end_ok` (새) | — | 4521–4525 | 결합 · 끝 rc `rc_success` · 확인 True |
| `resume_disk_rerun` (새) | — | 4528–4549 | 디스크상 첫 미완료 런 = 원천 ∪ 이 시도 groups 시작 기록 · 번호 차례 · `_src_run_done` · 런 이름 꼴 밖 = 사유 |
| `resume_boundary_problem` (ⓒ) | 4543–4590 | 4601–4673 | 아래 다섯 줄 (PC15-02) |
| `resume_first_new_problem` (ⓓ) | 4593–4614 | 4676–4707 | 디스크 rerun 이 이 시도에서 끝났으면 다시 대조 (PC15-01) |
| `resume_provenance_problem` | 4617–4655 | 4710–4764 | [꼴] (4736) · 요약 없는 길 (4746) → 원천 → 디스크 rerun → ⓒ · ⓓ |
| `class ResultHeld` · `resume_prov_unconfirmed` (새) | — | 5004–5013 | PC15-03 |
| `attempt_result` | 4895–4900 | 5016–5027 | 사유 [원천] → `ResultHeld` (5022) |
| `attempt_close` | 5031–5046 | 5158–5177 | `ResultHeld` → ATTEMPT_OPEN · rc 3 (5169) |
| `attempt_entry_diff` | 5091–5098 | 5222–5230 | 형까지 같아야 같음 (5227) (PC15-04) |
| `recover_ledger` | 8210–8292 | 8342–8426 | 주석만 (`ResultHeld` = 있던 Stop 처리 = 못 쓴 수 · 화면 사유) |

`resume_boundary_problem` 의 새 가드 다섯: 4618 resume.rerun = 디스크 rerun · 4649 첫 새 런 = 디스크 rerun (옛 가드 "첫 새 런 ≠ 원천에서 끝난 런" 대신) · 4654 새 런 groups 시작 · 끝 결합 · 4658 디스크 폴더 ⊆ 기록 outdir · 4661 멈춘 런 앞 새 런 = 이 시도에서 끝남 + 폴더 있음.

시험: 상주 검사 RR5A–F 여섯 (행 52) 새로 · RR4D F1 기대값 바꿈 (PC15-03 뜻).  생산자 조각 11 (`_src_done` · `run` · `_copy` · `_execute` · `_prepare` · `run_in_group` · `stop_trace` · `run_traces` · `record_outdir` · `resume_leftovers` · `group_pair`) = 바탕과 바이트 같음 11/11 (logs/producer_sha.log · logs/src_done_sha.log).

## 2. 수 (고치기 전 → 뒤 · 로그 = 이 폴더 logs/)

| 시험 | 고치기 전 | 뒤 | 로그 |
|---|---|---|---|
| 시험 먼저 `--only RR3,PA13,PA14,RR4,RR5` (바탕 = 69d714d09 와 scripts · webapp 779/779 같은 사본) | 18/25 (FAILED RR4D · RR5A–F) | 25/25 | tests_first_base.log · after_subset.log · base_tree_check.log |
| 행 단위 (RR5 52 + RR4D 3) | 55 중 23 다름 | 0 | rr5_rows_base.{log,json} · rr5_rows_after.{log,json} |
| 사슬 전체 3.11 | 500/500 (회차 ④) | 506/506 (409.6 s) | full_py311.log |
| 끝-끝 3.11 | 51 | 51 PASS · 0 FAIL | e2e_py311.log |
| kgy 판 3.8.20 · numpy 1.24.4 · scipy 1.10.1 | 11 묶음 | 11 묶음 통과 (사슬 506/506 · 끝-끝 51 · 그 밖 9) | py38_bundles.log · py38/ |
| 변이 (같은 부분집합) | 사전 공격 15 때 46 중 잡힘 19 | 71 중 잡힘 68 · 생존 2 (동등) · 적용 안 됨 1 · NOMUT 25/25 | mutation_final.{log,json} · 1 차 = mutation_c_1st.* |
| 정적 점검 (pyflakes · 미정의 이름 · 3.8 py_compile) | — | rc 0 | static_checks.log |
| ⑤ 이름 꼴 자기 점검 | — | 7/7 사유 · traceback 0 | rerun_type_selfcheck.log |
| 웹앱 grep | — | 0 건 (재개 자격 · 원장 화면 없음) | webapp_grep.log |

## 3. 사전 공격 15 탐침 무변경 재실행 (원 = 반입 out/ (e94f09905))

| 탐침 · 꼴 | 원 | 새 |
|---|---|---|
| p1 (P2-1 a) signal_after 요약 위조 | 세 자리 받음 | 거부 [ⓓ] (recover 자격 False · 차례 · 사슬 RESUME_NOT_ALLOWED [ⓓ]) |
| p2 (P2-1 b) 요약 지움 | 받음 | 거부 [ⓓ] |
| p13 정직 signal_after + 다른 payload | 받음 | 거부 [ⓓ] (기대한 뒤집힘) |
| p8 (P2-2) 기록 outdir 다른 이름 | 받음 | 거부 (폴더 증거 ⑤ 가 디스크 폴더로 다시 대조 · 표지 없음) |
| p9 (P2-2) 런 이름 바꿈 | 받음 | 거부 [ⓒ] |
| p3 (P2-3) recover 전 원천 옮김 | recover rc 0 · 줄 False [원천] · 판정 MISMATCH | recover rc 3 · 결과 줄 없음 |
| p6 원천 링크 | recover 줄 False [원천] | recover rc 3 · 줄 없음 (차례 · 사슬 거부 그대로) |
| p7 (P3-1) 요약 없는 길 resume_of true · 1.0 | 받음 · found_attempts_problem None | 거부 [ⓐ] · found 사유 |
| p14 · p15 (P3-2) runs = int · stop = str | TypeError · AttributeError (traceback) | 사유 [꼴] · RESUME_NOT_ALLOWED |
| p4 H1–H5 · p10 H6 · H7 · p11 정직 | 받음 | 받음 (그대로) |
| p5 V01–V18 변형 | 거부 17 · V07 받음 | 같음 |

- p13 의 짝 (정직 signal_after + 같은 payload) = 행 A4 · 통과.  p3 대조군 (원천 안 옮김) = ok 그대로 · 원천을 되돌린 뒤 recover = 자격 True · 판정 ok (행 C1).  p7 resume_of 1 (정직) = 그대로 받음 · null = 그대로 거부.  p12 · p15b = 다시 돌리지 않음 (p12 = 변이 실행이 대신 · p15b = 바탕 대조 기록).
- Codex 회차 ④ 재개 탐침 (무변경 · sha256 83622e5a…) = AssertionError 181 줄 (회차 ④ 와 같은 단언 · 계속 기대한 뒤집힘 · logs/codex_probe_rerun.log).  출력 = logs/probe_compare.log · logs/pa15_probes_out/.

## 4. 변이

- 구성 71 = mutate15 목록 46 (바이트 그대로 41 · 고친 판 글자에 맞춰 같은 뜻으로 옮김 4 = b_drop · c_first_new_done · new_attempt_no_early_return · write_old · 적용 안 됨 1 = d_name) + 새 가드 25.
- 결과 = 잡힘 68 (mutate15 43 + 새 25 · 새 가드 생존 0) · 생존 2 (동등) · 적용 안 됨 1.
- 사전 공격 15 가 지목한 변이 → 그것만 가르는 행 (logs/mutant_rows.log): entry_no_machine → F1 · c_bytes → F2 · F3 · c_launch_only → F2 · c_end_only → F3 · c_payload → F4 · loc_digest → F5 · R1 짝 c_copy_srcdone → F6 · F18 · R2 짝 c_first_new_done (새 가드) → B7 · c_new_launch_same → F7 · 다시 셈 자리 셋 (chain · tlp · lic _recount_nost) → F8 · close_old (행동) → C2 · C3 · N_src_names_only → B0c · B9.
- 생존 2 = 동등: loc_symlink (원천 폴더가 링크면 `folder_digest` = None · 원장이 결과 줄 sha 를 64 hex 로 강제 → 같은 [원천] · 사유 글만 다름) · c_new_launch_missing_ok (새 런 결합 `group_pair` = `read_regular_file` 이 이미 launch 읽기를 요구 · 차이 = 두 읽기 사이 경쟁뿐 · 추정 · 시험으로 만들 수 없음).
- 적용 안 됨 1 = d_name ("멈춘 런 = rerun 이면 대조 안 함" 가드를 디스크 판단으로 바꿔 없앰).

## 5. 벗어남

1. 작업 트리가 빈 커밋 `bf0dd1a32` 에서 시작 → 그 작업 트리에서만 `git reset --hard 69d714d09` 로 지시된 바탕에 맞춤.
2. PC15-02 "출력 폴더가 있어야" = 멈춘 런 앞 새 런 (끝난 런) 에만 · 새 런 전부에는 "디스크 폴더 ⊆ 기록 outdir" 만 (멈춘 런은 러너가 폴더를 만들기 전에 죽을 수 있음 · 생산자 대조 · 거짓 거부 방지).
3. p8 = 공통 검증 표지가 아니라 폴더 증거 ⑤ 가 먼저 자격 False · 세 자리 모두 거부 · 커밋 글 표지 없음 (행 B1).
4. ⓒ 옛 가드 (첫 새 런 ≠ 원천에서 끝난 런) · ⓓ 옛 가드 (멈춘 런 = rerun) → 디스크 판단으로 바꿈.
5. PC15-05 멈춤 이름 = 바탕 `e48e5fa04` 와 다름 (고친 판 = 차례 · 사슬 모두 RESUME_NOT_ALLOWED + [꼴] · 바탕 = 차례 None · 사슬 ATTEMPT_LEDGER_MISMATCH) · 같은 "Stop · 사유" 꼴 · traceback 없음.
6. RR4D F1 기대값 [0, False, [원천], False] → [3, None, [], True] (PC15-03).
7. 변이 1 차 (71 중 잡힘 67 · N_5_old_outdir 패턴이 두 곳에 걸림) 뒤 정직 행 B0c (탐침 p4 H2 꼴) 추가 → 최종 시험으로 변이 전부 다시.
8. `ResultHeld` 의 Stop 코드 = ATTEMPT_LEDGER_MISMATCH · 사슬 화면 = ATTEMPT_OPEN.

## 6. 한정

1. 결과 줄을 쓴 뒤 원천을 지우거나 옮기면 다시 셈이 [원천] 으로 멈춘다 (판정 · 합치기 거부 = 맞는 동작 · 규칙 "원천 시도 폴더를 지우거나 옮기지 않는다").
2. [원천] 때문에 못 쓴 정직 시도 = recover 가 "못 쓴 수" 로 남김 → 사람이 원천을 같은 바탕에 되돌린 뒤 recover (자동 아님).
3. 디스크상 첫 미완료 런 = groups 시작 기록 이름 (`<앞자리><번호>_<역할>`) 에 기댄다 · 꼴 밖 이름 = [ⓒ] 로 막음 (fail-closed) · graph 원천 런 = 다른 폴더 · 영향 없음.
4. V07 (중복 복사 기록) = 그대로 받음 (해 없음 · 바탕도 자격).
5. 모든 사본을 일관되게 고친 위조 = 계약 밖 · `ResumeRunner._src_done` 그대로.
6. 런 기록과 시작 기록 사이 예외 = CHAIN_EXCEPTION (원래 자격 없음 · 공통 검증까지 가지 않음).

## 7. 메인 세션에 넘긴 것

- 원장 PC15-01 – 06 등재 · claimed_fixed · 게이트 · push = 메인 세션.
- 원장 PC14-03 의 회귀 글 "RR4D F1 · F2 [원천]" 은 이제 맞지 않는다 (F1 = "결과 줄 없음" · PC15-03) → 메인이 메모로 정정.
- 다음 = Codex 회차 ⑤ 짧은 재확인 (PC14-02 · 03 · RR4-01 + PC15-01 – 06).
