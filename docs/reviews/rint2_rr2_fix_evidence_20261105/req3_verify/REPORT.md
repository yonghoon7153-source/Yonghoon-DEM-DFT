# 회차 ③ 요청서 (`e540c73fe` : `docs/reviews/codex_rint2_rr_round3_request_20261108.md`) 사전 공격 ① 대조 — 2026-11-08

> 반입 메모 (리뷰 핀 커밋 · 11-08): 원본 = 서브 세션 스크래치 req3_verify/REPORT.md (리포 밖 · sha256 2c8cbd825767264c2f1ce29596e8f6401f5f0956828a26f0d16472908f0890cc) · 반입 때 백틱 안의 약칭 경로 (E/ · N/ · X/ · P10/ · 폴더 생략) 17 종을 전체 경로로 전개했다 (경로 검사기 규약 · 글 · 수 · 판정 그대로 · 전개표 = 이 메모 아래) · 대상 = 요청서 초안 커밋 (작업 트리 가지 · push 안 됨 · 리뷰 핀 커밋에 cherry-pick -x) · 다름 1 · 과장 5 는 리뷰 핀 커밋의 요청서에서 좁혔다 (요청서 §5 첫 불릿 · §5-1).
>
> 전개표: E/REPORT.md → `docs/reviews/rint2_rr2_fix_evidence_20261105/REPORT.md` · E/logs/code_sha256.txt → `docs/reviews/rint2_rr2_fix_evidence_20261105/logs/code_sha256.txt` · E/rerun_codex_probe.py → `docs/reviews/rint2_rr2_fix_evidence_20261105/rerun_codex_probe.py` · N/REPORT.md → `docs/reviews/rint2_rr2_fix_evidence_20261105/pc10_n_fix/REPORT.md` · N/logs/count_bad_before.json → `docs/reviews/rint2_rr2_fix_evidence_20261105/pc10_n_fix/logs/count_bad_before.json` · P10/REPORT.md → `docs/reviews/rint2_rr2_fix_evidence_20261105/preattack10_fix/REPORT.md` · P10/codex_probe_rerun/results.json → `docs/reviews/rint2_rr2_fix_evidence_20261105/preattack10_fix/codex_probe_rerun/results.json` · P10/logs/code_sha256.txt → `docs/reviews/rint2_rr2_fix_evidence_20261105/preattack10_fix/logs/code_sha256.txt` · X/codex_probe_rerun/results.json → `docs/reviews/rint2_rr2_fix_evidence_20261105/pc10_n_fix/ext/codex_probe_rerun/results.json` · X/logs/code_sha256.txt → `docs/reviews/rint2_rr2_fix_evidence_20261105/pc10_n_fix/ext/logs/code_sha256.txt` · X/logs/count_bad_before.json → `docs/reviews/rint2_rr2_fix_evidence_20261105/pc10_n_fix/ext/logs/count_bad_before.json` · codex_probe_rerun/results.json → `docs/reviews/rint2_rr2_fix_evidence_20261105/codex_probe_rerun/results.json` · codex_rint2_rr_round2_evidence_20261105/runtime_review/probe_runtime.py → `docs/reviews/codex_rint2_rr_round2_evidence_20261105/runtime_review/probe_runtime.py` · pc10_n_fix/REPORT.md → `docs/reviews/rint2_rr2_fix_evidence_20261105/pc10_n_fix/REPORT.md` · preattack10_fix/REPORT.md → `docs/reviews/rint2_rr2_fix_evidence_20261105/preattack10_fix/REPORT.md` · preattack12/REPORT.md → `docs/reviews/rint2_rr2_fix_evidence_20261105/preattack12/REPORT.md` · rint2_s0_mem_fix_20261106/REPORT.md → `docs/reviews/rint2_s0_mem_fix_20261106/REPORT.md`

- 방법 = 읽기 전용 (`git show · log · diff · ls-tree · cat-file · merge-base · rev-parse` · 파일은 `git show e540c73fe:<경로>`) · 스크래치 `scratchpad/req3_verify/` · 체크아웃 · 실행 · 편집 없음.
- SHA256SUMS 검산 = 각 줄의 해시 ↔ `git cat-file blob` 의 sha256 (sha256sum -c 와 같은 뜻) · 원장 합계 = JSON 직접 집계 · 로그 수 = 그 파일의 실제 줄.
- 집계: **같음 81 · 다름 1 · 미확인 4** (표 86 행 · 반복 행은 묶음).

## 1. 주장 대조표

