# 사전 공격 15 — e94f09905 (부모 e48e5fa04 · 회차 ④ 고침) · 11-09 · 독립 · diff 만 · 판정 = P1 0 · P2 3 · P3 3

> 이 파일 = 독립 에이전트가 마지막 메시지로 돌려준 보고문을 메인 세션이 그대로 옮긴 것 (에이전트 쪽 보고 파일 쓰기 막힘 · 탐침 · 출력 = 같은 폴더 probes/ · out/ · 임시 폴더 out/td 는 뺌).  메인 세션 재현 (11-09 · 같은 사본 pa15/tree) = p1_sigafter · p8_outdir · p9_rename · p3_moved_source · p13_honest_sigafter 다섯 출력이 에이전트 출력과 같음 (경로 · seconds 뺀 비교).

판정문에 나온 반례 (R1 · R2 · attempt-null · 3 시도 from 다시 결속 · 동결 Z1–Z4) 는 세 자리에서 모두 거부된다. 정직 흐름 10 꼴에서도 거짓 거부는 없었다.
그러나 새 부류 둘이 세 자리 (결과 줄 쓰기 · 다시 셈 · 다음 재개 허용) 를 모두 통과한다. 원장이나 디스크는 건드리지 않고 요약만 고친 꼴이다. 보장 5 (쓰기 ↔ 다시 셈 대칭) 는 원천 위치가 바뀌면 깨진다.
- 줄 번호 = e94f09905 의 scripts/rint_r_chain.py
- 탐침 · 출력 폴더 = 이 폴더의 probes/ · out/ (작성 때 자리 = 세션 scratchpad pa15/)
- 실행 = Python 3.11.17 · 합성 입력 · scratch git 원장만

## P2-1 — 재실행 런이 디스크에서는 끝났는데 대조 기록이 없으면 자격 True가 되고, 다음 재개가 그 런을 대조 없이 복사한다
- 결함 한 줄: 재실행 런 (resume.rerun) 의 끝 기록 사슬 쪽이 원인 None · rc 0 · 확인 True 다. 즉 러너는 끝났고, 남은 payload 는 원천과 다르다. 그런데 요약이 "대조 전 멈춤" 이거나 요약이 아예 없으면 ⓓ 가 대조하지 않는다. 그 결과 자격 True 가 되고, 다음 `ResumeRunner._src_done(L02)` 가 True 를 내어 그 런을 복사한다. 결정성 대조는 끝내 일어나지 않는다.
- 탐침: probes/p1_sigafter.py → out/p1_sigafter.json · probes/p13_honest_sigafter.py → out/p13_honest_sigafter.json · probes/p2_orphan.py → out/p2_orphan.json
- 입력: 정직 RESUME_MISMATCH (`rr4_two(…,'changed-ceiling')`) 에서 두 길.
  - (a) 요약 6 칸만 고침: stop.code → RUNNER_RC (run = L02 그대로) · L02 기록 rc 0 → null · group_cause → 'signal_after' · arms_read → [] · resume.compared → [] · determinism → null.
    - 실제 `ResumeRunner.run` 의 signal_after 가지로 만든 정직 요약과, seconds 칸을 빼면 같다 (p13: `honest_summary_equals_forged_except_seconds` True).
  - (b) ladder_summary.json 하나를 지움. 이것은 머리말에 선언된 한정 "요약 없는 시도 = ⓐ 만" 에 해당한다.
- 기대: 자격 False. 원천 남은 payload 가 디스크에 있고, 다시 대조하면 `[{same: false}]` 다.
- 실제 ((a) · (b) 둘 다): 쓰기 `attempt_result` 가 True · 사유 없음 · 실제 recover CLI 는 rc 0 · 결과 줄 True · 다시 셈 None · 차례 None · 사슬 None · 다음 재개 `_src_done(L02)` 는 True · 정직 signal_after (p13) 도 같다. 즉 비결정 재실행이 대조 없이 전파된다. 이 고침 전부터 있던 설계 구멍이지만, 이번에 ⓓ 가 보장한다고 적은 범위 안이다.
- 자리: :4599–4600 (`resume_first_new_problem`: 멈춘 런 = rerun 이면 None) · :4638–4639 (요약이 없으면 ⓐ 만 본다) · :5595 (`_src_done`: 끝 rc 0 이면 복사 · 그대로 둔 자리)
- 고침 제안: 항목 resume_of 가 있는 재실행 시도에서, 디스크 기준으로 원천에서 처음 끝나지 않은 런이 이 시도에서 끝났으면 (사슬 쪽 원인 None · rc 0 · 확인) 원천 남은 payload ↔ 그 런 폴더를 다시 대조한다. 멈춘 런이 무엇인지, 요약이 있는지와 무관하게 한다. 다르면 사유를 낸다.

