# Codex 회차 ⑤ 짧은 재확인 요청 — Rint ② 회차 ④ (11-09) PC14-02 · PC14-03 · RR4-01 고침 + 사전 공격 15 처분 (PC15-01–06) + kgy S0 단계 1 채택 (SELF-155 · SELF-159) (2026-11-09 · 사전 공격 ① 반영 · 발송 = 1저자)

> **한 줄**: Codex 회차 ④ (`docs/reviews/codex_review_rint2_rr_round4_20261109.md` · 리뷰 핀 `1f9f3607e` · 지정 11 한정 닫힘 · 재개 정책 전체 HOLD · 새 P1/P2 없음 · 새 P3 RR4-01) 에서 열림으로 남은 PC14-02 · PC14-03 (재개 출처 · 복사 경계) 을 판정문 §3 의 최소 처리 선택지 1 (권고 · 공통 검증) 로 고쳤고 (`e94f09905`), RR4-01 회계를 제자리 정정 + 상주 음성 행으로 닫으려 한다.  그 고침을 사전 공격 15 회차 (독립 · diff 만) 로 다시 깼고 (P1 0 · P2 3 · P3 3), 여섯 다 고침 C (`db8322e70`) 로 고쳤다 (§3 · §5).  재개 규칙에 대한 우리 쪽 사전 공격은 15 회차로 끝낸다 (1저자 11-09 처분 기준 · §4 · Q6).  kgy S0 단계 1 (SBE) 실침대 재실행 채택 (SELF-155 · SELF-159) 도 이 회차에 함께 묻는다 (Q5).
> **리뷰 핀** = 이 요청서가 든 커밋 (작업 가지 B `claude/sdcp-dem-manuscript-si-pqwtv8` · push · stoic `claude/stoic-knuth-NObVQ` = 복귀 전까지 `6a81f0c55` 에서 동결) · 번호 = ZIP 의 PIN.txt (이 파일은 그 커밋 안이라 제 번호를 못 적는다).
> **1저자** — 11-09 *"권고대로"* (수정 계획 `docs/reviews/rint2_rr4_fix_plan_20261109.md` §5 Q1–Q3 = (가)) · 발송 = 1저자.

## 0. 이번에 닫는 것 / 닫지 않는 것

| 이번에 닫으려는 것 (판정 요청) | 닫지 않는 것 (이 회차 범위 밖) |
|---|---|
| ① PC14-02 (P3) — 복사 / 새 런 경계 ↔ 원천 디스크 (공통 검증 ⓒ · ⓓ) — `e94f09905` | S0 단계 2 와 그 앞 순서 (s_min → ⑥ → 기하 · 반복 수 → 숫자 · 실행 정책 → 새 계획 / 핀 봉인) — 단계 1 채택은 단계 2 · 등록 R 진입 승인이 아니다 |
| ② PC14-03 (P3) — attempt.json ↔ 원장 항목 (ⓐ) · resume.from ↔ 그 시점 유효 사슬 끝 (ⓑ) · 원천 확인 못 함 = 거부 — `e94f09905` | PC13-03 · PC11-05–08 (한정 그대로) |
| ③ RR4-01 (P3) — 회차 ④ 요청서 103 줄 · 사전 공격 14 보고 9 줄 제자리 정정 + 상주 음성 행 RR4C (M56 검출) — `e94f09905` | 현장 자격 (프로세스 · 잠금 · 권한 · 파일 시스템 · FIFO · NFS) · 12 단위 끝-끝 · 봉인 (숫자 칸 · 실행 정책 · S0 / R 계획 해시) · S0 단계 2 · 등록 R · 정량 판정 · 생산 GO |
| ④ PC15-01 – 06 (사전 공격 15 · P2 셋 · P3 셋) — 디스크상 첫 미완료 런 다시 대조 (요약의 멈춤 · 요약 유무와 무관) · 새 런 기록 ↔ 이 시도 디스크 · 원천을 못 찾으면 결과 줄 안 씀 (ATTEMPT_OPEN) · ⓐ 형까지 · 꼴 틀린 요약 = [꼴] 사유 · 가르는 행 — `db8322e70` | 재개 정책 전체 GO 의 최종 문안 = Q4 · Q6 으로 묻는다 (판정문 §6 문장의 갱신 · GO 조건 두 문장) |
| ⑤ SELF-155 (P2) — kgy S0 단계 1 (SBE) 실침대 재실행 채택 (핀 `f47bde0f6` · 1저자 11-08 kgy · 반입 `4d76378b9` · 채택 대조 `docs/data/rint2_s0_sbe_20261108/ADOPTION_CHECK.md` = 수정 계획 `docs/reviews/rint2_rr3_fix_plan_20261108.md` §5 조건 1–5) + SELF-159 (P2) — 그 반입 도구의 rc 근거 (고친 판 = `docs/data/rint2_s0_sbe_20261108/tools/import_s0_tgz.py`) | σ 값 (단계 1 = 접합 census · 계획 · σ 안 봄) · 실제 peak RSS (5 초 표본 최대만) · 원 입력 무쓰기의 묶음 밖 증명 |