| # | 주장 (요청서 자리) | 확인한 것 (명령 · 파일) | 판정 |
|---|---|---|---|
| 1 | 머리: 회차 ② = HOLD · 새 P1 0 · P2 1 · P3 2 · 리뷰 핀 `6917c3c9f` | `codex_review_rint2_rr_round2_20261105.md` 3·5·7·260 행 ("판정 … HOLD" · "P1 0건 · P2 1건 · P3 2건" · "대상 핀 6917c3c9fa39…") | 같음 |
| 2 | 머리: 비교 기준 `6917c3c9f` = 회차 ② 리뷰 핀 · stoic | 같은 파일 7 행 "대상 핀 … claude/stoic-knuth-NObVQ" · README_import 30 행 verified_sha `6917c3c9f` | 같음 |
| 3 | §5-1: 백틱 SHA 12 개 = 12/12 조상 · 유일 접두 | `grep -oE '`[0-9a-f]{9}`'` → 12 종 · `git cat-file -t` 12 commit · `merge-base --is-ancestor` 12/12 · `rev-parse` 12/12 유일 · `log --first-parent 6917c3c9f..e540c73fe` = 정확히 그 12 커밋 | 같음 |
| 4 | §5-1: stoic 동결 `6a81f0c55` = `rev-parse origin/claude/stoic-knuth-NObVQ` | `6a81f0c55d1583fba63ffe665874525cc82d36ff` | 같음 |
| 5 | 머리: 리뷰 핀 = 이 요청서 커밋 · 작업 가지 B `claude/sdcp-dem-manuscript-si-pqwtv8` · push | 로컬: `e540c73fe` 는 `worktree-agent-a1677a57e4e2a38f0` 에만 · `origin/claude/sdcp-dem-manuscript-si-pqwtv8` = `6a81f0c55` (이 리포 시점) | 미확인 (push · B 가지 소속 = 로컬 리포로 확인 불가 · 지금 원격 B ≠ 요청서 커밋) |
| 6 | 머리 · §0 ①: RR2-01·02·03 · PC6-05 → `f5b00a838` | 원장 e540: 넷 다 claimed_fixed · `claimed_fixed_sha` = `f5b00a838` (9 자리) | 같음 |
| 7 | §0 ②: PC9-01 (P2) · 02–07 (P3) claimed_fixed `f5b00a838` · PC9-08 wontfix | 원장: PC9-01 P2 · 02–07 P3 · sha `f5b00a838` · PC9-08 wontfix P3 | 같음 |
| 8 | §0 ③: PC10-01 (P2) · 02–07 (P3) → `766e1e80c` | 원장: 7 개 claimed_fixed · sha `766e1e80cf0a…74de` (40 자리) | 같음 |
| 9 | §0 ④ · §5-1 끝: PC10-08·09 (P2) · 10 (P3) · PC11-01·02 (P2) · 03·04 (P3) claimed_fixed = `6a81f0c55` 전체 SHA | 원장 e540: 7 개 모두 `claimed_fixed_sha` = `6a81f0c55d1583fba63ffe665874525cc82d36ff` · 심각도 그대로 | 같음 |
| 10 | §0 · §5-1: PC11-05–08 open (P3) · PC12-01–03 (P2) · 04·05 (P3) open · SELF-158 open | 원장 e540: 전부 open · 심각도 같음 · SELF-158 P3 open (`opened_in` = preattack12/REPORT.md) | 같음 |
| 11 | §0 ⑤ · §2: SELF-155 (P2) → `f47bde0f6` · 원장 전환은 `6a81f0c55` 에서 | 원장 sha `f47bde0f631f9…8333` · f47bde0f6→6a81f0c55 원장 diff = open→claimed_fixed 1 (SELF-155) | 같음 |
| 12 | §0 ①: PC6-13 부분 · 남은 분기 = RR2-01 · 수정 계획 Q5 (가) | `rint2_rr2_fix_plan_20261105.md` 37–39 행 ("PC6-13 의 남은 분기 = RR2-01") · 원장 PC6-13 claimed_fixed `4499f3ffd` 그대로 | 같음 |
| 13 | 머리: 1저자 11-05 "권고대로" · Q1–Q7 = (가) | 수정 계획 4 행 "✅ 1저자 11-05 *권고대로* — Q1–Q7 = 모두 (가)" · 각 Q 권고 = (가) | 같음 |
| 14 | 머리: 1저자 11-06 "권고대로" (사전 공격 10 · N1·N2·N4 · 규칙) | `docs/reviews/rint2_rr2_fix_evidence_20261105/preattack10_fix/REPORT.md` 1 행 · `docs/reviews/rint2_rr2_fix_evidence_20261105/pc10_n_fix/REPORT.md` 1 행 · 원장 PC10-10 note | 같음 |
| 15 | 머리: 1저자 11-08 "권고대로" · 인계 §5-1 | `docs/handoff_to_subsession_20261108.md` "5. 할 일" 1. "(1저자 11-08 "권고대로" · 발송 = 1저자)" (§5-1 = 5 장 1 항 · 제목 꼴 아님) | 같음 |
| 16 | 머리: 판정문 §8 Q8 (S0) · §8 끝 문단 = 좁은 재검토 | 판정문 §8 끝 "이 둘과 RR2-02/03을 고친 뒤, 위 봉인 전 확인 범위를 특정하여 좁게 재검토하면 된다" | 같음 |
| 17 | §0 ③: Q5 현장 자격 — PC5-03·07·08·PC6-01·PC8-05 (판정문 §9 · 0 건) | 판정문 §9 = 현장 자격 (ID 나열 없음 · ID 출처 = 수정 계획 Q5 37 행) · 다섯 = 원장 claimed_fixed 그대로 (닫힘 아님 = 일관) · "0 건" = 결과 부재 주장 | 미확인 (부재는 리포로 증명 못 함 · 모순 없음) |
| 18 | §0 ⑤: 회차 ② §8 Q8 칸 = S0 REPORT §11 · 예외 둘 · CP-ORD 자리 옮김 · S0 계획 해시 바뀜 | `docs/reviews/rint2_s0_mem_fix_20261106/REPORT.md` §11 제목 "Codex §8 Q8 확인 칸" · §4 예외 둘 · 45 행 CP-ORD · 93·101 행 계획 해시 | 같음 |
| 19 | §1: 표의 모든 경로 존재 (파일 · 폴더 43 경로) | `git ls-tree e540c73fe -- <경로>` 43/43 (MISSING 0) | 같음 |
| 20 | §1: 회차 ② 증거 84 (우리 트리 재현 `_repro_ours_20261105/` 포함) | `ls-tree -r` blob 84 (그 중 `_repro_ours_20261105/` 15) | 같음 |
| 21 | §1: 고침 증거 307 | `ls-tree -r docs/reviews/rint2_rr2_fix_evidence_20261105` blob 307 | 같음 |
| 22 | §1: 바깥 SHA256SUMS 287 줄 = preattack12/ 뺌 · SHA256SUMS 이름 뺌 | 287 줄 (빈 줄 0) · `preattack12/` 항목 0 · `SHA256SUMS` 이름 0 · 해시 ↔ blob 287/287 일치 · 287 + preattack12 17 + SHA256SUMS 3 = 307 | 같음 |
| 23 | §1: 안 SHA256SUMS = preattack10_fix/ 68 · pc10_n_fix/ 143 (ext/ 포함) · preattack12/ 16 | 68 · 143 (ext/ 79 포함) · 16 줄 · 해시 ↔ blob 68/68 · 143/143 · 16/16 · 폴더 blob 69 · 144 · 17 (= +1 SHA256SUMS) | 같음 |
| 24 | §1: S0 메모리 156 (SHA256SUMS 155) · 근거 측정 3 (SHA256SUMS 2) | blob 156 · 3 · SHA256SUMS 155 · 2 줄 · 해시 ↔ blob 155/155 · 2/2 | 같음 |
| 25 | §1 · §5-1: 바뀐 Rint ② 코드 · 시험 6 | `git diff --stat 6917c3c9f e540c73fe -- scripts/` 중 Rint 6 파일 (ca_s0_census 22 · carbon_junction 275 · rint_r_chain 665 · test_ca_s0_census 239 · test_carbon_junction 640 · test_rint_r_chain 2563) | 같음 |
| 26 | §1 · §5-1: 실행 의존 22 = `6917c3c9f` 와 diff 0 (CODE_FILES 나머지 16 · 시험 import 다섯 · e2e) | 22 경로 전부 존재 · `git diff --stat 6917c3c9f e540c73fe -- <22>` 빈 출력 | 같음 (단 "시험 import 다섯" 은 `test_rint_r_chain.py` 의 직접 import 아님 — test_ca_ext_b6 ← test_carbon_junction.py · test_ca_ext_runner ← test_rint_r_chain_e2e.py · check_method_discipline ← test_ca_ext_b6/runner · sdcp_gain_verdict ← check_method_discipline · cam_kinetics ← step4_dyn.py = 간접) |
| 27 | §1 · §5-1: CODE_FILES `scripts/rint_r_chain.py` 302 줄 · 19 | `grep -n CODE_FILES` → 302 행 · 튜플 항목 19 (302–306 행) · 19 − 3 (바뀐 셋) = 16 | 같음 |
| 28 | §1: 고친 문서 · 설계 · 등록 · 명령 9 | 9 경로 존재 · 그 중 7 바뀜 (`q9_time_budget.json` · `rint2_kgy_commands_20261020.md` = 무변경 · 표 이름이 "고친 문서 · 설계 · 등록 · 명령" 이라 모순 아님) | 같음 |
| 29 | §1: 합 = repo/ 591 파일 | 1 + (1+84+1) + 307 + (156+3) + 1 + 6 + 22 + 9 = 591 (산술 · 각 항 실측과 같음) | 같음 |
| 30 | §1: PIN.txt (핀 40 자리 + 가지) · ZIP 이름 · git archive · blob 대조 · sha256 대조 | ZIP = 리포 밖 · 아직 만들지 않음 | 미확인 (리포로 확인 불가) |
| 31 | §2 `a69bf7d53` = 회차 ② 판정 반입 · 원장 verified 35 · 새 open 3 · 수정 계획 초안 | stat: 84 A `codex_rint2_rr_round2_evidence_20261105/` · 판정문 A · 수정 계획 A · 원장 M · 원장 diff 6917c3c9f→a69bf7d53: claimed_fixed→verified **35** · 새 3 (RR2-01·02·03) · README_import 30·33·34 행 | 같음 |
| 32 | §2 `933863e47` = 수정 계획 비준 기록 · 같은 커밋 = 50kg | stat: `rint2_rr2_fix_plan_20261105.md` M · `docs/data/kg50_d07_end_20261105/` · 원장 상태 변화 0 | 같음 |
| 33 | §2 `f5b00a838` = A1 RR2-01·PC9-02·05 · A1b PC9-01 · A2 PC6-05·PC9-04 · A2b PC9-03 · A3 RR2-02·PC9-06 · A4 RR2-03·PC9-07 · A5 Q7 · 여덟 커밋 = 한 커밋 | 커밋 글 1 행 "여덟 커밋 = 한 커밋" · 원장 PC9-0x note (PA-01→A1b · PA-02·05→A1 · PA-03→A2b · PA-04→A2 · PA-06→A3 · PA-07→A4) · stat = scripts 2 + 문서 8 + 증거 62 · dev_probe_ledger +1 줄 (Q7) | 같음 |
| 34 | §2 `766e1e80c` = PB-01–07 = PC10-01–07 · 원장 (RR2·PC6-05·PC9 claimed_fixed · PC10 등재) · 같은 커밋 = FAM · 후막 | 원장 diff f5b00a838→766e1e80c: 새 18 (PC9-01–08 · PC10-01–10) · open→claimed_fixed 4 (PC6-05 · RR2-01·02·03) · wontfix 10→11 · stat: `codex_review_fam_s127_raw_20261106.md` · `th_comsol_handover_20261106/` · 84 A 증거 | 같음 |
| 35 | §2 `342eff6e1` = 원장 PC10-01–07 claimed_fixed · 같은 커밋 = /emod · LHS 대기 지문 | 원장 diff: open→claimed_fixed 7 (PC10-01–07) · 새 SELF-157 · stat: webapp emod · lhs 등록 둘 | 같음 (누락: 같은 커밋이 `rint2_s0_mem_probe_20261106/` 3 파일 · `SELF-157` 도 넣음 — §2 에 없음) |
| 36 | §2 `f47bde0f6` = S0 메모리 SELF-155 (carbon_junction · ca_s0_census + 시험) | stat: 156 A `rint2_s0_mem_fix_20261106/` · scripts 4 (carbon_junction · ca_s0_census · 시험 둘) · 원장 M (상태 변화 0 · SELF-155 note) | 같음 |
| 37 | §2 `6a81f0c55` = N1·N2·N4 (PC10-08–10) + 사전 공격 11 확장 · 원장 SELF-155 claimed_fixed | stat: 144 A `pc10_n_fix/` · scripts 2 · 원장 diff SELF-155 open→claimed_fixed · 커밋 글 ★ 확장 P2-B · P3-5 · P3-6 | 같음 |
| 38 | §2 `2b3c42c6c` = 인계 기록 (문서만) | stat: CLAUDE.md · progress · handoff A = 3 파일 · 코드 0 | 같음 |
| 39 | §2 (이 커밋) = 요청서 · preattack12/ 반입 · 원장 | `e540c73fe` stat: 17 A `preattack12/` · 요청서 A · findings M · progress M = 20 파일 | 같음 |
| 40 | §2: Rint ② 밖 = `504d84e52` · `cc1a96796` · `18bb6a2e4` (Ⓐ · 50kg · FAM · check_all 나누기) | stat: 504d = `p1_g2c_sandbox_20261104/` · cc1a = `docs/50kg/` · 18bb = `fam_s127_gabia_20261106/` + `scripts/check_all.sh` M + `scripts/test_check_all_split.sh` A | 같음 |
| 41 | §3 RR2-01 A1: RC01–RC05 0/5 → 5/5 | `E/logs/before_A1_RC.log` 끝 "test_rint_r_chain: 0/5 PASS … FAILED: ['RC01','RC02','RC03','RC04','RC05']" · `after_A1_RC.log` "5/5 PASS (7.9 s)" · 시험 이름 5 개 = `scripts/test_rint_r_chain.py` 13231–13346 | 같음 |
| 42 | §3 PC9-01 A1b: PE03u·CE01·CE02 0/3 → 14/14 | `before_A1b_CE.log` "0/3 PASS FAILED ['PE03u','CE01','CE02']" · `after_A1b_targeted.log` "14/14 PASS" · 이름 3 = 시험 파일 12016 · 13388 · 13412 | 같음 |
| 43 | §3 PC6-05 A2: LG01–LG03 0/3 → 34/34 · 3/3 | `before_A2_LG.log` "0/3 PASS FAILED ['LG01','LG02','LG03']" · `after_A2_targeted.log` "34/34 PASS" · `after_A2_LG_rows2.log` "3/3 PASS" · 이름 = 13581 · 13709 · 13840 | 같음 |
| 44 | §3 PC9-03 A2b: SU01·SU02 0/2 → 12/12 | `before_A2b_SU.log` "0/2 PASS FAILED ['SU01','SU02']" · `after_A2b_SU.log` "12/12 PASS" · 이름 = 13885 · 13957 | 같음 |
| 45 | §3 RR2-02 A3: Q9 설계 69 줄 취소선 + 현행 계약 · 회차 ①·② 요청서 표지 · `q9_time_budget.py` 낱말만 · before.out = after.out | `git diff 6917c3c9f e540c73fe -- q9_predict_units_design.md` = **69 행 한 줄** (취소선 두 곳 + "→ 11-0…" 정정 · 파일 전체 `~~` 줄 17 → 18) · 회차 ①·② 요청서 diff = 표지 줄만 · `q9_time_budget.py` diff 3 줄 문구 · `q9_time_budget_before.out` blob = `after.out` blob | 같음 (⚠ "69 줄" = 69 번째 줄 1 줄 — "69 개 줄" 로 읽힐 수 있음 · §3 과장 목록) |
| 46 | §3 RR2-03 A4: 등록 R ⑫ = 코드 한정어 + Δ/λ 0.02–0.63 · q 0.4–19 · 설계 v1 · RINT2-L01 표지 · verify ok · K01·PC18·PC20·EP06 4/4 | 등록 R 283 행 "Δ/λ 0.02 – 0.63 · q 0.4 – 19" (붙임표 양옆 공백 = 요청서 표기 차이만) · `verify_rr2_03_quote.out` `"ok": true` (quote_is_code_substring · ranges_in_fix [true,true]) · 설계 v1 diff 1 줄 교체 · `after_A4_doc_tests.log` "4/4 PASS" (EP06 K01 PC18 PC20) · 이름 4 = 시험 파일 6380 · 9596 · 10469 · 10488 | 같음 |
| 47 | §3 `f5b00a838` 회귀: 시험한 판 = 커밋 blob · 사슬 463/463 · 끝-끝 51 PASS 0 FAIL · kgy 3.8.20 11 묶음 · 변이 40/40 · 탐침 310/311 (다른 1 = known_PC6_05) | `docs/reviews/rint2_rr2_fix_evidence_20261105/logs/code_sha256.txt` 끝 판 `d3775ca8…` · `583b7c3d…` = `git show f5b00a838:scripts/{rint_r_chain,test_rint_r_chain}.py \| sha256sum` · `final_chain_full_py311.log` "463/463 PASS (434.9 s)" · `final_e2e_py311.log` "51 PASS · 0 FAIL" · `check_kgy_py38.out` "Python 3.8.20 · numpy 1.24.4 · scipy 1.10.1" · "11 묶음 통과" · `mutation_rr2fix.out` "변이 40 · 잡힘 40 · 생존 0" · `docs/reviews/rint2_rr2_fix_evidence_20261105/codex_probe_rerun/results.json` passed 310 total 311 · not-ok = `known_PC6_05_summary_missing_log_resume` 만 · source rint_r_chain `d3775ca8…` | 같음 |
| 48 | §3 PC10-01: RN01·RN02 + 기대 바뀐 다섯 3/10 → 10/10 | `P10/logs/before_PB01.log` "3/10 PASS FAILED ['PD13','PD13o','PE03u','RC04','LG01','RN01','RN02']" (= 2 + 5) · `after_PB01.log` "10/10 PASS" · RN01 14075 · RN02 14125 | 같음 |
| 49 | §3 PC10-02·03·04·06: SU03·SU04 0/2 → 2/2 · FF01 0/1 → 1/1 · RC01 0/1 → 1/1 · 3/4 → 4/4 | PB02 "0/2 FAILED ['SU03','SU04']" → "2/2" · PB03 "0/1 FAILED ['FF01']" → "1/1" · PB04 "0/1 FAILED ['RC01']" → "1/1" · PB06 "3/4 FAILED ['LG01']" → "4/4" · 이름 = 14206 · 14269 · 14395 | 같음 |
| 50 | §3 `766e1e80c` 회귀: 커밋 blob · 468/468 · 끝-끝 51/0 · kgy 11 묶음 · 변이 28/28 · 탐침 310/311 | `docs/reviews/rint2_rr2_fix_evidence_20261105/preattack10_fix/logs/code_sha256.txt` 끝 `da4c2ef6…` · `f797fe7e…` · `41762029…` = `766e1e80c` blob 셋 · `final_chain_full_py311.log` "468/468 PASS (396.1 s)" · e2e "51 PASS · 0 FAIL" · check_kgy "3.8.20 … 11 묶음 통과" · `mutation_pa10fix.out` "변이 28 · 잡힘 28 · 생존 0" · `docs/reviews/rint2_rr2_fix_evidence_20261105/preattack10_fix/codex_probe_rerun/results.json` 310/311 (not-ok known_PC6_05 · src `da4c2ef6…`) | 같음 |
| 51 | §3 PC10-08·09: CT01 91/150 → 0 · CT02 12/21 → 0 · CT04 4 → 0 · 기대 고친 기존 시험 합 73 | `docs/reviews/rint2_rr2_fix_evidence_20261105/pc10_n_fix/logs/count_bad_before.json` CT01 n 150 n_bad 91 · CT02 21/12 · CT04 n_bad 4 → `count_bad_after.json` 전부 0 pass true · `docs/reviews/rint2_rr2_fix_evidence_20261105/pc10_n_fix/REPORT.md` 43 행 RN01 42 + PD13 10 + PD02 7 + PD02c 2 + PE03u 4 + RC02 6 + LG01 2 = 73 · CT01 14479 · CT02 14562 · CT04 14691 | 같음 |
| 52 | §3 PC10-10: CT03 6/10 → 0 | 같은 두 JSON CT03 n 10 n_bad 6 → 0 · CT03 14631 | 같음 |
| 53 | §3 PC11-01: CT05 28/31 → 0 | `docs/reviews/rint2_rr2_fix_evidence_20261105/pc10_n_fix/ext/logs/count_bad_before.json` CT05 n 31 n_bad 28 → after 0 · CT05 14875 | 같음 |
| 54 | §3 PC11-02: CT06 35/61 → 0 · 중간 판 outdir 접두만 7/61 · GU 기록 rc 꼴 = 끝 기록 확인 True 고정물만 | X before CT06 61/35 → after 0 · `count_bad_prefix_only.json` CT06 n_bad 7 · 시험 15078 `CHAIN_OK1 = {'by':'chain','confirmed': True,…}` · 15085 `S2_forged_GU_rc0` 가 CHAIN_OK1 사용 · CT06 14933 | 같음 |
| 55 | §3 PC11-03·04: CT07 8/9 → 0 · CT08 실패 → 통과 | X before CT07 n 9 n_bad 8 · CT08 pass false → after CT07 0 · CT08 pass true · CT07 15171 · CT08 15227 | 같음 |
| 56 | §3 `6a81f0c55` 회귀: 커밋 blob · 476/476 · 끝-끝 51/0 · kgy 3.8.20 11 묶음 · 변이 첫 판 26 중 25 (K1 동등) · 새 가드 36/36 · 사전 공격 11 14/14 · 탐침 303/311 | `docs/reviews/rint2_rr2_fix_evidence_20261105/pc10_n_fix/ext/logs/code_sha256.txt` `0d72d11b…` · `4982c064…` = `6a81f0c55` blob · `final_chain_full_py311.log` "476/476 PASS (515.4 s)" · e2e "51 PASS · 0 FAIL" · `check_kgy_py38.out` "3.8.20 · 1.24.4 · 1.10.1" · "11 묶음 통과" · `N/logs/mutation_pc10_K1c.out` "변이 26 · 잡힘 25 · 생존 1" (K1) · `mutation_pc10ext.out` total 36 killed 36 · `mutation_pa11_rerun.out` KILLED 14 · 생존 0 · `docs/reviews/rint2_rr2_fix_evidence_20261105/pc10_n_fix/ext/codex_probe_rerun/results.json` 303/311 | 같음 (참고: ext 재실행 `mutation_pc10_rerun.out` = 26 중 24 잡힘 · 생존 1 · 건너뜀 1 — 요청서는 "첫 판" 만 인용) |
| 57 | §3 SELF-155: carbon_junction 547/547 · S0 186/0 · 새 시험 + 옛 구현 532/547 · 180/6 · 3.8 11 묶음 · 변이 7/7 · 끝-끝 킷 4 · npz 41 중 다른 것 0 · blob 넷 = 커밋 blob | `S0/logs/final_539844f8d/py311/carbon_junction.log` "547/547 PASS" · `ca_s0_census.log` "186 PASS · 0 FAIL" · `final_539844f8d_tests_on_old_impl/` "532/547 PASS" · "180 PASS · 6 FAIL" · `py38/check_kgy_py38.log` "11 묶음 통과" · `mutation_full.json` mutants 7 · 모두 rc≠0 한 묶음 이상 · restored true · `s0_e2e/s0_e2e_compare.log` 킷 4 (A · J · RV · L) "파일 6 같음 True · npz 다른 배열 0 / 41" · `tested_code_blobs.txt` sha256 넷 = `git show f47bde0f6:` 넷 | 같음 |
| 58 | §4: 한정 항목 (교차 대조 없음 · 같은 이름 둘 · 런 전 TIME_LIMIT 차례 · copied_from·seconds·machine · 디스크 signal_after · 칸 없음 받음 · 경합 꼴 · utc·cause·STOPS 소속 · 흔적 지운 폴더 · .nfs*) = REPORT_EXT §8 · N/REPORT §8 | `REPORT_EXT.md` §8 네 불릿 · `docs/reviews/rint2_rr2_fix_evidence_20261105/pc10_n_fix/REPORT.md` §8 아홉 불릿에 전부 있음 | 같음 |
| 59 | §4: 새 원장 PC11-05·06·07·08 = 그 네 한정 | 원장 제목: 05 같은 이름 둘 (S3) · 06 런 전 TIME_LIMIT 차례 · 07 copied_from·seconds·machine · 08 디스크 signal_after (S7) | 같음 |
| 60 | §4: 봉인 원천 런 (G01_<런>_a<i>) 중 신호 = runner_rc → PC9-08 wontfix (E/REPORT §5) | `docs/reviews/rint2_rr2_fix_evidence_20261105/REPORT.md` §5 "고치지 않음 (1저자 결정 = 한정만): 봉인 원천 런 … 신호 = runner_rc" · 원장 PC9-08 wontfix | 같음 |
| 61 | §4: 원인 None + rc 0 + 잘못된 주소·CUDA 로그 ↔ recover runner_rc · `_src_done` = rc 0 만 · 옛 결과 줄 = 다시 셈 거부 (따로 시험 안 함) = P10 §6 · N §8 | `docs/reviews/rint2_rr2_fix_evidence_20261105/preattack10_fix/REPORT.md` §6 "그대로 둔 다름 …" · `docs/reviews/rint2_rr2_fix_evidence_20261105/pc10_n_fix/REPORT.md` §8 "_src_done = rc 0 만" · "원장 옛 결과 줄 … 이번에 따로 시험 안 함" | 같음 |
| 62 | §4: 열림 그대로 PC6-03·06 · PC7-06·07 · RINT2-T01 · RINT2-L01 | 원장 e540 6 개 open | 같음 |
| 63 | §4: S0 실침대 peak RSS·시간 미측정 · 예외 ② 실침대 존재 미확인 · _cand_pairs 긴 꼬리 · 1,356 s 6.96 GB 원인 미확인 = S0 REPORT §4 · §10 | S0 REPORT 6 행 · §4 36 행 "실침대에 그런 꼴이 있는지 = 미확인" · §10 82–83 행 (_cand_pairs · "11-06 실측 1,356 s 에 표본 하나 6.96 GB") | 같음 |
| 64 | §4 · §5-1: `6a81f0c55` 회귀 수 = 반입 전 작업 트리 (바탕 766e1e80c · S0 고침 전) · 합친 판 게이트 기록 = 리포에 없음 | `REPORT_EXT.md` 39 행 "⚠ 이 수들은 main 반입 전 작업 트리 (바탕 766e1e80c) 에서 쟀다" · `6a81f0c55` + 게이트 언급 = progress · CLAUDE.md · handoff 에 없음 (제한 검색) | 같음 |
| 65 | §5-1: 폴더 수 · SHA256SUMS 수 · `sha256sum -c` 통과 | 행 20–24 (검산 671/671) | 같음 |
| 66 | §5-1: §3 의 수 = 로그 끝 줄 · count_bad JSON · results passed/total | 행 41–57 | 같음 |
| 67 | §5-1: 시험한 판 = 커밋 blob (넷) | E = f5b00a838 · P10 = 766e1e80c · X = 6a81f0c55 · S0 = f47bde0f6 (행 47 · 50 · 56 · 57) | 같음 |
| 68 | §5-1: Codex 탐침 "무변경" = probe_runtime.py sha256 ↔ PROBE_SHA | `docs/reviews/rint2_rr2_fix_evidence_20261105/rerun_codex_probe.py` 17 행 `PROBE_SHA = '12f3b4c9…c9ee'` · `docs/reviews/codex_rint2_rr_round2_evidence_20261105/runtime_review/probe_runtime.py` sha256 `12f3b4c9…c9ee` | 같음 |
| 69 | §5-1 · §5-2: PC12 줄 번호 4000 · 4021 · 4027–4033 · 4037 · 4044–4069 · 4303 · 4773 · 5625 · 줄 = 핀 (파일 = 6a81f0c55 와 같음) | `awk` on `e540c73fe:scripts/rint_r_chain.py`: 4000 ∈ `stop_record_problem` · 4021·4027–4033·4037 ∈ `stopped_record_problem` (4037 = `if code == 'GROUP_UNCONFIRMED'`) · 4044 `def chain_confirmed` … 4069 return · 4303 ∈ `rejected_form_problem` · 4773 `def record_outdir` · 5625 ∈ `read_summary_state` (`json.loads`) · blob e540 = 6a81 = 2b3c (`5b0abf8a…`) | 같음 |
| 70 | §5-1: 원장 997 → 1011 · open 336 → 343 · claimed_fixed 371 → 378 · verified 279 · wontfix 11 | `2b3c42c6c:findings.json` 997 {cf 371 · v 279 · open 336 · wf 11} → `e540c73fe` 1011 {cf 378 · v 279 · open 343 · wf 11} · 중복 id 0 | 같음 |
| 71 | §5-1: `check_review_findings.py` (앞·뒤) rc 0 | 검사기 실행 안 함 (읽기 전용 작업) · 합계는 행 70 으로 대신 확인 | 미확인 |
| 72 | §5-1 끝 줄: 이 커밋 원장 = PC10-08·09·10 claimed_fixed · 새 PC11-01–04 claimed_fixed · 05–08 open · PC12-01–05 · SELF-158 open · PC11-02 메모 범위 좁힘 · PC10-10 메모 정정 | 2b3c→e540 원장 diff: open→claimed_fixed 3 (PC10-08·09·10) · 새 14 · 다른 편집 0 · PC10-10 note "★ 11-08 정정 — 위 "권고" 글은 N1·N2 의 것을 옮겨 적은 것 · N4 의 권고 = result_recount …" · PC11-02 note "★ 11-08 범위 좁힘 (사전 공격 12 F2 = PC12-02)" | 같음 |
| 73 | §5-1: 이 대조로 고친 것 = §2 `f5b00a838` 행에 PC9-02·05 보강 · 진행 기록 줄 | §2 행에 "A1 RR2-01 · PC9-02 · 05" 있음 · `e540c73fe` stat progress M | 같음 |
| 74 | §5-2: 사전 공격 12 = P1 0 · P2 3 · P3 2 · 거짓 fail-closed 못 찾음 · 요약 꼴 무작위 30,000 Stop 아닌 예외 0 · 거부 기록 형·중복 칸·BOM·inf = Stop · SHA256SUMS 16 | `docs/reviews/rint2_rr2_fix_evidence_20261105/preattack12/REPORT.md` F1–F3 (P2) · F4·F5 (P3) · 47 행 "거짓 fail-closed 못 찾음" · `p3_fuzz_shapes.out` "cases 30000 non-Stop exception kinds 0" · `p6_rejected.out` n 1.0/true/"1" · dup key · NaN · 1e400→inf · BOM · hidden dir = Stop ATTEMPT_LEDGER_MISMATCH (글자 꼴 code 5 = rejected 그대로 = F5 · dir = PB-03 한정) · 원장 PC12 심각도 같음 | 같음 |
| 75 | §5-2 F1: outdir + 요청 칸 함께 고침 **11 가지** · 범위 밖 arms 9·0·−1·10**30 · arm_list []·[0]·[9]·[3,3]·[3,1] · 범위 안 arms 2 · 실제 원장 `--add --resume` rc 0 | `p1_outdir_coedit.out`: RUNNER_RC 함께 고침 **10 가지** 전부 True (arms 9 · 2 · 0 · −1 · 10**30 · arm_list [] · [0] · [9] · [3,3] · [3,1]) + TIME_LIMIT 2 (arms 9 · 2) True = True 줄 **12** · 정직 False · `p2_real_ledger.out` (1b) resume_ok True · resume_rc 0 | **다름** — "11 가지" 는 어느 셈과도 안 맞음 (RUNNER_RC 변종 10 · True 줄 12) |
| 76 | §5-2 F2: 정직 GU rc 1 (끝 기록 확인 False) 의 런 기록 rc 1→0 한 칸 = group_unconfirmed · 자격 · rc 0 · {timeout · null} 두 칸도 | `p2_real_ledger.out` (2a) cause runner_rc · resume_ok False · (2b) group_unconfirmed · True · resume_rc 0 · (2c) 두 칸 True · rc 0 | 같음 |
| 77 | §5-2 F2 과장 확인: `6a81f0c55` 커밋 글 「옛 = 한 칸 손질 넷 (… · GU 기록 rc) …」 · 「한 칸 손질 넷이 있었다 · 이번에 닫음」 · N/REPORT §8 「그 넷 (+ 옆 이름 outdir) 을 닫음」 · CT06 S2_forged_GU_rc0 = CHAIN_OK1 (확인 True) 위에서만 | `git log -1 --format=%B 6a81f0c55` 9 행 "옛 = 한 칸 손질 넷 (멈춤 이름 · 멈춘 런 이름 · outdir · GU 기록 rc)" · 11 행 "(한 칸 손질 넷이 있었다 · 이번에 닫음)" · `docs/reviews/rint2_rr2_fix_evidence_20261105/pc10_n_fix/REPORT.md` 68 행 "그 넷 (+ 옆 이름 outdir) 을 닫음" · 시험 15078·15085 | 같음 |
| 78 | §5-2 F3·F4·F5 자리 · 탐침 파일 (p4 · p5 · p6) · F5 = REPORT_EXT §8 "code 의 STOPS 소속 안 봄" | 줄 번호 = 행 69 · 파일 17 개 존재 · REPORT_EXT §8 세째 불릿 "code 의 STOPS 소속 = 안 봄" | 같음 |
| 79 | §6 Q2: 정상 생산자 꼴 행 변화 0 (N · X rows_diff_summary.json) | N CT01 `accepted_rows_changed: []` (changed 90 = 전부 resume True→False · 반대 0) · CT02 ctl_changed [] · X CT01 changed 0 · CT02 {} | 같음 |
| 80 | §6 Q3: 탐침 303/311 · 다른 8 = known_PC6_05 + summary_<7>_TIME_LIMIT_None | X results not-ok 8 = `known_PC6_05_summary_missing_log_resume` + `summary_{plain,python,oom,host,disk,gpu,cupy_oom}_TIME_LIMIT_None` · N results 같은 8 · `compare_prev.out` "same names: True · same content: True" | 같음 |
| 81 | §7: 회차 ② 요청서 §6 = 빠진 물리 | `codex_rint2_rr_round2_request_20261103.md` 253 행 "## 6. 빠진 물리 원장" | 같음 |
| 82 | 머리: 그 사이 Rint ② 밖 커밋 (50kg · Ⓐ G2c · FAM · /emod · 후막 · 게이트 나누기) 섞임 | 행 32 · 34 · 35 · 40 stat | 같음 |
| 83 | §1: 회차 ② 판정 · 반입 · 수정 계획 = 1 + 84 + 1 | 판정문 blob · 84 · 수정 계획 blob | 같음 |
| 84 | §3 PC10-05·07 = 문구 (주석 · 보고서) · 시험 — | P10/REPORT §8 PB-07 · 원장 PC10-05·07 claimed_fixed · 코드 변경 = 문구 (P10 code_sha256 "PB-05 (문구 … 동작 무변경)") | 같음 |
| 85 | §2 `a69bf7d53` 보고 = `README_import.md` 존재 · §2 `2b3c42c6c` 보고 = handoff 존재 | `ls-tree` blob 둘 | 같음 |
| 86 | 머리: 사전 공격 ① ② ③ 반영 (③ = 독립 에이전트 diff 공격 = preattack12) | `preattack12/` 17 파일 · REPORT "독립 · diff 만" · 변이 기록 = X/logs · N/logs | 같음 |

