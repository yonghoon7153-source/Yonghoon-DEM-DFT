# Rint ② 회차 ② (11-05) 고침 — RR2-01 · 같은 부류 A1b · PC6-05 · 같은 부류 A2b · RR2-02 · RR2-03 · Q7 (11-06 · 작업 트리 에이전트 · 1저자 11-05 *"권고대로"*)

- 근거 = Codex 판정문 `docs/reviews/codex_review_rint2_rr_round2_20261105.md` (§1 RR2-01 · RR2-02 · RR2-03 · §5 PC6-05 · §10) · 비준한 수정 계획 `docs/reviews/rint2_rr2_fix_plan_20261105.md` Q1–Q4 · Q7 (모두 (가)) · Codex 탐침 `docs/reviews/codex_rint2_rr_round2_evidence_20261105/runtime_review/probe_runtime.py`.
- 한 번 잃은 구현 (기계 교체) 을 다시 한 것 — 바탕 = claude/stoic-knuth-NObVQ 의 push 된 끝 (수정 계획 비준 기록 커밋) · 그 위 = 항목마다 한 커밋 (A1 · A1b · A2 · A2b · A3 · A4 · A5) + 증거 커밋 · 커밋 번호는 반입 (cherry-pick) 뒤 바뀌므로 여기 적지 않는다.  (반입 = 메인 세션이 **한 커밋으로 합침** — 1저자 11-06 규칙 *커밋 하나 → 게이트 → push* · 항목별 코드 판 = 아래 code_sha256.txt.)
- 차례 = 코드 항목마다 시험 먼저 (고치기 전 코드에서 옳은 까닭으로 실패 = logs/before_*) → 고침 → 통과 (logs/after_*) → 사슬 전체 → 커밋 · 시험한 코드 sha256 = `docs/reviews/rint2_rr2_fix_evidence_20261105/logs/code_sha256.txt` (바탕 · 항목마다 · 끝).
- 환경 = Linux 6.18 · Python 3.11.18 · numpy 2.4.6 · scipy 1.17.1 · kgy 판 = uv CPython 3.8.20 · numpy 1.24.4 · scipy 1.10.1 · 한 컨테이너 4 코어 · root (권한 행 = uid 65534 로 내린 포크 자식 · 실제 EACCES).
- 원장 `docs/reviews/findings.json` 무변경 (978 · check_review_findings rc 0) · `scripts/check_all.sh` 안 돌림 · push 없음 · 웹앱 · ibb · kgy 실행 없음.

## 0. 쉽게 말하면

- **RR2-01** — 러너 rc 칸 하나를 자리마다 다르게 읽던 것을 판독 한 함수 (`rc_kind`) 로 모았다 · 요약 없는 시도의 끝 기록 rc 가 false · 0.0 · −0.0 이면 예전엔 끝난 런으로 건너뛰어 traceback 런이 parent_dead · 재실행 자격 → 이제 runner_rc · 다음 `--resume` = RESUME_NOT_ALLOWED · 읽기가 바뀐 값은 그 셋뿐.
- **A1b** — 끝 기록의 사슬 원인 칸도 두 길이 다르게 읽었다 (by chain = 모르는 원인 → 읽음 False · recover = chain_end 로 옮긴 같은 값 → 읽음 True) → 한 읽기 · ~~두 길 같은 답~~ 두 길 같은 재실행 자격 (★ 11-06 정정 · 사전 공격 10 회차 PB-05 — 원인 글은 로그 낱말에 따라 다를 수 있다: 모르는 원인 + 메모리 낱말 로그 = by chain parent_dead ↔ recover resource · 잘못된 주소 로그 = by chain parent_dead ↔ recover runner_rc · 둘 다 읽음 False).
- **PC6-05** — 요약 있는 길에서 멈춘 런 로그가 없거나 못 읽으면 "오류 낱말 없음" 으로 재실행이 열렸다 → 로그 = (글, 상태) · ok 아니면 자격 없음 (런을 띄우기 전 TIME_LIMIT 만 예외) · 한 번 연 fd 라 FIFO · 바꿔치기에 막히거나 속지 않는다.
- **A2b** — 있는데 못 읽는 단계 요약을 "요약 없음" 으로 읽던 것 → 원인 summary_unreadable · 자격 없음 · 단계 요약 = 원자적 쓰기 (바이트 = 예전과 같음).
- **RR2-02 · RR2-03 · Q7** — 문서만 (현행 계약 문장 · 등록 ⑫ 코드 한정어 그대로 + 시험 범위 · ⑦ = 숫자 봉인 뒤).