## 1. 보내는 것 (ZIP · repo/ = 리뷰 핀 blob 그대로 + PIN.txt)

| 묶음 | 파일 | 수 |
|---|---|---|
| 이 요청서 | `docs/reviews/codex_rint2_rr_round5_request_20261109.md` | 1 |
| 회차 ④ 판정 · 반입 · 수정 계획 · 회차 ④ 요청서 (RR4-01 정정 자리) | `docs/reviews/codex_review_rint2_rr_round4_20261109.md` · `docs/reviews/codex_rint2_rr_round4_evidence_20261109/` · `docs/reviews/rint2_rr4_fix_plan_20261109.md` · `docs/reviews/codex_rint2_rr_round4_request_20261109.md` | 390 (판정 1 · 반입 387 · 계획 1 · 요청서 1) |
| 고침 증거 · 사전 공격 15 | `docs/reviews/rint2_rr4_fix_evidence_20261109/` (회차 ④ 고침 보고 `REPORT.md` · code.diff · logs · tools · 사전 공격 15 `preattack15/` · 고침 C `pa15_fix/`) | 180 (`preattack15/` 43 · `pa15_fix/` 96 · 회차 ④ 고침 41) |
| RR4-01 정정 자리 (사전 공격 14) | `docs/reviews/rint2_rr2_fix_evidence_20261105/preattack14/` (REPORT.md 9 줄 · SHA256SUMS 의 그 줄) | 26 |
| kgy S0 단계 1 반입 · 채택 대조 (SELF-155 · SELF-159) | `docs/data/rint2_s0_sbe_20261108/` (README · MANIFEST.tsv · NPZ_SHA256.txt · files/ · ADOPTION_CHECK.md · tools/ · SHA256SUMS) · 채택 조건 `docs/reviews/rint2_rr3_fix_plan_20261108.md` · 메모리 고침 보고 `docs/reviews/rint2_s0_mem_fix_20261106/` | 172 (반입 15 · 계획 1 · 메모리 고침 156) |
| 원장 | `docs/reviews/findings.json` · `docs/reviews/claims.json` (S0 kit JSON 숫자 글자 = 철회 패턴 우연 겹침 → allowed_in 한 파일) | 2 |
| 바뀐 Rint ② 코드 · 시험 (`1f9f3607e` → 핀) | `scripts/rint_r_chain.py` · `scripts/test_rint_r_chain.py` (그 밖 scripts 변경 = `scripts/check_all.sh` 주간보고 시험 한 줄 · DEM 세대 2 준비 넷 (`scripts/make_dem_gen2_decks.py` · `scripts/dem_gen2_qualification.py` · 그 시험 둘) = Rint ② 밖) | 2 |
| 실행 의존 (`1f9f3607e` 와 diff 0) | 사슬 CODE_FILES 나머지 18 · 간접 import 다섯 · 끝-끝 · 시험 둘 (회차 ④ 와 같은 목록) | 26 |

- repo/ 합 = 799 파일 (위 표의 합) · ZIP 맨 위 PIN.txt (핀 40 자리 + 가지 이름) · SHA256SUMS (repo/ 799 + PIN.txt = 800 줄) · 빌더가 핀의 ls-tree blob 과 푼 바이트를 대조한다.

## 2. 무엇이 바뀌었나 (`1f9f3607e` 뒤 · Rint ② 몫만)

| 커밋 | 무엇 | 보고 |
|---|---|---|
| `62623c7f8` | 회차 ④ 판정 반입 · 우리 트리 재현 · 원장 (지정 11 verified · PC14-02 · 03 열림 메모 · 새 open RR4-01) · 수정 계획 초안 | `docs/reviews/codex_rint2_rr_round4_evidence_20261109/` · 수정 계획 §1–§5 |
| `e94f09905` | 고침 (시험 먼저 · 작업 트리 커밋 하나) — 공통 검증 · 세 자리 · RR4-01 정정 · RR4A–E | `docs/reviews/rint2_rr4_fix_evidence_20261109/REPORT.md` · 수정 계획 §6 |
| `69d714d09` | 설명 문서 REPORT.md · 원장 PC14-02 · 03 · RR4-01 claimed_fixed · 진행 기록 | — |
| `4d76378b9` | kgy S0 단계 1 (SBE) 결과 반입 · 채택 (rc 0 = rss.log `rc=` 줄 · 여섯 출력 6/6 · 계획 sha 네 곳 같음 · 코드 지문 7/7 = `f47bde0f6`) · 고친 반입 도구 | `docs/data/rint2_s0_sbe_20261108/ADOPTION_CHECK.md` |
| `8842ed2bd` | 원장 SELF-155 메모 (실침대 채택 · claimed_fixed 그대로) · 새 SELF-159 (반입 도구 rc 근거 · P2 · claimed_fixed `4d76378b9`) | 원장 |
| `7cdc78111` | 원장 claims.json — S0 kit JSON 의 접합 census 긴 접촉 배수 `mult` 4 개 숫자 글자가 철회 패턴 "1.14508" · "1.1232" 와 겹침 (인용 아님) → 두 패턴 allowed_in 에 그 파일 하나 | 진행 기록 |
| `db8322e70` | 사전 공격 15 반입 (`preattack15/` · 보고 · 탐침 18 · 출력 23 · SHA256SUMS 42 줄) · 처분 = 고침 C (시험 먼저 · 작업 트리 커밋 하나 (로컬 f8cc7732e · push 안 함) → `cherry-pick -x` · 진행 기록 끝줄 충돌 = 둘 다 살림 · 나머지 141 파일 blob 같음) — PC15-01 – 06 | `docs/reviews/rint2_rr4_fix_evidence_20261109/pa15_fix/` · 수정 계획 §7 |
| (이 커밋) | 이 요청서 · 고침 C 보고 `docs/reviews/rint2_rr4_fix_evidence_20261109/pa15_fix/REPORT.md` (작업 트리 에이전트 보고를 그대로 옮김) · 원장 PC15-01 – 06 claimed_fixed (`db8322e70`) · PC14-03 회귀 글 메모 (RR4D F1 바뀜) · CLAUDE.md 처분 기준 한 줄 · 진행 기록 | — |

