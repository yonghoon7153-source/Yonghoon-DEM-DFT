# Rint ② 사전 공격 12 고침 (PC12-01 – 05 · 11-08 · 시험 먼저 · 작업 트리 에이전트)

- 바탕 = `2b3c42c6c` (작업 가지 끝 · `scripts/rint_r_chain.py` 는 `6a81f0c55` 와 같음) · 바탕 · 고친 판의 파일 sha256 = `logs/code_sha256.txt` · push 없음 · `scripts/check_all.sh` 안 돌림 (메인 세션 게이트).
- 발견 = 독립 사전 공격 12 (11-08 · 보고 · 탐침 · 출력 사본 = `preattack12/`) · 규칙 = 1저자 11-06 *"생산자가 쓰지 않는 칸 조합 = 모순 = 재실행 자격 없음"* · 정직 (생산자 꼴) 기록은 판정 그대로 (받아들임 행 = 아래 표).
- 환경 = Linux 6.18 · Python 3.11.17 · numpy 2.4.6 · scipy 1.17.1 · kgy 판 = uv CPython 3.8.20 · numpy 1.24.4 · scipy 1.10.1 · 4 코어 · 시험 = 합성 폴더 · 가짜 러너 · 실제 git 원장 (이 컨테이너 · GPU 아님).
- 손대지 않은 것 = `docs/reviews/findings.json` (원장 = 메인 세션) · 요청서 · CLAUDE.md · 봉인 32 (`rint_r_chain.py` 는 봉인 파일 아님) · **웹앱 화면 없음** — `webapp/` 에 재실행 자격 · resume_ok · RESUME_NOT_ALLOWED · 원장 · 단계 요약 멈춤 사유를 보이는 화면이 없다 (grep 0).

## 0. 쉽게 말하면

- **F1** — 멈춘 런 기록의 outdir 를 옆 이름 (L01_floor_arm9) 으로 바꾸고 요청 칸 (arms 9) 도 맞춰 바꾸면 "정확 이름 대조" 를 지나 진짜 폴더 L01_floor_arm1/.unchecked/ 의 검사 실패 흔적을 비켰다 (범위 안 arms 2 도) → 요청 칸은 생산자 범위 (arms 1–8 · arm_list 정렬 · 중복 없음 · 0–7 · 접두 아님 · 길이 = arms) 아니면 사유 · 흔적은 그 런의 출력 폴더 꼴 (<런> · <런>_arm…) **전부** 에서 본다.
- **F2** — GU 대조가 끝 기록의 확인 칸만 봐서 정직 GU (러너 스스로 rc 1 · 끝 기록 rc 1 · 확인 False) 의 런 기록 rc 1 → 0 한 칸이 재실행 자격을 얻었다 → 런 기록 꼴 ↔ 사슬 쪽 끝 기록 (원인 · rc · 확인) 을 생산자 대응표로 대조 (§5) · rc 같음 판독 = 새 판독 함수 `rc_equal` (RC01 목록에 등재).
- **F3** — 런 기록 없는 TIME_LIMIT (런 전 시간 상한) 이 runs 를 안 봐 정직 RUNNER_RC (L01 rc 1) 요약의 stop 두 칸만 바꾸면 자격 → 멈춘 런 **앞** 의 런 기록 전부 = 끝난 런 (rc 0 · 팔 읽음) 아니면 모순.
- **F4** — 결과 줄 길의 단계 요약 읽기가 느슨한 json.loads (중복 칸 = 뒤 값 · NaN) → 거부 기록 · 계획 · 원장과 같은 `_json_strict` (중복 · NaN · ±Infinity = unreadable · 자격 False).
- **F5** — 거부 기록 code 가 글자 꼴만 → `STOPS` 의 이름이어야 한다.

## 1. 발견 → 시험 → 고침 → 자리

