# Rint ② 사전 공격 10 회차 고침 — PB-01 (P2) · PB-02 · 03 · 04 · 06 (P3 코드) · PB-05 · 07 (문구) (11-06 · 작업 트리 에이전트 · 1저자 11-06 "권고대로")

- 근거 = `docs/reviews/rint2_rr2_fix_evidence_20261105/preattack10/PREATTACK10_report.md` (독립 · diff 만 · 대상 f5b00a838) · 탐침 · 산출물 = 같은 폴더 (리뷰어 커밋 69a08d094 반입 → fb1dd7a7b · 보고 파일만 더함).
- 바탕 = f5b00a838 · 그 위 항목마다 한 커밋 · push 없음 · 원장 findings.json · CLAUDE.md · check_all.sh · 진행 기록 무변경 · ibb · kgy · 웹앱 실행 없음.
- 차례 = 시험 먼저 (고치기 전 코드에서 옳은 까닭으로 실패 = logs/before_*) → 고침 → 통과 (logs/after_*) → 가까운 묶음 → 커밋 · 시험한 코드 sha256 = logs/code_sha256.txt.
- 환경 = Linux 6.18 · Python 3.11.18 · numpy 2.4.6 · scipy 1.17.1 · kgy 판 = uv CPython 3.8.20 · numpy 1.24.4 · scipy 1.10.1 · 4 코어 · root.

## 0. 쉽게 말하면
- PB-01 — 러너가 스스로 끝났다고 적힌 자리 (끝 기록 원인 None · 런 기록 group_cause None) 인데 rc null 인 꼴 (생산자가 만들지 않는다) 을 by chain 길은 runner_rc, recover 가 chain_end 로 옮긴 뒤 · 요약 있는 길 GROUP_UNCONFIRMED 는 재실행 자격으로 읽었다 → 그 자리 = 정확한 정수 0 만 성공 · rc null 이 실패 아님 = 사슬이 죽인 런 (group_cause timeout · signal · signal_after) 뿐 · GROUP_UNCONFIRMED 런 기록 없음 · 칸 없음 · 모르는 값 = 읽음 False.  실경로 두 꼴 = --add --resume rc 3 (옛 rc 0).
- PB-02 — 판정 입력 · 합치기 남은 런 목록이 있는데 못 읽는 요약을 없음으로 읽었다 → Stop INPUT_NOT_STAGE · Stop UNIT_PROVENANCE_MISMATCH (합치기 STOPPED).
- PB-03 — 그룹 기록 · attempt.json FIFO = 막힘 · rejected.json = is_file 뒤 바꿔치기 창 → 넷 다 read_regular_file.
- PB-04 — RC01 스캐너가 반례 17 중 16 을 놓쳤다 → 'rc' 자리 전수 ↔ 허용 문맥 목록.
- PB-06 — 런 전 TIME_LIMIT 예외가 시작 기록 자리만 보았다 → 끝 기록 · 로그 자리 · 런 폴더 흔적도 없을 때만.
- PB-05 · 07 — 문구.