## 1. 항목마다

| 항목 | 고친 자리 | 시험 (`scripts/test_rint_r_chain.py`) | 고치기 전 → 뒤 |
|---|---|---|---|
| A1 RR2-01 | `rc_kind` (ok 정확한 정수 0 · fail 그 밖 정확한 정수 · none · bad = bool · 실수 0.0 · −0.0 포함 · 글 · 목록 · 객체) · `rc_success` · `runner_rc_failed` (옛 식과 같은 값) · 소비자 전부 (orphan_cause · Replay.run · noop_check · MergeFetch.run · Runner._execute · RunnerGraphSource._run · ResumeRunner._src_done · stop_cause · chain_end_failed · load_ladders = R_j,0 확인 팔 런 기록 rc 새로 읽음 · 성공 아니면 LADDER_SET) | RC01 원천 AST 전수 (판독 함수 밖 rc 읽기 0 · 소비자마다 판독 함수 · 스캐너 자기 시험 나쁜 꼴 12 · 좋은 꼴 7) · RC02 실제 git 원장 (rc 0 · false · 0.0 · −0.0 · "0" · null · 1 · true → recover → 결과 줄 → `--add --resume`) · RC03 런 기록 소비자 넷 (예측 실경로 셋) · RC04 러너 쪽 (run_in_group 실측 exit 0 · 3) · RC05 판독 표 16 값 | 0/5 → 5/5 (고치기 전 = 날 읽기 10 자리 · false · 0.0 · −0.0 = parent_dead · 자격 True · resume rc 0 = 판정문 표) |
| A1b | `CHAIN_END_CAUSES` (run_in_group 이 디스크에 쓰는 None · timeout · signal · exception + signal_after) · `chain_cause_known` · recover 가지 = chain_end 가 dict 아님 · 원인 모름 → 읽음 False (원인 글 그대로) | CE01 단위 27 행 · CE02 실경로 6 행 (실제 git 원장 · recover 가 chain_end 로 옮김 → 결과 줄 → `--add --resume`) · PE03u weird 행 기대 변경 (나머지 43 행 그대로) | 0/3 → 3/3 |
| A2 PC6-05 | `read_regular_file` (O_RDONLY \| O_NONBLOCK \| O_NOCTTY → 그 fd 의 fstat 일반 파일 검사 → 그 fd 에서 읽기) · `run_log_text` → (글, 상태 ok · no_run · missing · unreadable) · `stop_log_readable` (예외 = 멈춤 코드 TIME_LIMIT + 런 기록 없음 + 시작 기록 자리 lexists 아님 + 로그 없음) · result_fields 한 번 읽기 · orphan_cause 같은 읽기 | LG01 표 56 행 (멈춤 여덟 × 로그 여섯 · 시작 기록 자리 파일 · 폴더 · 끊긴 링크 · 요약 없는 길 다섯 · 권한 = uid 65534 자식) · LG02 실경로 (그룹 미확인 멈춤 → 로그 지움 · 폴더로 → recover → `--add --resume` rc 3) · LG03 포크 자식 8 행 (FIFO 둘 · 장치 · 요약 없는 · 있는 길 FIFO · is_file 뒤 · 연 뒤 바꿔치기 · 읽기 중 EIO) | 0/3 → 3/3 |
| A2b | `read_summary_state` · `read_summary` (객체 아닌 JSON = None) · `stage_summary_read` (하나라도 못 읽음 · status 글 칸 없음 = unreadable) · result_fields · attempt_result_line · result_recount · recover_ledger · `write_summary` = `write_json_atomic(_clean)` (사다리 · 예측 · 단위 · 점 · 합치기 둘) | SU01 18 행 (잘린 · 0xff · 객체 아님 셋 · {} · status 없음 · 빈 · 깊이 10 만 · 폴더 · FIFO · 둘째 이름 · 읽히는 + 못 읽는 · 실경로 셋) · SU02 (사다리 · 예측 · 합치기 요약 = write_json_atomic · 정상 런 바이트 = 옛 write_json · os.replace 실패 = 요약 없음 · 원천에 요약 이름 write_json 0) | 0/2 → 2/2 |
| A3 RR2-02 | `docs/reviews/rint2_rr_fix_evidence_20261023/q9_predict_units_design.md` §3-1 취소선 + 11-05 정정 · `docs/reviews/codex_rint2_rr_round2_request_20261103.md` · `docs/reviews/codex_rint2_rr_round1_request_20261024.md` = 본문 그대로 + 표지 · `docs/reviews/rint2_rr_fix_evidence_20261023/q9_time_budget.py` 낱말만 | 출력 바이트 대조 | 출력 = 고치기 전 = q9_time_budget.json |
| A4 RR2-03 | `docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md` ⑫ = 넓은 괄호 취소선 + `scripts/carbon_junction.py` CJUNC_QUALIFIERS 전달 길이 문장 인용 + Δ/λ 0.02 – 0.63 · q 0.4 – 19 + 축저항 몫 문장 + 임의 교차 · 비스듬한 접합 = 식 검증 아님 · `docs/reviews/rint_carbon_additive_design_v1_20261020.md` 표지 · 요청서 RINT2-L01 행 표지 | `docs/reviews/rint2_rr2_fix_evidence_20261105/verify_rr2_03_quote.py` · K01 · PC18 · PC20 · EP06 | ok · 4/4 |
| A5 Q7 | `docs/reviews/rint2_dev_probe_ledger_20261026.md` §5 한 줄 | — | — |