- Rint ② 밖 (ZIP 에 안 넣음) = `e33cbafec` · `dc85907c8` (LHS12 수령) · `3e32488bf` · `29ffda1ca` · `e814b73c3` (믹서 수령) · `9b1fec84a` (주간보고) · `8a67b7eae` · `e48e5fa04` (비 Rint 종합 수령) · `a0eac62b3` (비 Rint 다음 준비표) · `27ed57b96` (DEM 세대 2 준비) · `5a9b73d1f` · `095bf43f2` (LHS 정책 비준 수령 · 동결안 초안) · `1df1ba5a7` (믹서 비활성 사본) · `160b9ee10` · `ce1b9fa51` · `2be18e9ec` (DEM 세대 2 G2PREP-01–04 수정 · 반입 · 한정 수용) · `f46c73f4c` · `ef9a94c90` (믹서 MIP-01) · `a0c2c0cbf` (DEM G2PREP 재확인 수령 · 이종기술 과제 2차년도 연차보고서 요지 기록).

## 3. finding → 고친 자리 → 시험 (F = `docs/reviews/rint2_rr4_fix_evidence_20261109` · G = `docs/reviews/rint2_rr4_fix_evidence_20261109/pa15_fix` · 줄 번호 = 고친 판 `scripts/rint_r_chain.py`)