| 발견 | 시험 (`scripts/test_rint_r_chain.py` · PC12 블록 15240 –) | 고침 (`scripts/rint_r_chain.py`) | 줄 |
|---|---|---|---|
| F1 PC12-01 (P2) | **PC12A** 27 행 = 정직 9 (arm1 흔적 · 흔적 없음 · arms 2 · 8 팔 · arml · TIME_LIMIT) · 함께 고침 13 (arms 9 · 0 · −1 · 10**30 · arm_list [] · [0] · [9] · [3,3] · [3,1] · 길이 ≠ arms · 범위 안 arms 2 둘) · 요청 칸 없는 옆 이름 + 흔적 1 · 실경로 (실제 git 원장 · recover → 결과 줄 → `--add --resume`) 4 | `request_fields_problem` + `ARMS_RANGE` · `ARM_INDEX_RANGE` · `record_outdir` 범위 밖 = '' · `stopped_record_problem` ②′ 사유 · `stop_trace` (od + 디스크의 <런> · <런>_arm* 전부 · 폴더 못 읽음 = 흔적 있음) · `result_fields` 가 `stop_trace` 를 부름 | 4883–4915 · 4061–4063 · 3786–3800 · 4358 |
| F2 PC12-02 (P2) | **PC12B** 33 행 = 정직 15 (GU rc 0 · rc 1 · timeout · rc null · signal · signal_after · recover chain_end · 옛 recover 끝 기록 · TIME_LIMIT 확인 True · RUNNER_RC rc 1 · signal · signal_after) · 모순 14 (탐침 2b 한 칸 · 2c 두 칸 · recover 한 칸 · 원인 어긋남 · 디스크 원인 signal_after · rc null · TIME_LIMIT 확인 False · RUNNER_RC 끝 rc 0 · 확인 False · rc bool · by weird …) · 실경로 4 | `chain_side` (by chain 끝 기록 · by recover 의 chain_end → {cause · rc · confirmed} · None = 못 읽음 · 'bad') · `CHAIN_SIDE_SHAPES` · `STOP_CONFIRMED` · `chain_side_problem` · `rc_equal` (판독 함수) · `stopped_record_problem` ④ = 세 멈춤 코드 모두 (옛 = GU 의 확인 칸만) · `chain_confirmed` = 확인 칸 wrapper (이름 유지) | 4082–4155 · 3852–3856 · 4072–4078 |
| F3 PC12-03 (P2) | **PC12C** 17 행 = 정직 5 (앞 런 끝남 · 첫 런 전 · GU · signal · 재실행 복사 기록) · 모순 8 (탐침 p4 L02 · zzz · p5 a1 · a2 · 앞 런 exit_ok 인데 arms_read [] · killed · arms_read 객체 · group_cause 칸 없음) · 실경로 4 | `prior_runs_problem` (멈춘 런 앞의 기록 전부 = `run_record_shape` exit_ok + arms_read 비지 않은 목록 · 런 기록 없는 멈춤 = runs 전부) · `stop_record_problem` 끝에서 부름 | 4157–4175 · 4035 |
| F4 PC12-04 (P3) | **PC12D** 10 행 = 중복 칸 (런 기록 안 · 최상위) · NaN · Infinity · −Infinity = unreadable · 정준 바이트 · 다른 객체의 같은 이름 칸 = ok · 탐침 b 다시 셈 · 생산자 바이트 다시 셈 · 실경로 1 | `read_summary_state` = `_json_strict` (옛 = json.loads) | 5759 |
| F5 PC12-05 (P3) | **PC12E** 14 행 = XYZ · CALIBRATED · PREDICTED · STOPPED · REJECTED · OK · 소문자 = Stop · 생산자 · RUNNER_RC = rejected · `STOPS` 전부 받음 · 밖 7 거부 · 실경로 3 (XYZ · CALIBRATED = recover 못 쓴 수 1 · 다시 셈 Stop · 생산자 = rejected) | `rejected_form_problem` code ∈ `STOPS` | 4410 |
| 머리말 | CT08 (이름 전부 모듈에 있음) | ★ 11-08 PC12 문단 | 171–176 |

