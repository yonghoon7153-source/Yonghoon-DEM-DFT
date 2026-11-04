# Rint ② 사전 공격 8 회차 고침 — PC8-01 … 09 (11-04 · 작업 트리 에이전트 · 1저자 11-04 *"다 권고대로"*)

보고 (읽기만 · 반입 = 바이트 그대로) `docs/reviews/rint2_rr_fix_evidence_20261023/preattack8/PREATTACK_8.md` · 원장 PC8-0N = 보고 P8-0N (`docs/reviews/findings.json`) ·
요청서 자리 = `docs/reviews/codex_rint2_rr_round2_request_20261103.md` §0 ⑪ · §2 · §4 · §5-5 · §8-1 · §8-2 · §9 · Q1.

- 커밋 = 작업 트리 가지 `pc8-fix-1104b` (기준 = 본 가지 `74150affc` · 그 사슬 · 접합 코드 = 리뷰 대상 끝 `7b51e591e` 와 같음) · 본 가지 번호 = 반입 때.
  차례 = 시험 먼저 (고치기 전 코드에서 옳은 까닭으로 실패) → 시험 결함 고침 (PD12u 상태 만들기 · 기대 그대로) → 고침 → 사전 공격 8 회차 반입 → 변이 보강 시험 (PD12u 증거 칸 줄 넷 · 코드 변경 없음) → 원장 · 증거 · 요청서 (커밋 번호 = §6 끝).
  고치기 전 코드 세 파일 sha256 (`logs/before_code_sha256.txt`) = `74150affc` 의 같은 파일 (3/3 · `git show` 로 셈) · 그 일곱 파일 = `7b51e591e` 와 차이 없음 (`git diff`).
- 시험한 코드 sha256 = `logs/tested_code_sha256.txt` (고친 판 일곱) · 고치기 전 코드 = `logs/before_code_sha256.txt` (사슬 · 접합 · 증거 계약 셋).
- 로그 머리의 커밋 칸 = 작업 트리 가지 번호 (반입 뒤 바뀐다 · 시험한 코드 = 위 sha256 · `SELF-116` 꼴).
- 환경 = Python 3.11.15 · numpy 2.4.6 · scipy 1.17.1 (기본) · kgy 판 = uv CPython 3.8.20 · numpy 1.24.4 · scipy 1.10.1 · BLAS 스레드 1 · 한 컨테이너 (4 코어).

## 1. finding 마다