| finding | 커밋 | 고친 자리 (요지) | 시험 · 증거 |
|---|---|---|---|
| PC14-02 (P3) | `e94f09905` | `resume_provenance_problem` ⓒ `resume_boundary_problem` (복사 기록 런 = 새 런 앞 · copied_from = from (int) · 원천에서 끝난 런 (`_src_run_done` = `_src_done` 과 같은 규칙) · 이 시도 groups/&lt;런&gt;.launch · end 바이트 = 원천 · 런 폴더 payload = 원천 / 첫 새 런 = 원천에서 안 끝난 런 · 새 런 launch ≠ 원천 (원천에 같은 이름 있을 때)) · ⓓ `resume_first_new_problem` (실제 첫 새 런 = rerun · 원천 payload 다시 대조 = compared) · 멈춘 런 = rerun 이어도 ⓐ–ⓒ | RR4A N1 · N2 · Z1 · Z2 = 세 자리 [ⓒ] · RR4D F3 [ⓓ] · F/REPORT.md · F/logs/rr4_rows_summary.log |
| PC14-03 (P3) | `e94f09905` | ⓐ `attempt_entry_diff` (= `found_attempts_problem` 과 같은 함수) · ⓑ `resume_from_problem` (from = `adoption(st, target, upto=n)['effective']`) · 원천 `resume_source_locate` (결과 줄 폴더 이름 · 링크 아님 · 하나 · attempt.json 번호 · 대상 · 요약 sha · 못 찾음 = [원천] fail-closed) · 부르는 자리 = 결과 줄 쓰기 (`attempt_close` · `recover_ledger` → `attempt_result`) · 다시 셈 (`result_recount` · `result_line_problem` = 같은 원장 상태 · 같은 함수 `result_fields_ledger`) · 다음 재개 허용 (`attempt_order_problem` → `resume_chain_provenance_problem` · `resume_chain_problem`) | RR4A N3 · N3a · Z3 [ⓐ] · N4 · Z4 [ⓑ] · RR4D F2 [원천] · RR4B 양성 12/12 · RR4E 구조 · (RR4D F1 = 고침 C 뒤 "[원천] 이면 결과 줄 안 씀" 으로 기대값 바뀜 = PC15-03 · 원장 PC14-03 메모) |
| RR4-01 (P3) | `e94f09905` | 회차 ④ 요청서 103 줄 · 사전 공격 14 보고 9 줄 = 취소선 + "11-09 정정 (RR4-01 · 판정문 §4)" (동치 1 · 45/50 · 비동치 생존 5) · 원로그 바이트 그대로 · 상주 음성 행 RR4C (일반 파일 attempt_1 + 옆 거부 기록) | RR4C · 변이 M56 → RR4C 실패 (F/logs/mutation_rr4.log) |
| SELF-155 (P2) | `f47bde0f6` (11-06 메모리 고침) · `4d76378b9` (실침대 채택) | 조각별 반경 · 후보 17,701,828 → 61,131 (합성) → kgy 실침대 SBE 단계 1 = rc 0 · 5,384 s · 표본 최대 RSS 5,694,360 kB (≈ 5.43 GiB · 5 초 간격 표본 · 실제 peak 아님 · 상한 41 GB · 11-04 첫 시도 = 52.1 GB 신호 kill) · 접합 117,583 행 · 접촉 117,070 행 (꼴만) · 계획 sha `4da98863…` | `docs/data/rint2_s0_sbe_20261108/ADOPTION_CHECK.md` 조건 1–5 · `docs/reviews/rint2_s0_mem_fix_20261106/REPORT.md` |
| SELF-159 (P2) | `4d76378b9` | 반입 도구 rc 근거 = 감시 셸 `run2.sh` 15 줄이 쓰는 rss.log 끝 `rc=` 줄 하나 (`CAP_TERM` = 채택 안 함 · rc 줄 둘 · 없음 = 거부) · 옛 판 = 생산자 꼴 실패 넷을 채택 · 실제 성공을 rc 미확인으로 | `docs/data/rint2_s0_sbe_20261108/tools/selftest.log` (옛 판 5/5 채택 → 고친 판 정상 1 채택 · 4 거부) |
| PC15-01 (P2) | `db8322e70` | 사전 공격 15 P2-1 — 재실행 런이 이 시도에서 끝났는데 (사슬 쪽 원인 None · rc 0 · 확인) 요약이 "대조 전 멈춤" 이거나 요약이 없으면 ⓓ 가 대조하지 않아 자격 True · 다음 재개가 대조 없이 복사 → `resume_disk_rerun` (4528–4549 · 디스크상 첫 미완료 런 = 원천 ∪ 이 시도 groups 시작 기록 · 번호 차례 · `_src_run_done`) · `resume_first_new_problem` ⓓ (4676–4707 · 그 런이 이 시도에서 끝났으면 원천 남은 payload ↔ 디스크 폴더 다시 대조 · 요약의 멈춤 · 요약 유무와 무관) · 요약 없는 재실행 시도 = ⓐ + 원천 (원장 그 시점 유효 사슬 끝) + 디스크 rerun + ⓓ (옛 = ⓐ 만) | RR5A 8 행 (A1 위조 signal_after · A2 요약 지움 + 다른 payload · A3 정직 signal_after + 다른 payload = 거부 [ⓓ] · A4 정직 signal_after + 같은 payload · A5 요약 지움 + 같은 payload · A6 재실행 런 rc 1 · A7 끝났는데 출력 폴더 없음 = 통과 · A8 그룹 미확인 = 차례 단언) · 탐침 무변경 p1 · p2 · p13 = 받음 → 거부 [ⓓ] · G/logs/probe_compare.log |
| PC15-02 (P2) | `db8322e70` | P2-2 — 새 런 기록의 이름 · outdir 가 이 시도 디스크와 묶이지 않아 ⓓ (와 옛 ⑤) 가 없는 폴더끼리 대조 → `resume_boundary_problem` ⓒ 새 가드 다섯 (4618 resume.rerun = 디스크 rerun · 4649 첫 새 런 = 디스크 rerun · 4654 새 런 groups 시작 · 끝 결합 · 4658 디스크 폴더 ⊆ 기록 outdir · 4661 멈춘 런 앞 새 런 = 이 시도에서 끝남 + 폴더 있음) · `run_dirs` · `resume_recompare_run` (다시 대조 = 디스크 출력 폴더 기준 · ⑤ 도 같은 함수) | RR5B 15 행 (정직 B0a · B0b · B0c = 통과 · 나머지 = 거부 또는 차례 단언 · 행 이름 = G/logs/rr5_row_names.log) · p8 = 받음 → 거부 (폴더 증거 ⑤ 가 먼저 자격 False · 행 B1) · p9 = 받음 → 거부 [ⓒ] |
| PC15-03 (P2) | `db8322e70` | P2-3 — 쓰기와 다시 셈이 원천을 서로 다른 곳에서 찾아 [원천] False 줄이 영구히 남고 판정이 ATTEMPT_LEDGER_MISMATCH → `class ResultHeld` · `attempt_result` (원천 사유 = 결과 줄 안 씀) · `attempt_close` (ATTEMPT_OPEN · rc 3) · `recover_ledger` (못 쓴 수 · 화면 사유) | RR5C 3 행 · p3 = recover rc 0 · False 줄 → rc 3 · 결과 줄 없음 · 원천을 되돌린 뒤 recover = 자격 True · 판정 ok (행 C1) · p6 원천 링크 = rc 3 · 줄 없음 · RR4D F1 기대값 [0, False, [원천], False] → [3, None, [], True] |
| PC15-04 (P3) | `db8322e70` | P3-1 — ⓐ `attempt_entry_diff` 의 `!=` 가 bool · float 를 통과 (resume_of true · 1.0 = 1) → 형까지 같아야 같음 (5227) | RR5E 3 행 · p7 = 받음 → 거부 [ⓐ] · resume_of 1 (정직) 그대로 · null 그대로 거부 |
| PC15-05 (P3 · 회귀) | `db8322e70` | P3-2 — 손으로 고친 결과 줄 + 꼴 틀린 요약 (runs = int · stop = str) 에서 `attempt_order_problem` · `resume_chain_problem` traceback → `resume_provenance_problem` 이 ⓑ 앞에서 `summary_shape_problem` = [꼴] 사유 (4736) | RR5D 2 행 · p14 · p15 = TypeError · AttributeError → 사유 [꼴] · RESUME_NOT_ALLOWED (멈춤 이름 = 바탕 e48e5fa04 와 다름 · §4) |
| PC15-06 (P3) | `db8322e70` | P3-3 — 가르는 입력이 있는 생존 변이에 그 가드 하나만 가르는 행 없음 → RR5F 21 행 + 변이 → 행 표 (entry_no_machine → F1 · c_bytes → F2 · F3 · c_launch_only → F2 · c_end_only → F3 · c_payload → F4 · loc_digest → F5 · R1 짝 c_copy_srcdone → F6 · F18 · R2 짝 c_first_new_done → RR5B B7 · c_new_launch_same → F7 · 다시 셈 자리 셋 → F8 · close_old → RR5C C2 · C3 · N_src_names_only → RR5B B0c · B9) | 변이 71 = 잡힘 68 · 생존 2 (동등 · §4) · 적용 안 됨 1 (d_name = 그 가드를 지웠다) · 무변이 25/25 · G/logs/mutation_final.log · G/logs/mutant_rows.log |
| 회귀 (`e94f09905`) | — | 시험한 판 = 커밋 blob (F/code_sha256.txt) | `--only RR3,PA13,PA14,RR4` 15/19 → 19/19 · 사슬 495 → 500/500 · 끝-끝 51 PASS · 0 FAIL · kgy 판 3.8.20 11 묶음 (사슬 500/500) · 변이 12/12 · 무변이 5/5 · Codex 재개 탐침 무변경 = 181 줄 AssertionError (PC14_03 attempt-null 단언 · 기대한 뒤집힘) |
| 회귀 (`db8322e70` · 고침 C) | — | 시험한 판 = 커밋 blob (G/code_sha256.txt · `scripts/rint_r_chain.py` 986bbdb3… · `scripts/test_rint_r_chain.py` 98480e89… · 바탕 + code.diff = 고친 판 2/2) · 생산자 조각 11 (`_src_done` · `run` · `_copy` · `_execute` · `_prepare` · `run_in_group` · `stop_trace` · `run_traces` · `record_outdir` · `resume_leftovers` · `group_pair`) = 바탕과 바이트 같음 11/11 | 시험 먼저 `--only RR3,PA13,PA14,RR4,RR5` 18/25 → 25/25 · 행 단위 (RR5 52 + RR4D 3) 55 중 다름 23 → 0 · 사슬 500 → 506/506 · 끝-끝 51 PASS · 0 FAIL · kgy 판 3.8.20 11 묶음 (사슬 506/506) · 정적 점검 rc 0 · 웹앱 grep 0 · Codex 재개 탐침 무변경 = 같은 181 줄 AssertionError (G/logs/codex_probe_rerun.log) |