- 고정물 고침 (뜻 그대로 · 둘): ① AL12c 'rej' 팔의 손 거부 기록 멈춤 이름 'X' (STOPS 밖 = 생산자가 쓰지 않는 값) → MACHINE_NOT_ALLOWED (결과 줄 멈춤 이름도 같게 · 이 팔의 뜻 "거부 기록만 있는 폴더 = 원장 대조 통과" 그대로 · 11-06 PC10 때도 같은 고정물을 같은 이유로 고쳤다) ② RC01 `RC_READERS` 에 `rc_equal` 등재 (rc 값 비교 = 판독 함수로만 · 첫 전체 돌림에서 RC01 이 `rc == rr.get('rc')` · 삼항식 안 칸 옮기기 둘을 날 읽기로 잡아 고침 → `rc_equal` · 문장 나눔).
- 적용 = `apply_tests.py` (시험 블록 끼움) · `apply_chain.py` (정확한 글 바꿈 12 · 각각 한 번 · 원자적 쓰기) + RC01 뒤 손 고침 셋 (`rc_equal` · `chain_side` 삼항식 · `chain_side_problem`) — 이 폴더.

## 2. 고치기 전 → 뒤 (수)

| 묶음 | 고치기 전 (바탕 `2b3c42c6c`) | 고친 뒤 |
|---|---|---|
| 새 시험 PC12A–E (`--only PC12`) | **0/5 PASS** (`logs/before_PC12.log` · 자르지 않은 판정 `logs/before_PC12_rows.json`) — 실패 행 = 위조 · 함께 고침 행만: A 16 · B 16 · C 10 · D 7 · E 9 · 정직 행 전부 통과 | **5/5 PASS** (`logs/after_PC12.log` · `logs/after_PC12_rows.json` · n_bad 0 · 끝 판) |
| 사슬 `scripts/test_rint_r_chain.py` (3.11) | 476/476 PASS (351.5 s · `logs/before_chain_full_py311.log`) | 첫 전체 돌림 479/481 (AL12c = 고정물 code 'X' · RC01 = 새 코드의 날 rc 읽기 셋 · `logs/after_chain_full_py311_first.log`) → 고정물 · `rc_equal` 고침 → 겨냥 14/14 (`logs/after_RC01_PC12_targeted.log`) → 전체 다시 **481/481 PASS (418.3 s)** (`logs/after_chain_full_py311.log`) |
| 끝-끝 `scripts/test_rint_r_chain_e2e.py` (3.11) | 51 PASS · 0 FAIL (685.0 s · `logs/before_e2e_py311.log`) | 51 PASS · 0 FAIL (732.5 s · `logs/after_e2e_py311.log` · 첫 고침 판) |
| `scripts/test_rint_first_result.py` | 9/9 PASS | 9/9 PASS (`logs/after_first_result.log`) |
| `scripts/test_ca_ext_runner.py` | 151 PASS · 0 FAIL | 151 PASS · 0 FAIL (`logs/after_ca_ext_runner.log`) |
| kgy 판 3.8 (`scripts/check_kgy_py38.sh` · 11 묶음) | — (11-05 보고 = 11 묶음 통과) | **11 묶음 통과 (사슬 481/481 · 끝-끝 51 PASS · 0 FAIL · Python 3.8.20)** (`logs/check_kgy_py38.out` · `logs/py38/` · 끝 판) |
| `scripts/check_doc_refs.py` | — | 깨진 참조 0 · rc 0 (`logs/check_doc_refs_final.log`) |

## 3. 변이 (`mutate_pc12.py` · 리포 밖 사본 트리 (끝 판) · 한 번에 하나 · 매번 원 바이트로 되돌림 · 끝 sha256 = 시작 · `logs/mutation_pc12.json`)

| 변이 | 끈 가드 | 기대 실패 | 실패한 검사 | 잡힘 |
|---|---|---|---|---|
| M1_range_off | `request_fields_problem` 의 arms · arm_list 범위 | PC12A | PC12A 만 | ✓ |
| M1b_trace_od_only | `stop_trace` 를 옛 꼴 (od 하나) 로 | PC12A | PC12A 만 | ✓ |
| M2a_side_shapes_off | `CHAIN_SIDE_SHAPES` = {} ((원인, rc) 대응 끔) | PC12B | PC12B 만 | ✓ |
| M2b_confirmed_gu_only | `STOP_CONFIRMED` = GU 만 (옛 꼴) | PC12B | PC12B 만 | ✓ |
| M3_prior_off | `prior_runs_problem` → None | PC12C | PC12C 만 | ✓ |
| M4_lenient_json | `read_summary_state` = json.loads (옛 꼴) | PC12D | PC12D 만 | ✓ |
| M5_code_shape_only | `rejected_form_problem` 의 in STOPS 뺌 | PC12E | PC12E 만 | ✓ |