## 2. 다름 (1)

| # | 요청서 | 실제 | 고칠 문장 |
|---|---|---|---|
| 75 | §5-2 F1 "함께 고침 11 가지" | `preattack12/p1_outdir_coedit.out`: RUNNER_RC 블록 함께 고침 변종 **10** (전부 True) + TIME_LIMIT 블록 2 (arms 9 · 2 · True) = True 줄 **12** · 11 이 되는 셈 없음 (preattack12/REPORT.md 의 "11 가지" 를 그대로 옮긴 것) | "함께 고침 RUNNER_RC 10 가지 전부 True (+ TIME_LIMIT 2 가지도 True · p1 출력 True 12 줄)" |

## 3. 미확인 (4)

| # | 요청서 | 왜 못 확인했나 | 권고 |
|---|---|---|---|
| 5 | 리뷰 핀 = 이 커밋 · 작업 가지 B · push | 이 리포에서 `e540c73fe` 는 `worktree-agent-a1677a57e4e2a38f0` 에만 있고 `origin/claude/sdcp-dem-manuscript-si-pqwtv8` = `6a81f0c55` | push 뒤 `git branch -r --contains <핀>` 결과를 PIN.txt · 진행 기록에 적는다 |
| 17 | §0 ③ "(판정문 §9 · 0 건)" | 결과 부재는 리포로 증명 불가 · §9 는 ID 를 안 나열함 (ID 출처 = 수정 계획 Q5) | "(현장 자격 = 판정문 §9 · 항목 = 수정 계획 Q5 · 결과 아직 0 건)" |
| 30 | PIN.txt · ZIP 이름 · git archive · blob · sha256 대조 | ZIP · PIN.txt = 리포 밖 · 아직 없음 | ZIP 만든 뒤 대조 결과 (파일 수 · sha256) 를 진행 기록에 |
| 71 | `check_review_findings.py` rc 0 (앞 · 뒤) | 읽기 전용 작업이라 실행 안 함 (합계 5 종은 JSON 집계로 모두 같음) | 그대로 (실행 로그 한 줄 첨부면 닫힘) |