## 4. 알려진 한정 (닫지 않는 것 · G = `docs/reviews/rint2_rr4_fix_evidence_20261109/pa15_fix`)

| 한정 | 출처 | 처분 |
|---|---|---|
| 재실행 러너의 복사 판단 `ResumeRunner._src_done` = 그대로 (다음 재개 허용 관문이 앞에서 막는다 · sha256 b530c2ad… = 바탕 · 고침 C 뒤에도 생산자 조각 11 바이트 같음) | 수정 계획 §2 · F/logs/src_done_sha.log · G/logs/producer_sha.log | 한정 |
| 모든 사본 (launch / end · payload · 요약 · attempt.json) 을 일관되게 고친 위조 = 계약 밖 | 판정문 §3 | 한정 |
| (고침 C 로 바뀜) 요약 없는 재실행 시도 = ⓐ + 원천 (원장 그 시점 유효 사슬 끝) + 디스크상 첫 미완료 런 + ⓓ (옛 = ⓐ 만 · PC15-01) · 요약 쪽 경계 ⓒ 는 요약이 있을 때만 · 요약 없는 새 시도 (resume_of null) = ⓐ 만 · ⓐ = 형까지 같음 (옛 `!=` · PC15-04) · 새 런 launch 다름 = 원천에 같은 이름 launch 가 있을 때만 · 다음 재개 = 시작 기록 바탕 (옮김 · 지움 = 거부) | F/REPORT.md 한정 · G/REPORT.md §1 | 한정 |
| 결과 줄 칸 · 원인 칸 = 그대로 (자격만 False · 사유 = 원장 커밋 글 · 화면) · 단 [원천] 사유 = 결과 줄을 쓰지 않는다 (ATTEMPT_OPEN · rc 3 · PC15-03) | F/REPORT.md 벗어남 ③ · G/REPORT.md §5 6 · 8 | Q3 |
| 고정물 `pa13_ledger` 항목 기계 'synthetic' → attempt.json 과 같은 MACH (기대값 그대로) | F/logs/pa13_old_fixture_check.log | Q3 |
| [원천] 때문에 못 쓴 정직 시도 = recover 가 "못 쓴 수" 로 남긴다 → 사람이 원천을 같은 바탕에 되돌린 뒤 recover (자동 아님) · 결과 줄을 쓴 뒤 원천을 지우거나 옮기면 다시 셈이 [원천] 으로 멈춘다 (판정 · 합치기 거부 = 맞는 동작 · 규칙 "원천 시도 폴더를 지우거나 옮기지 않는다") | G/REPORT.md §6 1–2 | 한정 (PC15-03) |
| 디스크상 첫 미완료 런 = groups 시작 기록 이름 (`<앞자리><번호>_<역할>`) 에 기댄다 · 꼴 밖 이름 = [ⓒ] 로 막음 (fail-closed) · graph 원천 런 = 다른 폴더 · 영향 없음 | G/REPORT.md §6 3 | 한정 (PC15-01 · 02) |
| PC15-02 "출력 폴더가 있어야" = 멈춘 런 앞 새 런 (이 시도에서 끝난 런) 에만 · 새 런 전부에는 "디스크 폴더 ⊆ 기록 outdir" 만 (멈춘 런은 러너가 폴더를 만들기 전에 죽을 수 있다 · 생산자 대조 · 거짓 거부 방지) | G/REPORT.md §5 2 | 한정 |
| V07 (중복 복사 기록) = 그대로 받음 (해 없음 · 바탕도 자격) | G/REPORT.md §6 4 · 사전 공격 15 "지켜진 것" | 한정 |
| 변이 생존 2 = 동등 — loc_symlink (원천 폴더가 링크면 `folder_digest` = None · 같은 [원천] · 사유 글만 다름) · c_new_launch_missing_ok (새 런 결합이 이미 launch 읽기를 요구 · 차이 = 두 읽기 사이 경쟁뿐 · 추정 · 시험으로 만들 수 없음) · 적용 안 됨 1 = d_name (그 가드를 고침 C 가 디스크 판단으로 바꿈) | G/REPORT.md §4 · G/logs/mutation_final.log | 한정 |
| PC15-05 멈춤 이름 = 바탕 `e48e5fa04` 와 다름 (고친 판 = 차례 · 사슬 모두 RESUME_NOT_ALLOWED + [꼴] · 바탕 = 차례 None · 사슬 ATTEMPT_LEDGER_MISMATCH) · `ResultHeld` 의 Stop 코드 = ATTEMPT_LEDGER_MISMATCH · 사슬 화면 = ATTEMPT_OPEN | G/REPORT.md §5 5 · 8 | Q3 |
| 런 기록과 시작 기록 사이 예외 = CHAIN_EXCEPTION (원래 자격 없음 · 공통 검증까지 가지 않는다) | G/REPORT.md §6 6 | 한정 |
| 처분 기준 (1저자 11-09 *"권고대로"*) — 재개 규칙 지적은 정직한 흐름 (끊김 · 재부팅 · 메모리 · 디스크 부족 · 다른 기계 재실행 · 비결정적 재계산 · 폴더 옮김) 에서 틀린 결과를 받아들이는 것만 고친다 · 손으로 고친 · 서로 어긋난 기록은 멈춤 (fail-closed) 확인 + 한정 (등급 무관) · 재개 규칙에 대한 자체 사전 공격 = 15 회차로 끝 | 진행 기록 11-09 | Q6 |
| 시험 = 합성 · 가짜 _execute · 실제 git 원장 · 이 컨테이너 (Linux · Python 3.11 · kgy 판 3.8.20 — 실제 kgy 3.8.10 · ibb · GPU · 실제 SIGKILL · flock · NFS 아님) · 웹앱 화면 없음 (grep 0) | F/logs/webapp_grep.log · G/logs/webapp_grep.log | 현장 자격 · 웹앱 = "없음" 기록 |
| `scripts/rint_r_chain.py` sha 바뀜 = R 계획 code key (CODE_FILES) 바뀜 → 봉인 = 새 핀 | 수정 계획 §4 | 봉인 때 |