7/7 잡힘 · 변이마다 다른 네 검사는 통과 (가드 하나 ↔ 검사 하나) · 사본 트리 무변이 = 5/5 PASS (`logs/mut_sanity_rows.json`).

## 4. 탐침 다시 (사전 공격 12 의 탐침 원본 그대로 · 하네스만 이 작업 트리 scripts/ 로 (`probe_rerun/harness_worktree.py`) · 끝 판 · `probe_rerun/`)

| 탐침 · 행 | 고치기 전 (`preattack12/`) | 고친 뒤 (`probe_rerun/`) |
|---|---|---|
| p1 정직 arms 1 · _arm1 (흔적) | resume_ok False | False (그대로) |
| p1 함께 고침 11 가지 (arms 9 · 0 · −1 · 10**30 · arm_list [] · [0] · [9] · [3,3] · [3,1] · TIME_LIMIT arms 9) | **True** | **False** · stop_record_problem 사유 |
| p1 함께 고침 범위 안 (arms 2 · _arm2 · RUNNER_RC · TIME_LIMIT) | **True** | **False** (사유 없음 · 흔적 = 그 런 폴더 전부) |
| p2 (1a) 옆 이름 arms 1 · (1c) 정직 | False · rc 3 | False · rc 3 (그대로) |
| p2 (1b) arms 9 함께 고침 (실제 원장) | **True · resume rc 0** | **False · rc 3 RESUME_NOT_ALLOWED** |
| p2 (2a) 정직 GU rc 1 | runner_rc · False · rc 3 | 그대로 |
| p2 (2b) 한 칸 rc 1 → 0 · (2c) 두 칸 {timeout · null} | **group_unconfirmed · True · rc 0** | **False · rc 3 RESUME_NOT_ALLOWED** |
| p4 정직 RUNNER_RC L01 rc 1 | runner_rc · False · rc 3 | 그대로 |
| p4 위조 TIME_LIMIT run L02_ceiling · zzz | **timeout · True · rc 0** | **timeout · False · rc 3 RESUME_NOT_ALLOWED** |
| p5 (a1) [L01 rc 1, L02 {timeout,null}] TIME_LIMIT · (a2) [L01 rc 1, L02 {None,0}] GU | **True** | **False** |
| p5 (b) 중복 칸 요약 | 읽기 ok · 뒤 값 arms 9 · 다시 셈 resource · **True** | **unreadable** · 다시 셈 interrupted · summary_unreadable · False (원 탐침은 None 첨자로 Traceback = 고침의 효과 · None 안전 사본 `probe_rerun/p5_misc_b_fixed.py`) |
| p5 (c1 선언 한정) arms 칸 없음 + _arm9 (+ _arm1 흔적) | True | **False** (흔적 = 그 런 폴더 전부 → 선언 한정 닫힘) |
| p5 (c2 선언 한정) GU {None,0} · 그룹 기록 없음 | True | True (그대로 · 사슬 쪽 끝 기록이 없으면 대조 못 함 · 한정 유지) |
| p5 (c3) 같은 + 끝 기록 확인 True | False | False |
| p5 (c4 선언 한정) RUNNER_RC rc 1 끝 기록 → 런 기록 {signal,null} | True | **False** (사슬 쪽 원인 None ≠ signal → 선언 한정 닫힘) |
| p6 code XYZ · CALIBRATED | rejected (그 이름 그대로) | **Stop ATTEMPT_LEDGER_MISMATCH** |
| p6 code GENERATION · OUTDIR_NOT_EMPTY (STOPS 안 · 풀기 전 자리가 아닌 이름) | rejected | rejected (그대로 · §6 한정) |
| p6 그 밖 (생산자 · utc "" · cause "" · n 꼴 · 중복 · NaN · BOM · 숨은 폴더 · 폴더) | 바탕 값 | 바탕 값 그대로 |