## 1. 항목마다
| 항목 | 커밋 | 고친 자리 | 시험 | 고치기 전 → 뒤 |
|---|---|---|---|---|
| PB-01 | 858ac9679 | chain_end_failed = 원인 None + not rc_success · stop_cause GROUP_UNCONFIRMED = group_cause 칸 있음 · None + 정수 0 아님 = 낱말 · 기본 runner_rc · 새 stop_record_readable · RUN_KILLED_CAUSES · result_fields 읽음 = 로그 ∧ 런 기록 꼴 | 새 RN01 (단위 112 행) · RN02 (실제 git 원장 10 행) · 허용을 박은 기대 다섯 변경 (RC04 · PE03u none_rcNone · LG01 norecord_GROUP_UNCONFIRMED · PD13 (None, None) → 실패 줄 · PD13o ce_none_rc) | 3/10 → 10/10 · 118/118 |
| PB-02 | 2861a1dad | _verdict_compute = read_summary_state · 못 읽음 = Stop INPUT_NOT_STAGE · MergeFetch.unused_runs = 못 읽음 · status 글 칸 없음 = Stop UNIT_PROVENANCE_MISMATCH | 새 SU03 (15 행 · FIFO 자식 · 실경로 판정 rc 3) · SU04 (15 행 · FIFO 자식 · 실경로 UMA 합치기 → rc 3 STOPPED) | 0/2 → 2/2 · 72/72 |
| PB-03 | 3b2b3628c | _read_group_json · read_attempt = read_regular_file · rejected.json 두 자리 = is_file 거름 그대로 + 확인 뒤 못 읽음 = Stop ATTEMPT_LEDGER_MISMATCH | 새 FF01 (포크한 자식 · 15 s · 9 행) | 0/1 (8 행 시간 초과) → 1/1 · 121/121 |
| PB-04 | bef02546e | (시험 가드) | rc_scan 허용 문맥 방식 · RC_SCAN_BAD 12 → 34 · GOOD 7 → 11 · 원천 허용 문맥별 자리 수 보고 | RC01 FAIL (놓친 꼴 21 · 그 판 e31def83… 다시 만들어 같은 결과) → PASS (34/34 · 오탐 0 · 원천 0 · 자리 37) · 3.8 = 33/33 (match 꼴 건너뜀) |
| PB-06 | 4329b6c80 | stop_log_readable 예외 = 런 기록 없음 + 시작 · 끝 기록 · 로그 자리 lexists 아님 + 런 폴더 흔적 (<런> · <런>_arm…) 없음 | LG01 런 전 행 일곱 · LG 합성 폴더 표지 = 앞 런 폴더 (LG_MARK) | LG01 FAIL (흔적 행 여섯) → LG 3/3 + SU01 · 154/154 |
| PB-05 | 74ab3b45c | 주석 · 독스트링 · 모듈 머리 이력 | CE01 · CE02 제목 | 동작 무변경 · 4/4 |
| PB-07 · 정정 | 8147c5928 | — | — | 바깥 REPORT §5 "모두 보수 쪽" = 거짓 정정 · §8 표 |

## 2. 회귀
- 사슬 3.11 468/468 (396.1 s) · 끝-끝 51 PASS · 0 FAIL (772.0 s) · kgy 판 3.8.20 11 묶음 (사슬 468/468 · 끝-끝 51/0 · run_contract 124/124 · step3_rint · ptfe 242 · carbon_junction 500 · ca_ext_b6 502 · ca_ext_runner 151 · target_cert 264 · conv_cert 29 · s0_census 167) · check_doc_refs 깨진 참조 0 · check_review_findings rc 0 · --ban-sweep 누수 없음.

## 3. 변이 (mutate_pa10fix.py)
- 리포 밖 git 없는 사본 · 한 번에 하나 · 매번 원 바이트 · 되돌림 True · 28/28 잡힘 · 모두 기대한 검사 FAIL (PB-01 B1–B8 · PB-02 C1–C3 · PB-03 D1–D4 · PB-04 E1–E9 · 원천 반례 둘 포함 · PB-06 F1–F4).

## 4. Codex 탐침 무변경 다시
- 310/311 · 다른 행 = known_PC6_05 하나 (옛 고침) · 이전 다시 돌리기 기록과 tested_sha256 칸만 다름 = 새 행 차이 0 (codex_probe_rerun/).

## 5. 리뷰어 탐침 다시 (reviewer_probe_rerun/)
- probe_ledger: ⓐ ⓑ rc 0 → 3 · 대조 넷 같음.
- probe_units: 57 행 중 9 다름 — R2 · G2 = runner_rc · False · T4 = False · T1 = True → False (첫 결과 표지가 멈춘 런 자신의 폴더 = PB-06 이 흔적으로 봄 · 생산자가 만들지 않는 꼴) · V1–V4 = INPUT_NOT_STAGE · V0 = 경로 글만.
- probe_units2: F1–F4 막히지 않음 · G5 · G6 = False · S1–S3 예외 그대로.  probe_rcscan: 17/17 · 5/5 · 원천 0.