## 5. 사전 공격 리뷰 (CLAUDE.md ①–④)

### 5-1. ① 숫자 · 전칭 ↔ 출처 (11-09 · 한 줄씩 대조 · G = `docs/reviews/rint2_rr4_fix_evidence_20261109/pa15_fix` · P = `docs/reviews/rint2_rr4_fix_evidence_20261109/preattack15`)

| 이 요청서의 숫자 · 전칭 | 출처 (리뷰 핀 안) | 대조 |
|---|---|---|
| 사전 공격 15 = P1 0 · P2 3 · P3 3 | P/REPORT.md 1 줄 · 절 머리 여섯 | 같음 |
| 탐침 18 · 출력 23 · SHA256SUMS 42 줄 | P/probes · P/out 파일 수 · `sha256sum -c` | 같음 · 42/42 OK |
| 사전 공격 15 때 변이 46 중 잡힘 19 · 생존 27 | P/REPORT.md §변이 | 같음 |
| 시험 먼저 `--only RR3,PA13,PA14,RR4,RR5` 18/25 → 25/25 | G/logs/tests_first_base.log · G/logs/after_subset.log | 같음 (FAILED RR4D · RR5A–F → 없음) |
| RR5 행 52 (A 8 · B 15 · C 3 · D 2 · E 3 · F 21) · 행 단위 55 중 다름 23 → 0 | G/logs/rr5_row_names.log · G/logs/rr5_rows_base.log (RR4D 1 · A 3 · B 10 · C 2 · D 2 · E 3 · F 2) · G/logs/rr5_rows_after.log | 같음 |
| 사슬 506/506 (409.6 s) · 끝-끝 51 PASS · 0 FAIL | G/logs/full_py311.log · G/logs/e2e_py311.log | 같음 |
| kgy 판 3.8.20 11 묶음 (사슬 506/506) | G/logs/py38_bundles.log | 같음 |
| 변이 71 = 잡힘 68 · 생존 2 · 적용 안 됨 1 · 무변이 25/25 | G/logs/mutation_final.log (끝 줄 · NOMUT 줄) | 같음 |
| 생산자 조각 11/11 바이트 같음 | G/logs/producer_sha.log | 같음 |
| 바탕 + code.diff = 고친 판 2/2 · 코드 sha256 986bbdb3… · 98480e89… | G/logs/apply_check.log · G/code_sha256.txt | 같음 |
| `cherry-pick` 142 파일 중 141 blob = 작업 트리 커밋 (진행 기록 1 = 충돌 풀이) | `git diff-tree` `db8322e70` ↔ 작업 트리 커밋 f8cc7732e (우리 로컬 객체 · push 안 함 → Codex 쪽 확인 = 위 code.diff 줄) | 같음 |
| Codex 회차 ④ 재개 탐침 무변경 = 181 줄 AssertionError | G/logs/codex_probe_rerun.log | 같음 |
| 고침 C 증거 SHA256SUMS 95 줄 | G/SHA256SUMS · `sha256sum -c` | 95/95 OK |
| SELF-155 = rc 0 · 5,384 s · 표본 최대 RSS 5,694,360 kB · 접합 117,583 · 접촉 117,070 · 계획 sha `4da98863…` | `docs/data/rint2_s0_sbe_20261108/ADOPTION_CHECK.md` | 같음 |
| 전칭 "실행 의존 26 = `1f9f3607e` 와 diff 0" | `git diff --stat 1f9f3607e <핀> -- (26 파일)` = 빈 출력 | 같음 (ZIP 만들 때 빌더가 다시 확인) |
| 전칭 "여섯 다 고쳤다" | 원장 PC15-01 – 06 = claimed_fixed (`db8322e70`) · §3 | 우리 쪽 주장 = Codex 판정 전 (verified 아님) |
| 전칭 "STOP 없음 (정직 흐름을 깨야만 고칠 수 있는 항목 없음)" | G/REPORT.md 머리 | 고친 쪽 진술 (탐침 p4 · p10 · p11 정직 = 그대로 받음 · RR5 정직 행 통과가 뒷받침) |