## 5. 생산자 대응표 (코드 = `CHAIN_SIDE_SHAPES` 4123 · `STOP_CONFIRMED` 4127 · `rc_equal` 3852 · 근거 줄 = `scripts/rint_r_chain.py` 고친 판)

| 멈춘 런 기록 (group_cause, rc) = `run_record_shape` | 디스크 사슬 쪽 (cause, rc) — by chain 끝 기록 · recover 끝 기록의 chain_end | 멈춤 코드 ↔ confirmed | 근거 (줄) |
|---|---|---|---|
| exit_ok (None, 0) · exit_fail (None, 정수 ≠ 0) | cause None · rc = **같은 정수** (`rc_equal`) | GU ⇒ False · RUNNER_RC (exit_fail) ⇒ True | `Runner._execute` 4974 (rec.rc = 원인 None 일 때만 `run_in_group` 의 rc) · 4975 (group_cause = 돌려준 원인) · `run_in_group` 2791 (디스크 끝 기록 rc · cause = 같은 값) |
| killed:timeout (timeout, null) | cause 'timeout' · rc 정수 \| null | GU ⇒ False · TIME_LIMIT ⇒ True | 2778–2780 (SIGKILL 뒤 wait = 정수 · 못 회수 = None) · 2791 · 4974 (rc None) · 4981 |
| killed:signal (signal, null) | cause 'signal' · rc 정수 \| null | GU ⇒ False · RUNNER_RC ⇒ True | 같은 줄 · 4983 |
| killed:signal_after (signal_after, null) | cause **None** · rc **정수** (러너 스스로 끝남) | GU ⇒ False · RUNNER_RC ⇒ True | 2800 (디스크 원인 None 그대로 · 돌려주는 원인만 signal_after · rc = 러너 스스로의 wait 값) · 4974–4975 · 4985 |
| (확인 차례) | — | 확인 False ⇒ GROUP_UNCONFIRMED **먼저** (4976–4979) · TIME_LIMIT · RUNNER_RC = 확인 True 뒤에만 (4981–4988) | `Runner._execute` |
| (recover 끝 기록) | chain_end = 옛 by chain 끝 기록의 {rc · cause · confirmed · ended_utc} 사본 → 같은 표 · chain_end 없음 = 대조 안 함 | — | `recover_group` 7530 · 7582 |

F3 (앞 런 = 끝난 런): `Runner._execute` 4988 (rc 성공 아니면 Stop) → 4989–4997 (`read_run` → arms_read = 팔 기록 · 실패 = Stop) = 다음 런 기록은 rc 0 · 팔 읽음 뒤에만 · `ResumeRunner._copy` 5071 (rc 0 · group_cause None) · 5079 (arms_read) · 합치기 `MergeFetch` 6397 · 6415.
F1 (요청 칸 범위): `run_request` 4861–4863 (arm_list = 정렬 · 비지 않음 · 중복 없음 · 0–7 · 접두 0..N−1 아님 · arms = 길이) · 러너 `scripts/sdcp_gain_vox015_8arm.sh` 46–63 (ARM_LIST 0–7 한 자리 · 중복 · 접두 거부) · 73–76 (ARMS 1..8) · `Runner._prepare` 4955 (outdir = name + `run_outdir_suffix`).
F4 (생산자 바이트): `write_summary` → `canon_bytes` (sort_keys · allow_nan False) + `_clean` (NaN · inf → null) = 정직 요약에 중복 칸 · NaN 없음 ⇒ 엄격 읽기가 정직 요약을 막지 않는다 (PC12D canonical 행 · 사슬 · 끝-끝 전체 시험).

## 6. 한정 (닫지 않은 것 · 범위가 바뀐 것)