로그 (이 폴더 logs/) = before_A1_RC.log → after_A1_RC.log · before_A1b_CE.log → after_A1b_targeted.log · before_A2_LG.log → after_A2_targeted.log (행 보강 뒤 after_A2_LG_rows2.log) · before_A2b_SU.log → after_A2b_SU.log · 자르지 않은 행 판정 = *_rows*.json (`docs/reviews/rint2_rr2_fix_evidence_20261105/dump_rows.py` · 칸 chain_sha256 = 그 시험이 돈 판).

## 2. 회귀 (하나씩 차례로)

| 묶음 | 결과 |
|---|---|
| 사슬 (3.11) | 바탕 451/451 → A1 456 → A1b 458 → A2 461 → A2b 463 → 끝 463/463 (434.9 s · 문서 정정 뒤) |
| 끝-끝 `scripts/test_rint_r_chain_e2e.py` (한 번) | 51 PASS · 0 FAIL (840.6 s) |
| kgy 판 3.8.20 (`scripts/check_kgy_py38.sh`) | 11 묶음 통과 (사슬 463/463 · 끝-끝 51 PASS · 0 FAIL · logs/py38/) |
| check_doc_refs · check_review_findings | 깨진 참조 0 · rc 0 |

## 3. 변이 (`docs/reviews/rint2_rr2_fix_evidence_20261105/mutate_rr2fix.py`)

- 리포 밖 git 없는 사본 · 한 번에 하나 · 매번 원 바이트 · 끝 sha256 = 시작 · 기준선 묶음 여덟 통과.
- **40 중 40 잡힘 · 모두 기대한 검사 FAIL** (logs/mutation_rr2fix.json) — A1 11 · A1b 5 · A2 12 · A2b 12 (목록 = 스크립트 머리 표).
- 변이로 보강한 시험 = 런 기록 없는 GROUP_UNCONFIRMED 행 · 읽기 중 EIO 행 (A2 커밋 안) · 예측 · 합치기 쓰기 · 원천 대조 (SU02 · A2b 커밋 안).

## 4. Codex 탐침 무변경 다시 (`docs/reviews/rint2_rr2_fix_evidence_20261105/rerun_codex_probe.py`)

- 탐침 원본 그대로 (sha256 = 반입 기록 값) · received/repo = 고친 판 · 리포 밖 · `python3 -I -B`.
- **310 / 311** (Codex 311 / 311) · 다른 행 = known_PC6_05_summary_missing_log_resume 하나 (열린 PC6-05 를 박은 행 · 우리 = False = 고친 결과).
- candidate_fix_results.json = Codex 와 같음 · residual_rc.json fields = 후보 고침 표 6/6 · integration = false · 0.0 이 정수 1 행과 같음 (runner_rc · 자격 False · RESUME_NOT_ALLOWED) · 산출 = codex_probe_rerun/.

## 5. 한정 · 범위가 바뀐 것