### 5-2. ② ③ 사전 공격 15 (11-09 · 독립 · diff 만 `e48e5fa04..e94f09905` · 고친 사람 보고 안 읽음 · 보고 `docs/reviews/rint2_rr4_fix_evidence_20261109/preattack15/REPORT.md`)

| 항목 | 결과 |
|---|---|
| 판정문 반례 9 꼴 (N1–N4 · N3a · Z1–Z4) | 세 자리 (결과 줄 쓰기 · 다시 셈 · 다음 재개 허용) 모두 거부 · 바탕 사슬에서는 9 행 모두 accepted = 시험이 옳은 이유로 실패 |
| 변형 반례 25 | 거부 18 · 받음 7 (해 있음 4 = P2-1 (a) · (b) · P2-2 (P8 · P9) / 해 없음 3 = V07 중복 복사 기록 · resume_of true · 1.0) |
| 정직 흐름 10 꼴 | 거짓 거부 = P2-3 하나 (원천을 다른 바탕으로 옮긴 정직 시도) |
| 지적 | P1 0 · P2 3 (PC15-01 – 03) · P3 3 (PC15-04 – 06) |
| 처분 (1저자 11-09 처분 기준 · §4) | P2 셋 = 정직 흐름 (비결정 재계산 · 폴더 옮김) 이 틀린 결과를 받아들이는 길 → 고침 · P3 셋 = 작고 같은 자리라 함께 고침 → 고침 C (`db8322e70` · §3) |
| 고침 C 뒤 탐침 무변경 재실행 | p1 · p2 · p13 · p8 · p9 · p3 · p6 · p7 · p14 · p15 = 기대한 뒤집힘 · p4 H1–H5 · p10 H6 · H7 · p11 정직 = 그대로 받음 · p5 V01–V18 = 같음 (거부 17 · V07 받음) · G/logs/probe_compare.log |
| 변이 (③) | 사전 공격 15 때 46 중 잡힘 19 → 고침 C 뒤 71 중 잡힘 68 (생존 2 = 동등 · §4) |
| 재개 규칙에 대한 우리 쪽 사전 공격 | 15 회차로 끝 (1저자 11-09 · 고침 C 뒤 다시 깨지 않았다) — 이 회차의 독립 검토 = Codex 회차 ⑤ |