- 요청 칸 없는 기록 (arms 칸 없음 = 시험 고정물 꼴) 은 outdir 접두 규칙만 (그대로) — 흔적은 이제 그 런 폴더 전부에서 보므로 흔적 있는 옆 이름은 막힌다 (c1) · 흔적 없는 옆 이름 자체는 받는다.
- 디스크에 그 런의 다른 출력 폴더 (옆 이름) 가 있다는 사실 자체는 모순으로 세지 않는다 (흔적 없으면 받음).
- 사슬 쪽 끝 기록이 없거나 (그룹 기록 없는 GU · c2) · 시작 기록에 결합 안 됨 · chain_end 없는 옛 recover 끝 기록 = 대조 안 함 (옛 그대로).
- 런 전 TIME_LIMIT 의 run 이름 차례 (다음 이름인지) 는 보지 않는다 — 'zzz' 는 앞 런 실패 규칙으로만 막혔다 (앞 런이 정직하게 끝난 뒤 'zzz' = 받음).
- F4: 1e400 같은 큰 수 리터럴은 inf 로 읽힌다 (`_json_strict` = NaN · Infinity 상수 · 중복 칸만) — 읽는 칸의 꼴 검사가 따로 막는다.
- F5: `STOPS` 안이지만 풀기 전 자리에서 생산자가 쓰지 않는 이름 (GENERATION · ARM_* 등 결과 뒤 멈춤 · OUTDIR_NOT_EMPTY 옆 기록 전용) 은 받는다 — 풀기 전 코드 집합은 열거하지 않았다 (`attempt_open` 의 Stop 전부).
- 같은 이름 런 기록 둘 · 다른 칸 (copied_from · seconds · machine …) · utc 글 꼴 = 그대로.
- 범위가 바뀐 것 (모두 자격 없음 쪽 · 생산자 꼴 아님): ① TIME_LIMIT · RUNNER_RC 멈춤인데 그 런 끝 기록의 사슬 쪽 확인이 False (또는 원인 · rc 어긋남) = 자격 없음 (옛 = GU 만 봄) ② 앞 런 기록이 exit_ok 인데 arms_read 가 빈 목록 · 꼴 틀림 · group_cause 칸 없음 = 모순 (옛 = 안 봄 — group_cause 칸이 생기기 전 (10-27 묶음 C1b 전) 옛 요약은 그 뒤 멈춤이 자격 없음으로 읽힌다 · 그런 요약에 재실행 자격을 준 적은 없다) ③ 요약 있는 길에서 디스크 끝 기록의 원인 'signal_after' (시험 고정물 꼴 · A1b 가 요약 없는 길에서 받는 값) 는 런 기록 killed:signal_after 와 모순 (생산자 디스크 원인 = None · `run_in_group` 2800) — 요약 없는 길 (`orphan_cause` · A1b) 읽기는 바꾸지 않았다 ④ 단계 요약의 중복 칸 · NaN · ±Infinity = unreadable (옛 = 읽음 · 생산자 바이트에는 없다).
- 시험 = 합성 · 가짜 러너 · 실제 git 원장 · 이 컨테이너 — 실제 kgy 3.8.10 · ibb · GPU 아님.  원장 (`findings.json` PC12-01 – 05 등재 · claimed_fixed) · 요청서 · CLAUDE.md · Codex 짧은 재확인 = 메인 세션 몫.

## 7. 파일

`REPORT.md` · `apply_tests.py` · `apply_chain.py` · `dump_pc12.py` · `mutate_pc12.py` · `logs/` (code_sha256.txt · before_* · after_* · before/after_PC12_rows.json · after_RC01_PC12_targeted.log · after_AL12c_fixture.log · mutation_pc12.json · mut_M*.json · mut_sanity_rows.json · check_kgy_py38.out · py38/ · check_doc_refs_final.log) · `probe_rerun/` (after_p1 · p2 · p4 · p5 · p5_fixed · p6 · harness_worktree.py · p5_misc_b_fixed.py) · `preattack12/` (독립 사전 공격 12 의 보고 · 탐침 · 출력 사본 그대로) · `SHA256SUMS` (이 폴더에서 sha256sum -c SHA256SUMS · 상대 경로 · 자신은 빠짐).