## 6. 범위 바뀜 · 남은 한정
- PB-01: GROUP_UNCONFIRMED 런 기록 없음 · 칸 없음 · 모르는 값 = 원인 글 그대로 · 읽음 False · 기존 시험 다섯 기대 변경.
- PB-02 (fail-closed): 잘린 JSON (옛 = 무시) 도 판정 입력 멈춤 · 사본 시도 (채택 아닌 것 포함) 단위 요약 못 읽음 · {} · status 없음 = 합치기 STOPPED · 요약 없음 = 건너뜀 그대로 · 그 밖 read_summary 자리 = 이미 멈추거나 판정 입구가 닫음 (보고 env 는 보고만).
- PB-03: 처음부터 FIFO · 폴더인 rejected.json = is_file 이 거름 (옛 그대로) · al07_foreign_ok · folder_digest 의 is_file → 읽기 = 바꿔치기 경합만 · 범위 밖.
- PB-04: 'rc' 낱말 없는 읽기는 못 봄.
- PB-06: 로그 자리 끊긴 링크 = 지시 두 조건에 더한 같은 부류.
- 그대로 둔 다름 (보수 쪽 · 옛부터): 원인 None + rc 0 + 잘못된 주소 · CUDA 낱말 로그 = by chain 끝난 런 (자격) ↔ recover chain_end 낱말 runner_rc.
- 옛 한정 그대로: 요약 칸 꼴 틀림 예외 · R8 · _src_done · PA-08 · 실제 SIGKILL · flock · 비 root /proc · hidepid · GPU · NFS/FUSE · kgy 3.8.10 아님.

## 7. 새로 본 것 (고치지 않음 · new_findings/ · 바탕에도 같음 · 단위 관찰만)
| 이름 | 등급 (제안) | 무엇 | 권고 |
|---|---|---|---|
| N1 | P2 후보 | 런 기록 {group_cause None · rc 1} + Traceback 에서 멈춤 코드 한 칸 RUNNER_RC → TIME_LIMIT = timeout · 자격 True (생산자 TIME_LIMIT 런 기록 = group_cause timeout · rc null) | 멈춤 코드와 무관하게 group_cause None ⇒ 정확한 정수 0 만 성공 · TIME_LIMIT + group_cause ≠ timeout = 읽음 False |
| N2 | P2 후보 | 같은 꼴에서 group_cause 한 칸 None → timeout · signal (rc 1) = 자격 True (생산자 = group_cause 있으면 rc null · RUNNER_RC + timeout 없음) | 사슬이 죽인 원인 + rc 있음 = 모순 = runner_rc 또는 읽음 False |
| N4 | P3 | recover_ledger 의 객체 아닌 rejected.json = AttributeError (잡지 않음) | result_recount 와 같은 isinstance 검사 |
- 구별 불가 (발견 아님): 요약 없는 by chain 끝 기록 원인 None → timeout · signal (rc 1) = 생산자 경합 꼴과 같다.

## 8. PB-07
- f5b00a838 커밋 메시지 A1b 줄 "CE01 · CE02 0/3 → 3/3" 의 셋째 = PE03u (logs/before_A1b_CE.log = FAILED [PE03u, CE01, CE02]) · push 된 커밋이라 역사를 고치지 않고 여기 · 바깥 REPORT §8 에 적는다.

## 9. 파일
logs/ (before_* · after_* · *_rows*.json · final_* · py38/ · check_* · mutation_pa10fix.* · code_sha256.txt · environment.txt) · mutate_pa10fix.py · make_sums.py · codex_probe_rerun/ · reviewer_probe_rerun/ · new_findings/ · SHA256SUMS — 이 REPORT.md 를 넣은 뒤 이 폴더와 바깥 폴더의 SHA256SUMS 를 make_sums.py 로 다시 만든다.