### 5-3. ④ 닫는 것 / 닫지 않는 것 = §0.

## 6. 판정 요청 질문

| # | 질문 |
|---|---|
| Q1 | §3 의 finding 마다 닫힘 / 부분 / 열림 — PC14-02 · PC14-03 · RR4-01 · PC15-01 – 06 (사전 공격 15 처분 = 고침 C) · 판정문 §3 의 원 반례 (R1 · R2 · attempt-null · 3 시도 from 다시 결속) 재실행 = F/logs (원 탐침 무변경 = 기대한 뒤집힘). |
| Q2 | 공통 검증 (ⓐ · ⓑ · 원천 · ⓒ · ⓓ) 과 세 자리 연결 (결과 줄 쓰기 · 다시 셈 · 다음 재개 허용 = 한 함수) 이 판정문 §3 최소 처리 선택지 1 을 충족하는가 — 정직 3 시도 · 복사 / 새 런 양성 보존 (RR4B 12 · RR5 정직 행 · 사슬 506 · 끝-끝 51) · 고침 C 의 디스크 기준 판단 (디스크상 첫 미완료 런 · 새 런 기록 ↔ 이 시도 디스크 · [원천] = 결과 줄 안 씀) · 원천을 확인 못 하면 거부 (fail-closed) 가 정직 흐름을 깨지 않는가. |
| Q3 | 기대 바뀜을 받는가 — 결과 줄 원인 칸 그대로 · 자격만 False (사유 = 원장 커밋 글 · 화면) · 고정물 `pa13_ledger` 기계 칸 (생산자 꼴로 맞춤 · 기대값 그대로). |
| Q4 | 이 회차 뒤 판정문 §6 사용 가능 문장을 "재개 출처 · 복사 경계의 PC14-02/03 은 지정한 코드 · 합성 범위에서 닫힌다 · 코드 재개 정책 = 한정 목록 (§4) 안에서 수용" 으로 갱신할 수 있는가 (PC15-01 – 06 포함) — 남는 것 = 현장 자격 · 12 단위 끝-끝 · 봉인 → S0 단계 2 → 등록 R 진입 판단 (판정문 §6 순서 그대로 · kgy S0 단계 1 재실행 = Q5). |
| Q5 | SELF-155 — kgy S0 단계 1 실침대 채택 (`docs/data/rint2_s0_sbe_20261108/ADOPTION_CHECK.md`) 이 수정 계획 `docs/reviews/rint2_rr3_fix_plan_20261108.md` §5 조건 1–5 와 회차 ② 판정 §8 Q8 의 짧은 확인 항목 (종료 코드 / 신호 · 완성 산출물 · 새 핀 RSS · 시간 · 계획 해시 · 코드 출처) 을 충족해 닫히는가 · SELF-159 — 고친 반입 도구의 rc 근거 (rss.log `rc=` 한 줄 · CAP_TERM 거부) 가 생산자 꼴 (`docs/reviews/rint2_s0_mem_fix_20261106/tools/run2.sh`) 을 따르는가. |
| Q6 | 재개 규칙의 GO 조건을 문장으로 확정할 수 있는가 — "정직한 흐름 (끊김 · 재부팅 · 메모리 · 디스크 부족 · 다른 기계 재실행 · 비결정적 재계산 · 폴더 옮김) 에서 틀린 결과를 받아들이지 않는다 + 서로 어긋난 기록이면 결과 줄을 쓰기 전 · 다음 재개 전에 멈춘다 (fail-closed)" · 그 밖 (모든 사본의 일관된 위조 = 회차 ④ §3 의 계약 밖 · 손으로 고친 기록의 세부 진단 · 오류 메시지 꼴) 은 §4 한정 목록.  기준을 낮추자는 질문이 아니라, 판정문이 보장 범위를 이 두 문장으로 고정해 주면 이 회차 뒤 재개 규칙의 새 지적은 두 문장을 깨는 것만 막는 결함으로 다루겠다는 것 (1저자 11-09 처분 기준 · §4). 이 문장이 부족하면 무엇을 더해야 하는지 함께 적어 달라. |

## 7. 묻지 않는 것

- 등록 R 캠페인 GO · R 런 · 정량 판정 · 생산 GO · 숫자 칸의 값 · ⑦ SBE 탐침 (봉인 뒤).
- 회차 ④ 에서 닫힌 11 의 다시 판정 (회귀가 깨졌을 때만) · S0 단계 1 의 σ (안 봄) · S0 단계 2 · 빠진 물리 (v0 동결) · 다음 트랙 설계.
- Rint ② 밖 트랙 (50kg · LHS · 믹서 · FAM · DEM 세대 2 · 웹앱 · 후막).