- 고치지 않음 (1저자 결정 = 한정만): 봉인 원천 런 (G01_&lt;런&gt;_a&lt;i&gt;) 도중 사슬이 받은 신호 = runner_rc · 이 폴더 로그 없음 (안전 쪽 · 재실행 없음) — `stop_log_readable` 설명.
- 범위 바뀜 ~~(모두 보수 쪽)~~: load_ladders 가 rc 를 새로 읽음 · PE03u weird 행 기대 변경 · 요약 없는 길 그룹 이름 RUN_DIR_RE 밖 = 읽음 False · 못 읽는 요약 = 목록 꼴 + 깊은 중첩 · {} · status 없는 객체 · FIFO 요약의 recover = 결과 줄 없음 · rc 3 (막힘 없음) · 원자적 쓰기 = 단계 요약 넷 + 합치기 둘 · 권한 행 = 실제 EACCES · RC01 의 허용 = 지시 목록 + 조건식 두 갈래를 지난 기록 칸 대입 · 생산자 run_in_group 의 return.
  - ★ 11-06 정정 (사전 공격 10 회차 PB-02) — "모두 보수 쪽" 은 **거짓**이었다.  A2b 의 `read_summary` (객체 아닌 JSON = None) 가 ① 판정 입력 (`_verdict_compute`) 의 "단계 요약 하나" 검사를 느슨하게 했다 — 예측 요약 + `ladder_summary.json` = `[]` · `0` · `true` 인 폴더가 옛 판 Stop INPUT_NOT_STAGE (요약 2 개) → 이 판 통과 (실경로: 주 예측 폴더 사본 + `[]` 의 판정 = rc 0) ② 합치기의 남은 런 목록 (`MergeFetch.unused_runs`) = 옛 판 예외 → 이 판 조용히 건너뜀 (보고만).  고침 = PB-02 (둘 다 `read_summary_state` · 있는데 못 읽는 요약 = 판정 입력 Stop INPUT_NOT_STAGE · 남은 런 목록 Stop UNIT_PROVENANCE_MISMATCH → 합치기 STOPPED · 잘린 JSON · `{}` 단위 요약도 이제 멈춤 = 옛보다 엄격) · 증거 `docs/reviews/rint2_rr2_fix_evidence_20261105/preattack10_fix/`.  RC01 의 허용 (위 줄 끝) = PB-04 뒤 허용 문맥 목록 방식 (모르는 문맥 = 실패) 으로 바뀜.
- 남은 한정: 단계 요약 칸 꼴 (stop 이 객체 아님 등) = 옛 그대로 예외 (재실행이 열리지는 않음) · 시험 = 합성 · 가짜 러너 · 실제 git 원장 · 이 컨테이너 — 실제 SIGKILL · flock 경쟁 · kgy 3.8.10 · hidepid · GPU 아님 (판정문 §9 현장 자격 별도) · 바탕 끝-끝 한 번 = A1 편집과 겹쳐 증거로 안 씀.
- 원장 · 요청서 머리 · 진행 기록 · CLAUDE.md = 메인 세션 몫.

## 6. 파일

dump_rows.py · mutate_rr2fix.py · rerun_codex_probe.py · verify_rr2_03_quote.py · logs/ · codex_probe_rerun/ · preattack9/ · SHA256SUMS (이 폴더에서 sha256sum -c SHA256SUMS · 메인 세션이 이 보고와 preattack9/ 를 넣은 뒤 다시 만듦 · SHA256SUMS 자신은 빠짐).

## 7. 사전 공격 9 회차 (11-05 · 독립 · diff 만) 발견 ↔ 이 판 (메인 세션 11-06 대조)

11-05 의 사전 공격 9 회차는 잃은 판 (회차 ② 고침 첫 판) 을 공격해 발견 여덟을 냈다.  1저자 11-05 *"권고대로"* = PA-01 – 07 고침 (시험 먼저) · PA-08 = 한정만.  보고 원문 = `docs/reviews/rint2_rr2_fix_evidence_20261105/preattack9/PREATTACK_RR2_report.md` (대화 기록에서 글 그대로 복구 · 판 번호 · 줄 번호 = 잃은 판 기준).  이 판에서 각 발견이 놓인 자리:

| 발견 | 등급 | 이 판 |
|---|---|---|
| PA-01 끝 기록 cause 칸 두 읽기 | P2 | A1b (`chain_cause_known` · CE01 · CE02) |
| PA-02 load_ladders 가 R_j,0 확인 런 rc 안 읽음 | P3 | A1 (load_ladders 가 `rc_success` 로 읽음 · 아니면 LADDER_SET) |
| PA-03 못 읽는 단계 요약 = 없음 · 원자적 쓰기 아님 | P3 | A2b (`read_summary_state` · `write_summary` · SU01 · SU02) |
| PA-04 run_log_text 검사 ↔ 읽기 경합 (FIFO) | P3 | A2 (`read_regular_file` · LG03) |
| PA-05 RC01 훑기가 좁음 | P3 | A1 RC01 (원천 AST 전수 · 스캐너 자기 시험 나쁜 꼴 12 · 좋은 꼴 7) |
| PA-06 회차 ① 요청서 표지 없는 사본 | P3 | A3 (`docs/reviews/codex_rint2_rr_round1_request_20261024.md` 표지) |
| PA-07 RINT2-L01 넓은 한정어 | P3 | A4 (회차 ② 요청서 RINT2-L01 행 표지) · 원장 RINT2-L01 메모 = 메인 세션 다음 커밋 |
| PA-08 그래프 원천 런 중 신호 = 오분류 (안전 쪽) | P3 | 고치지 않음 · `stop_log_readable` 설명에 한정 |

⚠ 11-05 의 탐침 · 로그 (scratch pa2/) 는 기계 교체로 잃었다 — 이 판의 시험 (RC · CE · LG · SU 표) · 변이 40/40 · Codex 탐침 다시 310/311 이 그 자리를 대신한다.  사전 공격 10 회차 (독립) = 이 판 대상 · 다음.

## 8. 사전 공격 10 회차 (11-06 · 독립 · diff 만) 발견 ↔ 고침 (★ 11-06 덧붙임)

보고 원문 = `docs/reviews/rint2_rr2_fix_evidence_20261105/preattack10/PREATTACK10_report.md` (탐침 · 산출물 같은 폴더) · 1저자 11-06 = PB-01 (P2) · PB-02 · 03 · 04 · 06 (P3 코드) 고침 (시험 먼저) · PB-05 · 07 = 문구만.  고침 증거 = `docs/reviews/rint2_rr2_fix_evidence_20261105/preattack10_fix/` (`logs/` = 고치기 전 · 뒤 · 행 판정 · 변이 · 회귀 · 코드 sha256 · `codex_probe_rerun/` · `reviewer_probe_rerun/` · `new_findings/` · `SHA256SUMS`) · 고침 보고 글 = 작업 트리 에이전트의 마지막 보고 (그 폴더에 보고 파일 쓰기가 거부됨 → 메인 세션이 옮긴다).

| 발견 | 등급 | 처분 |
|---|---|---|
| PB-01 rc null 을 소비자마다 반대로 읽음 (chain_end_failed · GROUP_UNCONFIRMED) | P2 | 고침 (RN01 · RN02 · 기대 변경 RC04 · PE03u · LG01 · PD13 · PD13o) |
| PB-02 판정 입력 · 합치기 남은 런 목록의 못 읽는 요약 | P3 | 고침 (SU03 · SU04) · 위 §5 정정 |
| PB-03 그룹 기록 · attempt.json · rejected.json 읽기가 FIFO 에 막힘 | P3 | 고침 (FF01) |
| PB-04 RC01 스캐너 빈틈 (반례 17 중 16) | P3 | 고침 (허용 문맥 목록 · RC_SCAN_BAD 34 · GOOD 11) |
| PB-05 A1b "두 길 같은 답" | P3 문구 | 위 §0 정정 · 코드 주석 · CE01 · CE02 제목 |
| PB-06 런 전 TIME_LIMIT 예외 = 시작 기록 자리만 | P3 | 고침 (LG01 흔적 행 일곱) |
| PB-07 f5b00a838 커밋 메시지 A1b 줄 "CE01 · CE02 0/3 → 3/3" | P3 문구 | 셋째 = **PE03u** (`logs/before_A1b_CE.log` = FAILED [PE03u, CE01, CE02] · 위 §1 A1b 줄은 이미 PE03u 를 적었다) · 커밋은 push 됨 = 역사 안 고침 · 이 줄이 정정 |

- 이 폴더의 `SHA256SUMS` = 11-06 다시 만듦 (이 보고 정정 · preattack10/ · preattack10_fix/ 포함 · 이름이 SHA256SUMS 인 파일은 빠짐 · preattack10_fix/ 에는 자기 SHA256SUMS 도 있다).