| 원장 (보고) | 고친 자리 (`scripts/rint_r_chain.py` 등) | 시험 (새 · 바뀐) | 고치기 전 → 뒤 | 탐침 무변경 다시 |
|---|---|---|---|---|
| PC8-05 (P8-05 · P1 후보) | 시작 기록 새 판 = 칸 여섯 + `chain_pid` · `chain_start` (`START_KEYS` · 옛 판 `START_KEYS_V1` 읽기 그대로 · `_start_problem`) · `attempt_open` 이 사슬 pid · 시작 틱을 씀 · `host_seen` (그룹 · 시작 기록 한 함수) · `start_chain_problem` · `recover_ledger(…, operator)` 결과 줄 전 대조 · `stage_recover` 운영자 표지 쓰임 수 · `--operator-confirm` 도움말 | PE05 (첫 러너 전) · PE05b (런 사이) · PE05o (죽음 · 삶 · pid 다시 쓰임 · 시작 틱 null · 다른 부팅 + 운영자 · 옛 판 + 운영자 · 표지 범위) · PE05p (원장 해석) · PE01 (시작 기록 칸) | 실패 (`logs/before_chain.log` · 범위 줄 = `logs/before_PE05o_PE06_full.json`) → 통과 (`logs/after_chain_targeted.log` · `logs/after_PE05o_PE06_rows2.log`) | `logs/probes/probe_p805*.out` — recover rc 3 · 결과 줄 없음 · 다음 --add · --resume rc 3 · 원 사슬 CALIBRATED + 자기 결과 줄 |
| PC8-02 (P8-02 · P2) | `group_pair` (표지 32 hex · 끝 기록 표지 = 시작 기록 · 이름 = 시작 기록 = 파일 이름) 를 `attempt_groups_problem` · `orphan_cause` · `stage_recover` · `recover_group` · `ResumeRunner._src_done` (rc = 정수 0) 이 씀 · `_read_group_json` (RecursionError 포함) | PE06 (확인 True · False 다른 끝 기록 실경로 · `_src_done` 다섯 꼴 · `attempt_groups_problem` 셋 · recover_group chain_end 없는 다른 끝 기록) | 실패 → 통과 (같은 로그) | `logs/probes/probe_p802_foreign_confirmed_end.out` — recover rc 3 · 결과 줄 없음 · 러너 그룹 정리됨 |
| PC8-01 (P8-01 · P2) | `al07_foreign_ok` (결과 줄 rejected · OUTDIR_NOT_EMPTY · 폴더 = 옆 기록 · 요약 sha · 거부 기록 꼴 `REJECTED_KEYS` · n · 시작 커밋 40 hex · 남의 폴더 `attempt_chain_trace` 없음) | PE02y (P8-01 탐침 꼴 실경로 셋 · 판정 · 예측 입력) · PD12u (바뀐 설계 단언 · 새 사유 줄 11 + 증거 칸 하나씩 줄 넷 `355c1b6d0`) | 실패 (`logs/before_chain.log` · `logs/before_PD12u.log` · 줄 넷 = `logs/before_PD12u_rows2_full.json` — 셋 실패 · status 줄 = 옛 규칙도 사유) → 통과 (`logs/after_chain_targeted.log` · 줄 넷 뒤 = `logs/py311_r2/` · `logs/mut/BASE2_al07.log`) | `logs/probes/probe_p801_al07_exception.out` — 우회 꼴 0 |
| PC8-03 (P8-03 · P3) | `json_same` (형 엄격 · 되풀이 없이 · 겹친 칸 사본) · `_json_pairs` · `_json_top_keys_differ` · `_grade_differ` · `reverify_report` 네 칸 · `reverify` 화면 공개 칸 | RV07 (형 바뀜 넷 · 겹친 칸 둘) · RV08 (실경로 · 결과 bool → 정수 · 판정 sentence_allowed false → 0 · 겹친 칸) | 실패 → 통과 | `logs/probes/probe_p803_byte_diff.out` · `probe_p803b_reverify_type.out` |
| PC8-04 (P8-04 · P3) | `byte_diff_view` = value 뒤에도 모음 (`_json_order_differs` · `_json_numform_differs` · 저장본 자기 값 정규 꼴 대조) | RV07 (value + 끝 줄바꿈 · value + 칸 순서 + CRLF) · 끝-끝 E18i 새 기대 [value, newline] | 실패 (`logs/before_e2e_E18.log` 10 PASS · 1 FAIL) → 통과 | 위 p803 |
| PC8-09 (P8-09 · P3) | `_json_pairs` 못 읽음 표지 (RecursionError) · `byte_diff_view` unreadable · `reverify_report` 못 읽음 = 다름 · `reverify` 판정 JSON 깊음 · 객체 아님 = 사유 한 줄 | RV07 (깊이 20 만 배열 · 객체) · RV09 (실경로 결과 깊음 · 판정 깊음 · 판정 []) | 실패 (RecursionError · AttributeError) → 통과 | p803 deep_nesting = 예외 없음 |
| PC8-06 (P8-06 · P3 · 시험만) | 코드 변경 없음 | RV07 numform_order (M26) · BAN8 ⑨ (B01 · 간선 기하 점 = 칸 가운데) | 고치기 전 코드에서 M26 · B01 잡힘 (`logs/kill_before_m26_b01.json` · `logs/before_RV07_rows_base.json` ↔ `logs/before_RV07_rows_M26.json`) | — |
| PC8-07 (P8-07 · P3 · 문구) | `scripts/carbon_junction.py` `CJUNC_QUALIFIERS` 넷째 줄 = 같은 두 곧은 나란한 레일만 · `scripts/ca_ext_cjunc.py` 계약 주석 (대조 코드 그대로 = producer 상수) | BAN8 ⑩ · `scripts/test_ca_ext_b6.py` R7 "한정어 = 11-03 판" (거부) | BAN8 33/34 → 34/34 (`logs/before_cj_ban8.log` → `logs/after_cj_ban8.log`) · b6 R 104/1 → 105/0 (`logs/before_b6_R.log` → `logs/after_b6_R.log`) | — |
| PC8-08 (P8-08 · P3 · 문구) | `byte_diff_view` docstring · `BYTE_DIFF_KINDS` 주석 (두 수 = 봉인 바이트에서 나온 수) | — (동작 그대로) | — | `logs/probes/probe_p808_offset.out` = 같은 수 8 · 4 · 0 |

## 2. 회귀 (하나씩 차례로 · `run_regression.sh`)