## P2-2 — 새 런 기록의 이름 · outdir 가 디스크와 묶이지 않아, ⓓ (와 옛 ⑤) 가 없는 폴더끼리 대조한다
RESUME_MISMATCH 를 숨기는 길이다. 원천 payload 가 남아 있는 PC13-01 계열이고, PC14-02 처럼 "요약 런 기록 ↔ 디스크 모순" 이다. Codex 가 같은 부류로 보면 P1 로 올릴 여지가 있다.
- 탐침: probes/p8_outdir.py → out/p8_outdir.json · probes/p9_rename.py → out/p9_rename.json
- 입력 (둘 다 정직 RESUME_MISMATCH 요약만 고침):
  - P8: stop → TIME_LIMIT/L03 (런 기록 없음) · L02 기록 arms 1 → 2 · outdir L02_ceiling_arm1 → L02_ceiling_arm2 · arms_read 에 판독 완료 꼴 둘째 팔 추가 (index 1 · …_a1.json · sha 'e'*64) · compared [] · determinism 'assumed'
  - P9: L02 이름 → L02_ceilingX · outdir → L02_ceilingX_arm1 · resume.rerun 도 같이 바꿈 · compared [] · assumed · stop TIME_LIMIT/L03.
- 기대: 거부. 요약이 주장한 런 폴더나 그룹 기록이 디스크에 없고, 실제 L02_ceiling_arm1 의 payload 는 원천과 다르다.
- 실제: 세 자리 모두 통과 (쓰기 True · recover rc 0 · True · 다시 셈 None · 차례 None · 사슬 None) · 디스크: attempt_2/L02_ceiling_arm2 가 없다 (P8) · groups/L02_ceilingX.* 와 그 폴더가 없다 (P9) · 다음 재개 `_src_done(L02_ceiling, …_arm1)` 는 True.
- 자리: :4580–4588 (새 런은 원천에 같은 이름 launch 가 없으면 continue · 이 시도의 launch 와 런 폴더가 있는지는 보지 않는다) · :4604–4608 (요약 outdir 를 그대로 다시 대조) · :4460–4470 (옛 ⑤ 도 같다) · 보장 6 관련: `_src_run_done` 은 술어는 같지만 od 를 요약 기록에서 받는다 (`_src_done` 은 요청 칸에서 받는다).
- 고침 제안: 새 런 기록마다 이 시도 groups/<이름> 의 시작 · 끝 결합 (`group_pair`) 과 outdir 폴더가 있는지 요구한다. ⓓ 의 다시 대조는 rerun 이름의 출력 폴더 꼴 전부 (`stop_trace` 와 같은 규칙) 로 한다. rerun 은 디스크상 첫 미완료 런과 같아야 한다.

## P2-3 — 보장 5 깨짐: 쓰기와 다시 셈이 원천을 서로 다른 곳에서 찾는다
- 결함 한 줄: 쓰기는 원천을 같은 바탕에서만 찾고, 다시 셈 (판정 · 합치기) 은 찾은 폴더에서 찾는다. recover 전에 원천을 다른 바탕으로 옮긴 정직 시도는 결과 줄이 False [원천] 로 영구히 남는다. 판정 때는 True 로 다시 세어져 ATTEMPT_LEDGER_MISMATCH 가 나고, 그 대상의 판정이 막힌다.
- 탐침: probes/p3_moved_source.py → out/p3_moved_source.json
- 입력: 정직 "대조 같음 뒤 멈춤" attempt_2 를 실제 git 원장에 둔다 (attempt.json 시작 커밋 = 항목 커밋). recover 전에 attempt_1 을 다른 바탕 B2 로 옮긴 뒤 실제 recover CLI 를 돌리고, `target_ledger_problem(found = B + B2)` 를 부른다.
- 기대: 정직 자료이므로 불일치가 없어야 한다.
- 실제: recover 는 rc 0 · 결과 줄 False · 커밋 글 [원천] · `target_ledger_problem` 은 Stop ATTEMPT_LEDGER_MISMATCH ("resume_ok False ≠ 다시 센 값 True") · 원천을 다시 옮겨 놓아도 줄이 False 로 남는다 · 대조군 (안 옮김) 은 ok · effective 2.
- 자리: :4522 (found None = 같은 바탕) · :4899 (`attempt_result`, found 없음) · :5005 · :5224 (다시 셈은 found 사용).
- 고침 제안: 원천을 못 찾으면 결과 줄을 쓰지 않는다 (미확인으로 두고 recover 를 다시). 아니면 결과 줄에 원천 위치 · sha (또는 [원천] 사유) 를 적어 다시 셈이 같은 근거로 재현하게 한다.