## 4. 과장 · 모호 (전칭 · 숫자 표기) — 좁힐 문장

| 자리 | 지금 문장 | 문제 | 권고 문장 |
|---|---|---|---|
| §3 RR2-02 행 · 수정 계획 Q3 | "Q9 설계 69 줄 취소선 + 현행 계약" | 실제 = **69 번째 줄 한 줄** 수정 (취소선 두 조각 + 정정 문장) · "69 개 줄" 로 읽힘 · 파일의 `~~` 줄 수 17 → 18 | "Q9 설계 69 번째 줄 (1 줄) 의 두 어구 취소선 + 11-05 정정 문장" |
| §1 실행 의존 행 | "시험 import 다섯 (cam_kinetics · check_method_discipline · sdcp_gain_verdict · test_ca_ext_b6 · test_ca_ext_runner)" | 다섯 중 `test_rint_r_chain.py` 가 직접 import 하는 것 0 · 전부 간접 (test_ca_ext_b6 ← test_carbon_junction · test_ca_ext_runner ← e2e · check_method_discipline ← test_ca_ext_* · sdcp_gain_verdict ← check_method_discipline · cam_kinetics ← step4_dyn) | "시험이 간접 import 하는 다섯 (…)" 또는 사슬을 한 줄로 |
| §5-2 F1 | "함께 고침 11 가지" | 행 75 (다름) | 위 표 |
| §3 `6a81f0c55` 회귀 행 | "변이 = 첫 판 26 중 25 (생존 K1 = 동등)" | 한정어 "첫 판" 은 있으나 같은 묶음의 ext 재실행 (`X/logs/mutation_pc10_rerun.out`) = 26 중 24 잡힘 · 생존 1 · 건너뜀 1 은 안 적음 | "첫 판 26 중 25 (N/logs/mutation_pc10_K1c.out) · ext 재실행 24 잡힘 · 생존 1 (K1 동등) · 건너뜀 1 (X/logs/mutation_pc10_rerun.out)" |
| §2 `342eff6e1` 행 | "원장 PC10-01–07 claimed_fixed · 같은 커밋 = /emod · LHS 대기 지문" | 같은 커밋이 §1 에 보내는 `docs/reviews/rint2_s0_mem_probe_20261106/` (3 파일) 과 `SELF-157` (open · P3) 도 넣었는데 §2 에 없음 → 보내는 폴더의 출처 커밋이 §2 에 안 보임 | "… · S0 메모리 근거 측정 `rint2_s0_mem_probe_20261106/` 3 파일 · 원장 SELF-157 (open) 도 같은 커밋" |
| 머리 (리뷰 핀 줄) | "작업 가지 B … · push" | 지금 원격 B = `6a81f0c55` (행 5) | push 뒤에만 쓰거나 "push 예정 · PIN.txt 로 확정" |
| §0 ③ | "(판정문 §9 · 0 건)" | 행 17 | 위 표 |
| 원장 (요청서 밖 · 참고) | — | RR2-01·02·03 · PC6-05 · PC9-01–07 의 `claimed_fixed_sha` 는 9 자리 `f5b00a838` · PC10 · PC11 · SELF-155 는 40 자리 — 같은 원장 안에서 꼴이 섞임 (요청서 주장은 아님) | 다음 원장 손질 때 40 자리로 통일 |

## 5. 전칭 낱말 점검 결과 (요약)

- "전부 · 모두 · 12/12 · 0 건 · 무변경 · 같음 · 닫힘" 중 리포에서 뒷받침된 것: 행 3 · 19 · 22–24 (sha256 671/671) · 26 (diff 0) · 47 · 50 · 56 · 57 · 68 · 69 · 70 · 72 · 74 · 76 · 77 · 79 · 80.
- 뒷받침 안 되는 전칭: "함께 고침 11 가지" (행 75 · 수 자체 불일치).  리포 밖이라 못 본 것: push · ZIP · PIN.txt · 검사기 rc (행 5 · 30 · 71) · 결과 부재 (행 17).