| 묶음 | Python 3.11.15 (`563b4019a` 판 · 사슬만 `355c1b6d0` 판 다시) | kgy 판 3.8.20 (`355c1b6d0` 판) |
|---|---|---|
| `scripts/test_rint_r_chain.py` | 451/451 PASS (459.9 s) · 다시 451/451 PASS (444.5 s · PD12u 줄 넷 뒤 · `logs/py311_r2/`) | ⬜ |
| `scripts/test_rint_r_chain_e2e.py` | 51 PASS · 0 FAIL (838.2 s) | ⬜ |
| `scripts/test_carbon_junction.py` | 500/500 PASS | ⬜ |
| `scripts/test_ca_ext_b6.py` | 502 PASS · 0 FAIL | ⬜ |
| `scripts/test_ca_ext_runner.py` | 151 PASS · 0 FAIL | ⬜ |
| `scripts/test_ca_ext_z3.py` | 84 PASS · 0 FAIL (24.0 s) | ⬜ |
| `scripts/test_step3_target_cert.py` | 264/264 PASS (빠른 판 · 13.1 s) | ⬜ |

로그 = `logs/py311/` · `logs/py311_r2/` · `logs/py38/` · 한 줄 요약 = `logs/regression_env.txt` (줄마다 판 · rc · 초 · 끝 줄).
`563b4019a` → `355c1b6d0` 사이에 바뀐 시험 · 코드 파일 = `scripts/test_rint_r_chain.py` 하나 (`7141ac593` = 보고 반입 · 문서만) — 그래서 py311 의 사슬 밖 여섯 묶음 = `355c1b6d0` 판과 같은 파일.
명령 = `bash docs/reviews/rint2_rr_fix_evidence_20261023/pc8_fix/run_regression.sh <작업 트리> <로그 폴더> <HEAD> py311` · 사슬만 다시 = 앞에 `SUITES=test_rint_r_chain SUFFIX=_r2` · kgy 판 = 끝 인자 `py38` (`PATH` 앞에 uv CPython 3.8.20 · 하나씩 차례로 · 묶음 사이 동시 실행 없음).

## 3. 변이

- 새 가드 (`mutate_pc8fix.py` · 고친 트리 사본 · git 없음 · 한 번에 하나 · 끝나면 원 바이트 · 끝난 뒤 사본의 코드 · 시험 일곱 sha256 = 작업 트리와 같음) = **47 중 46 잡힘** · 생존 1 = A10 (옆 거부 기록 링크 검사를 지워도 `folder_digest` 가 링크를 None 으로 돌려 요약 sha 대조에서 거부 = 같은 뜻 · 두 겹 가드) (`logs/mutation_pc8fix.json` = 이름마다 마지막 판 · `logs/mutation_pc8fix.out` = 두 판 차례로).
  첫 판 43 (N01–N03 · N05–N11 · B1–B9 · A1–A11 · J1–J11 · B01 · Q1 · N04 = 번호만 빔 · 만든 변이 없음) = 42 잡힘 · A10 생존 → 첫 판에 없던 증거 칸 하나씩 지운 변이 넷 (A12 결과 줄 status · A13 거부 기록 schema · A14 칸 수 · A15 시작 커밋) + PD12u 에 그 칸 하나씩 어긴 줄 넷 (`355c1b6d0` · 시험만 · 코드 변경 없음) → A1–A15 다시 = 14 잡힘 · A10 생존 (같은 뜻).
  새 PD12u 줄 넷 · 고치기 전 코드 = 셋 (schema · 칸 · 시작 커밋) 이 None (옛 예외가 받음 = 시험 먼저 실패) · 넷째 (status stopped) 는 옛 규칙 ("결과 줄 stopped 인데 옆 거부 기록 있음 = 사유") 으로도 사유 (`logs/before_PD12u_rows2_full.json` · 실패 줄만 싣는 꼴 = 그 줄 없음).
  사본 기준선 (변이 없음) = 첫 판 사슬 27/27 · BAN8 34/34 · b6 R 104 PASS · 1 FAIL (R10 = 커밋된 영수증을 git 이력에서 읽음 · 사본 트리 = git 없음 · 작업 트리에서는 105/0) (`logs/mut/BASE_*.log`) · 둘째 판 (PD12u 줄 넷 뒤) AL07 · AL07b · PD12u · PE02 · PE02x · PE02y 6/6 PASS (`logs/mut/BASE2_al07.log`).