## P3-1 — ⓐ 의 `!=` 비교가 bool · float 를 통과시킨다
- 내용: `attempt_entry_diff` 가 `!=` 로 비교해서 resume_of 의 true · 1.0 이 정수 1 과 같다고 본다. 요약 없는 길에서만 문제가 되고, 값 뜻이 같아 해는 없다. `found_attempts_problem` 도 같다.
- 탐침: probes/p7_orphan_types.py
- 입력 · 기대 ↔ 실제: 요약을 지운 정직 재실행 시도에 attempt.json resume_of = true / 1.0 을 넣었다. 기대는 [ⓐ] 거부인데 실제는 세 자리 통과이고 found_attempts_problem 도 None 이다. 대조로 null 은 [ⓐ] 로 거부된다. 요약이 있는 길에서는 V08 이 `resume_rerun_problem` 에서 거부된다.
- 자리: :5095
- 고침 제안: `type(a[f]) is type(e[f]) and a[f] == e[f]` 로 비교한다.

## P3-2 — 손으로 고친 원장 결과 줄 + 꼴 틀린 요약에서 traceback (실패 꼴 회귀)
- 탐침: probes/p15_order_crash.py · 바탕 대조 probes/p15b_order_crash_base.py
- 입력: 결과 줄 True 의 folder_sha256 을, 요약 runs=5 (또는 stop="x") 로 바꾼 폴더의 sha 로 고쳤다.
- 기대: Stop.
- 실제: 고친 판에서는 `attempt_order_problem` · `resume_chain_problem` 둘 다 TypeError: 'int' object is not iterable / AttributeError: 'str' object has no attribute 'get' · 바탕에서는 차례 None · 사슬 ATTEMPT_LEDGER_MISMATCH 로 깔끔하게 멈췄다 · 그래서 지금은 `--add` 가 traceback 으로 끝나고, 풀기 전 대조는 시작 기록을 커밋한 뒤 traceback 이 난다 · recover · 판정은 `summary_shape_problem` 이 먼저 Stop 하므로 영향이 없다 (p14).
- 자리: :4663–4675 · :3811–3815 (공통 검증이 다시 셈의 try 앞 · 밖에 있다) · :4554 · :4599
- 고침 제안: 공통 검증 앞에 `summary_shape_problem` 을 두거나, 그 부름을 다시 셈의 try 안으로 옮긴다.

## P3-3 — 시험 빈틈 (변이 생존)
- 탐침: probes/mutate15.py (out/mutation15.json) · 가르는 입력 probes/p12_distinguish.py (out/p12_distinguish.log)
- 가르는 입력이 있는데 생존한 변이 (지금 코드 = 거부 · 변이 = 받음): entry_no_machine ← attempt.json machine 바꿈 · c_bytes · c_launch_only · c_end_only ← 복사 런 end 만 / launch 만 다름 · c_payload ← 복사 런 payload 를 바꿈 · loc_digest ← 원천 결과 줄 뒤에 원천에 파일 하나를 더함
- R1/R2 가드 짝이 서로를 대신한다: c_copy_srcdone ↔ c_bytes, c_first_new_done ↔ c_new_launch_same. 둘 중 하나만 지운 변이는 모두 생존한다.
- 보장 5 의 호출 자리 셋에서 st · found 를 빼도 생존한다 (tlp_ · lic_ · chain_recount_nost).
- close_old 는 구조 행 RR4E 만 잡는다.
- 나머지 생존 (추정: 다른 가드나 풀기 전 대조가 먼저 막음): a_missing_ok · a_noentry_ok · b_newattempt_R_ok · b_nondict_ok · loc_count_ge1 · loc_symlink · loc_attempt · c_after_new · c_cf_eq · c_cf_type · c_new_launch_missing_ok · srd_no_dir · d_name · chainprov_nodigest · chainprov_nostart_skip
- 고침 제안: 위 가르는 입력을 행으로 넣는다 (R1/R2 짝은 가드 하나씩 가르는 행).

## 지켜진 것
- **판정문 반례:** 9 꼴 (N1–N4 · N3a · Z1–Z4) 이 세 자리 모두 거부 · 표지가 맞다. 바탕 사슬에서는 9 행 모두 accepted 였다. 즉 시험이 옳은 이유로 실패한다.
- **내 변형 반례 25:** 거부 18 (R1 (copied_from true · det assumed) · R2 (순서 바꿈) · 새 런에 copied_from 추가 · resume_of true · machine · from '1' / 1.0 · 3 시도 copied_from 1 · end 만 다름 · payload 다름 · 원천 링크 (P6) · attempt-null · attempt.json 만 null · 요약 없는 길의 resume_of null · Codex R1 · R2 · rebind 원형) · 받음 7 (해 있음 4: P2-1 (a) · (b) · P2-2 (P8 · P9) / 해 없음 3: 중복 복사 기록 V07 (바탕이 이미 자격) · resume_of true · 1.0)
- **정직 흐름 10 꼴 (거짓 거부 없음):** 4 시도 · 원천이 L02 를 시작하지 않음 · 3 런 사슬 · 3 시도 (대조 뒤) · 재실행 런 자체 멈춤 사슬 · 원천 런 폴더 없음 · 원천 시간 초과 · 사슬 가운데 결과 전 재실행 · 정직 signal_after · P2-3 대조군. 거짓 거부는 P2-3 하나다.
- **예외 (p14):** 큰 정수 copied_from · from −1 · 이름 없는 복사 기록 · resume 목록 → 사유로 거부되었다.
- **보장 6:** `ResumeRunner._src_done` · `run` · `_copy` 소스가 바탕과 같다 (AST 조각 sha256 앞 16 = f0730e50f1f630f2 · …).
- **RR4-01:** 원로그 셈: mutation_PA13.json 46 (잡힘 43 · 생존 M14 · M18 · M46) + _extra 5 (잡힘 M51 · M52 · 생존 M47 · M54 · M56) = 51 · 잡힘 45 · 생존 6. M46 만 동치로 보면 45/50 · 비동치 생존 5 로, 정정 문구와 같다 · preattack14 SHA256SUMS 25 줄 모두 OK · 원로그 · mutate.py 는 diff 에 없다 · M56 (mutate.py:60 과 같은 글자) 은 RR4C 가 잡는다 (18/19 · FAILED RR4C).

## 변이
- 내가 고른 46 개를 `--only RR3,PA13,PA14,RR4` 로 돌렸다 (각 10.3–14.1 s).
- 잡힘 19: a_drop · entry_no_resume_of · b_drop · b_eq_only_type · src_failopen · c_drop · srd_no_rc · d_drop · d_cmp · new_attempt_no_early_return · fields_keep_true · recount_ignore_st · write_old · recover_old · close_old · order_no_prov · chainprov_noprov · chain_noprov · M56_exists
- 생존 27: 목록과 처분은 P3-3 에 적었다. 전체 사슬은 변이마다 돌리지 않았다 (지시: 전체는 1 회).

## 돌린 시험
1. 고친 판 사본 `python3 scripts/test_rint_r_chain.py --only RR3,PA13,PA14,RR4` → 19/19 PASS (9.6 s)
2. 고친 판 사본 `python3 scripts/test_rint_r_chain.py` (1 회) → 499/500 PASS (316.6 s) · FAILED Y13 — 환경 탓: archive 사본은 git 저장소가 아니라 `git check-ignore` 가 rc 128 을 낸다 · 바탕 사본도 `--only Y13` 이 0/1 (1.9 s).
3. 고친 시험 × 바탕 사슬 (e48e5fa04 의 rint_r_chain.py) `--only RR3,PA13,PA14,RR4` → 15/19 (11.2 s) · FAILED RR4A · RR4B · RR4D · RR4E (RR4A 는 음성 9 행이 accepted 로 실패 · RR4B 는 behaviour_ok True 이고 실패 이유는 다시 셈 API 가 없어서 (api_absent)).
4. 탐침 p1–p15 (합성 · scratch git) · 변이 46 × 위 부분집합 · 리포는 손대지 않았다 (HEAD 69d714d09 · 작업 트리 깨끗) · 검토는 e94f09905 · e48e5fa04 archive 사본에서만.