- 사전 공격 8 회차 `mutate8.py` 무변경 다시 (같은 사본 · 첫 판 시험 파일) = **35 중 적용 27 = 27 잡힘** · SKIP 8 = 고친 줄이 바뀌어 옛 글 없음 (M12 · M13 · M14 · M17 · M18 · M20 · M26 · M27) · 보고에서 생존이던 B01 = 잡힘 (BAN8 28/34 · 실패 여섯 = 새 가드 판 B01 의 ⑨ 여섯과 같은 수 · mutate8 은 묶음 이름만 적는다) · M26 = SKIP (자리 바뀜 → 아래 J5) · E01 · E02 (보고에 결과 기록 없음) = 이번에 돎 · 잡힘 (E01 = E18i · E18j · E02 = E18j · 끝-끝 각 ≈ 380 s) (`logs/mutate8_rerun.json` · `logs/mutate8_rerun.out`).
  SKIP 자리의 같은 뜻 변이 (고친 줄 · 위 47 안 · 모두 잡힘) — M12 ≈ A11 (예외 검사 건너뜀) · M13 (옆 기록 조건 지움) ≈ 옆 기록 증거 칸 하나씩 지운 A2 · A3 · A4 · A5 · A13 · A14 · A15 · M14 (status 조건 지움) ≈ A12 · M17 ≈ B9 · M18 (이름 대조 지움) ≈ B2 · M20 ≈ J4 · M26 ≈ J5 · M27 ≈ J3 · 옛 예외 조건 그대로 되돌림 = A1 (잡힘).  M13 · M14 자체 = 옛 줄이 없어 안 돌림 (짝 = 이 대응뿐).
- 생존이던 M26 · B01 ↔ 새 시험 (고치기 전 코드) = `kill_before.py` · 위 §1 PC8-06 줄.

## 4. 사전 공격 8 회차 탐침 무변경 다시 (`logs/probes/` · 고친 트리 사본)

P8-05 a · b · c · d · P8-01 · P8-02 · P8-03 · P8-03b · P8-08 · PC7 닫힘 탐침 · 시작 기록 해석 — 열한 개 rc 0 (`logs/probes/_index.txt`) · 결과 = 위 §1 마지막 칸 · PC7 닫힘 탐침 A 의 원장 clone 줄 (`c_stale_clone_other_out` = CALIBRATED) = 그대로 (PC7-01 범위 · Q-D · 이 고침 밖) · 시작 기록 해석 = 보고와 같은 답 (옛 판 칸 여섯 기준 줄 = 받음).

## 5. 닫지 않는 것 · 한정

- 원장 clone (그림자 원장) — 시작 기록이 없는 clone 에서 같은 대상을 다시 돌리는 손 = 이 대조 밖 (PC7-01 범위 그대로 · Q-D).
- 옛 판 시작 기록 (11-02 PC7-01 · 사슬 칸 없음) 의 recover = 운영자 확인 표지 뒤만 (결정 = 1저자 11-04 *"다 권고대로"* 의 권고안 · 생산 원장 없음).
- 같은 기계 · 시작 틱 못 읽은 산 pid (`chain_start` null) = 산 것으로 (보수).
- 볼 수 있는 호스트에서 사슬 부모를 확인할 수 없음 (`/proc` 를 못 읽음 = `chain_parent_alive` None · 꼴 틀린 사슬 칸은 원장 해석 `_start_problem` 이 먼저 거부) = rc 3 · 운영자 확인 표지로도 안 덮음 → 그 시도 = 사람이 원장을 보기 전까지 멈춤 (보수 · 거짓 수용 없음 · PC6-01 의 hidepid 한정과 같은 부류).
- 시작 기록 없는 시도 = 옛 규칙 (그룹 기록 대조만).
- AL07 예외 = 사슬 흔적까지 지운 남의 폴더 + 원장 고침 = Q-D.
- 처음 다른 바이트 · 길이 차 = 봉인 바이트에서 나온 수 (보고 전용 · 문구로만 · 값 감추기 안 함).
- 등록 R §10-5 아 ⑦ · Q9 §3-5 · 웹앱 설명 페이지 = 시작 기록 사슬 부모 규칙 문장 안 실음 (메인 · 1저자 몫) · 웹앱 = 바뀐 화면 없음.

## 6. 파일

`run_regression.sh` (회귀) · `mutate_pc8fix.py` (새 가드 변이) · `kill_before.py` (M26 · B01 ↔ 새 시험 · 고치기 전 코드) · `logs/` · `SHA256SUMS` (이 폴더의 다른 파일 전부 · `sha256sum -c SHA256SUMS` 를 이 폴더에서).

커밋 차례 (작업 트리 가지 `pc8-fix-1104b` · 기준 `74150affc`) — `935ef2223` 시험 먼저 → `1cb165fef` 시험 결함 (PD12u 정수 칸 dict · 기대 그대로) → `563b4019a` 고침 → `7141ac593` 사전 공격 8 회차 반입 (바이트 그대로) → `355c1b6d0` 변이 보강 시험 (PD12u 줄 넷 · 코드 변경 없음) → 이 증거 · 원장 · 요청서 커밋.
